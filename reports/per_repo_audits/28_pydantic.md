# 🔬 CODE-Map 基準審查獨立驗證報告: `pydantic`
> **技術生態**: `Python (資料驗證 / 核心模型裝飾器)`  
> **本地倉庫路徑**: `test_repos/pydantic`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 23 Files  
> **報告生成時間**: 2026-10-20 21:43:55  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `8` / `23` | `34.8%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `11` / `23` | `47.8%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `4` / `23` | `17.4%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`19` / `23`** | **`82.6%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `23` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `834e800c`
- **完整 Hash**: `834e800cda72c264a1476d25dfbf892a9a2614ef`
- **說明 (Ground Truth)**: Fix mypy plugin crash on deferred empty model (#14027)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/mypy.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:124, E:172, A:0) ➔ After(N:124, E:172, A:0)
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

### 🔹 函式: `PydanticModelTransformer.transform()`
- **變更前簽章 (Before)**: `def transform(self) -> bool` (L521~L566)
- **變更後簽章 (After)**: `def transform(self) -> bool` (L521~L570)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def transform(self) -> bool:
        """Configures the BaseModel subclass according to the plugin settings.

        In particular:

        * determines the model config and fields,
        * adds a fields-aware signature for the initializer and construct methods
        * freezes the class if frozen = True
        * stores the fields, config, and if the class is settings in the mypy metadata for access by subclasses
        """
        info = self._cls.info
        # Tag the class as being processed by the plugin. This is used to detect base classes
        # that are Pydantic models for which the plugin hasn't completed processing yet (in which
        # case the `METADATA_KEY` is not yet present in the metadata):
        info.metadata.setdefault(METADATA_TAG_KEY, {})
        is_a_root_model = is_root_model(info)
        config = self.collect_config()
        fields, class_vars = self.collect_fields_and_class_vars(config, is_a_root_model)
        if fields is None or class_vars is None:
            # Some definitions are not ready. We need another pass.
            if not self._api.final_iteration:
                self._api.defer()
            return False
        for field in fields:
            if field.type is None or has_placeholder(field.type):
                # The field type may contain placeholders, e.g. when inheriting from a generic
                # model parametrized with a forward reference to the class being defined.
                # Request another pass so that they can be resolved:
                if not self._api.final_iteration:
                    self._api.defer()
                return False

        is_settings = info.has_base(BASESETTINGS_FULLNAME)
        self.add_initializer(fields, config, is_settings, is_a_root_model)
        self.add_model_construct_method(fields, config, is_settings, is_a_root_model)
        self.set_frozen(fields, self._api, frozen=config.frozen is True)

        self.adjust_decorator_signatures()

        info.metadata[METADATA_KEY] = {
            'fields': {field.name: field.serialize() for field in fields},
            'class_vars': {class_var.name: class_var.serialize() for class_var in class_vars},
            'config': config.get_values_dict(),
        }

        return True
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def transform(self) -> bool:
        """Configures the BaseModel subclass according to the plugin settings.

        In particular:

        * determines the model config and fields,
        * adds a fields-aware signature for the initializer and construct methods
        * freezes the class if frozen = True
        * stores the fields, config, and if the class is settings in the mypy metadata for access by subclasses
        """
        info = self._cls.info
        # Tag the class as being processed by the plugin. This is used to detect base classes
        # that are Pydantic models for which the plugin hasn't completed processing yet (in which
        # case the `METADATA_KEY` is not yet present in the metadata):
        info.metadata.setdefault(METADATA_TAG_KEY, {})
        is_a_root_model = is_root_model(info)
        config = self.collect_config()
        fields, class_vars = self.collect_fields_and_class_vars(config, is_a_root_model)
        if fields is None or class_vars is None:
            # Some definitions are not ready. We need another pass.
            if not self._api.final_iteration:
                self._api.defer()
            return False
        for field in fields:
            if field.type is None or has_placeholder(field.type):
                # The field type may contain placeholders, e.g. when inheriting from a generic
                # model parametrized with a forward reference to the class being defined.
                # Request another pass so that they can be resolved:
                if not self._api.final_iteration:
                    self._api.defer()
                return False
        for tv in info.defn.type_vars:
            if has_placeholder(tv) and not self._api.final_iteration:
                self._api.defer()
                return False

        is_settings = info.has_base(BASESETTINGS_FULLNAME)
        self.add_initializer(fields, config, is_settings, is_a_root_model)
        self.add_model_construct_method(fields, config, is_settings, is_a_root_model)
        self.set_frozen(fields, self._api, frozen=config.frozen is True)

        self.adjust_decorator_signatures()

        info.metadata[METADATA_KEY] = {
            'fields': {field.name: field.serialize() for field in fields},
            'class_vars': {class_var.name: class_var.serialize() for class_var in class_vars},
            'config': config.get_values_dict(),
        }

        return True
```


---

### 🔹 Commit #02: `5adfeaaa`
- **完整 Hash**: `5adfeaaaea947f81f0f01868604f219084ec151a`
- **說明 (Ground Truth)**: Add pre-commit hook to prevent invisible Unicode characters (#14008)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/main.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:142, E:185, A:0) ➔ After(N:142, E:185, A:0)
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

### 🔹 Commit #03: `900e8991`
- **完整 Hash**: `900e8991b7bf066a0d44346636c43b371608d8cf`
- **說明 (Ground Truth)**: Copy private attributes when making root model shallow copies (#13989)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/root_model.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:21, E:19, A:0) ➔ After(N:21, E:19, A:0)
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

### 🔹 函式: `RootModel.__copy__()`
- **變更前簽章 (Before)**: `def __copy__(self) -> Self` (L100~L108)
- **變更後簽章 (After)**: `def __copy__(self) -> Self` (L100~L114)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __copy__(self) -> Self:
        """Returns a shallow copy of the model."""
        cls = type(self)
        m = cls.__new__(cls)
        new_dict = copy(self.__dict__)
        new_dict['root'] = copy(self.__dict__['root'])  # pyright: ignore[reportIndexIssue] (https://github.com/microsoft/pyright/issues/11548)
        _object_setattr(m, '__dict__', new_dict)
        _object_setattr(m, '__pydantic_fields_set__', copy(self.__pydantic_fields_set__))
        return m
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __copy__(self) -> Self:
        """Returns a shallow copy of the model."""
        cls = type(self)
        m = cls.__new__(cls)
        new_dict = copy(self.__dict__)
        new_dict['root'] = copy(self.__dict__['root'])  # pyright: ignore[reportIndexIssue] (https://github.com/microsoft/pyright/issues/11548)
        # Private attributes live in `__dict__` on root models, so give the copy its own:
        private = new_dict.get('__pydantic_private__')
        if private is not None:
            new_dict['__pydantic_private__'] = {  # pyright: ignore[reportIndexIssue] (https://github.com/microsoft/pyright/issues/11548)
                k: v for k, v in private.items() if v is not PydanticUndefined
            }
        _object_setattr(m, '__dict__', new_dict)
        _object_setattr(m, '__pydantic_fields_set__', copy(self.__pydantic_fields_set__))
        return m
```


---

### 🔹 Commit #04: `03de65fc`
- **完整 Hash**: `03de65fc2f44faa4b32e05ce0a5d499cdf38f89b`
- **說明 (Ground Truth)**: Improve performance of `JsonValue` Python serialization (#13995)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/types.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:182, E:189, A:0) ➔ After(N:183, E:190, A:0)
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
  • + [新增節點] `simple_ser_schema (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `_AllowAnyJson.__get_pydantic_core_schema__` ──[CALLS]──> `simple_ser_schema (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_AllowAnyJson.__get_pydantic_core_schema__()`
- **變更前簽章 (Before)**: `def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema` (L3235~L3237)
- **變更後簽章 (After)**: `def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema` (L3235~L3243)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        python_schema = handler(source_type)
        return core_schema.json_or_python_schema(json_schema=core_schema.any_schema(), python_schema=python_schema)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        python_schema = handler(source_type)
        return core_schema.json_or_python_schema(
            json_schema=core_schema.any_schema(),
            python_schema=python_schema,
            # Valid JSON values are serialized identically by inference, which avoids the overhead
            # of the tagged union serializer (and its Python discriminator function) in Python mode:
            serialization=core_schema.simple_ser_schema('any'),
        )
```


---

### 🔹 Commit #05: `e1ca3322`
- **完整 Hash**: `e1ca33220585e8f745000eff4b067e04fe7d83e9`
- **說明 (Ground Truth)**: Fix unpickling of generic classes defined in separate module (#13994)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/_internal/_generics.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:64, E:73, A:0) ➔ After(N:64, E:73, A:0)
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

### 🔹 函式: `create_generic_submodel()`
- **變更前簽章 (Before)**: `def create_generic_submodel( model_name: str, origin: type[BaseModel], args: tuple[Any, ...], params: tuple[Any, ...] ) -> type[BaseModel]` (L104~L161)
- **變更後簽章 (After)**: `def create_generic_submodel( model_name: str, origin: type[BaseModel], args: tuple[Any, ...], params: tuple[Any, ...] ) -> type[BaseModel]` (L104~L164)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def create_generic_submodel(
    model_name: str, origin: type[BaseModel], args: tuple[Any, ...], params: tuple[Any, ...]
) -> type[BaseModel]:
    """Dynamically create a submodel of a provided (generic) BaseModel.

    This is used when producing concrete parametrizations of generic models. This function
    only *creates* the new subclass; the schema/validators/serialization must be updated to
    reflect a concrete parametrization elsewhere.

    Args:
        model_name: The name of the newly created model.
        origin: The base class for the new model to inherit from.
        args: A tuple of generic metadata arguments.
        params: A tuple of generic metadata parameters.

    Returns:
        The created submodel.
    """
    namespace: dict[str, Any] = {'__module__': origin.__module__}
    # As per https://docs.python.org/3/reference/datamodel.html#slots:
    # "The action of a __slots__ declaration is not limited to the class where it is defined.
    # __slots__ declared in parents are available in child classes. However, instances of a
    # child subclass will get a __dict__ and __weakref__ unless the subclass also defines
    # __slots__".
    # Because when users parameterize a generic model, we create a subclass of such generic model
    # (what happens in this function), they can't control the fact that no slots is defined on the
    # dynamic subclass, and so even if they defined extra __slots__ on the generic class (which results
    # in the class *not* being weakref-able), the parameterized class *will* be weakref-able.
    # For this reason (and to make Pydantic generic models behavior closer to generic aliases),
    # we forward any slots from the origin:
    if '__slots__' in origin.__dict__:
        namespace['__slots__'] = origin.__dict__['__slots__']
    bases = (origin,)
    meta, ns, kwds = prepare_class(model_name, bases)
    namespace.update(ns)
    created_model = meta(
        model_name,
        bases,
        namespace,
        __pydantic_generic_metadata__={
            'origin': origin,
            'args': args,
            'parameters': params,
        },
        __pydantic_reset_parent_namespace__=False,
        **kwds,
    )

    model_module, called_globally = _get_caller_frame_info(depth=3)
    if called_globally:  # create global reference and therefore allow pickling
        object_by_reference = None
        reference_name = model_name
        reference_module_globals = sys.modules[model_module or created_model.__module__].__dict__
        while object_by_reference is not created_model:
            object_by_reference = reference_module_globals.setdefault(reference_name, created_model)
            reference_name += '_'

    return created_model
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def create_generic_submodel(
    model_name: str, origin: type[BaseModel], args: tuple[Any, ...], params: tuple[Any, ...]
) -> type[BaseModel]:
    """Dynamically create a submodel of a provided (generic) BaseModel.

    This is used when producing concrete parametrizations of generic models. This function
    only *creates* the new subclass; the schema/validators/serialization must be updated to
    reflect a concrete parametrization elsewhere.

    Args:
        model_name: The name of the newly created model.
        origin: The base class for the new model to inherit from.
        args: A tuple of generic metadata arguments.
        params: A tuple of generic metadata parameters.

    Returns:
        The created submodel.
    """
    model_module, called_globally = _get_caller_frame_info(depth=3)
    # If parametrized at the module level, the parametrized class is registered in this module (see below).
    # Its `__module__` must match. We fall back to the module of the origin for backwards compatibility reasons.
    module = model_module if called_globally and model_module is not None else origin.__module__
    namespace: dict[str, Any] = {'__module__': module}
    # As per https://docs.python.org/3/reference/datamodel.html#slots:
    # "The action of a __slots__ declaration is not limited to the class where it is defined.
    # __slots__ declared in parents are available in child classes. However, instances of a
    # child subclass will get a __dict__ and __weakref__ unless the subclass also defines
    # __slots__".
    # Because when users parameterize a generic model, we create a subclass of such generic model
    # (what happens in this function), they can't control the fact that no slots is defined on the
    # dynamic subclass, and so even if they defined extra __slots__ on the generic class (which results
    # in the class *not* being weakref-able), the parameterized class *will* be weakref-able.
    # For this reason (and to make Pydantic generic models behavior closer to generic aliases),
    # we forward any slots from the origin:
    if '__slots__' in origin.__dict__:
        namespace['__slots__'] = origin.__dict__['__slots__']
    bases = (origin,)
    meta, ns, kwds = prepare_class(model_name, bases)
    namespace.update(ns)
    created_model = meta(
        model_name,
        bases,
        namespace,
        __pydantic_generic_metadata__={
            'origin': origin,
            'args': args,
            'parameters': params,
        },
        __pydantic_reset_parent_namespace__=False,
        **kwds,
    )

    if called_globally:  # create global reference and therefore allow pickling
        object_by_reference = None
        reference_name = model_name
        reference_module_globals = sys.modules[module].__dict__
        while object_by_reference is not created_model:
            object_by_reference = reference_module_globals.setdefault(reference_name, created_model)
            reference_name += '_'

    return created_model
```


---

### 🔹 Commit #06: `141c1e3d`
- **完整 Hash**: `141c1e3df86e1b3f4bfe908fb89ac860e8ba7c0c`
- **說明 (Ground Truth)**: Fix JSON Schema cache key mismatch with nested `json_schema_mode_override` (#13980)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/json_schema.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:219, E:327, A:0) ➔ After(N:220, E:332, A:0)
- **差分統計**: +Nodes: 8, -Nodes: 7, +Edges: 35, -Edges: 30, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `GenerateJsonSchema.handler_func` (FUNCTION_DEF)
  • + [新增節點] `GenerateJsonSchema.new_handler_func` (FUNCTION_DEF)
  • + [新增節點] `GenerateJsonSchema._generate_inner` (FUNCTION_DEF)
  • + [新增節點] `GenerateJsonSchema.js_updates_handler_func` (FUNCTION_DEF)
  • + [新增節點] `GenerateJsonSchema.js_extra_handler_func` (FUNCTION_DEF)
  • + [新增節點] `GenerateJsonSchema.new_handler_func` (FUNCTION_DEF)
  • + [新增節點] `GenerateJsonSchema.populate_defs` (FUNCTION_DEF)
  • + [新增節點] `_get_class_config` (FUNCTION_DEF)
  • - [移除節點] `GenerateJsonSchema.handler_func` (FUNCTION_DEF)
  • - [移除節點] `GenerateJsonSchema.js_updates_handler_func` (FUNCTION_DEF)
  • - [移除節點] `_get_typed_dict_config` (FUNCTION_DEF)
  • - [移除節點] `GenerateJsonSchema.new_handler_func` (FUNCTION_DEF)
  • - [移除節點] `GenerateJsonSchema.js_extra_handler_func` (FUNCTION_DEF)
  • - [移除節點] `GenerateJsonSchema.populate_defs` (FUNCTION_DEF)
  • - [移除節點] `GenerateJsonSchema.new_handler_func` (FUNCTION_DEF)
  • _... 以及其餘 65 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `GenerateJsonSchema.typed_dict_schema()`
- **變更前簽章 (Before)**: `def typed_dict_schema(self, schema: core_schema.TypedDictSchema) -> JsonSchemaValue` (L1599~L1648)
- **變更後簽章 (After)**: `def typed_dict_schema(self, schema: core_schema.TypedDictSchema) -> JsonSchemaValue` (L1607~L1656)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def typed_dict_schema(self, schema: core_schema.TypedDictSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that defines a typed dict.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """
        total = schema.get('total', True)
        named_required_fields: list[tuple[str, bool, CoreSchemaField]] = [
            (name, self.field_is_required(field, total), field)
            for name, field in schema['fields'].items()
            if self.field_is_present(field)
        ]
        if self.mode == 'serialization':
            named_required_fields.extend(self._name_required_computed_fields(schema.get('computed_fields', [])))
        cls = schema.get('cls')
        config = _get_typed_dict_config(cls)
        with self._config_wrapper_stack.push(config):
            json_schema = self._named_required_fields_schema(named_required_fields)

        # There's some duplication between `extra_behavior` and
        # the config's `extra`/core config's `extra_fields_behavior`.
        # However, it is common to manually create TypedDictSchemas,
        # where you don't necessarily have a class.
        # At runtime, `extra_behavior` takes priority over the config
        # for validation, so follow the same for the JSON Schema:
        if 'extras_schema' in schema and schema['extras_schema'] != core_schema.any_schema():
            allow_additional_props = self.generate_inner(schema['extras_schema'])
        else:
            allow_additional_props = True

        if schema.get('extra_behavior') == 'forbid':
            json_schema['additionalProperties'] = False
        elif schema.get('extra_behavior') == 'allow':
            json_schema['additionalProperties'] = allow_additional_props

        if cls is not None:
            # `_update_class_schema()` will not override
            # `additionalProperties` if already present:
            self._update_class_schema(json_schema, cls, config or {})
        elif 'additionalProperties' not in json_schema:
            extra = schema.get('config', {}).get('extra_fields_behavior')
            if extra == 'forbid':
                json_schema['additionalProperties'] = False
            elif extra == 'allow':
                json_schema['additionalProperties'] = allow_additional_props

        return json_schema
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def typed_dict_schema(self, schema: core_schema.TypedDictSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that defines a typed dict.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """
        total = schema.get('total', True)
        named_required_fields: list[tuple[str, bool, CoreSchemaField]] = [
            (name, self.field_is_required(field, total), field)
            for name, field in schema['fields'].items()
            if self.field_is_present(field)
        ]
        if self.mode == 'serialization':
            named_required_fields.extend(self._name_required_computed_fields(schema.get('computed_fields', [])))
        cls = schema.get('cls')
        config = _get_class_config(schema)
        with self._config_wrapper_stack.push(config):
            json_schema = self._named_required_fields_schema(named_required_fields)

        # There's some duplication between `extra_behavior` and
        # the config's `extra`/core config's `extra_fields_behavior`.
        # However, it is common to manually create TypedDictSchemas,
        # where you don't necessarily have a class.
        # At runtime, `extra_behavior` takes priority over the config
        # for validation, so follow the same for the JSON Schema:
        if 'extras_schema' in schema and schema['extras_schema'] != core_schema.any_schema():
            allow_additional_props = self.generate_inner(schema['extras_schema'])
        else:
            allow_additional_props = True

        if schema.get('extra_behavior') == 'forbid':
            json_schema['additionalProperties'] = False
        elif schema.get('extra_behavior') == 'allow':
            json_schema['additionalProperties'] = allow_additional_props

        if cls is not None:
            # `_update_class_schema()` will not override
            # `additionalProperties` if already present:
            self._update_class_schema(json_schema, cls, config or {})
        elif 'additionalProperties' not in json_schema:
            extra = schema.get('config', {}).get('extra_fields_behavior')
            if extra == 'forbid':
                json_schema['additionalProperties'] = False
            elif extra == 'allow':
                json_schema['additionalProperties'] = allow_additional_props

        return json_schema
```

### 🔹 函式: `GenerateJsonSchema.dataclass_schema()`
- **變更前簽章 (Before)**: `def dataclass_schema(self, schema: core_schema.DataclassSchema) -> JsonSchemaValue` (L1960~L1985)
- **變更後簽章 (After)**: `def dataclass_schema(self, schema: core_schema.DataclassSchema) -> JsonSchemaValue` (L1968~L1992)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def dataclass_schema(self, schema: core_schema.DataclassSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that defines a dataclass.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """

        cls = schema['cls']
        # If (stdlib) dataclass doesn't have config, the parent's config is used (as during core schema generation):
        config = cast('ConfigDict | None', getattr(cls, '__pydantic_config__', None))

        with self._config_wrapper_stack.push(config):
            json_schema = self.generate_inner(schema['schema']).copy()

        # Only the parent's `extra` config value is relevant to the class schema. It is propagated
        # to the core config (and used for validation), so we reuse it:
        class_config = config or {}
        if 'extra' not in class_config and (extra := schema.get('config', {}).get('extra_fields_behavior')) is not None:
            class_config = cast('ConfigDict', {**class_config, 'extra': extra})

        self._update_class_schema(json_schema, cls, class_config)

        return json_schema
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def dataclass_schema(self, schema: core_schema.DataclassSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that defines a dataclass.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """

        cls = schema['cls']
        config = _get_class_config(schema)

        with self._config_wrapper_stack.push(config):
            json_schema = self.generate_inner(schema['schema']).copy()

        # Only the parent's `extra` config value is relevant to the class schema. It is propagated
        # to the core config (and used for validation), so we reuse it:
        class_config = config or {}
        if 'extra' not in class_config and (extra := schema.get('config', {}).get('extra_fields_behavior')) is not None:
            class_config = cast('ConfigDict', {**class_config, 'extra': extra})

        self._update_class_schema(json_schema, cls, class_config)

        return json_schema
```

### 🔹 函式: `GenerateJsonSchema.generate_inner()`
- **變更前簽章 (Before)**: `def generate_inner(self, schema: CoreSchemaOrField) -> JsonSchemaValue: # noqa: C901` (L448~L586)
- **變更後簽章 (After)**: `def generate_inner(self, schema: CoreSchemaOrField) -> JsonSchemaValue` (L448~L462)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def generate_inner(self, schema: CoreSchemaOrField) -> JsonSchemaValue:  # noqa: C901
        """Generates a JSON schema for a given core schema.

        Args:
            schema: The given core schema.

        Returns:
            The generated JSON schema.

        TODO: the nested function definitions here seem like bad practice, I'd like to unpack these
        in a future PR. It'd be great if we could shorten the call stack a bit for JSON schema generation,
        and I think there's potential for that here.
        """
        # If a schema with the same CoreRef has been handled, just return a reference to it
        # Note that this assumes that it will _never_ be the case that the same CoreRef is used
        # on types that should have different JSON schemas
        if 'ref' in schema:
            core_ref = CoreRef(schema['ref'])  # type: ignore[typeddict-item]
            core_mode_ref = (core_ref, self.mode)
            if core_mode_ref in self.core_to_defs_refs and self.core_to_defs_refs[core_mode_ref] in self.definitions:
                return {'$ref': self.core_to_json_refs[core_mode_ref]}

        def populate_defs(core_schema: CoreSchema, json_schema: JsonSchemaValue) -> JsonSchemaValue:
            if 'ref' in core_schema:
                core_ref = CoreRef(core_schema['ref'])  # type: ignore[typeddict-item]
                defs_ref, ref_json_schema = self.get_cache_defs_ref_schema(core_ref)
                json_ref = JsonRef(ref_json_schema['$ref'])
                # Replace the schema if it's not a reference to itself
                # What we want to avoid is having the def be just a ref to itself
                # which is what would happen if we blindly assigned any
                if json_schema.get('$ref', None) != json_ref:
                    self.definitions[defs_ref] = json_schema
                    self._core_defs_invalid_for_json_schema.pop(defs_ref, None)
                json_schema = ref_json_schema
            return json_schema

        def handler_func(schema_or_field: CoreSchemaOrField) -> JsonSchemaValue:
            """Generate a JSON schema based on the input schema.

            Args:
                schema_or_field: The core schema to generate a JSON schema from.

            Returns:
                The generated JSON schema.

            Raises:
                TypeError: If an unexpected schema type is encountered.
            """
            # Generate the core-schema-type-specific bits of the schema generation:
            json_schema: JsonSchemaValue | None = None
            if self.mode == 'serialization' and 'serialization' in schema_or_field:
                # In this case, we skip the JSON Schema generation of the schema
                # and use the `'serialization'` schema instead (canonical example:
                # `Annotated[int, PlainSerializer(str)]`).
                ser_schema = schema_or_field['serialization']  # type: ignore
                json_schema = self.ser_schema(ser_schema)

                # It might be that the 'serialization'` is skipped depending on `when_used`.
                # This is only relevant for `nullable` schemas though, so we special case here.
                if (
                    json_schema is not None
                    and ser_schema.get('when_used') in ('unless-none', 'json-unless-none')
                    and schema_or_field['type'] == 'nullable'
                ):
                    json_schema = self.get_union_of_schemas([{'type': 'null'}, json_schema])
            if json_schema is None:
                if _core_utils.is_core_schema(schema_or_field) or _core_utils.is_core_schema_field(schema_or_field):
                    generate_for_schema_type = self._schema_type_to_method[schema_or_field['type']]
                    json_schema = generate_for_schema_type(schema_or_field)
                else:
                    raise TypeError(f'Unexpected schema type: schema={schema_or_field}')
            return json_schema

        current_handler = _schema_generation_shared.GenerateJsonSchemaHandler(self, handler_func)

        metadata = cast(_core_metadata.CoreMetadata, schema.get('metadata', {}))

        # TODO: I dislike that we have to wrap these basic dict updates in callables, is there any way around this?

        if js_updates := metadata.get('pydantic_js_updates'):

            def js_updates_handler_func(
                schema_or_field: CoreSchemaOrField,
                current_handler: GetJsonSchemaHandler = current_handler,
            ) -> JsonSchemaValue:
                json_schema = {**current_handler(schema_or_field), **js_updates}
                return json_schema

            current_handler = _schema_generation_shared.GenerateJsonSchemaHandler(self, js_updates_handler_func)

        if js_extra := metadata.get('pydantic_js_extra'):

            def js_extra_handler_func(
                schema_or_field: CoreSchemaOrField,
                current_handler: GetJsonSchemaHandler = current_handler,
            ) -> JsonSchemaValue:
                json_schema = current_handler(schema_or_field)
                if isinstance(js_extra, dict):
                    json_schema.update(to_jsonable_python(js_extra))
                elif callable(js_extra):
                    # similar to typing issue in _update_class_schema when we're working with callable js extra
                    js_extra(json_schema)  # type: ignore
                return json_schema

            current_handler = _schema_generation_shared.GenerateJsonSchemaHandler(self, js_extra_handler_func)

        for js_modify_function in metadata.get('pydantic_js_functions', ()):

            def new_handler_func(
                schema_or_field: CoreSchemaOrField,
                current_handler: GetJsonSchemaHandler = current_handler,
                js_modify_function: GetJsonSchemaFunction = js_modify_function,
            ) -> JsonSchemaValue:
                json_schema = js_modify_function(schema_or_field, current_handler)
                if _core_utils.is_core_schema(schema_or_field):
                    json_schema = populate_defs(schema_or_field, json_schema)
                original_schema = current_handler.resolve_ref_schema(json_schema)
                ref = json_schema.pop('$ref', None)
                if ref and json_schema:
                    original_schema.update(json_schema)
                return original_schema

            current_handler = _schema_generation_shared.GenerateJsonSchemaHandler(self, new_handler_func)

        for js_modify_function in metadata.get('pydantic_js_annotation_functions', ()):

            def new_handler_func(
                schema_or_field: CoreSchemaOrField,
                current_handler: GetJsonSchemaHandler = current_handler,
                js_modify_function: GetJsonSchemaFunction = js_modify_function,
            ) -> JsonSchemaValue:
                return js_modify_function(schema_or_field, current_handler)

            current_handler = _schema_generation_shared.GenerateJsonSchemaHandler(self, new_handler_func)

        json_schema = current_handler(schema)
        if _core_utils.is_core_schema(schema):
            json_schema = populate_defs(schema, json_schema)
        return json_schema
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def generate_inner(self, schema: CoreSchemaOrField) -> JsonSchemaValue:
        """Generates a JSON schema for a given core schema.

        Args:
            schema: The given core schema.

        Returns:
            The generated JSON schema.
        """
        if schema['type'] in ('model', 'dataclass', 'typed-dict'):
            # The class config (and in particular `json_schema_mode_override`) must be pushed *before*
            # the definitions cache lookup, so that the JSON Schema is cached under the mode it was generated with:
            with self._config_wrapper_stack.push(_get_class_config(schema)):  # pyright: ignore[reportArgumentType]
                return self._generate_inner(schema)
        return self._generate_inner(schema)
```


---

### 🔹 Commit #07: `7cb6ee4c`
- **完整 Hash**: `7cb6ee4c0550ab0380259e10cfaeef4659767de4`
- **說明 (Ground Truth)**: Fix `TypeError` on `ForwardRef` on Python 3.10.0 (#13964)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/_internal/_typing_extra.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:41, E:44, A:0) ➔ After(N:41, E:44, A:0)
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

### 🔹 函式: `_type_convert()`
- **變更前簽章 (Before)**: `def _type_convert(arg: Any) -> Any` (L198~L213)
- **變更後簽章 (After)**: `def _type_convert(arg: Any) -> Any` (L198~L216)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _type_convert(arg: Any) -> Any:
    """Convert `None` to `NoneType` and strings to `ForwardRef` instances.

    This is a vendored version of the private `typing._type_convert()` function. When
    evaluating a type, `ForwardRef._evaluate()` ends up being called, and is
    responsible for making this conversion. However, we still have to apply
    it for the first argument passed to our type evaluation functions, similarly
    to the `typing.get_type_hints()` function.
    """
    if arg is None:
        return NoneType
    if isinstance(arg, str):
        # Like `typing.get_type_hints()`, assume the arg can be in any context,
        # hence the proper `is_argument` and `is_class` args:
        return ForwardRef(arg, is_argument=False, is_class=True)
    return arg
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _type_convert(arg: Any) -> Any:
    """Convert `None` to `NoneType` and strings to `ForwardRef` instances.

    This is a vendored version of the private `typing._type_convert()` function. When
    evaluating a type, `ForwardRef._evaluate()` ends up being called, and is
    responsible for making this conversion. However, we still have to apply
    it for the first argument passed to our type evaluation functions, similarly
    to the `typing.get_type_hints()` function.
    """
    if arg is None:
        return NoneType
    if isinstance(arg, str):
        if sys.version_info[:3] == (3, 10, 0):
            return ForwardRef(arg, is_argument=False)
        else:
            # Like `typing.get_type_hints()`, assume the arg can be in any context,
            # hence the proper `is_argument` and `is_class` args:
            return ForwardRef(arg, is_argument=False, is_class=True)
    return arg
```


---

### 🔹 Commit #08: `027b5c71`
- **完整 Hash**: `027b5c714791d5f6e86faea4110ef26f4776648c`
- **說明 (Ground Truth)**: Rebuild incomplete types during serialization inference (#13922)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/_internal/_mock_val_ser.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:25, E:24, A:0) ➔ After(N:26, E:24, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 10, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `AttemptRebuild.__call__` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `handler()`
- **變更前簽章 (Before)**: `def handler() -> T | None` (L166~L169)
- **變更後簽章 (After)**: `def handler(*, parent_namespace_depth: int = 5) -> T | None` (L171~L174)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def handler() -> T | None:
            if cls.model_rebuild(raise_errors=False, _parent_namespace_depth=5) is not False:
                return attr_fn(cls)
            return None
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def handler(*, parent_namespace_depth: int = 5) -> T | None:
            if cls.model_rebuild(raise_errors=False, _parent_namespace_depth=parent_namespace_depth) is not False:
                return attr_fn(cls)
            return None
```

### 🔹 函式: `set_dataclass_mocks()`
- **變更前簽章 (Before)**: `def set_dataclass_mocks(cls: type[PydanticDataclass], undefined_name: str | None = None) -> None` (L192~L232)
- **變更後簽章 (After)**: `def set_dataclass_mocks(cls: type[PydanticDataclass], undefined_name: str | None = None) -> None` (L197~L237)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def set_dataclass_mocks(cls: type[PydanticDataclass], undefined_name: str | None = None) -> None:
    """Set `__pydantic_validator__` and `__pydantic_serializer__` to `MockValSer`s on a dataclass.

    Args:
        cls: The model class to set the mocks on
        undefined_name: Name of the undefined thing, used in error messages
    """
    from ..dataclasses import rebuild_dataclass

    undefined_name = undefined_name if undefined_name is not None else 'all referenced types'

    undefined_type_error_message = (
        f'`{cls.__name__}` is not fully defined; you should define {undefined_name},'
        f' then call `pydantic.dataclasses.rebuild_dataclass({cls.__name__})`.'
    )

    def attempt_rebuild_fn(attr_fn: Callable[[type[PydanticDataclass]], T]) -> Callable[[], T | None]:
        def handler() -> T | None:
            if rebuild_dataclass(cls, raise_errors=False, _parent_namespace_depth=5) is not False:
                return attr_fn(cls)
            return None

        return handler

    cls.__pydantic_core_schema__ = MockCoreSchema(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_core_schema__),
    )
    cls.__pydantic_validator__ = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='validator',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_validator__),
    )
    cls.__pydantic_serializer__ = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='serializer',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_serializer__),
    )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def set_dataclass_mocks(cls: type[PydanticDataclass], undefined_name: str | None = None) -> None:
    """Set `__pydantic_validator__` and `__pydantic_serializer__` to `MockValSer`s on a dataclass.

    Args:
        cls: The model class to set the mocks on
        undefined_name: Name of the undefined thing, used in error messages
    """
    from ..dataclasses import rebuild_dataclass

    undefined_name = undefined_name if undefined_name is not None else 'all referenced types'

    undefined_type_error_message = (
        f'`{cls.__name__}` is not fully defined; you should define {undefined_name},'
        f' then call `pydantic.dataclasses.rebuild_dataclass({cls.__name__})`.'
    )

    def attempt_rebuild_fn(attr_fn: Callable[[type[PydanticDataclass]], T]) -> AttemptRebuild[T]:
        def handler(*, parent_namespace_depth: int = 5) -> T | None:
            if rebuild_dataclass(cls, raise_errors=False, _parent_namespace_depth=parent_namespace_depth) is not False:
                return attr_fn(cls)
            return None

        return handler

    cls.__pydantic_core_schema__ = MockCoreSchema(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_core_schema__),
    )
    cls.__pydantic_validator__ = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='validator',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_validator__),
    )
    cls.__pydantic_serializer__ = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='serializer',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_serializer__),
    )
```

### 🔹 函式: `set_type_adapter_mocks()`
- **變更前簽章 (Before)**: `def set_type_adapter_mocks(adapter: TypeAdapter) -> None` (L112~L148)
- **變更後簽章 (After)**: `def set_type_adapter_mocks(adapter: TypeAdapter) -> None` (L117~L153)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def set_type_adapter_mocks(adapter: TypeAdapter) -> None:
    """Set `core_schema`, `validator` and `serializer` to mock core types on a type adapter instance.

    Args:
        adapter: The type adapter instance to set the mocks on
    """
    type_repr = str(adapter._type)
    undefined_type_error_message = (
        f'`TypeAdapter[{type_repr}]` is not fully defined; you should define `{type_repr}` and all referenced types,'
        f' then call `.rebuild()` on the instance.'
    )

    def attempt_rebuild_fn(attr_fn: Callable[[TypeAdapter], T]) -> Callable[[], T | None]:
        def handler() -> T | None:
            if adapter.rebuild(raise_errors=False, _parent_namespace_depth=5) is not False:
                return attr_fn(adapter)
            return None

        return handler

    adapter.core_schema = MockCoreSchema(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        attempt_rebuild=attempt_rebuild_fn(lambda ta: ta.core_schema),
    )
    adapter.validator = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='validator',
        attempt_rebuild=attempt_rebuild_fn(lambda ta: ta.validator),
    )
    adapter.serializer = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='serializer',
        attempt_rebuild=attempt_rebuild_fn(lambda ta: ta.serializer),
    )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def set_type_adapter_mocks(adapter: TypeAdapter) -> None:
    """Set `core_schema`, `validator` and `serializer` to mock core types on a type adapter instance.

    Args:
        adapter: The type adapter instance to set the mocks on
    """
    type_repr = str(adapter._type)
    undefined_type_error_message = (
        f'`TypeAdapter[{type_repr}]` is not fully defined; you should define `{type_repr}` and all referenced types,'
        f' then call `.rebuild()` on the instance.'
    )

    def attempt_rebuild_fn(attr_fn: Callable[[TypeAdapter], T]) -> AttemptRebuild[T]:
        def handler(*, parent_namespace_depth: int = 5) -> T | None:
            if adapter.rebuild(raise_errors=False, _parent_namespace_depth=parent_namespace_depth) is not False:
                return attr_fn(adapter)
            return None

        return handler

    adapter.core_schema = MockCoreSchema(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        attempt_rebuild=attempt_rebuild_fn(lambda ta: ta.core_schema),
    )
    adapter.validator = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='validator',
        attempt_rebuild=attempt_rebuild_fn(lambda ta: ta.validator),
    )
    adapter.serializer = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='serializer',
        attempt_rebuild=attempt_rebuild_fn(lambda ta: ta.serializer),
    )
```

### 🔹 函式: `attempt_rebuild_fn()`
- **變更前簽章 (Before)**: `def attempt_rebuild_fn(attr_fn: Callable[[TypeAdapter], T]) -> Callable[[], T | None]` (L124~L130)
- **變更後簽章 (After)**: `def attempt_rebuild_fn(attr_fn: Callable[[TypeAdapter], T]) -> AttemptRebuild[T]` (L129~L135)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def attempt_rebuild_fn(attr_fn: Callable[[TypeAdapter], T]) -> Callable[[], T | None]:
        def handler() -> T | None:
            if adapter.rebuild(raise_errors=False, _parent_namespace_depth=5) is not False:
                return attr_fn(adapter)
            return None

        return handler
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def attempt_rebuild_fn(attr_fn: Callable[[TypeAdapter], T]) -> AttemptRebuild[T]:
        def handler(*, parent_namespace_depth: int = 5) -> T | None:
            if adapter.rebuild(raise_errors=False, _parent_namespace_depth=parent_namespace_depth) is not False:
                return attr_fn(adapter)
            return None

        return handler
```

### 🔹 函式: `attempt_rebuild_fn()`
- **變更前簽章 (Before)**: `def attempt_rebuild_fn(attr_fn: Callable[[type[BaseModel]], T]) -> Callable[[], T | None]` (L165~L171)
- **變更後簽章 (After)**: `def attempt_rebuild_fn(attr_fn: Callable[[type[BaseModel]], T]) -> AttemptRebuild[T]` (L170~L176)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def attempt_rebuild_fn(attr_fn: Callable[[type[BaseModel]], T]) -> Callable[[], T | None]:
        def handler() -> T | None:
            if cls.model_rebuild(raise_errors=False, _parent_namespace_depth=5) is not False:
                return attr_fn(cls)
            return None

        return handler
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def attempt_rebuild_fn(attr_fn: Callable[[type[BaseModel]], T]) -> AttemptRebuild[T]:
        def handler(*, parent_namespace_depth: int = 5) -> T | None:
            if cls.model_rebuild(raise_errors=False, _parent_namespace_depth=parent_namespace_depth) is not False:
                return attr_fn(cls)
            return None

        return handler
```

### 🔹 函式: `attempt_rebuild_fn()`
- **變更前簽章 (Before)**: `def attempt_rebuild_fn(attr_fn: Callable[[type[PydanticDataclass]], T]) -> Callable[[], T | None]` (L208~L214)
- **變更後簽章 (After)**: `def attempt_rebuild_fn(attr_fn: Callable[[type[PydanticDataclass]], T]) -> AttemptRebuild[T]` (L213~L219)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def attempt_rebuild_fn(attr_fn: Callable[[type[PydanticDataclass]], T]) -> Callable[[], T | None]:
        def handler() -> T | None:
            if rebuild_dataclass(cls, raise_errors=False, _parent_namespace_depth=5) is not False:
                return attr_fn(cls)
            return None

        return handler
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def attempt_rebuild_fn(attr_fn: Callable[[type[PydanticDataclass]], T]) -> AttemptRebuild[T]:
        def handler(*, parent_namespace_depth: int = 5) -> T | None:
            if rebuild_dataclass(cls, raise_errors=False, _parent_namespace_depth=parent_namespace_depth) is not False:
                return attr_fn(cls)
            return None

        return handler
```

### 🔹 函式: `handler()`
- **變更前簽章 (Before)**: `def handler() -> T | None` (L125~L128)
- **變更後簽章 (After)**: `def handler(*, parent_namespace_depth: int = 5) -> T | None` (L130~L133)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def handler() -> T | None:
            if adapter.rebuild(raise_errors=False, _parent_namespace_depth=5) is not False:
                return attr_fn(adapter)
            return None
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def handler(*, parent_namespace_depth: int = 5) -> T | None:
            if adapter.rebuild(raise_errors=False, _parent_namespace_depth=parent_namespace_depth) is not False:
                return attr_fn(adapter)
            return None
```

### 🔹 函式: `handler()`
- **變更前簽章 (Before)**: `def handler() -> T | None` (L209~L212)
- **變更後簽章 (After)**: `def handler(*, parent_namespace_depth: int = 5) -> T | None` (L214~L217)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def handler() -> T | None:
            if rebuild_dataclass(cls, raise_errors=False, _parent_namespace_depth=5) is not False:
                return attr_fn(cls)
            return None
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def handler(*, parent_namespace_depth: int = 5) -> T | None:
            if rebuild_dataclass(cls, raise_errors=False, _parent_namespace_depth=parent_namespace_depth) is not False:
                return attr_fn(cls)
            return None
```

### 🔹 函式: `set_model_mocks()`
- **變更前簽章 (Before)**: `def set_model_mocks(cls: type[BaseModel], undefined_name: str | None = None) -> None` (L151~L189)
- **變更後簽章 (After)**: `def set_model_mocks(cls: type[BaseModel], undefined_name: str | None = None) -> None` (L156~L194)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def set_model_mocks(cls: type[BaseModel], undefined_name: str | None = None) -> None:
    """Set `__pydantic_core_schema__`, `__pydantic_validator__` and `__pydantic_serializer__` to mock core types on a model.

    Args:
        cls: The model class to set the mocks on
        undefined_name: Name of the undefined thing, used in error messages
    """
    undefined_name = undefined_name if undefined_name is not None else 'all referenced types'

    undefined_type_error_message = (
        f'`{cls.__name__}` is not fully defined; you should define {undefined_name},'
        f' then call `{cls.__name__}.model_rebuild()`.'
    )

    def attempt_rebuild_fn(attr_fn: Callable[[type[BaseModel]], T]) -> Callable[[], T | None]:
        def handler() -> T | None:
            if cls.model_rebuild(raise_errors=False, _parent_namespace_depth=5) is not False:
                return attr_fn(cls)
            return None

        return handler

    cls.__pydantic_core_schema__ = MockCoreSchema(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_core_schema__),
    )
    cls.__pydantic_validator__ = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='validator',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_validator__),
    )
    cls.__pydantic_serializer__ = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='serializer',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_serializer__),
    )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def set_model_mocks(cls: type[BaseModel], undefined_name: str | None = None) -> None:
    """Set `__pydantic_core_schema__`, `__pydantic_validator__` and `__pydantic_serializer__` to mock core types on a model.

    Args:
        cls: The model class to set the mocks on
        undefined_name: Name of the undefined thing, used in error messages
    """
    undefined_name = undefined_name if undefined_name is not None else 'all referenced types'

    undefined_type_error_message = (
        f'`{cls.__name__}` is not fully defined; you should define {undefined_name},'
        f' then call `{cls.__name__}.model_rebuild()`.'
    )

    def attempt_rebuild_fn(attr_fn: Callable[[type[BaseModel]], T]) -> AttemptRebuild[T]:
        def handler(*, parent_namespace_depth: int = 5) -> T | None:
            if cls.model_rebuild(raise_errors=False, _parent_namespace_depth=parent_namespace_depth) is not False:
                return attr_fn(cls)
            return None

        return handler

    cls.__pydantic_core_schema__ = MockCoreSchema(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_core_schema__),
    )
    cls.__pydantic_validator__ = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='validator',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_validator__),
    )
    cls.__pydantic_serializer__ = MockValSer(  # pyright: ignore[reportAttributeAccessIssue]
        undefined_type_error_message,
        code='class-not-fully-defined',
        val_or_ser='serializer',
        attempt_rebuild=attempt_rebuild_fn(lambda c: c.__pydantic_serializer__),
    )
