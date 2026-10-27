import html
import json
import os
from typing import Any, Dict, List, Optional
import networkx as nx

from code_map.core.graph import CodeMapGraph


class HTMLDashboardReporter:
    """
    全景雙欄互動式 HTML 儀表板生成器 (基於 workspace_file_tree_codemap_v2 風格)
    - 採用與 workspace_file_tree_codemap_v2.html 100% 相同的高質感 Catppuccin 深色主題
    - 左欄：可折疊因果拓撲樹 (UI 控制項 / CLI 入口 / 模組函式)，附帶醒目的「📦 關聯 X 函式代碼包」與「💻 查看原始碼」按鈕
    - 右欄：固定位置代碼切片檢視器，含「📋 複製代碼」、簽章標示、行數範圍與語法區塊
    - 修復 Windows 路徑反斜線轉義與 Marimo 匿名 cell 顯示問題
    """

    def generate(
        self,
        graph: CodeMapGraph,
        output_path: str,
        title: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> str:
        out_abs = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(out_abs), exist_ok=True)
        display_name = os.path.basename(file_path) if file_path else "源碼分析"
        page_title = title or f"CODE-Map 全景語意因果地圖 - {display_name}"

        # 1. 盤點所有函式節點
        funcs_meta: Dict[str, Dict[str, Any]] = {}
        for n, d in graph.g.nodes(data=True):
            if d.get("category") == "FUNCTION_DEF":
                props = d.get("props", {})
                f_scope = d.get("scope", {})
                label = d.get("label", n)
                sig = props.get("signature", label)
                params = props.get("parameters", "()")
                l_start = props.get("line_start", f_scope.get("line", 1))
                l_end = props.get("line_end", f_scope.get("line", 1))
                l_count = props.get("line_count", max(1, l_end - l_start + 1))
                code = props.get("source_code", "")

                # 若是 Marimo cell 的匿名 _，賦予有意義的標籤
                display_label = label
                if label == "_":
                    display_label = f"Cell (L{l_start})"

                funcs_meta[n] = {
                    "id": n,
                    "label": display_label,
                    "raw_label": label,
                    "signature": sig,
                    "parameters": params,
                    "line_start": l_start,
                    "line_end": l_end,
                    "line_count": l_count,
                    "is_async": props.get("is_async", False),
                    "source_code": code,
                    "scope_id": f_scope.get("scope_id", "scope:global"),
                    "class_name": props.get("class_name", ""),
                }

        # 2. 收集錨點 (UI_CONTROL / CLI 入口 / 或無 UI 時的具名函式)
        ui_anchors = graph.get_ui_anchors()
        anchor_nodes = []

        if ui_anchors:
            for n in ui_anchors:
                anchor_nodes.append((n, graph.g.nodes[n]))
        else:
            # 無 UI 控制項 (如後端模組或 Marimo 筆記本):
            # 優先將有具名宣告的函式 (非匿名 _) 以及入度為 0 的根函式作為錨點
            named_funcs = []
            anon_funcs = []
            for n, d in graph.g.nodes(data=True):
                if d.get("category") == "FUNCTION_DEF":
                    lbl = d.get("label", "")
                    if lbl and lbl != "_" and not lbl.endswith("(External/Unresolved)"):
                        named_funcs.append((n, d))
                    elif lbl == "_":
                        anon_funcs.append((n, d))

            if named_funcs:
                anchor_nodes = named_funcs
            elif anon_funcs:
                anchor_nodes = anon_funcs
            else:
                for n, d in list(graph.g.nodes(data=True))[:10]:
                    anchor_nodes.append((n, d))

        # 3. 遞迴構建因果樹
        ui_trees = []
        seen_anchor_labels = set()

        def build_tree_node(curr_id: str, visited: Optional[set] = None) -> Dict[str, Any]:
            if visited is None:
                visited = set()
            c_data = graph.g.nodes.get(curr_id, {})
            c_cat = c_data.get("category", "")
            raw_lbl = c_data.get("label", curr_id)

            disp_lbl = raw_lbl
            if raw_lbl == "_":
                f_scope = c_data.get("scope", {})
                disp_lbl = f"Cell (L{f_scope.get('line', '?')})"

            node_obj = {
                "id": curr_id,
                "label": disp_lbl,
                "category": c_cat,
                "has_code": curr_id in funcs_meta and bool(funcs_meta[curr_id].get("source_code")),
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
            raw_label = d.get("label", n)
            ctrl_props = d.get("props", {})
            ctrl_scope = d.get("scope", {})
            ui_type = ctrl_props.get("ui_type", d.get("category", "Control"))

            disp_label = raw_label
            if raw_label == "_":
                disp_label = f"Cell (L{ctrl_scope.get('line', 1)})"

            if disp_label in seen_anchor_labels and not list(graph.g.out_edges(n)):
                continue
            seen_anchor_labels.add(disp_label)

            tree_data = build_tree_node(n)
            descendants = nx.descendants(graph.g, n)
            bundle_funcs = [funcs_meta[did] for did in descendants if did in funcs_meta]
            if n in funcs_meta and funcs_meta[n] not in bundle_funcs:
                bundle_funcs.insert(0, funcs_meta[n])

            bundle_text = graph.to_causal_code_bundle(n)
            # 若為函式節點且自身有 source_code 但 bundle_text 是預設錯誤時，補齊自身原始碼
            if not bundle_text.strip() or "找不到錨點節點" in bundle_text:
                if n in funcs_meta and funcs_meta[n]["source_code"]:
                    m = funcs_meta[n]
                    bundle_text = f"# 📦 CODE-Map 函式切片: {m['label']}\n\n## 🔹 {m['signature']} (L{m['line_start']}~L{m['line_end']})\n```\n{m['source_code']}\n```"

            ui_trees.append({
                "anchor_id": n,
                "label": disp_label,
                "ui_type": ui_type,
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

        # 5. 安全 JSON 序列化 (防止反斜線路徑字串在 JS 內崩潰)
        funcs_json_str = json.dumps(funcs_meta, ensure_ascii=False)
        trees_json_str = json.dumps(ui_trees, ensure_ascii=False)

        # 6. 生成與 workspace_file_tree_codemap_v2.html 一致的完整自包含 HTML
        html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>{html.escape(page_title)}</title>
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
      --drawer-bg: #1e1e2e;
      --btn-bg: #313244;
      --btn-hover: #45475a;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
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
      font-size: 19px;
      color: var(--primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .header h1 span {{
      font-size: 13px;
      color: var(--text-dim);
      font-weight: normal;
    }}
    .badge-pass {{
      background: rgba(166, 227, 161, 0.15);
      color: var(--success);
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 600;
      border: 1px solid var(--success);
    }}
    .badge-danger {{
      background: rgba(243, 139, 168, 0.15);
      color: var(--danger);
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 600;
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
      color: var(--primary);
    }}
    .stat-label {{
      font-size: 11px;
      color: var(--text-dim);
    }}
    .filter-bar {{
      display: flex;
      gap: 10px;
      margin-bottom: 14px;
    }}
    .search-input {{
      flex: 1;
      background: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 13px;
      outline: none;
    }}
    .search-input:focus {{
      border-color: var(--primary);
    }}
    .layout {{
      display: flex;
      gap: 16px;
      align-items: flex-start;
    }}
    .tree-col {{
      flex: 1.1;
      background: var(--tree-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 12.5px;
      overflow-x: auto;
      max-height: 720px;
      overflow-y: auto;
    }}
    .code-col {{
      flex: 0.9;
      background: var(--drawer-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      position: sticky;
      top: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-height: 720px;
    }}
    .tree-item {{
      margin-bottom: 4px;
    }}
    .node-row {{
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 5px 8px;
      border-radius: 5px;
      cursor: pointer;
      user-select: none;
      transition: background 0.1s;
    }}
    .node-row:hover {{
      background: rgba(255, 255, 255, 0.06);
    }}
    .node-row.active {{
      background: rgba(137, 180, 250, 0.2) !important;
      border-left: 3px solid var(--primary);
    }}
    .tag-ctrl {{
      color: #89dceb;
      font-weight: 700;
    }}
    .tag-btn {{
      color: #89b4fa;
      font-weight: 700;
      background: rgba(137, 180, 250, 0.15);
      padding: 1px 7px;
      border-radius: 4px;
      border: 1px solid rgba(137, 180, 250, 0.3);
    }}
    .tag-event {{
      color: #f9e2af;
      font-weight: 600;
    }}
    .tag-func {{
      color: #a6e3a1;
      font-weight: 600;
    }}
    .tag-await {{
      color: #fab387;
      font-size: 10px;
      font-weight: bold;
      background: rgba(250, 179, 135, 0.15);
      padding: 0 4px;
      border-radius: 3px;
    }}
    .tag-blocked {{
      color: #f38ba8;
      font-size: 10px;
      font-weight: bold;
      background: rgba(243, 139, 168, 0.15);
      padding: 0 4px;
      border-radius: 3px;
      border: 1px solid var(--danger);
    }}
    .tag-type {{
      font-size: 11px;
      color: var(--text-dim);
      background: var(--card-bg);
      padding: 1px 5px;
      border-radius: 3px;
      border: 1px solid var(--border);
    }}
    
    /* 核心操作按鈕 */
    .btn-action-code {{
      margin-left: auto;
      background: #89b4fa;
      color: #11111b;
      border: none;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: bold;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.3);
      transition: all 0.15s;
    }}
    .btn-action-code:hover {{
      background: #b4befe;
      transform: translateY(-1px);
    }}
    .btn-bundle-code {{
      margin-left: 6px;
      background: rgba(245, 194, 231, 0.2);
      color: var(--accent);
      border: 1px solid var(--accent);
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
    }}
    .btn-bundle-code:hover {{
      background: var(--accent);
      color: #11111b;
    }}

    .sub-tree {{
      margin-left: 18px;
      border-left: 1px dashed var(--border);
      padding-left: 8px;
    }}
    .arrow {{
      color: var(--text-dim);
      font-size: 10px;
      display: inline-block;
      width: 12px;
      transition: transform 0.15s;
    }}
    .collapsed > .sub-tree {{ display: none; }}
    .collapsed > .node-row .arrow {{ transform: rotate(-90deg); }}
    
    /* Code Viewer Panel */
    .code-title {{
      font-size: 14px;
      font-weight: bold;
      color: var(--primary);
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border);
    }}
    .code-meta {{
      font-size: 12px;
      color: var(--text);
      background: var(--card-bg);
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .code-box {{
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 12px;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 12px;
      color: #cdd6f4;
      overflow-y: auto;
      max-height: 520px;
      white-space: pre;
      line-height: 1.45;
    }}
    .copy-btn {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 3px 9px;
      border-radius: 4px;
      font-size: 11px;
      cursor: pointer;
    }}
    .copy-btn:hover {{
      border-color: var(--primary);
      color: var(--primary);
    }}
  </style>
</head>
<body>

  <div class="header">
    <h1>🌲 CODE-Map 全景語意因果地圖 <span>({html.escape(display_name)})</span></h1>
    <div class="{verdict_badge}">{verdict_text}</div>
  </div>

  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-val">{len(ui_trees)}</div>
      <div class="stat-label">錨點/入口數量 (Anchors)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">{len(funcs_meta)}</div>
      <div class="stat-label">已截取原始碼函式 (NetworkX Props)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" style="color:{'var(--success)' if not inv.get('scope_errors') else 'var(--danger)'};">{len(inv.get('scope_errors', []))}</div>
      <div class="stat-label">作用域阻隔 (Scope Errors)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val" style="color:{'var(--success)' if not inv.get('hazards') else 'var(--warning)'};">{len(inv.get('hazards', []))}</div>
      <div class="stat-label">危害調用 (Hazards)</div>
    </div>
  </div>

  <div class="filter-bar">
    <input type="text" id="searchInput" class="search-input" placeholder="🔍 即時搜尋控制項、按鈕、CLI 或函式名稱..." oninput="filterTree()">
  </div>

  <div class="layout">
    <div class="tree-col" id="treeRoot">
      <!-- 樹狀控制項將透過 JavaScript 動態渲染 -->
    </div>

    <div class="code-col" id="codePanel">
      <div class="code-title">
        <span id="panelTitle">💻 程式碼切片檢視器</span>
        <button class="copy-btn" id="copyCodeBtn" onclick="copyCode()">複製代碼 📋</button>
      </div>
      <div id="inspectorContent">
        <!-- 預設載入首個錨點之代碼 -->
      </div>
    </div>
  </div>

  <script>
    const uiData = {trees_json_str};
    const funcsData = {funcs_json_str};

    let currentSourceCode = "";

    function renderTree() {{
      const root = document.getElementById('treeRoot');
      root.innerHTML = '';

      uiData.forEach((item, idx) => {{
        const itemEl = document.createElement('div');
        itemEl.className = 'tree-item';
        itemEl.dataset.label = item.label.toLowerCase();
        itemEl.id = 'anchor-' + idx;

        const row = document.createElement('div');
        row.className = 'node-row';
        row.id = 'row-anchor-' + idx;

        const arrow = document.createElement('span');
        arrow.className = 'arrow';
        arrow.textContent = (item.tree.children && item.tree.children.length > 0) ? '▼' : '';
        row.appendChild(arrow);

        const ctrlTag = document.createElement('span');
        ctrlTag.className = (item.ui_type === 'Button' || item.ui_type === 'CLI Entry') ? 'tag-btn' : 'tag-ctrl';
        ctrlTag.textContent = item.label;
        row.appendChild(ctrlTag);

        const typeTag = document.createElement('span');
        typeTag.className = 'tag-type';
        typeTag.textContent = item.ui_type + ' @ L' + item.line;
        row.appendChild(typeTag);

        // 整包因果代碼 (Bundle) 按鈕
        if (item.bundle_count > 0) {{
          const bundleBtn = document.createElement('button');
          bundleBtn.className = 'btn-bundle-code';
          bundleBtn.textContent = '📦 關聯 ' + item.bundle_count + ' 函式代碼包';
          bundleBtn.title = '查看該錨點觸發的所有函式原始碼集合';
          bundleBtn.onclick = (e) => {{
            e.stopPropagation();
            showBundle(item, row);
          }};
          row.appendChild(bundleBtn);
        }}

        // 若錨點本身就是函式且具備源碼，渲染查看按鈕
        if (funcsData[item.anchor_id]) {{
          const inspectBtn = document.createElement('button');
          inspectBtn.className = 'btn-action-code';
          inspectBtn.innerHTML = '💻 查看原始碼';
          inspectBtn.onclick = (e) => {{
            e.stopPropagation();
            inspectFunction(item.anchor_id, row);
          }};
          row.appendChild(inspectBtn);
        }}

        row.onclick = (e) => {{
          if (e.target.tagName !== 'BUTTON') {{
            toggleCollapse(itemEl);
            if (item.bundle_count > 0) showBundle(item, row);
            else if (funcsData[item.anchor_id]) inspectFunction(item.anchor_id, row);
          }}
        }};

        itemEl.appendChild(row);

        const subTree = document.createElement('div');
        subTree.className = 'sub-tree';
        renderChildren(item.tree.children, subTree);
        itemEl.appendChild(subTree);

        root.appendChild(itemEl);
      }});
    }}

    function renderChildren(children, parentEl) {{
      if (!children || children.length === 0) return;

      children.forEach(c => {{
        const wrap = document.createElement('div');
        wrap.className = 'tree-item';

        const row = document.createElement('div');
        row.className = 'node-row';

        const arrow = document.createElement('span');
        arrow.className = 'arrow';
        arrow.textContent = (c.children && c.children.length > 0) ? '▼' : '';
        row.appendChild(arrow);

        if (c.children && c.children.length > 0) {{
          row.onclick = (e) => {{
            if (e.target.tagName !== 'BUTTON') toggleCollapse(wrap);
          }};
        }}

        if (c.is_await) {{
          const awaitTag = document.createElement('span');
          awaitTag.className = 'tag-await';
          awaitTag.textContent = '⏳ await';
          row.appendChild(awaitTag);
        }}

        if (c.edge_status === 'BLOCKED_SCOPE') {{
          const blockedTag = document.createElement('span');
          blockedTag.className = 'tag-blocked';
          blockedTag.textContent = '💥 BLOCKED';
          row.appendChild(blockedTag);
        }}

        const nameTag = document.createElement('span');
        if (c.category === 'EVENT_BINDING') {{
          nameTag.className = 'tag-event';
          nameTag.textContent = '⚡ ' + c.label;
        }} else if (c.category === 'FUNCTION_DEF') {{
          nameTag.className = 'tag-func';
          nameTag.textContent = '🔒 ' + c.label + '()';
          row.onclick = (e) => {{
            if (e.target.tagName !== 'BUTTON') {{
              if (c.has_code) inspectFunction(c.id, row);
              if (c.children && c.children.length > 0) toggleCollapse(wrap);
            }}
          }};
        }} else {{
          nameTag.textContent = c.label;
        }}
        row.appendChild(nameTag);

        // 如果是函式節點且具備代碼，渲染查看原始碼按鈕
        if (c.has_code) {{
          const inspectBtn = document.createElement('button');
          inspectBtn.className = 'btn-action-code';
          inspectBtn.innerHTML = '💻 查看原始碼';
          inspectBtn.onclick = (e) => {{
            e.stopPropagation();
            inspectFunction(c.id, row);
          }};
          row.appendChild(inspectBtn);
        }}

        wrap.appendChild(row);

        if (c.children && c.children.length > 0) {{
          const sub = document.createElement('div');
          sub.className = 'sub-tree';
          renderChildren(c.children, sub);
          wrap.appendChild(sub);
        }}

        parentEl.appendChild(wrap);
      }});
    }}

    function toggleCollapse(el) {{
      el.classList.toggle('collapsed');
    }}

    function inspectFunction(funcId, rowEl) {{
      document.querySelectorAll('.node-row').forEach(r => r.classList.remove('active'));
      if (rowEl) rowEl.classList.add('active');

      const meta = funcsData[funcId];
      if (!meta) return;

      currentSourceCode = meta.source_code;
      document.getElementById('panelTitle').textContent = '💻 函式實作: ' + meta.label + '()';
      document.getElementById('copyCodeBtn').style.display = 'block';

      const panel = document.getElementById('inspectorContent');
      panel.innerHTML = `
        <div class="code-meta">
          <div><strong>函式簽章:</strong> <span style="color:var(--primary)">${{escapeHtml(meta.signature)}}</span></div>
          <div><strong>精確範圍:</strong> L${{meta.line_start}} ~ L${{meta.line_end}} (共 ${{meta.line_count}} 行)</div>
          <div><strong>執行型別:</strong> ${{meta.is_async ? '⚡ async function (非同步 Promise)' : '同步一般函式'}}</div>
          <div><strong>作用空間:</strong> ${{escapeHtml(meta.scope_id)}}</div>
        </div>
        <div class="code-box">${{escapeHtml(meta.source_code)}}</div>
      `;
    }}

    function showBundle(item, rowEl) {{
      document.querySelectorAll('.node-row').forEach(r => r.classList.remove('active'));
      if (rowEl) rowEl.classList.add('active');

      currentSourceCode = item.bundle_text;
      document.getElementById('panelTitle').textContent = '📦 ' + item.label + ' 因果代碼包 (共 ' + item.bundle_count + ' 函式)';
      document.getElementById('copyCodeBtn').style.display = 'block';

      const panel = document.getElementById('inspectorContent');
      panel.innerHTML = `
        <div class="code-meta">
          <div><strong>錨點/入口:</strong> <span style="color:var(--primary)">${{escapeHtml(item.label)}} (${{escapeHtml(item.ui_type)}})</span></div>
          <div><strong>關聯函式:</strong> 共 ${{item.bundle_count}} 個呼叫實作函式已由 NetworkX 打包</div>
        </div>
        <div class="code-box">${{escapeHtml(item.bundle_text)}}</div>
      `;
    }}

    function copyCode() {{
      if (currentSourceCode) {{
        navigator.clipboard.writeText(currentSourceCode);
        const btn = document.getElementById('copyCodeBtn');
        const orig = btn.textContent;
        btn.textContent = '✅ 已複製！';
        setTimeout(() => {{ btn.textContent = orig; }}, 1500);
      }}
    }}

    function escapeHtml(str) {{
      return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }}

    function filterTree() {{
      const query = document.getElementById('searchInput').value.toLowerCase().trim();
      document.querySelectorAll('#treeRoot > .tree-item').forEach(el => {{
        const text = el.textContent.toLowerCase();
        if (!query || text.includes(query)) {{
          el.style.display = 'block';
        }} else {{
          el.style.display = 'none';
        }}
      }});
    }}

    // 初始化渲染
    renderTree();

    // 預設高亮第一個錨點或優先選擇核心函式
    if (uiData.length > 0) {{
      let defaultIdx = 0;
      const targetIdx = uiData.findIndex(d => d.label.includes('Delete') || d.label.includes('main') || d.label.includes('clean_text') || d.label.includes('safe_parse'));
      if (targetIdx !== -1) defaultIdx = targetIdx;

      const targetItem = uiData[defaultIdx];
      const targetRow = document.getElementById('row-anchor-' + defaultIdx);
      if (targetItem.bundle_count > 0) {{
        showBundle(targetItem, targetRow);
      }} else if (funcsData[targetItem.anchor_id]) {{
        inspectFunction(targetItem.anchor_id, targetRow);
      }}
    }}
  </script>
</body>
</html>
"""
        with open(out_abs, "w", encoding="utf-8") as f:
            f.write(html_content)

        return out_abs
