# 🛠️ CODE-Map 靜態分析與差分引擎：Phase 2 核心修復與升級 TODO List (v2.1)

> **文檔目標**：供 **Gemini 3.8**（或另一台 Antigravity Agent）直接讀取並無縫執行底層修復與架構升級。  
> **核心背景**：在完成 Phase 1（`SpecVerifier`、跨檔 `WorkspaceGraphBuilder`、35 專案 693 Commits 全景基準審查）後，經由「資深靜態分析架構師與編譯器專家（Principal Static Analysis & Compiler Architect）」對 `reports/EXTERNAL_MODEL_REVIEW_PACK.md` 進行嚴格 Red-Team Audit，定位出 **6 個影響形式化驗收公信力的關鍵問題**：
> 1. **閉包作用域斷鏈誤報**：JS/TS Adapter 階段 1 與階段 2 的 Scope ID 不一致，將定義在 `scope:global` 的模組私有函式誤判為 `BLOCKED_SCOPE`（如 `Sortable` 與 `Preact`）。
> 2. **純註釋與純型別變更滲漏**：函式變更檢測直接比對 `source_code` 字串，導致僅加一行 `//exhaustive:ignore` 註釋（如 `Caddy` Commit #03）或僅改 Type Annotation（如 `vLLM` Commit #02）被灌水進 `BODY_LEVEL_SEMANTIC_DELTA`。
> 3. **歷史技術債連坐處罰**：Commit Diff 的驗收裁決直接讀取 `invariants_after`，未扣除 `invariants_before` 已存在的舊違規，且同一違規按呼叫點重複印出 10~20 次。
> 4. **非 UI 後端專案的 Widget 命名幻覺**：Python Adapter 對任何 `on_xxx_yyy` 命名的方法無條件拆解為 Textual UI 控制項，導致 `vLLM` 的 `MooncakeConnector.on_new_request()` 被幻覺為 `🌲 #new (Widget) -> ⚡ on('request')`。
> 5. **多行型別簽章截斷與非 UI 圖譜差分空白**：Python/TS 函式簽章用 `split(":")[0]` 擷取導致在第一個參數型別冒號處斷開；且無 UI Anchor 的後端專案在 `STRUCTURAL_GRAPH_DELTA` 時未列出新增/移除的具體節點與呼叫邊。
> 6. **頂層常數與映射表漏報**：模組頂層（Module-Scope）常數字典或映射表修改（如 `Preact` Commit #13 `compat/src/render.js`）因不在 `FUNCTION_DEF` 內而被漏判為 `ZERO_DELTA`。

---

## 📋 Phase 2 任務總覽與執行優先級 (Execution Checklist for Gemini 3.8)

- [x] **Task P0-1 (消滅閉包誤報)**：修復 `javascript_adapter.py` 與 `typescript_adapter.py` 階段 1 / 階段 2 的 Scope 追蹤斷鏈與 `scope:global` 誤判，徹底解決 `Sortable` 與 `Preact` 的 `BLOCKED_SCOPE` 假陽性。
- [x] **Task P0-2 (AST 語意去噪比對)**：在 `base_adapter.py` 與 `differ.py` 實作 `extract_executable_tokens()`（剝除 AST 中的 `comment` 與純 `type_annotation` 節點），杜絕註釋微調（如 `Caddy` `//exhaustive:ignore`）滲漏至 `BODY_LEVEL_SEMANTIC_DELTA`。
- [x] **Task P0-3 (差分不變量守衛與去重)**：在 `graph.py` 與 `differ.py` 實作違規去重（Deduplication）與 **Differential Invariant Verification**（僅當本次 Commit **新引入** 違規時才判為 `🔴 BLOCKED_BY_INVARIANTS`，既有違規標示為 `ℹ️ PRE_EXISTING_DEBT`）。
- [x] **Task P1-1 (拔除後端專案 UI 幻覺)**：在 `python_adapter.py` 增加 UI 框架上下文守衛（檢查 `imports` 或 Base Classes），禁止在 `vLLM`、`FastAPI` 等純後端專案上將 `on_new_request` 拆解為 `#new (Widget)`。
- [x] **Task P1-2 (修復簽章截斷 + 輸出結構差分明細)**：修復 `python_adapter.py` 等處的 `split(":")[0]` 簽章截斷問題；並在 `differ.py` 的 `to_diff_markdown()` 中為無 UI 錨點的專案輸出 `+Nodes / -Nodes / +Edges / -Edges` 的具體符號明細。
- [x] **Task P2-1 (納管頂層常數狀態 `MODULE_STATE`)**：在 `graph.py`、各語言 Adapter 與 `differ.py` 中新增對頂層常數/查找表 (`MODULE_STATE`) 的追蹤與差分，捕獲如 `Preact` Commit #13 的頂層映射表修復。

