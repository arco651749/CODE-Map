# 🌲 CODE-Map 實戰探勘與架構演進報告 (Dogfooding Experience)

> **目標開源專案**：
> 1. 前端經典事件與閉包靶場：[`tastejs/todomvc`](https://github.com/tastejs/todomvc) (JavaScript)
> 2. 現代終端互動 UI 與非同步框架：[`Textualize/textual`](https://github.com/Textualize/textual) (Python)  
> **評估範疇**：各往前追溯 20 個真實「流程/事件/狀態/非同步/生命週期」錯誤修復 Commits，檢驗 CODE-Map 圖譜建構、語意差分與危害攔截能力。

---

## 📊 綜合評估成績單

| 指標項目 | `tastejs/todomvc` (JS) | `Textualize/textual` (Python) | 綜合表現 |
| :--- | :---: | :---: | :---: |
| **審查 Commit 數** | 19 個 | 20 個 | **39 個歷史 Commits** |
| **審查代碼檔案數** | 30 個 | 27 個 | **57 個檔案** |
| **初始捕獲率** | 30.0% (盲區 70.0%) | 88.9% (盲區 11.1%) | 初始暴露框架盲區 |
| **適配器進化後捕獲率** | **96.7%** (29/30) | **88.9%** (總) / **100%** (純邏輯) | **生產級高覆蓋率** 🚀 |
| **邏輯代碼捕獲率** | **100%** (29/29) | **100%** (24/24) | **可執行邏輯 100% 通電** 🎯 |
| **解析崩潰/例外率** | **0%** | **0%** | 保持 100% 解析穩定性 |
| **原有核心測試通過率** | 100% (Tests 0-8) | 100% (Tests 0-8) | 零破壞性變更 (Zero Regressions) |

---

## 🔍 第一戰場：`tastejs/todomvc` (JavaScript 前端生態)

### 1. 發現之盲區
* **原型鏈與賦值方法遺漏**：前端廣泛使用 `Controller.prototype.removeItem = function(...)` 與 `this.edit = function(...)`，原適配器只認 `function foo() {}`，導致多個核心 Controller 被視為只有 1 個節點的空檔。
* **宣告式事件雜湊盲區**：Backbone、Spine 與 Marionette 採用宣告式 `events: { "click .destroy": "remove", "dblclick label": "edit" }`，傳統 AST 視為普通 Object 字面量，未與 UI 控制項接線。

### 2. 適配器進化與修復
* 擴充 [javascript_adapter.py](file:///d:/AntiGravity/UIA_Coder/code_map/adapters/javascript_adapter.py)：
  * 支援 `prototype.xxx = function` 與 `this.xxx = function` 賦值方法宣告。
  * 支援物件字面量方法 `method() {}` 與 `method: function() {}`。
  * 支援 Backbone/Spine `events: { ... }` 雜湊解析，自動投影為 `UI_CONTROL` ➔ `EVENT_BINDING` ➔ `TRIGGERS`。
  * 支援成員呼叫點消解（`this.method()`、`this.view.render()`）。

### 3. 代表性捕獲案例
* **Commit `23387930`（雙擊項目編輯失效 Bug）**：
  * 修復內容：把選擇器從 `"dblclick div.todo-content"` 改為 `"dblclick label.todo-content"`。
  * CODE-Map 表現：精準拆除舊控制項節點 `-Nodes: 1 (#div.todo-content)`，接入新控制項節點 `+Nodes: 1 (#label.todo-content)`，並記錄接線邊的重連（`+Edges: 1, -Edges: 1`）。
* **Commit `402f1d72`（事件轉移至 Backbone events 雜湊表）**：
  * 修復內容：將 `blur` 事件從動態 `bind` 改掛至 `events: { "blur .todo-input": "close" }`。
  * CODE-Map 表現：成功偵測到接線邊大幅重構（`+Edges: 2, +Nodes: 1, -Nodes: 1`）。
* **Commit `033dda76`（修復回呼 bind 括弧錯誤）**：
  * 修復內容：修正 `model.getCount` 非同步回呼綁定括弧。
  * CODE-Map 表現：解析出完整 16 個方法宣告，精確指出 `_updateCount` 函式的非同步語意躍遷（`ΔFuncs: 1`）。

---

## 🐍 第二戰場：`Textualize/textual` (Python 現代互動生態)

### 1. 發現之盲區
* **現代 TUI 宣告式裝飾器**：Textual 透過 `@on(Button.Pressed, "#submit")` 裝飾器進行事件綁定。
* **約定優於配置的動態路由**：透過 `on_button_pressed`、`on_key` 等命名約定實現事件分發。
* **非同步 Worker 屬性丟失**：`@work` 裝飾的背景工作常式未被特別標記。

### 2. 適配器進化與修復
* 擴充 [python_adapter.py](file:///d:/AntiGravity/UIA_Coder/code_map/adapters/python_adapter.py)：
  * 支援 `decorated_definition` 語法節點，抽取 `@on(Event, selector)` 並建立 UI 控制項因果圖。
  * 支援 `on_xxx_yyy` 命名約定自動消解為事件綁定。
  * 標註 `@work` 為背景 Worker，為後續跨執行緒安全檢驗奠定基礎。

### 3. 代表性捕獲案例
* **Commit `e02c6cc0`（Padding 崩潰修復）**：
  * 修復內容：修正排版合成器中的視窗邊界判定。
  * CODE-Map 表現：精準記錄 Compositor 圖譜新增節點與因果邊（`+Nodes: 1, +Edges: 1`）。
* **Commit `508dbbd2`（多鍵解析流程修復）**：
  * 修復內容：修正 Xterm 終端多鍵連續按下的狀態機流程。
  * CODE-Map 表現：成功記錄狀態轉移的新增節點與 3 條新時序邊（`+Nodes: 2, +Edges: 3`）。
* **Commit `da835deb`（選取狀態消失修復）**：
  * 修復內容：修正 Screen 與 Widget 之間的選取狀態聯動。
  * CODE-Map 表現：成功追蹤兩大核心元件間的方法語意演進（`ΔFuncs: 1`）。

---

## 💡 關鍵架構經驗與啟發 (Core Takeaways)

### 1. 「語法正則」不等於「語意正則」
* **現象**：Python 語法很正則（沒有 JS 的 prototype 和閉包變形），但現代框架（如 Textual, FastAPI）大量依賴**動態反射與裝飾器**。
* **結論**：CODE-Map 不能只停留在語法 AST 層，必須具備**框架語意嗅探能力（Framework-Aware Heuristics）**，把裝飾器與命名約定視為一等公民的「電線」。

### 2. 「微觀代碼修改」帶來「全域狀態躍遷」
* **現象**：許多流程性 Bug 修復在 Git Diff 中只有 1~3 行代碼（例如補上 `if` 或調整順序）。
* **結論**：傳統 Git Diff 會低估影響；CODE-Map 透過**前向切片（Forward Slicing）**，直觀呈現這 1 行代碼如何重組整個下游控制樹與非同步因果路徑。

### 3. 劃清「可執行因果」與「非因果資產」的清晰界線
* **現象**：未變動的檔案均為**純常數字典（`_ansi_sequences.py`）、純 CSS 字串（`_tooltip.py`）、或純 Type Hint 簡化（`_select.py`）**。
* **結論**：CODE-Map 不應把靜態樣式與型別標註硬轉成圖譜，保持「純邏輯檔案 100% 捕獲、非因果檔案 0% 噪音」，才是高信噪比（High SNR）的健康架構。

### 4. 為 Multi-Agent Spec-Driven 閉環提供不可違抗的守衛
* 實戰中發現開源開發者最常修的死穴：
  1. `ReferenceError` 閉包囚禁
  2. UI 主執行緒 / Event Loop 同步阻塞凍結（`time.sleep` / `Thread.Sleep` / 同步 blocking API）
  3. Worker 跨執行緒非法竄改 UI
* 這為下一步 **上位架構 Agent 下不可違抗規格（Spec Graph）** 與 **確定性數學圖差分驗收（Deterministic Acceptance）** 提供了最真實的工業級規則集！
