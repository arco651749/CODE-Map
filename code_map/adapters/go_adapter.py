import bisect
import hashlib
import re
from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_go as tsgo

from code_map.core.base_adapter import BaseCodeMapBuilder
from code_map.core.graph import CodeMapGraph


class GoCodeMapBuilder(BaseCodeMapBuilder):
    """
    基於 Tree-sitter TreeCursor 的高效穩定 Go 語意控制樹建構器
    - 採用 TreeCursor 走訪與位元組索引切片，避免 Windows C 擴充記憶體訪問越界 (Access Violation)
    - 追蹤頂層函式 (func)、結構體接收器方法 (func (r *Receiver[T]) Method)、結構體 (struct)、介面 (interface) 與型別別名
    - 解開並精確追蹤單行與群組化 const / var 規格 (const_spec, var_spec)
    - 識別 #CLI: main 進入點、HTTP 路由註冊與 Goroutine 非同步調度
    - 偵測 panic() 未決恐慌與 time.Sleep() 同步阻塞危害 (Hazards)
    """

    @property
    def supported_extensions(self) -> Set[str]:
        return {".go"}

    @property
    def language_name(self) -> str:
        return "Go"

    def __init__(self):
        self.language = Language(tsgo.language())
        self.parser = Parser(self.language)

    def compute_executable_fingerprint(self, node: Optional[Node]) -> str:
        """
        Go 語意專用 Token 指紋計算器：
        - 徹底剔除各類註解 (comment, line_comment, block_comment) 與純空白
        - 保留結構體欄位 (struct fields)、結構體標籤 (raw_string_literal tags)、介面方法簽章 (interface methods)
        - 保留常數/變數規格 (const_spec, var_spec) 與型別別名 (type_alias, type_spec)
        - 產生正規化 SHA-256 雜湊
        """
        if not node:
            return ""
        tokens = []
        stack = [node]
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

    def parse_and_build(self, source_code: str, file_path: str = "main.go") -> CodeMapGraph:
        # 保持 source_bytes 於局部變數生命週期內，防止 PyMalloc 記憶體重用
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

        def extract_receiver_type(node: Node) -> Optional[str]:
            recv_node = node.child_by_field_name("receiver")
            if not recv_node:
                return None
            for child in recv_node.children:
                if child.type == "parameter_declaration":
                    t_node = child.child_by_field_name("type") or child
                    while t_node:
                        if t_node.type == "pointer_type":
                            t_node = t_node.child_by_field_name("type") or (t_node.children[-1] if t_node.children else None)
                        elif t_node.type == "generic_type":
                            t_node = t_node.child_by_field_name("type") or (t_node.children[0] if t_node.children else None)
                        elif t_node.type == "type_identifier":
                            return decode_slice(t_node.start_byte, t_node.end_byte)
                        else:
                            for sub in child.children:
                                if sub.type == "type_identifier":
                                    return decode_slice(sub.start_byte, sub.end_byte)
                            break
            raw = decode_slice(recv_node.start_byte, recv_node.end_byte)
            raw = re.sub(r"\[.*?\]", "", raw.strip("() "))
            parts = raw.split()
            if len(parts) >= 2:
                return parts[-1].lstrip("*& ")
            elif len(parts) == 1:
                return parts[0].lstrip("*& ")
            return None

        defs: Dict[str, str] = {}

        def advance_skipping_children(cur) -> bool:
            if cur.goto_next_sibling():
                return True
            while cur.goto_parent():
                if cur.goto_next_sibling():
                    return True
            return False

        # 階段 1：收集所有函式宣告、結構體接收器方法、型別與模組狀態
        cursor = tree.walk()
        while True:
            node = cursor.node
            ntype = node.type

            if ntype in ("function_declaration", "method_declaration"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    recv_type = extract_receiver_type(node)
                    fn_name = f"{recv_type}.{raw_name}" if recv_type else raw_name
                    start_row = get_line(node.start_byte)
                    end_row = get_line(node.end_byte)
                    node_id = f"func:{fn_name}@{file_path}:L{start_row}"

                    params_node = node.child_by_field_name("parameters")
                    params = decode_slice(params_node.start_byte, params_node.end_byte) if params_node else "()"
                    sig = f"func {fn_name}{params}"
                    source_code_slice = decode_slice(node.start_byte, node.end_byte)

                    defs[fn_name] = node_id
                    defs[raw_name] = node_id

                    graph.add_node_rich(
                        node_id=node_id,
                        label=fn_name,
                        category="FUNCTION_DEF",
                        scope={"scope_id": recv_type or "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": sig,
                            "parameters": params,
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "line_count": max(1, end_row - start_row + 1),
                            "receiver_type": recv_type or "",
                            "raw_name": raw_name,
                            "executable_fingerprint": self.compute_executable_fingerprint(node),
                        },
                    )
                if advance_skipping_children(cursor):
                    continue
                break

            elif ntype in ("type_spec", "type_alias"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    start_row = get_line(node.start_byte)
                    end_row = get_line(node.end_byte)
                    source_code_slice = decode_slice(node.start_byte, node.end_byte)
                    node_id = f"type:{raw_name}@{file_path}:L{start_row}"

                    type_kind = "alias" if ntype == "type_alias" else "type"
                    if ntype == "type_spec":
                        for sub in node.children:
                            if sub.type == "struct_type":
                                type_kind = "struct"
                                break
                            elif sub.type == "interface_type":
                                type_kind = "interface"
                                break

                    defs[raw_name] = node_id

                    graph.add_node_rich(
                        node_id=node_id,
                        label=raw_name,
                        category="MODULE_STATE",
                        scope={"scope_id": "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": f"[{type_kind.capitalize()}] {raw_name}",
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "raw_name": raw_name,
                            "type_kind": type_kind,
                            "executable_fingerprint": self.compute_executable_fingerprint(node),
                        },
                    )
                if advance_skipping_children(cursor):
                    continue
                break

            elif ntype in ("const_spec", "var_spec"):
                start_row = get_line(node.start_byte)
                end_row = get_line(node.end_byte)
                source_code_slice = decode_slice(node.start_byte, node.end_byte)

                p_type = node.parent.type if node.parent else ""
                if p_type == "var_spec_list" and node.parent.parent:
                    p_type = node.parent.parent.type
                prefix = "const" if "const" in p_type else "var"

                id_nodes = [c for c in node.children if c.type == "identifier"]
                if not id_nodes:
                    name_node = node.child_by_field_name("name")
                    if name_node:
                        id_nodes = [name_node]

                fp = self.compute_executable_fingerprint(node)

                if not id_nodes:
                    var_name = f"{prefix}_{start_row}"
                    state_id = f"state:{var_name}@{file_path}:L{start_row}"
                    defs[var_name] = state_id
                    graph.add_node_rich(
                        node_id=state_id,
                        label=var_name,
                        category="MODULE_STATE",
                        scope={"scope_id": "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": f"[Module State] {prefix} {var_name}",
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "raw_name": var_name,
                            "executable_fingerprint": fp,
                        },
                    )
                else:
                    for id_n in id_nodes:
                        var_name = decode_slice(id_n.start_byte, id_n.end_byte)
                        if var_name == "_":
                            type_n = node.child_by_field_name("type")
                            val_n = node.child_by_field_name("value")
                            extra = ""
                            if type_n:
                                extra = decode_slice(type_n.start_byte, type_n.end_byte).strip()
                            if val_n:
                                val_txt = decode_slice(val_n.start_byte, val_n.end_byte).strip()
                                extra = f"{extra}={val_txt}" if extra else val_txt
                            var_name = f"_ ({extra})" if extra else f"_{get_line(id_n.start_byte)}"

                        state_id = f"state:{var_name}@{file_path}:L{start_row}"
                        defs[var_name] = state_id
                        graph.add_node_rich(
                            node_id=state_id,
                            label=var_name,
                            category="MODULE_STATE",
                            scope={"scope_id": "scope:global", "file": file_path, "line": start_row},
                            props={
                                "signature": f"[Module State] {prefix} {var_name}",
                                "source_code": source_code_slice,
                                "line_start": start_row,
                                "line_end": end_row,
                                "raw_name": var_name,
                                "executable_fingerprint": fp,
                            },
                        )
                if advance_skipping_children(cursor):
                    continue
                break

            if cursor.goto_first_child():
                continue

            if cursor.goto_next_sibling():
                continue

            found = False
            while cursor.goto_parent():
                if cursor.goto_next_sibling():
                    found = True
                    break
            if not found:
                break

        # 階段 2：走訪呼叫點與危害接線 (Pass 2)
        cursor = tree.walk()
        func_stack: List[Tuple[str, str, Optional[str]]] = []
        goroutine_stack: List[bool] = []

        while True:
            node = cursor.node
            ntype = node.type

            if ntype in ("function_declaration", "method_declaration"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    recv_type = extract_receiver_type(node)
                    fn_name = f"{recv_type}.{raw_name}" if recv_type else raw_name
                    start_row = get_line(node.start_byte)
                    caller_id = f"func:{fn_name}@{file_path}:L{start_row}"
                    func_stack.append((caller_id, fn_name, recv_type))

            elif ntype == "go_statement":
                goroutine_stack.append(True)

            elif ntype == "call_expression" and func_stack:
                caller_id, caller_fn, curr_recv = func_stack[-1]
                fn_node = node.child_by_field_name("function")
                if fn_node:
                    call_text = decode_slice(fn_node.start_byte, fn_node.end_byte)
                    call_row = get_line(node.start_byte)
                    is_async = len(goroutine_stack) > 0

                    if call_text == "panic":
                        hazard_id = f"hazard:panic@{file_path}:L{call_row}"
                        graph.add_node_rich(
                            node_id=hazard_id,
                            label="panic() [執行期恐慌/中斷]",
                            category="FUNCTION_DEF",
                            scope={"scope_id": curr_recv or "scope:global", "file": file_path, "line": call_row},
                            props={"hazard": "GO_PANIC", "is_blocking": True},
                        )
                        graph.add_edge_rich(
                            caller_id,
                            hazard_id,
                            edge_type="CALLS",
                            status="BLOCKED_INVARIANT",
                            detail="呼叫了執行期恐慌中斷常式: panic()",
                            flow_type="ASYNC" if is_async else "SYNC",
                        )
                    elif "time.Sleep" in call_text:
                        hazard_id = f"hazard:time.Sleep@{file_path}:L{call_row}"
                        graph.add_node_rich(
                            node_id=hazard_id,
                            label="time.Sleep() [同步休眠/介面凍結]",
                            category="FUNCTION_DEF",
                            scope={"scope_id": curr_recv or "scope:global", "file": file_path, "line": call_row},
                            props={"hazard": "GO_BLOCKING_SLEEP", "is_blocking": True},
                        )
                        graph.add_edge_rich(
                            caller_id,
                            hazard_id,
                            edge_type="CALLS",
                            status="BLOCKED_INVARIANT",
                            detail="呼叫了同步阻塞常式: time.Sleep()",
                            flow_type="ASYNC" if is_async else "SYNC",
                        )
                    else:
                        method_name = call_text.split(".")[-1]
                        target_def_id = None
                        if call_text in defs:
                            target_def_id = defs[call_text]
                        elif curr_recv and f"{curr_recv}.{method_name}" in defs:
                            target_def_id = defs[f"{curr_recv}.{method_name}"]
                        elif method_name in defs:
                            target_def_id = defs[method_name]

                        if not target_def_id:
                            ext_id = f"func:{call_text}@external"
                            if ext_id not in graph.g:
                                graph.add_node_rich(
                                    node_id=ext_id,
                                    label=f"{call_text} (External/Pkg)",
                                    category="FUNCTION_DEF",
                                    scope={"scope_id": "external", "file": file_path, "line": 0},
                                    props={"signature": f"{call_text}()", "source_code": ""},
                                )
                            target_def_id = ext_id

                        graph.add_edge_rich(
                            caller_id,
                            target_def_id,
                            edge_type="CALLS",
                            status="VALID",
                            detail="調用標準庫或外部 Go 套件",
                            flow_type="ASYNC" if is_async else "SYNC",
                        )

                        # 檢查是否為 HTTP 路由註冊或 Cobra 命令掛載 (e.g. router.GET, HandleFunc, AddCommand)
                        ROUTER_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "Any", "HandleFunc", "Handle", "AddCommand"}
                        if method_name in ROUTER_METHODS:
                            args_node = node.child_by_field_name("arguments")
                            if args_node:
                                for arg in args_node.children:
                                    if arg.type == "identifier":
                                        arg_name = decode_slice(arg.start_byte, arg.end_byte)
                                        if arg_name in defs and defs[arg_name] != target_def_id:
                                            graph.add_edge_rich(
                                                caller_id,
                                                defs[arg_name],
                                                edge_type="WIRES_TO" if method_name == "AddCommand" else "TRIGGERS",
                                                status="VALID",
                                                detail=f"註冊路由或指令處理常式: {arg_name}",
                                                flow_type="SYNC",
                                            )

            if cursor.goto_first_child():
                continue

            if ntype in ("function_declaration", "method_declaration") and func_stack:
                func_stack.pop()
            if ntype == "go_statement" and goroutine_stack:
                goroutine_stack.pop()

            if cursor.goto_next_sibling():
                continue

            found = False
            while cursor.goto_parent():
                p_type = cursor.node.type
                if p_type in ("function_declaration", "method_declaration") and func_stack:
                    func_stack.pop()
                if p_type == "go_statement" and goroutine_stack:
                    goroutine_stack.pop()
                if cursor.goto_next_sibling():
                    found = True
                    break
            if not found:
                break

        # 階段 3：若包含 func main()，自動註冊 CLI 程式入口錨點
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
                    "source_code": "func main() { ... }",
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
