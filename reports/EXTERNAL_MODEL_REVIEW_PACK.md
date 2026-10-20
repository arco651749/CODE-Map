# 🔬 CODE-Map 全景審查獨立覆核封包 (External AI Model Review Pack)
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

---

## 📊 三十五項專案去水分雙軌指標總表

| # | 專案名稱 | 語言 / 技術生態 | Commits | 檔案數 | 結構性變動 | 函式文字變動 | 命中率 | 報告連結 |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| 01 | **`todomvc`** | JavaScript (MVC / DOM 前端) | 20 | 35 | 22 | 11 | **94.3%** | [檢視報告](01_todomvc.md) |
| 02 | **`textual`** | Python (現代非同步 TUI 框架) | 20 | 32 | 20 | 7 | **84.4%** | [檢視報告](02_textual.md) |
| 03 | **`Sortable`** | JavaScript (拖曳排序 / 原生事件) | 13 | 13 | 0 | 12 | **92.3%** | [檢視報告](03_Sortable.md) |
| 04 | **`xstate`** | TypeScript (有限狀態機 / Actor 模型) | 20 | 30 | 14 | 9 | **76.7%** | [檢視報告](04_xstate.md) |
| 05 | **`ink`** | TypeScript (React CLI 框架) | 20 | 37 | 19 | 16 | **94.6%** | [檢視報告](05_ink.md) |
| 06 | **`httpx`** | Python (現代非同步 HTTP 客戶端) | 20 | 23 | 11 | 8 | **82.6%** | [檢視報告](06_httpx.md) |
| 07 | **`alpine`** | JavaScript (宣告式響應前端核心) | 20 | 22 | 9 | 12 | **95.5%** | [檢視報告](07_alpine.md) |
| 08 | **`ratatui`** | Rust (終端 UI / 系統級緩衝繪製) | 20 | 34 | 33 | 1 | **100.0%** | [檢視報告](08_ratatui.md) |
| 09 | **`bubbletea`** | Go (TUI / Elm 現代響應架構) | 20 | 24 | 11 | 8 | **79.2%** | [檢視報告](09_bubbletea.md) |
| 10 | **`spectre.console`** | C# (.NET Console / 旗艦 TUI 渲染) | 20 | 30 | 25 | 5 | **100.0%** | [檢視報告](10_spectre.console.md) |
| 11 | **`cobra`** | Go (全域 CLI 命令樹 / 旗標分發基石) | 20 | 24 | 10 | 10 | **83.3%** | [檢視報告](11_cobra.md) |
| 12 | **`preact`** | JavaScript (極致輕量 Virtual DOM / Hooks) | 20 | 30 | 6 | 22 | **93.3%** | [檢視報告](12_preact.md) |
| 13 | **`vue`** | TypeScript (Reactivity / 響應式依賴追蹤) | 20 | 29 | 14 | 15 | **100.0%** | [檢視報告](13_vue.md) |
| 14 | **`fastapi`** | Python (非同步 Web / 路由與依賴注入) | 20 | 24 | 15 | 5 | **83.3%** | [檢視報告](14_fastapi.md) |
| 15 | **`gin`** | Go (前綴樹路由 / 中介軟體管線) | 20 | 22 | 13 | 7 | **90.9%** | [檢視報告](15_gin.md) |
| 16 | **`ripgrep`** | Rust (高併發搜尋 / Mmap / 執行緒池) | 20 | 26 | 20 | 5 | **96.2%** | [檢視報告](16_ripgrep.md) |
| 17 | **`fzf`** | Go (終端互動事件循環 / 模糊搜尋引擎) | 20 | 32 | 16 | 14 | **93.8%** | [檢視報告](17_fzf.md) |
| 18 | **`Avalonia`** | C# (跨平台 GUI / 控制項樹 / XAML) | 20 | 33 | 22 | 6 | **84.8%** | [檢視報告](18_Avalonia.md) |
| 19 | **`RestSharp`** | C# (旗艦非同步 HTTP 客戶端 / 請求管線) | 20 | 33 | 21 | 3 | **72.7%** | [檢視報告](19_RestSharp.md) |
| 20 | **`bat`** | Rust (現代語法高亮終端分頁器 / CLI) | 20 | 25 | 20 | 4 | **96.0%** | [檢視報告](20_bat.md) |
| 21 | **`axum`** | Rust (Tokio 旗艦非同步 Web 框架 / Tower) | 20 | 27 | 17 | 3 | **74.1%** | [檢視報告](21_axum.md) |
| 22 | **`nest`** | TypeScript (企業級 IoC / 裝飾器管線) | 20 | 24 | 8 | 15 | **95.8%** | [檢視報告](22_nest.md) |
| 23 | **`zustand`** | TypeScript (全域狀態 / 閉包不可變性) | 20 | 24 | 6 | 13 | **79.2%** | [檢視報告](23_zustand.md) |
| 24 | **`go-redis`** | Go (高性能連線池 / Pipeline / 超時控制) | 20 | 29 | 15 | 10 | **86.2%** | [檢視報告](24_go-redis.md) |
| 25 | **`zellij`** | Rust (終端多工器 / Actor IPC / Pty) | 20 | 42 | 37 | 3 | **95.2%** | [檢視報告](25_zellij.md) |
| 26 | **`polars`** | Rust (DataFrame / Arrow / 平行 Rayon) | 20 | 33 | 27 | 3 | **90.9%** | [檢視報告](26_polars.md) |
| 27 | **`efcore`** | C# (企業級 ORM / 交易管線 / LINQ) | 20 | 25 | 21 | 4 | **100.0%** | [檢視報告](27_efcore.md) |
| 28 | **`pydantic`** | Python (資料驗證 / 核心模型裝飾器) | 20 | 23 | 8 | 11 | **82.6%** | [檢視報告](28_pydantic.md) |
| 29 | **`vllm`** | Python (LLM 推理串流 / PagedAttention) | 20 | 33 | 22 | 10 | **97.0%** | [檢視報告](29_vllm.md) |
| 30 | **`trpc`** | TypeScript (端到端型別 RPC / Proxy 路由) | 20 | 25 | 13 | 7 | **80.0%** | [檢視報告](30_trpc.md) |
| 31 | **`vite`** | TypeScript (現代前端打包管線 / HMR 廣播) | 20 | 25 | 8 | 17 | **100.0%** | [檢視報告](31_vite.md) |
| 32 | **`next.js`** | TypeScript (全端 SSR / Server Actions / RSC) | 20 | 39 | 15 | 15 | **76.9%** | [檢視報告](32_next.js.md) |
| 33 | **`caddy`** | Go (雲原生 Web 伺服器 / 自動 TLS / 重載) | 20 | 33 | 22 | 7 | **87.9%** | [檢視報告](33_caddy.md) |
| 34 | **`traefik`** | Go (邊緣路由器 / 動態中介軟體管線) | 20 | 30 | 19 | 7 | **86.7%** | [檢視報告](34_traefik.md) |
| 35 | **`bevy`** | Rust (ECS 遊戲引擎 / 資料導向排程器) | 20 | 35 | 26 | 3 | **82.9%** | [檢視報告](35_bevy.md) |
| -- | **總計 (Grand Total)** | **6 大主流語言生態 (35 專案)** | **693** | **1005** | **585** | **308** | **88.9%** | - |

---

### 🎯 統計亮點與科學客觀性說明:
1. **結構性因果圖變動 (Structural Graph Delta)**: 共 `585` 個檔案 (58.2%)，實質改變了 UI 控制項樹、事件綁定或非同步呼叫邊。
2. **函式體純文字變動 (Body-Level Semantic Delta)**: 共 `308` 個檔案 (30.6%)，控制流不變但函式內部邏輯更新，由 CODE-Map 函式級別 AST 差分精準捕獲。
3. **總體可執行邏輯變更捕獲率**: **`893` / `1005` (88.9%)**。
4. **AST 解析崩潰率**: **0% (0 / 920)**，Windows Tree-sitter 原生指針走訪全專案完全免疫崩潰。


---

## 🔬 第二部分：六大核心語言生態抽樣深度審查證據 (Sampled Repositories Evidence)

> 以下挑選 6 個最能突顯跨語言生態差異、演算法極限與死穴攔截特徵的典型倉庫進行深度展示：



================================================================================

### 📁 代表專案 #1: `Sortable` (03)

> **生態與抽樣意圖**: 展示「0 結構拓樸變動、12 函式內部微調」之極端純條件式修復生態 (JavaScript)  

> **完整 20-Commit 報告位址**: `reports/per_repo_audits/03_Sortable.md`


# 🔬 CODE-Map 基準審查獨立驗證報告: `Sortable`
> **技術生態**: `JavaScript (拖曳排序 / 原生事件)`  
> **本地倉庫路徑**: `test_repos/Sortable`  
> **審查 Commit 數**: 13 Commits  
> **審查原始碼檔案數**: 13 Files  
> **報告生成時間**: 2026-10-20 21:40:36  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `0` / `13` | `0.0%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `12` / `13` | `92.3%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `1` / `13` | `7.7%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`12` / `13`** | **`92.3%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `13` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

---

### 📋 精選代表性修復 Commit 形式化證據 (抽樣前 3 項 / 共 13 項)

### 🔹 Commit #01: `bd74abb2`
- **完整 Hash**: `bd74abb22ade431c0e1af0cd552796ec1e0bcb0c`
- **說明 (Ground Truth)**: fix: Sortable crashes browser when event is triggered from within ShadowDom element
- **變更檔案數**: 1

#### 📄 檔案: `src/utils.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:39, E:29, A:1) ➔ After(N:39, E:29, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#el** `(Control)`
    └── ⚡ **on('event')**
        └── 🎯 [TRIGGERS] `fn (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `getParentOrHost()`
- **變更前簽章 (Before)**: `function getParentOrHost(el)` (L40~L44)
- **變更後簽章 (After)**: `function getParentOrHost(el)` (L40~L44)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function getParentOrHost(el) {
	return (el.host && el !== document && el.host.nodeType)
		? el.host
		: el.parentNode;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function getParentOrHost(el) {
	return (el.host && el !== document && el.host.nodeType && el.host !== el)
		? el.host
		: el.parentNode;
}
```


---


---

### 🔹 Commit #02: `7d7d5d66`
- **完整 Hash**: `7d7d5d66c3220594379ec2027ab33c4053c8201a`
- **說明 (Ground Truth)**: restore old fallback selection clearing behaviour
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:106, E:127, A:3) ➔ After(N:106, E:127, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_triggerDragStart()`
- **變更前簽章 (Before)**: `_triggerDragStart(/** Event */evt, /** Touch */touch)` (L701~L728)
- **變更後簽章 (After)**: `_triggerDragStart(/** Event */evt, /** Touch */touch)` (L701~L728)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/** Event */evt, /** Touch */touch) {
		touch = touch || (evt.pointerType == 'touch' && evt);

		if (!this.nativeDraggable || touch) {
			if (this.options.supportPointer) {
				on(document, 'pointermove', this._onTouchMove);
			} else if (touch) {
				on(document, 'touchmove', this._onTouchMove);
			} else {
				on(document, 'mousemove', this._onTouchMove);
			}
		} else {
			on(dragEl, 'dragend', this);
			on(rootEl, 'dragstart', this._onDragStart);
		}

		try {
			
			if (document.selection) {
				_nextTick(() => {
					document.selection.empty();
				});
			} else if (this.nativeDraggable) {
				window.getSelection().removeAllRanges();
			}
		} catch (err) {
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/** Event */evt, /** Touch */touch) {
		touch = touch || (evt.pointerType == 'touch' && evt);

		if (!this.nativeDraggable || touch) {
			if (this.options.supportPointer) {
				on(document, 'pointermove', this._onTouchMove);
			} else if (touch) {
				on(document, 'touchmove', this._onTouchMove);
			} else {
				on(document, 'mousemove', this._onTouchMove);
			}
		} else {
			on(dragEl, 'dragend', this);
			on(rootEl, 'dragstart', this._onDragStart);
		}

		try {
			
			if (document.selection) {
				_nextTick(() => {
					document.selection.empty();
				});
			} else {
				window.getSelection().removeAllRanges();
			}
		} catch (err) {
		}
	}
```


---


---

### 🔹 Commit #03: `a81251f4`
- **完整 Hash**: `a81251f406f3bfc629bdb91f596b15066b688773`
- **說明 (Ground Truth)**: #2410: Further improve selection handling on drag start
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:106, E:127, A:3) ➔ After(N:106, E:127, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_onDragStart()`
- **變更前簽章 (Before)**: `_onDragStart(/**Event*/evt, /**boolean*/fallback)` (L930~L1005)
- **變更後簽章 (After)**: `_onDragStart(/**Event*/evt, /**boolean*/fallback)` (L928~L1005)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/**Event*/evt, /**boolean*/fallback) {
		let _this = this;
		let dataTransfer = evt.dataTransfer;
		let options = _this.options;

		pluginEvent('dragStart', this, { evt });
		if (Sortable.eventCanceled) {
			this._onDrop();
			return;
		}

		pluginEvent('setupClone', this);
		if (!Sortable.eventCanceled) {
			cloneEl = clone(dragEl);
			cloneEl.removeAttribute("id");
			cloneEl.draggable = false;
			cloneEl.style['will-change'] = '';

			this._hideClone();

			toggleClass(cloneEl, this.options.chosenClass, false);
			Sortable.clone = cloneEl;
		}


		// #1143: IFrame support workaround
		_this.cloneId = _nextTick(function() {
			pluginEvent('clone', _this);
			if (Sortable.eventCanceled) return;

			if (!_this.options.removeCloneOnHide) {
				rootEl.insertBefore(cloneEl, dragEl);
			}
			_this._hideClone();

			_dispatchEvent({
				sortable: _this,
				name: 'clone'
			});
		});


		!fallback && toggleClass(dragEl, options.dragClass, true);

		// Set proper drop events
		if (fallback) {
			ignoreNextClick = true;
			_this._loopId = setInterval(_this._emulateDragOver, 50);
		} else {
			// Undo what was set in _prepareDragStart before drag started
			off(document, 'mouseup', _this._onDrop);
			off(document, 'touchend', _this._onDrop);
			off(document, 'touchcancel', _this._onDrop);

			if (dataTransfer) {
				dataTransfer.effectAllowed = 'move';
				options.setData && options.setData.call(_this, dataTransfer, dragEl);
			}

			on(document, 'drop', _this);

			// #1276 fix:
			css(dragEl, 'transform', 'translateZ(0)');
		}

		awaitingDragStarted = true;

		_this._dragStartId = _nextTick(_this._dragStarted.bind(_this, fallback, evt));
		on(document, 'selectstart', _this);

		moved = true;

		if (Safari) {
			css(document.body, 'user-select', 'none');
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/**Event*/evt, /**boolean*/fallback) {
		let _this = this;
		let dataTransfer = evt.dataTransfer;
		let options = _this.options;

		pluginEvent('dragStart', this, { evt });
		if (Sortable.eventCanceled) {
			this._onDrop();
			return;
		}

		pluginEvent('setupClone', this);
		if (!Sortable.eventCanceled) {
			cloneEl = clone(dragEl);
			cloneEl.removeAttribute("id");
			cloneEl.draggable = false;
			cloneEl.style['will-change'] = '';

			this._hideClone();

			toggleClass(cloneEl, this.options.chosenClass, false);
			Sortable.clone = cloneEl;
		}


		// #1143: IFrame support workaround
		_this.cloneId = _nextTick(function() {
			pluginEvent('clone', _this);
			if (Sortable.eventCanceled) return;

			if (!_this.options.removeCloneOnHide) {
				rootEl.insertBefore(cloneEl, dragEl);
			}
			_this._hideClone();

			_dispatchEvent({
				sortable: _this,
				name: 'clone'
			});
		});


		!fallback && toggleClass(dragEl, options.dragClass, true);

		// Set proper drop events
		if (fallback) {
			ignoreNextClick = true;
			_this._loopId = setInterval(_this._emulateDragOver, 50);
		} else {
			// Undo what was set in _prepareDragStart before drag started
			off(document, 'mouseup', _this._onDrop);
			off(document, 'touchend', _this._onDrop);
			off(document, 'touchcancel', _this._onDrop);

			if (dataTransfer) {
				dataTransfer.effectAllowed = 'move';
				options.setData && options.setData.call(_this, dataTransfer, dragEl);
			}

			on(document, 'drop', _this);

			// #1276 fix:
			css(dragEl, 'transform', 'translateZ(0)');
		}

		awaitingDragStarted = true;

		_this._dragStartId = _nextTick(_this._dragStarted.bind(_this, fallback, evt));
		on(document, 'selectstart', _this);

		moved = true;

		window.getSelection().removeAllRanges();

		if (Safari) {
			css(document.body, 'user-select', 'none');
		}
	}
```

### 🔹 函式: `_triggerDragStart()`
- **變更前簽章 (Before)**: `_triggerDragStart(/** Event */evt, /** Touch */touch)` (L701~L730)
- **變更後簽章 (After)**: `_triggerDragStart(/** Event */evt, /** Touch */touch)` (L701~L728)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/** Event */evt, /** Touch */touch) {
		touch = touch || (evt.pointerType == 'touch' && evt);

		if (!this.nativeDraggable || touch) {
			if (this.options.supportPointer) {
				on(document, 'pointermove', this._onTouchMove);
			} else if (touch) {
				on(document, 'touchmove', this._onTouchMove);
			} else {
				on(document, 'mousemove', this._onTouchMove);
			}
		} else {
			on(dragEl, 'dragend', this);
			on(rootEl, 'dragstart', this._onDragStart);
		}

		try {
			if (this.nativeDraggable) {
				window.getSelection().removeAllRanges();
			}
			_nextTick(() => {
				if (document.selection) {
					document.selection.empty();
				} else if (!this.nativeDraggable) {
					window.getSelection().removeAllRanges();
				}
			});
		} catch (err) {
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/** Event */evt, /** Touch */touch) {
		touch = touch || (evt.pointerType == 'touch' && evt);

		if (!this.nativeDraggable || touch) {
			if (this.options.supportPointer) {
				on(document, 'pointermove', this._onTouchMove);
			} else if (touch) {
				on(document, 'touchmove', this._onTouchMove);
			} else {
				on(document, 'mousemove', this._onTouchMove);
			}
		} else {
			on(dragEl, 'dragend', this);
			on(rootEl, 'dragstart', this._onDragStart);
		}

		try {
			
			if (document.selection) {
				_nextTick(() => {
					document.selection.empty();
				});
			} else if (this.nativeDraggable) {
				window.getSelection().removeAllRanges();
			}
		} catch (err) {
		}
	}
```


---


---





================================================================================

### 📁 代表專案 #2: `ratatui` (08)

> **生態與抽樣意圖**: 展示「97.1% 結構性呼叫電線增修、100% 捕獲」之細粒度模組化生態 (Rust)  

> **完整 20-Commit 報告位址**: `reports/per_repo_audits/08_ratatui.md`


# 🔬 CODE-Map 基準審查獨立驗證報告: `ratatui`
> **技術生態**: `Rust (終端 UI / 系統級緩衝繪製)`  
> **本地倉庫路徑**: `test_repos/ratatui`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 34 Files  
> **報告生成時間**: 2026-10-20 21:41:04  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `33` / `34` | `97.1%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `1` / `34` | `2.9%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `0` / `34` | `0.0%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`34` / `34`** | **`100.0%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `34` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

---

### 📋 精選代表性修復 Commit 形式化證據 (抽樣前 3 項 / 共 20 項)

### 🔹 Commit #01: `d1ef782b`
- **完整 Hash**: `d1ef782b48ddf0cb825c111d4d8b9adef572c0e1`
- **說明 (Ground Truth)**: fix(charts): clip rendering to buffer bounds (#2817)
- **變更檔案數**: 3

#### 📄 檔案: `ratatui-widgets/src/barchart.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:219, E:534, A:0) ➔ After(N:226, E:550, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 16, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_barchart_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增節點] `Buffer::filled (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_barchart_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增呼叫邊] `BarChart::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `BarChart::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `render_barchart_outside_buffer_is_noop` ──[CALLS]──> `BarChart::new`
  • + [新增呼叫邊] `render_barchart_outside_buffer_is_noop` ──[CALLS]──> `Buffer::filled (External/Unresolved)`
  • + [新增呼叫邊] `render_barchart_outside_buffer_is_noop` ──[CALLS]──> `buf.clone (External/Unresolved)`
  • + [新增呼叫邊] `render_barchart_outside_buffer_is_noop` ──[CALLS]──> `BarChart::render`
  • + [新增呼叫邊] `render_barchart_outside_buffer_is_noop` ──[CALLS]──> `data`
  • + [新增呼叫邊] `render_barchart_outside_buffer_is_noop` ──[CALLS]──> `BarChart::default`
  • _... 以及其餘 8 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `BarChart::render()`
- **變更前簽章 (Before)**: `fn BarChart::render(self, area: Rect, buf: &mut Buffer)` (L705~L719)
- **變更後簽章 (After)**: `fn BarChart::render(self, area: Rect, buf: &mut Buffer)` (L705~L724)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        buf.set_style(area, self.style);

        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);

        if inner.is_empty() || self.data.is_empty() || self.bar_width == 0 {
            return;
        }

        match self.direction {
            Direction::Horizontal => self.render_horizontal(buf, inner),
            Direction::Vertical => self.render_vertical(buf, inner),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        buf.set_style(area, self.style);

        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);

        if inner.is_empty() || self.data.is_empty() || self.bar_width == 0 {
            return;
        }

        match self.direction {
            Direction::Horizontal => self.render_horizontal(buf, inner),
            Direction::Vertical => self.render_vertical(buf, inner),
        }
    }
```


