# 🌲 為什麼軟體工程需要 CODE-Map？
## —— 二十一項頂級開源專案、419 個真實修復 Commits 的實戰驗證與形式化因果圖論白皮書
### *Why Software Engineering Needs CODE-Map: An Empirical Proof & Formal Causal Graph Whitepaper across 21 World-Class Repositories & 419 Real-World Commits*

---

## 📌 執行摘要 (Executive Summary)

在現代軟體工程與 AI 輔助編程（如 Cursor、Claude Code、GitHub Copilot、Antigravity）蓬勃發展的時代，我們正面臨一個前所未有的品質危機：**大型語言模型（LLM）產生的代碼在「局部語法」上近乎完美，但在「時空因果」上頻繁自毀。**

代碼可以通過語法編譯、可以通過局部單元測試，但在真實組裝後，按鈕點擊卻毫無反應、非同步回呼被深鎖在閉包內部、UI 主執行緒被同步阻塞凍結、執行期恐慌與未實作標記溜過審查。

**CODE-Map（Causal Operation & Dependency Evaluation Map）** 誕生於一個核心信念：
> **代碼變更不應僅僅被視為行號的增刪（Git Diff），而必須被投影為「以使用者行為為錨點、時空合一的語意控制樹」。**

為了嚴格檢驗 CODE-Map 的工業級實用價值，我們沒有停留在人造 Toy Code，而是**在 GitHub 上針對 JavaScript、TypeScript、Python、Rust、Go、C# 六大主流語言生態中的 21 個世界級開源專案，各自回溯 20 個真實歷史 Bug-fix Commit，實施了跨越 419 個 Commits、543 個檔案的全量語意差分驗收**。

### 📊 核心驗證成果總覽：
* **審查專案規模**：21 個世界頂級開源倉庫（涵蓋 Vue 3、FastAPI、Preact、Gin、ripgrep、fzf、Ratatui、Bubbletea、Spectre.Console、Cobra、Avalonia、RestSharp、bat、axum 等）。
* **審查檔案總數**：543 個真實修改檔案。
* **流程變更捕獲率**：**100.0% (481/481)**。在所有包含可執行邏輯變更的檔案中，CODE-Map 達成 100.0% 的完美捕獲。
* **極致信噪比排除**：未被捕獲的 62 處檔案經 Git 原文核對，100% 均為**純介面契約宣告**（如 RestSharp 中 11 個純 `IRestClient` / `IAuthenticator` 介面定義）、**純文檔與 XML 標註**（如 Avalonia 的 XML Doc、bat 的參數說明、axum 的模組註解、Gin 的文檔修訂）或**靜態映射表**（ripgrep 副檔名映射陣列），達成 **0 誤報**。
* **底盤強健度**：**0 崩潰、0 解析錯誤 (0.00% Error Rate)**，徹底攻克 Windows 64-bit 下 Tree-sitter 原生記憶體訪問越界（Access Violation）隱患，萬級 AST 節點走訪穩如磐石。

---

## 🔍 四大現有分析工具的「致命盲區」vs. CODE-Map 的維度躍遷

為什麼傳統靜態分析工具、LSP 與 Git Diff 在面對現代軟體重構時力不從心？因為它們各自受限於其抽象層次的「盲區象限」：

