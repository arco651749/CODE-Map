import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path("D:/AntiGravity/UIA_Coder")
REPORTS_DIR = ROOT_DIR / "reports" / "per_repo_audits"
OUTPUT_FILE = ROOT_DIR / "reports" / "EXTERNAL_MODEL_REVIEW_PACK.md"

SAMPLES = [
    {
        "id": "03",
        "name": "Sortable",
        "file": "03_Sortable.md",
        "desc": "展示「0 結構拓樸變動、12 函式內部微調」之極端純條件式修復生態 (JavaScript)",
        "max_commits": 3
    },
    {
        "id": "08",
        "name": "ratatui",
        "file": "08_ratatui.md",
        "desc": "展示「97.1% 結構性呼叫電線增修、100% 捕獲」之細粒度模組化生態 (Rust)",
        "max_commits": 3
    },
    {
        "id": "12",
        "name": "preact",
        "file": "12_preact.md",
        "desc": "展示客觀標記 Barrel 轉發為 ZERO_DELTA，以及捕捉到閉包作用域阻隔死穴 BLOCKED_SCOPE (JavaScript)",
        "max_commits": 3
    },
    {
        "id": "14",
        "name": "fastapi",
        "file": "14_fastapi.md",
        "desc": "展示非同步路由與相依性注入架構下的 100% 捕獲證明 (Python)",
        "max_commits": 3
    },
    {
        "id": "29",
        "name": "vllm",
        "file": "29_vllm.md",
        "desc": "展示高併發 LLM 推理串流與 PagedAttention 記憶體生命週期修復證明 (Python)",
        "max_commits": 3
    },
    {
        "id": "33",
        "name": "caddy",
        "file": "33_caddy.md",
        "desc": "展示雲原生反向代理管線與錯誤守衛之程序式修復證明 (Go)",
        "max_commits": 3
    }
]

def extract_section(file_path: Path, max_commits: int = 3) -> str:
    if not file_path.exists():
        return f"> 檔案不存在: {file_path.name}\n"
    
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Split into commits
    parts = content.split("### 🔹 Commit #")
    header = parts[0]
    commit_sections = parts[1:] if len(parts) > 1 else []
    
    extracted = [header.strip()]
    extracted.append("\n---\n")
    extracted.append(f"### 📋 精選代表性修復 Commit 形式化證據 (抽樣前 {min(max_commits, len(commit_sections))} 項 / 共 {len(commit_sections)} 項)\n")
    
    for i, c in enumerate(commit_sections[:max_commits]):
        extracted.append(f"### 🔹 Commit #{c.strip()}")
        extracted.append("\n\n---\n")
        
    return "\n".join(extracted)

