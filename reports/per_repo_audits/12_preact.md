# 🔬 CODE-Map 基準審查獨立驗證報告: `preact`
> **技術生態**: `JavaScript (極致輕量 Virtual DOM / Hooks)`  
> **本地倉庫路徑**: `test_repos/preact`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 30 Files  
> **報告生成時間**: 2026-10-20 21:41:26  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `6` / `30` | `20.0%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `22` / `30` | `73.3%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `2` / `30` | `6.7%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`28` / `30`** | **`93.3%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `30` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `a9dc9b01`
- **完整 Hash**: `a9dc9b01073f2d9040e2fd45216bf296ec10ace0`
- **說明 (Ground Truth)**: Reduce core diff bundle size
- **變更檔案數**: 3

#### 📄 檔案: `src/diff/children.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:12, E:14, A:0) ➔ After(N:12, E:14, A:0)
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

### 🔹 函式: `constructNewChildrenArray()`
- **變更前簽章 (Before)**: `function constructNewChildrenArray(
	newParentVNode,
	renderResult,
	oldChildren,
	oldDom,
	newChildrenLength
)` (L159~L375)
- **變更後簽章 (After)**: `function constructNewChildrenArray(
	newParentVNode,
	renderResult,
	oldChildren,
	oldDom,
	newChildrenLength
)` (L159~L375)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function constructNewChildrenArray(
	newParentVNode,
	renderResult,
	oldChildren,
	oldDom,
	newChildrenLength
) {
	/** @type {number} */
	let i;
	/** @type {VNode} */
	let childVNode;
	/** @type {VNode} */
	let oldVNode;

	let oldChildrenLength = oldChildren.length,
		remainingOldChildren = oldChildrenLength;

	let skew = 0;

	/** Whether any matched child was found far from its skewed index, i.e. a
	 * real reorder happened and we need to compute the minimal set of moves. */
	let moved = false;

	// Hoisted: every normalization branch below writes through this array, so
	// reading `_children` off the vnode each time is a wasted property load.
	/** @type {VNode[]} */
	let newChildren = (newParentVNode._children = Array(newChildrenLength));
	for (i = 0; i < newChildrenLength; i++) {
		// @ts-expect-error We are reusing the childVNode variable to hold both the
		// pre and post normalized childVNode
		childVNode = renderResult[i];

		if (
			childVNode == NULL ||
			typeof childVNode == 'boolean' ||
			typeof childVNode == 'function'
		) {
			newChildren[i] = NULL;
			continue;
		}
		// If this newVNode is being reused (e.g. <div>{reuse}{reuse}</div>) in the same diff,
		// or we are rendering a component (e.g. setState) copy the oldVNodes so it can have
		// it's own DOM & etc. pointers
		// Anything that isn't an object at this point is a string, number or
		// bigint (null, booleans and functions are handled above), String
		// objects are the lone object type rendered as text.
		else if (
			typeof childVNode != 'object' ||
			childVNode.constructor == String
		) {
			childVNode = newChildren[i] = createVNode(NULL, childVNode);
		} else if (isArray(childVNode)) {
			childVNode = newChildren[i] = createVNode(Fragment, {
				children: childVNode
			});
		} else if (childVNode.constructor === UNDEFINED && childVNode._depth) {
			// VNode is already in use, clone it. This can happen in the following
			// scenario:
			//   const reuse = <div />
			//   <div>{reuse}<span />{reuse}</div>
			childVNode = newChildren[i] = createVNode(
				childVNode.type,
				childVNode.props,
				childVNode.key,
				childVNode.ref,
				childVNode._original
			);
		} else {
			newChildren[i] = childVNode;
		}

		const skewedIndex = i + skew;
		childVNode._parent = newParentVNode;
		childVNode._depth = newParentVNode._depth + 1;

		// Temporarily store the matchingIndex on the _index property so we can pull
		// out the oldVNode in diffChildren. We'll override this to the VNode's
		// final index after using this property to get the oldVNode
		const matchingIndex = (childVNode._index = findMatchingIndex(
			childVNode,
			oldChildren,
			skewedIndex,
			remainingOldChildren
		));

		oldVNode = NULL;
		// ~matchingIndex is only falsy for -1, i.e. when no match was found
		if (~matchingIndex) {
			oldVNode = oldChildren[matchingIndex];
			remainingOldChildren--;
			if (oldVNode) {
				oldVNode._flags |= MATCHED;
			}
		}

		// Here, we define isMounting for the purposes of the skew diffing
		// algorithm. Nodes that are unsuspending are considered mounting and we detect
		// this by checking if oldVNode._original == null
		if (!oldVNode || !oldVNode._original) {
			if (!~matchingIndex) {
				// When the array of children is growing we need to decrease the skew
				// as we are adding a new element to the array.
				// Example:
				// [1, 2, 3] --> [0, 1, 2, 3]
				// oldChildren   newChildren
				//
				// The new element is at index 0, so our skew is 0,
				// we need to decrease the skew as we are adding a new element.
				// The decrease will cause us to compare the element at position 1
				// with value 1 with the element at position 0 with value 0.
				//
				// A linear concept is applied when the array is shrinking,
				// if the length is unchanged we can assume that no skew
				// changes are needed.
				if (newChildrenLength > oldChildrenLength) {
					skew--;
				} else if (newChildrenLength < oldChildrenLength) {
					skew++;
				}
			}

			// If we are mounting a DOM VNode, mark it for insertion
			if (typeof childVNode.type != 'function') {
				childVNode._flags |= INSERT_VNODE;
			}
		} else {
			// Matched children are candidates for the minimal-move pass below;
			// MATCHED on a _new_ vnode is cleared in diffChildren's placement loop.
			childVNode._flags |= MATCHED;

			// The skew adjustments keep findMatchingIndex's search centered for
			// shift patterns (insertions/removals at the front). A match further
			// than one position away means children were genuinely reordered:
			// flag it so the minimal set of moves is computed below. Off-by-one
			// matches provably keep matched old indices in increasing order, so
			// no moves are needed for them.
			if (matchingIndex == skewedIndex - 1) {
				skew--;
			} else if (matchingIndex == skewedIndex + 1) {
				skew++;
			} else if (matchingIndex != skewedIndex) {
				if (matchingIndex > skewedIndex) {
					skew--;
				} else {
					skew++;
				}

				moved = true;
			}
		}
	}

	if (moved) {
		// Children were reordered: mark the minimal set of matched (MATCHED flag)
		// children for insertion by finding the longest increasing subsequence of
		// old indices (patience sorting). Children on the subsequence stay in
		// place, all others get INSERT_VNODE. `_index` still holds the
		// matchingIndex here.
		/** @type {number[]} tails[x] is the smallest old index ending an increasing subsequence of length x+1 */
		let tails = [];
		/** @type {number[]} length of the longest increasing subsequence ending at child i */
		let lisLengths = [];
		for (i = 0; i < newChildrenLength; i++) {
			childVNode = newChildren[i];
			if (childVNode && childVNode._flags & MATCHED) {
				// Binary search for the insertion point, keeping the pass at
				// O(n log n) even for pathological reorders.
				let lo = 0,
					hi = tails.length;
				while (lo < hi) {
					const mid = (lo + hi) >> 1;
					if (tails[mid] < childVNode._index) {
						lo = mid + 1;
					} else {
						hi = mid;
					}
				}
				tails[lo] = childVNode._index;
				lisLengths[i] = lo + 1;
			}
		}

		// `skew` is dead after the main loop; reuse it as the remaining
		// subsequence length while walking backwards. Likewise `i` is left at
		// newChildrenLength by the loop above.
		skew = tails.length;
		while (i--) {
			if (lisLengths[i]) {
				if (lisLengths[i] == skew) {
					skew--;
				} else {
					newChildren[i]._flags |= INSERT_VNODE;
				}
			}
		}
	}

	// Remove remaining oldChildren if there are any. Loop forwards so that as we
	// unmount DOM from the beginning of the oldChildren, we can adjust oldDom to
	// point to the next child, which needs to be the first DOM node that won't be
	// unmounted. Keep this a plain loop: an arrow function here would capture
	// `oldDom`, forcing V8 to context-allocate it on every call to this function.
	if (remainingOldChildren) {
		for (i = 0; i < oldChildrenLength; i++) {
			oldVNode = oldChildren[i];
			if (oldVNode && !(oldVNode._flags & MATCHED)) {
				if (oldVNode._dom == oldDom) {
					oldDom = getDomSibling(oldVNode);
				}

				unmount(oldVNode, oldVNode);
			}
		}
	}

	return oldDom;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function constructNewChildrenArray(
	newParentVNode,
	renderResult,
	oldChildren,
	oldDom,
	newChildrenLength
) {
	/** @type {number} */
	let i;
	/** @type {VNode} */
	let childVNode;
	/** @type {VNode} */
	let oldVNode;

	let oldChildrenLength = oldChildren.length,
		remainingOldChildren = oldChildrenLength;

	let skew = 0;

	/** Whether any matched child was found far from its skewed index, i.e. a
	 * real reorder happened and we need to compute the minimal set of moves. */
	let moved = false;

	// Hoisted: every normalization branch below writes through this array, so
	// reading `_children` off the vnode each time is a wasted property load.
	/** @type {VNode[]} */
	let newChildren = (newParentVNode._children = Array(newChildrenLength));
	for (i = 0; i < newChildrenLength; i++) {
		// @ts-expect-error We are reusing the childVNode variable to hold both the
		// pre and post normalized childVNode
		childVNode = renderResult[i];

		if (
			childVNode == NULL ||
			typeof childVNode == 'boolean' ||
			typeof childVNode == 'function'
		) {
			newChildren[i] = NULL;
			continue;
		}
		// If this newVNode is being reused (e.g. <div>{reuse}{reuse}</div>) in the same diff,
		// or we are rendering a component (e.g. setState) copy the oldVNodes so it can have
		// it's own DOM & etc. pointers
		// Anything that isn't an object at this point is a string, number or
		// bigint (null, booleans and functions are handled above), String
		// objects are the lone object type rendered as text.
		else if (
			typeof childVNode != 'object' ||
			childVNode.constructor == String
		) {
			childVNode = newChildren[i] = createVNode(NULL, childVNode);
		} else if (isArray(childVNode)) {
			childVNode = newChildren[i] = createVNode(Fragment, {
				children: childVNode
			});
		} else if (childVNode.constructor === UNDEFINED && childVNode._depth) {
			// VNode is already in use, clone it. This can happen in the following
			// scenario:
			//   const reuse = <div />
			//   <div>{reuse}<span />{reuse}</div>
			childVNode = newChildren[i] = createVNode(
				childVNode.type,
				childVNode.props,
				childVNode.key,
				childVNode.ref,
				childVNode._original
			);
		} else {
			newChildren[i] = childVNode;
		}

		const skewedIndex = i + skew;
		childVNode._parent = newParentVNode;
		childVNode._depth = newParentVNode._depth + 1;

		// Temporarily store the matchingIndex on the _index property so we can pull
		// out the oldVNode in diffChildren. We'll override this to the VNode's
		// final index after using this property to get the oldVNode
		const matchingIndex = (childVNode._index = findMatchingIndex(
			childVNode,
			oldChildren,
			skewedIndex,
			remainingOldChildren
		));

		oldVNode = NULL;
		// ~matchingIndex is only falsy for -1, i.e. when no match was found
		if (~matchingIndex) {
			oldVNode = oldChildren[matchingIndex];
			remainingOldChildren--;
			if (oldVNode) {
				oldVNode._flags |= MATCHED;
			}
		}

		// Here, we define isMounting for the purposes of the skew diffing
		// algorithm. Nodes that are unsuspending are considered mounting and we detect
		// this by checking if oldVNode._original == null
		if (!oldVNode || !oldVNode._original) {
			if (!~matchingIndex) {
				// When the array of children is growing we need to decrease the skew
				// as we are adding a new element to the array.
				// Example:
				// [1, 2, 3] --> [0, 1, 2, 3]
				// oldChildren   newChildren
				//
				// The new element is at index 0, so our skew is 0,
				// we need to decrease the skew as we are adding a new element.
				// The decrease will cause us to compare the element at position 1
				// with value 1 with the element at position 0 with value 0.
				//
				// A linear concept is applied when the array is shrinking,
				// if the length is unchanged we can assume that no skew
				// changes are needed.
				if (newChildrenLength > oldChildrenLength) {
					skew--;
				} else if (newChildrenLength < oldChildrenLength) {
					skew++;
				}
			}

			// If we are mounting a DOM VNode, mark it for insertion
			if (typeof childVNode.type != 'function') {
				childVNode._flags |= INSERT_VNODE;
			}
		} else {
			// Matched children are candidates for the minimal-move pass below;
			// MATCHED on a _new_ vnode is cleared in diffChildren's placement loop.
			childVNode._flags |= MATCHED;

			// The skew adjustments keep findMatchingIndex's search centered for
			// shift patterns (insertions/removals at the front). A match further
			// than one position away means children were genuinely reordered:
			// flag it so the minimal set of moves is computed below. Off-by-one
			// matches provably keep matched old indices in increasing order, so
			// no moves are needed for them.
			if (matchingIndex == skewedIndex - 1) {
				skew--;
			} else if (matchingIndex == skewedIndex + 1) {
				skew++;
			} else if (matchingIndex != skewedIndex) {
				if (matchingIndex > skewedIndex) {
					skew--;
				} else {
					skew++;
				}

				moved = true;
			}
		}
	}

	if (moved) {
		// Children were reordered: mark the minimal set of matched (MATCHED flag)
		// children for insertion by finding the longest increasing subsequence of
		// old indices (patience sorting). Children on the subsequence stay in
		// place, all others get INSERT_VNODE. `_index` still holds the
		// matchingIndex here.
		/** @type {number[]} tails[x] is the smallest old index ending an increasing subsequence of length x+1 */
		let tails = [];
		/** @type {number[]} length of the longest increasing subsequence ending at child i */
		let lisLengths = [];
		for (i = 0; i < newChildrenLength; i++) {
			childVNode = newChildren[i];
			if (childVNode && childVNode._flags & MATCHED) {
				// Binary search for the insertion point, keeping the pass at
				// O(n log n) even for pathological reorders.
				skew = 0;
				let hi = tails.length;
				while (skew < hi) {
					const mid = (skew + hi) >> 1;
					if (tails[mid] < childVNode._index) {
						skew = mid + 1;
					} else {
						hi = mid;
					}
				}
				tails[skew] = childVNode._index;
				lisLengths[i] = skew + 1;
			}
		}

		// `skew` is dead after the main loop; reuse it as the remaining
		// subsequence length while walking backwards. Likewise `i` is left at
		// newChildrenLength by the loop above.
		skew = tails.length;
		while (i--) {
			if (lisLengths[i]) {
				if (lisLengths[i] == skew) {
					skew--;
				} else {
					newChildren[i]._flags |= INSERT_VNODE;
				}
			}
		}
	}

	// Remove remaining oldChildren if there are any. Loop forwards so that as we
	// unmount DOM from the beginning of the oldChildren, we can adjust oldDom to
	// point to the next child, which needs to be the first DOM node that won't be
	// unmounted. Keep this a plain loop: an arrow function here would capture
	// `oldDom`, forcing V8 to context-allocate it on every call to this function.
	if (remainingOldChildren) {
		for (i = 0; i < oldChildrenLength; i++) {
			oldVNode = oldChildren[i];
			if (oldVNode && !(oldVNode._flags & MATCHED)) {
				if (oldVNode._dom == oldDom) {
					oldDom = getDomSibling(oldVNode);
				}

				unmount(oldVNode, oldVNode);
			}
		}
	}

	return oldDom;
}
```

### 🔹 函式: `findMatchingIndex()`
- **變更前簽章 (Before)**: `function findMatchingIndex(
	childVNode,
	oldChildren,
	skewedIndex,
	remainingOldChildren
)` (L462~L513)
- **變更後簽章 (After)**: `function findMatchingIndex(
	childVNode,
	oldChildren,
	skewedIndex,
	remainingOldChildren
)` (L462~L520)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function findMatchingIndex(
	childVNode,
	oldChildren,
	skewedIndex,
	remainingOldChildren
) {
	const key = childVNode.key;
	const type = childVNode.type;
	let oldVNode = oldChildren[skewedIndex];
	const matched = oldVNode && !(oldVNode._flags & MATCHED);

	// We only need to perform a search if there are more children
	// (remainingOldChildren) to search. However, if the oldVNode we just looked
	// at skewedIndex was not already used in this diff, then there must be at
	// least 1 other (so greater than 1) remainingOldChildren to attempt to match
	// against. So the following condition checks that ensuring
	// remainingOldChildren > 1 if the oldVNode is not already used/matched. Else
	// if the oldVNode was null or matched, then there could needs to be at least
	// 1 (aka `remainingOldChildren > 0`) children to find and compare against.
	//
	// If there is an unkeyed functional VNode, that isn't a built-in like our Fragment,
	// we should not search as we risk re-using state of an unrelated VNode. (reverted for now)
	let shouldSearch =
		// (typeof type != 'function' || type === Fragment || key) &&
		// The ternary keeps this a Smi comparison; `> matched` would compare
		// number to boolean which V8 can't serve from the fast path.
		remainingOldChildren > (matched ? 1 : 0);

	if (
		(oldVNode === NULL && key == NULL) ||
		(matched && key == oldVNode.key && type == oldVNode.type)
	) {
		return skewedIndex;
	} else if (shouldSearch) {
		let x = skewedIndex - 1;
		let y = skewedIndex + 1;
		while (x >= 0 || y < oldChildren.length) {
			const childIndex = x >= 0 ? x-- : y++;
			oldVNode = oldChildren[childIndex];
			if (
				oldVNode &&
				!(oldVNode._flags & MATCHED) &&
				key == oldVNode.key &&
				type == oldVNode.type
			) {
				return childIndex;
			}
		}
	}

	return -1;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function findMatchingIndex(
	childVNode,
	oldChildren,
	skewedIndex,
	remainingOldChildren
) {
	const key = childVNode.key;
	const type = childVNode.type;
	let oldVNode = oldChildren[skewedIndex];
	const matched = oldVNode && !(oldVNode._flags & MATCHED);

	// We only need to perform a search if there are more children
	// (remainingOldChildren) to search. However, if the oldVNode we just looked
	// at skewedIndex was not already used in this diff, then there must be at
	// least 1 other (so greater than 1) remainingOldChildren to attempt to match
	// against. So the following condition checks that ensuring
	// remainingOldChildren > 1 if the oldVNode is not already used/matched. Else
	// if the oldVNode was null or matched, then there could needs to be at least
	// 1 (aka `remainingOldChildren > 0`) children to find and compare against.
	//
	// If there is an unkeyed functional VNode, that isn't a built-in like our Fragment,
	// we should not search as we risk re-using state of an unrelated VNode. (reverted for now)
	let shouldSearch =
		// (typeof type != 'function' || type === Fragment || key) &&
		// The ternary keeps this a Smi comparison; `> matched` would compare
		// number to boolean which V8 can't serve from the fast path.
		remainingOldChildren > (matched ? 1 : 0);

	if (
		(oldVNode === NULL && key == NULL) ||
		(matched && key == oldVNode.key && type == oldVNode.type)
	) {
		return skewedIndex;
	} else if (shouldSearch) {
		let x;
		for (x = skewedIndex - 1; x >= 0; x--) {
			oldVNode = oldChildren[x];
			if (
				oldVNode &&
				!(oldVNode._flags & MATCHED) &&
				key == oldVNode.key &&
				type == oldVNode.type
			)
				return x;
		}
		for (x = skewedIndex + 1; x < oldChildren.length; x++) {
			oldVNode = oldChildren[x];
			if (
				oldVNode &&
				!(oldVNode._flags & MATCHED) &&
				key == oldVNode.key &&
				type == oldVNode.type
			)
				return x;
		}
	}

	return -1;
}
```


#### 📄 檔案: `src/diff/index.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:17, E:19, A:0) ➔ After(N:17, E:19, A:0)
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

### 🔹 函式: `diff()`
- **變更前簽章 (Before)**: `function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L57~L469)
- **變更後簽章 (After)**: `function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L57~L469)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	/** @type {any} */
	let tmp,
		resumed,
		newType = newVNode.type;

	// When passing through createElement it assigns the object
	// constructor as undefined. This to prevent JSON-injection.
	if (newVNode.constructor !== UNDEFINED) return NULL;

	// If the previous diff bailed out, resume creating/hydrating into the DOM
	// that was kept while suspended (server-rendered, or already in the
	// container we rendered into). `tmp` holds the stored excess node until the
	// options._diff call below.
	if (
		oldVNode._flags & MODE_SUSPENDED &&
		// @ts-expect-error This is MODE_HYDRATE or 0
		((isHydrating = oldVNode._flags & MODE_HYDRATE),
		(tmp = oldVNode._component._excess))
	) {
		newVNode._flags |= isHydrating;
		resumed = excessDomChildren = [];
		if (tmp.nodeType == 8) {
			// Re-scan DOM from stored start marker for streamed hydration.
			// `depth` only ever reaches 0 through the `break` below, so it
			// doesn't need to be re-tested in the loop condition.
			for (
				let depth = 1, node = tmp.nextSibling;
				node;
				node = node.nextSibling
			) {
				if (node.nodeType == 8) {
					if (node.data.startsWith('$s')) depth++;
					else if (node.data.startsWith('/$s') && !--depth) break;
				}
				excessDomChildren.push(node);
			}
		} else {
			excessDomChildren.push(tmp);
		}
		oldDom = excessDomChildren[0];
	}

	if ((tmp = options._diff)) tmp(newVNode);

	outer: if (typeof newType == 'function') {
		let oldCommitQueueLength = commitQueue.length;
		try {
			let c,
				oldProps,
				oldState,
				snapshot,
				newProps = newVNode.props;
			const isClassComponent = (tmp = newType.prototype) && tmp.render;

			// Necessary for createContext api. Setting this property will pass
			// the context value as `this.context` just for this component.
			tmp = newType.contextType;
			const provider = tmp && globalContext[tmp._id];
			const componentContext = tmp
				? provider
					? provider.props.value
					: tmp._defaultValue
				: globalContext;

			// Get component and set it to `c`
			if (oldVNode._component) {
				c = newVNode._component = oldVNode._component;
				if (c._bits & COMPONENT_PENDING_ERROR) {
					c._bits |= COMPONENT_PROCESSING_EXCEPTION;
				}
			} else {
				// Instantiate the new component
				if (isClassComponent) {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new newType(newProps, componentContext); // eslint-disable-line new-cap
				} else {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new BaseComponent(
						newProps,
						componentContext
					);

					c.constructor = newType;
					c.render = doRender;
				}
				if (provider) provider.sub(c);

				if (!c.state) c.state = {};
				c._globalContext = globalContext;
				c._bits |= COMPONENT_DIRTY;
				c._renderCallbacks = [];
				c._stateCallbacks = [];
			}

			if (isClassComponent) {
				if (!c._nextState) c._nextState = c.state;

				// Invoke getDerivedStateFromProps
				if (newType.getDerivedStateFromProps) {
					if (c._nextState == c.state) {
						c._nextState = assign({}, c._nextState);
					}

					assign(
						c._nextState,
						newType.getDerivedStateFromProps(newProps, c._nextState)
					);
				}
			}

			oldProps = c.props;
			oldState = c.state;
			c._vnode = newVNode;

			// Invoke pre-render lifecycle methods
			if (!oldVNode._component) {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					c.componentWillMount
				) {
					c.componentWillMount();
				}

				if (isClassComponent && c.componentDidMount) {
					c._renderCallbacks.push(c.componentDidMount);
				}
			} else {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					newProps !== oldProps &&
					c.componentWillReceiveProps
				) {
					c.componentWillReceiveProps(newProps, componentContext);
				}

				if (
					(newVNode._original == oldVNode._original &&
						!(c._bits & COMPONENT_DIRTY)) ||
					(!(c._bits & COMPONENT_FORCE) &&
						c.shouldComponentUpdate &&
						c.shouldComponentUpdate(
							newProps,
							c._nextState,
							componentContext
						) === false)
				) {
					// More info about this here: https://gist.github.com/JoviDeCroock/bec5f2ce93544d2e6070ef8e0036e4e8
					if (newVNode._original != oldVNode._original) {
						// When we are dealing with a bail because of sCU we have to update
						// the props, state and dirty-state.
						// when we are dealing with strict-equality we don't as the child could still
						// be dirtied see #3883
						c.props = newProps;
						c.state = c._nextState;
						c._bits &= ~COMPONENT_DIRTY;
					}

					newVNode._dom = oldVNode._dom;
					newVNode._children = oldVNode._children;
					newVNode._children.some(vnode => {
						if (vnode) vnode._parent = newVNode;
					});

					EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
					c._stateCallbacks = [];

					if (c._renderCallbacks.length) {
						commitQueue.push(c);
					}

					// Skip over the retained subtree without traversing it; the
					// `result` branch in diffChildren picks this up as the next
					// oldDom.
					oldDom = getDomSibling(oldVNode);

					break outer;
				}

				if (c.componentWillUpdate) {
					c.componentWillUpdate(newProps, c._nextState, componentContext);
				}

				if (isClassComponent && c.componentDidUpdate) {
					c._renderCallbacks.push(() => {
						c.componentDidUpdate(oldProps, oldState, snapshot);
					});
				}
			}

			c.context = componentContext;
			c.props = newProps;
			c._parentDom = parentDom;
			c._bits &= ~COMPONENT_FORCE;

			let renderHook = options._render,
				count = 0;
			if (isClassComponent) {
				c.state = c._nextState;
				c._bits &= ~COMPONENT_DIRTY;

				if (renderHook) renderHook(newVNode);

				tmp = c.render(c.props, c.state, c.context);

				EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
				c._stateCallbacks = [];
			} else {
				do {
					c._bits &= ~COMPONENT_DIRTY;
					if (renderHook) renderHook(newVNode);

					tmp = c.render(c.props, c.state, c.context);

					// Handle setState called in render, see #2553
					c.state = c._nextState;
				} while (c._bits & COMPONENT_DIRTY && ++count < 25);
			}

			// Handle setState called in render, see #2553
			c.state = c._nextState;

			if (c.getChildContext) {
				globalContext = assign({}, globalContext, c.getChildContext());
			}

			if (
				isClassComponent &&
				oldVNode._component &&
				c.getSnapshotBeforeUpdate
			) {
				snapshot = c.getSnapshotBeforeUpdate(oldProps, oldState);
			}

			const renderResult =
				tmp && tmp.type === Fragment && tmp.key == NULL
					? tmp.props.children
					: tmp;

			// A vnode carrying a `_parentDom` prop, considered a new root,
			// continues rendering into that container. The subtree must stay
			// invisible to the host tree's DOM bookkeeping: the portal vnode
			// keeps a `null` `_dom` and the host insertion cursor (`oldDom`)
			// passes through unchanged.
			// `tmp` (the raw render result, already unwrapped into renderResult)
			// doubles as the saved host insertion cursor while we render into
			// the portal's container.
			if (newProps._parentDom) {
				tmp = oldDom;
				parentDom = newProps._parentDom;
				// If we portal into a math or svg element we need
				// to swap the namespace (chart libraries often do this).
				// The document follows the container too (e.g. iframes) as
				// diffElementNodes derives it from its parentDom.
				namespace = parentDom.namespaceURI;
				// Portals are never server-rendered: hydration must not claim the
				// host parent's excess nodes for the container's children.
				isHydrating = excessDomChildren = NULL;

				// Changing the container remounts the children into the new one
				if (oldVNode.props && oldVNode.props._parentDom != parentDom) {
					/** @type {VNode[]} */ (oldVNode._children).some(child => {
						if (child) unmount(child, child);
					});
					oldVNode._children = NULL;
				}

				oldDom = oldVNode._children ? getDomSibling(oldVNode, 0) : NULL;
			}

			oldDom = diffChildren(
				parentDom,
				isArray(renderResult) ? renderResult : [renderResult],
				newVNode,
				oldVNode,
				globalContext,
				namespace,
				excessDomChildren,
				commitQueue,
				oldDom,
				isHydrating,
				refQueue
			);

			// When we exit a portal we
			// change up the oldDom
			if (newProps._parentDom) {
				newVNode._dom = NULL;
				oldDom = tmp;
			}

			// We successfully rendered this VNode, unset any stored hydration/bailout state:
			newVNode._flags &= RESET_MODE;
			if (oldVNode._flags & MODE_SUSPENDED) c._excess = NULL;

			// Remove the kept DOM this resumed render didn't claim
			if (resumed) resumed.some(removeNode);

			if (c._renderCallbacks.length) {
				commitQueue.push(c);
			}

			// Only clear when this render was the retry; PENDING_ERROR set by a
			// descendant during this render must survive until then.
			if (c._bits & COMPONENT_PROCESSING_EXCEPTION) {
				c._bits &= ~(COMPONENT_PROCESSING_EXCEPTION | COMPONENT_PENDING_ERROR);
			}
		} catch (e) {
			// We remove any componentDidMount, ...
			// that have been invalidated by us
			// intercepting the error.
			commitQueue.length = oldCommitQueueLength;
			newVNode._original = NULL;
			// if hydrating or creating initial tree, bailout preserves DOM:
			if (isHydrating || excessDomChildren) {
				if (e.then) {
					let commentMarkersToFind = 0,
						startMarker;

					newVNode._flags |= isHydrating
						? MODE_HYDRATE | MODE_SUSPENDED
						: MODE_SUSPENDED;

					if (excessDomChildren) {
						let i = excessDomChildren.indexOf(oldDom || UNDEFINED),
							child;
						if (!~i) i = excessDomChildren.length;

						// The cursor skips comments: step back to this component's markers.
						while ((child = excessDomChildren[i - 1]) && child.nodeType == 8) {
							i--;
						}

						for (; i < excessDomChildren.length; i++) {
							child = excessDomChildren[i];
							if (!child) continue;
							excessDomChildren[i] = NULL;

							if (child.nodeType == 8) {
								if (child.data.startsWith('$s')) {
									if (!commentMarkersToFind++) startMarker = child;
								} else if (
									commentMarkersToFind &&
									child.data.startsWith('/$s') &&
									!--commentMarkersToFind
								) {
									oldDom = child;
									break;
								}
							} else if (!commentMarkersToFind) {
								break;
							}
						}
					}

					if (!startMarker) {
						while (oldDom && oldDom.nodeType == 8 && oldDom.nextSibling) {
							oldDom = oldDom.nextSibling;
						}
						startMarker = oldDom;
					}
					// Store the start marker directly; children re-scanned on resume.
					// A re-suspension keeps the marker it originally started from.
					if (!newVNode._component._excess) {
						newVNode._component._excess = startMarker;
					}
					newVNode._dom = oldDom;
				} else if (excessDomChildren) {
					excessDomChildren.some(removeNode);
				}
			} else {
				newVNode._dom = oldVNode._dom;
			}

			if (!newVNode._children) {
				newVNode._children = oldVNode._children || [];
			}

			if (!e.then) markAsForce(newVNode);
			options._catchError(e, newVNode, oldVNode);
		}
	} else {
		oldDom = newVNode._dom = diffElementNodes(
			oldVNode._dom,
			newVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			isHydrating,
			refQueue,
			parentDom
		);
	}

	if ((tmp = options.diffed)) tmp(newVNode);

	return newVNode._flags & MODE_SUSPENDED ? UNDEFINED : oldDom;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	/** @type {any} */
	let tmp,
		resumed,
		newType = newVNode.type;

	// When passing through createElement it assigns the object
	// constructor as undefined. This to prevent JSON-injection.
	if (newVNode.constructor !== UNDEFINED) return NULL;

	// If the previous diff bailed out, resume creating/hydrating into the DOM
	// that was kept while suspended (server-rendered, or already in the
	// container we rendered into). `tmp` holds the stored excess node until the
	// options._diff call below.
	if (
		oldVNode._flags & MODE_SUSPENDED &&
		// @ts-expect-error This is MODE_HYDRATE or 0
		((isHydrating = oldVNode._flags & MODE_HYDRATE),
		(tmp = oldVNode._component._excess))
	) {
		newVNode._flags |= isHydrating;
		resumed = excessDomChildren = [];
		if (tmp.nodeType == 8) {
			// Re-scan DOM from stored start marker for streamed hydration.
			// `depth` only ever reaches 0 through the `break` below, so it
			// doesn't need to be re-tested in the loop condition.
			for (
				let depth = 1, node = tmp.nextSibling;
				node;
				node = node.nextSibling
			) {
				if (node.nodeType == 8) {
					if (node.data.startsWith('$s')) depth++;
					else if (node.data.startsWith('/$s') && !--depth) break;
				}
				excessDomChildren.push(node);
			}
		} else {
			excessDomChildren.push(tmp);
		}
		oldDom = excessDomChildren[0];
	}

	if ((tmp = options._diff)) tmp(newVNode);

	outer: if (typeof newType == 'function') {
		let oldCommitQueueLength = commitQueue.length;
		try {
			let c,
				oldProps,
				oldState,
				snapshot,
				newProps = newVNode.props;
			const isClassComponent = (tmp = newType.prototype) && tmp.render;

			// Necessary for createContext api. Setting this property will pass
			// the context value as `this.context` just for this component.
			tmp = newType.contextType;
			const provider = tmp && globalContext[tmp._id];
			const componentContext = tmp
				? provider
					? provider.props.value
					: tmp._defaultValue
				: globalContext;

			// Get component and set it to `c`
			if ((c = oldVNode._component)) {
				newVNode._component = c;
				if (c._bits & COMPONENT_PENDING_ERROR) {
					c._bits |= COMPONENT_PROCESSING_EXCEPTION;
				}
			} else {
				// Instantiate the new component
				if (isClassComponent) {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new newType(newProps, componentContext); // eslint-disable-line new-cap
				} else {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new BaseComponent(
						newProps,
						componentContext
					);

					c.constructor = newType;
					c.render = doRender;
				}
				if (provider) provider.sub(c);

				if (!c.state) c.state = {};
				c._globalContext = globalContext;
				c._bits |= COMPONENT_DIRTY;
				c._renderCallbacks = [];
				c._stateCallbacks = [];
			}

			if (isClassComponent) {
				if (!c._nextState) c._nextState = c.state;

				// Invoke getDerivedStateFromProps
				if (newType.getDerivedStateFromProps) {
					if (c._nextState == c.state) {
						c._nextState = assign({}, c._nextState);
					}

					assign(
						c._nextState,
						newType.getDerivedStateFromProps(newProps, c._nextState)
					);
				}
			}

			oldProps = c.props;
			oldState = c.state;
			c._vnode = newVNode;

			// Invoke pre-render lifecycle methods
			if (!oldVNode._component) {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					c.componentWillMount
				) {
					c.componentWillMount();
				}

				if (isClassComponent && c.componentDidMount) {
					c._renderCallbacks.push(c.componentDidMount);
				}
			} else {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					newProps !== oldProps &&
					c.componentWillReceiveProps
				) {
					c.componentWillReceiveProps(newProps, componentContext);
				}

				if (
					(newVNode._original == oldVNode._original &&
						!(c._bits & COMPONENT_DIRTY)) ||
					(!(c._bits & COMPONENT_FORCE) &&
						c.shouldComponentUpdate &&
						c.shouldComponentUpdate(
							newProps,
							c._nextState,
							componentContext
						) === false)
				) {
					// More info about this here: https://gist.github.com/JoviDeCroock/bec5f2ce93544d2e6070ef8e0036e4e8
					if (newVNode._original != oldVNode._original) {
						// When we are dealing with a bail because of sCU we have to update
						// the props, state and dirty-state.
						// when we are dealing with strict-equality we don't as the child could still
						// be dirtied see #3883
						c.props = newProps;
						c.state = c._nextState;
						c._bits &= ~COMPONENT_DIRTY;
					}

					newVNode._dom = oldVNode._dom;
					newVNode._children = oldVNode._children;
					newVNode._children.some(vnode => {
						if (vnode) vnode._parent = newVNode;
					});

					EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
					c._stateCallbacks = [];

					if (c._renderCallbacks.length) {
						commitQueue.push(c);
					}

					// Skip over the retained subtree without traversing it; the
					// `result` branch in diffChildren picks this up as the next
					// oldDom.
					oldDom = getDomSibling(oldVNode);

					break outer;
				}

				if (c.componentWillUpdate) {
					c.componentWillUpdate(newProps, c._nextState, componentContext);
				}

				if (isClassComponent && c.componentDidUpdate) {
					c._renderCallbacks.push(() => {
						c.componentDidUpdate(oldProps, oldState, snapshot);
					});
				}
			}

			c.context = componentContext;
			c.props = newProps;
			c._parentDom = parentDom;
			c._bits &= ~COMPONENT_FORCE;

			let renderHook = options._render,
				count = 0;
			if (isClassComponent) {
				c.state = c._nextState;
				c._bits &= ~COMPONENT_DIRTY;

				if (renderHook) renderHook(newVNode);

				tmp = c.render(c.props, c.state, c.context);

				EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
				c._stateCallbacks = [];
			} else {
				do {
					c._bits &= ~COMPONENT_DIRTY;
					if (renderHook) renderHook(newVNode);

					tmp = c.render(c.props, c.state, c.context);

					// Handle setState called in render, see #2553
					c.state = c._nextState;
				} while (c._bits & COMPONENT_DIRTY && ++count < 25);
			}

			// Handle setState called in render, see #2553
			c.state = c._nextState;

			if (c.getChildContext) {
				globalContext = assign({}, globalContext, c.getChildContext());
			}

			if (
				isClassComponent &&
				oldVNode._component &&
				c.getSnapshotBeforeUpdate
			) {
				snapshot = c.getSnapshotBeforeUpdate(oldProps, oldState);
			}

			const renderResult =
				tmp && tmp.type === Fragment && tmp.key == NULL
					? tmp.props.children
					: tmp;

			// A vnode carrying a `_parentDom` prop, considered a new root,
			// continues rendering into that container. The subtree must stay
			// invisible to the host tree's DOM bookkeeping: the portal vnode
			// keeps a `null` `_dom` and the host insertion cursor (`oldDom`)
			// passes through unchanged.
			// `tmp` (the raw render result, already unwrapped into renderResult)
			// doubles as the saved host insertion cursor while we render into
			// the portal's container.
			if (newProps._parentDom) {
				tmp = oldDom;
				parentDom = newProps._parentDom;
				// If we portal into a math or svg element we need
				// to swap the namespace (chart libraries often do this).
				// The document follows the container too (e.g. iframes) as
				// diffElementNodes derives it from its parentDom.
				namespace = parentDom.namespaceURI;
				// Portals are never server-rendered: hydration must not claim the
				// host parent's excess nodes for the container's children.
				isHydrating = excessDomChildren = NULL;

				// Changing the container remounts the children into the new one
				if (oldVNode.props && oldVNode.props._parentDom != parentDom) {
					/** @type {VNode[]} */ (oldVNode._children).some(child => {
						if (child) unmount(child, child);
					});
					oldVNode._children = NULL;
				}

				oldDom = oldVNode._children ? getDomSibling(oldVNode, 0) : NULL;
			}

			oldDom = diffChildren(
				parentDom,
				isArray(renderResult) ? renderResult : [renderResult],
				newVNode,
				oldVNode,
				globalContext,
				namespace,
				excessDomChildren,
				commitQueue,
				oldDom,
				isHydrating,
				refQueue
			);

			// When we exit a portal we
			// change up the oldDom
			if (newProps._parentDom) {
				newVNode._dom = NULL;
				oldDom = tmp;
			}

			// We successfully rendered this VNode, unset any stored hydration/bailout state:
			newVNode._flags &= RESET_MODE;
			if (oldVNode._flags & MODE_SUSPENDED) c._excess = NULL;

			// Remove the kept DOM this resumed render didn't claim
			if (resumed) resumed.some(removeNode);

			if (c._renderCallbacks.length) {
				commitQueue.push(c);
			}

			// Only clear when this render was the retry; PENDING_ERROR set by a
			// descendant during this render must survive until then.
			if (c._bits & COMPONENT_PROCESSING_EXCEPTION) {
				c._bits &= ~(COMPONENT_PROCESSING_EXCEPTION | COMPONENT_PENDING_ERROR);
			}
		} catch (e) {
			// We remove any componentDidMount, ...
			// that have been invalidated by us
			// intercepting the error.
			commitQueue.length = oldCommitQueueLength;
			newVNode._original = NULL;
			// if hydrating or creating initial tree, bailout preserves DOM:
			if (isHydrating || excessDomChildren) {
				if (e.then) {
					let commentMarkersToFind = 0,
						startMarker;

					newVNode._flags |= isHydrating
						? MODE_HYDRATE | MODE_SUSPENDED
						: MODE_SUSPENDED;

					if (excessDomChildren) {
						let i = excessDomChildren.indexOf(oldDom || UNDEFINED),
							child;
						if (!~i) i = excessDomChildren.length;

						// The cursor skips comments: step back to this component's markers.
						while ((child = excessDomChildren[i - 1]) && child.nodeType == 8) {
							i--;
						}

						for (; i < excessDomChildren.length; i++) {
							child = excessDomChildren[i];
							if (!child) continue;
							excessDomChildren[i] = NULL;

							if (child.nodeType == 8) {
								if (child.data.startsWith('$s')) {
									if (!commentMarkersToFind++) startMarker = child;
								} else if (
									commentMarkersToFind &&
									child.data.startsWith('/$s') &&
									!--commentMarkersToFind
								) {
									oldDom = child;
									break;
								}
							} else if (!commentMarkersToFind) {
								break;
							}
						}
					}

					if (!startMarker) {
						while (oldDom && oldDom.nodeType == 8 && oldDom.nextSibling) {
							oldDom = oldDom.nextSibling;
						}
						startMarker = oldDom;
					}
					// Store the start marker directly; children re-scanned on resume.
					// A re-suspension keeps the marker it originally started from.
					if (!newVNode._component._excess) {
						newVNode._component._excess = startMarker;
					}
					newVNode._dom = oldDom;
				} else if (excessDomChildren) {
					excessDomChildren.some(removeNode);
				}
			} else {
				newVNode._dom = oldVNode._dom;
			}

			if (!newVNode._children) {
				newVNode._children = oldVNode._children || [];
			}

			if (!e.then) markAsForce(newVNode);
			options._catchError(e, newVNode, oldVNode);
		}
	} else {
		oldDom = newVNode._dom = diffElementNodes(
			oldVNode._dom,
			newVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			isHydrating,
			refQueue,
			parentDom
		);
	}

	if ((tmp = options.diffed)) tmp(newVNode);

	return newVNode._flags & MODE_SUSPENDED ? UNDEFINED : oldDom;
}
```


#### 📄 檔案: `src/diff/props.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:12, E:5, A:1) ➔ After(N:12, E:5, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#dom** `(Control)`
    └── ⚡ **on('name')**
        └── 🎯 [TRIGGERS] `proxy (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `setProperty()`
- **變更前簽章 (Before)**: `function setProperty(dom, name, value, oldValue, namespace)` (L41~L142)
- **變更後簽章 (After)**: `function setProperty(dom, name, value, oldValue, namespace)` (L41~L141)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function setProperty(dom, name, value, oldValue, namespace) {
	let useCapture;

	o: if (name == 'style') {
		if (typeof value == 'string') {
			dom.style.cssText = value;
		} else {
			if (typeof oldValue == 'string') {
				dom.style.cssText = oldValue = '';
			}

			if (oldValue) {
				for (name in oldValue) {
					if (!(value && name in value)) {
						setStyle(dom.style, name, '');
					}
				}
			}

			if (value) {
				for (name in value) {
					if (!oldValue || value[name] != oldValue[name]) {
						setStyle(dom.style, name, value[name]);
					}
				}
			}
		}
	}
	// Benchmark for comparison: https://esbench.com/bench/574c954bdb965b9a00965ac6
	else if (name[0] == 'o' && name[1] == 'n') {
		// Handlers are keyed by prop name and every prop name gets its own proxy,
		// so swapping one (e.g. an inline arrow function on every render) is a
		// single store. The event name is only derived to attach or remove it.
		(dom._listeners || (dom._listeners = {}))[name] = value;

		if (!value || !oldValue) {
			const proxy =
				eventProxies[name] || (eventProxies[name] = createEventProxy(name));
			// The attach time belongs to the listener, not to the handler: one
			// function can back several listeners that were attached at different
			// times. It lives outside `_listeners`, which unmount resets even when
			// a re-suspended Suspense boundary keeps the DOM and its listeners.
			(dom._attached || (dom._attached = {}))[name] = eventClock;
			useCapture = name != (name = name.replace(CAPTURE_REGEX, '$1'));

			// Infer correct casing for DOM built-in events: `onClick` -> `click`.
			// Only names starting with an uppercase letter are lowercased, so
			// camelCase custom events keep their casing: `onionChange` -> `ionChange`.
			name = name.slice(2);
			if (name[0] < 'a') name = name.toLowerCase();

			if (value) {
				dom.addEventListener(name, proxy, useCapture);
			} else {
				dom.removeEventListener(name, proxy, useCapture);
			}
		}
	} else {
		if (namespace == SVG_NAMESPACE) {
			// Normalize incorrect prop usage for SVG:
			// - xlink:href / xlinkHref --> href (xlink:href was removed from SVG and isn't needed)
			// - className --> class
			name = name.replace(/xlink(H|:h)/, 'h').replace(/sName$/, 's');
		} else if (
			name != 'width' &&
			name != 'height' &&
			name != 'href' &&
			name != 'list' &&
			name != 'form' &&
			// Default value in browsers is `-1` and an empty string is
			// cast to `0` instead
			name != 'tabIndex' &&
			name != 'download' &&
			name != 'rowSpan' &&
			name != 'colSpan' &&
			name != 'role' &&
			name != 'popover' &&
			name in dom
		) {
			try {
				dom[name] = value == NULL ? '' : value;
				// labelled break is 1b smaller here than a return statement (sorry)
				break o;
			} catch (e) {}
		}

		// aria- and data- attributes have no boolean representation.
		// A `false` value is different from the attribute not being
		// present, so we can't remove it. For non-boolean aria
		// attributes we could treat false as a removal, but the
		// amount of exceptions would cost too many bytes. On top of
		// that other frameworks generally stringify `false`.

		if (typeof value == 'function') {
			// never serialize functions as attribute values
		} else if (value != NULL && (value !== false || name[4] == '-')) {
			dom.setAttribute(name, name == 'popover' && value == true ? '' : value);
		} else {
			dom.removeAttribute(name);
		}
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function setProperty(dom, name, value, oldValue, namespace) {
	let useCapture;

	if (name == 'style') {
		if (typeof value == 'string') {
			dom.style.cssText = value;
		} else {
			if (typeof oldValue == 'string') {
				dom.style.cssText = oldValue = '';
			}

			if (oldValue) {
				for (name in oldValue) {
					if (!(value && name in value)) {
						setStyle(dom.style, name, '');
					}
				}
			}

			if (value) {
				for (name in value) {
					if (!oldValue || value[name] != oldValue[name]) {
						setStyle(dom.style, name, value[name]);
					}
				}
			}
		}
	}
	// Benchmark for comparison: https://esbench.com/bench/574c954bdb965b9a00965ac6
	else if (name[0] == 'o' && name[1] == 'n') {
		// Handlers are keyed by prop name and every prop name gets its own proxy,
		// so swapping one (e.g. an inline arrow function on every render) is a
		// single store. The event name is only derived to attach or remove it.
		(dom._listeners || (dom._listeners = {}))[name] = value;

		if (!value || !oldValue) {
			const proxy =
				eventProxies[name] || (eventProxies[name] = createEventProxy(name));
			// The attach time belongs to the listener, not to the handler: one
			// function can back several listeners that were attached at different
			// times. It lives outside `_listeners`, which unmount resets even when
			// a re-suspended Suspense boundary keeps the DOM and its listeners.
			(dom._attached || (dom._attached = {}))[name] = eventClock;
			useCapture = name != (name = name.replace(CAPTURE_REGEX, '$1'));

			// Infer correct casing for DOM built-in events: `onClick` -> `click`.
			// Only names starting with an uppercase letter are lowercased, so
			// camelCase custom events keep their casing: `onionChange` -> `ionChange`.
			name = name.slice(2);
			if (name[0] < 'a') name = name.toLowerCase();

			if (value) {
				dom.addEventListener(name, proxy, useCapture);
			} else {
				dom.removeEventListener(name, proxy, useCapture);
			}
		}
	} else {
		if (namespace == SVG_NAMESPACE) {
			// Normalize incorrect prop usage for SVG:
			// - xlink:href / xlinkHref --> href (xlink:href was removed from SVG and isn't needed)
			// - className --> class
			name = name.replace(/xlink(H|:h)/, 'h').replace(/sName$/, 's');
		} else if (
			name != 'width' &&
			name != 'height' &&
			name != 'href' &&
			name != 'list' &&
			name != 'form' &&
			// Default value in browsers is `-1` and an empty string is
			// cast to `0` instead
			name != 'tabIndex' &&
			name != 'download' &&
			name != 'rowSpan' &&
			name != 'colSpan' &&
			name != 'role' &&
			name != 'popover' &&
			name in dom
		) {
			try {
				dom[name] = value == NULL ? '' : value;
				return;
			} catch (e) {}
		}

		// aria- and data- attributes have no boolean representation.
		// A `false` value is different from the attribute not being
		// present, so we can't remove it. For non-boolean aria
		// attributes we could treat false as a removal, but the
		// amount of exceptions would cost too many bytes. On top of
		// that other frameworks generally stringify `false`.

		// Never serialize functions as attribute values.
		if (typeof value == 'function') return;
		if (value != NULL && (value !== false || name[4] == '-')) {
			dom.setAttribute(name, name == 'popover' && value == true ? '' : value);
		} else {
			dom.removeAttribute(name);
		}
	}
}
```


---

### 🔹 Commit #02: `28ef4dcb`
- **完整 Hash**: `28ef4dcbe04d8322f46803a76071151512a4c705`
- **說明 (Ground Truth)**: fix: Correct file extension on compat/server.browser
- **變更檔案數**: 2

#### 📄 檔案: `compat/server.browser.js`
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

#### 📄 檔案: `compat/server.browser.mjs`
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

---

### 🔹 Commit #03: `67a88d56`
- **完整 Hash**: `67a88d56c02a073dd86e5f8c7b1ad3d44d501e86`
- **說明 (Ground Truth)**: Keep suspended hydration within a component's own `$s` range
- **變更檔案數**: 2

#### 📄 檔案: `src/diff/children.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:12, E:14, A:0) ➔ After(N:12, E:14, A:0)
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

### 🔹 函式: `insert()`
- **變更前簽章 (Before)**: `function insert(parentVNode, oldDom, parentDom, isMounting)` (L384~L428)
- **變更後簽章 (After)**: `function insert(parentVNode, oldDom, parentDom, isMounting)` (L384~L433)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function insert(parentVNode, oldDom, parentDom, isMounting) {
	// Note: VNodes in nested suspended trees may be missing _children.
	if (typeof parentVNode.type == 'function') {
		// Root children live in another container, they never move with the
		// host tree and contribute nothing to the host insertion cursor.
		if (parentVNode.props._parentDom) return oldDom;
		let children = parentVNode._children;
		if (children) {
			for (let i = 0; i < children.length; i++) {
				if (children[i]) {
					// If we enter this code path on sCU bailout, where we copy
					// oldVNode._children to newVNode._children, we need to update the old
					// children's _parent pointer to point to the newVNode (parentVNode
					// here).
					children[i]._parent = parentVNode;
					oldDom = insert(children[i], oldDom, parentDom, false);
				}
			}
		}

		return oldDom;
	} else {
		// A cursor a parked Suspense subtree detached can't be a reference node:
		// retry from the vnode tree, then give up and append.
		if (oldDom && !oldDom.parentNode) {
			oldDom = getDomSibling(parentVNode);
			if (oldDom && !oldDom.parentNode) oldDom = NULL;
		}

		if (parentVNode._dom != oldDom) {
			// Containers that aren't DOM nodes may not implement moveBefore()
			if (!isMounting && parentDom.moveBefore && parentVNode._dom.parentNode) {
				// @ts-expect-error This isn't added to TypeScript lib.d.ts yet
				parentDom.moveBefore(parentVNode._dom, oldDom);
			} else {
				parentDom.insertBefore(parentVNode._dom, oldDom || NULL);
			}
		}
		oldDom = parentVNode._dom;
	}

	while ((oldDom = oldDom && oldDom.nextSibling) && oldDom.nodeType == 8);

	return oldDom;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function insert(parentVNode, oldDom, parentDom, isMounting) {
	// Note: VNodes in nested suspended trees may be missing _children.
	if (typeof parentVNode.type == 'function') {
		// Root children live in another container, they never move with the
		// host tree and contribute nothing to the host insertion cursor.
		if (parentVNode.props._parentDom) return oldDom;
		let children = parentVNode._children;
		if (children) {
			for (let i = 0; i < children.length; i++) {
				if (children[i]) {
					// If we enter this code path on sCU bailout, where we copy
					// oldVNode._children to newVNode._children, we need to update the old
					// children's _parent pointer to point to the newVNode (parentVNode
					// here).
					children[i]._parent = parentVNode;
					oldDom = insert(children[i], oldDom, parentDom, false);
				}
			}
		}

		return oldDom;
	} else {
		// A cursor a parked Suspense subtree detached can't be a reference node:
		// retry from the vnode tree, then give up and append.
		if (oldDom && !oldDom.parentNode) {
			oldDom = getDomSibling(parentVNode);
			if (oldDom && !oldDom.parentNode) oldDom = NULL;
		}

		// Comments (e.g. server `$s` markers) are never ours: a node right after
		// them is already in place.
		let next = oldDom;
		while (next && next.nodeType == 8) next = next.nextSibling;

		if (parentVNode._dom != next) {
			// Containers that aren't DOM nodes may not implement moveBefore()
			if (!isMounting && parentDom.moveBefore && parentVNode._dom.parentNode) {
				// @ts-expect-error This isn't added to TypeScript lib.d.ts yet
				parentDom.moveBefore(parentVNode._dom, oldDom);
			} else {
				parentDom.insertBefore(parentVNode._dom, oldDom || NULL);
			}
		}
		oldDom = parentVNode._dom;
	}

	while ((oldDom = oldDom && oldDom.nextSibling) && oldDom.nodeType == 8);

	return oldDom;
}
```


#### 📄 檔案: `src/diff/index.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:17, E:19, A:0) ➔ After(N:17, E:19, A:0)
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

### 🔹 函式: `diff()`
- **變更前簽章 (Before)**: `function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L57~L463)
- **變更後簽章 (After)**: `function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L57~L469)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	/** @type {any} */
	let tmp,
		resumed,
		newType = newVNode.type;

	// When passing through createElement it assigns the object
	// constructor as undefined. This to prevent JSON-injection.
	if (newVNode.constructor !== UNDEFINED) return NULL;

	// If the previous diff bailed out, resume creating/hydrating into the DOM
	// that was kept while suspended (server-rendered, or already in the
	// container we rendered into). `tmp` holds the stored excess node until the
	// options._diff call below.
	if (
		oldVNode._flags & MODE_SUSPENDED &&
		// @ts-expect-error This is MODE_HYDRATE or 0
		((isHydrating = oldVNode._flags & MODE_HYDRATE),
		(tmp = oldVNode._component._excess))
	) {
		newVNode._flags |= isHydrating;
		resumed = excessDomChildren = [];
		if (tmp.nodeType == 8) {
			// Re-scan DOM from stored start marker for streamed hydration.
			// `depth` only ever reaches 0 through the `break` below, so it
			// doesn't need to be re-tested in the loop condition.
			for (
				let depth = 1, node = tmp.nextSibling;
				node;
				node = node.nextSibling
			) {
				if (node.nodeType == 8) {
					if (node.data.startsWith('$s')) depth++;
					else if (node.data.startsWith('/$s') && !--depth) break;
				}
				excessDomChildren.push(node);
			}
		} else {
			excessDomChildren.push(tmp);
		}
		oldDom = excessDomChildren[0];
	}

	if ((tmp = options._diff)) tmp(newVNode);

	outer: if (typeof newType == 'function') {
		let oldCommitQueueLength = commitQueue.length;
		try {
			let c,
				oldProps,
				oldState,
				snapshot,
				newProps = newVNode.props;
			const isClassComponent = (tmp = newType.prototype) && tmp.render;

			// Necessary for createContext api. Setting this property will pass
			// the context value as `this.context` just for this component.
			tmp = newType.contextType;
			const provider = tmp && globalContext[tmp._id];
			const componentContext = tmp
				? provider
					? provider.props.value
					: tmp._defaultValue
				: globalContext;

			// Get component and set it to `c`
			if (oldVNode._component) {
				c = newVNode._component = oldVNode._component;
				if (c._bits & COMPONENT_PENDING_ERROR) {
					c._bits |= COMPONENT_PROCESSING_EXCEPTION;
				}
			} else {
				// Instantiate the new component
				if (isClassComponent) {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new newType(newProps, componentContext); // eslint-disable-line new-cap
				} else {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new BaseComponent(
						newProps,
						componentContext
					);

					c.constructor = newType;
					c.render = doRender;
				}
				if (provider) provider.sub(c);

				if (!c.state) c.state = {};
				c._globalContext = globalContext;
				c._bits |= COMPONENT_DIRTY;
				c._renderCallbacks = [];
				c._stateCallbacks = [];
			}

			if (isClassComponent) {
				if (!c._nextState) c._nextState = c.state;

				// Invoke getDerivedStateFromProps
				if (newType.getDerivedStateFromProps) {
					if (c._nextState == c.state) {
						c._nextState = assign({}, c._nextState);
					}

					assign(
						c._nextState,
						newType.getDerivedStateFromProps(newProps, c._nextState)
					);
				}
			}

			oldProps = c.props;
			oldState = c.state;
			c._vnode = newVNode;

			// Invoke pre-render lifecycle methods
			if (!oldVNode._component) {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					c.componentWillMount
				) {
					c.componentWillMount();
				}

				if (isClassComponent && c.componentDidMount) {
					c._renderCallbacks.push(c.componentDidMount);
				}
			} else {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					newProps !== oldProps &&
					c.componentWillReceiveProps
				) {
					c.componentWillReceiveProps(newProps, componentContext);
				}

				if (
					(newVNode._original == oldVNode._original &&
						!(c._bits & COMPONENT_DIRTY)) ||
					(!(c._bits & COMPONENT_FORCE) &&
						c.shouldComponentUpdate &&
						c.shouldComponentUpdate(
							newProps,
							c._nextState,
							componentContext
						) === false)
				) {
					// More info about this here: https://gist.github.com/JoviDeCroock/bec5f2ce93544d2e6070ef8e0036e4e8
					if (newVNode._original != oldVNode._original) {
						// When we are dealing with a bail because of sCU we have to update
						// the props, state and dirty-state.
						// when we are dealing with strict-equality we don't as the child could still
						// be dirtied see #3883
						c.props = newProps;
						c.state = c._nextState;
						c._bits &= ~COMPONENT_DIRTY;
					}

					newVNode._dom = oldVNode._dom;
					newVNode._children = oldVNode._children;
					newVNode._children.some(vnode => {
						if (vnode) vnode._parent = newVNode;
					});

					EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
					c._stateCallbacks = [];

					if (c._renderCallbacks.length) {
						commitQueue.push(c);
					}

					// Skip over the retained subtree without traversing it; the
					// `result` branch in diffChildren picks this up as the next
					// oldDom.
					oldDom = getDomSibling(oldVNode);

					break outer;
				}

				if (c.componentWillUpdate) {
					c.componentWillUpdate(newProps, c._nextState, componentContext);
				}

				if (isClassComponent && c.componentDidUpdate) {
					c._renderCallbacks.push(() => {
						c.componentDidUpdate(oldProps, oldState, snapshot);
					});
				}
			}

			c.context = componentContext;
			c.props = newProps;
			c._parentDom = parentDom;
			c._bits &= ~COMPONENT_FORCE;

			let renderHook = options._render,
				count = 0;
			if (isClassComponent) {
				c.state = c._nextState;
				c._bits &= ~COMPONENT_DIRTY;

				if (renderHook) renderHook(newVNode);

				tmp = c.render(c.props, c.state, c.context);

				EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
				c._stateCallbacks = [];
			} else {
				do {
					c._bits &= ~COMPONENT_DIRTY;
					if (renderHook) renderHook(newVNode);

					tmp = c.render(c.props, c.state, c.context);

					// Handle setState called in render, see #2553
					c.state = c._nextState;
				} while (c._bits & COMPONENT_DIRTY && ++count < 25);
			}

			// Handle setState called in render, see #2553
			c.state = c._nextState;

			if (c.getChildContext) {
				globalContext = assign({}, globalContext, c.getChildContext());
			}

			if (
				isClassComponent &&
				oldVNode._component &&
				c.getSnapshotBeforeUpdate
			) {
				snapshot = c.getSnapshotBeforeUpdate(oldProps, oldState);
			}

			const renderResult =
				tmp && tmp.type === Fragment && tmp.key == NULL
					? tmp.props.children
					: tmp;

			// A vnode carrying a `_parentDom` prop, considered a new root,
			// continues rendering into that container. The subtree must stay
			// invisible to the host tree's DOM bookkeeping: the portal vnode
			// keeps a `null` `_dom` and the host insertion cursor (`oldDom`)
			// passes through unchanged.
			// `tmp` (the raw render result, already unwrapped into renderResult)
			// doubles as the saved host insertion cursor while we render into
			// the portal's container.
			if (newProps._parentDom) {
				tmp = oldDom;
				parentDom = newProps._parentDom;
				// If we portal into a math or svg element we need
				// to swap the namespace (chart libraries often do this).
				// The document follows the container too (e.g. iframes) as
				// diffElementNodes derives it from its parentDom.
				namespace = parentDom.namespaceURI;
				// Portals are never server-rendered: hydration must not claim the
				// host parent's excess nodes for the container's children.
				isHydrating = excessDomChildren = NULL;

				// Changing the container remounts the children into the new one
				if (oldVNode.props && oldVNode.props._parentDom != parentDom) {
					/** @type {VNode[]} */ (oldVNode._children).some(child => {
						if (child) unmount(child, child);
					});
					oldVNode._children = NULL;
				}

				oldDom = oldVNode._children ? getDomSibling(oldVNode, 0) : NULL;
			}

			oldDom = diffChildren(
				parentDom,
				isArray(renderResult) ? renderResult : [renderResult],
				newVNode,
				oldVNode,
				globalContext,
				namespace,
				excessDomChildren,
				commitQueue,
				oldDom,
				isHydrating,
				refQueue
			);

			// When we exit a portal we
			// change up the oldDom
			if (newProps._parentDom) {
				newVNode._dom = NULL;
				oldDom = tmp;
			}

			// We successfully rendered this VNode, unset any stored hydration/bailout state:
			newVNode._flags &= RESET_MODE;
			if (oldVNode._flags & MODE_SUSPENDED) c._excess = NULL;

			// Remove the kept DOM this resumed render didn't claim
			if (resumed) resumed.some(removeNode);

			if (c._renderCallbacks.length) {
				commitQueue.push(c);
			}

			// Only clear when this render was the retry; PENDING_ERROR set by a
			// descendant during this render must survive until then.
			if (c._bits & COMPONENT_PROCESSING_EXCEPTION) {
				c._bits &= ~(COMPONENT_PROCESSING_EXCEPTION | COMPONENT_PENDING_ERROR);
			}
		} catch (e) {
			// We remove any componentDidMount, ...
			// that have been invalidated by us
			// intercepting the error.
			commitQueue.length = oldCommitQueueLength;
			newVNode._original = NULL;
			// if hydrating or creating initial tree, bailout preserves DOM:
			if (isHydrating || excessDomChildren) {
				if (e.then) {
					let commentMarkersToFind = 0,
						startMarker;

					newVNode._flags |= isHydrating
						? MODE_HYDRATE | MODE_SUSPENDED
						: MODE_SUSPENDED;

					if (excessDomChildren) {
						for (let i = 0; i < excessDomChildren.length; i++) {
							let child = excessDomChildren[i];
							if (!child) continue;

							if (child.nodeType == 8) {
								excessDomChildren[i] = NULL;
								if (child.data.startsWith('$s')) {
									if (!commentMarkersToFind++) startMarker = child;
								} else if (
									child.data.startsWith('/$s') &&
									!--commentMarkersToFind
								) {
									oldDom = child;
									break;
								}
							} else if (commentMarkersToFind) {
								excessDomChildren[i] = NULL;
							}
						}
					}

					if (!startMarker) {
						while (oldDom && oldDom.nodeType == 8 && oldDom.nextSibling) {
							oldDom = oldDom.nextSibling;
						}

						if (excessDomChildren) {
							excessDomChildren[excessDomChildren.indexOf(oldDom)] = NULL;
						}
						startMarker = oldDom;
					}
					// Store the start marker directly; children re-scanned on resume.
					// A re-suspension keeps the marker it originally started from.
					if (!newVNode._component._excess) {
						newVNode._component._excess = startMarker;
					}
					newVNode._dom = oldDom;
				} else if (excessDomChildren) {
					excessDomChildren.some(removeNode);
				}
			} else {
				newVNode._dom = oldVNode._dom;
			}

			if (!newVNode._children) {
				newVNode._children = oldVNode._children || [];
			}

			if (!e.then) markAsForce(newVNode);
			options._catchError(e, newVNode, oldVNode);
		}
	} else {
		oldDom = newVNode._dom = diffElementNodes(
			oldVNode._dom,
			newVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			isHydrating,
			refQueue,
			parentDom
		);
	}

	if ((tmp = options.diffed)) tmp(newVNode);

	return newVNode._flags & MODE_SUSPENDED ? UNDEFINED : oldDom;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	/** @type {any} */
	let tmp,
		resumed,
		newType = newVNode.type;

	// When passing through createElement it assigns the object
	// constructor as undefined. This to prevent JSON-injection.
	if (newVNode.constructor !== UNDEFINED) return NULL;

	// If the previous diff bailed out, resume creating/hydrating into the DOM
	// that was kept while suspended (server-rendered, or already in the
	// container we rendered into). `tmp` holds the stored excess node until the
	// options._diff call below.
	if (
		oldVNode._flags & MODE_SUSPENDED &&
		// @ts-expect-error This is MODE_HYDRATE or 0
		((isHydrating = oldVNode._flags & MODE_HYDRATE),
		(tmp = oldVNode._component._excess))
	) {
		newVNode._flags |= isHydrating;
		resumed = excessDomChildren = [];
		if (tmp.nodeType == 8) {
			// Re-scan DOM from stored start marker for streamed hydration.
			// `depth` only ever reaches 0 through the `break` below, so it
			// doesn't need to be re-tested in the loop condition.
			for (
				let depth = 1, node = tmp.nextSibling;
				node;
				node = node.nextSibling
			) {
				if (node.nodeType == 8) {
					if (node.data.startsWith('$s')) depth++;
					else if (node.data.startsWith('/$s') && !--depth) break;
				}
				excessDomChildren.push(node);
			}
		} else {
			excessDomChildren.push(tmp);
		}
		oldDom = excessDomChildren[0];
	}

	if ((tmp = options._diff)) tmp(newVNode);

	outer: if (typeof newType == 'function') {
		let oldCommitQueueLength = commitQueue.length;
		try {
			let c,
				oldProps,
				oldState,
				snapshot,
				newProps = newVNode.props;
			const isClassComponent = (tmp = newType.prototype) && tmp.render;

			// Necessary for createContext api. Setting this property will pass
			// the context value as `this.context` just for this component.
			tmp = newType.contextType;
			const provider = tmp && globalContext[tmp._id];
			const componentContext = tmp
				? provider
					? provider.props.value
					: tmp._defaultValue
				: globalContext;

			// Get component and set it to `c`
			if (oldVNode._component) {
				c = newVNode._component = oldVNode._component;
				if (c._bits & COMPONENT_PENDING_ERROR) {
					c._bits |= COMPONENT_PROCESSING_EXCEPTION;
				}
			} else {
				// Instantiate the new component
				if (isClassComponent) {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new newType(newProps, componentContext); // eslint-disable-line new-cap
				} else {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new BaseComponent(
						newProps,
						componentContext
					);

					c.constructor = newType;
					c.render = doRender;
				}
				if (provider) provider.sub(c);

				if (!c.state) c.state = {};
				c._globalContext = globalContext;
				c._bits |= COMPONENT_DIRTY;
				c._renderCallbacks = [];
				c._stateCallbacks = [];
			}

			if (isClassComponent) {
				if (!c._nextState) c._nextState = c.state;

				// Invoke getDerivedStateFromProps
				if (newType.getDerivedStateFromProps) {
					if (c._nextState == c.state) {
						c._nextState = assign({}, c._nextState);
					}

					assign(
						c._nextState,
						newType.getDerivedStateFromProps(newProps, c._nextState)
					);
				}
			}

			oldProps = c.props;
			oldState = c.state;
			c._vnode = newVNode;

			// Invoke pre-render lifecycle methods
			if (!oldVNode._component) {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					c.componentWillMount
				) {
					c.componentWillMount();
				}

				if (isClassComponent && c.componentDidMount) {
					c._renderCallbacks.push(c.componentDidMount);
				}
			} else {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					newProps !== oldProps &&
					c.componentWillReceiveProps
				) {
					c.componentWillReceiveProps(newProps, componentContext);
				}

				if (
					(newVNode._original == oldVNode._original &&
						!(c._bits & COMPONENT_DIRTY)) ||
					(!(c._bits & COMPONENT_FORCE) &&
						c.shouldComponentUpdate &&
						c.shouldComponentUpdate(
							newProps,
							c._nextState,
							componentContext
						) === false)
				) {
					// More info about this here: https://gist.github.com/JoviDeCroock/bec5f2ce93544d2e6070ef8e0036e4e8
					if (newVNode._original != oldVNode._original) {
						// When we are dealing with a bail because of sCU we have to update
						// the props, state and dirty-state.
						// when we are dealing with strict-equality we don't as the child could still
						// be dirtied see #3883
						c.props = newProps;
						c.state = c._nextState;
						c._bits &= ~COMPONENT_DIRTY;
					}

					newVNode._dom = oldVNode._dom;
					newVNode._children = oldVNode._children;
					newVNode._children.some(vnode => {
						if (vnode) vnode._parent = newVNode;
					});

					EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
					c._stateCallbacks = [];

					if (c._renderCallbacks.length) {
						commitQueue.push(c);
					}

					// Skip over the retained subtree without traversing it; the
					// `result` branch in diffChildren picks this up as the next
					// oldDom.
					oldDom = getDomSibling(oldVNode);

					break outer;
				}

				if (c.componentWillUpdate) {
					c.componentWillUpdate(newProps, c._nextState, componentContext);
				}

				if (isClassComponent && c.componentDidUpdate) {
					c._renderCallbacks.push(() => {
						c.componentDidUpdate(oldProps, oldState, snapshot);
					});
				}
			}

			c.context = componentContext;
			c.props = newProps;
			c._parentDom = parentDom;
			c._bits &= ~COMPONENT_FORCE;

			let renderHook = options._render,
				count = 0;
			if (isClassComponent) {
				c.state = c._nextState;
				c._bits &= ~COMPONENT_DIRTY;

				if (renderHook) renderHook(newVNode);

				tmp = c.render(c.props, c.state, c.context);

				EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
				c._stateCallbacks = [];
			} else {
				do {
					c._bits &= ~COMPONENT_DIRTY;
					if (renderHook) renderHook(newVNode);

					tmp = c.render(c.props, c.state, c.context);

					// Handle setState called in render, see #2553
					c.state = c._nextState;
				} while (c._bits & COMPONENT_DIRTY && ++count < 25);
			}

			// Handle setState called in render, see #2553
			c.state = c._nextState;

			if (c.getChildContext) {
				globalContext = assign({}, globalContext, c.getChildContext());
			}

			if (
				isClassComponent &&
				oldVNode._component &&
				c.getSnapshotBeforeUpdate
			) {
				snapshot = c.getSnapshotBeforeUpdate(oldProps, oldState);
			}

			const renderResult =
				tmp && tmp.type === Fragment && tmp.key == NULL
					? tmp.props.children
					: tmp;

			// A vnode carrying a `_parentDom` prop, considered a new root,
			// continues rendering into that container. The subtree must stay
			// invisible to the host tree's DOM bookkeeping: the portal vnode
			// keeps a `null` `_dom` and the host insertion cursor (`oldDom`)
			// passes through unchanged.
			// `tmp` (the raw render result, already unwrapped into renderResult)
			// doubles as the saved host insertion cursor while we render into
			// the portal's container.
			if (newProps._parentDom) {
				tmp = oldDom;
				parentDom = newProps._parentDom;
				// If we portal into a math or svg element we need
				// to swap the namespace (chart libraries often do this).
				// The document follows the container too (e.g. iframes) as
				// diffElementNodes derives it from its parentDom.
				namespace = parentDom.namespaceURI;
				// Portals are never server-rendered: hydration must not claim the
				// host parent's excess nodes for the container's children.
				isHydrating = excessDomChildren = NULL;

				// Changing the container remounts the children into the new one
				if (oldVNode.props && oldVNode.props._parentDom != parentDom) {
					/** @type {VNode[]} */ (oldVNode._children).some(child => {
						if (child) unmount(child, child);
					});
					oldVNode._children = NULL;
				}

				oldDom = oldVNode._children ? getDomSibling(oldVNode, 0) : NULL;
			}

			oldDom = diffChildren(
				parentDom,
				isArray(renderResult) ? renderResult : [renderResult],
				newVNode,
				oldVNode,
				globalContext,
				namespace,
				excessDomChildren,
				commitQueue,
				oldDom,
				isHydrating,
				refQueue
			);

			// When we exit a portal we
			// change up the oldDom
			if (newProps._parentDom) {
				newVNode._dom = NULL;
				oldDom = tmp;
			}

			// We successfully rendered this VNode, unset any stored hydration/bailout state:
			newVNode._flags &= RESET_MODE;
			if (oldVNode._flags & MODE_SUSPENDED) c._excess = NULL;

			// Remove the kept DOM this resumed render didn't claim
			if (resumed) resumed.some(removeNode);

			if (c._renderCallbacks.length) {
				commitQueue.push(c);
			}

			// Only clear when this render was the retry; PENDING_ERROR set by a
			// descendant during this render must survive until then.
			if (c._bits & COMPONENT_PROCESSING_EXCEPTION) {
				c._bits &= ~(COMPONENT_PROCESSING_EXCEPTION | COMPONENT_PENDING_ERROR);
			}
		} catch (e) {
			// We remove any componentDidMount, ...
			// that have been invalidated by us
			// intercepting the error.
			commitQueue.length = oldCommitQueueLength;
			newVNode._original = NULL;
			// if hydrating or creating initial tree, bailout preserves DOM:
			if (isHydrating || excessDomChildren) {
				if (e.then) {
					let commentMarkersToFind = 0,
						startMarker;

					newVNode._flags |= isHydrating
						? MODE_HYDRATE | MODE_SUSPENDED
						: MODE_SUSPENDED;

					if (excessDomChildren) {
						let i = excessDomChildren.indexOf(oldDom || UNDEFINED),
							child;
						if (!~i) i = excessDomChildren.length;

						// The cursor skips comments: step back to this component's markers.
						while ((child = excessDomChildren[i - 1]) && child.nodeType == 8) {
							i--;
						}

						for (; i < excessDomChildren.length; i++) {
							child = excessDomChildren[i];
							if (!child) continue;
							excessDomChildren[i] = NULL;

							if (child.nodeType == 8) {
								if (child.data.startsWith('$s')) {
									if (!commentMarkersToFind++) startMarker = child;
								} else if (
									commentMarkersToFind &&
									child.data.startsWith('/$s') &&
									!--commentMarkersToFind
								) {
									oldDom = child;
									break;
								}
							} else if (!commentMarkersToFind) {
								break;
							}
						}
					}

					if (!startMarker) {
						while (oldDom && oldDom.nodeType == 8 && oldDom.nextSibling) {
							oldDom = oldDom.nextSibling;
						}
						startMarker = oldDom;
					}
					// Store the start marker directly; children re-scanned on resume.
					// A re-suspension keeps the marker it originally started from.
					if (!newVNode._component._excess) {
						newVNode._component._excess = startMarker;
					}
					newVNode._dom = oldDom;
				} else if (excessDomChildren) {
					excessDomChildren.some(removeNode);
				}
			} else {
				newVNode._dom = oldVNode._dom;
			}

			if (!newVNode._children) {
				newVNode._children = oldVNode._children || [];
			}

			if (!e.then) markAsForce(newVNode);
			options._catchError(e, newVNode, oldVNode);
		}
	} else {
		oldDom = newVNode._dom = diffElementNodes(
			oldVNode._dom,
			newVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			isHydrating,
			refQueue,
			parentDom
		);
	}

	if ((tmp = options.diffed)) tmp(newVNode);

	return newVNode._flags & MODE_SUSPENDED ? UNDEFINED : oldDom;
}
```


---

### 🔹 Commit #04: `4b543501`
- **完整 Hash**: `4b5435017236dc0199f226cfc4af63dea54ee4d7`
- **說明 (Ground Truth)**: Drop component stack entries of renders that threw
- **變更檔案數**: 1

#### 📄 檔案: `debug/src/component-stack.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:20, E:11, A:0) ➔ After(N:23, E:12, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `oldCatchError (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `_catchError` (FUNCTION_DEF)
  • + [新增節點] `stackLevels` (MODULE_STATE)
  • + [新增呼叫邊] `_catchError` ──[CALLS]──> `oldCatchError (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `setupComponentStack()`
- **變更前簽章 (Before)**: `function setupComponentStack()` (L107~L149)
- **變更後簽章 (After)**: `function setupComponentStack()` (L114~L175)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function setupComponentStack() {
	let oldDiff = options._diff;
	let oldDiffed = options.diffed;
	let oldRoot = options._root;
	let oldVNode = options.vnode;
	let oldRender = options._render;

	options.diffed = vnode => {
		if (isPossibleOwner(vnode)) {
			ownerStack.pop();
		}
		renderStack.pop();
		if (oldDiffed) oldDiffed(vnode);
	};

	options._diff = vnode => {
		if (isPossibleOwner(vnode)) {
			renderStack.push(vnode);
		}
		if (oldDiff) oldDiff(vnode);
	};

	options._root = (vnode, parent) => {
		ownerStack = [];
		if (oldRoot) oldRoot(vnode, parent);
	};

	options.vnode = vnode => {
		ownerMap.set(
			vnode,
			ownerStack.length > 0 ? ownerStack[ownerStack.length - 1] : null
		);
		if (oldVNode) oldVNode(vnode);
	};

	options._render = vnode => {
		if (isPossibleOwner(vnode)) {
			ownerStack.push(vnode);
		}

		if (oldRender) oldRender(vnode);
	};
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function setupComponentStack() {
	let oldDiff = options._diff;
	let oldDiffed = options.diffed;
	let oldRoot = options._root;
	let oldVNode = options.vnode;
	let oldRender = options._render;
	let oldCatchError = options._catchError;

	options.diffed = vnode => {
		if (isPossibleOwner(vnode)) {
			ownerStack.pop();
		}
		renderStack.pop();
		if (oldDiffed) oldDiffed(vnode);
	};

	options._diff = vnode => {
		stackLevels.set(vnode, [renderStack.length, ownerStack.length]);
		if (isPossibleOwner(vnode)) {
			renderStack.push(vnode);
		}
		if (oldDiff) oldDiff(vnode);
	};

	options._catchError = (error, vnode, oldVNode, errorInfo) => {
		// Drop what the components below `vnode` pushed before throwing. `vnode`
		// keeps its own entries when the error is handled, as its `diffed` runs.
		const level = stackLevels.get(vnode);
		if (level) {
			renderStack.length = Math.min(
				renderStack.length,
				level[0] + (renderStack[level[0]] == vnode)
			);
			ownerStack.length = Math.min(
				ownerStack.length,
				level[1] + (ownerStack[level[1]] == vnode)
			);
		}
		oldCatchError(error, vnode, oldVNode, errorInfo);
	};

	options._root = (vnode, parent) => {
		ownerStack = [];
		if (oldRoot) oldRoot(vnode, parent);
	};

	options.vnode = vnode => {
		ownerMap.set(
			vnode,
			ownerStack.length > 0 ? ownerStack[ownerStack.length - 1] : null
		);
		if (oldVNode) oldVNode(vnode);
	};

	options._render = vnode => {
		if (isPossibleOwner(vnode)) {
			ownerStack.push(vnode);
		}

		if (oldRender) oldRender(vnode);
	};
}
```

### 🔹 函式: `_diff()`
- **變更前簽章 (Before)**: `_diff()` (L122~L127)
- **變更後簽章 (After)**: `_diff()` (L130~L136)

#### ◀️ 變更前實作碼 (Before Implementation):
```
vnode => {
		if (isPossibleOwner(vnode)) {
			renderStack.push(vnode);
		}
		if (oldDiff) oldDiff(vnode);
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
vnode => {
		stackLevels.set(vnode, [renderStack.length, ownerStack.length]);
		if (isPossibleOwner(vnode)) {
			renderStack.push(vnode);
		}
		if (oldDiff) oldDiff(vnode);
	}
```


---

### 🔹 Commit #05: `7a34d7f5`
- **完整 Hash**: `7a34d7f5a7e1dfc8ba1aca2dc0376803f9c4cc80`
- **說明 (Ground Truth)**: Log the component stack of errors no boundary handles
- **變更檔案數**: 1

#### 📄 檔案: `debug/src/debug.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:37, E:33, A:0) ➔ After(N:37, E:33, A:0)
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

### 🔹 函式: `initDebug()`
- **變更前簽章 (Before)**: `function initDebug()` (L64~L494)
- **變更後簽章 (After)**: `function initDebug()` (L64~L507)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function initDebug() {
	setupComponentStack();

	let hooksAllowed = false;

	/* eslint-disable no-console */
	let oldBeforeDiff = options._diff;
	let oldDiffed = options.diffed;
	let oldVnode = options.vnode;
	let oldRender = options._render;
	let oldCatchError = options._catchError;
	let oldRoot = options._root;
	let oldHook = options._hook;
	const warnedComponents = !isWeakMapSupported
		? null
		: {
				useEffect: new WeakMap(),
				useLayoutEffect: new WeakMap(),
				lazyPropTypes: new WeakMap()
			};
	const deprecations = [];

	options._catchError = (error, vnode, oldVNode, errorInfo) => {
		let component = vnode && vnode._component;
		if (component && typeof error.then == 'function') {
			const promise = error;
			error = new Error(
				`Missing Suspense. The throwing component was: ${getDisplayName(vnode)}`
			);

			let parent = vnode;
			for (; parent; parent = parent._parent) {
				if (parent._component && parent._component._childDidSuspend) {
					error = promise;
					break;
				}
			}

			// We haven't recovered and we know at this point that there is no
			// Suspense component higher up in the tree
			if (error instanceof Error) {
				throw error;
			}
		}

		errorInfo = errorInfo || {};
		errorInfo.componentStack = getOwnerStack(vnode);
		oldCatchError(error, vnode, oldVNode, errorInfo);

		// when an error was handled by an ErrorBoundary we still log it, matching what
		// React does in development. Errors that were not handled are rethrown by the
		// core and thus surface as regular uncaught errors.
		if (typeof error.then != 'function') {
			console.error(error);
		}
	};

	options._root = (vnode, parentNode) => {
		if (!parentNode) {
			throw new Error(
				'Undefined parent passed to render(), this is the second argument.\n' +
					'Check if the element is available in the DOM/has the correct id.'
			);
		}

		let isValid;
		switch (parentNode.nodeType) {
			case ELEMENT_NODE:
			case DOCUMENT_FRAGMENT_NODE:
			case DOCUMENT_NODE:
				isValid = true;
				break;
			default:
				isValid = false;
		}

		if (!isValid) {
			let componentName = getDisplayName(vnode);
			throw new Error(
				`Expected a valid HTML node as a second argument to render.	Received ${parentNode} instead: render(<${componentName} />, ${parentNode});`
			);
		}

		if (oldRoot) oldRoot(vnode, parentNode);
	};

	options._diff = vnode => {
		let { type } = vnode;

		hooksAllowed = true;

		if (type === undefined) {
			throw new Error(
				'Undefined component passed to createElement()\n\n' +
					'You likely forgot to export your component or might have mixed up default and named imports' +
					serializeVNode(vnode) +
					`\n\n${getOwnerStack(vnode)}`
			);
		} else if (type != null && typeof type == 'object') {
			if (type._children !== undefined && type._dom !== undefined) {
				throw new Error(
					`Invalid type passed to createElement(): ${type}\n\n` +
						'Did you accidentally pass a JSX literal as JSX twice?\n\n' +
						`  let My${getDisplayName(vnode)} = ${serializeVNode(type)};\n` +
						`  let vnode = <My${getDisplayName(vnode)} />;\n\n` +
						'This usually happens when you export a JSX literal and not the component.' +
						`\n\n${getOwnerStack(vnode)}`
				);
			}

			throw new Error(
				'Invalid type passed to createElement(): ' +
					(Array.isArray(type) ? 'array' : type)
			);
		}

		if (
			vnode.ref !== undefined &&
			typeof vnode.ref != 'function' &&
			typeof vnode.ref != 'object' &&
			!('$$typeof' in vnode) // allow string refs when preact-compat is installed
		) {
			throw new Error(
				`Component's "ref" property should be a function, or an object created ` +
					`by createRef(), but got [${typeof vnode.ref}] instead\n` +
					serializeVNode(vnode) +
					`\n\n${getOwnerStack(vnode)}`
			);
		}

		if (typeof vnode.type == 'string') {
			for (const key in vnode.props) {
				if (
					key[0] === 'o' &&
					key[1] === 'n' &&
					typeof vnode.props[key] != 'function' &&
					vnode.props[key] != null
				) {
					throw new Error(
						`Component's "${key}" property should be a function, ` +
							`but got [${typeof vnode.props[key]}] instead\n` +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				}
			}
		}

		// Check prop-types if available
		if (typeof vnode.type == 'function' && vnode.type.propTypes) {
			if (
				vnode.type.displayName === 'Lazy' &&
				warnedComponents &&
				!warnedComponents.lazyPropTypes.has(vnode.type)
			) {
				const m =
					'PropTypes are not supported on lazy(). Use propTypes on the wrapped component itself. ';
				try {
					const lazyVNode = vnode.type();
					warnedComponents.lazyPropTypes.set(vnode.type, true);
					console.warn(
						m + `Component wrapped in lazy() is ${getDisplayName(lazyVNode)}`
					);
				} catch (promise) {
					console.warn(
						m + "We will log the wrapped component's name once it is loaded."
					);
				}
			}

			/* eslint-disable-next-line */
			const { ref: _ref, ...props } = vnode.props;

			checkPropTypes(
				vnode.type.propTypes,
				props,
				'prop',
				getDisplayName(vnode),
				() => getOwnerStack(vnode)
			);
		}

		if (oldBeforeDiff) oldBeforeDiff(vnode);
	};

	let renderCount = 0;
	let currentComponent;
	options._render = vnode => {
		if (oldRender) {
			oldRender(vnode);
		}
		hooksAllowed = true;

		const nextComponent = vnode._component;
		if (nextComponent === currentComponent) {
			renderCount++;
		} else {
			renderCount = 1;
		}

		if (renderCount >= 25) {
			throw new Error(
				`Too many re-renders. This is limited to prevent an infinite loop ` +
					`which may lock up your browser. The component causing this is: ${getDisplayName(
						vnode
					)}`
			);
		}

		currentComponent = nextComponent;
	};

	options._hook = (comp, index, type) => {
		if (!comp || !hooksAllowed) {
			throw new Error('Hook can only be invoked from render methods.');
		}

		if (oldHook) oldHook(comp, index, type);
	};

	// Ideally we'd want to print a warning once per component, but we
	// don't have access to the vnode that triggered it here. As a
	// compromise and to avoid flooding the console with warnings we
	// print each deprecation warning only once.
	const warn = (property, message) => ({
		get() {
			const key = 'get' + property + message;
			if (deprecations && deprecations.indexOf(key) < 0) {
				deprecations.push(key);
				console.warn(`getting vnode.${property} is deprecated, ${message}`);
			}
		},
		set() {
			const key = 'set' + property + message;
			if (deprecations && deprecations.indexOf(key) < 0) {
				deprecations.push(key);
				console.warn(`setting vnode.${property} is not allowed, ${message}`);
			}
		}
	});

	const deprecatedAttributes = {
		nodeName: warn('nodeName', 'use vnode.type'),
		attributes: warn('attributes', 'use vnode.props'),
		children: warn('children', 'use vnode.props.children')
	};

	const deprecatedProto = Object.create({}, deprecatedAttributes);

	options.vnode = vnode => {
		const props = vnode.props;
		if (
			vnode.type !== null &&
			props != null &&
			('__source' in props || '__self' in props)
		) {
			const newProps = (vnode.props = {});
			for (let i in props) {
				const v = props[i];
				if (i === '__source') vnode.__source = v;
				else if (i === '__self') vnode.__self = v;
				else newProps[i] = v;
			}
		}

		// eslint-disable-next-line
		vnode.__proto__ = deprecatedProto;
		if (oldVnode) oldVnode(vnode);
	};

	options.diffed = vnode => {
		const { type, _parent: parent } = vnode;
		// Check if the user passed plain objects as children. Note that we cannot
		// move this check into `options.vnode` because components can receive
		// children in any shape they want (e.g.
		// `<MyJSONFormatter>{{ foo: 123, bar: "abc" }}</MyJSONFormatter>`).
		// Putting this check in `options.diffed` ensures that
		// `vnode._children` is set and that we only validate the children
		// that were actually rendered.
		if (vnode._children) {
			vnode._children.forEach(child => {
				if (typeof child === 'object' && child && child.type === undefined) {
					const keys = Object.keys(child).join(',');
					throw new Error(
						`Objects are not valid as a child. Encountered an object with the keys {${keys}}.` +
							`\n\n${getOwnerStack(vnode)}`
					);
				}
			});
		}

		if (vnode._component === currentComponent) {
			renderCount = 0;
		}

		if (
			typeof type === 'string' &&
			(isTableElement(type) ||
				type === 'p' ||
				type === 'a' ||
				type === 'button')
		) {
			// Avoid false positives when Preact only partially rendered the
			// HTML tree. Whilst we attempt to include the outer DOM in our
			// validation, this wouldn't work on the server for
			// `preact-render-to-string`. There we'd otherwise flood the terminal
			// with false positives, which we'd like to avoid.
			let domParentName = getClosestDomNodeParentName(parent);
			if (domParentName !== '' && isTableElement(type)) {
				if (
					type === 'table' &&
					// Tables can be nested inside each other if it's inside a cell.
					// See https://developer.mozilla.org/en-US/docs/Learn/HTML/Tables/Advanced#nesting_tables
					domParentName !== 'td' &&
					isTableElement(domParentName)
				) {
					console.error(
						'Improper nesting of table. Your <table> should not have a table-node parent.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				} else if (
					(type === 'thead' || type === 'tfoot' || type === 'tbody') &&
					domParentName !== 'table'
				) {
					console.error(
						'Improper nesting of table. Your <thead/tbody/tfoot> should have a <table> parent.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				} else if (
					type === 'tr' &&
					domParentName !== 'thead' &&
					domParentName !== 'tfoot' &&
					domParentName !== 'tbody'
				) {
					console.error(
						'Improper nesting of table. Your <tr> should have a <thead/tbody/tfoot> parent.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				} else if (type === 'td' && domParentName !== 'tr') {
					console.error(
						'Improper nesting of table. Your <td> should have a <tr> parent.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				} else if (type === 'th' && domParentName !== 'tr') {
					console.error(
						'Improper nesting of table. Your <th> should have a <tr>.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				}
			} else if (type === 'p') {
				let illegalDomChildrenTypes = getDomChildren(vnode).filter(childType =>
					ILLEGAL_PARAGRAPH_CHILD_ELEMENTS.test(childType)
				);
				if (illegalDomChildrenTypes.length) {
					console.error(
						'Improper nesting of paragraph. Your <p> should not have ' +
							illegalDomChildrenTypes.join(', ') +
							' as child-elements.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				}
			} else if (type === 'a' || type === 'button') {
				if (getDomChildren(vnode).indexOf(type) !== -1) {
					console.error(
						`Improper nesting of interactive content. Your <${type}>` +
							` should not have other ${type === 'a' ? 'anchor' : 'button'}` +
							' tags as child-elements.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				}
			}
		}

		hooksAllowed = false;

		if (oldDiffed) oldDiffed(vnode);

		if (vnode._children != null) {
			const keys = [];
			for (let i = 0; i < vnode._children.length; i++) {
				const child = vnode._children[i];
				if (!child || child.key == null) continue;

				const key = child.key;
				if (keys.indexOf(key) !== -1) {
					console.error(
						'Following component has two or more children with the ' +
							`same key attribute: "${key}". This may cause glitches and misbehavior ` +
							'in rendering process. Component: \n\n' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);

					// Break early to not spam the console
					break;
				}

				keys.push(key);
			}
		}

		if (vnode._component != null && vnode._component.__hooks != null) {
			// Validate that none of the hooks in this component contain arguments that are NaN.
			// This is a common mistake that can be hard to debug, so we want to catch it early.
			const hooks = vnode._component.__hooks._list;
			if (hooks) {
				for (let i = 0; i < hooks.length; i += 1) {
					const hook = hooks[i];
					if (hook._args) {
						for (let j = 0; j < hook._args.length; j++) {
							const arg = hook._args[j];
							if (isNaN(arg)) {
								const componentName = getDisplayName(vnode);
								console.warn(
									`Invalid argument passed to hook. Hooks should not be called with NaN in the dependency array. Hook index ${i} in component ${componentName} was called with NaN.`
								);
							}
						}
					}
				}
			}
		}
	};
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function initDebug() {
	setupComponentStack();

	let hooksAllowed = false;

	/* eslint-disable no-console */
	let oldBeforeDiff = options._diff;
	let oldDiffed = options.diffed;
	let oldVnode = options.vnode;
	let oldRender = options._render;
	let oldCatchError = options._catchError;
	let oldRoot = options._root;
	let oldHook = options._hook;
	const warnedComponents = !isWeakMapSupported
		? null
		: {
				useEffect: new WeakMap(),
				useLayoutEffect: new WeakMap(),
				lazyPropTypes: new WeakMap()
			};
	const deprecations = [];
	let lastUncaughtError;

	options._catchError = (error, vnode, oldVNode, errorInfo) => {
		let component = vnode && vnode._component;
		if (component && typeof error.then == 'function') {
			const promise = error;
			error = new Error(
				`Missing Suspense. The throwing component was: ${getDisplayName(vnode)}`
			);

			let parent = vnode;
			for (; parent; parent = parent._parent) {
				if (parent._component && parent._component._childDidSuspend) {
					error = promise;
					break;
				}
			}

			// We haven't recovered and we know at this point that there is no
			// Suspense component higher up in the tree
			if (error instanceof Error) {
				throw error;
			}
		}

		errorInfo = errorInfo || {};
		errorInfo.componentStack = getOwnerStack(vnode);
		try {
			oldCatchError(error, vnode, oldVNode, errorInfo);
		} catch (e) {
			// Nothing handled the error. Its own stack only points into Preact, so
			// say which component it came from before it escapes.
			if (e !== lastUncaughtError) {
				lastUncaughtError = e;
				console.error(
					`An error occurred in the <${getDisplayName(vnode)}> component, and no error boundary handled it.\n\n${errorInfo.componentStack}`
				);
			}
			throw e;
		}

		// when an error was handled by an ErrorBoundary we still log it, matching what
		// React does in development. Errors that were not handled are rethrown by the
		// core and thus surface as regular uncaught errors.
		if (typeof error.then != 'function') {
			console.error(error);
		}
	};

	options._root = (vnode, parentNode) => {
		if (!parentNode) {
			throw new Error(
				'Undefined parent passed to render(), this is the second argument.\n' +
					'Check if the element is available in the DOM/has the correct id.'
			);
		}

		let isValid;
		switch (parentNode.nodeType) {
			case ELEMENT_NODE:
			case DOCUMENT_FRAGMENT_NODE:
			case DOCUMENT_NODE:
				isValid = true;
				break;
			default:
				isValid = false;
		}

		if (!isValid) {
			let componentName = getDisplayName(vnode);
			throw new Error(
				`Expected a valid HTML node as a second argument to render.	Received ${parentNode} instead: render(<${componentName} />, ${parentNode});`
			);
		}

		if (oldRoot) oldRoot(vnode, parentNode);
	};

	options._diff = vnode => {
		let { type } = vnode;

		hooksAllowed = true;

		if (type === undefined) {
			throw new Error(
				'Undefined component passed to createElement()\n\n' +
					'You likely forgot to export your component or might have mixed up default and named imports' +
					serializeVNode(vnode) +
					`\n\n${getOwnerStack(vnode)}`
			);
		} else if (type != null && typeof type == 'object') {
			if (type._children !== undefined && type._dom !== undefined) {
				throw new Error(
					`Invalid type passed to createElement(): ${type}\n\n` +
						'Did you accidentally pass a JSX literal as JSX twice?\n\n' +
						`  let My${getDisplayName(vnode)} = ${serializeVNode(type)};\n` +
						`  let vnode = <My${getDisplayName(vnode)} />;\n\n` +
						'This usually happens when you export a JSX literal and not the component.' +
						`\n\n${getOwnerStack(vnode)}`
				);
			}

			throw new Error(
				'Invalid type passed to createElement(): ' +
					(Array.isArray(type) ? 'array' : type)
			);
		}

		if (
			vnode.ref !== undefined &&
			typeof vnode.ref != 'function' &&
			typeof vnode.ref != 'object' &&
			!('$$typeof' in vnode) // allow string refs when preact-compat is installed
		) {
			throw new Error(
				`Component's "ref" property should be a function, or an object created ` +
					`by createRef(), but got [${typeof vnode.ref}] instead\n` +
					serializeVNode(vnode) +
					`\n\n${getOwnerStack(vnode)}`
			);
		}

		if (typeof vnode.type == 'string') {
			for (const key in vnode.props) {
				if (
					key[0] === 'o' &&
					key[1] === 'n' &&
					typeof vnode.props[key] != 'function' &&
					vnode.props[key] != null
				) {
					throw new Error(
						`Component's "${key}" property should be a function, ` +
							`but got [${typeof vnode.props[key]}] instead\n` +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				}
			}
		}

		// Check prop-types if available
		if (typeof vnode.type == 'function' && vnode.type.propTypes) {
			if (
				vnode.type.displayName === 'Lazy' &&
				warnedComponents &&
				!warnedComponents.lazyPropTypes.has(vnode.type)
			) {
				const m =
					'PropTypes are not supported on lazy(). Use propTypes on the wrapped component itself. ';
				try {
					const lazyVNode = vnode.type();
					warnedComponents.lazyPropTypes.set(vnode.type, true);
					console.warn(
						m + `Component wrapped in lazy() is ${getDisplayName(lazyVNode)}`
					);
				} catch (promise) {
					console.warn(
						m + "We will log the wrapped component's name once it is loaded."
					);
				}
			}

			/* eslint-disable-next-line */
			const { ref: _ref, ...props } = vnode.props;

			checkPropTypes(
				vnode.type.propTypes,
				props,
				'prop',
				getDisplayName(vnode),
				() => getOwnerStack(vnode)
			);
		}

		if (oldBeforeDiff) oldBeforeDiff(vnode);
	};

	let renderCount = 0;
	let currentComponent;
	options._render = vnode => {
		if (oldRender) {
			oldRender(vnode);
		}
		hooksAllowed = true;

		const nextComponent = vnode._component;
		if (nextComponent === currentComponent) {
			renderCount++;
		} else {
			renderCount = 1;
		}

		if (renderCount >= 25) {
			throw new Error(
				`Too many re-renders. This is limited to prevent an infinite loop ` +
					`which may lock up your browser. The component causing this is: ${getDisplayName(
						vnode
					)}`
			);
		}

		currentComponent = nextComponent;
	};

	options._hook = (comp, index, type) => {
		if (!comp || !hooksAllowed) {
			throw new Error('Hook can only be invoked from render methods.');
		}

		if (oldHook) oldHook(comp, index, type);
	};

	// Ideally we'd want to print a warning once per component, but we
	// don't have access to the vnode that triggered it here. As a
	// compromise and to avoid flooding the console with warnings we
	// print each deprecation warning only once.
	const warn = (property, message) => ({
		get() {
			const key = 'get' + property + message;
			if (deprecations && deprecations.indexOf(key) < 0) {
				deprecations.push(key);
				console.warn(`getting vnode.${property} is deprecated, ${message}`);
			}
		},
		set() {
			const key = 'set' + property + message;
			if (deprecations && deprecations.indexOf(key) < 0) {
				deprecations.push(key);
				console.warn(`setting vnode.${property} is not allowed, ${message}`);
			}
		}
	});

	const deprecatedAttributes = {
		nodeName: warn('nodeName', 'use vnode.type'),
		attributes: warn('attributes', 'use vnode.props'),
		children: warn('children', 'use vnode.props.children')
	};

	const deprecatedProto = Object.create({}, deprecatedAttributes);

	options.vnode = vnode => {
		const props = vnode.props;
		if (
			vnode.type !== null &&
			props != null &&
			('__source' in props || '__self' in props)
		) {
			const newProps = (vnode.props = {});
			for (let i in props) {
				const v = props[i];
				if (i === '__source') vnode.__source = v;
				else if (i === '__self') vnode.__self = v;
				else newProps[i] = v;
			}
		}

		// eslint-disable-next-line
		vnode.__proto__ = deprecatedProto;
		if (oldVnode) oldVnode(vnode);
	};

	options.diffed = vnode => {
		const { type, _parent: parent } = vnode;
		// Check if the user passed plain objects as children. Note that we cannot
		// move this check into `options.vnode` because components can receive
		// children in any shape they want (e.g.
		// `<MyJSONFormatter>{{ foo: 123, bar: "abc" }}</MyJSONFormatter>`).
		// Putting this check in `options.diffed` ensures that
		// `vnode._children` is set and that we only validate the children
		// that were actually rendered.
		if (vnode._children) {
			vnode._children.forEach(child => {
				if (typeof child === 'object' && child && child.type === undefined) {
					const keys = Object.keys(child).join(',');
					throw new Error(
						`Objects are not valid as a child. Encountered an object with the keys {${keys}}.` +
							`\n\n${getOwnerStack(vnode)}`
					);
				}
			});
		}

		if (vnode._component === currentComponent) {
			renderCount = 0;
		}

		if (
			typeof type === 'string' &&
			(isTableElement(type) ||
				type === 'p' ||
				type === 'a' ||
				type === 'button')
		) {
			// Avoid false positives when Preact only partially rendered the
			// HTML tree. Whilst we attempt to include the outer DOM in our
			// validation, this wouldn't work on the server for
			// `preact-render-to-string`. There we'd otherwise flood the terminal
			// with false positives, which we'd like to avoid.
			let domParentName = getClosestDomNodeParentName(parent);
			if (domParentName !== '' && isTableElement(type)) {
				if (
					type === 'table' &&
					// Tables can be nested inside each other if it's inside a cell.
					// See https://developer.mozilla.org/en-US/docs/Learn/HTML/Tables/Advanced#nesting_tables
					domParentName !== 'td' &&
					isTableElement(domParentName)
				) {
					console.error(
						'Improper nesting of table. Your <table> should not have a table-node parent.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				} else if (
					(type === 'thead' || type === 'tfoot' || type === 'tbody') &&
					domParentName !== 'table'
				) {
					console.error(
						'Improper nesting of table. Your <thead/tbody/tfoot> should have a <table> parent.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				} else if (
					type === 'tr' &&
					domParentName !== 'thead' &&
					domParentName !== 'tfoot' &&
					domParentName !== 'tbody'
				) {
					console.error(
						'Improper nesting of table. Your <tr> should have a <thead/tbody/tfoot> parent.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				} else if (type === 'td' && domParentName !== 'tr') {
					console.error(
						'Improper nesting of table. Your <td> should have a <tr> parent.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				} else if (type === 'th' && domParentName !== 'tr') {
					console.error(
						'Improper nesting of table. Your <th> should have a <tr>.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				}
			} else if (type === 'p') {
				let illegalDomChildrenTypes = getDomChildren(vnode).filter(childType =>
					ILLEGAL_PARAGRAPH_CHILD_ELEMENTS.test(childType)
				);
				if (illegalDomChildrenTypes.length) {
					console.error(
						'Improper nesting of paragraph. Your <p> should not have ' +
							illegalDomChildrenTypes.join(', ') +
							' as child-elements.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				}
			} else if (type === 'a' || type === 'button') {
				if (getDomChildren(vnode).indexOf(type) !== -1) {
					console.error(
						`Improper nesting of interactive content. Your <${type}>` +
							` should not have other ${type === 'a' ? 'anchor' : 'button'}` +
							' tags as child-elements.' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);
				}
			}
		}

		hooksAllowed = false;

		if (oldDiffed) oldDiffed(vnode);

		if (vnode._children != null) {
			const keys = [];
			for (let i = 0; i < vnode._children.length; i++) {
				const child = vnode._children[i];
				if (!child || child.key == null) continue;

				const key = child.key;
				if (keys.indexOf(key) !== -1) {
					console.error(
						'Following component has two or more children with the ' +
							`same key attribute: "${key}". This may cause glitches and misbehavior ` +
							'in rendering process. Component: \n\n' +
							serializeVNode(vnode) +
							`\n\n${getOwnerStack(vnode)}`
					);

					// Break early to not spam the console
					break;
				}

				keys.push(key);
			}
		}

		if (vnode._component != null && vnode._component.__hooks != null) {
			// Validate that none of the hooks in this component contain arguments that are NaN.
			// This is a common mistake that can be hard to debug, so we want to catch it early.
			const hooks = vnode._component.__hooks._list;
			if (hooks) {
				for (let i = 0; i < hooks.length; i += 1) {
					const hook = hooks[i];
					if (hook._args) {
						for (let j = 0; j < hook._args.length; j++) {
							const arg = hook._args[j];
							if (isNaN(arg)) {
								const componentName = getDisplayName(vnode);
								console.warn(
									`Invalid argument passed to hook. Hooks should not be called with NaN in the dependency array. Hook index ${i} in component ${componentName} was called with NaN.`
								);
							}
						}
					}
				}
			}
		}
	};
}
```

### 🔹 函式: `_catchError()`
- **變更前簽章 (Before)**: `_catchError(error, vnode, oldVNode, errorInfo)` (L86~L119)
- **變更後簽章 (After)**: `_catchError(error, vnode, oldVNode, errorInfo)` (L87~L132)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(error, vnode, oldVNode, errorInfo) => {
		let component = vnode && vnode._component;
		if (component && typeof error.then == 'function') {
			const promise = error;
			error = new Error(
				`Missing Suspense. The throwing component was: ${getDisplayName(vnode)}`
			);

			let parent = vnode;
			for (; parent; parent = parent._parent) {
				if (parent._component && parent._component._childDidSuspend) {
					error = promise;
					break;
				}
			}

			// We haven't recovered and we know at this point that there is no
			// Suspense component higher up in the tree
			if (error instanceof Error) {
				throw error;
			}
		}

		errorInfo = errorInfo || {};
		errorInfo.componentStack = getOwnerStack(vnode);
		oldCatchError(error, vnode, oldVNode, errorInfo);

		// when an error was handled by an ErrorBoundary we still log it, matching what
		// React does in development. Errors that were not handled are rethrown by the
		// core and thus surface as regular uncaught errors.
		if (typeof error.then != 'function') {
			console.error(error);
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(error, vnode, oldVNode, errorInfo) => {
		let component = vnode && vnode._component;
		if (component && typeof error.then == 'function') {
			const promise = error;
			error = new Error(
				`Missing Suspense. The throwing component was: ${getDisplayName(vnode)}`
			);

			let parent = vnode;
			for (; parent; parent = parent._parent) {
				if (parent._component && parent._component._childDidSuspend) {
					error = promise;
					break;
				}
			}

			// We haven't recovered and we know at this point that there is no
			// Suspense component higher up in the tree
			if (error instanceof Error) {
				throw error;
			}
		}

		errorInfo = errorInfo || {};
		errorInfo.componentStack = getOwnerStack(vnode);
		try {
			oldCatchError(error, vnode, oldVNode, errorInfo);
		} catch (e) {
			// Nothing handled the error. Its own stack only points into Preact, so
			// say which component it came from before it escapes.
			if (e !== lastUncaughtError) {
				lastUncaughtError = e;
				console.error(
					`An error occurred in the <${getDisplayName(vnode)}> component, and no error boundary handled it.\n\n${errorInfo.componentStack}`
				);
			}
			throw e;
		}

		// when an error was handled by an ErrorBoundary we still log it, matching what
		// React does in development. Errors that were not handled are rethrown by the
		// core and thus surface as regular uncaught errors.
		if (typeof error.then != 'function') {
			console.error(error);
		}
	}
```


---

### 🔹 Commit #06: `e25c22d6`
- **完整 Hash**: `e25c22d694ba4e185a6c8818c9305e06f4aa9a7d`
- **說明 (Ground Truth)**: Resolve the ref owner inside applyRef
- **變更檔案數**: 2

#### 📄 檔案: `src/diff/children.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:12, E:14, A:0) ➔ After(N:12, E:14, A:0)
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

### 🔹 函式: `diffChildren()`
- **變更前簽章 (Before)**: `function diffChildren(
	parentDom,
	renderResult,
	newParentVNode,
	oldParentVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L45~L160)
- **變更後簽章 (After)**: `function diffChildren(
	parentDom,
	renderResult,
	newParentVNode,
	oldParentVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L45~L155)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function diffChildren(
	parentDom,
	renderResult,
	newParentVNode,
	oldParentVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	let i,
		/** @type {VNode} */
		oldVNode,
		/** @type {VNode} */
		childVNode,
		/** @type {PreactElement} */
		newDom,
		/** @type {PreactElement} */
		firstChildDom;

	// This is a compression of oldParentVNode != EMPTY_OBJ && oldParentVNode._children || EMPTY_ARR
	// as EMPTY_OBJ._children should be `undefined`. Callers always pass at
	// least EMPTY_OBJ, so a null check isn't needed.
	/** @type {VNode[]} */
	let oldChildren = oldParentVNode._children || EMPTY_ARR;

	let newChildrenLength = renderResult.length;

	oldDom = constructNewChildrenArray(
		newParentVNode,
		renderResult,
		oldChildren,
		oldDom,
		newChildrenLength
	);

	for (i = 0; i < newChildrenLength; i++) {
		childVNode = newParentVNode._children[i];
		if (childVNode == NULL) continue;

		// At this point, constructNewChildrenArray has assigned _index to be the
		// matchingIndex for this VNode's oldVNode (or -1 if there is no oldVNode).
		// ~_index guards the -1 case: a negative array index is a named property
		// access which V8 can't serve from the fast elements path.
		oldVNode =
			(~childVNode._index && oldChildren[childVNode._index]) || EMPTY_OBJ;

		// Update childVNode._index to its final index
		childVNode._index = i;

		// Morph the old element into the new one, but don't append it to the dom yet
		let result = diff(
			parentDom,
			childVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			oldDom,
			isHydrating,
			refQueue
		);

		// Adjust DOM nodes
		newDom = childVNode._dom;
		// A ref detached while its subtree was parked by Suspense is attached
		// again on reveal.
		if (
			childVNode.ref &&
			(oldVNode.ref != childVNode.ref || oldVNode._flags & REF_DETACHED)
		) {
			if (oldVNode.ref != childVNode.ref && oldVNode.ref) {
				applyRef(
					oldVNode.ref,
					NULL,
					childVNode,
					oldVNode._component || oldVNode._dom
				);
			}
			refQueue.push(
				childVNode.ref,
				childVNode._component || newDom,
				childVNode
			);
		}

		firstChildDom = firstChildDom || newDom;

		if (childVNode._flags & INSERT_VNODE) {
			oldDom = insert(childVNode, oldDom, parentDom, !oldVNode._original);

			// When a matched VNode is physically moved via INSERT_VNODE, its old
			// _dom pointer becomes a stale positional reference. Clear it so that
			// getDomSibling (called from nested diffs) won't return this stale
			// reference and mis-place subsequent DOM nodes. See #5065.
			if (oldVNode._dom) {
				oldVNode._dom = NULL;
			}
		} else if (typeof childVNode.type == 'function' && result !== UNDEFINED) {
			oldDom = result;
		} else if (newDom) {
			oldDom = newDom.nextSibling;
		}

		// Unset diffing flags
		childVNode._flags &= ~(INSERT_VNODE | MATCHED);
	}

	newParentVNode._dom = firstChildDom;

	return oldDom;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function diffChildren(
	parentDom,
	renderResult,
	newParentVNode,
	oldParentVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	let i,
		/** @type {VNode} */
		oldVNode,
		/** @type {VNode} */
		childVNode,
		/** @type {PreactElement} */
		newDom,
		/** @type {PreactElement} */
		firstChildDom;

	// This is a compression of oldParentVNode != EMPTY_OBJ && oldParentVNode._children || EMPTY_ARR
	// as EMPTY_OBJ._children should be `undefined`. Callers always pass at
	// least EMPTY_OBJ, so a null check isn't needed.
	/** @type {VNode[]} */
	let oldChildren = oldParentVNode._children || EMPTY_ARR;

	let newChildrenLength = renderResult.length;

	oldDom = constructNewChildrenArray(
		newParentVNode,
		renderResult,
		oldChildren,
		oldDom,
		newChildrenLength
	);

	for (i = 0; i < newChildrenLength; i++) {
		childVNode = newParentVNode._children[i];
		if (childVNode == NULL) continue;

		// At this point, constructNewChildrenArray has assigned _index to be the
		// matchingIndex for this VNode's oldVNode (or -1 if there is no oldVNode).
		// ~_index guards the -1 case: a negative array index is a named property
		// access which V8 can't serve from the fast elements path.
		oldVNode =
			(~childVNode._index && oldChildren[childVNode._index]) || EMPTY_OBJ;

		// Update childVNode._index to its final index
		childVNode._index = i;

		// Morph the old element into the new one, but don't append it to the dom yet
		let result = diff(
			parentDom,
			childVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			oldDom,
			isHydrating,
			refQueue
		);

		// Adjust DOM nodes
		newDom = childVNode._dom;
		// A ref detached while its subtree was parked by Suspense is attached
		// again on reveal.
		if (
			childVNode.ref &&
			(oldVNode.ref != childVNode.ref || oldVNode._flags & REF_DETACHED)
		) {
			if (oldVNode.ref != childVNode.ref && oldVNode.ref) {
				applyRef(oldVNode.ref, NULL, childVNode, oldVNode);
			}
			refQueue.push(
				childVNode.ref,
				childVNode._component || newDom,
				childVNode
			);
		}

		firstChildDom = firstChildDom || newDom;

		if (childVNode._flags & INSERT_VNODE) {
			oldDom = insert(childVNode, oldDom, parentDom, !oldVNode._original);

			// When a matched VNode is physically moved via INSERT_VNODE, its old
			// _dom pointer becomes a stale positional reference. Clear it so that
			// getDomSibling (called from nested diffs) won't return this stale
			// reference and mis-place subsequent DOM nodes. See #5065.
			if (oldVNode._dom) {
				oldVNode._dom = NULL;
			}
		} else if (typeof childVNode.type == 'function' && result !== UNDEFINED) {
			oldDom = result;
		} else if (newDom) {
			oldDom = newDom.nextSibling;
		}

		// Unset diffing flags
		childVNode._flags &= ~(INSERT_VNODE | MATCHED);
	}

	newParentVNode._dom = firstChildDom;

	return oldDom;
}
```


#### 📄 檔案: `src/diff/index.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:17, E:19, A:0) ➔ After(N:17, E:19, A:0)
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

### 🔹 函式: `applyRef()`
- **變更前簽章 (Before)**: `function applyRef(ref, value, vnode, owner)` (L730~L746)
- **變更後簽章 (After)**: `function applyRef(ref, value, vnode, owner)` (L730~L749)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function applyRef(ref, value, vnode, owner) {
	try {
		if (typeof ref == 'function') {
			if (value) {
				// Store the cleanup on the element or component rather than on the
				// ref function, which can be shared between several of them
				value._refCleanup = ref(value);
			} else if (owner && typeof owner._refCleanup == 'function') {
				value = owner._refCleanup;
				owner._refCleanup = NULL;
				value();
			} else ref(NULL);
		} else ref.current = value;
	} catch (e) {
		options._catchError(e, vnode);
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function applyRef(ref, value, vnode, owner) {
	try {
		if (typeof ref == 'function') {
			// Store the cleanup on the element or component rather than on the
			// ref function, which can be shared between several of them
			if (value) value._refCleanup = ref(value);
			else if (
				owner &&
				(owner = owner._component || owner._dom) &&
				typeof owner._refCleanup == 'function'
			) {
				value = owner._refCleanup;
				owner._refCleanup = NULL;
				value();
			} else ref(value);
		} else ref.current = value;
	} catch (e) {
		options._catchError(e, vnode);
	}
}
```

### 🔹 函式: `unmount()`
- **變更前簽章 (Before)**: `function unmount(vnode, parentVNode, skipRemove)` (L755~L797)
- **變更後簽章 (After)**: `function unmount(vnode, parentVNode, skipRemove)` (L758~L800)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function unmount(vnode, parentVNode, skipRemove) {
	let r;
	if (options.unmount) options.unmount(vnode);

	if ((r = vnode.ref) && (!r.current || r.current == vnode._dom)) {
		applyRef(r, NULL, parentVNode, vnode._component || vnode._dom);
	}

	if ((r = vnode._component)) {
		if (r.componentWillUnmount) {
			try {
				r.componentWillUnmount();
			} catch (e) {
				options._catchError(e, parentVNode);
			}
		}

		r._parentDom = r._globalContext = NULL;
	}

	if ((r = vnode._children)) {
		for (let i = 0; i < r.length; i++) {
			if (r[i]) {
				unmount(
					r[i],
					parentVNode,
					// A portal's children live in another container, so a removed
					// host ancestor doesn't detach them; always remove them.
					typeof vnode.type == 'function'
						? skipRemove && !vnode.props._parentDom
						: true
				);
			}
		}
	}

	if ((r = vnode._dom)) {
		if (!skipRemove) removeNode(r);
		if (r._listeners) r._listeners = NULL;
	}

	vnode._dom = vnode._component = vnode._parent = NULL;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function unmount(vnode, parentVNode, skipRemove) {
	let r;
	if (options.unmount) options.unmount(vnode);

	if ((r = vnode.ref) && (!r.current || r.current == vnode._dom)) {
		applyRef(r, NULL, parentVNode, vnode);
	}

	if ((r = vnode._component)) {
		if (r.componentWillUnmount) {
			try {
				r.componentWillUnmount();
			} catch (e) {
				options._catchError(e, parentVNode);
			}
		}

		r._parentDom = r._globalContext = NULL;
	}

	if ((r = vnode._children)) {
		for (let i = 0; i < r.length; i++) {
			if (r[i]) {
				unmount(
					r[i],
					parentVNode,
					// A portal's children live in another container, so a removed
					// host ancestor doesn't detach them; always remove them.
					typeof vnode.type == 'function'
						? skipRemove && !vnode.props._parentDom
						: true
				);
			}
		}
	}

	if ((r = vnode._dom)) {
		if (!skipRemove) removeNode(r);
		if (r._listeners) r._listeners = NULL;
	}

	vnode._dom = vnode._component = vnode._parent = NULL;
}
```


---

### 🔹 Commit #07: `db2092b0`
- **完整 Hash**: `db2092b02361678d3e8b929682e131409c35b2e1`
- **說明 (Ground Truth)**: Keep ref cleanups on the element instead of the ref function
- **變更檔案數**: 2

#### 📄 檔案: `src/diff/children.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:12, E:14, A:0) ➔ After(N:12, E:14, A:0)
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

### 🔹 函式: `diffChildren()`
- **變更前簽章 (Before)**: `function diffChildren(
	parentDom,
	renderResult,
	newParentVNode,
	oldParentVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L45~L155)
- **變更後簽章 (After)**: `function diffChildren(
	parentDom,
	renderResult,
	newParentVNode,
	oldParentVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L45~L160)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function diffChildren(
	parentDom,
	renderResult,
	newParentVNode,
	oldParentVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	let i,
		/** @type {VNode} */
		oldVNode,
		/** @type {VNode} */
		childVNode,
		/** @type {PreactElement} */
		newDom,
		/** @type {PreactElement} */
		firstChildDom;

	// This is a compression of oldParentVNode != EMPTY_OBJ && oldParentVNode._children || EMPTY_ARR
	// as EMPTY_OBJ._children should be `undefined`. Callers always pass at
	// least EMPTY_OBJ, so a null check isn't needed.
	/** @type {VNode[]} */
	let oldChildren = oldParentVNode._children || EMPTY_ARR;

	let newChildrenLength = renderResult.length;

	oldDom = constructNewChildrenArray(
		newParentVNode,
		renderResult,
		oldChildren,
		oldDom,
		newChildrenLength
	);

	for (i = 0; i < newChildrenLength; i++) {
		childVNode = newParentVNode._children[i];
		if (childVNode == NULL) continue;

		// At this point, constructNewChildrenArray has assigned _index to be the
		// matchingIndex for this VNode's oldVNode (or -1 if there is no oldVNode).
		// ~_index guards the -1 case: a negative array index is a named property
		// access which V8 can't serve from the fast elements path.
		oldVNode =
			(~childVNode._index && oldChildren[childVNode._index]) || EMPTY_OBJ;

		// Update childVNode._index to its final index
		childVNode._index = i;

		// Morph the old element into the new one, but don't append it to the dom yet
		let result = diff(
			parentDom,
			childVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			oldDom,
			isHydrating,
			refQueue
		);

		// Adjust DOM nodes
		newDom = childVNode._dom;
		// A ref detached while its subtree was parked by Suspense is attached
		// again on reveal.
		if (
			childVNode.ref &&
			(oldVNode.ref != childVNode.ref || oldVNode._flags & REF_DETACHED)
		) {
			if (oldVNode.ref != childVNode.ref && oldVNode.ref) {
				applyRef(oldVNode.ref, NULL, childVNode);
			}
			refQueue.push(
				childVNode.ref,
				childVNode._component || newDom,
				childVNode
			);
		}

		firstChildDom = firstChildDom || newDom;

		if (childVNode._flags & INSERT_VNODE) {
			oldDom = insert(childVNode, oldDom, parentDom, !oldVNode._original);

			// When a matched VNode is physically moved via INSERT_VNODE, its old
			// _dom pointer becomes a stale positional reference. Clear it so that
			// getDomSibling (called from nested diffs) won't return this stale
			// reference and mis-place subsequent DOM nodes. See #5065.
			if (oldVNode._dom) {
				oldVNode._dom = NULL;
			}
		} else if (typeof childVNode.type == 'function' && result !== UNDEFINED) {
			oldDom = result;
		} else if (newDom) {
			oldDom = newDom.nextSibling;
		}

		// Unset diffing flags
		childVNode._flags &= ~(INSERT_VNODE | MATCHED);
	}

	newParentVNode._dom = firstChildDom;

	return oldDom;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function diffChildren(
	parentDom,
	renderResult,
	newParentVNode,
	oldParentVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	let i,
		/** @type {VNode} */
		oldVNode,
		/** @type {VNode} */
		childVNode,
		/** @type {PreactElement} */
		newDom,
		/** @type {PreactElement} */
		firstChildDom;

	// This is a compression of oldParentVNode != EMPTY_OBJ && oldParentVNode._children || EMPTY_ARR
	// as EMPTY_OBJ._children should be `undefined`. Callers always pass at
	// least EMPTY_OBJ, so a null check isn't needed.
	/** @type {VNode[]} */
	let oldChildren = oldParentVNode._children || EMPTY_ARR;

	let newChildrenLength = renderResult.length;

	oldDom = constructNewChildrenArray(
		newParentVNode,
		renderResult,
		oldChildren,
		oldDom,
		newChildrenLength
	);

	for (i = 0; i < newChildrenLength; i++) {
		childVNode = newParentVNode._children[i];
		if (childVNode == NULL) continue;

		// At this point, constructNewChildrenArray has assigned _index to be the
		// matchingIndex for this VNode's oldVNode (or -1 if there is no oldVNode).
		// ~_index guards the -1 case: a negative array index is a named property
		// access which V8 can't serve from the fast elements path.
		oldVNode =
			(~childVNode._index && oldChildren[childVNode._index]) || EMPTY_OBJ;

		// Update childVNode._index to its final index
		childVNode._index = i;

		// Morph the old element into the new one, but don't append it to the dom yet
		let result = diff(
			parentDom,
			childVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			oldDom,
			isHydrating,
			refQueue
		);

		// Adjust DOM nodes
		newDom = childVNode._dom;
		// A ref detached while its subtree was parked by Suspense is attached
		// again on reveal.
		if (
			childVNode.ref &&
			(oldVNode.ref != childVNode.ref || oldVNode._flags & REF_DETACHED)
		) {
			if (oldVNode.ref != childVNode.ref && oldVNode.ref) {
				applyRef(
					oldVNode.ref,
					NULL,
					childVNode,
					oldVNode._component || oldVNode._dom
				);
			}
			refQueue.push(
				childVNode.ref,
				childVNode._component || newDom,
				childVNode
			);
		}

		firstChildDom = firstChildDom || newDom;

		if (childVNode._flags & INSERT_VNODE) {
			oldDom = insert(childVNode, oldDom, parentDom, !oldVNode._original);

			// When a matched VNode is physically moved via INSERT_VNODE, its old
			// _dom pointer becomes a stale positional reference. Clear it so that
			// getDomSibling (called from nested diffs) won't return this stale
			// reference and mis-place subsequent DOM nodes. See #5065.
			if (oldVNode._dom) {
				oldVNode._dom = NULL;
			}
		} else if (typeof childVNode.type == 'function' && result !== UNDEFINED) {
			oldDom = result;
		} else if (newDom) {
			oldDom = newDom.nextSibling;
		}

		// Unset diffing flags
		childVNode._flags &= ~(INSERT_VNODE | MATCHED);
	}

	newParentVNode._dom = firstChildDom;

	return oldDom;
}
```


#### 📄 檔案: `src/diff/index.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:16, E:18, A:0) ➔ After(N:17, E:19, A:0)
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
  • + [新增節點] `value (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `applyRef` ──[CALLS [guard: (typeof ref == 'function')]]──> `value (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `applyRef()`
- **變更前簽章 (Before)**: `function applyRef(ref, value, vnode)` (L729~L746)
- **變更後簽章 (After)**: `function applyRef(ref, value, vnode, owner)` (L730~L746)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function applyRef(ref, value, vnode) {
	try {
		if (typeof ref == 'function') {
			if (typeof ref._unmount == 'function') {
				ref._unmount();
			}

			if (typeof ref._unmount != 'function' || value) {
				// Store the cleanup function on the function
				// instance object itself to avoid shape
				// transitioning vnode
				ref._unmount = ref(value);
			}
		} else ref.current = value;
	} catch (e) {
		options._catchError(e, vnode);
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function applyRef(ref, value, vnode, owner) {
	try {
		if (typeof ref == 'function') {
			if (value) {
				// Store the cleanup on the element or component rather than on the
				// ref function, which can be shared between several of them
				value._refCleanup = ref(value);
			} else if (owner && typeof owner._refCleanup == 'function') {
				value = owner._refCleanup;
				owner._refCleanup = NULL;
				value();
			} else ref(NULL);
		} else ref.current = value;
	} catch (e) {
		options._catchError(e, vnode);
	}
}
```

### 🔹 函式: `unmount()`
- **變更前簽章 (Before)**: `function unmount(vnode, parentVNode, skipRemove)` (L755~L797)
- **變更後簽章 (After)**: `function unmount(vnode, parentVNode, skipRemove)` (L755~L797)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function unmount(vnode, parentVNode, skipRemove) {
	let r;
	if (options.unmount) options.unmount(vnode);

	if ((r = vnode.ref) && (!r.current || r.current == vnode._dom)) {
		applyRef(r, NULL, parentVNode);
	}

	if ((r = vnode._component)) {
		if (r.componentWillUnmount) {
			try {
				r.componentWillUnmount();
			} catch (e) {
				options._catchError(e, parentVNode);
			}
		}

		r._parentDom = r._globalContext = NULL;
	}

	if ((r = vnode._children)) {
		for (let i = 0; i < r.length; i++) {
			if (r[i]) {
				unmount(
					r[i],
					parentVNode,
					// A portal's children live in another container, so a removed
					// host ancestor doesn't detach them; always remove them.
					typeof vnode.type == 'function'
						? skipRemove && !vnode.props._parentDom
						: true
				);
			}
		}
	}

	if ((r = vnode._dom)) {
		if (!skipRemove) removeNode(r);
		if (r._listeners) r._listeners = NULL;
	}

	vnode._dom = vnode._component = vnode._parent = NULL;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function unmount(vnode, parentVNode, skipRemove) {
	let r;
	if (options.unmount) options.unmount(vnode);

	if ((r = vnode.ref) && (!r.current || r.current == vnode._dom)) {
		applyRef(r, NULL, parentVNode, vnode._component || vnode._dom);
	}

	if ((r = vnode._component)) {
		if (r.componentWillUnmount) {
			try {
				r.componentWillUnmount();
			} catch (e) {
				options._catchError(e, parentVNode);
			}
		}

		r._parentDom = r._globalContext = NULL;
	}

	if ((r = vnode._children)) {
		for (let i = 0; i < r.length; i++) {
			if (r[i]) {
				unmount(
					r[i],
					parentVNode,
					// A portal's children live in another container, so a removed
					// host ancestor doesn't detach them; always remove them.
					typeof vnode.type == 'function'
						? skipRemove && !vnode.props._parentDom
						: true
				);
			}
		}
	}

	if ((r = vnode._dom)) {
		if (!skipRemove) removeNode(r);
		if (r._listeners) r._listeners = NULL;
	}

	vnode._dom = vnode._component = vnode._parent = NULL;
}
```


---

### 🔹 Commit #08: `884080eb`
- **完整 Hash**: `884080eb2b71d6a1076e29d7e85cdcbf858a7a97`
- **說明 (Ground Truth)**: Finish act() cleanup when the leftover render queue throws
- **變更檔案數**: 1

#### 📄 檔案: `test-utils/src/index.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:11, E:7, A:0) ➔ After(N:11, E:7, A:0)
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

### 🔹 函式: `act()`
- **變更前簽章 (Before)**: `function act(cb)` (L27~L112)
- **變更後簽章 (After)**: `function act(cb)` (L27~L120)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function act(cb) {
	if (++actDepth > 1) {
		// If calls to `act` are nested, a flush happens only when the
		// outermost call returns. In the inner call, we just execute the
		// callback and return since the infrastructure for flushing has already
		// been set up.
		//
		// If an exception occurs, the outermost `act` will handle cleanup.
		try {
			const result = cb();
			if (isThenable(result)) {
				return result.then(
					() => {
						--actDepth;
					},
					e => {
						--actDepth;
						throw e;
					}
				);
			}
		} catch (e) {
			--actDepth;
			throw e;
		}
		--actDepth;
		return Promise.resolve();
	}

	const previousRequestAnimationFrame = options.requestAnimationFrame;
	const rerender = setupRerender();

	/** @type {() => void} */
	let flushes = [],
		toFlush;

	// Override requestAnimationFrame so we can flush pending hooks.
	options.requestAnimationFrame = fc => flushes.push(fc);

	const finish = () => {
		try {
			rerender();
			while (flushes.length) {
				toFlush = flushes;
				flushes = [];

				toFlush.forEach(x => x());
				rerender();
			}
		} catch (e) {
			if (!err) {
				err = e;
			}
		} finally {
			teardown();
		}

		options.requestAnimationFrame = previousRequestAnimationFrame;
		--actDepth;
	};

	let err;
	let result;

	try {
		result = cb();
	} catch (e) {
		err = e;
	}

	if (isThenable(result)) {
		return result.then(finish, err => {
			finish();
			throw err;
		});
	}

	// nb. If the callback is synchronous, effects must be flushed before
	// `act` returns, so that the caller does not have to await the result,
	// even though React recommends this.
	finish();
	if (err) {
		throw err;
	}
	return Promise.resolve();
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function act(cb) {
	if (++actDepth > 1) {
		// If calls to `act` are nested, a flush happens only when the
		// outermost call returns. In the inner call, we just execute the
		// callback and return since the infrastructure for flushing has already
		// been set up.
		//
		// If an exception occurs, the outermost `act` will handle cleanup.
		try {
			const result = cb();
			if (isThenable(result)) {
				return result.then(
					() => {
						--actDepth;
					},
					e => {
						--actDepth;
						throw e;
					}
				);
			}
		} catch (e) {
			--actDepth;
			throw e;
		}
		--actDepth;
		return Promise.resolve();
	}

	const previousRequestAnimationFrame = options.requestAnimationFrame;
	const rerender = setupRerender();

	/** @type {() => void} */
	let flushes = [],
		toFlush;

	// Override requestAnimationFrame so we can flush pending hooks.
	options.requestAnimationFrame = fc => flushes.push(fc);

	const finish = () => {
		try {
			rerender();
			while (flushes.length) {
				toFlush = flushes;
				flushes = [];

				toFlush.forEach(x => x());
				rerender();
			}
		} catch (e) {
			if (!err) {
				err = e;
			}
		}

		// A failed render leaves the rest of the render queue for `teardown` to
		// drain, which can throw too.
		try {
			teardown();
		} catch (e) {
			if (!err) {
				err = e;
			}
		}

		options.requestAnimationFrame = previousRequestAnimationFrame;
		--actDepth;
	};

	let err;
	let result;

	try {
		result = cb();
	} catch (e) {
		err = e;
	}

	if (isThenable(result)) {
		return result.then(finish, err => {
			finish();
			throw err;
		});
	}

	// nb. If the callback is synchronous, effects must be flushed before
	// `act` returns, so that the caller does not have to await the result,
	// even though React recommends this.
	finish();
	if (err) {
		throw err;
	}
	return Promise.resolve();
}
```

### 🔹 函式: `finish()`
- **變更前簽章 (Before)**: `finish()` (L66~L86)
- **變更後簽章 (After)**: `finish()` (L66~L94)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
		try {
			rerender();
			while (flushes.length) {
				toFlush = flushes;
				flushes = [];

				toFlush.forEach(x => x());
				rerender();
			}
		} catch (e) {
			if (!err) {
				err = e;
			}
		} finally {
			teardown();
		}

		options.requestAnimationFrame = previousRequestAnimationFrame;
		--actDepth;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
		try {
			rerender();
			while (flushes.length) {
				toFlush = flushes;
				flushes = [];

				toFlush.forEach(x => x());
				rerender();
			}
		} catch (e) {
			if (!err) {
				err = e;
			}
		}

		// A failed render leaves the rest of the render queue for `teardown` to
		// drain, which can throw too.
		try {
			teardown();
		} catch (e) {
			if (!err) {
				err = e;
			}
		}

		options.requestAnimationFrame = previousRequestAnimationFrame;
		--actDepth;
	}
```

### 🔹 函式: `teardown()`
- **變更前簽章 (Before)**: `function teardown()` (L117~L130)
- **變更後簽章 (After)**: `function teardown()` (L125~L141)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function teardown() {
	if (options.__test__drainQueue) {
		// Flush any pending updates leftover by test
		options.__test__drainQueue();
		delete options.__test__drainQueue;
	}

	if (typeof options.__test__previousDebounce != 'undefined') {
		options.debounceRendering = options.__test__previousDebounce;
		delete options.__test__previousDebounce;
	} else {
		options.debounceRendering = undefined;
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function teardown() {
	try {
		if (options.__test__drainQueue) {
			// Flush any pending updates leftover by test
			options.__test__drainQueue();
		}
	} finally {
		delete options.__test__drainQueue;

		if (typeof options.__test__previousDebounce != 'undefined') {
			options.debounceRendering = options.__test__previousDebounce;
			delete options.__test__previousDebounce;
		} else {
			options.debounceRendering = undefined;
		}
	}
}
```


---

### 🔹 Commit #09: `0ebd1b6c`
- **完整 Hash**: `0ebd1b6c6a0e0d9c16a263a656b6e7a910c39f0f`
- **說明 (Ground Truth)**: Make PureComponent tree-shakeable and fix the _unmounted mangle collision
- **變更檔案數**: 4

#### 📄 檔案: `compat/src/PureComponent.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:3, E:1, A:0) ➔ After(N:5, E:1, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 1, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `PureComponent` (FUNCTION_DEF)
  • + [新增節點] `createPureComponent` (FUNCTION_DEF)
  • + [新增節點] `PureComponent` (MODULE_STATE)
  • - [移除節點] `PureComponent` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `shouldComponentUpdate()`
- **變更前簽章 (Before)**: `shouldComponentUpdate(props, state)` (L14~L16)
- **變更後簽章 (After)**: `shouldComponentUpdate(props, state)` (L16~L20)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (props, state) {
	return shallowDiffers(this.props, props) || shallowDiffers(this.state, state);
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (props, state) {
		return (
			shallowDiffers(this.props, props) || shallowDiffers(this.state, state)
		);
	}
```


#### 📄 檔案: `compat/src/index.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:15, E:6, A:0) ➔ After(N:14, E:6, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `isElement` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `compat/src/render.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:44, E:20, A:0) ➔ After(N:44, E:20, A:0)
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

### 🔹 函式: `IS_DOM()`
- **變更前簽章 (Before)**: `[Module State] IS_DOM` (L32~L32)
- **變更後簽章 (After)**: `[Module State] IS_DOM` (L32~L32)

#### ◀️ 變更前實作碼 (Before Implementation):
```
IS_DOM = typeof document != 'undefined'
```

#### ▶️ 變更後實作碼 (After Implementation):
```
IS_DOM = typeof document < 'u'
```


#### 📄 檔案: `compat/src/suspense.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:21, E:13, A:1) ➔ After(N:21, E:13, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 5, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#detachedParent** `(Control)`
    └── 🎯 [CALLS] `createSuspense()`
        └── 🎯 [CALLS] `initSuspenseHooks()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `initSuspenseHooks()`
- **變更前簽章 (Before)**: `function initSuspenseHooks()` (L11~L44)
- **變更後簽章 (After)**: `function initSuspenseHooks()` (L11~L43)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function initSuspenseHooks() {
	const oldCatchError = options._catchError;
	options._catchError = (error, newVNode, oldVNode, errorInfo) => {
		if (error.then) {
			/** @type {import('./internal').Component} */
			let component;
			let vnode = newVNode;

			while ((vnode = vnode._parent)) {
				if ((component = vnode._component) && component._childDidSuspend) {
					// A component that suspends before ever committing has no state
					// worth keeping; mounted ones keep their hooks while parked.
					if (oldVNode && !oldVNode._component)
						newVNode._component.__hooks = UNDEFINED;
					// Don't call oldCatchError if we found a Suspense
					return component._childDidSuspend(error, newVNode);
				}
			}
		}
		oldCatchError(error, newVNode, oldVNode, errorInfo);
	};

	const oldUnmount = options.unmount;
	options.unmount = vnode => {
		/** @type {import('./internal').Component} */
		const component = vnode._component;
		if (component) component._unmounted = true;
		if (component && component._onResolve) {
			component._onResolve();
		}

		if (oldUnmount) oldUnmount(vnode);
	};
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function initSuspenseHooks() {
	const oldCatchError = options._catchError;
	options._catchError = (error, newVNode, oldVNode, errorInfo) => {
		if (error.then) {
			/** @type {import('./internal').Component} */
			let component;
			let vnode = newVNode;

			while ((vnode = vnode._parent)) {
				if ((component = vnode._component) && component._childDidSuspend) {
					// A component that suspends before ever committing has no state
					// worth keeping; mounted ones keep their hooks while parked.
					if (oldVNode && !oldVNode._component)
						newVNode._component.__hooks = UNDEFINED;
					// Don't call oldCatchError if we found a Suspense
					return component._childDidSuspend(error, newVNode);
				}
			}
		}
		oldCatchError(error, newVNode, oldVNode, errorInfo);
	};

	const oldUnmount = options.unmount;
	options.unmount = vnode => {
		/** @type {import('./internal').Component} */
		const component = vnode._component;
		if (component && component._onResolve) {
			component._onResolve();
		}

		if (oldUnmount) oldUnmount(vnode);
	};
}
```

### 🔹 函式: `_childDidSuspend()`
- **變更前簽章 (Before)**: `_childDidSuspend(promise, suspendingVNode)` (L137~L201)
- **變更後簽章 (After)**: `_childDidSuspend(promise, suspendingVNode)` (L136~L201)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (promise, suspendingVNode) {
		const suspendingComponent = suspendingVNode._component;

		if (this._suspenders == null) {
			this._suspenders = [];
		}
		this._suspenders.push(suspendingComponent);

		let resolved = false;
		const onResolved = () => {
			if (resolved || this._unmounted) return;

			resolved = true;
			suspendingComponent._onResolve = null;

			onSuspensionComplete();
		};

		suspendingComponent._onResolve = onResolved;

		// Store and null _parentDom to prevent setState/forceUpdate from
		// scheduling renders while suspended. Render would be a no-op anyway
		// since renderComponent checks _parentDom, but this avoids queue churn.
		const originalParentDom = suspendingComponent._parentDom;
		suspendingComponent._parentDom = null;

		const onSuspensionComplete = () => {
			if (!--this._pendingSuspensionCount) {
				// If the suspension was during hydration we don't need to restore the
				// suspended children into the _children array
				if (this.state._suspended) {
					const suspendedVNode = this.state._suspended;
					this._vnode._children[0] = removeOriginal(
						suspendedVNode,
						suspendedVNode._component._parentDom,
						suspendedVNode._component._originalParentDom
					);
				}

				this.setState({ _suspended: (this._detachOnNextRender = null) });

				let suspended;
				while ((suspended = this._suspenders.pop())) {
					// Restore _parentDom before forceUpdate so render can proceed
					suspended._parentDom = originalParentDom;
					suspended.forceUpdate();
				}
			}
		};

		/**
		 * We do not set `suspended: true` during hydration because we want the actual markup
		 * to remain on screen and hydrate it when the suspense actually gets resolved.
		 * While in non-hydration cases the usual fallback -> component flow would occour.
		 */
		if (
			!this._pendingSuspensionCount++ &&
			!(suspendingVNode._flags & MODE_HYDRATE)
		) {
			this.setState({
				_suspended: (this._detachOnNextRender = this._vnode._children[0])
			});
		}
		promise.then(onResolved, onResolved);
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (promise, suspendingVNode) {
		const suspendingComponent = suspendingVNode._component;

		if (this._suspenders == null) {
			this._suspenders = [];
		}
		this._suspenders.push(suspendingComponent);

		let resolved = false;
		const onResolved = () => {
			// Core nulls `_parentDom` when the boundary unmounts.
			if (resolved || !this._parentDom) return;

			resolved = true;
			suspendingComponent._onResolve = null;

			onSuspensionComplete();
		};

		suspendingComponent._onResolve = onResolved;

		// Store and null _parentDom to prevent setState/forceUpdate from
		// scheduling renders while suspended. Render would be a no-op anyway
		// since renderComponent checks _parentDom, but this avoids queue churn.
		const originalParentDom = suspendingComponent._parentDom;
		suspendingComponent._parentDom = null;

		const onSuspensionComplete = () => {
			if (!--this._pendingSuspensionCount) {
				// If the suspension was during hydration we don't need to restore the
				// suspended children into the _children array
				if (this.state._suspended) {
					const suspendedVNode = this.state._suspended;
					this._vnode._children[0] = removeOriginal(
						suspendedVNode,
						suspendedVNode._component._parentDom,
						suspendedVNode._component._originalParentDom
					);
				}

				this.setState({ _suspended: (this._detachOnNextRender = null) });

				let suspended;
				while ((suspended = this._suspenders.pop())) {
					// Restore _parentDom before forceUpdate so render can proceed
					suspended._parentDom = originalParentDom;
					suspended.forceUpdate();
				}
			}
		};

		/**
		 * We do not set `suspended: true` during hydration because we want the actual markup
		 * to remain on screen and hydrate it when the suspense actually gets resolved.
		 * While in non-hydration cases the usual fallback -> component flow would occour.
		 */
		if (
			!this._pendingSuspensionCount++ &&
			!(suspendingVNode._flags & MODE_HYDRATE)
		) {
			this.setState({
				_suspended: (this._detachOnNextRender = this._vnode._children[0])
			});
		}
		promise.then(onResolved, onResolved);
	}
```

### 🔹 函式: `unmount()`
- **變更前簽章 (Before)**: `unmount()` (L34~L43)
- **變更後簽章 (After)**: `unmount()` (L34~L42)

#### ◀️ 變更前實作碼 (Before Implementation):
```
vnode => {
		/** @type {import('./internal').Component} */
		const component = vnode._component;
		if (component) component._unmounted = true;
		if (component && component._onResolve) {
			component._onResolve();
		}

		if (oldUnmount) oldUnmount(vnode);
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
vnode => {
		/** @type {import('./internal').Component} */
		const component = vnode._component;
		if (component && component._onResolve) {
			component._onResolve();
		}

		if (oldUnmount) oldUnmount(vnode);
	}
```

### 🔹 函式: `onResolved()`
- **變更前簽章 (Before)**: `onResolved()` (L146~L153)
- **變更後簽章 (After)**: `onResolved()` (L145~L153)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
			if (resolved || this._unmounted) return;

			resolved = true;
			suspendingComponent._onResolve = null;

			onSuspensionComplete();
		}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
			// Core nulls `_parentDom` when the boundary unmounts.
			if (resolved || !this._parentDom) return;

			resolved = true;
			suspendingComponent._onResolve = null;

			onSuspensionComplete();
		}
```

### 🔹 函式: `createSuspense()`
- **變更前簽章 (Before)**: `function createSuspense()` (L117~L237)
- **變更後簽章 (After)**: `function createSuspense()` (L116~L237)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createSuspense() {
	initSuspenseHooks();

	function Suspense() {
		// we do not call super here to golf some bytes...
		this._pendingSuspensionCount = 0;
		this._suspenders = null;
		this._detachOnNextRender = null;
	}

	// Things we do here to save some bytes but are not proper JS inheritance:
	// - call `new Component()` as the prototype
	// - do not set `Suspense.prototype.constructor` to `Suspense`
	Suspense.prototype = new Component();

	/**
	 * @this {import('./internal').SuspenseComponent}
	 * @param {Promise} promise The thrown promise
	 * @param {import('./internal').VNode<any, any>} suspendingVNode The suspending component
	 */
	Suspense.prototype._childDidSuspend = function (promise, suspendingVNode) {
		const suspendingComponent = suspendingVNode._component;

		if (this._suspenders == null) {
			this._suspenders = [];
		}
		this._suspenders.push(suspendingComponent);

		let resolved = false;
		const onResolved = () => {
			if (resolved || this._unmounted) return;

			resolved = true;
			suspendingComponent._onResolve = null;

			onSuspensionComplete();
		};

		suspendingComponent._onResolve = onResolved;

		// Store and null _parentDom to prevent setState/forceUpdate from
		// scheduling renders while suspended. Render would be a no-op anyway
		// since renderComponent checks _parentDom, but this avoids queue churn.
		const originalParentDom = suspendingComponent._parentDom;
		suspendingComponent._parentDom = null;

		const onSuspensionComplete = () => {
			if (!--this._pendingSuspensionCount) {
				// If the suspension was during hydration we don't need to restore the
				// suspended children into the _children array
				if (this.state._suspended) {
					const suspendedVNode = this.state._suspended;
					this._vnode._children[0] = removeOriginal(
						suspendedVNode,
						suspendedVNode._component._parentDom,
						suspendedVNode._component._originalParentDom
					);
				}

				this.setState({ _suspended: (this._detachOnNextRender = null) });

				let suspended;
				while ((suspended = this._suspenders.pop())) {
					// Restore _parentDom before forceUpdate so render can proceed
					suspended._parentDom = originalParentDom;
					suspended.forceUpdate();
				}
			}
		};

		/**
		 * We do not set `suspended: true` during hydration because we want the actual markup
		 * to remain on screen and hydrate it when the suspense actually gets resolved.
		 * While in non-hydration cases the usual fallback -> component flow would occour.
		 */
		if (
			!this._pendingSuspensionCount++ &&
			!(suspendingVNode._flags & MODE_HYDRATE)
		) {
			this.setState({
				_suspended: (this._detachOnNextRender = this._vnode._children[0])
			});
		}
		promise.then(onResolved, onResolved);
	};

	Suspense.prototype.componentWillUnmount = function () {
		this._suspenders = [];
	};

	/**
	 * @this {import('./internal').SuspenseComponent}
	 * @param {import('./internal').SuspenseComponent["props"]} props
	 * @param {import('./internal').SuspenseState} state
	 */
	Suspense.prototype.render = function (props, state) {
		if (this._detachOnNextRender) {
			// When the Suspense's _vnode was created by a call to createVNode
			// (i.e. due to a setState further up in the tree)
			// it's _children prop is null, in this case we "forget" about the parked vnodes to detach
			if (this._vnode._children) {
				const detachedParent = document.createElement('div');
				const detachedComponent = this._vnode._children[0]._component;
				this._vnode._children[0] = detachedClone(
					this._detachOnNextRender,
					detachedParent,
					(detachedComponent._originalParentDom = detachedComponent._parentDom)
				);
			}

			this._detachOnNextRender = null;
		}

		return [
			createElement(Fragment, null, state._suspended ? null : props.children),
			state._suspended && createElement(Fragment, null, props.fallback)
		];
	};

	return Suspense;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createSuspense() {
	initSuspenseHooks();

	function Suspense() {
		// we do not call super here to golf some bytes...
		this._pendingSuspensionCount = 0;
		this._suspenders = null;
		this._detachOnNextRender = null;
	}

	// Things we do here to save some bytes but are not proper JS inheritance:
	// - call `new Component()` as the prototype
	// - do not set `Suspense.prototype.constructor` to `Suspense`
	Suspense.prototype = new Component();

	/**
	 * @this {import('./internal').SuspenseComponent}
	 * @param {Promise} promise The thrown promise
	 * @param {import('./internal').VNode<any, any>} suspendingVNode The suspending component
	 */
	Suspense.prototype._childDidSuspend = function (promise, suspendingVNode) {
		const suspendingComponent = suspendingVNode._component;

		if (this._suspenders == null) {
			this._suspenders = [];
		}
		this._suspenders.push(suspendingComponent);

		let resolved = false;
		const onResolved = () => {
			// Core nulls `_parentDom` when the boundary unmounts.
			if (resolved || !this._parentDom) return;

			resolved = true;
			suspendingComponent._onResolve = null;

			onSuspensionComplete();
		};

		suspendingComponent._onResolve = onResolved;

		// Store and null _parentDom to prevent setState/forceUpdate from
		// scheduling renders while suspended. Render would be a no-op anyway
		// since renderComponent checks _parentDom, but this avoids queue churn.
		const originalParentDom = suspendingComponent._parentDom;
		suspendingComponent._parentDom = null;

		const onSuspensionComplete = () => {
			if (!--this._pendingSuspensionCount) {
				// If the suspension was during hydration we don't need to restore the
				// suspended children into the _children array
				if (this.state._suspended) {
					const suspendedVNode = this.state._suspended;
					this._vnode._children[0] = removeOriginal(
						suspendedVNode,
						suspendedVNode._component._parentDom,
						suspendedVNode._component._originalParentDom
					);
				}

				this.setState({ _suspended: (this._detachOnNextRender = null) });

				let suspended;
				while ((suspended = this._suspenders.pop())) {
					// Restore _parentDom before forceUpdate so render can proceed
					suspended._parentDom = originalParentDom;
					suspended.forceUpdate();
				}
			}
		};

		/**
		 * We do not set `suspended: true` during hydration because we want the actual markup
		 * to remain on screen and hydrate it when the suspense actually gets resolved.
		 * While in non-hydration cases the usual fallback -> component flow would occour.
		 */
		if (
			!this._pendingSuspensionCount++ &&
			!(suspendingVNode._flags & MODE_HYDRATE)
		) {
			this.setState({
				_suspended: (this._detachOnNextRender = this._vnode._children[0])
			});
		}
		promise.then(onResolved, onResolved);
	};

	Suspense.prototype.componentWillUnmount = function () {
		this._suspenders = [];
	};

	/**
	 * @this {import('./internal').SuspenseComponent}
	 * @param {import('./internal').SuspenseComponent["props"]} props
	 * @param {import('./internal').SuspenseState} state
	 */
	Suspense.prototype.render = function (props, state) {
		if (this._detachOnNextRender) {
			// When the Suspense's _vnode was created by a call to createVNode
			// (i.e. due to a setState further up in the tree)
			// it's _children prop is null, in this case we "forget" about the parked vnodes to detach
			if (this._vnode._children) {
				const detachedParent = document.createElement('div');
				const detachedComponent = this._vnode._children[0]._component;
				this._vnode._children[0] = detachedClone(
					this._detachOnNextRender,
					detachedParent,
					(detachedComponent._originalParentDom = detachedComponent._parentDom)
				);
			}

			this._detachOnNextRender = null;
		}

		return [
			createElement(Fragment, null, state._suspended ? null : props.children),
			state._suspended && createElement(Fragment, null, props.fallback)
		];
	};

	return Suspense;
}
```


---

### 🔹 Commit #10: `fa56ccec`
- **完整 Hash**: `fa56ccec69e13d771e2fa4bbbb385d5bdfcbb4a4`
- **說明 (Ground Truth)**: fix: pass errors rethrown by componentDidCatch to the next real boundary
- **變更檔案數**: 1

#### 📄 檔案: `src/diff/catch-error.js`
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

### 🔹 函式: `_catchError()`
- **變更前簽章 (Before)**: `function _catchError(error, vnode, oldVNode, errorInfo)` (L18~L60)
- **變更後簽章 (After)**: `function _catchError(error, vnode, oldVNode, errorInfo)` (L18~L64)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function _catchError(error, vnode, oldVNode, errorInfo) {
	/** @type {import('../internal').Component} */
	let component,
		/** @type {import('../internal').ComponentType} */
		ctor,
		/** @type {number} */
		handled;

	for (; (vnode = vnode._parent); ) {
		if (
			(component = vnode._component) &&
			!(component._bits & COMPONENT_PROCESSING_EXCEPTION)
		) {
			component._bits |= COMPONENT_FORCE;
			try {
				ctor = component.constructor;

				if (ctor && ctor.getDerivedStateFromError) {
					component.setState(ctor.getDerivedStateFromError(error));
					handled = component._bits & COMPONENT_DIRTY;
				}

				if (component.componentDidCatch) {
					component.componentDidCatch(error, errorInfo || {});
					handled = component._bits & COMPONENT_DIRTY;
				}

				// This is an error boundary. Mark it as having bailed out, and whether it was mid-hydration.
				if (handled) {
					component._bits |= COMPONENT_PENDING_ERROR;
					return;
				}
			} catch (e) {
				error = e;
			}
		}
	}

	// Reset rerender count to 0, so that the next render will not be skipped
	// when we leverage prefresh
	resetRenderCount();
	throw error;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function _catchError(error, vnode, oldVNode, errorInfo) {
	/** @type {import('../internal').Component} */
	let component,
		/** @type {import('../internal').ComponentType} */
		ctor,
		/** @type {number} */
		handled;

	for (; (vnode = vnode._parent); ) {
		if (
			(component = vnode._component) &&
			!(component._bits & COMPONENT_PROCESSING_EXCEPTION)
		) {
			component._bits |= COMPONENT_FORCE;
			try {
				ctor = component.constructor;

				if (ctor && ctor.getDerivedStateFromError) {
					component.setState(ctor.getDerivedStateFromError(error));
					handled = component._bits & COMPONENT_DIRTY;
				}

				if (component.componentDidCatch) {
					component.componentDidCatch(error, errorInfo || {});
					handled = component._bits & COMPONENT_DIRTY;
				}

				// This is an error boundary. Mark it as having bailed out, and whether it was mid-hydration.
				if (handled) {
					component._bits |= COMPONENT_PENDING_ERROR;
					return;
				}
			} catch (e) {
				error = e;
				// This component failed to handle the error, so what its
				// getDerivedStateFromError did must not make the next ancestor a
				// boundary.
				handled = 0;
			}
		}
	}

	// Reset rerender count to 0, so that the next render will not be skipped
	// when we leverage prefresh
	resetRenderCount();
	throw error;
}
```


---

### 🔹 Commit #11: `7c253417`
- **完整 Hash**: `7c25341774937bb5eb857fc53abc62ca24564979`
- **說明 (Ground Truth)**: Expose the ref of DOM and class elements on props in compat
- **變更檔案數**: 1

#### 📄 檔案: `compat/src/render.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:44, E:20, A:0) ➔ After(N:44, E:20, A:0)
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

### 🔹 函式: `vnode()`
- **變更前簽章 (Before)**: `vnode()` (L285~L310)
- **變更後簽章 (After)**: `vnode()` (L285~L322)

#### ◀️ 變更前實作碼 (Before Implementation):
```
vnode => {
	// only normalize props on Element nodes
	if (typeof vnode.type == 'string') {
		handleDomVNode(vnode);
	} else if (typeof vnode.type == 'function') {
		const shouldApplyRef =
			'prototype' in vnode.type && vnode.type.prototype.render;
		if ('ref' in vnode.props && shouldApplyRef) {
			vnode.ref = vnode.props.ref;
			delete vnode.props.ref;
		}

		if (vnode.type.defaultProps) {
			let normalizedProps = assign({}, vnode.props);
			for (let i in vnode.type.defaultProps) {
				if (normalizedProps[i] === undefined) {
					normalizedProps[i] = vnode.type.defaultProps[i];
				}
			}
			vnode.props = normalizedProps;
		}
	}
	vnode.$$typeof = REACT_ELEMENT_TYPE;

	if (oldVNodeHook) oldVNodeHook(vnode);
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
vnode => {
	// only normalize props on Element nodes
	if (typeof vnode.type == 'string') {
		handleDomVNode(vnode);
	} else if (typeof vnode.type == 'function') {
		const shouldApplyRef =
			'prototype' in vnode.type && vnode.type.prototype.render;
		if ('ref' in vnode.props && shouldApplyRef) {
			vnode.ref = vnode.props.ref;
			delete vnode.props.ref;
		}

		if (vnode.type.defaultProps) {
			let normalizedProps = assign({}, vnode.props);
			for (let i in vnode.type.defaultProps) {
				if (normalizedProps[i] === undefined) {
					normalizedProps[i] = vnode.type.defaultProps[i];
				}
			}
			vnode.props = normalizedProps;
		}
	}

	// React 19 keeps `ref` in element.props for every element type, and that's
	// where libraries detecting React 19 read it (e.g. MUI's getReactElementRef).
	// DOM and class vnodes keep theirs on vnode.ref, so expose it there too.
	// Non-enumerable, so diffing, spreading and render-to-string skip it.
	if (vnode.ref && !('ref' in vnode.props)) {
		Object.defineProperty(vnode.props, 'ref', {
			value: vnode.ref,
			configurable: true,
			writable: true
		});
	}
	vnode.$$typeof = REACT_ELEMENT_TYPE;

	if (oldVNodeHook) oldVNodeHook(vnode);
}
```


---

### 🔹 Commit #12: `78905d86`
- **完整 Hash**: `78905d86aadbffd88b7bda3b5f77b6dd4d9000d6`
- **說明 (Ground Truth)**: Keep the original start marker when a hydrating component re-suspends
- **變更檔案數**: 1

#### 📄 檔案: `src/diff/index.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:16, E:18, A:0) ➔ After(N:16, E:18, A:0)
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

### 🔹 函式: `diff()`
- **變更前簽章 (Before)**: `function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L57~L460)
- **變更後簽章 (After)**: `function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L57~L463)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	/** @type {any} */
	let tmp,
		resumed,
		newType = newVNode.type;

	// When passing through createElement it assigns the object
	// constructor as undefined. This to prevent JSON-injection.
	if (newVNode.constructor !== UNDEFINED) return NULL;

	// If the previous diff bailed out, resume creating/hydrating into the DOM
	// that was kept while suspended (server-rendered, or already in the
	// container we rendered into). `tmp` holds the stored excess node until the
	// options._diff call below.
	if (
		oldVNode._flags & MODE_SUSPENDED &&
		// @ts-expect-error This is MODE_HYDRATE or 0
		((isHydrating = oldVNode._flags & MODE_HYDRATE),
		(tmp = oldVNode._component._excess))
	) {
		newVNode._flags |= isHydrating;
		resumed = excessDomChildren = [];
		if (tmp.nodeType == 8) {
			// Re-scan DOM from stored start marker for streamed hydration.
			// `depth` only ever reaches 0 through the `break` below, so it
			// doesn't need to be re-tested in the loop condition.
			for (
				let depth = 1, node = tmp.nextSibling;
				node;
				node = node.nextSibling
			) {
				if (node.nodeType == 8) {
					if (node.data.startsWith('$s')) depth++;
					else if (node.data.startsWith('/$s') && !--depth) break;
				}
				excessDomChildren.push(node);
			}
		} else {
			excessDomChildren.push(tmp);
		}
		oldDom = excessDomChildren[0];
		oldVNode._component._excess = NULL;
	}

	if ((tmp = options._diff)) tmp(newVNode);

	outer: if (typeof newType == 'function') {
		let oldCommitQueueLength = commitQueue.length;
		try {
			let c,
				oldProps,
				oldState,
				snapshot,
				newProps = newVNode.props;
			const isClassComponent = (tmp = newType.prototype) && tmp.render;

			// Necessary for createContext api. Setting this property will pass
			// the context value as `this.context` just for this component.
			tmp = newType.contextType;
			const provider = tmp && globalContext[tmp._id];
			const componentContext = tmp
				? provider
					? provider.props.value
					: tmp._defaultValue
				: globalContext;

			// Get component and set it to `c`
			if (oldVNode._component) {
				c = newVNode._component = oldVNode._component;
				if (c._bits & COMPONENT_PENDING_ERROR) {
					c._bits |= COMPONENT_PROCESSING_EXCEPTION;
				}
			} else {
				// Instantiate the new component
				if (isClassComponent) {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new newType(newProps, componentContext); // eslint-disable-line new-cap
				} else {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new BaseComponent(
						newProps,
						componentContext
					);

					c.constructor = newType;
					c.render = doRender;
				}
				if (provider) provider.sub(c);

				if (!c.state) c.state = {};
				c._globalContext = globalContext;
				c._bits |= COMPONENT_DIRTY;
				c._renderCallbacks = [];
				c._stateCallbacks = [];
			}

			if (isClassComponent) {
				if (!c._nextState) c._nextState = c.state;

				// Invoke getDerivedStateFromProps
				if (newType.getDerivedStateFromProps) {
					if (c._nextState == c.state) {
						c._nextState = assign({}, c._nextState);
					}

					assign(
						c._nextState,
						newType.getDerivedStateFromProps(newProps, c._nextState)
					);
				}
			}

			oldProps = c.props;
			oldState = c.state;
			c._vnode = newVNode;

			// Invoke pre-render lifecycle methods
			if (!oldVNode._component) {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					c.componentWillMount
				) {
					c.componentWillMount();
				}

				if (isClassComponent && c.componentDidMount) {
					c._renderCallbacks.push(c.componentDidMount);
				}
			} else {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					newProps !== oldProps &&
					c.componentWillReceiveProps
				) {
					c.componentWillReceiveProps(newProps, componentContext);
				}

				if (
					(newVNode._original == oldVNode._original &&
						!(c._bits & COMPONENT_DIRTY)) ||
					(!(c._bits & COMPONENT_FORCE) &&
						c.shouldComponentUpdate &&
						c.shouldComponentUpdate(
							newProps,
							c._nextState,
							componentContext
						) === false)
				) {
					// More info about this here: https://gist.github.com/JoviDeCroock/bec5f2ce93544d2e6070ef8e0036e4e8
					if (newVNode._original != oldVNode._original) {
						// When we are dealing with a bail because of sCU we have to update
						// the props, state and dirty-state.
						// when we are dealing with strict-equality we don't as the child could still
						// be dirtied see #3883
						c.props = newProps;
						c.state = c._nextState;
						c._bits &= ~COMPONENT_DIRTY;
					}

					newVNode._dom = oldVNode._dom;
					newVNode._children = oldVNode._children;
					newVNode._children.some(vnode => {
						if (vnode) vnode._parent = newVNode;
					});

					EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
					c._stateCallbacks = [];

					if (c._renderCallbacks.length) {
						commitQueue.push(c);
					}

					// Skip over the retained subtree without traversing it; the
					// `result` branch in diffChildren picks this up as the next
					// oldDom.
					oldDom = getDomSibling(oldVNode);

					break outer;
				}

				if (c.componentWillUpdate) {
					c.componentWillUpdate(newProps, c._nextState, componentContext);
				}

				if (isClassComponent && c.componentDidUpdate) {
					c._renderCallbacks.push(() => {
						c.componentDidUpdate(oldProps, oldState, snapshot);
					});
				}
			}

			c.context = componentContext;
			c.props = newProps;
			c._parentDom = parentDom;
			c._bits &= ~COMPONENT_FORCE;

			let renderHook = options._render,
				count = 0;
			if (isClassComponent) {
				c.state = c._nextState;
				c._bits &= ~COMPONENT_DIRTY;

				if (renderHook) renderHook(newVNode);

				tmp = c.render(c.props, c.state, c.context);

				EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
				c._stateCallbacks = [];
			} else {
				do {
					c._bits &= ~COMPONENT_DIRTY;
					if (renderHook) renderHook(newVNode);

					tmp = c.render(c.props, c.state, c.context);

					// Handle setState called in render, see #2553
					c.state = c._nextState;
				} while (c._bits & COMPONENT_DIRTY && ++count < 25);
			}

			// Handle setState called in render, see #2553
			c.state = c._nextState;

			if (c.getChildContext) {
				globalContext = assign({}, globalContext, c.getChildContext());
			}

			if (
				isClassComponent &&
				oldVNode._component &&
				c.getSnapshotBeforeUpdate
			) {
				snapshot = c.getSnapshotBeforeUpdate(oldProps, oldState);
			}

			const renderResult =
				tmp && tmp.type === Fragment && tmp.key == NULL
					? tmp.props.children
					: tmp;

			// A vnode carrying a `_parentDom` prop, considered a new root,
			// continues rendering into that container. The subtree must stay
			// invisible to the host tree's DOM bookkeeping: the portal vnode
			// keeps a `null` `_dom` and the host insertion cursor (`oldDom`)
			// passes through unchanged.
			// `tmp` (the raw render result, already unwrapped into renderResult)
			// doubles as the saved host insertion cursor while we render into
			// the portal's container.
			if (newProps._parentDom) {
				tmp = oldDom;
				parentDom = newProps._parentDom;
				// If we portal into a math or svg element we need
				// to swap the namespace (chart libraries often do this).
				// The document follows the container too (e.g. iframes) as
				// diffElementNodes derives it from its parentDom.
				namespace = parentDom.namespaceURI;
				// Portals are never server-rendered: hydration must not claim the
				// host parent's excess nodes for the container's children.
				isHydrating = excessDomChildren = NULL;

				// Changing the container remounts the children into the new one
				if (oldVNode.props && oldVNode.props._parentDom != parentDom) {
					/** @type {VNode[]} */ (oldVNode._children).some(child => {
						if (child) unmount(child, child);
					});
					oldVNode._children = NULL;
				}

				oldDom = oldVNode._children ? getDomSibling(oldVNode, 0) : NULL;
			}

			oldDom = diffChildren(
				parentDom,
				isArray(renderResult) ? renderResult : [renderResult],
				newVNode,
				oldVNode,
				globalContext,
				namespace,
				excessDomChildren,
				commitQueue,
				oldDom,
				isHydrating,
				refQueue
			);

			// When we exit a portal we
			// change up the oldDom
			if (newProps._parentDom) {
				newVNode._dom = NULL;
				oldDom = tmp;
			}

			// We successfully rendered this VNode, unset any stored hydration/bailout state:
			newVNode._flags &= RESET_MODE;

			// Remove the kept DOM this resumed render didn't claim
			if (resumed) resumed.some(removeNode);

			if (c._renderCallbacks.length) {
				commitQueue.push(c);
			}

			// Only clear when this render was the retry; PENDING_ERROR set by a
			// descendant during this render must survive until then.
			if (c._bits & COMPONENT_PROCESSING_EXCEPTION) {
				c._bits &= ~(COMPONENT_PROCESSING_EXCEPTION | COMPONENT_PENDING_ERROR);
			}
		} catch (e) {
			// We remove any componentDidMount, ...
			// that have been invalidated by us
			// intercepting the error.
			commitQueue.length = oldCommitQueueLength;
			newVNode._original = NULL;
			// if hydrating or creating initial tree, bailout preserves DOM:
			if (isHydrating || excessDomChildren) {
				if (e.then) {
					let commentMarkersToFind = 0,
						startMarker;

					newVNode._flags |= isHydrating
						? MODE_HYDRATE | MODE_SUSPENDED
						: MODE_SUSPENDED;

					if (excessDomChildren) {
						for (let i = 0; i < excessDomChildren.length; i++) {
							let child = excessDomChildren[i];
							if (!child) continue;

							if (child.nodeType == 8) {
								excessDomChildren[i] = NULL;
								if (child.data.startsWith('$s')) {
									if (!commentMarkersToFind++) startMarker = child;
								} else if (
									child.data.startsWith('/$s') &&
									!--commentMarkersToFind
								) {
									oldDom = child;
									break;
								}
							} else if (commentMarkersToFind) {
								excessDomChildren[i] = NULL;
							}
						}
					}

					if (!startMarker) {
						while (oldDom && oldDom.nodeType == 8 && oldDom.nextSibling) {
							oldDom = oldDom.nextSibling;
						}

						if (excessDomChildren) {
							excessDomChildren[excessDomChildren.indexOf(oldDom)] = NULL;
						}
						startMarker = oldDom;
					}
					// Store the start marker directly; children re-scanned on resume
					newVNode._component._excess = startMarker;
					newVNode._dom = oldDom;
				} else if (excessDomChildren) {
					excessDomChildren.some(removeNode);
				}
			} else {
				newVNode._dom = oldVNode._dom;
			}

			if (!newVNode._children) {
				newVNode._children = oldVNode._children || [];
			}

			if (!e.then) markAsForce(newVNode);
			options._catchError(e, newVNode, oldVNode);
		}
	} else {
		oldDom = newVNode._dom = diffElementNodes(
			oldVNode._dom,
			newVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			isHydrating,
			refQueue,
			parentDom
		);
	}

	if ((tmp = options.diffed)) tmp(newVNode);

	return newVNode._flags & MODE_SUSPENDED ? UNDEFINED : oldDom;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	/** @type {any} */
	let tmp,
		resumed,
		newType = newVNode.type;

	// When passing through createElement it assigns the object
	// constructor as undefined. This to prevent JSON-injection.
	if (newVNode.constructor !== UNDEFINED) return NULL;

	// If the previous diff bailed out, resume creating/hydrating into the DOM
	// that was kept while suspended (server-rendered, or already in the
	// container we rendered into). `tmp` holds the stored excess node until the
	// options._diff call below.
	if (
		oldVNode._flags & MODE_SUSPENDED &&
		// @ts-expect-error This is MODE_HYDRATE or 0
		((isHydrating = oldVNode._flags & MODE_HYDRATE),
		(tmp = oldVNode._component._excess))
	) {
		newVNode._flags |= isHydrating;
		resumed = excessDomChildren = [];
		if (tmp.nodeType == 8) {
			// Re-scan DOM from stored start marker for streamed hydration.
			// `depth` only ever reaches 0 through the `break` below, so it
			// doesn't need to be re-tested in the loop condition.
			for (
				let depth = 1, node = tmp.nextSibling;
				node;
				node = node.nextSibling
			) {
				if (node.nodeType == 8) {
					if (node.data.startsWith('$s')) depth++;
					else if (node.data.startsWith('/$s') && !--depth) break;
				}
				excessDomChildren.push(node);
			}
		} else {
			excessDomChildren.push(tmp);
		}
		oldDom = excessDomChildren[0];
	}

	if ((tmp = options._diff)) tmp(newVNode);

	outer: if (typeof newType == 'function') {
		let oldCommitQueueLength = commitQueue.length;
		try {
			let c,
				oldProps,
				oldState,
				snapshot,
				newProps = newVNode.props;
			const isClassComponent = (tmp = newType.prototype) && tmp.render;

			// Necessary for createContext api. Setting this property will pass
			// the context value as `this.context` just for this component.
			tmp = newType.contextType;
			const provider = tmp && globalContext[tmp._id];
			const componentContext = tmp
				? provider
					? provider.props.value
					: tmp._defaultValue
				: globalContext;

			// Get component and set it to `c`
			if (oldVNode._component) {
				c = newVNode._component = oldVNode._component;
				if (c._bits & COMPONENT_PENDING_ERROR) {
					c._bits |= COMPONENT_PROCESSING_EXCEPTION;
				}
			} else {
				// Instantiate the new component
				if (isClassComponent) {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new newType(newProps, componentContext); // eslint-disable-line new-cap
				} else {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new BaseComponent(
						newProps,
						componentContext
					);

					c.constructor = newType;
					c.render = doRender;
				}
				if (provider) provider.sub(c);

				if (!c.state) c.state = {};
				c._globalContext = globalContext;
				c._bits |= COMPONENT_DIRTY;
				c._renderCallbacks = [];
				c._stateCallbacks = [];
			}

			if (isClassComponent) {
				if (!c._nextState) c._nextState = c.state;

				// Invoke getDerivedStateFromProps
				if (newType.getDerivedStateFromProps) {
					if (c._nextState == c.state) {
						c._nextState = assign({}, c._nextState);
					}

					assign(
						c._nextState,
						newType.getDerivedStateFromProps(newProps, c._nextState)
					);
				}
			}

			oldProps = c.props;
			oldState = c.state;
			c._vnode = newVNode;

			// Invoke pre-render lifecycle methods
			if (!oldVNode._component) {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					c.componentWillMount
				) {
					c.componentWillMount();
				}

				if (isClassComponent && c.componentDidMount) {
					c._renderCallbacks.push(c.componentDidMount);
				}
			} else {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					newProps !== oldProps &&
					c.componentWillReceiveProps
				) {
					c.componentWillReceiveProps(newProps, componentContext);
				}

				if (
					(newVNode._original == oldVNode._original &&
						!(c._bits & COMPONENT_DIRTY)) ||
					(!(c._bits & COMPONENT_FORCE) &&
						c.shouldComponentUpdate &&
						c.shouldComponentUpdate(
							newProps,
							c._nextState,
							componentContext
						) === false)
				) {
					// More info about this here: https://gist.github.com/JoviDeCroock/bec5f2ce93544d2e6070ef8e0036e4e8
					if (newVNode._original != oldVNode._original) {
						// When we are dealing with a bail because of sCU we have to update
						// the props, state and dirty-state.
						// when we are dealing with strict-equality we don't as the child could still
						// be dirtied see #3883
						c.props = newProps;
						c.state = c._nextState;
						c._bits &= ~COMPONENT_DIRTY;
					}

					newVNode._dom = oldVNode._dom;
					newVNode._children = oldVNode._children;
					newVNode._children.some(vnode => {
						if (vnode) vnode._parent = newVNode;
					});

					EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
					c._stateCallbacks = [];

					if (c._renderCallbacks.length) {
						commitQueue.push(c);
					}

					// Skip over the retained subtree without traversing it; the
					// `result` branch in diffChildren picks this up as the next
					// oldDom.
					oldDom = getDomSibling(oldVNode);

					break outer;
				}

				if (c.componentWillUpdate) {
					c.componentWillUpdate(newProps, c._nextState, componentContext);
				}

				if (isClassComponent && c.componentDidUpdate) {
					c._renderCallbacks.push(() => {
						c.componentDidUpdate(oldProps, oldState, snapshot);
					});
				}
			}

			c.context = componentContext;
			c.props = newProps;
			c._parentDom = parentDom;
			c._bits &= ~COMPONENT_FORCE;

			let renderHook = options._render,
				count = 0;
			if (isClassComponent) {
				c.state = c._nextState;
				c._bits &= ~COMPONENT_DIRTY;

				if (renderHook) renderHook(newVNode);

				tmp = c.render(c.props, c.state, c.context);

				EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
				c._stateCallbacks = [];
			} else {
				do {
					c._bits &= ~COMPONENT_DIRTY;
					if (renderHook) renderHook(newVNode);

					tmp = c.render(c.props, c.state, c.context);

					// Handle setState called in render, see #2553
					c.state = c._nextState;
				} while (c._bits & COMPONENT_DIRTY && ++count < 25);
			}

			// Handle setState called in render, see #2553
			c.state = c._nextState;

			if (c.getChildContext) {
				globalContext = assign({}, globalContext, c.getChildContext());
			}

			if (
				isClassComponent &&
				oldVNode._component &&
				c.getSnapshotBeforeUpdate
			) {
				snapshot = c.getSnapshotBeforeUpdate(oldProps, oldState);
			}

			const renderResult =
				tmp && tmp.type === Fragment && tmp.key == NULL
					? tmp.props.children
					: tmp;

			// A vnode carrying a `_parentDom` prop, considered a new root,
			// continues rendering into that container. The subtree must stay
			// invisible to the host tree's DOM bookkeeping: the portal vnode
			// keeps a `null` `_dom` and the host insertion cursor (`oldDom`)
			// passes through unchanged.
			// `tmp` (the raw render result, already unwrapped into renderResult)
			// doubles as the saved host insertion cursor while we render into
			// the portal's container.
			if (newProps._parentDom) {
				tmp = oldDom;
				parentDom = newProps._parentDom;
				// If we portal into a math or svg element we need
				// to swap the namespace (chart libraries often do this).
				// The document follows the container too (e.g. iframes) as
				// diffElementNodes derives it from its parentDom.
				namespace = parentDom.namespaceURI;
				// Portals are never server-rendered: hydration must not claim the
				// host parent's excess nodes for the container's children.
				isHydrating = excessDomChildren = NULL;

				// Changing the container remounts the children into the new one
				if (oldVNode.props && oldVNode.props._parentDom != parentDom) {
					/** @type {VNode[]} */ (oldVNode._children).some(child => {
						if (child) unmount(child, child);
					});
					oldVNode._children = NULL;
				}

				oldDom = oldVNode._children ? getDomSibling(oldVNode, 0) : NULL;
			}

			oldDom = diffChildren(
				parentDom,
				isArray(renderResult) ? renderResult : [renderResult],
				newVNode,
				oldVNode,
				globalContext,
				namespace,
				excessDomChildren,
				commitQueue,
				oldDom,
				isHydrating,
				refQueue
			);

			// When we exit a portal we
			// change up the oldDom
			if (newProps._parentDom) {
				newVNode._dom = NULL;
				oldDom = tmp;
			}

			// We successfully rendered this VNode, unset any stored hydration/bailout state:
			newVNode._flags &= RESET_MODE;
			if (oldVNode._flags & MODE_SUSPENDED) c._excess = NULL;

			// Remove the kept DOM this resumed render didn't claim
			if (resumed) resumed.some(removeNode);

			if (c._renderCallbacks.length) {
				commitQueue.push(c);
			}

			// Only clear when this render was the retry; PENDING_ERROR set by a
			// descendant during this render must survive until then.
			if (c._bits & COMPONENT_PROCESSING_EXCEPTION) {
				c._bits &= ~(COMPONENT_PROCESSING_EXCEPTION | COMPONENT_PENDING_ERROR);
			}
		} catch (e) {
			// We remove any componentDidMount, ...
			// that have been invalidated by us
			// intercepting the error.
			commitQueue.length = oldCommitQueueLength;
			newVNode._original = NULL;
			// if hydrating or creating initial tree, bailout preserves DOM:
			if (isHydrating || excessDomChildren) {
				if (e.then) {
					let commentMarkersToFind = 0,
						startMarker;

					newVNode._flags |= isHydrating
						? MODE_HYDRATE | MODE_SUSPENDED
						: MODE_SUSPENDED;

					if (excessDomChildren) {
						for (let i = 0; i < excessDomChildren.length; i++) {
							let child = excessDomChildren[i];
							if (!child) continue;

							if (child.nodeType == 8) {
								excessDomChildren[i] = NULL;
								if (child.data.startsWith('$s')) {
									if (!commentMarkersToFind++) startMarker = child;
								} else if (
									child.data.startsWith('/$s') &&
									!--commentMarkersToFind
								) {
									oldDom = child;
									break;
								}
							} else if (commentMarkersToFind) {
								excessDomChildren[i] = NULL;
							}
						}
					}

					if (!startMarker) {
						while (oldDom && oldDom.nodeType == 8 && oldDom.nextSibling) {
							oldDom = oldDom.nextSibling;
						}

						if (excessDomChildren) {
							excessDomChildren[excessDomChildren.indexOf(oldDom)] = NULL;
						}
						startMarker = oldDom;
					}
					// Store the start marker directly; children re-scanned on resume.
					// A re-suspension keeps the marker it originally started from.
					if (!newVNode._component._excess) {
						newVNode._component._excess = startMarker;
					}
					newVNode._dom = oldDom;
				} else if (excessDomChildren) {
					excessDomChildren.some(removeNode);
				}
			} else {
				newVNode._dom = oldVNode._dom;
			}

			if (!newVNode._children) {
				newVNode._children = oldVNode._children || [];
			}

			if (!e.then) markAsForce(newVNode);
			options._catchError(e, newVNode, oldVNode);
		}
	} else {
		oldDom = newVNode._dom = diffElementNodes(
			oldVNode._dom,
			newVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			isHydrating,
			refQueue,
			parentDom
		);
	}

	if ((tmp = options.diffed)) tmp(newVNode);

	return newVNode._flags & MODE_SUSPENDED ? UNDEFINED : oldDom;
}
```


---

### 🔹 Commit #13: `4cb4f809`
- **完整 Hash**: `4cb4f809af0f21c2e758603bf1852c24d5a6f664`
- **說明 (Ground Truth)**: fix(compat): map imageRendering to image-rendering
- **變更檔案數**: 1

#### 📄 檔案: `compat/src/render.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:44, E:20, A:0) ➔ After(N:44, E:20, A:0)
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

### 🔹 函式: `CAMEL_PROPS()`
- **變更前簽章 (Before)**: `[Module State] CAMEL_PROPS` (L29~L30)
- **變更後簽章 (After)**: `[Module State] CAMEL_PROPS` (L29~L30)

#### ◀️ 變更前實作碼 (Before Implementation):
```
CAMEL_PROPS =
	/^(?:accent|alignment|arabic|baseline|cap|clip(?!PathU)|color|dominant|fill|flood|font|glyph(?!R)|horiz|image(!S)|letter|lighting|marker(?!H|W|U)|overline|paint|pointer|shape|stop|strikethrough|stroke|text(?!L)|transform|underline|unicode|units|v|vector|vert|word|writing|x(?!C))[A-Z]/
```

#### ▶️ 變更後實作碼 (After Implementation):
```
CAMEL_PROPS =
	/^(?:accent|alignment|arabic|baseline|cap|clip(?!PathU)|color|dominant|fill|flood|font|glyph(?!R)|horiz|image(?!S)|letter|lighting|marker(?!H|W|U)|overline|paint|pointer|shape|stop|strikethrough|stroke|text(?!L)|transform|underline|unicode|units|v|vector|vert|word|writing|x(?!C))[A-Z]/
```


---

### 🔹 Commit #14: `cc1465d0`
- **完整 Hash**: `cc1465d072ff76317513e6c1da635d667d093a75`
- **說明 (Ground Truth)**: Reschedule queued components when a render throws
- **變更檔案數**: 1

#### 📄 檔案: `src/component.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:16, E:12, A:0) ➔ After(N:16, E:12, A:0)
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

### 🔹 函式: `process()`
- **變更前簽章 (Before)**: `function process()` (L226~L254)
- **變更後簽章 (After)**: `function process()` (L226~L256)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function process() {
	try {
		let c,
			l = 1;

		// Don't update `renderCount` yet. Keep its value non-zero to prevent unnecessary
		// process() calls from getting scheduled while `queue` is still being consumed.
		while (rerenderQueue.length) {
			// Keep the rerender queue sorted by (depth, insertion order). The queue
			// will initially be sorted on the first iteration only if it has more than 1 item.
			//
			// New items can be added to the queue e.g. when rerendering a provider, so we want to
			// keep the order from top to bottom with those new items so we can handle them in a
			// single pass
			if (rerenderQueue.length > l) {
				rerenderQueue.sort(depthSort);
			}

			c = rerenderQueue.shift();
			l = rerenderQueue.length;

			if (c._bits & COMPONENT_DIRTY) {
				renderComponent(c);
			}
		}
	} finally {
		rerenderQueue.length = rerenderCount = 0;
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function process() {
	try {
		let c,
			l = 1;

		// Don't update `renderCount` yet. Keep its value non-zero to prevent unnecessary
		// process() calls from getting scheduled while `queue` is still being consumed.
		while (rerenderQueue.length) {
			// Keep the rerender queue sorted by (depth, insertion order). The queue
			// will initially be sorted on the first iteration only if it has more than 1 item.
			//
			// New items can be added to the queue e.g. when rerendering a provider, so we want to
			// keep the order from top to bottom with those new items so we can handle them in a
			// single pass
			if (rerenderQueue.length > l) {
				rerenderQueue.sort(depthSort);
			}

			c = rerenderQueue.shift();
			l = rerenderQueue.length;

			if (c._bits & COMPONENT_DIRTY) {
				renderComponent(c);
			}
		}
	} finally {
		if ((rerenderCount = rerenderQueue.length)) {
			(prevDebounce || queueMicrotask)(process);
		}
	}
}
```


---

### 🔹 Commit #15: `aa0cf80d`
- **完整 Hash**: `aa0cf80db8b759d6796d1d094896edb37896ac4a`
- **說明 (Ground Truth)**: Preserve mounted hook state on re-suspend with a smaller footprint
- **變更檔案數**: 1

#### 📄 檔案: `compat/src/suspense.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:23, E:14, A:1) ➔ After(N:21, E:13, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 2, +Edges: 0, -Edges: 1, ΔFuncs: 5, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#detachedParent** `(Control)`
    └── 🎯 [CALLS] `createSuspense()`
        └── 🎯 [CALLS] `initSuspenseHooks()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `cleanup (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `componentDidUpdate` (FUNCTION_DEF)
  • - [移除呼叫邊] `detachedClone` ──[CALLS]──> `cleanup (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `initSuspenseHooks()`
- **變更前簽章 (Before)**: `function initSuspenseHooks()` (L10~L39)
- **變更後簽章 (After)**: `function initSuspenseHooks()` (L10~L43)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function initSuspenseHooks() {
	const oldCatchError = options._catchError;
	options._catchError = (error, newVNode, oldVNode, errorInfo) => {
		if (error.then) {
			/** @type {import('./internal').Component} */
			let component;
			let vnode = newVNode;

			while ((vnode = vnode._parent)) {
				if ((component = vnode._component) && component._childDidSuspend) {
					// Don't call oldCatchError if we found a Suspense
					return component._childDidSuspend(error, newVNode);
				}
			}
		}
		oldCatchError(error, newVNode, oldVNode, errorInfo);
	};

	const oldUnmount = options.unmount;
	options.unmount = vnode => {
		/** @type {import('./internal').Component} */
		const component = vnode._component;
		if (component) component._unmounted = true;
		if (component && component._onResolve) {
			component._onResolve();
		}

		if (oldUnmount) oldUnmount(vnode);
	};
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function initSuspenseHooks() {
	const oldCatchError = options._catchError;
	options._catchError = (error, newVNode, oldVNode, errorInfo) => {
		if (error.then) {
			/** @type {import('./internal').Component} */
			let component;
			let vnode = newVNode;

			while ((vnode = vnode._parent)) {
				if ((component = vnode._component) && component._childDidSuspend) {
					// A component that suspends before ever committing has no state
					// worth keeping; mounted ones keep their hooks while parked.
					if (oldVNode && !oldVNode._component)
						newVNode._component.__hooks = UNDEFINED;
					// Don't call oldCatchError if we found a Suspense
					return component._childDidSuspend(error, newVNode);
				}
			}
		}
		oldCatchError(error, newVNode, oldVNode, errorInfo);
	};

	const oldUnmount = options.unmount;
	options.unmount = vnode => {
		/** @type {import('./internal').Component} */
		const component = vnode._component;
		if (component) component._unmounted = true;
		if (component && component._onResolve) {
			component._onResolve();
		}

		if (oldUnmount) oldUnmount(vnode);
	};
}
```

### 🔹 函式: `detachedClone()`
- **變更前簽章 (Before)**: `function detachedClone(vnode, detachedParent, parentDom, preserveHooks)` (L41~L75)
- **變更後簽章 (After)**: `function detachedClone(vnode, detachedParent, parentDom)` (L45~L82)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function detachedClone(vnode, detachedParent, parentDom, preserveHooks) {
	if (vnode) {
		if (vnode._component && vnode._component.__hooks) {
			const hooks = vnode._component.__hooks;
			hooks._list.forEach(effect => {
				if (!preserveHooks || effect._passive != null) {
					const cleanup = effect._cleanup;
					effect._cleanup = effect._args = UNDEFINED;
					if (typeof cleanup == 'function') cleanup();
				}
			});
			if (preserveHooks) hooks._pendingEffects = [];
			else vnode._component.__hooks = null;
		}

		vnode = assign({ constructor: UNDEFINED }, vnode);
		if (vnode._component != null) {
			if (vnode._component._parentDom == parentDom) {
				vnode._component._parentDom = detachedParent;
			}

			vnode._component._bits |= COMPONENT_FORCE;

			vnode._component = null;
		}

		vnode._children =
			vnode._children &&
			vnode._children.map(child =>
				detachedClone(child, detachedParent, parentDom, preserveHooks)
			);
	}

	return vnode;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function detachedClone(vnode, detachedParent, parentDom) {
	if (vnode) {
		const hooks = vnode._component && vnode._component.__hooks;
		if (hooks) {
			hooks._list.forEach(effect => {
				// Only effects carry `_passive`; clearing `_args` makes them run
				// again when the tree is revealed, memo/ref state stays intact.
				if (effect._passive != null) {
					if (typeof effect._cleanup == 'function') effect._cleanup();
					effect._cleanup = effect._args = UNDEFINED;
				}
			});
			// Drop effects queued by the aborted render; `options._render` swaps in
			// a fresh `_pendingEffects` array before anything is pushed again, so
			// sharing one empty array here is safe.
			hooks._pendingEffects = vnode._component._renderCallbacks = [];
		}

		vnode = assign({ constructor: UNDEFINED }, vnode);
		if (vnode._component != null) {
			if (vnode._component._parentDom == parentDom) {
				vnode._component._parentDom = detachedParent;
			}

			vnode._component._bits |= COMPONENT_FORCE;

			vnode._component = null;
		}

		vnode._children =
			vnode._children &&
			vnode._children.map(child =>
				detachedClone(child, detachedParent, parentDom)
			);
	}

	return vnode;
}
```

### 🔹 函式: `render()`
- **變更前簽章 (Before)**: `render(props, state)` (L204~L227)
- **變更後簽章 (After)**: `render(props, state)` (L207~L229)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (props, state) {
		if (this._detachOnNextRender) {
			// When the Suspense's _vnode was created by a call to createVNode
			// (i.e. due to a setState further up in the tree)
			// it's _children prop is null, in this case we "forget" about the parked vnodes to detach
			if (this._vnode._children) {
				const detachedParent = document.createElement('div');
				const detachedComponent = this._vnode._children[0]._component;
				this._vnode._children[0] = detachedClone(
					this._detachOnNextRender,
					detachedParent,
					(detachedComponent._originalParentDom = detachedComponent._parentDom),
					this._unmounted == false
				);
			}

			this._detachOnNextRender = null;
		}

		return [
			createElement(Fragment, null, state._suspended ? null : props.children),
			state._suspended && createElement(Fragment, null, props.fallback)
		];
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (props, state) {
		if (this._detachOnNextRender) {
			// When the Suspense's _vnode was created by a call to createVNode
			// (i.e. due to a setState further up in the tree)
			// it's _children prop is null, in this case we "forget" about the parked vnodes to detach
			if (this._vnode._children) {
				const detachedParent = document.createElement('div');
				const detachedComponent = this._vnode._children[0]._component;
				this._vnode._children[0] = detachedClone(
					this._detachOnNextRender,
					detachedParent,
					(detachedComponent._originalParentDom = detachedComponent._parentDom)
				);
			}

			this._detachOnNextRender = null;
		}

		return [
			createElement(Fragment, null, state._suspended ? null : props.children),
			state._suspended && createElement(Fragment, null, props.fallback)
		];
	}
```

### 🔹 函式: `_catchError()`
- **變更前簽章 (Before)**: `_catchError(error, newVNode, oldVNode, errorInfo)` (L12~L26)
- **變更後簽章 (After)**: `_catchError(error, newVNode, oldVNode, errorInfo)` (L12~L30)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(error, newVNode, oldVNode, errorInfo) => {
		if (error.then) {
			/** @type {import('./internal').Component} */
			let component;
			let vnode = newVNode;

			while ((vnode = vnode._parent)) {
				if ((component = vnode._component) && component._childDidSuspend) {
					// Don't call oldCatchError if we found a Suspense
					return component._childDidSuspend(error, newVNode);
				}
			}
		}
		oldCatchError(error, newVNode, oldVNode, errorInfo);
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(error, newVNode, oldVNode, errorInfo) => {
		if (error.then) {
			/** @type {import('./internal').Component} */
			let component;
			let vnode = newVNode;

			while ((vnode = vnode._parent)) {
				if ((component = vnode._component) && component._childDidSuspend) {
					// A component that suspends before ever committing has no state
					// worth keeping; mounted ones keep their hooks while parked.
					if (oldVNode && !oldVNode._component)
						newVNode._component.__hooks = UNDEFINED;
					// Don't call oldCatchError if we found a Suspense
					return component._childDidSuspend(error, newVNode);
				}
			}
		}
		oldCatchError(error, newVNode, oldVNode, errorInfo);
	}
```

### 🔹 函式: `createSuspense()`
- **變更前簽章 (Before)**: `function createSuspense()` (L105~L230)
- **變更後簽章 (After)**: `function createSuspense()` (L112~L232)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createSuspense() {
	initSuspenseHooks();

	function Suspense() {
		// we do not call super here to golf some bytes...
		this._pendingSuspensionCount = 0;
		this._suspenders = null;
		this._detachOnNextRender = null;
	}

	// Things we do here to save some bytes but are not proper JS inheritance:
	// - call `new Component()` as the prototype
	// - do not set `Suspense.prototype.constructor` to `Suspense`
	Suspense.prototype = new Component();

	/**
	 * @this {import('./internal').SuspenseComponent}
	 * @param {Promise} promise The thrown promise
	 * @param {import('./internal').VNode<any, any>} suspendingVNode The suspending component
	 */
	Suspense.prototype._childDidSuspend = function (promise, suspendingVNode) {
		const suspendingComponent = suspendingVNode._component;

		if (this._suspenders == null) {
			this._suspenders = [];
		}
		this._suspenders.push(suspendingComponent);

		let resolved = false;
		const onResolved = () => {
			if (resolved || this._unmounted) return;

			resolved = true;
			suspendingComponent._onResolve = null;

			onSuspensionComplete();
		};

		suspendingComponent._onResolve = onResolved;

		// Store and null _parentDom to prevent setState/forceUpdate from
		// scheduling renders while suspended. Render would be a no-op anyway
		// since renderComponent checks _parentDom, but this avoids queue churn.
		const originalParentDom = suspendingComponent._parentDom;
		suspendingComponent._parentDom = null;

		const onSuspensionComplete = () => {
			if (!--this._pendingSuspensionCount) {
				// If the suspension was during hydration we don't need to restore the
				// suspended children into the _children array
				if (this.state._suspended) {
					const suspendedVNode = this.state._suspended;
					this._vnode._children[0] = removeOriginal(
						suspendedVNode,
						suspendedVNode._component._parentDom,
						suspendedVNode._component._originalParentDom
					);
				}

				this.setState({ _suspended: (this._detachOnNextRender = null) });

				let suspended;
				while ((suspended = this._suspenders.pop())) {
					// Restore _parentDom before forceUpdate so render can proceed
					suspended._parentDom = originalParentDom;
					suspended.forceUpdate();
				}
			}
		};

		/**
		 * We do not set `suspended: true` during hydration because we want the actual markup
		 * to remain on screen and hydrate it when the suspense actually gets resolved.
		 * While in non-hydration cases the usual fallback -> component flow would occour.
		 */
		if (
			!this._pendingSuspensionCount++ &&
			!(suspendingVNode._flags & MODE_HYDRATE)
		) {
			this.setState({
				_suspended: (this._detachOnNextRender = this._vnode._children[0])
			});
		}
		promise.then(onResolved, onResolved);
	};

	Suspense.prototype.componentWillUnmount = function () {
		this._suspenders = [];
	};
	Suspense.prototype.componentDidMount =
		Suspense.prototype.componentDidUpdate = function () {
			if (!this._pendingSuspensionCount) this._unmounted = false;
		};

	/**
	 * @this {import('./internal').SuspenseComponent}
	 * @param {import('./internal').SuspenseComponent["props"]} props
	 * @param {import('./internal').SuspenseState} state
	 */
	Suspense.prototype.render = function (props, state) {
		if (this._detachOnNextRender) {
			// When the Suspense's _vnode was created by a call to createVNode
			// (i.e. due to a setState further up in the tree)
			// it's _children prop is null, in this case we "forget" about the parked vnodes to detach
			if (this._vnode._children) {
				const detachedParent = document.createElement('div');
				const detachedComponent = this._vnode._children[0]._component;
				this._vnode._children[0] = detachedClone(
					this._detachOnNextRender,
					detachedParent,
					(detachedComponent._originalParentDom = detachedComponent._parentDom),
					this._unmounted == false
				);
			}

			this._detachOnNextRender = null;
		}

		return [
			createElement(Fragment, null, state._suspended ? null : props.children),
			state._suspended && createElement(Fragment, null, props.fallback)
		];
	};

	return Suspense;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createSuspense() {
	initSuspenseHooks();

	function Suspense() {
		// we do not call super here to golf some bytes...
		this._pendingSuspensionCount = 0;
		this._suspenders = null;
		this._detachOnNextRender = null;
	}

	// Things we do here to save some bytes but are not proper JS inheritance:
	// - call `new Component()` as the prototype
	// - do not set `Suspense.prototype.constructor` to `Suspense`
	Suspense.prototype = new Component();

	/**
	 * @this {import('./internal').SuspenseComponent}
	 * @param {Promise} promise The thrown promise
	 * @param {import('./internal').VNode<any, any>} suspendingVNode The suspending component
	 */
	Suspense.prototype._childDidSuspend = function (promise, suspendingVNode) {
		const suspendingComponent = suspendingVNode._component;

		if (this._suspenders == null) {
			this._suspenders = [];
		}
		this._suspenders.push(suspendingComponent);

		let resolved = false;
		const onResolved = () => {
			if (resolved || this._unmounted) return;

			resolved = true;
			suspendingComponent._onResolve = null;

			onSuspensionComplete();
		};

		suspendingComponent._onResolve = onResolved;

		// Store and null _parentDom to prevent setState/forceUpdate from
		// scheduling renders while suspended. Render would be a no-op anyway
		// since renderComponent checks _parentDom, but this avoids queue churn.
		const originalParentDom = suspendingComponent._parentDom;
		suspendingComponent._parentDom = null;

		const onSuspensionComplete = () => {
			if (!--this._pendingSuspensionCount) {
				// If the suspension was during hydration we don't need to restore the
				// suspended children into the _children array
				if (this.state._suspended) {
					const suspendedVNode = this.state._suspended;
					this._vnode._children[0] = removeOriginal(
						suspendedVNode,
						suspendedVNode._component._parentDom,
						suspendedVNode._component._originalParentDom
					);
				}

				this.setState({ _suspended: (this._detachOnNextRender = null) });

				let suspended;
				while ((suspended = this._suspenders.pop())) {
					// Restore _parentDom before forceUpdate so render can proceed
					suspended._parentDom = originalParentDom;
					suspended.forceUpdate();
				}
			}
		};

		/**
		 * We do not set `suspended: true` during hydration because we want the actual markup
		 * to remain on screen and hydrate it when the suspense actually gets resolved.
		 * While in non-hydration cases the usual fallback -> component flow would occour.
		 */
		if (
			!this._pendingSuspensionCount++ &&
			!(suspendingVNode._flags & MODE_HYDRATE)
		) {
			this.setState({
				_suspended: (this._detachOnNextRender = this._vnode._children[0])
			});
		}
		promise.then(onResolved, onResolved);
	};

	Suspense.prototype.componentWillUnmount = function () {
		this._suspenders = [];
	};

	/**
	 * @this {import('./internal').SuspenseComponent}
	 * @param {import('./internal').SuspenseComponent["props"]} props
	 * @param {import('./internal').SuspenseState} state
	 */
	Suspense.prototype.render = function (props, state) {
		if (this._detachOnNextRender) {
			// When the Suspense's _vnode was created by a call to createVNode
			// (i.e. due to a setState further up in the tree)
			// it's _children prop is null, in this case we "forget" about the parked vnodes to detach
			if (this._vnode._children) {
				const detachedParent = document.createElement('div');
				const detachedComponent = this._vnode._children[0]._component;
				this._vnode._children[0] = detachedClone(
					this._detachOnNextRender,
					detachedParent,
					(detachedComponent._originalParentDom = detachedComponent._parentDom)
				);
			}

			this._detachOnNextRender = null;
		}

		return [
			createElement(Fragment, null, state._suspended ? null : props.children),
			state._suspended && createElement(Fragment, null, props.fallback)
		];
	};

	return Suspense;
}
```


---

### 🔹 Commit #16: `be33f7af`
- **完整 Hash**: `be33f7af25bb25f3a584591b3951101f48de8910`
- **說明 (Ground Truth)**: Fix hook state loss when Suspense re-suspends
- **變更檔案數**: 2

#### 📄 檔案: `compat/src/suspense.js`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:21, E:13, A:1) ➔ After(N:23, E:14, A:1)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#detachedParent** `(Control)`
    └── 🎯 [CALLS] `createSuspense()`
        └── 🎯 [CALLS] `initSuspenseHooks()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `cleanup (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `componentDidUpdate` (FUNCTION_DEF)
  • + [新增呼叫邊] `detachedClone` ──[CALLS [guard: (!preserveHooks || effect._passive != null)]]──> `cleanup (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `detachedClone()`
- **變更前簽章 (Before)**: `function detachedClone(vnode, detachedParent, parentDom)` (L41~L70)
- **變更後簽章 (After)**: `function detachedClone(vnode, detachedParent, parentDom, preserveHooks)` (L41~L75)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function detachedClone(vnode, detachedParent, parentDom) {
	if (vnode) {
		if (vnode._component && vnode._component.__hooks) {
			vnode._component.__hooks._list.forEach(effect => {
				if (typeof effect._cleanup == 'function') effect._cleanup();
			});

			vnode._component.__hooks = null;
		}

		vnode = assign({ constructor: UNDEFINED }, vnode);
		if (vnode._component != null) {
			if (vnode._component._parentDom == parentDom) {
				vnode._component._parentDom = detachedParent;
			}

			vnode._component._bits |= COMPONENT_FORCE;

			vnode._component = null;
		}

		vnode._children =
			vnode._children &&
			vnode._children.map(child =>
				detachedClone(child, detachedParent, parentDom)
			);
	}

	return vnode;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function detachedClone(vnode, detachedParent, parentDom, preserveHooks) {
	if (vnode) {
		if (vnode._component && vnode._component.__hooks) {
			const hooks = vnode._component.__hooks;
			hooks._list.forEach(effect => {
				if (!preserveHooks || effect._passive != null) {
					const cleanup = effect._cleanup;
					effect._cleanup = effect._args = UNDEFINED;
					if (typeof cleanup == 'function') cleanup();
				}
			});
			if (preserveHooks) hooks._pendingEffects = [];
			else vnode._component.__hooks = null;
		}

		vnode = assign({ constructor: UNDEFINED }, vnode);
		if (vnode._component != null) {
			if (vnode._component._parentDom == parentDom) {
				vnode._component._parentDom = detachedParent;
			}

			vnode._component._bits |= COMPONENT_FORCE;

			vnode._component = null;
		}

		vnode._children =
			vnode._children &&
			vnode._children.map(child =>
				detachedClone(child, detachedParent, parentDom, preserveHooks)
			);
	}

	return vnode;
}
```

### 🔹 函式: `render()`
- **變更前簽章 (Before)**: `render(props, state)` (L195~L217)
- **變更後簽章 (After)**: `render(props, state)` (L204~L227)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (props, state) {
		if (this._detachOnNextRender) {
			// When the Suspense's _vnode was created by a call to createVNode
			// (i.e. due to a setState further up in the tree)
			// it's _children prop is null, in this case we "forget" about the parked vnodes to detach
			if (this._vnode._children) {
				const detachedParent = document.createElement('div');
				const detachedComponent = this._vnode._children[0]._component;
				this._vnode._children[0] = detachedClone(
					this._detachOnNextRender,
					detachedParent,
					(detachedComponent._originalParentDom = detachedComponent._parentDom)
				);
			}

			this._detachOnNextRender = null;
		}

		return [
			createElement(Fragment, null, state._suspended ? null : props.children),
			state._suspended && createElement(Fragment, null, props.fallback)
		];
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (props, state) {
		if (this._detachOnNextRender) {
			// When the Suspense's _vnode was created by a call to createVNode
			// (i.e. due to a setState further up in the tree)
			// it's _children prop is null, in this case we "forget" about the parked vnodes to detach
			if (this._vnode._children) {
				const detachedParent = document.createElement('div');
				const detachedComponent = this._vnode._children[0]._component;
				this._vnode._children[0] = detachedClone(
					this._detachOnNextRender,
					detachedParent,
					(detachedComponent._originalParentDom = detachedComponent._parentDom),
					this._unmounted == false
				);
			}

			this._detachOnNextRender = null;
		}

		return [
			createElement(Fragment, null, state._suspended ? null : props.children),
			state._suspended && createElement(Fragment, null, props.fallback)
		];
	}
```

### 🔹 函式: `createSuspense()`
- **變更前簽章 (Before)**: `function createSuspense()` (L100~L220)
- **變更後簽章 (After)**: `function createSuspense()` (L105~L230)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createSuspense() {
	initSuspenseHooks();

	function Suspense() {
		// we do not call super here to golf some bytes...
		this._pendingSuspensionCount = 0;
		this._suspenders = null;
		this._detachOnNextRender = null;
	}

	// Things we do here to save some bytes but are not proper JS inheritance:
	// - call `new Component()` as the prototype
	// - do not set `Suspense.prototype.constructor` to `Suspense`
	Suspense.prototype = new Component();

	/**
	 * @this {import('./internal').SuspenseComponent}
	 * @param {Promise} promise The thrown promise
	 * @param {import('./internal').VNode<any, any>} suspendingVNode The suspending component
	 */
	Suspense.prototype._childDidSuspend = function (promise, suspendingVNode) {
		const suspendingComponent = suspendingVNode._component;

		if (this._suspenders == null) {
			this._suspenders = [];
		}
		this._suspenders.push(suspendingComponent);

		let resolved = false;
		const onResolved = () => {
			if (resolved || this._unmounted) return;

			resolved = true;
			suspendingComponent._onResolve = null;

			onSuspensionComplete();
		};

		suspendingComponent._onResolve = onResolved;

		// Store and null _parentDom to prevent setState/forceUpdate from
		// scheduling renders while suspended. Render would be a no-op anyway
		// since renderComponent checks _parentDom, but this avoids queue churn.
		const originalParentDom = suspendingComponent._parentDom;
		suspendingComponent._parentDom = null;

		const onSuspensionComplete = () => {
			if (!--this._pendingSuspensionCount) {
				// If the suspension was during hydration we don't need to restore the
				// suspended children into the _children array
				if (this.state._suspended) {
					const suspendedVNode = this.state._suspended;
					this._vnode._children[0] = removeOriginal(
						suspendedVNode,
						suspendedVNode._component._parentDom,
						suspendedVNode._component._originalParentDom
					);
				}

				this.setState({ _suspended: (this._detachOnNextRender = null) });

				let suspended;
				while ((suspended = this._suspenders.pop())) {
					// Restore _parentDom before forceUpdate so render can proceed
					suspended._parentDom = originalParentDom;
					suspended.forceUpdate();
				}
			}
		};

		/**
		 * We do not set `suspended: true` during hydration because we want the actual markup
		 * to remain on screen and hydrate it when the suspense actually gets resolved.
		 * While in non-hydration cases the usual fallback -> component flow would occour.
		 */
		if (
			!this._pendingSuspensionCount++ &&
			!(suspendingVNode._flags & MODE_HYDRATE)
		) {
			this.setState({
				_suspended: (this._detachOnNextRender = this._vnode._children[0])
			});
		}
		promise.then(onResolved, onResolved);
	};

	Suspense.prototype.componentWillUnmount = function () {
		this._suspenders = [];
	};

	/**
	 * @this {import('./internal').SuspenseComponent}
	 * @param {import('./internal').SuspenseComponent["props"]} props
	 * @param {import('./internal').SuspenseState} state
	 */
	Suspense.prototype.render = function (props, state) {
		if (this._detachOnNextRender) {
			// When the Suspense's _vnode was created by a call to createVNode
			// (i.e. due to a setState further up in the tree)
			// it's _children prop is null, in this case we "forget" about the parked vnodes to detach
			if (this._vnode._children) {
				const detachedParent = document.createElement('div');
				const detachedComponent = this._vnode._children[0]._component;
				this._vnode._children[0] = detachedClone(
					this._detachOnNextRender,
					detachedParent,
					(detachedComponent._originalParentDom = detachedComponent._parentDom)
				);
			}

			this._detachOnNextRender = null;
		}

		return [
			createElement(Fragment, null, state._suspended ? null : props.children),
			state._suspended && createElement(Fragment, null, props.fallback)
		];
	};

	return Suspense;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createSuspense() {
	initSuspenseHooks();

	function Suspense() {
		// we do not call super here to golf some bytes...
		this._pendingSuspensionCount = 0;
		this._suspenders = null;
		this._detachOnNextRender = null;
	}

	// Things we do here to save some bytes but are not proper JS inheritance:
	// - call `new Component()` as the prototype
	// - do not set `Suspense.prototype.constructor` to `Suspense`
	Suspense.prototype = new Component();

	/**
	 * @this {import('./internal').SuspenseComponent}
	 * @param {Promise} promise The thrown promise
	 * @param {import('./internal').VNode<any, any>} suspendingVNode The suspending component
	 */
	Suspense.prototype._childDidSuspend = function (promise, suspendingVNode) {
		const suspendingComponent = suspendingVNode._component;

		if (this._suspenders == null) {
			this._suspenders = [];
		}
		this._suspenders.push(suspendingComponent);

		let resolved = false;
		const onResolved = () => {
			if (resolved || this._unmounted) return;

			resolved = true;
			suspendingComponent._onResolve = null;

			onSuspensionComplete();
		};

		suspendingComponent._onResolve = onResolved;

		// Store and null _parentDom to prevent setState/forceUpdate from
		// scheduling renders while suspended. Render would be a no-op anyway
		// since renderComponent checks _parentDom, but this avoids queue churn.
		const originalParentDom = suspendingComponent._parentDom;
		suspendingComponent._parentDom = null;

		const onSuspensionComplete = () => {
			if (!--this._pendingSuspensionCount) {
				// If the suspension was during hydration we don't need to restore the
				// suspended children into the _children array
				if (this.state._suspended) {
					const suspendedVNode = this.state._suspended;
					this._vnode._children[0] = removeOriginal(
						suspendedVNode,
						suspendedVNode._component._parentDom,
						suspendedVNode._component._originalParentDom
					);
				}

				this.setState({ _suspended: (this._detachOnNextRender = null) });

				let suspended;
				while ((suspended = this._suspenders.pop())) {
					// Restore _parentDom before forceUpdate so render can proceed
					suspended._parentDom = originalParentDom;
					suspended.forceUpdate();
				}
			}
		};

		/**
		 * We do not set `suspended: true` during hydration because we want the actual markup
		 * to remain on screen and hydrate it when the suspense actually gets resolved.
		 * While in non-hydration cases the usual fallback -> component flow would occour.
		 */
		if (
			!this._pendingSuspensionCount++ &&
			!(suspendingVNode._flags & MODE_HYDRATE)
		) {
			this.setState({
				_suspended: (this._detachOnNextRender = this._vnode._children[0])
			});
		}
		promise.then(onResolved, onResolved);
	};

	Suspense.prototype.componentWillUnmount = function () {
		this._suspenders = [];
	};
	Suspense.prototype.componentDidMount =
		Suspense.prototype.componentDidUpdate = function () {
			if (!this._pendingSuspensionCount) this._unmounted = false;
		};

	/**
	 * @this {import('./internal').SuspenseComponent}
	 * @param {import('./internal').SuspenseComponent["props"]} props
	 * @param {import('./internal').SuspenseState} state
	 */
	Suspense.prototype.render = function (props, state) {
		if (this._detachOnNextRender) {
			// When the Suspense's _vnode was created by a call to createVNode
			// (i.e. due to a setState further up in the tree)
			// it's _children prop is null, in this case we "forget" about the parked vnodes to detach
			if (this._vnode._children) {
				const detachedParent = document.createElement('div');
				const detachedComponent = this._vnode._children[0]._component;
				this._vnode._children[0] = detachedClone(
					this._detachOnNextRender,
					detachedParent,
					(detachedComponent._originalParentDom = detachedComponent._parentDom),
					this._unmounted == false
				);
			}

			this._detachOnNextRender = null;
		}

		return [
			createElement(Fragment, null, state._suspended ? null : props.children),
			state._suspended && createElement(Fragment, null, props.fallback)
		];
	};

	return Suspense;
}
```


#### 📄 檔案: `hooks/src/index.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:60, E:41, A:0) ➔ After(N:60, E:41, A:0)
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

### 🔹 函式: `useLayoutEffect()`
- **變更前簽章 (Before)**: `function useLayoutEffect(callback, args)` (L298~L307)
- **變更後簽章 (After)**: `function useLayoutEffect(callback, args)` (L298~L308)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function useLayoutEffect(callback, args) {
	/** @type {import('./internal').EffectHookState} */
	const state = getHookState(currentIndex++, 4);
	if (!options._skipEffects && argsChanged(state._args, args)) {
		state._value = callback;
		state._pendingArgs = args;

		currentComponent._renderCallbacks.push(state);
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function useLayoutEffect(callback, args) {
	/** @type {import('./internal').EffectHookState} */
	const state = getHookState(currentIndex++, 4);
	if (!options._skipEffects && argsChanged(state._args, args)) {
		state._passive = false;
		state._value = callback;
		state._pendingArgs = args;

		currentComponent._renderCallbacks.push(state);
	}
}
```


---

### 🔹 Commit #17: `cf4832c0`
- **完整 Hash**: `cf4832c04f669bc4ca56202394072d790dbddec3`
- **說明 (Ground Truth)**: fix: resolve preact dist build in minified tests
- **變更檔案數**: 1

#### 📄 檔案: `vitest.config.mjs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:13, E:1, A:0) ➔ After(N:13, E:1, A:0)
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

### 🔹 函式: `rollupAlias()`
- **變更前簽章 (Before)**: `[Module State] rollupAlias` (L12~L82)
- **變更後簽章 (After)**: `[Module State] rollupAlias` (L12~L87)

#### ◀️ 變更前實作碼 (Before Implementation):
```
rollupAlias = [
	{
		find: /^react$/,
		replacement: MINIFY
			? path.join(root, 'compat/dist/compat.mjs')
			: path.join(root, 'compat/src/index.js')
	},
	{
		find: /^react-dom$/,
		replacement: MINIFY
			? path.join(root, 'compat/dist/compat.mjs')
			: path.join(root, 'compat/src/index.js')
	},
	{
		find: /^react\/jsx-runtime$/,
		replacement: path.join(root, 'compat/jsx-runtime.mjs')
	},
	{
		find: /^react\/jsx-dev-runtime$/,
		replacement: path.join(root, 'compat/jsx-dev-runtime.mjs')
	},
	{ find: /^preact$/, replacement: path.join(root, 'src/index.js') },
	{
		find: /^preact\/compat$/,
		replacement: MINIFY
			? path.join(root, 'compat/dist/compat.mjs')
			: path.join(root, 'compat/src/index.js')
	},
	{
		find: /^preact\/jsx-runtime$/,
		replacement: MINIFY
			? path.join(root, 'jsx-runtime/dist/jsxRuntime.mjs')
			: path.join(root, 'jsx-runtime/src/index.js')
	},
	{
		find: /^preact\/jsx-runtime\/src$/,
		replacement: MINIFY
			? path.join(root, 'jsx-runtime/dist/jsxRuntime.mjs')
			: path.join(root, 'jsx-runtime/src')
	},
	{
		find: /^preact\/jsx-dev-runtime$/,
		replacement: MINIFY
			? path.join(root, 'jsx-runtime/dist/jsxRuntime.mjs')
			: path.join(root, 'jsx-runtime/src/index.js')
	},
	{
		find: /^preact\/debug$/,
		replacement: MINIFY
			? path.join(root, 'debug/dist/debug.mjs')
			: path.join(root, 'debug/src/index.js')
	},
	{
		find: /^preact\/devtools$/,
		replacement: MINIFY
			? path.join(root, 'devtools/dist/devtools.mjs')
			: path.join(root, 'devtools/src/index.js')
	},
	{
		find: /^preact\/hooks$/,
		replacement: MINIFY
			? path.join(root, 'hooks/dist/hooks.mjs')
			: path.join(root, 'hooks/src/index.js')
	},
	{
		find: /^preact\/test-utils$/,
		replacement: MINIFY
			? path.join(root, 'test-utils/dist/testUtils.mjs')
			: path.join(root, 'test-utils/src/index.js')
	}
]
```

#### ▶️ 變更後實作碼 (After Implementation):
```
rollupAlias = [
	{
		find: /^react$/,
		replacement: MINIFY
			? path.join(root, 'compat/dist/compat.mjs')
			: path.join(root, 'compat/src/index.js')
	},
	{
		find: /^react-dom$/,
		replacement: MINIFY
			? path.join(root, 'compat/dist/compat.mjs')
			: path.join(root, 'compat/src/index.js')
	},
	{
		find: /^react\/jsx-runtime$/,
		replacement: path.join(root, 'compat/jsx-runtime.mjs')
	},
	{
		find: /^react\/jsx-dev-runtime$/,
		replacement: path.join(root, 'compat/jsx-dev-runtime.mjs')
	},
	{
		find: /^preact$/,
		replacement: MINIFY
			? path.join(root, 'dist/preact.mjs')
			: path.join(root, 'src/index.js')
	},
	{
		find: /^preact\/compat$/,
		replacement: MINIFY
			? path.join(root, 'compat/dist/compat.mjs')
			: path.join(root, 'compat/src/index.js')
	},
	{
		find: /^preact\/jsx-runtime$/,
		replacement: MINIFY
			? path.join(root, 'jsx-runtime/dist/jsxRuntime.mjs')
			: path.join(root, 'jsx-runtime/src/index.js')
	},
	{
		find: /^preact\/jsx-runtime\/src$/,
		replacement: MINIFY
			? path.join(root, 'jsx-runtime/dist/jsxRuntime.mjs')
			: path.join(root, 'jsx-runtime/src')
	},
	{
		find: /^preact\/jsx-dev-runtime$/,
		replacement: MINIFY
			? path.join(root, 'jsx-runtime/dist/jsxRuntime.mjs')
			: path.join(root, 'jsx-runtime/src/index.js')
	},
	{
		find: /^preact\/debug$/,
		replacement: MINIFY
			? path.join(root, 'debug/dist/debug.mjs')
			: path.join(root, 'debug/src/index.js')
	},
	{
		find: /^preact\/devtools$/,
		replacement: MINIFY
			? path.join(root, 'devtools/dist/devtools.mjs')
			: path.join(root, 'devtools/src/index.js')
	},
	{
		find: /^preact\/hooks$/,
		replacement: MINIFY
			? path.join(root, 'hooks/dist/hooks.mjs')
			: path.join(root, 'hooks/src/index.js')
	},
	{
		find: /^preact\/test-utils$/,
		replacement: MINIFY
			? path.join(root, 'test-utils/dist/testUtils.mjs')
			: path.join(root, 'test-utils/src/index.js')
	}
]
```


---

### 🔹 Commit #18: `3a4b994b`
- **完整 Hash**: `3a4b994bed0a909c8c9e4ed290e8ffd78bd4698e`
- **說明 (Ground Truth)**: fix: anchor the MathML token element regex
- **變更檔案數**: 1

#### 📄 檔案: `src/constants.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:19, E:0, A:0) ➔ After(N:19, E:0, A:0)
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

### 🔹 函式: `MATHML_TOKEN_ELEMENTS()`
- **變更前簽章 (Before)**: `[Module State] MATHML_TOKEN_ELEMENTS` (L35~L35)
- **變更後簽章 (After)**: `[Module State] MATHML_TOKEN_ELEMENTS` (L35~L35)

#### ◀️ 變更前實作碼 (Before Implementation):
```
MATHML_TOKEN_ELEMENTS = /m(i|n|o|s$|te|sp)/
```

#### ▶️ 變更後實作碼 (After Implementation):
```
MATHML_TOKEN_ELEMENTS = /^m(i|n|o|s|text|space)$/
```


---

### 🔹 Commit #19: `0218a0ac`
- **完整 Hash**: `0218a0acf7f2e6595359f2dd93399179464e5293`
- **說明 (Ground Truth)**: fix: keep the pending error flag until the boundary's retry render
- **變更檔案數**: 1

#### 📄 檔案: `src/diff/index.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:17, E:21, A:0) ➔ After(N:17, E:21, A:0)
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

### 🔹 函式: `diff()`
- **變更前簽章 (Before)**: `function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L57~L449)
- **變更後簽章 (After)**: `function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
)` (L57~L451)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	/** @type {any} */
	let tmp,
		newType = newVNode.type;

	// When passing through createElement it assigns the object
	// constructor as undefined. This to prevent JSON-injection.
	if (newVNode.constructor !== UNDEFINED) return NULL;

	// If the previous diff bailed out, resume creating/hydrating.
	// `tmp` holds the stored excess node until the options._diff call below.
	if (
		oldVNode._flags & MODE_SUSPENDED &&
		// @ts-expect-error This is 1 or 0 (true or false)
		(isHydrating = oldVNode._flags & MODE_HYDRATE) &&
		(tmp = oldVNode._component._excess)
	) {
		newVNode._flags |= MODE_HYDRATE;
		excessDomChildren = [];
		if (tmp.nodeType == 8) {
			// Re-scan DOM from stored start marker for streamed hydration.
			// `depth` only ever reaches 0 through the `break` below, so it
			// doesn't need to be re-tested in the loop condition.
			for (
				let depth = 1, node = tmp.nextSibling;
				node;
				node = node.nextSibling
			) {
				if (node.nodeType == 8) {
					if (node.data.startsWith('$s')) depth++;
					else if (node.data.startsWith('/$s') && !--depth) break;
				}
				excessDomChildren.push(node);
			}
		} else {
			excessDomChildren.push(tmp);
		}
		oldDom = excessDomChildren[0];
		oldVNode._component._excess = NULL;
	}

	if ((tmp = options._diff)) tmp(newVNode);

	outer: if (typeof newType == 'function') {
		let oldCommitQueueLength = commitQueue.length;
		try {
			let c,
				oldProps,
				oldState,
				snapshot,
				newProps = newVNode.props;
			const isClassComponent = (tmp = newType.prototype) && tmp.render;

			// Necessary for createContext api. Setting this property will pass
			// the context value as `this.context` just for this component.
			tmp = newType.contextType;
			const provider = tmp && globalContext[tmp._id];
			const componentContext = tmp
				? provider
					? provider.props.value
					: tmp._defaultValue
				: globalContext;

			// Get component and set it to `c`
			if (oldVNode._component) {
				c = newVNode._component = oldVNode._component;
				if (c._bits & COMPONENT_PENDING_ERROR) {
					c._bits |= COMPONENT_PROCESSING_EXCEPTION;
				}
			} else {
				// Instantiate the new component
				if (isClassComponent) {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new newType(newProps, componentContext); // eslint-disable-line new-cap
				} else {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new BaseComponent(
						newProps,
						componentContext
					);

					c.constructor = newType;
					c.render = doRender;
				}
				if (provider) provider.sub(c);

				if (!c.state) c.state = {};
				c._globalContext = globalContext;
				c._bits |= COMPONENT_DIRTY;
				c._renderCallbacks = [];
				c._stateCallbacks = [];
			}

			if (isClassComponent) {
				if (!c._nextState) c._nextState = c.state;

				// Invoke getDerivedStateFromProps
				if (newType.getDerivedStateFromProps) {
					if (c._nextState == c.state) {
						c._nextState = assign({}, c._nextState);
					}

					assign(
						c._nextState,
						newType.getDerivedStateFromProps(newProps, c._nextState)
					);
				}
			}

			oldProps = c.props;
			oldState = c.state;
			c._vnode = newVNode;

			// Invoke pre-render lifecycle methods
			if (!oldVNode._component) {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					c.componentWillMount
				) {
					c.componentWillMount();
				}

				if (isClassComponent && c.componentDidMount) {
					c._renderCallbacks.push(c.componentDidMount);
				}
			} else {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					newProps !== oldProps &&
					c.componentWillReceiveProps
				) {
					c.componentWillReceiveProps(newProps, componentContext);
				}

				if (
					(newVNode._original == oldVNode._original &&
						!(c._bits & COMPONENT_DIRTY)) ||
					(!(c._bits & COMPONENT_FORCE) &&
						c.shouldComponentUpdate &&
						c.shouldComponentUpdate(
							newProps,
							c._nextState,
							componentContext
						) === false)
				) {
					// More info about this here: https://gist.github.com/JoviDeCroock/bec5f2ce93544d2e6070ef8e0036e4e8
					if (newVNode._original != oldVNode._original) {
						// When we are dealing with a bail because of sCU we have to update
						// the props, state and dirty-state.
						// when we are dealing with strict-equality we don't as the child could still
						// be dirtied see #3883
						c.props = newProps;
						c.state = c._nextState;
						c._bits &= ~COMPONENT_DIRTY;
					}

					newVNode._dom = oldVNode._dom;
					newVNode._children = oldVNode._children;
					newVNode._children.some(vnode => {
						if (vnode) vnode._parent = newVNode;
					});

					EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
					c._stateCallbacks = [];

					if (c._renderCallbacks.length) {
						commitQueue.push(c);
					}

					// Skip over the retained subtree without traversing it; the
					// `result` branch in diffChildren picks this up as the next
					// oldDom.
					oldDom = getDomSibling(oldVNode);

					break outer;
				}

				if (c.componentWillUpdate) {
					c.componentWillUpdate(newProps, c._nextState, componentContext);
				}

				if (isClassComponent && c.componentDidUpdate) {
					c._renderCallbacks.push(() => {
						c.componentDidUpdate(oldProps, oldState, snapshot);
					});
				}
			}

			c.context = componentContext;
			c.props = newProps;
			c._parentDom = parentDom;
			c._bits &= ~COMPONENT_FORCE;

			let renderHook = options._render,
				count = 0;
			if (isClassComponent) {
				c.state = c._nextState;
				c._bits &= ~COMPONENT_DIRTY;

				if (renderHook) renderHook(newVNode);

				tmp = c.render(c.props, c.state, c.context);

				EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
				c._stateCallbacks = [];
			} else {
				do {
					c._bits &= ~COMPONENT_DIRTY;
					if (renderHook) renderHook(newVNode);

					tmp = c.render(c.props, c.state, c.context);

					// Handle setState called in render, see #2553
					c.state = c._nextState;
				} while (c._bits & COMPONENT_DIRTY && ++count < 25);
			}

			// Handle setState called in render, see #2553
			c.state = c._nextState;

			if (c.getChildContext) {
				globalContext = assign({}, globalContext, c.getChildContext());
			}

			if (
				isClassComponent &&
				oldVNode._component &&
				c.getSnapshotBeforeUpdate
			) {
				snapshot = c.getSnapshotBeforeUpdate(oldProps, oldState);
			}

			const renderResult =
				tmp && tmp.type === Fragment && tmp.key == NULL
					? cloneNode(tmp.props.children)
					: tmp;

			// A vnode carrying a `_parentDom` prop, considered a new root,
			// continues rendering into that container. The subtree must stay
			// invisible to the host tree's DOM bookkeeping: the portal vnode
			// keeps a `null` `_dom` and the host insertion cursor (`oldDom`)
			// passes through unchanged.
			// `tmp` (the raw render result, already unwrapped into renderResult)
			// doubles as the saved host insertion cursor while we render into
			// the portal's container.
			if (newProps._parentDom) {
				tmp = oldDom;
				parentDom = newProps._parentDom;
				// If we portal into a math or svg element we need
				// to swap the namespace (chart libraries often do this).
				// The document follows the container too (e.g. iframes) as
				// diffElementNodes derives it from its parentDom.
				namespace = parentDom.namespaceURI;

				// Changing the container remounts the children into the new one
				if (oldVNode.props && oldVNode.props._parentDom != parentDom) {
					/** @type {VNode[]} */ (oldVNode._children).some(child => {
						if (child) unmount(child, child);
					});
					oldVNode._children = NULL;
				}

				oldDom = oldVNode._children ? getDomSibling(oldVNode, 0) : NULL;
			}

			oldDom = diffChildren(
				parentDom,
				isArray(renderResult) ? renderResult : [renderResult],
				newVNode,
				oldVNode,
				globalContext,
				namespace,
				excessDomChildren,
				commitQueue,
				oldDom,
				isHydrating,
				refQueue
			);

			// When we exit a portal we
			// change up the oldDom
			if (newProps._parentDom) {
				newVNode._dom = NULL;
				oldDom = tmp;
			}

			// We successfully rendered this VNode, unset any stored hydration/bailout state:
			newVNode._flags &= RESET_MODE;

			if (c._renderCallbacks.length) {
				commitQueue.push(c);
			}

			// PROCESSING_EXCEPTION is only ever set together with PENDING_ERROR,
			// so the clear doesn't need a guard.
			c._bits &= ~(COMPONENT_PROCESSING_EXCEPTION | COMPONENT_PENDING_ERROR);
		} catch (e) {
			// We remove any componentDidMount, ...
			// that have been invalidated by us
			// intercepting the error.
			commitQueue.length = oldCommitQueueLength;
			newVNode._original = NULL;
			// if hydrating or creating initial tree, bailout preserves DOM:
			if (isHydrating || excessDomChildren) {
				if (e.then) {
					let commentMarkersToFind = 0,
						startMarker;

					newVNode._flags |= isHydrating
						? MODE_HYDRATE | MODE_SUSPENDED
						: MODE_SUSPENDED;

					if (excessDomChildren) {
						for (let i = 0; i < excessDomChildren.length; i++) {
							let child = excessDomChildren[i];
							if (!child) continue;

							if (child.nodeType == 8) {
								excessDomChildren[i] = NULL;
								if (child.data.startsWith('$s')) {
									if (!commentMarkersToFind++) startMarker = child;
								} else if (
									child.data.startsWith('/$s') &&
									!--commentMarkersToFind
								) {
									oldDom = child;
									break;
								}
							} else if (commentMarkersToFind) {
								excessDomChildren[i] = NULL;
							}
						}
					}

					if (!startMarker) {
						while (oldDom && oldDom.nodeType == 8 && oldDom.nextSibling) {
							oldDom = oldDom.nextSibling;
						}

						if (excessDomChildren) {
							excessDomChildren[excessDomChildren.indexOf(oldDom)] = NULL;
						}
						startMarker = oldDom;
					}
					// Store the start marker directly; children re-scanned on resume
					newVNode._component._excess = startMarker;
					newVNode._dom = oldDom;
				} else if (excessDomChildren) {
					excessDomChildren.some(removeNode);
				}
			} else {
				newVNode._dom = oldVNode._dom;
			}

			if (!newVNode._children) {
				newVNode._children = oldVNode._children || [];
			}

			if (!e.then) markAsForce(newVNode);
			options._catchError(e, newVNode, oldVNode);
		}
	} else {
		oldDom = newVNode._dom = diffElementNodes(
			oldVNode._dom,
			newVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			isHydrating,
			refQueue,
			parentDom
		);
	}

	if ((tmp = options.diffed)) tmp(newVNode);

	return newVNode._flags & MODE_SUSPENDED ? UNDEFINED : oldDom;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function diff(
	parentDom,
	newVNode,
	oldVNode,
	globalContext,
	namespace,
	excessDomChildren,
	commitQueue,
	oldDom,
	isHydrating,
	refQueue
) {
	/** @type {any} */
	let tmp,
		newType = newVNode.type;

	// When passing through createElement it assigns the object
	// constructor as undefined. This to prevent JSON-injection.
	if (newVNode.constructor !== UNDEFINED) return NULL;

	// If the previous diff bailed out, resume creating/hydrating.
	// `tmp` holds the stored excess node until the options._diff call below.
	if (
		oldVNode._flags & MODE_SUSPENDED &&
		// @ts-expect-error This is 1 or 0 (true or false)
		(isHydrating = oldVNode._flags & MODE_HYDRATE) &&
		(tmp = oldVNode._component._excess)
	) {
		newVNode._flags |= MODE_HYDRATE;
		excessDomChildren = [];
		if (tmp.nodeType == 8) {
			// Re-scan DOM from stored start marker for streamed hydration.
			// `depth` only ever reaches 0 through the `break` below, so it
			// doesn't need to be re-tested in the loop condition.
			for (
				let depth = 1, node = tmp.nextSibling;
				node;
				node = node.nextSibling
			) {
				if (node.nodeType == 8) {
					if (node.data.startsWith('$s')) depth++;
					else if (node.data.startsWith('/$s') && !--depth) break;
				}
				excessDomChildren.push(node);
			}
		} else {
			excessDomChildren.push(tmp);
		}
		oldDom = excessDomChildren[0];
		oldVNode._component._excess = NULL;
	}

	if ((tmp = options._diff)) tmp(newVNode);

	outer: if (typeof newType == 'function') {
		let oldCommitQueueLength = commitQueue.length;
		try {
			let c,
				oldProps,
				oldState,
				snapshot,
				newProps = newVNode.props;
			const isClassComponent = (tmp = newType.prototype) && tmp.render;

			// Necessary for createContext api. Setting this property will pass
			// the context value as `this.context` just for this component.
			tmp = newType.contextType;
			const provider = tmp && globalContext[tmp._id];
			const componentContext = tmp
				? provider
					? provider.props.value
					: tmp._defaultValue
				: globalContext;

			// Get component and set it to `c`
			if (oldVNode._component) {
				c = newVNode._component = oldVNode._component;
				if (c._bits & COMPONENT_PENDING_ERROR) {
					c._bits |= COMPONENT_PROCESSING_EXCEPTION;
				}
			} else {
				// Instantiate the new component
				if (isClassComponent) {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new newType(newProps, componentContext); // eslint-disable-line new-cap
				} else {
					// @ts-expect-error Trust me, Component implements the interface we want
					newVNode._component = c = new BaseComponent(
						newProps,
						componentContext
					);

					c.constructor = newType;
					c.render = doRender;
				}
				if (provider) provider.sub(c);

				if (!c.state) c.state = {};
				c._globalContext = globalContext;
				c._bits |= COMPONENT_DIRTY;
				c._renderCallbacks = [];
				c._stateCallbacks = [];
			}

			if (isClassComponent) {
				if (!c._nextState) c._nextState = c.state;

				// Invoke getDerivedStateFromProps
				if (newType.getDerivedStateFromProps) {
					if (c._nextState == c.state) {
						c._nextState = assign({}, c._nextState);
					}

					assign(
						c._nextState,
						newType.getDerivedStateFromProps(newProps, c._nextState)
					);
				}
			}

			oldProps = c.props;
			oldState = c.state;
			c._vnode = newVNode;

			// Invoke pre-render lifecycle methods
			if (!oldVNode._component) {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					c.componentWillMount
				) {
					c.componentWillMount();
				}

				if (isClassComponent && c.componentDidMount) {
					c._renderCallbacks.push(c.componentDidMount);
				}
			} else {
				if (
					isClassComponent &&
					!newType.getDerivedStateFromProps &&
					newProps !== oldProps &&
					c.componentWillReceiveProps
				) {
					c.componentWillReceiveProps(newProps, componentContext);
				}

				if (
					(newVNode._original == oldVNode._original &&
						!(c._bits & COMPONENT_DIRTY)) ||
					(!(c._bits & COMPONENT_FORCE) &&
						c.shouldComponentUpdate &&
						c.shouldComponentUpdate(
							newProps,
							c._nextState,
							componentContext
						) === false)
				) {
					// More info about this here: https://gist.github.com/JoviDeCroock/bec5f2ce93544d2e6070ef8e0036e4e8
					if (newVNode._original != oldVNode._original) {
						// When we are dealing with a bail because of sCU we have to update
						// the props, state and dirty-state.
						// when we are dealing with strict-equality we don't as the child could still
						// be dirtied see #3883
						c.props = newProps;
						c.state = c._nextState;
						c._bits &= ~COMPONENT_DIRTY;
					}

					newVNode._dom = oldVNode._dom;
					newVNode._children = oldVNode._children;
					newVNode._children.some(vnode => {
						if (vnode) vnode._parent = newVNode;
					});

					EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
					c._stateCallbacks = [];

					if (c._renderCallbacks.length) {
						commitQueue.push(c);
					}

					// Skip over the retained subtree without traversing it; the
					// `result` branch in diffChildren picks this up as the next
					// oldDom.
					oldDom = getDomSibling(oldVNode);

					break outer;
				}

				if (c.componentWillUpdate) {
					c.componentWillUpdate(newProps, c._nextState, componentContext);
				}

				if (isClassComponent && c.componentDidUpdate) {
					c._renderCallbacks.push(() => {
						c.componentDidUpdate(oldProps, oldState, snapshot);
					});
				}
			}

			c.context = componentContext;
			c.props = newProps;
			c._parentDom = parentDom;
			c._bits &= ~COMPONENT_FORCE;

			let renderHook = options._render,
				count = 0;
			if (isClassComponent) {
				c.state = c._nextState;
				c._bits &= ~COMPONENT_DIRTY;

				if (renderHook) renderHook(newVNode);

				tmp = c.render(c.props, c.state, c.context);

				EMPTY_ARR.push.apply(c._renderCallbacks, c._stateCallbacks);
				c._stateCallbacks = [];
			} else {
				do {
					c._bits &= ~COMPONENT_DIRTY;
					if (renderHook) renderHook(newVNode);

					tmp = c.render(c.props, c.state, c.context);

					// Handle setState called in render, see #2553
					c.state = c._nextState;
				} while (c._bits & COMPONENT_DIRTY && ++count < 25);
			}

			// Handle setState called in render, see #2553
			c.state = c._nextState;

			if (c.getChildContext) {
				globalContext = assign({}, globalContext, c.getChildContext());
			}

			if (
				isClassComponent &&
				oldVNode._component &&
				c.getSnapshotBeforeUpdate
			) {
				snapshot = c.getSnapshotBeforeUpdate(oldProps, oldState);
			}

			const renderResult =
				tmp && tmp.type === Fragment && tmp.key == NULL
					? cloneNode(tmp.props.children)
					: tmp;

			// A vnode carrying a `_parentDom` prop, considered a new root,
			// continues rendering into that container. The subtree must stay
			// invisible to the host tree's DOM bookkeeping: the portal vnode
			// keeps a `null` `_dom` and the host insertion cursor (`oldDom`)
			// passes through unchanged.
			// `tmp` (the raw render result, already unwrapped into renderResult)
			// doubles as the saved host insertion cursor while we render into
			// the portal's container.
			if (newProps._parentDom) {
				tmp = oldDom;
				parentDom = newProps._parentDom;
				// If we portal into a math or svg element we need
				// to swap the namespace (chart libraries often do this).
				// The document follows the container too (e.g. iframes) as
				// diffElementNodes derives it from its parentDom.
				namespace = parentDom.namespaceURI;

				// Changing the container remounts the children into the new one
				if (oldVNode.props && oldVNode.props._parentDom != parentDom) {
					/** @type {VNode[]} */ (oldVNode._children).some(child => {
						if (child) unmount(child, child);
					});
					oldVNode._children = NULL;
				}

				oldDom = oldVNode._children ? getDomSibling(oldVNode, 0) : NULL;
			}

			oldDom = diffChildren(
				parentDom,
				isArray(renderResult) ? renderResult : [renderResult],
				newVNode,
				oldVNode,
				globalContext,
				namespace,
				excessDomChildren,
				commitQueue,
				oldDom,
				isHydrating,
				refQueue
			);

			// When we exit a portal we
			// change up the oldDom
			if (newProps._parentDom) {
				newVNode._dom = NULL;
				oldDom = tmp;
			}

			// We successfully rendered this VNode, unset any stored hydration/bailout state:
			newVNode._flags &= RESET_MODE;

			if (c._renderCallbacks.length) {
				commitQueue.push(c);
			}

			// Only clear when this render was the retry; PENDING_ERROR set by a
			// descendant during this render must survive until then.
			if (c._bits & COMPONENT_PROCESSING_EXCEPTION) {
				c._bits &= ~(COMPONENT_PROCESSING_EXCEPTION | COMPONENT_PENDING_ERROR);
			}
		} catch (e) {
			// We remove any componentDidMount, ...
			// that have been invalidated by us
			// intercepting the error.
			commitQueue.length = oldCommitQueueLength;
			newVNode._original = NULL;
			// if hydrating or creating initial tree, bailout preserves DOM:
			if (isHydrating || excessDomChildren) {
				if (e.then) {
					let commentMarkersToFind = 0,
						startMarker;

					newVNode._flags |= isHydrating
						? MODE_HYDRATE | MODE_SUSPENDED
						: MODE_SUSPENDED;

					if (excessDomChildren) {
						for (let i = 0; i < excessDomChildren.length; i++) {
							let child = excessDomChildren[i];
							if (!child) continue;

							if (child.nodeType == 8) {
								excessDomChildren[i] = NULL;
								if (child.data.startsWith('$s')) {
									if (!commentMarkersToFind++) startMarker = child;
								} else if (
									child.data.startsWith('/$s') &&
									!--commentMarkersToFind
								) {
									oldDom = child;
									break;
								}
							} else if (commentMarkersToFind) {
								excessDomChildren[i] = NULL;
							}
						}
					}

					if (!startMarker) {
						while (oldDom && oldDom.nodeType == 8 && oldDom.nextSibling) {
							oldDom = oldDom.nextSibling;
						}

						if (excessDomChildren) {
							excessDomChildren[excessDomChildren.indexOf(oldDom)] = NULL;
						}
						startMarker = oldDom;
					}
					// Store the start marker directly; children re-scanned on resume
					newVNode._component._excess = startMarker;
					newVNode._dom = oldDom;
				} else if (excessDomChildren) {
					excessDomChildren.some(removeNode);
				}
			} else {
				newVNode._dom = oldVNode._dom;
			}

			if (!newVNode._children) {
				newVNode._children = oldVNode._children || [];
			}

			if (!e.then) markAsForce(newVNode);
			options._catchError(e, newVNode, oldVNode);
		}
	} else {
		oldDom = newVNode._dom = diffElementNodes(
			oldVNode._dom,
			newVNode,
			oldVNode,
			globalContext,
			namespace,
			excessDomChildren,
			commitQueue,
			isHydrating,
			refQueue,
			parentDom
		);
	}

	if ((tmp = options.diffed)) tmp(newVNode);

	return newVNode._flags & MODE_SUSPENDED ? UNDEFINED : oldDom;
}
```


---

### 🔹 Commit #20: `e3f537a5`
- **完整 Hash**: `e3f537a519204ff4a6a69b4aec8718f7796bcf4d`
- **說明 (Ground Truth)**: fix: only treat components with error handlers as error boundaries
- **變更檔案數**: 1

#### 📄 檔案: `src/diff/catch-error.js`
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

### 🔹 函式: `_catchError()`
- **變更前簽章 (Before)**: `function _catchError(error, vnode, oldVNode, errorInfo)` (L18~L56)
- **變更後簽章 (After)**: `function _catchError(error, vnode, oldVNode, errorInfo)` (L18~L60)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function _catchError(error, vnode, oldVNode, errorInfo) {
	/** @type {import('../internal').Component} */
	let component,
		/** @type {import('../internal').ComponentType} */
		ctor;

	for (; (vnode = vnode._parent); ) {
		if (
			(component = vnode._component) &&
			!(component._bits & COMPONENT_PROCESSING_EXCEPTION)
		) {
			component._bits |= COMPONENT_FORCE;
			try {
				ctor = component.constructor;

				if (ctor && ctor.getDerivedStateFromError) {
					component.setState(ctor.getDerivedStateFromError(error));
				}

				if (component.componentDidCatch) {
					component.componentDidCatch(error, errorInfo || {});
				}

				// This is an error boundary. Mark it as having bailed out, and whether it was mid-hydration.
				if (component._bits & COMPONENT_DIRTY) {
					component._bits |= COMPONENT_PENDING_ERROR;
					return;
				}
			} catch (e) {
				error = e;
			}
		}
	}

	// Reset rerender count to 0, so that the next render will not be skipped
	// when we leverage prefresh
	resetRenderCount();
	throw error;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function _catchError(error, vnode, oldVNode, errorInfo) {
	/** @type {import('../internal').Component} */
	let component,
		/** @type {import('../internal').ComponentType} */
		ctor,
		/** @type {number} */
		handled;

	for (; (vnode = vnode._parent); ) {
		if (
			(component = vnode._component) &&
			!(component._bits & COMPONENT_PROCESSING_EXCEPTION)
		) {
			component._bits |= COMPONENT_FORCE;
			try {
				ctor = component.constructor;

				if (ctor && ctor.getDerivedStateFromError) {
					component.setState(ctor.getDerivedStateFromError(error));
					handled = component._bits & COMPONENT_DIRTY;
				}

				if (component.componentDidCatch) {
					component.componentDidCatch(error, errorInfo || {});
					handled = component._bits & COMPONENT_DIRTY;
				}

				// This is an error boundary. Mark it as having bailed out, and whether it was mid-hydration.
				if (handled) {
					component._bits |= COMPONENT_PENDING_ERROR;
					return;
				}
			} catch (e) {
				error = e;
			}
		}
	}

	// Reset rerender count to 0, so that the next render will not be skipped
	// when we leverage prefresh
	resetRenderCount();
	throw error;
}
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/preact show a9dc9b01073f2d9040e2fd45216bf296ec10ace0
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff a9dc9b01073f2d9040e2fd45216bf296ec10ace0~1 --file test_repos/preact/src/diff/children.js
   ```
