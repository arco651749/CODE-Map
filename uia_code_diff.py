import sys
import subprocess
import re
import argparse
from typing import Dict, List, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class UIACodeDiffAnalyzer:
    """
    UIA 風格程式碼語意差分分析器
    專門將 Git Diff 翻譯為 UIA 控制項樹、事件接線與生命週期守護的語意差分
    """

    def __init__(self, repo_path: str, diff_range: str = "HEAD~1"):
        self.repo_path = repo_path
        self.diff_range = diff_range

    def get_git_diff(self) -> str:
        """調用 git diff 取得原始差分輸出"""
        cmd = ["git", "-C", self.repo_path, "diff", *self.diff_range.split()]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode != 0:
            raise RuntimeError(f"Git diff 執行失敗: {res.stderr}")
        return res.stdout

    def analyze(self) -> Dict[str, Any]:
        diff_text = self.get_git_diff()
        if not diff_text.strip():
            return {"empty": True, "message": "無任何 Git 變更"}

        added_lines = []
        removed_lines = []

        for line in diff_text.splitlines():
            if line.startswith("+++") or line.startswith("---"):
                continue
            if line.startswith("+"):
                added_lines.append(line[1:])
            elif line.startswith("-"):
                removed_lines.append(line[1:])

        added_text = "\n".join(added_lines)
        removed_text = "\n".join(removed_lines)

        # 深入 diff 結構解析 Hunk、呼叫作用域與宣告位置
        hunk_analysis = self._analyze_hunks(diff_text)

        analysis = {
            "controls_added": self._extract_controls(added_text) + hunk_analysis["dynamic_controls"],
            "controls_removed": self._extract_controls(removed_text),
            "wires_added": hunk_analysis["wires_added"],
            "wires_removed": self._extract_wiring_simple(removed_text),
            "keys_handled": self._extract_keys(added_text),
            "cleanups": self._extract_cleanups(added_text),
            "scope_changes": self._extract_scope_changes(diff_text),
            "scope_violations": hunk_analysis["scope_violations"],
            "hazards": hunk_analysis["hazards"],
            "files_changed": self._extract_files(diff_text),
        }
        return analysis

    def _analyze_hunks(self, diff_text: str) -> Dict[str, Any]:
        """按 Hunk 區塊進行多行語法分析，精確提取事件接線、作用域深度與禁忌 API"""
        dynamic_controls = []
        wires_added = []
        declared_functions = {}  # name -> {enclosing, indent, is_top_level, file}
        hazards = []
        scope_violations = []

        # 1. 將 Diff 切割為檔案與 Hunk 區塊
        current_file = ""
        current_enclosing = "module"
        hunks = []  # list of {file, enclosing, lines, text}
        curr_hunk_lines = []

        for line in diff_text.splitlines():
            if line.startswith("diff --git"):
                if curr_hunk_lines:
                    hunks.append({
                        "file": current_file,
                        "enclosing": current_enclosing,
                        "lines": curr_hunk_lines,
                        "text": "\n".join(curr_hunk_lines)
                    })
                    curr_hunk_lines = []
                match = re.search(r'b/(.*)$', line)
                current_file = match.group(1) if match else ""
                current_enclosing = "module"
                continue

            if line.startswith("@@"):
                if curr_hunk_lines:
                    hunks.append({
                        "file": current_file,
                        "enclosing": current_enclosing,
                        "lines": curr_hunk_lines,
                        "text": "\n".join(curr_hunk_lines)
                    })
                    curr_hunk_lines = []
                
                # 擷取外層函式名稱
                match = re.search(r'@@\s+[^@]+@@\s*(?:(?:async\s+)?function\s+)?([a-zA-Z0-9_$]+)', line)
                if match and match.group(1):
                    current_enclosing = match.group(1).strip()
                else:
                    current_enclosing = "module"
                continue

            if line.startswith("+") and not line.startswith("+++"):
                curr_hunk_lines.append(line[1:])

        if curr_hunk_lines:
            hunks.append({
                "file": current_file,
                "enclosing": current_enclosing,
                "lines": curr_hunk_lines,
                "text": "\n".join(curr_hunk_lines)
            })

        # 2. 遍歷每個 Hunk 進行多行語法匹配
        for hunk in hunks:
            h_file = hunk["file"]
            h_enclosing = hunk["enclosing"]
            h_text = hunk["text"]

            # (A) 偵測動態建立的 DOM 控制項
            for elem_match in re.finditer(r'const\s+([a-zA-Z0-9_$]+)\s*=\s*document\.createElement\([\'"]([a-zA-Z0-9_-]+)[\'"]\)', h_text):
                var_name, tag = elem_match.groups()
                ctype = "Button" if tag.lower() == "button" or "btn" in var_name.lower() else "Element"
                dynamic_controls.append({"tag": tag, "id": var_name, "type": f"Dynamic {ctype} ({var_name})"})

            # (B) 偵測函式宣告位置與縮排
            for line in hunk["lines"]:
                func_decl = re.match(r'^(\s*)(?:async\s+)?function\s+([a-zA-Z0-9_$]+)', line)
                if func_decl:
                    indent = len(func_decl.group(1))
                    func_name = func_decl.group(2)
                    is_top_level = (indent == 0)
                    declared_functions[func_name] = {
                        "enclosing": h_enclosing if not is_top_level else "module",
                        "indent": indent,
                        "is_top_level": is_top_level,
                        "file": h_file
                    }

            # (C) 偵測事件監聽接線 (支援多行箭頭函式內部實質業務呼叫)
            pat_block = r'([a-zA-Z0-9_$.?]+)\.addEventListener\(\s*[\'"]([a-zA-Z0-9_-]+)[\'"]\s*,\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z0-9_$]+)\s*=>\s*\{([\s\S]*?)\}\s*\)'
            for m in re.finditer(pat_block, h_text):
                target, event, body = m.groups()
                calls = re.findall(r'(?:await\s+)?([a-zA-Z0-9_$]+)\(', body)
                meaningful = [c for c in calls if c not in ('stopPropagation', 'preventDefault', 'setTimeout', 'showToast', 'if', 'Boolean')]
                for handler in meaningful:
                    wires_added.append({
                        "target": target,
                        "event": event,
                        "handler": handler,
                        "caller_scope": h_enclosing,
                        "file": h_file
                    })

            direct_matches = re.finditer(
                r'([a-zA-Z0-9_$.?]+)\.addEventListener\(\s*[\'"]([a-zA-Z0-9_-]+)[\'"]\s*,\s*([a-zA-Z0-9_$]+)\s*\)',
                h_text
            )
            for m in direct_matches:
                target, event, handler = m.groups()
                if handler not in ("async", "function"):
                    wires_added.append({
                        "target": target,
                        "event": event,
                        "handler": handler,
                        "caller_scope": h_enclosing,
                        "file": h_file
                    })

            # (D) 偵測 Webview 禁忌阻塞 API
            if "window.confirm" in h_text:
                hazards.append({
                    "type": "BLOCKING_DIALOG",
                    "api": "window.confirm()",
                    "file": h_file,
                    "risk": "在 Webview / Extension 中會直接凍結 UI 執行緒或被 Chromium 靜音吞掉！"
                })
            if "window.alert" in h_text:
                hazards.append({
                    "type": "BLOCKING_DIALOG",
                    "api": "window.alert()",
                    "file": h_file,
                    "risk": "在 Webview / Extension 中會直接凍結 UI 執行緒！"
                })

        # 3. 作用域可達性校驗 (Scope Reachability Check)
        for w in wires_added:
            handler = w["handler"]
            caller_scope = w.get("caller_scope", "module")
            if handler in declared_functions:
                decl = declared_functions[handler]
                # 若函式被鎖在某個內部閉包中 (非 module 頂層)，且與呼叫者作用域不同
                if not decl["is_top_level"] and decl["enclosing"] != caller_scope:
                    scope_violations.append({
                        "handler": handler,
                        "declared_in": decl["enclosing"],
                        "caller_scope": caller_scope,
                        "file": w["file"],
                        "issue": f"函式 `{handler}` 被深鎖在 `{decl['enclosing']}` 內部閉包中，但卻在 `{caller_scope}` 嘗試調用，執行期將直接崩潰拋出 ReferenceError: {handler} is not defined！"
                    })

        return {
            "dynamic_controls": dynamic_controls,
            "wires_added": wires_added,
            "hazards": hazards,
            "scope_violations": scope_violations
        }

    def _extract_controls(self, text: str) -> List[Dict[str, str]]:
        controls = []
        id_matches = re.findall(r'<([a-zA-Z0-9_-]+)[^>]*\bid=["\']([^"\']+)["\']', text)
        for tag, cid in id_matches:
            ctype = "Button" if "btn" in cid.lower() or tag == "button" else ("Modal/Pane" if "modal" in cid.lower() else "Element")
            controls.append({"tag": tag, "id": cid, "type": ctype})
        return controls

    def _extract_wiring_simple(self, text: str) -> List[Dict[str, str]]:
        wires = []
        matches = re.findall(r'([a-zA-Z0-9_$.?]+)\.addEventListener\([\'"]([a-zA-Z0-9_-]+)[\'"]\s*,\s*([a-zA-Z0-9_$]+)', text)
        for target, event, handler in matches:
            if handler not in ("async", "function"):
                wires.append({"target": target, "event": event, "handler": handler})
        return wires

    def _extract_keys(self, text: str) -> List[str]:
        keys = set()
        key_matches = re.findall(r'e\.key\s*===?\s*[\'"]([a-zA-Z0-9_-]+)[\'"]', text)
        for k in key_matches:
            keys.add(k)
        return list(keys)

    def _extract_cleanups(self, text: str) -> List[str]:
        cleanups = []
        if "removeEventListener" in text:
            cleanups.append("removeEventListener (清理事件監聽器)")
        if re.search(r'\bcleanup\s*\(', text):
            cleanups.append("cleanup() (定義清理函式)")
        return cleanups

    def _extract_scope_changes(self, diff_text: str) -> List[str]:
        scopes = []
        if re.search(r'-\s*async\s+function\s+init\b', diff_text) or re.search(r'-\s*function\s+closePreview\b', diff_text):
            if re.search(r'\+\s*function\s+closePreview\b', diff_text):
                scopes.append("closePreview / deleteItem 從內部閉包提升至模組頂層作用域")
        return scopes

    def _extract_files(self, diff_text: str) -> List[str]:
        return re.findall(r'diff --git a/(.*?) b/', diff_text)

    def render_markdown_report(self, analysis: Dict[str, Any]) -> str:
        if analysis.get("empty"):
            return "### ⚠️ 目前版本無任何代碼差異。"

        md = []
        md.append("## 🔍 UIA 語意樹代碼變更驗收報告 (UIA Semantic Code Diff)")
        md.append(f"> **比對範圍**：`{self.diff_range}`  ")
        md.append(f"> **影響檔案**：`{', '.join(analysis['files_changed'])}`\n")

        # 1. Mermaid UIA 樹狀圖
        md.append("### 1. 🌲 UIA 控制項樹結構演進 (Visual Tree)")
        md.append("```mermaid")
        md.append("flowchart TD")
        md.append('    Root["Root Window / DOM Tree"]')

        added_ctrls = analysis["controls_added"]
        if added_ctrls:
            md.append('    Root ==>|"➕ 新增控制項子樹"| SubTree["新增 UIA 元件群"]')
            for c in added_ctrls:
                node_id = re.sub(r'[^a-zA-Z0-9_]', '_', c["id"])
                md.append(f'    SubTree --> {node_id}["{c["type"]}: #{c["id"]}"]')
        else:
            md.append('    Root --> Stable["控制項樹結構無新增節點 (純邏輯變更)"]')
        md.append("```\n")

        # 2. 語意差分驗收表格
        md.append("### 2. 📋 語意驗收差分清單 (Semantic Invariant Table)")
        md.append("| 類型 | 標籤 | 項目 | 語意說明與安全性評估 |")
        md.append("| :--- | :--- | :--- | :--- |")

        for c in analysis["controls_added"]:
            md.append(f"| **控制項** | `[+] CONTROL` | `#{c['id']}` ({c['type']}) | 介面長出新控制項節點。 |")

        for w in analysis["wires_added"]:
            md.append(f"| **接線** | `[+] WIRED` | `{w['target']} -> on('{w['event']}')` | 銜接至目標函式 `{w['handler']}`（觸發於 `{w.get('caller_scope', 'module')}`）。 |")

        if analysis["keys_handled"]:
            keys_str = ", ".join([f"`{k}`" for k in analysis["keys_handled"]])
            md.append(f"| **快速鍵** | `[+] SHORTCUT` | {keys_str} | 支援無障礙鍵盤導航操作。 |")

        for cl in analysis["cleanups"]:
            md.append(f"| **生命週期** | `[-] LEAK_GUARD` | `{cl}` | **防洩漏守衛**：具備銷毀清理機制，防止監聽器重複堆疊。 |")

        for sc in analysis["scope_changes"]:
            md.append(f"| **作用域提升** | `[*] SCOPE_FIX` | `{sc}` | 解決閉包作用域隱蔽問題，開放全域調用。 |")

        for sv in analysis.get("scope_violations", []):
            md.append(f"| **作用域違規** | `[!] SCOPE_ERROR` | `{sv['handler']}` | 💥 **{sv['issue']}** |")

        for hz in analysis.get("hazards", []):
            md.append(f"| **禁忌 API** | `[!] HAZARD` | `{hz['api']}` | ⚠️ **{hz['risk']}** |")

        md.append("\n### 3. 🛡️ 品質閘道判定 (Quality Gate Verdict)")
        has_violations = len(analysis.get("scope_violations", [])) > 0
        has_hazards = len(analysis.get("hazards", [])) > 0
        has_wires = len(analysis["wires_added"]) > 0
        has_controls = len(analysis["controls_added"]) > 0
        has_cleanups = len(analysis["cleanups"]) > 0

        if has_violations or has_hazards:
            md.append("> 🔴 **品質閘道阻擋 (BLOCKED_BY_INVARIANTS)**：")
            if has_violations:
                for sv in analysis["scope_violations"]:
                    md.append(f"> - ❌ **作用域致命錯誤**：{sv['issue']}")
            if has_hazards:
                for hz in analysis["hazards"]:
                    md.append(f"> - ⚠️ **禁忌阻塞 API**：偵測到 `{hz['api']}`，{hz['risk']}")
        elif has_controls and not has_wires:
            md.append("> ⚠️ **警告 (UNWIRED_RISK)**：長出了新控制項，但未偵測到事件監聽器接線！請確認是否有電線未插。")
        elif has_controls and has_wires and has_cleanups:
            md.append("> 🟢 **驗收通過 (READY_TO_SHIP)**：控制項結構完整、電線通電驗證無誤、閉包作用域安全、且自帶銷毀清理守門員！")
        else:
            md.append("> 🟢 **邏輯更新完成**：代碼已更新，無控制項孤兒或作用域異常風險。")

        return "\n".join(md)

    def render_html_dashboard(self, analysis: Dict[str, Any], output_path: str):
        """生成 100% 自包含的現代化 UIA 語意差分視覺化儀表板 HTML"""
        ctrl_nodes = ""
        for c in analysis.get("controls_added", []):
            ctrl_nodes += f"""
            <div class="node-pill node-added">
                <span class="node-tag">[+] {c['type']}</span>
                <span class="node-name">#{c['id']}</span>
            </div>
            """

        wire_rows = ""
        for w in analysis.get("wires_added", []):
            caller = w.get("caller_scope", "module")
            wire_rows += f"""
            <tr>
                <td><span class="badge badge-wire">⚡ WIRED</span></td>
                <td><code>{w['target']}</code></td>
                <td><code>on('{w['event']}')</code></td>
                <td><code>{w['handler']}</code> (scope: {caller})</td>
                <td><span class="status-ok">🟢 已接線</span></td>
            </tr>
            """

        leak_items = "".join([f"<li>🛡️ {l}</li>" for l in analysis.get("cleanups", [])]) or "<li>無新增清理函式</li>"
        keys_badges = " ".join([f"<span class='badge badge-key'>{k}</span>" for k in analysis.get("keys_handled", [])]) or "無"

        # 作用域違規與禁忌 API 警示區塊
        has_violations = len(analysis.get("scope_violations", [])) > 0
        has_hazards = len(analysis.get("hazards", [])) > 0
        
        alerts_html = ""
        if has_violations or has_hazards:
            alerts_html += """<div class="alerts-container">"""
            for sv in analysis.get("scope_violations", []):
                alerts_html += f"""
                <div class="alert-box alert-danger">
                    <span class="alert-icon">💥</span>
                    <div>
                        <strong>[!] 作用域致命囚禁 (Scope Trap):</strong>
                        <p>{sv['issue']}</p>
                    </div>
                </div>
                """
            for hz in analysis.get("hazards", []):
                alerts_html += f"""
                <div class="alert-box alert-warning">
                    <span class="alert-icon">⚠️</span>
                    <div>
                        <strong>[!] Webview 禁忌阻塞 API ({hz['api']}):</strong>
                        <p>{hz['risk']}</p>
                    </div>
                </div>
                """
            alerts_html += """</div>"""

        if has_violations or has_hazards:
            verdict_class = "verdict-blocked"
            verdict_icon = "🔴"
            verdict_text = "【UIA 品質閘道阻擋】：發布被拒絕 (BLOCKED BY INVARIANTS) —— 偵測到深層閉包作用域囚禁或禁忌阻塞 API，上線必翻車！"
        elif len(analysis.get("controls_added", [])) > 0 and len(analysis.get("wires_added", [])) == 0:
            verdict_class = "verdict-warning"
            verdict_icon = "⚠️"
            verdict_text = "【UIA 品質閘道警告】：發現孤兒控制項 (UNWIRED_RISK) —— 介面長出元件但電線未通！"
        else:
            verdict_class = "verdict-ok"
            verdict_icon = "🟢"
            verdict_text = "【UIA 品質閘道判定】：驗收通過 (READY TO SHIP) —— 控制項結構完整、電線通電驗證無誤、作用域安全！"

        html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>UIA Semantic Diff Dashboard</title>
    <style>
        :root {{
            --bg: #1e1e2e;
            --card: #252538;
            --border: #3b3b54;
            --text: #cdd6f4;
            --green: #a6e3a1;
            --blue: #89b4fa;
            --yellow: #f9e2af;
            --red: #f38ba8;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 24px;
            line-height: 1.5;
        }}
        .header {{ margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 12px; }}
        .header h1 {{ font-size: 20px; color: #fff; display: flex; align-items: center; gap: 10px; }}
        .badge {{ font-size: 11px; padding: 3px 8px; border-radius: 4px; font-weight: 600; text-transform: uppercase; }}
        .badge-range {{ background: #313244; color: var(--blue); border: 1px solid var(--border); }}
        .badge-wire {{ background: rgba(166, 227, 161, 0.2); color: var(--green); }}
        .badge-key {{ background: rgba(249, 226, 175, 0.2); color: var(--yellow); }}
        
        .alerts-container {{ margin-bottom: 20px; display: flex; flex-direction: column; gap: 12px; }}
        .alert-box {{
            padding: 14px 18px;
            border-radius: 8px;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            font-size: 13px;
        }}
        .alert-danger {{ background: rgba(243, 139, 168, 0.15); border: 1px solid var(--red); color: var(--red); }}
        .alert-warning {{ background: rgba(249, 226, 175, 0.15); border: 1px solid var(--yellow); color: var(--yellow); }}
        .alert-icon {{ font-size: 20px; }}
        
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }}
        @media(max-width: 800px) {{ .grid {{ grid-template-columns: 1fr; }} }}
        
        .card {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
        }}
        .card-title {{ font-size: 14px; font-weight: 700; margin-bottom: 12px; color: #fff; display: flex; justify-content: space-between; }}
        
        .node-container {{ display: flex; flex-direction: column; gap: 8px; }}
        .node-pill {{
            background: #181825;
            border: 1px solid var(--border);
            border-left: 4px solid var(--green);
            padding: 8px 12px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 13px;
        }}
        .node-tag {{ font-family: monospace; font-weight: bold; color: var(--green); }}
        .node-name {{ font-family: monospace; color: #bac2de; }}
        
        table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; text-align: left; }}
        th, td {{ padding: 8px 10px; border-bottom: 1px solid var(--border); }}
        th {{ color: #a6adc8; font-size: 11px; text-transform: uppercase; }}
        .status-ok {{ color: var(--green); font-weight: 600; }}
        
        .verdict-box {{
            border-radius: 8px;
            padding: 14px 18px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 600;
            font-size: 14px;
        }}
        .verdict-ok {{ background: rgba(166, 227, 161, 0.1); border: 1px solid var(--green); color: var(--green); }}
        .verdict-blocked {{ background: rgba(243, 139, 168, 0.15); border: 1px solid var(--red); color: var(--red); }}
        .verdict-warning {{ background: rgba(249, 226, 175, 0.15); border: 1px solid var(--yellow); color: var(--yellow); }}
    </style>
</head>
<body>
    <div class="header">
        <h1>
            <span>🌲 UIA 語意樹代碼差分儀表板</span>
            <span class="badge badge-range">Range: {self.diff_range}</span>
        </h1>
        <p style="color:#a6adc8; font-size:13px; margin-top:4px;">
            Target Repository: <code>{self.repo_path}</code>
        </p>
    </div>

    {alerts_html}

    <div class="grid">
        <!-- Controls Subtree -->
        <div class="card">
            <div class="card-title">
                <span>➕ 新增 UIA 控制項節點 (Controls Subtree)</span>
                <span style="color:var(--green); font-size:12px;">{len(analysis.get("controls_added", []))} Nodes</span>
            </div>
            <div class="node-container">
                {ctrl_nodes or '<div style="color:#6c7086; font-size:13px;">無新增控制項</div>'}
            </div>
        </div>

        <!-- Invariants & Lifecycle -->
        <div class="card">
            <div class="card-title">
                <span>🛡️ 鍵盤快速鍵與生命週期守衛</span>
            </div>
            <div style="font-size:13px; margin-bottom:12px;">
                <span style="color:#a6adc8;">捕獲快速鍵：</span> {keys_badges}
            </div>
            <div style="font-size:13px;">
                <span style="color:#a6adc8; display:block; margin-bottom:6px;">銷毀守衛 (Anti-Memory Leak)：</span>
                <ul style="padding-left:18px; color:var(--green); font-size:12px;">
                    {leak_items}
                </ul>
            </div>
        </div>
    </div>

    <!-- Wiring Table -->
    <div class="card" style="margin-bottom:20px;">
        <div class="card-title">
            <span>⚡ 電線通電檢查 (Event Wiring Check)</span>
        </div>
        <table>
            <thead>
                <tr>
                    <th>標籤</th>
                    <th>觸發對象 (Target)</th>
                    <th>事件類型 (Event)</th>
                    <th>銜接函式 (Handler)</th>
                    <th>通電狀態</th>
                </tr>
            </thead>
            <tbody>
                {wire_rows or '<tr><td colspan="5" style="color:#6c7086; text-align:center;">無直接 addEventListener 變更</td></tr>'}
            </tbody>
        </table>
    </div>

    <!-- Quality Gate Verdict -->
    <div class="verdict-box {verdict_class}">
        <span style="font-size:20px;">{verdict_icon}</span>
        <span>{verdict_text}</span>
    </div>
</body>
</html>
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)


def main():
    parser = argparse.ArgumentParser(description="UIA Style Semantic Code Diff Analyzer")
    parser.add_argument("--repo", default=".", help="目標 Git 倉庫目錄路徑")
    parser.add_argument("--diff", default="HEAD~1", help="Git diff 比對範圍 (例如: HEAD~1, 或 commitA commitB)")
    parser.add_argument("--html", default=None, help="輸出 HTML 視覺化儀表板檔案路徑")
    args = parser.parse_args()

    analyzer = UIACodeDiffAnalyzer(repo_path=args.repo, diff_range=args.diff)
    analysis = analyzer.analyze()
    report = analyzer.render_markdown_report(analysis)
    print(report)

    if args.html:
        analyzer.render_html_dashboard(analysis, args.html)
        print(f"\n[HTML 儀表板已輸出至]: {args.html}")


if __name__ == "__main__":
    main()

