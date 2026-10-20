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

### 🔹 Commit #04: `19c0b7a5`
- **完整 Hash**: `19c0b7a5b0c18a6f2e7c0763884654f48ffa3ff1`
- **說明 (Ground Truth)**: 🐛 Treat omitted boolean form fields as False (#16523)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/dependencies/utils.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:91, E:130, A:0) ➔ After(N:93, E:135, A:0)
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
  • + [新增節點] `next (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `all (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `_extract_form_body` ──[CALLS]──> `set (External/Unresolved)`
  • + [新增呼叫邊] `_extract_form_body` ──[CALLS]──> `all (External/Unresolved)`
  • + [新增呼叫邊] `_extract_form_body` ──[CALLS]──> `cast (External/Unresolved)`
  • + [新增呼叫邊] `_extract_form_body` ──[CALLS]──> `next (External/Unresolved)`
  • + [新增呼叫邊] `_extract_form_body` ──[CALLS]──> `add (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_extract_form_body()`
- **變更前簽章 (Before)**: `async def _extract_form_body( body_fields: list[ModelField], received_body: FormData, ) -> dict[str, Any]` (L912~L951)
- **變更後簽章 (After)**: `async def _extract_form_body( body_fields: list[ModelField], received_body: FormData, ) -> dict[str, Any]` (L912~L986)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def _extract_form_body(
    body_fields: list[ModelField],
    received_body: FormData,
) -> dict[str, Any]:
    values = {}

    for field in body_fields:
        value = _get_multidict_value(field, received_body)
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
        if value is not None:
            values[get_validation_alias(field)] = value
    field_aliases = {get_validation_alias(field) for field in body_fields}
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


---

### 🔹 Commit #05: `45c41993`
- **完整 Hash**: `45c419938435d668a85a2e81bb9ac41495f8a648`
- **說明 (Ground Truth)**: 🗑️ Deprecate the `root_path` parameter in `FastAPI` (#16520)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/applications.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:64, E:78, A:0) ➔ After(N:65, E:79, A:0)
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
  • + [新增節點] `warn (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `FastAPI.__init__` ──[CALLS]──> `warn (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FastAPI.__init__()`
- **變更前簽章 (Before)**: `def __init__( self: AppType, *, telemetry: Annotated[ TelemetryConfig | None, Doc( """ Native OpenTelemetry configuration as a dictionary. Uses global providers by default. Omitted options keep their defaults. ```python app = FastAPI(telemetry={"tracing": False}) ``` """ ), ] = None, debug: Annotated[ bool, Doc( """ Boolean indicating if debug tracebacks should be returned on server errors. Read more in the [Starlette docs for Applications](https://starlette.dev/applications/#starlette.applications.Starlette). """ ), ] = False, routes: Annotated[ list[BaseRoute] | None, Doc( """ **Note**: you probably shouldn't use this parameter, it is inherited from Starlette and supported for compatibility. --- A list of routes to serve incoming HTTP and WebSocket requests. """ ), deprecated( """ You normally wouldn't use this parameter with FastAPI, it is inherited from Starlette and supported for compatibility. In FastAPI, you normally would use the *path operation methods*, like `app.get()`, `app.post()`, etc. """ ), ] = None, title: Annotated[ str, Doc( """ The title of the API. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI(title="ChimichangApp") ``` """ ), ] = "FastAPI", summary: Annotated[ str | None, Doc( """ A short summary of the API. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI(summary="Deadpond's favorite app. Nuff said.") ``` """ ), ] = None, description: Annotated[ str, Doc( ''' A description of the API. Supports Markdown (using [CommonMark syntax](https://commonmark.org/)). It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI( description=""" ChimichangApp API helps you do awesome stuff. 🚀 ## Items You can **read items**. ## Users You will be able to: * **Create users** (_not implemented_). * **Read users** (_not implemented_). """ ) ``` ''' ), ] = "", version: Annotated[ str, Doc( """ The version of the API. **Note** This is the version of your application, not the version of the OpenAPI specification nor the version of FastAPI being used. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI(version="0.0.1") ``` """ ), ] = "0.1.0", openapi_url: Annotated[ str | None, Doc( """ The URL where the OpenAPI schema will be served from. If you set it to `None`, no OpenAPI schema will be served publicly, and the default automatic endpoints `/docs` and `/redoc` will also be disabled. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url). **Example** ```python from fastapi import FastAPI app = FastAPI(openapi_url="/api/v1/openapi.json") ``` """ ), ] = "/openapi.json", openapi_tags: Annotated[ list[dict[str, Any]] | None, Doc( """ A list of tags used by OpenAPI, these are the same `tags` you can set in the *path operations*, like: * `@app.get("/users/", tags=["users"])` * `@app.get("/items/", tags=["items"])` The order of the tags can be used to specify the order shown in tools like Swagger UI, used in the automatic path `/docs`. It's not required to specify all the tags used. The tags that are not declared MAY be organized randomly or based on the tools' logic. Each tag name in the list MUST be unique. The value of each item is a `dict` containing: * `name`: The name of the tag. * `description`: A short description of the tag. [CommonMark syntax](https://commonmark.org/) MAY be used for rich text representation. * `externalDocs`: Additional external documentation for this tag. If provided, it would contain a `dict` with: * `description`: A short description of the target documentation. [CommonMark syntax](https://commonmark.org/) MAY be used for rich text representation. * `url`: The URL for the target documentation. Value MUST be in the form of a URL. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags). **Example** ```python from fastapi import FastAPI tags_metadata = [ { "name": "users", "description": "Operations with users. The **login** logic is also here.", }, { "name": "items", "description": "Manage items. So _fancy_ they have their own docs.", "externalDocs": { "description": "Items external docs", "url": "https://fastapi.tiangolo.com/", }, }, ] app = FastAPI(openapi_tags=tags_metadata) ``` """ ), ] = None, servers: Annotated[ list[dict[str, str | Any]] | None, Doc( """ A `list` of `dict`s with connectivity information to a target server. You would use it, for example, if your application is served from different domains and you want to use the same Swagger UI in the browser to interact with each of them (instead of having multiple browser tabs open). Or if you want to leave fixed the possible URLs. If the servers `list` is not provided, or is an empty `list`, the `servers` property in the generated OpenAPI will be: * a `dict` with a `url` value of the application's mounting point (`root_path`) if it's different from `/`. * otherwise, the `servers` property will be omitted from the OpenAPI schema. Each item in the `list` is a `dict` containing: * `url`: A URL to the target host. This URL supports Server Variables and MAY be relative, to indicate that the host location is relative to the location where the OpenAPI document is being served. Variable substitutions will be made when a variable is named in `{`brackets`}`. * `description`: An optional string describing the host designated by the URL. [CommonMark syntax](https://commonmark.org/) MAY be used for rich text representation. * `variables`: A `dict` between a variable name and its value. The value is used for substitution in the server's URL template. Read more in the [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#additional-servers). **Example** ```python from fastapi import FastAPI app = FastAPI( servers=[ {"url": "https://stag.example.com", "description": "Staging environment"}, {"url": "https://prod.example.com", "description": "Production environment"}, ] ) ``` """ ), ] = None, dependencies: Annotated[ Sequence[Depends] | None, Doc( """ A list of global dependencies, they will be applied to each *path operation*, including in sub-routers. Read more about it in the [FastAPI docs for Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/). **Example** ```python from fastapi import Depends, FastAPI from .dependencies import func_dep_1, func_dep_2 app = FastAPI(dependencies=[Depends(func_dep_1), Depends(func_dep_2)]) ``` """ ), ] = None, default_response_class: Annotated[ type[Response], Doc( """ The default response class to be used. Read more in the [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class). **Example** ```python from fastapi import FastAPI from fastapi.responses import ORJSONResponse app = FastAPI(default_response_class=ORJSONResponse) ``` """ ), ] = Default(JSONResponse), redirect_slashes: Annotated[ bool, Doc( """ Whether to detect and redirect slashes in URLs when the client doesn't use the same format. **Example** ```python from fastapi import FastAPI app = FastAPI(redirect_slashes=True) # the default @app.get("/items/") async def read_items(): return [{"item_id": "Foo"}] ``` With this app, if a client goes to `/items` (without a trailing slash), they will be automatically redirected with an HTTP status code of 307 to `/items/`. """ ), ] = True, docs_url: Annotated[ str | None, Doc( """ The path to the automatic interactive API documentation. It is handled in the browser by Swagger UI. The default URL is `/docs`. You can disable it by setting it to `None`. If `openapi_url` is set to `None`, this will be automatically disabled. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls). **Example** ```python from fastapi import FastAPI app = FastAPI(docs_url="/documentation", redoc_url=None) ``` """ ), ] = "/docs", redoc_url: Annotated[ str | None, Doc( """ The path to the alternative automatic interactive API documentation provided by ReDoc. The default URL is `/redoc`. You can disable it by setting it to `None`. If `openapi_url` is set to `None`, this will be automatically disabled. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls). **Example** ```python from fastapi import FastAPI app = FastAPI(docs_url="/documentation", redoc_url="redocumentation") ``` """ ), ] = "/redoc", swagger_ui_oauth2_redirect_url: Annotated[ str | None, Doc( """ The OAuth2 redirect endpoint for the Swagger UI. By default it is `/docs/oauth2-redirect`. This is only used if you use OAuth2 (with the "Authorize" button) with Swagger UI. """ ), ] = "/docs/oauth2-redirect", swagger_ui_init_oauth: Annotated[ dict[str, Any] | None, Doc( """ OAuth2 configuration for the Swagger UI, by default shown at `/docs`. Read more about the available configuration options in the [Swagger UI docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/). """ ), ] = None, middleware: Annotated[ Sequence[Middleware] | None, Doc( """ List of middleware to be added when creating the application. In FastAPI you would normally do this with `app.add_middleware()` instead. Read more in the [FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/). """ ), ] = None, exception_handlers: Annotated[ dict[ int | type[Exception], Callable[[Request, Any], Coroutine[Any, Any, Response]], ] | None, Doc( """ A dictionary with handlers for exceptions. In FastAPI, you would normally use the decorator `@app.exception_handler()`. Read more in the [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/). """ ), ] = None, on_startup: Annotated[ Sequence[Callable[[], Any]] | None, Doc( """ A list of startup event handler functions. You should instead use the `lifespan` handlers. Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/). """ ), ] = None, on_shutdown: Annotated[ Sequence[Callable[[], Any]] | None, Doc( """ A list of shutdown event handler functions. You should instead use the `lifespan` handlers. Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/). """ ), ] = None, lifespan: Annotated[ Lifespan[AppType] | None, Doc( """ A `Lifespan` context manager handler. This replaces `startup` and `shutdown` functions with a single context manager. Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/). """ ), ] = None, terms_of_service: Annotated[ str | None, Doc( """ A URL to the Terms of Service for your API. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more at the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python app = FastAPI(terms_of_service="http://example.com/terms/") ``` """ ), ] = None, contact: Annotated[ dict[str, str | Any] | None, Doc( """ A dictionary with the contact information for the exposed API. It can contain several fields. * `name`: (`str`) The name of the contact person/organization. * `url`: (`str`) A URL pointing to the contact information. MUST be in the format of a URL. * `email`: (`str`) The email address of the contact person/organization. MUST be in the format of an email address. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more at the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python app = FastAPI( contact={ "name": "Deadpoolio the Amazing", "url": "http://x-force.example.com/contact/", "email": "dp@x-force.example.com", } ) ``` """ ), ] = None, license_info: Annotated[ dict[str, str | Any] | None, Doc( """ A dictionary with the license information for the exposed API. It can contain several fields. * `name`: (`str`) **REQUIRED** (if a `license_info` is set). The license name used for the API. * `identifier`: (`str`) An [SPDX](https://spdx.dev/) license expression for the API. The `identifier` field is mutually exclusive of the `url` field. Available since OpenAPI 3.1.0, FastAPI 0.99.0. * `url`: (`str`) A URL to the license used for the API. This MUST be the format of a URL. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more at the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python app = FastAPI( license_info={ "name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html", } ) ``` """ ), ] = None, root_path: Annotated[ str, Doc( """ A path prefix handled by a proxy that is not seen by the application but is seen by external clients, which affects things like Swagger UI. Read more about it at the [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/). **Example** ```python from fastapi import FastAPI app = FastAPI(root_path="/api/v1") ``` """ ), ] = "", root_path_in_servers: Annotated[ bool, Doc( """ To disable automatically generating the URLs in the `servers` field in the autogenerated OpenAPI using the `root_path`. Read more about it in the [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#disable-automatic-server-from-root-path). **Example** ```python from fastapi import FastAPI app = FastAPI(root_path_in_servers=False) ``` """ ), ] = True, responses: Annotated[ dict[int | str, dict[str, Any]] | None, Doc( """ Additional responses to be shown in OpenAPI. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/). And in the [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies). """ ), ] = None, callbacks: Annotated[ list[BaseRoute] | None, Doc( """ OpenAPI callbacks that should apply to all *path operations*. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/). """ ), ] = None, webhooks: Annotated[ routing.APIRouter | None, Doc( """ Add OpenAPI webhooks. This is similar to `callbacks` but it doesn't depend on specific *path operations*. It will be added to the generated OpenAPI (e.g. visible at `/docs`). **Note**: This is available since OpenAPI 3.1.0, FastAPI 0.99.0. Read more about it in the [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/). """ ), ] = None, deprecated: Annotated[ bool | None, Doc( """ Mark all *path operations* as deprecated. You probably don't need it, but it's available. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#deprecate-a-path-operation). """ ), ] = None, include_in_schema: Annotated[ bool, Doc( """ To include (or not) all the *path operations* in the generated OpenAPI. You probably don't need it, but it's available. This affects the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi). """ ), ] = True, swagger_ui_parameters: Annotated[ dict[str, Any] | None, Doc( """ Parameters to configure Swagger UI, the autogenerated interactive API documentation (by default at `/docs`). Read more about it in the [FastAPI docs about how to Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/). """ ), ] = None, generate_unique_id_function: Annotated[ Callable[[routing.APIRoute], str], Doc( """ Customize the function used to generate unique IDs for the *path operations* shown in the generated OpenAPI. This is particularly useful when automatically generating clients or SDKs for your API. Read more about it in the [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function). """ ), ] = Default(generate_unique_id), separate_input_output_schemas: Annotated[ bool, Doc( """ Whether to generate separate OpenAPI schemas for request body and response body when the results would be more precise. This is particularly useful when automatically generating clients. For example, if you have a model like: ```python from pydantic import BaseModel class Item(BaseModel): name: str tags: list[str] = [] ``` When `Item` is used for input, a request body, `tags` is not required, the client doesn't have to provide it. But when using `Item` for output, for a response body, `tags` is always available because it has a default value, even if it's just an empty list. So, the client should be able to always expect it. In this case, there would be two different schemas, one for input and another one for output. Read more about it in the [FastAPI docs about how to separate schemas for input and output](https://fastapi.tiangolo.com/how-to/separate-openapi-schemas) """ ), ] = True, openapi_external_docs: Annotated[ dict[str, Any] | None, Doc( """ This field allows you to provide additional external documentation links. If provided, it must be a dictionary containing: * `description`: A brief description of the external documentation. * `url`: The URL pointing to the external documentation. The value **MUST** be a valid URL format. **Example**: ```python from fastapi import FastAPI external_docs = { "description": "Detailed API Reference", "url": "https://example.com/api-docs", } app = FastAPI(openapi_external_docs=external_docs) ``` """ ), ] = None, strict_content_type: Annotated[ bool, Doc( """ Enable strict checking for request Content-Type headers. When `True` (the default), requests with a body that do not include a `Content-Type` header will **not** be parsed as JSON. This prevents potential cross-site request forgery (CSRF) attacks that exploit the browser's ability to send requests without a Content-Type header, bypassing CORS preflight checks. In particular applicable for apps that need to be run locally (in localhost). When `False`, requests without a `Content-Type` header will have their body parsed as JSON, which maintains compatibility with certain clients that don't send `Content-Type` headers. Read more about it in the [FastAPI docs for Strict Content-Type](https://fastapi.tiangolo.com/advanced/strict-content-type/). """ ), ] = True, ) -> None` (L63~L1018)
- **變更後簽章 (After)**: `def __init__( self: AppType, *, telemetry: Annotated[ TelemetryConfig | None, Doc( """ Native OpenTelemetry configuration as a dictionary. Uses global providers by default. Omitted options keep their defaults. ```python app = FastAPI(telemetry={"tracing": False}) ``` """ ), ] = None, debug: Annotated[ bool, Doc( """ Boolean indicating if debug tracebacks should be returned on server errors. Read more in the [Starlette docs for Applications](https://starlette.dev/applications/#starlette.applications.Starlette). """ ), ] = False, routes: Annotated[ list[BaseRoute] | None, Doc( """ **Note**: you probably shouldn't use this parameter, it is inherited from Starlette and supported for compatibility. --- A list of routes to serve incoming HTTP and WebSocket requests. """ ), deprecated( """ You normally wouldn't use this parameter with FastAPI, it is inherited from Starlette and supported for compatibility. In FastAPI, you normally would use the *path operation methods*, like `app.get()`, `app.post()`, etc. """ ), ] = None, title: Annotated[ str, Doc( """ The title of the API. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI(title="ChimichangApp") ``` """ ), ] = "FastAPI", summary: Annotated[ str | None, Doc( """ A short summary of the API. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI(summary="Deadpond's favorite app. Nuff said.") ``` """ ), ] = None, description: Annotated[ str, Doc( ''' A description of the API. Supports Markdown (using [CommonMark syntax](https://commonmark.org/)). It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI( description=""" ChimichangApp API helps you do awesome stuff. 🚀 ## Items You can **read items**. ## Users You will be able to: * **Create users** (_not implemented_). * **Read users** (_not implemented_). """ ) ``` ''' ), ] = "", version: Annotated[ str, Doc( """ The version of the API. **Note** This is the version of your application, not the version of the OpenAPI specification nor the version of FastAPI being used. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI(version="0.0.1") ``` """ ), ] = "0.1.0", openapi_url: Annotated[ str | None, Doc( """ The URL where the OpenAPI schema will be served from. If you set it to `None`, no OpenAPI schema will be served publicly, and the default automatic endpoints `/docs` and `/redoc` will also be disabled. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url). **Example** ```python from fastapi import FastAPI app = FastAPI(openapi_url="/api/v1/openapi.json") ``` """ ), ] = "/openapi.json", openapi_tags: Annotated[ list[dict[str, Any]] | None, Doc( """ A list of tags used by OpenAPI, these are the same `tags` you can set in the *path operations*, like: * `@app.get("/users/", tags=["users"])` * `@app.get("/items/", tags=["items"])` The order of the tags can be used to specify the order shown in tools like Swagger UI, used in the automatic path `/docs`. It's not required to specify all the tags used. The tags that are not declared MAY be organized randomly or based on the tools' logic. Each tag name in the list MUST be unique. The value of each item is a `dict` containing: * `name`: The name of the tag. * `description`: A short description of the tag. [CommonMark syntax](https://commonmark.org/) MAY be used for rich text representation. * `externalDocs`: Additional external documentation for this tag. If provided, it would contain a `dict` with: * `description`: A short description of the target documentation. [CommonMark syntax](https://commonmark.org/) MAY be used for rich text representation. * `url`: The URL for the target documentation. Value MUST be in the form of a URL. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags). **Example** ```python from fastapi import FastAPI tags_metadata = [ { "name": "users", "description": "Operations with users. The **login** logic is also here.", }, { "name": "items", "description": "Manage items. So _fancy_ they have their own docs.", "externalDocs": { "description": "Items external docs", "url": "https://fastapi.tiangolo.com/", }, }, ] app = FastAPI(openapi_tags=tags_metadata) ``` """ ), ] = None, servers: Annotated[ list[dict[str, str | Any]] | None, Doc( """ A `list` of `dict`s with connectivity information to a target server. You would use it, for example, if your application is served from different domains and you want to use the same Swagger UI in the browser to interact with each of them (instead of having multiple browser tabs open). Or if you want to leave fixed the possible URLs. If the servers `list` is not provided, or is an empty `list`, the `servers` property in the generated OpenAPI will be: * a `dict` with a `url` value of the application's mounting point (`root_path`) if it's different from `/`. * otherwise, the `servers` property will be omitted from the OpenAPI schema. Each item in the `list` is a `dict` containing: * `url`: A URL to the target host. This URL supports Server Variables and MAY be relative, to indicate that the host location is relative to the location where the OpenAPI document is being served. Variable substitutions will be made when a variable is named in `{`brackets`}`. * `description`: An optional string describing the host designated by the URL. [CommonMark syntax](https://commonmark.org/) MAY be used for rich text representation. * `variables`: A `dict` between a variable name and its value. The value is used for substitution in the server's URL template. Read more in the [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#additional-servers). **Example** ```python from fastapi import FastAPI app = FastAPI( servers=[ {"url": "https://stag.example.com", "description": "Staging environment"}, {"url": "https://prod.example.com", "description": "Production environment"}, ] ) ``` """ ), ] = None, dependencies: Annotated[ Sequence[Depends] | None, Doc( """ A list of global dependencies, they will be applied to each *path operation*, including in sub-routers. Read more about it in the [FastAPI docs for Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/). **Example** ```python from fastapi import Depends, FastAPI from .dependencies import func_dep_1, func_dep_2 app = FastAPI(dependencies=[Depends(func_dep_1), Depends(func_dep_2)]) ``` """ ), ] = None, default_response_class: Annotated[ type[Response], Doc( """ The default response class to be used. Read more in the [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class). **Example** ```python from fastapi import FastAPI from fastapi.responses import ORJSONResponse app = FastAPI(default_response_class=ORJSONResponse) ``` """ ), ] = Default(JSONResponse), redirect_slashes: Annotated[ bool, Doc( """ Whether to detect and redirect slashes in URLs when the client doesn't use the same format. **Example** ```python from fastapi import FastAPI app = FastAPI(redirect_slashes=True) # the default @app.get("/items/") async def read_items(): return [{"item_id": "Foo"}] ``` With this app, if a client goes to `/items` (without a trailing slash), they will be automatically redirected with an HTTP status code of 307 to `/items/`. """ ), ] = True, docs_url: Annotated[ str | None, Doc( """ The path to the automatic interactive API documentation. It is handled in the browser by Swagger UI. The default URL is `/docs`. You can disable it by setting it to `None`. If `openapi_url` is set to `None`, this will be automatically disabled. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls). **Example** ```python from fastapi import FastAPI app = FastAPI(docs_url="/documentation", redoc_url=None) ``` """ ), ] = "/docs", redoc_url: Annotated[ str | None, Doc( """ The path to the alternative automatic interactive API documentation provided by ReDoc. The default URL is `/redoc`. You can disable it by setting it to `None`. If `openapi_url` is set to `None`, this will be automatically disabled. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls). **Example** ```python from fastapi import FastAPI app = FastAPI(docs_url="/documentation", redoc_url="redocumentation") ``` """ ), ] = "/redoc", swagger_ui_oauth2_redirect_url: Annotated[ str | None, Doc( """ The OAuth2 redirect endpoint for the Swagger UI. By default it is `/docs/oauth2-redirect`. This is only used if you use OAuth2 (with the "Authorize" button) with Swagger UI. """ ), ] = "/docs/oauth2-redirect", swagger_ui_init_oauth: Annotated[ dict[str, Any] | None, Doc( """ OAuth2 configuration for the Swagger UI, by default shown at `/docs`. Read more about the available configuration options in the [Swagger UI docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/). """ ), ] = None, middleware: Annotated[ Sequence[Middleware] | None, Doc( """ List of middleware to be added when creating the application. In FastAPI you would normally do this with `app.add_middleware()` instead. Read more in the [FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/). """ ), ] = None, exception_handlers: Annotated[ dict[ int | type[Exception], Callable[[Request, Any], Coroutine[Any, Any, Response]], ] | None, Doc( """ A dictionary with handlers for exceptions. In FastAPI, you would normally use the decorator `@app.exception_handler()`. Read more in the [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/). """ ), ] = None, on_startup: Annotated[ Sequence[Callable[[], Any]] | None, Doc( """ A list of startup event handler functions. You should instead use the `lifespan` handlers. Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/). """ ), ] = None, on_shutdown: Annotated[ Sequence[Callable[[], Any]] | None, Doc( """ A list of shutdown event handler functions. You should instead use the `lifespan` handlers. Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/). """ ), ] = None, lifespan: Annotated[ Lifespan[AppType] | None, Doc( """ A `Lifespan` context manager handler. This replaces `startup` and `shutdown` functions with a single context manager. Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/). """ ), ] = None, terms_of_service: Annotated[ str | None, Doc( """ A URL to the Terms of Service for your API. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more at the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python app = FastAPI(terms_of_service="http://example.com/terms/") ``` """ ), ] = None, contact: Annotated[ dict[str, str | Any] | None, Doc( """ A dictionary with the contact information for the exposed API. It can contain several fields. * `name`: (`str`) The name of the contact person/organization. * `url`: (`str`) A URL pointing to the contact information. MUST be in the format of a URL. * `email`: (`str`) The email address of the contact person/organization. MUST be in the format of an email address. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more at the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python app = FastAPI( contact={ "name": "Deadpoolio the Amazing", "url": "http://x-force.example.com/contact/", "email": "dp@x-force.example.com", } ) ``` """ ), ] = None, license_info: Annotated[ dict[str, str | Any] | None, Doc( """ A dictionary with the license information for the exposed API. It can contain several fields. * `name`: (`str`) **REQUIRED** (if a `license_info` is set). The license name used for the API. * `identifier`: (`str`) An [SPDX](https://spdx.dev/) license expression for the API. The `identifier` field is mutually exclusive of the `url` field. Available since OpenAPI 3.1.0, FastAPI 0.99.0. * `url`: (`str`) A URL to the license used for the API. This MUST be the format of a URL. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more at the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python app = FastAPI( license_info={ "name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html", } ) ``` """ ), ] = None, root_path: Annotated[ str, Doc( """ Deprecated. Configure the server with `fastapi run --root-path /api/v1` instead. Read more in the [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/). """ ), deprecated( """ The `root_path` parameter is deprecated. Configure the server's root path instead, for example with `fastapi run --root-path /api/v1`. """ ), ] = "", root_path_in_servers: Annotated[ bool, Doc( """ To disable automatically generating the URLs in the `servers` field in the autogenerated OpenAPI using the `root_path`. Read more about it in the [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#disable-automatic-server-from-root-path). **Example** ```python from fastapi import FastAPI app = FastAPI(root_path_in_servers=False) ``` """ ), ] = True, responses: Annotated[ dict[int | str, dict[str, Any]] | None, Doc( """ Additional responses to be shown in OpenAPI. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/). And in the [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies). """ ), ] = None, callbacks: Annotated[ list[BaseRoute] | None, Doc( """ OpenAPI callbacks that should apply to all *path operations*. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/). """ ), ] = None, webhooks: Annotated[ routing.APIRouter | None, Doc( """ Add OpenAPI webhooks. This is similar to `callbacks` but it doesn't depend on specific *path operations*. It will be added to the generated OpenAPI (e.g. visible at `/docs`). **Note**: This is available since OpenAPI 3.1.0, FastAPI 0.99.0. Read more about it in the [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/). """ ), ] = None, deprecated: Annotated[ bool | None, Doc( """ Mark all *path operations* as deprecated. You probably don't need it, but it's available. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#deprecate-a-path-operation). """ ), ] = None, include_in_schema: Annotated[ bool, Doc( """ To include (or not) all the *path operations* in the generated OpenAPI. You probably don't need it, but it's available. This affects the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi). """ ), ] = True, swagger_ui_parameters: Annotated[ dict[str, Any] | None, Doc( """ Parameters to configure Swagger UI, the autogenerated interactive API documentation (by default at `/docs`). Read more about it in the [FastAPI docs about how to Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/). """ ), ] = None, generate_unique_id_function: Annotated[ Callable[[routing.APIRoute], str], Doc( """ Customize the function used to generate unique IDs for the *path operations* shown in the generated OpenAPI. This is particularly useful when automatically generating clients or SDKs for your API. Read more about it in the [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function). """ ), ] = Default(generate_unique_id), separate_input_output_schemas: Annotated[ bool, Doc( """ Whether to generate separate OpenAPI schemas for request body and response body when the results would be more precise. This is particularly useful when automatically generating clients. For example, if you have a model like: ```python from pydantic import BaseModel class Item(BaseModel): name: str tags: list[str] = [] ``` When `Item` is used for input, a request body, `tags` is not required, the client doesn't have to provide it. But when using `Item` for output, for a response body, `tags` is always available because it has a default value, even if it's just an empty list. So, the client should be able to always expect it. In this case, there would be two different schemas, one for input and another one for output. Read more about it in the [FastAPI docs about how to separate schemas for input and output](https://fastapi.tiangolo.com/how-to/separate-openapi-schemas) """ ), ] = True, openapi_external_docs: Annotated[ dict[str, Any] | None, Doc( """ This field allows you to provide additional external documentation links. If provided, it must be a dictionary containing: * `description`: A brief description of the external documentation. * `url`: The URL pointing to the external documentation. The value **MUST** be a valid URL format. **Example**: ```python from fastapi import FastAPI external_docs = { "description": "Detailed API Reference", "url": "https://example.com/api-docs", } app = FastAPI(openapi_external_docs=external_docs) ``` """ ), ] = None, strict_content_type: Annotated[ bool, Doc( """ Enable strict checking for request Content-Type headers. When `True` (the default), requests with a body that do not include a `Content-Type` header will **not** be parsed as JSON. This prevents potential cross-site request forgery (CSRF) attacks that exploit the browser's ability to send requests without a Content-Type header, bypassing CORS preflight checks. In particular applicable for apps that need to be run locally (in localhost). When `False`, requests without a `Content-Type` header will have their body parsed as JSON, which maintains compatibility with certain clients that don't send `Content-Type` headers. Read more about it in the [FastAPI docs for Strict Content-Type](https://fastapi.tiangolo.com/advanced/strict-content-type/). """ ), ] = True, ) -> None` (L68~L1030)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self: AppType,
        *,
        telemetry: Annotated[
            TelemetryConfig | None,
            Doc(
                """
                Native OpenTelemetry configuration as a dictionary. Uses global
                providers by default. Omitted options keep their defaults.

                ```python
                app = FastAPI(telemetry={"tracing": False})
                ```
                """
            ),
        ] = None,
        debug: Annotated[
            bool,
            Doc(
                """
                Boolean indicating if debug tracebacks should be returned on server
                errors.

                Read more in the
                [Starlette docs for Applications](https://starlette.dev/applications/#starlette.applications.Starlette).
                """
            ),
        ] = False,
        routes: Annotated[
            list[BaseRoute] | None,
            Doc(
                """
                **Note**: you probably shouldn't use this parameter, it is inherited
                from Starlette and supported for compatibility.

                ---

                A list of routes to serve incoming HTTP and WebSocket requests.
                """
            ),
            deprecated(
                """
                You normally wouldn't use this parameter with FastAPI, it is inherited
                from Starlette and supported for compatibility.

                In FastAPI, you normally would use the *path operation methods*,
                like `app.get()`, `app.post()`, etc.
                """
            ),
        ] = None,
        title: Annotated[
            str,
            Doc(
                """
                The title of the API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(title="ChimichangApp")
                ```
                """
            ),
        ] = "FastAPI",
        summary: Annotated[
            str | None,
            Doc(
                """
                A short summary of the API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(summary="Deadpond's favorite app. Nuff said.")
                ```
                """
            ),
        ] = None,
        description: Annotated[
            str,
            Doc(
                '''
                A description of the API. Supports Markdown (using
                [CommonMark syntax](https://commonmark.org/)).

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(
                    description="""
                                ChimichangApp API helps you do awesome stuff. 🚀

                                ## Items

                                You can **read items**.

                                ## Users

                                You will be able to:

                                * **Create users** (_not implemented_).
                                * **Read users** (_not implemented_).

                                """
                )
                ```
                '''
            ),
        ] = "",
        version: Annotated[
            str,
            Doc(
                """
                The version of the API.

                **Note** This is the version of your application, not the version of
                the OpenAPI specification nor the version of FastAPI being used.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(version="0.0.1")
                ```
                """
            ),
        ] = "0.1.0",
        openapi_url: Annotated[
            str | None,
            Doc(
                """
                The URL where the OpenAPI schema will be served from.

                If you set it to `None`, no OpenAPI schema will be served publicly, and
                the default automatic endpoints `/docs` and `/redoc` will also be
                disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(openapi_url="/api/v1/openapi.json")
                ```
                """
            ),
        ] = "/openapi.json",
        openapi_tags: Annotated[
            list[dict[str, Any]] | None,
            Doc(
                """
                A list of tags used by OpenAPI, these are the same `tags` you can set
                in the *path operations*, like:

                * `@app.get("/users/", tags=["users"])`
                * `@app.get("/items/", tags=["items"])`

                The order of the tags can be used to specify the order shown in
                tools like Swagger UI, used in the automatic path `/docs`.

                It's not required to specify all the tags used.

                The tags that are not declared MAY be organized randomly or based
                on the tools' logic. Each tag name in the list MUST be unique.

                The value of each item is a `dict` containing:

                * `name`: The name of the tag.
                * `description`: A short description of the tag.
                    [CommonMark syntax](https://commonmark.org/) MAY be used for rich
                    text representation.
                * `externalDocs`: Additional external documentation for this tag. If
                    provided, it would contain a `dict` with:
                    * `description`: A short description of the target documentation.
                        [CommonMark syntax](https://commonmark.org/) MAY be used for
                        rich text representation.
                    * `url`: The URL for the target documentation. Value MUST be in
                        the form of a URL.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags).

                **Example**

                ```python
                from fastapi import FastAPI

                tags_metadata = [
                    {
                        "name": "users",
                        "description": "Operations with users. The **login** logic is also here.",
                    },
                    {
                        "name": "items",
                        "description": "Manage items. So _fancy_ they have their own docs.",
                        "externalDocs": {
                            "description": "Items external docs",
                            "url": "https://fastapi.tiangolo.com/",
                        },
                    },
                ]

                app = FastAPI(openapi_tags=tags_metadata)
                ```
                """
            ),
        ] = None,
        servers: Annotated[
            list[dict[str, str | Any]] | None,
            Doc(
                """
                A `list` of `dict`s with connectivity information to a target server.

                You would use it, for example, if your application is served from
                different domains and you want to use the same Swagger UI in the
                browser to interact with each of them (instead of having multiple
                browser tabs open). Or if you want to leave fixed the possible URLs.

                If the servers `list` is not provided, or is an empty `list`, the
                `servers` property in the generated OpenAPI will be:

                * a `dict` with a `url` value of the application's mounting point
                (`root_path`) if it's different from `/`.
                * otherwise, the `servers` property will be omitted from the OpenAPI
                schema.

                Each item in the `list` is a `dict` containing:

                * `url`: A URL to the target host. This URL supports Server Variables
                and MAY be relative, to indicate that the host location is relative
                to the location where the OpenAPI document is being served. Variable
                substitutions will be made when a variable is named in `{`brackets`}`.
                * `description`: An optional string describing the host designated by
                the URL. [CommonMark syntax](https://commonmark.org/) MAY be used for
                rich text representation.
                * `variables`: A `dict` between a variable name and its value. The value
                    is used for substitution in the server's URL template.

                Read more in the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#additional-servers).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(
                    servers=[
                        {"url": "https://stag.example.com", "description": "Staging environment"},
                        {"url": "https://prod.example.com", "description": "Production environment"},
                    ]
                )
                ```
                """
            ),
        ] = None,
        dependencies: Annotated[
            Sequence[Depends] | None,
            Doc(
                """
                A list of global dependencies, they will be applied to each
                *path operation*, including in sub-routers.

                Read more about it in the
                [FastAPI docs for Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/).

                **Example**

                ```python
                from fastapi import Depends, FastAPI

                from .dependencies import func_dep_1, func_dep_2

                app = FastAPI(dependencies=[Depends(func_dep_1), Depends(func_dep_2)])
                ```
                """
            ),
        ] = None,
        default_response_class: Annotated[
            type[Response],
            Doc(
                """
                The default response class to be used.

                Read more in the
                [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).

                **Example**

                ```python
                from fastapi import FastAPI
                from fastapi.responses import ORJSONResponse

                app = FastAPI(default_response_class=ORJSONResponse)
                ```
                """
            ),
        ] = Default(JSONResponse),
        redirect_slashes: Annotated[
            bool,
            Doc(
                """
                Whether to detect and redirect slashes in URLs when the client doesn't
                use the same format.

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(redirect_slashes=True)  # the default

                @app.get("/items/")
                async def read_items():
                    return [{"item_id": "Foo"}]
                ```

                With this app, if a client goes to `/items` (without a trailing slash),
                they will be automatically redirected with an HTTP status code of 307
                to `/items/`.
                """
            ),
        ] = True,
        docs_url: Annotated[
            str | None,
            Doc(
                """
                The path to the automatic interactive API documentation.
                It is handled in the browser by Swagger UI.

                The default URL is `/docs`. You can disable it by setting it to `None`.

                If `openapi_url` is set to `None`, this will be automatically disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(docs_url="/documentation", redoc_url=None)
                ```
                """
            ),
        ] = "/docs",
        redoc_url: Annotated[
            str | None,
            Doc(
                """
                The path to the alternative automatic interactive API documentation
                provided by ReDoc.

                The default URL is `/redoc`. You can disable it by setting it to `None`.

                If `openapi_url` is set to `None`, this will be automatically disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(docs_url="/documentation", redoc_url="redocumentation")
                ```
                """
            ),
        ] = "/redoc",
        swagger_ui_oauth2_redirect_url: Annotated[
            str | None,
            Doc(
                """
                The OAuth2 redirect endpoint for the Swagger UI.

                By default it is `/docs/oauth2-redirect`.

                This is only used if you use OAuth2 (with the "Authorize" button)
                with Swagger UI.
                """
            ),
        ] = "/docs/oauth2-redirect",
        swagger_ui_init_oauth: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                OAuth2 configuration for the Swagger UI, by default shown at `/docs`.

                Read more about the available configuration options in the
                [Swagger UI docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/).
                """
            ),
        ] = None,
        middleware: Annotated[
            Sequence[Middleware] | None,
            Doc(
                """
                List of middleware to be added when creating the application.

                In FastAPI you would normally do this with `app.add_middleware()`
                instead.

                Read more in the
                [FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/).
                """
            ),
        ] = None,
        exception_handlers: Annotated[
            dict[
                int | type[Exception],
                Callable[[Request, Any], Coroutine[Any, Any, Response]],
            ]
            | None,
            Doc(
                """
                A dictionary with handlers for exceptions.

                In FastAPI, you would normally use the decorator
                `@app.exception_handler()`.

                Read more in the
                [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).
                """
            ),
        ] = None,
        on_startup: Annotated[
            Sequence[Callable[[], Any]] | None,
            Doc(
                """
                A list of startup event handler functions.

                You should instead use the `lifespan` handlers.

                Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        on_shutdown: Annotated[
            Sequence[Callable[[], Any]] | None,
            Doc(
                """
                A list of shutdown event handler functions.

                You should instead use the `lifespan` handlers.

                Read more in the
                [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        lifespan: Annotated[
            Lifespan[AppType] | None,
            Doc(
                """
                A `Lifespan` context manager handler. This replaces `startup` and
                `shutdown` functions with a single context manager.

                Read more in the
                [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        terms_of_service: Annotated[
            str | None,
            Doc(
                """
                A URL to the Terms of Service for your API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more at the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                app = FastAPI(terms_of_service="http://example.com/terms/")
                ```
                """
            ),
        ] = None,
        contact: Annotated[
            dict[str, str | Any] | None,
            Doc(
                """
                A dictionary with the contact information for the exposed API.

                It can contain several fields.

                * `name`: (`str`) The name of the contact person/organization.
                * `url`: (`str`) A URL pointing to the contact information. MUST be in
                    the format of a URL.
                * `email`: (`str`) The email address of the contact person/organization.
                    MUST be in the format of an email address.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more at the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                app = FastAPI(
                    contact={
                        "name": "Deadpoolio the Amazing",
                        "url": "http://x-force.example.com/contact/",
                        "email": "dp@x-force.example.com",
                    }
                )
                ```
                """
            ),
        ] = None,
        license_info: Annotated[
            dict[str, str | Any] | None,
            Doc(
                """
                A dictionary with the license information for the exposed API.

                It can contain several fields.

                * `name`: (`str`) **REQUIRED** (if a `license_info` is set). The
                    license name used for the API.
                * `identifier`: (`str`) An [SPDX](https://spdx.dev/) license expression
                    for the API. The `identifier` field is mutually exclusive of the `url`
                    field. Available since OpenAPI 3.1.0, FastAPI 0.99.0.
                * `url`: (`str`) A URL to the license used for the API. This MUST be
                    the format of a URL.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more at the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                app = FastAPI(
                    license_info={
                        "name": "Apache 2.0",
                        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                    }
                )
                ```
                """
            ),
        ] = None,
        root_path: Annotated[
            str,
            Doc(
                """
                A path prefix handled by a proxy that is not seen by the application
                but is seen by external clients, which affects things like Swagger UI.

                Read more about it at the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(root_path="/api/v1")
                ```
                """
            ),
        ] = "",
        root_path_in_servers: Annotated[
            bool,
            Doc(
                """
                To disable automatically generating the URLs in the `servers` field
                in the autogenerated OpenAPI using the `root_path`.

                Read more about it in the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#disable-automatic-server-from-root-path).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(root_path_in_servers=False)
                ```
                """
            ),
        ] = True,
        responses: Annotated[
            dict[int | str, dict[str, Any]] | None,
            Doc(
                """
                Additional responses to be shown in OpenAPI.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).

                And in the
                [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
                """
            ),
        ] = None,
        callbacks: Annotated[
            list[BaseRoute] | None,
            Doc(
                """
                OpenAPI callbacks that should apply to all *path operations*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                """
            ),
        ] = None,
        webhooks: Annotated[
            routing.APIRouter | None,
            Doc(
                """
                Add OpenAPI webhooks. This is similar to `callbacks` but it doesn't
                depend on specific *path operations*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                **Note**: This is available since OpenAPI 3.1.0, FastAPI 0.99.0.

                Read more about it in the
                [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/).
                """
            ),
        ] = None,
        deprecated: Annotated[
            bool | None,
            Doc(
                """
                Mark all *path operations* as deprecated. You probably don't need it,
                but it's available.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#deprecate-a-path-operation).
                """
            ),
        ] = None,
        include_in_schema: Annotated[
            bool,
            Doc(
                """
                To include (or not) all the *path operations* in the generated OpenAPI.
                You probably don't need it, but it's available.

                This affects the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi).
                """
            ),
        ] = True,
        swagger_ui_parameters: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                Parameters to configure Swagger UI, the autogenerated interactive API
                documentation (by default at `/docs`).

                Read more about it in the
                [FastAPI docs about how to Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/).
                """
            ),
        ] = None,
        generate_unique_id_function: Annotated[
            Callable[[routing.APIRoute], str],
            Doc(
                """
                Customize the function used to generate unique IDs for the *path
                operations* shown in the generated OpenAPI.

                This is particularly useful when automatically generating clients or
                SDKs for your API.

                Read more about it in the
                [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                """
            ),
        ] = Default(generate_unique_id),
        separate_input_output_schemas: Annotated[
            bool,
            Doc(
                """
                Whether to generate separate OpenAPI schemas for request body and
                response body when the results would be more precise.

                This is particularly useful when automatically generating clients.

                For example, if you have a model like:

                ```python
                from pydantic import BaseModel

                class Item(BaseModel):
                    name: str
                    tags: list[str] = []
                ```

                When `Item` is used for input, a request body, `tags` is not required,
                the client doesn't have to provide it.

                But when using `Item` for output, for a response body, `tags` is always
                available because it has a default value, even if it's just an empty
                list. So, the client should be able to always expect it.

                In this case, there would be two different schemas, one for input and
                another one for output.

                Read more about it in the
                [FastAPI docs about how to separate schemas for input and output](https://fastapi.tiangolo.com/how-to/separate-openapi-schemas)
                """
            ),
        ] = True,
        openapi_external_docs: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                This field allows you to provide additional external documentation links.
                If provided, it must be a dictionary containing:

                * `description`: A brief description of the external documentation.
                * `url`: The URL pointing to the external documentation. The value **MUST**
                be a valid URL format.

                **Example**:

                ```python
                from fastapi import FastAPI

                external_docs = {
                    "description": "Detailed API Reference",
                    "url": "https://example.com/api-docs",
                }

                app = FastAPI(openapi_external_docs=external_docs)
                ```
                """
            ),
        ] = None,
        strict_content_type: Annotated[
            bool,
            Doc(
                """
                Enable strict checking for request Content-Type headers.

                When `True` (the default), requests with a body that do not include
                a `Content-Type` header will **not** be parsed as JSON.

                This prevents potential cross-site request forgery (CSRF) attacks
                that exploit the browser's ability to send requests without a
                Content-Type header, bypassing CORS preflight checks. In particular
                applicable for apps that need to be run locally (in localhost).

                When `False`, requests without a `Content-Type` header will have
                their body parsed as JSON, which maintains compatibility with
                certain clients that don't send `Content-Type` headers.

                Read more about it in the
                [FastAPI docs for Strict Content-Type](https://fastapi.tiangolo.com/advanced/strict-content-type/).
                """
            ),
        ] = True,
    ) -> None:
        self.debug = debug
        self.title = title
        self.summary = summary
        self.description = description
        self.version = version
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license_info = license_info
        self.openapi_url = openapi_url
        self.openapi_tags = openapi_tags
        self.root_path_in_servers = root_path_in_servers
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.swagger_ui_oauth2_redirect_url = swagger_ui_oauth2_redirect_url
        self.swagger_ui_init_oauth = swagger_ui_init_oauth
        self.swagger_ui_parameters = swagger_ui_parameters
        self.servers = servers or []
        self.separate_input_output_schemas = separate_input_output_schemas
        self.openapi_external_docs = openapi_external_docs
        self.openapi_version: Annotated[
            str,
            Doc(
                """
                The version string of OpenAPI.

                FastAPI will generate OpenAPI version 3.1.0, and will output that as
                the OpenAPI version. But some tools, even though they might be
                compatible with OpenAPI 3.1.0, might not recognize it as a valid.

                So you could override this value to trick those tools into using
                the generated OpenAPI. Have in mind that this is a hack. But if you
                avoid using features added in OpenAPI 3.1.0, it might work for your
                use case.

                This is not passed as a parameter to the `FastAPI` class to avoid
                giving the false idea that FastAPI would generate a different OpenAPI
                schema. It is only available as an attribute.

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI()

                app.openapi_version = "3.0.2"
                ```
                """
            ),
        ] = "3.1.0"
        self.openapi_schema: dict[str, Any] | None = None
        self._openapi_routes_version: int | None = None
        if self.openapi_url:
            assert self.title, "A title must be provided for OpenAPI, e.g.: 'My API'"
            assert self.version, "A version must be provided for OpenAPI, e.g.: '2.1.0'"
        self.webhooks: Annotated[
            routing.APIRouter,
            Doc(
                """
                The `app.webhooks` attribute is an `APIRouter` with the *path
                operations* that will be used just for documentation of webhooks.

                Read more about it in the
                [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/).
                """
            ),
        ] = webhooks or routing.APIRouter()
        self.root_path = root_path
        self.state: Annotated[
            State,
            Doc(
                """
                A state object for the application. This is the same object for the
                entire application, it doesn't change from request to request.

                You normally wouldn't use this in FastAPI, for most of the cases you
                would instead use FastAPI dependencies.

                This is simply inherited from Starlette.

                Read more about it in the
                [Starlette docs for Applications](https://starlette.dev/applications/#storing-state-on-the-app-instance).
                """
            ),
        ] = State()
        self.dependency_overrides: Annotated[
            dict[Callable[..., Any], Callable[..., Any]],
            Doc(
                """
                A dictionary with overrides for the dependencies.

                Each key is the original dependency callable, and the value is the
                actual dependency that should be called.

                This is for testing, to replace expensive dependencies with testing
                versions.

                Read more about it in the
                [FastAPI docs for Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/).
                """
            ),
        ] = {}
        self.router: routing.APIRouter = routing.APIRouter(
            routes=routes,
            redirect_slashes=redirect_slashes,
            dependency_overrides_provider=self,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            default_response_class=default_response_class,
            dependencies=dependencies,
            callbacks=callbacks,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            responses=responses,
            generate_unique_id_function=generate_unique_id_function,
            strict_content_type=strict_content_type,
        )
        self.exception_handlers: dict[
            Any, Callable[[Request, Any], Response | Awaitable[Response]]
        ] = {} if exception_handlers is None else dict(exception_handlers)
        self.exception_handlers.setdefault(HTTPException, http_exception_handler)
        self.exception_handlers.setdefault(
            RequestValidationError, request_validation_exception_handler
        )

        # Starlette still has incorrect type specification for the handlers
        self.exception_handlers.setdefault(
            WebSocketRequestValidationError,
            websocket_request_validation_exception_handler,  # type: ignore[arg-type]
        )  # ty: ignore[no-matching-overload]

        self._telemetry: TelemetryConfig = {
            "tracer_provider": None,
            "meter_provider": None,
            "logger_provider": None,
            "tracing": True,
            "metrics": True,
            "logs": True,
            "operation_spans": True,
            "auto_configure": os.getenv("FASTAPI_OTEL_AUTO_CONFIGURE", "").lower()
            == "true",
            "exclude": None,
            **(telemetry if telemetry is not None else {}),
        }
        self._native_telemetry = NativeTelemetry(self._telemetry)

        self.user_middleware: list[Middleware] = (
            [] if middleware is None else list(middleware)
        )
        self.middleware_stack: ASGIApp | None = None
        self.setup()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self: AppType,
        *,
        telemetry: Annotated[
            TelemetryConfig | None,
            Doc(
                """
                Native OpenTelemetry configuration as a dictionary. Uses global
                providers by default. Omitted options keep their defaults.

                ```python
                app = FastAPI(telemetry={"tracing": False})
                ```
                """
            ),
        ] = None,
        debug: Annotated[
            bool,
            Doc(
                """
                Boolean indicating if debug tracebacks should be returned on server
                errors.

                Read more in the
                [Starlette docs for Applications](https://starlette.dev/applications/#starlette.applications.Starlette).
                """
            ),
        ] = False,
        routes: Annotated[
            list[BaseRoute] | None,
            Doc(
                """
                **Note**: you probably shouldn't use this parameter, it is inherited
                from Starlette and supported for compatibility.

                ---

                A list of routes to serve incoming HTTP and WebSocket requests.
                """
            ),
            deprecated(
                """
                You normally wouldn't use this parameter with FastAPI, it is inherited
                from Starlette and supported for compatibility.

                In FastAPI, you normally would use the *path operation methods*,
                like `app.get()`, `app.post()`, etc.
                """
            ),
        ] = None,
        title: Annotated[
            str,
            Doc(
                """
                The title of the API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(title="ChimichangApp")
                ```
                """
            ),
        ] = "FastAPI",
        summary: Annotated[
            str | None,
            Doc(
                """
                A short summary of the API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(summary="Deadpond's favorite app. Nuff said.")
                ```
                """
            ),
        ] = None,
        description: Annotated[
            str,
            Doc(
                '''
                A description of the API. Supports Markdown (using
                [CommonMark syntax](https://commonmark.org/)).

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(
                    description="""
                                ChimichangApp API helps you do awesome stuff. 🚀

                                ## Items

                                You can **read items**.

                                ## Users

                                You will be able to:

                                * **Create users** (_not implemented_).
                                * **Read users** (_not implemented_).

                                """
                )
                ```
                '''
            ),
        ] = "",
        version: Annotated[
            str,
            Doc(
                """
                The version of the API.

                **Note** This is the version of your application, not the version of
                the OpenAPI specification nor the version of FastAPI being used.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(version="0.0.1")
                ```
                """
            ),
        ] = "0.1.0",
        openapi_url: Annotated[
            str | None,
            Doc(
                """
                The URL where the OpenAPI schema will be served from.

                If you set it to `None`, no OpenAPI schema will be served publicly, and
                the default automatic endpoints `/docs` and `/redoc` will also be
                disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(openapi_url="/api/v1/openapi.json")
                ```
                """
            ),
        ] = "/openapi.json",
        openapi_tags: Annotated[
            list[dict[str, Any]] | None,
            Doc(
                """
                A list of tags used by OpenAPI, these are the same `tags` you can set
                in the *path operations*, like:

                * `@app.get("/users/", tags=["users"])`
                * `@app.get("/items/", tags=["items"])`

                The order of the tags can be used to specify the order shown in
                tools like Swagger UI, used in the automatic path `/docs`.

                It's not required to specify all the tags used.

                The tags that are not declared MAY be organized randomly or based
                on the tools' logic. Each tag name in the list MUST be unique.

                The value of each item is a `dict` containing:

                * `name`: The name of the tag.
                * `description`: A short description of the tag.
                    [CommonMark syntax](https://commonmark.org/) MAY be used for rich
                    text representation.
                * `externalDocs`: Additional external documentation for this tag. If
                    provided, it would contain a `dict` with:
                    * `description`: A short description of the target documentation.
                        [CommonMark syntax](https://commonmark.org/) MAY be used for
                        rich text representation.
                    * `url`: The URL for the target documentation. Value MUST be in
                        the form of a URL.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags).

                **Example**

                ```python
                from fastapi import FastAPI

                tags_metadata = [
                    {
                        "name": "users",
                        "description": "Operations with users. The **login** logic is also here.",
                    },
                    {
                        "name": "items",
                        "description": "Manage items. So _fancy_ they have their own docs.",
                        "externalDocs": {
                            "description": "Items external docs",
                            "url": "https://fastapi.tiangolo.com/",
                        },
                    },
                ]

                app = FastAPI(openapi_tags=tags_metadata)
                ```
                """
            ),
        ] = None,
        servers: Annotated[
            list[dict[str, str | Any]] | None,
            Doc(
                """
                A `list` of `dict`s with connectivity information to a target server.

                You would use it, for example, if your application is served from
                different domains and you want to use the same Swagger UI in the
                browser to interact with each of them (instead of having multiple
                browser tabs open). Or if you want to leave fixed the possible URLs.

                If the servers `list` is not provided, or is an empty `list`, the
                `servers` property in the generated OpenAPI will be:

                * a `dict` with a `url` value of the application's mounting point
                (`root_path`) if it's different from `/`.
                * otherwise, the `servers` property will be omitted from the OpenAPI
                schema.

                Each item in the `list` is a `dict` containing:

                * `url`: A URL to the target host. This URL supports Server Variables
                and MAY be relative, to indicate that the host location is relative
                to the location where the OpenAPI document is being served. Variable
                substitutions will be made when a variable is named in `{`brackets`}`.
                * `description`: An optional string describing the host designated by
                the URL. [CommonMark syntax](https://commonmark.org/) MAY be used for
                rich text representation.
                * `variables`: A `dict` between a variable name and its value. The value
                    is used for substitution in the server's URL template.

                Read more in the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#additional-servers).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(
                    servers=[
                        {"url": "https://stag.example.com", "description": "Staging environment"},
                        {"url": "https://prod.example.com", "description": "Production environment"},
                    ]
                )
                ```
                """
            ),
        ] = None,
        dependencies: Annotated[
            Sequence[Depends] | None,
            Doc(
                """
                A list of global dependencies, they will be applied to each
                *path operation*, including in sub-routers.

                Read more about it in the
                [FastAPI docs for Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/).

                **Example**

                ```python
                from fastapi import Depends, FastAPI

                from .dependencies import func_dep_1, func_dep_2

                app = FastAPI(dependencies=[Depends(func_dep_1), Depends(func_dep_2)])
                ```
                """
            ),
        ] = None,
        default_response_class: Annotated[
            type[Response],
            Doc(
                """
                The default response class to be used.

                Read more in the
                [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).

                **Example**

                ```python
                from fastapi import FastAPI
                from fastapi.responses import ORJSONResponse

                app = FastAPI(default_response_class=ORJSONResponse)
                ```
                """
            ),
        ] = Default(JSONResponse),
        redirect_slashes: Annotated[
            bool,
            Doc(
                """
                Whether to detect and redirect slashes in URLs when the client doesn't
                use the same format.

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(redirect_slashes=True)  # the default

                @app.get("/items/")
                async def read_items():
                    return [{"item_id": "Foo"}]
                ```

                With this app, if a client goes to `/items` (without a trailing slash),
                they will be automatically redirected with an HTTP status code of 307
                to `/items/`.
                """
            ),
        ] = True,
        docs_url: Annotated[
            str | None,
            Doc(
                """
                The path to the automatic interactive API documentation.
                It is handled in the browser by Swagger UI.

                The default URL is `/docs`. You can disable it by setting it to `None`.

                If `openapi_url` is set to `None`, this will be automatically disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(docs_url="/documentation", redoc_url=None)
                ```
                """
            ),
        ] = "/docs",
        redoc_url: Annotated[
            str | None,
            Doc(
                """
                The path to the alternative automatic interactive API documentation
                provided by ReDoc.

                The default URL is `/redoc`. You can disable it by setting it to `None`.

                If `openapi_url` is set to `None`, this will be automatically disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(docs_url="/documentation", redoc_url="redocumentation")
                ```
                """
            ),
        ] = "/redoc",
        swagger_ui_oauth2_redirect_url: Annotated[
            str | None,
            Doc(
                """
                The OAuth2 redirect endpoint for the Swagger UI.

                By default it is `/docs/oauth2-redirect`.

                This is only used if you use OAuth2 (with the "Authorize" button)
                with Swagger UI.
                """
            ),
        ] = "/docs/oauth2-redirect",
        swagger_ui_init_oauth: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                OAuth2 configuration for the Swagger UI, by default shown at `/docs`.

                Read more about the available configuration options in the
                [Swagger UI docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/).
                """
            ),
        ] = None,
        middleware: Annotated[
            Sequence[Middleware] | None,
            Doc(
                """
                List of middleware to be added when creating the application.

                In FastAPI you would normally do this with `app.add_middleware()`
                instead.

                Read more in the
                [FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/).
                """
            ),
        ] = None,
        exception_handlers: Annotated[
            dict[
                int | type[Exception],
                Callable[[Request, Any], Coroutine[Any, Any, Response]],
            ]
            | None,
            Doc(
                """
                A dictionary with handlers for exceptions.

                In FastAPI, you would normally use the decorator
                `@app.exception_handler()`.

                Read more in the
                [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).
                """
            ),
        ] = None,
        on_startup: Annotated[
            Sequence[Callable[[], Any]] | None,
            Doc(
                """
                A list of startup event handler functions.

                You should instead use the `lifespan` handlers.

                Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        on_shutdown: Annotated[
            Sequence[Callable[[], Any]] | None,
            Doc(
                """
                A list of shutdown event handler functions.

                You should instead use the `lifespan` handlers.

                Read more in the
                [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        lifespan: Annotated[
            Lifespan[AppType] | None,
            Doc(
                """
                A `Lifespan` context manager handler. This replaces `startup` and
                `shutdown` functions with a single context manager.

                Read more in the
                [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        terms_of_service: Annotated[
            str | None,
            Doc(
                """
                A URL to the Terms of Service for your API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more at the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                app = FastAPI(terms_of_service="http://example.com/terms/")
                ```
                """
            ),
        ] = None,
        contact: Annotated[
            dict[str, str | Any] | None,
            Doc(
                """
                A dictionary with the contact information for the exposed API.

                It can contain several fields.

                * `name`: (`str`) The name of the contact person/organization.
                * `url`: (`str`) A URL pointing to the contact information. MUST be in
                    the format of a URL.
                * `email`: (`str`) The email address of the contact person/organization.
                    MUST be in the format of an email address.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more at the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                app = FastAPI(
                    contact={
                        "name": "Deadpoolio the Amazing",
                        "url": "http://x-force.example.com/contact/",
                        "email": "dp@x-force.example.com",
                    }
                )
                ```
                """
            ),
        ] = None,
        license_info: Annotated[
            dict[str, str | Any] | None,
            Doc(
                """
                A dictionary with the license information for the exposed API.

                It can contain several fields.

                * `name`: (`str`) **REQUIRED** (if a `license_info` is set). The
                    license name used for the API.
                * `identifier`: (`str`) An [SPDX](https://spdx.dev/) license expression
                    for the API. The `identifier` field is mutually exclusive of the `url`
                    field. Available since OpenAPI 3.1.0, FastAPI 0.99.0.
                * `url`: (`str`) A URL to the license used for the API. This MUST be
                    the format of a URL.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more at the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                app = FastAPI(
                    license_info={
                        "name": "Apache 2.0",
                        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                    }
                )
                ```
                """
            ),
        ] = None,
        root_path: Annotated[
            str,
            Doc(
                """
                Deprecated. Configure the server with
                `fastapi run --root-path /api/v1` instead.

                Read more in the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/).
                """
            ),
            deprecated(
                """
                The `root_path` parameter is deprecated. Configure the server's
                root path instead, for example with
                `fastapi run --root-path /api/v1`.
                """
            ),
        ] = "",
        root_path_in_servers: Annotated[
            bool,
            Doc(
                """
                To disable automatically generating the URLs in the `servers` field
                in the autogenerated OpenAPI using the `root_path`.

                Read more about it in the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#disable-automatic-server-from-root-path).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(root_path_in_servers=False)
                ```
                """
            ),
        ] = True,
        responses: Annotated[
            dict[int | str, dict[str, Any]] | None,
            Doc(
                """
                Additional responses to be shown in OpenAPI.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).

                And in the
                [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
                """
            ),
        ] = None,
        callbacks: Annotated[
            list[BaseRoute] | None,
            Doc(
                """
                OpenAPI callbacks that should apply to all *path operations*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                """
            ),
        ] = None,
        webhooks: Annotated[
            routing.APIRouter | None,
            Doc(
                """
                Add OpenAPI webhooks. This is similar to `callbacks` but it doesn't
                depend on specific *path operations*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                **Note**: This is available since OpenAPI 3.1.0, FastAPI 0.99.0.

                Read more about it in the
                [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/).
                """
            ),
        ] = None,
        deprecated: Annotated[
            bool | None,
            Doc(
                """
                Mark all *path operations* as deprecated. You probably don't need it,
                but it's available.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#deprecate-a-path-operation).
                """
            ),
        ] = None,
        include_in_schema: Annotated[
            bool,
            Doc(
                """
                To include (or not) all the *path operations* in the generated OpenAPI.
                You probably don't need it, but it's available.

                This affects the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi).
                """
            ),
        ] = True,
        swagger_ui_parameters: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                Parameters to configure Swagger UI, the autogenerated interactive API
                documentation (by default at `/docs`).

                Read more about it in the
                [FastAPI docs about how to Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/).
                """
            ),
        ] = None,
        generate_unique_id_function: Annotated[
            Callable[[routing.APIRoute], str],
            Doc(
                """
                Customize the function used to generate unique IDs for the *path
                operations* shown in the generated OpenAPI.

                This is particularly useful when automatically generating clients or
                SDKs for your API.

                Read more about it in the
                [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                """
            ),
        ] = Default(generate_unique_id),
        separate_input_output_schemas: Annotated[
            bool,
            Doc(
                """
                Whether to generate separate OpenAPI schemas for request body and
                response body when the results would be more precise.

                This is particularly useful when automatically generating clients.

                For example, if you have a model like:

                ```python
                from pydantic import BaseModel

                class Item(BaseModel):
                    name: str
                    tags: list[str] = []
                ```

                When `Item` is used for input, a request body, `tags` is not required,
                the client doesn't have to provide it.

                But when using `Item` for output, for a response body, `tags` is always
                available because it has a default value, even if it's just an empty
                list. So, the client should be able to always expect it.

                In this case, there would be two different schemas, one for input and
                another one for output.

                Read more about it in the
                [FastAPI docs about how to separate schemas for input and output](https://fastapi.tiangolo.com/how-to/separate-openapi-schemas)
                """
            ),
        ] = True,
        openapi_external_docs: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                This field allows you to provide additional external documentation links.
                If provided, it must be a dictionary containing:

                * `description`: A brief description of the external documentation.
                * `url`: The URL pointing to the external documentation. The value **MUST**
                be a valid URL format.

                **Example**:

                ```python
                from fastapi import FastAPI

                external_docs = {
                    "description": "Detailed API Reference",
                    "url": "https://example.com/api-docs",
                }

                app = FastAPI(openapi_external_docs=external_docs)
                ```
                """
            ),
        ] = None,
        strict_content_type: Annotated[
            bool,
            Doc(
                """
                Enable strict checking for request Content-Type headers.

                When `True` (the default), requests with a body that do not include
                a `Content-Type` header will **not** be parsed as JSON.

                This prevents potential cross-site request forgery (CSRF) attacks
                that exploit the browser's ability to send requests without a
                Content-Type header, bypassing CORS preflight checks. In particular
                applicable for apps that need to be run locally (in localhost).

                When `False`, requests without a `Content-Type` header will have
                their body parsed as JSON, which maintains compatibility with
                certain clients that don't send `Content-Type` headers.

                Read more about it in the
                [FastAPI docs for Strict Content-Type](https://fastapi.tiangolo.com/advanced/strict-content-type/).
                """
            ),
        ] = True,
    ) -> None:
        self.debug = debug
        self.title = title
        self.summary = summary
        self.description = description
        self.version = version
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license_info = license_info
        self.openapi_url = openapi_url
        self.openapi_tags = openapi_tags
        self.root_path_in_servers = root_path_in_servers
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.swagger_ui_oauth2_redirect_url = swagger_ui_oauth2_redirect_url
        self.swagger_ui_init_oauth = swagger_ui_init_oauth
        self.swagger_ui_parameters = swagger_ui_parameters
        self.servers = servers or []
        self.separate_input_output_schemas = separate_input_output_schemas
        self.openapi_external_docs = openapi_external_docs
        self.openapi_version: Annotated[
            str,
            Doc(
                """
                The version string of OpenAPI.

                FastAPI will generate OpenAPI version 3.1.0, and will output that as
                the OpenAPI version. But some tools, even though they might be
                compatible with OpenAPI 3.1.0, might not recognize it as a valid.

                So you could override this value to trick those tools into using
                the generated OpenAPI. Have in mind that this is a hack. But if you
                avoid using features added in OpenAPI 3.1.0, it might work for your
                use case.

                This is not passed as a parameter to the `FastAPI` class to avoid
                giving the false idea that FastAPI would generate a different OpenAPI
                schema. It is only available as an attribute.

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI()

                app.openapi_version = "3.0.2"
                ```
                """
            ),
        ] = "3.1.0"
        self.openapi_schema: dict[str, Any] | None = None
        self._openapi_routes_version: int | None = None
        if self.openapi_url:
            assert self.title, "A title must be provided for OpenAPI, e.g.: 'My API'"
            assert self.version, "A version must be provided for OpenAPI, e.g.: '2.1.0'"
        self.webhooks: Annotated[
            routing.APIRouter,
            Doc(
                """
                The `app.webhooks` attribute is an `APIRouter` with the *path
                operations* that will be used just for documentation of webhooks.

                Read more about it in the
                [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/).
                """
            ),
        ] = webhooks or routing.APIRouter()
        if root_path:
            warnings.warn(
                "The `root_path` parameter is deprecated. Configure the "
                "server's root path instead, for example with "
                "`fastapi run --root-path /api/v1`.",
                category=FastAPIDeprecationWarning,
                stacklevel=2,
            )
        self.root_path = root_path
        self.state: Annotated[
            State,
            Doc(
                """
                A state object for the application. This is the same object for the
                entire application, it doesn't change from request to request.

                You normally wouldn't use this in FastAPI, for most of the cases you
                would instead use FastAPI dependencies.

                This is simply inherited from Starlette.

                Read more about it in the
                [Starlette docs for Applications](https://starlette.dev/applications/#storing-state-on-the-app-instance).
                """
            ),
        ] = State()
        self.dependency_overrides: Annotated[
            dict[Callable[..., Any], Callable[..., Any]],
            Doc(
                """
                A dictionary with overrides for the dependencies.

                Each key is the original dependency callable, and the value is the
                actual dependency that should be called.

                This is for testing, to replace expensive dependencies with testing
                versions.

                Read more about it in the
                [FastAPI docs for Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/).
                """
            ),
        ] = {}
        self.router: routing.APIRouter = routing.APIRouter(
            routes=routes,
            redirect_slashes=redirect_slashes,
            dependency_overrides_provider=self,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            default_response_class=default_response_class,
            dependencies=dependencies,
            callbacks=callbacks,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            responses=responses,
            generate_unique_id_function=generate_unique_id_function,
            strict_content_type=strict_content_type,
        )
        self.exception_handlers: dict[
            Any, Callable[[Request, Any], Response | Awaitable[Response]]
        ] = {} if exception_handlers is None else dict(exception_handlers)
        self.exception_handlers.setdefault(HTTPException, http_exception_handler)
        self.exception_handlers.setdefault(
            RequestValidationError, request_validation_exception_handler
        )

        # Starlette still has incorrect type specification for the handlers
        self.exception_handlers.setdefault(
            WebSocketRequestValidationError,
            websocket_request_validation_exception_handler,  # type: ignore[arg-type]
        )  # ty: ignore[no-matching-overload]

        self._telemetry: TelemetryConfig = {
            "tracer_provider": None,
            "meter_provider": None,
            "logger_provider": None,
            "tracing": True,
            "metrics": True,
            "logs": True,
            "operation_spans": True,
            "auto_configure": os.getenv("FASTAPI_OTEL_AUTO_CONFIGURE", "").lower()
            == "true",
            "exclude": None,
            **(telemetry if telemetry is not None else {}),
        }
        self._native_telemetry = NativeTelemetry(self._telemetry)

        self.user_middleware: list[Middleware] = (
            [] if middleware is None else list(middleware)
        )
        self.middleware_stack: ASGIApp | None = None
        self.setup()
```


---

### 🔹 Commit #06: `a37a162d`
- **完整 Hash**: `a37a162de602049ab65595a98d88a75996ee6814`
- **說明 (Ground Truth)**: 🔥 Remove deprecated `openapi_prefix` and unused `**extra` from `FastAPI` (#16518)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/applications.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:65, E:79, A:0) ➔ After(N:64, E:78, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 0, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `warning (External/Unresolved)` (FUNCTION_DEF)
  • - [移除呼叫邊] `FastAPI.__init__` ──[CALLS]──> `warning (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FastAPI.__init__()`
- **變更前簽章 (Before)**: `def __init__( self: AppType, *, telemetry: Annotated[ TelemetryConfig | None, Doc( """ Native OpenTelemetry configuration as a dictionary. Uses global providers by default. Omitted options keep their defaults. ```python app = FastAPI(telemetry={"tracing": False}) ``` """ ), ] = None, debug: Annotated[ bool, Doc( """ Boolean indicating if debug tracebacks should be returned on server errors. Read more in the [Starlette docs for Applications](https://starlette.dev/applications/#starlette.applications.Starlette). """ ), ] = False, routes: Annotated[ list[BaseRoute] | None, Doc( """ **Note**: you probably shouldn't use this parameter, it is inherited from Starlette and supported for compatibility. --- A list of routes to serve incoming HTTP and WebSocket requests. """ ), deprecated( """ You normally wouldn't use this parameter with FastAPI, it is inherited from Starlette and supported for compatibility. In FastAPI, you normally would use the *path operation methods*, like `app.get()`, `app.post()`, etc. """ ), ] = None, title: Annotated[ str, Doc( """ The title of the API. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI(title="ChimichangApp") ``` """ ), ] = "FastAPI", summary: Annotated[ str | None, Doc( """ A short summary of the API. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI(summary="Deadpond's favorite app. Nuff said.") ``` """ ), ] = None, description: Annotated[ str, Doc( ''' A description of the API. Supports Markdown (using [CommonMark syntax](https://commonmark.org/)). It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI( description=""" ChimichangApp API helps you do awesome stuff. 🚀 ## Items You can **read items**. ## Users You will be able to: * **Create users** (_not implemented_). * **Read users** (_not implemented_). """ ) ``` ''' ), ] = "", version: Annotated[ str, Doc( """ The version of the API. **Note** This is the version of your application, not the version of the OpenAPI specification nor the version of FastAPI being used. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI(version="0.0.1") ``` """ ), ] = "0.1.0", openapi_url: Annotated[ str | None, Doc( """ The URL where the OpenAPI schema will be served from. If you set it to `None`, no OpenAPI schema will be served publicly, and the default automatic endpoints `/docs` and `/redoc` will also be disabled. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url). **Example** ```python from fastapi import FastAPI app = FastAPI(openapi_url="/api/v1/openapi.json") ``` """ ), ] = "/openapi.json", openapi_tags: Annotated[ list[dict[str, Any]] | None, Doc( """ A list of tags used by OpenAPI, these are the same `tags` you can set in the *path operations*, like: * `@app.get("/users/", tags=["users"])` * `@app.get("/items/", tags=["items"])` The order of the tags can be used to specify the order shown in tools like Swagger UI, used in the automatic path `/docs`. It's not required to specify all the tags used. The tags that are not declared MAY be organized randomly or based on the tools' logic. Each tag name in the list MUST be unique. The value of each item is a `dict` containing: * `name`: The name of the tag. * `description`: A short description of the tag. [CommonMark syntax](https://commonmark.org/) MAY be used for rich text representation. * `externalDocs`: Additional external documentation for this tag. If provided, it would contain a `dict` with: * `description`: A short description of the target documentation. [CommonMark syntax](https://commonmark.org/) MAY be used for rich text representation. * `url`: The URL for the target documentation. Value MUST be in the form of a URL. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags). **Example** ```python from fastapi import FastAPI tags_metadata = [ { "name": "users", "description": "Operations with users. The **login** logic is also here.", }, { "name": "items", "description": "Manage items. So _fancy_ they have their own docs.", "externalDocs": { "description": "Items external docs", "url": "https://fastapi.tiangolo.com/", }, }, ] app = FastAPI(openapi_tags=tags_metadata) ``` """ ), ] = None, servers: Annotated[ list[dict[str, str | Any]] | None, Doc( """ A `list` of `dict`s with connectivity information to a target server. You would use it, for example, if your application is served from different domains and you want to use the same Swagger UI in the browser to interact with each of them (instead of having multiple browser tabs open). Or if you want to leave fixed the possible URLs. If the servers `list` is not provided, or is an empty `list`, the `servers` property in the generated OpenAPI will be: * a `dict` with a `url` value of the application's mounting point (`root_path`) if it's different from `/`. * otherwise, the `servers` property will be omitted from the OpenAPI schema. Each item in the `list` is a `dict` containing: * `url`: A URL to the target host. This URL supports Server Variables and MAY be relative, to indicate that the host location is relative to the location where the OpenAPI document is being served. Variable substitutions will be made when a variable is named in `{`brackets`}`. * `description`: An optional string describing the host designated by the URL. [CommonMark syntax](https://commonmark.org/) MAY be used for rich text representation. * `variables`: A `dict` between a variable name and its value. The value is used for substitution in the server's URL template. Read more in the [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#additional-servers). **Example** ```python from fastapi import FastAPI app = FastAPI( servers=[ {"url": "https://stag.example.com", "description": "Staging environment"}, {"url": "https://prod.example.com", "description": "Production environment"}, ] ) ``` """ ), ] = None, dependencies: Annotated[ Sequence[Depends] | None, Doc( """ A list of global dependencies, they will be applied to each *path operation*, including in sub-routers. Read more about it in the [FastAPI docs for Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/). **Example** ```python from fastapi import Depends, FastAPI from .dependencies import func_dep_1, func_dep_2 app = FastAPI(dependencies=[Depends(func_dep_1), Depends(func_dep_2)]) ``` """ ), ] = None, default_response_class: Annotated[ type[Response], Doc( """ The default response class to be used. Read more in the [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class). **Example** ```python from fastapi import FastAPI from fastapi.responses import ORJSONResponse app = FastAPI(default_response_class=ORJSONResponse) ``` """ ), ] = Default(JSONResponse), redirect_slashes: Annotated[ bool, Doc( """ Whether to detect and redirect slashes in URLs when the client doesn't use the same format. **Example** ```python from fastapi import FastAPI app = FastAPI(redirect_slashes=True) # the default @app.get("/items/") async def read_items(): return [{"item_id": "Foo"}] ``` With this app, if a client goes to `/items` (without a trailing slash), they will be automatically redirected with an HTTP status code of 307 to `/items/`. """ ), ] = True, docs_url: Annotated[ str | None, Doc( """ The path to the automatic interactive API documentation. It is handled in the browser by Swagger UI. The default URL is `/docs`. You can disable it by setting it to `None`. If `openapi_url` is set to `None`, this will be automatically disabled. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls). **Example** ```python from fastapi import FastAPI app = FastAPI(docs_url="/documentation", redoc_url=None) ``` """ ), ] = "/docs", redoc_url: Annotated[ str | None, Doc( """ The path to the alternative automatic interactive API documentation provided by ReDoc. The default URL is `/redoc`. You can disable it by setting it to `None`. If `openapi_url` is set to `None`, this will be automatically disabled. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls). **Example** ```python from fastapi import FastAPI app = FastAPI(docs_url="/documentation", redoc_url="redocumentation") ``` """ ), ] = "/redoc", swagger_ui_oauth2_redirect_url: Annotated[ str | None, Doc( """ The OAuth2 redirect endpoint for the Swagger UI. By default it is `/docs/oauth2-redirect`. This is only used if you use OAuth2 (with the "Authorize" button) with Swagger UI. """ ), ] = "/docs/oauth2-redirect", swagger_ui_init_oauth: Annotated[ dict[str, Any] | None, Doc( """ OAuth2 configuration for the Swagger UI, by default shown at `/docs`. Read more about the available configuration options in the [Swagger UI docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/). """ ), ] = None, middleware: Annotated[ Sequence[Middleware] | None, Doc( """ List of middleware to be added when creating the application. In FastAPI you would normally do this with `app.add_middleware()` instead. Read more in the [FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/). """ ), ] = None, exception_handlers: Annotated[ dict[ int | type[Exception], Callable[[Request, Any], Coroutine[Any, Any, Response]], ] | None, Doc( """ A dictionary with handlers for exceptions. In FastAPI, you would normally use the decorator `@app.exception_handler()`. Read more in the [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/). """ ), ] = None, on_startup: Annotated[ Sequence[Callable[[], Any]] | None, Doc( """ A list of startup event handler functions. You should instead use the `lifespan` handlers. Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/). """ ), ] = None, on_shutdown: Annotated[ Sequence[Callable[[], Any]] | None, Doc( """ A list of shutdown event handler functions. You should instead use the `lifespan` handlers. Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/). """ ), ] = None, lifespan: Annotated[ Lifespan[AppType] | None, Doc( """ A `Lifespan` context manager handler. This replaces `startup` and `shutdown` functions with a single context manager. Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/). """ ), ] = None, terms_of_service: Annotated[ str | None, Doc( """ A URL to the Terms of Service for your API. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more at the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python app = FastAPI(terms_of_service="http://example.com/terms/") ``` """ ), ] = None, contact: Annotated[ dict[str, str | Any] | None, Doc( """ A dictionary with the contact information for the exposed API. It can contain several fields. * `name`: (`str`) The name of the contact person/organization. * `url`: (`str`) A URL pointing to the contact information. MUST be in the format of a URL. * `email`: (`str`) The email address of the contact person/organization. MUST be in the format of an email address. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more at the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python app = FastAPI( contact={ "name": "Deadpoolio the Amazing", "url": "http://x-force.example.com/contact/", "email": "dp@x-force.example.com", } ) ``` """ ), ] = None, license_info: Annotated[ dict[str, str | Any] | None, Doc( """ A dictionary with the license information for the exposed API. It can contain several fields. * `name`: (`str`) **REQUIRED** (if a `license_info` is set). The license name used for the API. * `identifier`: (`str`) An [SPDX](https://spdx.dev/) license expression for the API. The `identifier` field is mutually exclusive of the `url` field. Available since OpenAPI 3.1.0, FastAPI 0.99.0. * `url`: (`str`) A URL to the license used for the API. This MUST be the format of a URL. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more at the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python app = FastAPI( license_info={ "name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html", } ) ``` """ ), ] = None, openapi_prefix: Annotated[ str, Doc( """ A URL prefix for the OpenAPI URL. """ ), deprecated( """ "openapi_prefix" has been deprecated in favor of "root_path", which follows more closely the ASGI standard, is simpler, and more automatic. """ ), ] = "", root_path: Annotated[ str, Doc( """ A path prefix handled by a proxy that is not seen by the application but is seen by external clients, which affects things like Swagger UI. Read more about it at the [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/). **Example** ```python from fastapi import FastAPI app = FastAPI(root_path="/api/v1") ``` """ ), ] = "", root_path_in_servers: Annotated[ bool, Doc( """ To disable automatically generating the URLs in the `servers` field in the autogenerated OpenAPI using the `root_path`. Read more about it in the [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#disable-automatic-server-from-root-path). **Example** ```python from fastapi import FastAPI app = FastAPI(root_path_in_servers=False) ``` """ ), ] = True, responses: Annotated[ dict[int | str, dict[str, Any]] | None, Doc( """ Additional responses to be shown in OpenAPI. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/). And in the [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies). """ ), ] = None, callbacks: Annotated[ list[BaseRoute] | None, Doc( """ OpenAPI callbacks that should apply to all *path operations*. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/). """ ), ] = None, webhooks: Annotated[ routing.APIRouter | None, Doc( """ Add OpenAPI webhooks. This is similar to `callbacks` but it doesn't depend on specific *path operations*. It will be added to the generated OpenAPI (e.g. visible at `/docs`). **Note**: This is available since OpenAPI 3.1.0, FastAPI 0.99.0. Read more about it in the [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/). """ ), ] = None, deprecated: Annotated[ bool | None, Doc( """ Mark all *path operations* as deprecated. You probably don't need it, but it's available. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#deprecate-a-path-operation). """ ), ] = None, include_in_schema: Annotated[ bool, Doc( """ To include (or not) all the *path operations* in the generated OpenAPI. You probably don't need it, but it's available. This affects the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi). """ ), ] = True, swagger_ui_parameters: Annotated[ dict[str, Any] | None, Doc( """ Parameters to configure Swagger UI, the autogenerated interactive API documentation (by default at `/docs`). Read more about it in the [FastAPI docs about how to Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/). """ ), ] = None, generate_unique_id_function: Annotated[ Callable[[routing.APIRoute], str], Doc( """ Customize the function used to generate unique IDs for the *path operations* shown in the generated OpenAPI. This is particularly useful when automatically generating clients or SDKs for your API. Read more about it in the [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function). """ ), ] = Default(generate_unique_id), separate_input_output_schemas: Annotated[ bool, Doc( """ Whether to generate separate OpenAPI schemas for request body and response body when the results would be more precise. This is particularly useful when automatically generating clients. For example, if you have a model like: ```python from pydantic import BaseModel class Item(BaseModel): name: str tags: list[str] = [] ``` When `Item` is used for input, a request body, `tags` is not required, the client doesn't have to provide it. But when using `Item` for output, for a response body, `tags` is always available because it has a default value, even if it's just an empty list. So, the client should be able to always expect it. In this case, there would be two different schemas, one for input and another one for output. Read more about it in the [FastAPI docs about how to separate schemas for input and output](https://fastapi.tiangolo.com/how-to/separate-openapi-schemas) """ ), ] = True, openapi_external_docs: Annotated[ dict[str, Any] | None, Doc( """ This field allows you to provide additional external documentation links. If provided, it must be a dictionary containing: * `description`: A brief description of the external documentation. * `url`: The URL pointing to the external documentation. The value **MUST** be a valid URL format. **Example**: ```python from fastapi import FastAPI external_docs = { "description": "Detailed API Reference", "url": "https://example.com/api-docs", } app = FastAPI(openapi_external_docs=external_docs) ``` """ ), ] = None, strict_content_type: Annotated[ bool, Doc( """ Enable strict checking for request Content-Type headers. When `True` (the default), requests with a body that do not include a `Content-Type` header will **not** be parsed as JSON. This prevents potential cross-site request forgery (CSRF) attacks that exploit the browser's ability to send requests without a Content-Type header, bypassing CORS preflight checks. In particular applicable for apps that need to be run locally (in localhost). When `False`, requests without a `Content-Type` header will have their body parsed as JSON, which maintains compatibility with certain clients that don't send `Content-Type` headers. Read more about it in the [FastAPI docs for Strict Content-Type](https://fastapi.tiangolo.com/advanced/strict-content-type/). """ ), ] = True, **extra: Annotated[ Any, Doc( """ Extra keyword arguments to be stored in the app, not used by FastAPI anywhere. """ ), ], ) -> None` (L64~L1052)
- **變更後簽章 (After)**: `def __init__( self: AppType, *, telemetry: Annotated[ TelemetryConfig | None, Doc( """ Native OpenTelemetry configuration as a dictionary. Uses global providers by default. Omitted options keep their defaults. ```python app = FastAPI(telemetry={"tracing": False}) ``` """ ), ] = None, debug: Annotated[ bool, Doc( """ Boolean indicating if debug tracebacks should be returned on server errors. Read more in the [Starlette docs for Applications](https://starlette.dev/applications/#starlette.applications.Starlette). """ ), ] = False, routes: Annotated[ list[BaseRoute] | None, Doc( """ **Note**: you probably shouldn't use this parameter, it is inherited from Starlette and supported for compatibility. --- A list of routes to serve incoming HTTP and WebSocket requests. """ ), deprecated( """ You normally wouldn't use this parameter with FastAPI, it is inherited from Starlette and supported for compatibility. In FastAPI, you normally would use the *path operation methods*, like `app.get()`, `app.post()`, etc. """ ), ] = None, title: Annotated[ str, Doc( """ The title of the API. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI(title="ChimichangApp") ``` """ ), ] = "FastAPI", summary: Annotated[ str | None, Doc( """ A short summary of the API. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI(summary="Deadpond's favorite app. Nuff said.") ``` """ ), ] = None, description: Annotated[ str, Doc( ''' A description of the API. Supports Markdown (using [CommonMark syntax](https://commonmark.org/)). It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI( description=""" ChimichangApp API helps you do awesome stuff. 🚀 ## Items You can **read items**. ## Users You will be able to: * **Create users** (_not implemented_). * **Read users** (_not implemented_). """ ) ``` ''' ), ] = "", version: Annotated[ str, Doc( """ The version of the API. **Note** This is the version of your application, not the version of the OpenAPI specification nor the version of FastAPI being used. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python from fastapi import FastAPI app = FastAPI(version="0.0.1") ``` """ ), ] = "0.1.0", openapi_url: Annotated[ str | None, Doc( """ The URL where the OpenAPI schema will be served from. If you set it to `None`, no OpenAPI schema will be served publicly, and the default automatic endpoints `/docs` and `/redoc` will also be disabled. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url). **Example** ```python from fastapi import FastAPI app = FastAPI(openapi_url="/api/v1/openapi.json") ``` """ ), ] = "/openapi.json", openapi_tags: Annotated[ list[dict[str, Any]] | None, Doc( """ A list of tags used by OpenAPI, these are the same `tags` you can set in the *path operations*, like: * `@app.get("/users/", tags=["users"])` * `@app.get("/items/", tags=["items"])` The order of the tags can be used to specify the order shown in tools like Swagger UI, used in the automatic path `/docs`. It's not required to specify all the tags used. The tags that are not declared MAY be organized randomly or based on the tools' logic. Each tag name in the list MUST be unique. The value of each item is a `dict` containing: * `name`: The name of the tag. * `description`: A short description of the tag. [CommonMark syntax](https://commonmark.org/) MAY be used for rich text representation. * `externalDocs`: Additional external documentation for this tag. If provided, it would contain a `dict` with: * `description`: A short description of the target documentation. [CommonMark syntax](https://commonmark.org/) MAY be used for rich text representation. * `url`: The URL for the target documentation. Value MUST be in the form of a URL. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags). **Example** ```python from fastapi import FastAPI tags_metadata = [ { "name": "users", "description": "Operations with users. The **login** logic is also here.", }, { "name": "items", "description": "Manage items. So _fancy_ they have their own docs.", "externalDocs": { "description": "Items external docs", "url": "https://fastapi.tiangolo.com/", }, }, ] app = FastAPI(openapi_tags=tags_metadata) ``` """ ), ] = None, servers: Annotated[ list[dict[str, str | Any]] | None, Doc( """ A `list` of `dict`s with connectivity information to a target server. You would use it, for example, if your application is served from different domains and you want to use the same Swagger UI in the browser to interact with each of them (instead of having multiple browser tabs open). Or if you want to leave fixed the possible URLs. If the servers `list` is not provided, or is an empty `list`, the `servers` property in the generated OpenAPI will be: * a `dict` with a `url` value of the application's mounting point (`root_path`) if it's different from `/`. * otherwise, the `servers` property will be omitted from the OpenAPI schema. Each item in the `list` is a `dict` containing: * `url`: A URL to the target host. This URL supports Server Variables and MAY be relative, to indicate that the host location is relative to the location where the OpenAPI document is being served. Variable substitutions will be made when a variable is named in `{`brackets`}`. * `description`: An optional string describing the host designated by the URL. [CommonMark syntax](https://commonmark.org/) MAY be used for rich text representation. * `variables`: A `dict` between a variable name and its value. The value is used for substitution in the server's URL template. Read more in the [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#additional-servers). **Example** ```python from fastapi import FastAPI app = FastAPI( servers=[ {"url": "https://stag.example.com", "description": "Staging environment"}, {"url": "https://prod.example.com", "description": "Production environment"}, ] ) ``` """ ), ] = None, dependencies: Annotated[ Sequence[Depends] | None, Doc( """ A list of global dependencies, they will be applied to each *path operation*, including in sub-routers. Read more about it in the [FastAPI docs for Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/). **Example** ```python from fastapi import Depends, FastAPI from .dependencies import func_dep_1, func_dep_2 app = FastAPI(dependencies=[Depends(func_dep_1), Depends(func_dep_2)]) ``` """ ), ] = None, default_response_class: Annotated[ type[Response], Doc( """ The default response class to be used. Read more in the [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class). **Example** ```python from fastapi import FastAPI from fastapi.responses import ORJSONResponse app = FastAPI(default_response_class=ORJSONResponse) ``` """ ), ] = Default(JSONResponse), redirect_slashes: Annotated[ bool, Doc( """ Whether to detect and redirect slashes in URLs when the client doesn't use the same format. **Example** ```python from fastapi import FastAPI app = FastAPI(redirect_slashes=True) # the default @app.get("/items/") async def read_items(): return [{"item_id": "Foo"}] ``` With this app, if a client goes to `/items` (without a trailing slash), they will be automatically redirected with an HTTP status code of 307 to `/items/`. """ ), ] = True, docs_url: Annotated[ str | None, Doc( """ The path to the automatic interactive API documentation. It is handled in the browser by Swagger UI. The default URL is `/docs`. You can disable it by setting it to `None`. If `openapi_url` is set to `None`, this will be automatically disabled. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls). **Example** ```python from fastapi import FastAPI app = FastAPI(docs_url="/documentation", redoc_url=None) ``` """ ), ] = "/docs", redoc_url: Annotated[ str | None, Doc( """ The path to the alternative automatic interactive API documentation provided by ReDoc. The default URL is `/redoc`. You can disable it by setting it to `None`. If `openapi_url` is set to `None`, this will be automatically disabled. Read more in the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls). **Example** ```python from fastapi import FastAPI app = FastAPI(docs_url="/documentation", redoc_url="redocumentation") ``` """ ), ] = "/redoc", swagger_ui_oauth2_redirect_url: Annotated[ str | None, Doc( """ The OAuth2 redirect endpoint for the Swagger UI. By default it is `/docs/oauth2-redirect`. This is only used if you use OAuth2 (with the "Authorize" button) with Swagger UI. """ ), ] = "/docs/oauth2-redirect", swagger_ui_init_oauth: Annotated[ dict[str, Any] | None, Doc( """ OAuth2 configuration for the Swagger UI, by default shown at `/docs`. Read more about the available configuration options in the [Swagger UI docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/). """ ), ] = None, middleware: Annotated[ Sequence[Middleware] | None, Doc( """ List of middleware to be added when creating the application. In FastAPI you would normally do this with `app.add_middleware()` instead. Read more in the [FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/). """ ), ] = None, exception_handlers: Annotated[ dict[ int | type[Exception], Callable[[Request, Any], Coroutine[Any, Any, Response]], ] | None, Doc( """ A dictionary with handlers for exceptions. In FastAPI, you would normally use the decorator `@app.exception_handler()`. Read more in the [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/). """ ), ] = None, on_startup: Annotated[ Sequence[Callable[[], Any]] | None, Doc( """ A list of startup event handler functions. You should instead use the `lifespan` handlers. Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/). """ ), ] = None, on_shutdown: Annotated[ Sequence[Callable[[], Any]] | None, Doc( """ A list of shutdown event handler functions. You should instead use the `lifespan` handlers. Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/). """ ), ] = None, lifespan: Annotated[ Lifespan[AppType] | None, Doc( """ A `Lifespan` context manager handler. This replaces `startup` and `shutdown` functions with a single context manager. Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/). """ ), ] = None, terms_of_service: Annotated[ str | None, Doc( """ A URL to the Terms of Service for your API. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more at the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python app = FastAPI(terms_of_service="http://example.com/terms/") ``` """ ), ] = None, contact: Annotated[ dict[str, str | Any] | None, Doc( """ A dictionary with the contact information for the exposed API. It can contain several fields. * `name`: (`str`) The name of the contact person/organization. * `url`: (`str`) A URL pointing to the contact information. MUST be in the format of a URL. * `email`: (`str`) The email address of the contact person/organization. MUST be in the format of an email address. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more at the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python app = FastAPI( contact={ "name": "Deadpoolio the Amazing", "url": "http://x-force.example.com/contact/", "email": "dp@x-force.example.com", } ) ``` """ ), ] = None, license_info: Annotated[ dict[str, str | Any] | None, Doc( """ A dictionary with the license information for the exposed API. It can contain several fields. * `name`: (`str`) **REQUIRED** (if a `license_info` is set). The license name used for the API. * `identifier`: (`str`) An [SPDX](https://spdx.dev/) license expression for the API. The `identifier` field is mutually exclusive of the `url` field. Available since OpenAPI 3.1.0, FastAPI 0.99.0. * `url`: (`str`) A URL to the license used for the API. This MUST be the format of a URL. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more at the [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api). **Example** ```python app = FastAPI( license_info={ "name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html", } ) ``` """ ), ] = None, root_path: Annotated[ str, Doc( """ A path prefix handled by a proxy that is not seen by the application but is seen by external clients, which affects things like Swagger UI. Read more about it at the [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/). **Example** ```python from fastapi import FastAPI app = FastAPI(root_path="/api/v1") ``` """ ), ] = "", root_path_in_servers: Annotated[ bool, Doc( """ To disable automatically generating the URLs in the `servers` field in the autogenerated OpenAPI using the `root_path`. Read more about it in the [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#disable-automatic-server-from-root-path). **Example** ```python from fastapi import FastAPI app = FastAPI(root_path_in_servers=False) ``` """ ), ] = True, responses: Annotated[ dict[int | str, dict[str, Any]] | None, Doc( """ Additional responses to be shown in OpenAPI. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/). And in the [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies). """ ), ] = None, callbacks: Annotated[ list[BaseRoute] | None, Doc( """ OpenAPI callbacks that should apply to all *path operations*. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/). """ ), ] = None, webhooks: Annotated[ routing.APIRouter | None, Doc( """ Add OpenAPI webhooks. This is similar to `callbacks` but it doesn't depend on specific *path operations*. It will be added to the generated OpenAPI (e.g. visible at `/docs`). **Note**: This is available since OpenAPI 3.1.0, FastAPI 0.99.0. Read more about it in the [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/). """ ), ] = None, deprecated: Annotated[ bool | None, Doc( """ Mark all *path operations* as deprecated. You probably don't need it, but it's available. It will be added to the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#deprecate-a-path-operation). """ ), ] = None, include_in_schema: Annotated[ bool, Doc( """ To include (or not) all the *path operations* in the generated OpenAPI. You probably don't need it, but it's available. This affects the generated OpenAPI (e.g. visible at `/docs`). Read more about it in the [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi). """ ), ] = True, swagger_ui_parameters: Annotated[ dict[str, Any] | None, Doc( """ Parameters to configure Swagger UI, the autogenerated interactive API documentation (by default at `/docs`). Read more about it in the [FastAPI docs about how to Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/). """ ), ] = None, generate_unique_id_function: Annotated[ Callable[[routing.APIRoute], str], Doc( """ Customize the function used to generate unique IDs for the *path operations* shown in the generated OpenAPI. This is particularly useful when automatically generating clients or SDKs for your API. Read more about it in the [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function). """ ), ] = Default(generate_unique_id), separate_input_output_schemas: Annotated[ bool, Doc( """ Whether to generate separate OpenAPI schemas for request body and response body when the results would be more precise. This is particularly useful when automatically generating clients. For example, if you have a model like: ```python from pydantic import BaseModel class Item(BaseModel): name: str tags: list[str] = [] ``` When `Item` is used for input, a request body, `tags` is not required, the client doesn't have to provide it. But when using `Item` for output, for a response body, `tags` is always available because it has a default value, even if it's just an empty list. So, the client should be able to always expect it. In this case, there would be two different schemas, one for input and another one for output. Read more about it in the [FastAPI docs about how to separate schemas for input and output](https://fastapi.tiangolo.com/how-to/separate-openapi-schemas) """ ), ] = True, openapi_external_docs: Annotated[ dict[str, Any] | None, Doc( """ This field allows you to provide additional external documentation links. If provided, it must be a dictionary containing: * `description`: A brief description of the external documentation. * `url`: The URL pointing to the external documentation. The value **MUST** be a valid URL format. **Example**: ```python from fastapi import FastAPI external_docs = { "description": "Detailed API Reference", "url": "https://example.com/api-docs", } app = FastAPI(openapi_external_docs=external_docs) ``` """ ), ] = None, strict_content_type: Annotated[ bool, Doc( """ Enable strict checking for request Content-Type headers. When `True` (the default), requests with a body that do not include a `Content-Type` header will **not** be parsed as JSON. This prevents potential cross-site request forgery (CSRF) attacks that exploit the browser's ability to send requests without a Content-Type header, bypassing CORS preflight checks. In particular applicable for apps that need to be run locally (in localhost). When `False`, requests without a `Content-Type` header will have their body parsed as JSON, which maintains compatibility with certain clients that don't send `Content-Type` headers. Read more about it in the [FastAPI docs for Strict Content-Type](https://fastapi.tiangolo.com/advanced/strict-content-type/). """ ), ] = True, ) -> None` (L63~L1018)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self: AppType,
        *,
        telemetry: Annotated[
            TelemetryConfig | None,
            Doc(
                """
                Native OpenTelemetry configuration as a dictionary. Uses global
                providers by default. Omitted options keep their defaults.

                ```python
                app = FastAPI(telemetry={"tracing": False})
                ```
                """
            ),
        ] = None,
        debug: Annotated[
            bool,
            Doc(
                """
                Boolean indicating if debug tracebacks should be returned on server
                errors.

                Read more in the
                [Starlette docs for Applications](https://starlette.dev/applications/#starlette.applications.Starlette).
                """
            ),
        ] = False,
        routes: Annotated[
            list[BaseRoute] | None,
            Doc(
                """
                **Note**: you probably shouldn't use this parameter, it is inherited
                from Starlette and supported for compatibility.

                ---

                A list of routes to serve incoming HTTP and WebSocket requests.
                """
            ),
            deprecated(
                """
                You normally wouldn't use this parameter with FastAPI, it is inherited
                from Starlette and supported for compatibility.

                In FastAPI, you normally would use the *path operation methods*,
                like `app.get()`, `app.post()`, etc.
                """
            ),
        ] = None,
        title: Annotated[
            str,
            Doc(
                """
                The title of the API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(title="ChimichangApp")
                ```
                """
            ),
        ] = "FastAPI",
        summary: Annotated[
            str | None,
            Doc(
                """
                A short summary of the API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(summary="Deadpond's favorite app. Nuff said.")
                ```
                """
            ),
        ] = None,
        description: Annotated[
            str,
            Doc(
                '''
                A description of the API. Supports Markdown (using
                [CommonMark syntax](https://commonmark.org/)).

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(
                    description="""
                                ChimichangApp API helps you do awesome stuff. 🚀

                                ## Items

                                You can **read items**.

                                ## Users

                                You will be able to:

                                * **Create users** (_not implemented_).
                                * **Read users** (_not implemented_).

                                """
                )
                ```
                '''
            ),
        ] = "",
        version: Annotated[
            str,
            Doc(
                """
                The version of the API.

                **Note** This is the version of your application, not the version of
                the OpenAPI specification nor the version of FastAPI being used.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(version="0.0.1")
                ```
                """
            ),
        ] = "0.1.0",
        openapi_url: Annotated[
            str | None,
            Doc(
                """
                The URL where the OpenAPI schema will be served from.

                If you set it to `None`, no OpenAPI schema will be served publicly, and
                the default automatic endpoints `/docs` and `/redoc` will also be
                disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(openapi_url="/api/v1/openapi.json")
                ```
                """
            ),
        ] = "/openapi.json",
        openapi_tags: Annotated[
            list[dict[str, Any]] | None,
            Doc(
                """
                A list of tags used by OpenAPI, these are the same `tags` you can set
                in the *path operations*, like:

                * `@app.get("/users/", tags=["users"])`
                * `@app.get("/items/", tags=["items"])`

                The order of the tags can be used to specify the order shown in
                tools like Swagger UI, used in the automatic path `/docs`.

                It's not required to specify all the tags used.

                The tags that are not declared MAY be organized randomly or based
                on the tools' logic. Each tag name in the list MUST be unique.

                The value of each item is a `dict` containing:

                * `name`: The name of the tag.
                * `description`: A short description of the tag.
                    [CommonMark syntax](https://commonmark.org/) MAY be used for rich
                    text representation.
                * `externalDocs`: Additional external documentation for this tag. If
                    provided, it would contain a `dict` with:
                    * `description`: A short description of the target documentation.
                        [CommonMark syntax](https://commonmark.org/) MAY be used for
                        rich text representation.
                    * `url`: The URL for the target documentation. Value MUST be in
                        the form of a URL.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags).

                **Example**

                ```python
                from fastapi import FastAPI

                tags_metadata = [
                    {
                        "name": "users",
                        "description": "Operations with users. The **login** logic is also here.",
                    },
                    {
                        "name": "items",
                        "description": "Manage items. So _fancy_ they have their own docs.",
                        "externalDocs": {
                            "description": "Items external docs",
                            "url": "https://fastapi.tiangolo.com/",
                        },
                    },
                ]

                app = FastAPI(openapi_tags=tags_metadata)
                ```
                """
            ),
        ] = None,
        servers: Annotated[
            list[dict[str, str | Any]] | None,
            Doc(
                """
                A `list` of `dict`s with connectivity information to a target server.

                You would use it, for example, if your application is served from
                different domains and you want to use the same Swagger UI in the
                browser to interact with each of them (instead of having multiple
                browser tabs open). Or if you want to leave fixed the possible URLs.

                If the servers `list` is not provided, or is an empty `list`, the
                `servers` property in the generated OpenAPI will be:

                * a `dict` with a `url` value of the application's mounting point
                (`root_path`) if it's different from `/`.
                * otherwise, the `servers` property will be omitted from the OpenAPI
                schema.

                Each item in the `list` is a `dict` containing:

                * `url`: A URL to the target host. This URL supports Server Variables
                and MAY be relative, to indicate that the host location is relative
                to the location where the OpenAPI document is being served. Variable
                substitutions will be made when a variable is named in `{`brackets`}`.
                * `description`: An optional string describing the host designated by
                the URL. [CommonMark syntax](https://commonmark.org/) MAY be used for
                rich text representation.
                * `variables`: A `dict` between a variable name and its value. The value
                    is used for substitution in the server's URL template.

                Read more in the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#additional-servers).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(
                    servers=[
                        {"url": "https://stag.example.com", "description": "Staging environment"},
                        {"url": "https://prod.example.com", "description": "Production environment"},
                    ]
                )
                ```
                """
            ),
        ] = None,
        dependencies: Annotated[
            Sequence[Depends] | None,
            Doc(
                """
                A list of global dependencies, they will be applied to each
                *path operation*, including in sub-routers.

                Read more about it in the
                [FastAPI docs for Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/).

                **Example**

                ```python
                from fastapi import Depends, FastAPI

                from .dependencies import func_dep_1, func_dep_2

                app = FastAPI(dependencies=[Depends(func_dep_1), Depends(func_dep_2)])
                ```
                """
            ),
        ] = None,
        default_response_class: Annotated[
            type[Response],
            Doc(
                """
                The default response class to be used.

                Read more in the
                [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).

                **Example**

                ```python
                from fastapi import FastAPI
                from fastapi.responses import ORJSONResponse

                app = FastAPI(default_response_class=ORJSONResponse)
                ```
                """
            ),
        ] = Default(JSONResponse),
        redirect_slashes: Annotated[
            bool,
            Doc(
                """
                Whether to detect and redirect slashes in URLs when the client doesn't
                use the same format.

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(redirect_slashes=True)  # the default

                @app.get("/items/")
                async def read_items():
                    return [{"item_id": "Foo"}]
                ```

                With this app, if a client goes to `/items` (without a trailing slash),
                they will be automatically redirected with an HTTP status code of 307
                to `/items/`.
                """
            ),
        ] = True,
        docs_url: Annotated[
            str | None,
            Doc(
                """
                The path to the automatic interactive API documentation.
                It is handled in the browser by Swagger UI.

                The default URL is `/docs`. You can disable it by setting it to `None`.

                If `openapi_url` is set to `None`, this will be automatically disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(docs_url="/documentation", redoc_url=None)
                ```
                """
            ),
        ] = "/docs",
        redoc_url: Annotated[
            str | None,
            Doc(
                """
                The path to the alternative automatic interactive API documentation
                provided by ReDoc.

                The default URL is `/redoc`. You can disable it by setting it to `None`.

                If `openapi_url` is set to `None`, this will be automatically disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(docs_url="/documentation", redoc_url="redocumentation")
                ```
                """
            ),
        ] = "/redoc",
        swagger_ui_oauth2_redirect_url: Annotated[
            str | None,
            Doc(
                """
                The OAuth2 redirect endpoint for the Swagger UI.

                By default it is `/docs/oauth2-redirect`.

                This is only used if you use OAuth2 (with the "Authorize" button)
                with Swagger UI.
                """
            ),
        ] = "/docs/oauth2-redirect",
        swagger_ui_init_oauth: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                OAuth2 configuration for the Swagger UI, by default shown at `/docs`.

                Read more about the available configuration options in the
                [Swagger UI docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/).
                """
            ),
        ] = None,
        middleware: Annotated[
            Sequence[Middleware] | None,
            Doc(
                """
                List of middleware to be added when creating the application.

                In FastAPI you would normally do this with `app.add_middleware()`
                instead.

                Read more in the
                [FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/).
                """
            ),
        ] = None,
        exception_handlers: Annotated[
            dict[
                int | type[Exception],
                Callable[[Request, Any], Coroutine[Any, Any, Response]],
            ]
            | None,
            Doc(
                """
                A dictionary with handlers for exceptions.

                In FastAPI, you would normally use the decorator
                `@app.exception_handler()`.

                Read more in the
                [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).
                """
            ),
        ] = None,
        on_startup: Annotated[
            Sequence[Callable[[], Any]] | None,
            Doc(
                """
                A list of startup event handler functions.

                You should instead use the `lifespan` handlers.

                Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        on_shutdown: Annotated[
            Sequence[Callable[[], Any]] | None,
            Doc(
                """
                A list of shutdown event handler functions.

                You should instead use the `lifespan` handlers.

                Read more in the
                [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        lifespan: Annotated[
            Lifespan[AppType] | None,
            Doc(
                """
                A `Lifespan` context manager handler. This replaces `startup` and
                `shutdown` functions with a single context manager.

                Read more in the
                [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        terms_of_service: Annotated[
            str | None,
            Doc(
                """
                A URL to the Terms of Service for your API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more at the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                app = FastAPI(terms_of_service="http://example.com/terms/")
                ```
                """
            ),
        ] = None,
        contact: Annotated[
            dict[str, str | Any] | None,
            Doc(
                """
                A dictionary with the contact information for the exposed API.

                It can contain several fields.

                * `name`: (`str`) The name of the contact person/organization.
                * `url`: (`str`) A URL pointing to the contact information. MUST be in
                    the format of a URL.
                * `email`: (`str`) The email address of the contact person/organization.
                    MUST be in the format of an email address.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more at the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                app = FastAPI(
                    contact={
                        "name": "Deadpoolio the Amazing",
                        "url": "http://x-force.example.com/contact/",
                        "email": "dp@x-force.example.com",
                    }
                )
                ```
                """
            ),
        ] = None,
        license_info: Annotated[
            dict[str, str | Any] | None,
            Doc(
                """
                A dictionary with the license information for the exposed API.

                It can contain several fields.

                * `name`: (`str`) **REQUIRED** (if a `license_info` is set). The
                    license name used for the API.
                * `identifier`: (`str`) An [SPDX](https://spdx.dev/) license expression
                    for the API. The `identifier` field is mutually exclusive of the `url`
                    field. Available since OpenAPI 3.1.0, FastAPI 0.99.0.
                * `url`: (`str`) A URL to the license used for the API. This MUST be
                    the format of a URL.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more at the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                app = FastAPI(
                    license_info={
                        "name": "Apache 2.0",
                        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                    }
                )
                ```
                """
            ),
        ] = None,
        openapi_prefix: Annotated[
            str,
            Doc(
                """
                A URL prefix for the OpenAPI URL.
                """
            ),
            deprecated(
                """
                "openapi_prefix" has been deprecated in favor of "root_path", which
                follows more closely the ASGI standard, is simpler, and more
                automatic.
                """
            ),
        ] = "",
        root_path: Annotated[
            str,
            Doc(
                """
                A path prefix handled by a proxy that is not seen by the application
                but is seen by external clients, which affects things like Swagger UI.

                Read more about it at the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(root_path="/api/v1")
                ```
                """
            ),
        ] = "",
        root_path_in_servers: Annotated[
            bool,
            Doc(
                """
                To disable automatically generating the URLs in the `servers` field
                in the autogenerated OpenAPI using the `root_path`.

                Read more about it in the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#disable-automatic-server-from-root-path).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(root_path_in_servers=False)
                ```
                """
            ),
        ] = True,
        responses: Annotated[
            dict[int | str, dict[str, Any]] | None,
            Doc(
                """
                Additional responses to be shown in OpenAPI.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).

                And in the
                [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
                """
            ),
        ] = None,
        callbacks: Annotated[
            list[BaseRoute] | None,
            Doc(
                """
                OpenAPI callbacks that should apply to all *path operations*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                """
            ),
        ] = None,
        webhooks: Annotated[
            routing.APIRouter | None,
            Doc(
                """
                Add OpenAPI webhooks. This is similar to `callbacks` but it doesn't
                depend on specific *path operations*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                **Note**: This is available since OpenAPI 3.1.0, FastAPI 0.99.0.

                Read more about it in the
                [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/).
                """
            ),
        ] = None,
        deprecated: Annotated[
            bool | None,
            Doc(
                """
                Mark all *path operations* as deprecated. You probably don't need it,
                but it's available.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#deprecate-a-path-operation).
                """
            ),
        ] = None,
        include_in_schema: Annotated[
            bool,
            Doc(
                """
                To include (or not) all the *path operations* in the generated OpenAPI.
                You probably don't need it, but it's available.

                This affects the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi).
                """
            ),
        ] = True,
        swagger_ui_parameters: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                Parameters to configure Swagger UI, the autogenerated interactive API
                documentation (by default at `/docs`).

                Read more about it in the
                [FastAPI docs about how to Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/).
                """
            ),
        ] = None,
        generate_unique_id_function: Annotated[
            Callable[[routing.APIRoute], str],
            Doc(
                """
                Customize the function used to generate unique IDs for the *path
                operations* shown in the generated OpenAPI.

                This is particularly useful when automatically generating clients or
                SDKs for your API.

                Read more about it in the
                [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                """
            ),
        ] = Default(generate_unique_id),
        separate_input_output_schemas: Annotated[
            bool,
            Doc(
                """
                Whether to generate separate OpenAPI schemas for request body and
                response body when the results would be more precise.

                This is particularly useful when automatically generating clients.

                For example, if you have a model like:

                ```python
                from pydantic import BaseModel

                class Item(BaseModel):
                    name: str
                    tags: list[str] = []
                ```

                When `Item` is used for input, a request body, `tags` is not required,
                the client doesn't have to provide it.

                But when using `Item` for output, for a response body, `tags` is always
                available because it has a default value, even if it's just an empty
                list. So, the client should be able to always expect it.

                In this case, there would be two different schemas, one for input and
                another one for output.

                Read more about it in the
                [FastAPI docs about how to separate schemas for input and output](https://fastapi.tiangolo.com/how-to/separate-openapi-schemas)
                """
            ),
        ] = True,
        openapi_external_docs: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                This field allows you to provide additional external documentation links.
                If provided, it must be a dictionary containing:

                * `description`: A brief description of the external documentation.
                * `url`: The URL pointing to the external documentation. The value **MUST**
                be a valid URL format.

                **Example**:

                ```python
                from fastapi import FastAPI

                external_docs = {
                    "description": "Detailed API Reference",
                    "url": "https://example.com/api-docs",
                }

                app = FastAPI(openapi_external_docs=external_docs)
                ```
                """
            ),
        ] = None,
        strict_content_type: Annotated[
            bool,
            Doc(
                """
                Enable strict checking for request Content-Type headers.

                When `True` (the default), requests with a body that do not include
                a `Content-Type` header will **not** be parsed as JSON.

                This prevents potential cross-site request forgery (CSRF) attacks
                that exploit the browser's ability to send requests without a
                Content-Type header, bypassing CORS preflight checks. In particular
                applicable for apps that need to be run locally (in localhost).

                When `False`, requests without a `Content-Type` header will have
                their body parsed as JSON, which maintains compatibility with
                certain clients that don't send `Content-Type` headers.

                Read more about it in the
                [FastAPI docs for Strict Content-Type](https://fastapi.tiangolo.com/advanced/strict-content-type/).
                """
            ),
        ] = True,
        **extra: Annotated[
            Any,
            Doc(
                """
                Extra keyword arguments to be stored in the app, not used by FastAPI
                anywhere.
                """
            ),
        ],
    ) -> None:
        self.debug = debug
        self.title = title
        self.summary = summary
        self.description = description
        self.version = version
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license_info = license_info
        self.openapi_url = openapi_url
        self.openapi_tags = openapi_tags
        self.root_path_in_servers = root_path_in_servers
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.swagger_ui_oauth2_redirect_url = swagger_ui_oauth2_redirect_url
        self.swagger_ui_init_oauth = swagger_ui_init_oauth
        self.swagger_ui_parameters = swagger_ui_parameters
        self.servers = servers or []
        self.separate_input_output_schemas = separate_input_output_schemas
        self.openapi_external_docs = openapi_external_docs
        self.extra = extra
        self.openapi_version: Annotated[
            str,
            Doc(
                """
                The version string of OpenAPI.

                FastAPI will generate OpenAPI version 3.1.0, and will output that as
                the OpenAPI version. But some tools, even though they might be
                compatible with OpenAPI 3.1.0, might not recognize it as a valid.

                So you could override this value to trick those tools into using
                the generated OpenAPI. Have in mind that this is a hack. But if you
                avoid using features added in OpenAPI 3.1.0, it might work for your
                use case.

                This is not passed as a parameter to the `FastAPI` class to avoid
                giving the false idea that FastAPI would generate a different OpenAPI
                schema. It is only available as an attribute.

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI()

                app.openapi_version = "3.0.2"
                ```
                """
            ),
        ] = "3.1.0"
        self.openapi_schema: dict[str, Any] | None = None
        self._openapi_routes_version: int | None = None
        if self.openapi_url:
            assert self.title, "A title must be provided for OpenAPI, e.g.: 'My API'"
            assert self.version, "A version must be provided for OpenAPI, e.g.: '2.1.0'"
        # TODO: remove when discarding the openapi_prefix parameter
        if openapi_prefix:
            logger.warning(
                '"openapi_prefix" has been deprecated in favor of "root_path", which '
                "follows more closely the ASGI standard, is simpler, and more "
                "automatic. Check the docs at "
                "https://fastapi.tiangolo.com/advanced/sub-applications/"
            )
        self.webhooks: Annotated[
            routing.APIRouter,
            Doc(
                """
                The `app.webhooks` attribute is an `APIRouter` with the *path
                operations* that will be used just for documentation of webhooks.

                Read more about it in the
                [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/).
                """
            ),
        ] = webhooks or routing.APIRouter()
        self.root_path = root_path or openapi_prefix
        self.state: Annotated[
            State,
            Doc(
                """
                A state object for the application. This is the same object for the
                entire application, it doesn't change from request to request.

                You normally wouldn't use this in FastAPI, for most of the cases you
                would instead use FastAPI dependencies.

                This is simply inherited from Starlette.

                Read more about it in the
                [Starlette docs for Applications](https://starlette.dev/applications/#storing-state-on-the-app-instance).
                """
            ),
        ] = State()
        self.dependency_overrides: Annotated[
            dict[Callable[..., Any], Callable[..., Any]],
            Doc(
                """
                A dictionary with overrides for the dependencies.

                Each key is the original dependency callable, and the value is the
                actual dependency that should be called.

                This is for testing, to replace expensive dependencies with testing
                versions.

                Read more about it in the
                [FastAPI docs for Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/).
                """
            ),
        ] = {}
        self.router: routing.APIRouter = routing.APIRouter(
            routes=routes,
            redirect_slashes=redirect_slashes,
            dependency_overrides_provider=self,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            default_response_class=default_response_class,
            dependencies=dependencies,
            callbacks=callbacks,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            responses=responses,
            generate_unique_id_function=generate_unique_id_function,
            strict_content_type=strict_content_type,
        )
        self.exception_handlers: dict[
            Any, Callable[[Request, Any], Response | Awaitable[Response]]
        ] = {} if exception_handlers is None else dict(exception_handlers)
        self.exception_handlers.setdefault(HTTPException, http_exception_handler)
        self.exception_handlers.setdefault(
            RequestValidationError, request_validation_exception_handler
        )

        # Starlette still has incorrect type specification for the handlers
        self.exception_handlers.setdefault(
            WebSocketRequestValidationError,
            websocket_request_validation_exception_handler,  # type: ignore[arg-type]
        )  # ty: ignore[no-matching-overload]

        self._telemetry: TelemetryConfig = {
            "tracer_provider": None,
            "meter_provider": None,
            "logger_provider": None,
            "tracing": True,
            "metrics": True,
            "logs": True,
            "operation_spans": True,
            "auto_configure": os.getenv("FASTAPI_OTEL_AUTO_CONFIGURE", "").lower()
            == "true",
            "exclude": None,
            **(telemetry if telemetry is not None else {}),
        }
        self._native_telemetry = NativeTelemetry(self._telemetry)

        self.user_middleware: list[Middleware] = (
            [] if middleware is None else list(middleware)
        )
        self.middleware_stack: ASGIApp | None = None
        self.setup()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self: AppType,
        *,
        telemetry: Annotated[
            TelemetryConfig | None,
            Doc(
                """
                Native OpenTelemetry configuration as a dictionary. Uses global
                providers by default. Omitted options keep their defaults.

                ```python
                app = FastAPI(telemetry={"tracing": False})
                ```
                """
            ),
        ] = None,
        debug: Annotated[
            bool,
            Doc(
                """
                Boolean indicating if debug tracebacks should be returned on server
                errors.

                Read more in the
                [Starlette docs for Applications](https://starlette.dev/applications/#starlette.applications.Starlette).
                """
            ),
        ] = False,
        routes: Annotated[
            list[BaseRoute] | None,
            Doc(
                """
                **Note**: you probably shouldn't use this parameter, it is inherited
                from Starlette and supported for compatibility.

                ---

                A list of routes to serve incoming HTTP and WebSocket requests.
                """
            ),
            deprecated(
                """
                You normally wouldn't use this parameter with FastAPI, it is inherited
                from Starlette and supported for compatibility.

                In FastAPI, you normally would use the *path operation methods*,
                like `app.get()`, `app.post()`, etc.
                """
            ),
        ] = None,
        title: Annotated[
            str,
            Doc(
                """
                The title of the API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(title="ChimichangApp")
                ```
                """
            ),
        ] = "FastAPI",
        summary: Annotated[
            str | None,
            Doc(
                """
                A short summary of the API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(summary="Deadpond's favorite app. Nuff said.")
                ```
                """
            ),
        ] = None,
        description: Annotated[
            str,
            Doc(
                '''
                A description of the API. Supports Markdown (using
                [CommonMark syntax](https://commonmark.org/)).

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(
                    description="""
                                ChimichangApp API helps you do awesome stuff. 🚀

                                ## Items

                                You can **read items**.

                                ## Users

                                You will be able to:

                                * **Create users** (_not implemented_).
                                * **Read users** (_not implemented_).

                                """
                )
                ```
                '''
            ),
        ] = "",
        version: Annotated[
            str,
            Doc(
                """
                The version of the API.

                **Note** This is the version of your application, not the version of
                the OpenAPI specification nor the version of FastAPI being used.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(version="0.0.1")
                ```
                """
            ),
        ] = "0.1.0",
        openapi_url: Annotated[
            str | None,
            Doc(
                """
                The URL where the OpenAPI schema will be served from.

                If you set it to `None`, no OpenAPI schema will be served publicly, and
                the default automatic endpoints `/docs` and `/redoc` will also be
                disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(openapi_url="/api/v1/openapi.json")
                ```
                """
            ),
        ] = "/openapi.json",
        openapi_tags: Annotated[
            list[dict[str, Any]] | None,
            Doc(
                """
                A list of tags used by OpenAPI, these are the same `tags` you can set
                in the *path operations*, like:

                * `@app.get("/users/", tags=["users"])`
                * `@app.get("/items/", tags=["items"])`

                The order of the tags can be used to specify the order shown in
                tools like Swagger UI, used in the automatic path `/docs`.

                It's not required to specify all the tags used.

                The tags that are not declared MAY be organized randomly or based
                on the tools' logic. Each tag name in the list MUST be unique.

                The value of each item is a `dict` containing:

                * `name`: The name of the tag.
                * `description`: A short description of the tag.
                    [CommonMark syntax](https://commonmark.org/) MAY be used for rich
                    text representation.
                * `externalDocs`: Additional external documentation for this tag. If
                    provided, it would contain a `dict` with:
                    * `description`: A short description of the target documentation.
                        [CommonMark syntax](https://commonmark.org/) MAY be used for
                        rich text representation.
                    * `url`: The URL for the target documentation. Value MUST be in
                        the form of a URL.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags).

                **Example**

                ```python
                from fastapi import FastAPI

                tags_metadata = [
                    {
                        "name": "users",
                        "description": "Operations with users. The **login** logic is also here.",
                    },
                    {
                        "name": "items",
                        "description": "Manage items. So _fancy_ they have their own docs.",
                        "externalDocs": {
                            "description": "Items external docs",
                            "url": "https://fastapi.tiangolo.com/",
                        },
                    },
                ]

                app = FastAPI(openapi_tags=tags_metadata)
                ```
                """
            ),
        ] = None,
        servers: Annotated[
            list[dict[str, str | Any]] | None,
            Doc(
                """
                A `list` of `dict`s with connectivity information to a target server.

                You would use it, for example, if your application is served from
                different domains and you want to use the same Swagger UI in the
                browser to interact with each of them (instead of having multiple
                browser tabs open). Or if you want to leave fixed the possible URLs.

                If the servers `list` is not provided, or is an empty `list`, the
                `servers` property in the generated OpenAPI will be:

                * a `dict` with a `url` value of the application's mounting point
                (`root_path`) if it's different from `/`.
                * otherwise, the `servers` property will be omitted from the OpenAPI
                schema.

                Each item in the `list` is a `dict` containing:

                * `url`: A URL to the target host. This URL supports Server Variables
                and MAY be relative, to indicate that the host location is relative
                to the location where the OpenAPI document is being served. Variable
                substitutions will be made when a variable is named in `{`brackets`}`.
                * `description`: An optional string describing the host designated by
                the URL. [CommonMark syntax](https://commonmark.org/) MAY be used for
                rich text representation.
                * `variables`: A `dict` between a variable name and its value. The value
                    is used for substitution in the server's URL template.

                Read more in the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#additional-servers).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(
                    servers=[
                        {"url": "https://stag.example.com", "description": "Staging environment"},
                        {"url": "https://prod.example.com", "description": "Production environment"},
                    ]
                )
                ```
                """
            ),
        ] = None,
        dependencies: Annotated[
            Sequence[Depends] | None,
            Doc(
                """
                A list of global dependencies, they will be applied to each
                *path operation*, including in sub-routers.

                Read more about it in the
                [FastAPI docs for Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/).

                **Example**

                ```python
                from fastapi import Depends, FastAPI

                from .dependencies import func_dep_1, func_dep_2

                app = FastAPI(dependencies=[Depends(func_dep_1), Depends(func_dep_2)])
                ```
                """
            ),
        ] = None,
        default_response_class: Annotated[
            type[Response],
            Doc(
                """
                The default response class to be used.

                Read more in the
                [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).

                **Example**

                ```python
                from fastapi import FastAPI
                from fastapi.responses import ORJSONResponse

                app = FastAPI(default_response_class=ORJSONResponse)
                ```
                """
            ),
        ] = Default(JSONResponse),
        redirect_slashes: Annotated[
            bool,
            Doc(
                """
                Whether to detect and redirect slashes in URLs when the client doesn't
                use the same format.

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(redirect_slashes=True)  # the default

                @app.get("/items/")
                async def read_items():
                    return [{"item_id": "Foo"}]
                ```

                With this app, if a client goes to `/items` (without a trailing slash),
                they will be automatically redirected with an HTTP status code of 307
                to `/items/`.
                """
            ),
        ] = True,
        docs_url: Annotated[
            str | None,
            Doc(
                """
                The path to the automatic interactive API documentation.
                It is handled in the browser by Swagger UI.

                The default URL is `/docs`. You can disable it by setting it to `None`.

                If `openapi_url` is set to `None`, this will be automatically disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(docs_url="/documentation", redoc_url=None)
                ```
                """
            ),
        ] = "/docs",
        redoc_url: Annotated[
            str | None,
            Doc(
                """
                The path to the alternative automatic interactive API documentation
                provided by ReDoc.

                The default URL is `/redoc`. You can disable it by setting it to `None`.

                If `openapi_url` is set to `None`, this will be automatically disabled.

                Read more in the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(docs_url="/documentation", redoc_url="redocumentation")
                ```
                """
            ),
        ] = "/redoc",
        swagger_ui_oauth2_redirect_url: Annotated[
            str | None,
            Doc(
                """
                The OAuth2 redirect endpoint for the Swagger UI.

                By default it is `/docs/oauth2-redirect`.

                This is only used if you use OAuth2 (with the "Authorize" button)
                with Swagger UI.
                """
            ),
        ] = "/docs/oauth2-redirect",
        swagger_ui_init_oauth: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                OAuth2 configuration for the Swagger UI, by default shown at `/docs`.

                Read more about the available configuration options in the
                [Swagger UI docs](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/).
                """
            ),
        ] = None,
        middleware: Annotated[
            Sequence[Middleware] | None,
            Doc(
                """
                List of middleware to be added when creating the application.

                In FastAPI you would normally do this with `app.add_middleware()`
                instead.

                Read more in the
                [FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/).
                """
            ),
        ] = None,
        exception_handlers: Annotated[
            dict[
                int | type[Exception],
                Callable[[Request, Any], Coroutine[Any, Any, Response]],
            ]
            | None,
            Doc(
                """
                A dictionary with handlers for exceptions.

                In FastAPI, you would normally use the decorator
                `@app.exception_handler()`.

                Read more in the
                [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).
                """
            ),
        ] = None,
        on_startup: Annotated[
            Sequence[Callable[[], Any]] | None,
            Doc(
                """
                A list of startup event handler functions.

                You should instead use the `lifespan` handlers.

                Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        on_shutdown: Annotated[
            Sequence[Callable[[], Any]] | None,
            Doc(
                """
                A list of shutdown event handler functions.

                You should instead use the `lifespan` handlers.

                Read more in the
                [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        lifespan: Annotated[
            Lifespan[AppType] | None,
            Doc(
                """
                A `Lifespan` context manager handler. This replaces `startup` and
                `shutdown` functions with a single context manager.

                Read more in the
                [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                """
            ),
        ] = None,
        terms_of_service: Annotated[
            str | None,
            Doc(
                """
                A URL to the Terms of Service for your API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more at the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                app = FastAPI(terms_of_service="http://example.com/terms/")
                ```
                """
            ),
        ] = None,
        contact: Annotated[
            dict[str, str | Any] | None,
            Doc(
                """
                A dictionary with the contact information for the exposed API.

                It can contain several fields.

                * `name`: (`str`) The name of the contact person/organization.
                * `url`: (`str`) A URL pointing to the contact information. MUST be in
                    the format of a URL.
                * `email`: (`str`) The email address of the contact person/organization.
                    MUST be in the format of an email address.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more at the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                app = FastAPI(
                    contact={
                        "name": "Deadpoolio the Amazing",
                        "url": "http://x-force.example.com/contact/",
                        "email": "dp@x-force.example.com",
                    }
                )
                ```
                """
            ),
        ] = None,
        license_info: Annotated[
            dict[str, str | Any] | None,
            Doc(
                """
                A dictionary with the license information for the exposed API.

                It can contain several fields.

                * `name`: (`str`) **REQUIRED** (if a `license_info` is set). The
                    license name used for the API.
                * `identifier`: (`str`) An [SPDX](https://spdx.dev/) license expression
                    for the API. The `identifier` field is mutually exclusive of the `url`
                    field. Available since OpenAPI 3.1.0, FastAPI 0.99.0.
                * `url`: (`str`) A URL to the license used for the API. This MUST be
                    the format of a URL.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more at the
                [FastAPI docs for Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api).

                **Example**

                ```python
                app = FastAPI(
                    license_info={
                        "name": "Apache 2.0",
                        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                    }
                )
                ```
                """
            ),
        ] = None,
        root_path: Annotated[
            str,
            Doc(
                """
                A path prefix handled by a proxy that is not seen by the application
                but is seen by external clients, which affects things like Swagger UI.

                Read more about it at the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(root_path="/api/v1")
                ```
                """
            ),
        ] = "",
        root_path_in_servers: Annotated[
            bool,
            Doc(
                """
                To disable automatically generating the URLs in the `servers` field
                in the autogenerated OpenAPI using the `root_path`.

                Read more about it in the
                [FastAPI docs for Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#disable-automatic-server-from-root-path).

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI(root_path_in_servers=False)
                ```
                """
            ),
        ] = True,
        responses: Annotated[
            dict[int | str, dict[str, Any]] | None,
            Doc(
                """
                Additional responses to be shown in OpenAPI.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).

                And in the
                [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
                """
            ),
        ] = None,
        callbacks: Annotated[
            list[BaseRoute] | None,
            Doc(
                """
                OpenAPI callbacks that should apply to all *path operations*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                """
            ),
        ] = None,
        webhooks: Annotated[
            routing.APIRouter | None,
            Doc(
                """
                Add OpenAPI webhooks. This is similar to `callbacks` but it doesn't
                depend on specific *path operations*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                **Note**: This is available since OpenAPI 3.1.0, FastAPI 0.99.0.

                Read more about it in the
                [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/).
                """
            ),
        ] = None,
        deprecated: Annotated[
            bool | None,
            Doc(
                """
                Mark all *path operations* as deprecated. You probably don't need it,
                but it's available.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#deprecate-a-path-operation).
                """
            ),
        ] = None,
        include_in_schema: Annotated[
            bool,
            Doc(
                """
                To include (or not) all the *path operations* in the generated OpenAPI.
                You probably don't need it, but it's available.

                This affects the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-parameters-from-openapi).
                """
            ),
        ] = True,
        swagger_ui_parameters: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                Parameters to configure Swagger UI, the autogenerated interactive API
                documentation (by default at `/docs`).

                Read more about it in the
                [FastAPI docs about how to Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/).
                """
            ),
        ] = None,
        generate_unique_id_function: Annotated[
            Callable[[routing.APIRoute], str],
            Doc(
                """
                Customize the function used to generate unique IDs for the *path
                operations* shown in the generated OpenAPI.

                This is particularly useful when automatically generating clients or
                SDKs for your API.

                Read more about it in the
                [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                """
            ),
        ] = Default(generate_unique_id),
        separate_input_output_schemas: Annotated[
            bool,
            Doc(
                """
                Whether to generate separate OpenAPI schemas for request body and
                response body when the results would be more precise.

                This is particularly useful when automatically generating clients.

                For example, if you have a model like:

                ```python
                from pydantic import BaseModel

                class Item(BaseModel):
                    name: str
                    tags: list[str] = []
                ```

                When `Item` is used for input, a request body, `tags` is not required,
                the client doesn't have to provide it.

                But when using `Item` for output, for a response body, `tags` is always
                available because it has a default value, even if it's just an empty
                list. So, the client should be able to always expect it.

                In this case, there would be two different schemas, one for input and
                another one for output.

                Read more about it in the
                [FastAPI docs about how to separate schemas for input and output](https://fastapi.tiangolo.com/how-to/separate-openapi-schemas)
                """
            ),
        ] = True,
        openapi_external_docs: Annotated[
            dict[str, Any] | None,
            Doc(
                """
                This field allows you to provide additional external documentation links.
                If provided, it must be a dictionary containing:

                * `description`: A brief description of the external documentation.
                * `url`: The URL pointing to the external documentation. The value **MUST**
                be a valid URL format.

                **Example**:

                ```python
                from fastapi import FastAPI

                external_docs = {
                    "description": "Detailed API Reference",
                    "url": "https://example.com/api-docs",
                }

                app = FastAPI(openapi_external_docs=external_docs)
                ```
                """
            ),
        ] = None,
        strict_content_type: Annotated[
            bool,
            Doc(
                """
                Enable strict checking for request Content-Type headers.

                When `True` (the default), requests with a body that do not include
                a `Content-Type` header will **not** be parsed as JSON.

                This prevents potential cross-site request forgery (CSRF) attacks
                that exploit the browser's ability to send requests without a
                Content-Type header, bypassing CORS preflight checks. In particular
                applicable for apps that need to be run locally (in localhost).

                When `False`, requests without a `Content-Type` header will have
                their body parsed as JSON, which maintains compatibility with
                certain clients that don't send `Content-Type` headers.

                Read more about it in the
                [FastAPI docs for Strict Content-Type](https://fastapi.tiangolo.com/advanced/strict-content-type/).
                """
            ),
        ] = True,
    ) -> None:
        self.debug = debug
        self.title = title
        self.summary = summary
        self.description = description
        self.version = version
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license_info = license_info
        self.openapi_url = openapi_url
        self.openapi_tags = openapi_tags
        self.root_path_in_servers = root_path_in_servers
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.swagger_ui_oauth2_redirect_url = swagger_ui_oauth2_redirect_url
        self.swagger_ui_init_oauth = swagger_ui_init_oauth
        self.swagger_ui_parameters = swagger_ui_parameters
        self.servers = servers or []
        self.separate_input_output_schemas = separate_input_output_schemas
        self.openapi_external_docs = openapi_external_docs
        self.openapi_version: Annotated[
            str,
            Doc(
                """
                The version string of OpenAPI.

                FastAPI will generate OpenAPI version 3.1.0, and will output that as
                the OpenAPI version. But some tools, even though they might be
                compatible with OpenAPI 3.1.0, might not recognize it as a valid.

                So you could override this value to trick those tools into using
                the generated OpenAPI. Have in mind that this is a hack. But if you
                avoid using features added in OpenAPI 3.1.0, it might work for your
                use case.

                This is not passed as a parameter to the `FastAPI` class to avoid
                giving the false idea that FastAPI would generate a different OpenAPI
                schema. It is only available as an attribute.

                **Example**

                ```python
                from fastapi import FastAPI

                app = FastAPI()

                app.openapi_version = "3.0.2"
                ```
                """
            ),
        ] = "3.1.0"
        self.openapi_schema: dict[str, Any] | None = None
        self._openapi_routes_version: int | None = None
        if self.openapi_url:
            assert self.title, "A title must be provided for OpenAPI, e.g.: 'My API'"
            assert self.version, "A version must be provided for OpenAPI, e.g.: '2.1.0'"
        self.webhooks: Annotated[
            routing.APIRouter,
            Doc(
                """
                The `app.webhooks` attribute is an `APIRouter` with the *path
                operations* that will be used just for documentation of webhooks.

                Read more about it in the
                [FastAPI docs for OpenAPI Webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/).
                """
            ),
        ] = webhooks or routing.APIRouter()
        self.root_path = root_path
        self.state: Annotated[
            State,
            Doc(
                """
                A state object for the application. This is the same object for the
                entire application, it doesn't change from request to request.

                You normally wouldn't use this in FastAPI, for most of the cases you
                would instead use FastAPI dependencies.

                This is simply inherited from Starlette.

                Read more about it in the
                [Starlette docs for Applications](https://starlette.dev/applications/#storing-state-on-the-app-instance).
                """
            ),
        ] = State()
        self.dependency_overrides: Annotated[
            dict[Callable[..., Any], Callable[..., Any]],
            Doc(
                """
                A dictionary with overrides for the dependencies.

                Each key is the original dependency callable, and the value is the
                actual dependency that should be called.

                This is for testing, to replace expensive dependencies with testing
                versions.

                Read more about it in the
                [FastAPI docs for Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/).
                """
            ),
        ] = {}
        self.router: routing.APIRouter = routing.APIRouter(
            routes=routes,
            redirect_slashes=redirect_slashes,
            dependency_overrides_provider=self,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            default_response_class=default_response_class,
            dependencies=dependencies,
            callbacks=callbacks,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            responses=responses,
            generate_unique_id_function=generate_unique_id_function,
            strict_content_type=strict_content_type,
        )
        self.exception_handlers: dict[
            Any, Callable[[Request, Any], Response | Awaitable[Response]]
        ] = {} if exception_handlers is None else dict(exception_handlers)
        self.exception_handlers.setdefault(HTTPException, http_exception_handler)
        self.exception_handlers.setdefault(
            RequestValidationError, request_validation_exception_handler
        )

        # Starlette still has incorrect type specification for the handlers
        self.exception_handlers.setdefault(
            WebSocketRequestValidationError,
            websocket_request_validation_exception_handler,  # type: ignore[arg-type]
        )  # ty: ignore[no-matching-overload]

        self._telemetry: TelemetryConfig = {
            "tracer_provider": None,
            "meter_provider": None,
            "logger_provider": None,
            "tracing": True,
            "metrics": True,
            "logs": True,
            "operation_spans": True,
            "auto_configure": os.getenv("FASTAPI_OTEL_AUTO_CONFIGURE", "").lower()
            == "true",
            "exclude": None,
            **(telemetry if telemetry is not None else {}),
        }
        self._native_telemetry = NativeTelemetry(self._telemetry)

        self.user_middleware: list[Middleware] = (
            [] if middleware is None else list(middleware)
        )
        self.middleware_stack: ASGIApp | None = None
        self.setup()
```


---

### 🔹 Commit #07: `1884325c`
- **完整 Hash**: `1884325cd6c880460ffa922457cc4224644eccc8`
- **說明 (Ground Truth)**: ✨ Add WebSocket support to security dependencies (#10147)
- **變更檔案數**: 4

#### 📄 檔案: `fastapi/security/api_key.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:13, E:15, A:0) ➔ After(N:13, E:15, A:0)
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

### 🔹 函式: `APIKeyBase.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, location: APIKeyIn, name: str, description: str | None, scheme_name: str | None, auto_error: bool, )` (L14~L29)
- **變更後簽章 (After)**: `def __init__( self, location: APIKeyIn, name: str, description: str | None, scheme_name: str | None, auto_error: bool, )` (L14~L29)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        location: APIKeyIn,
        name: str,
        description: str | None,
        scheme_name: str | None,
        auto_error: bool,
    ):
        self.auto_error = auto_error

        self.model: APIKey = APIKey(
            **{"in": location},
            name=name,
            description=description,
        )
        self.scheme_name = scheme_name or self.__class__.__name__
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        location: APIKeyIn,
        name: str,
        description: str | None,
        scheme_name: str | None,
        auto_error: bool,
    ):
        self.auto_error = auto_error

        self.model = APIKey(
            **{"in": location},
            name=name,
            description=description,
        )
        self.scheme_name = scheme_name or self.__class__.__name__
```


#### 📄 檔案: `fastapi/security/http.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:21, E:24, A:0) ➔ After(N:21, E:24, A:0)
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

#### 📄 檔案: `fastapi/security/oauth2.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:19, E:29, A:0) ➔ After(N:19, E:29, A:0)
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

#### 📄 檔案: `fastapi/security/open_id_connect_url.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:6, E:4, A:0) ➔ After(N:6, E:4, A:0)
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

### 🔹 Commit #08: `fab6eeac`
- **完整 Hash**: `fab6eeacae4a37d983f545f4cb3479f101942d58`
- **說明 (Ground Truth)**: 🐛 Fix handling of empty value for `byte` file list parameter (#9383)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/dependencies/utils.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:91, E:130, A:0) ➔ After(N:91, E:130, A:0)
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

### 🔹 函式: `_extract_form_body()`
- **變更前簽章 (Before)**: `async def _extract_form_body( body_fields: list[ModelField], received_body: FormData, ) -> dict[str, Any]` (L912~L948)
- **變更後簽章 (After)**: `async def _extract_form_body( body_fields: list[ModelField], received_body: FormData, ) -> dict[str, Any]` (L912~L951)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def _extract_form_body(
    body_fields: list[ModelField],
    received_body: FormData,
) -> dict[str, Any]:
    values = {}

    for field in body_fields:
        value = _get_multidict_value(field, received_body)
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
                results.append(await sub_value.read())
            value = serialize_sequence_value(field=field, value=results)
        if value is not None:
            values[get_validation_alias(field)] = value
    field_aliases = {get_validation_alias(field) for field in body_fields}
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
    values = {}

    for field in body_fields:
        value = _get_multidict_value(field, received_body)
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
        if value is not None:
            values[get_validation_alias(field)] = value
    field_aliases = {get_validation_alias(field) for field in body_fields}
    for key in received_body.keys():
        if key not in field_aliases:
            param_values = received_body.getlist(key)
            if len(param_values) == 1:
                values[key] = param_values[0]
            else:
                values[key] = param_values
    return values
```


---

### 🔹 Commit #09: `d1fd422f`
- **完整 Hash**: `d1fd422fd9c3b24b0e2bcf1cc89f1e7249b5fcd6`
- **說明 (Ground Truth)**: 🐛 Fix non-finite float serialization in JSONL and SSE streams (#16509)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/routing.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:285, E:432, A:0) ➔ After(N:287, E:436, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 4, -Edges: 0, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `isfinite (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `_normalize_non_finite_floats` (FUNCTION_DEF)
  • + [新增呼叫邊] `_normalize_non_finite_floats` ──[CALLS]──> `isfinite (External/Unresolved)`
  • + [新增呼叫邊] `_normalize_non_finite_floats` ──[CALLS]──> `_normalize_non_finite_floats`
  • + [新增呼叫邊] `_serialize_data` ──[CALLS]──> `_normalize_non_finite_floats`
  • + [新增呼叫邊] `_serialize_sse_item` ──[CALLS]──> `_normalize_non_finite_floats`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'app' 被深鎖在內部閉包 (scope:request_response@after/fastapi/routing.py:L129)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `app()`
- **變更前簽章 (Before)**: `async def app(request: Request) -> Response` (L416~L782)
- **變更後簽章 (After)**: `async def app(request: Request) -> Response` (L428~L800)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def app(request: Request) -> Response:
        telemetry_data = get_telemetry_data()
        if telemetry_data is not None:
            telemetry_data.request = request
        response: Response | None = None
        file_stack = request.scope.get("fastapi_middleware_astack")
        assert isinstance(file_stack, AsyncExitStack), (
            "fastapi_middleware_astack not found in request scope"
        )

        # Extract endpoint context for error messages
        endpoint_ctx = (
            _extract_endpoint_context(dependant.call)
            if dependant.call
            else EndpointContext()
        )

        if dependant.path:
            # For mounted sub-apps, include the mount path prefix
            mount_path = request.scope.get("root_path", "").rstrip("/")
            endpoint_ctx["path"] = f"{request.method} {mount_path}{dependant.path}"

        # Read body and auto-close files
        try:
            body: Any = None
            if body_field:
                if is_body_form:
                    body = await request.form()
                    file_stack.push_async_callback(body.close)
                else:
                    body_bytes = await request.body()
                    if body_bytes:
                        json_body: Any = Undefined
                        content_type_value = request.headers.get("content-type")
                        if not content_type_value:
                            if not actual_strict_content_type:
                                json_body = await request.json()
                        else:
                            message = email.message.Message()
                            message["content-type"] = content_type_value
                            if message.get_content_maintype() == "application":
                                subtype = message.get_content_subtype()
                                if subtype == "json" or subtype.endswith("+json"):
                                    json_body = await request.json()
                        if json_body != Undefined:
                            body = json_body
                        else:
                            body = body_bytes
        except json.JSONDecodeError as e:
            validation_error = RequestValidationError(
                [
                    {
                        "type": "json_invalid",
                        "loc": ("body", e.pos),
                        "msg": "JSON decode error",
                        "input": {},
                        "ctx": {"error": e.msg},
                    }
                ],
                body=e.doc,
                endpoint_ctx=endpoint_ctx,
            )
            _validation_failed(validation_error)
            raise validation_error from e
        except HTTPException:
            # If a middleware raises an HTTPException, it should be raised again
            raise
        except Exception as e:
            http_error = HTTPException(
                status_code=400, detail="There was an error parsing the body"
            )
            raise http_error from e

        if telemetry_data is not None:
            telemetry_data.body = body

        # Solve dependencies and run path operation function, auto-closing dependencies
        errors: list[Any] = []
        async_exit_stack = request.scope.get("fastapi_inner_astack")
        assert isinstance(async_exit_stack, AsyncExitStack), (
            "fastapi_inner_astack not found in request scope"
        )
        with _operation(name="dependencies", function=dependant.call):
            solved_result = await solve_dependencies(
                request=request,
                dependant=dependant,
                body=cast(dict[str, Any] | FormData | bytes | None, body),
                dependency_overrides_provider=dependency_overrides_provider,
                async_exit_stack=async_exit_stack,
                embed_body_fields=embed_body_fields,
            )
            if telemetry_data is not None:
                telemetry_data.values = solved_result.values
                telemetry_data.errors = solved_result.errors
        errors = solved_result.errors
        assert dependant.call  # For types
        if not errors:
            # Shared serializer for stream items (JSONL and SSE).
            # Validates against stream_item_field when set, then
            # serializes to JSON bytes.
            def _serialize_data(data: Any) -> bytes:
                if stream_item_field:
                    value, errors_ = stream_item_field.validate(
                        data, {}, loc=("response",)
                    )
                    if errors_:
                        ctx = endpoint_ctx or EndpointContext()
                        raise ResponseValidationError(
                            errors=errors_,
                            body=data,
                            endpoint_ctx=ctx,
                        )
                    return stream_item_field.serialize_json(
                        value,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                    )
                else:
                    data = jsonable_encoder(data)
                    return json.dumps(data).encode("utf-8")

            if is_sse_stream:
                # Generator endpoint: stream as Server-Sent Events
                gen = dependant.call(**solved_result.values)

                def _serialize_sse_item(item: Any) -> bytes:
                    if isinstance(item, ServerSentEvent):
                        # User controls the event structure.
                        # Serialize the data payload if present.
                        # For ServerSentEvent items we skip stream_item_field
                        # validation (the user may mix types intentionally).
                        if item.raw_data is not None:
                            data_str: str | None = item.raw_data
                        elif item.data is not None:
                            if hasattr(item.data, "model_dump_json"):
                                data_str = item.data.model_dump_json()
                            else:
                                data_str = json.dumps(jsonable_encoder(item.data))
                        else:
                            data_str = None
                        return format_sse_event(
                            data_str=data_str,
                            event=item.event,
                            id=item.id,
                            retry=item.retry,
                            comment=item.comment,
                        )
                    else:
                        # Plain object: validate + serialize via
                        # stream_item_field (if set) and wrap in data field
                        return format_sse_event(
                            data_str=_serialize_data(item).decode("utf-8")
                        )

                if _is_async_gen_callable(dependant.call):
                    sse_aiter: AsyncIterator[Any] = gen.__aiter__()
                else:
                    sse_aiter = iterate_in_threadpool(gen)

                @asynccontextmanager
                async def _sse_producer_cm() -> AsyncIterator[
                    ObjectReceiveStream[bytes]
                ]:
                    # Use a memory stream to decouple generator iteration
                    # from the keepalive timer. A producer task pulls items
                    # from the generator independently, so
                    # `anyio.fail_after` never wraps the generator's
                    # `__anext__` directly - avoiding CancelledError that
                    # would finalize the generator and also working for sync
                    # generators running in a thread pool.
                    #
                    # This context manager is entered on the request-scoped
                    # AsyncExitStack so its __aexit__ (which cancels the
                    # task group) is called by the exit stack after the
                    # streaming response completes — not by async generator
                    # finalization via GeneratorExit.
                    # Ref: https://peps.python.org/pep-0789/
                    send_stream, receive_stream = anyio.create_memory_object_stream[
                        bytes
                    ](max_buffer_size=1)

                    async def _producer() -> None:
                        async with send_stream:
                            async for raw_item in sse_aiter:
                                await send_stream.send(_serialize_sse_item(raw_item))

                    send_keepalive, receive_keepalive = (
                        anyio.create_memory_object_stream[bytes](max_buffer_size=1)
                    )

                    async def _keepalive_inserter() -> None:
                        """Read from the producer and forward to the output,
                        inserting keepalive comments on timeout."""
                        async with send_keepalive, receive_stream:
                            try:
                                while True:
                                    try:
                                        with anyio.fail_after(_PING_INTERVAL):
                                            data = await receive_stream.receive()
                                        await send_keepalive.send(data)
                                    except TimeoutError:
                                        await send_keepalive.send(KEEPALIVE_COMMENT)
                            except anyio.EndOfStream:
                                pass

                    async with anyio.create_task_group() as tg:
                        tg.start_soon(_producer)
                        tg.start_soon(_keepalive_inserter)
                        yield receive_keepalive
                        tg.cancel_scope.cancel()

                # Enter the SSE context manager on the request-scoped
                # exit stack. The stack outlives the streaming response,
                # so __aexit__ runs via proper structured teardown, not
                # via GeneratorExit thrown into an async generator.
                sse_receive_stream = await async_exit_stack.enter_async_context(
                    _sse_producer_cm()
                )
                # Ensure the receive stream is closed when the exit stack
                # unwinds, preventing ResourceWarning from __del__.
                async_exit_stack.push_async_callback(sse_receive_stream.aclose)

                async def _sse_with_checkpoints(
                    stream: ObjectReceiveStream[bytes],
                ) -> AsyncIterator[bytes]:
                    async for data in stream:
                        yield data
                        # Guarantee a checkpoint so cancellation can be
                        # delivered even when the producer is faster than
                        # the consumer and receive() never suspends.
                        await anyio.sleep(0)

                sse_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                    _sse_with_checkpoints(sse_receive_stream)
                )

                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = StreamingResponse(
                    sse_stream_content,
                    media_type="text/event-stream",
                    **response_args,
                )
                response.headers["Cache-Control"] = "no-cache"
                # For Nginx proxies to not buffer server sent events
                response.headers["X-Accel-Buffering"] = "no"
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif is_json_stream:
                # Generator endpoint: stream as JSONL
                gen = dependant.call(**solved_result.values)

                def _serialize_item(item: Any) -> bytes:
                    return _serialize_data(item) + b"\n"

                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_jsonl() -> AsyncIterator[bytes]:
                        async for item in gen:
                            yield _serialize_item(item)
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    jsonl_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                        _async_stream_jsonl()
                    )
                else:

                    def _sync_stream_jsonl() -> Iterator[bytes]:
                        for item in gen:  # ty: ignore[not-iterable]
                            yield _serialize_item(item)

                    jsonl_stream_content = _sync_stream_jsonl()

                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = StreamingResponse(
                    jsonl_stream_content,
                    media_type="application/jsonl",
                    **response_args,
                )
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif _is_async_gen_callable(dependant.call) or _is_gen_callable(
                dependant.call
            ):
                # Raw streaming with explicit response_class (e.g. StreamingResponse)
                gen = dependant.call(**solved_result.values)
                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_raw(
                        async_gen: AsyncIterator[Any],
                    ) -> AsyncIterator[Any]:
                        async for chunk in async_gen:
                            yield chunk
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    gen = _async_stream_raw(gen)
                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = actual_response_class(content=gen, **response_args)
                response.headers.raw.extend(solved_result.response.headers.raw)
            else:
                raw_response = await run_endpoint_function(
                    dependant=dependant,
                    values=solved_result.values,
                    is_coroutine=is_coroutine,
                )
                if isinstance(raw_response, Response):
                    if raw_response.background is None:
                        raw_response.background = solved_result.background_tasks
                    response = raw_response
                else:
                    response_args = _build_response_args(
                        status_code=status_code, solved_result=solved_result
                    )
                    # Use the fast path (dump_json) when no custom response
                    # class was set and a response field with a TypeAdapter
                    # exists. Serializes directly to JSON bytes via Pydantic's
                    # Rust core, skipping the intermediate Python dict +
                    # json.dumps() step.
                    use_dump_json = response_field is not None and isinstance(
                        response_class, DefaultPlaceholder
                    )
                    with _operation(name="serialization", function=dependant.call):
                        content = await serialize_response(
                            field=response_field,
                            response_content=raw_response,
                            include=response_model_include,
                            exclude=response_model_exclude,
                            by_alias=response_model_by_alias,
                            exclude_unset=response_model_exclude_unset,
                            exclude_defaults=response_model_exclude_defaults,
                            exclude_none=response_model_exclude_none,
                            is_coroutine=is_coroutine,
                            endpoint_ctx=endpoint_ctx,
                            dump_json=use_dump_json,
                        )
                    if use_dump_json:
                        response = Response(
                            content=content,
                            media_type="application/json",
                            **response_args,
                        )
                    else:
                        response = actual_response_class(content, **response_args)
                    if not is_body_allowed_for_status_code(response.status_code):
                        response.body = b""
                    response.headers.raw.extend(solved_result.response.headers.raw)
        if errors:
            validation_error = RequestValidationError(
                errors, body=body, endpoint_ctx=endpoint_ctx
            )
            _validation_failed(validation_error)
            raise validation_error

        # Return response
        assert response
        return response
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def app(request: Request) -> Response:
        telemetry_data = get_telemetry_data()
        if telemetry_data is not None:
            telemetry_data.request = request
        response: Response | None = None
        file_stack = request.scope.get("fastapi_middleware_astack")
        assert isinstance(file_stack, AsyncExitStack), (
            "fastapi_middleware_astack not found in request scope"
        )

        # Extract endpoint context for error messages
        endpoint_ctx = (
            _extract_endpoint_context(dependant.call)
            if dependant.call
            else EndpointContext()
        )

        if dependant.path:
            # For mounted sub-apps, include the mount path prefix
            mount_path = request.scope.get("root_path", "").rstrip("/")
            endpoint_ctx["path"] = f"{request.method} {mount_path}{dependant.path}"

        # Read body and auto-close files
        try:
            body: Any = None
            if body_field:
                if is_body_form:
                    body = await request.form()
                    file_stack.push_async_callback(body.close)
                else:
                    body_bytes = await request.body()
                    if body_bytes:
                        json_body: Any = Undefined
                        content_type_value = request.headers.get("content-type")
                        if not content_type_value:
                            if not actual_strict_content_type:
                                json_body = await request.json()
                        else:
                            message = email.message.Message()
                            message["content-type"] = content_type_value
                            if message.get_content_maintype() == "application":
                                subtype = message.get_content_subtype()
                                if subtype == "json" or subtype.endswith("+json"):
                                    json_body = await request.json()
                        if json_body != Undefined:
                            body = json_body
                        else:
                            body = body_bytes
        except json.JSONDecodeError as e:
            validation_error = RequestValidationError(
                [
                    {
                        "type": "json_invalid",
                        "loc": ("body", e.pos),
                        "msg": "JSON decode error",
                        "input": {},
                        "ctx": {"error": e.msg},
                    }
                ],
                body=e.doc,
                endpoint_ctx=endpoint_ctx,
            )
            _validation_failed(validation_error)
            raise validation_error from e
        except HTTPException:
            # If a middleware raises an HTTPException, it should be raised again
            raise
        except Exception as e:
            http_error = HTTPException(
                status_code=400, detail="There was an error parsing the body"
            )
            raise http_error from e

        if telemetry_data is not None:
            telemetry_data.body = body

        # Solve dependencies and run path operation function, auto-closing dependencies
        errors: list[Any] = []
        async_exit_stack = request.scope.get("fastapi_inner_astack")
        assert isinstance(async_exit_stack, AsyncExitStack), (
            "fastapi_inner_astack not found in request scope"
        )
        with _operation(name="dependencies", function=dependant.call):
            solved_result = await solve_dependencies(
                request=request,
                dependant=dependant,
                body=cast(dict[str, Any] | FormData | bytes | None, body),
                dependency_overrides_provider=dependency_overrides_provider,
                async_exit_stack=async_exit_stack,
                embed_body_fields=embed_body_fields,
            )
            if telemetry_data is not None:
                telemetry_data.values = solved_result.values
                telemetry_data.errors = solved_result.errors
        errors = solved_result.errors
        assert dependant.call  # For types
        if not errors:
            # Shared serializer for stream items (JSONL and SSE).
            # Validates against stream_item_field when set, then
            # serializes to JSON bytes.
            def _serialize_data(data: Any) -> bytes:
                if stream_item_field:
                    value, errors_ = stream_item_field.validate(
                        data, {}, loc=("response",)
                    )
                    if errors_:
                        ctx = endpoint_ctx or EndpointContext()
                        raise ResponseValidationError(
                            errors=errors_,
                            body=data,
                            endpoint_ctx=ctx,
                        )
                    return stream_item_field.serialize_json(
                        value,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                    )
                else:
                    data = jsonable_encoder(data)
                    return json.dumps(_normalize_non_finite_floats(data)).encode(
                        "utf-8"
                    )

            if is_sse_stream:
                # Generator endpoint: stream as Server-Sent Events
                gen = dependant.call(**solved_result.values)

                def _serialize_sse_item(item: Any) -> bytes:
                    if isinstance(item, ServerSentEvent):
                        # User controls the event structure.
                        # Serialize the data payload if present.
                        # For ServerSentEvent items we skip stream_item_field
                        # validation (the user may mix types intentionally).
                        if item.raw_data is not None:
                            data_str: str | None = item.raw_data
                        elif item.data is not None:
                            if hasattr(item.data, "model_dump_json"):
                                data_str = item.data.model_dump_json()
                            else:
                                data_str = json.dumps(
                                    _normalize_non_finite_floats(
                                        jsonable_encoder(item.data)
                                    )
                                )
                        else:
                            data_str = None
                        return format_sse_event(
                            data_str=data_str,
                            event=item.event,
                            id=item.id,
                            retry=item.retry,
                            comment=item.comment,
                        )
                    else:
                        # Plain object: validate + serialize via
                        # stream_item_field (if set) and wrap in data field
                        return format_sse_event(
                            data_str=_serialize_data(item).decode("utf-8")
                        )

                if _is_async_gen_callable(dependant.call):
                    sse_aiter: AsyncIterator[Any] = gen.__aiter__()
                else:
                    sse_aiter = iterate_in_threadpool(gen)

                @asynccontextmanager
                async def _sse_producer_cm() -> AsyncIterator[
                    ObjectReceiveStream[bytes]
                ]:
                    # Use a memory stream to decouple generator iteration
                    # from the keepalive timer. A producer task pulls items
                    # from the generator independently, so
                    # `anyio.fail_after` never wraps the generator's
                    # `__anext__` directly - avoiding CancelledError that
                    # would finalize the generator and also working for sync
                    # generators running in a thread pool.
                    #
                    # This context manager is entered on the request-scoped
                    # AsyncExitStack so its __aexit__ (which cancels the
                    # task group) is called by the exit stack after the
                    # streaming response completes — not by async generator
                    # finalization via GeneratorExit.
                    # Ref: https://peps.python.org/pep-0789/
                    send_stream, receive_stream = anyio.create_memory_object_stream[
                        bytes
                    ](max_buffer_size=1)

                    async def _producer() -> None:
                        async with send_stream:
                            async for raw_item in sse_aiter:
                                await send_stream.send(_serialize_sse_item(raw_item))

                    send_keepalive, receive_keepalive = (
                        anyio.create_memory_object_stream[bytes](max_buffer_size=1)
                    )

                    async def _keepalive_inserter() -> None:
                        """Read from the producer and forward to the output,
                        inserting keepalive comments on timeout."""
                        async with send_keepalive, receive_stream:
                            try:
                                while True:
                                    try:
                                        with anyio.fail_after(_PING_INTERVAL):
                                            data = await receive_stream.receive()
                                        await send_keepalive.send(data)
                                    except TimeoutError:
                                        await send_keepalive.send(KEEPALIVE_COMMENT)
                            except anyio.EndOfStream:
                                pass

                    async with anyio.create_task_group() as tg:
                        tg.start_soon(_producer)
                        tg.start_soon(_keepalive_inserter)
                        yield receive_keepalive
                        tg.cancel_scope.cancel()

                # Enter the SSE context manager on the request-scoped
                # exit stack. The stack outlives the streaming response,
                # so __aexit__ runs via proper structured teardown, not
                # via GeneratorExit thrown into an async generator.
                sse_receive_stream = await async_exit_stack.enter_async_context(
                    _sse_producer_cm()
                )
                # Ensure the receive stream is closed when the exit stack
                # unwinds, preventing ResourceWarning from __del__.
                async_exit_stack.push_async_callback(sse_receive_stream.aclose)

                async def _sse_with_checkpoints(
                    stream: ObjectReceiveStream[bytes],
                ) -> AsyncIterator[bytes]:
                    async for data in stream:
                        yield data
                        # Guarantee a checkpoint so cancellation can be
                        # delivered even when the producer is faster than
                        # the consumer and receive() never suspends.
                        await anyio.sleep(0)

                sse_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                    _sse_with_checkpoints(sse_receive_stream)
                )

                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = StreamingResponse(
                    sse_stream_content,
                    media_type="text/event-stream",
                    **response_args,
                )
                response.headers["Cache-Control"] = "no-cache"
                # For Nginx proxies to not buffer server sent events
                response.headers["X-Accel-Buffering"] = "no"
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif is_json_stream:
                # Generator endpoint: stream as JSONL
                gen = dependant.call(**solved_result.values)

                def _serialize_item(item: Any) -> bytes:
                    return _serialize_data(item) + b"\n"

                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_jsonl() -> AsyncIterator[bytes]:
                        async for item in gen:
                            yield _serialize_item(item)
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    jsonl_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                        _async_stream_jsonl()
                    )
                else:

                    def _sync_stream_jsonl() -> Iterator[bytes]:
                        for item in gen:  # ty: ignore[not-iterable]
                            yield _serialize_item(item)

                    jsonl_stream_content = _sync_stream_jsonl()

                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = StreamingResponse(
                    jsonl_stream_content,
                    media_type="application/jsonl",
                    **response_args,
                )
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif _is_async_gen_callable(dependant.call) or _is_gen_callable(
                dependant.call
            ):
                # Raw streaming with explicit response_class (e.g. StreamingResponse)
                gen = dependant.call(**solved_result.values)
                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_raw(
                        async_gen: AsyncIterator[Any],
                    ) -> AsyncIterator[Any]:
                        async for chunk in async_gen:
                            yield chunk
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    gen = _async_stream_raw(gen)
                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = actual_response_class(content=gen, **response_args)
                response.headers.raw.extend(solved_result.response.headers.raw)
            else:
                raw_response = await run_endpoint_function(
                    dependant=dependant,
                    values=solved_result.values,
                    is_coroutine=is_coroutine,
                )
                if isinstance(raw_response, Response):
                    if raw_response.background is None:
                        raw_response.background = solved_result.background_tasks
                    response = raw_response
                else:
                    response_args = _build_response_args(
                        status_code=status_code, solved_result=solved_result
                    )
                    # Use the fast path (dump_json) when no custom response
                    # class was set and a response field with a TypeAdapter
                    # exists. Serializes directly to JSON bytes via Pydantic's
                    # Rust core, skipping the intermediate Python dict +
                    # json.dumps() step.
                    use_dump_json = response_field is not None and isinstance(
                        response_class, DefaultPlaceholder
                    )
                    with _operation(name="serialization", function=dependant.call):
                        content = await serialize_response(
                            field=response_field,
                            response_content=raw_response,
                            include=response_model_include,
                            exclude=response_model_exclude,
                            by_alias=response_model_by_alias,
                            exclude_unset=response_model_exclude_unset,
                            exclude_defaults=response_model_exclude_defaults,
                            exclude_none=response_model_exclude_none,
                            is_coroutine=is_coroutine,
                            endpoint_ctx=endpoint_ctx,
                            dump_json=use_dump_json,
                        )
                    if use_dump_json:
                        response = Response(
                            content=content,
                            media_type="application/json",
                            **response_args,
                        )
                    else:
                        response = actual_response_class(content, **response_args)
                    if not is_body_allowed_for_status_code(response.status_code):
                        response.body = b""
                    response.headers.raw.extend(solved_result.response.headers.raw)
        if errors:
            validation_error = RequestValidationError(
                errors, body=body, endpoint_ctx=endpoint_ctx
            )
            _validation_failed(validation_error)
            raise validation_error

        # Return response
        assert response
        return response
```

### 🔹 函式: `get_request_handler()`
- **變更前簽章 (Before)**: `def get_request_handler( dependant: Dependant, body_field: ModelField | None = None, status_code: int | None = None, response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse), response_field: ModelField | None = None, response_model_include: IncEx | None = None, response_model_exclude: IncEx | None = None, response_model_by_alias: bool = True, response_model_exclude_unset: bool = False, response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False, dependency_overrides_provider: Any | None = None, embed_body_fields: bool = False, strict_content_type: bool | DefaultPlaceholder = Default(True), stream_item_field: ModelField | None = None, is_json_stream: bool = False, ) -> Callable[[Request], Coroutine[Any, Any, Response]]` (L385~L784)
- **變更後簽章 (After)**: `def get_request_handler( dependant: Dependant, body_field: ModelField | None = None, status_code: int | None = None, response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse), response_field: ModelField | None = None, response_model_include: IncEx | None = None, response_model_exclude: IncEx | None = None, response_model_by_alias: bool = True, response_model_exclude_unset: bool = False, response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False, dependency_overrides_provider: Any | None = None, embed_body_fields: bool = False, strict_content_type: bool | DefaultPlaceholder = Default(True), stream_item_field: ModelField | None = None, is_json_stream: bool = False, ) -> Callable[[Request], Coroutine[Any, Any, Response]]` (L397~L802)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def get_request_handler(
    dependant: Dependant,
    body_field: ModelField | None = None,
    status_code: int | None = None,
    response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse),
    response_field: ModelField | None = None,
    response_model_include: IncEx | None = None,
    response_model_exclude: IncEx | None = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    dependency_overrides_provider: Any | None = None,
    embed_body_fields: bool = False,
    strict_content_type: bool | DefaultPlaceholder = Default(True),
    stream_item_field: ModelField | None = None,
    is_json_stream: bool = False,
) -> Callable[[Request], Coroutine[Any, Any, Response]]:
    assert dependant.call is not None, "dependant.call must be a function"
    is_coroutine = _is_coroutine_callable(dependant.call)
    is_body_form = body_field and isinstance(body_field.field_info, params.Form)
    if isinstance(response_class, DefaultPlaceholder):
        actual_response_class: type[Response] = response_class.value
    else:
        actual_response_class = response_class
    is_sse_stream = lenient_issubclass(actual_response_class, EventSourceResponse)
    if isinstance(strict_content_type, DefaultPlaceholder):
        actual_strict_content_type: bool = strict_content_type.value
    else:
        actual_strict_content_type = strict_content_type

    async def app(request: Request) -> Response:
        telemetry_data = get_telemetry_data()
        if telemetry_data is not None:
            telemetry_data.request = request
        response: Response | None = None
        file_stack = request.scope.get("fastapi_middleware_astack")
        assert isinstance(file_stack, AsyncExitStack), (
            "fastapi_middleware_astack not found in request scope"
        )

        # Extract endpoint context for error messages
        endpoint_ctx = (
            _extract_endpoint_context(dependant.call)
            if dependant.call
            else EndpointContext()
        )

        if dependant.path:
            # For mounted sub-apps, include the mount path prefix
            mount_path = request.scope.get("root_path", "").rstrip("/")
            endpoint_ctx["path"] = f"{request.method} {mount_path}{dependant.path}"

        # Read body and auto-close files
        try:
            body: Any = None
            if body_field:
                if is_body_form:
                    body = await request.form()
                    file_stack.push_async_callback(body.close)
                else:
                    body_bytes = await request.body()
                    if body_bytes:
                        json_body: Any = Undefined
                        content_type_value = request.headers.get("content-type")
                        if not content_type_value:
                            if not actual_strict_content_type:
                                json_body = await request.json()
                        else:
                            message = email.message.Message()
                            message["content-type"] = content_type_value
                            if message.get_content_maintype() == "application":
                                subtype = message.get_content_subtype()
                                if subtype == "json" or subtype.endswith("+json"):
                                    json_body = await request.json()
                        if json_body != Undefined:
                            body = json_body
                        else:
                            body = body_bytes
        except json.JSONDecodeError as e:
            validation_error = RequestValidationError(
                [
                    {
                        "type": "json_invalid",
                        "loc": ("body", e.pos),
                        "msg": "JSON decode error",
                        "input": {},
                        "ctx": {"error": e.msg},
                    }
                ],
                body=e.doc,
                endpoint_ctx=endpoint_ctx,
            )
            _validation_failed(validation_error)
            raise validation_error from e
        except HTTPException:
            # If a middleware raises an HTTPException, it should be raised again
            raise
        except Exception as e:
            http_error = HTTPException(
                status_code=400, detail="There was an error parsing the body"
            )
            raise http_error from e

        if telemetry_data is not None:
            telemetry_data.body = body

        # Solve dependencies and run path operation function, auto-closing dependencies
        errors: list[Any] = []
        async_exit_stack = request.scope.get("fastapi_inner_astack")
        assert isinstance(async_exit_stack, AsyncExitStack), (
            "fastapi_inner_astack not found in request scope"
        )
        with _operation(name="dependencies", function=dependant.call):
            solved_result = await solve_dependencies(
                request=request,
                dependant=dependant,
                body=cast(dict[str, Any] | FormData | bytes | None, body),
                dependency_overrides_provider=dependency_overrides_provider,
                async_exit_stack=async_exit_stack,
                embed_body_fields=embed_body_fields,
            )
            if telemetry_data is not None:
                telemetry_data.values = solved_result.values
                telemetry_data.errors = solved_result.errors
        errors = solved_result.errors
        assert dependant.call  # For types
        if not errors:
            # Shared serializer for stream items (JSONL and SSE).
            # Validates against stream_item_field when set, then
            # serializes to JSON bytes.
            def _serialize_data(data: Any) -> bytes:
                if stream_item_field:
                    value, errors_ = stream_item_field.validate(
                        data, {}, loc=("response",)
                    )
                    if errors_:
                        ctx = endpoint_ctx or EndpointContext()
                        raise ResponseValidationError(
                            errors=errors_,
                            body=data,
                            endpoint_ctx=ctx,
                        )
                    return stream_item_field.serialize_json(
                        value,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                    )
                else:
                    data = jsonable_encoder(data)
                    return json.dumps(data).encode("utf-8")

            if is_sse_stream:
                # Generator endpoint: stream as Server-Sent Events
                gen = dependant.call(**solved_result.values)

                def _serialize_sse_item(item: Any) -> bytes:
                    if isinstance(item, ServerSentEvent):
                        # User controls the event structure.
                        # Serialize the data payload if present.
                        # For ServerSentEvent items we skip stream_item_field
                        # validation (the user may mix types intentionally).
                        if item.raw_data is not None:
                            data_str: str | None = item.raw_data
                        elif item.data is not None:
                            if hasattr(item.data, "model_dump_json"):
                                data_str = item.data.model_dump_json()
                            else:
                                data_str = json.dumps(jsonable_encoder(item.data))
                        else:
                            data_str = None
                        return format_sse_event(
                            data_str=data_str,
                            event=item.event,
                            id=item.id,
                            retry=item.retry,
                            comment=item.comment,
                        )
                    else:
                        # Plain object: validate + serialize via
                        # stream_item_field (if set) and wrap in data field
                        return format_sse_event(
                            data_str=_serialize_data(item).decode("utf-8")
                        )

                if _is_async_gen_callable(dependant.call):
                    sse_aiter: AsyncIterator[Any] = gen.__aiter__()
                else:
                    sse_aiter = iterate_in_threadpool(gen)

                @asynccontextmanager
                async def _sse_producer_cm() -> AsyncIterator[
                    ObjectReceiveStream[bytes]
                ]:
                    # Use a memory stream to decouple generator iteration
                    # from the keepalive timer. A producer task pulls items
                    # from the generator independently, so
                    # `anyio.fail_after` never wraps the generator's
                    # `__anext__` directly - avoiding CancelledError that
                    # would finalize the generator and also working for sync
                    # generators running in a thread pool.
                    #
                    # This context manager is entered on the request-scoped
                    # AsyncExitStack so its __aexit__ (which cancels the
                    # task group) is called by the exit stack after the
                    # streaming response completes — not by async generator
                    # finalization via GeneratorExit.
                    # Ref: https://peps.python.org/pep-0789/
                    send_stream, receive_stream = anyio.create_memory_object_stream[
                        bytes
                    ](max_buffer_size=1)

                    async def _producer() -> None:
                        async with send_stream:
                            async for raw_item in sse_aiter:
                                await send_stream.send(_serialize_sse_item(raw_item))

                    send_keepalive, receive_keepalive = (
                        anyio.create_memory_object_stream[bytes](max_buffer_size=1)
                    )

                    async def _keepalive_inserter() -> None:
                        """Read from the producer and forward to the output,
                        inserting keepalive comments on timeout."""
                        async with send_keepalive, receive_stream:
                            try:
                                while True:
                                    try:
                                        with anyio.fail_after(_PING_INTERVAL):
                                            data = await receive_stream.receive()
                                        await send_keepalive.send(data)
                                    except TimeoutError:
                                        await send_keepalive.send(KEEPALIVE_COMMENT)
                            except anyio.EndOfStream:
                                pass

                    async with anyio.create_task_group() as tg:
                        tg.start_soon(_producer)
                        tg.start_soon(_keepalive_inserter)
                        yield receive_keepalive
                        tg.cancel_scope.cancel()

                # Enter the SSE context manager on the request-scoped
                # exit stack. The stack outlives the streaming response,
                # so __aexit__ runs via proper structured teardown, not
                # via GeneratorExit thrown into an async generator.
                sse_receive_stream = await async_exit_stack.enter_async_context(
                    _sse_producer_cm()
                )
                # Ensure the receive stream is closed when the exit stack
                # unwinds, preventing ResourceWarning from __del__.
                async_exit_stack.push_async_callback(sse_receive_stream.aclose)

                async def _sse_with_checkpoints(
                    stream: ObjectReceiveStream[bytes],
                ) -> AsyncIterator[bytes]:
                    async for data in stream:
                        yield data
                        # Guarantee a checkpoint so cancellation can be
                        # delivered even when the producer is faster than
                        # the consumer and receive() never suspends.
                        await anyio.sleep(0)

                sse_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                    _sse_with_checkpoints(sse_receive_stream)
                )

                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = StreamingResponse(
                    sse_stream_content,
                    media_type="text/event-stream",
                    **response_args,
                )
                response.headers["Cache-Control"] = "no-cache"
                # For Nginx proxies to not buffer server sent events
                response.headers["X-Accel-Buffering"] = "no"
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif is_json_stream:
                # Generator endpoint: stream as JSONL
                gen = dependant.call(**solved_result.values)

                def _serialize_item(item: Any) -> bytes:
                    return _serialize_data(item) + b"\n"

                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_jsonl() -> AsyncIterator[bytes]:
                        async for item in gen:
                            yield _serialize_item(item)
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    jsonl_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                        _async_stream_jsonl()
                    )
                else:

                    def _sync_stream_jsonl() -> Iterator[bytes]:
                        for item in gen:  # ty: ignore[not-iterable]
                            yield _serialize_item(item)

                    jsonl_stream_content = _sync_stream_jsonl()

                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = StreamingResponse(
                    jsonl_stream_content,
                    media_type="application/jsonl",
                    **response_args,
                )
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif _is_async_gen_callable(dependant.call) or _is_gen_callable(
                dependant.call
            ):
                # Raw streaming with explicit response_class (e.g. StreamingResponse)
                gen = dependant.call(**solved_result.values)
                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_raw(
                        async_gen: AsyncIterator[Any],
                    ) -> AsyncIterator[Any]:
                        async for chunk in async_gen:
                            yield chunk
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    gen = _async_stream_raw(gen)
                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = actual_response_class(content=gen, **response_args)
                response.headers.raw.extend(solved_result.response.headers.raw)
            else:
                raw_response = await run_endpoint_function(
                    dependant=dependant,
                    values=solved_result.values,
                    is_coroutine=is_coroutine,
                )
                if isinstance(raw_response, Response):
                    if raw_response.background is None:
                        raw_response.background = solved_result.background_tasks
                    response = raw_response
                else:
                    response_args = _build_response_args(
                        status_code=status_code, solved_result=solved_result
                    )
                    # Use the fast path (dump_json) when no custom response
                    # class was set and a response field with a TypeAdapter
                    # exists. Serializes directly to JSON bytes via Pydantic's
                    # Rust core, skipping the intermediate Python dict +
                    # json.dumps() step.
                    use_dump_json = response_field is not None and isinstance(
                        response_class, DefaultPlaceholder
                    )
                    with _operation(name="serialization", function=dependant.call):
                        content = await serialize_response(
                            field=response_field,
                            response_content=raw_response,
                            include=response_model_include,
                            exclude=response_model_exclude,
                            by_alias=response_model_by_alias,
                            exclude_unset=response_model_exclude_unset,
                            exclude_defaults=response_model_exclude_defaults,
                            exclude_none=response_model_exclude_none,
                            is_coroutine=is_coroutine,
                            endpoint_ctx=endpoint_ctx,
                            dump_json=use_dump_json,
                        )
                    if use_dump_json:
                        response = Response(
                            content=content,
                            media_type="application/json",
                            **response_args,
                        )
                    else:
                        response = actual_response_class(content, **response_args)
                    if not is_body_allowed_for_status_code(response.status_code):
                        response.body = b""
                    response.headers.raw.extend(solved_result.response.headers.raw)
        if errors:
            validation_error = RequestValidationError(
                errors, body=body, endpoint_ctx=endpoint_ctx
            )
            _validation_failed(validation_error)
            raise validation_error

        # Return response
        assert response
        return response

    return app
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def get_request_handler(
    dependant: Dependant,
    body_field: ModelField | None = None,
    status_code: int | None = None,
    response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse),
    response_field: ModelField | None = None,
    response_model_include: IncEx | None = None,
    response_model_exclude: IncEx | None = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    dependency_overrides_provider: Any | None = None,
    embed_body_fields: bool = False,
    strict_content_type: bool | DefaultPlaceholder = Default(True),
    stream_item_field: ModelField | None = None,
    is_json_stream: bool = False,
) -> Callable[[Request], Coroutine[Any, Any, Response]]:
    assert dependant.call is not None, "dependant.call must be a function"
    is_coroutine = _is_coroutine_callable(dependant.call)
    is_body_form = body_field and isinstance(body_field.field_info, params.Form)
    if isinstance(response_class, DefaultPlaceholder):
        actual_response_class: type[Response] = response_class.value
    else:
        actual_response_class = response_class
    is_sse_stream = lenient_issubclass(actual_response_class, EventSourceResponse)
    if isinstance(strict_content_type, DefaultPlaceholder):
        actual_strict_content_type: bool = strict_content_type.value
    else:
        actual_strict_content_type = strict_content_type

    async def app(request: Request) -> Response:
        telemetry_data = get_telemetry_data()
        if telemetry_data is not None:
            telemetry_data.request = request
        response: Response | None = None
        file_stack = request.scope.get("fastapi_middleware_astack")
        assert isinstance(file_stack, AsyncExitStack), (
            "fastapi_middleware_astack not found in request scope"
        )

        # Extract endpoint context for error messages
        endpoint_ctx = (
            _extract_endpoint_context(dependant.call)
            if dependant.call
            else EndpointContext()
        )

        if dependant.path:
            # For mounted sub-apps, include the mount path prefix
            mount_path = request.scope.get("root_path", "").rstrip("/")
            endpoint_ctx["path"] = f"{request.method} {mount_path}{dependant.path}"

        # Read body and auto-close files
        try:
            body: Any = None
            if body_field:
                if is_body_form:
                    body = await request.form()
                    file_stack.push_async_callback(body.close)
                else:
                    body_bytes = await request.body()
                    if body_bytes:
                        json_body: Any = Undefined
                        content_type_value = request.headers.get("content-type")
                        if not content_type_value:
                            if not actual_strict_content_type:
                                json_body = await request.json()
                        else:
                            message = email.message.Message()
                            message["content-type"] = content_type_value
                            if message.get_content_maintype() == "application":
                                subtype = message.get_content_subtype()
                                if subtype == "json" or subtype.endswith("+json"):
                                    json_body = await request.json()
                        if json_body != Undefined:
                            body = json_body
                        else:
                            body = body_bytes
        except json.JSONDecodeError as e:
            validation_error = RequestValidationError(
                [
                    {
                        "type": "json_invalid",
                        "loc": ("body", e.pos),
                        "msg": "JSON decode error",
                        "input": {},
                        "ctx": {"error": e.msg},
                    }
                ],
                body=e.doc,
                endpoint_ctx=endpoint_ctx,
            )
            _validation_failed(validation_error)
            raise validation_error from e
        except HTTPException:
            # If a middleware raises an HTTPException, it should be raised again
            raise
        except Exception as e:
            http_error = HTTPException(
                status_code=400, detail="There was an error parsing the body"
            )
            raise http_error from e

        if telemetry_data is not None:
            telemetry_data.body = body

        # Solve dependencies and run path operation function, auto-closing dependencies
        errors: list[Any] = []
        async_exit_stack = request.scope.get("fastapi_inner_astack")
        assert isinstance(async_exit_stack, AsyncExitStack), (
            "fastapi_inner_astack not found in request scope"
        )
        with _operation(name="dependencies", function=dependant.call):
            solved_result = await solve_dependencies(
                request=request,
                dependant=dependant,
                body=cast(dict[str, Any] | FormData | bytes | None, body),
                dependency_overrides_provider=dependency_overrides_provider,
                async_exit_stack=async_exit_stack,
                embed_body_fields=embed_body_fields,
            )
            if telemetry_data is not None:
                telemetry_data.values = solved_result.values
                telemetry_data.errors = solved_result.errors
        errors = solved_result.errors
        assert dependant.call  # For types
        if not errors:
            # Shared serializer for stream items (JSONL and SSE).
            # Validates against stream_item_field when set, then
            # serializes to JSON bytes.
            def _serialize_data(data: Any) -> bytes:
                if stream_item_field:
                    value, errors_ = stream_item_field.validate(
                        data, {}, loc=("response",)
                    )
                    if errors_:
                        ctx = endpoint_ctx or EndpointContext()
                        raise ResponseValidationError(
                            errors=errors_,
                            body=data,
                            endpoint_ctx=ctx,
                        )
                    return stream_item_field.serialize_json(
                        value,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                    )
                else:
                    data = jsonable_encoder(data)
                    return json.dumps(_normalize_non_finite_floats(data)).encode(
                        "utf-8"
                    )

            if is_sse_stream:
                # Generator endpoint: stream as Server-Sent Events
                gen = dependant.call(**solved_result.values)

                def _serialize_sse_item(item: Any) -> bytes:
                    if isinstance(item, ServerSentEvent):
                        # User controls the event structure.
                        # Serialize the data payload if present.
                        # For ServerSentEvent items we skip stream_item_field
                        # validation (the user may mix types intentionally).
                        if item.raw_data is not None:
                            data_str: str | None = item.raw_data
                        elif item.data is not None:
                            if hasattr(item.data, "model_dump_json"):
                                data_str = item.data.model_dump_json()
                            else:
                                data_str = json.dumps(
                                    _normalize_non_finite_floats(
                                        jsonable_encoder(item.data)
                                    )
                                )
                        else:
                            data_str = None
                        return format_sse_event(
                            data_str=data_str,
                            event=item.event,
                            id=item.id,
                            retry=item.retry,
                            comment=item.comment,
                        )
                    else:
                        # Plain object: validate + serialize via
                        # stream_item_field (if set) and wrap in data field
                        return format_sse_event(
                            data_str=_serialize_data(item).decode("utf-8")
                        )

                if _is_async_gen_callable(dependant.call):
                    sse_aiter: AsyncIterator[Any] = gen.__aiter__()
                else:
                    sse_aiter = iterate_in_threadpool(gen)

                @asynccontextmanager
                async def _sse_producer_cm() -> AsyncIterator[
                    ObjectReceiveStream[bytes]
                ]:
                    # Use a memory stream to decouple generator iteration
                    # from the keepalive timer. A producer task pulls items
                    # from the generator independently, so
                    # `anyio.fail_after` never wraps the generator's
                    # `__anext__` directly - avoiding CancelledError that
                    # would finalize the generator and also working for sync
                    # generators running in a thread pool.
                    #
                    # This context manager is entered on the request-scoped
                    # AsyncExitStack so its __aexit__ (which cancels the
                    # task group) is called by the exit stack after the
                    # streaming response completes — not by async generator
                    # finalization via GeneratorExit.
                    # Ref: https://peps.python.org/pep-0789/
                    send_stream, receive_stream = anyio.create_memory_object_stream[
                        bytes
                    ](max_buffer_size=1)

                    async def _producer() -> None:
                        async with send_stream:
                            async for raw_item in sse_aiter:
                                await send_stream.send(_serialize_sse_item(raw_item))

                    send_keepalive, receive_keepalive = (
                        anyio.create_memory_object_stream[bytes](max_buffer_size=1)
                    )

                    async def _keepalive_inserter() -> None:
                        """Read from the producer and forward to the output,
                        inserting keepalive comments on timeout."""
                        async with send_keepalive, receive_stream:
                            try:
                                while True:
                                    try:
                                        with anyio.fail_after(_PING_INTERVAL):
                                            data = await receive_stream.receive()
                                        await send_keepalive.send(data)
                                    except TimeoutError:
                                        await send_keepalive.send(KEEPALIVE_COMMENT)
                            except anyio.EndOfStream:
                                pass

                    async with anyio.create_task_group() as tg:
                        tg.start_soon(_producer)
                        tg.start_soon(_keepalive_inserter)
                        yield receive_keepalive
                        tg.cancel_scope.cancel()

                # Enter the SSE context manager on the request-scoped
                # exit stack. The stack outlives the streaming response,
                # so __aexit__ runs via proper structured teardown, not
                # via GeneratorExit thrown into an async generator.
                sse_receive_stream = await async_exit_stack.enter_async_context(
                    _sse_producer_cm()
                )
                # Ensure the receive stream is closed when the exit stack
                # unwinds, preventing ResourceWarning from __del__.
                async_exit_stack.push_async_callback(sse_receive_stream.aclose)

                async def _sse_with_checkpoints(
                    stream: ObjectReceiveStream[bytes],
                ) -> AsyncIterator[bytes]:
                    async for data in stream:
                        yield data
                        # Guarantee a checkpoint so cancellation can be
                        # delivered even when the producer is faster than
                        # the consumer and receive() never suspends.
                        await anyio.sleep(0)

                sse_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                    _sse_with_checkpoints(sse_receive_stream)
                )

                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = StreamingResponse(
                    sse_stream_content,
                    media_type="text/event-stream",
                    **response_args,
                )
                response.headers["Cache-Control"] = "no-cache"
                # For Nginx proxies to not buffer server sent events
                response.headers["X-Accel-Buffering"] = "no"
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif is_json_stream:
                # Generator endpoint: stream as JSONL
                gen = dependant.call(**solved_result.values)

                def _serialize_item(item: Any) -> bytes:
                    return _serialize_data(item) + b"\n"

                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_jsonl() -> AsyncIterator[bytes]:
                        async for item in gen:
                            yield _serialize_item(item)
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    jsonl_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                        _async_stream_jsonl()
                    )
                else:

                    def _sync_stream_jsonl() -> Iterator[bytes]:
                        for item in gen:  # ty: ignore[not-iterable]
                            yield _serialize_item(item)

                    jsonl_stream_content = _sync_stream_jsonl()

                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = StreamingResponse(
                    jsonl_stream_content,
                    media_type="application/jsonl",
                    **response_args,
                )
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif _is_async_gen_callable(dependant.call) or _is_gen_callable(
                dependant.call
            ):
                # Raw streaming with explicit response_class (e.g. StreamingResponse)
                gen = dependant.call(**solved_result.values)
                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_raw(
                        async_gen: AsyncIterator[Any],
                    ) -> AsyncIterator[Any]:
                        async for chunk in async_gen:
                            yield chunk
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    gen = _async_stream_raw(gen)
                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = actual_response_class(content=gen, **response_args)
                response.headers.raw.extend(solved_result.response.headers.raw)
            else:
                raw_response = await run_endpoint_function(
                    dependant=dependant,
                    values=solved_result.values,
                    is_coroutine=is_coroutine,
                )
                if isinstance(raw_response, Response):
                    if raw_response.background is None:
                        raw_response.background = solved_result.background_tasks
                    response = raw_response
                else:
                    response_args = _build_response_args(
                        status_code=status_code, solved_result=solved_result
                    )
                    # Use the fast path (dump_json) when no custom response
                    # class was set and a response field with a TypeAdapter
                    # exists. Serializes directly to JSON bytes via Pydantic's
                    # Rust core, skipping the intermediate Python dict +
                    # json.dumps() step.
                    use_dump_json = response_field is not None and isinstance(
                        response_class, DefaultPlaceholder
                    )
                    with _operation(name="serialization", function=dependant.call):
                        content = await serialize_response(
                            field=response_field,
                            response_content=raw_response,
                            include=response_model_include,
                            exclude=response_model_exclude,
                            by_alias=response_model_by_alias,
                            exclude_unset=response_model_exclude_unset,
                            exclude_defaults=response_model_exclude_defaults,
                            exclude_none=response_model_exclude_none,
                            is_coroutine=is_coroutine,
                            endpoint_ctx=endpoint_ctx,
                            dump_json=use_dump_json,
                        )
                    if use_dump_json:
                        response = Response(
                            content=content,
                            media_type="application/json",
                            **response_args,
                        )
                    else:
                        response = actual_response_class(content, **response_args)
                    if not is_body_allowed_for_status_code(response.status_code):
                        response.body = b""
                    response.headers.raw.extend(solved_result.response.headers.raw)
        if errors:
            validation_error = RequestValidationError(
                errors, body=body, endpoint_ctx=endpoint_ctx
            )
            _validation_failed(validation_error)
            raise validation_error

        # Return response
        assert response
        return response

    return app
```

### 🔹 函式: `_serialize_sse_item()`
- **變更前簽章 (Before)**: `def _serialize_sse_item(item: Any) -> bytes` (L545~L572)
- **變更後簽章 (After)**: `def _serialize_sse_item(item: Any) -> bytes` (L559~L590)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _serialize_sse_item(item: Any) -> bytes:
                    if isinstance(item, ServerSentEvent):
                        # User controls the event structure.
                        # Serialize the data payload if present.
                        # For ServerSentEvent items we skip stream_item_field
                        # validation (the user may mix types intentionally).
                        if item.raw_data is not None:
                            data_str: str | None = item.raw_data
                        elif item.data is not None:
                            if hasattr(item.data, "model_dump_json"):
                                data_str = item.data.model_dump_json()
                            else:
                                data_str = json.dumps(jsonable_encoder(item.data))
                        else:
                            data_str = None
                        return format_sse_event(
                            data_str=data_str,
                            event=item.event,
                            id=item.id,
                            retry=item.retry,
                            comment=item.comment,
                        )
                    else:
                        # Plain object: validate + serialize via
                        # stream_item_field (if set) and wrap in data field
                        return format_sse_event(
                            data_str=_serialize_data(item).decode("utf-8")
                        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _serialize_sse_item(item: Any) -> bytes:
                    if isinstance(item, ServerSentEvent):
                        # User controls the event structure.
                        # Serialize the data payload if present.
                        # For ServerSentEvent items we skip stream_item_field
                        # validation (the user may mix types intentionally).
                        if item.raw_data is not None:
                            data_str: str | None = item.raw_data
                        elif item.data is not None:
                            if hasattr(item.data, "model_dump_json"):
                                data_str = item.data.model_dump_json()
                            else:
                                data_str = json.dumps(
                                    _normalize_non_finite_floats(
                                        jsonable_encoder(item.data)
                                    )
                                )
                        else:
                            data_str = None
                        return format_sse_event(
                            data_str=data_str,
                            event=item.event,
                            id=item.id,
                            retry=item.retry,
                            comment=item.comment,
                        )
                    else:
                        # Plain object: validate + serialize via
                        # stream_item_field (if set) and wrap in data field
                        return format_sse_event(
                            data_str=_serialize_data(item).decode("utf-8")
                        )
```

### 🔹 函式: `_serialize_data()`
- **變更前簽章 (Before)**: `def _serialize_data(data: Any) -> bytes` (L516~L539)
- **變更後簽章 (After)**: `def _serialize_data(data: Any) -> bytes` (L528~L553)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _serialize_data(data: Any) -> bytes:
                if stream_item_field:
                    value, errors_ = stream_item_field.validate(
                        data, {}, loc=("response",)
                    )
                    if errors_:
                        ctx = endpoint_ctx or EndpointContext()
                        raise ResponseValidationError(
                            errors=errors_,
                            body=data,
                            endpoint_ctx=ctx,
                        )
                    return stream_item_field.serialize_json(
                        value,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                    )
                else:
                    data = jsonable_encoder(data)
                    return json.dumps(data).encode("utf-8")
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _serialize_data(data: Any) -> bytes:
                if stream_item_field:
                    value, errors_ = stream_item_field.validate(
                        data, {}, loc=("response",)
                    )
                    if errors_:
                        ctx = endpoint_ctx or EndpointContext()
                        raise ResponseValidationError(
                            errors=errors_,
                            body=data,
                            endpoint_ctx=ctx,
                        )
                    return stream_item_field.serialize_json(
                        value,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                    )
                else:
                    data = jsonable_encoder(data)
                    return json.dumps(_normalize_non_finite_floats(data)).encode(
                        "utf-8"
                    )
```


---

### 🔹 Commit #10: `d0282a38`
- **完整 Hash**: `d0282a388b3875dfdfd69813693608676006254f`
- **說明 (Ground Truth)**: 🐛 Fix blocking frontend fallback file checks (#16503)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/routing.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:285, E:432, A:0) ➔ After(N:285, E:432, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 1, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `_FrontendStaticFiles._fallback_file_exists` ──[CALLS]──> `run_in_threadpool (External/Unresolved)`
  • - [移除呼叫邊] `_FrontendStaticFiles._fallback_file_exists` ──[CALLS]──> `lookup_path (External/Unresolved)`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'app' 被深鎖在內部閉包 (scope:request_response@after/fastapi/routing.py:L128)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_FrontendStaticFiles._fallback_file_exists()`
- **變更前簽章 (Before)**: `def _fallback_file_exists(self, fallback: str) -> bool` (L2046~L2048)
- **變更後簽章 (After)**: `async def _fallback_file_exists(self, fallback: str) -> bool` (L2049~L2051)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _fallback_file_exists(self, fallback: str) -> bool:
        _, stat_result = self.lookup_path(fallback)
        return stat_result is not None and stat.S_ISREG(stat_result.st_mode)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def _fallback_file_exists(self, fallback: str) -> bool:
        _, stat_result = await run_in_threadpool(self.lookup_path, fallback)
        return stat_result is not None and stat.S_ISREG(stat_result.st_mode)
```

### 🔹 函式: `_FrontendStaticFiles.get_response()`
- **變更前簽章 (Before)**: `async def get_response(self, path: str, scope: Scope) -> Response` (L1991~L2017)
- **變更後簽章 (After)**: `async def get_response(self, path: str, scope: Scope) -> Response` (L1991~L2020)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def get_response(self, path: str, scope: Scope) -> Response:
        if scope["method"] not in ("GET", "HEAD"):
            if await self._lookup_static_resource(path) is not None:
                raise HTTPException(status_code=405)
            raise HTTPException(status_code=404)

        static_resource = await self._lookup_static_resource(path)
        if static_resource is not None:
            full_path, stat_result, is_directory_index = static_resource
            if is_directory_index and not scope["path"].endswith("/"):
                url = URL(scope=scope)
                url = url.replace(path=url.path + "/")
                return RedirectResponse(url=url)
            return self.file_response(full_path, stat_result, scope)

        if self.fallback == "404.html" or (
            self.fallback == "auto" and self._fallback_file_exists("404.html")
        ):
            return await self._fallback_response("404.html", scope, status_code=404)

        if (
            self.fallback == "index.html"
            or (self.fallback == "auto" and self._fallback_file_exists("index.html"))
        ) and _is_frontend_navigation_request(scope):
            return await self._fallback_response("index.html", scope, status_code=200)

        raise HTTPException(status_code=404)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def get_response(self, path: str, scope: Scope) -> Response:
        if scope["method"] not in ("GET", "HEAD"):
            if await self._lookup_static_resource(path) is not None:
                raise HTTPException(status_code=405)
            raise HTTPException(status_code=404)

        static_resource = await self._lookup_static_resource(path)
        if static_resource is not None:
            full_path, stat_result, is_directory_index = static_resource
            if is_directory_index and not scope["path"].endswith("/"):
                url = URL(scope=scope)
                url = url.replace(path=url.path + "/")
                return RedirectResponse(url=url)
            return self.file_response(full_path, stat_result, scope)

        if self.fallback == "404.html" or (
            self.fallback == "auto" and await self._fallback_file_exists("404.html")
        ):
            return await self._fallback_response("404.html", scope, status_code=404)

        if (
            self.fallback == "index.html"
            or (
                self.fallback == "auto"
                and await self._fallback_file_exists("index.html")
            )
        ) and _is_frontend_navigation_request(scope):
            return await self._fallback_response("index.html", scope, status_code=200)

        raise HTTPException(status_code=404)
```


---

### 🔹 Commit #11: `5e6a1eec`
- **完整 Hash**: `5e6a1eec1fbc0acbe0a813e981cfd69539051b52`
- **說明 (Ground Truth)**: 🐛 Fix included route metadata in `iter_route_contexts()` (#16484)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/routing.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:285, E:432, A:0) ➔ After(N:285, E:432, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'app' 被深鎖在內部閉包 (scope:request_response@after/fastapi/routing.py:L128)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RouteContext._effective_route()`
- **變更前簽章 (Before)**: `def _effective_route(self) -> BaseRoute | _EffectiveRouteContext` (L1593~L1596)
- **變更後簽章 (After)**: `def _effective_route(self) -> BaseRoute | _EffectiveRouteContext` (L1593~L1598)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _effective_route(self) -> BaseRoute | _EffectiveRouteContext:
        if self._route_context is not None:
            return self._route_context
        return self.route
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _effective_route(self) -> BaseRoute | _EffectiveRouteContext:
        if self._route_context is not None:
            if self._route_context.starlette_route is not None:
                return self._route_context.starlette_route
            return self._route_context
        return self.route
```


---

### 🔹 Commit #12: `4e31a07b`
- **完整 Hash**: `4e31a07bafd08f247f39ab1e9144ba2a62395757`
- **說明 (Ground Truth)**: 🐛 Isolate FastAPI telemetry for excluded requests (#16470)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/telemetry/_asgi.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:65, E:68, A:0) ➔ After(N:65, E:68, A:0)
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

### 🔹 函式: `NativeTelemetry.__call__()`
- **變更前簽章 (Before)**: `async def __call__( self, *, app: ASGIApp, scope: Scope, receive: Receive, send: Send, legacy_otel: bool = False, ) -> None` (L228~L452)
- **變更後簽章 (After)**: `async def __call__( self, *, app: ASGIApp, scope: Scope, receive: Receive, send: Send, legacy_otel: bool = False, ) -> None` (L228~L457)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def __call__(
        self,
        *,
        app: ASGIApp,
        scope: Scope,
        receive: Receive,
        send: Send,
        legacy_otel: bool = False,
    ) -> None:
        config = self.config
        if config["exclude"] is not None and config["exclude"](scope):
            # Keep mounted FastAPI apps from observing this excluded request.
            scope["fastapi.telemetry"] = None
            try:
                await app(scope, receive, send)
            finally:
                scope.pop("fastapi.telemetry", None)
            return
        tracing = config["tracing"] and not legacy_otel
        logging = config["logs"] and not legacy_otel
        if logging:
            logger_provider = config["logger_provider"] or _logs.get_logger_provider()
            logging = not (
                (config["logger_provider"] is None and _unconfigured(logger_provider))
                or isinstance(logger_provider, _logs.NoOpLoggerProvider)
            )
        is_websocket = scope["type"] == "websocket"
        metering = config["metrics"] and not legacy_otel and not is_websocket
        if tracing:
            provider = config["tracer_provider"] or trace.get_tracer_provider()
            tracing = not (
                (config["tracer_provider"] is None and _unconfigured(provider))
                or isinstance(provider, trace.NoOpTracerProvider)
            )
        if metering:
            meter_provider = config["meter_provider"] or metrics.get_meter_provider()
            metering = not (
                (config["meter_provider"] is None and _unconfigured(meter_provider))
                or isinstance(meter_provider, metrics.NoOpMeterProvider)
            )
        if not tracing and not metering and not logging:
            await app(scope, receive, send)
            return
        original_method = scope.get("method", "")
        method = original_method if original_method in self._known_methods else "_OTHER"
        span_method = "WS" if is_websocket else "HTTP" if method == "_OTHER" else method
        attributes: dict[str, Any] = {
            "url.scheme": scope.get("scheme", "ws" if is_websocket else "http"),
        }
        if is_websocket:
            attributes["network.protocol.name"] = "websocket"
        else:
            attributes["http.request.method"] = method
            if scope.get("http_version"):
                attributes["network.protocol.version"] = scope["http_version"]
        duration, active = self._instruments() if metering else (None, None)
        active_attributes = {
            k: v for k, v in attributes.items() if k != "network.protocol.version"
        }
        if active is not None:
            active.add(1, active_attributes)
        started = perf_counter()
        span = None
        tracer = None
        parent_token = None
        if tracing:
            parent = propagate.extract(Headers(scope=scope), getter=_HEADERS_GETTER)
            parent_token = otel_context.attach(parent)
            tracer = self._get_tracer(provider=provider)
            span_attributes = {**attributes, **_server_attributes(scope)}
            if not is_websocket:
                span_attributes["url.path"] = scope["path"]
                if scope.get("query_string"):
                    span_attributes["url.query"] = urlencode(
                        [
                            (
                                key,
                                "REDACTED"
                                if key in _SENSITIVE_QUERY_PARAMETERS
                                else value,
                            )
                            for key, value in parse_qsl(
                                scope["query_string"].decode("latin-1"),
                                keep_blank_values=True,
                            )
                        ]
                    )
                if original_method != method:
                    span_attributes["http.request.method_original"] = original_method
            span = tracer.start_span(
                span_method,
                context=parent,
                kind=SpanKind.SERVER,
                attributes=span_attributes,
            )
        request_telemetry = _RequestTelemetry(
            span=span,
            span_method=span_method,
            tracer=tracer if config["operation_spans"] else None,
            logger=_logs.get_logger(
                "fastapi",
                __version__,
                config["logger_provider"],
                schema_url=_SCHEMA_URL,
            )
            if logging
            else None,
            _mount_prefix=scope.get("app_root_path", scope.get("root_path", "")).rstrip(
                "/"
            ),
        )
        scope["fastapi.telemetry"] = request_telemetry
        token = otel_context.attach(
            otel_context.set_value(_REQUEST_TELEMETRY_KEY, request_telemetry)
        )
        finished = False
        trailers = False
        disconnected = False

        def finish(error: BaseException | None = None) -> None:
            nonlocal finished
            if finished:
                return
            finished = True
            if request_telemetry.route is not None:
                attributes["http.route"] = request_telemetry.route
            if request_telemetry.status_code is not None:
                attributes["http.response.status_code"] = request_telemetry.status_code
            failed = (
                error is not None
                or not is_websocket
                and (
                    request_telemetry.status_code is None
                    or request_telemetry.status_code >= 500
                )
            )
            if failed:
                errors = request_telemetry._exceptions
                failure = error or (errors[-1] if errors else None)
                attributes["error.type"] = (
                    _exception_type(failure)
                    if failure
                    else str(request_telemetry.status_code or "incomplete_response")
                )
            if span is not None:
                span.set_attributes(attributes)
                if failed:
                    span.set_status(StatusCode.ERROR)
            # Record while the span is current, so exemplars can correlate it.
            if duration is not None:
                duration.record(max(0, perf_counter() - started), attributes)
            if active is not None:
                active.add(-1, active_attributes)
            if span is not None:
                span.end()

        async def wrapped_send(message: Message) -> None:
            nonlocal trailers
            if message["type"] == "http.response.start":
                request_telemetry.status_code = message["status"]
                trailers = message.get("trailers", False)
            await send(message)
            if (
                (
                    message["type"] == "http.response.body"
                    and not message.get("more_body", False)
                    and not trailers
                )
                or (
                    message["type"] == "http.response.trailers"
                    and not message.get("more_trailers", False)
                )
                or message["type"] == "http.response.pathsend"
            ):
                finish()

        async def wrapped_receive() -> Message:
            nonlocal disconnected
            message = await receive()
            if message["type"] == "http.disconnect":
                disconnected = True
            return message

        context = (
            trace.use_span(
                span,
                end_on_exit=False,
                record_exception=False,
                set_status_on_exception=False,
            )
            if span is not None
            else nullcontext()
        )
        try:
            with context:
                try:
                    await app(
                        scope,
                        receive if is_websocket else wrapped_receive,
                        send if is_websocket else wrapped_send,
                    )
                except BaseException as exc:
                    _exception(scope=scope, exc=exc)
                    finish(
                        None
                        if is_websocket and _normal_websocket_disconnect(exc)
                        else exc
                    )
                    raise
                finally:
                    if not finished:
                        finish(
                            None
                            if is_websocket
                            else ConnectionError("Client disconnected")
                            if disconnected
                            else RuntimeError("Incomplete ASGI response")
                        )
        finally:
            request_telemetry.data = None
            request_telemetry._exceptions.clear()
            otel_context.detach(token)
            scope.pop("fastapi.telemetry", None)
            if parent_token is not None:
                otel_context.detach(parent_token)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def __call__(
        self,
        *,
        app: ASGIApp,
        scope: Scope,
        receive: Receive,
        send: Send,
        legacy_otel: bool = False,
    ) -> None:
        config = self.config
        if config["exclude"] is not None and config["exclude"](scope):
            # Keep mounted FastAPI apps from observing this excluded request.
            scope["fastapi.telemetry"] = None
            # An in-process request can inherit another request's telemetry.
            token = otel_context.attach(
                otel_context.set_value(_REQUEST_TELEMETRY_KEY, None)
            )
            try:
                await app(scope, receive, send)
            finally:
                otel_context.detach(token)
                scope.pop("fastapi.telemetry", None)
            return
        tracing = config["tracing"] and not legacy_otel
        logging = config["logs"] and not legacy_otel
        if logging:
            logger_provider = config["logger_provider"] or _logs.get_logger_provider()
            logging = not (
                (config["logger_provider"] is None and _unconfigured(logger_provider))
                or isinstance(logger_provider, _logs.NoOpLoggerProvider)
            )
        is_websocket = scope["type"] == "websocket"
        metering = config["metrics"] and not legacy_otel and not is_websocket
        if tracing:
            provider = config["tracer_provider"] or trace.get_tracer_provider()
            tracing = not (
                (config["tracer_provider"] is None and _unconfigured(provider))
                or isinstance(provider, trace.NoOpTracerProvider)
            )
        if metering:
            meter_provider = config["meter_provider"] or metrics.get_meter_provider()
            metering = not (
                (config["meter_provider"] is None and _unconfigured(meter_provider))
                or isinstance(meter_provider, metrics.NoOpMeterProvider)
            )
        if not tracing and not metering and not logging:
            await app(scope, receive, send)
            return
        original_method = scope.get("method", "")
        method = original_method if original_method in self._known_methods else "_OTHER"
        span_method = "WS" if is_websocket else "HTTP" if method == "_OTHER" else method
        attributes: dict[str, Any] = {
            "url.scheme": scope.get("scheme", "ws" if is_websocket else "http"),
        }
        if is_websocket:
            attributes["network.protocol.name"] = "websocket"
        else:
            attributes["http.request.method"] = method
            if scope.get("http_version"):
                attributes["network.protocol.version"] = scope["http_version"]
        duration, active = self._instruments() if metering else (None, None)
        active_attributes = {
            k: v for k, v in attributes.items() if k != "network.protocol.version"
        }
        if active is not None:
            active.add(1, active_attributes)
        started = perf_counter()
        span = None
        tracer = None
        parent_token = None
        if tracing:
            parent = propagate.extract(Headers(scope=scope), getter=_HEADERS_GETTER)
            parent_token = otel_context.attach(parent)
            tracer = self._get_tracer(provider=provider)
            span_attributes = {**attributes, **_server_attributes(scope)}
            if not is_websocket:
                span_attributes["url.path"] = scope["path"]
                if scope.get("query_string"):
                    span_attributes["url.query"] = urlencode(
                        [
                            (
                                key,
                                "REDACTED"
                                if key in _SENSITIVE_QUERY_PARAMETERS
                                else value,
                            )
                            for key, value in parse_qsl(
                                scope["query_string"].decode("latin-1"),
                                keep_blank_values=True,
                            )
                        ]
                    )
                if original_method != method:
                    span_attributes["http.request.method_original"] = original_method
            span = tracer.start_span(
                span_method,
                context=parent,
                kind=SpanKind.SERVER,
                attributes=span_attributes,
            )
        request_telemetry = _RequestTelemetry(
            span=span,
            span_method=span_method,
            tracer=tracer if config["operation_spans"] else None,
            logger=_logs.get_logger(
                "fastapi",
                __version__,
                config["logger_provider"],
                schema_url=_SCHEMA_URL,
            )
            if logging
            else None,
            _mount_prefix=scope.get("app_root_path", scope.get("root_path", "")).rstrip(
                "/"
            ),
        )
        scope["fastapi.telemetry"] = request_telemetry
        token = otel_context.attach(
            otel_context.set_value(_REQUEST_TELEMETRY_KEY, request_telemetry)
        )
        finished = False
        trailers = False
        disconnected = False

        def finish(error: BaseException | None = None) -> None:
            nonlocal finished
            if finished:
                return
            finished = True
            if request_telemetry.route is not None:
                attributes["http.route"] = request_telemetry.route
            if request_telemetry.status_code is not None:
                attributes["http.response.status_code"] = request_telemetry.status_code
            failed = (
                error is not None
                or not is_websocket
                and (
                    request_telemetry.status_code is None
                    or request_telemetry.status_code >= 500
                )
            )
            if failed:
                errors = request_telemetry._exceptions
                failure = error or (errors[-1] if errors else None)
                attributes["error.type"] = (
                    _exception_type(failure)
                    if failure
                    else str(request_telemetry.status_code or "incomplete_response")
                )
            if span is not None:
                span.set_attributes(attributes)
                if failed:
                    span.set_status(StatusCode.ERROR)
            # Record while the span is current, so exemplars can correlate it.
            if duration is not None:
                duration.record(max(0, perf_counter() - started), attributes)
            if active is not None:
                active.add(-1, active_attributes)
            if span is not None:
                span.end()

        async def wrapped_send(message: Message) -> None:
            nonlocal trailers
            if message["type"] == "http.response.start":
                request_telemetry.status_code = message["status"]
                trailers = message.get("trailers", False)
            await send(message)
            if (
                (
                    message["type"] == "http.response.body"
                    and not message.get("more_body", False)
                    and not trailers
                )
                or (
                    message["type"] == "http.response.trailers"
                    and not message.get("more_trailers", False)
                )
                or message["type"] == "http.response.pathsend"
            ):
                finish()

        async def wrapped_receive() -> Message:
            nonlocal disconnected
            message = await receive()
            if message["type"] == "http.disconnect":
                disconnected = True
            return message

        context = (
            trace.use_span(
                span,
                end_on_exit=False,
                record_exception=False,
                set_status_on_exception=False,
            )
            if span is not None
            else nullcontext()
        )
        try:
            with context:
                try:
                    await app(
                        scope,
                        receive if is_websocket else wrapped_receive,
                        send if is_websocket else wrapped_send,
                    )
                except BaseException as exc:
                    _exception(scope=scope, exc=exc)
                    finish(
                        None
                        if is_websocket and _normal_websocket_disconnect(exc)
                        else exc
                    )
                    raise
                finally:
                    if not finished:
                        finish(
                            None
                            if is_websocket
                            else ConnectionError("Client disconnected")
                            if disconnected
                            else RuntimeError("Incomplete ASGI response")
                        )
        finally:
            request_telemetry.data = None
            request_telemetry._exceptions.clear()
            otel_context.detach(token)
            scope.pop("fastapi.telemetry", None)
            if parent_token is not None:
                otel_context.detach(parent_token)
```


---

### 🔹 Commit #13: `6eae2f34`
- **完整 Hash**: `6eae2f3456c889ad791de38dd45c14e17de775d3`
- **說明 (Ground Truth)**: 🐛 Cache OpenTelemetry tracers to preserve warning deduplication (#16468)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/telemetry/_asgi.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:64, E:67, A:0) ➔ After(N:65, E:68, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 2, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `NativeTelemetry._get_tracer` (FUNCTION_DEF)
  • + [新增呼叫邊] `NativeTelemetry._get_tracer` ──[CALLS]──> `get_tracer (External/Unresolved)`
  • + [新增呼叫邊] `NativeTelemetry.__call__` ──[CALLS]──> `NativeTelemetry._get_tracer`
  • - [移除呼叫邊] `NativeTelemetry.__call__` ──[CALLS]──> `get_tracer (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `NativeTelemetry.__call__()`
- **變更前簽章 (Before)**: `async def __call__( self, *, app: ASGIApp, scope: Scope, receive: Receive, send: Send, legacy_otel: bool = False, ) -> None` (L217~L446)
- **變更後簽章 (After)**: `async def __call__( self, *, app: ASGIApp, scope: Scope, receive: Receive, send: Send, legacy_otel: bool = False, ) -> None` (L228~L452)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def __call__(
        self,
        *,
        app: ASGIApp,
        scope: Scope,
        receive: Receive,
        send: Send,
        legacy_otel: bool = False,
    ) -> None:
        config = self.config
        if config["exclude"] is not None and config["exclude"](scope):
            # Keep mounted FastAPI apps from observing this excluded request.
            scope["fastapi.telemetry"] = None
            try:
                await app(scope, receive, send)
            finally:
                scope.pop("fastapi.telemetry", None)
            return
        tracing = config["tracing"] and not legacy_otel
        logging = config["logs"] and not legacy_otel
        if logging:
            logger_provider = config["logger_provider"] or _logs.get_logger_provider()
            logging = not (
                (config["logger_provider"] is None and _unconfigured(logger_provider))
                or isinstance(logger_provider, _logs.NoOpLoggerProvider)
            )
        is_websocket = scope["type"] == "websocket"
        metering = config["metrics"] and not legacy_otel and not is_websocket
        if tracing:
            provider = config["tracer_provider"] or trace.get_tracer_provider()
            tracing = not (
                (config["tracer_provider"] is None and _unconfigured(provider))
                or isinstance(provider, trace.NoOpTracerProvider)
            )
        if metering:
            meter_provider = config["meter_provider"] or metrics.get_meter_provider()
            metering = not (
                (config["meter_provider"] is None and _unconfigured(meter_provider))
                or isinstance(meter_provider, metrics.NoOpMeterProvider)
            )
        if not tracing and not metering and not logging:
            await app(scope, receive, send)
            return
        original_method = scope.get("method", "")
        method = original_method if original_method in self._known_methods else "_OTHER"
        span_method = "WS" if is_websocket else "HTTP" if method == "_OTHER" else method
        attributes: dict[str, Any] = {
            "url.scheme": scope.get("scheme", "ws" if is_websocket else "http"),
        }
        if is_websocket:
            attributes["network.protocol.name"] = "websocket"
        else:
            attributes["http.request.method"] = method
            if scope.get("http_version"):
                attributes["network.protocol.version"] = scope["http_version"]
        duration, active = self._instruments() if metering else (None, None)
        active_attributes = {
            k: v for k, v in attributes.items() if k != "network.protocol.version"
        }
        if active is not None:
            active.add(1, active_attributes)
        started = perf_counter()
        span = None
        tracer = None
        parent_token = None
        if tracing:
            parent = propagate.extract(Headers(scope=scope), getter=_HEADERS_GETTER)
            parent_token = otel_context.attach(parent)
            tracer = trace.get_tracer(
                "fastapi",
                __version__,
                config["tracer_provider"],
                schema_url=_SCHEMA_URL,
            )
            span_attributes = {**attributes, **_server_attributes(scope)}
            if not is_websocket:
                span_attributes["url.path"] = scope["path"]
                if scope.get("query_string"):
                    span_attributes["url.query"] = urlencode(
                        [
                            (
                                key,
                                "REDACTED"
                                if key in _SENSITIVE_QUERY_PARAMETERS
                                else value,
                            )
                            for key, value in parse_qsl(
                                scope["query_string"].decode("latin-1"),
                                keep_blank_values=True,
                            )
                        ]
                    )
                if original_method != method:
                    span_attributes["http.request.method_original"] = original_method
            span = tracer.start_span(
                span_method,
                context=parent,
                kind=SpanKind.SERVER,
                attributes=span_attributes,
            )
        request_telemetry = _RequestTelemetry(
            span=span,
            span_method=span_method,
            tracer=tracer if config["operation_spans"] else None,
            logger=_logs.get_logger(
                "fastapi",
                __version__,
                config["logger_provider"],
                schema_url=_SCHEMA_URL,
            )
            if logging
            else None,
            _mount_prefix=scope.get("app_root_path", scope.get("root_path", "")).rstrip(
                "/"
            ),
        )
        scope["fastapi.telemetry"] = request_telemetry
        token = otel_context.attach(
            otel_context.set_value(_REQUEST_TELEMETRY_KEY, request_telemetry)
        )
        finished = False
        trailers = False
        disconnected = False

        def finish(error: BaseException | None = None) -> None:
            nonlocal finished
            if finished:
                return
            finished = True
            if request_telemetry.route is not None:
                attributes["http.route"] = request_telemetry.route
            if request_telemetry.status_code is not None:
                attributes["http.response.status_code"] = request_telemetry.status_code
            failed = (
                error is not None
                or not is_websocket
                and (
                    request_telemetry.status_code is None
                    or request_telemetry.status_code >= 500
                )
            )
            if failed:
                errors = request_telemetry._exceptions
                failure = error or (errors[-1] if errors else None)
                attributes["error.type"] = (
                    _exception_type(failure)
                    if failure
                    else str(request_telemetry.status_code or "incomplete_response")
                )
            if span is not None:
                span.set_attributes(attributes)
                if failed:
                    span.set_status(StatusCode.ERROR)
            # Record while the span is current, so exemplars can correlate it.
            if duration is not None:
                duration.record(max(0, perf_counter() - started), attributes)
            if active is not None:
                active.add(-1, active_attributes)
            if span is not None:
                span.end()

        async def wrapped_send(message: Message) -> None:
            nonlocal trailers
            if message["type"] == "http.response.start":
                request_telemetry.status_code = message["status"]
                trailers = message.get("trailers", False)
            await send(message)
            if (
                (
                    message["type"] == "http.response.body"
                    and not message.get("more_body", False)
                    and not trailers
                )
                or (
                    message["type"] == "http.response.trailers"
                    and not message.get("more_trailers", False)
                )
                or message["type"] == "http.response.pathsend"
            ):
                finish()

        async def wrapped_receive() -> Message:
            nonlocal disconnected
            message = await receive()
            if message["type"] == "http.disconnect":
                disconnected = True
            return message

        context = (
            trace.use_span(
                span,
                end_on_exit=False,
                record_exception=False,
                set_status_on_exception=False,
            )
            if span is not None
            else nullcontext()
        )
        try:
            with context:
                try:
                    await app(
                        scope,
                        receive if is_websocket else wrapped_receive,
                        send if is_websocket else wrapped_send,
                    )
                except BaseException as exc:
                    _exception(scope=scope, exc=exc)
                    finish(
                        None
                        if is_websocket and _normal_websocket_disconnect(exc)
                        else exc
                    )
                    raise
                finally:
                    if not finished:
                        finish(
                            None
                            if is_websocket
                            else ConnectionError("Client disconnected")
                            if disconnected
                            else RuntimeError("Incomplete ASGI response")
                        )
        finally:
            request_telemetry.data = None
            request_telemetry._exceptions.clear()
            otel_context.detach(token)
            scope.pop("fastapi.telemetry", None)
            if parent_token is not None:
                otel_context.detach(parent_token)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def __call__(
        self,
        *,
        app: ASGIApp,
        scope: Scope,
        receive: Receive,
        send: Send,
        legacy_otel: bool = False,
    ) -> None:
        config = self.config
        if config["exclude"] is not None and config["exclude"](scope):
            # Keep mounted FastAPI apps from observing this excluded request.
            scope["fastapi.telemetry"] = None
            try:
                await app(scope, receive, send)
            finally:
                scope.pop("fastapi.telemetry", None)
            return
        tracing = config["tracing"] and not legacy_otel
        logging = config["logs"] and not legacy_otel
        if logging:
            logger_provider = config["logger_provider"] or _logs.get_logger_provider()
            logging = not (
                (config["logger_provider"] is None and _unconfigured(logger_provider))
                or isinstance(logger_provider, _logs.NoOpLoggerProvider)
            )
        is_websocket = scope["type"] == "websocket"
        metering = config["metrics"] and not legacy_otel and not is_websocket
        if tracing:
            provider = config["tracer_provider"] or trace.get_tracer_provider()
            tracing = not (
                (config["tracer_provider"] is None and _unconfigured(provider))
                or isinstance(provider, trace.NoOpTracerProvider)
            )
        if metering:
            meter_provider = config["meter_provider"] or metrics.get_meter_provider()
            metering = not (
                (config["meter_provider"] is None and _unconfigured(meter_provider))
                or isinstance(meter_provider, metrics.NoOpMeterProvider)
            )
        if not tracing and not metering and not logging:
            await app(scope, receive, send)
            return
        original_method = scope.get("method", "")
        method = original_method if original_method in self._known_methods else "_OTHER"
        span_method = "WS" if is_websocket else "HTTP" if method == "_OTHER" else method
        attributes: dict[str, Any] = {
            "url.scheme": scope.get("scheme", "ws" if is_websocket else "http"),
        }
        if is_websocket:
            attributes["network.protocol.name"] = "websocket"
        else:
            attributes["http.request.method"] = method
            if scope.get("http_version"):
                attributes["network.protocol.version"] = scope["http_version"]
        duration, active = self._instruments() if metering else (None, None)
        active_attributes = {
            k: v for k, v in attributes.items() if k != "network.protocol.version"
        }
        if active is not None:
            active.add(1, active_attributes)
        started = perf_counter()
        span = None
        tracer = None
        parent_token = None
        if tracing:
            parent = propagate.extract(Headers(scope=scope), getter=_HEADERS_GETTER)
            parent_token = otel_context.attach(parent)
            tracer = self._get_tracer(provider=provider)
            span_attributes = {**attributes, **_server_attributes(scope)}
            if not is_websocket:
                span_attributes["url.path"] = scope["path"]
                if scope.get("query_string"):
                    span_attributes["url.query"] = urlencode(
                        [
                            (
                                key,
                                "REDACTED"
                                if key in _SENSITIVE_QUERY_PARAMETERS
                                else value,
                            )
                            for key, value in parse_qsl(
                                scope["query_string"].decode("latin-1"),
                                keep_blank_values=True,
                            )
                        ]
                    )
                if original_method != method:
                    span_attributes["http.request.method_original"] = original_method
            span = tracer.start_span(
                span_method,
                context=parent,
                kind=SpanKind.SERVER,
                attributes=span_attributes,
            )
        request_telemetry = _RequestTelemetry(
            span=span,
            span_method=span_method,
            tracer=tracer if config["operation_spans"] else None,
            logger=_logs.get_logger(
                "fastapi",
                __version__,
                config["logger_provider"],
                schema_url=_SCHEMA_URL,
            )
            if logging
            else None,
            _mount_prefix=scope.get("app_root_path", scope.get("root_path", "")).rstrip(
                "/"
            ),
        )
        scope["fastapi.telemetry"] = request_telemetry
        token = otel_context.attach(
            otel_context.set_value(_REQUEST_TELEMETRY_KEY, request_telemetry)
        )
        finished = False
        trailers = False
        disconnected = False

        def finish(error: BaseException | None = None) -> None:
            nonlocal finished
            if finished:
                return
            finished = True
            if request_telemetry.route is not None:
                attributes["http.route"] = request_telemetry.route
            if request_telemetry.status_code is not None:
                attributes["http.response.status_code"] = request_telemetry.status_code
            failed = (
                error is not None
                or not is_websocket
                and (
                    request_telemetry.status_code is None
                    or request_telemetry.status_code >= 500
                )
            )
            if failed:
                errors = request_telemetry._exceptions
                failure = error or (errors[-1] if errors else None)
                attributes["error.type"] = (
                    _exception_type(failure)
                    if failure
                    else str(request_telemetry.status_code or "incomplete_response")
                )
            if span is not None:
                span.set_attributes(attributes)
                if failed:
                    span.set_status(StatusCode.ERROR)
            # Record while the span is current, so exemplars can correlate it.
            if duration is not None:
                duration.record(max(0, perf_counter() - started), attributes)
            if active is not None:
                active.add(-1, active_attributes)
            if span is not None:
                span.end()

        async def wrapped_send(message: Message) -> None:
            nonlocal trailers
            if message["type"] == "http.response.start":
                request_telemetry.status_code = message["status"]
                trailers = message.get("trailers", False)
            await send(message)
            if (
                (
                    message["type"] == "http.response.body"
                    and not message.get("more_body", False)
                    and not trailers
                )
                or (
                    message["type"] == "http.response.trailers"
                    and not message.get("more_trailers", False)
                )
                or message["type"] == "http.response.pathsend"
            ):
                finish()

        async def wrapped_receive() -> Message:
            nonlocal disconnected
            message = await receive()
            if message["type"] == "http.disconnect":
                disconnected = True
            return message

        context = (
            trace.use_span(
                span,
                end_on_exit=False,
                record_exception=False,
                set_status_on_exception=False,
            )
            if span is not None
            else nullcontext()
        )
        try:
            with context:
                try:
                    await app(
                        scope,
                        receive if is_websocket else wrapped_receive,
                        send if is_websocket else wrapped_send,
                    )
                except BaseException as exc:
                    _exception(scope=scope, exc=exc)
                    finish(
                        None
                        if is_websocket and _normal_websocket_disconnect(exc)
                        else exc
                    )
                    raise
                finally:
                    if not finished:
                        finish(
                            None
                            if is_websocket
                            else ConnectionError("Client disconnected")
                            if disconnected
                            else RuntimeError("Incomplete ASGI response")
                        )
        finally:
            request_telemetry.data = None
            request_telemetry._exceptions.clear()
            otel_context.detach(token)
            scope.pop("fastapi.telemetry", None)
            if parent_token is not None:
                otel_context.detach(parent_token)
```

### 🔹 函式: `NativeTelemetry.__init__()`
- **變更前簽章 (Before)**: `def __init__(self, config: TelemetryConfig) -> None` (L158~L170)
- **變更後簽章 (After)**: `def __init__(self, config: TelemetryConfig) -> None` (L158~L172)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(self, config: TelemetryConfig) -> None:
        self.config = config
        known_methods = os.getenv("OTEL_INSTRUMENTATION_HTTP_KNOWN_METHODS", "").strip()
        self._known_methods = (
            frozenset(
                method.strip() for method in known_methods.split(",") if method.strip()
            )
            if known_methods
            else _HTTP_METHODS
        )
        self._provider: metrics.MeterProvider | None = None
        self._duration: Histogram | None = None
        self._active: UpDownCounter | None = None
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(self, config: TelemetryConfig) -> None:
        self.config = config
        known_methods = os.getenv("OTEL_INSTRUMENTATION_HTTP_KNOWN_METHODS", "").strip()
        self._known_methods = (
            frozenset(
                method.strip() for method in known_methods.split(",") if method.strip()
            )
            if known_methods
            else _HTTP_METHODS
        )
        self._provider: metrics.MeterProvider | None = None
        self._duration: Histogram | None = None
        self._active: UpDownCounter | None = None
        self._tracer_provider: trace.TracerProvider | None = None
        self._tracer: trace.Tracer | None = None
```


---

### 🔹 Commit #14: `1d4953d2`
- **完整 Hash**: `1d4953d2e528b58cfb09bbc28fb25dcda227c6ea`
- **說明 (Ground Truth)**: 🐛 Allow startup when automatic OpenTelemetry configuration fails (#16418)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/telemetry/_runtime.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:46, E:47, A:0) ➔ After(N:47, E:47, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `warning (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `wrapped_receive` ──[CALLS]──> `warning (External/Unresolved)`
  • - [移除呼叫邊] `wrapped_receive` ──[CALLS]──> `send (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `lifespan()`
- **變更前簽章 (Before)**: `async def lifespan( *, config: TelemetryConfig, app: ASGIApp, scope: Scope, receive: Receive, send: Send ) -> None: # Consume startup only inside the wrapper, and preserve ASGI failure events. # Initialization exceptions before app(scope) would otherwise look like a # server's unsupported-lifespan fallback and silently disable telemetry.` (L210~L239)
- **變更後簽章 (After)**: `async def lifespan( *, config: TelemetryConfig, app: ASGIApp, scope: Scope, receive: Receive, send: Send ) -> None` (L210~L238)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def lifespan(
    *, config: TelemetryConfig, app: ASGIApp, scope: Scope, receive: Receive, send: Send
) -> None:
    # Consume startup only inside the wrapper, and preserve ASGI failure events.
    # Initialization exceptions before app(scope) would otherwise look like a
    # server's unsupported-lifespan fallback and silently disable telemetry.
    async def wrapped_receive() -> Message:
        message = await receive()
        if message["type"] == "lifespan.startup":
            try:
                _configure_from_environment(config)
            except Exception as exc:
                await send({"type": "lifespan.startup.failed", "message": str(exc)})
                raise
        return message

    async def wrapped_send(message: Message) -> None:
        if (
            message["type"]
            in {
                "lifespan.shutdown.complete",
                "lifespan.shutdown.failed",
                "lifespan.startup.failed",
            }
            and _owned
        ):
            await run_sync(_flush)
        await send(message)

    await app(scope, wrapped_receive, wrapped_send)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def lifespan(
    *, config: TelemetryConfig, app: ASGIApp, scope: Scope, receive: Receive, send: Send
) -> None:
    async def wrapped_receive() -> Message:
        message = await receive()
        if message["type"] == "lifespan.startup":
            try:
                _configure_from_environment(config)
            except Exception as exc:
                # Optional telemetry setup must not prevent application startup.
                logger.warning(
                    "FastAPI automatic telemetry configuration failed: %s", exc
                )
        return message

    async def wrapped_send(message: Message) -> None:
        if (
            message["type"]
            in {
                "lifespan.shutdown.complete",
                "lifespan.shutdown.failed",
                "lifespan.startup.failed",
            }
            and _owned
        ):
            await run_sync(_flush)
        await send(message)

    await app(scope, wrapped_receive, wrapped_send)
```

### 🔹 函式: `wrapped_receive()`
- **變更前簽章 (Before)**: `async def wrapped_receive() -> Message` (L216~L224)
- **變更後簽章 (After)**: `async def wrapped_receive() -> Message` (L213~L223)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def wrapped_receive() -> Message:
        message = await receive()
        if message["type"] == "lifespan.startup":
            try:
                _configure_from_environment(config)
            except Exception as exc:
                await send({"type": "lifespan.startup.failed", "message": str(exc)})
                raise
        return message
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def wrapped_receive() -> Message:
        message = await receive()
        if message["type"] == "lifespan.startup":
            try:
                _configure_from_environment(config)
            except Exception as exc:
                # Optional telemetry setup must not prevent application startup.
                logger.warning(
                    "FastAPI automatic telemetry configuration failed: %s", exc
                )
        return message
```


---

### 🔹 Commit #15: `ac88f563`
- **完整 Hash**: `ac88f563db5f4d3300d43355eca728c93ed9ffe2`
- **說明 (Ground Truth)**: 🐛 Fix repeated endpoint wrapping in included routers (#16414)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/routing.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:285, E:432, A:0) ➔ After(N:285, E:432, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 4, -Edges: 4, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `_EffectiveRouteContext.from_api_route` ──[CALLS]──> `set (External/Unresolved)`
  • + [新增呼叫邊] `_EffectiveRouteContext.from_api_route` ──[CALLS]──> `request_response`
  • + [新增呼叫邊] `_EffectiveRouteContext.from_api_route` ──[CALLS]──> `APIRoute.get_route_handler`
  • + [新增呼叫邊] `_EffectiveRouteContext.from_api_route` ──[CALLS]──> `reset (External/Unresolved)`
  • - [移除呼叫邊] `APIRoute.handle` ──[CALLS]──> `set (External/Unresolved)`
  • - [移除呼叫邊] `APIRoute.handle` ──[CALLS]──> `request_response`
  • - [移除呼叫邊] `APIRoute.handle` ──[CALLS]──> `APIRoute.get_route_handler`
  • - [移除呼叫邊] `APIRoute.handle` ──[CALLS]──> `reset (External/Unresolved)`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'app' 被深鎖在內部閉包 (scope:request_response@after/fastapi/routing.py:L128)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `APIRoute.handle()`
- **變更前簽章 (Before)**: `async def handle(self, scope: Scope, receive: Receive, send: Send) -> None` (L1294~L1314)
- **變更後簽章 (After)**: `async def handle(self, scope: Scope, receive: Receive, send: Send) -> None` (L1294~L1310)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def handle(self, scope: Scope, receive: Receive, send: Send) -> None:
        effective_context = _get_scope_effective_route_context(scope)
        if effective_context is not None and effective_context.original_route is self:
            methods = effective_context.methods
            if methods and scope["method"] not in methods:
                headers = {"Allow": ", ".join(methods)}
                if "app" in scope:
                    raise HTTPException(status_code=405, headers=headers)
                response = PlainTextResponse(
                    "Method Not Allowed", status_code=405, headers=headers
                )
                await response(scope, receive, send)
                return
            token = _effective_route_context_var.set(effective_context)
            try:
                app = request_response(self.get_route_handler())
            finally:
                _effective_route_context_var.reset(token)
            await app(scope, receive, send)
            return
        await super().handle(scope, receive, send)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def handle(self, scope: Scope, receive: Receive, send: Send) -> None:
        effective_context = _get_scope_effective_route_context(scope)
        if effective_context is not None and effective_context.original_route is self:
            methods = effective_context.methods
            if methods and scope["method"] not in methods:
                headers = {"Allow": ", ".join(methods)}
                if "app" in scope:
                    raise HTTPException(status_code=405, headers=headers)
                response = PlainTextResponse(
                    "Method Not Allowed", status_code=405, headers=headers
                )
                await response(scope, receive, send)
                return
            assert effective_context.app is not None
            await effective_context.app(scope, receive, send)
            return
        await super().handle(scope, receive, send)
```

### 🔹 函式: `_EffectiveRouteContext.from_api_route()`
- **變更前簽章 (Before)**: `def from_api_route( cls, *, original_route: APIRoute, include_context: _RouterIncludeContext, ) -> "_EffectiveRouteContext"` (L1459~L1511)
- **變更後簽章 (After)**: `def from_api_route( cls, *, original_route: APIRoute, include_context: _RouterIncludeContext, ) -> "_EffectiveRouteContext"` (L1456~L1515)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def from_api_route(
        cls,
        *,
        original_route: APIRoute,
        include_context: _RouterIncludeContext,
    ) -> "_EffectiveRouteContext":
        route = cast(_APIRouteLike, original_route)
        context = cls(original_route=original_route)
        _populate_api_route_state(
            cast(_APIRouteLike, context),
            include_context.path_for(original_route),
            route.endpoint,
            response_model=route.response_model,
            status_code=route.status_code,
            tags=[*include_context.tags, *route.tags],
            dependencies=[*include_context.dependencies, *route.dependencies],
            summary=route.summary,
            description=route.description,
            response_description=route.response_description,
            responses={**include_context.responses, **route.responses},
            deprecated=route.deprecated or include_context.deprecated,
            methods=route.methods,
            operation_id=route.operation_id,
            response_model_include=route.response_model_include,
            response_model_exclude=route.response_model_exclude,
            response_model_by_alias=route.response_model_by_alias,
            response_model_exclude_unset=route.response_model_exclude_unset,
            response_model_exclude_defaults=route.response_model_exclude_defaults,
            response_model_exclude_none=route.response_model_exclude_none,
            include_in_schema=route.include_in_schema
            and include_context.include_in_schema,
            response_class=get_value_or_default(
                route.response_class,
                include_context.included_router.default_response_class,
                include_context.default_response_class,
            ),
            name=route.name,
            dependency_overrides_provider=include_context.dependency_overrides_provider,
            callbacks=[*include_context.callbacks, *(route.callbacks or [])],
            openapi_extra=route.openapi_extra,
            generate_unique_id_function=get_value_or_default(
                route.generate_unique_id_function,
                include_context.included_router.generate_unique_id_function,
                include_context.generate_unique_id_function,
            ),
            strict_content_type=get_value_or_default(
                route.strict_content_type,
                include_context.included_router.strict_content_type,
                include_context.strict_content_type,
            ),
            stream_item_type=route.stream_item_type,
        )
        return context
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def from_api_route(
        cls,
        *,
        original_route: APIRoute,
        include_context: _RouterIncludeContext,
    ) -> "_EffectiveRouteContext":
        route = cast(_APIRouteLike, original_route)
        context = cls(original_route=original_route)
        _populate_api_route_state(
            cast(_APIRouteLike, context),
            include_context.path_for(original_route),
            route.endpoint,
            response_model=route.response_model,
            status_code=route.status_code,
            tags=[*include_context.tags, *route.tags],
            dependencies=[*include_context.dependencies, *route.dependencies],
            summary=route.summary,
            description=route.description,
            response_description=route.response_description,
            responses={**include_context.responses, **route.responses},
            deprecated=route.deprecated or include_context.deprecated,
            methods=route.methods,
            operation_id=route.operation_id,
            response_model_include=route.response_model_include,
            response_model_exclude=route.response_model_exclude,
            response_model_by_alias=route.response_model_by_alias,
            response_model_exclude_unset=route.response_model_exclude_unset,
            response_model_exclude_defaults=route.response_model_exclude_defaults,
            response_model_exclude_none=route.response_model_exclude_none,
            include_in_schema=route.include_in_schema
            and include_context.include_in_schema,
            response_class=get_value_or_default(
                route.response_class,
                include_context.included_router.default_response_class,
                include_context.default_response_class,
            ),
            name=route.name,
            dependency_overrides_provider=include_context.dependency_overrides_provider,
            callbacks=[*include_context.callbacks, *(route.callbacks or [])],
            openapi_extra=route.openapi_extra,
            generate_unique_id_function=get_value_or_default(
                route.generate_unique_id_function,
                include_context.included_router.generate_unique_id_function,
                include_context.generate_unique_id_function,
            ),
            strict_content_type=get_value_or_default(
                route.strict_content_type,
                include_context.included_router.strict_content_type,
                include_context.strict_content_type,
            ),
            stream_item_type=route.stream_item_type,
        )
        # Build once per inclusion context, just as APIRoute does for direct routes.
        # Integrations may wrap dependant.call while constructing the handler.
        token = _effective_route_context_var.set(context)
        try:
            context.app = request_response(original_route.get_route_handler())
        finally:
            _effective_route_context_var.reset(token)
        return context
```


---

### 🔹 Commit #16: `d6235443`
- **完整 Hash**: `d62354434b2e508fe89024213b220ca8e67dea5e`
- **說明 (Ground Truth)**: 🐛 Fix support for background tasks and headers from dependencies in `app.frontend()` (#16105)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/routing.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:279, E:411, A:0) ➔ After(N:281, E:417, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 7, -Edges: 1, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `check_config (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `_FrontendStaticFiles.get_response_for_scope` (FUNCTION_DEF)
  • + [新增呼叫邊] `_FrontendStaticFiles.get_response_for_scope` ──[CALLS]──> `check_config (External/Unresolved)`
  • + [新增呼叫邊] `_FrontendStaticFiles.get_response_for_scope` ──[CALLS]──> `_FrontendStaticFiles.get_response`
  • + [新增呼叫邊] `_FrontendStaticFiles.get_response_for_scope` ──[CALLS]──> `_FrontendStaticFiles.get_path`
  • + [新增呼叫邊] `_FrontendRoute.handle` ──[CALLS]──> `_FrontendStaticFiles.get_response_for_scope`
  • + [新增呼叫邊] `_FrontendRoute.handle` ──[CALLS]──> `response (External/Unresolved)`
  • + [新增呼叫邊] `_FrontendRouteGroup.handle` ──[CALLS]──> `_FrontendStaticFiles.get_response_for_scope`
  • + [新增呼叫邊] `_FrontendRouteGroup.handle` ──[CALLS]──> `response (External/Unresolved)`
  • - [移除呼叫邊] `_FrontendRoute.handle` ──[CALLS]──> `app`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'app' 被深鎖在內部閉包 (scope:request_response@after/fastapi/routing.py:L121)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_FrontendRouteGroup.handle()`
- **變更前簽章 (Before)**: `async def handle(self, scope: Scope, receive: Receive, send: Send) -> None` (L2163~L2195)
- **變更後簽章 (After)**: `async def handle(self, scope: Scope, receive: Receive, send: Send) -> None` (L2171~L2207)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def handle(self, scope: Scope, receive: Receive, send: Send) -> None:
        effective_context = _get_scope_effective_route_context(scope)
        if (
            isinstance(effective_context, _EffectiveRouteContext)
            and effective_context.original_route is self
        ):
            prefix = effective_context.frontend_prefix
            dependant = effective_context.dependant
            dependency_overrides_provider = (
                effective_context.dependency_overrides_provider
            )
            embed_body_fields = effective_context._embed_body_fields
        else:
            prefix = ""
            dependant = self.dependant
            dependency_overrides_provider = self.dependency_overrides_provider
            embed_body_fields = self._embed_body_fields
        match, child_scope, route = self._match(scope, prefix=prefix)
        if match == Match.NONE or route is None:
            raise HTTPException(status_code=404)
        _update_scope(scope, child_scope)
        if match == Match.FULL and dependant and dependant.dependencies:
            async with self._solve_dependencies(
                scope,
                receive,
                send,
                dependant=dependant,
                dependency_overrides_provider=dependency_overrides_provider,
                embed_body_fields=embed_body_fields,
            ):
                await route.handle(scope, receive, send)
            return
        await route.handle(scope, receive, send)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def handle(self, scope: Scope, receive: Receive, send: Send) -> None:
        effective_context = _get_scope_effective_route_context(scope)
        if (
            isinstance(effective_context, _EffectiveRouteContext)
            and effective_context.original_route is self
        ):
            prefix = effective_context.frontend_prefix
            dependant = effective_context.dependant
            dependency_overrides_provider = (
                effective_context.dependency_overrides_provider
            )
            embed_body_fields = effective_context._embed_body_fields
        else:
            prefix = ""
            dependant = self.dependant
            dependency_overrides_provider = self.dependency_overrides_provider
            embed_body_fields = self._embed_body_fields
        match, child_scope, route = self._match(scope, prefix=prefix)
        if match == Match.NONE or route is None:
            raise HTTPException(status_code=404)
        _update_scope(scope, child_scope)
        if match == Match.FULL and dependant and dependant.dependencies:
            async with self._solve_dependencies(
                scope,
                receive,
                send,
                dependant=dependant,
                dependency_overrides_provider=dependency_overrides_provider,
                embed_body_fields=embed_body_fields,
            ) as solved_result:
                response = await route.app.get_response_for_scope(scope)
                if response.background is None:
                    response.background = solved_result.background_tasks
                response.headers.raw.extend(solved_result.response.headers.raw)
                await response(scope, receive, send)
            return
        await route.handle(scope, receive, send)
```

### 🔹 函式: `_FrontendRoute.handle()`
- **變更前簽章 (Before)**: `async def handle(self, scope: Scope, receive: Receive, send: Send) -> None` (L2088~L2089)
- **變更後簽章 (After)**: `async def handle(self, scope: Scope, receive: Receive, send: Send) -> None` (L2095~L2097)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def handle(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.app(scope, receive, send)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def handle(self, scope: Scope, receive: Receive, send: Send) -> None:
        response = await self.app.get_response_for_scope(scope)
        await response(scope, receive, send)
```

### 🔹 函式: `_FrontendRouteGroup._solve_dependencies()`
- **變更前簽章 (Before)**: `async def _solve_dependencies( self, scope: Scope, receive: Receive, send: Send, *, dependant: Dependant, dependency_overrides_provider: Any | None, embed_body_fields: bool, ) -> AsyncIterator[None]` (L2204~L2240)
- **變更後簽章 (After)**: `async def _solve_dependencies( self, scope: Scope, receive: Receive, send: Send, *, dependant: Dependant, dependency_overrides_provider: Any | None, embed_body_fields: bool, ) -> AsyncIterator[SolvedDependency]` (L2216~L2252)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def _solve_dependencies(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
        *,
        dependant: Dependant,
        dependency_overrides_provider: Any | None,
        embed_body_fields: bool,
    ) -> AsyncIterator[None]:
        request = Request(scope, receive, send)
        previous_inner_astack = scope.get("fastapi_inner_astack", _SCOPE_MISSING)
        previous_function_astack = scope.get("fastapi_function_astack", _SCOPE_MISSING)
        try:
            async with AsyncExitStack() as request_stack:
                scope["fastapi_inner_astack"] = request_stack
                async with AsyncExitStack() as function_stack:
                    scope["fastapi_function_astack"] = function_stack
                    solved_result = await solve_dependencies(
                        request=request,
                        dependant=dependant,
                        dependency_overrides_provider=dependency_overrides_provider,
                        async_exit_stack=request_stack,
                        embed_body_fields=embed_body_fields,
                    )
                    if solved_result.errors:
                        raise RequestValidationError(solved_result.errors)
                    yield
        finally:
            if previous_inner_astack is _SCOPE_MISSING:
                scope.pop("fastapi_inner_astack", None)
            else:
                scope["fastapi_inner_astack"] = previous_inner_astack
            if previous_function_astack is _SCOPE_MISSING:
                scope.pop("fastapi_function_astack", None)
            else:
                scope["fastapi_function_astack"] = previous_function_astack
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def _solve_dependencies(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
        *,
        dependant: Dependant,
        dependency_overrides_provider: Any | None,
        embed_body_fields: bool,
    ) -> AsyncIterator[SolvedDependency]:
        request = Request(scope, receive, send)
        previous_inner_astack = scope.get("fastapi_inner_astack", _SCOPE_MISSING)
        previous_function_astack = scope.get("fastapi_function_astack", _SCOPE_MISSING)
        try:
            async with AsyncExitStack() as request_stack:
                scope["fastapi_inner_astack"] = request_stack
                async with AsyncExitStack() as function_stack:
                    scope["fastapi_function_astack"] = function_stack
                    solved_result = await solve_dependencies(
                        request=request,
                        dependant=dependant,
                        dependency_overrides_provider=dependency_overrides_provider,
                        async_exit_stack=request_stack,
                        embed_body_fields=embed_body_fields,
                    )
                    if solved_result.errors:
                        raise RequestValidationError(solved_result.errors)
                    yield solved_result
        finally:
            if previous_inner_astack is _SCOPE_MISSING:
                scope.pop("fastapi_inner_astack", None)
            else:
                scope["fastapi_inner_astack"] = previous_inner_astack
            if previous_function_astack is _SCOPE_MISSING:
                scope.pop("fastapi_function_astack", None)
            else:
                scope["fastapi_function_astack"] = previous_function_astack
```


---

### 🔹 Commit #17: `5429fed8`
- **完整 Hash**: `5429fed84e84e32672c25a953eca3429b841ce90`
- **說明 (Ground Truth)**: ✨ Add `app.frontend(check_dir="auto")`, to make local development more convenient with `fastapi dev` (#16102)
- **變更檔案數**: 2

#### 📄 檔案: `fastapi/applications.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:57, E:70, A:0) ➔ After(N:58, E:71, A:0)
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
  • + [新增節點] `_resolve_frontend_check_dir (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `FastAPI.frontend` ──[CALLS]──> `_resolve_frontend_check_dir (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FastAPI.frontend()`
- **變更前簽章 (Before)**: `def frontend( self, path: Annotated[ str, Doc( """ The URL path prefix where the frontend build should be served. """ ), ], *, directory: Annotated[ str | os.PathLike[str], Doc( """ The directory containing the static frontend build output. """ ), ], fallback: Annotated[ Literal["auto", "index.html", "404.html"] | None, Doc( """ The fallback file behavior for missing frontend paths. """ ), ] = "auto", check_dir: Annotated[ bool, Doc( """ Check that the frontend directory exists when the app is created. """ ), ] = True, ) -> None` (L1222~L1293)
- **變更後簽章 (After)**: `def frontend( self, path: Annotated[ str, Doc( """ The URL path prefix where the frontend build should be served. """ ), ], *, directory: Annotated[ str | os.PathLike[str], Doc( """ The directory containing the static frontend build output. """ ), ], fallback: Annotated[ Literal["auto", "index.html", "404.html"] | None, Doc( """ The fallback file behavior for missing frontend paths. """ ), ] = "auto", check_dir: Annotated[ bool | Literal["auto"], Doc( """ Check that the frontend directory exists when the app is created. When set to `"auto"`, skip the check with a warning when `FASTAPI_ENV` is `"development"`, and check it otherwise. The `fastapi dev` command sets `FASTAPI_ENV` to `"development"` if it is not already set. """ ), ] = "auto", ) -> None` (L1222~L1299)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def frontend(
        self,
        path: Annotated[
            str,
            Doc(
                """
                The URL path prefix where the frontend build should be served.
                """
            ),
        ],
        *,
        directory: Annotated[
            str | os.PathLike[str],
            Doc(
                """
                The directory containing the static frontend build output.
                """
            ),
        ],
        fallback: Annotated[
            Literal["auto", "index.html", "404.html"] | None,
            Doc(
                """
                The fallback file behavior for missing frontend paths.
                """
            ),
        ] = "auto",
        check_dir: Annotated[
            bool,
            Doc(
                """
                Check that the frontend directory exists when the app is created.
                """
            ),
        ] = True,
    ) -> None:
        """
        Serve a static frontend build as low-priority routes.

        Use this for frontend tools that build static files into a directory,
        such as `dist`. **FastAPI** path operations are checked first, and
        the frontend files are checked only if no normal route matched.

        A typical project could look like this:

        ```text
        .
        ├── pyproject.toml
        ├── app
        │   ├── __init__.py
        │   └── main.py
        └── dist
            ├── index.html
            └── assets
                └── app.js
        ```

        Then in `app/main.py`:

        ```python
        from fastapi import FastAPI

        app = FastAPI()
        app.frontend("/", directory="dist")
        ```
        """
        self.router.frontend(
            path,
            directory=directory,
            fallback=fallback,
            check_dir=check_dir,
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def frontend(
        self,
        path: Annotated[
            str,
            Doc(
                """
                The URL path prefix where the frontend build should be served.
                """
            ),
        ],
        *,
        directory: Annotated[
            str | os.PathLike[str],
            Doc(
                """
                The directory containing the static frontend build output.
                """
            ),
        ],
        fallback: Annotated[
            Literal["auto", "index.html", "404.html"] | None,
            Doc(
                """
                The fallback file behavior for missing frontend paths.
                """
            ),
        ] = "auto",
        check_dir: Annotated[
            bool | Literal["auto"],
            Doc(
                """
                Check that the frontend directory exists when the app is created. When
                set to `"auto"`, skip the check with a warning when `FASTAPI_ENV` is
                `"development"`, and check it otherwise. The `fastapi dev` command
                sets `FASTAPI_ENV` to `"development"` if it is not already set.
                """
            ),
        ] = "auto",
    ) -> None:
        """
        Serve a static frontend build as low-priority routes.

        Use this for frontend tools that build static files into a directory,
        such as `dist`. **FastAPI** path operations are checked first, and
        the frontend files are checked only if no normal route matched.

        A typical project could look like this:

        ```text
        .
        ├── pyproject.toml
        ├── app
        │   ├── __init__.py
        │   └── main.py
        └── dist
            ├── index.html
            └── assets
                └── app.js
        ```

        Then in `app/main.py`:

        ```python
        from fastapi import FastAPI

        app = FastAPI()
        app.frontend("/", directory="dist")
        ```
        """
        check_dir = routing._resolve_frontend_check_dir(
            directory=directory, check_dir=check_dir
        )
        self.router.frontend(
            path,
            directory=directory,
            fallback=fallback,
            check_dir=check_dir,
        )
```


#### 📄 檔案: `fastapi/routing.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:277, E:407, A:0) ➔ After(N:279, E:411, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 4, -Edges: 0, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `_resolve_frontend_check_dir` (FUNCTION_DEF)
  • + [新增節點] `warn (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `_resolve_frontend_check_dir` ──[CALLS]──> `isdir (External/Unresolved)`
  • + [新增呼叫邊] `_resolve_frontend_check_dir` ──[CALLS]──> `warn (External/Unresolved)`
  • + [新增呼叫邊] `_resolve_frontend_check_dir` ──[CALLS]──> `_get_resolved_absolute_path`
  • + [新增呼叫邊] `APIRouter.frontend` ──[CALLS]──> `_resolve_frontend_check_dir`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'app' 被深鎖在內部閉包 (scope:request_response@after/fastapi/routing.py:L120)，外部無法調用！ (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_FrontendRouteGroup.add_frontend_route()`
- **變更前簽章 (Before)**: `def add_frontend_route( self, path: str, *, directory: str | os.PathLike[str], fallback: Literal["auto", "index.html", "404.html"] | None = "auto", check_dir: bool = True, ) -> None` (L2096~L2111)
- **變更後簽章 (After)**: `def add_frontend_route( self, path: str, *, directory: str | os.PathLike[str], fallback: Literal["auto", "index.html", "404.html"] | None = "auto", check_dir: bool, ) -> None` (L2115~L2130)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def add_frontend_route(
        self,
        path: str,
        *,
        directory: str | os.PathLike[str],
        fallback: Literal["auto", "index.html", "404.html"] | None = "auto",
        check_dir: bool = True,
    ) -> None:
        self.routes.append(
            _FrontendRoute(
                path,
                directory=directory,
                fallback=fallback,
                check_dir=check_dir,
            )
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def add_frontend_route(
        self,
        path: str,
        *,
        directory: str | os.PathLike[str],
        fallback: Literal["auto", "index.html", "404.html"] | None = "auto",
        check_dir: bool,
    ) -> None:
        self.routes.append(
            _FrontendRoute(
                path,
                directory=directory,
                fallback=fallback,
                check_dir=check_dir,
            )
        )
```

### 🔹 函式: `_FrontendStaticFiles.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, *, directory: str | os.PathLike[str], fallback: Literal["auto", "index.html", "404.html"] | None, check_dir: bool = True, ) -> None` (L1880~L1900)
- **變更後簽章 (After)**: `def __init__( self, *, directory: str | os.PathLike[str], fallback: Literal["auto", "index.html", "404.html"] | None, check_dir: bool, ) -> None` (L1899~L1919)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        *,
        directory: str | os.PathLike[str],
        fallback: Literal["auto", "index.html", "404.html"] | None,
        check_dir: bool = True,
    ) -> None:
        self.fallback = fallback
        if check_dir and not os.path.isdir(directory):
            raise RuntimeError(
                f"Frontend directory '{directory}' does not exist. "
                f"Resolved absolute path: '{_get_resolved_absolute_path(directory)}'"
            )
        super().__init__(
            directory=directory,
            html=True,
            check_dir=check_dir,
            follow_symlink=False,
        )
        if check_dir and fallback in {"index.html", "404.html"}:
            self._check_fallback_file(fallback)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        *,
        directory: str | os.PathLike[str],
        fallback: Literal["auto", "index.html", "404.html"] | None,
        check_dir: bool,
    ) -> None:
        self.fallback = fallback
        if check_dir and not os.path.isdir(directory):
            raise RuntimeError(
                f"Frontend directory '{directory}' does not exist. "
                f"Resolved absolute path: '{_get_resolved_absolute_path(directory)}'"
            )
        super().__init__(
            directory=directory,
            html=True,
            check_dir=check_dir,
            follow_symlink=False,
        )
        if check_dir and fallback in {"index.html", "404.html"}:
            self._check_fallback_file(fallback)
```

### 🔹 函式: `_FrontendRoute.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, path: str, *, directory: str | os.PathLike[str], fallback: Literal["auto", "index.html", "404.html"] | None = "auto", check_dir: bool = True, ) -> None` (L2022~L2038)
- **變更後簽章 (After)**: `def __init__( self, path: str, *, directory: str | os.PathLike[str], fallback: Literal["auto", "index.html", "404.html"] | None = "auto", check_dir: bool, ) -> None` (L2041~L2057)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        path: str,
        *,
        directory: str | os.PathLike[str],
        fallback: Literal["auto", "index.html", "404.html"] | None = "auto",
        check_dir: bool = True,
    ) -> None:
        if fallback not in {"auto", "index.html", "404.html", None}:
            raise AssertionError(
                "fallback must be 'auto', 'index.html', '404.html', or None"
            )
        self.path = _normalize_frontend_path(path)
        self.methods = {"GET", "HEAD"}
        self.app = _FrontendStaticFiles(
            directory=directory, fallback=fallback, check_dir=check_dir
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        path: str,
        *,
        directory: str | os.PathLike[str],
        fallback: Literal["auto", "index.html", "404.html"] | None = "auto",
        check_dir: bool,
    ) -> None:
        if fallback not in {"auto", "index.html", "404.html", None}:
            raise AssertionError(
                "fallback must be 'auto', 'index.html', '404.html', or None"
            )
        self.path = _normalize_frontend_path(path)
        self.methods = {"GET", "HEAD"}
        self.app = _FrontendStaticFiles(
            directory=directory, fallback=fallback, check_dir=check_dir
        )
```

### 🔹 函式: `APIRouter.frontend()`
- **變更前簽章 (Before)**: `def frontend( self, path: Annotated[ str, Doc( """ The URL path prefix where the frontend build should be served. """ ), ], *, directory: Annotated[ str | os.PathLike[str], Doc( """ The directory containing the static frontend build output. """ ), ], fallback: Annotated[ Literal["auto", "index.html", "404.html"] | None, Doc( """ The fallback file behavior for missing frontend paths. """ ), ] = "auto", check_dir: Annotated[ bool, Doc( """ Check that the frontend directory exists when the app is created. """ ), ] = True, ) -> None` (L2599~L2680)
- **變更後簽章 (After)**: `def frontend( self, path: Annotated[ str, Doc( """ The URL path prefix where the frontend build should be served. """ ), ], *, directory: Annotated[ str | os.PathLike[str], Doc( """ The directory containing the static frontend build output. """ ), ], fallback: Annotated[ Literal["auto", "index.html", "404.html"] | None, Doc( """ The fallback file behavior for missing frontend paths. """ ), ] = "auto", check_dir: Annotated[ bool | Literal["auto"], Doc( """ Check that the frontend directory exists when the app is created. When set to `"auto"`, skip the check with a warning when `FASTAPI_ENV` is `"development"`, and check it otherwise. The `fastapi dev` command sets `FASTAPI_ENV` to `"development"` if it is not already set. """ ), ] = "auto", ) -> None` (L2618~L2705)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def frontend(
        self,
        path: Annotated[
            str,
            Doc(
                """
                The URL path prefix where the frontend build should be served.
                """
            ),
        ],
        *,
        directory: Annotated[
            str | os.PathLike[str],
            Doc(
                """
                The directory containing the static frontend build output.
                """
            ),
        ],
        fallback: Annotated[
            Literal["auto", "index.html", "404.html"] | None,
            Doc(
                """
                The fallback file behavior for missing frontend paths.
                """
            ),
        ] = "auto",
        check_dir: Annotated[
            bool,
            Doc(
                """
                Check that the frontend directory exists when the app is created.
                """
            ),
        ] = True,
    ) -> None:
        """
        Serve a static frontend build as low-priority routes.

        Use this for frontend tools that build static files into a directory,
        such as `dist`. **FastAPI** path operations are checked first, and
        the frontend files are checked only if no normal route matched.

        A typical project could look like this:

        ```text
        .
        ├── pyproject.toml
        ├── app
        │   ├── __init__.py
        │   └── main.py
        └── dist
            ├── index.html
            └── assets
                └── app.js
        ```

        Then in `app/main.py`:

        ```python
        from fastapi import APIRouter, FastAPI

        app = FastAPI()
        router = APIRouter()
        router.frontend("/", directory="dist")
        app.include_router(router)
        ```
        """
        normalized_path = _normalize_frontend_path(path)
        if self._frontend_routes is None:
            self._frontend_routes = _FrontendRouteGroup(
                dependencies=self.dependencies,
                dependency_overrides_provider=self.dependency_overrides_provider,
            )
            self._low_priority_routes.append(self._frontend_routes)
        self._frontend_routes.add_frontend_route(
            _join_frontend_paths(self.prefix, normalized_path),
            directory=directory,
            fallback=fallback,
            check_dir=check_dir,
        )
        self._mark_routes_changed()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def frontend(
        self,
        path: Annotated[
            str,
            Doc(
                """
                The URL path prefix where the frontend build should be served.
                """
            ),
        ],
        *,
        directory: Annotated[
            str | os.PathLike[str],
            Doc(
                """
                The directory containing the static frontend build output.
                """
            ),
        ],
        fallback: Annotated[
            Literal["auto", "index.html", "404.html"] | None,
            Doc(
                """
                The fallback file behavior for missing frontend paths.
                """
            ),
        ] = "auto",
        check_dir: Annotated[
            bool | Literal["auto"],
            Doc(
                """
                Check that the frontend directory exists when the app is created. When
                set to `"auto"`, skip the check with a warning when `FASTAPI_ENV` is
                `"development"`, and check it otherwise. The `fastapi dev` command
                sets `FASTAPI_ENV` to `"development"` if it is not already set.
                """
            ),
        ] = "auto",
    ) -> None:
        """
        Serve a static frontend build as low-priority routes.

        Use this for frontend tools that build static files into a directory,
        such as `dist`. **FastAPI** path operations are checked first, and
        the frontend files are checked only if no normal route matched.

        A typical project could look like this:

        ```text
        .
        ├── pyproject.toml
        ├── app
        │   ├── __init__.py
        │   └── main.py
        └── dist
            ├── index.html
            └── assets
                └── app.js
        ```

        Then in `app/main.py`:

        ```python
        from fastapi import APIRouter, FastAPI

        app = FastAPI()
        router = APIRouter()
        router.frontend("/", directory="dist")
        app.include_router(router)
        ```
        """
        check_dir = _resolve_frontend_check_dir(
            directory=directory, check_dir=check_dir
        )
        normalized_path = _normalize_frontend_path(path)
        if self._frontend_routes is None:
            self._frontend_routes = _FrontendRouteGroup(
                dependencies=self.dependencies,
                dependency_overrides_provider=self.dependency_overrides_provider,
            )
            self._low_priority_routes.append(self._frontend_routes)
        self._frontend_routes.add_frontend_route(
            _join_frontend_paths(self.prefix, normalized_path),
            directory=directory,
            fallback=fallback,
            check_dir=check_dir,
        )
        self._mark_routes_changed()
```


---

### 🔹 Commit #18: `e92a0dc3`
- **完整 Hash**: `e92a0dc3ce5ecbebb8655dbe5465cb61d48f9fc0`
- **說明 (Ground Truth)**: 🐛 Fix `status_code` being ignored for SSE and JSONL streaming endpoints (#15937)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/routing.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:277, E:407, A:0) ➔ After(N:277, E:407, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'app' 被深鎖在內部閉包 (scope:request_response@after/fastapi/routing.py:L119)，外部無法調用！ (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `app()`
- **變更前簽章 (Before)**: `async def app(request: Request) -> Response` (L404~L751)
- **變更後簽章 (After)**: `async def app(request: Request) -> Response` (L404~L757)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def app(request: Request) -> Response:
        response: Response | None = None
        file_stack = request.scope.get("fastapi_middleware_astack")
        assert isinstance(file_stack, AsyncExitStack), (
            "fastapi_middleware_astack not found in request scope"
        )

        # Extract endpoint context for error messages
        endpoint_ctx = (
            _extract_endpoint_context(dependant.call)
            if dependant.call
            else EndpointContext()
        )

        if dependant.path:
            # For mounted sub-apps, include the mount path prefix
            mount_path = request.scope.get("root_path", "").rstrip("/")
            endpoint_ctx["path"] = f"{request.method} {mount_path}{dependant.path}"

        # Read body and auto-close files
        try:
            body: Any = None
            if body_field:
                if is_body_form:
                    body = await request.form()
                    file_stack.push_async_callback(body.close)
                else:
                    body_bytes = await request.body()
                    if body_bytes:
                        json_body: Any = Undefined
                        content_type_value = request.headers.get("content-type")
                        if not content_type_value:
                            if not actual_strict_content_type:
                                json_body = await request.json()
                        else:
                            message = email.message.Message()
                            message["content-type"] = content_type_value
                            if message.get_content_maintype() == "application":
                                subtype = message.get_content_subtype()
                                if subtype == "json" or subtype.endswith("+json"):
                                    json_body = await request.json()
                        if json_body != Undefined:
                            body = json_body
                        else:
                            body = body_bytes
        except json.JSONDecodeError as e:
            validation_error = RequestValidationError(
                [
                    {
                        "type": "json_invalid",
                        "loc": ("body", e.pos),
                        "msg": "JSON decode error",
                        "input": {},
                        "ctx": {"error": e.msg},
                    }
                ],
                body=e.doc,
                endpoint_ctx=endpoint_ctx,
            )
            raise validation_error from e
        except HTTPException:
            # If a middleware raises an HTTPException, it should be raised again
            raise
        except Exception as e:
            http_error = HTTPException(
                status_code=400, detail="There was an error parsing the body"
            )
            raise http_error from e

        # Solve dependencies and run path operation function, auto-closing dependencies
        errors: list[Any] = []
        async_exit_stack = request.scope.get("fastapi_inner_astack")
        assert isinstance(async_exit_stack, AsyncExitStack), (
            "fastapi_inner_astack not found in request scope"
        )
        solved_result = await solve_dependencies(
            request=request,
            dependant=dependant,
            body=cast(dict[str, Any] | FormData | bytes | None, body),
            dependency_overrides_provider=dependency_overrides_provider,
            async_exit_stack=async_exit_stack,
            embed_body_fields=embed_body_fields,
        )
        errors = solved_result.errors
        assert dependant.call  # For types
        if not errors:
            # Shared serializer for stream items (JSONL and SSE).
            # Validates against stream_item_field when set, then
            # serializes to JSON bytes.
            def _serialize_data(data: Any) -> bytes:
                if stream_item_field:
                    value, errors_ = stream_item_field.validate(
                        data, {}, loc=("response",)
                    )
                    if errors_:
                        ctx = endpoint_ctx or EndpointContext()
                        raise ResponseValidationError(
                            errors=errors_,
                            body=data,
                            endpoint_ctx=ctx,
                        )
                    return stream_item_field.serialize_json(
                        value,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                    )
                else:
                    data = jsonable_encoder(data)
                    return json.dumps(data).encode("utf-8")

            if is_sse_stream:
                # Generator endpoint: stream as Server-Sent Events
                gen = dependant.call(**solved_result.values)

                def _serialize_sse_item(item: Any) -> bytes:
                    if isinstance(item, ServerSentEvent):
                        # User controls the event structure.
                        # Serialize the data payload if present.
                        # For ServerSentEvent items we skip stream_item_field
                        # validation (the user may mix types intentionally).
                        if item.raw_data is not None:
                            data_str: str | None = item.raw_data
                        elif item.data is not None:
                            if hasattr(item.data, "model_dump_json"):
                                data_str = item.data.model_dump_json()
                            else:
                                data_str = json.dumps(jsonable_encoder(item.data))
                        else:
                            data_str = None
                        return format_sse_event(
                            data_str=data_str,
                            event=item.event,
                            id=item.id,
                            retry=item.retry,
                            comment=item.comment,
                        )
                    else:
                        # Plain object: validate + serialize via
                        # stream_item_field (if set) and wrap in data field
                        return format_sse_event(
                            data_str=_serialize_data(item).decode("utf-8")
                        )

                if _is_async_gen_callable(dependant.call):
                    sse_aiter: AsyncIterator[Any] = gen.__aiter__()
                else:
                    sse_aiter = iterate_in_threadpool(gen)

                @asynccontextmanager
                async def _sse_producer_cm() -> AsyncIterator[
                    ObjectReceiveStream[bytes]
                ]:
                    # Use a memory stream to decouple generator iteration
                    # from the keepalive timer. A producer task pulls items
                    # from the generator independently, so
                    # `anyio.fail_after` never wraps the generator's
                    # `__anext__` directly - avoiding CancelledError that
                    # would finalize the generator and also working for sync
                    # generators running in a thread pool.
                    #
                    # This context manager is entered on the request-scoped
                    # AsyncExitStack so its __aexit__ (which cancels the
                    # task group) is called by the exit stack after the
                    # streaming response completes — not by async generator
                    # finalization via GeneratorExit.
                    # Ref: https://peps.python.org/pep-0789/
                    send_stream, receive_stream = anyio.create_memory_object_stream[
                        bytes
                    ](max_buffer_size=1)

                    async def _producer() -> None:
                        async with send_stream:
                            async for raw_item in sse_aiter:
                                await send_stream.send(_serialize_sse_item(raw_item))

                    send_keepalive, receive_keepalive = (
                        anyio.create_memory_object_stream[bytes](max_buffer_size=1)
                    )

                    async def _keepalive_inserter() -> None:
                        """Read from the producer and forward to the output,
                        inserting keepalive comments on timeout."""
                        async with send_keepalive, receive_stream:
                            try:
                                while True:
                                    try:
                                        with anyio.fail_after(_PING_INTERVAL):
                                            data = await receive_stream.receive()
                                        await send_keepalive.send(data)
                                    except TimeoutError:
                                        await send_keepalive.send(KEEPALIVE_COMMENT)
                            except anyio.EndOfStream:
                                pass

                    async with anyio.create_task_group() as tg:
                        tg.start_soon(_producer)
                        tg.start_soon(_keepalive_inserter)
                        yield receive_keepalive
                        tg.cancel_scope.cancel()

                # Enter the SSE context manager on the request-scoped
                # exit stack. The stack outlives the streaming response,
                # so __aexit__ runs via proper structured teardown, not
                # via GeneratorExit thrown into an async generator.
                sse_receive_stream = await async_exit_stack.enter_async_context(
                    _sse_producer_cm()
                )
                # Ensure the receive stream is closed when the exit stack
                # unwinds, preventing ResourceWarning from __del__.
                async_exit_stack.push_async_callback(sse_receive_stream.aclose)

                async def _sse_with_checkpoints(
                    stream: ObjectReceiveStream[bytes],
                ) -> AsyncIterator[bytes]:
                    async for data in stream:
                        yield data
                        # Guarantee a checkpoint so cancellation can be
                        # delivered even when the producer is faster than
                        # the consumer and receive() never suspends.
                        await anyio.sleep(0)

                sse_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                    _sse_with_checkpoints(sse_receive_stream)
                )

                response = StreamingResponse(
                    sse_stream_content,
                    media_type="text/event-stream",
                    background=solved_result.background_tasks,
                )
                response.headers["Cache-Control"] = "no-cache"
                # For Nginx proxies to not buffer server sent events
                response.headers["X-Accel-Buffering"] = "no"
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif is_json_stream:
                # Generator endpoint: stream as JSONL
                gen = dependant.call(**solved_result.values)

                def _serialize_item(item: Any) -> bytes:
                    return _serialize_data(item) + b"\n"

                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_jsonl() -> AsyncIterator[bytes]:
                        async for item in gen:
                            yield _serialize_item(item)
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    jsonl_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                        _async_stream_jsonl()
                    )
                else:

                    def _sync_stream_jsonl() -> Iterator[bytes]:
                        for item in gen:  # ty: ignore[not-iterable]
                            yield _serialize_item(item)

                    jsonl_stream_content = _sync_stream_jsonl()

                response = StreamingResponse(
                    jsonl_stream_content,
                    media_type="application/jsonl",
                    background=solved_result.background_tasks,
                )
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif _is_async_gen_callable(dependant.call) or _is_gen_callable(
                dependant.call
            ):
                # Raw streaming with explicit response_class (e.g. StreamingResponse)
                gen = dependant.call(**solved_result.values)
                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_raw(
                        async_gen: AsyncIterator[Any],
                    ) -> AsyncIterator[Any]:
                        async for chunk in async_gen:
                            yield chunk
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    gen = _async_stream_raw(gen)
                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = actual_response_class(content=gen, **response_args)
                response.headers.raw.extend(solved_result.response.headers.raw)
            else:
                raw_response = await run_endpoint_function(
                    dependant=dependant,
                    values=solved_result.values,
                    is_coroutine=is_coroutine,
                )
                if isinstance(raw_response, Response):
                    if raw_response.background is None:
                        raw_response.background = solved_result.background_tasks
                    response = raw_response
                else:
                    response_args = _build_response_args(
                        status_code=status_code, solved_result=solved_result
                    )
                    # Use the fast path (dump_json) when no custom response
                    # class was set and a response field with a TypeAdapter
                    # exists. Serializes directly to JSON bytes via Pydantic's
                    # Rust core, skipping the intermediate Python dict +
                    # json.dumps() step.
                    use_dump_json = response_field is not None and isinstance(
                        response_class, DefaultPlaceholder
                    )
                    content = await serialize_response(
                        field=response_field,
                        response_content=raw_response,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                        is_coroutine=is_coroutine,
                        endpoint_ctx=endpoint_ctx,
                        dump_json=use_dump_json,
                    )
                    if use_dump_json:
                        response = Response(
                            content=content,
                            media_type="application/json",
                            **response_args,
                        )
                    else:
                        response = actual_response_class(content, **response_args)
                    if not is_body_allowed_for_status_code(response.status_code):
                        response.body = b""
                    response.headers.raw.extend(solved_result.response.headers.raw)
        if errors:
            validation_error = RequestValidationError(
                errors, body=body, endpoint_ctx=endpoint_ctx
            )
            raise validation_error

        # Return response
        assert response
        return response
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def app(request: Request) -> Response:
        response: Response | None = None
        file_stack = request.scope.get("fastapi_middleware_astack")
        assert isinstance(file_stack, AsyncExitStack), (
            "fastapi_middleware_astack not found in request scope"
        )

        # Extract endpoint context for error messages
        endpoint_ctx = (
            _extract_endpoint_context(dependant.call)
            if dependant.call
            else EndpointContext()
        )

        if dependant.path:
            # For mounted sub-apps, include the mount path prefix
            mount_path = request.scope.get("root_path", "").rstrip("/")
            endpoint_ctx["path"] = f"{request.method} {mount_path}{dependant.path}"

        # Read body and auto-close files
        try:
            body: Any = None
            if body_field:
                if is_body_form:
                    body = await request.form()
                    file_stack.push_async_callback(body.close)
                else:
                    body_bytes = await request.body()
                    if body_bytes:
                        json_body: Any = Undefined
                        content_type_value = request.headers.get("content-type")
                        if not content_type_value:
                            if not actual_strict_content_type:
                                json_body = await request.json()
                        else:
                            message = email.message.Message()
                            message["content-type"] = content_type_value
                            if message.get_content_maintype() == "application":
                                subtype = message.get_content_subtype()
                                if subtype == "json" or subtype.endswith("+json"):
                                    json_body = await request.json()
                        if json_body != Undefined:
                            body = json_body
                        else:
                            body = body_bytes
        except json.JSONDecodeError as e:
            validation_error = RequestValidationError(
                [
                    {
                        "type": "json_invalid",
                        "loc": ("body", e.pos),
                        "msg": "JSON decode error",
                        "input": {},
                        "ctx": {"error": e.msg},
                    }
                ],
                body=e.doc,
                endpoint_ctx=endpoint_ctx,
            )
            raise validation_error from e
        except HTTPException:
            # If a middleware raises an HTTPException, it should be raised again
            raise
        except Exception as e:
            http_error = HTTPException(
                status_code=400, detail="There was an error parsing the body"
            )
            raise http_error from e

        # Solve dependencies and run path operation function, auto-closing dependencies
        errors: list[Any] = []
        async_exit_stack = request.scope.get("fastapi_inner_astack")
        assert isinstance(async_exit_stack, AsyncExitStack), (
            "fastapi_inner_astack not found in request scope"
        )
        solved_result = await solve_dependencies(
            request=request,
            dependant=dependant,
            body=cast(dict[str, Any] | FormData | bytes | None, body),
            dependency_overrides_provider=dependency_overrides_provider,
            async_exit_stack=async_exit_stack,
            embed_body_fields=embed_body_fields,
        )
        errors = solved_result.errors
        assert dependant.call  # For types
        if not errors:
            # Shared serializer for stream items (JSONL and SSE).
            # Validates against stream_item_field when set, then
            # serializes to JSON bytes.
            def _serialize_data(data: Any) -> bytes:
                if stream_item_field:
                    value, errors_ = stream_item_field.validate(
                        data, {}, loc=("response",)
                    )
                    if errors_:
                        ctx = endpoint_ctx or EndpointContext()
                        raise ResponseValidationError(
                            errors=errors_,
                            body=data,
                            endpoint_ctx=ctx,
                        )
                    return stream_item_field.serialize_json(
                        value,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                    )
                else:
                    data = jsonable_encoder(data)
                    return json.dumps(data).encode("utf-8")

            if is_sse_stream:
                # Generator endpoint: stream as Server-Sent Events
                gen = dependant.call(**solved_result.values)

                def _serialize_sse_item(item: Any) -> bytes:
                    if isinstance(item, ServerSentEvent):
                        # User controls the event structure.
                        # Serialize the data payload if present.
                        # For ServerSentEvent items we skip stream_item_field
                        # validation (the user may mix types intentionally).
                        if item.raw_data is not None:
                            data_str: str | None = item.raw_data
                        elif item.data is not None:
                            if hasattr(item.data, "model_dump_json"):
                                data_str = item.data.model_dump_json()
                            else:
                                data_str = json.dumps(jsonable_encoder(item.data))
                        else:
                            data_str = None
                        return format_sse_event(
                            data_str=data_str,
                            event=item.event,
                            id=item.id,
                            retry=item.retry,
                            comment=item.comment,
                        )
                    else:
                        # Plain object: validate + serialize via
                        # stream_item_field (if set) and wrap in data field
                        return format_sse_event(
                            data_str=_serialize_data(item).decode("utf-8")
                        )

                if _is_async_gen_callable(dependant.call):
                    sse_aiter: AsyncIterator[Any] = gen.__aiter__()
                else:
                    sse_aiter = iterate_in_threadpool(gen)

                @asynccontextmanager
                async def _sse_producer_cm() -> AsyncIterator[
                    ObjectReceiveStream[bytes]
                ]:
                    # Use a memory stream to decouple generator iteration
                    # from the keepalive timer. A producer task pulls items
                    # from the generator independently, so
                    # `anyio.fail_after` never wraps the generator's
                    # `__anext__` directly - avoiding CancelledError that
                    # would finalize the generator and also working for sync
                    # generators running in a thread pool.
                    #
                    # This context manager is entered on the request-scoped
                    # AsyncExitStack so its __aexit__ (which cancels the
                    # task group) is called by the exit stack after the
                    # streaming response completes — not by async generator
                    # finalization via GeneratorExit.
                    # Ref: https://peps.python.org/pep-0789/
                    send_stream, receive_stream = anyio.create_memory_object_stream[
                        bytes
                    ](max_buffer_size=1)

                    async def _producer() -> None:
                        async with send_stream:
                            async for raw_item in sse_aiter:
                                await send_stream.send(_serialize_sse_item(raw_item))

                    send_keepalive, receive_keepalive = (
                        anyio.create_memory_object_stream[bytes](max_buffer_size=1)
                    )

                    async def _keepalive_inserter() -> None:
                        """Read from the producer and forward to the output,
                        inserting keepalive comments on timeout."""
                        async with send_keepalive, receive_stream:
                            try:
                                while True:
                                    try:
                                        with anyio.fail_after(_PING_INTERVAL):
                                            data = await receive_stream.receive()
                                        await send_keepalive.send(data)
                                    except TimeoutError:
                                        await send_keepalive.send(KEEPALIVE_COMMENT)
                            except anyio.EndOfStream:
                                pass

                    async with anyio.create_task_group() as tg:
                        tg.start_soon(_producer)
                        tg.start_soon(_keepalive_inserter)
                        yield receive_keepalive
                        tg.cancel_scope.cancel()

                # Enter the SSE context manager on the request-scoped
                # exit stack. The stack outlives the streaming response,
                # so __aexit__ runs via proper structured teardown, not
                # via GeneratorExit thrown into an async generator.
                sse_receive_stream = await async_exit_stack.enter_async_context(
                    _sse_producer_cm()
                )
                # Ensure the receive stream is closed when the exit stack
                # unwinds, preventing ResourceWarning from __del__.
                async_exit_stack.push_async_callback(sse_receive_stream.aclose)

                async def _sse_with_checkpoints(
                    stream: ObjectReceiveStream[bytes],
                ) -> AsyncIterator[bytes]:
                    async for data in stream:
                        yield data
                        # Guarantee a checkpoint so cancellation can be
                        # delivered even when the producer is faster than
                        # the consumer and receive() never suspends.
                        await anyio.sleep(0)

                sse_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                    _sse_with_checkpoints(sse_receive_stream)
                )

                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = StreamingResponse(
                    sse_stream_content,
                    media_type="text/event-stream",
                    **response_args,
                )
                response.headers["Cache-Control"] = "no-cache"
                # For Nginx proxies to not buffer server sent events
                response.headers["X-Accel-Buffering"] = "no"
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif is_json_stream:
                # Generator endpoint: stream as JSONL
                gen = dependant.call(**solved_result.values)

                def _serialize_item(item: Any) -> bytes:
                    return _serialize_data(item) + b"\n"

                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_jsonl() -> AsyncIterator[bytes]:
                        async for item in gen:
                            yield _serialize_item(item)
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    jsonl_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                        _async_stream_jsonl()
                    )
                else:

                    def _sync_stream_jsonl() -> Iterator[bytes]:
                        for item in gen:  # ty: ignore[not-iterable]
                            yield _serialize_item(item)

                    jsonl_stream_content = _sync_stream_jsonl()

                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = StreamingResponse(
                    jsonl_stream_content,
                    media_type="application/jsonl",
                    **response_args,
                )
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif _is_async_gen_callable(dependant.call) or _is_gen_callable(
                dependant.call
            ):
                # Raw streaming with explicit response_class (e.g. StreamingResponse)
                gen = dependant.call(**solved_result.values)
                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_raw(
                        async_gen: AsyncIterator[Any],
                    ) -> AsyncIterator[Any]:
                        async for chunk in async_gen:
                            yield chunk
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    gen = _async_stream_raw(gen)
                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = actual_response_class(content=gen, **response_args)
                response.headers.raw.extend(solved_result.response.headers.raw)
            else:
                raw_response = await run_endpoint_function(
                    dependant=dependant,
                    values=solved_result.values,
                    is_coroutine=is_coroutine,
                )
                if isinstance(raw_response, Response):
                    if raw_response.background is None:
                        raw_response.background = solved_result.background_tasks
                    response = raw_response
                else:
                    response_args = _build_response_args(
                        status_code=status_code, solved_result=solved_result
                    )
                    # Use the fast path (dump_json) when no custom response
                    # class was set and a response field with a TypeAdapter
                    # exists. Serializes directly to JSON bytes via Pydantic's
                    # Rust core, skipping the intermediate Python dict +
                    # json.dumps() step.
                    use_dump_json = response_field is not None and isinstance(
                        response_class, DefaultPlaceholder
                    )
                    content = await serialize_response(
                        field=response_field,
                        response_content=raw_response,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                        is_coroutine=is_coroutine,
                        endpoint_ctx=endpoint_ctx,
                        dump_json=use_dump_json,
                    )
                    if use_dump_json:
                        response = Response(
                            content=content,
                            media_type="application/json",
                            **response_args,
                        )
                    else:
                        response = actual_response_class(content, **response_args)
                    if not is_body_allowed_for_status_code(response.status_code):
                        response.body = b""
                    response.headers.raw.extend(solved_result.response.headers.raw)
        if errors:
            validation_error = RequestValidationError(
                errors, body=body, endpoint_ctx=endpoint_ctx
            )
            raise validation_error

        # Return response
        assert response
        return response
```

### 🔹 函式: `get_request_handler()`
- **變更前簽章 (Before)**: `def get_request_handler( dependant: Dependant, body_field: ModelField | None = None, status_code: int | None = None, response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse), response_field: ModelField | None = None, response_model_include: IncEx | None = None, response_model_exclude: IncEx | None = None, response_model_by_alias: bool = True, response_model_exclude_unset: bool = False, response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False, dependency_overrides_provider: Any | None = None, embed_body_fields: bool = False, strict_content_type: bool | DefaultPlaceholder = Default(True), stream_item_field: ModelField | None = None, is_json_stream: bool = False, ) -> Callable[[Request], Coroutine[Any, Any, Response]]` (L373~L753)
- **變更後簽章 (After)**: `def get_request_handler( dependant: Dependant, body_field: ModelField | None = None, status_code: int | None = None, response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse), response_field: ModelField | None = None, response_model_include: IncEx | None = None, response_model_exclude: IncEx | None = None, response_model_by_alias: bool = True, response_model_exclude_unset: bool = False, response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False, dependency_overrides_provider: Any | None = None, embed_body_fields: bool = False, strict_content_type: bool | DefaultPlaceholder = Default(True), stream_item_field: ModelField | None = None, is_json_stream: bool = False, ) -> Callable[[Request], Coroutine[Any, Any, Response]]` (L373~L759)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def get_request_handler(
    dependant: Dependant,
    body_field: ModelField | None = None,
    status_code: int | None = None,
    response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse),
    response_field: ModelField | None = None,
    response_model_include: IncEx | None = None,
    response_model_exclude: IncEx | None = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    dependency_overrides_provider: Any | None = None,
    embed_body_fields: bool = False,
    strict_content_type: bool | DefaultPlaceholder = Default(True),
    stream_item_field: ModelField | None = None,
    is_json_stream: bool = False,
) -> Callable[[Request], Coroutine[Any, Any, Response]]:
    assert dependant.call is not None, "dependant.call must be a function"
    is_coroutine = _is_coroutine_callable(dependant.call)
    is_body_form = body_field and isinstance(body_field.field_info, params.Form)
    if isinstance(response_class, DefaultPlaceholder):
        actual_response_class: type[Response] = response_class.value
    else:
        actual_response_class = response_class
    is_sse_stream = lenient_issubclass(actual_response_class, EventSourceResponse)
    if isinstance(strict_content_type, DefaultPlaceholder):
        actual_strict_content_type: bool = strict_content_type.value
    else:
        actual_strict_content_type = strict_content_type

    async def app(request: Request) -> Response:
        response: Response | None = None
        file_stack = request.scope.get("fastapi_middleware_astack")
        assert isinstance(file_stack, AsyncExitStack), (
            "fastapi_middleware_astack not found in request scope"
        )

        # Extract endpoint context for error messages
        endpoint_ctx = (
            _extract_endpoint_context(dependant.call)
            if dependant.call
            else EndpointContext()
        )

        if dependant.path:
            # For mounted sub-apps, include the mount path prefix
            mount_path = request.scope.get("root_path", "").rstrip("/")
            endpoint_ctx["path"] = f"{request.method} {mount_path}{dependant.path}"

        # Read body and auto-close files
        try:
            body: Any = None
            if body_field:
                if is_body_form:
                    body = await request.form()
                    file_stack.push_async_callback(body.close)
                else:
                    body_bytes = await request.body()
                    if body_bytes:
                        json_body: Any = Undefined
                        content_type_value = request.headers.get("content-type")
                        if not content_type_value:
                            if not actual_strict_content_type:
                                json_body = await request.json()
                        else:
                            message = email.message.Message()
                            message["content-type"] = content_type_value
                            if message.get_content_maintype() == "application":
                                subtype = message.get_content_subtype()
                                if subtype == "json" or subtype.endswith("+json"):
                                    json_body = await request.json()
                        if json_body != Undefined:
                            body = json_body
                        else:
                            body = body_bytes
        except json.JSONDecodeError as e:
            validation_error = RequestValidationError(
                [
                    {
                        "type": "json_invalid",
                        "loc": ("body", e.pos),
                        "msg": "JSON decode error",
                        "input": {},
                        "ctx": {"error": e.msg},
                    }
                ],
                body=e.doc,
                endpoint_ctx=endpoint_ctx,
            )
            raise validation_error from e
        except HTTPException:
            # If a middleware raises an HTTPException, it should be raised again
            raise
        except Exception as e:
            http_error = HTTPException(
                status_code=400, detail="There was an error parsing the body"
            )
            raise http_error from e

        # Solve dependencies and run path operation function, auto-closing dependencies
        errors: list[Any] = []
        async_exit_stack = request.scope.get("fastapi_inner_astack")
        assert isinstance(async_exit_stack, AsyncExitStack), (
            "fastapi_inner_astack not found in request scope"
        )
        solved_result = await solve_dependencies(
            request=request,
            dependant=dependant,
            body=cast(dict[str, Any] | FormData | bytes | None, body),
            dependency_overrides_provider=dependency_overrides_provider,
            async_exit_stack=async_exit_stack,
            embed_body_fields=embed_body_fields,
        )
        errors = solved_result.errors
        assert dependant.call  # For types
        if not errors:
            # Shared serializer for stream items (JSONL and SSE).
            # Validates against stream_item_field when set, then
            # serializes to JSON bytes.
            def _serialize_data(data: Any) -> bytes:
                if stream_item_field:
                    value, errors_ = stream_item_field.validate(
                        data, {}, loc=("response",)
                    )
                    if errors_:
                        ctx = endpoint_ctx or EndpointContext()
                        raise ResponseValidationError(
                            errors=errors_,
                            body=data,
                            endpoint_ctx=ctx,
                        )
                    return stream_item_field.serialize_json(
                        value,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                    )
                else:
                    data = jsonable_encoder(data)
                    return json.dumps(data).encode("utf-8")

            if is_sse_stream:
                # Generator endpoint: stream as Server-Sent Events
                gen = dependant.call(**solved_result.values)

                def _serialize_sse_item(item: Any) -> bytes:
                    if isinstance(item, ServerSentEvent):
                        # User controls the event structure.
                        # Serialize the data payload if present.
                        # For ServerSentEvent items we skip stream_item_field
                        # validation (the user may mix types intentionally).
                        if item.raw_data is not None:
                            data_str: str | None = item.raw_data
                        elif item.data is not None:
                            if hasattr(item.data, "model_dump_json"):
                                data_str = item.data.model_dump_json()
                            else:
                                data_str = json.dumps(jsonable_encoder(item.data))
                        else:
                            data_str = None
                        return format_sse_event(
                            data_str=data_str,
                            event=item.event,
                            id=item.id,
                            retry=item.retry,
                            comment=item.comment,
                        )
                    else:
                        # Plain object: validate + serialize via
                        # stream_item_field (if set) and wrap in data field
                        return format_sse_event(
                            data_str=_serialize_data(item).decode("utf-8")
                        )

                if _is_async_gen_callable(dependant.call):
                    sse_aiter: AsyncIterator[Any] = gen.__aiter__()
                else:
                    sse_aiter = iterate_in_threadpool(gen)

                @asynccontextmanager
                async def _sse_producer_cm() -> AsyncIterator[
                    ObjectReceiveStream[bytes]
                ]:
                    # Use a memory stream to decouple generator iteration
                    # from the keepalive timer. A producer task pulls items
                    # from the generator independently, so
                    # `anyio.fail_after` never wraps the generator's
                    # `__anext__` directly - avoiding CancelledError that
                    # would finalize the generator and also working for sync
                    # generators running in a thread pool.
                    #
                    # This context manager is entered on the request-scoped
                    # AsyncExitStack so its __aexit__ (which cancels the
                    # task group) is called by the exit stack after the
                    # streaming response completes — not by async generator
                    # finalization via GeneratorExit.
                    # Ref: https://peps.python.org/pep-0789/
                    send_stream, receive_stream = anyio.create_memory_object_stream[
                        bytes
                    ](max_buffer_size=1)

                    async def _producer() -> None:
                        async with send_stream:
                            async for raw_item in sse_aiter:
                                await send_stream.send(_serialize_sse_item(raw_item))

                    send_keepalive, receive_keepalive = (
                        anyio.create_memory_object_stream[bytes](max_buffer_size=1)
                    )

                    async def _keepalive_inserter() -> None:
                        """Read from the producer and forward to the output,
                        inserting keepalive comments on timeout."""
                        async with send_keepalive, receive_stream:
                            try:
                                while True:
                                    try:
                                        with anyio.fail_after(_PING_INTERVAL):
                                            data = await receive_stream.receive()
                                        await send_keepalive.send(data)
                                    except TimeoutError:
                                        await send_keepalive.send(KEEPALIVE_COMMENT)
                            except anyio.EndOfStream:
                                pass

                    async with anyio.create_task_group() as tg:
                        tg.start_soon(_producer)
                        tg.start_soon(_keepalive_inserter)
                        yield receive_keepalive
                        tg.cancel_scope.cancel()

                # Enter the SSE context manager on the request-scoped
                # exit stack. The stack outlives the streaming response,
                # so __aexit__ runs via proper structured teardown, not
                # via GeneratorExit thrown into an async generator.
                sse_receive_stream = await async_exit_stack.enter_async_context(
                    _sse_producer_cm()
                )
                # Ensure the receive stream is closed when the exit stack
                # unwinds, preventing ResourceWarning from __del__.
                async_exit_stack.push_async_callback(sse_receive_stream.aclose)

                async def _sse_with_checkpoints(
                    stream: ObjectReceiveStream[bytes],
                ) -> AsyncIterator[bytes]:
                    async for data in stream:
                        yield data
                        # Guarantee a checkpoint so cancellation can be
                        # delivered even when the producer is faster than
                        # the consumer and receive() never suspends.
                        await anyio.sleep(0)

                sse_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                    _sse_with_checkpoints(sse_receive_stream)
                )

                response = StreamingResponse(
                    sse_stream_content,
                    media_type="text/event-stream",
                    background=solved_result.background_tasks,
                )
                response.headers["Cache-Control"] = "no-cache"
                # For Nginx proxies to not buffer server sent events
                response.headers["X-Accel-Buffering"] = "no"
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif is_json_stream:
                # Generator endpoint: stream as JSONL
                gen = dependant.call(**solved_result.values)

                def _serialize_item(item: Any) -> bytes:
                    return _serialize_data(item) + b"\n"

                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_jsonl() -> AsyncIterator[bytes]:
                        async for item in gen:
                            yield _serialize_item(item)
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    jsonl_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                        _async_stream_jsonl()
                    )
                else:

                    def _sync_stream_jsonl() -> Iterator[bytes]:
                        for item in gen:  # ty: ignore[not-iterable]
                            yield _serialize_item(item)

                    jsonl_stream_content = _sync_stream_jsonl()

                response = StreamingResponse(
                    jsonl_stream_content,
                    media_type="application/jsonl",
                    background=solved_result.background_tasks,
                )
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif _is_async_gen_callable(dependant.call) or _is_gen_callable(
                dependant.call
            ):
                # Raw streaming with explicit response_class (e.g. StreamingResponse)
                gen = dependant.call(**solved_result.values)
                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_raw(
                        async_gen: AsyncIterator[Any],
                    ) -> AsyncIterator[Any]:
                        async for chunk in async_gen:
                            yield chunk
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    gen = _async_stream_raw(gen)
                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = actual_response_class(content=gen, **response_args)
                response.headers.raw.extend(solved_result.response.headers.raw)
            else:
                raw_response = await run_endpoint_function(
                    dependant=dependant,
                    values=solved_result.values,
                    is_coroutine=is_coroutine,
                )
                if isinstance(raw_response, Response):
                    if raw_response.background is None:
                        raw_response.background = solved_result.background_tasks
                    response = raw_response
                else:
                    response_args = _build_response_args(
                        status_code=status_code, solved_result=solved_result
                    )
                    # Use the fast path (dump_json) when no custom response
                    # class was set and a response field with a TypeAdapter
                    # exists. Serializes directly to JSON bytes via Pydantic's
                    # Rust core, skipping the intermediate Python dict +
                    # json.dumps() step.
                    use_dump_json = response_field is not None and isinstance(
                        response_class, DefaultPlaceholder
                    )
                    content = await serialize_response(
                        field=response_field,
                        response_content=raw_response,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                        is_coroutine=is_coroutine,
                        endpoint_ctx=endpoint_ctx,
                        dump_json=use_dump_json,
                    )
                    if use_dump_json:
                        response = Response(
                            content=content,
                            media_type="application/json",
                            **response_args,
                        )
                    else:
                        response = actual_response_class(content, **response_args)
                    if not is_body_allowed_for_status_code(response.status_code):
                        response.body = b""
                    response.headers.raw.extend(solved_result.response.headers.raw)
        if errors:
            validation_error = RequestValidationError(
                errors, body=body, endpoint_ctx=endpoint_ctx
            )
            raise validation_error

        # Return response
        assert response
        return response

    return app
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def get_request_handler(
    dependant: Dependant,
    body_field: ModelField | None = None,
    status_code: int | None = None,
    response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse),
    response_field: ModelField | None = None,
    response_model_include: IncEx | None = None,
    response_model_exclude: IncEx | None = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    dependency_overrides_provider: Any | None = None,
    embed_body_fields: bool = False,
    strict_content_type: bool | DefaultPlaceholder = Default(True),
    stream_item_field: ModelField | None = None,
    is_json_stream: bool = False,
) -> Callable[[Request], Coroutine[Any, Any, Response]]:
    assert dependant.call is not None, "dependant.call must be a function"
    is_coroutine = _is_coroutine_callable(dependant.call)
    is_body_form = body_field and isinstance(body_field.field_info, params.Form)
    if isinstance(response_class, DefaultPlaceholder):
        actual_response_class: type[Response] = response_class.value
    else:
        actual_response_class = response_class
    is_sse_stream = lenient_issubclass(actual_response_class, EventSourceResponse)
    if isinstance(strict_content_type, DefaultPlaceholder):
        actual_strict_content_type: bool = strict_content_type.value
    else:
        actual_strict_content_type = strict_content_type

    async def app(request: Request) -> Response:
        response: Response | None = None
        file_stack = request.scope.get("fastapi_middleware_astack")
        assert isinstance(file_stack, AsyncExitStack), (
            "fastapi_middleware_astack not found in request scope"
        )

        # Extract endpoint context for error messages
        endpoint_ctx = (
            _extract_endpoint_context(dependant.call)
            if dependant.call
            else EndpointContext()
        )

        if dependant.path:
            # For mounted sub-apps, include the mount path prefix
            mount_path = request.scope.get("root_path", "").rstrip("/")
            endpoint_ctx["path"] = f"{request.method} {mount_path}{dependant.path}"

        # Read body and auto-close files
        try:
            body: Any = None
            if body_field:
                if is_body_form:
                    body = await request.form()
                    file_stack.push_async_callback(body.close)
                else:
                    body_bytes = await request.body()
                    if body_bytes:
                        json_body: Any = Undefined
                        content_type_value = request.headers.get("content-type")
                        if not content_type_value:
                            if not actual_strict_content_type:
                                json_body = await request.json()
                        else:
                            message = email.message.Message()
                            message["content-type"] = content_type_value
                            if message.get_content_maintype() == "application":
                                subtype = message.get_content_subtype()
                                if subtype == "json" or subtype.endswith("+json"):
                                    json_body = await request.json()
                        if json_body != Undefined:
                            body = json_body
                        else:
                            body = body_bytes
        except json.JSONDecodeError as e:
            validation_error = RequestValidationError(
                [
                    {
                        "type": "json_invalid",
                        "loc": ("body", e.pos),
                        "msg": "JSON decode error",
                        "input": {},
                        "ctx": {"error": e.msg},
                    }
                ],
                body=e.doc,
                endpoint_ctx=endpoint_ctx,
            )
            raise validation_error from e
        except HTTPException:
            # If a middleware raises an HTTPException, it should be raised again
            raise
        except Exception as e:
            http_error = HTTPException(
                status_code=400, detail="There was an error parsing the body"
            )
            raise http_error from e

        # Solve dependencies and run path operation function, auto-closing dependencies
        errors: list[Any] = []
        async_exit_stack = request.scope.get("fastapi_inner_astack")
        assert isinstance(async_exit_stack, AsyncExitStack), (
            "fastapi_inner_astack not found in request scope"
        )
        solved_result = await solve_dependencies(
            request=request,
            dependant=dependant,
            body=cast(dict[str, Any] | FormData | bytes | None, body),
            dependency_overrides_provider=dependency_overrides_provider,
            async_exit_stack=async_exit_stack,
            embed_body_fields=embed_body_fields,
        )
        errors = solved_result.errors
        assert dependant.call  # For types
        if not errors:
            # Shared serializer for stream items (JSONL and SSE).
            # Validates against stream_item_field when set, then
            # serializes to JSON bytes.
            def _serialize_data(data: Any) -> bytes:
                if stream_item_field:
                    value, errors_ = stream_item_field.validate(
                        data, {}, loc=("response",)
                    )
                    if errors_:
                        ctx = endpoint_ctx or EndpointContext()
                        raise ResponseValidationError(
                            errors=errors_,
                            body=data,
                            endpoint_ctx=ctx,
                        )
                    return stream_item_field.serialize_json(
                        value,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                    )
                else:
                    data = jsonable_encoder(data)
                    return json.dumps(data).encode("utf-8")

            if is_sse_stream:
                # Generator endpoint: stream as Server-Sent Events
                gen = dependant.call(**solved_result.values)

                def _serialize_sse_item(item: Any) -> bytes:
                    if isinstance(item, ServerSentEvent):
                        # User controls the event structure.
                        # Serialize the data payload if present.
                        # For ServerSentEvent items we skip stream_item_field
                        # validation (the user may mix types intentionally).
                        if item.raw_data is not None:
                            data_str: str | None = item.raw_data
                        elif item.data is not None:
                            if hasattr(item.data, "model_dump_json"):
                                data_str = item.data.model_dump_json()
                            else:
                                data_str = json.dumps(jsonable_encoder(item.data))
                        else:
                            data_str = None
                        return format_sse_event(
                            data_str=data_str,
                            event=item.event,
                            id=item.id,
                            retry=item.retry,
                            comment=item.comment,
                        )
                    else:
                        # Plain object: validate + serialize via
                        # stream_item_field (if set) and wrap in data field
                        return format_sse_event(
                            data_str=_serialize_data(item).decode("utf-8")
                        )

                if _is_async_gen_callable(dependant.call):
                    sse_aiter: AsyncIterator[Any] = gen.__aiter__()
                else:
                    sse_aiter = iterate_in_threadpool(gen)

                @asynccontextmanager
                async def _sse_producer_cm() -> AsyncIterator[
                    ObjectReceiveStream[bytes]
                ]:
                    # Use a memory stream to decouple generator iteration
                    # from the keepalive timer. A producer task pulls items
                    # from the generator independently, so
                    # `anyio.fail_after` never wraps the generator's
                    # `__anext__` directly - avoiding CancelledError that
                    # would finalize the generator and also working for sync
                    # generators running in a thread pool.
                    #
                    # This context manager is entered on the request-scoped
                    # AsyncExitStack so its __aexit__ (which cancels the
                    # task group) is called by the exit stack after the
                    # streaming response completes — not by async generator
                    # finalization via GeneratorExit.
                    # Ref: https://peps.python.org/pep-0789/
                    send_stream, receive_stream = anyio.create_memory_object_stream[
                        bytes
                    ](max_buffer_size=1)

                    async def _producer() -> None:
                        async with send_stream:
                            async for raw_item in sse_aiter:
                                await send_stream.send(_serialize_sse_item(raw_item))

                    send_keepalive, receive_keepalive = (
                        anyio.create_memory_object_stream[bytes](max_buffer_size=1)
                    )

                    async def _keepalive_inserter() -> None:
                        """Read from the producer and forward to the output,
                        inserting keepalive comments on timeout."""
                        async with send_keepalive, receive_stream:
                            try:
                                while True:
                                    try:
                                        with anyio.fail_after(_PING_INTERVAL):
                                            data = await receive_stream.receive()
                                        await send_keepalive.send(data)
                                    except TimeoutError:
                                        await send_keepalive.send(KEEPALIVE_COMMENT)
                            except anyio.EndOfStream:
                                pass

                    async with anyio.create_task_group() as tg:
                        tg.start_soon(_producer)
                        tg.start_soon(_keepalive_inserter)
                        yield receive_keepalive
                        tg.cancel_scope.cancel()

                # Enter the SSE context manager on the request-scoped
                # exit stack. The stack outlives the streaming response,
                # so __aexit__ runs via proper structured teardown, not
                # via GeneratorExit thrown into an async generator.
                sse_receive_stream = await async_exit_stack.enter_async_context(
                    _sse_producer_cm()
                )
                # Ensure the receive stream is closed when the exit stack
                # unwinds, preventing ResourceWarning from __del__.
                async_exit_stack.push_async_callback(sse_receive_stream.aclose)

                async def _sse_with_checkpoints(
                    stream: ObjectReceiveStream[bytes],
                ) -> AsyncIterator[bytes]:
                    async for data in stream:
                        yield data
                        # Guarantee a checkpoint so cancellation can be
                        # delivered even when the producer is faster than
                        # the consumer and receive() never suspends.
                        await anyio.sleep(0)

                sse_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                    _sse_with_checkpoints(sse_receive_stream)
                )

                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = StreamingResponse(
                    sse_stream_content,
                    media_type="text/event-stream",
                    **response_args,
                )
                response.headers["Cache-Control"] = "no-cache"
                # For Nginx proxies to not buffer server sent events
                response.headers["X-Accel-Buffering"] = "no"
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif is_json_stream:
                # Generator endpoint: stream as JSONL
                gen = dependant.call(**solved_result.values)

                def _serialize_item(item: Any) -> bytes:
                    return _serialize_data(item) + b"\n"

                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_jsonl() -> AsyncIterator[bytes]:
                        async for item in gen:
                            yield _serialize_item(item)
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    jsonl_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                        _async_stream_jsonl()
                    )
                else:

                    def _sync_stream_jsonl() -> Iterator[bytes]:
                        for item in gen:  # ty: ignore[not-iterable]
                            yield _serialize_item(item)

                    jsonl_stream_content = _sync_stream_jsonl()

                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = StreamingResponse(
                    jsonl_stream_content,
                    media_type="application/jsonl",
                    **response_args,
                )
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif _is_async_gen_callable(dependant.call) or _is_gen_callable(
                dependant.call
            ):
                # Raw streaming with explicit response_class (e.g. StreamingResponse)
                gen = dependant.call(**solved_result.values)
                if _is_async_gen_callable(dependant.call):

                    async def _async_stream_raw(
                        async_gen: AsyncIterator[Any],
                    ) -> AsyncIterator[Any]:
                        async for chunk in async_gen:
                            yield chunk
                            # To allow for cancellation to trigger
                            # Ref: https://github.com/fastapi/fastapi/issues/14680
                            await anyio.sleep(0)

                    gen = _async_stream_raw(gen)
                response_args = _build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = actual_response_class(content=gen, **response_args)
                response.headers.raw.extend(solved_result.response.headers.raw)
            else:
                raw_response = await run_endpoint_function(
                    dependant=dependant,
                    values=solved_result.values,
                    is_coroutine=is_coroutine,
                )
                if isinstance(raw_response, Response):
                    if raw_response.background is None:
                        raw_response.background = solved_result.background_tasks
                    response = raw_response
                else:
                    response_args = _build_response_args(
                        status_code=status_code, solved_result=solved_result
                    )
                    # Use the fast path (dump_json) when no custom response
                    # class was set and a response field with a TypeAdapter
                    # exists. Serializes directly to JSON bytes via Pydantic's
                    # Rust core, skipping the intermediate Python dict +
                    # json.dumps() step.
                    use_dump_json = response_field is not None and isinstance(
                        response_class, DefaultPlaceholder
                    )
                    content = await serialize_response(
                        field=response_field,
                        response_content=raw_response,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                        is_coroutine=is_coroutine,
                        endpoint_ctx=endpoint_ctx,
                        dump_json=use_dump_json,
                    )
                    if use_dump_json:
                        response = Response(
                            content=content,
                            media_type="application/json",
                            **response_args,
                        )
                    else:
                        response = actual_response_class(content, **response_args)
                    if not is_body_allowed_for_status_code(response.status_code):
                        response.body = b""
                    response.headers.raw.extend(solved_result.response.headers.raw)
        if errors:
            validation_error = RequestValidationError(
                errors, body=body, endpoint_ctx=endpoint_ctx
            )
            raise validation_error

        # Return response
        assert response
        return response

    return app
```


---

### 🔹 Commit #19: `12242c4f`
- **完整 Hash**: `12242c4fba71231440ed55ccb5bd10c3350c8465`
- **說明 (Ground Truth)**: 📝 Fix `format_sse_event` docstring rendering of `\n\n` terminator (#15613)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/sse.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:12, E:9, A:0) ➔ After(N:12, E:9, A:0)
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

### 🔹 Commit #20: `0f3e7bd6`
- **完整 Hash**: `0f3e7bd682a81488919227f2b5f1f7de1718ecdd`
- **說明 (Ground Truth)**: 🐛 Fix line splitting in `format_sse_event` to comply with SSE spec (#15515)
- **變更檔案數**: 1

#### 📄 檔案: `fastapi/sse.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:12, E:9, A:0) ➔ After(N:12, E:9, A:0)
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
  • + [新增節點] `_split_sse_lines` (FUNCTION_DEF)
  • - [移除節點] `splitlines (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `format_sse_event` ──[CALLS]──> `_split_sse_lines`
  • - [移除呼叫邊] `format_sse_event` ──[CALLS]──> `splitlines (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `format_sse_event()`
- **變更前簽章 (Before)**: `def format_sse_event( *, data_str: Annotated[ str | None, Doc( """ Pre-serialized data string to use as the `data:` field. """ ), ] = None, event: Annotated[ str | None, Doc( """ Optional event type name (`event:` field). """ ), ] = None, id: Annotated[ str | None, Doc( """ Optional event ID (`id:` field). """ ), ] = None, retry: Annotated[ int | None, Doc( """ Optional reconnection time in milliseconds (`retry:` field). """ ), ] = None, comment: Annotated[ str | None, Doc( """ Optional comment line(s) (`:` prefix). """ ), ] = None, ) -> bytes` (L159~L227)
- **變更後簽章 (After)**: `def format_sse_event( *, data_str: Annotated[ str | None, Doc( """ Pre-serialized data string to use as the `data:` field. """ ), ] = None, event: Annotated[ str | None, Doc( """ Optional event type name (`event:` field). """ ), ] = None, id: Annotated[ str | None, Doc( """ Optional event ID (`id:` field). """ ), ] = None, retry: Annotated[ int | None, Doc( """ Optional reconnection time in milliseconds (`retry:` field). """ ), ] = None, comment: Annotated[ str | None, Doc( """ Optional comment line(s) (`:` prefix). """ ), ] = None, ) -> bytes` (L165~L233)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def format_sse_event(
    *,
    data_str: Annotated[
        str | None,
        Doc(
            """
            Pre-serialized data string to use as the `data:` field.
            """
        ),
    ] = None,
    event: Annotated[
        str | None,
        Doc(
            """
            Optional event type name (`event:` field).
            """
        ),
    ] = None,
    id: Annotated[
        str | None,
        Doc(
            """
            Optional event ID (`id:` field).
            """
        ),
    ] = None,
    retry: Annotated[
        int | None,
        Doc(
            """
            Optional reconnection time in milliseconds (`retry:` field).
            """
        ),
    ] = None,
    comment: Annotated[
        str | None,
        Doc(
            """
            Optional comment line(s) (`:` prefix).
            """
        ),
    ] = None,
) -> bytes:
    """Build SSE wire-format bytes from **pre-serialized** data.

    The result always ends with `\n\n` (the event terminator).
    """
    lines: list[str] = []

    if comment is not None:
        for line in comment.splitlines():
            lines.append(f": {line}")

    if event is not None:
        lines.append(f"event: {event}")

    if data_str is not None:
        for line in data_str.splitlines():
            lines.append(f"data: {line}")

    if id is not None:
        lines.append(f"id: {id}")

    if retry is not None:
        lines.append(f"retry: {retry}")

    lines.append("")
    lines.append("")
    return "\n".join(lines).encode("utf-8")
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def format_sse_event(
    *,
    data_str: Annotated[
        str | None,
        Doc(
            """
            Pre-serialized data string to use as the `data:` field.
            """
        ),
    ] = None,
    event: Annotated[
        str | None,
        Doc(
            """
            Optional event type name (`event:` field).
            """
        ),
    ] = None,
    id: Annotated[
        str | None,
        Doc(
            """
            Optional event ID (`id:` field).
            """
        ),
    ] = None,
    retry: Annotated[
        int | None,
        Doc(
            """
            Optional reconnection time in milliseconds (`retry:` field).
            """
        ),
    ] = None,
    comment: Annotated[
        str | None,
        Doc(
            """
            Optional comment line(s) (`:` prefix).
            """
        ),
    ] = None,
) -> bytes:
    """Build SSE wire-format bytes from **pre-serialized** data.

    The result always ends with `\n\n` (the event terminator).
    """
    lines: list[str] = []

    if comment is not None:
        for line in _split_sse_lines(comment):
            lines.append(f": {line}")

    if event is not None:
        lines.append(f"event: {event}")

    if data_str is not None:
        for line in _split_sse_lines(data_str):
            lines.append(f"data: {line}")

    if id is not None:
        lines.append(f"id: {id}")

    if retry is not None:
        lines.append(f"retry: {retry}")

    lines.append("")
    lines.append("")
    return "\n".join(lines).encode("utf-8")
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/fastapi show 0890e2a32960bb5cc1cfb807dca3a5e10384ec9d
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 0890e2a32960bb5cc1cfb807dca3a5e10384ec9d~1 --file test_repos/fastapi/fastapi/dependencies/utils.py
   ```