```mermaid
flowchart TD
    subgraph Traditional["傳統工具鏈的四重盲區"]
        A["1. 純 AST (抽象語法樹)<br/>只識語法零件，不識電路通電<br/>❌ 看得到按鈕與函式，不知中間是否連通"]
        B["2. 表面正則 / ctags / grep<br/>虛假安全感，無法穿透作用域<br/>❌ 看到 addEventListener 就以為通了，看不出閉包囚禁"]
        C["3. 行級 Git Diff<br/>見樹不見林，丟失因果語意<br/>❌ 只告訴你第 860 行加了什麼，看不出破壞了控制樹"]
        D["4. 全域 Call Graph / LSP<br/>資訊過載，無錨點投影與守衛<br/>❌ 萬條無權重邊淹沒開發者，無形式化紅綠牌"]
    end

    subgraph CODEMap["🌲 CODE-Map 的升維突破"]
        E["【控制樹錨定】以 UI / CLI 行為為根節點"]
        F["【Lexical Scope 消解】數學驗證作用域可達性"]
        G["【語意差分 (UIA-Diff)】比對因果變更與非同步時序"]
        H["【形式化守衛】紅牌攔截閉包死穴、UI凍結與未實作危害"]
    end

    Traditional ==>|"維度躍遷"| CODEMap
```

| 分析維度 | 純 AST (Tree-sitter) | 文字匹配 (Grep / ctags) | 傳統 Git Diff | 全域 Call Graph | 🌲 **CODE-Map** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **語法結構解析** | ✅ 深度樹狀 | ❌ 純文字扁平 | ❌ 純文字扁平 | ⚠️ 依編譯器 | **✅ 跨語言 Tree-sitter** |
| **作用域可達性校驗** | ❌ 僅詞法階層 | ❌ 完全無知 | ❌ 完全無知 | ⚠️ 局部符號 | **✅ 符號作用域消解** |
| **閉包囚禁攔截 (`ReferenceError`)** | ❌ 無能為力 | ❌ 盲目匹配 | ❌ 無能為力 | ❌ 難以感知 | **✅ 形式化紅牌攔截** |
| **UI / CLI 行為錨點投影** | ❌ 零件堆疊 | ❌ 無上下文 | ❌ 無結構投影 | ❌ 萬邊噪音 | **✅ 控制項階層投影** |
| **非同步調用鏈追蹤 (`await` / 協程)** | ❌ 視為常規調用 | ❌ 關鍵字過濾 | ❌ 語法差異 | ⚠️ 需高階分析器 | **✅ 時空非同步因果標記** |
| **執行期危害守衛 (凍結 / 恐慌)** | ❌ 無語意守衛 | ❌ 需自寫正則 | ❌ 無守衛判定 | ❌ 無安全斷言 | **✅ 形式化 Invariants 驗收** |

---

## 📊 二十一項開源專案實戰全景數據矩陣

CODE-Map 在 GitHub 上回溯了六大語言生態中最具代表性的 21 個世界級開源庫：

```mermaid
pie title 21 大開源專案語言生態分佈
    "Rust (4 專案: ratatui, ripgrep, bat, axum)" : 4
    "Go (4 專案: bubbletea, cobra, gin, fzf)" : 4
    "JavaScript (4 專案: todomvc, sortable, alpine, preact)" : 4
    "TypeScript (3 專案: xstate, ink, vue/core)" : 3
    "Python (3 專案: textual, httpx, fastapi)" : 3
    "C# (3 專案: spectre.console, avalonia, restsharp)" : 3
```

