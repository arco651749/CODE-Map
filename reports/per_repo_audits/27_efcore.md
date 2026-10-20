# 🔬 CODE-Map 基準審查獨立驗證報告: `efcore`
> **技術生態**: `C# (企業級 ORM / 交易管線 / LINQ)`  
> **本地倉庫路徑**: `test_repos/efcore`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 25 Files  
> **報告生成時間**: 2026-10-20 21:43:47  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `21` / `25` | `84.0%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `4` / `25` | `16.0%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `0` / `25` | `0.0%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`25` / `25`** | **`100.0%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `25` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `abf7bd95`
- **完整 Hash**: `abf7bd959db2a114fdc5efb02382984495c465c4`
- **說明 (Ground Truth)**: Preserve model-level SQL Server HiLo sequences in snapshots (#39325)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.SqlServer/Design/Internal/SqlServerAnnotationCodeGenerator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:67, E:38, A:0) ➔ After(N:69, E:40, A:0)
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
  • + [新增節點] `model.GetHiLoSequenceSchema (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `model.GetHiLoSequenceName (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `SqlServerAnnotationCodeGenerator.GenerateValueGenerationStrategy` ──[CALLS]──> `model.GetHiLoSequenceName (External/BCL)`
  • + [新增呼叫邊] `SqlServerAnnotationCodeGenerator.GenerateValueGenerationStrategy` ──[CALLS]──> `model.GetHiLoSequenceSchema (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SqlServerAnnotationCodeGenerator.GenerateValueGenerationStrategy()`
- **變更前簽章 (Before)**: `SqlServerAnnotationCodeGenerator.GenerateValueGenerationStrategy(
        IDictionary<string, IAnnotation> annotations,
        IModel model,
        bool onModel,
        bool complexType)` (L505~L607)
- **變更後簽章 (After)**: `SqlServerAnnotationCodeGenerator.GenerateValueGenerationStrategy(
        IDictionary<string, IAnnotation> annotations,
        IModel model,
        bool onModel,
        bool complexType)` (L505~L609)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private static MethodCallCodeFragment? GenerateValueGenerationStrategy(
        IDictionary<string, IAnnotation> annotations,
        IModel model,
        bool onModel,
        bool complexType)
    {
        SqlServerValueGenerationStrategy strategy;
        if (annotations.TryGetValue(SqlServerAnnotationNames.ValueGenerationStrategy, out var strategyAnnotation)
            && strategyAnnotation.Value != null)
        {
            annotations.Remove(SqlServerAnnotationNames.ValueGenerationStrategy);
            strategy = (SqlServerValueGenerationStrategy)strategyAnnotation.Value;
        }
        else
        {
            return null;
        }

        switch (strategy)
        {
            case SqlServerValueGenerationStrategy.IdentityColumn:
                // Support pre-6.0 IdentitySeed annotations, which contained an int rather than a long
                if (annotations.TryGetValue(SqlServerAnnotationNames.IdentitySeed, out var seedAnnotation)
                    && seedAnnotation.Value != null)
                {
                    annotations.Remove(SqlServerAnnotationNames.IdentitySeed);
                }
                else
                {
                    seedAnnotation = model.FindAnnotation(SqlServerAnnotationNames.IdentitySeed);
                }

                var seed = seedAnnotation is null
                    ? 1L
                    : seedAnnotation.Value is int intValue
                        ? intValue
                        : (long?)seedAnnotation.Value ?? 1L;

                var increment = GetAndRemove<int?>(annotations, SqlServerAnnotationNames.IdentityIncrement)
                    ?? model.FindAnnotation(SqlServerAnnotationNames.IdentityIncrement)?.Value as int?
                    ?? 1;
                return new MethodCallCodeFragment(
                    onModel
                        ? ModelUseIdentityColumnsMethodInfo
                        : complexType
                            ? ComplexTypePropertyUseIdentityColumnsMethodInfo
                            : PropertyUseIdentityColumnsMethodInfo,
                    (seed, increment) switch
                    {
                        (1L, 1) => [],
                        (_, 1) => [seed],
                        _ => [seed, increment]
                    });

            case SqlServerValueGenerationStrategy.SequenceHiLo:
            {
                var name = GetAndRemove<string>(annotations, SqlServerAnnotationNames.HiLoSequenceName);
                var schema = GetAndRemove<string>(annotations, SqlServerAnnotationNames.HiLoSequenceSchema);
                return new MethodCallCodeFragment(
                    onModel
                        ? ModelUseHiLoMethodInfo
                        : complexType
                            ? ComplexTypePropertyUseHiLoMethodInfo
                            : PropertyUseHiLoMethodInfo,
                    (name, schema) switch
                    {
                        (null, null) => [],
                        (_, null) => [name],
                        _ => [name!, schema]
                    });
            }

            case SqlServerValueGenerationStrategy.Sequence:
            {
                var nameOrSuffix = GetAndRemove<string>(
                    annotations,
                    onModel ? SqlServerAnnotationNames.SequenceNameSuffix : SqlServerAnnotationNames.SequenceName);

                var schema = GetAndRemove<string>(annotations, SqlServerAnnotationNames.SequenceSchema);
                return new MethodCallCodeFragment(
                    onModel
                        ? ModelUseKeySequencesMethodInfo
                        : complexType
                            ? ComplexTypePropertyUseSequenceMethodInfo
                            : PropertyUseSequenceMethodInfo,
                    (name: nameOrSuffix, schema) switch
                    {
                        (null, null) => [],
                        (_, null) => [nameOrSuffix],
                        _ => [nameOrSuffix!, schema]
                    });
            }

            case SqlServerValueGenerationStrategy.None:
                return new MethodCallCodeFragment(
                    ModelHasAnnotationMethodInfo,
                    SqlServerAnnotationNames.ValueGenerationStrategy,
                    SqlServerValueGenerationStrategy.None);

            default:
                throw new ArgumentOutOfRangeException();
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private static MethodCallCodeFragment? GenerateValueGenerationStrategy(
        IDictionary<string, IAnnotation> annotations,
        IModel model,
        bool onModel,
        bool complexType)
    {
        SqlServerValueGenerationStrategy strategy;
        if (annotations.TryGetValue(SqlServerAnnotationNames.ValueGenerationStrategy, out var strategyAnnotation)
            && strategyAnnotation.Value != null)
        {
            annotations.Remove(SqlServerAnnotationNames.ValueGenerationStrategy);
            strategy = (SqlServerValueGenerationStrategy)strategyAnnotation.Value;
        }
        else
        {
            return null;
        }

        switch (strategy)
        {
            case SqlServerValueGenerationStrategy.IdentityColumn:
                // Support pre-6.0 IdentitySeed annotations, which contained an int rather than a long
                if (annotations.TryGetValue(SqlServerAnnotationNames.IdentitySeed, out var seedAnnotation)
                    && seedAnnotation.Value != null)
                {
                    annotations.Remove(SqlServerAnnotationNames.IdentitySeed);
                }
                else
                {
                    seedAnnotation = model.FindAnnotation(SqlServerAnnotationNames.IdentitySeed);
                }

                var seed = seedAnnotation is null
                    ? 1L
                    : seedAnnotation.Value is int intValue
                        ? intValue
                        : (long?)seedAnnotation.Value ?? 1L;

                var increment = GetAndRemove<int?>(annotations, SqlServerAnnotationNames.IdentityIncrement)
                    ?? model.FindAnnotation(SqlServerAnnotationNames.IdentityIncrement)?.Value as int?
                    ?? 1;
                return new MethodCallCodeFragment(
                    onModel
                        ? ModelUseIdentityColumnsMethodInfo
                        : complexType
                            ? ComplexTypePropertyUseIdentityColumnsMethodInfo
                            : PropertyUseIdentityColumnsMethodInfo,
                    (seed, increment) switch
                    {
                        (1L, 1) => [],
                        (_, 1) => [seed],
                        _ => [seed, increment]
                    });

            case SqlServerValueGenerationStrategy.SequenceHiLo:
            {
                var name = GetAndRemove<string>(annotations, SqlServerAnnotationNames.HiLoSequenceName)
                    ?? (onModel ? null : model.GetHiLoSequenceName());
                var schema = GetAndRemove<string>(annotations, SqlServerAnnotationNames.HiLoSequenceSchema)
                    ?? (onModel ? null : model.GetHiLoSequenceSchema());
                return new MethodCallCodeFragment(
                    onModel
                        ? ModelUseHiLoMethodInfo
                        : complexType
                            ? ComplexTypePropertyUseHiLoMethodInfo
                            : PropertyUseHiLoMethodInfo,
                    (name, schema) switch
                    {
                        (null, null) => [],
                        (_, null) => [name],
                        _ => [name!, schema]
                    });
            }

            case SqlServerValueGenerationStrategy.Sequence:
            {
                var nameOrSuffix = GetAndRemove<string>(
                    annotations,
                    onModel ? SqlServerAnnotationNames.SequenceNameSuffix : SqlServerAnnotationNames.SequenceName);

                var schema = GetAndRemove<string>(annotations, SqlServerAnnotationNames.SequenceSchema);
                return new MethodCallCodeFragment(
                    onModel
                        ? ModelUseKeySequencesMethodInfo
                        : complexType
                            ? ComplexTypePropertyUseSequenceMethodInfo
                            : PropertyUseSequenceMethodInfo,
                    (name: nameOrSuffix, schema) switch
                    {
                        (null, null) => [],
                        (_, null) => [nameOrSuffix],
                        _ => [nameOrSuffix!, schema]
                    });
            }

            case SqlServerValueGenerationStrategy.None:
                return new MethodCallCodeFragment(
                    ModelHasAnnotationMethodInfo,
                    SqlServerAnnotationNames.ValueGenerationStrategy,
                    SqlServerValueGenerationStrategy.None);

            default:
                throw new ArgumentOutOfRangeException();
        }
    }
```


---

### 🔹 Commit #02: `98af6078`
- **完整 Hash**: `98af60784eb48578d2a3be4e5a5f47550b9a3460`
- **說明 (Ground Truth)**: Fix Not on bool? and Increment/Decrement on non-int types in LinqToCSharpSyntaxTranslator(#39230)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.Design/Query/Internal/LinqToCSharpSyntaxTranslator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:463, E:707, A:0) ➔ After(N:468, E:712, A:0)
- **差分統計**: +Nodes: 11, -Nodes: 6, +Edges: 8, -Edges: 3, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Convert.ChangeType (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `unary.Type.UnwrapNullableType (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_3134` (MODULE_STATE)
  • + [新增節點] `state_3135` (MODULE_STATE)
  • + [新增節點] `LinqToCSharpSyntaxTranslator.IncrementOrDecrement` (FUNCTION_DEF)
  • + [新增節點] `Expression.Convert (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_3157` (MODULE_STATE)
  • + [新增節點] `Expression.MakeBinary (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_3189` (MODULE_STATE)
  • + [新增節點] `type.IsNullableType (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `type.UnwrapNullableType (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `state_3118` (MODULE_STATE)
  • - [移除節點] `state_3172` (MODULE_STATE)
  • - [移除節點] `state_3140` (MODULE_STATE)
  • - [移除節點] `Expression.Add (External/BCL)` (FUNCTION_DEF)
  • _... 以及其餘 13 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `LinqToCSharpSyntaxTranslator.VisitUnary()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.VisitUnary(UnaryExpression unary)` (L2599~L2646)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.VisitUnary(UnaryExpression unary)` (L2599~L2663)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override Expression VisitUnary(UnaryExpression unary)
    {
        if (unary.Method is not null
            && !unary.Method.IsHideBySig
            && !unary.Method.IsSpecialName
            && unary.Method.Name != "op_Implicit"
            && unary.Method.Name != "op_Explicit")
        {
            throw new NotImplementedException("Unary node with non-null method");
        }

        using var _ = ChangeContext(ExpressionContext.Expression);

        var operand = Translate<ExpressionSyntax>(unary.Operand);

        // TODO: Confirm what to do with the checked expression types

        Result = unary.NodeType switch
        {
            ExpressionType.Negate => _g.NegateExpression(operand),
            ExpressionType.NegateChecked => _g.NegateExpression(operand),
            ExpressionType.Not when unary.Type == typeof(bool) => _g.LogicalNotExpression(operand),
            ExpressionType.Not => _g.BitwiseNotExpression(operand),
            ExpressionType.OnesComplement => _g.BitwiseNotExpression(operand),
            ExpressionType.IsFalse => _g.LogicalNotExpression(operand),
            ExpressionType.IsTrue => operand,
            ExpressionType.ArrayLength => _g.MemberAccessExpression(operand, "Length"),
            ExpressionType.Convert => ParenthesizedExpression((ExpressionSyntax)_g.ConvertExpression(Generate(unary.Type), operand)),
            ExpressionType.ConvertChecked =>
                ParenthesizedExpression((ExpressionSyntax)_g.ConvertExpression(Generate(unary.Type), operand)),
            ExpressionType.Throw when unary.Type == typeof(void) => _g.ThrowStatement(operand),
            ExpressionType.Throw => _g.ThrowExpression(operand),
            ExpressionType.TypeAs => BinaryExpression(SyntaxKind.AsExpression, operand, Generate(unary.Type)),
            ExpressionType.Quote => operand,
            ExpressionType.UnaryPlus => PrefixUnaryExpression(SyntaxKind.UnaryPlusExpression, operand),
            ExpressionType.Unbox => operand,
            ExpressionType.Increment => Translate(Expression.Add(unary.Operand, Expression.Constant(1))),
            ExpressionType.Decrement => Translate(Expression.Subtract(unary.Operand, Expression.Constant(1))),
            ExpressionType.PostIncrementAssign => PostfixUnaryExpression(SyntaxKind.PostIncrementExpression, operand),
            ExpressionType.PostDecrementAssign => PostfixUnaryExpression(SyntaxKind.PostDecrementExpression, operand),
            ExpressionType.PreIncrementAssign => PrefixUnaryExpression(SyntaxKind.PreIncrementExpression, operand),
            ExpressionType.PreDecrementAssign => PrefixUnaryExpression(SyntaxKind.PreDecrementExpression, operand),

            _ => throw new ArgumentOutOfRangeException("Unsupported LINQ unary node: " + unary.NodeType)
        };

        return unary;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override Expression VisitUnary(UnaryExpression unary)
    {
        if (unary.Method is not null
            && !unary.Method.IsHideBySig
            && !unary.Method.IsSpecialName
            && unary.Method.Name != "op_Implicit"
            && unary.Method.Name != "op_Explicit")
        {
            throw new NotImplementedException("Unary node with non-null method");
        }

        using var _ = ChangeContext(ExpressionContext.Expression);

        var operand = Translate<ExpressionSyntax>(unary.Operand);

        // TODO: Confirm what to do with the checked expression types

        Result = unary.NodeType switch
        {
            ExpressionType.Negate => _g.NegateExpression(operand),
            ExpressionType.NegateChecked => _g.NegateExpression(operand),
            ExpressionType.Not when unary.Type.UnwrapNullableType() == typeof(bool) => _g.LogicalNotExpression(operand),
            ExpressionType.Not => _g.BitwiseNotExpression(operand),
            ExpressionType.OnesComplement => _g.BitwiseNotExpression(operand),
            ExpressionType.IsFalse => _g.LogicalNotExpression(operand),
            ExpressionType.IsTrue => operand,
            ExpressionType.ArrayLength => _g.MemberAccessExpression(operand, "Length"),
            ExpressionType.Convert => ParenthesizedExpression((ExpressionSyntax)_g.ConvertExpression(Generate(unary.Type), operand)),
            ExpressionType.ConvertChecked =>
                ParenthesizedExpression((ExpressionSyntax)_g.ConvertExpression(Generate(unary.Type), operand)),
            ExpressionType.Throw when unary.Type == typeof(void) => _g.ThrowStatement(operand),
            ExpressionType.Throw => _g.ThrowExpression(operand),
            ExpressionType.TypeAs => BinaryExpression(SyntaxKind.AsExpression, operand, Generate(unary.Type)),
            ExpressionType.Quote => operand,
            ExpressionType.UnaryPlus => PrefixUnaryExpression(SyntaxKind.UnaryPlusExpression, operand),
            ExpressionType.Unbox => operand,
            ExpressionType.Increment => Translate(IncrementOrDecrement(ExpressionType.Add, unary.Operand)),
            ExpressionType.Decrement => Translate(IncrementOrDecrement(ExpressionType.Subtract, unary.Operand)),
            ExpressionType.PostIncrementAssign => PostfixUnaryExpression(SyntaxKind.PostIncrementExpression, operand),
            ExpressionType.PostDecrementAssign => PostfixUnaryExpression(SyntaxKind.PostDecrementExpression, operand),
            ExpressionType.PreIncrementAssign => PrefixUnaryExpression(SyntaxKind.PreIncrementExpression, operand),
            ExpressionType.PreDecrementAssign => PrefixUnaryExpression(SyntaxKind.PreDecrementExpression, operand),

            _ => throw new ArgumentOutOfRangeException("Unsupported LINQ unary node: " + unary.NodeType)
        };

        return unary;

        // C# promotes short/ushort arithmetic to int, so compute in int and convert back to keep the expression's type
        static Expression IncrementOrDecrement(ExpressionType binaryType, Expression operand)
        {
            var type = operand.Type;
            if (type.UnwrapNullableType() is var underlyingType && (underlyingType == typeof(short) || underlyingType == typeof(ushort)))
            {
                var promotedType = type.IsNullableType() ? typeof(int?) : typeof(int);

                return Expression.Convert(
                    Expression.MakeBinary(binaryType, Expression.Convert(operand, promotedType), Expression.Constant(1, promotedType)),
                    type);
            }

            return Expression.MakeBinary(
                binaryType, operand, Expression.Constant(Convert.ChangeType(1, underlyingType, CultureInfo.InvariantCulture), type));
        }
    }
```


---

### 🔹 Commit #03: `eae5924d`
- **完整 Hash**: `eae5924d7949de6cd29fa0b9d83287011a1c745c`
- **說明 (Ground Truth)**: Keep fractional seconds in SQL Server TimeSpan literals (#39229)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.SqlServer/Storage/Internal/SqlServerTimeSpanTypeMapping.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:7, E:2, A:0) ➔ After(N:9, E:4, A:0)
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
  • + [新增節點] `Math.Abs (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `Math.Pow (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `SqlServerTimeSpanTypeMapping.GenerateNonNullSqlLiteral` ──[CALLS]──> `Math.Abs (External/BCL)`
  • + [新增呼叫邊] `SqlServerTimeSpanTypeMapping.GenerateNonNullSqlLiteral` ──[CALLS]──> `Math.Pow (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SqlServerTimeSpanTypeMapping.GenerateNonNullSqlLiteral()`
- **變更前簽章 (Before)**: `SqlServerTimeSpanTypeMapping.GenerateNonNullSqlLiteral(object value)` (L117~L120)
- **變更後簽章 (After)**: `SqlServerTimeSpanTypeMapping.GenerateNonNullSqlLiteral(object value)` (L117~L136)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override string GenerateNonNullSqlLiteral(object value)
        => value is TimeSpan { Milliseconds: 0 } // Handle trailing decimal separator when no fractional seconds
            ? string.Format(CultureInfo.InvariantCulture, _timeFormats[0], value)
            : string.Format(CultureInfo.InvariantCulture, SqlLiteralFormatString, value);
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override string GenerateNonNullSqlLiteral(object value)
    {
        // A value converter on the mapping may produce a provider value that isn't a TimeSpan
        if (value is not TimeSpan timeSpan)
        {
            return string.Format(CultureInfo.InvariantCulture, SqlLiteralFormatString, value);
        }

        var precision = Precision is >= 0 and <= 7 ? Precision.Value : 7;

        // The F format specifiers omit trailing zeros, so when no fractional digit is left at this precision the literal would end
        // with a decimal separator, which SQL Server rejects.
        var fractionTicks = Math.Abs(timeSpan.Ticks % TimeSpan.TicksPerSecond);
        var ticksPerDigit = TimeSpan.TicksPerSecond / (long)Math.Pow(10, precision);

        return string.Format(
            CultureInfo.InvariantCulture,
            fractionTicks < ticksPerDigit ? _timeFormats[0] : _timeFormats[precision],
            value);
    }
```


---

### 🔹 Commit #04: `419434f3`
- **完整 Hash**: `419434f328a9579f335b35dea1f857b7e5f49b04`
- **說明 (Ground Truth)**: Fix select concat (#39269)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore/Query/QueryRootProcessor.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:26, E:26, A:0) ➔ After(N:26, E:26, A:0)
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

### 🔹 函式: `QueryRootProcessor.VisitQueryRootCandidate()`
- **變更前簽章 (Before)**: `QueryRootProcessor.VisitQueryRootCandidate(Expression expression, Type elementClrType)` (L84~L152)
- **變更後簽章 (After)**: `QueryRootProcessor.VisitQueryRootCandidate(Expression expression, Type elementClrType)` (L84~L152)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private Expression VisitQueryRootCandidate(Expression expression, Type elementClrType)
    {
        // A:
        // In case the collection was value type, in order to call methods like AsQueryable,
        // we need to convert it to IEnumerable<T> which requires boxing.
        // We do that with Convert expression which we need to unwrap here.
        //
        // B:
        // For collections that are abstract (i.e. FrozenSet<T>), some internal type is used
        // and for readonly fields the compiler adds explicit cast. We need to unwrap here.
        if (expression is UnaryExpression { NodeType: ExpressionType.Convert } convertExpression
            && convertExpression.Type.IsAssignableTo(typeof(IEnumerable)))
        {
            return VisitQueryRootCandidate(convertExpression.Operand, elementClrType);
        }

        switch (expression)
        {
            // An array containing only constants is represented as a ConstantExpression with the array as the value.
            // Convert that into a NewArrayExpression for use with InlineQueryRootExpression.
            case ConstantExpression { Value: IEnumerable values }:
                var valueExpressions = new List<ConstantExpression>();

                Type? valueClrType = null;
                foreach (var value in values)
                {
                    var valueToAdd = value;

                    if (value is not null)
                    {
                        valueClrType ??= value.GetType();
                        // Enums are implicitly castable to/from the underlying type
                        // hence calling i.e. LINQ Cast<T> to underlying type
                        // does not have to do anything and return the enum array.
                        // But when expanding the constants, we need to change the type,
                        // otherwise the type of value for the Expression.Constant
                        // would not be the expected type and fail.
                        if (valueClrType != elementClrType.UnwrapNullableType() && valueClrType.IsEnum)
                        {
                            valueToAdd = Convert.ChangeType(value, elementClrType);
                        }
                    }

                    valueExpressions.Add(Expression.Constant(valueToAdd, elementClrType));
                }

                if (ShouldConvertToInlineQueryRoot(Expression.NewArrayInit(elementClrType, valueExpressions)))
                {
                    return new InlineQueryRootExpression(valueExpressions, elementClrType);
                }

                goto default;

            case NewArrayExpression newArray when ShouldConvertToInlineQueryRoot(newArray):
                return new InlineQueryRootExpression(newArray.Expressions, elementClrType);

            case QueryParameterExpression queryParameter when ShouldConvertToParameterQueryRoot(queryParameter):
                return new ParameterQueryRootExpression(queryParameter.Type.GetSequenceType(), queryParameter);

            case ListInitExpression listInit
                when listInit.Type.TryGetElementType(typeof(IList<>)) is not null
                && listInit.Initializers.All(x => x.Arguments.Count == 1)
                && ShouldConvertToInlineQueryRoot(listInit):
                return new InlineQueryRootExpression(listInit.Initializers.Select(x => x.Arguments[0]).ToList(), elementClrType);

            default:
                return Visit(expression);
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private Expression VisitQueryRootCandidate(Expression expression, Type elementClrType)
    {
        // A:
        // In case the collection was value type, in order to call methods like AsQueryable,
        // we need to convert it to IEnumerable<T> which requires boxing.
        // We do that with Convert expression which we need to unwrap here.
        //
        // B:
        // For collections that are abstract (i.e. FrozenSet<T>), some internal type is used
        // and for readonly fields the compiler adds explicit cast. We need to unwrap here.
        if (expression is UnaryExpression { NodeType: ExpressionType.Convert } convertExpression
            && convertExpression.Type.IsAssignableTo(typeof(IEnumerable)))
        {
            return VisitQueryRootCandidate(convertExpression.Operand, elementClrType);
        }

        switch (expression)
        {
            // An array containing only constants is represented as a ConstantExpression with the array as the value.
            // Convert that into a NewArrayExpression for use with InlineQueryRootExpression.
            case ConstantExpression { Value: IEnumerable values and not string }:
                var valueExpressions = new List<ConstantExpression>();

                Type? valueClrType = null;
                foreach (var value in values)
                {
                    var valueToAdd = value;

                    if (value is not null)
                    {
                        valueClrType ??= value.GetType();
                        // Enums are implicitly castable to/from the underlying type
                        // hence calling i.e. LINQ Cast<T> to underlying type
                        // does not have to do anything and return the enum array.
                        // But when expanding the constants, we need to change the type,
                        // otherwise the type of value for the Expression.Constant
                        // would not be the expected type and fail.
                        if (valueClrType != elementClrType.UnwrapNullableType() && valueClrType.IsEnum)
                        {
                            valueToAdd = Convert.ChangeType(value, elementClrType);
                        }
                    }

                    valueExpressions.Add(Expression.Constant(valueToAdd, elementClrType));
                }

                if (ShouldConvertToInlineQueryRoot(Expression.NewArrayInit(elementClrType, valueExpressions)))
                {
                    return new InlineQueryRootExpression(valueExpressions, elementClrType);
                }

                goto default;

            case NewArrayExpression newArray when ShouldConvertToInlineQueryRoot(newArray):
                return new InlineQueryRootExpression(newArray.Expressions, elementClrType);

            case QueryParameterExpression queryParameter when ShouldConvertToParameterQueryRoot(queryParameter) && queryParameter.Type != typeof(string):
                return new ParameterQueryRootExpression(queryParameter.Type.GetSequenceType(), queryParameter);

            case ListInitExpression listInit
                when listInit.Type.TryGetElementType(typeof(IList<>)) is not null
                && listInit.Initializers.All(x => x.Arguments.Count == 1)
                && ShouldConvertToInlineQueryRoot(listInit):
                return new InlineQueryRootExpression(listInit.Initializers.Select(x => x.Arguments[0]).ToList(), elementClrType);

            default:
                return Visit(expression);
        }
    }
```


---

### 🔹 Commit #05: `b95ca253`
- **完整 Hash**: `b95ca2532862f8b115943e24d7e8d235be8a0967`
- **說明 (Ground Truth)**: Fix TODATETIMEOFFSET translation in projection (#39223)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.Relational/Query/Internal/RelationalProjectionBindingExpressionVisitor.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:124, E:170, A:0) ➔ After(N:125, E:171, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 1, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_971` (MODULE_STATE)
  • + [新增節點] `RelationalProjectionBindingExpressionVisitor.AddExplicitConvertIfNeeded` (FUNCTION_DEF)
  • - [移除節點] `state_966` (MODULE_STATE)
  • + [新增呼叫邊] `RelationalProjectionBindingExpressionVisitor.Visit` ──[CALLS]──> `RelationalProjectionBindingExpressionVisitor.AddExplicitConvertIfNeeded`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RelationalProjectionBindingExpressionVisitor.Visit()`
- **變更前簽章 (Before)**: `RelationalProjectionBindingExpressionVisitor.Visit(Expression? expression)` (L188~L374)
- **變更後簽章 (After)**: `RelationalProjectionBindingExpressionVisitor.Visit(Expression? expression)` (L188~L367)

#### ◀️ 變更前實作碼 (Before Implementation):
```
[return: NotNullIfNotNull(nameof(expression))]
    public override Expression? Visit(Expression? expression)
    {
        switch (expression)
        {
            case NewExpression or MemberInitExpression or StructuralTypeShaperExpression or IncludeExpression:
                return base.Visit(expression);

            case null:
                return null;

            case not null when _indexBasedBinding:
            {
                switch (expression)
                {
                    case ConstantExpression:
                        return expression;

                    case QueryParameterExpression queryParameterExpression:
                        return Expression.Call(
                            GetParameterValueMethodInfo.MakeGenericMethod(queryParameterExpression.Type),
                            QueryCompilationContext.QueryContextParameter,
                            Expression.Constant(queryParameterExpression.Name));

                    case ParameterExpression parameterExpression:
                        throw new InvalidOperationException(CoreStrings.TranslationFailed(parameterExpression.Print()));

                    case ProjectionBindingExpression projectionBindingExpression:
                        return _selectExpression.GetProjection(projectionBindingExpression) switch
                        {
                            StructuralTypeProjectionExpression projection => AddClientProjection(projection, typeof(ValueBuffer)),
                            SqlExpression mappedSqlExpression => AddClientProjection(mappedSqlExpression, expression.Type.MakeNullable()),
                            // A single-result subquery (e.g. the group element of GroupBy(k).Select(g => g.First()))
                            // being composed over: lower it into the current select as a to-one join so the result
                            // has a bindable shape, instead of failing.
                            ShapedQueryExpression
                            {
                                ResultCardinality: ResultCardinality.Single or ResultCardinality.SingleOrDefault
                            } singleResultSubquery
                                => LowerSingleResultSubquery(projectionBindingExpression, singleResultSubquery),
                            _ => throw new InvalidOperationException(CoreStrings.TranslationFailed(projectionBindingExpression.Print()))
                        };

                    case MaterializeCollectionNavigationExpression materializeCollectionNavigationExpression:
                        if (materializeCollectionNavigationExpression.Navigation.TargetEntityType.IsMappedToJson())
                        {
                            var subquery = materializeCollectionNavigationExpression.Subquery;
                            if (subquery is MethodCallExpression { Method.IsGenericMethod: true } methodCallSubquery)
                            {
                                // strip .Select(x => x) and .AsQueryable() from the JsonCollectionResultExpression
                                if (methodCallSubquery.Method.GetGenericMethodDefinition() == QueryableMethods.Select
                                    && methodCallSubquery.Arguments[0] is MethodCallExpression selectSourceMethod)
                                {
                                    methodCallSubquery = selectSourceMethod;
                                }

                                if (methodCallSubquery.Method.IsGenericMethod
                                    && methodCallSubquery.Method.GetGenericMethodDefinition() == QueryableMethods.AsQueryable)
                                {
                                    subquery = methodCallSubquery.Arguments[0];
                                }
                            }

                            if (subquery is JsonQueryExpression jsonQueryExpression)
                            {
                                Check.DebugAssert(
                                    jsonQueryExpression.IsCollection,
                                    "JsonQueryExpression inside materialize collection should always be a collection.");

                                _clientProjections!.Add(jsonQueryExpression);

                                return new CollectionResultExpression(
                                    new ProjectionBindingExpression(
                                        _selectExpression, _clientProjections!.Count - 1, jsonQueryExpression.Type),
                                    materializeCollectionNavigationExpression.Navigation,
                                    materializeCollectionNavigationExpression.Navigation.ClrType.GetSequenceType());
                            }
                        }

                        _clientProjections!.Add(
                            _queryableMethodTranslatingExpressionVisitor.TranslateSubquery(
                                materializeCollectionNavigationExpression.Subquery)!);

                        return new CollectionResultExpression(
                            // expression.Type will be CLR type of the navigation here so that is fine.
                            new ProjectionBindingExpression(_selectExpression, _clientProjections.Count - 1, expression.Type),
                            materializeCollectionNavigationExpression.Navigation,
                            materializeCollectionNavigationExpression.Navigation.ClrType.GetSequenceType());
                }

                switch (_sqlTranslator.TranslateProjection(expression))
                {
                    case SqlExpression sqlExpression:
                        return AddClientProjection(sqlExpression, expression.Type.MakeNullable());

                    // This handles the case of a complex type being projected out of a Select.
                    case RelationalStructuralTypeShaperExpression { StructuralType: IComplexType } shaper:
                        return base.Visit(shaper);

                    case CollectionResultExpression collectionResult:
                        return base.Visit(collectionResult);
                }

                if (expression is MethodCallExpression methodCallExpression)
                {
                    if (methodCallExpression is
                        {
                            Method.IsGenericMethod: true,
                            Method.Name: nameof(Enumerable.ToList),
                            Method: var method,
                            Arguments: [var argument]
                        }
                        && method.DeclaringType == typeof(Enumerable)
                        && argument.Type.TryGetElementType(typeof(IQueryable<>)) != null)
                    {
                        if (_queryableMethodTranslatingExpressionVisitor.TranslateSubquery(argument) is { } subquery)
                        {
                            _clientProjections!.Add(subquery);
                            // expression.Type here will be List<T>
                            return new CollectionResultExpression(
                                new ProjectionBindingExpression(_selectExpression, _clientProjections.Count - 1, expression.Type),
                                structuralProperty: null,
                                methodCallExpression.Method.GetGenericArguments()[0]);
                        }
                    }
                    else
                    {
                        var subquery = _queryableMethodTranslatingExpressionVisitor.TranslateSubquery(methodCallExpression);
                        if (subquery != null)
                        {
                            _clientProjections!.Add(subquery);
                            var type = expression.Type;
                            if (type.IsGenericType
                                && type.GetGenericTypeDefinition() == typeof(IQueryable<>))
                            {
                                type = typeof(List<>).MakeGenericType(type.GetSequenceType());
                            }

                            var projectionBindingExpression = new ProjectionBindingExpression(
                                _selectExpression, _clientProjections.Count - 1, type);
                            return subquery.ResultCardinality == ResultCardinality.Enumerable
                                ? new CollectionResultExpression(
                                    projectionBindingExpression, structuralProperty: null, subquery.ShaperExpression.Type)
                                : projectionBindingExpression;
                        }
                    }
                }

                return base.Visit(expression);
            }

            default:
            {
                switch (_sqlTranslator.TranslateProjection(expression))
                {
                    case SqlExpression sqlExpression:
                        if (sqlExpression is SqlConstantExpression { Value: not null }
                            && (sqlExpression.Type == typeof(Guid)
                                || sqlExpression.Type == typeof(DateTime)
                                || sqlExpression.Type == typeof(DateOnly)
                                || sqlExpression.Type == typeof(TimeOnly)
                                || sqlExpression.Type == typeof(TimeSpan)
                                || sqlExpression.Type == typeof(DateTimeOffset)))
                        {
                            sqlExpression = new SqlUnaryExpression(ExpressionType.Convert, sqlExpression, sqlExpression.Type, sqlExpression.TypeMapping);
                        }
                        _projectionMapping[_projectionMembers.Peek()] = sqlExpression;
                        return new ProjectionBindingExpression(
                            _selectExpression, _projectionMembers.Peek(), expression.Type.MakeNullable());

                    // This handles the case of a complex type being projected out of a Select.
                    // Note that an entity type being projected is (currently) handled differently
                    case RelationalStructuralTypeShaperExpression { StructuralType: IComplexType } shaper:
                        return base.Visit(shaper);

                    case CollectionResultExpression collectionResult:
                        return base.Visit(collectionResult);

                    case null or RelationalStructuralTypeShaperExpression { StructuralType: IEntityType }:
                        return QueryCompilationContext.NotTranslatedExpression;

                    default:
                        throw new UnreachableException();
                }
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
[return: NotNullIfNotNull(nameof(expression))]
    public override Expression? Visit(Expression? expression)
    {
        switch (expression)
        {
            case MemberInitExpression or StructuralTypeShaperExpression or IncludeExpression:
            case NewExpression newExpression when !_indexBasedBinding || newExpression.Arguments.Count == 0:
                return base.Visit(expression);

            case null:
                return null;

            case not null when _indexBasedBinding:
            {
                switch (expression)
                {
                    case ConstantExpression:
                        return expression;

                    case QueryParameterExpression queryParameterExpression:
                        return Expression.Call(
                            GetParameterValueMethodInfo.MakeGenericMethod(queryParameterExpression.Type),
                            QueryCompilationContext.QueryContextParameter,
                            Expression.Constant(queryParameterExpression.Name));

                    case ParameterExpression parameterExpression:
                        throw new InvalidOperationException(CoreStrings.TranslationFailed(parameterExpression.Print()));

                    case ProjectionBindingExpression projectionBindingExpression:
                        return _selectExpression.GetProjection(projectionBindingExpression) switch
                        {
                            StructuralTypeProjectionExpression projection => AddClientProjection(projection, typeof(ValueBuffer)),
                            SqlExpression mappedSqlExpression => AddClientProjection(mappedSqlExpression, expression.Type.MakeNullable()),
                            // A single-result subquery (e.g. the group element of GroupBy(k).Select(g => g.First()))
                            // being composed over: lower it into the current select as a to-one join so the result
                            // has a bindable shape, instead of failing.
                            ShapedQueryExpression
                            {
                                ResultCardinality: ResultCardinality.Single or ResultCardinality.SingleOrDefault
                            } singleResultSubquery
                                => LowerSingleResultSubquery(projectionBindingExpression, singleResultSubquery),
                            _ => throw new InvalidOperationException(CoreStrings.TranslationFailed(projectionBindingExpression.Print()))
                        };

                    case MaterializeCollectionNavigationExpression materializeCollectionNavigationExpression:
                        if (materializeCollectionNavigationExpression.Navigation.TargetEntityType.IsMappedToJson())
                        {
                            var subquery = materializeCollectionNavigationExpression.Subquery;
                            if (subquery is MethodCallExpression { Method.IsGenericMethod: true } methodCallSubquery)
                            {
                                // strip .Select(x => x) and .AsQueryable() from the JsonCollectionResultExpression
                                if (methodCallSubquery.Method.GetGenericMethodDefinition() == QueryableMethods.Select
                                    && methodCallSubquery.Arguments[0] is MethodCallExpression selectSourceMethod)
                                {
                                    methodCallSubquery = selectSourceMethod;
                                }

                                if (methodCallSubquery.Method.IsGenericMethod
                                    && methodCallSubquery.Method.GetGenericMethodDefinition() == QueryableMethods.AsQueryable)
                                {
                                    subquery = methodCallSubquery.Arguments[0];
                                }
                            }

                            if (subquery is JsonQueryExpression jsonQueryExpression)
                            {
                                Check.DebugAssert(
                                    jsonQueryExpression.IsCollection,
                                    "JsonQueryExpression inside materialize collection should always be a collection.");

                                _clientProjections!.Add(jsonQueryExpression);

                                return new CollectionResultExpression(
                                    new ProjectionBindingExpression(
                                        _selectExpression, _clientProjections!.Count - 1, jsonQueryExpression.Type),
                                    materializeCollectionNavigationExpression.Navigation,
                                    materializeCollectionNavigationExpression.Navigation.ClrType.GetSequenceType());
                            }
                        }

                        _clientProjections!.Add(
                            _queryableMethodTranslatingExpressionVisitor.TranslateSubquery(
                                materializeCollectionNavigationExpression.Subquery)!);

                        return new CollectionResultExpression(
                            // expression.Type will be CLR type of the navigation here so that is fine.
                            new ProjectionBindingExpression(_selectExpression, _clientProjections.Count - 1, expression.Type),
                            materializeCollectionNavigationExpression.Navigation,
                            materializeCollectionNavigationExpression.Navigation.ClrType.GetSequenceType());
                }

                switch (_sqlTranslator.TranslateProjection(expression))
                {
                    case SqlExpression sqlExpression:
                        sqlExpression = AddExplicitConvertIfNeeded(sqlExpression);
                        return AddClientProjection(sqlExpression, expression.Type.MakeNullable());

                    // This handles the case of a complex type being projected out of a Select.
                    case RelationalStructuralTypeShaperExpression { StructuralType: IComplexType } shaper:
                        return base.Visit(shaper);

                    case CollectionResultExpression collectionResult:
                        return base.Visit(collectionResult);
                }

                if (expression is MethodCallExpression methodCallExpression)
                {
                    if (methodCallExpression is
                        {
                            Method.IsGenericMethod: true,
                            Method.Name: nameof(Enumerable.ToList),
                            Method: var method,
                            Arguments: [var argument]
                        }
                        && method.DeclaringType == typeof(Enumerable)
                        && argument.Type.TryGetElementType(typeof(IQueryable<>)) != null)
                    {
                        if (_queryableMethodTranslatingExpressionVisitor.TranslateSubquery(argument) is { } subquery)
                        {
                            _clientProjections!.Add(subquery);
                            // expression.Type here will be List<T>
                            return new CollectionResultExpression(
                                new ProjectionBindingExpression(_selectExpression, _clientProjections.Count - 1, expression.Type),
                                structuralProperty: null,
                                methodCallExpression.Method.GetGenericArguments()[0]);
                        }
                    }
                    else
                    {
                        var subquery = _queryableMethodTranslatingExpressionVisitor.TranslateSubquery(methodCallExpression);
                        if (subquery != null)
                        {
                            _clientProjections!.Add(subquery);
                            var type = expression.Type;
                            if (type.IsGenericType
                                && type.GetGenericTypeDefinition() == typeof(IQueryable<>))
                            {
                                type = typeof(List<>).MakeGenericType(type.GetSequenceType());
                            }

                            var projectionBindingExpression = new ProjectionBindingExpression(
                                _selectExpression, _clientProjections.Count - 1, type);
                            return subquery.ResultCardinality == ResultCardinality.Enumerable
                                ? new CollectionResultExpression(
                                    projectionBindingExpression, structuralProperty: null, subquery.ShaperExpression.Type)
                                : projectionBindingExpression;
                        }
                    }
                }

                return base.Visit(expression);
            }

            default:
            {
                switch (_sqlTranslator.TranslateProjection(expression))
                {
                    case SqlExpression sqlExpression:
                        sqlExpression = AddExplicitConvertIfNeeded(sqlExpression);
                        _projectionMapping[_projectionMembers.Peek()] = sqlExpression;
                        return new ProjectionBindingExpression(
                            _selectExpression, _projectionMembers.Peek(), expression.Type.MakeNullable());

                    // This handles the case of a complex type being projected out of a Select.
                    // Note that an entity type being projected is (currently) handled differently
                    case RelationalStructuralTypeShaperExpression { StructuralType: IComplexType } shaper:
                        return base.Visit(shaper);

                    case CollectionResultExpression collectionResult:
                        return base.Visit(collectionResult);

                    case null or RelationalStructuralTypeShaperExpression { StructuralType: IEntityType }:
                        return QueryCompilationContext.NotTranslatedExpression;

                    default:
                        throw new UnreachableException();
                }
            }
        }
    }
```


---

### 🔹 Commit #06: `757e2d0b`
- **完整 Hash**: `757e2d0bc377142afc3f48df904cdf121f2b81ae`
- **說明 (Ground Truth)**: Query: translate GroupBy element reads with ROW_NUMBER only (#39173)
- **變更檔案數**: 2

#### 📄 檔案: `src/EFCore.Relational/Query/RelationalQueryableMethodTranslatingExpressionVisitor.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:361, E:505, A:0) ➔ After(N:398, E:573, A:0)
- **差分統計**: +Nodes: 47, -Nodes: 10, +Edges: 71, -Edges: 3, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `lambdaArgument.UnwrapLambdaFromQuote (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `element.UnwrapTypeConversion (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `orderings.Add (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `orderings.Any (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_2149` (MODULE_STATE)
  • + [新增節點] `visitor._columns.Any (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `navigation.TargetEntityType.IsMappedToJson (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `RelationalQueryableMethodTranslatingExpressionVisitor.TryTranslateGroupingElementRead` (FUNCTION_DEF)
  • + [新增節點] `_columns` (MODULE_STATE)
  • + [新增節點] `OuterReferenceFindingExpressionVisitor.Visit` (FUNCTION_DEF)
  • + [新增節點] `Orderings.Clear (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_1566` (MODULE_STATE)
  • + [新增節點] `GroupingElementReadAnalyzer.TryMatchElementRead` (FUNCTION_DEF)
  • + [新增節點] `state_2148` (MODULE_STATE)
  • + [新增節點] `predicate (External/BCL)` (FUNCTION_DEF)
  • _... 以及其餘 116 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RelationalQueryableMethodTranslatingExpressionVisitor.TranslateGroupBy()`
- **變更前簽章 (Before)**: `RelationalQueryableMethodTranslatingExpressionVisitor.TranslateGroupBy(
        ShapedQueryExpression source,
        LambdaExpression keySelector,
        LambdaExpression? elementSelector,
        LambdaExpression? resultSelector)` (L787~L845)
- **變更後簽章 (After)**: `RelationalQueryableMethodTranslatingExpressionVisitor.TranslateGroupBy(
        ShapedQueryExpression source,
        LambdaExpression keySelector,
        LambdaExpression? elementSelector,
        LambdaExpression? resultSelector)` (L787~L850)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override ShapedQueryExpression? TranslateGroupBy(
        ShapedQueryExpression source,
        LambdaExpression keySelector,
        LambdaExpression? elementSelector,
        LambdaExpression? resultSelector)
    {
        var selectExpression = (SelectExpression)source.QueryExpression;
        selectExpression.PrepareForAggregate();

        var remappedKeySelector = RemapLambdaBody(source, keySelector);
        var translatedKey = TranslateGroupingKey(remappedKeySelector);
        switch (translatedKey)
        {
            // Special handling for GroupBy over entity type: get the entity projection expression out.
            // For GroupBy over a complex type, we already get the projection expression out.
            case StructuralTypeShaperExpression { StructuralType: IEntityType } shaper:
                if (shaper.ValueBufferExpression is not ProjectionBindingExpression pbe)
                {
                    // ValueBufferExpression can be JsonQuery, ProjectionBindingExpression, EntityProjection
                    // We only allow ProjectionBindingExpression which represents a regular entity
                    return null;
                }

                translatedKey = shaper.Update(((SelectExpression)pbe.QueryExpression).GetProjection(pbe));
                break;

            case null:
                return null;
        }

        if (elementSelector != null)
        {
            source = TranslateSelect(source, elementSelector);
        }

        var groupByShaper = selectExpression.ApplyGrouping(translatedKey, source.ShaperExpression, _sqlExpressionFactory);
        if (resultSelector == null)
        {
            return source.UpdateShaperExpression(groupByShaper);
        }

        var original1 = resultSelector.Parameters[0];
        var original2 = resultSelector.Parameters[1];

        var newResultSelectorBody = new ReplacingExpressionVisitor(
                [original1, original2],
                [groupByShaper.KeySelector, groupByShaper])
            .Visit(resultSelector.Body);

        newResultSelectorBody = ExpandSharedTypeEntities(selectExpression, newResultSelectorBody);

        if (TryTranslateGroupingElementProjection(source, groupByShaper, newResultSelectorBody) is { } liftedGroupBy)
        {
            return liftedGroupBy;
        }

        return source.UpdateShaperExpression(
            _projectionBindingExpressionVisitor.Translate(selectExpression, newResultSelectorBody));
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override ShapedQueryExpression? TranslateGroupBy(
        ShapedQueryExpression source,
        LambdaExpression keySelector,
        LambdaExpression? elementSelector,
        LambdaExpression? resultSelector)
    {
        var selectExpression = (SelectExpression)source.QueryExpression;
        selectExpression.PrepareForAggregate();

        var remappedKeySelector = RemapLambdaBody(source, keySelector);
        var translatedKey = TranslateGroupingKey(remappedKeySelector);
        switch (translatedKey)
        {
            // Special handling for GroupBy over entity type: get the entity projection expression out.
            // For GroupBy over a complex type, we already get the projection expression out.
            case StructuralTypeShaperExpression { StructuralType: IEntityType } shaper:
                if (shaper.ValueBufferExpression is not ProjectionBindingExpression pbe)
                {
                    // ValueBufferExpression can be JsonQuery, ProjectionBindingExpression, EntityProjection
                    // We only allow ProjectionBindingExpression which represents a regular entity
                    return null;
                }

                translatedKey = shaper.Update(((SelectExpression)pbe.QueryExpression).GetProjection(pbe));
                break;

            case null:
                return null;
        }

        if (elementSelector != null)
        {
            source = TranslateSelect(source, elementSelector);
        }

        var groupByShaper = selectExpression.ApplyGrouping(translatedKey, source.ShaperExpression, _sqlExpressionFactory);
        if (resultSelector == null)
        {
            return source.UpdateShaperExpression(groupByShaper);
        }

        var original1 = resultSelector.Parameters[0];
        var original2 = resultSelector.Parameters[1];

        var newResultSelectorBody = new ReplacingExpressionVisitor(
                [original1, original2],
                [groupByShaper.KeySelector, groupByShaper])
            .Visit(resultSelector.Body);

        newResultSelectorBody = ExpandSharedTypeEntities(selectExpression, newResultSelectorBody);

        if (TryTranslateGroupingElementProjection(source, groupByShaper, newResultSelectorBody) is { } liftedGroupBy)
        {
            return liftedGroupBy;
        }

        if (TryTranslateGroupingElementRead(source, groupByShaper, newResultSelectorBody) is { } elementRead)
        {
            return elementRead;
        }

        return source.UpdateShaperExpression(
            _projectionBindingExpressionVisitor.Translate(selectExpression, newResultSelectorBody));
    }
```

### 🔹 函式: `RelationalQueryableMethodTranslatingExpressionVisitor.TranslateSelect()`
- **變更前簽章 (Before)**: `RelationalQueryableMethodTranslatingExpressionVisitor.TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)` (L1385~L1407)
- **變更後簽章 (After)**: `RelationalQueryableMethodTranslatingExpressionVisitor.TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)` (L1479~L1508)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override ShapedQueryExpression TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)
    {
        if (selector.Body == selector.Parameters[0])
        {
            return source;
        }

        var selectExpression = (SelectExpression)source.QueryExpression;
        if (selectExpression.IsDistinct)
        {
            selectExpression.PushdownIntoSubquery();
        }

        var newSelectorBody = RemapLambdaBody(source, selector);

        if (source.ShaperExpression is RelationalGroupByShaperExpression groupByShaper
            && TryTranslateGroupingElementProjection(source, groupByShaper, newSelectorBody) is { } liftedGroupBy)
        {
            return liftedGroupBy;
        }

        return source.UpdateShaperExpression(_projectionBindingExpressionVisitor.Translate(selectExpression, newSelectorBody));
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override ShapedQueryExpression TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)
    {
        if (selector.Body == selector.Parameters[0])
        {
            return source;
        }

        var selectExpression = (SelectExpression)source.QueryExpression;
        if (selectExpression.IsDistinct)
        {
            selectExpression.PushdownIntoSubquery();
        }

        var newSelectorBody = RemapLambdaBody(source, selector);

        if (source.ShaperExpression is RelationalGroupByShaperExpression groupByShaper)
        {
            if (TryTranslateGroupingElementProjection(source, groupByShaper, newSelectorBody) is { } liftedGroupBy)
            {
                return liftedGroupBy;
            }

            if (TryTranslateGroupingElementRead(source, groupByShaper, newSelectorBody) is { } elementRead)
            {
                return elementRead;
            }
        }

        return source.UpdateShaperExpression(_projectionBindingExpressionVisitor.Translate(selectExpression, newSelectorBody));
    }
```


#### 📄 檔案: `src/EFCore.Relational/Query/SqlExpressions/SelectExpression.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:535, E:770, A:0) ➔ After(N:541, E:786, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 1, +Edges: 17, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `identifier.Select (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `SelectExpression.ApplyFirstRowPerGroup` (FUNCTION_DEF)
  • + [新增節點] `SelectExpression.GetRowNumberOrderings` (FUNCTION_DEF)
  • + [新增節點] `state_3185` (MODULE_STATE)
  • + [新增節點] `identifier.Select(e => new OrderingExpression(e.Column, true)).ToList (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `sqlRemappingVisitor.Visit (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `sqlExpressionFactory.LessThanOrEqual (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `state_3140` (MODULE_STATE)
  • + [新增呼叫邊] `SelectExpression.ApplyFirstRowPerGroup` ──[CALLS]──> `Check.DebugAssert (External/BCL)`
  • + [新增呼叫邊] `SelectExpression.ApplyFirstRowPerGroup` ──[CALLS]──> `_groupBy.ToList (External/BCL)`
  • + [新增呼叫邊] `SelectExpression.ApplyFirstRowPerGroup` ──[CALLS]──> `_groupBy.Clear (External/BCL)`
  • + [新增呼叫邊] `SelectExpression.ApplyFirstRowPerGroup` ──[CALLS]──> `_identifier.Clear (External/BCL)`
  • + [新增呼叫邊] `SelectExpression.ApplyFirstRowPerGroup` ──[CALLS]──> `_identifier.AddRange (External/BCL)`
  • + [新增呼叫邊] `SelectExpression.ApplyFirstRowPerGroup` ──[CALLS]──> `sqlExpressionFactory.ApplyDefaultTypeMapping (External/BCL)`
  • + [新增呼叫邊] `SelectExpression.ApplyFirstRowPerGroup` ──[CALLS]──> `sqlExpressionFactory.Constant (External/BCL)`
  • _... 以及其餘 11 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SelectExpression.AddJoin()`
- **變更前簽章 (Before)**: `SelectExpression.AddJoin(
        JoinType joinType,
        ref SelectExpression innerSelect,
        out bool innerPushdownOccurred,
        SqlExpression? joinPredicate = null,
        bool isToOneJoin = false,
        bool isPrunableJoin = false)` (L3193~L3742)
- **變更後簽章 (After)**: `SelectExpression.AddJoin(
        JoinType joinType,
        ref SelectExpression innerSelect,
        out bool innerPushdownOccurred,
        SqlExpression? joinPredicate = null,
        bool isToOneJoin = false,
        bool isPrunableJoin = false)` (L3238~L3782)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private void AddJoin(
        JoinType joinType,
        ref SelectExpression innerSelect,
        out bool innerPushdownOccurred,
        SqlExpression? joinPredicate = null,
        bool isToOneJoin = false,
        bool isPrunableJoin = false)
    {
        innerPushdownOccurred = false;
        // Try to convert Apply to normal join
        if (joinType is JoinType.CrossApply or JoinType.OuterApply)
        {
            var limit = innerSelect.Limit;
            var offset = innerSelect.Offset;
            if (!innerSelect.IsDistinct
                || (limit == null && offset == null))
            {
                innerSelect.Limit = null;
                innerSelect.Offset = null;

                var originalInnerSelectPredicate = innerSelect.GroupBy.Count > 0
                    ? innerSelect.Having
                    : innerSelect.Predicate;

                joinPredicate = TryExtractJoinKey(this, innerSelect, allowNonEquality: limit == null && offset == null);
                if (joinPredicate != null)
                {
                    var containsOuterReference = new SelectExpressionCorrelationFindingExpressionVisitor(this)
                        .ContainsOuterReference(innerSelect);
                    if (!containsOuterReference)
                    {
                        if (limit != null || offset != null)
                        {
                            var partitions = new List<SqlExpression>();
                            GetPartitions(innerSelect, joinPredicate, partitions);
                            var orderings = innerSelect.Orderings.Count > 0
                                ? innerSelect.Orderings
                                : innerSelect._identifier.Count > 0
                                    ? innerSelect._identifier.Select(e => new OrderingExpression(e.Column, true))
                                    : [new OrderingExpression(new SqlFragmentExpression("(SELECT 1)", typeof(int)), true)];

                            var rowNumberExpression = new RowNumberExpression(
                                partitions, orderings.ToList(), (limit ?? offset)!.TypeMapping);
                            innerSelect.ClearOrdering();

                            joinPredicate = innerSelect.PushdownIntoSubqueryInternal().Remap(joinPredicate);

                            var outerColumn = ((SelectExpression)innerSelect.Tables[0]).GenerateOuterColumn(
                                innerSelect.Tables[0].Alias!, rowNumberExpression, "row");
                            SqlExpression? offsetPredicate = null;
                            SqlExpression? limitPredicate = null;
                            if (offset != null)
                            {
                                offsetPredicate = new SqlBinaryExpression(
                                    ExpressionType.LessThan, offset, outerColumn, typeof(bool), joinPredicate.TypeMapping);
                            }

                            if (limit != null)
                            {
                                if (offset != null)
                                {
                                    limit = offset is SqlConstantExpression offsetConstant
                                        && limit is SqlConstantExpression limitConstant
                                            ? new SqlConstantExpression(
                                                (int)offsetConstant.Value! + (int)limitConstant.Value!,
                                                limit.TypeMapping)
                                            : new SqlBinaryExpression(ExpressionType.Add, offset, limit, limit.Type, limit.TypeMapping);
                                }

                                limitPredicate = new SqlBinaryExpression(
                                    ExpressionType.LessThanOrEqual, outerColumn, limit, typeof(bool), joinPredicate.TypeMapping);
                            }

                            var predicate = offsetPredicate != null
                                ? limitPredicate != null
                                    ? new SqlBinaryExpression(
                                        ExpressionType.AndAlso, offsetPredicate, limitPredicate, typeof(bool),
                                        joinPredicate.TypeMapping)
                                    : offsetPredicate
                                : limitPredicate;
                            innerSelect.ApplyPredicate(predicate!);
                        }

                        AddJoin(
                            joinType == JoinType.CrossApply ? JoinType.InnerJoin : JoinType.LeftJoin,
                            ref innerSelect,
                            out innerPushdownOccurred,
                            joinPredicate,
                            isToOneJoin,
                            isPrunableJoin);

                        return;
                    }

                    if (originalInnerSelectPredicate != null)
                    {
                        if (innerSelect.GroupBy.Count > 0)
                        {
                            innerSelect.Having = originalInnerSelectPredicate;
                        }
                        else
                        {
                            innerSelect.Predicate = originalInnerSelectPredicate;
                        }
                    }

                    joinPredicate = null;
                }

                // Order matters Apply Offset before Limit
                if (offset != null)
                {
                    innerSelect.ApplyOffset(offset);
                }

                if (limit != null)
                {
                    innerSelect.ApplyLimit(limit);
                }
            }
        }

        if (Limit != null
            || Offset != null
            || IsDistinct
            || GroupBy.Count > 0
            // When the outer becomes nullable (RIGHT/FULL JOIN), an outer predicate must be applied before the join; otherwise it
            // would be rendered as a post-join WHERE that incorrectly filters out the unmatched inner rows (where the outer is null).
            || (joinType is JoinType.RightJoin or JoinType.FullJoin && Predicate != null))
        {
            var sqlRemappingVisitor = PushdownIntoSubqueryInternal();
            innerSelect = sqlRemappingVisitor.Remap(innerSelect);
            joinPredicate = sqlRemappingVisitor.Remap(joinPredicate);
        }

        if (innerSelect.Limit != null
            || innerSelect.Offset != null
            || innerSelect.IsDistinct
            || innerSelect.Predicate != null
            || innerSelect.Tables.Count > 1
            || innerSelect.GroupBy.Count > 0)
        {
            joinPredicate = innerSelect.PushdownIntoSubqueryInternal().Remap(joinPredicate);
            innerPushdownOccurred = true;
        }

        // If this is a to-one join, then we know that it doesn't increase cardinality — the outer identifiers are already sufficient.
        // Skipping the inner's identifiers avoids unnecessary ORDER BY columns and projections (#29182).
        if (_identifier.Count == 0 || innerSelect._identifier.Count == 0)
        {
            // Either the outer and inner sides aren't uniquely identifiable; mark everything as non-uniquely-identifiable.
            _identifier.Clear();
            innerSelect._identifier.Clear();
        }
        else if (!isToOneJoin || joinType is JoinType.RightJoin or JoinType.FullJoin)
        {
            // This is cardinality-increasing join - add identifiers from the inner.
            // Note that we do the same for right/full joins, since these make the outer identifiers nullable; that could mean that
            // multiple inner rows get the same NULL identifier.
            switch (joinType)
            {
                case JoinType.LeftJoin or JoinType.OuterApply:
                    _identifier.AddRange(innerSelect._identifier.Select(e => (e.Column.MakeNullable(), e.Comparer)));
                    break;

                case JoinType.RightJoin:
                    // Make the outer identifiers nullable, then add the inner identifiers
                    for (var i = 0; i < _identifier.Count; i++)
                    {
                        var identifier = _identifier[i];
                        _identifier[i] = (identifier.Column.MakeNullable(), identifier.Comparer);
                    }

                    _identifier.AddRange(innerSelect._identifier);
                    break;

                case JoinType.FullJoin:
                    // Both sides may be unmatched, so make the outer identifiers nullable and add the inner identifiers made nullable.
                    for (var i = 0; i < _identifier.Count; i++)
                    {
                        var identifier = _identifier[i];
                        _identifier[i] = (identifier.Column.MakeNullable(), identifier.Comparer);
                    }

                    _identifier.AddRange(innerSelect._identifier.Select(e => (e.Column.MakeNullable(), e.Comparer)));
                    break;

                case JoinType.InnerJoin or JoinType.CrossJoin or JoinType.CrossApply:
                    _identifier.AddRange(innerSelect._identifier);
                    break;

                default:
                    throw new UnreachableException();
            }
        }

        var innerTable = innerSelect.Tables.Single();
        var joinTable = joinType switch
        {
            JoinType.InnerJoin => new InnerJoinExpression(innerTable, joinPredicate!, isPrunableJoin),
            JoinType.LeftJoin => new LeftJoinExpression(innerTable, joinPredicate!, isPrunableJoin),
            JoinType.RightJoin => new RightJoinExpression(innerTable, joinPredicate!),
            JoinType.FullJoin => new FullJoinExpression(innerTable, joinPredicate!),
            JoinType.CrossJoin => new CrossJoinExpression(innerTable),
            JoinType.CrossApply => new CrossApplyExpression(innerTable),
            JoinType.OuterApply => (TableExpressionBase)new OuterApplyExpression(innerTable),
            _ => throw new InvalidOperationException(CoreStrings.InvalidSwitch(nameof(joinType), joinType))
        };

        _tables.Add(joinTable);

        static void GetPartitions(SelectExpression select, SqlExpression sqlExpression, List<SqlExpression> partitions)
        {
            switch (sqlExpression)
            {
                case SqlBinaryExpression { OperatorType: ExpressionType.Equal } binary:
                {
                    partitions.Add(
                        binary.Left is ColumnExpression column && select.ContainsReferencedTable(column)
                            ? binary.Left
                            : binary.Right);

                    break;
                }

                case SqlBinaryExpression { OperatorType: ExpressionType.AndAlso } binary:
                {
                    GetPartitions(select, binary.Left, partitions);
                    GetPartitions(select, binary.Right, partitions);

                    break;
                }
            }
        }

        static SqlExpression? TryExtractJoinKey(SelectExpression outer, SelectExpression inner, bool allowNonEquality)
        {
            if (inner.Limit != null
                || inner.Offset != null)
            {
                return null;
            }

            var predicate = inner.GroupBy.Count > 0 ? inner.Having : inner.Predicate;
            if (predicate == null)
            {
                return null;
            }

            var outerColumnExpressions = new List<SqlExpression>();
            var joinPredicate = TryExtractJoinKey(
                outer,
                inner,
                predicate,
                outerColumnExpressions,
                allowNonEquality,
                out var updatedPredicate);

            if (joinPredicate != null)
            {
                joinPredicate = RemoveRedundantNullChecks(joinPredicate, outerColumnExpressions);
            }

            // we can't convert apply to join in case of distinct and group by, if the projection doesn't already contain the join keys
            // since we can't add the missing keys to the projection - only convert to join if all the keys are already there
            if (joinPredicate != null
                && (inner.IsDistinct
                    || inner.GroupBy.Count > 0))
            {
                var innerKeyColumns = new List<ColumnExpression>();
                PopulateInnerKeyColumns(inner, joinPredicate, innerKeyColumns);

                // if projection has already been applied we can use it directly
                // otherwise we extract future projection columns from projection mapping
                // and based on that we determine whether we can convert from APPLY to JOIN
                var projectionColumns = inner.Projection.Count > 0
                    ? inner.Projection.Select(p => p.Expression)
                    : ExtractColumnsFromProjectionMapping(inner._projectionMapping);

                foreach (var innerColumn in innerKeyColumns)
                {
                    if (!projectionColumns.Contains(innerColumn))
                    {
                        return null;
                    }
                }
            }

            if (inner.GroupBy.Count > 0)
            {
                inner.Having = updatedPredicate;
            }
            else
            {
                inner.Predicate = updatedPredicate;
            }

            return joinPredicate;

            static SqlExpression? TryExtractJoinKey(
                SelectExpression outer,
                SelectExpression inner,
                SqlExpression predicate,
                List<SqlExpression> outerColumnExpressions,
                bool allowNonEquality,
                out SqlExpression? updatedPredicate)
            {
                if (predicate is SqlBinaryExpression sqlBinaryExpression)
                {
                    var joinPredicate = ValidateKeyComparison(
                        outer, inner, sqlBinaryExpression, outerColumnExpressions, allowNonEquality);
                    if (joinPredicate != null)
                    {
                        updatedPredicate = null;

                        return joinPredicate;
                    }

                    if (sqlBinaryExpression.OperatorType == ExpressionType.AndAlso)
                    {
                        var leftJoinKey = TryExtractJoinKey(
                            outer, inner, sqlBinaryExpression.Left, outerColumnExpressions, allowNonEquality, out var leftPredicate);
                        var rightJoinKey = TryExtractJoinKey(
                            outer, inner, sqlBinaryExpression.Right, outerColumnExpressions, allowNonEquality, out var rightPredicate);

                        updatedPredicate = CombineNonNullExpressions(leftPredicate, rightPredicate);

                        return CombineNonNullExpressions(leftJoinKey, rightJoinKey);
                    }
                }

                updatedPredicate = predicate;

                return null;
            }

            static SqlBinaryExpression? ValidateKeyComparison(
                SelectExpression outer,
                SelectExpression inner,
                SqlBinaryExpression sqlBinaryExpression,
                List<SqlExpression> outerColumnExpressions,
                bool allowNonEquality)
            {
                if (sqlBinaryExpression.OperatorType == ExpressionType.Equal
                    || (allowNonEquality
                        && sqlBinaryExpression.OperatorType is ExpressionType.NotEqual
                            or ExpressionType.GreaterThan
                            or ExpressionType.GreaterThanOrEqual
                            or ExpressionType.LessThan
                            or ExpressionType.LessThanOrEqual))
                {
                    if (IsContainedSql(outer, sqlBinaryExpression.Left)
                        && IsContainedSql(inner, sqlBinaryExpression.Right))
                    {
                        outerColumnExpressions.Add(sqlBinaryExpression.Left);

                        return sqlBinaryExpression;
                    }

                    if (IsContainedSql(outer, sqlBinaryExpression.Right)
                        && IsContainedSql(inner, sqlBinaryExpression.Left))
                    {
                        outerColumnExpressions.Add(sqlBinaryExpression.Right);

                        var mirroredOperation = sqlBinaryExpression.OperatorType switch
                        {
                            ExpressionType.Equal => ExpressionType.Equal,
                            ExpressionType.NotEqual => ExpressionType.NotEqual,
                            ExpressionType.LessThan => ExpressionType.GreaterThan,
                            ExpressionType.LessThanOrEqual => ExpressionType.GreaterThanOrEqual,
                            ExpressionType.GreaterThan => ExpressionType.LessThan,
                            ExpressionType.GreaterThanOrEqual => ExpressionType.LessThanOrEqual,

                            _ => throw new UnreachableException($"Unexpected operator type '{sqlBinaryExpression.OperatorType}'.")
                        };

                        return new SqlBinaryExpression(
                            mirroredOperation,
                            sqlBinaryExpression.Right,
                            sqlBinaryExpression.Left,
                            sqlBinaryExpression.Type,
                            sqlBinaryExpression.TypeMapping);
                    }
                }

                // null checks are considered part of join key
                if (sqlBinaryExpression.OperatorType == ExpressionType.NotEqual)
                {
                    if (IsContainedSql(outer, sqlBinaryExpression.Left)
                        && sqlBinaryExpression.Right is SqlConstantExpression { Value: null })
                    {
                        return sqlBinaryExpression;
                    }

                    if (IsContainedSql(outer, sqlBinaryExpression.Right)
                        && sqlBinaryExpression.Left is SqlConstantExpression { Value: null })
                    {
                        return sqlBinaryExpression.Update(
                            sqlBinaryExpression.Right,
                            sqlBinaryExpression.Left);
                    }
                }

                return null;
            }

            static bool IsContainedSql(SelectExpression selectExpression, SqlExpression sqlExpression)
                => sqlExpression switch
                {
                    ColumnExpression columnExpression => selectExpression.ContainsReferencedTable(columnExpression),

                    // We check condition in a separate function to avoid matching structure of condition outside of case block
                    CaseExpression
                    {
                        Operand: null,
                        WhenClauses: [{ Result: ColumnExpression resultColumn } whenClause],
                        ElseResult: null
                    }
                        => IsContainedCondition(selectExpression, whenClause.Test)
                        && selectExpression.ContainsReferencedTable(resultColumn),

                    _ => false
                };

            static bool IsContainedCondition(SelectExpression selectExpression, SqlExpression condition)
            {
                if (condition is not SqlBinaryExpression
                    {
                        OperatorType: ExpressionType.AndAlso or ExpressionType.OrElse or ExpressionType.NotEqual
                    } sqlBinaryExpression)
                {
                    return false;
                }

                if (sqlBinaryExpression.OperatorType == ExpressionType.NotEqual)
                {
                    // We don't check left/right inverted because we generate this.
                    return sqlBinaryExpression is { Left: ColumnExpression column, Right: SqlConstantExpression { Value: null } }
                        && selectExpression.ContainsReferencedTable(column);
                }

                return IsContainedCondition(selectExpression, sqlBinaryExpression.Left)
                    && IsContainedCondition(selectExpression, sqlBinaryExpression.Right);
            }

            static void PopulateInnerKeyColumns(
                SelectExpression select,
                SqlExpression joinPredicate,
                List<ColumnExpression> resultColumns)
            {
                switch (joinPredicate)
                {
                    case SqlBinaryExpression binary:
                        PopulateInnerKeyColumns(select, binary.Left, resultColumns);
                        PopulateInnerKeyColumns(select, binary.Right, resultColumns);
                        break;
                    case ColumnExpression columnExpression when select.ContainsReferencedTable(columnExpression):
                        resultColumns.Add(columnExpression);
                        break;
                }
            }

            static List<ColumnExpression> ExtractColumnsFromProjectionMapping(
                IDictionary<ProjectionMember, Expression> projectionMapping)
            {
                var result = new List<ColumnExpression>();
                foreach (var (_, expression) in projectionMapping)
                {
                    if (expression is StructuralTypeProjectionExpression projection)
                    {
                        foreach (var property in projection.StructuralType.GetPropertiesInHierarchy())
                        {
                            result.Add(projection.BindProperty(property));
                        }

                        if (projection.DiscriminatorExpression is ColumnExpression discriminatorColumn)
                        {
                            result.Add(discriminatorColumn);
                        }
                    }
                    else if (expression is ColumnExpression column)
                    {
                        result.Add(column);
                    }
                }

                return result;
            }

            static SqlExpression? CombineNonNullExpressions(SqlExpression? left, SqlExpression? right)
                => left != null
                    ? right != null
                        ? new SqlBinaryExpression(ExpressionType.AndAlso, left, right, left.Type, left.TypeMapping)
                        : left
                    : right;

            static SqlExpression? RemoveRedundantNullChecks(SqlExpression predicate, List<SqlExpression> outerColumnExpressions)
            {
                // A single key comparison join predicate is processed with SQL null semantics in SqlNullabilityProcessor, so the
                // outer key null check is genuinely redundant and is removed. But when the predicate is compound (e.g. the collection
                // navigation has an additional filter), it's expanded with C# null semantics, which would incorrectly match rows where
                // both keys are null. In that case the null check on a nullable outer key (e.g. the principal entity is reached through
                // an optional navigation) must be kept to suppress that compensation. See #35706.
                var keepNullableKeyChecks = CountNonNullCheckConjuncts(predicate, outerColumnExpressions) > 1;

                return Rewrite(predicate, outerColumnExpressions, keepNullableKeyChecks);

                static SqlExpression? Rewrite(
                    SqlExpression predicate,
                    List<SqlExpression> outerColumnExpressions,
                    bool keepNullableKeyChecks)
                {
                    if (predicate is SqlBinaryExpression sqlBinaryExpression)
                    {
                        if (sqlBinaryExpression.OperatorType == ExpressionType.NotEqual
                            && outerColumnExpressions.Contains(sqlBinaryExpression.Left)
                            && sqlBinaryExpression.Right is SqlConstantExpression { Value: null }
                            && !(keepNullableKeyChecks && sqlBinaryExpression.Left is ColumnExpression { IsNullable: true }))
                        {
                            return null;
                        }

                        if (sqlBinaryExpression.OperatorType == ExpressionType.AndAlso)
                        {
                            var leftPredicate = Rewrite(sqlBinaryExpression.Left, outerColumnExpressions, keepNullableKeyChecks);
                            var rightPredicate = Rewrite(sqlBinaryExpression.Right, outerColumnExpressions, keepNullableKeyChecks);

                            return CombineNonNullExpressions(leftPredicate, rightPredicate);
                        }
                    }

                    return predicate;
                }

                // Counts the non-null-check conjuncts in the extracted join predicate; when more than one remains the resulting join
                // predicate is a conjunction subject to C# null semantics expansion.
                static int CountNonNullCheckConjuncts(SqlExpression predicate, List<SqlExpression> outerColumnExpressions)
                    => predicate is SqlBinaryExpression { OperatorType: ExpressionType.AndAlso } andAlso
                        ? CountNonNullCheckConjuncts(andAlso.Left, outerColumnExpressions)
                        + CountNonNullCheckConjuncts(andAlso.Right, outerColumnExpressions)
                        : predicate is SqlBinaryExpression
                        {
                            OperatorType: ExpressionType.NotEqual, Right: SqlConstantExpression { Value: null }
                        } nullCheck
                        && outerColumnExpressions.Contains(nullCheck.Left)
                            ? 0
                            : 1;
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private void AddJoin(
        JoinType joinType,
        ref SelectExpression innerSelect,
        out bool innerPushdownOccurred,
        SqlExpression? joinPredicate = null,
        bool isToOneJoin = false,
        bool isPrunableJoin = false)
    {
        innerPushdownOccurred = false;
        // Try to convert Apply to normal join
        if (joinType is JoinType.CrossApply or JoinType.OuterApply)
        {
            var limit = innerSelect.Limit;
            var offset = innerSelect.Offset;
            if (!innerSelect.IsDistinct
                || (limit == null && offset == null))
            {
                innerSelect.Limit = null;
                innerSelect.Offset = null;

                var originalInnerSelectPredicate = innerSelect.GroupBy.Count > 0
                    ? innerSelect.Having
                    : innerSelect.Predicate;

                joinPredicate = TryExtractJoinKey(this, innerSelect, allowNonEquality: limit == null && offset == null);
                if (joinPredicate != null)
                {
                    var containsOuterReference = new SelectExpressionCorrelationFindingExpressionVisitor(this)
                        .ContainsOuterReference(innerSelect);
                    if (!containsOuterReference)
                    {
                        if (limit != null || offset != null)
                        {
                            var partitions = new List<SqlExpression>();
                            GetPartitions(innerSelect, joinPredicate, partitions);
                            var rowNumberExpression = new RowNumberExpression(
                                partitions, GetRowNumberOrderings(innerSelect.Orderings, innerSelect._identifier),
                                (limit ?? offset)!.TypeMapping);
                            innerSelect.ClearOrdering();

                            joinPredicate = innerSelect.PushdownIntoSubqueryInternal().Remap(joinPredicate);

                            var outerColumn = ((SelectExpression)innerSelect.Tables[0]).GenerateOuterColumn(
                                innerSelect.Tables[0].Alias!, rowNumberExpression, "row");
                            SqlExpression? offsetPredicate = null;
                            SqlExpression? limitPredicate = null;
                            if (offset != null)
                            {
                                offsetPredicate = new SqlBinaryExpression(
                                    ExpressionType.LessThan, offset, outerColumn, typeof(bool), joinPredicate.TypeMapping);
                            }

                            if (limit != null)
                            {
                                if (offset != null)
                                {
                                    limit = offset is SqlConstantExpression offsetConstant
                                        && limit is SqlConstantExpression limitConstant
                                            ? new SqlConstantExpression(
                                                (int)offsetConstant.Value! + (int)limitConstant.Value!,
                                                limit.TypeMapping)
                                            : new SqlBinaryExpression(ExpressionType.Add, offset, limit, limit.Type, limit.TypeMapping);
                                }

                                limitPredicate = new SqlBinaryExpression(
                                    ExpressionType.LessThanOrEqual, outerColumn, limit, typeof(bool), joinPredicate.TypeMapping);
                            }

                            var predicate = offsetPredicate != null
                                ? limitPredicate != null
                                    ? new SqlBinaryExpression(
                                        ExpressionType.AndAlso, offsetPredicate, limitPredicate, typeof(bool),
                                        joinPredicate.TypeMapping)
                                    : offsetPredicate
                                : limitPredicate;
                            innerSelect.ApplyPredicate(predicate!);
                        }

                        AddJoin(
                            joinType == JoinType.CrossApply ? JoinType.InnerJoin : JoinType.LeftJoin,
                            ref innerSelect,
                            out innerPushdownOccurred,
                            joinPredicate,
                            isToOneJoin,
                            isPrunableJoin);

                        return;
                    }

                    if (originalInnerSelectPredicate != null)
                    {
                        if (innerSelect.GroupBy.Count > 0)
                        {
                            innerSelect.Having = originalInnerSelectPredicate;
                        }
                        else
                        {
                            innerSelect.Predicate = originalInnerSelectPredicate;
                        }
                    }

                    joinPredicate = null;
                }

                // Order matters Apply Offset before Limit
                if (offset != null)
                {
                    innerSelect.ApplyOffset(offset);
                }

                if (limit != null)
                {
                    innerSelect.ApplyLimit(limit);
                }
            }
        }

        if (Limit != null
            || Offset != null
            || IsDistinct
            || GroupBy.Count > 0
            // When the outer becomes nullable (RIGHT/FULL JOIN), an outer predicate must be applied before the join; otherwise it
            // would be rendered as a post-join WHERE that incorrectly filters out the unmatched inner rows (where the outer is null).
            || (joinType is JoinType.RightJoin or JoinType.FullJoin && Predicate != null))
        {
            var sqlRemappingVisitor = PushdownIntoSubqueryInternal();
            innerSelect = sqlRemappingVisitor.Remap(innerSelect);
            joinPredicate = sqlRemappingVisitor.Remap(joinPredicate);
        }

        if (innerSelect.Limit != null
            || innerSelect.Offset != null
            || innerSelect.IsDistinct
            || innerSelect.Predicate != null
            || innerSelect.Tables.Count > 1
            || innerSelect.GroupBy.Count > 0)
        {
            joinPredicate = innerSelect.PushdownIntoSubqueryInternal().Remap(joinPredicate);
            innerPushdownOccurred = true;
        }

        // If this is a to-one join, then we know that it doesn't increase cardinality — the outer identifiers are already sufficient.
        // Skipping the inner's identifiers avoids unnecessary ORDER BY columns and projections (#29182).
        if (_identifier.Count == 0 || innerSelect._identifier.Count == 0)
        {
            // Either the outer and inner sides aren't uniquely identifiable; mark everything as non-uniquely-identifiable.
            _identifier.Clear();
            innerSelect._identifier.Clear();
        }
        else if (!isToOneJoin || joinType is JoinType.RightJoin or JoinType.FullJoin)
        {
            // This is cardinality-increasing join - add identifiers from the inner.
            // Note that we do the same for right/full joins, since these make the outer identifiers nullable; that could mean that
            // multiple inner rows get the same NULL identifier.
            switch (joinType)
            {
                case JoinType.LeftJoin or JoinType.OuterApply:
                    _identifier.AddRange(innerSelect._identifier.Select(e => (e.Column.MakeNullable(), e.Comparer)));
                    break;

                case JoinType.RightJoin:
                    // Make the outer identifiers nullable, then add the inner identifiers
                    for (var i = 0; i < _identifier.Count; i++)
                    {
                        var identifier = _identifier[i];
                        _identifier[i] = (identifier.Column.MakeNullable(), identifier.Comparer);
                    }

                    _identifier.AddRange(innerSelect._identifier);
                    break;

                case JoinType.FullJoin:
                    // Both sides may be unmatched, so make the outer identifiers nullable and add the inner identifiers made nullable.
                    for (var i = 0; i < _identifier.Count; i++)
                    {
                        var identifier = _identifier[i];
                        _identifier[i] = (identifier.Column.MakeNullable(), identifier.Comparer);
                    }

                    _identifier.AddRange(innerSelect._identifier.Select(e => (e.Column.MakeNullable(), e.Comparer)));
                    break;

                case JoinType.InnerJoin or JoinType.CrossJoin or JoinType.CrossApply:
                    _identifier.AddRange(innerSelect._identifier);
                    break;

                default:
                    throw new UnreachableException();
            }
        }

        var innerTable = innerSelect.Tables.Single();
        var joinTable = joinType switch
        {
            JoinType.InnerJoin => new InnerJoinExpression(innerTable, joinPredicate!, isPrunableJoin),
            JoinType.LeftJoin => new LeftJoinExpression(innerTable, joinPredicate!, isPrunableJoin),
            JoinType.RightJoin => new RightJoinExpression(innerTable, joinPredicate!),
            JoinType.FullJoin => new FullJoinExpression(innerTable, joinPredicate!),
            JoinType.CrossJoin => new CrossJoinExpression(innerTable),
            JoinType.CrossApply => new CrossApplyExpression(innerTable),
            JoinType.OuterApply => (TableExpressionBase)new OuterApplyExpression(innerTable),
            _ => throw new InvalidOperationException(CoreStrings.InvalidSwitch(nameof(joinType), joinType))
        };

        _tables.Add(joinTable);

        static void GetPartitions(SelectExpression select, SqlExpression sqlExpression, List<SqlExpression> partitions)
        {
            switch (sqlExpression)
            {
                case SqlBinaryExpression { OperatorType: ExpressionType.Equal } binary:
                {
                    partitions.Add(
                        binary.Left is ColumnExpression column && select.ContainsReferencedTable(column)
                            ? binary.Left
                            : binary.Right);

                    break;
                }

                case SqlBinaryExpression { OperatorType: ExpressionType.AndAlso } binary:
                {
                    GetPartitions(select, binary.Left, partitions);
                    GetPartitions(select, binary.Right, partitions);

                    break;
                }
            }
        }

        static SqlExpression? TryExtractJoinKey(SelectExpression outer, SelectExpression inner, bool allowNonEquality)
        {
            if (inner.Limit != null
                || inner.Offset != null)
            {
                return null;
            }

            var predicate = inner.GroupBy.Count > 0 ? inner.Having : inner.Predicate;
            if (predicate == null)
            {
                return null;
            }

            var outerColumnExpressions = new List<SqlExpression>();
            var joinPredicate = TryExtractJoinKey(
                outer,
                inner,
                predicate,
                outerColumnExpressions,
                allowNonEquality,
                out var updatedPredicate);

            if (joinPredicate != null)
            {
                joinPredicate = RemoveRedundantNullChecks(joinPredicate, outerColumnExpressions);
            }

            // we can't convert apply to join in case of distinct and group by, if the projection doesn't already contain the join keys
            // since we can't add the missing keys to the projection - only convert to join if all the keys are already there
            if (joinPredicate != null
                && (inner.IsDistinct
                    || inner.GroupBy.Count > 0))
            {
                var innerKeyColumns = new List<ColumnExpression>();
                PopulateInnerKeyColumns(inner, joinPredicate, innerKeyColumns);

                // if projection has already been applied we can use it directly
                // otherwise we extract future projection columns from projection mapping
                // and based on that we determine whether we can convert from APPLY to JOIN
                var projectionColumns = inner.Projection.Count > 0
                    ? inner.Projection.Select(p => p.Expression)
                    : ExtractColumnsFromProjectionMapping(inner._projectionMapping);

                foreach (var innerColumn in innerKeyColumns)
                {
                    if (!projectionColumns.Contains(innerColumn))
                    {
                        return null;
                    }
                }
            }

            if (inner.GroupBy.Count > 0)
            {
                inner.Having = updatedPredicate;
            }
            else
            {
                inner.Predicate = updatedPredicate;
            }

            return joinPredicate;

            static SqlExpression? TryExtractJoinKey(
                SelectExpression outer,
                SelectExpression inner,
                SqlExpression predicate,
                List<SqlExpression> outerColumnExpressions,
                bool allowNonEquality,
                out SqlExpression? updatedPredicate)
            {
                if (predicate is SqlBinaryExpression sqlBinaryExpression)
                {
                    var joinPredicate = ValidateKeyComparison(
                        outer, inner, sqlBinaryExpression, outerColumnExpressions, allowNonEquality);
                    if (joinPredicate != null)
                    {
                        updatedPredicate = null;

                        return joinPredicate;
                    }

                    if (sqlBinaryExpression.OperatorType == ExpressionType.AndAlso)
                    {
                        var leftJoinKey = TryExtractJoinKey(
                            outer, inner, sqlBinaryExpression.Left, outerColumnExpressions, allowNonEquality, out var leftPredicate);
                        var rightJoinKey = TryExtractJoinKey(
                            outer, inner, sqlBinaryExpression.Right, outerColumnExpressions, allowNonEquality, out var rightPredicate);

                        updatedPredicate = CombineNonNullExpressions(leftPredicate, rightPredicate);

                        return CombineNonNullExpressions(leftJoinKey, rightJoinKey);
                    }
                }

                updatedPredicate = predicate;

                return null;
            }

            static SqlBinaryExpression? ValidateKeyComparison(
                SelectExpression outer,
                SelectExpression inner,
                SqlBinaryExpression sqlBinaryExpression,
                List<SqlExpression> outerColumnExpressions,
                bool allowNonEquality)
            {
                if (sqlBinaryExpression.OperatorType == ExpressionType.Equal
                    || (allowNonEquality
                        && sqlBinaryExpression.OperatorType is ExpressionType.NotEqual
                            or ExpressionType.GreaterThan
                            or ExpressionType.GreaterThanOrEqual
                            or ExpressionType.LessThan
                            or ExpressionType.LessThanOrEqual))
                {
                    if (IsContainedSql(outer, sqlBinaryExpression.Left)
                        && IsContainedSql(inner, sqlBinaryExpression.Right))
                    {
                        outerColumnExpressions.Add(sqlBinaryExpression.Left);

                        return sqlBinaryExpression;
                    }

                    if (IsContainedSql(outer, sqlBinaryExpression.Right)
                        && IsContainedSql(inner, sqlBinaryExpression.Left))
                    {
                        outerColumnExpressions.Add(sqlBinaryExpression.Right);

                        var mirroredOperation = sqlBinaryExpression.OperatorType switch
                        {
                            ExpressionType.Equal => ExpressionType.Equal,
                            ExpressionType.NotEqual => ExpressionType.NotEqual,
                            ExpressionType.LessThan => ExpressionType.GreaterThan,
                            ExpressionType.LessThanOrEqual => ExpressionType.GreaterThanOrEqual,
                            ExpressionType.GreaterThan => ExpressionType.LessThan,
                            ExpressionType.GreaterThanOrEqual => ExpressionType.LessThanOrEqual,

                            _ => throw new UnreachableException($"Unexpected operator type '{sqlBinaryExpression.OperatorType}'.")
                        };

                        return new SqlBinaryExpression(
                            mirroredOperation,
                            sqlBinaryExpression.Right,
                            sqlBinaryExpression.Left,
                            sqlBinaryExpression.Type,
                            sqlBinaryExpression.TypeMapping);
                    }
                }

                // null checks are considered part of join key
                if (sqlBinaryExpression.OperatorType == ExpressionType.NotEqual)
                {
                    if (IsContainedSql(outer, sqlBinaryExpression.Left)
                        && sqlBinaryExpression.Right is SqlConstantExpression { Value: null })
                    {
                        return sqlBinaryExpression;
                    }

                    if (IsContainedSql(outer, sqlBinaryExpression.Right)
                        && sqlBinaryExpression.Left is SqlConstantExpression { Value: null })
                    {
                        return sqlBinaryExpression.Update(
                            sqlBinaryExpression.Right,
                            sqlBinaryExpression.Left);
                    }
                }

                return null;
            }

            static bool IsContainedSql(SelectExpression selectExpression, SqlExpression sqlExpression)
                => sqlExpression switch
                {
                    ColumnExpression columnExpression => selectExpression.ContainsReferencedTable(columnExpression),

                    // We check condition in a separate function to avoid matching structure of condition outside of case block
                    CaseExpression
                    {
                        Operand: null,
                        WhenClauses: [{ Result: ColumnExpression resultColumn } whenClause],
                        ElseResult: null
                    }
                        => IsContainedCondition(selectExpression, whenClause.Test)
                        && selectExpression.ContainsReferencedTable(resultColumn),

                    _ => false
                };

            static bool IsContainedCondition(SelectExpression selectExpression, SqlExpression condition)
            {
                if (condition is not SqlBinaryExpression
                    {
                        OperatorType: ExpressionType.AndAlso or ExpressionType.OrElse or ExpressionType.NotEqual
                    } sqlBinaryExpression)
                {
                    return false;
                }

                if (sqlBinaryExpression.OperatorType == ExpressionType.NotEqual)
                {
                    // We don't check left/right inverted because we generate this.
                    return sqlBinaryExpression is { Left: ColumnExpression column, Right: SqlConstantExpression { Value: null } }
                        && selectExpression.ContainsReferencedTable(column);
                }

                return IsContainedCondition(selectExpression, sqlBinaryExpression.Left)
                    && IsContainedCondition(selectExpression, sqlBinaryExpression.Right);
            }

            static void PopulateInnerKeyColumns(
                SelectExpression select,
                SqlExpression joinPredicate,
                List<ColumnExpression> resultColumns)
            {
                switch (joinPredicate)
                {
                    case SqlBinaryExpression binary:
                        PopulateInnerKeyColumns(select, binary.Left, resultColumns);
                        PopulateInnerKeyColumns(select, binary.Right, resultColumns);
                        break;
                    case ColumnExpression columnExpression when select.ContainsReferencedTable(columnExpression):
                        resultColumns.Add(columnExpression);
                        break;
                }
            }

            static List<ColumnExpression> ExtractColumnsFromProjectionMapping(
                IDictionary<ProjectionMember, Expression> projectionMapping)
            {
                var result = new List<ColumnExpression>();
                foreach (var (_, expression) in projectionMapping)
                {
                    if (expression is StructuralTypeProjectionExpression projection)
                    {
                        foreach (var property in projection.StructuralType.GetPropertiesInHierarchy())
                        {
                            result.Add(projection.BindProperty(property));
                        }

                        if (projection.DiscriminatorExpression is ColumnExpression discriminatorColumn)
                        {
                            result.Add(discriminatorColumn);
                        }
                    }
                    else if (expression is ColumnExpression column)
                    {
                        result.Add(column);
                    }
                }

                return result;
            }

            static SqlExpression? CombineNonNullExpressions(SqlExpression? left, SqlExpression? right)
                => left != null
                    ? right != null
                        ? new SqlBinaryExpression(ExpressionType.AndAlso, left, right, left.Type, left.TypeMapping)
                        : left
                    : right;

            static SqlExpression? RemoveRedundantNullChecks(SqlExpression predicate, List<SqlExpression> outerColumnExpressions)
            {
                // A single key comparison join predicate is processed with SQL null semantics in SqlNullabilityProcessor, so the
                // outer key null check is genuinely redundant and is removed. But when the predicate is compound (e.g. the collection
                // navigation has an additional filter), it's expanded with C# null semantics, which would incorrectly match rows where
                // both keys are null. In that case the null check on a nullable outer key (e.g. the principal entity is reached through
                // an optional navigation) must be kept to suppress that compensation. See #35706.
                var keepNullableKeyChecks = CountNonNullCheckConjuncts(predicate, outerColumnExpressions) > 1;

                return Rewrite(predicate, outerColumnExpressions, keepNullableKeyChecks);

                static SqlExpression? Rewrite(
                    SqlExpression predicate,
                    List<SqlExpression> outerColumnExpressions,
                    bool keepNullableKeyChecks)
                {
                    if (predicate is SqlBinaryExpression sqlBinaryExpression)
                    {
                        if (sqlBinaryExpression.OperatorType == ExpressionType.NotEqual
                            && outerColumnExpressions.Contains(sqlBinaryExpression.Left)
                            && sqlBinaryExpression.Right is SqlConstantExpression { Value: null }
                            && !(keepNullableKeyChecks && sqlBinaryExpression.Left is ColumnExpression { IsNullable: true }))
                        {
                            return null;
                        }

                        if (sqlBinaryExpression.OperatorType == ExpressionType.AndAlso)
                        {
                            var leftPredicate = Rewrite(sqlBinaryExpression.Left, outerColumnExpressions, keepNullableKeyChecks);
                            var rightPredicate = Rewrite(sqlBinaryExpression.Right, outerColumnExpressions, keepNullableKeyChecks);

                            return CombineNonNullExpressions(leftPredicate, rightPredicate);
                        }
                    }

                    return predicate;
                }

                // Counts the non-null-check conjuncts in the extracted join predicate; when more than one remains the resulting join
                // predicate is a conjunction subject to C# null semantics expansion.
                static int CountNonNullCheckConjuncts(SqlExpression predicate, List<SqlExpression> outerColumnExpressions)
                    => predicate is SqlBinaryExpression { OperatorType: ExpressionType.AndAlso } andAlso
                        ? CountNonNullCheckConjuncts(andAlso.Left, outerColumnExpressions)
                        + CountNonNullCheckConjuncts(andAlso.Right, outerColumnExpressions)
                        : predicate is SqlBinaryExpression
                        {
                            OperatorType: ExpressionType.NotEqual, Right: SqlConstantExpression { Value: null }
                        } nullCheck
                        && outerColumnExpressions.Contains(nullCheck.Left)
                            ? 0
                            : 1;
            }
        }
    }
```


---

### 🔹 Commit #07: `eec664d1`
- **完整 Hash**: `eec664d18030c25bc7ee005052d563800ed288ac`
- **說明 (Ground Truth)**: Enable nullable annotations in precompiled query interceptors (#39224)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.Design/Query/Internal/PrecompiledQueryCodeGenerator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:257, E:241, A:0) ➔ After(N:258, E:242, A:0)
- **差分統計**: +Nodes: 12, -Nodes: 11, +Edges: 9, -Edges: 8, ΔFuncs: 6, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_1435` (MODULE_STATE)
  • + [新增節點] `state_1443` (MODULE_STATE)
  • + [新增節點] `_code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            // Auto-generated code has the nullable context disabled, but the interceptor signatures contain nullable annotations
            .AppendLine("#nullable enable annotations")
            .AppendLine()
            .Append (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            // Auto-generated code has the nullable context disabled, but the interceptor signatures contain nullable annotations
            .AppendLine (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            // Auto-generated code has the nullable context disabled, but the interceptor signatures contain nullable annotations
            .AppendLine("#nullable enable annotations")
            .AppendLine()
            .Append("namespace ").AppendLine(InterceptorsNamespace)
            .AppendLine("{")
            .IncrementIndent()
            .AppendLine("file static class EntityFrameworkCoreInterceptors")
            .AppendLine("{")
            .IncrementIndent (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            // Auto-generated code has the nullable context disabled, but the interceptor signatures contain nullable annotations
            .AppendLine("#nullable enable annotations")
            .AppendLine()
            .Append("namespace ").AppendLine(InterceptorsNamespace)
            .AppendLine("{")
            .IncrementIndent (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            // Auto-generated code has the nullable context disabled, but the interceptor signatures contain nullable annotations
            .AppendLine("#nullable enable annotations")
            .AppendLine()
            .Append("namespace ").AppendLine(InterceptorsNamespace)
            .AppendLine("{")
            .IncrementIndent()
            .AppendLine("file static class EntityFrameworkCoreInterceptors")
            .AppendLine (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            // Auto-generated code has the nullable context disabled, but the interceptor signatures contain nullable annotations
            .AppendLine("#nullable enable annotations")
            .AppendLine (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            // Auto-generated code has the nullable context disabled, but the interceptor signatures contain nullable annotations
            .AppendLine("#nullable enable annotations")
            .AppendLine()
            .Append("namespace ").AppendLine (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            // Auto-generated code has the nullable context disabled, but the interceptor signatures contain nullable annotations
            .AppendLine("#nullable enable annotations")
            .AppendLine()
            .Append("namespace ").AppendLine(InterceptorsNamespace)
            .AppendLine("{")
            .IncrementIndent()
            .AppendLine (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            // Auto-generated code has the nullable context disabled, but the interceptor signatures contain nullable annotations
            .AppendLine("#nullable enable annotations")
            .AppendLine()
            .Append("namespace ").AppendLine(InterceptorsNamespace)
            .AppendLine (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_1444` (MODULE_STATE)
  • - [移除節點] `_code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            .AppendLine()
            .Append("namespace ").AppendLine (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `_code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            .AppendLine()
            .Append("namespace ").AppendLine(InterceptorsNamespace)
            .AppendLine (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `_code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            .AppendLine()
            .Append (External/BCL)` (FUNCTION_DEF)
  • _... 以及其餘 25 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `state_1438()`
- **變更前簽章 (Before)**: `[Module State] state_1438` (L1438~L1438)
- **變更後簽章 (After)**: `[Module State] state_1438` (L1438~L1438)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public readonly INamedTypeSymbol GenericEnumerator;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public readonly INamedTypeSymbol GenericEnumerable;
```

### 🔹 函式: `state_1439()`
- **變更前簽章 (Before)**: `[Module State] state_1439` (L1439~L1439)
- **變更後簽章 (After)**: `[Module State] state_1439` (L1439~L1439)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public readonly INamedTypeSymbol IQueryable;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public readonly INamedTypeSymbol GenericAsyncEnumerable;
```

### 🔹 函式: `state_1442()`
- **變更前簽章 (Before)**: `[Module State] state_1442` (L1442~L1442)
- **變更後簽章 (After)**: `[Module State] state_1442` (L1442~L1442)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public readonly INamedTypeSymbol GenericTask;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public readonly INamedTypeSymbol IOrderedQueryable;
```

### 🔹 函式: `state_1441()`
- **變更前簽章 (Before)**: `[Module State] state_1441` (L1441~L1441)
- **變更後簽章 (After)**: `[Module State] state_1441` (L1441~L1441)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public readonly INamedTypeSymbol IIncludableQueryable;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public readonly INamedTypeSymbol IQueryable;
```

### 🔹 函式: `PrecompiledQueryCodeGenerator.ProcessSyntaxTree()`
- **變更前簽章 (Before)**: `PrecompiledQueryCodeGenerator.ProcessSyntaxTree(
        SyntaxTree syntaxTree,
        SemanticModel semanticModel,
        IReadOnlyList<InvocationExpressionSyntax> locatedQueries,
        List<QueryPrecompilationError> precompilationErrors,
        string suffix,
        ISet<string> generatedFileNames,
        CancellationToken cancellationToken)` (L158~L397)
- **變更後簽章 (After)**: `PrecompiledQueryCodeGenerator.ProcessSyntaxTree(
        SyntaxTree syntaxTree,
        SemanticModel semanticModel,
        IReadOnlyList<InvocationExpressionSyntax> locatedQueries,
        List<QueryPrecompilationError> precompilationErrors,
        string suffix,
        ISet<string> generatedFileNames,
        CancellationToken cancellationToken)` (L158~L399)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected virtual ScaffoldedFile? ProcessSyntaxTree(
        SyntaxTree syntaxTree,
        SemanticModel semanticModel,
        IReadOnlyList<InvocationExpressionSyntax> locatedQueries,
        List<QueryPrecompilationError> precompilationErrors,
        string suffix,
        ISet<string> generatedFileNames,
        CancellationToken cancellationToken)
    {
        var queriesPrecompiledInFile = 0;
        _namespaces.Clear();
        _code.Clear();
        _code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            .AppendLine()
            .Append("namespace ").AppendLine(InterceptorsNamespace)
            .AppendLine("{")
            .IncrementIndent()
            .AppendLine("file static class EntityFrameworkCoreInterceptors")
            .AppendLine("{")
            .IncrementIndent();

        for (var queryNum = 0; queryNum < locatedQueries.Count; queryNum++)
        {
            var querySyntax = locatedQueries[queryNum];

            // A query that fails must leave nothing of itself behind: its interceptors reference an executor that will never be
            // generated, and the executor method itself may be half-written, so the file would not compile for the queries that
            // did succeed. Its code is therefore generated into a builder of its own and added to the file only once the query has
            // succeeded, and the runtime constants it declares are recorded so that exactly those can be taken back.
            var queryCode = new IndentedStringBuilder();
            for (var i = 0; i < _code.IndentCount; i++)
            {
                queryCode.IncrementIndent();
            }

            _runtimeConstantsOfCurrentQuery.Clear();

            try
            {
                // We have a query lambda, as a Roslyn syntax tree. Translate to LINQ expression tree.
                // TODO: Add verification that this is an EF query over our user's context. If translation returns null the moment
                // there's another query root (another context or another LINQ provider), that's fine.
                if (_csharpToLinqTranslator.Translate(querySyntax, semanticModel) is not MethodCallExpression terminatingOperator)
                {
                    throw new UnreachableException("Non-method call encountered as the root of a LINQ query");
                }

                // We have a LINQ representation of the query tree as it appears in the user's source code, but this isn't the same as the
                // LINQ tree the EF query pipeline needs to get; the latter is the result of evaluating the queryable operators in the user's
                // source code. For example, in the user's code the root is a DbSet as the root, but the expression tree we require needs to
                // contain an EntityQueryRootExpression. To get the LINQ tree for EF, we need to evaluate the operator chain, building an
                // expression tree as usual.

                // However, we cannot evaluate the last operator, since that would execute the query instead of returning an expression tree.
                // So we need to chop off the last operator before evaluation, and then (optionally) recompose it back afterwards.
                // For ToList(), we don't actually recompose it (since ToList() isn't a node in the expression tree), and for async operators,
                // we need to rewrite them to their sync counterparts (since that's what gets injected into the query tree).
                var penultimateOperator = terminatingOperator switch
                {
                    // This is needed e.g. for GetEnumerator(), DbSet.AsAsyncEnumerable (non-static terminating operators)
                    { Object: { } @object } => @object,
                    { Arguments: [var sourceArgument, ..] } => sourceArgument,
                    _ => throw new UnreachableException()
                };

                penultimateOperator = Expression.Lambda<Func<IQueryable>>(penultimateOperator)
                    .Compile(preferInterpretation: true)().Expression;

                // Pass the query through EF's query pipeline; this returns the query's executor function, which can produce an enumerable
                // that invokes the query.
                // Note that we cannot recompose the terminating operator on top of the evaluated penultimate, since method signatures
                // may not allow that (e.g. DbSet.AsAsyncEnumerable() requires a DbSet, but the evaluated value for a DbSet is
                // EntityQueryRootExpression. So we handle the penultimate and the terminating separately.
                var queryExecutor = CompileQuery(penultimateOperator, terminatingOperator);

                // The query has been compiled successfully by the EF query pipeline.
                // Now go over each LINQ operator, generating an interceptor for it.
                queryCode.AppendLine($"#region Query{queryNum + 1}").AppendLine();

                try
                {
                    _funcletizer.ResetPathCalculation();

                    if (querySyntax is not { Expression: MemberAccessExpressionSyntax { Expression: var penultimateOperatorSyntax } })
                    {
                        throw new UnreachableException();
                    }

                    // Generate interceptors for all LINQ operators in the query, starting from the root up until the penultimate.
                    // Then generate the interceptor for the terminating operator, and finally the query's executor.
                    GenerateOperatorInterceptorsRecursively(
                        queryCode, penultimateOperator, penultimateOperatorSyntax, semanticModel, queryNum + 1, out var operatorNum,
                        cancellationToken: cancellationToken);

                    GenerateOperatorInterceptor(
                        queryCode, terminatingOperator, querySyntax, semanticModel, queryNum + 1, operatorNum + 1,
                        isTerminatingOperator: true, cancellationToken);

                    GenerateQueryExecutor(queryCode, queryNum + 1, queryExecutor, _namespaces, _unsafeAccessors);
                }
                finally
                {
                    queryCode
                        .AppendLine()
                        .AppendLine($"#endregion Query{queryNum + 1}");
                }
            }
            catch (Exception e)
            {
                precompilationErrors.Add(new QueryPrecompilationError(querySyntax, e));

                foreach (var constantName in _runtimeConstantsOfCurrentQuery)
                {
                    var constant = _runtimeConstants[constantName];
                    _runtimeConstants.Remove(constantName);
                    _constantReplacements.Remove(constant.Value);
                    if (_runtimeConstantsByInitializer.TryGetValue(constant.InitializeExpression, out var declared)
                        && ReferenceEquals(declared, constant))
                    {
                        _runtimeConstantsByInitializer.Remove(constant.InitializeExpression);
                    }
                }

                continue;
            }

            // We're done generating the interceptors for the query's LINQ operators. The query's code already carries the file's
            // indentation, so it is added as it is, and the trailing line break is re-added through the builder to keep its own
            // indentation state right for what follows.
            using (_code.SuspendIndent())
            {
                _code.Append(queryCode.ToString().TrimEnd('\r', '\n'));
            }

            _code.AppendLine();

            queriesPrecompiledInFile++;
        }

        if (queriesPrecompiledInFile == 0)
        {
            return null;
        }

        // Output all the unsafe accessors that were generated for all intercepted shapers, e.g.:
        // [UnsafeAccessor(UnsafeAccessorKind.Field, Name = "<Name>k__BackingField")]
        // static extern ref int GetSet_Foo_Name(Foo f);
        if (_unsafeAccessors.Count > 0)
        {
            _code.AppendLine("#region Unsafe accessors");
            foreach (var unsafeAccessor in _unsafeAccessors)
            {
                _code.AppendLine(unsafeAccessor.NormalizeWhitespace().ToFullString());
            }

            _code.AppendLine("#endregion Unsafe accessors");
        }

        // The fields are in scope for their own initializers, so a type an initializer refers to by a name one of them has taken
        // has to be written out fully qualified; the translator does that for the names it is told are declared here.
        var runtimeConstantNames = _runtimeConstants.Keys.ToHashSet();
        foreach (var (fieldName, constant) in _runtimeConstants.OrderBy(x => x.Key))
        {
            var typeSymbol = GetTypeSymbol(semanticModel.Compilation, constant.Type);

            var syntax = _linqToCSharpTranslator.TranslateExpression(
                constant.InitializeExpression, constantReplacements: null, _namespaces, _unsafeAccessors, runtimeConstantNames);
            _code.AppendLine(
                $"private static readonly {typeSymbol.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat)} {fieldName} = {syntax.NormalizeWhitespace().ToFullString()};");
        }

        _code
            .DecrementIndent().AppendLine("}")
            .DecrementIndent().AppendLine("}");

        var mainCode = _code.ToString();

        _code.Clear();
        _code.AppendLine("// <auto-generated />").AppendLine();

        // In addition to the namespaces auto-detected by LinqToCSharpTranslator, we manually add these namespaces which are required
        // by manually generated code above.
        _namespaces.UnionWith(
        [
            "System",
            "System.Collections.Concurrent",
            "System.Collections.Generic",
            "System.Linq",
            "System.Linq.Expressions",
            "System.Runtime.CompilerServices",
            "System.Reflection",
            "System.Threading.Tasks",
            "Microsoft.EntityFrameworkCore",
            "Microsoft.EntityFrameworkCore.ChangeTracking.Internal",
            "Microsoft.EntityFrameworkCore.Diagnostics",
            "Microsoft.EntityFrameworkCore.Infrastructure",
            "Microsoft.EntityFrameworkCore.Infrastructure.Internal",
            "Microsoft.EntityFrameworkCore.Internal",
            "Microsoft.EntityFrameworkCore.Metadata",
            "Microsoft.EntityFrameworkCore.Query",
            "Microsoft.EntityFrameworkCore.Query.Internal",
            "Microsoft.EntityFrameworkCore.Storage"
        ]);

        foreach (var ns in _namespaces
                     .OrderBy(ns => ns switch
                     {
                         _ when ns.StartsWith("System.", StringComparison.Ordinal) => 10,
                         _ when ns.StartsWith("Microsoft.", StringComparison.Ordinal) => 9,
                         _ => 0
                     })
                     .ThenBy(ns => ns))
        {
            _code.Append("using ").Append(ns).AppendLine(";");
        }

        _code.AppendLine(mainCode);

        _code.AppendLine(
            """
namespace System.Runtime.CompilerServices
{
    [AttributeUsage(AttributeTargets.Method, AllowMultiple = true)]
    file sealed class InterceptsLocationAttribute : Attribute
    {
        public InterceptsLocationAttribute(int version, string data) { }
    }
}
"""
        );

        var name = Uniquifier.Uniquify(
            Path.GetFileNameWithoutExtension(syntaxTree.FilePath),
            generatedFileNames,
            CompiledModelScaffolder.MaxFileNameLength,
            ".EFInterceptors" + suffix + Path.GetExtension(syntaxTree.FilePath));
        return new ScaffoldedFile(name, _code.ToString());
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected virtual ScaffoldedFile? ProcessSyntaxTree(
        SyntaxTree syntaxTree,
        SemanticModel semanticModel,
        IReadOnlyList<InvocationExpressionSyntax> locatedQueries,
        List<QueryPrecompilationError> precompilationErrors,
        string suffix,
        ISet<string> generatedFileNames,
        CancellationToken cancellationToken)
    {
        var queriesPrecompiledInFile = 0;
        _namespaces.Clear();
        _code.Clear();
        _code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            // Auto-generated code has the nullable context disabled, but the interceptor signatures contain nullable annotations
            .AppendLine("#nullable enable annotations")
            .AppendLine()
            .Append("namespace ").AppendLine(InterceptorsNamespace)
            .AppendLine("{")
            .IncrementIndent()
            .AppendLine("file static class EntityFrameworkCoreInterceptors")
            .AppendLine("{")
            .IncrementIndent();

        for (var queryNum = 0; queryNum < locatedQueries.Count; queryNum++)
        {
            var querySyntax = locatedQueries[queryNum];

            // A query that fails must leave nothing of itself behind: its interceptors reference an executor that will never be
            // generated, and the executor method itself may be half-written, so the file would not compile for the queries that
            // did succeed. Its code is therefore generated into a builder of its own and added to the file only once the query has
            // succeeded, and the runtime constants it declares are recorded so that exactly those can be taken back.
            var queryCode = new IndentedStringBuilder();
            for (var i = 0; i < _code.IndentCount; i++)
            {
                queryCode.IncrementIndent();
            }

            _runtimeConstantsOfCurrentQuery.Clear();

            try
            {
                // We have a query lambda, as a Roslyn syntax tree. Translate to LINQ expression tree.
                // TODO: Add verification that this is an EF query over our user's context. If translation returns null the moment
                // there's another query root (another context or another LINQ provider), that's fine.
                if (_csharpToLinqTranslator.Translate(querySyntax, semanticModel) is not MethodCallExpression terminatingOperator)
                {
                    throw new UnreachableException("Non-method call encountered as the root of a LINQ query");
                }

                // We have a LINQ representation of the query tree as it appears in the user's source code, but this isn't the same as the
                // LINQ tree the EF query pipeline needs to get; the latter is the result of evaluating the queryable operators in the user's
                // source code. For example, in the user's code the root is a DbSet as the root, but the expression tree we require needs to
                // contain an EntityQueryRootExpression. To get the LINQ tree for EF, we need to evaluate the operator chain, building an
                // expression tree as usual.

                // However, we cannot evaluate the last operator, since that would execute the query instead of returning an expression tree.
                // So we need to chop off the last operator before evaluation, and then (optionally) recompose it back afterwards.
                // For ToList(), we don't actually recompose it (since ToList() isn't a node in the expression tree), and for async operators,
                // we need to rewrite them to their sync counterparts (since that's what gets injected into the query tree).
                var penultimateOperator = terminatingOperator switch
                {
                    // This is needed e.g. for GetEnumerator(), DbSet.AsAsyncEnumerable (non-static terminating operators)
                    { Object: { } @object } => @object,
                    { Arguments: [var sourceArgument, ..] } => sourceArgument,
                    _ => throw new UnreachableException()
                };

                penultimateOperator = Expression.Lambda<Func<IQueryable>>(penultimateOperator)
                    .Compile(preferInterpretation: true)().Expression;

                // Pass the query through EF's query pipeline; this returns the query's executor function, which can produce an enumerable
                // that invokes the query.
                // Note that we cannot recompose the terminating operator on top of the evaluated penultimate, since method signatures
                // may not allow that (e.g. DbSet.AsAsyncEnumerable() requires a DbSet, but the evaluated value for a DbSet is
                // EntityQueryRootExpression. So we handle the penultimate and the terminating separately.
                var queryExecutor = CompileQuery(penultimateOperator, terminatingOperator);

                // The query has been compiled successfully by the EF query pipeline.
                // Now go over each LINQ operator, generating an interceptor for it.
                queryCode.AppendLine($"#region Query{queryNum + 1}").AppendLine();

                try
                {
                    _funcletizer.ResetPathCalculation();

                    if (querySyntax is not { Expression: MemberAccessExpressionSyntax { Expression: var penultimateOperatorSyntax } })
                    {
                        throw new UnreachableException();
                    }

                    // Generate interceptors for all LINQ operators in the query, starting from the root up until the penultimate.
                    // Then generate the interceptor for the terminating operator, and finally the query's executor.
                    GenerateOperatorInterceptorsRecursively(
                        queryCode, penultimateOperator, penultimateOperatorSyntax, semanticModel, queryNum + 1, out var operatorNum,
                        cancellationToken: cancellationToken);

                    GenerateOperatorInterceptor(
                        queryCode, terminatingOperator, querySyntax, semanticModel, queryNum + 1, operatorNum + 1,
                        isTerminatingOperator: true, cancellationToken);

                    GenerateQueryExecutor(queryCode, queryNum + 1, queryExecutor, _namespaces, _unsafeAccessors);
                }
                finally
                {
                    queryCode
                        .AppendLine()
                        .AppendLine($"#endregion Query{queryNum + 1}");
                }
            }
            catch (Exception e)
            {
                precompilationErrors.Add(new QueryPrecompilationError(querySyntax, e));

                foreach (var constantName in _runtimeConstantsOfCurrentQuery)
                {
                    var constant = _runtimeConstants[constantName];
                    _runtimeConstants.Remove(constantName);
                    _constantReplacements.Remove(constant.Value);
                    if (_runtimeConstantsByInitializer.TryGetValue(constant.InitializeExpression, out var declared)
                        && ReferenceEquals(declared, constant))
                    {
                        _runtimeConstantsByInitializer.Remove(constant.InitializeExpression);
                    }
                }

                continue;
            }

            // We're done generating the interceptors for the query's LINQ operators. The query's code already carries the file's
            // indentation, so it is added as it is, and the trailing line break is re-added through the builder to keep its own
            // indentation state right for what follows.
            using (_code.SuspendIndent())
            {
                _code.Append(queryCode.ToString().TrimEnd('\r', '\n'));
            }

            _code.AppendLine();

            queriesPrecompiledInFile++;
        }

        if (queriesPrecompiledInFile == 0)
        {
            return null;
        }

        // Output all the unsafe accessors that were generated for all intercepted shapers, e.g.:
        // [UnsafeAccessor(UnsafeAccessorKind.Field, Name = "<Name>k__BackingField")]
        // static extern ref int GetSet_Foo_Name(Foo f);
        if (_unsafeAccessors.Count > 0)
        {
            _code.AppendLine("#region Unsafe accessors");
            foreach (var unsafeAccessor in _unsafeAccessors)
            {
                _code.AppendLine(unsafeAccessor.NormalizeWhitespace().ToFullString());
            }

            _code.AppendLine("#endregion Unsafe accessors");
        }

        // The fields are in scope for their own initializers, so a type an initializer refers to by a name one of them has taken
        // has to be written out fully qualified; the translator does that for the names it is told are declared here.
        var runtimeConstantNames = _runtimeConstants.Keys.ToHashSet();
        foreach (var (fieldName, constant) in _runtimeConstants.OrderBy(x => x.Key))
        {
            var typeSymbol = GetTypeSymbol(semanticModel.Compilation, constant.Type);

            var syntax = _linqToCSharpTranslator.TranslateExpression(
                constant.InitializeExpression, constantReplacements: null, _namespaces, _unsafeAccessors, runtimeConstantNames);
            _code.AppendLine(
                $"private static readonly {typeSymbol.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat)} {fieldName} = {syntax.NormalizeWhitespace().ToFullString()};");
        }

        _code
            .DecrementIndent().AppendLine("}")
            .DecrementIndent().AppendLine("}");

        var mainCode = _code.ToString();

        _code.Clear();
        _code.AppendLine("// <auto-generated />").AppendLine();

        // In addition to the namespaces auto-detected by LinqToCSharpTranslator, we manually add these namespaces which are required
        // by manually generated code above.
        _namespaces.UnionWith(
        [
            "System",
            "System.Collections.Concurrent",
            "System.Collections.Generic",
            "System.Linq",
            "System.Linq.Expressions",
            "System.Runtime.CompilerServices",
            "System.Reflection",
            "System.Threading.Tasks",
            "Microsoft.EntityFrameworkCore",
            "Microsoft.EntityFrameworkCore.ChangeTracking.Internal",
            "Microsoft.EntityFrameworkCore.Diagnostics",
            "Microsoft.EntityFrameworkCore.Infrastructure",
            "Microsoft.EntityFrameworkCore.Infrastructure.Internal",
            "Microsoft.EntityFrameworkCore.Internal",
            "Microsoft.EntityFrameworkCore.Metadata",
            "Microsoft.EntityFrameworkCore.Query",
            "Microsoft.EntityFrameworkCore.Query.Internal",
            "Microsoft.EntityFrameworkCore.Storage"
        ]);

        foreach (var ns in _namespaces
                     .OrderBy(ns => ns switch
                     {
                         _ when ns.StartsWith("System.", StringComparison.Ordinal) => 10,
                         _ when ns.StartsWith("Microsoft.", StringComparison.Ordinal) => 9,
                         _ => 0
                     })
                     .ThenBy(ns => ns))
        {
            _code.Append("using ").Append(ns).AppendLine(";");
        }

        _code.AppendLine(mainCode);

        _code.AppendLine(
            """
namespace System.Runtime.CompilerServices
{
    [AttributeUsage(AttributeTargets.Method, AllowMultiple = true)]
    file sealed class InterceptsLocationAttribute : Attribute
    {
        public InterceptsLocationAttribute(int version, string data) { }
    }
}
"""
        );

        var name = Uniquifier.Uniquify(
            Path.GetFileNameWithoutExtension(syntaxTree.FilePath),
            generatedFileNames,
            CompiledModelScaffolder.MaxFileNameLength,
            ".EFInterceptors" + suffix + Path.GetExtension(syntaxTree.FilePath));
        return new ScaffoldedFile(name, _code.ToString());
    }
```

### 🔹 函式: `state_1440()`
- **變更前簽章 (Before)**: `[Module State] state_1440` (L1440~L1440)
- **變更後簽章 (After)**: `[Module State] state_1440` (L1440~L1440)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public readonly INamedTypeSymbol IOrderedQueryable;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public readonly INamedTypeSymbol GenericEnumerator;
```


---

### 🔹 Commit #08: `f01f1ea3`
- **完整 Hash**: `f01f1ea3f97baadb879f78e6b33fc75236a3d4d4`
- **說明 (Ground Truth)**: Return the starting position for IndexOf with an empty string on SQL Server (#39231)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.SqlServer/Query/Internal/Translators/SqlServerStringMethodTranslator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:28, E:44, A:0) ➔ After(N:29, E:45, A:0)
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
  • + [新增節點] `sqlExpressionFactory.Negate (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `SqlServerStringMethodTranslator.TranslateIndexOf` ──[CALLS]──> `sqlExpressionFactory.Negate (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SqlServerStringMethodTranslator.TranslateIndexOf()`
- **變更前簽章 (Before)**: `SqlServerStringMethodTranslator.TranslateIndexOf(
        SqlExpression instance,
        MethodInfo method,
        SqlExpression searchExpression,
        SqlExpression? startIndex)` (L201~L272)
- **變更後簽章 (After)**: `SqlServerStringMethodTranslator.TranslateIndexOf(
        SqlExpression instance,
        MethodInfo method,
        SqlExpression searchExpression,
        SqlExpression? startIndex)` (L201~L273)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private SqlExpression TranslateIndexOf(
        SqlExpression instance,
        MethodInfo method,
        SqlExpression searchExpression,
        SqlExpression? startIndex)
    {
        var stringTypeMapping = ExpressionExtensions.InferTypeMapping(instance, searchExpression)
            ?? sqlExpressionFactory.ApplyDefaultTypeMapping(instance)!.TypeMapping!;
        searchExpression = ApplyStringTypeMapping(searchExpression, stringTypeMapping);

        instance = sqlExpressionFactory.ApplyTypeMapping(instance, stringTypeMapping);

        var charIndexArguments = new List<SqlExpression> { searchExpression, instance };

        if (startIndex is not null)
        {
            charIndexArguments.Add(
                startIndex is SqlConstantExpression { Value: int constantStartIndex }
                    ? sqlExpressionFactory.Constant(constantStartIndex + 1, typeof(int))
                    : sqlExpressionFactory.Add(startIndex, sqlExpressionFactory.Constant(1)));
        }

        var argumentsPropagateNullability = Enumerable.Repeat(true, charIndexArguments.Count);

        SqlExpression charIndexExpression;
        var storeType = stringTypeMapping.StoreType;
        if (string.Equals(storeType, "nvarchar(max)", StringComparison.OrdinalIgnoreCase)
            || string.Equals(storeType, "varchar(max)", StringComparison.OrdinalIgnoreCase))
        {
            charIndexExpression = sqlExpressionFactory.Function(
                "CHARINDEX",
                charIndexArguments,
                nullable: true,
                argumentsPropagateNullability,
                typeof(long));

            charIndexExpression = sqlExpressionFactory.Convert(charIndexExpression, typeof(int));
        }
        else
        {
            charIndexExpression = sqlExpressionFactory.Function(
                "CHARINDEX",
                charIndexArguments,
                nullable: true,
                argumentsPropagateNullability,
                method.ReturnType);
        }

        // If the pattern is an empty string, we need to special case to always return 0 (since CHARINDEX return 0, which we'd subtract to
        // -1). Handle separately for constant and non-constant patterns.
        if (searchExpression is SqlConstantExpression { Value: "" })
        {
            return sqlExpressionFactory.Case(
                [new CaseWhenClause(sqlExpressionFactory.IsNotNull(instance), sqlExpressionFactory.Constant(0))],
                elseResult: null
            );
        }

        var offsetExpression = searchExpression is SqlConstantExpression
            ? sqlExpressionFactory.Constant(1)
            : sqlExpressionFactory.Case(
                [
                    new CaseWhenClause(
                        sqlExpressionFactory.Equal(
                            searchExpression,
                            sqlExpressionFactory.Constant(string.Empty, stringTypeMapping)),
                        sqlExpressionFactory.Constant(0))
                ],
                sqlExpressionFactory.Constant(1));

        return sqlExpressionFactory.Subtract(charIndexExpression, offsetExpression);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private SqlExpression TranslateIndexOf(
        SqlExpression instance,
        MethodInfo method,
        SqlExpression searchExpression,
        SqlExpression? startIndex)
    {
        var stringTypeMapping = ExpressionExtensions.InferTypeMapping(instance, searchExpression)
            ?? sqlExpressionFactory.ApplyDefaultTypeMapping(instance)!.TypeMapping!;
        searchExpression = ApplyStringTypeMapping(searchExpression, stringTypeMapping);

        instance = sqlExpressionFactory.ApplyTypeMapping(instance, stringTypeMapping);

        var charIndexArguments = new List<SqlExpression> { searchExpression, instance };

        if (startIndex is not null)
        {
            charIndexArguments.Add(
                startIndex is SqlConstantExpression { Value: int constantStartIndex }
                    ? sqlExpressionFactory.Constant(constantStartIndex + 1, typeof(int))
                    : sqlExpressionFactory.Add(startIndex, sqlExpressionFactory.Constant(1)));
        }

        var argumentsPropagateNullability = Enumerable.Repeat(true, charIndexArguments.Count);

        SqlExpression charIndexExpression;
        var storeType = stringTypeMapping.StoreType;
        if (string.Equals(storeType, "nvarchar(max)", StringComparison.OrdinalIgnoreCase)
            || string.Equals(storeType, "varchar(max)", StringComparison.OrdinalIgnoreCase))
        {
            charIndexExpression = sqlExpressionFactory.Function(
                "CHARINDEX",
                charIndexArguments,
                nullable: true,
                argumentsPropagateNullability,
                typeof(long));

            charIndexExpression = sqlExpressionFactory.Convert(charIndexExpression, typeof(int));
        }
        else
        {
            charIndexExpression = sqlExpressionFactory.Function(
                "CHARINDEX",
                charIndexArguments,
                nullable: true,
                argumentsPropagateNullability,
                method.ReturnType);
        }

        // If the pattern is an empty string, we need to special case to return the starting position (0 by default), as .NET does: CHARINDEX
        // returns 0 for an empty pattern regardless of its start location, which we'd subtract to -1. Handle separately for constant and
        // non-constant patterns.
        if (searchExpression is SqlConstantExpression { Value: "" })
        {
            return sqlExpressionFactory.Case(
                [new CaseWhenClause(sqlExpressionFactory.IsNotNull(instance), startIndex ?? sqlExpressionFactory.Constant(0))],
                elseResult: null
            );
        }

        var offsetExpression = searchExpression is SqlConstantExpression
            ? sqlExpressionFactory.Constant(1)
            : sqlExpressionFactory.Case(
                [
                    new CaseWhenClause(
                        sqlExpressionFactory.Equal(
                            searchExpression,
                            sqlExpressionFactory.Constant(string.Empty, stringTypeMapping)),
                        startIndex is null ? sqlExpressionFactory.Constant(0) : sqlExpressionFactory.Negate(startIndex))
                ],
                sqlExpressionFactory.Constant(1));

        return sqlExpressionFactory.Subtract(charIndexExpression, offsetExpression);
    }
```


---

### 🔹 Commit #09: `791bc2c1`
- **完整 Hash**: `791bc2c19048fa0e7de4c74f16060b3fe5a05398`
- **說明 (Ground Truth)**: Fix GetRelationalModel race condition (#39216)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.Relational/Extensions/RelationalModelExtensions.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:68, E:72, A:0) ➔ After(N:68, E:72, A:0)
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

### 🔹 函式: `RelationalModelExtensions.GetRelationalModel()`
- **變更前簽章 (Before)**: `RelationalModelExtensions.GetRelationalModel(this IModel model)` (L67~L84)
- **變更後簽章 (After)**: `RelationalModelExtensions.GetRelationalModel(this IModel model)` (L67~L90)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static IRelationalModel GetRelationalModel(this IModel model)
    {
        var relationalModel = (IRelationalModel?)model.FindRuntimeAnnotationValue(RelationalAnnotationNames.RelationalModel);
        if (relationalModel == null)
        {
            var relationalModelFactory = (Func<IRelationalModel>?)model.FindRuntimeAnnotationValue(
                    RelationalAnnotationNames.RelationalModelFactory)
                ?? throw new InvalidOperationException(CoreStrings.ModelNotFinalized(nameof(GetRelationalModel)));
            lock (relationalModelFactory)
            {
                relationalModel = model.GetOrAddRuntimeAnnotationValue(
                    RelationalAnnotationNames.RelationalModel, f => f!(), relationalModelFactory);
                model.RemoveRuntimeAnnotation(RelationalAnnotationNames.RelationalModelFactory);
            }
        }

        return relationalModel;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static IRelationalModel GetRelationalModel(this IModel model)
    {
        var relationalModel = (IRelationalModel?)model.FindRuntimeAnnotationValue(RelationalAnnotationNames.RelationalModel);
        if (relationalModel == null)
        {
            var relationalModelFactory = (Func<IRelationalModel>?)model.FindRuntimeAnnotationValue(
                RelationalAnnotationNames.RelationalModelFactory);
            if (relationalModelFactory == null)
            {
                // The factory is removed after the relational model is created, which could have happened on another thread
                return (IRelationalModel?)model.FindRuntimeAnnotationValue(RelationalAnnotationNames.RelationalModel)
                    ?? throw new InvalidOperationException(CoreStrings.ModelNotFinalized(nameof(GetRelationalModel)));
            }

            lock (relationalModelFactory)
            {
                relationalModel = model.GetOrAddRuntimeAnnotationValue(
                    RelationalAnnotationNames.RelationalModel, f => f!(), relationalModelFactory);
                model.RemoveRuntimeAnnotation(RelationalAnnotationNames.RelationalModelFactory);
            }
        }

        return relationalModel;
    }
```


---

### 🔹 Commit #10: `2b992857`
- **完整 Hash**: `2b992857815f044304276565bf912d968c160495`
- **說明 (Ground Truth)**: Fix constant guid select (#39200)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.Relational/Query/Internal/RelationalProjectionBindingExpressionVisitor.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:124, E:170, A:0) ➔ After(N:124, E:170, A:0)
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
  • + [新增節點] `state_966` (MODULE_STATE)
  • - [移除節點] `state_956` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RelationalProjectionBindingExpressionVisitor.Visit()`
- **變更前簽章 (Before)**: `RelationalProjectionBindingExpressionVisitor.Visit(Expression? expression)` (L188~L364)
- **變更後簽章 (After)**: `RelationalProjectionBindingExpressionVisitor.Visit(Expression? expression)` (L188~L374)

#### ◀️ 變更前實作碼 (Before Implementation):
```
[return: NotNullIfNotNull(nameof(expression))]
    public override Expression? Visit(Expression? expression)
    {
        switch (expression)
        {
            case NewExpression or MemberInitExpression or StructuralTypeShaperExpression or IncludeExpression:
                return base.Visit(expression);

            case null:
                return null;

            case not null when _indexBasedBinding:
            {
                switch (expression)
                {
                    case ConstantExpression:
                        return expression;

                    case QueryParameterExpression queryParameterExpression:
                        return Expression.Call(
                            GetParameterValueMethodInfo.MakeGenericMethod(queryParameterExpression.Type),
                            QueryCompilationContext.QueryContextParameter,
                            Expression.Constant(queryParameterExpression.Name));

                    case ParameterExpression parameterExpression:
                        throw new InvalidOperationException(CoreStrings.TranslationFailed(parameterExpression.Print()));

                    case ProjectionBindingExpression projectionBindingExpression:
                        return _selectExpression.GetProjection(projectionBindingExpression) switch
                        {
                            StructuralTypeProjectionExpression projection => AddClientProjection(projection, typeof(ValueBuffer)),
                            SqlExpression mappedSqlExpression => AddClientProjection(mappedSqlExpression, expression.Type.MakeNullable()),
                            // A single-result subquery (e.g. the group element of GroupBy(k).Select(g => g.First()))
                            // being composed over: lower it into the current select as a to-one join so the result
                            // has a bindable shape, instead of failing.
                            ShapedQueryExpression
                            {
                                ResultCardinality: ResultCardinality.Single or ResultCardinality.SingleOrDefault
                            } singleResultSubquery
                                => LowerSingleResultSubquery(projectionBindingExpression, singleResultSubquery),
                            _ => throw new InvalidOperationException(CoreStrings.TranslationFailed(projectionBindingExpression.Print()))
                        };

                    case MaterializeCollectionNavigationExpression materializeCollectionNavigationExpression:
                        if (materializeCollectionNavigationExpression.Navigation.TargetEntityType.IsMappedToJson())
                        {
                            var subquery = materializeCollectionNavigationExpression.Subquery;
                            if (subquery is MethodCallExpression { Method.IsGenericMethod: true } methodCallSubquery)
                            {
                                // strip .Select(x => x) and .AsQueryable() from the JsonCollectionResultExpression
                                if (methodCallSubquery.Method.GetGenericMethodDefinition() == QueryableMethods.Select
                                    && methodCallSubquery.Arguments[0] is MethodCallExpression selectSourceMethod)
                                {
                                    methodCallSubquery = selectSourceMethod;
                                }

                                if (methodCallSubquery.Method.IsGenericMethod
                                    && methodCallSubquery.Method.GetGenericMethodDefinition() == QueryableMethods.AsQueryable)
                                {
                                    subquery = methodCallSubquery.Arguments[0];
                                }
                            }

                            if (subquery is JsonQueryExpression jsonQueryExpression)
                            {
                                Check.DebugAssert(
                                    jsonQueryExpression.IsCollection,
                                    "JsonQueryExpression inside materialize collection should always be a collection.");

                                _clientProjections!.Add(jsonQueryExpression);

                                return new CollectionResultExpression(
                                    new ProjectionBindingExpression(
                                        _selectExpression, _clientProjections!.Count - 1, jsonQueryExpression.Type),
                                    materializeCollectionNavigationExpression.Navigation,
                                    materializeCollectionNavigationExpression.Navigation.ClrType.GetSequenceType());
                            }
                        }

                        _clientProjections!.Add(
                            _queryableMethodTranslatingExpressionVisitor.TranslateSubquery(
                                materializeCollectionNavigationExpression.Subquery)!);

                        return new CollectionResultExpression(
                            // expression.Type will be CLR type of the navigation here so that is fine.
                            new ProjectionBindingExpression(_selectExpression, _clientProjections.Count - 1, expression.Type),
                            materializeCollectionNavigationExpression.Navigation,
                            materializeCollectionNavigationExpression.Navigation.ClrType.GetSequenceType());
                }

                switch (_sqlTranslator.TranslateProjection(expression))
                {
                    case SqlExpression sqlExpression:
                        return AddClientProjection(sqlExpression, expression.Type.MakeNullable());

                    // This handles the case of a complex type being projected out of a Select.
                    case RelationalStructuralTypeShaperExpression { StructuralType: IComplexType } shaper:
                        return base.Visit(shaper);

                    case CollectionResultExpression collectionResult:
                        return base.Visit(collectionResult);
                }

                if (expression is MethodCallExpression methodCallExpression)
                {
                    if (methodCallExpression is
                        {
                            Method.IsGenericMethod: true,
                            Method.Name: nameof(Enumerable.ToList),
                            Method: var method,
                            Arguments: [var argument]
                        }
                        && method.DeclaringType == typeof(Enumerable)
                        && argument.Type.TryGetElementType(typeof(IQueryable<>)) != null)
                    {
                        if (_queryableMethodTranslatingExpressionVisitor.TranslateSubquery(argument) is { } subquery)
                        {
                            _clientProjections!.Add(subquery);
                            // expression.Type here will be List<T>
                            return new CollectionResultExpression(
                                new ProjectionBindingExpression(_selectExpression, _clientProjections.Count - 1, expression.Type),
                                structuralProperty: null,
                                methodCallExpression.Method.GetGenericArguments()[0]);
                        }
                    }
                    else
                    {
                        var subquery = _queryableMethodTranslatingExpressionVisitor.TranslateSubquery(methodCallExpression);
                        if (subquery != null)
                        {
                            _clientProjections!.Add(subquery);
                            var type = expression.Type;
                            if (type.IsGenericType
                                && type.GetGenericTypeDefinition() == typeof(IQueryable<>))
                            {
                                type = typeof(List<>).MakeGenericType(type.GetSequenceType());
                            }

                            var projectionBindingExpression = new ProjectionBindingExpression(
                                _selectExpression, _clientProjections.Count - 1, type);
                            return subquery.ResultCardinality == ResultCardinality.Enumerable
                                ? new CollectionResultExpression(
                                    projectionBindingExpression, structuralProperty: null, subquery.ShaperExpression.Type)
                                : projectionBindingExpression;
                        }
                    }
                }

                return base.Visit(expression);
            }

            default:
            {
                switch (_sqlTranslator.TranslateProjection(expression))
                {
                    case SqlExpression sqlExpression:
                        _projectionMapping[_projectionMembers.Peek()] = sqlExpression;
                        return new ProjectionBindingExpression(
                            _selectExpression, _projectionMembers.Peek(), expression.Type.MakeNullable());

                    // This handles the case of a complex type being projected out of a Select.
                    // Note that an entity type being projected is (currently) handled differently
                    case RelationalStructuralTypeShaperExpression { StructuralType: IComplexType } shaper:
                        return base.Visit(shaper);

                    case CollectionResultExpression collectionResult:
                        return base.Visit(collectionResult);

                    case null or RelationalStructuralTypeShaperExpression { StructuralType: IEntityType }:
                        return QueryCompilationContext.NotTranslatedExpression;

                    default:
                        throw new UnreachableException();
                }
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
[return: NotNullIfNotNull(nameof(expression))]
    public override Expression? Visit(Expression? expression)
    {
        switch (expression)
        {
            case NewExpression or MemberInitExpression or StructuralTypeShaperExpression or IncludeExpression:
                return base.Visit(expression);

            case null:
                return null;

            case not null when _indexBasedBinding:
            {
                switch (expression)
                {
                    case ConstantExpression:
                        return expression;

                    case QueryParameterExpression queryParameterExpression:
                        return Expression.Call(
                            GetParameterValueMethodInfo.MakeGenericMethod(queryParameterExpression.Type),
                            QueryCompilationContext.QueryContextParameter,
                            Expression.Constant(queryParameterExpression.Name));

                    case ParameterExpression parameterExpression:
                        throw new InvalidOperationException(CoreStrings.TranslationFailed(parameterExpression.Print()));

                    case ProjectionBindingExpression projectionBindingExpression:
                        return _selectExpression.GetProjection(projectionBindingExpression) switch
                        {
                            StructuralTypeProjectionExpression projection => AddClientProjection(projection, typeof(ValueBuffer)),
                            SqlExpression mappedSqlExpression => AddClientProjection(mappedSqlExpression, expression.Type.MakeNullable()),
                            // A single-result subquery (e.g. the group element of GroupBy(k).Select(g => g.First()))
                            // being composed over: lower it into the current select as a to-one join so the result
                            // has a bindable shape, instead of failing.
                            ShapedQueryExpression
                            {
                                ResultCardinality: ResultCardinality.Single or ResultCardinality.SingleOrDefault
                            } singleResultSubquery
                                => LowerSingleResultSubquery(projectionBindingExpression, singleResultSubquery),
                            _ => throw new InvalidOperationException(CoreStrings.TranslationFailed(projectionBindingExpression.Print()))
                        };

                    case MaterializeCollectionNavigationExpression materializeCollectionNavigationExpression:
                        if (materializeCollectionNavigationExpression.Navigation.TargetEntityType.IsMappedToJson())
                        {
                            var subquery = materializeCollectionNavigationExpression.Subquery;
                            if (subquery is MethodCallExpression { Method.IsGenericMethod: true } methodCallSubquery)
                            {
                                // strip .Select(x => x) and .AsQueryable() from the JsonCollectionResultExpression
                                if (methodCallSubquery.Method.GetGenericMethodDefinition() == QueryableMethods.Select
                                    && methodCallSubquery.Arguments[0] is MethodCallExpression selectSourceMethod)
                                {
                                    methodCallSubquery = selectSourceMethod;
                                }

                                if (methodCallSubquery.Method.IsGenericMethod
                                    && methodCallSubquery.Method.GetGenericMethodDefinition() == QueryableMethods.AsQueryable)
                                {
                                    subquery = methodCallSubquery.Arguments[0];
                                }
                            }

                            if (subquery is JsonQueryExpression jsonQueryExpression)
                            {
                                Check.DebugAssert(
                                    jsonQueryExpression.IsCollection,
                                    "JsonQueryExpression inside materialize collection should always be a collection.");

                                _clientProjections!.Add(jsonQueryExpression);

                                return new CollectionResultExpression(
                                    new ProjectionBindingExpression(
                                        _selectExpression, _clientProjections!.Count - 1, jsonQueryExpression.Type),
                                    materializeCollectionNavigationExpression.Navigation,
                                    materializeCollectionNavigationExpression.Navigation.ClrType.GetSequenceType());
                            }
                        }

                        _clientProjections!.Add(
                            _queryableMethodTranslatingExpressionVisitor.TranslateSubquery(
                                materializeCollectionNavigationExpression.Subquery)!);

                        return new CollectionResultExpression(
                            // expression.Type will be CLR type of the navigation here so that is fine.
                            new ProjectionBindingExpression(_selectExpression, _clientProjections.Count - 1, expression.Type),
                            materializeCollectionNavigationExpression.Navigation,
                            materializeCollectionNavigationExpression.Navigation.ClrType.GetSequenceType());
                }

                switch (_sqlTranslator.TranslateProjection(expression))
                {
                    case SqlExpression sqlExpression:
                        return AddClientProjection(sqlExpression, expression.Type.MakeNullable());

                    // This handles the case of a complex type being projected out of a Select.
                    case RelationalStructuralTypeShaperExpression { StructuralType: IComplexType } shaper:
                        return base.Visit(shaper);

                    case CollectionResultExpression collectionResult:
                        return base.Visit(collectionResult);
                }

                if (expression is MethodCallExpression methodCallExpression)
                {
                    if (methodCallExpression is
                        {
                            Method.IsGenericMethod: true,
                            Method.Name: nameof(Enumerable.ToList),
                            Method: var method,
                            Arguments: [var argument]
                        }
                        && method.DeclaringType == typeof(Enumerable)
                        && argument.Type.TryGetElementType(typeof(IQueryable<>)) != null)
                    {
                        if (_queryableMethodTranslatingExpressionVisitor.TranslateSubquery(argument) is { } subquery)
                        {
                            _clientProjections!.Add(subquery);
                            // expression.Type here will be List<T>
                            return new CollectionResultExpression(
                                new ProjectionBindingExpression(_selectExpression, _clientProjections.Count - 1, expression.Type),
                                structuralProperty: null,
                                methodCallExpression.Method.GetGenericArguments()[0]);
                        }
                    }
                    else
                    {
                        var subquery = _queryableMethodTranslatingExpressionVisitor.TranslateSubquery(methodCallExpression);
                        if (subquery != null)
                        {
                            _clientProjections!.Add(subquery);
                            var type = expression.Type;
                            if (type.IsGenericType
                                && type.GetGenericTypeDefinition() == typeof(IQueryable<>))
                            {
                                type = typeof(List<>).MakeGenericType(type.GetSequenceType());
                            }

                            var projectionBindingExpression = new ProjectionBindingExpression(
                                _selectExpression, _clientProjections.Count - 1, type);
                            return subquery.ResultCardinality == ResultCardinality.Enumerable
                                ? new CollectionResultExpression(
                                    projectionBindingExpression, structuralProperty: null, subquery.ShaperExpression.Type)
                                : projectionBindingExpression;
                        }
                    }
                }

                return base.Visit(expression);
            }

            default:
            {
                switch (_sqlTranslator.TranslateProjection(expression))
                {
                    case SqlExpression sqlExpression:
                        if (sqlExpression is SqlConstantExpression { Value: not null }
                            && (sqlExpression.Type == typeof(Guid)
                                || sqlExpression.Type == typeof(DateTime)
                                || sqlExpression.Type == typeof(DateOnly)
                                || sqlExpression.Type == typeof(TimeOnly)
                                || sqlExpression.Type == typeof(TimeSpan)
                                || sqlExpression.Type == typeof(DateTimeOffset)))
                        {
                            sqlExpression = new SqlUnaryExpression(ExpressionType.Convert, sqlExpression, sqlExpression.Type, sqlExpression.TypeMapping);
                        }
                        _projectionMapping[_projectionMembers.Peek()] = sqlExpression;
                        return new ProjectionBindingExpression(
                            _selectExpression, _projectionMembers.Peek(), expression.Type.MakeNullable());

                    // This handles the case of a complex type being projected out of a Select.
                    // Note that an entity type being projected is (currently) handled differently
                    case RelationalStructuralTypeShaperExpression { StructuralType: IComplexType } shaper:
                        return base.Visit(shaper);

                    case CollectionResultExpression collectionResult:
                        return base.Visit(collectionResult);

                    case null or RelationalStructuralTypeShaperExpression { StructuralType: IEntityType }:
                        return QueryCompilationContext.NotTranslatedExpression;

                    default:
                        throw new UnreachableException();
                }
            }
        }
    }
```


---

### 🔹 Commit #11: `b62c52f2`
- **完整 Hash**: `b62c52f21921e1114c0144c2f77c18395b29cf5e`
- **說明 (Ground Truth)**: Use ShortName for precompiled query liftable constant variables (#39208)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore/Query/ShapedQueryCompilingExpressionVisitor.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:128, E:132, A:0) ➔ After(N:129, E:133, A:0)
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
  • + [新增節點] `typeBase.ShortName (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `StructuralTypeMaterializerInjector.ProcessStructuralTypeShaper` ──[CALLS]──> `typeBase.ShortName (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `StructuralTypeMaterializerInjector.ProcessStructuralTypeShaper()`
- **變更前簽章 (Before)**: `StructuralTypeMaterializerInjector.ProcessStructuralTypeShaper(StructuralTypeShaperExpression shaper)` (L428~L592)
- **變更後簽章 (After)**: `StructuralTypeMaterializerInjector.ProcessStructuralTypeShaper(StructuralTypeShaperExpression shaper)` (L428~L592)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private Expression ProcessStructuralTypeShaper(StructuralTypeShaperExpression shaper)
        {
            _currentEntityIndex++;

            var expressions = new List<Expression>();
            var variables = new List<ParameterExpression>();

            var typeBase = shaper.StructuralType;
            var clrType = shaper.Type;

            var materializationContextVariable = Variable(
                typeof(MaterializationContext),
                "materializationContext" + _currentEntityIndex);
            variables.Add(materializationContextVariable);
            expressions.Add(
                Assign(
                    materializationContextVariable,
                    New(
                        MaterializationContextConstructor,
                        shaper.ValueBufferExpression,
                        MakeMemberAccess(QueryCompilationContext.QueryContextParameter, DbContextMemberInfo))));

            var valueBufferExpression = Call(materializationContextVariable, MaterializationContext.GetValueBufferMethod);

            var primaryKey = typeBase is IEntityType entityType ? entityType.FindPrimaryKey() : null;

            var concreteEntityTypeVariable = Variable(
                typeBase is IEntityType ? typeof(IEntityType) : typeof(IComplexType),
                "entityType" + _currentEntityIndex);
            variables.Add(concreteEntityTypeVariable);

            var instanceVariable = Variable(clrType, "instance" + _currentEntityIndex);
            variables.Add(instanceVariable);
            expressions.Add(Assign(instanceVariable, Default(clrType)));

            if (_queryStateManager
                && primaryKey != null)
            {
                var entryVariable = Variable(typeof(InternalEntityEntry), "entry" + _currentEntityIndex);
                var hasNullKeyVariable = Variable(typeof(bool), "hasNullKey" + _currentEntityIndex);
                variables.Add(entryVariable);
                variables.Add(hasNullKeyVariable);

                var resolverPrm = Parameter(typeof(MaterializerLiftableConstantContext), "c");
                expressions.Add(
                    Assign(
                        entryVariable,
                        Call(
                            QueryCompilationContext.QueryContextParameter,
                            TryGetEntryMethodInfo,
                            supportsPrecompiledQuery
                                ? liftableConstantFactory.CreateLiftableConstant(
                                    primaryKey,
                                    Lambda<Func<MaterializerLiftableConstantContext, object>>(
                                        Call(
                                            LiftableConstantExpressionHelpers.BuildMemberAccessForEntityOrComplexType(
                                                typeBase, resolverPrm),
                                            EntityTypeFindPrimaryKeyMethod),
                                        resolverPrm),
                                    /*typeBase.Name +*/ "key",
                                    typeof(IKey))
                                : Constant(primaryKey),
                            NewArrayInit(
                                typeof(object),
                                primaryKey.Properties
                                    .Select(p => valueBufferExpression.CreateValueBufferReadValueExpression(
                                        typeof(object),
                                        p.GetIndex(),
                                        p))),
                            Constant(!shaper.IsNullable),
                            hasNullKeyVariable)));

                expressions.Add(
                    IfThen(
                        Not(hasNullKeyVariable),
                        IfThenElse(
                            NotEqual(entryVariable, Default(typeof(InternalEntityEntry))),
                            Block(
                                Assign(concreteEntityTypeVariable, MakeMemberAccess(entryVariable, EntityTypeMemberInfo)),
                                Assign(
                                    instanceVariable, Convert(
                                        MakeMemberAccess(entryVariable, EntityMemberInfo),
                                        clrType))),
                            MaterializeEntity(
                                shaper, materializationContextVariable, concreteEntityTypeVariable, instanceVariable,
                                entryVariable))));
            }
            else
            {
                if (primaryKey != null)
                {
                    if (shaper.IsNullable)
                    {
                        expressions.Add(
                            IfThen(
                                primaryKey.Properties.Select(p => NotEqual(
                                        valueBufferExpression.CreateValueBufferReadValueExpression(typeof(object), p.GetIndex(), p),
                                        Constant(null)))
                                    .Aggregate(AndAlso),
                                MaterializeEntity(
                                    shaper, materializationContextVariable, concreteEntityTypeVariable,
                                    instanceVariable,
                                    null)));
                    }
                    else
                    {
                        var keyValuesVariable = Variable(typeof(object[]), "keyValues" + _currentEntityIndex);
                        var resolverPrm = Parameter(typeof(MaterializerLiftableConstantContext), "c");

                        expressions.Add(
                            IfThenElse(
                                primaryKey.Properties.Select(p => NotEqual(
                                        valueBufferExpression.CreateValueBufferReadValueExpression(typeof(object), p.GetIndex(), p),
                                        Constant(null)))
                                    .Aggregate(AndAlso),
                                MaterializeEntity(
                                    shaper, materializationContextVariable, concreteEntityTypeVariable,
                                    instanceVariable,
                                    null),
                                Block(
                                    [keyValuesVariable],
                                    Assign(
                                        keyValuesVariable,
                                        NewArrayInit(
                                            typeof(object),
                                            primaryKey.Properties.Select(p => valueBufferExpression.CreateValueBufferReadValueExpression(
                                                typeof(object), p.GetIndex(), p)))),
                                    Call(
                                        CreateNullKeyValueInNoTrackingQueryMethod,
                                        supportsPrecompiledQuery
                                            ? liftableConstantFactory.CreateLiftableConstant(
                                                typeBase,
                                                LiftableConstantExpressionHelpers.BuildMemberAccessLambdaForStructuralType(typeBase),
                                                typeBase.Name + "EntityType",
                                                typeof(IEntityType))
                                            : Constant(typeBase),
                                        supportsPrecompiledQuery
                                            ? liftableConstantFactory.CreateLiftableConstant(
                                                primaryKey.Properties,
                                                Lambda<Func<MaterializerLiftableConstantContext, object>>(
                                                    Property(
                                                        Call(
                                                            LiftableConstantExpressionHelpers.BuildMemberAccessForEntityOrComplexType(
                                                                typeBase, resolverPrm),
                                                            EntityTypeFindPrimaryKeyMethod),
                                                        nameof(IKey.Properties)),
                                                    resolverPrm),
                                                typeBase.Name + "PrimaryKeyProperties",
                                                typeof(IReadOnlyList<IProperty>))
                                            : Constant(primaryKey.Properties),
                                        keyValuesVariable))));
                    }
                }
                else
                {
                    expressions.Add(
                        MaterializeEntity(
                            shaper, materializationContextVariable, concreteEntityTypeVariable, instanceVariable,
                            null));
                }
            }

            expressions.Add(instanceVariable);
            return Block(variables, expressions);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private Expression ProcessStructuralTypeShaper(StructuralTypeShaperExpression shaper)
        {
            _currentEntityIndex++;

            var expressions = new List<Expression>();
            var variables = new List<ParameterExpression>();

            var typeBase = shaper.StructuralType;
            var clrType = shaper.Type;

            var materializationContextVariable = Variable(
                typeof(MaterializationContext),
                "materializationContext" + _currentEntityIndex);
            variables.Add(materializationContextVariable);
            expressions.Add(
                Assign(
                    materializationContextVariable,
                    New(
                        MaterializationContextConstructor,
                        shaper.ValueBufferExpression,
                        MakeMemberAccess(QueryCompilationContext.QueryContextParameter, DbContextMemberInfo))));

            var valueBufferExpression = Call(materializationContextVariable, MaterializationContext.GetValueBufferMethod);

            var primaryKey = typeBase is IEntityType entityType ? entityType.FindPrimaryKey() : null;

            var concreteEntityTypeVariable = Variable(
                typeBase is IEntityType ? typeof(IEntityType) : typeof(IComplexType),
                "entityType" + _currentEntityIndex);
            variables.Add(concreteEntityTypeVariable);

            var instanceVariable = Variable(clrType, "instance" + _currentEntityIndex);
            variables.Add(instanceVariable);
            expressions.Add(Assign(instanceVariable, Default(clrType)));

            if (_queryStateManager
                && primaryKey != null)
            {
                var entryVariable = Variable(typeof(InternalEntityEntry), "entry" + _currentEntityIndex);
                var hasNullKeyVariable = Variable(typeof(bool), "hasNullKey" + _currentEntityIndex);
                variables.Add(entryVariable);
                variables.Add(hasNullKeyVariable);

                var resolverPrm = Parameter(typeof(MaterializerLiftableConstantContext), "c");
                expressions.Add(
                    Assign(
                        entryVariable,
                        Call(
                            QueryCompilationContext.QueryContextParameter,
                            TryGetEntryMethodInfo,
                            supportsPrecompiledQuery
                                ? liftableConstantFactory.CreateLiftableConstant(
                                    primaryKey,
                                    Lambda<Func<MaterializerLiftableConstantContext, object>>(
                                        Call(
                                            LiftableConstantExpressionHelpers.BuildMemberAccessForEntityOrComplexType(
                                                typeBase, resolverPrm),
                                            EntityTypeFindPrimaryKeyMethod),
                                        resolverPrm),
                                    typeBase.ShortName() + "Key",
                                    typeof(IKey))
                                : Constant(primaryKey),
                            NewArrayInit(
                                typeof(object),
                                primaryKey.Properties
                                    .Select(p => valueBufferExpression.CreateValueBufferReadValueExpression(
                                        typeof(object),
                                        p.GetIndex(),
                                        p))),
                            Constant(!shaper.IsNullable),
                            hasNullKeyVariable)));

                expressions.Add(
                    IfThen(
                        Not(hasNullKeyVariable),
                        IfThenElse(
                            NotEqual(entryVariable, Default(typeof(InternalEntityEntry))),
                            Block(
                                Assign(concreteEntityTypeVariable, MakeMemberAccess(entryVariable, EntityTypeMemberInfo)),
                                Assign(
                                    instanceVariable, Convert(
                                        MakeMemberAccess(entryVariable, EntityMemberInfo),
                                        clrType))),
                            MaterializeEntity(
                                shaper, materializationContextVariable, concreteEntityTypeVariable, instanceVariable,
                                entryVariable))));
            }
            else
            {
                if (primaryKey != null)
                {
                    if (shaper.IsNullable)
                    {
                        expressions.Add(
                            IfThen(
                                primaryKey.Properties.Select(p => NotEqual(
                                        valueBufferExpression.CreateValueBufferReadValueExpression(typeof(object), p.GetIndex(), p),
                                        Constant(null)))
                                    .Aggregate(AndAlso),
                                MaterializeEntity(
                                    shaper, materializationContextVariable, concreteEntityTypeVariable,
                                    instanceVariable,
                                    null)));
                    }
                    else
                    {
                        var keyValuesVariable = Variable(typeof(object[]), "keyValues" + _currentEntityIndex);
                        var resolverPrm = Parameter(typeof(MaterializerLiftableConstantContext), "c");

                        expressions.Add(
                            IfThenElse(
                                primaryKey.Properties.Select(p => NotEqual(
                                        valueBufferExpression.CreateValueBufferReadValueExpression(typeof(object), p.GetIndex(), p),
                                        Constant(null)))
                                    .Aggregate(AndAlso),
                                MaterializeEntity(
                                    shaper, materializationContextVariable, concreteEntityTypeVariable,
                                    instanceVariable,
                                    null),
                                Block(
                                    [keyValuesVariable],
                                    Assign(
                                        keyValuesVariable,
                                        NewArrayInit(
                                            typeof(object),
                                            primaryKey.Properties.Select(p => valueBufferExpression.CreateValueBufferReadValueExpression(
                                                typeof(object), p.GetIndex(), p)))),
                                    Call(
                                        CreateNullKeyValueInNoTrackingQueryMethod,
                                        supportsPrecompiledQuery
                                            ? liftableConstantFactory.CreateLiftableConstant(
                                                typeBase,
                                                LiftableConstantExpressionHelpers.BuildMemberAccessLambdaForStructuralType(typeBase),
                                                typeBase.ShortName() + "EntityType",
                                                typeof(IEntityType))
                                            : Constant(typeBase),
                                        supportsPrecompiledQuery
                                            ? liftableConstantFactory.CreateLiftableConstant(
                                                primaryKey.Properties,
                                                Lambda<Func<MaterializerLiftableConstantContext, object>>(
                                                    Property(
                                                        Call(
                                                            LiftableConstantExpressionHelpers.BuildMemberAccessForEntityOrComplexType(
                                                                typeBase, resolverPrm),
                                                            EntityTypeFindPrimaryKeyMethod),
                                                        nameof(IKey.Properties)),
                                                    resolverPrm),
                                                typeBase.ShortName() + "PrimaryKeyProperties",
                                                typeof(IReadOnlyList<IProperty>))
                                            : Constant(primaryKey.Properties),
                                        keyValuesVariable))));
                    }
                }
                else
                {
                    expressions.Add(
                        MaterializeEntity(
                            shaper, materializationContextVariable, concreteEntityTypeVariable, instanceVariable,
                            null));
                }
            }

            expressions.Add(instanceVariable);
            return Block(variables, expressions);
        }
```


---

### 🔹 Commit #12: `288d144f`
- **完整 Hash**: `288d144f4f989bd87139870e9e9b1c37e9aaa395`
- **說明 (Ground Truth)**: Don't add an IS NOT NULL filter to unique indexes on required TPT and TPC columns on SQL Server (#39161)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.SqlServer/Metadata/Conventions/SqlServerIndexConvention.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:27, E:25, A:0) ➔ After(N:30, E:28, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 1, +Edges: 3, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `entityTypeBuilder.Metadata.GetDerivedTypesInclusive (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_28` (MODULE_STATE)
  • + [新增節點] `entityType.GetDeclaredIndexes (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `SqlServerIndexConvention.ProcessDiscriminatorPropertySet` (FUNCTION_DEF)
  • - [移除節點] `state_27` (MODULE_STATE)
  • + [新增呼叫邊] `SqlServerIndexConvention.ProcessDiscriminatorPropertySet` ──[CALLS]──> `entityTypeBuilder.Metadata.GetDerivedTypesInclusive (External/BCL)`
  • + [新增呼叫邊] `SqlServerIndexConvention.ProcessDiscriminatorPropertySet` ──[CALLS]──> `entityType.GetDeclaredIndexes (External/BCL)`
  • + [新增呼叫邊] `SqlServerIndexConvention.ProcessDiscriminatorPropertySet` ──[CALLS]──> `SqlServerIndexConvention.SetIndexFilter`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SqlServerIndexConvention.SetIndexFilter()`
- **變更前簽章 (Before)**: `SqlServerIndexConvention.SetIndexFilter(IConventionIndexBuilder indexBuilder, bool columnNameChanged = false)` (L159~L179)
- **變更後簽章 (After)**: `SqlServerIndexConvention.SetIndexFilter(IConventionIndexBuilder indexBuilder, bool regenerate = false)` (L188~L208)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private void SetIndexFilter(IConventionIndexBuilder indexBuilder, bool columnNameChanged = false)
    {
        var index = indexBuilder.Metadata;
        if (index.IsUnique
            && index.IsClustered() != true
            && GetNullableColumns(index) is { Count: > 0 } nullableColumns)
        {
            if (columnNameChanged
                || index.GetFilter() == null)
            {
                indexBuilder.HasFilter(CreateIndexFilter(nullableColumns));
            }
        }
        else
        {
            if (index.GetFilter() != null)
            {
                indexBuilder.HasFilter(null);
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private void SetIndexFilter(IConventionIndexBuilder indexBuilder, bool regenerate = false)
    {
        var index = indexBuilder.Metadata;
        if (index.IsUnique
            && index.IsClustered() != true
            && GetNullableColumns(index) is { Count: > 0 } nullableColumns)
        {
            if (regenerate
                || index.GetFilter() == null)
            {
                indexBuilder.HasFilter(CreateIndexFilter(nullableColumns));
            }
        }
        else
        {
            if (index.GetFilter() != null)
            {
                indexBuilder.HasFilter(null);
            }
        }
    }
```

### 🔹 函式: `SqlServerIndexConvention.ProcessPropertyAnnotationChanged()`
- **變更前簽章 (Before)**: `SqlServerIndexConvention.ProcessPropertyAnnotationChanged(
        IConventionPropertyBuilder propertyBuilder,
        string name,
        IConventionAnnotation? annotation,
        IConventionAnnotation? oldAnnotation,
        IConventionContext<IConventionAnnotation> context)` (L143~L157)
- **變更後簽章 (After)**: `SqlServerIndexConvention.ProcessPropertyAnnotationChanged(
        IConventionPropertyBuilder propertyBuilder,
        string name,
        IConventionAnnotation? annotation,
        IConventionAnnotation? oldAnnotation,
        IConventionContext<IConventionAnnotation> context)` (L172~L186)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public virtual void ProcessPropertyAnnotationChanged(
        IConventionPropertyBuilder propertyBuilder,
        string name,
        IConventionAnnotation? annotation,
        IConventionAnnotation? oldAnnotation,
        IConventionContext<IConventionAnnotation> context)
    {
        if (name == RelationalAnnotationNames.ColumnName)
        {
            foreach (var index in propertyBuilder.Metadata.GetContainingIndexes())
            {
                SetIndexFilter(index.Builder, columnNameChanged: true);
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public virtual void ProcessPropertyAnnotationChanged(
        IConventionPropertyBuilder propertyBuilder,
        string name,
        IConventionAnnotation? annotation,
        IConventionAnnotation? oldAnnotation,
        IConventionContext<IConventionAnnotation> context)
    {
        if (name == RelationalAnnotationNames.ColumnName)
        {
            foreach (var index in propertyBuilder.Metadata.GetContainingIndexes())
            {
                SetIndexFilter(index.Builder, regenerate: true);
            }
        }
    }
```


---

### 🔹 Commit #13: `07addc76`
- **完整 Hash**: `07addc769900cdfd3924a8078b403d38c32e9681`
- **說明 (Ground Truth)**: Read vector dimensions when scaffolding SQL Server databases below compatibility level 170 (#39162)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.SqlServer/Scaffolding/Internal/SqlServerDatabaseModelFactory.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:208, E:309, A:2) ➔ After(N:209, E:310, A:2)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#command** `(Button / UI Control)`
    └── ⚡ **CommandText()**
  🌲 **#command** `(Button / UI Control)`
    └── ⚡ **CommandText()**

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `typeAliases.ContainsKey (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `SqlServerDatabaseModelFactory.GetColumns` ──[CALLS]──> `typeAliases.ContainsKey (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SqlServerDatabaseModelFactory.GetColumns()`
- **變更前簽章 (Before)**: `SqlServerDatabaseModelFactory.GetColumns(
        DbConnection connection,
        IReadOnlyList<DatabaseTable> tables,
        string tableFilter,
        string? viewFilter,
        IReadOnlyDictionary<string, (string storeType, string typeName)> typeAliases,
        string? databaseCollation)` (L682~L863)
- **變更後簽章 (After)**: `SqlServerDatabaseModelFactory.GetColumns(
        DbConnection connection,
        IReadOnlyList<DatabaseTable> tables,
        string tableFilter,
        string? viewFilter,
        IReadOnlyDictionary<string, (string storeType, string typeName)> typeAliases,
        string? databaseCollation)` (L682~L867)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private void GetColumns(
        DbConnection connection,
        IReadOnlyList<DatabaseTable> tables,
        string tableFilter,
        string? viewFilter,
        IReadOnlyDictionary<string, (string storeType, string typeName)> typeAliases,
        string? databaseCollation)
    {
        using var command = connection.CreateCommand();
        var builder = new StringBuilder(
            $"""
SELECT
    SCHEMA_NAME([o].[schema_id]) AS [table_schema],
    [o].[name] AS [table_name],
    [c].[name] AS [column_name],
    [c].[column_id] AS [ordinal],
    SCHEMA_NAME([tp].[schema_id]) AS [type_schema],
    [tp].[name] AS [type_name],
    CAST([c].[max_length] AS int) AS [max_length],
    CAST([c].[precision] AS int) AS [precision],
    CAST([c].[scale] AS int) AS [scale],
    {(_compatibilityLevel is >= 170 ? "[c].[vector_dimensions]" : "NULL as [vector_dimensions]")},
    [c].[is_nullable],
    [c].[is_identity],
    [dc].[definition] AS [default_sql],
    [dc].[name] AS [default_constraint_name],
    [dc].[is_system_named] AS [default_constraint_is_system_named],
    [cc].[definition] AS [computed_sql],
    [cc].[is_persisted] AS [computed_is_persisted],
    CAST([e].[value] AS nvarchar(MAX)) AS [comment],
    [c].[collation_name],
    [c].[is_sparse]
FROM
(
    SELECT [t].[name], [t].[object_id], [t].[schema_id]
    FROM [sys].[tables] t
    WHERE {tableFilter}
""");

        if (SupportsViews)
        {
            Check.DebugAssert(viewFilter is not null);

            builder.AppendLine().Append(
                $"""
    UNION ALL
    SELECT[v].[name], [v].[object_id], [v].[schema_id]
    FROM [sys].[views] v
    WHERE {viewFilter}
""");
        }

        builder.AppendLine().Append(
            """
) o
JOIN [sys].[columns] AS [c] ON [o].[object_id] = [c].[object_id]
LEFT JOIN [sys].[types] AS [tp] ON [c].[user_type_id] = [tp].[user_type_id]
LEFT JOIN [sys].[extended_properties] AS [e] ON [e].[major_id] = [o].[object_id] AND [e].[minor_id] = [c].[column_id] AND [e].[class] = 1 AND [e].[name] = 'MS_Description'
LEFT JOIN [sys].[computed_columns] AS [cc] ON [c].[object_id] = [cc].[object_id] AND [c].[column_id] = [cc].[column_id]
LEFT JOIN [sys].[default_constraints] AS [dc] ON [c].[object_id] = [dc].[parent_object_id] AND [c].[column_id] = [dc].[parent_column_id]
""");

        if (SupportsTemporalTable)
        {
            builder.AppendLine().Append("WHERE [c].[generated_always_type] <> 1 AND [c].[generated_always_type] <> 2");
        }

        builder.AppendLine().Append("ORDER BY [table_schema], [table_name], [c].[column_id];");

        command.CommandText = builder.ToString();

        using var reader = command.ExecuteReader();
        var tableColumnGroups = reader.Cast<DbDataRecord>()
            .GroupBy(ddr => (tableSchema: ddr.GetValueOrDefault<string>("table_schema"),
                tableName: ddr.GetFieldValue<string>("table_name")));

        foreach (var tableColumnGroup in tableColumnGroups)
        {
            var tableSchema = tableColumnGroup.Key.tableSchema;
            var tableName = tableColumnGroup.Key.tableName;

            var table = tables.Single(t => t.Schema == tableSchema && t.Name == tableName);

            foreach (var dataRecord in tableColumnGroup)
            {
                var columnName = dataRecord.GetFieldValue<string>("column_name");
                var ordinal = dataRecord.GetFieldValue<int>("ordinal");
                var dataTypeSchemaName = dataRecord.GetValueOrDefault<string>("type_schema");
                var dataTypeName = dataRecord.GetValueOrDefault<string>("type_name");
                var maxLength = dataRecord.GetValueOrDefault<int>("max_length");
                var precision = dataRecord.GetValueOrDefault<int>("precision");
                var scale = dataRecord.GetValueOrDefault<int>("scale");
                var vectorDimensions = dataRecord.GetValueOrDefault<int>("vector_dimensions");
                var nullable = dataRecord.GetValueOrDefault<bool>("is_nullable");
                var isIdentity = dataRecord.GetValueOrDefault<bool>("is_identity");
                var defaultValueSql = dataRecord.GetValueOrDefault<string>("default_sql");
                var defaultConstraintName = dataRecord.GetValueOrDefault<string>("default_constraint_name");
                var defaultConstraintIsSystemNamed = dataRecord.GetValueOrDefault<bool>("default_constraint_is_system_named");
                var computedValue = dataRecord.GetValueOrDefault<string>("computed_sql");
                var computedIsPersisted = dataRecord.GetValueOrDefault<bool>("computed_is_persisted");
                var comment = dataRecord.GetValueOrDefault<string>("comment");
                var collation = dataRecord.GetValueOrDefault<string>("collation_name");
                var isSparse = dataRecord.GetValueOrDefault<bool>("is_sparse");

                if (dataTypeName is null)
                {
                    _logger.ColumnWithoutTypeWarning(DisplayName(tableSchema, tableName), columnName);
                    continue;
                }

                _logger.ColumnFound(
                    DisplayName(tableSchema, tableName),
                    columnName,
                    ordinal,
                    DisplayName(dataTypeSchemaName, dataTypeName),
                    maxLength,
                    precision,
                    scale,
                    nullable,
                    isIdentity,
                    defaultValueSql,
                    computedValue,
                    computedIsPersisted);

                string storeType;
                string systemTypeName;

                // If the store type is in our loaded aliases dictionary, resolve to the canonical type.
                // Note that the vector type is implemented as an alias for varbinary, but we do not want
                // to scaffold vectors as varbinary.
                var fullQualifiedTypeName = $"[{dataTypeSchemaName}].[{dataTypeName}]";
                if (fullQualifiedTypeName is not "[sys].[vector]"
                    && typeAliases.TryGetValue(fullQualifiedTypeName, out var value))
                {
                    storeType = value.storeType;
                    systemTypeName = value.typeName;
                }
                else
                {
                    storeType = GetStoreType(dataTypeName, maxLength, precision, scale, vectorDimensions);
                    systemTypeName = dataTypeName;
                }

                var column = new DatabaseColumn
                {
                    Table = table,
                    Name = columnName,
                    StoreType = storeType,
                    IsNullable = nullable,
                    DefaultValue = TryParseClrDefault(systemTypeName, defaultValueSql),
                    DefaultValueSql = defaultValueSql,
                    ComputedColumnSql = computedValue,
                    IsStored = computedIsPersisted,
                    Comment = comment,
                    Collation = collation == databaseCollation ? null : collation,
                    ValueGenerated = isIdentity
                        ? ValueGenerated.OnAdd
                        : storeType == "rowversion"
                            ? ValueGenerated.OnAddOrUpdate
                            : default(ValueGenerated?)
                };

                if (storeType == "rowversion")
                {
                    // Note: annotation name must match `ScaffoldingAnnotationNames.ConcurrencyToken`
                    column["ConcurrencyToken"] = true;
                }

                if (isSparse)
                {
                    column[SqlServerAnnotationNames.Sparse] = true;
                }

                if (defaultConstraintName != null && !defaultConstraintIsSystemNamed)
                {
                    column[RelationalAnnotationNames.DefaultConstraintName] = defaultConstraintName;
                }

                table.Columns.Add(column);
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private void GetColumns(
        DbConnection connection,
        IReadOnlyList<DatabaseTable> tables,
        string tableFilter,
        string? viewFilter,
        IReadOnlyDictionary<string, (string storeType, string typeName)> typeAliases,
        string? databaseCollation)
    {
        // The vector type is available under all database compatibility levels, so check whether the server knows
        // the type rather than checking the compatibility level.
        var supportsVectorType = typeAliases.ContainsKey("[sys].[vector]");

        using var command = connection.CreateCommand();
        var builder = new StringBuilder(
            $"""
SELECT
    SCHEMA_NAME([o].[schema_id]) AS [table_schema],
    [o].[name] AS [table_name],
    [c].[name] AS [column_name],
    [c].[column_id] AS [ordinal],
    SCHEMA_NAME([tp].[schema_id]) AS [type_schema],
    [tp].[name] AS [type_name],
    CAST([c].[max_length] AS int) AS [max_length],
    CAST([c].[precision] AS int) AS [precision],
    CAST([c].[scale] AS int) AS [scale],
    {(supportsVectorType ? "[c].[vector_dimensions]" : "NULL as [vector_dimensions]")},
    [c].[is_nullable],
    [c].[is_identity],
    [dc].[definition] AS [default_sql],
    [dc].[name] AS [default_constraint_name],
    [dc].[is_system_named] AS [default_constraint_is_system_named],
    [cc].[definition] AS [computed_sql],
    [cc].[is_persisted] AS [computed_is_persisted],
    CAST([e].[value] AS nvarchar(MAX)) AS [comment],
    [c].[collation_name],
    [c].[is_sparse]
FROM
(
    SELECT [t].[name], [t].[object_id], [t].[schema_id]
    FROM [sys].[tables] t
    WHERE {tableFilter}
""");

        if (SupportsViews)
        {
            Check.DebugAssert(viewFilter is not null);

            builder.AppendLine().Append(
                $"""
    UNION ALL
    SELECT[v].[name], [v].[object_id], [v].[schema_id]
    FROM [sys].[views] v
    WHERE {viewFilter}
""");
        }

        builder.AppendLine().Append(
            """
) o
JOIN [sys].[columns] AS [c] ON [o].[object_id] = [c].[object_id]
LEFT JOIN [sys].[types] AS [tp] ON [c].[user_type_id] = [tp].[user_type_id]
LEFT JOIN [sys].[extended_properties] AS [e] ON [e].[major_id] = [o].[object_id] AND [e].[minor_id] = [c].[column_id] AND [e].[class] = 1 AND [e].[name] = 'MS_Description'
LEFT JOIN [sys].[computed_columns] AS [cc] ON [c].[object_id] = [cc].[object_id] AND [c].[column_id] = [cc].[column_id]
LEFT JOIN [sys].[default_constraints] AS [dc] ON [c].[object_id] = [dc].[parent_object_id] AND [c].[column_id] = [dc].[parent_column_id]
""");

        if (SupportsTemporalTable)
        {
            builder.AppendLine().Append("WHERE [c].[generated_always_type] <> 1 AND [c].[generated_always_type] <> 2");
        }

        builder.AppendLine().Append("ORDER BY [table_schema], [table_name], [c].[column_id];");

        command.CommandText = builder.ToString();

        using var reader = command.ExecuteReader();
        var tableColumnGroups = reader.Cast<DbDataRecord>()
            .GroupBy(ddr => (tableSchema: ddr.GetValueOrDefault<string>("table_schema"),
                tableName: ddr.GetFieldValue<string>("table_name")));

        foreach (var tableColumnGroup in tableColumnGroups)
        {
            var tableSchema = tableColumnGroup.Key.tableSchema;
            var tableName = tableColumnGroup.Key.tableName;

            var table = tables.Single(t => t.Schema == tableSchema && t.Name == tableName);

            foreach (var dataRecord in tableColumnGroup)
            {
                var columnName = dataRecord.GetFieldValue<string>("column_name");
                var ordinal = dataRecord.GetFieldValue<int>("ordinal");
                var dataTypeSchemaName = dataRecord.GetValueOrDefault<string>("type_schema");
                var dataTypeName = dataRecord.GetValueOrDefault<string>("type_name");
                var maxLength = dataRecord.GetValueOrDefault<int>("max_length");
                var precision = dataRecord.GetValueOrDefault<int>("precision");
                var scale = dataRecord.GetValueOrDefault<int>("scale");
                var vectorDimensions = dataRecord.GetValueOrDefault<int>("vector_dimensions");
                var nullable = dataRecord.GetValueOrDefault<bool>("is_nullable");
                var isIdentity = dataRecord.GetValueOrDefault<bool>("is_identity");
                var defaultValueSql = dataRecord.GetValueOrDefault<string>("default_sql");
                var defaultConstraintName = dataRecord.GetValueOrDefault<string>("default_constraint_name");
                var defaultConstraintIsSystemNamed = dataRecord.GetValueOrDefault<bool>("default_constraint_is_system_named");
                var computedValue = dataRecord.GetValueOrDefault<string>("computed_sql");
                var computedIsPersisted = dataRecord.GetValueOrDefault<bool>("computed_is_persisted");
                var comment = dataRecord.GetValueOrDefault<string>("comment");
                var collation = dataRecord.GetValueOrDefault<string>("collation_name");
                var isSparse = dataRecord.GetValueOrDefault<bool>("is_sparse");

                if (dataTypeName is null)
                {
                    _logger.ColumnWithoutTypeWarning(DisplayName(tableSchema, tableName), columnName);
                    continue;
                }

                _logger.ColumnFound(
                    DisplayName(tableSchema, tableName),
                    columnName,
                    ordinal,
                    DisplayName(dataTypeSchemaName, dataTypeName),
                    maxLength,
                    precision,
                    scale,
                    nullable,
                    isIdentity,
                    defaultValueSql,
                    computedValue,
                    computedIsPersisted);

                string storeType;
                string systemTypeName;

                // If the store type is in our loaded aliases dictionary, resolve to the canonical type.
                // Note that the vector type is implemented as an alias for varbinary, but we do not want
                // to scaffold vectors as varbinary.
                var fullQualifiedTypeName = $"[{dataTypeSchemaName}].[{dataTypeName}]";
                if (fullQualifiedTypeName is not "[sys].[vector]"
                    && typeAliases.TryGetValue(fullQualifiedTypeName, out var value))
                {
                    storeType = value.storeType;
                    systemTypeName = value.typeName;
                }
                else
                {
                    storeType = GetStoreType(dataTypeName, maxLength, precision, scale, vectorDimensions);
                    systemTypeName = dataTypeName;
                }

                var column = new DatabaseColumn
                {
                    Table = table,
                    Name = columnName,
                    StoreType = storeType,
                    IsNullable = nullable,
                    DefaultValue = TryParseClrDefault(systemTypeName, defaultValueSql),
                    DefaultValueSql = defaultValueSql,
                    ComputedColumnSql = computedValue,
                    IsStored = computedIsPersisted,
                    Comment = comment,
                    Collation = collation == databaseCollation ? null : collation,
                    ValueGenerated = isIdentity
                        ? ValueGenerated.OnAdd
                        : storeType == "rowversion"
                            ? ValueGenerated.OnAddOrUpdate
                            : default(ValueGenerated?)
                };

                if (storeType == "rowversion")
                {
                    // Note: annotation name must match `ScaffoldingAnnotationNames.ConcurrencyToken`
                    column["ConcurrencyToken"] = true;
                }

                if (isSparse)
                {
                    column[SqlServerAnnotationNames.Sparse] = true;
                }

                if (defaultConstraintName != null && !defaultConstraintIsSystemNamed)
                {
                    column[RelationalAnnotationNames.DefaultConstraintName] = defaultConstraintName;
                }

                table.Columns.Add(column);
            }
        }
    }
```


---

### 🔹 Commit #14: `a8255c14`
- **完整 Hash**: `a8255c147ab736a7a37fd39d1391cbd282b579ed`
- **說明 (Ground Truth)**: Parse the identity seed as a long when generating DBCC CHECKIDENT on SQL Server (#39157)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.SqlServer/Migrations/SqlServerMigrationsSqlGenerator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:551, E:818, A:0) ➔ After(N:553, E:819, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 1, +Edges: 3, -Edges: 2, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `long.TryParse (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `newSeed.ToString (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `builder
                    .Append($"DBCC CHECKIDENT({table}, RESEED, {newSeed.ToString(CultureInfo.InvariantCulture)})")
                    .AppendLine (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `builder
                    .Append($"DBCC CHECKIDENT({table}, RESEED, {newSeed})")
                    .AppendLine (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `SqlServerMigrationsSqlGenerator.Generate` ──[CALLS]──> `builder
                    .Append($"DBCC CHECKIDENT({table}, RESEED, {newSeed.ToString(CultureInfo.InvariantCulture)})")
                    .AppendLine (External/BCL)`
  • + [新增呼叫邊] `SqlServerMigrationsSqlGenerator.Generate` ──[CALLS]──> `newSeed.ToString (External/BCL)`
  • + [新增呼叫邊] `SqlServerMigrationsSqlGenerator.TryParseIdentitySeedIncrement` ──[CALLS]──> `long.TryParse (External/BCL)`
  • - [移除呼叫邊] `SqlServerMigrationsSqlGenerator.Generate` ──[CALLS]──> `builder
                    .Append($"DBCC CHECKIDENT({table}, RESEED, {newSeed})")
                    .AppendLine (External/BCL)`
  • - [移除呼叫邊] `SqlServerMigrationsSqlGenerator.TryParseIdentitySeedIncrement` ──[CALLS]──> `int.TryParse (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SqlServerMigrationsSqlGenerator.Generate()`
- **變更前簽章 (Before)**: `SqlServerMigrationsSqlGenerator.Generate(
        AlterColumnOperation operation,
        IModel? model,
        MigrationCommandListBuilder builder)` (L224~L493)
- **變更後簽章 (After)**: `SqlServerMigrationsSqlGenerator.Generate(
        AlterColumnOperation operation,
        IModel? model,
        MigrationCommandListBuilder builder)` (L224~L493)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override void Generate(
        AlterColumnOperation operation,
        IModel? model,
        MigrationCommandListBuilder builder)
    {
        if (operation[RelationalAnnotationNames.ColumnOrder] != operation.OldColumn[RelationalAnnotationNames.ColumnOrder])
        {
            Dependencies.MigrationsLogger.ColumnOrderIgnoredWarning(operation);
        }

        IEnumerable<ITableIndex>? indexesToRebuild = null;
        var column = model?.GetRelationalModel().FindTable(operation.Table, operation.Schema)
            ?.Columns.FirstOrDefault(c => c.Name == operation.Name);

        if (operation.ComputedColumnSql != operation.OldColumn.ComputedColumnSql
            || operation.IsStored != operation.OldColumn.IsStored)
        {
            var dropColumnOperation = new DropColumnOperation
            {
                Schema = operation.Schema,
                Table = operation.Table,
                Name = operation.Name
            };
            if (column != null)
            {
                dropColumnOperation.AddAnnotations(column.GetAnnotations());
            }

            var addColumnOperation = new AddColumnOperation
            {
                Schema = operation.Schema,
                Table = operation.Table,
                Name = operation.Name,
                ClrType = operation.ClrType,
                ColumnType = operation.ColumnType,
                IsUnicode = operation.IsUnicode,
                IsFixedLength = operation.IsFixedLength,
                MaxLength = operation.MaxLength,
                Precision = operation.Precision,
                Scale = operation.Scale,
                IsRowVersion = operation.IsRowVersion,
                IsNullable = operation.IsNullable,
                DefaultValue = operation.DefaultValue,
                DefaultValueSql = operation.DefaultValueSql,
                ComputedColumnSql = operation.ComputedColumnSql,
                IsStored = operation.IsStored,
                Comment = operation.Comment,
                Collation = operation.Collation
            };
            addColumnOperation.AddAnnotations(operation.GetAnnotations());

            // TODO: Use a column rebuild instead
            indexesToRebuild = GetIndexesToRebuild(column, operation).ToList();
            DropIndexes(indexesToRebuild, builder);
            Generate(dropColumnOperation, model, builder, terminate: false);
            builder.AppendLine(Dependencies.SqlGenerationHelper.StatementTerminator);
            Generate(addColumnOperation, model, builder);
            CreateIndexes(indexesToRebuild, builder);
            builder.EndCommand(suppressTransaction: IsMemoryOptimized(operation, model, operation.Schema, operation.Table));

            return;
        }

        var columnType = operation.ColumnType
            ?? GetColumnType(
                operation.Schema,
                operation.Table,
                operation.Name,
                operation,
                model);

        var narrowed = false;
        var oldColumnSupported = IsOldColumnSupported(model);
        string? oldType = null;

        // SQL Server can't ALTER COLUMN on a computed column when the expression is unchanged; see #33425.
        var computedColumnIsNoOp = operation.ComputedColumnSql != null
            && operation.OldColumn.ComputedColumnSql != null
            && operation.ComputedColumnSql == operation.OldColumn.ComputedColumnSql
            && operation.IsStored == operation.OldColumn.IsStored;

        if (oldColumnSupported && !computedColumnIsNoOp)
        {
            if (IsIdentity(operation) != IsIdentity(operation.OldColumn))
            {
                throw new InvalidOperationException(SqlServerStrings.AlterIdentityColumn);
            }

            oldType = operation.OldColumn.ColumnType
                ?? GetColumnType(
                    operation.Schema,
                    operation.Table,
                    operation.Name,
                    operation.OldColumn,
                    model);
            narrowed = columnType != oldType
                || operation.Collation != operation.OldColumn.Collation
                || operation is { IsNullable: false, OldColumn.IsNullable: true };
        }

        var sparseChanged = ((bool?)operation[SqlServerAnnotationNames.Sparse] ?? false)
            != ((bool?)operation.OldColumn[SqlServerAnnotationNames.Sparse] ?? false);
        if (narrowed || sparseChanged)
        {
            indexesToRebuild = GetIndexesToRebuild(column, operation).ToList();
            DropIndexes(indexesToRebuild, builder);
        }

        // Handle change of identity seed value
        if (IsIdentity(operation) && oldColumnSupported)
        {
            Check.DebugAssert(IsIdentity(operation.OldColumn), "Unsupported column change to identity");

            var oldSeed = 1;
            if (TryParseIdentitySeedIncrement(operation, out var newSeed, out _)
                && (operation.OldColumn[SqlServerAnnotationNames.Identity] is null
                    || TryParseIdentitySeedIncrement(operation.OldColumn, out oldSeed, out _))
                && newSeed != oldSeed)
            {
                var stringTypeMapping = Dependencies.TypeMappingSource.GetMapping(typeof(string));
                var table = stringTypeMapping.GenerateSqlLiteral(
                    Dependencies.SqlGenerationHelper.DelimitIdentifier(operation.Table, operation.Schema));

                builder
                    .Append($"DBCC CHECKIDENT({table}, RESEED, {newSeed})")
                    .AppendLine(Dependencies.SqlGenerationHelper.StatementTerminator);
            }
        }

        var newAnnotations = operation.GetAnnotations().Where(a => a.Name != SqlServerAnnotationNames.Identity);
        var oldAnnotations = operation.OldColumn.GetAnnotations().Where(a => a.Name != SqlServerAnnotationNames.Identity);

        var alterStatementNeeded = narrowed
            || !oldColumnSupported
            || operation.ClrType != operation.OldColumn.ClrType
            || columnType != operation.OldColumn.ColumnType
            || operation.IsUnicode != operation.OldColumn.IsUnicode
            || operation.IsFixedLength != operation.OldColumn.IsFixedLength
            || operation.MaxLength != operation.OldColumn.MaxLength
            || operation.Precision != operation.OldColumn.Precision
            || operation.Scale != operation.OldColumn.Scale
            || operation.IsRowVersion != operation.OldColumn.IsRowVersion
            || operation.IsNullable != operation.OldColumn.IsNullable
            || operation.Collation != operation.OldColumn.Collation
            || HasDifferences(newAnnotations, oldAnnotations);

        if (computedColumnIsNoOp)
        {
            alterStatementNeeded = false;
        }

        var (oldDefaultValue, oldDefaultValueSql) = (operation.OldColumn.DefaultValue, operation.OldColumn.DefaultValueSql);

        if (alterStatementNeeded
            || !Equals(operation.DefaultValue, oldDefaultValue)
            || operation.DefaultValueSql != oldDefaultValueSql)
        {
            var oldDefaultConstraintName = operation.OldColumn[RelationalAnnotationNames.DefaultConstraintName] as string;

            DropDefaultConstraint(operation.Schema, operation.Table, operation.Name, oldDefaultConstraintName, builder);
            (oldDefaultValue, oldDefaultValueSql) = (null, null);
        }

        // The column is being made non-nullable. Generate an update statement before doing that, to convert any existing null values to
        // the default value (otherwise SQL Server fails).
        if (operation is { IsNullable: false, OldColumn.IsNullable: true }
            && (operation.DefaultValueSql is not null || operation.DefaultValue is not null))
        {
            string defaultValueSql;
            if (operation.DefaultValueSql is not null)
            {
                defaultValueSql = operation.DefaultValueSql;
            }
            else
            {
                Check.DebugAssert(operation.DefaultValue is not null);

                var typeMapping = Dependencies.TypeMappingSource.FindMapping(operation.DefaultValue.GetType(), columnType)
                    ?? Dependencies.TypeMappingSource.GetMappingForValue(operation.DefaultValue);

                defaultValueSql = typeMapping.GenerateSqlLiteral(operation.DefaultValue);
            }

            var updateBuilder = new StringBuilder()
                .Append("UPDATE ")
                .Append(Dependencies.SqlGenerationHelper.DelimitIdentifier(operation.Table, operation.Schema))
                .Append(" SET ")
                .Append(Dependencies.SqlGenerationHelper.DelimitIdentifier(operation.Name))
                .Append(" = ")
                .Append(defaultValueSql)
                .Append(" WHERE ")
                .Append(Dependencies.SqlGenerationHelper.DelimitIdentifier(operation.Name))
                .Append(" IS NULL");

            if (Options.HasFlag(MigrationsSqlGenerationOptions.Idempotent))
            {
                builder
                    .Append("EXEC(N'")
                    .Append(updateBuilder.ToString().TrimEnd('\n', '\r', ';').Replace("'", "''"))
                    .Append("')");
            }
            else
            {
                builder.Append(updateBuilder.ToString());
            }

            builder.AppendLine(Dependencies.SqlGenerationHelper.StatementTerminator);
        }

        if (alterStatementNeeded)
        {
            // SQL Server can't ALTER COLUMN from json to a non JSON type; use rename-add-copy-drop instead. See #38364.
            if ((oldType ?? operation.OldColumn.ColumnType)
                ?.Equals("json", StringComparison.OrdinalIgnoreCase)
                == true
                && !columnType.Equals("json", StringComparison.OrdinalIgnoreCase))
            {
                AlterColumnFromJson(operation, columnType, model, builder);
            }
            else
            {
                AppendAlterColumnDefinition(operation, operation.IsNullable, model, builder);
            }
        }

        if (!Equals(operation.DefaultValue, oldDefaultValue) || operation.DefaultValueSql != oldDefaultValueSql)
        {
            var defaultConstraintName = operation[RelationalAnnotationNames.DefaultConstraintName] as string;

            builder
                .Append("ALTER TABLE ")
                .Append(Dependencies.SqlGenerationHelper.DelimitIdentifier(operation.Table, operation.Schema))
                .Append(" ADD");
            DefaultValue(operation.DefaultValue, operation.DefaultValueSql, operation.ColumnType, defaultConstraintName, builder);
            builder
                .Append(" FOR ")
                .Append(Dependencies.SqlGenerationHelper.DelimitIdentifier(operation.Name))
                .AppendLine(Dependencies.SqlGenerationHelper.StatementTerminator);
        }

        if (operation.OldColumn.Comment != operation.Comment)
        {
            var dropDescription = operation.OldColumn.Comment != null;
            if (dropDescription)
            {
                DropDescription(
                    builder,
                    operation.Schema,
                    operation.Table,
                    operation.Name);
            }

            if (operation.Comment != null)
            {
                AddDescription(
                    builder, operation.Comment,
                    operation.Schema,
                    operation.Table,
                    operation.Name,
                    omitVariableDeclarations: dropDescription);
            }
        }

        if (narrowed || sparseChanged)
        {
            CreateIndexes(indexesToRebuild!, builder);
        }

        builder.EndCommand(suppressTransaction: IsMemoryOptimized(operation, model, operation.Schema, operation.Table));
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override void Generate(
        AlterColumnOperation operation,
        IModel? model,
        MigrationCommandListBuilder builder)
    {
        if (operation[RelationalAnnotationNames.ColumnOrder] != operation.OldColumn[RelationalAnnotationNames.ColumnOrder])
        {
            Dependencies.MigrationsLogger.ColumnOrderIgnoredWarning(operation);
        }

        IEnumerable<ITableIndex>? indexesToRebuild = null;
        var column = model?.GetRelationalModel().FindTable(operation.Table, operation.Schema)
            ?.Columns.FirstOrDefault(c => c.Name == operation.Name);

        if (operation.ComputedColumnSql != operation.OldColumn.ComputedColumnSql
            || operation.IsStored != operation.OldColumn.IsStored)
        {
            var dropColumnOperation = new DropColumnOperation
            {
                Schema = operation.Schema,
                Table = operation.Table,
                Name = operation.Name
            };
            if (column != null)
            {
                dropColumnOperation.AddAnnotations(column.GetAnnotations());
            }

            var addColumnOperation = new AddColumnOperation
            {
                Schema = operation.Schema,
                Table = operation.Table,
                Name = operation.Name,
                ClrType = operation.ClrType,
                ColumnType = operation.ColumnType,
                IsUnicode = operation.IsUnicode,
                IsFixedLength = operation.IsFixedLength,
                MaxLength = operation.MaxLength,
                Precision = operation.Precision,
                Scale = operation.Scale,
                IsRowVersion = operation.IsRowVersion,
                IsNullable = operation.IsNullable,
                DefaultValue = operation.DefaultValue,
                DefaultValueSql = operation.DefaultValueSql,
                ComputedColumnSql = operation.ComputedColumnSql,
                IsStored = operation.IsStored,
                Comment = operation.Comment,
                Collation = operation.Collation
            };
            addColumnOperation.AddAnnotations(operation.GetAnnotations());

            // TODO: Use a column rebuild instead
            indexesToRebuild = GetIndexesToRebuild(column, operation).ToList();
            DropIndexes(indexesToRebuild, builder);
            Generate(dropColumnOperation, model, builder, terminate: false);
            builder.AppendLine(Dependencies.SqlGenerationHelper.StatementTerminator);
            Generate(addColumnOperation, model, builder);
            CreateIndexes(indexesToRebuild, builder);
            builder.EndCommand(suppressTransaction: IsMemoryOptimized(operation, model, operation.Schema, operation.Table));

            return;
        }

        var columnType = operation.ColumnType
            ?? GetColumnType(
                operation.Schema,
                operation.Table,
                operation.Name,
                operation,
                model);

        var narrowed = false;
        var oldColumnSupported = IsOldColumnSupported(model);
        string? oldType = null;

        // SQL Server can't ALTER COLUMN on a computed column when the expression is unchanged; see #33425.
        var computedColumnIsNoOp = operation.ComputedColumnSql != null
            && operation.OldColumn.ComputedColumnSql != null
            && operation.ComputedColumnSql == operation.OldColumn.ComputedColumnSql
            && operation.IsStored == operation.OldColumn.IsStored;

        if (oldColumnSupported && !computedColumnIsNoOp)
        {
            if (IsIdentity(operation) != IsIdentity(operation.OldColumn))
            {
                throw new InvalidOperationException(SqlServerStrings.AlterIdentityColumn);
            }

            oldType = operation.OldColumn.ColumnType
                ?? GetColumnType(
                    operation.Schema,
                    operation.Table,
                    operation.Name,
                    operation.OldColumn,
                    model);
            narrowed = columnType != oldType
                || operation.Collation != operation.OldColumn.Collation
                || operation is { IsNullable: false, OldColumn.IsNullable: true };
        }

        var sparseChanged = ((bool?)operation[SqlServerAnnotationNames.Sparse] ?? false)
            != ((bool?)operation.OldColumn[SqlServerAnnotationNames.Sparse] ?? false);
        if (narrowed || sparseChanged)
        {
            indexesToRebuild = GetIndexesToRebuild(column, operation).ToList();
            DropIndexes(indexesToRebuild, builder);
        }

        // Handle change of identity seed value
        if (IsIdentity(operation) && oldColumnSupported)
        {
            Check.DebugAssert(IsIdentity(operation.OldColumn), "Unsupported column change to identity");

            var oldSeed = 1L;
            if (TryParseIdentitySeedIncrement(operation, out var newSeed, out _)
                && (operation.OldColumn[SqlServerAnnotationNames.Identity] is null
                    || TryParseIdentitySeedIncrement(operation.OldColumn, out oldSeed, out _))
                && newSeed != oldSeed)
            {
                var stringTypeMapping = Dependencies.TypeMappingSource.GetMapping(typeof(string));
                var table = stringTypeMapping.GenerateSqlLiteral(
                    Dependencies.SqlGenerationHelper.DelimitIdentifier(operation.Table, operation.Schema));

                builder
                    .Append($"DBCC CHECKIDENT({table}, RESEED, {newSeed.ToString(CultureInfo.InvariantCulture)})")
                    .AppendLine(Dependencies.SqlGenerationHelper.StatementTerminator);
            }
        }

        var newAnnotations = operation.GetAnnotations().Where(a => a.Name != SqlServerAnnotationNames.Identity);
        var oldAnnotations = operation.OldColumn.GetAnnotations().Where(a => a.Name != SqlServerAnnotationNames.Identity);

        var alterStatementNeeded = narrowed
            || !oldColumnSupported
            || operation.ClrType != operation.OldColumn.ClrType
            || columnType != operation.OldColumn.ColumnType
            || operation.IsUnicode != operation.OldColumn.IsUnicode
            || operation.IsFixedLength != operation.OldColumn.IsFixedLength
            || operation.MaxLength != operation.OldColumn.MaxLength
            || operation.Precision != operation.OldColumn.Precision
            || operation.Scale != operation.OldColumn.Scale
            || operation.IsRowVersion != operation.OldColumn.IsRowVersion
            || operation.IsNullable != operation.OldColumn.IsNullable
            || operation.Collation != operation.OldColumn.Collation
            || HasDifferences(newAnnotations, oldAnnotations);

        if (computedColumnIsNoOp)
        {
            alterStatementNeeded = false;
        }

        var (oldDefaultValue, oldDefaultValueSql) = (operation.OldColumn.DefaultValue, operation.OldColumn.DefaultValueSql);

        if (alterStatementNeeded
            || !Equals(operation.DefaultValue, oldDefaultValue)
            || operation.DefaultValueSql != oldDefaultValueSql)
        {
            var oldDefaultConstraintName = operation.OldColumn[RelationalAnnotationNames.DefaultConstraintName] as string;

            DropDefaultConstraint(operation.Schema, operation.Table, operation.Name, oldDefaultConstraintName, builder);
            (oldDefaultValue, oldDefaultValueSql) = (null, null);
        }

        // The column is being made non-nullable. Generate an update statement before doing that, to convert any existing null values to
        // the default value (otherwise SQL Server fails).
        if (operation is { IsNullable: false, OldColumn.IsNullable: true }
            && (operation.DefaultValueSql is not null || operation.DefaultValue is not null))
        {
            string defaultValueSql;
            if (operation.DefaultValueSql is not null)
            {
                defaultValueSql = operation.DefaultValueSql;
            }
            else
            {
                Check.DebugAssert(operation.DefaultValue is not null);

                var typeMapping = Dependencies.TypeMappingSource.FindMapping(operation.DefaultValue.GetType(), columnType)
                    ?? Dependencies.TypeMappingSource.GetMappingForValue(operation.DefaultValue);

                defaultValueSql = typeMapping.GenerateSqlLiteral(operation.DefaultValue);
            }

            var updateBuilder = new StringBuilder()
                .Append("UPDATE ")
                .Append(Dependencies.SqlGenerationHelper.DelimitIdentifier(operation.Table, operation.Schema))
                .Append(" SET ")
                .Append(Dependencies.SqlGenerationHelper.DelimitIdentifier(operation.Name))
                .Append(" = ")
                .Append(defaultValueSql)
                .Append(" WHERE ")
                .Append(Dependencies.SqlGenerationHelper.DelimitIdentifier(operation.Name))
                .Append(" IS NULL");

            if (Options.HasFlag(MigrationsSqlGenerationOptions.Idempotent))
            {
                builder
                    .Append("EXEC(N'")
                    .Append(updateBuilder.ToString().TrimEnd('\n', '\r', ';').Replace("'", "''"))
                    .Append("')");
            }
            else
            {
                builder.Append(updateBuilder.ToString());
            }

            builder.AppendLine(Dependencies.SqlGenerationHelper.StatementTerminator);
        }

        if (alterStatementNeeded)
        {
            // SQL Server can't ALTER COLUMN from json to a non JSON type; use rename-add-copy-drop instead. See #38364.
            if ((oldType ?? operation.OldColumn.ColumnType)
                ?.Equals("json", StringComparison.OrdinalIgnoreCase)
                == true
                && !columnType.Equals("json", StringComparison.OrdinalIgnoreCase))
            {
                AlterColumnFromJson(operation, columnType, model, builder);
            }
            else
            {
                AppendAlterColumnDefinition(operation, operation.IsNullable, model, builder);
            }
        }

        if (!Equals(operation.DefaultValue, oldDefaultValue) || operation.DefaultValueSql != oldDefaultValueSql)
        {
            var defaultConstraintName = operation[RelationalAnnotationNames.DefaultConstraintName] as string;

            builder
                .Append("ALTER TABLE ")
                .Append(Dependencies.SqlGenerationHelper.DelimitIdentifier(operation.Table, operation.Schema))
                .Append(" ADD");
            DefaultValue(operation.DefaultValue, operation.DefaultValueSql, operation.ColumnType, defaultConstraintName, builder);
            builder
                .Append(" FOR ")
                .Append(Dependencies.SqlGenerationHelper.DelimitIdentifier(operation.Name))
                .AppendLine(Dependencies.SqlGenerationHelper.StatementTerminator);
        }

        if (operation.OldColumn.Comment != operation.Comment)
        {
            var dropDescription = operation.OldColumn.Comment != null;
            if (dropDescription)
            {
                DropDescription(
                    builder,
                    operation.Schema,
                    operation.Table,
                    operation.Name);
            }

            if (operation.Comment != null)
            {
                AddDescription(
                    builder, operation.Comment,
                    operation.Schema,
                    operation.Table,
                    operation.Name,
                    omitVariableDeclarations: dropDescription);
            }
        }

        if (narrowed || sparseChanged)
        {
            CreateIndexes(indexesToRebuild!, builder);
        }

        builder.EndCommand(suppressTransaction: IsMemoryOptimized(operation, model, operation.Schema, operation.Table));
    }
```

### 🔹 函式: `SqlServerMigrationsSqlGenerator.TryParseIdentitySeedIncrement()`
- **變更前簽章 (Before)**: `SqlServerMigrationsSqlGenerator.TryParseIdentitySeedIncrement(ColumnOperation operation, out int seed, out int increment)` (L2793~L2806)
- **變更後簽章 (After)**: `SqlServerMigrationsSqlGenerator.TryParseIdentitySeedIncrement(ColumnOperation operation, out long seed, out long increment)` (L2793~L2807)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private static bool TryParseIdentitySeedIncrement(ColumnOperation operation, out int seed, out int increment)
    {
        if (operation[SqlServerAnnotationNames.Identity] is string seedIncrement
            && seedIncrement.Split(",") is [var seedString, var incrementString]
            && int.TryParse(seedString, out var seedParsed)
            && int.TryParse(incrementString, out var incrementParsed))
        {
            (seed, increment) = (seedParsed, incrementParsed);
            return true;
        }

        (seed, increment) = (0, 0);
        return false;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private static bool TryParseIdentitySeedIncrement(ColumnOperation operation, out long seed, out long increment)
    {
        // The seed is a long (see UseIdentityColumn), so a bigint identity column can have a seed above the int range
        if (operation[SqlServerAnnotationNames.Identity] is string seedIncrement
            && seedIncrement.Split(",") is [var seedString, var incrementString]
            && long.TryParse(seedString, NumberStyles.Integer, CultureInfo.InvariantCulture, out var seedParsed)
            && long.TryParse(incrementString, NumberStyles.Integer, CultureInfo.InvariantCulture, out var incrementParsed))
        {
            (seed, increment) = (seedParsed, incrementParsed);
            return true;
        }

        (seed, increment) = (0, 0);
        return false;
    }
```


---

### 🔹 Commit #15: `634135f8`
- **完整 Hash**: `634135f88aaff17de1c774e090cccd8f326d76f0`
- **說明 (Ground Truth)**: Inline char constants as Unicode string literals in SQL Server IndexOf/Replace translations (#39104)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.SqlServer/Query/Internal/Translators/SqlServerStringMethodTranslator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:26, E:38, A:0) ➔ After(N:28, E:44, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 6, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `charValue.ToString (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `SqlServerStringMethodTranslator.ApplyStringTypeMapping` (FUNCTION_DEF)
  • + [新增呼叫邊] `SqlServerStringMethodTranslator.TranslateReplace` ──[CALLS]──> `SqlServerStringMethodTranslator.ApplyStringTypeMapping`
  • + [新增呼叫邊] `SqlServerStringMethodTranslator.TranslateIndexOf` ──[CALLS]──> `SqlServerStringMethodTranslator.ApplyStringTypeMapping`
  • + [新增呼叫邊] `SqlServerStringMethodTranslator.ApplyStringTypeMapping` ──[CALLS]──> `sqlExpressionFactory.Constant (External/BCL)`
  • + [新增呼叫邊] `SqlServerStringMethodTranslator.ApplyStringTypeMapping` ──[CALLS]──> `charValue.ToString (External/BCL)`
  • + [新增呼叫邊] `SqlServerStringMethodTranslator.ApplyStringTypeMapping` ──[CALLS]──> `sqlExpressionFactory.ApplyTypeMapping (External/BCL)`
  • + [新增呼叫邊] `SqlServerStringMethodTranslator.ApplyStringTypeMapping` ──[CALLS]──> `stringTypeMapping.WithComposedConverter (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SqlServerStringMethodTranslator.TranslateIndexOf()`
- **變更前簽章 (Before)**: `SqlServerStringMethodTranslator.TranslateIndexOf(
        SqlExpression instance,
        MethodInfo method,
        SqlExpression searchExpression,
        SqlExpression? startIndex)` (L204~L276)
- **變更後簽章 (After)**: `SqlServerStringMethodTranslator.TranslateIndexOf(
        SqlExpression instance,
        MethodInfo method,
        SqlExpression searchExpression,
        SqlExpression? startIndex)` (L201~L272)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private SqlExpression TranslateIndexOf(
        SqlExpression instance,
        MethodInfo method,
        SqlExpression searchExpression,
        SqlExpression? startIndex)
    {
        var stringTypeMapping = ExpressionExtensions.InferTypeMapping(instance, searchExpression)
            ?? sqlExpressionFactory.ApplyDefaultTypeMapping(instance)!.TypeMapping!;
        searchExpression = sqlExpressionFactory.ApplyTypeMapping(
            searchExpression, searchExpression.Type == typeof(char) ? CharTypeMapping.Default : stringTypeMapping);

        instance = sqlExpressionFactory.ApplyTypeMapping(instance, stringTypeMapping);

        var charIndexArguments = new List<SqlExpression> { searchExpression, instance };

        if (startIndex is not null)
        {
            charIndexArguments.Add(
                startIndex is SqlConstantExpression { Value: int constantStartIndex }
                    ? sqlExpressionFactory.Constant(constantStartIndex + 1, typeof(int))
                    : sqlExpressionFactory.Add(startIndex, sqlExpressionFactory.Constant(1)));
        }

        var argumentsPropagateNullability = Enumerable.Repeat(true, charIndexArguments.Count);

        SqlExpression charIndexExpression;
        var storeType = stringTypeMapping.StoreType;
        if (string.Equals(storeType, "nvarchar(max)", StringComparison.OrdinalIgnoreCase)
            || string.Equals(storeType, "varchar(max)", StringComparison.OrdinalIgnoreCase))
        {
            charIndexExpression = sqlExpressionFactory.Function(
                "CHARINDEX",
                charIndexArguments,
                nullable: true,
                argumentsPropagateNullability,
                typeof(long));

            charIndexExpression = sqlExpressionFactory.Convert(charIndexExpression, typeof(int));
        }
        else
        {
            charIndexExpression = sqlExpressionFactory.Function(
                "CHARINDEX",
                charIndexArguments,
                nullable: true,
                argumentsPropagateNullability,
                method.ReturnType);
        }

        // If the pattern is an empty string, we need to special case to always return 0 (since CHARINDEX return 0, which we'd subtract to
        // -1). Handle separately for constant and non-constant patterns.
        if (searchExpression is SqlConstantExpression { Value: "" })
        {
            return sqlExpressionFactory.Case(
                [new CaseWhenClause(sqlExpressionFactory.IsNotNull(instance), sqlExpressionFactory.Constant(0))],
                elseResult: null
            );
        }

        var offsetExpression = searchExpression is SqlConstantExpression
            ? sqlExpressionFactory.Constant(1)
            : sqlExpressionFactory.Case(
                [
                    new CaseWhenClause(
                        sqlExpressionFactory.Equal(
                            searchExpression,
                            sqlExpressionFactory.Constant(string.Empty, stringTypeMapping)),
                        sqlExpressionFactory.Constant(0))
                ],
                sqlExpressionFactory.Constant(1));

        return sqlExpressionFactory.Subtract(charIndexExpression, offsetExpression);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private SqlExpression TranslateIndexOf(
        SqlExpression instance,
        MethodInfo method,
        SqlExpression searchExpression,
        SqlExpression? startIndex)
    {
        var stringTypeMapping = ExpressionExtensions.InferTypeMapping(instance, searchExpression)
            ?? sqlExpressionFactory.ApplyDefaultTypeMapping(instance)!.TypeMapping!;
        searchExpression = ApplyStringTypeMapping(searchExpression, stringTypeMapping);

        instance = sqlExpressionFactory.ApplyTypeMapping(instance, stringTypeMapping);

        var charIndexArguments = new List<SqlExpression> { searchExpression, instance };

        if (startIndex is not null)
        {
            charIndexArguments.Add(
                startIndex is SqlConstantExpression { Value: int constantStartIndex }
                    ? sqlExpressionFactory.Constant(constantStartIndex + 1, typeof(int))
                    : sqlExpressionFactory.Add(startIndex, sqlExpressionFactory.Constant(1)));
        }

        var argumentsPropagateNullability = Enumerable.Repeat(true, charIndexArguments.Count);

        SqlExpression charIndexExpression;
        var storeType = stringTypeMapping.StoreType;
        if (string.Equals(storeType, "nvarchar(max)", StringComparison.OrdinalIgnoreCase)
            || string.Equals(storeType, "varchar(max)", StringComparison.OrdinalIgnoreCase))
        {
            charIndexExpression = sqlExpressionFactory.Function(
                "CHARINDEX",
                charIndexArguments,
                nullable: true,
                argumentsPropagateNullability,
                typeof(long));

            charIndexExpression = sqlExpressionFactory.Convert(charIndexExpression, typeof(int));
        }
        else
        {
            charIndexExpression = sqlExpressionFactory.Function(
                "CHARINDEX",
                charIndexArguments,
                nullable: true,
                argumentsPropagateNullability,
                method.ReturnType);
        }

        // If the pattern is an empty string, we need to special case to always return 0 (since CHARINDEX return 0, which we'd subtract to
        // -1). Handle separately for constant and non-constant patterns.
        if (searchExpression is SqlConstantExpression { Value: "" })
        {
            return sqlExpressionFactory.Case(
                [new CaseWhenClause(sqlExpressionFactory.IsNotNull(instance), sqlExpressionFactory.Constant(0))],
                elseResult: null
            );
        }

        var offsetExpression = searchExpression is SqlConstantExpression
            ? sqlExpressionFactory.Constant(1)
            : sqlExpressionFactory.Case(
                [
                    new CaseWhenClause(
                        sqlExpressionFactory.Equal(
                            searchExpression,
                            sqlExpressionFactory.Constant(string.Empty, stringTypeMapping)),
                        sqlExpressionFactory.Constant(0))
                ],
                sqlExpressionFactory.Constant(1));

        return sqlExpressionFactory.Subtract(charIndexExpression, offsetExpression);
    }
```

### 🔹 函式: `SqlServerStringMethodTranslator.TranslateReplace()`
- **變更前簽章 (Before)**: `SqlServerStringMethodTranslator.TranslateReplace(
        SqlExpression instance,
        MethodInfo method,
        SqlExpression oldValue,
        SqlExpression newValue)` (L142~L163)
- **變更後簽章 (After)**: `SqlServerStringMethodTranslator.TranslateReplace(
        SqlExpression instance,
        MethodInfo method,
        SqlExpression oldValue,
        SqlExpression newValue)` (L141~L160)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private SqlExpression TranslateReplace(
        SqlExpression instance,
        MethodInfo method,
        SqlExpression oldValue,
        SqlExpression newValue)
    {
        var stringTypeMapping = ExpressionExtensions.InferTypeMapping(instance, oldValue, newValue);

        instance = sqlExpressionFactory.ApplyTypeMapping(instance, stringTypeMapping);
        oldValue = sqlExpressionFactory.ApplyTypeMapping(
            oldValue, oldValue.Type == typeof(char) ? CharTypeMapping.Default : stringTypeMapping);
        newValue = sqlExpressionFactory.ApplyTypeMapping(
            newValue, newValue.Type == typeof(char) ? CharTypeMapping.Default : stringTypeMapping);

        return sqlExpressionFactory.Function(
            "REPLACE",
            [instance, oldValue, newValue],
            nullable: true,
            argumentsPropagateNullability: Statics.TrueArrays[3],
            method.ReturnType,
            stringTypeMapping);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private SqlExpression TranslateReplace(
        SqlExpression instance,
        MethodInfo method,
        SqlExpression oldValue,
        SqlExpression newValue)
    {
        var stringTypeMapping = ExpressionExtensions.InferTypeMapping(instance, oldValue, newValue);

        instance = sqlExpressionFactory.ApplyTypeMapping(instance, stringTypeMapping);
        oldValue = ApplyStringTypeMapping(oldValue, stringTypeMapping);
        newValue = ApplyStringTypeMapping(newValue, stringTypeMapping);

        return sqlExpressionFactory.Function(
            "REPLACE",
            [instance, oldValue, newValue],
            nullable: true,
            argumentsPropagateNullability: Statics.TrueArrays[3],
            method.ReturnType,
            stringTypeMapping);
    }
```


---

### 🔹 Commit #16: `acbbdb67`
- **完整 Hash**: `acbbdb6779e3fe3da90dfddb7fb83f9c0cc90d94`
- **說明 (Ground Truth)**: Fix precompiled queries not capturing parameter symbol (#39149)
- **變更檔案數**: 2

#### 📄 檔案: `src/EFCore.Design/Query/Internal/CSharpToLinqTranslator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:227, E:263, A:0) ➔ After(N:227, E:263, A:0)
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
  • + [新增節點] `state_1286` (MODULE_STATE)
  • - [移除節點] `state_1270` (MODULE_STATE)

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `CSharpToLinqTranslator.VisitIdentifierName()`
- **變更前簽章 (Before)**: `CSharpToLinqTranslator.VisitIdentifierName(IdentifierNameSyntax identifierName)` (L398~L460)
- **變更後簽章 (After)**: `CSharpToLinqTranslator.VisitIdentifierName(IdentifierNameSyntax identifierName)` (L398~L476)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public override Expression VisitIdentifierName(IdentifierNameSyntax identifierName)
    {
        if (_parameterStack.Peek().TryGetValue(identifierName.Identifier.Text, out var parameter))
        {
            return parameter;
        }

        var symbol = _semanticModel.GetSymbolInfo(identifierName).Symbol;

        ITypeSymbol typeSymbol;
        switch (symbol)
        {
            case INamedTypeSymbol s:
                return Constant(ResolveType(s));
            case ILocalSymbol s:
                typeSymbol = s.Type;
                break;
            case IFieldSymbol s:
                typeSymbol = s.Type;
                break;
            case IPropertySymbol s:
                typeSymbol = s.Type;
                break;
            case null:
                throw new InvalidOperationException($"Identifier without symbol: {identifierName}");
            default:
                throw new UnreachableException($"IdentifierName of type {symbol.GetType().Name}: {identifierName}");
        }

        // TODO: Separate out EF Core-specific logic (EF Core would extend this visitor)
        if (typeSymbol.Name.Contains("DbSet"))
        {
            throw new NotImplementedException("DbSet local symbol");
        }

        // We have an identifier which isn't in our parameters stack.

        // First, if the identifier type is the user's DbContext type (e.g. DbContext local variable, or field/property),
        // return a constant over that.
        if (typeSymbol.Equals(_userDbContextSymbol, SymbolEqualityComparer.Default))
        {
            return Constant(_userDbContext);
        }

        // The Translate entry point into the translator uses Roslyn's data flow analysis to locate all local variables flowing in
        // (e.g. captured variables), and populates the _dataFlowsIn dictionary with them (with null values).
        if (symbol is ILocalSymbol localSymbol && _dataFlowsIn.TryGetValue(localSymbol, out var memberExpression))
        {
            // The first time we see a flowing-in variable, we create MemberExpression for it and cache it in _dataFlowsIn.
            return memberExpression
                ?? (_dataFlowsIn[localSymbol] =
                    Field(
                        Constant(new FakeClosureFrameClass()),
                        new FakeFieldInfo(
                            typeof(FakeClosureFrameClass),
                            ResolveType(localSymbol.Type),
                            localSymbol.Name,
                            localSymbol.NullableAnnotation is NullableAnnotation.NotAnnotated)));
        }

        throw new InvalidOperationException(
            $"Encountered unknown identifier name '{identifierName}', which doesn't correspond to a lambda parameter or captured variable");
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public override Expression VisitIdentifierName(IdentifierNameSyntax identifierName)
    {
        if (_parameterStack.Peek().TryGetValue(identifierName.Identifier.Text, out var parameter))
        {
            return parameter;
        }

        var symbol = _semanticModel.GetSymbolInfo(identifierName).Symbol;

        ITypeSymbol typeSymbol;
        switch (symbol)
        {
            case INamedTypeSymbol s:
                return Constant(ResolveType(s));
            case ILocalSymbol s:
                typeSymbol = s.Type;
                break;
            case IFieldSymbol s:
                typeSymbol = s.Type;
                break;
            case IPropertySymbol s:
                typeSymbol = s.Type;
                break;
            case IParameterSymbol s:
                typeSymbol = s.Type;
                break;
            case null:
                throw new InvalidOperationException($"Identifier without symbol: {identifierName}");
            default:
                throw new UnreachableException($"IdentifierName of type {symbol.GetType().Name}: {identifierName}");
        }

        // TODO: Separate out EF Core-specific logic (EF Core would extend this visitor)
        if (typeSymbol.Name.Contains("DbSet"))
        {
            throw new NotImplementedException("DbSet local symbol");
        }

        // We have an identifier which isn't in our parameters stack.

        // First, if the identifier type is the user's DbContext type (e.g. DbContext local variable, or field/property),
        // return a constant over that.
        if (typeSymbol.Equals(_userDbContextSymbol, SymbolEqualityComparer.Default))
        {
            return Constant(_userDbContext);
        }

        // The Translate entry point into the translator uses Roslyn's data flow analysis to locate all local variables flowing in
        // (e.g. captured variables), and populates the _dataFlowsIn dictionary with them (with null values).
        if (symbol is ILocalSymbol localSymbol && _dataFlowsIn.TryGetValue(localSymbol, out var memberExpression))
        {
            // The first time we see a flowing-in variable, we create MemberExpression for it and cache it in _dataFlowsIn.
            return memberExpression
                ?? (_dataFlowsIn[localSymbol] =
                    Field(
                        Constant(new FakeClosureFrameClass()),
                        new FakeFieldInfo(
                            typeof(FakeClosureFrameClass),
                            ResolveType(localSymbol.Type),
                            localSymbol.Name,
                            localSymbol.NullableAnnotation is NullableAnnotation.NotAnnotated)));
        }

        if (symbol is IParameterSymbol parameterSymbol && _dataFlowsIn.TryGetValue(parameterSymbol, out memberExpression))
        {
            return memberExpression
                ?? (_dataFlowsIn[parameterSymbol] =
                    Field(
                        Constant(new FakeClosureFrameClass()),
                        new FakeFieldInfo(
                            typeof(FakeClosureFrameClass),
                            ResolveType(parameterSymbol.Type),
                            parameterSymbol.Name,
                            parameterSymbol.NullableAnnotation is NullableAnnotation.NotAnnotated)));
        }

        throw new InvalidOperationException(
            $"Encountered unknown identifier name '{identifierName}', which doesn't correspond to a lambda parameter or captured variable");
    }
```


#### 📄 檔案: `src/EFCore.Design/Query/Internal/QueryLocator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:46, E:36, A:0) ➔ After(N:46, E:36, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 3, +Edges: 0, -Edges: 0, ΔFuncs: 8, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_333` (MODULE_STATE)
  • + [新增節點] `state_344` (MODULE_STATE)
  • + [新增節點] `state_339` (MODULE_STATE)
  • - [移除節點] `state_340` (MODULE_STATE)
  • - [移除節點] `state_332` (MODULE_STATE)
  • - [移除節點] `state_335` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `state_342()`
- **變更前簽章 (Before)**: `[Module State] state_342` (L342~L342)
- **變更後簽章 (After)**: `[Module State] state_342` (L342~L342)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public readonly INamedTypeSymbol Queryable;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public readonly INamedTypeSymbol IEnumerableOfT;
```

### 🔹 函式: `state_337()`
- **變更前簽章 (Before)**: `[Module State] state_337` (L337~L337)
- **變更後簽章 (After)**: `[Module State] state_337` (L337~L337)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public readonly INamedTypeSymbol DbContext;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public readonly INamedTypeSymbol IQueryable;
```

### 🔹 函式: `state_338()`
- **變更前簽章 (Before)**: `[Module State] state_338` (L338~L338)
- **變更後簽章 (After)**: `[Module State] state_338` (L338~L338)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public readonly INamedTypeSymbol DbSet;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public readonly INamedTypeSymbol DbContext;
```

### 🔹 函式: `QueryLocator.IsDbContext()`
- **變更前簽章 (Before)**: `QueryLocator.IsDbContext(ExpressionSyntax expression)` (L281~L310)
- **變更後簽章 (After)**: `QueryLocator.IsDbContext(ExpressionSyntax expression)` (L281~L311)

#### ◀️ 變更前實作碼 (Before Implementation):
```
bool IsDbContext(ExpressionSyntax expression)
        {
            return _semanticModel.GetSymbolInfo(expression, _cancellationToken).Symbol switch
            {
                ILocalSymbol localSymbol => IsDbContextType(localSymbol.Type),
                IPropertySymbol propertySymbol => IsDbContextType(propertySymbol.Type),
                IFieldSymbol fieldSymbol => IsDbContextType(fieldSymbol.Type),
                IMethodSymbol methodSymbol => IsDbContextType(methodSymbol.ReturnType),
                _ => false
            };

            bool IsDbContextType(ITypeSymbol typeSymbol)
            {
                while (true)
                {
                    // TODO: Check for the user's specific DbContext type #33866
                    if (typeSymbol.Equals(_symbols.DbContext, SymbolEqualityComparer.Default))
                    {
                        return true;
                    }

                    if (typeSymbol.BaseType is null)
                    {
                        return false;
                    }

                    typeSymbol = typeSymbol.BaseType;
                }
            }
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
bool IsDbContext(ExpressionSyntax expression)
        {
            return _semanticModel.GetSymbolInfo(expression, _cancellationToken).Symbol switch
            {
                ILocalSymbol localSymbol => IsDbContextType(localSymbol.Type),
                IPropertySymbol propertySymbol => IsDbContextType(propertySymbol.Type),
                IFieldSymbol fieldSymbol => IsDbContextType(fieldSymbol.Type),
                IMethodSymbol methodSymbol => IsDbContextType(methodSymbol.ReturnType),
                IParameterSymbol parameterSymbol => IsDbContextType(parameterSymbol.Type),
                _ => false
            };

            bool IsDbContextType(ITypeSymbol typeSymbol)
            {
                while (true)
                {
                    // TODO: Check for the user's specific DbContext type #33866
                    if (typeSymbol.Equals(_symbols.DbContext, SymbolEqualityComparer.Default))
                    {
                        return true;
                    }

                    if (typeSymbol.BaseType is null)
                    {
                        return false;
                    }

                    typeSymbol = typeSymbol.BaseType;
                }
            }
        }
```

### 🔹 函式: `state_336()`
- **變更前簽章 (Before)**: `[Module State] state_336` (L336~L336)
- **變更後簽章 (After)**: `[Module State] state_336` (L336~L336)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public readonly INamedTypeSymbol IQueryable;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public readonly INamedTypeSymbol IQueryableOfT;
```

### 🔹 函式: `state_341()`
- **變更前簽章 (Before)**: `[Module State] state_341` (L341~L341)
- **變更後簽章 (After)**: `[Module State] state_341` (L341~L341)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public readonly INamedTypeSymbol IEnumerableOfT;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public readonly INamedTypeSymbol Enumerable;
```

### 🔹 函式: `QueryLocator.ProcessQueryCandidate()`
- **變更前簽章 (Before)**: `QueryLocator.ProcessQueryCandidate(InvocationExpressionSyntax query)` (L233~L311)
- **變更後簽章 (After)**: `QueryLocator.ProcessQueryCandidate(InvocationExpressionSyntax query)` (L233~L312)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private bool ProcessQueryCandidate(InvocationExpressionSyntax query)
    {
        // TODO: Carefully think about exactly what kind of verification we want to do here: static/non-static, actually get the
        // TODO: method symbols and confirm it's an IQueryable flowing all the way through, etc.
        // TODO: Move this code out, for reuse in the inner loop source generator

        // Work backwards through the LINQ operator chain until we reach something that isn't a method invocation
        ExpressionSyntax operatorSyntax = query;
        while (operatorSyntax is InvocationExpressionSyntax
            {
                Expression: MemberAccessExpressionSyntax { Expression: var innerExpression }
            })
        {
            if (innerExpression is QueryExpressionSyntax or ParenthesizedExpressionSyntax { Expression: QueryExpressionSyntax })
            {
                _precompilationErrors.Add(
                    new PrecompiledQueryCodeGenerator.QueryPrecompilationError(
                        query, new InvalidOperationException(DesignStrings.QueryComprehensionSyntaxNotSupportedInPrecompiledQueries)));
                return false;
            }

            operatorSyntax = innerExpression;
        }

        // We've reached a non-invocation.

        // First, check if this is a property access for a DbSet
        if (operatorSyntax is MemberAccessExpressionSyntax { Expression: var innerExpression2 }
            && IsDbContext(innerExpression2))
        {
            _locatedQueries.Add(query);

            // TODO: Check symbol for DbSet?
            return true;
        }

        // If we had context.Set<Blog>(), the Set() method was skipped like any other method, and we're on the context.
        if (IsDbContext(operatorSyntax))
        {
            _locatedQueries.Add(query);
            return true;
        }

        _precompilationErrors.Add(
            new PrecompiledQueryCodeGenerator.QueryPrecompilationError(
                query, new InvalidOperationException(DesignStrings.DynamicQueryNotSupported)));
        return false;

        bool IsDbContext(ExpressionSyntax expression)
        {
            return _semanticModel.GetSymbolInfo(expression, _cancellationToken).Symbol switch
            {
                ILocalSymbol localSymbol => IsDbContextType(localSymbol.Type),
                IPropertySymbol propertySymbol => IsDbContextType(propertySymbol.Type),
                IFieldSymbol fieldSymbol => IsDbContextType(fieldSymbol.Type),
                IMethodSymbol methodSymbol => IsDbContextType(methodSymbol.ReturnType),
                _ => false
            };

            bool IsDbContextType(ITypeSymbol typeSymbol)
            {
                while (true)
                {
                    // TODO: Check for the user's specific DbContext type #33866
                    if (typeSymbol.Equals(_symbols.DbContext, SymbolEqualityComparer.Default))
                    {
                        return true;
                    }

                    if (typeSymbol.BaseType is null)
                    {
                        return false;
                    }

                    typeSymbol = typeSymbol.BaseType;
                }
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private bool ProcessQueryCandidate(InvocationExpressionSyntax query)
    {
        // TODO: Carefully think about exactly what kind of verification we want to do here: static/non-static, actually get the
        // TODO: method symbols and confirm it's an IQueryable flowing all the way through, etc.
        // TODO: Move this code out, for reuse in the inner loop source generator

        // Work backwards through the LINQ operator chain until we reach something that isn't a method invocation
        ExpressionSyntax operatorSyntax = query;
        while (operatorSyntax is InvocationExpressionSyntax
            {
                Expression: MemberAccessExpressionSyntax { Expression: var innerExpression }
            })
        {
            if (innerExpression is QueryExpressionSyntax or ParenthesizedExpressionSyntax { Expression: QueryExpressionSyntax })
            {
                _precompilationErrors.Add(
                    new PrecompiledQueryCodeGenerator.QueryPrecompilationError(
                        query, new InvalidOperationException(DesignStrings.QueryComprehensionSyntaxNotSupportedInPrecompiledQueries)));
                return false;
            }

            operatorSyntax = innerExpression;
        }

        // We've reached a non-invocation.

        // First, check if this is a property access for a DbSet
        if (operatorSyntax is MemberAccessExpressionSyntax { Expression: var innerExpression2 }
            && IsDbContext(innerExpression2))
        {
            _locatedQueries.Add(query);

            // TODO: Check symbol for DbSet?
            return true;
        }

        // If we had context.Set<Blog>(), the Set() method was skipped like any other method, and we're on the context.
        if (IsDbContext(operatorSyntax))
        {
            _locatedQueries.Add(query);
            return true;
        }

        _precompilationErrors.Add(
            new PrecompiledQueryCodeGenerator.QueryPrecompilationError(
                query, new InvalidOperationException(DesignStrings.DynamicQueryNotSupported)));
        return false;

        bool IsDbContext(ExpressionSyntax expression)
        {
            return _semanticModel.GetSymbolInfo(expression, _cancellationToken).Symbol switch
            {
                ILocalSymbol localSymbol => IsDbContextType(localSymbol.Type),
                IPropertySymbol propertySymbol => IsDbContextType(propertySymbol.Type),
                IFieldSymbol fieldSymbol => IsDbContextType(fieldSymbol.Type),
                IMethodSymbol methodSymbol => IsDbContextType(methodSymbol.ReturnType),
                IParameterSymbol parameterSymbol => IsDbContextType(parameterSymbol.Type),
                _ => false
            };

            bool IsDbContextType(ITypeSymbol typeSymbol)
            {
                while (true)
                {
                    // TODO: Check for the user's specific DbContext type #33866
                    if (typeSymbol.Equals(_symbols.DbContext, SymbolEqualityComparer.Default))
                    {
                        return true;
                    }

                    if (typeSymbol.BaseType is null)
                    {
                        return false;
                    }

                    typeSymbol = typeSymbol.BaseType;
                }
            }
        }
    }
```

### 🔹 函式: `state_343()`
- **變更前簽章 (Before)**: `[Module State] state_343` (L343~L343)
- **變更後簽章 (After)**: `[Module State] state_343` (L343~L343)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public readonly INamedTypeSymbol EfQueryableExtensions;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public readonly INamedTypeSymbol Queryable;
```


---

### 🔹 Commit #17: `90ebd100`
- **完整 Hash**: `90ebd1004be01b81b3794a22334e9a6768f3038e`
- **說明 (Ground Truth)**: Query: read nullable value-type GroupBy keys as nullable on the client (#39098)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.Relational/Query/SqlExpressions/SelectExpression.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:535, E:770, A:0) ➔ After(N:535, E:770, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_3140` (MODULE_STATE)
  • - [移除節點] `state_3128` (MODULE_STATE)

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SelectExpression.AddGroupByKeySelectorToProjection()`
- **變更前簽章 (Before)**: `SelectExpression.AddGroupByKeySelectorToProjection(
                    SelectExpression selectExpression,
                    List<Expression> clientProjectionList,
                    Dictionary<SqlExpression, Expression> projectionBindingMap,
                    Expression keySelector)` (L674~L761)
- **變更後簽章 (After)**: `SelectExpression.AddGroupByKeySelectorToProjection(
                    SelectExpression selectExpression,
                    List<Expression> clientProjectionList,
                    Dictionary<SqlExpression, Expression> projectionBindingMap,
                    Expression keySelector)` (L674~L773)

#### ◀️ 變更前實作碼 (Before Implementation):
```
Expression AddGroupByKeySelectorToProjection(
                    SelectExpression selectExpression,
                    List<Expression> clientProjectionList,
                    Dictionary<SqlExpression, Expression> projectionBindingMap,
                    Expression keySelector)
                {
                    switch (keySelector)
                    {
                        case SqlExpression sqlExpression:
                        {
                            var index = selectExpression.AddToProjection(sqlExpression);
                            var clientProjectionToAdd = Constant(index);
                            var existingIndex = clientProjectionList.FindIndex(e
                                => ExpressionEqualityComparer.Instance.Equals(e, clientProjectionToAdd));
                            if (existingIndex == -1)
                            {
                                clientProjectionList.Add(clientProjectionToAdd);
                                existingIndex = clientProjectionList.Count - 1;
                            }

                            var projectionBindingExpression = sqlExpression.Type.IsNullableType()
                                ? (Expression)new ProjectionBindingExpression(selectExpression, existingIndex, sqlExpression.Type)
                                : Convert(
                                    new ProjectionBindingExpression(
                                        selectExpression, existingIndex, sqlExpression.Type.MakeNullable()),
                                    sqlExpression.Type);
                            projectionBindingMap[sqlExpression] = projectionBindingExpression;
                            return projectionBindingExpression;
                        }

                        case NewExpression newExpression:
                            var newArguments = new Expression[newExpression.Arguments.Count];
                            for (var i = 0; i < newExpression.Arguments.Count; i++)
                            {
                                var newArgument = AddGroupByKeySelectorToProjection(
                                    selectExpression, clientProjectionList, projectionBindingMap, newExpression.Arguments[i]);
                                newArguments[i] = newExpression.Arguments[i].Type != newArgument.Type
                                    ? Convert(newArgument, newExpression.Arguments[i].Type)
                                    : newArgument;
                            }

                            return newExpression.Update(newArguments);

                        case MemberInitExpression memberInitExpression:
                            var updatedNewExpression = AddGroupByKeySelectorToProjection(
                                selectExpression, clientProjectionList, projectionBindingMap, memberInitExpression.NewExpression);
                            var newBindings = new MemberBinding[memberInitExpression.Bindings.Count];
                            for (var i = 0; i < newBindings.Length; i++)
                            {
                                var memberAssignment = (MemberAssignment)memberInitExpression.Bindings[i];
                                var newAssignmentExpression = AddGroupByKeySelectorToProjection(
                                    selectExpression, clientProjectionList, projectionBindingMap, memberAssignment.Expression);
                                newBindings[i] = memberAssignment.Update(
                                    memberAssignment.Expression.Type != newAssignmentExpression.Type
                                        ? Convert(newAssignmentExpression, memberAssignment.Expression.Type)
                                        : newAssignmentExpression);
                            }

                            return memberInitExpression.Update((NewExpression)updatedNewExpression, newBindings);

                        case UnaryExpression { NodeType: ExpressionType.Convert or ExpressionType.ConvertChecked } unaryExpression:
                            return unaryExpression.Update(
                                AddGroupByKeySelectorToProjection(
                                    selectExpression, clientProjectionList, projectionBindingMap, unaryExpression.Operand));

                        case StructuralTypeShaperExpression
                        {
                            ValueBufferExpression: StructuralTypeProjectionExpression projection
                        } shaper:
                        {
                            var clientProjectionToAdd = AddStructuralTypeProjection(projection);
                            var existingIndex = clientProjectionList.FindIndex(e
                                => ExpressionEqualityComparer.Instance.Equals(e, clientProjectionToAdd));
                            if (existingIndex == -1)
                            {
                                clientProjectionList.Add(clientProjectionToAdd);
                                existingIndex = clientProjectionList.Count - 1;
                            }

                            return shaper.Update(
                                new ProjectionBindingExpression(selectExpression, existingIndex, typeof(ValueBuffer)));
                        }

                        default:
                            throw new InvalidOperationException(
                                RelationalStrings.InvalidKeySelectorForGroupBy(keySelector, keySelector.GetType()));
                    }
                }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
Expression AddGroupByKeySelectorToProjection(
                    SelectExpression selectExpression,
                    List<Expression> clientProjectionList,
                    Dictionary<SqlExpression, Expression> projectionBindingMap,
                    Expression keySelector)
                {
                    switch (keySelector)
                    {
                        case SqlExpression sqlExpression:
                        {
                            var index = selectExpression.AddToProjection(sqlExpression);
                            var clientProjectionToAdd = Constant(index);
                            var existingIndex = clientProjectionList.FindIndex(e
                                => ExpressionEqualityComparer.Instance.Equals(e, clientProjectionToAdd));
                            if (existingIndex == -1)
                            {
                                clientProjectionList.Add(clientProjectionToAdd);
                                existingIndex = clientProjectionList.Count - 1;
                            }

                            // The key identifier reads the value as nullable so that a null key doesn't throw.
                            var projectionBindingExpression = new ProjectionBindingExpression(
                                selectExpression, existingIndex, sqlExpression.Type.MakeNullable());
                            projectionBindingMap[sqlExpression] = projectionBindingExpression;
                            return sqlExpression.Type.IsNullableType()
                                ? projectionBindingExpression
                                : Convert(projectionBindingExpression, sqlExpression.Type);
                        }

                        case NewExpression newExpression:
                            var newArguments = new Expression[newExpression.Arguments.Count];
                            for (var i = 0; i < newExpression.Arguments.Count; i++)
                            {
                                var newArgument = AddGroupByKeySelectorToProjection(
                                    selectExpression, clientProjectionList, projectionBindingMap, newExpression.Arguments[i]);
                                newArguments[i] = newExpression.Arguments[i].Type != newArgument.Type
                                    ? Convert(newArgument, newExpression.Arguments[i].Type)
                                    : newArgument;
                            }

                            return newExpression.Update(newArguments);

                        case MemberInitExpression memberInitExpression:
                            var updatedNewExpression = AddGroupByKeySelectorToProjection(
                                selectExpression, clientProjectionList, projectionBindingMap, memberInitExpression.NewExpression);
                            var newBindings = new MemberBinding[memberInitExpression.Bindings.Count];
                            for (var i = 0; i < newBindings.Length; i++)
                            {
                                var memberAssignment = (MemberAssignment)memberInitExpression.Bindings[i];
                                var newAssignmentExpression = AddGroupByKeySelectorToProjection(
                                    selectExpression, clientProjectionList, projectionBindingMap, memberAssignment.Expression);
                                newBindings[i] = memberAssignment.Update(
                                    memberAssignment.Expression.Type != newAssignmentExpression.Type
                                        ? Convert(newAssignmentExpression, memberAssignment.Expression.Type)
                                        : newAssignmentExpression);
                            }

                            return memberInitExpression.Update((NewExpression)updatedNewExpression, newBindings);

                        case UnaryExpression { NodeType: ExpressionType.Convert or ExpressionType.ConvertChecked } unaryExpression:
                        {
                            // Also adds the operand to projectionBindingMap, which the nullable read below comes from.
                            var operand = AddGroupByKeySelectorToProjection(
                                selectExpression, clientProjectionList, projectionBindingMap, unaryExpression.Operand);

                            // A nullable or reference-type (e.g. object) key over a SQL expression with a non-nullable CLR type;
                            // converting through the non-nullable operand would throw for a null key.
                            if (unaryExpression is { Operand: SqlExpression sqlOperand, Method: null }
                                && (unaryExpression.Type == sqlOperand.Type.MakeNullable() || !unaryExpression.Type.IsValueType))
                            {
                                var nullableRead = projectionBindingMap[sqlOperand];
                                return nullableRead.Type == unaryExpression.Type ? nullableRead : unaryExpression.Update(nullableRead);
                            }

                            return unaryExpression.Update(operand);
                        }

                        case StructuralTypeShaperExpression
                        {
                            ValueBufferExpression: StructuralTypeProjectionExpression projection
                        } shaper:
                        {
                            var clientProjectionToAdd = AddStructuralTypeProjection(projection);
                            var existingIndex = clientProjectionList.FindIndex(e
                                => ExpressionEqualityComparer.Instance.Equals(e, clientProjectionToAdd));
                            if (existingIndex == -1)
                            {
                                clientProjectionList.Add(clientProjectionToAdd);
                                existingIndex = clientProjectionList.Count - 1;
                            }

                            return shaper.Update(
                                new ProjectionBindingExpression(selectExpression, existingIndex, typeof(ValueBuffer)));
                        }

                        default:
                            throw new InvalidOperationException(
                                RelationalStrings.InvalidKeySelectorForGroupBy(keySelector, keySelector.GetType()));
                    }
                }
```

### 🔹 函式: `SelectExpression.ApplyProjection()`
- **變更前簽章 (Before)**: `SelectExpression.ApplyProjection(
        Expression shaperExpression,
        ResultCardinality resultCardinality,
        QuerySplittingBehavior querySplittingBehavior)` (L553~L1556)
- **變更後簽章 (After)**: `SelectExpression.ApplyProjection(
        Expression shaperExpression,
        ResultCardinality resultCardinality,
        QuerySplittingBehavior querySplittingBehavior)` (L553~L1568)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public Expression ApplyProjection(
        Expression shaperExpression,
        ResultCardinality resultCardinality,
        QuerySplittingBehavior querySplittingBehavior)
    {
        if (!IsMutable)
        {
            throw new InvalidOperationException("Applying projection on already finalized select expression");
        }

        IsMutable = false;
        if (shaperExpression is RelationalGroupByShaperExpression relationalGroupByShaperExpression)
        {
            // This is final GroupBy operation
            Check.DebugAssert(_groupBy.Count > 0, "The selectExpression doesn't have grouping terms.");

            if (_clientProjections.Count == 0)
            {
                // Force client projection because we would be injecting keys and client-side key comparison
                var mapping = ConvertProjectionMappingToClientProjections(_projectionMapping);
                var innerShaperExpression = new ProjectionMemberToIndexConvertingExpressionVisitor(this, mapping).Visit(
                    relationalGroupByShaperExpression.ElementSelector);
                shaperExpression = new RelationalGroupByShaperExpression(
                    relationalGroupByShaperExpression.KeySelector,
                    innerShaperExpression,
                    relationalGroupByShaperExpression.GroupingEnumerable,
                    relationalGroupByShaperExpression.ResultSelector);
            }

            // Convert GroupBy to OrderBy
            foreach (var groupingTerm in _groupBy)
            {
                AppendOrdering(new OrderingExpression(groupingTerm, ascending: true));
            }

            _groupBy.Clear();
            // We do processing of adding key terms to projection when applying projection so we can move offsets for other
            // projections correctly
        }

        if (_clientProjections.Count > 0)
        {
            EntityShaperNullableMarkingExpressionVisitor? entityShaperNullableMarkingExpressionVisitor = null;
            CloningExpressionVisitor? cloningExpressionVisitor = null;
            var pushdownOccurred = false;
            var containsCollection = false;
            var containsSingleResult = false;
            var jsonClientProjectionsCount = 0;

            foreach (var projection in _clientProjections)
            {
                switch (projection)
                {
                    case ShapedQueryExpression { ResultCardinality: ResultCardinality.Enumerable }:
                        containsCollection = true;
                        break;

                    case ShapedQueryExpression { ResultCardinality: ResultCardinality.Single or ResultCardinality.SingleOrDefault }:
                        containsSingleResult = true;
                        break;

                    case JsonQueryExpression:
                        jsonClientProjectionsCount++;
                        break;
                }
            }

            if (containsSingleResult
                || (querySplittingBehavior == QuerySplittingBehavior.SingleQuery && containsCollection))
            {
                // Pushdown outer since we will be adding join to this
                // For grouping query pushdown will not occur since we don't allow this terms to compose (yet!).
                if (Limit != null
                    || Offset != null
                    || IsDistinct
                    || GroupBy.Count > 0)
                {
                    PushdownIntoSubqueryInternal();
                    pushdownOccurred = true;
                }

                entityShaperNullableMarkingExpressionVisitor = new EntityShaperNullableMarkingExpressionVisitor();
            }

            if (querySplittingBehavior == QuerySplittingBehavior.SplitQuery
                && (containsSingleResult || containsCollection))
            {
                // SingleResult can lift collection from inner

                // Specifically for here, we want to avoid cloning the client projection; if we do, when applying the projection on the
                // cloned inner query we go into an endless recursion.

                // Note that we create a CloningExpressionVisitor without a SQL alias manager - this means that aliases won't get uniquified
                // as expressions are being cloned. Since we're cloning here to get a completely separate (split) query, that makes sense
                // as we don't want aliases to be unique across different queries (but in other contexts, when the cloned fragment gets
                // integrated back into the same query (e.g. GroupBy) we do want to uniquify aliases).
                cloningExpressionVisitor = new CloningExpressionVisitor(sqlAliasManager: null, cloneClientProjections: false);
            }

            var earlierClientProjectionCount = _clientProjections.Count;
            var newClientProjections = new List<Expression>();
            var clientProjectionIndexMap = new List<object>();
            var remappingRequired = false;

            if (shaperExpression is RelationalGroupByShaperExpression groupByShaper)
            {
                // We need to add key to projection and generate key selector in terms of projectionBindings
                var projectionBindingMap = new Dictionary<SqlExpression, Expression>();
                var keySelector = AddGroupByKeySelectorToProjection(
                    this, newClientProjections, projectionBindingMap, groupByShaper.KeySelector);
                var (keyIdentifier, keyIdentifierValueComparers) = GetIdentifierAccessor(
                    this, newClientProjections, projectionBindingMap, _identifier);
                // ApplyGrouping only sets this aside when it replaced the identifier with the grouping terms; when the identifier was
                // already part of the key (e.g. grouping by the primary key) it left it alone, and there's nothing to restore.
                if (_preGroupByIdentifier is not null)
                {
                    _identifier.Clear();
                    _identifier.AddRange(_preGroupByIdentifier);
                    _preGroupByIdentifier.Clear();
                }

                Expression AddGroupByKeySelectorToProjection(
                    SelectExpression selectExpression,
                    List<Expression> clientProjectionList,
                    Dictionary<SqlExpression, Expression> projectionBindingMap,
                    Expression keySelector)
                {
                    switch (keySelector)
                    {
                        case SqlExpression sqlExpression:
                        {
                            var index = selectExpression.AddToProjection(sqlExpression);
                            var clientProjectionToAdd = Constant(index);
                            var existingIndex = clientProjectionList.FindIndex(e
                                => ExpressionEqualityComparer.Instance.Equals(e, clientProjectionToAdd));
                            if (existingIndex == -1)
                            {
                                clientProjectionList.Add(clientProjectionToAdd);
                                existingIndex = clientProjectionList.Count - 1;
                            }

                            var projectionBindingExpression = sqlExpression.Type.IsNullableType()
                                ? (Expression)new ProjectionBindingExpression(selectExpression, existingIndex, sqlExpression.Type)
                                : Convert(
                                    new ProjectionBindingExpression(
                                        selectExpression, existingIndex, sqlExpression.Type.MakeNullable()),
                                    sqlExpression.Type);
                            projectionBindingMap[sqlExpression] = projectionBindingExpression;
                            return projectionBindingExpression;
                        }

                        case NewExpression newExpression:
                            var newArguments = new Expression[newExpression.Arguments.Count];
                            for (var i = 0; i < newExpression.Arguments.Count; i++)
                            {
                                var newArgument = AddGroupByKeySelectorToProjection(
                                    selectExpression, clientProjectionList, projectionBindingMap, newExpression.Arguments[i]);
                                newArguments[i] = newExpression.Arguments[i].Type != newArgument.Type
                                    ? Convert(newArgument, newExpression.Arguments[i].Type)
                                    : newArgument;
                            }

                            return newExpression.Update(newArguments);

                        case MemberInitExpression memberInitExpression:
                            var updatedNewExpression = AddGroupByKeySelectorToProjection(
                                selectExpression, clientProjectionList, projectionBindingMap, memberInitExpression.NewExpression);
                            var newBindings = new MemberBinding[memberInitExpression.Bindings.Count];
                            for (var i = 0; i < newBindings.Length; i++)
                            {
                                var memberAssignment = (MemberAssignment)memberInitExpression.Bindings[i];
                                var newAssignmentExpression = AddGroupByKeySelectorToProjection(
                                    selectExpression, clientProjectionList, projectionBindingMap, memberAssignment.Expression);
                                newBindings[i] = memberAssignment.Update(
                                    memberAssignment.Expression.Type != newAssignmentExpression.Type
                                        ? Convert(newAssignmentExpression, memberAssignment.Expression.Type)
                                        : newAssignmentExpression);
                            }

                            return memberInitExpression.Update((NewExpression)updatedNewExpression, newBindings);

                        case UnaryExpression { NodeType: ExpressionType.Convert or ExpressionType.ConvertChecked } unaryExpression:
                            return unaryExpression.Update(
                                AddGroupByKeySelectorToProjection(
                                    selectExpression, clientProjectionList, projectionBindingMap, unaryExpression.Operand));

                        case StructuralTypeShaperExpression
                        {
                            ValueBufferExpression: StructuralTypeProjectionExpression projection
                        } shaper:
                        {
                            var clientProjectionToAdd = AddStructuralTypeProjection(projection);
                            var existingIndex = clientProjectionList.FindIndex(e
                                => ExpressionEqualityComparer.Instance.Equals(e, clientProjectionToAdd));
                            if (existingIndex == -1)
                            {
                                clientProjectionList.Add(clientProjectionToAdd);
                                existingIndex = clientProjectionList.Count - 1;
                            }

                            return shaper.Update(
                                new ProjectionBindingExpression(selectExpression, existingIndex, typeof(ValueBuffer)));
                        }

                        default:
                            throw new InvalidOperationException(
                                RelationalStrings.InvalidKeySelectorForGroupBy(keySelector, keySelector.GetType()));
                    }
                }

                static (Expression, IReadOnlyList<ValueComparer>) GetIdentifierAccessor(
                    SelectExpression selectExpression,
                    List<Expression> clientProjectionList,
                    Dictionary<SqlExpression, Expression> projectionBindingMap,
                    IEnumerable<(ColumnExpression Column, ValueComparer Comparer)> identifyingProjection)
                {
                    var updatedExpressions = new List<Expression>();
                    var comparers = new List<ValueComparer>();
                    foreach (var (column, comparer) in identifyingProjection)
                    {
                        if (!projectionBindingMap.TryGetValue(column, out var mappedExpression))
                        {
                            var index = selectExpression.AddToProjection(column);
                            var clientProjectionToAdd = Constant(index);
                            var existingIndex = clientProjectionList.FindIndex(e
                                => ExpressionEqualityComparer.Instance.Equals(e, clientProjectionToAdd));
                            if (existingIndex == -1)
                            {
                                clientProjectionList.Add(clientProjectionToAdd);
                                existingIndex = clientProjectionList.Count - 1;
                            }

                            mappedExpression = new ProjectionBindingExpression(selectExpression, existingIndex, column.Type.MakeNullable());
                        }

                        updatedExpressions.Add(
                            mappedExpression.Type.IsValueType
                                ? Convert(mappedExpression, typeof(object))
                                : mappedExpression);
                        comparers.Add(comparer);
                    }

                    return (NewArrayInit(typeof(object), updatedExpressions), comparers);
                }

                remappingRequired = true;
                shaperExpression = new RelationalGroupByResultExpression(
                    keyIdentifier, keyIdentifierValueComparers, keySelector, groupByShaper.ElementSelector,
                    groupByShaper.ResultSelector);
            }

            SelectExpression? baseSelectExpression = null;
            if (querySplittingBehavior == QuerySplittingBehavior.SplitQuery && containsCollection)
            {
                // Needs to happen after converting final GroupBy so we clone correct form.
                baseSelectExpression = (SelectExpression)cloningExpressionVisitor!.Visit(this);
                // We mark this as mutable because the split query will combine into this and take it over.
                baseSelectExpression.IsMutable = true;
                if (resultCardinality is ResultCardinality.Single or ResultCardinality.SingleOrDefault)
                {
                    // Update limit since split queries don't need limit 2
                    if (pushdownOccurred)
                    {
                        UpdateLimit((SelectExpression)baseSelectExpression.Tables[0]);
                    }
                    else
                    {
                        UpdateLimit(baseSelectExpression);
                    }

                    static void UpdateLimit(SelectExpression selectExpression)
                    {
                        if (selectExpression.Limit is SqlConstantExpression { Value: 2 } limitConstantExpression)
                        {
                            selectExpression.Limit = new SqlConstantExpression(1, limitConstantExpression.TypeMapping);
                        }
                    }
                }
            }

            for (var i = 0; i < _clientProjections.Count; i++)
            {
                if (i == earlierClientProjectionCount)
                {
                    // Since we lift nested client projections for single results up, we may need to re-clone the baseSelectExpression
                    // again so it does contain the single result subquery too. We erase projections for it since it would be non-empty.
                    earlierClientProjectionCount = _clientProjections.Count;
                    if (cloningExpressionVisitor != null)
                    {
                        baseSelectExpression = (SelectExpression)cloningExpressionVisitor.Visit(this);
                        baseSelectExpression.IsMutable = true;
                        baseSelectExpression._projection.Clear();
                    }
                }

                var value = _clientProjections[i];
                switch (value)
                {
                    case StructuralTypeProjectionExpression projection:
                    {
                        var result = AddStructuralTypeProjection(projection);
                        newClientProjections.Add(result);
                        clientProjectionIndexMap.Add(newClientProjections.Count - 1);

                        break;
                    }

                    case JsonQueryExpression jsonQueryExpression:
                    {
                        var jsonProjectionResult = AddJsonProjection(jsonQueryExpression);
                        newClientProjections.Add(jsonProjectionResult);
                        clientProjectionIndexMap.Add(newClientProjections.Count - 1);

                        break;
                    }

                    case SqlExpression sqlExpression:
                    {
                        var result = Constant(AddToProjection(sqlExpression, _aliasForClientProjections[i]));
                        newClientProjections.Add(result);
                        clientProjectionIndexMap.Add(newClientProjections.Count - 1);

                        break;
                    }

                    case ShapedQueryExpression
                    {
                        ResultCardinality: ResultCardinality.Single or ResultCardinality.SingleOrDefault
                    } shapedQueryExpression:
                    {
                        var innerShaperExpression = LowerSingleResultSubqueryCore(
                            shapedQueryExpression,
                            (projection, alias) =>
                            {
                                _clientProjections.Add(projection);
                                _aliasForClientProjections.Add(alias);
                                return _clientProjections.Count - 1;
                            },
                            entityShaperNullableMarkingExpressionVisitor!);
                        clientProjectionIndexMap.Add(innerShaperExpression);
                        remappingRequired = true;
                        break;
                    }

                    case ShapedQueryExpression { ResultCardinality: ResultCardinality.Enumerable } shapedQueryExpression:
                    {
                        var innerSelectExpression = (SelectExpression)shapedQueryExpression.QueryExpression;
                        if (_identifier.Count == 0
                            || innerSelectExpression._identifier.Count == 0)
                        {
                            throw new InvalidOperationException(
                                RelationalStrings.InsufficientInformationToIdentifyElementOfCollectionJoin);
                        }

                        var innerShaperExpression = shapedQueryExpression.ShaperExpression;
                        if (innerSelectExpression._clientProjections.Count == 0)
                        {
                            var mapping = innerSelectExpression.ConvertProjectionMappingToClientProjections(
                                innerSelectExpression._projectionMapping);
                            innerShaperExpression =
                                new ProjectionMemberToIndexConvertingExpressionVisitor(innerSelectExpression, mapping)
                                    .Visit(innerShaperExpression);
                        }

                        if (querySplittingBehavior == QuerySplittingBehavior.SplitQuery)
                        {
                            var outerSelectExpression = (SelectExpression)cloningExpressionVisitor!.Visit(baseSelectExpression!);

                            // Inject deterministic orderings (the identifier columns) to both the main query and the split query.
                            // Note that just below we pushdown the split query if it has limit/offset/distinct/groupby; this ensures
                            // that the orderings are also propagated to that split subquery if it has limit/offset, which ensures that
                            // that subquery returns the same rows as the main query (#26808)
                            var actualParentIdentifier = _identifier.Take(outerSelectExpression._identifier.Count).ToList();
                            for (var j = 0; j < actualParentIdentifier.Count; j++)
                            {
                                AppendOrderingInternal(new OrderingExpression(actualParentIdentifier[j].Column, ascending: true));
                                outerSelectExpression.AppendOrderingInternal(
                                    new OrderingExpression(outerSelectExpression._identifier[j].Column, ascending: true));
                            }

                            if (outerSelectExpression.Limit != null
                                || outerSelectExpression.Offset != null
                                || outerSelectExpression.IsDistinct
                                || outerSelectExpression._groupBy.Count > 0)
                            {
                                // We do pushdown after making sure that inner contains references to outer only
                                // so that when we do pushdown, we can update inner and maintain graph
                                var sqlRemappingVisitor = outerSelectExpression.PushdownIntoSubqueryInternal();
                                innerSelectExpression = sqlRemappingVisitor.Remap(innerSelectExpression);
                            }

                            var containsOrdering = innerSelectExpression.Orderings.Count > 0;
                            List<OrderingExpression>? orderingsToBeErased = null;
                            if (containsOrdering
                                && innerSelectExpression.Limit == null
                                && innerSelectExpression.Offset == null)
                            {
                                orderingsToBeErased = innerSelectExpression.Orderings.ToList();
                            }

                            var parentIdentifier = GetIdentifierAccessor(this, newClientProjections, actualParentIdentifier).Item1;

                            outerSelectExpression.AddJoin(
                                JoinType.CrossApply, ref innerSelectExpression, out var pushdownOccurredWhenJoining);
                            outerSelectExpression._clientProjections.AddRange(innerSelectExpression._clientProjections);
                            outerSelectExpression._aliasForClientProjections.AddRange(innerSelectExpression._aliasForClientProjections);
                            innerSelectExpression = outerSelectExpression;

                            // Copy over any nested ordering if there were any
                            if (containsOrdering)
                            {
                                var collectionJoinedInnerTable = ((JoinExpressionBase)innerSelectExpression._tables[^1]).Table;
                                var innerOrderingExpressions = new List<OrderingExpression>();
                                if (orderingsToBeErased != null)
                                {
                                    // Ordering was present but erased so we add again
                                    if (pushdownOccurredWhenJoining)
                                    {
                                        // We lift from inner subquery if pushdown occurred with ordering erased
                                        var subquery = (SelectExpression)collectionJoinedInnerTable;
                                        foreach (var ordering in orderingsToBeErased)
                                        {
                                            innerOrderingExpressions.Add(
                                                new OrderingExpression(
                                                    subquery.GenerateOuterColumn(
                                                        collectionJoinedInnerTable.GetRequiredAlias(), ordering.Expression),
                                                    ordering.IsAscending));
                                        }
                                    }
                                    else
                                    {
                                        // We copy from inner if pushdown did not happen but ordering was left behind when
                                        // generating join
                                        innerOrderingExpressions.AddRange(orderingsToBeErased);
                                    }
                                }
                                else
                                {
                                    // If orderings were not erased then they must be present in inner
                                    GetOrderingsFromInnerTable(collectionJoinedInnerTable, innerOrderingExpressions);
                                }

                                foreach (var ordering in innerOrderingExpressions)
                                {
                                    innerSelectExpression.AppendOrdering(ordering);
                                }
                            }

                            innerShaperExpression = innerSelectExpression.ApplyProjection(
                                innerShaperExpression, shapedQueryExpression.ResultCardinality, querySplittingBehavior);

                            var (childIdentifier, childIdentifierValueComparers) = GetIdentifierAccessor(
                                innerSelectExpression,
                                innerSelectExpression._clientProjections,
                                innerSelectExpression._identifier.Take(_identifier.Count));

                            var result = new SplitCollectionInfo(
                                parentIdentifier, childIdentifier, childIdentifierValueComparers,
                                innerSelectExpression, innerShaperExpression);
                            clientProjectionIndexMap.Add(result);
                        }
                        else
                        {
                            var parentIdentifierList = _identifier.Except(_childIdentifiers, IdentifierComparerInstance).ToList();
                            var (parentIdentifier, parentIdentifierValueComparers) = GetIdentifierAccessor(
                                this, newClientProjections, parentIdentifierList);
                            var (outerIdentifier, outerIdentifierValueComparers) = GetIdentifierAccessor(
                                this, newClientProjections, _identifier);

                            foreach (var identifier in _identifier)
                            {
                                AppendOrdering(new OrderingExpression(identifier.Column, ascending: true));
                            }

                            innerShaperExpression = innerSelectExpression.ApplyProjection(
                                innerShaperExpression, shapedQueryExpression.ResultCardinality, querySplittingBehavior);

                            var containsOrdering = innerSelectExpression.Orderings.Count > 0;
                            List<OrderingExpression>? orderingsToBeErased = null;
                            if (containsOrdering
                                && innerSelectExpression.Limit == null
                                && innerSelectExpression.Offset == null)
                            {
                                orderingsToBeErased = innerSelectExpression.Orderings.ToList();
                            }

                            AddJoin(JoinType.OuterApply, ref innerSelectExpression, out var pushdownOccurredWhenJoining);

                            // Copy over any nested ordering if there were any
                            if (containsOrdering)
                            {
                                var collectionJoinedInnerTable = innerSelectExpression._tables[0];
                                var innerOrderingExpressions = new List<OrderingExpression>();
                                if (orderingsToBeErased != null)
                                {
                                    // Ordering was present but erased so we add again
                                    if (pushdownOccurredWhenJoining)
                                    {
                                        // We lift from inner subquery if pushdown occurred with ordering erased
                                        var subquery = (SelectExpression)collectionJoinedInnerTable;
                                        foreach (var ordering in orderingsToBeErased)
                                        {
                                            innerOrderingExpressions.Add(
                                                new OrderingExpression(
                                                    subquery.GenerateOuterColumn(
                                                        collectionJoinedInnerTable.GetRequiredAlias(), ordering.Expression),
                                                    ordering.IsAscending));
                                        }
                                    }
                                    else
                                    {
                                        // We copy from inner if pushdown did not happen but ordering was left behind when
                                        // generating join
                                        innerOrderingExpressions.AddRange(orderingsToBeErased);
                                    }
                                }
                                else
                                {
                                    // If orderings were not erased then they must be present in inner
                                    GetOrderingsFromInnerTable(collectionJoinedInnerTable, innerOrderingExpressions);
                                }

                                foreach (var ordering in innerOrderingExpressions)
                                {
                                    AppendOrdering(ordering.Update(MakeNullable(ordering.Expression, nullable: true)));
                                }
                            }

                            innerShaperExpression = CopyProjectionToOuter(innerSelectExpression, innerShaperExpression);
                            var (selfIdentifier, selfIdentifierValueComparers) = GetIdentifierAccessor(
                                this,
                                newClientProjections,
                                innerSelectExpression._identifier
                                    .Except(innerSelectExpression._childIdentifiers, IdentifierComparerInstance)
                                    .Select(e => (e.Column.MakeNullable(), e.Comparer)));

                            var collectionJoinPredicate = (_tables[^1] as PredicateJoinExpressionBase)?.JoinPredicate;
                            var hasOrderingForJoinKey = false;
                            var hasOrderingForNonJoinKey = false;
                            OrderingExpression? pendingOrdering = null;
                            foreach (var (identifierColumn, identifierComparer) in innerSelectExpression._identifier)
                            {
                                var updatedColumn = identifierColumn.MakeNullable();
                                _childIdentifiers.Add((updatedColumn, identifierComparer));

                                // We omit the last ordering as an optimization
                                var orderingExpression = new OrderingExpression(updatedColumn, ascending: true);

                                if (!_orderings.Any(o => o.Expression.Equals(updatedColumn)))
                                {
                                    if (pendingOrdering is not null)
                                    {
                                        if (orderingExpression.Equals(pendingOrdering))
                                        {
                                            continue;
                                        }

                                        AppendOrderingInternal(pendingOrdering);
                                        TrackOrdering(pendingOrdering.Expression);
                                    }

                                    pendingOrdering = orderingExpression;
                                }
                                else
                                {
                                    TrackOrdering(updatedColumn);
                                }
                            }

                            if (pendingOrdering is not null
                                && hasOrderingForJoinKey
                                && !hasOrderingForNonJoinKey)
                            {
                                // The pending identifier is the only ordering that discriminates elements within the collection.
                                AppendOrderingInternal(pendingOrdering);
                            }

                            void TrackOrdering(SqlExpression ordering)
                            {
                                if (collectionJoinPredicate is not null
                                    && IsJoinKeyColumn(collectionJoinPredicate, ordering))
                                {
                                    hasOrderingForJoinKey = true;
                                }
                                else
                                {
                                    hasOrderingForNonJoinKey = true;
                                }
                            }

                            static bool IsJoinKeyColumn(SqlExpression joinPredicate, SqlExpression column)
                                => joinPredicate switch
                                {
                                    SqlBinaryExpression { OperatorType: ExpressionType.Equal } binary
                                        => IsSameColumn(binary.Left, column) || IsSameColumn(binary.Right, column),
                                    SqlBinaryExpression { OperatorType: ExpressionType.AndAlso } binary
                                        => IsJoinKeyColumn(binary.Left, column) || IsJoinKeyColumn(binary.Right, column),
                                    _ => false
                                };

                            static bool IsSameColumn(SqlExpression left, SqlExpression right)
                                => left is ColumnExpression leftColumn
                                    && right is ColumnExpression rightColumn
                                    && leftColumn.TableAlias == rightColumn.TableAlias
                                    && leftColumn.Name == rightColumn.Name;

                            var result = new SingleCollectionInfo(
                                parentIdentifier, outerIdentifier, selfIdentifier,
                                parentIdentifierValueComparers, outerIdentifierValueComparers, selfIdentifierValueComparers,
                                innerShaperExpression);
                            clientProjectionIndexMap.Add(result);
                        }

                        remappingRequired = true;

                        static (Expression, IReadOnlyList<ValueComparer>) GetIdentifierAccessor(
                            SelectExpression selectExpression,
                            List<Expression> clientProjectionList,
                            IEnumerable<(ColumnExpression Column, ValueComparer Comparer)> identifyingProjection)
                        {
                            var updatedExpressions = new List<Expression>();
                            var comparers = new List<ValueComparer>();
                            foreach (var (column, comparer) in identifyingProjection)
                            {
                                var index = selectExpression.AddToProjection(column, null);
                                var clientProjectionToAdd = Constant(index);
                                var existingIndex = clientProjectionList.FindIndex(e
                                    => ExpressionEqualityComparer.Instance.Equals(e, clientProjectionToAdd));
                                if (existingIndex == -1)
                                {
                                    clientProjectionList.Add(Constant(index));
                                    existingIndex = clientProjectionList.Count - 1;
                                }

                                var projectionBindingExpression = new ProjectionBindingExpression(
                                    selectExpression, existingIndex, column.Type.MakeNullable());

                                updatedExpressions.Add(
                                    projectionBindingExpression.Type.IsValueType
                                        ? Convert(projectionBindingExpression, typeof(object))
                                        : projectionBindingExpression);
                                comparers.Add(comparer);
                            }

                            return (NewArrayInit(typeof(object), updatedExpressions), comparers);
                        }

                        break;
                    }

                    default:
                        throw new InvalidOperationException(value.GetType().ToString());
                }
            }

            if (remappingRequired)
            {
                shaperExpression = new ClientProjectionRemappingExpressionVisitor(clientProjectionIndexMap).Visit(shaperExpression);
            }

            _clientProjections = newClientProjections;
            _aliasForClientProjections.Clear();

            return shaperExpression;

            void GetOrderingsFromInnerTable(TableExpressionBase tableExpressionBase, List<OrderingExpression> orderings)
            {
                var tableAlias = tableExpressionBase.GetRequiredAlias();

                // If operation was converted to predicate join (inner/left join), then ordering will be in a RowNumberExpression
                if (tableExpressionBase is SelectExpression
                    {
                        Tables: [SelectExpression rowNumberSubquery],
                        Predicate: not null
                    } joinedSubquery
                    && rowNumberSubquery.Projection.Select(pe => pe.Expression)
                        .OfType<RowNumberExpression>().SingleOrDefault() is { } rowNumberExpression)
                {
                    var rowNumberSubqueryTableAlias = joinedSubquery.Tables.Single().GetRequiredAlias();
                    foreach (var partition in rowNumberExpression.Partitions)
                    {
                        orderings.Add(
                            new OrderingExpression(
                                joinedSubquery.GenerateOuterColumn(
                                    tableAlias,
                                    rowNumberSubquery.GenerateOuterColumn(rowNumberSubqueryTableAlias, partition)),
                                ascending: true));
                    }

                    foreach (var ordering in rowNumberExpression.Orderings)
                    {
                        orderings.Add(
                            new OrderingExpression(
                                joinedSubquery.GenerateOuterColumn(
                                    tableAlias,
                                    rowNumberSubquery.GenerateOuterColumn(rowNumberSubqueryTableAlias, ordering.Expression)),
                                ordering.IsAscending));
                    }
                }
                // If operation remained apply then ordering will be in the subquery
                else if (tableExpressionBase is SelectExpression { Orderings.Count: > 0 } collectionSelectExpression)
                {
                    foreach (var ordering in collectionSelectExpression.Orderings)
                    {
                        orderings.Add(
                            new OrderingExpression(
                                collectionSelectExpression.GenerateOuterColumn(tableAlias, ordering.Expression),
                                ordering.IsAscending));
                    }
                }
            }

            Expression CopyProjectionToOuter(SelectExpression innerSelectExpression, Expression innerShaperExpression)
            {
                var projectionIndexMap = new int[innerSelectExpression._projection.Count];
                for (var j = 0; j < projectionIndexMap.Length; j++)
                {
                    var projection = MakeNullable(innerSelectExpression._projection[j].Expression, nullable: true);
                    var index = AddToProjection(projection);
                    projectionIndexMap[j] = index;
                }

                var indexMap = new int[innerSelectExpression._clientProjections.Count];
                for (var j = 0; j < indexMap.Length; j++)
                {
                    var constantValue = ((ConstantExpression)innerSelectExpression._clientProjections[j]).Value!;
                    ConstantExpression remappedConstant;
                    switch (((ConstantExpression)innerSelectExpression._clientProjections[j]).Value!)
                    {
                        case Dictionary<IPropertyBase, int> entityDictionary:
                        {
                            var newDictionary = new Dictionary<IPropertyBase, int>(entityDictionary.Count);
                            foreach (var (property, value) in entityDictionary)
                            {
                                newDictionary[property] = projectionIndexMap[value];
                            }

                            remappedConstant = Constant(newDictionary);
                            break;
                        }

                        case JsonProjectionInfo jsonProjectionInfo:
                        {
                            var newKeyAccessInfo = new List<(IProperty?, int?, int?)>();
                            foreach (var (keyProperty, constantKeyValue, keyProjectionIndex) in jsonProjectionInfo.KeyAccessInfo)
                            {
                                newKeyAccessInfo.Add(
                                    (keyProperty, constantKeyValue,
                                        keyProjectionIndex != null ? projectionIndexMap[keyProjectionIndex.Value] : null));
                            }

                            // The outer projection still references the same underlying JSON column; only the
                            // index into the outer projection changes, so preserve JsonColumn for the shaper.
                            remappedConstant = Constant(
                                new JsonProjectionInfo(
                                    projectionIndexMap[jsonProjectionInfo.JsonColumnIndex],
                                    newKeyAccessInfo,
                                    jsonProjectionInfo.JsonColumn));
                            break;
                        }

                        case QueryableJsonProjectionInfo queryableJsonProjectionInfo:
                        {
                            var newPropertyIndexMap =
                                new Dictionary<IPropertyBase, int>(queryableJsonProjectionInfo.PropertyIndexMap.Count);
                            foreach (var (property, value) in queryableJsonProjectionInfo.PropertyIndexMap)
                            {
                                newPropertyIndexMap[property] = projectionIndexMap[value];
                            }

                            var newChildrenProjectionInfo = new List<(JsonProjectionInfo, INavigation)>();
                            foreach (var childProjectionInfo in queryableJsonProjectionInfo.ChildrenProjectionInfo)
                            {
                                var newKeyAccessInfo = new List<(IProperty?, int?, int?)>();
                                foreach (var (keyProperty, constantKeyValue, keyProjectionIndex) in childProjectionInfo.JsonProjectionInfo
                                             .KeyAccessInfo)
                                {
                                    newKeyAccessInfo.Add(
                                        (keyProperty, constantKeyValue,
                                            keyProjectionIndex != null ? projectionIndexMap[keyProjectionIndex.Value] : null));
                                }

                                newChildrenProjectionInfo.Add(
                                    (new JsonProjectionInfo(
                                            projectionIndexMap[childProjectionInfo.JsonProjectionInfo.JsonColumnIndex],
                                            newKeyAccessInfo,
                                            childProjectionInfo.JsonProjectionInfo.JsonColumn),
                                        childProjectionInfo.Navigation));
                            }

                            remappedConstant = Constant(
                                new QueryableJsonProjectionInfo(newPropertyIndexMap, newChildrenProjectionInfo));

                            break;
                        }

                        default:
                            remappedConstant = Constant(projectionIndexMap[(int)constantValue]);
                            break;
                    }

                    newClientProjections.Add(remappedConstant);
                    indexMap[j] = newClientProjections.Count - 1;
                }

                innerSelectExpression._clientProjections.Clear();
                innerSelectExpression._aliasForClientProjections.Clear();
                innerShaperExpression =
                    new ProjectionIndexRemappingExpressionVisitor(innerSelectExpression, this, indexMap).Visit(innerShaperExpression);
                innerShaperExpression = entityShaperNullableMarkingExpressionVisitor!.Visit(innerShaperExpression);

                return innerShaperExpression;
            }
        }

        {
            var result = new Dictionary<ProjectionMember, Expression>(_projectionMapping.Count);

            foreach (var (projectionMember, expression) in _projectionMapping)
            {
                result[projectionMember] = expression switch
                {
                    StructuralTypeProjectionExpression p => AddStructuralTypeProjection(p),
                    JsonQueryExpression p => AddJsonProjection(p),
                    SqlExpression p => Constant(AddToProjection(p, GetProjectionAlias(projectionMember))),
                    _ => throw new UnreachableException("Unexpected expression type in projection mapping.")
                };
            }

            _projectionMapping.Clear();
            _projectionMapping = result;

            return shaperExpression;
        }

        ConstantExpression AddStructuralTypeProjection(StructuralTypeProjectionExpression projection)
        {
            // JSON entity that had some query operations applied on it - it has been converted to a query root via OPENJSON/json_each
            // so it requires different materialization path than regular entity
            // e.g. we need to also add all the child navigations, JSON entity builds all the includes as part of it's own materializer
            // rather than relying on IncludeExpressions in the shaper query
            // also, we don't want to add projection map for synthesized keys, whereas regular entity needs to project every single property it has
            if (projection is { StructuralType: IEntityType entityType }
                && entityType.IsMappedToJson())
            {
                var propertyIndexMap = new Dictionary<IPropertyBase, int>();
                var ownerEntity = entityType;

                do
                {
                    var ownership = ownerEntity.FindOwnership();
                    if (ownership != null)
                    {
                        ownerEntity = ownership.PrincipalEntityType;
                    }
                }
                while (ownerEntity.IsMappedToJson());

                var keyPropertyCount = ownerEntity.FindPrimaryKey()!.Properties.Count;
                foreach (var property in entityType.FindPrimaryKey()!.Properties.Take(keyPropertyCount)
                             .Concat(entityType.GetDeclaredProperties().Where(p => p.GetJsonPropertyName() is not null)))
                {
                    propertyIndexMap[property] = AddToProjection(projection.BindProperty(property), null);
                }

                var childrenProjectionInfo = new List<(JsonProjectionInfo, INavigation)>();
                foreach (var ownedNavigation in entityType.GetNavigations().Where(n => n.TargetEntityType.IsMappedToJson()
                             && n.ForeignKey.IsOwnership
                             && n == n.ForeignKey.PrincipalToDependent))
                {
                    var jsonQueryExpression = (JsonQueryExpression)projection.BindNavigation(ownedNavigation)!.ValueBufferExpression;
                    var jsonProjectionInfo = (JsonProjectionInfo)AddJsonProjection(jsonQueryExpression).Value!;
                    childrenProjectionInfo.Add((jsonProjectionInfo, ownedNavigation));
                }

                return Constant(new QueryableJsonProjectionInfo(propertyIndexMap, childrenProjectionInfo));
            }

            var projections = new Dictionary<IPropertyBase, int>();

            ProcessType(projection);

            void ProcessType(StructuralTypeProjectionExpression typeProjection)
            {
                foreach (var property in typeProjection.StructuralType.GetPropertiesInHierarchy())
                {
                    if (typeProjection is { StructuralType: IEntityType entityType }
                        && entityType.IsMappedToJson()
                        && property.IsOrdinalKeyProperty())
                    {
                        continue;
                    }

                    if (!property.IsAutoLoaded)
                    {
                        continue;
                    }

                    projections[property] = AddToProjection(typeProjection.BindProperty(property), alias: null);
                }

                foreach (var complexProperty in GetAllComplexPropertiesInHierarchy(typeProjection.StructuralType))
                {
                    switch (typeProjection.BindComplexProperty(complexProperty))
                    {
                        case StructuralTypeShaperExpression { ValueBufferExpression: StructuralTypeProjectionExpression nestedProjection }:
                            ProcessType(nestedProjection);
                            break;

                        // Complex (not owned) JSON, single (non-collection)
                        case StructuralTypeShaperExpression { ValueBufferExpression: JsonQueryExpression jsonQuery }:
                            projections[complexProperty] = ((JsonProjectionInfo)AddJsonProjection(jsonQuery).Value!).JsonColumnIndex;
                            break;

                        // Complex (not owned) JSON, collection
                        case CollectionResultExpression { QueryExpression: JsonQueryExpression jsonQuery }:
                            projections[complexProperty] = ((JsonProjectionInfo)AddJsonProjection(jsonQuery).Value!).JsonColumnIndex;
                            break;

                        default:
                            throw new UnreachableException(
                                "Unexpected complex property binding when building structural type projection.");
                    }
                }
            }

            if (projection.DiscriminatorExpression is not null)
            {
                AddToProjection(projection.DiscriminatorExpression, DiscriminatorColumnAlias);
            }

            return Constant(projections);
        }

        ConstantExpression AddJsonProjection(JsonQueryExpression jsonQueryExpression)
        {
            var jsonScalarExpression = new JsonScalarExpression(
                jsonQueryExpression.JsonColumn,
                jsonQueryExpression.Path,
                jsonQueryExpression.JsonColumn.Type,
                jsonQueryExpression.JsonColumn.TypeMapping!,
                jsonQueryExpression.IsNullable);

            _projection.Add(new ProjectionExpression(jsonScalarExpression, ""));
            var jsonColumnIndex = _projection.Count - 1;
            var keyAccessInfo = new List<(IProperty?, int?, int?)>();

            switch (jsonQueryExpression.StructuralType)
            {
                case IEntityType entityType:
                    var keyProperties = GetMappedKeyProperties(entityType.FindPrimaryKey()!);
                    foreach (var keyProperty in keyProperties)
                    {
                        var keyColumn = jsonQueryExpression.BindProperty(keyProperty);
                        keyAccessInfo.Add((keyProperty, null, AddToProjection(keyColumn)));
                    }

                    foreach (var elementAccessSegment in jsonScalarExpression.Path.Where(x => x.ArrayIndex != null))
                    {
                        if (elementAccessSegment.ArrayIndex is SqlConstantExpression { Value: int intValue })
                        {
                            keyAccessInfo.Add((null, intValue, null));
                        }
                        else
                        {
                            keyAccessInfo.Add((null, null, AddToProjection(elementAccessSegment.ArrayIndex!)));
                        }
                    }

                    break;

                case IComplexType complexType:
                    break;

                default:
                    throw new UnreachableException("Unexpected structural type when building JSON projection.");
            }

            return Constant(new JsonProjectionInfo(jsonColumnIndex, keyAccessInfo, jsonQueryExpression.JsonColumn.Column));
        }

        static IReadOnlyList<IProperty> GetMappedKeyProperties(IKey key)
        {
            if (!key.DeclaringEntityType.IsMappedToJson())
            {
                return key.Properties;
            }

            // TODO: fix this once we enable json entity being owned by another owned non-json entity (issue #28441)

            // for json collections we need to filter out the ordinal key as it's not mapped to any column
            // there could be multiple of these in deeply nested structures,
            // so we traverse to the outermost owner to see how many mapped keys there are
            var currentEntity = key.DeclaringEntityType;
            while (currentEntity.IsMappedToJson())
            {
                currentEntity = currentEntity.FindOwnership()!.PrincipalEntityType;
            }

            var count = currentEntity.FindPrimaryKey()!.Properties.Count;

            return key.Properties.Take(count).ToList();
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public Expression ApplyProjection(
        Expression shaperExpression,
        ResultCardinality resultCardinality,
        QuerySplittingBehavior querySplittingBehavior)
    {
        if (!IsMutable)
        {
            throw new InvalidOperationException("Applying projection on already finalized select expression");
        }

        IsMutable = false;
        if (shaperExpression is RelationalGroupByShaperExpression relationalGroupByShaperExpression)
        {
            // This is final GroupBy operation
            Check.DebugAssert(_groupBy.Count > 0, "The selectExpression doesn't have grouping terms.");

            if (_clientProjections.Count == 0)
            {
                // Force client projection because we would be injecting keys and client-side key comparison
                var mapping = ConvertProjectionMappingToClientProjections(_projectionMapping);
                var innerShaperExpression = new ProjectionMemberToIndexConvertingExpressionVisitor(this, mapping).Visit(
                    relationalGroupByShaperExpression.ElementSelector);
                shaperExpression = new RelationalGroupByShaperExpression(
                    relationalGroupByShaperExpression.KeySelector,
                    innerShaperExpression,
                    relationalGroupByShaperExpression.GroupingEnumerable,
                    relationalGroupByShaperExpression.ResultSelector);
            }

            // Convert GroupBy to OrderBy
            foreach (var groupingTerm in _groupBy)
            {
                AppendOrdering(new OrderingExpression(groupingTerm, ascending: true));
            }

            _groupBy.Clear();
            // We do processing of adding key terms to projection when applying projection so we can move offsets for other
            // projections correctly
        }

        if (_clientProjections.Count > 0)
        {
            EntityShaperNullableMarkingExpressionVisitor? entityShaperNullableMarkingExpressionVisitor = null;
            CloningExpressionVisitor? cloningExpressionVisitor = null;
            var pushdownOccurred = false;
            var containsCollection = false;
            var containsSingleResult = false;
            var jsonClientProjectionsCount = 0;

            foreach (var projection in _clientProjections)
            {
                switch (projection)
                {
                    case ShapedQueryExpression { ResultCardinality: ResultCardinality.Enumerable }:
                        containsCollection = true;
                        break;

                    case ShapedQueryExpression { ResultCardinality: ResultCardinality.Single or ResultCardinality.SingleOrDefault }:
                        containsSingleResult = true;
                        break;

                    case JsonQueryExpression:
                        jsonClientProjectionsCount++;
                        break;
                }
            }

            if (containsSingleResult
                || (querySplittingBehavior == QuerySplittingBehavior.SingleQuery && containsCollection))
            {
                // Pushdown outer since we will be adding join to this
                // For grouping query pushdown will not occur since we don't allow this terms to compose (yet!).
                if (Limit != null
                    || Offset != null
                    || IsDistinct
                    || GroupBy.Count > 0)
                {
                    PushdownIntoSubqueryInternal();
                    pushdownOccurred = true;
                }

                entityShaperNullableMarkingExpressionVisitor = new EntityShaperNullableMarkingExpressionVisitor();
            }

            if (querySplittingBehavior == QuerySplittingBehavior.SplitQuery
                && (containsSingleResult || containsCollection))
            {
                // SingleResult can lift collection from inner

                // Specifically for here, we want to avoid cloning the client projection; if we do, when applying the projection on the
                // cloned inner query we go into an endless recursion.

                // Note that we create a CloningExpressionVisitor without a SQL alias manager - this means that aliases won't get uniquified
                // as expressions are being cloned. Since we're cloning here to get a completely separate (split) query, that makes sense
                // as we don't want aliases to be unique across different queries (but in other contexts, when the cloned fragment gets
                // integrated back into the same query (e.g. GroupBy) we do want to uniquify aliases).
                cloningExpressionVisitor = new CloningExpressionVisitor(sqlAliasManager: null, cloneClientProjections: false);
            }

            var earlierClientProjectionCount = _clientProjections.Count;
            var newClientProjections = new List<Expression>();
            var clientProjectionIndexMap = new List<object>();
            var remappingRequired = false;

            if (shaperExpression is RelationalGroupByShaperExpression groupByShaper)
            {
                // We need to add key to projection and generate key selector in terms of projectionBindings
                var projectionBindingMap = new Dictionary<SqlExpression, Expression>();
                var keySelector = AddGroupByKeySelectorToProjection(
                    this, newClientProjections, projectionBindingMap, groupByShaper.KeySelector);
                var (keyIdentifier, keyIdentifierValueComparers) = GetIdentifierAccessor(
                    this, newClientProjections, projectionBindingMap, _identifier);
                // ApplyGrouping only sets this aside when it replaced the identifier with the grouping terms; when the identifier was
                // already part of the key (e.g. grouping by the primary key) it left it alone, and there's nothing to restore.
                if (_preGroupByIdentifier is not null)
                {
                    _identifier.Clear();
                    _identifier.AddRange(_preGroupByIdentifier);
                    _preGroupByIdentifier.Clear();
                }

                Expression AddGroupByKeySelectorToProjection(
                    SelectExpression selectExpression,
                    List<Expression> clientProjectionList,
                    Dictionary<SqlExpression, Expression> projectionBindingMap,
                    Expression keySelector)
                {
                    switch (keySelector)
                    {
                        case SqlExpression sqlExpression:
                        {
                            var index = selectExpression.AddToProjection(sqlExpression);
                            var clientProjectionToAdd = Constant(index);
                            var existingIndex = clientProjectionList.FindIndex(e
                                => ExpressionEqualityComparer.Instance.Equals(e, clientProjectionToAdd));
                            if (existingIndex == -1)
                            {
                                clientProjectionList.Add(clientProjectionToAdd);
                                existingIndex = clientProjectionList.Count - 1;
                            }

                            // The key identifier reads the value as nullable so that a null key doesn't throw.
                            var projectionBindingExpression = new ProjectionBindingExpression(
                                selectExpression, existingIndex, sqlExpression.Type.MakeNullable());
                            projectionBindingMap[sqlExpression] = projectionBindingExpression;
                            return sqlExpression.Type.IsNullableType()
                                ? projectionBindingExpression
                                : Convert(projectionBindingExpression, sqlExpression.Type);
                        }

                        case NewExpression newExpression:
                            var newArguments = new Expression[newExpression.Arguments.Count];
                            for (var i = 0; i < newExpression.Arguments.Count; i++)
                            {
                                var newArgument = AddGroupByKeySelectorToProjection(
                                    selectExpression, clientProjectionList, projectionBindingMap, newExpression.Arguments[i]);
                                newArguments[i] = newExpression.Arguments[i].Type != newArgument.Type
                                    ? Convert(newArgument, newExpression.Arguments[i].Type)
                                    : newArgument;
                            }

                            return newExpression.Update(newArguments);

                        case MemberInitExpression memberInitExpression:
                            var updatedNewExpression = AddGroupByKeySelectorToProjection(
                                selectExpression, clientProjectionList, projectionBindingMap, memberInitExpression.NewExpression);
                            var newBindings = new MemberBinding[memberInitExpression.Bindings.Count];
                            for (var i = 0; i < newBindings.Length; i++)
                            {
                                var memberAssignment = (MemberAssignment)memberInitExpression.Bindings[i];
                                var newAssignmentExpression = AddGroupByKeySelectorToProjection(
                                    selectExpression, clientProjectionList, projectionBindingMap, memberAssignment.Expression);
                                newBindings[i] = memberAssignment.Update(
                                    memberAssignment.Expression.Type != newAssignmentExpression.Type
                                        ? Convert(newAssignmentExpression, memberAssignment.Expression.Type)
                                        : newAssignmentExpression);
                            }

                            return memberInitExpression.Update((NewExpression)updatedNewExpression, newBindings);

                        case UnaryExpression { NodeType: ExpressionType.Convert or ExpressionType.ConvertChecked } unaryExpression:
                        {
                            // Also adds the operand to projectionBindingMap, which the nullable read below comes from.
                            var operand = AddGroupByKeySelectorToProjection(
                                selectExpression, clientProjectionList, projectionBindingMap, unaryExpression.Operand);

                            // A nullable or reference-type (e.g. object) key over a SQL expression with a non-nullable CLR type;
                            // converting through the non-nullable operand would throw for a null key.
                            if (unaryExpression is { Operand: SqlExpression sqlOperand, Method: null }
                                && (unaryExpression.Type == sqlOperand.Type.MakeNullable() || !unaryExpression.Type.IsValueType))
                            {
                                var nullableRead = projectionBindingMap[sqlOperand];
                                return nullableRead.Type == unaryExpression.Type ? nullableRead : unaryExpression.Update(nullableRead);
                            }

                            return unaryExpression.Update(operand);
                        }

                        case StructuralTypeShaperExpression
                        {
                            ValueBufferExpression: StructuralTypeProjectionExpression projection
                        } shaper:
                        {
                            var clientProjectionToAdd = AddStructuralTypeProjection(projection);
                            var existingIndex = clientProjectionList.FindIndex(e
                                => ExpressionEqualityComparer.Instance.Equals(e, clientProjectionToAdd));
                            if (existingIndex == -1)
                            {
                                clientProjectionList.Add(clientProjectionToAdd);
                                existingIndex = clientProjectionList.Count - 1;
                            }

                            return shaper.Update(
                                new ProjectionBindingExpression(selectExpression, existingIndex, typeof(ValueBuffer)));
                        }

                        default:
                            throw new InvalidOperationException(
                                RelationalStrings.InvalidKeySelectorForGroupBy(keySelector, keySelector.GetType()));
                    }
                }

                static (Expression, IReadOnlyList<ValueComparer>) GetIdentifierAccessor(
                    SelectExpression selectExpression,
                    List<Expression> clientProjectionList,
                    Dictionary<SqlExpression, Expression> projectionBindingMap,
                    IEnumerable<(ColumnExpression Column, ValueComparer Comparer)> identifyingProjection)
                {
                    var updatedExpressions = new List<Expression>();
                    var comparers = new List<ValueComparer>();
                    foreach (var (column, comparer) in identifyingProjection)
                    {
                        if (!projectionBindingMap.TryGetValue(column, out var mappedExpression))
                        {
                            var index = selectExpression.AddToProjection(column);
                            var clientProjectionToAdd = Constant(index);
                            var existingIndex = clientProjectionList.FindIndex(e
                                => ExpressionEqualityComparer.Instance.Equals(e, clientProjectionToAdd));
                            if (existingIndex == -1)
                            {
                                clientProjectionList.Add(clientProjectionToAdd);
                                existingIndex = clientProjectionList.Count - 1;
                            }

                            mappedExpression = new ProjectionBindingExpression(selectExpression, existingIndex, column.Type.MakeNullable());
                        }

                        updatedExpressions.Add(
                            mappedExpression.Type.IsValueType
                                ? Convert(mappedExpression, typeof(object))
                                : mappedExpression);
                        comparers.Add(comparer);
                    }

                    return (NewArrayInit(typeof(object), updatedExpressions), comparers);
                }

                remappingRequired = true;
                shaperExpression = new RelationalGroupByResultExpression(
                    keyIdentifier, keyIdentifierValueComparers, keySelector, groupByShaper.ElementSelector,
                    groupByShaper.ResultSelector);
            }

            SelectExpression? baseSelectExpression = null;
            if (querySplittingBehavior == QuerySplittingBehavior.SplitQuery && containsCollection)
            {
                // Needs to happen after converting final GroupBy so we clone correct form.
                baseSelectExpression = (SelectExpression)cloningExpressionVisitor!.Visit(this);
                // We mark this as mutable because the split query will combine into this and take it over.
                baseSelectExpression.IsMutable = true;
                if (resultCardinality is ResultCardinality.Single or ResultCardinality.SingleOrDefault)
                {
                    // Update limit since split queries don't need limit 2
                    if (pushdownOccurred)
                    {
                        UpdateLimit((SelectExpression)baseSelectExpression.Tables[0]);
                    }
                    else
                    {
                        UpdateLimit(baseSelectExpression);
                    }

                    static void UpdateLimit(SelectExpression selectExpression)
                    {
                        if (selectExpression.Limit is SqlConstantExpression { Value: 2 } limitConstantExpression)
                        {
                            selectExpression.Limit = new SqlConstantExpression(1, limitConstantExpression.TypeMapping);
                        }
                    }
                }
            }

            for (var i = 0; i < _clientProjections.Count; i++)
            {
                if (i == earlierClientProjectionCount)
                {
                    // Since we lift nested client projections for single results up, we may need to re-clone the baseSelectExpression
                    // again so it does contain the single result subquery too. We erase projections for it since it would be non-empty.
                    earlierClientProjectionCount = _clientProjections.Count;
                    if (cloningExpressionVisitor != null)
                    {
                        baseSelectExpression = (SelectExpression)cloningExpressionVisitor.Visit(this);
                        baseSelectExpression.IsMutable = true;
                        baseSelectExpression._projection.Clear();
                    }
                }

                var value = _clientProjections[i];
                switch (value)
                {
                    case StructuralTypeProjectionExpression projection:
                    {
                        var result = AddStructuralTypeProjection(projection);
                        newClientProjections.Add(result);
                        clientProjectionIndexMap.Add(newClientProjections.Count - 1);

                        break;
                    }

                    case JsonQueryExpression jsonQueryExpression:
                    {
                        var jsonProjectionResult = AddJsonProjection(jsonQueryExpression);
                        newClientProjections.Add(jsonProjectionResult);
                        clientProjectionIndexMap.Add(newClientProjections.Count - 1);

                        break;
                    }

                    case SqlExpression sqlExpression:
                    {
                        var result = Constant(AddToProjection(sqlExpression, _aliasForClientProjections[i]));
                        newClientProjections.Add(result);
                        clientProjectionIndexMap.Add(newClientProjections.Count - 1);

                        break;
                    }

                    case ShapedQueryExpression
                    {
                        ResultCardinality: ResultCardinality.Single or ResultCardinality.SingleOrDefault
                    } shapedQueryExpression:
                    {
                        var innerShaperExpression = LowerSingleResultSubqueryCore(
                            shapedQueryExpression,
                            (projection, alias) =>
                            {
                                _clientProjections.Add(projection);
                                _aliasForClientProjections.Add(alias);
                                return _clientProjections.Count - 1;
                            },
                            entityShaperNullableMarkingExpressionVisitor!);
                        clientProjectionIndexMap.Add(innerShaperExpression);
                        remappingRequired = true;
                        break;
                    }

                    case ShapedQueryExpression { ResultCardinality: ResultCardinality.Enumerable } shapedQueryExpression:
                    {
                        var innerSelectExpression = (SelectExpression)shapedQueryExpression.QueryExpression;
                        if (_identifier.Count == 0
                            || innerSelectExpression._identifier.Count == 0)
                        {
                            throw new InvalidOperationException(
                                RelationalStrings.InsufficientInformationToIdentifyElementOfCollectionJoin);
                        }

                        var innerShaperExpression = shapedQueryExpression.ShaperExpression;
                        if (innerSelectExpression._clientProjections.Count == 0)
                        {
                            var mapping = innerSelectExpression.ConvertProjectionMappingToClientProjections(
                                innerSelectExpression._projectionMapping);
                            innerShaperExpression =
                                new ProjectionMemberToIndexConvertingExpressionVisitor(innerSelectExpression, mapping)
                                    .Visit(innerShaperExpression);
                        }

                        if (querySplittingBehavior == QuerySplittingBehavior.SplitQuery)
                        {
                            var outerSelectExpression = (SelectExpression)cloningExpressionVisitor!.Visit(baseSelectExpression!);

                            // Inject deterministic orderings (the identifier columns) to both the main query and the split query.
                            // Note that just below we pushdown the split query if it has limit/offset/distinct/groupby; this ensures
                            // that the orderings are also propagated to that split subquery if it has limit/offset, which ensures that
                            // that subquery returns the same rows as the main query (#26808)
                            var actualParentIdentifier = _identifier.Take(outerSelectExpression._identifier.Count).ToList();
                            for (var j = 0; j < actualParentIdentifier.Count; j++)
                            {
                                AppendOrderingInternal(new OrderingExpression(actualParentIdentifier[j].Column, ascending: true));
                                outerSelectExpression.AppendOrderingInternal(
                                    new OrderingExpression(outerSelectExpression._identifier[j].Column, ascending: true));
                            }

                            if (outerSelectExpression.Limit != null
                                || outerSelectExpression.Offset != null
                                || outerSelectExpression.IsDistinct
                                || outerSelectExpression._groupBy.Count > 0)
                            {
                                // We do pushdown after making sure that inner contains references to outer only
                                // so that when we do pushdown, we can update inner and maintain graph
                                var sqlRemappingVisitor = outerSelectExpression.PushdownIntoSubqueryInternal();
                                innerSelectExpression = sqlRemappingVisitor.Remap(innerSelectExpression);
                            }

                            var containsOrdering = innerSelectExpression.Orderings.Count > 0;
                            List<OrderingExpression>? orderingsToBeErased = null;
                            if (containsOrdering
                                && innerSelectExpression.Limit == null
                                && innerSelectExpression.Offset == null)
                            {
                                orderingsToBeErased = innerSelectExpression.Orderings.ToList();
                            }

                            var parentIdentifier = GetIdentifierAccessor(this, newClientProjections, actualParentIdentifier).Item1;

                            outerSelectExpression.AddJoin(
                                JoinType.CrossApply, ref innerSelectExpression, out var pushdownOccurredWhenJoining);
                            outerSelectExpression._clientProjections.AddRange(innerSelectExpression._clientProjections);
                            outerSelectExpression._aliasForClientProjections.AddRange(innerSelectExpression._aliasForClientProjections);
                            innerSelectExpression = outerSelectExpression;

                            // Copy over any nested ordering if there were any
                            if (containsOrdering)
                            {
                                var collectionJoinedInnerTable = ((JoinExpressionBase)innerSelectExpression._tables[^1]).Table;
                                var innerOrderingExpressions = new List<OrderingExpression>();
                                if (orderingsToBeErased != null)
                                {
                                    // Ordering was present but erased so we add again
                                    if (pushdownOccurredWhenJoining)
                                    {
                                        // We lift from inner subquery if pushdown occurred with ordering erased
                                        var subquery = (SelectExpression)collectionJoinedInnerTable;
                                        foreach (var ordering in orderingsToBeErased)
                                        {
                                            innerOrderingExpressions.Add(
                                                new OrderingExpression(
                                                    subquery.GenerateOuterColumn(
                                                        collectionJoinedInnerTable.GetRequiredAlias(), ordering.Expression),
                                                    ordering.IsAscending));
                                        }
                                    }
                                    else
                                    {
                                        // We copy from inner if pushdown did not happen but ordering was left behind when
                                        // generating join
                                        innerOrderingExpressions.AddRange(orderingsToBeErased);
                                    }
                                }
                                else
                                {
                                    // If orderings were not erased then they must be present in inner
                                    GetOrderingsFromInnerTable(collectionJoinedInnerTable, innerOrderingExpressions);
                                }

                                foreach (var ordering in innerOrderingExpressions)
                                {
                                    innerSelectExpression.AppendOrdering(ordering);
                                }
                            }

                            innerShaperExpression = innerSelectExpression.ApplyProjection(
                                innerShaperExpression, shapedQueryExpression.ResultCardinality, querySplittingBehavior);

                            var (childIdentifier, childIdentifierValueComparers) = GetIdentifierAccessor(
                                innerSelectExpression,
                                innerSelectExpression._clientProjections,
                                innerSelectExpression._identifier.Take(_identifier.Count));

                            var result = new SplitCollectionInfo(
                                parentIdentifier, childIdentifier, childIdentifierValueComparers,
                                innerSelectExpression, innerShaperExpression);
                            clientProjectionIndexMap.Add(result);
                        }
                        else
                        {
                            var parentIdentifierList = _identifier.Except(_childIdentifiers, IdentifierComparerInstance).ToList();
                            var (parentIdentifier, parentIdentifierValueComparers) = GetIdentifierAccessor(
                                this, newClientProjections, parentIdentifierList);
                            var (outerIdentifier, outerIdentifierValueComparers) = GetIdentifierAccessor(
                                this, newClientProjections, _identifier);

                            foreach (var identifier in _identifier)
                            {
                                AppendOrdering(new OrderingExpression(identifier.Column, ascending: true));
                            }

                            innerShaperExpression = innerSelectExpression.ApplyProjection(
                                innerShaperExpression, shapedQueryExpression.ResultCardinality, querySplittingBehavior);

                            var containsOrdering = innerSelectExpression.Orderings.Count > 0;
                            List<OrderingExpression>? orderingsToBeErased = null;
                            if (containsOrdering
                                && innerSelectExpression.Limit == null
                                && innerSelectExpression.Offset == null)
                            {
                                orderingsToBeErased = innerSelectExpression.Orderings.ToList();
                            }

                            AddJoin(JoinType.OuterApply, ref innerSelectExpression, out var pushdownOccurredWhenJoining);

                            // Copy over any nested ordering if there were any
                            if (containsOrdering)
                            {
                                var collectionJoinedInnerTable = innerSelectExpression._tables[0];
                                var innerOrderingExpressions = new List<OrderingExpression>();
                                if (orderingsToBeErased != null)
                                {
                                    // Ordering was present but erased so we add again
                                    if (pushdownOccurredWhenJoining)
                                    {
                                        // We lift from inner subquery if pushdown occurred with ordering erased
                                        var subquery = (SelectExpression)collectionJoinedInnerTable;
                                        foreach (var ordering in orderingsToBeErased)
                                        {
                                            innerOrderingExpressions.Add(
                                                new OrderingExpression(
                                                    subquery.GenerateOuterColumn(
                                                        collectionJoinedInnerTable.GetRequiredAlias(), ordering.Expression),
                                                    ordering.IsAscending));
                                        }
                                    }
                                    else
                                    {
                                        // We copy from inner if pushdown did not happen but ordering was left behind when
                                        // generating join
                                        innerOrderingExpressions.AddRange(orderingsToBeErased);
                                    }
                                }
                                else
                                {
                                    // If orderings were not erased then they must be present in inner
                                    GetOrderingsFromInnerTable(collectionJoinedInnerTable, innerOrderingExpressions);
                                }

                                foreach (var ordering in innerOrderingExpressions)
                                {
                                    AppendOrdering(ordering.Update(MakeNullable(ordering.Expression, nullable: true)));
                                }
                            }

                            innerShaperExpression = CopyProjectionToOuter(innerSelectExpression, innerShaperExpression);
                            var (selfIdentifier, selfIdentifierValueComparers) = GetIdentifierAccessor(
                                this,
                                newClientProjections,
                                innerSelectExpression._identifier
                                    .Except(innerSelectExpression._childIdentifiers, IdentifierComparerInstance)
                                    .Select(e => (e.Column.MakeNullable(), e.Comparer)));

                            var collectionJoinPredicate = (_tables[^1] as PredicateJoinExpressionBase)?.JoinPredicate;
                            var hasOrderingForJoinKey = false;
                            var hasOrderingForNonJoinKey = false;
                            OrderingExpression? pendingOrdering = null;
                            foreach (var (identifierColumn, identifierComparer) in innerSelectExpression._identifier)
                            {
                                var updatedColumn = identifierColumn.MakeNullable();
                                _childIdentifiers.Add((updatedColumn, identifierComparer));

                                // We omit the last ordering as an optimization
                                var orderingExpression = new OrderingExpression(updatedColumn, ascending: true);

                                if (!_orderings.Any(o => o.Expression.Equals(updatedColumn)))
                                {
                                    if (pendingOrdering is not null)
                                    {
                                        if (orderingExpression.Equals(pendingOrdering))
                                        {
                                            continue;
                                        }

                                        AppendOrderingInternal(pendingOrdering);
                                        TrackOrdering(pendingOrdering.Expression);
                                    }

                                    pendingOrdering = orderingExpression;
                                }
                                else
                                {
                                    TrackOrdering(updatedColumn);
                                }
                            }

                            if (pendingOrdering is not null
                                && hasOrderingForJoinKey
                                && !hasOrderingForNonJoinKey)
                            {
                                // The pending identifier is the only ordering that discriminates elements within the collection.
                                AppendOrderingInternal(pendingOrdering);
                            }

                            void TrackOrdering(SqlExpression ordering)
                            {
                                if (collectionJoinPredicate is not null
                                    && IsJoinKeyColumn(collectionJoinPredicate, ordering))
                                {
                                    hasOrderingForJoinKey = true;
                                }
                                else
                                {
                                    hasOrderingForNonJoinKey = true;
                                }
                            }

                            static bool IsJoinKeyColumn(SqlExpression joinPredicate, SqlExpression column)
                                => joinPredicate switch
                                {
                                    SqlBinaryExpression { OperatorType: ExpressionType.Equal } binary
                                        => IsSameColumn(binary.Left, column) || IsSameColumn(binary.Right, column),
                                    SqlBinaryExpression { OperatorType: ExpressionType.AndAlso } binary
                                        => IsJoinKeyColumn(binary.Left, column) || IsJoinKeyColumn(binary.Right, column),
                                    _ => false
                                };

                            static bool IsSameColumn(SqlExpression left, SqlExpression right)
                                => left is ColumnExpression leftColumn
                                    && right is ColumnExpression rightColumn
                                    && leftColumn.TableAlias == rightColumn.TableAlias
                                    && leftColumn.Name == rightColumn.Name;

                            var result = new SingleCollectionInfo(
                                parentIdentifier, outerIdentifier, selfIdentifier,
                                parentIdentifierValueComparers, outerIdentifierValueComparers, selfIdentifierValueComparers,
                                innerShaperExpression);
                            clientProjectionIndexMap.Add(result);
                        }

                        remappingRequired = true;

                        static (Expression, IReadOnlyList<ValueComparer>) GetIdentifierAccessor(
                            SelectExpression selectExpression,
                            List<Expression> clientProjectionList,
                            IEnumerable<(ColumnExpression Column, ValueComparer Comparer)> identifyingProjection)
                        {
                            var updatedExpressions = new List<Expression>();
                            var comparers = new List<ValueComparer>();
                            foreach (var (column, comparer) in identifyingProjection)
                            {
                                var index = selectExpression.AddToProjection(column, null);
                                var clientProjectionToAdd = Constant(index);
                                var existingIndex = clientProjectionList.FindIndex(e
                                    => ExpressionEqualityComparer.Instance.Equals(e, clientProjectionToAdd));
                                if (existingIndex == -1)
                                {
                                    clientProjectionList.Add(Constant(index));
                                    existingIndex = clientProjectionList.Count - 1;
                                }

                                var projectionBindingExpression = new ProjectionBindingExpression(
                                    selectExpression, existingIndex, column.Type.MakeNullable());

                                updatedExpressions.Add(
                                    projectionBindingExpression.Type.IsValueType
                                        ? Convert(projectionBindingExpression, typeof(object))
                                        : projectionBindingExpression);
                                comparers.Add(comparer);
                            }

                            return (NewArrayInit(typeof(object), updatedExpressions), comparers);
                        }

                        break;
                    }

                    default:
                        throw new InvalidOperationException(value.GetType().ToString());
                }
            }

            if (remappingRequired)
            {
                shaperExpression = new ClientProjectionRemappingExpressionVisitor(clientProjectionIndexMap).Visit(shaperExpression);
            }

            _clientProjections = newClientProjections;
            _aliasForClientProjections.Clear();

            return shaperExpression;

            void GetOrderingsFromInnerTable(TableExpressionBase tableExpressionBase, List<OrderingExpression> orderings)
            {
                var tableAlias = tableExpressionBase.GetRequiredAlias();

                // If operation was converted to predicate join (inner/left join), then ordering will be in a RowNumberExpression
                if (tableExpressionBase is SelectExpression
                    {
                        Tables: [SelectExpression rowNumberSubquery],
                        Predicate: not null
                    } joinedSubquery
                    && rowNumberSubquery.Projection.Select(pe => pe.Expression)
                        .OfType<RowNumberExpression>().SingleOrDefault() is { } rowNumberExpression)
                {
                    var rowNumberSubqueryTableAlias = joinedSubquery.Tables.Single().GetRequiredAlias();
                    foreach (var partition in rowNumberExpression.Partitions)
                    {
                        orderings.Add(
                            new OrderingExpression(
                                joinedSubquery.GenerateOuterColumn(
                                    tableAlias,
                                    rowNumberSubquery.GenerateOuterColumn(rowNumberSubqueryTableAlias, partition)),
                                ascending: true));
                    }

                    foreach (var ordering in rowNumberExpression.Orderings)
                    {
                        orderings.Add(
                            new OrderingExpression(
                                joinedSubquery.GenerateOuterColumn(
                                    tableAlias,
                                    rowNumberSubquery.GenerateOuterColumn(rowNumberSubqueryTableAlias, ordering.Expression)),
                                ordering.IsAscending));
                    }
                }
                // If operation remained apply then ordering will be in the subquery
                else if (tableExpressionBase is SelectExpression { Orderings.Count: > 0 } collectionSelectExpression)
                {
                    foreach (var ordering in collectionSelectExpression.Orderings)
                    {
                        orderings.Add(
                            new OrderingExpression(
                                collectionSelectExpression.GenerateOuterColumn(tableAlias, ordering.Expression),
                                ordering.IsAscending));
                    }
                }
            }

            Expression CopyProjectionToOuter(SelectExpression innerSelectExpression, Expression innerShaperExpression)
            {
                var projectionIndexMap = new int[innerSelectExpression._projection.Count];
                for (var j = 0; j < projectionIndexMap.Length; j++)
                {
                    var projection = MakeNullable(innerSelectExpression._projection[j].Expression, nullable: true);
                    var index = AddToProjection(projection);
                    projectionIndexMap[j] = index;
                }

                var indexMap = new int[innerSelectExpression._clientProjections.Count];
                for (var j = 0; j < indexMap.Length; j++)
                {
                    var constantValue = ((ConstantExpression)innerSelectExpression._clientProjections[j]).Value!;
                    ConstantExpression remappedConstant;
                    switch (((ConstantExpression)innerSelectExpression._clientProjections[j]).Value!)
                    {
                        case Dictionary<IPropertyBase, int> entityDictionary:
                        {
                            var newDictionary = new Dictionary<IPropertyBase, int>(entityDictionary.Count);
                            foreach (var (property, value) in entityDictionary)
                            {
                                newDictionary[property] = projectionIndexMap[value];
                            }

                            remappedConstant = Constant(newDictionary);
                            break;
                        }

                        case JsonProjectionInfo jsonProjectionInfo:
                        {
                            var newKeyAccessInfo = new List<(IProperty?, int?, int?)>();
                            foreach (var (keyProperty, constantKeyValue, keyProjectionIndex) in jsonProjectionInfo.KeyAccessInfo)
                            {
                                newKeyAccessInfo.Add(
                                    (keyProperty, constantKeyValue,
                                        keyProjectionIndex != null ? projectionIndexMap[keyProjectionIndex.Value] : null));
                            }

                            // The outer projection still references the same underlying JSON column; only the
                            // index into the outer projection changes, so preserve JsonColumn for the shaper.
                            remappedConstant = Constant(
                                new JsonProjectionInfo(
                                    projectionIndexMap[jsonProjectionInfo.JsonColumnIndex],
                                    newKeyAccessInfo,
                                    jsonProjectionInfo.JsonColumn));
                            break;
                        }

                        case QueryableJsonProjectionInfo queryableJsonProjectionInfo:
                        {
                            var newPropertyIndexMap =
                                new Dictionary<IPropertyBase, int>(queryableJsonProjectionInfo.PropertyIndexMap.Count);
                            foreach (var (property, value) in queryableJsonProjectionInfo.PropertyIndexMap)
                            {
                                newPropertyIndexMap[property] = projectionIndexMap[value];
                            }

                            var newChildrenProjectionInfo = new List<(JsonProjectionInfo, INavigation)>();
                            foreach (var childProjectionInfo in queryableJsonProjectionInfo.ChildrenProjectionInfo)
                            {
                                var newKeyAccessInfo = new List<(IProperty?, int?, int?)>();
                                foreach (var (keyProperty, constantKeyValue, keyProjectionIndex) in childProjectionInfo.JsonProjectionInfo
                                             .KeyAccessInfo)
                                {
                                    newKeyAccessInfo.Add(
                                        (keyProperty, constantKeyValue,
                                            keyProjectionIndex != null ? projectionIndexMap[keyProjectionIndex.Value] : null));
                                }

                                newChildrenProjectionInfo.Add(
                                    (new JsonProjectionInfo(
                                            projectionIndexMap[childProjectionInfo.JsonProjectionInfo.JsonColumnIndex],
                                            newKeyAccessInfo,
                                            childProjectionInfo.JsonProjectionInfo.JsonColumn),
                                        childProjectionInfo.Navigation));
                            }

                            remappedConstant = Constant(
                                new QueryableJsonProjectionInfo(newPropertyIndexMap, newChildrenProjectionInfo));

                            break;
                        }

                        default:
                            remappedConstant = Constant(projectionIndexMap[(int)constantValue]);
                            break;
                    }

                    newClientProjections.Add(remappedConstant);
                    indexMap[j] = newClientProjections.Count - 1;
                }

                innerSelectExpression._clientProjections.Clear();
                innerSelectExpression._aliasForClientProjections.Clear();
                innerShaperExpression =
                    new ProjectionIndexRemappingExpressionVisitor(innerSelectExpression, this, indexMap).Visit(innerShaperExpression);
                innerShaperExpression = entityShaperNullableMarkingExpressionVisitor!.Visit(innerShaperExpression);

                return innerShaperExpression;
            }
        }

        {
            var result = new Dictionary<ProjectionMember, Expression>(_projectionMapping.Count);

            foreach (var (projectionMember, expression) in _projectionMapping)
            {
                result[projectionMember] = expression switch
                {
                    StructuralTypeProjectionExpression p => AddStructuralTypeProjection(p),
                    JsonQueryExpression p => AddJsonProjection(p),
                    SqlExpression p => Constant(AddToProjection(p, GetProjectionAlias(projectionMember))),
                    _ => throw new UnreachableException("Unexpected expression type in projection mapping.")
                };
            }

            _projectionMapping.Clear();
            _projectionMapping = result;

            return shaperExpression;
        }

        ConstantExpression AddStructuralTypeProjection(StructuralTypeProjectionExpression projection)
        {
            // JSON entity that had some query operations applied on it - it has been converted to a query root via OPENJSON/json_each
            // so it requires different materialization path than regular entity
            // e.g. we need to also add all the child navigations, JSON entity builds all the includes as part of it's own materializer
            // rather than relying on IncludeExpressions in the shaper query
            // also, we don't want to add projection map for synthesized keys, whereas regular entity needs to project every single property it has
            if (projection is { StructuralType: IEntityType entityType }
                && entityType.IsMappedToJson())
            {
                var propertyIndexMap = new Dictionary<IPropertyBase, int>();
                var ownerEntity = entityType;

                do
                {
                    var ownership = ownerEntity.FindOwnership();
                    if (ownership != null)
                    {
                        ownerEntity = ownership.PrincipalEntityType;
                    }
                }
                while (ownerEntity.IsMappedToJson());

                var keyPropertyCount = ownerEntity.FindPrimaryKey()!.Properties.Count;
                foreach (var property in entityType.FindPrimaryKey()!.Properties.Take(keyPropertyCount)
                             .Concat(entityType.GetDeclaredProperties().Where(p => p.GetJsonPropertyName() is not null)))
                {
                    propertyIndexMap[property] = AddToProjection(projection.BindProperty(property), null);
                }

                var childrenProjectionInfo = new List<(JsonProjectionInfo, INavigation)>();
                foreach (var ownedNavigation in entityType.GetNavigations().Where(n => n.TargetEntityType.IsMappedToJson()
                             && n.ForeignKey.IsOwnership
                             && n == n.ForeignKey.PrincipalToDependent))
                {
                    var jsonQueryExpression = (JsonQueryExpression)projection.BindNavigation(ownedNavigation)!.ValueBufferExpression;
                    var jsonProjectionInfo = (JsonProjectionInfo)AddJsonProjection(jsonQueryExpression).Value!;
                    childrenProjectionInfo.Add((jsonProjectionInfo, ownedNavigation));
                }

                return Constant(new QueryableJsonProjectionInfo(propertyIndexMap, childrenProjectionInfo));
            }

            var projections = new Dictionary<IPropertyBase, int>();

            ProcessType(projection);

            void ProcessType(StructuralTypeProjectionExpression typeProjection)
            {
                foreach (var property in typeProjection.StructuralType.GetPropertiesInHierarchy())
                {
                    if (typeProjection is { StructuralType: IEntityType entityType }
                        && entityType.IsMappedToJson()
                        && property.IsOrdinalKeyProperty())
                    {
                        continue;
                    }

                    if (!property.IsAutoLoaded)
                    {
                        continue;
                    }

                    projections[property] = AddToProjection(typeProjection.BindProperty(property), alias: null);
                }

                foreach (var complexProperty in GetAllComplexPropertiesInHierarchy(typeProjection.StructuralType))
                {
                    switch (typeProjection.BindComplexProperty(complexProperty))
                    {
                        case StructuralTypeShaperExpression { ValueBufferExpression: StructuralTypeProjectionExpression nestedProjection }:
                            ProcessType(nestedProjection);
                            break;

                        // Complex (not owned) JSON, single (non-collection)
                        case StructuralTypeShaperExpression { ValueBufferExpression: JsonQueryExpression jsonQuery }:
                            projections[complexProperty] = ((JsonProjectionInfo)AddJsonProjection(jsonQuery).Value!).JsonColumnIndex;
                            break;

                        // Complex (not owned) JSON, collection
                        case CollectionResultExpression { QueryExpression: JsonQueryExpression jsonQuery }:
                            projections[complexProperty] = ((JsonProjectionInfo)AddJsonProjection(jsonQuery).Value!).JsonColumnIndex;
                            break;

                        default:
                            throw new UnreachableException(
                                "Unexpected complex property binding when building structural type projection.");
                    }
                }
            }

            if (projection.DiscriminatorExpression is not null)
            {
                AddToProjection(projection.DiscriminatorExpression, DiscriminatorColumnAlias);
            }

            return Constant(projections);
        }

        ConstantExpression AddJsonProjection(JsonQueryExpression jsonQueryExpression)
        {
            var jsonScalarExpression = new JsonScalarExpression(
                jsonQueryExpression.JsonColumn,
                jsonQueryExpression.Path,
                jsonQueryExpression.JsonColumn.Type,
                jsonQueryExpression.JsonColumn.TypeMapping!,
                jsonQueryExpression.IsNullable);

            _projection.Add(new ProjectionExpression(jsonScalarExpression, ""));
            var jsonColumnIndex = _projection.Count - 1;
            var keyAccessInfo = new List<(IProperty?, int?, int?)>();

            switch (jsonQueryExpression.StructuralType)
            {
                case IEntityType entityType:
                    var keyProperties = GetMappedKeyProperties(entityType.FindPrimaryKey()!);
                    foreach (var keyProperty in keyProperties)
                    {
                        var keyColumn = jsonQueryExpression.BindProperty(keyProperty);
                        keyAccessInfo.Add((keyProperty, null, AddToProjection(keyColumn)));
                    }

                    foreach (var elementAccessSegment in jsonScalarExpression.Path.Where(x => x.ArrayIndex != null))
                    {
                        if (elementAccessSegment.ArrayIndex is SqlConstantExpression { Value: int intValue })
                        {
                            keyAccessInfo.Add((null, intValue, null));
                        }
                        else
                        {
                            keyAccessInfo.Add((null, null, AddToProjection(elementAccessSegment.ArrayIndex!)));
                        }
                    }

                    break;

                case IComplexType complexType:
                    break;

                default:
                    throw new UnreachableException("Unexpected structural type when building JSON projection.");
            }

            return Constant(new JsonProjectionInfo(jsonColumnIndex, keyAccessInfo, jsonQueryExpression.JsonColumn.Column));
        }

        static IReadOnlyList<IProperty> GetMappedKeyProperties(IKey key)
        {
            if (!key.DeclaringEntityType.IsMappedToJson())
            {
                return key.Properties;
            }

            // TODO: fix this once we enable json entity being owned by another owned non-json entity (issue #28441)

            // for json collections we need to filter out the ordinal key as it's not mapped to any column
            // there could be multiple of these in deeply nested structures,
            // so we traverse to the outermost owner to see how many mapped keys there are
            var currentEntity = key.DeclaringEntityType;
            while (currentEntity.IsMappedToJson())
            {
                currentEntity = currentEntity.FindOwnership()!.PrincipalEntityType;
            }

            var count = currentEntity.FindPrimaryKey()!.Properties.Count;

            return key.Properties.Take(count).ToList();
        }
    }
```


---

### 🔹 Commit #18: `de2caec1`
- **完整 Hash**: `de2caec1e593735e11e33c807e5f4ac89132dcbb`
- **說明 (Ground Truth)**: Sanitize expression variable names when generating precompiled query code (#39062)
- **變更檔案數**: 3

#### 📄 檔案: `src/EFCore.Design/Query/Internal/LinqToCSharpSyntaxTranslator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:420, E:637, A:0) ➔ After(N:463, E:707, A:0)
- **差分統計**: +Nodes: 51, -Nodes: 8, +Edges: 73, -Edges: 3, ΔFuncs: 12, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `ConstantReplacementsContain(name) || _declaredNames?.Contains (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `SyntaxFacts.GetKeywordKind (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `name.Any (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_stack.Clear (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_3118` (MODULE_STATE)
  • + [新增節點] `@namespace.Split (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_3172` (MODULE_STATE)
  • + [新增節點] `_declared` (MODULE_STATE)
  • + [新增節點] `state_3140` (MODULE_STATE)
  • + [新增節點] `_declared.ContainsKey (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `name.Where (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `LinqToCSharpSyntaxTranslator.IsNameInScope` (FUNCTION_DEF)
  • + [新增節點] `FreeVariableNameCollector.VisitBlock` (FUNCTION_DEF)
  • + [新增節點] `_declared.TryGetValue (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `bidirectionalDictionary.ContainsValue (External/BCL)` (FUNCTION_DEF)
  • _... 以及其餘 120 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `LinqToCSharpSyntaxTranslator.VisitLambda()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.VisitLambda(Expression<T> lambda)` (L1522~L1590)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.VisitLambda(Expression<T> lambda)` (L1591~L1673)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override Expression VisitLambda<T>(Expression<T> lambda)
    {
        using var _ = ChangeContext(
            lambda.ReturnType == typeof(void) ? ExpressionContext.Statement : ExpressionContext.ExpressionLambda);
        var parentOnLastLambdaLine = _onLastLambdaLine;
        _onLastLambdaLine = true;

        var stackFrame = PushNewStackFrame();

        var localUnnamedParameterCounter = 0;
        foreach (var parameter in lambda.Parameters)
        {
            var name = parameter.Name ?? ("unnamed" + (++localUnnamedParameterCounter));

            if (_constantReplacements?.Values.Contains(name) == true)
            {
                name = UniquifyVariableName(name);
            }

            stackFrame.Variables[parameter] = name;
            stackFrame.VariableNames.Add(name);
        }

        var body = Translate(lambda.Body);
        var expressionBody = body as ExpressionSyntax;
        var blockBody = body as BlockSyntax;

        if (_liftedState.Statements.Count > 0)
        {
            Check.DebugAssert(lambda.ReturnType != typeof(void));

            if (expressionBody != null)
            {
                // If the lambda body was an expression that had lifted statements (e.g. some block in expression context), we need to create
                // a block to contain these statements
                blockBody = Block(_liftedState.Statements.Append(ReturnStatement(expressionBody)));
                expressionBody = null;
            }
            else
            {
                // If the lambda body was already a block, we just prepend lifted statements to the ones already existing in the block
                Check.DebugAssert(blockBody != null, "expressionBody != null || blockBody != null");
                blockBody = Block(_liftedState.Statements.Concat(blockBody.Statements));
            }

            _liftedState.Statements.Clear();
        }

        // Note that we always explicitly include the parameters' types.
        // This is because in some cases, the parameter isn't actually used in the lambda body, and the compiler can't infer its type.
        // However, we can't do that when the type is anonymous.
        Result = ParenthesizedLambdaExpression(
            attributeLists: List<AttributeListSyntax>(),
            modifiers: TokenList(),
            returnType: lambda.ReturnType == typeof(void) || !TryGenerate(lambda.ReturnType, out var returnSyntax) ? null : returnSyntax,
            ParameterList(
                SeparatedList(
                    lambda.Parameters.Select(p => Parameter(Identifier(LookupVariableName(p)))
                        .WithType(p.Type.IsAnonymousType() ? null : Generate(p.Type))))),
            blockBody,
            expressionBody);

        var popped = _stack.Pop();
        Check.DebugAssert(popped.Equals(stackFrame));

        _onLastLambdaLine = parentOnLastLambdaLine;

        return lambda;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override Expression VisitLambda<T>(Expression<T> lambda)
    {
        using var _ = ChangeContext(
            lambda.ReturnType == typeof(void) ? ExpressionContext.Statement : ExpressionContext.ExpressionLambda);
        var parentOnLastLambdaLine = _onLastLambdaLine;
        _onLastLambdaLine = true;

        var stackFrame = PushNewStackFrame();

        var localUnnamedParameterCounter = 0;
        var lambdaParameterNames = new HashSet<string>();
        foreach (var parameter in lambda.Parameters)
        {
            var name = parameter.Name is null
                ? "unnamed" + (++localUnnamedParameterCounter)
                : SanitizeIdentifierName(parameter.Name);

            // A parameter that already had the same name as a variable in scope keeps shadowing it, as before
            // (Variable_with_same_name_in_lambda_does_not_get_renamed). What must not happen is a collision that sanitization
            // itself creates, or one with a lifted variable, whose declaration is emitted inside the lambda body: either would
            // rebind references to that variable. The same goes for the caller's own declarations and for captured variables,
            // which the lambda body refers to by name.
            if (IsCallerDeclaredName(name)
                || !lambdaParameterNames.Add(name)
                || _liftedState.VariableNames.Contains(name)
                || _capturedVariableNames.Contains(name)
                || (stackFrame.VariableNames.Contains(name)
                    && !stackFrame.Variables.Any(v => v.Value == name && v.Key.Name == parameter.Name)))
            {
                name = UniquifyVariableName(name);
                lambdaParameterNames.Add(name);
            }

            stackFrame.Variables[parameter] = name;
            stackFrame.VariableNames.Add(name);
        }

        var body = Translate(lambda.Body);
        var expressionBody = body as ExpressionSyntax;
        var blockBody = body as BlockSyntax;

        if (_liftedState.Statements.Count > 0)
        {
            Check.DebugAssert(lambda.ReturnType != typeof(void));

            if (expressionBody != null)
            {
                // If the lambda body was an expression that had lifted statements (e.g. some block in expression context), we need to create
                // a block to contain these statements
                blockBody = Block(_liftedState.Statements.Append(ReturnStatement(expressionBody)));
                expressionBody = null;
            }
            else
            {
                // If the lambda body was already a block, we just prepend lifted statements to the ones already existing in the block
                Check.DebugAssert(blockBody != null, "expressionBody != null || blockBody != null");
                blockBody = Block(_liftedState.Statements.Concat(blockBody.Statements));
            }

            _liftedState.Statements.Clear();
        }

        // Note that we always explicitly include the parameters' types.
        // This is because in some cases, the parameter isn't actually used in the lambda body, and the compiler can't infer its type.
        // However, we can't do that when the type is anonymous.
        Result = ParenthesizedLambdaExpression(
            attributeLists: List<AttributeListSyntax>(),
            modifiers: TokenList(),
            returnType: lambda.ReturnType == typeof(void) || !TryGenerate(lambda.ReturnType, out var returnSyntax) ? null : returnSyntax,
            ParameterList(
                SeparatedList(
                    lambda.Parameters.Select(p => Parameter(Identifier(LookupVariableName(p)))
                        .WithType(p.Type.IsAnonymousType() ? null : Generate(p.Type))))),
            blockBody,
            expressionBody);

        var popped = _stack.Pop();
        Check.DebugAssert(popped.Equals(stackFrame));

        _onLastLambdaLine = parentOnLastLambdaLine;

        return lambda;
    }
```

### 🔹 函式: `LinqToCSharpSyntaxTranslator.VisitBlock()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.VisitBlock(BlockExpression block)` (L499~L780)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.VisitBlock(BlockExpression block)` (L540~L821)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override Expression VisitBlock(BlockExpression block)
    {
        var blockContext = _context;

        var parentOnLastLambdaLine = _onLastLambdaLine;
        var parentLiftedState = _liftedState;

        // Expression blocks have no stack of their own, since they're lifted directly to their parent non-expression block.
        StackFrame? ownStackFrame = null;
        if (blockContext != ExpressionContext.Expression)
        {
            ownStackFrame = PushNewStackFrame();
            _liftedState = parentLiftedState.CreateChild();
        }

        var stackFrame = _stack.Peek();

        // Do a 1st pass to identify and register any labels, since goto can appear before its label.
        PreprocessLabels();

        // Go over the block's variables, assign names to any unnamed ones and uniquify. Then add them to our stack frame, unless
        // this is an expression block that will get lifted.
        foreach (var parameter in block.Variables)
        {
            var (variables, variableNames) = (stackFrame.Variables, stackFrame.VariableNames);

            var uniquifiedName = UniquifyVariableName(parameter.Name ?? "unnamed");

            if (blockContext == ExpressionContext.Expression)
            {
                if (!_liftedState.Variables.TryAdd(parameter, uniquifiedName))
                {
                    throw new NotSupportedException("Parameter clash during expression lifting for: " + parameter.Name);
                }

                _liftedState.VariableNames.Add(uniquifiedName);
            }
            else
            {
                if (!variables.TryAdd(parameter, uniquifiedName))
                {
                    throw new InvalidOperationException(
                        DesignStrings.SameParameterExpressionDeclaredAsVariableInNestedBlocks(parameter.Name ?? "<null>"));
                }

                variableNames.Add(uniquifiedName);
            }
        }

        var unassignedVariables = block.Variables.ToList();

        var statements = new List<StatementSyntax>();
        LabeledStatementSyntax? pendingLabeledStatement = null;

        // Now visit the block's expressions
        for (var i = 0; i < block.Expressions.Count; i++)
        {
            var expression = block.Expressions[i];
            var onLastBlockLine = i == block.Expressions.Count - 1;
            _onLastLambdaLine = parentOnLastLambdaLine && onLastBlockLine;

            // Any lines before the last are evaluated in statement context (they aren't returned); the last line is evaluated in the
            // context of the block as a whole. _context now refers to the statement's context, blockContext to the block's.
            var statementContext = onLastBlockLine ? _context : ExpressionContext.Statement;

            SyntaxNode translated;
            using (ChangeContext(statementContext))
            {
                translated = Translate(expression);
            }

            // If we have a labeled statement, unwrap it and keep the label as pending. VisitLabel returns a dummy statement (since
            // LINQ labels don't have a statement, unlike C#), so we'll skip that statement and add the label to the next real one.
            if (translated is LabeledStatementSyntax labeledStatement)
            {
                if (pendingLabeledStatement is not null)
                {
                    throw new NotImplementedException("Multiple labels on the same statement");
                }

                pendingLabeledStatement = labeledStatement;
                translated = labeledStatement.Statement;
            }

            // Syntax optimization. This is an assignment of a block variable to some value. Render this as:
            // var x = <expression>;
            // ... instead of:
            // int x;
            // x = <expression>;
            // ... except for expression context (i.e. on the last line), where we just return the value if needed.
            if (expression is BinaryExpression { NodeType: ExpressionType.Assign, Left: ParameterExpression lValue }
                && translated is AssignmentExpressionSyntax { Right: var valueSyntax }
                && statementContext == ExpressionContext.Statement
                && unassignedVariables.Remove(lValue))
            {
                var useExplicitVariableType = valueSyntax.Kind() == SyntaxKind.NullLiteralExpression;

                translated = useExplicitVariableType
                    ? _g.LocalDeclarationStatement(Generate(lValue.Type), LookupVariableName(lValue), valueSyntax)
                    : _g.LocalDeclarationStatement(LookupVariableName(lValue), valueSyntax);
            }

            if (statementContext == ExpressionContext.Expression)
            {
                // We're on the last line of a block in expression context - the block is being lifted out.
                // All statements before the last line (this one) have already been added to _liftedStatements, just return the last
                // expression.
                Check.DebugAssert(onLastBlockLine);
                Result = translated;
                break;
            }

            if (blockContext != ExpressionContext.Expression)
            {
                if (_liftedState.Statements.Count > 0)
                {
                    // If any expressions were lifted out of the current expression, flatten them into our own block, just before the
                    // expression from which they were lifted. Note that we don't do this in Expression context, since our own block is
                    // lifted out.
                    statements.AddRange(_liftedState.Statements);
                    _liftedState.Statements.Clear();
                }

                // Same for any variables being lifted out of the block; we add them to our own stack frame so that we can do proper
                // variable name uniquification etc.
                if (_liftedState.Variables.Count > 0)
                {
                    foreach (var (parameter, name) in _liftedState.Variables)
                    {
                        stackFrame.Variables[parameter] = name;
                        stackFrame.VariableNames.Add(name);
                    }

                    _liftedState.Variables.Clear();
                }
            }

            // Skip useless expressions with no side effects in statement context (these can be the result of switch/conditional lifting
            // with assignment lowering)
            if (statementContext == ExpressionContext.Statement && !_sideEffectDetector.MayHaveSideEffects(translated))
            {
                continue;
            }

            var statement = translated switch
            {
                StatementSyntax s => s,

                // If this is the last line in an expression lambda, wrap it in a return statement.
                ExpressionSyntax e when _onLastLambdaLine && statementContext == ExpressionContext.ExpressionLambda
                    => ReturnStatement(e),

                // If we're in statement context and we have an expression that can't stand alone (e.g. literal), assign it to discard
                ExpressionSyntax e when statementContext == ExpressionContext.Statement && !IsExpressionValidAsStatement(e)
                    => ExpressionStatement((ExpressionSyntax)_g.AssignmentStatement(_g.IdentifierName("_"), e)),

                ExpressionSyntax e => ExpressionStatement(e),

                _ => throw new ArgumentOutOfRangeException()
            };

            if (blockContext == ExpressionContext.Expression)
            {
                // This block is in expression context, and so will be lifted (we won't be returning a block).
                _liftedState.Statements.Add(statement);
            }
            else
            {
                if (pendingLabeledStatement is not null)
                {
                    statement = pendingLabeledStatement.WithStatement(statement);
                    pendingLabeledStatement = null;
                }

                statements.Add(statement);
            }
        }

        // If a label existed on the last line of the block, add an empty statement (since C# requires it); for expression blocks we'd
        // have to lift that, not supported for now.
        if (pendingLabeledStatement is not null)
        {
            if (blockContext == ExpressionContext.Expression)
            {
                throw new NotImplementedException("Label on last expression of an expression block");
            }

            statements.Add(pendingLabeledStatement.WithStatement(EmptyStatement()));
        }

        // Above we transform top-level assignments (i = 8) to var-declarations with initializers (var i = 8); those variables have
        // already been taken care of and removed from the list.
        // But there may still be variables that get assigned inside nested blocks or other situations; prepare declarations for those
        // and either add them to the block, or lift them if we're an expression block.
        var unassignedVariableDeclarations =
            unassignedVariables.Select(v => (LocalDeclarationStatementSyntax)_g.LocalDeclarationStatement(
                Generate(v.Type), LookupVariableName(v), initializer: _g.DefaultExpression(Generate(v.Type))));

        if (blockContext == ExpressionContext.Expression)
        {
            _liftedState.UnassignedVariableDeclarations.AddRange(unassignedVariableDeclarations);
        }
        else
        {
            statements.InsertRange(0, unassignedVariableDeclarations.Concat(_liftedState.UnassignedVariableDeclarations));
            _liftedState.UnassignedVariableDeclarations.Clear();

            // We're done. If the block is in an expression context, it needs to be lifted out; but not if it's in a lambda (in that
            // case we just added return above).
            Result = Block(statements);
        }

        if (ownStackFrame is not null)
        {
            var popped = _stack.Pop();
            Check.DebugAssert(popped.Equals(ownStackFrame));
        }

        _onLastLambdaLine = parentOnLastLambdaLine;
        _liftedState = parentLiftedState;

        return block;

        // Returns true for expressions which have side-effects, and can therefore appear alone as a statement
        static bool IsExpressionValidAsStatement(ExpressionSyntax expression)
            => expression.Kind() switch
            {
                SyntaxKind.InvocationExpression => true,

                SyntaxKind.AddAssignmentExpression => true,
                SyntaxKind.AndAssignmentExpression => true,
                SyntaxKind.CoalesceAssignmentExpression => true,
                SyntaxKind.DivideAssignmentExpression => true,
                SyntaxKind.ModuloAssignmentExpression => true,
                SyntaxKind.MultiplyAssignmentExpression => true,
                SyntaxKind.OrAssignmentExpression => true,
                SyntaxKind.SimpleAssignmentExpression => true,
                SyntaxKind.SubtractAssignmentExpression => true,
                SyntaxKind.ExclusiveOrAssignmentExpression => true,
                SyntaxKind.LeftShiftAssignmentExpression => true,
                SyntaxKind.RightShiftAssignmentExpression => true,

                SyntaxKind.PostIncrementExpression => true,
                SyntaxKind.PostDecrementExpression => true,
                SyntaxKind.PreIncrementExpression => true,
                SyntaxKind.PreDecrementExpression => true,

                _ => false
            };

        void PreprocessLabels()
        {
            // LINQ label targets can be unnamed, so we need to generate names for unnamed ones and maintain a target->name mapping.
            // Also labels can have duplicated names - we need to de-duplicate them before we can generate a valid c# code
            // just like we do with variables/parameters
            // We need to maintain this as a stack for every block which has labels.
            // Normal blocks get their own labels stack frame, which gets popped when we leave the block. Expression labels add their
            // labels to their parent's stack frame (since they get lifted).
            var stackFrame = _stack.Peek();

            foreach (var label in block.Expressions.OfType<LabelExpression>())
            {
                if (stackFrame.Labels.TryGetValue(label.Target, out var identifier))
                {
                    continue;
                }

                var (_, _, labels, uniqueLabelNames) = stackFrame;

                // Generate names for unnamed label targets and uniquify (all label names)
                identifier = label.Target.Name ?? "unnamedLabel";
                var identifierBase = identifier;
                for (var i = 0; uniqueLabelNames.Contains(identifier); i++)
                {
                    identifier = identifierBase + i;
                }

                uniqueLabelNames.Add(identifier);
                labels.Add(label.Target, identifier);
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override Expression VisitBlock(BlockExpression block)
    {
        var blockContext = _context;

        var parentOnLastLambdaLine = _onLastLambdaLine;
        var parentLiftedState = _liftedState;

        // Expression blocks have no stack of their own, since they're lifted directly to their parent non-expression block.
        StackFrame? ownStackFrame = null;
        if (blockContext != ExpressionContext.Expression)
        {
            ownStackFrame = PushNewStackFrame();
            _liftedState = parentLiftedState.CreateChild();
        }

        var stackFrame = _stack.Peek();

        // Do a 1st pass to identify and register any labels, since goto can appear before its label.
        PreprocessLabels();

        // Go over the block's variables, assign names to any unnamed ones and uniquify. Then add them to our stack frame, unless
        // this is an expression block that will get lifted.
        foreach (var parameter in block.Variables)
        {
            var (variables, variableNames) = (stackFrame.Variables, stackFrame.VariableNames);

            var uniquifiedName = UniquifyVariableName(parameter.Name ?? "unnamed");

            if (blockContext == ExpressionContext.Expression)
            {
                if (!_liftedState.Variables.TryAdd(parameter, uniquifiedName))
                {
                    throw new NotSupportedException("Parameter clash during expression lifting for: " + parameter.Name);
                }

                _liftedState.VariableNames.Add(uniquifiedName);
            }
            else
            {
                if (!variables.TryAdd(parameter, uniquifiedName))
                {
                    throw new InvalidOperationException(
                        DesignStrings.SameParameterExpressionDeclaredAsVariableInNestedBlocks(parameter.Name ?? "<null>"));
                }

                variableNames.Add(uniquifiedName);
            }
        }

        var unassignedVariables = block.Variables.ToList();

        var statements = new List<StatementSyntax>();
        LabeledStatementSyntax? pendingLabeledStatement = null;

        // Now visit the block's expressions
        for (var i = 0; i < block.Expressions.Count; i++)
        {
            var expression = block.Expressions[i];
            var onLastBlockLine = i == block.Expressions.Count - 1;
            _onLastLambdaLine = parentOnLastLambdaLine && onLastBlockLine;

            // Any lines before the last are evaluated in statement context (they aren't returned); the last line is evaluated in the
            // context of the block as a whole. _context now refers to the statement's context, blockContext to the block's.
            var statementContext = onLastBlockLine ? _context : ExpressionContext.Statement;

            SyntaxNode translated;
            using (ChangeContext(statementContext))
            {
                translated = Translate(expression);
            }

            // If we have a labeled statement, unwrap it and keep the label as pending. VisitLabel returns a dummy statement (since
            // LINQ labels don't have a statement, unlike C#), so we'll skip that statement and add the label to the next real one.
            if (translated is LabeledStatementSyntax labeledStatement)
            {
                if (pendingLabeledStatement is not null)
                {
                    throw new NotImplementedException("Multiple labels on the same statement");
                }

                pendingLabeledStatement = labeledStatement;
                translated = labeledStatement.Statement;
            }

            // Syntax optimization. This is an assignment of a block variable to some value. Render this as:
            // var x = <expression>;
            // ... instead of:
            // int x;
            // x = <expression>;
            // ... except for expression context (i.e. on the last line), where we just return the value if needed.
            if (expression is BinaryExpression { NodeType: ExpressionType.Assign, Left: ParameterExpression lValue }
                && translated is AssignmentExpressionSyntax { Right: var valueSyntax }
                && statementContext == ExpressionContext.Statement
                && unassignedVariables.Remove(lValue))
            {
                var useExplicitVariableType = valueSyntax.Kind() == SyntaxKind.NullLiteralExpression;

                translated = useExplicitVariableType
                    ? _g.LocalDeclarationStatement(Generate(lValue.Type), LookupVariableName(lValue), valueSyntax)
                    : _g.LocalDeclarationStatement(LookupVariableName(lValue), valueSyntax);
            }

            if (statementContext == ExpressionContext.Expression)
            {
                // We're on the last line of a block in expression context - the block is being lifted out.
                // All statements before the last line (this one) have already been added to _liftedStatements, just return the last
                // expression.
                Check.DebugAssert(onLastBlockLine);
                Result = translated;
                break;
            }

            if (blockContext != ExpressionContext.Expression)
            {
                if (_liftedState.Statements.Count > 0)
                {
                    // If any expressions were lifted out of the current expression, flatten them into our own block, just before the
                    // expression from which they were lifted. Note that we don't do this in Expression context, since our own block is
                    // lifted out.
                    statements.AddRange(_liftedState.Statements);
                    _liftedState.Statements.Clear();
                }

                // Same for any variables being lifted out of the block; we add them to our own stack frame so that we can do proper
                // variable name uniquification etc.
                if (_liftedState.Variables.Count > 0)
                {
                    foreach (var (parameter, name) in _liftedState.Variables)
                    {
                        stackFrame.Variables[parameter] = name;
                        stackFrame.VariableNames.Add(name);
                    }

                    _liftedState.Variables.Clear();
                }
            }

            // Skip useless expressions with no side effects in statement context (these can be the result of switch/conditional lifting
            // with assignment lowering)
            if (statementContext == ExpressionContext.Statement && !_sideEffectDetector.MayHaveSideEffects(translated))
            {
                continue;
            }

            var statement = translated switch
            {
                StatementSyntax s => s,

                // If this is the last line in an expression lambda, wrap it in a return statement.
                ExpressionSyntax e when _onLastLambdaLine && statementContext == ExpressionContext.ExpressionLambda
                    => ReturnStatement(e),

                // If we're in statement context and we have an expression that can't stand alone (e.g. literal), assign it to discard
                ExpressionSyntax e when statementContext == ExpressionContext.Statement && !IsExpressionValidAsStatement(e)
                    => ExpressionStatement((ExpressionSyntax)_g.AssignmentStatement(_g.IdentifierName("_"), e)),

                ExpressionSyntax e => ExpressionStatement(e),

                _ => throw new ArgumentOutOfRangeException()
            };

            if (blockContext == ExpressionContext.Expression)
            {
                // This block is in expression context, and so will be lifted (we won't be returning a block).
                _liftedState.Statements.Add(statement);
            }
            else
            {
                if (pendingLabeledStatement is not null)
                {
                    statement = pendingLabeledStatement.WithStatement(statement);
                    pendingLabeledStatement = null;
                }

                statements.Add(statement);
            }
        }

        // If a label existed on the last line of the block, add an empty statement (since C# requires it); for expression blocks we'd
        // have to lift that, not supported for now.
        if (pendingLabeledStatement is not null)
        {
            if (blockContext == ExpressionContext.Expression)
            {
                throw new NotImplementedException("Label on last expression of an expression block");
            }

            statements.Add(pendingLabeledStatement.WithStatement(EmptyStatement()));
        }

        // Above we transform top-level assignments (i = 8) to var-declarations with initializers (var i = 8); those variables have
        // already been taken care of and removed from the list.
        // But there may still be variables that get assigned inside nested blocks or other situations; prepare declarations for those
        // and either add them to the block, or lift them if we're an expression block.
        var unassignedVariableDeclarations =
            unassignedVariables.Select(v => (LocalDeclarationStatementSyntax)_g.LocalDeclarationStatement(
                Generate(v.Type), LookupVariableName(v), initializer: _g.DefaultExpression(Generate(v.Type))));

        if (blockContext == ExpressionContext.Expression)
        {
            _liftedState.UnassignedVariableDeclarations.AddRange(unassignedVariableDeclarations);
        }
        else
        {
            statements.InsertRange(0, unassignedVariableDeclarations.Concat(_liftedState.UnassignedVariableDeclarations));
            _liftedState.UnassignedVariableDeclarations.Clear();

            // We're done. If the block is in an expression context, it needs to be lifted out; but not if it's in a lambda (in that
            // case we just added return above).
            Result = Block(statements);
        }

        if (ownStackFrame is not null)
        {
            var popped = _stack.Pop();
            Check.DebugAssert(popped.Equals(ownStackFrame));
        }

        _onLastLambdaLine = parentOnLastLambdaLine;
        _liftedState = parentLiftedState;

        return block;

        // Returns true for expressions which have side-effects, and can therefore appear alone as a statement
        static bool IsExpressionValidAsStatement(ExpressionSyntax expression)
            => expression.Kind() switch
            {
                SyntaxKind.InvocationExpression => true,

                SyntaxKind.AddAssignmentExpression => true,
                SyntaxKind.AndAssignmentExpression => true,
                SyntaxKind.CoalesceAssignmentExpression => true,
                SyntaxKind.DivideAssignmentExpression => true,
                SyntaxKind.ModuloAssignmentExpression => true,
                SyntaxKind.MultiplyAssignmentExpression => true,
                SyntaxKind.OrAssignmentExpression => true,
                SyntaxKind.SimpleAssignmentExpression => true,
                SyntaxKind.SubtractAssignmentExpression => true,
                SyntaxKind.ExclusiveOrAssignmentExpression => true,
                SyntaxKind.LeftShiftAssignmentExpression => true,
                SyntaxKind.RightShiftAssignmentExpression => true,

                SyntaxKind.PostIncrementExpression => true,
                SyntaxKind.PostDecrementExpression => true,
                SyntaxKind.PreIncrementExpression => true,
                SyntaxKind.PreDecrementExpression => true,

                _ => false
            };

        void PreprocessLabels()
        {
            // LINQ label targets can be unnamed, so we need to generate names for unnamed ones and maintain a target->name mapping.
            // Also labels can have duplicated names - we need to de-duplicate them before we can generate a valid c# code
            // just like we do with variables/parameters
            // We need to maintain this as a stack for every block which has labels.
            // Normal blocks get their own labels stack frame, which gets popped when we leave the block. Expression labels add their
            // labels to their parent's stack frame (since they get lifted).
            var stackFrame = _stack.Peek();

            foreach (var label in block.Expressions.OfType<LabelExpression>())
            {
                if (stackFrame.Labels.TryGetValue(label.Target, out var identifier))
                {
                    continue;
                }

                var (_, _, labels, uniqueLabelNames) = stackFrame;

                // Generate names for unnamed label targets, sanitize named ones, and uniquify (all label names)
                identifier = label.Target.Name is null ? "unnamedLabel" : SanitizeIdentifierName(label.Target.Name);
                var identifierBase = identifier;
                for (var i = 0; uniqueLabelNames.Contains(identifier); i++)
                {
                    identifier = identifierBase + i;
                }

                uniqueLabelNames.Add(identifier);
                labels.Add(label.Target, identifier);
            }
        }
    }
```

### 🔹 函式: `LinqToCSharpSyntaxTranslator.TranslateCore()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.TranslateCore(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors,
        bool statementContext)` (L153~L213)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.TranslateCore(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        IReadOnlySet<string>? declaredNames,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors,
        bool statementContext)` (L157~L254)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected virtual SyntaxNode TranslateCore(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors,
        bool statementContext)
    {
        _capturedVariables.Clear();
        _constantReplacements = constantReplacements;
        _collectedNamespaces = collectedNamespaces;
        _unnamedParameterCounter = 0;
        _context = statementContext ? ExpressionContext.Statement : ExpressionContext.Expression;
        _onLastLambdaLine = true;

        // The constant replacements (e.g. variables declared in the enclosing generated method for properties,
        // navigations, etc.) are in scope for the whole translation, so register their names in the root stack frame.
        // This keeps the in-scope variable tracking accurate, ensuring generated variables and lambda parameters don't
        // clash with them (their references are emitted by name inside the translated lambda bodies).
        var rootFrame = _stack.Peek();
        if (constantReplacements != null)
        {
            foreach (var name in constantReplacements.Values)
            {
                rootFrame.VariableNames.Add(name);
            }
        }

        try
        {
            Visit(node);
        }
        finally
        {
            if (constantReplacements != null)
            {
                foreach (var name in constantReplacements.Values)
                {
                    rootFrame.VariableNames.Remove(name);
                }
            }
        }

        if (_liftedState.Statements.Count > 0
            && _context == ExpressionContext.Expression)
        {
            throw new NotSupportedException("Lifted expressions remaining at top-level in expression context");
        }

        Check.DebugAssert(_stack.Count == 1, "_parameterStack.Count == 1");
        Check.DebugAssert(_stack.Peek().Variables.Count == 0, "_stack.Peek().Parameters.Count == 0");
        Check.DebugAssert(_stack.Peek().VariableNames.Count == 0, "_stack.Peek().ParameterNames.Count == 0");
        Check.DebugAssert(_stack.Peek().Labels.Count == 0);
        Check.DebugAssert(_stack.Peek().UniqueLabelNames.Count == 0);

        foreach (var unsafeAccessor in _fieldUnsafeAccessors.Values.Concat(_methodUnsafeAccessors.Values))
        {
            unsafeAccessors.Add(unsafeAccessor);
        }

        return Result!;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected virtual SyntaxNode TranslateCore(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        IReadOnlySet<string>? declaredNames,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors,
        bool statementContext)
    {
        _capturedVariables.Clear();
        // Names the expression references without declaring belong to the caller and are emitted as-is, so nothing generated here
        // may take one of them; collecting them up front means a name chosen later cannot rebind an earlier reference.
        _capturedVariableNames.Clear();
        FreeVariableNameCollector.Collect(node, _capturedVariableNames);
        _constantReplacements = constantReplacements;
        // Other names the caller declares in the scope the result is emitted into, such as the fields for the runtime constants when
        // one of their initializers is being translated; treated like the constant replacement names below.
        _declaredNames = declaredNames;
        _collectedNamespaces = collectedNamespaces;
        _unnamedParameterCounter = 0;
        _context = statementContext ? ExpressionContext.Statement : ExpressionContext.Expression;
        _onLastLambdaLine = true;

        // The constant replacements (e.g. variables declared in the enclosing generated method for properties,
        // navigations, etc.) are in scope for the whole translation, so register their names in the root stack frame.
        // This keeps the in-scope variable tracking accurate, ensuring generated variables and lambda parameters don't
        // clash with them (their references are emitted by name inside the translated lambda bodies).
        var rootFrame = _stack.Peek();
        if (constantReplacements != null)
        {
            foreach (var name in constantReplacements.Values)
            {
                rootFrame.VariableNames.Add(name);
            }
        }

        if (declaredNames != null)
        {
            foreach (var name in declaredNames)
            {
                rootFrame.VariableNames.Add(name);
            }
        }

        try
        {
            try
            {
                Visit(node);
            }
            finally
            {
                if (constantReplacements != null)
                {
                    foreach (var name in constantReplacements.Values)
                    {
                        rootFrame.VariableNames.Remove(name);
                    }
                }

                if (declaredNames != null)
                {
                    foreach (var name in declaredNames)
                    {
                        rootFrame.VariableNames.Remove(name);
                    }
                }
            }

            if (_liftedState.Statements.Count > 0
                && _context == ExpressionContext.Expression)
            {
                throw new NotSupportedException("Lifted expressions remaining at top-level in expression context");
            }

            Check.DebugAssert(_stack.Count == 1, "_parameterStack.Count == 1");
            Check.DebugAssert(_stack.Peek().Variables.Count == 0, "_stack.Peek().Parameters.Count == 0");
            Check.DebugAssert(_stack.Peek().VariableNames.Count == 0, "_stack.Peek().ParameterNames.Count == 0");
            Check.DebugAssert(_stack.Peek().Labels.Count == 0);
            Check.DebugAssert(_stack.Peek().UniqueLabelNames.Count == 0);
        }
        catch
        {
            // The translator is reused for later translations (PrecompiledQueryCodeGenerator records a failed query and moves on to
            // the next one), so the scopes and lifted statements a failed translation left behind must not leak into them
            _stack.Clear();
            _stack.Push(new StackFrame([], [], [], []));
            _liftedState = new LiftedState();

            throw;
        }

        foreach (var unsafeAccessor in _fieldUnsafeAccessors.Values.Concat(_methodUnsafeAccessors.Values))
        {
            unsafeAccessors.Add(unsafeAccessor);
        }

        return Result!;
    }
```

### 🔹 函式: `LinqToCSharpSyntaxTranslator.TranslateStatement()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.TranslateStatement(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors)` (L127~L132)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.TranslateStatement(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors,
        IReadOnlySet<string>? declaredNames = null)` (L129~L135)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public virtual SyntaxNode TranslateStatement(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors)
        => TranslateCore(node, constantReplacements, collectedNamespaces, unsafeAccessors, statementContext: true);
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public virtual SyntaxNode TranslateStatement(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors,
        IReadOnlySet<string>? declaredNames = null)
        => TranslateCore(node, constantReplacements, declaredNames, collectedNamespaces, unsafeAccessors, statementContext: true);
```

### 🔹 函式: `LinqToCSharpSyntaxTranslator.VisitInvocation()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.VisitInvocation(InvocationExpression invocation)` (L1238~L1284)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.VisitInvocation(InvocationExpression invocation)` (L1292~L1341)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override Expression VisitInvocation(InvocationExpression invocation)
    {
        if (invocation.Expression is LambdaExpression lambda)
        {
            // We need to inline the lambda invocation into the tree, by replacing parameters in the lambda body with the invocation arguments.
            // However, if an argument to the invocation can have side effects (e.g. a method call), and it's referenced multiple times from
            // the body, then that would cause multiple evaluation, which is wrong (same if the arguments are evaluated only once but in reverse
            // order).
            // So we have to lift such arguments.
            var arguments = new Expression[invocation.Arguments.Count];

            for (var i = 0; i < arguments.Length; i++)
            {
                var argument = invocation.Arguments[i];

                if (argument is ConstantExpression)
                {
                    // No need to evaluate into a separate variable, just pass directly
                    arguments[i] = argument;
                    continue;
                }

                // Need to lift
                var name = UniquifyVariableName(lambda.Parameters[i].Name ?? "lifted");
                var parameter = Expression.Parameter(argument.Type, name);
                _liftedState.Statements.Add(GenerateVarDeclaration(name, Translate<ExpressionSyntax>(argument)));
                _liftedState.VariableNames.Add(name);
                arguments[i] = parameter;
            }

            var replacedBody = new ReplacingExpressionVisitor(lambda.Parameters, arguments).Visit(lambda.Body);
            Result = Translate(replacedBody);
        }
        else
        {
            // The invocation is over a non-inline lambda expression (i.e. field/property/method)
            var expression = (ExpressionSyntax)Translate(invocation.Expression);

            var translatedExpressions = TranslateList(invocation.Arguments);

            Result = InvocationExpression(
                expression,
                ArgumentList(SeparatedList(translatedExpressions.Select(Argument))));
        }

        return invocation;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override Expression VisitInvocation(InvocationExpression invocation)
    {
        if (invocation.Expression is LambdaExpression lambda)
        {
            // We need to inline the lambda invocation into the tree, by replacing parameters in the lambda body with the invocation arguments.
            // However, if an argument to the invocation can have side effects (e.g. a method call), and it's referenced multiple times from
            // the body, then that would cause multiple evaluation, which is wrong (same if the arguments are evaluated only once but in reverse
            // order).
            // So we have to lift such arguments.
            var arguments = new Expression[invocation.Arguments.Count];

            for (var i = 0; i < arguments.Length; i++)
            {
                var argument = invocation.Arguments[i];

                if (argument is ConstantExpression)
                {
                    // No need to evaluate into a separate variable, just pass directly
                    arguments[i] = argument;
                    continue;
                }

                // Need to lift
                var name = UniquifyVariableName(lambda.Parameters[i].Name ?? "lifted");
                var parameter = Expression.Parameter(argument.Type, name);
                _liftedState.Statements.Add(GenerateVarDeclaration(name, Translate<ExpressionSyntax>(argument)));
                _liftedState.VariableNames.Add(name);
                // The body references this parameter in place of the lambda's; registering it means those references resolve to
                // the lifted local by identity rather than by its name happening to match
                _liftedState.Variables[parameter] = name;
                arguments[i] = parameter;
            }

            var replacedBody = new ReplacingExpressionVisitor(lambda.Parameters, arguments).Visit(lambda.Body);
            Result = Translate(replacedBody);
        }
        else
        {
            // The invocation is over a non-inline lambda expression (i.e. field/property/method)
            var expression = (ExpressionSyntax)Translate(invocation.Expression);

            var translatedExpressions = TranslateList(invocation.Arguments);

            Result = InvocationExpression(
                expression,
                ArgumentList(SeparatedList(translatedExpressions.Select(Argument))));
        }

        return invocation;
    }
```

### 🔹 函式: `LinqToCSharpSyntaxTranslator.TranslateCatchBlock()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.TranslateCatchBlock(CatchBlock catchBlock, bool noType = false)` (L796~L826)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.TranslateCatchBlock(CatchBlock catchBlock, bool noType = false)` (L837~L880)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected virtual SyntaxNode TranslateCatchBlock(CatchBlock catchBlock, bool noType = false)
    {
        var translatedBody = Translate(catchBlock.Body) switch
        {
            BlockSyntax b => b,
            StatementSyntax s => Block(s),
            ExpressionSyntax e => Block(ExpressionStatement(e)),
            _ => throw new ArgumentOutOfRangeException()
        };

        var catchDeclaration = noType
            ? null
            : CatchDeclaration(Generate(catchBlock.Test));

        if (catchBlock.Variable is not null)
        {
            Check.DebugAssert(catchDeclaration is not null);

            if (catchBlock.Variable.Name is null)
            {
                throw new NotSupportedException("TranslateCatchBlock: unnamed parameter as catch variable");
            }

            catchDeclaration = catchDeclaration.WithIdentifier(Identifier(catchBlock.Variable.Name));
        }

        return CatchClause(
            catchDeclaration,
            catchBlock.Filter is null ? null : CatchFilterClause(Translate<ExpressionSyntax>(catchBlock.Filter)),
            translatedBody);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected virtual SyntaxNode TranslateCatchBlock(CatchBlock catchBlock, bool noType = false)
    {
        if (catchBlock.Variable is { Name: null })
        {
            throw new NotSupportedException("TranslateCatchBlock: unnamed parameter as catch variable");
        }

        var catchDeclaration = noType
            ? null
            : CatchDeclaration(Generate(catchBlock.Test));

        // The catch variable gets its own scope, so that its declaration and the references to it agree on the (sanitized) name
        var stackFrame = PushNewStackFrame();

        if (catchBlock.Variable is not null)
        {
            Check.DebugAssert(catchDeclaration is not null);

            var name = UniquifyVariableName(catchBlock.Variable.Name!);
            if (!stackFrame.Variables.TryAdd(catchBlock.Variable, name))
            {
                throw new InvalidOperationException(
                    DesignStrings.SameParameterExpressionDeclaredAsVariableInNestedBlocks(catchBlock.Variable.Name));
            }

            stackFrame.VariableNames.Add(name);
            catchDeclaration = catchDeclaration.WithIdentifier(Identifier(name));
        }

        var translatedBody = Translate(catchBlock.Body) switch
        {
            BlockSyntax b => b,
            StatementSyntax s => Block(s),
            ExpressionSyntax e => Block(ExpressionStatement(e)),
            _ => throw new ArgumentOutOfRangeException()
        };

        var filter = catchBlock.Filter is null ? null : CatchFilterClause(Translate<ExpressionSyntax>(catchBlock.Filter));

        var popped = _stack.Pop();
        Check.DebugAssert(popped.Equals(stackFrame));

        return CatchClause(catchDeclaration, filter, translatedBody);
    }
```

### 🔹 函式: `LinqToCSharpSyntaxTranslator.PreprocessLabels()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.PreprocessLabels()` (L749~L779)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.PreprocessLabels()` (L790~L820)

#### ◀️ 變更前實作碼 (Before Implementation):
```
void PreprocessLabels()
        {
            // LINQ label targets can be unnamed, so we need to generate names for unnamed ones and maintain a target->name mapping.
            // Also labels can have duplicated names - we need to de-duplicate them before we can generate a valid c# code
            // just like we do with variables/parameters
            // We need to maintain this as a stack for every block which has labels.
            // Normal blocks get their own labels stack frame, which gets popped when we leave the block. Expression labels add their
            // labels to their parent's stack frame (since they get lifted).
            var stackFrame = _stack.Peek();

            foreach (var label in block.Expressions.OfType<LabelExpression>())
            {
                if (stackFrame.Labels.TryGetValue(label.Target, out var identifier))
                {
                    continue;
                }

                var (_, _, labels, uniqueLabelNames) = stackFrame;

                // Generate names for unnamed label targets and uniquify (all label names)
                identifier = label.Target.Name ?? "unnamedLabel";
                var identifierBase = identifier;
                for (var i = 0; uniqueLabelNames.Contains(identifier); i++)
                {
                    identifier = identifierBase + i;
                }

                uniqueLabelNames.Add(identifier);
                labels.Add(label.Target, identifier);
            }
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
void PreprocessLabels()
        {
            // LINQ label targets can be unnamed, so we need to generate names for unnamed ones and maintain a target->name mapping.
            // Also labels can have duplicated names - we need to de-duplicate them before we can generate a valid c# code
            // just like we do with variables/parameters
            // We need to maintain this as a stack for every block which has labels.
            // Normal blocks get their own labels stack frame, which gets popped when we leave the block. Expression labels add their
            // labels to their parent's stack frame (since they get lifted).
            var stackFrame = _stack.Peek();

            foreach (var label in block.Expressions.OfType<LabelExpression>())
            {
                if (stackFrame.Labels.TryGetValue(label.Target, out var identifier))
                {
                    continue;
                }

                var (_, _, labels, uniqueLabelNames) = stackFrame;

                // Generate names for unnamed label targets, sanitize named ones, and uniquify (all label names)
                identifier = label.Target.Name is null ? "unnamedLabel" : SanitizeIdentifierName(label.Target.Name);
                var identifierBase = identifier;
                for (var i = 0; uniqueLabelNames.Contains(identifier); i++)
                {
                    identifier = identifierBase + i;
                }

                uniqueLabelNames.Add(identifier);
                labels.Add(label.Target, identifier);
            }
        }
```

### 🔹 函式: `LinqToCSharpSyntaxTranslator.TranslateExpression()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.TranslateExpression(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors)` (L140~L145)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.TranslateExpression(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors,
        IReadOnlySet<string>? declaredNames = null)` (L143~L149)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public virtual SyntaxNode TranslateExpression(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors)
        => TranslateCore(node, constantReplacements, collectedNamespaces, unsafeAccessors, statementContext: false);
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public virtual SyntaxNode TranslateExpression(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors,
        IReadOnlySet<string>? declaredNames = null)
        => TranslateCore(node, constantReplacements, declaredNames, collectedNamespaces, unsafeAccessors, statementContext: false);
```

### 🔹 函式: `LinqToCSharpSyntaxTranslator.TryGenerate()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.TryGenerate(Type type, [NotNullWhen(true)] out TypeSyntax? result)` (L1346~L1519)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.TryGenerate(Type type, [NotNullWhen(true)] out TypeSyntax? result)` (L1403~L1588)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected virtual bool TryGenerate(Type type, [NotNullWhen(true)] out TypeSyntax? result)
    {
        result = null;
        if (type.IsAnonymousType())
        {
            return false;
        }

        if (type.IsGenericType)
        {
            if (type.IsConstructedGenericType
                && type.GetGenericTypeDefinition() == typeof(Nullable<>))
            {
                result = NullableType(Generate(type.GenericTypeArguments[0]));
                return true;
            }

            var genericArguments = new List<TypeSyntax>();
            foreach (var genericArgument in type.GenericTypeArguments)
            {
                if (!TryGenerate(genericArgument, out var syntax))
                {
                    return false;
                }

                genericArguments.Add(syntax);
            }

            result = GenerateGenericType(type, genericArguments, genericArguments.Count);
            return true;
        }

        if (type.IsArray)
        {
            result = ArrayType(Generate(type.GetElementType()!))
                .WithRankSpecifiers(
                    SingletonList(ArrayRankSpecifier(SingletonSeparatedList<ExpressionSyntax>(OmittedArraySizeExpression()))));
            return true;
        }

        if (type == typeof(string))
        {
            result = PredefinedType(Token(SyntaxKind.StringKeyword));
            return true;
        }

        if (type == typeof(bool))
        {
            result = PredefinedType(Token(SyntaxKind.BoolKeyword));
            return true;
        }

        if (type == typeof(byte))
        {
            result = PredefinedType(Token(SyntaxKind.ByteKeyword));
            return true;
        }

        if (type == typeof(sbyte))
        {
            result = PredefinedType(Token(SyntaxKind.SByteKeyword));
            return true;
        }

        if (type == typeof(int))
        {
            result = PredefinedType(Token(SyntaxKind.IntKeyword));
            return true;
        }

        if (type == typeof(uint))
        {
            result = PredefinedType(Token(SyntaxKind.UIntKeyword));
            return true;
        }

        if (type == typeof(short))
        {
            result = PredefinedType(Token(SyntaxKind.ShortKeyword));
            return true;
        }

        if (type == typeof(ushort))
        {
            result = PredefinedType(Token(SyntaxKind.UShortKeyword));
            return true;
        }

        if (type == typeof(long))
        {
            result = PredefinedType(Token(SyntaxKind.LongKeyword));
            return true;
        }

        if (type == typeof(ulong))
        {
            result = PredefinedType(Token(SyntaxKind.ULongKeyword));
            return true;
        }

        if (type == typeof(float))
        {
            result = PredefinedType(Token(SyntaxKind.FloatKeyword));
            return true;
        }

        if (type == typeof(double))
        {
            result = PredefinedType(Token(SyntaxKind.DoubleKeyword));
            return true;
        }

        if (type == typeof(decimal))
        {
            result = PredefinedType(Token(SyntaxKind.DecimalKeyword));
            return true;
        }

        if (type == typeof(char))
        {
            result = PredefinedType(Token(SyntaxKind.CharKeyword));
            return true;
        }

        if (type == typeof(object))
        {
            result = PredefinedType(Token(SyntaxKind.ObjectKeyword));
            return true;
        }

        if (type == typeof(void))
        {
            result = PredefinedType(Token(SyntaxKind.VoidKeyword));
            return true;
        }

        if (type.IsNested)
        {
            result = QualifiedName(
                (NameSyntax)Generate(type.DeclaringType!),
                IdentifierName(type.Name));
            return true;
        }

        if (type.Namespace != null)
        {
            _collectedNamespaces.Add(type.Namespace);
        }

        result = IdentifierName(type.Name);
        return true;

        NameSyntax GenerateGenericType(Type type, List<TypeSyntax> genericArguments, int length)
        {
            var offset = type.DeclaringType != null ? type.DeclaringType.GetGenericArguments().Length : 0;

            var genericPartIndex = type.Name.IndexOf('`');
            SimpleNameSyntax nameSyntax = genericPartIndex <= 0
                ? IdentifierName(type.Name)
                : GenericName(
                    Identifier(type.Name[..genericPartIndex]),
                    TypeArgumentList(SeparatedList(genericArguments.Skip(offset).Take(length - offset))));
            if (type.DeclaringType == null)
            {
                AddNamespace(type);

                return nameSyntax;
            }

            return QualifiedName(
                GenerateGenericType(type.DeclaringType, genericArguments, offset),
                nameSyntax);
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected virtual bool TryGenerate(Type type, [NotNullWhen(true)] out TypeSyntax? result)
    {
        result = null;
        if (type.IsAnonymousType())
        {
            return false;
        }

        if (type.IsGenericType)
        {
            if (type.IsConstructedGenericType
                && type.GetGenericTypeDefinition() == typeof(Nullable<>))
            {
                result = NullableType(Generate(type.GenericTypeArguments[0]));
                return true;
            }

            var genericArguments = new List<TypeSyntax>();
            foreach (var genericArgument in type.GenericTypeArguments)
            {
                if (!TryGenerate(genericArgument, out var syntax))
                {
                    return false;
                }

                genericArguments.Add(syntax);
            }

            result = GenerateGenericType(type, genericArguments, genericArguments.Count);
            return true;
        }

        if (type.IsArray)
        {
            result = ArrayType(Generate(type.GetElementType()!))
                .WithRankSpecifiers(
                    SingletonList(ArrayRankSpecifier(SingletonSeparatedList<ExpressionSyntax>(OmittedArraySizeExpression()))));
            return true;
        }

        if (type == typeof(string))
        {
            result = PredefinedType(Token(SyntaxKind.StringKeyword));
            return true;
        }

        if (type == typeof(bool))
        {
            result = PredefinedType(Token(SyntaxKind.BoolKeyword));
            return true;
        }

        if (type == typeof(byte))
        {
            result = PredefinedType(Token(SyntaxKind.ByteKeyword));
            return true;
        }

        if (type == typeof(sbyte))
        {
            result = PredefinedType(Token(SyntaxKind.SByteKeyword));
            return true;
        }

        if (type == typeof(int))
        {
            result = PredefinedType(Token(SyntaxKind.IntKeyword));
            return true;
        }

        if (type == typeof(uint))
        {
            result = PredefinedType(Token(SyntaxKind.UIntKeyword));
            return true;
        }

        if (type == typeof(short))
        {
            result = PredefinedType(Token(SyntaxKind.ShortKeyword));
            return true;
        }

        if (type == typeof(ushort))
        {
            result = PredefinedType(Token(SyntaxKind.UShortKeyword));
            return true;
        }

        if (type == typeof(long))
        {
            result = PredefinedType(Token(SyntaxKind.LongKeyword));
            return true;
        }

        if (type == typeof(ulong))
        {
            result = PredefinedType(Token(SyntaxKind.ULongKeyword));
            return true;
        }

        if (type == typeof(float))
        {
            result = PredefinedType(Token(SyntaxKind.FloatKeyword));
            return true;
        }

        if (type == typeof(double))
        {
            result = PredefinedType(Token(SyntaxKind.DoubleKeyword));
            return true;
        }

        if (type == typeof(decimal))
        {
            result = PredefinedType(Token(SyntaxKind.DecimalKeyword));
            return true;
        }

        if (type == typeof(char))
        {
            result = PredefinedType(Token(SyntaxKind.CharKeyword));
            return true;
        }

        if (type == typeof(object))
        {
            result = PredefinedType(Token(SyntaxKind.ObjectKeyword));
            return true;
        }

        if (type == typeof(void))
        {
            result = PredefinedType(Token(SyntaxKind.VoidKeyword));
            return true;
        }

        if (type.IsNested)
        {
            result = QualifiedName(
                (NameSyntax)Generate(type.DeclaringType!),
                IdentifierName(type.Name));
            return true;
        }

        if (IsNameInScope(type.Name))
        {
            result = GloballyQualified(type.Namespace, IdentifierName(type.Name));
            return true;
        }

        if (type.Namespace != null)
        {
            _collectedNamespaces.Add(type.Namespace);
        }

        result = IdentifierName(type.Name);
        return true;

        NameSyntax GenerateGenericType(Type type, List<TypeSyntax> genericArguments, int length)
        {
            var offset = type.DeclaringType != null ? type.DeclaringType.GetGenericArguments().Length : 0;

            var genericPartIndex = type.Name.IndexOf('`');
            var simpleName = genericPartIndex <= 0 ? type.Name : type.Name[..genericPartIndex];
            SimpleNameSyntax nameSyntax = genericPartIndex <= 0
                ? IdentifierName(type.Name)
                : GenericName(
                    Identifier(simpleName),
                    TypeArgumentList(SeparatedList(genericArguments.Skip(offset).Take(length - offset))));
            if (type.DeclaringType == null)
            {
                if (IsNameInScope(simpleName))
                {
                    return GloballyQualified(type.Namespace, nameSyntax);
                }

                AddNamespace(type);

                return nameSyntax;
            }

            return QualifiedName(
                GenerateGenericType(type.DeclaringType, genericArguments, offset),
                nameSyntax);
        }
    }
```

### 🔹 函式: `LinqToCSharpSyntaxTranslator.GenerateGenericType()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.GenerateGenericType(Type type, List<TypeSyntax> genericArguments, int length)` (L1498~L1518)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.GenerateGenericType(Type type, List<TypeSyntax> genericArguments, int length)` (L1561~L1587)

#### ◀️ 變更前實作碼 (Before Implementation):
```
NameSyntax GenerateGenericType(Type type, List<TypeSyntax> genericArguments, int length)
        {
            var offset = type.DeclaringType != null ? type.DeclaringType.GetGenericArguments().Length : 0;

            var genericPartIndex = type.Name.IndexOf('`');
            SimpleNameSyntax nameSyntax = genericPartIndex <= 0
                ? IdentifierName(type.Name)
                : GenericName(
                    Identifier(type.Name[..genericPartIndex]),
                    TypeArgumentList(SeparatedList(genericArguments.Skip(offset).Take(length - offset))));
            if (type.DeclaringType == null)
            {
                AddNamespace(type);

                return nameSyntax;
            }

            return QualifiedName(
                GenerateGenericType(type.DeclaringType, genericArguments, offset),
                nameSyntax);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
NameSyntax GenerateGenericType(Type type, List<TypeSyntax> genericArguments, int length)
        {
            var offset = type.DeclaringType != null ? type.DeclaringType.GetGenericArguments().Length : 0;

            var genericPartIndex = type.Name.IndexOf('`');
            var simpleName = genericPartIndex <= 0 ? type.Name : type.Name[..genericPartIndex];
            SimpleNameSyntax nameSyntax = genericPartIndex <= 0
                ? IdentifierName(type.Name)
                : GenericName(
                    Identifier(simpleName),
                    TypeArgumentList(SeparatedList(genericArguments.Skip(offset).Take(length - offset))));
            if (type.DeclaringType == null)
            {
                if (IsNameInScope(simpleName))
                {
                    return GloballyQualified(type.Namespace, nameSyntax);
                }

                AddNamespace(type);

                return nameSyntax;
            }

            return QualifiedName(
                GenerateGenericType(type.DeclaringType, genericArguments, offset),
                nameSyntax);
        }
```

### 🔹 函式: `LinqToCSharpSyntaxTranslator.UniquifyVariableName()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.UniquifyVariableName(string? name)` (L2825~L2846)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.UniquifyVariableName(string? name)` (L3004~L3025)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private string UniquifyVariableName(string? name)
    {
        var isUnnamed = name is null;
        name ??= "unnamed";

        var parameterNames = _stack.Peek().VariableNames;

        Func<string, bool> constantReplacementsContainsName =
            _constantReplacements is BidirectionalDictionary<object, string> bidirectionalDictionary
                ? bidirectionalDictionary.ContainsValue
                : n => _constantReplacements?.Values.Contains(n) == true;

        var baseName = name;
        for (var j = isUnnamed ? _unnamedParameterCounter++ : 0;
             parameterNames.Contains(name) || _liftedState.VariableNames.Contains(name) || constantReplacementsContainsName(name);
             j++)
        {
            name = baseName + j;
        }

        return name;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private string UniquifyVariableName(string? name)
    {
        var isUnnamed = name is null;
        // Expression tree variable names are arbitrary strings (e.g. derived from JSON property names) and must become valid identifiers.
        name = name is null ? "unnamed" : SanitizeIdentifierName(name);

        var parameterNames = _stack.Peek().VariableNames;

        var baseName = name;
        for (var j = isUnnamed ? _unnamedParameterCounter++ : 0;
             parameterNames.Contains(name)
             || _liftedState.VariableNames.Contains(name)
             || IsCallerDeclaredName(name)
             // A captured variable already emitted under this name would be rebound by a local we declare now
             || _capturedVariableNames.Contains(name);
             j++)
        {
            name = baseName + j;
        }

        return name;
    }
```

### 🔹 函式: `LinqToCSharpSyntaxTranslator.VisitParameter()`
- **變更前簽章 (Before)**: `LinqToCSharpSyntaxTranslator.VisitParameter(ParameterExpression parameter)` (L2181~L2204)
- **變更後簽章 (After)**: `LinqToCSharpSyntaxTranslator.VisitParameter(ParameterExpression parameter)` (L2264~L2300)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override Expression VisitParameter(ParameterExpression parameter)
    {
        // Note that the parameter in the lambda declaration is handled separately in VisitLambda
        if (_stack.Peek().Variables.TryGetValue(parameter, out var name)
            || _liftedState.Variables.TryGetValue(parameter, out name))
        {
            Result = IdentifierName(name);

            return parameter;
        }

        // This parameter is unknown to us - it's captured from outside the entire expression tree.
        // Simply return its name without worrying about uniquification, since the variable needs to correspond to the outside in any
        // case (it's the callers responsibility).
        _capturedVariables.Add(parameter);

        if (parameter.Name is null)
        {
            throw new NotSupportedException("Unnamed captured variable");
        }

        Result = IdentifierName(parameter.Name);
        return parameter;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override Expression VisitParameter(ParameterExpression parameter)
    {
        // Note that the parameter in the lambda declaration is handled separately in VisitLambda
        if (_stack.Peek().Variables.TryGetValue(parameter, out var name)
            || _liftedState.Variables.TryGetValue(parameter, out name))
        {
            Result = IdentifierName(name);

            return parameter;
        }

        // This parameter is unknown to us - it's captured from outside the entire expression tree.
        // Simply return its name without worrying about uniquification, since the variable needs to correspond to the outside in any
        // case (it's the callers responsibility).
        _capturedVariables.Add(parameter);

        if (parameter.Name is null)
        {
            throw new NotSupportedException("Unnamed captured variable");
        }

        // Since the name is emitted as-is, anything we generated under that same name would capture the reference instead. That
        // includes generated locals, which exist in these scopes by name only. Constant replacement names are excluded: they are
        // the caller's own declarations, and referencing them is exactly what a captured variable of that name means to do.
        var comparableName = WithoutFormattingCharacters(parameter.Name);
        if ((_stack.Peek().VariableNames.Contains(comparableName) || _liftedState.VariableNames.Contains(comparableName))
            && !IsCallerDeclaredName(comparableName))
        {
            throw new NotSupportedException(
                $"Captured variable '{parameter.Name}' is shadowed by a variable generated for the translated expression");
        }

        _capturedVariableNames.Add(comparableName);

        Result = IdentifierName(parameter.Name);
        return parameter;
    }
```


#### 📄 檔案: `src/EFCore.Design/Query/Internal/PrecompiledQueryCodeGenerator.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:229, E:221, A:0) ➔ After(N:257, E:241, A:0)
- **差分統計**: +Nodes: 57, -Nodes: 29, +Edges: 39, -Edges: 19, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `RelationalModelVariable` (MODULE_STATE)
  • + [新增節點] `queryCode.ToString().TrimEnd (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `code
            .AppendLine(
                $"private static object Query{queryNum}_GenerateExecutor(DbContext {DbContextVariable}, QueryContext {QueryContextVariable})")
            .AppendLine("{")
            .IncrementIndent()
            .AppendLine($"var {RelationalModelVariable} = {DbContextVariable}.Model.GetRelationalModel();")
            .AppendLine($"var {RelationalTypeMappingSourceVariable} = {DbContextVariable}.GetService<IRelationalTypeMappingSource>();")
            .AppendLine($"var {MaterializerLiftableConstantContextVariable} = new RelationalMaterializerLiftableConstantContext(")
            .AppendLine (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_runtimeConstantsByInitializer.TryAdd (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `GeneratedExecutorVariableNames` (MODULE_STATE)
  • + [新增節點] `_runtimeConstants.Keys.ToHashSet (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_constantReplacements.ContainsKey (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_runtimeConstantsOfCurrentQuery.Clear (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_runtimeConstantsOfCurrentQuery.Add (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `QueryContextVariable` (MODULE_STATE)
  • + [新增節點] `RelationalTypeMappingSourceVariable` (MODULE_STATE)
  • + [新增節點] `LinqToCSharpSyntaxTranslator.SanitizeIdentifierName (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `declared.TryGetValue (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_runtimeConstantsByInitializer.TryGetValue (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `DeclaredRuntimeConstantReplacingExpressionVisitor.VisitExtension` (FUNCTION_DEF)
  • _... 以及其餘 129 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `PrecompiledQueryCodeGenerator.GenerateQueryExecutor()`
- **變更前簽章 (Before)**: `PrecompiledQueryCodeGenerator.GenerateQueryExecutor(
        IndentedStringBuilder code,
        int queryNum,
        Expression queryExecutor,
        HashSet<string> namespaces,
        HashSet<MethodDeclarationSyntax> unsafeAccessors)` (L934~L1004)
- **變更後簽章 (After)**: `PrecompiledQueryCodeGenerator.GenerateQueryExecutor(
        IndentedStringBuilder code,
        int queryNum,
        Expression queryExecutor,
        HashSet<string> namespaces,
        HashSet<MethodDeclarationSyntax> unsafeAccessors)` (L993~L1128)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private void GenerateQueryExecutor(
        IndentedStringBuilder code,
        int queryNum,
        Expression queryExecutor,
        HashSet<string> namespaces,
        HashSet<MethodDeclarationSyntax> unsafeAccessors)
    {
        // We're going to generate the method which will create the query executor (Func<QueryContext, TResult>).
        // Note that the we store the executor itself (and return it) as object, not as a typed Func<QueryContext, TResult>.
        // We can't strong-type it since it may return an anonymous type, which is unspeakable; so instead we cast down from object to
        // the real strongly-typed signature inside the interceptor, where the return value is represented as a generic type parameter
        // (which can be an anonymous type).
        code
            .AppendLine($"private static object Query{queryNum}_GenerateExecutor(DbContext dbContext, QueryContext queryContext)")
            .AppendLine("{")
            .IncrementIndent()
            .AppendLine("var relationalModel = dbContext.Model.GetRelationalModel();")
            .AppendLine("var relationalTypeMappingSource = dbContext.GetService<IRelationalTypeMappingSource>();")
            .AppendLine("var materializerLiftableConstantContext = new RelationalMaterializerLiftableConstantContext(")
            .AppendLine("    dbContext.GetService<ShapedQueryCompilingExpressionVisitorDependencies>(),")
            .AppendLine("    dbContext.GetService<RelationalShapedQueryCompilingExpressionVisitorDependencies>(),")
            .AppendLine("    dbContext.GetService<RelationalCommandBuilderDependencies>());");

        queryExecutor = _runtimeConstantProcessor.Process(queryExecutor);
        foreach (var runtimeConstant in _runtimeConstantProcessor.LastProcessFoundRuntimeConstants)
        {
            var name = SanitizeIdentifierName(runtimeConstant.Name);
            var baseName = name;
            for (var j = 0; _runtimeConstants.ContainsKey(name); j++)
            {
                name = baseName + j;
            }

            _runtimeConstants.Add(name, runtimeConstant);
            _constantReplacements.Add(runtimeConstant.Value, name);
        }

        HashSet<string> variableNames =
            [.. _constantReplacements.Values, "relationalModel", "relationalTypeMappingSource", "materializerLiftableConstantContext"];

        var materializerLiftableConstantContext =
            Expression.Parameter(typeof(RelationalMaterializerLiftableConstantContext), "materializerLiftableConstantContext");

        // The materializer expression tree contains LiftedConstantExpression nodes, which contain instructions on how to resolve
        // constant values which need to be lifted.
        var queryExecutorAfterLiftingExpression =
            _liftableConstantProcessor.LiftConstants(queryExecutor, materializerLiftableConstantContext, variableNames);

        foreach (var liftedConstant in _liftableConstantProcessor.LiftedConstants)
        {
            var variableValueSyntax = _linqToCSharpTranslator.TranslateExpression(
                liftedConstant.Expression, _constantReplacements, _memberAccessReplacements, namespaces, unsafeAccessors);
            // code.AppendLine($"{liftedConstant.Parameter.Type.Name} {liftedConstant.Parameter.Name} = {variableValueSyntax.NormalizeWhitespace().ToFullString()};");
            code.AppendLine($"var {liftedConstant.Parameter.Name} = {variableValueSyntax.NormalizeWhitespace().ToFullString()};");
        }

        var queryExecutorSyntaxTree =
            (AnonymousFunctionExpressionSyntax)_linqToCSharpTranslator.TranslateExpression(
                queryExecutorAfterLiftingExpression,
                _constantReplacements,
                _memberAccessReplacements,
                namespaces,
                unsafeAccessors);

        code
            .AppendLine($"return {queryExecutorSyntaxTree.NormalizeWhitespace().ToFullString()};")
            .DecrementIndent()
            .AppendLine("}")
            .AppendLine()
            .AppendLine($"private static object Query{queryNum}_Executor;");
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private void GenerateQueryExecutor(
        IndentedStringBuilder code,
        int queryNum,
        Expression queryExecutor,
        HashSet<string> namespaces,
        HashSet<MethodDeclarationSyntax> unsafeAccessors)
    {
        // We're going to generate the method which will create the query executor (Func<QueryContext, TResult>).
        // Note that the we store the executor itself (and return it) as object, not as a typed Func<QueryContext, TResult>.
        // We can't strong-type it since it may return an anonymous type, which is unspeakable; so instead we cast down from object to
        // the real strongly-typed signature inside the interceptor, where the return value is represented as a generic type parameter
        // (which can be an anonymous type).
        code
            .AppendLine(
                $"private static object Query{queryNum}_GenerateExecutor(DbContext {DbContextVariable}, QueryContext {QueryContextVariable})")
            .AppendLine("{")
            .IncrementIndent()
            .AppendLine($"var {RelationalModelVariable} = {DbContextVariable}.Model.GetRelationalModel();")
            .AppendLine($"var {RelationalTypeMappingSourceVariable} = {DbContextVariable}.GetService<IRelationalTypeMappingSource>();")
            .AppendLine($"var {MaterializerLiftableConstantContextVariable} = new RelationalMaterializerLiftableConstantContext(")
            .AppendLine($"    {DbContextVariable}.GetService<ShapedQueryCompilingExpressionVisitorDependencies>(),")
            .AppendLine($"    {DbContextVariable}.GetService<RelationalShapedQueryCompilingExpressionVisitorDependencies>(),")
            .AppendLine($"    {DbContextVariable}.GetService<RelationalCommandBuilderDependencies>());");

        // A processor per query: its deduplication cache would otherwise outlive a query that failed and was rolled back, so a
        // later query reusing the same constant would be told it is already registered and end up with no field to reference.
        // Constants shared between queries are deduplicated here instead, against what has actually been declared. Equality by
        // value is not enough for that: the shaper evaluates a runtime constant's initializer afresh for every query, so the same
        // JSON property name in two queries is two byte arrays. A constant whose initializer matches a declared one is replaced by
        // that constant's value, which the translator emits as the existing field.
        queryExecutor = new DeclaredRuntimeConstantReplacingExpressionVisitor(_runtimeConstantsByInitializer).Visit(queryExecutor);
        var runtimeConstantProcessor = new RuntimeConstantProcessor();
        queryExecutor = runtimeConstantProcessor.Process(queryExecutor);
        foreach (var runtimeConstant in runtimeConstantProcessor.LastProcessFoundRuntimeConstants)
        {
            if (_constantReplacements.ContainsKey(runtimeConstant.Value))
            {
                continue;
            }

            // A runtime constant becomes a field of the interceptors class under a name that came from the model or from a provider.
            // The members the class declares for itself and the executor's parameters all start with a letter, so a field name that
            // starts with an underscore is none of them, and nothing has to be reserved family by family. A type can start with one,
            // which is why the translator writes out any type whose simple name is in use in the emitted scope fully qualified. The
            // lifted constants, which can start with an underscore as well, are uniquified against these names below. The prefixed
            // name is what gets sanitized, since the prefix can itself complete a reserved token: _arglist is an identifier,
            // __arglist is not.
            var name = LinqToCSharpSyntaxTranslator.SanitizeIdentifierName("_" + runtimeConstant.Name);
            var baseName = name;
            for (var j = 0; _runtimeConstants.ContainsKey(name); j++)
            {
                name = baseName + j;
            }

            _runtimeConstants.Add(name, runtimeConstant);
            _constantReplacements.Add(runtimeConstant.Value, name);
            _runtimeConstantsByInitializer.TryAdd(runtimeConstant.InitializeExpression, runtimeConstant);
            _runtimeConstantsOfCurrentQuery.Add(name);
        }

        // Everything the generated executor declares for itself, so that nothing named by the model or by a provider can take
        // one of these names. Keep in step with the declarations emitted below.
        HashSet<string> variableNames = [.. _constantReplacements.Values, .. GeneratedExecutorVariableNames];

        var materializerLiftableConstantContext =
            Expression.Parameter(typeof(RelationalMaterializerLiftableConstantContext), MaterializerLiftableConstantContextVariable);

        // The materializer expression tree contains LiftedConstantExpression nodes, which contain instructions on how to resolve
        // constant values which need to be lifted.
        var queryExecutorAfterLiftingExpression =
            _liftableConstantProcessor.LiftConstants(queryExecutor, materializerLiftableConstantContext, variableNames);

        // The name of a lifted constant is whatever the caller of ILiftableConstantFactory.CreateLiftableConstant passed, so it
        // need not be a valid C# identifier. The parameter itself is renamed rather than just its declaration, because the same
        // name is what the translated executor emits for every reference to that constant.
        var liftedConstantOriginals = new List<Expression>();
        var liftedConstantReplacements = new List<Expression>();
        foreach (var liftedConstant in _liftableConstantProcessor.LiftedConstants)
        {
            var name = LinqToCSharpSyntaxTranslator.SanitizeIdentifierName(liftedConstant.Parameter.Name)!;
            if (name == liftedConstant.Parameter.Name)
            {
                continue;
            }

            var baseName = name;
            for (var j = 0; variableNames.Contains(name); j++)
            {
                name = baseName + j;
            }

            variableNames.Add(name);
            liftedConstantOriginals.Add(liftedConstant.Parameter);
            liftedConstantReplacements.Add(Expression.Parameter(liftedConstant.Parameter.Type, name));
        }

        foreach (var liftedConstant in _liftableConstantProcessor.LiftedConstants)
        {
            var parameter = liftedConstant.Parameter;
            var expression = liftedConstant.Expression;

            if (liftedConstantOriginals.Count > 0)
            {
                var replacer = new ReplacingExpressionVisitor(liftedConstantOriginals, liftedConstantReplacements);
                parameter = (ParameterExpression)replacer.Visit(parameter);
                expression = replacer.Visit(expression);
            }

            var variableValueSyntax = _linqToCSharpTranslator.TranslateExpression(
                expression, _constantReplacements, _memberAccessReplacements, namespaces, unsafeAccessors, variableNames);
            code.AppendLine($"var {parameter.Name} = {variableValueSyntax.NormalizeWhitespace().ToFullString()};");
        }

        if (liftedConstantOriginals.Count > 0)
        {
            queryExecutorAfterLiftingExpression =
                new ReplacingExpressionVisitor(liftedConstantOriginals, liftedConstantReplacements)
                    .Visit(queryExecutorAfterLiftingExpression);
        }

        var queryExecutorSyntaxTree =
            (AnonymousFunctionExpressionSyntax)_linqToCSharpTranslator.TranslateExpression(
                queryExecutorAfterLiftingExpression,
                _constantReplacements,
                _memberAccessReplacements,
                namespaces,
                unsafeAccessors,
                variableNames);

        code
            .AppendLine($"return {queryExecutorSyntaxTree.NormalizeWhitespace().ToFullString()};")
            .DecrementIndent()
            .AppendLine("}")
            .AppendLine()
            .AppendLine($"private static object Query{queryNum}_Executor;");
    }
```

### 🔹 函式: `PrecompiledQueryCodeGenerator.GeneratePrecompiledQueries()`
- **變更前簽章 (Before)**: `PrecompiledQueryCodeGenerator.GeneratePrecompiledQueries(
        Compilation compilation,
        SyntaxGenerator syntaxGenerator,
        DbContext dbContext,
        IReadOnlyDictionary<MemberInfo, QualifiedName> memberAccessReplacements,
        List<QueryPrecompilationError> precompilationErrors,
        ISet<string> generatedFileNames,
        Assembly? additionalAssembly = null,
        string? suffix = null,
        CancellationToken cancellationToken = default)` (L69~L127)
- **變更後簽章 (After)**: `PrecompiledQueryCodeGenerator.GeneratePrecompiledQueries(
        Compilation compilation,
        SyntaxGenerator syntaxGenerator,
        DbContext dbContext,
        IReadOnlyDictionary<MemberInfo, QualifiedName> memberAccessReplacements,
        List<QueryPrecompilationError> precompilationErrors,
        ISet<string> generatedFileNames,
        Assembly? additionalAssembly = null,
        string? suffix = null,
        CancellationToken cancellationToken = default)` (L92~L150)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public virtual IReadOnlyList<ScaffoldedFile> GeneratePrecompiledQueries(
        Compilation compilation,
        SyntaxGenerator syntaxGenerator,
        DbContext dbContext,
        IReadOnlyDictionary<MemberInfo, QualifiedName> memberAccessReplacements,
        List<QueryPrecompilationError> precompilationErrors,
        ISet<string> generatedFileNames,
        Assembly? additionalAssembly = null,
        string? suffix = null,
        CancellationToken cancellationToken = default)
    {
        _queryLocator.Initialize(compilation);
        _symbols = Symbols.Load(compilation);
        _g = syntaxGenerator;
        _linqToCSharpTranslator = new RuntimeModelLinqToCSharpSyntaxTranslator(_g, compilation.UseUpdatedMemorySafetyRules());
        _memberAccessReplacements = memberAccessReplacements;
        _liftableConstantProcessor = new LiftableConstantProcessor(null!);
        _constantReplacements.Clear();
        _runtimeConstants.Clear();
        _runtimeConstantProcessor = new RuntimeConstantProcessor();
        _queryCompiler = dbContext.GetService<IQueryCompiler>();
        _unsafeAccessors.Clear();
        var contextType = dbContext.GetType();
        _funcletizer = new ExpressionTreeFuncletizer(
            dbContext.Model,
            dbContext.GetService<IEvaluatableExpressionFilter>(),
            contextType,
            generateContextAccessors: false,
            dbContext.GetService<IDiagnosticsLogger<DbLoggerCategory.Query>>());

        // This must be done after we complete generating the final compilation above
        _csharpToLinqTranslator.Load(compilation, dbContext, additionalAssembly);

        // TODO: Ignore our auto-generated code! Also compiled model, generated code (comment, filename...?).
        var generatedFiles = new List<ScaffoldedFile>();
        foreach (var syntaxTree in compilation.SyntaxTrees)
        {
            if (_queryLocator.LocateQueries(syntaxTree, precompilationErrors, cancellationToken) is not { Count: > 0 } locatedQueries)
            {
                continue;
            }

            var semanticModel = compilation.GetSemanticModel(syntaxTree);
            var generatedFile = ProcessSyntaxTree(
                syntaxTree,
                semanticModel,
                locatedQueries,
                precompilationErrors,
                "." + contextType.ShortDisplayName() + (suffix ?? ".g"),
                generatedFileNames,
                cancellationToken);
            if (generatedFile is not null)
            {
                generatedFiles.Add(generatedFile);
            }
        }

        return generatedFiles;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public virtual IReadOnlyList<ScaffoldedFile> GeneratePrecompiledQueries(
        Compilation compilation,
        SyntaxGenerator syntaxGenerator,
        DbContext dbContext,
        IReadOnlyDictionary<MemberInfo, QualifiedName> memberAccessReplacements,
        List<QueryPrecompilationError> precompilationErrors,
        ISet<string> generatedFileNames,
        Assembly? additionalAssembly = null,
        string? suffix = null,
        CancellationToken cancellationToken = default)
    {
        _queryLocator.Initialize(compilation);
        _symbols = Symbols.Load(compilation);
        _g = syntaxGenerator;
        _linqToCSharpTranslator = new RuntimeModelLinqToCSharpSyntaxTranslator(_g, compilation.UseUpdatedMemorySafetyRules());
        _memberAccessReplacements = memberAccessReplacements;
        _liftableConstantProcessor = new LiftableConstantProcessor(null!);
        _constantReplacements.Clear();
        _runtimeConstants.Clear();
        _runtimeConstantsByInitializer.Clear();
        _queryCompiler = dbContext.GetService<IQueryCompiler>();
        _unsafeAccessors.Clear();
        var contextType = dbContext.GetType();
        _funcletizer = new ExpressionTreeFuncletizer(
            dbContext.Model,
            dbContext.GetService<IEvaluatableExpressionFilter>(),
            contextType,
            generateContextAccessors: false,
            dbContext.GetService<IDiagnosticsLogger<DbLoggerCategory.Query>>());

        // This must be done after we complete generating the final compilation above
        _csharpToLinqTranslator.Load(compilation, dbContext, additionalAssembly);

        // TODO: Ignore our auto-generated code! Also compiled model, generated code (comment, filename...?).
        var generatedFiles = new List<ScaffoldedFile>();
        foreach (var syntaxTree in compilation.SyntaxTrees)
        {
            if (_queryLocator.LocateQueries(syntaxTree, precompilationErrors, cancellationToken) is not { Count: > 0 } locatedQueries)
            {
                continue;
            }

            var semanticModel = compilation.GetSemanticModel(syntaxTree);
            var generatedFile = ProcessSyntaxTree(
                syntaxTree,
                semanticModel,
                locatedQueries,
                precompilationErrors,
                "." + contextType.ShortDisplayName() + (suffix ?? ".g"),
                generatedFileNames,
                cancellationToken);
            if (generatedFile is not null)
            {
                generatedFiles.Add(generatedFile);
            }
        }

        return generatedFiles;
    }
```

### 🔹 函式: `state_25()`
- **變更前簽章 (Before)**: `[Module State] state_25` (L25~L25)
- **變更後簽章 (After)**: `[Module State] state_25` (L25~L25)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private readonly QueryLocator _queryLocator;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private readonly CSharpToLinqTranslator _csharpToLinqTranslator;
```

### 🔹 函式: `PrecompiledQueryCodeGenerator.ProcessSyntaxTree()`
- **變更前簽章 (Before)**: `PrecompiledQueryCodeGenerator.ProcessSyntaxTree(
        SyntaxTree syntaxTree,
        SemanticModel semanticModel,
        IReadOnlyList<InvocationExpressionSyntax> locatedQueries,
        List<QueryPrecompilationError> precompilationErrors,
        string suffix,
        ISet<string> generatedFileNames,
        CancellationToken cancellationToken)` (L135~L338)
- **變更後簽章 (After)**: `PrecompiledQueryCodeGenerator.ProcessSyntaxTree(
        SyntaxTree syntaxTree,
        SemanticModel semanticModel,
        IReadOnlyList<InvocationExpressionSyntax> locatedQueries,
        List<QueryPrecompilationError> precompilationErrors,
        string suffix,
        ISet<string> generatedFileNames,
        CancellationToken cancellationToken)` (L158~L397)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected virtual ScaffoldedFile? ProcessSyntaxTree(
        SyntaxTree syntaxTree,
        SemanticModel semanticModel,
        IReadOnlyList<InvocationExpressionSyntax> locatedQueries,
        List<QueryPrecompilationError> precompilationErrors,
        string suffix,
        ISet<string> generatedFileNames,
        CancellationToken cancellationToken)
    {
        var queriesPrecompiledInFile = 0;
        _namespaces.Clear();
        _code.Clear();
        _code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            .AppendLine()
            .Append("namespace ").AppendLine(InterceptorsNamespace)
            .AppendLine("{")
            .IncrementIndent()
            .AppendLine("file static class EntityFrameworkCoreInterceptors")
            .AppendLine("{")
            .IncrementIndent();

        for (var queryNum = 0; queryNum < locatedQueries.Count; queryNum++)
        {
            var querySyntax = locatedQueries[queryNum];

            try
            {
                // We have a query lambda, as a Roslyn syntax tree. Translate to LINQ expression tree.
                // TODO: Add verification that this is an EF query over our user's context. If translation returns null the moment
                // there's another query root (another context or another LINQ provider), that's fine.
                if (_csharpToLinqTranslator.Translate(querySyntax, semanticModel) is not MethodCallExpression terminatingOperator)
                {
                    throw new UnreachableException("Non-method call encountered as the root of a LINQ query");
                }

                // We have a LINQ representation of the query tree as it appears in the user's source code, but this isn't the same as the
                // LINQ tree the EF query pipeline needs to get; the latter is the result of evaluating the queryable operators in the user's
                // source code. For example, in the user's code the root is a DbSet as the root, but the expression tree we require needs to
                // contain an EntityQueryRootExpression. To get the LINQ tree for EF, we need to evaluate the operator chain, building an
                // expression tree as usual.

                // However, we cannot evaluate the last operator, since that would execute the query instead of returning an expression tree.
                // So we need to chop off the last operator before evaluation, and then (optionally) recompose it back afterwards.
                // For ToList(), we don't actually recompose it (since ToList() isn't a node in the expression tree), and for async operators,
                // we need to rewrite them to their sync counterparts (since that's what gets injected into the query tree).
                var penultimateOperator = terminatingOperator switch
                {
                    // This is needed e.g. for GetEnumerator(), DbSet.AsAsyncEnumerable (non-static terminating operators)
                    { Object: { } @object } => @object,
                    { Arguments: [var sourceArgument, ..] } => sourceArgument,
                    _ => throw new UnreachableException()
                };

                penultimateOperator = Expression.Lambda<Func<IQueryable>>(penultimateOperator)
                    .Compile(preferInterpretation: true)().Expression;

                // Pass the query through EF's query pipeline; this returns the query's executor function, which can produce an enumerable
                // that invokes the query.
                // Note that we cannot recompose the terminating operator on top of the evaluated penultimate, since method signatures
                // may not allow that (e.g. DbSet.AsAsyncEnumerable() requires a DbSet, but the evaluated value for a DbSet is
                // EntityQueryRootExpression. So we handle the penultimate and the terminating separately.
                var queryExecutor = CompileQuery(penultimateOperator, terminatingOperator);

                // The query has been compiled successfully by the EF query pipeline.
                // Now go over each LINQ operator, generating an interceptor for it.
                _code.AppendLine($"#region Query{queryNum + 1}").AppendLine();

                try
                {
                    _funcletizer.ResetPathCalculation();

                    if (querySyntax is not { Expression: MemberAccessExpressionSyntax { Expression: var penultimateOperatorSyntax } })
                    {
                        throw new UnreachableException();
                    }

                    // Generate interceptors for all LINQ operators in the query, starting from the root up until the penultimate.
                    // Then generate the interceptor for the terminating operator, and finally the query's executor.
                    GenerateOperatorInterceptorsRecursively(
                        _code, penultimateOperator, penultimateOperatorSyntax, semanticModel, queryNum + 1, out var operatorNum,
                        cancellationToken: cancellationToken);

                    GenerateOperatorInterceptor(
                        _code, terminatingOperator, querySyntax, semanticModel, queryNum + 1, operatorNum + 1, isTerminatingOperator: true,
                        cancellationToken);

                    GenerateQueryExecutor(_code, queryNum + 1, queryExecutor, _namespaces, _unsafeAccessors);
                }
                finally
                {
                    _code
                        .AppendLine()
                        .AppendLine($"#endregion Query{queryNum + 1}");
                }
            }
            catch (Exception e)
            {
                precompilationErrors.Add(new QueryPrecompilationError(querySyntax, e));
                continue;
            }

            // We're done generating the interceptors for the query's LINQ operators.

            queriesPrecompiledInFile++;
        }

        if (queriesPrecompiledInFile == 0)
        {
            return null;
        }

        // Output all the unsafe accessors that were generated for all intercepted shapers, e.g.:
        // [UnsafeAccessor(UnsafeAccessorKind.Field, Name = "<Name>k__BackingField")]
        // static extern ref int GetSet_Foo_Name(Foo f);
        if (_unsafeAccessors.Count > 0)
        {
            _code.AppendLine("#region Unsafe accessors");
            foreach (var unsafeAccessor in _unsafeAccessors)
            {
                _code.AppendLine(unsafeAccessor.NormalizeWhitespace().ToFullString());
            }

            _code.AppendLine("#endregion Unsafe accessors");
        }

        foreach (var (fieldName, constant) in _runtimeConstants.OrderBy(x => x.Key))
        {
            var typeSymbol = GetTypeSymbol(semanticModel.Compilation, constant.Type);

            var syntax = _linqToCSharpTranslator.TranslateExpression(
                constant.InitializeExpression, constantReplacements: null, _namespaces, _unsafeAccessors);
            _code.AppendLine(
                $"private static readonly {typeSymbol.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat)} {fieldName} = {syntax.NormalizeWhitespace().ToFullString()};");
        }

        _code
            .DecrementIndent().AppendLine("}")
            .DecrementIndent().AppendLine("}");

        var mainCode = _code.ToString();

        _code.Clear();
        _code.AppendLine("// <auto-generated />").AppendLine();

        // In addition to the namespaces auto-detected by LinqToCSharpTranslator, we manually add these namespaces which are required
        // by manually generated code above.
        _namespaces.UnionWith(
        [
            "System",
            "System.Collections.Concurrent",
            "System.Collections.Generic",
            "System.Linq",
            "System.Linq.Expressions",
            "System.Runtime.CompilerServices",
            "System.Reflection",
            "System.Threading.Tasks",
            "Microsoft.EntityFrameworkCore",
            "Microsoft.EntityFrameworkCore.ChangeTracking.Internal",
            "Microsoft.EntityFrameworkCore.Diagnostics",
            "Microsoft.EntityFrameworkCore.Infrastructure",
            "Microsoft.EntityFrameworkCore.Infrastructure.Internal",
            "Microsoft.EntityFrameworkCore.Internal",
            "Microsoft.EntityFrameworkCore.Metadata",
            "Microsoft.EntityFrameworkCore.Query",
            "Microsoft.EntityFrameworkCore.Query.Internal",
            "Microsoft.EntityFrameworkCore.Storage"
        ]);

        foreach (var ns in _namespaces
                     .OrderBy(ns => ns switch
                     {
                         _ when ns.StartsWith("System.", StringComparison.Ordinal) => 10,
                         _ when ns.StartsWith("Microsoft.", StringComparison.Ordinal) => 9,
                         _ => 0
                     })
                     .ThenBy(ns => ns))
        {
            _code.Append("using ").Append(ns).AppendLine(";");
        }

        _code.AppendLine(mainCode);

        _code.AppendLine(
            """
namespace System.Runtime.CompilerServices
{
    [AttributeUsage(AttributeTargets.Method, AllowMultiple = true)]
    file sealed class InterceptsLocationAttribute : Attribute
    {
        public InterceptsLocationAttribute(int version, string data) { }
    }
}
"""
        );

        var name = Uniquifier.Uniquify(
            Path.GetFileNameWithoutExtension(syntaxTree.FilePath),
            generatedFileNames,
            CompiledModelScaffolder.MaxFileNameLength,
            ".EFInterceptors" + suffix + Path.GetExtension(syntaxTree.FilePath));
        return new ScaffoldedFile(name, _code.ToString());
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected virtual ScaffoldedFile? ProcessSyntaxTree(
        SyntaxTree syntaxTree,
        SemanticModel semanticModel,
        IReadOnlyList<InvocationExpressionSyntax> locatedQueries,
        List<QueryPrecompilationError> precompilationErrors,
        string suffix,
        ISet<string> generatedFileNames,
        CancellationToken cancellationToken)
    {
        var queriesPrecompiledInFile = 0;
        _namespaces.Clear();
        _code.Clear();
        _code
            .AppendLine()
            .AppendLine("#pragma warning disable EF9100 // Precompiled query is experimental")
            .AppendLine()
            .Append("namespace ").AppendLine(InterceptorsNamespace)
            .AppendLine("{")
            .IncrementIndent()
            .AppendLine("file static class EntityFrameworkCoreInterceptors")
            .AppendLine("{")
            .IncrementIndent();

        for (var queryNum = 0; queryNum < locatedQueries.Count; queryNum++)
        {
            var querySyntax = locatedQueries[queryNum];

            // A query that fails must leave nothing of itself behind: its interceptors reference an executor that will never be
            // generated, and the executor method itself may be half-written, so the file would not compile for the queries that
            // did succeed. Its code is therefore generated into a builder of its own and added to the file only once the query has
            // succeeded, and the runtime constants it declares are recorded so that exactly those can be taken back.
            var queryCode = new IndentedStringBuilder();
            for (var i = 0; i < _code.IndentCount; i++)
            {
                queryCode.IncrementIndent();
            }

            _runtimeConstantsOfCurrentQuery.Clear();

            try
            {
                // We have a query lambda, as a Roslyn syntax tree. Translate to LINQ expression tree.
                // TODO: Add verification that this is an EF query over our user's context. If translation returns null the moment
                // there's another query root (another context or another LINQ provider), that's fine.
                if (_csharpToLinqTranslator.Translate(querySyntax, semanticModel) is not MethodCallExpression terminatingOperator)
                {
                    throw new UnreachableException("Non-method call encountered as the root of a LINQ query");
                }

                // We have a LINQ representation of the query tree as it appears in the user's source code, but this isn't the same as the
                // LINQ tree the EF query pipeline needs to get; the latter is the result of evaluating the queryable operators in the user's
                // source code. For example, in the user's code the root is a DbSet as the root, but the expression tree we require needs to
                // contain an EntityQueryRootExpression. To get the LINQ tree for EF, we need to evaluate the operator chain, building an
                // expression tree as usual.

                // However, we cannot evaluate the last operator, since that would execute the query instead of returning an expression tree.
                // So we need to chop off the last operator before evaluation, and then (optionally) recompose it back afterwards.
                // For ToList(), we don't actually recompose it (since ToList() isn't a node in the expression tree), and for async operators,
                // we need to rewrite them to their sync counterparts (since that's what gets injected into the query tree).
                var penultimateOperator = terminatingOperator switch
                {
                    // This is needed e.g. for GetEnumerator(), DbSet.AsAsyncEnumerable (non-static terminating operators)
                    { Object: { } @object } => @object,
                    { Arguments: [var sourceArgument, ..] } => sourceArgument,
                    _ => throw new UnreachableException()
                };

                penultimateOperator = Expression.Lambda<Func<IQueryable>>(penultimateOperator)
                    .Compile(preferInterpretation: true)().Expression;

                // Pass the query through EF's query pipeline; this returns the query's executor function, which can produce an enumerable
                // that invokes the query.
                // Note that we cannot recompose the terminating operator on top of the evaluated penultimate, since method signatures
                // may not allow that (e.g. DbSet.AsAsyncEnumerable() requires a DbSet, but the evaluated value for a DbSet is
                // EntityQueryRootExpression. So we handle the penultimate and the terminating separately.
                var queryExecutor = CompileQuery(penultimateOperator, terminatingOperator);

                // The query has been compiled successfully by the EF query pipeline.
                // Now go over each LINQ operator, generating an interceptor for it.
                queryCode.AppendLine($"#region Query{queryNum + 1}").AppendLine();

                try
                {
                    _funcletizer.ResetPathCalculation();

                    if (querySyntax is not { Expression: MemberAccessExpressionSyntax { Expression: var penultimateOperatorSyntax } })
                    {
                        throw new UnreachableException();
                    }

                    // Generate interceptors for all LINQ operators in the query, starting from the root up until the penultimate.
                    // Then generate the interceptor for the terminating operator, and finally the query's executor.
                    GenerateOperatorInterceptorsRecursively(
                        queryCode, penultimateOperator, penultimateOperatorSyntax, semanticModel, queryNum + 1, out var operatorNum,
                        cancellationToken: cancellationToken);

                    GenerateOperatorInterceptor(
                        queryCode, terminatingOperator, querySyntax, semanticModel, queryNum + 1, operatorNum + 1,
                        isTerminatingOperator: true, cancellationToken);

                    GenerateQueryExecutor(queryCode, queryNum + 1, queryExecutor, _namespaces, _unsafeAccessors);
                }
                finally
                {
                    queryCode
                        .AppendLine()
                        .AppendLine($"#endregion Query{queryNum + 1}");
                }
            }
            catch (Exception e)
            {
                precompilationErrors.Add(new QueryPrecompilationError(querySyntax, e));

                foreach (var constantName in _runtimeConstantsOfCurrentQuery)
                {
                    var constant = _runtimeConstants[constantName];
                    _runtimeConstants.Remove(constantName);
                    _constantReplacements.Remove(constant.Value);
                    if (_runtimeConstantsByInitializer.TryGetValue(constant.InitializeExpression, out var declared)
                        && ReferenceEquals(declared, constant))
                    {
                        _runtimeConstantsByInitializer.Remove(constant.InitializeExpression);
                    }
                }

                continue;
            }

            // We're done generating the interceptors for the query's LINQ operators. The query's code already carries the file's
            // indentation, so it is added as it is, and the trailing line break is re-added through the builder to keep its own
            // indentation state right for what follows.
            using (_code.SuspendIndent())
            {
                _code.Append(queryCode.ToString().TrimEnd('\r', '\n'));
            }

            _code.AppendLine();

            queriesPrecompiledInFile++;
        }

        if (queriesPrecompiledInFile == 0)
        {
            return null;
        }

        // Output all the unsafe accessors that were generated for all intercepted shapers, e.g.:
        // [UnsafeAccessor(UnsafeAccessorKind.Field, Name = "<Name>k__BackingField")]
        // static extern ref int GetSet_Foo_Name(Foo f);
        if (_unsafeAccessors.Count > 0)
        {
            _code.AppendLine("#region Unsafe accessors");
            foreach (var unsafeAccessor in _unsafeAccessors)
            {
                _code.AppendLine(unsafeAccessor.NormalizeWhitespace().ToFullString());
            }

            _code.AppendLine("#endregion Unsafe accessors");
        }

        // The fields are in scope for their own initializers, so a type an initializer refers to by a name one of them has taken
        // has to be written out fully qualified; the translator does that for the names it is told are declared here.
        var runtimeConstantNames = _runtimeConstants.Keys.ToHashSet();
        foreach (var (fieldName, constant) in _runtimeConstants.OrderBy(x => x.Key))
        {
            var typeSymbol = GetTypeSymbol(semanticModel.Compilation, constant.Type);

            var syntax = _linqToCSharpTranslator.TranslateExpression(
                constant.InitializeExpression, constantReplacements: null, _namespaces, _unsafeAccessors, runtimeConstantNames);
            _code.AppendLine(
                $"private static readonly {typeSymbol.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat)} {fieldName} = {syntax.NormalizeWhitespace().ToFullString()};");
        }

        _code
            .DecrementIndent().AppendLine("}")
            .DecrementIndent().AppendLine("}");

        var mainCode = _code.ToString();

        _code.Clear();
        _code.AppendLine("// <auto-generated />").AppendLine();

        // In addition to the namespaces auto-detected by LinqToCSharpTranslator, we manually add these namespaces which are required
        // by manually generated code above.
        _namespaces.UnionWith(
        [
            "System",
            "System.Collections.Concurrent",
            "System.Collections.Generic",
            "System.Linq",
            "System.Linq.Expressions",
            "System.Runtime.CompilerServices",
            "System.Reflection",
            "System.Threading.Tasks",
            "Microsoft.EntityFrameworkCore",
            "Microsoft.EntityFrameworkCore.ChangeTracking.Internal",
            "Microsoft.EntityFrameworkCore.Diagnostics",
            "Microsoft.EntityFrameworkCore.Infrastructure",
            "Microsoft.EntityFrameworkCore.Infrastructure.Internal",
            "Microsoft.EntityFrameworkCore.Internal",
            "Microsoft.EntityFrameworkCore.Metadata",
            "Microsoft.EntityFrameworkCore.Query",
            "Microsoft.EntityFrameworkCore.Query.Internal",
            "Microsoft.EntityFrameworkCore.Storage"
        ]);

        foreach (var ns in _namespaces
                     .OrderBy(ns => ns switch
                     {
                         _ when ns.StartsWith("System.", StringComparison.Ordinal) => 10,
                         _ when ns.StartsWith("Microsoft.", StringComparison.Ordinal) => 9,
                         _ => 0
                     })
                     .ThenBy(ns => ns))
        {
            _code.Append("using ").Append(ns).AppendLine(";");
        }

        _code.AppendLine(mainCode);

        _code.AppendLine(
            """
namespace System.Runtime.CompilerServices
{
    [AttributeUsage(AttributeTargets.Method, AllowMultiple = true)]
    file sealed class InterceptsLocationAttribute : Attribute
    {
        public InterceptsLocationAttribute(int version, string data) { }
    }
}
"""
        );

        var name = Uniquifier.Uniquify(
            Path.GetFileNameWithoutExtension(syntaxTree.FilePath),
            generatedFileNames,
            CompiledModelScaffolder.MaxFileNameLength,
            ".EFInterceptors" + suffix + Path.GetExtension(syntaxTree.FilePath));
        return new ScaffoldedFile(name, _code.ToString());
    }
```


#### 📄 檔案: `src/EFCore.Design/Query/Internal/RuntimeModelLinqToCSharpSyntaxTranslator.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:21, E:27, A:0) ➔ After(N:21, E:27, A:0)
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

### 🔹 函式: `RuntimeModelLinqToCSharpSyntaxTranslator.TranslateStatement()`
- **變更前簽章 (Before)**: `RuntimeModelLinqToCSharpSyntaxTranslator.TranslateStatement(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        IReadOnlyDictionary<MemberInfo, QualifiedName>? memberAccessReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors)` (L53~L64)
- **變更後簽章 (After)**: `RuntimeModelLinqToCSharpSyntaxTranslator.TranslateStatement(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        IReadOnlyDictionary<MemberInfo, QualifiedName>? memberAccessReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors,
        IReadOnlySet<string>? declaredNames = null)` (L53~L70)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public virtual SyntaxNode TranslateStatement(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        IReadOnlyDictionary<MemberInfo, QualifiedName>? memberAccessReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors)
    {
        _memberAccessReplacements = memberAccessReplacements;
        var result = TranslateStatement(node, constantReplacements, collectedNamespaces, unsafeAccessors);
        _memberAccessReplacements = null;
        return result;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public virtual SyntaxNode TranslateStatement(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        IReadOnlyDictionary<MemberInfo, QualifiedName>? memberAccessReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors,
        IReadOnlySet<string>? declaredNames = null)
    {
        _memberAccessReplacements = memberAccessReplacements;
        try
        {
            return TranslateStatement(node, constantReplacements, collectedNamespaces, unsafeAccessors, declaredNames);
        }
        finally
        {
            _memberAccessReplacements = null;
        }
    }
```

### 🔹 函式: `RuntimeModelLinqToCSharpSyntaxTranslator.TranslateExpression()`
- **變更前簽章 (Before)**: `RuntimeModelLinqToCSharpSyntaxTranslator.TranslateExpression(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        IReadOnlyDictionary<MemberInfo, QualifiedName>? memberAccessReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors)` (L72~L83)
- **變更後簽章 (After)**: `RuntimeModelLinqToCSharpSyntaxTranslator.TranslateExpression(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        IReadOnlyDictionary<MemberInfo, QualifiedName>? memberAccessReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors,
        IReadOnlySet<string>? declaredNames = null)` (L78~L95)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public virtual SyntaxNode TranslateExpression(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        IReadOnlyDictionary<MemberInfo, QualifiedName>? memberAccessReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors)
    {
        _memberAccessReplacements = memberAccessReplacements;
        var result = TranslateExpression(node, constantReplacements, collectedNamespaces, unsafeAccessors);
        _memberAccessReplacements = null;
        return result;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public virtual SyntaxNode TranslateExpression(
        Expression node,
        IReadOnlyDictionary<object, string>? constantReplacements,
        IReadOnlyDictionary<MemberInfo, QualifiedName>? memberAccessReplacements,
        ISet<string> collectedNamespaces,
        ISet<MethodDeclarationSyntax> unsafeAccessors,
        IReadOnlySet<string>? declaredNames = null)
    {
        _memberAccessReplacements = memberAccessReplacements;
        try
        {
            return TranslateExpression(node, constantReplacements, collectedNamespaces, unsafeAccessors, declaredNames);
        }
        finally
        {
            _memberAccessReplacements = null;
        }
    }
```


---

### 🔹 Commit #19: `ac7bebae`
- **完整 Hash**: `ac7bebaedfd32316cd5bebd6114ca6f9a24a2107`
- **說明 (Ground Truth)**: Escape LIKE wildcard chars correctly in SQL Server StartsWith(char) (#39076)
- **變更檔案數**: 2

#### 📄 檔案: `src/EFCore.SqlServer/Query/Internal/SqlServerSqlTranslatingExpressionVisitor.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:71, E:96, A:0) ➔ After(N:72, E:97, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 5, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `s.ToString (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `SqlServerSqlTranslatingExpressionVisitor.TranslateStartsEndsWithContains` ──[CALLS]──> `s.ToString (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SqlServerSqlTranslatingExpressionVisitor.TranslateWithoutLike()`
- **變更前簽章 (Before)**: `SqlServerSqlTranslatingExpressionVisitor.TranslateWithoutLike(bool patternIsNonEmptyConstantString = false)` (L624~L687)
- **變更後簽章 (After)**: `SqlServerSqlTranslatingExpressionVisitor.TranslateWithoutLike(bool patternIsNonEmptyConstantString = false, SqlExpression? pattern = null)` (L631~L696)

#### ◀️ 變更前實作碼 (Before Implementation):
```
SqlExpression TranslateWithoutLike(bool patternIsNonEmptyConstantString = false)
            {
                return methodType switch
                {
                    // For StartsWith/EndsWith, use LEFT or RIGHT instead to extract substring and compare:
                    // WHERE instance IS NOT NULL AND pattern IS NOT NULL AND LEFT(instance, LEN(pattern)) = pattern
                    // This is less efficient than LIKE (i.e. StartsWith does an index scan instead of seek), but we have no choice.
                    // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                    // simple equality would yield true in that case, but we want false. We technically
                    StartsEndsWithContains.StartsWith or StartsEndsWithContains.EndsWith
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedPattern),
                                _sqlExpressionFactory.Equal(
                                    _sqlExpressionFactory.Function(
                                        methodType is StartsEndsWithContains.StartsWith ? "LEFT" : "RIGHT",
                                        [
                                            translatedInstance,
                                            _sqlExpressionFactory.Function(
                                                "LEN",
                                                [translatedPattern],
                                                nullable: true,
                                                argumentsPropagateNullability: Statics.TrueArrays[1],
                                                typeof(int))
                                        ],
                                        nullable: true,
                                        argumentsPropagateNullability: Statics.TrueArrays[2],
                                        typeof(string),
                                        stringTypeMapping),
                                    translatedPattern))),

                    // For Contains, just use CHARINDEX and check if the result is greater than 0.
                    StartsEndsWithContains.Contains when patternIsNonEmptyConstantString
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            CharIndexGreaterThanZero()),

                    // For Contains, just use CHARINDEX and check if the result is greater than 0.
                    // Add a check to return null when the pattern is an empty string (and the string isn't null)
                    StartsEndsWithContains.Contains
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedPattern),
                                _sqlExpressionFactory.OrElse(
                                    CharIndexGreaterThanZero(),
                                    _sqlExpressionFactory.Like(
                                        translatedPattern,
                                        _sqlExpressionFactory.Constant(string.Empty, stringTypeMapping))))),

                    _ => throw new UnreachableException()
                };

                SqlExpression CharIndexGreaterThanZero()
                    => _sqlExpressionFactory.GreaterThan(
                        _sqlExpressionFactory.Function(
                            "CHARINDEX",
                            [translatedPattern, translatedInstance],
                            nullable: true,
                            argumentsPropagateNullability: Statics.TrueArrays[2],
                            typeof(int)),
                        _sqlExpressionFactory.Constant(0));
            }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
SqlExpression TranslateWithoutLike(bool patternIsNonEmptyConstantString = false, SqlExpression? pattern = null)
            {
                pattern ??= translatedPattern;

                return methodType switch
                {
                    // For StartsWith/EndsWith, use LEFT or RIGHT instead to extract substring and compare:
                    // WHERE instance IS NOT NULL AND pattern IS NOT NULL AND LEFT(instance, LEN(pattern)) = pattern
                    // This is less efficient than LIKE (i.e. StartsWith does an index scan instead of seek), but we have no choice.
                    // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                    // simple equality would yield true in that case, but we want false. We technically
                    StartsEndsWithContains.StartsWith or StartsEndsWithContains.EndsWith
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(pattern),
                                _sqlExpressionFactory.Equal(
                                    _sqlExpressionFactory.Function(
                                        methodType is StartsEndsWithContains.StartsWith ? "LEFT" : "RIGHT",
                                        [
                                            translatedInstance,
                                            _sqlExpressionFactory.Function(
                                                "LEN",
                                                [pattern],
                                                nullable: true,
                                                argumentsPropagateNullability: Statics.TrueArrays[1],
                                                typeof(int))
                                        ],
                                        nullable: true,
                                        argumentsPropagateNullability: Statics.TrueArrays[2],
                                        typeof(string),
                                        stringTypeMapping),
                                    pattern))),

                    // For Contains, just use CHARINDEX and check if the result is greater than 0.
                    StartsEndsWithContains.Contains when patternIsNonEmptyConstantString
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            CharIndexGreaterThanZero()),

                    // For Contains, just use CHARINDEX and check if the result is greater than 0.
                    // Add a check to return null when the pattern is an empty string (and the string isn't null)
                    StartsEndsWithContains.Contains
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(pattern),
                                _sqlExpressionFactory.OrElse(
                                    CharIndexGreaterThanZero(),
                                    _sqlExpressionFactory.Like(
                                        pattern,
                                        _sqlExpressionFactory.Constant(string.Empty, stringTypeMapping))))),

                    _ => throw new UnreachableException()
                };

                SqlExpression CharIndexGreaterThanZero()
                    => _sqlExpressionFactory.GreaterThan(
                        _sqlExpressionFactory.Function(
                            "CHARINDEX",
                            [pattern, translatedInstance],
                            nullable: true,
                            argumentsPropagateNullability: Statics.TrueArrays[2],
                            typeof(int)),
                        _sqlExpressionFactory.Constant(0));
            }
```

### 🔹 函式: `SqlServerSqlTranslatingExpressionVisitor.CharIndexGreaterThanZero()`
- **變更前簽章 (Before)**: `SqlServerSqlTranslatingExpressionVisitor.CharIndexGreaterThanZero()` (L678~L686)
- **變更後簽章 (After)**: `SqlServerSqlTranslatingExpressionVisitor.CharIndexGreaterThanZero()` (L687~L695)

#### ◀️ 變更前實作碼 (Before Implementation):
```
SqlExpression CharIndexGreaterThanZero()
                    => _sqlExpressionFactory.GreaterThan(
                        _sqlExpressionFactory.Function(
                            "CHARINDEX",
                            [translatedPattern, translatedInstance],
                            nullable: true,
                            argumentsPropagateNullability: Statics.TrueArrays[2],
                            typeof(int)),
                        _sqlExpressionFactory.Constant(0));
```

#### ▶️ 變更後實作碼 (After Implementation):
```
SqlExpression CharIndexGreaterThanZero()
                    => _sqlExpressionFactory.GreaterThan(
                        _sqlExpressionFactory.Function(
                            "CHARINDEX",
                            [pattern, translatedInstance],
                            nullable: true,
                            argumentsPropagateNullability: Statics.TrueArrays[2],
                            typeof(int)),
                        _sqlExpressionFactory.Constant(0));
```

### 🔹 函式: `SqlServerSqlTranslatingExpressionVisitor.VisitMethodCall()`
- **變更前簽章 (Before)**: `SqlServerSqlTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)` (L250~L689)
- **變更後簽章 (After)**: `SqlServerSqlTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)` (L250~L698)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override Expression VisitMethodCall(MethodCallExpression methodCallExpression)
    {
        if (base.VisitMethodCall(methodCallExpression) is var translation
            && translation != QueryCompilationContext.NotTranslatedExpression)
        {
            return translation;
        }

        var method = methodCallExpression.Method;
        var declaringType = method.DeclaringType;
        var @object = methodCallExpression.Object;
        var arguments = methodCallExpression.Arguments;

        switch (method.Name)
        {
            // https://learn.microsoft.com/dotnet/api/system.linq.enumerable.elementat#system-linq-enumerable-elementat-1(system-collections-generic-ienumerable((-0))-system-int32)
            case nameof(Enumerable.ElementAt)
                when declaringType == typeof(Enumerable)
                && @object is null
                && arguments is [Expression source, Expression index]
                && source.Type == typeof(byte[])
                && index.Type == typeof(int):
                return TranslateByteArrayElementAccess(source, index, methodCallExpression.Type);

            // https://learn.microsoft.com/dotnet/api/system.string.startswith#system-string-startswith(system-string)
            // https://learn.microsoft.com/dotnet/api/system.string.startswith#system-string-startswith(system-char)
            // https://learn.microsoft.com/dotnet/api/system.string.endswith#system-string-endswith(system-string)
            // https://learn.microsoft.com/dotnet/api/system.string.endswith#system-string-endswith(system-char)
            // https://learn.microsoft.com/dotnet/api/system.string.contains#system-string-contains(system-string)
            // https://learn.microsoft.com/dotnet/api/system.string.contains#system-string-contains(system-char)
            case nameof(string.StartsWith) or nameof(string.EndsWith) or nameof(string.Contains)
                when declaringType == typeof(string)
                && @object is not null
                && arguments is [Expression value]
                && (value.Type == typeof(string) || value.Type == typeof(char)):
            {
                return TranslateStartsEndsWithContains(
                    @object,
                    value,
                    method.Name switch
                    {
                        nameof(string.StartsWith) => StartsEndsWithContains.StartsWith,
                        nameof(string.EndsWith) => StartsEndsWithContains.EndsWith,
                        nameof(string.Contains) => StartsEndsWithContains.Contains,
                        _ => throw new UnreachableException()
                    });
            }

            // Translate non-aggregate string.Join to CONCAT_WS (for aggregate string.Join, see SqlServerStringAggregateMethodTranslator)
            // https://learn.microsoft.com/dotnet/api/system.string.join#system-string-join(system-string-system-string())
            case nameof(string.Join)
                when declaringType == typeof(string)
                && @object is null
                && arguments is [Expression separator, NewArrayExpression value]
                && separator.Type == typeof(string)
                && value.Type == typeof(string[])
                && _sqlServerSingletonOptions.EngineType switch
                {
                    SqlServerEngineType.SqlServer => _sqlServerSingletonOptions.SqlServerCompatibilityLevel >= 140,
                    SqlServerEngineType.AzureSql => _sqlServerSingletonOptions.AzureSqlCompatibilityLevel >= 140,
                    SqlServerEngineType.AzureSynapse => true,
                    _ => throw new UnreachableException()
                }:
            {
                if (TranslationFailed(separator, Visit(separator), out var translatedSeparator))
                {
                    return QueryCompilationContext.NotTranslatedExpression;
                }

                var translatedArguments = new SqlExpression[value.Expressions.Count + 1];
                translatedArguments[0] = translatedSeparator!;

                var isUnicode = translatedSeparator!.TypeMapping?.IsUnicode == true;

                for (var i = 0; i < value.Expressions.Count; i++)
                {
                    var argument = value.Expressions[i];
                    if (TranslationFailed(argument, Visit(argument), out var sqlArgument))
                    {
                        return QueryCompilationContext.NotTranslatedExpression;
                    }

                    // CONCAT_WS returns a type with a length that varies based on actual inputs (i.e. the sum of all argument lengths, plus
                    // the length needed for the delimiters). We don't know column values (or even parameter values, so we always return max.
                    // We do vary return varchar(max) or nvarchar(max) based on whether we saw any nvarchar mapping.
                    if (sqlArgument!.TypeMapping?.IsUnicode == true)
                    {
                        isUnicode = true;
                    }

                    // CONCAT_WS filters out nulls, but string.Join treats them as empty strings; so coalesce (which is a no-op for non-nullable
                    // arguments).
                    translatedArguments[i + 1] = Dependencies.SqlExpressionFactory.Coalesce(
                        sqlArgument, _sqlExpressionFactory.Constant(string.Empty));
                }

                // CONCAT_WS never returns null; a null delimiter is interpreted as an empty string, and null arguments are skipped
                // (but we coalesce them above in any case).
                return Dependencies.SqlExpressionFactory.Function(
                    "CONCAT_WS",
                    translatedArguments,
                    nullable: false,
                    argumentsPropagateNullability: new bool[translatedArguments.Length],
                    typeof(string),
                    _typeMappingSource.FindMapping(isUnicode ? "nvarchar(max)" : "varchar(max)"));
            }

            // We translate EF.Functions.JsonContains here and not in a method translator since we need to support JsonContains over
            // complex and owned JSON properties, which requires special handling.
            case nameof(SqlServerDbFunctionsExtensions.JsonContains)
                when declaringType == typeof(SqlServerDbFunctionsExtensions)
                && @object is null
                && arguments is [_, var json, var searchValue, var path, var searchMode]:
            {
                if (Translate(searchValue) is not SqlExpression translatedSearchValue)
                {
                    return QueryCompilationContext.NotTranslatedExpression;
                }

                SqlExpression? translatedPath = null;
                if (path is not ConstantExpression { Value: null })
                {
                    if (Translate(path) is not SqlExpression pathExpression)
                    {
                        return QueryCompilationContext.NotTranslatedExpression;
                    }

                    translatedPath = pathExpression;
                }

                SqlExpression? translatedSearchMode = null;
                if (searchMode is not ConstantExpression { Value: null })
                {
                    if (Translate(searchMode) is not SqlExpression searchModeExpression)
                    {
                        return QueryCompilationContext.NotTranslatedExpression;
                    }

                    translatedSearchMode = searchModeExpression;
                }

#pragma warning disable EF1001 // TranslateProjection() is pubternal
                var translatedJson = TranslateProjection(json) switch
                {
                    // The JSON argument is a scalar string property
                    SqlExpression scalar => scalar,

                    // The JSON argument is a complex or owned JSON property
                    RelationalStructuralTypeShaperExpression { ValueBufferExpression: JsonQueryExpression { JsonColumn: var c } } => c,

                    _ => null
                };
#pragma warning restore EF1001

                if (translatedJson is null)
                {
                    return QueryCompilationContext.NotTranslatedExpression;
                }

                List<SqlExpression> functionArguments = [translatedJson, translatedSearchValue];
                List<bool> argumentsPropagateNullability = [true, false];

                if (translatedPath is not null)
                {
                    functionArguments.Add(translatedPath);
                    argumentsPropagateNullability.Add(true);
                }

                if (translatedSearchMode is not null)
                {
                    functionArguments.Add(translatedSearchMode);
                    argumentsPropagateNullability.Add(true);
                }

                return _sqlExpressionFactory.Function(
                    "JSON_CONTAINS",
                    functionArguments,
                    nullable: true,
                    argumentsPropagateNullability: argumentsPropagateNullability,
                    typeof(int));
            }

            // We translate EF.Functions.JsonPathExists here and not in a method translator since we need to support JsonPathExists over
            // complex and owned JSON properties, which requires special handling.
            case nameof(RelationalDbFunctionsExtensions.JsonPathExists)
                when declaringType == typeof(RelationalDbFunctionsExtensions)
                && @object is null
                && arguments is [_, var json, var path]:
            {
                if (Translate(path) is not SqlExpression translatedPath)
                {
                    return QueryCompilationContext.NotTranslatedExpression;
                }

#pragma warning disable EF1001 // TranslateProjection() is pubternal
                var translatedJson = TranslateProjection(json) switch
                {
                    // The JSON argument is a scalar string property
                    SqlExpression scalar => scalar,

                    // The JSON argument is a complex or owned JSON property
                    RelationalStructuralTypeShaperExpression { ValueBufferExpression: JsonQueryExpression { JsonColumn: var c } } => c,

                    _ => null
                };
#pragma warning restore EF1001

                return translatedJson is null
                    ? QueryCompilationContext.NotTranslatedExpression
                    : _sqlExpressionFactory.Equal(
                        _sqlExpressionFactory.Function(
                            "JSON_PATH_EXISTS",
                            [translatedJson, translatedPath],
                            nullable: true,
                            // Note that JSON_PATH_EXISTS() does propagate nullability; however, our query pipeline assumes that if
                            // arguments propagate nullability, that's the *only* reason for the function to return null; this means that
                            // if the arguments are non-nullable, the IS NOT NULL wrapping check can be optimized away.
                            argumentsPropagateNullability: [false, false],
                            typeof(int)),
                        _sqlExpressionFactory.Constant(1));
            }

            // https://learn.microsoft.com/dotnet/api/system.datetimeoffset.tooffset
            case nameof(DateTimeOffset.ToOffset)
                when declaringType == typeof(DateTimeOffset)
                && @object is not null
                && arguments is [{ Type: var argType } offsetArgument]
                && argType == typeof(TimeSpan):
            {
                if (Visit(@object) is not SqlExpression translatedInstance
                    || Visit(offsetArgument) is not SqlExpression translatedOffset)
                {
                    return QueryCompilationContext.NotTranslatedExpression;
                }

                var offsetExpression = TranslateTimeSpanToOffsetExpression(translatedOffset);
                return offsetExpression is null
                    ? QueryCompilationContext.NotTranslatedExpression
                    : _sqlExpressionFactory.Function(
                        "SWITCHOFFSET",
                        [translatedInstance, offsetExpression],
                        nullable: true,
                        argumentsPropagateNullability: Statics.TrueArrays[2],
                        typeof(DateTimeOffset),
                        translatedInstance.TypeMapping);
            }

            default:
                return QueryCompilationContext.NotTranslatedExpression;
        }

        Expression TranslateStartsEndsWithContains(Expression instance, Expression pattern, StartsEndsWithContains methodType)
        {
            if (Visit(instance) is not SqlExpression translatedInstance
                || Visit(pattern) is not SqlExpression translatedPattern)
            {
                return QueryCompilationContext.NotTranslatedExpression;
            }

            var stringTypeMapping = ExpressionExtensions.InferTypeMapping(translatedInstance, translatedPattern);

            translatedInstance = _sqlExpressionFactory.ApplyTypeMapping(translatedInstance, stringTypeMapping);
            translatedPattern = _sqlExpressionFactory.ApplyTypeMapping(translatedPattern, stringTypeMapping);

            switch (translatedPattern)
            {
                case SqlConstantExpression patternConstant:
                {
                    // The pattern is constant. Aside from null and empty string, we escape all special characters (%, _, \) and send a
                    // simple LIKE
                    return patternConstant.Value switch
                    {
                        null => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(null, typeof(string), stringTypeMapping)),

                        // In .NET, all strings start with/end with/contain the empty string, but SQL LIKE return false for empty patterns.
                        // Return % which always matches instead.
                        // Note that we don't just return a true constant, since null strings shouldn't match even an empty string
                        // (but SqlNullabilityProcess will convert this to a true constant if the instance is non-nullable)
                        "" => _sqlExpressionFactory.Like(translatedInstance, _sqlExpressionFactory.Constant("%")),

                        string s when !s.Any(IsLikeWildChar)
                            => _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(
                                    methodType switch
                                    {
                                        StartsEndsWithContains.StartsWith => s + '%',
                                        StartsEndsWithContains.EndsWith => '%' + s,
                                        StartsEndsWithContains.Contains => $"%{s}%",

                                        _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                    })),

                        // Azure Synapse does not support ESCAPE clause in LIKE
                        // fallback to translation like with column/expression
                        string when _sqlServerSingletonOptions.EngineType is SqlServerEngineType.AzureSynapse
                            => TranslateWithoutLike(patternIsNonEmptyConstantString: true),

                        string s => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(
                                methodType switch
                                {
                                    StartsEndsWithContains.StartsWith => EscapeLikePattern(s) + '%',
                                    StartsEndsWithContains.EndsWith => '%' + EscapeLikePattern(s),
                                    StartsEndsWithContains.Contains => $"%{EscapeLikePattern(s)}%",

                                    _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                }),
                            _sqlExpressionFactory.Constant(LikeEscapeString)),

                        char s when !IsLikeWildChar(s)
                            => _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(
                                    methodType switch
                                    {
                                        StartsEndsWithContains.StartsWith => s + "%",
                                        StartsEndsWithContains.EndsWith => "%" + s,
                                        StartsEndsWithContains.Contains => $"%{s}%",

                                        _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                    })),

                        char s => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(
                                methodType switch
                                {
                                    StartsEndsWithContains.StartsWith => LikeEscapeChar + s + "%",
                                    StartsEndsWithContains.EndsWith => "%" + LikeEscapeChar + s,
                                    StartsEndsWithContains.Contains => $"%{LikeEscapeChar}{s}%",

                                    _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                }),
                            _sqlExpressionFactory.Constant(LikeEscapeString)),

                        _ => throw new UnreachableException()
                    };
                }

                // Azure Synapse does not support ESCAPE clause in LIKE
                // fall through to translation like with column/expression
                case SqlParameterExpression patternParameter
                    when _sqlServerSingletonOptions.EngineType is not SqlServerEngineType.AzureSynapse:
                {
                    // The pattern is a parameter, register a runtime parameter that will contain the rewritten LIKE pattern, where
                    // all special characters have been escaped.
                    var lambda = Expression.Lambda(
                        Expression.Call(
                            EscapeLikePatternParameterMethod,
                            QueryCompilationContext.QueryContextParameter,
                            Expression.Constant(patternParameter.Name),
                            Expression.Constant(methodType)),
                        QueryCompilationContext.QueryContextParameter);

                    var escapedPatternParameter =
                        _queryCompilationContext.RegisterRuntimeParameter(
                            $"{patternParameter.Name}_{methodType.ToString().ToLower(CultureInfo.InvariantCulture)}", lambda);

                    return _sqlExpressionFactory.Like(
                        translatedInstance,
                        new SqlParameterExpression(escapedPatternParameter.Name!, escapedPatternParameter.Type, stringTypeMapping),
                        _sqlExpressionFactory.Constant(LikeEscapeString));
                }

                default:
                    // The pattern is a column or a complex expression; the possible special characters in the pattern cannot be escaped,
                    // preventing us from translating to LIKE.
                    return TranslateWithoutLike();
            }

            SqlExpression TranslateWithoutLike(bool patternIsNonEmptyConstantString = false)
            {
                return methodType switch
                {
                    // For StartsWith/EndsWith, use LEFT or RIGHT instead to extract substring and compare:
                    // WHERE instance IS NOT NULL AND pattern IS NOT NULL AND LEFT(instance, LEN(pattern)) = pattern
                    // This is less efficient than LIKE (i.e. StartsWith does an index scan instead of seek), but we have no choice.
                    // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                    // simple equality would yield true in that case, but we want false. We technically
                    StartsEndsWithContains.StartsWith or StartsEndsWithContains.EndsWith
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedPattern),
                                _sqlExpressionFactory.Equal(
                                    _sqlExpressionFactory.Function(
                                        methodType is StartsEndsWithContains.StartsWith ? "LEFT" : "RIGHT",
                                        [
                                            translatedInstance,
                                            _sqlExpressionFactory.Function(
                                                "LEN",
                                                [translatedPattern],
                                                nullable: true,
                                                argumentsPropagateNullability: Statics.TrueArrays[1],
                                                typeof(int))
                                        ],
                                        nullable: true,
                                        argumentsPropagateNullability: Statics.TrueArrays[2],
                                        typeof(string),
                                        stringTypeMapping),
                                    translatedPattern))),

                    // For Contains, just use CHARINDEX and check if the result is greater than 0.
                    StartsEndsWithContains.Contains when patternIsNonEmptyConstantString
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            CharIndexGreaterThanZero()),

                    // For Contains, just use CHARINDEX and check if the result is greater than 0.
                    // Add a check to return null when the pattern is an empty string (and the string isn't null)
                    StartsEndsWithContains.Contains
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedPattern),
                                _sqlExpressionFactory.OrElse(
                                    CharIndexGreaterThanZero(),
                                    _sqlExpressionFactory.Like(
                                        translatedPattern,
                                        _sqlExpressionFactory.Constant(string.Empty, stringTypeMapping))))),

                    _ => throw new UnreachableException()
                };

                SqlExpression CharIndexGreaterThanZero()
                    => _sqlExpressionFactory.GreaterThan(
                        _sqlExpressionFactory.Function(
                            "CHARINDEX",
                            [translatedPattern, translatedInstance],
                            nullable: true,
                            argumentsPropagateNullability: Statics.TrueArrays[2],
                            typeof(int)),
                        _sqlExpressionFactory.Constant(0));
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override Expression VisitMethodCall(MethodCallExpression methodCallExpression)
    {
        if (base.VisitMethodCall(methodCallExpression) is var translation
            && translation != QueryCompilationContext.NotTranslatedExpression)
        {
            return translation;
        }

        var method = methodCallExpression.Method;
        var declaringType = method.DeclaringType;
        var @object = methodCallExpression.Object;
        var arguments = methodCallExpression.Arguments;

        switch (method.Name)
        {
            // https://learn.microsoft.com/dotnet/api/system.linq.enumerable.elementat#system-linq-enumerable-elementat-1(system-collections-generic-ienumerable((-0))-system-int32)
            case nameof(Enumerable.ElementAt)
                when declaringType == typeof(Enumerable)
                && @object is null
                && arguments is [Expression source, Expression index]
                && source.Type == typeof(byte[])
                && index.Type == typeof(int):
                return TranslateByteArrayElementAccess(source, index, methodCallExpression.Type);

            // https://learn.microsoft.com/dotnet/api/system.string.startswith#system-string-startswith(system-string)
            // https://learn.microsoft.com/dotnet/api/system.string.startswith#system-string-startswith(system-char)
            // https://learn.microsoft.com/dotnet/api/system.string.endswith#system-string-endswith(system-string)
            // https://learn.microsoft.com/dotnet/api/system.string.endswith#system-string-endswith(system-char)
            // https://learn.microsoft.com/dotnet/api/system.string.contains#system-string-contains(system-string)
            // https://learn.microsoft.com/dotnet/api/system.string.contains#system-string-contains(system-char)
            case nameof(string.StartsWith) or nameof(string.EndsWith) or nameof(string.Contains)
                when declaringType == typeof(string)
                && @object is not null
                && arguments is [Expression value]
                && (value.Type == typeof(string) || value.Type == typeof(char)):
            {
                return TranslateStartsEndsWithContains(
                    @object,
                    value,
                    method.Name switch
                    {
                        nameof(string.StartsWith) => StartsEndsWithContains.StartsWith,
                        nameof(string.EndsWith) => StartsEndsWithContains.EndsWith,
                        nameof(string.Contains) => StartsEndsWithContains.Contains,
                        _ => throw new UnreachableException()
                    });
            }

            // Translate non-aggregate string.Join to CONCAT_WS (for aggregate string.Join, see SqlServerStringAggregateMethodTranslator)
            // https://learn.microsoft.com/dotnet/api/system.string.join#system-string-join(system-string-system-string())
            case nameof(string.Join)
                when declaringType == typeof(string)
                && @object is null
                && arguments is [Expression separator, NewArrayExpression value]
                && separator.Type == typeof(string)
                && value.Type == typeof(string[])
                && _sqlServerSingletonOptions.EngineType switch
                {
                    SqlServerEngineType.SqlServer => _sqlServerSingletonOptions.SqlServerCompatibilityLevel >= 140,
                    SqlServerEngineType.AzureSql => _sqlServerSingletonOptions.AzureSqlCompatibilityLevel >= 140,
                    SqlServerEngineType.AzureSynapse => true,
                    _ => throw new UnreachableException()
                }:
            {
                if (TranslationFailed(separator, Visit(separator), out var translatedSeparator))
                {
                    return QueryCompilationContext.NotTranslatedExpression;
                }

                var translatedArguments = new SqlExpression[value.Expressions.Count + 1];
                translatedArguments[0] = translatedSeparator!;

                var isUnicode = translatedSeparator!.TypeMapping?.IsUnicode == true;

                for (var i = 0; i < value.Expressions.Count; i++)
                {
                    var argument = value.Expressions[i];
                    if (TranslationFailed(argument, Visit(argument), out var sqlArgument))
                    {
                        return QueryCompilationContext.NotTranslatedExpression;
                    }

                    // CONCAT_WS returns a type with a length that varies based on actual inputs (i.e. the sum of all argument lengths, plus
                    // the length needed for the delimiters). We don't know column values (or even parameter values, so we always return max.
                    // We do vary return varchar(max) or nvarchar(max) based on whether we saw any nvarchar mapping.
                    if (sqlArgument!.TypeMapping?.IsUnicode == true)
                    {
                        isUnicode = true;
                    }

                    // CONCAT_WS filters out nulls, but string.Join treats them as empty strings; so coalesce (which is a no-op for non-nullable
                    // arguments).
                    translatedArguments[i + 1] = Dependencies.SqlExpressionFactory.Coalesce(
                        sqlArgument, _sqlExpressionFactory.Constant(string.Empty));
                }

                // CONCAT_WS never returns null; a null delimiter is interpreted as an empty string, and null arguments are skipped
                // (but we coalesce them above in any case).
                return Dependencies.SqlExpressionFactory.Function(
                    "CONCAT_WS",
                    translatedArguments,
                    nullable: false,
                    argumentsPropagateNullability: new bool[translatedArguments.Length],
                    typeof(string),
                    _typeMappingSource.FindMapping(isUnicode ? "nvarchar(max)" : "varchar(max)"));
            }

            // We translate EF.Functions.JsonContains here and not in a method translator since we need to support JsonContains over
            // complex and owned JSON properties, which requires special handling.
            case nameof(SqlServerDbFunctionsExtensions.JsonContains)
                when declaringType == typeof(SqlServerDbFunctionsExtensions)
                && @object is null
                && arguments is [_, var json, var searchValue, var path, var searchMode]:
            {
                if (Translate(searchValue) is not SqlExpression translatedSearchValue)
                {
                    return QueryCompilationContext.NotTranslatedExpression;
                }

                SqlExpression? translatedPath = null;
                if (path is not ConstantExpression { Value: null })
                {
                    if (Translate(path) is not SqlExpression pathExpression)
                    {
                        return QueryCompilationContext.NotTranslatedExpression;
                    }

                    translatedPath = pathExpression;
                }

                SqlExpression? translatedSearchMode = null;
                if (searchMode is not ConstantExpression { Value: null })
                {
                    if (Translate(searchMode) is not SqlExpression searchModeExpression)
                    {
                        return QueryCompilationContext.NotTranslatedExpression;
                    }

                    translatedSearchMode = searchModeExpression;
                }

#pragma warning disable EF1001 // TranslateProjection() is pubternal
                var translatedJson = TranslateProjection(json) switch
                {
                    // The JSON argument is a scalar string property
                    SqlExpression scalar => scalar,

                    // The JSON argument is a complex or owned JSON property
                    RelationalStructuralTypeShaperExpression { ValueBufferExpression: JsonQueryExpression { JsonColumn: var c } } => c,

                    _ => null
                };
#pragma warning restore EF1001

                if (translatedJson is null)
                {
                    return QueryCompilationContext.NotTranslatedExpression;
                }

                List<SqlExpression> functionArguments = [translatedJson, translatedSearchValue];
                List<bool> argumentsPropagateNullability = [true, false];

                if (translatedPath is not null)
                {
                    functionArguments.Add(translatedPath);
                    argumentsPropagateNullability.Add(true);
                }

                if (translatedSearchMode is not null)
                {
                    functionArguments.Add(translatedSearchMode);
                    argumentsPropagateNullability.Add(true);
                }

                return _sqlExpressionFactory.Function(
                    "JSON_CONTAINS",
                    functionArguments,
                    nullable: true,
                    argumentsPropagateNullability: argumentsPropagateNullability,
                    typeof(int));
            }

            // We translate EF.Functions.JsonPathExists here and not in a method translator since we need to support JsonPathExists over
            // complex and owned JSON properties, which requires special handling.
            case nameof(RelationalDbFunctionsExtensions.JsonPathExists)
                when declaringType == typeof(RelationalDbFunctionsExtensions)
                && @object is null
                && arguments is [_, var json, var path]:
            {
                if (Translate(path) is not SqlExpression translatedPath)
                {
                    return QueryCompilationContext.NotTranslatedExpression;
                }

#pragma warning disable EF1001 // TranslateProjection() is pubternal
                var translatedJson = TranslateProjection(json) switch
                {
                    // The JSON argument is a scalar string property
                    SqlExpression scalar => scalar,

                    // The JSON argument is a complex or owned JSON property
                    RelationalStructuralTypeShaperExpression { ValueBufferExpression: JsonQueryExpression { JsonColumn: var c } } => c,

                    _ => null
                };
#pragma warning restore EF1001

                return translatedJson is null
                    ? QueryCompilationContext.NotTranslatedExpression
                    : _sqlExpressionFactory.Equal(
                        _sqlExpressionFactory.Function(
                            "JSON_PATH_EXISTS",
                            [translatedJson, translatedPath],
                            nullable: true,
                            // Note that JSON_PATH_EXISTS() does propagate nullability; however, our query pipeline assumes that if
                            // arguments propagate nullability, that's the *only* reason for the function to return null; this means that
                            // if the arguments are non-nullable, the IS NOT NULL wrapping check can be optimized away.
                            argumentsPropagateNullability: [false, false],
                            typeof(int)),
                        _sqlExpressionFactory.Constant(1));
            }

            // https://learn.microsoft.com/dotnet/api/system.datetimeoffset.tooffset
            case nameof(DateTimeOffset.ToOffset)
                when declaringType == typeof(DateTimeOffset)
                && @object is not null
                && arguments is [{ Type: var argType } offsetArgument]
                && argType == typeof(TimeSpan):
            {
                if (Visit(@object) is not SqlExpression translatedInstance
                    || Visit(offsetArgument) is not SqlExpression translatedOffset)
                {
                    return QueryCompilationContext.NotTranslatedExpression;
                }

                var offsetExpression = TranslateTimeSpanToOffsetExpression(translatedOffset);
                return offsetExpression is null
                    ? QueryCompilationContext.NotTranslatedExpression
                    : _sqlExpressionFactory.Function(
                        "SWITCHOFFSET",
                        [translatedInstance, offsetExpression],
                        nullable: true,
                        argumentsPropagateNullability: Statics.TrueArrays[2],
                        typeof(DateTimeOffset),
                        translatedInstance.TypeMapping);
            }

            default:
                return QueryCompilationContext.NotTranslatedExpression;
        }

        Expression TranslateStartsEndsWithContains(Expression instance, Expression pattern, StartsEndsWithContains methodType)
        {
            if (Visit(instance) is not SqlExpression translatedInstance
                || Visit(pattern) is not SqlExpression translatedPattern)
            {
                return QueryCompilationContext.NotTranslatedExpression;
            }

            var stringTypeMapping = ExpressionExtensions.InferTypeMapping(translatedInstance, translatedPattern);

            translatedInstance = _sqlExpressionFactory.ApplyTypeMapping(translatedInstance, stringTypeMapping);
            translatedPattern = _sqlExpressionFactory.ApplyTypeMapping(translatedPattern, stringTypeMapping);

            switch (translatedPattern)
            {
                case SqlConstantExpression patternConstant:
                {
                    // The pattern is constant. Aside from null and empty string, we escape all special characters (%, _, \) and send a
                    // simple LIKE
                    return patternConstant.Value switch
                    {
                        null => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(null, typeof(string), stringTypeMapping)),

                        // In .NET, all strings start with/end with/contain the empty string, but SQL LIKE return false for empty patterns.
                        // Return % which always matches instead.
                        // Note that we don't just return a true constant, since null strings shouldn't match even an empty string
                        // (but SqlNullabilityProcess will convert this to a true constant if the instance is non-nullable)
                        "" => _sqlExpressionFactory.Like(translatedInstance, _sqlExpressionFactory.Constant("%")),

                        string s when !s.Any(IsLikeWildChar)
                            => _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(
                                    methodType switch
                                    {
                                        StartsEndsWithContains.StartsWith => $"{s}%",
                                        StartsEndsWithContains.EndsWith => $"%{s}",
                                        StartsEndsWithContains.Contains => $"%{s}%",

                                        _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                    })),

                        // Azure Synapse does not support ESCAPE clause in LIKE
                        // fallback to translation like with column/expression
                        string when _sqlServerSingletonOptions.EngineType is SqlServerEngineType.AzureSynapse
                            => TranslateWithoutLike(patternIsNonEmptyConstantString: true),

                        string s => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(
                                methodType switch
                                {
                                    StartsEndsWithContains.StartsWith => $"{EscapeLikePattern(s)}%",
                                    StartsEndsWithContains.EndsWith => $"%{EscapeLikePattern(s)}",
                                    StartsEndsWithContains.Contains => $"%{EscapeLikePattern(s)}%",

                                    _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                }),
                            _sqlExpressionFactory.Constant(LikeEscapeString)),

                        char s when !IsLikeWildChar(s)
                            => _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(
                                    methodType switch
                                    {
                                        StartsEndsWithContains.StartsWith => $"{s}%",
                                        StartsEndsWithContains.EndsWith => $"%{s}",
                                        StartsEndsWithContains.Contains => $"%{s}%",

                                        _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                    })),

                        // Azure Synapse does not support ESCAPE clause in LIKE
                        // fallback to translation like with column/expression
                        char s when _sqlServerSingletonOptions.EngineType is SqlServerEngineType.AzureSynapse
                            => TranslateWithoutLike(
                                patternIsNonEmptyConstantString: true,
                                pattern: _sqlExpressionFactory.Constant(s.ToString(), stringTypeMapping)),

                        char s => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(
                                methodType switch
                                {
                                    StartsEndsWithContains.StartsWith => $"{LikeEscapeChar}{s}%",
                                    StartsEndsWithContains.EndsWith => $"%{LikeEscapeChar}{s}",
                                    StartsEndsWithContains.Contains => $"%{LikeEscapeChar}{s}%",

                                    _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                }),
                            _sqlExpressionFactory.Constant(LikeEscapeString)),

                        _ => throw new UnreachableException()
                    };
                }

                // Azure Synapse does not support ESCAPE clause in LIKE
                // fall through to translation like with column/expression
                case SqlParameterExpression patternParameter
                    when _sqlServerSingletonOptions.EngineType is not SqlServerEngineType.AzureSynapse:
                {
                    // The pattern is a parameter, register a runtime parameter that will contain the rewritten LIKE pattern, where
                    // all special characters have been escaped.
                    var lambda = Expression.Lambda(
                        Expression.Call(
                            EscapeLikePatternParameterMethod,
                            QueryCompilationContext.QueryContextParameter,
                            Expression.Constant(patternParameter.Name),
                            Expression.Constant(methodType)),
                        QueryCompilationContext.QueryContextParameter);

                    var escapedPatternParameter =
                        _queryCompilationContext.RegisterRuntimeParameter(
                            $"{patternParameter.Name}_{methodType.ToString().ToLower(CultureInfo.InvariantCulture)}", lambda);

                    return _sqlExpressionFactory.Like(
                        translatedInstance,
                        new SqlParameterExpression(escapedPatternParameter.Name!, escapedPatternParameter.Type, stringTypeMapping),
                        _sqlExpressionFactory.Constant(LikeEscapeString));
                }

                default:
                    // The pattern is a column or a complex expression; the possible special characters in the pattern cannot be escaped,
                    // preventing us from translating to LIKE.
                    return TranslateWithoutLike();
            }

            SqlExpression TranslateWithoutLike(bool patternIsNonEmptyConstantString = false, SqlExpression? pattern = null)
            {
                pattern ??= translatedPattern;

                return methodType switch
                {
                    // For StartsWith/EndsWith, use LEFT or RIGHT instead to extract substring and compare:
                    // WHERE instance IS NOT NULL AND pattern IS NOT NULL AND LEFT(instance, LEN(pattern)) = pattern
                    // This is less efficient than LIKE (i.e. StartsWith does an index scan instead of seek), but we have no choice.
                    // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                    // simple equality would yield true in that case, but we want false. We technically
                    StartsEndsWithContains.StartsWith or StartsEndsWithContains.EndsWith
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(pattern),
                                _sqlExpressionFactory.Equal(
                                    _sqlExpressionFactory.Function(
                                        methodType is StartsEndsWithContains.StartsWith ? "LEFT" : "RIGHT",
                                        [
                                            translatedInstance,
                                            _sqlExpressionFactory.Function(
                                                "LEN",
                                                [pattern],
                                                nullable: true,
                                                argumentsPropagateNullability: Statics.TrueArrays[1],
                                                typeof(int))
                                        ],
                                        nullable: true,
                                        argumentsPropagateNullability: Statics.TrueArrays[2],
                                        typeof(string),
                                        stringTypeMapping),
                                    pattern))),

                    // For Contains, just use CHARINDEX and check if the result is greater than 0.
                    StartsEndsWithContains.Contains when patternIsNonEmptyConstantString
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            CharIndexGreaterThanZero()),

                    // For Contains, just use CHARINDEX and check if the result is greater than 0.
                    // Add a check to return null when the pattern is an empty string (and the string isn't null)
                    StartsEndsWithContains.Contains
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(pattern),
                                _sqlExpressionFactory.OrElse(
                                    CharIndexGreaterThanZero(),
                                    _sqlExpressionFactory.Like(
                                        pattern,
                                        _sqlExpressionFactory.Constant(string.Empty, stringTypeMapping))))),

                    _ => throw new UnreachableException()
                };

                SqlExpression CharIndexGreaterThanZero()
                    => _sqlExpressionFactory.GreaterThan(
                        _sqlExpressionFactory.Function(
                            "CHARINDEX",
                            [pattern, translatedInstance],
                            nullable: true,
                            argumentsPropagateNullability: Statics.TrueArrays[2],
                            typeof(int)),
                        _sqlExpressionFactory.Constant(0));
            }
        }
    }
```

### 🔹 函式: `SqlServerSqlTranslatingExpressionVisitor.TranslateStartsEndsWithContains()`
- **變更前簽章 (Before)**: `SqlServerSqlTranslatingExpressionVisitor.TranslateStartsEndsWithContains(Expression instance, Expression pattern, StartsEndsWithContains methodType)` (L501~L688)
- **變更後簽章 (After)**: `SqlServerSqlTranslatingExpressionVisitor.TranslateStartsEndsWithContains(Expression instance, Expression pattern, StartsEndsWithContains methodType)` (L501~L697)

#### ◀️ 變更前實作碼 (Before Implementation):
```
Expression TranslateStartsEndsWithContains(Expression instance, Expression pattern, StartsEndsWithContains methodType)
        {
            if (Visit(instance) is not SqlExpression translatedInstance
                || Visit(pattern) is not SqlExpression translatedPattern)
            {
                return QueryCompilationContext.NotTranslatedExpression;
            }

            var stringTypeMapping = ExpressionExtensions.InferTypeMapping(translatedInstance, translatedPattern);

            translatedInstance = _sqlExpressionFactory.ApplyTypeMapping(translatedInstance, stringTypeMapping);
            translatedPattern = _sqlExpressionFactory.ApplyTypeMapping(translatedPattern, stringTypeMapping);

            switch (translatedPattern)
            {
                case SqlConstantExpression patternConstant:
                {
                    // The pattern is constant. Aside from null and empty string, we escape all special characters (%, _, \) and send a
                    // simple LIKE
                    return patternConstant.Value switch
                    {
                        null => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(null, typeof(string), stringTypeMapping)),

                        // In .NET, all strings start with/end with/contain the empty string, but SQL LIKE return false for empty patterns.
                        // Return % which always matches instead.
                        // Note that we don't just return a true constant, since null strings shouldn't match even an empty string
                        // (but SqlNullabilityProcess will convert this to a true constant if the instance is non-nullable)
                        "" => _sqlExpressionFactory.Like(translatedInstance, _sqlExpressionFactory.Constant("%")),

                        string s when !s.Any(IsLikeWildChar)
                            => _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(
                                    methodType switch
                                    {
                                        StartsEndsWithContains.StartsWith => s + '%',
                                        StartsEndsWithContains.EndsWith => '%' + s,
                                        StartsEndsWithContains.Contains => $"%{s}%",

                                        _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                    })),

                        // Azure Synapse does not support ESCAPE clause in LIKE
                        // fallback to translation like with column/expression
                        string when _sqlServerSingletonOptions.EngineType is SqlServerEngineType.AzureSynapse
                            => TranslateWithoutLike(patternIsNonEmptyConstantString: true),

                        string s => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(
                                methodType switch
                                {
                                    StartsEndsWithContains.StartsWith => EscapeLikePattern(s) + '%',
                                    StartsEndsWithContains.EndsWith => '%' + EscapeLikePattern(s),
                                    StartsEndsWithContains.Contains => $"%{EscapeLikePattern(s)}%",

                                    _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                }),
                            _sqlExpressionFactory.Constant(LikeEscapeString)),

                        char s when !IsLikeWildChar(s)
                            => _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(
                                    methodType switch
                                    {
                                        StartsEndsWithContains.StartsWith => s + "%",
                                        StartsEndsWithContains.EndsWith => "%" + s,
                                        StartsEndsWithContains.Contains => $"%{s}%",

                                        _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                    })),

                        char s => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(
                                methodType switch
                                {
                                    StartsEndsWithContains.StartsWith => LikeEscapeChar + s + "%",
                                    StartsEndsWithContains.EndsWith => "%" + LikeEscapeChar + s,
                                    StartsEndsWithContains.Contains => $"%{LikeEscapeChar}{s}%",

                                    _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                }),
                            _sqlExpressionFactory.Constant(LikeEscapeString)),

                        _ => throw new UnreachableException()
                    };
                }

                // Azure Synapse does not support ESCAPE clause in LIKE
                // fall through to translation like with column/expression
                case SqlParameterExpression patternParameter
                    when _sqlServerSingletonOptions.EngineType is not SqlServerEngineType.AzureSynapse:
                {
                    // The pattern is a parameter, register a runtime parameter that will contain the rewritten LIKE pattern, where
                    // all special characters have been escaped.
                    var lambda = Expression.Lambda(
                        Expression.Call(
                            EscapeLikePatternParameterMethod,
                            QueryCompilationContext.QueryContextParameter,
                            Expression.Constant(patternParameter.Name),
                            Expression.Constant(methodType)),
                        QueryCompilationContext.QueryContextParameter);

                    var escapedPatternParameter =
                        _queryCompilationContext.RegisterRuntimeParameter(
                            $"{patternParameter.Name}_{methodType.ToString().ToLower(CultureInfo.InvariantCulture)}", lambda);

                    return _sqlExpressionFactory.Like(
                        translatedInstance,
                        new SqlParameterExpression(escapedPatternParameter.Name!, escapedPatternParameter.Type, stringTypeMapping),
                        _sqlExpressionFactory.Constant(LikeEscapeString));
                }

                default:
                    // The pattern is a column or a complex expression; the possible special characters in the pattern cannot be escaped,
                    // preventing us from translating to LIKE.
                    return TranslateWithoutLike();
            }

            SqlExpression TranslateWithoutLike(bool patternIsNonEmptyConstantString = false)
            {
                return methodType switch
                {
                    // For StartsWith/EndsWith, use LEFT or RIGHT instead to extract substring and compare:
                    // WHERE instance IS NOT NULL AND pattern IS NOT NULL AND LEFT(instance, LEN(pattern)) = pattern
                    // This is less efficient than LIKE (i.e. StartsWith does an index scan instead of seek), but we have no choice.
                    // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                    // simple equality would yield true in that case, but we want false. We technically
                    StartsEndsWithContains.StartsWith or StartsEndsWithContains.EndsWith
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedPattern),
                                _sqlExpressionFactory.Equal(
                                    _sqlExpressionFactory.Function(
                                        methodType is StartsEndsWithContains.StartsWith ? "LEFT" : "RIGHT",
                                        [
                                            translatedInstance,
                                            _sqlExpressionFactory.Function(
                                                "LEN",
                                                [translatedPattern],
                                                nullable: true,
                                                argumentsPropagateNullability: Statics.TrueArrays[1],
                                                typeof(int))
                                        ],
                                        nullable: true,
                                        argumentsPropagateNullability: Statics.TrueArrays[2],
                                        typeof(string),
                                        stringTypeMapping),
                                    translatedPattern))),

                    // For Contains, just use CHARINDEX and check if the result is greater than 0.
                    StartsEndsWithContains.Contains when patternIsNonEmptyConstantString
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            CharIndexGreaterThanZero()),

                    // For Contains, just use CHARINDEX and check if the result is greater than 0.
                    // Add a check to return null when the pattern is an empty string (and the string isn't null)
                    StartsEndsWithContains.Contains
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedPattern),
                                _sqlExpressionFactory.OrElse(
                                    CharIndexGreaterThanZero(),
                                    _sqlExpressionFactory.Like(
                                        translatedPattern,
                                        _sqlExpressionFactory.Constant(string.Empty, stringTypeMapping))))),

                    _ => throw new UnreachableException()
                };

                SqlExpression CharIndexGreaterThanZero()
                    => _sqlExpressionFactory.GreaterThan(
                        _sqlExpressionFactory.Function(
                            "CHARINDEX",
                            [translatedPattern, translatedInstance],
                            nullable: true,
                            argumentsPropagateNullability: Statics.TrueArrays[2],
                            typeof(int)),
                        _sqlExpressionFactory.Constant(0));
            }
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
Expression TranslateStartsEndsWithContains(Expression instance, Expression pattern, StartsEndsWithContains methodType)
        {
            if (Visit(instance) is not SqlExpression translatedInstance
                || Visit(pattern) is not SqlExpression translatedPattern)
            {
                return QueryCompilationContext.NotTranslatedExpression;
            }

            var stringTypeMapping = ExpressionExtensions.InferTypeMapping(translatedInstance, translatedPattern);

            translatedInstance = _sqlExpressionFactory.ApplyTypeMapping(translatedInstance, stringTypeMapping);
            translatedPattern = _sqlExpressionFactory.ApplyTypeMapping(translatedPattern, stringTypeMapping);

            switch (translatedPattern)
            {
                case SqlConstantExpression patternConstant:
                {
                    // The pattern is constant. Aside from null and empty string, we escape all special characters (%, _, \) and send a
                    // simple LIKE
                    return patternConstant.Value switch
                    {
                        null => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(null, typeof(string), stringTypeMapping)),

                        // In .NET, all strings start with/end with/contain the empty string, but SQL LIKE return false for empty patterns.
                        // Return % which always matches instead.
                        // Note that we don't just return a true constant, since null strings shouldn't match even an empty string
                        // (but SqlNullabilityProcess will convert this to a true constant if the instance is non-nullable)
                        "" => _sqlExpressionFactory.Like(translatedInstance, _sqlExpressionFactory.Constant("%")),

                        string s when !s.Any(IsLikeWildChar)
                            => _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(
                                    methodType switch
                                    {
                                        StartsEndsWithContains.StartsWith => $"{s}%",
                                        StartsEndsWithContains.EndsWith => $"%{s}",
                                        StartsEndsWithContains.Contains => $"%{s}%",

                                        _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                    })),

                        // Azure Synapse does not support ESCAPE clause in LIKE
                        // fallback to translation like with column/expression
                        string when _sqlServerSingletonOptions.EngineType is SqlServerEngineType.AzureSynapse
                            => TranslateWithoutLike(patternIsNonEmptyConstantString: true),

                        string s => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(
                                methodType switch
                                {
                                    StartsEndsWithContains.StartsWith => $"{EscapeLikePattern(s)}%",
                                    StartsEndsWithContains.EndsWith => $"%{EscapeLikePattern(s)}",
                                    StartsEndsWithContains.Contains => $"%{EscapeLikePattern(s)}%",

                                    _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                }),
                            _sqlExpressionFactory.Constant(LikeEscapeString)),

                        char s when !IsLikeWildChar(s)
                            => _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(
                                    methodType switch
                                    {
                                        StartsEndsWithContains.StartsWith => $"{s}%",
                                        StartsEndsWithContains.EndsWith => $"%{s}",
                                        StartsEndsWithContains.Contains => $"%{s}%",

                                        _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                    })),

                        // Azure Synapse does not support ESCAPE clause in LIKE
                        // fallback to translation like with column/expression
                        char s when _sqlServerSingletonOptions.EngineType is SqlServerEngineType.AzureSynapse
                            => TranslateWithoutLike(
                                patternIsNonEmptyConstantString: true,
                                pattern: _sqlExpressionFactory.Constant(s.ToString(), stringTypeMapping)),

                        char s => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(
                                methodType switch
                                {
                                    StartsEndsWithContains.StartsWith => $"{LikeEscapeChar}{s}%",
                                    StartsEndsWithContains.EndsWith => $"%{LikeEscapeChar}{s}",
                                    StartsEndsWithContains.Contains => $"%{LikeEscapeChar}{s}%",

                                    _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
                                }),
                            _sqlExpressionFactory.Constant(LikeEscapeString)),

                        _ => throw new UnreachableException()
                    };
                }

                // Azure Synapse does not support ESCAPE clause in LIKE
                // fall through to translation like with column/expression
                case SqlParameterExpression patternParameter
                    when _sqlServerSingletonOptions.EngineType is not SqlServerEngineType.AzureSynapse:
                {
                    // The pattern is a parameter, register a runtime parameter that will contain the rewritten LIKE pattern, where
                    // all special characters have been escaped.
                    var lambda = Expression.Lambda(
                        Expression.Call(
                            EscapeLikePatternParameterMethod,
                            QueryCompilationContext.QueryContextParameter,
                            Expression.Constant(patternParameter.Name),
                            Expression.Constant(methodType)),
                        QueryCompilationContext.QueryContextParameter);

                    var escapedPatternParameter =
                        _queryCompilationContext.RegisterRuntimeParameter(
                            $"{patternParameter.Name}_{methodType.ToString().ToLower(CultureInfo.InvariantCulture)}", lambda);

                    return _sqlExpressionFactory.Like(
                        translatedInstance,
                        new SqlParameterExpression(escapedPatternParameter.Name!, escapedPatternParameter.Type, stringTypeMapping),
                        _sqlExpressionFactory.Constant(LikeEscapeString));
                }

                default:
                    // The pattern is a column or a complex expression; the possible special characters in the pattern cannot be escaped,
                    // preventing us from translating to LIKE.
                    return TranslateWithoutLike();
            }

            SqlExpression TranslateWithoutLike(bool patternIsNonEmptyConstantString = false, SqlExpression? pattern = null)
            {
                pattern ??= translatedPattern;

                return methodType switch
                {
                    // For StartsWith/EndsWith, use LEFT or RIGHT instead to extract substring and compare:
                    // WHERE instance IS NOT NULL AND pattern IS NOT NULL AND LEFT(instance, LEN(pattern)) = pattern
                    // This is less efficient than LIKE (i.e. StartsWith does an index scan instead of seek), but we have no choice.
                    // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                    // simple equality would yield true in that case, but we want false. We technically
                    StartsEndsWithContains.StartsWith or StartsEndsWithContains.EndsWith
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(pattern),
                                _sqlExpressionFactory.Equal(
                                    _sqlExpressionFactory.Function(
                                        methodType is StartsEndsWithContains.StartsWith ? "LEFT" : "RIGHT",
                                        [
                                            translatedInstance,
                                            _sqlExpressionFactory.Function(
                                                "LEN",
                                                [pattern],
                                                nullable: true,
                                                argumentsPropagateNullability: Statics.TrueArrays[1],
                                                typeof(int))
                                        ],
                                        nullable: true,
                                        argumentsPropagateNullability: Statics.TrueArrays[2],
                                        typeof(string),
                                        stringTypeMapping),
                                    pattern))),

                    // For Contains, just use CHARINDEX and check if the result is greater than 0.
                    StartsEndsWithContains.Contains when patternIsNonEmptyConstantString
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            CharIndexGreaterThanZero()),

                    // For Contains, just use CHARINDEX and check if the result is greater than 0.
                    // Add a check to return null when the pattern is an empty string (and the string isn't null)
                    StartsEndsWithContains.Contains
                        => _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(pattern),
                                _sqlExpressionFactory.OrElse(
                                    CharIndexGreaterThanZero(),
                                    _sqlExpressionFactory.Like(
                                        pattern,
                                        _sqlExpressionFactory.Constant(string.Empty, stringTypeMapping))))),

                    _ => throw new UnreachableException()
                };

                SqlExpression CharIndexGreaterThanZero()
                    => _sqlExpressionFactory.GreaterThan(
                        _sqlExpressionFactory.Function(
                            "CHARINDEX",
                            [pattern, translatedInstance],
                            nullable: true,
                            argumentsPropagateNullability: Statics.TrueArrays[2],
                            typeof(int)),
                        _sqlExpressionFactory.Constant(0));
            }
        }
```

### 🔹 函式: `SqlServerSqlTranslatingExpressionVisitor.ConstructLikePatternParameter()`
- **變更前簽章 (Before)**: `SqlServerSqlTranslatingExpressionVisitor.ConstructLikePatternParameter(
        QueryContext queryContext,
        string baseParameterName,
        StartsEndsWithContains methodType)` (L734~L772)
- **變更後簽章 (After)**: `SqlServerSqlTranslatingExpressionVisitor.ConstructLikePatternParameter(
        QueryContext queryContext,
        string baseParameterName,
        StartsEndsWithContains methodType)` (L743~L781)

#### ◀️ 變更前實作碼 (Before Implementation):
```
[EntityFrameworkInternal]
    public static string? ConstructLikePatternParameter(
        QueryContext queryContext,
        string baseParameterName,
        StartsEndsWithContains methodType)
        => queryContext.Parameters[baseParameterName] switch
        {
            null => null,

            // In .NET, all strings start/end with the empty string, but SQL LIKE return false for empty patterns.
            // Return % which always matches instead.
            "" => "%",

            string s => methodType switch
            {
                StartsEndsWithContains.StartsWith => EscapeLikePattern(s) + '%',
                StartsEndsWithContains.EndsWith => '%' + EscapeLikePattern(s),
                StartsEndsWithContains.Contains => $"%{EscapeLikePattern(s)}%",
                _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
            },

            char s when !IsLikeWildChar(s) => methodType switch
            {
                StartsEndsWithContains.StartsWith => s + "%",
                StartsEndsWithContains.EndsWith => "%" + s,
                StartsEndsWithContains.Contains => $"%{s}%",
                _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
            },

            char s => methodType switch
            {
                StartsEndsWithContains.StartsWith => LikeEscapeChar + s + "%",
                StartsEndsWithContains.EndsWith => "%" + LikeEscapeChar + s,
                StartsEndsWithContains.Contains => $"%{LikeEscapeChar}{s}%",
                _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
            },

            _ => throw new UnreachableException()
        };
```

#### ▶️ 變更後實作碼 (After Implementation):
```
[EntityFrameworkInternal]
    public static string? ConstructLikePatternParameter(
        QueryContext queryContext,
        string baseParameterName,
        StartsEndsWithContains methodType)
        => queryContext.Parameters[baseParameterName] switch
        {
            null => null,

            // In .NET, all strings start/end with the empty string, but SQL LIKE return false for empty patterns.
            // Return % which always matches instead.
            "" => "%",

            string s => methodType switch
            {
                StartsEndsWithContains.StartsWith => $"{EscapeLikePattern(s)}%",
                StartsEndsWithContains.EndsWith => $"%{EscapeLikePattern(s)}",
                StartsEndsWithContains.Contains => $"%{EscapeLikePattern(s)}%",
                _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
            },

            char s when !IsLikeWildChar(s) => methodType switch
            {
                StartsEndsWithContains.StartsWith => $"{s}%",
                StartsEndsWithContains.EndsWith => $"%{s}",
                StartsEndsWithContains.Contains => $"%{s}%",
                _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
            },

            char s => methodType switch
            {
                StartsEndsWithContains.StartsWith => $"{LikeEscapeChar}{s}%",
                StartsEndsWithContains.EndsWith => $"%{LikeEscapeChar}{s}",
                StartsEndsWithContains.Contains => $"%{LikeEscapeChar}{s}%",
                _ => throw new ArgumentOutOfRangeException(nameof(methodType), methodType, null)
            },

            _ => throw new UnreachableException()
        };
```


#### 📄 檔案: `src/EFCore.Sqlite.Core/Query/Internal/SqliteSqlTranslatingExpressionVisitor.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:63, E:71, A:0) ➔ After(N:63, E:71, A:0)
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

### 🔹 函式: `SqliteSqlTranslatingExpressionVisitor.TranslateStartsEndsWith()`
- **變更前簽章 (Before)**: `SqliteSqlTranslatingExpressionVisitor.TranslateStartsEndsWith(Expression instance, Expression pattern, bool startsWith)` (L274~L417)
- **變更後簽章 (After)**: `SqliteSqlTranslatingExpressionVisitor.TranslateStartsEndsWith(Expression instance, Expression pattern, bool startsWith)` (L274~L417)

#### ◀️ 變更前實作碼 (Before Implementation):
```
Expression TranslateStartsEndsWith(Expression instance, Expression pattern, bool startsWith)
        {
            if (Visit(instance) is not SqlExpression translatedInstance
                || Visit(pattern) is not SqlExpression translatedPattern)
            {
                return QueryCompilationContext.NotTranslatedExpression;
            }

            var stringTypeMapping = ExpressionExtensions.InferTypeMapping(translatedInstance, translatedPattern);

            translatedInstance = _sqlExpressionFactory.ApplyTypeMapping(translatedInstance, stringTypeMapping);
            translatedPattern = _sqlExpressionFactory.ApplyTypeMapping(translatedPattern, stringTypeMapping);

            switch (translatedPattern)
            {
                case SqlConstantExpression patternConstant:
                {
                    // The pattern is constant. Aside from null and empty string, we escape all special characters (%, _, \) and send a
                    // simple LIKE
                    return patternConstant.Value switch
                    {
                        null => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(null, typeof(string), stringTypeMapping)),

                        // In .NET, all strings start with/end with/contain the empty string, but SQL LIKE return false for empty patterns.
                        // Return % which always matches instead.
                        // Note that we don't just return a true constant, since null strings shouldn't match even an empty string
                        // (but SqlNullabilityProcess will convert this to a true constant if the instance is non-nullable)
                        "" => _sqlExpressionFactory.Like(translatedInstance, _sqlExpressionFactory.Constant("%")),

                        string s => s.Any(IsLikeWildChar)
                            ? _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? EscapeLikePattern(s) + '%' : '%' + EscapeLikePattern(s)),
                                _sqlExpressionFactory.Constant(LikeEscapeString))
                            : _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? s + '%' : '%' + s)),

                        char s => IsLikeWildChar(s)
                            ? _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? LikeEscapeString + s + "%" : '%' + LikeEscapeString + s),
                                _sqlExpressionFactory.Constant(LikeEscapeString))
                            : _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? s + "%" : "%" + s)),

                        _ => throw new UnreachableException()
                    };
                }

                case SqlParameterExpression patternParameter:
                {
                    // The pattern is a parameter, register a runtime parameter that will contain the rewritten LIKE pattern, where
                    // all special characters have been escaped.
                    var lambda = Expression.Lambda(
                        Expression.Call(
                            EscapeLikePatternParameterMethod,
                            QueryCompilationContext.QueryContextParameter,
                            Expression.Constant(patternParameter.Name),
                            Expression.Constant(startsWith)),
                        QueryCompilationContext.QueryContextParameter);

                    var escapedPatternParameter =
                        _queryCompilationContext.RegisterRuntimeParameter(
                            $"{patternParameter.Name}_{(startsWith ? "startswith" : "endswith")}", lambda);

                    return _sqlExpressionFactory.Like(
                        translatedInstance,
                        new SqlParameterExpression(escapedPatternParameter.Name!, escapedPatternParameter.Type, stringTypeMapping),
                        _sqlExpressionFactory.Constant(LikeEscapeString));
                }

                default:
                    // The pattern is a column or a complex expression; the possible special characters in the pattern cannot be escaped,
                    // preventing us from translating to LIKE.
                    if (startsWith)
                    {
                        // Generate: WHERE instance IS NOT NULL AND pattern IS NOT NULL AND (substr(instance, 1, length(pattern)) = pattern OR pattern = '')
                        // Note that the empty string pattern needs special handling, since in .NET it returns true for all non-null
                        // instances, but substr(instance, 0) returns the entire string in SQLite.
                        // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                        // simple equality would yield true in that case, but we want false. We technically
                        return
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedInstance),
                                _sqlExpressionFactory.AndAlso(
                                    _sqlExpressionFactory.IsNotNull(translatedPattern),
                                    _sqlExpressionFactory.OrElse(
                                        _sqlExpressionFactory.Equal(
                                            _sqlExpressionFactory.Function(
                                                "substr",
                                                [
                                                    translatedInstance,
                                                    _sqlExpressionFactory.Constant(1),
                                                    _sqlExpressionFactory.Function(
                                                        "length",
                                                        [translatedPattern],
                                                        nullable: true,
                                                        argumentsPropagateNullability: Statics.TrueArrays[1],
                                                        typeof(int))
                                                ],
                                                nullable: true,
                                                argumentsPropagateNullability: [true, false, false],
                                                typeof(string),
                                                stringTypeMapping),
                                            translatedPattern),
                                        _sqlExpressionFactory.Equal(translatedPattern, _sqlExpressionFactory.Constant(string.Empty)))));
                    }

                    // Generate: WHERE instance IS NOT NULL AND pattern IS NOT NULL AND (substr(instance, -length(pattern)) = pattern OR pattern = '')
                    // Note that the empty string pattern needs special handling, since in .NET it returns true for all non-null
                    // instances, but substr(instance, 0) returns the entire string in SQLite.
                    // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                    // simple equality would yield true in that case, but we want false. We technically
                    return
                        _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedPattern),
                                _sqlExpressionFactory.OrElse(
                                    _sqlExpressionFactory.Equal(
                                        _sqlExpressionFactory.Function(
                                            "substr",
                                            [
                                                translatedInstance,
                                                _sqlExpressionFactory.Negate(
                                                    _sqlExpressionFactory.Function(
                                                        "length",
                                                        [translatedPattern],
                                                        nullable: true,
                                                        argumentsPropagateNullability: Statics.TrueArrays[1],
                                                        typeof(int)))
                                            ],
                                            nullable: true,
                                            argumentsPropagateNullability: Statics.TrueArrays[2],
                                            typeof(string),
                                            stringTypeMapping),
                                        translatedPattern),
                                    _sqlExpressionFactory.Equal(translatedPattern, _sqlExpressionFactory.Constant(string.Empty)))));
            }
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
Expression TranslateStartsEndsWith(Expression instance, Expression pattern, bool startsWith)
        {
            if (Visit(instance) is not SqlExpression translatedInstance
                || Visit(pattern) is not SqlExpression translatedPattern)
            {
                return QueryCompilationContext.NotTranslatedExpression;
            }

            var stringTypeMapping = ExpressionExtensions.InferTypeMapping(translatedInstance, translatedPattern);

            translatedInstance = _sqlExpressionFactory.ApplyTypeMapping(translatedInstance, stringTypeMapping);
            translatedPattern = _sqlExpressionFactory.ApplyTypeMapping(translatedPattern, stringTypeMapping);

            switch (translatedPattern)
            {
                case SqlConstantExpression patternConstant:
                {
                    // The pattern is constant. Aside from null and empty string, we escape all special characters (%, _, \) and send a
                    // simple LIKE
                    return patternConstant.Value switch
                    {
                        null => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(null, typeof(string), stringTypeMapping)),

                        // In .NET, all strings start with/end with/contain the empty string, but SQL LIKE return false for empty patterns.
                        // Return % which always matches instead.
                        // Note that we don't just return a true constant, since null strings shouldn't match even an empty string
                        // (but SqlNullabilityProcess will convert this to a true constant if the instance is non-nullable)
                        "" => _sqlExpressionFactory.Like(translatedInstance, _sqlExpressionFactory.Constant("%")),

                        string s => s.Any(IsLikeWildChar)
                            ? _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? $"{EscapeLikePattern(s)}%" : $"%{EscapeLikePattern(s)}"),
                                _sqlExpressionFactory.Constant(LikeEscapeString))
                            : _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? $"{s}%" : $"%{s}")),

                        char s => IsLikeWildChar(s)
                            ? _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? $"{LikeEscapeChar}{s}%" : $"%{LikeEscapeChar}{s}"),
                                _sqlExpressionFactory.Constant(LikeEscapeString))
                            : _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? $"{s}%" : $"%{s}")),

                        _ => throw new UnreachableException()
                    };
                }

                case SqlParameterExpression patternParameter:
                {
                    // The pattern is a parameter, register a runtime parameter that will contain the rewritten LIKE pattern, where
                    // all special characters have been escaped.
                    var lambda = Expression.Lambda(
                        Expression.Call(
                            EscapeLikePatternParameterMethod,
                            QueryCompilationContext.QueryContextParameter,
                            Expression.Constant(patternParameter.Name),
                            Expression.Constant(startsWith)),
                        QueryCompilationContext.QueryContextParameter);

                    var escapedPatternParameter =
                        _queryCompilationContext.RegisterRuntimeParameter(
                            $"{patternParameter.Name}_{(startsWith ? "startswith" : "endswith")}", lambda);

                    return _sqlExpressionFactory.Like(
                        translatedInstance,
                        new SqlParameterExpression(escapedPatternParameter.Name!, escapedPatternParameter.Type, stringTypeMapping),
                        _sqlExpressionFactory.Constant(LikeEscapeString));
                }

                default:
                    // The pattern is a column or a complex expression; the possible special characters in the pattern cannot be escaped,
                    // preventing us from translating to LIKE.
                    if (startsWith)
                    {
                        // Generate: WHERE instance IS NOT NULL AND pattern IS NOT NULL AND (substr(instance, 1, length(pattern)) = pattern OR pattern = '')
                        // Note that the empty string pattern needs special handling, since in .NET it returns true for all non-null
                        // instances, but substr(instance, 0) returns the entire string in SQLite.
                        // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                        // simple equality would yield true in that case, but we want false. We technically
                        return
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedInstance),
                                _sqlExpressionFactory.AndAlso(
                                    _sqlExpressionFactory.IsNotNull(translatedPattern),
                                    _sqlExpressionFactory.OrElse(
                                        _sqlExpressionFactory.Equal(
                                            _sqlExpressionFactory.Function(
                                                "substr",
                                                [
                                                    translatedInstance,
                                                    _sqlExpressionFactory.Constant(1),
                                                    _sqlExpressionFactory.Function(
                                                        "length",
                                                        [translatedPattern],
                                                        nullable: true,
                                                        argumentsPropagateNullability: Statics.TrueArrays[1],
                                                        typeof(int))
                                                ],
                                                nullable: true,
                                                argumentsPropagateNullability: [true, false, false],
                                                typeof(string),
                                                stringTypeMapping),
                                            translatedPattern),
                                        _sqlExpressionFactory.Equal(translatedPattern, _sqlExpressionFactory.Constant(string.Empty)))));
                    }

                    // Generate: WHERE instance IS NOT NULL AND pattern IS NOT NULL AND (substr(instance, -length(pattern)) = pattern OR pattern = '')
                    // Note that the empty string pattern needs special handling, since in .NET it returns true for all non-null
                    // instances, but substr(instance, 0) returns the entire string in SQLite.
                    // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                    // simple equality would yield true in that case, but we want false. We technically
                    return
                        _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedPattern),
                                _sqlExpressionFactory.OrElse(
                                    _sqlExpressionFactory.Equal(
                                        _sqlExpressionFactory.Function(
                                            "substr",
                                            [
                                                translatedInstance,
                                                _sqlExpressionFactory.Negate(
                                                    _sqlExpressionFactory.Function(
                                                        "length",
                                                        [translatedPattern],
                                                        nullable: true,
                                                        argumentsPropagateNullability: Statics.TrueArrays[1],
                                                        typeof(int)))
                                            ],
                                            nullable: true,
                                            argumentsPropagateNullability: Statics.TrueArrays[2],
                                            typeof(string),
                                            stringTypeMapping),
                                        translatedPattern),
                                    _sqlExpressionFactory.Equal(translatedPattern, _sqlExpressionFactory.Constant(string.Empty)))));
            }
        }
```

### 🔹 函式: `SqliteSqlTranslatingExpressionVisitor.VisitMethodCall()`
- **變更前簽章 (Before)**: `SqliteSqlTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)` (L202~L418)
- **變更後簽章 (After)**: `SqliteSqlTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)` (L202~L418)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override Expression VisitMethodCall(MethodCallExpression methodCallExpression)
    {
        if (base.VisitMethodCall(methodCallExpression) is var translation
            && translation != QueryCompilationContext.NotTranslatedExpression)
        {
            return translation;
        }

        var method = methodCallExpression.Method;
        var declaringType = method.DeclaringType;
        var @object = methodCallExpression.Object;
        var arguments = methodCallExpression.Arguments;

        switch (method.Name)
        {
            // https://learn.microsoft.com/dotnet/api/system.string.startswith#system-string-startswith(system-string)
            // https://learn.microsoft.com/dotnet/api/system.string.startswith#system-string-startswith(system-char)
            // https://learn.microsoft.com/dotnet/api/system.string.endswith#system-string-endswith(system-string)
            // https://learn.microsoft.com/dotnet/api/system.string.endswith#system-string-endswith(system-char)
            case nameof(string.StartsWith) or nameof(string.EndsWith)
                when methodCallExpression.Object is not null
                && declaringType == typeof(string)
                && arguments is [Expression value]
                && (value.Type == typeof(string) || value.Type == typeof(char)):
            {
                return TranslateStartsEndsWith(
                    methodCallExpression.Object,
                    value,
                    method.Name is nameof(string.StartsWith));
            }

            // We translate EF.Functions.JsonPathExists here and not in a method translator since we need to support JsonPathExists over
            // complex and owned JSON properties, which requires special handling.
            case nameof(RelationalDbFunctionsExtensions.JsonPathExists)
                when declaringType == typeof(RelationalDbFunctionsExtensions)
                && @object is null
                && arguments is [_, var json, var path]:
            {
                if (Translate(path) is not SqlExpression translatedPath)
                {
                    return QueryCompilationContext.NotTranslatedExpression;
                }

#pragma warning disable EF1001 // TranslateProjection() is pubternal
                var translatedJson = TranslateProjection(json) switch
                {
                    // The JSON argument is a scalar string property
                    SqlExpression scalar => scalar,

                    // The JSON argument is a complex or owned JSON property
                    RelationalStructuralTypeShaperExpression { ValueBufferExpression: JsonQueryExpression { JsonColumn: var c } } => c,
                    _ => null
                };
#pragma warning restore EF1001

                return translatedJson is null
                    ? QueryCompilationContext.NotTranslatedExpression
                    : _sqlExpressionFactory.IsNotNull(
                        _sqlExpressionFactory.Function(
                            "json_type",
                            [translatedJson, translatedPath],
                            nullable: true,
                            // Note that json_type() does propagate nullability; however, our query pipeline assumes that if arguments
                            // propagate nullability, that's the *only* reason for the function to return null; this means that if the
                            // arguments are non-nullable, the IS NOT NULL wrapping check can be optimized away.
                            argumentsPropagateNullability: [false, false],
                            typeof(int)));
            }
        }

        return QueryCompilationContext.NotTranslatedExpression;

        Expression TranslateStartsEndsWith(Expression instance, Expression pattern, bool startsWith)
        {
            if (Visit(instance) is not SqlExpression translatedInstance
                || Visit(pattern) is not SqlExpression translatedPattern)
            {
                return QueryCompilationContext.NotTranslatedExpression;
            }

            var stringTypeMapping = ExpressionExtensions.InferTypeMapping(translatedInstance, translatedPattern);

            translatedInstance = _sqlExpressionFactory.ApplyTypeMapping(translatedInstance, stringTypeMapping);
            translatedPattern = _sqlExpressionFactory.ApplyTypeMapping(translatedPattern, stringTypeMapping);

            switch (translatedPattern)
            {
                case SqlConstantExpression patternConstant:
                {
                    // The pattern is constant. Aside from null and empty string, we escape all special characters (%, _, \) and send a
                    // simple LIKE
                    return patternConstant.Value switch
                    {
                        null => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(null, typeof(string), stringTypeMapping)),

                        // In .NET, all strings start with/end with/contain the empty string, but SQL LIKE return false for empty patterns.
                        // Return % which always matches instead.
                        // Note that we don't just return a true constant, since null strings shouldn't match even an empty string
                        // (but SqlNullabilityProcess will convert this to a true constant if the instance is non-nullable)
                        "" => _sqlExpressionFactory.Like(translatedInstance, _sqlExpressionFactory.Constant("%")),

                        string s => s.Any(IsLikeWildChar)
                            ? _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? EscapeLikePattern(s) + '%' : '%' + EscapeLikePattern(s)),
                                _sqlExpressionFactory.Constant(LikeEscapeString))
                            : _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? s + '%' : '%' + s)),

                        char s => IsLikeWildChar(s)
                            ? _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? LikeEscapeString + s + "%" : '%' + LikeEscapeString + s),
                                _sqlExpressionFactory.Constant(LikeEscapeString))
                            : _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? s + "%" : "%" + s)),

                        _ => throw new UnreachableException()
                    };
                }

                case SqlParameterExpression patternParameter:
                {
                    // The pattern is a parameter, register a runtime parameter that will contain the rewritten LIKE pattern, where
                    // all special characters have been escaped.
                    var lambda = Expression.Lambda(
                        Expression.Call(
                            EscapeLikePatternParameterMethod,
                            QueryCompilationContext.QueryContextParameter,
                            Expression.Constant(patternParameter.Name),
                            Expression.Constant(startsWith)),
                        QueryCompilationContext.QueryContextParameter);

                    var escapedPatternParameter =
                        _queryCompilationContext.RegisterRuntimeParameter(
                            $"{patternParameter.Name}_{(startsWith ? "startswith" : "endswith")}", lambda);

                    return _sqlExpressionFactory.Like(
                        translatedInstance,
                        new SqlParameterExpression(escapedPatternParameter.Name!, escapedPatternParameter.Type, stringTypeMapping),
                        _sqlExpressionFactory.Constant(LikeEscapeString));
                }

                default:
                    // The pattern is a column or a complex expression; the possible special characters in the pattern cannot be escaped,
                    // preventing us from translating to LIKE.
                    if (startsWith)
                    {
                        // Generate: WHERE instance IS NOT NULL AND pattern IS NOT NULL AND (substr(instance, 1, length(pattern)) = pattern OR pattern = '')
                        // Note that the empty string pattern needs special handling, since in .NET it returns true for all non-null
                        // instances, but substr(instance, 0) returns the entire string in SQLite.
                        // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                        // simple equality would yield true in that case, but we want false. We technically
                        return
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedInstance),
                                _sqlExpressionFactory.AndAlso(
                                    _sqlExpressionFactory.IsNotNull(translatedPattern),
                                    _sqlExpressionFactory.OrElse(
                                        _sqlExpressionFactory.Equal(
                                            _sqlExpressionFactory.Function(
                                                "substr",
                                                [
                                                    translatedInstance,
                                                    _sqlExpressionFactory.Constant(1),
                                                    _sqlExpressionFactory.Function(
                                                        "length",
                                                        [translatedPattern],
                                                        nullable: true,
                                                        argumentsPropagateNullability: Statics.TrueArrays[1],
                                                        typeof(int))
                                                ],
                                                nullable: true,
                                                argumentsPropagateNullability: [true, false, false],
                                                typeof(string),
                                                stringTypeMapping),
                                            translatedPattern),
                                        _sqlExpressionFactory.Equal(translatedPattern, _sqlExpressionFactory.Constant(string.Empty)))));
                    }

                    // Generate: WHERE instance IS NOT NULL AND pattern IS NOT NULL AND (substr(instance, -length(pattern)) = pattern OR pattern = '')
                    // Note that the empty string pattern needs special handling, since in .NET it returns true for all non-null
                    // instances, but substr(instance, 0) returns the entire string in SQLite.
                    // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                    // simple equality would yield true in that case, but we want false. We technically
                    return
                        _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedPattern),
                                _sqlExpressionFactory.OrElse(
                                    _sqlExpressionFactory.Equal(
                                        _sqlExpressionFactory.Function(
                                            "substr",
                                            [
                                                translatedInstance,
                                                _sqlExpressionFactory.Negate(
                                                    _sqlExpressionFactory.Function(
                                                        "length",
                                                        [translatedPattern],
                                                        nullable: true,
                                                        argumentsPropagateNullability: Statics.TrueArrays[1],
                                                        typeof(int)))
                                            ],
                                            nullable: true,
                                            argumentsPropagateNullability: Statics.TrueArrays[2],
                                            typeof(string),
                                            stringTypeMapping),
                                        translatedPattern),
                                    _sqlExpressionFactory.Equal(translatedPattern, _sqlExpressionFactory.Constant(string.Empty)))));
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override Expression VisitMethodCall(MethodCallExpression methodCallExpression)
    {
        if (base.VisitMethodCall(methodCallExpression) is var translation
            && translation != QueryCompilationContext.NotTranslatedExpression)
        {
            return translation;
        }

        var method = methodCallExpression.Method;
        var declaringType = method.DeclaringType;
        var @object = methodCallExpression.Object;
        var arguments = methodCallExpression.Arguments;

        switch (method.Name)
        {
            // https://learn.microsoft.com/dotnet/api/system.string.startswith#system-string-startswith(system-string)
            // https://learn.microsoft.com/dotnet/api/system.string.startswith#system-string-startswith(system-char)
            // https://learn.microsoft.com/dotnet/api/system.string.endswith#system-string-endswith(system-string)
            // https://learn.microsoft.com/dotnet/api/system.string.endswith#system-string-endswith(system-char)
            case nameof(string.StartsWith) or nameof(string.EndsWith)
                when methodCallExpression.Object is not null
                && declaringType == typeof(string)
                && arguments is [Expression value]
                && (value.Type == typeof(string) || value.Type == typeof(char)):
            {
                return TranslateStartsEndsWith(
                    methodCallExpression.Object,
                    value,
                    method.Name is nameof(string.StartsWith));
            }

            // We translate EF.Functions.JsonPathExists here and not in a method translator since we need to support JsonPathExists over
            // complex and owned JSON properties, which requires special handling.
            case nameof(RelationalDbFunctionsExtensions.JsonPathExists)
                when declaringType == typeof(RelationalDbFunctionsExtensions)
                && @object is null
                && arguments is [_, var json, var path]:
            {
                if (Translate(path) is not SqlExpression translatedPath)
                {
                    return QueryCompilationContext.NotTranslatedExpression;
                }

#pragma warning disable EF1001 // TranslateProjection() is pubternal
                var translatedJson = TranslateProjection(json) switch
                {
                    // The JSON argument is a scalar string property
                    SqlExpression scalar => scalar,

                    // The JSON argument is a complex or owned JSON property
                    RelationalStructuralTypeShaperExpression { ValueBufferExpression: JsonQueryExpression { JsonColumn: var c } } => c,
                    _ => null
                };
#pragma warning restore EF1001

                return translatedJson is null
                    ? QueryCompilationContext.NotTranslatedExpression
                    : _sqlExpressionFactory.IsNotNull(
                        _sqlExpressionFactory.Function(
                            "json_type",
                            [translatedJson, translatedPath],
                            nullable: true,
                            // Note that json_type() does propagate nullability; however, our query pipeline assumes that if arguments
                            // propagate nullability, that's the *only* reason for the function to return null; this means that if the
                            // arguments are non-nullable, the IS NOT NULL wrapping check can be optimized away.
                            argumentsPropagateNullability: [false, false],
                            typeof(int)));
            }
        }

        return QueryCompilationContext.NotTranslatedExpression;

        Expression TranslateStartsEndsWith(Expression instance, Expression pattern, bool startsWith)
        {
            if (Visit(instance) is not SqlExpression translatedInstance
                || Visit(pattern) is not SqlExpression translatedPattern)
            {
                return QueryCompilationContext.NotTranslatedExpression;
            }

            var stringTypeMapping = ExpressionExtensions.InferTypeMapping(translatedInstance, translatedPattern);

            translatedInstance = _sqlExpressionFactory.ApplyTypeMapping(translatedInstance, stringTypeMapping);
            translatedPattern = _sqlExpressionFactory.ApplyTypeMapping(translatedPattern, stringTypeMapping);

            switch (translatedPattern)
            {
                case SqlConstantExpression patternConstant:
                {
                    // The pattern is constant. Aside from null and empty string, we escape all special characters (%, _, \) and send a
                    // simple LIKE
                    return patternConstant.Value switch
                    {
                        null => _sqlExpressionFactory.Like(
                            translatedInstance,
                            _sqlExpressionFactory.Constant(null, typeof(string), stringTypeMapping)),

                        // In .NET, all strings start with/end with/contain the empty string, but SQL LIKE return false for empty patterns.
                        // Return % which always matches instead.
                        // Note that we don't just return a true constant, since null strings shouldn't match even an empty string
                        // (but SqlNullabilityProcess will convert this to a true constant if the instance is non-nullable)
                        "" => _sqlExpressionFactory.Like(translatedInstance, _sqlExpressionFactory.Constant("%")),

                        string s => s.Any(IsLikeWildChar)
                            ? _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? $"{EscapeLikePattern(s)}%" : $"%{EscapeLikePattern(s)}"),
                                _sqlExpressionFactory.Constant(LikeEscapeString))
                            : _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? $"{s}%" : $"%{s}")),

                        char s => IsLikeWildChar(s)
                            ? _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? $"{LikeEscapeChar}{s}%" : $"%{LikeEscapeChar}{s}"),
                                _sqlExpressionFactory.Constant(LikeEscapeString))
                            : _sqlExpressionFactory.Like(
                                translatedInstance,
                                _sqlExpressionFactory.Constant(startsWith ? $"{s}%" : $"%{s}")),

                        _ => throw new UnreachableException()
                    };
                }

                case SqlParameterExpression patternParameter:
                {
                    // The pattern is a parameter, register a runtime parameter that will contain the rewritten LIKE pattern, where
                    // all special characters have been escaped.
                    var lambda = Expression.Lambda(
                        Expression.Call(
                            EscapeLikePatternParameterMethod,
                            QueryCompilationContext.QueryContextParameter,
                            Expression.Constant(patternParameter.Name),
                            Expression.Constant(startsWith)),
                        QueryCompilationContext.QueryContextParameter);

                    var escapedPatternParameter =
                        _queryCompilationContext.RegisterRuntimeParameter(
                            $"{patternParameter.Name}_{(startsWith ? "startswith" : "endswith")}", lambda);

                    return _sqlExpressionFactory.Like(
                        translatedInstance,
                        new SqlParameterExpression(escapedPatternParameter.Name!, escapedPatternParameter.Type, stringTypeMapping),
                        _sqlExpressionFactory.Constant(LikeEscapeString));
                }

                default:
                    // The pattern is a column or a complex expression; the possible special characters in the pattern cannot be escaped,
                    // preventing us from translating to LIKE.
                    if (startsWith)
                    {
                        // Generate: WHERE instance IS NOT NULL AND pattern IS NOT NULL AND (substr(instance, 1, length(pattern)) = pattern OR pattern = '')
                        // Note that the empty string pattern needs special handling, since in .NET it returns true for all non-null
                        // instances, but substr(instance, 0) returns the entire string in SQLite.
                        // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                        // simple equality would yield true in that case, but we want false. We technically
                        return
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedInstance),
                                _sqlExpressionFactory.AndAlso(
                                    _sqlExpressionFactory.IsNotNull(translatedPattern),
                                    _sqlExpressionFactory.OrElse(
                                        _sqlExpressionFactory.Equal(
                                            _sqlExpressionFactory.Function(
                                                "substr",
                                                [
                                                    translatedInstance,
                                                    _sqlExpressionFactory.Constant(1),
                                                    _sqlExpressionFactory.Function(
                                                        "length",
                                                        [translatedPattern],
                                                        nullable: true,
                                                        argumentsPropagateNullability: Statics.TrueArrays[1],
                                                        typeof(int))
                                                ],
                                                nullable: true,
                                                argumentsPropagateNullability: [true, false, false],
                                                typeof(string),
                                                stringTypeMapping),
                                            translatedPattern),
                                        _sqlExpressionFactory.Equal(translatedPattern, _sqlExpressionFactory.Constant(string.Empty)))));
                    }

                    // Generate: WHERE instance IS NOT NULL AND pattern IS NOT NULL AND (substr(instance, -length(pattern)) = pattern OR pattern = '')
                    // Note that the empty string pattern needs special handling, since in .NET it returns true for all non-null
                    // instances, but substr(instance, 0) returns the entire string in SQLite.
                    // Note that we compensate for the case where both the instance and the pattern are null (null.StartsWith(null)); a
                    // simple equality would yield true in that case, but we want false. We technically
                    return
                        _sqlExpressionFactory.AndAlso(
                            _sqlExpressionFactory.IsNotNull(translatedInstance),
                            _sqlExpressionFactory.AndAlso(
                                _sqlExpressionFactory.IsNotNull(translatedPattern),
                                _sqlExpressionFactory.OrElse(
                                    _sqlExpressionFactory.Equal(
                                        _sqlExpressionFactory.Function(
                                            "substr",
                                            [
                                                translatedInstance,
                                                _sqlExpressionFactory.Negate(
                                                    _sqlExpressionFactory.Function(
                                                        "length",
                                                        [translatedPattern],
                                                        nullable: true,
                                                        argumentsPropagateNullability: Statics.TrueArrays[1],
                                                        typeof(int)))
                                            ],
                                            nullable: true,
                                            argumentsPropagateNullability: Statics.TrueArrays[2],
                                            typeof(string),
                                            stringTypeMapping),
                                        translatedPattern),
                                    _sqlExpressionFactory.Equal(translatedPattern, _sqlExpressionFactory.Constant(string.Empty)))));
            }
        }
    }
```

### 🔹 函式: `SqliteSqlTranslatingExpressionVisitor.ConstructLikePatternParameter()`
- **變更前簽章 (Before)**: `SqliteSqlTranslatingExpressionVisitor.ConstructLikePatternParameter(
        QueryContext queryContext,
        string baseParameterName,
        bool startsWith)` (L426~L446)
- **變更後簽章 (After)**: `SqliteSqlTranslatingExpressionVisitor.ConstructLikePatternParameter(
        QueryContext queryContext,
        string baseParameterName,
        bool startsWith)` (L426~L446)

#### ◀️ 變更前實作碼 (Before Implementation):
```
[EntityFrameworkInternal] // Can be called from precompiled shapers
    public static string? ConstructLikePatternParameter(
        QueryContext queryContext,
        string baseParameterName,
        bool startsWith)
        => queryContext.Parameters[baseParameterName] switch
        {
            null => null,

            // In .NET, all strings start/end with the empty string, but SQL LIKE return false for empty patterns.
            // Return % which always matches instead.
            "" => "%",

            string s => startsWith ? EscapeLikePattern(s) + '%' : '%' + EscapeLikePattern(s),

            char s when IsLikeWildChar(s) => startsWith ? LikeEscapeString + s + '%' : '%' + LikeEscapeString + s,

            char s => startsWith ? s + "%" : "%" + s,

            _ => throw new UnreachableException()
        };
```

#### ▶️ 變更後實作碼 (After Implementation):
```
[EntityFrameworkInternal] // Can be called from precompiled shapers
    public static string? ConstructLikePatternParameter(
        QueryContext queryContext,
        string baseParameterName,
        bool startsWith)
        => queryContext.Parameters[baseParameterName] switch
        {
            null => null,

            // In .NET, all strings start/end with the empty string, but SQL LIKE return false for empty patterns.
            // Return % which always matches instead.
            "" => "%",

            string s => startsWith ? $"{EscapeLikePattern(s)}%" : $"%{EscapeLikePattern(s)}",

            char s when IsLikeWildChar(s) => startsWith ? $"{LikeEscapeChar}{s}%" : $"%{LikeEscapeChar}{s}",

            char s => startsWith ? $"{s}%" : $"%{s}",

            _ => throw new UnreachableException()
        };
```


---

### 🔹 Commit #20: `7ae0f8f7`
- **完整 Hash**: `7ae0f8f72996c83b9311d0e168eebb41bc160264`
- **說明 (Ground Truth)**: Fix negated nullable comparison in a CASE condition (#39084)
- **變更檔案數**: 1

#### 📄 檔案: `src/EFCore.Relational/Query/SqlExpressionFactory.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:96, E:129, A:0) ➔ After(N:96, E:129, A:0)
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
  • + [新增呼叫邊] `SqlExpressionFactory.Case` ──[CALLS]──> `SqlExpressionFactory.Case`
  • - [移除呼叫邊] `SqlExpressionFactory.Case` ──[CALLS]──> `SqlExpressionFactory.Not`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SqlExpressionFactory.Case()`
- **變更前簽章 (Before)**: `SqlExpressionFactory.Case(
        SqlExpression? operand,
        IReadOnlyList<CaseWhenClause> whenClauses,
        SqlExpression? elseResult,
        SqlExpression? existingExpression = null)` (L705~L899)
- **變更後簽章 (After)**: `SqlExpressionFactory.Case(
        SqlExpression? operand,
        IReadOnlyList<CaseWhenClause> whenClauses,
        SqlExpression? elseResult,
        SqlExpression? existingExpression = null)` (L705~L918)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public virtual SqlExpression Case(
        SqlExpression? operand,
        IReadOnlyList<CaseWhenClause> whenClauses,
        SqlExpression? elseResult,
        SqlExpression? existingExpression = null)
    {
        RelationalTypeMapping? testTypeMapping;
        if (operand == null)
        {
            testTypeMapping = _boolTypeMapping;
        }
        else
        {
            testTypeMapping = operand.TypeMapping
                ?? whenClauses.Select(wc => wc.Test.TypeMapping).FirstOrDefault(t => t != null)
                // Since we never look at type of Operand/Test after this place,
                // we need to find actual typeMapping based on non-object type.
                ?? new[] { operand.Type }.Concat(whenClauses.Select(wc => wc.Test.Type))
                    .Where(t => t != typeof(object)).Select(t => _typeMappingSource.FindMapping(t, Dependencies.Model))
                    .FirstOrDefault();

            operand = ApplyTypeMapping(operand, testTypeMapping);
        }

        var resultTypeMapping = elseResult?.TypeMapping
            ?? whenClauses.Select(wc => wc.Result.TypeMapping).FirstOrDefault(t => t != null);

        elseResult = ApplyTypeMapping(elseResult, resultTypeMapping);

        var typeMappedWhenClauses = new List<CaseWhenClause>();
        foreach (var caseWhenClause in whenClauses)
        {
            var test = caseWhenClause.Test;

            if (operand == null && test is CaseExpression { Operand: null, WhenClauses: [var nestedSingleClause] } testExpr)
            {
                if (nestedSingleClause.Result is SqlConstantExpression { Value: true }
                    && testExpr.ElseResult is null or SqlConstantExpression { Value: false or null })
                {
                    // WHEN CASE
                    //   WHEN x THEN TRUE
                    //   ELSE FALSE/NULL
                    // END THEN y
                    // simplifies to
                    // WHEN x THEN y
                    test = nestedSingleClause.Test;
                }
                else if (nestedSingleClause.Result is SqlConstantExpression { Value: false or null }
                         && testExpr.ElseResult is SqlConstantExpression { Value: true })
                {
                    // same for the negated results
                    test = Not(nestedSingleClause.Test);
                }
            }

            typeMappedWhenClauses.Add(
                new CaseWhenClause(
                    ApplyTypeMapping(test, testTypeMapping),
                    ApplyTypeMapping(caseWhenClause.Result, resultTypeMapping)));
        }

        if (operand is null && elseResult is CaseExpression { Operand: null } nestedCaseExpression)
        {
            typeMappedWhenClauses.AddRange(nestedCaseExpression.WhenClauses);
            elseResult = nestedCaseExpression.ElseResult;
        }

        typeMappedWhenClauses = typeMappedWhenClauses
            .Where(c => !IsSkipped(c))
            .TakeUpTo(IsMatched)
            .DistinctBy(c => c.Test)
            .ToList();

        // CASE
        //   ...
        //   WHEN TRUE THEN a
        //   ELSE b
        // END
        // simplifies to
        // CASE
        //   ...
        //   ELSE a
        // END
        if (typeMappedWhenClauses.Count > 0 && IsMatched(typeMappedWhenClauses[^1]))
        {
            elseResult = typeMappedWhenClauses[^1].Result;
            typeMappedWhenClauses.RemoveAt(typeMappedWhenClauses.Count - 1);
        }

        var nullResult = Constant(null, elseResult?.Type ?? whenClauses[0].Result.Type, resultTypeMapping);

        // if there are no whenClauses left (e.g. their tests evaluated to false):
        // - if there is Else block, return it
        // - if there is no Else block, return null
        if (typeMappedWhenClauses.Count == 0)
        {
            return elseResult ?? nullResult;
        }

        // omit `ELSE NULL` (this makes it easier to compare/reuse expressions)
        if (elseResult is SqlConstantExpression { Value: null })
        {
            elseResult = null;
        }

        // CASE
        //   ...
        //   WHEN x THEN CASE
        //     WHEN y THEN a
        //     ELSE b
        //   END
        //   ELSE b
        // END
        // simplifies to
        // CASE
        //   ...
        //   WHEN x AND y THEN a
        //   ELSE b
        // END
        if (operand == null
            && typeMappedWhenClauses[^1].Result is CaseExpression { Operand: null, WhenClauses: [var lastClause] } lastCase
            && Equals(elseResult, lastCase.ElseResult))
        {
            typeMappedWhenClauses[^1] = new CaseWhenClause(AndAlso(typeMappedWhenClauses[^1].Test, lastClause.Test), lastClause.Result);
            elseResult = lastCase.ElseResult;
        }

        // Simplify:
        //   a == b ? b : a -> a
        //   a != b ? a : b -> a
        // And lift:
        //   a == b ? null : a -> NULLIF(a, b)
        //   a != b ? a : null -> NULLIF(a, b)
        if (operand is null
            && typeMappedWhenClauses is
            [
                {
                    Test: SqlBinaryExpression
                    {
                        OperatorType: ExpressionType.Equal or ExpressionType.NotEqual,
                        Left: var left,
                        Right: var right
                    } binary,
                    Result: var result
                }
            ])
        {
            // Swap result/elseResult for NotEqual so we can reason uniformly about ifEqual/ifNotEqual.
            // A missing ELSE clause is equivalent to ELSE NULL, so normalize to a null constant for matching.
            var (ifEqual, ifNotEqual) = binary.OperatorType is ExpressionType.Equal
                ? (result, elseResult ?? Constant(null, result.Type, result.TypeMapping))
                : (elseResult ?? Constant(null, result.Type, result.TypeMapping), result);

            // 'left' survives the conditional.
            if (left.Equals(ifNotEqual))
            {
                switch (ifEqual)
                {
                    // a == b ? b : a -> a   (also collapses NULLIF(a, NULL) when both are null constants)
                    case var _ when ifEqual.Equals(right):
                        return left;
                    // a == b ? null : a -> NULLIF(a, b)
                    case SqlConstantExpression { Value: null }:
                        return Function("NULLIF", [left, right], nullable: true, Statics.TrueFalse, left.Type, left.TypeMapping);
                }
            }

            // 'right' survives the conditional (operand-swapped equivalents of the patterns above).
            if (right.Equals(ifNotEqual))
            {
                switch (ifEqual)
                {
                    // a == b ? a : b -> b
                    case var _ when ifEqual.Equals(left):
                        return right;
                    // a == b ? null : b -> NULLIF(b, a)
                    case SqlConstantExpression { Value: null }:
                        return Function("NULLIF", [right, left], nullable: true, Statics.TrueFalse, right.Type, right.TypeMapping);
                }
            }
        }

        return existingExpression is CaseExpression expr
            && operand == expr.Operand
            && typeMappedWhenClauses.SequenceEqual(expr.WhenClauses)
            && elseResult == expr.ElseResult
                ? expr
                : new CaseExpression(operand, typeMappedWhenClauses, elseResult);

        bool IsSkipped(CaseWhenClause clause)
            => operand is null && clause.Test is SqlConstantExpression { Value: false or null };

        bool IsMatched(CaseWhenClause clause)
            => operand is null && clause.Test is SqlConstantExpression { Value: true };
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public virtual SqlExpression Case(
        SqlExpression? operand,
        IReadOnlyList<CaseWhenClause> whenClauses,
        SqlExpression? elseResult,
        SqlExpression? existingExpression = null)
    {
        RelationalTypeMapping? testTypeMapping;
        if (operand == null)
        {
            testTypeMapping = _boolTypeMapping;
        }
        else
        {
            testTypeMapping = operand.TypeMapping
                ?? whenClauses.Select(wc => wc.Test.TypeMapping).FirstOrDefault(t => t != null)
                // Since we never look at type of Operand/Test after this place,
                // we need to find actual typeMapping based on non-object type.
                ?? new[] { operand.Type }.Concat(whenClauses.Select(wc => wc.Test.Type))
                    .Where(t => t != typeof(object)).Select(t => _typeMappingSource.FindMapping(t, Dependencies.Model))
                    .FirstOrDefault();

            operand = ApplyTypeMapping(operand, testTypeMapping);
        }

        var resultTypeMapping = elseResult?.TypeMapping
            ?? whenClauses.Select(wc => wc.Result.TypeMapping).FirstOrDefault(t => t != null);

        elseResult = ApplyTypeMapping(elseResult, resultTypeMapping);

        var typeMappedWhenClauses = new List<CaseWhenClause>();
        foreach (var caseWhenClause in whenClauses)
        {
            var test = caseWhenClause.Test;

            if (operand == null && test is CaseExpression { Operand: null, WhenClauses: [var nestedSingleClause] } testExpr)
            {
                if (nestedSingleClause.Result is SqlConstantExpression { Value: true }
                    && testExpr.ElseResult is null or SqlConstantExpression { Value: false or null })
                {
                    // WHEN CASE
                    //   WHEN x THEN TRUE
                    //   ELSE FALSE/NULL
                    // END THEN y
                    // simplifies to
                    // WHEN x THEN y
                    test = nestedSingleClause.Test;
                }
                else if (whenClauses.Count == 1
                         && nestedSingleClause.Result is SqlConstantExpression { Value: false or null }
                         && testExpr.ElseResult is SqlConstantExpression { Value: true })
                {
                    // CASE
                    //   WHEN CASE
                    //     WHEN x THEN FALSE/NULL
                    //     ELSE TRUE
                    //   END THEN y
                    //   ELSE z
                    // END
                    // simplifies to
                    // CASE
                    //   WHEN x THEN z
                    //   ELSE y
                    // END
                    // It cannot become WHEN NOT x THEN y: when x is NULL the nested CASE is TRUE, but NOT x is NULL. That is
                    // the case the nested CASE exists for, as the nullability processor wraps a nullable comparison in it
                    // to give it C# semantics. With more clauses, swapping would change which one the remaining rows reach,
                    // so the nested CASE is left as is.
                    return Case(
                        operand: null,
                        [new CaseWhenClause(nestedSingleClause.Test, elseResult ?? Constant(null, caseWhenClause.Result.Type, caseWhenClause.Result.TypeMapping))],
                        caseWhenClause.Result);
                }
            }

            typeMappedWhenClauses.Add(
                new CaseWhenClause(
                    ApplyTypeMapping(test, testTypeMapping),
                    ApplyTypeMapping(caseWhenClause.Result, resultTypeMapping)));
        }

        if (operand is null && elseResult is CaseExpression { Operand: null } nestedCaseExpression)
        {
            typeMappedWhenClauses.AddRange(nestedCaseExpression.WhenClauses);
            elseResult = nestedCaseExpression.ElseResult;
        }

        typeMappedWhenClauses = typeMappedWhenClauses
            .Where(c => !IsSkipped(c))
            .TakeUpTo(IsMatched)
            .DistinctBy(c => c.Test)
            .ToList();

        // CASE
        //   ...
        //   WHEN TRUE THEN a
        //   ELSE b
        // END
        // simplifies to
        // CASE
        //   ...
        //   ELSE a
        // END
        if (typeMappedWhenClauses.Count > 0 && IsMatched(typeMappedWhenClauses[^1]))
        {
            elseResult = typeMappedWhenClauses[^1].Result;
            typeMappedWhenClauses.RemoveAt(typeMappedWhenClauses.Count - 1);
        }

        var nullResult = Constant(null, elseResult?.Type ?? whenClauses[0].Result.Type, resultTypeMapping);

        // if there are no whenClauses left (e.g. their tests evaluated to false):
        // - if there is Else block, return it
        // - if there is no Else block, return null
        if (typeMappedWhenClauses.Count == 0)
        {
            return elseResult ?? nullResult;
        }

        // omit `ELSE NULL` (this makes it easier to compare/reuse expressions)
        if (elseResult is SqlConstantExpression { Value: null })
        {
            elseResult = null;
        }

        // CASE
        //   ...
        //   WHEN x THEN CASE
        //     WHEN y THEN a
        //     ELSE b
        //   END
        //   ELSE b
        // END
        // simplifies to
        // CASE
        //   ...
        //   WHEN x AND y THEN a
        //   ELSE b
        // END
        if (operand == null
            && typeMappedWhenClauses[^1].Result is CaseExpression { Operand: null, WhenClauses: [var lastClause] } lastCase
            && Equals(elseResult, lastCase.ElseResult))
        {
            typeMappedWhenClauses[^1] = new CaseWhenClause(AndAlso(typeMappedWhenClauses[^1].Test, lastClause.Test), lastClause.Result);
            elseResult = lastCase.ElseResult;
        }

        // Simplify:
        //   a == b ? b : a -> a
        //   a != b ? a : b -> a
        // And lift:
        //   a == b ? null : a -> NULLIF(a, b)
        //   a != b ? a : null -> NULLIF(a, b)
        if (operand is null
            && typeMappedWhenClauses is
            [
                {
                    Test: SqlBinaryExpression
                    {
                        OperatorType: ExpressionType.Equal or ExpressionType.NotEqual,
                        Left: var left,
                        Right: var right
                    } binary,
                    Result: var result
                }
            ])
        {
            // Swap result/elseResult for NotEqual so we can reason uniformly about ifEqual/ifNotEqual.
            // A missing ELSE clause is equivalent to ELSE NULL, so normalize to a null constant for matching.
            var (ifEqual, ifNotEqual) = binary.OperatorType is ExpressionType.Equal
                ? (result, elseResult ?? Constant(null, result.Type, result.TypeMapping))
                : (elseResult ?? Constant(null, result.Type, result.TypeMapping), result);

            // 'left' survives the conditional.
            if (left.Equals(ifNotEqual))
            {
                switch (ifEqual)
                {
                    // a == b ? b : a -> a   (also collapses NULLIF(a, NULL) when both are null constants)
                    case var _ when ifEqual.Equals(right):
                        return left;
                    // a == b ? null : a -> NULLIF(a, b)
                    case SqlConstantExpression { Value: null }:
                        return Function("NULLIF", [left, right], nullable: true, Statics.TrueFalse, left.Type, left.TypeMapping);
                }
            }

            // 'right' survives the conditional (operand-swapped equivalents of the patterns above).
            if (right.Equals(ifNotEqual))
            {
                switch (ifEqual)
                {
                    // a == b ? a : b -> b
                    case var _ when ifEqual.Equals(left):
                        return right;
                    // a == b ? null : b -> NULLIF(b, a)
                    case SqlConstantExpression { Value: null }:
                        return Function("NULLIF", [right, left], nullable: true, Statics.TrueFalse, right.Type, right.TypeMapping);
                }
            }
        }

        return existingExpression is CaseExpression expr
            && operand == expr.Operand
            && typeMappedWhenClauses.SequenceEqual(expr.WhenClauses)
            && elseResult == expr.ElseResult
                ? expr
                : new CaseExpression(operand, typeMappedWhenClauses, elseResult);

        bool IsSkipped(CaseWhenClause clause)
            => operand is null && clause.Test is SqlConstantExpression { Value: false or null };

        bool IsMatched(CaseWhenClause clause)
            => operand is null && clause.Test is SqlConstantExpression { Value: true };
    }
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/efcore show abf7bd959db2a114fdc5efb02382984495c465c4
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff abf7bd959db2a114fdc5efb02382984495c465c4~1 --file test_repos/efcore/src/EFCore.SqlServer/Design/Internal/SqlServerAnnotationCodeGenerator.cs
   ```