#### 📄 檔案: `ratatui-widgets/src/chart.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:182, E:329, A:0) ➔ After(N:189, E:347, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 18, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Buffer::filled (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_chart_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_chart_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增呼叫邊] `Chart::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `Chart::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `render_chart_outside_buffer_is_noop` ──[CALLS]──> `Chart::new`
  • + [新增呼叫邊] `render_chart_outside_buffer_is_noop` ──[CALLS]──> `Buffer::filled (External/Unresolved)`
  • + [新增呼叫邊] `render_chart_outside_buffer_is_noop` ──[CALLS]──> `buf.clone (External/Unresolved)`
  • + [新增呼叫邊] `render_chart_outside_buffer_is_noop` ──[CALLS]──> `Chart::render`
  • + [新增呼叫邊] `render_chart_outside_buffer_is_noop` ──[CALLS]──> `vec! (Macro)`
  • + [新增呼叫邊] `render_chart_outside_buffer_is_noop` ──[CALLS]──> `assert_eq! (Macro)`
  • _... 以及其餘 10 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Chart::render()`
- **變更前簽章 (Before)**: `fn Chart::render(self, area: Rect, buf: &mut Buffer)` (L1002~L1157)
- **變更後簽章 (After)**: `fn Chart::render(self, area: Rect, buf: &mut Buffer)` (L1002~L1162)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        buf.set_style(area, self.style);

        self.block.as_ref().render(area, buf);
        let chart_area = self.block.inner_if_some(area);
        let Some(layout) = self.layout(chart_area) else {
            return;
        };
        let graph_area = layout.graph_area;

        // Sample the style of the entire widget. This sample will be used to reset the style of
        // the cells that are part of the components put on top of the grah area (i.e legend and
        // axis names).
        let original_style = buf[(area.left(), area.top())].style();

        self.render_x_labels(buf, &layout, chart_area, graph_area);
        self.render_y_labels(buf, &layout, chart_area, graph_area);

        if let Some(y) = layout.axis_x {
            for x in graph_area.left()..graph_area.right() {
                buf[(x, y)]
                    .set_symbol(symbols::line::HORIZONTAL)
                    .set_style(self.x_axis.style);
            }
        }

        if let Some(x) = layout.axis_y {
            for y in graph_area.top()..graph_area.bottom() {
                buf[(x, y)]
                    .set_symbol(symbols::line::VERTICAL)
                    .set_style(self.y_axis.style);
            }
        }

        if let Some(y) = layout.axis_x
            && let Some(x) = layout.axis_y
        {
            buf[(x, y)]
                .set_symbol(symbols::line::BOTTOM_LEFT)
                .set_style(self.x_axis.style);
        }

        Canvas::default()
            .background_color(self.style.bg.unwrap_or(Color::Reset))
            .x_bounds(self.x_axis.bounds)
            .y_bounds(self.y_axis.bounds)
            .paint(|ctx| {
                for dataset in &self.datasets {
                    ctx.marker(dataset.marker);

                    let color = dataset.style.fg.unwrap_or(Color::Reset);
                    ctx.draw(&Points {
                        coords: dataset.data,
                        color,
                    });
                    match dataset.graph_type {
                        GraphType::Line => {
                            for data in dataset.data.windows(2) {
                                ctx.draw(&CanvasLine {
                                    x1: data[0].0,
                                    y1: data[0].1,
                                    x2: data[1].0,
                                    y2: data[1].1,
                                    color,
                                });
                            }
                        }
                        GraphType::Bar => {
                            for (x, y) in dataset.data {
                                ctx.draw(&CanvasLine {
                                    x1: *x,
                                    y1: 0.0,
                                    x2: *x,
                                    y2: *y,
                                    color,
                                });
                            }
                        }
                        GraphType::Area => {
                            for data in dataset.data.windows(2) {
                                ctx.draw(&FilledLine {
                                    x1: data[0].0,
                                    y1: data[0].1,
                                    x2: data[1].0,
                                    y2: data[1].1,
                                    fill_to_y: dataset.fill_to_y,
                                    color,
                                });
                            }
                        }

                        GraphType::Scatter => {}
                    }
                }
            })
            .render(graph_area, buf);

        if let Some(Position { x, y }) = layout.title_x {
            let title = self.x_axis.title.as_ref().unwrap();
            let width = graph_area
                .right()
                .saturating_sub(x)
                .min(title.width() as u16);
            buf.set_style(
                Rect {
                    x,
                    y,
                    width,
                    height: 1,
                },
                original_style,
            );
            buf.set_line(x, y, title, width);
        }

        if let Some(Position { x, y }) = layout.title_y {
            let title = self.y_axis.title.as_ref().unwrap();
            let width = graph_area
                .right()
                .saturating_sub(x)
                .min(title.width() as u16);
            buf.set_style(
                Rect {
                    x,
                    y,
                    width,
                    height: 1,
                },
                original_style,
            );
            buf.set_line(x, y, title, width);
        }

        if let Some(legend_area) = layout.legend_area {
            buf.set_style(legend_area, original_style);
            Block::bordered().render(legend_area, buf);

            for (i, (dataset_name, dataset_style)) in self
                .datasets
                .iter()
                .filter_map(|ds| Some((ds.name.as_ref()?, ds.style())))
                .enumerate()
            {
                let name = dataset_name.clone().patch_style(dataset_style);
                name.render(
                    Rect {
                        x: legend_area.x + 1,
                        y: legend_area.y + 1 + i as u16,
                        width: legend_area.width - 2,
                        height: 1,
                    },
                    buf,
                );
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        buf.set_style(area, self.style);

        self.block.as_ref().render(area, buf);
        let chart_area = self.block.inner_if_some(area);
        let Some(layout) = self.layout(chart_area) else {
            return;
        };
        let graph_area = layout.graph_area;

        // Sample the style of the entire widget. This sample will be used to reset the style of
        // the cells that are part of the components put on top of the grah area (i.e legend and
        // axis names).
        let original_style = buf[(area.left(), area.top())].style();

        self.render_x_labels(buf, &layout, chart_area, graph_area);
        self.render_y_labels(buf, &layout, chart_area, graph_area);

        if let Some(y) = layout.axis_x {
            for x in graph_area.left()..graph_area.right() {
                buf[(x, y)]
                    .set_symbol(symbols::line::HORIZONTAL)
                    .set_style(self.x_axis.style);
            }
        }

        if let Some(x) = layout.axis_y {
            for y in graph_area.top()..graph_area.bottom() {
                buf[(x, y)]
                    .set_symbol(symbols::line::VERTICAL)
                    .set_style(self.y_axis.style);
            }
        }

        if let Some(y) = layout.axis_x
            && let Some(x) = layout.axis_y
        {
            buf[(x, y)]
                .set_symbol(symbols::line::BOTTOM_LEFT)
                .set_style(self.x_axis.style);
        }

        Canvas::default()
            .background_color(self.style.bg.unwrap_or(Color::Reset))
            .x_bounds(self.x_axis.bounds)
            .y_bounds(self.y_axis.bounds)
            .paint(|ctx| {
                for dataset in &self.datasets {
                    ctx.marker(dataset.marker);

                    let color = dataset.style.fg.unwrap_or(Color::Reset);
                    ctx.draw(&Points {
                        coords: dataset.data,
                        color,
                    });
                    match dataset.graph_type {
                        GraphType::Line => {
                            for data in dataset.data.windows(2) {
                                ctx.draw(&CanvasLine {
                                    x1: data[0].0,
                                    y1: data[0].1,
                                    x2: data[1].0,
                                    y2: data[1].1,
                                    color,
                                });
                            }
                        }
                        GraphType::Bar => {
                            for (x, y) in dataset.data {
                                ctx.draw(&CanvasLine {
                                    x1: *x,
                                    y1: 0.0,
                                    x2: *x,
                                    y2: *y,
                                    color,
                                });
                            }
                        }
                        GraphType::Area => {
                            for data in dataset.data.windows(2) {
                                ctx.draw(&FilledLine {
                                    x1: data[0].0,
                                    y1: data[0].1,
                                    x2: data[1].0,
                                    y2: data[1].1,
                                    fill_to_y: dataset.fill_to_y,
                                    color,
                                });
                            }
                        }

                        GraphType::Scatter => {}
                    }
                }
            })
            .render(graph_area, buf);

        if let Some(Position { x, y }) = layout.title_x {
            let title = self.x_axis.title.as_ref().unwrap();
            let width = graph_area
                .right()
                .saturating_sub(x)
                .min(title.width() as u16);
            buf.set_style(
                Rect {
                    x,
                    y,
                    width,
                    height: 1,
                },
                original_style,
            );
            buf.set_line(x, y, title, width);
        }

        if let Some(Position { x, y }) = layout.title_y {
            let title = self.y_axis.title.as_ref().unwrap();
            let width = graph_area
                .right()
                .saturating_sub(x)
                .min(title.width() as u16);
            buf.set_style(
                Rect {
                    x,
                    y,
                    width,
                    height: 1,
                },
                original_style,
            );
            buf.set_line(x, y, title, width);
        }

        if let Some(legend_area) = layout.legend_area {
            buf.set_style(legend_area, original_style);
            Block::bordered().render(legend_area, buf);

            for (i, (dataset_name, dataset_style)) in self
                .datasets
                .iter()
                .filter_map(|ds| Some((ds.name.as_ref()?, ds.style())))
                .enumerate()
            {
                let name = dataset_name.clone().patch_style(dataset_style);
                name.render(
                    Rect {
                        x: legend_area.x + 1,
                        y: legend_area.y + 1 + i as u16,
                        width: legend_area.width - 2,
                        height: 1,
                    },
                    buf,
                );
            }
        }
    }
```


#### 📄 檔案: `ratatui-widgets/src/sparkline.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:137, E:402, A:0) ➔ After(N:144, E:419, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 17, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_sparkline_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增節點] `render_sparkline_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `ratatui_core::buffer::Cell::new (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Sparkline::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `Sparkline::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `render_sparkline_outside_buffer_is_noop` ──[CALLS]──> `Rect::new (External/Unresolved)`
  • + [新增呼叫邊] `render_sparkline_outside_buffer_is_noop` ──[CALLS]──> `Buffer::filled (External/Unresolved)`
  • + [新增呼叫邊] `render_sparkline_outside_buffer_is_noop` ──[CALLS]──> `ratatui_core::buffer::Cell::new (External/Unresolved)`
  • + [新增呼叫邊] `render_sparkline_outside_buffer_is_noop` ──[CALLS]──> `buf.clone (External/Unresolved)`
  • + [新增呼叫邊] `render_sparkline_outside_buffer_is_noop` ──[CALLS]──> `render`
  • + [新增呼叫邊] `render_sparkline_outside_buffer_is_noop` ──[CALLS]──> `Sparkline::data`
  • _... 以及其餘 9 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Sparkline::render()`
- **變更前簽章 (Before)**: `fn Sparkline::render(self, area: Rect, buf: &mut Buffer)` (L390~L394)
- **變更後簽章 (After)**: `fn Sparkline::render(self, area: Rect, buf: &mut Buffer)` (L390~L399)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);
        self.render_sparkline(inner, buf);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);
        self.render_sparkline(inner, buf);
    }
```


---


---