```

### 🔹 函式: `MockValSer.rebuild()`
- **變更前簽章 (Before)**: `def rebuild(self) -> ValSer | None` (L102~L109)
- **變更後簽章 (After)**: `def rebuild(self, *, parent_namespace_depth: int = 5) -> ValSer | None` (L107~L114)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def rebuild(self) -> ValSer | None:
        if self._attempt_rebuild:
            val_ser = self._attempt_rebuild()
            if val_ser is not None:
                return val_ser
            else:
                raise PydanticUserError(self._error_message, code=self._code)
        return None
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def rebuild(self, *, parent_namespace_depth: int = 5) -> ValSer | None:
        if self._attempt_rebuild:
            val_ser = self._attempt_rebuild(parent_namespace_depth=parent_namespace_depth)
            if val_ser is not None:
                return val_ser
            else:
                raise PydanticUserError(self._error_message, code=self._code)
        return None
```


---

### 🔹 Commit #09: `e5b02608`
- **完整 Hash**: `e5b02608847e59c4cdbeb6355d49374a800a9c91`
- **說明 (Ground Truth)**: Handle OS errors during `ZoneInfo` validation (#13912)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/_internal/_validators.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:70, E:82, A:0) ➔ After(N:70, E:82, A:0)
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

### 🔹 函式: `validate_str_is_valid_iana_tz()`
- **變更前簽章 (Before)**: `def validate_str_is_valid_iana_tz(value: Any, /) -> ZoneInfo` (L486~L492)
- **變更後簽章 (After)**: `def validate_str_is_valid_iana_tz(value: Any, /) -> ZoneInfo` (L486~L492)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def validate_str_is_valid_iana_tz(value: Any, /) -> ZoneInfo:
    if isinstance(value, ZoneInfo):
        return value
    try:
        return ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError, TypeError):
        raise PydanticCustomError('zoneinfo_str', 'invalid timezone: {value}', {'value': value})
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def validate_str_is_valid_iana_tz(value: Any, /) -> ZoneInfo:
    if isinstance(value, ZoneInfo):
        return value
    try:
        return ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError, TypeError, OSError):
        raise PydanticCustomError('zoneinfo_str', 'invalid timezone: {value}', {'value': value})
