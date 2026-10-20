# 🔬 CODE-Map 基準審查獨立驗證報告: `alpine`
> **技術生態**: `JavaScript (宣告式響應前端核心)`  
> **本地倉庫路徑**: `test_repos/alpine`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 22 Files  
> **報告生成時間**: 2026-10-20 21:40:57  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `9` / `22` | `40.9%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `12` / `22` | `54.5%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `1` / `22` | `4.5%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`21` / `22`** | **`95.5%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `22` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `a7e28022`
- **完整 Hash**: `a7e280222df1f63b29370218d5e09c90110cc56d`
- **說明 (Ground Truth)**: Fix mutation observer recovery after errors (#4908)
- **變更檔案數**: 1

#### 📄 檔案: `packages/alpinejs/src/mutation.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:27, E:13, A:0) ➔ After(N:27, E:13, A:0)
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

### 🔹 函式: `mutateDom()`
- **變更前簽章 (Before)**: `function mutateDom(callback)` (L98~L108)
- **變更後簽章 (After)**: `function mutateDom(callback)` (L98~L108)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function mutateDom(callback) {
    if (! currentlyObserving) return callback()

    stopObservingMutations()

    let result = callback()

    startObservingMutations()

    return result
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function mutateDom(callback) {
    if (! currentlyObserving) return callback()

    stopObservingMutations()

    try {
        return callback()
    } finally {
        startObservingMutations()
    }
}
```


---

### 🔹 Commit #02: `636c78c4`
- **完整 Hash**: `636c78c4104704802b141666d9f20d2145a9ebd9`
- **說明 (Ground Truth)**: Fix: skip init() in x-data during clone, matching x-init behavior (#4901)
- **變更檔案數**: 1

#### 📄 檔案: `packages/alpinejs/src/directives/x-data.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:17, E:0, A:0) ➔ After(N:18, E:0, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `skipDuringClone (External/Unresolved)` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #03: `6996321f`
- **完整 Hash**: `6996321f7fef99fc4827cd4d0e9a7bc27a3cd10b`
- **說明 (Ground Truth)**: Fix(CspParser): accept reserved words as property/method names and object keys (#4905)
- **變更檔案數**: 1

#### 📄 檔案: `packages/csp/src/parser.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:50, E:2, A:1) ➔ After(N:53, E:2, A:1)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#blacklist** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `consumeIdentifierName` (FUNCTION_DEF)
  • + [新增節點] `IDENTIFIER_NAME_TYPES` (MODULE_STATE)
  • + [新增節點] `checkIdentifierName` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `parseObjectLiteral()`
- **變更前簽章 (Before)**: `parseObjectLiteral()` (L562~L608)
- **變更後簽章 (After)**: `parseObjectLiteral()` (L565~L611)

#### ◀️ 變更前實作碼 (Before Implementation):
```
parseObjectLiteral() {
        const properties = [];

        while (!this.check('PUNCTUATION', '}') && !this.isAtEnd()) {
            let key;
            let computed = false;

            if (this.match('STRING')) {
                key = { type: 'Literal', value: this.previous().value };
            } else if (this.match('IDENTIFIER')) {
                const name = this.previous().value;
                key = { type: 'Identifier', name };
            } else if (this.match('PUNCTUATION', '[')) {
                key = this.parseExpression();
                computed = true;
                this.consume('PUNCTUATION', ']');
            } else {
                throw new Error('Expected property key');
            }

            this.consume('PUNCTUATION', ':');
            const value = this.parseExpression();

            properties.push({
                type: 'Property',
                key,
                value,
                computed,
                shorthand: false
            });

            if (this.match('PUNCTUATION', ',')) {
                // Handle trailing comma
                if (this.check('PUNCTUATION', '}')) {
                    break;
                }
            } else {
                break;
            }
        }

        this.consume('PUNCTUATION', '}');
        return {
            type: 'ObjectExpression',
            properties
        };
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
parseObjectLiteral() {
        const properties = [];

        while (!this.check('PUNCTUATION', '}') && !this.isAtEnd()) {
            let key;
            let computed = false;

            if (this.match('STRING')) {
                key = { type: 'Literal', value: this.previous().value };
            } else if (this.checkIdentifierName()) {
                const name = this.consumeIdentifierName();
                key = { type: 'Identifier', name };
            } else if (this.match('PUNCTUATION', '[')) {
                key = this.parseExpression();
                computed = true;
                this.consume('PUNCTUATION', ']');
            } else {
                throw new Error('Expected property key');
            }

            this.consume('PUNCTUATION', ':');
            const value = this.parseExpression();

            properties.push({
                type: 'Property',
                key,
                value,
                computed,
                shorthand: false
            });

            if (this.match('PUNCTUATION', ',')) {
                // Handle trailing comma
                if (this.check('PUNCTUATION', '}')) {
                    break;
                }
            } else {
                break;
            }
        }

        this.consume('PUNCTUATION', '}');
        return {
            type: 'ObjectExpression',
            properties
        };
    }
```

### 🔹 函式: `parseMember()`
- **變更前簽章 (Before)**: `parseMember()` (L440~L474)
- **變更後簽章 (After)**: `parseMember()` (L443~L477)

#### ◀️ 變更前實作碼 (Before Implementation):
```
parseMember() {
        let expr = this.parsePrimary();

        while (true) {
            if (this.match('PUNCTUATION', '.')) {
                const property = this.consume('IDENTIFIER');
                expr = {
                    type: 'MemberExpression',
                    object: expr,
                    property: { type: 'Identifier', name: property.value },
                    computed: false
                };
            } else if (this.match('PUNCTUATION', '[')) {
                const property = this.parseExpression();
                this.consume('PUNCTUATION', ']');
                expr = {
                    type: 'MemberExpression',
                    object: expr,
                    property,
                    computed: true
                };
            } else if (this.match('PUNCTUATION', '(')) {
                const args = this.parseArguments();
                expr = {
                    type: 'CallExpression',
                    callee: expr,
                    arguments: args
                };
            } else {
                break;
            }
        }

        return expr;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
parseMember() {
        let expr = this.parsePrimary();

        while (true) {
            if (this.match('PUNCTUATION', '.')) {
                const name = this.consumeIdentifierName();
                expr = {
                    type: 'MemberExpression',
                    object: expr,
                    property: { type: 'Identifier', name },
                    computed: false
                };
            } else if (this.match('PUNCTUATION', '[')) {
                const property = this.parseExpression();
                this.consume('PUNCTUATION', ']');
                expr = {
                    type: 'MemberExpression',
                    object: expr,
                    property,
                    computed: true
                };
            } else if (this.match('PUNCTUATION', '(')) {
                const args = this.parseArguments();
                expr = {
                    type: 'CallExpression',
                    callee: expr,
                    arguments: args
                };
            } else {
                break;
            }
        }

        return expr;
    }
```


---

### 🔹 Commit #04: `e610f47b`
- **完整 Hash**: `e610f47b7748670d285f988351ccf04ddee05a62`
- **說明 (Ground Truth)**: Fix CSP initialization in sandboxed iframes (#4893)
- **變更檔案數**: 1

#### 📄 檔案: `packages/csp/src/parser.js`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:49, E:2, A:0) ➔ After(N:49, E:2, A:0)
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

### 🔹 Commit #05: `022c4946`
- **完整 Hash**: `022c4946da6316f5d7e4175f7f2e22941a6052e0`
- **說明 (Ground Truth)**: fix(csp): parse Unicode string escapes (#4881)
- **變更檔案數**: 1

#### 📄 檔案: `packages/csp/src/parser.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:49, E:2, A:0) ➔ After(N:49, E:2, A:0)
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

### 🔹 函式: `readString()`
- **變更前簽章 (Before)**: `readString()` (L124~L159)
- **變更後簽章 (After)**: `readString()` (L124~L171)

#### ◀️ 變更前實作碼 (Before Implementation):
```
readString() {
        const start = this.position;
        const quote = this.input[this.position];
        this.position++; // Skip opening quote

        let value = '';
        let escaped = false;

        while (this.position < this.input.length) {
            const char = this.input[this.position];

            if (escaped) {
                switch (char) {
                    case 'n': value += '\n'; break;
                    case 't': value += '\t'; break;
                    case 'r': value += '\r'; break;
                    case '\\': value += '\\'; break;
                    case quote: value += quote; break;
                    default: value += char;
                }
                escaped = false;
            } else if (char === '\\') {
                escaped = true;
            } else if (char === quote) {
                this.position++; // Skip closing quote
                this.tokens.push(new Token('STRING', value, start, this.position));
                return;
            } else {
                value += char;
            }

            this.position++;
        }

        throw new Error(`Unterminated string starting at position ${start}`);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
readString() {
        const start = this.position;
        const quote = this.input[this.position];
        this.position++; // Skip opening quote

        let value = '';
        let escaped = false;

        while (this.position < this.input.length) {
            const char = this.input[this.position];

            if (escaped) {
                switch (char) {
                    case 'n': value += '\n'; break;
                    case 't': value += '\t'; break;
                    case 'r': value += '\r'; break;
                    case '\\': value += '\\'; break;
                    case quote: value += quote; break;
                    case 'u': {
                        const codeUnit = this.input.slice(this.position + 1, this.position + 5);

                        if (/^[0-9a-fA-F]{4}$/.test(codeUnit)) {
                            value += String.fromCharCode(parseInt(codeUnit, 16));
                            this.position += 4;
                        } else {
                            value += char;
                        }

                        break;
                    }
                    default: value += char;
                }
                escaped = false;
            } else if (char === '\\') {
                escaped = true;
            } else if (char === quote) {
                this.position++; // Skip closing quote
                this.tokens.push(new Token('STRING', value, start, this.position));
                return;
            } else {
                value += char;
            }

            this.position++;
        }

        throw new Error(`Unterminated string starting at position ${start}`);
    }
```


---

### 🔹 Commit #06: `cd7b353e`
- **完整 Hash**: `cd7b353e9849afea96737c60117650ac21008970`
- **說明 (Ground Truth)**: Fix `x-mask` attribute changes on `x-model` inputs (#4852)
- **變更檔案數**: 1

#### 📄 檔案: `packages/mask/src/index.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:25, E:25, A:1) ➔ After(N:27, E:26, A:1)
- **差分統計**: +Nodes: 3, -Nodes: 1, +Edges: 5, -Edges: 4, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#el** `(Control)`
    └── ⚡ **on('blur')**
        └── 🎯 [TRIGGERS] `on('blur')_handler()`
            └── 🎯 [CALLS] `processInputValue()`
                └── 🎯 [CALLS] `setInput()`
                    └── 🎯 [CALLS] `formatInput()`
                └── 🎯 [CALLS] `templateFn()`
                └── 🎯 [CALLS] `restoreCursorPosition()`
                    └── 🎯 [CALLS] `callback (External/Unresolved)()`
                    └── *ref:`formatInput` [已折疊指針]
    └── ⚡ **on('input')**
        └── 🎯 [TRIGGERS] `on('input')_handler()`
            └── *ref:`processInputValue` [已折疊指針]

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `undoModelUpdate` (FUNCTION_DEF)
  • + [新增節點] `undoModelUpdate` (FUNCTION_DEF)
  • + [新增節點] `update` (FUNCTION_DEF)
  • - [移除節點] `_x_forceModelUpdate` (FUNCTION_DEF)
  • + [新增呼叫邊] `directive:mask` ──[CALLS]──> `undoModelUpdate`
  • + [新增呼叫邊] `update` ──[CALLS [guard: (value === undefined)]]──> `updater (External/Unresolved)`
  • + [新增呼叫邊] `update` ──[CALLS [guard: (value === undefined)]]──> `String (External/Unresolved)`
  • + [新增呼叫邊] `update` ──[CALLS [guard: (value === undefined)]]──> `templateFn`
  • + [新增呼叫邊] `update` ──[CALLS [guard: (template && template !== 'false')]]──> `formatInput`
  • - [移除呼叫邊] `_x_forceModelUpdate` ──[CALLS]──> `updater (External/Unresolved)`
  • - [移除呼叫邊] `_x_forceModelUpdate` ──[CALLS]──> `String (External/Unresolved)`
  • - [移除呼叫邊] `_x_forceModelUpdate` ──[CALLS]──> `templateFn`
  • - [移除呼叫邊] `_x_forceModelUpdate` ──[CALLS]──> `formatInput`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `directive:mask()`
- **變更前簽章 (Before)**: `directive:mask(el, { value, expression }, { effect, evaluateLater, cleanup })` (L3~L120)
- **變更後簽章 (After)**: `directive:mask(el, { value, expression }, { effect, evaluateLater, cleanup })` (L3~L130)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(el, { value, expression }, { effect, evaluateLater, cleanup }) => {
        let templateFn = () => expression
        let lastInputValue = ''

        queueMicrotask(() => {
            if (['function', 'dynamic'].includes(value)) {
                // This is an x-mask:function directive.

                let evaluator = evaluateLater(expression)

                effect(() => {
                    templateFn = input => {
                        let result

                        // We need to prevent "auto-evaluation" of functions like
                        // x-on expressions do so that we can use them as mask functions.
                        Alpine.dontAutoEvaluateFunctions(() => {
                            evaluator(value => {
                                result = typeof value === 'function' ? value(input) : value
                            }, { scope: {
                                // These are "magics" we'll make available to the x-mask:function:
                                '$input': input,
                                '$money': formatMoney.bind({ el }),
                            }})
                        })

                        return result
                    }

                    // Run on initialize which serves a dual purpose:
                    // - Initializing the mask on the input if it has an initial value.
                    // - Running the template function to set up reactivity, so that
                    //   when a dependency inside it changes, the input re-masks.
                    processInputValue(el, false)
                })
            } else {
                processInputValue(el, false)
            }

            // Override x-model's initial value...
            if (el._x_model) {
                // If the x-model value is the same, don't override it as that will trigger updates...
                if (el._x_model.get() !== el.value) {
                    // If the x-model value is `null` and the input value is an empty
                    // string, don't override it as that will trigger updates...
                    if (!(el._x_model.get() === null && el.value === '')) {
                        el._x_model.set(el.value)
                    }
                }

                let updater = el._x_forceModelUpdate
                el._x_forceModelUpdate = (value) => {
                    // If the model value was cleared (e.g. the parent object was
                    // removed), just clear the input — don't format and write back
                    // as that would resurrect the model path with an empty value.
                    if (value === undefined) {
                        lastInputValue = ''
                        return updater(value)
                    }

                    value = String(value)
                    let template = templateFn(value)
                    if (template && template !== 'false') {
                        value = formatInput(template, value)
                    }
                    lastInputValue = value
                    updater(value)
                    el._x_model.set(value)
                }
            }
        })

        const controller = new AbortController()

        cleanup(() => {
            controller.abort()
        })

        el.addEventListener('input', () => processInputValue(el), {
            signal: controller.signal,
            // Setting this as a capture phase listener to ensure it runs
            // before wire:model or x-model added as a latent binding...
            capture: true,
        })

        // Don't "restoreCursorPosition" on "blur", because Safari
        // will re-focus the input and cause a focus trap.
        el.addEventListener('blur', () => processInputValue(el, false), { signal: controller.signal })

        function processInputValue (el, shouldRestoreCursor = true) {
            let input = el.value

            let template = templateFn(input)

            // If a template value is `falsy`, then don't process the input value
            if(!template || template === 'false') return false

            // If they hit backspace, don't process input.
            if (lastInputValue.length - el.value.length === 1) {
                return lastInputValue = el.value
            }

            let setInput = () => {
                lastInputValue = el.value = formatInput(template,input)
            }

            if (shouldRestoreCursor) {
                // When an input element's value is set, it moves the cursor to the end
                // therefore we need to track, estimate, and restore the cursor after
                // a change was made.
                restoreCursorPosition(el, template, () => {
                    setInput()
                })
            } else {
                setInput()
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(el, { value, expression }, { effect, evaluateLater, cleanup }) => {
        let templateFn = () => expression
        let lastInputValue = ''
        let undoModelUpdate = () => {}

        queueMicrotask(() => {
            if (['function', 'dynamic'].includes(value)) {
                // This is an x-mask:function directive.

                let evaluator = evaluateLater(expression)

                effect(() => {
                    templateFn = input => {
                        let result

                        // We need to prevent "auto-evaluation" of functions like
                        // x-on expressions do so that we can use them as mask functions.
                        Alpine.dontAutoEvaluateFunctions(() => {
                            evaluator(value => {
                                result = typeof value === 'function' ? value(input) : value
                            }, { scope: {
                                // These are "magics" we'll make available to the x-mask:function:
                                '$input': input,
                                '$money': formatMoney.bind({ el }),
                            }})
                        })

                        return result
                    }

                    // Run on initialize which serves a dual purpose:
                    // - Initializing the mask on the input if it has an initial value.
                    // - Running the template function to set up reactivity, so that
                    //   when a dependency inside it changes, the input re-masks.
                    processInputValue(el, false)
                })
            } else {
                processInputValue(el, false)
            }

            // Override x-model's initial value...
            if (el._x_model) {
                // If the x-model value is the same, don't override it as that will trigger updates...
                if (el._x_model.get() !== el.value) {
                    // If the x-model value is `null` and the input value is an empty
                    // string, don't override it as that will trigger updates...
                    if (!(el._x_model.get() === null && el.value === '')) {
                        el._x_model.set(el.value)
                    }
                }

                let updater = el._x_forceModelUpdate
                let update = (value) => {
                    // If the model value was cleared (e.g. the parent object was
                    // removed), just clear the input — don't format and write back
                    // as that would resurrect the model path with an empty value.
                    if (value === undefined) {
                        lastInputValue = ''
                        return updater(value)
                    }

                    value = String(value)
                    let template = templateFn(value)
                    if (template && template !== 'false') {
                        value = formatInput(template, value)
                    }
                    lastInputValue = value
                    updater(value)
                    el._x_model.set(value)
                }

                el._x_forceModelUpdate = update

                undoModelUpdate = () => {
                    if (el._x_forceModelUpdate === update) {
                        el._x_forceModelUpdate = updater
                    }
                }
            }
        })

        const controller = new AbortController()

        cleanup(() => {
            controller.abort()
            undoModelUpdate()
        })

        el.addEventListener('input', () => processInputValue(el), {
            signal: controller.signal,
            // Setting this as a capture phase listener to ensure it runs
            // before wire:model or x-model added as a latent binding...
            capture: true,
        })

        // Don't "restoreCursorPosition" on "blur", because Safari
        // will re-focus the input and cause a focus trap.
        el.addEventListener('blur', () => processInputValue(el, false), { signal: controller.signal })

        function processInputValue (el, shouldRestoreCursor = true) {
            let input = el.value

            let template = templateFn(input)

            // If a template value is `falsy`, then don't process the input value
            if(!template || template === 'false') return false

            // If they hit backspace, don't process input.
            if (lastInputValue.length - el.value.length === 1) {
                return lastInputValue = el.value
            }

            let setInput = () => {
                lastInputValue = el.value = formatInput(template,input)
            }

            if (shouldRestoreCursor) {
                // When an input element's value is set, it moves the cursor to the end
                // therefore we need to track, estimate, and restore the cursor after
                // a change was made.
                restoreCursorPosition(el, template, () => {
                    setInput()
                })
            } else {
                setInput()
            }
        }
    }
```


---

### 🔹 Commit #07: `eb6f4398`
- **完整 Hash**: `eb6f4398fdba2175204d993aaf2e4733479d2abc`
- **說明 (Ground Truth)**: fix(persist): don't persist undefined values (#4876)
- **變更檔案數**: 1

#### 📄 檔案: `packages/persist/src/index.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:14, E:13, A:0) ➔ After(N:14, E:13, A:0)
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
  - 💥 作用域阻隔: 函式 'persist' 被深鎖在內部閉包 (scope:arrow@after/packages/persist/src/index.js:L1C16)，外部無法調用！
  - 💥 作用域阻隔: 函式 'get' 被深鎖在內部閉包 (scope:arrow@after/packages/persist/src/index.js:L1C16)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `storageSet()`
- **變更前簽章 (Before)**: `function storageSet(key, value, storage)` (L79~L81)
- **變更後簽章 (After)**: `function storageSet(key, value, storage)` (L79~L91)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function storageSet(key, value, storage) {
    storage.setItem(key, JSON.stringify(value))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function storageSet(key, value, storage) {
    // Avoid persisting "undefined" values. JSON.stringify(undefined) returns
    // undefined, which the storage API coerces into the string "undefined".
    // On the next page load, JSON.parse("undefined") would throw and break
    // the component that initialized that persisted value.
    if (value === undefined) {
        storage.removeItem?.(key)

        return
    }

    storage.setItem(key, JSON.stringify(value))
}
```


---

### 🔹 Commit #08: `f96e3c8b`
- **完整 Hash**: `f96e3c8b79e5c954d7415a562c149fd62028257b`
- **說明 (Ground Truth)**: fix(persist): fix fallback dummy storage returning undefined for missing keys (#4867)
- **變更檔案數**: 1

#### 📄 檔案: `packages/persist/src/index.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:13, E:13, A:0) ➔ After(N:14, E:13, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `getItem` (FUNCTION_DEF)

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'persist' 被深鎖在內部閉包 (scope:arrow@after/packages/persist/src/index.js:L1C16)，外部無法調用！
  - 💥 作用域阻隔: 函式 'get' 被深鎖在內部閉包 (scope:arrow@after/packages/persist/src/index.js:L1C16)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `persist()`
- **變更前簽章 (Before)**: `persist()` (L2~L44)
- **變更後簽章 (After)**: `persist()` (L2~L44)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
        let alias
        let storage

        try {
            storage = localStorage
        } catch (e) {
            console.error(e)
            console.warn('Alpine: $persist is using temporary storage since localStorage is unavailable.')

            let dummy = new Map();

            storage = {
                getItem: dummy.get.bind(dummy),
                setItem: dummy.set.bind(dummy)
            }
        }

        return Alpine.interceptor((initialValue, getter, setter, path, key, cleanup = () => {}) => {
            let lookup = alias || `_x_${path}`

            let initial = storageHas(lookup, storage)
                ? storageGet(lookup, storage)
                : initialValue

            setter(initial)

            let effect = Alpine.effect(() => {
                let value = getter()

                storageSet(lookup, value, storage)

                setter(value)
            })

            cleanup(() => Alpine.release(effect))

            return initial
        }, func => {
            func.as = key => { alias = key; return func },
            func.using = target => { storage = target; return func }
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
        let alias
        let storage

        try {
            storage = localStorage
        } catch (e) {
            console.error(e)
            console.warn('Alpine: $persist is using temporary storage since localStorage is unavailable.')

            let dummy = new Map();

            storage = {
                getItem: key => dummy.has(key) ? dummy.get(key) : null,
                setItem: dummy.set.bind(dummy)
            }
        }

        return Alpine.interceptor((initialValue, getter, setter, path, key, cleanup = () => {}) => {
            let lookup = alias || `_x_${path}`

            let initial = storageHas(lookup, storage)
                ? storageGet(lookup, storage)
                : initialValue

            setter(initial)

            let effect = Alpine.effect(() => {
                let value = getter()

                storageSet(lookup, value, storage)

                setter(value)
            })

            cleanup(() => Alpine.release(effect))

            return initial
        }, func => {
            func.as = key => { alias = key; return func },
            func.using = target => { storage = target; return func }
        })
    }
```

### 🔹 函式: `storageHas()`
- **變更前簽章 (Before)**: `function storageHas(key, storage)` (L65~L67)
- **變更後簽章 (After)**: `function storageHas(key, storage)` (L65~L69)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function storageHas(key, storage) {
    return storage.getItem(key) !== null
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function storageHas(key, storage) {
    let value = storage.getItem(key)

    return value !== null && value !== undefined
}
```


---

### 🔹 Commit #09: `31119c5e`
- **完整 Hash**: `31119c5e898ff83e9fd02aab51851f139ab253fc`
- **說明 (Ground Truth)**: Pass cleanup callback to direct store interceptors (#4869)
- **變更檔案數**: 1

#### 📄 檔案: `packages/alpinejs/src/store.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:6, E:2, A:0) ➔ After(N:6, E:2, A:0)
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

### 🔹 函式: `store()`
- **變更前簽章 (Before)**: `function store(name, value)` (L7~L26)
- **變更後簽章 (After)**: `function store(name, value)` (L7~L26)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function store(name, value) {
    if (! isReactive) { stores = reactive(stores); isReactive = true; }

    if (value === undefined) {
        return stores[name]
    }

    stores[name] = value

    // Initialize the interceptor directly when it is the store value itself.
    if (typeof value === 'object' && value !== null && value._x_interceptor) {
        stores[name] = value.initialize(stores, name, name)
    } else {
        initInterceptors(stores[name])
    }

    if (typeof value === 'object' && value !== null && value.hasOwnProperty('init') && typeof value.init === 'function') {
        stores[name].init()
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function store(name, value) {
    if (! isReactive) { stores = reactive(stores); isReactive = true; }

    if (value === undefined) {
        return stores[name]
    }

    stores[name] = value

    // Initialize the interceptor directly when it is the store value itself.
    if (typeof value === 'object' && value !== null && value._x_interceptor) {
        stores[name] = value.initialize(stores, name, name, () => {})
    } else {
        initInterceptors(stores[name])
    }

    if (typeof value === 'object' && value !== null && value.hasOwnProperty('init') && typeof value.init === 'function') {
        stores[name].init()
    }
}
```


---

### 🔹 Commit #10: `bc956c22`
- **完整 Hash**: `bc956c22c4747a9ad01321c2df1822ca0f510150`
- **說明 (Ground Truth)**: Fix persisted direct stores (#4859)
- **變更檔案數**: 1

#### 📄 檔案: `packages/alpinejs/src/store.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:6, E:2, A:0) ➔ After(N:6, E:2, A:0)
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

### 🔹 函式: `store()`
- **變更前簽章 (Before)**: `function store(name, value)` (L7~L21)
- **變更後簽章 (After)**: `function store(name, value)` (L7~L26)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function store(name, value) {
    if (! isReactive) { stores = reactive(stores); isReactive = true; }

    if (value === undefined) {
        return stores[name]
    }

    stores[name] = value

    initInterceptors(stores[name])

    if (typeof value === 'object' && value !== null && value.hasOwnProperty('init') && typeof value.init === 'function') {
        stores[name].init()
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function store(name, value) {
    if (! isReactive) { stores = reactive(stores); isReactive = true; }

    if (value === undefined) {
        return stores[name]
    }

    stores[name] = value

    // Initialize the interceptor directly when it is the store value itself.
    if (typeof value === 'object' && value !== null && value._x_interceptor) {
        stores[name] = value.initialize(stores, name, name)
    } else {
        initInterceptors(stores[name])
    }

    if (typeof value === 'object' && value !== null && value.hasOwnProperty('init') && typeof value.init === 'function') {
        stores[name].init()
    }
}
```


---

### 🔹 Commit #11: `13266d2c`
- **完整 Hash**: `13266d2c77b28b32b661bdf87b38feb1c360f9c5`
- **說明 (Ground Truth)**: Fix `:value` bindings not updating custom elements when bound object data mutates
- **變更檔案數**: 1

#### 📄 檔案: `packages/alpinejs/src/utils/bind.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:30, E:28, A:0) ➔ After(N:30, E:28, A:0)
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

### 🔹 函式: `bindInputValue()`
- **變更前簽章 (Before)**: `function bindInputValue(el, value)` (L41~L73)
- **變更後簽章 (After)**: `function bindInputValue(el, value)` (L41~L78)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function bindInputValue(el, value) {
    if (isRadio(el)) {
        // Set radio value from x-bind:value, if no "value" attribute exists.
        // If there are any initial state values, radio will have a correct
        // "checked" value since x-bind:value is processed before x-model.
        if (el.attributes.value === undefined) {
            el.value = value
        }
    } else if (isCheckbox(el)) {
        // If we are explicitly binding a string to the :value, set the string,
        // If the value is a boolean/array/number/null/undefined, leave it alone, it will be set to "on"
        // automatically.
        if (Number.isInteger(value)) {
            el.value = value
        } else if (! Array.isArray(value) && typeof value !== 'boolean' && ! [null, undefined].includes(value)) {
            el.value = String(value)
        } else {
            if (Array.isArray(value)) {
                el.checked = value.some(val => checkedAttrLooseCompare(val, el.value))
            } else {
                el.checked = !!value
            }
        }
    } else if (el.tagName === 'SELECT') {
        updateSelect(el, value)
    } else if (el.tagName === 'OPTION') {
        bindAttribute(el, 'value', value)
    } else {
        if (el.value === value) return

        el.value = value === undefined ? '' : value
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function bindInputValue(el, value) {
    if (isRadio(el)) {
        // Set radio value from x-bind:value, if no "value" attribute exists.
        // If there are any initial state values, radio will have a correct
        // "checked" value since x-bind:value is processed before x-model.
        if (el.attributes.value === undefined) {
            el.value = value
        }
    } else if (isCheckbox(el)) {
        // If we are explicitly binding a string to the :value, set the string,
        // If the value is a boolean/array/number/null/undefined, leave it alone, it will be set to "on"
        // automatically.
        if (Number.isInteger(value)) {
            el.value = value
        } else if (! Array.isArray(value) && typeof value !== 'boolean' && ! [null, undefined].includes(value)) {
            el.value = String(value)
        } else {
            if (Array.isArray(value)) {
                el.checked = value.some(val => checkedAttrLooseCompare(val, el.value))
            } else {
                el.checked = !!value
            }
        }
    } else if (el.tagName === 'SELECT') {
        updateSelect(el, value)
    } else if (el.tagName === 'OPTION') {
        bindAttribute(el, 'value', value)
    } else {
        // For non-null objects, reference equality doesn't imply state
        // equality: reactive proxies can mutate internally while the
        // top-level reference stays the same. Without this guard, custom
        // elements receiving an object value via x-bind:value or x-model
        // would never see those nested updates.
        if (el.value === value && (typeof value !== 'object' || value === null)) return

        el.value = value === undefined ? '' : value
    }
}
```


---

### 🔹 Commit #12: `707c20cd`
- **完整 Hash**: `707c20cda9095623271314baa07147254ca65a37`
- **說明 (Ground Truth)**: Simplify option value fix to delegate to bindAttribute
- **變更檔案數**: 1

#### 📄 檔案: `packages/alpinejs/src/utils/bind.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:29, E:27, A:0) ➔ After(N:30, E:28, A:0)
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
  • + [新增節點] `isObjectAttr` (FUNCTION_DEF)
  • + [新增呼叫邊] `bindInputValue` ──[CALLS [guard: (isRadio(el))]]──> `bindAttribute`
  • + [新增呼叫邊] `bindAttribute` ──[CALLS [guard: ([null, undefined, false].includes(value) && attributeShouldntBePreservedIfFalsy(name))]]──> `isObjectAttr`
  • - [移除呼叫邊] `bindInputValue` ──[CALLS]──> `setIfChanged`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `bindAttribute()`
- **變更前簽章 (Before)**: `function bindAttribute(el, name, value)` (L100~L108)
- **變更後簽章 (After)**: `function bindAttribute(el, name, value)` (L92~L101)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function bindAttribute(el, name, value) {
    if ([null, undefined, false].includes(value) && attributeShouldntBePreservedIfFalsy(name)) {
        el.removeAttribute(name)
    } else {
        if (isBooleanAttr(name)) value = name

        setIfChanged(el, name, value)
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function bindAttribute(el, name, value) {
    if ([null, undefined, false].includes(value) && attributeShouldntBePreservedIfFalsy(name)) {
        el.removeAttribute(name)
    } else {
        if (isBooleanAttr(name)) value = name
        if (isObjectAttr(value)) value = JSON.stringify(value)

        setIfChanged(el, name, value)
    }
}
```

### 🔹 函式: `bindInputValue()`
- **變更前簽章 (Before)**: `function bindInputValue(el, value)` (L41~L81)
- **變更後簽章 (After)**: `function bindInputValue(el, value)` (L41~L73)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function bindInputValue(el, value) {
    if (isRadio(el)) {
        // Set radio value from x-bind:value, if no "value" attribute exists.
        // If there are any initial state values, radio will have a correct
        // "checked" value since x-bind:value is processed before x-model.
        if (el.attributes.value === undefined) {
            el.value = value
        }
    } else if (isCheckbox(el)) {
        // If we are explicitly binding a string to the :value, set the string,
        // If the value is a boolean/array/number/null/undefined, leave it alone, it will be set to "on"
        // automatically.
        if (Number.isInteger(value)) {
            el.value = value
        } else if (! Array.isArray(value) && typeof value !== 'boolean' && ! [null, undefined].includes(value)) {
            el.value = String(value)
        } else {
            if (Array.isArray(value)) {
                el.checked = value.some(val => checkedAttrLooseCompare(val, el.value))
            } else {
                el.checked = !!value
            }
        }
    } else if (el.tagName === 'SELECT') {
        updateSelect(el, value)
    } else if (el.tagName === 'OPTION') {
        // The .value property of an <option> reflects its text content when no
        // value attribute is present, so we must set the attribute explicitly
        // to avoid el.value drifting when sibling directives (e.g. x-text) write text.
        // null/undefined/false removes the attribute, allowing the DOM's text-fallback to apply.
        if (value === null || value === undefined || value === false) {
            if (el.hasAttribute('value')) el.removeAttribute('value')
        } else {
            setIfChanged(el, 'value', value)
        }
    } else {
        if (el.value === value) return

        el.value = value === undefined ? '' : value
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function bindInputValue(el, value) {
    if (isRadio(el)) {
        // Set radio value from x-bind:value, if no "value" attribute exists.
        // If there are any initial state values, radio will have a correct
        // "checked" value since x-bind:value is processed before x-model.
        if (el.attributes.value === undefined) {
            el.value = value
        }
    } else if (isCheckbox(el)) {
        // If we are explicitly binding a string to the :value, set the string,
        // If the value is a boolean/array/number/null/undefined, leave it alone, it will be set to "on"
        // automatically.
        if (Number.isInteger(value)) {
            el.value = value
        } else if (! Array.isArray(value) && typeof value !== 'boolean' && ! [null, undefined].includes(value)) {
            el.value = String(value)
        } else {
            if (Array.isArray(value)) {
                el.checked = value.some(val => checkedAttrLooseCompare(val, el.value))
            } else {
                el.checked = !!value
            }
        }
    } else if (el.tagName === 'SELECT') {
        updateSelect(el, value)
    } else if (el.tagName === 'OPTION') {
        bindAttribute(el, 'value', value)
    } else {
        if (el.value === value) return

        el.value = value === undefined ? '' : value
    }
}
```


---

### 🔹 Commit #13: `e95ea108`
- **完整 Hash**: `e95ea108a27a328f9a3381927efef0826020a5ca`
- **說明 (Ground Truth)**: Fix `x-bind:value` on `<option>` losing attribute when value is an empty string
- **變更檔案數**: 1

#### 📄 檔案: `packages/alpinejs/src/utils/bind.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:29, E:26, A:0) ➔ After(N:29, E:27, A:0)
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
  • + [新增呼叫邊] `bindInputValue` ──[CALLS [guard: (isRadio(el))]]──> `setIfChanged`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `bindInputValue()`
- **變更前簽章 (Before)**: `function bindInputValue(el, value)` (L41~L71)
- **變更後簽章 (After)**: `function bindInputValue(el, value)` (L41~L81)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function bindInputValue(el, value) {
    if (isRadio(el)) {
        // Set radio value from x-bind:value, if no "value" attribute exists.
        // If there are any initial state values, radio will have a correct
        // "checked" value since x-bind:value is processed before x-model.
        if (el.attributes.value === undefined) {
            el.value = value
        }
    } else if (isCheckbox(el)) {
        // If we are explicitly binding a string to the :value, set the string,
        // If the value is a boolean/array/number/null/undefined, leave it alone, it will be set to "on"
        // automatically.
        if (Number.isInteger(value)) {
            el.value = value
        } else if (! Array.isArray(value) && typeof value !== 'boolean' && ! [null, undefined].includes(value)) {
            el.value = String(value)
        } else {
            if (Array.isArray(value)) {
                el.checked = value.some(val => checkedAttrLooseCompare(val, el.value))
            } else {
                el.checked = !!value
            }
        }
    } else if (el.tagName === 'SELECT') {
        updateSelect(el, value)
    } else {
        if (el.value === value) return

        el.value = value === undefined ? '' : value
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function bindInputValue(el, value) {
    if (isRadio(el)) {
        // Set radio value from x-bind:value, if no "value" attribute exists.
        // If there are any initial state values, radio will have a correct
        // "checked" value since x-bind:value is processed before x-model.
        if (el.attributes.value === undefined) {
            el.value = value
        }
    } else if (isCheckbox(el)) {
        // If we are explicitly binding a string to the :value, set the string,
        // If the value is a boolean/array/number/null/undefined, leave it alone, it will be set to "on"
        // automatically.
        if (Number.isInteger(value)) {
            el.value = value
        } else if (! Array.isArray(value) && typeof value !== 'boolean' && ! [null, undefined].includes(value)) {
            el.value = String(value)
        } else {
            if (Array.isArray(value)) {
                el.checked = value.some(val => checkedAttrLooseCompare(val, el.value))
            } else {
                el.checked = !!value
            }
        }
    } else if (el.tagName === 'SELECT') {
        updateSelect(el, value)
    } else if (el.tagName === 'OPTION') {
        // The .value property of an <option> reflects its text content when no
        // value attribute is present, so we must set the attribute explicitly
        // to avoid el.value drifting when sibling directives (e.g. x-text) write text.
        // null/undefined/false removes the attribute, allowing the DOM's text-fallback to apply.
        if (value === null || value === undefined || value === false) {
            if (el.hasAttribute('value')) el.removeAttribute('value')
        } else {
            setIfChanged(el, 'value', value)
        }
    } else {
        if (el.value === value) return

        el.value = value === undefined ? '' : value
    }
}
```


---

### 🔹 Commit #14: `3c64d45d`
- **完整 Hash**: `3c64d45d415e57f53d150267da161424056929c0`
- **說明 (Ground Truth)**: fix: sync x-model select value after x-for renders options (#4769)
- **變更檔案數**: 1

#### 📄 檔案: `packages/alpinejs/src/directives/x-model.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:37, E:46, A:0) ➔ After(N:37, E:46, A:0)
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

### 🔹 函式: `directive:model()`
- **變更前簽章 (Before)**: `directive:model(el, { modifiers, expression }, { effect, cleanup })` (L10~L193)
- **變更後簽章 (After)**: `directive:model(el, { modifiers, expression }, { effect, cleanup })` (L10~L203)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(el, { modifiers, expression }, { effect, cleanup }) => {
    let scopeTarget = el

    if (modifiers.includes('parent')) {
        scopeTarget = findClosest(el, (element) => element !== el)
    }

    let evaluateGet = evaluateLater(scopeTarget, expression)
    let evaluateSet

    if (typeof expression === 'string') {
        evaluateSet = evaluateLater(scopeTarget, `${expression} = __placeholder`)
    } else if (typeof expression === 'function' && typeof expression() === 'string') {
        evaluateSet = evaluateLater(scopeTarget, `${expression()} = __placeholder`)
    } else {
        evaluateSet = () => {}
    }

    let getValue = () => {
        let result

        evaluateGet(value => result = value)

        return isGetterSetter(result) ? result.get() : result
    }

    let setValue = value => {
        let result

        evaluateGet(value => result = value)

        if (isGetterSetter(result)) {
            result.set(value)
        } else {
            evaluateSet(() => {}, {
                scope: { '__placeholder': value }
            })
        }
    }

    if (typeof expression === 'string' && el.type === 'radio') {
        // Radio buttons only work properly when they share a name attribute.
        // People might assume we take care of that for them, because
        // they already set a shared "x-model" attribute.
        mutateDom(() => {
            if (! el.hasAttribute('name')) el.setAttribute('name', expression)
        })
    }

    // Check for explicit event modifiers (.change, .blur, .enter)
    let hasChangeModifier = modifiers.includes('change') || modifiers.includes('lazy')
    let hasBlurModifier = modifiers.includes('blur')
    let hasEnterModifier = modifiers.includes('enter')
    let hasExplicitEventModifiers = hasChangeModifier || hasBlurModifier || hasEnterModifier

    let removeListener

    if (isCloning) {
        removeListener = () => {}
    } else if (hasExplicitEventModifiers) {
        // When explicit event modifiers are present, attach listeners for each specified event
        let listeners = []

        let syncValue = (e) => setValue(getInputValue(el, modifiers, e, getValue()))

        if (hasChangeModifier) {
            listeners.push(on(el, 'change', modifiers, syncValue))
        }

        if (hasBlurModifier) {
            listeners.push(on(el, 'blur', modifiers, syncValue))

            // The browser fires "submit" before "blur", so if this input
            // is inside a form, the model value would be stale when the
            // submit handler runs. Register a pending update on the form
            // so it can be flushed before submit handlers execute.
            if (el.form) {
                let form = el.form
                let syncCallback = () => syncValue({ target: el })

                if (!form._x_pendingModelUpdates) form._x_pendingModelUpdates = []
                form._x_pendingModelUpdates.push(syncCallback)

                cleanup(() => {
                    if (form._x_pendingModelUpdates) {
                        form._x_pendingModelUpdates.splice(form._x_pendingModelUpdates.indexOf(syncCallback), 1)
                    }
                })
            }
        }

        if (hasEnterModifier) {
            listeners.push(on(el, 'keydown', modifiers, (e) => {
                if (e.key === 'Enter') syncValue(e)
            }))
        }

        removeListener = () => listeners.forEach(remove => remove())
    } else {
        // Default behavior: select, checkbox, radio use 'change', others use 'input'
        let event = (el.tagName.toLowerCase() === 'select')
            || ['checkbox', 'radio'].includes(el.type)
                ? 'change' : 'input'

        removeListener = on(el, event, modifiers, (e) => {
            setValue(getInputValue(el, modifiers, e, getValue()))
        })
    }

    if (modifiers.includes('fill'))
        if ([undefined, null, ''].includes(getValue())
            || (isCheckbox(el) && Array.isArray(getValue()))
            || (el.tagName.toLowerCase() === 'select' && el.multiple)) {
        setValue(
            getInputValue(el, modifiers, { target: el }, getValue())
        );
    }

    // Register the listener removal callback on the element, so that
    // in addition to the cleanup function, x-modelable may call it.
    // Also, make this a keyed object if we decide to reintroduce
    // "named modelables" some time in a future Alpine version.
    if (! el._x_removeModelListeners) el._x_removeModelListeners = {}
    el._x_removeModelListeners['default'] = removeListener

    cleanup(() => el._x_removeModelListeners['default']())

    // If the input/select/textarea element is linked to a form
    // we listen for the reset event on the parent form (the event
    // does not trigger on the single inputs) and update
    // on nextTick so the page doesn't end up out of sync
    if (el.form) {
        let removeResetListener = on(el.form, 'reset', [], (e) => {
            nextTick(() => el._x_model && el._x_model.set(getInputValue(el, modifiers, { target: el }, getValue())))
        })
        cleanup(() => removeResetListener())
    }

    // Allow programmatic overriding of x-model.
    el._x_model = {
        get() {
            return getValue()
        },
        set(value) {
            setValue(value)
        },
        setWithModifiers: addDebounceOrThrottle(modifiers, setValue),
    }

    el._x_forceModelUpdate = (value) => {
        // If nested model key is undefined, set the default value to empty string.
        if (value === undefined && typeof expression === 'string' && expression.match(/\./)) value = ''

        mutateDom(() => {
            if (isCheckbox(el)) {
                if (Array.isArray(value)) {
                    el.checked = value.some(val => val == el.value)
                } else {
                    el.checked = !!value
                }
            } else if (isRadio(el)) {
                if (typeof value === 'boolean') {
                    el.checked = safeParseBoolean(el.value) === value
                } else {
                    el.checked = el.value == value
                }
            } else {
                bind(el, 'value', value)
            }
        })
    }

    effect(() => {
        // We need to make sure we're always "getting" the value up front,
        // so that we don't run into a situation where because of the early
        // the reactive value isn't gotten and therefore disables future reactions.
        let value = getValue()

        // Don't modify the value of the input if it's focused.
        if (modifiers.includes('unintrusive') && document.activeElement.isSameNode(el)) return

        el._x_forceModelUpdate(value)
    })
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(el, { modifiers, expression }, { effect, cleanup }) => {
    let scopeTarget = el

    if (modifiers.includes('parent')) {
        scopeTarget = findClosest(el, (element) => element !== el)
    }

    let evaluateGet = evaluateLater(scopeTarget, expression)
    let evaluateSet

    if (typeof expression === 'string') {
        evaluateSet = evaluateLater(scopeTarget, `${expression} = __placeholder`)
    } else if (typeof expression === 'function' && typeof expression() === 'string') {
        evaluateSet = evaluateLater(scopeTarget, `${expression()} = __placeholder`)
    } else {
        evaluateSet = () => {}
    }

    let getValue = () => {
        let result

        evaluateGet(value => result = value)

        return isGetterSetter(result) ? result.get() : result
    }

    let setValue = value => {
        let result

        evaluateGet(value => result = value)

        if (isGetterSetter(result)) {
            result.set(value)
        } else {
            evaluateSet(() => {}, {
                scope: { '__placeholder': value }
            })
        }
    }

    if (typeof expression === 'string' && el.type === 'radio') {
        // Radio buttons only work properly when they share a name attribute.
        // People might assume we take care of that for them, because
        // they already set a shared "x-model" attribute.
        mutateDom(() => {
            if (! el.hasAttribute('name')) el.setAttribute('name', expression)
        })
    }

    // Check for explicit event modifiers (.change, .blur, .enter)
    let hasChangeModifier = modifiers.includes('change') || modifiers.includes('lazy')
    let hasBlurModifier = modifiers.includes('blur')
    let hasEnterModifier = modifiers.includes('enter')
    let hasExplicitEventModifiers = hasChangeModifier || hasBlurModifier || hasEnterModifier

    let removeListener

    if (isCloning) {
        removeListener = () => {}
    } else if (hasExplicitEventModifiers) {
        // When explicit event modifiers are present, attach listeners for each specified event
        let listeners = []

        let syncValue = (e) => setValue(getInputValue(el, modifiers, e, getValue()))

        if (hasChangeModifier) {
            listeners.push(on(el, 'change', modifiers, syncValue))
        }

        if (hasBlurModifier) {
            listeners.push(on(el, 'blur', modifiers, syncValue))

            // The browser fires "submit" before "blur", so if this input
            // is inside a form, the model value would be stale when the
            // submit handler runs. Register a pending update on the form
            // so it can be flushed before submit handlers execute.
            if (el.form) {
                let form = el.form
                let syncCallback = () => syncValue({ target: el })

                if (!form._x_pendingModelUpdates) form._x_pendingModelUpdates = []
                form._x_pendingModelUpdates.push(syncCallback)

                cleanup(() => {
                    if (form._x_pendingModelUpdates) {
                        form._x_pendingModelUpdates.splice(form._x_pendingModelUpdates.indexOf(syncCallback), 1)
                    }
                })
            }
        }

        if (hasEnterModifier) {
            listeners.push(on(el, 'keydown', modifiers, (e) => {
                if (e.key === 'Enter') syncValue(e)
            }))
        }

        removeListener = () => listeners.forEach(remove => remove())
    } else {
        // Default behavior: select, checkbox, radio use 'change', others use 'input'
        let event = (el.tagName.toLowerCase() === 'select')
            || ['checkbox', 'radio'].includes(el.type)
                ? 'change' : 'input'

        removeListener = on(el, event, modifiers, (e) => {
            setValue(getInputValue(el, modifiers, e, getValue()))
        })
    }

    if (modifiers.includes('fill'))
        if ([undefined, null, ''].includes(getValue())
            || (isCheckbox(el) && Array.isArray(getValue()))
            || (el.tagName.toLowerCase() === 'select' && el.multiple)) {
        setValue(
            getInputValue(el, modifiers, { target: el }, getValue())
        );
    }

    // Register the listener removal callback on the element, so that
    // in addition to the cleanup function, x-modelable may call it.
    // Also, make this a keyed object if we decide to reintroduce
    // "named modelables" some time in a future Alpine version.
    if (! el._x_removeModelListeners) el._x_removeModelListeners = {}
    el._x_removeModelListeners['default'] = removeListener

    cleanup(() => el._x_removeModelListeners['default']())

    // If the input/select/textarea element is linked to a form
    // we listen for the reset event on the parent form (the event
    // does not trigger on the single inputs) and update
    // on nextTick so the page doesn't end up out of sync
    if (el.form) {
        let removeResetListener = on(el.form, 'reset', [], (e) => {
            nextTick(() => el._x_model && el._x_model.set(getInputValue(el, modifiers, { target: el }, getValue())))
        })
        cleanup(() => removeResetListener())
    }

    // Allow programmatic overriding of x-model.
    el._x_model = {
        get() {
            return getValue()
        },
        set(value) {
            setValue(value)
        },
        setWithModifiers: addDebounceOrThrottle(modifiers, setValue),
    }

    el._x_forceModelUpdate = (value) => {
        // If nested model key is undefined, set the default value to empty string.
        if (value === undefined && typeof expression === 'string' && expression.match(/\./)) value = ''

        mutateDom(() => {
            if (isCheckbox(el)) {
                if (Array.isArray(value)) {
                    el.checked = value.some(val => val == el.value)
                } else {
                    el.checked = !!value
                }
            } else if (isRadio(el)) {
                if (typeof value === 'boolean') {
                    el.checked = safeParseBoolean(el.value) === value
                } else {
                    el.checked = el.value == value
                }
            } else {
                bind(el, 'value', value)
            }
        })
    }

    if (el.tagName === 'SELECT') {
        let observer = new MutationObserver(() => {
            el._x_forceModelUpdate(getValue())
        })

        observer.observe(el, { childList: true })

        cleanup(() => observer.disconnect())
    }

    effect(() => {
        // We need to make sure we're always "getting" the value up front,
        // so that we don't run into a situation where because of the early
        // the reactive value isn't gotten and therefore disables future reactions.
        let value = getValue()

        // Don't modify the value of the input if it's focused.
        if (modifiers.includes('unintrusive') && document.activeElement.isSameNode(el)) return

        el._x_forceModelUpdate(value)
    })
}
```


---

### 🔹 Commit #15: `f23defeb`
- **完整 Hash**: `f23defebab9f7e5a2d6262cd46b84f2e08a95439`
- **說明 (Ground Truth)**: Fix x-if and x-for content duplicating during morph (#4785)
- **變更檔案數**: 3

#### 📄 檔案: `packages/alpinejs/src/directives/x-for.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:25, E:22, A:0) ➔ After(N:24, E:14, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 0, -Edges: 8, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `directive:for` (FUNCTION_DEF)
  • - [移除呼叫邊] `directive:for` ──[CALLS]──> `parseForExpression`
  • - [移除呼叫邊] `directive:for` ──[CALLS]──> `evaluateLater (External/Unresolved)`
  • - [移除呼叫邊] `directive:for` ──[CALLS]──> `effect (External/Unresolved)`
  • - [移除呼叫邊] `directive:for` ──[CALLS]──> `loop`
  • - [移除呼叫邊] `directive:for` ──[CALLS]──> `cleanup (External/Unresolved)`
  • - [移除呼叫邊] `directive:for` ──[CALLS]──> `mutateDom (External/Unresolved)`
  • - [移除呼叫邊] `directive:for` ──[CALLS]──> `destroyTree (External/Unresolved)`
  • - [移除呼叫邊] `loop` ──[CALLS]──> `skipDuringClone (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `loop()`
- **變更前簽章 (Before)**: `function loop(templateEl, iteratorNames, evaluateItems, evaluateKey)` (L44~L131)
- **變更後簽章 (After)**: `function loop(templateEl, iteratorNames, evaluateItems, evaluateKey)` (L45~L140)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function loop(templateEl, iteratorNames, evaluateItems, evaluateKey) {
    evaluateItems(items => {
        // Prepare yourself. There's a lot going on here. Take heart,
        // every bit of complexity in this function was added for
        // the purpose of making Alpine fast with large datas.

        // Support number literals. Ex: x-for="i in 100"
        if (isNumeric(items))
            items = Array.from({ length: items }, (_, i) => i + 1)

        if (items === undefined || items === null) items = []

        // Support Set and Map objects by converting to arrays.
        if (items instanceof Set) items = Array.from(items)
        if (items instanceof Map) items = Array.from(items)

        // In order to remove elements early we need to generate the key/scope
        // pairs up front, moving existing elements from the old lookup to the
        // new. This leaves only the elements to be removed in the old lookup.
        let oldLookup = templateEl._x_lookup
        let lookup = new Map()
        templateEl._x_lookup = lookup

        let hasStringKeys = isObject(items)
        let scopeEntries = Object.entries(items).map(([index, item]) => {
            if (! hasStringKeys) index = parseInt(index)
            let scope = getIterationScopeVariables(iteratorNames, item, index, items)
            let key
            evaluateKey(innerKey => {
                if (typeof innerKey === 'object')
                    warn('x-for key cannot be an object, it must be a string or an integer', templateEl)

                if (oldLookup.has(innerKey)) {
                    lookup.set(innerKey, oldLookup.get(innerKey))
                    oldLookup.delete(innerKey)
                }
                key = innerKey
            }, { scope: { index, ...scope } })
            return [key, scope]
        })

        mutateDom(() => {
            oldLookup.forEach((el) => {
                destroyTree(el)
                el.remove()
            })

            let added = new Set()

            let prev = templateEl
            scopeEntries.forEach(([key, scope]) => {
                if (lookup.has(key)) {
                    let el = lookup.get(key)
                    el._x_refreshXForScope(scope)

                    if (prev.nextElementSibling !== el) {
                        if (prev.nextElementSibling)
                            el.replaceWith(prev.nextElementSibling)
                        prev.after(el)
                    }
                    prev = el

                    if (el._x_currentIfEl) {
                        if (el.nextElementSibling !== el._x_currentIfEl)
                            prev.after(el._x_currentIfEl)
                        prev = el._x_currentIfEl
                    }
                    return
                }

                if (templateEl.content.children.length > 1)
                    warn('x-for templates require a single root element, additional elements will be ignored.', templateEl)

                let clone = document.importNode(templateEl.content, true).firstElementChild
                let reactiveScope = reactive(scope)
                addScopeToNode(clone, reactiveScope, templateEl)
                clone._x_refreshXForScope = refreshScope(reactiveScope)

                lookup.set(key, clone)
                added.add(clone)

                prev.after(clone)
                prev = clone
            })
            skipDuringClone(() => added.forEach(clone => initTree(clone)))()
        })
    })
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function loop(templateEl, iteratorNames, evaluateItems, evaluateKey) {
    evaluateItems(items => {
        // Prepare yourself. There's a lot going on here. Take heart,
        // every bit of complexity in this function was added for
        // the purpose of making Alpine fast with large datas.

        // Support number literals. Ex: x-for="i in 100"
        if (isNumeric(items))
            items = Array.from({ length: items }, (_, i) => i + 1)

        if (items === undefined || items === null) items = []

        // Support Set and Map objects by converting to arrays.
        if (items instanceof Set) items = Array.from(items)
        if (items instanceof Map) items = Array.from(items)

        // In order to remove elements early we need to generate the key/scope
        // pairs up front, moving existing elements from the old lookup to the
        // new. This leaves only the elements to be removed in the old lookup.
        let oldLookup = templateEl._x_lookup
        let lookup = new Map()
        templateEl._x_lookup = lookup

        let hasStringKeys = isObject(items)
        let scopeEntries = Object.entries(items).map(([index, item]) => {
            if (! hasStringKeys) index = parseInt(index)
            let scope = getIterationScopeVariables(iteratorNames, item, index, items)
            let key
            evaluateKey(innerKey => {
                if (typeof innerKey === 'object')
                    warn('x-for key cannot be an object, it must be a string or an integer', templateEl)

                if (oldLookup.has(innerKey)) {
                    lookup.set(innerKey, oldLookup.get(innerKey))
                    oldLookup.delete(innerKey)
                }
                key = innerKey
            }, { scope: { index, ...scope } })
            return [key, scope]
        })

        mutateDom(() => {
            oldLookup.forEach((el) => {
                destroyTree(el)
                el.remove()
            })

            let added = new Set()

            let prev = templateEl
            scopeEntries.forEach(([key, scope]) => {
                if (lookup.has(key)) {
                    let el = lookup.get(key)
                    el._x_refreshXForScope(scope)

                    if (prev.nextElementSibling !== el) {
                        if (prev.nextElementSibling)
                            el.replaceWith(prev.nextElementSibling)
                        prev.after(el)
                    }
                    prev = el

                    if (el._x_currentIfEl) {
                        if (el.nextElementSibling !== el._x_currentIfEl)
                            prev.after(el._x_currentIfEl)
                        prev = el._x_currentIfEl
                    }
                    return
                }

                if (templateEl.content.children.length > 1)
                    warn('x-for templates require a single root element, additional elements will be ignored.', templateEl)

                let clone = document.importNode(templateEl.content, true).firstElementChild
                let reactiveScope = reactive(scope)
                addScopeToNode(clone, reactiveScope, templateEl)
                clone._x_refreshXForScope = refreshScope(reactiveScope)

                lookup.set(key, clone)
                added.add(clone)

                prev.after(clone)
                prev = clone
            })
            added.forEach(clone => initTree(clone))

            // Mark the last rendered element so morph can skip
            // past these items instead of trying to diff them...
            if (prev !== templateEl) {
                templateEl._x_lastRenderedEl = prev
            } else {
                delete templateEl._x_lastRenderedEl
            }
        })
    })
}
```


#### 📄 檔案: `packages/alpinejs/src/directives/x-if.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:15, E:13, A:0) ➔ After(N:14, E:5, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 3, +Edges: 3, -Edges: 11, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `hide` (FUNCTION_DEF)
  • + [新增節點] `show` (FUNCTION_DEF)
  • - [移除節點] `directive:if` (FUNCTION_DEF)
  • - [移除節點] `hide` (FUNCTION_DEF)
  • - [移除節點] `show` (FUNCTION_DEF)
  • + [新增呼叫邊] `show` ──[CALLS [guard: (el._x_currentIfEl)]]──> `addScopeToNode (External/Unresolved)`
  • + [新增呼叫邊] `show` ──[CALLS [guard: (el._x_currentIfEl)]]──> `mutateDom (External/Unresolved)`
  • + [新增呼叫邊] `show` ──[CALLS]──> `initTree (External/Unresolved)`
  • - [移除呼叫邊] `directive:if` ──[CALLS]──> `warn (External/Unresolved)`
  • - [移除呼叫邊] `directive:if` ──[CALLS]──> `evaluateLater (External/Unresolved)`
  • - [移除呼叫邊] `directive:if` ──[CALLS]──> `effect (External/Unresolved)`
  • - [移除呼叫邊] `directive:if` ──[CALLS]──> `evaluate (External/Unresolved)`
  • - [移除呼叫邊] `directive:if` ──[CALLS]──> `show`
  • - [移除呼叫邊] `directive:if` ──[CALLS]──> `hide`
  • - [移除呼叫邊] `directive:if` ──[CALLS]──> `cleanup (External/Unresolved)`
  • _... 以及其餘 4 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_x_undoIf()`
- **變更前簽章 (Before)**: `_x_undoIf()` (L30~L38)
- **變更後簽章 (After)**: `_x_undoIf()` (L33~L42)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
            mutateDom(() => {
                destroyTree(clone)

                clone.remove()
            })

            delete el._x_currentIfEl
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
            mutateDom(() => {
                destroyTree(clone)

                clone.remove()
            })

            delete el._x_currentIfEl
            delete el._x_lastRenderedEl
        }
```


#### 📄 檔案: `packages/morph/src/morph.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:43, E:17, A:5) ➔ After(N:43, E:17, A:5)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#container** `(Control)`
  🌲 **#hostDiv** `(Control)`
  🌲 **#template** `(Control)`
  🌲 **#toContainer** `(Control)`
  🌲 **#toEl** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `patchChildren()`
- **變更前簽章 (Before)**: `patchChildren(from, to)` (L195~L398)
- **變更後簽章 (After)**: `patchChildren(from, to)` (L195~L405)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function(from, to) {
        let fromKeys = context.keyToMap(from.children)
        let fromKeyHoldovers = {}

        let currentTo = getFirstNode(to)
        let currentFrom = getFirstNode(from)

        while (currentTo) {
            // If the "from" element has a dynamically bound "id" (x-bind:id="..."),
            // Let's transfer it to the "to" element so that there isn't a key mismatch...
            seedingMatchingId(currentTo, currentFrom)

            let toKey = context.getKey(currentTo)
            let fromKey = context.getKey(currentFrom)

            if (context.skipUntilCondition) {
                let fromDone = ! currentFrom || context.skipUntilCondition(currentFrom)
                let toDone   = ! currentTo   || context.skipUntilCondition(currentTo)
                if (fromDone && toDone) {
                    context.skipUntilCondition = null
                } else {
                    if (! fromDone) currentFrom = currentFrom && getNextSibling(from, currentFrom)
                    if (! toDone)   currentTo   = currentTo   && getNextSibling(to, currentTo)
                    continue
                }
            }

            // Add new elements...
            if (! currentFrom) {
                if (toKey && fromKeyHoldovers[toKey]) {
                    // Add element (from key)...
                    let holdover = fromKeyHoldovers[toKey]

                    from.appendChild(holdover)

                    currentFrom = holdover
                    fromKey = context.getKey(currentFrom)
                } else {
                    if(! shouldSkip(context.adding, currentTo)) {
                        // Add element...
                        let clone = currentTo.cloneNode(true)

                        from.appendChild(clone)

                        context.added(clone)
                    }

                    currentTo = getNextSibling(to, currentTo)

                    continue
                }
            }

            // Handle conditional markers (presumably added by backends like Livewire)...
            let isIf = node => node && node.nodeType === 8 && node.textContent === '[if BLOCK]><![endif]'
            let isEnd = node => node && node.nodeType === 8 && node.textContent === '[if ENDBLOCK]><![endif]'

            if (isIf(currentTo) && isIf(currentFrom)) {
                let nestedIfCount = 0

                let fromBlockStart = currentFrom

                while (currentFrom) {
                    let next = getNextSibling(from, currentFrom)

                    if (isIf(next)) {
                        nestedIfCount++
                    } else if (isEnd(next) && nestedIfCount > 0) {
                        nestedIfCount--
                    } else if (isEnd(next) && nestedIfCount === 0) {
                        currentFrom = next

                        break;
                    }

                    currentFrom = next
                }

                let fromBlockEnd = currentFrom

                nestedIfCount = 0

                let toBlockStart = currentTo

                while (currentTo) {
                    let next = getNextSibling(to, currentTo)

                    if (isIf(next)) {
                        nestedIfCount++
                    } else if (isEnd(next) && nestedIfCount > 0) {
                        nestedIfCount--
                    } else if (isEnd(next) && nestedIfCount === 0) {
                        currentTo = next

                        break;
                    }

                    currentTo = next
                }

                let toBlockEnd = currentTo

                let fromBlock = new Block(fromBlockStart, fromBlockEnd)
                let toBlock = new Block(toBlockStart, toBlockEnd)

                context.patchChildren(fromBlock, toBlock)

                continue
            }

            // Lookaheads should only apply to non-text-or-comment elements...
            if (currentFrom.nodeType === 1 && context.lookahead && ! currentFrom.isEqualNode(currentTo)) {
                let nextToElementSibling = getNextSibling(to, currentTo)

                let found = false

                while (! found && nextToElementSibling) {
                    if (nextToElementSibling.nodeType === 1 && currentFrom.isEqualNode(nextToElementSibling)) {
                        found = true; // This ";" needs to be here...

                        currentFrom = context.addNodeBefore(from, currentTo, currentFrom)

                        fromKey = context.getKey(currentFrom)
                    }

                    nextToElementSibling = getNextSibling(to, nextToElementSibling)
                }
            }

            if (toKey !== fromKey) {
                if (! toKey && fromKey) {
                    // No "to" key...
                    fromKeyHoldovers[fromKey] = currentFrom; // This ";" needs to be here...
                    currentFrom = context.addNodeBefore(from, currentTo, currentFrom)
                    fromKeyHoldovers[fromKey].remove()
                    currentFrom = getNextSibling(from, currentFrom)
                    currentTo = getNextSibling(to, currentTo)

                    continue
                }

                if (toKey && ! fromKey) {
                    if (fromKeys[toKey]) {
                        // No "from" key...
                        currentFrom.replaceWith(fromKeys[toKey])
                        currentFrom = fromKeys[toKey]
                        fromKey = context.getKey(currentFrom)
                    }
                }

                if (toKey && fromKey) {
                    let fromKeyNode = fromKeys[toKey]

                    if (fromKeyNode) {
                        // Move "from" key...
                        fromKeyHoldovers[fromKey] = currentFrom
                        currentFrom.replaceWith(fromKeyNode)
                        currentFrom = fromKeyNode
                        fromKey = context.getKey(currentFrom)
                    } else {
                        // Swap elements with keys...
                        fromKeyHoldovers[fromKey] = currentFrom; // This ";" needs to be here...
                        currentFrom = context.addNodeBefore(from, currentTo, currentFrom)
                        fromKeyHoldovers[fromKey].remove()
                        currentFrom = getNextSibling(from, currentFrom)
                        currentTo = getNextSibling(to, currentTo)

                        continue
                    }
                }
            }

            // Get next from sibling before patching in case the node is replaced
            let currentFromNext = currentFrom && getNextSibling(from, currentFrom) //dom.next(from, fromChildren, currentFrom))

            // Patch elements
            context.patch(currentFrom, currentTo)

            currentTo = currentTo && getNextSibling(to, currentTo) // dom.next(from, toChildren, currentTo))

            currentFrom = currentFromNext
        }

        // Cleanup extra forms.
        let removals = []

        // We need to collect the "removals" first before actually
        // removing them so we don't mess with the order of things.
        while (currentFrom) {
            if (! shouldSkip(context.removing, currentFrom)) removals.push(currentFrom)

            // currentFrom = dom.next(fromChildren, currentFrom)
            currentFrom = getNextSibling(from, currentFrom)
        }

        // Now we can do the actual removals.
        while (removals.length) {
            let domForRemoval = removals.shift()

            domForRemoval.remove()

            context.removed(domForRemoval)
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function(from, to) {
        let fromKeys = context.keyToMap(from.children)
        let fromKeyHoldovers = {}

        let currentTo = getFirstNode(to)
        let currentFrom = getFirstNode(from)

        while (currentTo) {
            // If the "from" element has a dynamically bound "id" (x-bind:id="..."),
            // Let's transfer it to the "to" element so that there isn't a key mismatch...
            seedingMatchingId(currentTo, currentFrom)

            let toKey = context.getKey(currentTo)
            let fromKey = context.getKey(currentFrom)

            if (context.skipUntilCondition) {
                let fromDone = ! currentFrom || context.skipUntilCondition(currentFrom)
                let toDone   = ! currentTo   || context.skipUntilCondition(currentTo)
                if (fromDone && toDone) {
                    context.skipUntilCondition = null
                } else {
                    if (! fromDone) currentFrom = currentFrom && getNextSibling(from, currentFrom)
                    if (! toDone)   currentTo   = currentTo   && getNextSibling(to, currentTo)
                    continue
                }
            }

            // Add new elements...
            if (! currentFrom) {
                if (toKey && fromKeyHoldovers[toKey]) {
                    // Add element (from key)...
                    let holdover = fromKeyHoldovers[toKey]

                    from.appendChild(holdover)

                    currentFrom = holdover
                    fromKey = context.getKey(currentFrom)
                } else {
                    if(! shouldSkip(context.adding, currentTo)) {
                        // Add element...
                        let clone = currentTo.cloneNode(true)

                        from.appendChild(clone)

                        context.added(clone)
                    }

                    currentTo = getNextSibling(to, currentTo)

                    continue
                }
            }

            // Handle conditional markers (presumably added by backends like Livewire)...
            let isIf = node => node && node.nodeType === 8 && node.textContent === '[if BLOCK]><![endif]'
            let isEnd = node => node && node.nodeType === 8 && node.textContent === '[if ENDBLOCK]><![endif]'

            if (isIf(currentTo) && isIf(currentFrom)) {
                let nestedIfCount = 0

                let fromBlockStart = currentFrom

                while (currentFrom) {
                    let next = getNextSibling(from, currentFrom)

                    if (isIf(next)) {
                        nestedIfCount++
                    } else if (isEnd(next) && nestedIfCount > 0) {
                        nestedIfCount--
                    } else if (isEnd(next) && nestedIfCount === 0) {
                        currentFrom = next

                        break;
                    }

                    currentFrom = next
                }

                let fromBlockEnd = currentFrom

                nestedIfCount = 0

                let toBlockStart = currentTo

                while (currentTo) {
                    let next = getNextSibling(to, currentTo)

                    if (isIf(next)) {
                        nestedIfCount++
                    } else if (isEnd(next) && nestedIfCount > 0) {
                        nestedIfCount--
                    } else if (isEnd(next) && nestedIfCount === 0) {
                        currentTo = next

                        break;
                    }

                    currentTo = next
                }

                let toBlockEnd = currentTo

                let fromBlock = new Block(fromBlockStart, fromBlockEnd)
                let toBlock = new Block(toBlockStart, toBlockEnd)

                context.patchChildren(fromBlock, toBlock)

                continue
            }

            // Lookaheads should only apply to non-text-or-comment elements...
            if (currentFrom.nodeType === 1 && context.lookahead && ! currentFrom.isEqualNode(currentTo)) {
                let nextToElementSibling = getNextSibling(to, currentTo)

                let found = false

                while (! found && nextToElementSibling) {
                    if (nextToElementSibling.nodeType === 1 && currentFrom.isEqualNode(nextToElementSibling)) {
                        found = true; // This ";" needs to be here...

                        currentFrom = context.addNodeBefore(from, currentTo, currentFrom)

                        fromKey = context.getKey(currentFrom)
                    }

                    nextToElementSibling = getNextSibling(to, nextToElementSibling)
                }
            }

            if (toKey !== fromKey) {
                if (! toKey && fromKey) {
                    // No "to" key...
                    fromKeyHoldovers[fromKey] = currentFrom; // This ";" needs to be here...
                    currentFrom = context.addNodeBefore(from, currentTo, currentFrom)
                    fromKeyHoldovers[fromKey].remove()
                    currentFrom = getNextSibling(from, currentFrom)
                    currentTo = getNextSibling(to, currentTo)

                    continue
                }

                if (toKey && ! fromKey) {
                    if (fromKeys[toKey]) {
                        // No "from" key...
                        currentFrom.replaceWith(fromKeys[toKey])
                        currentFrom = fromKeys[toKey]
                        fromKey = context.getKey(currentFrom)
                    }
                }

                if (toKey && fromKey) {
                    let fromKeyNode = fromKeys[toKey]

                    if (fromKeyNode) {
                        // Move "from" key...
                        fromKeyHoldovers[fromKey] = currentFrom
                        currentFrom.replaceWith(fromKeyNode)
                        currentFrom = fromKeyNode
                        fromKey = context.getKey(currentFrom)
                    } else {
                        // Swap elements with keys...
                        fromKeyHoldovers[fromKey] = currentFrom; // This ";" needs to be here...
                        currentFrom = context.addNodeBefore(from, currentTo, currentFrom)
                        fromKeyHoldovers[fromKey].remove()
                        currentFrom = getNextSibling(from, currentFrom)
                        currentTo = getNextSibling(to, currentTo)

                        continue
                    }
                }
            }

            // Get next from sibling before patching in case the node is replaced
            let currentFromNext = currentFrom && getNextSibling(from, currentFrom) //dom.next(from, fromChildren, currentFrom))

            // Patch elements
            context.patch(currentFrom, currentTo)

            // Directives like x-if and x-for insert sibling elements
            // that they manage. Skip past them — they'll be handled
            // by Alpine's reactivity after the morph completes...
            if (currentFrom._x_lastRenderedEl) {
                currentFromNext = getNextSibling(from, currentFrom._x_lastRenderedEl)
            }

            currentTo = currentTo && getNextSibling(to, currentTo) // dom.next(from, toChildren, currentTo))

            currentFrom = currentFromNext
        }

        // Cleanup extra forms.
        let removals = []

        // We need to collect the "removals" first before actually
        // removing them so we don't mess with the order of things.
        while (currentFrom) {
            if (! shouldSkip(context.removing, currentFrom)) removals.push(currentFrom)

            // currentFrom = dom.next(fromChildren, currentFrom)
            currentFrom = getNextSibling(from, currentFrom)
        }

        // Now we can do the actual removals.
        while (removals.length) {
            let domForRemoval = removals.shift()

            domForRemoval.remove()

            context.removed(domForRemoval)
        }
    }
```

### 🔹 函式: `createMorphContext()`
- **變更前簽章 (Before)**: `function createMorphContext(options =` (L68~L433)
- **變更後簽章 (After)**: `function createMorphContext(options =` (L68~L440)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createMorphContext(options = {}) {
    let defaultGetKey = el => el.getAttribute('key')
    let noop = () => {}

    let context = {
        key: options.key || defaultGetKey,
        lookahead: options.lookahead || false,
        updating: options.updating || noop,
        updated: options.updated || noop,
        removing: options.removing || noop,
        removed: options.removed || noop,
        adding: options.adding || noop,
        added: options.added || noop
    }

    context.patch = function(from, to) {
        if (context.differentElementNamesTypesOrKeys(from, to)) {
            return context.swapElements(from, to)
        }

        let updateChildrenOnly = false
        let skipChildren = false

        // If we used `shouldSkip()` here and append the `skipChildren` function on the end, it will cause the signature of the `updating`
        // hook to change. For example, when it was `shouldSkip()` the signature was `updating: (el, toEl, childrenOnly, skip)`. But if
        // we append `skipChildren()`, it would make the signature `updating: (el, toEl, childrenOnly, skipChildren, skip)`. This is
        // a breaking change due to how the `shouldSkip()` function is structured.
        //
        // So we're using `shouldSkipChildren()` instead which doesn't have this problem as it allows us to pass in the `skipChildren()`
        // function as an earlier parameter and then append it to the `updating` hook signature manually. The signature of `updating`
        // hook is now `updating: (el, toEl, childrenOnly, skip, skipChildren)`.

        let skipUntil = predicate => context.skipUntilCondition = predicate

        if (shouldSkipChildren(context.updating, () => skipChildren = true, skipUntil, from, to, () => updateChildrenOnly = true)) return

        // Initialize the server-side HTML element with Alpine...
        if (from.nodeType === 1 && window.Alpine) {
            window.Alpine.cloneNode(from, to)

            if (from._x_teleport && to._x_teleport) {
                context.patch(from._x_teleport, to._x_teleport)
            }
        }

        if (textOrComment(to)) {
            context.patchNodeValue(from, to)

            context.updated(from, to)

            return
        }

        if (! updateChildrenOnly) {
            context.patchAttributes(from, to)
        }

        context.updated(from, to)

        if (! skipChildren) {
            context.patchChildren(from, to)
        }
    }

    context.differentElementNamesTypesOrKeys = function(from, to) {
        return from.nodeType != to.nodeType
            || from.nodeName != to.nodeName
            || context.getKey(from) != context.getKey(to)
    }

    context.swapElements = function(from, to) {
        if (shouldSkip(context.removing, from)) return

        let toCloned = to.cloneNode(true)

        if (shouldSkip(context.adding, toCloned)) return

        from.replaceWith(toCloned)

        context.removed(from)
        context.added(toCloned)
    }

    context.patchNodeValue = function(from, to) {
        let value = to.nodeValue

        if (from.nodeValue !== value) {
            // Change text node...
            from.nodeValue = value
        }
    }

    context.patchAttributes = function(from, to) {
        if (from._x_transitioning) return

        if (from._x_isShown && ! to._x_isShown) {
            return
        }
        if (! from._x_isShown && to._x_isShown) {
            return
        }

        let domAttributes = Array.from(from.attributes)
        let toAttributes = Array.from(to.attributes)

        for (let i = domAttributes.length - 1; i >= 0; i--) {
            let name = domAttributes[i].name;

            if (! to.hasAttribute(name)) {
                if (name === 'open' && from.nodeName === 'DIALOG' && from.open) {
                    from.close()
                } else {
                    from.removeAttribute(name)
                }
            }
        }

        for (let i = toAttributes.length - 1; i >= 0; i--) {
            let name = toAttributes[i].name
            let value = toAttributes[i].value

            if (from.getAttribute(name) !== value) {
                from.setAttribute(name, value)
            }
        }
    }

    context.patchChildren = function(from, to) {
        let fromKeys = context.keyToMap(from.children)
        let fromKeyHoldovers = {}

        let currentTo = getFirstNode(to)
        let currentFrom = getFirstNode(from)

        while (currentTo) {
            // If the "from" element has a dynamically bound "id" (x-bind:id="..."),
            // Let's transfer it to the "to" element so that there isn't a key mismatch...
            seedingMatchingId(currentTo, currentFrom)

            let toKey = context.getKey(currentTo)
            let fromKey = context.getKey(currentFrom)

            if (context.skipUntilCondition) {
                let fromDone = ! currentFrom || context.skipUntilCondition(currentFrom)
                let toDone   = ! currentTo   || context.skipUntilCondition(currentTo)
                if (fromDone && toDone) {
                    context.skipUntilCondition = null
                } else {
                    if (! fromDone) currentFrom = currentFrom && getNextSibling(from, currentFrom)
                    if (! toDone)   currentTo   = currentTo   && getNextSibling(to, currentTo)
                    continue
                }
            }

            // Add new elements...
            if (! currentFrom) {
                if (toKey && fromKeyHoldovers[toKey]) {
                    // Add element (from key)...
                    let holdover = fromKeyHoldovers[toKey]

                    from.appendChild(holdover)

                    currentFrom = holdover
                    fromKey = context.getKey(currentFrom)
                } else {
                    if(! shouldSkip(context.adding, currentTo)) {
                        // Add element...
                        let clone = currentTo.cloneNode(true)

                        from.appendChild(clone)

                        context.added(clone)
                    }

                    currentTo = getNextSibling(to, currentTo)

                    continue
                }
            }

            // Handle conditional markers (presumably added by backends like Livewire)...
            let isIf = node => node && node.nodeType === 8 && node.textContent === '[if BLOCK]><![endif]'
            let isEnd = node => node && node.nodeType === 8 && node.textContent === '[if ENDBLOCK]><![endif]'

            if (isIf(currentTo) && isIf(currentFrom)) {
                let nestedIfCount = 0

                let fromBlockStart = currentFrom

                while (currentFrom) {
                    let next = getNextSibling(from, currentFrom)

                    if (isIf(next)) {
                        nestedIfCount++
                    } else if (isEnd(next) && nestedIfCount > 0) {
                        nestedIfCount--
                    } else if (isEnd(next) && nestedIfCount === 0) {
                        currentFrom = next

                        break;
                    }

                    currentFrom = next
                }

                let fromBlockEnd = currentFrom

                nestedIfCount = 0

                let toBlockStart = currentTo

                while (currentTo) {
                    let next = getNextSibling(to, currentTo)

                    if (isIf(next)) {
                        nestedIfCount++
                    } else if (isEnd(next) && nestedIfCount > 0) {
                        nestedIfCount--
                    } else if (isEnd(next) && nestedIfCount === 0) {
                        currentTo = next

                        break;
                    }

                    currentTo = next
                }

                let toBlockEnd = currentTo

                let fromBlock = new Block(fromBlockStart, fromBlockEnd)
                let toBlock = new Block(toBlockStart, toBlockEnd)

                context.patchChildren(fromBlock, toBlock)

                continue
            }

            // Lookaheads should only apply to non-text-or-comment elements...
            if (currentFrom.nodeType === 1 && context.lookahead && ! currentFrom.isEqualNode(currentTo)) {
                let nextToElementSibling = getNextSibling(to, currentTo)

                let found = false

                while (! found && nextToElementSibling) {
                    if (nextToElementSibling.nodeType === 1 && currentFrom.isEqualNode(nextToElementSibling)) {
                        found = true; // This ";" needs to be here...

                        currentFrom = context.addNodeBefore(from, currentTo, currentFrom)

                        fromKey = context.getKey(currentFrom)
                    }

                    nextToElementSibling = getNextSibling(to, nextToElementSibling)
                }
            }

            if (toKey !== fromKey) {
                if (! toKey && fromKey) {
                    // No "to" key...
                    fromKeyHoldovers[fromKey] = currentFrom; // This ";" needs to be here...
                    currentFrom = context.addNodeBefore(from, currentTo, currentFrom)
                    fromKeyHoldovers[fromKey].remove()
                    currentFrom = getNextSibling(from, currentFrom)
                    currentTo = getNextSibling(to, currentTo)

                    continue
                }

                if (toKey && ! fromKey) {
                    if (fromKeys[toKey]) {
                        // No "from" key...
                        currentFrom.replaceWith(fromKeys[toKey])
                        currentFrom = fromKeys[toKey]
                        fromKey = context.getKey(currentFrom)
                    }
                }

                if (toKey && fromKey) {
                    let fromKeyNode = fromKeys[toKey]

                    if (fromKeyNode) {
                        // Move "from" key...
                        fromKeyHoldovers[fromKey] = currentFrom
                        currentFrom.replaceWith(fromKeyNode)
                        currentFrom = fromKeyNode
                        fromKey = context.getKey(currentFrom)
                    } else {
                        // Swap elements with keys...
                        fromKeyHoldovers[fromKey] = currentFrom; // This ";" needs to be here...
                        currentFrom = context.addNodeBefore(from, currentTo, currentFrom)
                        fromKeyHoldovers[fromKey].remove()
                        currentFrom = getNextSibling(from, currentFrom)
                        currentTo = getNextSibling(to, currentTo)

                        continue
                    }
                }
            }

            // Get next from sibling before patching in case the node is replaced
            let currentFromNext = currentFrom && getNextSibling(from, currentFrom) //dom.next(from, fromChildren, currentFrom))

            // Patch elements
            context.patch(currentFrom, currentTo)

            currentTo = currentTo && getNextSibling(to, currentTo) // dom.next(from, toChildren, currentTo))

            currentFrom = currentFromNext
        }

        // Cleanup extra forms.
        let removals = []

        // We need to collect the "removals" first before actually
        // removing them so we don't mess with the order of things.
        while (currentFrom) {
            if (! shouldSkip(context.removing, currentFrom)) removals.push(currentFrom)

            // currentFrom = dom.next(fromChildren, currentFrom)
            currentFrom = getNextSibling(from, currentFrom)
        }

        // Now we can do the actual removals.
        while (removals.length) {
            let domForRemoval = removals.shift()

            domForRemoval.remove()

            context.removed(domForRemoval)
        }
    }

    context.getKey = function(el) {
        return el && el.nodeType === 1 && context.key(el)
    }

    context.keyToMap = function(els) {
        let map = {}

        for (let el of els) {
            let theKey = context.getKey(el)

            if (theKey) {
                map[theKey] = el
            }
        }

        return map
    }

    context.addNodeBefore = function(parent, node, beforeMe) {
        if(! shouldSkip(context.adding, node)) {
            let clone = node.cloneNode(true)

            parent.insertBefore(clone, beforeMe)

            context.added(clone)

            return clone
        }

        return node
    }

    return context
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createMorphContext(options = {}) {
    let defaultGetKey = el => el.getAttribute('key')
    let noop = () => {}

    let context = {
        key: options.key || defaultGetKey,
        lookahead: options.lookahead || false,
        updating: options.updating || noop,
        updated: options.updated || noop,
        removing: options.removing || noop,
        removed: options.removed || noop,
        adding: options.adding || noop,
        added: options.added || noop
    }

    context.patch = function(from, to) {
        if (context.differentElementNamesTypesOrKeys(from, to)) {
            return context.swapElements(from, to)
        }

        let updateChildrenOnly = false
        let skipChildren = false

        // If we used `shouldSkip()` here and append the `skipChildren` function on the end, it will cause the signature of the `updating`
        // hook to change. For example, when it was `shouldSkip()` the signature was `updating: (el, toEl, childrenOnly, skip)`. But if
        // we append `skipChildren()`, it would make the signature `updating: (el, toEl, childrenOnly, skipChildren, skip)`. This is
        // a breaking change due to how the `shouldSkip()` function is structured.
        //
        // So we're using `shouldSkipChildren()` instead which doesn't have this problem as it allows us to pass in the `skipChildren()`
        // function as an earlier parameter and then append it to the `updating` hook signature manually. The signature of `updating`
        // hook is now `updating: (el, toEl, childrenOnly, skip, skipChildren)`.

        let skipUntil = predicate => context.skipUntilCondition = predicate

        if (shouldSkipChildren(context.updating, () => skipChildren = true, skipUntil, from, to, () => updateChildrenOnly = true)) return

        // Initialize the server-side HTML element with Alpine...
        if (from.nodeType === 1 && window.Alpine) {
            window.Alpine.cloneNode(from, to)

            if (from._x_teleport && to._x_teleport) {
                context.patch(from._x_teleport, to._x_teleport)
            }
        }

        if (textOrComment(to)) {
            context.patchNodeValue(from, to)

            context.updated(from, to)

            return
        }

        if (! updateChildrenOnly) {
            context.patchAttributes(from, to)
        }

        context.updated(from, to)

        if (! skipChildren) {
            context.patchChildren(from, to)
        }
    }

    context.differentElementNamesTypesOrKeys = function(from, to) {
        return from.nodeType != to.nodeType
            || from.nodeName != to.nodeName
            || context.getKey(from) != context.getKey(to)
    }

    context.swapElements = function(from, to) {
        if (shouldSkip(context.removing, from)) return

        let toCloned = to.cloneNode(true)

        if (shouldSkip(context.adding, toCloned)) return

        from.replaceWith(toCloned)

        context.removed(from)
        context.added(toCloned)
    }

    context.patchNodeValue = function(from, to) {
        let value = to.nodeValue

        if (from.nodeValue !== value) {
            // Change text node...
            from.nodeValue = value
        }
    }

    context.patchAttributes = function(from, to) {
        if (from._x_transitioning) return

        if (from._x_isShown && ! to._x_isShown) {
            return
        }
        if (! from._x_isShown && to._x_isShown) {
            return
        }

        let domAttributes = Array.from(from.attributes)
        let toAttributes = Array.from(to.attributes)

        for (let i = domAttributes.length - 1; i >= 0; i--) {
            let name = domAttributes[i].name;

            if (! to.hasAttribute(name)) {
                if (name === 'open' && from.nodeName === 'DIALOG' && from.open) {
                    from.close()
                } else {
                    from.removeAttribute(name)
                }
            }
        }

        for (let i = toAttributes.length - 1; i >= 0; i--) {
            let name = toAttributes[i].name
            let value = toAttributes[i].value

            if (from.getAttribute(name) !== value) {
                from.setAttribute(name, value)
            }
        }
    }

    context.patchChildren = function(from, to) {
        let fromKeys = context.keyToMap(from.children)
        let fromKeyHoldovers = {}

        let currentTo = getFirstNode(to)
        let currentFrom = getFirstNode(from)

        while (currentTo) {
            // If the "from" element has a dynamically bound "id" (x-bind:id="..."),
            // Let's transfer it to the "to" element so that there isn't a key mismatch...
            seedingMatchingId(currentTo, currentFrom)

            let toKey = context.getKey(currentTo)
            let fromKey = context.getKey(currentFrom)

            if (context.skipUntilCondition) {
                let fromDone = ! currentFrom || context.skipUntilCondition(currentFrom)
                let toDone   = ! currentTo   || context.skipUntilCondition(currentTo)
                if (fromDone && toDone) {
                    context.skipUntilCondition = null
                } else {
                    if (! fromDone) currentFrom = currentFrom && getNextSibling(from, currentFrom)
                    if (! toDone)   currentTo   = currentTo   && getNextSibling(to, currentTo)
                    continue
                }
            }

            // Add new elements...
            if (! currentFrom) {
                if (toKey && fromKeyHoldovers[toKey]) {
                    // Add element (from key)...
                    let holdover = fromKeyHoldovers[toKey]

                    from.appendChild(holdover)

                    currentFrom = holdover
                    fromKey = context.getKey(currentFrom)
                } else {
                    if(! shouldSkip(context.adding, currentTo)) {
                        // Add element...
                        let clone = currentTo.cloneNode(true)

                        from.appendChild(clone)

                        context.added(clone)
                    }

                    currentTo = getNextSibling(to, currentTo)

                    continue
                }
            }

            // Handle conditional markers (presumably added by backends like Livewire)...
            let isIf = node => node && node.nodeType === 8 && node.textContent === '[if BLOCK]><![endif]'
            let isEnd = node => node && node.nodeType === 8 && node.textContent === '[if ENDBLOCK]><![endif]'

            if (isIf(currentTo) && isIf(currentFrom)) {
                let nestedIfCount = 0

                let fromBlockStart = currentFrom

                while (currentFrom) {
                    let next = getNextSibling(from, currentFrom)

                    if (isIf(next)) {
                        nestedIfCount++
                    } else if (isEnd(next) && nestedIfCount > 0) {
                        nestedIfCount--
                    } else if (isEnd(next) && nestedIfCount === 0) {
                        currentFrom = next

                        break;
                    }

                    currentFrom = next
                }

                let fromBlockEnd = currentFrom

                nestedIfCount = 0

                let toBlockStart = currentTo

                while (currentTo) {
                    let next = getNextSibling(to, currentTo)

                    if (isIf(next)) {
                        nestedIfCount++
                    } else if (isEnd(next) && nestedIfCount > 0) {
                        nestedIfCount--
                    } else if (isEnd(next) && nestedIfCount === 0) {
                        currentTo = next

                        break;
                    }

                    currentTo = next
                }

                let toBlockEnd = currentTo

                let fromBlock = new Block(fromBlockStart, fromBlockEnd)
                let toBlock = new Block(toBlockStart, toBlockEnd)

                context.patchChildren(fromBlock, toBlock)

                continue
            }

            // Lookaheads should only apply to non-text-or-comment elements...
            if (currentFrom.nodeType === 1 && context.lookahead && ! currentFrom.isEqualNode(currentTo)) {
                let nextToElementSibling = getNextSibling(to, currentTo)

                let found = false

                while (! found && nextToElementSibling) {
                    if (nextToElementSibling.nodeType === 1 && currentFrom.isEqualNode(nextToElementSibling)) {
                        found = true; // This ";" needs to be here...

                        currentFrom = context.addNodeBefore(from, currentTo, currentFrom)

                        fromKey = context.getKey(currentFrom)
                    }

                    nextToElementSibling = getNextSibling(to, nextToElementSibling)
                }
            }

            if (toKey !== fromKey) {
                if (! toKey && fromKey) {
                    // No "to" key...
                    fromKeyHoldovers[fromKey] = currentFrom; // This ";" needs to be here...
                    currentFrom = context.addNodeBefore(from, currentTo, currentFrom)
                    fromKeyHoldovers[fromKey].remove()
                    currentFrom = getNextSibling(from, currentFrom)
                    currentTo = getNextSibling(to, currentTo)

                    continue
                }

                if (toKey && ! fromKey) {
                    if (fromKeys[toKey]) {
                        // No "from" key...
                        currentFrom.replaceWith(fromKeys[toKey])
                        currentFrom = fromKeys[toKey]
                        fromKey = context.getKey(currentFrom)
                    }
                }

                if (toKey && fromKey) {
                    let fromKeyNode = fromKeys[toKey]

                    if (fromKeyNode) {
                        // Move "from" key...
                        fromKeyHoldovers[fromKey] = currentFrom
                        currentFrom.replaceWith(fromKeyNode)
                        currentFrom = fromKeyNode
                        fromKey = context.getKey(currentFrom)
                    } else {
                        // Swap elements with keys...
                        fromKeyHoldovers[fromKey] = currentFrom; // This ";" needs to be here...
                        currentFrom = context.addNodeBefore(from, currentTo, currentFrom)
                        fromKeyHoldovers[fromKey].remove()
                        currentFrom = getNextSibling(from, currentFrom)
                        currentTo = getNextSibling(to, currentTo)

                        continue
                    }
                }
            }

            // Get next from sibling before patching in case the node is replaced
            let currentFromNext = currentFrom && getNextSibling(from, currentFrom) //dom.next(from, fromChildren, currentFrom))

            // Patch elements
            context.patch(currentFrom, currentTo)

            // Directives like x-if and x-for insert sibling elements
            // that they manage. Skip past them — they'll be handled
            // by Alpine's reactivity after the morph completes...
            if (currentFrom._x_lastRenderedEl) {
                currentFromNext = getNextSibling(from, currentFrom._x_lastRenderedEl)
            }

            currentTo = currentTo && getNextSibling(to, currentTo) // dom.next(from, toChildren, currentTo))

            currentFrom = currentFromNext
        }

        // Cleanup extra forms.
        let removals = []

        // We need to collect the "removals" first before actually
        // removing them so we don't mess with the order of things.
        while (currentFrom) {
            if (! shouldSkip(context.removing, currentFrom)) removals.push(currentFrom)

            // currentFrom = dom.next(fromChildren, currentFrom)
            currentFrom = getNextSibling(from, currentFrom)
        }

        // Now we can do the actual removals.
        while (removals.length) {
            let domForRemoval = removals.shift()

            domForRemoval.remove()

            context.removed(domForRemoval)
        }
    }

    context.getKey = function(el) {
        return el && el.nodeType === 1 && context.key(el)
    }

    context.keyToMap = function(els) {
        let map = {}

        for (let el of els) {
            let theKey = context.getKey(el)

            if (theKey) {
                map[theKey] = el
            }
        }

        return map
    }

    context.addNodeBefore = function(parent, node, beforeMe) {
        if(! shouldSkip(context.adding, node)) {
            let clone = node.cloneNode(true)

            parent.insertBefore(clone, beforeMe)

            context.added(clone)

            return clone
        }

        return node
    }

    return context
}
```


---

### 🔹 Commit #16: `999d77d7`
- **完整 Hash**: `999d77d7579ab9ceb2ef94717647533478a0bfa6`
- **說明 (Ground Truth)**: fix: Mask resurrecting key in object (#4812)
- **變更檔案數**: 1

#### 📄 檔案: `packages/mask/src/index.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:25, E:25, A:1) ➔ After(N:25, E:25, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#el** `(Control)`
    └── ⚡ **on('blur')**
        └── 🎯 [TRIGGERS] `on('blur')_handler()`
            └── 🎯 [CALLS] `processInputValue()`
                └── 🎯 [CALLS] `setInput()`
                    └── 🎯 [CALLS] `formatInput()`
                └── 🎯 [CALLS] `templateFn()`
                └── 🎯 [CALLS] `restoreCursorPosition()`
                    └── 🎯 [CALLS] `callback (External/Unresolved)()`
                    └── *ref:`formatInput` [已折疊指針]
    └── ⚡ **on('input')**
        └── 🎯 [TRIGGERS] `on('input')_handler()`
            └── *ref:`processInputValue` [已折疊指針]

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'templateFn' 被深鎖在內部閉包 (scope:directive:mask@after/packages/mask/src/index.js:L3C30)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_x_forceModelUpdate()`
- **變更前簽章 (Before)**: `_x_forceModelUpdate(value)` (L54~L63)
- **變更後簽章 (After)**: `_x_forceModelUpdate(value)` (L54~L71)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(value) => {
                    value = String(value)
                    let template = templateFn(value)
                    if (template && template !== 'false') {
                        value = formatInput(template, value)
                    }
                    lastInputValue = value
                    updater(value)
                    el._x_model.set(value)
                }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(value) => {
                    // If the model value was cleared (e.g. the parent object was
                    // removed), just clear the input — don't format and write back
                    // as that would resurrect the model path with an empty value.
                    if (value === undefined) {
                        lastInputValue = ''
                        return updater(value)
                    }

                    value = String(value)
                    let template = templateFn(value)
                    if (template && template !== 'false') {
                        value = formatInput(template, value)
                    }
                    lastInputValue = value
                    updater(value)
                    el._x_model.set(value)
                }
```

### 🔹 函式: `directive:mask()`
- **變更前簽章 (Before)**: `directive:mask(el, { value, expression }, { effect, evaluateLater, cleanup })` (L3~L112)
- **變更後簽章 (After)**: `directive:mask(el, { value, expression }, { effect, evaluateLater, cleanup })` (L3~L120)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(el, { value, expression }, { effect, evaluateLater, cleanup }) => {
        let templateFn = () => expression
        let lastInputValue = ''

        queueMicrotask(() => {
            if (['function', 'dynamic'].includes(value)) {
                // This is an x-mask:function directive.

                let evaluator = evaluateLater(expression)

                effect(() => {
                    templateFn = input => {
                        let result

                        // We need to prevent "auto-evaluation" of functions like
                        // x-on expressions do so that we can use them as mask functions.
                        Alpine.dontAutoEvaluateFunctions(() => {
                            evaluator(value => {
                                result = typeof value === 'function' ? value(input) : value
                            }, { scope: {
                                // These are "magics" we'll make available to the x-mask:function:
                                '$input': input,
                                '$money': formatMoney.bind({ el }),
                            }})
                        })

                        return result
                    }

                    // Run on initialize which serves a dual purpose:
                    // - Initializing the mask on the input if it has an initial value.
                    // - Running the template function to set up reactivity, so that
                    //   when a dependency inside it changes, the input re-masks.
                    processInputValue(el, false)
                })
            } else {
                processInputValue(el, false)
            }

            // Override x-model's initial value...
            if (el._x_model) {
                // If the x-model value is the same, don't override it as that will trigger updates...
                if (el._x_model.get() !== el.value) {
                    // If the x-model value is `null` and the input value is an empty
                    // string, don't override it as that will trigger updates...
                    if (!(el._x_model.get() === null && el.value === '')) {
                        el._x_model.set(el.value)
                    }
                }

                let updater = el._x_forceModelUpdate
                el._x_forceModelUpdate = (value) => {
                    value = String(value)
                    let template = templateFn(value)
                    if (template && template !== 'false') {
                        value = formatInput(template, value)
                    }
                    lastInputValue = value
                    updater(value)
                    el._x_model.set(value)
                }
            }
        })

        const controller = new AbortController()

        cleanup(() => {
            controller.abort()
        })

        el.addEventListener('input', () => processInputValue(el), {
            signal: controller.signal,
            // Setting this as a capture phase listener to ensure it runs
            // before wire:model or x-model added as a latent binding...
            capture: true,
        })

        // Don't "restoreCursorPosition" on "blur", because Safari
        // will re-focus the input and cause a focus trap.
        el.addEventListener('blur', () => processInputValue(el, false), { signal: controller.signal })

        function processInputValue (el, shouldRestoreCursor = true) {
            let input = el.value

            let template = templateFn(input)

            // If a template value is `falsy`, then don't process the input value
            if(!template || template === 'false') return false

            // If they hit backspace, don't process input.
            if (lastInputValue.length - el.value.length === 1) {
                return lastInputValue = el.value
            }

            let setInput = () => {
                lastInputValue = el.value = formatInput(template,input)
            }

            if (shouldRestoreCursor) {
                // When an input element's value is set, it moves the cursor to the end
                // therefore we need to track, estimate, and restore the cursor after
                // a change was made.
                restoreCursorPosition(el, template, () => {
                    setInput()
                })
            } else {
                setInput()
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(el, { value, expression }, { effect, evaluateLater, cleanup }) => {
        let templateFn = () => expression
        let lastInputValue = ''

        queueMicrotask(() => {
            if (['function', 'dynamic'].includes(value)) {
                // This is an x-mask:function directive.

                let evaluator = evaluateLater(expression)

                effect(() => {
                    templateFn = input => {
                        let result

                        // We need to prevent "auto-evaluation" of functions like
                        // x-on expressions do so that we can use them as mask functions.
                        Alpine.dontAutoEvaluateFunctions(() => {
                            evaluator(value => {
                                result = typeof value === 'function' ? value(input) : value
                            }, { scope: {
                                // These are "magics" we'll make available to the x-mask:function:
                                '$input': input,
                                '$money': formatMoney.bind({ el }),
                            }})
                        })

                        return result
                    }

                    // Run on initialize which serves a dual purpose:
                    // - Initializing the mask on the input if it has an initial value.
                    // - Running the template function to set up reactivity, so that
                    //   when a dependency inside it changes, the input re-masks.
                    processInputValue(el, false)
                })
            } else {
                processInputValue(el, false)
            }

            // Override x-model's initial value...
            if (el._x_model) {
                // If the x-model value is the same, don't override it as that will trigger updates...
                if (el._x_model.get() !== el.value) {
                    // If the x-model value is `null` and the input value is an empty
                    // string, don't override it as that will trigger updates...
                    if (!(el._x_model.get() === null && el.value === '')) {
                        el._x_model.set(el.value)
                    }
                }

                let updater = el._x_forceModelUpdate
                el._x_forceModelUpdate = (value) => {
                    // If the model value was cleared (e.g. the parent object was
                    // removed), just clear the input — don't format and write back
                    // as that would resurrect the model path with an empty value.
                    if (value === undefined) {
                        lastInputValue = ''
                        return updater(value)
                    }

                    value = String(value)
                    let template = templateFn(value)
                    if (template && template !== 'false') {
                        value = formatInput(template, value)
                    }
                    lastInputValue = value
                    updater(value)
                    el._x_model.set(value)
                }
            }
        })

        const controller = new AbortController()

        cleanup(() => {
            controller.abort()
        })

        el.addEventListener('input', () => processInputValue(el), {
            signal: controller.signal,
            // Setting this as a capture phase listener to ensure it runs
            // before wire:model or x-model added as a latent binding...
            capture: true,
        })

        // Don't "restoreCursorPosition" on "blur", because Safari
        // will re-focus the input and cause a focus trap.
        el.addEventListener('blur', () => processInputValue(el, false), { signal: controller.signal })

        function processInputValue (el, shouldRestoreCursor = true) {
            let input = el.value

            let template = templateFn(input)

            // If a template value is `falsy`, then don't process the input value
            if(!template || template === 'false') return false

            // If they hit backspace, don't process input.
            if (lastInputValue.length - el.value.length === 1) {
                return lastInputValue = el.value
            }

            let setInput = () => {
                lastInputValue = el.value = formatInput(template,input)
            }

            if (shouldRestoreCursor) {
                // When an input element's value is set, it moves the cursor to the end
                // therefore we need to track, estimate, and restore the cursor after
                // a change was made.
                restoreCursorPosition(el, template, () => {
                    setInput()
                })
            } else {
                setInput()
            }
        }
    }
```


---

### 🔹 Commit #17: `cdb7c428`
- **完整 Hash**: `cdb7c428800eb3297d9e343a4ca88995aa4a2fac`
- **說明 (Ground Truth)**: fix: serialize object/array values to JSON in attribute bindings (#4826)
- **變更檔案數**: 1

#### 📄 檔案: `packages/alpinejs/src/utils/bind.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:29, E:26, A:0) ➔ After(N:30, E:27, A:0)
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
  • + [新增節點] `isObjectAttr` (FUNCTION_DEF)
  • + [新增呼叫邊] `bindAttribute` ──[CALLS [guard: ([null, undefined, false].includes(value) && attributeShouldntBePreservedIfFalsy(name))]]──> `isObjectAttr`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `bindAttribute()`
- **變更前簽章 (Before)**: `function bindAttribute(el, name, value)` (L90~L98)
- **變更後簽章 (After)**: `function bindAttribute(el, name, value)` (L90~L99)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function bindAttribute(el, name, value) {
    if ([null, undefined, false].includes(value) && attributeShouldntBePreservedIfFalsy(name)) {
        el.removeAttribute(name)
    } else {
        if (isBooleanAttr(name)) value = name

        setIfChanged(el, name, value)
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function bindAttribute(el, name, value) {
    if ([null, undefined, false].includes(value) && attributeShouldntBePreservedIfFalsy(name)) {
        el.removeAttribute(name)
    } else {
        if (isBooleanAttr(name)) value = name
        if (isObjectAttr(value)) value = JSON.stringify(value)

        setIfChanged(el, name, value)
    }
}
```


---

### 🔹 Commit #18: `8f519b7a`
- **完整 Hash**: `8f519b7a0911bc676ab025bce2a0bc36c35defe3`
- **說明 (Ground Truth)**: Fix `@teleport` leaking detached nodes on every Livewire render (#4822)
- **變更檔案數**: 1

#### 📄 檔案: `packages/alpinejs/src/directives/x-teleport.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:17, E:16, A:3) ➔ After(N:17, E:16, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#clone** `(Control)`
    └── ⚡ **on('eventName')**
        └── 🎯 [TRIGGERS] `on('eventName')_handler()`
  🌲 **#target** `(Control)`
  🌲 **#teleportContainerDuringClone** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'placeInDom' 被深鎖在內部閉包 (scope:directive:teleport@after/packages/alpinejs/src/directives/x-teleport.js:L8C23)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `directive:teleport()`
- **變更前簽章 (Before)**: `directive:teleport(el, { modifiers, expression }, { cleanup })` (L8~L71)
- **變更後簽章 (After)**: `directive:teleport(el, { modifiers, expression }, { cleanup })` (L8~L71)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(el, { modifiers, expression }, { cleanup }) => {
    if (el.tagName.toLowerCase() !== 'template') warn('x-teleport can only be used on a <template> tag', el)

    let target = getTarget(expression)

    let clone = el.content.cloneNode(true).firstElementChild

    // Add reference to element on <template x-teleport, and visa versa.
    el._x_teleport = clone
    clone._x_teleportBack = el

    // Add the key to the DOM so they can be more easily searched for and linked up...
    el.setAttribute('data-teleport-template', true)
    clone.setAttribute('data-teleport-target', true)

    // Forward event listeners:
    if (el._x_forwardEvents) {
        el._x_forwardEvents.forEach(eventName => {
            clone.addEventListener(eventName, e => {
                e.stopPropagation()

                el.dispatchEvent(new e.constructor(e.type, e))
            })
        })
    }

    addScopeToNode(clone, {}, el)

    let placeInDom = (clone, target, modifiers) => {
        if (modifiers.includes('prepend')) {
            // insert element before the target
            target.parentNode.insertBefore(clone, target)
        } else if (modifiers.includes('append')) {
            // insert element after the target
            target.parentNode.insertBefore(clone, target.nextSibling)
        } else {
            // origin
            target.appendChild(clone)
        }
    }

    mutateDom(() => {
        placeInDom(clone, target, modifiers)

        skipDuringClone(() => {
            initTree(clone)
        })()
    })

    el._x_teleportPutBack = () => {
        let target = getTarget(expression)

        mutateDom(() => {
            placeInDom(el._x_teleport, target, modifiers)
        })
    }

    cleanup(() =>
      mutateDom(() => {
        clone.remove()
        destroyTree(clone)
      })
    )
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(el, { modifiers, expression }, { cleanup }) => {
    if (el.tagName.toLowerCase() !== 'template') warn('x-teleport can only be used on a <template> tag', el)

    let target = getTarget(expression)

    let clone = el.content.cloneNode(true).firstElementChild

    // Add reference to element on <template x-teleport, and visa versa.
    el._x_teleport = clone
    clone._x_teleportBack = el

    // Add the key to the DOM so they can be more easily searched for and linked up...
    el.setAttribute('data-teleport-template', true)
    clone.setAttribute('data-teleport-target', true)

    // Forward event listeners:
    if (el._x_forwardEvents) {
        el._x_forwardEvents.forEach(eventName => {
            clone.addEventListener(eventName, e => {
                e.stopPropagation()

                el.dispatchEvent(new e.constructor(e.type, e))
            })
        })
    }

    addScopeToNode(clone, {}, el)

    let placeInDom = (clone, target, modifiers) => {
        if (modifiers.includes('prepend')) {
            // insert element before the target
            target.parentNode.insertBefore(clone, target)
        } else if (modifiers.includes('append')) {
            // insert element after the target
            target.parentNode.insertBefore(clone, target.nextSibling)
        } else {
            // origin
            target.appendChild(clone)
        }
    }

    mutateDom(() => {
        skipDuringClone(() => {
            placeInDom(clone, target, modifiers)

            initTree(clone)
        })()
    })

    el._x_teleportPutBack = () => {
        let target = getTarget(expression)

        mutateDom(() => {
            placeInDom(el._x_teleport, target, modifiers)
        })
    }

    cleanup(() =>
      mutateDom(() => {
        clone.remove()
        destroyTree(clone)
      })
    )
}
```


---

### 🔹 Commit #19: `7d3cb1c6`
- **完整 Hash**: `7d3cb1c66a7e6d24dd2fe30b78df58bf061fa174`
- **說明 (Ground Truth)**: Fix `x-id` evaluation order so `$id` resolves consistently inside `x-data` (#4821)
- **變更檔案數**: 1

#### 📄 檔案: `packages/alpinejs/src/directives.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:42, E:19, A:0) ➔ After(N:42, E:19, A:0)
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

### 🔹 函式: `directiveOrder()`
- **變更前簽章 (Before)**: `[Module State] directiveOrder` (L206~L222)
- **變更後簽章 (After)**: `[Module State] directiveOrder` (L206~L222)

#### ◀️ 變更前實作碼 (Before Implementation):
```
directiveOrder = [
    'ignore',
    'ref',
    'data',
    'id',
    'anchor',
    'bind',
    'init',
    'for',
    'model',
    'modelable',
    'transition',
    'show',
    'if',
    DEFAULT,
    'teleport',
]
```

#### ▶️ 變更後實作碼 (After Implementation):
```
directiveOrder = [
    'ignore',
    'ref',
    'id',
    'data',
    'anchor',
    'bind',
    'init',
    'for',
    'model',
    'modelable',
    'transition',
    'show',
    'if',
    DEFAULT,
    'teleport',
]
```


---

### 🔹 Commit #20: `d76a11eb`
- **完整 Hash**: `d76a11eb4124e6c1e534014ef8bb36c2c2e348c2`
- **說明 (Ground Truth)**: Fix `x-sort` crash when container has a `<template>` with no `.content` (#4819)
- **變更檔案數**: 1

#### 📄 檔案: `packages/sort/src/index.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:19, E:13, A:2) ➔ After(N:19, E:13, A:2)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#options** `(Button)`
  🌲 **#preferences** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `directive:sort()`
- **變更前簽章 (Before)**: `directive:sort(el, { value, modifiers, expression }, { effect, evaluate, cleanup })` (L5~L45)
- **變更後簽章 (After)**: `directive:sort(el, { value, modifiers, expression }, { effect, evaluate, cleanup })` (L5~L45)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(el, { value, modifiers, expression }, { effect, evaluate, cleanup }) => {
        if (value === 'config') {
            return // This will get handled by the main directive...
        }

        if (value === 'handle') {
            return // This will get handled by the main directive...
        }

        if (value === 'group') {
            return // This will get handled by the main directive...
        }

        // Supporting both `x-sort:item` AND `x-sort:key` (key for BC)...
        if (value === 'key' || value === 'item') {
            if ([undefined, null, ''].includes(expression)) return

            el._x_sort_key = evaluate(expression)

            return
        }

        let handleSelector = '[x-sort\\:handle],[wire\\:sort\\:handle]'

        let preferences = {
            hideGhost: ! modifiers.includes('ghost'),
            useHandles: !! el.querySelector(handleSelector)
                || Array.from(el.querySelectorAll('template')).some(tmpl => tmpl.content.querySelector(handleSelector)),
            group: getGroupName(el, modifiers),
        }

        let handleSort = generateSortHandler(expression, evaluate)

        let config = getConfigurationOverrides(el, modifiers, evaluate)

        let sortable = initSortable(el, config, preferences, (key, position) => {
            handleSort(key, position)
        })

        cleanup(() => sortable.destroy())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(el, { value, modifiers, expression }, { effect, evaluate, cleanup }) => {
        if (value === 'config') {
            return // This will get handled by the main directive...
        }

        if (value === 'handle') {
            return // This will get handled by the main directive...
        }

        if (value === 'group') {
            return // This will get handled by the main directive...
        }

        // Supporting both `x-sort:item` AND `x-sort:key` (key for BC)...
        if (value === 'key' || value === 'item') {
            if ([undefined, null, ''].includes(expression)) return

            el._x_sort_key = evaluate(expression)

            return
        }

        let handleSelector = '[x-sort\\:handle],[wire\\:sort\\:handle]'

        let preferences = {
            hideGhost: ! modifiers.includes('ghost'),
            useHandles: !! el.querySelector(handleSelector)
                || Array.from(el.querySelectorAll('template:not(svg template)')).some(tmpl => tmpl.content?.querySelector(handleSelector)),
            group: getGroupName(el, modifiers),
        }

        let handleSort = generateSortHandler(expression, evaluate)

        let config = getConfigurationOverrides(el, modifiers, evaluate)

        let sortable = initSortable(el, config, preferences, (key, position) => {
            handleSort(key, position)
        })

        cleanup(() => sortable.destroy())
    }
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/alpine show a7e280222df1f63b29370218d5e09c90110cc56d
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff a7e280222df1f63b29370218d5e09c90110cc56d~1 --file test_repos/alpine/packages/alpinejs/src/mutation.js
   ```
