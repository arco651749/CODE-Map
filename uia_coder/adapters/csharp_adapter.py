from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_c_sharp as tscs

from uia_coder.core.base_adapter import BaseUIAGraphBuilder
from uia_coder.core.graph import UIACodeGraph


class CSharpUIAGraphBuilder(BaseUIAGraphBuilder):
    """
    基於 Tree-sitter 的 C# 語意控制樹建構器
    - 追蹤命名空間、類別方法 (Class.Method) 與 UI 事件綁定 (btn.Click += OnClick)
    - 識別 WPF/WinUI 控制項錨點與 CLI Main 進入點
    - 偵測 Thread.Sleep() 同步凍結與 NotImplementedException 危害 (Hazards)
    """

    @property
    def supported_extensions(self) -> Set[str]:
        return {".cs"}

    @property
    def language_name(self) -> str:
        return "C#"

    def __init__(self):
        self.language = Language(tscs.language())
        self.parser = Parser(self.language)

    def parse_and_build(self, source_code: str, file_path: str = "Program.cs") -> UIACodeGraph:
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

        # 階段 1：收集類別宣告與方法定義
        self._collect_classes_and_methods(
            tree.root_node, "scope:global", scopes, source_code, file_path, graph
        )

        # 階段 2：收集 UI 事件綁定 (如 btn.Click += OnClick) 與呼叫接線
        self._wire_events_and_calls(
            tree.root_node, "scope:global", scopes, source_code, file_path, graph
        )

        # 階段 3：如果沒有 UI 控制項錨點，但存在 Main() 函式，自動註冊 CLI 程式入口
        if not graph.get_ui_anchors():
            main_nodes = [
                n for n, d in graph.g.nodes(data=True)
                if d.get("label") == "Main" or d.get("label", "").endswith(".Main")
            ]
            if main_nodes:
                main_nid = main_nodes[0]
                m_scope = graph.g.nodes[main_nid].get("scope", {})
                m_line = m_scope.get("line", 1)
                entry_id = f"ctrl:CLI:Main@{file_path}:L{m_line}"
                graph.add_node_rich(
                    node_id=entry_id,
                    label="#CLI: Main",
                    category="UI_CONTROL",
                    scope={"scope_id": "scope:global", "file": file_path, "line": m_line},
                    props={
                        "ui_type": "CLI Entry",
                        "source_code": "public static void Main() { ... }",
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
                    detail="CLI 觸發 Main() 進入點",
                )

        return graph

    def _collect_classes_and_methods(
        self,
        node: Node,
        current_scope: str,
        scopes: Dict[str, Dict[str, Any]],
        source: str,
        file_path: str,
        graph: UIACodeGraph,
        current_class: Optional[str] = None,
    ):
        if node.type in ("class_declaration", "struct_declaration", "record_declaration"):
            name_node = node.child_by_field_name("name")
            class_name = name_node.text.decode("utf-8") if name_node else "AnonymousClass"
            class_scope_id = f"scope:class:{class_name}"
            scopes[class_scope_id] = {
                "id": class_scope_id,
                "parent": current_scope,
                "depth": scopes[current_scope]["depth"] + 1,
                "defs": {},
                "class_name": class_name,
            }
            body = node.child_by_field_name("body")
            if body:
                for child in body.children:
                    self._collect_classes_and_methods(
                        child, class_scope_id, scopes, source, file_path, graph, current_class=class_name
                    )
            return

        if node.type == "method_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                raw_name = name_node.text.decode("utf-8")
                fn_name = f"{current_class}.{raw_name}" if current_class else raw_name
                start_row = node.start_point.row + 1
                end_row = node.end_point.row + 1
                node_id = f"func:{fn_name}@{file_path}:L{start_row}"

                source_code = source[node.start_byte : node.end_byte]
                params_node = node.child_by_field_name("parameters")
                params = params_node.text.decode("utf-8") if params_node else "()"
                sig = f"{fn_name}{params}"

                scopes[current_scope]["defs"][fn_name] = node_id
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
                        "class_name": current_class or "",
                        "raw_name": raw_name,
                    },
                )

                inner_scope_id = f"scope:fn:{fn_name}@{start_row}"
                scopes[inner_scope_id] = {
                    "id": inner_scope_id,
                    "parent": current_scope,
                    "depth": scopes[current_scope]["depth"] + 1,
                    "defs": {},
                    "class_name": current_class,
                }

                body = node.child_by_field_name("body")
                if body:
                    for child in body.children:
                        self._collect_classes_and_methods(
                            child, inner_scope_id, scopes, source, file_path, graph, current_class
                        )
                return

        for child in node.children:
            self._collect_classes_and_methods(
                child, current_scope, scopes, source, file_path, graph, current_class
            )

    def _wire_events_and_calls(
        self,
        node: Node,
        current_scope: str,
        scopes: Dict[str, Dict[str, Any]],
        source: str,
        file_path: str,
        graph: UIACodeGraph,
        caller_func_id: Optional[str] = None,
        current_class: Optional[str] = None,
    ):
        if node.type in ("class_declaration", "struct_declaration", "record_declaration"):
            name_node = node.child_by_field_name("name")
            class_name = name_node.text.decode("utf-8") if name_node else current_class
            class_scope_id = f"scope:class:{class_name}" if class_name else current_scope
            body = node.child_by_field_name("body")
            if body:
                for child in body.children:
                    self._wire_events_and_calls(
                        child, class_scope_id, scopes, source, file_path, graph, caller_func_id, class_name
                    )
            return

        if node.type == "method_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                raw_name = name_node.text.decode("utf-8")
                fn_name = f"{current_class}.{raw_name}" if current_class else raw_name
                start_row = node.start_point.row + 1
                curr_func_id = f"func:{fn_name}@{file_path}:L{start_row}"
                inner_scope_id = f"scope:fn:{fn_name}@{start_row}"

                body = node.child_by_field_name("body")
                if body:
                    for child in body.children:
                        self._wire_events_and_calls(
                            child, inner_scope_id, scopes, source, file_path, graph, curr_func_id, current_class
                        )
                return

        # 1. 偵測 WPF / WinUI 事件綁定 (例如 btnSubmit.Click += OnSubmitClicked)
        if node.type == "assignment_expression":
            left_node = node.child_by_field_name("left")
            right_node = node.child_by_field_name("right")
            has_plus_assign = any(c.type == "+=" for c in node.children)

            if has_plus_assign and left_node and right_node:
                left_text = left_node.text.decode("utf-8")
                right_text = right_node.text.decode("utf-8")
                line_no = node.start_point.row + 1

                if "." in left_text:
                    parts = left_text.split(".")
                    ctrl_name = parts[-2]
                    evt_name = parts[-1]

                    ctrl_id = f"ctrl:#{ctrl_name}@{file_path}:L{line_no}"
                    if ctrl_id not in graph.g:
                        graph.add_node_rich(
                            node_id=ctrl_id,
                            label=f"#{ctrl_name}",
                            category="UI_CONTROL",
                            scope={"scope_id": current_scope, "file": file_path, "line": line_no},
                            props={
                                "ui_type": "Button / UI Control",
                                "source_code": node.text.decode("utf-8"),
                                "line_start": line_no,
                                "line_end": line_no,
                            },
                        )

                    evt_id = f"event:{ctrl_name}.{evt_name}@{file_path}:L{line_no}"
                    graph.add_node_rich(
                        node_id=evt_id,
                        label=f"{evt_name}()",
                        category="EVENT_BINDING",
                        scope={"scope_id": current_scope, "file": file_path, "line": line_no},
                        props={"event": evt_name},
                    )
                    graph.add_edge_rich(ctrl_id, evt_id, edge_type="WIRES_TO", status="VALID")

                    # 查詢目標處理常式
                    handler_name = right_text.split(".")[-1]
                    target_id, status, detail = self._lookup_cs_scope(
                        handler_name, current_scope, scopes, current_class
                    )
                    if target_id:
                        graph.add_edge_rich(
                            evt_id,
                            target_id,
                            edge_type="TRIGGERS",
                            status=status,
                            detail=f"C# 事件訂閱觸發: {detail}",
                        )

        # 2. 偵測未完成例外 (throw new NotImplementedException)
        if node.type == "throw_statement" and caller_func_id:
            throw_text = node.text.decode("utf-8")
            line_no = node.start_point.row + 1
            if "NotImplementedException" in throw_text:
                hazard_id = f"hazard:NotImplementedException@{file_path}:L{line_no}"
                graph.add_node_rich(
                    node_id=hazard_id,
                    label="NotImplementedException [未完成實作危害]",
                    category="FUNCTION_DEF",
                    scope={"scope_id": current_scope, "file": file_path, "line": line_no},
                    props={"hazard": "CSHARP_NOT_IMPLEMENTED", "is_blocking": True},
                )
                graph.add_edge_rich(
                    caller_func_id,
                    hazard_id,
                    edge_type="CALLS",
                    status="BLOCKED_INVARIANT",
                    detail="拋出了未完成實作例外: NotImplementedException",
                )
                return

        # 3. 偵測呼叫運算式 (invocation_expression)
        if node.type == "invocation_expression" and caller_func_id:
            fn_node = node.child_by_field_name("function")
            if fn_node:
                call_text = fn_node.text.decode("utf-8")
                line_no = node.start_point.row + 1

                # 偵測 Thread.Sleep 同步阻塞
                if "Thread.Sleep" in call_text:
                    hazard_id = f"hazard:Thread.Sleep@{file_path}:L{line_no}"
                    graph.add_node_rich(
                        node_id=hazard_id,
                        label="Thread.Sleep() [同步休眠/UI凍結]",
                        category="FUNCTION_DEF",
                        scope={"scope_id": current_scope, "file": file_path, "line": line_no},
                        props={"hazard": "CSHARP_THREAD_SLEEP", "is_blocking": True},
                    )
                    graph.add_edge_rich(
                        caller_func_id,
                        hazard_id,
                        edge_type="CALLS",
                        status="BLOCKED_INVARIANT",
                        detail="呼叫了 Thread.Sleep() 同步阻塞 UI 執行緒",
                    )
                    return

                # 常規呼叫消解
                method_name = call_text.split(".")[-1]
                target_id, status, detail = self._lookup_cs_scope(
                    method_name, current_scope, scopes, current_class
                )

                if not target_id:
                    ext_id = f"func:{call_text}@external"
                    if ext_id not in graph.g:
                        graph.add_node_rich(
                            node_id=ext_id,
                            label=f"{call_text} (External/BCL)",
                            category="FUNCTION_DEF",
                            scope={"scope_id": "external", "file": file_path, "line": 0},
                            props={"signature": f"{call_text}()", "source_code": ""},
                        )
                    target_id = ext_id
                    status = "VALID"
                    detail = "引用 .NET BCL 或外部組件"

                graph.add_edge_rich(
                    caller_func_id,
                    target_id,
                    edge_type="CALLS",
                    status=status,
                    detail=detail,
                )

        for child in node.children:
            self._wire_events_and_calls(
                child, current_scope, scopes, source, file_path, graph, caller_func_id, current_class
            )

    def _lookup_cs_scope(
        self,
        name: str,
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        current_class: Optional[str],
    ) -> Tuple[Optional[str], str, str]:
        curr = current_scope_id
        while curr:
            defs = scopes.get(curr, {}).get("defs", {})
            if name in defs:
                return defs[name], "VALID", f"作用域可達 (定義於 {curr})"

            if current_class:
                qualified = f"{current_class}.{name}"
                if qualified in defs:
                    return defs[qualified], "VALID", f"類別方法可達 (定義於 {curr})"

            curr = scopes.get(curr, {}).get("parent")

        # 遍歷所有類別 scope 查找
        for s_id, s_data in scopes.items():
            if name in s_data.get("defs", {}):
                return s_data["defs"][name], "VALID", f"類別成員可達 (定義於 {s_id})"

        return None, "UNRESOLVED", "未在當前檔案內找到宣告 (外部依賴或基底類別)"
