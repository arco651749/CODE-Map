from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_rust as tsrust

from uia_coder.core.base_adapter import BaseUIAGraphBuilder
from uia_coder.core.graph import UIACodeGraph


class RustUIAGraphBuilder(BaseUIAGraphBuilder):
    """
    基於 Tree-sitter 的 Rust 語意控制樹建構器
    - 追蹤頂層函式 (fn)、結構體關聯方法 (impl Type) 與巢狀函式 Scope
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
        tree = self.parser.parse(bytes(source_code, "utf-8"))
        graph = UIACodeGraph(name=f"Graph of {file_path}")

        scopes: Dict[str, Dict[str, Any]] = {
            "scope:global": {
                "id": "scope:global",
                "parent": None,
                "depth": 0,
                "defs": {},
            }
        }

        # 階段 1：盤點所有函式宣告 (fn) 與關聯方法 (impl Struct)
        self._collect_scopes_and_functions(tree.root_node, "scope:global", scopes, source_code, file_path, graph)

        # 階段 2：走訪呼叫點 (call_expression, field_expression, macro_invocation) 並接線
        self._wire_calls_and_macros(tree.root_node, "scope:global", scopes, source_code, file_path, graph)

        # 階段 3：若包含 fn main()，自動註冊 CLI 程式入口錨點
        main_nodes = [n for n, d in graph.g.nodes(data=True) if d.get("label") == "main"]
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

    def _collect_scopes_and_functions(
        self,
        node: Node,
        current_scope: str,
        scopes: Dict[str, Dict[str, Any]],
        source: str,
        file_path: str,
        graph: UIACodeGraph,
        current_impl_type: Optional[str] = None,
    ):
        if node.type == "impl_item":
            # 處理 impl StructType 區塊
            type_node = node.child_by_field_name("type")
            impl_type = type_node.text.decode("utf-8") if type_node else "AnonymousType"
            impl_scope_id = f"scope:impl:{impl_type}"
            scopes[impl_scope_id] = {
                "id": impl_scope_id,
                "parent": "scope:global",
                "depth": 1,
                "defs": {},
                "impl_type": impl_type,
            }
            body = node.child_by_field_name("body")
            if body:
                for child in body.children:
                    self._collect_scopes_and_functions(
                        child, impl_scope_id, scopes, source, file_path, graph, current_impl_type=impl_type
                    )
            return

        if node.type == "function_item":
            name_node = node.child_by_field_name("name")
            if name_node:
                raw_name = name_node.text.decode("utf-8")
                fn_name = f"{current_impl_type}::{raw_name}" if current_impl_type else raw_name
                start_row = node.start_point.row + 1
                end_row = node.end_point.row + 1
                node_id = f"func:{fn_name}@{file_path}:L{start_row}"

                # 提取完整原始碼與簽章
                source_code = source[node.start_byte : node.end_byte]
                params_node = node.child_by_field_name("parameters")
                params = params_node.text.decode("utf-8") if params_node else "()"
                sig = f"fn {fn_name}{params}"

                scopes[current_scope]["defs"][fn_name] = node_id
                if current_impl_type:
                    # 允許直接以方法名稱尋訪
                    scopes[current_scope]["defs"][raw_name] = node_id

                graph.add_node_rich(
                    node_id=node_id,
                    label=fn_name,
                    category="FUNCTION_DEF",
                    scope={"scope_id": current_scope, "file": file_path, "line": start_row},
                    props={
                        "signature": sig,
                        "parameters": params,
                        "source_code": source_code,
                        "line_start": start_row,
                        "line_end": end_row,
                        "line_count": max(1, end_row - start_row + 1),
                        "is_async": "async" in source[node.start_byte : node.start_byte + 30],
                        "impl_type": current_impl_type or "",
                        "raw_name": raw_name,
                    },
                )

                # 函式內部 scope
                inner_scope_id = f"scope:fn:{fn_name}@{start_row}"
                scopes[inner_scope_id] = {
                    "id": inner_scope_id,
                    "parent": current_scope,
                    "depth": scopes[current_scope]["depth"] + 1,
                    "defs": {},
                }

                body = node.child_by_field_name("body")
                if body:
                    for child in body.children:
                        self._collect_scopes_and_functions(
                            child, inner_scope_id, scopes, source, file_path, graph, current_impl_type
                        )
                return

        # 遞迴遍歷其他子節點
        for child in node.children:
            self._collect_scopes_and_functions(
                child, current_scope, scopes, source, file_path, graph, current_impl_type
            )

    def _wire_calls_and_macros(
        self,
        node: Node,
        current_scope: str,
        scopes: Dict[str, Dict[str, Any]],
        source: str,
        file_path: str,
        graph: UIACodeGraph,
        caller_func_id: Optional[str] = None,
        current_impl_type: Optional[str] = None,
    ):
        if node.type == "impl_item":
            type_node = node.child_by_field_name("type")
            impl_type = type_node.text.decode("utf-8") if type_node else None
            impl_scope_id = f"scope:impl:{impl_type}" if impl_type else current_scope
            body = node.child_by_field_name("body")
            if body:
                for child in body.children:
                    self._wire_calls_and_macros(
                        child, impl_scope_id, scopes, source, file_path, graph, caller_func_id, impl_type
                    )
            return

        if node.type == "function_item":
            name_node = node.child_by_field_name("name")
            if name_node:
                raw_name = name_node.text.decode("utf-8")
                fn_name = f"{current_impl_type}::{raw_name}" if current_impl_type else raw_name
                start_row = node.start_point.row + 1
                curr_func_id = f"func:{fn_name}@{file_path}:L{start_row}"
                inner_scope_id = f"scope:fn:{fn_name}@{start_row}"

                body = node.child_by_field_name("body")
                if body:
                    for child in body.children:
                        self._wire_calls_and_macros(
                            child, inner_scope_id, scopes, source, file_path, graph, curr_func_id, current_impl_type
                        )
                return

        # 1. 處理巨集調用 (macro_invocation: panic!, todo!, unimplemented!, println!)
        if node.type == "macro_invocation" and caller_func_id:
            macro_node = node.child_by_field_name("macro")
            if macro_node:
                m_name = macro_node.text.decode("utf-8")
                m_row = node.start_point.row + 1

                # 偵測執行期崩潰或未完成代碼危害 (panic!, todo!, unimplemented!)
                if m_name in ("panic", "todo", "unimplemented"):
                    hazard_id = f"hazard:{m_name}@{file_path}:L{m_row}"
                    graph.add_node_rich(
                        node_id=hazard_id,
                        label=f"{m_name}! [未完成實作/執行期中斷]",
                        category="FUNCTION_DEF",
                        scope={"scope_id": current_scope, "file": file_path, "line": m_row},
                        props={"hazard": f"RUST_{m_name.upper()}", "is_blocking": True},
                    )
                    graph.add_edge_rich(
                        caller_func_id,
                        hazard_id,
                        edge_type="CALLS",
                        status="BLOCKED_INVARIANT",
                        detail=f"呼叫了未完成實作或執行期中斷巨集: {m_name}!()",
                    )
                else:
                    # 常規巨集 (如 println!, format!)
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
                        caller_func_id,
                        target_id,
                        edge_type="CALLS",
                        status="VALID",
                        detail="調用標準庫或外部巨集",
                    )

        # 2. 處理常規呼叫 (call_expression)
        if node.type == "call_expression" and caller_func_id:
            fn_target_node = node.child_by_field_name("function")
            if fn_target_node:
                call_name, is_method, target_class = self._resolve_call_target(fn_target_node, current_impl_type)
                call_row = node.start_point.row + 1
                
                # 依作用域查找目標定義
                target_def_id, status, detail = self._lookup_scope(
                    call_name, current_scope, scopes, is_method, target_class
                )

                if not target_def_id:
                    # 外部或未解析呼叫
                    ext_id = f"func:{call_name}@external"
                    if ext_id not in graph.g:
                        graph.add_node_rich(
                            node_id=ext_id,
                            label=f"{call_name} (External/Unresolved)",
                            category="FUNCTION_DEF",
                            scope={"scope_id": "external", "file": file_path, "line": 0},
                            props={"signature": f"{call_name}()", "source_code": ""},
                        )
                    target_def_id = ext_id
                    status = "VALID"
                    detail = "引用全域模組或外部 Crate"

                is_await = ".await" in node.text.decode("utf-8")
                graph.add_edge_rich(
                    caller_func_id,
                    target_def_id,
                    edge_type="CALLS",
                    status=status,
                    detail=detail,
                    flow_type="ASYNC" if is_await else "SYNC",
                )

        # 遞迴遍歷子節點
        for child in node.children:
            self._wire_calls_and_macros(
                child, current_scope, scopes, source, file_path, graph, caller_func_id, current_impl_type
            )

    def _resolve_call_target(self, fn_node: Node, current_impl_type: Optional[str]) -> Tuple[str, bool, Optional[str]]:
        """解析呼叫目標節點 (identifier, scoped_identifier, field_expression)"""
        if fn_node.type == "identifier":
            return fn_node.text.decode("utf-8"), False, None

        if fn_node.type == "scoped_identifier":
            # 例如 Server::new
            return fn_node.text.decode("utf-8"), True, None

        if fn_node.type == "field_expression":
            # 例如 self.bind_socket() 或 s.start()
            val_node = fn_node.child_by_field_name("value")
            field_node = fn_node.child_by_field_name("field")
            if field_node:
                method_name = field_node.text.decode("utf-8")
                val_text = val_node.text.decode("utf-8") if val_node else ""
                if val_text == "self" and current_impl_type:
                    return f"{current_impl_type}::{method_name}", True, current_impl_type
                return method_name, True, None

        return fn_node.text.decode("utf-8"), False, None

    def _lookup_scope(
        self,
        call_name: str,
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        is_method: bool = False,
        target_class: Optional[str] = None,
    ) -> Tuple[Optional[str], str, str]:
        """向上追溯 Scope 堆疊以消解識別碼"""
        curr = current_scope_id
        while curr:
            s_data = scopes.get(curr, {})
            defs = s_data.get("defs", {})

            if call_name in defs:
                return defs[call_name], "VALID", f"作用域可達 (定義於 {curr})"

            if is_method and target_class:
                qualified = f"{target_class}::{call_name}"
                if qualified in defs:
                    return defs[qualified], "VALID", f"結構體關聯方法可達 (定義於 {curr})"

            curr = s_data.get("parent")

        # 若在全域未找到，但屬於同一個結構體 impl 區塊中的方法
        if is_method:
            for s_id, s_data in scopes.items():
                if s_data.get("impl_type") and call_name in s_data.get("defs", {}):
                    return s_data["defs"][call_name], "VALID", f"結構體方法可達 (定義於 {s_id})"

        return None, "UNRESOLVED", "未在此檔案內找到宣告 (外部模組或 Crate)"