```


---

### 🔹 Commit #10: `26f7b8a1`
- **完整 Hash**: `26f7b8a1ad02951962c4073297fa9a2b1ce8d30c`
- **說明 (Ground Truth)**: Respect propagated extra config in the JSON Schema of stdlib dataclasses (#13899)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/json_schema.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:220, E:329, A:0) ➔ After(N:220, E:329, A:0)
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

### 🔹 函式: `GenerateJsonSchema.dataclass_schema()`
- **變更前簽章 (Before)**: `def dataclass_schema(self, schema: core_schema.DataclassSchema) -> JsonSchemaValue` (L1972~L1991)
- **變更後簽章 (After)**: `def dataclass_schema(self, schema: core_schema.DataclassSchema) -> JsonSchemaValue` (L1972~L1997)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def dataclass_schema(self, schema: core_schema.DataclassSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that defines a dataclass.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """

        cls = schema['cls']
        # If (stdlib) dataclass doesn't have config, the parent's config is used (as during core schema generation):
        config = cast('ConfigDict | None', getattr(cls, '__pydantic_config__', None))

        with self._config_wrapper_stack.push(config):
            json_schema = self.generate_inner(schema['schema']).copy()

        self._update_class_schema(json_schema, cls, config or {})

        return json_schema
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def dataclass_schema(self, schema: core_schema.DataclassSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that defines a dataclass.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """

        cls = schema['cls']
        # If (stdlib) dataclass doesn't have config, the parent's config is used (as during core schema generation):
        config = cast('ConfigDict | None', getattr(cls, '__pydantic_config__', None))

        with self._config_wrapper_stack.push(config):
            json_schema = self.generate_inner(schema['schema']).copy()

        # Only the parent's `extra` config value is relevant to the class schema. It is propagated
        # to the core config (and used for validation), so we reuse it:
        class_config = config or {}
        if 'extra' not in class_config and (extra := schema.get('config', {}).get('extra_fields_behavior')) is not None:
            class_config = cast('ConfigDict', {**class_config, 'extra': extra})

        self._update_class_schema(json_schema, cls, class_config)

        return json_schema
```


