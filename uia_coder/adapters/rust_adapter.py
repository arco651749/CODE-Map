import bisect
from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_rust as tsrust

from uia_coder.core.base_adapter import BaseUIAGraphBuilder
from uia_coder.core.graph import UIACodeGraph


class RustUIAGraphBuilder(BaseUIAGraphBuilder):
    """
    基於 Tree-sitter TreeCursor 的高效穩定 Rust 語意控制樹建構器
    - 採用 TreeCursor 走訪與位元組索引切片，避免 Windows C 擴充記憶體訪問越界 (Access Violation)
    - 追蹤頂層函式 (fn)、結構體關聯方法 (impl Type)
    - 識別 #CLI: main 進入點與因果調度樹
    - 偵測 panic! / todo! / unimplemented! 執行期未決危害 (Hazards)
    """

    @property
    def supported_extensions(self) -> Set[str]:
        return {".rs"}

    @property
    def language_name(self) -> str:
        return "Rust"

    def __init__(self):
        self.language = Language(tsrust.language())
        self.parser = Parser(self.language)

    def parse_and_build(self, source_code: str, file_path: str = "main.rs") -> UIACodeGraph:
        # 保持 source_bytes 於局部變數生命週期內，防止 PyMalloc 記憶體重用
        source_bytes = source_code.encode("utf-8")
        tree = self.parser.parse(source_bytes)
        graph = UIACodeGraph(name=f"Graph of {file_path}")

        # 預先計算換行位元組位移，安全且極速換算行號
        line_starts = [0]
        for i, b in enumerate(source_bytes):
            if b == 10:  # ord('\n')
                line_starts.append(i + 1)

        def get_line(byte_offset: int) -> int:
            return bisect.bisect_right(line_starts, byte_offset)

        def decode_slice(start: int, end: int) -> str:
            return source_bytes[start:end].decode("utf-8", errors="replace")

        defs: Dict[str, str] = {}

        # 階段 1：收集所有 impl 結構體與函式宣告
        cursor = tree.walk()
        impl_stack: List[str] = []

        while True:
            node = cursor.node
            ntype = node.type

            if ntype == "impl_item":
                t_node = node.child_by_field_name("type")
                impl_name = "Anonymous"
                if t_node:
                    raw_t = decode_slice(t_node.start_byte, t_node.end_byte)
                    impl_name = raw_t.split("<")[0].lstrip("&* ").strip()
                impl_stack.append(impl_name)

            elif ntype == "function_item":
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    curr_impl = impl_stack[-1] if impl_stack else None
                    fn_name = f"{curr_impl}::{raw_name}" if curr_impl else raw_name
                    start_row = get_line(node.start_byte)
                    end_row = get_line(node.end_byte)
                    node_id = f"func:{fn_name}@{file_path}:L{start_row}"

                    params_node = node.child_by_field_name("parameters")
                    params = decode_slice(params_node.start_byte, params_node.end_byte) if params_node else "()"
                    sig = f"fn {fn_name}{params}"
                    source_code_slice = decode_slice(node.start_byte, node.end_byte)

                    defs[fn_name] = node_id
                    defs[raw_name] = node_id
                    if curr_impl:
                        defs[f"{curr_impl}.{raw_name}"] = node_id

                    is_async = "async" in decode_slice(node.start_byte, min(len(source_bytes), node.start_byte + 30))

                    graph.add_node_rich(
                        node_id=node_id,
                        label=fn_name,
                        category="FUNCTION_DEF",
                        scope={"scope_id": curr_impl or "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": sig,
                            "parameters": params,
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "line_count": max(1, end_row - start_row + 1),
                            "is_async": is_async,
                            "impl_type": curr_impl or "",
                            "raw_name": raw_name,
                        },
                    )

            if cursor.goto_first_child():
                continue

            # 葉節點離開
            if ntype == "impl_item" and impl_stack:
                impl_stack.pop()

            if cursor.goto_next_sibling():
                continue

            # 回溯父節點
            found = False
            while cursor.goto_parent():
                p_type = cursor.node.type
                if p_type == "impl_item" and impl_stack:
                    impl_stack.pop()
                if cursor.goto_next_sibling():
                    found = True
                    break
            if not found:
                break

        # 階段 2：走訪呼叫點與巨集 (Pass 2)
        cursor = tree.walk()
        impl_stack = []
        func_stack: List[Tuple[str, str, Optional[str]]] = []

        while True:
            node = cursor.node
            ntype = node.type

            if ntype == "impl_item":
                t_node = node.child_by_field_name("type")
                impl_name = "Anonymous"
                if t_node:
                    raw_t = decode_slice(t_node.start_byte, t_node.end_byte)
                    impl_name = raw_t.split("<")[0].lstrip("&* ").strip()
                impl_stack.append(impl_name)

            elif ntype == "function_item":
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    curr_impl = impl_stack[-1] if impl_stack else None
                    fn_name = f"{curr_impl}::{raw_name}" if curr_impl else raw_name
                    start_row = get_line(node.start_byte)
                    caller_id = f"func:{fn_name}@{file_path}:L{start_row}"
                    func_stack.append((caller_id, fn_name, curr_impl))

            elif ntype == "macro_invocation" and func_stack:
                caller_id, caller_fn, curr_impl = func_stack[-1]
                macro_node = node.child_by_field_name("macro")
                if macro_node:
                    m_name = decode_slice(macro_node.start_byte, macro_node.end_byte)
                    m_row = get_line(node.start_byte)

                    if m_name in ("panic", "todo", "unimplemented"):
                        hazard_id = f"hazard:{m_name}@{file_path}:L{m_row}"
                        graph.add_node_rich(
                            node_id=hazard_id,
                            label=f"{m_name}! [未完成實作/執行期中斷]",
                            category="FUNCTION_DEF",
                            scope={"scope_id": curr_impl or "scope:global", "file": file_path, "line": m_row},
                            props={"hazard": f"RUST_{m_name.upper()}", "is_blocking": True},
                        )
                        graph.add_edge_rich(
                            caller_id,
                            hazard_id,
                            edge_type="CALLS",
                            status="BLOCKED_INVARIANT",
                            detail=f"呼叫了未完成實作或執行期中斷巨集: {m_name}!()",
                        )
                    else:
                        target_id = f"macro:{m_name}!@external"
                        if target_id not in graph.g:
                            graph.add_node_rich(
                                node_id=target_id,
                                label=f"{m_name}! (Macro)",
                                category="FUNCTION_DEF",
                                scope={"scope_id": "external", "file": "std", "line": 0},
                                props={"signature": f"{m_name}!()", "source_code": ""},
                            )
                        graph.add_edge_rich(
                            caller_id,
                            target_id,
                            edge_type="CALLS",
                            status="VALID",
                            detail="調用標準庫或外部巨集",
                        )

            elif ntype == "call_expression" and func_stack:
                caller_id, caller_fn, curr_impl = func_stack[-1]
                fn_node = node.child_by_field_name("function")
                if fn_node:
                    target_text = decode_slice(fn_node.start_byte, fn_node.end_byte)
                    method_name = target_text.split(".")[-1].split("::")[-1]

                    target_def_id = None
                    if target_text in defs:
                        target_def_id = defs[target_text]
                    elif curr_impl and f"{curr_impl}::{method_name}" in defs:
                        target_def_id = defs[f"{curr_impl}::{method_name}"]
                    elif method_name in defs:
                        target_def_id = defs[method_name]

                    if not target_def_id:
                        ext_id = f"func:{target_text}@external"
                        if ext_id not in graph.g:
                            graph.add_node_rich(
                                node_id=ext_id,
                                label=f"{target_text} (External/Unresolved)",
                                category="FUNCTION_DEF",
                                scope={"scope_id": "external", "file": file_path, "line": 0},
                                props={"signature": f"{target_text}()", "source_code": ""},
                            )
                        target_def_id = ext_id

                    is_await = b".await" in source_bytes[node.start_byte:node.end_byte]
                    graph.add_edge_rich(
                        caller_id,
                        target_def_id,
                        edge_type="CALLS",
                        status="VALID",
                        detail="調用函式或結構體方法",
                        flow_type="ASYNC" if is_await else "SYNC",
                    )

            if cursor.goto_first_child():
                continue

            if ntype == "impl_item" and impl_stack:
                impl_stack.pop()
            if ntype == "function_item" and func_stack:
                func_stack.pop()

            if cursor.goto_next_sibling():
                continue

            found = False
            while cursor.goto_parent():
                p_type = cursor.node.type
                if p_type == "impl_item" and impl_stack:
                    impl_stack.pop()
                if p_type == "function_item" and func_stack:
                    func_stack.pop()
                if cursor.goto_next_sibling():
                    found = True
                    break
            if not found:
                break

        # 階段 3：若包含 fn main()，自動註冊 CLI 程式入口錨點
        main_nodes = [n for n, d in graph.g.nodes(data=True) if d.get("label") == "main" or n.startswith("func:main@")]
        if main_nodes:
            main_nid = main_nodes[0]
            m_scope = graph.g.nodes[main_nid].get("scope", {})
            m_line = m_scope.get("line", 1)
            entry_id = f"ctrl:CLI:main@{file_path}:L{m_line}"
            graph.add_node_rich(
                node_id=entry_id,
                label="#CLI: main",
                category="UI_CONTROL",
                scope={"scope_id": "scope:global", "file": file_path, "line": m_line},
                props={
                    "ui_type": "CLI Entry",
                    "source_code": "fn main() { ... }",
                    "line_start": m_line,
                    "line_end": m_line,
                },
            )
            evt_id = f"event:CLI.run@{file_path}:L{m_line}"
            graph.add_node_rich(
                node_id=evt_id,
                label="run()",
                category="EVENT_BINDING",
                scope={"scope_id": "scope:global", "file": file_path, "line": m_line},
                props={"event": "run"},
            )
            graph.add_edge_rich(entry_id, evt_id, edge_type="WIRES_TO", status="VALID")
            graph.add_edge_rich(
                evt_id,
                main_nid,
                edge_type="TRIGGERS",
                status="VALID",
                detail="CLI 觸發 main() 進入點",
            )

        return graph