### 🔹 Commit #02: `5a57af20`
- **完整 Hash**: `5a57af20a2260b31753780d791a6c1b0d56d33eb`
- **說明 (Ground Truth)**: fix(widgets): clip string rendering to buffer (#2815)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-core/src/widgets/widget.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:20, E:30, A:0) ➔ After(N:28, E:45, A:0)
- **差分統計**: +Nodes: 8, -Nodes: 0, +Edges: 17, -Edges: 2, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_string_widgets_outside_buffer` (FUNCTION_DEF)
  • + [新增節點] `buf.reset (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.as_str (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Buffer::with_lines (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_string_widgets_clip_to_buffer` (FUNCTION_DEF)
  • + [新增呼叫邊] `str::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `str::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `String::render` ──[CALLS]──> `String::render`
  • + [新增呼叫邊] `String::render` ──[CALLS]──> `self.as_str (External/Unresolved)`
  • + [新增呼叫邊] `render_string_widgets_outside_buffer` ──[CALLS]──> `Buffer::empty (External/Unresolved)`
  • + [新增呼叫邊] `render_string_widgets_outside_buffer` ──[CALLS]──> `buf.clone (External/Unresolved)`
  • + [新增呼叫邊] `render_string_widgets_outside_buffer` ──[CALLS]──> `render`
  • _... 以及其餘 12 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `str::render()`
- **變更前簽章 (Before)**: `fn str::render(self, area: Rect, buf: &mut Buffer)` (L85~L87)
- **變更後簽章 (After)**: `fn str::render(self, area: Rect, buf: &mut Buffer)` (L85~L91)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        buf.set_stringn(area.x, area.y, self, area.width as usize, Style::new());
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }
        buf.set_stringn(area.x, area.y, self, area.width as usize, Style::new());
    }
```

### 🔹 函式: `String::render()`
- **變更前簽章 (Before)**: `fn String::render(self, area: Rect, buf: &mut Buffer)` (L95~L97)
- **變更後簽章 (After)**: `fn String::render(self, area: Rect, buf: &mut Buffer)` (L99~L101)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        buf.set_stringn(area.x, area.y, self, area.width as usize, Style::new());
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        self.as_str().render(area, buf);
    }
```


---


---

### 🔹 Commit #03: `7125ef2e`
- **完整 Hash**: `7125ef2ec3dbb12d10e12d75c72aee40cf9fecbb`
- **說明 (Ground Truth)**: fix(calendar): respect rendering bounds (#2819)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-widgets/src/calendar.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:111, E:145, A:0) ➔ After(N:121, E:172, A:0)
- **差分統計**: +Nodes: 10, -Nodes: 0, +Edges: 27, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_calendar_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增節點] `days_area.bottom (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_calendar_stays_within_requested_rows` (FUNCTION_DEF)
  • + [新增節點] `Date::from_calendar_date(2026, Month::October, 8).expect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Buffer::filled (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_calendar_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增呼叫邊] `Monthly::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `Monthly::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `Monthly::render_monthly` ──[CALLS]──> `days_area.bottom (External/Unresolved)`
  • + [新增呼叫邊] `render_calendar_outside_buffer_is_noop` ──[CALLS]──> `Monthly::new`
  • + [新增呼叫邊] `render_calendar_outside_buffer_is_noop` ──[CALLS]──> `Buffer::filled (External/Unresolved)`
  • _... 以及其餘 22 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Monthly::render_monthly()`
- **變更前簽章 (Before)**: `fn Monthly::render_monthly(&self, area: Rect, buf: &mut Buffer)` (L182~L230)
- **變更後簽章 (After)**: `fn Monthly::render_monthly(&self, area: Rect, buf: &mut Buffer)` (L187~L233)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render_monthly(&self, area: Rect, buf: &mut Buffer) {
        let layout = Layout::vertical([
            Constraint::Length(self.show_month.is_some().into()),
            Constraint::Length(self.show_weekday.is_some().into()),
            Constraint::Fill(1),
        ]);
        let [month_header, days_header, days_area] = layout.areas(area);

        // Draw the month name and year
        if let Some(style) = self.show_month {
            Line::styled(
                format!("{} {}", self.display_date.month(), self.display_date.year()),
                style,
            )
            .alignment(Alignment::Center)
            .render(month_header, buf);
        }

        // Draw days of week
        if let Some(style) = self.show_weekday {
            Span::styled(" Su Mo Tu We Th Fr Sa", style).render(days_header, buf);
        }

        // Set the start of the calendar to the Sunday before the 1st (or the sunday of the first)
        let first_of_month = self.display_date.replace_day(1).unwrap();
        let offset = Duration::days(first_of_month.weekday().number_days_from_sunday().into());
        let mut curr_day = first_of_month - offset;

        let mut y = days_area.y;
        // go through all the weeks containing a day in the target month.
        while curr_day.month() != self.display_date.month().next() {
            let mut spans = Vec::with_capacity(14);
            for i in 0..7 {
                // Draw the gutter. Do it here so we can avoid worrying about
                // styling the ' ' in the format_date method
                if i == 0 {
                    spans.push(Span::styled(" ", Style::default()));
                } else {
                    spans.push(Span::styled(" ", self.default_bg()));
                }
                spans.push(self.format_date(curr_day));
                curr_day += Duration::DAY;
            }
            if buf.area.height > y {
                buf.set_line(days_area.x, y, &spans.into(), area.width);
            }
            y += 1;
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render_monthly(&self, area: Rect, buf: &mut Buffer) {
        let layout = Layout::vertical([
            Constraint::Length(self.show_month.is_some().into()),
            Constraint::Length(self.show_weekday.is_some().into()),
            Constraint::Fill(1),
        ]);
        let [month_header, days_header, days_area] = layout.areas(area);

        // Draw the month name and year
        if let Some(style) = self.show_month {
            Line::styled(
                format!("{} {}", self.display_date.month(), self.display_date.year()),
                style,
            )
            .alignment(Alignment::Center)
            .render(month_header, buf);
        }

        // Draw days of week
        if let Some(style) = self.show_weekday {
            Span::styled(" Su Mo Tu We Th Fr Sa", style).render(days_header, buf);
        }

        // Set the start of the calendar to the Sunday before the 1st (or the sunday of the first)
        let first_of_month = self.display_date.replace_day(1).unwrap();
        let offset = Duration::days(first_of_month.weekday().number_days_from_sunday().into());
        let mut curr_day = first_of_month - offset;

        let mut y = days_area.y;
        // go through all the weeks containing a day in the target month.
        while curr_day.month() != self.display_date.month().next() && y < days_area.bottom() {
            let mut spans = Vec::with_capacity(14);
            for i in 0..7 {
                // Draw the gutter. Do it here so we can avoid worrying about
                // styling the ' ' in the format_date method
                if i == 0 {
                    spans.push(Span::styled(" ", Style::default()));
                } else {
                    spans.push(Span::styled(" ", self.default_bg()));
                }
                spans.push(self.format_date(curr_day));
                curr_day += Duration::DAY;
            }
            buf.set_line(days_area.x, y, &spans.into(), days_area.width);
            y += 1;
        }
    }
```

### 🔹 函式: `Monthly::render()`
- **變更前簽章 (Before)**: `fn Monthly::render(self, area: Rect, buf: &mut Buffer)` (L174~L178)
- **變更後簽章 (After)**: `fn Monthly::render(self, area: Rect, buf: &mut Buffer)` (L174~L183)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);
        self.render_monthly(inner, buf);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);
        self.render_monthly(inner, buf);
    }
```


---


---





================================================================================

### 📁 代表專案 #3: `preact` (12)

> **生態與抽樣意圖**: 展示客觀標記 Barrel 轉發為 ZERO_DELTA，以及捕捉到閉包作用域阻隔死穴 BLOCKED_SCOPE (JavaScript)  

> **完整 20-Commit 報告位址**: `reports/per_repo_audits/12_preact.md`


# 🔬 CODE-Map 基準審查獨立驗證報告: `preact`
> **技術生態**: `JavaScript (極致輕量 Virtual DOM / Hooks)`  
> **本地倉庫路徑**: `test_repos/preact`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 30 Files  
> **報告生成時間**: 2026-10-20 21:41:26  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `6` / `30` | `20.0%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `22` / `30` | `73.3%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `2` / `30` | `6.7%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`28` / `30`** | **`93.3%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `30` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

---

### 📋 精選代表性修復 Commit 形式化證據 (抽樣前 3 項 / 共 20 項)

### 🔹 Commit #01: `a9dc9b01`
- **完整 Hash**: `a9dc9b01073f2d9040e2fd45216bf296ec10ace0`
- **說明 (Ground Truth)**: Reduce core diff bundle size
- **變更檔案數**: 3

#### 📄 檔案: `src/diff/children.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:12, E:14, A:0) ➔ After(N:12, E:14, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `constructNewChildrenArray()`
- **變更前簽章 (Before)**: `function constructNewChildrenArray(
	newParentVNode,
	renderResult,
	oldChildren,
	oldDom,
	newChildrenLength
)` (L159~L375)
- **變更後簽章 (After)**: `function constructNewChildrenArray(
	newParentVNode,
	renderResult,
	oldChildren,
	oldDom,
	newChildrenLength
)` (L159~L375)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function constructNewChildrenArray(
	newParentVNode,
	renderResult,
	oldChildren,
	oldDom,
	newChildrenLength
) {
	/** @type {number} */
	let i;
	/** @type {VNode} */
	let childVNode;
	/** @type {VNode} */
	let oldVNode;

	let oldChildrenLength = oldChildren.length,
		remainingOldChildren = oldChildrenLength;

	let skew = 0;

	/** Whether any matched child was found far from its skewed index, i.e. a
	 * real reorder happened and we need to compute the minimal set of moves. */
	let moved = false;

	// Hoisted: every normalization branch below writes through this array, so
	// reading `_children` off the vnode each time is a wasted property load.
	/** @type {VNode[]} */
	let newChildren = (newParentVNode._children = Array(newChildrenLength));
	for (i = 0; i < newChildrenLength; i++) {
		// @ts-expect-error We are reusing the childVNode variable to hold both the
		// pre and post normalized childVNode
		childVNode = renderResult[i];

		if (
			childVNode == NULL ||
			typeof childVNode == 'boolean' ||
			typeof childVNode == 'function'
		) {
			newChildren[i] = NULL;
			continue;
		}
		// If this newVNode is being reused (e.g. <div>{reuse}{reuse}</div>) in the same diff,
		// or we are rendering a component (e.g. setState) copy the oldVNodes so it can have
		// it's own DOM & etc. pointers
		// Anything that isn't an object at this point is a string, number or
		// bigint (null, booleans and functions are handled above), String
		// objects are the lone object type rendered as text.
		else if (
			typeof childVNode != 'object' ||
			childVNode.constructor == String
		) {
			childVNode = newChildren[i] = createVNode(NULL, childVNode);
		} else if (isArray(childVNode)) {
			childVNode = newChildren[i] = createVNode(Fragment, {
				children: childVNode
			});
		} else if (childVNode.constructor === UNDEFINED && childVNode._depth) {
			// VNode is already in use, clone it. This can happen in the following
			// scenario:
			//   const reuse = <div />
			//   <div>{reuse}<span />{reuse}</div>
			childVNode = newChildren[i] = createVNode(
				childVNode.type,
				childVNode.props,
				childVNode.key,
				childVNode.ref,
				childVNode._original
			);
		} else {
			newChildren[i] = childVNode;
		}

		const skewedIndex = i + skew;
		childVNode._parent = newParentVNode;
		childVNode._depth = newParentVNode._depth + 1;

		// Temporarily store the matchingIndex on the _index property so we can pull
		// out the oldVNode in diffChildren. We'll override this to the VNode's
		// final index after using this property to get the oldVNode
		const matchingIndex = (childVNode._index = findMatchingIndex(
			childVNode,
			oldChildren,
			skewedIndex,
			remainingOldChildren
		));

		oldVNode = NULL;
		// ~matchingIndex is only falsy for -1, i.e. when no match was found
		if (~matchingIndex) {
			oldVNode = oldChildren[matchingIndex];
			remainingOldChildren--;
			if (oldVNode) {
				oldVNode._flags |= MATCHED;
			}
		}

		// Here, we define isMounting for the purposes of the skew diffing
		// algorithm. Nodes that are unsuspending are considered mounting and we detect
		// this by checking if oldVNode._original == null
		if (!oldVNode || !oldVNode._original) {
			if (!~matchingIndex) {
				// When the array of children is growing we need to decrease the skew
				// as we are adding a new element to the array.
				// Example:
				// [1, 2, 3] --> [0, 1, 2, 3]
				// oldChildren   newChildren
				//
				// The new element is at index 0, so our skew is 0,
				// we need to decrease the skew as we are adding a new element.
				// The decrease will cause us to compare the element at position 1
				// with value 1 with the element at position 0 with value 0.
				//
				// A linear concept is applied when the array is shrinking,
				// if the length is unchanged we can assume that no skew
				// changes are needed.
				if (newChildrenLength > oldChildrenLength) {
					skew--;
				} else if (newChildrenLength < oldChildrenLength) {
					skew++;
				}
			}

			// If we are mounting a DOM VNode, mark it for insertion
			if (typeof childVNode.type != 'function') {
				childVNode._flags |= INSERT_VNODE;
			}
		} else {
			// Matched children are candidates for the minimal-move pass below;
			// MATCHED on a _new_ vnode is cleared in diffChildren's placement loop.
			childVNode._flags |= MATCHED;

			// The skew adjustments keep findMatchingIndex's search centered for
			// shift patterns (insertions/removals at the front). A match further
			// than one position away means children were genuinely reordered:
			// flag it so the minimal set of moves is computed below. Off-by-one
			// matches provably keep matched old indices in increasing order, so
			// no moves are needed for them.
			if (matchingIndex == skewedIndex - 1) {
				skew--;
			} else if (matchingIndex == skewedIndex + 1) {
				skew++;
			} else if (matchingIndex != skewedIndex) {
				if (matchingIndex > skewedIndex) {
					skew--;
				} else {
					skew++;
				}

				moved = true;
			}
		}
	}

	if (moved) {
		// Children were reordered: mark the minimal set of matched (MATCHED flag)
		// children for insertion by finding the longest increasing subsequence of
		// old indices (patience sorting). Children on the subsequence stay in
		// place, all others get INSERT_VNODE. `_index` still holds the
		// matchingIndex here.
		/** @type {number[]} tails[x] is the smallest old index ending an increasing subsequence of length x+1 */
		let tails = [];
		/** @type {number[]} length of the longest increasing subsequence ending at child i */
		let lisLengths = [];
		for (i = 0; i < newChildrenLength; i++) {
			childVNode = newChildren[i];
			if (childVNode && childVNode._flags & MATCHED) {
				// Binary search for the insertion point, keeping the pass at
				// O(n log n) even for pathological reorders.
				let lo = 0,
					hi = tails.length;
				while (lo < hi) {
					const mid = (lo + hi) >> 1;
					if (tails[mid] < childVNode._index) {
						lo = mid + 1;
					} else {
						hi = mid;
					}
				}
				tails[lo] = childVNode._index;
				lisLengths[i] = lo + 1;
			}
		}

		// `skew` is dead after the main loop; reuse it as the remaining
		// subsequence length while walking backwards. Likewise `i` is left at
		// newChildrenLength by the loop above.
		skew = tails.length;
		while (i--) {
			if (lisLengths[i]) {
				if (lisLengths[i] == skew) {
					skew--;
				} else {
					newChildren[i]._flags |= INSERT_VNODE;
				}
			}
		}
	}

	// Remove remaining oldChildren if there are any. Loop forwards so that as we
	// unmount DOM from the beginning of the oldChildren, we can adjust oldDom to
	// point to the next child, which needs to be the first DOM node that won't be
	// unmounted. Keep this a plain loop: an arrow function here would capture
	// `oldDom`, forcing V8 to context-allocate it on every call to this function.
	if (remainingOldChildren) {
		for (i = 0; i < oldChildrenLength; i++) {
			oldVNode = oldChildren[i];
			if (oldVNode && !(oldVNode._flags & MATCHED)) {
				if (oldVNode._dom == oldDom) {
					oldDom = getDomSibling(oldVNode);
				}

				unmount(oldVNode, oldVNode);
			}
		}
	}

	return oldDom;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function constructNewChildrenArray(
	newParentVNode,
	renderResult,
	oldChildren,
	oldDom,
	newChildrenLength
) {
	/** @type {number} */
	let i;
	/** @type {VNode} */
	let childVNode;
	/** @type {VNode} */
	let oldVNode;

	let oldChildrenLength = oldChildren.length,
		remainingOldChildren = oldChildrenLength;

	let skew = 0;

	/** Whether any matched child was found far from its skewed index, i.e. a
	 * real reorder happened and we need to compute the minimal set of moves. */
	let moved = false;

	// Hoisted: every normalization branch below writes through this array, so
	// reading `_children` off the vnode each time is a wasted property load.
	/** @type {VNode[]} */
	let newChildren = (newParentVNode._children = Array(newChildrenLength));
	for (i = 0; i < newChildrenLength; i++) {
		// @ts-expect-error We are reusing the childVNode variable to hold both the
		// pre and post normalized childVNode
		childVNode = renderResult[i];

		if (
			childVNode == NULL ||
			typeof childVNode == 'boolean' ||
			typeof childVNode == 'function'
		) {
			newChildren[i] = NULL;
			continue;
		}
		// If this newVNode is being reused (e.g. <div>{reuse}{reuse}</div>) in the same diff,
		// or we are rendering a component (e.g. setState) copy the oldVNodes so it can have
		// it's own DOM & etc. pointers
		// Anything that isn't an object at this point is a string, number or
		// bigint (null, booleans and functions are handled above), String
		// objects are the lone object type rendered as text.
		else if (
			typeof childVNode != 'object' ||
			childVNode.constructor == String
		) {
			childVNode = newChildren[i] = createVNode(NULL, childVNode);
		} else if (isArray(childVNode)) {
			childVNode = newChildren[i] = createVNode(Fragment, {
				children: childVNode
			});
		} else if (childVNode.constructor === UNDEFINED && childVNode._depth) {
			// VNode is already in use, clone it. This can happen in the following
			// scenario:
			//   const reuse = <div />
			//   <div>{reuse}<span />{reuse}</div>
			childVNode = newChildren[i] = createVNode(
				childVNode.type,
				childVNode.props,
				childVNode.key,
				childVNode.ref,
				childVNode._original
			);
		} else {
			newChildren[i] = childVNode;
		}

		const skewedIndex = i + skew;
		childVNode._parent = newParentVNode;
		childVNode._depth = newParentVNode._depth + 1;

		// Temporarily store the matchingIndex on the _index property so we can pull
		// out the oldVNode in diffChildren. We'll override this to the VNode's
		// final index after using this property to get the oldVNode
		const matchingIndex = (childVNode._index = findMatchingIndex(
			childVNode,
			oldChildren,
			skewedIndex,
			remainingOldChildren
		));

		oldVNode = NULL;
		// ~matchingIndex is only falsy for -1, i.e. when no match was found
		if (~matchingIndex) {
			oldVNode = oldChildren[matchingIndex];
			remainingOldChildren--;
			if (oldVNode) {
				oldVNode._flags |= MATCHED;
			}
		}

		// Here, we define isMounting for the purposes of the skew diffing
		// algorithm. Nodes that are unsuspending are considered mounting and we detect
		// this by checking if oldVNode._original == null
		if (!oldVNode || !oldVNode._original) {
			if (!~matchingIndex) {
				// When the array of children is growing we need to decrease the skew
				// as we are adding a new element to the array.
				// Example:
				// [1, 2, 3] --> [0, 1, 2, 3]
				// oldChildren   newChildren
				//
				// The new element is at index 0, so our skew is 0,
				// we need to decrease the skew as we are adding a new element.
				// The decrease will cause us to compare the element at position 1
				// with value 1 with the element at position 0 with value 0.
				//
				// A linear concept is applied when the array is shrinking,
				// if the length is unchanged we can assume that no skew
				// changes are needed.
				if (newChildrenLength > oldChildrenLength) {
					skew--;
				} else if (newChildrenLength < oldChildrenLength) {
					skew++;
				}
			}

			// If we are mounting a DOM VNode, mark it for insertion
			if (typeof childVNode.type != 'function') {
				childVNode._flags |= INSERT_VNODE;
			}
		} else {
			// Matched children are candidates for the minimal-move pass below;
			// MATCHED on a _new_ vnode is cleared in diffChildren's placement loop.
			childVNode._flags |= MATCHED;

			// The skew adjustments keep findMatchingIndex's search centered for
			// shift patterns (insertions/removals at the front). A match further
			// than one position away means children were genuinely reordered:
			// flag it so the minimal set of moves is computed below. Off-by-one
			// matches provably keep matched old indices in increasing order, so
			// no moves are needed for them.
			if (matchingIndex == skewedIndex - 1) {
				skew--;
			} else if (matchingIndex == skewedIndex + 1) {
				skew++;
			} else if (matchingIndex != skewedIndex) {
				if (matchingIndex > skewedIndex) {
					skew--;
				} else {
					skew++;
				}

				moved = true;
			}
		}
	}

	if (moved) {
		// Children were reordered: mark the minimal set of matched (MATCHED flag)
		// children for insertion by finding the longest increasing subsequence of
		// old indices (patience sorting). Children on the subsequence stay in
		// place, all others get INSERT_VNODE. `_index` still holds the
		// matchingIndex here.
		/** @type {number[]} tails[x] is the smallest old index ending an increasing subsequence of length x+1 */
		let tails = [];
		/** @type {number[]} length of the longest increasing subsequence ending at child i */
		let lisLengths = [];
		for (i = 0; i < newChildrenLength; i++) {
			childVNode = newChildren[i];
			if (childVNode && childVNode._flags & MATCHED) {
				// Binary search for the insertion point, keeping the pass at
				// O(n log n) even for pathological reorders.
				skew = 0;
				let hi = tails.length;
				while (skew < hi) {
					const mid = (skew + hi) >> 1;
					if (tails[mid] < childVNode._index) {
						skew = mid + 1;
					} else {
						hi = mid;
					}
				}
				tails[skew] = childVNode._index;
				lisLengths[i] = skew + 1;
			}
		}

		// `skew` is dead after the main loop; reuse it as the remaining
		// subsequence length while walking backwards. Likewise `i` is left at
		// newChildrenLength by the loop above.
		skew = tails.length;
		while (i--) {
			if (lisLengths[i]) {
				if (lisLengths[i] == skew) {
					skew--;
				} else {
					newChildren[i]._flags |= INSERT_VNODE;
				}
			}
		}
	}

	// Remove remaining oldChildren if there are any. Loop forwards so that as we
	// unmount DOM from the beginning of the oldChildren, we can adjust oldDom to
	// point to the next child, which needs to be the first DOM node that won't be
	// unmounted. Keep this a plain loop: an arrow function here would capture
	// `oldDom`, forcing V8 to context-allocate it on every call to this function.
	if (remainingOldChildren) {
		for (i = 0; i < oldChildrenLength; i++) {
			oldVNode = oldChildren[i];
			if (oldVNode && !(oldVNode._flags & MATCHED)) {
				if (oldVNode._dom == oldDom) {
					oldDom = getDomSibling(oldVNode);
				}

				unmount(oldVNode, oldVNode);
			}
		}
	}

	return oldDom;
}
```

### 🔹 函式: `findMatchingIndex()`
- **變更前簽章 (Before)**: `function findMatchingIndex(
	childVNode,
	oldChildren,
	skewedIndex,
	remainingOldChildren
)` (L462~L513)
- **變更後簽章 (After)**: `function findMatchingIndex(
	childVNode,
	oldChildren,
	skewedIndex,
	remainingOldChildren
)` (L462~L520)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function findMatchingIndex(
	childVNode,
	oldChildren,
	skewedIndex,
	remainingOldChildren
) {
	const key = childVNode.key;
	const type = childVNode.type;
	let oldVNode = oldChildren[skewedIndex];
	const matched = oldVNode && !(oldVNode._flags & MATCHED);

	// We only need to perform a search if there are more children
	// (remainingOldChildren) to search. However, if the oldVNode we just looked
	// at skewedIndex was not already used in this diff, then there must be at
	// least 1 other (so greater than 1) remainingOldChildren to attempt to match
	// against. So the following condition checks that ensuring
	// remainingOldChildren > 1 if the oldVNode is not already used/matched. Else
	// if the oldVNode was null or matched, then there could needs to be at least
	// 1 (aka `remainingOldChildren > 0`) children to find and compare against.
	//
	// If there is an unkeyed functional VNode, that isn't a built-in like our Fragment,
	// we should not search as we risk re-using state of an unrelated VNode. (reverted for now)
	let shouldSearch =
		// (typeof type != 'function' || type === Fragment || key) &&
		// The ternary keeps this a Smi comparison; `> matched` would compare
		// number to boolean which V8 can't serve from the fast path.
		remainingOldChildren > (matched ? 1 : 0);

	if (
		(oldVNode === NULL && key == NULL) ||
		(matched && key == oldVNode.key && type == oldVNode.type)
	) {
		return skewedIndex;
	} else if (shouldSearch) {
		let x = skewedIndex - 1;
		let y = skewedIndex + 1;
		while (x >= 0 || y < oldChildren.length) {
			const childIndex = x >= 0 ? x-- : y++;
			oldVNode = oldChildren[childIndex];
			if (
				oldVNode &&
				!(oldVNode._flags & MATCHED) &&
				key == oldVNode.key &&
				type == oldVNode.type
			) {
				return childIndex;
			}
		}
	}

	return -1;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function findMatchingIndex(
	childVNode,
	oldChildren,
	skewedIndex,
	remainingOldChildren
) {
	const key = childVNode.key;
	const type = childVNode.type;
	let oldVNode = oldChildren[skewedIndex];
	const matched = oldVNode && !(oldVNode._flags & MATCHED);

	// We only need to perform a search if there are more children
	// (remainingOldChildren) to search. However, if the oldVNode we just looked
	// at skewedIndex was not already used in this diff, then there must be at
	// least 1 other (so greater than 1) remainingOldChildren to attempt to match
	// against. So the following condition checks that ensuring
	// remainingOldChildren > 1 if the oldVNode is not already used/matched. Else
	// if the oldVNode was null or matched, then there could needs to be at least
	// 1 (aka `remainingOldChildren > 0`) children to find and compare against.
	//
	// If there is an unkeyed functional VNode, that isn't a built-in like our Fragment,
	// we should not search as we risk re-using state of an unrelated VNode. (reverted for now)
	let shouldSearch =
		// (typeof type != 'function' || type === Fragment || key) &&
		// The ternary keeps this a Smi comparison; `> matched` would compare
		// number to boolean which V8 can't serve from the fast path.
		remainingOldChildren > (matched ? 1 : 0);

	if (
		(oldVNode === NULL && key == NULL) ||
		(matched && key == oldVNode.key && type == oldVNode.type)
	) {
		return skewedIndex;
	} else if (shouldSearch) {
		let x;
		for (x = skewedIndex - 1; x >= 0; x--) {
			oldVNode = oldChildren[x];
			if (
				oldVNode &&
				!(oldVNode._flags & MATCHED) &&
				key == oldVNode.key &&
				type == oldVNode.type
			)
				return x;
		}
		for (x = skewedIndex + 1; x < oldChildren.length; x++) {
			oldVNode = oldChildren[x];
			if (
				oldVNode &&
				!(oldVNode._flags & MATCHED) &&
				key == oldVNode.key &&
				type == oldVNode.type
			)
				return x;
		}
	}

	return -1;
}
```


#### 📄 檔案: `src/diff/index.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:17, E:19, A:0) ➔ After(N:17, E:19, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `diff()`
- **變更前簽章 (Before)**: `function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L57~L469)
- **變更後簽章 (After)**: `function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L57~L469)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	/** @type {any} */
	let tmp,
		resumed,
		newType = newVNode.type;

	// When passing through createElement it assigns the object
	// constructor as undefined. This to prevent JSON-injection.
	if (newVNode.constructor !== UNDEFINED) return NULL;

	// If the previous diff bailed out, resume creating/hydrating into the DOM
	// that was kept while suspended (server-rendered, or already in the
	// container we rendered into). `tmp` holds the stored excess node until the
	// options._diff call below.
	if (
		oldVNode._flags & MODE_SUSPENDED &&
		// @ts-expect-error This is MODE_HYDRATE or 0
		((isHydrating = oldVNode._flags & MODE_HYDRATE),
		(tmp = oldVNode._component._excess))
	) {
		newVNode._flags |= isHydrating;
		resumed = excessDomChildren = [];
		if (tmp.nodeType == 8) {
			// Re-scan DOM from stored start marker for streamed hydration.
			// `depth` only ever reaches 0 through the `break` below, so it
			// doesn't need to be re-tested in the loop condition.
			for (
				let depth = 1, node = tmp.nextSibling;
				node;
				node = node.nextSibling
			) {
				if (node.nodeType == 8) {
					if (node.data.startsWith('$s')) depth++;
					else if (node.data.startsWith('/$s') && !--depth) break;
				}
				excessDomChildren.push(node);
			}
		} else {
			excessDomChildren.push(tmp);
		}
		oldDom = excessDomChildren[0];
	}

	if ((tmp = options._diff)) tmp(newVNode);

	outer: if (typeof newType == 'function') {
		let oldCommitQueueLength = commitQueue.length;
		try {
			let c,
				oldProps,
				oldState,
				snapshot,
				newProps = newVNode.props;
			const isClassComponent = (tmp = newType.prototype) && tmp.render;

			// Necessary for createContext api. Setting this property will pass
			// the context value as `this.context` just for this component.
			tmp = newType.contextType;
			const provider = tmp && globalContext[tmp._id];
			const componentContext = tmp
				? provider
					? provider.props.value
					: tmp._defaultValue
				: globalContext;

			// Get component and set it to `c`
			if (oldVNode._component) {
				c = newVNode._component = oldVNode._component;
				if (c._bits & COMPONENT_PENDING_ERROR) {
					c._bits |= COMPONENT_PROCESSING_EXCEPTION;
				}
			} else {
				// Instantiate the new component
				if (isClassComponent) {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new newType(newProps, componentContext); // eslint-disable-line new-cap
				} else {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new BaseComponent(
						newProps,
						componentContext
					);

					c.constructor = newType;
					c.render = doRender;
				}
				if (provider) provider.sub(c);

				if (!c.state) c.state = {};
				c._globalContext = globalContext;
				c._bits |= COMPONENT_DIRTY;
				c._renderCallbacks = [];
				c._stateCallbacks = [];
			}

			if (isClassComponent) {
				if (!c._nextState) c._nextState = c.state;

				// Invoke getDerivedStateFromProps
				if (newType.getDerivedStateFromProps) {
					if (c._nextState == c.state) {
						c._nextState = assign({}, c._nextState);
					}

					assign(
						c._nextState,
						newType.getDerivedStateFromProps(newProps, c._nextState)
					);
				}
			}

			oldProps = c.props;
			oldState = c.state;
			c._vnode = newVNode;

			// Invoke pre-render lifecycle methods
			if (!oldVNode._component) {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					c.componentWillMount
				) {
					c.componentWillMount();
				}

				if (isClassComponent && c.componentDidMount) {
					c._renderCallbacks.push(c.componentDidMount);
				}
			} else {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					newProps !== oldProps &&
					c.componentWillReceiveProps
				) {
					c.componentWillReceiveProps(newProps, componentContext);
				}

				if (
					(newVNode._original == oldVNode._original &&
						!(c._bits & COMPONENT_DIRTY)) ||
					(!(c._bits & COMPONENT_FORCE) &&
						c.shouldComponentUpdate &&
						c.shouldComponentUpdate(
							newProps,
							c._nextState,
							componentContext
						) === false)
				) {
					// More info about this here: https://gist.github.com/JoviDeCroock/bec5f2ce93544d2e6070ef8e0036e4e8
					if (newVNode._original != oldVNode._original) {
						// When we are dealing with a bail because of sCU we have to update
						// the props, state and dirty-state.
						// when we are dealing with strict-equality we don't as the child could still
						// be dirtied see #3883
						c.props = newProps;
						c.state = c._nextState;
						c._bits &= ~COMPONENT_DIRTY;
					}

					newVNode._dom = oldVNode._dom;
					newVNode._children = oldVNode._children;
					newVNode._children.some(vnode => {
						if (vnode) vnode._parent = newVNode;
					});

					EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
					c._stateCallbacks = [];

					if (c._renderCallbacks.length) {
						commitQueue.push(c);
					}

					// Skip over the retained subtree without traversing it; the
					// `result` branch in diffChildren picks this up as the next
					// oldDom.
					oldDom = getDomSibling(oldVNode);

					break outer;
				}

				if (c.componentWillUpdate) {
					c.componentWillUpdate(newProps, c._nextState, componentContext);
				}

				if (isClassComponent && c.componentDidUpdate) {
					c._renderCallbacks.push(() => {
						c.componentDidUpdate(oldProps, oldState, snapshot);
					});
				}
			}

			c.context = componentContext;
			c.props = newProps;
			c._parentDom = parentDom;
			c._bits &= ~COMPONENT_FORCE;

			let renderHook = options._render,
				count = 0;
			if (isClassComponent) {
				c.state = c._nextState;
				c._bits &= ~COMPONENT_DIRTY;

				if (renderHook) renderHook(newVNode);

				tmp = c.render(c.props, c.state, c.context);

				EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
				c._stateCallbacks = [];
			} else {
				do {
					c._bits &= ~COMPONENT_DIRTY;
					if (renderHook) renderHook(newVNode);

					tmp = c.render(c.props, c.state, c.context);

					// Handle setState called in render, see #2553
					c.state = c._nextState;
				} while (c._bits & COMPONENT_DIRTY && ++count < 25);
			}

			// Handle setState called in render, see #2553
			c.state = c._nextState;

			if (c.getChildContext) {
				globalContext = assign({}, globalContext, c.getChildContext());
			}

			if (
				isClassComponent &&
				oldVNode._component &&
				c.getSnapshotBeforeUpdate
			) {
				snapshot = c.getSnapshotBeforeUpdate(oldProps, oldState);
			}

			const renderResult =
				tmp && tmp.type === Fragment && tmp.key == NULL
					? tmp.props.children
					: tmp;

			// A vnode carrying a `_parentDom` prop, considered a new root,
			// continues rendering into that container. The subtree must stay
			// invisible to the host tree's DOM bookkeeping: the portal vnode
			// keeps a `null` `_dom` and the host insertion cursor (`oldDom`)
			// passes through unchanged.
			// `tmp` (the raw render result, already unwrapped into renderResult)
			// doubles as the saved host insertion cursor while we render into
			// the portal's container.
			if (newProps._parentDom) {
				tmp = oldDom;
				parentDom = newProps._parentDom;
				// If we portal into a math or svg element we need
				// to swap the namespace (chart libraries often do this).
				// The document follows the container too (e.g. iframes) as
				// diffElementNodes derives it from its parentDom.
				namespace = parentDom.namespaceURI;
				// Portals are never server-rendered: hydration must not claim the
				// host parent's excess nodes for the container's children.
				isHydrating = excessDomChildren = NULL;

				// Changing the container remounts the children into the new one
				if (oldVNode.props && oldVNode.props._parentDom != parentDom) {
					/** @type {VNode[]} */ (oldVNode._children).some(child => {
						if (child) unmount(child, child);
					});
					oldVNode._children = NULL;
				}

				oldDom = oldVNode._children ? getDomSibling(oldVNode, 0) : NULL;
			}

			oldDom = diffChildren(
				parentDom,
				isArray(renderResult) ? renderResult : [renderResult],
				newVNode,
				oldVNode,
				globalContext,
				namespace,
				excessDomChildren,
				commitQueue,
				oldDom,
				isHydrating,
				refQueue
			);

			// When we exit a portal we
			// change up the oldDom
			if (newProps._parentDom) {
				newVNode._dom = NULL;
				oldDom = tmp;
			}

			// We successfully rendered this VNode, unset any stored hydration/bailout state:
			newVNode._flags &= RESET_MODE;
			if (oldVNode._flags & MODE_SUSPENDED) c._excess = NULL;

			// Remove the kept DOM this resumed render didn't claim
			if (resumed) resumed.some(removeNode);

			if (c._renderCallbacks.length) {
				commitQueue.push(c);
			}

			// Only clear when this render was the retry; PENDING_ERROR set by a
			// descendant during this render must survive until then.
			if (c._bits & COMPONENT_PROCESSING_EXCEPTION) {
				c._bits &= ~(COMPONENT_PROCESSING_EXCEPTION | COMPONENT_PENDING_ERROR);
			}
		} catch (e) {
			// We remove any componentDidMount, ...
			// that have been invalidated by us
			// intercepting the error.
			commitQueue.length = oldCommitQueueLength;
			newVNode._original = NULL;
			// if hydrating or creating initial tree, bailout preserves DOM:
			if (isHydrating || excessDomChildren) {
				if (e.then) {
					let commentMarkersToFind = 0,
						startMarker;

					newVNode._flags |= isHydrating
						? MODE_HYDRATE | MODE_SUSPENDED
						: MODE_SUSPENDED;

					if (excessDomChildren) {
						let i = excessDomChildren.indexOf(oldDom || UNDEFINED),
							child;
						if (!~i) i = excessDomChildren.length;

						// The cursor skips comments: step back to this component's markers.
						while ((child = excessDomChildren[i - 1]) && child.nodeType == 8) {
							i--;
						}

						for (; i < excessDomChildren.length; i++) {
							child = excessDomChildren[i];
							if (!child) continue;
							excessDomChildren[i] = NULL;

							if (child.nodeType == 8) {
								if (child.data.startsWith('$s')) {
									if (!commentMarkersToFind++) startMarker = child;
								} else if (
									commentMarkersToFind &&
									child.data.startsWith('/$s') &&
									!--commentMarkersToFind
								) {
									oldDom = child;
									break;
								}
							} else if (!commentMarkersToFind) {
								break;
							}
						}
					}

					if (!startMarker) {
						while (oldDom && oldDom.nodeType == 8 && oldDom.nextSibling) {
							oldDom = oldDom.nextSibling;
						}
						startMarker = oldDom;
					}
					// Store the start marker directly; children re-scanned on resume.
					// A re-suspension keeps the marker it originally started from.
					if (!newVNode._component._excess) {
						newVNode._component._excess = startMarker;
					}
					newVNode._dom = oldDom;
				} else if (excessDomChildren) {
					excessDomChildren.some(removeNode);
				}
			} else {
				newVNode._dom = oldVNode._dom;
			}

			if (!newVNode._children) {
				newVNode._children = oldVNode._children || [];
			}

			if (!e.then) markAsForce(newVNode);
			options._catchError(e, newVNode, oldVNode);
		}
	} else {
		oldDom = newVNode._dom = diffElementNodes(
			oldVNode._dom,
			newVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			isHydrating,
			refQueue,
			parentDom
		);
	}

	if ((tmp = options.diffed)) tmp(newVNode);

	return newVNode._flags & MODE_SUSPENDED ? UNDEFINED : oldDom;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	/** @type {any} */
	let tmp,
		resumed,
		newType = newVNode.type;

	// When passing through createElement it assigns the object
	// constructor as undefined. This to prevent JSON-injection.
	if (newVNode.constructor !== UNDEFINED) return NULL;

	// If the previous diff bailed out, resume creating/hydrating into the DOM
	// that was kept while suspended (server-rendered, or already in the
	// container we rendered into). `tmp` holds the stored excess node until the
	// options._diff call below.
	if (
		oldVNode._flags & MODE_SUSPENDED &&
		// @ts-expect-error This is MODE_HYDRATE or 0
		((isHydrating = oldVNode._flags & MODE_HYDRATE),
		(tmp = oldVNode._component._excess))
	) {
		newVNode._flags |= isHydrating;
		resumed = excessDomChildren = [];
		if (tmp.nodeType == 8) {
			// Re-scan DOM from stored start marker for streamed hydration.
			// `depth` only ever reaches 0 through the `break` below, so it
			// doesn't need to be re-tested in the loop condition.
			for (
				let depth = 1, node = tmp.nextSibling;
				node;
				node = node.nextSibling
			) {
				if (node.nodeType == 8) {
					if (node.data.startsWith('$s')) depth++;
					else if (node.data.startsWith('/$s') && !--depth) break;
				}
				excessDomChildren.push(node);
			}
		} else {
			excessDomChildren.push(tmp);
		}
		oldDom = excessDomChildren[0];
	}

	if ((tmp = options._diff)) tmp(newVNode);

	outer: if (typeof newType == 'function') {
		let oldCommitQueueLength = commitQueue.length;
		try {
			let c,
				oldProps,
				oldState,
				snapshot,
				newProps = newVNode.props;
			const isClassComponent = (tmp = newType.prototype) && tmp.render;

			// Necessary for createContext api. Setting this property will pass
			// the context value as `this.context` just for this component.
			tmp = newType.contextType;
			const provider = tmp && globalContext[tmp._id];
			const componentContext = tmp
				? provider
					? provider.props.value
					: tmp._defaultValue
				: globalContext;

			// Get component and set it to `c`
			if ((c = oldVNode._component)) {
				newVNode._component = c;
				if (c._bits & COMPONENT_PENDING_ERROR) {
					c._bits |= COMPONENT_PROCESSING_EXCEPTION;
				}
			} else {
				// Instantiate the new component
				if (isClassComponent) {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new newType(newProps, componentContext); // eslint-disable-line new-cap
				} else {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new BaseComponent(
						newProps,
						componentContext
					);

					c.constructor = newType;
					c.render = doRender;
				}
				if (provider) provider.sub(c);

				if (!c.state) c.state = {};
				c._globalContext = globalContext;
				c._bits |= COMPONENT_DIRTY;
				c._renderCallbacks = [];
				c._stateCallbacks = [];
			}

			if (isClassComponent) {
				if (!c._nextState) c._nextState = c.state;

				// Invoke getDerivedStateFromProps
				if (newType.getDerivedStateFromProps) {
					if (c._nextState == c.state) {
						c._nextState = assign({}, c._nextState);
					}

					assign(
						c._nextState,
						newType.getDerivedStateFromProps(newProps, c._nextState)
					);
				}
			}

			oldProps = c.props;
			oldState = c.state;
			c._vnode = newVNode;

			// Invoke pre-render lifecycle methods
			if (!oldVNode._component) {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					c.componentWillMount
				) {
					c.componentWillMount();
				}

				if (isClassComponent && c.componentDidMount) {
					c._renderCallbacks.push(c.componentDidMount);
				}
			} else {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					newProps !== oldProps &&
					c.componentWillReceiveProps
				) {
					c.componentWillReceiveProps(newProps, componentContext);
				}

				if (
					(newVNode._original == oldVNode._original &&
						!(c._bits & COMPONENT_DIRTY)) ||
					(!(c._bits & COMPONENT_FORCE) &&
						c.shouldComponentUpdate &&
						c.shouldComponentUpdate(
							newProps,
							c._nextState,
							componentContext
						) === false)
				) {
					// More info about this here: https://gist.github.com/JoviDeCroock/bec5f2ce93544d2e6070ef8e0036e4e8
					if (newVNode._original != oldVNode._original) {
						// When we are dealing with a bail because of sCU we have to update
						// the props, state and dirty-state.
						// when we are dealing with strict-equality we don't as the child could still
						// be dirtied see #3883
						c.props = newProps;
						c.state = c._nextState;
						c._bits &= ~COMPONENT_DIRTY;
					}

					newVNode._dom = oldVNode._dom;
					newVNode._children = oldVNode._children;
					newVNode._children.some(vnode => {
						if (vnode) vnode._parent = newVNode;
					});

					EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
					c._stateCallbacks = [];

					if (c._renderCallbacks.length) {
						commitQueue.push(c);
					}

					// Skip over the retained subtree without traversing it; the
					// `result` branch in diffChildren picks this up as the next
					// oldDom.
					oldDom = getDomSibling(oldVNode);

					break outer;
				}

				if (c.componentWillUpdate) {
					c.componentWillUpdate(newProps, c._nextState, componentContext);
				}

				if (isClassComponent && c.componentDidUpdate) {
					c._renderCallbacks.push(() => {
						c.componentDidUpdate(oldProps, oldState, snapshot);
					});
				}
			}

			c.context = componentContext;
			c.props = newProps;
			c._parentDom = parentDom;
			c._bits &= ~COMPONENT_FORCE;

			let renderHook = options._render,
				count = 0;
			if (isClassComponent) {
				c.state = c._nextState;
				c._bits &= ~COMPONENT_DIRTY;

				if (renderHook) renderHook(newVNode);

				tmp = c.render(c.props, c.state, c.context);

				EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
				c._stateCallbacks = [];
			} else {
				do {
					c._bits &= ~COMPONENT_DIRTY;
					if (renderHook) renderHook(newVNode);

					tmp = c.render(c.props, c.state, c.context);

					// Handle setState called in render, see #2553
					c.state = c._nextState;
				} while (c._bits & COMPONENT_DIRTY && ++count < 25);
			}

			// Handle setState called in render, see #2553
			c.state = c._nextState;

			if (c.getChildContext) {
				globalContext = assign({}, globalContext, c.getChildContext());
			}

			if (
				isClassComponent &&
				oldVNode._component &&
				c.getSnapshotBeforeUpdate
			) {
				snapshot = c.getSnapshotBeforeUpdate(oldProps, oldState);
			}

			const renderResult =
				tmp && tmp.type === Fragment && tmp.key == NULL
					? tmp.props.children
					: tmp;

			// A vnode carrying a `_parentDom` prop, considered a new root,
			// continues rendering into that container. The subtree must stay
			// invisible to the host tree's DOM bookkeeping: the portal vnode
			// keeps a `null` `_dom` and the host insertion cursor (`oldDom`)
			// passes through unchanged.
			// `tmp` (the raw render result, already unwrapped into renderResult)
			// doubles as the saved host insertion cursor while we render into
			// the portal's container.
			if (newProps._parentDom) {
				tmp = oldDom;
				parentDom = newProps._parentDom;
				// If we portal into a math or svg element we need
				// to swap the namespace (chart libraries often do this).
				// The document follows the container too (e.g. iframes) as
				// diffElementNodes derives it from its parentDom.
				namespace = parentDom.namespaceURI;
				// Portals are never server-rendered: hydration must not claim the
				// host parent's excess nodes for the container's children.
				isHydrating = excessDomChildren = NULL;

				// Changing the container remounts the children into the new one
				if (oldVNode.props && oldVNode.props._parentDom != parentDom) {
					/** @type {VNode[]} */ (oldVNode._children).some(child => {
						if (child) unmount(child, child);
					});
					oldVNode._children = NULL;
				}

				oldDom = oldVNode._children ? getDomSibling(oldVNode, 0) : NULL;
			}

			oldDom = diffChildren(
				parentDom,
				isArray(renderResult) ? renderResult : [renderResult],
				newVNode,
				oldVNode,
				globalContext,
				namespace,
				excessDomChildren,
				commitQueue,
				oldDom,
				isHydrating,
				refQueue
			);

			// When we exit a portal we
			// change up the oldDom
			if (newProps._parentDom) {
				newVNode._dom = NULL;
				oldDom = tmp;
			}

			// We successfully rendered this VNode, unset any stored hydration/bailout state:
			newVNode._flags &= RESET_MODE;
			if (oldVNode._flags & MODE_SUSPENDED) c._excess = NULL;

			// Remove the kept DOM this resumed render didn't claim
			if (resumed) resumed.some(removeNode);

			if (c._renderCallbacks.length) {
				commitQueue.push(c);
			}

			// Only clear when this render was the retry; PENDING_ERROR set by a
			// descendant during this render must survive until then.
			if (c._bits & COMPONENT_PROCESSING_EXCEPTION) {
				c._bits &= ~(COMPONENT_PROCESSING_EXCEPTION | COMPONENT_PENDING_ERROR);
			}
		} catch (e) {
			// We remove any componentDidMount, ...
			// that have been invalidated by us
			// intercepting the error.
			commitQueue.length = oldCommitQueueLength;
			newVNode._original = NULL;
			// if hydrating or creating initial tree, bailout preserves DOM:
			if (isHydrating || excessDomChildren) {
				if (e.then) {
					let commentMarkersToFind = 0,
						startMarker;

					newVNode._flags |= isHydrating
						? MODE_HYDRATE | MODE_SUSPENDED
						: MODE_SUSPENDED;

					if (excessDomChildren) {
						let i = excessDomChildren.indexOf(oldDom || UNDEFINED),
							child;
						if (!~i) i = excessDomChildren.length;

						// The cursor skips comments: step back to this component's markers.
						while ((child = excessDomChildren[i - 1]) && child.nodeType == 8) {
							i--;
						}

						for (; i < excessDomChildren.length; i++) {
							child = excessDomChildren[i];
							if (!child) continue;
							excessDomChildren[i] = NULL;

							if (child.nodeType == 8) {
								if (child.data.startsWith('$s')) {
									if (!commentMarkersToFind++) startMarker = child;
								} else if (
									commentMarkersToFind &&
									child.data.startsWith('/$s') &&
									!--commentMarkersToFind
								) {
									oldDom = child;
									break;
								}
							} else if (!commentMarkersToFind) {
								break;
							}
						}
					}

					if (!startMarker) {
						while (oldDom && oldDom.nodeType == 8 && oldDom.nextSibling) {
							oldDom = oldDom.nextSibling;
						}
						startMarker = oldDom;
					}
					// Store the start marker directly; children re-scanned on resume.
					// A re-suspension keeps the marker it originally started from.
					if (!newVNode._component._excess) {
						newVNode._component._excess = startMarker;
					}
					newVNode._dom = oldDom;
				} else if (excessDomChildren) {
					excessDomChildren.some(removeNode);
				}
			} else {
				newVNode._dom = oldVNode._dom;
			}

			if (!newVNode._children) {
				newVNode._children = oldVNode._children || [];
			}

			if (!e.then) markAsForce(newVNode);
			options._catchError(e, newVNode, oldVNode);
		}
	} else {
		oldDom = newVNode._dom = diffElementNodes(
			oldVNode._dom,
			newVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			isHydrating,
			refQueue,
			parentDom
		);
	}

	if ((tmp = options.diffed)) tmp(newVNode);

	return newVNode._flags & MODE_SUSPENDED ? UNDEFINED : oldDom;
}
```


#### 📄 檔案: `src/diff/props.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:12, E:5, A:1) ➔ After(N:12, E:5, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#dom** `(Control)`
    └── ⚡ **on('name')**
        └── 🎯 [TRIGGERS] `proxy (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `setProperty()`
- **變更前簽章 (Before)**: `function setProperty(dom, name, value, oldValue, namespace)` (L41~L142)
- **變更後簽章 (After)**: `function setProperty(dom, name, value, oldValue, namespace)` (L41~L141)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function setProperty(dom, name, value, oldValue, namespace) {
	let useCapture;

	o: if (name == 'style') {
		if (typeof value == 'string') {
			dom.style.cssText = value;
		} else {
			if (typeof oldValue == 'string') {
				dom.style.cssText = oldValue = '';
			}

			if (oldValue) {
				for (name in oldValue) {
					if (!(value && name in value)) {
						setStyle(dom.style, name, '');
					}
				}
			}

			if (value) {
				for (name in value) {
					if (!oldValue || value[name] != oldValue[name]) {
						setStyle(dom.style, name, value[name]);
					}
				}
			}
		}
	}
	// Benchmark for comparison: https://esbench.com/bench/574c954bdb965b9a00965ac6
	else if (name[0] == 'o' && name[1] == 'n') {
		// Handlers are keyed by prop name and every prop name gets its own proxy,
		// so swapping one (e.g. an inline arrow function on every render) is a
		// single store. The event name is only derived to attach or remove it.
		(dom._listeners || (dom._listeners = {}))[name] = value;

		if (!value || !oldValue) {
			const proxy =
				eventProxies[name] || (eventProxies[name] = createEventProxy(name));
			// The attach time belongs to the listener, not to the handler: one
			// function can back several listeners that were attached at different
			// times. It lives outside `_listeners`, which unmount resets even when
			// a re-suspended Suspense boundary keeps the DOM and its listeners.
			(dom._attached || (dom._attached = {}))[name] = eventClock;
			useCapture = name != (name = name.replace(CAPTURE_REGEX, '$1'));

			// Infer correct casing for DOM built-in events: `onClick` -> `click`.
			// Only names starting with an uppercase letter are lowercased, so
			// camelCase custom events keep their casing: `onionChange` -> `ionChange`.
			name = name.slice(2);
			if (name[0] < 'a') name = name.toLowerCase();

			if (value) {
				dom.addEventListener(name, proxy, useCapture);
			} else {
				dom.removeEventListener(name, proxy, useCapture);
			}
		}
	} else {
		if (namespace == SVG_NAMESPACE) {
			// Normalize incorrect prop usage for SVG:
			// - xlink:href / xlinkHref --> href (xlink:href was removed from SVG and isn't needed)
			// - className --> class
			name = name.replace(/xlink(H|:h)/, 'h').replace(/sName$/, 's');
		} else if (
			name != 'width' &&
			name != 'height' &&
			name != 'href' &&
			name != 'list' &&
			name != 'form' &&
			// Default value in browsers is `-1` and an empty string is
			// cast to `0` instead
			name != 'tabIndex' &&
			name != 'download' &&
			name != 'rowSpan' &&
			name != 'colSpan' &&
			name != 'role' &&
			name != 'popover' &&
			name in dom
		) {
			try {
				dom[name] = value == NULL ? '' : value;
				// labelled break is 1b smaller here than a return statement (sorry)
				break o;
			} catch (e) {}
		}

		// aria- and data- attributes have no boolean representation.
		// A `false` value is different from the attribute not being
		// present, so we can't remove it. For non-boolean aria
		// attributes we could treat false as a removal, but the
		// amount of exceptions would cost too many bytes. On top of
		// that other frameworks generally stringify `false`.

		if (typeof value == 'function') {
			// never serialize functions as attribute values
		} else if (value != NULL && (value !== false || name[4] == '-')) {
			dom.setAttribute(name, name == 'popover' && value == true ? '' : value);
		} else {
			dom.removeAttribute(name);
		}
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function setProperty(dom, name, value, oldValue, namespace) {
	let useCapture;

	if (name == 'style') {
		if (typeof value == 'string') {
			dom.style.cssText = value;
		} else {
			if (typeof oldValue == 'string') {
				dom.style.cssText = oldValue = '';
			}

			if (oldValue) {
				for (name in oldValue) {
					if (!(value && name in value)) {
						setStyle(dom.style, name, '');
					}
				}
			}

			if (value) {
				for (name in value) {
					if (!oldValue || value[name] != oldValue[name]) {
						setStyle(dom.style, name, value[name]);
					}
				}
			}
		}
	}
	// Benchmark for comparison: https://esbench.com/bench/574c954bdb965b9a00965ac6
	else if (name[0] == 'o' && name[1] == 'n') {
		// Handlers are keyed by prop name and every prop name gets its own proxy,
		// so swapping one (e.g. an inline arrow function on every render) is a
		// single store. The event name is only derived to attach or remove it.
		(dom._listeners || (dom._listeners = {}))[name] = value;

		if (!value || !oldValue) {
			const proxy =
				eventProxies[name] || (eventProxies[name] = createEventProxy(name));
			// The attach time belongs to the listener, not to the handler: one
			// function can back several listeners that were attached at different
			// times. It lives outside `_listeners`, which unmount resets even when
			// a re-suspended Suspense boundary keeps the DOM and its listeners.
			(dom._attached || (dom._attached = {}))[name] = eventClock;
			useCapture = name != (name = name.replace(CAPTURE_REGEX, '$1'));

			// Infer correct casing for DOM built-in events: `onClick` -> `click`.
			// Only names starting with an uppercase letter are lowercased, so
			// camelCase custom events keep their casing: `onionChange` -> `ionChange`.
			name = name.slice(2);
			if (name[0] < 'a') name = name.toLowerCase();

			if (value) {
				dom.addEventListener(name, proxy, useCapture);
			} else {
				dom.removeEventListener(name, proxy, useCapture);
			}
		}
	} else {
		if (namespace == SVG_NAMESPACE) {
			// Normalize incorrect prop usage for SVG:
			// - xlink:href / xlinkHref --> href (xlink:href was removed from SVG and isn't needed)
			// - className --> class
			name = name.replace(/xlink(H|:h)/, 'h').replace(/sName$/, 's');
		} else if (
			name != 'width' &&
			name != 'height' &&
			name != 'href' &&
			name != 'list' &&
			name != 'form' &&
			// Default value in browsers is `-1` and an empty string is
			// cast to `0` instead
			name != 'tabIndex' &&
			name != 'download' &&
			name != 'rowSpan' &&
			name != 'colSpan' &&
			name != 'role' &&
			name != 'popover' &&
			name in dom
		) {
			try {
				dom[name] = value == NULL ? '' : value;
				return;
			} catch (e) {}
		}

		// aria- and data- attributes have no boolean representation.
		// A `false` value is different from the attribute not being
		// present, so we can't remove it. For non-boolean aria
		// attributes we could treat false as a removal, but the
		// amount of exceptions would cost too many bytes. On top of
		// that other frameworks generally stringify `false`.

		// Never serialize functions as attribute values.
		if (typeof value == 'function') return;
		if (value != NULL && (value !== false || name[4] == '-')) {
			dom.setAttribute(name, name == 'popover' && value == true ? '' : value);
		} else {
			dom.removeAttribute(name);
		}
	}
}
```


---


---

### 🔹 Commit #02: `28ef4dcb`
- **完整 Hash**: `28ef4dcbe04d8322f46803a76071151512a4c705`
- **說明 (Ground Truth)**: fix: Correct file extension on compat/server.browser
- **變更檔案數**: 2

#### 📄 檔案: `compat/server.browser.js`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:0, E:0, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `compat/server.browser.mjs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:0, E:0, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---


---

### 🔹 Commit #03: `67a88d56`
- **完整 Hash**: `67a88d56c02a073dd86e5f8c7b1ad3d44d501e86`
- **說明 (Ground Truth)**: Keep suspended hydration within a component's own `$s` range
- **變更檔案數**: 2

#### 📄 檔案: `src/diff/children.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:12, E:14, A:0) ➔ After(N:12, E:14, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `insert()`
- **變更前簽章 (Before)**: `function insert(parentVNode, oldDom, parentDom, isMounting)` (L384~L428)
- **變更後簽章 (After)**: `function insert(parentVNode, oldDom, parentDom, isMounting)` (L384~L433)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function insert(parentVNode, oldDom, parentDom, isMounting) {
	// Note: VNodes in nested suspended trees may be missing _children.
	if (typeof parentVNode.type == 'function') {
		// Root children live in another container, they never move with the
		// host tree and contribute nothing to the host insertion cursor.
		if (parentVNode.props._parentDom) return oldDom;
		let children = parentVNode._children;
		if (children) {
			for (let i = 0; i < children.length; i++) {
				if (children[i]) {
					// If we enter this code path on sCU bailout, where we copy
					// oldVNode._children to newVNode._children, we need to update the old
					// children's _parent pointer to point to the newVNode (parentVNode
					// here).
					children[i]._parent = parentVNode;
					oldDom = insert(children[i], oldDom, parentDom, false);
				}
			}
		}

		return oldDom;
	} else {
		// A cursor a parked Suspense subtree detached can't be a reference node:
		// retry from the vnode tree, then give up and append.
		if (oldDom && !oldDom.parentNode) {
			oldDom = getDomSibling(parentVNode);
			if (oldDom && !oldDom.parentNode) oldDom = NULL;
		}

		if (parentVNode._dom != oldDom) {
			// Containers that aren't DOM nodes may not implement moveBefore()
			if (!isMounting && parentDom.moveBefore && parentVNode._dom.parentNode) {
				// @ts-expect-error This isn't added to TypeScript lib.d.ts yet
				parentDom.moveBefore(parentVNode._dom, oldDom);
			} else {
				parentDom.insertBefore(parentVNode._dom, oldDom || NULL);
			}
		}
		oldDom = parentVNode._dom;
	}

	while ((oldDom = oldDom && oldDom.nextSibling) && oldDom.nodeType == 8);

	return oldDom;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function insert(parentVNode, oldDom, parentDom, isMounting) {
	// Note: VNodes in nested suspended trees may be missing _children.
	if (typeof parentVNode.type == 'function') {
		// Root children live in another container, they never move with the
		// host tree and contribute nothing to the host insertion cursor.
		if (parentVNode.props._parentDom) return oldDom;
		let children = parentVNode._children;
		if (children) {
			for (let i = 0; i < children.length; i++) {
				if (children[i]) {
					// If we enter this code path on sCU bailout, where we copy
					// oldVNode._children to newVNode._children, we need to update the old
					// children's _parent pointer to point to the newVNode (parentVNode
					// here).
					children[i]._parent = parentVNode;
					oldDom = insert(children[i], oldDom, parentDom, false);
				}
			}
		}

		return oldDom;
	} else {
		// A cursor a parked Suspense subtree detached can't be a reference node:
		// retry from the vnode tree, then give up and append.
		if (oldDom && !oldDom.parentNode) {
			oldDom = getDomSibling(parentVNode);
			if (oldDom && !oldDom.parentNode) oldDom = NULL;
		}

		// Comments (e.g. server `$s` markers) are never ours: a node right after
		// them is already in place.
		let next = oldDom;
		while (next && next.nodeType == 8) next = next.nextSibling;

		if (parentVNode._dom != next) {
			// Containers that aren't DOM nodes may not implement moveBefore()
			if (!isMounting && parentDom.moveBefore && parentVNode._dom.parentNode) {
				// @ts-expect-error This isn't added to TypeScript lib.d.ts yet
				parentDom.moveBefore(parentVNode._dom, oldDom);
			} else {
				parentDom.insertBefore(parentVNode._dom, oldDom || NULL);
			}
		}
		oldDom = parentVNode._dom;
	}

	while ((oldDom = oldDom && oldDom.nextSibling) && oldDom.nodeType == 8);

	return oldDom;
}
```


#### 📄 檔案: `src/diff/index.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:17, E:19, A:0) ➔ After(N:17, E:19, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `diff()`
- **變更前簽章 (Before)**: `function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L57~L463)
- **變更後簽章 (After)**: `function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L57~L469)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	/** @type {any} */
	let tmp,
		resumed,
		newType = newVNode.type;

	// When passing through createElement it assigns the object
	// constructor as undefined. This to prevent JSON-injection.
	if (newVNode.constructor !== UNDEFINED) return NULL;

	// If the previous diff bailed out, resume creating/hydrating into the DOM
	// that was kept while suspended (server-rendered, or already in the
	// container we rendered into). `tmp` holds the stored excess node until the
	// options._diff call below.
	if (
		oldVNode._flags & MODE_SUSPENDED &&
		// @ts-expect-error This is MODE_HYDRATE or 0
		((isHydrating = oldVNode._flags & MODE_HYDRATE),
		(tmp = oldVNode._component._excess))
	) {
		newVNode._flags |= isHydrating;
		resumed = excessDomChildren = [];
		if (tmp.nodeType == 8) {
			// Re-scan DOM from stored start marker for streamed hydration.
			// `depth` only ever reaches 0 through the `break` below, so it
			// doesn't need to be re-tested in the loop condition.
			for (
				let depth = 1, node = tmp.nextSibling;
				node;
				node = node.nextSibling
			) {
				if (node.nodeType == 8) {
					if (node.data.startsWith('$s')) depth++;
					else if (node.data.startsWith('/$s') && !--depth) break;
				}
				excessDomChildren.push(node);
			}
		} else {
			excessDomChildren.push(tmp);
		}
		oldDom = excessDomChildren[0];
	}

	if ((tmp = options._diff)) tmp(newVNode);

	outer: if (typeof newType == 'function') {
		let oldCommitQueueLength = commitQueue.length;
		try {
			let c,
				oldProps,
				oldState,
				snapshot,
				newProps = newVNode.props;
			const isClassComponent = (tmp = newType.prototype) && tmp.render;

			// Necessary for createContext api. Setting this property will pass
			// the context value as `this.context` just for this component.
			tmp = newType.contextType;
			const provider = tmp && globalContext[tmp._id];
			const componentContext = tmp
				? provider
					? provider.props.value
					: tmp._defaultValue
				: globalContext;

			// Get component and set it to `c`
			if (oldVNode._component) {
				c = newVNode._component = oldVNode._component;
				if (c._bits & COMPONENT_PENDING_ERROR) {
					c._bits |= COMPONENT_PROCESSING_EXCEPTION;
				}
			} else {
				// Instantiate the new component
				if (isClassComponent) {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new newType(newProps, componentContext); // eslint-disable-line new-cap
				} else {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new BaseComponent(
						newProps,
						componentContext
					);

					c.constructor = newType;
					c.render = doRender;
				}
				if (provider) provider.sub(c);

				if (!c.state) c.state = {};
				c._globalContext = globalContext;
				c._bits |= COMPONENT_DIRTY;
				c._renderCallbacks = [];
				c._stateCallbacks = [];
			}

			if (isClassComponent) {
				if (!c._nextState) c._nextState = c.state;

				// Invoke getDerivedStateFromProps
				if (newType.getDerivedStateFromProps) {
					if (c._nextState == c.state) {
						c._nextState = assign({}, c._nextState);
					}

					assign(
						c._nextState,
						newType.getDerivedStateFromProps(newProps, c._nextState)
					);
				}
			}

			oldProps = c.props;
			oldState = c.state;
			c._vnode = newVNode;

			// Invoke pre-render lifecycle methods
			if (!oldVNode._component) {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					c.componentWillMount
				) {
					c.componentWillMount();
				}

				if (isClassComponent && c.componentDidMount) {
					c._renderCallbacks.push(c.componentDidMount);
				}
			} else {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					newProps !== oldProps &&
					c.componentWillReceiveProps
				) {
					c.componentWillReceiveProps(newProps, componentContext);
				}

				if (
					(newVNode._original == oldVNode._original &&
						!(c._bits & COMPONENT_DIRTY)) ||
					(!(c._bits & COMPONENT_FORCE) &&
						c.shouldComponentUpdate &&
						c.shouldComponentUpdate(
							newProps,
							c._nextState,
							componentContext
						) === false)
				) {
					// More info about this here: https://gist.github.com/JoviDeCroock/bec5f2ce93544d2e6070ef8e0036e4e8
					if (newVNode._original != oldVNode._original) {
						// When we are dealing with a bail because of sCU we have to update
						// the props, state and dirty-state.
						// when we are dealing with strict-equality we don't as the child could still
						// be dirtied see #3883
						c.props = newProps;
						c.state = c._nextState;
						c._bits &= ~COMPONENT_DIRTY;
					}

					newVNode._dom = oldVNode._dom;
					newVNode._children = oldVNode._children;
					newVNode._children.some(vnode => {
						if (vnode) vnode._parent = newVNode;
					});

					EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
					c._stateCallbacks = [];

					if (c._renderCallbacks.length) {
						commitQueue.push(c);
					}

					// Skip over the retained subtree without traversing it; the
					// `result` branch in diffChildren picks this up as the next
					// oldDom.
					oldDom = getDomSibling(oldVNode);

					break outer;
				}

				if (c.componentWillUpdate) {
					c.componentWillUpdate(newProps, c._nextState, componentContext);
				}

				if (isClassComponent && c.componentDidUpdate) {
					c._renderCallbacks.push(() => {
						c.componentDidUpdate(oldProps, oldState, snapshot);
					});
				}
			}

			c.context = componentContext;
			c.props = newProps;
			c._parentDom = parentDom;
			c._bits &= ~COMPONENT_FORCE;

			let renderHook = options._render,
				count = 0;
			if (isClassComponent) {
				c.state = c._nextState;
				c._bits &= ~COMPONENT_DIRTY;

				if (renderHook) renderHook(newVNode);

				tmp = c.render(c.props, c.state, c.context);

				EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
				c._stateCallbacks = [];
			} else {
				do {
					c._bits &= ~COMPONENT_DIRTY;
					if (renderHook) renderHook(newVNode);

					tmp = c.render(c.props, c.state, c.context);

					// Handle setState called in render, see #2553
					c.state = c._nextState;
				} while (c._bits & COMPONENT_DIRTY && ++count < 25);
			}

			// Handle setState called in render, see #2553
			c.state = c._nextState;

			if (c.getChildContext) {
				globalContext = assign({}, globalContext, c.getChildContext());
			}

			if (
				isClassComponent &&
				oldVNode._component &&
				c.getSnapshotBeforeUpdate
			) {
				snapshot = c.getSnapshotBeforeUpdate(oldProps, oldState);
			}

			const renderResult =
				tmp && tmp.type === Fragment && tmp.key == NULL
					? tmp.props.children
					: tmp;

			// A vnode carrying a `_parentDom` prop, considered a new root,
			// continues rendering into that container. The subtree must stay
			// invisible to the host tree's DOM bookkeeping: the portal vnode
			// keeps a `null` `_dom` and the host insertion cursor (`oldDom`)
			// passes through unchanged.
			// `tmp` (the raw render result, already unwrapped into renderResult)
			// doubles as the saved host insertion cursor while we render into
			// the portal's container.
			if (newProps._parentDom) {
				tmp = oldDom;
				parentDom = newProps._parentDom;
				// If we portal into a math or svg element we need
				// to swap the namespace (chart libraries often do this).
				// The document follows the container too (e.g. iframes) as
				// diffElementNodes derives it from its parentDom.
				namespace = parentDom.namespaceURI;
				// Portals are never server-rendered: hydration must not claim the
				// host parent's excess nodes for the container's children.
				isHydrating = excessDomChildren = NULL;

				// Changing the container remounts the children into the new one
				if (oldVNode.props && oldVNode.props._parentDom != parentDom) {
					/** @type {VNode[]} */ (oldVNode._children).some(child => {
						if (child) unmount(child, child);
					});
					oldVNode._children = NULL;
				}

				oldDom = oldVNode._children ? getDomSibling(oldVNode, 0) : NULL;
			}

			oldDom = diffChildren(
				parentDom,
				isArray(renderResult) ? renderResult : [renderResult],
				newVNode,
				oldVNode,
				globalContext,
				namespace,
				excessDomChildren,
				commitQueue,
				oldDom,
				isHydrating,
				refQueue
			);

			// When we exit a portal we
			// change up the oldDom
			if (newProps._parentDom) {
				newVNode._dom = NULL;
				oldDom = tmp;
			}

			// We successfully rendered this VNode, unset any stored hydration/bailout state:
			newVNode._flags &= RESET_MODE;
			if (oldVNode._flags & MODE_SUSPENDED) c._excess = NULL;

			// Remove the kept DOM this resumed render didn't claim
			if (resumed) resumed.some(removeNode);

			if (c._renderCallbacks.length) {
				commitQueue.push(c);
			}

			// Only clear when this render was the retry; PENDING_ERROR set by a
			// descendant during this render must survive until then.
			if (c._bits & COMPONENT_PROCESSING_EXCEPTION) {
				c._bits &= ~(COMPONENT_PROCESSING_EXCEPTION | COMPONENT_PENDING_ERROR);
			}
		} catch (e) {
			// We remove any componentDidMount, ...
			// that have been invalidated by us
			// intercepting the error.
			commitQueue.length = oldCommitQueueLength;
			newVNode._original = NULL;
			// if hydrating or creating initial tree, bailout preserves DOM:
			if (isHydrating || excessDomChildren) {
				if (e.then) {
					let commentMarkersToFind = 0,
						startMarker;

					newVNode._flags |= isHydrating
						? MODE_HYDRATE | MODE_SUSPENDED
						: MODE_SUSPENDED;

					if (excessDomChildren) {
						for (let i = 0; i < excessDomChildren.length; i++) {
							let child = excessDomChildren[i];
							if (!child) continue;

							if (child.nodeType == 8) {
								excessDomChildren[i] = NULL;
								if (child.data.startsWith('$s')) {
									if (!commentMarkersToFind++) startMarker = child;
								} else if (
									child.data.startsWith('/$s') &&
									!--commentMarkersToFind
								) {
									oldDom = child;
									break;
								}
							} else if (commentMarkersToFind) {
								excessDomChildren[i] = NULL;
							}
						}
					}

					if (!startMarker) {
						while (oldDom && oldDom.nodeType == 8 && oldDom.nextSibling) {
							oldDom = oldDom.nextSibling;
						}

						if (excessDomChildren) {
							excessDomChildren[excessDomChildren.indexOf(oldDom)] = NULL;
						}
						startMarker = oldDom;
					}
					// Store the start marker directly; children re-scanned on resume.
					// A re-suspension keeps the marker it originally started from.
					if (!newVNode._component._excess) {
						newVNode._component._excess = startMarker;
					}
					newVNode._dom = oldDom;
				} else if (excessDomChildren) {
					excessDomChildren.some(removeNode);
				}
			} else {
				newVNode._dom = oldVNode._dom;
			}

			if (!newVNode._children) {
				newVNode._children = oldVNode._children || [];
			}

			if (!e.then) markAsForce(newVNode);
			options._catchError(e, newVNode, oldVNode);
		}
	} else {
		oldDom = newVNode._dom = diffElementNodes(
			oldVNode._dom,
			newVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			isHydrating,
			refQueue,
			parentDom
		);
	}

	if ((tmp = options.diffed)) tmp(newVNode);

	return newVNode._flags & MODE_SUSPENDED ? UNDEFINED : oldDom;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	/** @type {any} */
	let tmp,
		resumed,
		newType = newVNode.type;

	// When passing through createElement it assigns the object
	// constructor as undefined. This to prevent JSON-injection.
	if (newVNode.constructor !== UNDEFINED) return NULL;

	// If the previous diff bailed out, resume creating/hydrating into the DOM
	// that was kept while suspended (server-rendered, or already in the
	// container we rendered into). `tmp` holds the stored excess node until the
	// options._diff call below.
	if (
		oldVNode._flags & MODE_SUSPENDED &&
		// @ts-expect-error This is MODE_HYDRATE or 0
		((isHydrating = oldVNode._flags & MODE_HYDRATE),
		(tmp = oldVNode._component._excess))
	) {
		newVNode._flags |= isHydrating;
		resumed = excessDomChildren = [];
		if (tmp.nodeType == 8) {
			// Re-scan DOM from stored start marker for streamed hydration.
			// `depth` only ever reaches 0 through the `break` below, so it
			// doesn't need to be re-tested in the loop condition.
			for (
				let depth = 1, node = tmp.nextSibling;
				node;
				node = node.nextSibling
			) {
				if (node.nodeType == 8) {
					if (node.data.startsWith('$s')) depth++;
					else if (node.data.startsWith('/$s') && !--depth) break;
				}
				excessDomChildren.push(node);
			}
		} else {
			excessDomChildren.push(tmp);
		}
		oldDom = excessDomChildren[0];
	}

	if ((tmp = options._diff)) tmp(newVNode);

	outer: if (typeof newType == 'function') {
		let oldCommitQueueLength = commitQueue.length;
		try {
			let c,
				oldProps,
				oldState,
				snapshot,
				newProps = newVNode.props;
			const isClassComponent = (tmp = newType.prototype) && tmp.render;

			// Necessary for createContext api. Setting this property will pass
			// the context value as `this.context` just for this component.
			tmp = newType.contextType;
			const provider = tmp && globalContext[tmp._id];
			const componentContext = tmp
				? provider
					? provider.props.value
					: tmp._defaultValue
				: globalContext;

			// Get component and set it to `c`
			if (oldVNode._component) {
				c = newVNode._component = oldVNode._component;
				if (c._bits & COMPONENT_PENDING_ERROR) {
					c._bits |= COMPONENT_PROCESSING_EXCEPTION;
				}
			} else {
				// Instantiate the new component
				if (isClassComponent) {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new newType(newProps, componentContext); // eslint-disable-line new-cap
				} else {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new BaseComponent(
						newProps,
						componentContext
					);

					c.constructor = newType;
					c.render = doRender;
				}
				if (provider) provider.sub(c);

				if (!c.state) c.state = {};
				c._globalContext = globalContext;
				c._bits |= COMPONENT_DIRTY;
				c._renderCallbacks = [];
				c._stateCallbacks = [];
			}

			if (isClassComponent) {
				if (!c._nextState) c._nextState = c.state;

				// Invoke getDerivedStateFromProps
				if (newType.getDerivedStateFromProps) {
					if (c._nextState == c.state) {
						c._nextState = assign({}, c._nextState);
					}

					assign(
						c._nextState,
						newType.getDerivedStateFromProps(newProps, c._nextState)
					);
				}
			}

			oldProps = c.props;
			oldState = c.state;
			c._vnode = newVNode;

			// Invoke pre-render lifecycle methods
			if (!oldVNode._component) {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					c.componentWillMount
				) {
					c.componentWillMount();
				}

				if (isClassComponent && c.componentDidMount) {
					c._renderCallbacks.push(c.componentDidMount);
				}
			} else {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					newProps !== oldProps &&
					c.componentWillReceiveProps
				) {
					c.componentWillReceiveProps(newProps, componentContext);
				}

				if (
					(newVNode._original == oldVNode._original &&
						!(c._bits & COMPONENT_DIRTY)) ||
					(!(c._bits & COMPONENT_FORCE) &&
						c.shouldComponentUpdate &&
						c.shouldComponentUpdate(
							newProps,
							c._nextState,
							componentContext
						) === false)
				) {
					// More info about this here: https://gist.github.com/JoviDeCroock/bec5f2ce93544d2e6070ef8e0036e4e8
					if (newVNode._original != oldVNode._original) {
						// When we are dealing with a bail because of sCU we have to update
						// the props, state and dirty-state.
						// when we are dealing with strict-equality we don't as the child could still
						// be dirtied see #3883
						c.props = newProps;
						c.state = c._nextState;
						c._bits &= ~COMPONENT_DIRTY;
					}

					newVNode._dom = oldVNode._dom;
					newVNode._children = oldVNode._children;
					newVNode._children.some(vnode => {
						if (vnode) vnode._parent = newVNode;
					});

					EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
					c._stateCallbacks = [];

					if (c._renderCallbacks.length) {
						commitQueue.push(c);
					}

					// Skip over the retained subtree without traversing it; the
					// `result` branch in diffChildren picks this up as the next
					// oldDom.
					oldDom = getDomSibling(oldVNode);

					break outer;
				}

				if (c.componentWillUpdate) {
					c.componentWillUpdate(newProps, c._nextState, componentContext);
				}

				if (isClassComponent && c.componentDidUpdate) {
					c._renderCallbacks.push(() => {
						c.componentDidUpdate(oldProps, oldState, snapshot);
					});
				}
			}

			c.context = componentContext;
			c.props = newProps;
			c._parentDom = parentDom;
			c._bits &= ~COMPONENT_FORCE;

			let renderHook = options._render,
				count = 0;
			if (isClassComponent) {
				c.state = c._nextState;
				c._bits &= ~COMPONENT_DIRTY;

				if (renderHook) renderHook(newVNode);

				tmp = c.render(c.props, c.state, c.context);

				EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
				c._stateCallbacks = [];
			} else {
				do {
					c._bits &= ~COMPONENT_DIRTY;
					if (renderHook) renderHook(newVNode);

					tmp = c.render(c.props, c.state, c.context);

					// Handle setState called in render, see #2553
					c.state = c._nextState;
				} while (c._bits & COMPONENT_DIRTY && ++count < 25);
			}

			// Handle setState called in render, see #2553
			c.state = c._nextState;

			if (c.getChildContext) {
				globalContext = assign({}, globalContext, c.getChildContext());
			}

			if (
				isClassComponent &&
				oldVNode._component &&
				c.getSnapshotBeforeUpdate
			) {
				snapshot = c.getSnapshotBeforeUpdate(oldProps, oldState);
			}

			const renderResult =
				tmp && tmp.type === Fragment && tmp.key == NULL
					? tmp.props.children
					: tmp;

			// A vnode carrying a `_parentDom` prop, considered a new root,
			// continues rendering into that container. The subtree must stay
			// invisible to the host tree's DOM bookkeeping: the portal vnode
			// keeps a `null` `_dom` and the host insertion cursor (`oldDom`)
			// passes through unchanged.
			// `tmp` (the raw render result, already unwrapped into renderResult)
			// doubles as the saved host insertion cursor while we render into
			// the portal's container.
			if (newProps._parentDom) {
				tmp = oldDom;
				parentDom = newProps._parentDom;
				// If we portal into a math or svg element we need
				// to swap the namespace (chart libraries often do this).
				// The document follows the container too (e.g. iframes) as
				// diffElementNodes derives it from its parentDom.
				namespace = parentDom.namespaceURI;
				// Portals are never server-rendered: hydration must not claim the
				// host parent's excess nodes for the container's children.
				isHydrating = excessDomChildren = NULL;

				// Changing the container remounts the children into the new one
				if (oldVNode.props && oldVNode.props._parentDom != parentDom) {
					/** @type {VNode[]} */ (oldVNode._children).some(child => {
						if (child) unmount(child, child);
					});
					oldVNode._children = NULL;
				}

				oldDom = oldVNode._children ? getDomSibling(oldVNode, 0) : NULL;
			}

			oldDom = diffChildren(
				parentDom,
				isArray(renderResult) ? renderResult : [renderResult],
				newVNode,
				oldVNode,
				globalContext,
				namespace,
				excessDomChildren,
				commitQueue,
				oldDom,
				isHydrating,
				refQueue
			);

			// When we exit a portal we
			// change up the oldDom
			if (newProps._parentDom) {
				newVNode._dom = NULL;
				oldDom = tmp;
			}

			// We successfully rendered this VNode, unset any stored hydration/bailout state:
			newVNode._flags &= RESET_MODE;
			if (oldVNode._flags & MODE_SUSPENDED) c._excess = NULL;

			// Remove the kept DOM this resumed render didn't claim
			if (resumed) resumed.some(removeNode);

			if (c._renderCallbacks.length) {
				commitQueue.push(c);
			}

			// Only clear when this render was the retry; PENDING_ERROR set by a
			// descendant during this render must survive until then.
			if (c._bits & COMPONENT_PROCESSING_EXCEPTION) {
				c._bits &= ~(COMPONENT_PROCESSING_EXCEPTION | COMPONENT_PENDING_ERROR);
			}
		} catch (e) {
			// We remove any componentDidMount, ...
			// that have been invalidated by us
			// intercepting the error.
			commitQueue.length = oldCommitQueueLength;
			newVNode._original = NULL;
			// if hydrating or creating initial tree, bailout preserves DOM:
			if (isHydrating || excessDomChildren) {
				if (e.then) {
					let commentMarkersToFind = 0,
						startMarker;

					newVNode._flags |= isHydrating
						? MODE_HYDRATE | MODE_SUSPENDED
						: MODE_SUSPENDED;

					if (excessDomChildren) {
						let i = excessDomChildren.indexOf(oldDom || UNDEFINED),
							child;
						if (!~i) i = excessDomChildren.length;

						// The cursor skips comments: step back to this component's markers.
						while ((child = excessDomChildren[i - 1]) && child.nodeType == 8) {
							i--;
						}

						for (; i < excessDomChildren.length; i++) {
							child = excessDomChildren[i];
							if (!child) continue;
							excessDomChildren[i] = NULL;

							if (child.nodeType == 8) {
								if (child.data.startsWith('$s')) {
									if (!commentMarkersToFind++) startMarker = child;
								} else if (
									commentMarkersToFind &&
									child.data.startsWith('/$s') &&
									!--commentMarkersToFind
								) {
									oldDom = child;
									break;
								}
							} else if (!commentMarkersToFind) {
								break;
							}
						}
					}

					if (!startMarker) {
						while (oldDom && oldDom.nodeType == 8 && oldDom.nextSibling) {
							oldDom = oldDom.nextSibling;
						}
						startMarker = oldDom;
					}
					// Store the start marker directly; children re-scanned on resume.
					// A re-suspension keeps the marker it originally started from.
					if (!newVNode._component._excess) {
						newVNode._component._excess = startMarker;
					}
					newVNode._dom = oldDom;
				} else if (excessDomChildren) {
					excessDomChildren.some(removeNode);
				}
			} else {
				newVNode._dom = oldVNode._dom;
			}

			if (!newVNode._children) {
				newVNode._children = oldVNode._children || [];
			}

			if (!e.then) markAsForce(newVNode);
			options._catchError(e, newVNode, oldVNode);
		}
	} else {
		oldDom = newVNode._dom = diffElementNodes(
			oldVNode._dom,
			newVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			isHydrating,
			refQueue,
			parentDom
		);
	}

	if ((tmp = options.diffed)) tmp(newVNode);

	return newVNode._flags & MODE_SUSPENDED ? UNDEFINED : oldDom;
}
```


---


---





================================================================================

### 📁 代表專案 #4: `fastapi` (14)

> **生態與抽樣意圖**: 展示非同步路由與相依性注入架構下的 100% 捕獲證明 (Python)  

> **完整 20-Commit 報告位址**: `reports/per_repo_audits/14_fastapi.md`


# 🔬 CODE-Map 基準審查獨立驗證報告: `fastapi`
> **技術生態**: `Python (非同步 Web / 路由與依賴注入)`  
> **本地倉庫路徑**: `test_repos/fastapi`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 24 Files  
> **報告生成時間**: 2026-10-20 21:41:41  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `15` / `24` | `62.5%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `5` / `24` | `20.8%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `4` / `24` | `16.7%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`20` / `24`** | **`83.3%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `24` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

---

### 📋 精選代表性修復 Commit 形式化證據 (抽樣前 3 項 / 共 20 項)

### 🔹 Commit #01: `0890e2a3`
- **完整 Hash**: `0890e2a32960bb5cc1cfb807dca3a5e10384ec9d`
- **說明 (Ground Truth)**: 🐛 Treat unselected browser file inputs as missing (#16534)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/dependencies/utils.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:91, E:133, A:0) ➔ After(N:92, E:134, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `_is_empty_file_input` (FUNCTION_DEF)
  • + [新增呼叫邊] `_get_multidict_value` ──[CALLS]──> `_is_empty_file_input`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_get_multidict_value()`
