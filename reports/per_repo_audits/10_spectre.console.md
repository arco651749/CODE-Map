# 🔬 CODE-Map 基準審查獨立驗證報告: `spectre.console`
> **技術生態**: `C# (.NET Console / 旗艦 TUI 渲染)`  
> **本地倉庫路徑**: `test_repos/spectre.console`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 30 Files  
> **報告生成時間**: 2026-10-20 21:41:15  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `25` / `30` | `83.3%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `5` / `30` | `16.7%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `0` / `30` | `0.0%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`30` / `30`** | **`100.0%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `30` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `a5d49bc8`
- **完整 Hash**: `a5d49bc822ea4e01efa9596782a054bf347b7ad6`
- **說明 (Ground Truth)**: Fix initial selection when no default value is set
- **變更檔案數**: 2

#### 📄 檔案: `src/Spectre.Console/Prompts/MultiSelectionPrompt.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:43, E:36, A:0) ➔ After(N:45, E:36, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_10` (MODULE_STATE)
  • + [新增節點] `state_11` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `MultiSelectionPrompt.CalculateInitialIndex()`
- **變更前簽章 (Before)**: `MultiSelectionPrompt.CalculateInitialIndex(IReadOnlyList<ListPromptItem<T>> nodes)` (L304~L312)
- **變更後簽章 (After)**: `MultiSelectionPrompt.CalculateInitialIndex(IReadOnlyList<ListPromptItem<T>> nodes)` (L317~L325)

#### ◀️ 變更前實作碼 (Before Implementation):
```
int IListPromptStrategy<T>.CalculateInitialIndex(IReadOnlyList<ListPromptItem<T>> nodes)
    {
        if (DefaultValue is not null)
        {
            return Tree.IndexOf(DefaultValue) ?? 0;
        }

        return 0;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
int IListPromptStrategy<T>.CalculateInitialIndex(IReadOnlyList<ListPromptItem<T>> nodes)
    {
        if (_hasDefaultValue && DefaultValue is not null)
        {
            return Tree.IndexOf(DefaultValue) ?? 0;
        }

        return 0;
    }
```