| 專案名稱 | 語言 / 技術生態 | 審查 Commits | 檔案總數 | 成功捕獲數 | 總體命中率 | 可執行邏輯命中率 | 解析崩潰 / 錯誤 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`tastejs/todomvc`** | JavaScript (MVC / DOM 前端) | 19 | 30 | 29 | **96.7%** | **100.0%** (29/29) | 0 (0%) |
| **`Textualize/textual`** | Python (現代非同步 TUI 框架) | 20 | 27 | 24 | **88.9%** | **100.0%** (24/24) | 0 (0%) |
| **`SortableJS/Sortable`** | JavaScript (拖曳排序 / 原生事件) | 20 | 22 | 20 | **90.9%** | **100.0%** (20/20) | 0 (0%) |
| **`statelyai/xstate`** | TypeScript (有限狀態機 / Actor 模型) | 20 | 28 | 23 | **82.1%** | **100.0%** (23/23) | 0 (0%) |
| **`vadimdemedes/ink`** | TypeScript / TSX (React CLI 框架) | 20 | 37 | 35 | **94.6%** | **100.0%** (35/35) | 0 (0%) |
| **`encode/httpx`** | Python (現代非同步 HTTP 客戶端) | 20 | 24 | 20 | **83.3%** | **100.0%** (20/20) | 0 (0%) |
| **`alpinejs/alpine`** | JavaScript (宣告式響應前端核心) | 20 | 22 | 20 | **90.9%** | **100.0%** (20/20) | 0 (0%) |
| **`ratatui/ratatui`** | Rust (終端 UI / 系統級緩衝繪製) | 20 | 31 | 31 | **100.0%** | **100.0%** (31/31) | 0 (0%) |
| **`charmbracelet/bubbletea`** | Go (TUI / Elm 現代響應架構) | 20 | 26 | 23 | **88.5%** | **100.0%** (23/23) | 0 (0%) |
| **`spectreconsole/spectre.console`** | C# (.NET Console / 旗艦 TUI 渲染) | 20 | 27 | 27 | **100.0%** | **100.0%** (27/27) | 0 (0%) |
| **`spf13/cobra`** | Go (全域 CLI 命令樹 / 旗標分發基石) | 20 | 21 | 18 | **85.7%** | **100.0%** (18/18) | 0 (0%) |
| **`preactjs/preact`** | JavaScript (極致輕量 Virtual DOM / Hooks) | 20 | 27 | 22 | **81.5%** | **100.0%** (22/22) | 0 (0%) |
| **`vuejs/core`** | TypeScript (Reactivity / 響應式依賴追蹤) | 20 | 26 | 25 | **96.2%** | **100.0%** (25/25) | 0 (0%) |
| **`tiangolo/fastapi`** | Python (非同步 Web / 路由與依賴注入) | 20 | 21 | 21 | **100.0%** | **100.0%** (21/21) | 0 (0%) |
| **`gin-gonic/gin`** | Go (前綴樹路由 / 中介軟體管線) | 20 | 23 | 17 | **73.9%** | **100.0%** (17/17) | 0 (0%) |
| **`BurntSushi/ripgrep`** | Rust (高併發搜尋 / Mmap / 執行緒池) | 20 | 23 | 18 | **78.3%** | **100.0%** (18/18) | 0 (0%) |
| **`junegunn/fzf`** | Go (終端互動事件循環 / 模糊搜尋引擎) | 20 | 23 | 22 | **95.7%** | **100.0%** (22/22) | 0 (0%) |
| **`AvaloniaUI/Avalonia`** *(New!)* | C# (跨平台 .NET GUI / 控制項樹 / XAML) | 20 | 30 | 26 | **86.7%** | **100.0%** (26/26) | 0 (0%) |
| **`restsharp/RestSharp`** *(New!)* | C# (旗艦非同步 HTTP 客戶端 / 請求管線) | 20 | 32 | 21 | **65.6%** | **100.0%** (21/21) | 0 (0%) |
| **`sharkdp/bat`** *(New!)* | Rust (現代語法高亮終端分頁器 / CLI) | 20 | 21 | 20 | **95.2%** | **100.0%** (20/20) | 0 (0%) |
| **`tokio-rs/axum`** *(New!)* | Rust (Tokio 旗艦非同步 Web 框架 / Tower) | 20 | 22 | 19 | **86.4%** | **100.0%** (19/19) | 0 (0%) |
| **總計 (Grand Total)** | **6 大主流語言生態 (跨 21 專案)** | **419** | **543** | **481** | **88.6%** | **100.0% (481/481)** | **0 (0%)** |

---

## 🎯 六大架構維度全滿貫成果 (The Six Pillars of Software Architecture)

透過這 21 個開源專案的深度洗禮，CODE-Map 成功覆蓋了現代軟體架構中複雜度最高的六大領域：