---

### 🔹 Commit #11: `e3d96620`
- **完整 Hash**: `e3d96620f9384e82f9c659469d61a2ffc61c94cb`
- **說明 (Ground Truth)**: Propagate `init` and `kw_only=False` from `Field()` to stdlib dataclass fields (#13898)
- **變更檔案數**: 2

#### 📄 檔案: `pydantic/_internal/_dataclasses.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:25, E:22, A:0) ➔ After(N:25, E:22, A:0)
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

### 🔹 函式: `patch_base_fields()`
- **變更前簽章 (Before)**: `def patch_base_fields(cls: type[Any]) -> Generator[None]` (L230~L315)
- **變更後簽章 (After)**: `def patch_base_fields(cls: type[Any]) -> Generator[None]` (L235~L327)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def patch_base_fields(cls: type[Any]) -> Generator[None]:
    """Temporarily patch the stdlib dataclasses bases of `cls` if the Pydantic `Field()` function is used.

    When creating a Pydantic dataclass, it is possible to inherit from stdlib dataclasses, where
    the Pydantic `Field()` function is used. To create this Pydantic dataclass, we first apply
    the stdlib `@dataclass` decorator on it. During the construction of the stdlib dataclass,
    the `kw_only` and `repr` field arguments need to be understood by the stdlib *during* the
    dataclass construction. To do so, we temporarily patch the fields dictionary of the affected
    bases.

    For instance, with the following example:

    ```python {test="skip" lint="skip"}
    import dataclasses as stdlib_dc

    import pydantic
    import pydantic.dataclasses as pydantic_dc

    @stdlib_dc.dataclass
    class A:
        a: int = pydantic.Field(repr=False)

    # Notice that the `repr` attribute of the dataclass field is `True`:
    A.__dataclass_fields__['a']
    #> dataclass.Field(default=FieldInfo(repr=False), repr=True, ...)

    @pydantic_dc.dataclass
    class B(A):
        b: int = pydantic.Field(repr=False)
    ```

    When passing `B` to the stdlib `@dataclass` decorator, it will look for fields in the parent classes
    and reuse them directly. When this context manager is active, `A` will be temporarily patched to be
    equivalent to:

    ```python {test="skip" lint="skip"}
    @stdlib_dc.dataclass
    class A:
        a: int = stdlib_dc.field(default=Field(repr=False), repr=False)
    ```

    !!! note
        This is only applied to the bases of `cls`, and not `cls` itself. The reason is that the Pydantic
        dataclass decorator "owns" `cls` (in the previous example, `B`). As such, we instead modify the fields
        directly (in the previous example, we simply do `setattr(B, 'b', as_dataclass_field(pydantic_field))`).

    !!! note
        This approach is far from ideal, and can probably be the source of unwanted side effects/race conditions.
        The previous implemented approach was mutating the `__annotations__` dict of `cls`, which is no longer a
        safe operation in Python 3.14+, and resulted in unexpected behavior with field ordering anyway.
    """
    # A list of two-tuples, the first element being a reference to the
    # dataclass fields dictionary, the second element being a mapping between
    # the field names that were modified, and their original `Field`:
    original_fields_list: list[tuple[DcFields, DcFields]] = []

    for base in cls.__mro__[1:]:
        dc_fields: dict[str, dataclasses.Field[Any]] = base.__dict__.get('__dataclass_fields__', {})
        dc_fields_with_pydantic_field_defaults = {
            field_name: field
            for field_name, field in dc_fields.items()
            if isinstance(field.default, FieldInfo)
            # Only do the patching if one of the affected attributes is set:
            and (field.default.description is not None or field.default.kw_only or field.default.repr is not True)
        }
        if dc_fields_with_pydantic_field_defaults:
            original_fields_list.append((dc_fields, dc_fields_with_pydantic_field_defaults))
            for field_name, field in dc_fields_with_pydantic_field_defaults.items():
                default = cast(FieldInfo, field.default)
                # `dataclasses.Field` isn't documented as working with `copy.copy()`.
                # It is a class with `__slots__`, so should work (and we hope for the best):
                new_dc_field = copy.copy(field)
                # For base fields, no need to set `doc` from `FieldInfo.description`, this is only relevant
                # for the class under construction and handled in `as_dataclass_field()`.
                if default.kw_only:
                    new_dc_field.kw_only = True
                if default.repr is not True:
                    new_dc_field.repr = default.repr
                dc_fields[field_name] = new_dc_field

    try:
        yield
    finally:
        for fields, original_fields in original_fields_list:
            for field_name, original_field in original_fields.items():
                fields[field_name] = original_field
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def patch_base_fields(cls: type[Any]) -> Generator[None]:
    """Temporarily patch the stdlib dataclasses bases of `cls` if the Pydantic `Field()` function is used.

    When creating a Pydantic dataclass, it is possible to inherit from stdlib dataclasses, where
    the Pydantic `Field()` function is used. To create this Pydantic dataclass, we first apply
    the stdlib `@dataclass` decorator on it. During the construction of the stdlib dataclass,
    the `kw_only`, `repr` and `init` field arguments need to be understood by the stdlib *during* the
    dataclass construction. To do so, we temporarily patch the fields dictionary of the affected
    bases.

    For instance, with the following example:

    ```python {test="skip" lint="skip"}
    import dataclasses as stdlib_dc

    import pydantic
    import pydantic.dataclasses as pydantic_dc

    @stdlib_dc.dataclass
    class A:
        a: int = pydantic.Field(repr=False)

    # Notice that the `repr` attribute of the dataclass field is `True`:
    A.__dataclass_fields__['a']
    #> dataclass.Field(default=FieldInfo(repr=False), repr=True, ...)

    @pydantic_dc.dataclass
    class B(A):
        b: int = pydantic.Field(repr=False)
    ```

    When passing `B` to the stdlib `@dataclass` decorator, it will look for fields in the parent classes
    and reuse them directly. When this context manager is active, `A` will be temporarily patched to be
    equivalent to:

    ```python {test="skip" lint="skip"}
    @stdlib_dc.dataclass
    class A:
        a: int = stdlib_dc.field(default=Field(repr=False), repr=False)
    ```

    !!! note
        This is only applied to the bases of `cls`, and not `cls` itself. The reason is that the Pydantic
        dataclass decorator "owns" `cls` (in the previous example, `B`). As such, we instead modify the fields
        directly (in the previous example, we simply do `setattr(B, 'b', as_dataclass_field(pydantic_field))`).

    !!! note
        This approach is far from ideal, and can probably be the source of unwanted side effects/race conditions.
        The previous implemented approach was mutating the `__annotations__` dict of `cls`, which is no longer a
        safe operation in Python 3.14+, and resulted in unexpected behavior with field ordering anyway.
    """
    # A list of two-tuples, the first element being a reference to the
    # dataclass fields dictionary, the second element being a mapping between
    # the field names that were modified, and their original `Field`:
    original_fields_list: list[tuple[DcFields, DcFields]] = []

    for base in cls.__mro__[1:]:
        dc_fields: dict[str, dataclasses.Field[Any]] = base.__dict__.get('__dataclass_fields__', {})
        dc_fields_with_pydantic_field_defaults = {
            field_name: field
            for field_name, field in dc_fields.items()
            if isinstance(field.default, FieldInfo)
            # Only do the patching if one of the affected attributes is set:
            and (
                field.default.description is not None
                or field.default.kw_only is not None
                or field.default.repr is not True
                or field.default.init is False
            )
        }
        if dc_fields_with_pydantic_field_defaults:
            original_fields_list.append((dc_fields, dc_fields_with_pydantic_field_defaults))
            for field_name, field in dc_fields_with_pydantic_field_defaults.items():
                default = cast(FieldInfo, field.default)
                # `dataclasses.Field` isn't documented as working with `copy.copy()`.
                # It is a class with `__slots__`, so should work (and we hope for the best):
                new_dc_field = copy.copy(field)
                # For base fields, no need to set `doc` from `FieldInfo.description`, this is only relevant
                # for the class under construction and handled in `as_dataclass_field()`.
                if default.kw_only is not None:
                    new_dc_field.kw_only = default.kw_only
                if default.repr is not True:
                    new_dc_field.repr = default.repr
                if default.init is False:
                    new_dc_field.init = False
                dc_fields[field_name] = new_dc_field

    try:
        yield
    finally:
        for fields, original_fields in original_fields_list:
            for field_name, original_field in original_fields.items():
                fields[field_name] = original_field
```

### 🔹 函式: `as_dataclass_field()`
- **變更前簽章 (Before)**: `def as_dataclass_field(pydantic_field: FieldInfo) -> dataclasses.Field[Any]` (L208~L223)
- **變更後簽章 (After)**: `def as_dataclass_field(pydantic_field: FieldInfo) -> dataclasses.Field[Any]` (L208~L228)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def as_dataclass_field(pydantic_field: FieldInfo) -> dataclasses.Field[Any]:
    field_args: dict[str, Any] = {'default': pydantic_field}

    # Needed because if `doc` is set, the dataclass slots will be a dict (field name -> doc) instead of a tuple:
    if sys.version_info >= (3, 14) and pydantic_field.description is not None:
        field_args['doc'] = pydantic_field.description

    # Needed as the stdlib dataclass module processes kw_only in a specific way during class construction:
    if pydantic_field.kw_only is not None:
        field_args['kw_only'] = pydantic_field.kw_only

    # Needed as the stdlib dataclass modules generates `__repr__()` during class construction:
    if pydantic_field.repr is not True:
        field_args['repr'] = pydantic_field.repr

    return dataclasses.field(**field_args)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def as_dataclass_field(pydantic_field: FieldInfo) -> dataclasses.Field[Any]:
    field_args: dict[str, Any] = {'default': pydantic_field}

    # Needed because if `doc` is set, the dataclass slots will be a dict (field name -> doc) instead of a tuple:
    if sys.version_info >= (3, 14) and pydantic_field.description is not None:
        field_args['doc'] = pydantic_field.description

    # Needed as the stdlib dataclass module processes `kw_only` in a specific way during class construction:
    if pydantic_field.kw_only is not None:
        field_args['kw_only'] = pydantic_field.kw_only

    # Needed as the stdlib dataclass modules generates `__repr__()` during class construction:
    if pydantic_field.repr is not True:
        field_args['repr'] = pydantic_field.repr

    # Needed as the stdlib dataclass module uses `init` during class construction (e.g. to generate `__match_args__`),
    # and `dataclasses.replace()` relies on it:
    if pydantic_field.init is False:
        field_args['init'] = False

    return dataclasses.field(**field_args)
```


#### 📄 檔案: `pydantic/dataclasses.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:48, E:46, A:0) ➔ After(N:48, E:46, A:0)
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

### 🔹 Commit #12: `48785824`
- **完整 Hash**: `48785824a8071c9a33d4db9d2c0651b78b38cd3c`
- **說明 (Ground Truth)**: Encode JSON Schema defaults with a consistent configuration (#13893)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/json_schema.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:220, E:329, A:0) ➔ After(N:220, E:329, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 1, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `GenerateJsonSchema.encode_default` ──[CALLS]──> `cast (External/Unresolved)`
  • - [移除呼叫邊] `GenerateJsonSchema.encode_default` ──[CALLS]──> `to_jsonable_python (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `GenerateJsonSchema.encode_default()`
- **變更前簽章 (Before)**: `def encode_default(self, dft: Any) -> Any` (L2540~L2569)
- **變更後簽章 (After)**: `def encode_default(self, dft: Any) -> Any` (L2540~L2568)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def encode_default(self, dft: Any) -> Any:
        """Encode a default value to a JSON-serializable value.

        This is used to encode default values for fields in the generated JSON schema.

        Args:
            dft: The default value to encode.

        Returns:
            The encoded default value.
        """
        from .type_adapter import TypeAdapter, _type_has_config

        config = self._config
        try:
            default = (
                dft
                if _type_has_config(type(dft))
                else TypeAdapter(type(dft), config=config.config_dict).dump_python(
                    dft, by_alias=self.by_alias, mode='json'
                )
            )
            return pydantic_core.to_jsonable_python(
                default,
                timedelta_mode=config.ser_json_timedelta,
                bytes_mode=config.ser_json_bytes,
                by_alias=self.by_alias,
            )
        except Exception as e:
            raise pydantic_core.PydanticSerializationError(f'Unable to encode default value {dft}') from e
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def encode_default(self, dft: Any) -> Any:
        """Encode a default value to a JSON-serializable value.

        This is used to encode default values for fields in the generated JSON schema.

        Args:
            dft: The default value to encode.

        Returns:
            The encoded default value.
        """
        from .type_adapter import TypeAdapter, _type_has_config

        config = self._config.config_dict
        if self.mode == 'validation' and ('ser_json_temporal' in config or 'ser_json_timedelta' in config):
            # Temporal serialization formats aren't applied to validation JSON Schemas (see `_common_temporal_schema()`),
            # so they shouldn't be applied to the default either:
            config = cast(
                'ConfigDict',
                {k: v for k, v in config.items() if k not in ('ser_json_temporal', 'ser_json_timedelta')},
            )
        try:
            # Types with their own config (e.g. models) can't be used with a config, so we serialize "as Any",
            # which will serialize using their own serializer.
            return TypeAdapter(Any if _type_has_config(type(dft)) else type(dft), config=config).dump_python(
                dft, by_alias=self.by_alias, mode='json'
            )
        except Exception as e:
            raise pydantic_core.PydanticSerializationError(f'Unable to encode default value {dft}') from e
```


---

### 🔹 Commit #13: `b0cd9d34`
- **完整 Hash**: `b0cd9d347dc4159043620fde554cbd63d08e3ad5`
- **說明 (Ground Truth)**: Fix config propagation of stdlib dataclasses and `TypedDict`s in JSON Schema (#13891)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/json_schema.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:220, E:329, A:0) ➔ After(N:220, E:329, A:0)
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

### 🔹 函式: `GenerateJsonSchema.typed_dict_schema()`
- **變更前簽章 (Before)**: `def typed_dict_schema(self, schema: core_schema.TypedDictSchema) -> JsonSchemaValue` (L1611~L1660)
- **變更後簽章 (After)**: `def typed_dict_schema(self, schema: core_schema.TypedDictSchema) -> JsonSchemaValue` (L1611~L1660)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def typed_dict_schema(self, schema: core_schema.TypedDictSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that defines a typed dict.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """
        total = schema.get('total', True)
        named_required_fields: list[tuple[str, bool, CoreSchemaField]] = [
            (name, self.field_is_required(field, total), field)
            for name, field in schema['fields'].items()
            if self.field_is_present(field)
        ]
        if self.mode == 'serialization':
            named_required_fields.extend(self._name_required_computed_fields(schema.get('computed_fields', [])))
        cls = schema.get('cls')
        config = _get_typed_dict_config(cls)
        with self._config_wrapper_stack.push(config):
            json_schema = self._named_required_fields_schema(named_required_fields)

        # There's some duplication between `extra_behavior` and
        # the config's `extra`/core config's `extra_fields_behavior`.
        # However, it is common to manually create TypedDictSchemas,
        # where you don't necessarily have a class.
        # At runtime, `extra_behavior` takes priority over the config
        # for validation, so follow the same for the JSON Schema:
        if 'extras_schema' in schema and schema['extras_schema'] != core_schema.any_schema():
            allow_additional_props = self.generate_inner(schema['extras_schema'])
        else:
            allow_additional_props = True

        if schema.get('extra_behavior') == 'forbid':
            json_schema['additionalProperties'] = False
        elif schema.get('extra_behavior') == 'allow':
            json_schema['additionalProperties'] = allow_additional_props

        if cls is not None:
            # `_update_class_schema()` will not override
            # `additionalProperties` if already present:
            self._update_class_schema(json_schema, cls, config)
        elif 'additionalProperties' not in json_schema:
            extra = schema.get('config', {}).get('extra_fields_behavior')
            if extra == 'forbid':
                json_schema['additionalProperties'] = False
            elif extra == 'allow':
                json_schema['additionalProperties'] = allow_additional_props

        return json_schema
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def typed_dict_schema(self, schema: core_schema.TypedDictSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that defines a typed dict.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """
        total = schema.get('total', True)
        named_required_fields: list[tuple[str, bool, CoreSchemaField]] = [
            (name, self.field_is_required(field, total), field)
            for name, field in schema['fields'].items()
            if self.field_is_present(field)
        ]
        if self.mode == 'serialization':
            named_required_fields.extend(self._name_required_computed_fields(schema.get('computed_fields', [])))
        cls = schema.get('cls')
        config = _get_typed_dict_config(cls)
        with self._config_wrapper_stack.push(config):
            json_schema = self._named_required_fields_schema(named_required_fields)

        # There's some duplication between `extra_behavior` and
        # the config's `extra`/core config's `extra_fields_behavior`.
        # However, it is common to manually create TypedDictSchemas,
        # where you don't necessarily have a class.
        # At runtime, `extra_behavior` takes priority over the config
        # for validation, so follow the same for the JSON Schema:
        if 'extras_schema' in schema and schema['extras_schema'] != core_schema.any_schema():
            allow_additional_props = self.generate_inner(schema['extras_schema'])
        else:
            allow_additional_props = True

        if schema.get('extra_behavior') == 'forbid':
            json_schema['additionalProperties'] = False
        elif schema.get('extra_behavior') == 'allow':
            json_schema['additionalProperties'] = allow_additional_props

        if cls is not None:
            # `_update_class_schema()` will not override
            # `additionalProperties` if already present:
            self._update_class_schema(json_schema, cls, config or {})
        elif 'additionalProperties' not in json_schema:
            extra = schema.get('config', {}).get('extra_fields_behavior')
            if extra == 'forbid':
                json_schema['additionalProperties'] = False
            elif extra == 'allow':
                json_schema['additionalProperties'] = allow_additional_props

        return json_schema
```

### 🔹 函式: `_get_typed_dict_config()`
- **變更前簽章 (Before)**: `def _get_typed_dict_config(cls: type[Any] | None) -> ConfigDict` (L3236~L3242)
- **變更後簽章 (After)**: `def _get_typed_dict_config(cls: type[Any] | None) -> ConfigDict | None: # If typed dictionary doesn't have config, the parent's config is used (as during core schema generation), # hence a default of `None`` (L3237~L3245)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _get_typed_dict_config(cls: type[Any] | None) -> ConfigDict:
    if cls is not None:
        try:
            return _decorators.get_attribute_from_bases(cls, '__pydantic_config__')
        except AttributeError:
            pass
    return {}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _get_typed_dict_config(cls: type[Any] | None) -> ConfigDict | None:
    # If typed dictionary doesn't have config, the parent's config is used (as during core schema generation),
    # hence a default of `None`:
    if cls is not None:
        try:
            return _decorators.get_attribute_from_bases(cls, '__pydantic_config__')
        except AttributeError:
            pass
    return None
```

### 🔹 函式: `GenerateJsonSchema.dataclass_schema()`
- **變更前簽章 (Before)**: `def dataclass_schema(self, schema: core_schema.DataclassSchema) -> JsonSchemaValue` (L1972~L1990)
- **變更後簽章 (After)**: `def dataclass_schema(self, schema: core_schema.DataclassSchema) -> JsonSchemaValue` (L1972~L1991)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def dataclass_schema(self, schema: core_schema.DataclassSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that defines a dataclass.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """

        cls = schema['cls']
        config = cast('ConfigDict', getattr(cls, '__pydantic_config__', {}))

        with self._config_wrapper_stack.push(config):
            json_schema = self.generate_inner(schema['schema']).copy()

        self._update_class_schema(json_schema, cls, config)

        return json_schema
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def dataclass_schema(self, schema: core_schema.DataclassSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema that defines a dataclass.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """

        cls = schema['cls']
        # If (stdlib) dataclass doesn't have config, the parent's config is used (as during core schema generation):
        config = cast('ConfigDict | None', getattr(cls, '__pydantic_config__', None))

        with self._config_wrapper_stack.push(config):
            json_schema = self.generate_inner(schema['schema']).copy()

        self._update_class_schema(json_schema, cls, config or {})

        return json_schema
```


---

### 🔹 Commit #14: `bb6da4cf`
- **完整 Hash**: `bb6da4cfbb1f559885ea2fa207ec93853bfeac64`
- **說明 (Ground Truth)**: Handle `TypeError` gracefully during docstring extraction (#13874)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/_internal/_docs_extraction.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:17, E:18, A:0) ➔ After(N:17, E:18, A:0)
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

### 🔹 函式: `extract_docstrings_from_cls()`
- **變更前簽章 (Before)**: `def extract_docstrings_from_cls(cls: type[Any], use_inspect: bool = False) -> dict[str, str]` (L82~L113)
- **變更後簽章 (After)**: `def extract_docstrings_from_cls(cls: type[Any], use_inspect: bool = False) -> dict[str, str]` (L82~L113)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def extract_docstrings_from_cls(cls: type[Any], use_inspect: bool = False) -> dict[str, str]:
    """Map model attributes and their corresponding docstring.

    Args:
        cls: The class of the Pydantic model to inspect.
        use_inspect: Whether to skip usage of frames to find the object and use
            the `inspect` module instead.

    Returns:
        A mapping containing attribute names and their corresponding docstring.
    """
    if use_inspect or sys.version_info >= (3, 13):
        # On Python < 3.13, `inspect.getsourcelines()` might not work as expected
        # if two classes have the same name in the same source file.
        # On Python 3.13+, it will use the new `__firstlineno__` class attribute,
        # making it way more robust.
        try:
            source, _ = inspect.getsourcelines(cls)
        except OSError:  # pragma: no cover
            return {}
    else:
        # TODO remove this implementation when we drop support for Python 3.12:
        source = _extract_source_from_frame(cls)

    if not source:
        return {}

    dedent_source = _dedent_source_lines(source)

    visitor = DocstringVisitor()
    visitor.visit(ast.parse(dedent_source))
    return visitor.attrs
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def extract_docstrings_from_cls(cls: type[Any], use_inspect: bool = False) -> dict[str, str]:
    """Map model attributes and their corresponding docstring.

    Args:
        cls: The class of the Pydantic model to inspect.
        use_inspect: Whether to skip usage of frames to find the object and use
            the `inspect` module instead.

    Returns:
        A mapping containing attribute names and their corresponding docstring.
    """
    if use_inspect or sys.version_info >= (3, 13):
        # On Python < 3.13, `inspect.getsourcelines()` might not work as expected
        # if two classes have the same name in the same source file.
        # On Python 3.13+, it will use the new `__firstlineno__` class attribute,
        # making it way more robust.
        try:
            source, _ = inspect.getsourcelines(cls)
        except (OSError, TypeError):  # pragma: no cover
            return {}
    else:
        # TODO remove this implementation when we drop support for Python 3.12:
        source = _extract_source_from_frame(cls)

    if not source:
        return {}

    dedent_source = _dedent_source_lines(source)

    visitor = DocstringVisitor()
    visitor.visit(ast.parse(dedent_source))
    return visitor.attrs
```


---

### 🔹 Commit #15: `65d67541`
- **完整 Hash**: `65d67541fee3aea55b0dbd9ad31629f005b22f2d`
- **說明 (Ground Truth)**: Add support for `multiple_of` constraint in `fraction` and `timedelta` core schemas (#13873)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/_internal/_known_annotated_metadata.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:32, E:35, A:0) ➔ After(N:32, E:35, A:0)
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

### 🔹 Commit #16: `5cca2176`
- **完整 Hash**: `5cca21767e47284a53d8c982af5424c70cbe4be3`
- **說明 (Ground Truth)**: Consistently use `Dict` in `BaseModel` type annotations (#13853)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/main.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:140, E:183, A:0) ➔ After(N:140, E:183, A:0)
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

### 🔹 Commit #17: `afff1eb7`
- **完整 Hash**: `afff1eb7040e568de521d05ebd8b8747f96ad9d9`
- **說明 (Ground Truth)**: Always pop field name and model type stacks during schema generation (#13859)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/_internal/_generate_schema.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:302, E:565, A:0) ➔ After(N:302, E:565, A:0)
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

### 🔹 函式: `_ModelTypeStack.push()`
- **變更前簽章 (Before)**: `def push(self, type_obj: type) -> Iterator[None]` (L2930~L2933)
- **變更後簽章 (After)**: `def push(self, type_obj: type) -> Iterator[None]` (L2932~L2937)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def push(self, type_obj: type) -> Iterator[None]:
        self._stack.append(type_obj)
        yield
        self._stack.pop()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def push(self, type_obj: type) -> Iterator[None]:
        self._stack.append(type_obj)
        try:
            yield
        finally:
            self._stack.pop()
```

### 🔹 函式: `_FieldNameStack.push()`
- **變更前簽章 (Before)**: `def push(self, field_name: str) -> Iterator[None]` (L2911~L2914)
- **變更後簽章 (After)**: `def push(self, field_name: str) -> Iterator[None]` (L2911~L2916)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def push(self, field_name: str) -> Iterator[None]:
        self._stack.append(field_name)
        yield
        self._stack.pop()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def push(self, field_name: str) -> Iterator[None]:
        self._stack.append(field_name)
        try:
            yield
        finally:
            self._stack.pop()
```


---

### 🔹 Commit #18: `dae7e206`
- **完整 Hash**: `dae7e2065283db4d3d677ebae9d2dc8423131c62`
- **說明 (Ground Truth)**: Fix dead isinstance check in `_decorator_infos_for_class()` (#13858)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/_internal/_decorators.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:70, E:92, A:0) ➔ After(N:70, E:92, A:0)
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

### 🔹 函式: `_decorator_infos_for_class()`
- **變更前簽章 (Before)**: `def _decorator_infos_for_class( typ: type[Any], *, cls_ref: Callable[[], str], collect_to_replace: bool, ) -> tuple[DecoratorInfos, list[tuple[str, Any]]]` (L528~L580)
- **變更後簽章 (After)**: `def _decorator_infos_for_class( typ: type[Any], *, cls_ref: Callable[[], str], collect_to_replace: bool, ) -> tuple[DecoratorInfos, list[tuple[str, Any]]]` (L528~L580)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _decorator_infos_for_class(
    typ: type[Any],
    *,
    cls_ref: Callable[[], str],
    collect_to_replace: bool,
) -> tuple[DecoratorInfos, list[tuple[str, Any]]]:
    """Collect a `DecoratorInfos` for class, without looking into bases."""
    res = DecoratorInfos()
    to_replace: list[tuple[str, Any]] = []

    # Iterate on the vars with a copy to avoid changes in dictionary size during iteration.
    # This can happen if a concurrent thread has Pydantic processing the same `typ` (e.g. two
    # concurrent threads doing `TypeAdapter(SomeClassType)`), and such thread reads annotations
    # for the first time during the iteration here in the other thread (since 3.14, reading annotations
    # can set attributes such as `__annotations_cache__` or `__annotate_func__` to the type).
    for var_name, var_value in vars(typ).copy().items():
        if isinstance(var_value, PydanticDescriptorProxy):
            info = var_value.decorator_info
            if isinstance(info, ValidatorDecoratorInfo):
                res.validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, FieldValidatorDecoratorInfo):
                res.field_validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, RootValidatorDecoratorInfo):
                res.root_validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, FieldSerializerDecoratorInfo):
                res.field_serializers[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, ModelValidatorDecoratorInfo):
                res.model_validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, ModelSerializerDecoratorInfo):
                res.model_serializers[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            else:
                from ..fields import ComputedFieldInfo

                isinstance(var_value, ComputedFieldInfo)
                res.computed_fields[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=None, info=info
                )
            if collect_to_replace:
                to_replace.append((var_name, var_value.wrapped))

    return res, to_replace
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _decorator_infos_for_class(
    typ: type[Any],
    *,
    cls_ref: Callable[[], str],
    collect_to_replace: bool,
) -> tuple[DecoratorInfos, list[tuple[str, Any]]]:
    """Collect a `DecoratorInfos` for class, without looking into bases."""
    res = DecoratorInfos()
    to_replace: list[tuple[str, Any]] = []

    # Iterate on the vars with a copy to avoid changes in dictionary size during iteration.
    # This can happen if a concurrent thread has Pydantic processing the same `typ` (e.g. two
    # concurrent threads doing `TypeAdapter(SomeClassType)`), and such thread reads annotations
    # for the first time during the iteration here in the other thread (since 3.14, reading annotations
    # can set attributes such as `__annotations_cache__` or `__annotate_func__` to the type).
    for var_name, var_value in vars(typ).copy().items():
        if isinstance(var_value, PydanticDescriptorProxy):
            info = var_value.decorator_info
            if isinstance(info, ValidatorDecoratorInfo):
                res.validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, FieldValidatorDecoratorInfo):
                res.field_validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, RootValidatorDecoratorInfo):
                res.root_validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, FieldSerializerDecoratorInfo):
                res.field_serializers[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, ModelValidatorDecoratorInfo):
                res.model_validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, ModelSerializerDecoratorInfo):
                res.model_serializers[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            else:
                from ..fields import ComputedFieldInfo

                assert isinstance(info, ComputedFieldInfo)
                res.computed_fields[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=None, info=info
                )
            if collect_to_replace:
                to_replace.append((var_name, var_value.wrapped))

    return res, to_replace
```


---

### 🔹 Commit #19: `831893ed`
- **完整 Hash**: `831893ed0411d45c20aacae88e067c9c33a89501`
- **說明 (Ground Truth)**: Fix race conditions in freethreaded build (#13785)
- **變更檔案數**: 3

#### 📄 檔案: `pydantic/_internal/_decorators.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:70, E:91, A:0) ➔ After(N:70, E:92, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `_decorator_infos_for_class` ──[CALLS]──> `copy (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_decorator_infos_for_class()`
- **變更前簽章 (Before)**: `def _decorator_infos_for_class( typ: type[Any], *, cls_ref: Callable[[], str], collect_to_replace: bool, ) -> tuple[DecoratorInfos, list[tuple[str, Any]]]` (L528~L575)
- **變更後簽章 (After)**: `def _decorator_infos_for_class( typ: type[Any], *, cls_ref: Callable[[], str], collect_to_replace: bool, ) -> tuple[DecoratorInfos, list[tuple[str, Any]]]` (L528~L580)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _decorator_infos_for_class(
    typ: type[Any],
    *,
    cls_ref: Callable[[], str],
    collect_to_replace: bool,
) -> tuple[DecoratorInfos, list[tuple[str, Any]]]:
    """Collect a `DecoratorInfos` for class, without looking into bases."""
    res = DecoratorInfos()
    to_replace: list[tuple[str, Any]] = []

    for var_name, var_value in vars(typ).items():
        if isinstance(var_value, PydanticDescriptorProxy):
            info = var_value.decorator_info
            if isinstance(info, ValidatorDecoratorInfo):
                res.validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, FieldValidatorDecoratorInfo):
                res.field_validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, RootValidatorDecoratorInfo):
                res.root_validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, FieldSerializerDecoratorInfo):
                res.field_serializers[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, ModelValidatorDecoratorInfo):
                res.model_validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, ModelSerializerDecoratorInfo):
                res.model_serializers[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            else:
                from ..fields import ComputedFieldInfo

                isinstance(var_value, ComputedFieldInfo)
                res.computed_fields[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=None, info=info
                )
            if collect_to_replace:
                to_replace.append((var_name, var_value.wrapped))

    return res, to_replace
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _decorator_infos_for_class(
    typ: type[Any],
    *,
    cls_ref: Callable[[], str],
    collect_to_replace: bool,
) -> tuple[DecoratorInfos, list[tuple[str, Any]]]:
    """Collect a `DecoratorInfos` for class, without looking into bases."""
    res = DecoratorInfos()
    to_replace: list[tuple[str, Any]] = []

    # Iterate on the vars with a copy to avoid changes in dictionary size during iteration.
    # This can happen if a concurrent thread has Pydantic processing the same `typ` (e.g. two
    # concurrent threads doing `TypeAdapter(SomeClassType)`), and such thread reads annotations
    # for the first time during the iteration here in the other thread (since 3.14, reading annotations
    # can set attributes such as `__annotations_cache__` or `__annotate_func__` to the type).
    for var_name, var_value in vars(typ).copy().items():
        if isinstance(var_value, PydanticDescriptorProxy):
            info = var_value.decorator_info
            if isinstance(info, ValidatorDecoratorInfo):
                res.validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, FieldValidatorDecoratorInfo):
                res.field_validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, RootValidatorDecoratorInfo):
                res.root_validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, FieldSerializerDecoratorInfo):
                res.field_serializers[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, ModelValidatorDecoratorInfo):
                res.model_validators[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, ModelSerializerDecoratorInfo):
                res.model_serializers[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=var_value.shim, info=info
                )
            else:
                from ..fields import ComputedFieldInfo

                isinstance(var_value, ComputedFieldInfo)
                res.computed_fields[var_name] = Decorator.build(
                    typ, cls_ref=cls_ref(), cls_var_name=var_name, shim=None, info=info
                )
            if collect_to_replace:
                to_replace.append((var_name, var_value.wrapped))

    return res, to_replace