#### 📄 檔案: `src/Spectre.Console/Prompts/SelectionPrompt.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:27, E:20, A:0) ➔ After(N:29, E:20, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_12` (MODULE_STATE)
  • + [新增節點] `state_11` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SelectionPrompt.CalculateInitialIndex()`
- **變更前簽章 (Before)**: `SelectionPrompt.CalculateInitialIndex(IReadOnlyList<ListPromptItem<T>> nodes)` (L258~L266)
- **變更後簽章 (After)**: `SelectionPrompt.CalculateInitialIndex(IReadOnlyList<ListPromptItem<T>> nodes)` (L270~L278)

#### ◀️ 變更前實作碼 (Before Implementation):
```
int IListPromptStrategy<T>.CalculateInitialIndex(IReadOnlyList<ListPromptItem<T>> nodes)
    {
        if (DefaultValue is not null)
        {
            return _tree.IndexOf(DefaultValue) ?? 0;
        }

        return 0;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
int IListPromptStrategy<T>.CalculateInitialIndex(IReadOnlyList<ListPromptItem<T>> nodes)
    {
        if (_hasDefaultValue && DefaultValue is not null)
        {
            return _tree.IndexOf(DefaultValue) ?? 0;
        }

        return 0;
    }
```


---

### 🔹 Commit #02: `a5a6cba0`
- **完整 Hash**: `a5a6cba089b0d87c390c48f1694789e49754888f`
- **說明 (Ground Truth)**: fix(generator): ignore static or invalid spinners in source generator
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console.SourceGenerator/Spinners/SpinnerGenerator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:19, E:17, A:0) ➔ After(N:24, E:21, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 0, +Edges: 4, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `string.Equals (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `parsedSpinners
                    .Where(IsValidSpinner)
                    .ToArray (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `SpinnerGenerator.IsValidSpinner` (FUNCTION_DEF)
  • + [新增節點] `parsedSpinners
                    .Where (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `spinner.Frames.Any (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `SpinnerGenerator.Initialize` ──[CALLS]──> `parsedSpinners
                    .Where(IsValidSpinner)
                    .ToArray (External/BCL)`
  • + [新增呼叫邊] `SpinnerGenerator.Initialize` ──[CALLS]──> `parsedSpinners
                    .Where (External/BCL)`
  • + [新增呼叫邊] `SpinnerGenerator.IsValidSpinner` ──[CALLS]──> `spinner.Frames.Any (External/BCL)`
  • + [新增呼叫邊] `SpinnerGenerator.IsValidSpinner` ──[CALLS]──> `string.Equals (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SpinnerGenerator.Initialize()`
- **變更前簽章 (Before)**: `SpinnerGenerator.Initialize(IncrementalGeneratorInitializationContext context)` (L19~L66)
- **變更後簽章 (After)**: `SpinnerGenerator.Initialize(IncrementalGeneratorInitializationContext context)` (L20~L71)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public void Initialize(IncrementalGeneratorInitializationContext context)
    {
        // Find spinners_default.json
        // Step 1: Extract text (cached by string value equality)
        // Step 2: Wrap in EquatableArray for value equality when combining
        var defaultSpinners = context.AdditionalTextsProvider
            .Where(static file => file.Path.EndsWith("spinners_default.json", StringComparison.OrdinalIgnoreCase))
            .Select(static (file, ct) =>
                file.GetText(ct)?.ToString()
                ?? throw new InvalidOperationException($"Failed to read spinners_default.json at {file.Path}"))
            .Collect()
            .Select(static (arr, _) => new EquatableArray<string>(arr));

        // Find spinners_sindresorhus.json
        var sindreSpinners = context.AdditionalTextsProvider
            .Where(static file => file.Path.EndsWith("spinners_sindresorhus.json", StringComparison.OrdinalIgnoreCase))
            .Select(static (file, ct) =>
                file.GetText(ct)?.ToString()
                ?? throw new InvalidOperationException($"Failed to read spinners_sindresorhus.json at {file.Path}"))
            .Collect()
            .Select(static (arr, _) => new EquatableArray<string>(arr));

        // Combine both JSON files and parse in the pipeline (for caching)
        // EquatableArray has value equality, so this step is properly cached
        var spinners = defaultSpinners.Combine(sindreSpinners)
            .Select(static (data, _) =>
            {
                var (defaultJsonFiles, sindreJsonFiles) = data;
                if (defaultJsonFiles.IsEmpty || sindreJsonFiles.IsEmpty)
                {
                    return EquatableArray<SpinnerModel>.Empty;
                }

                return SpinnerParser.ParseAll(defaultJsonFiles[0], sindreJsonFiles[0]);
            });

        // Register source output - only emit, no parsing (parsing is cached above)
        context.RegisterSourceOutput(spinners, static (spc, models) =>
        {
            if (models.IsEmpty)
            {
                return;
            }

            var source = SpinnerEmitter.Emit(models);
            spc.AddSource("Spinner.Generated.g.cs", SourceText.From(source, Utf8NoBom));
        });
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public void Initialize(IncrementalGeneratorInitializationContext context)
    {
        // Find spinners_default.json
        // Step 1: Extract text (cached by string value equality)
        // Step 2: Wrap in EquatableArray for value equality when combining
        var defaultSpinners = context.AdditionalTextsProvider
            .Where(static file => file.Path.EndsWith("spinners_default.json", StringComparison.OrdinalIgnoreCase))
            .Select(static (file, ct) =>
                file.GetText(ct)?.ToString()
                ?? throw new InvalidOperationException($"Failed to read spinners_default.json at {file.Path}"))
            .Collect()
            .Select(static (arr, _) => new EquatableArray<string>(arr));

        // Find spinners_sindresorhus.json
        var sindreSpinners = context.AdditionalTextsProvider
            .Where(static file => file.Path.EndsWith("spinners_sindresorhus.json", StringComparison.OrdinalIgnoreCase))
            .Select(static (file, ct) =>
                file.GetText(ct)?.ToString()
                ?? throw new InvalidOperationException($"Failed to read spinners_sindresorhus.json at {file.Path}"))
            .Collect()
            .Select(static (arr, _) => new EquatableArray<string>(arr));

        // Combine both JSON files and parse in the pipeline (for caching)
        // EquatableArray has value equality, so this step is properly cached
        var spinners = defaultSpinners.Combine(sindreSpinners)
            .Select(static (data, _) =>
            {
                var (defaultJsonFiles, sindreJsonFiles) = data;
                if (defaultJsonFiles.IsEmpty || sindreJsonFiles.IsEmpty)
                {
                    return EquatableArray<SpinnerModel>.Empty;
                }

                var parsedSpinners = SpinnerParser.ParseAll(defaultJsonFiles[0], sindreJsonFiles[0]);
                var validSpinners = parsedSpinners
                    .Where(IsValidSpinner)
                    .ToArray();

                return new EquatableArray<SpinnerModel>(validSpinners);
            });

        context.RegisterSourceOutput(spinners, static (spc, models) =>
        {
            if (models.IsEmpty)
            {
                return;
            }

            var source = SpinnerEmitter.Emit(models);
            spc.AddSource("Spinner.Generated.g.cs", SourceText.From(source, Utf8NoBom));
        });
    }
```


---

### 🔹 Commit #03: `3ba10230`
- **完整 Hash**: `3ba1023095399bb6a50d4f9f2f194d3d4d28187e`
- **說明 (Ground Truth)**: Fix infinite loop in TableMeasurer.CollapseWidths when wrappable columns have zero width (#2132)
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console/Widgets/Table/TableMeasurer.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:49, E:50, A:0) ➔ After(N:49, E:50, A:0)
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
  • + [新增節點] `widths.Zip(wrappable, (width, allowWrap) => allowWrap && width != maxColumn ? width : 0).Max (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `widths.Zip(wrappable, (width, allowWrap) => allowWrap && width != maxColumn ? width : 1).Max (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `TableMeasurer.CollapseWidths` ──[CALLS]──> `widths.Zip(wrappable, (width, allowWrap) => allowWrap && width != maxColumn ? width : 0).Max (External/BCL)`
  • - [移除呼叫邊] `TableMeasurer.CollapseWidths` ──[CALLS]──> `widths.Zip(wrappable, (width, allowWrap) => allowWrap && width != maxColumn ? width : 1).Max (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TableMeasurer.CollapseWidths()`
- **變更前簽章 (Before)**: `TableMeasurer.CollapseWidths(List<int> widths, List<bool> wrappable, int maxWidth)` (L173~L204)
- **變更後簽章 (After)**: `TableMeasurer.CollapseWidths(List<int> widths, List<bool> wrappable, int maxWidth)` (L173~L204)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private static List<int> CollapseWidths(List<int> widths, List<bool> wrappable, int maxWidth)
    {
        var totalWidth = widths.Sum();
        var excessWidth = totalWidth - maxWidth;

        if (wrappable.AnyTrue())
        {
            while (totalWidth != 0 && excessWidth > 0)
            {
                var maxColumn = widths.Zip(wrappable, (first, second) => (width: first, allowWrap: second))
                    .Where(x => x.allowWrap)
                    .Max(x => x.width);

                var secondMaxColumn = widths.Zip(wrappable, (width, allowWrap) => allowWrap && width != maxColumn ? width : 1).Max();
                var columnDifference = maxColumn - secondMaxColumn;

                var ratios = widths.Zip(wrappable, (width, allowWrap) => width == maxColumn && allowWrap ? 1 : 0).ToList();
                if (!ratios.Any(x => x != 0) || columnDifference == 0)
                {
                    break;
                }

                var maxReduce = widths.Select(_ => Math.Min(excessWidth, columnDifference)).ToList();
                widths = Ratio.Reduce(excessWidth, ratios, maxReduce, widths);

                totalWidth = widths.Sum();
                excessWidth = totalWidth - maxWidth;
            }
        }

        return widths;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private static List<int> CollapseWidths(List<int> widths, List<bool> wrappable, int maxWidth)
    {
        var totalWidth = widths.Sum();
        var excessWidth = totalWidth - maxWidth;

        if (wrappable.AnyTrue())
        {
            while (totalWidth != 0 && excessWidth > 0)
            {
                var maxColumn = widths.Zip(wrappable, (first, second) => (width: first, allowWrap: second))
                    .Where(x => x.allowWrap)
                    .Max(x => x.width);

                var secondMaxColumn = widths.Zip(wrappable, (width, allowWrap) => allowWrap && width != maxColumn ? width : 0).Max();
                var columnDifference = maxColumn - secondMaxColumn;

                var ratios = widths.Zip(wrappable, (width, allowWrap) => width == maxColumn && allowWrap ? 1 : 0).ToList();
                if (!ratios.Any(x => x != 0) || columnDifference <= 0)
                {
                    break;
                }

                var maxReduce = widths.Select(_ => Math.Min(excessWidth, columnDifference)).ToList();
                widths = Ratio.Reduce(excessWidth, ratios, maxReduce, widths);

                totalWidth = widths.Sum();
                excessWidth = totalWidth - maxWidth;
            }
        }

        return widths;
    }
```


---

### 🔹 Commit #04: `a0913f86`
- **完整 Hash**: `a0913f8628344e429e3994a020c3f791347436b1`
- **說明 (Ground Truth)**: (GH-2153) Fix async stack traces rendering as MoveNext() instead of source methods
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console/Widgets/Exceptions/ExceptionRenderableBuilder.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:64, E:75, A:0) ➔ After(N:64, E:75, A:0)
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

### 🔹 函式: `ExceptionRenderableBuilder.GetMethodName()`
- **變更前簽章 (Before)**: `ExceptionRenderableBuilder.GetMethodName(ExceptionInfoResolver resolver, ref MethodBase method, out bool isAsync)` (L286~L304)
- **變更後簽章 (After)**: `ExceptionRenderableBuilder.GetMethodName(ExceptionInfoResolver resolver, ref MethodBase method, out bool isAsync)` (L286~L304)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private static string GetMethodName(ExceptionInfoResolver resolver, ref MethodBase method, out bool isAsync)
    {
        var declaringType = method.DeclaringType;

        if (declaringType?.IsDefined(typeof(CompilerGeneratedAttribute), false) == true)
        {
            isAsync = typeof(IAsyncStateMachine).IsAssignableFrom(declaringType);
            if (isAsync || typeof(IEnumerator).IsAssignableFrom(declaringType))
            {
                TryResolveStateMachineMethod(method, out declaringType);
            }
        }
        else
        {
            isAsync = false;
        }

        return resolver.GetMethodName(method);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private static string GetMethodName(ExceptionInfoResolver resolver, ref MethodBase method, out bool isAsync)
    {
        var declaringType = method.DeclaringType;

        if (declaringType?.IsDefined(typeof(CompilerGeneratedAttribute), false) == true)
        {
            isAsync = typeof(IAsyncStateMachine).IsAssignableFrom(declaringType);
            if (isAsync || typeof(IEnumerator).IsAssignableFrom(declaringType))
            {
                TryResolveStateMachineMethod(ref method, out declaringType);
            }
        }
        else
        {
            isAsync = false;
        }

        return resolver.GetMethodName(method);
    }
```

### 🔹 函式: `ExceptionRenderableBuilder.TryResolveStateMachineMethod()`
- **變更前簽章 (Before)**: `ExceptionRenderableBuilder.TryResolveStateMachineMethod(MethodBase method, out Type declaringType)` (L306~L359)
- **變更後簽章 (After)**: `ExceptionRenderableBuilder.TryResolveStateMachineMethod(ref MethodBase method, out Type declaringType)` (L306~L359)

#### ◀️ 變更前實作碼 (Before Implementation):
```
[RequiresDynamicCode(ExceptionRenderableBuilder.AotWarning)]
    private static bool TryResolveStateMachineMethod(MethodBase method, out Type declaringType)
    {
        // https://github.com/dotnet/runtime/blob/v6.0.0/src/libraries/System.Private.CoreLib/src/System/Diagnostics/StackTrace.cs#L400-L455
        declaringType = method.DeclaringType ??
                        throw new ArgumentException("Method must have a declaring type.", nameof(method));

        var parentType = declaringType.DeclaringType;
        if (parentType == null)
        {
            return false;
        }

        static IEnumerable<MethodInfo> GetDeclaredMethods(IReflect type) => type.GetMethods(
            BindingFlags.Public |
            BindingFlags.NonPublic |
            BindingFlags.Static |
            BindingFlags.Instance |
            BindingFlags.DeclaredOnly);

        var methods = GetDeclaredMethods(parentType);

        foreach (var candidateMethod in methods)
        {
            var attributes = candidateMethod.GetCustomAttributes<StateMachineAttribute>(false);

            bool foundAttribute = false, foundIteratorAttribute = false;
            foreach (var asma in attributes)
            {
                if (asma.StateMachineType != declaringType)
                {
                    continue;
                }

                foundAttribute = true;
#if NET6_0_OR_GREATER
                foundIteratorAttribute |= asma is IteratorStateMachineAttribute or AsyncIteratorStateMachineAttribute;
#else
                foundIteratorAttribute |= asma is IteratorStateMachineAttribute;
#endif
            }

            if (!foundAttribute)
            {
                continue;
            }

            method = candidateMethod;
            declaringType = candidateMethod.DeclaringType!;
            return foundIteratorAttribute;
        }

        return false;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
[RequiresDynamicCode(ExceptionRenderableBuilder.AotWarning)]
    private static bool TryResolveStateMachineMethod(ref MethodBase method, out Type declaringType)
    {
        // https://github.com/dotnet/runtime/blob/v6.0.0/src/libraries/System.Private.CoreLib/src/System/Diagnostics/StackTrace.cs#L400-L455
        declaringType = method.DeclaringType ??
                        throw new ArgumentException("Method must have a declaring type.", nameof(method));

        var parentType = declaringType.DeclaringType;
        if (parentType == null)
        {
            return false;
        }

        static IEnumerable<MethodInfo> GetDeclaredMethods(IReflect type) => type.GetMethods(
            BindingFlags.Public |
            BindingFlags.NonPublic |
            BindingFlags.Static |
            BindingFlags.Instance |
            BindingFlags.DeclaredOnly);

        var methods = GetDeclaredMethods(parentType);

        foreach (var candidateMethod in methods)
        {
            var attributes = candidateMethod.GetCustomAttributes<StateMachineAttribute>(false);

            bool foundAttribute = false, foundIteratorAttribute = false;
            foreach (var asma in attributes)
            {
                if (asma.StateMachineType != declaringType)
                {
                    continue;
                }

                foundAttribute = true;
#if NET6_0_OR_GREATER
                foundIteratorAttribute |= asma is IteratorStateMachineAttribute or AsyncIteratorStateMachineAttribute;
#else
                foundIteratorAttribute |= asma is IteratorStateMachineAttribute;
#endif
            }

            if (!foundAttribute)
            {
                continue;
            }

            method = candidateMethod;
            declaringType = candidateMethod.DeclaringType!;
            return foundIteratorAttribute;
        }

        return false;
    }
```


---

### 🔹 Commit #05: `bbf51e4c`
- **完整 Hash**: `bbf51e4c2841dae4d574193a7a5695499d453f60`
- **說明 (Ground Truth)**: Fix grid regression where expansion did not work
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console/Widgets/Grid.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:23, E:21, A:0) ➔ After(N:23, E:21, A:0)
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

### 🔹 函式: `Grid.Build()`
- **變更前簽章 (Before)**: `Grid.Build()` (L103~L131)
- **變更後簽章 (After)**: `Grid.Build()` (L103~L132)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override IRenderable Build()
    {
        var table = new Table
        {
            Border = TableBorder.None,
            ShowHeaders = false,
            IsGrid = true,
            PadRightCell = _padRightCell,
            Width = Width,
        };

        foreach (var column in _columns)
        {
            table.AddColumn(new TableColumn(string.Empty)
            {
                Width = column.Width,
                NoWrap = column.NoWrap,
                Padding = column.Padding ?? new Padding(0, 0, 2, 0),
                Alignment = column.Alignment,
            });
        }

        foreach (var row in _rows)
        {
            table.AddRow(row);
        }

        return table;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override IRenderable Build()
    {
        var table = new Table
        {
            Expand = Expand,
            Border = TableBorder.None,
            ShowHeaders = false,
            IsGrid = true,
            PadRightCell = _padRightCell,
            Width = Width,
        };

        foreach (var column in _columns)
        {
            table.AddColumn(new TableColumn(string.Empty)
            {
                Width = column.Width,
                NoWrap = column.NoWrap,
                Padding = column.Padding ?? new Padding(0, 0, 2, 0),
                Alignment = column.Alignment,
            });
        }

        foreach (var row in _rows)
        {
            table.AddRow(row);
        }

        return table;
    }
```


---

### 🔹 Commit #06: `a334da97`
- **完整 Hash**: `a334da97ce1e718cd2bac21aa8aaadd9d5d225e4`
- **說明 (Ground Truth)**: Fix escaping of interpolated arguments in markup
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console/Widgets/Markup.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:20, E:16, A:0) ➔ After(N:21, E:18, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 3, +Edges: 5, -Edges: 3, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `value.GetArguments()
            .Select (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `arg.ToString (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `value.GetArguments()
            .Select(arg => arg switch
            {
                null => null,
                string text => text.EscapeMarkup(),
                IFormattable => arg,
                _ => arg.ToString()?.EscapeMarkup(),
            })
            .ToArray (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `arg.ToString()?.EscapeMarkup (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `value.GetArguments().Select (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `s.EscapeMarkup (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `value.GetArguments().Select(arg => arg is string s ? s.EscapeMarkup() : arg).ToArray (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Markup.EscapeInterpolated` ──[CALLS]──> `value.GetArguments()
            .Select(arg => arg switch
            {
                null => null,
                string text => text.EscapeMarkup(),
                IFormattable => arg,
                _ => arg.ToString()?.EscapeMarkup(),
            })
            .ToArray (External/BCL)`
  • + [新增呼叫邊] `Markup.EscapeInterpolated` ──[CALLS]──> `value.GetArguments()
            .Select (External/BCL)`
  • + [新增呼叫邊] `Markup.EscapeInterpolated` ──[CALLS]──> `text.EscapeMarkup (External/BCL)`
  • + [新增呼叫邊] `Markup.EscapeInterpolated` ──[CALLS]──> `arg.ToString()?.EscapeMarkup (External/BCL)`
  • + [新增呼叫邊] `Markup.EscapeInterpolated` ──[CALLS]──> `arg.ToString (External/BCL)`
  • - [移除呼叫邊] `Markup.EscapeInterpolated` ──[CALLS]──> `value.GetArguments().Select(arg => arg is string s ? s.EscapeMarkup() : arg).ToArray (External/BCL)`
  • - [移除呼叫邊] `Markup.EscapeInterpolated` ──[CALLS]──> `value.GetArguments().Select (External/BCL)`
  • - [移除呼叫邊] `Markup.EscapeInterpolated` ──[CALLS]──> `s.EscapeMarkup (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Markup.EscapeInterpolated()`
- **變更前簽章 (Before)**: `Markup.EscapeInterpolated(IFormatProvider provider, FormattableString value)` (L108~L112)
- **變更後簽章 (After)**: `Markup.EscapeInterpolated(IFormatProvider provider, FormattableString value)` (L108~L120)

#### ◀️ 變更前實作碼 (Before Implementation):
```
internal static string EscapeInterpolated(IFormatProvider provider, FormattableString value)
    {
        object?[] args = value.GetArguments().Select(arg => arg is string s ? s.EscapeMarkup() : arg).ToArray();
        return string.Format(provider, value.Format, args);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal static string EscapeInterpolated(IFormatProvider provider, FormattableString value)
    {
        object?[] args = value.GetArguments()
            .Select(arg => arg switch
            {
                null => null,
                string text => text.EscapeMarkup(),
                IFormattable => arg,
                _ => arg.ToString()?.EscapeMarkup(),
            })
            .ToArray();
        return string.Format(provider, value.Format, args);
    }
```


---

### 🔹 Commit #07: `2bbdf1ca`
- **完整 Hash**: `2bbdf1ca7ca198a719606382898575ccde849beb`
- **說明 (Ground Truth)**: Fix various bugs, add Figlet font report
- **變更檔案數**: 3

#### 📄 檔案: `src/Spectre.Console/Widgets/Figlet/FigletCharacter.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:4, E:3, A:0) ➔ After(N:4, E:3, A:0)
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

### 🔹 函式: `FigletCharacter.FigletCharacter()`
- **變更前簽章 (Before)**: `FigletCharacter.FigletCharacter(int code, IEnumerable<string> lines)` (L10~L24)
- **變更後簽章 (After)**: `FigletCharacter.FigletCharacter(int code, IEnumerable<string> lines)` (L10~L20)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public FigletCharacter(int code, IEnumerable<string> lines)
    {
        Code = code;
        Lines = new List<string>(lines ?? throw new ArgumentNullException(nameof(lines)));

        var min = Lines.Min(x => x.Length);
        var max = Lines.Max(x => x.Length);
        if (min != max)
        {
            throw new InvalidOperationException($"Figlet character #{code} has varying width");
        }

        Width = max;
        Height = Lines.Count;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public FigletCharacter(int code, IEnumerable<string> lines)
    {
        Code = code;
        Lines = new List<string>(lines ?? throw new ArgumentNullException(nameof(lines)));

        var min = Lines.Min(x => x.Length);
        var max = Lines.Max(x => x.Length);

        Width = max;
        Height = Lines.Count;
    }
```


#### 📄 檔案: `src/Spectre.Console/Widgets/Figlet/FigletFont.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:19, E:14, A:0) ➔ After(N:18, E:13, A:0)
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
  • - [移除節點] `_characters.TryAdd (External/BCL)` (FUNCTION_DEF)
  • - [移除呼叫邊] `FigletFont.FigletFont` ──[CALLS]──> `_characters.TryAdd (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FigletFont.FigletFont()`
- **變更前簽章 (Before)**: `FigletFont.FigletFont(IEnumerable<FigletCharacter> characters, FigletHeader header)` (L57~L88)
- **變更後簽章 (After)**: `FigletFont.FigletFont(IEnumerable<FigletCharacter> characters, FigletHeader header)` (L57~L85)

#### ◀️ 變更前實作碼 (Before Implementation):
```
internal FigletFont(IEnumerable<FigletCharacter> characters, FigletHeader header)
    {
        _characters = new Dictionary<int, FigletCharacter>();

        foreach (var character in characters)
        {
            if (!_characters.TryAdd(character.Code, character))
            {
                throw new InvalidOperationException("Character already exist");
            }
        }

        Height = header.Height;
        Baseline = header.Baseline;
        MaxWidth = header.MaxLength;
        Hardblank = header.Hardblank;

        // Bits 0–5 (values 1, 2, 4, 8, 16, 32) encode the six horizontal smushing rules.
        // A result of 0 means no specific rules are defined, i.e. use universal smushing.
        if (header.FullLayout.HasValue)
        {
            SmushingRules = header.FullLayout.Value & 63;
        }
        else if (header.OldLayout > 0)
        {
            SmushingRules = header.OldLayout & 63;
        }
        else
        {
            SmushingRules = 0;
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal FigletFont(IEnumerable<FigletCharacter> characters, FigletHeader header)
    {
        _characters = new Dictionary<int, FigletCharacter>();

        foreach (var character in characters)
        {
            _characters[character.Code] = character;
        }

        Height = header.Height;
        Baseline = header.Baseline;
        MaxWidth = header.MaxLength;
        Hardblank = header.Hardblank;

        // Bits 0–5 (values 1, 2, 4, 8, 16, 32) encode the six horizontal smushing rules.
        // A result of 0 means no specific rules are defined, i.e. use universal smushing.
        if (header.FullLayout.HasValue)
        {
            SmushingRules = header.FullLayout.Value & 63;
        }
        else if (header.OldLayout > 0)
        {
            SmushingRules = header.OldLayout & 63;
        }
        else
        {
            SmushingRules = 0;
        }
    }
```


#### 📄 檔案: `src/Spectre.Console/Widgets/Figlet/FigletFontParser.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:19, E:20, A:0) ➔ After(N:23, E:25, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 1, +Edges: 6, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `lines.Skip(header.CommentLines + 1).Take(1).FirstOrDefault (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `firstEndLine?.Trim().LastOrDefault (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `FigletFontParser.ParseEndOfLineMarker` (FUNCTION_DEF)
  • + [新增節點] `lines.Skip(header.CommentLines + 1).Take (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `firstEndLine?.Trim (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `index.ReplaceExact("0x", string.Empty).ReplaceExact (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `FigletFontParser.Parse` ──[CALLS]──> `FigletFontParser.ParseEndOfLineMarker`
  • + [新增呼叫邊] `FigletFontParser.ParseEndOfLineMarker` ──[CALLS]──> `lines.Skip(header.CommentLines + 1).Take(1).FirstOrDefault (External/BCL)`
  • + [新增呼叫邊] `FigletFontParser.ParseEndOfLineMarker` ──[CALLS]──> `lines.Skip(header.CommentLines + 1).Take (External/BCL)`
  • + [新增呼叫邊] `FigletFontParser.ParseEndOfLineMarker` ──[CALLS]──> `lines.Skip (External/BCL)`
  • + [新增呼叫邊] `FigletFontParser.ParseEndOfLineMarker` ──[CALLS]──> `firstEndLine?.Trim().LastOrDefault (External/BCL)`
  • + [新增呼叫邊] `FigletFontParser.ParseEndOfLineMarker` ──[CALLS]──> `firstEndLine?.Trim (External/BCL)`
  • - [移除呼叫邊] `FigletFontParser.TryParseIndex` ──[CALLS]──> `index.ReplaceExact("0x", string.Empty).ReplaceExact (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FigletFontParser.TryParseIndex()`
- **變更前簽章 (Before)**: `FigletFontParser.TryParseIndex(string index, out int result)` (L65~L75)
- **變更後簽章 (After)**: `FigletFontParser.TryParseIndex(string index, out int result)` (L85~L95)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private static bool TryParseIndex(string index, out int result)
    {
        var style = NumberStyles.Integer;
        if (index.StartsWith("0x", StringComparison.OrdinalIgnoreCase))
        {
            index = index.ReplaceExact("0x", string.Empty).ReplaceExact("0x", string.Empty);
            style = NumberStyles.HexNumber;
        }

        return int.TryParse(index, style, CultureInfo.InvariantCulture, out result);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private static bool TryParseIndex(string index, out int result)
    {
        var style = NumberStyles.Integer;
        if (index.StartsWith("0x", StringComparison.OrdinalIgnoreCase))
        {
            index = index.ReplaceExact("0x", string.Empty);
            style = NumberStyles.HexNumber;
        }

        return int.TryParse(index, style, CultureInfo.InvariantCulture, out result);
    }
```

### 🔹 函式: `FigletFontParser.Parse()`
- **變更前簽章 (Before)**: `FigletFontParser.Parse(string source)` (L5~L63)
- **變更後簽章 (After)**: `FigletFontParser.Parse(string source)` (L5~L70)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static FigletFont Parse(string source)
    {
        var lines = source.SplitLines();

        var headerLine = lines.FirstOrDefault();
        if (headerLine == null)
        {
            throw new InvalidOperationException("Could not read header line");
        }

        var header = ParseHeader(headerLine);

        var index = 32;
        var indexOverridden = false;
        var hasOverriddenIndex = false;
        var buffer = new List<string>();
        var characters = new List<FigletCharacter>();

        foreach (var line in lines.Skip(header.CommentLines + 1))
        {
            if (!line.EndsWith("@", StringComparison.Ordinal))
            {
                var words = line.SplitWords();
                if (words.Length > 0 && TryParseIndex(words[0], out var newIndex))
                {
                    index = newIndex;
                    indexOverridden = true;
                    hasOverriddenIndex = true;
                    continue;
                }

                continue;
            }

            if (hasOverriddenIndex && !indexOverridden)
            {
                continue;
            }

            buffer.Add(line.TrimEnd('@'));

            if (line.EndsWith("@@", StringComparison.Ordinal))
            {
                characters.Add(new FigletCharacter(index, buffer));
                buffer.Clear();

                if (!hasOverriddenIndex)
                {
                    index++;
                }

                // Reset the flag so we know if we're trying to parse
                // a character that wasn't prefixed with an ASCII index.
                indexOverridden = false;
            }
        }

        return new FigletFont(characters, header);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static FigletFont Parse(string source)
    {
        var lines = source.SplitLines();

        var headerLine = lines.FirstOrDefault();
        if (headerLine == null)
        {
            throw new InvalidOperationException("Could not read header line");
        }

        var header = ParseHeader(headerLine);

        var index = 32;
        var indexOverridden = false;
        var hasOverriddenIndex = false;
        var buffer = new List<string>();
        var characters = new List<FigletCharacter>();
        var accumulatedHeight = 0;

        var eolMarker = ParseEndOfLineMarker(lines, header);

        foreach (var line in lines.Skip(header.CommentLines + 1))
        {
            // This might be an index?
            if (!line.EndsWith(eolMarker))
            {
                var words = line.SplitWords();
                if (words.Length > 0 && TryParseIndex(words[0], out var newIndex))
                {
                    index = newIndex;
                    indexOverridden = true;
                    hasOverriddenIndex = true;
                    accumulatedHeight = 0;
                    continue;
                }
            }

            if (hasOverriddenIndex && !indexOverridden)
            {
                continue;
            }

            buffer.Add(line.TrimEnd(eolMarker));
            accumulatedHeight++;

            if (accumulatedHeight == header.Height)
            {
                characters.Add(new FigletCharacter(index, buffer));
                buffer.Clear();

                if (!hasOverriddenIndex)
                {
                    index++;
                }

                // Reset the flag so we know if we're trying to parse
                // a character that wasn't prefixed with an ASCII index.
                indexOverridden = false;

                // Reset the accumulated height
                accumulatedHeight = 0;
            }
        }

        return new FigletFont(characters, header);
    }
```


---

### 🔹 Commit #08: `2d51cb2e`
- **完整 Hash**: `2d51cb2eef8818343f03f23bf26e692ff935581a`
- **說明 (Ground Truth)**: Don't emit \e[0N for zero steps in any cursor movement (#2104)
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console.Ansi/AnsiWriter.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:76, E:95, A:0) ➔ After(N:76, E:95, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 8, ΔTrans: 0
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

### 🔹 函式: `AnsiWriter.CursorPreviousLine()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorPreviousLine(int lines = 1)` (L650~L653)
- **變更後簽章 (After)**: `AnsiWriter.CursorPreviousLine(int lines = 1)` (L685~L693)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorPreviousLine(int lines = 1)
    {
        return WriteCsi(lines, 'F');
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorPreviousLine(int lines = 1)
    {
        if (lines == 0)
        {
            return this;
        }

        return WriteCsi(lines, 'F');
    }
```

### 🔹 函式: `AnsiWriter.CursorDown()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorDown(int steps)` (L368~L371)
- **變更後簽章 (After)**: `AnsiWriter.CursorDown(int steps)` (L373~L381)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorDown(int steps)
    {
        return WriteCsi(steps, 'B');
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorDown(int steps)
    {
        if (steps == 0)
        {
            return this;
        }

        return WriteCsi(steps, 'B');
    }
```

### 🔹 函式: `AnsiWriter.CursorNextLine()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorNextLine(int lines = 1)` (L636~L639)
- **變更後簽章 (After)**: `AnsiWriter.CursorNextLine(int lines = 1)` (L666~L674)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorNextLine(int lines = 1)
    {
        return WriteCsi(lines, 'E');
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorNextLine(int lines = 1)
    {
        if (lines == 0)
        {
            return this;
        }

        return WriteCsi(lines, 'E');
    }
```

### 🔹 函式: `AnsiWriter.CursorUp()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorUp(int steps)` (L352~L355)
- **變更後簽章 (After)**: `AnsiWriter.CursorUp(int steps)` (L352~L360)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorUp(int steps)
    {
        return WriteCsi(steps, 'A');
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorUp(int steps)
    {
        if (steps == 0)
        {
            return this;
        }

        return WriteCsi(steps, 'A');
    }
```

### 🔹 函式: `AnsiWriter.CursorBackward()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorBackward(int steps)` (L428~L431)
- **變更後簽章 (After)**: `AnsiWriter.CursorBackward(int steps)` (L443~L451)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorBackward(int steps)
    {
        return WriteCsi(steps, 'D');
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorBackward(int steps)
    {
        if (steps == 0)
        {
            return this;
        }

        return WriteCsi(steps, 'D');
    }
```

### 🔹 函式: `AnsiWriter.CursorHorizontalTabulation()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorHorizontalTabulation(int tabs = 1)` (L622~L625)
- **變更後簽章 (After)**: `AnsiWriter.CursorHorizontalTabulation(int tabs = 1)` (L647~L655)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorHorizontalTabulation(int tabs = 1)
    {
        return WriteCsi(tabs, 'I');
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorHorizontalTabulation(int tabs = 1)
    {
        if (tabs == 0)
        {
            return this;
        }

        return WriteCsi(tabs, 'I');
    }
```

### 🔹 函式: `AnsiWriter.CursorForward()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorForward(int steps)` (L398~L401)
- **變更後簽章 (After)**: `AnsiWriter.CursorForward(int steps)` (L408~L416)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorForward(int steps)
    {
        return WriteCsi(steps, 'C');
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorForward(int steps)
    {
        if (steps == 0)
        {
            return this;
        }

        return WriteCsi(steps, 'C');
    }
```

### 🔹 函式: `AnsiWriter.CursorBackwardTabulation()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorBackwardTabulation(int tabs = 1)` (L608~L611)
- **變更後簽章 (After)**: `AnsiWriter.CursorBackwardTabulation(int tabs = 1)` (L628~L636)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorBackwardTabulation(int tabs = 1)
    {
        return WriteCsi(tabs, 'Z');
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorBackwardTabulation(int tabs = 1)
    {
        if (tabs == 0)
        {
            return this;
        }

        return WriteCsi(tabs, 'Z');
    }
```


---

### 🔹 Commit #09: `dbbed60c`
- **完整 Hash**: `dbbed60c76ad73d5961d4e4bab370e650ff5617f`
- **說明 (Ground Truth)**: Option to exclude vertical padding for live progress renderer (#2100)
- **變更檔案數**: 3

#### 📄 檔案: `src/Spectre.Console/Live/LiveRenderable.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:27, E:22, A:0) ➔ After(N:27, E:22, A:0)
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

### 🔹 函式: `LiveRenderable.PositionCursor()`
- **變更前簽章 (Before)**: `LiveRenderable.PositionCursor(RenderOptions options)` (L40~L69)
- **變更後簽章 (After)**: `LiveRenderable.PositionCursor(RenderOptions options)` (L40~L72)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public IRenderable PositionCursor(RenderOptions options)
    {
        lock (_lock)
        {
            if (_shape == null)
            {
                return ControlCode.Empty;
            }

            // Check if the size have been reduced
            if (_shape.Value.Height > options.ConsoleSize.Height || _shape.Value.Width > options.ConsoleSize.Width)
            {
                // Important reset shape, so the size can shrink
                _shape = null;
                return ControlCode.Create(options.Capabilities, w =>
                {
                    w.EraseInDisplay(2);
                    w.ClearScrollback();
                    w.CursorHome();
                });
            }

            var linesToMoveUp = _shape.Value.Height - 1;
            return ControlCode.Create(options.Capabilities, w =>
            {
                w.Write("\r"); // More efficient than CHA (CSI 1 G)?
                w.CursorUp(linesToMoveUp);
            });
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public IRenderable PositionCursor(RenderOptions options)
    {
        lock (_lock)
        {
            if (_shape == null)
            {
                return ControlCode.Empty;
            }

            // Check if the size have been reduced
            if (_shape.Value.Height > options.ConsoleSize.Height || _shape.Value.Width > options.ConsoleSize.Width)
            {
                // Important reset shape, so the size can shrink
                _shape = null;
                return ControlCode.Create(options.Capabilities, w =>
                {
                    w.EraseInDisplay(2);
                    w.ClearScrollback();
                    w.CursorHome();
                });
            }

            var linesToMoveUp = _shape.Value.Height - 1;
            return ControlCode.Create(options.Capabilities, w =>
            {
                w.Write("\r"); // More efficient than CHA (CSI 1 G)?
                if (linesToMoveUp > 0)
                {
                    w.CursorUp(linesToMoveUp);
                }
            });
        }
    }
```


#### 📄 檔案: `src/Spectre.Console/Live/Progress/Progress.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:32, E:31, A:0) ➔ After(N:35, E:34, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 3, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `ProgressExtensions.IncludeVerticalPadding` (FUNCTION_DEF)
  • + [新增節點] `ProgressExtensions.ExcludeVerticalPadding` (FUNCTION_DEF)
  • + [新增節點] `ProgressExtensions.ExcludeVerticalPadding` (FUNCTION_DEF)
  • + [新增呼叫邊] `ProgressExtensions.ExcludeVerticalPadding` ──[CALLS]──> `ArgumentNullException.ThrowIfNull (External/BCL)`
  • + [新增呼叫邊] `ProgressExtensions.ExcludeVerticalPadding` ──[CALLS]──> `ProgressExtensions.ExcludeVerticalPadding`
  • + [新增呼叫邊] `ProgressExtensions.IncludeVerticalPadding` ──[CALLS]──> `ProgressExtensions.ExcludeVerticalPadding`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Progress.CreateRenderer()`
- **變更前簽章 (Before)**: `Progress.CreateRenderer()` (L155~L169)
- **變更後簽章 (After)**: `Progress.CreateRenderer()` (L162~L176)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private ProgressRenderer CreateRenderer()
    {
        var caps = _console.Profile.Capabilities;
        var interactive = caps.Interactive && caps.Ansi;

        if (interactive)
        {
            var columns = new List<ProgressColumn>(Columns);
            return new DefaultProgressRenderer(_console, columns, RefreshRate, HideCompleted, RenderHook);
        }
        else
        {
            return FallbackRenderer ?? new FallbackProgressRenderer(_timeProvider);
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private ProgressRenderer CreateRenderer()
    {
        var caps = _console.Profile.Capabilities;
        var interactive = caps.Interactive && caps.Ansi;

        if (interactive)
        {
            var columns = new List<ProgressColumn>(Columns);
            return new DefaultProgressRenderer(_console, columns, RefreshRate, HideCompleted, ExcludeVerticalPadding, RenderHook);
        }
        else
        {
            return FallbackRenderer ?? new FallbackProgressRenderer(_timeProvider);
        }
    }
```


#### 📄 檔案: `src/Spectre.Console/Live/Progress/Renderers/DefaultProgressRenderer.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:37, E:24, A:0) ➔ After(N:38, E:24, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_13` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `state_11()`
- **變更前簽章 (Before)**: `[Module State] state_11` (L11~L11)
- **變更後簽章 (After)**: `[Module State] state_11` (L11~L11)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private readonly Func<IRenderable, IReadOnlyList<ProgressTask>, IRenderable> _renderHook;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private readonly bool _excludeVerticalPadding;
```

### 🔹 函式: `DefaultProgressRenderer.DefaultProgressRenderer()`
- **變更前簽章 (Before)**: `DefaultProgressRenderer.DefaultProgressRenderer(IAnsiConsole console, List<ProgressColumn> columns, TimeSpan refreshRate, bool hideCompleted, Func<IRenderable, IReadOnlyList<ProgressTask>, IRenderable> renderHook)` (L16~L28)
- **變更後簽章 (After)**: `DefaultProgressRenderer.DefaultProgressRenderer(IAnsiConsole console, List<ProgressColumn> columns, TimeSpan refreshRate, bool hideCompleted, bool excludeVerticalPadding, Func<IRenderable, IReadOnlyList<ProgressTask>, IRenderable> renderHook)` (L17~L30)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public DefaultProgressRenderer(IAnsiConsole console, List<ProgressColumn> columns, TimeSpan refreshRate, bool hideCompleted, Func<IRenderable, IReadOnlyList<ProgressTask>, IRenderable> renderHook)
    {
        _console = console ?? throw new ArgumentNullException(nameof(console));
        _columns = columns ?? throw new ArgumentNullException(nameof(columns));
        _live = new LiveRenderable(console);
        _lock = new();
        _stopwatch = new Stopwatch();
        _lastUpdate = TimeSpan.Zero;
        _hideCompleted = hideCompleted;
        _renderHook = renderHook;

        RefreshRate = refreshRate;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public DefaultProgressRenderer(IAnsiConsole console, List<ProgressColumn> columns, TimeSpan refreshRate, bool hideCompleted, bool excludeVerticalPadding, Func<IRenderable, IReadOnlyList<ProgressTask>, IRenderable> renderHook)
    {
        _console = console ?? throw new ArgumentNullException(nameof(console));
        _columns = columns ?? throw new ArgumentNullException(nameof(columns));
        _live = new LiveRenderable(console);
        _lock = new();
        _stopwatch = new Stopwatch();
        _lastUpdate = TimeSpan.Zero;
        _hideCompleted = hideCompleted;
        _excludeVerticalPadding = excludeVerticalPadding;
        _renderHook = renderHook;

        RefreshRate = refreshRate;
    }
```

### 🔹 函式: `DefaultProgressRenderer.Update()`
- **變更前簽章 (Before)**: `DefaultProgressRenderer.Update(ProgressContext context)` (L60~L115)
- **變更後簽章 (After)**: `DefaultProgressRenderer.Update(ProgressContext context)` (L62~L117)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public override void Update(ProgressContext context)
    {
        lock (_lock)
        {
            if (!_stopwatch.IsRunning)
            {
                _stopwatch.Start();
            }

            var renderContext = RenderOptions.Create(_console, _console.Profile.Capabilities);

            var delta = _stopwatch.Elapsed - _lastUpdate;
            _lastUpdate = _stopwatch.Elapsed;

            var grid = new Grid();
            for (var columnIndex = 0; columnIndex < _columns.Count; columnIndex++)
            {
                var column = new GridColumn().PadRight(1);

                var columnWidth = _columns[columnIndex].GetColumnWidth(renderContext);
                if (columnWidth != null)
                {
                    column.Width = columnWidth;
                }

                if (_columns[columnIndex].NoWrap)
                {
                    column.NoWrap();
                }

                // Last column?
                if (columnIndex == _columns.Count - 1)
                {
                    column.PadRight(0);
                }

                grid.AddColumn(column);
            }

            // Add rows
            var tasks = context.GetTasks();

            var layout = new Grid();
            layout.AddColumn();

            foreach (var task in tasks.Where(tsk => !((tsk.HideWhenCompleted ?? _hideCompleted) && tsk.IsFinished)))
            {
                var columns = _columns.Select(column => column.Render(renderContext, task, delta));
                grid.AddRow(columns.ToArray());
            }

            layout.AddRow(grid);

            _live.SetRenderable(new Padder(_renderHook(layout, tasks), new Padding(0, 1)));
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public override void Update(ProgressContext context)
    {
        lock (_lock)
        {
            if (!_stopwatch.IsRunning)
            {
                _stopwatch.Start();
            }

            var renderContext = RenderOptions.Create(_console, _console.Profile.Capabilities);

            var delta = _stopwatch.Elapsed - _lastUpdate;
            _lastUpdate = _stopwatch.Elapsed;

            var grid = new Grid();
            for (var columnIndex = 0; columnIndex < _columns.Count; columnIndex++)
            {
                var column = new GridColumn().PadRight(1);

                var columnWidth = _columns[columnIndex].GetColumnWidth(renderContext);
                if (columnWidth != null)
                {
                    column.Width = columnWidth;
                }

                if (_columns[columnIndex].NoWrap)
                {
                    column.NoWrap();
                }

                // Last column?
                if (columnIndex == _columns.Count - 1)
                {
                    column.PadRight(0);
                }

                grid.AddColumn(column);
            }

            // Add rows
            var tasks = context.GetTasks();

            var layout = new Grid();
            layout.AddColumn();

            foreach (var task in tasks.Where(tsk => !((tsk.HideWhenCompleted ?? _hideCompleted) && tsk.IsFinished)))
            {
                var columns = _columns.Select(column => column.Render(renderContext, task, delta));
                grid.AddRow(columns.ToArray());
            }

            layout.AddRow(grid);

            _live.SetRenderable(_excludeVerticalPadding ? _renderHook(layout, tasks) : new Padder(_renderHook(layout, tasks), new Padding(0, 1)));
        }
    }
```

### 🔹 函式: `state_12()`
- **變更前簽章 (Before)**: `[Module State] state_12` (L12~L12)
- **變更後簽章 (After)**: `[Module State] state_12` (L12~L12)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private TimeSpan _lastUpdate;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private readonly Func<IRenderable, IReadOnlyList<ProgressTask>, IRenderable> _renderHook;
```


---

### 🔹 Commit #10: `58429081`
- **完整 Hash**: `58429081d62d5a7a446dc33f22967037159c3b1b`
- **說明 (Ground Truth)**: Fix Align measure to respect explicitly set width (#2101)
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console/Widgets/Align.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:19, E:13, A:0) ➔ After(N:20, E:15, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Align.Measure` (FUNCTION_DEF)
  • + [新增呼叫邊] `Align.Measure` ──[CALLS]──> `Math.Min (External/BCL)`
  • + [新增呼叫邊] `Align.Measure` ──[CALLS]──> `Align.Measure`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #11: `9aeb9e70`
- **完整 Hash**: `9aeb9e7018758d75625d4026cbd83f106f34c033`
- **說明 (Ground Truth)**: Fix #1638: Add missing text prompt suffix
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console/Prompts/TextPrompt.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:42, E:44, A:0) ➔ After(N:46, E:48, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 4, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `char.IsLetterOrDigit (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `Markup.Remove(markup).TrimEnd (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `Markup.Remove (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `TextPrompt.ShouldAppendColon` (FUNCTION_DEF)
  • + [新增呼叫邊] `TextPrompt.WritePrompt` ──[CALLS]──> `TextPrompt.ShouldAppendColon`
  • + [新增呼叫邊] `TextPrompt.ShouldAppendColon` ──[CALLS]──> `Markup.Remove(markup).TrimEnd (External/BCL)`
  • + [新增呼叫邊] `TextPrompt.ShouldAppendColon` ──[CALLS]──> `Markup.Remove (External/BCL)`
  • + [新增呼叫邊] `TextPrompt.ShouldAppendColon` ──[CALLS]──> `char.IsLetterOrDigit (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TextPrompt.WritePrompt()`
- **變更前簽章 (Before)**: `TextPrompt.WritePrompt(IAnsiConsole console)` (L215~L253)
- **變更後簽章 (After)**: `TextPrompt.WritePrompt(IAnsiConsole console)` (L215~L253)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private void WritePrompt(IAnsiConsole console)
    {
        ArgumentNullException.ThrowIfNull(console);

        var builder = new StringBuilder();
        builder.Append(_prompt.TrimEnd());

        var appendSuffix = false;
        if (ShowChoices && Choices.Count > 0)
        {
            appendSuffix = true;
            var converter = Converter ?? TypeConverterHelper.ConvertToString;
            var choices = string.Join("/", Choices.Select(choice => converter(choice)));
            var choicesStyle = ChoicesStyle?.ToMarkup() ?? "blue";
            builder.AppendFormat(CultureInfo.InvariantCulture, " [{0}][[{1}]][/]", choicesStyle, choices);
        }

        if (ShowDefaultValue && DefaultValue != null)
        {
            appendSuffix = true;
            var converter = Converter ?? TypeConverterHelper.ConvertToString;
            var defaultValueStyle = DefaultValueStyle?.ToMarkup() ?? "green";
            var defaultValue = converter(DefaultValue.Value);

            builder.AppendFormat(
                CultureInfo.InvariantCulture,
                " [{0}]({1})[/]",
                defaultValueStyle,
                IsSecret ? defaultValue.Mask(Mask) : defaultValue);
        }

        var markup = builder.ToString().Trim();
        if (appendSuffix)
        {
            markup += ":";
        }

        console.Markup(markup + " ");
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private void WritePrompt(IAnsiConsole console)
    {
        ArgumentNullException.ThrowIfNull(console);

        var builder = new StringBuilder();
        builder.Append(_prompt.TrimEnd());

        var hasPromptDetails = false;
        if (ShowChoices && Choices.Count > 0)
        {
            hasPromptDetails = true;
            var converter = Converter ?? TypeConverterHelper.ConvertToString;
            var choices = string.Join("/", Choices.Select(choice => converter(choice)));
            var choicesStyle = ChoicesStyle?.ToMarkup() ?? "blue";
            builder.AppendFormat(CultureInfo.InvariantCulture, " [{0}][[{1}]][/]", choicesStyle, choices);
        }

        if (ShowDefaultValue && DefaultValue != null)
        {
            hasPromptDetails = true;
            var converter = Converter ?? TypeConverterHelper.ConvertToString;
            var defaultValueStyle = DefaultValueStyle?.ToMarkup() ?? "green";
            var defaultValue = converter(DefaultValue.Value);

            builder.AppendFormat(
                CultureInfo.InvariantCulture,
                " [{0}]({1})[/]",
                defaultValueStyle,
                IsSecret ? defaultValue.Mask(Mask) : defaultValue);
        }

        var markup = builder.ToString().Trim();
        if (ShouldAppendColon(markup, hasPromptDetails))
        {
            markup += ":";
        }

        console.Markup(markup + " ");
    }
```


---

### 🔹 Commit #12: `e997b0e1`
- **完整 Hash**: `e997b0e14c8e2846cd34c125061ecb91e8b2ad59`
- **說明 (Ground Truth)**: Fix links being incorrectly merged into subsequent markup blocks.
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console.Ansi/AnsiMarkup.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:37, E:39, A:1) ➔ After(N:40, E:42, A:1)
- **差分統計**: +Nodes: 6, -Nodes: 3, +Edges: 5, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#result[^1]** `(Button / UI Control)`
    └── ⚡ **Text()**

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `linkStack.Pop (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `Equals (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `styleStack.Push (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_234` (MODULE_STATE)
  • + [新增節點] `linkStack.Push (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `styleStack.Pop (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `stack.Pop (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `stack.Push (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `state_231` (MODULE_STATE)
  • + [新增呼叫邊] `AnsiMarkup.Parse` ──[CALLS]──> `linkStack.Push (External/BCL)`
  • + [新增呼叫邊] `AnsiMarkup.Parse` ──[CALLS]──> `styleStack.Push (External/BCL)`
  • + [新增呼叫邊] `AnsiMarkup.Parse` ──[CALLS]──> `styleStack.Pop (External/BCL)`
  • + [新增呼叫邊] `AnsiMarkup.Parse` ──[CALLS]──> `linkStack.Pop (External/BCL)`
  • + [新增呼叫邊] `AnsiMarkup.Parse` ──[CALLS]──> `Equals (External/BCL)`
  • - [移除呼叫邊] `AnsiMarkup.Parse` ──[CALLS]──> `stack.Push (External/BCL)`
  • _... 以及其餘 1 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `AnsiMarkup.Parse()`
- **變更前簽章 (Before)**: `AnsiMarkup.Parse(string markup, Style? style = null)` (L48~L107)
- **變更後簽章 (After)**: `AnsiMarkup.Parse(string markup, Style? style = null)` (L48~L110)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static IEnumerable<AnsiMarkupSegment> Parse(string markup, Style? style = null)
    {
        ArgumentNullException.ThrowIfNull(markup);

        style ??= Style.Plain;

        using var tokenizer = new MarkupTokenizer(markup);

        var result = new List<AnsiMarkupSegment>();
        var stack = new Stack<Style>();
        var link = default(Link?);

        while (tokenizer.MoveNext())
        {
            var token = tokenizer.Current;

            if (token.Kind == MarkupTokenKind.Open)
            {
                var parsed = AnsiMarkupTagParser.Parse(token.Value);
                link ??= parsed.Link;
                stack.Push(style.Value);
                style = style.Value.Combine(parsed.Style);
            }
            else if (token.Kind == MarkupTokenKind.Close)
            {
                if (stack.Count == 0)
                {
                    throw new InvalidOperationException(
                        $"Encountered closing tag when none was expected near position {token.Position}.");
                }

                style = stack.Pop();
            }
            else if (token.Kind == MarkupTokenKind.Text)
            {
                if (result.Count > 0 && result[^1].Style.Equals(style))
                {
                    // Merge segments
                    result[^1].Text += token.Value;
                }
                else
                {
                    result.Add(
                        new AnsiMarkupSegment(
                        token.Value, style.Value, link));
                }
            }
            else
            {
                throw new InvalidOperationException("Encountered unknown markup token.");
            }
        }

        if (stack.Count > 0)
        {
            throw new InvalidOperationException("Unbalanced markup stack. Did you forget to close a tag?");
        }

        return result;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static IEnumerable<AnsiMarkupSegment> Parse(string markup, Style? style = null)
    {
        ArgumentNullException.ThrowIfNull(markup);

        style ??= Style.Plain;

        using var tokenizer = new MarkupTokenizer(markup);

        var result = new List<AnsiMarkupSegment>();
        var styleStack = new Stack<Style>();
        var linkStack = new Stack<Link?>();
        var link = default(Link?);

        while (tokenizer.MoveNext())
        {
            var token = tokenizer.Current;

            if (token.Kind == MarkupTokenKind.Open)
            {
                var parsed = AnsiMarkupTagParser.Parse(token.Value);
                linkStack.Push(link);
                link = parsed.Link ?? link;
                styleStack.Push(style.Value);
                style = style.Value.Combine(parsed.Style);
            }
            else if (token.Kind == MarkupTokenKind.Close)
            {
                if (styleStack.Count == 0)
                {
                    throw new InvalidOperationException(
                        $"Encountered closing tag when none was expected near position {token.Position}.");
                }

                style = styleStack.Pop();
                link = linkStack.Pop();
            }
            else if (token.Kind == MarkupTokenKind.Text)
            {
                if (result.Count > 0 && result[^1].Style.Equals(style) && Equals(result[^1].Link, link))
                {
                    // Merge segments with same style and link
                    result[^1].Text += token.Value;
                }
                else
                {
                    result.Add(
                        new AnsiMarkupSegment(
                        token.Value, style.Value, link));
                }
            }
            else
            {
                throw new InvalidOperationException("Encountered unknown markup token.");
            }
        }

        if (styleStack.Count > 0)
        {
            throw new InvalidOperationException("Unbalanced markup stack. Did you forget to close a tag?");
        }

        return result;
    }
```


---

### 🔹 Commit #13: `efdfe055`
- **完整 Hash**: `efdfe055c10ef4a6b9ccc6c645ddb6dfd12c0c60`
- **說明 (Ground Truth)**: Fix markup link rendering regression
- **變更檔案數**: 2

#### 📄 檔案: `src/Spectre.Console.Ansi/Link.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:4, E:4, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 4, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Link.GetHashCode` (FUNCTION_DEF)
  • + [新增節點] `ReferenceEquals (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `Link.Equals` (FUNCTION_DEF)
  • + [新增節點] `Link.Equals` (FUNCTION_DEF)
  • + [新增呼叫邊] `Link.Equals` ──[CALLS]──> `ReferenceEquals (External/BCL)`
  • + [新增呼叫邊] `Link.Equals` ──[CALLS]──> `ReferenceEquals (External/BCL)`
  • + [新增呼叫邊] `Link.Equals` ──[CALLS]──> `Link.Equals`
  • + [新增呼叫邊] `Link.GetHashCode` ──[CALLS]──> `Link.GetHashCode`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `src/Spectre.Console/Rendering/Segment.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:61, E:75, A:0) ➔ After(N:63, E:77, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `SegmentBuilder.HasSameLink` (FUNCTION_DEF)
  • + [新增節點] `_originalSegment.Link?.Equals (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Segment.Merge` ──[CALLS]──> `SegmentBuilder.HasSameLink`
  • + [新增呼叫邊] `SegmentBuilder.HasSameLink` ──[CALLS]──> `_originalSegment.Link?.Equals (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Segment.Merge()`
- **變更前簽章 (Before)**: `Segment.Merge(IEnumerable<Segment> segments)` (L452~L488)
- **變更後簽章 (After)**: `Segment.Merge(IEnumerable<Segment> segments)` (L452~L488)

#### ◀️ 變更前實作碼 (Before Implementation):
```
internal static IEnumerable<Segment> Merge(IEnumerable<Segment> segments)
    {
        ArgumentNullException.ThrowIfNull(segments);

        var segmentBuilder = (SegmentBuilder?)null;
        foreach (var segment in segments)
        {
            if (segmentBuilder == null)
            {
                segmentBuilder = new SegmentBuilder(segment);
                continue;
            }

            // Both control codes?
            if (segment.IsControlCode && segmentBuilder.IsControlCode())
            {
                segmentBuilder.Append(segment.Text);
                continue;
            }

            // Same style?
            if (segmentBuilder.StyleEquals(segment.Style) && !segmentBuilder.IsLineBreak() &&
                !segmentBuilder.IsControlCode())
            {
                segmentBuilder.Append(segment.Text);
                continue;
            }

            yield return segmentBuilder.Build();
            segmentBuilder.Reset(segment);
        }

        if (segmentBuilder != null)
        {
            yield return segmentBuilder.Build();
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal static IEnumerable<Segment> Merge(IEnumerable<Segment> segments)
    {
        ArgumentNullException.ThrowIfNull(segments);

        var segmentBuilder = (SegmentBuilder?)null;
        foreach (var segment in segments)
        {
            if (segmentBuilder == null)
            {
                segmentBuilder = new SegmentBuilder(segment);
                continue;
            }

            // Both control codes?
            if (segment.IsControlCode && segmentBuilder.IsControlCode())
            {
                segmentBuilder.Append(segment.Text);
                continue;
            }

            // Same style and link?
            if (segmentBuilder.StyleEquals(segment.Style) && !segmentBuilder.IsLineBreak() &&
                !segmentBuilder.IsControlCode() && segmentBuilder.HasSameLink(segment.Link))
            {
                segmentBuilder.Append(segment.Text);
                continue;
            }

            yield return segmentBuilder.Build();
            segmentBuilder.Reset(segment);
        }

        if (segmentBuilder != null)
        {
            yield return segmentBuilder.Build();
        }
    }
```


---

### 🔹 Commit #14: `8ef7a116`
- **完整 Hash**: `8ef7a11609ecdaabedd86af4d52d0b33d40a587b`
- **說明 (Ground Truth)**: Add missing ANSI/VT sequences
- **變更檔案數**: 3

#### 📄 檔案: `src/Spectre.Console.Ansi/AnsiWriter.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:58, E:75, A:0) ➔ After(N:76, E:95, A:0)
- **差分統計**: +Nodes: 18, -Nodes: 0, +Edges: 23, -Edges: 3, ΔFuncs: 21, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `AnsiWriter.ReverseIndex` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.DeleteCharacter` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.InsertLine` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.ScrollDown` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.SetCursorStyle` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.CursorNextLine` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.DeleteLine` (FUNCTION_DEF)
  • + [新增節點] `string.IsNullOrWhiteSpace (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.Index` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.CursorBackward` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.EraseCharacter` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.CursorHorizontalTabulation` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.CursorForward` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.CursorPreviousLine` (FUNCTION_DEF)
  • + [新增節點] `AnsiWriter.ScrollUp` (FUNCTION_DEF)
  • _... 以及其餘 29 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `AnsiWriter.EraseInLine()`
- **變更前簽章 (Before)**: `AnsiWriter.EraseInLine(int mode = 0)` (L523~L527)
- **變更後簽章 (After)**: `AnsiWriter.EraseInLine(int mode = 0)` (L556~L559)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter EraseInLine(int mode = 0)
    {
        WriteCsi(mode, 'K');
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter EraseInLine(int mode = 0)
    {
        return WriteCsi(mode, 'K');
    }
```

### 🔹 函式: `AnsiWriter.CursorHorizontalAbsolute()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorHorizontalAbsolute(int position)` (L471~L475)
- **變更後簽章 (After)**: `AnsiWriter.CursorHorizontalAbsolute(int position)` (L507~L510)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorHorizontalAbsolute(int position)
    {
        WriteCsi(position, 'G');
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorHorizontalAbsolute(int position)
    {
        return WriteCsi(position, 'G');
    }
```

### 🔹 函式: `AnsiWriter.ShowCursor()`
- **變更前簽章 (Before)**: `AnsiWriter.ShowCursor()` (L416~L420)
- **變更後簽章 (After)**: `AnsiWriter.ShowCursor()` (L440~L443)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter ShowCursor()
    {
        WriteCsi(25, 'h', decPrivateMode: true);
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter ShowCursor()
    {
        return WriteCsi(25, 'h', decPrivateMode: true);
    }
```

### 🔹 函式: `AnsiWriter.SaveCursor()`
- **變更前簽章 (Before)**: `AnsiWriter.SaveCursor()` (L443~L447)
- **變更後簽章 (After)**: `AnsiWriter.SaveCursor(bool stayOnPage = true)` (L466~L476)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter SaveCursor()
    {
        WriteCsi("s");
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter SaveCursor(bool stayOnPage = true)
    {
        if (stayOnPage)
        {
            // SCOSC
            return WriteCsi("s");
        }

        // DECSC
        return WriteEsc("7");
    }
```

### 🔹 函式: `AnsiWriter.CursorDown()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorDown(int steps)` (L371~L375)
- **變更後簽章 (After)**: `AnsiWriter.CursorDown(int steps)` (L368~L371)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorDown(int steps)
    {
        WriteCsi(steps, 'B');
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorDown(int steps)
    {
        return WriteCsi(steps, 'B');
    }
```

### 🔹 函式: `AnsiWriter.WriteCsi()`
- **變更前簽章 (Before)**: `AnsiWriter.WriteCsi(string parameters, char terminator, bool decPrivateMode = false)` (L585~L588)
- **變更後簽章 (After)**: `AnsiWriter.WriteCsi(string parameters, char terminator, bool decPrivateMode = false)` (L845~L848)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private bool WriteCsi(string parameters, char terminator, bool decPrivateMode = false)
    {
        return WriteCsi($"{parameters}{terminator}");
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private AnsiWriter WriteCsi(string parameters, char terminator, bool decPrivateMode = false)
    {
        return WriteCsi($"{parameters}{terminator}", decPrivateMode);
    }
```

### 🔹 函式: `AnsiWriter.WriteCsi()`
- **變更前簽章 (Before)**: `AnsiWriter.WriteCsi(string parameters, bool decPrivateMode = false)` (L590~L599)
- **變更後簽章 (After)**: `AnsiWriter.WriteCsi(string parameters, bool decPrivateMode = false)` (L850~L858)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private bool WriteCsi(string parameters, bool decPrivateMode = false)
    {
        if (!Capabilities.Ansi)
        {
            return false;
        }

        Write(decPrivateMode ? $"\e[?{parameters}" : $"\e[{parameters}");
        return true;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private AnsiWriter WriteCsi(string parameters, bool decPrivateMode = false)
    {
        if (Capabilities.Ansi)
        {
            Write(decPrivateMode ? $"\e[?{parameters}" : $"\e[{parameters}");
        }

        return this;
    }
```

### 🔹 函式: `AnsiWriter.CursorUp()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorUp(int steps)` (L354~L358)
- **變更後簽章 (After)**: `AnsiWriter.CursorUp(int steps)` (L352~L355)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorUp(int steps)
    {
        WriteCsi(steps, 'A');
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorUp(int steps)
    {
        return WriteCsi(steps, 'A');
    }
```

### 🔹 函式: `AnsiWriter.CursorRight()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorRight(int steps)` (L387~L391)
- **變更後簽章 (After)**: `AnsiWriter.CursorRight(int steps)` (L383~L386)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorRight(int steps)
    {
        WriteCsi(steps, 'C');
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorRight(int steps)
    {
        return CursorForward(steps);
    }
```

### 🔹 函式: `AnsiWriter.RestoreCursor()`
- **變更前簽章 (Before)**: `AnsiWriter.RestoreCursor()` (L457~L461)
- **變更後簽章 (After)**: `AnsiWriter.RestoreCursor(bool stayOnPage = true)` (L487~L497)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter RestoreCursor()
    {
        WriteCsi("u");
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter RestoreCursor(bool stayOnPage = true)
    {
        if (stayOnPage)
        {
            // SCORC
            return WriteCsi("u");
        }

        // DECRC
        return WriteEsc("8");
    }
```

### 🔹 函式: `AnsiWriter.EnterAltScreen()`
- **變更前簽章 (Before)**: `AnsiWriter.EnterAltScreen()` (L481~L485)
- **變更後簽章 (After)**: `AnsiWriter.EnterAltScreen()` (L516~L519)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter EnterAltScreen()
    {
        WriteCsi(1049, 'h', decPrivateMode: true);
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter EnterAltScreen()
    {
        return WriteCsi(1049, 'h', decPrivateMode: true);
    }
```

### 🔹 函式: `AnsiWriter.ClearScrollback()`
- **變更前簽章 (Before)**: `AnsiWriter.ClearScrollback()` (L563~L567)
- **變更後簽章 (After)**: `AnsiWriter.ClearScrollback()` (L594~L597)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter ClearScrollback()
    {
        WriteCsi(3, 'J');
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter ClearScrollback()
    {
        return EraseInDisplay(3);
    }
```

### 🔹 函式: `AnsiWriter.CursorLeft()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorLeft(int steps)` (L403~L407)
- **變更後簽章 (After)**: `AnsiWriter.CursorLeft(int steps)` (L413~L416)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorLeft(int steps)
    {
        WriteCsi(steps, 'D');
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorLeft(int steps)
    {
        return CursorBackward(steps);
    }
```

### 🔹 函式: `AnsiWriter.EraseInDisplay()`
- **變更前簽章 (Before)**: `AnsiWriter.EraseInDisplay(int mode = 0)` (L553~L557)
- **變更後簽章 (After)**: `AnsiWriter.EraseInDisplay(int mode = 0)` (L585~L588)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter EraseInDisplay(int mode = 0)
    {
        WriteCsi(mode, 'J');
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter EraseInDisplay(int mode = 0)
    {
        return WriteCsi(mode, 'J');
    }
```

### 🔹 函式: `AnsiWriter.HideCursor()`
- **變更前簽章 (Before)**: `AnsiWriter.HideCursor()` (L429~L433)
- **變更後簽章 (After)**: `AnsiWriter.HideCursor()` (L452~L455)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter HideCursor()
    {
        WriteCsi(25, 'l', decPrivateMode: true);
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter HideCursor()
    {
        return WriteCsi(25, 'l', decPrivateMode: true);
    }
```

### 🔹 函式: `AnsiWriter.CursorPosition()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorPosition(int row, int column)` (L325~L329)
- **變更後簽章 (After)**: `AnsiWriter.CursorPosition(int row, int column)` (L325~L328)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorPosition(int row, int column)
    {
        WriteCsi($"{row};{column}", 'H');
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorPosition(int row, int column)
    {
        return WriteCsi($"{row};{column}", 'H');
    }
```

### 🔹 函式: `AnsiWriter.WriteSgr()`
- **變更前簽章 (Before)**: `AnsiWriter.WriteSgr(params List<byte> codes)` (L569~L578)
- **變更後簽章 (After)**: `AnsiWriter.WriteSgr(params List<byte> codes)` (L875~L890)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private bool WriteSgr(params List<byte> codes)
    {
        if (!Capabilities.Ansi || codes.Count == 0)
        {
            return false;
        }

        WriteCsi(string.Join(";", codes), 'm');
        return true;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private bool WriteSgr(params List<byte> codes)
    {
        if (!Capabilities.Ansi)
        {
            return false;
        }

        var parameters = string.Join(";", codes);
        if (string.IsNullOrWhiteSpace(parameters))
        {
            return false;
        }

        WriteCsi(parameters, 'm');
        return true;
    }
```

### 🔹 函式: `AnsiWriter.CursorHome()`
- **變更前簽章 (Before)**: `AnsiWriter.CursorHome()` (L338~L342)
- **變更後簽章 (After)**: `AnsiWriter.CursorHome()` (L337~L340)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter CursorHome()
    {
        WriteCsi("H");
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter CursorHome()
    {
        return WriteCsi("H");
    }
```

### 🔹 函式: `AnsiWriter.ExitAltScreen()`
- **變更前簽章 (Before)**: `AnsiWriter.ExitAltScreen()` (L491~L495)
- **變更後簽章 (After)**: `AnsiWriter.ExitAltScreen()` (L525~L528)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public AnsiWriter ExitAltScreen()
    {
        WriteCsi(1049, 'l', decPrivateMode: true);
        return this;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public AnsiWriter ExitAltScreen()
    {
        return WriteCsi(1049, 'l', decPrivateMode: true);
    }
```

### 🔹 函式: `AnsiWriter.WriteCsi()`
- **變更前簽章 (Before)**: `AnsiWriter.WriteCsi(int value, char terminator, bool decPrivateMode = false)` (L580~L583)
- **變更後簽章 (After)**: `AnsiWriter.WriteCsi(int value, char terminator, bool decPrivateMode = false)` (L840~L843)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private bool WriteCsi(int value, char terminator, bool decPrivateMode = false)
    {
        return WriteCsi($"{value}{terminator}", decPrivateMode);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private AnsiWriter WriteCsi(int value, char terminator, bool decPrivateMode = false)
    {
        return WriteCsi($"{value}{terminator}", decPrivateMode);
    }
```

### 🔹 函式: `AnsiWriter.WriteOsc()`
- **變更前簽章 (Before)**: `AnsiWriter.WriteOsc(string parameters)` (L601~L610)
- **變更後簽章 (After)**: `AnsiWriter.WriteOsc(string parameters)` (L860~L868)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private bool WriteOsc(string parameters)
    {
        if (!Capabilities.Ansi)
        {
            return false;
        }

        Write($"\e]{parameters}");
        return true;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private AnsiWriter WriteOsc(string parameters)
    {
        if (Capabilities.Ansi)
        {
            Write($"\e]{parameters}");
        }

        return this;
    }
```


#### 📄 檔案: `src/Spectre.Console/CircularBuffer.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:31, E:29, A:0) ➔ After(N:0, E:0, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 31, +Edges: 0, -Edges: 29, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `state_36` (MODULE_STATE)
  • - [移除節點] `_collection` (MODULE_STATE)
  • - [移除節點] `CircularBuffer.GetEnumerator` (FUNCTION_DEF)
  • - [移除節點] `Array.Empty<T> (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `_buffer.ToList (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `CircularBuffer.IndexOf` (FUNCTION_DEF)
  • - [移除節點] `CircularBuffer.Contains` (FUNCTION_DEF)
  • - [移除節點] `CircularBuffer.Increment` (FUNCTION_DEF)
  • - [移除節點] `state_37` (MODULE_STATE)
  • - [移除節點] `CircularBuffer.Clear` (FUNCTION_DEF)
  • - [移除節點] `CircularBuffer.GetEnumerator` (FUNCTION_DEF)
  • - [移除節點] `CircularBuffer.ValidateIndexInRange` (FUNCTION_DEF)
  • - [移除節點] `Debug.Assert (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `CollectionsMarshal.AsSpan (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `CircularBuffer.ToArray` (FUNCTION_DEF)
  • _... 以及其餘 45 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `src/Spectre.Console/Internal/CircularBuffer.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:31, E:29, A:0)
- **差分統計**: +Nodes: 31, -Nodes: 0, +Edges: 29, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_36` (MODULE_STATE)
  • + [新增節點] `_collection` (MODULE_STATE)
  • + [新增節點] `CircularBuffer.GetEnumerator` (FUNCTION_DEF)
  • + [新增節點] `Array.Empty<T> (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_buffer.ToList (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `CircularBuffer.IndexOf` (FUNCTION_DEF)
  • + [新增節點] `CircularBuffer.Contains` (FUNCTION_DEF)
  • + [新增節點] `CircularBuffer.Increment` (FUNCTION_DEF)
  • + [新增節點] `state_37` (MODULE_STATE)
  • + [新增節點] `CircularBuffer.Clear` (FUNCTION_DEF)
  • + [新增節點] `CircularBuffer.GetEnumerator` (FUNCTION_DEF)
  • + [新增節點] `CircularBuffer.ValidateIndexInRange` (FUNCTION_DEF)
  • + [新增節點] `Debug.Assert (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `CollectionsMarshal.AsSpan (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `CircularBuffer.ToArray` (FUNCTION_DEF)
  • _... 以及其餘 45 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #15: `33bcbc4a`
- **完整 Hash**: `33bcbc4a269fbfaa354395ba4839d31c471db533`
- **說明 (Ground Truth)**: Fix Segment.SplitLines ignoring multiple line breaks (#2052)
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console/Rendering/Segment.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:61, E:75, A:0) ➔ After(N:61, E:75, A:0)
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
  • + [新增節點] `string.Join (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `string.Concat (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Segment.SplitLines` ──[CALLS]──> `string.Join (External/BCL)`
  • - [移除呼叫邊] `Segment.SplitLines` ──[CALLS]──> `string.Concat (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Segment.SplitLines()`
- **變更前簽章 (Before)**: `Segment.SplitLines(IEnumerable<Segment> segments, int maxWidth, int? height = null)` (L207~L315)
- **變更後簽章 (After)**: `Segment.SplitLines(IEnumerable<Segment> segments, int maxWidth, int? height = null)` (L207~L315)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static List<SegmentLine> SplitLines(IEnumerable<Segment> segments, int maxWidth, int? height = null)
    {
        ArgumentNullException.ThrowIfNull(segments);

        var lines = new List<SegmentLine>();
        var line = new SegmentLine();

        var stack = new Stack<Segment>(segments.Reverse());

        while (stack.Count > 0)
        {
            var segment = stack.Pop();
            var segmentLength = segment.CellCount();

            // Does this segment make the line exceed the max width?
            var lineLength = line.CellCount();
            if (lineLength + segmentLength > maxWidth)
            {
                var offset = maxWidth - lineLength;

                var (first, second) = segment.Split(offset);

                line.Add(first);
                lines.Add(line);
                line = [];

                if (second != null)
                {
                    stack.Push(second);
                }

                continue;
            }

            // Does the segment contain a newline?
            if (segment.Text.ContainsExact("\n"))
            {
                // Is it a new line?
                if (segment.Text == "\n")
                {
                    if (line.Length != 0 || segment.IsLineBreak)
                    {
                        lines.Add(line);
                        line = [];
                    }

                    continue;
                }

                var text = segment.Text;
                while (text != null)
                {
                    var parts = text.SplitLines();
                    if (parts.Length > 0)
                    {
                        if (parts[0].Length > 0)
                        {
                            line.Add(new Segment(parts[0], segment.Style));
                        }
                    }

                    if (parts.Length > 1)
                    {
                        if (line.Length > 0)
                        {
                            lines.Add(line);
                            line = [];
                        }

                        text = string.Concat(parts.Skip(1).Take(parts.Length - 1));
                    }
                    else
                    {
                        text = null;
                    }
                }
            }
            else
            {
                line.Add(segment);
            }
        }

        if (line.Count > 0)
        {
            lines.Add(line);
        }

        // Got a height specified?
        if (height != null)
        {
            if (lines.Count >= height)
            {
                // Remove lines
                lines.RemoveRange(height.Value, lines.Count - height.Value);
            }
            else
            {
                // Add lines
                var missing = height - lines.Count;
                for (var i = 0; i < missing; i++)
                {
                    lines.Add([]);
                }
            }
        }

        return lines;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static List<SegmentLine> SplitLines(IEnumerable<Segment> segments, int maxWidth, int? height = null)
    {
        ArgumentNullException.ThrowIfNull(segments);

        var lines = new List<SegmentLine>();
        var line = new SegmentLine();

        var stack = new Stack<Segment>(segments.Reverse());

        while (stack.Count > 0)
        {
            var segment = stack.Pop();
            var segmentLength = segment.CellCount();

            // Does this segment make the line exceed the max width?
            var lineLength = line.CellCount();
            if (lineLength + segmentLength > maxWidth)
            {
                var offset = maxWidth - lineLength;

                var (first, second) = segment.Split(offset);

                line.Add(first);
                lines.Add(line);
                line = [];

                if (second != null)
                {
                    stack.Push(second);
                }

                continue;
            }

            // Does the segment contain a newline?
            if (segment.Text.ContainsExact("\n"))
            {
                // Is it a new line?
                if (segment.Text == "\n")
                {
                    if (line.Length != 0 || segment.IsLineBreak)
                    {
                        lines.Add(line);
                        line = [];
                    }

                    continue;
                }

                var text = segment.Text;
                while (text != null)
                {
                    var parts = text.SplitLines();
                    if (parts.Length > 0)
                    {
                        if (parts[0].Length > 0)
                        {
                            line.Add(new Segment(parts[0], segment.Style));
                        }
                    }

                    if (parts.Length > 1)
                    {
                        if (line.Length > 0)
                        {
                            lines.Add(line);
                            line = [];
                        }

                        text = string.Join('\n', parts.Skip(1).Take(parts.Length - 1));
                    }
                    else
                    {
                        text = null;
                    }
                }
            }
            else
            {
                line.Add(segment);
            }
        }

        if (line.Count > 0)
        {
            lines.Add(line);
        }

        // Got a height specified?
        if (height != null)
        {
            if (lines.Count >= height)
            {
                // Remove lines
                lines.RemoveRange(height.Value, lines.Count - height.Value);
            }
            else
            {
                // Add lines
                var missing = height - lines.Count;
                for (var i = 0; i < missing; i++)
                {
                    lines.Add([]);
                }
            }
        }

        return lines;
    }
```


---

### 🔹 Commit #16: `94a9a0ba`
- **完整 Hash**: `94a9a0bab7b7bad8760329a897a8c81482f02ff0`
- **說明 (Ground Truth)**: Escape text in AnsiMarkupSegment.ToString()
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console.Ansi/AnsiMarkup.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:37, E:38, A:1) ➔ After(N:37, E:39, A:1)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#result[^1]** `(Button / UI Control)`
    └── ⚡ **Text()**

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_231` (MODULE_STATE)
  • - [移除節點] `state_230` (MODULE_STATE)
  • + [新增呼叫邊] `AnsiMarkupSegment.ToString` ──[CALLS]──> `AnsiMarkup.Escape`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `AnsiMarkupSegment.ToString()`
- **變更前簽章 (Before)**: `AnsiMarkupSegment.ToString()` (L199~L204)
- **變更後簽章 (After)**: `AnsiMarkupSegment.ToString()` (L199~L205)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public override string ToString()
    {
        return !Style.Equals(Style.Plain)
            ? $"[{Style.ToMarkup()}]{Text}[/]"
            : Text;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public override string ToString()
    {
        var escaped = AnsiMarkup.Escape(Text);
        return !Style.Equals(Style.Plain)
            ? $"[{Style.ToMarkup()}]{escaped}[/]"
            : escaped;
    }
```


---

### 🔹 Commit #17: `9eb0b0e4`
- **完整 Hash**: `9eb0b0e497ad3d8a2aa81fda2fd3d73e12dc0f1b`
- **說明 (Ground Truth)**: Disable ANSI when stdout or stderr is redirected (#2047)
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console.Ansi/AnsiDetector.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:22, E:18, A:0) ➔ After(N:23, E:19, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 10, -Edges: 9, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `AnsiDetector.Detect` (FUNCTION_DEF)
  • + [新增呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `AnsiDetector.Detect`
  • + [新增呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `buffer.IsStandardOut (External/BCL)`
  • + [新增呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `buffer.IsStandardError (External/BCL)`
  • + [新增呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `AnsiDetector.Detect`
  • + [新增呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `RuntimeInformation.IsOSPlatform (External/BCL)`
  • + [新增呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `Environment.GetEnvironmentVariable (External/BCL)`
  • + [新增呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `string.IsNullOrEmpty (External/BCL)`
  • + [新增呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `conEmu.Equals (External/BCL)`
  • + [新增呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `Windows.SupportsAnsi`
  • + [新增呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `AnsiDetector.DetectFromTerm`
  • - [移除呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `AnsiDetector.Detect`
  • - [移除呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `buffer.IsStandardError (External/BCL)`
  • - [移除呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `buffer.IsStandardOut (External/BCL)`
  • - [移除呼叫邊] `AnsiDetector.Detect` ──[CALLS]──> `RuntimeInformation.IsOSPlatform (External/BCL)`
  • _... 以及其餘 5 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `AnsiDetector.Detect()`
- **變更前簽章 (Before)**: `AnsiDetector.Detect(bool stdError, bool upgrade)` (L52~L69)
- **變更後簽章 (After)**: `AnsiDetector.Detect(
        TextWriter buffer,
        AnsiSupport ansi,
        bool isOutputRedirected,
        bool isErrorRedirected)` (L37~L73)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private static (bool SupportsAnsi, bool LegacyConsole) Detect(bool stdError, bool upgrade)
    {
        // Running on Windows?
        if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
        {
            // Running under ConEmu?
            var conEmu = Environment.GetEnvironmentVariable("ConEmuANSI");
            if (!string.IsNullOrEmpty(conEmu) && conEmu.Equals("On", StringComparison.OrdinalIgnoreCase))
            {
                return (true, false);
            }

            var supportsAnsi = Windows.SupportsAnsi(upgrade, stdError, out var legacyConsole);
            return (supportsAnsi, legacyConsole);
        }

        return DetectFromTerm();
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal static (bool Ansi, bool Legacy) Detect(
        TextWriter buffer,
        AnsiSupport ansi,
        bool isOutputRedirected,
        bool isErrorRedirected)
    {
        var supportsAnsi = ansi == AnsiSupport.Yes;
        var legacyConsole = false;

        if (ansi == AnsiSupport.Detect)
        {
            if (buffer.IsStandardOut() && isOutputRedirected)
            {
                return (false, false);
            }

            if (buffer.IsStandardError() && isErrorRedirected)
            {
                return (false, false);
            }

            (supportsAnsi, legacyConsole) = AnsiDetector.Detect(buffer.IsStandardError(), true);
            return (supportsAnsi, legacyConsole);
        }

        if (buffer.IsStandardOut() || buffer.IsStandardError())
        {
            // Are we running on Windows?
            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                // Try detecting whether or not this is a legacy console
                (_, legacyConsole) = AnsiDetector.Detect(buffer.IsStandardError(), false);
            }
        }

        return (supportsAnsi, legacyConsole);
    }
```

### 🔹 函式: `AnsiDetector.Detect()`
- **變更前簽章 (Before)**: `AnsiDetector.Detect(TextWriter buffer, AnsiSupport ansi)` (L28~L50)
- **變更後簽章 (After)**: `AnsiDetector.Detect(TextWriter buffer, AnsiSupport ansi)` (L28~L35)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static (bool Ansi, bool Legacy) Detect(TextWriter buffer, AnsiSupport ansi)
    {
        var supportsAnsi = ansi == AnsiSupport.Yes;
        var legacyConsole = false;

        if (ansi == AnsiSupport.Detect)
        {
            (supportsAnsi, legacyConsole) = AnsiDetector.Detect(buffer.IsStandardError(), true);
            return (supportsAnsi, legacyConsole);
        }

        if (buffer.IsStandardOut() || buffer.IsStandardError())
        {
            // Are we running on Windows?
            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                // Try detecting whether or not this is a legacy console
                (_, legacyConsole) = AnsiDetector.Detect(buffer.IsStandardError(), false);
            }
        }

        return (supportsAnsi, legacyConsole);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static (bool Ansi, bool Legacy) Detect(TextWriter buffer, AnsiSupport ansi)
    {
        return Detect(
            buffer,
            ansi,
            System.Console.IsOutputRedirected,
            System.Console.IsErrorRedirected);
    }
```


---

### 🔹 Commit #18: `b3f8c848`
- **完整 Hash**: `b3f8c8483e61fe3bed117cec78f3cecc16d08ba3`
- **說明 (Ground Truth)**: Fix memory leak bug related to Segment (#2046)
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console/Rendering/Segment.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:61, E:75, A:0) ➔ After(N:61, E:75, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_595` (MODULE_STATE)
  • - [移除節點] `state_596` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Segment.SplitLines()`
- **變更前簽章 (Before)**: `Segment.SplitLines(IEnumerable<Segment> segments, int maxWidth, int? height = null)` (L207~L316)
- **變更後簽章 (After)**: `Segment.SplitLines(IEnumerable<Segment> segments, int maxWidth, int? height = null)` (L207~L315)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static List<SegmentLine> SplitLines(IEnumerable<Segment> segments, int maxWidth, int? height = null)
    {
        ArgumentNullException.ThrowIfNull(segments);

        var lines = new List<SegmentLine>();
        var line = new SegmentLine();

        var stack = new Stack<Segment>(segments.Reverse());

        while (stack.Count > 0)
        {
            var segment = stack.Pop();
            var segmentLength = segment.CellCount();

            // Does this segment make the line exceed the max width?
            var lineLength = line.CellCount();
            if (lineLength + segmentLength > maxWidth)
            {
                var diff = -(maxWidth - (lineLength + segmentLength));
                var offset = segment.Text.Length - diff;

                var (first, second) = segment.Split(offset);

                line.Add(first);
                lines.Add(line);
                line = [];

                if (second != null)
                {
                    stack.Push(second);
                }

                continue;
            }

            // Does the segment contain a newline?
            if (segment.Text.ContainsExact("\n"))
            {
                // Is it a new line?
                if (segment.Text == "\n")
                {
                    if (line.Length != 0 || segment.IsLineBreak)
                    {
                        lines.Add(line);
                        line = [];
                    }

                    continue;
                }

                var text = segment.Text;
                while (text != null)
                {
                    var parts = text.SplitLines();
                    if (parts.Length > 0)
                    {
                        if (parts[0].Length > 0)
                        {
                            line.Add(new Segment(parts[0], segment.Style));
                        }
                    }

                    if (parts.Length > 1)
                    {
                        if (line.Length > 0)
                        {
                            lines.Add(line);
                            line = [];
                        }

                        text = string.Concat(parts.Skip(1).Take(parts.Length - 1));
                    }
                    else
                    {
                        text = null;
                    }
                }
            }
            else
            {
                line.Add(segment);
            }
        }

        if (line.Count > 0)
        {
            lines.Add(line);
        }

        // Got a height specified?
        if (height != null)
        {
            if (lines.Count >= height)
            {
                // Remove lines
                lines.RemoveRange(height.Value, lines.Count - height.Value);
            }
            else
            {
                // Add lines
                var missing = height - lines.Count;
                for (var i = 0; i < missing; i++)
                {
                    lines.Add([]);
                }
            }
        }

        return lines;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static List<SegmentLine> SplitLines(IEnumerable<Segment> segments, int maxWidth, int? height = null)
    {
        ArgumentNullException.ThrowIfNull(segments);

        var lines = new List<SegmentLine>();
        var line = new SegmentLine();

        var stack = new Stack<Segment>(segments.Reverse());

        while (stack.Count > 0)
        {
            var segment = stack.Pop();
            var segmentLength = segment.CellCount();

            // Does this segment make the line exceed the max width?
            var lineLength = line.CellCount();
            if (lineLength + segmentLength > maxWidth)
            {
                var offset = maxWidth - lineLength;

                var (first, second) = segment.Split(offset);

                line.Add(first);
                lines.Add(line);
                line = [];

                if (second != null)
                {
                    stack.Push(second);
                }

                continue;
            }

            // Does the segment contain a newline?
            if (segment.Text.ContainsExact("\n"))
            {
                // Is it a new line?
                if (segment.Text == "\n")
                {
                    if (line.Length != 0 || segment.IsLineBreak)
                    {
                        lines.Add(line);
                        line = [];
                    }

                    continue;
                }

                var text = segment.Text;
                while (text != null)
                {
                    var parts = text.SplitLines();
                    if (parts.Length > 0)
                    {
                        if (parts[0].Length > 0)
                        {
                            line.Add(new Segment(parts[0], segment.Style));
                        }
                    }

                    if (parts.Length > 1)
                    {
                        if (line.Length > 0)
                        {
                            lines.Add(line);
                            line = [];
                        }

                        text = string.Concat(parts.Skip(1).Take(parts.Length - 1));
                    }
                    else
                    {
                        text = null;
                    }
                }
            }
            else
            {
                line.Add(segment);
            }
        }

        if (line.Count > 0)
        {
            lines.Add(line);
        }

        // Got a height specified?
        if (height != null)
        {
            if (lines.Count >= height)
            {
                // Remove lines
                lines.RemoveRange(height.Value, lines.Count - height.Value);
            }
            else
            {
                // Add lines
                var missing = height - lines.Count;
                for (var i = 0; i < missing; i++)
                {
                    lines.Add([]);
                }
            }
        }

        return lines;
    }
```


---

### 🔹 Commit #19: `ad44bce7`
- **完整 Hash**: `ad44bce7e61f2a4049fc3ce74d7222fdaf40a640`
- **說明 (Ground Truth)**: Fix interactive console detection when output is redirected (#2042)
- **變更檔案數**: 1

#### 📄 檔案: `src/Spectre.Console/InteractionDetector.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:1, E:0, A:0) ➔ After(N:2, E:1, A:0)
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
  • + [新增節點] `InteractionDetector.IsInteractive` (FUNCTION_DEF)
  • + [新增呼叫邊] `InteractionDetector.IsInteractive` ──[CALLS]──> `InteractionDetector.IsInteractive`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `InteractionDetector.IsInteractive()`
- **變更前簽章 (Before)**: `InteractionDetector.IsInteractive(InteractionSupport interaction)` (L5~L15)
- **變更後簽章 (After)**: `InteractionDetector.IsInteractive(InteractionSupport interaction)` (L5~L12)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static bool IsInteractive(InteractionSupport interaction)
    {
        var interactive = interaction == InteractionSupport.Yes;
        if (interaction == InteractionSupport.Detect)
        {
            // TODO: We need a better way of checking this
            interactive = !System.Console.IsInputRedirected;
        }

        return interactive;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static bool IsInteractive(InteractionSupport interaction)
    {
        return IsInteractive(
            interaction,
            System.Console.IsInputRedirected,
            System.Console.IsOutputRedirected,
            System.Console.IsErrorRedirected);
    }
```


---

### 🔹 Commit #20: `5369ef92`
- **完整 Hash**: `5369ef92900abaf40646e8e9af8592c0cf6fbd47`
- **說明 (Ground Truth)**: Text prompt editable default (#2016)
- **變更檔案數**: 3

#### 📄 檔案: `src/Spectre.Console/Extensions/AnsiConsoleExtensions.Input.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:21, E:21, A:0) ➔ After(N:24, E:24, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 3, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `injectedQueue.Enqueue (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `injectedQueue.Dequeue (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `char.IsUpper (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `AnsiConsoleExtensions.ReadLine` ──[CALLS]──> `char.IsUpper (External/BCL)`
  • + [新增呼叫邊] `AnsiConsoleExtensions.ReadLine` ──[CALLS]──> `injectedQueue.Enqueue (External/BCL)`
  • + [新增呼叫邊] `AnsiConsoleExtensions.ReadLine` ──[CALLS]──> `injectedQueue.Dequeue (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `AnsiConsoleExtensions.ReadLine()`
- **變更前簽章 (Before)**: `AnsiConsoleExtensions.ReadLine(this IAnsiConsole console, Style? style, bool secret, char? mask, IEnumerable<string>? items = null, CancellationToken cancellationToken = default)` (L8~L78)
- **變更後簽章 (After)**: `AnsiConsoleExtensions.ReadLine(this IAnsiConsole console, Style? style, bool secret, char? mask, IEnumerable<string>? items = null, CancellationToken cancellationToken = default, string? initialInput = null)` (L8~L99)

#### ◀️ 變更前實作碼 (Before Implementation):
```
internal static async Task<string> ReadLine(this IAnsiConsole console, Style? style, bool secret, char? mask, IEnumerable<string>? items = null, CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(console);

        style ??= Style.Plain;
        var text = string.Empty;

        var autocomplete = new List<string>(items ?? []);

        while (true)
        {
            cancellationToken.ThrowIfCancellationRequested();
            var rawKey = await console.Input.ReadKeyAsync(true, cancellationToken).ConfigureAwait(false);
            if (rawKey == null)
            {
                continue;
            }

            var key = rawKey.Value;
            if (key.Key == ConsoleKey.Enter)
            {
                return text;
            }

            if (key.Key == ConsoleKey.Tab && autocomplete.Count > 0)
            {
                var autoCompleteDirection = key.Modifiers.HasFlag(ConsoleModifiers.Shift)
                    ? AutoCompleteDirection.Backward
                    : AutoCompleteDirection.Forward;
                var replace = AutoComplete(autocomplete, text, autoCompleteDirection);
                if (!string.IsNullOrEmpty(replace))
                {
                    // Render the suggestion
                    console.Write("\b \b".Repeat(text.Length), style);
                    console.Write(replace);
                    text = replace;
                    continue;
                }
            }

            if (key.Key == ConsoleKey.Backspace)
            {
                if (text.Length > 0)
                {
                    var lastChar = text.Last();
                    text = text.Substring(0, text.Length - 1);

                    if (mask != null)
                    {
                        if (UnicodeCalculator.GetWidth(lastChar) == 1)
                        {
                            console.Write("\b \b");
                        }
                        else if (UnicodeCalculator.GetWidth(lastChar) == 2)
                        {
                            console.Write("\b \b\b \b");
                        }
                    }
                }

                continue;
            }

            if (!char.IsControl(key.KeyChar))
            {
                text += key.KeyChar.ToString();
                var output = key.KeyChar.ToString();
                console.Write(secret ? output.Mask(mask) : output, style);
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal static async Task<string> ReadLine(this IAnsiConsole console, Style? style, bool secret, char? mask, IEnumerable<string>? items = null, CancellationToken cancellationToken = default, string? initialInput = null)
    {
        ArgumentNullException.ThrowIfNull(console);

        style ??= Style.Plain;
        var text = string.Empty;

        var autocomplete = new List<string>(items ?? []);

        Queue<ConsoleKeyInfo>? injectedQueue = null;
        if (!string.IsNullOrEmpty(initialInput))
        {
            injectedQueue = new Queue<ConsoleKeyInfo>();
            foreach (var ch in initialInput)
            {
                var control = char.IsUpper(ch);
                injectedQueue.Enqueue(new ConsoleKeyInfo(ch, (ConsoleKey)ch, false, false, control));
            }
        }

        while (true)
        {
            cancellationToken.ThrowIfCancellationRequested();

            ConsoleKeyInfo? rawKey;
            if (injectedQueue != null && injectedQueue.Count > 0)
            {
                rawKey = injectedQueue.Dequeue();
            }
            else
            {
                rawKey = await console.Input.ReadKeyAsync(true, cancellationToken).ConfigureAwait(false);
            }

            if (rawKey == null)
            {
                continue;
            }

            var key = rawKey.Value;
            if (key.Key == ConsoleKey.Enter)
            {
                return text;
            }

            if (key.Key == ConsoleKey.Tab && autocomplete.Count > 0)
            {
                var autoCompleteDirection = key.Modifiers.HasFlag(ConsoleModifiers.Shift)
                    ? AutoCompleteDirection.Backward
                    : AutoCompleteDirection.Forward;
                var replace = AutoComplete(autocomplete, text, autoCompleteDirection);
                if (!string.IsNullOrEmpty(replace))
                {
                    // Render the suggestion
                    console.Write("\b \b".Repeat(text.Length), style);
                    console.Write(replace);
                    text = replace;
                    continue;
                }
            }

            if (key.Key == ConsoleKey.Backspace)
            {
                if (text.Length > 0)
                {
                    var lastChar = text.Last();
                    text = text.Substring(0, text.Length - 1);

                    if (mask != null)
                    {
                        if (UnicodeCalculator.GetWidth(lastChar) == 1)
                        {
                            console.Write("\b \b");
                        }
                        else if (UnicodeCalculator.GetWidth(lastChar) == 2)
                        {
                            console.Write("\b \b\b \b");
                        }
                    }
                }

                continue;
            }

            if (!char.IsControl(key.KeyChar))
            {
                text += key.KeyChar.ToString();
                var output = key.KeyChar.ToString();
                console.Write(secret ? output.Mask(mask) : output, style);
            }
        }
    }
```


#### 📄 檔案: `src/Spectre.Console/Prompts/TextPrompt.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:41, E:43, A:0) ➔ After(N:42, E:44, A:0)
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
  • + [新增節點] `console.ReadLine(promptStyle, IsSecret, Mask, choices, cancellationToken, converter(DefaultValue.Value)).ConfigureAwait (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `console.RunExclusive(async () =>
        {
            var promptStyle = PromptStyle ?? Style.Plain;
            var converter = Converter ?? TypeConverterHelper.ConvertToString;
            var choices = Choices.Select(choice => converter(choice)).ToList();
            var choiceMap = Choices.ToDictionary(choice => converter(choice), choice => choice, _comparer);

            WritePrompt(console);

            while (true)
            {
                string input;
                if (EditableDefaultValue && DefaultValue != null)
                {
                    input = await console.ReadLine(promptStyle, IsSecret, Mask, choices, cancellationToken, converter(DefaultValue.Value)).ConfigureAwait(false);
                }
                else
                {
                    input = await console.ReadLine(promptStyle, IsSecret, Mask, choices, cancellationToken).ConfigureAwait(false);
                }



                // Nothing entered?
                if (string.IsNullOrWhiteSpace(input))
                {
                    if (DefaultValue != null)
                    {
                        var defaultValue = converter(DefaultValue.Value);
                        console.Write(IsSecret ? defaultValue.Mask(Mask) : defaultValue, promptStyle);
                        console.WriteLine();

                        ClearPromptLine(console);
                        return DefaultValue.Value;
                    }

                    if (!AllowEmpty)
                    {
                        continue;
                    }
                }

                console.WriteLine();

                T? result;
                if (Choices.Count > 0)
                {
                    if (choiceMap.TryGetValue(input, out result) && result != null)
                    {
                        ClearPromptLine(console);
                        return result;
                    }
                    else
                    {
                        console.MarkupLine(InvalidChoiceMessage);
                        WritePrompt(console);
                        continue;
                    }
                }
                else if (!TypeConverterHelper.TryConvertFromStringWithCulture<T>(input, Culture, out result) || result == null)
                {
                    console.MarkupLine(ValidationErrorMessage);
                    WritePrompt(console);
                    continue;
                }

                // Run all validators
                if (!ValidateResult(result, out var validationMessage))
                {
                    console.MarkupLine(validationMessage);
                    WritePrompt(console);
                    continue;
                }

                ClearPromptLine(console);
                return result;
            }
        }).ConfigureAwait (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `console.RunExclusive(async () =>
        {
            var promptStyle = PromptStyle ?? Style.Plain;
            var converter = Converter ?? TypeConverterHelper.ConvertToString;
            var choices = Choices.Select(choice => converter(choice)).ToList();
            var choiceMap = Choices.ToDictionary(choice => converter(choice), choice => choice, _comparer);

            WritePrompt(console);

            while (true)
            {
                var input = await console.ReadLine(promptStyle, IsSecret, Mask, choices, cancellationToken).ConfigureAwait(false);

                // Nothing entered?
                if (string.IsNullOrWhiteSpace(input))
                {
                    if (DefaultValue != null)
                    {
                        var defaultValue = converter(DefaultValue.Value);
                        console.Write(IsSecret ? defaultValue.Mask(Mask) : defaultValue, promptStyle);
                        console.WriteLine();

                        ClearPromptLine(console);
                        return DefaultValue.Value;
                    }

                    if (!AllowEmpty)
                    {
                        continue;
                    }
                }

                console.WriteLine();

                T? result;
                if (Choices.Count > 0)
                {
                    if (choiceMap.TryGetValue(input, out result) && result != null)
                    {
                        ClearPromptLine(console);
                        return result;
                    }
                    else
                    {
                        console.MarkupLine(InvalidChoiceMessage);
                        WritePrompt(console);
                        continue;
                    }
                }
                else if (!TypeConverterHelper.TryConvertFromStringWithCulture<T>(input, Culture, out result) || result == null)
                {
                    console.MarkupLine(ValidationErrorMessage);
                    WritePrompt(console);
                    continue;
                }

                // Run all validators
                if (!ValidateResult(result, out var validationMessage))
                {
                    console.MarkupLine(validationMessage);
                    WritePrompt(console);
                    continue;
                }

                ClearPromptLine(console);
                return result;
            }
        }).ConfigureAwait (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `TextPrompt.ShowAsync` ──[CALLS]──> `console.RunExclusive(async () =>
        {
            var promptStyle = PromptStyle ?? Style.Plain;
            var converter = Converter ?? TypeConverterHelper.ConvertToString;
            var choices = Choices.Select(choice => converter(choice)).ToList();
            var choiceMap = Choices.ToDictionary(choice => converter(choice), choice => choice, _comparer);

            WritePrompt(console);

            while (true)
            {
                string input;
                if (EditableDefaultValue && DefaultValue != null)
                {
                    input = await console.ReadLine(promptStyle, IsSecret, Mask, choices, cancellationToken, converter(DefaultValue.Value)).ConfigureAwait(false);
                }
                else
                {
                    input = await console.ReadLine(promptStyle, IsSecret, Mask, choices, cancellationToken).ConfigureAwait(false);
                }



                // Nothing entered?
                if (string.IsNullOrWhiteSpace(input))
                {
                    if (DefaultValue != null)
                    {
                        var defaultValue = converter(DefaultValue.Value);
                        console.Write(IsSecret ? defaultValue.Mask(Mask) : defaultValue, promptStyle);
                        console.WriteLine();

                        ClearPromptLine(console);
                        return DefaultValue.Value;
                    }

                    if (!AllowEmpty)
                    {
                        continue;
                    }
                }

                console.WriteLine();

                T? result;
                if (Choices.Count > 0)
                {
                    if (choiceMap.TryGetValue(input, out result) && result != null)
                    {
                        ClearPromptLine(console);
                        return result;
                    }
                    else
                    {
                        console.MarkupLine(InvalidChoiceMessage);
                        WritePrompt(console);
                        continue;
                    }
                }
                else if (!TypeConverterHelper.TryConvertFromStringWithCulture<T>(input, Culture, out result) || result == null)
                {
                    console.MarkupLine(ValidationErrorMessage);
                    WritePrompt(console);
                    continue;
                }

                // Run all validators
                if (!ValidateResult(result, out var validationMessage))
                {
                    console.MarkupLine(validationMessage);
                    WritePrompt(console);
                    continue;
                }

                ClearPromptLine(console);
                return result;
            }
        }).ConfigureAwait (External/BCL)`
  • + [新增呼叫邊] `TextPrompt.ShowAsync` ──[CALLS]──> `console.ReadLine(promptStyle, IsSecret, Mask, choices, cancellationToken, converter(DefaultValue.Value)).ConfigureAwait (External/BCL)`
  • - [移除呼叫邊] `TextPrompt.ShowAsync` ──[CALLS]──> `console.RunExclusive(async () =>
        {
            var promptStyle = PromptStyle ?? Style.Plain;
            var converter = Converter ?? TypeConverterHelper.ConvertToString;
            var choices = Choices.Select(choice => converter(choice)).ToList();
            var choiceMap = Choices.ToDictionary(choice => converter(choice), choice => choice, _comparer);

            WritePrompt(console);

            while (true)
            {
                var input = await console.ReadLine(promptStyle, IsSecret, Mask, choices, cancellationToken).ConfigureAwait(false);

                // Nothing entered?
                if (string.IsNullOrWhiteSpace(input))
                {
                    if (DefaultValue != null)
                    {
                        var defaultValue = converter(DefaultValue.Value);
                        console.Write(IsSecret ? defaultValue.Mask(Mask) : defaultValue, promptStyle);
                        console.WriteLine();

                        ClearPromptLine(console);
                        return DefaultValue.Value;
                    }

                    if (!AllowEmpty)
                    {
                        continue;
                    }
                }

                console.WriteLine();

                T? result;
                if (Choices.Count > 0)
                {
                    if (choiceMap.TryGetValue(input, out result) && result != null)
                    {
                        ClearPromptLine(console);
                        return result;
                    }
                    else
                    {
                        console.MarkupLine(InvalidChoiceMessage);
                        WritePrompt(console);
                        continue;
                    }
                }
                else if (!TypeConverterHelper.TryConvertFromStringWithCulture<T>(input, Culture, out result) || result == null)
                {
                    console.MarkupLine(ValidationErrorMessage);
                    WritePrompt(console);
                    continue;
                }

                // Run all validators
                if (!ValidateResult(result, out var validationMessage))
                {
                    console.MarkupLine(validationMessage);
                    WritePrompt(console);
                    continue;
                }

                ClearPromptLine(console);
                return result;
            }
        }).ConfigureAwait (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TextPrompt.ShowAsync()`
- **變更前簽章 (Before)**: `TextPrompt.ShowAsync(IAnsiConsole console, CancellationToken cancellationToken)` (L121~L193)
- **變更後簽章 (After)**: `TextPrompt.ShowAsync(IAnsiConsole console, CancellationToken cancellationToken)` (L127~L209)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async Task<T> ShowAsync(IAnsiConsole console, CancellationToken cancellationToken)
    {
        ArgumentNullException.ThrowIfNull(console);

        return await console.RunExclusive(async () =>
        {
            var promptStyle = PromptStyle ?? Style.Plain;
            var converter = Converter ?? TypeConverterHelper.ConvertToString;
            var choices = Choices.Select(choice => converter(choice)).ToList();
            var choiceMap = Choices.ToDictionary(choice => converter(choice), choice => choice, _comparer);

            WritePrompt(console);

            while (true)
            {
                var input = await console.ReadLine(promptStyle, IsSecret, Mask, choices, cancellationToken).ConfigureAwait(false);

                // Nothing entered?
                if (string.IsNullOrWhiteSpace(input))
                {
                    if (DefaultValue != null)
                    {
                        var defaultValue = converter(DefaultValue.Value);
                        console.Write(IsSecret ? defaultValue.Mask(Mask) : defaultValue, promptStyle);
                        console.WriteLine();

                        ClearPromptLine(console);
                        return DefaultValue.Value;
                    }

                    if (!AllowEmpty)
                    {
                        continue;
                    }
                }

                console.WriteLine();

                T? result;
                if (Choices.Count > 0)
                {
                    if (choiceMap.TryGetValue(input, out result) && result != null)
                    {
                        ClearPromptLine(console);
                        return result;
                    }
                    else
                    {
                        console.MarkupLine(InvalidChoiceMessage);
                        WritePrompt(console);
                        continue;
                    }
                }
                else if (!TypeConverterHelper.TryConvertFromStringWithCulture<T>(input, Culture, out result) || result == null)
                {
                    console.MarkupLine(ValidationErrorMessage);
                    WritePrompt(console);
                    continue;
                }

                // Run all validators
                if (!ValidateResult(result, out var validationMessage))
                {
                    console.MarkupLine(validationMessage);
                    WritePrompt(console);
                    continue;
                }

                ClearPromptLine(console);
                return result;
            }
        }).ConfigureAwait(false);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async Task<T> ShowAsync(IAnsiConsole console, CancellationToken cancellationToken)
    {
        ArgumentNullException.ThrowIfNull(console);

        return await console.RunExclusive(async () =>
        {
            var promptStyle = PromptStyle ?? Style.Plain;
            var converter = Converter ?? TypeConverterHelper.ConvertToString;
            var choices = Choices.Select(choice => converter(choice)).ToList();
            var choiceMap = Choices.ToDictionary(choice => converter(choice), choice => choice, _comparer);

            WritePrompt(console);

            while (true)
            {
                string input;
                if (EditableDefaultValue && DefaultValue != null)
                {
                    input = await console.ReadLine(promptStyle, IsSecret, Mask, choices, cancellationToken, converter(DefaultValue.Value)).ConfigureAwait(false);
                }
                else
                {
                    input = await console.ReadLine(promptStyle, IsSecret, Mask, choices, cancellationToken).ConfigureAwait(false);
                }



                // Nothing entered?
                if (string.IsNullOrWhiteSpace(input))
                {
                    if (DefaultValue != null)
                    {
                        var defaultValue = converter(DefaultValue.Value);
                        console.Write(IsSecret ? defaultValue.Mask(Mask) : defaultValue, promptStyle);
                        console.WriteLine();

                        ClearPromptLine(console);
                        return DefaultValue.Value;
                    }

                    if (!AllowEmpty)
                    {
                        continue;
                    }
                }

                console.WriteLine();

                T? result;
                if (Choices.Count > 0)
                {
                    if (choiceMap.TryGetValue(input, out result) && result != null)
                    {
                        ClearPromptLine(console);
                        return result;
                    }
                    else
                    {
                        console.MarkupLine(InvalidChoiceMessage);
                        WritePrompt(console);
                        continue;
                    }
                }
                else if (!TypeConverterHelper.TryConvertFromStringWithCulture<T>(input, Culture, out result) || result == null)
                {
                    console.MarkupLine(ValidationErrorMessage);
                    WritePrompt(console);
                    continue;
                }

                // Run all validators
                if (!ValidateResult(result, out var validationMessage))
                {
                    console.MarkupLine(validationMessage);
                    WritePrompt(console);
                    continue;
                }

                ClearPromptLine(console);
                return result;
            }
        }).ConfigureAwait(false);
    }
```


#### 📄 檔案: `src/Spectre.Console/Prompts/TextPromptExtensions.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:26, E:26, A:0) ➔ After(N:27, E:27, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `TextPromptExtensions.EditableDefaultValue` (FUNCTION_DEF)
  • + [新增呼叫邊] `TextPromptExtensions.EditableDefaultValue` ──[CALLS]──> `ArgumentNullException.ThrowIfNull (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/spectre.console show a5d49bc822ea4e01efa9596782a054bf347b7ad6
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff a5d49bc822ea4e01efa9596782a054bf347b7ad6~1 --file test_repos/spectre.console/src/Spectre.Console/Prompts/MultiSelectionPrompt.cs
   ```
