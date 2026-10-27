from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_python as tspy

from code_map.core.base_adapter import BaseCodeMapBuilder
from code_map.core.graph import CodeMapGraph


class PythonCodeMapBuilder(BaseCodeMapBuilder):
    """
    基於 Tree-sitter 的 Python 語意控制樹建構器
    追蹤 Python 函式作用域、PyQt/PySide 信號槽、Tkinter 綁定與主執行緒阻塞危害 (time.sleep)。
    """

    @property
    def supported_extensions(self) -> Set[str]:
        return {".py"}

    @property
    def language_name(self) -> str:
        return "Python"

    def __init__(self):
        self.language = Language(tspy.language())
        self.parser = Parser(self.language)

    def parse_and_build(self, source_code: str, file_path: str = "app.py") -> CodeMapGraph:
        tree = self.parser.parse(bytes(source_code, "utf-8"))
        graph = CodeMapGraph(name=f"Graph of {file_path}")

        scopes: Dict[str, Dict[str, Any]] = {
            "scope:global": {
                "id": "scope:global",
                "parent": None,
                "depth": 0,
                "defs": {}
            }
        }

        # 檢測原始碼是否引入 UI 框架特徵 (避免純後端專案被誤判為 UI 應用)
        ui_keywords = ("textual", "PyQt", "PySide", "tkinter", "ttk", "wx", "kivy", "flet", "customtkinter")
        self._has_ui_import = any(kw in source_code for kw in ui_keywords)

        # 階段 1：收集所有函式宣告、方法宣告與巢狀 Scope
        self._collect_scopes_and_functions(tree.root_node, "scope:global", scopes, source_code, file_path, graph)

        # 階段 2：識別 UI 控制項 (PyQt/Tkinter)、信號槽連接與呼叫點
        self._wire_ui_and_calls(tree.root_node, "scope:global", scopes, source_code, file_path, graph)

        # 階段 3：若包含 main() 函式，自動註冊 CLI 程式入口錨點
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
                props={"ui_type": "CLI Entry", "source_code": "def main():", "line_start": m_line, "line_end": m_line}
            )
            evt_id = f"event:CLI.run@{file_path}:L{m_line}"
            graph.add_node_rich(
                node_id=evt_id,
                label="run()",
                category="EVENT_BINDING",
                scope={"scope_id": "scope:global", "file": file_path, "line": m_line},
                props={"event_name": "run", "source_code": "if __name__ == '__main__': main()", "line_start": m_line, "line_end": m_line}
            )
            graph.add_edge_rich(
                source=entry_id,
                target=evt_id,
                edge_type="WIRES_TO",
                status="VALID",
                detail="CLI 命令列入口執行"
            )
            graph.add_edge_rich(
                source=evt_id,
                target=main_nid,
                edge_type="TRIGGERS",
                status="VALID",
                detail="觸發 main() 流程"
            )

        return graph

    def _collect_scopes_and_functions(
        self,
        node: Node,
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        code: str,
        file_path: str,
        graph: CodeMapGraph,
    ):
        next_scope_id = current_scope_id

        if node.type == "class_definition":
            name_node = node.child_by_field_name("name")
            class_name = name_node.text.decode("utf-8") if name_node else "AnonymousClass"
            start_line = node.start_point[0] + 1
            new_scope_id = f"scope:{class_name}@{file_path}:L{start_line}"
            depth = scopes[current_scope_id]["depth"] + 1

            scopes[new_scope_id] = {
                "id": new_scope_id,
                "parent": current_scope_id,
                "depth": depth,
                "defs": {},
                "class_name": class_name,
            }
            # 同時在父作用域註冊該類別建構子
            class_node_id = f"class:{class_name}@{file_path}:L{start_line}"
            scopes[current_scope_id]["defs"][class_name] = {
                "node_id": class_node_id,
                "declared_scope": current_scope_id,
                "inner_scope": new_scope_id,
                "line": start_line,
                "is_async": False,
                "signature": f"class {class_name}",
            }
            next_scope_id = new_scope_id

        elif node.type == "function_definition":
            name_node = node.child_by_field_name("name")
            func_name = name_node.text.decode("utf-8") if name_node else "anonymous"
            start_line = node.start_point[0] + 1
            
            # 若身處類別內部，標註為 Class.Method
            cls_name = scopes[current_scope_id].get("class_name")
            full_label = f"{cls_name}.{func_name}" if cls_name else func_name

            new_scope_id = f"scope:{full_label}@{file_path}:L{start_line}"
            depth = scopes[current_scope_id]["depth"] + 1

            scopes[new_scope_id] = {
                "id": new_scope_id,
                "parent": current_scope_id,
                "depth": depth,
                "defs": {},
                "class_name": cls_name,
            }

            func_node_id = f"func:{full_label}@{file_path}:L{start_line}"
            is_async = (node.children[0].type == "async" if node.children else False)
            params_node = node.child_by_field_name("parameters")
            param_text = params_node.text.decode("utf-8") if params_node else "()"
            full_text = node.text.decode("utf-8")
            body_node = node.child_by_field_name("body")
            if body_node:
                header_bytes = node.text[: body_node.start_byte - node.start_byte]
                sig_text = " ".join(header_bytes.decode("utf-8", errors="replace").strip().rstrip(":").split())
            else:
                sig_text = " ".join(full_text.split("\n")[0].strip().rstrip(":").split())
            end_line = node.end_point[0] + 1

            scopes[current_scope_id]["defs"][func_name] = {
                "node_id": func_node_id,
                "declared_scope": current_scope_id,
                "inner_scope": new_scope_id,
                "line": start_line,
                "is_async": is_async,
                "signature": sig_text,
                "parameters": param_text,
            }
            if cls_name:
                scopes[current_scope_id]["defs"][full_label] = scopes[current_scope_id]["defs"][func_name]

            graph.add_node_rich(
                node_id=func_node_id,
                label=full_label,
                category="FUNCTION_DEF",
                scope={"scope_id": current_scope_id, "inner_scope": new_scope_id, "depth": depth - 1, "file": file_path, "line": start_line},
                props={
                    "is_async": is_async,
                    "inner_scope": new_scope_id,
                    "signature": sig_text,
                    "parameters": param_text,
                    "line_start": start_line,
                    "line_end": end_line,
                    "line_count": end_line - start_line + 1,
                    "source_code": full_text,
                    "executable_fingerprint": self.compute_executable_fingerprint(node),
                }
            )

            next_scope_id = new_scope_id

        for child in node.children:
            self._collect_scopes_and_functions(child, next_scope_id, scopes, code, file_path, graph)

    def _wire_ui_and_calls(
        self,
        node: Node,
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        code: str,
        file_path: str,
        graph: CodeMapGraph,
    ):
        next_scope_id = current_scope_id

        if node.type == "class_definition":
            name_node = node.child_by_field_name("name")
            class_name = name_node.text.decode("utf-8") if name_node else "AnonymousClass"
            start_line = node.start_point[0] + 1
            next_scope_id = f"scope:{class_name}@{file_path}:L{start_line}"

        elif node.type in ("function_definition", "decorated_definition"):
            func_node = node if node.type == "function_definition" else node.child_by_field_name("definition")
            if func_node and func_node.type == "function_definition":
                name_node = func_node.child_by_field_name("name")
                func_name = name_node.text.decode("utf-8") if name_node else "anonymous"
                start_line = func_node.start_point[0] + 1
                cls_name = scopes.get(current_scope_id, {}).get("class_name")
                full_label = f"{cls_name}.{func_name}" if cls_name else func_name
                next_scope_id = f"scope:{full_label}@{file_path}:L{start_line}"
                
                # 支援 Textual @on(...) 裝飾器與 on_xxx_yyy 事件約定
                self._handle_textual_event_bindings(node, func_name, full_label, next_scope_id, scopes, file_path, graph)

        # 1. 偵測 Python UI 控制項賦值 (嚴格要求右側為呼叫表達式，且調用 GUI 類別)
        if node.type == "assignment":
            left_node = node.child_by_field_name("left")
            right_node = node.child_by_field_name("right")
            if left_node and right_node and right_node.type == "call":
                fn_child = right_node.child_by_field_name("function")
                callee_text = fn_child.text.decode("utf-8") if fn_child else ""
                widget_types = ("QPushButton", "QAction", "QWidget", "QMainWindow", "Button", "tk.Button", "ttk.Button")
                if any(w in callee_text for w in widget_types):
                    ctrl_name = left_node.text.decode("utf-8").replace("self.", "")
                    line = node.start_point[0] + 1
                    ctrl_id = f"ctrl:{ctrl_name}@{file_path}:L{line}"
                    graph.add_node_rich(
                        node_id=ctrl_id,
                        label=f"#{ctrl_name}",
                        category="UI_CONTROL",
                        scope={"scope_id": next_scope_id, "file": file_path, "line": line},
                        props={
                            "ui_type": "Button" if "btn" in ctrl_name.lower() or "button" in callee_text.lower() else "Control",
                            "source_code": node.text.decode("utf-8"),
                            "line_start": line,
                            "line_end": node.end_point[0] + 1,
                        }
                    )

        # 2. 偵測呼叫點 (包含屬性方法調用與信號槽連接)
        if node.type == "call":
            func_node = node.child_by_field_name("function")
            if func_node:
                line = node.start_point[0] + 1
                parent_node = self._find_enclosing_node_id(next_scope_id, graph)

                if func_node.type == "attribute":
                    attr_name = func_node.child_by_field_name("attribute")
                    attr_text = attr_name.text.decode("utf-8") if attr_name else ""
                    if attr_text == "connect":
                        self._handle_pyqt_connect(node, func_node, next_scope_id, scopes, file_path, graph)
                    elif attr_text not in ("append", "extend", "get", "split", "strip", "join", "format", "replace", "startswith", "endswith", "items", "keys", "values", "pop", "insert", "write", "read"):
                        # 方法調用 (例如: self.get_git_diff() 或 analyzer.analyze())
                        self._link_handler_with_reachability(
                            caller_id=parent_node or f"scope:{next_scope_id}",
                            callee_name=attr_text,
                            call_scope_id=next_scope_id,
                            scopes=scopes,
                            file_path=file_path,
                            line=line,
                            graph=graph,
                            is_direct_trigger=False,
                        )

        # 3. 偵測呼叫點與危害 (time.sleep, 等)
        if node.type == "call":
            func_node = node.child_by_field_name("function")
            if func_node:
                callee_name = func_node.text.decode("utf-8")
                line = node.start_point[0] + 1

                # 危害檢查 (例如 time.sleep 阻塞 UI 主執行緒)
                if "time.sleep" in callee_name or callee_name == "sleep":
                    hazard_id = f"hazard:sleep@{file_path}:L{line}"
                    graph.add_node_rich(
                        node_id=hazard_id,
                        label="time.sleep()",
                        category="INVARIANT_GUARD",
                        scope={"scope_id": next_scope_id, "file": file_path, "line": line},
                        props={"is_blocking": True, "hazard": "SYNC_BLOCKING_UI"}
                    )
                    parent_node = self._find_enclosing_node_id(next_scope_id, graph)
                    if parent_node:
                        graph.add_edge_rich(
                            source=parent_node,
                            target=hazard_id,
                            edge_type="CALLS",
                            status="BLOCKED_INVARIANT",
                            detail="呼叫了同步阻塞之 time.sleep()，將凍結 UI 介面"
                        )
                elif func_node.type == "identifier":
                    pure_name = func_node.text.decode("utf-8")
                    if pure_name not in ("print", "len", "range", "isinstance", "int", "str"):
                        parent_node = self._find_enclosing_node_id(next_scope_id, graph)
                        self._link_handler_with_reachability(
                            caller_id=parent_node or f"scope:{next_scope_id}",
                            callee_name=pure_name,
                            call_scope_id=next_scope_id,
                            scopes=scopes,
                            file_path=file_path,
                            line=line,
                            graph=graph,
                            is_direct_trigger=False,
                        )

        for child in node.children:
            self._wire_ui_and_calls(child, next_scope_id, scopes, code, file_path, graph)

    def _handle_textual_event_bindings(
        self,
        node: Node,
        func_name: str,
        full_label: str,
        scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        file_path: str,
        graph: CodeMapGraph,
    ):
        """解析 Textual 的 @on(...) 裝飾器與 on_button_pressed 等約定事件處理常式"""
        line = node.start_point[0] + 1
        ctrl_name = None
        event_name = None
        
        # 1. 檢查裝飾器: @on(Button.Pressed, "#btn_id") 或 @work
        if node.type == "decorated_definition":
            for child in node.children:
                if child.type == "decorator":
                    dec_text = child.text.decode("utf-8")
                    if "@on" in dec_text:
                        # 嘗試抽取 selector 與 event
                        call_node = None
                        for c in child.children:
                            if c.type == "call":
                                call_node = c
                                break
                        if call_node:
                            args_node = call_node.child_by_field_name("arguments")
                            if args_node:
                                for arg in args_node.children:
                                    arg_str = arg.text.decode("utf-8").strip("'\"")
                                    if arg_str.startswith("#") or arg_str.startswith("."):
                                        ctrl_name = arg_str.lstrip("#.")
                                    elif "Pressed" in arg_str or "Click" in arg_str or "Key" in arg_str or "Changed" in arg_str or "Selected" in arg_str:
                                        event_name = arg_str.split(".")[-1]
                    elif "@work" in dec_text:
                        # 標註該方法為非同步背景 Worker
                        func_nid = f"func:{full_label}@{file_path}:L{line}"
                        if func_nid in graph.g:
                            graph.g.nodes[func_nid]["props"]["is_worker"] = True

        # 2. 檢查命名約定: on_button_pressed, on_key, on_mount, on_click
        if not event_name and func_name.startswith("on_") and getattr(self, "_has_ui_import", False):
            parts = func_name.split("_")
            if len(parts) >= 3:
                # 例如 on_button_pressed -> ctrl=button, event=pressed
                ctrl_name = ctrl_name or parts[1]
                event_name = "_".join(parts[2:])
            elif len(parts) == 2:
                # 例如 on_key, on_mount
                ctrl_name = ctrl_name or "app"
                event_name = parts[1]

        if event_name:
            clean_ctrl = ctrl_name or "control"
            ctrl_id = f"ctrl:{clean_ctrl}@{file_path}:L{line}"
            existing_ctrl = None
            clean_label = f"#{clean_ctrl}"
            
            for n, d in graph.g.nodes(data=True):
                if d.get("category") == "UI_CONTROL" and d.get("label") == clean_label:
                    existing_ctrl = n
                    break
                    
            if not existing_ctrl:
                graph.add_node_rich(
                    node_id=ctrl_id,
                    label=clean_label,
                    category="UI_CONTROL",
                    scope={"scope_id": scope_id, "file": file_path, "line": line},
                    props={"ui_type": "Button" if "button" in clean_ctrl.lower() or "btn" in clean_ctrl.lower() else "Widget"}
                )
                active_ctrl = ctrl_id
            else:
                active_ctrl = existing_ctrl
                
            event_nid = f"event:{clean_ctrl}.{event_name}@{file_path}:L{line}"
            graph.add_node_rich(
                node_id=event_nid,
                label=f"on('{event_name}')",
                category="EVENT_BINDING",
                scope={"scope_id": scope_id, "file": file_path, "line": line},
                props={"event_name": event_name}
            )
            graph.add_edge_rich(
                source=active_ctrl,
                target=event_nid,
                edge_type="WIRES_TO",
                flow_type="SYNC",
                status="VALID",
                detail="Textual 事件綁定"
            )
            # 接線至處理方法
            func_nid = f"func:{full_label}@{file_path}:L{line}"
            if func_nid in graph.g:
                graph.add_edge_rich(
                    source=event_nid,
                    target=func_nid,
                    edge_type="TRIGGERS",
                    flow_type="SYNC",
                    status="VALID",
                    detail="Textual 事件處理常式"
                )

    def _handle_pyqt_connect(
        self,
        call_node: Node,
        func_attr_node: Node,
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        file_path: str,
        graph: CodeMapGraph,
    ):
        # 拆解 btn.clicked.connect(...)
        # obj_node 為 btn.clicked
        obj_node = func_attr_node.child_by_field_name("object")
        signal_name = "clicked"
        ctrl_name = "element"

        if obj_node and obj_node.type == "attribute":
            sig_attr = obj_node.child_by_field_name("attribute")
            if sig_attr:
                signal_name = sig_attr.text.decode("utf-8")
            base_obj = obj_node.child_by_field_name("object")
            if base_obj:
                ctrl_name = base_obj.text.decode("utf-8").replace("self.", "")
        elif obj_node:
            ctrl_name = obj_node.text.decode("utf-8").replace("self.", "")

        line = call_node.start_point[0] + 1
        ctrl_id = None

        for n, d in graph.g.nodes(data=True):
            if d.get("category") == "UI_CONTROL" and (ctrl_name in n or ctrl_name in d.get("label", "")):
                ctrl_id = n
                break

        if not ctrl_id:
            ctrl_id = f"ctrl:{ctrl_name}@{file_path}:L{line}"
            graph.add_node_rich(
                node_id=ctrl_id,
                label=f"#{ctrl_name}",
                category="UI_CONTROL",
                scope={"scope_id": current_scope_id, "file": file_path, "line": line},
                props={"ui_type": "Button" if "btn" in ctrl_name.lower() else "Control"}
            )

        event_node_id = f"event:{ctrl_name}.{signal_name}@{file_path}:L{line}"
        graph.add_node_rich(
            node_id=event_node_id,
            label=f"{signal_name}.connect",
            category="EVENT_BINDING",
            scope={"scope_id": current_scope_id, "file": file_path, "line": line},
            props={"signal": signal_name}
        )

        graph.add_edge_rich(
            source=ctrl_id,
            target=event_node_id,
            edge_type="WIRES_TO",
            flow_type="SYNC",
            status="VALID",
            detail=f"連接 {signal_name} 信號"
        )

        # 檢查參數 (槽函式)
        args_node = call_node.child_by_field_name("arguments")
        if not args_node or args_node.child_count < 2:
            return

        arg_slot = args_node.children[1]  # [0] 是 '('
        slot_text = arg_slot.text.decode("utf-8")
        handler_name = slot_text.split(".")[-1]

        self._link_handler_with_reachability(
            caller_id=event_node_id,
            callee_name=handler_name,
            call_scope_id=current_scope_id,
            scopes=scopes,
            file_path=file_path,
            line=line,
            graph=graph,
            is_direct_trigger=True,
        )

    def _link_handler_with_reachability(
        self,
        caller_id: str,
        callee_name: str,
        call_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        file_path: str,
        line: int,
        graph: CodeMapGraph,
        is_direct_trigger: bool = False,
        flow_type: str = "SYNC",
    ):
        found_def = None
        declaring_scope_id = None

        curr = call_scope_id
        while curr:
            if callee_name in scopes.get(curr, {}).get("defs", {}):
                found_def = scopes[curr]["defs"][callee_name]
                declaring_scope_id = curr
                break
            curr = scopes.get(curr, {}).get("parent")

        edge_type = "TRIGGERS" if is_direct_trigger else "CALLS"

        if found_def:
            target_node_id = found_def["node_id"]
            if caller_id in graph.g and target_node_id in graph.g:
                graph.add_edge_rich(
                    source=caller_id,
                    target=target_node_id,
                    edge_type=edge_type,
                    flow_type=flow_type,
                    status="VALID",
                    detail=f"作用域可達 (定義於 {declaring_scope_id})"
                )
        else:
            isolated_def = None
            isolated_scope_id = None
            is_class_method = False
            for s_id, s_data in scopes.items():
                if callee_name in s_data.get("defs", {}):
                    isolated_def = s_data["defs"][callee_name]
                    isolated_scope_id = s_id
                    if s_data.get("class_name"):
                        is_class_method = True
                    break

            if isolated_def:
                target_node_id = isolated_def["node_id"]
                if caller_id in graph.g and target_node_id in graph.g:
                    if is_class_method:
                        graph.add_edge_rich(
                            source=caller_id,
                            target=target_node_id,
                            edge_type=edge_type,
                            flow_type=flow_type,
                            status="VALID",
                            detail=f"呼叫類別實例方法 ({isolated_scope_id})"
                        )
                    else:
                        graph.add_edge_rich(
                            source=caller_id,
                            target=target_node_id,
                            edge_type=edge_type,
                            flow_type=flow_type,
                            status="BLOCKED_SCOPE",
                            detail=f"💥 作用域阻隔: 函式 '{callee_name}' 被深鎖在內部閉包 ({isolated_scope_id})，外部無法調用！"
                        )
            else:
                unresolved_id = f"func:{callee_name}@external"
                if unresolved_id not in graph.g:
                    graph.add_node_rich(
                        node_id=unresolved_id,
                        label=f"{callee_name} (External/Unresolved)",
                        category="FUNCTION_DEF",
                        scope={"scope_id": "external", "file": "external", "line": 0},
                        props={"is_external": True}
                    )
                if caller_id in graph.g:
                    graph.add_edge_rich(
                        source=caller_id,
                        target=unresolved_id,
                        edge_type=edge_type,
                        flow_type=flow_type,
                        status="VALID",
                        detail="引用全域或模組外部函式"
                    )

    def _find_enclosing_node_id(self, scope_id: str, graph: CodeMapGraph) -> Optional[str]:
        for n, d in graph.g.nodes(data=True):
            props = d.get("props", {})
            scope = d.get("scope", {})
            if props.get("inner_scope") == scope_id or scope.get("inner_scope") == scope_id:
                return n

        for n, d in graph.g.nodes(data=True):
            if d.get("category") == "EVENT_BINDING" and scope_id in d.get("scope", {}).get("scope_id", ""):
                return n

        anchors = graph.get_ui_anchors()
        return anchors[0] if anchors else None
