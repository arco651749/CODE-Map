# 🔬 CODE-Map 基準審查獨立驗證報告: `ink`
> **技術生態**: `TypeScript (React CLI 框架)`  
> **本地倉庫路徑**: `test_repos/ink`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 37 Files  
> **報告生成時間**: 2026-10-20 21:40:48  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `19` / `37` | `51.4%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `16` / `37` | `43.2%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `2` / `37` | `5.4%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`35` / `37`** | **`94.6%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `37` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `13707d2d`
- **完整 Hash**: `13707d2df9ea722d15f0d2de5790ddbf1054dea1`
- **說明 (Ground Truth)**: Handle Ctrl+C buffered with ordinary input
- **變更檔案數**: 1

#### 📄 檔案: `src/input-parser.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:19, E:12, A:0) ➔ After(N:19, E:12, A:0)
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
  • + [新增節點] `splitControlBytes` (FUNCTION_DEF)
  • - [移除節點] `splitBackspaceBytes` (FUNCTION_DEF)
  • + [新增呼叫邊] `parseKeypresses` ──[CALLS [guard: (escapeIndex > index)]]──> `splitControlBytes`
  • - [移除呼叫邊] `parseKeypresses` ──[CALLS]──> `splitBackspaceBytes`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `parseKeypresses()`
