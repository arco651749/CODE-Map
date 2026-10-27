import re
from pathlib import Path

p = Path("d:/AntiGravity/UIA_Coder/code_map/adapters/python_adapter.py")
text = p.read_text(encoding="utf-8")

# 1. parse_and_build add _has_ui_import
old_pab = '        # 階段 1：收集所有函式宣告、方法宣告與巢狀 Scope\n        self._collect_scopes_and_functions(tree.root_node, "scope:global", scopes, source_code, file_path, graph)'
new_pab = '''        # 檢測原始碼是否引入 UI 框架特徵 (避免純後端專案被誤判為 UI 應用)
        ui_keywords = ("textual", "PyQt", "PySide", "tkinter", "ttk", "wx", "kivy", "flet", "customtkinter")
        self._has_ui_import = any(kw in source_code for kw in ui_keywords)

        # 階段 1：收集所有函式宣告、方法宣告與巢狀 Scope
        self._collect_scopes_and_functions(tree.root_node, "scope:global", scopes, source_code, file_path, graph)'''
text = text.replace(old_pab, new_pab)

# 2. _collect_scopes_and_functions add MODULE_STATE collection at top of method
old_collect_top = '        next_scope_id = current_scope_id\n\n        if node.type in ("function_definition", "async_function_definition"):'
new_collect_top = '''        next_scope_id = current_scope_id

        # 收集模組頂層常數狀態 (MODULE_STATE)
        if current_scope_id == "scope:global" and node.type == "expression_statement":
            for c in node.children:
                if c.type == "assignment":
                    left = c.child_by_field_name("left")
                    right = c.child_by_field_name("right")
                    if left and right and right.type not in ("lambda",):
                        var_name = left.text.decode("utf-8").strip()
                        if var_name.isidentifier() and (var_name.isupper() or var_name.startswith(("_", "GLOBAL", "CONFIG")) or len(var_name) > 3):
                            start_line = c.start_point[0] + 1
                            end_line = c.end_point[0] + 1
                            state_nid = f"state:{var_name}@{file_path}:L{start_line}"
                            raw_text = c.text.decode("utf-8")
                            graph.add_node_rich(
                                node_id=state_nid,
                                label=var_name,
                                category="MODULE_STATE",
                                scope={"scope_id": "scope:global", "file": file_path, "line": start_line},
                                props={
                                    "line_start": start_line,
                                    "line_end": end_line,
                                    "source_code": raw_text,
                                    "executable_fingerprint": self.compute_executable_fingerprint(c),
                                }
                            )

        if node.type in ("function_definition", "async_function_definition"):'''
text = text.replace(old_collect_top, new_collect_top)

# 3. signature fix & executable_fingerprint
old_sig = '            sig_text = full_text.split(":")[0].strip() if ":" in full_text else full_text.split("\\n")[0].strip()'
new_sig = '''            body_node = node.child_by_field_name("body")
            if body_node:
                header_bytes = node.text[: body_node.start_byte - node.start_byte]
                sig_text = " ".join(header_bytes.decode("utf-8", errors="replace").strip().rstrip(":").split())
            else:
                sig_text = " ".join(full_text.split("\\n")[0].strip().rstrip(":").split())'''
text = text.replace(old_sig, new_sig)

old_props = '''                    "line_count": end_line - start_line + 1,
                    "source_code": full_text,
                }
            )'''
new_props = '''                    "line_count": end_line - start_line + 1,
                    "source_code": full_text,
                    "executable_fingerprint": self.compute_executable_fingerprint(node),
                }
            )'''
text = text.replace(old_props, new_props)

# 4. _handle_textual_event_bindings guard
old_guard = '        if not event_name and func_name.startswith("on_"):'
new_guard = '        if not event_name and func_name.startswith("on_") and getattr(self, "_has_ui_import", False):'
text = text.replace(old_guard, new_guard)

p.write_text(text, encoding="utf-8")
print("Successfully patched python_adapter.py")
