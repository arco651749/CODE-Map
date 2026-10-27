import bisect
from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_c_sharp as tscs

from code_map.core.base_adapter import BaseCodeMapBuilder
from code_map.core.graph import CodeMapGraph


class CSharpCodeMapBuilder(BaseCodeMapBuilder):
    """
    基於 Tree-sitter TreeCursor 的高效穩定 C# 語意控制樹建構器
    - 採用 TreeCursor 走訪與位元組索引切片，避免 Windows C 擴充記憶體訪問越界 (Access Violation)
    - 追蹤命名空間、類別/結構體方法 (Class.Method)、建構子與本機函式
    - 識別 WPF/WinUI 事件綁定 (btn.Click += OnClick) 與 CLI Main 進入點
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

    def parse_and_build(self, source_code: str, file_path: str = "Program.cs") -> CodeMapGraph:
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

        defs: Dict[str, str] = {}
        graph.g.graph["exports"] = {}
        graph.g.graph["imports"] = []

        # 階段 1：收集類別宣告與方法/建構子定義
        cursor = tree.walk()
        class_stack: List[str] = []

        while True:
            node = cursor.node
            ntype = node.type

            if ntype in ("class_declaration", "struct_declaration", "record_declaration", "interface_declaration"):
                name_node = node.child_by_field_name("name")
                class_name = decode_slice(name_node.start_byte, name_node.end_byte) if name_node else "AnonymousClass"
                class_stack.append(class_name)

            elif ntype in ("method_declaration", "constructor_declaration", "local_function_statement"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    curr_class = class_stack[-1] if class_stack else None
                    fn_name = f"{curr_class}.{raw_name}" if curr_class else raw_name
                    start_row = get_line(node.start_byte)
                    end_row = get_line(node.end_byte)
                    node_id = f"func:{fn_name}@{file_path}:L{start_row}"

                    params_node = node.child_by_field_name("parameters")
                    params = decode_slice(params_node.start_byte, params_node.end_byte) if params_node else "()"
                    sig = f"{fn_name}{params}"
                    source_code_slice = decode_slice(node.start_byte, node.end_byte)

                    # 偵測 CommunityToolkit.Mvvm [RelayCommand] 裝飾器
                    is_relay_cmd = "RelayCommand" in source_code_slice.split(raw_name)[0]
                    base_cmd_name = raw_name[:-5] if (raw_name.endswith("Async") and len(raw_name) > 5) else raw_name
                    relay_cmd_name = f"{base_cmd_name}Command" if is_relay_cmd else ""

                    defs[fn_name] = node_id
                    defs[raw_name] = node_id
                    graph.g.graph["exports"][raw_name] = node_id
                    graph.g.graph["exports"][fn_name] = node_id

                    if is_relay_cmd:
                        defs[relay_cmd_name] = node_id
                        if curr_class:
                            defs[f"{curr_class}.{relay_cmd_name}"] = node_id
                        graph.g.graph["exports"][relay_cmd_name] = node_id

                    graph.add_node_rich(
                        node_id=node_id,
                        label=fn_name,
                        category="FUNCTION_DEF",
                        scope={"scope_id": curr_class or "scope:global", "file": file_path, "line": start_row},
                        props={
                            "signature": f"[RelayCommand -> {relay_cmd_name}] {sig}" if is_relay_cmd else sig,
                            "parameters": params,
                            "source_code": source_code_slice,
                            "line_start": start_row,
                            "line_end": end_row,
                            "line_count": max(1, end_row - start_row + 1),
                            "class_name": curr_class or "",
                            "raw_name": raw_name,
                            "relay_command": relay_cmd_name,
                            "executable_fingerprint": self.compute_executable_fingerprint(node),
                        },
                    )

            elif ntype in ("field_declaration", "constant_declaration", "property_declaration"):
                curr_class = class_stack[-1] if class_stack else None
                start_row = get_line(node.start_byte)
                end_row = get_line(node.end_byte)
                source_code_slice = decode_slice(node.start_byte, node.end_byte)
                
                # 提取屬性或欄位名稱
                name_node = node.child_by_field_name("name")
                if name_node:
                    var_name = decode_slice(name_node.start_byte, name_node.end_byte)
                else:
                    head_part = source_code_slice.split("=")[0].split("{")[0].strip().rstrip(";")
                    var_name = head_part.split()[-1] if head_part.split() else f"state_{start_row}"
                var_name = var_name.strip(";")

                # 偵測 CommunityToolkit.Mvvm [ObservableProperty] 自動生成屬性 (例如 _userName -> UserName)
                is_observable_prop = "ObservableProperty" in source_code_slice
                generated_prop_name = ""
                if is_observable_prop:
                    clean_field = var_name.lstrip("_")
                    if clean_field.startswith("m_") and len(clean_field) > 2:
                        clean_field = clean_field[2:]
                    if clean_field:
                        generated_prop_name = clean_field[0].upper() + clean_field[1:]

                state_id = f"state:{var_name}@{file_path}:L{start_row}"
                category = "FUNCTION_DEF" if (ntype == "property_declaration" and ("=>" in source_code_slice or "{" in source_code_slice)) or is_observable_prop else "MODULE_STATE"
                graph.add_node_rich(
                    node_id=state_id,
                    label=f"{var_name} (-> {generated_prop_name})" if generated_prop_name else var_name,
                    category=category,
                    scope={"scope_id": curr_class or "scope:global", "file": file_path, "line": start_row},
                    props={
                        "signature": f"[ObservableProperty -> {generated_prop_name}] {var_name}" if is_observable_prop else f"[{'Property' if ntype == 'property_declaration' else 'Module State'}] {var_name}",
                        "source_code": source_code_slice,
                        "line_start": start_row,
                        "line_end": end_row,
                        "line_count": max(1, end_row - start_row + 1),
                        "class_name": curr_class or "",
                        "raw_name": var_name,
                        "generated_property": generated_prop_name,
                        "executable_fingerprint": self.compute_executable_fingerprint(node),
                    }
                )
                defs[var_name] = state_id
                graph.g.graph["exports"][var_name] = state_id
                if generated_prop_name:
                    defs[generated_prop_name] = state_id
                    graph.g.graph["exports"][generated_prop_name] = state_id

            if cursor.goto_first_child():
                continue

            if ntype in ("class_declaration", "struct_declaration", "record_declaration", "interface_declaration") and class_stack:
                class_stack.pop()

            if cursor.goto_next_sibling():
                continue

            found = False
            while cursor.goto_parent():
                p_type = cursor.node.type
                if p_type in ("class_declaration", "struct_declaration", "record_declaration", "interface_declaration") and class_stack:
                    class_stack.pop()
                if cursor.goto_next_sibling():
                    found = True
                    break
            if not found:
                break

        # 階段 2：收集 UI 事件綁定 (btn.Click += OnClick) 與呼叫接線 (Pass 2)
        cursor = tree.walk()
        class_stack = []
        func_stack: List[Tuple[str, str, Optional[str]]] = []

        while True:
            node = cursor.node
            ntype = node.type

            if ntype in ("class_declaration", "struct_declaration", "record_declaration", "interface_declaration"):
                name_node = node.child_by_field_name("name")
                class_name = decode_slice(name_node.start_byte, name_node.end_byte) if name_node else "AnonymousClass"
                class_stack.append(class_name)

            elif ntype in ("method_declaration", "constructor_declaration", "local_function_statement"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    raw_name = decode_slice(name_node.start_byte, name_node.end_byte)
                    curr_class = class_stack[-1] if class_stack else None
                    fn_name = f"{curr_class}.{raw_name}" if curr_class else raw_name
                    start_row = get_line(node.start_byte)
                    caller_id = f"func:{fn_name}@{file_path}:L{start_row}"
                    func_stack.append((caller_id, fn_name, curr_class))

            elif ntype == "assignment_expression":
                assign_slice = decode_slice(node.start_byte, min(len(source_bytes), node.start_byte + 100))
                if "+=" in assign_slice:
                    left_node = node.child_by_field_name("left")
                    right_node = node.child_by_field_name("right")
                    if left_node and right_node:
                        left_text = decode_slice(left_node.start_byte, left_node.end_byte)
                        right_text = decode_slice(right_node.start_byte, right_node.end_byte)
                        line_no = get_line(node.start_byte)

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
                                    scope={"scope_id": class_stack[-1] if class_stack else "scope:global", "file": file_path, "line": line_no},
                                    props={
                                        "ui_type": "Button / UI Control",
                                        "source_code": decode_slice(node.start_byte, node.end_byte),
                                        "line_start": line_no,
                                        "line_end": line_no,
                                    },
                                )

                            evt_id = f"event:{ctrl_name}.{evt_name}@{file_path}:L{line_no}"
                            graph.add_node_rich(
                                node_id=evt_id,
                                label=f"{evt_name}()",
                                category="EVENT_BINDING",
                                scope={"scope_id": class_stack[-1] if class_stack else "scope:global", "file": file_path, "line": line_no},
                                props={"event": evt_name},
                            )
                            graph.add_edge_rich(ctrl_id, evt_id, edge_type="WIRES_TO", status="VALID")

                            handler_name = right_text.split(".")[-1]
                            curr_class = class_stack[-1] if class_stack else None
                            target_id = defs.get(handler_name) or (defs.get(f"{curr_class}.{handler_name}") if curr_class else None)
                            if target_id:
                                graph.add_edge_rich(
                                    evt_id,
                                    target_id,
                                    edge_type="TRIGGERS",
                                    status="VALID",
                                    detail="C# 事件訂閱觸發",
                                )

            elif ntype == "throw_statement" and func_stack:
                throw_text = decode_slice(node.start_byte, node.end_byte)
                line_no = get_line(node.start_byte)
                if "NotImplementedException" in throw_text:
                    caller_id, caller_fn, curr_class = func_stack[-1]
                    hazard_id = f"hazard:NotImplementedException@{file_path}:L{line_no}"
                    graph.add_node_rich(
                        node_id=hazard_id,
                        label="NotImplementedException [未完成實作危害]",
                        category="FUNCTION_DEF",
                        scope={"scope_id": curr_class or "scope:global", "file": file_path, "line": line_no},
                        props={"hazard": "CSHARP_NOT_IMPLEMENTED", "is_blocking": True},
                    )
                    graph.add_edge_rich(
                        caller_id,
                        hazard_id,
                        edge_type="CALLS",
                        status="BLOCKED_INVARIANT",
                        detail="拋出了未完成實作例外: NotImplementedException",
                    )

            elif ntype == "invocation_expression" and func_stack:
                caller_id, caller_fn, curr_class = func_stack[-1]
                fn_node = node.child_by_field_name("function")
                if fn_node:
                    call_text = decode_slice(fn_node.start_byte, fn_node.end_byte)
                    line_no = get_line(node.start_byte)

                    # 1. Avalonia / WPF 專屬事件接線: button.AddHandler(Button.ClickEvent, OnClick)
                    if "AddHandler" in call_text:
                        args_node = node.child_by_field_name("arguments")
                        if args_node and len(args_node.children) >= 3:
                            arg_text = decode_slice(args_node.start_byte, args_node.end_byte)
                            # 提取 receiver (例如 button) 與 handler (例如 OnClick)
                            ctrl_name = call_text.split(".")[0].strip("?")
                            ctrl_id = f"ctrl:#{ctrl_name}@{file_path}:L{line_no}"
                            if ctrl_id not in graph.g:
                                graph.add_node_rich(
                                    node_id=ctrl_id,
                                    label=f"#{ctrl_name}",
                                    category="UI_CONTROL",
                                    scope={"scope_id": curr_class or "scope:global", "file": file_path, "line": line_no},
                                    props={"ui_type": "Avalonia Control", "source_code": decode_slice(node.start_byte, node.end_byte), "line_start": line_no, "line_end": line_no},
                                )
                            evt_id = f"event:{ctrl_name}.AddHandler@{file_path}:L{line_no}"
                            graph.add_node_rich(
                                node_id=evt_id,
                                label=f"AddHandler({arg_text.split(',')[0].strip('() ')})",
                                category="EVENT_BINDING",
                                scope={"scope_id": curr_class or "scope:global", "file": file_path, "line": line_no},
                                props={"event": "AddHandler"},
                            )
                            graph.add_edge_rich(ctrl_id, evt_id, edge_type="WIRES_TO", status="VALID")
                            handler_candidate = arg_text.split(",")[-1].strip("() \r\n\t")
                            handler_name = handler_candidate.split(".")[-1]
                            target_id = defs.get(handler_name) or (defs.get(f"{curr_class}.{handler_name}") if curr_class else None)
                            if target_id:
                                graph.add_edge_rich(evt_id, target_id, edge_type="TRIGGERS", status="VALID", detail="Avalonia AddHandler 事件接線")

                    # 2. C# / GUI 同步執行緒凍結與跨執行緒 UI 存取危害偵測
                    if call_text in ("Task.Run", "ThreadPool.QueueUserWorkItem") or call_text.endswith(".Task.Run"):
                        full_inv_text = decode_slice(node.start_byte, node.end_byte)
                        ui_mutation_markers = (
                            ".Text =", ".Text=", ".Content =", ".Content=",
                            ".IsVisible =", ".IsVisible=", ".Visibility =", ".Visibility=",
                            ".Items.Add(", ".Items.Clear(", ".Children.Add(", ".InvalidateVisual(",
                        )
                        dispatcher_guards = (
                            "Dispatcher.UIThread", "Dispatcher.Invoke", "Dispatcher.BeginInvoke",
                        )
                        if any(m in full_inv_text for m in ui_mutation_markers) and not any(g in full_inv_text for g in dispatcher_guards):
                            hazard_id = f"hazard:CrossThreadUIAccess@{file_path}:L{line_no}"
                            graph.add_node_rich(
                                node_id=hazard_id,
                                label=f"{call_text}() [跨執行緒直接操作 UI 崩潰危害]",
                                category="FUNCTION_DEF",
                                scope={"scope_id": curr_class or "scope:global", "file": file_path, "line": line_no},
                                props={"hazard": "CSHARP_CROSS_THREAD_UI", "is_blocking": True},
                            )
                            graph.add_edge_rich(
                                caller_id,
                                hazard_id,
                                edge_type="CALLS",
                                status="BLOCKED_INVARIANT",
                                detail="在背景執行緒 (Task.Run) 未經 Dispatcher.UIThread 直接存取或修改 UI 控制項，執行期將拋出 InvalidOperationException",
                            )

                    if "Thread.Sleep" in call_text:
                        hazard_id = f"hazard:Thread.Sleep@{file_path}:L{line_no}"
                        graph.add_node_rich(
                            node_id=hazard_id,
                            label="Thread.Sleep() [同步休眠/UI凍結]",
                            category="FUNCTION_DEF",
                            scope={"scope_id": curr_class or "scope:global", "file": file_path, "line": line_no},
                            props={"hazard": "CSHARP_THREAD_SLEEP", "is_blocking": True},
                        )
                        graph.add_edge_rich(
                            caller_id,
                            hazard_id,
                            edge_type="CALLS",
                            status="BLOCKED_INVARIANT",
                            detail="呼叫了 Thread.Sleep() 同步阻塞 UI 執行緒",
                        )
                    elif any(call_text.endswith(k) for k in (".GetAwaiter().GetResult", ".Wait", ".Result")) or ".GetAwaiter().GetResult" in call_text:
                        hazard_id = f"hazard:AsyncSyncDeadlock@{file_path}:L{line_no}"
                        graph.add_node_rich(
                            node_id=hazard_id,
                            label=f"{call_text} [非同步同步化死鎖危害]",
                            category="FUNCTION_DEF",
                            scope={"scope_id": curr_class or "scope:global", "file": file_path, "line": line_no},
                            props={"hazard": "CSHARP_ASYNC_SYNC_DEADLOCK", "is_blocking": True},
                        )
                        graph.add_edge_rich(
                            caller_id,
                            hazard_id,
                            edge_type="CALLS",
                            status="BLOCKED_INVARIANT",
                            detail=f"呼叫了 {call_text}，存在 UI 執行緒非同步死鎖風險",
                        )
                    else:
                        # 3. 鏈式與 Null-conditional 調用正規化
                        clean_call = call_text.replace("?.", ".").replace("!.", ".")
                        method_name = clean_call.split(".")[-1]
                        target_id = defs.get(clean_call) or (defs.get(f"{curr_class}.{method_name}") if curr_class else None) or defs.get(method_name)

                        if not target_id:
                            ext_id = f"func:{clean_call}@external"
                            if ext_id not in graph.g:
                                graph.add_node_rich(
                                    node_id=ext_id,
                                    label=f"{clean_call} (External/BCL)",
                                    category="FUNCTION_DEF",
                                    scope={"scope_id": "external", "file": file_path, "line": 0},
                                    props={"signature": f"{clean_call}()", "source_code": ""},
                                )
                            target_id = ext_id

                        graph.add_edge_rich(
                            caller_id,
                            target_id,
                            edge_type="CALLS",
                            status="VALID",
                            detail="引用 .NET BCL 或外部組件",
                        )

            if cursor.goto_first_child():
                continue

            if ntype in ("class_declaration", "struct_declaration", "record_declaration", "interface_declaration") and class_stack:
                class_stack.pop()
            if ntype in ("method_declaration", "constructor_declaration", "local_function_statement") and func_stack:
                func_stack.pop()

            if cursor.goto_next_sibling():
                continue

            found = False
            while cursor.goto_parent():
                p_type = cursor.node.type
                if p_type in ("class_declaration", "struct_declaration", "record_declaration", "interface_declaration") and class_stack:
                    class_stack.pop()
                if p_type in ("method_declaration", "constructor_declaration", "local_function_statement") and func_stack:
                    func_stack.pop()
                if cursor.goto_next_sibling():
                    found = True
                    break
            if not found:
                break

        # 階段 3：自動為 [RelayCommand] 方法建立 MVVM 命令錨點（若尚未被其他 UI 控制項綁定）
        for nid, ndata in list(graph.g.nodes(data=True)):
            if ndata.get("category") == "FUNCTION_DEF":
                relay_cmd = ndata.get("props", {}).get("relay_command", "")
                if relay_cmd and graph.g.in_degree(nid) == 0:
                    m_line = ndata.get("scope", {}).get("line", 1)
                    curr_cls = ndata.get("props", {}).get("class_name", "")
                    ctrl_id = f"ctrl:#MVVM:{relay_cmd}@{file_path}:L{m_line}"
                    evt_id = f"event:MVVM.{relay_cmd}@{file_path}:L{m_line}"
                    graph.add_node_rich(
                        node_id=ctrl_id,
                        label=f"#MVVM:{relay_cmd}",
                        category="UI_CONTROL",
                        scope={"scope_id": curr_cls or "scope:global", "file": file_path, "line": m_line},
                        props={"ui_type": "MVVM RelayCommand", "line_start": m_line, "line_end": m_line},
                    )
                    graph.add_node_rich(
                        node_id=evt_id,
                        label=f"Execute ({relay_cmd})",
                        category="EVENT_BINDING",
                        scope={"scope_id": curr_cls or "scope:global", "file": file_path, "line": m_line},
                        props={"event": "Command", "kind": "MVVM_COMMAND"},
                    )
                    graph.add_edge_rich(ctrl_id, evt_id, edge_type="WIRES_TO", status="VALID")
                    graph.add_edge_rich(evt_id, nid, edge_type="TRIGGERS", status="VALID", detail=f"MVVM [RelayCommand] 觸發 {ndata.get('label')}")

        # 階段 4：如果沒有 UI 控制項錨點，但存在 Main() 函式，自動註冊 CLI 程式入口
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
