import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Fix C# Adapter
cs_path = Path("d:/AntiGravity/UIA_Coder/code_map/adapters/csharp_adapter.py")
cs_text = cs_path.read_text(encoding="utf-8").replace("\r\n", "\n")

dup_cs_block = '''            elif ntype in ("field_declaration", "constant_declaration"):
                start_row = get_line(node.start_byte)
                end_row = get_line(node.end_byte)
                source_code_slice = decode_slice(node.start_byte, node.end_byte)
                var_name = source_code_slice.split("=")[0].strip().split()[-1] if "=" in source_code_slice else f"state_{start_row}"
                var_name = var_name.strip(";")
                state_id = f"state:{var_name}@{file_path}:L{start_row}"
                graph.add_node_rich(
                    node_id=state_id,
                    label=var_name,
                    category="MODULE_STATE",
                    scope={"scope_id": curr_class or "scope:global", "file": file_path, "line": start_row},
                    props={
                        "signature": f"[Module State] {var_name}",
                        "source_code": source_code_slice,
                        "line_start": start_row,
                        "line_end": end_row,
                        "executable_fingerprint": self.compute_executable_fingerprint(node),
                    }
                )'''

fixed_cs_block = '''            elif ntype in ("field_declaration", "constant_declaration"):
                curr_class = class_stack[-1] if class_stack else None
                start_row = get_line(node.start_byte)
                end_row = get_line(node.end_byte)
                source_code_slice = decode_slice(node.start_byte, node.end_byte)
                var_name = source_code_slice.split("=")[0].strip().split()[-1] if "=" in source_code_slice else f"state_{start_row}"
                var_name = var_name.strip(";")
                state_id = f"state:{var_name}@{file_path}:L{start_row}"
                graph.add_node_rich(
                    node_id=state_id,
                    label=var_name,
                    category="MODULE_STATE",
                    scope={"scope_id": curr_class or "scope:global", "file": file_path, "line": start_row},
                    props={
                        "signature": f"[Module State] {var_name}",
                        "source_code": source_code_slice,
                        "line_start": start_row,
                        "line_end": end_row,
                        "executable_fingerprint": self.compute_executable_fingerprint(node),
                    }
                )'''

# Replace first occurrence (Pass 1) with fixed_cs_block, and remove second occurrence (Pass 2)
parts = cs_text.split(dup_cs_block)
if len(parts) == 3:
    cs_text = parts[0] + fixed_cs_block + parts[1] + parts[2].lstrip("\n")
elif len(parts) == 2:
    cs_text = parts[0] + fixed_cs_block + parts[1]
cs_path.write_text(cs_text, encoding="utf-8")
print("Fixed csharp_adapter.py, parts:", len(parts))

# 2. Fix Rust Adapter
rust_path = Path("d:/AntiGravity/UIA_Coder/code_map/adapters/rust_adapter.py")
rust_text = rust_path.read_text(encoding="utf-8").replace("\r\n", "\n")

old_rust_props = '''                            "is_async": is_async,
                            "impl_type": curr_impl or "",
                            "raw_name": raw_name,
                        },'''
new_rust_props = '''                            "is_async": is_async,
                            "impl_type": curr_impl or "",
                            "raw_name": raw_name,
                            "executable_fingerprint": self.compute_executable_fingerprint(node),
                        },'''
rust_text = rust_text.replace(old_rust_props, new_rust_props)

dup_rust_block = '''            elif ntype in ("const_item", "static_item"):
                start_row = get_line(node.start_byte)
                end_row = get_line(node.end_byte)
                source_code_slice = decode_slice(node.start_byte, node.end_byte)
                name_node = node.child_by_field_name("name")
                var_name = decode_slice(name_node.start_byte, name_node.end_byte) if name_node else f"state_{start_row}"
                state_id = f"state:{var_name}@{file_path}:L{start_row}"
                graph.add_node_rich(
                    node_id=state_id,
                    label=var_name,
                    category="MODULE_STATE",
                    scope={"scope_id": "scope:global", "file": file_path, "line": start_row},
                    props={
                        "signature": f"[Module State] {var_name}",
                        "source_code": source_code_slice,
                        "line_start": start_row,
                        "line_end": end_row,
                        "executable_fingerprint": self.compute_executable_fingerprint(node),
                    }
                )'''

r_parts = rust_text.split(dup_rust_block)
if len(r_parts) == 3:
    rust_text = r_parts[0] + dup_rust_block + r_parts[1] + r_parts[2].lstrip("\n")
rust_path.write_text(rust_text, encoding="utf-8")
print("Fixed rust_adapter.py, parts:", len(r_parts))

# 3. Fix Go Adapter
go_path = Path("d:/AntiGravity/UIA_Coder/code_map/adapters/go_adapter.py")
go_text = go_path.read_text(encoding="utf-8").replace("\r\n", "\n")

dup_go_block = '''            elif ntype in ("const_declaration", "var_declaration"):
                start_row = get_line(node.start_byte)
                end_row = get_line(node.end_byte)
                source_code_slice = decode_slice(node.start_byte, node.end_byte)
                var_name = source_code_slice.split("\\n")[0].split("=")[0].replace("const", "").replace("var", "").strip().split()[0] if source_code_slice else f"state_{start_row}"
                var_name = var_name.strip("()")
                if var_name:
                    state_id = f"state:{var_name}@{file_path}:L{start_row}"
                    graph.add_node_rich(
                        node_id=state_id,
                        label=var_name,
                        category="MODULE_STATE",
                        scope={"scope_id": "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": f"[Module State] {var_name}",
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "executable_fingerprint": self.compute_executable_fingerprint(node),
                        }
                    )'''

g_parts = go_text.split(dup_go_block)
if len(g_parts) == 3:
    go_text = g_parts[0] + dup_go_block + g_parts[1] + g_parts[2].lstrip("\n")
go_path.write_text(go_text, encoding="utf-8")
print("Fixed go_adapter.py, parts:", len(g_parts))
