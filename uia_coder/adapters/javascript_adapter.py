from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_javascript as tsjs

from uia_coder.core.base_adapter import BaseUIAGraphBuilder
from uia_coder.core.graph import UIACodeGraph


class JavaScriptUIAGraphBuilder(BaseUIAGraphBuilder):
    """
    基於 Tree-sitter 的 JavaScript 語意控制樹建構器
    追蹤 Lexical Scope 堆疊、消解識別碼可達性並建立 NetworkX 語意圖。
    """

    @property
    def supported_extensions(self) -> Set[str]:
        return {".js", ".mjs", ".cjs"}

    @property
    def language_name(self) -> str:
        return "JavaScript"

    def __init__(self):
        self.language = Language(tsjs.language())
        self.parser = Parser(self.language)

    def parse_and_build(self, source_code: str, file_path: str = "app.js") -> UIACodeGraph:
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
            start_col = node.start_point[1] + 1
            new_scope_id = f"scope:{func_name}@{file_path}:L{start_line}C{start_col}"
            depth = scopes[current_scope_id]["depth"] + 1

            func_node_id = f"func:{func_name}@{file_path}:L{start_line}C{start_col}"
            scopes[new_scope_id] = {
                "id": new_scope_id,
                "parent": current_scope_id,
                "depth": depth,
                "defs": {},
                "func_node_id": func_node_id,
            }

            is_async = (b"async" in node.children[0].text if node.children else False)
            params_node = node.child_by_field_name("parameters")
            param_text = params_node.text.decode("utf-8") if params_node else "()"
            full_text = node.text.decode("utf-8")
            sig_text = full_text.split("{")[0].strip() if "{" in full_text else full_text.split("\n")[0].strip()
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

        elif node.type in ("arrow_function", "function_expression"):
            start_line = node.start_point[0] + 1
            start_col = node.start_point[1] + 1
            new_scope_id = f"scope:arrow@{file_path}:L{start_line}C{start_col}"
            depth = scopes[current_scope_id]["depth"] + 1
            scopes[new_scope_id] = {
                "id": new_scope_id,
                "parent": current_scope_id,
                "depth": depth,
                "defs": {},
                "func_node_id": scopes.get(current_scope_id, {}).get("func_node_id"),
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
            start_col = node.start_point[1] + 1
            next_scope_id = f"scope:{func_name}@{file_path}:L{start_line}C{start_col}"
        elif node.type in ("arrow_function", "function_expression"):
            start_line = node.start_point[0] + 1
            start_col = node.start_point[1] + 1
            next_scope_id = f"scope:arrow@{file_path}:L{start_line}C{start_col}"

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
                        props={
                            "ui_type": ui_type,
                            "source_code": node_text,
                            "line_start": node.start_point[0] + 1,
                            "line_end": node.end_point[0] + 1,
                        }
                    )

        if node.type == "call_expression":
            fn_node = node.child_by_field_name("function")
            if fn_node and fn_node.type == "member_expression":
                prop = fn_node.child_by_field_name("property")
                obj = fn_node.child_by_field_name("object")
                if prop and prop.text.decode("utf-8") == "addEventListener":
                    self._handle_add_event_listener(node, obj, next_scope_id, scopes, file_path, graph)

            elif fn_node and fn_node.type == "identifier":
                callee_name = fn_node.text.decode("utf-8")
                if callee_name not in ("fetch", "parseInt", "setTimeout"):
                    is_awaited = (node.parent and node.parent.type == "await_expression")
                    self._resolve_call_site(node, callee_name, next_scope_id, scopes, file_path, graph, is_awaited)

        for child in node.children:
            self._wire_ui_and_calls(child, next_scope_id, scopes, code, file_path, graph)

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
        obj_name = "element"
        if obj_node:
            raw_text = obj_node.text.decode("utf-8")
            if obj_node.type == "call_expression":
                # 自動解包 $('id')、getElementById('id')、querySelector('#id')
                call_args = obj_node.child_by_field_name("arguments")
                if call_args and call_args.child_count >= 2:
                    arg_str = call_args.children[1].text.decode("utf-8").strip("'\"`")
                    if arg_str and not any(c in arg_str for c in "\n\r();"):
                        obj_name = arg_str.lstrip("#")
                    else:
                        obj_name = raw_text
                else:
                    obj_name = raw_text
            else:
                obj_name = raw_text

        clean_label = f"#{obj_name.lstrip('#')}"
        ctrl_id = None

        for n, d in graph.g.nodes(data=True):
            if d.get("category") == "UI_CONTROL" and (obj_name in n or clean_label == d.get("label", "")):
                ctrl_id = n
                break

        if not ctrl_id:
            ctrl_id = f"ctrl:{obj_name}@{file_path}:L{line}"
            graph.add_node_rich(
                node_id=ctrl_id,
                label=clean_label,
                category="UI_CONTROL",
                scope={"scope_id": current_scope_id, "file": file_path, "line": line},
                props={
                    "ui_type": "Button" if "btn" in obj_name.lower() else "Control",
                    "source_code": obj_node.text.decode("utf-8") if obj_node else "",
                    "line_start": line,
                    "line_end": call_node.end_point[0] + 1,
                }
            )

        event_node_id = f"event:{obj_name}.on('{event_name}')@{file_path}:L{line}"
        graph.add_node_rich(
            node_id=event_node_id,
            label=f"on('{event_name}')",
            category="EVENT_BINDING",
            scope={"scope_id": current_scope_id, "file": file_path, "line": line},
            props={
                "event_name": event_name,
                "source_code": call_node.text.decode("utf-8"),
                "line_start": line,
                "line_end": call_node.end_point[0] + 1,
            }
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
        elif handler_arg.type in ("arrow_function", "function_expression"):
            h_line = handler_arg.start_point[0] + 1
            h_col = handler_arg.start_point[1] + 1
            arrow_scope_id = f"scope:arrow@{file_path}:L{h_line}C{h_col}"
            if arrow_scope_id in scopes:
                scopes[arrow_scope_id]["func_node_id"] = event_node_id

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
            parent_node = self._find_enclosing_node_id(caller_scope_id, scopes, graph)
            if parent_node:
                graph.add_edge_rich(
                    source=parent_node,
                    target=hazard_node_id,
                    edge_type="CALLS",
                    status="BLOCKED_INVARIANT",
                    detail=f"呼叫了同步阻塞之 window.{callee_name}()"
                )
            return

        parent_node = self._find_enclosing_node_id(caller_scope_id, scopes, graph)
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
        visited_scopes = set()
        while curr and curr not in visited_scopes:
            visited_scopes.add(curr)
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

    def _find_enclosing_node_id(self, scope_id: str, scopes: Dict[str, Dict[str, Any]], graph: UIACodeGraph) -> Optional[str]:
        curr = scope_id
        visited = set()
        while curr and curr not in visited:
            visited.add(curr)
            func_id = scopes.get(curr, {}).get("func_node_id")
            if func_id and func_id in graph.g:
                return func_id
            curr = scopes.get(curr, {}).get("parent")

        anchors = graph.get_ui_anchors()
        return anchors[0] if anchors else None