- **變更前簽章 (Before)**: `def _get_multidict_value( field: ModelField, values: Mapping[str, Any], alias: str | None = None ) -> Any` (L750~L776)
- **變更後簽章 (After)**: `def _get_multidict_value( field: ModelField, values: Mapping[str, Any], alias: str | None = None ) -> Any` (L755~L784)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _get_multidict_value(
    field: ModelField, values: Mapping[str, Any], alias: str | None = None
) -> Any:
    alias = alias or get_validation_alias(field)
    if (
        (not _is_json_field(field))
        and field_annotation_is_sequence(field.field_info.annotation)
        and isinstance(values, (ImmutableMultiDict, Headers))
    ):
        value = values.getlist(alias)
    else:
        value = values.get(alias, None)
    if (
        value is None
        or (
            isinstance(values, FormData)
            and isinstance(value, str)  # For type checks
            and value == ""
        )
        or (
            field_annotation_is_sequence(field.field_info.annotation)
            and len(value) == 0
        )
    ):
        # Apply defaults during validation, not while extracting request data.
        return None
    return value
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _get_multidict_value(
    field: ModelField, values: Mapping[str, Any], alias: str | None = None
) -> Any:
    alias = alias or get_validation_alias(field)
    if (
        (not _is_json_field(field))
        and field_annotation_is_sequence(field.field_info.annotation)
        and isinstance(values, (ImmutableMultiDict, Headers))
    ):
        value = values.getlist(alias)
        if isinstance(values, FormData):
            value = [item for item in value if not _is_empty_file_input(item)]
    else:
        value = values.get(alias, None)
    if (
        value is None
        or (
            isinstance(values, FormData)
            and (
                (isinstance(value, str) and value == "") or _is_empty_file_input(value)
            )
        )
        or (
            field_annotation_is_sequence(field.field_info.annotation)
            and len(value) == 0
        )
    ):
        # Apply defaults during validation, not while extracting request data.
        return None
    return value