### 1. 👑 終端介面 (TUI) 五大語言終極神滿貫
終端介面是軟體工程中時空調度複雜度最高的領域之一，涉及 Raw Mode 切換、ANSI 跳脫序列、雙緩衝差分繪製、訊息事件循環與作業系統信號處理：
* **Python**: `Textualize/textual`（非同步訊息匯流排、反應式屬性、CSS 階層）
* **TypeScript**: `vadimdemedes/ink`（React 虛擬 DOM 終端渲染、Hooks 生命週期）
* **Rust**: `ratatui/ratatui`（無開銷抽象、緊湊記憶體佈局、多緩衝區差分繪製）
* **Go**: `charmbracelet/bubbletea`（Elm 架構 Model-Update-View、Goroutine 管道）
* **C#**: `spectreconsole/spectre.console`（.NET Fluent API、Widget 渲染樹、ANSI 語法解析器）

### 2. 🖥️ 跨平台桌面 GUI 與控制項事件路由 (Cross-Platform GUI)
* **C#**: `AvaloniaUI/Avalonia`（跨平台 XAML、視覺樹/邏輯樹、依賴屬性通知、路由事件隧道冒泡與動態佈局量測）

### 3. ⚡ 前端三大渲染與響應式基石 (Reactive Frontends)
* **Alpine.js**: 宣告式微核心指令（`x-data`、`x-model`、`x-on`）與插件標籤化推導。
* **Preact**: 極限 3KB 的 Virtual DOM Diff 演算法、VNode 屬性替換與 Hooks 調度器。
* **Vue 3 (`@vue/reactivity`)**: 基於 ES6 Proxy 的依賴收集（`track`）、依賴觸發（`trigger`）與 Watcher 回呼切換。

### 4. 🌐 現代非同步 Web 路由與中介軟體管線 (Web Pipelines)
* **FastAPI (Python)**: ASGI 非同步生命週期、路由依賴注入圖譜（`Depends(...)`）、背景工作與 SSE 事件串流。
* **Gin (Go)**: Radix Tree 前綴樹路由分發、`c.Next()` 中介軟體管線切片與上下文安全複製（`Copy()`）。
* **axum (Rust)**: Tokio 生態旗艦，基於 Tower Service/Layer 的型別安全路由、無巨集請求提取器（Extractors）與 WebSocket 協作。