---

## 🔥 Task P0-1：修復 JS/TS 閉包作用域斷鏈與 `scope:global` 誤判

### 1. 問題根因定位 (Root Cause)
* **檔案位置**：
  * [`uia_coder/adapters/javascript_adapter.py`](file:///d:/AntiGravity/UIA_Coder/uia_coder/adapters/javascript_adapter.py#L287-L348)
  * [`uia_coder/adapters/typescript_adapter.py`](file:///d:/AntiGravity/UIA_Coder/uia_coder/adapters/typescript_adapter.py)
* **Bug 解剖**：
  1. 在階段 1 `_collect_scopes_and_functions` (L287~L348) 走訪 `assignment_expression`（例如 `Sortable.prototype = { ... }` 或 `_onDragStart = function() {}`）時，建立了 `new_scope_id = f"scope:{method_name}@{file_path}:L{start_line}C{start_col}"`，且 `scopes[new_scope_id]` 的字典有時漏設 `"parent": current_scope_id`（見 L306~L312、L361~L367，**漏寫了 `"parent": current_scope_id`！**）。
  2. 在階段 2 `_wire_ui_and_calls` (L418~L440) 中，沒有 `assignment_expression` 的對應 Scope 切換分支，導致階段 2 查詢 `scopes.get(curr, {}).get("parent")` 時拿到 `None`，作用域向上查找鏈當場斷裂！
  3. 當向上查找失敗後，程式進入 [`javascript_adapter.py`](file:///d:/AntiGravity/UIA_Coder/uia_coder/adapters/javascript_adapter.py#L824-L846) 的 `else` 分支掃描全表 `scopes.items()`，把明明定義在 `scope:global`（頂層模組作用域，對檔案內所有函式 100% 可達）的私有輔助函式（如 `_dispatchEvent`, `pluginEvent`, `closest`, `enqueueRender`）當成 `isolated_def`，印出矛盾的錯誤訊息：
     `💥 作用域阻隔: 函式 'pluginEvent' 被深鎖在內部閉包 (scope:global)，外部無法調用！`

### 2. 修改規格 (Implementation Spec)
1. **補齊 `"parent": current_scope_id`**：
   檢查 `javascript_adapter.py` (特別是 L306~L312 的 `assignment_expression` 與 L361~L367 的 `method_definition` / `pair`) 以及 `typescript_adapter.py` 中所有建立 `scopes[new_scope_id] = { ... }` 的地方，確保**每一個 Scope 字典都包含 `"parent": current_scope_id`**。
2. **使用 `node_scope_map: Dict[int, str]` 統一階段 1 與階段 2 的 Scope ID**：
   在 `parse_and_build` 中初始化 `node_scope_map: Dict[int, str] = {}`。在階段 1 `_collect_scopes_and_functions` 決定 `next_scope_id` 後，記錄 `node_scope_map[node.id] = next_scope_id`；在階段 2 `_wire_ui_and_calls` 直接以 `next_scope_id = node_scope_map.get(node.id, current_scope_id)` 取得，消除兩階段手動拼湊字串不一致的問題。
3. **頂層與祖先作用域安全防呆**：
   在 `_link_handler_with_reachability` 中，若全域掃描找到的 `isolated_scope_id == "scope:global"`（代表目標函式定義於模組頂層），則該呼叫在詞法作用域上必然可達，**必須走 `status="VALID"` 分支**，絕不可標記為 `BLOCKED_SCOPE`。

---

## 🔥 Task P0-2：實作「正規化 AST 可執行 Token 指紋」，消除註釋與純型別變更滲漏

### 1. 問題根因定位 (Root Cause)
* **檔案位置**：
  * [`uia_coder/core/differ.py`](file:///d:/AntiGravity/UIA_Coder/uia_coder/core/differ.py#L355-L378)
  * [`uia_coder/core/base_adapter.py`](file:///d:/AntiGravity/UIA_Coder/uia_coder/core/base_adapter.py)
* **Bug 解剖**：
  `differ.py` 第 364~366 行直接用 `src_b != src_a`（原始碼字串比對）判定函式是否發生實作變更。這導致：
  * `Caddy` Commit #03 (`1619352f`) 在 3 個 `.go` 檔案的 `switch` 前各加了一行 `//exhaustive:ignore` 註釋，被算進 `BODY_LEVEL_SEMANTIC_DELTA` (`ΔFuncs: 1`)。
  * `vLLM` Commit #02 (`143ee3b4`) 在 `_validate_step5_dsa_attention_contract` 僅修改參數型別標註 `alibi_slopes: list[float] | torch.Tensor | None`，也被算進 `BODY_LEVEL_SEMANTIC_DELTA`。

### 2. 修改規格 (Implementation Spec)
1. **在 `BaseUIAGraphBuilder` (`uia_coder/core/base_adapter.py`) 新增 `compute_executable_fingerprint(node: Any) -> str`**：
   * 撰寫一個遞迴或 Stack 走訪 Tree-sitter `node` 的輔助方法，收集所有葉節點（Leaf Nodes，`len(curr.children) == 0`）的 Token 文字，但**跳過（Skip）以下非執行語意子樹**：
     * 節點 `type` 包含 `"comment"`（如 `comment`, `line_comment`, `block_comment`）。
     * 純型別標註節點：`type` 為 `"type_annotation"`, `"type_arguments"`, `"type_parameters"`, `"type_parameter"`, `"return_type"`, `"generic_type"`，或父節點欄位為 `type`（如 Python `typed_parameter` / `typed_default_parameter` 的 `type` 子節點）。
     * Python 函式 `body` (`block`) 的第一個子節點若為純字串常數（Docstring），予以跳過。
   * 將收集到的可執行葉節點 Token 以空白串接並計算 SHA-256 或正規化字串，存入函式節點 `props["executable_fingerprint"]`。
2. **在 6 大語言 Adapter 建立 `FUNCTION_DEF` 節點時**：
   呼叫 `self.compute_executable_fingerprint(func_node)` 並寫入 `props["executable_fingerprint"]`。
3. **在 `UIAGraphDiffer.diff_graphs` (`uia_coder/core/differ.py` L364~L366)**：
   ```python
   fp_b = props_b.get("executable_fingerprint")
   fp_a = props_a.get("executable_fingerprint")
   is_modified = (fp_b != fp_a) if (fp_b is not None and fp_a is not None) else (src_b != src_a)
   if src_b and src_a and is_modified:
       # 列入 functions_modified
   ```

---

## 🔥 Task P0-3：實作「差分不變量守衛 (Differential Invariants)」與違規去重

### 1. 問題根因定位 (Root Cause)
* **檔案位置**：
  * [`uia_coder/core/graph.py`](file:///d:/AntiGravity/UIA_Coder/uia_coder/core/graph.py#L196-L251)
  * [`uia_coder/core/differ.py`](file:///d:/AntiGravity/UIA_Coder/uia_coder/core/differ.py#L98-L164)
* **Bug 解剖**：
  1. `graph.py` 的 `check_invariants()` 在遍歷邊與節點時未去重，且對於 `panic()` 既在邊上觸發一次 `INVARIANT_VIOLATION`（`呼叫了執行期恐慌中斷常式: panic()`），又在節點上因為 `is_blocking: True` 觸發一次 `BLOCKING_API`（`使用了同步阻塞 API (panic())`），導致 Caddy 單一檔案印出 20 行重複警告。
  2. `differ.py` 的 `UIAGraphDiffResult.passed` 直接回傳 `self.invariants_after["passed"]`。如果一個舊檔案原本就有 `panic()`，任何修改該檔案的 Commit 都會被無差別攔截為 `🔴 BLOCKED_BY_INVARIANTS`。

### 2. 修改規格 (Implementation Spec)
1. **在 `graph.py` 的 `check_invariants()` 進行去重與分類修正**：
   * 若節點已在邊的 `BLOCKED_INVARIANT` 中被報告過，不再於節點迴圈重複報告第二次；或針對 `panic()` 將其 `props["is_blocking"]` 改為 `props["is_abrupt_exit"] = True`，避免同一顆 `panic()` 節點產生兩條不同名目的警告。
   * 對 `scope_errors` 與 `hazards` 以 `(item.get("caller", ""), item.get("target", item.get("label", "")), item.get("detail", ""))` 去重，若重複出現則統計次數 `count`（如 `(共 5 處呼叫)`）。
2. **在 `differ.py` 的 `UIAGraphDiffResult` 實作差分守衛**：
   * 比對 `invariants_before` 與 `invariants_after`（以正規化後的 `(target_label, detail)` 為比對鍵）：
     * **`new_scope_errors` / `new_hazards`**：在 `after` 出現、但不在 `before` 中的新增違規（或同類違規數量增加）。
     * **`pre_existing_scope_errors` / `pre_existing_hazards`**：在 `before` 與 `after` 中皆存在的既有違規。
   * 修改 `passed` 與 `verdict` 屬性：
     * 僅當 `len(new_scope_errors) > 0 or len(new_hazards) > 0` 時，`passed = False`，`verdict = "🔴 BLOCKED_BY_INVARIANTS"`。
     * 若無新增違規（即使有存量舊違規），`passed = True`，`verdict = "🟢 READY_TO_SHIP"`（並在 `to_diff_markdown()` 中以單行摘要顯示：`ℹ️ 存量環境提醒: 檔案內含 N 項既有非阻塞提醒 (非本次 Commit 引入)`）。

---

## 🛠️ Task P1-1：拔除 Python 後端專案的 Textual UI 命名幻覺

### 1. 問題根因定位 (Root Cause)
* **檔案位置**：[`uia_coder/adapters/python_adapter.py`](file:///d:/AntiGravity/UIA_Coder/uia_coder/adapters/python_adapter.py#L308-L362)
* **Bug 解剖**：
  `_handle_textual_event_bindings` (L351) 只要看到任何 Python 方法名稱符合 `func_name.startswith("on_")` 且 `len(parts) >= 3`，就無條件將 `parts[1]` 當成 UI Widget 控制項（如 `vLLM` 的 `on_new_request` 被拆成 `#new (Widget)` 與 `on('request')`）。

### 2. 修改規格 (Implementation Spec)
1. 在 `PythonUIAGraphBuilder.parse_and_build` 開始時，先檢查 `source_code` 是否包含 UI 框架特徵：
   ```python
   ui_keywords = ("textual", "PyQt", "PySide", "tkinter", "ttk", "wx", "kivy", "flet", "customtkinter")
   has_ui_import = any(kw in source_code for kw in ui_keywords)
   ```
   並將 `has_ui_import` 存入實例屬性或傳遞給 `_wire_ui_and_calls`。
2. 在 `_handle_textual_event_bindings` 中：
   * 裝飾器 `@on(...)` 檢查維持不變。
   * 命名約定 `if not event_name and func_name.startswith("on_"):` **必須加上守衛 `and self._has_ui_import`**，確保在 `vLLM`, `FastAPI`, `HTTPX`, `Pydantic` 等純後端專案中不會憑空捏造 `#new (Widget)` 控制項！

---

## 🛠️ Task P1-2：修復多行函式簽章截斷 Bug，並輸出非 UI 結構差分明細

### 1. 問題根因定位 (Root Cause)
* **檔案位置**：
  * [`uia_coder/adapters/python_adapter.py`](file:///d:/AntiGravity/UIA_Coder/uia_coder/adapters/python_adapter.py#L147)
  * [`uia_coder/core/differ.py`](file:///d:/AntiGravity/UIA_Coder/uia_coder/core/differ.py#L112-L164)
* **Bug 解剖**：
  1. `python_adapter.py` L147 使用 `sig_text = full_text.split(":")[0].strip()` 提取簽章。當函式有參數型別註解（如 `def _get_multidict_value(field: ModelField, ...)`）時，會在第一個參數的 `:` 處被腰斬！
  2. `differ.py` 的 `to_diff_markdown()` 只渲染 `get_ui_anchors()`。當 `Ratatui`、`FastAPI`、`Caddy` 發生 `STRUCTURAL_GRAPH_DELTA`（如 `+Nodes: 7, +Edges: 16`）但檔案內無 UI 控制項時，報告只印出 `_無任何 UI 控制項變更_`，完全看不出新增或刪除了哪 7 個節點與 16 條邊。

### 2. 修改規格 (Implementation Spec)
1. **精確提取函式簽章（利用 AST `body` 節點邊界）**：
   在 `python_adapter.py` L147（並同步檢查 `typescript_adapter.py`, `rust_adapter.py`, `go_adapter.py`, `csharp_adapter.py`）：
   ```python
   body_node = node.child_by_field_name("body")
   if body_node:
       header_bytes = node.text[: body_node.start_byte - node.start_byte]
       sig_text = " ".join(header_bytes.decode("utf-8", errors="replace").strip().rstrip(":").split())
   else:
       sig_text = " ".join(full_text.split("\n")[0].strip().rstrip(":").split())
   ```
2. **在 `differ.py` 的 `to_diff_markdown()` 補充結構拓樸差分明細**：
   當 `self.nodes_added`、`self.nodes_removed`、`self.edges_added` 或 `self.edges_removed` 非空時，在 `to_diff_markdown()` 中增加 `🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**` 區塊，列出（最多前 15 項，超出則摺疊顯示 `... 等共 N 項`）：
   * `+ [新增節點] {node_canon_id}` / `- [移除節點] {node_canon_id}`
   * `+ [新增呼叫邊] {u} ──[{edge_type}{guard_info}]──> {v}`
   * `- [移除呼叫邊] {u} ──[{edge_type}]──> {v}`

---

## 🛠️ Task P2-1：納管模組頂層常數與查找表變更 (`MODULE_STATE`)

### 1. 問題根因定位 (Root Cause)
* **檔案位置**：
  * [`uia_coder/core/graph.py`](file:///d:/AntiGravity/UIA_Coder/uia_coder/core/graph.py#L17-L24)
  * `uia_coder/adapters/*.py`
  * [`uia_coder/core/differ.py`](file:///d:/AntiGravity/UIA_Coder/uia_coder/core/differ.py#L354-L379)
* **Bug 解剖**：
  在 `Preact` Commit #13 (`4cb4f809`, `compat/src/render.js`) 中，開發者修改了模組頂層（Module-Scope）的常數/正則表達式映射表。因為該變更不在任何 `FUNCTION_DEF` 內，也未改變呼叫邊，導致被漏判為 `ZERO_DELTA`。

### 2. 修改規格 (Implementation Spec)
1. 在 `UIACodeGraph.CATEGORIES` (`graph.py`) 加入 `"MODULE_STATE"`。
2. 在 JS/TS/Python/Go/Rust Adapter 中，當處於頂層作用域 (`current_scope_id == "scope:global"`) 且遇到頂層常數/變數宣告（如 JS/TS 的 `lexical_declaration` / `variable_declaration`、Python 的頂層 `assignment`、Rust 的 `const_item` / `static_item`、Go 的 `const_declaration` / `var_declaration`），若其右側值不是函式定義，則建立一個 `category="MODULE_STATE"` 節點（包含 `label`, `source_code`, `executable_fingerprint`, `line_start`, `line_end`）。
3. 在 `differ.py` L356 的實作變更檢測中，將 `cid.startswith(("FUNCTION_DEF:", "MODULE_STATE:"))` 一併納入比對。若頂層常數的 `executable_fingerprint` 發生實質變更，同樣記入 `functions_modified`（可標註簽章為 `[Module State] {label}`），使其正確歸入 `BODY_LEVEL_SEMANTIC_DELTA`。

---

## ✅ 最終驗收與重跑指令 (Verification & Regeneration Commands)

請 Gemini 3.8 在完成上述所有程式碼修改後，依序執行以下指令完成閉環驗收：

```powershell
# Step 1: 執行所有既有與新增的單元測試，確保 100% 通過
python.exe -X utf8 -m unittest discover -s tests

# Step 2: 重新生成 35 個開源專案的獨立形式化審查報告與 INDEX.md
python.exe -X utf8 tools/generate_all_35_repo_verification_reports.py

# Step 3: 重新打包單一自包含外部模型審查封包 (EXTERNAL_MODEL_REVIEW_PACK.md)
python.exe -X utf8 tools/build_review_pack.py
```

### 🎯 驗收必檢指標 (Acceptance Criteria)：
1. **檢查 `Sortable` (`03_Sortable.md`) 與 `Preact` (`12_preact.md`)**：
   不再出現 `函式 'xxx' 被深鎖在內部閉包 (scope:global)` 的假陽性錯誤，且 `Preact` Commit #13 (`4cb4f809`) 成功由 `ZERO_DELTA` 轉為 `BODY_LEVEL_SEMANTIC_DELTA`。
2. **檢查 `Caddy` (`33_caddy.md`) Commit #03 (`1619352f`)**：
   僅新增 `//exhaustive:ignore` 註釋的 3 個檔案（`context.go`, `responsewriter.go`, `service_windows.go`）正確歸類為 `ZERO_DELTA`，且 `context.go` 不再因既有 `panic()` 而被判為 `🔴 BLOCKED_BY_INVARIANTS` 或重複印出 20 行相同警告。
3. **檢查 `vLLM` (`29_vllm.md`) Commit #01 (`34ac4f96`) 與 Commit #02 (`143ee3b4`)**：
   Commit #01 不再出現 `#new (Widget)` 幻覺控制項；Commit #02 中純修改型別註解的 `_validate_step5_dsa_attention_contract` 不再被誤算為實作變動。
4. **檢查 `FastAPI` (`14_fastapi.md`)**：
   `_get_multidict_value` 與 `_extract_form_body` 的變更前後簽章完整顯示所有參數與回傳型別，不再於第一個 `:` 處截斷；且 `STRUCTURAL_GRAPH_DELTA` 區塊能清楚看到新增/移除的節點與呼叫邊明細。

---

## 📜 附錄：Phase 1 已完成項目留存紀錄 (Completed in Phase 1)
- [x] **Phase 1 - Task 1**：新增 `uia_coder/core/spec_verifier.py` (`SpecVerifier` 路徑可達性與 LCA 拓樸偏序驗收)。
- [x] **Phase 1 - Task 2A/2B**：`differ.py` `get_canonical_id()` 詞法作用域路徑防碰撞，以及 `base_adapter.py` `_inspect_control_context()` 條件分支與 Early-Return 守衛識別。
- [x] **Phase 1 - Task 3**：新增 `uia_coder/core/workspace_graph.py` (`WorkspaceGraphBuilder` 跨檔 `import`/`export` 符號消解)。
- [x] **Phase 1 - Task 4A/4B**：`verify_objection_evidence()` 異議防偽查核與 35 專案雙軌指標分離。
