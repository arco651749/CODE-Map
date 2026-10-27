import os
import subprocess
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import networkx as nx
from code_map.core.graph import CodeMapGraph


def get_canonical_id(node_data: Dict[str, Any], fallback_id: str) -> str:
    """
    提取節點語意正規鍵。
    結合詞法作用域鏈 (Qualified Lexical Path) 產生唯一鍵，
    例如 FUNCTION_DEF:UserModal::handleClick 或 FUNCTION_DEF:deleteItem。
    """
    cat = node_data.get("category", "")
    label = node_data.get("label", fallback_id)
    scope = node_data.get("scope", {})
    qual = scope.get("qualified_path", "")

    if not qual:
        # 從 scope_id 提取 (去除檔名與行列號，例如 scope:UserModal@app.tsx:L10C1 -> UserModal)
        scope_id = scope.get("scope_id", "")
        if scope_id and scope_id != "scope:global":
            raw = scope_id.split("@")[0].replace("scope:", "")
            qual = raw if raw else ""

    if cat == "UI_CONTROL":
        return f"{cat}:{label}"

    if qual and qual != "global":
        return f"{cat}:{qual}::{label}"

    return f"{cat}:{label}"


def build_canonical_map(graph: CodeMapGraph) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    建立 node_id -> canonical_id 以及 canonical_id -> node_id 的雙向映射。
    若同一圖中出現同名節點，自動附加序號 (#2, #3...) 防止覆寫與碰撞。
    """
    canon: Dict[str, str] = {}
    rev_canon: Dict[str, str] = {}
    counts: Dict[str, int] = {}

    for n in graph.g.nodes:
        nd = graph.g.nodes[n]
        base_cid = get_canonical_id(nd, n)
        if base_cid not in counts:
            counts[base_cid] = 1
            cid = base_cid
        else:
            counts[base_cid] += 1
            cid = f"{base_cid}#{counts[base_cid]}"
        canon[n] = cid
        rev_canon[cid] = n

    return canon, rev_canon


class CodeMapDiffResult:
    """
    UIA 圖譜差分結果物件
    記錄修改前後的節點增減、電線通斷、狀態躍遷與可讀差分樹。
    """

    def __init__(
        self,
        g_before: CodeMapGraph,
        g_after: CodeMapGraph,
        nodes_added: List[Dict[str, Any]],
        nodes_removed: List[Dict[str, Any]],
        edges_added: List[Dict[str, Any]],
        edges_removed: List[Dict[str, Any]],
        status_transitions: List[Dict[str, Any]],
        invariants_before: Dict[str, Any],
        invariants_after: Dict[str, Any],
        canon_map_b: Dict[str, str],
        canon_map_a: Dict[str, str],
        functions_modified: Optional[List[Dict[str, Any]]] = None,
    ):
        self.g_before = g_before
        self.g_after = g_after
        self.nodes_added = nodes_added
        self.nodes_removed = nodes_removed
        self.edges_added = edges_added
        self.edges_removed = edges_removed
        self.status_transitions = status_transitions
        self.invariants_before = invariants_before
        self.invariants_after = invariants_after
        self.canon_map_b = canon_map_b
        self.canon_map_a = canon_map_a
        self.functions_modified = functions_modified or []

        # 差分不變量守衛 (Differential Invariant Verification)
        errs_b = invariants_before.get("scope_errors", [])
        haz_b = invariants_before.get("hazards", [])
        errs_a = invariants_after.get("scope_errors", [])
        haz_a = invariants_after.get("hazards", [])

        def _scope_err_key(item: Dict[str, Any]) -> Any:
            tgt = item.get("target", "")
            base_tgt = tgt.split("@")[0].split(":")[-1]
            return (base_tgt, item.get("detail", ""))

        def _hazard_key(item: Dict[str, Any]) -> Any:
            tgt = str(item.get("target") or item.get("node") or item.get("label", ""))
            base_tgt = tgt.split("@")[0].split(":")[-1]
            return (item.get("type", ""), base_tgt, item.get("detail", ""))

        b_err_keys = {_scope_err_key(e) for e in errs_b}
        b_haz_keys = {_hazard_key(h) for h in haz_b}

        self.new_scope_errors = [e for e in errs_a if _scope_err_key(e) not in b_err_keys]
        self.new_hazards = [h for h in haz_a if _hazard_key(h) not in b_haz_keys]
        self.pre_existing_scope_errors = [e for e in errs_a if _scope_err_key(e) in b_err_keys]
        self.pre_existing_hazards = [h for h in haz_a if _hazard_key(h) in b_haz_keys]

    @property
    def passed(self) -> bool:
        # 僅當本次 Commit 引入新增違規時判定不通過
        return (len(self.new_scope_errors) == 0 and len(self.new_hazards) == 0)

    @property
    def verdict(self) -> str:
        return "🟢 READY_TO_SHIP" if self.passed else "🔴 BLOCKED_BY_INVARIANTS"

    @property
    def invariant_violations(self) -> List[Dict[str, Any]]:
        return [{"message": e.get("detail", str(e))} for e in self.new_scope_errors + self.new_hazards]

    def to_diff_markdown(self) -> str:
        lines = []
        lines.append("🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**")
        lines.append("---")

        # 整理兩邊的 UI 錨點 (依 canonical id 對齊)
        anchors_b = {self.canon_map_b[n]: n for n in self.g_before.get_ui_anchors() if n in self.canon_map_b}
        anchors_a = {self.canon_map_a[n]: n for n in self.g_after.get_ui_anchors() if n in self.canon_map_a}
        all_canon_anchors = sorted(set(anchors_b.keys()) | set(anchors_a.keys()))

        if not all_canon_anchors:
            lines.append("  _無任何 UI 控制項變更_")
        else:
            for canon_id in all_canon_anchors:
                in_b = canon_id in anchors_b
                in_a = canon_id in anchors_a

                if in_a and not in_b:
                    node_a = anchors_a[canon_id]
                    data = self.g_after.g.nodes[node_a]
                    lines.append(f"+ 🌲 **{data.get('label', canon_id)}** `({data.get('props', {}).get('ui_type', 'Control')})` [新增控制項]")
                    self._render_graph_subtree(self.g_after, node_a, lines, indent="  ", prefix="+ ")
                elif in_b and not in_a:
                    node_b = anchors_b[canon_id]
                    data = self.g_before.g.nodes[node_b]
                    lines.append(f"- 🌲 **{data.get('label', canon_id)}** `({data.get('props', {}).get('ui_type', 'Control')})` [刪除控制項]")
                    self._render_graph_subtree(self.g_before, node_b, lines, indent="  ", prefix="- ")
                else:
                    node_b = anchors_b[canon_id]
                    node_a = anchors_a[canon_id]
                    data = self.g_after.g.nodes[node_a]
                    lines.append(f"  🌲 **{data.get('label', canon_id)}** `({data.get('props', {}).get('ui_type', 'Control')})`")
                    self._render_dual_subtree(node_b, node_a, lines, indent="  ")

        lines.append("\n🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**")
        if self.status_transitions:
            for trans in self.status_transitions:
                lines.append(f"  • {trans['icon']} `{trans['target']}`: **{trans['from']}** ➔ **{trans['to']}** ({trans['detail']})")
        else:
            lines.append("  • _無狀態躍遷變動_")

        # 補充結構拓樸圖變更明細 (當發生節點或呼叫邊增刪時)
        if self.nodes_added or self.nodes_removed or self.edges_added or self.edges_removed:
            lines.append("\n🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**")
            rev_a = {cid: nid for nid, cid in self.canon_map_a.items()}
            rev_b = {cid: nid for nid, cid in self.canon_map_b.items()}
            items = []
            for n in self.nodes_added:
                nid_a = rev_a.get(n, n)
                nd_a = self.g_after.g.nodes.get(nid_a, {})
                lbl = nd_a.get("label", n)
                cat = nd_a.get("category", n.split(":", 1)[0] if ":" in n else "")
                items.append(f"+ [新增節點] `{lbl}` ({cat})")
            for n in self.nodes_removed:
                nid_b = rev_b.get(n, n)
                nd_b = self.g_before.g.nodes.get(nid_b, {})
                lbl = nd_b.get("label", n)
                cat = nd_b.get("category", n.split(":", 1)[0] if ":" in n else "")
                items.append(f"- [移除節點] `{lbl}` ({cat})")
            for item in self.edges_added:
                u, v = item[0], item[1]
                et_default = item[2] if len(item) > 2 else "CALLS"
                u_nid = rev_a.get(u, u)
                v_nid = rev_a.get(v, v)
                u_lbl = self.g_after.g.nodes.get(u_nid, {}).get("label", u)
                v_lbl = self.g_after.g.nodes.get(v_nid, {}).get("label", v)
                ed = self.g_after.g.get_edge_data(u_nid, v_nid) or {}
                et = ed.get("edge_type", et_default)
                g_expr = ed.get("guard_expr")
                g_info = f" [guard: {g_expr}]" if (ed.get("is_conditional") and g_expr) else (" [guarded]" if ed.get("is_conditional") else "")
                items.append(f"+ [新增呼叫邊] `{u_lbl}` ──[{et}{g_info}]──> `{v_lbl}`")
            for item in self.edges_removed:
                u, v = item[0], item[1]
                et_default = item[2] if len(item) > 2 else "CALLS"
                u_nid = rev_b.get(u, u)
                v_nid = rev_b.get(v, v)
                u_lbl = self.g_before.g.nodes.get(u_nid, {}).get("label", u)
                v_lbl = self.g_before.g.nodes.get(v_nid, {}).get("label", v)
                ed = self.g_before.g.get_edge_data(u_nid, v_nid) or {}
                et = ed.get("edge_type", et_default)
                items.append(f"- [移除呼叫邊] `{u_lbl}` ──[{et}]──> `{v_lbl}`")

            max_items = 15
            for it in items[:max_items]:
                lines.append(f"  • {it}")
            if len(items) > max_items:
                lines.append(f"  • _... 以及其餘 {len(items) - max_items} 項拓樸變更_")

        if self.new_scope_errors:
            lines.append("\n❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**")
            for err in self.new_scope_errors:
                c_str = f" (共 {err['count']} 處)" if err.get("count", 1) > 1 else ""
                lines.append(f"  - {err['detail']}{c_str}")

        if self.new_hazards:
            lines.append("\n⚠️ **本次 Commit 新引入之危害操作 (New Hazards):**")
            for h in self.new_hazards:
                c_str = f" (共 {h['count']} 處)" if h.get("count", 1) > 1 else ""
                lines.append(f"  - {h['detail']}{c_str}")

        total_pre = len(self.pre_existing_scope_errors) + len(self.pre_existing_hazards)
        if total_pre > 0:
            lines.append(f"\nℹ️ **存量環境提醒**: 檔案內含 {total_pre} 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)")

        lines.append(f"\n**最終驗收裁決: {self.verdict}**")
        return "\n".join(lines)

    def _render_graph_subtree(self, graph: CodeMapGraph, parent: str, lines: List[str], indent: str, prefix: str, visited: Optional[Set[str]] = None):
        if visited is None:
            visited = set()
        for _s, target, d in graph.g.out_edges(parent, data=True):
            t_data = graph.g.nodes.get(target, {})
            label = t_data.get("label", target)
            e_type = d.get("edge_type", "")
            flow = "⏳ [await] " if d.get("flow_type") == "AWAIT" else ""
            if target in visited:
                lines.append(f"{prefix}{indent}└── *ref:`{label}()` [已折疊指針]")
                continue
            visited.add(target)
            lines.append(f"{prefix}{indent}└── {flow}[{e_type}] `{label}()`")
            self._render_graph_subtree(graph, target, lines, indent + "    ", prefix, visited)

    def _render_dual_subtree(self, parent_b: str, parent_a: str, lines: List[str], indent: str, visited: Optional[Set[str]] = None):
        if visited is None:
            visited = set()
        out_b = {self.canon_map_b[v]: (v, d) for _u, v, d in self.g_before.g.out_edges(parent_b, data=True) if v in self.canon_map_b} if parent_b else {}
        out_a = {self.canon_map_a[v]: (v, d) for _u, v, d in self.g_after.g.out_edges(parent_a, data=True) if v in self.canon_map_a} if parent_a else {}

        # 1. 直接配對 exact canonical target
        paired_keys: List[Tuple[str, str]] = []
        unpaired_b = dict(out_b)
        unpaired_a = dict(out_a)

        for k in list(unpaired_b.keys()):
            if k in unpaired_a:
                paired_keys.append((k, k))
                del unpaired_b[k]
                del unpaired_a[k]

        # 2. 作用域修復/提升之函式配對 (同函式名 label)
        for kb in list(unpaired_b.keys()):
            vb, db = unpaired_b[kb]
            label_b = self.g_before.g.nodes.get(vb, {}).get("label", kb)
            for ka in list(unpaired_a.keys()):
                va, da = unpaired_a[ka]
                label_a = self.g_after.g.nodes.get(va, {}).get("label", ka)
                if label_b == label_a:
                    paired_keys.append((kb, ka))
                    del unpaired_b[kb]
                    del unpaired_a[ka]
                    break

        # 刪除的節點
        for kb, (v_b, d_b) in sorted(unpaired_b.items()):
            t_data = self.g_before.g.nodes.get(v_b, {})
            label = t_data.get("label", v_b)
            lines.append(f"- {indent}└── [{d_b.get('edge_type')}] `{label}()` [已拆除]")

        # 新增的節點
        for ka, (v_a, d_a) in sorted(unpaired_a.items()):
            t_data = self.g_after.g.nodes.get(v_a, {})
            label = t_data.get("label", v_a)
            flow = "⏳ [await] " if d_a.get("flow_type") == "AWAIT" else ""
            status_icon = "🟢 " if d_a.get("status") == "VALID" else "💥 "
            lines.append(f"+ {indent}└── {status_icon}{flow}[{d_a.get('edge_type')}] `{label}()` [新增因果]")
            self._render_dual_subtree(parent_b="", parent_a=v_a, lines=lines, indent=indent + "    ", visited=visited)

        # 配對的節點
        for kb, ka in sorted(paired_keys):
            v_b, d_b = out_b[kb]
            v_a, d_a = out_a[ka]
            t_data = self.g_after.g.nodes.get(v_a, {})
            label = t_data.get("label", v_a)

            if ka in visited:
                lines.append(f"  {indent}└── *ref:`{label}` [已折疊指針]")
                continue
            visited.add(ka)

            st_b = d_b.get("status")
            st_a = d_a.get("status")

            if st_b != st_a:
                lines.append(f"- {indent}└── 💥 [{d_b.get('edge_type')}] `{label}()` ({st_b}: 閉包囚禁)")
                lines.append(f"+ {indent}└── 🟢 [{d_a.get('edge_type')}] `{label}()` ({st_a}: 作用域已修復)")
            else:
                flow = "⏳ [await] " if d_a.get("flow_type") == "AWAIT" else ""
                if d_a.get("edge_type") == "WIRES_TO":
                    lines.append(f"  {indent}└── ⚡ **{label}**")
                else:
                    lines.append(f"  {indent}└── 🎯 {flow}[{d_a.get('edge_type')}] `{label}()`")

            self._render_dual_subtree(v_b, v_a, lines, indent=indent + "    ", visited=visited)

    def to_function_code_diff_markdown(self) -> str:
        """輸出修改前後函式真實原始碼對照包，專供 AI Agent 進行語意功能比對"""
        if not self.functions_modified:
            return "_無任何現存函式發生實作變更_"

        lines = ["## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)", ""]
        for fn in self.functions_modified:
            label = fn["label"]
            lb_start, lb_end = fn["lines_before"]
            la_start, la_end = fn["lines_after"]
            lines.append(f"### 🔹 函式: `{label}()`")
            lines.append(f"- **變更前簽章 (Before)**: `{fn['sig_before']}` (L{lb_start}~L{lb_end})")
            lines.append(f"- **變更後簽章 (After)**: `{fn['sig_after']}` (L{la_start}~L{la_end})")
            lines.append("")
            lines.append("#### ◀️ 變更前實作碼 (Before Implementation):")
            lines.append("```")
            lines.append(fn["source_before"])
            lines.append("```")
            lines.append("")
            lines.append("#### ▶️ 變更後實作碼 (After Implementation):")
            lines.append("```")
            lines.append(fn["source_after"])
            lines.append("```")
            lines.append("")
        return "\n".join(lines)


class CodeMapDiffer:
    """
    UIA 圖譜差分計算器
    支援兩個 CodeMapGraph 實例比較、或是對 Git 歷史抽取檔案比對。
    """

    @classmethod
    def diff_graphs(cls, g_before: CodeMapGraph, g_after: CodeMapGraph) -> CodeMapDiffResult:
        # 1. 建立語意正規鍵對照 (Canonical Map，具備防同名碰撞序號)
        canon_b, rev_canon_b = build_canonical_map(g_before)
        canon_a, rev_canon_a = build_canonical_map(g_after)

        canon_nodes_b = set(canon_b.values())
        canon_nodes_a = set(canon_a.values())

        nodes_added = [n for n in canon_nodes_a if n not in canon_nodes_b]
        nodes_removed = [n for n in canon_nodes_b if n not in canon_nodes_a]

        # 2. 建立邊的正規鍵
        edges_canon_b = {
            (canon_b[u], canon_b[v], d.get("edge_type")): d 
            for u, v, d in g_before.g.edges(data=True) if u in canon_b and v in canon_b
        }
        edges_canon_a = {
            (canon_a[u], canon_a[v], d.get("edge_type")): d 
            for u, v, d in g_after.g.edges(data=True) if u in canon_a and v in canon_a
        }

        # 3. 狀態躍遷分析 (Exact Match + Scope-Hoisting Match)
        status_transitions = []
        matched_b_edges: Set[Tuple[str, str, str]] = set()
        matched_a_edges: Set[Tuple[str, str, str]] = set()

        # 3.1 完全相符的邊
        for k in (set(edges_canon_b.keys()) & set(edges_canon_a.keys())):
            st_b = edges_canon_b[k].get("status")
            st_a = edges_canon_a[k].get("status")
            if st_b != st_a:
                icon = "🎉 修復成功:" if (st_b == "BLOCKED_SCOPE" and st_a == "VALID") else "💥 引入死穴:"
                status_transitions.append({
                    "target": k[1],
                    "from": st_b,
                    "to": st_a,
                    "icon": icon,
                    "detail": edges_canon_a[k].get("detail", "")
                })
            matched_b_edges.add(k)
            matched_a_edges.add(k)

        # 3.2 作用域躍遷修復匹配 (例如函式從內部閉包提升至外部/全域，使 BLOCKED_SCOPE 躍遷至 VALID)
        unmatched_b = [k for k in edges_canon_b if k not in matched_b_edges and edges_canon_b[k].get("status") == "BLOCKED_SCOPE"]
        unmatched_a = [k for k in edges_canon_a if k not in matched_a_edges and edges_canon_a[k].get("status") == "VALID"]

        for kb in unmatched_b:
            src_b, tgt_b, type_b = kb
            base_name_b = tgt_b.split(":")[-1].split("#")[0]
            for ka in unmatched_a:
                src_a, tgt_a, type_a = ka
                base_name_a = tgt_a.split(":")[-1].split("#")[0]
                if src_b == src_a and type_b == type_a and base_name_b == base_name_a:
                    status_transitions.append({
                        "target": tgt_a,
                        "from": "BLOCKED_SCOPE",
                        "to": "VALID",
                        "icon": "🎉 修復成功:",
                        "detail": edges_canon_a[ka].get("detail", "")
                    })
                    matched_b_edges.add(kb)
                    matched_a_edges.add(ka)
                    break

        edges_added = [k for k in edges_canon_a if k not in edges_canon_b and k not in matched_a_edges]
        edges_removed = [k for k in edges_canon_b if k not in edges_canon_a and k not in matched_b_edges]

        # 4. 函式實作、頂層狀態與 UI 控制項/主題定義變更檢測
        functions_modified = []
        for cid in (canon_nodes_b & canon_nodes_a):
            if cid.startswith(("FUNCTION_DEF:", "MODULE_STATE:", "UI_CONTROL:")):
                nid_b = rev_canon_b[cid]
                nid_a = rev_canon_a[cid]
                data_b = g_before.g.nodes[nid_b]
                data_a = g_after.g.nodes[nid_a]
                props_b = data_b.get("props", {})
                props_a = data_a.get("props", {})
                src_b = props_b.get("source_code", "").strip()
                src_a = props_a.get("source_code", "").strip()
                fp_b = props_b.get("executable_fingerprint")
                fp_a = props_a.get("executable_fingerprint")

                # 優先使用去噪後的 AST 可執行 Token 指紋比對，若無則降級為原始碼字串比對
                is_modified = (fp_b != fp_a) if (fp_b is not None and fp_a is not None) else (src_b != src_a)
                if src_b and src_a and is_modified:
                    f_scope_b = data_b.get("scope", {})
                    f_scope_a = data_a.get("scope", {})
                    is_module_state = cid.startswith("MODULE_STATE:")
                    default_sig_b = f"[Module State] {data_b.get('label', '')}" if is_module_state else data_b.get("label", "")
                    default_sig_a = f"[Module State] {data_a.get('label', '')}" if is_module_state else data_a.get("label", "")
                    functions_modified.append({
                        "canonical_id": cid,
                        "label": data_a.get("label", cid.split(":", 1)[-1]),
                        "sig_before": props_b.get("signature", default_sig_b),
                        "sig_after": props_a.get("signature", default_sig_a),
                        "lines_before": (props_b.get("line_start", f_scope_b.get("line", "?")), props_b.get("line_end", "?")),
                        "lines_after": (props_a.get("line_start", f_scope_a.get("line", "?")), props_a.get("line_end", "?")),
                        "source_before": src_b,
                        "source_after": src_a,
                    })

        inv_b = g_before.check_invariants()
        inv_a = g_after.check_invariants()

        return CodeMapDiffResult(
            g_before=g_before,
            g_after=g_after,
            nodes_added=nodes_added,
            nodes_removed=nodes_removed,
            edges_added=edges_added,
            edges_removed=edges_removed,
            status_transitions=status_transitions,
            invariants_before=inv_b,
            invariants_after=inv_a,
            canon_map_b=canon_b,
            canon_map_a=canon_a,
            functions_modified=functions_modified,
        )

    @classmethod
    def diff_git_file(
        cls,
        repo_path: str,
        file_path: str,
        diff_range: str = "HEAD~1",
        target_ref: Optional[str] = None,
    ) -> CodeMapDiffResult:
        from code_map.adapters import get_adapter_for_file

        adapter = get_adapter_for_file(file_path)
        rel_path = os.path.relpath(file_path, repo_path).replace("\\", "/")
        cmd_old = ["git", "-C", repo_path, "show", f"{diff_range}:{rel_path}"]
        res_old = subprocess.run(cmd_old, capture_output=True, text=True, encoding="utf-8", errors="replace")
        old_code = res_old.stdout if res_old.returncode == 0 else ""

        if target_ref:
            cmd_new = ["git", "-C", repo_path, "show", f"{target_ref}:{rel_path}"]
            res_new = subprocess.run(cmd_new, capture_output=True, text=True, encoding="utf-8", errors="replace")
            new_code = res_new.stdout if res_new.returncode == 0 else ""
        elif os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                new_code = f.read()
        else:
            cmd_new = ["git", "-C", repo_path, "show", f"HEAD:{rel_path}"]
            res_new = subprocess.run(cmd_new, capture_output=True, text=True, encoding="utf-8", errors="replace")
            new_code = res_new.stdout if res_new.returncode == 0 else ""

        g_before = adapter.parse_and_build(old_code, file_path=f"before/{rel_path}")
        g_after = adapter.parse_and_build(new_code, file_path=f"after/{rel_path}")

        return cls.diff_graphs(g_before, g_after)