- **變更前簽章 (Before)**: `parseKeypresses(input: string)` (L209~L256)
- **變更後簽章 (After)**: `parseKeypresses(input: string)` (L213~L260)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(input: string): ParsedInput => {
	const events: InputEvent[] = [];
	let index = 0;
	const pendingFrom = (pendingStartIndex: number): ParsedInput => ({
		events,
		pending: input.slice(pendingStartIndex),
	});

	while (index < input.length) {
		const escapeIndex = input.indexOf(escape, index);
		if (escapeIndex === -1) {
			splitBackspaceBytes(input.slice(index), events);
			return {
				events,
				pending: '',
			};
		}

		if (escapeIndex > index) {
			splitBackspaceBytes(input.slice(index, escapeIndex), events);
		}

		const parsedEscapeSequence = parseEscapeSequence(input, escapeIndex);
		if (parsedEscapeSequence === 'pending') {
			return pendingFrom(escapeIndex);
		}

		if (parsedEscapeSequence.sequence === pasteStart) {
			const afterStart = parsedEscapeSequence.nextIndex;
			const endIndex = input.indexOf(pasteEnd, afterStart);
			if (endIndex === -1) {
				return pendingFrom(escapeIndex);
			}

			events.push({paste: input.slice(afterStart, endIndex)});
			index = endIndex + pasteEnd.length;
			continue;
		}

		events.push(parsedEscapeSequence.sequence);
		index = parsedEscapeSequence.nextIndex;
	}

	return {
		events,
		pending: '',
	};
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(input: string): ParsedInput => {
	const events: InputEvent[] = [];
	let index = 0;
	const pendingFrom = (pendingStartIndex: number): ParsedInput => ({
		events,
		pending: input.slice(pendingStartIndex),
	});

	while (index < input.length) {
		const escapeIndex = input.indexOf(escape, index);
		if (escapeIndex === -1) {
			splitControlBytes(input.slice(index), events);
			return {
				events,
				pending: '',
			};
		}

		if (escapeIndex > index) {
			splitControlBytes(input.slice(index, escapeIndex), events);
		}

		const parsedEscapeSequence = parseEscapeSequence(input, escapeIndex);
		if (parsedEscapeSequence === 'pending') {
			return pendingFrom(escapeIndex);
		}

		if (parsedEscapeSequence.sequence === pasteStart) {
			const afterStart = parsedEscapeSequence.nextIndex;
			const endIndex = input.indexOf(pasteEnd, afterStart);
			if (endIndex === -1) {
				return pendingFrom(escapeIndex);
			}

			events.push({paste: input.slice(afterStart, endIndex)});
			index = endIndex + pasteEnd.length;
			continue;
		}

		events.push(parsedEscapeSequence.sequence);
		index = parsedEscapeSequence.nextIndex;
	}

	return {
		events,
		pending: '',
	};
}
```


---

### 🔹 Commit #02: `1fcd380f`
- **完整 Hash**: `1fcd380f56cd4b0b700798549456c51c08a8f976`
- **說明 (Ground Truth)**: Avoid retaining an exit listener when waiting after unmount
- **變更檔案數**: 1

#### 📄 檔案: `src/ink.tsx`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:55, E:34, A:0) ➔ After(N:55, E:34, A:0)
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

### 🔹 函式: `waitUntilExit()`
- **變更前簽章 (Before)**: `waitUntilExit()` (L840~L850)
- **變更後簽章 (After)**: `waitUntilExit()` (L840~L850)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async waitUntilExit(): Promise<unknown> {
		if (!this.beforeExitHandler) {
			this.beforeExitHandler = () => {
				this.unmount();
			};

			process.once('beforeExit', this.beforeExitHandler);
		}

		return this.exitPromise;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async waitUntilExit(): Promise<unknown> {
		if (!this.isUnmounting && !this.beforeExitHandler) {
			this.beforeExitHandler = () => {
				this.unmount();
			};

			process.once('beforeExit', this.beforeExitHandler);
		}

		return this.exitPromise;
	}
```


---

### 🔹 Commit #03: `793fe59d`
- **完整 Hash**: `793fe59d3d19dba52a157028dce1ebb295a745cd`
- **說明 (Ground Truth)**: Fix `Static` rendering
- **變更檔案數**: 2

#### 📄 檔案: `src/components/Static.tsx`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:10, E:6, A:0) ➔ After(N:10, E:6, A:0)
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

### 🔹 函式: `Static()`
- **變更前簽章 (Before)**: `function Static<T>(props: Props<T>)` (L35~L71)
- **變更後簽章 (After)**: `function Static<T>(props: Props<T>)` (L35~L72)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function Static<T>(props: Props<T>) {
	const {items, children: render, style: customStyle} = props;
	const [index, setIndex] = useState(0);
	const inheritedBackgroundColor = useContext(backgroundContext);
	const effectiveBackgroundColor =
		// eslint-disable-next-line @typescript-eslint/prefer-nullish-coalescing -- Empty background colors inherit from the parent too.
		customStyle?.backgroundColor || inheritedBackgroundColor;

	const itemsToRender: T[] = useMemo(() => {
		return items.slice(index);
	}, [items, index]);

	useLayoutEffect(() => {
		setIndex(items.length);
	}, [items.length]);

	const children = itemsToRender.map((item, itemIndex): ReactNode => {
		return render(item, index + itemIndex);
	});

	const style: Styles = useMemo(
		() => ({
			position: 'absolute',
			flexDirection: 'column',
			...customStyle,
		}),
		[customStyle],
	);

	return (
		<backgroundContext.Provider value={effectiveBackgroundColor}>
			<ink-box internal_static style={style}>
				{children}
			</ink-box>
		</backgroundContext.Provider>
	);
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function Static<T>(props: Props<T>) {
	const {items, children: render, style: customStyle} = props;
	const [index, setIndex] = useState(0);
	const inheritedBackgroundColor = useContext(backgroundContext);
	const effectiveBackgroundColor =
		// eslint-disable-next-line @typescript-eslint/prefer-nullish-coalescing -- Empty background colors inherit from the parent too.
		customStyle?.backgroundColor || inheritedBackgroundColor;

	const itemsToRender: T[] = useMemo(() => {
		return items.slice(index);
	}, [items, index]);

	useLayoutEffect(() => {
		setIndex(items.length);
	}, [items.length]);

	const children = itemsToRender.map((item, itemIndex): ReactNode => {
		return render(item, index + itemIndex);
	});

	const style: Styles = useMemo(
		() => ({
			position: 'absolute',
			flexDirection: 'column',
			...customStyle,
			display: itemsToRender.length > 0 ? customStyle?.display : 'none',
		}),
		[customStyle, itemsToRender.length],
	);

	return (
		<backgroundContext.Provider value={effectiveBackgroundColor}>
			<ink-box internal_static style={style}>
				{children}
			</ink-box>
		</backgroundContext.Provider>
	);
}
```

### 🔹 函式: `style()`
- **變更前簽章 (Before)**: `style()` (L56~L60)
- **變更後簽章 (After)**: `style()` (L56~L61)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => ({
			position: 'absolute',
			flexDirection: 'column',
			...customStyle,
		})
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => ({
			position: 'absolute',
			flexDirection: 'column',
			...customStyle,
			display: itemsToRender.length > 0 ? customStyle?.display : 'none',
		})
```


#### 📄 檔案: `src/renderer.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:3, E:2, A:0) ➔ After(N:4, E:3, A:0)
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
  • + [新增節點] `getVisibleStaticNode` (FUNCTION_DEF)
  • + [新增呼叫邊] `renderer` ──[CALLS [guard: (node.yogaNode)]]──> `getVisibleStaticNode`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `renderer()`
- **變更前簽章 (Before)**: `renderer(node: DOMElement, isScreenReaderEnabled: boolean)` (L13~L75)
- **變更後簽章 (After)**: `renderer(node: DOMElement, isScreenReaderEnabled: boolean)` (L27~L98)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(node: DOMElement, isScreenReaderEnabled: boolean): Result => {
	if (node.yogaNode) {
		if (isScreenReaderEnabled) {
			const output = renderNodeToScreenReaderOutput(node, {
				skipStaticElements: true,
			});

			const outputHeight = output === '' ? 0 : output.split('\n').length;

			let staticOutput = '';

			if (node.staticNode) {
				staticOutput = renderNodeToScreenReaderOutput(node.staticNode, {
					skipStaticElements: false,
				});
			}

			return {
				output,
				outputHeight,
				staticOutput: staticOutput ? `${staticOutput}\n` : '',
			};
		}

		const output = new Output({
			width: node.yogaNode.getComputedWidth(),
			height: node.yogaNode.getComputedHeight(),
		});

		renderNodeToOutput(node, output, {
			skipStaticElements: true,
		});

		let staticOutput;

		if (node.staticNode?.yogaNode) {
			staticOutput = new Output({
				width: node.staticNode.yogaNode.getComputedWidth(),
				height: node.staticNode.yogaNode.getComputedHeight(),
			});

			renderNodeToOutput(node.staticNode, staticOutput, {
				skipStaticElements: false,
			});
		}

		const {output: generatedOutput, height: outputHeight} = output.get();

		return {
			output: generatedOutput,
			outputHeight,
			// Newline at the end is needed, because static output doesn't have one, so
			// interactive output will override last line of static output
			staticOutput: staticOutput ? `${staticOutput.get().output}\n` : '',
		};
	}

	return {
		output: '',
		outputHeight: 0,
		staticOutput: '',
	};
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(node: DOMElement, isScreenReaderEnabled: boolean): Result => {
	if (node.yogaNode) {
		const staticNode = getVisibleStaticNode(node.staticNode);

		if (isScreenReaderEnabled) {
			const output = renderNodeToScreenReaderOutput(node, {
				skipStaticElements: true,
			});

			const outputHeight = output === '' ? 0 : output.split('\n').length;

			let staticOutput = '';

			if (staticNode) {
				staticOutput = renderNodeToScreenReaderOutput(staticNode, {
					skipStaticElements: false,
				});
			}

			return {
				output,
				outputHeight,
				staticOutput: staticOutput ? `${staticOutput}\n` : '',
			};
		}

		const output = new Output({
			width: node.yogaNode.getComputedWidth(),
			height: node.yogaNode.getComputedHeight(),
		});

		renderNodeToOutput(node, output, {
			skipStaticElements: true,
		});

		let staticOutput;

		if (staticNode?.yogaNode) {
			const {yogaNode} = staticNode;
			staticOutput = new Output({
				width:
					yogaNode.getComputedLeft() +
					yogaNode.getComputedWidth() +
					yogaNode.getComputedMargin(Yoga.EDGE_RIGHT),
				height:
					yogaNode.getComputedTop() +
					yogaNode.getComputedHeight() +
					yogaNode.getComputedMargin(Yoga.EDGE_BOTTOM),
			});

			renderNodeToOutput(staticNode, staticOutput, {
				skipStaticElements: false,
			});
		}

		const {output: generatedOutput, height: outputHeight} = output.get();

		return {
			output: generatedOutput,
			outputHeight,
			// Newline at the end is needed, because static output doesn't have one, so
			// interactive output will override last line of static output
			staticOutput: staticOutput ? `${staticOutput.get().output}\n` : '',
		};
	}

	return {
		output: '',
		outputHeight: 0,
		staticOutput: '',
	};
}
```


---

### 🔹 Commit #04: `9f7c1d03`
- **完整 Hash**: `9f7c1d03cf38c574fa96d8a408cf379e82f7f4f6`
- **說明 (Ground Truth)**: Fix `renderToString` error handling
- **變更檔案數**: 1

#### 📄 檔案: `src/render-to-string.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:10, E:4, A:0) ➔ After(N:10, E:4, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 1, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `container` ──[CALLS [guarded]]──> `String (External/Unresolved)`
  • - [移除呼叫邊] `renderToString` ──[CALLS]──> `String (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `renderToString()`
- **變更前簽章 (Before)**: `renderToString(
	node: ReactNode,
	options?: RenderToStringOptions,
)` (L44~L156)
- **變更後簽章 (After)**: `renderToString(
	node: ReactNode,
	options?: RenderToStringOptions,
)` (L45~L160)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(
	node: ReactNode,
	options?: RenderToStringOptions,
): string => {
	const columns = options?.columns ?? 80;

	// Create a standalone root node — no stdout, stdin, or terminal bindings
	const rootNode: DOMElement = createNode('ink-root');

	// Capture static output from intermediate renders.
	// The <Static> component uses useLayoutEffect to clear its children after
	// the first commit. The reconciler's resetAfterCommit calls onImmediateRender
	// when static content is dirty (and returns early, skipping the normal
	// onRender callback), giving us a chance to capture it before it's cleared
	// by the subsequent re-render.
	let capturedStaticOutput = '';

	rootNode.onComputeLayout = () => {
		rootNode.yogaNode!.setWidth(columns);
		rootNode.yogaNode!.calculateLayout(
			undefined,
			undefined,
			Yoga.DIRECTION_LTR,
		);
	};

	rootNode.onImmediateRender = () => {
		const {staticOutput} = renderer(rootNode, false);
		if (staticOutput && staticOutput !== '\n') {
			capturedStaticOutput += staticOutput;
		}
	};

	// Capture the first uncaught error so we can re-throw it after cleanup.
	// React's reconciler catches component errors internally and reports them
	// via onUncaughtError rather than letting them propagate. For a synchronous
	// utility like renderToString, callers expect errors to throw.
	let uncaughtError: unknown;

	// Create a reconciler container in legacy (synchronous) mode.
	// The four trailing callbacks are: onUncaughtError, onCaughtError,
	// onRecoverableError, and onDefaultTransitionIndicator.
	// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
	const container = reconciler.createContainer(
		rootNode,
		LegacyRoot,
		null,
		false,
		null,
		'render-to-string',
		(error: unknown) => {
			uncaughtError ??= error;
		},
		() => {},
		() => {},
		() => {},
	);

	let teardownSucceeded = false;

	try {
		// Synchronously render the React tree into the container
		reconciler.updateContainerSync(node, container, null, () => {});
		reconciler.flushSyncWork();

		// Yoga layout has already been calculated by onComputeLayout during commit.
		// Render the DOM tree to a string — this captures the dynamic (non-static) output.
		const {output} = renderer(rootNode, false);

		// Tear down: unmount the tree so the reconciler cleans up child nodes
		// and runs effect cleanup functions. Child Yoga nodes are freed by the
		// reconciler's removeChildFromContainer → freeYogaSubtree → freeRecursive.
		reconciler.updateContainerSync(null, container, null, () => {});
		reconciler.flushSyncWork();
		teardownSucceeded = true;

		// Free the root yoga node itself (children already freed by reconciler)
		rootNode.yogaNode!.free();

		// Re-throw after full cleanup so callers see the original error.
		if (uncaughtError !== undefined) {
			throw uncaughtError instanceof Error
				? uncaughtError
				: // eslint-disable-next-line @typescript-eslint/no-base-to-string
					new Error(String(uncaughtError));
		}

		// The renderer appends a trailing newline to static output for terminal
		// rendering (so dynamic output starts on a fresh line). Strip it here
		// so renderToString returns clean output.
		const normalizedStaticOutput = capturedStaticOutput.endsWith('\n')
			? capturedStaticOutput.slice(0, -1)
			: capturedStaticOutput;

		if (normalizedStaticOutput && output) {
			return normalizedStaticOutput + '\n' + output;
		}

		return normalizedStaticOutput || output;
	} finally {
		// Ensure native Yoga memory is freed even if rendering or teardown threw.
		// Yoga nodes are WASM-backed and not garbage collected.
		if (!teardownSucceeded && rootNode.yogaNode) {
			try {
				// If reconciler teardown failed, some child nodes may not have been
				// freed. Use freeRecursive to clean up the entire tree as best-effort.
				rootNode.yogaNode.freeRecursive();
			} catch {
				// Best-effort: node may already be partially freed
			}
		}
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(
	node: ReactNode,
	options?: RenderToStringOptions,
): string => {
	const columns = options?.columns ?? 80;

	// Create a standalone root node — no stdout, stdin, or terminal bindings
	const rootNode: DOMElement = createNode('ink-root');

	// Capture static output from intermediate renders.
	// The <Static> component uses useLayoutEffect to clear its children after
	// the first commit. The reconciler's resetAfterCommit calls onImmediateRender
	// when static content is dirty (and returns early, skipping the normal
	// onRender callback), giving us a chance to capture it before it's cleared
	// by the subsequent re-render.
	let capturedStaticOutput = '';

	rootNode.onComputeLayout = () => {
		rootNode.yogaNode!.setWidth(columns);
		rootNode.yogaNode!.calculateLayout(
			undefined,
			undefined,
			Yoga.DIRECTION_LTR,
		);
	};

	rootNode.onImmediateRender = () => {
		const {staticOutput} = renderer(rootNode, false);
		if (staticOutput && staticOutput !== '\n') {
			capturedStaticOutput += staticOutput;
		}
	};

	// Capture the first uncaught error so we can re-throw it after cleanup.
	// React's reconciler catches component errors internally and reports them
	// via onUncaughtError rather than letting them propagate. For a synchronous
	// utility like renderToString, callers expect errors to throw.
	let uncaughtError: Error | undefined;

	// Create a reconciler container in legacy (synchronous) mode.
	// The four trailing callbacks are: onUncaughtError, onCaughtError,
	// onRecoverableError, and onDefaultTransitionIndicator.
	// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
	const container = reconciler.createContainer(
		rootNode,
		LegacyRoot,
		null,
		false,
		null,
		'render-to-string',
		(error: unknown) => {
			// eslint-disable-next-line @typescript-eslint/no-deprecated -- Error.isError is not available in Node.js 22.
			uncaughtError ??= types.isNativeError(error)
				? error
				: new Error(String(error));
		},
		() => {},
		() => {},
		() => {},
	);

	let teardownSucceeded = false;

	try {
		let output: string;
		try {
			// Synchronously render the React tree into the container
			reconciler.updateContainerSync(node, container, null, () => {});
			reconciler.flushSyncWork();

			// Yoga layout has already been calculated by onComputeLayout during commit.
			// Render the DOM tree to a string — this captures the dynamic (non-static) output.
			({output} = renderer(rootNode, false));
		} finally {
			// Tear down: unmount the tree so the reconciler cleans up child nodes
			// and runs effect cleanup functions. Child Yoga nodes are freed by the
			// reconciler's removeChildFromContainer → freeYogaSubtree → freeRecursive.
			reconciler.updateContainerSync(null, container, null, () => {});
			reconciler.flushSyncWork();
			teardownSucceeded = true;

			// Free the root yoga node itself (children already freed by reconciler)
			rootNode.yogaNode!.free();
		}

		// Re-throw after full cleanup so callers see the original error.
		if (uncaughtError !== undefined) {
			throw uncaughtError;
		}

		// The renderer appends a trailing newline to static output for terminal
		// rendering (so dynamic output starts on a fresh line). Strip it here
		// so renderToString returns clean output.
		const normalizedStaticOutput = capturedStaticOutput.endsWith('\n')
			? capturedStaticOutput.slice(0, -1)
			: capturedStaticOutput;

		if (normalizedStaticOutput && output) {
			return normalizedStaticOutput + '\n' + output;
		}

		return normalizedStaticOutput || output;
	} finally {
		// Ensure native Yoga memory is freed even if rendering or teardown threw.
		// Yoga nodes are WASM-backed and not garbage collected.
		if (!teardownSucceeded && rootNode.yogaNode) {
			try {
				// If reconciler teardown failed, some child nodes may not have been
				// freed. Use freeRecursive to clean up the entire tree as best-effort.
				rootNode.yogaNode.freeRecursive();
			} catch {
				// Best-effort: node may already be partially freed
			}
		}
	}
}
```

### 🔹 函式: `container()`
- **變更前簽章 (Before)**: `container(error: unknown)` (L94~L96)
- **變更後簽章 (After)**: `container(error: unknown)` (L95~L100)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(error: unknown) => {
			uncaughtError ??= error;
		}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(error: unknown) => {
			// eslint-disable-next-line @typescript-eslint/no-deprecated -- Error.isError is not available in Node.js 22.
			uncaughtError ??= types.isNativeError(error)
				? error
				: new Error(String(error));
		}
```


---

### 🔹 Commit #05: `fc685bc5`
- **完整 Hash**: `fc685bc560565f3114289660d8c177c9ad55c9b6`
- **說明 (Ground Truth)**: Fix node visibility and text measurement updates
- **變更檔案數**: 3

#### 📄 檔案: `src/dom.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:20, E:16, A:0) ➔ After(N:21, E:17, A:0)
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
  • + [新增節點] `setNodeHidden` (FUNCTION_DEF)
  • + [新增呼叫邊] `setNodeHidden` ──[CALLS [guard: (node.nodeName === 'ink-virtual-text')]]──> `markNodeAsDirty`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `setStyle()`
- **變更前簽章 (Before)**: `setStyle(node: DOMNode, style?: Styles)` (L226~L229)
- **變更後簽章 (After)**: `setStyle(node: DOMNode, style?: Styles)` (L227~L235)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(node: DOMNode, style?: Styles): void => {
	// Rendering code assumes style is always an object.
	node.style = style ?? {};
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(node: DOMNode, style?: Styles): void => {
	if (node.nodeName === 'ink-text' && node.style.textWrap !== style?.textWrap) {
		// Wrapping changes text measurements without changing any Yoga style.
		node.yogaNode?.markDirty();
	}

	// Rendering code assumes style is always an object.
	node.style = style ?? {};
}
```


#### 📄 檔案: `src/reconciler.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:61, E:22, A:0) ➔ After(N:62, E:24, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `setNodeHidden (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `hideInstance` ──[CALLS]──> `setNodeHidden (External/Unresolved)`
  • + [新增呼叫邊] `unhideInstance` ──[CALLS]──> `setNodeHidden (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `unhideInstance()`
- **變更前簽章 (Before)**: `unhideInstance(node)` (L316~L318)
- **變更後簽章 (After)**: `unhideInstance(node)` (L316~L318)

#### ◀️ 變更前實作碼 (Before Implementation):
```
unhideInstance(node) {
		node.yogaNode?.setDisplay(Yoga.DISPLAY_FLEX);
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
unhideInstance(node) {
		setNodeHidden(node, false);
	}
```

### 🔹 函式: `hideInstance()`
- **變更前簽章 (Before)**: `hideInstance(node)` (L313~L315)
- **變更後簽章 (After)**: `hideInstance(node)` (L313~L315)

#### ◀️ 變更前實作碼 (Before Implementation):
```
hideInstance(node) {
		node.yogaNode?.setDisplay(Yoga.DISPLAY_NONE);
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
hideInstance(node) {
		setNodeHidden(node, true);
	}
```


#### 📄 檔案: `src/squash-text-nodes.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:4, E:4, A:0) ➔ After(N:4, E:4, A:0)
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

### 🔹 函式: `squashTextNodes()`
- **變更前簽章 (Before)**: `squashTextNodes(node: DOMElement)` (L11~L52)
- **變更後簽章 (After)**: `squashTextNodes(node: DOMElement)` (L11~L56)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(node: DOMElement): string => {
	let text = '';

	for (const childNode of node.childNodes) {
		let nodeText = '';

		if (childNode.nodeName === '#text') {
			nodeText = childNode.nodeValue;
		} else {
			if (
				childNode.nodeName === 'ink-text' ||
				childNode.nodeName === 'ink-virtual-text'
			) {
				nodeText = squashTextNodes(childNode);
			}

			// Since these text nodes are being concatenated, `Output` instance won't be able to
			// apply children transform, so we have to do it manually here for each text node
			if (
				nodeText.length > 0 &&
				typeof childNode.internal_transform === 'function'
			) {
				const transform = childNode.internal_transform;
				nodeText = nodeText
					.split('\n')
					.map((line, lineIndex) => transform(line, lineIndex))
					.join('\n');
			}
		}

		text += nodeText;
	}

	text = sanitizeAnsi(text.replaceAll('\r\n', '\n'));

	// Expand tabs after combining nested text so measurement and rendering use the same columns.
	if (node.nodeName === 'ink-text' && text.includes('\t')) {
		text = wrapAnsi(text, Number.POSITIVE_INFINITY, {trim: false});
	}

	return text;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(node: DOMElement): string => {
	let text = '';

	for (const childNode of node.childNodes) {
		let nodeText = '';

		if (childNode.nodeName === '#text') {
			nodeText = childNode.nodeValue;
		} else {
			if (childNode.isHidden) {
				continue;
			}

			if (
				childNode.nodeName === 'ink-text' ||
				childNode.nodeName === 'ink-virtual-text'
			) {
				nodeText = squashTextNodes(childNode);
			}

			// Since these text nodes are being concatenated, `Output` instance won't be able to
			// apply children transform, so we have to do it manually here for each text node
			if (
				nodeText.length > 0 &&
				typeof childNode.internal_transform === 'function'
			) {
				const transform = childNode.internal_transform;
				nodeText = nodeText
					.split('\n')
					.map((line, lineIndex) => transform(line, lineIndex))
					.join('\n');
			}
		}

		text += nodeText;
	}

	text = sanitizeAnsi(text.replaceAll('\r\n', '\n'));

	// Expand tabs after combining nested text so measurement and rendering use the same columns.
	if (node.nodeName === 'ink-text' && text.includes('\t')) {
		text = wrapAnsi(text, Number.POSITIVE_INFINITY, {trim: false});
	}

	return text;
}
```


---

### 🔹 Commit #06: `f4803010`
- **完整 Hash**: `f48030107b6733a8de8f587b78adbd0cc59bf586`
- **說明 (Ground Truth)**: Fix screen-reader output
- **變更檔案數**: 3

#### 📄 檔案: `src/components/Text.tsx`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:4, E:2, A:0) ➔ After(N:4, E:2, A:0)
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

### 🔹 函式: `Text()`
- **變更前簽章 (Before)**: `function Text(` (L71~L151)
- **變更後簽章 (After)**: `function Text(` (L71~L151)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function Text({
	color,
	backgroundColor,
	dimColor = false,
	bold = false,
	italic = false,
	underline = false,
	strikethrough = false,
	inverse = false,
	wrap = 'wrap',
	children,
	'aria-label': ariaLabel,
	'aria-hidden': ariaHidden = false,
}: Props) {
	const {isScreenReaderEnabled} = useContext(accessibilityContext);
	const inheritedBackgroundColor = useContext(backgroundContext);
	// Use explicit backgroundColor if provided, otherwise inherit from the nearest parent Text or Box.
	const effectiveBackgroundColor = backgroundColor ?? inheritedBackgroundColor;
	const childrenOrAriaLabel =
		isScreenReaderEnabled && ariaLabel ? ariaLabel : children;

	if (childrenOrAriaLabel === undefined || childrenOrAriaLabel === null) {
		return null;
	}

	const transform = (children: string): string => {
		if (dimColor) {
			children = chalk.dim(children);
		}

		if (color) {
			children = colorize(children, color, 'foreground');
		}

		if (effectiveBackgroundColor) {
			children = colorize(children, effectiveBackgroundColor, 'background');
		}

		if (bold) {
			children = chalk.bold(children);
		}

		if (italic) {
			children = chalk.italic(children);
		}

		if (underline) {
			children = chalk.underline(children);
		}

		if (strikethrough) {
			children = chalk.strikethrough(children);
		}

		if (inverse) {
			children = chalk.inverse(children);
		}

		return children;
	};

	if (isScreenReaderEnabled && ariaHidden) {
		return null;
	}

	return (
		<backgroundContext.Provider value={effectiveBackgroundColor}>
			<ink-text
				style={{
					flexGrow: 0,
					flexShrink: 1,
					flexDirection: 'row',
					textWrap: wrap,
				}}
				internal_transform={transform}
			>
				{childrenOrAriaLabel}
			</ink-text>
		</backgroundContext.Provider>
	);
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function Text({
	color,
	backgroundColor,
	dimColor = false,
	bold = false,
	italic = false,
	underline = false,
	strikethrough = false,
	inverse = false,
	wrap = 'wrap',
	children,
	'aria-label': ariaLabel,
	'aria-hidden': ariaHidden = false,
}: Props) {
	const {isScreenReaderEnabled} = useContext(accessibilityContext);
	const inheritedBackgroundColor = useContext(backgroundContext);
	// Use explicit backgroundColor if provided, otherwise inherit from the nearest parent Text or Box.
	const effectiveBackgroundColor = backgroundColor ?? inheritedBackgroundColor;
	const childrenOrAriaLabel =
		isScreenReaderEnabled && ariaLabel ? ariaLabel : children;

	if (childrenOrAriaLabel === undefined || childrenOrAriaLabel === null) {
		return null;
	}

	const transform = (children: string): string => {
		if (dimColor) {
			children = chalk.dim(children);
		}

		if (color) {
			children = colorize(children, color, 'foreground');
		}

		if (effectiveBackgroundColor) {
			children = colorize(children, effectiveBackgroundColor, 'background');
		}

		if (bold) {
			children = chalk.bold(children);
		}

		if (italic) {
			children = chalk.italic(children);
		}

		if (underline) {
			children = chalk.underline(children);
		}

		if (strikethrough) {
			children = chalk.strikethrough(children);
		}

		if (inverse) {
			children = chalk.inverse(children);
		}

		return children;
	};

	if (isScreenReaderEnabled && ariaHidden) {
		return null;
	}

	return (
		<backgroundContext.Provider value={effectiveBackgroundColor}>
			<ink-text
				style={{
					flexGrow: 0,
					flexShrink: 1,
					flexDirection: 'row',
					textWrap: wrap,
				}}
				internal_transform={isScreenReaderEnabled ? undefined : transform}
			>
				{childrenOrAriaLabel}
			</ink-text>
		</backgroundContext.Provider>
	);
}
```


#### 📄 檔案: `src/components/Transform.tsx`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:2, E:1, A:0) ➔ After(N:2, E:1, A:0)
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

### 🔹 函式: `Transform()`
- **變更前簽章 (Before)**: `function Transform(` (L21~L42)
- **變更後簽章 (After)**: `function Transform(` (L21~L46)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function Transform({
	children,
	transform,
	accessibilityLabel,
}: Props) {
	const {isScreenReaderEnabled} = useContext(accessibilityContext);

	if (children === undefined || children === null) {
		return null;
	}

	return (
		<ink-text
			style={{flexGrow: 0, flexShrink: 1, flexDirection: 'row'}}
			internal_transform={transform}
		>
			{isScreenReaderEnabled && accessibilityLabel
				? accessibilityLabel
				: children}
		</ink-text>
	);
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function Transform({
	children,
	transform,
	accessibilityLabel,
}: Props) {
	const {isScreenReaderEnabled} = useContext(accessibilityContext);
	const childrenOrAccessibilityLabel = isScreenReaderEnabled
		? (accessibilityLabel ?? children)
		: children;

	if (
		childrenOrAccessibilityLabel === undefined ||
		childrenOrAccessibilityLabel === null
	) {
		return null;
	}

	return (
		<ink-text
			style={{flexGrow: 0, flexShrink: 1, flexDirection: 'row'}}
			internal_transform={isScreenReaderEnabled ? undefined : transform}
		>
			{childrenOrAccessibilityLabel}
		</ink-text>
	);
}
```


#### 📄 檔案: `src/ink.tsx`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:66, E:39, A:0) ➔ After(N:66, E:39, A:0)
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

### 🔹 Commit #07: `753a5f80`
- **完整 Hash**: `753a5f80f4dac9de1db01fa104ff1d023d1fb203`
- **說明 (Ground Truth)**: Fix background color inheritance
- **變更檔案數**: 3

#### 📄 檔案: `src/components/Box.tsx`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:4, E:1, A:0) ➔ After(N:4, E:1, A:0)
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

### 🔹 函式: `Box()`
- **變更前簽章 (Before)**: `Box(
		{
			children,
			backgroundColor,
			flexWrap = 'nowrap',
			flexDirection = 'row',
			'aria-label': ariaLabel,
			'aria-hidden': ariaHidden,
			'aria-role': role,
			'aria-state': ariaState,
			...style
		},
		ref,
	)` (L62~L114)
- **變更後簽章 (After)**: `Box(
		{
			children,
			backgroundColor,
			flexWrap = 'nowrap',
			flexDirection = 'row',
			'aria-label': ariaLabel,
			'aria-hidden': ariaHidden,
			'aria-role': role,
			'aria-state': ariaState,
			...style
		},
		ref,
	)` (L62~L114)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(
		{
			children,
			backgroundColor,
			flexWrap = 'nowrap',
			flexDirection = 'row',
			'aria-label': ariaLabel,
			'aria-hidden': ariaHidden,
			'aria-role': role,
			'aria-state': ariaState,
			...style
		},
		ref,
	) => {
		const {isScreenReaderEnabled} = useContext(accessibilityContext);
		const label = ariaLabel ? <ink-text>{ariaLabel}</ink-text> : undefined;
		if (isScreenReaderEnabled && ariaHidden) {
			return null;
		}

		const boxElement = (
			<ink-box
				ref={ref}
				style={{
					flexWrap,
					flexDirection,
					flexGrow: 0,
					flexShrink: 1,
					...style,
					backgroundColor,
					overflowX: style.overflowX ?? style.overflow ?? 'visible',
					overflowY: style.overflowY ?? style.overflow ?? 'visible',
				}}
				internal_accessibility={{
					role,
					state: ariaState,
				}}
			>
				{isScreenReaderEnabled && label ? label : children}
			</ink-box>
		);

		// If this Box has a background color, provide it to children via context
		if (backgroundColor) {
			return (
				<backgroundContext.Provider value={backgroundColor}>
					{boxElement}
				</backgroundContext.Provider>
			);
		}

		return boxElement;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(
		{
			children,
			backgroundColor,
			flexWrap = 'nowrap',
			flexDirection = 'row',
			'aria-label': ariaLabel,
			'aria-hidden': ariaHidden,
			'aria-role': role,
			'aria-state': ariaState,
			...style
		},
		ref,
	) => {
		const {isScreenReaderEnabled} = useContext(accessibilityContext);
		const inheritedBackgroundColor = useContext(backgroundContext);
		const effectiveBackgroundColor =
			// eslint-disable-next-line @typescript-eslint/prefer-nullish-coalescing -- Empty background colors inherit from the parent too.
			backgroundColor || inheritedBackgroundColor;
		const label = ariaLabel ? <ink-text>{ariaLabel}</ink-text> : undefined;
		if (isScreenReaderEnabled && ariaHidden) {
			return null;
		}

		const boxElement = (
			<ink-box
				ref={ref}
				style={{
					flexWrap,
					flexDirection,
					flexGrow: 0,
					flexShrink: 1,
					...style,
					backgroundColor,
					overflowX: style.overflowX ?? style.overflow ?? 'visible',
					overflowY: style.overflowY ?? style.overflow ?? 'visible',
				}}
				internal_accessibility={{
					role,
					state: ariaState,
				}}
			>
				{isScreenReaderEnabled && label ? label : children}
			</ink-box>
		);

		// Provide this Box's background color or its inherited color to children via context
		return (
			<backgroundContext.Provider value={effectiveBackgroundColor}>
				{boxElement}
			</backgroundContext.Provider>
		);
	}
```

### 🔹 函式: `Box()`
- **變更前簽章 (Before)**: `[Module State] Box` (L61~L115)
- **變更後簽章 (After)**: `[Module State] Box` (L61~L115)

#### ◀️ 變更前實作碼 (Before Implementation):
```
Box = forwardRef<DOMElement, PropsWithChildren<Props>>(
	(
		{
			children,
			backgroundColor,
			flexWrap = 'nowrap',
			flexDirection = 'row',
			'aria-label': ariaLabel,
			'aria-hidden': ariaHidden,
			'aria-role': role,
			'aria-state': ariaState,
			...style
		},
		ref,
	) => {
		const {isScreenReaderEnabled} = useContext(accessibilityContext);
		const label = ariaLabel ? <ink-text>{ariaLabel}</ink-text> : undefined;
		if (isScreenReaderEnabled && ariaHidden) {
			return null;
		}

		const boxElement = (
			<ink-box
				ref={ref}
				style={{
					flexWrap,
					flexDirection,
					flexGrow: 0,
					flexShrink: 1,
					...style,
					backgroundColor,
					overflowX: style.overflowX ?? style.overflow ?? 'visible',
					overflowY: style.overflowY ?? style.overflow ?? 'visible',
				}}
				internal_accessibility={{
					role,
					state: ariaState,
				}}
			>
				{isScreenReaderEnabled && label ? label : children}
			</ink-box>
		);

		// If this Box has a background color, provide it to children via context
		if (backgroundColor) {
			return (
				<backgroundContext.Provider value={backgroundColor}>
					{boxElement}
				</backgroundContext.Provider>
			);
		}

		return boxElement;
	},
)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
Box = forwardRef<DOMElement, PropsWithChildren<Props>>(
	(
		{
			children,
			backgroundColor,
			flexWrap = 'nowrap',
			flexDirection = 'row',
			'aria-label': ariaLabel,
			'aria-hidden': ariaHidden,
			'aria-role': role,
			'aria-state': ariaState,
			...style
		},
		ref,
	) => {
		const {isScreenReaderEnabled} = useContext(accessibilityContext);
		const inheritedBackgroundColor = useContext(backgroundContext);
		const effectiveBackgroundColor =
			// eslint-disable-next-line @typescript-eslint/prefer-nullish-coalescing -- Empty background colors inherit from the parent too.
			backgroundColor || inheritedBackgroundColor;
		const label = ariaLabel ? <ink-text>{ariaLabel}</ink-text> : undefined;
		if (isScreenReaderEnabled && ariaHidden) {
			return null;
		}

		const boxElement = (
			<ink-box
				ref={ref}
				style={{
					flexWrap,
					flexDirection,
					flexGrow: 0,
					flexShrink: 1,
					...style,
					backgroundColor,
					overflowX: style.overflowX ?? style.overflow ?? 'visible',
					overflowY: style.overflowY ?? style.overflow ?? 'visible',
				}}
				internal_accessibility={{
					role,
					state: ariaState,
				}}
			>
				{isScreenReaderEnabled && label ? label : children}
			</ink-box>
		);

		// Provide this Box's background color or its inherited color to children via context
		return (
			<backgroundContext.Provider value={effectiveBackgroundColor}>
				{boxElement}
			</backgroundContext.Provider>
		);
	},
)
```


#### 📄 檔案: `src/components/Static.tsx`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:9, E:5, A:0) ➔ After(N:10, E:6, A:0)
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
  • + [新增節點] `useContext (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Static` ──[CALLS]──> `useContext (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Static()`
- **變更前簽章 (Before)**: `function Static<T>(props: Props<T>)` (L28~L58)
- **變更後簽章 (After)**: `function Static<T>(props: Props<T>)` (L35~L71)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function Static<T>(props: Props<T>) {
	const {items, children: render, style: customStyle} = props;
	const [index, setIndex] = useState(0);

	const itemsToRender: T[] = useMemo(() => {
		return items.slice(index);
	}, [items, index]);

	useLayoutEffect(() => {
		setIndex(items.length);
	}, [items.length]);

	const children = itemsToRender.map((item, itemIndex): ReactNode => {
		return render(item, index + itemIndex);
	});

	const style: Styles = useMemo(
		() => ({
			position: 'absolute',
			flexDirection: 'column',
			...customStyle,
		}),
		[customStyle],
	);

	return (
		<ink-box internal_static style={style}>
			{children}
		</ink-box>
	);
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function Static<T>(props: Props<T>) {
	const {items, children: render, style: customStyle} = props;
	const [index, setIndex] = useState(0);
	const inheritedBackgroundColor = useContext(backgroundContext);
	const effectiveBackgroundColor =
		// eslint-disable-next-line @typescript-eslint/prefer-nullish-coalescing -- Empty background colors inherit from the parent too.
		customStyle?.backgroundColor || inheritedBackgroundColor;

	const itemsToRender: T[] = useMemo(() => {
		return items.slice(index);
	}, [items, index]);

	useLayoutEffect(() => {
		setIndex(items.length);
	}, [items.length]);

	const children = itemsToRender.map((item, itemIndex): ReactNode => {
		return render(item, index + itemIndex);
	});

	const style: Styles = useMemo(
		() => ({
			position: 'absolute',
			flexDirection: 'column',
			...customStyle,
		}),
		[customStyle],
	);

	return (
		<backgroundContext.Provider value={effectiveBackgroundColor}>
			<ink-box internal_static style={style}>
				{children}
			</ink-box>
		</backgroundContext.Provider>
	);
}
```


#### 📄 檔案: `src/components/Text.tsx`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:4, E:2, A:0) ➔ After(N:4, E:2, A:0)
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

### 🔹 函式: `Text()`
- **變更前簽章 (Before)**: `function Text(` (L71~L145)
- **變更後簽章 (After)**: `function Text(` (L71~L151)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function Text({
	color,
	backgroundColor,
	dimColor = false,
	bold = false,
	italic = false,
	underline = false,
	strikethrough = false,
	inverse = false,
	wrap = 'wrap',
	children,
	'aria-label': ariaLabel,
	'aria-hidden': ariaHidden = false,
}: Props) {
	const {isScreenReaderEnabled} = useContext(accessibilityContext);
	const inheritedBackgroundColor = useContext(backgroundContext);
	const childrenOrAriaLabel =
		isScreenReaderEnabled && ariaLabel ? ariaLabel : children;

	if (childrenOrAriaLabel === undefined || childrenOrAriaLabel === null) {
		return null;
	}

	const transform = (children: string): string => {
		if (dimColor) {
			children = chalk.dim(children);
		}

		if (color) {
			children = colorize(children, color, 'foreground');
		}

		// Use explicit backgroundColor if provided, otherwise use inherited from parent Box
		const effectiveBackgroundColor =
			backgroundColor ?? inheritedBackgroundColor;
		if (effectiveBackgroundColor) {
			children = colorize(children, effectiveBackgroundColor, 'background');
		}

		if (bold) {
			children = chalk.bold(children);
		}

		if (italic) {
			children = chalk.italic(children);
		}

		if (underline) {
			children = chalk.underline(children);
		}

		if (strikethrough) {
			children = chalk.strikethrough(children);
		}

		if (inverse) {
			children = chalk.inverse(children);
		}

		return children;
	};

	if (isScreenReaderEnabled && ariaHidden) {
		return null;
	}

	return (
		<ink-text
			style={{flexGrow: 0, flexShrink: 1, flexDirection: 'row', textWrap: wrap}}
			internal_transform={transform}
		>
			{childrenOrAriaLabel}
		</ink-text>
	);
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function Text({
	color,
	backgroundColor,
	dimColor = false,
	bold = false,
	italic = false,
	underline = false,
	strikethrough = false,
	inverse = false,
	wrap = 'wrap',
	children,
	'aria-label': ariaLabel,
	'aria-hidden': ariaHidden = false,
}: Props) {
	const {isScreenReaderEnabled} = useContext(accessibilityContext);
	const inheritedBackgroundColor = useContext(backgroundContext);
	// Use explicit backgroundColor if provided, otherwise inherit from the nearest parent Text or Box.
	const effectiveBackgroundColor = backgroundColor ?? inheritedBackgroundColor;
	const childrenOrAriaLabel =
		isScreenReaderEnabled && ariaLabel ? ariaLabel : children;

	if (childrenOrAriaLabel === undefined || childrenOrAriaLabel === null) {
		return null;
	}

	const transform = (children: string): string => {
		if (dimColor) {
			children = chalk.dim(children);
		}

		if (color) {
			children = colorize(children, color, 'foreground');
		}

		if (effectiveBackgroundColor) {
			children = colorize(children, effectiveBackgroundColor, 'background');
		}

		if (bold) {
			children = chalk.bold(children);
		}

		if (italic) {
			children = chalk.italic(children);
		}

		if (underline) {
			children = chalk.underline(children);
		}

		if (strikethrough) {
			children = chalk.strikethrough(children);
		}

		if (inverse) {
			children = chalk.inverse(children);
		}

		return children;
	};

	if (isScreenReaderEnabled && ariaHidden) {
		return null;
	}

	return (
		<backgroundContext.Provider value={effectiveBackgroundColor}>
			<ink-text
				style={{
					flexGrow: 0,
					flexShrink: 1,
					flexDirection: 'row',
					textWrap: wrap,
				}}
				internal_transform={transform}
			>
				{childrenOrAriaLabel}
			</ink-text>
		</backgroundContext.Provider>
	);
}
```

### 🔹 函式: `transform()`
- **變更前簽章 (Before)**: `transform(children: string)` (L94~L131)
- **變更後簽章 (After)**: `transform(children: string)` (L96~L130)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(children: string): string => {
		if (dimColor) {
			children = chalk.dim(children);
		}

		if (color) {
			children = colorize(children, color, 'foreground');
		}

		// Use explicit backgroundColor if provided, otherwise use inherited from parent Box
		const effectiveBackgroundColor =
			backgroundColor ?? inheritedBackgroundColor;
		if (effectiveBackgroundColor) {
			children = colorize(children, effectiveBackgroundColor, 'background');
		}

		if (bold) {
			children = chalk.bold(children);
		}

		if (italic) {
			children = chalk.italic(children);
		}

		if (underline) {
			children = chalk.underline(children);
		}

		if (strikethrough) {
			children = chalk.strikethrough(children);
		}

		if (inverse) {
			children = chalk.inverse(children);
		}

		return children;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(children: string): string => {
		if (dimColor) {
			children = chalk.dim(children);
		}

		if (color) {
			children = colorize(children, color, 'foreground');
		}

		if (effectiveBackgroundColor) {
			children = colorize(children, effectiveBackgroundColor, 'background');
		}

		if (bold) {
			children = chalk.bold(children);
		}

		if (italic) {
			children = chalk.italic(children);
		}

		if (underline) {
			children = chalk.underline(children);
		}

		if (strikethrough) {
			children = chalk.strikethrough(children);
		}

		if (inverse) {
			children = chalk.inverse(children);
		}

		return children;
	}
```


---

### 🔹 Commit #08: `81e24516`
- **完整 Hash**: `81e24516120f09db2607f7dc23481893a86b4008`
- **說明 (Ground Truth)**: Fix error reporting
- **變更檔案數**: 2

#### 📄 檔案: `src/components/ErrorBoundary.tsx`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:3, E:0, A:0) ➔ After(N:4, E:1, A:0)
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
  • + [新增節點] `String (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `getDerivedStateFromError` ──[CALLS [guarded]]──> `String (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `getDerivedStateFromError()`
- **變更前簽章 (Before)**: `getDerivedStateFromError(error: Error)` (L18~L20)
- **變更後簽章 (After)**: `getDerivedStateFromError(error: unknown)` (L19~L24)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static getDerivedStateFromError(error: Error) {
		return {error};
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static getDerivedStateFromError(error: unknown) {
		return {
			// eslint-disable-next-line @typescript-eslint/no-deprecated -- Error.isError is not available in Node.js 22.
			error: types.isNativeError(error) ? error : new Error(String(error)),
		};
	}
```

### 🔹 函式: `componentDidCatch()`
- **變更前簽章 (Before)**: `componentDidCatch(error: Error)` (L26~L28)
- **變更後簽章 (After)**: `componentDidCatch()` (L30~L32)

#### ◀️ 變更前實作碼 (Before Implementation):
```
override componentDidCatch(error: Error): void {
		this.props.onError(error);
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
override componentDidCatch(): void {
		this.props.onError(this.state.error!);
	}
```


#### 📄 檔案: `src/components/ErrorOverview.tsx`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:6, E:4, A:0) ➔ After(N:8, E:6, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `relative (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `fileURLToPath (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `cleanupPath` ──[CALLS [guarded]]──> `relative (External/Unresolved)`
  • + [新增呼叫邊] `cleanupPath` ──[CALLS [guarded]]──> `fileURLToPath (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `cleanupPath()`
- **變更前簽章 (Before)**: `cleanupPath(path: string | undefined)` (L11~L13)
- **變更後簽章 (After)**: `cleanupPath(path: string | undefined)` (L13~L17)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(path: string | undefined): string | undefined => {
	return path?.replace(`file://${cwd()}/`, '');
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(path: string | undefined): string | undefined => {
	return path?.startsWith('file://')
		? relative(cwd(), fileURLToPath(path))
		: path;
}
```

### 🔹 函式: `ErrorOverview()`
- **變更前簽章 (Before)**: `function ErrorOverview(` (L24~L143)
- **變更後簽章 (After)**: `function ErrorOverview(` (L28~L150)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function ErrorOverview({error}: Props) {
	const stack = error.stack ? error.stack.split('\n').slice(1) : undefined;
	const origin = stack ? stackUtils.parseLine(stack[0]!) : undefined;
	const filePath = cleanupPath(origin?.file);
	let excerpt: CodeExcerpt[] | undefined;
	let lineWidth = 0;
	const stackLineCounts = new Map<string, number>();

	if (filePath && origin?.line && fs.existsSync(filePath)) {
		const sourceCode = fs.readFileSync(filePath, 'utf8');
		excerpt = codeExcerpt(sourceCode, origin.line);

		if (excerpt) {
			for (const {line} of excerpt) {
				lineWidth = Math.max(lineWidth, String(line).length);
			}
		}
	}

	return (
		<Box flexDirection="column" padding={1}>
			<Box>
				<Text backgroundColor="red" color="white">
					{' '}
					ERROR{' '}
				</Text>

				<Text> {error.message}</Text>
			</Box>

			{origin && filePath ? (
				<Box marginTop={1}>
					<Text dimColor>
						{filePath}:{origin.line}:{origin.column}
					</Text>
				</Box>
			) : null}

			{origin && excerpt ? (
				<Box marginTop={1} flexDirection="column">
					{excerpt.map(({line, value}) => (
						<Box key={line}>
							<Box width={lineWidth + 1}>
								<Text
									dimColor={line !== origin.line}
									backgroundColor={line === origin.line ? 'red' : undefined}
									color={line === origin.line ? 'white' : undefined}
									aria-label={
										line === origin.line
											? `Line ${line}, error`
											: `Line ${line}`
									}
								>
									{String(line).padStart(lineWidth, ' ')}:
								</Text>
							</Box>

							<Text
								key={line}
								backgroundColor={line === origin.line ? 'red' : undefined}
								color={line === origin.line ? 'white' : undefined}
							>
								{' ' + value}
							</Text>
						</Box>
					))}
				</Box>
			) : null}

			{error.stack ? (
				<Box marginTop={1} flexDirection="column">
					{error.stack
						.split('\n')
						.slice(1)
						.map(line => {
							const parsedLine = stackUtils.parseLine(line);
							const lineCount = stackLineCounts.get(line) ?? 0;
							stackLineCounts.set(line, lineCount + 1);
							const key = `${line}-${lineCount}`;

							// If the line from the stack cannot be parsed, or parsed into an incomplete
							// frame without source location data (for example, "at native"), we print
							// out the unparsed line.
							if (!parsedLine?.file || !parsedLine.line || !parsedLine.column) {
								return (
									<Box key={key}>
										<Text dimColor>- </Text>
										<Text dimColor bold>
											{line}
											\t{' '}
										</Text>
									</Box>
								);
							}

							return (
								<Box key={key}>
									<Text dimColor>- </Text>
									<Text dimColor bold>
										{parsedLine.function}
									</Text>
									<Text
										dimColor
										color="gray"
										aria-label={`at ${
											cleanupPath(parsedLine.file) ?? ''
										} line ${parsedLine.line} column ${parsedLine.column}`}
									>
										{' '}
										({cleanupPath(parsedLine.file) ?? ''}:{parsedLine.line}:
										{parsedLine.column})
									</Text>
								</Box>
							);
						})}
				</Box>
			) : null}
		</Box>
	);
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function ErrorOverview({error}: Props) {
	const stack = error.stack
		?.split('\n')
		.slice(error.message.split('\n').length);
	const origin = stack ? stackUtils.parseLine(stack[0]!) : undefined;
	const filePath = cleanupPath(origin?.file);
	let excerpt: CodeExcerpt[] | undefined;
	let lineWidth = 0;
	const stackLineCounts = new Map<string, number>();

	if (filePath && origin?.line) {
		try {
			const sourceCode = fs.readFileSync(filePath, 'utf8');
			excerpt = codeExcerpt(sourceCode, origin.line);
		} catch {
			// Source excerpts are best-effort and must not hide the original error.
		}

		if (excerpt) {
			for (const {line} of excerpt) {
				lineWidth = Math.max(lineWidth, String(line).length);
			}
		}
	}

	return (
		<Box flexDirection="column" padding={1}>
			<Box>
				<Text backgroundColor="red" color="white">
					{' '}
					ERROR{' '}
				</Text>

				<Text> {error.message}</Text>
			</Box>

			{origin && filePath ? (
				<Box marginTop={1}>
					<Text dimColor>
						{filePath}:{origin.line}:{origin.column}
					</Text>
				</Box>
			) : null}

			{origin && excerpt ? (
				<Box marginTop={1} flexDirection="column">
					{excerpt.map(({line, value}) => (
						<Box key={line}>
							<Box width={lineWidth + 1}>
								<Text
									dimColor={line !== origin.line}
									backgroundColor={line === origin.line ? 'red' : undefined}
									color={line === origin.line ? 'white' : undefined}
									aria-label={
										line === origin.line
											? `Line ${line}, error`
											: `Line ${line}`
									}
								>
									{String(line).padStart(lineWidth, ' ')}:
								</Text>
							</Box>

							<Text
								key={line}
								backgroundColor={line === origin.line ? 'red' : undefined}
								color={line === origin.line ? 'white' : undefined}
							>
								{' ' + value}
							</Text>
						</Box>
					))}
				</Box>
			) : null}

			{stack ? (
				<Box marginTop={1} flexDirection="column">
					{stack.map(line => {
						const parsedLine = stackUtils.parseLine(line);
						const lineCount = stackLineCounts.get(line) ?? 0;
						stackLineCounts.set(line, lineCount + 1);
						const key = `${line}-${lineCount}`;

						// If the line from the stack cannot be parsed, or parsed into an incomplete
						// frame without source location data (for example, "at native"), we print
						// out the unparsed line.
						if (!parsedLine?.file || !parsedLine.line || !parsedLine.column) {
							return (
								<Box key={key}>
									<Text dimColor>- </Text>
									<Text dimColor bold>
										{line}
										\t{' '}
									</Text>
								</Box>
							);
						}

						return (
							<Box key={key}>
								<Text dimColor>- </Text>
								<Text dimColor bold>
									{parsedLine.function}
								</Text>
								<Text
									dimColor
									color="gray"
									aria-label={`at ${
										cleanupPath(parsedLine.file) ?? ''
									} line ${parsedLine.line} column ${parsedLine.column}`}
								>
									{' '}
									({cleanupPath(parsedLine.file) ?? ''}:{parsedLine.line}:
									{parsedLine.column})
								</Text>
							</Box>
						);
					})}
				</Box>
			) : null}
		</Box>
	);
}
```


---

### 🔹 Commit #09: `fab670b6`
- **完整 Hash**: `fab670b67480346797f5f0a955872e58d2215096`
- **說明 (Ground Truth)**: Fix useWindowSize missing resizes before subscription
- **變更檔案數**: 1

#### 📄 檔案: `src/hooks/use-window-size.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:8, E:6, A:0) ➔ After(N:8, E:7, A:0)
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
  • + [新增呼叫邊] `useWindowSize` ──[CALLS]──> `onResize`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `useWindowSize()`
- **變更前簽章 (Before)**: `useWindowSize()` (L23~L40)
- **變更後簽章 (After)**: `useWindowSize()` (L23~L41)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(): WindowSize => {
	const {stdout} = useStdout();
	const [size, setSize] = useState<WindowSize>(() => getWindowSize(stdout));

	useEffect(() => {
		const onResize = () => {
			setSize(getWindowSize(stdout));
		};

		stdout.on('resize', onResize);

		return () => {
			stdout.off('resize', onResize);
		};
	}, [stdout]);

	return size;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(): WindowSize => {
	const {stdout} = useStdout();
	const [size, setSize] = useState<WindowSize>(() => getWindowSize(stdout));

	useEffect(() => {
		const onResize = () => {
			setSize(getWindowSize(stdout));
		};

		stdout.on('resize', onResize);
		onResize();

		return () => {
			stdout.off('resize', onResize);
		};
	}, [stdout]);

	return size;
}
```


---

### 🔹 Commit #10: `274b15ad`
- **完整 Hash**: `274b15ad1063057216c60febeefe40da9a968bed`
- **說明 (Ground Truth)**: Fix layout style handling
- **變更檔案數**: 2

#### 📄 檔案: `src/components/Box.tsx`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:4, E:1, A:0) ➔ After(N:4, E:1, A:0)
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

### 🔹 函式: `Box()`
- **變更前簽章 (Before)**: `Box(
		{
			children,
			backgroundColor,
			'aria-label': ariaLabel,
			'aria-hidden': ariaHidden,
			'aria-role': role,
			'aria-state': ariaState,
			...style
		},
		ref,
	)` (L62~L112)
- **變更後簽章 (After)**: `Box(
		{
			children,
			backgroundColor,
			flexWrap = 'nowrap',
			flexDirection = 'row',
			'aria-label': ariaLabel,
			'aria-hidden': ariaHidden,
			'aria-role': role,
			'aria-state': ariaState,
			...style
		},
		ref,
	)` (L62~L114)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(
		{
			children,
			backgroundColor,
			'aria-label': ariaLabel,
			'aria-hidden': ariaHidden,
			'aria-role': role,
			'aria-state': ariaState,
			...style
		},
		ref,
	) => {
		const {isScreenReaderEnabled} = useContext(accessibilityContext);
		const label = ariaLabel ? <ink-text>{ariaLabel}</ink-text> : undefined;
		if (isScreenReaderEnabled && ariaHidden) {
			return null;
		}

		const boxElement = (
			<ink-box
				ref={ref}
				style={{
					flexWrap: 'nowrap',
					flexDirection: 'row',
					flexGrow: 0,
					flexShrink: 1,
					...style,
					backgroundColor,
					overflowX: style.overflowX ?? style.overflow ?? 'visible',
					overflowY: style.overflowY ?? style.overflow ?? 'visible',
				}}
				internal_accessibility={{
					role,
					state: ariaState,
				}}
			>
				{isScreenReaderEnabled && label ? label : children}
			</ink-box>
		);

		// If this Box has a background color, provide it to children via context
		if (backgroundColor) {
			return (
				<backgroundContext.Provider value={backgroundColor}>
					{boxElement}
				</backgroundContext.Provider>
			);
		}

		return boxElement;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(
		{
			children,
			backgroundColor,
			flexWrap = 'nowrap',
			flexDirection = 'row',
			'aria-label': ariaLabel,
			'aria-hidden': ariaHidden,
			'aria-role': role,
			'aria-state': ariaState,
			...style
		},
		ref,
	) => {
		const {isScreenReaderEnabled} = useContext(accessibilityContext);
		const label = ariaLabel ? <ink-text>{ariaLabel}</ink-text> : undefined;
		if (isScreenReaderEnabled && ariaHidden) {
			return null;
		}

		const boxElement = (
			<ink-box
				ref={ref}
				style={{
					flexWrap,
					flexDirection,
					flexGrow: 0,
					flexShrink: 1,
					...style,
					backgroundColor,
					overflowX: style.overflowX ?? style.overflow ?? 'visible',
					overflowY: style.overflowY ?? style.overflow ?? 'visible',
				}}
				internal_accessibility={{
					role,
					state: ariaState,
				}}
			>
				{isScreenReaderEnabled && label ? label : children}
			</ink-box>
		);

		// If this Box has a background color, provide it to children via context
		if (backgroundColor) {
			return (
				<backgroundContext.Provider value={backgroundColor}>
					{boxElement}
				</backgroundContext.Provider>
			);
		}

		return boxElement;
	}
```

### 🔹 函式: `Box()`
- **變更前簽章 (Before)**: `[Module State] Box` (L61~L113)
- **變更後簽章 (After)**: `[Module State] Box` (L61~L115)

#### ◀️ 變更前實作碼 (Before Implementation):
```
Box = forwardRef<DOMElement, PropsWithChildren<Props>>(
	(
		{
			children,
			backgroundColor,
			'aria-label': ariaLabel,
			'aria-hidden': ariaHidden,
			'aria-role': role,
			'aria-state': ariaState,
			...style
		},
		ref,
	) => {
		const {isScreenReaderEnabled} = useContext(accessibilityContext);
		const label = ariaLabel ? <ink-text>{ariaLabel}</ink-text> : undefined;
		if (isScreenReaderEnabled && ariaHidden) {
			return null;
		}

		const boxElement = (
			<ink-box
				ref={ref}
				style={{
					flexWrap: 'nowrap',
					flexDirection: 'row',
					flexGrow: 0,
					flexShrink: 1,
					...style,
					backgroundColor,
					overflowX: style.overflowX ?? style.overflow ?? 'visible',
					overflowY: style.overflowY ?? style.overflow ?? 'visible',
				}}
				internal_accessibility={{
					role,
					state: ariaState,
				}}
			>
				{isScreenReaderEnabled && label ? label : children}
			</ink-box>
		);

		// If this Box has a background color, provide it to children via context
		if (backgroundColor) {
			return (
				<backgroundContext.Provider value={backgroundColor}>
					{boxElement}
				</backgroundContext.Provider>
			);
		}

		return boxElement;
	},
)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
Box = forwardRef<DOMElement, PropsWithChildren<Props>>(
	(
		{
			children,
			backgroundColor,
			flexWrap = 'nowrap',
			flexDirection = 'row',
			'aria-label': ariaLabel,
			'aria-hidden': ariaHidden,
			'aria-role': role,
			'aria-state': ariaState,
			...style
		},
		ref,
	) => {
		const {isScreenReaderEnabled} = useContext(accessibilityContext);
		const label = ariaLabel ? <ink-text>{ariaLabel}</ink-text> : undefined;
		if (isScreenReaderEnabled && ariaHidden) {
			return null;
		}

		const boxElement = (
			<ink-box
				ref={ref}
				style={{
					flexWrap,
					flexDirection,
					flexGrow: 0,
					flexShrink: 1,
					...style,
					backgroundColor,
					overflowX: style.overflowX ?? style.overflow ?? 'visible',
					overflowY: style.overflowY ?? style.overflow ?? 'visible',
				}}
				internal_accessibility={{
					role,
					state: ariaState,
				}}
			>
				{isScreenReaderEnabled && label ? label : children}
			</ink-box>
		);

		// If this Box has a background color, provide it to children via context
		if (backgroundColor) {
			return (
				<backgroundContext.Provider value={backgroundColor}>
					{boxElement}
				</backgroundContext.Provider>
			);
		}

		return boxElement;
	},
)
```


#### 📄 檔案: `src/styles.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:10, E:8, A:0) ➔ After(N:10, E:8, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 6, ΔTrans: 0
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

### 🔹 函式: `applyGapStyles()`
- **變更前簽章 (Before)**: `applyGapStyles(node: YogaNode, style: Styles)` (L774~L786)
- **變更後簽章 (After)**: `applyGapStyles(node: YogaNode, style: Styles)` (L774~L786)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(node: YogaNode, style: Styles): void => {
	if ('gap' in style) {
		node.setGap(Yoga.GUTTER_ALL, style.gap ?? 0);
	}

	if ('columnGap' in style) {
		node.setGap(Yoga.GUTTER_COLUMN, style.columnGap ?? 0);
	}

	if ('rowGap' in style) {
		node.setGap(Yoga.GUTTER_ROW, style.rowGap ?? 0);
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(node: YogaNode, style: Styles): void => {
	if ('gap' in style) {
		node.setGap(Yoga.GUTTER_ALL, style.gap ?? 0);
	}

	if ('columnGap' in style) {
		node.setGap(Yoga.GUTTER_COLUMN, style.columnGap);
	}

	if ('rowGap' in style) {
		node.setGap(Yoga.GUTTER_ROW, style.rowGap);
	}
}
```

### 🔹 函式: `applyDisplayStyles()`
- **變更前簽章 (Before)**: `applyDisplayStyles(node: YogaNode, style: Styles)` (L730~L736)
- **變更後簽章 (After)**: `applyDisplayStyles(node: YogaNode, style: Styles)` (L730~L736)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(node: YogaNode, style: Styles): void => {
	if ('display' in style) {
		node.setDisplay(
			style.display === 'flex' ? Yoga.DISPLAY_FLEX : Yoga.DISPLAY_NONE,
		);
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(node: YogaNode, style: Styles): void => {
	if ('display' in style) {
		node.setDisplay(
			style.display === 'none' ? Yoga.DISPLAY_NONE : Yoga.DISPLAY_FLEX,
		);
	}
}
```

### 🔹 函式: `applyPaddingStyles()`
- **變更前簽章 (Before)**: `applyPaddingStyles(node: YogaNode, style: Styles)` (L483~L511)
- **變更後簽章 (After)**: `applyPaddingStyles(node: YogaNode, style: Styles)` (L483~L511)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(node: YogaNode, style: Styles): void => {
	if ('padding' in style) {
		node.setPadding(Yoga.EDGE_ALL, style.padding ?? 0);
	}

	if ('paddingX' in style) {
		node.setPadding(Yoga.EDGE_HORIZONTAL, style.paddingX ?? 0);
	}

	if ('paddingY' in style) {
		node.setPadding(Yoga.EDGE_VERTICAL, style.paddingY ?? 0);
	}

	if ('paddingLeft' in style) {
		node.setPadding(Yoga.EDGE_LEFT, style.paddingLeft ?? 0);
	}

	if ('paddingRight' in style) {
		node.setPadding(Yoga.EDGE_RIGHT, style.paddingRight ?? 0);
	}

	if ('paddingTop' in style) {
		node.setPadding(Yoga.EDGE_TOP, style.paddingTop ?? 0);
	}

	if ('paddingBottom' in style) {
		node.setPadding(Yoga.EDGE_BOTTOM, style.paddingBottom ?? 0);
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(node: YogaNode, style: Styles): void => {
	if ('padding' in style) {
		node.setPadding(Yoga.EDGE_ALL, style.padding ?? 0);
	}

	if ('paddingX' in style) {
		node.setPadding(Yoga.EDGE_HORIZONTAL, style.paddingX);
	}

	if ('paddingY' in style) {
		node.setPadding(Yoga.EDGE_VERTICAL, style.paddingY);
	}

	if ('paddingLeft' in style) {
		node.setPadding(Yoga.EDGE_LEFT, style.paddingLeft);
	}

	if ('paddingRight' in style) {
		node.setPadding(Yoga.EDGE_RIGHT, style.paddingRight);
	}

	if ('paddingTop' in style) {
		node.setPadding(Yoga.EDGE_TOP, style.paddingTop);
	}

	if ('paddingBottom' in style) {
		node.setPadding(Yoga.EDGE_BOTTOM, style.paddingBottom);
	}
}
```

### 🔹 函式: `applyDimensionStyles()`
- **變更前簽章 (Before)**: `applyDimensionStyles(node: YogaNode, style: Styles)` (L672~L728)
- **變更後簽章 (After)**: `applyDimensionStyles(node: YogaNode, style: Styles)` (L672~L728)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(node: YogaNode, style: Styles): void => {
	if ('width' in style) {
		if (typeof style.width === 'number') {
			node.setWidth(style.width);
		} else if (typeof style.width === 'string') {
			node.setWidthPercent(Number.parseInt(style.width, 10));
		} else {
			node.setWidthAuto();
		}
	}

	if ('height' in style) {
		if (typeof style.height === 'number') {
			node.setHeight(style.height);
		} else if (typeof style.height === 'string') {
			node.setHeightPercent(Number.parseInt(style.height, 10));
		} else {
			node.setHeightAuto();
		}
	}

	if ('minWidth' in style) {
		if (typeof style.minWidth === 'string') {
			node.setMinWidthPercent(Number.parseInt(style.minWidth, 10));
		} else {
			node.setMinWidth(style.minWidth ?? 0);
		}
	}

	if ('minHeight' in style) {
		if (typeof style.minHeight === 'string') {
			node.setMinHeightPercent(Number.parseInt(style.minHeight, 10));
		} else {
			node.setMinHeight(style.minHeight ?? 0);
		}
	}

	if ('maxWidth' in style) {
		if (typeof style.maxWidth === 'string') {
			node.setMaxWidthPercent(Number.parseInt(style.maxWidth, 10));
		} else {
			node.setMaxWidth(style.maxWidth);
		}
	}

	if ('maxHeight' in style) {
		if (typeof style.maxHeight === 'string') {
			node.setMaxHeightPercent(Number.parseInt(style.maxHeight, 10));
		} else {
			node.setMaxHeight(style.maxHeight);
		}
	}

	if ('aspectRatio' in style) {
		node.setAspectRatio(style.aspectRatio);
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(node: YogaNode, style: Styles): void => {
	if ('width' in style) {
		if (typeof style.width === 'number') {
			node.setWidth(style.width);
		} else if (typeof style.width === 'string') {
			node.setWidthPercent(Number.parseFloat(style.width));
		} else {
			node.setWidthAuto();
		}
	}

	if ('height' in style) {
		if (typeof style.height === 'number') {
			node.setHeight(style.height);
		} else if (typeof style.height === 'string') {
			node.setHeightPercent(Number.parseFloat(style.height));
		} else {
			node.setHeightAuto();
		}
	}

	if ('minWidth' in style) {
		if (typeof style.minWidth === 'string') {
			node.setMinWidthPercent(Number.parseFloat(style.minWidth));
		} else {
			node.setMinWidth(style.minWidth ?? 0);
		}
	}

	if ('minHeight' in style) {
		if (typeof style.minHeight === 'string') {
			node.setMinHeightPercent(Number.parseFloat(style.minHeight));
		} else {
			node.setMinHeight(style.minHeight ?? 0);
		}
	}

	if ('maxWidth' in style) {
		if (typeof style.maxWidth === 'string') {
			node.setMaxWidthPercent(Number.parseFloat(style.maxWidth));
		} else {
			node.setMaxWidth(style.maxWidth);
		}
	}

	if ('maxHeight' in style) {
		if (typeof style.maxHeight === 'string') {
			node.setMaxHeightPercent(Number.parseFloat(style.maxHeight));
		} else {
			node.setMaxHeight(style.maxHeight);
		}
	}

	if ('aspectRatio' in style) {
		node.setAspectRatio(style.aspectRatio);
	}
}
```

### 🔹 函式: `applyMarginStyles()`
- **變更前簽章 (Before)**: `applyMarginStyles(node: YogaNode, style: Styles)` (L453~L481)
- **變更後簽章 (After)**: `applyMarginStyles(node: YogaNode, style: Styles)` (L453~L481)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(node: YogaNode, style: Styles): void => {
	if ('margin' in style) {
		node.setMargin(Yoga.EDGE_ALL, style.margin ?? 0);
	}

	if ('marginX' in style) {
		node.setMargin(Yoga.EDGE_HORIZONTAL, style.marginX ?? 0);
	}

	if ('marginY' in style) {
		node.setMargin(Yoga.EDGE_VERTICAL, style.marginY ?? 0);
	}

	if ('marginLeft' in style) {
		node.setMargin(Yoga.EDGE_START, style.marginLeft ?? 0);
	}

	if ('marginRight' in style) {
		node.setMargin(Yoga.EDGE_END, style.marginRight ?? 0);
	}

	if ('marginTop' in style) {
		node.setMargin(Yoga.EDGE_TOP, style.marginTop ?? 0);
	}

	if ('marginBottom' in style) {
		node.setMargin(Yoga.EDGE_BOTTOM, style.marginBottom ?? 0);
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(node: YogaNode, style: Styles): void => {
	if ('margin' in style) {
		node.setMargin(Yoga.EDGE_ALL, style.margin ?? 0);
	}

	if ('marginX' in style) {
		node.setMargin(Yoga.EDGE_HORIZONTAL, style.marginX);
	}

	if ('marginY' in style) {
		node.setMargin(Yoga.EDGE_VERTICAL, style.marginY);
	}

	if ('marginLeft' in style) {
		node.setMargin(Yoga.EDGE_START, style.marginLeft);
	}

	if ('marginRight' in style) {
		node.setMargin(Yoga.EDGE_END, style.marginRight);
	}

	if ('marginTop' in style) {
		node.setMargin(Yoga.EDGE_TOP, style.marginTop);
	}

	if ('marginBottom' in style) {
		node.setMargin(Yoga.EDGE_BOTTOM, style.marginBottom);
	}
}
```

### 🔹 函式: `applyFlexStyles()`
- **變更前簽章 (Before)**: `applyFlexStyles(node: YogaNode, style: Styles)` (L513~L670)
- **變更後簽章 (After)**: `applyFlexStyles(node: YogaNode, style: Styles)` (L513~L670)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(node: YogaNode, style: Styles): void => {
	if ('flexGrow' in style) {
		node.setFlexGrow(style.flexGrow ?? 0);
	}

	if ('flexShrink' in style) {
		node.setFlexShrink(
			typeof style.flexShrink === 'number' ? style.flexShrink : 1,
		);
	}

	if ('flexWrap' in style) {
		if (style.flexWrap === 'nowrap') {
			node.setFlexWrap(Yoga.WRAP_NO_WRAP);
		}

		if (style.flexWrap === 'wrap') {
			node.setFlexWrap(Yoga.WRAP_WRAP);
		}

		if (style.flexWrap === 'wrap-reverse') {
			node.setFlexWrap(Yoga.WRAP_WRAP_REVERSE);
		}
	}

	if ('flexDirection' in style) {
		if (style.flexDirection === 'row') {
			node.setFlexDirection(Yoga.FLEX_DIRECTION_ROW);
		}

		if (style.flexDirection === 'row-reverse') {
			node.setFlexDirection(Yoga.FLEX_DIRECTION_ROW_REVERSE);
		}

		if (style.flexDirection === 'column') {
			node.setFlexDirection(Yoga.FLEX_DIRECTION_COLUMN);
		}

		if (style.flexDirection === 'column-reverse') {
			node.setFlexDirection(Yoga.FLEX_DIRECTION_COLUMN_REVERSE);
		}
	}

	if ('flexBasis' in style) {
		if (typeof style.flexBasis === 'number') {
			node.setFlexBasis(style.flexBasis);
		} else if (typeof style.flexBasis === 'string') {
			node.setFlexBasisPercent(Number.parseInt(style.flexBasis, 10));
		} else {
			node.setFlexBasisAuto();
		}
	}

	if ('alignItems' in style) {
		if (style.alignItems === 'stretch' || !style.alignItems) {
			node.setAlignItems(Yoga.ALIGN_STRETCH);
		}

		if (style.alignItems === 'flex-start') {
			node.setAlignItems(Yoga.ALIGN_FLEX_START);
		}

		if (style.alignItems === 'center') {
			node.setAlignItems(Yoga.ALIGN_CENTER);
		}

		if (style.alignItems === 'flex-end') {
			node.setAlignItems(Yoga.ALIGN_FLEX_END);
		}

		if (style.alignItems === 'baseline') {
			node.setAlignItems(Yoga.ALIGN_BASELINE);
		}
	}

	if ('alignSelf' in style) {
		if (style.alignSelf === 'auto' || !style.alignSelf) {
			node.setAlignSelf(Yoga.ALIGN_AUTO);
		}

		if (style.alignSelf === 'flex-start') {
			node.setAlignSelf(Yoga.ALIGN_FLEX_START);
		}

		if (style.alignSelf === 'center') {
			node.setAlignSelf(Yoga.ALIGN_CENTER);
		}

		if (style.alignSelf === 'flex-end') {
			node.setAlignSelf(Yoga.ALIGN_FLEX_END);
		}

		if (style.alignSelf === 'stretch') {
			node.setAlignSelf(Yoga.ALIGN_STRETCH);
		}

		if (style.alignSelf === 'baseline') {
			node.setAlignSelf(Yoga.ALIGN_BASELINE);
		}
	}

	if ('alignContent' in style) {
		// Keep wrapped lines top-packed by default; stretch can add surprising empty rows in fixed-height boxes.
		if (style.alignContent === 'flex-start' || !style.alignContent) {
			node.setAlignContent(Yoga.ALIGN_FLEX_START);
		}

		if (style.alignContent === 'center') {
			node.setAlignContent(Yoga.ALIGN_CENTER);
		}

		if (style.alignContent === 'flex-end') {
			node.setAlignContent(Yoga.ALIGN_FLEX_END);
		}

		if (style.alignContent === 'space-between') {
			node.setAlignContent(Yoga.ALIGN_SPACE_BETWEEN);
		}

		if (style.alignContent === 'space-around') {
			node.setAlignContent(Yoga.ALIGN_SPACE_AROUND);
		}

		if (style.alignContent === 'space-evenly') {
			node.setAlignContent(Yoga.ALIGN_SPACE_EVENLY);
		}

		if (style.alignContent === 'stretch') {
			node.setAlignContent(Yoga.ALIGN_STRETCH);
		}
	}

	if ('justifyContent' in style) {
		if (style.justifyContent === 'flex-start' || !style.justifyContent) {
			node.setJustifyContent(Yoga.JUSTIFY_FLEX_START);
		}

		if (style.justifyContent === 'center') {
			node.setJustifyContent(Yoga.JUSTIFY_CENTER);
		}

		if (style.justifyContent === 'flex-end') {
			node.setJustifyContent(Yoga.JUSTIFY_FLEX_END);
		}

		if (style.justifyContent === 'space-between') {
			node.setJustifyContent(Yoga.JUSTIFY_SPACE_BETWEEN);
		}

		if (style.justifyContent === 'space-around') {
			node.setJustifyContent(Yoga.JUSTIFY_SPACE_AROUND);
		}

		if (style.justifyContent === 'space-evenly') {
			node.setJustifyContent(Yoga.JUSTIFY_SPACE_EVENLY);
		}
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(node: YogaNode, style: Styles): void => {
	if ('flexGrow' in style) {
		node.setFlexGrow(style.flexGrow ?? 0);
	}

	if ('flexShrink' in style) {
		node.setFlexShrink(
			typeof style.flexShrink === 'number' ? style.flexShrink : 1,
		);
	}

	if ('flexWrap' in style) {
		if (style.flexWrap === 'nowrap') {
			node.setFlexWrap(Yoga.WRAP_NO_WRAP);
		}

		if (style.flexWrap === 'wrap') {
			node.setFlexWrap(Yoga.WRAP_WRAP);
		}

		if (style.flexWrap === 'wrap-reverse') {
			node.setFlexWrap(Yoga.WRAP_WRAP_REVERSE);
		}
	}

	if ('flexDirection' in style) {
		if (style.flexDirection === 'row') {
			node.setFlexDirection(Yoga.FLEX_DIRECTION_ROW);
		}

		if (style.flexDirection === 'row-reverse') {
			node.setFlexDirection(Yoga.FLEX_DIRECTION_ROW_REVERSE);
		}

		if (style.flexDirection === 'column') {
			node.setFlexDirection(Yoga.FLEX_DIRECTION_COLUMN);
		}

		if (style.flexDirection === 'column-reverse') {
			node.setFlexDirection(Yoga.FLEX_DIRECTION_COLUMN_REVERSE);
		}
	}

	if ('flexBasis' in style) {
		if (typeof style.flexBasis === 'number') {
			node.setFlexBasis(style.flexBasis);
		} else if (typeof style.flexBasis === 'string') {
			node.setFlexBasisPercent(Number.parseFloat(style.flexBasis));
		} else {
			node.setFlexBasisAuto();
		}
	}

	if ('alignItems' in style) {
		if (style.alignItems === 'stretch' || !style.alignItems) {
			node.setAlignItems(Yoga.ALIGN_STRETCH);
		}

		if (style.alignItems === 'flex-start') {
			node.setAlignItems(Yoga.ALIGN_FLEX_START);
		}

		if (style.alignItems === 'center') {
			node.setAlignItems(Yoga.ALIGN_CENTER);
		}

		if (style.alignItems === 'flex-end') {
			node.setAlignItems(Yoga.ALIGN_FLEX_END);
		}

		if (style.alignItems === 'baseline') {
			node.setAlignItems(Yoga.ALIGN_BASELINE);
		}
	}

	if ('alignSelf' in style) {
		if (style.alignSelf === 'auto' || !style.alignSelf) {
			node.setAlignSelf(Yoga.ALIGN_AUTO);
		}

		if (style.alignSelf === 'flex-start') {
			node.setAlignSelf(Yoga.ALIGN_FLEX_START);
		}

		if (style.alignSelf === 'center') {
			node.setAlignSelf(Yoga.ALIGN_CENTER);
		}

		if (style.alignSelf === 'flex-end') {
			node.setAlignSelf(Yoga.ALIGN_FLEX_END);
		}

		if (style.alignSelf === 'stretch') {
			node.setAlignSelf(Yoga.ALIGN_STRETCH);
		}

		if (style.alignSelf === 'baseline') {
			node.setAlignSelf(Yoga.ALIGN_BASELINE);
		}
	}

	if ('alignContent' in style) {
		// Keep wrapped lines top-packed by default; stretch can add surprising empty rows in fixed-height boxes.
		if (style.alignContent === 'flex-start' || !style.alignContent) {
			node.setAlignContent(Yoga.ALIGN_FLEX_START);
		}

		if (style.alignContent === 'center') {
			node.setAlignContent(Yoga.ALIGN_CENTER);
		}

		if (style.alignContent === 'flex-end') {
			node.setAlignContent(Yoga.ALIGN_FLEX_END);
		}

		if (style.alignContent === 'space-between') {
			node.setAlignContent(Yoga.ALIGN_SPACE_BETWEEN);
		}

		if (style.alignContent === 'space-around') {
			node.setAlignContent(Yoga.ALIGN_SPACE_AROUND);
		}

		if (style.alignContent === 'space-evenly') {
			node.setAlignContent(Yoga.ALIGN_SPACE_EVENLY);
		}

		if (style.alignContent === 'stretch') {
			node.setAlignContent(Yoga.ALIGN_STRETCH);
		}
	}

	if ('justifyContent' in style) {
		if (style.justifyContent === 'flex-start' || !style.justifyContent) {
			node.setJustifyContent(Yoga.JUSTIFY_FLEX_START);
		}

		if (style.justifyContent === 'center') {
			node.setJustifyContent(Yoga.JUSTIFY_CENTER);
		}

		if (style.justifyContent === 'flex-end') {
			node.setJustifyContent(Yoga.JUSTIFY_FLEX_END);
		}

		if (style.justifyContent === 'space-between') {
			node.setJustifyContent(Yoga.JUSTIFY_SPACE_BETWEEN);
		}

		if (style.justifyContent === 'space-around') {
			node.setJustifyContent(Yoga.JUSTIFY_SPACE_AROUND);
		}

		if (style.justifyContent === 'space-evenly') {
			node.setJustifyContent(Yoga.JUSTIFY_SPACE_EVENLY);
		}
	}
}
```


---

### 🔹 Commit #11: `4f3c7aa3`
- **完整 Hash**: `4f3c7aa3186ab63da2f7b2b57d7ccf92fc29c289`
- **說明 (Ground Truth)**: Fix overflow clipping
- **變更檔案數**: 3

#### 📄 檔案: `src/output.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:22, E:10, A:0) ➔ After(N:22, E:10, A:0)
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

### 🔹 函式: `get()`
- **變更前簽章 (Before)**: `get()` (L199~L380)
- **變更後簽章 (After)**: `get()` (L199~L380)

#### ◀️ 變更前實作碼 (Before Implementation):
```
get(): {output: string; height: number} {
		// Initialize output array with a specific set of rows, so that margin/padding at the bottom is preserved
		const output: StyledChar[][] = [];

		for (let y = 0; y < this.height; y++) {
			const row: StyledChar[] = [];

			for (let x = 0; x < this.width; x++) {
				row.push({
					type: 'char',
					value: ' ',
					fullWidth: false,
					styles: [],
				});
			}

			output.push(row);
		}

		const clips: Clip[] = [];

		for (const operation of this.operations) {
			if (operation.type === 'clip') {
				// Nested clips must intersect, not replace, otherwise an inner `overflow="hidden"` box lets content escape the outer clip and overwrite surrounding UI.
				clips.push(intersectClips(clips.at(-1), operation.clip));
			}

			if (operation.type === 'unclip') {
				clips.pop();
			}

			if (operation.type === 'write') {
				const {text, transformers} = operation;
				let {x, y} = operation;
				let lines = text.split('\n');

				const clip = clips.at(-1);

				if (clip) {
					// Two nested clips can intersect to nothing. Nothing is visible, so bail out before slicing.
					if (isClipEmpty(clip)) {
						continue;
					}

					const clipHorizontally =
						typeof clip?.x1 === 'number' && typeof clip?.x2 === 'number';

					const clipVertically =
						typeof clip?.y1 === 'number' && typeof clip?.y2 === 'number';

					// If text is positioned outside of clipping area altogether,
					// skip to the next operation to avoid unnecessary calculations
					if (clipHorizontally) {
						const width = this.caches.getWidestLine(text);

						if (x + width < clip.x1! || x > clip.x2!) {
							continue;
						}
					}

					if (clipVertically) {
						const height = lines.length;

						if (y + height < clip.y1! || y > clip.y2!) {
							continue;
						}
					}

					if (clipHorizontally) {
						lines = lines.map(line => {
							const from = x < clip.x1! ? clip.x1! - x : 0;
							const width = this.caches.getStringWidth(line);
							const to = x + width > clip.x2! ? clip.x2! - x : width;

							return this.sliceLineToColumns(line, from, to);
						});

						if (x < clip.x1!) {
							x = clip.x1!;
						}
					}

					if (clipVertically) {
						const from = y < clip.y1! ? clip.y1! - y : 0;
						const height = lines.length;
						const to = y + height > clip.y2! ? clip.y2! - y : height;

						lines = lines.slice(from, to);

						if (y < clip.y1!) {
							y = clip.y1!;
						}
					}
				}

				for (let [index, line] of lines.entries()) {
					const currentLine = output[y + index];

					// Lines above or below the output area have no corresponding pre-initialized row.
					if (!currentLine) {
						continue;
					}

					for (const transformer of transformers) {
						line = transformer(line, index);
					}

					const characters = this.caches.getStyledChars(line);
					let offsetX = x;

					// Nothing to write (e.g. line was clipped away).
					if (characters.length === 0) {
						continue;
					}

					const spaceCell: StyledChar = {
						type: 'char',
						value: ' ',
						fullWidth: false,
						styles: [],
					};

					// Wide characters (e.g. CJK) occupy two cells: a leading
					// cell with the character and a trailing placeholder with
					// value ''. When an overlapping write lands in the middle
					// of a wide character, the boundary cells need cleanup so
					// the terminal never renders a half-visible wide character.
					if (
						currentLine[offsetX]?.value === '' &&
						offsetX > 0 &&
						this.caches.getStringWidth(currentLine[offsetX - 1]?.value ?? '') >
							1
					) {
						currentLine[offsetX - 1] = spaceCell;
					}

					for (const character of characters) {
						currentLine[offsetX] = character;

						// Determine printed width using string-width to align with measurement
						const characterWidth = Math.max(
							1,
							this.caches.getStringWidth(character.value),
						);

						// For multi-column characters, clear following cells to avoid stray spaces/artifacts
						if (characterWidth > 1) {
							for (let index = 1; index < characterWidth; index++) {
								currentLine[offsetX + index] = {
									type: 'char',
									// Preserve visible cells when the leading cell is outside the output.
									value: offsetX < 0 ? ' ' : '',
									fullWidth: false,
									styles: character.styles,
								};
							}
						}

						offsetX += characterWidth;
					}

					if (currentLine[offsetX]?.value === '') {
						currentLine[offsetX] = spaceCell;
					}
				}
			}
		}

		const generatedOutput = output
			.map(line => {
				// See https://github.com/vadimdemedes/ink/pull/564#issuecomment-1637022742
				const lineWithoutEmptyItems = line.filter(item => item !== undefined);

				return styledCharsToString(lineWithoutEmptyItems).trimEnd();
			})
			.join('\n');

		return {
			output: generatedOutput,
			height: output.length,
		};
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
get(): {output: string; height: number} {
		// Initialize output array with a specific set of rows, so that margin/padding at the bottom is preserved
		const output: StyledChar[][] = [];

		for (let y = 0; y < this.height; y++) {
			const row: StyledChar[] = [];

			for (let x = 0; x < this.width; x++) {
				row.push({
					type: 'char',
					value: ' ',
					fullWidth: false,
					styles: [],
				});
			}

			output.push(row);
		}

		const clips: Clip[] = [];

		for (const operation of this.operations) {
			if (operation.type === 'clip') {
				// Nested clips must intersect, not replace, otherwise an inner `overflow="hidden"` box lets content escape the outer clip and overwrite surrounding UI.
				clips.push(intersectClips(clips.at(-1), operation.clip));
			}

			if (operation.type === 'unclip') {
				clips.pop();
			}

			if (operation.type === 'write') {
				const {text, transformers} = operation;
				let {x, y} = operation;
				let lines = text.split('\n');

				const clip = clips.at(-1);

				if (clip) {
					// Two nested clips can intersect to nothing. Nothing is visible, so bail out before slicing.
					if (isClipEmpty(clip)) {
						continue;
					}

					const clipHorizontally =
						typeof clip?.x1 === 'number' && typeof clip?.x2 === 'number';

					const clipVertically =
						typeof clip?.y1 === 'number' && typeof clip?.y2 === 'number';

					// If text is positioned outside of clipping area altogether,
					// skip to the next operation to avoid unnecessary calculations
					if (clipHorizontally) {
						const width = this.caches.getWidestLine(text);

						if (x + width < clip.x1! || x > clip.x2!) {
							continue;
						}
					}

					if (clipVertically) {
						const height = lines.length;

						if (y + height < clip.y1! || y > clip.y2!) {
							continue;
						}
					}

					if (clipHorizontally) {
						lines = lines.map(line => {
							const from = x < clip.x1! ? clip.x1! - x : 0;
							const width = this.caches.getStringWidth(line);
							const to = x + width > clip.x2! ? clip.x2! - x : width;

							return this.sliceLineToColumns(line, from, to);
						});

						if (x < clip.x1!) {
							x = clip.x1!;
						}
					}

					if (clipVertically) {
						const from = y < clip.y1! ? clip.y1! - y : 0;
						const height = lines.length;
						const to = y + height > clip.y2! ? clip.y2! - y : height;

						lines = lines.slice(from, to);

						if (y < clip.y1!) {
							y = clip.y1!;
						}
					}
				}

				for (let [index, line] of lines.entries()) {
					const currentLine = output[y + index];

					// Lines above or below the output area have no corresponding pre-initialized row.
					if (!currentLine) {
						continue;
					}

					for (const transformer of transformers) {
						line = transformer(line, index + y - operation.y);
					}

					const characters = this.caches.getStyledChars(line);
					let offsetX = x;

					// Nothing to write (e.g. line was clipped away).
					if (characters.length === 0) {
						continue;
					}

					const spaceCell: StyledChar = {
						type: 'char',
						value: ' ',
						fullWidth: false,
						styles: [],
					};

					// Wide characters (e.g. CJK) occupy two cells: a leading
					// cell with the character and a trailing placeholder with
					// value ''. When an overlapping write lands in the middle
					// of a wide character, the boundary cells need cleanup so
					// the terminal never renders a half-visible wide character.
					if (
						currentLine[offsetX]?.value === '' &&
						offsetX > 0 &&
						this.caches.getStringWidth(currentLine[offsetX - 1]?.value ?? '') >
							1
					) {
						currentLine[offsetX - 1] = spaceCell;
					}

					for (const character of characters) {
						currentLine[offsetX] = character;

						// Determine printed width using string-width to align with measurement
						const characterWidth = Math.max(
							1,
							this.caches.getStringWidth(character.value),
						);

						// For multi-column characters, clear following cells to avoid stray spaces/artifacts
						if (characterWidth > 1) {
							for (let index = 1; index < characterWidth; index++) {
								currentLine[offsetX + index] = {
									type: 'char',
									// Preserve visible cells when the leading cell is outside the output.
									value: offsetX < 0 ? ' ' : '',
									fullWidth: false,
									styles: character.styles,
								};
							}
						}

						offsetX += characterWidth;
					}

					if (currentLine[offsetX]?.value === '') {
						currentLine[offsetX] = spaceCell;
					}
				}
			}
		}

		const generatedOutput = output
			.map(line => {
				// See https://github.com/vadimdemedes/ink/pull/564#issuecomment-1637022742
				const lineWithoutEmptyItems = line.filter(item => item !== undefined);

				return styledCharsToString(lineWithoutEmptyItems).trimEnd();
			})
			.join('\n');

		return {
			output: generatedOutput,
			height: output.length,
		};
	}
```


#### 📄 檔案: `src/render-node-to-output.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:11, E:12, A:0) ➔ After(N:11, E:12, A:0)
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

### 🔹 函式: `renderNodeToOutput()`
- **變更前簽章 (Before)**: `renderNodeToOutput(
	node: DOMElement,
	output: Output,
	options: {
		offsetX?: number;
		offsetY?: number;
		transformers?: OutputTransformer[];
		skipStaticElements: boolean;
	},
)` (L104~L216)
- **變更後簽章 (After)**: `renderNodeToOutput(
	node: DOMElement,
	output: Output,
	options: {
		offsetX?: number;
		offsetY?: number;
		transformers?: OutputTransformer[];
		skipStaticElements: boolean;
	},
)` (L104~L216)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(
	node: DOMElement,
	output: Output,
	options: {
		offsetX?: number;
		offsetY?: number;
		transformers?: OutputTransformer[];
		skipStaticElements: boolean;
	},
) => {
	const {
		offsetX = 0,
		offsetY = 0,
		transformers = [],
		skipStaticElements,
	} = options;

	if (skipStaticElements && node.internal_static) {
		return;
	}

	const {yogaNode} = node;

	if (yogaNode) {
		if (yogaNode.getDisplay() === Yoga.DISPLAY_NONE) {
			return;
		}

		// Left and top positions in Yoga are relative to their parent node
		const x = offsetX + yogaNode.getComputedLeft();
		const y = offsetY + yogaNode.getComputedTop();

		// Transformers are functions that transform final text output of each component
		// See Output class for logic that applies transformers
		let newTransformers = transformers;

		if (typeof node.internal_transform === 'function') {
			newTransformers = [node.internal_transform, ...transformers];
		}

		if (node.nodeName === 'ink-text') {
			let text = squashTextNodes(node);

			if (text.length > 0) {
				const currentWidth = widestLine(text);
				const maxWidth = getMaxWidth(yogaNode);

				if (currentWidth > maxWidth) {
					const textWrap = node.style.textWrap ?? 'wrap';
					text = wrapText(text, maxWidth, textWrap);
				}

				text = applyPaddingToText(node, text);

				output.write(x, y, text, {transformers: newTransformers});
			}

			return;
		}

		let clipped = false;

		if (node.nodeName === 'ink-box') {
			renderBackground(x, y, node, output);
			renderBorder(x, y, node, output);

			const clipHorizontally =
				node.style.overflowX === 'hidden' || node.style.overflow === 'hidden';
			const clipVertically =
				node.style.overflowY === 'hidden' || node.style.overflow === 'hidden';

			if (clipHorizontally || clipVertically) {
				const x1 = clipHorizontally
					? x + yogaNode.getComputedBorder(Yoga.EDGE_LEFT)
					: undefined;

				const x2 = clipHorizontally
					? x +
						yogaNode.getComputedWidth() -
						yogaNode.getComputedBorder(Yoga.EDGE_RIGHT)
					: undefined;

				const y1 = clipVertically
					? y + yogaNode.getComputedBorder(Yoga.EDGE_TOP)
					: undefined;

				const y2 = clipVertically
					? y +
						yogaNode.getComputedHeight() -
						yogaNode.getComputedBorder(Yoga.EDGE_BOTTOM)
					: undefined;

				output.clip({x1, x2, y1, y2});
				clipped = true;
			}
		}

		if (node.nodeName === 'ink-root' || node.nodeName === 'ink-box') {
			for (const childNode of node.childNodes) {
				renderNodeToOutput(childNode as DOMElement, output, {
					offsetX: x - normalizeContentOffset(node.style.contentOffsetX),
					offsetY: y - normalizeContentOffset(node.style.contentOffsetY),
					transformers: newTransformers,
					skipStaticElements,
				});
			}

			if (clipped) {
				output.unclip();
			}
		}
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(
	node: DOMElement,
	output: Output,
	options: {
		offsetX?: number;
		offsetY?: number;
		transformers?: OutputTransformer[];
		skipStaticElements: boolean;
	},
) => {
	const {
		offsetX = 0,
		offsetY = 0,
		transformers = [],
		skipStaticElements,
	} = options;

	if (skipStaticElements && node.internal_static) {
		return;
	}

	const {yogaNode} = node;

	if (yogaNode) {
		if (yogaNode.getDisplay() === Yoga.DISPLAY_NONE) {
			return;
		}

		// Left and top positions in Yoga are relative to their parent node
		const x = offsetX + yogaNode.getComputedLeft();
		const y = offsetY + yogaNode.getComputedTop();

		// Transformers are functions that transform final text output of each component
		// See Output class for logic that applies transformers
		let newTransformers = transformers;

		if (typeof node.internal_transform === 'function') {
			newTransformers = [node.internal_transform, ...transformers];
		}

		if (node.nodeName === 'ink-text') {
			let text = squashTextNodes(node);

			if (text.length > 0) {
				const currentWidth = widestLine(text);
				const maxWidth = getMaxWidth(yogaNode);

				if (currentWidth > maxWidth) {
					const textWrap = node.style.textWrap ?? 'wrap';
					text = wrapText(text, maxWidth, textWrap);
				}

				text = applyPaddingToText(node, text);

				output.write(x, y, text, {transformers: newTransformers});
			}

			return;
		}

		let clipped = false;

		if (node.nodeName === 'ink-box') {
			renderBackground(x, y, node, output);
			renderBorder(x, y, node, output);

			const clipHorizontally =
				(node.style.overflowX ?? node.style.overflow) === 'hidden';
			const clipVertically =
				(node.style.overflowY ?? node.style.overflow) === 'hidden';

			if (clipHorizontally || clipVertically) {
				const x1 = clipHorizontally
					? x + yogaNode.getComputedBorder(Yoga.EDGE_LEFT)
					: undefined;

				const x2 = clipHorizontally
					? x +
						yogaNode.getComputedWidth() -
						yogaNode.getComputedBorder(Yoga.EDGE_RIGHT)
					: undefined;

				const y1 = clipVertically
					? y + yogaNode.getComputedBorder(Yoga.EDGE_TOP)
					: undefined;

				const y2 = clipVertically
					? y +
						yogaNode.getComputedHeight() -
						yogaNode.getComputedBorder(Yoga.EDGE_BOTTOM)
					: undefined;

				output.clip({x1, x2, y1, y2});
				clipped = true;
			}
		}

		if (node.nodeName === 'ink-root' || node.nodeName === 'ink-box') {
			for (const childNode of node.childNodes) {
				renderNodeToOutput(childNode as DOMElement, output, {
					offsetX: x - normalizeContentOffset(node.style.contentOffsetX),
					offsetY: y - normalizeContentOffset(node.style.contentOffsetY),
					transformers: newTransformers,
					skipStaticElements,
				});
			}

			if (clipped) {
				output.unclip();
			}
		}
	}
}
```


#### 📄 檔案: `src/squash-text-nodes.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:3, E:3, A:0) ➔ After(N:4, E:4, A:0)
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
  • + [新增節點] `transform (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `squashTextNodes` ──[CALLS]──> `transform (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `squashTextNodes()`
- **變更前簽章 (Before)**: `squashTextNodes(node: DOMElement)` (L11~L54)
- **變更後簽章 (After)**: `squashTextNodes(node: DOMElement)` (L11~L52)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(node: DOMElement): string => {
	let text = '';

	for (let index = 0; index < node.childNodes.length; index++) {
		const childNode = node.childNodes[index];

		if (childNode === undefined) {
			continue;
		}

		let nodeText = '';

		if (childNode.nodeName === '#text') {
			nodeText = childNode.nodeValue;
		} else {
			if (
				childNode.nodeName === 'ink-text' ||
				childNode.nodeName === 'ink-virtual-text'
			) {
				nodeText = squashTextNodes(childNode);
			}

			// Since these text nodes are being concatenated, `Output` instance won't be able to
			// apply children transform, so we have to do it manually here for each text node
			if (
				nodeText.length > 0 &&
				typeof childNode.internal_transform === 'function'
			) {
				nodeText = childNode.internal_transform(nodeText, index);
			}
		}

		text += nodeText;
	}

	text = sanitizeAnsi(text.replaceAll('\r\n', '\n'));

	// Expand tabs after combining nested text so measurement and rendering use the same columns.
	if (node.nodeName === 'ink-text' && text.includes('\t')) {
		text = wrapAnsi(text, Number.POSITIVE_INFINITY, {trim: false});
	}

	return text;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(node: DOMElement): string => {
	let text = '';

	for (const childNode of node.childNodes) {
		let nodeText = '';

		if (childNode.nodeName === '#text') {
			nodeText = childNode.nodeValue;
		} else {
			if (
				childNode.nodeName === 'ink-text' ||
				childNode.nodeName === 'ink-virtual-text'
			) {
				nodeText = squashTextNodes(childNode);
			}

			// Since these text nodes are being concatenated, `Output` instance won't be able to
			// apply children transform, so we have to do it manually here for each text node
			if (
				nodeText.length > 0 &&
				typeof childNode.internal_transform === 'function'
			) {
				const transform = childNode.internal_transform;
				nodeText = nodeText
					.split('\n')
					.map((line, lineIndex) => transform(line, lineIndex))
					.join('\n');
			}
		}

		text += nodeText;
	}

	text = sanitizeAnsi(text.replaceAll('\r\n', '\n'));

	// Expand tabs after combining nested text so measurement and rendering use the same columns.
	if (node.nodeName === 'ink-text' && text.includes('\t')) {
		text = wrapAnsi(text, Number.POSITIVE_INFINITY, {trim: false});
	}

	return text;
}
```


---

### 🔹 Commit #12: `32dc2663`
- **完整 Hash**: `32dc26633d33967ac225bec47297eb9e4ba652be`
- **說明 (Ground Truth)**: Fix text output edge cases
- **變更檔案數**: 2

#### 📄 檔案: `src/output.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:21, E:10, A:0) ➔ After(N:22, E:10, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `cached` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `getStyledChars()`
- **變更前簽章 (Before)**: `getStyledChars(line: string)` (L90~L98)
- **變更後簽章 (After)**: `getStyledChars(line: string)` (L90~L102)

#### ◀️ 變更前實作碼 (Before Implementation):
```
getStyledChars(line: string): StyledChar[] {
		let cached = this.styledChars.get(line);
		if (cached === undefined) {
			cached = styledCharsFromTokens(tokenize(line));
			this.styledChars.set(line, cached);
		}

		return cached;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
getStyledChars(line: string): StyledChar[] {
		let cached = this.styledChars.get(line);
		if (cached === undefined) {
			// Standalone invisible Unicode characters must not occupy terminal cells.
			cached = styledCharsFromTokens(tokenize(line)).filter(
				character =>
					!/^\p{Default_Ignorable_Code_Point}+$/u.test(character.value),
			);
			this.styledChars.set(line, cached);
		}

		return cached;
	}
```

### 🔹 函式: `get()`
- **變更前簽章 (Before)**: `get()` (L195~L383)
- **變更後簽章 (After)**: `get()` (L199~L380)

#### ◀️ 變更前實作碼 (Before Implementation):
```
get(): {output: string; height: number} {
		// Initialize output array with a specific set of rows, so that margin/padding at the bottom is preserved
		const output: StyledChar[][] = [];

		for (let y = 0; y < this.height; y++) {
			const row: StyledChar[] = [];

			for (let x = 0; x < this.width; x++) {
				row.push({
					type: 'char',
					value: ' ',
					fullWidth: false,
					styles: [],
				});
			}

			output.push(row);
		}

		const clips: Clip[] = [];

		for (const operation of this.operations) {
			if (operation.type === 'clip') {
				// Nested clips must intersect, not replace, otherwise an inner `overflow="hidden"` box lets content escape the outer clip and overwrite surrounding UI.
				clips.push(intersectClips(clips.at(-1), operation.clip));
			}

			if (operation.type === 'unclip') {
				clips.pop();
			}

			if (operation.type === 'write') {
				const {text, transformers} = operation;
				let {x, y} = operation;
				let lines = text.split('\n');

				const clip = clips.at(-1);

				if (clip) {
					// Two nested clips can intersect to nothing. Nothing is visible, so bail out before slicing.
					if (isClipEmpty(clip)) {
						continue;
					}

					const clipHorizontally =
						typeof clip?.x1 === 'number' && typeof clip?.x2 === 'number';

					const clipVertically =
						typeof clip?.y1 === 'number' && typeof clip?.y2 === 'number';

					// If text is positioned outside of clipping area altogether,
					// skip to the next operation to avoid unnecessary calculations
					if (clipHorizontally) {
						const width = this.caches.getWidestLine(text);

						if (x + width < clip.x1! || x > clip.x2!) {
							continue;
						}
					}

					if (clipVertically) {
						const height = lines.length;

						if (y + height < clip.y1! || y > clip.y2!) {
							continue;
						}
					}

					if (clipHorizontally) {
						lines = lines.map(line => {
							const from = x < clip.x1! ? clip.x1! - x : 0;
							const width = this.caches.getStringWidth(line);
							const to = x + width > clip.x2! ? clip.x2! - x : width;

							return this.sliceLineToColumns(line, from, to);
						});

						if (x < clip.x1!) {
							x = clip.x1!;
						}
					}

					if (clipVertically) {
						const from = y < clip.y1! ? clip.y1! - y : 0;
						const height = lines.length;
						const to = y + height > clip.y2! ? clip.y2! - y : height;

						lines = lines.slice(from, to);

						if (y < clip.y1!) {
							y = clip.y1!;
						}
					}
				}

				let offsetY = 0;

				for (let [index, line] of lines.entries()) {
					const currentLine = output[y + offsetY];

					// Line can be missing if `text` starts above the top of
					// `this.output` or is taller than its height. Advance `offsetY`
					// anyway, so the lines that do land inside still get written.
					if (!currentLine) {
						offsetY++;
						continue;
					}

					for (const transformer of transformers) {
						line = transformer(line, index);
					}

					const characters = this.caches.getStyledChars(line);
					let offsetX = x;

					// Nothing to write (e.g. line was clipped away).
					if (characters.length === 0) {
						offsetY++;
						continue;
					}

					const spaceCell: StyledChar = {
						type: 'char',
						value: ' ',
						fullWidth: false,
						styles: [],
					};

					// Wide characters (e.g. CJK) occupy two cells: a leading
					// cell with the character and a trailing placeholder with
					// value ''. When an overlapping write lands in the middle
					// of a wide character, the boundary cells need cleanup so
					// the terminal never renders a half-visible wide character.
					if (
						currentLine[offsetX]?.value === '' &&
						offsetX > 0 &&
						this.caches.getStringWidth(currentLine[offsetX - 1]?.value ?? '') >
							1
					) {
						currentLine[offsetX - 1] = spaceCell;
					}

					for (const character of characters) {
						currentLine[offsetX] = character;

						// Determine printed width using string-width to align with measurement
						const characterWidth = Math.max(
							1,
							this.caches.getStringWidth(character.value),
						);

						// For multi-column characters, clear following cells to avoid stray spaces/artifacts
						if (characterWidth > 1) {
							for (let index = 1; index < characterWidth; index++) {
								currentLine[offsetX + index] = {
									type: 'char',
									value: '',
									fullWidth: false,
									styles: character.styles,
								};
							}
						}

						offsetX += characterWidth;
					}

					if (currentLine[offsetX]?.value === '') {
						currentLine[offsetX] = spaceCell;
					}

					offsetY++;
				}
			}
		}

		const generatedOutput = output
			.map(line => {
				// See https://github.com/vadimdemedes/ink/pull/564#issuecomment-1637022742
				const lineWithoutEmptyItems = line.filter(item => item !== undefined);

				return styledCharsToString(lineWithoutEmptyItems).trimEnd();
			})
			.join('\n');

		return {
			output: generatedOutput,
			height: output.length,
		};
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
get(): {output: string; height: number} {
		// Initialize output array with a specific set of rows, so that margin/padding at the bottom is preserved
		const output: StyledChar[][] = [];

		for (let y = 0; y < this.height; y++) {
			const row: StyledChar[] = [];

			for (let x = 0; x < this.width; x++) {
				row.push({
					type: 'char',
					value: ' ',
					fullWidth: false,
					styles: [],
				});
			}

			output.push(row);
		}

		const clips: Clip[] = [];

		for (const operation of this.operations) {
			if (operation.type === 'clip') {
				// Nested clips must intersect, not replace, otherwise an inner `overflow="hidden"` box lets content escape the outer clip and overwrite surrounding UI.
				clips.push(intersectClips(clips.at(-1), operation.clip));
			}

			if (operation.type === 'unclip') {
				clips.pop();
			}

			if (operation.type === 'write') {
				const {text, transformers} = operation;
				let {x, y} = operation;
				let lines = text.split('\n');

				const clip = clips.at(-1);

				if (clip) {
					// Two nested clips can intersect to nothing. Nothing is visible, so bail out before slicing.
					if (isClipEmpty(clip)) {
						continue;
					}

					const clipHorizontally =
						typeof clip?.x1 === 'number' && typeof clip?.x2 === 'number';

					const clipVertically =
						typeof clip?.y1 === 'number' && typeof clip?.y2 === 'number';

					// If text is positioned outside of clipping area altogether,
					// skip to the next operation to avoid unnecessary calculations
					if (clipHorizontally) {
						const width = this.caches.getWidestLine(text);

						if (x + width < clip.x1! || x > clip.x2!) {
							continue;
						}
					}

					if (clipVertically) {
						const height = lines.length;

						if (y + height < clip.y1! || y > clip.y2!) {
							continue;
						}
					}

					if (clipHorizontally) {
						lines = lines.map(line => {
							const from = x < clip.x1! ? clip.x1! - x : 0;
							const width = this.caches.getStringWidth(line);
							const to = x + width > clip.x2! ? clip.x2! - x : width;

							return this.sliceLineToColumns(line, from, to);
						});

						if (x < clip.x1!) {
							x = clip.x1!;
						}
					}

					if (clipVertically) {
						const from = y < clip.y1! ? clip.y1! - y : 0;
						const height = lines.length;
						const to = y + height > clip.y2! ? clip.y2! - y : height;

						lines = lines.slice(from, to);

						if (y < clip.y1!) {
							y = clip.y1!;
						}
					}
				}

				for (let [index, line] of lines.entries()) {
					const currentLine = output[y + index];

					// Lines above or below the output area have no corresponding pre-initialized row.
					if (!currentLine) {
						continue;
					}

					for (const transformer of transformers) {
						line = transformer(line, index);
					}

					const characters = this.caches.getStyledChars(line);
					let offsetX = x;

					// Nothing to write (e.g. line was clipped away).
					if (characters.length === 0) {
						continue;
					}

					const spaceCell: StyledChar = {
						type: 'char',
						value: ' ',
						fullWidth: false,
						styles: [],
					};

					// Wide characters (e.g. CJK) occupy two cells: a leading
					// cell with the character and a trailing placeholder with
					// value ''. When an overlapping write lands in the middle
					// of a wide character, the boundary cells need cleanup so
					// the terminal never renders a half-visible wide character.
					if (
						currentLine[offsetX]?.value === '' &&
						offsetX > 0 &&
						this.caches.getStringWidth(currentLine[offsetX - 1]?.value ?? '') >
							1
					) {
						currentLine[offsetX - 1] = spaceCell;
					}

					for (const character of characters) {
						currentLine[offsetX] = character;

						// Determine printed width using string-width to align with measurement
						const characterWidth = Math.max(
							1,
							this.caches.getStringWidth(character.value),
						);

						// For multi-column characters, clear following cells to avoid stray spaces/artifacts
						if (characterWidth > 1) {
							for (let index = 1; index < characterWidth; index++) {
								currentLine[offsetX + index] = {
									type: 'char',
									// Preserve visible cells when the leading cell is outside the output.
									value: offsetX < 0 ? ' ' : '',
									fullWidth: false,
									styles: character.styles,
								};
							}
						}

						offsetX += characterWidth;
					}

					if (currentLine[offsetX]?.value === '') {
						currentLine[offsetX] = spaceCell;
					}
				}
			}
		}

		const generatedOutput = output
			.map(line => {
				// See https://github.com/vadimdemedes/ink/pull/564#issuecomment-1637022742
				const lineWithoutEmptyItems = line.filter(item => item !== undefined);

				return styledCharsToString(lineWithoutEmptyItems).trimEnd();
			})
			.join('\n');

		return {
			output: generatedOutput,
			height: output.length,
		};
	}
```


#### 📄 檔案: `src/squash-text-nodes.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:2, E:2, A:0) ➔ After(N:3, E:3, A:0)
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
  • + [新增節點] `wrapAnsi (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `squashTextNodes` ──[CALLS [guard: (node.nodeName === 'ink-text' && text.includes('\t'))]]──> `wrapAnsi (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `squashTextNodes()`
- **變更前簽章 (Before)**: `squashTextNodes(node: DOMElement)` (L10~L46)
- **變更後簽章 (After)**: `squashTextNodes(node: DOMElement)` (L11~L54)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(node: DOMElement): string => {
	let text = '';

	for (let index = 0; index < node.childNodes.length; index++) {
		const childNode = node.childNodes[index];

		if (childNode === undefined) {
			continue;
		}

		let nodeText = '';

		if (childNode.nodeName === '#text') {
			nodeText = childNode.nodeValue;
		} else {
			if (
				childNode.nodeName === 'ink-text' ||
				childNode.nodeName === 'ink-virtual-text'
			) {
				nodeText = squashTextNodes(childNode);
			}

			// Since these text nodes are being concatenated, `Output` instance won't be able to
			// apply children transform, so we have to do it manually here for each text node
			if (
				nodeText.length > 0 &&
				typeof childNode.internal_transform === 'function'
			) {
				nodeText = childNode.internal_transform(nodeText, index);
			}
		}

		text += nodeText;
	}

	return sanitizeAnsi(text);
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(node: DOMElement): string => {
	let text = '';

	for (let index = 0; index < node.childNodes.length; index++) {
		const childNode = node.childNodes[index];

		if (childNode === undefined) {
			continue;
		}

		let nodeText = '';

		if (childNode.nodeName === '#text') {
			nodeText = childNode.nodeValue;
		} else {
			if (
				childNode.nodeName === 'ink-text' ||
				childNode.nodeName === 'ink-virtual-text'
			) {
				nodeText = squashTextNodes(childNode);
			}

			// Since these text nodes are being concatenated, `Output` instance won't be able to
			// apply children transform, so we have to do it manually here for each text node
			if (
				nodeText.length > 0 &&
				typeof childNode.internal_transform === 'function'
			) {
				nodeText = childNode.internal_transform(nodeText, index);
			}
		}

		text += nodeText;
	}

	text = sanitizeAnsi(text.replaceAll('\r\n', '\n'));

	// Expand tabs after combining nested text so measurement and rendering use the same columns.
	if (node.nodeName === 'ink-text' && text.includes('\t')) {
		text = wrapAnsi(text, Number.POSITIVE_INFINITY, {trim: false});
	}

	return text;
}
```


---

### 🔹 Commit #13: `d1305882`
- **完整 Hash**: `d1305882332e686cea619411b00ee8edb891772e`
- **說明 (Ground Truth)**: Fix focus management
- **變更檔案數**: 2

#### 📄 檔案: `src/components/App.tsx`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:60, E:56, A:0) ➔ After(N:59, E:55, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 1, -Edges: 2, ΔFuncs: 8, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `setIsFocusEnabled (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `disableFocus` ──[CALLS]──> `setActiveFocusId (External/Unresolved)`
  • - [移除呼叫邊] `enableFocus` ──[CALLS]──> `setIsFocusEnabled (External/Unresolved)`
  • - [移除呼叫邊] `disableFocus` ──[CALLS]──> `setIsFocusEnabled (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `focus()`
- **變更前簽章 (Before)**: `focus(id: string)` (L586~L598)
- **變更後簽章 (After)**: `focus(id: string)` (L587~L599)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(id: string): void => {
		setFocusables(currentFocusables => {
			const hasFocusableId = currentFocusables.some(
				focusable => focusable?.id === id,
			);

			if (hasFocusableId) {
				setActiveFocusId(id);
			}

			return currentFocusables;
		});
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(id: string): void => {
		setFocusables(currentFocusables => {
			const hasFocusableId = currentFocusables.some(
				focusable => focusable.id === id && focusable.isActive,
			);

			if (hasFocusableId) {
				setActiveFocusId(id);
			}

			return currentFocusables;
		});
	}
```

### 🔹 函式: `handleInput()`
- **變更前簽章 (Before)**: `handleInput(input: string)` (L254~L266)
- **變更後簽章 (After)**: `handleInput(input: string)` (L254~L266)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(input: string): void => {
			// Exit on Ctrl+C
			// eslint-disable-next-line unicorn/no-hex-escape
			if (input === '\x03' && exitOnCtrlC) {
				handleExit();
				return;
			}

			// Reset focus when there's an active focused component on Esc
			if (input === escape && isFocusEnabled) {
				setActiveFocusId(undefined);
			}
		}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(input: string): void => {
			// Exit on Ctrl+C
			// eslint-disable-next-line unicorn/no-hex-escape
			if (input === '\x03' && exitOnCtrlC) {
				handleExit();
				return;
			}

			// Reset focus when there's an active focused component on Esc
			if (input === escape && isFocusEnabledRef.current) {
				setActiveFocusId(undefined);
			}
		}
```

### 🔹 函式: `addFocusable()`
- **變更前簽章 (Before)**: `addFocusable(id: string, {autoFocus}: {autoFocus: boolean})` (L601~L623)
- **變更後簽章 (After)**: `addFocusable(id: string, {autoFocus}: {autoFocus: boolean})` (L602~L624)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(id: string, {autoFocus}: {autoFocus: boolean}): void => {
			setFocusables(currentFocusables => {
				focusablesCountRef.current = currentFocusables.length + 1;

				return [
					...currentFocusables,
					{
						id,
						isActive: true,
					},
				];
			});

			if (autoFocus) {
				setActiveFocusId(currentActiveFocusId => {
					if (!currentActiveFocusId) {
						return id;
					}

					return currentActiveFocusId;
				});
			}
		}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(id: string, {autoFocus}: {autoFocus: boolean}): void => {
			setFocusables(currentFocusables => {
				focusablesCountRef.current = currentFocusables.length + 1;

				return [
					...currentFocusables,
					{
						id,
						isActive: true,
					},
				];
			});

			if (autoFocus && isFocusEnabledRef.current) {
				setActiveFocusId(currentActiveFocusId => {
					if (!currentActiveFocusId) {
						return id;
					}

					return currentActiveFocusId;
				});
			}
		}
```

### 🔹 函式: `handleTabNavigation()`
- **變更前簽章 (Before)**: `handleTabNavigation(input: string)` (L558~L568)
- **變更後簽章 (After)**: `handleTabNavigation(input: string)` (L558~L568)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(input: string): void => {
			if (!isFocusEnabled || focusablesCountRef.current === 0) return;

			if (input === tab) {
				focusNext();
			}

			if (input === shiftTab) {
				focusPrevious();
			}
		}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(input: string): void => {
			if (!isFocusEnabledRef.current || focusablesCountRef.current === 0) return;

			if (input === tab) {
				focusNext();
			}

			if (input === shiftTab) {
				focusPrevious();
			}
		}
```

### 🔹 函式: `enableFocus()`
- **變更前簽章 (Before)**: `enableFocus()` (L578~L580)
- **變更後簽章 (After)**: `enableFocus()` (L578~L580)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(): void => {
		setIsFocusEnabled(true);
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(): void => {
		isFocusEnabledRef.current = true;
	}
```

### 🔹 函式: `hasFocusableId()`
- **變更前簽章 (Before)**: `hasFocusableId()` (L589~L589)
- **變更後簽章 (After)**: `hasFocusableId()` (L590~L590)

#### ◀️ 變更前實作碼 (Before Implementation):
```
focusable => focusable?.id === id
```

#### ▶️ 變更後實作碼 (After Implementation):
```
focusable => focusable.id === id && focusable.isActive
```

### 🔹 函式: `disableFocus()`
- **變更前簽章 (Before)**: `disableFocus()` (L582~L584)
- **變更後簽章 (After)**: `disableFocus()` (L582~L585)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(): void => {
		setIsFocusEnabled(false);
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(): void => {
		isFocusEnabledRef.current = false;
		setActiveFocusId(undefined);
	}
```

### 🔹 函式: `App()`
- **變更前簽章 (Before)**: `function App(` (L64~L815)
- **變更後簽章 (After)**: `function App(` (L64~L816)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function App({
	children,
	stdin,
	stdout,
	stderr,
	writeToStdout,
	writeToStderr,
	exitOnCtrlC,
	onExit,
	onWaitUntilRenderFlush,
	onSuspendTerminal,
	onRegisterInputControl,
	setCursorPosition,
	interactive,
	renderThrottleMs,
}: Props): React.ReactNode {
	const [isFocusEnabled, setIsFocusEnabled] = useState(true);
	const [activeFocusId, setActiveFocusId] = useState<string | undefined>(
		undefined,
	);
	// Focusables array is managed internally via setFocusables callback pattern
	// eslint-disable-next-line react/hook-use-state
	const [, setFocusables] = useState<Focusable[]>([]);
	// Track focusables count for tab navigation check (avoids stale closure)
	const focusablesCountRef = useRef(0);
	const animationSubscribersRef = useRef(
		new Map<(currentTime: number) => void, AnimationSubscriber>(),
	);
	const animationTimerRef = useRef<ReturnType<typeof setTimeout> | undefined>(
		undefined,
	);
	// Count how many components enabled raw mode to avoid disabling
	// raw mode until all components don't need it anymore
	const rawModeEnabledCount = useRef(0);
	const pendingDisableRawModeRef = useRef(false);
	// Count how many components enabled bracketed paste mode
	const bracketedPasteModeEnabledCount = useRef(0);
	// eslint-disable-next-line @typescript-eslint/naming-convention
	const internal_eventEmitter = useRef(new EventEmitter());
	// Each useInput hook adds a listener, so the count can legitimately exceed the default limit of 10.
	internal_eventEmitter.current.setMaxListeners(Infinity);
	// Store the currently attached readable listener to avoid stale closure issues
	const readableListenerRef = useRef<(() => void) | undefined>(undefined);
	const inputParserRef = useRef(createInputParser());
	const pendingInputFlushRef = useRef<NodeJS.Timeout | undefined>(undefined);
	// Small delay to let chunked escape sequences complete before flushing as literal input.
	const pendingInputFlushDelayMilliseconds = 20;

	const clearPendingInputFlush = useCallback((): void => {
		if (!pendingInputFlushRef.current) {
			return;
		}

		clearTimeout(pendingInputFlushRef.current);
		pendingInputFlushRef.current = undefined;
	}, []);

	const clearAnimationTimer = useCallback((): void => {
		if (!animationTimerRef.current) {
			return;
		}

		clearTimeout(animationTimerRef.current);
		animationTimerRef.current = undefined;
	}, []);

	const scheduleAnimationTick = useCallback((): void => {
		clearAnimationTimer();

		if (animationSubscribersRef.current.size === 0) {
			return;
		}

		let nextDueTime = Number.POSITIVE_INFINITY;

		for (const subscriber of animationSubscribersRef.current.values()) {
			// One shared timer is enough as long as it wakes at the earliest
			// subscriber deadline and lets slower animations skip that tick.
			nextDueTime = Math.min(nextDueTime, subscriber.nextDueTime);
		}

		const delay = Math.max(0, nextDueTime - performance.now());
		animationTimerRef.current = setTimeout(() => {
			animationTimerRef.current = undefined;
			const currentTime = performance.now();

			for (const subscriber of animationSubscribersRef.current.values()) {
				if (currentTime < subscriber.nextDueTime) {
					continue;
				}

				subscriber.callback(currentTime);
				const elapsedTime = currentTime - subscriber.startTime;
				const elapsedFrames = Math.floor(elapsedTime / subscriber.interval) + 1;
				// Advance from elapsed time rather than callback count so delayed
				// ticks catch up instead of stretching the animation timeline.
				subscriber.nextDueTime =
					subscriber.startTime + elapsedFrames * subscriber.interval;
			}

			scheduleAnimationTick();
		}, delay);
		// Keep the timer ref'd while animations are active so `useAnimation()`
		// can drive process lifetime in both interactive and non-interactive apps.
	}, [clearAnimationTimer]);

	const animationSubscribe = useCallback(
		(
			callback: (currentTime: number) => void,
			interval: number,
		): {readonly startTime: number; readonly unsubscribe: () => void} => {
			const startTime = performance.now();
			// The scheduler owns the start timestamp so hooks can derive frames from
			// the exact same origin that determines each subscriber's due time.
			animationSubscribersRef.current.set(callback, {
				callback,
				interval,
				startTime,
				nextDueTime: startTime + interval,
			});
			scheduleAnimationTick();

			return {
				startTime,
				unsubscribe() {
					animationSubscribersRef.current.delete(callback);

					if (animationSubscribersRef.current.size === 0) {
						clearAnimationTimer();
						return;
					}

					scheduleAnimationTick();
				},
			};
		},
		[clearAnimationTimer, scheduleAnimationTick],
	);

	useEffect(() => {
		return () => {
			clearAnimationTimer();
		};
	}, [clearAnimationTimer]);

	const rawModeStdin = getRawModeStream(stdin);
	const isRawModeSupported = rawModeStdin !== undefined;

	const detachReadableListener = useCallback((): void => {
		if (!readableListenerRef.current) {
			return;
		}

		stdin.removeListener('readable', readableListenerRef.current);
		readableListenerRef.current = undefined;
	}, [stdin]);

	const clearInputState = useCallback((): void => {
		inputParserRef.current.reset();
		clearPendingInputFlush();
		detachReadableListener();
	}, [clearPendingInputFlush, detachReadableListener]);

	const disableRawMode = useCallback((): void => {
		if (!rawModeStdin) {
			return;
		}

		pendingDisableRawModeRef.current = false;
		rawModeStdin.setRawMode(false);
		rawModeStdin.unref?.();
		rawModeEnabledCount.current = 0;
		clearInputState();
	}, [rawModeStdin, clearInputState]);

	const handleExit = useCallback(
		(errorOrResult?: unknown): void => {
			if (
				isRawModeSupported &&
				(rawModeEnabledCount.current > 0 || pendingDisableRawModeRef.current)
			) {
				disableRawMode();
			}

			onExit(errorOrResult);
		},
		[isRawModeSupported, disableRawMode, onExit],
	);

	const handleInput = useCallback(
		(input: string): void => {
			// Exit on Ctrl+C
			// eslint-disable-next-line unicorn/no-hex-escape
			if (input === '\x03' && exitOnCtrlC) {
				handleExit();
				return;
			}

			// Reset focus when there's an active focused component on Esc
			if (input === escape && isFocusEnabled) {
				setActiveFocusId(undefined);
			}
		},
		[exitOnCtrlC, handleExit, isFocusEnabled],
	);

	const emitInput = useCallback(
		(input: string): void => {
			handleInput(input);
			internal_eventEmitter.current.emit('input', input);
		},
		[handleInput],
	);

	const schedulePendingInputFlush = useCallback((): void => {
		clearPendingInputFlush();
		pendingInputFlushRef.current = setTimeout(() => {
			pendingInputFlushRef.current = undefined;
			const pendingEscape = inputParserRef.current.flushPendingEscape();
			if (!pendingEscape) {
				return;
			}

			emitInput(pendingEscape);
		}, pendingInputFlushDelayMilliseconds);
	}, [clearPendingInputFlush, emitInput]);

	const handleReadable = useCallback((): void => {
		clearPendingInputFlush();
		let chunk;
		// eslint-disable-next-line @typescript-eslint/no-restricted-types
		while ((chunk = stdin.read() as string | null) !== null) {
			const inputEvents = inputParserRef.current.push(chunk);
			for (const event of inputEvents) {
				if (typeof event === 'string') {
					emitInput(event);
				} else {
					// Keep paste on a separate channel from `useInput` so key handlers
					// don't need to branch on mixed key-vs-paste event shapes.
					if (internal_eventEmitter.current.listenerCount('paste') === 0) {
						emitInput(event.paste);
						continue;
					}

					internal_eventEmitter.current.emit('paste', event.paste);
				}
			}
		}

		if (inputParserRef.current.hasPendingEscape()) {
			schedulePendingInputFlush();
		}
	}, [stdin, emitInput, clearPendingInputFlush, schedulePendingInputFlush]);

	const attachReadableListener = useCallback((): void => {
		if (readableListenerRef.current) {
			return;
		}

		// Store the listener reference to avoid stale closure when removing
		readableListenerRef.current = handleReadable;
		stdin.addListener('readable', handleReadable);
	}, [stdin, handleReadable]);

	const handleSetRawMode = useCallback(
		(isEnabled: boolean): void => {
			if (!rawModeStdin) {
				if (stdin === process.stdin) {
					throw new Error(
						'Raw mode is not supported on the current process.stdin, which Ink uses as input stream by default.\nRead about how to prevent this error on https://github.com/vadimdemedes/ink/#israwmodesupported',
					);
				} else {
					throw new Error(
						'Raw mode is not supported on the stdin provided to Ink.\nRead about how to prevent this error on https://github.com/vadimdemedes/ink/#israwmodesupported',
					);
				}
			}

			rawModeStdin.setEncoding('utf8');

			if (isEnabled) {
				if (rawModeEnabledCount.current === 0) {
					// A same-render component swap may have detached input handling while
					// leaving terminal raw mode enabled until the queued disable runs.
					const isRawModeAlreadyEnabled = pendingDisableRawModeRef.current;
					pendingDisableRawModeRef.current = false;

					if (!isRawModeAlreadyEnabled) {
						rawModeStdin.ref?.();
						rawModeStdin.setRawMode(true);
					}

					attachReadableListener();
				}

				rawModeEnabledCount.current++;
				return;
			}

			if (rawModeEnabledCount.current === 0) {
				return;
			}

			if (--rawModeEnabledCount.current === 0) {
				// Stop owning input immediately so pending parser state cannot leak into
				// a replacement `useInput` component mounted in the same React update.
				clearInputState();

				// Defer only the terminal raw-mode teardown so a same-render replacement
				// can keep the process ref and raw mode active without a disable/enable cycle.
				pendingDisableRawModeRef.current = true;
				queueMicrotask(() => {
					if (!pendingDisableRawModeRef.current) {
						return;
					}

					disableRawMode();
				});
			}
		},
		[
			rawModeStdin,
			stdin,
			attachReadableListener,
			clearInputState,
			disableRawMode,
		],
	);

	const handleSetBracketedPasteMode = useCallback(
		(isEnabled: boolean): void => {
			if (!stdout.isTTY) {
				return;
			}

			if (isEnabled) {
				if (bracketedPasteModeEnabledCount.current === 0) {
					stdout.write('\u001B[?2004h');
				}

				bracketedPasteModeEnabledCount.current++;
				return;
			}

			if (bracketedPasteModeEnabledCount.current === 0) {
				return;
			}

			if (--bracketedPasteModeEnabledCount.current === 0) {
				stdout.write('\u001B[?2004l');
			}
		},
		[stdout],
	);

	// Remembers which input modes were active so resumeInput can reinstate exactly
	// those after a terminal suspension, without touching the ref counts (the React
	// components still "own" raw mode/bracketed paste across the suspension).
	const suspendedInputStateRef = useRef({
		rawMode: false,
		bracketedPaste: false,
	});

	const pauseInput = useCallback((): void => {
		const wasRawMode = isRawModeSupported && rawModeEnabledCount.current > 0;
		const wasBracketedPaste = bracketedPasteModeEnabledCount.current > 0;
		suspendedInputStateRef.current = {
			rawMode: wasRawMode,
			bracketedPaste: wasBracketedPaste,
		};

		if (wasBracketedPaste && stdout.isTTY) {
			try {
				stdout.write('\u001B[?2004l');
			} catch {}
		}

		if (wasRawMode) {
			rawModeStdin?.setRawMode(false);
			rawModeStdin?.unref?.();
			clearInputState();
		}
	}, [isRawModeSupported, rawModeStdin, stdout, clearInputState]);

	const resumeInput = useCallback((): void => {
		const {rawMode, bracketedPaste} = suspendedInputStateRef.current;

		if (rawMode) {
			rawModeStdin?.setEncoding('utf8');
			rawModeStdin?.ref?.();
			rawModeStdin?.setRawMode(true);
			attachReadableListener();
		}

		if (bracketedPaste && stdout.isTTY) {
			try {
				stdout.write('\u001B[?2004h');
			} catch {}
		}
	}, [rawModeStdin, stdout, attachReadableListener]);

	// Register input pause/resume in an insertion effect: it runs before every
	// passive effect (parent and child), so a child that calls suspendTerminal()
	// from its own effect always finds the input control already registered. A
	// normal effect would run too late (child effects fire before the parent's).
	useInsertionEffect(() => {
		onRegisterInputControl(pauseInput, resumeInput);
	}, [onRegisterInputControl, pauseInput, resumeInput]);

	// Focus navigation helpers
	const findNextFocusable = useCallback(
		(
			currentFocusables: Focusable[],
			currentActiveFocusId: string | undefined,
		): string | undefined => {
			const activeIndex = currentFocusables.findIndex(focusable => {
				return focusable.id === currentActiveFocusId;
			});

			for (
				let index = activeIndex + 1;
				index < currentFocusables.length;
				index++
			) {
				const focusable = currentFocusables[index];

				if (focusable?.isActive) {
					return focusable.id;
				}
			}

			return undefined;
		},
		[],
	);

	const findPreviousFocusable = useCallback(
		(
			currentFocusables: Focusable[],
			currentActiveFocusId: string | undefined,
		): string | undefined => {
			const activeIndex = currentFocusables.findIndex(focusable => {
				return focusable.id === currentActiveFocusId;
			});

			for (let index = activeIndex - 1; index >= 0; index--) {
				const focusable = currentFocusables[index];

				if (focusable?.isActive) {
					return focusable.id;
				}
			}

			return undefined;
		},
		[],
	);

	const focusNext = useCallback((): void => {
		setFocusables(currentFocusables => {
			setActiveFocusId(currentActiveFocusId => {
				const firstFocusableId = currentFocusables.find(
					focusable => focusable.isActive,
				)?.id;
				const nextFocusableId = findNextFocusable(
					currentFocusables,
					currentActiveFocusId,
				);

				return nextFocusableId ?? firstFocusableId;
			});
			return currentFocusables;
		});
	}, [findNextFocusable]);

	const focusPrevious = useCallback((): void => {
		setFocusables(currentFocusables => {
			setActiveFocusId(currentActiveFocusId => {
				const lastFocusableId = currentFocusables.findLast(
					focusable => focusable.isActive,
				)?.id;
				const previousFocusableId = findPreviousFocusable(
					currentFocusables,
					currentActiveFocusId,
				);

				return previousFocusableId ?? lastFocusableId;
			});
			return currentFocusables;
		});
	}, [findPreviousFocusable]);

	// Handle tab navigation via effect that subscribes to input events
	useEffect(() => {
		const handleTabNavigation = (input: string): void => {
			if (!isFocusEnabled || focusablesCountRef.current === 0) return;

			if (input === tab) {
				focusNext();
			}

			if (input === shiftTab) {
				focusPrevious();
			}
		};

		internal_eventEmitter.current.on('input', handleTabNavigation);
		const emitter = internal_eventEmitter.current;

		return () => {
			emitter.off('input', handleTabNavigation);
		};
	}, [isFocusEnabled, focusNext, focusPrevious]);

	const enableFocus = useCallback((): void => {
		setIsFocusEnabled(true);
	}, []);

	const disableFocus = useCallback((): void => {
		setIsFocusEnabled(false);
	}, []);

	const focus = useCallback((id: string): void => {
		setFocusables(currentFocusables => {
			const hasFocusableId = currentFocusables.some(
				focusable => focusable?.id === id,
			);

			if (hasFocusableId) {
				setActiveFocusId(id);
			}

			return currentFocusables;
		});
	}, []);

	const addFocusable = useCallback(
		(id: string, {autoFocus}: {autoFocus: boolean}): void => {
			setFocusables(currentFocusables => {
				focusablesCountRef.current = currentFocusables.length + 1;

				return [
					...currentFocusables,
					{
						id,
						isActive: true,
					},
				];
			});

			if (autoFocus) {
				setActiveFocusId(currentActiveFocusId => {
					if (!currentActiveFocusId) {
						return id;
					}

					return currentActiveFocusId;
				});
			}
		},
		[],
	);

	const removeFocusable = useCallback((id: string): void => {
		setActiveFocusId(currentActiveFocusId => {
			if (currentActiveFocusId === id) {
				return undefined;
			}

			return currentActiveFocusId;
		});

		setFocusables(currentFocusables => {
			const filtered = currentFocusables.filter(focusable => {
				return focusable.id !== id;
			});
			focusablesCountRef.current = filtered.length;

			return filtered;
		});
	}, []);

	const activateFocusable = useCallback((id: string): void => {
		setFocusables(currentFocusables =>
			currentFocusables.map(focusable => {
				if (focusable.id !== id) {
					return focusable;
				}

				return {
					id,
					isActive: true,
				};
			}),
		);
	}, []);

	const deactivateFocusable = useCallback((id: string): void => {
		setActiveFocusId(currentActiveFocusId => {
			if (currentActiveFocusId === id) {
				return undefined;
			}

			return currentActiveFocusId;
		});

		setFocusables(currentFocusables =>
			currentFocusables.map(focusable => {
				if (focusable.id !== id) {
					return focusable;
				}

				return {
					id,
					isActive: false,
				};
			}),
		);
	}, []);

	// Handle cursor visibility, raw mode, and bracketed paste mode cleanup on unmount
	useEffect(() => {
		return () => {
			const canWriteToStdout = !stdout.destroyed && !stdout.writableEnded;

			if (interactive && canWriteToStdout) {
				cliCursor.show(stdout);
			}

			if (
				isRawModeSupported &&
				(rawModeEnabledCount.current > 0 || pendingDisableRawModeRef.current)
			) {
				disableRawMode();
			}

			if (bracketedPasteModeEnabledCount.current > 0) {
				if (stdout.isTTY && canWriteToStdout) {
					stdout.write('\u001B[?2004l');
				}

				bracketedPasteModeEnabledCount.current = 0;
			}
		};
	}, [stdout, isRawModeSupported, disableRawMode, interactive]);

	// Memoize context values to prevent unnecessary re-renders
	const appContextValue = useMemo(
		() => ({
			exit: handleExit,
			waitUntilRenderFlush: onWaitUntilRenderFlush,
			suspendTerminal: onSuspendTerminal,
		}),
		[handleExit, onWaitUntilRenderFlush, onSuspendTerminal],
	);

	const stdinContextValue = useMemo(
		() => ({
			stdin,
			setRawMode: handleSetRawMode,
			setBracketedPasteMode: handleSetBracketedPasteMode,
			isRawModeSupported,
			// eslint-disable-next-line @typescript-eslint/naming-convention
			internal_exitOnCtrlC: exitOnCtrlC,
			// eslint-disable-next-line @typescript-eslint/naming-convention
			internal_eventEmitter: internal_eventEmitter.current,
		}),
		[
			stdin,
			handleSetRawMode,
			handleSetBracketedPasteMode,
			isRawModeSupported,
			exitOnCtrlC,
		],
	);

	const stdoutContextValue = useMemo(
		() => ({
			stdout,
			write: writeToStdout,
		}),
		[stdout, writeToStdout],
	);

	const stderrContextValue = useMemo(
		() => ({
			stderr,
			write: writeToStderr,
		}),
		[stderr, writeToStderr],
	);

	const cursorContextValue = useMemo(
		() => ({
			setCursorPosition,
		}),
		[setCursorPosition],
	);

	const focusContextValue = useMemo(
		() => ({
			activeId: activeFocusId,
			add: addFocusable,
			remove: removeFocusable,
			activate: activateFocusable,
			deactivate: deactivateFocusable,
			enableFocus,
			disableFocus,
			focusNext,
			focusPrevious,
			focus,
		}),
		[
			activeFocusId,
			addFocusable,
			removeFocusable,
			activateFocusable,
			deactivateFocusable,
			enableFocus,
			disableFocus,
			focusNext,
			focusPrevious,
			focus,
		],
	);

	const animationContextValue = useMemo(
		() => ({
			renderThrottleMs,
			subscribe: animationSubscribe,
		}),
		[animationSubscribe, renderThrottleMs],
	);

	return (
		<AppContext.Provider value={appContextValue}>
			<StdinContext.Provider value={stdinContextValue}>
				<StdoutContext.Provider value={stdoutContextValue}>
					<StderrContext.Provider value={stderrContextValue}>
						<FocusContext.Provider value={focusContextValue}>
							<AnimationContext.Provider value={animationContextValue}>
								<CursorContext.Provider value={cursorContextValue}>
									<ErrorBoundary onError={handleExit}>{children}</ErrorBoundary>
								</CursorContext.Provider>
							</AnimationContext.Provider>
						</FocusContext.Provider>
					</StderrContext.Provider>
				</StdoutContext.Provider>
			</StdinContext.Provider>
		</AppContext.Provider>
	);
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function App({
	children,
	stdin,
	stdout,
	stderr,
	writeToStdout,
	writeToStderr,
	exitOnCtrlC,
	onExit,
	onWaitUntilRenderFlush,
	onSuspendTerminal,
	onRegisterInputControl,
	setCursorPosition,
	interactive,
	renderThrottleMs,
}: Props): React.ReactNode {
	const isFocusEnabledRef = useRef(true);
	const [activeFocusId, setActiveFocusId] = useState<string | undefined>(
		undefined,
	);
	// Focusables array is managed internally via setFocusables callback pattern
	// eslint-disable-next-line react/hook-use-state
	const [, setFocusables] = useState<Focusable[]>([]);
	// Track focusables count for tab navigation check (avoids stale closure)
	const focusablesCountRef = useRef(0);
	const animationSubscribersRef = useRef(
		new Map<(currentTime: number) => void, AnimationSubscriber>(),
	);
	const animationTimerRef = useRef<ReturnType<typeof setTimeout> | undefined>(
		undefined,
	);
	// Count how many components enabled raw mode to avoid disabling
	// raw mode until all components don't need it anymore
	const rawModeEnabledCount = useRef(0);
	const pendingDisableRawModeRef = useRef(false);
	// Count how many components enabled bracketed paste mode
	const bracketedPasteModeEnabledCount = useRef(0);
	// eslint-disable-next-line @typescript-eslint/naming-convention
	const internal_eventEmitter = useRef(new EventEmitter());
	// Each useInput hook adds a listener, so the count can legitimately exceed the default limit of 10.
	internal_eventEmitter.current.setMaxListeners(Infinity);
	// Store the currently attached readable listener to avoid stale closure issues
	const readableListenerRef = useRef<(() => void) | undefined>(undefined);
	const inputParserRef = useRef(createInputParser());
	const pendingInputFlushRef = useRef<NodeJS.Timeout | undefined>(undefined);
	// Small delay to let chunked escape sequences complete before flushing as literal input.
	const pendingInputFlushDelayMilliseconds = 20;

	const clearPendingInputFlush = useCallback((): void => {
		if (!pendingInputFlushRef.current) {
			return;
		}

		clearTimeout(pendingInputFlushRef.current);
		pendingInputFlushRef.current = undefined;
	}, []);

	const clearAnimationTimer = useCallback((): void => {
		if (!animationTimerRef.current) {
			return;
		}

		clearTimeout(animationTimerRef.current);
		animationTimerRef.current = undefined;
	}, []);

	const scheduleAnimationTick = useCallback((): void => {
		clearAnimationTimer();

		if (animationSubscribersRef.current.size === 0) {
			return;
		}

		let nextDueTime = Number.POSITIVE_INFINITY;

		for (const subscriber of animationSubscribersRef.current.values()) {
			// One shared timer is enough as long as it wakes at the earliest
			// subscriber deadline and lets slower animations skip that tick.
			nextDueTime = Math.min(nextDueTime, subscriber.nextDueTime);
		}

		const delay = Math.max(0, nextDueTime - performance.now());
		animationTimerRef.current = setTimeout(() => {
			animationTimerRef.current = undefined;
			const currentTime = performance.now();

			for (const subscriber of animationSubscribersRef.current.values()) {
				if (currentTime < subscriber.nextDueTime) {
					continue;
				}

				subscriber.callback(currentTime);
				const elapsedTime = currentTime - subscriber.startTime;
				const elapsedFrames = Math.floor(elapsedTime / subscriber.interval) + 1;
				// Advance from elapsed time rather than callback count so delayed
				// ticks catch up instead of stretching the animation timeline.
				subscriber.nextDueTime =
					subscriber.startTime + elapsedFrames * subscriber.interval;
			}

			scheduleAnimationTick();
		}, delay);
		// Keep the timer ref'd while animations are active so `useAnimation()`
		// can drive process lifetime in both interactive and non-interactive apps.
	}, [clearAnimationTimer]);

	const animationSubscribe = useCallback(
		(
			callback: (currentTime: number) => void,
			interval: number,
		): {readonly startTime: number; readonly unsubscribe: () => void} => {
			const startTime = performance.now();
			// The scheduler owns the start timestamp so hooks can derive frames from
			// the exact same origin that determines each subscriber's due time.
			animationSubscribersRef.current.set(callback, {
				callback,
				interval,
				startTime,
				nextDueTime: startTime + interval,
			});
			scheduleAnimationTick();

			return {
				startTime,
				unsubscribe() {
					animationSubscribersRef.current.delete(callback);

					if (animationSubscribersRef.current.size === 0) {
						clearAnimationTimer();
						return;
					}

					scheduleAnimationTick();
				},
			};
		},
		[clearAnimationTimer, scheduleAnimationTick],
	);

	useEffect(() => {
		return () => {
			clearAnimationTimer();
		};
	}, [clearAnimationTimer]);

	const rawModeStdin = getRawModeStream(stdin);
	const isRawModeSupported = rawModeStdin !== undefined;

	const detachReadableListener = useCallback((): void => {
		if (!readableListenerRef.current) {
			return;
		}

		stdin.removeListener('readable', readableListenerRef.current);
		readableListenerRef.current = undefined;
	}, [stdin]);

	const clearInputState = useCallback((): void => {
		inputParserRef.current.reset();
		clearPendingInputFlush();
		detachReadableListener();
	}, [clearPendingInputFlush, detachReadableListener]);

	const disableRawMode = useCallback((): void => {
		if (!rawModeStdin) {
			return;
		}

		pendingDisableRawModeRef.current = false;
		rawModeStdin.setRawMode(false);
		rawModeStdin.unref?.();
		rawModeEnabledCount.current = 0;
		clearInputState();
	}, [rawModeStdin, clearInputState]);

	const handleExit = useCallback(
		(errorOrResult?: unknown): void => {
			if (
				isRawModeSupported &&
				(rawModeEnabledCount.current > 0 || pendingDisableRawModeRef.current)
			) {
				disableRawMode();
			}

			onExit(errorOrResult);
		},
		[isRawModeSupported, disableRawMode, onExit],
	);

	const handleInput = useCallback(
		(input: string): void => {
			// Exit on Ctrl+C
			// eslint-disable-next-line unicorn/no-hex-escape
			if (input === '\x03' && exitOnCtrlC) {
				handleExit();
				return;
			}

			// Reset focus when there's an active focused component on Esc
			if (input === escape && isFocusEnabledRef.current) {
				setActiveFocusId(undefined);
			}
		},
		[exitOnCtrlC, handleExit],
	);

	const emitInput = useCallback(
		(input: string): void => {
			handleInput(input);
			internal_eventEmitter.current.emit('input', input);
		},
		[handleInput],
	);

	const schedulePendingInputFlush = useCallback((): void => {
		clearPendingInputFlush();
		pendingInputFlushRef.current = setTimeout(() => {
			pendingInputFlushRef.current = undefined;
			const pendingEscape = inputParserRef.current.flushPendingEscape();
			if (!pendingEscape) {
				return;
			}

			emitInput(pendingEscape);
		}, pendingInputFlushDelayMilliseconds);
	}, [clearPendingInputFlush, emitInput]);

	const handleReadable = useCallback((): void => {
		clearPendingInputFlush();
		let chunk;
		// eslint-disable-next-line @typescript-eslint/no-restricted-types
		while ((chunk = stdin.read() as string | null) !== null) {
			const inputEvents = inputParserRef.current.push(chunk);
			for (const event of inputEvents) {
				if (typeof event === 'string') {
					emitInput(event);
				} else {
					// Keep paste on a separate channel from `useInput` so key handlers
					// don't need to branch on mixed key-vs-paste event shapes.
					if (internal_eventEmitter.current.listenerCount('paste') === 0) {
						emitInput(event.paste);
						continue;
					}

					internal_eventEmitter.current.emit('paste', event.paste);
				}
			}
		}

		if (inputParserRef.current.hasPendingEscape()) {
			schedulePendingInputFlush();
		}
	}, [stdin, emitInput, clearPendingInputFlush, schedulePendingInputFlush]);

	const attachReadableListener = useCallback((): void => {
		if (readableListenerRef.current) {
			return;
		}

		// Store the listener reference to avoid stale closure when removing
		readableListenerRef.current = handleReadable;
		stdin.addListener('readable', handleReadable);
	}, [stdin, handleReadable]);

	const handleSetRawMode = useCallback(
		(isEnabled: boolean): void => {
			if (!rawModeStdin) {
				if (stdin === process.stdin) {
					throw new Error(
						'Raw mode is not supported on the current process.stdin, which Ink uses as input stream by default.\nRead about how to prevent this error on https://github.com/vadimdemedes/ink/#israwmodesupported',
					);
				} else {
					throw new Error(
						'Raw mode is not supported on the stdin provided to Ink.\nRead about how to prevent this error on https://github.com/vadimdemedes/ink/#israwmodesupported',
					);
				}
			}

			rawModeStdin.setEncoding('utf8');

			if (isEnabled) {
				if (rawModeEnabledCount.current === 0) {
					// A same-render component swap may have detached input handling while
					// leaving terminal raw mode enabled until the queued disable runs.
					const isRawModeAlreadyEnabled = pendingDisableRawModeRef.current;
					pendingDisableRawModeRef.current = false;

					if (!isRawModeAlreadyEnabled) {
						rawModeStdin.ref?.();
						rawModeStdin.setRawMode(true);
					}

					attachReadableListener();
				}

				rawModeEnabledCount.current++;
				return;
			}

			if (rawModeEnabledCount.current === 0) {
				return;
			}

			if (--rawModeEnabledCount.current === 0) {
				// Stop owning input immediately so pending parser state cannot leak into
				// a replacement `useInput` component mounted in the same React update.
				clearInputState();

				// Defer only the terminal raw-mode teardown so a same-render replacement
				// can keep the process ref and raw mode active without a disable/enable cycle.
				pendingDisableRawModeRef.current = true;
				queueMicrotask(() => {
					if (!pendingDisableRawModeRef.current) {
						return;
					}

					disableRawMode();
				});
			}
		},
		[
			rawModeStdin,
			stdin,
			attachReadableListener,
			clearInputState,
			disableRawMode,
		],
	);

	const handleSetBracketedPasteMode = useCallback(
		(isEnabled: boolean): void => {
			if (!stdout.isTTY) {
				return;
			}

			if (isEnabled) {
				if (bracketedPasteModeEnabledCount.current === 0) {
					stdout.write('\u001B[?2004h');
				}

				bracketedPasteModeEnabledCount.current++;
				return;
			}

			if (bracketedPasteModeEnabledCount.current === 0) {
				return;
			}

			if (--bracketedPasteModeEnabledCount.current === 0) {
				stdout.write('\u001B[?2004l');
			}
		},
		[stdout],
	);

	// Remembers which input modes were active so resumeInput can reinstate exactly
	// those after a terminal suspension, without touching the ref counts (the React
	// components still "own" raw mode/bracketed paste across the suspension).
	const suspendedInputStateRef = useRef({
		rawMode: false,
		bracketedPaste: false,
	});

	const pauseInput = useCallback((): void => {
		const wasRawMode = isRawModeSupported && rawModeEnabledCount.current > 0;
		const wasBracketedPaste = bracketedPasteModeEnabledCount.current > 0;
		suspendedInputStateRef.current = {
			rawMode: wasRawMode,
			bracketedPaste: wasBracketedPaste,
		};

		if (wasBracketedPaste && stdout.isTTY) {
			try {
				stdout.write('\u001B[?2004l');
			} catch {}
		}

		if (wasRawMode) {
			rawModeStdin?.setRawMode(false);
			rawModeStdin?.unref?.();
			clearInputState();
		}
	}, [isRawModeSupported, rawModeStdin, stdout, clearInputState]);

	const resumeInput = useCallback((): void => {
		const {rawMode, bracketedPaste} = suspendedInputStateRef.current;

		if (rawMode) {
			rawModeStdin?.setEncoding('utf8');
			rawModeStdin?.ref?.();
			rawModeStdin?.setRawMode(true);
			attachReadableListener();
		}

		if (bracketedPaste && stdout.isTTY) {
			try {
				stdout.write('\u001B[?2004h');
			} catch {}
		}
	}, [rawModeStdin, stdout, attachReadableListener]);

	// Register input pause/resume in an insertion effect: it runs before every
	// passive effect (parent and child), so a child that calls suspendTerminal()
	// from its own effect always finds the input control already registered. A
	// normal effect would run too late (child effects fire before the parent's).
	useInsertionEffect(() => {
		onRegisterInputControl(pauseInput, resumeInput);
	}, [onRegisterInputControl, pauseInput, resumeInput]);

	// Focus navigation helpers
	const findNextFocusable = useCallback(
		(
			currentFocusables: Focusable[],
			currentActiveFocusId: string | undefined,
		): string | undefined => {
			const activeIndex = currentFocusables.findIndex(focusable => {
				return focusable.id === currentActiveFocusId;
			});

			for (
				let index = activeIndex + 1;
				index < currentFocusables.length;
				index++
			) {
				const focusable = currentFocusables[index];

				if (focusable?.isActive) {
					return focusable.id;
				}
			}

			return undefined;
		},
		[],
	);

	const findPreviousFocusable = useCallback(
		(
			currentFocusables: Focusable[],
			currentActiveFocusId: string | undefined,
		): string | undefined => {
			const activeIndex = currentFocusables.findIndex(focusable => {
				return focusable.id === currentActiveFocusId;
			});

			for (let index = activeIndex - 1; index >= 0; index--) {
				const focusable = currentFocusables[index];

				if (focusable?.isActive) {
					return focusable.id;
				}
			}

			return undefined;
		},
		[],
	);

	const focusNext = useCallback((): void => {
		setFocusables(currentFocusables => {
			setActiveFocusId(currentActiveFocusId => {
				const firstFocusableId = currentFocusables.find(
					focusable => focusable.isActive,
				)?.id;
				const nextFocusableId = findNextFocusable(
					currentFocusables,
					currentActiveFocusId,
				);

				return nextFocusableId ?? firstFocusableId;
			});
			return currentFocusables;
		});
	}, [findNextFocusable]);

	const focusPrevious = useCallback((): void => {
		setFocusables(currentFocusables => {
			setActiveFocusId(currentActiveFocusId => {
				const lastFocusableId = currentFocusables.findLast(
					focusable => focusable.isActive,
				)?.id;
				const previousFocusableId = findPreviousFocusable(
					currentFocusables,
					currentActiveFocusId,
				);

				return previousFocusableId ?? lastFocusableId;
			});
			return currentFocusables;
		});
	}, [findPreviousFocusable]);

	// Handle tab navigation via effect that subscribes to input events
	useEffect(() => {
		const handleTabNavigation = (input: string): void => {
			if (!isFocusEnabledRef.current || focusablesCountRef.current === 0) return;

			if (input === tab) {
				focusNext();
			}

			if (input === shiftTab) {
				focusPrevious();
			}
		};

		internal_eventEmitter.current.on('input', handleTabNavigation);
		const emitter = internal_eventEmitter.current;

		return () => {
			emitter.off('input', handleTabNavigation);
		};
	}, [focusNext, focusPrevious]);

	const enableFocus = useCallback((): void => {
		isFocusEnabledRef.current = true;
	}, []);

	const disableFocus = useCallback((): void => {
		isFocusEnabledRef.current = false;
		setActiveFocusId(undefined);
	}, []);

	const focus = useCallback((id: string): void => {
		setFocusables(currentFocusables => {
			const hasFocusableId = currentFocusables.some(
				focusable => focusable.id === id && focusable.isActive,
			);

			if (hasFocusableId) {
				setActiveFocusId(id);
			}

			return currentFocusables;
		});
	}, []);

	const addFocusable = useCallback(
		(id: string, {autoFocus}: {autoFocus: boolean}): void => {
			setFocusables(currentFocusables => {
				focusablesCountRef.current = currentFocusables.length + 1;

				return [
					...currentFocusables,
					{
						id,
						isActive: true,
					},
				];
			});

			if (autoFocus && isFocusEnabledRef.current) {
				setActiveFocusId(currentActiveFocusId => {
					if (!currentActiveFocusId) {
						return id;
					}

					return currentActiveFocusId;
				});
			}
		},
		[],
	);

	const removeFocusable = useCallback((id: string): void => {
		setActiveFocusId(currentActiveFocusId => {
			if (currentActiveFocusId === id) {
				return undefined;
			}

			return currentActiveFocusId;
		});

		setFocusables(currentFocusables => {
			const filtered = currentFocusables.filter(focusable => {
				return focusable.id !== id;
			});
			focusablesCountRef.current = filtered.length;

			return filtered;
		});
	}, []);

	const activateFocusable = useCallback((id: string): void => {
		setFocusables(currentFocusables =>
			currentFocusables.map(focusable => {
				if (focusable.id !== id) {
					return focusable;
				}

				return {
					id,
					isActive: true,
				};
			}),
		);
	}, []);

	const deactivateFocusable = useCallback((id: string): void => {
		setActiveFocusId(currentActiveFocusId => {
			if (currentActiveFocusId === id) {
				return undefined;
			}

			return currentActiveFocusId;
		});

		setFocusables(currentFocusables =>
			currentFocusables.map(focusable => {
				if (focusable.id !== id) {
					return focusable;
				}

				return {
					id,
					isActive: false,
				};
			}),
		);
	}, []);

	// Handle cursor visibility, raw mode, and bracketed paste mode cleanup on unmount
	useEffect(() => {
		return () => {
			const canWriteToStdout = !stdout.destroyed && !stdout.writableEnded;

			if (interactive && canWriteToStdout) {
				cliCursor.show(stdout);
			}

			if (
				isRawModeSupported &&
				(rawModeEnabledCount.current > 0 || pendingDisableRawModeRef.current)
			) {
				disableRawMode();
			}

			if (bracketedPasteModeEnabledCount.current > 0) {
				if (stdout.isTTY && canWriteToStdout) {
					stdout.write('\u001B[?2004l');
				}

				bracketedPasteModeEnabledCount.current = 0;
			}
		};
	}, [stdout, isRawModeSupported, disableRawMode, interactive]);

	// Memoize context values to prevent unnecessary re-renders
	const appContextValue = useMemo(
		() => ({
			exit: handleExit,
			waitUntilRenderFlush: onWaitUntilRenderFlush,
			suspendTerminal: onSuspendTerminal,
		}),
		[handleExit, onWaitUntilRenderFlush, onSuspendTerminal],
	);

	const stdinContextValue = useMemo(
		() => ({
			stdin,
			setRawMode: handleSetRawMode,
			setBracketedPasteMode: handleSetBracketedPasteMode,
			isRawModeSupported,
			// eslint-disable-next-line @typescript-eslint/naming-convention
			internal_exitOnCtrlC: exitOnCtrlC,
			// eslint-disable-next-line @typescript-eslint/naming-convention
			internal_eventEmitter: internal_eventEmitter.current,
		}),
		[
			stdin,
			handleSetRawMode,
			handleSetBracketedPasteMode,
			isRawModeSupported,
			exitOnCtrlC,
		],
	);

	const stdoutContextValue = useMemo(
		() => ({
			stdout,
			write: writeToStdout,
		}),
		[stdout, writeToStdout],
	);

	const stderrContextValue = useMemo(
		() => ({
			stderr,
			write: writeToStderr,
		}),
		[stderr, writeToStderr],
	);

	const cursorContextValue = useMemo(
		() => ({
			setCursorPosition,
		}),
		[setCursorPosition],
	);

	const focusContextValue = useMemo(
		() => ({
			activeId: activeFocusId,
			add: addFocusable,
			remove: removeFocusable,
			activate: activateFocusable,
			deactivate: deactivateFocusable,
			enableFocus,
			disableFocus,
			focusNext,
			focusPrevious,
			focus,
		}),
		[
			activeFocusId,
			addFocusable,
			removeFocusable,
			activateFocusable,
			deactivateFocusable,
			enableFocus,
			disableFocus,
			focusNext,
			focusPrevious,
			focus,
		],
	);

	const animationContextValue = useMemo(
		() => ({
			renderThrottleMs,
			subscribe: animationSubscribe,
		}),
		[animationSubscribe, renderThrottleMs],
	);

	return (
		<AppContext.Provider value={appContextValue}>
			<StdinContext.Provider value={stdinContextValue}>
				<StdoutContext.Provider value={stdoutContextValue}>
					<StderrContext.Provider value={stderrContextValue}>
						<FocusContext.Provider value={focusContextValue}>
							<AnimationContext.Provider value={animationContextValue}>
								<CursorContext.Provider value={cursorContextValue}>
									<ErrorBoundary onError={handleExit}>{children}</ErrorBoundary>
								</CursorContext.Provider>
							</AnimationContext.Provider>
						</FocusContext.Provider>
					</StderrContext.Provider>
				</StdoutContext.Provider>
			</StdinContext.Provider>
		</AppContext.Provider>
	);
}
```


#### 📄 檔案: `src/hooks/use-focus.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:12, E:10, A:0) ➔ After(N:11, E:10, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 2, +Edges: 1, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `useId (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `useMemo (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `id` (FUNCTION_DEF)
  • + [新增呼叫邊] `useFocus` ──[CALLS]──> `useId (External/Unresolved)`
  • - [移除呼叫邊] `useFocus` ──[CALLS]──> `useMemo (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `useFocus()`
- **變更前簽章 (Before)**: `useFocus({
	isActive = true,
	autoFocus = false,
	id: customId,
}: Input = {})` (L38~L83)
- **變更後簽章 (After)**: `useFocus({
	isActive = true,
	autoFocus = false,
	id: customId,
}: Input = {})` (L38~L83)

#### ◀️ 變更前實作碼 (Before Implementation):
```
({
	isActive = true,
	autoFocus = false,
	id: customId,
}: Input = {}): Output => {
	const {isRawModeSupported, setRawMode} = useStdin();
	const {activeId, add, remove, activate, deactivate, focus} =
		useContext(FocusContext);

	const id = useMemo(() => {
		return customId ?? Math.random().toString().slice(2, 7);
	}, [customId]);

	useEffect(() => {
		add(id, {autoFocus});

		return () => {
			remove(id);
		};
	}, [id, autoFocus, add, remove]);

	useEffect(() => {
		if (isActive) {
			activate(id);
		} else {
			deactivate(id);
		}
	}, [isActive, id, activate, deactivate]);

	useEffect(() => {
		if (!isRawModeSupported || !isActive) {
			return;
		}

		setRawMode(true);

		return () => {
			setRawMode(false);
		};
	}, [isActive, isRawModeSupported, setRawMode]);

	return {
		isFocused: Boolean(id) && activeId === id,
		focus,
	};
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
({
	isActive = true,
	autoFocus = false,
	id: customId,
}: Input = {}): Output => {
	const {isRawModeSupported, setRawMode} = useStdin();
	const {activeId, add, remove, activate, deactivate, focus} =
		useContext(FocusContext);

	const generatedId = useId();
	const id = customId ?? generatedId;

	useEffect(() => {
		add(id, {autoFocus});

		return () => {
			remove(id);
		};
	}, [id, autoFocus, add, remove]);

	useEffect(() => {
		// Reapply active state when autoFocus changes and re-registers this component.
		if (isActive) {
			activate(id);
		} else {
			deactivate(id);
		}
	}, [isActive, id, autoFocus, activate, deactivate]);

	useEffect(() => {
		if (!isRawModeSupported || !isActive) {
			return;
		}

		setRawMode(true);

		return () => {
			setRawMode(false);
		};
	}, [isActive, isRawModeSupported, setRawMode]);

	return {
		isFocused: Boolean(id) && activeId === id,
		focus,
	};
}
```


---

### 🔹 Commit #14: `3be9ed7c`
- **完整 Hash**: `3be9ed7c8c0e96969e484796063ac30a112ea7f4`
- **說明 (Ground Truth)**: Fix color parsing
- **變更檔案數**: 1

#### 📄 檔案: `src/colorize.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:5, E:2, A:0) ➔ After(N:5, E:2, A:0)
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

### 🔹 函式: `isNamedColor()`
- **變更前簽章 (Before)**: `isNamedColor(color: string)` (L8~L10)
- **變更後簽章 (After)**: `isNamedColor(color: string)` (L12~L14)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(color: string): color is ForegroundColorName => {
	return color in chalk;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(color: string): color is ForegroundColorName => {
	return foregroundColorNames.includes(color as ForegroundColorName);
}
```

### 🔹 函式: `rgbRegex()`
- **變更前簽章 (Before)**: `[Module State] rgbRegex` (L5~L5)
- **變更後簽章 (After)**: `[Module State] rgbRegex` (L9~L9)

#### ◀️ 變更前實作碼 (Before Implementation):
```
rgbRegex = /^rgb\(\s?(\d+),\s?(\d+),\s?(\d+)\s?\)$/
```

#### ▶️ 變更後實作碼 (After Implementation):
```
rgbRegex = /^rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/
```


---

### 🔹 Commit #15: `77aba4a9`
- **完整 Hash**: `77aba4a97fca2a19c5950daad2828fceb885f305`
- **說明 (Ground Truth)**: Fix multi-line `<Text>` vanishing when it starts above the top of the output (#1001)
- **變更檔案數**: 1

#### 📄 檔案: `src/output.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:21, E:10, A:0) ➔ After(N:21, E:10, A:0)
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

### 🔹 函式: `get()`
- **變更前簽章 (Before)**: `get()` (L195~L380)
- **變更後簽章 (After)**: `get()` (L195~L383)

#### ◀️ 變更前實作碼 (Before Implementation):
```
get(): {output: string; height: number} {
		// Initialize output array with a specific set of rows, so that margin/padding at the bottom is preserved
		const output: StyledChar[][] = [];

		for (let y = 0; y < this.height; y++) {
			const row: StyledChar[] = [];

			for (let x = 0; x < this.width; x++) {
				row.push({
					type: 'char',
					value: ' ',
					fullWidth: false,
					styles: [],
				});
			}

			output.push(row);
		}

		const clips: Clip[] = [];

		for (const operation of this.operations) {
			if (operation.type === 'clip') {
				// Nested clips must intersect, not replace, otherwise an inner `overflow="hidden"` box lets content escape the outer clip and overwrite surrounding UI.
				clips.push(intersectClips(clips.at(-1), operation.clip));
			}

			if (operation.type === 'unclip') {
				clips.pop();
			}

			if (operation.type === 'write') {
				const {text, transformers} = operation;
				let {x, y} = operation;
				let lines = text.split('\n');

				const clip = clips.at(-1);

				if (clip) {
					// Two nested clips can intersect to nothing. Nothing is visible, so bail out before slicing.
					if (isClipEmpty(clip)) {
						continue;
					}

					const clipHorizontally =
						typeof clip?.x1 === 'number' && typeof clip?.x2 === 'number';

					const clipVertically =
						typeof clip?.y1 === 'number' && typeof clip?.y2 === 'number';

					// If text is positioned outside of clipping area altogether,
					// skip to the next operation to avoid unnecessary calculations
					if (clipHorizontally) {
						const width = this.caches.getWidestLine(text);

						if (x + width < clip.x1! || x > clip.x2!) {
							continue;
						}
					}

					if (clipVertically) {
						const height = lines.length;

						if (y + height < clip.y1! || y > clip.y2!) {
							continue;
						}
					}

					if (clipHorizontally) {
						lines = lines.map(line => {
							const from = x < clip.x1! ? clip.x1! - x : 0;
							const width = this.caches.getStringWidth(line);
							const to = x + width > clip.x2! ? clip.x2! - x : width;

							return this.sliceLineToColumns(line, from, to);
						});

						if (x < clip.x1!) {
							x = clip.x1!;
						}
					}

					if (clipVertically) {
						const from = y < clip.y1! ? clip.y1! - y : 0;
						const height = lines.length;
						const to = y + height > clip.y2! ? clip.y2! - y : height;

						lines = lines.slice(from, to);

						if (y < clip.y1!) {
							y = clip.y1!;
						}
					}
				}

				let offsetY = 0;

				for (let [index, line] of lines.entries()) {
					const currentLine = output[y + offsetY];

					// Line can be missing if `text` is taller than height of pre-initialized `this.output`
					if (!currentLine) {
						continue;
					}

					for (const transformer of transformers) {
						line = transformer(line, index);
					}

					const characters = this.caches.getStyledChars(line);
					let offsetX = x;

					// Nothing to write (e.g. line was clipped away).
					if (characters.length === 0) {
						offsetY++;
						continue;
					}

					const spaceCell: StyledChar = {
						type: 'char',
						value: ' ',
						fullWidth: false,
						styles: [],
					};

					// Wide characters (e.g. CJK) occupy two cells: a leading
					// cell with the character and a trailing placeholder with
					// value ''. When an overlapping write lands in the middle
					// of a wide character, the boundary cells need cleanup so
					// the terminal never renders a half-visible wide character.
					if (
						currentLine[offsetX]?.value === '' &&
						offsetX > 0 &&
						this.caches.getStringWidth(currentLine[offsetX - 1]?.value ?? '') >
							1
					) {
						currentLine[offsetX - 1] = spaceCell;
					}

					for (const character of characters) {
						currentLine[offsetX] = character;

						// Determine printed width using string-width to align with measurement
						const characterWidth = Math.max(
							1,
							this.caches.getStringWidth(character.value),
						);

						// For multi-column characters, clear following cells to avoid stray spaces/artifacts
						if (characterWidth > 1) {
							for (let index = 1; index < characterWidth; index++) {
								currentLine[offsetX + index] = {
									type: 'char',
									value: '',
									fullWidth: false,
									styles: character.styles,
								};
							}
						}

						offsetX += characterWidth;
					}

					if (currentLine[offsetX]?.value === '') {
						currentLine[offsetX] = spaceCell;
					}

					offsetY++;
				}
			}
		}

		const generatedOutput = output
			.map(line => {
				// See https://github.com/vadimdemedes/ink/pull/564#issuecomment-1637022742
				const lineWithoutEmptyItems = line.filter(item => item !== undefined);

				return styledCharsToString(lineWithoutEmptyItems).trimEnd();
			})
			.join('\n');

		return {
			output: generatedOutput,
			height: output.length,
		};
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
get(): {output: string; height: number} {
		// Initialize output array with a specific set of rows, so that margin/padding at the bottom is preserved
		const output: StyledChar[][] = [];

		for (let y = 0; y < this.height; y++) {
			const row: StyledChar[] = [];

			for (let x = 0; x < this.width; x++) {
				row.push({
					type: 'char',
					value: ' ',
					fullWidth: false,
					styles: [],
				});
			}

			output.push(row);
		}

		const clips: Clip[] = [];

		for (const operation of this.operations) {
			if (operation.type === 'clip') {
				// Nested clips must intersect, not replace, otherwise an inner `overflow="hidden"` box lets content escape the outer clip and overwrite surrounding UI.
				clips.push(intersectClips(clips.at(-1), operation.clip));
			}

			if (operation.type === 'unclip') {
				clips.pop();
			}

			if (operation.type === 'write') {
				const {text, transformers} = operation;
				let {x, y} = operation;
				let lines = text.split('\n');

				const clip = clips.at(-1);

				if (clip) {
					// Two nested clips can intersect to nothing. Nothing is visible, so bail out before slicing.
					if (isClipEmpty(clip)) {
						continue;
					}

					const clipHorizontally =
						typeof clip?.x1 === 'number' && typeof clip?.x2 === 'number';

					const clipVertically =
						typeof clip?.y1 === 'number' && typeof clip?.y2 === 'number';

					// If text is positioned outside of clipping area altogether,
					// skip to the next operation to avoid unnecessary calculations
					if (clipHorizontally) {
						const width = this.caches.getWidestLine(text);

						if (x + width < clip.x1! || x > clip.x2!) {
							continue;
						}
					}

					if (clipVertically) {
						const height = lines.length;

						if (y + height < clip.y1! || y > clip.y2!) {
							continue;
						}
					}

					if (clipHorizontally) {
						lines = lines.map(line => {
							const from = x < clip.x1! ? clip.x1! - x : 0;
							const width = this.caches.getStringWidth(line);
							const to = x + width > clip.x2! ? clip.x2! - x : width;

							return this.sliceLineToColumns(line, from, to);
						});

						if (x < clip.x1!) {
							x = clip.x1!;
						}
					}

					if (clipVertically) {
						const from = y < clip.y1! ? clip.y1! - y : 0;
						const height = lines.length;
						const to = y + height > clip.y2! ? clip.y2! - y : height;

						lines = lines.slice(from, to);

						if (y < clip.y1!) {
							y = clip.y1!;
						}
					}
				}

				let offsetY = 0;

				for (let [index, line] of lines.entries()) {
					const currentLine = output[y + offsetY];

					// Line can be missing if `text` starts above the top of
					// `this.output` or is taller than its height. Advance `offsetY`
					// anyway, so the lines that do land inside still get written.
					if (!currentLine) {
						offsetY++;
						continue;
					}

					for (const transformer of transformers) {
						line = transformer(line, index);
					}

					const characters = this.caches.getStyledChars(line);
					let offsetX = x;

					// Nothing to write (e.g. line was clipped away).
					if (characters.length === 0) {
						offsetY++;
						continue;
					}

					const spaceCell: StyledChar = {
						type: 'char',
						value: ' ',
						fullWidth: false,
						styles: [],
					};

					// Wide characters (e.g. CJK) occupy two cells: a leading
					// cell with the character and a trailing placeholder with
					// value ''. When an overlapping write lands in the middle
					// of a wide character, the boundary cells need cleanup so
					// the terminal never renders a half-visible wide character.
					if (
						currentLine[offsetX]?.value === '' &&
						offsetX > 0 &&
						this.caches.getStringWidth(currentLine[offsetX - 1]?.value ?? '') >
							1
					) {
						currentLine[offsetX - 1] = spaceCell;
					}

					for (const character of characters) {
						currentLine[offsetX] = character;

						// Determine printed width using string-width to align with measurement
						const characterWidth = Math.max(
							1,
							this.caches.getStringWidth(character.value),
						);

						// For multi-column characters, clear following cells to avoid stray spaces/artifacts
						if (characterWidth > 1) {
							for (let index = 1; index < characterWidth; index++) {
								currentLine[offsetX + index] = {
									type: 'char',
									value: '',
									fullWidth: false,
									styles: character.styles,
								};
							}
						}

						offsetX += characterWidth;
					}

					if (currentLine[offsetX]?.value === '') {
						currentLine[offsetX] = spaceCell;
					}

					offsetY++;
				}
			}
		}

		const generatedOutput = output
			.map(line => {
				// See https://github.com/vadimdemedes/ink/pull/564#issuecomment-1637022742
				const lineWithoutEmptyItems = line.filter(item => item !== undefined);

				return styledCharsToString(lineWithoutEmptyItems).trimEnd();
			})
			.join('\n');

		return {
			output: generatedOutput,
			height: output.length,
		};
	}
```


---

### 🔹 Commit #16: `3809acc1`
- **完整 Hash**: `3809acc1dffbc5179c78c5b0effb18b74e20adbc`
- **說明 (Ground Truth)**: Fix `wrapText` cache key collision between different texts and widths (#998)
- **變更檔案數**: 1

#### 📄 檔案: `src/wrap-text.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:5, E:3, A:0) ➔ After(N:5, E:3, A:0)
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

### 🔹 函式: `wrapText()`
- **變更前簽章 (Before)**: `wrapText(
	text: string,
	maxWidth: number,
	wrapType: Styles['textWrap'],
)` (L8~L54)
- **變更後簽章 (After)**: `wrapText(
	text: string,
	maxWidth: number,
	wrapType: Styles['textWrap'],
)` (L8~L57)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(
	text: string,
	maxWidth: number,
	wrapType: Styles['textWrap'],
): string => {
	const cacheKey = text + String(maxWidth) + String(wrapType);
	const cachedText = wrapTextCache.get(cacheKey);

	if (cachedText !== undefined) {
		return cachedText;
	}

	let wrappedText = text;

	if (wrapType === 'wrap') {
		wrappedText = wrapAnsi(text, maxWidth, {
			trim: false,
			hard: true,
		});
	}

	if (wrapType === 'hard') {
		wrappedText = wrapAnsi(text, maxWidth, {
			trim: false,
			hard: true,
			wordWrap: false,
		});
	}

	if (wrapType!.startsWith('truncate')) {
		let position: 'end' | 'middle' | 'start' = 'end';

		if (wrapType === 'truncate-middle') {
			position = 'middle';
		}

		if (wrapType === 'truncate-start') {
			position = 'start';
		}

		wrappedText = cliTruncate(text, maxWidth, {position});
	}

	wrapTextCache.set(cacheKey, wrappedText);

	return wrappedText;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(
	text: string,
	maxWidth: number,
	wrapType: Styles['textWrap'],
): string => {
	// `text` goes last because it's the only part of the key that can contain
	// arbitrary characters. With it first, ('ab', 12, 'wrap') and
	// ('ab1', 2, 'wrap') both produce the key `ab12wrap` and share a result.
	const cacheKey = `${maxWidth}\u0000${String(wrapType)}\u0000${text}`;
	const cachedText = wrapTextCache.get(cacheKey);

	if (cachedText !== undefined) {
		return cachedText;
	}

	let wrappedText = text;

	if (wrapType === 'wrap') {
		wrappedText = wrapAnsi(text, maxWidth, {
			trim: false,
			hard: true,
		});
	}

	if (wrapType === 'hard') {
		wrappedText = wrapAnsi(text, maxWidth, {
			trim: false,
			hard: true,
			wordWrap: false,
		});
	}

	if (wrapType!.startsWith('truncate')) {
		let position: 'end' | 'middle' | 'start' = 'end';

		if (wrapType === 'truncate-middle') {
			position = 'middle';
		}

		if (wrapType === 'truncate-start') {
			position = 'start';
		}

		wrappedText = cliTruncate(text, maxWidth, {position});
	}

	wrapTextCache.set(cacheKey, wrappedText);

	return wrappedText;
}
```


---

### 🔹 Commit #17: `fe1d1233`
- **完整 Hash**: `fe1d1233472b97071d9ea9d9bdd72660f4cf4ae0`
- **說明 (Ground Truth)**: Fix: Clear viewport with home + erase-down instead of `clearTerminal`  to preserve scrollback (#994)
- **變更檔案數**: 1

#### 📄 檔案: `src/ink.tsx`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:65, E:39, A:0) ➔ After(N:66, E:39, A:0)
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
  • + [新增節點] `homeAndEraseDown` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `renderInteractiveFrame()`
- **變更前簽章 (Before)**: `renderInteractiveFrame(
		output: string,
		outputHeight: number,
		staticOutput: string,
	)` (L1099~L1164)
- **變更後簽章 (After)**: `renderInteractiveFrame(
		output: string,
		outputHeight: number,
		staticOutput: string,
	)` (L1108~L1173)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private renderInteractiveFrame(
		output: string,
		outputHeight: number,
		staticOutput: string,
	): void {
		const hasStaticOutput = staticOutput !== '';
		const isTty = Boolean(this.options.stdout.isTTY);

		// Detect fullscreen: output fills or exceeds terminal height.
		// Only apply when writing to a real TTY — piped output always gets trailing newlines.
		const viewportRows = isTty ? getWindowSize(this.options.stdout).rows : 24;
		const isFullscreen = isTty && outputHeight >= viewportRows;
		const outputToRender = isFullscreen ? output : output + '\n';

		const shouldClearTerminal = shouldClearTerminalForFrame({
			isTty,
			viewportRows,
			previousOutputHeight: this.lastOutputHeight,
			nextOutputHeight: outputHeight,
			isUnmounting: this.isUnmounting,
		});

		if (shouldClearTerminal) {
			const sync = this.shouldSync();
			if (sync) {
				this.options.stdout.write(bsu);
			}

			this.options.stdout.write(
				ansiEscapes.clearTerminal + this.fullStaticOutput + outputToRender,
			);
			this.lastOutput = output;
			this.lastOutputToRender = outputToRender;
			this.lastOutputHeight = outputHeight;
			this.log.sync(outputToRender);

			if (sync) {
				this.options.stdout.write(esu);
			}

			return;
		}

		// To ensure static output is cleanly rendered before main output, clear main output first
		if (hasStaticOutput) {
			const sync = this.shouldSync();
			if (sync) {
				this.options.stdout.write(bsu);
			}

			this.log.clear();
			this.options.stdout.write(staticOutput);
			this.log(outputToRender);

			if (sync) {
				this.options.stdout.write(esu);
			}
		} else if (output !== this.lastOutput || this.log.isCursorDirty()) {
			// ThrottledLog manages its own bsu/esu at actual write time
			this.throttledLog(outputToRender);
		}

		this.lastOutput = output;
		this.lastOutputToRender = outputToRender;
		this.lastOutputHeight = outputHeight;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private renderInteractiveFrame(
		output: string,
		outputHeight: number,
		staticOutput: string,
	): void {
		const hasStaticOutput = staticOutput !== '';
		const isTty = Boolean(this.options.stdout.isTTY);

		// Detect fullscreen: output fills or exceeds terminal height.
		// Only apply when writing to a real TTY — piped output always gets trailing newlines.
		const viewportRows = isTty ? getWindowSize(this.options.stdout).rows : 24;
		const isFullscreen = isTty && outputHeight >= viewportRows;
		const outputToRender = isFullscreen ? output : output + '\n';

		const shouldClearTerminal = shouldClearTerminalForFrame({
			isTty,
			viewportRows,
			previousOutputHeight: this.lastOutputHeight,
			nextOutputHeight: outputHeight,
			isUnmounting: this.isUnmounting,
		});

		if (shouldClearTerminal) {
			const sync = this.shouldSync();
			if (sync) {
				this.options.stdout.write(bsu);
			}

			this.options.stdout.write(
				homeAndEraseDown + this.fullStaticOutput + outputToRender,
			);
			this.lastOutput = output;
			this.lastOutputToRender = outputToRender;
			this.lastOutputHeight = outputHeight;
			this.log.sync(outputToRender);

			if (sync) {
				this.options.stdout.write(esu);
			}

			return;
		}

		// To ensure static output is cleanly rendered before main output, clear main output first
		if (hasStaticOutput) {
			const sync = this.shouldSync();
			if (sync) {
				this.options.stdout.write(bsu);
			}

			this.log.clear();
			this.options.stdout.write(staticOutput);
			this.log(outputToRender);

			if (sync) {
				this.options.stdout.write(esu);
			}
		} else if (output !== this.lastOutput || this.log.isCursorDirty()) {
			// ThrottledLog manages its own bsu/esu at actual write time
			this.throttledLog(outputToRender);
		}

		this.lastOutput = output;
		this.lastOutputToRender = outputToRender;
		this.lastOutputHeight = outputHeight;
	}
```


---

### 🔹 Commit #18: `ad9e3ea4`
- **完整 Hash**: `ad9e3ea430acd3411be1c7578a2859f810a848ec`
- **說明 (Ground Truth)**: Fix unbounded text caches
- **變更檔案數**: 2

#### 📄 檔案: `src/measure-text.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:3, E:1, A:0) ➔ After(N:3, E:1, A:0)
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

### 🔹 函式: `cache()`
- **變更前簽章 (Before)**: `[Module State] cache` (L3~L3)
- **變更後簽章 (After)**: `[Module State] cache` (L4~L4)

#### ◀️ 變更前實作碼 (Before Implementation):
```
cache = new Map<string, Output>()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
cache = new QuickLRU<string, Output>({maxSize: 4096})
```


#### 📄 檔案: `src/wrap-text.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:5, E:3, A:0) ➔ After(N:5, E:3, A:0)
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
  • + [新增節點] `wrapTextCache` (MODULE_STATE)
  • - [移除節點] `cache` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `wrapText()`
- **變更前簽章 (Before)**: `wrapText(
	text: string,
	maxWidth: number,
	wrapType: Styles['textWrap'],
)` (L7~L53)
- **變更後簽章 (After)**: `wrapText(
	text: string,
	maxWidth: number,
	wrapType: Styles['textWrap'],
)` (L8~L54)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(
	text: string,
	maxWidth: number,
	wrapType: Styles['textWrap'],
): string => {
	const cacheKey = text + String(maxWidth) + String(wrapType);
	const cachedText = cache[cacheKey];

	if (cachedText) {
		return cachedText;
	}

	let wrappedText = text;

	if (wrapType === 'wrap') {
		wrappedText = wrapAnsi(text, maxWidth, {
			trim: false,
			hard: true,
		});
	}

	if (wrapType === 'hard') {
		wrappedText = wrapAnsi(text, maxWidth, {
			trim: false,
			hard: true,
			wordWrap: false,
		});
	}

	if (wrapType!.startsWith('truncate')) {
		let position: 'end' | 'middle' | 'start' = 'end';

		if (wrapType === 'truncate-middle') {
			position = 'middle';
		}

		if (wrapType === 'truncate-start') {
			position = 'start';
		}

		wrappedText = cliTruncate(text, maxWidth, {position});
	}

	cache[cacheKey] = wrappedText;

	return wrappedText;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(
	text: string,
	maxWidth: number,
	wrapType: Styles['textWrap'],
): string => {
	const cacheKey = text + String(maxWidth) + String(wrapType);
	const cachedText = wrapTextCache.get(cacheKey);

	if (cachedText !== undefined) {
		return cachedText;
	}

	let wrappedText = text;

	if (wrapType === 'wrap') {
		wrappedText = wrapAnsi(text, maxWidth, {
			trim: false,
			hard: true,
		});
	}

	if (wrapType === 'hard') {
		wrappedText = wrapAnsi(text, maxWidth, {
			trim: false,
			hard: true,
			wordWrap: false,
		});
	}

	if (wrapType!.startsWith('truncate')) {
		let position: 'end' | 'middle' | 'start' = 'end';

		if (wrapType === 'truncate-middle') {
			position = 'middle';
		}

		if (wrapType === 'truncate-start') {
			position = 'start';
		}

		wrappedText = cliTruncate(text, maxWidth, {position});
	}

	wrapTextCache.set(cacheKey, wrappedText);

	return wrappedText;
}
```


---

### 🔹 Commit #19: `cdc18fa4`
- **完整 Hash**: `cdc18fa4942b580cda13304545cc2cf18fdde9b8`
- **說明 (Ground Truth)**: Fix: Keep cursor on the last line when output has no trailing newline (#982)
- **變更檔案數**: 2

#### 📄 檔案: `src/cursor-helpers.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:7, E:3, A:0) ➔ After(N:7, E:3, A:0)
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

### 🔹 函式: `buildCursorOnlySequence()`
- **變更前簽章 (Before)**: `buildCursorOnlySequence(input: CursorOnlyInput)` (L73~L84)
- **變更後簽章 (After)**: `buildCursorOnlySequence(input: CursorOnlyInput)` (L86~L97)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(input: CursorOnlyInput): string => {
	const hidePrefix = input.cursorWasShown ? hideCursorEscape : '';
	const returnToBottom = buildReturnToBottom(
		input.previousLineCount,
		input.previousCursorPosition,
	);
	const cursorSuffix = buildCursorSuffix(
		input.visibleLineCount,
		input.cursorPosition,
	);
	return hidePrefix + returnToBottom + cursorSuffix;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(input: CursorOnlyInput): string => {
	const hidePrefix = input.cursorWasShown ? hideCursorEscape : '';
	const returnToBottom = buildReturnToBottom(
		input.previousLineCount,
		input.previousCursorPosition,
	);
	const cursorSuffix = buildCursorSuffix(
		input.previousLineCount - 1,
		input.cursorPosition,
	);
	return hidePrefix + returnToBottom + cursorSuffix;
}
```

### 🔹 函式: `buildCursorSuffix()`
- **變更前簽章 (Before)**: `buildCursorSuffix(
	visibleLineCount: number,
	cursorPosition: CursorPosition | undefined,
)` (L25~L39)
- **變更後簽章 (After)**: `buildCursorSuffix(
	bottomLine: number,
	cursorPosition: CursorPosition | undefined,
)` (L35~L49)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(
	visibleLineCount: number,
	cursorPosition: CursorPosition | undefined,
): string => {
	if (!cursorPosition) {
		return '';
	}

	const moveUp = visibleLineCount - cursorPosition.y;
	return (
		(moveUp > 0 ? ansiEscapes.cursorUp(moveUp) : '') +
		ansiEscapes.cursorTo(cursorPosition.x) +
		showCursorEscape
	);
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(
	bottomLine: number,
	cursorPosition: CursorPosition | undefined,
): string => {
	if (!cursorPosition) {
		return '';
	}

	const moveUp = bottomLine - cursorPosition.y;
	return (
		(moveUp > 0 ? ansiEscapes.cursorUp(moveUp) : '') +
		ansiEscapes.cursorTo(cursorPosition.x) +
		showCursorEscape
	);
}
```


#### 📄 檔案: `src/log-update.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:29, E:28, A:0) ➔ After(N:29, E:25, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 3, ΔFuncs: 6, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除呼叫邊] `render` ──[CALLS]──> `visibleLineCount`
  • - [移除呼叫邊] `sync` ──[CALLS]──> `visibleLineCount`
  • - [移除呼叫邊] `sync` ──[CALLS]──> `visibleLineCount`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'hasChanges' 被深鎖在內部閉包 (scope:createStandard@after/src/log-update.ts:L31C24)，外部無法調用！ (共 2 處)
  - 💥 作用域阻隔: 函式 'getActiveCursor' 被深鎖在內部閉包 (scope:createStandard@after/src/log-update.ts:L31C24)，外部無法調用！ (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `createIncremental()`
- **變更前簽章 (Before)**: `createIncremental(
	stream: Writable,
	{showCursor = false} = {},
)` (L174~L375)
- **變更後簽章 (After)**: `createIncremental(
	stream: Writable,
	{showCursor = false} = {},
)` (L170~L371)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(
	stream: Writable,
	{showCursor = false} = {},
): LogUpdate => {
	let previousLines: string[] = [];
	let previousOutput = '';
	let hasHiddenCursor = false;
	let cursorPosition: CursorPosition | undefined;
	let cursorDirty = false;
	let previousCursorPosition: CursorPosition | undefined;
	let cursorWasShown = false;

	const getActiveCursor = () => (cursorDirty ? cursorPosition : undefined);
	const hasChanges = (
		str: string,
		activeCursor: CursorPosition | undefined,
	): boolean => {
		const cursorChanged = cursorPositionChanged(
			activeCursor,
			previousCursorPosition,
		);
		return str !== previousOutput || cursorChanged;
	};

	const render = (str: string) => {
		if (!showCursor && !hasHiddenCursor) {
			cliCursor.hide(stream);
			hasHiddenCursor = true;
		}

		// Only use cursor if setCursorPosition was called since last render.
		// This ensures stale positions don't persist after component unmount.
		const activeCursor = getActiveCursor();
		cursorDirty = false;
		const cursorChanged = cursorPositionChanged(
			activeCursor,
			previousCursorPosition,
		);

		if (!hasChanges(str, activeCursor)) {
			return false;
		}

		const nextLines = str.split('\n');
		const visibleCount = visibleLineCount(nextLines, str);
		const previousVisible = visibleLineCount(previousLines, previousOutput);

		if (str === previousOutput && cursorChanged) {
			stream.write(
				buildCursorOnlySequence({
					cursorWasShown,
					previousLineCount: previousLines.length,
					previousCursorPosition,
					visibleLineCount: visibleCount,
					cursorPosition: activeCursor,
				}),
			);
			previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
			cursorWasShown = activeCursor !== undefined;
			return true;
		}

		const returnPrefix = buildReturnToBottomPrefix(
			cursorWasShown,
			previousLines.length,
			previousCursorPosition,
		);

		if (str === '\n' || previousOutput.length === 0) {
			const cursorSuffix = buildCursorSuffix(visibleCount, activeCursor);
			stream.write(
				returnPrefix +
					ansiEscapes.eraseLines(previousLines.length) +
					str +
					cursorSuffix,
			);
			cursorWasShown = activeCursor !== undefined;
			previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
			previousOutput = str;
			previousLines = nextLines;
			return true;
		}

		const hasTrailingNewline = str.endsWith('\n');

		// We aggregate all chunks for incremental rendering into a buffer, and then write them to stdout at the end.
		const buffer: string[] = [];

		buffer.push(returnPrefix);

		// Clear extra lines if the current content's line count is lower than the previous.
		if (visibleCount < previousVisible) {
			const previousHadTrailingNewline = previousOutput.endsWith('\n');
			const extraSlot = previousHadTrailingNewline ? 1 : 0;
			buffer.push(
				ansiEscapes.eraseLines(previousVisible - visibleCount + extraSlot),
				ansiEscapes.cursorUp(visibleCount),
			);
		} else {
			buffer.push(ansiEscapes.cursorUp(previousLines.length - 1));
		}

		for (let i = 0; i < visibleCount; i++) {
			const isLastLine = i === visibleCount - 1;

			// We do not write lines if the contents are the same. This prevents flickering during renders.
			if (nextLines[i] === previousLines[i]) {
				// Don't move past the last line when there's no trailing newline,
				// otherwise the cursor overshoots the rendered block.
				if (!isLastLine || hasTrailingNewline) {
					buffer.push(ansiEscapes.cursorNextLine);
				}

				continue;
			}

			buffer.push(
				ansiEscapes.cursorTo(0) +
					nextLines[i] +
					ansiEscapes.eraseEndLine +
					// Don't append newline after the last line when the input
					// has no trailing newline (fullscreen mode).
					(isLastLine && !hasTrailingNewline ? '' : '\n'),
			);
		}

		const cursorSuffix = buildCursorSuffix(visibleCount, activeCursor);
		buffer.push(cursorSuffix);

		stream.write(buffer.join(''));

		cursorWasShown = activeCursor !== undefined;
		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		previousOutput = str;
		previousLines = nextLines;
		return true;
	};

	render.clear = () => {
		const prefix = buildReturnToBottomPrefix(
			cursorWasShown,
			previousLines.length,
			previousCursorPosition,
		);
		stream.write(prefix + ansiEscapes.eraseLines(previousLines.length));
		previousOutput = '';
		previousLines = [];
		previousCursorPosition = undefined;
		cursorWasShown = false;
	};

	render.done = () => {
		previousOutput = '';
		previousLines = [];
		previousCursorPosition = undefined;
		cursorWasShown = false;

		if (!showCursor) {
			cliCursor.show(stream);
			hasHiddenCursor = false;
		}
	};

	render.reset = () => {
		previousOutput = '';
		previousLines = [];
		previousCursorPosition = undefined;
		cursorWasShown = false;
	};

	render.sync = (str: string) => {
		const activeCursor = cursorDirty ? cursorPosition : undefined;
		cursorDirty = false;

		const lines = str.split('\n');
		previousOutput = str;
		previousLines = lines;

		if (!activeCursor && cursorWasShown) {
			stream.write(hideCursorEscape);
		}

		if (activeCursor) {
			stream.write(
				buildCursorSuffix(visibleLineCount(lines, str), activeCursor),
			);
		}

		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		cursorWasShown = activeCursor !== undefined;
	};

	render.setCursorPosition = (position: CursorPosition | undefined) => {
		cursorPosition = position;
		cursorDirty = true;
	};

	render.isCursorDirty = () => cursorDirty;
	render.willRender = (str: string) => hasChanges(str, getActiveCursor());

	return render;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(
	stream: Writable,
	{showCursor = false} = {},
): LogUpdate => {
	let previousLines: string[] = [];
	let previousOutput = '';
	let hasHiddenCursor = false;
	let cursorPosition: CursorPosition | undefined;
	let cursorDirty = false;
	let previousCursorPosition: CursorPosition | undefined;
	let cursorWasShown = false;

	const getActiveCursor = () => (cursorDirty ? cursorPosition : undefined);
	const hasChanges = (
		str: string,
		activeCursor: CursorPosition | undefined,
	): boolean => {
		const cursorChanged = cursorPositionChanged(
			activeCursor,
			previousCursorPosition,
		);
		return str !== previousOutput || cursorChanged;
	};

	const render = (str: string) => {
		if (!showCursor && !hasHiddenCursor) {
			cliCursor.hide(stream);
			hasHiddenCursor = true;
		}

		// Only use cursor if setCursorPosition was called since last render.
		// This ensures stale positions don't persist after component unmount.
		const activeCursor = getActiveCursor();
		cursorDirty = false;
		const cursorChanged = cursorPositionChanged(
			activeCursor,
			previousCursorPosition,
		);

		if (!hasChanges(str, activeCursor)) {
			return false;
		}

		const nextLines = str.split('\n');
		const visibleCount = visibleLineCount(nextLines, str);
		const previousVisible = visibleLineCount(previousLines, previousOutput);

		if (str === previousOutput && cursorChanged) {
			stream.write(
				buildCursorOnlySequence({
					cursorWasShown,
					previousLineCount: previousLines.length,
					previousCursorPosition,
					cursorPosition: activeCursor,
				}),
			);
			previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
			cursorWasShown = activeCursor !== undefined;
			return true;
		}

		const returnPrefix = buildReturnToBottomPrefix(
			cursorWasShown,
			previousLines.length,
			previousCursorPosition,
		);

		if (str === '\n' || previousOutput.length === 0) {
			const cursorSuffix = buildCursorSuffix(
				nextLines.length - 1,
				activeCursor,
			);
			stream.write(
				returnPrefix +
					ansiEscapes.eraseLines(previousLines.length) +
					str +
					cursorSuffix,
			);
			cursorWasShown = activeCursor !== undefined;
			previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
			previousOutput = str;
			previousLines = nextLines;
			return true;
		}

		const hasTrailingNewline = str.endsWith('\n');

		// We aggregate all chunks for incremental rendering into a buffer, and then write them to stdout at the end.
		const buffer: string[] = [];

		buffer.push(returnPrefix);

		// Clear extra lines if the current content's line count is lower than the previous.
		if (visibleCount < previousVisible) {
			const previousHadTrailingNewline = previousOutput.endsWith('\n');
			const extraSlot = previousHadTrailingNewline ? 1 : 0;
			buffer.push(
				ansiEscapes.eraseLines(previousVisible - visibleCount + extraSlot),
				ansiEscapes.cursorUp(visibleCount),
			);
		} else {
			buffer.push(ansiEscapes.cursorUp(previousLines.length - 1));
		}

		for (let i = 0; i < visibleCount; i++) {
			const isLastLine = i === visibleCount - 1;

			// We do not write lines if the contents are the same. This prevents flickering during renders.
			if (nextLines[i] === previousLines[i]) {
				// Don't move past the last line when there's no trailing newline,
				// otherwise the cursor overshoots the rendered block.
				if (!isLastLine || hasTrailingNewline) {
					buffer.push(ansiEscapes.cursorNextLine);
				}

				continue;
			}

			buffer.push(
				ansiEscapes.cursorTo(0) +
					nextLines[i] +
					ansiEscapes.eraseEndLine +
					// Don't append newline after the last line when the input
					// has no trailing newline (fullscreen mode).
					(isLastLine && !hasTrailingNewline ? '' : '\n'),
			);
		}

		const cursorSuffix = buildCursorSuffix(nextLines.length - 1, activeCursor);
		buffer.push(cursorSuffix);

		stream.write(buffer.join(''));

		cursorWasShown = activeCursor !== undefined;
		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		previousOutput = str;
		previousLines = nextLines;
		return true;
	};

	render.clear = () => {
		const prefix = buildReturnToBottomPrefix(
			cursorWasShown,
			previousLines.length,
			previousCursorPosition,
		);
		stream.write(prefix + ansiEscapes.eraseLines(previousLines.length));
		previousOutput = '';
		previousLines = [];
		previousCursorPosition = undefined;
		cursorWasShown = false;
	};

	render.done = () => {
		previousOutput = '';
		previousLines = [];
		previousCursorPosition = undefined;
		cursorWasShown = false;

		if (!showCursor) {
			cliCursor.show(stream);
			hasHiddenCursor = false;
		}
	};

	render.reset = () => {
		previousOutput = '';
		previousLines = [];
		previousCursorPosition = undefined;
		cursorWasShown = false;
	};

	render.sync = (str: string) => {
		const activeCursor = cursorDirty ? cursorPosition : undefined;
		cursorDirty = false;

		const lines = str.split('\n');
		previousOutput = str;
		previousLines = lines;

		if (!activeCursor && cursorWasShown) {
			stream.write(hideCursorEscape);
		}

		if (activeCursor) {
			stream.write(buildCursorSuffix(lines.length - 1, activeCursor));
		}

		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		cursorWasShown = activeCursor !== undefined;
	};

	render.setCursorPosition = (position: CursorPosition | undefined) => {
		cursorPosition = position;
		cursorDirty = true;
	};

	render.isCursorDirty = () => cursorDirty;
	render.willRender = (str: string) => hasChanges(str, getActiveCursor());

	return render;
}
```

### 🔹 函式: `render()`
- **變更前簽章 (Before)**: `render(str: string)` (L198~L310)
- **變更後簽章 (After)**: `render(str: string)` (L194~L308)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(str: string) => {
		if (!showCursor && !hasHiddenCursor) {
			cliCursor.hide(stream);
			hasHiddenCursor = true;
		}

		// Only use cursor if setCursorPosition was called since last render.
		// This ensures stale positions don't persist after component unmount.
		const activeCursor = getActiveCursor();
		cursorDirty = false;
		const cursorChanged = cursorPositionChanged(
			activeCursor,
			previousCursorPosition,
		);

		if (!hasChanges(str, activeCursor)) {
			return false;
		}

		const nextLines = str.split('\n');
		const visibleCount = visibleLineCount(nextLines, str);
		const previousVisible = visibleLineCount(previousLines, previousOutput);

		if (str === previousOutput && cursorChanged) {
			stream.write(
				buildCursorOnlySequence({
					cursorWasShown,
					previousLineCount: previousLines.length,
					previousCursorPosition,
					visibleLineCount: visibleCount,
					cursorPosition: activeCursor,
				}),
			);
			previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
			cursorWasShown = activeCursor !== undefined;
			return true;
		}

		const returnPrefix = buildReturnToBottomPrefix(
			cursorWasShown,
			previousLines.length,
			previousCursorPosition,
		);

		if (str === '\n' || previousOutput.length === 0) {
			const cursorSuffix = buildCursorSuffix(visibleCount, activeCursor);
			stream.write(
				returnPrefix +
					ansiEscapes.eraseLines(previousLines.length) +
					str +
					cursorSuffix,
			);
			cursorWasShown = activeCursor !== undefined;
			previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
			previousOutput = str;
			previousLines = nextLines;
			return true;
		}

		const hasTrailingNewline = str.endsWith('\n');

		// We aggregate all chunks for incremental rendering into a buffer, and then write them to stdout at the end.
		const buffer: string[] = [];

		buffer.push(returnPrefix);

		// Clear extra lines if the current content's line count is lower than the previous.
		if (visibleCount < previousVisible) {
			const previousHadTrailingNewline = previousOutput.endsWith('\n');
			const extraSlot = previousHadTrailingNewline ? 1 : 0;
			buffer.push(
				ansiEscapes.eraseLines(previousVisible - visibleCount + extraSlot),
				ansiEscapes.cursorUp(visibleCount),
			);
		} else {
			buffer.push(ansiEscapes.cursorUp(previousLines.length - 1));
		}

		for (let i = 0; i < visibleCount; i++) {
			const isLastLine = i === visibleCount - 1;

			// We do not write lines if the contents are the same. This prevents flickering during renders.
			if (nextLines[i] === previousLines[i]) {
				// Don't move past the last line when there's no trailing newline,
				// otherwise the cursor overshoots the rendered block.
				if (!isLastLine || hasTrailingNewline) {
					buffer.push(ansiEscapes.cursorNextLine);
				}

				continue;
			}

			buffer.push(
				ansiEscapes.cursorTo(0) +
					nextLines[i] +
					ansiEscapes.eraseEndLine +
					// Don't append newline after the last line when the input
					// has no trailing newline (fullscreen mode).
					(isLastLine && !hasTrailingNewline ? '' : '\n'),
			);
		}

		const cursorSuffix = buildCursorSuffix(visibleCount, activeCursor);
		buffer.push(cursorSuffix);

		stream.write(buffer.join(''));

		cursorWasShown = activeCursor !== undefined;
		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		previousOutput = str;
		previousLines = nextLines;
		return true;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(str: string) => {
		if (!showCursor && !hasHiddenCursor) {
			cliCursor.hide(stream);
			hasHiddenCursor = true;
		}

		// Only use cursor if setCursorPosition was called since last render.
		// This ensures stale positions don't persist after component unmount.
		const activeCursor = getActiveCursor();
		cursorDirty = false;
		const cursorChanged = cursorPositionChanged(
			activeCursor,
			previousCursorPosition,
		);

		if (!hasChanges(str, activeCursor)) {
			return false;
		}

		const nextLines = str.split('\n');
		const visibleCount = visibleLineCount(nextLines, str);
		const previousVisible = visibleLineCount(previousLines, previousOutput);

		if (str === previousOutput && cursorChanged) {
			stream.write(
				buildCursorOnlySequence({
					cursorWasShown,
					previousLineCount: previousLines.length,
					previousCursorPosition,
					cursorPosition: activeCursor,
				}),
			);
			previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
			cursorWasShown = activeCursor !== undefined;
			return true;
		}

		const returnPrefix = buildReturnToBottomPrefix(
			cursorWasShown,
			previousLines.length,
			previousCursorPosition,
		);

		if (str === '\n' || previousOutput.length === 0) {
			const cursorSuffix = buildCursorSuffix(
				nextLines.length - 1,
				activeCursor,
			);
			stream.write(
				returnPrefix +
					ansiEscapes.eraseLines(previousLines.length) +
					str +
					cursorSuffix,
			);
			cursorWasShown = activeCursor !== undefined;
			previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
			previousOutput = str;
			previousLines = nextLines;
			return true;
		}

		const hasTrailingNewline = str.endsWith('\n');

		// We aggregate all chunks for incremental rendering into a buffer, and then write them to stdout at the end.
		const buffer: string[] = [];

		buffer.push(returnPrefix);

		// Clear extra lines if the current content's line count is lower than the previous.
		if (visibleCount < previousVisible) {
			const previousHadTrailingNewline = previousOutput.endsWith('\n');
			const extraSlot = previousHadTrailingNewline ? 1 : 0;
			buffer.push(
				ansiEscapes.eraseLines(previousVisible - visibleCount + extraSlot),
				ansiEscapes.cursorUp(visibleCount),
			);
		} else {
			buffer.push(ansiEscapes.cursorUp(previousLines.length - 1));
		}

		for (let i = 0; i < visibleCount; i++) {
			const isLastLine = i === visibleCount - 1;

			// We do not write lines if the contents are the same. This prevents flickering during renders.
			if (nextLines[i] === previousLines[i]) {
				// Don't move past the last line when there's no trailing newline,
				// otherwise the cursor overshoots the rendered block.
				if (!isLastLine || hasTrailingNewline) {
					buffer.push(ansiEscapes.cursorNextLine);
				}

				continue;
			}

			buffer.push(
				ansiEscapes.cursorTo(0) +
					nextLines[i] +
					ansiEscapes.eraseEndLine +
					// Don't append newline after the last line when the input
					// has no trailing newline (fullscreen mode).
					(isLastLine && !hasTrailingNewline ? '' : '\n'),
			);
		}

		const cursorSuffix = buildCursorSuffix(nextLines.length - 1, activeCursor);
		buffer.push(cursorSuffix);

		stream.write(buffer.join(''));

		cursorWasShown = activeCursor !== undefined;
		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		previousOutput = str;
		previousLines = nextLines;
		return true;
	}
```

### 🔹 函式: `sync()`
- **變更前簽章 (Before)**: `sync(str: string)` (L344~L364)
- **變更後簽章 (After)**: `sync(str: string)` (L342~L360)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(str: string) => {
		const activeCursor = cursorDirty ? cursorPosition : undefined;
		cursorDirty = false;

		const lines = str.split('\n');
		previousOutput = str;
		previousLines = lines;

		if (!activeCursor && cursorWasShown) {
			stream.write(hideCursorEscape);
		}

		if (activeCursor) {
			stream.write(
				buildCursorSuffix(visibleLineCount(lines, str), activeCursor),
			);
		}

		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		cursorWasShown = activeCursor !== undefined;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(str: string) => {
		const activeCursor = cursorDirty ? cursorPosition : undefined;
		cursorDirty = false;

		const lines = str.split('\n');
		previousOutput = str;
		previousLines = lines;

		if (!activeCursor && cursorWasShown) {
			stream.write(hideCursorEscape);
		}

		if (activeCursor) {
			stream.write(buildCursorSuffix(lines.length - 1, activeCursor));
		}

		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		cursorWasShown = activeCursor !== undefined;
	}
```

### 🔹 函式: `sync()`
- **變更前簽章 (Before)**: `sync(str: string)` (L141~L161)
- **變更後簽章 (After)**: `sync(str: string)` (L139~L157)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(str: string) => {
		const activeCursor = cursorDirty ? cursorPosition : undefined;
		cursorDirty = false;

		const lines = str.split('\n');
		previousOutput = str;
		previousLineCount = lines.length;

		if (!activeCursor && cursorWasShown) {
			stream.write(hideCursorEscape);
		}

		if (activeCursor) {
			stream.write(
				buildCursorSuffix(visibleLineCount(lines, str), activeCursor),
			);
		}

		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		cursorWasShown = activeCursor !== undefined;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(str: string) => {
		const activeCursor = cursorDirty ? cursorPosition : undefined;
		cursorDirty = false;

		const lines = str.split('\n');
		previousOutput = str;
		previousLineCount = lines.length;

		if (!activeCursor && cursorWasShown) {
			stream.write(hideCursorEscape);
		}

		if (activeCursor) {
			stream.write(buildCursorSuffix(lines.length - 1, activeCursor));
		}

		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		cursorWasShown = activeCursor !== undefined;
	}
```

### 🔹 函式: `render()`
- **變更前簽章 (Before)**: `render(str: string)` (L55~L107)
- **變更後簽章 (After)**: `render(str: string)` (L55~L105)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(str: string) => {
		if (!showCursor && !hasHiddenCursor) {
			cliCursor.hide(stream);
			hasHiddenCursor = true;
		}

		// Only use cursor if setCursorPosition was called since last render.
		// This ensures stale positions don't persist after component unmount.
		const activeCursor = getActiveCursor();
		cursorDirty = false;
		const cursorChanged = cursorPositionChanged(
			activeCursor,
			previousCursorPosition,
		);

		if (!hasChanges(str, activeCursor)) {
			return false;
		}

		const lines = str.split('\n');
		const visibleCount = visibleLineCount(lines, str);
		const cursorSuffix = buildCursorSuffix(visibleCount, activeCursor);

		if (str === previousOutput && cursorChanged) {
			stream.write(
				buildCursorOnlySequence({
					cursorWasShown,
					previousLineCount,
					previousCursorPosition,
					visibleLineCount: visibleCount,
					cursorPosition: activeCursor,
				}),
			);
		} else {
			previousOutput = str;
			const returnPrefix = buildReturnToBottomPrefix(
				cursorWasShown,
				previousLineCount,
				previousCursorPosition,
			);
			stream.write(
				returnPrefix +
					ansiEscapes.eraseLines(previousLineCount) +
					str +
					cursorSuffix,
			);
			previousLineCount = lines.length;
		}

		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		cursorWasShown = activeCursor !== undefined;
		return true;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(str: string) => {
		if (!showCursor && !hasHiddenCursor) {
			cliCursor.hide(stream);
			hasHiddenCursor = true;
		}

		// Only use cursor if setCursorPosition was called since last render.
		// This ensures stale positions don't persist after component unmount.
		const activeCursor = getActiveCursor();
		cursorDirty = false;
		const cursorChanged = cursorPositionChanged(
			activeCursor,
			previousCursorPosition,
		);

		if (!hasChanges(str, activeCursor)) {
			return false;
		}

		const lines = str.split('\n');
		const cursorSuffix = buildCursorSuffix(lines.length - 1, activeCursor);

		if (str === previousOutput && cursorChanged) {
			stream.write(
				buildCursorOnlySequence({
					cursorWasShown,
					previousLineCount,
					previousCursorPosition,
					cursorPosition: activeCursor,
				}),
			);
		} else {
			previousOutput = str;
			const returnPrefix = buildReturnToBottomPrefix(
				cursorWasShown,
				previousLineCount,
				previousCursorPosition,
			);
			stream.write(
				returnPrefix +
					ansiEscapes.eraseLines(previousLineCount) +
					str +
					cursorSuffix,
			);
			previousLineCount = lines.length;
		}

		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		cursorWasShown = activeCursor !== undefined;
		return true;
	}
```

### 🔹 函式: `createStandard()`
- **變更前簽章 (Before)**: `createStandard(
	stream: Writable,
	{showCursor = false} = {},
)` (L31~L172)
- **變更後簽章 (After)**: `createStandard(
	stream: Writable,
	{showCursor = false} = {},
)` (L31~L168)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(
	stream: Writable,
	{showCursor = false} = {},
): LogUpdate => {
	let previousLineCount = 0;
	let previousOutput = '';
	let hasHiddenCursor = false;
	let cursorPosition: CursorPosition | undefined;
	let cursorDirty = false;
	let previousCursorPosition: CursorPosition | undefined;
	let cursorWasShown = false;

	const getActiveCursor = () => (cursorDirty ? cursorPosition : undefined);
	const hasChanges = (
		str: string,
		activeCursor: CursorPosition | undefined,
	): boolean => {
		const cursorChanged = cursorPositionChanged(
			activeCursor,
			previousCursorPosition,
		);
		return str !== previousOutput || cursorChanged;
	};

	const render = (str: string) => {
		if (!showCursor && !hasHiddenCursor) {
			cliCursor.hide(stream);
			hasHiddenCursor = true;
		}

		// Only use cursor if setCursorPosition was called since last render.
		// This ensures stale positions don't persist after component unmount.
		const activeCursor = getActiveCursor();
		cursorDirty = false;
		const cursorChanged = cursorPositionChanged(
			activeCursor,
			previousCursorPosition,
		);

		if (!hasChanges(str, activeCursor)) {
			return false;
		}

		const lines = str.split('\n');
		const visibleCount = visibleLineCount(lines, str);
		const cursorSuffix = buildCursorSuffix(visibleCount, activeCursor);

		if (str === previousOutput && cursorChanged) {
			stream.write(
				buildCursorOnlySequence({
					cursorWasShown,
					previousLineCount,
					previousCursorPosition,
					visibleLineCount: visibleCount,
					cursorPosition: activeCursor,
				}),
			);
		} else {
			previousOutput = str;
			const returnPrefix = buildReturnToBottomPrefix(
				cursorWasShown,
				previousLineCount,
				previousCursorPosition,
			);
			stream.write(
				returnPrefix +
					ansiEscapes.eraseLines(previousLineCount) +
					str +
					cursorSuffix,
			);
			previousLineCount = lines.length;
		}

		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		cursorWasShown = activeCursor !== undefined;
		return true;
	};

	render.clear = () => {
		const prefix = buildReturnToBottomPrefix(
			cursorWasShown,
			previousLineCount,
			previousCursorPosition,
		);
		stream.write(prefix + ansiEscapes.eraseLines(previousLineCount));
		previousOutput = '';
		previousLineCount = 0;
		previousCursorPosition = undefined;
		cursorWasShown = false;
	};

	render.done = () => {
		previousOutput = '';
		previousLineCount = 0;
		previousCursorPosition = undefined;
		cursorWasShown = false;

		if (!showCursor) {
			cliCursor.show(stream);
			hasHiddenCursor = false;
		}
	};

	render.reset = () => {
		previousOutput = '';
		previousLineCount = 0;
		previousCursorPosition = undefined;
		cursorWasShown = false;
	};

	render.sync = (str: string) => {
		const activeCursor = cursorDirty ? cursorPosition : undefined;
		cursorDirty = false;

		const lines = str.split('\n');
		previousOutput = str;
		previousLineCount = lines.length;

		if (!activeCursor && cursorWasShown) {
			stream.write(hideCursorEscape);
		}

		if (activeCursor) {
			stream.write(
				buildCursorSuffix(visibleLineCount(lines, str), activeCursor),
			);
		}

		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		cursorWasShown = activeCursor !== undefined;
	};

	render.setCursorPosition = (position: CursorPosition | undefined) => {
		cursorPosition = position;
		cursorDirty = true;
	};

	render.isCursorDirty = () => cursorDirty;
	render.willRender = (str: string) => hasChanges(str, getActiveCursor());

	return render;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(
	stream: Writable,
	{showCursor = false} = {},
): LogUpdate => {
	let previousLineCount = 0;
	let previousOutput = '';
	let hasHiddenCursor = false;
	let cursorPosition: CursorPosition | undefined;
	let cursorDirty = false;
	let previousCursorPosition: CursorPosition | undefined;
	let cursorWasShown = false;

	const getActiveCursor = () => (cursorDirty ? cursorPosition : undefined);
	const hasChanges = (
		str: string,
		activeCursor: CursorPosition | undefined,
	): boolean => {
		const cursorChanged = cursorPositionChanged(
			activeCursor,
			previousCursorPosition,
		);
		return str !== previousOutput || cursorChanged;
	};

	const render = (str: string) => {
		if (!showCursor && !hasHiddenCursor) {
			cliCursor.hide(stream);
			hasHiddenCursor = true;
		}

		// Only use cursor if setCursorPosition was called since last render.
		// This ensures stale positions don't persist after component unmount.
		const activeCursor = getActiveCursor();
		cursorDirty = false;
		const cursorChanged = cursorPositionChanged(
			activeCursor,
			previousCursorPosition,
		);

		if (!hasChanges(str, activeCursor)) {
			return false;
		}

		const lines = str.split('\n');
		const cursorSuffix = buildCursorSuffix(lines.length - 1, activeCursor);

		if (str === previousOutput && cursorChanged) {
			stream.write(
				buildCursorOnlySequence({
					cursorWasShown,
					previousLineCount,
					previousCursorPosition,
					cursorPosition: activeCursor,
				}),
			);
		} else {
			previousOutput = str;
			const returnPrefix = buildReturnToBottomPrefix(
				cursorWasShown,
				previousLineCount,
				previousCursorPosition,
			);
			stream.write(
				returnPrefix +
					ansiEscapes.eraseLines(previousLineCount) +
					str +
					cursorSuffix,
			);
			previousLineCount = lines.length;
		}

		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		cursorWasShown = activeCursor !== undefined;
		return true;
	};

	render.clear = () => {
		const prefix = buildReturnToBottomPrefix(
			cursorWasShown,
			previousLineCount,
			previousCursorPosition,
		);
		stream.write(prefix + ansiEscapes.eraseLines(previousLineCount));
		previousOutput = '';
		previousLineCount = 0;
		previousCursorPosition = undefined;
		cursorWasShown = false;
	};

	render.done = () => {
		previousOutput = '';
		previousLineCount = 0;
		previousCursorPosition = undefined;
		cursorWasShown = false;

		if (!showCursor) {
			cliCursor.show(stream);
			hasHiddenCursor = false;
		}
	};

	render.reset = () => {
		previousOutput = '';
		previousLineCount = 0;
		previousCursorPosition = undefined;
		cursorWasShown = false;
	};

	render.sync = (str: string) => {
		const activeCursor = cursorDirty ? cursorPosition : undefined;
		cursorDirty = false;

		const lines = str.split('\n');
		previousOutput = str;
		previousLineCount = lines.length;

		if (!activeCursor && cursorWasShown) {
			stream.write(hideCursorEscape);
		}

		if (activeCursor) {
			stream.write(buildCursorSuffix(lines.length - 1, activeCursor));
		}

		previousCursorPosition = activeCursor ? {...activeCursor} : undefined;
		cursorWasShown = activeCursor !== undefined;
	};

	render.setCursorPosition = (position: CursorPosition | undefined) => {
		cursorPosition = position;
		cursorDirty = true;
	};

	render.isCursorDirty = () => cursorDirty;
	render.willRender = (str: string) => hasChanges(str, getActiveCursor());

	return render;
}
```


---

### 🔹 Commit #20: `5448e6b4`
- **完整 Hash**: `5448e6b4014c10318224999f9b719423a5e80c47`
- **說明 (Ground Truth)**: Fix dangling `staticNode` reference on indirect subtree removal (#979)
- **變更檔案數**: 3

#### 📄 檔案: `src/dom.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:18, E:14, A:0) ➔ After(N:20, E:16, A:0)
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
  • + [新增節點] `nullifyYogaNodes` (FUNCTION_DEF)
  • + [新增節點] `freeYogaSubtree` (FUNCTION_DEF)
  • + [新增呼叫邊] `nullifyYogaNodes` ──[CALLS [guard: (node.nodeName !== '#text')]]──> `nullifyYogaNodes`
  • + [新增呼叫邊] `freeYogaSubtree` ──[CALLS]──> `nullifyYogaNodes`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `src/reconciler.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:57, E:17, A:0) ➔ After(N:59, E:22, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 1, +Edges: 7, -Edges: 2, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `clearStaticNodeIfContained` (FUNCTION_DEF)
  • + [新增節點] `freeYogaSubtree (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `findRootNode` (FUNCTION_DEF)
  • - [移除節點] `cleanupYogaNode` (FUNCTION_DEF)
  • + [新增呼叫邊] `removeChildFromContainer` ──[CALLS]──> `clearStaticNodeIfContained`
  • + [新增呼叫邊] `removeChildFromContainer` ──[CALLS]──> `findRootNode`
  • + [新增呼叫邊] `removeChildFromContainer` ──[CALLS]──> `freeYogaSubtree (External/Unresolved)`
  • + [新增呼叫邊] `commitUpdate` ──[CALLS [guard: (node.internal_static)]]──> `findRootNode`
  • + [新增呼叫邊] `removeChild` ──[CALLS]──> `clearStaticNodeIfContained`
  • + [新增呼叫邊] `removeChild` ──[CALLS]──> `findRootNode`
  • + [新增呼叫邊] `removeChild` ──[CALLS]──> `freeYogaSubtree (External/Unresolved)`
  • - [移除呼叫邊] `removeChildFromContainer` ──[CALLS]──> `cleanupYogaNode`
  • - [移除呼叫邊] `removeChild` ──[CALLS]──> `cleanupYogaNode`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `commitUpdate()`
- **變更前簽章 (Before)**: `commitUpdate(node, _type, oldProps, newProps)` (L316~L360)
- **變更後簽章 (After)**: `commitUpdate(node, _type, oldProps, newProps)` (L357~L405)

#### ◀️ 變更前實作碼 (Before Implementation):
```
commitUpdate(node, _type, oldProps, newProps) {
		if (currentRootNode && node.internal_static) {
			currentRootNode.isStaticDirty = true;
		}

		const props = diff(oldProps, newProps);

		const style = diff(
			oldProps['style'] as Styles,
			newProps['style'] as Styles,
		);

		if (!props && !style) {
			return;
		}

		if (props) {
			for (const [key, value] of Object.entries(props)) {
				if (key === 'style') {
					setStyle(node, value as Styles);
					continue;
				}

				if (key === 'internal_transform') {
					node.internal_transform = value as OutputTransformer;
					continue;
				}

				if (key === 'internal_static') {
					node.internal_static = true;
					continue;
				}

				setAttribute(node, key, value as DOMNodeAttribute);
			}
		}

		if (style && node.yogaNode) {
			applyStyles(
				node.yogaNode,
				style,
				(newProps['style'] as Styles | undefined) ?? {},
			);
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
commitUpdate(node, _type, oldProps, newProps) {
		if (node.internal_static) {
			const rootNode = findRootNode(node);

			if (rootNode) {
				rootNode.isStaticDirty = true;
			}
		}

		const props = diff(oldProps, newProps);

		const style = diff(
			oldProps['style'] as Styles,
			newProps['style'] as Styles,
		);

		if (!props && !style) {
			return;
		}

		if (props) {
			for (const [key, value] of Object.entries(props)) {
				if (key === 'style') {
					setStyle(node, value as Styles);
					continue;
				}

				if (key === 'internal_transform') {
					node.internal_transform = value as OutputTransformer;
					continue;
				}

				if (key === 'internal_static') {
					node.internal_static = true;
					continue;
				}

				setAttribute(node, key, value as DOMNodeAttribute);
			}
		}

		if (style && node.yogaNode) {
			applyStyles(
				node.yogaNode,
				style,
				(newProps['style'] as Styles | undefined) ?? {},
			);
		}
	}
```

### 🔹 函式: `removeChild()`
- **變更前簽章 (Before)**: `removeChild(node, removeNode)` (L364~L375)
- **變更後簽章 (After)**: `removeChild(node, removeNode)` (L409~L416)

#### ◀️ 變更前實作碼 (Before Implementation):
```
removeChild(node, removeNode) {
		removeChildNode(node, removeNode);
		cleanupYogaNode(removeNode.yogaNode);

		// Same guard as removeChildFromContainer: only clear if this is still the active static node.
		if (
			removeNode.internal_static &&
			currentRootNode?.staticNode === removeNode
		) {
			currentRootNode.staticNode = undefined;
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
removeChild(node, removeNode) {
		// `node` is the host parent; its chain up to the root is still intact
		// here, so derive the owning root from it rather than a global.
		clearStaticNodeIfContained(findRootNode(node), removeNode);

		removeChildNode(node, removeNode);
		freeYogaSubtree(removeNode);
	}
```

### 🔹 函式: `removeChildFromContainer()`
- **變更前簽章 (Before)**: `removeChildFromContainer(node, removeNode)` (L304~L315)
- **變更後簽章 (After)**: `removeChildFromContainer(node, removeNode)` (L349~L356)

#### ◀️ 變更前實作碼 (Before Implementation):
```
removeChildFromContainer(node, removeNode) {
		removeChildNode(node, removeNode);
		cleanupYogaNode(removeNode.yogaNode);

		// Only clear staticNode if it still points at the removed node. On key-driven remounts, `createInstance` already registered the new node before this removal fires.
		if (
			removeNode.internal_static &&
			currentRootNode?.staticNode === removeNode
		) {
			currentRootNode.staticNode = undefined;
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
removeChildFromContainer(node, removeNode) {
		// `node` is the container, i.e. the root itself. Clear before
		// removeChildNode breaks the parent chain.
		clearStaticNodeIfContained(findRootNode(node), removeNode);

		removeChildNode(node, removeNode);
		freeYogaSubtree(removeNode);
	}
```

### 🔹 函式: `createInstance()`
- **變更前簽章 (Before)**: `createInstance(originalType, newProps, rootNode, hostContext)` (L204~L251)
- **變更後簽章 (After)**: `createInstance(originalType, newProps, rootNode, hostContext)` (L250~L296)

#### ◀️ 變更前實作碼 (Before Implementation):
```
createInstance(originalType, newProps, rootNode, hostContext) {
		if (hostContext.isInsideText && originalType === 'ink-box') {
			throw new Error(`<Box> can’t be nested inside <Text> component`);
		}

		const type =
			originalType === 'ink-text' && hostContext.isInsideText
				? 'ink-virtual-text'
				: originalType;

		const node = createNode(type);

		for (const [key, value] of Object.entries(newProps)) {
			if (key === 'children') {
				continue;
			}

			if (key === 'style') {
				setStyle(node, value as Styles);

				if (node.yogaNode) {
					applyStyles(node.yogaNode, value as Styles);
				}

				continue;
			}

			if (key === 'internal_transform') {
				node.internal_transform = value as OutputTransformer;
				continue;
			}

			if (key === 'internal_static') {
				currentRootNode = rootNode;
				node.internal_static = true;
				rootNode.isStaticDirty = true;

				// Save reference to <Static> node to skip traversal of entire
				// node tree to find it
				rootNode.staticNode = node;
				continue;
			}

			setAttribute(node, key, value as DOMNodeAttribute);
		}

		return node;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
createInstance(originalType, newProps, rootNode, hostContext) {
		if (hostContext.isInsideText && originalType === 'ink-box') {
			throw new Error(`<Box> can’t be nested inside <Text> component`);
		}

		const type =
			originalType === 'ink-text' && hostContext.isInsideText
				? 'ink-virtual-text'
				: originalType;

		const node = createNode(type);

		for (const [key, value] of Object.entries(newProps)) {
			if (key === 'children') {
				continue;
			}

			if (key === 'style') {
				setStyle(node, value as Styles);

				if (node.yogaNode) {
					applyStyles(node.yogaNode, value as Styles);
				}

				continue;
			}

			if (key === 'internal_transform') {
				node.internal_transform = value as OutputTransformer;
				continue;
			}

			if (key === 'internal_static') {
				node.internal_static = true;
				rootNode.isStaticDirty = true;

				// Save reference to <Static> node to skip traversal of entire
				// node tree to find it
				rootNode.staticNode = node;
				continue;
			}

			setAttribute(node, key, value as DOMNodeAttribute);
		}

		return node;
	}
```


#### 📄 檔案: `src/render-to-string.ts`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:10, E:4, A:0) ➔ After(N:10, E:4, A:0)
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

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/ink show 13707d2df9ea722d15f0d2de5790ddbf1054dea1
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 13707d2df9ea722d15f0d2de5790ddbf1054dea1~1 --file test_repos/ink/src/input-parser.ts
   ```
