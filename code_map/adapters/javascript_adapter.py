import re
from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_javascript as tsjs

from code_map.core.base_adapter import BaseCodeMapBuilder
from code_map.core.graph import CodeMapGraph


class JavaScriptCodeMapBuilder(BaseCodeMapBuilder):
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

    def parse_and_build(self, source_code: str, file_path: str = "app.js") -> CodeMapGraph:
        tree = self.parser.parse(bytes(source_code, "utf-8"))
        graph = CodeMapGraph(name=f"Graph of {file_path}")

        scopes: Dict[str, Dict[str, Any]] = {
            "scope:global": {
                "id": "scope:global",
                "parent": None,
                "depth": 0,
                "defs": {},
                "qualified_path": "global",
            }
        }

        node_scope_map: Dict[int, str] = {}
        self._collect_scopes_and_functions(tree.root_node, "scope:global", scopes, source_code, file_path, graph, node_scope_map)
        self._wire_ui_and_calls(tree.root_node, "scope:global", scopes, source_code, file_path, graph, node_scope_map)
        return graph

    def _infer_function_name(self, node: Node) -> Optional[str]:
        parent = node.parent
        if not parent:
            return None

        # 1. const foo = () => {} 或 let foo = function() {}
        if parent.type == "variable_declarator":
            name_node = parent.child_by_field_name("name")
            if name_node:
                return name_node.text.decode("utf-8")

        # 2. foo = () => {} 或 this.foo = () => {}
        if parent.type == "assignment_expression":
            left = parent.child_by_field_name("left")
            if left:
                if left.type == "identifier":
                    return left.text.decode("utf-8")
                elif left.type == "member_expression":
                    prop = left.child_by_field_name("property")
                    if prop:
                        return prop.text.decode("utf-8")

        # 3. { foo: () => {} }
        if parent.type == "pair":
            key = parent.child_by_field_name("key")
            if key:
                return key.text.decode("utf-8").strip("'\"")

        # 3.1 類別欄位函式: class Foo { bar = () => {} }
        if parent.type in ("public_field_definition", "field_definition", "property_definition", "class_field"):
            prop_node = parent.child_by_field_name("name") or parent.child_by_field_name("property")
            if prop_node:
                return prop_node.text.decode("utf-8").strip("'\"")
            for c in parent.children:
                if c.type in ("property_identifier", "identifier"):
                    return c.text.decode("utf-8").strip("'\"")

        # 3.2 預設匯出: export default () => {} 或 export default function() {}
        if parent.type in ("export_statement", "export_declaration"):
            for c in parent.children:
                if c.type == "default":
                    return "default"

        # 4. React HOCs 或 Alpine/Framework 指令包裝器:
        #    directive('model', (el, ...) => ...)
        #    Alpine.directive('sort', ...)
        if parent.type == "arguments" and parent.parent and parent.parent.type == "call_expression":
            call_expr = parent.parent
            fn = call_expr.child_by_field_name("function")
            fn_name = fn.text.decode("utf-8") if fn else ""

            if call_expr.parent and call_expr.parent.type == "variable_declarator":
                var_name = call_expr.parent.child_by_field_name("name")
                if var_name:
                    return var_name.text.decode("utf-8")

            if call_expr.parent and call_expr.parent.type == "assignment_expression":
                left = call_expr.parent.child_by_field_name("left")
                if left and left.type == "identifier":
                    return left.text.decode("utf-8")

            if any(kw in fn_name for kw in ("directive", "magic", "plugin")):
                for a in parent.children:
                    if a.type in ("string", "string_fragment", "string_literal"):
                        clean = a.text.decode("utf-8").strip("'\"`")
                        if clean:
                            return f"directive:{clean}"

            if call_expr.parent and call_expr.parent.type == "expression_statement":
                short_fn = fn_name.split(".")[-1]
                if short_fn in ("forEach", "map", "filter", "reduce", "then", "catch", "define", "it", "test", "describe", "ready", "each"):
                    return f"{short_fn}:callback"

        return None

    def _collect_scopes_and_functions(
        self,
        node: Node,
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        code: str,
        file_path: str,
        graph: CodeMapGraph,
        node_scope_map: Optional[Dict[int, str]] = None,
    ):
        next_scope_id = current_scope_id

        # 收集模組頂層常數狀態 (MODULE_STATE)，如頂層映射表、正則常數等
        if current_scope_id == "scope:global" and node.type in ("lexical_declaration", "variable_declaration"):
            for child in node.children:
                if child.type == "variable_declarator":
                    name_node = child.child_by_field_name("name")
                    val_node = child.child_by_field_name("value")
                    if name_node and val_node and val_node.type not in ("function_expression", "arrow_function"):
                        val_text = val_node.text.decode("utf-8")
                        # 排除 DOM 控制項建立或選取 (由 UI_CONTROL 專責處理)
                        if "createElement" in val_text or "querySelector" in val_text:
                            continue
                        var_name = name_node.text.decode("utf-8")
                        start_line = child.start_point[0] + 1
                        end_line = child.end_point[0] + 1
                        state_nid = f"state:{var_name}@{file_path}:L{start_line}"
                        raw_text = child.text.decode("utf-8")
                        graph.add_node_rich(
                            node_id=state_nid,
                            label=var_name,
                            category="MODULE_STATE",
                            scope={"scope_id": "scope:global", "file": file_path, "line": start_line},
                            props={
                                "line_start": start_line,
                                "line_end": end_line,
                                "source_code": raw_text,
                                "executable_fingerprint": self.compute_executable_fingerprint(child),
                            }
                        )

        # 收集 export default 非函式表達式 (例如 export default { ... } 或 export default defineConfig(...))
        if current_scope_id == "scope:global" and node.type in ("export_statement", "export_declaration"):
            has_default = any(c.type == "default" for c in node.children)
            if has_default:
                val_node = node.child_by_field_name("value") or node.child_by_field_name("declaration")
                if not val_node:
                    for c in node.children:
                        if c.type not in ("export", "default", ";", "comment"):
                            val_node = c
                            break
                if val_node and val_node.type not in ("function_expression", "arrow_function", "function_declaration", "class_declaration"):
                    start_line = node.start_point[0] + 1
                    end_line = node.end_point[0] + 1
                    state_nid = f"state:default@{file_path}:L{start_line}"
                    raw_text = node.text.decode("utf-8")
                    graph.add_node_rich(
                        node_id=state_nid,
                        label="default",
                        category="MODULE_STATE",
                        scope={"scope_id": "scope:global", "file": file_path, "line": start_line},
                        props={
                            "line_start": start_line,
                            "line_end": end_line,
                            "source_code": raw_text,
                            "executable_fingerprint": self.compute_executable_fingerprint(val_node),
                        }
                    )
                    graph.g.graph["exports"]["default"] = state_nid

        # 收集模組頂層呼叫表達式 (例如 enyo.kind({...}), define([...]), Object.forEach(...))
        if current_scope_id == "scope:global" and node.type == "expression_statement":
            for child in node.children:
                if child.type == "call_expression":
                    fn_node = child.child_by_field_name("function")
                    if fn_node:
                        fn_name = fn_node.text.decode("utf-8")
                        if not any(fn_name.endswith(ig) for ig in ("addEventListener", "removeEventListener", "console.log", "console.warn", "console.error", "console.info", "require")):
                            start_line = child.start_point[0] + 1
                            end_line = child.end_point[0] + 1
                            call_nid = f"call:{fn_name}@{file_path}:L{start_line}"
                            graph.add_node_rich(
                                node_id=call_nid,
                                label=f"{fn_name}()",
                                category="MODULE_STATE",
                                scope={"scope_id": "scope:global", "file": file_path, "line": start_line},
                                props={
                                    "line_start": start_line,
                                    "line_end": end_line,
                                    "source_code": child.text.decode("utf-8"),
                                    "executable_fingerprint": self.compute_executable_fingerprint(child),
                                }
                            )

        # 收集模組頂層控制流 (例如 scripts/ensure-pnpm.js 的 if (...), 或 Sortable.js 的 if (documentExists))
        if current_scope_id == "scope:global" and node.type in ("if_statement", "try_statement"):
            start_line = node.start_point[0] + 1
            end_line = node.end_point[0] + 1
            cond_node = node.child_by_field_name("condition")
            cond_text = cond_node.text.decode("utf-8") if cond_node else node.type
            clean_cond = " ".join(cond_text.split())[:25]
            stmt_nid = f"guard:{node.type}@{file_path}:L{start_line}"
            graph.add_node_rich(
                node_id=stmt_nid,
                label=f"{node.type}({clean_cond})",
                category="MODULE_STATE",
                scope={"scope_id": "scope:global", "file": file_path, "line": start_line},
                props={
                    "line_start": start_line,
                    "line_end": end_line,
                    "source_code": node.text.decode("utf-8"),
                    "executable_fingerprint": self.compute_executable_fingerprint(node),
                }
            )

        if node.type == "import_statement":
            source_node = node.child_by_field_name("source")
            mod_path = source_node.text.decode("utf-8").strip("'\"`") if source_node else ""
            line = node.start_point[0] + 1
            for child in node.children:
                if child.type == "import_clause":
                    for c in child.children:
                        if c.type == "named_imports":
                            for spec in c.children:
                                if spec.type == "import_specifier":
                                    name_node = spec.child_by_field_name("name")
                                    alias_node = spec.child_by_field_name("alias")
                                    imp_name = name_node.text.decode("utf-8") if name_node else ""
                                    local_name = alias_node.text.decode("utf-8") if alias_node else imp_name
                                    if imp_name:
                                        graph.g.graph["imports"].append({
                                            "local_name": local_name,
                                            "imported_name": imp_name,
                                            "module_specifier": mod_path,
                                            "line": line,
                                        })
                        elif c.type == "identifier":
                            dname = c.text.decode("utf-8")
                            graph.g.graph["imports"].append({
                                "local_name": dname,
                                "imported_name": "default",
                                "module_specifier": mod_path,
                                "line": line,
                            })

        elif node.type in ("class_declaration", "abstract_class_declaration", "class"):
            name_node = node.child_by_field_name("name")
            class_name = name_node.text.decode("utf-8") if name_node else "AnonymousClass"
            start_line = node.start_point[0] + 1
            start_col = node.start_point[1] + 1
            new_scope_id = f"scope:{class_name}@{file_path}:L{start_line}C{start_col}"
            depth = scopes[current_scope_id]["depth"] + 1

            parent_qual = scopes[current_scope_id].get("qualified_path", "global")
            qual = class_name if parent_qual == "global" else f"{parent_qual}.{class_name}"

            class_node_id = f"class:{class_name}@{file_path}:L{start_line}C{start_col}"
            scopes[new_scope_id] = {
                "id": new_scope_id,
                "parent": current_scope_id,
                "depth": depth,
                "defs": {},
                "func_node_id": class_node_id,
                "qualified_path": qual,
            }
            next_scope_id = new_scope_id

        elif node.type in ("public_field_definition", "field_definition", "property_definition"):
            val_node = node.child_by_field_name("value")
            name_node = node.child_by_field_name("name") or node.child_by_field_name("property")
            field_name = name_node.text.decode("utf-8").strip("'\"") if name_node else "field"
            if val_node and val_node.type not in ("function_expression", "arrow_function"):
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                parent_qual = scopes[current_scope_id].get("qualified_path", "global")
                qual = f"{parent_qual}.{field_name}" if parent_qual != "global" else field_name
                state_nid = f"field:{qual}@{file_path}:L{start_line}"
                raw_text = node.text.decode("utf-8")
                graph.add_node_rich(
                    node_id=state_nid,
                    label=field_name,
                    category="MODULE_STATE",
                    scope={"scope_id": current_scope_id, "file": file_path, "line": start_line, "qualified_path": parent_qual},
                    props={
                        "line_start": start_line,
                        "line_end": end_line,
                        "source_code": raw_text,
                        "executable_fingerprint": self.compute_executable_fingerprint(node),
                    }
                )

        elif node.type in ("function_declaration", "generator_function_declaration"):
            func_name_node = node.child_by_field_name("name")
            func_name = func_name_node.text.decode("utf-8") if func_name_node else "anonymous"
            start_line = node.start_point[0] + 1
            start_col = node.start_point[1] + 1
            new_scope_id = f"scope:{func_name}@{file_path}:L{start_line}C{start_col}"
            depth = scopes[current_scope_id]["depth"] + 1

            parent_qual = scopes[current_scope_id].get("qualified_path", "global")
            qual = func_name if parent_qual == "global" else f"{parent_qual}.{func_name}"

            func_node_id = f"func:{func_name}@{file_path}:L{start_line}C{start_col}"
            scopes[new_scope_id] = {
                "id": new_scope_id,
                "parent": current_scope_id,
                "depth": depth,
                "defs": {},
                "func_node_id": func_node_id,
                "qualified_path": qual,
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
                scope={"scope_id": current_scope_id, "inner_scope": new_scope_id, "depth": depth - 1, "file": file_path, "line": start_line, "qualified_path": parent_qual},
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

            is_exported = False
            p_check = node.parent
            while p_check:
                if p_check.type in ("export_statement", "export_declaration"):
                    is_exported = True
                    break
                p_check = p_check.parent
            if is_exported:
                graph.g.graph["exports"][func_name] = func_node_id

            next_scope_id = new_scope_id

        elif node.type in ("arrow_function", "function_expression"):
            start_line = node.start_point[0] + 1
            start_col = node.start_point[1] + 1
            inferred_name = self._infer_function_name(node)

            if inferred_name:
                parent_qual = scopes[current_scope_id].get("qualified_path", "global")
                qual = inferred_name if parent_qual == "global" else f"{parent_qual}.{inferred_name}"

                new_scope_id = f"scope:{inferred_name}@{file_path}:L{start_line}C{start_col}"
                func_node_id = f"func:{inferred_name}@{file_path}:L{start_line}C{start_col}"
                depth = scopes[current_scope_id]["depth"] + 1

                scopes[new_scope_id] = {
                    "id": new_scope_id,
                    "parent": current_scope_id,
                    "depth": depth,
                    "defs": {},
                    "func_node_id": func_node_id,
                    "qualified_path": qual,
                }

                is_async = (b"async" in node.children[0].text if node.children else False)
                params_node = node.child_by_field_name("parameters")
                param_text = params_node.text.decode("utf-8") if params_node else "()"
                full_text = node.text.decode("utf-8")
                sig_text = f"{inferred_name}{param_text}"
                end_line = node.end_point[0] + 1

                scopes[current_scope_id]["defs"][inferred_name] = {
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
                    label=inferred_name,
                    category="FUNCTION_DEF",
                    scope={"scope_id": current_scope_id, "inner_scope": new_scope_id, "depth": depth - 1, "file": file_path, "line": start_line, "qualified_path": parent_qual},
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

                is_exported = False
                p_check = node.parent
                while p_check:
                    if p_check.type in ("export_statement", "export_declaration"):
                        is_exported = True
                        break
                    p_check = p_check.parent
                if is_exported:
                    graph.g.graph["exports"][inferred_name] = func_node_id

                next_scope_id = new_scope_id
            else:
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

        elif node.type == "assignment_expression":
            left = node.child_by_field_name("left")
            right = node.child_by_field_name("right")
            if right and right.type in ("function_expression", "arrow_function") and left:
                method_name = None
                if left.type == "member_expression":
                    prop = left.child_by_field_name("property")
                    if prop:
                        method_name = prop.text.decode("utf-8")
                elif left.type == "identifier":
                    method_name = left.text.decode("utf-8")

                if method_name:
                    start_line = right.start_point[0] + 1
                    start_col = right.start_point[1] + 1
                    new_scope_id = f"scope:{method_name}@{file_path}:L{start_line}C{start_col}"
                    depth = scopes[current_scope_id]["depth"] + 1

                    parent_qual = scopes[current_scope_id].get("qualified_path", "global")
                    qual = method_name if parent_qual == "global" else f"{parent_qual}.{method_name}"

                    func_node_id = f"func:{method_name}@{file_path}:L{start_line}C{start_col}"
                    scopes[new_scope_id] = {
                        "id": new_scope_id,
                        "parent": current_scope_id,
                        "depth": depth,
                        "defs": {},
                        "func_node_id": func_node_id,
                        "qualified_path": qual,
                    }

                    is_async = (b"async" in right.children[0].text if right.children else False)
                    params_node = right.child_by_field_name("parameters")
                    param_text = params_node.text.decode("utf-8") if params_node else "()"
                    full_text = right.text.decode("utf-8")
                    sig_text = f"{method_name}{param_text}"
                    end_line = right.end_point[0] + 1

                    scopes[current_scope_id]["defs"][method_name] = {
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
                        label=method_name,
                        category="FUNCTION_DEF",
                        scope={"scope_id": current_scope_id, "inner_scope": new_scope_id, "depth": depth - 1, "file": file_path, "line": start_line, "qualified_path": parent_qual},
                        props={
                            "is_async": is_async,
                            "inner_scope": new_scope_id,
                            "signature": sig_text,
                            "parameters": param_text,
                            "line_start": start_line,
                            "line_end": end_line,
                            "line_count": end_line - start_line + 1,
                            "source_code": full_text,
                            "executable_fingerprint": self.compute_executable_fingerprint(right),
                        }
                    )
                    next_scope_id = new_scope_id
            elif current_scope_id == "scope:global" and left:
                var_name = left.text.decode("utf-8")
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                state_nid = f"state:{var_name}@{file_path}:L{start_line}"
                raw_text = node.text.decode("utf-8")
                graph.add_node_rich(
                    node_id=state_nid,
                    label=var_name,
                    category="MODULE_STATE",
                    scope={"scope_id": "scope:global", "file": file_path, "line": start_line},
                    props={
                        "line_start": start_line,
                        "line_end": end_line,
                        "source_code": raw_text,
                        "executable_fingerprint": self.compute_executable_fingerprint(node),
                    }
                )

        elif node.type in ("method_definition", "pair"):
            key_node = node.child_by_field_name("name") or node.child_by_field_name("key")
            value_node = node.child_by_field_name("value") or node
            if key_node and (node.type == "method_definition" or (value_node and value_node.type in ("function_expression", "arrow_function"))):
                method_name = key_node.text.decode("utf-8").strip("'\"")
                target_func_node = value_node if node.type == "pair" else node
                start_line = target_func_node.start_point[0] + 1
                start_col = target_func_node.start_point[1] + 1
                new_scope_id = f"scope:{method_name}@{file_path}:L{start_line}C{start_col}"
                depth = scopes[current_scope_id]["depth"] + 1

                parent_qual = scopes[current_scope_id].get("qualified_path", "global")
                qual = method_name if parent_qual == "global" else f"{parent_qual}.{method_name}"

                func_node_id = f"func:{method_name}@{file_path}:L{start_line}C{start_col}"
                scopes[new_scope_id] = {
                    "id": new_scope_id,
                    "parent": current_scope_id,
                    "depth": depth,
                    "defs": {},
                    "func_node_id": func_node_id,
                    "qualified_path": qual,
                }

                is_async = (b"async" in target_func_node.children[0].text if target_func_node.children else False)
                params_node = target_func_node.child_by_field_name("parameters")
                param_text = params_node.text.decode("utf-8") if params_node else "()"
                full_text = target_func_node.text.decode("utf-8")
                sig_text = f"{method_name}{param_text}"
                end_line = target_func_node.end_point[0] + 1

                scopes[current_scope_id]["defs"][method_name] = {
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
                    label=method_name,
                    category="FUNCTION_DEF",
                    scope={"scope_id": current_scope_id, "inner_scope": new_scope_id, "depth": depth - 1, "file": file_path, "line": start_line, "qualified_path": parent_qual},
                    props={
                        "is_async": is_async,
                        "inner_scope": new_scope_id,
                        "signature": sig_text,
                        "parameters": param_text,
                        "line_start": start_line,
                        "line_end": end_line,
                        "line_count": end_line - start_line + 1,
                        "source_code": full_text,
                        "executable_fingerprint": self.compute_executable_fingerprint(target_func_node),
                    }
                )
                next_scope_id = new_scope_id

        if node_scope_map is not None and next_scope_id != current_scope_id:
            node_scope_map[node.id] = next_scope_id

        for child in node.children:
            self._collect_scopes_and_functions(child, next_scope_id, scopes, code, file_path, graph, node_scope_map)

    def _wire_ui_and_calls(
        self,
        node: Node,
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        code: str,
        file_path: str,
        graph: CodeMapGraph,
        node_scope_map: Optional[Dict[int, str]] = None,
    ):
        if node_scope_map is not None:
            next_scope_id = node_scope_map.get(node.id, current_scope_id)
        else:
            next_scope_id = current_scope_id
            if node.type in ("function_declaration", "generator_function_declaration"):
                func_name_node = node.child_by_field_name("name")
                func_name = func_name_node.text.decode("utf-8") if func_name_node else "anonymous"
                start_line = node.start_point[0] + 1
                start_col = node.start_point[1] + 1
                next_scope_id = f"scope:{func_name}@{file_path}:L{start_line}C{start_col}"
            elif node.type in ("method_definition", "pair"):
                key_node = node.child_by_field_name("name") or node.child_by_field_name("key")
                if key_node:
                    method_name = key_node.text.decode("utf-8").strip("'\"")
                    target_node = node.child_by_field_name("value") or node
                    start_line = target_node.start_point[0] + 1
                    start_col = target_node.start_point[1] + 1
                    next_scope_id = f"scope:{method_name}@{file_path}:L{start_line}C{start_col}"
            elif node.type in ("arrow_function", "function_expression"):
                start_line = node.start_point[0] + 1
                start_col = node.start_point[1] + 1
                inferred_name = self._infer_function_name(node)
                if inferred_name:
                    next_scope_id = f"scope:{inferred_name}@{file_path}:L{start_line}C{start_col}"
                else:
                    next_scope_id = f"scope:arrow@{file_path}:L{start_line}C{start_col}"
            elif node.type in ("class_declaration", "abstract_class_declaration", "class"):
                name_node = node.child_by_field_name("name")
                class_name = name_node.text.decode("utf-8") if name_node else "AnonymousClass"
                start_line = node.start_point[0] + 1
                start_col = node.start_point[1] + 1
                next_scope_id = f"scope:{class_name}@{file_path}:L{start_line}C{start_col}"

        # 支援 Backbone / Spine / Marionette 的宣告式 events 雜湊表:
        # events: { 'click .destroy': 'remove', 'dblclick label': 'edit' }
        # 或 Todos.prototype.events = { ... }
        if node.type == "pair":
            key_node = node.child_by_field_name("key")
            value_node = node.child_by_field_name("value")
            if key_node and key_node.text.decode("utf-8").strip("'\"") == "events" and value_node and value_node.type == "object":
                self._handle_declarative_events_hash(value_node, next_scope_id, scopes, file_path, graph)

        elif node.type == "assignment_expression":
            left = node.child_by_field_name("left")
            right = node.child_by_field_name("right")
            if left and "events" in left.text.decode("utf-8") and right and right.type == "object":
                self._handle_declarative_events_hash(right, next_scope_id, scopes, file_path, graph)

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

            elif fn_node and fn_node.type == "member_expression":
                prop = fn_node.child_by_field_name("property")
                obj = fn_node.child_by_field_name("object")
                prop_name = prop.text.decode("utf-8") if prop else ""
                
                # 支援 .on('click', ...), .bind('event', ...), $delegate(...)
                if prop_name in ("on", "bind", "delegate", "live"):
                    self._handle_add_event_listener(node, obj, next_scope_id, scopes, file_path, graph)
                elif prop_name not in ("log", "split", "trim", "charAt", "substr", "indexOf", "push", "filter", "map", "forEach"):
                    is_awaited = (node.parent and node.parent.type == "await_expression")
                    self._resolve_call_site(node, prop_name, next_scope_id, scopes, file_path, graph, is_awaited)

            elif fn_node and fn_node.type == "identifier":
                callee_name = fn_node.text.decode("utf-8")
                if callee_name in ("$delegate", "$live", "$on"):
                    self._handle_add_event_listener(node, None, next_scope_id, scopes, file_path, graph)
                elif callee_name not in ("fetch", "parseInt", "setTimeout", "require", "define"):
                    is_awaited = (node.parent and node.parent.type == "await_expression")
                    self._resolve_call_site(node, callee_name, next_scope_id, scopes, file_path, graph, is_awaited)

        for child in node.children:
            self._wire_ui_and_calls(child, next_scope_id, scopes, code, file_path, graph, node_scope_map)

    def _handle_declarative_events_hash(
        self,
        object_node: Node,
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        file_path: str,
        graph: CodeMapGraph,
    ):
        """解析 Backbone / Spine 的 events 雜湊表，建立 UI_CONTROL -> EVENT_BINDING -> 處理常式 接線"""
        for child in object_node.children:
            if child.type == "pair":
                key_node = child.child_by_field_name("key")
                val_node = child.child_by_field_name("value")
                if not key_node or not val_node:
                    continue
                
                event_selector_str = key_node.text.decode("utf-8").strip("'\"")
                handler_name = val_node.text.decode("utf-8").strip("'\"")
                line = child.start_point[0] + 1
                
                parts = event_selector_str.split(None, 1)
                event_name = parts[0] if parts else "action"
                selector = parts[1] if len(parts) > 1 else "element"
                
                clean_selector = selector.strip()
                clean_label = f"#{clean_selector}" if not clean_selector.startswith(("#", ".")) else clean_selector
                ctrl_id = f"ctrl:{clean_selector}@{file_path}:L{line}"
                
                ui_type = "Button" if any(k in clean_selector.lower() for k in ("btn", "destroy", "toggle", "check", "button")) else "Control"
                
                # 新增或複用控制項節點
                existing_ctrl = None
                for n, d in graph.g.nodes(data=True):
                    if d.get("category") == "UI_CONTROL" and d.get("label") == clean_label:
                        existing_ctrl = n
                        break
                
                if not existing_ctrl:
                    graph.add_node_rich(
                        node_id=ctrl_id,
                        label=clean_label,
                        category="UI_CONTROL",
                        scope={"scope_id": current_scope_id, "file": file_path, "line": line},
                        props={"ui_type": ui_type, "selector": clean_selector}
                    )
                    active_ctrl_id = ctrl_id
                else:
                    active_ctrl_id = existing_ctrl
                
                event_node_id = f"event:{clean_selector}.on('{event_name}')@{file_path}:L{line}"
                graph.add_node_rich(
                    node_id=event_node_id,
                    label=f"on('{event_name}')",
                    category="EVENT_BINDING",
                    scope={"scope_id": current_scope_id, "file": file_path, "line": line},
                    props={"event_name": event_name, "selector": clean_selector}
                )
                
                graph.add_edge_rich(
                    source=active_ctrl_id,
                    target=event_node_id,
                    edge_type="WIRES_TO",
                    flow_type="SYNC",
                    status="VALID",
                    detail=f"Backbone/Spine 宣告式綁定 {event_name}"
                )
                
                # 接線到處理函式
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
        graph: CodeMapGraph,
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
            anon_func_id = f"func:{obj_name}.on('{event_name}')_handler@{file_path}:L{h_line}"
            if arrow_scope_id in scopes:
                scopes[arrow_scope_id]["func_node_id"] = anon_func_id

            if anon_func_id not in graph.g:
                graph.add_node_rich(
                    node_id=anon_func_id,
                    label=f"on('{event_name}')_handler",
                    category="FUNCTION_DEF",
                    scope={"scope_id": arrow_scope_id, "file": file_path, "line": h_line},
                    props={
                        "is_async": False,
                        "signature": f"function(event)",
                        "line_start": h_line,
                        "line_end": handler_arg.end_point[0] + 1,
                        "source_code": handler_arg.text.decode("utf-8"),
                        "executable_fingerprint": self.compute_executable_fingerprint(handler_arg),
                    }
                )
                graph.add_edge_rich(
                    source=event_node_id,
                    target=anon_func_id,
                    edge_type="TRIGGERS",
                    flow_type="SYNC",
                    status="VALID",
                    detail=f"觸發匿名 {event_name} 處理常式"
                )

    def _resolve_call_site(
        self,
        call_node: Node,
        callee_name: str,
        caller_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        file_path: str,
        graph: CodeMapGraph,
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
        ctx = self._inspect_control_context(call_node)

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
            is_conditional=ctx["is_conditional"],
            guard_type=ctx["guard_type"],
            guard_expr=ctx["guard_expr"],
            is_error_handled=ctx["is_error_handled"],
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
        is_conditional: bool = False,
        guard_type: str = "NONE",
        guard_expr: str = "",
        is_error_handled: bool = False,
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
                    detail=f"作用域可達 (定義於 {declaring_scope_id})",
                    is_conditional=is_conditional,
                    guard_type=guard_type,
                    guard_expr=guard_expr,
                    is_error_handled=is_error_handled,
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
                    if isolated_scope_id == "scope:global":
                        graph.add_edge_rich(
                            source=caller_id,
                            target=target_node_id,
                            edge_type=edge_type,
                            flow_type=flow_type,
                            status="VALID",
                            detail=f"作用域可達 (定義於模組頂層 {isolated_scope_id})",
                            is_conditional=is_conditional,
                            guard_type=guard_type,
                            guard_expr=guard_expr,
                            is_error_handled=is_error_handled,
                        )
                    else:
                        graph.add_edge_rich(
                            source=caller_id,
                            target=target_node_id,
                            edge_type=edge_type,
                            flow_type=flow_type,
                            status="BLOCKED_SCOPE",
                            detail=f"💥 作用域阻隔: 函式 '{callee_name}' 被深鎖在內部閉包 ({isolated_scope_id})，外部無法調用！",
                            is_conditional=is_conditional,
                            guard_type=guard_type,
                            guard_expr=guard_expr,
                            is_error_handled=is_error_handled,
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
                        detail="引用全域或外部函式",
                        is_conditional=is_conditional,
                        guard_type=guard_type,
                        guard_expr=guard_expr,
                        is_error_handled=is_error_handled,
                    )

    def _find_enclosing_node_id(self, scope_id: str, scopes: Dict[str, Dict[str, Any]], graph: CodeMapGraph) -> Optional[str]:
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
