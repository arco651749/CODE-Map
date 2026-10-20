# 🔬 CODE-Map 基準審查獨立驗證報告: `RestSharp`
> **技術生態**: `C# (旗艦非同步 HTTP 客戶端 / 請求管線)`  
> **本地倉庫路徑**: `test_repos/RestSharp`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 33 Files  
> **報告生成時間**: 2026-10-20 21:42:21  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `21` / `33` | `63.6%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `3` / `33` | `9.1%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `9` / `33` | `27.3%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`24` / `33`** | **`72.7%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `33` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `2370d2ef`
- **完整 Hash**: `2370d2ef453f64bd10da9ab7a924e92e8b667978`
- **說明 (Ground Truth)**: Fix #2400: AddObjectStatic throwing on null property values (#2401)
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp/Request/PropertyCache.Populator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:83, E:116, A:0) ➔ After(N:84, E:117, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 1, +Edges: 3, -Edges: 2, ΔFuncs: 15, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `populate (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `getEnumerable(value).Cast<V> (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `getEnumerable(entity).Cast<V> (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Populator.From` ──[CALLS]──> `getObject (External/BCL)`
  • + [新增呼叫邊] `Populator.From` ──[CALLS]──> `populate (External/BCL)`
  • + [新增呼叫邊] `Populator.GetEnumerableOf` ──[CALLS]──> `getEnumerable(value).Cast<V> (External/BCL)`
  • - [移除呼叫邊] `Populator.GetPopulate` ──[CALLS]──> `getObject (External/BCL)`
  • - [移除呼叫邊] `Populator.GetEnumerableOf` ──[CALLS]──> `getEnumerable(entity).Cast<V> (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Populator.GetPopulate()`
- **變更前簽章 (Before)**: `Populator.GetPopulate(Func<T, object> getObject, PropertyInfo property)` (L114~L139)
- **變更後簽章 (After)**: `Populator.GetPopulate(PropertyInfo property)` (L123~L148)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulate(Func<T, object> getObject, PropertyInfo property) {
            var requestProperty = RequestProperty.From(property);

            // We need to use different conversion mechanisms for each return type. Simply calling `.ToString()`
            // on every returned object would not take into account special cases like custom formatting, enumeration etc.
            // Unchecked casts here are safe because we know the return type of `getObject` is boxed if needed.
            return property.PropertyType switch {
                var formattableType when typeof(IFormattable).IsAssignableFrom(formattableType) => GetPopulate(
                    entity => Unsafe.As<IFormattable>(getObject(entity)),
                    requestProperty
                ),
                var convertibleType when typeof(IConvertible).IsAssignableFrom(convertibleType) => GetPopulate(
                    entity => Unsafe.As<IConvertible>(getObject(entity)),
                    requestProperty
                ),
                var enumerableType when typeof(IEnumerable).IsAssignableFrom(enumerableType) => GetPopulateUnknown(
                    entity => Unsafe.As<IEnumerable>(getObject(entity)),
                    requestProperty
                ),
                // At this point we're not necessarily sure we can just treat this as a bare object
                // and use its type converter. Even though the property itself returns an object,
                // the object returned itself may need to be treated in a special way, so we check
                // it as we go.
                _ => GetPopulate(getObject, requestProperty)
            };
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulate(PropertyInfo property) {
            var requestProperty = RequestProperty.From(property);

            // We need to use different conversion mechanisms for each return type. Simply calling `.ToString()`
            // on every returned object would not take into account special cases like custom formatting, enumeration etc.
            // Unchecked casts here are safe because the property value is boxed if needed.
            return property.PropertyType switch {
                var formattableType when typeof(IFormattable).IsAssignableFrom(formattableType) => GetPopulate(
                    value => Unsafe.As<IFormattable>(value),
                    requestProperty
                ),
                var convertibleType when typeof(IConvertible).IsAssignableFrom(convertibleType) => GetPopulate(
                    value => Unsafe.As<IConvertible>(value),
                    requestProperty
                ),
                var enumerableType when typeof(IEnumerable).IsAssignableFrom(enumerableType) => GetPopulateUnknown(
                    value => Unsafe.As<IEnumerable>(value),
                    requestProperty
                ),
                // At this point we're not necessarily sure we can just treat this as a bare object
                // and use its type converter. Even though the property itself returns an object,
                // the object returned itself may need to be treated in a special way, so we check
                // it as we go.
                _ => GetPopulate(static value => value, requestProperty)
            };
        }
```

### 🔹 函式: `Populator.GetPopulate()`
- **變更前簽章 (Before)**: `Populator.GetPopulate(Func<T, IConvertible> getConvertible, RequestProperty requestProperty)` (L83~L84)
- **變更後簽章 (After)**: `Populator.GetPopulate(Func<object, IConvertible> getConvertible, RequestProperty requestProperty)` (L92~L93)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulate(Func<T, IConvertible> getConvertible, RequestProperty requestProperty)
            => (model, parameters) => Populate(getConvertible(model), requestProperty, parameters);
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulate(Func<object, IConvertible> getConvertible, RequestProperty requestProperty)
            => (value, parameters) => Populate(getConvertible(value), requestProperty, parameters);
```

### 🔹 函式: `Populator.GetPopulateUnknown()`
- **變更前簽章 (Before)**: `Populator.GetPopulateUnknown(Func<T, IEnumerable> getEnumerable, RequestProperty requestProperty)` (L141~L163)
- **變更後簽章 (After)**: `Populator.GetPopulateUnknown(Func<object, IEnumerable> getEnumerable, RequestProperty requestProperty)` (L150~L172)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulateUnknown(Func<T, IEnumerable> getEnumerable, RequestProperty requestProperty) {
            if (GetSingleEnumeratedTypeOrNull(requestProperty.Type) is not { } enumeratedType) {
                // Means we're dealing with a legacy, untyped enumerable instance.
                // We can just convert it into an enumerable of objects and delegate
                // conversion to string to the type converter of each enumerated item.
                return GetPopulateKnown(getEnumerable, requestProperty);
            }

            return enumeratedType switch {
                _ when typeof(IFormattable).IsAssignableFrom(enumeratedType) => GetPopulate(
                    GetEnumerableOf<IFormattable>(getEnumerable, enumeratedType),
                    requestProperty
                ),
                _ when typeof(IConvertible).IsAssignableFrom(enumeratedType) => GetPopulate(
                    GetEnumerableOf<IConvertible>(getEnumerable, enumeratedType),
                    requestProperty
                ),
                // At this point we're not necessarily sure we can just treat this as an enumerable of objects.
                // Since we know the actual enumerable may be a typed `IEnumerable<>` enumerating a type we're
                // interested in, we do further checks to ensure the correct conversion to string is applied.
                _ => GetPopulate(getEnumerable, requestProperty)
            };
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulateUnknown(Func<object, IEnumerable> getEnumerable, RequestProperty requestProperty) {
            if (GetSingleEnumeratedTypeOrNull(requestProperty.Type) is not { } enumeratedType) {
                // Means we're dealing with a legacy, untyped enumerable instance.
                // We can just convert it into an enumerable of objects and delegate
                // conversion to string to the type converter of each enumerated item.
                return GetPopulateKnown(getEnumerable, requestProperty);
            }

            return enumeratedType switch {
                _ when typeof(IFormattable).IsAssignableFrom(enumeratedType) => GetPopulate(
                    GetEnumerableOf<IFormattable>(getEnumerable, enumeratedType),
                    requestProperty
                ),
                _ when typeof(IConvertible).IsAssignableFrom(enumeratedType) => GetPopulate(
                    GetEnumerableOf<IConvertible>(getEnumerable, enumeratedType),
                    requestProperty
                ),
                // At this point we're not necessarily sure we can just treat this as an enumerable of objects.
                // Since we know the actual enumerable may be a typed `IEnumerable<>` enumerating a type we're
                // interested in, we do further checks to ensure the correct conversion to string is applied.
                _ => GetPopulate(getEnumerable, requestProperty)
            };
        }
```

### 🔹 函式: `Populator.GetPopulateArray()`
- **變更前簽章 (Before)**: `Populator.GetPopulateArray(Func<T, IEnumerable<IFormattable>> getFormattables, RequestProperty requestProperty)` (L176~L177)
- **變更後簽章 (After)**: `Populator.GetPopulateArray(
            Func<object, IEnumerable<IFormattable>> getFormattables,
            RequestProperty requestProperty
        )` (L185~L189)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulateArray(Func<T, IEnumerable<IFormattable>> getFormattables, RequestProperty requestProperty)
            => GetPopulateArray(getFormattables, formattable => GetStringValue(formattable, requestProperty), requestProperty);
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulateArray(
            Func<object, IEnumerable<IFormattable>> getFormattables,
            RequestProperty requestProperty
        )
            => GetPopulateArray(getFormattables, formattable => GetStringValue(formattable, requestProperty), requestProperty);
```

### 🔹 函式: `Populator.GetPopulate()`
- **變更前簽章 (Before)**: `Populator.GetPopulate(Func<T, object> getObject, RequestProperty requestProperty)` (L107~L112)
- **變更後簽章 (After)**: `Populator.GetPopulate(Func<object, object> getObject, RequestProperty requestProperty)` (L116~L121)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulate(Func<T, object> getObject, RequestProperty requestProperty)
            => requestProperty.ArrayQueryType switch {
                RequestArrayQueryType.CommaSeparated => (entity, parameters) => PopulateCsv(getObject(entity), requestProperty, parameters),
                RequestArrayQueryType.ArrayParameters => (entity, parameters) => PopulateArray(getObject(entity), requestProperty, parameters),
                _ => (_, _) => { }
            };
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulate(Func<object, object> getObject, RequestProperty requestProperty)
            => requestProperty.ArrayQueryType switch {
                RequestArrayQueryType.CommaSeparated => (value, parameters) => PopulateCsv(getObject(value), requestProperty, parameters),
                RequestArrayQueryType.ArrayParameters => (value, parameters) => PopulateArray(getObject(value), requestProperty, parameters),
                _ => (_, _) => { }
            };
```

### 🔹 函式: `Populator.GetPopulateKnown()`
- **變更前簽章 (Before)**: `Populator.GetPopulateKnown(Func<T, IEnumerable> getEnumerable, RequestProperty requestProperty)` (L165~L174)
- **變更後簽章 (After)**: `Populator.GetPopulateKnown(Func<object, IEnumerable> getEnumerable, RequestProperty requestProperty)` (L174~L183)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulateKnown(Func<T, IEnumerable> getEnumerable, RequestProperty requestProperty)
            => requestProperty.ArrayQueryType switch {
                RequestArrayQueryType.CommaSeparated => (entity, parameters) => PopulateCsvUnknown(
                    getEnumerable(entity),
                    requestProperty,
                    parameters
                ),
                RequestArrayQueryType.ArrayParameters => GetPopulateArray(getEnumerable, requestProperty),
                _ => (_, _) => { }
            };
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulateKnown(Func<object, IEnumerable> getEnumerable, RequestProperty requestProperty)
            => requestProperty.ArrayQueryType switch {
                RequestArrayQueryType.CommaSeparated => (value, parameters) => PopulateCsvUnknown(
                    getEnumerable(value),
                    requestProperty,
                    parameters
                ),
                RequestArrayQueryType.ArrayParameters => GetPopulateArray(getEnumerable, requestProperty),
                _ => (_, _) => { }
            };
```

### 🔹 函式: `Populator.GetPopulateArray()`
- **變更前簽章 (Before)**: `Populator.GetPopulateArray(Func<T, IEnumerable> getEnumerable, RequestProperty requestProperty)` (L192~L196)
- **變更後簽章 (After)**: `Populator.GetPopulateArray(Func<object, IEnumerable> getEnumerable, RequestProperty requestProperty)` (L207~L211)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulateArray(Func<T, IEnumerable> getEnumerable, RequestProperty requestProperty) {
            // We do this to avoid recreating request property on each iteration.
            var newRequestProperty = requestProperty with { Name = $"{requestProperty.Name}[]" };
            return (entity, parameters) => PopulateArray(getEnumerable(entity), newRequestProperty, parameters);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulateArray(Func<object, IEnumerable> getEnumerable, RequestProperty requestProperty) {
            // We do this to avoid recreating request property on each iteration.
            var newRequestProperty = requestProperty with { Name = $"{requestProperty.Name}[]" };
            return (value, parameters) => PopulateArray(getEnumerable(value), newRequestProperty, parameters);
        }
```

### 🔹 函式: `Populator.From()`
- **變更前簽章 (Before)**: `Populator.From(PropertyInfo property)` (L54~L78)
- **變更後簽章 (After)**: `Populator.From(PropertyInfo property)` (L54~L87)

#### ◀️ 變更前實作碼 (Before Implementation):
```
internal static Populator From(PropertyInfo property) {
            var entity = Expression.Parameter(typeof(T));
            var callGetter = Expression.Call(entity, property.GetGetMethod()!);

            Expression convertGetterReturnToObject =
                property.PropertyType.IsValueType
                    ?
                    // Values types are not automatically boxed in LINQ expressions.
                    // This would throw an exception.
                    Expression.Convert(callGetter, typeof(object))
                    :
                    // Avoid unnecessary cast to object if property is already a reference type.
                    callGetter;

            // This compiles roughly to: `(T entity) => (object)entity.get_Property()`,
            // where `.GetProperty()` is the getter. The reason we use LINQ expressions
            // instead of direct calls to the MethodInfo instance is for an increase in
            // performance. We can then leverage our knowledge of the type parameter provided.

            var getObject = Expression.Lambda<Func<T, object>>(convertGetterReturnToObject, entity).Compile();

            var populate = GetPopulate(getObject, property);

            return new(property.Name, populate);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal static Populator From(PropertyInfo property) {
            var entity = Expression.Parameter(typeof(T));
            var callGetter = Expression.Call(entity, property.GetGetMethod()!);

            Expression convertGetterReturnToObject =
                property.PropertyType.IsValueType
                    ?
                    // Values types are not automatically boxed in LINQ expressions.
                    // This would throw an exception.
                    Expression.Convert(callGetter, typeof(object))
                    :
                    // Avoid unnecessary cast to object if property is already a reference type.
                    callGetter;

            // This compiles roughly to: `(T entity) => (object)entity.get_Property()`,
            // where `.GetProperty()` is the getter. The reason we use LINQ expressions
            // instead of direct calls to the MethodInfo instance is for an increase in
            // performance. We can then leverage our knowledge of the type parameter provided.

            var getObject = Expression.Lambda<Func<T, object>>(convertGetterReturnToObject, entity).Compile();

            var populate = GetPopulate(property);

            // Skip null property values so a DTO with unset optional properties doesn't throw.
            // This matches the reflection-based AddObject.
            return new(
                property.Name,
                (model, parameters) => {
                    var value = getObject(model);
                    if (value is null) return;
                    populate(value, parameters);
                }
            );
        }
```

### 🔹 函式: `Populator.GetPopulateArray()`
- **變更前簽章 (Before)**: `Populator.GetPopulateArray(
            Func<T, IEnumerable<V>> getEnumerable,
            Func<V, string?> toString,
            RequestProperty requestProperty
        )` (L182~L190)
- **變更後簽章 (After)**: `Populator.GetPopulateArray(
            Func<object, IEnumerable<V>> getEnumerable,
            Func<V, string?> toString,
            RequestProperty requestProperty
        )` (L197~L205)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulateArray<V>(
            Func<T, IEnumerable<V>> getEnumerable,
            Func<V, string?> toString,
            RequestProperty requestProperty
        ) where V : class {
            // We do this to avoid recreating request property on each iteration.
            var newRequestProperty = requestProperty with { Name = $"{requestProperty.Name}[]" };
            return (entity, parameters) => PopulateArray(getEnumerable(entity), toString, newRequestProperty, parameters);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulateArray<V>(
            Func<object, IEnumerable<V>> getEnumerable,
            Func<V, string?> toString,
            RequestProperty requestProperty
        ) where V : class {
            // We do this to avoid recreating request property on each iteration.
            var newRequestProperty = requestProperty with { Name = $"{requestProperty.Name}[]" };
            return (value, parameters) => PopulateArray(getEnumerable(value), toString, newRequestProperty, parameters);
        }
```

### 🔹 函式: `Populator.GetPopulate()`
- **變更前簽章 (Before)**: `Populator.GetPopulate(Func<T, IEnumerable> getEnumerable, RequestProperty requestProperty)` (L100~L105)
- **變更後簽章 (After)**: `Populator.GetPopulate(Func<object, IEnumerable> getEnumerable, RequestProperty requestProperty)` (L109~L114)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulate(Func<T, IEnumerable> getEnumerable, RequestProperty requestProperty)
            => requestProperty.ArrayQueryType switch {
                RequestArrayQueryType.CommaSeparated => (entity, parameters) => PopulateCsv(getEnumerable(entity), requestProperty, parameters),
                RequestArrayQueryType.ArrayParameters => GetPopulateArray(getEnumerable, requestProperty),
                _ => (_, _) => { }
            };
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulate(Func<object, IEnumerable> getEnumerable, RequestProperty requestProperty)
            => requestProperty.ArrayQueryType switch {
                RequestArrayQueryType.CommaSeparated => (value, parameters) => PopulateCsv(getEnumerable(value), requestProperty, parameters),
                RequestArrayQueryType.ArrayParameters => GetPopulateArray(getEnumerable, requestProperty),
                _ => (_, _) => { }
            };
```

### 🔹 函式: `Populator.GetPopulate()`
- **變更前簽章 (Before)**: `Populator.GetPopulate(Func<T, IFormattable> getFormattable, RequestProperty requestProperty)` (L80~L81)
- **變更後簽章 (After)**: `Populator.GetPopulate(Func<object, IFormattable> getFormattable, RequestProperty requestProperty)` (L89~L90)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulate(Func<T, IFormattable> getFormattable, RequestProperty requestProperty)
            => (model, parameters) => Populate(getFormattable(model), requestProperty, parameters);
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulate(Func<object, IFormattable> getFormattable, RequestProperty requestProperty)
            => (value, parameters) => Populate(getFormattable(value), requestProperty, parameters);
```

### 🔹 函式: `Populator.GetPopulateArray()`
- **變更前簽章 (Before)**: `Populator.GetPopulateArray(Func<T, IEnumerable<IConvertible>> getConvertibles, RequestProperty requestProperty)` (L179~L180)
- **變更後簽章 (After)**: `Populator.GetPopulateArray(
            Func<object, IEnumerable<IConvertible>> getConvertibles,
            RequestProperty requestProperty
        )` (L191~L195)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulateArray(Func<T, IEnumerable<IConvertible>> getConvertibles, RequestProperty requestProperty)
            => GetPopulateArray(getConvertibles, GetStringValue, requestProperty);
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulateArray(
            Func<object, IEnumerable<IConvertible>> getConvertibles,
            RequestProperty requestProperty
        )
            => GetPopulateArray(getConvertibles, GetStringValue, requestProperty);
```

### 🔹 函式: `Populator.GetPopulate()`
- **變更前簽章 (Before)**: `Populator.GetPopulate(Func<T, IEnumerable<IFormattable>> getFormattables, RequestProperty requestProperty)` (L86~L91)
- **變更後簽章 (After)**: `Populator.GetPopulate(Func<object, IEnumerable<IFormattable>> getFormattables, RequestProperty requestProperty)` (L95~L100)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulate(Func<T, IEnumerable<IFormattable>> getFormattables, RequestProperty requestProperty)
            => requestProperty.ArrayQueryType switch {
                RequestArrayQueryType.CommaSeparated => (model, parameters) => PopulateCsv(getFormattables(model), requestProperty, parameters),
                RequestArrayQueryType.ArrayParameters => GetPopulateArray(getFormattables, requestProperty),
                _ => (_, _) => { }
            };
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulate(Func<object, IEnumerable<IFormattable>> getFormattables, RequestProperty requestProperty)
            => requestProperty.ArrayQueryType switch {
                RequestArrayQueryType.CommaSeparated => (value, parameters) => PopulateCsv(getFormattables(value), requestProperty, parameters),
                RequestArrayQueryType.ArrayParameters => GetPopulateArray(getFormattables, requestProperty),
                _ => (_, _) => { }
            };
```

### 🔹 函式: `Populator.GetEnumerableOf()`
- **變更前簽章 (Before)**: `Populator.GetEnumerableOf(Func<T, IEnumerable> getEnumerable, Type enumeratedType)` (L396~L397)
- **變更後簽章 (After)**: `Populator.GetEnumerableOf(Func<object, IEnumerable> getEnumerable, Type enumeratedType)` (L411~L412)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Func<T, IEnumerable<V>> GetEnumerableOf<V>(Func<T, IEnumerable> getEnumerable, Type enumeratedType) where V : class
            => enumeratedType.IsValueType ? entity => getEnumerable(entity).Cast<V>() : entity => Unsafe.As<IEnumerable<V>>(getEnumerable(entity));
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Func<object, IEnumerable<V>> GetEnumerableOf<V>(Func<object, IEnumerable> getEnumerable, Type enumeratedType) where V : class
            => enumeratedType.IsValueType ? value => getEnumerable(value).Cast<V>() : value => Unsafe.As<IEnumerable<V>>(getEnumerable(value));
```

### 🔹 函式: `Populator.GetPopulate()`
- **變更前簽章 (Before)**: `Populator.GetPopulate(Func<T, IEnumerable<IConvertible>> getConvertibles, RequestProperty requestProperty)` (L93~L98)
- **變更後簽章 (After)**: `Populator.GetPopulate(Func<object, IEnumerable<IConvertible>> getConvertibles, RequestProperty requestProperty)` (L102~L107)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static Action<T, ICollection<Parameter>> GetPopulate(Func<T, IEnumerable<IConvertible>> getConvertibles, RequestProperty requestProperty)
            => requestProperty.ArrayQueryType switch {
                RequestArrayQueryType.CommaSeparated => (entity, parameters) => PopulateCsv(getConvertibles(entity), requestProperty, parameters),
                RequestArrayQueryType.ArrayParameters => GetPopulateArray(getConvertibles, requestProperty),
                _ => (_, _) => { }
            };
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static Action<object, ICollection<Parameter>> GetPopulate(Func<object, IEnumerable<IConvertible>> getConvertibles, RequestProperty requestProperty)
            => requestProperty.ArrayQueryType switch {
                RequestArrayQueryType.CommaSeparated => (value, parameters) => PopulateCsv(getConvertibles(value), requestProperty, parameters),
                RequestArrayQueryType.ArrayParameters => GetPopulateArray(getConvertibles, requestProperty),
                _ => (_, _) => { }
            };
```


---

### 🔹 Commit #02: `a95bcea6`
- **完整 Hash**: `a95bcea6cecc2c50913b0a63c3076b2a4e3ab2cd`
- **說明 (Ground Truth)**: Remove CustomSynchronizationContext and use Task.Run for sync over async (#2371)
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp/AsyncHelpers.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:26, E:17, A:0) ➔ After(N:4, E:3, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 25, +Edges: 3, -Edges: 17, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Task.Run(func).GetAwaiter().GetResult (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `Task.Run (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `Task.Run(func).GetAwaiter (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `AsyncHelpers.RunSync` (FUNCTION_DEF)
  • - [移除節點] `_items.Enqueue (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `_workItemsWaiting.Set (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `_task (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `CustomSynchronizationContext.CreateCopy` (FUNCTION_DEF)
  • - [移除節點] `ExceptionDispatchInfo.Capture (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `_items.TryDequeue (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `CustomSynchronizationContext.Post` (FUNCTION_DEF)
  • - [移除節點] `_workItemsWaiting.WaitOne (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `_task().ConfigureAwait (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `CustomSynchronizationContext.PostCallback` (FUNCTION_DEF)
  • - [移除節點] `state_60` (MODULE_STATE)
  • _... 以及其餘 33 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `AsyncHelpers.RunSync()`
- **變更前簽章 (Before)**: `AsyncHelpers.RunSync(Func<Task> task)` (L27~L38)
- **變更後簽章 (After)**: `AsyncHelpers.RunSync(Func<Task<T>> func)` (L30~L32)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static void RunSync(Func<Task> task) {
        var currentContext = SynchronizationContext.Current;
        var customContext  = new CustomSynchronizationContext(task);

        try {
            SynchronizationContext.SetSynchronizationContext(customContext);
            customContext.Run();
        }
        finally {
            SynchronizationContext.SetSynchronizationContext(currentContext);
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static T RunSync<T>(Func<Task<T>> func) {
        return Task.Run(func).GetAwaiter().GetResult();
    }
```


---

### 🔹 Commit #03: `c362621b`
- **完整 Hash**: `c362621b172699270783dedc97d87dfd7d66d961`
- **說明 (Ground Truth)**: Add missing ConfigureAwait(false) to prevent deadlocks (#2367)
- **變更檔案數**: 3

#### 📄 檔案: `src/RestSharp/Extensions/HttpResponseExtensions.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:12, E:10, A:0) ➔ After(N:13, E:11, A:0)
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
  • + [新增節點] `reader.ReadToEndAsync().ConfigureAwait (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `GetResponseString` ──[CALLS]──> `reader.ReadToEndAsync().ConfigureAwait (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `GetResponseString()`
- **變更前簽章 (Before)**: `GetResponseString(this HttpResponseMessage response, byte[] bytes, Encoding clientEncoding)` (L30~L44)
- **變更後簽章 (After)**: `GetResponseString(this HttpResponseMessage response, byte[] bytes, Encoding clientEncoding)` (L30~L44)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static async Task<string> GetResponseString(this HttpResponseMessage response, byte[] bytes, Encoding clientEncoding) {
        var encodingString = response.Content.Headers.ContentType?.CharSet;
        var encoding       = encodingString != null ? TryGetEncoding(encodingString) : clientEncoding;

        using var reader = new StreamReader(new MemoryStream(bytes), encoding);
        return await reader.ReadToEndAsync();
        Encoding TryGetEncoding(string es) {
            try {
                return Encoding.GetEncoding(es);
            }
            catch {
                return Encoding.Default;
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static async Task<string> GetResponseString(this HttpResponseMessage response, byte[] bytes, Encoding clientEncoding) {
        var encodingString = response.Content.Headers.ContentType?.CharSet;
        var encoding       = encodingString != null ? TryGetEncoding(encodingString) : clientEncoding;

        using var reader = new StreamReader(new MemoryStream(bytes), encoding);
        return await reader.ReadToEndAsync().ConfigureAwait(false);
        Encoding TryGetEncoding(string es) {
            try {
                return Encoding.GetEncoding(es);
            }
            catch {
                return Encoding.Default;
            }
        }
    }
```


#### 📄 檔案: `src/RestSharp/Response/RestResponse.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:17, E:15, A:0) ➔ After(N:18, E:16, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `httpResponse.GetResponseString(bytes, options.Encoding).ConfigureAwait (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `RestResponse.GetDefaultResponse` ──[CALLS]──> `httpResponse.GetResponseString(bytes, options.Encoding).ConfigureAwait (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RestResponse.GetDefaultResponse()`
- **變更前簽章 (Before)**: `RestResponse.GetDefaultResponse()` (L49~L78)
- **變更後簽章 (After)**: `RestResponse.GetDefaultResponse()` (L49~L78)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async Task<RestResponse> GetDefaultResponse() {
#if NET
            await using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#else
            using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#endif

            var bytes   = stream == null ? null : await stream.ReadAsBytes(cancellationToken).ConfigureAwait(false);
            var content = bytes == null ? null : await httpResponse.GetResponseString(bytes, options.Encoding);

            return new(request) {
                Content             = content,
                ContentEncoding     = httpResponse.Content?.Headers.ContentEncoding ?? Array.Empty<string>(),
                ContentHeaders      = httpResponse.Content?.Headers.GetHeaderParameters(),
                ContentLength       = httpResponse.Content?.Headers.ContentLength,
                ContentType         = httpResponse.Content?.Headers.ContentType?.MediaType,
                Cookies             = cookieCollection,
                ErrorException      = httpResponse.MaybeException(options.SetErrorExceptionOnUnsuccessfulStatusCode),
                Headers             = httpResponse.Headers.GetHeaderParameters(),
                IsSuccessStatusCode = httpResponse.IsSuccessStatusCode,
                RawBytes            = bytes,
                ResponseStatus      = options.CalculateResponseStatus(httpResponse),
                ResponseUri         = GetResponseUri(httpResponse),
                RootElement         = request.RootElement,
                Server              = httpResponse.Headers.Server.ToString(),
                StatusCode          = httpResponse.StatusCode,
                StatusDescription   = httpResponse.ReasonPhrase,
                Version             = httpResponse.RequestMessage?.Version
            };
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async Task<RestResponse> GetDefaultResponse() {
#if NET
            await using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#else
            using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#endif

            var bytes   = stream == null ? null : await stream.ReadAsBytes(cancellationToken).ConfigureAwait(false);
            var content = bytes == null ? null : await httpResponse.GetResponseString(bytes, options.Encoding).ConfigureAwait(false);

            return new(request) {
                Content             = content,
                ContentEncoding     = httpResponse.Content?.Headers.ContentEncoding ?? Array.Empty<string>(),
                ContentHeaders      = httpResponse.Content?.Headers.GetHeaderParameters(),
                ContentLength       = httpResponse.Content?.Headers.ContentLength,
                ContentType         = httpResponse.Content?.Headers.ContentType?.MediaType,
                Cookies             = cookieCollection,
                ErrorException      = httpResponse.MaybeException(options.SetErrorExceptionOnUnsuccessfulStatusCode),
                Headers             = httpResponse.Headers.GetHeaderParameters(),
                IsSuccessStatusCode = httpResponse.IsSuccessStatusCode,
                RawBytes            = bytes,
                ResponseStatus      = options.CalculateResponseStatus(httpResponse),
                ResponseUri         = GetResponseUri(httpResponse),
                RootElement         = request.RootElement,
                Server              = httpResponse.Headers.Server.ToString(),
                StatusCode          = httpResponse.StatusCode,
                StatusDescription   = httpResponse.ReasonPhrase,
                Version             = httpResponse.RequestMessage?.Version
            };
        }
```

### 🔹 函式: `RestResponse.FromHttpResponse()`
- **變更前簽章 (Before)**: `RestResponse.FromHttpResponse(
        HttpResponseMessage       httpResponse,
        RestRequest               request,
        ReadOnlyRestClientOptions options,
        CookieCollection?         cookieCollection,
        CancellationToken         cancellationToken
    )` (L40~L79)
- **變更後簽章 (After)**: `RestResponse.FromHttpResponse(
        HttpResponseMessage       httpResponse,
        RestRequest               request,
        ReadOnlyRestClientOptions options,
        CookieCollection?         cookieCollection,
        CancellationToken         cancellationToken
    )` (L40~L79)

#### ◀️ 變更前實作碼 (Before Implementation):
```
internal static async Task<RestResponse> FromHttpResponse(
        HttpResponseMessage       httpResponse,
        RestRequest               request,
        ReadOnlyRestClientOptions options,
        CookieCollection?         cookieCollection,
        CancellationToken         cancellationToken
    ) {
        return request.AdvancedResponseWriter?.Invoke(httpResponse, request) ?? await GetDefaultResponse().ConfigureAwait(false);

        async Task<RestResponse> GetDefaultResponse() {
#if NET
            await using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#else
            using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#endif

            var bytes   = stream == null ? null : await stream.ReadAsBytes(cancellationToken).ConfigureAwait(false);
            var content = bytes == null ? null : await httpResponse.GetResponseString(bytes, options.Encoding);

            return new(request) {
                Content             = content,
                ContentEncoding     = httpResponse.Content?.Headers.ContentEncoding ?? Array.Empty<string>(),
                ContentHeaders      = httpResponse.Content?.Headers.GetHeaderParameters(),
                ContentLength       = httpResponse.Content?.Headers.ContentLength,
                ContentType         = httpResponse.Content?.Headers.ContentType?.MediaType,
                Cookies             = cookieCollection,
                ErrorException      = httpResponse.MaybeException(options.SetErrorExceptionOnUnsuccessfulStatusCode),
                Headers             = httpResponse.Headers.GetHeaderParameters(),
                IsSuccessStatusCode = httpResponse.IsSuccessStatusCode,
                RawBytes            = bytes,
                ResponseStatus      = options.CalculateResponseStatus(httpResponse),
                ResponseUri         = GetResponseUri(httpResponse),
                RootElement         = request.RootElement,
                Server              = httpResponse.Headers.Server.ToString(),
                StatusCode          = httpResponse.StatusCode,
                StatusDescription   = httpResponse.ReasonPhrase,
                Version             = httpResponse.RequestMessage?.Version
            };
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal static async Task<RestResponse> FromHttpResponse(
        HttpResponseMessage       httpResponse,
        RestRequest               request,
        ReadOnlyRestClientOptions options,
        CookieCollection?         cookieCollection,
        CancellationToken         cancellationToken
    ) {
        return request.AdvancedResponseWriter?.Invoke(httpResponse, request) ?? await GetDefaultResponse().ConfigureAwait(false);

        async Task<RestResponse> GetDefaultResponse() {
#if NET
            await using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#else
            using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#endif

            var bytes   = stream == null ? null : await stream.ReadAsBytes(cancellationToken).ConfigureAwait(false);
            var content = bytes == null ? null : await httpResponse.GetResponseString(bytes, options.Encoding).ConfigureAwait(false);

            return new(request) {
                Content             = content,
                ContentEncoding     = httpResponse.Content?.Headers.ContentEncoding ?? Array.Empty<string>(),
                ContentHeaders      = httpResponse.Content?.Headers.GetHeaderParameters(),
                ContentLength       = httpResponse.Content?.Headers.ContentLength,
                ContentType         = httpResponse.Content?.Headers.ContentType?.MediaType,
                Cookies             = cookieCollection,
                ErrorException      = httpResponse.MaybeException(options.SetErrorExceptionOnUnsuccessfulStatusCode),
                Headers             = httpResponse.Headers.GetHeaderParameters(),
                IsSuccessStatusCode = httpResponse.IsSuccessStatusCode,
                RawBytes            = bytes,
                ResponseStatus      = options.CalculateResponseStatus(httpResponse),
                ResponseUri         = GetResponseUri(httpResponse),
                RootElement         = request.RootElement,
                Server              = httpResponse.Headers.Server.ToString(),
                StatusCode          = httpResponse.StatusCode,
                StatusDescription   = httpResponse.ReasonPhrase,
                Version             = httpResponse.RequestMessage?.Version
            };
        }
    }
```


#### 📄 檔案: `src/RestSharp/RestClient.Extensions.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:23, E:31, A:0) ➔ After(N:24, E:32, A:0)
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
  • + [新增節點] `client.Serializers.Deserialize<T>(request, response, client.Options, cancellationToken).ConfigureAwait (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `ExecuteAsync` ──[CALLS]──> `client.Serializers.Deserialize<T>(request, response, client.Options, cancellationToken).ConfigureAwait (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `ExecuteAsync()`
- **變更前簽章 (Before)**: `ExecuteAsync(
            RestRequest       request,
            CancellationToken cancellationToken = default
        )` (L41~L49)
- **變更後簽章 (After)**: `ExecuteAsync(
            RestRequest       request,
            CancellationToken cancellationToken = default
        )` (L41~L49)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async Task<RestResponse<T>> ExecuteAsync<T>(
            RestRequest       request,
            CancellationToken cancellationToken = default
        ) {
            Ensure.NotNull(request, nameof(request));

            var response = await client.ExecuteAsync(request, cancellationToken).ConfigureAwait(false);
            return await client.Serializers.Deserialize<T>(request, response, client.Options, cancellationToken);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async Task<RestResponse<T>> ExecuteAsync<T>(
            RestRequest       request,
            CancellationToken cancellationToken = default
        ) {
            Ensure.NotNull(request, nameof(request));

            var response = await client.ExecuteAsync(request, cancellationToken).ConfigureAwait(false);
            return await client.Serializers.Deserialize<T>(request, response, client.Options, cancellationToken).ConfigureAwait(false);
        }
```


---

### 🔹 Commit #04: `04679523`
- **完整 Hash**: `046795231e33ca08c72cb906e9085b4e94bcbdae`
- **說明 (Ground Truth)**: Quote multipart form parameter names by default (RFC 7578) (#2357)
- **變更檔案數**: 2

#### 📄 檔案: `src/RestSharp/Request/RequestContent.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:58, E:63, A:0) ➔ After(N:58, E:63, A:0)
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

### 🔹 函式: `RequestContent.AddBody()`
- **變更前簽章 (Before)**: `RequestContent.AddBody(bool hasPostParameters, BodyParameter bodyParameter)` (L133~L157)
- **變更後簽章 (After)**: `RequestContent.AddBody(bool hasPostParameters, BodyParameter bodyParameter)` (L133~L157)

#### ◀️ 變更前實作碼 (Before Implementation):
```
void AddBody(bool hasPostParameters, BodyParameter bodyParameter) {
        var bodyContent = Serialize(bodyParameter);

        // we need to send the body
        if (hasPostParameters || request.HasFiles() || BodyShouldBeMultipartForm(bodyParameter) || request.AlwaysMultipartFormData) {
            // here we must use multipart form data
            var mpContent = Content as MultipartFormDataContent ?? CreateMultipartFormDataContent();
            var ct        = bodyContent.Headers.ContentType?.MediaType;
            var name      = bodyParameter.Name.IsEmpty() ? ct : bodyParameter.Name;

            if (name.IsEmpty())
                mpContent.Add(bodyContent);
            else
                mpContent.Add(bodyContent, name);
            Content = mpContent;
        }
        else {
            // we don't have parameters, only the body
            Content = bodyContent;
        }

        if (client.Options.DisableCharset) {
            Content.Headers.ContentType!.CharSet = "";
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
void AddBody(bool hasPostParameters, BodyParameter bodyParameter) {
        var bodyContent = Serialize(bodyParameter);

        // we need to send the body
        if (hasPostParameters || request.HasFiles() || BodyShouldBeMultipartForm(bodyParameter) || request.AlwaysMultipartFormData) {
            // here we must use multipart form data
            var mpContent = Content as MultipartFormDataContent ?? CreateMultipartFormDataContent();
            var ct        = bodyContent.Headers.ContentType?.MediaType;
            var name      = bodyParameter.Name.IsEmpty() ? ct : bodyParameter.Name;

            if (name.IsEmpty())
                mpContent.Add(bodyContent);
            else
                mpContent.Add(bodyContent, request.MultipartFormQuoteParameters ? $"\"{name}\"" : name);
            Content = mpContent;
        }
        else {
            // we don't have parameters, only the body
            Content = bodyContent;
        }

        if (client.Options.DisableCharset) {
            Content.Headers.ContentType!.CharSet = "";
        }
    }
```


#### 📄 檔案: `src/RestSharp/Request/RestRequest.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:22, E:15, A:0) ➔ After(N:22, E:15, A:0)
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

### 🔹 Commit #05: `53b797b4`
- **完整 Hash**: `53b797b41c8c58655d71cf7b2ab5b902577e85ff`
- **說明 (Ground Truth)**: Fix credential/UseDefaultCredentials property order on HttpClientHandler (#2353)
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp/RestClient.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:28, E:27, A:0) ➔ After(N:28, E:27, A:0)
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

### 🔹 Commit #06: `3831d523`
- **完整 Hash**: `3831d5237fd614cf0e57e64e113a180714448200`
- **說明 (Ground Truth)**: Document Timeout property behavior for RestClientOptions and RestRequest (#2331)
- **變更檔案數**: 2

#### 📄 檔案: `src/RestSharp/Options/RestClientOptions.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:7, E:2, A:0) ➔ After(N:7, E:2, A:0)
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

#### 📄 檔案: `src/RestSharp/Request/RestRequest.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:17, E:12, A:0) ➔ After(N:17, E:12, A:0)
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

### 🔹 Commit #07: `eb9e3d1f`
- **完整 Hash**: `eb9e3d1fe9b9097e249f83ed0e218f8198309700`
- **說明 (Ground Truth)**: Fix ResponseUri returning original URL instead of redirect target when FollowRedirects=false (#2346) (#2350)
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp/Response/RestResponse.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:16, E:14, A:0) ➔ After(N:17, E:15, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `RestResponse.GetResponseUri` (FUNCTION_DEF)
  • + [新增呼叫邊] `RestResponse.GetDefaultResponse` ──[CALLS]──> `RestResponse.GetResponseUri`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RestResponse.GetDefaultResponse()`
- **變更前簽章 (Before)**: `RestResponse.GetDefaultResponse()` (L49~L78)
- **變更後簽章 (After)**: `RestResponse.GetDefaultResponse()` (L49~L78)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async Task<RestResponse> GetDefaultResponse() {
#if NET
            await using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#else
            using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#endif

            var bytes   = stream == null ? null : await stream.ReadAsBytes(cancellationToken).ConfigureAwait(false);
            var content = bytes == null ? null : await httpResponse.GetResponseString(bytes, options.Encoding);

            return new(request) {
                Content             = content,
                ContentEncoding     = httpResponse.Content?.Headers.ContentEncoding ?? Array.Empty<string>(),
                ContentHeaders      = httpResponse.Content?.Headers.GetHeaderParameters(),
                ContentLength       = httpResponse.Content?.Headers.ContentLength,
                ContentType         = httpResponse.Content?.Headers.ContentType?.MediaType,
                Cookies             = cookieCollection,
                ErrorException      = httpResponse.MaybeException(options.SetErrorExceptionOnUnsuccessfulStatusCode),
                Headers             = httpResponse.Headers.GetHeaderParameters(),
                IsSuccessStatusCode = httpResponse.IsSuccessStatusCode,
                RawBytes            = bytes,
                ResponseStatus      = options.CalculateResponseStatus(httpResponse),
                ResponseUri         = httpResponse.RequestMessage?.RequestUri,
                RootElement         = request.RootElement,
                Server              = httpResponse.Headers.Server.ToString(),
                StatusCode          = httpResponse.StatusCode,
                StatusDescription   = httpResponse.ReasonPhrase,
                Version             = httpResponse.RequestMessage?.Version
            };
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async Task<RestResponse> GetDefaultResponse() {
#if NET
            await using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#else
            using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#endif

            var bytes   = stream == null ? null : await stream.ReadAsBytes(cancellationToken).ConfigureAwait(false);
            var content = bytes == null ? null : await httpResponse.GetResponseString(bytes, options.Encoding);

            return new(request) {
                Content             = content,
                ContentEncoding     = httpResponse.Content?.Headers.ContentEncoding ?? Array.Empty<string>(),
                ContentHeaders      = httpResponse.Content?.Headers.GetHeaderParameters(),
                ContentLength       = httpResponse.Content?.Headers.ContentLength,
                ContentType         = httpResponse.Content?.Headers.ContentType?.MediaType,
                Cookies             = cookieCollection,
                ErrorException      = httpResponse.MaybeException(options.SetErrorExceptionOnUnsuccessfulStatusCode),
                Headers             = httpResponse.Headers.GetHeaderParameters(),
                IsSuccessStatusCode = httpResponse.IsSuccessStatusCode,
                RawBytes            = bytes,
                ResponseStatus      = options.CalculateResponseStatus(httpResponse),
                ResponseUri         = GetResponseUri(httpResponse),
                RootElement         = request.RootElement,
                Server              = httpResponse.Headers.Server.ToString(),
                StatusCode          = httpResponse.StatusCode,
                StatusDescription   = httpResponse.ReasonPhrase,
                Version             = httpResponse.RequestMessage?.Version
            };
        }
```

### 🔹 函式: `RestResponse.FromHttpResponse()`
- **變更前簽章 (Before)**: `RestResponse.FromHttpResponse(
        HttpResponseMessage       httpResponse,
        RestRequest               request,
        ReadOnlyRestClientOptions options,
        CookieCollection?         cookieCollection,
        CancellationToken         cancellationToken
    )` (L40~L79)
- **變更後簽章 (After)**: `RestResponse.FromHttpResponse(
        HttpResponseMessage       httpResponse,
        RestRequest               request,
        ReadOnlyRestClientOptions options,
        CookieCollection?         cookieCollection,
        CancellationToken         cancellationToken
    )` (L40~L79)

#### ◀️ 變更前實作碼 (Before Implementation):
```
internal static async Task<RestResponse> FromHttpResponse(
        HttpResponseMessage       httpResponse,
        RestRequest               request,
        ReadOnlyRestClientOptions options,
        CookieCollection?         cookieCollection,
        CancellationToken         cancellationToken
    ) {
        return request.AdvancedResponseWriter?.Invoke(httpResponse, request) ?? await GetDefaultResponse().ConfigureAwait(false);

        async Task<RestResponse> GetDefaultResponse() {
#if NET
            await using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#else
            using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#endif

            var bytes   = stream == null ? null : await stream.ReadAsBytes(cancellationToken).ConfigureAwait(false);
            var content = bytes == null ? null : await httpResponse.GetResponseString(bytes, options.Encoding);

            return new(request) {
                Content             = content,
                ContentEncoding     = httpResponse.Content?.Headers.ContentEncoding ?? Array.Empty<string>(),
                ContentHeaders      = httpResponse.Content?.Headers.GetHeaderParameters(),
                ContentLength       = httpResponse.Content?.Headers.ContentLength,
                ContentType         = httpResponse.Content?.Headers.ContentType?.MediaType,
                Cookies             = cookieCollection,
                ErrorException      = httpResponse.MaybeException(options.SetErrorExceptionOnUnsuccessfulStatusCode),
                Headers             = httpResponse.Headers.GetHeaderParameters(),
                IsSuccessStatusCode = httpResponse.IsSuccessStatusCode,
                RawBytes            = bytes,
                ResponseStatus      = options.CalculateResponseStatus(httpResponse),
                ResponseUri         = httpResponse.RequestMessage?.RequestUri,
                RootElement         = request.RootElement,
                Server              = httpResponse.Headers.Server.ToString(),
                StatusCode          = httpResponse.StatusCode,
                StatusDescription   = httpResponse.ReasonPhrase,
                Version             = httpResponse.RequestMessage?.Version
            };
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal static async Task<RestResponse> FromHttpResponse(
        HttpResponseMessage       httpResponse,
        RestRequest               request,
        ReadOnlyRestClientOptions options,
        CookieCollection?         cookieCollection,
        CancellationToken         cancellationToken
    ) {
        return request.AdvancedResponseWriter?.Invoke(httpResponse, request) ?? await GetDefaultResponse().ConfigureAwait(false);

        async Task<RestResponse> GetDefaultResponse() {
#if NET
            await using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#else
            using var stream = await httpResponse.ReadResponseStream(request.ResponseWriter, cancellationToken).ConfigureAwait(false);
#endif

            var bytes   = stream == null ? null : await stream.ReadAsBytes(cancellationToken).ConfigureAwait(false);
            var content = bytes == null ? null : await httpResponse.GetResponseString(bytes, options.Encoding);

            return new(request) {
                Content             = content,
                ContentEncoding     = httpResponse.Content?.Headers.ContentEncoding ?? Array.Empty<string>(),
                ContentHeaders      = httpResponse.Content?.Headers.GetHeaderParameters(),
                ContentLength       = httpResponse.Content?.Headers.ContentLength,
                ContentType         = httpResponse.Content?.Headers.ContentType?.MediaType,
                Cookies             = cookieCollection,
                ErrorException      = httpResponse.MaybeException(options.SetErrorExceptionOnUnsuccessfulStatusCode),
                Headers             = httpResponse.Headers.GetHeaderParameters(),
                IsSuccessStatusCode = httpResponse.IsSuccessStatusCode,
                RawBytes            = bytes,
                ResponseStatus      = options.CalculateResponseStatus(httpResponse),
                ResponseUri         = GetResponseUri(httpResponse),
                RootElement         = request.RootElement,
                Server              = httpResponse.Headers.Server.ToString(),
                StatusCode          = httpResponse.StatusCode,
                StatusDescription   = httpResponse.ReasonPhrase,
                Version             = httpResponse.RequestMessage?.Version
            };
        }
    }
```


---

### 🔹 Commit #08: `991130b0`
- **完整 Hash**: `991130b00a021da3b54c7617cb87c4b17073aac4`
- **說明 (Ground Truth)**: Fix default parameter merging bugs, add MergedParameters to RestResponse (#2349)
- **變更檔案數**: 2

#### 📄 檔案: `src/RestSharp/Response/RestResponseBase.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:6, E:2, A:0) ➔ After(N:6, E:2, A:0)
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

#### 📄 檔案: `src/RestSharp/RestClient.Async.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:59, E:60, A:0) ➔ After(N:60, E:61, A:0)
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
  • + [新增節點] `request.Parameters.Union (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `RestClient.ExecuteAsync` ──[CALLS]──> `request.Parameters.Union (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RestClient.ExecuteAsync()`
- **變更前簽章 (Before)**: `RestClient.ExecuteAsync(RestRequest request, CancellationToken cancellationToken = default)` (L26~L42)
- **變更後簽章 (After)**: `RestClient.ExecuteAsync(RestRequest request, CancellationToken cancellationToken = default)` (L26~L43)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async Task<RestResponse> ExecuteAsync(RestRequest request, CancellationToken cancellationToken = default) {
        using var internalResponse = await ExecuteRequestAsync(request, cancellationToken).ConfigureAwait(false);

        var response = internalResponse.Exception == null
            ? await RestResponse.FromHttpResponse(
                    internalResponse.ResponseMessage!,
                    request,
                    Options,
                    internalResponse.CookieContainer?.GetCookies(internalResponse.Url),
                    cancellationToken
                )
                .ConfigureAwait(false)
            : GetErrorResponse(request, internalResponse.Exception, internalResponse.TimeoutToken);
        await OnAfterRequest(response, cancellationToken).ConfigureAwait(false);

        return Options.ThrowOnAnyError ? response.ThrowIfError() : response;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async Task<RestResponse> ExecuteAsync(RestRequest request, CancellationToken cancellationToken = default) {
        using var internalResponse = await ExecuteRequestAsync(request, cancellationToken).ConfigureAwait(false);

        var response = internalResponse.Exception == null
            ? await RestResponse.FromHttpResponse(
                    internalResponse.ResponseMessage!,
                    request,
                    Options,
                    internalResponse.CookieContainer?.GetCookies(internalResponse.Url),
                    cancellationToken
                )
                .ConfigureAwait(false)
            : GetErrorResponse(request, internalResponse.Exception, internalResponse.TimeoutToken);
        response.MergedParameters = new RequestParameters(request.Parameters.Union(DefaultParameters));
        await OnAfterRequest(response, cancellationToken).ConfigureAwait(false);

        return Options.ThrowOnAnyError ? response.ThrowIfError() : response;
    }
```


---

### 🔹 Commit #09: `ea557db0`
- **完整 Hash**: `ea557db018015b1b97465cf2f44bbbdada2eafd5`
- **說明 (Ground Truth)**: Fix pipe char encoding issue (#2345)
- **變更檔案數**: 4

#### 📄 檔案: `src/RestSharp/Authenticators/OAuth/OAuth1Authenticator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:46, E:41, A:0) ➔ After(N:45, E:40, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 2, +Edges: 1, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `client.BuildUriString (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `client.BuildUri (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `client.BuildUri(request).ToString (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `OAuth1Authenticator.AddOAuthData` ──[CALLS]──> `client.BuildUriString (External/BCL)`
  • - [移除呼叫邊] `OAuth1Authenticator.AddOAuthData` ──[CALLS]──> `client.BuildUri(request).ToString (External/BCL)`
  • - [移除呼叫邊] `OAuth1Authenticator.AddOAuthData` ──[CALLS]──> `client.BuildUri (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `OAuth1Authenticator.AddOAuthData()`
- **變更前簽章 (Before)**: `OAuth1Authenticator.AddOAuthData(
        IRestClient            client,
        RestRequest            request,
        OAuthWorkflow          workflow,
        OAuthType              type,
        string?                realm
    )` (L234~L307)
- **變更後簽章 (After)**: `OAuth1Authenticator.AddOAuthData(
        IRestClient            client,
        RestRequest            request,
        OAuthWorkflow          workflow,
        OAuthType              type,
        string?                realm
    )` (L234~L307)

#### ◀️ 變更前實作碼 (Before Implementation):
```
internal static void AddOAuthData(
        IRestClient            client,
        RestRequest            request,
        OAuthWorkflow          workflow,
        OAuthType              type,
        string?                realm
    ) {
        var requestUrl = client.BuildUriWithoutQueryParameters(request).AbsoluteUri;

        if (requestUrl.Contains('?'))
            throw new ApplicationException(
                "Using query parameters in the base URL is not supported for OAuth calls. Consider using AddDefaultQueryParameter instead."
            );

        var url              = client.BuildUri(request).ToString();
        var queryStringStart = url.IndexOf('?');

        if (queryStringStart != -1) url = url[..queryStringStart];

        var method     = request.Method.ToString().ToUpperInvariant();
        var parameters = new WebPairCollection();

        var query =
            request.AlwaysMultipartFormData || request.Files.Count > 0
                ? x => BaseQuery(x) && x.Name != null && x.Name.StartsWith("oauth_")
                : (Func<Parameter, bool>)BaseQuery;

        parameters.AddRange(client.DefaultParameters.Where(query).ToWebParameters());
        parameters.AddRange(request.Parameters.Where(query).ToWebParameters());

        workflow.RequestUrl = url;

        var oauth = type switch {
            OAuthType.RequestToken         => workflow.BuildRequestTokenSignature(method, parameters),
            OAuthType.AccessToken          => workflow.BuildAccessTokenSignature(method, parameters),
            OAuthType.ClientAuthentication => workflow.BuildClientAuthAccessTokenSignature(method, parameters),
            OAuthType.ProtectedResource    => workflow.BuildProtectedResourceSignature(method, parameters),
            _                              => throw new ArgumentOutOfRangeException(nameof(Type))
        };

        oauth.Parameters.Add("oauth_signature", oauth.Signature);

        var oauthParameters = workflow.ParameterHandling switch {
            OAuthParameterHandling.HttpAuthorizationHeader => CreateHeaderParameters(),
            OAuthParameterHandling.UrlOrPostParameters     => CreateUrlParameters(),
            _                                              => throw new ArgumentOutOfRangeException(nameof(ParameterHandling))
        };

        request.AddOrUpdateParameters(oauthParameters);
        return;

        // include all GET and POST parameters before generating the signature
        // according to the RFC 5849 - The OAuth 1.0 Protocol
        // http://tools.ietf.org/html/rfc5849#section-3.4.1
        // if this change causes trouble we need to introduce a flag indicating the specific OAuth implementation level,
        // or implement a separate class for each OAuth version
        static bool BaseQuery(Parameter x) => x.Type is ParameterType.GetOrPost or ParameterType.QueryString;

        IEnumerable<Parameter> CreateHeaderParameters() => [new HeaderParameter(KnownHeaders.Authorization, GetAuthorizationHeader())];

        IEnumerable<Parameter> CreateUrlParameters() => oauth.Parameters.Select(p => new GetOrPostParameter(p.Name, HttpUtility.UrlDecode(p.Value)));

        string GetAuthorizationHeader() {
            var oathParameters =
                oauth.Parameters
                    .OrderBy(x => x, WebPair.Comparer)
                    .Select(x => x.GetQueryParameter(true))
                    .ToList();

            if (!realm.IsEmpty()) oathParameters.Insert(0, $"realm=\"{OAuthTools.UrlEncodeRelaxed(realm)}\"");

            return $"OAuth {string.Join(",", oathParameters)}";
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal static void AddOAuthData(
        IRestClient            client,
        RestRequest            request,
        OAuthWorkflow          workflow,
        OAuthType              type,
        string?                realm
    ) {
        var requestUrl = client.BuildUriWithoutQueryParameters(request).AbsoluteUri;

        if (requestUrl.Contains('?'))
            throw new ApplicationException(
                "Using query parameters in the base URL is not supported for OAuth calls. Consider using AddDefaultQueryParameter instead."
            );

        var url              = client.BuildUriString(request);
        var queryStringStart = url.IndexOf('?');

        if (queryStringStart != -1) url = url[..queryStringStart];

        var method     = request.Method.ToString().ToUpperInvariant();
        var parameters = new WebPairCollection();

        var query =
            request.AlwaysMultipartFormData || request.Files.Count > 0
                ? x => BaseQuery(x) && x.Name != null && x.Name.StartsWith("oauth_")
                : (Func<Parameter, bool>)BaseQuery;

        parameters.AddRange(client.DefaultParameters.Where(query).ToWebParameters());
        parameters.AddRange(request.Parameters.Where(query).ToWebParameters());

        workflow.RequestUrl = url;

        var oauth = type switch {
            OAuthType.RequestToken         => workflow.BuildRequestTokenSignature(method, parameters),
            OAuthType.AccessToken          => workflow.BuildAccessTokenSignature(method, parameters),
            OAuthType.ClientAuthentication => workflow.BuildClientAuthAccessTokenSignature(method, parameters),
            OAuthType.ProtectedResource    => workflow.BuildProtectedResourceSignature(method, parameters),
            _                              => throw new ArgumentOutOfRangeException(nameof(Type))
        };

        oauth.Parameters.Add("oauth_signature", oauth.Signature);

        var oauthParameters = workflow.ParameterHandling switch {
            OAuthParameterHandling.HttpAuthorizationHeader => CreateHeaderParameters(),
            OAuthParameterHandling.UrlOrPostParameters     => CreateUrlParameters(),
            _                                              => throw new ArgumentOutOfRangeException(nameof(ParameterHandling))
        };

        request.AddOrUpdateParameters(oauthParameters);
        return;

        // include all GET and POST parameters before generating the signature
        // according to the RFC 5849 - The OAuth 1.0 Protocol
        // http://tools.ietf.org/html/rfc5849#section-3.4.1
        // if this change causes trouble we need to introduce a flag indicating the specific OAuth implementation level,
        // or implement a separate class for each OAuth version
        static bool BaseQuery(Parameter x) => x.Type is ParameterType.GetOrPost or ParameterType.QueryString;

        IEnumerable<Parameter> CreateHeaderParameters() => [new HeaderParameter(KnownHeaders.Authorization, GetAuthorizationHeader())];

        IEnumerable<Parameter> CreateUrlParameters() => oauth.Parameters.Select(p => new GetOrPostParameter(p.Name, HttpUtility.UrlDecode(p.Value)));

        string GetAuthorizationHeader() {
            var oathParameters =
                oauth.Parameters
                    .OrderBy(x => x, WebPair.Comparer)
                    .Select(x => x.GetQueryParameter(true))
                    .ToList();

            if (!realm.IsEmpty()) oathParameters.Insert(0, $"realm=\"{OAuthTools.UrlEncodeRelaxed(realm)}\"");

            return $"OAuth {string.Join(",", oathParameters)}";
        }
    }
```


#### 📄 檔案: `src/RestSharp/BuildUriExtensions.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:21, E:20, A:0) ➔ After(N:22, E:19, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 1, +Edges: 4, -Edges: 5, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `mergedUri.AbsoluteUri.Contains (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `BuildUriExtensions.BuildUriString` (FUNCTION_DEF)
  • - [移除節點] `mergedUri.AddQueryString (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `BuildUriExtensions.BuildUri` ──[CALLS]──> `BuildUriExtensions.BuildUriString`
  • + [新增呼叫邊] `BuildUriExtensions.BuildUriString` ──[CALLS]──> `BuildUriExtensions.BuildUriWithoutQueryParameters`
  • + [新增呼叫邊] `BuildUriExtensions.BuildUriString` ──[CALLS]──> `BuildUriExtensions.GetRequestQuery`
  • + [新增呼叫邊] `BuildUriExtensions.BuildUriString` ──[CALLS]──> `mergedUri.AbsoluteUri.Contains (External/BCL)`
  • - [移除呼叫邊] `BuildUriExtensions.BuildUri` ──[CALLS]──> `BuildUriExtensions.DoBuildUriValidations`
  • - [移除呼叫邊] `BuildUriExtensions.BuildUri` ──[CALLS]──> `client.Options.BaseUrl.GetUrlSegmentParamsValues (External/BCL)`
  • - [移除呼叫邊] `BuildUriExtensions.BuildUri` ──[CALLS]──> `uri.MergeBaseUrlAndResource (External/BCL)`
  • - [移除呼叫邊] `BuildUriExtensions.BuildUri` ──[CALLS]──> `BuildUriExtensions.GetRequestQuery`
  • - [移除呼叫邊] `BuildUriExtensions.BuildUri` ──[CALLS]──> `mergedUri.AddQueryString (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `BuildUriExtensions.extension()`
- **變更前簽章 (Before)**: `BuildUriExtensions.extension(IRestClient client)` (L20~L84)
- **變更後簽章 (After)**: `BuildUriExtensions.extension(IRestClient client)` (L20~L89)

#### ◀️ 變更前實作碼 (Before Implementation):
```
extension(IRestClient client) {
        /// <summary>
        /// Builds the URI for the request
        /// </summary>
        /// <param name="request">Request instance</param>
        /// <returns></returns>
        public Uri BuildUri(RestRequest request) {
            DoBuildUriValidations(client, request);

            var (uri, resource) = client.Options.BaseUrl.GetUrlSegmentParamsValues(
                request.Resource,
                client.Options.Encode,
                request.Parameters,
                client.DefaultParameters
            );
            var mergedUri = uri.MergeBaseUrlAndResource(resource);
            var query     = client.GetRequestQuery(request);
            return mergedUri.AddQueryString(query);
        }

        /// <summary>
        /// Builds the URI for the request without query parameters.
        /// </summary>
        /// <param name="request">Request instance</param>
        /// <returns></returns>
        public Uri BuildUriWithoutQueryParameters(RestRequest request) {
            DoBuildUriValidations(client, request);

            var (uri, resource) = client.Options.BaseUrl.GetUrlSegmentParamsValues(
                request.Resource,
                client.Options.Encode,
                request.Parameters,
                client.DefaultParameters
            );
            return uri.MergeBaseUrlAndResource(resource);
        }

        /// <summary>
        /// Gets the query string for the request.
        /// </summary>
        /// <param name="request">Request instance</param>
        /// <returns></returns>
        [PublicAPI]
        public string? GetRequestQuery(RestRequest request) {
            var parametersCollections = new ParametersCollection[] { request.Parameters, client.DefaultParameters };

            var parameters = parametersCollections.SelectMany(x => x.GetQueryParameters(request.Method)).ToList();

            return parameters.Count == 0 ? null : string.Join("&", parameters.Select(EncodeParameter).ToArray());

            string GetString(string name, string? value, Func<string, string>? encode) {
                var val = encode != null && value != null ? encode(value) : value;
                return val == null ? name : $"{name}={val}";
            }

            string EncodeParameter(Parameter parameter)
                => !parameter.Encode
                    ? GetString(parameter.Name!, parameter.Value?.ToString(), null)
                    : GetString(
                        client.Options.EncodeQuery(parameter.Name!, client.Options.Encoding),
                        parameter.Value?.ToString(),
                        x => client.Options.EncodeQuery(x, client.Options.Encoding)
                    );
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
extension(IRestClient client) {
        /// <summary>
        /// Builds the URI for the request
        /// </summary>
        /// <param name="request">Request instance</param>
        /// <returns></returns>
        public Uri BuildUri(RestRequest request) => new(client.BuildUriString(request));

        /// <summary>
        /// Builds the URI string for the request. This method returns a string instead of a Uri object
        /// to preserve unencoded characters when encode=false is specified for query parameters.
        /// </summary>
        /// <param name="request">Request instance</param>
        /// <returns></returns>
        [PublicAPI]
        public string BuildUriString(RestRequest request) {
            var mergedUri = client.BuildUriWithoutQueryParameters(request);
            var query     = client.GetRequestQuery(request);

            if (query == null) return mergedUri.AbsoluteUri;

            var separator = mergedUri.AbsoluteUri.Contains('?') ? "&" : "?";
            return $"{mergedUri.AbsoluteUri}{separator}{query}";
        }

        /// <summary>
        /// Builds the URI for the request without query parameters.
        /// </summary>
        /// <param name="request">Request instance</param>
        /// <returns></returns>
        public Uri BuildUriWithoutQueryParameters(RestRequest request) {
            DoBuildUriValidations(client, request);

            var (uri, resource) = client.Options.BaseUrl.GetUrlSegmentParamsValues(
                request.Resource,
                client.Options.Encode,
                request.Parameters,
                client.DefaultParameters
            );
            return uri.MergeBaseUrlAndResource(resource);
        }

        /// <summary>
        /// Gets the query string for the request.
        /// </summary>
        /// <param name="request">Request instance</param>
        /// <returns></returns>
        [PublicAPI]
        public string? GetRequestQuery(RestRequest request) {
            var parametersCollections = new ParametersCollection[] { request.Parameters, client.DefaultParameters };

            var parameters = parametersCollections.SelectMany(x => x.GetQueryParameters(request.Method)).ToList();

            return parameters.Count == 0 ? null : string.Join("&", parameters.Select(EncodeParameter).ToArray());

            string GetString(string name, string? value, Func<string, string>? encode) {
                var val = encode != null && value != null ? encode(value) : value;
                return val == null ? name : $"{name}={val}";
            }

            string EncodeParameter(Parameter parameter)
                => !parameter.Encode
                    ? GetString(parameter.Name!, parameter.Value?.ToString(), null)
                    : GetString(
                        client.Options.EncodeQuery(parameter.Name!, client.Options.Encoding),
                        parameter.Value?.ToString(),
                        x => client.Options.EncodeQuery(x, client.Options.Encoding)
                    );
        }
    }
```

### 🔹 函式: `BuildUriExtensions.BuildUri()`
- **變更前簽章 (Before)**: `BuildUriExtensions.BuildUri(RestRequest request)` (L26~L38)
- **變更後簽章 (After)**: `BuildUriExtensions.BuildUri(RestRequest request)` (L26~L26)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public Uri BuildUri(RestRequest request) {
            DoBuildUriValidations(client, request);

            var (uri, resource) = client.Options.BaseUrl.GetUrlSegmentParamsValues(
                request.Resource,
                client.Options.Encode,
                request.Parameters,
                client.DefaultParameters
            );
            var mergedUri = uri.MergeBaseUrlAndResource(resource);
            var query     = client.GetRequestQuery(request);
            return mergedUri.AddQueryString(query);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public Uri BuildUri(RestRequest request) => new(client.BuildUriString(request));
```


#### 📄 檔案: `src/RestSharp/Request/UriExtensions.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:17, E:15, A:0) ➔ After(N:16, E:14, A:0)
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
  • - [移除節點] `absoluteUri.Contains (External/BCL)` (FUNCTION_DEF)
  • - [移除呼叫邊] `UriExtensions.AddQueryString` ──[CALLS]──> `absoluteUri.Contains (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `UriExtensions.AddQueryString()`
- **變更前簽章 (Before)**: `UriExtensions.AddQueryString(this Uri uri, string? query)` (L41~L48)
- **變更後簽章 (After)**: `UriExtensions.AddQueryString(this Uri uri, string? query)` (L41~L48)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static Uri AddQueryString(this Uri uri, string? query) {
        if (query == null) return uri;

        var absoluteUri = uri.AbsoluteUri;
        var separator   = absoluteUri.Contains('?') ? "&" : "?";

        return new($"{absoluteUri}{separator}{query}");
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static Uri AddQueryString(this Uri uri, string? query) {
        if (query == null) return uri;

        var builder = new UriBuilder(uri);
        builder.Query = builder.Query.Length > 1 ? $"{builder.Query[1..]}&{query}" : query;

        return builder.Uri;
    }
```


#### 📄 檔案: `src/RestSharp/RestClient.Async.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:59, E:60, A:0) ➔ After(N:59, E:60, A:0)
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
  • + [新增節點] `this.BuildUriString (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `this.BuildUri (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `RestClient.ExecuteRequestAsync` ──[CALLS]──> `this.BuildUriString (External/BCL)`
  • - [移除呼叫邊] `RestClient.ExecuteRequestAsync` ──[CALLS]──> `this.BuildUri (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RestClient.ExecuteRequestAsync()`
- **變更前簽章 (Before)**: `RestClient.ExecuteRequestAsync(RestRequest request, CancellationToken cancellationToken)` (L91~L164)
- **變更後簽章 (After)**: `RestClient.ExecuteRequestAsync(RestRequest request, CancellationToken cancellationToken)` (L91~L165)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async Task<HttpResponse> ExecuteRequestAsync(RestRequest request, CancellationToken cancellationToken) {
        Ensure.NotNull(request, nameof(request));

        // Make sure we are not disposed of when someone tries to call us!
#if NET
        ObjectDisposedException.ThrowIf(_disposed, this);
#else
        if (_disposed) {
            throw new ObjectDisposedException(nameof(RestClient));
        }
#endif
        CombineInterceptors(request);
        await OnBeforeRequest(request, cancellationToken).ConfigureAwait(false);
        request.ValidateParameters();
        var authenticator = request.Authenticator ?? Options.Authenticator;

        if (authenticator != null) {
            await authenticator.Authenticate(this, request).ConfigureAwait(false);
        }

        using var requestContent = new RequestContent(this, request);

        var httpMethod = AsHttpMethod(request.Method);
        var url        = this.BuildUri(request);

        using var message = new HttpRequestMessage(httpMethod, url);
        message.Content              = requestContent.BuildContent();
        message.Headers.Host         = Options.BaseHost;
        message.Headers.CacheControl = request.CachePolicy ?? Options.CachePolicy;
        message.Version              = request.Version;

        using var timeoutCts = new CancellationTokenSource(request.Timeout ?? Options.Timeout ?? _defaultTimeout);
        using var cts        = CancellationTokenSource.CreateLinkedTokenSource(timeoutCts.Token, cancellationToken);

        var ct = cts.Token;

        HttpResponseMessage? responseMessage;
        // Make sure we have a cookie container if not provided in the request
        var cookieContainer = request.CookieContainer ??= new();

        var headers = new RequestHeaders()
            .AddHeaders(request.Parameters)
            .AddHeaders(DefaultParameters)
            .AddAcceptHeader(AcceptedContentTypes)
            .AddCookieHeaders(url, cookieContainer)
            .AddCookieHeaders(url, Options.CookieContainer);

        message.AddHeaders(headers);
#pragma warning disable CS0618 // Type or member is obsolete
        if (request.OnBeforeRequest != null) await request.OnBeforeRequest(message).ConfigureAwait(false);
#pragma warning restore CS0618 // Type or member is obsolete
        await OnBeforeHttpRequest(request, message, cancellationToken).ConfigureAwait(false);

        try {
            responseMessage = await HttpClient.SendAsync(message, request.CompletionOption, ct).ConfigureAwait(false);

            // Parse all the cookies from the response and update the cookie jar with cookies
            if (responseMessage.Headers.TryGetValues(KnownHeaders.SetCookie, out var cookiesHeader)) {
                // ReSharper disable once PossibleMultipleEnumeration
                cookieContainer.AddCookies(url, cookiesHeader);
                // ReSharper disable once PossibleMultipleEnumeration
                Options.CookieContainer?.AddCookies(url, cookiesHeader);
            }
        }
        catch (Exception ex) {
            return new(null, url, null, ex, timeoutCts.Token);
        }

#pragma warning disable CS0618 // Type or member is obsolete
        if (request.OnAfterRequest != null) await request.OnAfterRequest(responseMessage).ConfigureAwait(false);
#pragma warning restore CS0618 // Type or member is obsolete
        await OnAfterHttpRequest(request, responseMessage, cancellationToken).ConfigureAwait(false);
        return new(responseMessage, url, cookieContainer, null, timeoutCts.Token);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async Task<HttpResponse> ExecuteRequestAsync(RestRequest request, CancellationToken cancellationToken) {
        Ensure.NotNull(request, nameof(request));

        // Make sure we are not disposed of when someone tries to call us!
#if NET
        ObjectDisposedException.ThrowIf(_disposed, this);
#else
        if (_disposed) {
            throw new ObjectDisposedException(nameof(RestClient));
        }
#endif
        CombineInterceptors(request);
        await OnBeforeRequest(request, cancellationToken).ConfigureAwait(false);
        request.ValidateParameters();
        var authenticator = request.Authenticator ?? Options.Authenticator;

        if (authenticator != null) {
            await authenticator.Authenticate(this, request).ConfigureAwait(false);
        }

        using var requestContent = new RequestContent(this, request);

        var httpMethod = AsHttpMethod(request.Method);
        var urlString  = this.BuildUriString(request);
        var url        = new Uri(urlString);

        using var message = new HttpRequestMessage(httpMethod, urlString);
        message.Content              = requestContent.BuildContent();
        message.Headers.Host         = Options.BaseHost;
        message.Headers.CacheControl = request.CachePolicy ?? Options.CachePolicy;
        message.Version              = request.Version;

        using var timeoutCts = new CancellationTokenSource(request.Timeout ?? Options.Timeout ?? _defaultTimeout);
        using var cts        = CancellationTokenSource.CreateLinkedTokenSource(timeoutCts.Token, cancellationToken);

        var ct = cts.Token;

        HttpResponseMessage? responseMessage;
        // Make sure we have a cookie container if not provided in the request
        var cookieContainer = request.CookieContainer ??= new();

        var headers = new RequestHeaders()
            .AddHeaders(request.Parameters)
            .AddHeaders(DefaultParameters)
            .AddAcceptHeader(AcceptedContentTypes)
            .AddCookieHeaders(url, cookieContainer)
            .AddCookieHeaders(url, Options.CookieContainer);

        message.AddHeaders(headers);
#pragma warning disable CS0618 // Type or member is obsolete
        if (request.OnBeforeRequest != null) await request.OnBeforeRequest(message).ConfigureAwait(false);
#pragma warning restore CS0618 // Type or member is obsolete
        await OnBeforeHttpRequest(request, message, cancellationToken).ConfigureAwait(false);

        try {
            responseMessage = await HttpClient.SendAsync(message, request.CompletionOption, ct).ConfigureAwait(false);

            // Parse all the cookies from the response and update the cookie jar with cookies
            if (responseMessage.Headers.TryGetValues(KnownHeaders.SetCookie, out var cookiesHeader)) {
                // ReSharper disable once PossibleMultipleEnumeration
                cookieContainer.AddCookies(url, cookiesHeader);
                // ReSharper disable once PossibleMultipleEnumeration
                Options.CookieContainer?.AddCookies(url, cookiesHeader);
            }
        }
        catch (Exception ex) {
            return new(null, url, null, ex, timeoutCts.Token);
        }

#pragma warning disable CS0618 // Type or member is obsolete
        if (request.OnAfterRequest != null) await request.OnAfterRequest(responseMessage).ConfigureAwait(false);
#pragma warning restore CS0618 // Type or member is obsolete
        await OnAfterHttpRequest(request, responseMessage, cancellationToken).ConfigureAwait(false);
        return new(responseMessage, url, cookieContainer, null, timeoutCts.Token);
    }
```


---

### 🔹 Commit #10: `13b0425e`
- **完整 Hash**: `13b0425ece77e997abc6c71745b92c46fbd237f4`
- **說明 (Ground Truth)**: Fix OAuth1 double-encoding of RFC 3986 special characters in URL paths (#2341)
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp/Authenticators/OAuth/OAuthTools.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:60, E:51, A:0) ➔ After(N:61, E:52, A:0)
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
  • + [新增節點] `Uri.UnescapeDataString (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `OAuthTools.ConstructRequestUrl` ──[CALLS]──> `Uri.UnescapeDataString (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `OAuthTools.ConstructRequestUrl()`
- **變更前簽章 (Before)**: `OAuthTools.ConstructRequestUrl(Uri url)` (L150~L158)
- **變更後簽章 (After)**: `OAuthTools.ConstructRequestUrl(Uri url)` (L150~L170)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static string ConstructRequestUrl(Uri url) {
        Ensure.NotNull(url, nameof(url));

        var basic  = url is { Scheme: "http", Port : 80 };
        var secure = url is { Scheme: "https", Port: 443 };
        var port   = basic || secure ? "" : $":{url.Port}";

        return $"{url.Scheme}://{url.Host}{port}{url.AbsolutePath}";
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static string ConstructRequestUrl(Uri url) {
        Ensure.NotNull(url, nameof(url));

        var basic  = url is { Scheme: "http", Port : 80 };
        var secure = url is { Scheme: "https", Port: 443 };
        var port   = basic || secure ? "" : $":{url.Port}";

        // Decode the path to avoid double-encoding when the path contains already-encoded characters.
        // For example, if a URL segment was added with AddUrlSegment("id", "value!"), it gets encoded
        // to "value%21" in the URL. When we extract url.AbsolutePath, it contains "%21" (encoded).
        // If we then call UrlEncodeRelaxed on it, Uri.EscapeDataString would encode the "%" to "%25",
        // resulting in "%2521" (double-encoded). By decoding first, we ensure proper single encoding.
        // 
        // Security note: This is safe because:
        // - The url parameter is a validated Uri object constructed by RestSharp's BuildUri()
        // - The decoded path is immediately re-encoded by UrlEncodeRelaxed before use
        // - There is no direct user input involved in this internal OAuth signature calculation
        var decodedPath = Uri.UnescapeDataString(url.AbsolutePath);

        return $"{url.Scheme}://{url.Host}{port}{decodedPath}";
    }
```


---

### 🔹 Commit #11: `bc2ae9c3`
- **完整 Hash**: `bc2ae9c3a38911ad1f6933c95cda542c74ea7a68`
- **說明 (Ground Truth)**: Fix XmlDeserializer when XML uses same tag in nested elements (#2339)
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp.Serializers.Xml/XmlDeserializer.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:107, E:120, A:0) ➔ After(N:123, E:138, A:0)
- **差分統計**: +Nodes: 29, -Nodes: 13, +Edges: 33, -Edges: 15, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `source.Elements()
                    .Where (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `name.Contains (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `itemName?.ToLower (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `source.Elements()
                    .Where(e => e.Name.LocalName.RemoveUnderscoresAndDashes() == lowerName)
                    .ToList (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `doc.Root.DescendantsAndSelf(namespacedRoot)
                        .OrderBy (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `doc.Root.DescendantsAndSelf(namespacedRoot)
                        .OrderBy(e => e.Ancestors().Count())
                        .FirstOrDefault (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `source.Descendants (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `source.Elements(typeName.AsNamespaced(Namespace)).ToList (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `itemName?.ToCamelCase (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `doc.Root.Element (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `source.Descendants(camelName).ToList (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `source.Descendants(typeName.AsNamespaced(Namespace)).ToList (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `source.Elements(camelName).ToList (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `itemName?.ToLower(Culture).AsNamespaced (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `e.Ancestors().Count (External/BCL)` (FUNCTION_DEF)
  • _... 以及其餘 75 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `XmlDeserializer.Map()`
- **變更前簽章 (Before)**: `XmlDeserializer.Map(object x, XElement? root)` (L83~L283)
- **變更後簽章 (After)**: `XmlDeserializer.Map(object x, XElement? root)` (L96~L307)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected virtual object Map(object x, XElement? root) {
        var objType = x.GetType();
        var props   = objType.GetProperties();

        var deserializeFromContentAttributeAlreadyUsed = false;

        foreach (var prop in props) {
            var type         = prop.PropertyType.GetTypeInfo();
            var typeIsPublic = type.IsPublic || type.IsNestedPublic;

            if (!typeIsPublic || !prop.CanWrite)
                continue;

            var    deserializeFromContent   = false;
            var    isNameDefinedInAttribute = false;
            XName? name                     = null;
            var    attributes               = prop.GetCustomAttributes(typeof(DeserializeAsAttribute), false);

            if (attributes.Any()) {
                var attribute = (DeserializeAsAttribute)attributes.First();

                name                     = attribute.Name.AsNamespaced(Namespace);
                isNameDefinedInAttribute = !string.IsNullOrEmpty(name?.LocalName);

                deserializeFromContent = attribute.Content;

                if (deserializeFromContentAttributeAlreadyUsed && deserializeFromContent)
                    throw new ArgumentException("Class cannot have two properties marked with SerializeAs(Content = true) attribute.");

                deserializeFromContentAttributeAlreadyUsed |= deserializeFromContent;
            }

            if (name == null) name = prop.Name.AsNamespaced(Namespace);

            var value = GetValueFromXml(root, name, prop, isNameDefinedInAttribute);

            if (value == null) {
                // special case for text content node
                if (deserializeFromContent) {
                    var textNode = root!.Nodes().FirstOrDefault(n => n is XText);

                    if (textNode != null) {
                        value = ((XText)textNode).Value;
                        prop.SetValue(x, value, null);
                    }

                    continue;
                }

                // special case for inline list items
                if (type.IsGenericType) {
                    var genericType = type.GetGenericArguments()[0];
                    var first       = GetElementByName(root, genericType.Name);
                    var list        = (IList)Activator.CreateInstance(type.AsType())!;

                    if (first != null && root != null) {
                        var elements = root.Elements(first.Name);

                        PopulateListFromElements(genericType, elements, list);
                    }

                    prop.SetValue(x, list, null);
                }

                continue;
            }

            if (type.IsGenericType && type.GetGenericTypeDefinition() == typeof(Nullable<>)) {
                // if the value is empty, set the property to null...
                if (string.IsNullOrEmpty(value.ToString())) {
                    prop.SetValue(x, null, null);
                    continue;
                }

                type = type.GetGenericArguments()[0].GetTypeInfo();
            }

            var asType = type.AsType();

            if (asType == typeof(bool)) {
                var toConvert = value.ToString()!.ToLower(Culture);

                prop.SetValue(x, XmlConvert.ToBoolean(toConvert), null);
            }
            else if (type.IsPrimitive) {
                try {
                    prop.SetValue(x, value.ChangeType(asType), null);
                }
                catch (FormatException ex) {
                    throw new FormatException(
                        $"Couldn't parse the value of '{value}' into the '{prop.Name}'" +
                        $" property, because it isn't a type of '{prop.PropertyType}'.",
                        ex.InnerException
                    );
                }
            }
            else if (type.IsEnum) {
                var converted = type.AsType().FindEnumValue(value.ToString()!, Culture);

                prop.SetValue(x, converted, null);
            }
            else if (asType == typeof(Uri)) {
                var uri = new Uri(value.ToString()!, UriKind.RelativeOrAbsolute);

                prop.SetValue(x, uri, null);
            }
            else if (asType == typeof(string)) {
                prop.SetValue(x, value, null);
            }
            else if (asType == typeof(DateTime)) {
                value = DateFormat.IsNotEmpty()
                    ? DateTime.ParseExact(value.ToString()!, DateFormat!, Culture)
                    : DateTime.Parse(value.ToString()!, Culture);

                prop.SetValue(x, value, null);
            }
            else if (asType == typeof(DateTimeOffset)) {
                var toConvert = value.ToString();

                if (string.IsNullOrEmpty(toConvert)) continue;

                DateTimeOffset deserialisedValue;

                try {
                    deserialisedValue = XmlConvert.ToDateTimeOffset(toConvert);
                    prop.SetValue(x, deserialisedValue, null);
                }
                catch (Exception) {
                    if (TryGetFromString(toConvert, out var result, asType)) {
                        prop.SetValue(x, result, null);
                    }
                    else {
                        //fallback to parse
                        deserialisedValue = DateTimeOffset.Parse(toConvert);
                        prop.SetValue(x, deserialisedValue, null);
                    }
                }
            }
            else if (asType == typeof(decimal)) {
                value = decimal.Parse(value.ToString()!, Culture);
                prop.SetValue(x, value, null);
            }
            else if (asType == typeof(Guid)) {
                var raw = value.ToString();

                value = string.IsNullOrEmpty(raw) ? Guid.Empty : new(value.ToString()!);

                prop.SetValue(x, value, null);
            }
            else if (asType == typeof(TimeSpan)) {
                var timeSpan = XmlConvert.ToTimeSpan(value.ToString()!);

                prop.SetValue(x, timeSpan, null);
            }
            else if (type.IsGenericType) {
                var list      = (IList)Activator.CreateInstance(asType)!;
                var container = GetElementByName(root, name);

                if (container?.HasElements == true) {
                    var first = container.Elements().FirstOrDefault();

                    if (first != null) {
                        var t        = type.GetGenericArguments()[0];
                        var elements = container.Elements(first.Name);

                        PopulateListFromElements(t, elements, list);
                    }
                }

                prop.SetValue(x, list, null);
            }
            else if (asType.IsSubclassOfRawGeneric(typeof(List<>))) {
                // handles classes that derive from List<T>
                // e.g. a collection that also has attributes
                var list = HandleListDerivative(root!, prop.Name, asType);

                prop.SetValue(x, list, null);
            }
            else {
                //fallback to type converters if possible

                if (TryGetFromString(value.ToString()!, out var result, asType)) {
                    prop.SetValue(x, result, null);
                }
                else {
                    // nested property classes
                    if (root == null) continue;

                    var element = GetElementByName(root, name);

                    if (element == null) continue;

                    var item = CreateAndMap(asType, element);

                    prop.SetValue(x, item, null);
                }
            }
        }

        return x;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected virtual object Map(object x, XElement? root) {
        var objType = x.GetType();
        var props   = objType.GetProperties();

        var deserializeFromContentAttributeAlreadyUsed = false;

        foreach (var prop in props) {
            var type         = prop.PropertyType.GetTypeInfo();
            var typeIsPublic = type.IsPublic || type.IsNestedPublic;

            if (!typeIsPublic || !prop.CanWrite)
                continue;

            var    deserializeFromContent   = false;
            var    isNameDefinedInAttribute = false;
            XName? name                     = null;
            var    attributes               = prop.GetCustomAttributes(typeof(DeserializeAsAttribute), false);

            if (attributes.Any()) {
                var attribute = (DeserializeAsAttribute)attributes.First();

                name                     = attribute.Name.AsNamespaced(Namespace);
                isNameDefinedInAttribute = !string.IsNullOrEmpty(name?.LocalName);

                deserializeFromContent = attribute.Content;

                if (deserializeFromContentAttributeAlreadyUsed && deserializeFromContent)
                    throw new ArgumentException("Class cannot have two properties marked with SerializeAs(Content = true) attribute.");

                deserializeFromContentAttributeAlreadyUsed |= deserializeFromContent;
            }

            if (name == null) name = prop.Name.AsNamespaced(Namespace);

            var value = GetValueFromXml(root, name, prop, isNameDefinedInAttribute);

            if (value == null) {
                // special case for text content node
                if (deserializeFromContent) {
                    var textNode = root!.Nodes().FirstOrDefault(n => n is XText);

                    if (textNode != null) {
                        value = ((XText)textNode).Value;
                        prop.SetValue(x, value, null);
                    }

                    continue;
                }

                // special case for inline list items
                if (type.IsGenericType) {
                    var genericType = type.GetGenericArguments()[0];
                    var first       = GetElementByName(root, genericType.Name);
                    var list        = (IList)Activator.CreateInstance(type.AsType())!;

                    if (first != null && root != null) {
                        var elements = root.Elements(first.Name);

                        PopulateListFromElements(genericType, elements, list);
                    }

                    prop.SetValue(x, list, null);
                }

                continue;
            }

            if (type.IsGenericType && type.GetGenericTypeDefinition() == typeof(Nullable<>)) {
                // if the value is empty, set the property to null...
                if (string.IsNullOrEmpty(value.ToString())) {
                    prop.SetValue(x, null, null);
                    continue;
                }

                type = type.GetGenericArguments()[0].GetTypeInfo();
            }

            var asType = type.AsType();

            if (asType == typeof(bool)) {
                var toConvert = value.ToString()!.ToLower(Culture);

                prop.SetValue(x, XmlConvert.ToBoolean(toConvert), null);
            }
            else if (type.IsPrimitive) {
                try {
                    prop.SetValue(x, value.ChangeType(asType), null);
                }
                catch (FormatException ex) {
                    throw new FormatException(
                        $"Couldn't parse the value of '{value}' into the '{prop.Name}'" +
                        $" property, because it isn't a type of '{prop.PropertyType}'.",
                        ex.InnerException
                    );
                }
            }
            else if (type.IsEnum) {
                var converted = type.AsType().FindEnumValue(value.ToString(), Culture);

                prop.SetValue(x, converted, null);
            }
            else if (asType == typeof(Uri)) {
                var uri = new Uri(value.ToString(), UriKind.RelativeOrAbsolute);

                prop.SetValue(x, uri, null);
            }
            else if (asType == typeof(string)) {
                prop.SetValue(x, value, null);
            }
            else if (asType == typeof(DateTime)) {
                value = DateFormat.IsNotEmpty()
                    ? DateTime.ParseExact(value.ToString(), DateFormat!, Culture)
                    : DateTime.Parse(value.ToString(), Culture);

                prop.SetValue(x, value, null);
            }
            else if (asType == typeof(DateTimeOffset)) {
                var toConvert = value.ToString();

                if (string.IsNullOrEmpty(toConvert)) continue;

                DateTimeOffset deserialisedValue;

                try {
                    deserialisedValue = XmlConvert.ToDateTimeOffset(toConvert);
                    prop.SetValue(x, deserialisedValue, null);
                }
                catch (Exception) {
                    if (TryGetFromString(toConvert, out var result, asType)) {
                        prop.SetValue(x, result, null);
                    }
                    else {
                        //fallback to parse
                        deserialisedValue = DateTimeOffset.Parse(toConvert);
                        prop.SetValue(x, deserialisedValue, null);
                    }
                }
            }
            else if (asType == typeof(decimal)) {
                value = decimal.Parse(value.ToString(), Culture);
                prop.SetValue(x, value, null);
            }
            else if (asType == typeof(Guid)) {
                var raw = value.ToString();

                value = string.IsNullOrEmpty(raw) ? Guid.Empty : new(value.ToString());

                prop.SetValue(x, value, null);
            }
            else if (asType == typeof(TimeSpan)) {
                var timeSpan = XmlConvert.ToTimeSpan(value.ToString());

                prop.SetValue(x, timeSpan, null);
            }
            else if (type.IsGenericType) {
                var list      = (IList)Activator.CreateInstance(asType)!;
                XElement? container = null;
                
                // First check if root itself is the container (matches property name)
                if (root != null && name?.LocalName != null) {
                    var rootName = root.Name.LocalName;
                    if (rootName.Equals(name.LocalName, StringComparison.OrdinalIgnoreCase)) {
                        container = root;
                    }
                }
                
                // If root is not the container, try to find it as a child element
                container ??= GetElementByName(root, name);

                if (container?.HasElements == true) {
                    var first = container.Elements().FirstOrDefault();

                    if (first != null) {
                        var t        = type.GetGenericArguments()[0];
                        var elements = container.Elements(first.Name);

                        PopulateListFromElements(t, elements, list);
                    }
                }

                prop.SetValue(x, list, null);
            }
            else if (asType.IsSubclassOfRawGeneric(typeof(List<>))) {
                // handles classes that derive from List<T>
                // e.g. a collection that also has attributes
                var list = HandleListDerivative(root!, prop.Name, asType);

                prop.SetValue(x, list, null);
            }
            else {
                //fallback to type converters if possible

                if (TryGetFromString(value.ToString(), out var result, asType)) {
                    prop.SetValue(x, result, null);
                }
                else {
                    // nested property classes
                    if (root == null) continue;

                    var element = GetElementByName(root, name);

                    if (element == null) continue;

                    var item = CreateAndMap(asType, element);

                    prop.SetValue(x, item, null);
                }
            }
        }

        return x;
    }
```

### 🔹 函式: `XmlDeserializer.RemoveNamespace()`
- **變更前簽章 (Before)**: `XmlDeserializer.RemoveNamespace(XDocument xdoc)` (L61~L81)
- **變更後簽章 (After)**: `XmlDeserializer.RemoveNamespace(XDocument xdoc)` (L69~L90)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static void RemoveNamespace(XDocument xdoc) {
        if (xdoc.Root == null) return;

        foreach (var e in xdoc.Root.DescendantsAndSelf()) {
            if (e.Name.Namespace != XNamespace.None)
                e.Name = XNamespace.None.GetName(e.Name.LocalName);

            if (!e.Attributes().Any(a => a.IsNamespaceDeclaration || a.Name.Namespace != XNamespace.None)) continue;

            e.ReplaceAttributes(
                e.Attributes()
                    .Select(
                        a => a.IsNamespaceDeclaration
                            ? null
                            : a.Name.Namespace != XNamespace.None
                                ? new(XNamespace.None.GetName(a.Name.LocalName), a.Value)
                                : a
                    )
            );
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static void RemoveNamespace(XDocument xdoc) {
        if (xdoc.Root == null) return;

        foreach (var e in xdoc.Root.DescendantsAndSelf()) {
            if (e.Name.Namespace != XNamespace.None)
                e.Name = XNamespace.None.GetName(e.Name.LocalName);

            if (!e.Attributes().Any(a => a.IsNamespaceDeclaration || a.Name.Namespace != XNamespace.None)) continue;

            e.ReplaceAttributes(
                e.Attributes()
                    .Select(
                        a => a.IsNamespaceDeclaration
                            ? null
                            : a.Name.Namespace != XNamespace.None
                                ? new(XNamespace.None.GetName(a.Name.LocalName), a.Value)
                                : a
                    )
                    .Where(a => a != null)
            );
        }
    }
```

### 🔹 函式: `XmlDeserializer.HandleListDerivative()`
- **變更前簽章 (Before)**: `XmlDeserializer.HandleListDerivative(XElement root, string propName, Type type)` (L302~L350)
- **變更後簽章 (After)**: `XmlDeserializer.HandleListDerivative(XElement root, string propName, Type type)` (L326~L377)

#### ◀️ 變更前實作碼 (Before Implementation):
```
object HandleListDerivative(XElement root, string propName, Type type) {
        var t = type.IsGenericType
            ? type.GetGenericArguments()[0]
            : type.BaseType!.GetGenericArguments()[0];

        var list = (IList)Activator.CreateInstance(type)!;

        IList<XElement> elements = root.Descendants(t.Name.AsNamespaced(Namespace)).ToList();

        var name      = t.Name;
        var attribute = t.GetAttribute<DeserializeAsAttribute>();

        if (attribute != null)
            name = attribute.Name;

        if (!elements.Any()) {
            var lowerName = name?.ToLower(Culture).AsNamespaced(Namespace);

            elements = root.Descendants(lowerName).ToList();
        }

        if (!elements.Any()) {
            var camelName = name?.ToCamelCase(Culture).AsNamespaced(Namespace);

            elements = root.Descendants(camelName).ToList();
        }

        if (!elements.Any())
            elements = root.Descendants()
                .Where(e => e.Name.LocalName.RemoveUnderscoresAndDashes() == name)
                .ToList();

        if (!elements.Any()) {
            var lowerName = name?.ToLower(Culture).AsNamespaced(Namespace);

            elements = root.Descendants()
                .Where(e => e.Name.LocalName.RemoveUnderscoresAndDashes() == lowerName)
                .ToList();
        }

        PopulateListFromElements(t, elements, list);

        // get properties too, not just list items
        // only if this isn't a generic type
        if (!type.IsGenericType)
            Map(list, root.Element(propName.AsNamespaced(Namespace)!) ?? root);

        return list;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
object HandleListDerivative(XElement root, string propName, Type type) {
        var t = type.IsGenericType
            ? type.GetGenericArguments()[0]
            : type.BaseType!.GetGenericArguments()[0];

        var list = (IList)Activator.CreateInstance(type)!;

        var name      = t.Name;
        var attribute = t.GetAttribute<DeserializeAsAttribute>();

        if (attribute != null)
            name = attribute.Name;

        // Try to find a container element first using the property name
        XElement? container = null;

        // Try the property name first (skip if it contains invalid XML name characters like ` in generic types)
        if (IsValidXmlElementName(propName)) {
            container = GetElementByName(root, propName.AsNamespaced(Namespace));
        }

        // Check if root itself matches the container naming
        if (container == null && IsValidXmlElementName(propName)) {
            var rootName = root.Name.LocalName;

            if (rootName.Equals(propName, StringComparison.OrdinalIgnoreCase)) {
                container = root;
            }
        }

        IList<XElement> elements;

        // If we found a specific container, use Elements() to get only direct children
        // This prevents nested lists from being incorrectly flattened
        if (container is { HasElements: true }) {
            elements = TryFindElementsByNameVariations(container, t.Name, name, useDirectChildrenOnly: true);
        }
        else {
            // No container found - use Descendants() for backward compatibility
            // This handles cases where items are nested at varying depths without a clear container
            elements = TryFindElementsByNameVariations(root, t.Name, name, useDirectChildrenOnly: false);
        }

        PopulateListFromElements(t, elements, list);

        // get properties too, not just list items
        // only if this isn't a generic type
        if (!type.IsGenericType)
            Map(list, root.Element(propName.AsNamespaced(Namespace)!) ?? root);

        return list;
    }
```

### 🔹 函式: `XmlDeserializer.Deserialize()`
- **變更前簽章 (Before)**: `XmlDeserializer.Deserialize(RestResponse response)` (L35~L59)
- **變更後簽章 (After)**: `XmlDeserializer.Deserialize(RestResponse response)` (L35~L67)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public virtual T? Deserialize<T>(RestResponse response) {
        if (string.IsNullOrEmpty(response.Content))
            return default;

        var doc         = XDocument.Parse(response.Content!);
        var root        = doc.Root;
        var rootElement = response.RootElement ?? RootElement;

        if (rootElement != null && doc.Root != null)
            root = doc.Root.DescendantsAndSelf(rootElement.AsNamespaced(Namespace)).SingleOrDefault();

        // autodetect xml namespace
        if (Namespace.IsEmpty())
            RemoveNamespace(doc);

        var x       = Activator.CreateInstance<T>();
        var objType = x!.GetType();

        if (objType.IsSubclassOfRawGeneric(typeof(List<>)))
            x = (T)HandleListDerivative(root!, objType.Name, objType);
        else
            x = (T)Map(x, root!);

        return x;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public virtual T? Deserialize<T>(RestResponse response) {
        if (string.IsNullOrEmpty(response.Content))
            return default;

        var doc         = XDocument.Parse(response.Content!);
        var root        = doc.Root;
        var rootElement = response.RootElement ?? RootElement;

        if (rootElement != null && doc.Root != null) {
            var namespacedRoot = rootElement.AsNamespaced(Namespace);
            // Prefer the shallowest match to avoid nested elements with the same name
            root = namespacedRoot != null 
                ? doc.Root.Element(namespacedRoot) 
                    ?? doc.Root.DescendantsAndSelf(namespacedRoot)
                        .OrderBy(e => e.Ancestors().Count())
                        .FirstOrDefault()
                : null;
        }

        // autodetect xml namespace
        if (Namespace.IsEmpty())
            RemoveNamespace(doc);

        var x       = Activator.CreateInstance<T>();
        var objType = x!.GetType();

        if (objType.IsSubclassOfRawGeneric(typeof(List<>)))
            x = (T)HandleListDerivative(root!, objType.Name, objType);
        else
            x = (T)Map(x, root!);

        return x;
    }
```


---

### 🔹 Commit #12: `bf4008f9`
- **完整 Hash**: `bf4008f972257908d666b2884ec7fe330b759424`
- **說明 (Ground Truth)**: Allow tabs in header value, fixes #2263
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp/Parameters/HeaderParameter.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:18, E:17, A:0) ➔ After(N:18, E:17, A:0)
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

### 🔹 函式: `HeaderParameter.IsInvalidHeaderString()`
- **變更前簽章 (Before)**: `HeaderParameter.IsInvalidHeaderString(string stringValue)` (L52~L64)
- **變更後簽章 (After)**: `HeaderParameter.IsInvalidHeaderString(string stringValue)` (L52~L63)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static bool IsInvalidHeaderString(string stringValue) {
        // ReSharper disable once ForCanBeConvertedToForeach
        for (var i = 0; i < stringValue.Length; i++) {
            switch (stringValue[i]) {
                case '\t':
                case '\r':
                case '\n':
                    return true;
            }
        }

        return false;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static bool IsInvalidHeaderString(string stringValue) {
        // ReSharper disable once ForCanBeConvertedToForeach
        for (var i = 0; i < stringValue.Length; i++) {
            switch (stringValue[i]) {
                case '\r':
                case '\n':
                    return true;
            }
        }

        return false;
    }
```


---

### 🔹 Commit #13: `6391624b`
- **完整 Hash**: `6391624bfaaf3f4df56481d308e755e96b5eb1b9`
- **說明 (Ground Truth)**: Added extensions for getting content header values (#2247)
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp/Response/RestResponseExtensions.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:10, E:9, A:0) ➔ After(N:17, E:17, A:0)
- **差分統計**: +Nodes: 10, -Nodes: 3, +Edges: 11, -Edges: 3, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `response.ContentHeaders
                ?.Where(x => NameIs(x.Name, headerName))
                .Select(x => x.Value.ToString() ?? "")
                .ToArray (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `response.Headers?.FirstOrDefault(x => NameIs(x.Name, headerName))?.Value.ToString (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `response.ContentHeaders?.FirstOrDefault (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `x.Value.ToString (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `response.Headers
                ?.Where(x => NameIs(x.Name, headerName))
                .Select(x => x.Value.ToString() ?? "")
                .ToArray (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `response.ContentHeaders?.FirstOrDefault(x => NameIs(x.Name, headerName))?.Value.ToString (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `RestResponseExtensions.GetContentHeaderValue` (FUNCTION_DEF)
  • + [新增節點] `response.ContentHeaders
                ?.Where(x => NameIs(x.Name, headerName))
                .Select (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `response.ContentHeaders
                ?.Where (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `RestResponseExtensions.GetContentHeaderValues` (FUNCTION_DEF)
  • - [移除節點] `response.Headers?.FirstOrDefault(x => NameIs(x.Name, headerName))?.Value?.ToString (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `response.Headers
                ?.Where(x => NameIs(x.Name, headerName))
                .Select(x => x.Value?.ToString() ?? "")
                .ToArray (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `x.Value?.ToString (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `RestResponseExtensions.GetHeaderValue` ──[CALLS]──> `response.Headers?.FirstOrDefault(x => NameIs(x.Name, headerName))?.Value.ToString (External/BCL)`
  • + [新增呼叫邊] `RestResponseExtensions.GetHeaderValues` ──[CALLS]──> `response.Headers
                ?.Where(x => NameIs(x.Name, headerName))
                .Select(x => x.Value.ToString() ?? "")
                .ToArray (External/BCL)`
  • _... 以及其餘 12 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RestResponseExtensions.GetHeaderValue()`
- **變更前簽章 (Before)**: `RestResponseExtensions.GetHeaderValue(this RestResponse response, string headerName)` (L24~L25)
- **變更後簽章 (After)**: `RestResponseExtensions.GetHeaderValue(this RestResponse response, string headerName)` (L24~L25)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static string? GetHeaderValue(this RestResponse response, string headerName)
        => response.Headers?.FirstOrDefault(x => NameIs(x.Name, headerName))?.Value?.ToString();
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static string? GetHeaderValue(this RestResponse response, string headerName)
        => response.Headers?.FirstOrDefault(x => NameIs(x.Name, headerName))?.Value.ToString();
```

### 🔹 函式: `RestResponseExtensions.GetHeaderValues()`
- **變更前簽章 (Before)**: `RestResponseExtensions.GetHeaderValues(this RestResponse response, string headerName)` (L33~L38)
- **變更後簽章 (After)**: `RestResponseExtensions.GetHeaderValues(this RestResponse response, string headerName)` (L33~L38)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static string[] GetHeaderValues(this RestResponse response, string headerName)
        => response.Headers
                ?.Where(x => NameIs(x.Name, headerName))
                .Select(x => x.Value?.ToString() ?? "")
                .ToArray() ??
            [];
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static string[] GetHeaderValues(this RestResponse response, string headerName)
        => response.Headers
                ?.Where(x => NameIs(x.Name, headerName))
                .Select(x => x.Value.ToString() ?? "")
                .ToArray() ??
            [];
```


---

### 🔹 Commit #14: `fef25a56`
- **完整 Hash**: `fef25a56d57f6ac8377d34ce50451ef3be95e9e7`
- **說明 (Ground Truth)**: Allow setting parameter content type (#2249)
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp/Parameters/Parameter.cs`
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

### 🔹 Commit #15: `3cbaa429`
- **完整 Hash**: `3cbaa4291455159f8323e9e1707c139ec3fa1dbb`
- **說明 (Ground Truth)**: Fix the XML docs
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp/RestClient.Extensions.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:28, E:36, A:0) ➔ After(N:28, E:36, A:0)
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

### 🔹 Commit #16: `dcb11c0b`
- **完整 Hash**: `dcb11c0beed7df8a7151ebcc11c4c18e426fd82c`
- **說明 (Ground Truth)**: Fix the http client timeout
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp/RestClient.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:28, E:27, A:0) ➔ After(N:28, E:27, A:0)
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

### 🔹 函式: `RestClient()`
- **變更前簽章 (Before)**: `RestClient(
        RestClientOptions       options,
        ConfigureHeaders?       configureDefaultHeaders = null,
        ConfigureSerialization? configureSerialization  = null,
        bool                    useClientFactory        = false
    )` (L64~L99)
- **變更後簽章 (After)**: `RestClient(
        RestClientOptions       options,
        ConfigureHeaders?       configureDefaultHeaders = null,
        ConfigureSerialization? configureSerialization  = null,
        bool                    useClientFactory        = false
    )` (L66~L105)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public RestClient(
        RestClientOptions       options,
        ConfigureHeaders?       configureDefaultHeaders = null,
        ConfigureSerialization? configureSerialization  = null,
        bool                    useClientFactory        = false
    ) {
        if (useClientFactory && options.BaseUrl == null) {
            throw new ArgumentException("BaseUrl must be set when using a client factory");
        }

        ConfigureSerializers(configureSerialization);
        Options = new ReadOnlyRestClientOptions(options);
        DefaultParameters = new DefaultParameters(Options);

        if (useClientFactory) {
            _disposeHttpClient = false;
            HttpClient         = SimpleClientFactory.GetClient(options.BaseUrl!, GetClient);
        }
        else {
            _disposeHttpClient = true;
            HttpClient         = GetClient();
        }

        return;

        HttpClient GetClient() {
            var handler = new HttpClientHandler();
            ConfigureHttpMessageHandler(handler, options);
            var finalHandler = options.ConfigureMessageHandler?.Invoke(handler) ?? handler;
            var httpClient = new HttpClient(finalHandler);
            ConfigureHttpClient(httpClient, options);
            ConfigureDefaultParameters(options);
            configureDefaultHeaders?.Invoke(httpClient.DefaultRequestHeaders);
            return httpClient;
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public RestClient(
        RestClientOptions       options,
        ConfigureHeaders?       configureDefaultHeaders = null,
        ConfigureSerialization? configureSerialization  = null,
        bool                    useClientFactory        = false
    ) {
        if (useClientFactory && options.BaseUrl == null) {
            throw new ArgumentException("BaseUrl must be set when using a client factory");
        }

        ConfigureSerializers(configureSerialization);
        Options           = new ReadOnlyRestClientOptions(options);
        DefaultParameters = new DefaultParameters(Options);

        if (useClientFactory) {
            _disposeHttpClient = false;
            HttpClient         = SimpleClientFactory.GetClient(options.BaseUrl!, GetClient);
        }
        else {
            _disposeHttpClient = true;
            HttpClient         = GetClient();
        }

        return;

        HttpClient GetClient() {
            var handler = new HttpClientHandler();
            ConfigureHttpMessageHandler(handler, options);
            var finalHandler = options.ConfigureMessageHandler?.Invoke(handler) ?? handler;
            var httpClient   = new HttpClient(finalHandler);
            ConfigureHttpClient(httpClient, options);

            // We will use Options.Timeout in ExecuteAsInternalAsync method
            httpClient.Timeout = Timeout.InfiniteTimeSpan;

            ConfigureDefaultParameters(options);
            configureDefaultHeaders?.Invoke(httpClient.DefaultRequestHeaders);
            return httpClient;
        }
    }
```

### 🔹 函式: `ConfigureHttpClient()`
- **變更前簽章 (Before)**: `ConfigureHttpClient(HttpClient httpClient, RestClientOptions options)` (L222~L227)
- **變更後簽章 (After)**: `ConfigureHttpClient(HttpClient httpClient, RestClientOptions options)` (L228~L230)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static void ConfigureHttpClient(HttpClient httpClient, RestClientOptions options) {
        // We will use Options.Timeout in ExecuteAsInternalAsync method
        httpClient.Timeout = Timeout.InfiniteTimeSpan;

        if (options.Expect100Continue != null) httpClient.DefaultRequestHeaders.ExpectContinue = options.Expect100Continue;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static void ConfigureHttpClient(HttpClient httpClient, RestClientOptions options) {
        if (options.Expect100Continue != null) httpClient.DefaultRequestHeaders.ExpectContinue = options.Expect100Continue;
    }
```

### 🔹 函式: `GetClient()`
- **變更前簽章 (Before)**: `GetClient()` (L89~L98)
- **變更後簽章 (After)**: `GetClient()` (L91~L104)

#### ◀️ 變更前實作碼 (Before Implementation):
```
HttpClient GetClient() {
            var handler = new HttpClientHandler();
            ConfigureHttpMessageHandler(handler, options);
            var finalHandler = options.ConfigureMessageHandler?.Invoke(handler) ?? handler;
            var httpClient = new HttpClient(finalHandler);
            ConfigureHttpClient(httpClient, options);
            ConfigureDefaultParameters(options);
            configureDefaultHeaders?.Invoke(httpClient.DefaultRequestHeaders);
            return httpClient;
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
HttpClient GetClient() {
            var handler = new HttpClientHandler();
            ConfigureHttpMessageHandler(handler, options);
            var finalHandler = options.ConfigureMessageHandler?.Invoke(handler) ?? handler;
            var httpClient   = new HttpClient(finalHandler);
            ConfigureHttpClient(httpClient, options);

            // We will use Options.Timeout in ExecuteAsInternalAsync method
            httpClient.Timeout = Timeout.InfiniteTimeSpan;

            ConfigureDefaultParameters(options);
            configureDefaultHeaders?.Invoke(httpClient.DefaultRequestHeaders);
            return httpClient;
        }
```


---

### 🔹 Commit #17: `f3642c1b`
- **完整 Hash**: `f3642c1bdc937f02c5a178305c1a437b96a39189`
- **說明 (Ground Truth)**: Set UserAgent as a default header parameter (#2157)
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp/RestClient.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:26, E:24, A:0) ➔ After(N:29, E:28, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 2, +Edges: 6, -Edges: 2, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `DefaultParameters.Any (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `DefaultParameters.AddParameter (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `Parameter.CreateParameter (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `ConfigureDefaultParameters` (FUNCTION_DEF)
  • + [新增節點] `DefaultParameters.RemoveParameter (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `httpClient.DefaultRequestHeaders.TryAddWithoutValidation (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `httpClient.DefaultRequestHeaders.UserAgent.All (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `GetClient` ──[CALLS]──> `ConfigureDefaultParameters`
  • + [新增呼叫邊] `RestClient` ──[CALLS]──> `ConfigureDefaultParameters`
  • + [新增呼叫邊] `ConfigureDefaultParameters` ──[CALLS]──> `DefaultParameters.Any (External/BCL)`
  • + [新增呼叫邊] `ConfigureDefaultParameters` ──[CALLS]──> `DefaultParameters.RemoveParameter (External/BCL)`
  • + [新增呼叫邊] `ConfigureDefaultParameters` ──[CALLS]──> `DefaultParameters.AddParameter (External/BCL)`
  • + [新增呼叫邊] `ConfigureDefaultParameters` ──[CALLS]──> `Parameter.CreateParameter (External/BCL)`
  • - [移除呼叫邊] `ConfigureHttpClient` ──[CALLS]──> `httpClient.DefaultRequestHeaders.UserAgent.All (External/BCL)`
  • - [移除呼叫邊] `ConfigureHttpClient` ──[CALLS]──> `httpClient.DefaultRequestHeaders.TryAddWithoutValidation (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RestClient()`
- **變更前簽章 (Before)**: `RestClient(
        HttpClient              httpClient,
        RestClientOptions?      options,
        bool                    disposeHttpClient      = false,
        ConfigureSerialization? configureSerialization = null
    )` (L165~L185)
- **變更後簽章 (After)**: `RestClient(
        HttpClient              httpClient,
        RestClientOptions?      options,
        bool                    disposeHttpClient      = false,
        ConfigureSerialization? configureSerialization = null
    )` (L165~L188)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public RestClient(
        HttpClient              httpClient,
        RestClientOptions?      options,
        bool                    disposeHttpClient      = false,
        ConfigureSerialization? configureSerialization = null
    ) {
        ConfigureSerializers(configureSerialization);

        HttpClient         = httpClient;
        _disposeHttpClient = disposeHttpClient;

        if (httpClient.BaseAddress != null && options != null && options.BaseUrl == null) {
            options.BaseUrl = httpClient.BaseAddress;
        }

        var opt = options ?? new RestClientOptions();
        Options           = new ReadOnlyRestClientOptions(opt);
        DefaultParameters = new DefaultParameters(Options);

        if (options != null) ConfigureHttpClient(httpClient, options);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public RestClient(
        HttpClient              httpClient,
        RestClientOptions?      options,
        bool                    disposeHttpClient      = false,
        ConfigureSerialization? configureSerialization = null
    ) {
        ConfigureSerializers(configureSerialization);

        HttpClient         = httpClient;
        _disposeHttpClient = disposeHttpClient;

        if (httpClient.BaseAddress != null && options != null && options.BaseUrl == null) {
            options.BaseUrl = httpClient.BaseAddress;
        }

        var opt = options ?? new RestClientOptions();
        Options           = new ReadOnlyRestClientOptions(opt);
        DefaultParameters = new DefaultParameters(Options);

        if (options != null) {
            ConfigureHttpClient(httpClient, options);
            ConfigureDefaultParameters(options);
        }
    }
```

### 🔹 函式: `RestClient()`
- **變更前簽章 (Before)**: `RestClient(
        RestClientOptions       options,
        ConfigureHeaders?       configureDefaultHeaders = null,
        ConfigureSerialization? configureSerialization  = null,
        bool                    useClientFactory        = false
    )` (L64~L98)
- **變更後簽章 (After)**: `RestClient(
        RestClientOptions       options,
        ConfigureHeaders?       configureDefaultHeaders = null,
        ConfigureSerialization? configureSerialization  = null,
        bool                    useClientFactory        = false
    )` (L64~L98)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public RestClient(
        RestClientOptions       options,
        ConfigureHeaders?       configureDefaultHeaders = null,
        ConfigureSerialization? configureSerialization  = null,
        bool                    useClientFactory        = false
    ) {
        if (useClientFactory && options.BaseUrl == null) {
            throw new ArgumentException("BaseUrl must be set when using a client factory");
        }

        ConfigureSerializers(configureSerialization);
        Options = new ReadOnlyRestClientOptions(options);

        if (useClientFactory) {
            _disposeHttpClient = false;
            HttpClient         = SimpleClientFactory.GetClient(options.BaseUrl!, GetClient);
        }
        else {
            _disposeHttpClient = true;
            HttpClient         = GetClient();
        }

        DefaultParameters = new DefaultParameters(Options);

        HttpClient GetClient() {
            var handler = new HttpClientHandler();
            ConfigureHttpMessageHandler(handler, Options);
            var finalHandler = options.ConfigureMessageHandler?.Invoke(handler) ?? handler;

            var httpClient = new HttpClient(finalHandler);
            ConfigureHttpClient(httpClient, options);
            configureDefaultHeaders?.Invoke(httpClient.DefaultRequestHeaders);
            return httpClient;
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public RestClient(
        RestClientOptions       options,
        ConfigureHeaders?       configureDefaultHeaders = null,
        ConfigureSerialization? configureSerialization  = null,
        bool                    useClientFactory        = false
    ) {
        if (useClientFactory && options.BaseUrl == null) {
            throw new ArgumentException("BaseUrl must be set when using a client factory");
        }

        ConfigureSerializers(configureSerialization);
        Options = new ReadOnlyRestClientOptions(options);
        DefaultParameters = new DefaultParameters(Options);

        if (useClientFactory) {
            _disposeHttpClient = false;
            HttpClient         = SimpleClientFactory.GetClient(options.BaseUrl!, GetClient);
        }
        else {
            _disposeHttpClient = true;
            HttpClient         = GetClient();
        }

        HttpClient GetClient() {
            var handler = new HttpClientHandler();
            ConfigureHttpMessageHandler(handler, Options);
            var finalHandler = options.ConfigureMessageHandler?.Invoke(handler) ?? handler;

            var httpClient = new HttpClient(finalHandler);
            ConfigureHttpClient(httpClient, options);
            ConfigureDefaultParameters(options);
            configureDefaultHeaders?.Invoke(httpClient.DefaultRequestHeaders);
            return httpClient;
        }
    }
```

### 🔹 函式: `ConfigureHttpClient()`
- **變更前簽章 (Before)**: `ConfigureHttpClient(HttpClient httpClient, RestClientOptions options)` (L218~L227)
- **變更後簽章 (After)**: `ConfigureHttpClient(HttpClient httpClient, RestClientOptions options)` (L221~L225)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static void ConfigureHttpClient(HttpClient httpClient, RestClientOptions options) {
        if (options.MaxTimeout > 0) httpClient.Timeout = TimeSpan.FromMilliseconds(options.MaxTimeout);

        if (options.UserAgent != null &&
            httpClient.DefaultRequestHeaders.UserAgent.All(x => $"{x.Product?.Name}/{x.Product?.Version}" != options.UserAgent)) {
            httpClient.DefaultRequestHeaders.TryAddWithoutValidation(KnownHeaders.UserAgent, options.UserAgent);
        }

        if (options.Expect100Continue != null) httpClient.DefaultRequestHeaders.ExpectContinue = options.Expect100Continue;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static void ConfigureHttpClient(HttpClient httpClient, RestClientOptions options) {
        if (options.MaxTimeout > 0) httpClient.Timeout = TimeSpan.FromMilliseconds(options.MaxTimeout);

        if (options.Expect100Continue != null) httpClient.DefaultRequestHeaders.ExpectContinue = options.Expect100Continue;
    }
```

### 🔹 函式: `GetClient()`
- **變更前簽章 (Before)**: `GetClient()` (L88~L97)
- **變更後簽章 (After)**: `GetClient()` (L87~L97)

#### ◀️ 變更前實作碼 (Before Implementation):
```
HttpClient GetClient() {
            var handler = new HttpClientHandler();
            ConfigureHttpMessageHandler(handler, Options);
            var finalHandler = options.ConfigureMessageHandler?.Invoke(handler) ?? handler;

            var httpClient = new HttpClient(finalHandler);
            ConfigureHttpClient(httpClient, options);
            configureDefaultHeaders?.Invoke(httpClient.DefaultRequestHeaders);
            return httpClient;
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
HttpClient GetClient() {
            var handler = new HttpClientHandler();
            ConfigureHttpMessageHandler(handler, Options);
            var finalHandler = options.ConfigureMessageHandler?.Invoke(handler) ?? handler;

            var httpClient = new HttpClient(finalHandler);
            ConfigureHttpClient(httpClient, options);
            ConfigureDefaultParameters(options);
            configureDefaultHeaders?.Invoke(httpClient.DefaultRequestHeaders);
            return httpClient;
        }
```


---

### 🔹 Commit #18: `cc44c361`
- **完整 Hash**: `cc44c361d4aa7caa5b868d4440820cd2e382a7ef`
- **說明 (Ground Truth)**: Fix authenticator docs
- **變更檔案數**: 1

#### 📄 檔案: `src/RestSharp/RestClient.Extensions.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:59, E:72, A:0) ➔ After(N:59, E:71, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除呼叫邊] `RestClientExtensions.ExecuteAsync` ──[CALLS]──> `nameof (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RestClientExtensions.ExecuteAsync()`
- **變更前簽章 (Before)**: `RestClientExtensions.ExecuteAsync(
        this IRestClient  client,
        RestRequest       request,
        CancellationToken cancellationToken = default
    )` (L100~L110)
- **變更後簽章 (After)**: `RestClientExtensions.ExecuteAsync(
        this IRestClient  client,
        RestRequest       request,
        CancellationToken cancellationToken = default
    )` (L100~L107)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static async Task<RestResponse<T>> ExecuteAsync<T>(
        this IRestClient  client,
        RestRequest       request,
        CancellationToken cancellationToken = default
    ) {
        if (request == null)
            throw new ArgumentNullException(nameof(request));

        var response = await client.ExecuteAsync(request, cancellationToken).ConfigureAwait(false);
        return client.Serializers.Deserialize<T>(request, response, client.Options);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static async Task<RestResponse<T>> ExecuteAsync<T>(
        this IRestClient  client,
        RestRequest       request,
        CancellationToken cancellationToken = default
    ) {
        var response = await client.ExecuteAsync(request, cancellationToken).ConfigureAwait(false);
        return client.Serializers.Deserialize<T>(request, response, client.Options);
    }
```


---

### 🔹 Commit #19: `c9482f31`
- **完整 Hash**: `c9482f3171fee432077bf8689fa9ed4572ff4114`
- **說明 (Ground Truth)**: Timeout as TimeSpan, Support custom request timeout
- **變更檔案數**: 4

#### 📄 檔案: `src/RestSharp/Options/RestClientOptions.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:7, E:2, A:0) ➔ After(N:7, E:2, A:0)
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

#### 📄 檔案: `src/RestSharp/Request/RestRequest.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:21, E:14, A:0) ➔ After(N:21, E:14, A:0)
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

#### 📄 檔案: `src/RestSharp/RestClient.Async.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:39, E:40, A:0) ➔ After(N:40, E:40, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `DefaultTimeout` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RestClient.ExecuteRequestAsync()`
- **變更前簽章 (Before)**: `RestClient.ExecuteRequestAsync(RestRequest request, CancellationToken cancellationToken)` (L72~L130)
- **變更後簽章 (After)**: `RestClient.ExecuteRequestAsync(RestRequest request, CancellationToken cancellationToken)` (L74~L132)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async Task<HttpResponse> ExecuteRequestAsync(RestRequest request, CancellationToken cancellationToken) {
        Ensure.NotNull(request, nameof(request));

        // Make sure we are not disposed of when someone tries to call us!
        if (_disposed) {
            throw new ObjectDisposedException(nameof(RestClient));
        }

        request.ValidateParameters();
        var authenticator = request.Authenticator ?? Options.Authenticator;
        if (authenticator != null) await authenticator.Authenticate(this, request).ConfigureAwait(false);

        using var requestContent = new RequestContent(this, request);

        var httpMethod = AsHttpMethod(request.Method);
        var url        = this.BuildUri(request);

        using var message    = new HttpRequestMessage(httpMethod, url) { Content = requestContent.BuildContent() };
        message.Headers.Host         = Options.BaseHost;
        message.Headers.CacheControl = request.CachePolicy ?? Options.CachePolicy;

        using var timeoutCts = new CancellationTokenSource(request.Timeout > 0 ? request.Timeout : int.MaxValue);
        using var cts        = CancellationTokenSource.CreateLinkedTokenSource(timeoutCts.Token, cancellationToken);

        var ct = cts.Token;

        try {
            // Make sure we have a cookie container if not provided in the request
            var cookieContainer = request.CookieContainer ??= new CookieContainer();

            var headers = new RequestHeaders()
                .AddHeaders(request.Parameters)
                .AddHeaders(DefaultParameters)
                .AddAcceptHeader(AcceptedContentTypes)
                .AddCookieHeaders(url, cookieContainer)
                .AddCookieHeaders(url, Options.CookieContainer);

            message.AddHeaders(headers);

            if (request.OnBeforeRequest != null) await request.OnBeforeRequest(message).ConfigureAwait(false);

            var responseMessage = await HttpClient.SendAsync(message, request.CompletionOption, ct).ConfigureAwait(false);

            // Parse all the cookies from the response and update the cookie jar with cookies
            if (responseMessage.Headers.TryGetValues(KnownHeaders.SetCookie, out var cookiesHeader)) {
                // ReSharper disable once PossibleMultipleEnumeration
                cookieContainer.AddCookies(url, cookiesHeader);
                // ReSharper disable once PossibleMultipleEnumeration
                Options.CookieContainer?.AddCookies(url, cookiesHeader);
            }

            if (request.OnAfterRequest != null) await request.OnAfterRequest(responseMessage).ConfigureAwait(false);

            return new HttpResponse(responseMessage, url, cookieContainer, null, timeoutCts.Token);
        }
        catch (Exception ex) {
            return new HttpResponse(null, url, null, ex, timeoutCts.Token);
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async Task<HttpResponse> ExecuteRequestAsync(RestRequest request, CancellationToken cancellationToken) {
        Ensure.NotNull(request, nameof(request));

        // Make sure we are not disposed of when someone tries to call us!
        if (_disposed) {
            throw new ObjectDisposedException(nameof(RestClient));
        }

        request.ValidateParameters();
        var authenticator = request.Authenticator ?? Options.Authenticator;
        if (authenticator != null) await authenticator.Authenticate(this, request).ConfigureAwait(false);

        using var requestContent = new RequestContent(this, request);

        var httpMethod = AsHttpMethod(request.Method);
        var url        = this.BuildUri(request);

        using var message    = new HttpRequestMessage(httpMethod, url) { Content = requestContent.BuildContent() };
        message.Headers.Host         = Options.BaseHost;
        message.Headers.CacheControl = request.CachePolicy ?? Options.CachePolicy;

        using var timeoutCts = new CancellationTokenSource(request.Timeout ?? Options.Timeout ?? DefaultTimeout);
        using var cts        = CancellationTokenSource.CreateLinkedTokenSource(timeoutCts.Token, cancellationToken);

        var ct = cts.Token;

        try {
            // Make sure we have a cookie container if not provided in the request
            var cookieContainer = request.CookieContainer ??= new CookieContainer();

            var headers = new RequestHeaders()
                .AddHeaders(request.Parameters)
                .AddHeaders(DefaultParameters)
                .AddAcceptHeader(AcceptedContentTypes)
                .AddCookieHeaders(url, cookieContainer)
                .AddCookieHeaders(url, Options.CookieContainer);

            message.AddHeaders(headers);

            if (request.OnBeforeRequest != null) await request.OnBeforeRequest(message).ConfigureAwait(false);

            var responseMessage = await HttpClient.SendAsync(message, request.CompletionOption, ct).ConfigureAwait(false);

            // Parse all the cookies from the response and update the cookie jar with cookies
            if (responseMessage.Headers.TryGetValues(KnownHeaders.SetCookie, out var cookiesHeader)) {
                // ReSharper disable once PossibleMultipleEnumeration
                cookieContainer.AddCookies(url, cookiesHeader);
                // ReSharper disable once PossibleMultipleEnumeration
                Options.CookieContainer?.AddCookies(url, cookiesHeader);
            }

            if (request.OnAfterRequest != null) await request.OnAfterRequest(responseMessage).ConfigureAwait(false);

            return new HttpResponse(responseMessage, url, cookieContainer, null, timeoutCts.Token);
        }
        catch (Exception ex) {
            return new HttpResponse(null, url, null, ex, timeoutCts.Token);
        }
    }
```


#### 📄 檔案: `src/RestSharp/RestClient.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:26, E:24, A:0) ➔ After(N:25, E:23, A:0)
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
  • - [移除節點] `TimeSpan.FromMilliseconds (External/BCL)` (FUNCTION_DEF)
  • - [移除呼叫邊] `ConfigureHttpClient` ──[CALLS]──> `TimeSpan.FromMilliseconds (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `ConfigureHttpClient()`
- **變更前簽章 (Before)**: `ConfigureHttpClient(HttpClient httpClient, RestClientOptions options)` (L218~L227)
- **變更後簽章 (After)**: `ConfigureHttpClient(HttpClient httpClient, RestClientOptions options)` (L218~L229)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static void ConfigureHttpClient(HttpClient httpClient, RestClientOptions options) {
        if (options.MaxTimeout > 0) httpClient.Timeout = TimeSpan.FromMilliseconds(options.MaxTimeout);

        if (options.UserAgent != null &&
            httpClient.DefaultRequestHeaders.UserAgent.All(x => $"{x.Product?.Name}/{x.Product?.Version}" != options.UserAgent)) {
            httpClient.DefaultRequestHeaders.TryAddWithoutValidation(KnownHeaders.UserAgent, options.UserAgent);
        }

        if (options.Expect100Continue != null) httpClient.DefaultRequestHeaders.ExpectContinue = options.Expect100Continue;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static void ConfigureHttpClient(HttpClient httpClient, RestClientOptions options) {
        
        // We will use Options.Timeout in ExecuteAsInternalAsync method
        httpClient.Timeout = Timeout.InfiniteTimeSpan;

        if (options.UserAgent != null &&
            httpClient.DefaultRequestHeaders.UserAgent.All(x => $"{x.Product?.Name}/{x.Product?.Version}" != options.UserAgent)) {
            httpClient.DefaultRequestHeaders.TryAddWithoutValidation(KnownHeaders.UserAgent, options.UserAgent);
        }

        if (options.Expect100Continue != null) httpClient.DefaultRequestHeaders.ExpectContinue = options.Expect100Continue;
    }
```


---

### 🔹 Commit #20: `794348ec`
- **完整 Hash**: `794348ec29a17b1ff30ea4d8a77091aa61d56dab`
- **說明 (Ground Truth)**: Merge client- and request-level cookies in the header. Also, dispose the request if not downloading data. (#2056)
- **變更檔案數**: 3

#### 📄 檔案: `src/RestSharp/Extensions/CookieContainerExtensions.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:2, E:1, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `cookieContainer.SetCookies (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `CookieContainerExtensions.AddCookies` (FUNCTION_DEF)
  • + [新增呼叫邊] `CookieContainerExtensions.AddCookies` ──[CALLS]──> `cookieContainer.SetCookies (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `src/RestSharp/Request/RequestHeaders.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:9, E:7, A:0) ➔ After(N:19, E:17, A:0)
- **差分統計**: +Nodes: 10, -Nodes: 0, +Edges: 10, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `RequestHeaders.SplitHeader` (FUNCTION_DEF)
  • + [新增節點] `x.Trim (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `header.Split(';').Select (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `Parameters.GetParameters<HeaderParameter>().FirstOrDefault (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `string.Join (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `existing.Value.ToString (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `newCookies.Union (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `header.Split (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `string.IsNullOrWhiteSpace (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `Parameters.GetParameters<HeaderParameter> (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `RequestHeaders.AddCookieHeaders` ──[CALLS]──> `string.IsNullOrWhiteSpace (External/BCL)`
  • + [新增呼叫邊] `RequestHeaders.AddCookieHeaders` ──[CALLS]──> `RequestHeaders.SplitHeader`
  • + [新增呼叫邊] `RequestHeaders.AddCookieHeaders` ──[CALLS]──> `Parameters.GetParameters<HeaderParameter>().FirstOrDefault (External/BCL)`
  • + [新增呼叫邊] `RequestHeaders.AddCookieHeaders` ──[CALLS]──> `Parameters.GetParameters<HeaderParameter> (External/BCL)`
  • + [新增呼叫邊] `RequestHeaders.AddCookieHeaders` ──[CALLS]──> `newCookies.Union (External/BCL)`
  • _... 以及其餘 5 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RequestHeaders.AddCookieHeaders()`
- **變更前簽章 (Before)**: `RequestHeaders.AddCookieHeaders(CookieContainer cookieContainer, Uri uri)` (L42~L50)
- **變更後簽章 (After)**: `RequestHeaders.AddCookieHeaders(Uri uri, CookieContainer? cookieContainer)` (L42~L61)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public RequestHeaders AddCookieHeaders(CookieContainer cookieContainer, Uri uri) {
        var cookies = cookieContainer.GetCookieHeader(uri);

        if (cookies.Length > 0) {
            Parameters.AddParameter(new HeaderParameter(KnownHeaders.Cookie, cookies));
        }

        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public RequestHeaders AddCookieHeaders(Uri uri, CookieContainer? cookieContainer) {
        if (cookieContainer == null) return this;

        var cookies = cookieContainer.GetCookieHeader(uri);

        if (string.IsNullOrWhiteSpace(cookies)) return this;

        var newCookies = SplitHeader(cookies);
        var existing   = Parameters.GetParameters<HeaderParameter>().FirstOrDefault(x => x.Name == KnownHeaders.Cookie);

        if (existing?.Value != null) {
            newCookies = newCookies.Union(SplitHeader(existing.Value.ToString()!));
        }

        Parameters.AddParameter(new HeaderParameter(KnownHeaders.Cookie, string.Join("; ", newCookies)));

        return this;

        IEnumerable<string> SplitHeader(string header) => header.Split(';').Select(x => x.Trim());
    }
```


#### 📄 檔案: `src/RestSharp/RestClient.Async.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:36, E:37, A:0) ➔ After(N:38, E:39, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 2, +Edges: 4, -Edges: 2, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `cookieContainer.AddCookies (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `Options.CookieContainer?.AddCookies (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `HttpResponse.Dispose` (FUNCTION_DEF)
  • + [新增節點] `new RequestHeaders()
                .AddHeaders(request.Parameters)
                .AddHeaders(DefaultParameters)
                .AddAcceptHeader(AcceptedContentTypes)
                .AddCookieHeaders(url, cookieContainer)
                .AddCookieHeaders (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `cookieContainer.SetCookies (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `headers.AddCookieHeaders (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `RestClient.ExecuteRequestAsync` ──[CALLS]──> `new RequestHeaders()
                .AddHeaders(request.Parameters)
                .AddHeaders(DefaultParameters)
                .AddAcceptHeader(AcceptedContentTypes)
                .AddCookieHeaders(url, cookieContainer)
                .AddCookieHeaders (External/BCL)`
  • + [新增呼叫邊] `RestClient.ExecuteRequestAsync` ──[CALLS]──> `cookieContainer.AddCookies (External/BCL)`
  • + [新增呼叫邊] `RestClient.ExecuteRequestAsync` ──[CALLS]──> `Options.CookieContainer?.AddCookies (External/BCL)`
  • + [新增呼叫邊] `HttpResponse.Dispose` ──[CALLS]──> `HttpResponse.Dispose`
  • - [移除呼叫邊] `RestClient.ExecuteRequestAsync` ──[CALLS]──> `headers.AddCookieHeaders (External/BCL)`
  • - [移除呼叫邊] `RestClient.ExecuteRequestAsync` ──[CALLS]──> `cookieContainer.SetCookies (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RestClient.ExecuteAsync()`
- **變更前簽章 (Before)**: `RestClient.ExecuteAsync(RestRequest request, CancellationToken cancellationToken = default)` (L23~L39)
- **變更後簽章 (After)**: `RestClient.ExecuteAsync(RestRequest request, CancellationToken cancellationToken = default)` (L23~L39)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async Task<RestResponse> ExecuteAsync(RestRequest request, CancellationToken cancellationToken = default) {
        var internalResponse = await ExecuteRequestAsync(request, cancellationToken).ConfigureAwait(false);

        var response = internalResponse.Exception == null
            ? await RestResponse.FromHttpResponse(
                    internalResponse.ResponseMessage!,
                    request,
                    Options.Encoding,
                    internalResponse.CookieContainer?.GetCookies(internalResponse.Url),
                    Options.CalculateResponseStatus,
                    cancellationToken
                )
                .ConfigureAwait(false)
            : GetErrorResponse(request, internalResponse.Exception, internalResponse.TimeoutToken);

        return Options.ThrowOnAnyError ? response.ThrowIfError() : response;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async Task<RestResponse> ExecuteAsync(RestRequest request, CancellationToken cancellationToken = default) {
        using var internalResponse = await ExecuteRequestAsync(request, cancellationToken).ConfigureAwait(false);

        var response = internalResponse.Exception == null
            ? await RestResponse.FromHttpResponse(
                    internalResponse.ResponseMessage!,
                    request,
                    Options.Encoding,
                    internalResponse.CookieContainer?.GetCookies(internalResponse.Url),
                    Options.CalculateResponseStatus,
                    cancellationToken
                )
                .ConfigureAwait(false)
            : GetErrorResponse(request, internalResponse.Exception, internalResponse.TimeoutToken);

        return Options.ThrowOnAnyError ? response.ThrowIfError() : response;
    }
```

### 🔹 函式: `RestClient.ExecuteRequestAsync()`
- **變更前簽章 (Before)**: `RestClient.ExecuteRequestAsync(RestRequest request, CancellationToken cancellationToken)` (L73~L136)
- **變更後簽章 (After)**: `RestClient.ExecuteRequestAsync(RestRequest request, CancellationToken cancellationToken)` (L73~L130)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async Task<HttpResponse> ExecuteRequestAsync(RestRequest request, CancellationToken cancellationToken) {
        Ensure.NotNull(request, nameof(request));

        // Make sure we are not disposed of when someone tries to call us!
        if (_disposed) {
            throw new ObjectDisposedException(nameof(RestClient));
        }

        using var requestContent = new RequestContent(this, request);

        var authenticator = request.Authenticator ?? Options.Authenticator;
        if (authenticator != null) await authenticator.Authenticate(this, request).ConfigureAwait(false);

        var httpMethod = AsHttpMethod(request.Method);
        var url        = this.BuildUri(request);
        var message    = new HttpRequestMessage(httpMethod, url) { Content = requestContent.BuildContent() };
        message.Headers.Host         = Options.BaseHost;
        message.Headers.CacheControl = request.CachePolicy ?? Options.CachePolicy;

        using var timeoutCts = new CancellationTokenSource(request.Timeout > 0 ? request.Timeout : int.MaxValue);
        using var cts        = CancellationTokenSource.CreateLinkedTokenSource(timeoutCts.Token, cancellationToken);

        var ct = cts.Token;

        try {
            // Make sure we have a cookie container if not provided in the request
            var cookieContainer = request.CookieContainer ??= new CookieContainer();

            var headers = new RequestHeaders()
                .AddHeaders(request.Parameters)
                .AddHeaders(DefaultParameters)
                .AddAcceptHeader(AcceptedContentTypes)
                .AddCookieHeaders(cookieContainer, url);

            if (Options.CookieContainer != null) {
                headers.AddCookieHeaders(Options.CookieContainer, url);
            }

            message.AddHeaders(headers);

            if (request.OnBeforeRequest != null) await request.OnBeforeRequest(message).ConfigureAwait(false);

            var responseMessage = await HttpClient.SendAsync(message, request.CompletionOption, ct).ConfigureAwait(false);

            // Parse all the cookies from the response and update the cookie jar with cookies
            if (responseMessage.Headers.TryGetValues(KnownHeaders.SetCookie, out var cookiesHeader)) {
                foreach (var header in cookiesHeader) {
                    try {
                        cookieContainer.SetCookies(url, header);
                    }
                    catch (CookieException) {
                        // Do not fail request if we cannot parse a cookie
                    }
                }
            }

            if (request.OnAfterRequest != null) await request.OnAfterRequest(responseMessage).ConfigureAwait(false);

            return new HttpResponse(responseMessage, url, cookieContainer, null, timeoutCts.Token);
        }
        catch (Exception ex) {
            return new HttpResponse(null, url, null, ex, timeoutCts.Token);
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async Task<HttpResponse> ExecuteRequestAsync(RestRequest request, CancellationToken cancellationToken) {
        Ensure.NotNull(request, nameof(request));

        // Make sure we are not disposed of when someone tries to call us!
        if (_disposed) {
            throw new ObjectDisposedException(nameof(RestClient));
        }

        using var requestContent = new RequestContent(this, request);

        var authenticator = request.Authenticator ?? Options.Authenticator;
        if (authenticator != null) await authenticator.Authenticate(this, request).ConfigureAwait(false);

        var httpMethod = AsHttpMethod(request.Method);
        var url        = this.BuildUri(request);

        using var message    = new HttpRequestMessage(httpMethod, url) { Content = requestContent.BuildContent() };
        message.Headers.Host         = Options.BaseHost;
        message.Headers.CacheControl = request.CachePolicy ?? Options.CachePolicy;

        using var timeoutCts = new CancellationTokenSource(request.Timeout > 0 ? request.Timeout : int.MaxValue);
        using var cts        = CancellationTokenSource.CreateLinkedTokenSource(timeoutCts.Token, cancellationToken);

        var ct = cts.Token;

        try {
            // Make sure we have a cookie container if not provided in the request
            var cookieContainer = request.CookieContainer ??= new CookieContainer();

            var headers = new RequestHeaders()
                .AddHeaders(request.Parameters)
                .AddHeaders(DefaultParameters)
                .AddAcceptHeader(AcceptedContentTypes)
                .AddCookieHeaders(url, cookieContainer)
                .AddCookieHeaders(url, Options.CookieContainer);

            message.AddHeaders(headers);

            if (request.OnBeforeRequest != null) await request.OnBeforeRequest(message).ConfigureAwait(false);

            var responseMessage = await HttpClient.SendAsync(message, request.CompletionOption, ct).ConfigureAwait(false);

            // Parse all the cookies from the response and update the cookie jar with cookies
            if (responseMessage.Headers.TryGetValues(KnownHeaders.SetCookie, out var cookiesHeader)) {
                // ReSharper disable once PossibleMultipleEnumeration
                cookieContainer.AddCookies(url, cookiesHeader);
                // ReSharper disable once PossibleMultipleEnumeration
                Options.CookieContainer?.AddCookies(url, cookiesHeader);
            }

            if (request.OnAfterRequest != null) await request.OnAfterRequest(responseMessage).ConfigureAwait(false);

            return new HttpResponse(responseMessage, url, cookieContainer, null, timeoutCts.Token);
        }
        catch (Exception ex) {
            return new HttpResponse(null, url, null, ex, timeoutCts.Token);
        }
    }
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/RestSharp show 2370d2ef453f64bd10da9ab7a924e92e8b667978
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 2370d2ef453f64bd10da9ab7a924e92e8b667978~1 --file test_repos/RestSharp/src/RestSharp/Request/PropertyCache.Populator.cs
   ```
