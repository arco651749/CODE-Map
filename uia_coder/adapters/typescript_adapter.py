from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_typescript as tsts

from uia_coder.core.base_adapter import BaseUIAGraphBuilder
from uia_coder.core.graph import UIACodeGraph


class TypeScriptUIAGraphBuilder(BaseUIAGraphBuilder):
    """
    基於 Tree-sitter 的 TypeScript / TSX 語意控制樹建構器
    支援型別化函式作用域、React JSX 標籤 (<button onClick={...}>) 與 Promise.all 並聯偵測。
    """

    @property
    def supported_extensions(self) -> Set[str]:
        return {".ts", ".tsx"}

    @property
    def language_name(self) -> str:
        return "TypeScript"

    def __init__(self):
        self.ts_lang = Language(tsts.language_typescript())
        self.tsx_lang = Language(tsts.language_tsx())
        self.ts_parser = Parser(self.ts_lang)
        self.tsx_parser = Parser(self.tsx_lang)

    def parse_and_build(self, source_code: str, file_path: str = "app.ts") -> UIACodeGraph:
        is_tsx = file_path.endswith(".tsx") or "<" in source_code
        parser = self.tsx_parser if is_tsx else self.ts_parser
        tree = parser.parse(bytes(source_code, "utf-8"))
        graph = UIACodeGraph(name=f"Graph of {file_path}")

        scopes: Dict[str, Dict[str, Any]] = {
            "scope:global": {
                "id": "scope:global",
                "parent": None,
                "depth": 0,
                "defs": {}
            }
        }

        self._collect_scopes_and_functions(tree.root_node, "scope:global", scopes, source_code, file_path, graph)
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

        if node.type in ("function_declaration", "generator_function_declaration"):
            func_name_node = node.child_by_field_name("name")
            func_name = func_name_node.text.decode("utf-8") if func_name_node else "anonymous"
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
            is_async = (b"async" in node.children[0].text if node.children else False)

            scopes[current_scope_id]["defs"][func_name] = {
                "node_id": func_node_id,
                "declared_scope": current_scope_id,
                "inner_scope": new_scope_id,
                "line": start_line,
                "is_async": is_async,
            }

            graph.add_node_rich(
                node_id=func_node_id,
                label=func_name,
                category="FUNCTION_DEF",
                scope={"scope_id": current_scope_id, "inner_scope": new_scope_id, "depth": depth - 1, "file": file_path, "line": start_line},
                props={"is_async": is_async, "inner_scope": new_scope_id}
            )

            next_scope_id = new_scope_id

        elif node.type in ("arrow_function", "function_expression"):
            start_line = node.start_point[0] + 1
            new_scope_id = f"scope:arrow@{file_path}:L{start_line}"
            depth = scopes[current_scope_id]["depth"] + 1
            scopes[new_scope_id] = {
                "id": new_scope_id,
                "parent": current_scope_id,
                "depth": depth,
                "defs": {}
            }
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

        if node.type in ("function_declaration", "generator_function_declaration"):
            func_name_node = node.child_by_field_name("name")
            func_name = func_name_node.text.decode("utf-8") if func_name_node else "anonymous"
            start_line = node.start_point[0] + 1
            next_scope_id = f"scope:{func_name}@{file_path}:L{start_line}"
        elif node.type in ("arrow_function", "function_expression"):
            start_line = node.start_point[0] + 1
            next_scope_id = f"scope:arrow@{file_path}:L{start_line}"

        # 1. 偵測 React TSX JSX 元素: <button onClick={handleDelete}>
        if node.type == "jsx_element" or node.type == "jsx_self_closing_element":
            self._handle_jsx_element(node, next_scope_id, scopes, file_path, graph)

        # 2. 偵測 DOM 建立 (document.createElement)
        if node.type in ("lexical_declaration", "variable_declaration"):
            node_text = node.text.decode("utf-8")
            if "createElement" in node_text or "querySelector" in node_text:
                ctrl_id, label, ui_type = self._extract_control_info(node, file_path)
                if ctrl_id:
                    graph.add_node_rich(
                        node_id=ctrl_id,
                        label=label,
                        category="UI_CONTROL",
                        scope={"scope_id": next_scope_id, "file": file_path, "line": node.start_point[0] + 1},
                        props={"ui_type": ui_type}
                    )

        # 3. 偵測事件綁定與清理 (addEventListener / removeEventListener)
        if node.type == "call_expression":
            fn_node = node.child_by_field_name("function")
            if fn_node and fn_node.type == "member_expression":
                prop = fn_node.child_by_field_name("property")
                obj = fn_node.child_by_field_name("object")
                if prop:
                    method_name = prop.text.decode("utf-8")
                    if method_name == "addEventListener":
                        self._handle_add_event_listener(node, obj, next_scope_id, scopes, file_path, graph)
                    elif method_name == "removeEventListener":
                        # 性能與記憶體防護：偵測銷毀清理守衛 (Cleanup Guard)
                        line = node.start_point[0] + 1
                        guard_id = f"cleanup:removeListener@{file_path}:L{line}"
                        graph.add_node_rich(
                            node_id=guard_id,
                            label="removeEventListener()",
                            category="INVARIANT_GUARD",
                            scope={"scope_id": next_scope_id, "file": file_path, "line": line},
                            props={"is_cleanup": True}
                        )
                        parent = self._find_enclosing_node_id(next_scope_id, graph)
                        if parent:
                            graph.add_edge_rich(
                                source=parent,
                                target=guard_id,
                                edge_type="CALLS",
                                status="VALID",
                                detail="建立防洩漏銷毀清理守衛"
                            )

            elif fn_node and fn_node.type == "identifier":
                callee_name = fn_node.text.decode("utf-8")
                if callee_name not in ("fetch", "parseInt", "setTimeout"):
                    is_awaited = (node.parent and node.parent.type == "await_expression")
                    self._resolve_call_site(node, callee_name, next_scope_id, scopes, file_path, graph, is_awaited)

        for child in node.children:
            self._wire_ui_and_calls(child, next_scope_id, scopes, code, file_path, graph)

    def _handle_jsx_element(
        self,
        jsx_node: Node,
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        file_path: str,
        graph: UIACodeGraph,
    ):
        text = jsx_node.text.decode("utf-8")
        line = jsx_node.start_point[0] + 1
        
        # 尋找 tag 名稱
        tag_name = "Button" if "button" in text[:30].lower() else "JSXElement"
        ctrl_id = f"ctrl:{tag_name}@{file_path}:L{line}"
        
        # 尋找是否有 onClick / onKeyDown 等屬性
        if "onClick" in text:
            graph.add_node_rich(
                node_id=ctrl_id,
                label=f"<{tag_name} onClick>",
                category="UI_CONTROL",
                scope={"scope_id": current_scope_id, "file": file_path, "line": line},
                props={"ui_type": "Button"}
            )
            evt_id = f"event:{tag_name}.onClick@{file_path}:L{line}"
            graph.add_node_rich(
                node_id=evt_id,
                label="onClick",
                category="EVENT_BINDING",
                scope={"scope_id": current_scope_id, "file": file_path, "line": line},
                props={"event_name": "click"}
            )
            graph.add_edge_rich(
                source=ctrl_id,
                target=evt_id,
                edge_type="WIRES_TO",
                status="VALID",
                detail="JSX 屬性綁定"
            )

    def _extract_control_info(self, decl_node: Node, file_path: str) -> Tuple[Optional[str], str, str]:
        text = decl_node.text.decode("utf-8")
        line = decl_node.start_point[0] + 1
        var_name = "element"
        for child in decl_node.children:
            if child.type == "variable_declarator":
                name_node = child.child_by_field_name("name")
                if name_node:
                    var_name = name_node.text.decode("utf-8")

        ui_type = "Button" if "btn" in var_name.lower() or "button" in text.lower() else "Control"
        label = f"#{var_name}" if not var_name.startswith("#") else var_name
        ctrl_id = f"ctrl:{var_name}@{file_path}:L{line}"
        return ctrl_id, label, ui_type

    def _handle_add_event_listener(
        self,
        call_node: Node,
        obj_node: Optional[Node],
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        file_path: str,
        graph: UIACodeGraph,
    ):
        args_node = call_node.child_by_field_name("arguments")
        if not args_node or args_node.child_count < 2:
            return

        event_arg = args_node.children[1]
        event_name = event_arg.text.decode("utf-8").strip("'\"")
        line = call_node.start_point[0] + 1
        obj_name = obj_node.text.decode("utf-8") if obj_node else "element"
        ctrl_id = None

        for n, d in graph.g.nodes(data=True):
            if d.get("category") == "UI_CONTROL" and (obj_name in n or obj_name in d.get("label", "")):
                ctrl_id = n
                break

        if not ctrl_id:
            ctrl_id = f"ctrl:{obj_name}@{file_path}:L{line}"
            graph.add_node_rich(
                node_id=ctrl_id,
                label=f"#{obj_name}",
                category="UI_CONTROL",
                scope={"scope_id": current_scope_id, "file": file_path, "line": line},
                props={"ui_type": "Button" if "btn" in obj_name.lower() else "Control"}
            )

        event_node_id = f"event:{obj_name}.on('{event_name}')@{file_path}:L{line}"
        graph.add_node_rich(
            node_id=event_node_id,
            label=f"on('{event_name}')",
            category="EVENT_BINDING",
            scope={"scope_id": current_scope_id, "file": file_path, "line": line},
            props={"event_name": event_name}
        )

        graph.add_edge_rich(
            source=ctrl_id,
            target=event_node_id,
            edge_type="WIRES_TO",
            flow_type="SYNC",
            status="VALID",
            detail=f"綁定 {event_name} 事件"
        )

        handler_arg = args_node.children[3] if args_node.child_count > 3 else None
        if not handler_arg:
            return

        if handler_arg.type == "identifier":
            handler_name = handler_arg.text.decode("utf-8")
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

    def _resolve_call_site(
        self,
        call_node: Node,
        callee_name: str,
        caller_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        file_path: str,
        graph: UIACodeGraph,
        is_awaited: bool = False,
    ):
        line = call_node.start_point[0] + 1

        if callee_name in ("confirm", "alert", "prompt"):
            hazard_node_id = f"hazard:{callee_name}@{file_path}:L{line}"
            graph.add_node_rich(
                node_id=hazard_node_id,
                label=f"window.{callee_name}",
                category="INVARIANT_GUARD",
                scope={"scope_id": caller_scope_id, "file": file_path, "line": line},
                props={"is_blocking": True, "hazard": "SYNC_BLOCKING_UI"}
            )
            parent_node = self._find_enclosing_node_id(caller_scope_id, graph)
            if parent_node:
                graph.add_edge_rich(
                    source=parent_node,
                    target=hazard_node_id,
                    edge_type="CALLS",
                    status="BLOCKED_INVARIANT",
                    detail=f"呼叫了同步阻塞之 window.{callee_name}()"
                )
            return

        parent_node = self._find_enclosing_node_id(caller_scope_id, graph)
        flow_type = "AWAIT" if is_awaited else "SYNC"

        self._link_handler_with_reachability(
            caller_id=parent_node or f"scope:{caller_scope_id}",
            callee_name=callee_name,
            call_scope_id=caller_scope_id,
            scopes=scopes,
            file_path=file_path,
            line=line,
            graph=graph,
            is_direct_trigger=False,
            flow_type=flow_type,
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
                        detail="引用全域或外部函式"
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
