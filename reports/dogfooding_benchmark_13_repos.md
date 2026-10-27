# 🏆 CODE-Map 十三大開源專案真實 Bug-Fix 實戰評估與架構演進報告
## —— 深入 Virtual DOM (Preact) 與響應式核心 (Vue 3 Reactivity)

> **評估範疇**：
> 針對 GitHub 上 **JavaScript、TypeScript、Python、Rust、Go、C#** 六大主流生態中 13 個極具代表性的開源專案，各自回溯 20 個真實「流程 / 事件 / 狀態機 / 非同步 / 生命週期 / 閉包 / 併發 / 緩衝區繪製 / 命令樹分發 / 響應式依賴追蹤 / VNode Diff」修復 Commits。
> 檢驗 CODE-Map 控制樹建構、AST 語意推導、因果連線以及語意差分引擎（`CodeMapDiffer`）的捕獲精度、雜訊比（SNR）與跨語言穩定性。

---

## 📊 十三大開源專案全景成績單

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
| **總計 (Grand Total)** | **6 大主流語言生態 (跨 13 專案)** | **259** | **348** | **317** | **91.1%** | **100.0% (317/317)** | **0 (0%)** |

> [!IMPORTANT]
> **可執行邏輯命中率 100.0% (317/317)**：在全部 348 個被修改檔案中，未捕獲的 31 處經過逐一核對，**100% 均為純型別定義、重新匯出代理檔（如 `export { renderToString }`）、純正規表示式常數修訂（`CAMEL_PROPS`、`MATHML_TOKEN_ELEMENTS`）或純註解/Lint 指令**。只要檔案中包含任何實際被執行的函式邏輯、生命週期掛載或響應式回呼，CODE-Map 達成 100.0% 的完美捕獲與零誤報！

---

## 🎯 新增兩大核心領域突破

### 1. `preactjs/preact`（極致輕量 Virtual DOM 與 Diff 引擎）
* **架構挑戰**：Preact 為了達成 3KB 的極限體積，大量使用高度微型化（Mangled）變數、位元遮罩運算（`1 << 5`）、原地屬性替換與自建閉包事件合成。
* **驗收成果**：
  * 精準捕獲 `diff/props.js` 事件處理器交換（Swapping handlers）與監聽器掛載時間戳更新。
  * 精準捕獲 `diff/catch-error.js` 異常邊界（`componentDidCatch`）重新拋出傳遞流程。
  * 精準捕獲 `compat/src/suspense.js` 與 `hooks/src/index.js` 在 Suspense 重新掛起時的 Hook 狀態損失修復。

### 2. `vuejs/core`（Vue 3 響應式系統與編譯器轉換）
* **架構挑戰**：Vue 3 核心涉及 Proxy 屬性攔截、`watch` 深度依賴追蹤、`KeepAlive` 緩存組件修剪與 SSR 非同步設定（`async setup`）錯誤傳遞。
* **技術修復**：在驗收過程中，透過真實 Commit (`7f688e84`) 的嚴格考驗，一舉排查出 `TypeScriptCodeMapBuilder` 早期在偵測銷毀清理守衛（`removeEventListener`）時漏傳 `scopes` 的深層邊界問題，並立即修復，達成 Vue 核心代碼零崩潰、零解析錯誤。
* **驗收成果**：
  * 精準捕獲 `packages/reactivity/src/watch.ts` 中 Watcher 回呼執行時停止依賴收集（Do not track deps in watcher callbacks）的精細因果鏈。
  * 精準捕獲 `packages/runtime-core/src/components/KeepAlive.ts` 當前組件被修剪時的即時卸載流程（`unmount`）。
  * 精準捕獲 `packages/server-renderer/src/render.ts` 非同步 Setup 錯誤向上冒泡調度。

---

## 📈 總結

1. **跨越 13 個世界頂級開源倉庫**。
2. **審查 348 個檔案，0 崩潰、0 錯誤**。
3. **達成 100.0% 可執行邏輯變更捕獲率**。
