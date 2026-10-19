import html
import json
import os
import sys
from typing import Any, Dict, List, Optional
import networkx as nx

from uia_coder.core.graph import UIACodeGraph


class HTMLDashboardReporter:
    """
    全景雙欄互動式 HTML 儀表板生成器
    - 左欄：可折疊因果拓撲樹 (UI 控制項錨點 / CLI 入口 / 函式鏈)
    - 右欄：外科手術級原始碼預覽器 (支援一鍵查看函式源碼與整包因果代碼包)
    - 100% 自包含 (Inline CSS + Vanilla JS)，無外部 CDN 依賴，相容 Antigravity 內嵌預覽。
    """

    def generate(
        self,
        graph: UIACodeGraph,
        output_path: str,
        title: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> str:
        out_abs = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(out_abs), exist_ok=True)
        display_title = title or f"CODE-Map 全景因果地圖 - {os.path.basename(file_path or '源碼分析')}"
        target_name = file_path or "analyzed_source"

        # 1. 盤點所有函式節點原始碼與元資料
        funcs_meta: Dict[str, Dict[str, Any]] = {}
        for n, d in graph.g.nodes(data=True):
            if d.get("category") == "FUNCTION_DEF":
                props = d.get("props", {})
                f_scope = d.get("scope", {})
                funcs_meta[n] = {
                    "id": n,
                    "label": d.get("label", n),
                    "signature": props.get("signature", d.get("label", n)),
                    "parameters": props.get("parameters", "()"),
                    "line_start": props.get("line_start", f_scope.get("line", 1)),
                    "line_end": props.get("line_end", f_scope.get("line", 1)),
                    "line_count": props.get("line_count", 1),
                    "is_async": props.get("is_async", False),
                    "source_code": props.get("source_code", ""),
                    "scope_id": f_scope.get("scope_id", "scope:global"),
                    "class_name": props.get("class_name", ""),
                }

        # 2. 收集錨點 (UI 控制項 / CLI 入口 / 或無錨點時的頂層函式)
        ui_anchors = graph.get_ui_anchors()
        anchor_nodes = []

        if ui_anchors:
            for n in ui_anchors:
                anchor_nodes.append((n, graph.g.nodes[n]))
        else:
            # 若無 UI 控制項，自動尋找入度為 0 的根函式，或模組內前置函式作為錨點
            for n, d in graph.g.nodes(data=True):
                if d.get("category") == "FUNCTION_DEF":
                    in_deg = graph.g.in_degree(n)
                    if in_deg == 0:
                        anchor_nodes.append((n, d))
            if not anchor_nodes and funcs_meta:
                for n in list(funcs_meta.keys())[:10]:
                    anchor_nodes.append((n, graph.g.nodes[n]))

        # 3. 遞迴構建因果樹
        ui_trees = []
        seen_labels = set()

        def build_tree_node(curr_id: str, visited: Optional[set] = None) -> Dict[str, Any]:
            if visited is None:
                visited = set()
            c_data = graph.g.nodes.get(curr_id, {})
            c_cat = c_data.get("category", "")
            c_label = c_data.get("label", curr_id)

            node_obj = {
                "id": curr_id,
                "label": c_label,
                "category": c_cat,
                "has_code": curr_id in funcs_meta,
                "children": [],
            }

            if curr_id in visited:
                node_obj["is_ref"] = True
                return node_obj

            visited.add(curr_id)

            for _, tgt, edata in graph.g.out_edges(curr_id, data=True):
                child_node = build_tree_node(tgt, visited.copy())
                child_node["edge_type"] = edata.get("edge_type", "CALLS")
                child_node["edge_status"] = edata.get("status", "VALID")
                child_node["is_await"] = edata.get("flow_type") == "ASYNC" or "await" in edata.get("detail", "")
                child_node["detail"] = edata.get("detail", "")
                node_obj["children"].append(child_node)

            return node_obj

        for n, d in anchor_nodes:
            label = d.get("label", n)
            if label in seen_labels and not list(graph.g.out_edges(n)):
                continue
            seen_labels.add(label)

            ctrl_props = d.get("props", {})
            ctrl_scope = d.get("scope", {})
            tree_data = build_tree_node(n)

            descendants = nx.descendants(graph.g, n)
            bundle_funcs = [funcs_meta[did] for did in descendants if did in funcs_meta]
            if n in funcs_meta:
                bundle_funcs.insert(0, funcs_meta[n])

            bundle_text = graph.to_causal_code_bundle(n)

            ui_trees.append({
                "anchor_id": n,
                "label": label,
                "ui_type": ctrl_props.get("ui_type", d.get("category", "Anchor")),
                "line": ctrl_scope.get("line", 1),
                "tree": tree_data,
                "bundle_count": len(bundle_funcs),
                "bundle_funcs": [f["id"] for f in bundle_funcs],
                "bundle_text": bundle_text,
            })

        # 4. 形式化守衛檢驗
        inv = graph.check_invariants()
        is_passed = inv["passed"]
        verdict_badge = "badge-pass" if is_passed else "badge-danger"
        verdict_text = "🟢 READY_TO_SHIP" if is_passed else "🔴 BLOCKED_BY_INVARIANTS"

        # 5. 序列化 JSON 注入前端
        funcs_json = json.dumps(funcs_meta, ensure_ascii=False)
        trees_json = json.dumps(ui_trees, ensure_ascii=False)
        inv_json = json.dumps(inv, ensure_ascii=False)

        default_select_anchor = ui_trees[0]["anchor_id"] if ui_trees else ""

        html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>{html.escape(display_title)}</title>
  <style>
    :root {{
      --bg: #1e1e2e;
      --card-bg: #252538;
      --tree-bg: #181825;
      --border: #313244;
      --text: #cdd6f4;
      --text-dim: #a6adc8;
      --primary: #89b4fa;
      --accent: #f5c2e7;
      --success: #a6e3a1;
      --warning: #f9e2af;
      --danger: #f38ba8;
      --code-bg: #11111b;
      --btn-bg: #313244;
      --btn-hover: #45475a;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", monospace;
      padding: 16px;
      line-height: 1.5;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 16px;
    }}
    .header h1 {{
      font-size: 18px;
      color: var(--primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .badge {{
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 600;
    }}
    .badge-pass {{
      background: rgba(166, 227, 161, 0.15);
      color: var(--success);
      border: 1px solid var(--success);
    }}
    .badge-danger {{
      background: rgba(243, 139, 168, 0.15);
      color: var(--danger);
      border: 1px solid var(--danger);
    }}
    .stats-bar {{
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
    }}
    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 16px;
      flex: 1;
    }}
    .stat-val {{
      font-size: 20px;
      font-weight: bold;
      color: #fff;
    }}
    .stat-lbl {{
      font-size: 12px;
      color: var(--text-dim);
    }}

    .workspace {{
      display: grid;
      grid-template-columns: 460px 1fr;
      gap: 16px;
      height: calc(100vh - 170px);
      min-height: 550px;
    }}
    @media(max-width: 900px) {{
      .workspace {{ grid-template-columns: 1fr; height: auto; }}
    }}

    /* 左欄: 因果樹 */
    .tree-col {{
      background: var(--tree-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
    }}
    .col-header {{
      padding: 12px 16px;
      background: var(--card-bg);
      border-bottom: 1px solid var(--border);
      font-weight: 600;
      font-size: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 5;
    }}
    .search-input {{
      width: 100%;
      background: var(--code-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 6px 10px;
      border-radius: 4px;
      font-size: 12px;
      margin-top: 8px;
    }}
    .tree-container {{
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .anchor-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 10px;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .anchor-card:hover, .anchor-card.active {{
      border-color: var(--primary);
      background: #2a2a3e;
    }}
    .anchor-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}
    .anchor-title {{
      font-weight: bold;
      color: var(--primary);
      font-size: 13.5px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .btn-bundle {{
      background: var(--btn-bg);
      border: 1px solid var(--border);
      color: var(--warning);
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 4px;
      cursor: pointer;
      font-weight: 600;
    }}
    .btn-bundle:hover {{
      background: var(--btn-hover);
      color: #fff;
    }}

    /* 樹狀結構節點 */
    .tree-node {{
      font-size: 12.5px;
      margin-left: 14px;
      border-left: 1px dashed var(--border);
      padding-left: 10px;
      margin-top: 4px;
    }}
    .node-row {{
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 2px 4px;
      border-radius: 4px;
    }}
    .node-row:hover {{
      background: rgba(255, 255, 255, 0.05);
    }}
    .btn-inspect {{
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-dim);
      font-size: 10.5px;
      padding: 1px 6px;
      border-radius: 3px;
      cursor: pointer;
      margin-left: auto;
    }}
    .btn-inspect:hover {{
      color: var(--accent);
      border-color: var(--accent);
    }}
    .pill-async {{
      color: var(--warning);
      font-size: 10px;
      font-weight: bold;
    }}
    .pill-blocked {{
      color: var(--danger);
      font-size: 10px;
      font-weight: bold;
      background: rgba(243, 139, 168, 0.15);
      padding: 1px 4px;
      border-radius: 3px;
    }}

    /* 右欄: 原始碼預覽器 */
    .code-col {{
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    .code-toolbar {{
      background: var(--card-bg);
      border-bottom: 1px solid var(--border);
      padding: 10px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .code-title {{
      font-size: 14px;
      font-weight: bold;
      color: var(--accent);
    }}
    .code-meta {{
      font-size: 12px;
      color: var(--text-dim);
      display: flex;
      gap: 12px;
    }}
    .btn-copy {{
      background: var(--btn-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 12px;
      cursor: pointer;
    }}
    .btn-copy:hover {{
      background: var(--btn-hover);
    }}
    .code-content {{
      flex: 1;
      overflow: auto;
      padding: 16px;
      font-family: Consolas, "Courier New", monospace;
      font-size: 13px;
      line-height: 1.6;
      white-space: pre;
      color: #bac2de;
    }}
  </style>
</head>
<body>
  <div class="header">
    <h1>
      <span>🌲 CODE-Map 全景語意因果地圖</span>
      <span style="font-size:12px; color:var(--text-dim); font-weight:normal;">({html.escape(target_name)})</span>
    </h1>
    <div class="badge {verdict_badge}">{verdict_text}</div>
  </div>

  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-val">{len(ui_trees)}</div>
      <div class="stat-lbl">錨點數量 (Anchors)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">{len(funcs_meta)}</div>
      <div class="stat-lbl">解析函式 (Functions)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" style="color:{'var(--success)' if is_passed else 'var(--danger)'};">
        {len(inv.get('scope_errors', []))}
      </div>
      <div class="stat-lbl">作用域阻隔 (Scope Errors)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" style="color:{'var(--success)' if not inv.get('hazards', []) else 'var(--warning)'};">
        {len(inv.get('hazards', []))}
      </div>
      <div class="stat-lbl">危害調用 (Hazards)</div>
    </div>
  </div>

  <div class="workspace">
    <!-- 左欄: 因果拓撲樹 -->
    <div class="tree-col">
      <div class="col-header">
        <div>因果調度樹 (Causal Subtrees)</div>
        <span style="font-size:11px; color:var(--text-dim);">{len(ui_trees)} 條業務鏈</span>
      </div>
      <div style="padding: 0 12px;">
        <input type="text" id="searchBox" class="search-input" placeholder="🔍 搜尋控制項、函式或事件...">
      </div>
      <div class="tree-container" id="treeList">
        <!-- JS 動態渲染樹狀清單 -->
      </div>
    </div>

    <!-- 右欄: 外科手術代碼預覽器 -->
    <div class="code-col">
      <div class="code-toolbar">
        <div>
          <div class="code-title" id="codeHeaderTitle">請選擇左側函式或點擊代碼包</div>
          <div class="code-meta" id="codeHeaderMeta">點擊左側 [📦 關聯代碼包] 或 [💻 查看原始碼]</div>
        </div>
        <button class="btn-copy" id="btnCopyCode" onclick="copyCurrentCode()">📋 複製代碼</button>
      </div>
      <div class="code-content" id="codeView">// 代碼將展示於此...</div>
    </div>
  </div>

  <script>
    const funcs = {funcs_json};
    const trees = {trees_json};
    let currentCode = "";
    let activeAnchorId = "{default_select_anchor}";

    function renderTree() {{
      const container = document.getElementById("treeList");
      container.innerHTML = "";
      const filter = document.getElementById("searchBox").value.toLowerCase();

      trees.forEach(t => {{
        if (filter && !t.label.toLowerCase().includes(filter) && !JSON.stringify(t.tree).toLowerCase().includes(filter)) {{
          return;
        }}

        const card = document.createElement("div");
        card.className = "anchor-card" + (t.anchor_id === activeAnchorId ? " active" : "");
        card.id = "card-" + t.anchor_id;

        const header = document.createElement("div");
        header.className = "anchor-header";
        header.innerHTML = `
          <div class="anchor-title">
            <span>🌲</span>
            <span>${{escapeHtml(t.label)}}</span>
            <span style="font-size:11px; color:var(--text-dim);">(${{escapeHtml(t.ui_type)}})</span>
          </div>
          <button class="btn-bundle" onclick="event.stopPropagation(); inspectBundle('${{t.anchor_id}}')">
            📦 關聯 ${{t.bundle_count}} 函式代碼包
          </button>
        `;
        card.appendChild(header);

        // 遞迴渲染子節點
        function renderChildren(node, parentEl) {{
          if (!node.children || node.children.length === 0) return;
          node.children.forEach(c => {{
            const row = document.createElement("div");
            row.className = "tree-node";
            
            const awaitPill = c.is_await ? '<span class="pill-async">⏳ [await]</span>' : '';
            const blockedPill = c.edge_status === "BLOCKED_SCOPE" ? '<span class="pill-blocked">💥 BLOCKED</span>' : '';
            const inspectBtn = c.has_code ? `<button class="btn-inspect" onclick="event.stopPropagation(); inspectFunc('${{c.id}}')">💻 查看原始碼</button>` : '';

            row.innerHTML = `
              <div class="node-row">
                <span>└──</span>
                ${{awaitPill}}
                ${{blockedPill}}
                <span style="color:#a6adc8; font-size:11px;">[${{c.edge_type}}]</span>
                <span style="font-weight:500;">${{escapeHtml(c.label)}}()</span>
                ${{inspectBtn}}
              </div>
            `;
            parentEl.appendChild(row);
            renderChildren(c, row);
          }});
        }}

        renderChildren(t.tree, card);

        card.onclick = () => {{
          inspectBundle(t.anchor_id);
        }};

        container.appendChild(card);
      }});
    }}

    function inspectFunc(funcId) {{
      const meta = funcs[funcId];
      if (!meta) return;

      document.getElementById("codeHeaderTitle").innerText = "🔹 函式: " + meta.label + meta.parameters;
      document.getElementById("codeHeaderMeta").innerText = `行數: L${{meta.line_start}} ~ L${{meta.line_end}} (${{meta.line_count}} 行) | 作用域: ${{meta.scope_id}}`;
      currentCode = meta.source_code;
      document.getElementById("codeView").innerText = meta.source_code;
    }}

    function inspectBundle(anchorId) {{
      activeAnchorId = anchorId;
      document.querySelectorAll(".anchor-card").forEach(c => c.classList.remove("active"));
      const activeEl = document.getElementById("card-" + anchorId);
      if (activeEl) activeEl.classList.add("active");

      const t = trees.find(x => x.anchor_id === anchorId);
      if (!t) return;

      document.getElementById("codeHeaderTitle").innerText = `📦 【${{t.label}}】全因果關聯代碼包`;
      document.getElementById("codeHeaderMeta").innerText = `共涵蓋 ${{t.bundle_count}} 個呼叫實作函式，供 Coding Agent 進行最小切片審查`;
      currentCode = t.bundle_text;
      document.getElementById("codeView").innerText = t.bundle_text;
    }}

    function copyCurrentCode() {{
      if (!currentCode) return;
      navigator.clipboard.writeText(currentCode).then(() => {{
        const btn = document.getElementById("btnCopyCode");
        const oldText = btn.innerText;
        btn.innerText = "✅ 已複製！";
        setTimeout(() => {{ btn.innerText = oldText; }}, 1500);
      }});
    }}

    function escapeHtml(str) {{
      return (str || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }}

    document.getElementById("searchBox").addEventListener("input", renderTree);

    // 初始化渲染
    renderTree();
    if (activeAnchorId) {{
      inspectBundle(activeAnchorId);
    }}
  </script>
</body>
</html>
"""
        with open(out_abs, "w", encoding="utf-8") as f:
            f.write(html_content)

        return out_abs