```


---


---

### 🔹 Commit #02: `f214cd34`
- **完整 Hash**: `f214cd34627aa7cff092cb1b7b8f40589e97252a`
- **說明 (Ground Truth)**: 🐛 Treat empty scalar values as missing in form models (#16529)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/dependencies/utils.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:93, E:133, A:0) ➔ After(N:91, E:133, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 2, +Edges: 2, -Edges: 2, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `next (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `all (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `_extract_form_body` ──[CALLS]──> `any (External/Unresolved)`
  • + [新增呼叫邊] `_extract_form_body` ──[CALLS]──> `list (External/Unresolved)`
  • - [移除呼叫邊] `_extract_form_body` ──[CALLS]──> `all (External/Unresolved)`
  • - [移除呼叫邊] `_extract_form_body` ──[CALLS]──> `next (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_extract_form_body()`
- **變更前簽章 (Before)**: `async def _extract_form_body( body_fields: list[ModelField], received_body: FormData, ) -> dict[str, Any]` (L911~L985)
- **變更後簽章 (After)**: `async def _extract_form_body( body_fields: list[ModelField], received_body: FormData, ) -> dict[str, Any]` (L911~L989)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def _extract_form_body(
    body_fields: list[ModelField],
    received_body: FormData,
) -> dict[str, Any]:
    values: dict[str, Any] = {}
    field_aliases: set[str] = set()

    for field in body_fields:
        alias = get_validation_alias(field)
        validation_alias = field.field_info.validation_alias
        # Interpret missing boolean form fields as unchecked HTML checkboxes.
        infer_false_if_missing = field.field_info.annotation in (
            bool,
            bool | None,
        ) and (
            validation_alias is None
            or isinstance(validation_alias, str)
            or (
                isinstance(validation_alias, AliasChoices)
                and all(isinstance(choice, str) for choice in validation_alias.choices)
            )
        )
        if infer_false_if_missing:
            if isinstance(validation_alias, AliasChoices):
                aliases = cast(list[str], validation_alias.choices)
                alias = next(
                    (name for name in aliases if name in received_body), aliases[0]
                )
            config = field.config or {}
            if config.get(
                "validate_by_name", config.get("populate_by_name", False)
            ) and (
                alias not in received_body or config.get("validate_by_alias") is False
            ):
                alias = field.name
        field_aliases.add(alias)
        if infer_false_if_missing and alias not in received_body:
            value: Any = False
        else:
            value = _get_multidict_value(field, received_body, alias=alias)
        field_info = field.field_info
        if (
            isinstance(field_info, params.File)
            and is_bytes_or_nonable_bytes_annotation(field.field_info.annotation)
            and isinstance(value, UploadFile)
        ):
            value = await value.read()
        elif (
            is_bytes_sequence_annotation(field.field_info.annotation)
            and isinstance(field_info, params.File)
            and value_is_sequence(value)
        ):
            # For types
            assert isinstance(value, sequence_types)
            results: list[bytes | str] = []
            for sub_value in value:
                if isinstance(sub_value, UploadFile):
                    results.append(await sub_value.read())
                else:
                    results.append(sub_value)
            value = serialize_sequence_value(field=field, value=results)
        if field.config is None:
            # Individual parameters are later looked up by their declared alias.
            alias = get_validation_alias(field)
            field_aliases.add(alias)
        if value is not None:
            values[alias] = value
    for key in received_body.keys():
        if key not in field_aliases:
            param_values = received_body.getlist(key)
            if len(param_values) == 1:
                values[key] = param_values[0]
            else:
                values[key] = param_values
    return values
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def _extract_form_body(
    body_fields: list[ModelField],
    received_body: FormData,
) -> dict[str, Any]:
    values: dict[str, Any] = {}
    field_aliases: set[str] = set()

    for field in body_fields:
        aliases = [get_validation_alias(field)]
        validation_alias = field.field_info.validation_alias
        has_alias_path = isinstance(validation_alias, AliasPath) or (
            isinstance(validation_alias, AliasChoices)
            and any(
                isinstance(choice, AliasPath) for choice in validation_alias.choices
            )
        )
        if not has_alias_path:
            if isinstance(validation_alias, AliasChoices):
                aliases = list(cast(list[str], validation_alias.choices))
            config = field.config or {}
            if config.get("validate_by_name", config.get("populate_by_name", False)):
                if config.get("validate_by_alias") is False:
                    aliases = [field.name]
                elif field.name not in aliases:
                    aliases.append(field.name)
        # Interpret missing boolean form fields as unchecked HTML checkboxes.
        infer_false_if_missing = (
            not has_alias_path
            and field.field_info.annotation in (bool, bool | None)
            and not any(alias in received_body for alias in aliases)
        )
        if field.config is None or infer_false_if_missing:
            selected_alias = aliases[0]
            for alias in aliases:
                if _get_multidict_value(field, received_body, alias=alias) is not None:
                    selected_alias = alias
                    break
            aliases = [selected_alias]
        for alias in aliases:
            field_aliases.add(alias)
            if infer_false_if_missing:
                value: Any = False
            else:
                value = _get_multidict_value(field, received_body, alias=alias)
            field_info = field.field_info
            if (
                isinstance(field_info, params.File)
                and is_bytes_or_nonable_bytes_annotation(field.field_info.annotation)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif (
                is_bytes_sequence_annotation(field.field_info.annotation)
                and isinstance(field_info, params.File)
                and value_is_sequence(value)
            ):
                # For types
                assert isinstance(value, sequence_types)
                results: list[bytes | str] = []
                for sub_value in value:
                    if isinstance(sub_value, UploadFile):
                        results.append(await sub_value.read())
                    else:
                        results.append(sub_value)
                value = serialize_sequence_value(field=field, value=results)
            if field.config is None:
                # Individual parameters are later looked up by their declared alias.
                alias = get_validation_alias(field)
                field_aliases.add(alias)
            if value is not None:
                values[alias] = value
    for key in received_body.keys():
        if key not in field_aliases:
            param_values = received_body.getlist(key)
            if len(param_values) == 1:
                values[key] = param_values[0]
            else:
                values[key] = param_values
    return values
```

### 🔹 函式: `_get_multidict_value()`
- **變更前簽章 (Before)**: `def _get_multidict_value( field: ModelField, values: Mapping[str, Any], alias: str | None = None ) -> Any` (L750~L776)
- **變更後簽章 (After)**: `def _get_multidict_value( field: ModelField, values: Mapping[str, Any], alias: str | None = None ) -> Any` (L750~L776)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _get_multidict_value(
    field: ModelField, values: Mapping[str, Any], alias: str | None = None
) -> Any:
    alias = alias or get_validation_alias(field)
    if (
        (not _is_json_field(field))
        and field_annotation_is_sequence(field.field_info.annotation)
        and isinstance(values, (ImmutableMultiDict, Headers))
    ):
        value = values.getlist(alias)
    else:
        value = values.get(alias, None)
    if (
        value is None
        or (
            isinstance(field.field_info, params.Form)
            and isinstance(value, str)  # For type checks
            and value == ""
        )
        or (
            field_annotation_is_sequence(field.field_info.annotation)
            and len(value) == 0
        )
    ):
        # Apply defaults during validation, not while extracting request data.
        return None
    return value
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _get_multidict_value(
    field: ModelField, values: Mapping[str, Any], alias: str | None = None
) -> Any:
    alias = alias or get_validation_alias(field)
    if (
        (not _is_json_field(field))
        and field_annotation_is_sequence(field.field_info.annotation)
        and isinstance(values, (ImmutableMultiDict, Headers))
    ):
        value = values.getlist(alias)
    else:
        value = values.get(alias, None)
    if (
        value is None
        or (
            isinstance(values, FormData)
            and isinstance(value, str)  # For type checks
            and value == ""
        )
        or (
            field_annotation_is_sequence(field.field_info.annotation)
            and len(value) == 0
        )
    ):
        # Apply defaults during validation, not while extracting request data.
        return None
    return value
```


---


---

### 🔹 Commit #03: `32240026`
- **完整 Hash**: `32240026ad8bdea0b78fd06ac607bba7e4d9da8a`
- **說明 (Ground Truth)**: 🐛 Fix default handling for request parameters and models (#16527)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/dependencies/utils.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:93, E:135, A:0) ➔ After(N:93, E:133, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 2, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除呼叫邊] `_get_multidict_value` ──[CALLS]──> `is_required (External/Unresolved)`
  • - [移除呼叫邊] `_get_multidict_value` ──[CALLS]──> `deepcopy (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_validate_value_with_model_field()`
- **變更前簽章 (Before)**: `def _validate_value_with_model_field( *, field: ModelField, value: Any, values: dict[str, Any], loc: tuple[str, ...] ) -> tuple[Any, list[Any]]` (L734~L742)
- **變更後簽章 (After)**: `def _validate_value_with_model_field( *, field: ModelField, value: Any, values: dict[str, Any], loc: tuple[str, ...] ) -> tuple[Any, list[Any]]` (L734~L743)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _validate_value_with_model_field(
    *, field: ModelField, value: Any, values: dict[str, Any], loc: tuple[str, ...]
) -> tuple[Any, list[Any]]:
    if value is None:
        if field.field_info.is_required():
            return None, [get_missing_field_error(loc=loc)]
        else:
            return deepcopy(field.default), []
    return field.validate(value, values, loc=loc)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _validate_value_with_model_field(
    *, field: ModelField, value: Any, values: dict[str, Any], loc: tuple[str, ...]
) -> tuple[Any, list[Any]]:
    if value is None:
        if field.field_info.is_required():
            return None, [get_missing_field_error(loc=loc)]
        value = deepcopy(field.default)
        if not field.field_info.validate_default:
            return value, []
    return field.validate(value, values, loc=loc)
```

### 🔹 函式: `_get_multidict_value()`
- **變更前簽章 (Before)**: `def _get_multidict_value( field: ModelField, values: Mapping[str, Any], alias: str | None = None ) -> Any` (L749~L777)
- **變更後簽章 (After)**: `def _get_multidict_value( field: ModelField, values: Mapping[str, Any], alias: str | None = None ) -> Any` (L750~L776)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _get_multidict_value(
    field: ModelField, values: Mapping[str, Any], alias: str | None = None
) -> Any:
    alias = alias or get_validation_alias(field)
    if (
        (not _is_json_field(field))
        and field_annotation_is_sequence(field.field_info.annotation)
        and isinstance(values, (ImmutableMultiDict, Headers))
    ):
        value = values.getlist(alias)
    else:
        value = values.get(alias, None)
    if (
        value is None
        or (
            isinstance(field.field_info, params.Form)
            and isinstance(value, str)  # For type checks
            and value == ""
        )
        or (
            field_annotation_is_sequence(field.field_info.annotation)
            and len(value) == 0
        )
    ):
        if field.field_info.is_required():
            return
        else:
            return deepcopy(field.default)
    return value
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _get_multidict_value(
    field: ModelField, values: Mapping[str, Any], alias: str | None = None
) -> Any:
    alias = alias or get_validation_alias(field)
    if (
        (not _is_json_field(field))
        and field_annotation_is_sequence(field.field_info.annotation)
        and isinstance(values, (ImmutableMultiDict, Headers))
    ):
        value = values.getlist(alias)
    else:
        value = values.get(alias, None)
    if (
        value is None
        or (
            isinstance(field.field_info, params.Form)
            and isinstance(value, str)  # For type checks
            and value == ""
        )
        or (
            field_annotation_is_sequence(field.field_info.annotation)
            and len(value) == 0
        )
    ):
        # Apply defaults during validation, not while extracting request data.
        return None
    return value
```


---


---





================================================================================

### 📁 代表專案 #5: `vllm` (29)

> **生態與抽樣意圖**: 展示高併發 LLM 推理串流與 PagedAttention 記憶體生命週期修復證明 (Python)  

> **完整 20-Commit 報告位址**: `reports/per_repo_audits/29_vllm.md`


# 🔬 CODE-Map 基準審查獨立驗證報告: `vllm`
> **技術生態**: `Python (LLM 推理串流 / PagedAttention)`  
> **本地倉庫路徑**: `test_repos/vllm`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 33 Files  
> **報告生成時間**: 2026-10-20 21:44:04  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `22` / `33` | `66.7%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `10` / `33` | `30.3%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `1` / `33` | `3.0%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`32` / `33`** | **`97.0%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `33` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

---

### 📋 精選代表性修復 Commit 形式化證據 (抽樣前 3 項 / 共 20 項)

### 🔹 Commit #01: `34ac4f96`
- **完整 Hash**: `34ac4f96a399836393894207dae296760b413715`
- **說明 (Ground Truth)**: [Bugfix][KV Connector][Mooncake] Wait for all peers before completing failed receives to avoid potential KV block write-after-free (#62282)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/distributed/kv_transfer/kv_connector/v1/mooncake/mooncake_connector.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:238, E:347, A:0) ➔ After(N:240, E:350, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 6, -Edges: 3, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `MooncakeConnectorWorker._complete_pull_task` (FUNCTION_DEF)
  • + [新增節點] `copy (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `MooncakeConnectorWorker.receive_kv_from_single_worker` ──[CALLS]──> `copy (External/Unresolved)`
  • + [新增呼叫邊] `MooncakeConnectorWorker.receive_kv_from_single_worker` ──[CALLS]──> `list (External/Unresolved)`
  • + [新增呼叫邊] `MooncakeConnectorWorker._handle_failed_recv` ──[CALLS]──> `MooncakeConnectorWorker._complete_pull_task`
  • + [新增呼叫邊] `MooncakeConnectorWorker._complete_pull_task` ──[CALLS]──> `any (External/Unresolved)`
  • + [新增呼叫邊] `MooncakeConnectorWorker._complete_pull_task` ──[CALLS]──> `add (External/Unresolved)`
  • + [新增呼叫邊] `MooncakeConnectorWorker.process_pulling_result` ──[CALLS]──> `MooncakeConnectorWorker._complete_pull_task`
  • - [移除呼叫邊] `MooncakeConnectorWorker._handle_failed_recv` ──[CALLS]──> `add (External/Unresolved)`
  • - [移除呼叫邊] `MooncakeConnectorWorker.process_pulling_result` ──[CALLS]──> `any (External/Unresolved)`
  • - [移除呼叫邊] `MooncakeConnectorWorker.process_pulling_result` ──[CALLS]──> `add (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `MooncakeConnectorWorker.process_pulling_result()`
- **變更前簽章 (Before)**: `def process_pulling_result( self, response: MooncakeXferResponse, pull_metas: dict[ReqId, PullReqMeta], )` (L2516~L2540)
- **變更後簽章 (After)**: `def process_pulling_result( self, response: MooncakeXferResponse, pull_metas: dict[ReqId, PullReqMeta], )` (L2535~L2552)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def process_pulling_result(
        self,
        response: MooncakeXferResponse,
        pull_metas: dict[ReqId, PullReqMeta],
    ):
        ok_reqs: list[ReqId] = response.ok_reqs or []

        for req_id in ok_reqs:
            pull_meta = pull_metas[req_id]
            if pull_meta.failed:
                continue
            # No race because we are in async loop.
            pull_meta.pull_tasks_count -= 1
            # Empty pulls only release the producer's blocks; the consumer
            # did not enter WAITING_FOR_REMOTE_KVS.
            if pull_meta.pull_tasks_count == 0 and any(pull_meta.local_block_ids):
                self.finished_recving_reqs.add(pull_meta.d_req_id)

        if ok_reqs:
            logger.debug("pulling kv_caches for %s finished", ok_reqs)

        if response.err_reqs:
            self._handle_failed_recv(
                pull_metas, response.err_reqs, response.err_msg or "unknown error"
            )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def process_pulling_result(
        self,
        response: MooncakeXferResponse,
        pull_metas: dict[ReqId, PullReqMeta],
    ):
        if response.err_reqs:
            self._handle_failed_recv(
                pull_metas, response.err_reqs, response.err_msg or "unknown error"
            )
        ok_reqs: list[ReqId] = response.ok_reqs or []

        for req_id in ok_reqs:
            pull_meta = pull_metas.pop(req_id, None)
            if pull_meta is not None:
                self._complete_pull_task(pull_meta)

        if ok_reqs:
            logger.debug("pulling kv_caches for %s finished", ok_reqs)
```

### 🔹 函式: `MooncakeConnectorWorker.receive_kv_from_single_worker()`
- **變更前簽章 (Before)**: `async def receive_kv_from_single_worker( self, worker_addr: str, pull_metas: dict[ReqId, PullReqMeta], )` (L2397~L2470)
- **變更後簽章 (After)**: `async def receive_kv_from_single_worker( self, worker_addr: str, pull_metas: dict[ReqId, PullReqMeta], ): # Each peer settles its own requests, sharing the per-request counters.` (L2397~L2478)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def receive_kv_from_single_worker(
        self,
        worker_addr: str,
        pull_metas: dict[ReqId, PullReqMeta],
    ):
        req_ids = set(pull_metas)
        include_layout = (
            not self._kv_layout_id or worker_addr not in self._acked_layout_peers
        )
        # Each pass either returns or breaks out of the recv loop to resend
        # the layout after a LAYOUT_MISS.
        while True:
            metadata = self._build_pull_metadata(
                pull_metas, include_layout=include_layout
            )
            encoded_data = self._encoder.encode(metadata)
            logger.debug(
                "MooncakeXferMetadata to %s is %d bytes (%s).",
                worker_addr,
                len(encoded_data),
                "layout" if include_layout else "blocks",
            )
            logger.debug(
                "Sending kv transfer request for %s on path: %s", req_ids, worker_addr
            )
            try:
                with make_zmq_socket(
                    self.async_zmq_ctx, worker_addr, zmq.DEALER, bind=False, linger=0
                ) as sock:
                    sock.setsockopt(
                        zmq.RCVTIMEO,
                        (envs.VLLM_MOONCAKE_ABORT_REQUEST_TIMEOUT + 60) * 1000,
                    )
                    await sock.send(encoded_data)
                    while True:
                        ret_msg = await sock.recv()
                        response = self._xfer_resp_decoder.decode(ret_msg)
                        status = response.status
                        if status == MooncakeXferResponseStatus.LAYOUT_MISS:
                            self._acked_layout_peers.discard(worker_addr)
                            if not include_layout:
                                logger.info(
                                    "Mooncake prefill %s lost the KV layout; "
                                    "resending it.",
                                    worker_addr,
                                )
                                include_layout = True
                                break
                        if status in (
                            MooncakeXferResponseStatus.ERROR,
                            MooncakeXferResponseStatus.LAYOUT_MISS,
                        ):
                            self._handle_failed_recv(
                                pull_metas,
                                req_ids,
                                response.err_msg or "transfer error",
                            )
                            return
                        if (
                            self._kv_layout_id
                            and response.layout_id == self._kv_layout_id
                        ):
                            self._acked_layout_peers.add(worker_addr)
                        self.process_pulling_result(response, pull_metas)
                        if status == MooncakeXferResponseStatus.FINISH:
                            return
            except zmq.ContextTerminated:
                logger.debug(
                    "ZMQ context terminated, exiting Mooncake receiver thread."
                )
                return
            except Exception as e:
                self._handle_failed_recv(pull_metas, req_ids, f"transfer failed: {e}")
                return
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def receive_kv_from_single_worker(
        self,
        worker_addr: str,
        pull_metas: dict[ReqId, PullReqMeta],
    ):
        # Each peer settles its own requests, sharing the per-request counters.
        pull_metas = pull_metas.copy()
        req_ids = set(pull_metas)
        include_layout = (
            not self._kv_layout_id or worker_addr not in self._acked_layout_peers
        )
        # Each pass either returns or breaks out of the recv loop to resend
        # the layout after a LAYOUT_MISS.
        while True:
            metadata = self._build_pull_metadata(
                pull_metas, include_layout=include_layout
            )
            encoded_data = self._encoder.encode(metadata)
            logger.debug(
                "MooncakeXferMetadata to %s is %d bytes (%s).",
                worker_addr,
                len(encoded_data),
                "layout" if include_layout else "blocks",
            )
            logger.debug(
                "Sending kv transfer request for %s on path: %s", req_ids, worker_addr
            )
            try:
                with make_zmq_socket(
                    self.async_zmq_ctx, worker_addr, zmq.DEALER, bind=False, linger=0
                ) as sock:
                    sock.setsockopt(
                        zmq.RCVTIMEO,
                        (envs.VLLM_MOONCAKE_ABORT_REQUEST_TIMEOUT + 60) * 1000,
                    )
                    await sock.send(encoded_data)
                    while True:
                        ret_msg = await sock.recv()
                        response = self._xfer_resp_decoder.decode(ret_msg)
                        status = response.status
                        if status == MooncakeXferResponseStatus.LAYOUT_MISS:
                            self._acked_layout_peers.discard(worker_addr)
                            if not include_layout:
                                logger.info(
                                    "Mooncake prefill %s lost the KV layout; "
                                    "resending it.",
                                    worker_addr,
                                )
                                include_layout = True
                                break
                        if status in (
                            MooncakeXferResponseStatus.ERROR,
                            MooncakeXferResponseStatus.LAYOUT_MISS,
                        ):
                            self._handle_failed_recv(
                                pull_metas,
                                req_ids,
                                response.err_msg or "transfer error",
                            )
                            return
                        if (
                            self._kv_layout_id
                            and response.layout_id == self._kv_layout_id
                        ):
                            self._acked_layout_peers.add(worker_addr)
                        self.process_pulling_result(response, pull_metas)
                        if status == MooncakeXferResponseStatus.FINISH:
                            # P may omit expired requests from its final response.
                            self._handle_failed_recv(
                                pull_metas,
                                list(pull_metas),
                                "peer finished without reporting a transfer result",
                            )
                            return
            except zmq.ContextTerminated:
                logger.debug(
                    "ZMQ context terminated, exiting Mooncake receiver thread."
                )
                return
            except Exception as e:
                self._handle_failed_recv(pull_metas, req_ids, f"transfer failed: {e}")
                return
```

### 🔹 函式: `MooncakeConnectorWorker._handle_failed_recv()`
- **變更前簽章 (Before)**: `def _handle_failed_recv( self, pull_metas: dict[ReqId, PullReqMeta], req_ids: Collection[ReqId], reason: str, ) -> None` (L2472~L2504)
- **變更後簽章 (After)**: `def _handle_failed_recv( self, pull_metas: dict[ReqId, PullReqMeta], req_ids: Collection[ReqId], reason: str, ) -> None` (L2480~L2516)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _handle_failed_recv(
        self,
        pull_metas: dict[ReqId, PullReqMeta],
        req_ids: Collection[ReqId],
        reason: str,
    ) -> None:
        """Report a failed remote KV load so the scheduler can fail or recompute it."""
        failed: list[ReqId] = []
        for req_id in req_ids:
            pull_meta = pull_metas.get(req_id)
            if pull_meta is None or pull_meta.failed:
                continue
            pull_meta.failed = True
            failed.append(req_id)
            self.xfer_stats.record_failed_recv()

            invalid = {b for group in pull_meta.local_block_ids for b in group}
            if not invalid:
                # A pull with no local blocks only asks P to release its blocks
                # for a request that never reached the scheduler (see
                # AsyncLLM.notify_kv_transfer_request_rejected, which submits an
                # abort_immediately request just to run request_finished). No D
                # request is waiting on a load, and reporting one here would trip
                # the scheduler's `assert req_id in self.requests`.
                continue
            if self._is_hma_required:
                self._failed_recv_reqs.put(pull_meta.d_req_id)
            else:
                self._invalid_block_ids.put(invalid)
            self.finished_recving_reqs.add(pull_meta.d_req_id)

        if failed:
            logger.error("pulling kv_caches for %s failed: %s", failed, reason)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _handle_failed_recv(
        self,
        pull_metas: dict[ReqId, PullReqMeta],
        req_ids: Collection[ReqId],
        reason: str,
    ) -> None:
        """Report a failed remote KV load so the scheduler can fail or recompute it."""
        failed: list[ReqId] = []
        for req_id in req_ids:
            pull_meta = pull_metas.pop(req_id, None)
            if pull_meta is None:
                continue
            if pull_meta.failed:
                self._complete_pull_task(pull_meta)
                continue
            pull_meta.failed = True
            failed.append(req_id)
            self.xfer_stats.record_failed_recv()

            invalid = {b for group in pull_meta.local_block_ids for b in group}
            if not invalid:
                # A pull with no local blocks only asks P to release its blocks
                # for a request that never reached the scheduler (see
                # AsyncLLM.notify_kv_transfer_request_rejected, which submits an
                # abort_immediately request just to run request_finished). No D
                # request is waiting on a load, and reporting one here would trip
                # the scheduler's `assert req_id in self.requests`.
                self._complete_pull_task(pull_meta)
                continue
            if self._is_hma_required:
                self._failed_recv_reqs.put(pull_meta.d_req_id)
            else:
                self._invalid_block_ids.put(invalid)
            self._complete_pull_task(pull_meta)

        if failed:
            logger.error("pulling kv_caches for %s failed: %s", failed, reason)
```


---


---

### 🔹 Commit #02: `143ee3b4`
- **完整 Hash**: `143ee3b4c9eb7fd25b5343cf3d2621a0f1bfa7c7`
- **說明 (Ground Truth)**: [Misc] Fix pre-commit failure on main from conflicts between pluggable KV cache and Step5 (#62593)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/models/step5/nvidia/sparse_attention.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:100, E:103, A:0) ➔ After(N:100, E:103, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Step5DSAMetadataBuilder._plan_prefill()`
- **變更前簽章 (Before)**: `def _plan_prefill(self, metadata, common) -> None` (L213~L253)
- **變更後簽章 (After)**: `def _plan_prefill(self, metadata, common) -> None` (L212~L252)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _plan_prefill(self, metadata, common) -> None:
        """Plan prefill steps here, before the forward, so the forward has no
        host sync: host lengths come from the scheduler and exact positions
        stay on device. Uniform (decode and MTP verify) batches need no plan.
        """
        layer = self._layer()
        impl = getattr(layer, "impl", None)
        n, reqs, query_len = (
            common.num_actual_tokens,
            common.num_reqs,
            common.max_query_len,
        )
        if (
            impl is None
            or impl.adapter is None
            or impl.summary_cache is None
            or not n
            or common.seq_lens_cpu_upper_bound is None
            or (n == reqs * query_len and query_len <= impl.num_speculative_tokens + 1)
        ):
            return
        # Upper bounds are exact without speculative decoding.
        positions = common.positions[:n] if impl.num_speculative_tokens else None
        if impl.num_speculative_tokens and common.positions is None:
            return
        spec = cast(AttentionSpec, self.kv_cache_spec)
        metadata.step5_runtime = impl.plan_prefill_step(
            metadata,
            n,
            common.seq_lens_cpu_upper_bound[:reqs].numpy(),
            _PrefillLayout(
                impl.num_heads // spec.num_kv_heads,
                spec.head_size,
                spec.num_kv_heads,
                self.vllm_config.model_config.dtype,
                is_quantized_kv_cache(impl.kv_cache_dtype),
                spec.block_size,
                kv_page_stride(layer.kv_cache),
            ),
            positions,
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _plan_prefill(self, metadata, common) -> None:
        """Plan prefill steps here, before the forward, so the forward has no
        host sync: host lengths come from the scheduler and exact positions
        stay on device. Uniform (decode and MTP verify) batches need no plan.
        """
        layer = self._layer()
        impl = getattr(layer, "impl", None)
        n, reqs, query_len = (
            common.num_actual_tokens,
            common.num_reqs,
            common.max_query_len,
        )
        if (
            impl is None
            or impl.adapter is None
            or impl.summary_cache is None
            or not n
            or common.seq_lens_cpu_upper_bound is None
            or (n == reqs * query_len and query_len <= impl.num_speculative_tokens + 1)
        ):
            return
        # Upper bounds are exact without speculative decoding.
        positions = common.positions[:n] if impl.num_speculative_tokens else None
        if impl.num_speculative_tokens and common.positions is None:
            return
        spec = cast(AttentionSpec, self.kv_cache_spec)
        metadata.step5_runtime = impl.plan_prefill_step(
            metadata,
            n,
            common.seq_lens_cpu_upper_bound[:reqs].numpy(),
            _PrefillLayout(
                impl.num_heads // spec.num_kv_heads,
                spec.head_size,
                spec.num_kv_heads,
                cast(torch.dtype, self.vllm_config.model_config.dtype),
                is_quantized_kv_cache(impl.kv_cache_dtype),
                spec.block_size,
                kv_page_stride(layer.kv_cache),
            ),
            positions,
        )
```


---


---

### 🔹 Commit #03: `17dd7d8f`
- **完整 Hash**: `17dd7d8fdd76f83384721bab790a32631813347f`
- **說明 (Ground Truth)**: [Bugfix][AuxOutput] Send routed-experts block hashes only for computed or scheduled blocks (#62489)
- **變更檔案數**: 2

#### 📄 檔案: `vllm/distributed/aux_output_connector/connector.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:14, E:9, A:0) ➔ After(N:14, E:10, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 3, -Edges: 2, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `AuxOutputSchedulerConnector._take_new_hashes` (FUNCTION_DEF)
  • - [移除節點] `AuxOutputSchedulerConnector._pack_new_hashes` (FUNCTION_DEF)
  • + [新增呼叫邊] `AuxOutputSchedulerConnector.build_connector_meta` ──[CALLS]──> `AuxOutputSchedulerConnector._take_new_hashes`
  • + [新增呼叫邊] `AuxOutputSchedulerConnector.request_finished` ──[CALLS]──> `AuxOutputSchedulerConnector._take_new_hashes`
  • + [新增呼叫邊] `AuxOutputSchedulerConnector._take_new_hashes` ──[CALLS]──> `min (External/Unresolved)`
  • - [移除呼叫邊] `AuxOutputSchedulerConnector.build_connector_meta` ──[CALLS]──> `AuxOutputSchedulerConnector._pack_new_hashes`
  • - [移除呼叫邊] `AuxOutputSchedulerConnector.request_finished` ──[CALLS]──> `AuxOutputSchedulerConnector._pack_new_hashes`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `AuxOutputSchedulerConnector.request_finished()`
- **變更前簽章 (Before)**: `def request_finished(self, request: Request) -> None` (L135~L144)
- **變更後簽章 (After)**: `def request_finished(self, request: Request) -> None` (L135~L144)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def request_finished(self, request: Request) -> None:
        """Queue a request's terminal event and final block hashes."""
        request_id = request.request_id
        num_sent = self._sent_hash_counts.pop(request_id, None)
        if num_sent is None:
            return
        # The next metadata delivers this terminal event to the worker.
        self._finished_requests[request_id] = self._pack_new_hashes(
            request.block_hashes, num_sent
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def request_finished(self, request: Request) -> None:
        """Queue a request's terminal event and final block hashes."""
        request_id = request.request_id
        if request_id not in self._sent_hash_counts:
            return
        # The next metadata delivers this terminal event to the worker.
        self._finished_requests[request_id] = self._take_new_hashes(
            request, request.num_computed_tokens
        )
        del self._sent_hash_counts[request_id]
```

### 🔹 函式: `AuxOutputSchedulerConnector.build_connector_meta()`
- **變更前簽章 (Before)**: `def build_connector_meta( self, scheduler_output: SchedulerOutput, requests: dict[str, Request], ) -> AuxOutputConnectorMetadata` (L54~L103)
- **變更後簽章 (After)**: `def build_connector_meta( self, scheduler_output: SchedulerOutput, requests: dict[str, Request], ) -> AuxOutputConnectorMetadata` (L55~L103)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def build_connector_meta(
        self,
        scheduler_output: SchedulerOutput,
        requests: dict[str, Request],
    ) -> AuxOutputConnectorMetadata:
        """Build one step's incremental worker metadata."""
        scheduled_requests: dict[str, int] = {}
        block_hashes_by_request: dict[str, PackedBlockHashes] = {}
        for request_id in scheduler_output.num_scheduled_tokens:
            num_sent = self._sent_hash_counts.setdefault(request_id, 0)
            request = requests[request_id]
            packed = self._pack_new_hashes(request.block_hashes, num_sent)
            if packed is not None:
                block_hashes_by_request[request_id] = packed
            self._sent_hash_counts[request_id] = len(request.block_hashes)
            assert request.sampling_params is not None
            # A P/D prefiller may cut the prompt short of the requested start.
            scheduled_requests[request_id] = max(
                min(
                    request.sampling_params.routed_experts_prompt_start,
                    request.num_prompt_tokens,
                ),
                0 if request.num_output_tokens == 0 else request.num_tokens - 1,
            )
        # A settled token can complete a hash block after the next async schedule
        # was built. Send a hash-only update if the request was not rescheduled.
        if len(self._sent_hash_counts) != len(scheduled_requests):
            for request_id, num_sent in self._sent_hash_counts.items():
                if request_id in scheduled_requests:
                    continue
                request = requests[request_id]
                packed = self._pack_new_hashes(request.block_hashes, num_sent)
                if packed is None:
                    continue
                block_hashes_by_request[request_id] = packed
                self._sent_hash_counts[request_id] = len(request.block_hashes)
        # Sending transfers ownership of these one-shot events.
        finished_requests = tuple(self._finished_requests)
        block_hashes_by_request.update(
            (request_id, block_hashes)
            for request_id, block_hashes in self._finished_requests.items()
            if block_hashes is not None
        )
        self._finished_requests = {}
        return AuxOutputConnectorMetadata(
            self._generation,
            scheduled_requests,
            block_hashes_by_request,
            finished_requests,
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def build_connector_meta(
        self,
        scheduler_output: SchedulerOutput,
        requests: dict[str, Request],
    ) -> AuxOutputConnectorMetadata:
        """Build one step's incremental worker metadata."""
        scheduled_requests: dict[str, int] = {}
        block_hashes_by_request: dict[str, PackedBlockHashes] = {}
        for request_id, num_tokens in scheduler_output.num_scheduled_tokens.items():
            self._sent_hash_counts.setdefault(request_id, 0)
            request = requests[request_id]
            packed = self._take_new_hashes(
                request, request.num_computed_tokens + num_tokens
            )
            if packed is not None:
                block_hashes_by_request[request_id] = packed
            assert request.sampling_params is not None
            # A P/D prefiller may cut the prompt short of the requested start.
            scheduled_requests[request_id] = max(
                min(
                    request.sampling_params.routed_experts_prompt_start,
                    request.num_prompt_tokens,
                ),
                0 if request.num_output_tokens == 0 else request.num_tokens - 1,
            )
        # A settled token can complete a hash block after the next async schedule
        # was built. Send a hash-only update if the request was not rescheduled.
        if len(self._sent_hash_counts) != len(scheduled_requests):
            for request_id in self._sent_hash_counts:
                if request_id in scheduled_requests:
                    continue
                request = requests[request_id]
                packed = self._take_new_hashes(request, request.num_computed_tokens)
                if packed is not None:
                    block_hashes_by_request[request_id] = packed
        # Sending transfers ownership of these one-shot events.
        finished_requests = tuple(self._finished_requests)
        block_hashes_by_request.update(
            (request_id, block_hashes)
            for request_id, block_hashes in self._finished_requests.items()
            if block_hashes is not None
        )
        self._finished_requests = {}
        return AuxOutputConnectorMetadata(
            self._generation,
            scheduled_requests,
            block_hashes_by_request,
            finished_requests,
        )
```

### 🔹 函式: `AuxOutputSchedulerConnector.__init__()`
- **變更前簽章 (Before)**: `def __init__(self) -> None: # Number of hashes already sent to the worker for each active request.` (L47~L52)
- **變更後簽章 (After)**: `def __init__(self, hash_block_size: int) -> None` (L47~L53)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(self) -> None:
        # Number of hashes already sent to the worker for each active request.
        self._sent_hash_counts: dict[str, int] = {}
        # Terminal events are delivered with the next connector metadata.
        self._finished_requests: dict[str, PackedBlockHashes | None] = {}
        self._generation = 0
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(self, hash_block_size: int) -> None:
        self._hash_block_size = hash_block_size
        # Number of hashes already sent to the worker for each active request.
        self._sent_hash_counts: dict[str, int] = {}
        # Terminal events are delivered with the next connector metadata.
        self._finished_requests: dict[str, PackedBlockHashes | None] = {}
        self._generation = 0
```


#### 📄 檔案: `vllm/v1/core/sched/scheduler.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:226, E:326, A:0) ➔ After(N:226, E:326, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Scheduler.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, vllm_config: VllmConfig, kv_cache_config: KVCacheConfig, structured_output_manager: StructuredOutputManager, block_size: int, hash_block_size: int | None = None, mm_registry: MultiModalRegistry = MULTIMODAL_REGISTRY, include_finished_set: bool = False, log_stats: bool = False, ) -> None` (L85~L471)
- **變更後簽章 (After)**: `def __init__( self, vllm_config: VllmConfig, kv_cache_config: KVCacheConfig, structured_output_manager: StructuredOutputManager, block_size: int, hash_block_size: int | None = None, mm_registry: MultiModalRegistry = MULTIMODAL_REGISTRY, include_finished_set: bool = False, log_stats: bool = False, ) -> None` (L85~L471)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        vllm_config: VllmConfig,
        kv_cache_config: KVCacheConfig,
        structured_output_manager: StructuredOutputManager,
        block_size: int,
        hash_block_size: int | None = None,
        mm_registry: MultiModalRegistry = MULTIMODAL_REGISTRY,
        include_finished_set: bool = False,
        log_stats: bool = False,
    ) -> None:
        self.vllm_config = vllm_config
        self.scheduler_config = vllm_config.scheduler_config
        self.cache_config = vllm_config.cache_config
        self.lora_config = vllm_config.lora_config
        self.model_uses_mrope = vllm_config.model_config.uses_mrope
        self.kv_cache_config = kv_cache_config
        self.kv_events_config = vllm_config.kv_events_config
        self.parallel_config = vllm_config.parallel_config
        self.log_stats = log_stats
        self.observability_config = vllm_config.observability_config
        self.spec_decode_metrics_level = (
            self.observability_config.per_request_spec_decode_metrics
        )
        self.kv_metrics_collector: KVCacheMetricsCollector | None = None
        if self.observability_config.kv_cache_metrics:
            self.kv_metrics_collector = KVCacheMetricsCollector(
                self.observability_config.kv_cache_metrics_sample,
            )
        self.structured_output_manager = structured_output_manager
        self.is_encoder_decoder = vllm_config.model_config.is_encoder_decoder
        self.is_mm_encoder_only = vllm_config.is_mm_encoder_only

        # include_finished_set controls whether a separate set of finished
        # request ids should be included in the EngineCoreOutputs returned
        # by update_from_outputs(). This is currently used in the multi-engine
        # case to track request lifetimes efficiently.
        self.finished_req_ids_dict: dict[int, set[str]] | None = (
            defaultdict(set) if include_finished_set else None
        )
        # Track requests scheduled in prior step (MRV1-only).
        self.prev_step_scheduled_req_ids: set[str] = set()

        # Scheduling constraints.
        self.max_num_running_reqs = self.scheduler_config.max_num_seqs
        # Admission into RUNNING. Separate from max_num_running_reqs, which
        # is the model-runner slot count.
        self.max_num_active_reqs = (
            self.scheduler_config.max_num_active_seqs
            if self.scheduler_config.max_num_active_seqs is not None
            else self.max_num_running_reqs
        )
        self.max_num_scheduled_tokens = (
            self.scheduler_config.max_num_scheduled_tokens
            if self.scheduler_config.max_num_scheduled_tokens is not None
            else self.scheduler_config.max_num_batched_tokens
        )
        self.adaptive_long_prefill_threshold = (
            self.scheduler_config.long_prefill_token_threshold_adaptive
        )
        self.max_model_len = vllm_config.model_config.max_model_len
        self.enable_kv_cache_events = (
            self.kv_events_config is not None
            and self.kv_events_config.enable_kv_cache_events
        )
        # Pooling and diffusion models do not append a sampled token after
        # prefill, so they should not reserve one context slot while scheduling.
        self.num_sampled_tokens_per_step = (
            0
            if (
                vllm_config.model_config.runner_type == "pooling"
                or vllm_config.model_config.is_diffusion
            )
            else 1
        )

        # Create KVConnector for the Scheduler. Note that each Worker
        # will have a corresponding KVConnector with Role=WORKER.
        # KV Connector pushes/pull of remote KVs for P/D and offloading.
        self.connector = None
        self.connector_prefix_cache_stats: PrefixCacheStats | None = None
        self.recompute_kv_load_failures = True
        self.defer_block_free = False
        # Whether a preempted request's in-flight output must be dropped; see
        # KVConnectorBase_V1.requires_kv_delivery.
        self.requires_kv_delivery = False
        kv_transfer_config = self.vllm_config.kv_transfer_config
        if kv_transfer_config is not None:
            assert not self.is_encoder_decoder, (
                "Encoder-decoder models are not currently supported with KV connectors"
            )
            self.connector = KVConnectorFactory.create_connector(
                config=self.vllm_config,
                role=KVConnectorRole.SCHEDULER,
                kv_cache_config=self.kv_cache_config,
            )
            if self.log_stats:
                self.connector_prefix_cache_stats = PrefixCacheStats()
            kv_load_failure_policy = kv_transfer_config.kv_load_failure_policy
            self.recompute_kv_load_failures = kv_load_failure_policy == "recompute"

            # With overlapping batches (async scheduling or PP), a step may
            # still be writing a freed request's KV blocks. A consumer KV
            # Connector can reallocate and fill those blocks via a load that
            # isn't ordered against that write, so defer freeing them.
            multiple_inflight_batches = self.vllm_config.max_concurrent_batches > 1
            if multiple_inflight_batches and kv_transfer_config.is_kv_consumer:
                self.defer_block_free = True

            self.requires_kv_delivery = self.connector.requires_kv_delivery

        self.kv_event_publisher = EventPublisherFactory.create(
            self.kv_events_config,
            self.parallel_config.data_parallel_index,
        )
        self.ec_connector = None
        if self.vllm_config.ec_transfer_config is not None:
            self.ec_connector = ECConnectorFactory.create_connector(
                config=self.vllm_config, role=ECConnectorRole.SCHEDULER
            )

        num_gpu_blocks = self.cache_config.num_gpu_blocks
        assert num_gpu_blocks is not None and num_gpu_blocks > 0

        self.block_size = block_size
        self.dcp_world_size = vllm_config.parallel_config.decode_context_parallel_size
        self.pcp_world_size = vllm_config.parallel_config.prefill_context_parallel_size

        # req_id -> Request
        self.requests: dict[str, Request] = {}
        # Scheduling policy
        try:
            self.policy = SchedulingPolicy(self.scheduler_config.policy)
        except ValueError as e:
            raise ValueError(
                f"Unknown scheduling policy: {self.scheduler_config.policy}"
            ) from e
        # Priority queues for requests.
        self.waiting = create_request_queue(self.policy)
        # Waiting requests that hold KV blocks are always drained before
        # self.waiting: a block-holder must never sit behind a request whose
        # failed allocation would stop the scheduling scan.
        self.kv_holding_waiting = create_request_queue(self.policy)
        # Waiting requests that are deferred, i.e. were skipped by the scheduling
        # scan or enqueued in a blocked status.
        self.deferred_waiting: set[Request] = set()
        self.running: list[Request] = []

        # The request IDs that are finished in between the previous and the
        # current steps. This is used to notify the workers about the finished
        # requests so that they can free the cached states for those requests.
        # This is flushed at the end of each scheduling step.
        self.finished_req_ids: set[str] = set()

        # IDs of requests preempted since the last call to schedule().
        self.reset_preempted_req_ids: set[str] = set()

        # Counter for requests waiting for streaming input. Used to calculate
        # number of unfinished requests
        self.num_waiting_for_streaming_input: int = 0

        # KV Connector: requests in process of async KV loading or recving
        self.finished_recving_kv_req_ids: set[str] = set()
        self.failed_recving_kv_req_ids: set[str] = set()

        # Grammar compilation failures to finish as per-request errors in
        # update_from_output.
        self.grammar_compile_error_reqs: set[str] = set()
        self.encoder_cache_mismatch_reqs: set[str] = set()

        # Encoder-related.
        # Calculate encoder cache size if applicable
        supports_mm_inputs = vllm_config.model_config.supports_multimodal_inputs
        mm_budget = (
            MultiModalBudget(vllm_config, mm_registry) if supports_mm_inputs else None
        )

        # NOTE: Text-only encoder-decoder models are implemented as
        # multi-modal models for convenience
        # Example: https://github.com/vllm-project/bart-plugin
        if self.is_encoder_decoder:
            assert mm_budget and len(mm_budget.mm_max_toks_per_item) <= 1, (
                "Encoder-decoder models are expected to implement the "
                "multimodal interface with at most one modality."
            )

        self.max_num_encoder_input_tokens = (
            mm_budget.encoder_compute_budget if mm_budget else 0
        )
        encoder_cache_size = mm_budget.encoder_cache_size if mm_budget else 0
        manager_cls_obj = vllm_config.ec_manager_config.get_encoder_cache_manager_obj()
        if manager_cls_obj is None:
            manager_cls_obj = (
                EncoderDecoderCacheManager
                if self.is_encoder_decoder
                else EncoderCacheManager
            )
        self.encoder_cache_manager = manager_cls_obj.create_manager(
            cache_size=encoder_cache_size, vllm_config=vllm_config
        )
        speculative_config = vllm_config.speculative_config
        self.use_eagle = False
        self.use_eagle_block_drop = False
        self.num_spec_tokens = vllm_config.num_speculative_tokens
        self.num_lookahead_tokens = vllm_config.num_lookahead_tokens
        # DSV41 SWA bounded replay: groups that declare a replay window are rebuilt
        # after a prefix hit by recomputing its trailing tokens. One window
        # for all such groups, so the rewind matches every group's allocation.
        self.prefix_replay_group_ids = tuple(
            group_id
            for group_id, group in enumerate(kv_cache_config.kv_cache_groups)
            if group.kv_cache_spec.prefix_replay_tokens > 0
        )
        replay_windows = {
            kv_cache_config.kv_cache_groups[group_id].kv_cache_spec.prefix_replay_tokens
            for group_id in self.prefix_replay_group_ids
        }
        assert len(replay_windows) <= 1, (
            f"Prefix replay windows should agree: {sorted(replay_windows)}"
        )
        self.prefix_replay_tokens = replay_windows.pop() if replay_windows else 0
        self.num_prefill_lookahead = vllm_config.num_prefill_lookahead_tokens
        self.dynamic_sd_lookup: list[int] | None = None
        if speculative_config is not None:
            if speculative_config.num_speculative_tokens_per_batch_size:
                self.dynamic_sd_lookup = build_dynamic_sd_schedule_lookup(
                    speculative_config.num_speculative_tokens_per_batch_size,
                    vllm_max_batch_size=self.scheduler_config.max_num_seqs,
                    vllm_num_speculative_tokens=self.num_spec_tokens,
                )
            self.use_eagle = speculative_config.use_eagle()
            self.use_eagle_block_drop = speculative_config.use_eagle_block_drop()
            if self.use_eagle and not self.use_eagle_block_drop:
                logger.warning(
                    "EAGLE trailing prefix-cache block dropping is disabled. "
                    "This is experimental and may affect speculative-token "
                    "acceptance rates."
                )

        # Create the KV cache manager.
        if hash_block_size is None:
            hash_block_size = block_size
        self.hash_block_size = hash_block_size
        self.kv_cache_manager = KVCacheManager(
            kv_cache_config=kv_cache_config,
            max_model_len=self.max_model_len,
            max_in_flight_tokens=vllm_config.max_in_flight_tokens,
            enable_caching=self.cache_config.enable_prefix_caching,
            use_eagle=self.use_eagle_block_drop,
            num_prefill_lookahead=self.num_prefill_lookahead,
            log_stats=self.log_stats,
            enable_kv_cache_events=self.enable_kv_cache_events,
            dcp_world_size=self.dcp_world_size,
            pcp_world_size=1,
            scheduler_block_size=self.block_size,
            hash_block_size=hash_block_size,
            metrics_collector=self.kv_metrics_collector,
            watermark=self.scheduler_config.watermark,
            enable_mamba_shared_prefix_checkpoint=(
                self.cache_config.enable_mamba_shared_prefix_checkpoint
            ),
        )
        # Mamba managers already account for their speculative state blocks.
        num_spec_decode_tokens = (
            1 + self.num_spec_tokens + self.num_lookahead_tokens
            if self.num_spec_tokens
            else 0
        )
        self._spec_decode_step_blocks = sum(
            cdiv(num_spec_decode_tokens, manager.block_size)
            for manager in self.kv_cache_manager.coordinator.single_type_managers
            if not isinstance(manager.kv_cache_spec, MambaSpec)
        )
        # Bind after construction so connectors can access the cache manager.
        if self.connector is not None:
            self.connector.bind_kv_cache_manager(self.kv_cache_manager)

        self.use_pp = self.parallel_config.pipeline_parallel_size > 1
        self.use_v2_model_runner = vllm_config.use_v2_model_runner
        # Scheduler iteration counter. Drives the V2+PP+async decode-throttle
        # cadence (`next_decode_eligible_step`).
        self.current_step = 0
        # DP prefill balancing: Flag to track whether the last cadence-aligned
        # prefill batch fully drained the waiting queue. Prefill throttling
        # is disabled in this case.
        self.prefill_capacity_bound = False
        # The DP engine core drives this cadence from a counter shared across
        # ranks; an engine without one never throttles, so apply the interval
        # locally, timed from the last prefill-carrying step. Three regimes:
        #   1. no DP -- local cadence applies;
        #   2. dense DP rank -- `reconfigure_for_independent_dp_rank` already
        #      set data_parallel_size=1, so each rank gets its own cadence.
        #      Intended, but a behaviour change: this used to be a no-op;
        #   3. MoE DP rank (size > 1) -- the engine core drives it, no-op here.
        self.local_prefill_interval = (
            self.scheduler_config.prefill_schedule_interval
            if self.parallel_config.data_parallel_size == 1
            else 1
        )
        if self.local_prefill_interval > 1:
            # Neither the hold nor its release is otherwise visible in logs or
            # stats, which makes a misapplied cadence hard to diagnose.
            logger.info_once(
                "Prefill cadence: applying prefill_schedule_interval=%d "
                "locally (this engine is not DP-coordinated); prefill is held "
                "until %d executed steps have passed since the last "
                "prefill-carrying step.",
                self.local_prefill_interval,
                self.local_prefill_interval,
            )
        # A full interval back, so the first step is never gated.
        self.last_prefill_step = -self.local_prefill_interval
        # Steps that actually scheduled tokens. `current_step` counts every
        # schedule() call including empty ones, so it would expire the hold
        # early; it keeps its own meaning (next_decode_eligible_step).
        self.num_executed_steps = 0
        self.scheduler_reserve_full_isl = (
            self.scheduler_config.scheduler_reserve_full_isl
        )

        self.has_mamba_layers = kv_cache_config.has_mamba_layers
        self.needs_kv_cache_zeroing = kv_cache_config.needs_kv_cache_zeroing
        self.need_mamba_block_aligned_split = (
            self.has_mamba_layers and self.cache_config.mamba_cache_mode == "align"
        )
        # TODO: Support models with multiple Mamba specs that require different
        # prefill checkpoint alignments instead of selecting the first one.
        self.mamba_prefill_checkpoint_alignment = next(
            (
                group.kv_cache_spec.prefill_checkpoint_alignment
                for group in kv_cache_config.kv_cache_groups
                if isinstance(group.kv_cache_spec, MambaSpec)
            ),
            None,
        )
        self.mamba_has_prefill_checkpoint_blocks = self.has_mamba_layers and all(
            not isinstance(group.kv_cache_spec, MambaSpec)
            or group.kv_cache_spec.num_prefill_checkpoint_blocks > 0
            for group in kv_cache_config.kv_cache_groups
        )
        # Fine-grained hits reuse the prompt's hash-aligned Mamba checkpoint.
        # Split there only if the backend cannot save it within the final chunk.
        self.mamba_partial_cache_hit = (
            self.need_mamba_block_aligned_split
            and self.hash_block_size < self.block_size
            and self.kv_cache_manager.coordinator.enable_partial_hash_hits
        )
        # Opt-in: also stop at the junction, where an eagle sibling resumes. The
        # manager decides whether it can check-point there (per-group eagle bit,
        # no MTP re-prefill tail); splitting for a stop it would refuse costs a
        # forward pass and displaces the block-boundary stop.
        self.mamba_shared_prefix_checkpoint = (
            self.mamba_partial_cache_hit
            and self.kv_cache_manager.mamba_shared_prefix_checkpoint
        )

        # Counts of non-empty steps scheduled / processed. update_from_output
        # is called once per scheduled step in FIFO order, so these stay in sync.
        self.sched_step_seq = 0
        self.processed_step_seq = 0
        # FIFO of (fence_seq, blocks): blocks become safe to free once
        # processed_step_seq >= fence_seq.
        self.deferred_frees: deque[tuple[int, list[KVCacheBlock]]] = deque()

        self.perf_metrics: ModelMetrics | None = None
        if self.log_stats and vllm_config.observability_config.enable_mfu_metrics:
            self.perf_metrics = ModelMetrics(vllm_config)

        self.aux_output_connector = (
            AuxOutputSchedulerConnector()
            if vllm_config.aux_output_config.enabled
            else None
        )
        self.return_sampling_mask = vllm_config.model_config.return_sampling_mask

        self._pause_state: PauseState = PauseState.UNPAUSED

        # In-flight requests still prefilling (prefill chunks + in-progress
        # async KV loads). Their remaining-block reservation gates async loads.
        self._inflight_prefills: set[Request] = set()

        # Requests with an async KV load, by stage (KV_FETCH_STAGES).
        # None when not tracked (stats disabled or no KV connector).
        self._kv_fetch_stages: dict[Request, str] | None = (
            {} if self.log_stats and self.connector is not None else None
        )
        self._kv_fetch_counts: dict[str, int] = dict.fromkeys(KV_FETCH_STAGES, 0)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        vllm_config: VllmConfig,
        kv_cache_config: KVCacheConfig,
        structured_output_manager: StructuredOutputManager,
        block_size: int,
        hash_block_size: int | None = None,
        mm_registry: MultiModalRegistry = MULTIMODAL_REGISTRY,
        include_finished_set: bool = False,
        log_stats: bool = False,
    ) -> None:
        self.vllm_config = vllm_config
        self.scheduler_config = vllm_config.scheduler_config
        self.cache_config = vllm_config.cache_config
        self.lora_config = vllm_config.lora_config
        self.model_uses_mrope = vllm_config.model_config.uses_mrope
        self.kv_cache_config = kv_cache_config
        self.kv_events_config = vllm_config.kv_events_config
        self.parallel_config = vllm_config.parallel_config
        self.log_stats = log_stats
        self.observability_config = vllm_config.observability_config
        self.spec_decode_metrics_level = (
            self.observability_config.per_request_spec_decode_metrics
        )
        self.kv_metrics_collector: KVCacheMetricsCollector | None = None
        if self.observability_config.kv_cache_metrics:
            self.kv_metrics_collector = KVCacheMetricsCollector(
                self.observability_config.kv_cache_metrics_sample,
            )
        self.structured_output_manager = structured_output_manager
        self.is_encoder_decoder = vllm_config.model_config.is_encoder_decoder
        self.is_mm_encoder_only = vllm_config.is_mm_encoder_only

        # include_finished_set controls whether a separate set of finished
        # request ids should be included in the EngineCoreOutputs returned
        # by update_from_outputs(). This is currently used in the multi-engine
        # case to track request lifetimes efficiently.
        self.finished_req_ids_dict: dict[int, set[str]] | None = (
            defaultdict(set) if include_finished_set else None
        )
        # Track requests scheduled in prior step (MRV1-only).
        self.prev_step_scheduled_req_ids: set[str] = set()

        # Scheduling constraints.
        self.max_num_running_reqs = self.scheduler_config.max_num_seqs
        # Admission into RUNNING. Separate from max_num_running_reqs, which
        # is the model-runner slot count.
        self.max_num_active_reqs = (
            self.scheduler_config.max_num_active_seqs
            if self.scheduler_config.max_num_active_seqs is not None
            else self.max_num_running_reqs
        )
        self.max_num_scheduled_tokens = (
            self.scheduler_config.max_num_scheduled_tokens
            if self.scheduler_config.max_num_scheduled_tokens is not None
            else self.scheduler_config.max_num_batched_tokens
        )
        self.adaptive_long_prefill_threshold = (
            self.scheduler_config.long_prefill_token_threshold_adaptive
        )
        self.max_model_len = vllm_config.model_config.max_model_len
        self.enable_kv_cache_events = (
            self.kv_events_config is not None
            and self.kv_events_config.enable_kv_cache_events
        )
        # Pooling and diffusion models do not append a sampled token after
        # prefill, so they should not reserve one context slot while scheduling.
        self.num_sampled_tokens_per_step = (
            0
            if (
                vllm_config.model_config.runner_type == "pooling"
                or vllm_config.model_config.is_diffusion
            )
            else 1
        )

        # Create KVConnector for the Scheduler. Note that each Worker
        # will have a corresponding KVConnector with Role=WORKER.
        # KV Connector pushes/pull of remote KVs for P/D and offloading.
        self.connector = None
        self.connector_prefix_cache_stats: PrefixCacheStats | None = None
        self.recompute_kv_load_failures = True
        self.defer_block_free = False
        # Whether a preempted request's in-flight output must be dropped; see
        # KVConnectorBase_V1.requires_kv_delivery.
        self.requires_kv_delivery = False
        kv_transfer_config = self.vllm_config.kv_transfer_config
        if kv_transfer_config is not None:
            assert not self.is_encoder_decoder, (
                "Encoder-decoder models are not currently supported with KV connectors"
            )
            self.connector = KVConnectorFactory.create_connector(
                config=self.vllm_config,
                role=KVConnectorRole.SCHEDULER,
                kv_cache_config=self.kv_cache_config,
            )
            if self.log_stats:
                self.connector_prefix_cache_stats = PrefixCacheStats()
            kv_load_failure_policy = kv_transfer_config.kv_load_failure_policy
            self.recompute_kv_load_failures = kv_load_failure_policy == "recompute"

            # With overlapping batches (async scheduling or PP), a step may
            # still be writing a freed request's KV blocks. A consumer KV
            # Connector can reallocate and fill those blocks via a load that
            # isn't ordered against that write, so defer freeing them.
            multiple_inflight_batches = self.vllm_config.max_concurrent_batches > 1
            if multiple_inflight_batches and kv_transfer_config.is_kv_consumer:
                self.defer_block_free = True

            self.requires_kv_delivery = self.connector.requires_kv_delivery

        self.kv_event_publisher = EventPublisherFactory.create(
            self.kv_events_config,
            self.parallel_config.data_parallel_index,
        )
        self.ec_connector = None
        if self.vllm_config.ec_transfer_config is not None:
            self.ec_connector = ECConnectorFactory.create_connector(
                config=self.vllm_config, role=ECConnectorRole.SCHEDULER
            )

        num_gpu_blocks = self.cache_config.num_gpu_blocks
        assert num_gpu_blocks is not None and num_gpu_blocks > 0

        self.block_size = block_size
        self.dcp_world_size = vllm_config.parallel_config.decode_context_parallel_size
        self.pcp_world_size = vllm_config.parallel_config.prefill_context_parallel_size

        # req_id -> Request
        self.requests: dict[str, Request] = {}
        # Scheduling policy
        try:
            self.policy = SchedulingPolicy(self.scheduler_config.policy)
        except ValueError as e:
            raise ValueError(
                f"Unknown scheduling policy: {self.scheduler_config.policy}"
            ) from e
        # Priority queues for requests.
        self.waiting = create_request_queue(self.policy)
        # Waiting requests that hold KV blocks are always drained before
        # self.waiting: a block-holder must never sit behind a request whose
        # failed allocation would stop the scheduling scan.
        self.kv_holding_waiting = create_request_queue(self.policy)
        # Waiting requests that are deferred, i.e. were skipped by the scheduling
        # scan or enqueued in a blocked status.
        self.deferred_waiting: set[Request] = set()
        self.running: list[Request] = []

        # The request IDs that are finished in between the previous and the
        # current steps. This is used to notify the workers about the finished
        # requests so that they can free the cached states for those requests.
        # This is flushed at the end of each scheduling step.
        self.finished_req_ids: set[str] = set()

        # IDs of requests preempted since the last call to schedule().
        self.reset_preempted_req_ids: set[str] = set()

        # Counter for requests waiting for streaming input. Used to calculate
        # number of unfinished requests
        self.num_waiting_for_streaming_input: int = 0

        # KV Connector: requests in process of async KV loading or recving
        self.finished_recving_kv_req_ids: set[str] = set()
        self.failed_recving_kv_req_ids: set[str] = set()

        # Grammar compilation failures to finish as per-request errors in
        # update_from_output.
        self.grammar_compile_error_reqs: set[str] = set()
        self.encoder_cache_mismatch_reqs: set[str] = set()

        # Encoder-related.
        # Calculate encoder cache size if applicable
        supports_mm_inputs = vllm_config.model_config.supports_multimodal_inputs
        mm_budget = (
            MultiModalBudget(vllm_config, mm_registry) if supports_mm_inputs else None
        )

        # NOTE: Text-only encoder-decoder models are implemented as
        # multi-modal models for convenience
        # Example: https://github.com/vllm-project/bart-plugin
        if self.is_encoder_decoder:
            assert mm_budget and len(mm_budget.mm_max_toks_per_item) <= 1, (
                "Encoder-decoder models are expected to implement the "
                "multimodal interface with at most one modality."
            )

        self.max_num_encoder_input_tokens = (
            mm_budget.encoder_compute_budget if mm_budget else 0
        )
        encoder_cache_size = mm_budget.encoder_cache_size if mm_budget else 0
        manager_cls_obj = vllm_config.ec_manager_config.get_encoder_cache_manager_obj()
        if manager_cls_obj is None:
            manager_cls_obj = (
                EncoderDecoderCacheManager
                if self.is_encoder_decoder
                else EncoderCacheManager
            )
        self.encoder_cache_manager = manager_cls_obj.create_manager(
            cache_size=encoder_cache_size, vllm_config=vllm_config
        )
        speculative_config = vllm_config.speculative_config
        self.use_eagle = False
        self.use_eagle_block_drop = False
        self.num_spec_tokens = vllm_config.num_speculative_tokens
        self.num_lookahead_tokens = vllm_config.num_lookahead_tokens
        # DSV41 SWA bounded replay: groups that declare a replay window are rebuilt
        # after a prefix hit by recomputing its trailing tokens. One window
        # for all such groups, so the rewind matches every group's allocation.
        self.prefix_replay_group_ids = tuple(
            group_id
            for group_id, group in enumerate(kv_cache_config.kv_cache_groups)
            if group.kv_cache_spec.prefix_replay_tokens > 0
        )
        replay_windows = {
            kv_cache_config.kv_cache_groups[group_id].kv_cache_spec.prefix_replay_tokens
            for group_id in self.prefix_replay_group_ids
        }
        assert len(replay_windows) <= 1, (
            f"Prefix replay windows should agree: {sorted(replay_windows)}"
        )
        self.prefix_replay_tokens = replay_windows.pop() if replay_windows else 0
        self.num_prefill_lookahead = vllm_config.num_prefill_lookahead_tokens
        self.dynamic_sd_lookup: list[int] | None = None
        if speculative_config is not None:
            if speculative_config.num_speculative_tokens_per_batch_size:
                self.dynamic_sd_lookup = build_dynamic_sd_schedule_lookup(
                    speculative_config.num_speculative_tokens_per_batch_size,
                    vllm_max_batch_size=self.scheduler_config.max_num_seqs,
                    vllm_num_speculative_tokens=self.num_spec_tokens,
                )
            self.use_eagle = speculative_config.use_eagle()
            self.use_eagle_block_drop = speculative_config.use_eagle_block_drop()
            if self.use_eagle and not self.use_eagle_block_drop:
                logger.warning(
                    "EAGLE trailing prefix-cache block dropping is disabled. "
                    "This is experimental and may affect speculative-token "
                    "acceptance rates."
                )

        # Create the KV cache manager.
        if hash_block_size is None:
            hash_block_size = block_size
        self.hash_block_size = hash_block_size
        self.kv_cache_manager = KVCacheManager(
            kv_cache_config=kv_cache_config,
            max_model_len=self.max_model_len,
            max_in_flight_tokens=vllm_config.max_in_flight_tokens,
            enable_caching=self.cache_config.enable_prefix_caching,
            use_eagle=self.use_eagle_block_drop,
            num_prefill_lookahead=self.num_prefill_lookahead,
            log_stats=self.log_stats,
            enable_kv_cache_events=self.enable_kv_cache_events,
            dcp_world_size=self.dcp_world_size,
            pcp_world_size=1,
            scheduler_block_size=self.block_size,
            hash_block_size=hash_block_size,
            metrics_collector=self.kv_metrics_collector,
            watermark=self.scheduler_config.watermark,
            enable_mamba_shared_prefix_checkpoint=(
                self.cache_config.enable_mamba_shared_prefix_checkpoint
            ),
        )
        # Mamba managers already account for their speculative state blocks.
        num_spec_decode_tokens = (
            1 + self.num_spec_tokens + self.num_lookahead_tokens
            if self.num_spec_tokens
            else 0
        )
        self._spec_decode_step_blocks = sum(
            cdiv(num_spec_decode_tokens, manager.block_size)
            for manager in self.kv_cache_manager.coordinator.single_type_managers
            if not isinstance(manager.kv_cache_spec, MambaSpec)
        )
        # Bind after construction so connectors can access the cache manager.
        if self.connector is not None:
            self.connector.bind_kv_cache_manager(self.kv_cache_manager)

        self.use_pp = self.parallel_config.pipeline_parallel_size > 1
        self.use_v2_model_runner = vllm_config.use_v2_model_runner
        # Scheduler iteration counter. Drives the V2+PP+async decode-throttle
        # cadence (`next_decode_eligible_step`).
        self.current_step = 0
        # DP prefill balancing: Flag to track whether the last cadence-aligned
        # prefill batch fully drained the waiting queue. Prefill throttling
        # is disabled in this case.
        self.prefill_capacity_bound = False
        # The DP engine core drives this cadence from a counter shared across
        # ranks; an engine without one never throttles, so apply the interval
        # locally, timed from the last prefill-carrying step. Three regimes:
        #   1. no DP -- local cadence applies;
        #   2. dense DP rank -- `reconfigure_for_independent_dp_rank` already
        #      set data_parallel_size=1, so each rank gets its own cadence.
        #      Intended, but a behaviour change: this used to be a no-op;
        #   3. MoE DP rank (size > 1) -- the engine core drives it, no-op here.
        self.local_prefill_interval = (
            self.scheduler_config.prefill_schedule_interval
            if self.parallel_config.data_parallel_size == 1
            else 1
        )
        if self.local_prefill_interval > 1:
            # Neither the hold nor its release is otherwise visible in logs or
            # stats, which makes a misapplied cadence hard to diagnose.
            logger.info_once(
                "Prefill cadence: applying prefill_schedule_interval=%d "
                "locally (this engine is not DP-coordinated); prefill is held "
                "until %d executed steps have passed since the last "
                "prefill-carrying step.",
                self.local_prefill_interval,
                self.local_prefill_interval,
            )
        # A full interval back, so the first step is never gated.
        self.last_prefill_step = -self.local_prefill_interval
        # Steps that actually scheduled tokens. `current_step` counts every
        # schedule() call including empty ones, so it would expire the hold
        # early; it keeps its own meaning (next_decode_eligible_step).
        self.num_executed_steps = 0
        self.scheduler_reserve_full_isl = (
            self.scheduler_config.scheduler_reserve_full_isl
        )

        self.has_mamba_layers = kv_cache_config.has_mamba_layers
        self.needs_kv_cache_zeroing = kv_cache_config.needs_kv_cache_zeroing
        self.need_mamba_block_aligned_split = (
            self.has_mamba_layers and self.cache_config.mamba_cache_mode == "align"
        )
        # TODO: Support models with multiple Mamba specs that require different
        # prefill checkpoint alignments instead of selecting the first one.
        self.mamba_prefill_checkpoint_alignment = next(
            (
                group.kv_cache_spec.prefill_checkpoint_alignment
                for group in kv_cache_config.kv_cache_groups
                if isinstance(group.kv_cache_spec, MambaSpec)
            ),
            None,
        )
        self.mamba_has_prefill_checkpoint_blocks = self.has_mamba_layers and all(
            not isinstance(group.kv_cache_spec, MambaSpec)
            or group.kv_cache_spec.num_prefill_checkpoint_blocks > 0
            for group in kv_cache_config.kv_cache_groups
        )
        # Fine-grained hits reuse the prompt's hash-aligned Mamba checkpoint.
        # Split there only if the backend cannot save it within the final chunk.
        self.mamba_partial_cache_hit = (
            self.need_mamba_block_aligned_split
            and self.hash_block_size < self.block_size
            and self.kv_cache_manager.coordinator.enable_partial_hash_hits
        )
        # Opt-in: also stop at the junction, where an eagle sibling resumes. The
        # manager decides whether it can check-point there (per-group eagle bit,
        # no MTP re-prefill tail); splitting for a stop it would refuse costs a
        # forward pass and displaces the block-boundary stop.
        self.mamba_shared_prefix_checkpoint = (
            self.mamba_partial_cache_hit
            and self.kv_cache_manager.mamba_shared_prefix_checkpoint
        )

        # Counts of non-empty steps scheduled / processed. update_from_output
        # is called once per scheduled step in FIFO order, so these stay in sync.
        self.sched_step_seq = 0
        self.processed_step_seq = 0
        # FIFO of (fence_seq, blocks): blocks become safe to free once
        # processed_step_seq >= fence_seq.
        self.deferred_frees: deque[tuple[int, list[KVCacheBlock]]] = deque()

        self.perf_metrics: ModelMetrics | None = None
        if self.log_stats and vllm_config.observability_config.enable_mfu_metrics:
            self.perf_metrics = ModelMetrics(vllm_config)

        self.aux_output_connector = (
            AuxOutputSchedulerConnector(self.hash_block_size)
            if vllm_config.aux_output_config.enabled
            else None
        )
        self.return_sampling_mask = vllm_config.model_config.return_sampling_mask

        self._pause_state: PauseState = PauseState.UNPAUSED

        # In-flight requests still prefilling (prefill chunks + in-progress
        # async KV loads). Their remaining-block reservation gates async loads.
        self._inflight_prefills: set[Request] = set()

        # Requests with an async KV load, by stage (KV_FETCH_STAGES).
        # None when not tracked (stats disabled or no KV connector).
        self._kv_fetch_stages: dict[Request, str] | None = (
            {} if self.log_stats and self.connector is not None else None
        )
        self._kv_fetch_counts: dict[str, int] = dict.fromkeys(KV_FETCH_STAGES, 0)
```


---


---





================================================================================

### 📁 代表專案 #6: `caddy` (33)

> **生態與抽樣意圖**: 展示雲原生反向代理管線與錯誤守衛之程序式修復證明 (Go)  

> **完整 20-Commit 報告位址**: `reports/per_repo_audits/33_caddy.md`


# 🔬 CODE-Map 基準審查獨立驗證報告: `caddy`
> **技術生態**: `Go (雲原生 Web 伺服器 / 自動 TLS / 重載)`  
> **本地倉庫路徑**: `test_repos/caddy`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 33 Files  
> **報告生成時間**: 2026-10-20 21:44:37  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `22` / `33` | `66.7%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `7` / `33` | `21.2%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `4` / `33` | `12.1%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`29` / `33`** | **`87.9%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `33` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

---

### 📋 精選代表性修復 Commit 形式化證據 (抽樣前 3 項 / 共 20 項)

### 🔹 Commit #01: `612128e3`
- **完整 Hash**: `612128e3b0f290af44649d7a7dcb1111fc3ebb33`
- **說明 (Ground Truth)**: logging: Parse request URIs in the `query` filter like the server does (#8255)
- **變更檔案數**: 1

#### 📄 檔案: `modules/logging/filters.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:91, E:128, A:0) ➔ After(N:92, E:129, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 1, +Edges: 2, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `strings.HasPrefix (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `parse (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `url.Parse (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `QueryFilter.processQueryString` ──[CALLS]──> `strings.HasPrefix (External/Pkg)`
  • + [新增呼叫邊] `QueryFilter.processQueryString` ──[CALLS]──> `parse (External/Pkg)`
  • - [移除呼叫邊] `QueryFilter.processQueryString` ──[CALLS]──> `url.Parse (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `QueryFilter.processQueryString()`
- **變更前簽章 (Before)**: `func QueryFilter.processQueryString(s string)` (L417~L443)
- **變更後簽章 (After)**: `func QueryFilter.processQueryString(s string)` (L417~L451)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (m QueryFilter) processQueryString(s string) string {
	u, err := url.Parse(s)
	if err != nil {
		return s
	}

	q := u.Query()
	for _, a := range m.Actions {
		switch a.Type {
		case replaceAction:
			for i := range q[a.Parameter] {
				q[a.Parameter][i] = a.Value
			}

		case hashAction:
			for i := range q[a.Parameter] {
				q[a.Parameter][i] = hash(q[a.Parameter][i])
			}

		case deleteAction:
			q.Del(a.Parameter)
		}
	}

	u.RawQuery = q.Encode()
	return u.String()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (m QueryFilter) processQueryString(s string) string {
	parse := url.Parse
	if strings.HasPrefix(s, "/") {
		// parse a request-target like the server does. Browsers and most
		// clients strip a #fragment before sending, but a client that
		// sends a raw '#' has it kept in the query by the server
		// (url.ParseRequestURI does not split it off), so filter it too
		parse = url.ParseRequestURI
	}
	u, err := parse(s)
	if err != nil {
		return s
	}

	q := u.Query()
	for _, a := range m.Actions {
		switch a.Type {
		case replaceAction:
			for i := range q[a.Parameter] {
				q[a.Parameter][i] = a.Value
			}

		case hashAction:
			for i := range q[a.Parameter] {
				q[a.Parameter][i] = hash(q[a.Parameter][i])
			}

		case deleteAction:
			q.Del(a.Parameter)
		}
	}

	u.RawQuery = q.Encode()
	return u.String()
}
```


---


---

### 🔹 Commit #02: `872c864c`
- **完整 Hash**: `872c864c200b22dc5161942816be6409eafcb295`
- **說明 (Ground Truth)**: caddytls: skip client cert verifiers when no certificate is presented (#8251)
- **變更檔案數**: 1

#### 📄 檔案: `modules/caddytls/connpolicy.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:102, E:149, A:0) ➔ After(N:102, E:149, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `ClientAuthentication.verifyConnection()`
- **變更前簽章 (Before)**: `func ClientAuthentication.verifyConnection(cs tls.ConnectionState)` (L909~L927)
- **變更後簽章 (After)**: `func ClientAuthentication.verifyConnection(cs tls.ConnectionState)` (L909~L933)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (clientauth *ClientAuthentication) verifyConnection(cs tls.ConnectionState) error {
	rawCerts := make([][]byte, len(cs.PeerCertificates))
	for i, cert := range cs.PeerCertificates {
		rawCerts[i] = cert.Raw
	}

	// first use any pre-existing custom verification function
	if clientauth.existingVerifyPeerCert != nil {
		if err := clientauth.existingVerifyPeerCert(rawCerts, cs.VerifiedChains); err != nil {
			return err
		}
	}
	for _, verifier := range clientauth.verifiers {
		if err := verifier.VerifyClientCertificate(rawCerts, cs.VerifiedChains); err != nil {
			return err
		}
	}
	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (clientauth *ClientAuthentication) verifyConnection(cs tls.ConnectionState) error {
	rawCerts := make([][]byte, len(cs.PeerCertificates))
	for i, cert := range cs.PeerCertificates {
		rawCerts[i] = cert.Raw
	}

	// first use any pre-existing custom verification function
	if clientauth.existingVerifyPeerCert != nil {
		if err := clientauth.existingVerifyPeerCert(rawCerts, cs.VerifiedChains); err != nil {
			return err
		}
	}

	// crypto/tls has already enforced whether the mode requires a
	// certificate, so the verifiers only check one that was presented
	if len(rawCerts) == 0 {
		return nil
	}
	for _, verifier := range clientauth.verifiers {
		if err := verifier.VerifyClientCertificate(rawCerts, cs.VerifiedChains); err != nil {
			return err
		}
	}
	return nil
}
```


---


---

### 🔹 Commit #03: `1619352f`
- **完整 Hash**: `1619352f4e36d2c7dfab6d9e793f8495d7b36993`
- **說明 (Ground Truth)**: ci: fix exhaustive linting (#8238)
- **變更檔案數**: 3

#### 📄 檔案: `context.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:122, E:137, A:0) ➔ After(N:122, E:137, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `modules/caddyhttp/responsewriter.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:50, E:44, A:0) ➔ After(N:50, E:44, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `service_windows.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:10, E:8, A:0) ➔ After(N:10, E:8, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---


---



