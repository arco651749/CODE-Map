from typing import Any, Dict, List, Optional, Set, Tuple
from tree_sitter import Language, Node, Parser
import tree_sitter_go as tsgo

from uia_coder.core.base_adapter import BaseUIAGraphBuilder
from uia_coder.core.graph import UIACodeGraph


class GoUIAGraphBuilder(BaseUIAGraphBuilder):
    """
    基於 Tree-sitter 的 Go 語意控制樹建構器
    - 追蹤頂層函式 (func)、結構體接收器方法 (func (r *Receiver) Method)
    - 識別 #CLI: main 進入點與 Goroutine 非同步調度
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

    def parse_and_build(self, source_code: str, file_path: str = "main.go") -> UIACodeGraph:
        tree = self.parser.parse(bytes(source_code, "utf-8"))
        graph = UIACodeGraph(name=f"Graph of {file_path}")

        scopes: Dict[str, Dict[str, Any]] = {
            "scope:global": {
                "id": "scope:global",
                "parent": None,
                "depth": 0,
                "defs": {},
            }
        }

        # 階段 1：收集所有函式宣告與結構體接收器方法
        self._collect_scopes_and_functions(tree.root_node, "scope:global", scopes, source_code, file_path, graph)

        # 階段 2：走訪呼叫點與危害接線
        self._wire_calls_and_hazards(tree.root_node, "scope:global", scopes, source_code, file_path, graph)

        # 階段 3：若包含 func main()，自動註冊 CLI 程式入口錨點
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

    def _extract_receiver_type(self, node: Node) -> Optional[str]:
        """從 method_declaration 提取接收器型別 (例如 *Server -> Server)"""
        recv_node = node.child_by_field_name("receiver")
        if not recv_node:
            return None
        for p in recv_node.children:
            if p.type == "parameter_declaration":
                t_node = p.child_by_field_name("type")
                if t_node:
                    return t_node.text.decode("utf-8").lstrip("*& ")
        return None

    def _collect_scopes_and_functions(
        self,
        node: Node,
        current_scope: str,
        scopes: Dict[str, Dict[str, Any]],
        source: str,
        file_path: str,
        graph: UIACodeGraph,
    ):
        if node.type in ("function_declaration", "method_declaration"):
            name_node = node.child_by_field_name("name")
            if name_node:
                raw_name = name_node.text.decode("utf-8")
                recv_type = self._extract_receiver_type(node)
                fn_name = f"{recv_type}.{raw_name}" if recv_type else raw_name

                start_row = node.start_point.row + 1
                end_row = node.end_point.row + 1
                node_id = f"func:{fn_name}@{file_path}:L{start_row}"

                source_code = source[node.start_byte : node.end_byte]
                params_node = node.child_by_field_name("parameters")
                params = params_node.text.decode("utf-8") if params_node else "()"
                sig = f"func {fn_name}{params}"

                scopes[current_scope]["defs"][fn_name] = node_id
                if recv_type:
                    scopes[current_scope]["defs"][raw_name] = node_id

                graph.add_node_rich(
                    node_id=node_id,
                    label=fn_name,
                    category="FUNCTION_DEF",
                    scope={"scope_id": current_scope, "file": file_path, "line": start_row},
                    props={
                        "signature": sig,
                        "parameters": params,
                        "source_code": source_code,
                        "line_start": start_row,
                        "line_end": end_row,
                        "line_count": max(1, end_row - start_row + 1),
                        "receiver_type": recv_type or "",
                        "raw_name": raw_name,
                    },
                )

                inner_scope_id = f"scope:fn:{fn_name}@{start_row}"
                scopes[inner_scope_id] = {
                    "id": inner_scope_id,
                    "parent": current_scope,
                    "depth": scopes[current_scope]["depth"] + 1,
                    "defs": {},
                    "receiver_type": recv_type,
                }

                body = node.child_by_field_name("body")
                if body:
                    for child in body.children:
                        self._collect_scopes_and_functions(
                            child, inner_scope_id, scopes, source, file_path, graph
                        )
                return

        for child in node.children:
            self._collect_scopes_and_functions(child, current_scope, scopes, source, file_path, graph)

    def _wire_calls_and_hazards(
        self,
        node: Node,
        current_scope: str,
        scopes: Dict[str, Dict[str, Any]],
        source: str,
        file_path: str,
        graph: UIACodeGraph,
        caller_func_id: Optional[str] = None,
        current_receiver_type: Optional[str] = None,
    ):
        if node.type in ("function_declaration", "method_declaration"):
            name_node = node.child_by_field_name("name")
            if name_node:
                raw_name = name_node.text.decode("utf-8")
                recv_type = self._extract_receiver_type(node)
                fn_name = f"{recv_type}.{raw_name}" if recv_type else raw_name
                start_row = node.start_point.row + 1
                curr_func_id = f"func:{fn_name}@{file_path}:L{start_row}"
                inner_scope_id = f"scope:fn:{fn_name}@{start_row}"

                body = node.child_by_field_name("body")
                if body:
                    for child in body.children:
                        self._wire_calls_and_hazards(
                            child, inner_scope_id, scopes, source, file_path, graph, curr_func_id, recv_type
                        )
                return

        # 檢測非同步啟動 (go func() 語句)
        is_goroutine = False
        if node.type == "go_statement":
            is_goroutine = True

        # 處理呼叫運算式 (call_expression)
        if node.type == "call_expression" and caller_func_id:
            fn_node = node.child_by_field_name("function")
            if fn_node:
                call_text = fn_node.text.decode("utf-8")
                call_row = node.start_point.row + 1

                # 1. 偵測 panic 執行期中斷危害
                if call_text == "panic":
                    hazard_id = f"hazard:panic@{file_path}:L{call_row}"
                    graph.add_node_rich(
                        node_id=hazard_id,
                        label="panic() [執行期恐慌/中斷]",
                        category="FUNCTION_DEF",
                        scope={"scope_id": current_scope, "file": file_path, "line": call_row},
                        props={"hazard": "GO_PANIC", "is_blocking": True},
                    )
                    graph.add_edge_rich(
                        caller_func_id,
                        hazard_id,
                        edge_type="CALLS",
                        status="BLOCKED_INVARIANT",
                        detail="呼叫了執行期恐慌中斷常式: panic()",
                        flow_type="ASYNC" if is_goroutine else "SYNC",
                    )
                    return

                # 2. 偵測 time.Sleep 同步阻塞危害
                if "time.Sleep" in call_text:
                    hazard_id = f"hazard:time.Sleep@{file_path}:L{call_row}"
                    graph.add_node_rich(
                        node_id=hazard_id,
                        label="time.Sleep() [同步休眠/介面凍結]",
                        category="FUNCTION_DEF",
                        scope={"scope_id": current_scope, "file": file_path, "line": call_row},
                        props={"hazard": "GO_BLOCKING_SLEEP", "is_blocking": True},
                    )
                    graph.add_edge_rich(
                        caller_func_id,
                        hazard_id,
                        edge_type="CALLS",
                        status="BLOCKED_INVARIANT",
                        detail="呼叫了同步阻塞常式: time.Sleep()",
                        flow_type="ASYNC" if is_goroutine else "SYNC",
                    )
                    return

                # 3. 常規函式或方法呼叫消解
                target_def_id, status, detail = self._lookup_go_scope(
                    call_text, current_scope, scopes, current_receiver_type
                )

                if not target_def_id:
                    # 外部套件或未消解呼叫 (如 fmt.Println)
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
                    status = "VALID"
                    detail = "調用標準庫或外部 Go 套件"

                graph.add_edge_rich(
                    caller_func_id,
                    target_def_id,
                    edge_type="CALLS",
                    status=status,
                    detail=detail,
                    flow_type="ASYNC" if is_goroutine else "SYNC",
                )

        # 遞迴遍歷子節點
        for child in node.children:
            self._wire_calls_and_hazards(
                child, current_scope, scopes, source, file_path, graph, caller_func_id, current_receiver_type
            )

    def _lookup_go_scope(
        self,
        call_text: str,
        current_scope_id: str,
        scopes: Dict[str, Dict[str, Any]],
        current_receiver_type: Optional[str],
    ) -> Tuple[Optional[str], str, str]:
        # 若是 selector (e.g. s.bind 或 Server.bind)
        method_name = call_text.split(".")[-1]
        
        curr = current_scope_id
        while curr:
            defs = scopes.get(curr, {}).get("defs", {})
            if call_text in defs:
                return defs[call_text], "VALID", f"作用域可達 (定義於 {curr})"

            if current_receiver_type:
                qualified = f"{current_receiver_type}.{method_name}"
                if qualified in defs:
                    return defs[qualified], "VALID", f"接收器方法可達 (定義於 {curr})"

            if method_name in defs:
                return defs[method_name], "VALID", f"作用域可達 (定義於 {curr})"

            curr = scopes.get(curr, {}).get("parent")

        # 全域搜尋接收器方法
        global_defs = scopes.get("scope:global", {}).get("defs", {})
        if current_receiver_type:
            q_name = f"{current_receiver_type}.{method_name}"
            if q_name in global_defs:
                return global_defs[q_name], "VALID", "結構體接收器方法可達"

        if method_name in global_defs:
            return global_defs[method_name], "VALID", "全域函式可達"

        return None, "UNRESOLVED", "未在當前檔案內找到宣告 (外部套件或模組)"
