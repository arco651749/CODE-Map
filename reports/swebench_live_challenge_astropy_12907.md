# 🏆 CODE-Map 實戰盲測 SWE-bench Verified 官方題庫全紀錄
## 挑戰題號：`astropy__astropy-12907`（零全檔讀取、兩步因果定位、100% Exact Match 一刀修復）

> **資料集來源**：HuggingFace [`princeton-nlp/SWE-bench_Verified`](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified) (Split: `test`, Row `#0`)  
> **目標開源專案**：`astropy/astropy`  
> **基準 Commit (Base Commit)**：`d16bfe05a744909de4b27f5875fe0d4ed41ce607`  
> **測試目標**：在**不開啟 LSP、不讀取整支檔案、事先封存官方標準答案 (`patch`)** 的盲測條件下，僅憑 GitHub Issue 描述與 **CODE-Map `--locate` 雙向病灶切片器**，定位並修復 Bug，最後與人類原作者 PR 比對是否一致。

---

## 📜 第一步：原始題目輸入（GitHub Issue `problem_statement`）

以下為 SWE-bench Verified 官方題庫提供的唯一題目描述：

```markdown
Modeling's `separability_matrix` does not compute separability correctly for nested CompoundModels

Consider the following model:
>>> from astropy.modeling import models as m
>>> from astropy.modeling.separable import separability_matrix
>>> cm = m.Linear1D(10) & m.Linear1D(5)

It's separability matrix as you might expect is a diagonal:
>>> separability_matrix(cm)
array([[ True, False],
       [False,  True]])

If I make the model more complex:
>>> separability_matrix(m.Pix2Sky_TAN() & m.Linear1D(10) & m.Linear1D(5))
array([[ True,  True, False, False],
       [ True,  True, False, False],
       [False, False,  True, False],
       [False, False, False,  True]])

If however, I nest these compound models:
>>> separability_matrix(m.Pix2Sky_TAN() & cm)
array([[ True,  True, False, False],
       [ True,  True, False, False],
       [False, False,  True,  True],
       [False, False,  True,  True]])
Suddenly the inputs and outputs are no longer separable?
```

---

## 🧭 第二步：CODE-Map 兩步雙向因果定位（0 全檔盲讀）

傳統 Agent 面對此題會直接讀取整支 `astropy/modeling/separable.py`（315 行、9,878 bytes）與 `core.py`（數千行）。  
而我們嚴格遵循 **CODE-Map 反顛簸協議**，只從 Issue 提到的唯一入口符號 `separability_matrix` 出發：

### 🔹 第 1 刀：定位入口函式 `--locate "separability_matrix"`
執行指令：
```powershell
python.exe -X utf8 codemap.py --file "astropy/modeling/separable.py" --locate "separability_matrix"
```

**CODE-Map 輸出之雙向病灶拓撲與源碼切片**：
```text
## 🧭 病灶拓撲視圖: `separability_matrix`
  • ⬆️ [上游呼叫者 Caller] _(頂層入口或外部路由觸發)_ ──> 🎯 **`separability_matrix`**
  • ⬇️ [下游被調用 Callee] 🎯 **`separability_matrix`** ──[CALLS]──> `_separable`
```
```python
# 🔗 [上下游關聯 NEIGHBOR] def _separable(transform) (L290~L311)
def _separable(transform):
    if (transform_matrix := transform._calculate_separability_matrix()) is not NotImplemented:
        return transform_matrix
    elif isinstance(transform, CompoundModel):
        sepleft = _separable(transform.left)
        sepright = _separable(transform.right)
        return _operators[transform.op](sepleft, sepright)
    elif isinstance(transform, Model):
        return _coord_matrix(transform, 'left', transform.n_outputs)
```
> 💡 **因果推論**：从 `_separable` 可見，當模型為 `CompoundModel` 時，會遞迴計算 `sepleft` 與 `sepright`（型別為 `ndarray` 矩陣），再交由 `&` 運算子對應的函式 `_cstack(sepleft, sepright)` 合併！

---

### 🔹 第 2 刀：順著呼叫鏈定位 `--locate "_cstack"`
執行指令：
```powershell
python.exe -X utf8 codemap.py --file "astropy/modeling/separable.py" --locate "_cstack"
```

