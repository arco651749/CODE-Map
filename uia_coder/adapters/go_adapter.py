import bisect
from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_go as tsgo

from uia_coder.core.base_adapter import BaseUIAGraphBuilder
from uia_coder.core.graph import UIACodeGraph


class GoUIAGraphBuilder(BaseUIAGraphBuilder):
    """
    基於 Tree-sitter TreeCursor 的高效穩定 Go 語意控制樹建構器
    - 採用 TreeCursor 走訪與位元組索引切片，避免 Windows C 擴充記憶體訪問越界 (Access Violation)
    - 追蹤頂層函式 (func)、結構體接收器方法 (func (r *Receiver) Method)
    - 識別 #CLI: main 進入點與 Goroutine 非同步調度
    - 偵測 panic() 未決恐慌與 time.Sleep() 同步阻塞危害 (Hazards)
    """

    @property
    def supported_extensions(self) -> Set[str]:
        return {".go"}

    @property
    def language_name(self) -> str:
        return "Go"

    def __init__(self):
        self.language = Language(tsgo.language())
        self.parser = Parser(self.language)

    def parse_and_build(self, source_code: str, file_path: str = "main.go") -> UIACodeGraph:
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

        def extract_receiver_type(node: Node) -> Optional[str]:
            recv_node = node.child_by_field_name("receiver")
            if not recv_node:
                return None
            raw = decode_slice(recv_node.start_byte, recv_node.end_byte)
            parts = raw.strip("() ").split()
            if len(parts) >= 2:
                return parts[-1].lstrip("*& ")
            elif len(parts) == 1:
                return parts[0].lstrip("*& ")
            return None

        defs: Dict[str, str] = {}

        # 階段 1：收集所有函式宣告與結構體接收器方法
        cursor = tree.walk()
        while True:
            node = cursor.node
            ntype = node.type

            if ntype in ("function_declaration", "method_declaration"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    recv_type = extract_receiver_type(node)
                    fn_name = f"{recv_type}.{raw_name}" if recv_type else raw_name
                    start_row = get_line(node.start_byte)
                    end_row = get_line(node.end_byte)
                    node_id = f"func:{fn_name}@{file_path}:L{start_row}"

                    params_node = node.child_by_field_name("parameters")
                    params = decode_slice(params_node.start_byte, params_node.end_byte) if params_node else "()"
                    sig = f"func {fn_name}{params}"
                    source_code_slice = decode_slice(node.start_byte, node.end_byte)

                    defs[fn_name] = node_id
                    defs[raw_name] = node_id

                    graph.add_node_rich(
                        node_id=node_id,
                        label=fn_name,
                        category="FUNCTION_DEF",
                        scope={"scope_id": recv_type or "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": sig,
                            "parameters": params,
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "line_count": max(1, end_row - start_row + 1),
                            "receiver_type": recv_type or "",
                            "raw_name": raw_name,
                        },
                    )

            if cursor.goto_first_child():
                continue

            if cursor.goto_next_sibling():
                continue

            found = False
            while cursor.goto_parent():
                if cursor.goto_next_sibling():
                    found = True
                    break
            if not found:
                break

        # 階段 2：走訪呼叫點與危害接線 (Pass 2)
        cursor = tree.walk()
        func_stack: List[Tuple[str, str, Optional[str]]] = []
        goroutine_stack: List[bool] = []

        while True:
            node = cursor.node
            ntype = node.type

            if ntype in ("function_declaration", "method_declaration"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    recv_type = extract_receiver_type(node)
                    fn_name = f"{recv_type}.{raw_name}" if recv_type else raw_name
                    start_row = get_line(node.start_byte)
                    caller_id = f"func:{fn_name}@{file_path}:L{start_row}"
                    func_stack.append((caller_id, fn_name, recv_type))

            elif ntype == "go_statement":
                goroutine_stack.append(True)

            elif ntype == "call_expression" and func_stack:
                caller_id, caller_fn, curr_recv = func_stack[-1]
                fn_node = node.child_by_field_name("function")
                if fn_node:
                    call_text = decode_slice(fn_node.start_byte, fn_node.end_byte)
                    call_row = get_line(node.start_byte)
                    is_async = len(goroutine_stack) > 0

                    if call_text == "panic":
                        hazard_id = f"hazard:panic@{file_path}:L{call_row}"
                        graph.add_node_rich(
                            node_id=hazard_id,
                            label="panic() [執行期恐慌/中斷]",
                            category="FUNCTION_DEF",
                            scope={"scope_id": curr_recv or "scope:global", "file": file_path, "line": call_row},
                            props={"hazard": "GO_PANIC", "is_blocking": True},
                        )
                        graph.add_edge_rich(
                            caller_id,
                            hazard_id,
                            edge_type="CALLS",
                            status="BLOCKED_INVARIANT",
                            detail="呼叫了執行期恐慌中斷常式: panic()",
                            flow_type="ASYNC" if is_async else "SYNC",
                        )
                    elif "time.Sleep" in call_text:
                        hazard_id = f"hazard:time.Sleep@{file_path}:L{call_row}"
                        graph.add_node_rich(
                            node_id=hazard_id,
                            label="time.Sleep() [同步休眠/介面凍結]",
                            category="FUNCTION_DEF",
                            scope={"scope_id": curr_recv or "scope:global", "file": file_path, "line": call_row},
                            props={"hazard": "GO_BLOCKING_SLEEP", "is_blocking": True},
                        )
                        graph.add_edge_rich(
                            caller_id,
                            hazard_id,
                            edge_type="CALLS",
                            status="BLOCKED_INVARIANT",
                            detail="呼叫了同步阻塞常式: time.Sleep()",
                            flow_type="ASYNC" if is_async else "SYNC",
                        )
                    else:
                        method_name = call_text.split(".")[-1]
                        target_def_id = None
                        if call_text in defs:
                            target_def_id = defs[call_text]
                        elif curr_recv and f"{curr_recv}.{method_name}" in defs:
                            target_def_id = defs[f"{curr_recv}.{method_name}"]
                        elif method_name in defs:
                            target_def_id = defs[method_name]

                        if not target_def_id:
                            ext_id = f"func:{call_text}@external"
                            if ext_id not in graph.g:
                                graph.add_node_rich(
                                    node_id=ext_id,
                                    label=f"{call_text} (External/Pkg)",
                                    category="FUNCTION_DEF",
                                    scope={"scope_id": "external", "file": file_path, "line": 0},
                                    props={"signature": f"{call_text}()", "source_code": ""},
                                )
                            target_def_id = ext_id

                        graph.add_edge_rich(
                            caller_id,
                            target_def_id,
                            edge_type="CALLS",
                            status="VALID",
                            detail="調用標準庫或外部 Go 套件",
                            flow_type="ASYNC" if is_async else "SYNC",
                        )

            if cursor.goto_first_child():
                continue

            if ntype in ("function_declaration", "method_declaration") and func_stack:
                func_stack.pop()
            if ntype == "go_statement" and goroutine_stack:
                goroutine_stack.pop()

            if cursor.goto_next_sibling():
                continue

            found = False
            while cursor.goto_parent():
                p_type = cursor.node.type
                if p_type in ("function_declaration", "method_declaration") and func_stack:
                    func_stack.pop()
                if p_type == "go_statement" and goroutine_stack:
                    goroutine_stack.pop()
                if cursor.goto_next_sibling():
                    found = True
                    break
            if not found:
                break

        # 階段 3：若包含 func main()，自動註冊 CLI 程式入口錨點
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
                    "source_code": "func main() { ... }",
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
