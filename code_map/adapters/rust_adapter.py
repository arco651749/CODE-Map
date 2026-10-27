import bisect
import hashlib
from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_rust as tsrust

from code_map.core.base_adapter import BaseCodeMapBuilder
from code_map.core.graph import CodeMapGraph


class RustCodeMapBuilder(BaseCodeMapBuilder):
    """
    基於 Tree-sitter TreeCursor 的高效穩定 Rust 語意控制樹建構器
    - 採用 TreeCursor 走訪與位元組索引切片，避免 Windows C 擴充記憶體訪問越界 (Access Violation)
    - 追蹤頂層函式 (fn)、結構體關聯方法 (impl Type)、Trait 定義與方法簽名
    - 收錄 struct_item, enum_item, type_item, macro_definition, item-level macro_invocation
    - 支援泛型 impl<T> Trait<U> for Type<T> 精準型別抽取
    - 識別 #CLI: main 進入點與因果調度樹
    - 偵測 panic! / todo! / unimplemented! 執行期未決危害 (Hazards)，包含 token_tree 內巢狀調用
    - 精準計算去註解 (line_comment, block_comment) 之 executable_fingerprint
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

    def _extract_type_name(self, node: Optional[Node], source_bytes: bytes) -> str:
        """
        精準提取 impl<T> Trait for Type<T> 區塊中被實作型別之核心名稱，
        正確解開 reference_type, pointer_type, generic_type 與 scoped_type_identifier。
        """
        if not node:
            return "Anonymous"
        curr = node
        while curr:
            if curr.type in ("reference_type", "pointer_type", "generic_type"):
                inner = curr.child_by_field_name("type")
                if inner:
                    curr = inner
                    continue
            elif curr.type == "scoped_type_identifier":
                name_n = curr.child_by_field_name("name")
                if name_n:
                    return source_bytes[name_n.start_byte:name_n.end_byte].decode("utf-8", errors="replace").strip()
                raw = source_bytes[curr.start_byte:curr.end_byte].decode("utf-8", errors="replace").strip()
                return raw.split("::")[-1].strip()
            elif curr.type in ("type_identifier", "primitive_type"):
                return source_bytes[curr.start_byte:curr.end_byte].decode("utf-8", errors="replace").strip()
            elif curr.type == "tuple_type":
                return source_bytes[curr.start_byte:curr.end_byte].decode("utf-8", errors="replace").strip()
            break
        raw = source_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace").strip()
        return raw.split("<")[0].split("::")[-1].lstrip("&* ").strip() or "Anonymous"

    def _get_leading_attributes(self, node: Node) -> List[Node]:
        """
        收集語法節點前方的所有裝飾屬性（attribute_item，如 #[derive(...)] 或 #[require(...)]），
        跳過夾雜的註解行。
        """
        attrs = []
        curr = node.prev_named_sibling
        while curr and curr.type in ("attribute_item", "line_comment", "block_comment"):
            if curr.type == "attribute_item":
                attrs.append(curr)
            curr = curr.prev_named_sibling
        attrs.reverse()
        return attrs

    def compute_executable_fingerprint(self, node: Any, leading_attrs: Optional[List[Any]] = None) -> str:
        """
        提取 Rust AST 中所有可執行語意與結構宣告之 Token 指紋（去除 line_comment、block_comment）。
        包含前置 attribute_item，回傳正規化的 token 字串 SHA-256 雜湊值。
        """
        if not node:
            return ""
        tokens = []
        nodes = list(reversed(leading_attrs or [])) + [node]
        stack = list(reversed(nodes))
        while stack:
            curr = stack.pop()
            if "comment" in curr.type:
                continue
            if not curr.children:
                txt = curr.text.decode("utf-8", errors="replace").strip()
                if txt:
                    tokens.append(txt)
            else:
                stack.extend(reversed(curr.children))
        combined = " ".join(tokens)
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def _extract_token_tree_macros(self, tt_node: Node) -> List[Tuple[str, int]]:
        """
        走訪 macro_invocation 內部的 token_tree，提取巢狀巨集調用（如 select! 中的 tracing::error! 或 todo!）。
        """
        macros = []
        stack = [tt_node]
        while stack:
            curr = stack.pop()
            children = curr.children
            for i in range(len(children) - 1):
                if children[i + 1].type == "!":
                    parts = []
                    idx = i
                    while idx >= 0 and children[idx].type in ("identifier", "::", "scoped_identifier"):
                        parts.insert(0, children[idx].text.decode("utf-8", errors="replace"))
                        idx -= 1
                    m_name = "".join(parts).strip()
                    if m_name:
                        macros.append((m_name, children[i].start_point[0] + 1))
            for c in reversed(children):
                if c.type == "token_tree":
                    stack.append(c)
        return macros

    def parse_and_build(self, source_code: str, file_path: str = "main.rs") -> CodeMapGraph:
        source_bytes = source_code.encode("utf-8")
        tree = self.parser.parse(source_bytes)
        graph = CodeMapGraph(name=f"Graph of {file_path}")

        # 預先計算換行位元組位移，安全且極速換算行號
        line_starts = [0]
        for i, b in enumerate(source_bytes):
            if b == 10:  # ord('\n')
                line_starts.append(i + 1)

        def get_line(byte_offset: int) -> int:
            return bisect.bisect_right(line_starts, byte_offset)

        def decode_slice(start: int, end: int) -> str:
            return source_bytes[start:end].decode("utf-8", errors="replace")

        defs: Dict[str, str] = {}

        # 階段 1：收集結構宣告、Trait 定義、impl 關聯與函式定義 (Pass 1)
        cursor = tree.walk()
        impl_stack: List[str] = []
        func_depth: int = 0

        while True:
            node = cursor.node
            ntype = node.type

            if ntype == "impl_item":
                t_node = node.child_by_field_name("type")
                impl_name = self._extract_type_name(t_node, source_bytes)
                impl_stack.append(impl_name)

            elif ntype == "trait_item":
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    start_row = get_line(node.start_byte)
                    end_row = get_line(node.end_byte)
                    node_id = f"trait:{raw_name}@{file_path}:L{start_row}"
                    attrs = self._get_leading_attributes(node)
                    slice_start = attrs[0].start_byte if attrs else node.start_byte
                    source_code_slice = decode_slice(slice_start, node.end_byte)

                    defs[raw_name] = node_id

                    graph.add_node_rich(
                        node_id=node_id,
                        label=raw_name,
                        category="MODULE_STATE",
                        scope={"scope_id": "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": f"[Trait] {raw_name}",
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "raw_name": raw_name,
                            "executable_fingerprint": self.compute_executable_fingerprint(node, attrs),
                        },
                    )
                    impl_stack.append(raw_name)

            elif ntype in ("struct_item", "enum_item"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    curr_impl = impl_stack[-1] if impl_stack else None
                    type_prefix = "struct" if ntype == "struct_item" else "enum"
                    start_row = get_line(node.start_byte)
                    end_row = get_line(node.end_byte)
                    node_id = f"{type_prefix}:{raw_name}@{file_path}:L{start_row}"
                    attrs = self._get_leading_attributes(node)
                    slice_start = attrs[0].start_byte if attrs else node.start_byte
                    source_code_slice = decode_slice(slice_start, node.end_byte)

                    defs[raw_name] = node_id

                    graph.add_node_rich(
                        node_id=node_id,
                        label=raw_name,
                        category="MODULE_STATE",
                        scope={"scope_id": curr_impl or "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": f"[{type_prefix.capitalize()}] {raw_name}",
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "raw_name": raw_name,
                            "executable_fingerprint": self.compute_executable_fingerprint(node, attrs),
                        },
                    )

            elif ntype == "type_item":
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    curr_impl = impl_stack[-1] if impl_stack else None
                    start_row = get_line(node.start_byte)
                    end_row = get_line(node.end_byte)
                    node_id = f"type:{raw_name}@{file_path}:L{start_row}"
                    attrs = self._get_leading_attributes(node)
                    slice_start = attrs[0].start_byte if attrs else node.start_byte
                    source_code_slice = decode_slice(slice_start, node.end_byte)

                    defs[raw_name] = node_id

                    graph.add_node_rich(
                        node_id=node_id,
                        label=raw_name,
                        category="MODULE_STATE",
                        scope={"scope_id": curr_impl or "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": f"[Type Alias] {raw_name}",
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "raw_name": raw_name,
                            "executable_fingerprint": self.compute_executable_fingerprint(node, attrs),
                        },
                    )

            elif ntype == "macro_definition":
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    start_row = get_line(node.start_byte)
                    end_row = get_line(node.end_byte)
                    node_id = f"macro:{raw_name}@{file_path}:L{start_row}"
                    attrs = self._get_leading_attributes(node)
                    slice_start = attrs[0].start_byte if attrs else node.start_byte
                    source_code_slice = decode_slice(slice_start, node.end_byte)

                    defs[raw_name] = node_id

                    graph.add_node_rich(
                        node_id=node_id,
                        label=f"{raw_name}!",
                        category="FUNCTION_DEF",
                        scope={"scope_id": "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": f"macro_rules! {raw_name}",
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "raw_name": raw_name,
                            "executable_fingerprint": self.compute_executable_fingerprint(node, attrs),
                        },
                    )

            elif ntype == "macro_invocation" and func_depth == 0:
                macro_node = node.child_by_field_name("macro")
                if macro_node:
                    m_name = decode_slice(macro_node.start_byte, macro_node.end_byte)
                    start_row = get_line(node.start_byte)
                    end_row = get_line(node.end_byte)
                    node_id = f"macro_invoke:{m_name}@{file_path}:L{start_row}"
                    attrs = self._get_leading_attributes(node)
                    slice_start = attrs[0].start_byte if attrs else node.start_byte
                    source_code_slice = decode_slice(slice_start, node.end_byte)

                    graph.add_node_rich(
                        node_id=node_id,
                        label=f"{m_name}! (Item)",
                        category="MODULE_STATE",
                        scope={"scope_id": "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": f"{m_name}! {{ ... }}",
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "macro_name": m_name,
                            "executable_fingerprint": self.compute_executable_fingerprint(node, attrs),
                        },
                    )

            elif ntype in ("function_item", "function_signature_item"):
                if ntype == "function_item":
                    func_depth += 1
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    curr_impl = impl_stack[-1] if impl_stack else None
                    fn_name = f"{curr_impl}::{raw_name}" if curr_impl else raw_name
                    start_row = get_line(node.start_byte)
                    end_row = get_line(node.end_byte)
                    node_id = f"func:{fn_name}@{file_path}:L{start_row}"

                    params_node = node.child_by_field_name("parameters")
                    params = decode_slice(params_node.start_byte, params_node.end_byte) if params_node else "()"
                    sig = f"fn {fn_name}{params}"
                    attrs = self._get_leading_attributes(node)
                    slice_start = attrs[0].start_byte if attrs else node.start_byte
                    source_code_slice = decode_slice(slice_start, node.end_byte)

                    defs[fn_name] = node_id
                    defs[raw_name] = node_id
                    if curr_impl:
                        defs[f"{curr_impl}.{raw_name}"] = node_id

                    is_async = "async" in decode_slice(node.start_byte, min(len(source_bytes), node.start_byte + 30))

                    graph.add_node_rich(
                        node_id=node_id,
                        label=fn_name,
                        category="FUNCTION_DEF",
                        scope={"scope_id": curr_impl or "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": sig,
                            "parameters": params,
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "line_count": max(1, end_row - start_row + 1),
                            "is_async": is_async,
                            "impl_type": curr_impl or "",
                            "raw_name": raw_name,
                            "executable_fingerprint": self.compute_executable_fingerprint(node, attrs),
                        },
                    )

            elif ntype in ("const_item", "static_item"):
                start_row = get_line(node.start_byte)
                end_row = get_line(node.end_byte)
                attrs = self._get_leading_attributes(node)
                slice_start = attrs[0].start_byte if attrs else node.start_byte
                source_code_slice = decode_slice(slice_start, node.end_byte)
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
                        "executable_fingerprint": self.compute_executable_fingerprint(node, attrs),
                    },
                )

            if cursor.goto_first_child():
                continue

            # 葉節點離開
            if ntype in ("impl_item", "trait_item") and impl_stack:
                impl_stack.pop()
            if ntype == "function_item":
                func_depth = max(0, func_depth - 1)

            if cursor.goto_next_sibling():
                continue

            # 回溯父節點
            found = False
            while cursor.goto_parent():
                p_type = cursor.node.type
                if p_type in ("impl_item", "trait_item") and impl_stack:
                    impl_stack.pop()
                if p_type == "function_item":
                    func_depth = max(0, func_depth - 1)
                if cursor.goto_next_sibling():
                    found = True
                    break
            if not found:
                break

        # 階段 2：走訪呼叫點與巨集 (Pass 2)
        cursor = tree.walk()
        impl_stack = []
        func_stack: List[Tuple[str, str, Optional[str]]] = []

        while True:
            node = cursor.node
            ntype = node.type

            if ntype == "impl_item":
                t_node = node.child_by_field_name("type")
                impl_name = self._extract_type_name(t_node, source_bytes)
                impl_stack.append(impl_name)

            elif ntype == "trait_item":
                name_node = node.child_by_field_name("name")
                trait_name = decode_slice(name_node.start_byte, name_node.end_byte) if name_node else "Anonymous"
                impl_stack.append(trait_name)

            elif ntype == "function_item":
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    curr_impl = impl_stack[-1] if impl_stack else None
                    fn_name = f"{curr_impl}::{raw_name}" if curr_impl else raw_name
                    start_row = get_line(node.start_byte)
                    caller_id = f"func:{fn_name}@{file_path}:L{start_row}"
                    func_stack.append((caller_id, fn_name, curr_impl))

            elif ntype == "macro_invocation" and func_stack:
                caller_id, caller_fn, curr_impl = func_stack[-1]
                macro_node = node.child_by_field_name("macro")
                if macro_node:
                    m_name = decode_slice(macro_node.start_byte, macro_node.end_byte)
                    m_row = get_line(node.start_byte)

                    if m_name in ("panic", "todo", "unimplemented") or m_name.endswith(("::panic", "::todo", "::unimplemented")):
                        hazard_type = m_name.split("::")[-1]
                        hazard_id = f"hazard:{hazard_type}@{file_path}:L{m_row}"
                        graph.add_node_rich(
                            node_id=hazard_id,
                            label=f"{hazard_type}! [未完成實作/執行期中斷]",
                            category="FUNCTION_DEF",
                            scope={"scope_id": curr_impl or "scope:global", "file": file_path, "line": m_row},
                            props={"hazard": f"RUST_{hazard_type.upper()}", "is_blocking": True},
                        )
                        graph.add_edge_rich(
                            caller_id,
                            hazard_id,
                            edge_type="CALLS",
                            status="BLOCKED_INVARIANT",
                            detail=f"呼叫了未完成實作或執行期中斷巨集: {hazard_type}!()",
                        )
                    else:
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
                            caller_id,
                            target_id,
                            edge_type="CALLS",
                            status="VALID",
                            detail="調用標準庫或外部巨集",
                        )

                    # 針對 select!, join!, format!, println! 等包含 token_tree 區塊的巢狀巨集進一步解析
                    tt_child = None
                    for ch in node.children:
                        if ch.type == "token_tree":
                            tt_child = ch
                            break
                    if tt_child:
                        nested_macros = self._extract_token_tree_macros(tt_child)
                        for sub_name, sub_row in nested_macros:
                            if sub_name in ("panic", "todo", "unimplemented") or sub_name.endswith(("::panic", "::todo", "::unimplemented")):
                                h_type = sub_name.split("::")[-1]
                                h_id = f"hazard:{h_type}@{file_path}:L{sub_row}"
                                graph.add_node_rich(
                                    node_id=h_id,
                                    label=f"{h_type}! [未完成實作/執行期中斷]",
                                    category="FUNCTION_DEF",
                                    scope={"scope_id": curr_impl or "scope:global", "file": file_path, "line": sub_row},
                                    props={"hazard": f"RUST_{h_type.upper()}", "is_blocking": True},
                                )
                                graph.add_edge_rich(
                                    caller_id,
                                    h_id,
                                    edge_type="CALLS",
                                    status="BLOCKED_INVARIANT",
                                    detail=f"呼叫了未完成實作或執行期中斷巨集: {h_type}!()",
                                )
                            else:
                                sub_target = f"macro:{sub_name}!@external"
                                if sub_target not in graph.g:
                                    graph.add_node_rich(
                                        node_id=sub_target,
                                        label=f"{sub_name}! (Macro)",
                                        category="FUNCTION_DEF",
                                        scope={"scope_id": "external", "file": file_path, "line": 0},
                                        props={"signature": f"{sub_name}!()", "source_code": ""},
                                    )
                                graph.add_edge_rich(
                                    caller_id,
                                    sub_target,
                                    edge_type="CALLS",
                                    status="VALID",
                                    detail="調用巢狀巨集",
                                )

            elif ntype == "call_expression" and func_stack:
                caller_id, caller_fn, curr_impl = func_stack[-1]
                fn_node = node.child_by_field_name("function")
                if fn_node:
                    target_text = decode_slice(fn_node.start_byte, fn_node.end_byte)
                    clean_fn = fn_node
                    if clean_fn.type == "generic_function":
                        inner = clean_fn.child_by_field_name("function")
                        if inner:
                            clean_fn = inner

                    method_name = ""
                    path_prefix = ""
                    if clean_fn.type == "field_expression":
                        field_n = clean_fn.child_by_field_name("field")
                        if field_n:
                            method_name = decode_slice(field_n.start_byte, field_n.end_byte).strip()
                    elif clean_fn.type == "scoped_identifier":
                        name_n = clean_fn.child_by_field_name("name")
                        path_n = clean_fn.child_by_field_name("path")
                        if name_n:
                            method_name = decode_slice(name_n.start_byte, name_n.end_byte).strip()
                        if path_n:
                            path_prefix = decode_slice(path_n.start_byte, path_n.end_byte).strip()
                    elif clean_fn.type == "identifier":
                        method_name = decode_slice(clean_fn.start_byte, clean_fn.end_byte).strip()

                    if not method_name:
                        method_name = target_text.split(".")[-1].split("::")[-1].strip()

                    target_def_id = None
                    if path_prefix == "Self" and curr_impl and f"{curr_impl}::{method_name}" in defs:
                        target_def_id = defs[f"{curr_impl}::{method_name}"]
                    elif target_text in defs:
                        target_def_id = defs[target_text]
                    elif curr_impl and f"{curr_impl}::{method_name}" in defs:
                        target_def_id = defs[f"{curr_impl}::{method_name}"]
                    elif method_name in defs:
                        target_def_id = defs[method_name]

                    if not target_def_id:
                        clean_label = f"{path_prefix}::{method_name}" if path_prefix else method_name
                        ext_id = f"func:{clean_label}@external"
                        if ext_id not in graph.g:
                            graph.add_node_rich(
                                node_id=ext_id,
                                label=f"{clean_label} (External/Unresolved)",
                                category="FUNCTION_DEF",
                                scope={"scope_id": "external", "file": file_path, "line": 0},
                                props={"signature": f"{clean_label}()", "source_code": ""},
                            )
                        target_def_id = ext_id

                    is_await = b".await" in source_bytes[node.start_byte:node.end_byte]
                    graph.add_edge_rich(
                        caller_id,
                        target_def_id,
                        edge_type="CALLS",
                        status="VALID",
                        detail="調用函式或結構體方法",
                        flow_type="ASYNC" if is_await else "SYNC",
                    )

            if cursor.goto_first_child():
                continue

            if ntype in ("impl_item", "trait_item") and impl_stack:
                impl_stack.pop()
            if ntype == "function_item" and func_stack:
                func_stack.pop()

            if cursor.goto_next_sibling():
                continue

            found = False
            while cursor.goto_parent():
                p_type = cursor.node.type
                if p_type in ("impl_item", "trait_item") and impl_stack:
                    impl_stack.pop()
                if p_type == "function_item" and func_stack:
                    func_stack.pop()
                if cursor.goto_next_sibling():
                    found = True
                    break
            if not found:
                break

        # 階段 3：若包含 fn main()，自動註冊 CLI 程式入口錨點
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
