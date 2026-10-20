import json
import sys
from typing import Any, Dict, List, Optional, Set

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import networkx as nx


class UIACodeGraph:
    """
    UIA-Coder 行為語意圖譜核心 (語言無關，基於 NetworkX DiGraph)
    負責管理所有 UI 控制項錨點、事件綁定、函式宣告、呼叫點與不變量守衛。
    """

    CATEGORIES = {
        "UI_CONTROL",       # 按鈕、輸入框、選單項、快捷鍵
        "EVENT_BINDING",    # 事件綁定、信號槽、onClick
        "FUNCTION_DEF",     # 函式宣告、方法宣告
        "MODULE_STATE",     # 模組頂層常數、設定表、正規表示式對應表
        "CALL_SITE",        # 函式呼叫點
        "INVARIANT_GUARD",  # 模態確認、權限檢查、參數驗證
        "SIDE_EFFECT",      # DOM 變更、RPC 網路請求、Toast 提示
    }

    EDGE_TYPES = {
        "WIRES_TO",         # 控制項 -> 事件
        "TRIGGERS",         # 事件 -> 處理函式
        "RESOLVES_TO",      # 呼叫點 -> 函式宣告 (作用域消解)
        "CALLS",            # 函式 -> 呼叫點 / 子呼叫
        "SEQUENTIAL",       # 串聯時序 (Stage 1 -> Stage 2)
        "CONCURRENT",       # 並聯時序 (Promise.all, unawaited)
    }

    EDGE_STATUSES = {
        "VALID",            # 正常通電且作用域可達
        "BLOCKED_SCOPE",    # 作用域阻隔 (閉包囚禁，執行期拋出 ReferenceError / NameError)
        "BLOCKED_INVARIANT" # 違反安全不變量 (例如阻塞主執行緒、記憶體洩漏風險)
    }

    def __init__(self, name: str = "UIA Semantic Graph"):
        self.g = nx.DiGraph(name=name, version="2.0")
        if "imports" not in self.g.graph:
            self.g.graph["imports"] = []
        if "exports" not in self.g.graph:
            self.g.graph["exports"] = {}

    # --- 節點新增方法 ---

    def add_node_rich(
        self,
        node_id: str,
        label: str,
        category: str,
        scope: Dict[str, Any],
        props: Optional[Dict[str, Any]] = None,
    ) -> str:
        if category not in self.CATEGORIES:
            raise ValueError(f"無效的節點類別: {category}，允許值: {self.CATEGORIES}")
        
        props = props or {}
        self.g.add_node(
            node_id,
            id=node_id,
            label=label,
            category=category,
            scope=scope,
            props=props,
        )
        return node_id

    def add_edge_rich(
        self,
        source: str,
        target: str,
        edge_type: str,
        flow_type: str = "SYNC",
        status: str = "VALID",
        sequence_order: int = 1,
        detail: str = "",
        is_conditional: bool = False,
        guard_type: str = "NONE",
        guard_expr: str = "",
        is_error_handled: bool = False,
    ):
        if edge_type not in self.EDGE_TYPES:
            raise ValueError(f"無效的邊類別: {edge_type}，允許值: {self.EDGE_TYPES}")
        if status not in self.EDGE_STATUSES:
            raise ValueError(f"無效的狀態: {status}，允許值: {self.EDGE_STATUSES}")

        self.g.add_edge(
            source,
            target,
            edge_type=edge_type,
            flow_type=flow_type,
            status=status,
            sequence_order=sequence_order,
            detail=detail,
            is_conditional=is_conditional,
            guard_type=guard_type,
            guard_expr=guard_expr,
            is_error_handled=is_error_handled,
        )

    # --- 序列化 (NetworkX Native Node-Link Format) ---

    def to_node_link_data(self) -> Dict[str, Any]:
        """導出為標準 NetworkX Node-Link JSON 字典，同時相容 links 與 edges 鍵名"""
        data = nx.node_link_data(self.g)
        if "edges" in data and "links" not in data:
            data["links"] = data["edges"]
        elif "links" in data and "edges" not in data:
            data["edges"] = data["links"]
        return data

    @classmethod
    def from_node_link_data(cls, data: Dict[str, Any]) -> "UIACodeGraph":
        """從標準 NetworkX Node-Link 字典還原為圖實例"""
        graph = cls()
        graph.g = nx.node_link_graph(data)
        return graph

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_node_link_data(), ensure_ascii=False, indent=indent)

    # --- 圖切片與語意演算法 ---

    def get_ui_anchors(self) -> List[str]:
        """尋找圖中所有 UI 控制項節點 (Root Anchors)"""
        return [
            n for n, d in self.g.nodes(data=True)
            if d.get("category") == "UI_CONTROL"
        ]

    def forward_slice(self, anchor_id: str) -> "UIACodeGraph":
        """
        前向圖切片 (Forward Graph Slicing)
        從指定的 UI 控制項錨點出發，切出所有受其波及與觸發的因果子圖。
        """
        if anchor_id not in self.g:
            raise KeyError(f"錨點不存在: {anchor_id}")

        descendants = nx.descendants(self.g, anchor_id)
        sub_nodes = descendants | {anchor_id}
        sub_g = self.g.subgraph(sub_nodes).copy()
        
        sliced = UIACodeGraph(name=f"Slice of {anchor_id}")
        sliced.g = sub_g
        return sliced

    def get_node_source(self, node_id: str) -> Optional[str]:
        """取得特定節點的真實源碼切片"""
        node_data = self.g.nodes.get(node_id, {})
        props = node_data.get("props", {})
        return props.get("source_code")

    def get_node_signature(self, node_id: str) -> Optional[str]:
        """取得函式節點的宣告簽章"""
        node_data = self.g.nodes.get(node_id, {})
        props = node_data.get("props", {})
        return props.get("signature")

    def to_causal_code_bundle(self, anchor_id: str) -> str:
        """
        以特定 UI 錨點為 Root，提取該控制項觸發的所有函式原始碼，
        打包成高密度、零干擾的 Context 代碼包供 Coding Agent 直接修改。
        """
        if anchor_id not in self.g:
            return f"❌ 找不到錨點節點: {anchor_id}"

        descendants = nx.descendants(self.g, anchor_id)
        relevant_nodes = [anchor_id] + list(descendants)

        lines = [f"# 📦 CODE-Map 因果切片代碼包: {anchor_id}", ""]
        seen_sources = set()

        for nid in relevant_nodes:
            ndata = self.g.nodes.get(nid, {})
            props = ndata.get("props", {})
            cat = ndata.get("category", "")
            src = props.get("source_code")

            if cat == "FUNCTION_DEF" and src and src not in seen_sources:
                seen_sources.add(src)
                sig = props.get("signature", ndata.get("label", nid))
                f_scope = ndata.get("scope", {})
                line_start = props.get("line_start", f_scope.get("line", "?"))
                line_end = props.get("line_end", "?")
                lines.append(f"## 🔹 {sig} ({f_scope.get('file', '')}: L{line_start}~L{line_end})")
                lines.append("```")
                lines.append(src)
                lines.append("```\n")

        return "\n".join(lines)

    def check_invariants(self) -> Dict[str, Any]:
        """
        形式化不變量守衛驗收：
        1. 檢查是否存在閉包作用域阻隔 (ReferenceError / Scope trap)
        2. 檢查是否存在主執行緒阻塞危害 (window.confirm, alert, time.sleep)
        """
        raw_scope_errors: Dict[Any, Dict[str, Any]] = {}
        raw_hazards: Dict[Any, Dict[str, Any]] = {}
        reported_targets: Set[str] = set()

        # 檢測所有的邊並去重彙整
        for u, v, d in self.g.edges(data=True):
            status = d.get("status")
            if status == "BLOCKED_SCOPE":
                src_data = self.g.nodes.get(u, {})
                dst_data = self.g.nodes.get(v, {})
                base_target = v.split("@")[0].split(":")[-1]
                key = (base_target, d.get("detail", ""))
                if key not in raw_scope_errors:
                    raw_scope_errors[key] = {
                        "type": "SCOPE_VIOLATION",
                        "caller": u,
                        "target": v,
                        "caller_scope": src_data.get("scope", {}),
                        "target_scope": dst_data.get("scope", {}),
                        "detail": d.get("detail", "目標函式被封閉於不可達之閉包作用域中"),
                        "count": 1,
                    }
                else:
                    raw_scope_errors[key]["count"] += 1
            elif status == "BLOCKED_INVARIANT":
                reported_targets.add(v)
                base_target = v.split("@")[0].split(":")[-1]
                key = ("INVARIANT_VIOLATION", base_target, d.get("detail", ""))
                if key not in raw_hazards:
                    raw_hazards[key] = {
                        "type": "INVARIANT_VIOLATION",
                        "source": u,
                        "target": v,
                        "detail": d.get("detail", "觸發不可接受的阻塞或危險操作"),
                        "count": 1,
                    }
                else:
                    raw_hazards[key]["count"] += 1

        # 檢測節點危害屬性 (若該目標節點已在邊上的 BLOCKED_INVARIANT 報告過，則不重複回報)
        for n, d in self.g.nodes(data=True):
            props = d.get("props", {})
            if props.get("is_blocking") and n not in reported_targets:
                base_node = n.split("@")[0].split(":")[-1]
                key = ("BLOCKING_API", base_node, d.get("label"))
                if key not in raw_hazards:
                    raw_hazards[key] = {
                        "type": "BLOCKING_API",
                        "node": n,
                        "label": d.get("label"),
                        "detail": f"使用了同步阻塞 API ({d.get('label')})，破壞非同步流暢度",
                        "count": 1,
                    }
                else:
                    raw_hazards[key]["count"] += 1

        scope_errors = list(raw_scope_errors.values())
        hazards = list(raw_hazards.values())

        passed = (len(scope_errors) == 0 and len(hazards) == 0)
        verdict = "🟢 READY_TO_SHIP" if passed else "🔴 BLOCKED_BY_INVARIANTS"

        return {
            "passed": passed,
            "verdict": verdict,
            "scope_errors": scope_errors,
            "hazards": hazards,
            "stats": {
                "total_nodes": self.g.number_of_nodes(),
                "total_edges": self.g.number_of_edges(),
                "ui_anchors_count": len(self.get_ui_anchors()),
            }
        }

    def to_uia_markdown(self, anchor_id: Optional[str] = None) -> str:
        """
        將有向圖投影為樹狀 Markdown 呈現（UIA 階層控制樹）
        適用於對人類工程師或 LLM 展現清晰的直觀脈絡。
        """
        anchors = [anchor_id] if anchor_id else self.get_ui_anchors()
        if not anchors:
            return "_無任何 UI 控制項錨點節點_"

        lines = []
        for anchor in anchors:
            anchor_data = self.g.nodes.get(anchor, {})
            label = anchor_data.get("label", anchor)
            props = anchor_data.get("props", {})
            ui_type = props.get("ui_type", "Control")
            lines.append(f"🌲 **{label}** `({ui_type})`")

            visited = set()
            self._render_subtree(anchor, lines, indent="  ", visited=visited)

        return "\n".join(lines)

    def _render_subtree(self, parent: str, lines: List[str], indent: str, visited: Set[str]):
        out_edges = sorted(
            self.g.out_edges(parent, data=True),
            key=lambda e: (e[2].get("sequence_order", 1), e[2].get("edge_type", ""))
        )

        for i, (_src, target, data) in enumerate(out_edges):
            is_last = (i == len(out_edges) - 1)
            branch = "└── " if is_last else "├── "
            child_indent = indent + ("    " if is_last else "│   ")

            edge_type = data.get("edge_type", "")
            flow_type = data.get("flow_type", "SYNC")
            status = data.get("status", "VALID")
            order = data.get("sequence_order", 1)
            target_data = self.g.nodes.get(target, {})
            target_label = target_data.get("label", target)

            status_icon = "💥 " if status == "BLOCKED_SCOPE" else ("⚠️ " if status == "BLOCKED_INVARIANT" else "")
            
            if edge_type == "WIRES_TO":
                lines.append(f"{indent}{branch}⚡ **{target_label}**")
            elif edge_type == "TRIGGERS":
                lines.append(f"{indent}{branch}🎯 處理函式: `{target_label}()`")
            elif edge_type in ("CALLS", "RESOLVES_TO"):
                order_prefix = f"[Stage {order}] " if order else ""
                if status == "BLOCKED_SCOPE":
                    lines.append(f"{indent}{branch}{status_icon}🔴 **{order_prefix}{target_label}()** _(作用域阻隔: 閉包不可達)_")
                elif status == "BLOCKED_INVARIANT":
                    lines.append(f"{indent}{branch}{status_icon}⚠️ **{order_prefix}{target_label}()** _(阻塞危害: 違反非同步守衛)_")
                else:
                    flow_badge = "⏳ [await] " if flow_type == "AWAIT" else ""
                    guard_badge = "🛡️ [guarded] " if data.get("is_conditional") else ""
                    lines.append(f"{indent}{branch}{status_icon}🔒 {flow_badge}{guard_badge}{order_prefix}`{target_label}()`")
            elif edge_type == "SEQUENTIAL":
                lines.append(f"{indent}{branch}⏳ [串聯 await] ➔ `{target_label}()`")
            elif edge_type == "CONCURRENT":
                lines.append(f"{indent}{branch}🔀 [並聯 async] ➔ `{target_label}()`")
            else:
                lines.append(f"{indent}{branch}{status_icon}`{target_label}` ({edge_type})")

            if target not in visited:
                visited.add(target)
                self._render_subtree(target, lines, child_indent, visited)
            else:
                lines.append(f"{child_indent}└── ↪️ _*ref: {target_label}_")
