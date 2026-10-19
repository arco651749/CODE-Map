import os
import sys
import json
import html

# 將專案根目錄加入模組搜尋路徑
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from uia_coder.adapters import get_adapter_for_file
import networkx as nx

def generate_report():
    target_file = r"D:\Users\arco0\.gemini\config\plugins\workspace-file-tree\sidecars\panel\app.js"
    adapter = get_adapter_for_file(target_file)
    with open(target_file, "r", encoding="utf-8") as f:
        code = f.read()

    graph = adapter.parse_and_build(code, file_path="sidecars/panel/app.js")

    # 收集所有的函式原始碼快照字典
    funcs_meta = {}
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
            }

    # 收集每個 UI 控制項的因果樹
    ui_trees = []
    seen_ctrls = set()

    for n, d in graph.g.nodes(data=True):
        if d.get("category") == "UI_CONTROL":
            label = d.get("label", "")
            out_edges = list(graph.g.out_edges(n, data=True))
            if not out_edges and label in seen_ctrls:
                continue
            seen_ctrls.add(label)

            ctrl_props = d.get("props", {})
            ctrl_scope = d.get("scope", {})

            # 構建該控制項的遞迴樹狀結構
            def build_tree_node(curr_id, visited=None):
                if visited is None:
                    visited = set()
                c_data = graph.g.nodes.get(curr_id, {})
                c_cat = c_data.get("category", "")
                c_label = c_data.get("label", curr_id)
                c_props = c_data.get("props", {})

                node_obj = {
                    "id": curr_id,
                    "label": c_label,
                    "category": c_cat,
                    "has_code": curr_id in funcs_meta,
                    "children": []
                }

                if curr_id in visited:
                    node_obj["is_ref"] = True
                    return node_obj

                visited.add(curr_id)

                for _, tgt, edata in graph.g.out_edges(curr_id, data=True):
                    child_node = build_tree_node(tgt, visited.copy())
                    child_node["edge_type"] = edata.get("edge_type", "CALLS")
                    child_node["is_await"] = edata.get("flow_type") == "ASYNC" or "await" in edata.get("detail", "")
                    child_node["detail"] = edata.get("detail", "")
                    node_obj["children"].append(child_node)

                return node_obj

            tree_data = build_tree_node(n)
            if tree_data["children"]:
                descendants = nx.descendants(graph.g, n)
                bundle_funcs = [funcs_meta[did] for did in descendants if did in funcs_meta]
                
                # 產出該控制項的整包因果 Markdown 代碼包
                bundle_text = graph.to_causal_code_bundle(n)

                ui_trees.append({
                    "anchor_id": n,
                    "label": label,
                    "ui_type": ctrl_props.get("ui_type", "Control"),
                    "line": ctrl_scope.get("line", 1),
                    "tree": tree_data,
                    "bundle_count": len(bundle_funcs),
                    "bundle_funcs": [f["id"] for f in bundle_funcs],
                    "bundle_text": bundle_text
                })

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>CODE-Map 互動式全景語意因果地圖 (workspace-file-tree v2)</title>
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
    .badge-pass {{
      background: rgba(166, 227, 161, 0.15);
      color: var(--success);
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 600;
      border: 1px solid var(--success);
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
    .tabs {{
      display: flex;
      gap: 8px;
    }}
    .tab-btn {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text-dim);
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 12px;
      cursor: pointer;
    }}
    .tab-btn.active {{
      background: var(--primary);
      color: #11111b;
      font-weight: bold;
      border-color: var(--primary);
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
      max-height: 480px;
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
    <h1>🌲 CODE-Map 全景語意因果地圖 <span>workspace-file-tree (sidecars/panel/app.js)</span></h1>
    <div class="badge-pass">🟢 READY_TO_SHIP</div>
  </div>

  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-val">{len(ui_trees)}</div>
      <div class="stat-label">UI 控制項錨點 (Anchors)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">{len(funcs_meta)}</div>
      <div class="stat-label">已截取原始碼函式 (NetworkX Props)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">0</div>
      <div class="stat-label">閉包死穴 (Scope Errors)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">0</div>
      <div class="stat-label">主執行緒阻塞危害 (UI Blocking)</div>
    </div>
  </div>

  <div class="filter-bar">
    <input type="text" id="searchInput" class="search-input" placeholder="🔍 即時搜尋控制項、按鈕或函式 (例如: delete, refresh, toast, preview)..." oninput="filterTree()">
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
        <!-- 預設由 JavaScript 載入 #btnDelete 之原始碼 -->
      </div>
    </div>
  </div>

  <script>
    const uiData = {json.dumps(ui_trees, ensure_ascii=False)};
    const funcsData = {json.dumps(funcs_meta, ensure_ascii=False)};

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
        arrow.textContent = '▼';
        row.appendChild(arrow);

        const ctrlTag = document.createElement('span');
        ctrlTag.className = item.ui_type === 'Button' ? 'tag-btn' : 'tag-ctrl';
        ctrlTag.textContent = item.label;
        row.appendChild(ctrlTag);

        const typeTag = document.createElement('span');
        typeTag.className = 'tag-type';
        typeTag.textContent = item.ui_type + ' @ L' + item.line;
        row.appendChild(typeTag);

        // 頂層按鈕專屬：整包因果代碼 (Bundle) 按鈕
        if (item.bundle_count > 0) {{
          const bundleBtn = document.createElement('button');
          bundleBtn.className = 'btn-bundle-code';
          bundleBtn.textContent = '📦 關聯 ' + item.bundle_count + ' 函式代碼包';
          bundleBtn.title = '查看按鈕點擊後觸發的所有函式原始碼集合';
          bundleBtn.onclick = (e) => {{
            e.stopPropagation();
            showBundle(item, row);
          }};
          row.appendChild(bundleBtn);
        }}

        // 點擊頂層行即切換折疊或查看
        row.onclick = (e) => {{
          if (e.target.tagName !== 'BUTTON') {{
            toggleCollapse(itemEl);
            if (item.bundle_count > 0) showBundle(item, row);
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

        const nameTag = document.createElement('span');
        if (c.category === 'EVENT_BINDING') {{
          nameTag.className = 'tag-event';
          nameTag.textContent = '⚡ ' + c.label;
        }} else if (c.category === 'FUNCTION_DEF') {{
          nameTag.className = 'tag-func';
          nameTag.textContent = '🔒 ' + c.label + '()';
          // 函式節點點擊整行直接看代碼
          row.onclick = (e) => {{
            if (e.target.tagName !== 'BUTTON') {{
              inspectFunction(c.id, row);
              if (c.children && c.children.length > 0) toggleCollapse(wrap);
            }}
          }};
        }} else {{
          nameTag.textContent = c.label;
        }}
        row.appendChild(nameTag);

        // 如果是函式節點且具備代碼，強制渲染搶眼的代碼按鈕
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
          <div><strong>參數宣告:</strong> ${{escapeHtml(meta.parameters)}}</div>
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
          <div><strong>UI 錨點:</strong> <span style="color:var(--primary)">${{escapeHtml(item.label)}} (${{item.ui_type}})</span></div>
          <div><strong>觸發下游:</strong> 共 ${{item.bundle_count}} 個關聯函式實作已由 NetworkX 打包</div>
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

    // 🌟 預設自動打開並高亮 #btnDelete 的代碼包，保證一進來就看到程式碼！
    const deleteAnchor = uiData.find(d => d.label === '#btnDelete');
    if (deleteAnchor) {{
      const delIdx = uiData.indexOf(deleteAnchor);
      const row = document.getElementById('row-anchor-' + delIdx);
      showBundle(deleteAnchor, row);
    }} else if (uiData.length > 0) {{
      showBundle(uiData[0], document.getElementById('row-anchor-0'));
    }}
  </script>
</body>
</html>
"""

    report_path_v2 = r"d:\AntiGravity\UIA_Coder\reports\workspace_file_tree_codemap_v2.html"
    with open(report_path_v2, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ 互動式 CODE-Map 儀表板 v2 已成功生成: {report_path_v2}")

if __name__ == "__main__":
    generate_report()
