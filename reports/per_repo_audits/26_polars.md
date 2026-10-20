# 🔬 CODE-Map 基準審查獨立驗證報告: `polars`
> **技術生態**: `Rust (DataFrame / Arrow / 平行 Rayon)`  
> **本地倉庫路徑**: `test_repos/polars`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 33 Files  
> **報告生成時間**: 2026-10-20 21:43:38  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `27` / `33` | `81.8%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `3` / `33` | `9.1%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `3` / `33` | `9.1%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`30` / `33`** | **`90.9%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `33` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `c99202aa`
- **完整 Hash**: `c99202aac2eaf89bbda8aaeb25a9c4587bf27692`
- **說明 (Ground Truth)**: fix!: Disallow mixed string <=> numeric arithmetic in eager (#30071)
- **變更檔案數**: 2

#### 📄 檔案: `crates/polars-core/src/series/arithmetic/borrowed.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:244, E:353, A:0) ➔ After(N:246, E:358, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 5, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `dt.is_decimal (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `dt.is_primitive_numeric (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `coerce_lhs_rhs_numeric_op` ──[CALLS]──> `lhs.dtype (External/Unresolved)`
  • + [新增呼叫邊] `coerce_lhs_rhs_numeric_op` ──[CALLS]──> `rhs.dtype (External/Unresolved)`
  • + [新增呼叫邊] `coerce_lhs_rhs_numeric_op` ──[CALLS]──> `dt.is_primitive_numeric (External/Unresolved)`
  • + [新增呼叫邊] `coerce_lhs_rhs_numeric_op` ──[CALLS]──> `dt.is_decimal (External/Unresolved)`
  • + [新增呼叫邊] `coerce_lhs_rhs_numeric_op` ──[CALLS]──> `polars_ensure! (Macro)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `coerce_lhs_rhs_numeric_op()`
- **變更前簽章 (Before)**: `fn coerce_lhs_rhs_numeric_op(
    lhs: &'a Series,
    rhs: &'a Series,
)` (L418~L427)
- **變更後簽章 (After)**: `fn coerce_lhs_rhs_numeric_op(
    lhs: &'a Series,
    rhs: &'a Series,
)` (L419~L436)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn coerce_lhs_rhs_numeric_op<'a>(
    lhs: &'a Series,
    rhs: &'a Series,
) -> PolarsResult<(Cow<'a, Series>, Cow<'a, Series>)> {
    #[cfg(feature = "dtype-decimal")]
    if let Some(out) = decimal_op_operands(lhs, rhs) {
        return out;
    }
    coerce_lhs_rhs(lhs, rhs)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn coerce_lhs_rhs_numeric_op<'a>(
    lhs: &'a Series,
    rhs: &'a Series,
) -> PolarsResult<(Cow<'a, Series>, Cow<'a, Series>)> {
    // String is a supertype of the numeric types, but they must not be mixed in arithmetic.
    let (l, r) = (lhs.dtype(), rhs.dtype());
    let is_numeric = |dt: &DataType| dt.is_primitive_numeric() || dt.is_decimal();
    polars_ensure!(
        !((l.is_string() && is_numeric(r)) || (is_numeric(l) && r.is_string())),
        InvalidOperation: "arithmetic on dtypes {l} and {r} is not allowed; try an explicit cast first"
    );

    #[cfg(feature = "dtype-decimal")]
    if let Some(out) = decimal_op_operands(lhs, rhs) {
        return out;
    }
    coerce_lhs_rhs(lhs, rhs)
}
```


#### 📄 檔案: `crates/polars-plan/src/plans/conversion/type_coercion/binary.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:116, E:145, A:0) ➔ After(N:117, E:146, A:0)
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
  • + [新增節點] `a.is_decimal (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `coerced_binop_dtype` ──[CALLS]──> `a.is_decimal (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `coerced_binop_dtype()`
- **變更前簽章 (Before)**: `fn coerced_binop_dtype(
    expr_arena: &Arena<AExpr>,
    node_left: Node,
    type_left: &DataType,
    op: Operator,
    node_right: Node,
    type_right: &DataType,
)` (L156~L267)
- **變更後簽章 (After)**: `fn coerced_binop_dtype(
    expr_arena: &Arena<AExpr>,
    node_left: Node,
    type_left: &DataType,
    op: Operator,
    node_right: Node,
    type_right: &DataType,
)` (L156~L267)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(super) fn coerced_binop_dtype(
    expr_arena: &Arena<AExpr>,
    node_left: Node,
    type_left: &DataType,
    op: Operator,
    node_right: Node,
    type_right: &DataType,
) -> PolarsResult<Option<DataType>> {
    let left = expr_arena.get(node_left);
    let right = expr_arena.get(node_right);

    use DataType::*;
    // don't coerce string with number comparisons. They must error
    match (&type_left, &type_right, op) {
        #[cfg(not(feature = "dtype-categorical"))]
        (DataType::String, dt, op) | (dt, DataType::String, op)
            if op.is_comparison_or_bitwise() && dt.is_primitive_numeric() =>
        {
            return Ok(None);
        },
        #[cfg(feature = "dtype-categorical")]
        (String | Unknown(UnknownKind::Str) | Categorical(_, _), dt, op)
        | (dt, Unknown(UnknownKind::Str) | String | Categorical(_, _), op)
            if op.is_comparison_or_bitwise() && dt.is_primitive_numeric() =>
        {
            return Ok(None);
        },
        #[cfg(feature = "dtype-categorical")]
        (Unknown(UnknownKind::Str) | String | Enum(_, _), dt, op)
        | (dt, Unknown(UnknownKind::Str) | String | Enum(_, _), op)
            if op.is_comparison_or_bitwise() && dt.is_primitive_numeric() =>
        {
            return Ok(None);
        },
        #[cfg(feature = "dtype-date")]
        (Date, String | Unknown(UnknownKind::Str), op)
        | (String | Unknown(UnknownKind::Str), Date, op)
            if op.is_comparison_or_bitwise() =>
        {
            err_date_str_compare()?
        },
        #[cfg(feature = "dtype-datetime")]
        (Datetime(_, _), String | Unknown(UnknownKind::Str), op)
        | (String | Unknown(UnknownKind::Str), Datetime(_, _), op)
            if op.is_comparison_or_bitwise() =>
        {
            err_date_str_compare()?
        },
        #[cfg(feature = "dtype-time")]
        (Time | Unknown(UnknownKind::Str), String, op) if op.is_comparison_or_bitwise() => {
            err_date_str_compare()?
        },
        // structs can be arbitrarily nested, leave the complexity to the caller for now.
        #[cfg(feature = "dtype-struct")]
        (Struct(_), Struct(_), _op) => return Ok(None),
        _ => {},
    }

    if op.is_arithmetic() {
        match (&type_left, &type_right) {
            (Duration(_), Duration(_)) => return Ok(None),
            (Duration(_), r) if r.is_primitive_numeric() => return Ok(None),
            (String, a) | (a, String) if a.is_primitive_numeric() => {
                let fmt_side = |node: Node, ae: &AExpr| -> std::string::String {
                    if let AExpr::Column(name) = ae {
                        format!(" column '{name}'")
                    } else {
                        format!(" expression `{}`", node_to_expr(node, expr_arena))
                    }
                };
                let lhs = fmt_side(node_left, left);
                let rhs = fmt_side(node_right, right);
                polars_bail!(
                    InvalidOperation:
                    "arithmetic on dtypes {type_left} and {type_right} is not allowed \
                    (lhs:{lhs}, rhs:{rhs}); try an explicit cast first",
                )
            },
            (Datetime(_, _), _)
            | (_, Datetime(_, _))
            | (Date, _)
            | (_, Date)
            | (Duration(_), _)
            | (_, Duration(_))
            | (Time, _)
            | (_, Time)
            | (List(_), _)
            | (_, List(_)) => return Ok(None),
            #[cfg(feature = "dtype-array")]
            (Array(..), _) | (_, Array(..)) => return Ok(None),
            _ => {},
        }
    } else if compares_cat_to_string(type_left, type_right, op) {
        return Ok(None);
    }

    // Coerce types:
    let st = unpack!(get_supertype(type_left, type_right));
    let mut st = modify_supertype(st, left, right, type_left, type_right);

    if is_cat_str_binary(type_left, type_right) {
        st = String
    }

    // TODO! raise here?
    // We should at least never cast to Unknown.
    if matches!(st, DataType::Unknown(_)) {
        return Ok(None);
    }

    Ok(Some(st))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(super) fn coerced_binop_dtype(
    expr_arena: &Arena<AExpr>,
    node_left: Node,
    type_left: &DataType,
    op: Operator,
    node_right: Node,
    type_right: &DataType,
) -> PolarsResult<Option<DataType>> {
    let left = expr_arena.get(node_left);
    let right = expr_arena.get(node_right);

    use DataType::*;
    // don't coerce string with number comparisons. They must error
    match (&type_left, &type_right, op) {
        #[cfg(not(feature = "dtype-categorical"))]
        (DataType::String, dt, op) | (dt, DataType::String, op)
            if op.is_comparison_or_bitwise() && dt.is_primitive_numeric() =>
        {
            return Ok(None);
        },
        #[cfg(feature = "dtype-categorical")]
        (String | Unknown(UnknownKind::Str) | Categorical(_, _), dt, op)
        | (dt, Unknown(UnknownKind::Str) | String | Categorical(_, _), op)
            if op.is_comparison_or_bitwise() && dt.is_primitive_numeric() =>
        {
            return Ok(None);
        },
        #[cfg(feature = "dtype-categorical")]
        (Unknown(UnknownKind::Str) | String | Enum(_, _), dt, op)
        | (dt, Unknown(UnknownKind::Str) | String | Enum(_, _), op)
            if op.is_comparison_or_bitwise() && dt.is_primitive_numeric() =>
        {
            return Ok(None);
        },
        #[cfg(feature = "dtype-date")]
        (Date, String | Unknown(UnknownKind::Str), op)
        | (String | Unknown(UnknownKind::Str), Date, op)
            if op.is_comparison_or_bitwise() =>
        {
            err_date_str_compare()?
        },
        #[cfg(feature = "dtype-datetime")]
        (Datetime(_, _), String | Unknown(UnknownKind::Str), op)
        | (String | Unknown(UnknownKind::Str), Datetime(_, _), op)
            if op.is_comparison_or_bitwise() =>
        {
            err_date_str_compare()?
        },
        #[cfg(feature = "dtype-time")]
        (Time | Unknown(UnknownKind::Str), String, op) if op.is_comparison_or_bitwise() => {
            err_date_str_compare()?
        },
        // structs can be arbitrarily nested, leave the complexity to the caller for now.
        #[cfg(feature = "dtype-struct")]
        (Struct(_), Struct(_), _op) => return Ok(None),
        _ => {},
    }

    if op.is_arithmetic() {
        match (&type_left, &type_right) {
            (Duration(_), Duration(_)) => return Ok(None),
            (Duration(_), r) if r.is_primitive_numeric() => return Ok(None),
            (String, a) | (a, String) if a.is_primitive_numeric() || a.is_decimal() => {
                let fmt_side = |node: Node, ae: &AExpr| -> std::string::String {
                    if let AExpr::Column(name) = ae {
                        format!(" column '{name}'")
                    } else {
                        format!(" expression `{}`", node_to_expr(node, expr_arena))
                    }
                };
                let lhs = fmt_side(node_left, left);
                let rhs = fmt_side(node_right, right);
                polars_bail!(
                    InvalidOperation:
                    "arithmetic on dtypes {type_left} and {type_right} is not allowed \
                    (lhs:{lhs}, rhs:{rhs}); try an explicit cast first",
                )
            },
            (Datetime(_, _), _)
            | (_, Datetime(_, _))
            | (Date, _)
            | (_, Date)
            | (Duration(_), _)
            | (_, Duration(_))
            | (Time, _)
            | (_, Time)
            | (List(_), _)
            | (_, List(_)) => return Ok(None),
            #[cfg(feature = "dtype-array")]
            (Array(..), _) | (_, Array(..)) => return Ok(None),
            _ => {},
        }
    } else if compares_cat_to_string(type_left, type_right, op) {
        return Ok(None);
    }

    // Coerce types:
    let st = unpack!(get_supertype(type_left, type_right));
    let mut st = modify_supertype(st, left, right, type_left, type_right);

    if is_cat_str_binary(type_left, type_right) {
        st = String
    }

    // TODO! raise here?
    // We should at least never cast to Unknown.
    if matches!(st, DataType::Unknown(_)) {
        return Ok(None);
    }

    Ok(Some(st))
}
```


---

### 🔹 Commit #02: `0b57b7f0`
- **完整 Hash**: `0b57b7f0d9fb6f15cddf2789697fd0c7a8b76c64`
- **說明 (Ground Truth)**: fix: Preserve temporal sorted flag only when allowed (#30058)
- **變更檔案數**: 2

#### 📄 檔案: `crates/polars-expr/src/dispatch/datetime.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:181, E:308, A:0) ➔ After(N:177, E:304, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 4, +Edges: 1, -Edges: 5, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `polars_core::chunked_array::temporal::replace_time_zone::replace_time_zone(
                    s.datetime().unwrap(),
                    None,
                    &StringChunked::from_iter(std::iter::once("raise")),
                    NonExistent::Raise,
                )?
                .cast (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `s.is_sorted_flag (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `out.set_sorted_flag (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `time_series.is_sorted_flag (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `date` ──[CALLS]──> `polars_core::chunked_array::temporal::replace_time_zone::replace_time_zone(
                s.datetime().unwrap(),
                None,
                &StringChunked::from_iter(std::iter::once("raise")),
                NonExistent::Raise,
            )?
            .cast (External/Unresolved)`
  • - [移除呼叫邊] `date` ──[CALLS]──> `polars_core::chunked_array::temporal::replace_time_zone::replace_time_zone(
                    s.datetime().unwrap(),
                    None,
                    &StringChunked::from_iter(std::iter::once("raise")),
                    NonExistent::Raise,
                )?
                .cast (External/Unresolved)`
  • - [移除呼叫邊] `date` ──[CALLS]──> `out.set_sorted_flag (External/Unresolved)`
  • - [移除呼叫邊] `date` ──[CALLS]──> `s.is_sorted_flag (External/Unresolved)`
  • - [移除呼叫邊] `truncate` ──[CALLS]──> `out.set_sorted_flag (External/Unresolved)`
  • - [移除呼叫邊] `truncate` ──[CALLS]──> `time_series.is_sorted_flag (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `truncate()`
- **變更前簽章 (Before)**: `fn truncate(s: &[Column])` (L274~L292)
- **變更後簽章 (After)**: `fn truncate(s: &[Column])` (L266~L283)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(super) fn truncate(s: &[Column]) -> PolarsResult<Column> {
    let time_series = &s[0];
    let every = s[1].str()?;

    let mut out = match time_series.dtype() {
        DataType::Datetime(_, tz) => match tz {
            #[cfg(feature = "timezones")]
            Some(tz) => time_series
                .datetime()?
                .truncate(tz.parse::<Tz>().ok().as_ref(), every)?
                .into_column(),
            _ => time_series.datetime()?.truncate(None, every)?.into_column(),
        },
        DataType::Date => time_series.date()?.truncate(None, every)?.into_column(),
        dt => polars_bail!(opq = round, got = dt, expected = "date/datetime"),
    };
    out.set_sorted_flag(time_series.is_sorted_flag());
    Ok(out)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(super) fn truncate(s: &[Column]) -> PolarsResult<Column> {
    let time_series = &s[0];
    let every = s[1].str()?;

    let out = match time_series.dtype() {
        DataType::Datetime(_, tz) => match tz {
            #[cfg(feature = "timezones")]
            Some(tz) => time_series
                .datetime()?
                .truncate(tz.parse::<Tz>().ok().as_ref(), every)?
                .into_column(),
            _ => time_series.datetime()?.truncate(None, every)?.into_column(),
        },
        DataType::Date => time_series.date()?.truncate(None, every)?.into_column(),
        dt => polars_bail!(opq = truncate, got = dt, expected = "date/datetime"),
    };
    Ok(out)
}
```

### 🔹 函式: `date()`
- **變更前簽章 (Before)**: `fn date(s: &Column)` (L89~L118)
- **變更後簽章 (After)**: `fn date(s: &Column)` (L89~L110)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(super) fn date(s: &Column) -> PolarsResult<Column> {
    match s.dtype() {
        #[cfg(feature = "timezones")]
        DataType::Datetime(_, Some(_)) => {
            let mut out = {
                polars_core::chunked_array::temporal::replace_time_zone::replace_time_zone(
                    s.datetime().unwrap(),
                    None,
                    &StringChunked::from_iter(std::iter::once("raise")),
                    NonExistent::Raise,
                )?
                .cast(&DataType::Date)?
            };
            // `replace_time_zone` may unset sorted flag. But, we're only taking the date
            // part of the result, so we can safely preserve the sorted flag here. We may
            // need to make an exception if a time zone introduces a change which involves
            // "going back in time" and repeating a day, but we're not aware of that ever
            // having happened.
            out.set_sorted_flag(s.is_sorted_flag());
            Ok(out.into())
        },
        DataType::Datetime(_, _) => s
            .datetime()
            .unwrap()
            .cast(&DataType::Date)
            .map(Column::from),
        DataType::Date => Ok(s.clone()),
        dtype => polars_bail!(ComputeError: "expected Datetime or Date, got {dtype}"),
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(super) fn date(s: &Column) -> PolarsResult<Column> {
    match s.dtype() {
        #[cfg(feature = "timezones")]
        DataType::Datetime(_, Some(_)) => {
            let out = polars_core::chunked_array::temporal::replace_time_zone::replace_time_zone(
                s.datetime().unwrap(),
                None,
                &StringChunked::from_iter(std::iter::once("raise")),
                NonExistent::Raise,
            )?
            .cast(&DataType::Date)?;
            Ok(out.into())
        },
        DataType::Datetime(_, _) => s
            .datetime()
            .unwrap()
            .cast(&DataType::Date)
            .map(Column::from),
        DataType::Date => Ok(s.clone()),
        dtype => polars_bail!(ComputeError: "expected Datetime or Date, got {dtype}"),
    }
}
```


#### 📄 檔案: `crates/polars-time/src/truncate.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:41, E:58, A:0) ➔ After(N:41, E:61, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 4, +Edges: 7, -Edges: 4, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `self.physical().is_sorted_flag (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.physical().apply_values (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out.into_datetime (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out.set_sorted_flag (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `self
                        .physical()
                        .apply_values (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `self
                        .physical()
                        .apply_values(|t| fast_truncate(t, every))
                        .into_datetime (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `self
                        .physical (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `self
                        .physical()
                        .try_apply_nonnull_values_generic (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `DatetimeChunked::truncate` ──[CALLS]──> `self.physical().apply_values (External/Unresolved)`
  • + [新增呼叫邊] `DatetimeChunked::truncate` ──[CALLS]──> `out.set_sorted_flag (External/Unresolved)`
  • + [新增呼叫邊] `DatetimeChunked::truncate` ──[CALLS]──> `self.physical().is_sorted_flag (External/Unresolved)`
  • + [新增呼叫邊] `DatetimeChunked::truncate` ──[CALLS]──> `out.into_datetime (External/Unresolved)`
  • + [新增呼叫邊] `DatetimeChunked::truncate` ──[CALLS]──> `self.physical().try_apply_nonnull_values_generic (External/Unresolved)`
  • + [新增呼叫邊] `DateChunked::truncate` ──[CALLS]──> `out.set_sorted_flag (External/Unresolved)`
  • + [新增呼叫邊] `DateChunked::truncate` ──[CALLS]──> `self.physical().is_sorted_flag (External/Unresolved)`
  • _... 以及其餘 4 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `DateChunked::truncate()`
- **變更前簽章 (Before)**: `fn DateChunked::truncate(&self, _tz: Option<&Tz>, every: &StringChunked)` (L93~L150)
- **變更後簽章 (After)**: `fn DateChunked::truncate(&self, _tz: Option<&Tz>, every: &StringChunked)` (L97~L158)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn truncate(&self, _tz: Option<&Tz>, every: &StringChunked) -> PolarsResult<Self> {
        polars_ensure!(
            self.len() == every.len() || self.len() == 1 || every.len() == 1,
            length_mismatch = "dt.truncate",
            self.len(),
            every.len()
        );

        let offset = Duration::new(0);
        let out = match every.len() {
            1 => {
                if let Some(every) = every.get(0) {
                    let every = Duration::try_parse(every)?;
                    if every.negative {
                        polars_bail!(ComputeError: "cannot truncate a Date to a negative duration")
                    }
                    let w = Window::new(every, every, offset);
                    self.physical().try_apply_nonnull_values_generic(|t| {
                        Ok((w.truncate(
                            TimeUnit::Milliseconds,
                            MILLISECONDS_IN_DAY * t as i64,
                            None,
                        )? / MILLISECONDS_IN_DAY) as i32)
                    })
                } else {
                    Ok(Int32Chunked::full_null(self.name().clone(), self.len()))
                }
            },
            _ => {
                // A sqrt(n) cache is not too small, not too large.
                let mut duration_cache =
                    LruCache::with_capacity((every.len() as f64).sqrt() as usize);
                broadcast_try_binary_elementwise(self.physical(), every, |opt_t, opt_every| match (
                    opt_t, opt_every,
                ) {
                    (Some(t), Some(every)) => {
                        let every =
                            *duration_cache.try_get_or_insert_with(every, Duration::try_parse)?;

                        if every.negative {
                            polars_bail!(ComputeError: "cannot truncate a Date to a negative duration")
                        }

                        let w = Window::new(every, every, offset);
                        Ok(Some(
                            (w.truncate(
                                TimeUnit::Milliseconds,
                                MILLISECONDS_IN_DAY * t as i64,
                                None,
                            )? / MILLISECONDS_IN_DAY) as i32,
                        ))
                    },
                    _ => Ok(None),
                })
            },
        };
        Ok(out?.into_date())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn truncate(&self, _tz: Option<&Tz>, every: &StringChunked) -> PolarsResult<Self> {
        polars_ensure!(
            self.len() == every.len() || self.len() == 1 || every.len() == 1,
            length_mismatch = "dt.truncate",
            self.len(),
            every.len()
        );

        let offset = Duration::new(0);
        let out = match every.len() {
            1 => {
                if let Some(every) = every.get(0) {
                    let every = Duration::try_parse(every)?;
                    if every.negative {
                        polars_bail!(ComputeError: "cannot truncate a Date to a negative duration")
                    }
                    let w = Window::new(every, every, offset);
                    let mut out = self.physical().try_apply_nonnull_values_generic(
                        |t| -> PolarsResult<i32> {
                            Ok((w.truncate(
                                TimeUnit::Milliseconds,
                                MILLISECONDS_IN_DAY * t as i64,
                                None,
                            )? / MILLISECONDS_IN_DAY) as i32)
                        },
                    )?;
                    out.set_sorted_flag(self.physical().is_sorted_flag());
                    Ok(out)
                } else {
                    Ok(Int32Chunked::full_null(self.name().clone(), self.len()))
                }
            },
            _ => {
                // A sqrt(n) cache is not too small, not too large.
                let mut duration_cache =
                    LruCache::with_capacity((every.len() as f64).sqrt() as usize);
                broadcast_try_binary_elementwise(self.physical(), every, |opt_t, opt_every| match (
                    opt_t, opt_every,
                ) {
                    (Some(t), Some(every)) => {
                        let every =
                            *duration_cache.try_get_or_insert_with(every, Duration::try_parse)?;

                        if every.negative {
                            polars_bail!(ComputeError: "cannot truncate a Date to a negative duration")
                        }

                        let w = Window::new(every, every, offset);
                        Ok(Some(
                            (w.truncate(
                                TimeUnit::Milliseconds,
                                MILLISECONDS_IN_DAY * t as i64,
                                None,
                            )? / MILLISECONDS_IN_DAY) as i32,
                        ))
                    },
                    _ => Ok(None),
                })
            },
        };
        Ok(out?.into_date())
    }
```

### 🔹 函式: `DatetimeChunked::truncate()`
- **變更前簽章 (Before)**: `fn DatetimeChunked::truncate(&self, tz: Option<&Tz>, every: &StringChunked)` (L23~L89)
- **變更後簽章 (After)**: `fn DatetimeChunked::truncate(&self, tz: Option<&Tz>, every: &StringChunked)` (L23~L93)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn truncate(&self, tz: Option<&Tz>, every: &StringChunked) -> PolarsResult<Self> {
        polars_ensure!(
            self.len() == every.len() || self.len() == 1 || every.len() == 1,
            length_mismatch = "dt.truncate",
            self.len(),
            every.len()
        );

        let time_zone = self.time_zone();
        let offset = Duration::new(0);

        // Let's check if we can use a fastpath...
        if every.len() == 1 {
            if let Some(every) = every.get(0) {
                let every_parsed = Duration::try_parse(every)?;
                if every_parsed.negative {
                    polars_bail!(ComputeError: "cannot truncate a Datetime to a negative duration")
                }
                if (time_zone.is_none() || time_zone.as_ref() == Some(&TimeZone::UTC))
                    && (every_parsed.months() == 0 && every_parsed.weeks() == 0)
                {
                    // ... yes we can! Weeks, months, and time zones require extra logic.
                    // But in this simple case, it's just simple integer arithmetic.
                    let every = every_parsed.duration(self.time_unit());
                    if every == 0 {
                        return Ok(self.clone());
                    }
                    return Ok(self
                        .physical()
                        .apply_values(|t| fast_truncate(t, every))
                        .into_datetime(self.time_unit(), time_zone.clone()));
                } else {
                    let w = Window::new(every_parsed, every_parsed, offset);
                    let out = self
                        .physical()
                        .try_apply_nonnull_values_generic(|t| w.truncate(self.time_unit(), t, tz));
                    return Ok(out?.into_datetime(self.time_unit(), self.time_zone().clone()));
                }
            } else {
                return Ok(Int64Chunked::full_null(self.name().clone(), self.len())
                    .into_datetime(self.time_unit(), self.time_zone().clone()));
            }
        }

        // A sqrt(n) cache is not too small, not too large.
        let mut duration_cache = LruCache::with_capacity((every.len() as f64).sqrt() as usize);

        let out = broadcast_try_binary_elementwise(
            self.physical(),
            every,
            |opt_timestamp, opt_every| match (opt_timestamp, opt_every) {
                (Some(timestamp), Some(every)) => {
                    let every =
                        *duration_cache.try_get_or_insert_with(every, Duration::try_parse)?;

                    if every.negative {
                        polars_bail!(ComputeError: "cannot truncate a Datetime to a negative duration")
                    }

                    let w = Window::new(every, every, offset);
                    w.truncate(self.time_unit(), timestamp, tz).map(Some)
                },
                _ => Ok(None),
            },
        );
        Ok(out?.into_datetime(self.time_unit(), self.time_zone().clone()))
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn truncate(&self, tz: Option<&Tz>, every: &StringChunked) -> PolarsResult<Self> {
        polars_ensure!(
            self.len() == every.len() || self.len() == 1 || every.len() == 1,
            length_mismatch = "dt.truncate",
            self.len(),
            every.len()
        );

        let time_zone = self.time_zone();
        let offset = Duration::new(0);

        // Let's check if we can use a fastpath...
        if every.len() == 1 {
            if let Some(every) = every.get(0) {
                let every_parsed = Duration::try_parse(every)?;
                if every_parsed.negative {
                    polars_bail!(ComputeError: "cannot truncate a Datetime to a negative duration")
                }
                // Offset changes can make truncated local times go backwards, so sortedness is
                // only kept without a time zone or in UTC.
                let naive_or_utc =
                    time_zone.is_none() || time_zone.as_ref() == Some(&TimeZone::UTC);
                if naive_or_utc && (every_parsed.months() == 0 && every_parsed.weeks() == 0) {
                    // ... yes we can! Weeks, months, and time zones require extra logic.
                    // But in this simple case, it's just simple integer arithmetic.
                    let every = every_parsed.duration(self.time_unit());
                    if every == 0 {
                        return Ok(self.clone());
                    }
                    let mut out = self.physical().apply_values(|t| fast_truncate(t, every));
                    out.set_sorted_flag(self.physical().is_sorted_flag());
                    return Ok(out.into_datetime(self.time_unit(), time_zone.clone()));
                } else {
                    let w = Window::new(every_parsed, every_parsed, offset);
                    let mut out = self.physical().try_apply_nonnull_values_generic(|t| {
                        w.truncate(self.time_unit(), t, tz)
                    })?;
                    if naive_or_utc {
                        out.set_sorted_flag(self.physical().is_sorted_flag());
                    }
                    return Ok(out.into_datetime(self.time_unit(), self.time_zone().clone()));
                }
            } else {
                return Ok(Int64Chunked::full_null(self.name().clone(), self.len())
                    .into_datetime(self.time_unit(), self.time_zone().clone()));
            }
        }

        // A sqrt(n) cache is not too small, not too large.
        let mut duration_cache = LruCache::with_capacity((every.len() as f64).sqrt() as usize);

        let out = broadcast_try_binary_elementwise(
            self.physical(),
            every,
            |opt_timestamp, opt_every| match (opt_timestamp, opt_every) {
                (Some(timestamp), Some(every)) => {
                    let every =
                        *duration_cache.try_get_or_insert_with(every, Duration::try_parse)?;

                    if every.negative {
                        polars_bail!(ComputeError: "cannot truncate a Datetime to a negative duration")
                    }

                    let w = Window::new(every, every, offset);
                    w.truncate(self.time_unit(), timestamp, tz).map(Some)
                },
                _ => Ok(None),
            },
        );
        Ok(out?.into_datetime(self.time_unit(), self.time_zone().clone()))
    }
```


---

### 🔹 Commit #03: `d5c68d0a`
- **完整 Hash**: `d5c68d0acd8acc94d389f6cf6e3d97c6df1ffe8e`
- **說明 (Ground Truth)**: fix: Decimal cast to int should truncate (#30069)
- **變更檔案數**: 1

#### 📄 檔案: `crates/polars-compute/src/decimal.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:261, E:358, A:0) ➔ After(N:263, E:361, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 2, +Edges: 9, -Edges: 6, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `nu.is_multiple_of (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `div_128_pow10_round` (FUNCTION_DEF)
  • + [新增節點] `div_128_pow10_impl` (FUNCTION_DEF)
  • + [新增節點] `div_128_pow10_trunc` (FUNCTION_DEF)
  • - [移除節點] `zu.is_multiple_of (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `div_128_pow10` (FUNCTION_DEF)
  • + [新增呼叫邊] `div_128_pow10_impl` ──[CALLS]──> `nu.is_multiple_of (External/Unresolved)`
  • + [新增呼叫邊] `div_128_pow10_impl` ──[CALLS]──> `widening_mul_128`
  • + [新增呼叫邊] `div_128_pow10_round` ──[CALLS]──> `x.unsigned_abs (External/Unresolved)`
  • + [新增呼叫邊] `div_128_pow10_round` ──[CALLS]──> `div_128_pow10_impl`
  • + [新增呼叫邊] `div_128_pow10_trunc` ──[CALLS]──> `div_128_pow10_impl`
  • + [新增呼叫邊] `div_128_pow10_trunc` ──[CALLS]──> `x.unsigned_abs (External/Unresolved)`
  • + [新增呼叫邊] `dec128_to_i128` ──[CALLS]──> `div_128_pow10_trunc`
  • + [新增呼叫邊] `dec128_rescale` ──[CALLS]──> `div_128_pow10_round`
  • + [新增呼叫邊] `i128_to_dec128_scaled` ──[CALLS]──> `div_128_pow10_round`
  • _... 以及其餘 6 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `dec128_rescale()`
- **變更前簽章 (Before)**: `fn dec128_rescale(x: i128, old_s: usize, new_p: usize, new_s: usize)` (L595~L605)
- **變更後簽章 (After)**: `fn dec128_rescale(x: i128, old_s: usize, new_p: usize, new_s: usize)` (L611~L621)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn dec128_rescale(x: i128, old_s: usize, new_p: usize, new_s: usize) -> Option<i128> {
    let r = if new_s < old_s {
        div_128_pow10(x, old_s - new_s)
    } else if new_s > old_s {
        mul_128_pow10(x, new_s - old_s)?
    } else {
        return Some(x);
    };

    dec128_fits(r, new_p).then_some(r)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn dec128_rescale(x: i128, old_s: usize, new_p: usize, new_s: usize) -> Option<i128> {
    let r = if new_s < old_s {
        div_128_pow10_round(x, old_s - new_s)
    } else if new_s > old_s {
        mul_128_pow10(x, new_s - old_s)?
    } else {
        return Some(x);
    };

    dec128_fits(r, new_p).then_some(r)
}
```

### 🔹 函式: `dec128_to_i128()`
- **變更前簽章 (Before)**: `fn dec128_to_i128(x: i128, s: usize)` (L527~L529)
- **變更後簽章 (After)**: `fn dec128_to_i128(x: i128, s: usize)` (L543~L545)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn dec128_to_i128(x: i128, s: usize) -> i128 {
    if s == 0 { x } else { div_128_pow10(x, s) }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn dec128_to_i128(x: i128, s: usize) -> i128 {
    div_128_pow10_trunc(x, s)
}
```

### 🔹 函式: `i128_to_dec128_scaled()`
- **變更前簽章 (Before)**: `fn i128_to_dec128_scaled(x: i128, s: usize, s_out: usize)` (L710~L717)
- **變更後簽章 (After)**: `fn i128_to_dec128_scaled(x: i128, s: usize, s_out: usize)` (L726~L733)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn i128_to_dec128_scaled(x: i128, s: usize, s_out: usize) -> Option<i128> {
    let r = match s_out.cmp(&s) {
        Ordering::Less => div_128_pow10(x, s - s_out),
        Ordering::Equal => x,
        Ordering::Greater => x.checked_mul(POW10_I128[s_out - s])?,
    };
    dec128_fits(r, DEC128_MAX_PREC).then_some(r)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn i128_to_dec128_scaled(x: i128, s: usize, s_out: usize) -> Option<i128> {
    let r = match s_out.cmp(&s) {
        Ordering::Less => div_128_pow10_round(x, s - s_out),
        Ordering::Equal => x,
        Ordering::Greater => x.checked_mul(POW10_I128[s_out - s])?,
    };
    dec128_fits(r, DEC128_MAX_PREC).then_some(r)
}
```


---

### 🔹 Commit #04: `ce0043cd`
- **完整 Hash**: `ce0043cd6038e64d288a19c464db289f859c17da`
- **說明 (Ground Truth)**: fix: Casting far future dates shouldn't silently wrap (#30068)
- **變更檔案數**: 2

#### 📄 檔案: `crates/polars-expr/src/dispatch/datetime.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:179, E:310, A:0) ➔ After(N:181, E:308, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 2, +Edges: 4, -Edges: 6, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `DataType::Datetime (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `tz.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `DataType::Duration (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `s.strict_cast (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `s.as_materialized_series().duration (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `ca.cast_time_unit(tu).into_column (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `cast_time_unit` ──[CALLS]──> `s.strict_cast (External/Unresolved)`
  • + [新增呼叫邊] `cast_time_unit` ──[CALLS]──> `DataType::Datetime (External/Unresolved)`
  • + [新增呼叫邊] `cast_time_unit` ──[CALLS]──> `tz.clone (External/Unresolved)`
  • + [新增呼叫邊] `cast_time_unit` ──[CALLS]──> `DataType::Duration (External/Unresolved)`
  • - [移除呼叫邊] `cast_time_unit` ──[CALLS]──> `s.datetime (External/Unresolved)`
  • - [移除呼叫邊] `cast_time_unit` ──[CALLS]──> `Ok (External/Unresolved)`
  • - [移除呼叫邊] `cast_time_unit` ──[CALLS]──> `ca.cast_time_unit(tu).into_column (External/Unresolved)`
  • - [移除呼叫邊] `cast_time_unit` ──[CALLS]──> `cast_time_unit`
  • - [移除呼叫邊] `cast_time_unit` ──[CALLS]──> `s.as_materialized_series().duration (External/Unresolved)`
  • _... 以及其餘 1 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `cast_time_unit()`
- **變更前簽章 (Before)**: `fn cast_time_unit(s: &Column, tu: TimeUnit)` (L265~L278)
- **變更後簽章 (After)**: `fn cast_time_unit(s: &Column, tu: TimeUnit)` (L265~L272)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(super) fn cast_time_unit(s: &Column, tu: TimeUnit) -> PolarsResult<Column> {
    match s.dtype() {
        DataType::Datetime(_, _) => {
            let ca = s.datetime()?;
            Ok(ca.cast_time_unit(tu).into_column())
        },
        #[cfg(feature = "dtype-duration")]
        DataType::Duration(_) => {
            let ca = s.as_materialized_series().duration()?;
            Ok(ca.cast_time_unit(tu).into_column())
        },
        dt => polars_bail!(ComputeError: "dtype `{}` has no time unit", dt),
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(super) fn cast_time_unit(s: &Column, tu: TimeUnit) -> PolarsResult<Column> {
    match s.dtype() {
        DataType::Datetime(_, tz) => s.strict_cast(&DataType::Datetime(tu, tz.clone())),
        #[cfg(feature = "dtype-duration")]
        DataType::Duration(_) => s.strict_cast(&DataType::Duration(tu)),
        dt => polars_bail!(ComputeError: "dtype `{}` has no time unit", dt),
    }
}
```


#### 📄 檔案: `crates/polars-plan/src/plans/conversion/type_coercion/mod.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:196, E:241, A:0) ➔ After(N:196, E:241, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 1, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `CastColumnsPolicy {
                            integer_upcast: true,
                            integer_to_float_cast: false,
                            float_upcast: true,
                            float_downcast: true,
                            datetime_nanoseconds_downcast: true,
                            datetime_microseconds_downcast: true,
                            // Increasing the time unit precision can overflow.
                            datetime_milliseconds_upcast: false,
                            datetime_microseconds_upcast: false,
                            datetime_convert_timezone: true,
                            null_upcast: true,
                            categorical_to_string: true,
                            missing_struct_fields: MissingColumnsPolicy::Insert,
                            extra_struct_fields: ExtraColumnsPolicy::Ignore,
                        }
                        .should_cast_column (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `CastColumnsPolicy {
                            integer_upcast: true,
                            integer_to_float_cast: false,
                            float_upcast: true,
                            float_downcast: true,
                            datetime_nanoseconds_downcast: true,
                            datetime_microseconds_downcast: true,
                            datetime_milliseconds_upcast: true,
                            datetime_microseconds_upcast: true,
                            datetime_convert_timezone: true,
                            null_upcast: true,
                            categorical_to_string: true,
                            missing_struct_fields: MissingColumnsPolicy::Insert,
                            extra_struct_fields: ExtraColumnsPolicy::Ignore,
                        }
                        .should_cast_column (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `TypeCoercionRule::optimize_expr` ──[CALLS]──> `CastColumnsPolicy {
                            integer_upcast: true,
                            integer_to_float_cast: false,
                            float_upcast: true,
                            float_downcast: true,
                            datetime_nanoseconds_downcast: true,
                            datetime_microseconds_downcast: true,
                            // Increasing the time unit precision can overflow.
                            datetime_milliseconds_upcast: false,
                            datetime_microseconds_upcast: false,
                            datetime_convert_timezone: true,
                            null_upcast: true,
                            categorical_to_string: true,
                            missing_struct_fields: MissingColumnsPolicy::Insert,
                            extra_struct_fields: ExtraColumnsPolicy::Ignore,
                        }
                        .should_cast_column (External/Unresolved)`
  • - [移除呼叫邊] `TypeCoercionRule::optimize_expr` ──[CALLS]──> `CastColumnsPolicy {
                            integer_upcast: true,
                            integer_to_float_cast: false,
                            float_upcast: true,
                            float_downcast: true,
                            datetime_nanoseconds_downcast: true,
                            datetime_microseconds_downcast: true,
                            datetime_milliseconds_upcast: true,
                            datetime_microseconds_upcast: true,
                            datetime_convert_timezone: true,
                            null_upcast: true,
                            categorical_to_string: true,
                            missing_struct_fields: MissingColumnsPolicy::Insert,
                            extra_struct_fields: ExtraColumnsPolicy::Ignore,
                        }
                        .should_cast_column (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TypeCoercionRule::optimize_expr()`
- **變更前簽章 (Before)**: `fn TypeCoercionRule::optimize_expr(
        &mut self,
        expr_arena: &mut Arena<AExpr>,
        expr_node: Node,
        schema: &Schema,
        ctx: OptimizeExprContext,
    )` (L114~L1267)
- **變更後簽章 (After)**: `fn TypeCoercionRule::optimize_expr(
        &mut self,
        expr_arena: &mut Arena<AExpr>,
        expr_node: Node,
        schema: &Schema,
        ctx: OptimizeExprContext,
    )` (L114~L1268)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn optimize_expr(
        &mut self,
        expr_arena: &mut Arena<AExpr>,
        expr_node: Node,
        schema: &Schema,
        ctx: OptimizeExprContext,
    ) -> PolarsResult<Option<AExpr>> {
        let expr = expr_arena.get(expr_node);
        let out = match *expr {
            ref ae @ AExpr::Cast { .. } => {
                let AExpr::Cast {
                    expr: input_expr,
                    dtype,
                    options,
                } = ae.clone()
                else {
                    unreachable!()
                };

                let input = expr_arena.get(input_expr).clone();
                if ctx.has_inputs {
                    if let CastOptions::Strict = options {
                        let cast_from = expr_arena
                            .get(input_expr)
                            .to_field(&ToFieldContext::new(expr_arena, schema))?
                            .dtype;
                        let cast_to = &dtype;

                        let v = CastColumnsPolicy {
                            integer_upcast: true,
                            integer_to_float_cast: false,
                            float_upcast: true,
                            float_downcast: true,
                            datetime_nanoseconds_downcast: true,
                            datetime_microseconds_downcast: true,
                            datetime_milliseconds_upcast: true,
                            datetime_microseconds_upcast: true,
                            datetime_convert_timezone: true,
                            null_upcast: true,
                            categorical_to_string: true,
                            missing_struct_fields: MissingColumnsPolicy::Insert,
                            extra_struct_fields: ExtraColumnsPolicy::Ignore,
                        }
                        .should_cast_column("", cast_to, &cast_from);

                        match v {
                            // No casting needed
                            Ok(false) => {
                                return Ok(Some(expr_arena.get(input_expr).clone()));
                            },
                            Ok(true) => {
                                let options = if cast_from.is_primitive_numeric()
                                    && cast_to.is_primitive_numeric()
                                {
                                    CastOptions::Overflowing
                                } else {
                                    CastOptions::NonStrict
                                };

                                let dtype = cast_to.clone();

                                expr_arena.replace(
                                    expr_node,
                                    AExpr::Cast {
                                        expr: input_expr,
                                        dtype,
                                        options,
                                    },
                                );
                            },

                            Err(_) => {},
                        }
                    }
                }

                inline_or_prune_cast(&input, &dtype, options, schema, expr_arena)?
            },
            AExpr::Agg(IRAggExpr::Implode {
                input,
                maintain_order: _,
            }) => inline_implode(input, expr_arena)?,
            AExpr::Ternary {
                truthy: truthy_node,
                falsy: falsy_node,
                predicate,
            } => {
                let (truthy, type_true) =
                    unpack!(get_aexpr_and_type(expr_arena, truthy_node, schema));
                let (falsy, type_false) =
                    unpack!(get_aexpr_and_type(expr_arena, falsy_node, schema));

                if type_true == type_false {
                    return Ok(None);
                }
                let st = unpack!(get_supertype(&type_true, &type_false));
                let st = modify_supertype(st, truthy, falsy, &type_true, &type_false);

                // only cast if the type is not already the super type.
                // this can prevent an expensive flattening and subsequent aggregation
                // in a group_by context. To be able to cast the groups need to be
                // flattened
                let new_node_truthy = if type_true != st {
                    expr_arena.add(AExpr::Cast {
                        expr: truthy_node,
                        dtype: st.clone(),
                        options: CastOptions::Strict,
                    })
                } else {
                    truthy_node
                };

                let new_node_falsy = if type_false != st {
                    expr_arena.add(AExpr::Cast {
                        expr: falsy_node,
                        dtype: st,
                        options: CastOptions::Strict,
                    })
                } else {
                    falsy_node
                };

                Some(AExpr::Ternary {
                    truthy: new_node_truthy,
                    falsy: new_node_falsy,
                    predicate,
                })
            },
            AExpr::BinaryExpr {
                left: node_left,
                op,
                right: node_right,
            } => return process_binary(expr_arena, schema, node_left, op, node_right),
            #[cfg(feature = "is_between")]
            AExpr::Function {
                ref input,
                function: IRFunctionExpr::Boolean(IRBooleanFunction::IsBetween { closed }),
                options,
            } => {
                use CmpLiteralRhsRewrite::*;

                use crate::plans::type_coercion::binary::{
                    BoolValueAlways, CmpLiteralRhsRewrite, coerce_comparison_literal,
                    coerced_binop_dtype,
                };

                let [needle, low, high] = input.as_slice() else {
                    return Ok(None);
                };

                let needle = needle.clone();
                let low = low.clone();
                let high = high.clone();

                let mut new_low: Option<ExprIR> = None;
                let mut new_high: Option<ExprIR> = None;
                // Some(v):
                // * v @ false -> LHS only
                // * v @ true -> RHS only
                let mut one_side: Option<bool> = None;

                let cmp_op_low = match closed {
                    ClosedInterval::Both | ClosedInterval::Left => Operator::GtEq,
                    ClosedInterval::Right | ClosedInterval::None => Operator::Gt,
                };
                let cmp_op_high = match closed {
                    ClosedInterval::Both | ClosedInterval::Right => Operator::LtEq,
                    ClosedInterval::Left | ClosedInterval::None => Operator::Lt,
                };

                let needle_dtype = unpack!(try_get_dtype(expr_arena, needle.node(), schema).ok());

                let (low_ae, low_dtype) =
                    unpack!(get_aexpr_and_type(expr_arena, low.node(), schema));

                if low_dtype != needle_dtype
                    && let AExpr::Literal(lv) = low_ae
                {
                    use crate::plans::type_coercion::binary::BoolValueAlways;

                    if let LiteralValue::Scalar(lit) = lv.clone().materialize()
                        && let Some(rewrite) = coerce_comparison_literal(
                            needle.node(),
                            &needle_dtype,
                            cmp_op_low,
                            lit,
                            expr_arena,
                        )
                    {
                        match rewrite {
                            ReplaceLit(new_lit) => {
                                new_low = Some(ExprIR::from_node(
                                    expr_arena.add(AExpr::Literal(LiteralValue::Scalar(new_lit))),
                                    expr_arena,
                                ));
                            },
                            NewAExpr {
                                aexpr,
                                output_constraint,
                            } => match output_constraint {
                                Some(BoolValueAlways::True | BoolValueAlways::TrueOrNull) => {
                                    one_side = Some(true)
                                },
                                Some(BoolValueAlways::FalseOrNull) => return Ok(Some(aexpr)),
                                None => return Ok(None),
                            },
                        }
                    }
                }

                let (high_ae, high_dtype) =
                    unpack!(get_aexpr_and_type(expr_arena, high.node(), schema));

                if high_dtype != needle_dtype
                    && let AExpr::Literal(lv) = high_ae
                {
                    if let LiteralValue::Scalar(lit) = lv.clone().materialize()
                        && let Some(rewrite) = coerce_comparison_literal(
                            needle.node(),
                            &needle_dtype,
                            cmp_op_high,
                            lit,
                            expr_arena,
                        )
                    {
                        match rewrite {
                            ReplaceLit(new_lit) => {
                                new_high = Some(ExprIR::from_node(
                                    expr_arena.add(AExpr::Literal(LiteralValue::Scalar(new_lit))),
                                    expr_arena,
                                ));
                            },
                            NewAExpr {
                                aexpr,
                                output_constraint,
                            } => match output_constraint {
                                Some(BoolValueAlways::True | BoolValueAlways::TrueOrNull) => {
                                    one_side = Some(false)
                                },
                                Some(BoolValueAlways::FalseOrNull) => return Ok(Some(aexpr)),
                                None => return Ok(None),
                            },
                        }
                    }
                }

                let out = match one_side {
                    Some(false) => AExpr::BinaryExpr {
                        left: needle.node(),
                        op: cmp_op_low,
                        right: new_low.unwrap_or(low).node(),
                    },
                    Some(true) => AExpr::BinaryExpr {
                        left: needle.node(),
                        op: cmp_op_high,
                        right: new_high.unwrap_or(high).node(),
                    },
                    None => {
                        let CastingRules::Supertype(supertype_options) =
                            unpack!(options.cast_options)
                        else {
                            return Ok(None);
                        };
                        let mut low = new_low.unwrap_or(low);
                        let mut high = new_high.unwrap_or(high);

                        let low_dtype = unpack!(try_get_dtype(expr_arena, low.node(), schema).ok());
                        let high_dtype =
                            unpack!(try_get_dtype(expr_arena, high.node(), schema).ok());

                        let low_st = unpack!(coerced_binop_dtype(
                            expr_arena,
                            needle.node(),
                            &needle_dtype,
                            cmp_op_low,
                            low.node(),
                            &low_dtype,
                        )?);
                        let high_st = unpack!(coerced_binop_dtype(
                            expr_arena,
                            needle.node(),
                            &needle_dtype,
                            cmp_op_high,
                            high.node(),
                            &high_dtype,
                        )?);

                        let super_type = unpack!(get_supertype_with_options(
                            &low_st,
                            &high_st,
                            supertype_options,
                        ));

                        let mut needle = needle;
                        // TODO: NonStrict casts are what process_binary
                        // inserts for binops. cast_expr_ir always ignores
                        // the input CastOptions and sets strict casts.
                        // Should probably be consistent.
                        cast_expr_ir(
                            &mut needle,
                            &needle_dtype,
                            &super_type,
                            expr_arena,
                            CastOptions::NonStrict,
                        )?;
                        cast_expr_ir(
                            &mut low,
                            &low_dtype,
                            &super_type,
                            expr_arena,
                            CastOptions::NonStrict,
                        )?;
                        cast_expr_ir(
                            &mut high,
                            &high_dtype,
                            &super_type,
                            expr_arena,
                            CastOptions::NonStrict,
                        )?;
                        // We've already applied all the casts, so switch
                        // off casting for this newly rewritten isbetween
                        // node.
                        let mut options = options;
                        options.cast_options = None;
                        AExpr::Function {
                            input: vec![needle, low, high],
                            function: IRFunctionExpr::Boolean(IRBooleanFunction::IsBetween {
                                closed,
                            }),
                            options,
                        }
                    },
                };

                Some(out)
            },
            // Map lookup must work without the `is_in` feature.
            #[cfg(feature = "dtype-map")]
            AExpr::Function {
                function:
                    IRFunctionExpr::MapExpr(
                        ref func @ (IRMapFunction::Get { .. } | IRMapFunction::ContainsKey { .. }),
                    ),
                ..
            } => {
                let op = match func {
                    IRMapFunction::Get { .. } => "map.get",
                    _ => "map.contains_key",
                };
                membership::coerce_is_in(
                    expr_node,
                    expr_arena,
                    schema,
                    MembershipForm::Contains,
                    |input, arena| membership::resolve_map_key(input, arena, schema, op),
                )?
            },
            #[cfg(feature = "is_in")]
            AExpr::Function { ref function, .. }
                if {
                    let mut matches = matches!(
                        function,
                        IRFunctionExpr::Boolean(IRBooleanFunction::IsIn { .. })
                            | IRFunctionExpr::ListExpr(IRListFunction::Contains { .. })
                    );
                    #[cfg(feature = "dtype-array")]
                    {
                        matches |= matches!(
                            function,
                            IRFunctionExpr::ArrayExpr(IRArrayFunction::Contains { .. })
                        );
                    }
                    matches
                } =>
            {
                let (op, form) = match function {
                    IRFunctionExpr::Boolean(IRBooleanFunction::IsIn { .. }) => {
                        ("is_in", MembershipForm::IsIn)
                    },
                    IRFunctionExpr::ListExpr(IRListFunction::Contains { .. }) => {
                        ("list.contains", MembershipForm::Contains)
                    },
                    #[cfg(feature = "dtype-array")]
                    IRFunctionExpr::ArrayExpr(IRArrayFunction::Contains { .. }) => {
                        ("arr.contains", MembershipForm::Contains)
                    },
                    _ => unreachable!(),
                };

                membership::coerce_is_in(expr_node, expr_arena, schema, form, |input, arena| {
                    membership::resolve_is_in(input, arena, schema, form, op)
                })?
            },
            AExpr::Function {
                ref function,
                ref input,
                options,
            } if matches!(
                function,
                IRFunctionExpr::Boolean(
                    IRBooleanFunction::Any { .. } | IRBooleanFunction::All { .. }
                )
            ) =>
            {
                // Ensure the input to boolean aggregations is boolean; try cast if possible.
                let (_, in_dtype) =
                    unpack!(get_aexpr_and_type(expr_arena, input[0].node(), schema));

                if in_dtype.is_bool() {
                    return Ok(None);
                }

                // If input cannot be cast to boolean, raise a error.
                polars_ensure!(
                    in_dtype.can_cast_to(&DataType::Boolean) != Some(false),
                    InvalidOperation: "expected boolean input for '{}()' (got {})",
                    function,
                    in_dtype
                );

                let function = function.clone();
                let mut input = input.clone();
                cast_expr_ir(
                    &mut input[0],
                    &in_dtype,
                    &DataType::Boolean,
                    expr_arena,
                    CastOptions::NonStrict,
                )?;

                Some(AExpr::Function {
                    function,
                    input,
                    options,
                })
            },
            // shift and fill should only cast left and fill value to super type.
            // @3.0: Raise a type error instead of upcasting the input.
            AExpr::Function {
                function: IRFunctionExpr::ShiftAndFill,
                ref input,
                options,
            } => {
                let left_node = input[0].node();
                let fill_value_node = input[2].node();
                let (left, type_left) = unpack!(get_aexpr_and_type(expr_arena, left_node, schema));
                let (fill_value, type_fill_value) =
                    unpack!(get_aexpr_and_type(expr_arena, fill_value_node, schema));

                unpack!(early_escape(&type_left, &type_fill_value));

                let super_type = unpack!(get_supertype(&type_left, &type_fill_value));
                let super_type =
                    modify_supertype(super_type, left, fill_value, &type_left, &type_fill_value);

                let mut input = input.clone();
                let new_node_left = if type_left != super_type {
                    expr_arena.add(AExpr::Cast {
                        expr: left_node,
                        dtype: super_type.clone(),
                        options: CastOptions::NonStrict,
                    })
                } else {
                    left_node
                };

                let new_node_fill_value = if type_fill_value != super_type {
                    expr_arena.add(AExpr::Cast {
                        expr: fill_value_node,
                        dtype: super_type,
                        options: CastOptions::NonStrict,
                    })
                } else {
                    fill_value_node
                };

                input[0].set_node(new_node_left);
                input[2].set_node(new_node_fill_value);

                Some(AExpr::Function {
                    function: IRFunctionExpr::ShiftAndFill,
                    input,
                    options,
                })
            },
            #[cfg(feature = "ewma")]
            AExpr::Function {
                function:
                    ref ewm_variant @ IRFunctionExpr::EwmMean {
                        options: ewm_options,
                    }
                    | ref ewm_variant @ IRFunctionExpr::EwmVar {
                        options: ewm_options,
                    }
                    | ref ewm_variant @ IRFunctionExpr::EwmStd {
                        options: ewm_options,
                    }
                    | ref ewm_variant @ IRFunctionExpr::EwmSum {
                        options: ewm_options,
                    },
                ref input,
                options,
            } => {
                polars_ensure!(
                    (0.0..=1.0).contains(&ewm_options.alpha),
                    ComputeError: "alpha must be in [0; 1], got {}", ewm_options.alpha
                );

                let input_expr = match &input.as_slice() {
                    &[first] => first,
                    v => polars_bail!(
                        ComputeError:
                        "ewm_mean requires 1 input, got {} (input: {:?})",
                        v.len(),
                        v
                    ),
                };

                let (_, dtype) = get_aexpr_and_type(expr_arena, input_expr.node(), schema).unwrap();

                if dtype.is_float() {
                    return Ok(None);
                }
                polars_ensure!(!dtype.is_struct(), opq = ewm, dtype);

                let new_function = match ewm_variant {
                    IRFunctionExpr::EwmMean { .. } => IRFunctionExpr::EwmMean {
                        options: ewm_options,
                    },
                    IRFunctionExpr::EwmVar { .. } => IRFunctionExpr::EwmVar {
                        options: ewm_options,
                    },
                    IRFunctionExpr::EwmStd { .. } => IRFunctionExpr::EwmStd {
                        options: ewm_options,
                    },
                    IRFunctionExpr::EwmSum { .. } => IRFunctionExpr::EwmSum {
                        options: ewm_options,
                    },
                    _ => unreachable!(),
                };

                let input_expr = ExprIR::from_node(
                    expr_arena.add(AExpr::Cast {
                        expr: input_expr.node(),
                        dtype: DataType::Float64,
                        // TODO: Non-strict to match legacy execution behavior, but should be strict.
                        options: CastOptions::NonStrict,
                    }),
                    expr_arena,
                );

                Some(AExpr::Function {
                    function: new_function,
                    input: vec![input_expr],
                    options,
                })
            },
            // generic type coercion of any function.
            AExpr::Function {
                // only for `DataType::Unknown` as it still has to be set.
                ref function,
                ref input,
                mut options,
            } if options.cast_options.is_some() => {
                let casting_rules = options.cast_options.unwrap();

                let function = function.clone();
                let mut input = input.clone();

                if let Some(dtypes) =
                    functions::get_function_dtypes(&input, expr_arena, schema, &function)?
                {
                    let self_e = input[0].clone();
                    let (self_ae, type_self) =
                        unpack!(get_aexpr_and_type(expr_arena, self_e.node(), schema));
                    let mut super_type = type_self.clone();
                    match casting_rules {
                        CastingRules::Supertype(super_type_opts) => {
                            for other in &input[1..] {
                                let (other, type_other) =
                                    unpack!(get_aexpr_and_type(expr_arena, other.node(), schema));

                                let Some(new_st) = get_supertype_with_options(
                                    &super_type,
                                    &type_other,
                                    super_type_opts,
                                ) else {
                                    raise_supertype(&function, &input, schema, expr_arena)?;
                                    unreachable!()
                                };
                                if input.len() == 2 {
                                    // modify_supertype is a bit more conservative of casting columns
                                    // to literals
                                    super_type = modify_supertype(
                                        new_st,
                                        self_ae,
                                        other,
                                        &type_self,
                                        &type_other,
                                    )
                                } else {
                                    // when dealing with more than 1 argument, we simply find the supertypes
                                    super_type = new_st
                                }
                            }
                        },
                        CastingRules::FirstArgLossless => {
                            for other in &input[1..] {
                                let other = other.dtype(schema, expr_arena)?;
                                can_cast_to_lossless(&super_type, other)?;
                            }
                        },
                    }

                    if matches!(super_type, DataType::Unknown(UnknownKind::Any)) {
                        raise_supertype(&function, &input, schema, expr_arena)?;
                        unreachable!()
                    }

                    match super_type {
                        DataType::Unknown(UnknownKind::Float) => super_type = DataType::Float64,
                        DataType::Unknown(UnknownKind::Int(v)) => {
                            super_type = materialize_dyn_int(v).dtype()
                        },
                        _ => {},
                    }

                    // A decimal supertype may not hold every value, raise instead of
                    // producing nulls.
                    let literal_options = if super_type.leaf_dtype().is_decimal() {
                        CastOptions::Strict
                    } else {
                        CastOptions::NonStrict
                    };
                    for (e, dtype) in input.iter_mut().zip(dtypes) {
                        cast_expr_ir(e, &dtype, &super_type, expr_arena, literal_options)?;
                    }
                }

                // Ensure we don't go through this on next iteration.
                options.cast_options = None;
                Some(AExpr::Function {
                    function,
                    input,
                    options,
                })
            },
            #[cfg(all(feature = "temporal", feature = "dtype-duration"))]
            AExpr::Function {
                function: IRFunctionExpr::TemporalExpr(IRTemporalFunction::Duration(_)),
                ..
            } => coerce_function_inputs(
                expr_node,
                expr_arena,
                schema,
                CastOptions::Strict,
                |i, dtype| match dtype {
                    DataType::Int64 | DataType::Float64 => Ok(None),
                    dt if dt.is_integer() => Ok(Some(DataType::Int64)),
                    dt if dt.is_float() => Ok(Some(DataType::Float64)),
                    dt => polars_bail!(
                        InvalidOperation: "expected integer or float dtype, (got {dt}) in input {i} of duration"
                    ),
                },
            )?,
            #[cfg(feature = "business")]
            AExpr::Function {
                function: IRFunctionExpr::Business(ref business_fn),
                ref input,
                options,
            } => {
                let holiday_arg_idx: usize = match business_fn {
                    IRBusinessFunction::AddBusinessDay { .. }
                    | IRBusinessFunction::BusinessDayCount { .. } => 2,
                    IRBusinessFunction::IsBusinessDay { .. } => 1,
                };

                let holiday_arg = unpack!(input.get(holiday_arg_idx));

                // We implode, only for literal Series(dtype=Date), as this is considered a valid
                // parameter on the Python API as an `Iterable[date]`.
                let new_lv_ae: AExpr = match expr_arena.get(holiday_arg.node()) {
                    AExpr::Literal(LiteralValue::Series(s)) if s.dtype() == &DataType::Date => {
                        AExpr::Literal(LiteralValue::Series(SpecialEq::new(
                            s.implode().unwrap().into_series(),
                        )))
                    },
                    ae => {
                        let dtype = ae.to_dtype(&ToFieldContext::new(expr_arena, schema))?;

                        let is_list_of_date = match &dtype {
                            DataType::List(inner) => inner.as_ref() == &DataType::Date,
                            _ => false,
                        };

                        polars_ensure!(
                            is_list_of_date,
                            ComputeError:
                            "dtype of holidays list must be List(Date), got {dtype:?} instead"
                        );

                        return Ok(None);
                    },
                };

                let mut input = input.clone();
                let function = IRFunctionExpr::Business(business_fn.clone());
                input[holiday_arg_idx].set_node(expr_arena.add(new_lv_ae));

                Some(AExpr::Function {
                    input,
                    function,
                    options,
                })
            },
            #[cfg(feature = "list_gather")]
            AExpr::Function {
                function: IRFunctionExpr::ListExpr(IRListFunction::Gather(_)),
                ref input,
                ..
            } => {
                let (_, type_left) =
                    unpack!(get_aexpr_and_type(expr_arena, input[0].node(), schema));
                let (_, type_other) =
                    unpack!(get_aexpr_and_type(expr_arena, input[1].node(), schema));

                let DataType::List(inner_dtype) = &type_other else {
                    polars_bail!(InvalidOperation: "`list.gather` indices must be a list of integers, not a flat {type_other}. Use `implode` to wrap the flat value into a list.");
                };

                polars_ensure!(
                    inner_dtype.is_integer(),
                    op = "list.gather",
                    type_left,
                    type_other
                );
                None
            },
            #[cfg(all(feature = "strings", feature = "find_many"))]
            AExpr::Function {
                function:
                    ref function @ IRFunctionExpr::StringExpr(
                        IRStringFunction::ContainsAny { .. }
                        | IRStringFunction::FindMany { .. }
                        | IRStringFunction::ExtractMany { .. },
                    ),
                ref input,
                ..
            } => {
                let (_, type_left) =
                    unpack!(get_aexpr_and_type(expr_arena, input[0].node(), schema));
                let (_, type_other) =
                    unpack!(get_aexpr_and_type(expr_arena, input[1].node(), schema));

                let DataType::List(inner_dtype) = &type_other else {
                    polars_bail!(InvalidOperation: "`{function}` with a flat string datatype is invalid. Use `implode` to wrap the string value into a list.");
                };

                polars_ensure!(
                    type_left.is_string() && inner_dtype.is_string(),
                    op = format!("{function}"),
                    type_left,
                    type_other
                );
                None
            },

            #[cfg(feature = "string_pad")]
            AExpr::Function {
                function:
                    IRFunctionExpr::StringExpr(
                        IRStringFunction::PadStart { .. }
                        | IRStringFunction::PadEnd { .. }
                        | IRStringFunction::ZFill,
                    ),
                ..
            } => coerce_function_inputs(
                expr_node,
                expr_arena,
                schema,
                CastOptions::Strict,
                |i, _| Ok((i == 1).then_some(DataType::UInt64)), // length
            )?,

            #[cfg(all(feature = "strings", feature = "concat_str"))]
            AExpr::Function {
                function: IRFunctionExpr::StringExpr(IRStringFunction::ConcatHorizontal { .. }),
                ..
            } => coerce_function_inputs(
                expr_node,
                expr_arena,
                schema,
                CastOptions::NonStrict,
                |_, dtype| Ok((!dtype.is_string()).then_some(DataType::String)),
            )?,
            #[cfg(all(feature = "strings", feature = "find_many"))]
            AExpr::Function {
                function: IRFunctionExpr::StringExpr(IRStringFunction::ReplaceMany { .. }),
                ref input,
                ..
            } => {
                let (_, type_left) =
                    unpack!(get_aexpr_and_type(expr_arena, input[0].node(), schema));
                let (_, type_patterns) =
                    unpack!(get_aexpr_and_type(expr_arena, input[1].node(), schema));
                let (_, type_replace_with) =
                    unpack!(get_aexpr_and_type(expr_arena, input[2].node(), schema));

                let DataType::List(type_patterns_inner_dtype) = &type_patterns else {
                    polars_bail!(InvalidOperation: "`str.replace_many` with a flat {type_patterns} datatype as pattern is invalid. Use `implode` to wrap the string value into a list.");
                };
                let DataType::List(type_replace_with_inner_dtype) = &type_replace_with else {
                    polars_bail!(InvalidOperation: "`str.replace_many` with a flat {type_replace_with} datatype as replacement is invalid. Use `implode` to wrap the string value into a list.");
                };

                polars_ensure!(
                    type_left.is_string()
                        && type_patterns_inner_dtype.is_string()
                        && type_replace_with_inner_dtype.is_string(),
                    op = "str.replace_many",
                    type_left,
                    type_patterns,
                    type_replace_with
                );
                None
            },
            #[cfg(feature = "replace")]
            AExpr::Function {
                function:
                    ref function @ (IRFunctionExpr::Replace | IRFunctionExpr::ReplaceStrict { .. }),
                ref input,
                options,
            } => {
                let (_, type_old) =
                    unpack!(get_aexpr_and_type(expr_arena, input[1].node(), schema));
                let (_, type_new) =
                    unpack!(get_aexpr_and_type(expr_arena, input[2].node(), schema));

                polars_ensure!(
                    !type_old.contains_objects() && !type_new.contains_objects(),
                    InvalidOperation: "`replace` does not support `old`/`new` values of object dtype"
                );

                let (DataType::List(_), DataType::List(_)) = (&type_old, &type_new) else {
                    let function = function.clone();
                    let mut input = input.clone();

                    if !type_old.is_list() {
                        let other_input = expr_arena.add(AExpr::Agg(IRAggExpr::Implode {
                            input: input[1].node(),
                            maintain_order: true,
                        }));
                        input[1].set_node(other_input);
                    }
                    if !type_new.is_list() {
                        let other_input = expr_arena.add(AExpr::Agg(IRAggExpr::Implode {
                            input: input[2].node(),
                            maintain_order: true,
                        }));
                        input[2].set_node(other_input);
                    }

                    return Ok(Some(AExpr::Function {
                        function,
                        input,
                        options,
                    }));
                };
                None
            },
            #[cfg(feature = "range")]
            AExpr::Function {
                function:
                    ref
                    function @ IRFunctionExpr::Range(IRRangeFunction::IntRange { step: _, ref dtype }),
                ref input,
                options,
            } => {
                polars_ensure!(dtype.is_integer(), ComputeError: "non-integer `dtype` passed to `int_range`: {:?}", dtype);

                let (_, type_start) =
                    unpack!(get_aexpr_and_type(expr_arena, input[0].node(), schema));
                let (_, type_end) =
                    unpack!(get_aexpr_and_type(expr_arena, input[1].node(), schema));

                polars_ensure!(type_start.is_numeric() || type_start.is_null(), InvalidOperation: "`start` must be numeric for `int_range`, got {}", type_start);
                polars_ensure!(type_end.is_numeric() || type_end.is_null(), InvalidOperation: "`end` must be numeric for `int_range`, got {}", type_end);

                if [&type_start, &type_end]
                    .into_iter()
                    .all(|arg_dtype| arg_dtype == dtype)
                {
                    return Ok(None);
                }

                let function = function.clone();
                let dtype = dtype.clone();
                let mut input = input.clone();
                for (i, arg_dtype) in [type_start, type_end].into_iter().enumerate() {
                    cast_expr_ir(
                        &mut input[i],
                        &arg_dtype,
                        &dtype,
                        expr_arena,
                        CastOptions::Strict,
                    )?;
                }

                Some(AExpr::Function {
                    function,
                    input,
                    options,
                })
            },
            #[cfg(feature = "range")]
            AExpr::Function {
                function: IRFunctionExpr::Range(IRRangeFunction::IntRanges { .. }),
                ..
            } => coerce_function_inputs(
                expr_node,
                expr_arena,
                schema,
                CastOptions::Strict,
                |i, dtype| {
                    let name = ["start", "end", "step"][i];
                    polars_ensure!(
                        dtype.is_numeric() || dtype.is_null(),
                        InvalidOperation: "`{name}` must be numeric for `int_ranges`, got {dtype}"
                    );
                    Ok(Some(DataType::Int64))
                },
            )?,
            // The estimate casts the quantile to `Float64`, so give a dynamic literal
            // that dtype rather than leaving it unknown in the plan.
            #[cfg(feature = "approx_quantile")]
            AExpr::Function {
                function: IRFunctionExpr::ApproxQuantileEstimate { .. },
                ..
            } => coerce_function_inputs(
                expr_node,
                expr_arena,
                schema,
                CastOptions::Strict,
                |i, dtype| {
                    let is_dyn_number = matches!(
                        dtype,
                        DataType::Unknown(UnknownKind::Int(_) | UnknownKind::Float)
                    );
                    Ok((i == 1 && is_dyn_number).then_some(DataType::Float64))
                },
            )?,
            #[cfg(feature = "moment")]
            AExpr::Function {
                function: IRFunctionExpr::Skew(..) | IRFunctionExpr::Kurtosis(..),
                ..
            } => coerce_function_inputs(
                expr_node,
                expr_arena,
                schema,
                CastOptions::Strict,
                |i, _| Ok((i == 0).then_some(DataType::Float64)),
            )?,
            #[cfg(all(feature = "range", feature = "dtype-date"))]
            AExpr::Function {
                function:
                    ref function @ IRFunctionExpr::Range(IRRangeFunction::DateRange {
                        interval: _,
                        closed: _,
                        arg_type,
                    })
                    | ref function @ IRFunctionExpr::Range(IRRangeFunction::DateRanges {
                        interval: _,
                        closed: _,
                        arg_type,
                    }),
                ref input,
                options,
            } => {
                let (from_types, to_types) = match arg_type {
                    DateRangeArgs::StartEndInterval => {
                        let start = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let end = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        ensure_datetime!(start);
                        ensure_datetime!(end);
                        let from_types = [Some(start), Some(end), None];
                        let to_types = [Some(DataType::Date), Some(DataType::Date), None];
                        (from_types, to_types)
                    },
                    DateRangeArgs::StartEndSamples => {
                        let start = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let end = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        let num_samples = try_get_dtype(expr_arena, input[2].node(), schema)?;
                        ensure_datetime!(start);
                        ensure_datetime!(end);
                        ensure_int!(num_samples);
                        let from_types = [Some(start), Some(end), Some(num_samples)];
                        let to_types = [
                            Some(DataType::Date),
                            Some(DataType::Date),
                            Some(DataType::Int64),
                        ];
                        (from_types, to_types)
                    },
                    DateRangeArgs::StartIntervalSamples => {
                        let start = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let num_samples = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        ensure_datetime!(start);
                        ensure_int!(num_samples);
                        let from_types = [Some(start), Some(num_samples), None];
                        let to_types = [Some(DataType::Date), Some(DataType::Int64), None];
                        (from_types, to_types)
                    },
                    DateRangeArgs::EndIntervalSamples => {
                        let end = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let num_samples = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        ensure_datetime!(end);
                        ensure_int!(num_samples);
                        let from_types = [Some(end), Some(num_samples), None];
                        let to_types = [Some(DataType::Date), Some(DataType::Int64), None];
                        (from_types, to_types)
                    },
                };

                let from_iter = from_types.into_iter();
                let to_iter = to_types.into_iter();
                let mut input = input.clone();
                let function = function.clone();
                let mut modified = false;
                for (i, (from_dtype, to_dtype)) in from_iter.zip(to_iter).enumerate() {
                    if let (Some(from_dt), Some(to_dt)) = (from_dtype, to_dtype) {
                        if from_dt != to_dt {
                            modified = true;
                            coerce_temporal_dt(&from_dt, &to_dt, &mut input[i], expr_arena)?;
                        }
                    }
                }

                if modified {
                    Some(AExpr::Function {
                        function,
                        input,
                        options,
                    })
                } else {
                    return Ok(None);
                }
            },
            #[cfg(all(feature = "range", feature = "dtype-datetime"))]
            AExpr::Function {
                function:
                    ref function @ IRFunctionExpr::Range(IRRangeFunction::DatetimeRange {
                        ref interval,
                        closed: _,
                        time_unit: ref tu,
                        time_zone: ref tz,
                        arg_type,
                    })
                    | ref function @ IRFunctionExpr::Range(IRRangeFunction::DatetimeRanges {
                        ref interval,
                        closed: _,
                        time_unit: ref tu,
                        time_zone: ref tz,
                        arg_type,
                    }),
                ref input,
                options,
            } => {
                let (from_types, to_types) = match arg_type {
                    DateRangeArgs::StartEndInterval => {
                        let start = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let end = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        ensure_datetime!(start);
                        ensure_datetime!(end);
                        let initial_st = try_get_supertype(&start, &end).unwrap();
                        let supertype = temporal_range_output_type(initial_st, tu, tz, interval)?;
                        let from_types = [Some(start), Some(end), None];
                        let to_types = [Some(supertype.clone()), Some(supertype), None];
                        (from_types, to_types)
                    },
                    DateRangeArgs::StartEndSamples => {
                        let start = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let end = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        let num_samples = try_get_dtype(expr_arena, input[2].node(), schema)?;
                        ensure_datetime!(start);
                        ensure_datetime!(end);
                        ensure_int!(num_samples);
                        let initial_st = try_get_supertype(&start, &end)?;
                        let supertype = temporal_range_output_type(initial_st, tu, tz, interval)?;
                        let from_types = [Some(start), Some(end), Some(num_samples)];
                        let to_types = [
                            Some(supertype.clone()),
                            Some(supertype),
                            Some(DataType::Int64),
                        ];
                        (from_types, to_types)
                    },
                    DateRangeArgs::StartIntervalSamples => {
                        let start = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let num_samples = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        ensure_datetime!(start);
                        ensure_int!(num_samples);
                        let supertype =
                            temporal_range_output_type(start.clone(), tu, tz, interval)?;
                        let from_types = [Some(start), Some(num_samples), None];
                        let to_types = [Some(supertype), Some(DataType::Int64), None];
                        (from_types, to_types)
                    },
                    DateRangeArgs::EndIntervalSamples => {
                        let end = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let num_samples = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        ensure_datetime!(end);
                        ensure_int!(num_samples);
                        let supertype = temporal_range_output_type(end.clone(), tu, tz, interval)?;
                        let from_types = [Some(end), Some(num_samples), None];
                        let to_types = [Some(supertype), Some(DataType::Int64), None];
                        (from_types, to_types)
                    },
                };

                let from_iter = from_types.into_iter();
                let to_iter = to_types.into_iter();
                let mut input = input.clone();
                let function = function.clone();
                let mut modified = false;
                for (i, (from_dtype, to_dtype)) in from_iter.zip(to_iter).enumerate() {
                    if let (Some(from_dt), Some(to_dt)) = (from_dtype, to_dtype) {
                        if from_dt != to_dt {
                            modified = true;
                            coerce_temporal_dt(&from_dt, &to_dt, &mut input[i], expr_arena)?;
                        }
                    }
                }

                if modified {
                    Some(AExpr::Function {
                        function,
                        input,
                        options,
                    })
                } else {
                    return Ok(None);
                }
            },
            AExpr::Slice { offset, length, .. } => {
                let (_, offset_dtype) = unpack!(get_aexpr_and_type(expr_arena, offset, schema));
                polars_ensure!(offset_dtype.is_integer(), InvalidOperation: "offset must be integral for slice expression, not {}", offset_dtype);
                let (_, length_dtype) = unpack!(get_aexpr_and_type(expr_arena, length, schema));
                polars_ensure!(length_dtype.is_integer() || length_dtype.is_null(), InvalidOperation: "length must be integral for slice expression, not {}", length_dtype);
                None
            },
            _ => None,
        };
        Ok(out)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn optimize_expr(
        &mut self,
        expr_arena: &mut Arena<AExpr>,
        expr_node: Node,
        schema: &Schema,
        ctx: OptimizeExprContext,
    ) -> PolarsResult<Option<AExpr>> {
        let expr = expr_arena.get(expr_node);
        let out = match *expr {
            ref ae @ AExpr::Cast { .. } => {
                let AExpr::Cast {
                    expr: input_expr,
                    dtype,
                    options,
                } = ae.clone()
                else {
                    unreachable!()
                };

                let input = expr_arena.get(input_expr).clone();
                if ctx.has_inputs {
                    if let CastOptions::Strict = options {
                        let cast_from = expr_arena
                            .get(input_expr)
                            .to_field(&ToFieldContext::new(expr_arena, schema))?
                            .dtype;
                        let cast_to = &dtype;

                        let v = CastColumnsPolicy {
                            integer_upcast: true,
                            integer_to_float_cast: false,
                            float_upcast: true,
                            float_downcast: true,
                            datetime_nanoseconds_downcast: true,
                            datetime_microseconds_downcast: true,
                            // Increasing the time unit precision can overflow.
                            datetime_milliseconds_upcast: false,
                            datetime_microseconds_upcast: false,
                            datetime_convert_timezone: true,
                            null_upcast: true,
                            categorical_to_string: true,
                            missing_struct_fields: MissingColumnsPolicy::Insert,
                            extra_struct_fields: ExtraColumnsPolicy::Ignore,
                        }
                        .should_cast_column("", cast_to, &cast_from);

                        match v {
                            // No casting needed
                            Ok(false) => {
                                return Ok(Some(expr_arena.get(input_expr).clone()));
                            },
                            Ok(true) => {
                                let options = if cast_from.is_primitive_numeric()
                                    && cast_to.is_primitive_numeric()
                                {
                                    CastOptions::Overflowing
                                } else {
                                    CastOptions::NonStrict
                                };

                                let dtype = cast_to.clone();

                                expr_arena.replace(
                                    expr_node,
                                    AExpr::Cast {
                                        expr: input_expr,
                                        dtype,
                                        options,
                                    },
                                );
                            },

                            Err(_) => {},
                        }
                    }
                }

                inline_or_prune_cast(&input, &dtype, options, schema, expr_arena)?
            },
            AExpr::Agg(IRAggExpr::Implode {
                input,
                maintain_order: _,
            }) => inline_implode(input, expr_arena)?,
            AExpr::Ternary {
                truthy: truthy_node,
                falsy: falsy_node,
                predicate,
            } => {
                let (truthy, type_true) =
                    unpack!(get_aexpr_and_type(expr_arena, truthy_node, schema));
                let (falsy, type_false) =
                    unpack!(get_aexpr_and_type(expr_arena, falsy_node, schema));

                if type_true == type_false {
                    return Ok(None);
                }
                let st = unpack!(get_supertype(&type_true, &type_false));
                let st = modify_supertype(st, truthy, falsy, &type_true, &type_false);

                // only cast if the type is not already the super type.
                // this can prevent an expensive flattening and subsequent aggregation
                // in a group_by context. To be able to cast the groups need to be
                // flattened
                let new_node_truthy = if type_true != st {
                    expr_arena.add(AExpr::Cast {
                        expr: truthy_node,
                        dtype: st.clone(),
                        options: CastOptions::Strict,
                    })
                } else {
                    truthy_node
                };

                let new_node_falsy = if type_false != st {
                    expr_arena.add(AExpr::Cast {
                        expr: falsy_node,
                        dtype: st,
                        options: CastOptions::Strict,
                    })
                } else {
                    falsy_node
                };

                Some(AExpr::Ternary {
                    truthy: new_node_truthy,
                    falsy: new_node_falsy,
                    predicate,
                })
            },
            AExpr::BinaryExpr {
                left: node_left,
                op,
                right: node_right,
            } => return process_binary(expr_arena, schema, node_left, op, node_right),
            #[cfg(feature = "is_between")]
            AExpr::Function {
                ref input,
                function: IRFunctionExpr::Boolean(IRBooleanFunction::IsBetween { closed }),
                options,
            } => {
                use CmpLiteralRhsRewrite::*;

                use crate::plans::type_coercion::binary::{
                    BoolValueAlways, CmpLiteralRhsRewrite, coerce_comparison_literal,
                    coerced_binop_dtype,
                };

                let [needle, low, high] = input.as_slice() else {
                    return Ok(None);
                };

                let needle = needle.clone();
                let low = low.clone();
                let high = high.clone();

                let mut new_low: Option<ExprIR> = None;
                let mut new_high: Option<ExprIR> = None;
                // Some(v):
                // * v @ false -> LHS only
                // * v @ true -> RHS only
                let mut one_side: Option<bool> = None;

                let cmp_op_low = match closed {
                    ClosedInterval::Both | ClosedInterval::Left => Operator::GtEq,
                    ClosedInterval::Right | ClosedInterval::None => Operator::Gt,
                };
                let cmp_op_high = match closed {
                    ClosedInterval::Both | ClosedInterval::Right => Operator::LtEq,
                    ClosedInterval::Left | ClosedInterval::None => Operator::Lt,
                };

                let needle_dtype = unpack!(try_get_dtype(expr_arena, needle.node(), schema).ok());

                let (low_ae, low_dtype) =
                    unpack!(get_aexpr_and_type(expr_arena, low.node(), schema));

                if low_dtype != needle_dtype
                    && let AExpr::Literal(lv) = low_ae
                {
                    use crate::plans::type_coercion::binary::BoolValueAlways;

                    if let LiteralValue::Scalar(lit) = lv.clone().materialize()
                        && let Some(rewrite) = coerce_comparison_literal(
                            needle.node(),
                            &needle_dtype,
                            cmp_op_low,
                            lit,
                            expr_arena,
                        )
                    {
                        match rewrite {
                            ReplaceLit(new_lit) => {
                                new_low = Some(ExprIR::from_node(
                                    expr_arena.add(AExpr::Literal(LiteralValue::Scalar(new_lit))),
                                    expr_arena,
                                ));
                            },
                            NewAExpr {
                                aexpr,
                                output_constraint,
                            } => match output_constraint {
                                Some(BoolValueAlways::True | BoolValueAlways::TrueOrNull) => {
                                    one_side = Some(true)
                                },
                                Some(BoolValueAlways::FalseOrNull) => return Ok(Some(aexpr)),
                                None => return Ok(None),
                            },
                        }
                    }
                }

                let (high_ae, high_dtype) =
                    unpack!(get_aexpr_and_type(expr_arena, high.node(), schema));

                if high_dtype != needle_dtype
                    && let AExpr::Literal(lv) = high_ae
                {
                    if let LiteralValue::Scalar(lit) = lv.clone().materialize()
                        && let Some(rewrite) = coerce_comparison_literal(
                            needle.node(),
                            &needle_dtype,
                            cmp_op_high,
                            lit,
                            expr_arena,
                        )
                    {
                        match rewrite {
                            ReplaceLit(new_lit) => {
                                new_high = Some(ExprIR::from_node(
                                    expr_arena.add(AExpr::Literal(LiteralValue::Scalar(new_lit))),
                                    expr_arena,
                                ));
                            },
                            NewAExpr {
                                aexpr,
                                output_constraint,
                            } => match output_constraint {
                                Some(BoolValueAlways::True | BoolValueAlways::TrueOrNull) => {
                                    one_side = Some(false)
                                },
                                Some(BoolValueAlways::FalseOrNull) => return Ok(Some(aexpr)),
                                None => return Ok(None),
                            },
                        }
                    }
                }

                let out = match one_side {
                    Some(false) => AExpr::BinaryExpr {
                        left: needle.node(),
                        op: cmp_op_low,
                        right: new_low.unwrap_or(low).node(),
                    },
                    Some(true) => AExpr::BinaryExpr {
                        left: needle.node(),
                        op: cmp_op_high,
                        right: new_high.unwrap_or(high).node(),
                    },
                    None => {
                        let CastingRules::Supertype(supertype_options) =
                            unpack!(options.cast_options)
                        else {
                            return Ok(None);
                        };
                        let mut low = new_low.unwrap_or(low);
                        let mut high = new_high.unwrap_or(high);

                        let low_dtype = unpack!(try_get_dtype(expr_arena, low.node(), schema).ok());
                        let high_dtype =
                            unpack!(try_get_dtype(expr_arena, high.node(), schema).ok());

                        let low_st = unpack!(coerced_binop_dtype(
                            expr_arena,
                            needle.node(),
                            &needle_dtype,
                            cmp_op_low,
                            low.node(),
                            &low_dtype,
                        )?);
                        let high_st = unpack!(coerced_binop_dtype(
                            expr_arena,
                            needle.node(),
                            &needle_dtype,
                            cmp_op_high,
                            high.node(),
                            &high_dtype,
                        )?);

                        let super_type = unpack!(get_supertype_with_options(
                            &low_st,
                            &high_st,
                            supertype_options,
                        ));

                        let mut needle = needle;
                        // TODO: NonStrict casts are what process_binary
                        // inserts for binops. cast_expr_ir always ignores
                        // the input CastOptions and sets strict casts.
                        // Should probably be consistent.
                        cast_expr_ir(
                            &mut needle,
                            &needle_dtype,
                            &super_type,
                            expr_arena,
                            CastOptions::NonStrict,
                        )?;
                        cast_expr_ir(
                            &mut low,
                            &low_dtype,
                            &super_type,
                            expr_arena,
                            CastOptions::NonStrict,
                        )?;
                        cast_expr_ir(
                            &mut high,
                            &high_dtype,
                            &super_type,
                            expr_arena,
                            CastOptions::NonStrict,
                        )?;
                        // We've already applied all the casts, so switch
                        // off casting for this newly rewritten isbetween
                        // node.
                        let mut options = options;
                        options.cast_options = None;
                        AExpr::Function {
                            input: vec![needle, low, high],
                            function: IRFunctionExpr::Boolean(IRBooleanFunction::IsBetween {
                                closed,
                            }),
                            options,
                        }
                    },
                };

                Some(out)
            },
            // Map lookup must work without the `is_in` feature.
            #[cfg(feature = "dtype-map")]
            AExpr::Function {
                function:
                    IRFunctionExpr::MapExpr(
                        ref func @ (IRMapFunction::Get { .. } | IRMapFunction::ContainsKey { .. }),
                    ),
                ..
            } => {
                let op = match func {
                    IRMapFunction::Get { .. } => "map.get",
                    _ => "map.contains_key",
                };
                membership::coerce_is_in(
                    expr_node,
                    expr_arena,
                    schema,
                    MembershipForm::Contains,
                    |input, arena| membership::resolve_map_key(input, arena, schema, op),
                )?
            },
            #[cfg(feature = "is_in")]
            AExpr::Function { ref function, .. }
                if {
                    let mut matches = matches!(
                        function,
                        IRFunctionExpr::Boolean(IRBooleanFunction::IsIn { .. })
                            | IRFunctionExpr::ListExpr(IRListFunction::Contains { .. })
                    );
                    #[cfg(feature = "dtype-array")]
                    {
                        matches |= matches!(
                            function,
                            IRFunctionExpr::ArrayExpr(IRArrayFunction::Contains { .. })
                        );
                    }
                    matches
                } =>
            {
                let (op, form) = match function {
                    IRFunctionExpr::Boolean(IRBooleanFunction::IsIn { .. }) => {
                        ("is_in", MembershipForm::IsIn)
                    },
                    IRFunctionExpr::ListExpr(IRListFunction::Contains { .. }) => {
                        ("list.contains", MembershipForm::Contains)
                    },
                    #[cfg(feature = "dtype-array")]
                    IRFunctionExpr::ArrayExpr(IRArrayFunction::Contains { .. }) => {
                        ("arr.contains", MembershipForm::Contains)
                    },
                    _ => unreachable!(),
                };

                membership::coerce_is_in(expr_node, expr_arena, schema, form, |input, arena| {
                    membership::resolve_is_in(input, arena, schema, form, op)
                })?
            },
            AExpr::Function {
                ref function,
                ref input,
                options,
            } if matches!(
                function,
                IRFunctionExpr::Boolean(
                    IRBooleanFunction::Any { .. } | IRBooleanFunction::All { .. }
                )
            ) =>
            {
                // Ensure the input to boolean aggregations is boolean; try cast if possible.
                let (_, in_dtype) =
                    unpack!(get_aexpr_and_type(expr_arena, input[0].node(), schema));

                if in_dtype.is_bool() {
                    return Ok(None);
                }

                // If input cannot be cast to boolean, raise a error.
                polars_ensure!(
                    in_dtype.can_cast_to(&DataType::Boolean) != Some(false),
                    InvalidOperation: "expected boolean input for '{}()' (got {})",
                    function,
                    in_dtype
                );

                let function = function.clone();
                let mut input = input.clone();
                cast_expr_ir(
                    &mut input[0],
                    &in_dtype,
                    &DataType::Boolean,
                    expr_arena,
                    CastOptions::NonStrict,
                )?;

                Some(AExpr::Function {
                    function,
                    input,
                    options,
                })
            },
            // shift and fill should only cast left and fill value to super type.
            // @3.0: Raise a type error instead of upcasting the input.
            AExpr::Function {
                function: IRFunctionExpr::ShiftAndFill,
                ref input,
                options,
            } => {
                let left_node = input[0].node();
                let fill_value_node = input[2].node();
                let (left, type_left) = unpack!(get_aexpr_and_type(expr_arena, left_node, schema));
                let (fill_value, type_fill_value) =
                    unpack!(get_aexpr_and_type(expr_arena, fill_value_node, schema));

                unpack!(early_escape(&type_left, &type_fill_value));

                let super_type = unpack!(get_supertype(&type_left, &type_fill_value));
                let super_type =
                    modify_supertype(super_type, left, fill_value, &type_left, &type_fill_value);

                let mut input = input.clone();
                let new_node_left = if type_left != super_type {
                    expr_arena.add(AExpr::Cast {
                        expr: left_node,
                        dtype: super_type.clone(),
                        options: CastOptions::NonStrict,
                    })
                } else {
                    left_node
                };

                let new_node_fill_value = if type_fill_value != super_type {
                    expr_arena.add(AExpr::Cast {
                        expr: fill_value_node,
                        dtype: super_type,
                        options: CastOptions::NonStrict,
                    })
                } else {
                    fill_value_node
                };

                input[0].set_node(new_node_left);
                input[2].set_node(new_node_fill_value);

                Some(AExpr::Function {
                    function: IRFunctionExpr::ShiftAndFill,
                    input,
                    options,
                })
            },
            #[cfg(feature = "ewma")]
            AExpr::Function {
                function:
                    ref ewm_variant @ IRFunctionExpr::EwmMean {
                        options: ewm_options,
                    }
                    | ref ewm_variant @ IRFunctionExpr::EwmVar {
                        options: ewm_options,
                    }
                    | ref ewm_variant @ IRFunctionExpr::EwmStd {
                        options: ewm_options,
                    }
                    | ref ewm_variant @ IRFunctionExpr::EwmSum {
                        options: ewm_options,
                    },
                ref input,
                options,
            } => {
                polars_ensure!(
                    (0.0..=1.0).contains(&ewm_options.alpha),
                    ComputeError: "alpha must be in [0; 1], got {}", ewm_options.alpha
                );

                let input_expr = match &input.as_slice() {
                    &[first] => first,
                    v => polars_bail!(
                        ComputeError:
                        "ewm_mean requires 1 input, got {} (input: {:?})",
                        v.len(),
                        v
                    ),
                };

                let (_, dtype) = get_aexpr_and_type(expr_arena, input_expr.node(), schema).unwrap();

                if dtype.is_float() {
                    return Ok(None);
                }
                polars_ensure!(!dtype.is_struct(), opq = ewm, dtype);

                let new_function = match ewm_variant {
                    IRFunctionExpr::EwmMean { .. } => IRFunctionExpr::EwmMean {
                        options: ewm_options,
                    },
                    IRFunctionExpr::EwmVar { .. } => IRFunctionExpr::EwmVar {
                        options: ewm_options,
                    },
                    IRFunctionExpr::EwmStd { .. } => IRFunctionExpr::EwmStd {
                        options: ewm_options,
                    },
                    IRFunctionExpr::EwmSum { .. } => IRFunctionExpr::EwmSum {
                        options: ewm_options,
                    },
                    _ => unreachable!(),
                };

                let input_expr = ExprIR::from_node(
                    expr_arena.add(AExpr::Cast {
                        expr: input_expr.node(),
                        dtype: DataType::Float64,
                        // TODO: Non-strict to match legacy execution behavior, but should be strict.
                        options: CastOptions::NonStrict,
                    }),
                    expr_arena,
                );

                Some(AExpr::Function {
                    function: new_function,
                    input: vec![input_expr],
                    options,
                })
            },
            // generic type coercion of any function.
            AExpr::Function {
                // only for `DataType::Unknown` as it still has to be set.
                ref function,
                ref input,
                mut options,
            } if options.cast_options.is_some() => {
                let casting_rules = options.cast_options.unwrap();

                let function = function.clone();
                let mut input = input.clone();

                if let Some(dtypes) =
                    functions::get_function_dtypes(&input, expr_arena, schema, &function)?
                {
                    let self_e = input[0].clone();
                    let (self_ae, type_self) =
                        unpack!(get_aexpr_and_type(expr_arena, self_e.node(), schema));
                    let mut super_type = type_self.clone();
                    match casting_rules {
                        CastingRules::Supertype(super_type_opts) => {
                            for other in &input[1..] {
                                let (other, type_other) =
                                    unpack!(get_aexpr_and_type(expr_arena, other.node(), schema));

                                let Some(new_st) = get_supertype_with_options(
                                    &super_type,
                                    &type_other,
                                    super_type_opts,
                                ) else {
                                    raise_supertype(&function, &input, schema, expr_arena)?;
                                    unreachable!()
                                };
                                if input.len() == 2 {
                                    // modify_supertype is a bit more conservative of casting columns
                                    // to literals
                                    super_type = modify_supertype(
                                        new_st,
                                        self_ae,
                                        other,
                                        &type_self,
                                        &type_other,
                                    )
                                } else {
                                    // when dealing with more than 1 argument, we simply find the supertypes
                                    super_type = new_st
                                }
                            }
                        },
                        CastingRules::FirstArgLossless => {
                            for other in &input[1..] {
                                let other = other.dtype(schema, expr_arena)?;
                                can_cast_to_lossless(&super_type, other)?;
                            }
                        },
                    }

                    if matches!(super_type, DataType::Unknown(UnknownKind::Any)) {
                        raise_supertype(&function, &input, schema, expr_arena)?;
                        unreachable!()
                    }

                    match super_type {
                        DataType::Unknown(UnknownKind::Float) => super_type = DataType::Float64,
                        DataType::Unknown(UnknownKind::Int(v)) => {
                            super_type = materialize_dyn_int(v).dtype()
                        },
                        _ => {},
                    }

                    // A decimal supertype may not hold every value, raise instead of
                    // producing nulls.
                    let literal_options = if super_type.leaf_dtype().is_decimal() {
                        CastOptions::Strict
                    } else {
                        CastOptions::NonStrict
                    };
                    for (e, dtype) in input.iter_mut().zip(dtypes) {
                        cast_expr_ir(e, &dtype, &super_type, expr_arena, literal_options)?;
                    }
                }

                // Ensure we don't go through this on next iteration.
                options.cast_options = None;
                Some(AExpr::Function {
                    function,
                    input,
                    options,
                })
            },
            #[cfg(all(feature = "temporal", feature = "dtype-duration"))]
            AExpr::Function {
                function: IRFunctionExpr::TemporalExpr(IRTemporalFunction::Duration(_)),
                ..
            } => coerce_function_inputs(
                expr_node,
                expr_arena,
                schema,
                CastOptions::Strict,
                |i, dtype| match dtype {
                    DataType::Int64 | DataType::Float64 => Ok(None),
                    dt if dt.is_integer() => Ok(Some(DataType::Int64)),
                    dt if dt.is_float() => Ok(Some(DataType::Float64)),
                    dt => polars_bail!(
                        InvalidOperation: "expected integer or float dtype, (got {dt}) in input {i} of duration"
                    ),
                },
            )?,
            #[cfg(feature = "business")]
            AExpr::Function {
                function: IRFunctionExpr::Business(ref business_fn),
                ref input,
                options,
            } => {
                let holiday_arg_idx: usize = match business_fn {
                    IRBusinessFunction::AddBusinessDay { .. }
                    | IRBusinessFunction::BusinessDayCount { .. } => 2,
                    IRBusinessFunction::IsBusinessDay { .. } => 1,
                };

                let holiday_arg = unpack!(input.get(holiday_arg_idx));

                // We implode, only for literal Series(dtype=Date), as this is considered a valid
                // parameter on the Python API as an `Iterable[date]`.
                let new_lv_ae: AExpr = match expr_arena.get(holiday_arg.node()) {
                    AExpr::Literal(LiteralValue::Series(s)) if s.dtype() == &DataType::Date => {
                        AExpr::Literal(LiteralValue::Series(SpecialEq::new(
                            s.implode().unwrap().into_series(),
                        )))
                    },
                    ae => {
                        let dtype = ae.to_dtype(&ToFieldContext::new(expr_arena, schema))?;

                        let is_list_of_date = match &dtype {
                            DataType::List(inner) => inner.as_ref() == &DataType::Date,
                            _ => false,
                        };

                        polars_ensure!(
                            is_list_of_date,
                            ComputeError:
                            "dtype of holidays list must be List(Date), got {dtype:?} instead"
                        );

                        return Ok(None);
                    },
                };

                let mut input = input.clone();
                let function = IRFunctionExpr::Business(business_fn.clone());
                input[holiday_arg_idx].set_node(expr_arena.add(new_lv_ae));

                Some(AExpr::Function {
                    input,
                    function,
                    options,
                })
            },
            #[cfg(feature = "list_gather")]
            AExpr::Function {
                function: IRFunctionExpr::ListExpr(IRListFunction::Gather(_)),
                ref input,
                ..
            } => {
                let (_, type_left) =
                    unpack!(get_aexpr_and_type(expr_arena, input[0].node(), schema));
                let (_, type_other) =
                    unpack!(get_aexpr_and_type(expr_arena, input[1].node(), schema));

                let DataType::List(inner_dtype) = &type_other else {
                    polars_bail!(InvalidOperation: "`list.gather` indices must be a list of integers, not a flat {type_other}. Use `implode` to wrap the flat value into a list.");
                };

                polars_ensure!(
                    inner_dtype.is_integer(),
                    op = "list.gather",
                    type_left,
                    type_other
                );
                None
            },
            #[cfg(all(feature = "strings", feature = "find_many"))]
            AExpr::Function {
                function:
                    ref function @ IRFunctionExpr::StringExpr(
                        IRStringFunction::ContainsAny { .. }
                        | IRStringFunction::FindMany { .. }
                        | IRStringFunction::ExtractMany { .. },
                    ),
                ref input,
                ..
            } => {
                let (_, type_left) =
                    unpack!(get_aexpr_and_type(expr_arena, input[0].node(), schema));
                let (_, type_other) =
                    unpack!(get_aexpr_and_type(expr_arena, input[1].node(), schema));

                let DataType::List(inner_dtype) = &type_other else {
                    polars_bail!(InvalidOperation: "`{function}` with a flat string datatype is invalid. Use `implode` to wrap the string value into a list.");
                };

                polars_ensure!(
                    type_left.is_string() && inner_dtype.is_string(),
                    op = format!("{function}"),
                    type_left,
                    type_other
                );
                None
            },

            #[cfg(feature = "string_pad")]
            AExpr::Function {
                function:
                    IRFunctionExpr::StringExpr(
                        IRStringFunction::PadStart { .. }
                        | IRStringFunction::PadEnd { .. }
                        | IRStringFunction::ZFill,
                    ),
                ..
            } => coerce_function_inputs(
                expr_node,
                expr_arena,
                schema,
                CastOptions::Strict,
                |i, _| Ok((i == 1).then_some(DataType::UInt64)), // length
            )?,

            #[cfg(all(feature = "strings", feature = "concat_str"))]
            AExpr::Function {
                function: IRFunctionExpr::StringExpr(IRStringFunction::ConcatHorizontal { .. }),
                ..
            } => coerce_function_inputs(
                expr_node,
                expr_arena,
                schema,
                CastOptions::NonStrict,
                |_, dtype| Ok((!dtype.is_string()).then_some(DataType::String)),
            )?,
            #[cfg(all(feature = "strings", feature = "find_many"))]
            AExpr::Function {
                function: IRFunctionExpr::StringExpr(IRStringFunction::ReplaceMany { .. }),
                ref input,
                ..
            } => {
                let (_, type_left) =
                    unpack!(get_aexpr_and_type(expr_arena, input[0].node(), schema));
                let (_, type_patterns) =
                    unpack!(get_aexpr_and_type(expr_arena, input[1].node(), schema));
                let (_, type_replace_with) =
                    unpack!(get_aexpr_and_type(expr_arena, input[2].node(), schema));

                let DataType::List(type_patterns_inner_dtype) = &type_patterns else {
                    polars_bail!(InvalidOperation: "`str.replace_many` with a flat {type_patterns} datatype as pattern is invalid. Use `implode` to wrap the string value into a list.");
                };
                let DataType::List(type_replace_with_inner_dtype) = &type_replace_with else {
                    polars_bail!(InvalidOperation: "`str.replace_many` with a flat {type_replace_with} datatype as replacement is invalid. Use `implode` to wrap the string value into a list.");
                };

                polars_ensure!(
                    type_left.is_string()
                        && type_patterns_inner_dtype.is_string()
                        && type_replace_with_inner_dtype.is_string(),
                    op = "str.replace_many",
                    type_left,
                    type_patterns,
                    type_replace_with
                );
                None
            },
            #[cfg(feature = "replace")]
            AExpr::Function {
                function:
                    ref function @ (IRFunctionExpr::Replace | IRFunctionExpr::ReplaceStrict { .. }),
                ref input,
                options,
            } => {
                let (_, type_old) =
                    unpack!(get_aexpr_and_type(expr_arena, input[1].node(), schema));
                let (_, type_new) =
                    unpack!(get_aexpr_and_type(expr_arena, input[2].node(), schema));

                polars_ensure!(
                    !type_old.contains_objects() && !type_new.contains_objects(),
                    InvalidOperation: "`replace` does not support `old`/`new` values of object dtype"
                );

                let (DataType::List(_), DataType::List(_)) = (&type_old, &type_new) else {
                    let function = function.clone();
                    let mut input = input.clone();

                    if !type_old.is_list() {
                        let other_input = expr_arena.add(AExpr::Agg(IRAggExpr::Implode {
                            input: input[1].node(),
                            maintain_order: true,
                        }));
                        input[1].set_node(other_input);
                    }
                    if !type_new.is_list() {
                        let other_input = expr_arena.add(AExpr::Agg(IRAggExpr::Implode {
                            input: input[2].node(),
                            maintain_order: true,
                        }));
                        input[2].set_node(other_input);
                    }

                    return Ok(Some(AExpr::Function {
                        function,
                        input,
                        options,
                    }));
                };
                None
            },
            #[cfg(feature = "range")]
            AExpr::Function {
                function:
                    ref
                    function @ IRFunctionExpr::Range(IRRangeFunction::IntRange { step: _, ref dtype }),
                ref input,
                options,
            } => {
                polars_ensure!(dtype.is_integer(), ComputeError: "non-integer `dtype` passed to `int_range`: {:?}", dtype);

                let (_, type_start) =
                    unpack!(get_aexpr_and_type(expr_arena, input[0].node(), schema));
                let (_, type_end) =
                    unpack!(get_aexpr_and_type(expr_arena, input[1].node(), schema));

                polars_ensure!(type_start.is_numeric() || type_start.is_null(), InvalidOperation: "`start` must be numeric for `int_range`, got {}", type_start);
                polars_ensure!(type_end.is_numeric() || type_end.is_null(), InvalidOperation: "`end` must be numeric for `int_range`, got {}", type_end);

                if [&type_start, &type_end]
                    .into_iter()
                    .all(|arg_dtype| arg_dtype == dtype)
                {
                    return Ok(None);
                }

                let function = function.clone();
                let dtype = dtype.clone();
                let mut input = input.clone();
                for (i, arg_dtype) in [type_start, type_end].into_iter().enumerate() {
                    cast_expr_ir(
                        &mut input[i],
                        &arg_dtype,
                        &dtype,
                        expr_arena,
                        CastOptions::Strict,
                    )?;
                }

                Some(AExpr::Function {
                    function,
                    input,
                    options,
                })
            },
            #[cfg(feature = "range")]
            AExpr::Function {
                function: IRFunctionExpr::Range(IRRangeFunction::IntRanges { .. }),
                ..
            } => coerce_function_inputs(
                expr_node,
                expr_arena,
                schema,
                CastOptions::Strict,
                |i, dtype| {
                    let name = ["start", "end", "step"][i];
                    polars_ensure!(
                        dtype.is_numeric() || dtype.is_null(),
                        InvalidOperation: "`{name}` must be numeric for `int_ranges`, got {dtype}"
                    );
                    Ok(Some(DataType::Int64))
                },
            )?,
            // The estimate casts the quantile to `Float64`, so give a dynamic literal
            // that dtype rather than leaving it unknown in the plan.
            #[cfg(feature = "approx_quantile")]
            AExpr::Function {
                function: IRFunctionExpr::ApproxQuantileEstimate { .. },
                ..
            } => coerce_function_inputs(
                expr_node,
                expr_arena,
                schema,
                CastOptions::Strict,
                |i, dtype| {
                    let is_dyn_number = matches!(
                        dtype,
                        DataType::Unknown(UnknownKind::Int(_) | UnknownKind::Float)
                    );
                    Ok((i == 1 && is_dyn_number).then_some(DataType::Float64))
                },
            )?,
            #[cfg(feature = "moment")]
            AExpr::Function {
                function: IRFunctionExpr::Skew(..) | IRFunctionExpr::Kurtosis(..),
                ..
            } => coerce_function_inputs(
                expr_node,
                expr_arena,
                schema,
                CastOptions::Strict,
                |i, _| Ok((i == 0).then_some(DataType::Float64)),
            )?,
            #[cfg(all(feature = "range", feature = "dtype-date"))]
            AExpr::Function {
                function:
                    ref function @ IRFunctionExpr::Range(IRRangeFunction::DateRange {
                        interval: _,
                        closed: _,
                        arg_type,
                    })
                    | ref function @ IRFunctionExpr::Range(IRRangeFunction::DateRanges {
                        interval: _,
                        closed: _,
                        arg_type,
                    }),
                ref input,
                options,
            } => {
                let (from_types, to_types) = match arg_type {
                    DateRangeArgs::StartEndInterval => {
                        let start = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let end = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        ensure_datetime!(start);
                        ensure_datetime!(end);
                        let from_types = [Some(start), Some(end), None];
                        let to_types = [Some(DataType::Date), Some(DataType::Date), None];
                        (from_types, to_types)
                    },
                    DateRangeArgs::StartEndSamples => {
                        let start = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let end = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        let num_samples = try_get_dtype(expr_arena, input[2].node(), schema)?;
                        ensure_datetime!(start);
                        ensure_datetime!(end);
                        ensure_int!(num_samples);
                        let from_types = [Some(start), Some(end), Some(num_samples)];
                        let to_types = [
                            Some(DataType::Date),
                            Some(DataType::Date),
                            Some(DataType::Int64),
                        ];
                        (from_types, to_types)
                    },
                    DateRangeArgs::StartIntervalSamples => {
                        let start = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let num_samples = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        ensure_datetime!(start);
                        ensure_int!(num_samples);
                        let from_types = [Some(start), Some(num_samples), None];
                        let to_types = [Some(DataType::Date), Some(DataType::Int64), None];
                        (from_types, to_types)
                    },
                    DateRangeArgs::EndIntervalSamples => {
                        let end = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let num_samples = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        ensure_datetime!(end);
                        ensure_int!(num_samples);
                        let from_types = [Some(end), Some(num_samples), None];
                        let to_types = [Some(DataType::Date), Some(DataType::Int64), None];
                        (from_types, to_types)
                    },
                };

                let from_iter = from_types.into_iter();
                let to_iter = to_types.into_iter();
                let mut input = input.clone();
                let function = function.clone();
                let mut modified = false;
                for (i, (from_dtype, to_dtype)) in from_iter.zip(to_iter).enumerate() {
                    if let (Some(from_dt), Some(to_dt)) = (from_dtype, to_dtype) {
                        if from_dt != to_dt {
                            modified = true;
                            coerce_temporal_dt(&from_dt, &to_dt, &mut input[i], expr_arena)?;
                        }
                    }
                }

                if modified {
                    Some(AExpr::Function {
                        function,
                        input,
                        options,
                    })
                } else {
                    return Ok(None);
                }
            },
            #[cfg(all(feature = "range", feature = "dtype-datetime"))]
            AExpr::Function {
                function:
                    ref function @ IRFunctionExpr::Range(IRRangeFunction::DatetimeRange {
                        ref interval,
                        closed: _,
                        time_unit: ref tu,
                        time_zone: ref tz,
                        arg_type,
                    })
                    | ref function @ IRFunctionExpr::Range(IRRangeFunction::DatetimeRanges {
                        ref interval,
                        closed: _,
                        time_unit: ref tu,
                        time_zone: ref tz,
                        arg_type,
                    }),
                ref input,
                options,
            } => {
                let (from_types, to_types) = match arg_type {
                    DateRangeArgs::StartEndInterval => {
                        let start = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let end = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        ensure_datetime!(start);
                        ensure_datetime!(end);
                        let initial_st = try_get_supertype(&start, &end).unwrap();
                        let supertype = temporal_range_output_type(initial_st, tu, tz, interval)?;
                        let from_types = [Some(start), Some(end), None];
                        let to_types = [Some(supertype.clone()), Some(supertype), None];
                        (from_types, to_types)
                    },
                    DateRangeArgs::StartEndSamples => {
                        let start = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let end = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        let num_samples = try_get_dtype(expr_arena, input[2].node(), schema)?;
                        ensure_datetime!(start);
                        ensure_datetime!(end);
                        ensure_int!(num_samples);
                        let initial_st = try_get_supertype(&start, &end)?;
                        let supertype = temporal_range_output_type(initial_st, tu, tz, interval)?;
                        let from_types = [Some(start), Some(end), Some(num_samples)];
                        let to_types = [
                            Some(supertype.clone()),
                            Some(supertype),
                            Some(DataType::Int64),
                        ];
                        (from_types, to_types)
                    },
                    DateRangeArgs::StartIntervalSamples => {
                        let start = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let num_samples = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        ensure_datetime!(start);
                        ensure_int!(num_samples);
                        let supertype =
                            temporal_range_output_type(start.clone(), tu, tz, interval)?;
                        let from_types = [Some(start), Some(num_samples), None];
                        let to_types = [Some(supertype), Some(DataType::Int64), None];
                        (from_types, to_types)
                    },
                    DateRangeArgs::EndIntervalSamples => {
                        let end = try_get_dtype(expr_arena, input[0].node(), schema)?;
                        let num_samples = try_get_dtype(expr_arena, input[1].node(), schema)?;
                        ensure_datetime!(end);
                        ensure_int!(num_samples);
                        let supertype = temporal_range_output_type(end.clone(), tu, tz, interval)?;
                        let from_types = [Some(end), Some(num_samples), None];
                        let to_types = [Some(supertype), Some(DataType::Int64), None];
                        (from_types, to_types)
                    },
                };

                let from_iter = from_types.into_iter();
                let to_iter = to_types.into_iter();
                let mut input = input.clone();
                let function = function.clone();
                let mut modified = false;
                for (i, (from_dtype, to_dtype)) in from_iter.zip(to_iter).enumerate() {
                    if let (Some(from_dt), Some(to_dt)) = (from_dtype, to_dtype) {
                        if from_dt != to_dt {
                            modified = true;
                            coerce_temporal_dt(&from_dt, &to_dt, &mut input[i], expr_arena)?;
                        }
                    }
                }

                if modified {
                    Some(AExpr::Function {
                        function,
                        input,
                        options,
                    })
                } else {
                    return Ok(None);
                }
            },
            AExpr::Slice { offset, length, .. } => {
                let (_, offset_dtype) = unpack!(get_aexpr_and_type(expr_arena, offset, schema));
                polars_ensure!(offset_dtype.is_integer(), InvalidOperation: "offset must be integral for slice expression, not {}", offset_dtype);
                let (_, length_dtype) = unpack!(get_aexpr_and_type(expr_arena, length, schema));
                polars_ensure!(length_dtype.is_integer() || length_dtype.is_null(), InvalidOperation: "length must be integral for slice expression, not {}", length_dtype);
                None
            },
            _ => None,
        };
        Ok(out)
    }
```


---

### 🔹 Commit #05: `e6994a58`
- **完整 Hash**: `e6994a587648575318ed8f36b1c01794ab3117c5`
- **說明 (Ground Truth)**: fix: Correctly parse timestamps with offsets in JSON (#30064)
- **變更檔案數**: 3

#### 📄 檔案: `crates/polars-arrow/src/temporal_conversions.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:103, E:91, A:0) ➔ After(N:85, E:74, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 18, +Edges: 0, -Edges: 17, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `r.is_some (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `parsed
            .to_datetime (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `tz.from_utc_datetime (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `x.timestamp_micros (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `parsed
            .to_datetime()
            .map(|x| x.naive_utc())
            .map(|x| tz.from_utc_datetime(&x))
            .map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `x.timestamp_millis (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `x.timestamp (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `StrftimeItems::new (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `x.timestamp_nanos_opt().unwrap (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `x.timestamp_nanos_opt (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `utf8_to_timestamp_scalar` (FUNCTION_DEF)
  • - [移除節點] `parsed
            .to_datetime()
            .map(|x| x.naive_utc())
            .map(|x| tz.from_utc_datetime(&x))
            .map(|x| match tu {
                TimeUnit::Second => x.timestamp(),
                TimeUnit::Millisecond => x.timestamp_millis(),
                TimeUnit::Microsecond => x.timestamp_micros(),
                TimeUnit::Nanosecond => x.timestamp_nanos_opt().unwrap(),
            })
            .ok (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `parsed
            .to_datetime()
            .map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `Parsed::new (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `parse (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 20 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `crates/polars-compute/src/cast/temporal.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:27, E:23, A:0) ➔ After(N:35, E:31, A:0)
- **差分統計**: +Nodes: 21, -Nodes: 13, +Edges: 22, -Edges: 14, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `parse(&mut parsed, rest, StrftimeItems::new("%#z")).ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `utf8_to_timestamp_scalar` (FUNCTION_DEF)
  • + [新增節點] `parsed.to_naive_datetime_with_offset(0).ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `parsed.to_naive_datetime_with_offset (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `parsed.to_datetime().ok()?.naive_utc (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `parse_and_remainder(&mut parsed, value, StrftimeItems::new("%Y-%m-%d")).ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `dt.timestamp_nanos_opt (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `parse_and_remainder(&mut parsed, rest, StrftimeItems::new("%H:%M")).ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `parsed.to_datetime (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `parsed.to_datetime().ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `dt.timestamp (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `dt.and_utc (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `rest.starts_with (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `parse_and_remainder (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 55 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `crates/polars-json/src/json/deserialize.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:140, E:220, A:0) ➔ After(N:134, E:214, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 7, +Edges: 1, -Edges: 7, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `utf8_to_timestamp_scalar (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `temporal_conversions::parse_offset (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `polars_compute::cast::temporal::utf8_to_naive_timestamp_scalar (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `tz
                .as_ref()
                .map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `tz
                .as_ref (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `temporal_conversions::utf8_to_timestamp_scalar (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `tz
                .as_ref()
                .map(|tz| temporal_conversions::parse_offset(tz.as_str()))
                .transpose (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `tz.as_str (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `_deserialize` ──[CALLS]──> `utf8_to_timestamp_scalar (External/Unresolved)`
  • - [移除呼叫邊] `_deserialize` ──[CALLS]──> `tz
                .as_ref()
                .map(|tz| temporal_conversions::parse_offset(tz.as_str()))
                .transpose (External/Unresolved)`
  • - [移除呼叫邊] `_deserialize` ──[CALLS]──> `tz
                .as_ref()
                .map (External/Unresolved)`
  • - [移除呼叫邊] `_deserialize` ──[CALLS]──> `tz
                .as_ref (External/Unresolved)`
  • - [移除呼叫邊] `_deserialize` ──[CALLS]──> `temporal_conversions::parse_offset (External/Unresolved)`
  • - [移除呼叫邊] `_deserialize` ──[CALLS]──> `tz.as_str (External/Unresolved)`
  • - [移除呼叫邊] `_deserialize` ──[CALLS]──> `polars_compute::cast::temporal::utf8_to_naive_timestamp_scalar (External/Unresolved)`
  • _... 以及其餘 1 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 2 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_deserialize()`
- **變更前簽章 (Before)**: `fn _deserialize(
    rows: &[A],
    dtype: ArrowDataType,
    allow_extra_fields_in_struct: bool,
)` (L411~L539)
- **變更後簽章 (After)**: `fn _deserialize(
    rows: &[A],
    dtype: ArrowDataType,
    allow_extra_fields_in_struct: bool,
)` (L413~L532)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn _deserialize<'a, A: Borrow<BorrowedValue<'a>>>(
    rows: &[A],
    dtype: ArrowDataType,
    allow_extra_fields_in_struct: bool,
) -> PolarsResult<Box<dyn Array>> {
    match &dtype {
        ArrowDataType::Null => {
            if let Some(err_idx) = (0..rows.len())
                .find(|i| !matches!(rows[*i].borrow(), BorrowedValue::Static(StaticNode::Null)))
            {
                check_err_idx(rows, err_idx, "null")?;
            }

            Ok(Box::new(NullArray::new(dtype, rows.len())))
        },
        ArrowDataType::Boolean => {
            fill_generic_array_from::<_, _, BooleanArray>(deserialize_boolean_into, rows)
        },
        ArrowDataType::Int8 => {
            fill_array_from::<_, _, PrimitiveArray<i8>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Int16 => {
            fill_array_from::<_, _, PrimitiveArray<i16>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Int32 | ArrowDataType::Interval(IntervalUnit::YearMonth) => {
            fill_array_from::<_, _, PrimitiveArray<i32>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Interval(IntervalUnit::DayTime) => {
            unimplemented!("There is no natural representation of DayTime in JSON.")
        },
        ArrowDataType::Int64 | ArrowDataType::Duration(_) => {
            fill_array_from::<_, _, PrimitiveArray<i64>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Date32 => {
            deserialize_temporal_primitive::<i32, _>(rows, dtype, "date", utf8_to_naive_date_scalar)
        },
        ArrowDataType::Date64 => {
            deserialize_temporal_primitive::<i64, _>(rows, dtype, "date", |s| {
                utf8_to_naive_date_scalar(s)
                    .map(|d| d as i64 * temporal_conversions::MILLISECONDS_IN_DAY)
            })
        },
        ArrowDataType::Time32(tu) => {
            let tu = *tu;
            deserialize_temporal_primitive::<i32, _>(rows, dtype, "time", |s| {
                utf8_to_naive_time_scalar(s, tu).and_then(|v| i32::try_from(v).ok())
            })
        },
        ArrowDataType::Time64(tu) => {
            let tu = *tu;
            deserialize_temporal_primitive::<i64, _>(rows, dtype, "time", |s| {
                utf8_to_naive_time_scalar(s, tu)
            })
        },
        ArrowDataType::Int128 => {
            fill_array_from::<_, _, PrimitiveArray<i128>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Timestamp(tu, tz) => {
            let tz_offset = tz
                .as_ref()
                .map(|tz| temporal_conversions::parse_offset(tz.as_str()))
                .transpose()?;
            let mut err_idx = rows.len();
            let iter = rows.iter().enumerate().map(|(i, row)| match row.borrow() {
                BorrowedValue::Static(StaticNode::I64(v)) => Some(*v),
                BorrowedValue::String(v) => match &tz_offset {
                    None => {
                        polars_compute::cast::temporal::utf8_to_naive_timestamp_scalar(v, "%+", tu)
                    },
                    Some(tz) => temporal_conversions::utf8_to_timestamp_scalar(v, "%+", tz, tu),
                },
                BorrowedValue::Static(StaticNode::Null) => None,
                _ => {
                    err_idx = if err_idx == rows.len() { i } else { err_idx };
                    None
                },
            });
            let out = Box::new(Int64Array::from_trusted_len_iter(iter).to(dtype));
            check_err_idx(rows, err_idx, "timestamp")?;
            Ok(out)
        },
        ArrowDataType::UInt8 => {
            fill_array_from::<_, _, PrimitiveArray<u8>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::UInt16 => {
            fill_array_from::<_, _, PrimitiveArray<u16>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::UInt32 => {
            fill_array_from::<_, _, PrimitiveArray<u32>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::UInt64 => {
            fill_array_from::<_, _, PrimitiveArray<u64>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::UInt128 => {
            fill_array_from::<_, _, PrimitiveArray<u128>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Float16 => {
            fill_array_from::<_, _, PrimitiveArray<pf16>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Float32 => {
            fill_array_from::<_, _, PrimitiveArray<f32>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Float64 => {
            fill_array_from::<_, _, PrimitiveArray<f64>>(deserialize_primitive_into, dtype, rows)
        },
        #[cfg(feature = "dtype-decimal")]
        ArrowDataType::Decimal(_, _) => Ok(Box::new(deserialize_decimal(rows, dtype)?)),
        ArrowDataType::LargeUtf8 => {
            fill_generic_array_from::<_, _, Utf8Array<i64>>(deserialize_utf8_into, rows)
        },
        ArrowDataType::Utf8View => {
            fill_generic_array_from::<_, _, Utf8ViewArray>(deserialize_utf8view_into, rows)
        },
        ArrowDataType::LargeList(_) => Ok(Box::new(deserialize_list(
            rows,
            dtype,
            allow_extra_fields_in_struct,
        )?)),
        ArrowDataType::LargeBinary => Ok(Box::new(deserialize_binary(rows)?)),
        ArrowDataType::Struct(_) => Ok(Box::new(deserialize_struct(
            rows,
            dtype,
            allow_extra_fields_in_struct,
        )?)),
        adt => polars_bail!(
            ComputeError: "deserialization from JSON is not implemented for `{adt:?}`"
        ),
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn _deserialize<'a, A: Borrow<BorrowedValue<'a>>>(
    rows: &[A],
    dtype: ArrowDataType,
    allow_extra_fields_in_struct: bool,
) -> PolarsResult<Box<dyn Array>> {
    match &dtype {
        ArrowDataType::Null => {
            if let Some(err_idx) = (0..rows.len())
                .find(|i| !matches!(rows[*i].borrow(), BorrowedValue::Static(StaticNode::Null)))
            {
                check_err_idx(rows, err_idx, "null")?;
            }

            Ok(Box::new(NullArray::new(dtype, rows.len())))
        },
        ArrowDataType::Boolean => {
            fill_generic_array_from::<_, _, BooleanArray>(deserialize_boolean_into, rows)
        },
        ArrowDataType::Int8 => {
            fill_array_from::<_, _, PrimitiveArray<i8>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Int16 => {
            fill_array_from::<_, _, PrimitiveArray<i16>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Int32 | ArrowDataType::Interval(IntervalUnit::YearMonth) => {
            fill_array_from::<_, _, PrimitiveArray<i32>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Interval(IntervalUnit::DayTime) => {
            unimplemented!("There is no natural representation of DayTime in JSON.")
        },
        ArrowDataType::Int64 | ArrowDataType::Duration(_) => {
            fill_array_from::<_, _, PrimitiveArray<i64>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Date32 => {
            deserialize_temporal_primitive::<i32, _>(rows, dtype, "date", utf8_to_naive_date_scalar)
        },
        ArrowDataType::Date64 => {
            deserialize_temporal_primitive::<i64, _>(rows, dtype, "date", |s| {
                utf8_to_naive_date_scalar(s)
                    .map(|d| d as i64 * temporal_conversions::MILLISECONDS_IN_DAY)
            })
        },
        ArrowDataType::Time32(tu) => {
            let tu = *tu;
            deserialize_temporal_primitive::<i32, _>(rows, dtype, "time", |s| {
                utf8_to_naive_time_scalar(s, tu).and_then(|v| i32::try_from(v).ok())
            })
        },
        ArrowDataType::Time64(tu) => {
            let tu = *tu;
            deserialize_temporal_primitive::<i64, _>(rows, dtype, "time", |s| {
                utf8_to_naive_time_scalar(s, tu)
            })
        },
        ArrowDataType::Int128 => {
            fill_array_from::<_, _, PrimitiveArray<i128>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Timestamp(tu, _) => {
            let mut err_idx = rows.len();
            let iter = rows.iter().enumerate().map(|(i, row)| match row.borrow() {
                BorrowedValue::Static(StaticNode::I64(v)) => Some(*v),
                BorrowedValue::String(v) => utf8_to_timestamp_scalar(v, *tu),
                BorrowedValue::Static(StaticNode::Null) => None,
                _ => {
                    err_idx = if err_idx == rows.len() { i } else { err_idx };
                    None
                },
            });
            let out = Box::new(Int64Array::from_trusted_len_iter(iter).to(dtype));
            check_err_idx(rows, err_idx, "timestamp")?;
            Ok(out)
        },
        ArrowDataType::UInt8 => {
            fill_array_from::<_, _, PrimitiveArray<u8>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::UInt16 => {
            fill_array_from::<_, _, PrimitiveArray<u16>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::UInt32 => {
            fill_array_from::<_, _, PrimitiveArray<u32>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::UInt64 => {
            fill_array_from::<_, _, PrimitiveArray<u64>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::UInt128 => {
            fill_array_from::<_, _, PrimitiveArray<u128>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Float16 => {
            fill_array_from::<_, _, PrimitiveArray<pf16>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Float32 => {
            fill_array_from::<_, _, PrimitiveArray<f32>>(deserialize_primitive_into, dtype, rows)
        },
        ArrowDataType::Float64 => {
            fill_array_from::<_, _, PrimitiveArray<f64>>(deserialize_primitive_into, dtype, rows)
        },
        #[cfg(feature = "dtype-decimal")]
        ArrowDataType::Decimal(_, _) => Ok(Box::new(deserialize_decimal(rows, dtype)?)),
        ArrowDataType::LargeUtf8 => {
            fill_generic_array_from::<_, _, Utf8Array<i64>>(deserialize_utf8_into, rows)
        },
        ArrowDataType::Utf8View => {
            fill_generic_array_from::<_, _, Utf8ViewArray>(deserialize_utf8view_into, rows)
        },
        ArrowDataType::LargeList(_) => Ok(Box::new(deserialize_list(
            rows,
            dtype,
            allow_extra_fields_in_struct,
        )?)),
        ArrowDataType::LargeBinary => Ok(Box::new(deserialize_binary(rows)?)),
        ArrowDataType::Struct(_) => Ok(Box::new(deserialize_struct(
            rows,
            dtype,
            allow_extra_fields_in_struct,
        )?)),
        adt => polars_bail!(
            ComputeError: "deserialization from JSON is not implemented for `{adt:?}`"
        ),
    }
}
```


---

### 🔹 Commit #06: `f2f8d1e8`
- **完整 Hash**: `f2f8d1e8e6b35eded7de87d0ea7599874c97df8a`
- **說明 (Ground Truth)**: fix: Use the correct input schema for join expressions in the expression optimizer (#30053)
- **變更檔案數**: 3

#### 📄 檔案: `crates/polars-plan/src/plans/ir/inputs.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:91, E:111, A:0) ➔ After(N:93, E:113, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `IR::expr_schema` (FUNCTION_DEF)
  • + [新增節點] `ExprSchema::Input (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `IR::expr_schema` ──[CALLS]──> `IR::expr_schema`
  • + [新增呼叫邊] `IR::expr_schema` ──[CALLS]──> `ExprSchema::Input (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `crates/polars-plan/src/plans/optimizer/stack_opt.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:45, E:47, A:0) ➔ After(N:53, E:55, A:0)
- **差分統計**: +Nodes: 12, -Nodes: 4, +Edges: 12, -Edges: 4, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `is_scan (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `lp_arena.get(input).schema (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `scratch.drain(..).enumerate (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `scratch.drain(..).enumerate().rev (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `plan.schema (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `plan.expr_schema (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `schema_stack.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `plan.schema(lp_arena).into_owned (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `scratch.drain (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `plan.inputs (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `get_input_schema(lp_arena, current_node).into_owned (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `lp_arena.get(input).schema(lp_arena).into_owned (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `get_input (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `get_input(lp_arena, current_node).is_empty (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `input_schema.into_owned (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 17 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `StackOptimizer::optimize_loop()`
- **變更前簽章 (Before)**: `fn StackOptimizer::optimize_loop(
        &self,
        rules: &mut [Box<dyn OptimizationRule>],
        expr_arena: &mut Arena<AExpr>,
        lp_arena: &mut Arena<IR>,
        lp_top: Node,
    )` (L17~L135)
- **變更後簽章 (After)**: `fn StackOptimizer::optimize_loop(
        &self,
        rules: &mut [Box<dyn OptimizationRule>],
        expr_arena: &mut Arena<AExpr>,
        lp_arena: &mut Arena<IR>,
        lp_top: Node,
    )` (L19~L153)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn optimize_loop(
        &self,
        rules: &mut [Box<dyn OptimizationRule>],
        expr_arena: &mut Arena<AExpr>,
        lp_arena: &mut Arena<IR>,
        lp_top: Node,
    ) -> PolarsResult<Node> {
        let mut changed = true;

        // Nodes of expressions and lp node from which the expressions are a member of.
        let mut plans = vec![];
        let mut exprs = vec![];
        let mut scratch = vec![];
        let mut children = vec![];
        let mut schema_stack: Vec<Arc<Schema>> = vec![];

        // Run loop until reaching fixed point.
        #[allow(clippy::field_reassign_with_default)]
        while changed {
            // Recurse into sub plans and expressions and apply rules.
            changed = false;

            plans.push(lp_top);
            while let Some(current_node) = plans.pop() {
                // Apply rules
                for rule in rules.iter_mut() {
                    // keep iterating over same rule
                    while let Some(x) = rule.optimize_plan(lp_arena, expr_arena, current_node)? {
                        lp_arena.replace(current_node, x);
                        changed = true;
                    }
                }

                let plan = lp_arena.get(current_node);

                // traverse subplans and expressions and add to the stack
                plan.copy_exprs(&mut scratch);
                plan.copy_inputs(&mut plans);

                if scratch.is_empty() {
                    continue;
                }

                let input_schema = get_input_schema(lp_arena, current_node);

                schema_stack.clear();
                let schema_idx = 0;
                schema_stack.push(input_schema.into_owned());

                let is_filter = matches!(plan, IR::Filter { .. });
                while let Some(expr_ir) = scratch.pop() {
                    exprs.push((expr_ir.node(), schema_idx, is_filter));
                }

                let mut ctx = OptimizeExprContext::default();
                #[cfg(feature = "python")]
                {
                    use crate::dsl::python_dsl::PythonScanSource;
                    ctx.in_pyarrow_scan = matches!(plan, IR::PythonScan { options } if options.python_source == PythonScanSource::Pyarrow);
                    ctx.in_io_plugin = matches!(plan, IR::PythonScan { options } if options.python_source == PythonScanSource::IOPlugin);
                };
                ctx.has_inputs = !get_input(lp_arena, current_node).is_empty();

                // process the expressions on the stack and apply optimizations.
                while let Some((current_expr_node, schema_idx, is_filter_predicate)) = exprs.pop() {
                    ctx.is_filter_predicate = is_filter_predicate;
                    {
                        let expr = unsafe { expr_arena.get_unchecked(current_expr_node) };
                        if expr.is_leaf() {
                            continue;
                        }
                    }
                    let schema = &schema_stack[schema_idx];
                    for rule in rules.iter_mut() {
                        while let Some(x) =
                            rule.optimize_expr(expr_arena, current_expr_node, schema, ctx)?
                        {
                            expr_arena.replace(current_expr_node, x);
                            changed = true;
                        }
                    }
                    let expr = unsafe { expr_arena.get_unchecked(current_expr_node) };

                    // traverse subexpressions and add to the stack
                    match expr {
                        #[cfg(feature = "dtype-struct")]
                        AExpr::StructEval {
                            expr, evaluation, ..
                        } => {
                            let struct_field = expr_arena
                                .get(current_expr_node)
                                .to_field_impl(&ToFieldContext::new(expr_arena, schema))?;

                            let mut eval_schema = (**schema).clone();
                            eval_schema
                                .insert(get_pl_structfields_name(), struct_field.dtype().clone());
                            let eval_schema_idx = schema_stack.len();
                            schema_stack.push(Arc::new(eval_schema));

                            exprs.push((*expr, schema_idx, false));
                            for node in evaluation.iter().map(ExprIR::node).rev() {
                                exprs.push((node, eval_schema_idx, false));
                            }
                        },
                        expr => {
                            let is_filter_predicate =
                                is_filter_predicate && passes_on_filter_predicate(expr);
                            children.clear();
                            expr.inputs_rev(&mut children);
                            for node in children.drain(..) {
                                exprs.push((node, schema_idx, is_filter_predicate));
                            }
                        },
                    }
                }
            }
        }
        Ok(lp_top)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn optimize_loop(
        &self,
        rules: &mut [Box<dyn OptimizationRule>],
        expr_arena: &mut Arena<AExpr>,
        lp_arena: &mut Arena<IR>,
        lp_top: Node,
    ) -> PolarsResult<Node> {
        let mut changed = true;

        // Nodes of expressions and lp node from which the expressions are a member of.
        let mut plans = vec![];
        let mut exprs = vec![];
        let mut scratch = vec![];
        let mut children = vec![];
        let mut schema_stack: Vec<Arc<Schema>> = vec![];

        // Run loop until reaching fixed point.
        #[allow(clippy::field_reassign_with_default)]
        while changed {
            // Recurse into sub plans and expressions and apply rules.
            changed = false;

            plans.push(lp_top);
            while let Some(current_node) = plans.pop() {
                // Apply rules
                for rule in rules.iter_mut() {
                    // keep iterating over same rule
                    while let Some(x) = rule.optimize_plan(lp_arena, expr_arena, current_node)? {
                        lp_arena.replace(current_node, x);
                        changed = true;
                    }
                }

                let plan = lp_arena.get(current_node);

                // traverse subplans and expressions and add to the stack
                plan.copy_exprs(&mut scratch);
                plan.copy_inputs(&mut plans);

                if scratch.is_empty() {
                    continue;
                }

                let is_filter = matches!(plan, IR::Filter { .. });

                schema_stack.clear();
                for input in plan.inputs() {
                    schema_stack.push(lp_arena.get(input).schema(lp_arena).into_owned());
                }
                let has_inputs = !schema_stack.is_empty() || is_scan(plan);
                if schema_stack.is_empty() {
                    schema_stack.push(get_input_schema(lp_arena, current_node).into_owned());
                }

                let output_schema_idx = schema_stack.len();
                let mut uses_output_schema = false;
                for (idx, expr_ir) in scratch.drain(..).enumerate().rev() {
                    let schema_idx = match plan.expr_schema(idx) {
                        ExprSchema::Input(input_idx) => input_idx,
                        ExprSchema::Output => {
                            uses_output_schema = true;
                            output_schema_idx
                        },
                    };
                    exprs.push((expr_ir.node(), schema_idx, is_filter));
                }
                if uses_output_schema {
                    schema_stack.push(plan.schema(lp_arena).into_owned());
                }

                let mut ctx = OptimizeExprContext::default();
                #[cfg(feature = "python")]
                {
                    use crate::dsl::python_dsl::PythonScanSource;
                    ctx.in_pyarrow_scan = matches!(plan, IR::PythonScan { options } if options.python_source == PythonScanSource::Pyarrow);
                    ctx.in_io_plugin = matches!(plan, IR::PythonScan { options } if options.python_source == PythonScanSource::IOPlugin);
                };
                ctx.has_inputs = has_inputs;

                // process the expressions on the stack and apply optimizations.
                while let Some((current_expr_node, schema_idx, is_filter_predicate)) = exprs.pop() {
                    ctx.is_filter_predicate = is_filter_predicate;
                    {
                        let expr = unsafe { expr_arena.get_unchecked(current_expr_node) };
                        if expr.is_leaf() {
                            continue;
                        }
                    }
                    let schema = &schema_stack[schema_idx];
                    for rule in rules.iter_mut() {
                        while let Some(x) =
                            rule.optimize_expr(expr_arena, current_expr_node, schema, ctx)?
                        {
                            expr_arena.replace(current_expr_node, x);
                            changed = true;
                        }
                    }
                    let expr = unsafe { expr_arena.get_unchecked(current_expr_node) };

                    // traverse subexpressions and add to the stack
                    match expr {
                        #[cfg(feature = "dtype-struct")]
                        AExpr::StructEval {
                            expr, evaluation, ..
                        } => {
                            let struct_field = expr_arena
                                .get(current_expr_node)
                                .to_field_impl(&ToFieldContext::new(expr_arena, schema))?;

                            let mut eval_schema = (**schema).clone();
                            eval_schema
                                .insert(get_pl_structfields_name(), struct_field.dtype().clone());
                            let eval_schema_idx = schema_stack.len();
                            schema_stack.push(Arc::new(eval_schema));

                            exprs.push((*expr, schema_idx, false));
                            for node in evaluation.iter().map(ExprIR::node).rev() {
                                exprs.push((node, eval_schema_idx, false));
                            }
                        },
                        expr => {
                            let is_filter_predicate =
                                is_filter_predicate && passes_on_filter_predicate(expr);
                            children.clear();
                            expr.inputs_rev(&mut children);
                            for node in children.drain(..) {
                                exprs.push((node, schema_idx, is_filter_predicate));
                            }
                        },
                    }
                }
            }
        }
        Ok(lp_top)
    }
```


#### 📄 檔案: `crates/polars-plan/src/plans/options.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:140, E:136, A:0) ➔ After(N:142, E:139, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 3, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `JoinTypeOptionsIR::expr_schema` (FUNCTION_DEF)
  • + [新增節點] `ExprSchema::Input (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `JoinTypeOptionsIR::expr_schema` ──[CALLS]──> `JoinTypeOptionsIR::left_on_len`
  • + [新增呼叫邊] `JoinTypeOptionsIR::expr_schema` ──[CALLS]──> `ExprSchema::Input (External/Unresolved)`
  • + [新增呼叫邊] `JoinTypeOptionsIR::expr_schema` ──[CALLS]──> `JoinTypeOptionsIR::right_on_len`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #07: `d124aa38`
- **完整 Hash**: `d124aa38913d87a5a2c549ef156d81cd4e724004`
- **說明 (Ground Truth)**: fix: Sliced list writes in Avro (#30061)
- **變更檔案數**: 2

#### 📄 檔案: `crates/polars-arrow/src/io/avro/write/serialize.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:113, E:194, A:0) ➔ After(N:122, E:192, A:0)
- **差分統計**: +Nodes: 14, -Nodes: 5, +Edges: 25, -Edges: 27, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `write_list_items` (FUNCTION_DEF)
  • + [新增節點] `inner.advance (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `inner.next().unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `skip_list_items` (FUNCTION_DEF)
  • + [新增節點] `array.offsets (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `array
        .offsets()
        .lengths()
        .enumerate()
        .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `list_values_serializer` (FUNCTION_DEF)
  • + [新增節點] `array
        .offsets()
        .lengths()
        .enumerate (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `array.offsets().first().to_usize (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `array.is_valid (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `array.offsets().lengths (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `encode::zigzag_encode(length as i64, buf).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `array
        .offsets()
        .lengths (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `array.offsets().first (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `array
        .offsets()
        .buffer()
        .windows(2)
        .map (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 56 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `list_required()`
- **變更前簽章 (Before)**: `fn list_required(array: &'a ListArray<O>, schema: &AvroSchema)` (L98~L122)
- **變更後簽章 (After)**: `fn list_required(array: &'a ListArray<O>, schema: &AvroSchema)` (L125~L134)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn list_required<'a, O: Offset>(array: &'a ListArray<O>, schema: &AvroSchema) -> BoxSerializer<'a> {
    let mut inner = new_serializer(array.values().as_ref(), schema);
    let lengths = array
        .offsets()
        .buffer()
        .windows(2)
        .map(|w| (w[1] - w[0]).to_usize() as i64);

    Box::new(BufStreamingIterator::new(
        lengths,
        move |length, buf| {
            encode::zigzag_encode(length, buf).unwrap();
            let mut rows = 0;
            while let Some(item) = inner.next() {
                buf.extend_from_slice(item);
                rows += 1;
                if rows == length {
                    encode::zigzag_encode(0, buf).unwrap();
                    break;
                }
            }
        },
        vec![],
    ))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn list_required<'a, O: Offset>(array: &'a ListArray<O>, schema: &AvroSchema) -> BoxSerializer<'a> {
    let mut inner = list_values_serializer(array, schema);
    let lengths = array.offsets().lengths();

    Box::new(BufStreamingIterator::new(
        lengths,
        move |length, buf| write_list_items(&mut inner, length, buf),
        vec![],
    ))
}
```

### 🔹 函式: `list_optional()`
- **變更前簽章 (Before)**: `fn list_optional(array: &'a ListArray<O>, schema: &AvroSchema)` (L124~L154)
- **變更後簽章 (After)**: `fn list_optional(array: &'a ListArray<O>, schema: &AvroSchema)` (L136~L157)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn list_optional<'a, O: Offset>(array: &'a ListArray<O>, schema: &AvroSchema) -> BoxSerializer<'a> {
    let mut inner = new_serializer(array.values().as_ref(), schema);
    let lengths = array
        .offsets()
        .buffer()
        .windows(2)
        .map(|w| (w[1] - w[0]).to_usize() as i64);
    let lengths = ZipValidity::new_with_validity(lengths, array.validity());

    Box::new(BufStreamingIterator::new(
        lengths,
        move |length, buf| {
            if let Some(length) = length {
                buf.push(IS_VALID);
                encode::zigzag_encode(length, buf).unwrap();
                let mut rows = 0;
                while let Some(item) = inner.next() {
                    buf.extend_from_slice(item);
                    rows += 1;
                    if rows == length {
                        encode::zigzag_encode(0, buf).unwrap();
                        break;
                    }
                }
            } else {
                buf.push(IS_NULL);
            }
        },
        vec![],
    ))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn list_optional<'a, O: Offset>(array: &'a ListArray<O>, schema: &AvroSchema) -> BoxSerializer<'a> {
    let mut inner = list_values_serializer(array, schema);
    let rows = array
        .offsets()
        .lengths()
        .enumerate()
        .map(|(i, length)| (length, array.is_valid(i)));

    Box::new(BufStreamingIterator::new(
        rows,
        move |(length, is_valid), buf| {
            if is_valid {
                buf.push(IS_VALID);
                write_list_items(&mut inner, length, buf);
            } else {
                buf.push(IS_NULL);
                skip_list_items(&mut inner, length);
            }
        },
        vec![],
    ))
}
```


#### 📄 檔案: `crates/polars-io/src/avro/write.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:34, E:31, A:0) ➔ After(N:39, E:36, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 0, +Edges: 5, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `df.apply_columns (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `c.trim_lists_to_normalized_offsets (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `c.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `df.height (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `c.trim_lists_to_normalized_offsets()
                    .unwrap_or_else (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `AvroWriter::finish` ──[CALLS]──> `df.height (External/Unresolved)`
  • + [新增呼叫邊] `AvroWriter::finish` ──[CALLS]──> `df.apply_columns (External/Unresolved)`
  • + [新增呼叫邊] `AvroWriter::finish` ──[CALLS]──> `c.trim_lists_to_normalized_offsets()
                    .unwrap_or_else (External/Unresolved)`
  • + [新增呼叫邊] `AvroWriter::finish` ──[CALLS]──> `c.trim_lists_to_normalized_offsets (External/Unresolved)`
  • + [新增呼叫邊] `AvroWriter::finish` ──[CALLS]──> `c.clone (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `AvroWriter::finish()`
- **變更前簽章 (Before)**: `fn AvroWriter::finish(&mut self, df: &mut DataFrame)` (L66~L101)
- **變更後簽章 (After)**: `fn AvroWriter::finish(&mut self, df: &mut DataFrame)` (L66~L110)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn finish(&mut self, df: &mut DataFrame) -> PolarsResult<()> {
        let schema = schema_to_arrow_checked(df.schema(), CompatLevel::oldest(), "avro")?;
        let record = write::to_record(&schema, self.name.clone())?;

        avro_schema::write::write_metadata(&mut self.writer, record.clone(), self.compression)
            .map_err(to_compute_err)?;

        let mut data = vec![];
        let mut compressed_block = avro_schema::file::CompressedBlock::default();
        for chunk in df.iter_chunks(CompatLevel::oldest(), true) {
            let mut serializers = chunk
                .iter()
                .zip(record.fields.iter())
                .map(|(array, field)| write::new_serializer(array.as_ref(), &field.schema))
                .collect::<Vec<_>>();

            let mut block =
                avro_schema::file::Block::new(chunk.arrays()[0].len(), std::mem::take(&mut data));
            write::serialize(&mut serializers, &mut block);
            let _was_compressed =
                avro_schema::write::compress(&mut block, &mut compressed_block, self.compression)
                    .map_err(to_compute_err)?;

            avro_schema::write::write_block(&mut self.writer, &compressed_block)
                .map_err(to_compute_err)?;
            // reuse block for next iteration.
            data = block.data;
            data.clear();

            // reuse block for next iteration
            compressed_block.data.clear();
            compressed_block.number_of_rows = 0
        }

        Ok(())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn finish(&mut self, df: &mut DataFrame) -> PolarsResult<()> {
        let schema = schema_to_arrow_checked(df.schema(), CompatLevel::oldest(), "avro")?;
        let record = write::to_record(&schema, self.name.clone())?;

        avro_schema::write::write_metadata(&mut self.writer, record.clone(), self.compression)
            .map_err(to_compute_err)?;

        // Slicing list children to their offsets avoids converting and serializing unused values.
        let df = DataFrame::new(
            df.height(),
            df.apply_columns(|c| {
                c.trim_lists_to_normalized_offsets()
                    .unwrap_or_else(|| c.clone())
            }),
        )?;

        let mut data = vec![];
        let mut compressed_block = avro_schema::file::CompressedBlock::default();
        for chunk in df.iter_chunks(CompatLevel::oldest(), true) {
            let mut serializers = chunk
                .iter()
                .zip(record.fields.iter())
                .map(|(array, field)| write::new_serializer(array.as_ref(), &field.schema))
                .collect::<Vec<_>>();

            let mut block =
                avro_schema::file::Block::new(chunk.arrays()[0].len(), std::mem::take(&mut data));
            write::serialize(&mut serializers, &mut block);
            let _was_compressed =
                avro_schema::write::compress(&mut block, &mut compressed_block, self.compression)
                    .map_err(to_compute_err)?;

            avro_schema::write::write_block(&mut self.writer, &compressed_block)
                .map_err(to_compute_err)?;
            // reuse block for next iteration.
            data = block.data;
            data.clear();

            // reuse block for next iteration
            compressed_block.data.clear();
            compressed_block.number_of_rows = 0
        }

        Ok(())
    }
```


---

### 🔹 Commit #08: `bb845c1b`
- **完整 Hash**: `bb845c1b74ab26df13fadeac07e2dea26793b1ed`
- **說明 (Ground Truth)**: fix(rust): Compile polars-stream with only the IPC feature (#30051)
- **變更檔案數**: 4

#### 📄 檔案: `crates/polars-stream/src/nodes/io_sources/ipc/mod.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:191, E:201, A:0) ➔ After(N:191, E:201, A:0)
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

#### 📄 檔案: `crates/polars-stream/src/nodes/io_sources/parquet/init.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:175, E:183, A:0) ➔ After(N:165, E:172, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 11, +Edges: 1, -Edges: 12, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `split_to_morsels (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `df.slice (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `(df.height() / ideal_morsel_size).max (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `split_to_morsels` (FUNCTION_DEF)
  • - [移除節點] `i64::try_from (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `n_morsels.max (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `(0..i64::try_from(df.height()).unwrap())
        .step_by(rows_per_morsel)
        .map(move |offset| df.slice(offset, rows_per_morsel))
        .filter (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `df.height().div_ceil(n_morsels).max (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `(0..i64::try_from(df.height()).unwrap())
        .step_by (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `df.height().div_ceil (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `i64::try_from(df.height()).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `(0..i64::try_from(df.height()).unwrap())
        .step_by(rows_per_morsel)
        .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `ParquetReadImpl::init_morsel_distributor` ──[CALLS]──> `split_to_morsels (External/Unresolved)`
  • - [移除呼叫邊] `ParquetReadImpl::init_morsel_distributor` ──[CALLS]──> `split_to_morsels`
  • - [移除呼叫邊] `split_to_morsels` ──[CALLS]──> `df.height (External/Unresolved)`
  • _... 以及其餘 10 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `crates/polars-stream/src/nodes/io_sources/shared/mod.rs`
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

#### 📄 檔案: `crates/polars-stream/src/nodes/io_sources/shared/morsels.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:22, E:21, A:0)
- **差分統計**: +Nodes: 22, -Nodes: 0, +Edges: 21, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `df.slice (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `(0..i64::try_from(df.height()).unwrap())
        .step_by(rows_per_morsel)
        .map(move |offset| df.slice(offset, rows_per_morsel))
        .filter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `i64::try_from(df.height()).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `test_split_to_morsels` (FUNCTION_DEF)
  • + [新增節點] `(0..i64::try_from(df.height()).unwrap())
        .step_by (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert_eq! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `DataFrame::new(height, vec![Column::new("a".into(), values)]).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `(df.height() / ideal_morsel_size).max (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `split_to_morsels(&df, ideal, last, pipelines)
            .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `df.height().div_ceil(n_morsels).max (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `vec! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `DataFrame::new (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `split_to_morsels` (FUNCTION_DEF)
  • + [新增節點] `df.height (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 28 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #09: `2ddd4f5f`
- **完整 Hash**: `2ddd4f5f1a10906bf4a0d63d2f06ca3cb25408d4`
- **說明 (Ground Truth)**: fix: Check SQL casts to STRUCT[]/MAP[] and specify cast failure (#30026)
- **變更檔案數**: 1

#### 📄 檔案: `crates/polars-sql/src/sql_expr.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:600, E:886, A:0) ➔ After(N:615, E:905, A:0)
- **差分統計**: +Nodes: 19, -Nodes: 4, +Edges: 29, -Edges: 10, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `"STRUCT".to_string (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `within("map key".into(), nested_cast_mismatch(key, source_key)).or_else (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `nested_target_name(inner).map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `source.map_entries_dtype (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `"map key".into (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `"MAP".to_string (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `"list element".into (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `nested_cast_mismatch` (FUNCTION_DEF)
  • + [新增節點] `nested_target_name(&polars_type).is_some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `mismatch.path.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `target_fields.iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `source.clone().materialize_unknown (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `target_fields.iter().find_map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `"map value".into (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `mismatch.path.push (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 47 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SQLExprVisitor::array_expr_to_series()`
- **變更前簽章 (Before)**: `fn SQLExprVisitor::array_expr_to_series(&mut self, elements: &[SQLExpr])` (L340~L396)
- **變更後簽章 (After)**: `fn SQLExprVisitor::array_expr_to_series(&mut self, elements: &[SQLExpr])` (L340~L396)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn array_expr_to_series(&mut self, elements: &[SQLExpr]) -> PolarsResult<Series> {
        let mut array_elements = Vec::with_capacity(elements.len());
        let mut cast_dtypes = Vec::new();
        for e in elements {
            let val = match e {
                SQLExpr::Value(ValueWithSpan { value: v, .. }) => self.visit_any_value(v, None),
                SQLExpr::UnaryOp { op, expr } => match extract_literal_with_op(expr, Some(op)) {
                    Some((v, op)) => self.visit_any_value(v, op),
                    None => match expr.as_ref() {
                        SQLExpr::Cast {
                            data_type, expr: inner, format: None, ..
                        } => {
                            cast_dtypes.push(map_sql_dtype_to_polars(data_type)?);
                            match extract_literal_with_op(inner, Some(op)) {
                                Some((v, op)) => self.visit_any_value(v, op),
                                None => Err(polars_err!(SQLInterface: "array element {:?} is not supported", e)),
                            }
                        },
                        _ => Err(polars_err!(SQLInterface: "array element {:?} is not supported", e)),
                    },
                },
                SQLExpr::Array(values) => {
                    let srs = self.array_expr_to_series(&values.elem)?;
                    Ok(AnyValue::List(srs))
                },
                SQLExpr::TypedString(TypedString {
                    data_type,
                    value: ValueWithSpan {
                        value: SQLValue::SingleQuotedString(v), ..
                    },
                    ..
                }) => {
                    cast_dtypes.push(self.resolve_typed_literal_dtype(data_type, v)?);
                    Ok(AnyValue::StringOwned(v.as_str().into()))
                },
                SQLExpr::Cast {
                    data_type, expr, format: None, ..
                } => {
                    cast_dtypes.push(map_sql_dtype_to_polars(data_type)?);
                    match extract_literal_with_op(expr, None) {
                        Some((v, op)) => self.visit_any_value(v, op),
                        None => Err(polars_err!(SQLInterface: "array element {:?} is not supported", e)),
                    }
                },
                _ => Err(polars_err!(SQLInterface: "array element {:?} is not supported", e)),
            }?
            .into_static();
            array_elements.push(val);
        }
        let mut s = series_from_literals(PlSmallStr::EMPTY, &array_elements)?;
        if let Some(dtype) = resolve_common_dtype(&cast_dtypes, Some("array literal "))? {
            // Checked on the assembled series, whose elements share one type.
            ensure_nested_cast_source(&dtype, s.dtype())?;
            s = cast_literal_series(&s, &dtype)?;
        }
        Ok(s)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn array_expr_to_series(&mut self, elements: &[SQLExpr]) -> PolarsResult<Series> {
        let mut array_elements = Vec::with_capacity(elements.len());
        let mut cast_dtypes = Vec::new();
        for e in elements {
            let val = match e {
                SQLExpr::Value(ValueWithSpan { value: v, .. }) => self.visit_any_value(v, None),
                SQLExpr::UnaryOp { op, expr } => match extract_literal_with_op(expr, Some(op)) {
                    Some((v, op)) => self.visit_any_value(v, op),
                    None => match expr.as_ref() {
                        SQLExpr::Cast {
                            data_type, expr: inner, format: None, ..
                        } => {
                            cast_dtypes.push(map_sql_dtype_to_polars(data_type)?);
                            match extract_literal_with_op(inner, Some(op)) {
                                Some((v, op)) => self.visit_any_value(v, op),
                                None => Err(polars_err!(SQLInterface: "array element {:?} is not supported", e)),
                            }
                        },
                        _ => Err(polars_err!(SQLInterface: "array element {:?} is not supported", e)),
                    },
                },
                SQLExpr::Array(values) => {
                    let srs = self.array_expr_to_series(&values.elem)?;
                    Ok(AnyValue::List(srs))
                },
                SQLExpr::TypedString(TypedString {
                    data_type,
                    value: ValueWithSpan {
                        value: SQLValue::SingleQuotedString(v), ..
                    },
                    ..
                }) => {
                    cast_dtypes.push(self.resolve_typed_literal_dtype(data_type, v)?);
                    Ok(AnyValue::StringOwned(v.as_str().into()))
                },
                SQLExpr::Cast {
                    data_type, expr, format: None, ..
                } => {
                    cast_dtypes.push(map_sql_dtype_to_polars(data_type)?);
                    match extract_literal_with_op(expr, None) {
                        Some((v, op)) => self.visit_any_value(v, op),
                        None => Err(polars_err!(SQLInterface: "array element {:?} is not supported", e)),
                    }
                },
                _ => Err(polars_err!(SQLInterface: "array element {:?} is not supported", e)),
            }?
            .into_static();
            array_elements.push(val);
        }
        let mut s = series_from_literals(PlSmallStr::EMPTY, &array_elements)?;
        if let Some(dtype) = resolve_common_dtype(&cast_dtypes, Some("array literal "))? {
            // Checked on the assembled series, whose elements share one type.
            ensure_nested_cast_source("CAST", &dtype, s.dtype())?;
            s = cast_literal_series(&s, &dtype)?;
        }
        Ok(s)
    }
```

### 🔹 函式: `ensure_nested_cast_source()`
- **變更前簽章 (Before)**: `fn ensure_nested_cast_source(target: &DataType, source: &DataType)` (L2364~L2399)
- **變更後簽章 (After)**: `fn ensure_nested_cast_source(
    cast_kind: &str,
    target: &DataType,
    source: &DataType,
)` (L2364~L2386)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn ensure_nested_cast_source(target: &DataType, source: &DataType) -> PolarsResult<()> {
    match (target, source) {
        (_, DataType::Null | DataType::Unknown(UnknownKind::Any)) => Ok(()),
        (
            DataType::List(target) | DataType::Array(target, _),
            DataType::List(source) | DataType::Array(source, _),
        ) => ensure_nested_cast_source(target, source),
        (DataType::Struct(target_fields), DataType::Struct(source_fields)) => {
            for field in target_fields {
                if let Some(source_field) = source_fields.iter().find(|f| f.name == field.name) {
                    ensure_nested_cast_source(&field.dtype, &source_field.dtype)?;
                }
            }
            Ok(())
        },
        #[cfg(feature = "dtype-map")]
        (DataType::Map(key, value), DataType::Map(source_key, source_value)) => {
            ensure_nested_cast_source(key, source_key)?;
            ensure_nested_cast_source(value, source_value)
        },
        _ => {
            let Some(name) = nested_target_name(target) else {
                return Ok(());
            };
            // A literal's dynamic type (`dyn int`) is shown as the type it becomes.
            let source = match source {
                DataType::Unknown(kind) => kind.materialize().unwrap_or_else(|| source.clone()),
                _ => source.clone(),
            };
            polars_bail!(
                SQLInterface: "CAST from {} to {} is not supported; only {} values or NULL can be cast to {}",
                source, name, name, name
            )
        },
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn ensure_nested_cast_source(
    cast_kind: &str,
    target: &DataType,
    source: &DataType,
) -> PolarsResult<()> {
    let Some(mismatch) = nested_cast_mismatch(target, source) else {
        return Ok(());
    };
    // A literal's dynamic type (`dyn int`) is shown as the type it becomes.
    let source = source.clone().materialize_unknown(true)?;
    let name = mismatch.target;
    if mismatch.path.is_empty() {
        polars_bail!(
            SQLInterface: "{} from {} to {} is not supported; only {} values or NULL can be cast to {}",
            cast_kind, source, name, name, name
        )
    }
    polars_bail!(
        SQLInterface: "{} from {} to {} is not supported: {} is {}; only {} values or NULL can be cast to {}",
        cast_kind, source, nested_target_name(target).unwrap_or_default(),
        mismatch.path.join(" of "), mismatch.source.materialize_unknown(true)?, name, name
    )
}
```

### 🔹 函式: `SQLExprVisitor::visit_cast()`
- **變更前簽章 (Before)**: `fn SQLExprVisitor::visit_cast(
        &mut self,
        expr: &SQLExpr,
        dtype: &SQLDataType,
        format: &Option<CastFormat>,
        cast_kind: &CastKind,
    )` (L1397~L1447)
- **變更後簽章 (After)**: `fn SQLExprVisitor::visit_cast(
        &mut self,
        expr: &SQLExpr,
        dtype: &SQLDataType,
        format: &Option<CastFormat>,
        cast_kind: &CastKind,
    )` (L1397~L1452)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn visit_cast(
        &mut self,
        expr: &SQLExpr,
        dtype: &SQLDataType,
        format: &Option<CastFormat>,
        cast_kind: &CastKind,
    ) -> PolarsResult<Expr> {
        if format.is_some() {
            return Err(
                polars_err!(SQLInterface: "use of FORMAT is not currently supported in CAST"),
            );
        }
        let expr = self.visit_expr(expr)?;

        #[cfg(feature = "json")]
        if dtype == &SQLDataType::JSON {
            // @BROKEN: we cannot handle this.
            return Ok(expr.str().json_decode(DataType::Struct(Vec::new())));
        }
        let polars_type = map_sql_dtype_to_polars(dtype)?;
        if contains_struct_or_map(&polars_type) {
            // A scalar subquery only gets a type from its plan, and a window has the type of its
            // function (`OVER ()` partitions by a column that isn't in the schema).
            let typed = self
                .ctx
                .with_typed_subqueries(&expr)?
                .map_expr(|e| match e {
                    Expr::Over { function, .. } => Arc::unwrap_or_clone(function),
                    e => e,
                });
            if let Some(source) = self.cast_or_expr_dtype(&typed) {
                ensure_nested_cast_source(&polars_type, &source)?;
            }
        }
        let strict = matches!(cast_kind, CastKind::Cast | CastKind::DoubleColon);

        // `CAST(<string> AS DATE/TIME/TIMESTAMP)` parses rather than casts
        if matches!(
            polars_type,
            DataType::Date | DataType::Time | DataType::Datetime(_, _)
        ) && self.expr_dtype(&expr) == Some(DataType::String)
            && let Some(parsed) = string_to_temporal(expr.clone(), &polars_type, strict)
        {
            return Ok(parsed);
        }
        Ok(if strict {
            expr.strict_cast(polars_type)
        } else {
            expr.cast(polars_type)
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn visit_cast(
        &mut self,
        expr: &SQLExpr,
        dtype: &SQLDataType,
        format: &Option<CastFormat>,
        cast_kind: &CastKind,
    ) -> PolarsResult<Expr> {
        if format.is_some() {
            return Err(
                polars_err!(SQLInterface: "use of FORMAT is not currently supported in CAST"),
            );
        }
        let expr = self.visit_expr(expr)?;

        #[cfg(feature = "json")]
        if dtype == &SQLDataType::JSON {
            // @BROKEN: we cannot handle this.
            return Ok(expr.str().json_decode(DataType::Struct(Vec::new())));
        }
        let polars_type = map_sql_dtype_to_polars(dtype)?;
        if nested_target_name(&polars_type).is_some() {
            // A scalar subquery only gets a type from its plan, and a window has the type of its
            // function (`OVER ()` partitions by a column that isn't in the schema).
            let typed = self
                .ctx
                .with_typed_subqueries(&expr)?
                .map_expr(|e| match e {
                    Expr::Over { function, .. } => Arc::unwrap_or_clone(function),
                    e => e,
                });
            if let Some(source) = self.cast_or_expr_dtype(&typed) {
                let kind = match cast_kind {
                    CastKind::TryCast => "TRY_CAST",
                    CastKind::SafeCast => "SAFE_CAST",
                    CastKind::Cast | CastKind::DoubleColon => "CAST",
                };
                ensure_nested_cast_source(kind, &polars_type, &source)?;
            }
        }
        let strict = matches!(cast_kind, CastKind::Cast | CastKind::DoubleColon);

        // `CAST(<string> AS DATE/TIME/TIMESTAMP)` parses rather than casts
        if matches!(
            polars_type,
            DataType::Date | DataType::Time | DataType::Datetime(_, _)
        ) && self.expr_dtype(&expr) == Some(DataType::String)
            && let Some(parsed) = string_to_temporal(expr.clone(), &polars_type, strict)
        {
            return Ok(parsed);
        }
        Ok(if strict {
            expr.strict_cast(polars_type)
        } else {
            expr.cast(polars_type)
        })
    }
```

### 🔹 函式: `nested_target_name()`
- **變更前簽章 (Before)**: `fn nested_target_name(dtype: &DataType)` (L2344~L2351)
- **變更後簽章 (After)**: `fn nested_target_name(dtype: &DataType)` (L2349~L2359)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn nested_target_name(dtype: &DataType) -> Option<&'static str> {
    match dtype {
        DataType::Struct(_) => Some("STRUCT"),
        #[cfg(feature = "dtype-map")]
        DataType::Map(..) => Some("MAP"),
        _ => None,
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn nested_target_name(dtype: &DataType) -> Option<String> {
    match dtype {
        DataType::List(inner) | DataType::Array(inner, _) => {
            nested_target_name(inner).map(|name| format!("{name}[]"))
        },
        DataType::Struct(_) => Some("STRUCT".to_string()),
        #[cfg(feature = "dtype-map")]
        DataType::Map(..) => Some("MAP".to_string()),
        _ => None,
    }
}
```


---

### 🔹 Commit #10: `bee937fe`
- **完整 Hash**: `bee937fe894bcedd0d1eedac368c701a24615126`
- **說明 (Ground Truth)**: fix: Allow empty groups in multi key sort_by (#29825)
- **變更檔案數**: 1

#### 📄 檔案: `crates/polars-expr/src/expressions/sortby.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:178, E:209, A:0) ➔ After(N:175, E:208, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 3, +Edges: 2, -Edges: 3, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `new_idx
        .first()
        .ok_or_else (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `polars_err! (Macro)` (FUNCTION_DEF)
  • - [移除節點] `new_idx
        .first (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `sort_by_groups_multiple_by` ──[CALLS]──> `new_idx.first().unwrap_or (External/Unresolved)`
  • + [新增呼叫邊] `sort_by_groups_multiple_by` ──[CALLS]──> `new_idx.first (External/Unresolved)`
  • - [移除呼叫邊] `sort_by_groups_multiple_by` ──[CALLS]──> `new_idx
        .first()
        .ok_or_else (External/Unresolved)`
  • - [移除呼叫邊] `sort_by_groups_multiple_by` ──[CALLS]──> `new_idx
        .first (External/Unresolved)`
  • - [移除呼叫邊] `sort_by_groups_multiple_by` ──[CALLS]──> `polars_err! (Macro)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `sort_by_groups_multiple_by()`
- **變更前簽章 (Before)**: `fn sort_by_groups_multiple_by(
    indicator: GroupsIndicator,
    sort_by_s: &[Series],
    descending: &[bool],
    nulls_last: &[bool],
    multithreaded: bool,
    maintain_order: bool,
    limit: Option<IdxSize>,
)` (L173~L225)
- **變更後簽章 (After)**: `fn sort_by_groups_multiple_by(
    indicator: GroupsIndicator,
    sort_by_s: &[Series],
    descending: &[bool],
    nulls_last: &[bool],
    multithreaded: bool,
    maintain_order: bool,
    limit: Option<IdxSize>,
)` (L173~L223)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn sort_by_groups_multiple_by(
    indicator: GroupsIndicator,
    sort_by_s: &[Series],
    descending: &[bool],
    nulls_last: &[bool],
    multithreaded: bool,
    maintain_order: bool,
    limit: Option<IdxSize>,
) -> PolarsResult<(IdxSize, IdxVec)> {
    let new_idx = match indicator {
        GroupsIndicator::Idx((_first, idx)) => {
            // SAFETY: group tuples are always in bounds.
            let groups = sort_by_s
                .iter()
                .map(|s| unsafe { s.take_slice_unchecked(idx) })
                .map(Column::from)
                .collect::<Vec<_>>();

            let options = SortMultipleOptions {
                descending: descending.to_owned(),
                nulls_last: nulls_last.to_owned(),
                multithreaded,
                maintain_order,
                limit,
            };

            let sorted_idx = arg_sort(&groups, options)?;
            map_sorted_indices_to_group_idx(&sorted_idx, idx)
        },
        GroupsIndicator::Slice([first, len]) => {
            let groups = sort_by_s
                .iter()
                .map(|s| s.slice(first as i64, len as usize))
                .map(Column::from)
                .collect::<Vec<_>>();

            let options = SortMultipleOptions {
                descending: descending.to_owned(),
                nulls_last: nulls_last.to_owned(),
                multithreaded,
                maintain_order,
                limit,
            };
            let sorted_idx = arg_sort(&groups, options)?;
            map_sorted_indices_to_group_slice(&sorted_idx, first)
        },
    };
    let first = new_idx
        .first()
        .ok_or_else(|| polars_err!(ComputeError: "{ERR_MSG}"))?;

    Ok((*first, new_idx))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn sort_by_groups_multiple_by(
    indicator: GroupsIndicator,
    sort_by_s: &[Series],
    descending: &[bool],
    nulls_last: &[bool],
    multithreaded: bool,
    maintain_order: bool,
    limit: Option<IdxSize>,
) -> PolarsResult<(IdxSize, IdxVec)> {
    let new_idx = match indicator {
        GroupsIndicator::Idx((_first, idx)) => {
            // SAFETY: group tuples are always in bounds.
            let groups = sort_by_s
                .iter()
                .map(|s| unsafe { s.take_slice_unchecked(idx) })
                .map(Column::from)
                .collect::<Vec<_>>();

            let options = SortMultipleOptions {
                descending: descending.to_owned(),
                nulls_last: nulls_last.to_owned(),
                multithreaded,
                maintain_order,
                limit,
            };

            let sorted_idx = arg_sort(&groups, options)?;
            map_sorted_indices_to_group_idx(&sorted_idx, idx)
        },
        GroupsIndicator::Slice([first, len]) => {
            let groups = sort_by_s
                .iter()
                .map(|s| s.slice(first as i64, len as usize))
                .map(Column::from)
                .collect::<Vec<_>>();

            let options = SortMultipleOptions {
                descending: descending.to_owned(),
                nulls_last: nulls_last.to_owned(),
                multithreaded,
                maintain_order,
                limit,
            };
            let sorted_idx = arg_sort(&groups, options)?;
            map_sorted_indices_to_group_slice(&sorted_idx, first)
        },
    };

    let first = new_idx.first().unwrap_or(&0);
    Ok((*first, new_idx))
}
```


---

### 🔹 Commit #11: `6d17cb58`
- **完整 Hash**: `6d17cb58100c4d08513b0ad7399f81e70005ab33`
- **說明 (Ground Truth)**: perf: Fix dead early exit in `coalesce` (#30013)
- **變更檔案數**: 1

#### 📄 檔案: `crates/polars-ops/src/series/ops/horizontal.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:157, E:197, A:0) ➔ After(N:164, E:205, A:0)
- **差分統計**: +Nodes: 11, -Nodes: 4, +Edges: 12, -Edges: 4, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `next.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out.new_from_index (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `next.as_materialized_series (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out
            .as_materialized_series()
            .zip_with_same_type(&mask, next.as_materialized_series())?
            .into (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `next.clone().with_name (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out.has_nulls (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out.len (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out
            .as_materialized_series (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out
            .as_materialized_series()
            .zip_with_same_type (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out.name().clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out.name (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `out
                .as_materialized_series()
                .zip_with_same_type (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `out
                .as_materialized_series (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `out
                .as_materialized_series()
                .zip_with_same_type(&mask, s.as_materialized_series())?
                .into (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `s.as_materialized_series (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 16 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `coalesce_columns()`
- **變更前簽章 (Before)**: `fn coalesce_columns(s: &[Column])` (L341~L357)
- **變更後簽章 (After)**: `fn coalesce_columns(s: &[Column])` (L341~L366)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn coalesce_columns(s: &[Column]) -> PolarsResult<Column> {
    // TODO! this can be faster if we have more than two inputs.
    polars_ensure!(!s.is_empty(), NoData: "cannot coalesce empty list");
    let mut out = s[0].clone();
    for s in s {
        if !out.null_count() == 0 {
            return Ok(out);
        } else {
            let mask = out.is_not_null();
            out = out
                .as_materialized_series()
                .zip_with_same_type(&mask, s.as_materialized_series())?
                .into();
        }
    }
    Ok(out)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn coalesce_columns(s: &[Column]) -> PolarsResult<Column> {
    // Each iteration recomputes the null mask and allocates a new `out`; a single
    // pass over all inputs would be faster for many inputs with many nulls.
    polars_ensure!(!s.is_empty(), NoData: "cannot coalesce empty list");
    let len = broadcast_len(s)?;
    let mut out = s[0].clone();
    for next in &s[1..] {
        if !out.has_nulls() {
            break;
        }
        if out.null_count() == out.len() {
            out = next.clone().with_name(out.name().clone());
            continue;
        }
        let mask = out.is_not_null();
        out = out
            .as_materialized_series()
            .zip_with_same_type(&mask, next.as_materialized_series())?
            .into();
    }
    // The early exits skip the broadcast `zip_with` would have done.
    if out.len() != len {
        out = out.new_from_index(0, len);
    }
    Ok(out)
}
```


---

### 🔹 Commit #12: `c960222a`
- **完整 Hash**: `c960222a47f331e3027d27515ff15402f5f83aba`
- **說明 (Ground Truth)**: fix: Fix reading Parquet files with empty row groups (#30001)
- **變更檔案數**: 1

#### 📄 檔案: `crates/polars-stream/src/nodes/io_sources/parquet/row_group_data_fetch.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:128, E:145, A:0) ➔ After(N:134, E:155, A:0)
- **差分統計**: +Nodes: 12, -Nodes: 6, +Edges: 22, -Edges: 12, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `row_group_metadata
            .byte_ranges_iter()
            .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `PlHashMap::default (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `row_group_metadata
            .byte_ranges_iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `ranges.retain (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `get_row_group_byte_ranges_for_projection(
            row_group_metadata,
            &mut projection.iter().map(|x| &x.arrow_field().name),
        )
        .collect::<ParquetResult<Vec<_>>> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `get_row_group_fetch_ranges` (FUNCTION_DEF)
  • + [新增節點] `tokio_handle_ext::AbortOnDropHandle(
            ASYNC.spawn(async move { fetch_ranges(&source, &mut ranges).await }),
        )
        .await
        .expect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `r.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `polars_ensure! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `range.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `row_group_metadata
            .byte_ranges_iter()
            .map(|x| x.start as usize..x.end as usize)
            .collect::<Vec<_>> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `fetch_ranges` (FUNCTION_DEF)
  • - [移除節點] `get_row_group_byte_ranges_for_projection(
                            row_group_metadata,
                            &mut projection.iter().map(|x| &x.arrow_field().name),
                        )
                        .collect::<ParquetResult<Vec<_>>> (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `row_group_metadata
                            .byte_ranges_iter()
                            .map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `tokio_handle_ext::AbortOnDropHandle(
            ASYNC.spawn(async move { source.get_ranges(&mut ranges).await }),
        )
        .await
        .expect (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 37 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RowGroupDataFetcher::next()`
- **變更前簽章 (Before)**: `fn RowGroupDataFetcher::next(
        &mut self,
    )` (L176~L319)
- **變更後簽章 (After)**: `fn RowGroupDataFetcher::next(
        &mut self,
    )` (L176~L286)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(super) async fn next(
        &mut self,
    ) -> Option<PolarsResult<tokio_handle_ext::AbortOnDropHandle<PolarsResult<RowGroupData>>>> {
        let RowGroupToRead {
            idx,
            row_offset: current_row_offset,
            slice,
        } = self.row_groups.pop_front()?;
        let sorting_map = create_sorting_map(&self.metadata.row_groups[idx]);

        let metadata = self.metadata.clone();
        let current_byte_source = self.byte_source.clone();
        let projection = self.projection.clone();
        let is_full_projection = self.is_full_projection;
        let memory_prefetch_func = self.memory_prefetch_func;
        let read_stats = self.read_stats.clone();

        let handle = ASYNC.spawn(async move {
            let row_group_metadata = &metadata.row_groups[idx];
            let fetched_bytes = match current_byte_source.as_ref() {
                DynByteSource::Buffer(mem_slice) => {
                    // Skip byte range calculation for `no_prefetch`.
                    if memory_prefetch_func as usize
                        != polars_utils::mem::prefetch::no_prefetch as *const () as usize
                    {
                        let slice = mem_slice.0.as_ref();

                        if !is_full_projection {
                            // Errors are raised when decoding rather than when prefetching.
                            for range in get_row_group_byte_ranges_for_projection(
                                row_group_metadata,
                                &mut projection.iter().map(|x| &x.arrow_field().name),
                            )
                            .filter_map(|r| r.ok())
                            {
                                memory_prefetch_func(unsafe { slice.get_unchecked(range) })
                            }
                        } else {
                            let range = row_group_metadata.full_byte_range();
                            let range = range.start as usize..range.end as usize;

                            memory_prefetch_func(unsafe { slice.get_unchecked(range) })
                        };
                    }

                    // We have a mmapped or in-memory slice representing the entire
                    // file that can be sliced directly, so we can skip the byte-range
                    // calculations and HashMap allocation.
                    let mem_slice = mem_slice.0.clone();
                    FetchedBytes::Buffer {
                        offset: 0,
                        buffer: mem_slice,
                    }
                },
                DynByteSource::File(source) => {
                    let mut ranges = if !is_full_projection {
                        get_row_group_byte_ranges_for_projection(
                            row_group_metadata,
                            &mut projection.iter().map(|x| &x.arrow_field().name),
                        )
                        .collect::<ParquetResult<Vec<_>>>()?
                    } else {
                        row_group_metadata
                            .byte_ranges_iter()
                            .map(|x| x.start as usize..x.end as usize)
                            .collect::<Vec<_>>()
                    };

                    // Reade a cached row group in its decode tasks, each column chunk on
                    // the thread that decompresses it. This beats copying it ahead on the blocking
                    // pool. Uncached ones are prefetched, so that the I/O overlaps decoding.
                    let defer = read_stats.defer_cached_reads
                        && !ranges.is_empty()
                        && source.is_cached(&ranges);

                    if defer {
                        read_stats.deferred.fetch_add(1, Ordering::Relaxed);
                        FetchedBytes::Deferred {
                            source: current_byte_source.clone(),
                            ranges,
                            read_stats: read_stats.clone(),
                        }
                    } else {
                        read_stats.prefetched.fetch_add(1, Ordering::Relaxed);

                        let n_ranges = ranges.len();

                        let bytes_map = source.get_ranges(&mut ranges).await?;

                        assert_eq!(bytes_map.len(), n_ranges);

                        FetchedBytes::BytesMap(bytes_map)
                    }
                },
                DynByteSource::Cloud(_) => {
                    if !is_full_projection {
                        let mut ranges = get_row_group_byte_ranges_for_projection(
                            row_group_metadata,
                            &mut projection.iter().map(|x| &x.arrow_field().name),
                        )
                        .collect::<ParquetResult<Vec<_>>>()?;

                        let n_ranges = ranges.len();

                        let bytes_map = current_byte_source.get_ranges(&mut ranges).await?;

                        assert_eq!(bytes_map.len(), n_ranges);

                        FetchedBytes::BytesMap(bytes_map)
                    } else {
                        // We still prefer `get_ranges()` over a single `get_range()` for downloading
                        // the entire row group, as it can have less memory-copying. A single `get_range()`
                        // would naively concatenate the memory blocks of the entire row group, while
                        // `get_ranges()` can skip concatenation since the downloaded blocks are
                        // aligned to the columns.
                        let mut ranges = row_group_metadata
                            .byte_ranges_iter()
                            .map(|x| x.start as usize..x.end as usize)
                            .collect::<Vec<_>>();

                        let n_ranges = ranges.len();

                        let bytes_map = current_byte_source.get_ranges(&mut ranges).await?;

                        assert_eq!(bytes_map.len(), n_ranges);

                        FetchedBytes::BytesMap(bytes_map)
                    }
                },
            };

            PolarsResult::Ok(RowGroupData {
                fetched_bytes,
                row_offset: current_row_offset,
                slice,
                // @TODO: Remove clone
                row_group_metadata: row_group_metadata.clone(),
                sorting_map,
            })
        });

        let handle = tokio_handle_ext::AbortOnDropHandle(handle);
        Some(Ok(handle))
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(super) async fn next(
        &mut self,
    ) -> Option<PolarsResult<tokio_handle_ext::AbortOnDropHandle<PolarsResult<RowGroupData>>>> {
        let RowGroupToRead {
            idx,
            row_offset: current_row_offset,
            slice,
        } = self.row_groups.pop_front()?;
        let sorting_map = create_sorting_map(&self.metadata.row_groups[idx]);

        let metadata = self.metadata.clone();
        let current_byte_source = self.byte_source.clone();
        let projection = self.projection.clone();
        let is_full_projection = self.is_full_projection;
        let memory_prefetch_func = self.memory_prefetch_func;
        let read_stats = self.read_stats.clone();

        let handle = ASYNC.spawn(async move {
            let row_group_metadata = &metadata.row_groups[idx];
            let fetched_bytes = match current_byte_source.as_ref() {
                DynByteSource::Buffer(mem_slice) => {
                    // Skip byte range calculation for `no_prefetch`.
                    if memory_prefetch_func as usize
                        != polars_utils::mem::prefetch::no_prefetch as *const () as usize
                    {
                        let slice = mem_slice.0.as_ref();

                        if !is_full_projection {
                            // Errors are raised when decoding rather than when prefetching.
                            for range in get_row_group_byte_ranges_for_projection(
                                row_group_metadata,
                                &mut projection.iter().map(|x| &x.arrow_field().name),
                            )
                            .filter_map(|r| r.ok())
                            {
                                memory_prefetch_func(unsafe { slice.get_unchecked(range) })
                            }
                        } else {
                            let range = row_group_metadata.full_byte_range();
                            let range = range.start as usize..range.end as usize;

                            memory_prefetch_func(unsafe { slice.get_unchecked(range) })
                        };
                    }

                    // We have a mmapped or in-memory slice representing the entire
                    // file that can be sliced directly, so we can skip the byte-range
                    // calculations and HashMap allocation.
                    let mem_slice = mem_slice.0.clone();
                    FetchedBytes::Buffer {
                        offset: 0,
                        buffer: mem_slice,
                    }
                },
                DynByteSource::File(source) => {
                    let mut ranges = get_row_group_fetch_ranges(
                        row_group_metadata,
                        &projection,
                        is_full_projection,
                    )?;

                    if ranges.is_empty() {
                        // Nothing to read, e.g. an empty row group.
                        FetchedBytes::BytesMap(PlHashMap::default())
                    } else if read_stats.defer_cached_reads && source.is_cached(&ranges) {
                        // Read a cached row group in its decode tasks, each column chunk on
                        // the thread that decompresses it. This beats copying it ahead on the blocking
                        // pool. Uncached ones are prefetched, so that the I/O overlaps decoding.
                        read_stats.deferred.fetch_add(1, Ordering::Relaxed);
                        FetchedBytes::Deferred {
                            source: current_byte_source.clone(),
                            ranges,
                            read_stats: read_stats.clone(),
                        }
                    } else {
                        read_stats.prefetched.fetch_add(1, Ordering::Relaxed);

                        FetchedBytes::BytesMap(
                            fetch_ranges(&current_byte_source, &mut ranges).await?,
                        )
                    }
                },
                DynByteSource::Cloud(_) => {
                    // We still prefer `get_ranges()` over a single `get_range()` for downloading
                    // the entire row group, as it can have less memory-copying. A single `get_range()`
                    // would naively concatenate the memory blocks of the entire row group, while
                    // `get_ranges()` can skip concatenation since the downloaded blocks are
                    // aligned to the columns.
                    let mut ranges = get_row_group_fetch_ranges(
                        row_group_metadata,
                        &projection,
                        is_full_projection,
                    )?;

                    FetchedBytes::BytesMap(fetch_ranges(&current_byte_source, &mut ranges).await?)
                },
            };

            PolarsResult::Ok(RowGroupData {
                fetched_bytes,
                row_offset: current_row_offset,
                slice,
                // @TODO: Remove clone
                row_group_metadata: row_group_metadata.clone(),
                sorting_map,
            })
        });

        let handle = tokio_handle_ext::AbortOnDropHandle(handle);
        Some(Ok(handle))
    }
```

### 🔹 函式: `FetchedBytes::get_range()`
- **變更前簽章 (Before)**: `fn FetchedBytes::get_range(&self, range: std::ops::Range<usize>)` (L371~L390)
- **變更後簽章 (After)**: `fn FetchedBytes::get_range(&self, range: std::ops::Range<usize>)` (L336~L360)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(super) fn get_range(&self, range: std::ops::Range<usize>) -> PolarsResult<Buffer<u8>> {
        Ok(match self {
            Self::Buffer { buffer, offset } => {
                let offset = *offset;
                debug_assert!(range.start >= offset);
                buffer
                    .clone()
                    .sliced(range.start - offset..range.end - offset)
            },
            Self::BytesMap(v) => {
                let v = v.get(&range.start).unwrap();
                debug_assert_eq!(v.len(), range.len());
                v.clone()
            },
            Self::Deferred { source, .. } => match source.as_ref() {
                DynByteSource::File(source) => source.read_blocking(range)?,
                _ => unreachable!("only file sources defer their reads"),
            },
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(super) fn get_range(&self, range: std::ops::Range<usize>) -> PolarsResult<Buffer<u8>> {
        // Empty ranges are not fetched.
        if range.is_empty() {
            return Ok(Buffer::new());
        }

        Ok(match self {
            Self::Buffer { buffer, offset } => {
                let offset = *offset;
                debug_assert!(range.start >= offset);
                buffer
                    .clone()
                    .sliced(range.start - offset..range.end - offset)
            },
            Self::BytesMap(v) => {
                let v = v.get(&range.start).unwrap();
                debug_assert_eq!(v.len(), range.len());
                v.clone()
            },
            Self::Deferred { source, .. } => match source.as_ref() {
                DynByteSource::File(source) => source.read_blocking(range)?,
                _ => unreachable!("only file sources defer their reads"),
            },
        })
    }
```

### 🔹 函式: `FetchedBytes::fetch_if_evicted()`
- **變更前簽章 (Before)**: `fn FetchedBytes::fetch_if_evicted(&mut self)` (L340~L369)
- **變更後簽章 (After)**: `fn FetchedBytes::fetch_if_evicted(&mut self)` (L307~L334)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(super) async fn fetch_if_evicted(&mut self) -> PolarsResult<()> {
        let Self::Deferred {
            source,
            ranges,
            read_stats,
        } = self
        else {
            return Ok(());
        };
        let DynByteSource::File(file) = source.as_ref() else {
            unreachable!("only file sources defer their reads")
        };
        if file.is_cached(ranges) {
            return Ok(());
        }

        read_stats.reread.fetch_add(1, Ordering::Relaxed);
        let source = source.clone();
        let mut ranges = std::mem::take(ranges);
        let n_ranges = ranges.len();
        let bytes_map = tokio_handle_ext::AbortOnDropHandle(
            ASYNC.spawn(async move { source.get_ranges(&mut ranges).await }),
        )
        .await
        .expect("fetch task panicked")?;
        assert_eq!(bytes_map.len(), n_ranges);

        *self = Self::BytesMap(bytes_map);
        Ok(())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(super) async fn fetch_if_evicted(&mut self) -> PolarsResult<()> {
        let Self::Deferred {
            source,
            ranges,
            read_stats,
        } = self
        else {
            return Ok(());
        };
        let DynByteSource::File(file) = source.as_ref() else {
            unreachable!("only file sources defer their reads")
        };
        if file.is_cached(ranges) {
            return Ok(());
        }

        read_stats.reread.fetch_add(1, Ordering::Relaxed);
        let source = source.clone();
        let mut ranges = std::mem::take(ranges);
        let bytes_map = tokio_handle_ext::AbortOnDropHandle(
            ASYNC.spawn(async move { fetch_ranges(&source, &mut ranges).await }),
        )
        .await
        .expect("fetch task panicked")?;

        *self = Self::BytesMap(bytes_map);
        Ok(())
    }
```


---

### 🔹 Commit #13: `fecce5a5`
- **完整 Hash**: `fecce5a57b0a5ccfdfd2f8784b9b74887da4026e`
- **說明 (Ground Truth)**: perf: Fix some in-memory filter regressions (#29988)
- **變更檔案數**: 1

#### 📄 檔案: `crates/polars-mem-engine/src/executors/filter.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:40, E:47, A:0) ➔ After(N:63, E:75, A:0)
- **差分統計**: +Nodes: 25, -Nodes: 2, +Edges: 39, -Edges: 11, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `_split_offsets(df.height(), n_chunks)
            .into_par_iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `_split_offsets (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `df.slice (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out.append_owned (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `df.clone().split_chunks_by_n (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `RAYON.current_num_threads().div_ceil (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `chunks
                .into_par_iter()
                .map(|chunk| self.predicate.evaluate(&chunk, state))
                .collect::<PolarsResult<Vec<_>>> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `filter_par` (FUNCTION_DEF)
  • + [新增節點] `chunks
                .into_par_iter()
                .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `_split_offsets(df.height(), n_chunks)
            .into_par_iter()
            .map(|(offset, len)| {
                let offset = offset as i64;
                df.slice(offset, len).filter(&mask.slice(offset, len))
            })
            .collect::<PolarsResult<Vec<_>>> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `FilterExec::evaluate_predicate` (FUNCTION_DEF)
  • + [新增節點] `df.slice(offset, len).filter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `columns.next (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `MIN_ROWS_PER_PREDICATE_CHUNK` (MODULE_STATE)
  • + [新增節點] `MIN_ROWS_PER_FILTER_CHUNK` (MODULE_STATE)
  • _... 以及其餘 62 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FilterExec::execute_impl()`
- **變更前簽章 (Before)**: `fn FilterExec::execute_impl(
        &mut self,
        mut df: DataFrame,
        state: &mut ExecutionState,
    )` (L94~L114)
- **變更後簽章 (After)**: `fn FilterExec::execute_impl(
        &mut self,
        mut df: DataFrame,
        state: &mut ExecutionState,
    )` (L107~L130)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn execute_impl(
        &mut self,
        mut df: DataFrame,
        state: &mut ExecutionState,
    ) -> PolarsResult<DataFrame> {
        let n_partitions = RAYON.current_num_threads();
        // Vertical parallelism.
        if self.streamable && df.height() > 0 {
            if df.first_col_n_chunks() > 1 {
                let chunks = df.split_chunks().collect::<Vec<_>>();
                self.execute_chunks(chunks, state)
            } else if df.width() >= n_partitions {
                self.execute_hor(df, state)
            } else {
                let chunks = df.split_chunks_by_n(n_partitions, true);
                self.execute_chunks(chunks, state)
            }
        } else {
            self.execute_hor(df, state)
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn execute_impl(
        &mut self,
        mut df: DataFrame,
        state: &mut ExecutionState,
    ) -> PolarsResult<DataFrame> {
        // Use pre-chunked data.
        if self.streamable && df.height() > 0 && df.first_col_n_chunks() > 1 {
            let chunks = df.split_chunks().collect::<Vec<_>>();
            return self.execute_chunks(chunks, state);
        }

        if self.has_window {
            state.insert_has_window_function_flag()
        }
        let c = self.evaluate_predicate(&df, state)?;
        if self.has_window {
            state.clear_window_expr_cache()
        }

        // @scalar-opt
        // @partition-opt
        let mask = column_to_mask(&c, df.height())?;
        filter_par(&df, &mask)
    }
```


---

### 🔹 Commit #14: `858a20f5`
- **完整 Hash**: `858a20f57f052aa594366913710e886a733bfd60`
- **說明 (Ground Truth)**: fix: Check the last 4 bytes of inlined strings for invalid UTF-8 in parquet (#29981)
- **變更檔案數**: 1

#### 📄 檔案: `crates/polars-parquet/src/arrow/read/deserialize/binview/mod.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:185, E:220, A:0) ➔ After(N:185, E:220, A:0)
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

### 🔹 函式: `decode_plain_generic()`
- **變更前簽章 (Before)**: `fn decode_plain_generic(
    values: &[u8],
    target: &mut MutableBinaryViewArray<[u8]>,

    num_rows: usize,
    mut next: impl FnMut() -> Option<(bool, bool)>,

    verify_utf8: bool,
)` (L329~L482)
- **變更後簽章 (After)**: `fn decode_plain_generic(
    values: &[u8],
    target: &mut MutableBinaryViewArray<[u8]>,

    num_rows: usize,
    mut next: impl FnMut() -> Option<(bool, bool)>,

    verify_utf8: bool,
)` (L329~L483)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn decode_plain_generic(
    values: &[u8],
    target: &mut MutableBinaryViewArray<[u8]>,

    num_rows: usize,
    mut next: impl FnMut() -> Option<(bool, bool)>,

    verify_utf8: bool,
) -> ParquetResult<()> {
    // Since the offset in the buffer is decided by the interleaved lengths, every value has to be
    // walked no matter what. This makes decoding rather inefficient in general.
    //
    // There are three cases:
    // 1. All inlinable values
    //    - Most time is spend in decoding
    //    - No additional buffer has to be formed
    //    - Possible UTF-8 verification is fast because the len_below_128 trick
    // 2. All non-inlinable values
    //    - Little time is spend in decoding
    //    - Most time is spend in buffer memcopying (we remove the interleaved lengths)
    //    - Possible UTF-8 verification is fast because the continuation byte trick
    // 3. Mixed inlinable and non-inlinable values
    //    - Time shared between decoding and buffer forming
    //    - UTF-8 verification might still use len_below_128 trick, but might need to fall back to
    //      slow path.

    target.finish_in_progress();
    unsafe { target.views_mut() }.reserve(num_rows);

    let start_target_length = target.len();

    let buffer_idx = target.completed_buffers().len() as u32;
    let mut buffer = Vec::with_capacity(values.len() + 1);
    let mut none_starting_with_continuation_byte = true; // Whether the transition from between strings is valid
    // UTF-8
    let mut all_len_below_128 = true; // Whether all the lengths of the values are below 128, this
    // allows us to make UTF-8 verification a lot faster.

    let mut total_bytes_len = 0;
    let mut num_inlined = 0;

    let mut mvalues = values;
    while let Some((is_valid, is_selected)) = next() {
        if !is_valid {
            if is_selected {
                unsafe { target.views_mut() }.push(unsafe { View::new_inline_unchecked(&[]) });
            }
            continue;
        }

        if mvalues.len() < 4 {
            return Err(invalid_input_err());
        }

        let length;
        (length, mvalues) = mvalues.split_at(4);
        let length: &[u8; 4] = unsafe { length.try_into().unwrap_unchecked() };
        let length = u32::from_le_bytes(*length);

        if mvalues.len() < length as usize {
            return Err(invalid_input_err());
        }

        let value;
        (value, mvalues) = mvalues.split_at(length as usize);

        all_len_below_128 &= value.len() < 128;
        // Everything starting with 10.. .... is a continuation byte.
        none_starting_with_continuation_byte &=
            value.is_empty() || value[0] & 0b1100_0000 != 0b1000_0000;

        if !is_selected {
            continue;
        }

        let offset = buffer.len() as u32;

        if value.len() <= View::MAX_INLINE_SIZE as usize {
            unsafe { target.views_mut() }.push(unsafe { View::new_inline_unchecked(value) });
            num_inlined += 1;
        } else {
            buffer.extend_from_slice(value);
            unsafe { target.views_mut() }
                .push(unsafe { View::new_noninline_unchecked(value, buffer_idx, offset) });
        }

        total_bytes_len += value.len();
    }

    unsafe {
        target.set_total_bytes_len(target.total_bytes_len() + total_bytes_len);
    }

    if verify_utf8 {
        // This is a trick that allows us to check the resulting buffer which allows to batch the
        // UTF-8 verification.
        //
        // This is allowed if none of the strings start with a UTF-8 continuation byte, so we keep
        // track of that during the decoding.
        if num_inlined == 0 {
            if !none_starting_with_continuation_byte || simdutf8::basic::from_utf8(&buffer).is_err()
            {
                return Err(invalid_utf8_err());
            }

        // This is a small trick that allows us to check the Parquet buffer instead of the view
        // buffer. Batching the UTF-8 verification is more performant. For this to be allowed,
        // all the interleaved lengths need to be valid UTF-8.
        //
        // Every strings prepended by 4 bytes (L, 0, 0, 0), since we check here L < 128. L is
        // only a valid first byte of a UTF-8 code-point and (L, 0, 0, 0) is valid UTF-8.
        // Consequently, it is valid to just check the whole buffer.
        } else if all_len_below_128 {
            if simdutf8::basic::from_utf8(&values[..values.len() - mvalues.len()]).is_err() {
                return Err(invalid_utf8_err());
            }
        } else {
            // We check all the non-inlined values here.
            if !none_starting_with_continuation_byte || simdutf8::basic::from_utf8(&buffer).is_err()
            {
                return Err(invalid_utf8_err());
            }

            let mut all_inlined_are_ascii = true;

            // @NOTE: This is only valid because we initialize our inline View's to be zeroes on
            // non-included bytes.
            for view in &target.views()[start_target_length..] {
                all_inlined_are_ascii &= (view.length > View::MAX_INLINE_SIZE)
                    | (view.as_u128() & 0x0000_0000_8080_8080_8080_8080_8080_8080 == 0);
            }

            // This is the very slow path.
            if !all_inlined_are_ascii {
                let mut is_valid = true;
                for view in &target.views()[start_target_length..] {
                    if view.length <= View::MAX_INLINE_SIZE {
                        is_valid &=
                            std::str::from_utf8(unsafe { view.get_inlined_slice_unchecked() })
                                .is_ok();
                    }
                }

                if !is_valid {
                    return Err(invalid_utf8_err());
                }
            }
        }
    }

    target.push_buffer(buffer.into());

    Ok(())
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn decode_plain_generic(
    values: &[u8],
    target: &mut MutableBinaryViewArray<[u8]>,

    num_rows: usize,
    mut next: impl FnMut() -> Option<(bool, bool)>,

    verify_utf8: bool,
) -> ParquetResult<()> {
    // Since the offset in the buffer is decided by the interleaved lengths, every value has to be
    // walked no matter what. This makes decoding rather inefficient in general.
    //
    // There are three cases:
    // 1. All inlinable values
    //    - Most time is spend in decoding
    //    - No additional buffer has to be formed
    //    - Possible UTF-8 verification is fast because the len_below_128 trick
    // 2. All non-inlinable values
    //    - Little time is spend in decoding
    //    - Most time is spend in buffer memcopying (we remove the interleaved lengths)
    //    - Possible UTF-8 verification is fast because the continuation byte trick
    // 3. Mixed inlinable and non-inlinable values
    //    - Time shared between decoding and buffer forming
    //    - UTF-8 verification might still use len_below_128 trick, but might need to fall back to
    //      slow path.

    target.finish_in_progress();
    unsafe { target.views_mut() }.reserve(num_rows);

    let start_target_length = target.len();

    let buffer_idx = target.completed_buffers().len() as u32;
    let mut buffer = Vec::with_capacity(values.len() + 1);
    let mut none_starting_with_continuation_byte = true; // Whether the transition from between strings is valid
    // UTF-8
    let mut all_len_below_128 = true; // Whether all the lengths of the values are below 128, this
    // allows us to make UTF-8 verification a lot faster.

    let mut total_bytes_len = 0;
    let mut num_inlined = 0;

    let mut mvalues = values;
    while let Some((is_valid, is_selected)) = next() {
        if !is_valid {
            if is_selected {
                unsafe { target.views_mut() }.push(unsafe { View::new_inline_unchecked(&[]) });
            }
            continue;
        }

        if mvalues.len() < 4 {
            return Err(invalid_input_err());
        }

        let length;
        (length, mvalues) = mvalues.split_at(4);
        let length: &[u8; 4] = unsafe { length.try_into().unwrap_unchecked() };
        let length = u32::from_le_bytes(*length);

        if mvalues.len() < length as usize {
            return Err(invalid_input_err());
        }

        let value;
        (value, mvalues) = mvalues.split_at(length as usize);

        all_len_below_128 &= value.len() < 128;
        // Everything starting with 10.. .... is a continuation byte.
        none_starting_with_continuation_byte &=
            value.is_empty() || value[0] & 0b1100_0000 != 0b1000_0000;

        if !is_selected {
            continue;
        }

        let offset = buffer.len() as u32;

        if value.len() <= View::MAX_INLINE_SIZE as usize {
            unsafe { target.views_mut() }.push(unsafe { View::new_inline_unchecked(value) });
            num_inlined += 1;
        } else {
            buffer.extend_from_slice(value);
            unsafe { target.views_mut() }
                .push(unsafe { View::new_noninline_unchecked(value, buffer_idx, offset) });
        }

        total_bytes_len += value.len();
    }

    unsafe {
        target.set_total_bytes_len(target.total_bytes_len() + total_bytes_len);
    }

    if verify_utf8 {
        // This is a trick that allows us to check the resulting buffer which allows to batch the
        // UTF-8 verification.
        //
        // This is allowed if none of the strings start with a UTF-8 continuation byte, so we keep
        // track of that during the decoding.
        if num_inlined == 0 {
            if !none_starting_with_continuation_byte || simdutf8::basic::from_utf8(&buffer).is_err()
            {
                return Err(invalid_utf8_err());
            }

        // This is a small trick that allows us to check the Parquet buffer instead of the view
        // buffer. Batching the UTF-8 verification is more performant. For this to be allowed,
        // all the interleaved lengths need to be valid UTF-8.
        //
        // Every strings prepended by 4 bytes (L, 0, 0, 0), since we check here L < 128. L is
        // only a valid first byte of a UTF-8 code-point and (L, 0, 0, 0) is valid UTF-8.
        // Consequently, it is valid to just check the whole buffer.
        } else if all_len_below_128 {
            if simdutf8::basic::from_utf8(&values[..values.len() - mvalues.len()]).is_err() {
                return Err(invalid_utf8_err());
            }
        } else {
            // We check all the non-inlined values here.
            if !none_starting_with_continuation_byte || simdutf8::basic::from_utf8(&buffer).is_err()
            {
                return Err(invalid_utf8_err());
            }

            let mut all_inlined_are_ascii = true;

            // @NOTE: This is only valid because we initialize our inline View's to be zeroes on
            // non-included bytes. The mask also covers the length, which is below 128 for inline
            // views.
            for view in &target.views()[start_target_length..] {
                all_inlined_are_ascii &= (view.length > View::MAX_INLINE_SIZE)
                    | (view.as_u128() & 0x8080_8080_8080_8080_8080_8080_8080_8080 == 0);
            }

            // This is the very slow path.
            if !all_inlined_are_ascii {
                let mut is_valid = true;
                for view in &target.views()[start_target_length..] {
                    if view.length <= View::MAX_INLINE_SIZE {
                        is_valid &=
                            std::str::from_utf8(unsafe { view.get_inlined_slice_unchecked() })
                                .is_ok();
                    }
                }

                if !is_valid {
                    return Err(invalid_utf8_err());
                }
            }
        }
    }

    target.push_buffer(buffer.into());

    Ok(())
}
```


---

### 🔹 Commit #15: `bc7ab105`
- **完整 Hash**: `bc7ab1054522f1c59356ac3666997eb4d0b50e7d`
- **說明 (Ground Truth)**: fix: Fix `shift` with `fill_value` reporting the wrong lazy schema (#29978)
- **變更檔案數**: 2

#### 📄 檔案: `crates/polars-plan/src/plans/aexpr/function_expr/schema.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:182, E:265, A:0) ➔ After(N:186, E:270, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 5, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `dtype.is_categorical (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `mapper.args()[2].dtype (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `get_supertype (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `dtype.is_enum (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `IRFunctionExpr::get_field` ──[CALLS]──> `mapper.args()[2].dtype (External/Unresolved)`
  • + [新增呼叫邊] `IRFunctionExpr::get_field` ──[CALLS]──> `dtype.is_categorical (External/Unresolved)`
  • + [新增呼叫邊] `IRFunctionExpr::get_field` ──[CALLS]──> `dtype.is_enum (External/Unresolved)`
  • + [新增呼叫邊] `IRFunctionExpr::get_field` ──[CALLS]──> `matches! (Macro)`
  • + [新增呼叫邊] `IRFunctionExpr::get_field` ──[CALLS]──> `get_supertype (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `IRFunctionExpr::get_field()`
- **變更前簽章 (Before)**: `fn IRFunctionExpr::get_field(&self, fields: &[Field])` (L8~L584)
- **變更後簽章 (After)**: `fn IRFunctionExpr::get_field(&self, fields: &[Field])` (L8~L598)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn get_field(&self, fields: &[Field]) -> PolarsResult<Field> {
        use IRFunctionExpr::*;

        let mapper = FieldsMapper { fields };
        match self {
            // Namespaces
            #[cfg(feature = "dtype-array")]
            ArrayExpr(func) => func.get_field(mapper),
            BinaryExpr(s) => s.get_field(mapper),
            #[cfg(feature = "dtype-categorical")]
            Categorical(func) => func.get_field(mapper),
            #[cfg(feature = "dtype-extension")]
            Extension(func) => func.get_field(mapper),
            ListExpr(func) => func.get_field(mapper),
            #[cfg(feature = "dtype-map")]
            MapExpr(func) => func.get_field(mapper),
            #[cfg(feature = "strings")]
            StringExpr(s) => s.get_field(mapper),
            #[cfg(feature = "dtype-struct")]
            StructExpr(s) => s.get_field(mapper),
            #[cfg(feature = "temporal")]
            TemporalExpr(fun) => fun.get_field(mapper),
            #[cfg(feature = "bitwise")]
            Bitwise(fun) => fun.get_field(mapper),

            // Other expressions
            Boolean(func) => func.get_field(mapper),
            #[cfg(feature = "business")]
            Business(func) => func.get_field(mapper),
            #[cfg(feature = "abs")]
            Abs => mapper.with_same_dtype(),
            Negate => mapper.with_same_dtype(),
            NullCount => mapper.with_dtype(IDX_DTYPE),
            Pow(pow_function) => match pow_function {
                IRPowFunction::Generic => mapper.pow_dtype(),
                _ => mapper.map_numeric_to_float_dtype(true),
            },
            Coalesce => mapper.map_to_supertype(),
            #[cfg(feature = "row_hash")]
            Hash(..) => mapper.with_dtype(DataType::UInt64),
            #[cfg(feature = "arg_where")]
            ArgWhere => mapper.with_dtype(IDX_DTYPE),
            #[cfg(feature = "index_of")]
            IndexOf => mapper.with_dtype(IDX_DTYPE),
            #[cfg(feature = "search_sorted")]
            SearchSorted { .. } => mapper.with_dtype(IDX_DTYPE),
            #[cfg(feature = "range")]
            Range(func) => func.get_field(mapper),
            #[cfg(feature = "trigonometry")]
            Trigonometry(_) => mapper.map_to_float_dtype(),
            #[cfg(feature = "trigonometry")]
            Atan2 => mapper.map_to_float_dtype(),
            #[cfg(feature = "sign")]
            Sign => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric(), "sign")?
                .map_dtype(|dt| match dt {
                    // The result 1 needs an integer digit.
                    #[cfg(feature = "dtype-decimal")]
                    DataType::Decimal(p, s) => {
                        DataType::Decimal((*p).max(s + 1).min(DEC128_MAX_PREC), *s)
                    },
                    dt => dt.clone(),
                }),
            FillNull => mapper.map_to_supertype(),
            #[cfg(feature = "rolling_window")]
            RollingExpr { function, options } => {
                use IRRollingFunction::*;
                match function {
                    Min | Max => mapper.with_same_dtype(),
                    Mean | Quantile => mapper.moment_dtype(),
                    Std => mapper.var_dtype("std"),
                    Var => mapper.var_dtype("var"),
                    Sum => mapper.sum_dtype(),
                    Rank => match options.fn_params {
                        Some(RollingFnParams::Rank {
                            method: RollingRankMethod::Average,
                            ..
                        }) => mapper.with_dtype(DataType::Float64),
                        Some(RollingFnParams::Rank { .. }) => mapper.with_dtype(IDX_DTYPE),
                        _ => unreachable!("should be Some(RollingFnParams::Rank)"),
                    },
                    #[cfg(feature = "cov")]
                    CorrCov { .. } => mapper.try_map_dtypes(|dtypes| {
                        Ok(match try_get_supertype(dtypes[0], dtypes[1])? {
                            dt if dt.is_float() => dt,
                            _ => DataType::Float64,
                        })
                    }),
                    #[cfg(feature = "moment")]
                    Skew | Kurtosis => mapper.map_to_float_dtype(),
                    Map(_) => mapper.try_map_field(|field| {
                        if options.weights.is_some() {
                            let dtype = match field.dtype() {
                                #[cfg(feature = "dtype-f16")]
                                DataType::Float16 => DataType::Float16,
                                DataType::Float32 => DataType::Float32,
                                _ => DataType::Float64,
                            };
                            Ok(Field::new(field.name().clone(), dtype))
                        } else {
                            Ok(field.clone())
                        }
                    }),
                }
            },
            #[cfg(feature = "rolling_window_by")]
            RollingExprBy {
                function_by,
                options,
                ..
            } => {
                use IRRollingFunctionBy::*;
                match function_by {
                    MinBy | MaxBy => mapper.with_same_dtype(),
                    MeanBy | QuantileBy => mapper.moment_dtype(),
                    StdBy => mapper.var_dtype("std"),
                    VarBy => mapper.var_dtype("var"),
                    SumBy => mapper.sum_dtype(),
                    RankBy => match options.fn_params {
                        Some(RollingFnParams::Rank {
                            method: RollingRankMethod::Average,
                            ..
                        }) => mapper.with_dtype(DataType::Float64),
                        Some(RollingFnParams::Rank { .. }) => mapper.with_dtype(IDX_DTYPE),
                        _ => unreachable!("should be Some(RollingFnParams::Rank)"),
                    },
                }
            },
            ShiftAndFill => mapper.with_same_dtype(),
            DropNans => mapper.with_same_dtype(),
            DropNulls => mapper.with_same_dtype(),
            #[cfg(feature = "round_series")]
            Clip {
                has_min: _,
                has_max: _,
            } => mapper.with_same_dtype(),
            Quantile { method: _ } => mapper.quantile_dtype(),
            #[cfg(feature = "mode")]
            Mode { maintain_order: _ } => mapper.with_same_dtype(),
            #[cfg(feature = "moment")]
            Skew(_) => mapper.with_dtype(DataType::Float64),
            #[cfg(feature = "moment")]
            Kurtosis(..) => mapper.with_dtype(DataType::Float64),
            ArgUnique | ArgMin | ArgMax | ArgSort { .. } => mapper.with_dtype(IDX_DTYPE),
            MinBy { .. } | MaxBy { .. } => mapper.with_same_dtype(),
            Product => mapper.map_dtype(|dtype| {
                use DataType as T;
                match dtype {
                    #[cfg(feature = "dtype-f16")]
                    T::Float16 => T::Float16,
                    T::Float32 => T::Float32,
                    T::Float64 => T::Float64,
                    T::UInt64 => T::UInt64,
                    #[cfg(feature = "dtype-i128")]
                    T::Int128 => T::Int128,
                    #[cfg(feature = "dtype-decimal")]
                    T::Decimal(_p, s) => T::Decimal(DEC128_MAX_PREC, *s),
                    _ => T::Int64,
                }
            }),
            Repeat => mapper.with_same_dtype(),
            #[cfg(feature = "rank")]
            Rank { options, .. } => mapper.with_dtype(match options.method {
                RankMethod::Average => DataType::Float64,
                _ => IDX_DTYPE,
            }),
            AsList => mapper.map_to_list_of_dtypes(),
            #[cfg(feature = "dtype-struct")]
            AsStruct => {
                let mut field_names = PlIndexSet::with_capacity(fields.len() - 1);
                let struct_fields = fields
                    .iter()
                    .map(|f| {
                        polars_ensure!(
                            field_names.insert(f.name.as_str()),
                            duplicate_field = f.name()
                        );
                        Ok(f.clone())
                    })
                    .collect::<PolarsResult<Vec<_>>>()?;
                Ok(Field::new(
                    fields[0].name().clone(),
                    DataType::Struct(struct_fields),
                ))
            },
            #[cfg(feature = "top_k")]
            TopK { .. } => mapper.with_same_dtype(),
            #[cfg(feature = "top_k")]
            TopKBy { .. } => mapper.with_same_dtype(),
            #[cfg(feature = "dtype-struct")]
            ValueCounts {
                sort: _,
                parallel: _,
                name,
                normalize,
            } => mapper.map_dtype(|dt| {
                let count_dt = if *normalize {
                    DataType::Float64
                } else {
                    IDX_DTYPE
                };
                DataType::Struct(vec![
                    Field::new(fields[0].name().clone(), dt.clone()),
                    Field::new(name.clone(), count_dt),
                ])
            }),
            #[cfg(feature = "unique_counts")]
            UniqueCounts => mapper.with_dtype(IDX_DTYPE),
            Shift | Reverse => mapper.with_same_dtype(),
            #[cfg(feature = "cum_agg")]
            CumCount { .. } => mapper.with_dtype(IDX_DTYPE),
            #[cfg(feature = "cum_agg")]
            CumSum { .. } => mapper.map_dtype(cum::dtypes::cum_sum),
            #[cfg(feature = "cum_agg")]
            CumProd { .. } => mapper.map_dtype(cum::dtypes::cum_prod),
            #[cfg(feature = "cum_agg")]
            CumMin { .. } => mapper.with_same_dtype(),
            #[cfg(feature = "cum_agg")]
            CumMax { .. } => mapper.with_same_dtype(),
            #[cfg(feature = "approx_unique")]
            ApproxNUnique => mapper.with_dtype(IDX_DTYPE),
            #[cfg(feature = "approx_quantile")]
            ApproxQuantileSketch { .. } => mapper.with_dtype(DataType::Binary),
            #[cfg(feature = "approx_quantile")]
            ApproxQuantileEstimate { values_dtype } => {
                if mapper.args()[1].dtype().is_list() {
                    mapper.with_dtype(DataType::List(Box::new(values_dtype.clone())))
                } else {
                    mapper.with_dtype(values_dtype.clone())
                }
            },
            #[cfg(feature = "hist")]
            Hist {
                include_category,
                include_breakpoint,
                ..
            } => {
                if *include_breakpoint || *include_category {
                    let mut fields = Vec::with_capacity(3);
                    if *include_breakpoint {
                        fields.push(Field::new(
                            PlSmallStr::from_static("breakpoint"),
                            DataType::Float64,
                        ));
                    }
                    if *include_category {
                        fields.push(Field::new(
                            PlSmallStr::from_static("category"),
                            DataType::from_categories(Categories::global()),
                        ));
                    }
                    fields.push(Field::new(PlSmallStr::from_static("count"), IDX_DTYPE));
                    mapper.with_dtype(DataType::Struct(fields))
                } else {
                    mapper.with_dtype(IDX_DTYPE)
                }
            },
            #[cfg(feature = "diff")]
            Diff(_) => mapper.map_dtype(|dt| match dt {
                #[cfg(feature = "dtype-datetime")]
                DataType::Datetime(tu, _) => DataType::Duration(*tu),
                #[cfg(feature = "dtype-date")]
                DataType::Date => DataType::Duration(TimeUnit::Microseconds),
                #[cfg(feature = "dtype-time")]
                DataType::Time => DataType::Duration(TimeUnit::Nanoseconds),
                DataType::UInt64 | DataType::UInt32 => DataType::Int64,
                DataType::UInt16 => DataType::Int32,
                DataType::UInt8 => DataType::Int16,
                #[cfg(feature = "dtype-decimal")]
                DataType::Decimal(_, scale) => DataType::Decimal(DEC128_MAX_PREC, *scale),
                dt => dt.clone(),
            }),
            #[cfg(feature = "pct_change")]
            PctChange => mapper.map_dtype(|dt| match dt {
                #[cfg(feature = "dtype-f16")]
                DataType::Float16 => dt.clone(),
                DataType::Float32 => dt.clone(),
                _ => DataType::Float64,
            }),
            #[cfg(feature = "interpolate")]
            Interpolate(method) => match method {
                InterpolationMethod::Linear => mapper.map_numeric_to_float_dtype(false),
                InterpolationMethod::Nearest => mapper.with_same_dtype(),
            },
            #[cfg(feature = "interpolate_by")]
            InterpolateBy => mapper.map_numeric_to_float_dtype(true),
            #[cfg(feature = "log")]
            Entropy { .. } => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric() || dtype.is_bool(), "entropy")?
                .map_to_float_dtype(),
            #[cfg(feature = "log")]
            Log1p => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric() || dtype.is_bool(), "log1p")?
                .map_to_float_dtype(),
            #[cfg(feature = "log")]
            Exp => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric() || dtype.is_bool(), "exp")?
                .map_to_float_dtype(),
            #[cfg(feature = "log")]
            Erf => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric() || dtype.is_bool(), "erf")?
                .map_to_float_dtype(),
            #[cfg(feature = "log")]
            Erfc => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric() || dtype.is_bool(), "erfc")?
                .map_to_float_dtype(),
            #[cfg(feature = "log")]
            Log => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric() || dtype.is_bool(), "log")?
                .log_dtype(),
            Unique(_) => mapper.with_same_dtype(),
            // Rounding a decimal away from zero can carry into one more integer digit.
            #[cfg(feature = "round_series")]
            Round { decimals, mode } => mapper.map_dtype(|dt| match dt {
                #[cfg(feature = "dtype-decimal")]
                DataType::Decimal(p, s)
                    if *s > *decimals as usize && *mode != RoundMode::ToZero =>
                {
                    DataType::Decimal((p + 1).min(DEC128_MAX_PREC), *s)
                },
                dt => dt.clone(),
            }),
            #[cfg(feature = "round_series")]
            RoundSF { .. } => mapper.map_dtype(|dt| match dt {
                #[cfg(feature = "dtype-decimal")]
                DataType::Decimal(p, s) => DataType::Decimal((p + 1).min(DEC128_MAX_PREC), *s),
                dt => dt.clone(),
            }),
            #[cfg(feature = "round_series")]
            Floor | Ceil => mapper.map_dtype(|dt| match dt {
                #[cfg(feature = "dtype-decimal")]
                DataType::Decimal(p, s) if *s > 0 => {
                    DataType::Decimal((p + 1).min(DEC128_MAX_PREC), *s)
                },
                dt => dt.clone(),
            }),
            #[cfg(feature = "round_series")]
            Truncate { .. } => mapper.with_same_dtype(),
            #[cfg(feature = "dtype-decimal")]
            DecimalArith { op, scale } => mapper
                .ensure_satisfies(
                    |_, dtype| dtype.is_decimal() || dtype.is_integer(),
                    op.name(),
                )?
                .with_dtype(DataType::Decimal(DEC128_MAX_PREC, *scale)),
            // With a decimal, the remainder keeps the larger scale (integers are scale 0)
            // and the quotient is an integer; other numerics keep their supertype.
            TruncArith(op) => {
                let args = mapper.args();
                match (args[0].dtype(), args[1].dtype()) {
                    #[cfg(feature = "dtype-decimal")]
                    (l, r) if l.is_decimal() || r.is_decimal() => {
                        let scale = |dt: &DataType| match dt {
                            DataType::Decimal(_, s) => *s,
                            _ => 0,
                        };
                        let scale = match op {
                            TruncArithOp::Rem => scale(l).max(scale(r)),
                            TruncArithOp::IntDiv => 0,
                        };
                        mapper.with_dtype(DataType::Decimal(DEC128_MAX_PREC, scale))
                    },
                    _ => mapper.map_to_supertype(),
                }
            },
            #[cfg(feature = "fused")]
            Fused(_) => mapper.map_to_supertype(),
            ConcatExpr { .. } => mapper.map_to_supertype(),
            #[cfg(feature = "cov")]
            Correlation { .. } => mapper.map_to_float_dtype(),
            #[cfg(feature = "peaks")]
            PeakMin | PeakMax => mapper.with_dtype(DataType::Boolean),
            #[cfg(feature = "cutqcut")]
            Cut {
                breaks,
                labels,
                left_closed,
                include_breaks,
            } => {
                let cut_labels: Vec<PlSmallStr> = if let Some(l) = labels {
                    polars_ensure!(
                        l.len() == breaks.len() + 1,
                        ShapeMismatch: "expected {} labels (len(breaks) + 1), got {}",
                        breaks.len() + 1, l.len()
                    );
                    l.clone()
                } else {
                    use polars_core::utils::cut::compute_cut_labels;

                    compute_cut_labels(breaks, *left_closed)?
                };
                let enum_dtype = DataType::from_frozen_categories(FrozenCategories::new(
                    cut_labels.iter().map(|s| s.as_str()),
                )?);
                if *include_breaks {
                    let struct_dt = DataType::Struct(vec![
                        Field::new(PlSmallStr::from_static("breakpoint"), DataType::Float64),
                        Field::new(PlSmallStr::from_static("category"), enum_dtype),
                    ]);
                    mapper.with_dtype(struct_dt)
                } else {
                    mapper.with_dtype(enum_dtype)
                }
            },
            #[cfg(feature = "repeat_by")]
            RepeatBy => mapper.map_dtype(|dt| DataType::List(dt.clone().into())),
            #[cfg(feature = "dtype-array")]
            Reshape(dims) => mapper.try_map_dtype(|dt: &DataType| {
                let mut wrapped_dtype = dt.leaf_dtype().clone();
                for dim in dims[1..].iter().rev() {
                    let Some(array_size) = dim.get() else {
                        polars_bail!(InvalidOperation: "can only infer the first dimension");
                    };
                    wrapped_dtype = DataType::Array(Box::new(wrapped_dtype), array_size as usize);
                }
                Ok(wrapped_dtype)
            }),
            #[cfg(feature = "cutqcut")]
            QCut {
                include_breaks: false,
                ..
            } => mapper.with_dtype(DataType::from_categories(Categories::global())),
            #[cfg(feature = "cutqcut")]
            QCut {
                include_breaks: true,
                ..
            } => {
                let struct_dt = DataType::Struct(vec![
                    Field::new(PlSmallStr::from_static("breakpoint"), DataType::Float64),
                    Field::new(
                        PlSmallStr::from_static("category"),
                        DataType::from_categories(Categories::global()),
                    ),
                ]);
                mapper.with_dtype(struct_dt)
            },
            #[cfg(feature = "cutqcut")]
            Bin(options) => {
                let n_bins = options.method.n_bins();
                let bin_dtype = match &options.labels {
                    None => DataType::UInt32,
                    Some(labels) => {
                        polars_ensure!(
                            labels.len() == n_bins,
                            ShapeMismatch: "`{}` produces {} bins but got {} labels",
                            options.method.name(), n_bins, labels.len()
                        );
                        DataType::from_frozen_categories(FrozenCategories::new(
                            labels.iter().map(|s| s.as_str()),
                        )?)
                    },
                };
                if !options.include_intervals {
                    return mapper.with_dtype(bin_dtype);
                }
                // The input has been converted to the correct type during DSL -> IR conversion.
                let bound = mapper.args()[0].dtype().clone();
                mapper.with_dtype(DataType::Struct(vec![
                    Field::new(PlSmallStr::from_static("bin"), bin_dtype),
                    Field::new(PlSmallStr::from_static("left"), bound.clone()),
                    Field::new(PlSmallStr::from_static("right"), bound),
                ]))
            },
            #[cfg(feature = "rle")]
            RLE => mapper.map_dtype(|dt| {
                DataType::Struct(vec![
                    Field::new(PlSmallStr::from_static("len"), IDX_DTYPE),
                    Field::new(PlSmallStr::from_static("value"), dt.clone()),
                ])
            }),
            #[cfg(feature = "rle")]
            RLEID => mapper.with_dtype(IDX_DTYPE),
            ToPhysical => mapper.to_physical_type(),
            #[cfg(feature = "random")]
            Random { .. } => mapper.with_same_dtype(),
            SetSortedFlag(_) => mapper.with_same_dtype(),
            #[cfg(feature = "ffi_plugin")]
            FfiPlugin {
                flags: _,
                is_deterministic: _,
                lib,
                symbol,
                kwargs,
            } => unsafe { plugin::plugin_field(fields, lib, symbol.as_ref(), kwargs) },

            FoldHorizontal { return_dtype, .. } => match return_dtype {
                None => mapper.with_same_dtype(),
                Some(dtype) => mapper.with_dtype(dtype.clone()),
            },
            ReduceHorizontal { return_dtype, .. } => match return_dtype {
                None => mapper.map_to_supertype(),
                Some(dtype) => mapper.with_dtype(dtype.clone()),
            },
            #[cfg(feature = "dtype-struct")]
            CumReduceHorizontal { return_dtype, .. } => match return_dtype {
                None => mapper.with_dtype(DataType::Struct(fields.to_vec())),
                Some(dtype) => mapper.with_dtype(DataType::Struct(
                    fields
                        .iter()
                        .map(|f| Field::new(f.name().clone(), dtype.clone()))
                        .collect(),
                )),
            },
            #[cfg(feature = "dtype-struct")]
            CumFoldHorizontal {
                return_dtype,
                include_init,
                ..
            } => match return_dtype {
                None => mapper.with_dtype(DataType::Struct(
                    fields
                        .iter()
                        .skip(usize::from(!include_init))
                        .map(|f| Field::new(f.name().clone(), fields[0].dtype().clone()))
                        .collect(),
                )),
                Some(dtype) => mapper.with_dtype(DataType::Struct(
                    fields
                        .iter()
                        .skip(usize::from(!include_init))
                        .map(|f| Field::new(f.name().clone(), dtype.clone()))
                        .collect(),
                )),
            },

            MaxHorizontal => mapper.map_to_supertype(),
            MinHorizontal => mapper.map_to_supertype(),
            SumHorizontal { .. } => mapper.map_to_supertype().map(|mut f| {
                if f.dtype == DataType::Boolean {
                    f.dtype = IDX_DTYPE;
                }
                f
            }),
            MeanHorizontal { .. } => mapper.map_to_supertype().map(|mut f| {
                match f.dtype {
                    #[cfg(feature = "dtype-f16")]
                    DataType::Float16 => {},
                    DataType::Float32 => {},
                    _ => {
                        f.dtype = DataType::Float64;
                    },
                }
                f
            }),
            #[cfg(feature = "ewma")]
            EwmMean { .. } => mapper.map_numeric_to_float_dtype(true),
            #[cfg(feature = "ewma_by")]
            EwmMeanBy { .. } => mapper.map_numeric_to_float_dtype(true),
            #[cfg(feature = "ewma")]
            EwmSum { .. } => mapper.map_numeric_to_float_dtype(true),
            #[cfg(feature = "ewma_by")]
            EwmSumBy { .. } => mapper.map_numeric_to_float_dtype(true),
            #[cfg(feature = "ewma")]
            EwmStd { .. } => mapper.ewm_var_dtype("ewm_std", true),
            #[cfg(feature = "ewma")]
            EwmVar { .. } => mapper.ewm_var_dtype("ewm_var", true),
            #[cfg(feature = "replace")]
            Replace => mapper.with_same_dtype(),
            #[cfg(feature = "replace")]
            ReplaceStrict { return_dtype } => mapper.replace_dtype(return_dtype.clone()),
            FillNullWithStrategy(_) => mapper.with_same_dtype(),
            GatherEvery { .. } => mapper.with_same_dtype(),
            #[cfg(feature = "reinterpret")]
            Reinterpret(dtype) => mapper.with_dtype(dtype.clone()),
            ExtendConstant => mapper.with_same_dtype(),

            RowEncode(..) => mapper.try_map_field(|_| {
                Ok(Field::new(
                    PlSmallStr::from_static("row_encoded"),
                    DataType::BinaryOffset,
                ))
            }),
            #[cfg(feature = "dtype-struct")]
            RowDecode(fields, _) => mapper.with_dtype(DataType::Struct(fields.to_vec())),
            DynamicPred { .. } | DynamicSkipBatch { .. } => mapper.with_dtype(DataType::Boolean),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn get_field(&self, fields: &[Field]) -> PolarsResult<Field> {
        use IRFunctionExpr::*;

        let mapper = FieldsMapper { fields };
        match self {
            // Namespaces
            #[cfg(feature = "dtype-array")]
            ArrayExpr(func) => func.get_field(mapper),
            BinaryExpr(s) => s.get_field(mapper),
            #[cfg(feature = "dtype-categorical")]
            Categorical(func) => func.get_field(mapper),
            #[cfg(feature = "dtype-extension")]
            Extension(func) => func.get_field(mapper),
            ListExpr(func) => func.get_field(mapper),
            #[cfg(feature = "dtype-map")]
            MapExpr(func) => func.get_field(mapper),
            #[cfg(feature = "strings")]
            StringExpr(s) => s.get_field(mapper),
            #[cfg(feature = "dtype-struct")]
            StructExpr(s) => s.get_field(mapper),
            #[cfg(feature = "temporal")]
            TemporalExpr(fun) => fun.get_field(mapper),
            #[cfg(feature = "bitwise")]
            Bitwise(fun) => fun.get_field(mapper),

            // Other expressions
            Boolean(func) => func.get_field(mapper),
            #[cfg(feature = "business")]
            Business(func) => func.get_field(mapper),
            #[cfg(feature = "abs")]
            Abs => mapper.with_same_dtype(),
            Negate => mapper.with_same_dtype(),
            NullCount => mapper.with_dtype(IDX_DTYPE),
            Pow(pow_function) => match pow_function {
                IRPowFunction::Generic => mapper.pow_dtype(),
                _ => mapper.map_numeric_to_float_dtype(true),
            },
            Coalesce => mapper.map_to_supertype(),
            #[cfg(feature = "row_hash")]
            Hash(..) => mapper.with_dtype(DataType::UInt64),
            #[cfg(feature = "arg_where")]
            ArgWhere => mapper.with_dtype(IDX_DTYPE),
            #[cfg(feature = "index_of")]
            IndexOf => mapper.with_dtype(IDX_DTYPE),
            #[cfg(feature = "search_sorted")]
            SearchSorted { .. } => mapper.with_dtype(IDX_DTYPE),
            #[cfg(feature = "range")]
            Range(func) => func.get_field(mapper),
            #[cfg(feature = "trigonometry")]
            Trigonometry(_) => mapper.map_to_float_dtype(),
            #[cfg(feature = "trigonometry")]
            Atan2 => mapper.map_to_float_dtype(),
            #[cfg(feature = "sign")]
            Sign => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric(), "sign")?
                .map_dtype(|dt| match dt {
                    // The result 1 needs an integer digit.
                    #[cfg(feature = "dtype-decimal")]
                    DataType::Decimal(p, s) => {
                        DataType::Decimal((*p).max(s + 1).min(DEC128_MAX_PREC), *s)
                    },
                    dt => dt.clone(),
                }),
            FillNull => mapper.map_to_supertype(),
            #[cfg(feature = "rolling_window")]
            RollingExpr { function, options } => {
                use IRRollingFunction::*;
                match function {
                    Min | Max => mapper.with_same_dtype(),
                    Mean | Quantile => mapper.moment_dtype(),
                    Std => mapper.var_dtype("std"),
                    Var => mapper.var_dtype("var"),
                    Sum => mapper.sum_dtype(),
                    Rank => match options.fn_params {
                        Some(RollingFnParams::Rank {
                            method: RollingRankMethod::Average,
                            ..
                        }) => mapper.with_dtype(DataType::Float64),
                        Some(RollingFnParams::Rank { .. }) => mapper.with_dtype(IDX_DTYPE),
                        _ => unreachable!("should be Some(RollingFnParams::Rank)"),
                    },
                    #[cfg(feature = "cov")]
                    CorrCov { .. } => mapper.try_map_dtypes(|dtypes| {
                        Ok(match try_get_supertype(dtypes[0], dtypes[1])? {
                            dt if dt.is_float() => dt,
                            _ => DataType::Float64,
                        })
                    }),
                    #[cfg(feature = "moment")]
                    Skew | Kurtosis => mapper.map_to_float_dtype(),
                    Map(_) => mapper.try_map_field(|field| {
                        if options.weights.is_some() {
                            let dtype = match field.dtype() {
                                #[cfg(feature = "dtype-f16")]
                                DataType::Float16 => DataType::Float16,
                                DataType::Float32 => DataType::Float32,
                                _ => DataType::Float64,
                            };
                            Ok(Field::new(field.name().clone(), dtype))
                        } else {
                            Ok(field.clone())
                        }
                    }),
                }
            },
            #[cfg(feature = "rolling_window_by")]
            RollingExprBy {
                function_by,
                options,
                ..
            } => {
                use IRRollingFunctionBy::*;
                match function_by {
                    MinBy | MaxBy => mapper.with_same_dtype(),
                    MeanBy | QuantileBy => mapper.moment_dtype(),
                    StdBy => mapper.var_dtype("std"),
                    VarBy => mapper.var_dtype("var"),
                    SumBy => mapper.sum_dtype(),
                    RankBy => match options.fn_params {
                        Some(RollingFnParams::Rank {
                            method: RollingRankMethod::Average,
                            ..
                        }) => mapper.with_dtype(DataType::Float64),
                        Some(RollingFnParams::Rank { .. }) => mapper.with_dtype(IDX_DTYPE),
                        _ => unreachable!("should be Some(RollingFnParams::Rank)"),
                    },
                }
            },
            ShiftAndFill => {
                // Mirror type coercion, which casts the input and fill value to their supertype.
                // @3.0: Raise a type error instead of upcasting the input.
                let dtype = mapper.args()[0].dtype();
                let fill_dtype = mapper.args()[2].dtype();
                let is_cat_with_str_fill = (dtype.is_categorical() || dtype.is_enum())
                    && matches!(
                        fill_dtype,
                        DataType::String | DataType::Unknown(UnknownKind::Str)
                    );
                match get_supertype(dtype, fill_dtype) {
                    Some(st) if !is_cat_with_str_fill => mapper.with_dtype(st),
                    _ => mapper.with_same_dtype(),
                }
            },
            DropNans => mapper.with_same_dtype(),
            DropNulls => mapper.with_same_dtype(),
            #[cfg(feature = "round_series")]
            Clip {
                has_min: _,
                has_max: _,
            } => mapper.with_same_dtype(),
            Quantile { method: _ } => mapper.quantile_dtype(),
            #[cfg(feature = "mode")]
            Mode { maintain_order: _ } => mapper.with_same_dtype(),
            #[cfg(feature = "moment")]
            Skew(_) => mapper.with_dtype(DataType::Float64),
            #[cfg(feature = "moment")]
            Kurtosis(..) => mapper.with_dtype(DataType::Float64),
            ArgUnique | ArgMin | ArgMax | ArgSort { .. } => mapper.with_dtype(IDX_DTYPE),
            MinBy { .. } | MaxBy { .. } => mapper.with_same_dtype(),
            Product => mapper.map_dtype(|dtype| {
                use DataType as T;
                match dtype {
                    #[cfg(feature = "dtype-f16")]
                    T::Float16 => T::Float16,
                    T::Float32 => T::Float32,
                    T::Float64 => T::Float64,
                    T::UInt64 => T::UInt64,
                    #[cfg(feature = "dtype-i128")]
                    T::Int128 => T::Int128,
                    #[cfg(feature = "dtype-decimal")]
                    T::Decimal(_p, s) => T::Decimal(DEC128_MAX_PREC, *s),
                    _ => T::Int64,
                }
            }),
            Repeat => mapper.with_same_dtype(),
            #[cfg(feature = "rank")]
            Rank { options, .. } => mapper.with_dtype(match options.method {
                RankMethod::Average => DataType::Float64,
                _ => IDX_DTYPE,
            }),
            AsList => mapper.map_to_list_of_dtypes(),
            #[cfg(feature = "dtype-struct")]
            AsStruct => {
                let mut field_names = PlIndexSet::with_capacity(fields.len() - 1);
                let struct_fields = fields
                    .iter()
                    .map(|f| {
                        polars_ensure!(
                            field_names.insert(f.name.as_str()),
                            duplicate_field = f.name()
                        );
                        Ok(f.clone())
                    })
                    .collect::<PolarsResult<Vec<_>>>()?;
                Ok(Field::new(
                    fields[0].name().clone(),
                    DataType::Struct(struct_fields),
                ))
            },
            #[cfg(feature = "top_k")]
            TopK { .. } => mapper.with_same_dtype(),
            #[cfg(feature = "top_k")]
            TopKBy { .. } => mapper.with_same_dtype(),
            #[cfg(feature = "dtype-struct")]
            ValueCounts {
                sort: _,
                parallel: _,
                name,
                normalize,
            } => mapper.map_dtype(|dt| {
                let count_dt = if *normalize {
                    DataType::Float64
                } else {
                    IDX_DTYPE
                };
                DataType::Struct(vec![
                    Field::new(fields[0].name().clone(), dt.clone()),
                    Field::new(name.clone(), count_dt),
                ])
            }),
            #[cfg(feature = "unique_counts")]
            UniqueCounts => mapper.with_dtype(IDX_DTYPE),
            Shift | Reverse => mapper.with_same_dtype(),
            #[cfg(feature = "cum_agg")]
            CumCount { .. } => mapper.with_dtype(IDX_DTYPE),
            #[cfg(feature = "cum_agg")]
            CumSum { .. } => mapper.map_dtype(cum::dtypes::cum_sum),
            #[cfg(feature = "cum_agg")]
            CumProd { .. } => mapper.map_dtype(cum::dtypes::cum_prod),
            #[cfg(feature = "cum_agg")]
            CumMin { .. } => mapper.with_same_dtype(),
            #[cfg(feature = "cum_agg")]
            CumMax { .. } => mapper.with_same_dtype(),
            #[cfg(feature = "approx_unique")]
            ApproxNUnique => mapper.with_dtype(IDX_DTYPE),
            #[cfg(feature = "approx_quantile")]
            ApproxQuantileSketch { .. } => mapper.with_dtype(DataType::Binary),
            #[cfg(feature = "approx_quantile")]
            ApproxQuantileEstimate { values_dtype } => {
                if mapper.args()[1].dtype().is_list() {
                    mapper.with_dtype(DataType::List(Box::new(values_dtype.clone())))
                } else {
                    mapper.with_dtype(values_dtype.clone())
                }
            },
            #[cfg(feature = "hist")]
            Hist {
                include_category,
                include_breakpoint,
                ..
            } => {
                if *include_breakpoint || *include_category {
                    let mut fields = Vec::with_capacity(3);
                    if *include_breakpoint {
                        fields.push(Field::new(
                            PlSmallStr::from_static("breakpoint"),
                            DataType::Float64,
                        ));
                    }
                    if *include_category {
                        fields.push(Field::new(
                            PlSmallStr::from_static("category"),
                            DataType::from_categories(Categories::global()),
                        ));
                    }
                    fields.push(Field::new(PlSmallStr::from_static("count"), IDX_DTYPE));
                    mapper.with_dtype(DataType::Struct(fields))
                } else {
                    mapper.with_dtype(IDX_DTYPE)
                }
            },
            #[cfg(feature = "diff")]
            Diff(_) => mapper.map_dtype(|dt| match dt {
                #[cfg(feature = "dtype-datetime")]
                DataType::Datetime(tu, _) => DataType::Duration(*tu),
                #[cfg(feature = "dtype-date")]
                DataType::Date => DataType::Duration(TimeUnit::Microseconds),
                #[cfg(feature = "dtype-time")]
                DataType::Time => DataType::Duration(TimeUnit::Nanoseconds),
                DataType::UInt64 | DataType::UInt32 => DataType::Int64,
                DataType::UInt16 => DataType::Int32,
                DataType::UInt8 => DataType::Int16,
                #[cfg(feature = "dtype-decimal")]
                DataType::Decimal(_, scale) => DataType::Decimal(DEC128_MAX_PREC, *scale),
                dt => dt.clone(),
            }),
            #[cfg(feature = "pct_change")]
            PctChange => mapper.map_dtype(|dt| match dt {
                #[cfg(feature = "dtype-f16")]
                DataType::Float16 => dt.clone(),
                DataType::Float32 => dt.clone(),
                _ => DataType::Float64,
            }),
            #[cfg(feature = "interpolate")]
            Interpolate(method) => match method {
                InterpolationMethod::Linear => mapper.map_numeric_to_float_dtype(false),
                InterpolationMethod::Nearest => mapper.with_same_dtype(),
            },
            #[cfg(feature = "interpolate_by")]
            InterpolateBy => mapper.map_numeric_to_float_dtype(true),
            #[cfg(feature = "log")]
            Entropy { .. } => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric() || dtype.is_bool(), "entropy")?
                .map_to_float_dtype(),
            #[cfg(feature = "log")]
            Log1p => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric() || dtype.is_bool(), "log1p")?
                .map_to_float_dtype(),
            #[cfg(feature = "log")]
            Exp => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric() || dtype.is_bool(), "exp")?
                .map_to_float_dtype(),
            #[cfg(feature = "log")]
            Erf => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric() || dtype.is_bool(), "erf")?
                .map_to_float_dtype(),
            #[cfg(feature = "log")]
            Erfc => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric() || dtype.is_bool(), "erfc")?
                .map_to_float_dtype(),
            #[cfg(feature = "log")]
            Log => mapper
                .ensure_satisfies(|_, dtype| dtype.is_numeric() || dtype.is_bool(), "log")?
                .log_dtype(),
            Unique(_) => mapper.with_same_dtype(),
            // Rounding a decimal away from zero can carry into one more integer digit.
            #[cfg(feature = "round_series")]
            Round { decimals, mode } => mapper.map_dtype(|dt| match dt {
                #[cfg(feature = "dtype-decimal")]
                DataType::Decimal(p, s)
                    if *s > *decimals as usize && *mode != RoundMode::ToZero =>
                {
                    DataType::Decimal((p + 1).min(DEC128_MAX_PREC), *s)
                },
                dt => dt.clone(),
            }),
            #[cfg(feature = "round_series")]
            RoundSF { .. } => mapper.map_dtype(|dt| match dt {
                #[cfg(feature = "dtype-decimal")]
                DataType::Decimal(p, s) => DataType::Decimal((p + 1).min(DEC128_MAX_PREC), *s),
                dt => dt.clone(),
            }),
            #[cfg(feature = "round_series")]
            Floor | Ceil => mapper.map_dtype(|dt| match dt {
                #[cfg(feature = "dtype-decimal")]
                DataType::Decimal(p, s) if *s > 0 => {
                    DataType::Decimal((p + 1).min(DEC128_MAX_PREC), *s)
                },
                dt => dt.clone(),
            }),
            #[cfg(feature = "round_series")]
            Truncate { .. } => mapper.with_same_dtype(),
            #[cfg(feature = "dtype-decimal")]
            DecimalArith { op, scale } => mapper
                .ensure_satisfies(
                    |_, dtype| dtype.is_decimal() || dtype.is_integer(),
                    op.name(),
                )?
                .with_dtype(DataType::Decimal(DEC128_MAX_PREC, *scale)),
            // With a decimal, the remainder keeps the larger scale (integers are scale 0)
            // and the quotient is an integer; other numerics keep their supertype.
            TruncArith(op) => {
                let args = mapper.args();
                match (args[0].dtype(), args[1].dtype()) {
                    #[cfg(feature = "dtype-decimal")]
                    (l, r) if l.is_decimal() || r.is_decimal() => {
                        let scale = |dt: &DataType| match dt {
                            DataType::Decimal(_, s) => *s,
                            _ => 0,
                        };
                        let scale = match op {
                            TruncArithOp::Rem => scale(l).max(scale(r)),
                            TruncArithOp::IntDiv => 0,
                        };
                        mapper.with_dtype(DataType::Decimal(DEC128_MAX_PREC, scale))
                    },
                    _ => mapper.map_to_supertype(),
                }
            },
            #[cfg(feature = "fused")]
            Fused(_) => mapper.map_to_supertype(),
            ConcatExpr { .. } => mapper.map_to_supertype(),
            #[cfg(feature = "cov")]
            Correlation { .. } => mapper.map_to_float_dtype(),
            #[cfg(feature = "peaks")]
            PeakMin | PeakMax => mapper.with_dtype(DataType::Boolean),
            #[cfg(feature = "cutqcut")]
            Cut {
                breaks,
                labels,
                left_closed,
                include_breaks,
            } => {
                let cut_labels: Vec<PlSmallStr> = if let Some(l) = labels {
                    polars_ensure!(
                        l.len() == breaks.len() + 1,
                        ShapeMismatch: "expected {} labels (len(breaks) + 1), got {}",
                        breaks.len() + 1, l.len()
                    );
                    l.clone()
                } else {
                    use polars_core::utils::cut::compute_cut_labels;

                    compute_cut_labels(breaks, *left_closed)?
                };
                let enum_dtype = DataType::from_frozen_categories(FrozenCategories::new(
                    cut_labels.iter().map(|s| s.as_str()),
                )?);
                if *include_breaks {
                    let struct_dt = DataType::Struct(vec![
                        Field::new(PlSmallStr::from_static("breakpoint"), DataType::Float64),
                        Field::new(PlSmallStr::from_static("category"), enum_dtype),
                    ]);
                    mapper.with_dtype(struct_dt)
                } else {
                    mapper.with_dtype(enum_dtype)
                }
            },
            #[cfg(feature = "repeat_by")]
            RepeatBy => mapper.map_dtype(|dt| DataType::List(dt.clone().into())),
            #[cfg(feature = "dtype-array")]
            Reshape(dims) => mapper.try_map_dtype(|dt: &DataType| {
                let mut wrapped_dtype = dt.leaf_dtype().clone();
                for dim in dims[1..].iter().rev() {
                    let Some(array_size) = dim.get() else {
                        polars_bail!(InvalidOperation: "can only infer the first dimension");
                    };
                    wrapped_dtype = DataType::Array(Box::new(wrapped_dtype), array_size as usize);
                }
                Ok(wrapped_dtype)
            }),
            #[cfg(feature = "cutqcut")]
            QCut {
                include_breaks: false,
                ..
            } => mapper.with_dtype(DataType::from_categories(Categories::global())),
            #[cfg(feature = "cutqcut")]
            QCut {
                include_breaks: true,
                ..
            } => {
                let struct_dt = DataType::Struct(vec![
                    Field::new(PlSmallStr::from_static("breakpoint"), DataType::Float64),
                    Field::new(
                        PlSmallStr::from_static("category"),
                        DataType::from_categories(Categories::global()),
                    ),
                ]);
                mapper.with_dtype(struct_dt)
            },
            #[cfg(feature = "cutqcut")]
            Bin(options) => {
                let n_bins = options.method.n_bins();
                let bin_dtype = match &options.labels {
                    None => DataType::UInt32,
                    Some(labels) => {
                        polars_ensure!(
                            labels.len() == n_bins,
                            ShapeMismatch: "`{}` produces {} bins but got {} labels",
                            options.method.name(), n_bins, labels.len()
                        );
                        DataType::from_frozen_categories(FrozenCategories::new(
                            labels.iter().map(|s| s.as_str()),
                        )?)
                    },
                };
                if !options.include_intervals {
                    return mapper.with_dtype(bin_dtype);
                }
                // The input has been converted to the correct type during DSL -> IR conversion.
                let bound = mapper.args()[0].dtype().clone();
                mapper.with_dtype(DataType::Struct(vec![
                    Field::new(PlSmallStr::from_static("bin"), bin_dtype),
                    Field::new(PlSmallStr::from_static("left"), bound.clone()),
                    Field::new(PlSmallStr::from_static("right"), bound),
                ]))
            },
            #[cfg(feature = "rle")]
            RLE => mapper.map_dtype(|dt| {
                DataType::Struct(vec![
                    Field::new(PlSmallStr::from_static("len"), IDX_DTYPE),
                    Field::new(PlSmallStr::from_static("value"), dt.clone()),
                ])
            }),
            #[cfg(feature = "rle")]
            RLEID => mapper.with_dtype(IDX_DTYPE),
            ToPhysical => mapper.to_physical_type(),
            #[cfg(feature = "random")]
            Random { .. } => mapper.with_same_dtype(),
            SetSortedFlag(_) => mapper.with_same_dtype(),
            #[cfg(feature = "ffi_plugin")]
            FfiPlugin {
                flags: _,
                is_deterministic: _,
                lib,
                symbol,
                kwargs,
            } => unsafe { plugin::plugin_field(fields, lib, symbol.as_ref(), kwargs) },

            FoldHorizontal { return_dtype, .. } => match return_dtype {
                None => mapper.with_same_dtype(),
                Some(dtype) => mapper.with_dtype(dtype.clone()),
            },
            ReduceHorizontal { return_dtype, .. } => match return_dtype {
                None => mapper.map_to_supertype(),
                Some(dtype) => mapper.with_dtype(dtype.clone()),
            },
            #[cfg(feature = "dtype-struct")]
            CumReduceHorizontal { return_dtype, .. } => match return_dtype {
                None => mapper.with_dtype(DataType::Struct(fields.to_vec())),
                Some(dtype) => mapper.with_dtype(DataType::Struct(
                    fields
                        .iter()
                        .map(|f| Field::new(f.name().clone(), dtype.clone()))
                        .collect(),
                )),
            },
            #[cfg(feature = "dtype-struct")]
            CumFoldHorizontal {
                return_dtype,
                include_init,
                ..
            } => match return_dtype {
                None => mapper.with_dtype(DataType::Struct(
                    fields
                        .iter()
                        .skip(usize::from(!include_init))
                        .map(|f| Field::new(f.name().clone(), fields[0].dtype().clone()))
                        .collect(),
                )),
                Some(dtype) => mapper.with_dtype(DataType::Struct(
                    fields
                        .iter()
                        .skip(usize::from(!include_init))
                        .map(|f| Field::new(f.name().clone(), dtype.clone()))
                        .collect(),
                )),
            },

            MaxHorizontal => mapper.map_to_supertype(),
            MinHorizontal => mapper.map_to_supertype(),
            SumHorizontal { .. } => mapper.map_to_supertype().map(|mut f| {
                if f.dtype == DataType::Boolean {
                    f.dtype = IDX_DTYPE;
                }
                f
            }),
            MeanHorizontal { .. } => mapper.map_to_supertype().map(|mut f| {
                match f.dtype {
                    #[cfg(feature = "dtype-f16")]
                    DataType::Float16 => {},
                    DataType::Float32 => {},
                    _ => {
                        f.dtype = DataType::Float64;
                    },
                }
                f
            }),
            #[cfg(feature = "ewma")]
            EwmMean { .. } => mapper.map_numeric_to_float_dtype(true),
            #[cfg(feature = "ewma_by")]
            EwmMeanBy { .. } => mapper.map_numeric_to_float_dtype(true),
            #[cfg(feature = "ewma")]
            EwmSum { .. } => mapper.map_numeric_to_float_dtype(true),
            #[cfg(feature = "ewma_by")]
            EwmSumBy { .. } => mapper.map_numeric_to_float_dtype(true),
            #[cfg(feature = "ewma")]
            EwmStd { .. } => mapper.ewm_var_dtype("ewm_std", true),
            #[cfg(feature = "ewma")]
            EwmVar { .. } => mapper.ewm_var_dtype("ewm_var", true),
            #[cfg(feature = "replace")]
            Replace => mapper.with_same_dtype(),
            #[cfg(feature = "replace")]
            ReplaceStrict { return_dtype } => mapper.replace_dtype(return_dtype.clone()),
            FillNullWithStrategy(_) => mapper.with_same_dtype(),
            GatherEvery { .. } => mapper.with_same_dtype(),
            #[cfg(feature = "reinterpret")]
            Reinterpret(dtype) => mapper.with_dtype(dtype.clone()),
            ExtendConstant => mapper.with_same_dtype(),

            RowEncode(..) => mapper.try_map_field(|_| {
                Ok(Field::new(
                    PlSmallStr::from_static("row_encoded"),
                    DataType::BinaryOffset,
                ))
            }),
            #[cfg(feature = "dtype-struct")]
            RowDecode(fields, _) => mapper.with_dtype(DataType::Struct(fields.to_vec())),
            DynamicPred { .. } | DynamicSkipBatch { .. } => mapper.with_dtype(DataType::Boolean),
        }
    }
```


#### 📄 檔案: `crates/polars-plan/src/plans/conversion/type_coercion/mod.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:196, E:241, A:0) ➔ After(N:196, E:241, A:0)
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

### 🔹 Commit #16: `245d1de3`
- **完整 Hash**: `245d1de3bae2327ec1b0a5a0bfb164102a79c6fa`
- **說明 (Ground Truth)**: fix: Correct schema supertype for mixed bool <> unknown float ops (#29947)
- **變更檔案數**: 1

#### 📄 檔案: `crates/polars-core/src/utils/supertype.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:149, E:172, A:0) ➔ After(N:149, E:172, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
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

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `get_supertype_with_options()`
- **變更前簽章 (Before)**: `fn get_supertype_with_options(
    l: &DataType,
    r: &DataType,
    options: SuperTypeOptions,
)` (L149~L577)
- **變更後簽章 (After)**: `fn get_supertype_with_options(
    l: &DataType,
    r: &DataType,
    options: SuperTypeOptions,
)` (L149~L578)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn get_supertype_with_options(
    l: &DataType,
    r: &DataType,
    options: SuperTypeOptions,
) -> Option<DataType> {
    fn inner(l: &DataType, r: &DataType, options: SuperTypeOptions) -> Option<DataType> {
        use DataType::*;
        if l == r {
            return Some(l.clone());
        }
        match (l, r) {
            #[cfg(feature = "dtype-i8")]
            (Int8, Boolean) => Some(Int8),
            //(Int8, Int8) => Some(Int8),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-i16"))]
            (Int8, Int16) => Some(Int16),
            #[cfg(feature = "dtype-i8")]
            (Int8, Int32) => Some(Int32),
            #[cfg(feature = "dtype-i8")]
            (Int8, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-i16"))]
            (Int8, UInt8) => Some(Int16),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-u16"))]
            (Int8, UInt16) => Some(Int32),
            #[cfg(feature = "dtype-i8")]
            (Int8, UInt32) => Some(Int64),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-i128"))]
            (Int8, UInt64) => Some(Int128),
            #[cfg(all(feature = "dtype-i8", not(feature = "dtype-i128")))]
            (Int8, UInt64) => Some(Float64), // Follow numpy
            #[cfg(all(feature = "dtype-i8", feature = "dtype-f16"))]
            (Int8, Float16) => Some(Float16),
            #[cfg(feature = "dtype-i8")]
            (Int8, Float32) => Some(Float32),
            #[cfg(feature = "dtype-i8")]
            (Int8, Float64) => Some(Float64),

            #[cfg(feature = "dtype-i16")]
            (Int16, Boolean) => Some(Int16),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-i8"))]
            (Int16, Int8) => Some(Int16),
            //(Int16, Int16) => Some(Int16),
            #[cfg(feature = "dtype-i16")]
            (Int16, Int32) => Some(Int32),
            #[cfg(feature = "dtype-i16")]
            (Int16, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-u8"))]
            (Int16, UInt8) => Some(Int16),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-u16"))]
            (Int16, UInt16) => Some(Int32),
            #[cfg(feature = "dtype-i16")]
            (Int16, UInt32) => Some(Int64),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-i128"))]
            (Int16, UInt64) => Some(Int128),
            #[cfg(all(feature = "dtype-i16", not(feature = "dtype-i128")))]
            (Int16, UInt64) => Some(Float64), // Follow numpy
            #[cfg(all(feature = "dtype-i16", feature = "dtype-f16"))]
            (Int16, Float16) => Some(Float32),
            #[cfg(feature = "dtype-i16")]
            (Int16, Float32) => Some(Float32),
            #[cfg(feature = "dtype-i16")]
            (Int16, Float64) => Some(Float64),

            (Int32, Boolean) => Some(Int32),
            #[cfg(feature = "dtype-i8")]
            (Int32, Int8) => Some(Int32),
            #[cfg(feature = "dtype-i16")]
            (Int32, Int16) => Some(Int32),
            //(Int32, Int32) => Some(Int32),
            (Int32, Int64) => Some(Int64),
            #[cfg(feature = "dtype-u8")]
            (Int32, UInt8) => Some(Int32),
            #[cfg(feature = "dtype-u16")]
            (Int32, UInt16) => Some(Int32),
            (Int32, UInt32) => Some(Int64),
            #[cfg(feature = "dtype-i128")]
            (Int32, UInt64) => Some(Int128),
            #[cfg(not(feature = "dtype-i128"))]
            (Int32, UInt64) => Some(Float64), // Follow numpy
            #[cfg(feature = "dtype-f16")]
            (Int32, Float16) => Some(Float64),
            (Int32, Float32) => Some(Float64), // Follow numpy
            (Int32, Float64) => Some(Float64),

            (Int64, Boolean) => Some(Int64),
            #[cfg(feature = "dtype-i8")]
            (Int64, Int8) => Some(Int64),
            #[cfg(feature = "dtype-i16")]
            (Int64, Int16) => Some(Int64),
            (Int64, Int32) => Some(Int64),
            //(Int64, Int64) => Some(Int64),
            #[cfg(feature = "dtype-u8")]
            (Int64, UInt8) => Some(Int64),
            #[cfg(feature = "dtype-u16")]
            (Int64, UInt16) => Some(Int64),
            (Int64, UInt32) => Some(Int64),
            #[cfg(feature = "dtype-i128")]
            (Int64, UInt64) => Some(Int128),
            #[cfg(not(feature = "dtype-i128"))]
            (Int64, UInt64) => Some(Float64), // Follow numpy
            #[cfg(feature = "dtype-f16")]
            (Int64, Float16) => Some(Float64), // Follow (Int64, Float32) case
            (Int64, Float32) => Some(Float64), // Follow numpy
            (Int64, Float64) => Some(Float64),

            #[cfg(feature = "dtype-i128")]
            (Int128, a) if a.is_integer() | a.is_bool() => Some(Int128),
            #[cfg(feature = "dtype-i128")]
            (Int128, a) if a.is_float() => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (UInt8, UInt32) => Some(UInt32),
            #[cfg(feature = "dtype-u8")]
            (UInt8, UInt64) => Some(UInt64),

            #[cfg(all(feature = "dtype-u16", feature = "dtype-u8"))]
            (UInt16, UInt8) => Some(UInt16),
            #[cfg(feature = "dtype-u16")]
            (UInt16, UInt32) => Some(UInt32),
            #[cfg(feature = "dtype-u16")]
            (UInt16, UInt64) => Some(UInt64),

            (UInt32, UInt64) => Some(UInt64),

            #[cfg(feature = "dtype-u128")]
            (UInt128, a) if a.is_unsigned_integer() || a.is_bool() => Some(UInt128),
            #[cfg(feature = "dtype-u128")]
            (UInt128, a) if a.is_signed_integer() => Some(Int128),
            #[cfg(feature = "dtype-u128")]
            (UInt128, a) if a.is_float() => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (Boolean, UInt8) => Some(UInt8),
            #[cfg(feature = "dtype-u16")]
            (Boolean, UInt16) => Some(UInt16),
            (Boolean, UInt32) => Some(UInt32),
            (Boolean, UInt64) => Some(UInt64),

            #[cfg(all(feature = "dtype-f16", feature = "dtype-u8"))]
            (Float16, UInt8) => Some(Float16),
            #[cfg(all(feature = "dtype-f16", feature = "dtype-u16"))]
            (Float16, UInt16) => Some(Float32),
            #[cfg(feature = "dtype-f16")]
            (Float16, UInt32) => Some(Float64),
            #[cfg(feature = "dtype-f16")]
            (Float16, UInt64) => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (Float32, UInt8) => Some(Float32),
            #[cfg(feature = "dtype-u16")]
            (Float32, UInt16) => Some(Float32),
            (Float32, UInt32) => Some(Float64),
            (Float32, UInt64) => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (Float64, UInt8) => Some(Float64),
            #[cfg(feature = "dtype-u16")]
            (Float64, UInt16) => Some(Float64),
            (Float64, UInt32) => Some(Float64),
            (Float64, UInt64) => Some(Float64),

            #[cfg(feature = "dtype-f16")]
            (Float16, Float32) => Some(Float32),
            #[cfg(feature = "dtype-f16")]
            (Float16, Float64) => Some(Float64),
            (Float32, Float64) => Some(Float64),
            #[cfg(feature = "dtype-f16")]
            (Float32, Float16) => Some(Float32),
            #[cfg(feature = "dtype-f16")]
            (Float64, Float16) => Some(Float64),
            (Float64, Float32) => Some(Float64),

            // Time related dtypes
            #[cfg(feature = "dtype-date")]
            (Date, UInt32) => Some(Int64),
            #[cfg(feature = "dtype-date")]
            (Date, UInt64) => Some(Int64),
            #[cfg(feature = "dtype-date")]
            (Date, Int32) => Some(Int32),
            #[cfg(feature = "dtype-date")]
            (Date, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-date", feature = "dtype-f16"))]
            (Date, Float16) => Some(Float32),
            #[cfg(feature = "dtype-date")]
            (Date, Float32) => Some(Float32),
            #[cfg(feature = "dtype-date")]
            (Date, Float64) => Some(Float64),
            #[cfg(all(feature = "dtype-date", feature = "dtype-datetime"))]
            (Date, Datetime(tu, tz)) => Some(Datetime(*tu, tz.clone())),

            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), UInt32) => Some(Int64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), UInt64) => Some(Int64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Int32) => Some(Int64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-datetime", feature = "dtype-f16"))]
            (Datetime(_, _), Float16) => Some(Float64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Float32) => Some(Float64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Float64) => Some(Float64),
            #[cfg(all(feature = "dtype-datetime", feature = "dtype-date"))]
            (Datetime(tu, tz), Date) => Some(Datetime(*tu, tz.clone())),

            #[cfg(feature = "dtype-f16")]
            (Boolean, Float16) => Some(Float16),
            (Boolean, Float32) => Some(Float32),
            (Boolean, Float64) => Some(Float64),

            #[cfg(feature = "dtype-duration")]
            (Duration(_), UInt32) => Some(Int64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), UInt64) => Some(Int64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Int32) => Some(Int64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-duration", feature = "dtype-f16"))]
            (Duration(_), Float16) => Some(Float64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Float32) => Some(Float64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Float64) => Some(Float64),

            #[cfg(feature = "dtype-time")]
            (Time, Int32) => Some(Int64),
            #[cfg(feature = "dtype-time")]
            (Time, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-time", feature = "dtype-f16"))]
            (Time, Float16) => Some(Float64),
            #[cfg(feature = "dtype-time")]
            (Time, Float32) => Some(Float64),
            #[cfg(feature = "dtype-time")]
            (Time, Float64) => Some(Float64),

            // Every known type can be cast to a string except binary
            (dt, String) if !matches!(dt, Unknown(UnknownKind::Any)) && dt != &Binary && options.allow_primitive_to_string() || !dt.to_physical().is_primitive() => Some(String),
            (String, Binary) => Some(Binary),
            (dt, Null) => Some(dt.clone()),

            #[cfg(all(feature = "dtype-duration", feature = "dtype-datetime"))]
            (Duration(lu), Datetime(ru, Some(tz))) | (Datetime(lu, Some(tz)), Duration(ru)) => {
                if tz.is_empty() {
                    Some(Datetime(get_time_units(lu, ru), None))
                } else {
                    Some(Datetime(get_time_units(lu, ru), Some(tz.clone())))
                }
            }
            #[cfg(all(feature = "dtype-duration", feature = "dtype-datetime"))]
            (Duration(lu), Datetime(ru, None)) | (Datetime(lu, None), Duration(ru)) => {
                Some(Datetime(get_time_units(lu, ru), None))
            }
            #[cfg(all(feature = "dtype-duration", feature = "dtype-date"))]
            (Duration(_), Date) | (Date, Duration(_)) => Some(Date),
            #[cfg(feature = "dtype-duration")]
            (Duration(lu), Duration(ru)) => Some(Duration(get_time_units(lu, ru))),

            // both None or both Some("<tz>") timezones
            // we cast from more precision to higher precision as that always fits with occasional loss of precision
            #[cfg(feature = "dtype-datetime")]
            (Datetime(tu_l, tz_l), Datetime(tu_r, tz_r)) if
                // both are none
                (tz_l.is_none() && tz_r.is_none())
                // both have the same time zone
                || (tz_l.is_some() && (tz_l == tz_r)) => {
                let tu = get_time_units(tu_l, tu_r);
                Some(Datetime(tu, tz_r.clone()))
            }
            (List(inner_left), List(inner_right)) => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-array")]
            (List(inner_left), Array(inner_right, _)) | (Array(inner_left, _), List(inner_right)) => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-array")]
            (Array(inner_left, width_left), Array(inner_right, width_right)) if *width_left == *width_right => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(Array(Box::new(st), *width_left))
            }
            #[cfg(feature = "dtype-map")]
            (Map(key_left, value_left), Map(key_right, value_right)) => {
                // We forbid casting the key type, as it might collapse distinct keys into one.
                if key_left != key_right
                    && !key_left.is_nested_null()
                    && !key_right.is_nested_null()
                {
                    return None;
                }
                let key = get_supertype(key_left, key_right)?;
                let value = get_supertype(value_left, value_right)?;
                Some(Map(Box::new(key), Box::new(value)))
            }
            (List(inner), other) | (other, List(inner)) if options.allow_implode_list() => {
                let st = get_supertype(inner, other)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-array")]
            (Array(inner_left, _), Array(inner_right, _)) => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-struct")]
            (Struct(inner), right @ Unknown(UnknownKind::Float | UnknownKind::Int(_))) => {
                match inner.first() {
                    Some(inner) => get_supertype(&inner.dtype, right),
                    None => None
                }
            },
            #[cfg(feature = "dtype-struct")]
            (Struct(fields_a), Struct(fields_b)) => {
                super_type_structs(fields_a, fields_b)
            }
            #[cfg(feature = "dtype-struct")]
            (Struct(fields_a), rhs) if rhs.is_primitive_numeric() => {
                let mut new_fields = Vec::with_capacity(fields_a.len());
                for a in fields_a {
                    let st = get_supertype(&a.dtype, rhs)?;
                    new_fields.push(Field::new(a.name.clone(), st))
                }
                Some(Struct(new_fields))
            }
            #[cfg(feature = "dtype-decimal")]
            (Decimal(p1, s1), Decimal(p2, s2)) => {
                // Keep all integer digits and the larger scale. Beyond precision 38 values
                // that don't fit raise when cast.
                let s = (*s1).max(*s2);
                let p = ((p1 - s1).max(p2 - s2) + s).min(DEC128_MAX_PREC);
                Some(Decimal(p, s))
            },
            #[cfg(all(feature = "dtype-decimal", feature = "dtype-f16"))]
            (Decimal(_, _), Float16) => Some(Float64),
            #[cfg(feature = "dtype-decimal")]
            (Decimal(_, _), Float32 | Float64 | Unknown(UnknownKind::Float)) => Some(Float64),
            #[cfg(feature = "dtype-decimal")]
            (Decimal(prec, scale), dt) if dt.is_signed_integer() || dt.is_unsigned_integer() => {
                let fits = |v| { i128_to_dec128(v, *prec, *scale).is_some() };
                let fits_orig_prec_scale = match dt {
                    UInt8 => fits(u8::MAX as i128),
                    UInt16 => fits(u16::MAX as i128),
                    UInt32 => fits(u32::MAX as i128),
                    UInt64 => fits(u64::MAX as i128),
                    UInt128 => false,
                    Int8 => fits(i8::MAX as i128),
                    Int16 => fits(i16::MAX as i128),
                    Int32 => fits(i32::MAX as i128),
                    Int64 => fits(i64::MAX as i128),
                    Int128 => false,
                    _ => unreachable!(),
                };
                if fits_orig_prec_scale {
                    Some(Decimal(*prec, *scale))
                } else {
                    Some(Decimal(DEC128_MAX_PREC, *scale))
                }
            }
            (dt, Unknown(kind)) => {
                match kind {
                    UnknownKind::Float | UnknownKind::Int(_) if  dt.is_string() => {
                        if options.allow_primitive_to_string() {
                            Some(dt.clone())
                        } else {
                            None
                        }
                    },
                    // Materialize float to float
                    UnknownKind::Float | UnknownKind::Int(_) if dt.is_float() => Some(dt.clone()),
                    UnknownKind::Float if dt.is_integer() => {
                        if dt.is_known() {
                            Some(Float64)
                        } else {
                            Some(Unknown(UnknownKind::Float))
                        }
                    },
                    // Materialize str
                    UnknownKind::Str if dt.is_string() | dt.is_enum() => Some(dt.clone()),
                    // Materialize str
                    #[cfg(feature = "dtype-categorical")]
                    UnknownKind::Str if dt.is_categorical() => Some(dt.clone()),
                    // Keep unknown
                    dynam if dt.is_null() => Some(Unknown(*dynam)),
                    // Find integers sizes
                    UnknownKind::Int(v) if dt.is_primitive_numeric() => {
                        // Both dyn int
                        if let Unknown(UnknownKind::Int(v_other)) = dt {
                            // Take the maximum value to ensure we bubble up the required minimal size.
                            Some(Unknown(UnknownKind::Int(std::cmp::max(*v, *v_other))))
                        }
                        // dyn int vs number
                        else {
                            let smallest_fitting_dtype = if dt.is_unsigned_integer() && !v.is_negative() {
                                materialize_dyn_int_pos(*v).dtype()
                            } else {
                                materialize_smallest_dyn_int(*v).dtype()
                            };
                            match dt {
                                UInt64 if smallest_fitting_dtype.is_signed_integer() => {
                                    // Ensure we don't cast to float when dealing with dynamic literals
                                    Some(Int64)
                                },
                                _ => {
                                    get_supertype(dt, &smallest_fitting_dtype)
                                }
                            }
                        }
                    }
                    UnknownKind::Int(v) if dt.is_bool() => {
                        let int_dtype = materialize_dyn_int(*v).dtype();
                        get_supertype(dt, &int_dtype)
                    },
                    #[cfg(feature = "dtype-decimal")]
                    UnknownKind::Int(_) if dt.is_decimal() => {
                        let DataType::Decimal(_prec, scale) = dt else { unreachable!() };
                        Some(DataType::Decimal(DEC128_MAX_PREC, *scale))
                    }
                    _ => Some(Unknown(UnknownKind::Any))
                }
            },
            _ => None,
        }
    }

    inner(l, r, options).or_else(|| inner(r, l, options))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn get_supertype_with_options(
    l: &DataType,
    r: &DataType,
    options: SuperTypeOptions,
) -> Option<DataType> {
    fn inner(l: &DataType, r: &DataType, options: SuperTypeOptions) -> Option<DataType> {
        use DataType::*;
        if l == r {
            return Some(l.clone());
        }
        match (l, r) {
            #[cfg(feature = "dtype-i8")]
            (Int8, Boolean) => Some(Int8),
            //(Int8, Int8) => Some(Int8),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-i16"))]
            (Int8, Int16) => Some(Int16),
            #[cfg(feature = "dtype-i8")]
            (Int8, Int32) => Some(Int32),
            #[cfg(feature = "dtype-i8")]
            (Int8, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-i16"))]
            (Int8, UInt8) => Some(Int16),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-u16"))]
            (Int8, UInt16) => Some(Int32),
            #[cfg(feature = "dtype-i8")]
            (Int8, UInt32) => Some(Int64),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-i128"))]
            (Int8, UInt64) => Some(Int128),
            #[cfg(all(feature = "dtype-i8", not(feature = "dtype-i128")))]
            (Int8, UInt64) => Some(Float64), // Follow numpy
            #[cfg(all(feature = "dtype-i8", feature = "dtype-f16"))]
            (Int8, Float16) => Some(Float16),
            #[cfg(feature = "dtype-i8")]
            (Int8, Float32) => Some(Float32),
            #[cfg(feature = "dtype-i8")]
            (Int8, Float64) => Some(Float64),

            #[cfg(feature = "dtype-i16")]
            (Int16, Boolean) => Some(Int16),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-i8"))]
            (Int16, Int8) => Some(Int16),
            //(Int16, Int16) => Some(Int16),
            #[cfg(feature = "dtype-i16")]
            (Int16, Int32) => Some(Int32),
            #[cfg(feature = "dtype-i16")]
            (Int16, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-u8"))]
            (Int16, UInt8) => Some(Int16),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-u16"))]
            (Int16, UInt16) => Some(Int32),
            #[cfg(feature = "dtype-i16")]
            (Int16, UInt32) => Some(Int64),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-i128"))]
            (Int16, UInt64) => Some(Int128),
            #[cfg(all(feature = "dtype-i16", not(feature = "dtype-i128")))]
            (Int16, UInt64) => Some(Float64), // Follow numpy
            #[cfg(all(feature = "dtype-i16", feature = "dtype-f16"))]
            (Int16, Float16) => Some(Float32),
            #[cfg(feature = "dtype-i16")]
            (Int16, Float32) => Some(Float32),
            #[cfg(feature = "dtype-i16")]
            (Int16, Float64) => Some(Float64),

            (Int32, Boolean) => Some(Int32),
            #[cfg(feature = "dtype-i8")]
            (Int32, Int8) => Some(Int32),
            #[cfg(feature = "dtype-i16")]
            (Int32, Int16) => Some(Int32),
            //(Int32, Int32) => Some(Int32),
            (Int32, Int64) => Some(Int64),
            #[cfg(feature = "dtype-u8")]
            (Int32, UInt8) => Some(Int32),
            #[cfg(feature = "dtype-u16")]
            (Int32, UInt16) => Some(Int32),
            (Int32, UInt32) => Some(Int64),
            #[cfg(feature = "dtype-i128")]
            (Int32, UInt64) => Some(Int128),
            #[cfg(not(feature = "dtype-i128"))]
            (Int32, UInt64) => Some(Float64), // Follow numpy
            #[cfg(feature = "dtype-f16")]
            (Int32, Float16) => Some(Float64),
            (Int32, Float32) => Some(Float64), // Follow numpy
            (Int32, Float64) => Some(Float64),

            (Int64, Boolean) => Some(Int64),
            #[cfg(feature = "dtype-i8")]
            (Int64, Int8) => Some(Int64),
            #[cfg(feature = "dtype-i16")]
            (Int64, Int16) => Some(Int64),
            (Int64, Int32) => Some(Int64),
            //(Int64, Int64) => Some(Int64),
            #[cfg(feature = "dtype-u8")]
            (Int64, UInt8) => Some(Int64),
            #[cfg(feature = "dtype-u16")]
            (Int64, UInt16) => Some(Int64),
            (Int64, UInt32) => Some(Int64),
            #[cfg(feature = "dtype-i128")]
            (Int64, UInt64) => Some(Int128),
            #[cfg(not(feature = "dtype-i128"))]
            (Int64, UInt64) => Some(Float64), // Follow numpy
            #[cfg(feature = "dtype-f16")]
            (Int64, Float16) => Some(Float64), // Follow (Int64, Float32) case
            (Int64, Float32) => Some(Float64), // Follow numpy
            (Int64, Float64) => Some(Float64),

            #[cfg(feature = "dtype-i128")]
            (Int128, a) if a.is_integer() | a.is_bool() => Some(Int128),
            #[cfg(feature = "dtype-i128")]
            (Int128, a) if a.is_float() => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (UInt8, UInt32) => Some(UInt32),
            #[cfg(feature = "dtype-u8")]
            (UInt8, UInt64) => Some(UInt64),

            #[cfg(all(feature = "dtype-u16", feature = "dtype-u8"))]
            (UInt16, UInt8) => Some(UInt16),
            #[cfg(feature = "dtype-u16")]
            (UInt16, UInt32) => Some(UInt32),
            #[cfg(feature = "dtype-u16")]
            (UInt16, UInt64) => Some(UInt64),

            (UInt32, UInt64) => Some(UInt64),

            #[cfg(feature = "dtype-u128")]
            (UInt128, a) if a.is_unsigned_integer() || a.is_bool() => Some(UInt128),
            #[cfg(feature = "dtype-u128")]
            (UInt128, a) if a.is_signed_integer() => Some(Int128),
            #[cfg(feature = "dtype-u128")]
            (UInt128, a) if a.is_float() => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (Boolean, UInt8) => Some(UInt8),
            #[cfg(feature = "dtype-u16")]
            (Boolean, UInt16) => Some(UInt16),
            (Boolean, UInt32) => Some(UInt32),
            (Boolean, UInt64) => Some(UInt64),

            #[cfg(all(feature = "dtype-f16", feature = "dtype-u8"))]
            (Float16, UInt8) => Some(Float16),
            #[cfg(all(feature = "dtype-f16", feature = "dtype-u16"))]
            (Float16, UInt16) => Some(Float32),
            #[cfg(feature = "dtype-f16")]
            (Float16, UInt32) => Some(Float64),
            #[cfg(feature = "dtype-f16")]
            (Float16, UInt64) => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (Float32, UInt8) => Some(Float32),
            #[cfg(feature = "dtype-u16")]
            (Float32, UInt16) => Some(Float32),
            (Float32, UInt32) => Some(Float64),
            (Float32, UInt64) => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (Float64, UInt8) => Some(Float64),
            #[cfg(feature = "dtype-u16")]
            (Float64, UInt16) => Some(Float64),
            (Float64, UInt32) => Some(Float64),
            (Float64, UInt64) => Some(Float64),

            #[cfg(feature = "dtype-f16")]
            (Float16, Float32) => Some(Float32),
            #[cfg(feature = "dtype-f16")]
            (Float16, Float64) => Some(Float64),
            (Float32, Float64) => Some(Float64),
            #[cfg(feature = "dtype-f16")]
            (Float32, Float16) => Some(Float32),
            #[cfg(feature = "dtype-f16")]
            (Float64, Float16) => Some(Float64),
            (Float64, Float32) => Some(Float64),

            // Time related dtypes
            #[cfg(feature = "dtype-date")]
            (Date, UInt32) => Some(Int64),
            #[cfg(feature = "dtype-date")]
            (Date, UInt64) => Some(Int64),
            #[cfg(feature = "dtype-date")]
            (Date, Int32) => Some(Int32),
            #[cfg(feature = "dtype-date")]
            (Date, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-date", feature = "dtype-f16"))]
            (Date, Float16) => Some(Float32),
            #[cfg(feature = "dtype-date")]
            (Date, Float32) => Some(Float32),
            #[cfg(feature = "dtype-date")]
            (Date, Float64) => Some(Float64),
            #[cfg(all(feature = "dtype-date", feature = "dtype-datetime"))]
            (Date, Datetime(tu, tz)) => Some(Datetime(*tu, tz.clone())),

            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), UInt32) => Some(Int64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), UInt64) => Some(Int64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Int32) => Some(Int64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-datetime", feature = "dtype-f16"))]
            (Datetime(_, _), Float16) => Some(Float64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Float32) => Some(Float64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Float64) => Some(Float64),
            #[cfg(all(feature = "dtype-datetime", feature = "dtype-date"))]
            (Datetime(tu, tz), Date) => Some(Datetime(*tu, tz.clone())),

            #[cfg(feature = "dtype-f16")]
            (Boolean, Float16) => Some(Float16),
            (Boolean, Float32) => Some(Float32),
            (Boolean, Float64) => Some(Float64),

            #[cfg(feature = "dtype-duration")]
            (Duration(_), UInt32) => Some(Int64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), UInt64) => Some(Int64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Int32) => Some(Int64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-duration", feature = "dtype-f16"))]
            (Duration(_), Float16) => Some(Float64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Float32) => Some(Float64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Float64) => Some(Float64),

            #[cfg(feature = "dtype-time")]
            (Time, Int32) => Some(Int64),
            #[cfg(feature = "dtype-time")]
            (Time, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-time", feature = "dtype-f16"))]
            (Time, Float16) => Some(Float64),
            #[cfg(feature = "dtype-time")]
            (Time, Float32) => Some(Float64),
            #[cfg(feature = "dtype-time")]
            (Time, Float64) => Some(Float64),

            // Every known type can be cast to a string except binary
            (dt, String) if !matches!(dt, Unknown(UnknownKind::Any)) && dt != &Binary && options.allow_primitive_to_string() || !dt.to_physical().is_primitive() => Some(String),
            (String, Binary) => Some(Binary),
            (dt, Null) => Some(dt.clone()),

            #[cfg(all(feature = "dtype-duration", feature = "dtype-datetime"))]
            (Duration(lu), Datetime(ru, Some(tz))) | (Datetime(lu, Some(tz)), Duration(ru)) => {
                if tz.is_empty() {
                    Some(Datetime(get_time_units(lu, ru), None))
                } else {
                    Some(Datetime(get_time_units(lu, ru), Some(tz.clone())))
                }
            }
            #[cfg(all(feature = "dtype-duration", feature = "dtype-datetime"))]
            (Duration(lu), Datetime(ru, None)) | (Datetime(lu, None), Duration(ru)) => {
                Some(Datetime(get_time_units(lu, ru), None))
            }
            #[cfg(all(feature = "dtype-duration", feature = "dtype-date"))]
            (Duration(_), Date) | (Date, Duration(_)) => Some(Date),
            #[cfg(feature = "dtype-duration")]
            (Duration(lu), Duration(ru)) => Some(Duration(get_time_units(lu, ru))),

            // both None or both Some("<tz>") timezones
            // we cast from more precision to higher precision as that always fits with occasional loss of precision
            #[cfg(feature = "dtype-datetime")]
            (Datetime(tu_l, tz_l), Datetime(tu_r, tz_r)) if
                // both are none
                (tz_l.is_none() && tz_r.is_none())
                // both have the same time zone
                || (tz_l.is_some() && (tz_l == tz_r)) => {
                let tu = get_time_units(tu_l, tu_r);
                Some(Datetime(tu, tz_r.clone()))
            }
            (List(inner_left), List(inner_right)) => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-array")]
            (List(inner_left), Array(inner_right, _)) | (Array(inner_left, _), List(inner_right)) => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-array")]
            (Array(inner_left, width_left), Array(inner_right, width_right)) if *width_left == *width_right => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(Array(Box::new(st), *width_left))
            }
            #[cfg(feature = "dtype-map")]
            (Map(key_left, value_left), Map(key_right, value_right)) => {
                // We forbid casting the key type, as it might collapse distinct keys into one.
                if key_left != key_right
                    && !key_left.is_nested_null()
                    && !key_right.is_nested_null()
                {
                    return None;
                }
                let key = get_supertype(key_left, key_right)?;
                let value = get_supertype(value_left, value_right)?;
                Some(Map(Box::new(key), Box::new(value)))
            }
            (List(inner), other) | (other, List(inner)) if options.allow_implode_list() => {
                let st = get_supertype(inner, other)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-array")]
            (Array(inner_left, _), Array(inner_right, _)) => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-struct")]
            (Struct(inner), right @ Unknown(UnknownKind::Float | UnknownKind::Int(_))) => {
                match inner.first() {
                    Some(inner) => get_supertype(&inner.dtype, right),
                    None => None
                }
            },
            #[cfg(feature = "dtype-struct")]
            (Struct(fields_a), Struct(fields_b)) => {
                super_type_structs(fields_a, fields_b)
            }
            #[cfg(feature = "dtype-struct")]
            (Struct(fields_a), rhs) if rhs.is_primitive_numeric() => {
                let mut new_fields = Vec::with_capacity(fields_a.len());
                for a in fields_a {
                    let st = get_supertype(&a.dtype, rhs)?;
                    new_fields.push(Field::new(a.name.clone(), st))
                }
                Some(Struct(new_fields))
            }
            #[cfg(feature = "dtype-decimal")]
            (Decimal(p1, s1), Decimal(p2, s2)) => {
                // Keep all integer digits and the larger scale. Beyond precision 38 values
                // that don't fit raise when cast.
                let s = (*s1).max(*s2);
                let p = ((p1 - s1).max(p2 - s2) + s).min(DEC128_MAX_PREC);
                Some(Decimal(p, s))
            },
            #[cfg(all(feature = "dtype-decimal", feature = "dtype-f16"))]
            (Decimal(_, _), Float16) => Some(Float64),
            #[cfg(feature = "dtype-decimal")]
            (Decimal(_, _), Float32 | Float64 | Unknown(UnknownKind::Float)) => Some(Float64),
            #[cfg(feature = "dtype-decimal")]
            (Decimal(prec, scale), dt) if dt.is_signed_integer() || dt.is_unsigned_integer() => {
                let fits = |v| { i128_to_dec128(v, *prec, *scale).is_some() };
                let fits_orig_prec_scale = match dt {
                    UInt8 => fits(u8::MAX as i128),
                    UInt16 => fits(u16::MAX as i128),
                    UInt32 => fits(u32::MAX as i128),
                    UInt64 => fits(u64::MAX as i128),
                    UInt128 => false,
                    Int8 => fits(i8::MAX as i128),
                    Int16 => fits(i16::MAX as i128),
                    Int32 => fits(i32::MAX as i128),
                    Int64 => fits(i64::MAX as i128),
                    Int128 => false,
                    _ => unreachable!(),
                };
                if fits_orig_prec_scale {
                    Some(Decimal(*prec, *scale))
                } else {
                    Some(Decimal(DEC128_MAX_PREC, *scale))
                }
            }
            (dt, Unknown(kind)) => {
                match kind {
                    UnknownKind::Float | UnknownKind::Int(_) if  dt.is_string() => {
                        if options.allow_primitive_to_string() {
                            Some(dt.clone())
                        } else {
                            None
                        }
                    },
                    // Materialize float to float
                    UnknownKind::Float | UnknownKind::Int(_) if dt.is_float() => Some(dt.clone()),
                    UnknownKind::Float if dt.is_bool() => Some(Unknown(UnknownKind::Float)),
                    UnknownKind::Float if dt.is_integer() => {
                        if dt.is_known() {
                            Some(Float64)
                        } else {
                            Some(Unknown(UnknownKind::Float))
                        }
                    },
                    // Materialize str
                    UnknownKind::Str if dt.is_string() | dt.is_enum() => Some(dt.clone()),
                    // Materialize str
                    #[cfg(feature = "dtype-categorical")]
                    UnknownKind::Str if dt.is_categorical() => Some(dt.clone()),
                    // Keep unknown
                    dynam if dt.is_null() => Some(Unknown(*dynam)),
                    // Find integers sizes
                    UnknownKind::Int(v) if dt.is_primitive_numeric() => {
                        // Both dyn int
                        if let Unknown(UnknownKind::Int(v_other)) = dt {
                            // Take the maximum value to ensure we bubble up the required minimal size.
                            Some(Unknown(UnknownKind::Int(std::cmp::max(*v, *v_other))))
                        }
                        // dyn int vs number
                        else {
                            let smallest_fitting_dtype = if dt.is_unsigned_integer() && !v.is_negative() {
                                materialize_dyn_int_pos(*v).dtype()
                            } else {
                                materialize_smallest_dyn_int(*v).dtype()
                            };
                            match dt {
                                UInt64 if smallest_fitting_dtype.is_signed_integer() => {
                                    // Ensure we don't cast to float when dealing with dynamic literals
                                    Some(Int64)
                                },
                                _ => {
                                    get_supertype(dt, &smallest_fitting_dtype)
                                }
                            }
                        }
                    }
                    UnknownKind::Int(v) if dt.is_bool() => {
                        let int_dtype = materialize_dyn_int(*v).dtype();
                        get_supertype(dt, &int_dtype)
                    },
                    #[cfg(feature = "dtype-decimal")]
                    UnknownKind::Int(_) if dt.is_decimal() => {
                        let DataType::Decimal(_prec, scale) = dt else { unreachable!() };
                        Some(DataType::Decimal(DEC128_MAX_PREC, *scale))
                    }
                    _ => Some(Unknown(UnknownKind::Any))
                }
            },
            _ => None,
        }
    }

    inner(l, r, options).or_else(|| inner(r, l, options))
}
```

### 🔹 函式: `inner()`
- **變更前簽章 (Before)**: `fn inner(l: &DataType, r: &DataType, options: SuperTypeOptions)` (L154~L574)
- **變更後簽章 (After)**: `fn inner(l: &DataType, r: &DataType, options: SuperTypeOptions)` (L154~L575)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn inner(l: &DataType, r: &DataType, options: SuperTypeOptions) -> Option<DataType> {
        use DataType::*;
        if l == r {
            return Some(l.clone());
        }
        match (l, r) {
            #[cfg(feature = "dtype-i8")]
            (Int8, Boolean) => Some(Int8),
            //(Int8, Int8) => Some(Int8),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-i16"))]
            (Int8, Int16) => Some(Int16),
            #[cfg(feature = "dtype-i8")]
            (Int8, Int32) => Some(Int32),
            #[cfg(feature = "dtype-i8")]
            (Int8, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-i16"))]
            (Int8, UInt8) => Some(Int16),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-u16"))]
            (Int8, UInt16) => Some(Int32),
            #[cfg(feature = "dtype-i8")]
            (Int8, UInt32) => Some(Int64),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-i128"))]
            (Int8, UInt64) => Some(Int128),
            #[cfg(all(feature = "dtype-i8", not(feature = "dtype-i128")))]
            (Int8, UInt64) => Some(Float64), // Follow numpy
            #[cfg(all(feature = "dtype-i8", feature = "dtype-f16"))]
            (Int8, Float16) => Some(Float16),
            #[cfg(feature = "dtype-i8")]
            (Int8, Float32) => Some(Float32),
            #[cfg(feature = "dtype-i8")]
            (Int8, Float64) => Some(Float64),

            #[cfg(feature = "dtype-i16")]
            (Int16, Boolean) => Some(Int16),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-i8"))]
            (Int16, Int8) => Some(Int16),
            //(Int16, Int16) => Some(Int16),
            #[cfg(feature = "dtype-i16")]
            (Int16, Int32) => Some(Int32),
            #[cfg(feature = "dtype-i16")]
            (Int16, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-u8"))]
            (Int16, UInt8) => Some(Int16),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-u16"))]
            (Int16, UInt16) => Some(Int32),
            #[cfg(feature = "dtype-i16")]
            (Int16, UInt32) => Some(Int64),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-i128"))]
            (Int16, UInt64) => Some(Int128),
            #[cfg(all(feature = "dtype-i16", not(feature = "dtype-i128")))]
            (Int16, UInt64) => Some(Float64), // Follow numpy
            #[cfg(all(feature = "dtype-i16", feature = "dtype-f16"))]
            (Int16, Float16) => Some(Float32),
            #[cfg(feature = "dtype-i16")]
            (Int16, Float32) => Some(Float32),
            #[cfg(feature = "dtype-i16")]
            (Int16, Float64) => Some(Float64),

            (Int32, Boolean) => Some(Int32),
            #[cfg(feature = "dtype-i8")]
            (Int32, Int8) => Some(Int32),
            #[cfg(feature = "dtype-i16")]
            (Int32, Int16) => Some(Int32),
            //(Int32, Int32) => Some(Int32),
            (Int32, Int64) => Some(Int64),
            #[cfg(feature = "dtype-u8")]
            (Int32, UInt8) => Some(Int32),
            #[cfg(feature = "dtype-u16")]
            (Int32, UInt16) => Some(Int32),
            (Int32, UInt32) => Some(Int64),
            #[cfg(feature = "dtype-i128")]
            (Int32, UInt64) => Some(Int128),
            #[cfg(not(feature = "dtype-i128"))]
            (Int32, UInt64) => Some(Float64), // Follow numpy
            #[cfg(feature = "dtype-f16")]
            (Int32, Float16) => Some(Float64),
            (Int32, Float32) => Some(Float64), // Follow numpy
            (Int32, Float64) => Some(Float64),

            (Int64, Boolean) => Some(Int64),
            #[cfg(feature = "dtype-i8")]
            (Int64, Int8) => Some(Int64),
            #[cfg(feature = "dtype-i16")]
            (Int64, Int16) => Some(Int64),
            (Int64, Int32) => Some(Int64),
            //(Int64, Int64) => Some(Int64),
            #[cfg(feature = "dtype-u8")]
            (Int64, UInt8) => Some(Int64),
            #[cfg(feature = "dtype-u16")]
            (Int64, UInt16) => Some(Int64),
            (Int64, UInt32) => Some(Int64),
            #[cfg(feature = "dtype-i128")]
            (Int64, UInt64) => Some(Int128),
            #[cfg(not(feature = "dtype-i128"))]
            (Int64, UInt64) => Some(Float64), // Follow numpy
            #[cfg(feature = "dtype-f16")]
            (Int64, Float16) => Some(Float64), // Follow (Int64, Float32) case
            (Int64, Float32) => Some(Float64), // Follow numpy
            (Int64, Float64) => Some(Float64),

            #[cfg(feature = "dtype-i128")]
            (Int128, a) if a.is_integer() | a.is_bool() => Some(Int128),
            #[cfg(feature = "dtype-i128")]
            (Int128, a) if a.is_float() => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (UInt8, UInt32) => Some(UInt32),
            #[cfg(feature = "dtype-u8")]
            (UInt8, UInt64) => Some(UInt64),

            #[cfg(all(feature = "dtype-u16", feature = "dtype-u8"))]
            (UInt16, UInt8) => Some(UInt16),
            #[cfg(feature = "dtype-u16")]
            (UInt16, UInt32) => Some(UInt32),
            #[cfg(feature = "dtype-u16")]
            (UInt16, UInt64) => Some(UInt64),

            (UInt32, UInt64) => Some(UInt64),

            #[cfg(feature = "dtype-u128")]
            (UInt128, a) if a.is_unsigned_integer() || a.is_bool() => Some(UInt128),
            #[cfg(feature = "dtype-u128")]
            (UInt128, a) if a.is_signed_integer() => Some(Int128),
            #[cfg(feature = "dtype-u128")]
            (UInt128, a) if a.is_float() => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (Boolean, UInt8) => Some(UInt8),
            #[cfg(feature = "dtype-u16")]
            (Boolean, UInt16) => Some(UInt16),
            (Boolean, UInt32) => Some(UInt32),
            (Boolean, UInt64) => Some(UInt64),

            #[cfg(all(feature = "dtype-f16", feature = "dtype-u8"))]
            (Float16, UInt8) => Some(Float16),
            #[cfg(all(feature = "dtype-f16", feature = "dtype-u16"))]
            (Float16, UInt16) => Some(Float32),
            #[cfg(feature = "dtype-f16")]
            (Float16, UInt32) => Some(Float64),
            #[cfg(feature = "dtype-f16")]
            (Float16, UInt64) => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (Float32, UInt8) => Some(Float32),
            #[cfg(feature = "dtype-u16")]
            (Float32, UInt16) => Some(Float32),
            (Float32, UInt32) => Some(Float64),
            (Float32, UInt64) => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (Float64, UInt8) => Some(Float64),
            #[cfg(feature = "dtype-u16")]
            (Float64, UInt16) => Some(Float64),
            (Float64, UInt32) => Some(Float64),
            (Float64, UInt64) => Some(Float64),

            #[cfg(feature = "dtype-f16")]
            (Float16, Float32) => Some(Float32),
            #[cfg(feature = "dtype-f16")]
            (Float16, Float64) => Some(Float64),
            (Float32, Float64) => Some(Float64),
            #[cfg(feature = "dtype-f16")]
            (Float32, Float16) => Some(Float32),
            #[cfg(feature = "dtype-f16")]
            (Float64, Float16) => Some(Float64),
            (Float64, Float32) => Some(Float64),

            // Time related dtypes
            #[cfg(feature = "dtype-date")]
            (Date, UInt32) => Some(Int64),
            #[cfg(feature = "dtype-date")]
            (Date, UInt64) => Some(Int64),
            #[cfg(feature = "dtype-date")]
            (Date, Int32) => Some(Int32),
            #[cfg(feature = "dtype-date")]
            (Date, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-date", feature = "dtype-f16"))]
            (Date, Float16) => Some(Float32),
            #[cfg(feature = "dtype-date")]
            (Date, Float32) => Some(Float32),
            #[cfg(feature = "dtype-date")]
            (Date, Float64) => Some(Float64),
            #[cfg(all(feature = "dtype-date", feature = "dtype-datetime"))]
            (Date, Datetime(tu, tz)) => Some(Datetime(*tu, tz.clone())),

            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), UInt32) => Some(Int64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), UInt64) => Some(Int64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Int32) => Some(Int64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-datetime", feature = "dtype-f16"))]
            (Datetime(_, _), Float16) => Some(Float64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Float32) => Some(Float64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Float64) => Some(Float64),
            #[cfg(all(feature = "dtype-datetime", feature = "dtype-date"))]
            (Datetime(tu, tz), Date) => Some(Datetime(*tu, tz.clone())),

            #[cfg(feature = "dtype-f16")]
            (Boolean, Float16) => Some(Float16),
            (Boolean, Float32) => Some(Float32),
            (Boolean, Float64) => Some(Float64),

            #[cfg(feature = "dtype-duration")]
            (Duration(_), UInt32) => Some(Int64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), UInt64) => Some(Int64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Int32) => Some(Int64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-duration", feature = "dtype-f16"))]
            (Duration(_), Float16) => Some(Float64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Float32) => Some(Float64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Float64) => Some(Float64),

            #[cfg(feature = "dtype-time")]
            (Time, Int32) => Some(Int64),
            #[cfg(feature = "dtype-time")]
            (Time, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-time", feature = "dtype-f16"))]
            (Time, Float16) => Some(Float64),
            #[cfg(feature = "dtype-time")]
            (Time, Float32) => Some(Float64),
            #[cfg(feature = "dtype-time")]
            (Time, Float64) => Some(Float64),

            // Every known type can be cast to a string except binary
            (dt, String) if !matches!(dt, Unknown(UnknownKind::Any)) && dt != &Binary && options.allow_primitive_to_string() || !dt.to_physical().is_primitive() => Some(String),
            (String, Binary) => Some(Binary),
            (dt, Null) => Some(dt.clone()),

            #[cfg(all(feature = "dtype-duration", feature = "dtype-datetime"))]
            (Duration(lu), Datetime(ru, Some(tz))) | (Datetime(lu, Some(tz)), Duration(ru)) => {
                if tz.is_empty() {
                    Some(Datetime(get_time_units(lu, ru), None))
                } else {
                    Some(Datetime(get_time_units(lu, ru), Some(tz.clone())))
                }
            }
            #[cfg(all(feature = "dtype-duration", feature = "dtype-datetime"))]
            (Duration(lu), Datetime(ru, None)) | (Datetime(lu, None), Duration(ru)) => {
                Some(Datetime(get_time_units(lu, ru), None))
            }
            #[cfg(all(feature = "dtype-duration", feature = "dtype-date"))]
            (Duration(_), Date) | (Date, Duration(_)) => Some(Date),
            #[cfg(feature = "dtype-duration")]
            (Duration(lu), Duration(ru)) => Some(Duration(get_time_units(lu, ru))),

            // both None or both Some("<tz>") timezones
            // we cast from more precision to higher precision as that always fits with occasional loss of precision
            #[cfg(feature = "dtype-datetime")]
            (Datetime(tu_l, tz_l), Datetime(tu_r, tz_r)) if
                // both are none
                (tz_l.is_none() && tz_r.is_none())
                // both have the same time zone
                || (tz_l.is_some() && (tz_l == tz_r)) => {
                let tu = get_time_units(tu_l, tu_r);
                Some(Datetime(tu, tz_r.clone()))
            }
            (List(inner_left), List(inner_right)) => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-array")]
            (List(inner_left), Array(inner_right, _)) | (Array(inner_left, _), List(inner_right)) => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-array")]
            (Array(inner_left, width_left), Array(inner_right, width_right)) if *width_left == *width_right => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(Array(Box::new(st), *width_left))
            }
            #[cfg(feature = "dtype-map")]
            (Map(key_left, value_left), Map(key_right, value_right)) => {
                // We forbid casting the key type, as it might collapse distinct keys into one.
                if key_left != key_right
                    && !key_left.is_nested_null()
                    && !key_right.is_nested_null()
                {
                    return None;
                }
                let key = get_supertype(key_left, key_right)?;
                let value = get_supertype(value_left, value_right)?;
                Some(Map(Box::new(key), Box::new(value)))
            }
            (List(inner), other) | (other, List(inner)) if options.allow_implode_list() => {
                let st = get_supertype(inner, other)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-array")]
            (Array(inner_left, _), Array(inner_right, _)) => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-struct")]
            (Struct(inner), right @ Unknown(UnknownKind::Float | UnknownKind::Int(_))) => {
                match inner.first() {
                    Some(inner) => get_supertype(&inner.dtype, right),
                    None => None
                }
            },
            #[cfg(feature = "dtype-struct")]
            (Struct(fields_a), Struct(fields_b)) => {
                super_type_structs(fields_a, fields_b)
            }
            #[cfg(feature = "dtype-struct")]
            (Struct(fields_a), rhs) if rhs.is_primitive_numeric() => {
                let mut new_fields = Vec::with_capacity(fields_a.len());
                for a in fields_a {
                    let st = get_supertype(&a.dtype, rhs)?;
                    new_fields.push(Field::new(a.name.clone(), st))
                }
                Some(Struct(new_fields))
            }
            #[cfg(feature = "dtype-decimal")]
            (Decimal(p1, s1), Decimal(p2, s2)) => {
                // Keep all integer digits and the larger scale. Beyond precision 38 values
                // that don't fit raise when cast.
                let s = (*s1).max(*s2);
                let p = ((p1 - s1).max(p2 - s2) + s).min(DEC128_MAX_PREC);
                Some(Decimal(p, s))
            },
            #[cfg(all(feature = "dtype-decimal", feature = "dtype-f16"))]
            (Decimal(_, _), Float16) => Some(Float64),
            #[cfg(feature = "dtype-decimal")]
            (Decimal(_, _), Float32 | Float64 | Unknown(UnknownKind::Float)) => Some(Float64),
            #[cfg(feature = "dtype-decimal")]
            (Decimal(prec, scale), dt) if dt.is_signed_integer() || dt.is_unsigned_integer() => {
                let fits = |v| { i128_to_dec128(v, *prec, *scale).is_some() };
                let fits_orig_prec_scale = match dt {
                    UInt8 => fits(u8::MAX as i128),
                    UInt16 => fits(u16::MAX as i128),
                    UInt32 => fits(u32::MAX as i128),
                    UInt64 => fits(u64::MAX as i128),
                    UInt128 => false,
                    Int8 => fits(i8::MAX as i128),
                    Int16 => fits(i16::MAX as i128),
                    Int32 => fits(i32::MAX as i128),
                    Int64 => fits(i64::MAX as i128),
                    Int128 => false,
                    _ => unreachable!(),
                };
                if fits_orig_prec_scale {
                    Some(Decimal(*prec, *scale))
                } else {
                    Some(Decimal(DEC128_MAX_PREC, *scale))
                }
            }
            (dt, Unknown(kind)) => {
                match kind {
                    UnknownKind::Float | UnknownKind::Int(_) if  dt.is_string() => {
                        if options.allow_primitive_to_string() {
                            Some(dt.clone())
                        } else {
                            None
                        }
                    },
                    // Materialize float to float
                    UnknownKind::Float | UnknownKind::Int(_) if dt.is_float() => Some(dt.clone()),
                    UnknownKind::Float if dt.is_integer() => {
                        if dt.is_known() {
                            Some(Float64)
                        } else {
                            Some(Unknown(UnknownKind::Float))
                        }
                    },
                    // Materialize str
                    UnknownKind::Str if dt.is_string() | dt.is_enum() => Some(dt.clone()),
                    // Materialize str
                    #[cfg(feature = "dtype-categorical")]
                    UnknownKind::Str if dt.is_categorical() => Some(dt.clone()),
                    // Keep unknown
                    dynam if dt.is_null() => Some(Unknown(*dynam)),
                    // Find integers sizes
                    UnknownKind::Int(v) if dt.is_primitive_numeric() => {
                        // Both dyn int
                        if let Unknown(UnknownKind::Int(v_other)) = dt {
                            // Take the maximum value to ensure we bubble up the required minimal size.
                            Some(Unknown(UnknownKind::Int(std::cmp::max(*v, *v_other))))
                        }
                        // dyn int vs number
                        else {
                            let smallest_fitting_dtype = if dt.is_unsigned_integer() && !v.is_negative() {
                                materialize_dyn_int_pos(*v).dtype()
                            } else {
                                materialize_smallest_dyn_int(*v).dtype()
                            };
                            match dt {
                                UInt64 if smallest_fitting_dtype.is_signed_integer() => {
                                    // Ensure we don't cast to float when dealing with dynamic literals
                                    Some(Int64)
                                },
                                _ => {
                                    get_supertype(dt, &smallest_fitting_dtype)
                                }
                            }
                        }
                    }
                    UnknownKind::Int(v) if dt.is_bool() => {
                        let int_dtype = materialize_dyn_int(*v).dtype();
                        get_supertype(dt, &int_dtype)
                    },
                    #[cfg(feature = "dtype-decimal")]
                    UnknownKind::Int(_) if dt.is_decimal() => {
                        let DataType::Decimal(_prec, scale) = dt else { unreachable!() };
                        Some(DataType::Decimal(DEC128_MAX_PREC, *scale))
                    }
                    _ => Some(Unknown(UnknownKind::Any))
                }
            },
            _ => None,
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn inner(l: &DataType, r: &DataType, options: SuperTypeOptions) -> Option<DataType> {
        use DataType::*;
        if l == r {
            return Some(l.clone());
        }
        match (l, r) {
            #[cfg(feature = "dtype-i8")]
            (Int8, Boolean) => Some(Int8),
            //(Int8, Int8) => Some(Int8),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-i16"))]
            (Int8, Int16) => Some(Int16),
            #[cfg(feature = "dtype-i8")]
            (Int8, Int32) => Some(Int32),
            #[cfg(feature = "dtype-i8")]
            (Int8, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-i16"))]
            (Int8, UInt8) => Some(Int16),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-u16"))]
            (Int8, UInt16) => Some(Int32),
            #[cfg(feature = "dtype-i8")]
            (Int8, UInt32) => Some(Int64),
            #[cfg(all(feature = "dtype-i8", feature = "dtype-i128"))]
            (Int8, UInt64) => Some(Int128),
            #[cfg(all(feature = "dtype-i8", not(feature = "dtype-i128")))]
            (Int8, UInt64) => Some(Float64), // Follow numpy
            #[cfg(all(feature = "dtype-i8", feature = "dtype-f16"))]
            (Int8, Float16) => Some(Float16),
            #[cfg(feature = "dtype-i8")]
            (Int8, Float32) => Some(Float32),
            #[cfg(feature = "dtype-i8")]
            (Int8, Float64) => Some(Float64),

            #[cfg(feature = "dtype-i16")]
            (Int16, Boolean) => Some(Int16),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-i8"))]
            (Int16, Int8) => Some(Int16),
            //(Int16, Int16) => Some(Int16),
            #[cfg(feature = "dtype-i16")]
            (Int16, Int32) => Some(Int32),
            #[cfg(feature = "dtype-i16")]
            (Int16, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-u8"))]
            (Int16, UInt8) => Some(Int16),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-u16"))]
            (Int16, UInt16) => Some(Int32),
            #[cfg(feature = "dtype-i16")]
            (Int16, UInt32) => Some(Int64),
            #[cfg(all(feature = "dtype-i16", feature = "dtype-i128"))]
            (Int16, UInt64) => Some(Int128),
            #[cfg(all(feature = "dtype-i16", not(feature = "dtype-i128")))]
            (Int16, UInt64) => Some(Float64), // Follow numpy
            #[cfg(all(feature = "dtype-i16", feature = "dtype-f16"))]
            (Int16, Float16) => Some(Float32),
            #[cfg(feature = "dtype-i16")]
            (Int16, Float32) => Some(Float32),
            #[cfg(feature = "dtype-i16")]
            (Int16, Float64) => Some(Float64),

            (Int32, Boolean) => Some(Int32),
            #[cfg(feature = "dtype-i8")]
            (Int32, Int8) => Some(Int32),
            #[cfg(feature = "dtype-i16")]
            (Int32, Int16) => Some(Int32),
            //(Int32, Int32) => Some(Int32),
            (Int32, Int64) => Some(Int64),
            #[cfg(feature = "dtype-u8")]
            (Int32, UInt8) => Some(Int32),
            #[cfg(feature = "dtype-u16")]
            (Int32, UInt16) => Some(Int32),
            (Int32, UInt32) => Some(Int64),
            #[cfg(feature = "dtype-i128")]
            (Int32, UInt64) => Some(Int128),
            #[cfg(not(feature = "dtype-i128"))]
            (Int32, UInt64) => Some(Float64), // Follow numpy
            #[cfg(feature = "dtype-f16")]
            (Int32, Float16) => Some(Float64),
            (Int32, Float32) => Some(Float64), // Follow numpy
            (Int32, Float64) => Some(Float64),

            (Int64, Boolean) => Some(Int64),
            #[cfg(feature = "dtype-i8")]
            (Int64, Int8) => Some(Int64),
            #[cfg(feature = "dtype-i16")]
            (Int64, Int16) => Some(Int64),
            (Int64, Int32) => Some(Int64),
            //(Int64, Int64) => Some(Int64),
            #[cfg(feature = "dtype-u8")]
            (Int64, UInt8) => Some(Int64),
            #[cfg(feature = "dtype-u16")]
            (Int64, UInt16) => Some(Int64),
            (Int64, UInt32) => Some(Int64),
            #[cfg(feature = "dtype-i128")]
            (Int64, UInt64) => Some(Int128),
            #[cfg(not(feature = "dtype-i128"))]
            (Int64, UInt64) => Some(Float64), // Follow numpy
            #[cfg(feature = "dtype-f16")]
            (Int64, Float16) => Some(Float64), // Follow (Int64, Float32) case
            (Int64, Float32) => Some(Float64), // Follow numpy
            (Int64, Float64) => Some(Float64),

            #[cfg(feature = "dtype-i128")]
            (Int128, a) if a.is_integer() | a.is_bool() => Some(Int128),
            #[cfg(feature = "dtype-i128")]
            (Int128, a) if a.is_float() => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (UInt8, UInt32) => Some(UInt32),
            #[cfg(feature = "dtype-u8")]
            (UInt8, UInt64) => Some(UInt64),

            #[cfg(all(feature = "dtype-u16", feature = "dtype-u8"))]
            (UInt16, UInt8) => Some(UInt16),
            #[cfg(feature = "dtype-u16")]
            (UInt16, UInt32) => Some(UInt32),
            #[cfg(feature = "dtype-u16")]
            (UInt16, UInt64) => Some(UInt64),

            (UInt32, UInt64) => Some(UInt64),

            #[cfg(feature = "dtype-u128")]
            (UInt128, a) if a.is_unsigned_integer() || a.is_bool() => Some(UInt128),
            #[cfg(feature = "dtype-u128")]
            (UInt128, a) if a.is_signed_integer() => Some(Int128),
            #[cfg(feature = "dtype-u128")]
            (UInt128, a) if a.is_float() => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (Boolean, UInt8) => Some(UInt8),
            #[cfg(feature = "dtype-u16")]
            (Boolean, UInt16) => Some(UInt16),
            (Boolean, UInt32) => Some(UInt32),
            (Boolean, UInt64) => Some(UInt64),

            #[cfg(all(feature = "dtype-f16", feature = "dtype-u8"))]
            (Float16, UInt8) => Some(Float16),
            #[cfg(all(feature = "dtype-f16", feature = "dtype-u16"))]
            (Float16, UInt16) => Some(Float32),
            #[cfg(feature = "dtype-f16")]
            (Float16, UInt32) => Some(Float64),
            #[cfg(feature = "dtype-f16")]
            (Float16, UInt64) => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (Float32, UInt8) => Some(Float32),
            #[cfg(feature = "dtype-u16")]
            (Float32, UInt16) => Some(Float32),
            (Float32, UInt32) => Some(Float64),
            (Float32, UInt64) => Some(Float64),

            #[cfg(feature = "dtype-u8")]
            (Float64, UInt8) => Some(Float64),
            #[cfg(feature = "dtype-u16")]
            (Float64, UInt16) => Some(Float64),
            (Float64, UInt32) => Some(Float64),
            (Float64, UInt64) => Some(Float64),

            #[cfg(feature = "dtype-f16")]
            (Float16, Float32) => Some(Float32),
            #[cfg(feature = "dtype-f16")]
            (Float16, Float64) => Some(Float64),
            (Float32, Float64) => Some(Float64),
            #[cfg(feature = "dtype-f16")]
            (Float32, Float16) => Some(Float32),
            #[cfg(feature = "dtype-f16")]
            (Float64, Float16) => Some(Float64),
            (Float64, Float32) => Some(Float64),

            // Time related dtypes
            #[cfg(feature = "dtype-date")]
            (Date, UInt32) => Some(Int64),
            #[cfg(feature = "dtype-date")]
            (Date, UInt64) => Some(Int64),
            #[cfg(feature = "dtype-date")]
            (Date, Int32) => Some(Int32),
            #[cfg(feature = "dtype-date")]
            (Date, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-date", feature = "dtype-f16"))]
            (Date, Float16) => Some(Float32),
            #[cfg(feature = "dtype-date")]
            (Date, Float32) => Some(Float32),
            #[cfg(feature = "dtype-date")]
            (Date, Float64) => Some(Float64),
            #[cfg(all(feature = "dtype-date", feature = "dtype-datetime"))]
            (Date, Datetime(tu, tz)) => Some(Datetime(*tu, tz.clone())),

            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), UInt32) => Some(Int64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), UInt64) => Some(Int64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Int32) => Some(Int64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-datetime", feature = "dtype-f16"))]
            (Datetime(_, _), Float16) => Some(Float64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Float32) => Some(Float64),
            #[cfg(feature = "dtype-datetime")]
            (Datetime(_, _), Float64) => Some(Float64),
            #[cfg(all(feature = "dtype-datetime", feature = "dtype-date"))]
            (Datetime(tu, tz), Date) => Some(Datetime(*tu, tz.clone())),

            #[cfg(feature = "dtype-f16")]
            (Boolean, Float16) => Some(Float16),
            (Boolean, Float32) => Some(Float32),
            (Boolean, Float64) => Some(Float64),

            #[cfg(feature = "dtype-duration")]
            (Duration(_), UInt32) => Some(Int64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), UInt64) => Some(Int64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Int32) => Some(Int64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-duration", feature = "dtype-f16"))]
            (Duration(_), Float16) => Some(Float64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Float32) => Some(Float64),
            #[cfg(feature = "dtype-duration")]
            (Duration(_), Float64) => Some(Float64),

            #[cfg(feature = "dtype-time")]
            (Time, Int32) => Some(Int64),
            #[cfg(feature = "dtype-time")]
            (Time, Int64) => Some(Int64),
            #[cfg(all(feature = "dtype-time", feature = "dtype-f16"))]
            (Time, Float16) => Some(Float64),
            #[cfg(feature = "dtype-time")]
            (Time, Float32) => Some(Float64),
            #[cfg(feature = "dtype-time")]
            (Time, Float64) => Some(Float64),

            // Every known type can be cast to a string except binary
            (dt, String) if !matches!(dt, Unknown(UnknownKind::Any)) && dt != &Binary && options.allow_primitive_to_string() || !dt.to_physical().is_primitive() => Some(String),
            (String, Binary) => Some(Binary),
            (dt, Null) => Some(dt.clone()),

            #[cfg(all(feature = "dtype-duration", feature = "dtype-datetime"))]
            (Duration(lu), Datetime(ru, Some(tz))) | (Datetime(lu, Some(tz)), Duration(ru)) => {
                if tz.is_empty() {
                    Some(Datetime(get_time_units(lu, ru), None))
                } else {
                    Some(Datetime(get_time_units(lu, ru), Some(tz.clone())))
                }
            }
            #[cfg(all(feature = "dtype-duration", feature = "dtype-datetime"))]
            (Duration(lu), Datetime(ru, None)) | (Datetime(lu, None), Duration(ru)) => {
                Some(Datetime(get_time_units(lu, ru), None))
            }
            #[cfg(all(feature = "dtype-duration", feature = "dtype-date"))]
            (Duration(_), Date) | (Date, Duration(_)) => Some(Date),
            #[cfg(feature = "dtype-duration")]
            (Duration(lu), Duration(ru)) => Some(Duration(get_time_units(lu, ru))),

            // both None or both Some("<tz>") timezones
            // we cast from more precision to higher precision as that always fits with occasional loss of precision
            #[cfg(feature = "dtype-datetime")]
            (Datetime(tu_l, tz_l), Datetime(tu_r, tz_r)) if
                // both are none
                (tz_l.is_none() && tz_r.is_none())
                // both have the same time zone
                || (tz_l.is_some() && (tz_l == tz_r)) => {
                let tu = get_time_units(tu_l, tu_r);
                Some(Datetime(tu, tz_r.clone()))
            }
            (List(inner_left), List(inner_right)) => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-array")]
            (List(inner_left), Array(inner_right, _)) | (Array(inner_left, _), List(inner_right)) => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-array")]
            (Array(inner_left, width_left), Array(inner_right, width_right)) if *width_left == *width_right => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(Array(Box::new(st), *width_left))
            }
            #[cfg(feature = "dtype-map")]
            (Map(key_left, value_left), Map(key_right, value_right)) => {
                // We forbid casting the key type, as it might collapse distinct keys into one.
                if key_left != key_right
                    && !key_left.is_nested_null()
                    && !key_right.is_nested_null()
                {
                    return None;
                }
                let key = get_supertype(key_left, key_right)?;
                let value = get_supertype(value_left, value_right)?;
                Some(Map(Box::new(key), Box::new(value)))
            }
            (List(inner), other) | (other, List(inner)) if options.allow_implode_list() => {
                let st = get_supertype(inner, other)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-array")]
            (Array(inner_left, _), Array(inner_right, _)) => {
                let st = get_supertype(inner_left, inner_right)?;
                Some(List(Box::new(st)))
            }
            #[cfg(feature = "dtype-struct")]
            (Struct(inner), right @ Unknown(UnknownKind::Float | UnknownKind::Int(_))) => {
                match inner.first() {
                    Some(inner) => get_supertype(&inner.dtype, right),
                    None => None
                }
            },
            #[cfg(feature = "dtype-struct")]
            (Struct(fields_a), Struct(fields_b)) => {
                super_type_structs(fields_a, fields_b)
            }
            #[cfg(feature = "dtype-struct")]
            (Struct(fields_a), rhs) if rhs.is_primitive_numeric() => {
                let mut new_fields = Vec::with_capacity(fields_a.len());
                for a in fields_a {
                    let st = get_supertype(&a.dtype, rhs)?;
                    new_fields.push(Field::new(a.name.clone(), st))
                }
                Some(Struct(new_fields))
            }
            #[cfg(feature = "dtype-decimal")]
            (Decimal(p1, s1), Decimal(p2, s2)) => {
                // Keep all integer digits and the larger scale. Beyond precision 38 values
                // that don't fit raise when cast.
                let s = (*s1).max(*s2);
                let p = ((p1 - s1).max(p2 - s2) + s).min(DEC128_MAX_PREC);
                Some(Decimal(p, s))
            },
            #[cfg(all(feature = "dtype-decimal", feature = "dtype-f16"))]
            (Decimal(_, _), Float16) => Some(Float64),
            #[cfg(feature = "dtype-decimal")]
            (Decimal(_, _), Float32 | Float64 | Unknown(UnknownKind::Float)) => Some(Float64),
            #[cfg(feature = "dtype-decimal")]
            (Decimal(prec, scale), dt) if dt.is_signed_integer() || dt.is_unsigned_integer() => {
                let fits = |v| { i128_to_dec128(v, *prec, *scale).is_some() };
                let fits_orig_prec_scale = match dt {
                    UInt8 => fits(u8::MAX as i128),
                    UInt16 => fits(u16::MAX as i128),
                    UInt32 => fits(u32::MAX as i128),
                    UInt64 => fits(u64::MAX as i128),
                    UInt128 => false,
                    Int8 => fits(i8::MAX as i128),
                    Int16 => fits(i16::MAX as i128),
                    Int32 => fits(i32::MAX as i128),
                    Int64 => fits(i64::MAX as i128),
                    Int128 => false,
                    _ => unreachable!(),
                };
                if fits_orig_prec_scale {
                    Some(Decimal(*prec, *scale))
                } else {
                    Some(Decimal(DEC128_MAX_PREC, *scale))
                }
            }
            (dt, Unknown(kind)) => {
                match kind {
                    UnknownKind::Float | UnknownKind::Int(_) if  dt.is_string() => {
                        if options.allow_primitive_to_string() {
                            Some(dt.clone())
                        } else {
                            None
                        }
                    },
                    // Materialize float to float
                    UnknownKind::Float | UnknownKind::Int(_) if dt.is_float() => Some(dt.clone()),
                    UnknownKind::Float if dt.is_bool() => Some(Unknown(UnknownKind::Float)),
                    UnknownKind::Float if dt.is_integer() => {
                        if dt.is_known() {
                            Some(Float64)
                        } else {
                            Some(Unknown(UnknownKind::Float))
                        }
                    },
                    // Materialize str
                    UnknownKind::Str if dt.is_string() | dt.is_enum() => Some(dt.clone()),
                    // Materialize str
                    #[cfg(feature = "dtype-categorical")]
                    UnknownKind::Str if dt.is_categorical() => Some(dt.clone()),
                    // Keep unknown
                    dynam if dt.is_null() => Some(Unknown(*dynam)),
                    // Find integers sizes
                    UnknownKind::Int(v) if dt.is_primitive_numeric() => {
                        // Both dyn int
                        if let Unknown(UnknownKind::Int(v_other)) = dt {
                            // Take the maximum value to ensure we bubble up the required minimal size.
                            Some(Unknown(UnknownKind::Int(std::cmp::max(*v, *v_other))))
                        }
                        // dyn int vs number
                        else {
                            let smallest_fitting_dtype = if dt.is_unsigned_integer() && !v.is_negative() {
                                materialize_dyn_int_pos(*v).dtype()
                            } else {
                                materialize_smallest_dyn_int(*v).dtype()
                            };
                            match dt {
                                UInt64 if smallest_fitting_dtype.is_signed_integer() => {
                                    // Ensure we don't cast to float when dealing with dynamic literals
                                    Some(Int64)
                                },
                                _ => {
                                    get_supertype(dt, &smallest_fitting_dtype)
                                }
                            }
                        }
                    }
                    UnknownKind::Int(v) if dt.is_bool() => {
                        let int_dtype = materialize_dyn_int(*v).dtype();
                        get_supertype(dt, &int_dtype)
                    },
                    #[cfg(feature = "dtype-decimal")]
                    UnknownKind::Int(_) if dt.is_decimal() => {
                        let DataType::Decimal(_prec, scale) = dt else { unreachable!() };
                        Some(DataType::Decimal(DEC128_MAX_PREC, *scale))
                    }
                    _ => Some(Unknown(UnknownKind::Any))
                }
            },
            _ => None,
        }
    }
```


---

### 🔹 Commit #17: `a850ab56`
- **完整 Hash**: `a850ab56352f10ea3cf7171e8c3329471a1d760e`
- **說明 (Ground Truth)**: fix: More numerically stable ewm_std/var (#29942)
- **變更檔案數**: 1

#### 📄 檔案: `crates/polars-compute/src/ewm/cov.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:48, E:58, A:0) ➔ After(N:48, E:58, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
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

### 🔹 函式: `EwmCovState::update_iter()`
- **變更前簽章 (Before)**: `fn EwmCovState::update_iter(&mut self, values: I)` (L55~L127)
- **變更後簽章 (After)**: `fn EwmCovState::update_iter(&mut self, values: I)` (L56~L129)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn update_iter<I>(&mut self, values: I) -> impl Iterator<Item = Option<T>>
    where
        I: IntoIterator<Item = Option<(T, T)>>,
    {
        let other_weight = if self.adjust { T::one() } else { self.alpha };

        values.into_iter().map(move |opt_xy| {
            if self.non_null_count == 0
                && let Some((x, y)) = opt_xy
            {
                // Initialize
                self.non_null_count = 1;
                self.mean_x = x;
                self.mean_y = y;
                self.weight = T::one();
                self.weight_sum = T::one();
                self.weight_square_sum = T::one();
            } else {
                if opt_xy.is_some() || !self.ignore_nulls {
                    self.weight_sum *= T::one() - self.alpha;
                    self.weight_square_sum *= (T::one() - self.alpha) * (T::one() - self.alpha);
                    self.weight *= T::one() - self.alpha;
                }

                if let Some((other_x, other_y)) = opt_xy {
                    self.non_null_count += 1;

                    let new_weight = self.weight + other_weight;
                    let other_weight_frac = other_weight / new_weight;
                    let delta_mean_x = other_x - self.mean_x;
                    let delta_mean_y = other_y - self.mean_y;

                    let new_mean_x = self.mean_x + delta_mean_x * other_weight_frac;
                    let new_mean_y = self.mean_y + delta_mean_y * other_weight_frac;

                    let cov = ((self.weight
                        * (self.cov + (self.mean_x - new_mean_x) * (self.mean_y - new_mean_y)))
                        + other_weight * (other_x - new_mean_x) * (other_y - new_mean_y))
                        / new_weight;

                    self.cov = cov;
                    self.weight = new_weight;
                    self.mean_x = new_mean_x;
                    self.mean_y = new_mean_y;

                    self.weight_sum += other_weight;
                    self.weight_square_sum += other_weight * other_weight;

                    if !self.adjust {
                        self.weight_sum /= new_weight;
                        self.weight_square_sum /= new_weight * new_weight;
                        self.weight = T::one();
                    }
                }
            }

            (opt_xy.is_some() && self.non_null_count >= self.min_periods)
                .then_some(self.cov)
                .and_then(|cov| {
                    if self.bias {
                        Some(cov)
                    } else {
                        let numerator = self.weight_sum * self.weight_sum;
                        let denominator = numerator - self.weight_square_sum;
                        if denominator > T::zero() {
                            Some((numerator / denominator) * cov)
                        } else {
                            None
                        }
                    }
                })
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn update_iter<I>(&mut self, values: I) -> impl Iterator<Item = Option<T>>
    where
        I: IntoIterator<Item = Option<(T, T)>>,
    {
        let other_weight = if self.adjust { T::one() } else { self.alpha };

        values.into_iter().map(move |opt_xy| {
            if self.non_null_count == 0
                && let Some((x, y)) = opt_xy
            {
                // Initialize
                self.non_null_count = 1;
                self.mean_x = x;
                self.mean_y = y;
                self.weight = T::one();
                self.weight_sum = T::one();
                self.weight_pair_sum = T::zero();
            } else {
                if opt_xy.is_some() || !self.ignore_nulls {
                    self.weight_sum *= T::one() - self.alpha;
                    self.weight_pair_sum *= (T::one() - self.alpha) * (T::one() - self.alpha);
                    self.weight *= T::one() - self.alpha;
                }

                if let Some((other_x, other_y)) = opt_xy {
                    self.non_null_count += 1;

                    let new_weight = self.weight + other_weight;
                    let other_weight_frac = other_weight / new_weight;
                    let delta_mean_x = other_x - self.mean_x;
                    let delta_mean_y = other_y - self.mean_y;

                    let new_mean_x = self.mean_x + delta_mean_x * other_weight_frac;
                    let new_mean_y = self.mean_y + delta_mean_y * other_weight_frac;

                    let cov = ((self.weight
                        * (self.cov + (self.mean_x - new_mean_x) * (self.mean_y - new_mean_y)))
                        + other_weight * (other_x - new_mean_x) * (other_y - new_mean_y))
                        / new_weight;

                    self.cov = cov;
                    self.weight = new_weight;
                    self.mean_x = new_mean_x;
                    self.mean_y = new_mean_y;

                    self.weight_pair_sum += self.weight_sum * other_weight;
                    self.weight_sum += other_weight;

                    if !self.adjust {
                        self.weight_sum /= new_weight;
                        self.weight_pair_sum /= new_weight * new_weight;
                        self.weight = T::one();
                    }
                }
            }

            (opt_xy.is_some() && self.non_null_count >= self.min_periods)
                .then_some(self.cov)
                .and_then(|cov| {
                    if self.bias {
                        Some(cov)
                    } else {
                        let numerator = self.weight_sum * self.weight_sum;
                        // Equal to `numerator - sum(w_i^2)`, without the cancellation.
                        let denominator = self.weight_pair_sum + self.weight_pair_sum;
                        if denominator > T::zero() {
                            Some((numerator / denominator) * cov)
                        } else {
                            None
                        }
                    }
                })
        })
    }
```

### 🔹 函式: `EwmCovState::new()`
- **變更前簽章 (Before)**: `fn EwmCovState::new(alpha: T, adjust: bool, bias: bool, min_periods: usize, ignore_nulls: bool)` (L29~L44)
- **變更後簽章 (After)**: `fn EwmCovState::new(alpha: T, adjust: bool, bias: bool, min_periods: usize, ignore_nulls: bool)` (L30~L45)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn new(alpha: T, adjust: bool, bias: bool, min_periods: usize, ignore_nulls: bool) -> Self {
        Self {
            mean_x: T::zero(),
            mean_y: T::zero(),
            weight: T::zero(),
            cov: T::zero(),
            weight_sum: T::zero(),
            weight_square_sum: T::zero(),
            alpha,
            non_null_count: 0,
            adjust,
            bias,
            min_periods: min_periods.max(1),
            ignore_nulls,
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn new(alpha: T, adjust: bool, bias: bool, min_periods: usize, ignore_nulls: bool) -> Self {
        Self {
            mean_x: T::zero(),
            mean_y: T::zero(),
            weight: T::zero(),
            cov: T::zero(),
            weight_sum: T::zero(),
            weight_pair_sum: T::zero(),
            alpha,
            non_null_count: 0,
            adjust,
            bias,
            min_periods: min_periods.max(1),
            ignore_nulls,
        }
    }
```

### 🔹 函式: `EPS()`
- **變更前簽章 (Before)**: `[Module State] EPS` (L233~L233)
- **變更後簽章 (After)**: `[Module State] EPS` (L235~L235)

#### ◀️ 變更前實作碼 (Before Implementation):
```
const EPS: f64 = 1e-15;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
const EPS: f64 = 1e-14;
```


---

### 🔹 Commit #18: `0f56a8f5`
- **完整 Hash**: `0f56a8f5533e7f826229e65f921157914171370c`
- **說明 (Ground Truth)**: fix: Expand `$` references in `str.replace` for patterns without punctuation (#29966)
- **變更檔案數**: 1

#### 📄 檔案: `crates/polars-expr/src/dispatch/strings.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:224, E:373, A:0) ➔ After(N:229, E:383, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 0, +Edges: 10, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `std::borrow::Cow::Borrowed (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `caps.expand (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `std::borrow::Cow::Owned (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `reg.captures (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `expand_for_literal_pat` (FUNCTION_DEF)
  • + [新增呼叫邊] `expand_for_literal_pat` ──[CALLS]──> `contains`
  • + [新增呼叫邊] `expand_for_literal_pat` ──[CALLS]──> `Ok (External/Unresolved)`
  • + [新增呼叫邊] `expand_for_literal_pat` ──[CALLS]──> `std::borrow::Cow::Borrowed (External/Unresolved)`
  • + [新增呼叫邊] `expand_for_literal_pat` ──[CALLS]──> `polars_utils::regex_cache::compile_regex (External/Unresolved)`
  • + [新增呼叫邊] `expand_for_literal_pat` ──[CALLS]──> `String::new (External/Unresolved)`
  • + [新增呼叫邊] `expand_for_literal_pat` ──[CALLS]──> `reg.captures (External/Unresolved)`
  • + [新增呼叫邊] `expand_for_literal_pat` ──[CALLS]──> `caps.expand (External/Unresolved)`
  • + [新增呼叫邊] `expand_for_literal_pat` ──[CALLS]──> `std::borrow::Cow::Owned (External/Unresolved)`
  • + [新增呼叫邊] `replace_n` ──[CALLS]──> `expand_for_literal_pat`
  • + [新增呼叫邊] `replace_all` ──[CALLS]──> `expand_for_literal_pat`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `replace_all()`
- **變更前簽章 (Before)**: `fn replace_all(
    ca: &StringChunked,
    pat: &StringChunked,
    val: &StringChunked,
    literal: bool,
)` (L689~L741)
- **變更後簽章 (After)**: `fn replace_all(
    ca: &StringChunked,
    pat: &StringChunked,
    val: &StringChunked,
    literal: bool,
)` (L703~L756)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn replace_all(
    ca: &StringChunked,
    pat: &StringChunked,
    val: &StringChunked,
    literal: bool,
) -> PolarsResult<StringChunked> {
    match (pat.len(), val.len()) {
        (1, 1) => {
            let pat = get_pat(pat)?;
            let val = val.get(0).ok_or_else(
                || polars_err!(ComputeError: "value cannot be 'null' in 'replace' expression"),
            )?;
            let literal = literal || is_literal_pat(pat);

            match literal {
                true => ca.replace_literal_all(pat, val),
                false => ca.replace_all(pat, val),
            }
        },
        (1, len_val) => {
            let mut pat = get_pat(pat)?.to_string();
            polars_ensure!(
                len_val == ca.len(),
                ComputeError:
                "replacement value length ({}) does not match string column length ({})",
                len_val, ca.len(),
            );

            let literal_pat = literal || is_literal_pat(&pat);

            if literal_pat {
                pat = escape(&pat)
            }

            let reg = polars_utils::regex_cache::compile_regex(&pat)?;

            let f = |s: &str, val: &str, buf: &mut String| {
                // According to the docs for replace_all
                // when literal = True then capture groups are ignored.
                if literal {
                    regex_replacen_into(&reg, s, 0, NoExpand(val), buf)
                } else {
                    regex_replacen_into(&reg, s, 0, val, buf)
                }
            };

            Ok(iter_and_replace(ca, val, f))
        },
        _ => polars_bail!(
            ComputeError: "dynamic pattern length in 'str.replace' expressions is not supported yet"
        ),
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn replace_all(
    ca: &StringChunked,
    pat: &StringChunked,
    val: &StringChunked,
    literal: bool,
) -> PolarsResult<StringChunked> {
    match (pat.len(), val.len()) {
        (1, 1) => {
            let pat = get_pat(pat)?;
            let val = val.get(0).ok_or_else(
                || polars_err!(ComputeError: "value cannot be 'null' in 'replace' expression"),
            )?;
            if literal {
                return ca.replace_literal_all(pat, val);
            }
            if is_literal_pat(pat) {
                return ca.replace_literal_all(pat, &expand_for_literal_pat(pat, val)?);
            }
            ca.replace_all(pat, val)
        },
        (1, len_val) => {
            let mut pat = get_pat(pat)?.to_string();
            polars_ensure!(
                len_val == ca.len(),
                ComputeError:
                "replacement value length ({}) does not match string column length ({})",
                len_val, ca.len(),
            );

            let literal_pat = literal || is_literal_pat(&pat);

            if literal_pat {
                pat = escape(&pat)
            }

            let reg = polars_utils::regex_cache::compile_regex(&pat)?;

            let f = |s: &str, val: &str, buf: &mut String| {
                // According to the docs for replace_all
                // when literal = True then capture groups are ignored.
                if literal {
                    regex_replacen_into(&reg, s, 0, NoExpand(val), buf)
                } else {
                    regex_replacen_into(&reg, s, 0, val, buf)
                }
            };

            Ok(iter_and_replace(ca, val, f))
        },
        _ => polars_bail!(
            ComputeError: "dynamic pattern length in 'str.replace' expressions is not supported yet"
        ),
    }
}
```

### 🔹 函式: `replace_n()`
- **變更前簽章 (Before)**: `fn replace_n(
    ca: &StringChunked,
    pat: &StringChunked,
    val: &StringChunked,
    literal: bool,
    n: usize,
)` (L621~L686)
- **變更後簽章 (After)**: `fn replace_n(
    ca: &StringChunked,
    pat: &StringChunked,
    val: &StringChunked,
    literal: bool,
    n: usize,
)` (L636~L700)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn replace_n(
    ca: &StringChunked,
    pat: &StringChunked,
    val: &StringChunked,
    literal: bool,
    n: usize,
) -> PolarsResult<StringChunked> {
    match (pat.len(), val.len()) {
        (1, 1) => {
            let pat = get_pat(pat)?;
            let Some(val) = val.get(0) else {
                return Ok(ca.clone());
            };
            let literal = literal || is_literal_pat(pat);

            match literal {
                true => ca.replace_literal(pat, val, n),
                false => {
                    if n > 1 {
                        polars_bail!(ComputeError: "regex replacement with 'n > 1' not yet supported")
                    }
                    ca.replace(pat, val)
                },
            }
        },
        (1, len_val) => {
            if n > 1 {
                polars_bail!(ComputeError: "multivalue replacement with 'n > 1' not yet supported")
            }

            if n == 0 {
                return Ok(ca.clone());
            };

            // from here on, we know that n == 1
            let mut pat = get_pat(pat)?.to_string();
            polars_ensure!(
                len_val == ca.len(),
                ComputeError:
                "replacement value length ({}) does not match string column length ({})",
                len_val, ca.len(),
            );
            let lit = is_literal_pat(&pat);
            let literal_pat = literal || lit;

            if literal_pat {
                pat = escape(&pat)
            }

            let reg = polars_utils::regex_cache::compile_regex(&pat)?;

            let f = |s: &str, val: &str, buf: &mut String| {
                if literal {
                    regex_replacen_into(&reg, s, 1, NoExpand(val), buf)
                } else {
                    regex_replacen_into(&reg, s, 1, val, buf)
                }
            };

            Ok(iter_and_replace(ca, val, f))
        },
        _ => polars_bail!(
            ComputeError: "dynamic pattern length in 'str.replace' expressions is not supported yet"
        ),
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn replace_n(
    ca: &StringChunked,
    pat: &StringChunked,
    val: &StringChunked,
    literal: bool,
    n: usize,
) -> PolarsResult<StringChunked> {
    match (pat.len(), val.len()) {
        (1, 1) => {
            let pat = get_pat(pat)?;
            let Some(val) = val.get(0) else {
                return Ok(ca.clone());
            };
            if literal {
                return ca.replace_literal(pat, val, n);
            }
            if is_literal_pat(pat) {
                return ca.replace_literal(pat, &expand_for_literal_pat(pat, val)?, n);
            }
            if n > 1 {
                polars_bail!(ComputeError: "regex replacement with 'n > 1' not yet supported")
            }
            ca.replace(pat, val)
        },
        (1, len_val) => {
            if n > 1 {
                polars_bail!(ComputeError: "multivalue replacement with 'n > 1' not yet supported")
            }

            if n == 0 {
                return Ok(ca.clone());
            };

            // from here on, we know that n == 1
            let mut pat = get_pat(pat)?.to_string();
            polars_ensure!(
                len_val == ca.len(),
                ComputeError:
                "replacement value length ({}) does not match string column length ({})",
                len_val, ca.len(),
            );
            let lit = is_literal_pat(&pat);
            let literal_pat = literal || lit;

            if literal_pat {
                pat = escape(&pat)
            }

            let reg = polars_utils::regex_cache::compile_regex(&pat)?;

            let f = |s: &str, val: &str, buf: &mut String| {
                if literal {
                    regex_replacen_into(&reg, s, 1, NoExpand(val), buf)
                } else {
                    regex_replacen_into(&reg, s, 1, val, buf)
                }
            };

            Ok(iter_and_replace(ca, val, f))
        },
        _ => polars_bail!(
            ComputeError: "dynamic pattern length in 'str.replace' expressions is not supported yet"
        ),
    }
}
```


---

### 🔹 Commit #19: `40dd90ee`
- **完整 Hash**: `40dd90ee0ad929acba4bdf402ba2ea2a48e54a7c`
- **說明 (Ground Truth)**: fix: Fix wrong results and name clashes for computed SQL `GROUP BY` keys (#29965)
- **變更檔案數**: 2

#### 📄 檔案: `crates/polars-sql/src/context.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:1233, E:1739, A:0) ➔ After(N:1254, E:1765, A:0)
- **差分統計**: +Nodes: 24, -Nodes: 3, +Edges: 29, -Edges: 3, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `group_by_keys
                .iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `grouping_sets.is_none (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `prepared.push (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `group_key_data
                .iter()
                .filter_map(|(key, name)| Some((key.clone(), name.clone()?)))
                .chain(match grouping {
                    Some(_) => vec![],
                    None => stored_keys.clone(),
                })
                .collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `seen.contains (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `projections
                .into_iter()
                .map(|p| {
                    let stripped = strip_outer_alias(&p);
                    let bound = bind_stored_keys(stripped.clone(), &stored_keys);
                    Ok(if bound == stripped {
                        p
                    } else {
                        bound.alias(p.to_field(&schema_before)?.name)
                    })
                })
                .collect::<PolarsResult<Vec<_>>> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `bind_stored_keys (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `stripped.clone().alias (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `stored_keys.iter().any (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `stored_keys.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `prepared.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `group_by_keys.len (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `stored_keys.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `grouping.stored_keys (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `group_by_keys.retain (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 44 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SQLContext::process_group_by()`
- **變更前簽章 (Before)**: `fn SQLContext::process_group_by(
        &mut self,
        mut lf: LazyFrame,
        group_by_keys: &[Expr],
        projections: Vec<Expr>,
        explicit_aliases: &[bool],
        having: Option<Expr>,
        qualify: Option<(PlSmallStr, Expr)>,
        order_by: &Option<OrderBy>,
        grouping: Option<&GroupingSets>,
        subquery_names: &PlHashSet<PlSmallStr>,
    )` (L3548~L3952)
- **變更後簽章 (After)**: `fn SQLContext::process_group_by(
        &mut self,
        mut lf: LazyFrame,
        group_by_keys: &[Expr],
        projections: Vec<Expr>,
        explicit_aliases: &[bool],
        having: Option<Expr>,
        qualify: Option<(PlSmallStr, Expr)>,
        order_by: &Option<OrderBy>,
        grouping: Option<&GroupingSets>,
        subquery_names: &PlHashSet<PlSmallStr>,
    )` (L3562~L4020)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn process_group_by(
        &mut self,
        mut lf: LazyFrame,
        group_by_keys: &[Expr],
        projections: Vec<Expr>,
        explicit_aliases: &[bool],
        having: Option<Expr>,
        qualify: Option<(PlSmallStr, Expr)>,
        order_by: &Option<OrderBy>,
        grouping: Option<&GroupingSets>,
        subquery_names: &PlHashSet<PlSmallStr>,
    ) -> PolarsResult<(LazyFrame, Vec<PlSmallStr>, Option<OrderBy>)> {
        let mut schema_before = self.get_frame_schema(&mut lf)?;
        let key_schema =
            expressions_to_schema(group_by_keys, &schema_before, |duplicate_name: &str| {
                format!("group_by keys contained duplicate output name '{duplicate_name}'")
            })?;
        let mut group_by_keys_schema = key_schema.clone();
        // Columns the parsed expressions may name before the aggregation resolves them:
        // the whole-frame window partition, and `GROUPING()` values, which are
        // per-set constants the projections treat like group keys.
        let whole_frame_partition = self.group_scope.whole_frame_partition.clone();
        let placeholders: Vec<PlSmallStr> = grouping
            .map(|g| g.placeholders().cloned().collect())
            .unwrap_or_default();
        if whole_frame_partition.is_some() || !placeholders.is_empty() {
            let mut extended = Arc::unwrap_or_clone(schema_before);
            if let Some(partition) = &whole_frame_partition {
                extended.with_column(partition.clone(), DataType::Int32);
            }
            for placeholder in &placeholders {
                extended.with_column(placeholder.clone(), DataType::Int64);
                group_by_keys_schema.with_column(placeholder.clone(), DataType::Int64);
            }
            schema_before = Arc::new(extended);
        }

        // Disambiguate SELECT-list output-name collisions.
        let projections = disambiguate_output_names(
            projections
                .into_iter()
                .zip(explicit_aliases.iter().copied())
                .collect(),
            &schema_before,
        )?;
        // Hidden output columns: the ORDER BY aggregates, and the QUALIFY predicate that the
        // block filters on after the aggregation.
        let (order_by, mut extra_projections) =
            self.resolve_order_by_aggregates(order_by, &projections, &schema_before)?;

        let projections: Vec<Expr> = projections
            .into_iter()
            .map(reduce_correlated_cols_in_group_context)
            .collect();

        // Note: HAVING is evaluated in the group context (`group_by().having(...)` for
        // ordinary grouping, a post-union filter for grouping sets), so any reference
        // to a SELECT alias is resolved to the aggregate it names.
        let mut having = having.map(|having_expr| {
            let having_expr = having_expr.map_expr(|e| match &e {
                Expr::Column(name) => resolve_select_alias(name, &projections, &schema_before)
                    .map_or(e, |resolved| strip_outer_alias(&resolved)),
                _ => e,
            });
            reduce_correlated_cols_in_group_context(having_expr)
        });

        // Resolve scalar subqueries in HAVING and the ORDER BY aggregates against the
        // pre-aggregation frame.
        let new_subquery_names;
        let mut exprs: Vec<&mut Expr> = extra_projections.iter_mut().map(|(_, e)| e).collect();
        exprs.extend(having.as_mut());
        (lf, new_subquery_names) = self.process_subqueries(lf, exprs, SubqueryShape::Scalar)?;
        if !new_subquery_names.is_empty() {
            let schema = self.get_frame_schema(&mut lf)?;
            let schema_before = Arc::make_mut(&mut schema_before);
            for name in &new_subquery_names {
                schema_before.with_column(name.clone(), schema.get(name).unwrap().clone());
            }
        }
        for e in extra_projections
            .iter_mut()
            .map(|(_, e)| e)
            .chain(having.as_mut())
        {
            *e = broadcast_subqueries_in_inputs(
                e.clone(),
                &new_subquery_names,
                &self.group_scope.subqueries_read_per_row,
            );
        }
        let mut subquery_names = subquery_names.clone();
        subquery_names.extend(new_subquery_names);

        extra_projections
            .extend(qualify.map(|(name, e)| (name, reduce_correlated_cols_in_group_context(e))));

        // Note: remove the `group_by` keys as Polars adds those implicitly.
        let mut aliased_aggregations: PlHashMap<PlSmallStr, PlSmallStr> = PlHashMap::new();
        let mut post_agg_projection: Vec<Expr> = Vec::new();
        let mut projection_overrides = PlHashMap::with_capacity(projections.len());
        let mut projection_aliases = PlHashSet::new();
        let mut group_key_aliases = PlHashSet::new();

        // Pre-compute group key data (alias-stripped expression + aggregated output
        // name) to avoid repeated work matching projections against the group keys
        let group_key_data: Vec<_> = group_by_keys
            .iter()
            .map(|gk| {
                (
                    strip_outer_alias(gk),
                    gk.to_field(&schema_before).ok().map(|f| f.name),
                )
            })
            .collect();

        // ORDER BY extras were parsed above and may have registered the partition.
        let whole_frame_partition = self.group_scope.whole_frame_partition.clone();
        let mut splitter = GroupContextSplitter {
            keys: &group_by_keys_schema,
            key_exprs: group_key_data
                .iter()
                .filter_map(|(key, name)| Some((key.clone(), name.clone()?)))
                .collect(),
            whole_frame_partition: whole_frame_partition.as_ref(),
            subquery_names: &subquery_names,
            subqueries_after_aggregation: grouping.is_none() && group_by_keys.is_empty(),
            subqueries_read_after: PlIndexSet::new(),
            aggregates: AggregateOutputs::with_capacity(projections.len()),
        };
        if let Some(having) = &having {
            splitter.check_columns_per_group(having)?;
        }
        // Post-aggregation expressions read computed keys from their stored columns.
        let bind_keys = |e: Expr| match grouping {
            Some(grouping) => grouping.bind_stored_keys(e, &key_schema),
            None => e,
        };

        let projection_group_key: Vec<Option<PlSmallStr>> = projections
            .iter()
            .map(|p| {
                let p_stripped = strip_outer_alias(p);
                group_key_data.iter().find_map(|(gk_stripped, gk_name)| {
                    (*gk_stripped == p_stripped)
                        .then(|| gk_name.clone())
                        .flatten()
                })
            })
            .collect();

        for (e, group_key) in projections.iter().zip(&projection_group_key) {
            let matches_group_key = group_key.is_some();
            let is_non_group_key_expr = !matches_group_key && splitter.requires_group_processing(e);

            // Note: if simple aliased expression we defer aliasing until after the group_by.
            // Use `e_inner` to track the potentially unwrapped expression for field lookup.
            let mut e_inner = e;
            if let Expr::Alias(expr, alias) = e {
                if e.clone().meta().is_simple_projection(Some(&schema_before)) {
                    group_key_aliases.insert(alias.as_ref());
                    e_inner = expr
                } else if let Expr::Function {
                    function: FunctionExpr::StructExpr(StructFunction::FieldByName(name)),
                    ..
                } = expr.deref()
                {
                    projection_overrides
                        .insert(alias.as_ref(), col(name.clone()).alias(alias.clone()));
                } else if !is_non_group_key_expr && !group_by_keys_schema.contains(alias) {
                    projection_aliases.insert(alias.as_ref());
                }
            }
            let field = e_inner.to_field(&schema_before)?;
            if is_non_group_key_expr {
                splitter.check_columns_per_group(e)?;
                // Window functions run on the aggregated frame; only the aggregates
                // inside them run in the group context. The same holds for anything
                // combining aggregates with grouped keys or `GROUPING()` values.
                let bound = bind_keys(strip_outer_alias(e));
                if splitter.needs_post_aggregation(&bound) {
                    let post_agg_expr = splitter.hoist(bound)?;
                    post_agg_projection.push(post_agg_expr.alias(field.name.clone()));
                    continue;
                }
                let mut e = e.clone();
                // If aggregation colname conflicts with a group key,
                // alias it to avoid duplicate/mis-tracked columns
                if group_by_keys_schema.get(&field.name).is_some() {
                    let alias_name = format_pl_smallstr!("__POLARS_AGG_{}", field.name);
                    e = e.alias(alias_name.clone());
                    aliased_aggregations.insert(field.name.clone(), alias_name);
                }
                splitter.aggregates.push(e);
            } else if !matches_group_key {
                // Non-aggregated columns must be part of the GROUP BY clause
                if let Expr::Column(_)
                | Expr::Function {
                    function: FunctionExpr::StructExpr(StructFunction::FieldByName(_)),
                    ..
                } = e_inner
                {
                    if !group_by_keys_schema.contains(&field.name) {
                        polars_bail!(SQLSyntax: "'{}' should participate in the GROUP BY clause or an aggregate function", &field.name);
                    }
                } else {
                    splitter.check_columns_per_group(e_inner)?;
                }
            }
        }

        for (name, e) in &extra_projections {
            let bound = bind_keys(strip_outer_alias(e));
            if splitter.needs_post_aggregation(&bound) {
                let rest = splitter.hoist(bound)?;
                post_agg_projection.push(rest.alias(name.clone()));
            } else {
                splitter.aggregates.push(e.clone());
            }
        }

        if let Some(grouping) = grouping {
            polars_ensure!(
                !splitter.aggregates.iter().any(|e| grouping.contains_placeholder(e)),
                SQLSyntax: "GROUPING() cannot be used inside an aggregate function"
            );
        }

        let aggregated = match grouping {
            None if group_by_keys.is_empty() => {
                // Without GROUP BY there is one aggregated row, which HAVING filters.
                let having = having.map(|having| splitter.hoist(having)).transpose()?;
                let mut aggregates = splitter.aggregates.into_exprs();
                // The row also exists when nothing is aggregated, as in `SELECT 1 ... HAVING`.
                if aggregates.is_empty() {
                    aggregates.push(len());
                }
                let mut aggregated = lf.select(aggregates);
                if !splitter.subqueries_read_after.is_empty() {
                    let mut frames = vec![aggregated];
                    frames.extend(
                        splitter
                            .subqueries_read_after
                            .iter()
                            .map(|name| self.group_scope.subquery_plans[name].clone()),
                    );
                    aggregated = concat_lf_horizontal(
                        frames,
                        HConcatOptions {
                            broadcast_unit_length: true,
                            ..Default::default()
                        },
                    )?;
                }
                match having {
                    Some(having) => aggregated.filter(having.cast(DataType::Boolean)),
                    None => aggregated,
                }
            },
            None => {
                // With a column key, every group has a row. A group-by on scalar keys only runs
                // as a select over all rows, which may be none.
                let has_column_key = group_by_keys
                    .iter()
                    .any(|key| matches!(strip_outer_alias(key), Expr::Column(_)));
                let in_groups = |e: Expr| {
                    if has_column_key {
                        assume_groups_have_rows(e)
                    } else {
                        e
                    }
                };
                let group_by = lf.group_by(group_by_keys);
                match having {
                    Some(having) => group_by.having(in_groups(strip_aggregate_marks(
                        splitter.read_keys_per_group(having),
                    ))),
                    None => group_by,
                }
                .agg(
                    splitter
                        .aggregates
                        .into_exprs()
                        .into_iter()
                        .map(in_groups)
                        .collect::<Vec<_>>(),
                )
            },
            Some(grouping) => {
                // HAVING runs on the combined rows, where it can also see `GROUPING()`.
                let having = having
                    .map(|having| {
                        let having = grouping.bind_stored_keys(having, &key_schema);
                        splitter.hoist(having)
                    })
                    .transpose()?;
                let aggregation_projection = splitter.aggregates.into_exprs();
                let agg_names = aggregation_projection
                    .iter()
                    .map(|e| Ok(e.to_field(&schema_before)?.name))
                    .collect::<PolarsResult<Vec<_>>>()?;
                let aggregated =
                    grouping.aggregate(lf, &key_schema, &aggregation_projection, &agg_names)?;
                match having {
                    Some(having) => aggregated.filter(having.cast(DataType::Boolean)),
                    None => aggregated,
                }
            },
        };

        let aggregated = if post_agg_projection.is_empty() {
            aggregated
        } else {
            aggregated.with_columns(&post_agg_projection)
        };

        let projection_schema =
            expressions_to_schema(&projections, &schema_before, |duplicate_name: &str| {
                format!("group_by aggregations contained duplicate output name '{duplicate_name}'")
            })?;

        // A final projection to get the proper order and any deferred transforms/aliases
        // (will also drop any temporary columns created for the HAVING post-filter)
        let final_projection = projection_schema
            .iter_names()
            .zip(projections.iter().zip(&projection_group_key))
            .map(|(name, (projection_expr, group_key))| {
                if let Some(expr) = projection_overrides.get(name.as_str()) {
                    expr.clone()
                } else if let Some(aliased_name) = aliased_aggregations.get(name) {
                    col(aliased_name.clone()).alias(name.clone())
                } else if let Some(key_name) = group_key {
                    // projection is a group key; reference aggregated key col rather than
                    // re-evaluating against aggregated frame (incorrect for computed keys)
                    if key_name == name {
                        col(name.clone())
                    } else {
                        col(key_name.clone()).alias(name.clone())
                    }
                } else if group_by_keys_schema.get(name).is_some()
                    || projection_aliases.contains(name.as_str())
                    || group_key_aliases.contains(name.as_str())
                {
                    if has_expr(projection_expr, |e| {
                        matches!(e, Expr::Agg(_) | Expr::Len | Expr::Over { .. })
                    }) {
                        col(name.clone())
                    } else {
                        bind_keys(projection_expr.clone())
                    }
                } else if is_constant(projection_expr) {
                    // Constants are not part of the aggregation; re-evaluate them.
                    projection_expr.clone()
                } else {
                    col(name.clone())
                }
            })
            .collect::<Vec<_>>();

        // Include original GROUP BY columns for ORDER BY access (if aliased).
        let mut output_projection = final_projection;
        let mut output_names: Vec<PlSmallStr> = projection_schema.iter_names_cloned().collect();
        let mut push_hidden = |expr: Expr, name: PlSmallStr| {
            output_projection.push(expr);
            output_names.push(name);
        };
        for (name, _) in &extra_projections {
            push_hidden(col(name.clone()), name.clone());
        }
        for key_name in group_by_keys_schema.iter_names() {
            if !projection_schema.contains(key_name) {
                // Original col name not in output - add for ORDER BY access
                push_hidden(col(key_name.clone()), key_name.clone());
            } else if group_by_keys.iter().any(|k| is_simple_col_ref(k, key_name)) {
                // Original col name in output - check if cross-aliased
                let is_cross_aliased = projection_schema
                    .iter_names()
                    .zip(projections.iter())
                    .any(|(name, p)| name == key_name && !is_simple_col_ref(p, key_name));
                if is_cross_aliased {
                    // Add original name under a prefixed alias for subsequent ORDER BY resolution
                    let internal_name = format_pl_smallstr!("__POLARS_ORIG_{}", key_name);
                    push_hidden(
                        col(key_name.clone()).alias(internal_name.clone()),
                        internal_name,
                    );
                }
            }
        }
        // A literal-only projection (`SELECT 1 ... GROUP BY ()` or `SELECT 1 ... HAVING`)
        // must keep the height of the aggregated rows, so the columns are added before the
        // frame is narrowed.
        let projected = if grouping.is_some() || group_by_keys.is_empty() {
            aggregated
                .with_columns(&output_projection)
                .select(output_names.into_iter().map(col).collect::<Vec<_>>())
        } else {
            aggregated.select(&output_projection)
        };
        Ok((
            projected,
            projection_schema.iter_names_cloned().collect(),
            order_by,
        ))
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn process_group_by(
        &mut self,
        mut lf: LazyFrame,
        group_by_keys: &[Expr],
        projections: Vec<Expr>,
        explicit_aliases: &[bool],
        having: Option<Expr>,
        qualify: Option<(PlSmallStr, Expr)>,
        order_by: &Option<OrderBy>,
        grouping: Option<&GroupingSets>,
        subquery_names: &PlHashSet<PlSmallStr>,
    ) -> PolarsResult<(LazyFrame, Vec<PlSmallStr>, Option<OrderBy>)> {
        // Ordinary grouping stores each computed key in a hidden column. The other
        // expressions read that column, as the key's output name can be taken by
        // an input column or by another key.
        let mut stored_keys: Vec<(Expr, PlSmallStr)> = Vec::new();
        let column_keys: Vec<Expr>;
        let group_by_keys = if grouping.is_none() {
            let mut prepared = Vec::new();
            column_keys = group_by_keys
                .iter()
                .map(|key| {
                    let stripped = strip_outer_alias(key);
                    if matches!(stripped, Expr::Column(_)) || is_constant(&stripped) {
                        return key.clone();
                    }
                    let name = unique_column_name();
                    prepared.push(stripped.clone().alias(name.clone()));
                    stored_keys.push((stripped, name.clone()));
                    col(name)
                })
                .collect();
            if !prepared.is_empty() {
                lf = lf.with_columns(prepared);
            }
            &column_keys[..]
        } else {
            group_by_keys
        };
        let mut schema_before = self.get_frame_schema(&mut lf)?;
        let key_schema =
            expressions_to_schema(group_by_keys, &schema_before, |duplicate_name: &str| {
                format!("group_by keys contained duplicate output name '{duplicate_name}'")
            })?;
        if let Some(grouping) = grouping {
            stored_keys = grouping.stored_keys(&key_schema);
        }
        let mut group_by_keys_schema = key_schema.clone();
        // Columns the parsed expressions may name before the aggregation resolves them:
        // the whole-frame window partition, and `GROUPING()` values, which are
        // per-set constants the projections treat like group keys.
        let whole_frame_partition = self.group_scope.whole_frame_partition.clone();
        let placeholders: Vec<PlSmallStr> = grouping
            .map(|g| g.placeholders().cloned().collect())
            .unwrap_or_default();
        if whole_frame_partition.is_some() || !placeholders.is_empty() {
            let mut extended = Arc::unwrap_or_clone(schema_before);
            if let Some(partition) = &whole_frame_partition {
                extended.with_column(partition.clone(), DataType::Int32);
            }
            for placeholder in &placeholders {
                extended.with_column(placeholder.clone(), DataType::Int64);
                group_by_keys_schema.with_column(placeholder.clone(), DataType::Int64);
            }
            schema_before = Arc::new(extended);
        }

        // Disambiguate SELECT-list output-name collisions.
        let projections = disambiguate_output_names(
            projections
                .into_iter()
                .zip(explicit_aliases.iter().copied())
                .collect(),
            &schema_before,
        )?;
        // Hidden output columns: the ORDER BY items with aggregates or computed keys, and
        // the QUALIFY predicate that the block filters on after the aggregation.
        let (order_by, mut extra_projections) =
            self.resolve_order_by_aggregates(order_by, &projections, &schema_before, &stored_keys)?;
        let projections = if grouping.is_none() && !stored_keys.is_empty() {
            projections
                .into_iter()
                .map(|p| {
                    let stripped = strip_outer_alias(&p);
                    let bound = bind_stored_keys(stripped.clone(), &stored_keys);
                    Ok(if bound == stripped {
                        p
                    } else {
                        bound.alias(p.to_field(&schema_before)?.name)
                    })
                })
                .collect::<PolarsResult<Vec<_>>>()?
        } else {
            projections
        };

        let projections: Vec<Expr> = projections
            .into_iter()
            .map(reduce_correlated_cols_in_group_context)
            .collect();

        // Note: HAVING is evaluated in the group context (`group_by().having(...)` for
        // ordinary grouping, a post-union filter for grouping sets), so any reference
        // to a SELECT alias is resolved to the aggregate it names.
        let mut having = having.map(|having_expr| {
            let having_expr = having_expr.map_expr(|e| match &e {
                Expr::Column(name) => resolve_select_alias(name, &projections, &schema_before)
                    .map_or(e, |resolved| strip_outer_alias(&resolved)),
                _ => e,
            });
            let having_expr = match grouping {
                // Grouping sets bind the keys once HAVING runs on the combined rows.
                Some(_) => having_expr,
                None => bind_stored_keys(having_expr, &stored_keys),
            };
            reduce_correlated_cols_in_group_context(having_expr)
        });

        // Resolve scalar subqueries in HAVING and the ORDER BY aggregates against the
        // pre-aggregation frame.
        let new_subquery_names;
        let mut exprs: Vec<&mut Expr> = extra_projections.iter_mut().map(|(_, e)| e).collect();
        exprs.extend(having.as_mut());
        (lf, new_subquery_names) = self.process_subqueries(lf, exprs, SubqueryShape::Scalar)?;
        if !new_subquery_names.is_empty() {
            let schema = self.get_frame_schema(&mut lf)?;
            let schema_before = Arc::make_mut(&mut schema_before);
            for name in &new_subquery_names {
                schema_before.with_column(name.clone(), schema.get(name).unwrap().clone());
            }
        }
        for e in extra_projections
            .iter_mut()
            .map(|(_, e)| e)
            .chain(having.as_mut())
        {
            *e = broadcast_subqueries_in_inputs(
                e.clone(),
                &new_subquery_names,
                &self.group_scope.subqueries_read_per_row,
            );
        }
        let mut subquery_names = subquery_names.clone();
        subquery_names.extend(new_subquery_names);

        extra_projections
            .extend(qualify.map(|(name, e)| (name, reduce_correlated_cols_in_group_context(e))));

        // Note: remove the `group_by` keys as Polars adds those implicitly.
        let mut aliased_aggregations: PlHashMap<PlSmallStr, PlSmallStr> = PlHashMap::new();
        let mut post_agg_projection: Vec<Expr> = Vec::new();
        let mut projection_overrides = PlHashMap::with_capacity(projections.len());
        let mut projection_aliases = PlHashSet::new();
        let mut group_key_aliases = PlHashSet::new();

        // Pre-compute group key data (alias-stripped expression + aggregated output
        // name) to avoid repeated work matching projections against the group keys
        let group_key_data: Vec<_> = group_by_keys
            .iter()
            .map(|gk| {
                (
                    strip_outer_alias(gk),
                    gk.to_field(&schema_before).ok().map(|f| f.name),
                )
            })
            .collect();

        // ORDER BY extras were parsed above and may have registered the partition.
        let whole_frame_partition = self.group_scope.whole_frame_partition.clone();
        let mut splitter = GroupContextSplitter {
            keys: &group_by_keys_schema,
            key_exprs: group_key_data
                .iter()
                .filter_map(|(key, name)| Some((key.clone(), name.clone()?)))
                .chain(match grouping {
                    Some(_) => vec![],
                    None => stored_keys.clone(),
                })
                .collect(),
            whole_frame_partition: whole_frame_partition.as_ref(),
            subquery_names: &subquery_names,
            subqueries_after_aggregation: grouping.is_none() && group_by_keys.is_empty(),
            subqueries_read_after: PlIndexSet::new(),
            aggregates: AggregateOutputs::with_capacity(projections.len()),
        };
        if let Some(having) = &having {
            splitter.check_columns_per_group(having)?;
        }
        // Post-aggregation expressions read computed keys from their stored columns.
        let bind_keys = |e: Expr| bind_stored_keys(e, &stored_keys);

        let projection_group_key: Vec<Option<PlSmallStr>> = projections
            .iter()
            .map(|p| {
                let p_stripped = strip_outer_alias(p);
                group_key_data.iter().find_map(|(gk_stripped, gk_name)| {
                    (*gk_stripped == p_stripped)
                        .then(|| gk_name.clone())
                        .flatten()
                })
            })
            .collect();

        for (e, group_key) in projections.iter().zip(&projection_group_key) {
            let matches_group_key = group_key.is_some();
            let is_non_group_key_expr = !matches_group_key && splitter.requires_group_processing(e);

            // Note: if simple aliased expression we defer aliasing until after the group_by.
            // Use `e_inner` to track the potentially unwrapped expression for field lookup.
            let mut e_inner = e;
            if let Expr::Alias(expr, alias) = e {
                if e.clone().meta().is_simple_projection(Some(&schema_before)) {
                    group_key_aliases.insert(alias.as_ref());
                    e_inner = expr
                } else if let Expr::Function {
                    function: FunctionExpr::StructExpr(StructFunction::FieldByName(name)),
                    ..
                } = expr.deref()
                {
                    projection_overrides
                        .insert(alias.as_ref(), col(name.clone()).alias(alias.clone()));
                } else if !is_non_group_key_expr && !group_by_keys_schema.contains(alias) {
                    projection_aliases.insert(alias.as_ref());
                }
            }
            let field = e_inner.to_field(&schema_before)?;
            if is_non_group_key_expr {
                splitter.check_columns_per_group(e)?;
                // Window functions run on the aggregated frame; only the aggregates
                // inside them run in the group context. The same holds for anything
                // combining aggregates with grouped keys or `GROUPING()` values.
                let bound = bind_keys(strip_outer_alias(e));
                if splitter.needs_post_aggregation(&bound) {
                    let post_agg_expr = splitter.hoist(bound)?;
                    post_agg_projection.push(post_agg_expr.alias(field.name.clone()));
                    continue;
                }
                let mut e = e.clone();
                // If aggregation colname conflicts with a group key,
                // alias it to avoid duplicate/mis-tracked columns
                if group_by_keys_schema.get(&field.name).is_some() {
                    let alias_name = format_pl_smallstr!("__POLARS_AGG_{}", field.name);
                    e = e.alias(alias_name.clone());
                    aliased_aggregations.insert(field.name.clone(), alias_name);
                }
                splitter.aggregates.push(e);
            } else if !matches_group_key {
                // Non-aggregated columns must be part of the GROUP BY clause
                if let Expr::Column(_)
                | Expr::Function {
                    function: FunctionExpr::StructExpr(StructFunction::FieldByName(_)),
                    ..
                } = e_inner
                {
                    if !group_by_keys_schema.contains(&field.name) {
                        polars_bail!(SQLSyntax: "'{}' should participate in the GROUP BY clause or an aggregate function", &field.name);
                    }
                } else {
                    splitter.check_columns_per_group(e_inner)?;
                }
            }
        }

        for (name, e) in &extra_projections {
            let bound = bind_keys(strip_outer_alias(e));
            if splitter.needs_post_aggregation(&bound) {
                let rest = splitter.hoist(bound)?;
                post_agg_projection.push(rest.alias(name.clone()));
            } else if !splitter.requires_group_processing(&bound) {
                post_agg_projection.push(bound.alias(name.clone()));
            } else {
                splitter.aggregates.push(e.clone());
            }
        }

        if let Some(grouping) = grouping {
            polars_ensure!(
                !splitter.aggregates.iter().any(|e| grouping.contains_placeholder(e)),
                SQLSyntax: "GROUPING() cannot be used inside an aggregate function"
            );
        }

        let aggregated = match grouping {
            None if group_by_keys.is_empty() => {
                // Without GROUP BY there is one aggregated row, which HAVING filters.
                let having = having.map(|having| splitter.hoist(having)).transpose()?;
                let mut aggregates = splitter.aggregates.into_exprs();
                // The row also exists when nothing is aggregated, as in `SELECT 1 ... HAVING`.
                if aggregates.is_empty() {
                    aggregates.push(len());
                }
                let mut aggregated = lf.select(aggregates);
                if !splitter.subqueries_read_after.is_empty() {
                    let mut frames = vec![aggregated];
                    frames.extend(
                        splitter
                            .subqueries_read_after
                            .iter()
                            .map(|name| self.group_scope.subquery_plans[name].clone()),
                    );
                    aggregated = concat_lf_horizontal(
                        frames,
                        HConcatOptions {
                            broadcast_unit_length: true,
                            ..Default::default()
                        },
                    )?;
                }
                match having {
                    Some(having) => aggregated.filter(having.cast(DataType::Boolean)),
                    None => aggregated,
                }
            },
            None => {
                // With a column key, every group has a row. A group-by on scalar keys only runs
                // as a select over all rows, which may be none.
                let has_column_key = group_by_keys
                    .iter()
                    .any(|key| matches!(strip_outer_alias(key), Expr::Column(_)));
                let in_groups = |e: Expr| {
                    if has_column_key {
                        assume_groups_have_rows(e)
                    } else {
                        e
                    }
                };
                let group_by = lf.group_by(group_by_keys);
                match having {
                    Some(having) => group_by.having(in_groups(strip_aggregate_marks(
                        splitter.read_keys_per_group(having),
                    ))),
                    None => group_by,
                }
                .agg(
                    splitter
                        .aggregates
                        .into_exprs()
                        .into_iter()
                        .map(in_groups)
                        .collect::<Vec<_>>(),
                )
            },
            Some(grouping) => {
                // HAVING runs on the combined rows, where it can also see `GROUPING()`.
                let having = having
                    .map(|having| {
                        let having = bind_stored_keys(having, &stored_keys);
                        splitter.hoist(having)
                    })
                    .transpose()?;
                let aggregation_projection = splitter.aggregates.into_exprs();
                let agg_names = aggregation_projection
                    .iter()
                    .map(|e| Ok(e.to_field(&schema_before)?.name))
                    .collect::<PolarsResult<Vec<_>>>()?;
                let aggregated =
                    grouping.aggregate(lf, &key_schema, &aggregation_projection, &agg_names)?;
                match having {
                    Some(having) => aggregated.filter(having.cast(DataType::Boolean)),
                    None => aggregated,
                }
            },
        };

        let aggregated = if post_agg_projection.is_empty() {
            aggregated
        } else {
            aggregated.with_columns(&post_agg_projection)
        };

        let projection_schema =
            expressions_to_schema(&projections, &schema_before, |duplicate_name: &str| {
                format!("group_by aggregations contained duplicate output name '{duplicate_name}'")
            })?;

        // A final projection to get the proper order and any deferred transforms/aliases
        // (will also drop any temporary columns created for the HAVING post-filter)
        let final_projection = projection_schema
            .iter_names()
            .zip(projections.iter().zip(&projection_group_key))
            .map(|(name, (projection_expr, group_key))| {
                if let Some(expr) = projection_overrides.get(name.as_str()) {
                    expr.clone()
                } else if let Some(aliased_name) = aliased_aggregations.get(name) {
                    col(aliased_name.clone()).alias(name.clone())
                } else if let Some(key_name) = group_key {
                    // projection is a group key; reference aggregated key col rather than
                    // re-evaluating against aggregated frame (incorrect for computed keys)
                    if key_name == name {
                        col(name.clone())
                    } else {
                        col(key_name.clone()).alias(name.clone())
                    }
                } else if group_by_keys_schema.get(name).is_some()
                    || projection_aliases.contains(name.as_str())
                    || group_key_aliases.contains(name.as_str())
                {
                    if has_expr(projection_expr, |e| {
                        matches!(e, Expr::Agg(_) | Expr::Len | Expr::Over { .. })
                    }) {
                        col(name.clone())
                    } else {
                        bind_keys(projection_expr.clone())
                    }
                } else if is_constant(projection_expr) {
                    // Constants are not part of the aggregation; re-evaluate them.
                    projection_expr.clone()
                } else {
                    col(name.clone())
                }
            })
            .collect::<Vec<_>>();

        // Include original GROUP BY columns for ORDER BY access (if aliased).
        let mut output_projection = final_projection;
        let mut output_names: Vec<PlSmallStr> = projection_schema.iter_names_cloned().collect();
        let mut push_hidden = |expr: Expr, name: PlSmallStr| {
            output_projection.push(expr);
            output_names.push(name);
        };
        for (name, _) in &extra_projections {
            push_hidden(col(name.clone()), name.clone());
        }
        for key_name in group_by_keys_schema.iter_names() {
            if !projection_schema.contains(key_name) {
                // Original col name not in output - add for ORDER BY access
                push_hidden(col(key_name.clone()), key_name.clone());
            } else if group_by_keys.iter().any(|k| is_simple_col_ref(k, key_name)) {
                // Original col name in output - check if cross-aliased
                let is_cross_aliased = projection_schema
                    .iter_names()
                    .zip(projections.iter())
                    .any(|(name, p)| name == key_name && !is_simple_col_ref(p, key_name));
                if is_cross_aliased {
                    // Add original name under a prefixed alias for subsequent ORDER BY resolution
                    let internal_name = format_pl_smallstr!("__POLARS_ORIG_{}", key_name);
                    push_hidden(
                        col(key_name.clone()).alias(internal_name.clone()),
                        internal_name,
                    );
                }
            }
        }
        // A literal-only projection (`SELECT 1 ... GROUP BY ()` or `SELECT 1 ... HAVING`)
        // must keep the height of the aggregated rows, so the columns are added before the
        // frame is narrowed.
        let projected = if grouping.is_some() || group_by_keys.is_empty() {
            aggregated
                .with_columns(&output_projection)
                .select(output_names.into_iter().map(col).collect::<Vec<_>>())
        } else {
            aggregated.select(&output_projection)
        };
        Ok((
            projected,
            projection_schema.iter_names_cloned().collect(),
            order_by,
        ))
    }
```

### 🔹 函式: `SQLContext::resolve_order_by_aggregates()`
- **變更前簽章 (Before)**: `fn SQLContext::resolve_order_by_aggregates(
        &mut self,
        order_by: &Option<OrderBy>,
        projections: &[Expr],
        schema: &Schema,
    )` (L3421~L3463)
- **變更後簽章 (After)**: `fn SQLContext::resolve_order_by_aggregates(
        &mut self,
        order_by: &Option<OrderBy>,
        projections: &[Expr],
        schema: &Schema,
        stored_keys: &[(Expr, PlSmallStr)],
    )` (L3432~L3477)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn resolve_order_by_aggregates(
        &mut self,
        order_by: &Option<OrderBy>,
        projections: &[Expr],
        schema: &Schema,
    ) -> PolarsResult<ResolvedOrderBy> {
        let mut clause = order_by.clone();
        let mut extra: Vec<(PlSmallStr, Expr)> = Vec::new();

        if let Some(OrderBy {
            kind: OrderByKind::Expressions(exprs),
            ..
        }) = &mut clause
        {
            let output_names = OutputNames::new(projections, schema, schema);
            let output_schema = output_names.extend_schema(schema);
            for ob in exprs {
                // Anything without an aggregate already resolves against the
                // aggregated frame.
                let Ok(parsed) = self
                    .marking_aggregates(|ctx| parse_sql_expr(&ob.expr, ctx, Some(&output_schema)))
                else {
                    continue;
                };
                if !has_expr(&parsed, |e| {
                    is_marked_aggregate(e) || matches!(e, Expr::Agg(_) | Expr::Len)
                }) {
                    continue;
                }
                let parsed = output_names.resolve(strip_outer_alias(&parsed));
                let name = match projections.iter().find(|p| strip_outer_alias(p) == parsed) {
                    Some(projection) => projection.to_field(schema)?.name,
                    None => {
                        let name = format_pl_smallstr!("__POLARS_ORDERAGG_{}", extra.len());
                        extra.push((name.clone(), parsed.alias(name.clone())));
                        name
                    },
                };
                ob.expr = SQLExpr::Identifier(Ident::new(name.as_str()));
            }
        }
        Ok((clause, extra))
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn resolve_order_by_aggregates(
        &mut self,
        order_by: &Option<OrderBy>,
        projections: &[Expr],
        schema: &Schema,
        stored_keys: &[(Expr, PlSmallStr)],
    ) -> PolarsResult<ResolvedOrderBy> {
        let mut clause = order_by.clone();
        let mut extra: Vec<(PlSmallStr, Expr)> = Vec::new();

        if let Some(OrderBy {
            kind: OrderByKind::Expressions(exprs),
            ..
        }) = &mut clause
        {
            let output_names = OutputNames::new(projections, schema, schema);
            let output_schema = output_names.extend_schema(schema);
            for ob in exprs {
                // Anything without an aggregate or a computed key already resolves
                // against the aggregated frame.
                let Ok(parsed) = self
                    .marking_aggregates(|ctx| parse_sql_expr(&ob.expr, ctx, Some(&output_schema)))
                else {
                    continue;
                };
                if !has_expr(&parsed, |e| {
                    is_marked_aggregate(e)
                        || matches!(e, Expr::Agg(_) | Expr::Len)
                        || stored_keys.iter().any(|(key, _)| key == e)
                }) {
                    continue;
                }
                let parsed = output_names.resolve(strip_outer_alias(&parsed));
                let name = match projections.iter().find(|p| strip_outer_alias(p) == parsed) {
                    Some(projection) => projection.to_field(schema)?.name,
                    None => {
                        let name = format_pl_smallstr!("__POLARS_ORDERAGG_{}", extra.len());
                        extra.push((name.clone(), parsed.alias(name.clone())));
                        name
                    },
                };
                ob.expr = SQLExpr::Identifier(Ident::new(name.as_str()));
            }
        }
        Ok((clause, extra))
    }
```

### 🔹 函式: `SQLContext::execute_select_block()`
- **變更前簽章 (Before)**: `fn SQLContext::execute_select_block(
        &mut self,
        select_stmt: &Select,
        query: &Query,
    )` (L1820~L2392)
- **變更後簽章 (After)**: `fn SQLContext::execute_select_block(
        &mut self,
        select_stmt: &Select,
        query: &Query,
    )` (L1820~L2403)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn execute_select_block(
        &mut self,
        select_stmt: &Select,
        query: &Query,
    ) -> PolarsResult<LazyFrame> {
        // Check that the statement doesn't contain unsupported SELECT clauses
        self.validate_select(select_stmt)?;

        // Parse named windows first, as they may be referenced in the SELECT clause
        self.register_named_windows(&select_stmt.named_window)?;

        // Get `FROM` table/data
        let mut implicit_join_filter: Option<SQLExpr> = None;
        let mut lf = if select_stmt.from.is_empty() {
            self.active_relations.clear();
            DataFrame::new(1, vec![])?.lazy()
        } else {
            let from = &select_stmt.from;
            let first = from.first().unwrap();
            // Set before the relations are resolved, so a join constraint
            // resolves against them.
            self.active_relations = declared_relations(from);
            let mut lf = self.execute_from_statement(first)?;
            if from.len() > 1 {
                implicit_join_filter =
                    self.process_implicit_joins(&mut lf, from, &select_stmt.selection)?;
            }
            lf
        };

        self.set_join_base(&select_stmt.from);
        self.check_select_column_refs(select_stmt)?;

        // Apply `WHERE` constraint (using residual filter for implicit joins)
        let where_expr = if implicit_join_filter.is_some() {
            implicit_join_filter.as_ref()
        } else {
            select_stmt.selection.as_ref()
        };
        let mut schema = self.get_frame_schema(&mut lf)?;

        // Shared by every pass over this frame: WHERE, the projection list and HAVING.
        let mut bindings = SubqueryBindings::new();

        // A correlated scalar subquery is lowered against the frame as it stands, so
        // the conjuncts that don't need it are applied first: the lowering can then
        // restrict its aggregate to the rows that survive them.
        let mut join_tree = None;
        let where_expr: Option<Cow<'_, SQLExpr>> = match where_expr {
            Some(where_expr) if expr_contains_scalar_subquery(where_expr) => {
                let n_grouping_calls = self.group_scope.grouping_calls.len();
                let residual;
                (lf, residual) = self.rewrite_subquery_conjuncts(
                    lf,
                    where_expr,
                    FilterMode::KeepTrue,
                    &schema,
                    RewriteStage::BeforeScalarLowering,
                )?;
                self.reject_grouping_in_where(n_grouping_calls)?;
                join_tree = self.outer_join_tree(select_stmt, where_expr, &residual)?;
                schema = self.get_frame_schema(&mut lf)?;
                combine_conditions(
                    residual.into_iter().cloned().collect(),
                    SQLBinaryOperator::And,
                )
                .map(Cow::Owned)
            },
            other => other.map(Cow::Borrowed),
        };

        // Lower correlated scalar subqueries in the WHERE clause before the filter is
        // parsed, leaving `[NOT] EXISTS` to `process_where`.
        let effective_where = match where_expr.as_deref() {
            Some(where_expr) => {
                let lowered;
                (lf, lowered) = self.lower_correlated_subqueries(
                    lf,
                    &schema,
                    where_expr,
                    LowerScope::ScalarOnly,
                    &mut bindings,
                    join_tree.as_ref(),
                )?;
                if matches!(lowered, Cow::Owned(_)) {
                    schema = self.get_frame_schema(&mut lf)?;
                }
                Some(lowered)
            },
            None => None,
        };

        lf = self.process_where(
            lf,
            effective_where.as_deref(),
            FilterMode::KeepTrue,
            Some(schema.clone()),
        )?;

        // HAVING is parsed further below but lowered here, against the pre-aggregation
        // frame.
        let mut lowered_projection: Option<Vec<SelectItem>> = None;
        let mut lowered_having: Option<Cow<'_, SQLExpr>> = None;
        {
            let mut changed = false;
            for (idx, item) in select_stmt.projection.iter().enumerate() {
                let (SelectItem::UnnamedExpr(e) | SelectItem::ExprWithAlias { expr: e, .. }) = item
                else {
                    continue;
                };
                let lowered;
                (lf, lowered) = self.lower_correlated_subqueries(
                    lf,
                    &schema,
                    e,
                    LowerScope::ScalarAndPredicates,
                    &mut bindings,
                    None,
                )?;
                if let Cow::Owned(lowered) = lowered {
                    changed = true;
                    let items =
                        lowered_projection.get_or_insert_with(|| select_stmt.projection.clone());
                    match &mut items[idx] {
                        SelectItem::UnnamedExpr(slot)
                        | SelectItem::ExprWithAlias { expr: slot, .. } => *slot = lowered,
                        _ => unreachable!("only expression items are lowered"),
                    }
                }
            }
            if let Some(having) = &select_stmt.having {
                let lowered;
                (lf, lowered) = self.lower_correlated_subqueries(
                    lf,
                    &schema,
                    having,
                    LowerScope::ScalarAndPredicates,
                    &mut bindings,
                    None,
                )?;
                changed |= matches!(lowered, Cow::Owned(_));
                lowered_having = Some(lowered);
            }
            if changed {
                schema = self.get_frame_schema(&mut lf)?;
            }
        }
        let projection: &[SelectItem] = lowered_projection
            .as_deref()
            .unwrap_or(&select_stmt.projection);

        if let Some(qualify) = &select_stmt.qualify {
            check_qualify(qualify, &select_stmt.projection)?;
        }

        let mark_whole_frame_windows =
            std::mem::replace(&mut self.group_scope.mark_whole_frame_windows, true);
        let mut projections_with_flags = self.marking_aggregates(|ctx| {
            ctx.column_projections(projection, select_stmt.flavor, &schema)
        })?;
        self.group_scope.mark_whole_frame_windows = mark_whole_frame_windows;
        let mut subquery_names;
        (lf, subquery_names) = self.process_subqueries(
            lf,
            projections_with_flags.iter_mut().map(|(e, _)| e).collect(),
            SubqueryShape::Scalar,
        )?;
        for (expr, _) in projections_with_flags.iter_mut() {
            *expr = broadcast_subqueries_in_inputs(
                expr.clone(),
                &subquery_names,
                &self.group_scope.subqueries_read_per_row,
            );
        }
        schema = self.get_frame_schema(&mut lf)?;

        // Placeholder names are generated per execution, so an unaliased projection
        // named after one gets the name given to any other unnamed scalar expression.
        // Matching on the output name rather than the expression shape also catches
        // projections that merely derive their name from a placeholder.
        if !subquery_names.is_empty() {
            for (expr, is_explicit_alias) in projections_with_flags.iter_mut() {
                if *is_explicit_alias {
                    continue;
                }
                let is_placeholder_name = expr
                    .to_field(&schema)
                    .is_ok_and(|f| subquery_names.contains(&f.name));
                if is_placeholder_name {
                    *expr = expr.clone().alias(PlSmallStr::from_static("literal"));
                }
            }
        }

        // QUALIFY filters on windows over the rows the SELECT list reads, so it is computed
        // with the SELECT list, as a hidden column. It can name SELECT aliases, which read the
        // subqueries of the SELECT list resolved above.
        let qualify_column = format_pl_smallstr!("__POLARS_QUALIFY_{}", unique_column_name());
        let mut qualify = match &select_stmt.qualify {
            Some(qualify) => {
                let projections: Vec<Expr> = projections_with_flags
                    .iter()
                    .map(|(e, _)| e.clone())
                    .collect();
                let output_names = OutputNames::new(
                    &projections,
                    &schema,
                    &self.with_placeholder_columns(&schema),
                );
                let output_schema = output_names.extend_schema(&schema);
                let mark_whole_frame_windows =
                    std::mem::replace(&mut self.group_scope.mark_whole_frame_windows, true);
                let parsed = self
                    .marking_aggregates(|ctx| parse_sql_expr(qualify, ctx, Some(&output_schema)));
                self.group_scope.mark_whole_frame_windows = mark_whole_frame_windows;
                let mut qualify = output_names.resolve(parsed?);
                if qualify.clone().meta().has_multiple_outputs() {
                    qualify = all_horizontal([qualify])?;
                }
                let qualify_subquery_names;
                (lf, qualify_subquery_names) =
                    self.process_subqueries(lf, vec![&mut qualify], SubqueryShape::Scalar)?;
                if !qualify_subquery_names.is_empty() {
                    subquery_names.extend(qualify_subquery_names);
                    schema = self.get_frame_schema(&mut lf)?;
                }
                let qualify = broadcast_subqueries_in_inputs(
                    qualify,
                    &subquery_names,
                    &self.group_scope.subqueries_read_per_row,
                );
                Some(qualify.alias(qualify_column.clone()))
            },
            None => None,
        };

        let (mut projections, mut explicit_aliases): (Vec<Expr>, Vec<bool>) =
            projections_with_flags.into_iter().unzip();

        // Apply `UNNEST` expressions
        let mut explode_names = Vec::new();
        let mut explode_exprs = Vec::new();
        let mut explode_lookup = PlHashMap::new();

        for expr in &projections {
            for e in expr {
                if let Expr::Explode { input, .. } = e {
                    match input.as_ref() {
                        Expr::Column(name) => explode_names.push(name.clone()),
                        other_expr => {
                            // Note: skip aggregate expressions; those are handled in the GROUP BY phase
                            if !has_expr(other_expr, |e| matches!(e, Expr::Agg(_) | Expr::Len)) {
                                let temp_name =
                                    format_pl_smallstr!("__POLARS_UNNEST_{}", explode_exprs.len());
                                explode_exprs.push(other_expr.clone().alias(temp_name.as_str()));
                                explode_lookup.insert(other_expr.clone(), temp_name.clone());
                                explode_names.push(temp_name);
                            }
                        },
                    }
                }
            }
        }
        if !explode_names.is_empty() {
            if !explode_exprs.is_empty() {
                lf = lf.with_columns(explode_exprs);
            }
            lf = lf.explode(
                Selector::ByName {
                    names: Arc::from(explode_names),
                    strict: true,
                },
                ExplodeOptions {
                    empty_as_null: true,
                    keep_nulls: true,
                },
            );
            projections = projections
                .into_iter()
                .map(|p| {
                    // Update "projections" with column refs to the now-exploded expressions
                    p.map_expr(|e| match e {
                        Expr::Explode { input, .. } => explode_lookup
                            .get(input.as_ref())
                            .map(|name| Expr::Column(name.clone()))
                            .unwrap_or_else(|| input.as_ref().clone()),
                        _ => e,
                    })
                })
                .collect();

            schema = self.get_frame_schema(&mut lf)?;
        }

        // Check for "GROUP BY ..." (after determining projections)
        let mut group_by_keys: Vec<Expr> = Vec::new();
        let mut grouping_sets: Option<Vec<Vec<usize>>> = None;
        match &select_stmt.group_by {
            // Standard "GROUP BY x, y, z" syntax (also recognising ordinal values)
            GroupByExpr::Expressions(group_by_exprs, modifiers) => {
                if !modifiers.is_empty() {
                    polars_bail!(SQLInterface: "GROUP BY does not support CUBE, ROLLUP, or TOTALS modifiers")
                }
                let expanded = expand_grouping_sets(group_by_exprs)?;
                let key_exprs: &[SQLExpr] = expanded
                    .as_ref()
                    .map_or(group_by_exprs, |expanded| &expanded.keys);
                // Translate the group expressions, resolving ordinal values and SELECT aliases
                group_by_keys = key_exprs
                    .iter()
                    .map(|e| self.resolve_group_by_key(e, &projections, &schema, true))
                    .collect::<PolarsResult<_>>()?;
                if let Some(expanded) = expanded {
                    let (keys, sets) = canonicalize_keys(group_by_keys, expanded.sets);
                    group_by_keys = keys;
                    grouping_sets = Some(sets);
                }
            },
            // "GROUP BY ALL" syntax; automatically adds expressions that do not contain
            // nested agg/window funcs to the group key (also ignores literals).
            GroupByExpr::All(modifiers) => {
                if !modifiers.is_empty() {
                    polars_bail!(SQLInterface: "GROUP BY does not support CUBE, ROLLUP, or TOTALS modifiers")
                }
                projections.iter().for_each(|expr| match expr {
                    // immediately match the most common cases (col|agg|len|lit, optionally aliased).
                    Expr::Agg(_) | Expr::Len | Expr::Literal(_) => (),
                    _ if self.contains_grouping_placeholder(expr) => (),
                    Expr::Column(_) => group_by_keys.push(expr.clone()),
                    Expr::Alias(e, _)
                        if matches!(&**e, Expr::Agg(_) | Expr::Len | Expr::Literal(_)) => {},
                    Expr::Alias(e, _) if matches!(&**e, Expr::Column(_)) => {
                        if let Expr::Column(name) = &**e {
                            group_by_keys.push(col(name.clone()));
                        }
                    },
                    _ => {
                        // If not quick-matched, add if no nested agg/window expressions
                        if !has_expr(expr, |e| {
                            is_marked_aggregate(e)
                                || matches!(e, Expr::Agg(_))
                                || matches!(e, Expr::Len)
                                || matches!(e, Expr::Over { .. })
                                || {
                                    #[cfg(feature = "dynamic_group_by")]
                                    {
                                        matches!(e, Expr::Rolling { .. })
                                    }
                                    #[cfg(not(feature = "dynamic_group_by"))]
                                    {
                                        false
                                    }
                                }
                        }) {
                            group_by_keys.push(expr.clone())
                        }
                    },
                });
            },
        };
        for e in &group_by_keys {
            reject_unresolved_subquery(e, "GROUP BY")?;
            polars_ensure!(
                !self.contains_grouping_placeholder(e),
                SQLSyntax: "GROUPING() is not allowed in the GROUP BY clause"
            );
        }

        let has_group_by = !group_by_keys.is_empty() || grouping_sets.is_some();
        if !has_group_by {
            polars_ensure!(
                self.group_scope.grouping_calls.is_empty(),
                SQLSyntax: "GROUPING() requires a GROUP BY clause"
            );
        }
        // Without GROUP BY, a block with aggregates or HAVING is one group, and its windows
        // and the subqueries outside its aggregates run on that one row.
        let all_projections = projections
            .iter()
            .chain(&qualify)
            .cloned()
            .collect::<Vec<_>>();
        lf = if !has_group_by
            && lowered_having.is_none()
            && !has_windows_over_aggregates(&all_projections)
            && !has_subquery_outside_aggregates(&all_projections, &subquery_names)
        {
            // `GROUP BY ALL` may infer no keys; nothing here runs in a group context.
            self.group_scope.mark_whole_frame_windows = false;
            projections = all_projections;
            explicit_aliases.extend(qualify.is_some().then_some(true));
            // Aggregates are marked only until the projections are resolved below.
            check_columns_in_aggregates(&projections, &subquery_names)?;

            // Initialize containing InheritsContext to handle empty projection case.
            let mut projection_heights = ExprSqlProjectionHeightBehavior::InheritsContext;
            for p in &projections {
                // A window over the whole frame has one value per row, so for the output
                // height it counts like a literal.
                let height_expr = self.map_whole_frame_windows(p.clone(), |_| lit(1));
                projection_heights |= ExprSqlProjectionHeightBehavior::identify_from_expr(
                    &without_resolved_subqueries(&height_expr, &subquery_names),
                );
            }
            projections = projections
                .into_iter()
                .map(|e| strip_aggregate_marks(self.resolve_whole_frame_windows(e)))
                .collect();

            // Disambiguate SELECT-list output-name collisions.
            projections = disambiguate_output_names(
                projections.into_iter().zip(explicit_aliases).collect(),
                &schema,
            )?;

            let have_order_by = query.order_by.is_some();

            // Note: if there is an 'order by' then we project everything (original cols
            // and new projections) and *then* select the final cols by name. If there's no
            // 'order by', clause then we can project the final column *expressions* directly.
            let mut final_cols = Vec::with_capacity(projections.len());
            let mut final_names = Vec::with_capacity(projections.len());
            for p in &projections {
                let name = p.to_field(schema.deref())?.name;
                final_cols.push(if have_order_by {
                    col(name.clone())
                } else {
                    p.clone()
                });
                final_names.push(col(name));
            }

            // Establish the final projection
            if have_order_by {
                if select_stmt.from.is_empty() {
                    lf = lf.select(projections);
                } else if projection_heights
                    .contains(ExprSqlProjectionHeightBehavior::MaintainsColumn)
                    || projection_heights == ExprSqlProjectionHeightBehavior::InheritsContext
                {
                    // We can safely use `with_columns()` and avoid a join if:
                    // * There is already a projection that projects to the table height.
                    // * All projection heights inherit from context (e.g. all scalar literals that
                    //   are to be broadcasted to table height).
                    lf = lf.with_columns(projections)
                } else {
                    // We hit this branch if the output height is not guaranteed to match the table
                    // height. E.g.:
                    //
                    // * SELECT COUNT(*) FROM df ORDER BY sort_key;
                    //
                    // For these cases we truncate / extend the sorting columns with NULLs to match
                    // the output height. We do this by projecting independently and then joining
                    // back the original frame on the row index.
                    const NAME: PlSmallStr = PlSmallStr::from_static("__PL_INDEX");
                    // The row index pairs the two sides, so both must read one
                    // materialisation of the frame.
                    let cached = lf.cache();
                    lf = cached
                        .clone()
                        .select(projections)
                        .with_row_index(NAME, None)
                        .join(
                            cached.with_row_index(NAME, None),
                            [col(NAME)],
                            [col(NAME)],
                            JoinArgs {
                                how: JoinType::Left,
                                validation: Default::default(),
                                suffix: None,
                                slice: None,
                                nulls_equal: false,
                                coalesce: Default::default(),
                                maintain_order: MaintainOrderJoin::Left,
                                build_side: None,
                            },
                        )?;
                }
            }
            let n_selected = final_cols.len() - usize::from(qualify.is_some());
            lf = self.process_order_by(lf, &query.order_by, Some(&final_cols[..n_selected]))?;

            // Note: If `have_order_by`, with_columns is already done above.
            if projection_heights == ExprSqlProjectionHeightBehavior::InheritsContext
                && !have_order_by
                && !select_stmt.from.is_empty()
                && !final_cols.is_empty()
            {
                // All projections need to be broadcasted to table height, so evaluate in `with_columns()`
                lf = lf.with_columns(final_cols).select(final_names);
            } else {
                lf = lf.select(final_cols);
            }
            lf
        } else {
            let having = lowered_having
                .as_deref()
                .map(|expr| self.marking_aggregates(|ctx| parse_sql_expr(expr, ctx, Some(&schema))))
                .transpose()?;
            let grouping = self.bind_grouping_sets(
                &group_by_keys,
                grouping_sets,
                &projections,
                &schema,
                &query.order_by,
            )?;
            let (output_names, order_by);
            (lf, output_names, order_by) = self.process_group_by(
                lf,
                &group_by_keys,
                projections,
                &explicit_aliases,
                having,
                qualify.take().map(|e| (qualify_column.clone(), e)),
                &query.order_by,
                grouping.as_ref(),
                &subquery_names,
            )?;
            // The remaining clauses run on the aggregated frame.
            self.group_scope.mark_whole_frame_windows = false;
            let visible_cols: Vec<_> = output_names.iter().cloned().map(col).collect();
            lf = self.process_order_by(lf, &order_by, Some(&visible_cols))?;

            // Drop any extra columns (eg: added to maintain ORDER BY access to original cols).
            let mut output_cols = visible_cols;
            if select_stmt.qualify.is_some() {
                output_cols.push(col(qualify_column.clone()));
            }
            lf.select(&output_cols)
        };

        if select_stmt.qualify.is_some() {
            lf = lf
                .filter(col(qualify_column.clone()))
                .drop(Selector::ByName {
                    names: Arc::from([qualify_column]),
                    strict: true,
                });
        }

        // Apply optional DISTINCT clause.
        lf = match &select_stmt.distinct {
            Some(Distinct::Distinct) => lf.unique_stable(None, UniqueKeepStrategy::Any),
            Some(Distinct::On(exprs)) => {
                // TODO: support exprs in `unique` see https://github.com/pola-rs/polars/issues/5760
                let schema = Some(self.get_frame_schema(&mut lf)?);
                let cols = exprs
                    .iter()
                    .map(|e| {
                        let expr = parse_sql_expr(e, self, schema.as_deref())?;
                        if let Expr::Column(name) = expr {
                            Ok(name)
                        } else {
                            Err(polars_err!(SQLSyntax:"DISTINCT ON only supports column names"))
                        }
                    })
                    .collect::<PolarsResult<Vec<_>>>()?;

                // DISTINCT ON has to apply the ORDER BY before the operation.
                lf = self.process_order_by(lf, &query.order_by, None)?;
                return Ok(lf.unique_stable(
                    Some(Selector::ByName {
                        names: cols.into(),
                        strict: true,
                    }),
                    UniqueKeepStrategy::First,
                ));
            },
            // Note: `ALL` explicitly keeps duplicate rows (the default), so it's a no-op.
            Some(Distinct::All) | None => lf,
        };
        Ok(lf)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn execute_select_block(
        &mut self,
        select_stmt: &Select,
        query: &Query,
    ) -> PolarsResult<LazyFrame> {
        // Check that the statement doesn't contain unsupported SELECT clauses
        self.validate_select(select_stmt)?;

        // Parse named windows first, as they may be referenced in the SELECT clause
        self.register_named_windows(&select_stmt.named_window)?;

        // Get `FROM` table/data
        let mut implicit_join_filter: Option<SQLExpr> = None;
        let mut lf = if select_stmt.from.is_empty() {
            self.active_relations.clear();
            DataFrame::new(1, vec![])?.lazy()
        } else {
            let from = &select_stmt.from;
            let first = from.first().unwrap();
            // Set before the relations are resolved, so a join constraint
            // resolves against them.
            self.active_relations = declared_relations(from);
            let mut lf = self.execute_from_statement(first)?;
            if from.len() > 1 {
                implicit_join_filter =
                    self.process_implicit_joins(&mut lf, from, &select_stmt.selection)?;
            }
            lf
        };

        self.set_join_base(&select_stmt.from);
        self.check_select_column_refs(select_stmt)?;

        // Apply `WHERE` constraint (using residual filter for implicit joins)
        let where_expr = if implicit_join_filter.is_some() {
            implicit_join_filter.as_ref()
        } else {
            select_stmt.selection.as_ref()
        };
        let mut schema = self.get_frame_schema(&mut lf)?;

        // Shared by every pass over this frame: WHERE, the projection list and HAVING.
        let mut bindings = SubqueryBindings::new();

        // A correlated scalar subquery is lowered against the frame as it stands, so
        // the conjuncts that don't need it are applied first: the lowering can then
        // restrict its aggregate to the rows that survive them.
        let mut join_tree = None;
        let where_expr: Option<Cow<'_, SQLExpr>> = match where_expr {
            Some(where_expr) if expr_contains_scalar_subquery(where_expr) => {
                let n_grouping_calls = self.group_scope.grouping_calls.len();
                let residual;
                (lf, residual) = self.rewrite_subquery_conjuncts(
                    lf,
                    where_expr,
                    FilterMode::KeepTrue,
                    &schema,
                    RewriteStage::BeforeScalarLowering,
                )?;
                self.reject_grouping_in_where(n_grouping_calls)?;
                join_tree = self.outer_join_tree(select_stmt, where_expr, &residual)?;
                schema = self.get_frame_schema(&mut lf)?;
                combine_conditions(
                    residual.into_iter().cloned().collect(),
                    SQLBinaryOperator::And,
                )
                .map(Cow::Owned)
            },
            other => other.map(Cow::Borrowed),
        };

        // Lower correlated scalar subqueries in the WHERE clause before the filter is
        // parsed, leaving `[NOT] EXISTS` to `process_where`.
        let effective_where = match where_expr.as_deref() {
            Some(where_expr) => {
                let lowered;
                (lf, lowered) = self.lower_correlated_subqueries(
                    lf,
                    &schema,
                    where_expr,
                    LowerScope::ScalarOnly,
                    &mut bindings,
                    join_tree.as_ref(),
                )?;
                if matches!(lowered, Cow::Owned(_)) {
                    schema = self.get_frame_schema(&mut lf)?;
                }
                Some(lowered)
            },
            None => None,
        };

        lf = self.process_where(
            lf,
            effective_where.as_deref(),
            FilterMode::KeepTrue,
            Some(schema.clone()),
        )?;

        // HAVING is parsed further below but lowered here, against the pre-aggregation
        // frame.
        let mut lowered_projection: Option<Vec<SelectItem>> = None;
        let mut lowered_having: Option<Cow<'_, SQLExpr>> = None;
        {
            let mut changed = false;
            for (idx, item) in select_stmt.projection.iter().enumerate() {
                let (SelectItem::UnnamedExpr(e) | SelectItem::ExprWithAlias { expr: e, .. }) = item
                else {
                    continue;
                };
                let lowered;
                (lf, lowered) = self.lower_correlated_subqueries(
                    lf,
                    &schema,
                    e,
                    LowerScope::ScalarAndPredicates,
                    &mut bindings,
                    None,
                )?;
                if let Cow::Owned(lowered) = lowered {
                    changed = true;
                    let items =
                        lowered_projection.get_or_insert_with(|| select_stmt.projection.clone());
                    match &mut items[idx] {
                        SelectItem::UnnamedExpr(slot)
                        | SelectItem::ExprWithAlias { expr: slot, .. } => *slot = lowered,
                        _ => unreachable!("only expression items are lowered"),
                    }
                }
            }
            if let Some(having) = &select_stmt.having {
                let lowered;
                (lf, lowered) = self.lower_correlated_subqueries(
                    lf,
                    &schema,
                    having,
                    LowerScope::ScalarAndPredicates,
                    &mut bindings,
                    None,
                )?;
                changed |= matches!(lowered, Cow::Owned(_));
                lowered_having = Some(lowered);
            }
            if changed {
                schema = self.get_frame_schema(&mut lf)?;
            }
        }
        let projection: &[SelectItem] = lowered_projection
            .as_deref()
            .unwrap_or(&select_stmt.projection);

        if let Some(qualify) = &select_stmt.qualify {
            check_qualify(qualify, &select_stmt.projection)?;
        }

        let mark_whole_frame_windows =
            std::mem::replace(&mut self.group_scope.mark_whole_frame_windows, true);
        let mut projections_with_flags = self.marking_aggregates(|ctx| {
            ctx.column_projections(projection, select_stmt.flavor, &schema)
        })?;
        self.group_scope.mark_whole_frame_windows = mark_whole_frame_windows;
        let mut subquery_names;
        (lf, subquery_names) = self.process_subqueries(
            lf,
            projections_with_flags.iter_mut().map(|(e, _)| e).collect(),
            SubqueryShape::Scalar,
        )?;
        for (expr, _) in projections_with_flags.iter_mut() {
            *expr = broadcast_subqueries_in_inputs(
                expr.clone(),
                &subquery_names,
                &self.group_scope.subqueries_read_per_row,
            );
        }
        schema = self.get_frame_schema(&mut lf)?;

        // Placeholder names are generated per execution, so an unaliased projection
        // named after one gets the name given to any other unnamed scalar expression.
        // Matching on the output name rather than the expression shape also catches
        // projections that merely derive their name from a placeholder.
        if !subquery_names.is_empty() {
            for (expr, is_explicit_alias) in projections_with_flags.iter_mut() {
                if *is_explicit_alias {
                    continue;
                }
                let is_placeholder_name = expr
                    .to_field(&schema)
                    .is_ok_and(|f| subquery_names.contains(&f.name));
                if is_placeholder_name {
                    *expr = expr.clone().alias(PlSmallStr::from_static("literal"));
                }
            }
        }

        // QUALIFY filters on windows over the rows the SELECT list reads, so it is computed
        // with the SELECT list, as a hidden column. It can name SELECT aliases, which read the
        // subqueries of the SELECT list resolved above.
        let qualify_column = format_pl_smallstr!("__POLARS_QUALIFY_{}", unique_column_name());
        let mut qualify = match &select_stmt.qualify {
            Some(qualify) => {
                let projections: Vec<Expr> = projections_with_flags
                    .iter()
                    .map(|(e, _)| e.clone())
                    .collect();
                let output_names = OutputNames::new(
                    &projections,
                    &schema,
                    &self.with_placeholder_columns(&schema),
                );
                let output_schema = output_names.extend_schema(&schema);
                let mark_whole_frame_windows =
                    std::mem::replace(&mut self.group_scope.mark_whole_frame_windows, true);
                let parsed = self
                    .marking_aggregates(|ctx| parse_sql_expr(qualify, ctx, Some(&output_schema)));
                self.group_scope.mark_whole_frame_windows = mark_whole_frame_windows;
                let mut qualify = output_names.resolve(parsed?);
                if qualify.clone().meta().has_multiple_outputs() {
                    qualify = all_horizontal([qualify])?;
                }
                let qualify_subquery_names;
                (lf, qualify_subquery_names) =
                    self.process_subqueries(lf, vec![&mut qualify], SubqueryShape::Scalar)?;
                if !qualify_subquery_names.is_empty() {
                    subquery_names.extend(qualify_subquery_names);
                    schema = self.get_frame_schema(&mut lf)?;
                }
                let qualify = broadcast_subqueries_in_inputs(
                    qualify,
                    &subquery_names,
                    &self.group_scope.subqueries_read_per_row,
                );
                Some(qualify.alias(qualify_column.clone()))
            },
            None => None,
        };

        let (mut projections, mut explicit_aliases): (Vec<Expr>, Vec<bool>) =
            projections_with_flags.into_iter().unzip();

        // Apply `UNNEST` expressions
        let mut explode_names = Vec::new();
        let mut explode_exprs = Vec::new();
        let mut explode_lookup = PlHashMap::new();

        for expr in &projections {
            for e in expr {
                if let Expr::Explode { input, .. } = e {
                    match input.as_ref() {
                        Expr::Column(name) => explode_names.push(name.clone()),
                        other_expr => {
                            // Note: skip aggregate expressions; those are handled in the GROUP BY phase
                            if !has_expr(other_expr, |e| matches!(e, Expr::Agg(_) | Expr::Len)) {
                                let temp_name =
                                    format_pl_smallstr!("__POLARS_UNNEST_{}", explode_exprs.len());
                                explode_exprs.push(other_expr.clone().alias(temp_name.as_str()));
                                explode_lookup.insert(other_expr.clone(), temp_name.clone());
                                explode_names.push(temp_name);
                            }
                        },
                    }
                }
            }
        }
        if !explode_names.is_empty() {
            if !explode_exprs.is_empty() {
                lf = lf.with_columns(explode_exprs);
            }
            lf = lf.explode(
                Selector::ByName {
                    names: Arc::from(explode_names),
                    strict: true,
                },
                ExplodeOptions {
                    empty_as_null: true,
                    keep_nulls: true,
                },
            );
            projections = projections
                .into_iter()
                .map(|p| {
                    // Update "projections" with column refs to the now-exploded expressions
                    p.map_expr(|e| match e {
                        Expr::Explode { input, .. } => explode_lookup
                            .get(input.as_ref())
                            .map(|name| Expr::Column(name.clone()))
                            .unwrap_or_else(|| input.as_ref().clone()),
                        _ => e,
                    })
                })
                .collect();

            schema = self.get_frame_schema(&mut lf)?;
        }

        // Check for "GROUP BY ..." (after determining projections)
        let mut group_by_keys: Vec<Expr> = Vec::new();
        let mut grouping_sets: Option<Vec<Vec<usize>>> = None;
        match &select_stmt.group_by {
            // Standard "GROUP BY x, y, z" syntax (also recognising ordinal values)
            GroupByExpr::Expressions(group_by_exprs, modifiers) => {
                if !modifiers.is_empty() {
                    polars_bail!(SQLInterface: "GROUP BY does not support CUBE, ROLLUP, or TOTALS modifiers")
                }
                let expanded = expand_grouping_sets(group_by_exprs)?;
                let key_exprs: &[SQLExpr] = expanded
                    .as_ref()
                    .map_or(group_by_exprs, |expanded| &expanded.keys);
                // Translate the group expressions, resolving ordinal values and SELECT aliases
                group_by_keys = key_exprs
                    .iter()
                    .map(|e| self.resolve_group_by_key(e, &projections, &schema, true))
                    .collect::<PolarsResult<_>>()?;
                if let Some(expanded) = expanded {
                    let (keys, sets) = canonicalize_keys(group_by_keys, expanded.sets);
                    group_by_keys = keys;
                    grouping_sets = Some(sets);
                }
            },
            // "GROUP BY ALL" syntax; automatically adds expressions that do not contain
            // nested agg/window funcs to the group key (also ignores literals).
            GroupByExpr::All(modifiers) => {
                if !modifiers.is_empty() {
                    polars_bail!(SQLInterface: "GROUP BY does not support CUBE, ROLLUP, or TOTALS modifiers")
                }
                projections.iter().for_each(|expr| match expr {
                    // immediately match the most common cases (col|agg|len|lit, optionally aliased).
                    Expr::Agg(_) | Expr::Len | Expr::Literal(_) => (),
                    _ if self.contains_grouping_placeholder(expr) => (),
                    Expr::Column(_) => group_by_keys.push(expr.clone()),
                    Expr::Alias(e, _)
                        if matches!(&**e, Expr::Agg(_) | Expr::Len | Expr::Literal(_)) => {},
                    Expr::Alias(e, _) if matches!(&**e, Expr::Column(_)) => {
                        if let Expr::Column(name) = &**e {
                            group_by_keys.push(col(name.clone()));
                        }
                    },
                    _ => {
                        // If not quick-matched, add if no nested agg/window expressions
                        if !has_expr(expr, |e| {
                            is_marked_aggregate(e)
                                || matches!(e, Expr::Agg(_))
                                || matches!(e, Expr::Len)
                                || matches!(e, Expr::Over { .. })
                                || {
                                    #[cfg(feature = "dynamic_group_by")]
                                    {
                                        matches!(e, Expr::Rolling { .. })
                                    }
                                    #[cfg(not(feature = "dynamic_group_by"))]
                                    {
                                        false
                                    }
                                }
                        }) {
                            group_by_keys.push(expr.clone())
                        }
                    },
                });
            },
        };
        for e in &group_by_keys {
            reject_unresolved_subquery(e, "GROUP BY")?;
            polars_ensure!(
                !self.contains_grouping_placeholder(e),
                SQLSyntax: "GROUPING() is not allowed in the GROUP BY clause"
            );
        }
        if grouping_sets.is_none() {
            let mut seen: Vec<Expr> = Vec::with_capacity(group_by_keys.len());
            group_by_keys.retain(|key| {
                let stripped = strip_outer_alias(key);
                let is_new = !seen.contains(&stripped);
                if is_new {
                    seen.push(stripped);
                }
                is_new
            });
        }

        let has_group_by = !group_by_keys.is_empty() || grouping_sets.is_some();
        if !has_group_by {
            polars_ensure!(
                self.group_scope.grouping_calls.is_empty(),
                SQLSyntax: "GROUPING() requires a GROUP BY clause"
            );
        }
        // Without GROUP BY, a block with aggregates or HAVING is one group, and its windows
        // and the subqueries outside its aggregates run on that one row.
        let all_projections = projections
            .iter()
            .chain(&qualify)
            .cloned()
            .collect::<Vec<_>>();
        lf = if !has_group_by
            && lowered_having.is_none()
            && !has_windows_over_aggregates(&all_projections)
            && !has_subquery_outside_aggregates(&all_projections, &subquery_names)
        {
            // `GROUP BY ALL` may infer no keys; nothing here runs in a group context.
            self.group_scope.mark_whole_frame_windows = false;
            projections = all_projections;
            explicit_aliases.extend(qualify.is_some().then_some(true));
            // Aggregates are marked only until the projections are resolved below.
            check_columns_in_aggregates(&projections, &subquery_names)?;

            // Initialize containing InheritsContext to handle empty projection case.
            let mut projection_heights = ExprSqlProjectionHeightBehavior::InheritsContext;
            for p in &projections {
                // A window over the whole frame has one value per row, so for the output
                // height it counts like a literal.
                let height_expr = self.map_whole_frame_windows(p.clone(), |_| lit(1));
                projection_heights |= ExprSqlProjectionHeightBehavior::identify_from_expr(
                    &without_resolved_subqueries(&height_expr, &subquery_names),
                );
            }
            projections = projections
                .into_iter()
                .map(|e| strip_aggregate_marks(self.resolve_whole_frame_windows(e)))
                .collect();

            // Disambiguate SELECT-list output-name collisions.
            projections = disambiguate_output_names(
                projections.into_iter().zip(explicit_aliases).collect(),
                &schema,
            )?;

            let have_order_by = query.order_by.is_some();

            // Note: if there is an 'order by' then we project everything (original cols
            // and new projections) and *then* select the final cols by name. If there's no
            // 'order by', clause then we can project the final column *expressions* directly.
            let mut final_cols = Vec::with_capacity(projections.len());
            let mut final_names = Vec::with_capacity(projections.len());
            for p in &projections {
                let name = p.to_field(schema.deref())?.name;
                final_cols.push(if have_order_by {
                    col(name.clone())
                } else {
                    p.clone()
                });
                final_names.push(col(name));
            }

            // Establish the final projection
            if have_order_by {
                if select_stmt.from.is_empty() {
                    lf = lf.select(projections);
                } else if projection_heights
                    .contains(ExprSqlProjectionHeightBehavior::MaintainsColumn)
                    || projection_heights == ExprSqlProjectionHeightBehavior::InheritsContext
                {
                    // We can safely use `with_columns()` and avoid a join if:
                    // * There is already a projection that projects to the table height.
                    // * All projection heights inherit from context (e.g. all scalar literals that
                    //   are to be broadcasted to table height).
                    lf = lf.with_columns(projections)
                } else {
                    // We hit this branch if the output height is not guaranteed to match the table
                    // height. E.g.:
                    //
                    // * SELECT COUNT(*) FROM df ORDER BY sort_key;
                    //
                    // For these cases we truncate / extend the sorting columns with NULLs to match
                    // the output height. We do this by projecting independently and then joining
                    // back the original frame on the row index.
                    const NAME: PlSmallStr = PlSmallStr::from_static("__PL_INDEX");
                    // The row index pairs the two sides, so both must read one
                    // materialisation of the frame.
                    let cached = lf.cache();
                    lf = cached
                        .clone()
                        .select(projections)
                        .with_row_index(NAME, None)
                        .join(
                            cached.with_row_index(NAME, None),
                            [col(NAME)],
                            [col(NAME)],
                            JoinArgs {
                                how: JoinType::Left,
                                validation: Default::default(),
                                suffix: None,
                                slice: None,
                                nulls_equal: false,
                                coalesce: Default::default(),
                                maintain_order: MaintainOrderJoin::Left,
                                build_side: None,
                            },
                        )?;
                }
            }
            let n_selected = final_cols.len() - usize::from(qualify.is_some());
            lf = self.process_order_by(lf, &query.order_by, Some(&final_cols[..n_selected]))?;

            // Note: If `have_order_by`, with_columns is already done above.
            if projection_heights == ExprSqlProjectionHeightBehavior::InheritsContext
                && !have_order_by
                && !select_stmt.from.is_empty()
                && !final_cols.is_empty()
            {
                // All projections need to be broadcasted to table height, so evaluate in `with_columns()`
                lf = lf.with_columns(final_cols).select(final_names);
            } else {
                lf = lf.select(final_cols);
            }
            lf
        } else {
            let having = lowered_having
                .as_deref()
                .map(|expr| self.marking_aggregates(|ctx| parse_sql_expr(expr, ctx, Some(&schema))))
                .transpose()?;
            let grouping = self.bind_grouping_sets(
                &group_by_keys,
                grouping_sets,
                &projections,
                &schema,
                &query.order_by,
            )?;
            let (output_names, order_by);
            (lf, output_names, order_by) = self.process_group_by(
                lf,
                &group_by_keys,
                projections,
                &explicit_aliases,
                having,
                qualify.take().map(|e| (qualify_column.clone(), e)),
                &query.order_by,
                grouping.as_ref(),
                &subquery_names,
            )?;
            // The remaining clauses run on the aggregated frame.
            self.group_scope.mark_whole_frame_windows = false;
            let visible_cols: Vec<_> = output_names.iter().cloned().map(col).collect();
            lf = self.process_order_by(lf, &order_by, Some(&visible_cols))?;

            // Drop any extra columns (eg: added to maintain ORDER BY access to original cols).
            let mut output_cols = visible_cols;
            if select_stmt.qualify.is_some() {
                output_cols.push(col(qualify_column.clone()));
            }
            lf.select(&output_cols)
        };

        if select_stmt.qualify.is_some() {
            lf = lf
                .filter(col(qualify_column.clone()))
                .drop(Selector::ByName {
                    names: Arc::from([qualify_column]),
                    strict: true,
                });
        }

        // Apply optional DISTINCT clause.
        lf = match &select_stmt.distinct {
            Some(Distinct::Distinct) => lf.unique_stable(None, UniqueKeepStrategy::Any),
            Some(Distinct::On(exprs)) => {
                // TODO: support exprs in `unique` see https://github.com/pola-rs/polars/issues/5760
                let schema = Some(self.get_frame_schema(&mut lf)?);
                let cols = exprs
                    .iter()
                    .map(|e| {
                        let expr = parse_sql_expr(e, self, schema.as_deref())?;
                        if let Expr::Column(name) = expr {
                            Ok(name)
                        } else {
                            Err(polars_err!(SQLSyntax:"DISTINCT ON only supports column names"))
                        }
                    })
                    .collect::<PolarsResult<Vec<_>>>()?;

                // DISTINCT ON has to apply the ORDER BY before the operation.
                lf = self.process_order_by(lf, &query.order_by, None)?;
                return Ok(lf.unique_stable(
                    Some(Selector::ByName {
                        names: cols.into(),
                        strict: true,
                    }),
                    UniqueKeepStrategy::First,
                ));
            },
            // Note: `ALL` explicitly keeps duplicate rows (the default), so it's a no-op.
            Some(Distinct::All) | None => lf,
        };
        Ok(lf)
    }
```


#### 📄 檔案: `crates/polars-sql/src/grouping_sets.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:177, E:185, A:0) ➔ After(N:177, E:186, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 7, +Edges: 13, -Edges: 12, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `self.stripped_keys
            .iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.stripped_keys
            .iter()
            .zip(key_schema.iter_names())
            .filter(|(key, _)| !matches!(key, Expr::Column(_)))
            .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `bind_stored_keys` (FUNCTION_DEF)
  • + [新增節點] `self.stripped_keys
            .iter()
            .zip (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.stripped_keys
            .iter()
            .zip(key_schema.iter_names())
            .filter(|(key, _)| !matches!(key, Expr::Column(_)))
            .map(|(key, name)| (key.clone(), name.clone()))
            .collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.stripped_keys
            .iter()
            .zip(key_schema.iter_names())
            .filter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `GroupingSets::stored_keys` (FUNCTION_DEF)
  • - [移除節點] `self
            .stripped_keys
            .iter()
            .zip(key_schema.iter_names())
            .map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `self
            .stripped_keys
            .iter()
            .zip(key_schema.iter_names())
            .map(|(key, name)| (key.clone(), name))
            .filter (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `self
            .stripped_keys
            .iter (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `self
            .stripped_keys
            .iter()
            .zip(key_schema.iter_names())
            .map(|(key, name)| (key.clone(), name))
            .filter(|(key, _)| !matches!(key, Expr::Column(_)))
            .collect::<Vec<_>> (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `self
            .stripped_keys
            .iter()
            .zip (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `GroupingSets::bind_stored_keys` (FUNCTION_DEF)
  • - [移除節點] `(*name).clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `GroupingSets::stored_keys` ──[CALLS]──> `self.stripped_keys
            .iter()
            .zip(key_schema.iter_names())
            .filter(|(key, _)| !matches!(key, Expr::Column(_)))
            .map(|(key, name)| (key.clone(), name.clone()))
            .collect (External/Unresolved)`
  • _... 以及其餘 24 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Binder::mutate()`
- **變更前簽章 (Before)**: `fn Binder::mutate(&mut self, node: Expr, _: &mut ())` (L244~L247)
- **變更後簽章 (After)**: `fn Binder::mutate(&mut self, node: Expr, _: &mut ())` (L345~L348)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn mutate(&mut self, node: Expr, _: &mut ()) -> PolarsResult<Expr> {
                let (_, name) = self.keys.iter().find(|(k, _)| *k == node).unwrap();
                Ok(col((*name).clone()))
            }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn mutate(&mut self, node: Expr, _: &mut ()) -> PolarsResult<Expr> {
            let (_, name) = self.keys.iter().find(|(k, _)| *k == node).unwrap();
            Ok(col(name.clone()))
        }
```

### 🔹 函式: `Binder::pre_visit()`
- **變更前簽章 (Before)**: `fn Binder::pre_visit(&mut self, node: &Expr, _: &mut ())` (L234~L242)
- **變更後簽章 (After)**: `fn Binder::pre_visit(&mut self, node: &Expr, _: &mut ())` (L337~L343)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn pre_visit(&mut self, node: &Expr, _: &mut ()) -> PolarsResult<RewriteRecursion> {
                Ok(match node {
                    Expr::Agg(_) | Expr::Len => RewriteRecursion::Stop,
                    _ if self.keys.iter().any(|(k, _)| k == node) => {
                        RewriteRecursion::MutateAndStop
                    },
                    _ => RewriteRecursion::NoMutateAndContinue,
                })
            }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn pre_visit(&mut self, node: &Expr, _: &mut ()) -> PolarsResult<RewriteRecursion> {
            Ok(match node {
                Expr::Agg(_) | Expr::Len => RewriteRecursion::Stop,
                _ if self.keys.iter().any(|(k, _)| k == node) => RewriteRecursion::MutateAndStop,
                _ => RewriteRecursion::NoMutateAndContinue,
            })
        }
```


---

### 🔹 Commit #20: `769413ba`
- **完整 Hash**: `769413ba3fc959af9bc3c0329048eb9a8c569723`
- **說明 (Ground Truth)**: fix: Clear null propagated flag when setting outer validity on struct (#29949)
- **變更檔案數**: 1

#### 📄 檔案: `crates/polars-core/src/chunked_array/struct_/mod.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:217, E:267, A:0) ➔ After(N:219, E:271, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 4, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `self.get_flags (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.set_flags (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `StructChunked::zip_outer_validity` ──[CALLS]──> `self.set_flags (External/Unresolved)`
  • + [新增呼叫邊] `StructChunked::zip_outer_validity` ──[CALLS]──> `self.get_flags (External/Unresolved)`
  • + [新增呼叫邊] `StructChunked::set_outer_validity` ──[CALLS]──> `self.set_flags (External/Unresolved)`
  • + [新增呼叫邊] `StructChunked::set_outer_validity` ──[CALLS]──> `self.get_flags (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `StructChunked::zip_outer_validity()`
- **變更前簽章 (Before)**: `fn StructChunked::zip_outer_validity(&mut self, other: &StructChunked)` (L421~L453)
- **變更後簽章 (After)**: `fn StructChunked::zip_outer_validity(&mut self, other: &StructChunked)` (L422~L455)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn zip_outer_validity(&mut self, other: &StructChunked) {
        // This might go wrong for broadcasting behavior. If this is not checked, it leads to a
        // segfault because we infinitely recurse.
        assert_eq!(self.len(), other.len());

        if other.null_count() == 0 {
            return;
        }

        if self.chunks.len() != other.chunks.len()
            || self
                .chunks
                .iter()
                .zip(other.chunks())
                .any(|(a, b)| a.len() != b.len())
        {
            self.rechunk_mut();
            let other = other.rechunk();
            return self.zip_outer_validity(&other);
        }

        // SAFETY:
        // We keep length and dtypes the same.
        unsafe {
            for (a, b) in self.downcast_iter_mut().zip(other.downcast_iter()) {
                let new = combine_validities_and(a.validity(), b.validity());
                a.set_validity(new)
            }
        }

        self.compute_len();
        self.propagate_nulls_mut();
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn zip_outer_validity(&mut self, other: &StructChunked) {
        // This might go wrong for broadcasting behavior. If this is not checked, it leads to a
        // segfault because we infinitely recurse.
        assert_eq!(self.len(), other.len());

        if other.null_count() == 0 {
            return;
        }

        if self.chunks.len() != other.chunks.len()
            || self
                .chunks
                .iter()
                .zip(other.chunks())
                .any(|(a, b)| a.len() != b.len())
        {
            self.rechunk_mut();
            let other = other.rechunk();
            return self.zip_outer_validity(&other);
        }

        // SAFETY:
        // We keep length and dtypes the same.
        unsafe {
            for (a, b) in self.downcast_iter_mut().zip(other.downcast_iter()) {
                let new = combine_validities_and(a.validity(), b.validity());
                a.set_validity(new)
            }
        }

        self.compute_len();
        self.set_flags(self.get_flags() - StatisticsFlags::HAS_PROPAGATED_NULLS);
        self.propagate_nulls_mut();
    }
```

### 🔹 函式: `StructChunked::set_outer_validity()`
- **變更前簽章 (Before)**: `fn StructChunked::set_outer_validity(&mut self, validity: Option<Bitmap>)` (L474~L498)
- **變更後簽章 (After)**: `fn StructChunked::set_outer_validity(&mut self, validity: Option<Bitmap>)` (L476~L501)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn set_outer_validity(&mut self, validity: Option<Bitmap>) {
        if let Some(v) = &validity {
            assert_eq!(self.len(), v.len());
        }

        let validity = validity.filter(|v| v.unset_bits() > 0);

        // SAFETY: We keep length and dtypes the same.
        unsafe {
            let chunks = self.chunks_mut();
            if chunks.len() == 1 {
                chunks[0] = chunks[0].with_validity(validity);
            } else {
                let mut offset = 0;
                for arr in chunks {
                    let len = arr.len();
                    *arr =
                        arr.with_validity(validity.as_ref().map(|v| v.clone().sliced(offset, len)));
                    offset += len;
                }
            }
        }
        self.compute_len();
        self.propagate_nulls_mut();
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn set_outer_validity(&mut self, validity: Option<Bitmap>) {
        if let Some(v) = &validity {
            assert_eq!(self.len(), v.len());
        }

        let validity = validity.filter(|v| v.unset_bits() > 0);

        // SAFETY: We keep length and dtypes the same.
        unsafe {
            let chunks = self.chunks_mut();
            if chunks.len() == 1 {
                chunks[0] = chunks[0].with_validity(validity);
            } else {
                let mut offset = 0;
                for arr in chunks {
                    let len = arr.len();
                    *arr =
                        arr.with_validity(validity.as_ref().map(|v| v.clone().sliced(offset, len)));
                    offset += len;
                }
            }
        }
        self.compute_len();
        self.set_flags(self.get_flags() - StatisticsFlags::HAS_PROPAGATED_NULLS);
        self.propagate_nulls_mut();
    }
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/polars show c99202aac2eaf89bbda8aaeb25a9c4587bf27692
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff c99202aac2eaf89bbda8aaeb25a9c4587bf27692~1 --file test_repos/polars/crates/polars-core/src/series/arithmetic/borrowed.rs
   ```
