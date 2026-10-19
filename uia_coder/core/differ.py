import os
import subprocess
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import networkx as nx
from uia_coder.core.graph import UIACodeGraph


def get_canonical_id(node_data: Dict[str, Any], fallback_id: str) -> str:
    """提取節點語意正規鍵，例如 UI_CONTROL:#btnDelete 或 FUNCTION_DEF:deleteItem"""
    cat = node_data.get("category", "")
    label = node_data.get("label", fallback_id)
    return f"{cat}:{label}"


class UIAGraphDiffResult:
    """
    UIA 圖譜差分結果物件
    記錄修改前後的節點增減、電線通斷、狀態躍遷與可讀差分樹。
    """

    def __init__(
        self,
        g_before: UIACodeGraph,
        g_after: UIACodeGraph,
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

    @property
    def passed(self) -> bool:
        return self.invariants_after["passed"]

    @property
    def verdict(self) -> str:
        return self.invariants_after["verdict"]

    @property
    def invariant_violations(self) -> List[Dict[str, Any]]:
        errs = self.invariants_after.get("scope_errors", [])
        haz = self.invariants_after.get("hazards", [])
        return [{"message": e.get("detail", str(e))} for e in errs + haz]

    def to_diff_markdown(self) -> str:
        lines = []
        lines.append("🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**")
        lines.append("---")

        # 整理兩邊的 UI 錨點 (依 canonical id 對齊)
        anchors_b = {self.canon_map_b[n]: n for n in self.g_before.get_ui_anchors() if n in self.canon_map_b}
        anchors_a = {self.canon_map_a[n]: n for n in self.g_after.get_ui_anchors() if n in self.canon_map_a}
        all_canon_anchors = sorted(set(anchors_b.keys()) | set(anchors_a.keys()))

        if not all_canon_anchors:
            return "_無任何 UI 控制項變更_"

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
                # 前後都有，比對其因果樹分支
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

        if self.invariants_after["scope_errors"]:
            lines.append("\n❌ **仍存在之作用域死穴:**")
            for err in self.invariants_after["scope_errors"]:
                lines.append(f"  - {err['detail']}")

        if self.invariants_after["hazards"]:
            lines.append("\n⚠️ **仍存在之危害操作:**")
            for h in self.invariants_after["hazards"]:
                lines.append(f"  - {h['detail']}")

        lines.append(f"\n**最終驗收裁決: {self.verdict}**")
        return "\n".join(lines)

    def _render_graph_subtree(self, graph: UIACodeGraph, parent: str, lines: List[str], indent: str, prefix: str, visited: Optional[Set[str]] = None):
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
        # 建立 canonical 映射表: canon_target -> (raw_target, edge_data)
        out_b = {self.canon_map_b[v]: (v, d) for _u, v, d in self.g_before.g.out_edges(parent_b, data=True) if v in self.canon_map_b} if parent_b else {}
        out_a = {self.canon_map_a[v]: (v, d) for _u, v, d in self.g_after.g.out_edges(parent_a, data=True) if v in self.canon_map_a} if parent_a else {}

        all_targets = sorted(set(out_b.keys()) | set(out_a.keys()))

        for canon_tgt in all_targets:
            in_b = canon_tgt in out_b
            in_a = canon_tgt in out_a

            if canon_tgt in visited:
                lines.append(f"  {indent}└── *ref:`{canon_tgt}` [已折疊指針]")
                continue
            visited.add(canon_tgt)

            if in_b and not in_a:
                v_b, d_b = out_b[canon_tgt]
                t_data = self.g_before.g.nodes.get(v_b, {})
                label = t_data.get("label", v_b)
                lines.append(f"- {indent}└── [{d_b.get('edge_type')}] `{label}()` [已拆除]")
            elif in_a and not in_b:
                v_a, d_a = out_a[canon_tgt]
                t_data = self.g_after.g.nodes.get(v_a, {})
                label = t_data.get("label", v_a)
                flow = "⏳ [await] " if d_a.get("flow_type") == "AWAIT" else ""
                status_icon = "🟢 " if d_a.get("status") == "VALID" else "💥 "
                lines.append(f"+ {indent}└── {status_icon}{flow}[{d_a.get('edge_type')}] `{label}()` [新增因果]")
                self._render_dual_subtree(parent_b="", parent_a=v_a, lines=lines, indent=indent + "    ", visited=visited)
            else:
                v_b, d_b = out_b[canon_tgt]
                v_a, d_a = out_a[canon_tgt]
                t_data = self.g_after.g.nodes.get(v_a, {})
                label = t_data.get("label", v_a)

                # 比對邊的狀態
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

                self._render_dual_subtree(v_b, v_a, lines, indent + "    ", visited=visited)

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


class UIAGraphDiffer:
    """
    UIA 圖譜差分計算器
    支援兩個 UIACodeGraph 實例比較、或是對 Git 歷史抽取檔案比對。
    """

    @classmethod
    def diff_graphs(cls, g_before: UIACodeGraph, g_after: UIACodeGraph) -> UIAGraphDiffResult:
        # 1. 建立語意正規鍵對照 (Canonical Map)
        canon_b = {n: get_canonical_id(g_before.g.nodes[n], n) for n in g_before.g.nodes}
        canon_a = {n: get_canonical_id(g_after.g.nodes[n], n) for n in g_after.g.nodes}

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

        edges_added = [k for k in edges_canon_a if k not in edges_canon_b]
        edges_removed = [k for k in edges_canon_b if k not in edges_canon_a]

        # 3. 狀態躍遷分析
        status_transitions = []
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

        # 4. 函式實作變更檢測 (Function Code Modification Detection)
        functions_modified = []
        rev_canon_b = {v: k for k, v in canon_b.items()}
        rev_canon_a = {v: k for k, v in canon_a.items()}

        for cid in (canon_nodes_b & canon_nodes_a):
            if cid.startswith("FUNCTION_DEF:"):
                nid_b = rev_canon_b[cid]
                nid_a = rev_canon_a[cid]
                data_b = g_before.g.nodes[nid_b]
                data_a = g_after.g.nodes[nid_a]
                props_b = data_b.get("props", {})
                props_a = data_a.get("props", {})
                src_b = props_b.get("source_code", "").strip()
                src_a = props_a.get("source_code", "").strip()
                if src_b and src_a and src_b != src_a:
                    f_scope_b = data_b.get("scope", {})
                    f_scope_a = data_a.get("scope", {})
                    functions_modified.append({
                        "canonical_id": cid,
                        "label": data_a.get("label", cid.split(":", 1)[-1]),
                        "sig_before": props_b.get("signature", data_b.get("label", "")),
                        "sig_after": props_a.get("signature", data_a.get("label", "")),
                        "lines_before": (props_b.get("line_start", f_scope_b.get("line", "?")), props_b.get("line_end", "?")),
                        "lines_after": (props_a.get("line_start", f_scope_a.get("line", "?")), props_a.get("line_end", "?")),
                        "source_before": src_b,
                        "source_after": src_a,
                    })

        inv_b = g_before.check_invariants()
        inv_a = g_after.check_invariants()

        return UIAGraphDiffResult(
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
    ) -> UIAGraphDiffResult:
        from uia_coder.adapters import get_adapter_for_file

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
