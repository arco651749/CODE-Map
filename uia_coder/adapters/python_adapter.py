from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_python as tspy

from uia_coder.core.base_adapter import BaseUIAGraphBuilder
from uia_coder.core.graph import UIACodeGraph


class PythonUIAGraphBuilder(BaseUIAGraphBuilder):
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

    def parse_and_build(self, source_code: str, file_path: str = "app.py") -> UIACodeGraph:
        tree = self.parser.parse(bytes(source_code, "utf-8"))
        graph = UIACodeGraph(name=f"Graph of {file_path}")

        scopes: Dict[str, Dict[str, Any]] = {
            "scope:global": {
                "id": "scope:global",
                "parent": None,
                "depth": 0,
                "defs": {}
            }
        }

        # 階段 1：收集所有函式宣告、方法宣告與巢狀 Scope
        self._collect_scopes_and_functions(tree.root_node, "scope:global", scopes, source_code, file_path, graph)

        # 階段 2：識別 UI 控制項 (PyQt/Tkinter)、信號槽連接與呼叫點
        self._wire_ui_and_calls(tree.root_node, "scope:global", scopes, source_code, file_path, graph)

        return graph

    def _collect_scopes_and_functions(
        self,
        node: Node,
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        code: str,
        file_path: str,
        graph: UIACodeGraph,
    ):
        next_scope_id = current_scope_id

        if node.type == "function_definition":
            name_node = node.child_by_field_name("name")
            func_name = name_node.text.decode("utf-8") if name_node else "anonymous"
            start_line = node.start_point[0] + 1
            new_scope_id = f"scope:{func_name}@{file_path}:L{start_line}"
            depth = scopes[current_scope_id]["depth"] + 1

            scopes[new_scope_id] = {
                "id": new_scope_id,
                "parent": current_scope_id,
                "depth": depth,
                "defs": {}
            }

            func_node_id = f"func:{func_name}@{file_path}:L{start_line}"
            is_async = (node.children[0].type == "async" if node.children else False)
            params_node = node.child_by_field_name("parameters")
            param_text = params_node.text.decode("utf-8") if params_node else "()"
            full_text = node.text.decode("utf-8")
            sig_text = full_text.split(":")[0].strip() if ":" in full_text else full_text.split("\n")[0].strip()
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

            graph.add_node_rich(
                node_id=func_node_id,
                label=func_name,
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
        graph: UIACodeGraph,
    ):
        next_scope_id = current_scope_id

        if node.type == "function_definition":
            name_node = node.child_by_field_name("name")
            func_name = name_node.text.decode("utf-8") if name_node else "anonymous"
            start_line = node.start_point[0] + 1
            next_scope_id = f"scope:{func_name}@{file_path}:L{start_line}"

        # 1. 偵測 Python UI 控制項賦值 (例如: self.btn_delete = QPushButton("刪除") 或 btn = Button(...))
        if node.type == "assignment":
            left_node = node.child_by_field_name("left")
            right_node = node.child_by_field_name("right")
            if left_node and right_node:
                right_text = right_node.text.decode("utf-8")
                if any(k in right_text for k in ("QPushButton", "Button", "Action", "QAction")):
                    ctrl_name = left_node.text.decode("utf-8").replace("self.", "")
                    line = node.start_point[0] + 1
                    ctrl_id = f"ctrl:{ctrl_name}@{file_path}:L{line}"
                    graph.add_node_rich(
                        node_id=ctrl_id,
                        label=f"#{ctrl_name}",
                        category="UI_CONTROL",
                        scope={"scope_id": next_scope_id, "file": file_path, "line": line},
                        props={"ui_type": "Button" if "btn" in ctrl_name.lower() or "button" in right_text.lower() else "Control"}
                    )

        # 2. 偵測信號槽連接: btn.clicked.connect(handler) 或 btn.clicked.connect(self.handler)
        if node.type == "call":
            func_node = node.child_by_field_name("function")
            if func_node and func_node.type == "attribute":
                attr_name = func_node.child_by_field_name("attribute")
                if attr_name and attr_name.text.decode("utf-8") == "connect":
                    self._handle_pyqt_connect(node, func_node, next_scope_id, scopes, file_path, graph)

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

    def _handle_pyqt_connect(
        self,
        call_node: Node,
        func_attr_node: Node,
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        file_path: str,
        graph: UIACodeGraph,
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
        graph: UIACodeGraph,
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
            for s_id, s_data in scopes.items():
                if callee_name in s_data.get("defs", {}):
                    isolated_def = s_data["defs"][callee_name]
                    isolated_scope_id = s_id
                    break

            if isolated_def:
                target_node_id = isolated_def["node_id"]
                if caller_id in graph.g and target_node_id in graph.g:
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

    def _find_enclosing_node_id(self, scope_id: str, graph: UIACodeGraph) -> Optional[str]:
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