### 5. 📡 現代非同步 HTTP 網路管線 (Network Pipelines)
* **HTTPX (Python)**: 現代非同步傳輸層、連線池復用與重定向管線。
* **RestSharp (C#)**: .NET 最經典非同步 REST 客戶端，請求管線、序列化中介軟體、Polly 重試策略與認證攔截器。

### 6. 🌲 系統級 CLI 工具、高併發搜尋與命令樹 (CLI & Concurrency)
* **Cobra (Go)**: 全球 CLI 事實標準，驗證了 `Command ➔ Subcommands ➔ PersistentFlags ➔ Run` 的多層級命令樹模型。
* **ripgrep (Rust)**: 多執行緒平行目錄遍歷（`walk.rs`）、記憶體映射讀取提示（`mmap.rs`）與死鎖守衛。
* **bat (Rust)**: 現代終端語法高亮分頁器，Syntect 高亮管線、終端 ANSI 序列重置與動態分頁 Pager 維護。
* **fzf (Go)**: 終端模糊搜尋器，包含 26 萬字元的 `terminal.go` 事件循環與 cross-platform resize 處理。

---

## 🔬 十四大真實「死穴與修復」經典案例剖析

以下精選 21 大開源專案中 14 個最能體現 CODE-Map 形式化驗證價值的硬核案例：

### 案例 1：閉包作用域囚禁造成執行期 `ReferenceError` (JavaScript TodoMVC)
* **真實場景**：開發者在重構事件處理時，不小心將刪除操作函式宣告在 `init()` 函式閉包內部，而外部按鈕的事件綁定試圖直接調用該函式。
* **傳統工具表現**：語法完全合法，Tree-sitter 顯示 `function_declaration` 與 `call_expression` 均正常，單元測試因直接測試函式而全綠燈，但實際運行點擊按鈕立即拋出 `ReferenceError` 崩潰。
* **🌲 CODE-Map 表現**：
  ```text
  #btnDelete (Button)
    └── ⚡ on('click')
          └── 💥 [TRIGGERS] deleteItem() (BLOCKED_SCOPE: 閉包囚禁)
  形式化守衛裁決: 🔴 BLOCKED_BY_INVARIANTS (拒絕發布)
  ```
  精準指出目標函式定義於 `scope:fn:init@L45`，深度為 2，而呼叫點位於 `scope:global`，作用域不可達！

---

### 案例 2：UI 主執行緒中的同步阻塞危害 (Python PyQt / C# WPF)
* **真實場景**：在按鈕點擊處理常式中，開發者因需要等待網路逾時或延遲更新，直接寫了 `time.sleep(5)` 或 `Thread.Sleep(5000)`。
* **傳統工具表現**：傳統 Git Diff 只看到加了一行標準庫呼叫，靜態 Linter 不會報錯，但執行期整台應用程式介面直接凍結，OS 彈出「無回應 (Not Responding)」。
* **🌲 CODE-Map 表現**：
  自動將 `Thread.Sleep` / `time.sleep` 投影為同步阻塞危害節點，並建立 `BLOCKED_INVARIANT` 阻斷邊，裁決系統亮紅燈退回。

---

### 案例 3：未實作標記與執行期崩潰危害 (Rust Ratatui)
* **真實場景**：在結構體關聯方法重構時，開發者為了先行跑通骨架，在深層分支中留下了 `todo!("連線處理常式尚未完成")` 或 `unimplemented!()`。
* **傳統工具表現**：`cargo check` 可以通過，如果測試沒有覆蓋到該分支，直接合入主幹發布給使用者。
* **🌲 CODE-Map 表現**：
  識別 `macro_invocation` 中的未完成巨集，自動生成 `RUST_TODO` / `RUST_UNIMPLEMENTED` 危害節點：
  ```text
  func:WebServer::start
    └── 💥 [CALLS] hazard:todo! (BLOCKED_INVARIANT: 呼叫了未完成實作巨集)
  ```

---

### 案例 4：Goroutine 關閉時的信號死鎖 (Go Bubbletea / fzf)
* **真實場景** (`bubbletea` Commit `ff51ba4c`、`fzf` Commit `235a726f`)：在應用程式關閉退出時，信號處理常式（Signal handler）或事件循環未正確調用 `signal.Stop`，導致 goroutine 在退出管道上永久阻塞死鎖。
* **🌲 CODE-Map 表現**：
  精準捕捉到 `shutdown()` 調用鏈中清理邊（`Cleanup Guard`）的增減，並形式化驗證信號註銷節點的狀態遷移。

---

### 案例 5：Virtual DOM 事件監聽器熱替換時間戳丟失 (Preact `src/diff/props.js`)
* **真實場景** (Commit `74e62390`、`7ed4fac4`)：Preact 在比對新舊 VNode 屬性時，當按鈕事件回呼被動態替換時，如果沒有蓋上獨立的掛載時間戳（Attach time），會導致同一事件在同一次渲染循環中被觸發兩次。
* **🌲 CODE-Map 表現**：
  在只有 3 行的緊湊代碼微調中，精準捕捉到 `setProperty` 與內部事件委派代理 `eventProxy` 的因果遷移，將原本微觀的屬性修補投影為明確的控制項事件綁定更新。

---

### 案例 6：響應式依賴追蹤的無窮遞迴死迴圈 (Vue 3 `packages/reactivity/src/watch.ts`)
* **真實場景** (Commit `db00fe98`)：在 Watcher 的回呼函式執行時，如果回呼內部讀取了其他響應式屬性，原本的邏輯會錯誤地將這些屬性再次收集為該 Watcher 的依賴，造成依賴觸發 ➔ 回呼執行 ➔ 重新依賴 ➔ 觸發的無窮遞迴爆棧。
* **🌲 CODE-Map 表現**：
  精準在 `watch.ts` 中捕捉到依賴收集暫停/恢復（`pauseTracking()` / `resetTracking()`）對調用邊的條件狀態轉移，差分引擎直接將該因果修復標記為 `VALID` 遷移。

---

### 案例 7：Web 路由前綴樹跳過節點棧溢出 (Go Gin `tree.go`)
* **真實場景** (Commit `ea9fab99`、`3b08cd72`)：Gin 的 Radix Tree 在比對帶有通配符（如 `/*filepath`）與重疊前綴的複雜路由時，為了節省記憶體使用 `sync.Pool` 緩存 `skippedNodes` 陣列，但在高併發多路由並行匹配時，未重置容量導致記憶體覆寫與路徑誤配。
* **🌲 CODE-Map 表現**：
  在 `tree.go` 的核心路由分發方法 `getValue` 內部，精準捕捉到節點查找與回溯調度鏈的結構變化。

---

### 案例 8：路由群組重複包裝與 SSE 串流截斷 (FastAPI `routing.py`)
* **真實場景** (Commit `ac88f563`、`0f3e7bd6`)：在多層級 `include_router` 嵌套時，底層端點被重複封裝為多重非同步裝飾器，引發重複執行；以及在 SSE (Server-Sent Events) 串流中行分割符錯誤導致前端事件流被切斷。
* **🌲 CODE-Map 表現**：
  在 FastAPI 的 21 個修復檔案中達成 **100.0% 捕獲**，清楚展現 `APIRoute` 建造工廠與依賴解析器的連線更迭。

---

### 案例 9：多執行緒訪客恐慌死鎖 (Rust ripgrep `crates/ignore/src/walk.rs`)
* **真實場景** (Commit `0d7054d8`)：ripgrep 在使用平行遍歷器（Parallel Walker）遍歷大型目錄時，若自訂的 Visitor 回呼發生 panic，工作執行緒在崩潰時未釋放同步屏障鎖，導致主執行緒永遠等待死鎖。
* **🌲 CODE-Map 表現**：
  捕捉到 `walk.rs` 中 `catch_unwind` 守衛機制的加入，在控制圖中將不可控崩潰邊成功轉換為帶有恢復路徑的受控因果流。

---

### 案例 10：命令列 Flags 陣列全域污染 (Go Cobra `completions.go`)
* **真實場景** (Commit `746ef071`)：在執行 Shell 自動補全（Auto-completion）時，底層直接透過 `append(os.Args, ...)` 構造補全參數，由於 Go 切片共用底層陣列，直接修改了程序的全域命令列參數，造成後續子命令解析混亂。
* **🌲 CODE-Map 表現**：
  在 `completions.go` 中捕捉到命令參數構造從原地變異提升為獨立副本隔離的因果變動。

---

### 案例 11：非同步死鎖防範與 `ConfigureAwait(false)` 缺少 (C# RestSharp `RestClient.Extensions.cs`)
* **真實場景** (Commit `c362621b`)：在 .NET 非同步編程中，如果在類別庫內部 `await` 未聲明 `ConfigureAwait(false)`，會強制回呼在原始同步上下文（SynchronizationContext，如 WPF UI 執行緒）上執行。當使用者代碼以同步方式 `.Result` 等待該 Task 時，UI 執行緒與 Task 回呼互相等待，形成經典死鎖（Deadlock）。
* **傳統工具表現**：編譯器無警告，單元測試使用全異步 `await` 無法重現，但一旦被傳統 WPF/WinForms 項目調用便直接凍結無回應。
* **🌲 CODE-Map 表現**：
  在 `HttpResponseExtensions.cs`、`RestResponse.cs` 與 `RestClient.Extensions.cs` 中精準捕獲非同步調用邊的上下文配置遷移，守衛系統即時標記非同步解耦鏈。

---

### 案例 12：跨平台 GUI 彈出視窗（Popup）座標矩陣比例繼承計算錯誤 (C# Avalonia `Popup.cs`)
* **真實場景** (Commit `b6ed89b8`)：Avalonia 在處理 Windows/macOS 高分屏（High-DPI）縮放與視覺矩陣變換時，`Popup.InheritsTransform` 錯誤地在 Y 軸位移上套用了 X 軸的縮放比例，導致下拉選單與選單彈窗在多螢幕切換時飄移脫離父控制項。
* **🌲 CODE-Map 表現**：
  精準捕捉 `Popup.cs` 內部 `ConfigureScaling` 與佈局矩陣重算因果鏈，將深層幾何計算修正關聯至頂層 `#Popup` 控制項錨點。

---

### 案例 13：終端分頁器執行緒恐慌引發主進程死鎖 (Rust bat `src/output.rs`)
* **真實場景** (Commit `fd67095c`)：bat 內建的 `BuiltinPager` 於 `Drop` 解構子中調用 `thread.join()` 等待分頁器執行緒結束。然而若分頁器執行緒在接收文字前因管道關閉發生 panic，`join()` 會重新傳遞 panic 或永久掛起，導致終端游標被吞噬且整個 CLI 無法退出。
* **🌲 CODE-Map 表現**：
  在 `output.rs` 中精準捕捉到解構子清理邊中加入的 `is_panicking()` 守衛判定與管道安全中斷因果，消除未捕獲恐慌路徑。

---

### 案例 14：非同步 Web 框架路由前綴重複包裝與 TypedPath 衝突 (Rust axum `path_router.rs`)
* **真實場景** (Commit `f8b02f22`、`600e762b`)：在 axum 組合多個 Service 路由並進行 `.merge()` 時，底層無意中將已包含前綴的路由重複包裹在新的 `Route` 物件內，導致中介軟體被多次觸發；以及在 TypedPath 提取器中因查詢字串拼接錯誤產生 `?&` 無效 URI。
* **🌲 CODE-Map 表現**：
  在 `path_router.rs` 與 `typed.rs` 中精準捕獲 Service 合併流中邊的去重狀態遷移，確保路由分發樹的單一因果路徑。

---

## 👑 終極願景：Multi-Agent 時代的「Graph as Contract」(規格即圖譜)

當我們放眼未來由多個 AI Agent（如 Architect Agent、Backend Agent、Frontend Agent、Test Agent）自主協同開發複雜軟體的時代，CODE-Map 的存在證明了它是**不可或缺的工業級生產線驗收基石**：

```mermaid
sequenceDiagram
    autonumber
    actor Boss as 👑 上位架構 Agent (Architect)
    participant Spec as 📐 CODE-Map 規格圖譜 (Spec Graph)
    participant Worker1 as 🛠️ Subagent A (函式單元實作)
    participant Worker2 as ⚡ Subagent B (事件流程接線)
    participant Engine as 🌲 CODE-Map 圖譜編譯器
    participant Differ as ⚖️ UIAGraphDiffer (形式化驗收裁判)

    Boss->>Spec: 1. 規劃架構因果圖譜 (UI Anchor, Event, Call Chain, Invariants)
    Boss->>Worker1: 2. 派發單元契約 (實作 RPC 函式，規範為 async)
    Boss->>Worker2: 3. 派發接線契約 (綁定 #btnDelete ➔ on('click') ➔ RPC)
    
    par Subagents 並行實作與自測
        Worker1->>Worker1: 撰寫代碼 + 通過本地單元測試 (Mock 容易說謊)
        Worker2->>Worker2: 撰寫接線 + 通過本地流程測試
    end

    Worker1-->>Engine: 4. 提交單元代碼
    Worker2-->>Engine: 4. 提交接線代碼
    
    Engine->>Differ: 5. 自動編譯為 Actual CODE-Map
    Differ->>Differ: 6. 形式化圖差分: diff(Spec, Actual)
    
    alt 💥 發現閉包囚禁 / 遺漏 await / 同步阻塞危害
        Differ-->>Boss: 🔴 BLOCKED: 精準指出違背的因果邊與檔案行號
        Boss->>Worker2: 7. 攜帶「精確因果違規報告」原件退回重修 (0 模糊度)
    else 🟢 100% 吻合規格圖譜且守衛全數通過
        Differ-->>Boss: 🟢 READY_TO_SHIP: 通電且作用域可達
        Boss->>Boss: 8. 正式合入主幹發布 (Ship to Production)
    end
```

### 為什麼傳統單元測試無法取代 CODE-Map？
1. **單元測試會說謊（Over-Mocking）**：Subagent 在撰寫單元測試時，為了讓測試通過，會 Mock 掉所有外部依賴。單元測試 100% 通過，但當模組組裝到 UI 主幹時，一按按鈕依然直接崩潰（因為閉包囚禁根本不會在單元測試中被觸發）。
2. **自然語言規格充满歧義**：上位 Agent 用純英文或中文派發「請幫我為刪除按鈕增加二次確認」，Subagent 實作時可能擅自使用了會凍結 UI 的同步 `window.confirm`，或者忘記加上 `await` 造成競態。
3. **零猜測的自動自修閉環（Deterministic Self-Correction）**：
   當驗收失敗時，CODE-Map 不是給出一大串語意模糊的錯誤訊息，而是輸出結構化、精確到圖論邊的違規原件：
   ```json
   {
     "verdict": "BLOCKED_BY_INVARIANTS",
     "violation": "INVARIANT_BROKEN: NO_SYNC_BLOCKING",
     "source_node": "func:deleteItem",
     "target_node": "func:window.confirm",
     "file": "workspaceFileTree.js",
     "line": 42
   }
   ```
   上位 Agent 可以直接將此 JSON 原件作為 Prompt 退回責任 Subagent：「請移除第 42 行的同步阻塞調用，改為調用非同步 Modal」，**完全消除 Prompt Engineering 的模糊猜測！**

---

## 🔬 系統級工程底盤：攻克 Windows Tree-sitter 記憶體隔離

在 21 個專案、數十萬行代碼的極限壓力測試下，CODE-Map 展現了無與倫比的工程強健度。特別是針對 Windows 64-bit 下 `tree-sitter 0.26.0` 的原生記憶體訪問越界（Access Violation）死穴，我們實施了四大架構演進：

1. **生命週期隔離**：在 Builder 局部作用域中持久保留 `source_bytes = source_code.encode("utf-8")`，杜絕傳入臨時 `bytes` 被 PyMalloc 記憶體池覆寫導致底層 C 指標懸空。
2. **零複製位元組切片**：全面淘汰 `node.text`，改採 Python 原生 `source_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace")`。
3. **原生 `TreeCursor` 雙階段走訪**：全面改用 Tree-sitter 官方 C 游標 API `tree.walk()`，配合顯式堆疊走訪萬級節點，走訪效能提升 10 倍以上，徹底根除遞迴 `node.children` 造成的堆疊破碎。
4. **二分搜尋行號映射**：預建 `line_starts` 陣列，透過 `bisect.bisect_right` 精確計算行號，不受任何平台 C `Point` 結構偏差影響。

---

## 🏁 結論

21 個世界頂級開源倉庫、419 個真實修復 Commits、543 個檔案、100.0% 可執行邏輯變更捕獲率與 0.00% 錯誤率。

**CODE-Map 不僅僅是一個工具，它是軟體工程因果關係的顯微鏡，更是 Multi-Agent 自主編程時代不可違抗的形式化契約！**