def main():
    # Read index
    index_path = REPORTS_DIR / "INDEX.md"
    index_content = ""
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            index_content = f.read()

    doc = []
    
    doc.append("""# 🔬 CODE-Map 全景審查獨立覆核封包 (External AI Model Review Pack)
> **致審查者**: 本文件是一份專為第三方 AI 模型（如 Claude 3.5 Sonnet, GPT-4o, DeepSeek-R1）設計的「單一自我包含 (Self-Contained)」形式化審查報告。
> **涵蓋範圍**: 35 個跨語言開源專案、693 個歷史真實修復 Commits、1,005 個變更檔案之 AST 語法樹分析、控制拓樸圖差分與前後代碼對照。

---

## 🤖 推薦給第三方 AI 模型的系統審查 Prompt

如果你是將此 Markdown 檔案上傳給其他 AI 模型進行審核，請直接將下方提示詞複製並作為開頭 Instructions：

```markdown
你現在是一位具備 15 年以上經驗的「資深靜態分析架構師與編譯器專家（Principal Static Analysis & Compiler Architect）」。
我正在評估一套名為「CODE-Map」的自動化程式碼語意因果圖與 AST 差分引擎。

這套引擎針對 35 個涵蓋不同語言生態（JavaScript, TypeScript, Python, Rust, Go, C#）的頂級開源專案，回溯了最近 20 個真實修復 Commits（總計 693 個 Commits、1,005 個變更檔案），並為每個專案建立了獨立的形式化審查報告。

請你基於本文件中提供的「審查總索引 (Grand Matrix Index)」以及「六大代表性專案抽樣審查證據 (Sortable, Ratatui, Preact, FastAPI, vLLM, Caddy)」，以極度理性、批判性且不討好的視角，對這套系統的審查結果進行全盤 Audit，並回答以下五個核心問題：

---

### 🔍 審查核心問題：

1. 【去水分雙軌指標審查】
   - CODE-Map 將變更嚴格切分為「結構性拓樸變動 (STRUCTURAL_GRAPH_DELTA)」、「函式體純文字變動 (BODY_LEVEL_SEMANTIC_DELTA)」與「無語意圖譜變動 (ZERO_DELTA)」。
   - 請檢查此分類標準是否客觀？是否有將純型別宣告（如 .d.ts）、註釋格式微調或純打包轉發（Barrel Re-exports）灌水為有效變更？

2. 【跨語言生態特徵真實性】
   - 報告指出：
     - Rust 生態（如 Ratatui, Zellij）有高達 90%~97% 的變更是「結構性圖譜變動」。
     - JavaScript 原生 DOM 生態（如 Sortable）有 92% 是「函式內部語意變動」，拓樸邊完全沒變。
     - Go 生態（如 Bubbletea, Gin, Caddy）呈現結構與內部變動各半。
   - 根據你對這些語言與真實開源維護習慣的理解，這樣的統計分佈是否符合現實？為什麼？

3. 【AST 提取與代碼差分精度】
   - 檢視抽樣報告中的真實案例（例如 Sortable 的 Shadow DOM 崩潰修復、Ratatui 的 BarChart 越界裁切修復、Preact 的 PureComponent 重構、FastAPI 的瀏覽器檔案輸入處理等）。
   - 其所提取的「Before / After 函式實作代碼」與「AST 呼叫邊 / 控制樹變化」，是否足以作為工程師或下游工具驗收的確定性證據？

4. 【形式化驗收與死穴阻隔 (Invariants)】
   - 報告中標註了如 Preact 專案中被深鎖在內部閉包未匯出的函式（BLOCKED_SCOPE / 作用域阻隔）。
   - 這種基於 AST 作用域阻隔與守衛狀態躍遷（Invariant Transitions）的判定邏輯，在防範死碼或不可達邏輯上有何實際價值？

5. 【盲點與極限挑戰 (Red Team / Critique)】
   - 直球指出這套基於 Tree-sitter AST 的因果控制流分析方案，可能存在哪些根本性盲點與死穴？（例如動態反射、頂層全域常數物件未進函式、宏展開 Macro Expansion 等）。
   - 你認為要進一步達到 100% 可驗證，下一步最該補強的關鍵技術是什麼？
```

---

## 📊 第一部分：全域 35 專案基準測試總評 (Global Benchmark Index)
""")

    # Append index content (without duplicating # header)
    clean_index = "\n".join(index_content.splitlines()[5:]) # skip top header
    doc.append(clean_index)
    
    doc.append("\n\n---\n\n## 🔬 第二部分：六大核心語言生態抽樣深度審查證據 (Sampled Repositories Evidence)\n")
    doc.append("> 以下挑選 6 個最能突顯跨語言生態差異、演算法極限與死穴攔截特徵的典型倉庫進行深度展示：\n\n")

    for idx, s in enumerate(SAMPLES, 1):
        doc.append(f"\n================================================================================\n")
        doc.append(f"### 📁 代表專案 #{idx}: `{s['name']}` ({s['id']})\n")
        doc.append(f"> **生態與抽樣意圖**: {s['desc']}  \n")
        doc.append(f"> **完整 20-Commit 報告位址**: `reports/per_repo_audits/{s['file']}`\n\n")
        
        extracted_content = extract_section(REPORTS_DIR / s['file'], max_commits=s['max_commits'])
        doc.append(extracted_content)
        doc.append("\n\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(doc))

    print(f"✅ 成功生成全自我包含 Review 封包: {OUTPUT_FILE}")
    print(f"   檔案大小: {OUTPUT_FILE.stat().st_size:,} bytes")

if __name__ == "__main__":
    main()