**CODE-Map 輸出之目標病灶切片（L219~L247，僅 28 行）**：
```text
## 🧭 病灶拓撲視圖: `_cstack`
  • ⬆️ [上游呼叫者 Caller] _(頂層入口或外部路由觸發)_ ──> 🎯 **`_cstack`**
  • ⬇️ [下游被調用 Callee] 🎯 **`_cstack`** ──[CALLS]──> `_compute_n_outputs`
  • ⬇️ [下游被調用 Callee] 🎯 **`_cstack`** ──[CALLS]──> `_coord_matrix`
```
```python
# 🎯 [目標病灶 TARGET] def _cstack(left, right) (L219~L247)
def _cstack(left, right):
    noutp = _compute_n_outputs(left, right)

    if isinstance(left, Model):
        cleft = _coord_matrix(left, 'left', noutp)
    else:
        cleft = np.zeros((noutp, left.shape[1]))
        cleft[: left.shape[0], : left.shape[1]] = left
    if isinstance(right, Model):
        cright = _coord_matrix(right, 'right', noutp)
    else:
        cright = np.zeros((noutp, right.shape[1]))
        cright[-right.shape[0]:, -right.shape[1]:] = 1   # 💥 當場抓獲 Bug 根因！

    return np.hstack([cleft, cright])
```

> 🔍 **根因一秒破案**：
> - 當 `left` 不是單一 `Model`（而是嵌套 `CompoundModel` 傳入的 `ndarray` 矩陣）時，第 239 行正確寫道：`cleft[: left.shape[0], : left.shape[1]] = left`。
> - 當 `right` 是嵌套 `CompoundModel` 傳入的 `ndarray` 對角矩陣 `[[1, 0], [0, 1]]` 時，第 244 行卻誤寫成常數 `= 1`，導致右下角整個區塊被強制填滿 `1`（即 `[[True, True], [True, True]]`）！

---

## 🛠️ 第三步：微創手術式修補與 CODE-Map 形式化驗收

我們僅針對 `_cstack` 第 244 行進行單行微創替換（`edit_file`），並透過 `CodeMapDiffer` 執行形式化驗收：

```text
🌲 UIA 語意控制樹變更差分 (Semantic UIA-Diff):
---
  _無任何 UI 控制項變更_

🛡️ 形式化守衛狀態遷移 (Invariant Transitions):
  • _無狀態躍遷變動_

最終驗收裁決: 🟢 READY_TO_SHIP

## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)
### 🔹 函式: `_cstack()`
- 變更前簽章 (Before): `def _cstack(left, right)` (L219~L247)
- 變更後簽章 (After):  `def _cstack(left, right)` (L219~L247)
```

---

## 🎯 第四步：揭曉 SWE-bench Verified 官方標準答案對決

將我們產出的 Patch 與事先封存於 HuggingFace 資料集的官方人類作者 PR (`row["patch"]`) 進行逐字比對：

### ▶ 我們的微創補丁 (Our Surgical Patch):
```diff
--- a/astropy/modeling/separable.py
+++ b/astropy/modeling/separable.py
@@ -242,7 +242,7 @@ def _cstack(left, right):
         cright = _coord_matrix(right, 'right', noutp)
     else:
         cright = np.zeros((noutp, right.shape[1]))
-        cright[-right.shape[0]:, -right.shape[1]:] = 1
+        cright[-right.shape[0]:, -right.shape[1]:] = right
 
     return np.hstack([cleft, cright])
```

### ▶ SWE-bench Verified 官方標準答案 (Official Ground Truth Patch):
```diff
diff --git a/astropy/modeling/separable.py b/astropy/modeling/separable.py
--- a/astropy/modeling/separable.py
+++ b/astropy/modeling/separable.py
@@ -242,7 +242,7 @@ def _cstack(left, right):
         cright = _coord_matrix(right, 'right', noutp)
     else:
         cright = np.zeros((noutp, right.shape[1]))
-        cright[-right.shape[0]:, -right.shape[1]:] = 1
+        cright[-right.shape[0]:, -right.shape[1]:] = right
 
     return np.hstack([cleft, cright])
```

> 🏆 **最終裁決**：**100% Exact Match（檔案、行號 L242、修改字元與官方答案一字不差完全命中）！**