```


#### 📄 檔案: `pydantic/_internal/_namespace_utils.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:15, E:8, A:0) ➔ After(N:16, E:9, A:0)
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
  • + [新增節點] `copy (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `LazyLocalNamespace.data` ──[CALLS]──> `copy (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `LazyLocalNamespace.data()`
- **變更前簽章 (Before)**: `def data(self) -> dict[str, Any]` (L90~L91)
- **變更後簽章 (After)**: `def data(self) -> dict[str, Any]: # In rare scenarios, a race condition can happen when iterating over class namespaces (i.e. created with `var(SomeClass)`), # if another thread accesses the type annotations for the first time (since 3.14, reading annotations can set attributes # such as `__annotations_cache__` or `__annotate_func__` to the type).` (L91~L97)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def data(self) -> dict[str, Any]:
        return {k: v for ns in self._namespaces for k, v in ns.items()}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def data(self) -> dict[str, Any]:
        # In rare scenarios, a race condition can happen when iterating over class namespaces (i.e. created with `var(SomeClass)`),
        # if another thread accesses the type annotations for the first time (since 3.14, reading annotations can set attributes
        # such as `__annotations_cache__` or `__annotate_func__` to the type).
        return {
            k: v for ns in self._namespaces for k, v in (ns.copy() if isinstance(ns, MappingProxyType) else ns).items()
        }
```


#### 📄 檔案: `pydantic/main.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:140, E:184, A:0) ➔ After(N:140, E:183, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 1, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `set_model_mocks (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `delattr (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `BaseModel.model_rebuild` ──[CALLS]──> `set_model_mocks (External/Unresolved)`
  • - [移除呼叫邊] `BaseModel.model_rebuild` ──[CALLS]──> `getattr (External/Unresolved)`
  • - [移除呼叫邊] `BaseModel.model_rebuild` ──[CALLS]──> `delattr (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `BaseModel.model_rebuild()`
- **變更前簽章 (Before)**: `def model_rebuild( cls, *, force: bool = False, raise_errors: bool = True, _parent_namespace_depth: int = 2, _types_namespace: MappingNamespace | None = None, ) -> bool | None` (L678~L748)
- **變更後簽章 (After)**: `def model_rebuild( cls, *, force: bool = False, raise_errors: bool = True, _parent_namespace_depth: int = 2, _types_namespace: MappingNamespace | None = None, ) -> bool | None` (L678~L744)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def model_rebuild(
        cls,
        *,
        force: bool = False,
        raise_errors: bool = True,
        _parent_namespace_depth: int = 2,
        _types_namespace: MappingNamespace | None = None,
    ) -> bool | None:
        """Try to rebuild the pydantic-core schema for the model.

        This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
        the initial attempt to build the schema, and automatic rebuilding fails.

        Args:
            force: Whether to force the rebuilding of the model schema, defaults to `False`.
            raise_errors: Whether to raise errors, defaults to `True`.
            _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
            _types_namespace: The types namespace, defaults to `None`.

        Returns:
            Returns `None` if the schema is already "complete" and rebuilding was not required.
            If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
        """
        # As the rebuild lock is global (not per model class), avoid needlessly holding it if the model is
        # already complete:
        if cls.__pydantic_complete__ and not force:
            return None

        with _rebuild_lock:
            # Re-check inside the lock, as another thread may have rebuilt the model while we were waiting:
            already_complete = cls.__pydantic_complete__
            if already_complete and not force:
                return None

            cls.__pydantic_complete__ = False

            for attr in ('__pydantic_core_schema__', '__pydantic_validator__', '__pydantic_serializer__'):
                if attr in cls.__dict__ and not isinstance(
                    getattr(cls, attr), (_mock_val_ser.MockCoreSchema, _mock_val_ser.MockValSer)
                ):
                    # Deleting the validator/serializer is necessary as otherwise they can get reused in
                    # pydantic-core. Same applies for the core schema that can be reused in schema generation.
                    # We do so only if they aren't mock instances, otherwise concurrent reads of these attributes
                    # — performed without holding the rebuild lock (e.g. when instantiating the model) — can
                    # resolve them from the parent class.
                    delattr(cls, attr)

            if _types_namespace is not None:
                rebuild_ns = _types_namespace
            elif _parent_namespace_depth > 0:
                rebuild_ns = (
                    _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}
                )
            else:
                rebuild_ns = {}

            parent_ns = _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

            ns_resolver = _namespace_utils.NsResolver(
                parent_namespace={**rebuild_ns, **parent_ns},
            )

            return _model_construction.complete_model_class(
                cls,
                _config.ConfigWrapper(cls.model_config, check=False),
                ns_resolver,
                raise_errors=raise_errors,
                # If the model was already complete, we don't need to call the hook again.
                call_on_complete_hook=not already_complete,
                is_force_rebuild=force,
            )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def model_rebuild(
        cls,
        *,
        force: bool = False,
        raise_errors: bool = True,
        _parent_namespace_depth: int = 2,
        _types_namespace: MappingNamespace | None = None,
    ) -> bool | None:
        """Try to rebuild the pydantic-core schema for the model.

        This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
        the initial attempt to build the schema, and automatic rebuilding fails.

        Args:
            force: Whether to force the rebuilding of the model schema, defaults to `False`.
            raise_errors: Whether to raise errors, defaults to `True`.
            _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
            _types_namespace: The types namespace, defaults to `None`.

        Returns:
            Returns `None` if the schema is already "complete" and rebuilding was not required.
            If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
        """
        # As the rebuild lock is global (not per model class), avoid needlessly holding it if the model is
        # already complete:
        if cls.__pydantic_complete__ and not force:
            return None

        with _rebuild_lock:
            # Re-check inside the lock, as another thread may have rebuilt the model while we were waiting:
            already_complete = cls.__pydantic_complete__
            if already_complete and not force:
                return None

            cls.__pydantic_complete__ = False

            if already_complete:
                # The existing validator/serializer must not be reused in pydantic-core, and the core schema
                # must not be reused in schema generation. If the model is already complete (i.e. `force=True`),
                # we set back mocks for the model (we could also delete the complete core schema/validator/serializer,
                # but this isn't thread-safe).
                _mock_val_ser.set_model_mocks(cls)

            if _types_namespace is not None:
                rebuild_ns = _types_namespace
            elif _parent_namespace_depth > 0:
                rebuild_ns = (
                    _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}
                )
            else:
                rebuild_ns = {}

            parent_ns = _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

            ns_resolver = _namespace_utils.NsResolver(
                parent_namespace={**rebuild_ns, **parent_ns},
            )

            return _model_construction.complete_model_class(
                cls,
                _config.ConfigWrapper(cls.model_config, check=False),
                ns_resolver,
                raise_errors=raise_errors,
                # If the model was already complete, we don't need to call the hook again.
                call_on_complete_hook=not already_complete,
                is_force_rebuild=force,
            )
```


---

### 🔹 Commit #20: `e2683e14`
- **完整 Hash**: `e2683e14d3c449cc74cde3efc94bf19f4ee9d95f`
- **說明 (Ground Truth)**: Refactor `Decimal` JSON Schema `pattern` constraint (#13672)
- **變更檔案數**: 1

#### 📄 檔案: `pydantic/json_schema.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:209, E:313, A:0) ➔ After(N:217, E:325, A:0)
- **差分統計**: +Nodes: 9, -Nodes: 1, +Edges: 14, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `GenerateJsonSchema.build_decimal_pattern` (FUNCTION_DEF)
  • + [新增節點] `_repeat` (FUNCTION_DEF)
  • + [新增節點] `_decimal_validation_pattern` (FUNCTION_DEF)
  • + [新增節點] `enumerate (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `GenerateJsonSchema.get_decimal_pattern` (FUNCTION_DEF)
  • + [新增節點] `_decimal_serialization_pattern` (FUNCTION_DEF)
  • + [新增節點] `_int_range_pattern` (FUNCTION_DEF)
  • + [新增節點] `frac_part` (FUNCTION_DEF)
  • + [新增節點] `min (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `GenerateJsonSchema.get_decimal_pattern` (FUNCTION_DEF)
  • + [新增呼叫邊] `GenerateJsonSchema.decimal_schema` ──[CALLS]──> `GenerateJsonSchema.get_decimal_pattern`
  • + [新增呼叫邊] `GenerateJsonSchema.build_decimal_pattern` ──[CALLS]──> `_decimal_validation_pattern`
  • + [新增呼叫邊] `GenerateJsonSchema.build_decimal_pattern` ──[CALLS]──> `_decimal_serialization_pattern`
  • + [新增呼叫邊] `_int_range_pattern` ──[CALLS]──> `_repeat`
  • + [新增呼叫邊] `_int_range_pattern` ──[CALLS]──> `enumerate (External/Unresolved)`
  • _... 以及其餘 11 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `GenerateJsonSchema.decimal_schema()`
- **變更前簽章 (Before)**: `def decimal_schema(self, schema: core_schema.DecimalSchema) -> JsonSchemaValue` (L717~L790)
- **變更後簽章 (After)**: `def decimal_schema(self, schema: core_schema.DecimalSchema) -> JsonSchemaValue` (L717~L752)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def decimal_schema(self, schema: core_schema.DecimalSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a decimal value.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """

        def get_decimal_pattern(schema: core_schema.DecimalSchema) -> str:
            max_digits = schema.get('max_digits')
            decimal_places = schema.get('decimal_places')

            pattern = (
                r'^(?!^[-+.]*$)[+-]?0*'  # check it is not empty string and not one or sequence of ".+-" characters.
            )

            # Case 1: Both max_digits and decimal_places are set
            if max_digits is not None and decimal_places is not None:
                integer_places = max(0, max_digits - decimal_places)
                pattern += (
                    rf'(?:'
                    rf'\d{{0,{integer_places}}}'
                    rf'|'
                    rf'(?=[\d.]{{1,{max_digits + 1}}}0*$)'
                    rf'\d{{0,{integer_places}}}\.\d{{0,{decimal_places}}}0*$'
                    rf')'
                )

            # Case 2: Only max_digits is set
            elif max_digits is not None and decimal_places is None:
                pattern += (
                    rf'(?:'
                    rf'\d{{0,{max_digits}}}'
                    rf'|'
                    rf'(?=[\d.]{{1,{max_digits + 1}}}0*$)'
                    rf'\d*\.\d*0*$'
                    rf')'
                )

            # Case 3: Only decimal_places is set
            elif max_digits is None and decimal_places is not None:
                pattern += rf'\d*\.?\d{{0,{decimal_places}}}0*$'

            # Case 4: Both are None (no restrictions)
            else:
                pattern += r'\d*\.?\d*$'  # look for arbitrary integer or decimal

            return pattern

        json_schema = self.str_schema(core_schema.str_schema(pattern=get_decimal_pattern(schema)))
        if self.mode == 'validation':
            multiple_of = schema.get('multiple_of')
            le = schema.get('le')
            ge = schema.get('ge')
            lt = schema.get('lt')
            gt = schema.get('gt')
            json_schema = {
                'anyOf': [
                    self.float_schema(
                        core_schema.float_schema(
                            allow_inf_nan=schema.get('allow_inf_nan'),
                            multiple_of=None if multiple_of is None else float(multiple_of),
                            le=None if le is None else float(le),
                            ge=None if ge is None else float(ge),
                            lt=None if lt is None else float(lt),
                            gt=None if gt is None else float(gt),
                        )
                    ),
                    json_schema,
                ],
            }
        return json_schema
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def decimal_schema(self, schema: core_schema.DecimalSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a decimal value.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """
        str_schema = core_schema.str_schema()
        pattern = self.get_decimal_pattern(schema)
        if pattern is not None:
            str_schema['pattern'] = pattern
        json_schema = self.str_schema(str_schema)
        if self.mode == 'validation':
            multiple_of = schema.get('multiple_of')
            le = schema.get('le')
            ge = schema.get('ge')
            lt = schema.get('lt')
            gt = schema.get('gt')
            json_schema = {
                'anyOf': [
                    self.float_schema(
                        core_schema.float_schema(
                            allow_inf_nan=schema.get('allow_inf_nan'),
                            multiple_of=None if multiple_of is None else float(multiple_of),
                            le=None if le is None else float(le),
                            ge=None if ge is None else float(ge),
                            lt=None if lt is None else float(lt),
                            gt=None if gt is None else float(gt),
                        )
                    ),
                    json_schema,
                ],
            }
        return json_schema
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/pydantic show 834e800cda72c264a1476d25dfbf892a9a2614ef
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 834e800cda72c264a1476d25dfbf892a9a2614ef~1 --file test_repos/pydantic/pydantic/mypy.py
   ```
