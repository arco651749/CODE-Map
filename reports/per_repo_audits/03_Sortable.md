# 🔬 CODE-Map 基準審查獨立驗證報告: `Sortable`
> **技術生態**: `JavaScript (拖曳排序 / 原生事件)`  
> **本地倉庫路徑**: `test_repos/Sortable`  
> **審查 Commit 數**: 13 Commits  
> **審查原始碼檔案數**: 13 Files  
> **報告生成時間**: 2026-10-20 21:40:36  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `0` / `13` | `0.0%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `12` / `13` | `92.3%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `1` / `13` | `7.7%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`12` / `13`** | **`92.3%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `13` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `bd74abb2`
- **完整 Hash**: `bd74abb22ade431c0e1af0cd552796ec1e0bcb0c`
- **說明 (Ground Truth)**: fix: Sortable crashes browser when event is triggered from within ShadowDom element
- **變更檔案數**: 1

#### 📄 檔案: `src/utils.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:39, E:29, A:1) ➔ After(N:39, E:29, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#el** `(Control)`
    └── ⚡ **on('event')**
        └── 🎯 [TRIGGERS] `fn (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `getParentOrHost()`
- **變更前簽章 (Before)**: `function getParentOrHost(el)` (L40~L44)
- **變更後簽章 (After)**: `function getParentOrHost(el)` (L40~L44)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function getParentOrHost(el) {
	return (el.host && el !== document && el.host.nodeType)
		? el.host
		: el.parentNode;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function getParentOrHost(el) {
	return (el.host && el !== document && el.host.nodeType && el.host !== el)
		? el.host
		: el.parentNode;
}
```


---

### 🔹 Commit #02: `7d7d5d66`
- **完整 Hash**: `7d7d5d66c3220594379ec2027ab33c4053c8201a`
- **說明 (Ground Truth)**: restore old fallback selection clearing behaviour
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:106, E:127, A:3) ➔ After(N:106, E:127, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_triggerDragStart()`
- **變更前簽章 (Before)**: `_triggerDragStart(/** Event */evt, /** Touch */touch)` (L701~L728)
- **變更後簽章 (After)**: `_triggerDragStart(/** Event */evt, /** Touch */touch)` (L701~L728)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/** Event */evt, /** Touch */touch) {
		touch = touch || (evt.pointerType == 'touch' && evt);

		if (!this.nativeDraggable || touch) {
			if (this.options.supportPointer) {
				on(document, 'pointermove', this._onTouchMove);
			} else if (touch) {
				on(document, 'touchmove', this._onTouchMove);
			} else {
				on(document, 'mousemove', this._onTouchMove);
			}
		} else {
			on(dragEl, 'dragend', this);
			on(rootEl, 'dragstart', this._onDragStart);
		}

		try {
			
			if (document.selection) {
				_nextTick(() => {
					document.selection.empty();
				});
			} else if (this.nativeDraggable) {
				window.getSelection().removeAllRanges();
			}
		} catch (err) {
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/** Event */evt, /** Touch */touch) {
		touch = touch || (evt.pointerType == 'touch' && evt);

		if (!this.nativeDraggable || touch) {
			if (this.options.supportPointer) {
				on(document, 'pointermove', this._onTouchMove);
			} else if (touch) {
				on(document, 'touchmove', this._onTouchMove);
			} else {
				on(document, 'mousemove', this._onTouchMove);
			}
		} else {
			on(dragEl, 'dragend', this);
			on(rootEl, 'dragstart', this._onDragStart);
		}

		try {
			
			if (document.selection) {
				_nextTick(() => {
					document.selection.empty();
				});
			} else {
				window.getSelection().removeAllRanges();
			}
		} catch (err) {
		}
	}
```


---

### 🔹 Commit #03: `a81251f4`
- **完整 Hash**: `a81251f406f3bfc629bdb91f596b15066b688773`
- **說明 (Ground Truth)**: #2410: Further improve selection handling on drag start
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:106, E:127, A:3) ➔ After(N:106, E:127, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_onDragStart()`
- **變更前簽章 (Before)**: `_onDragStart(/**Event*/evt, /**boolean*/fallback)` (L930~L1005)
- **變更後簽章 (After)**: `_onDragStart(/**Event*/evt, /**boolean*/fallback)` (L928~L1005)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/**Event*/evt, /**boolean*/fallback) {
		let _this = this;
		let dataTransfer = evt.dataTransfer;
		let options = _this.options;

		pluginEvent('dragStart', this, { evt });
		if (Sortable.eventCanceled) {
			this._onDrop();
			return;
		}

		pluginEvent('setupClone', this);
		if (!Sortable.eventCanceled) {
			cloneEl = clone(dragEl);
			cloneEl.removeAttribute("id");
			cloneEl.draggable = false;
			cloneEl.style['will-change'] = '';

			this._hideClone();

			toggleClass(cloneEl, this.options.chosenClass, false);
			Sortable.clone = cloneEl;
		}


		// #1143: IFrame support workaround
		_this.cloneId = _nextTick(function() {
			pluginEvent('clone', _this);
			if (Sortable.eventCanceled) return;

			if (!_this.options.removeCloneOnHide) {
				rootEl.insertBefore(cloneEl, dragEl);
			}
			_this._hideClone();

			_dispatchEvent({
				sortable: _this,
				name: 'clone'
			});
		});


		!fallback && toggleClass(dragEl, options.dragClass, true);

		// Set proper drop events
		if (fallback) {
			ignoreNextClick = true;
			_this._loopId = setInterval(_this._emulateDragOver, 50);
		} else {
			// Undo what was set in _prepareDragStart before drag started
			off(document, 'mouseup', _this._onDrop);
			off(document, 'touchend', _this._onDrop);
			off(document, 'touchcancel', _this._onDrop);

			if (dataTransfer) {
				dataTransfer.effectAllowed = 'move';
				options.setData && options.setData.call(_this, dataTransfer, dragEl);
			}

			on(document, 'drop', _this);

			// #1276 fix:
			css(dragEl, 'transform', 'translateZ(0)');
		}

		awaitingDragStarted = true;

		_this._dragStartId = _nextTick(_this._dragStarted.bind(_this, fallback, evt));
		on(document, 'selectstart', _this);

		moved = true;

		if (Safari) {
			css(document.body, 'user-select', 'none');
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/**Event*/evt, /**boolean*/fallback) {
		let _this = this;
		let dataTransfer = evt.dataTransfer;
		let options = _this.options;

		pluginEvent('dragStart', this, { evt });
		if (Sortable.eventCanceled) {
			this._onDrop();
			return;
		}

		pluginEvent('setupClone', this);
		if (!Sortable.eventCanceled) {
			cloneEl = clone(dragEl);
			cloneEl.removeAttribute("id");
			cloneEl.draggable = false;
			cloneEl.style['will-change'] = '';

			this._hideClone();

			toggleClass(cloneEl, this.options.chosenClass, false);
			Sortable.clone = cloneEl;
		}


		// #1143: IFrame support workaround
		_this.cloneId = _nextTick(function() {
			pluginEvent('clone', _this);
			if (Sortable.eventCanceled) return;

			if (!_this.options.removeCloneOnHide) {
				rootEl.insertBefore(cloneEl, dragEl);
			}
			_this._hideClone();

			_dispatchEvent({
				sortable: _this,
				name: 'clone'
			});
		});


		!fallback && toggleClass(dragEl, options.dragClass, true);

		// Set proper drop events
		if (fallback) {
			ignoreNextClick = true;
			_this._loopId = setInterval(_this._emulateDragOver, 50);
		} else {
			// Undo what was set in _prepareDragStart before drag started
			off(document, 'mouseup', _this._onDrop);
			off(document, 'touchend', _this._onDrop);
			off(document, 'touchcancel', _this._onDrop);

			if (dataTransfer) {
				dataTransfer.effectAllowed = 'move';
				options.setData && options.setData.call(_this, dataTransfer, dragEl);
			}

			on(document, 'drop', _this);

			// #1276 fix:
			css(dragEl, 'transform', 'translateZ(0)');
		}

		awaitingDragStarted = true;

		_this._dragStartId = _nextTick(_this._dragStarted.bind(_this, fallback, evt));
		on(document, 'selectstart', _this);

		moved = true;

		window.getSelection().removeAllRanges();

		if (Safari) {
			css(document.body, 'user-select', 'none');
		}
	}
```

### 🔹 函式: `_triggerDragStart()`
- **變更前簽章 (Before)**: `_triggerDragStart(/** Event */evt, /** Touch */touch)` (L701~L730)
- **變更後簽章 (After)**: `_triggerDragStart(/** Event */evt, /** Touch */touch)` (L701~L728)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/** Event */evt, /** Touch */touch) {
		touch = touch || (evt.pointerType == 'touch' && evt);

		if (!this.nativeDraggable || touch) {
			if (this.options.supportPointer) {
				on(document, 'pointermove', this._onTouchMove);
			} else if (touch) {
				on(document, 'touchmove', this._onTouchMove);
			} else {
				on(document, 'mousemove', this._onTouchMove);
			}
		} else {
			on(dragEl, 'dragend', this);
			on(rootEl, 'dragstart', this._onDragStart);
		}

		try {
			if (this.nativeDraggable) {
				window.getSelection().removeAllRanges();
			}
			_nextTick(() => {
				if (document.selection) {
					document.selection.empty();
				} else if (!this.nativeDraggable) {
					window.getSelection().removeAllRanges();
				}
			});
		} catch (err) {
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/** Event */evt, /** Touch */touch) {
		touch = touch || (evt.pointerType == 'touch' && evt);

		if (!this.nativeDraggable || touch) {
			if (this.options.supportPointer) {
				on(document, 'pointermove', this._onTouchMove);
			} else if (touch) {
				on(document, 'touchmove', this._onTouchMove);
			} else {
				on(document, 'mousemove', this._onTouchMove);
			}
		} else {
			on(dragEl, 'dragend', this);
			on(rootEl, 'dragstart', this._onDragStart);
		}

		try {
			
			if (document.selection) {
				_nextTick(() => {
					document.selection.empty();
				});
			} else if (this.nativeDraggable) {
				window.getSelection().removeAllRanges();
			}
		} catch (err) {
		}
	}
```


---

### 🔹 Commit #04: `ca13d2c3`
- **完整 Hash**: `ca13d2c3dde73604f41dd04d9165864db6441220`
- **說明 (Ground Truth)**: #2410: clear selection after drag start only with fallback
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:106, E:127, A:3) ➔ After(N:106, E:127, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_triggerDragStart()`
- **變更前簽章 (Before)**: `_triggerDragStart(/** Event */evt, /** Touch */touch)` (L701~L727)
- **變更後簽章 (After)**: `_triggerDragStart(/** Event */evt, /** Touch */touch)` (L701~L730)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/** Event */evt, /** Touch */touch) {
		touch = touch || (evt.pointerType == 'touch' && evt);

		if (!this.nativeDraggable || touch) {
			if (this.options.supportPointer) {
				on(document, 'pointermove', this._onTouchMove);
			} else if (touch) {
				on(document, 'touchmove', this._onTouchMove);
			} else {
				on(document, 'mousemove', this._onTouchMove);
			}
		} else {
			on(dragEl, 'dragend', this);
			on(rootEl, 'dragstart', this._onDragStart);
		}

		try {
			_nextTick(function () {
				if (document.selection) {
					document.selection.empty();
				} else {
					window.getSelection().removeAllRanges();
				}
			});
		} catch (err) {
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/** Event */evt, /** Touch */touch) {
		touch = touch || (evt.pointerType == 'touch' && evt);

		if (!this.nativeDraggable || touch) {
			if (this.options.supportPointer) {
				on(document, 'pointermove', this._onTouchMove);
			} else if (touch) {
				on(document, 'touchmove', this._onTouchMove);
			} else {
				on(document, 'mousemove', this._onTouchMove);
			}
		} else {
			on(dragEl, 'dragend', this);
			on(rootEl, 'dragstart', this._onDragStart);
		}

		try {
			if (this.nativeDraggable) {
				window.getSelection().removeAllRanges();
			}
			_nextTick(() => {
				if (document.selection) {
					document.selection.empty();
				} else if (!this.nativeDraggable) {
					window.getSelection().removeAllRanges();
				}
			});
		} catch (err) {
		}
	}
```


---

### 🔹 Commit #05: `f7a645c6`
- **完整 Hash**: `f7a645c6f2a50d3303074bd4170e7ff7da7cf6b3`
- **說明 (Ground Truth)**: fix text selection during fallback drag + improve pointer event support
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:106, E:127, A:3) ➔ After(N:106, E:127, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 5, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_onTapStart()`
- **變更前簽章 (Before)**: `_onTapStart(/** Event|TouchEvent */evt)` (L460~L556)
- **變更後簽章 (After)**: `_onTapStart(/** Event|TouchEvent */evt)` (L460~L556)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/** Event|TouchEvent */evt) {
		if (!evt.cancelable) return;
		let _this = this,
			el = this.el,
			options = this.options,
			preventOnFilter = options.preventOnFilter,
			type = evt.type,
			touch = (evt.touches && evt.touches[0]) || (evt.pointerType && evt.pointerType === 'touch' && evt),
			target = (touch || evt).target,
			originalTarget = evt.target.shadowRoot && ((evt.path && evt.path[0]) || (evt.composedPath && evt.composedPath()[0])) || target,
			filter = options.filter;

		_saveInputCheckedState(el);


		// Don't trigger start event when an element is been dragged, otherwise the evt.oldindex always wrong when set option.group.
		if (dragEl) {
			return;
		}

		if (/mousedown|pointerdown/.test(type) && evt.button !== 0 || options.disabled) {
			return; // only left button and enabled
		}

		// cancel dnd if original target is content editable
		if (originalTarget.isContentEditable) {
			return;
		}

		// Safari ignores further event handling after mousedown
		if (!this.nativeDraggable && Safari && target && target.tagName.toUpperCase() === 'SELECT') {
			return;
		}

		target = closest(target, options.draggable, el, false);


		if (target && target.animated) {
			return;
		}

		if (lastDownEl === target) {
			// Ignoring duplicate `down`
			return;
		}

		// Get the index of the dragged element within its parent
		oldIndex = index(target);
		oldDraggableIndex = index(target, options.draggable);

		// Check filter
		if (typeof filter === 'function') {
			if (filter.call(this, evt, target, this)) {
				_dispatchEvent({
					sortable: _this,
					rootEl: originalTarget,
					name: 'filter',
					targetEl: target,
					toEl: el,
					fromEl: el
				});
				pluginEvent('filter', _this, { evt });
				preventOnFilter && evt.cancelable && evt.preventDefault();
				return; // cancel dnd
			}
		}
		else if (filter) {
			filter = filter.split(',').some(function (criteria) {
				criteria = closest(originalTarget, criteria.trim(), el, false);

				if (criteria) {
					_dispatchEvent({
						sortable: _this,
						rootEl: criteria,
						name: 'filter',
						targetEl: target,
						fromEl: el,
						toEl: el
					});
					pluginEvent('filter', _this, { evt });
					return true;
				}
			});

			if (filter) {
				preventOnFilter && evt.cancelable && evt.preventDefault();
				return; // cancel dnd
			}
		}

		if (options.handle && !closest(originalTarget, options.handle, el, false)) {
			return;
		}

		// Prepare `dragstart`
		this._prepareDragStart(evt, touch, target);
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/** Event|TouchEvent */evt) {
		if (!evt.cancelable) return;
		let _this = this,
			el = this.el,
			options = this.options,
			preventOnFilter = options.preventOnFilter,
			type = evt.type,
			touch = (evt.touches && evt.touches[0]) || (evt.pointerType && evt.pointerType === 'touch' && evt),
			target = (touch || evt).target,
			originalTarget = evt.target.shadowRoot && ((evt.path && evt.path[0]) || (evt.composedPath && evt.composedPath()[0])) || target,
			filter = options.filter;

		_saveInputCheckedState(el);


		// Don't trigger start event when an element is been dragged, otherwise the evt.oldindex always wrong when set option.group.
		if (dragEl) {
			return;
		}

		if (/mousedown|pointerdown/.test(type) && evt.button !== 0 || options.disabled) {
			return; // only left button and enabled
		}

		// cancel dnd if original target is content editable
		if (originalTarget.isContentEditable) {
			return;
		}

		// Safari ignores further event handling after mousedown
		if (!this.nativeDraggable && Safari && target && target.tagName.toUpperCase() === 'SELECT') {
			return;
		}

		target = closest(target, options.draggable, el, false);


		if (target && target.animated) {
			return;
		}

		if (lastDownEl === target) {
			// Ignoring duplicate `down`
			return;
		}

		// Get the index of the dragged element within its parent
		oldIndex = index(target);
		oldDraggableIndex = index(target, options.draggable);

		// Check filter
		if (typeof filter === 'function') {
			if (filter.call(this, evt, target, this)) {
				_dispatchEvent({
					sortable: _this,
					rootEl: originalTarget,
					name: 'filter',
					targetEl: target,
					toEl: el,
					fromEl: el
				});
				pluginEvent('filter', _this, { evt });
				preventOnFilter && evt.preventDefault();
				return; // cancel dnd
			}
		}
		else if (filter) {
			filter = filter.split(',').some(function (criteria) {
				criteria = closest(originalTarget, criteria.trim(), el, false);

				if (criteria) {
					_dispatchEvent({
						sortable: _this,
						rootEl: criteria,
						name: 'filter',
						targetEl: target,
						fromEl: el,
						toEl: el
					});
					pluginEvent('filter', _this, { evt });
					return true;
				}
			});

			if (filter) {
				preventOnFilter && evt.preventDefault();
				return; // cancel dnd
			}
		}

		if (options.handle && !closest(originalTarget, options.handle, el, false)) {
			return;
		}

		// Prepare `dragstart`
		this._prepareDragStart(evt, touch, target);
	}
```

### 🔹 函式: `_prepareDragStart()`
- **變更前簽章 (Before)**: `_prepareDragStart(/** Event */evt, /** Touch */touch, /** HTMLElement */target)` (L558~L660)
- **變更後簽章 (After)**: `_prepareDragStart(/** Event */evt, /** Touch */touch, /** HTMLElement */target)` (L558~L671)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/** Event */evt, /** Touch */touch, /** HTMLElement */target) {
		let _this = this,
			el = _this.el,
			options = _this.options,
			ownerDocument = el.ownerDocument,
			dragStartFn;

		if (target && !dragEl && (target.parentNode === el)) {
			let dragRect = getRect(target);
			rootEl = el;
			dragEl = target;
			parentEl = dragEl.parentNode;
			nextEl = dragEl.nextSibling;
			lastDownEl = target;
			activeGroup = options.group;

			Sortable.dragged = dragEl;

			tapEvt = {
				target: dragEl,
				clientX: (touch || evt).clientX,
				clientY: (touch || evt).clientY
			};

			tapDistanceLeft = tapEvt.clientX - dragRect.left;
			tapDistanceTop = tapEvt.clientY - dragRect.top;

			this._lastX = (touch || evt).clientX;
			this._lastY = (touch || evt).clientY;

			dragEl.style['will-change'] = 'all';

			dragStartFn = function () {
				pluginEvent('delayEnded', _this, { evt });
				if (Sortable.eventCanceled) {
					_this._onDrop();
					return;
				}
				// Delayed drag has been triggered
				// we can re-enable the events: touchmove/mousemove
				_this._disableDelayedDragEvents();

				if (!FireFox && _this.nativeDraggable) {
					dragEl.draggable = true;
				}

				// Bind the events: dragstart/dragend
				_this._triggerDragStart(evt, touch);

				// Drag start event
				_dispatchEvent({
					sortable: _this,
					name: 'choose',
					originalEvent: evt
				});

				// Chosen item
				toggleClass(dragEl, options.chosenClass, true);
			};

			// Disable "draggable"
			options.ignore.split(',').forEach(function (criteria) {
				find(dragEl, criteria.trim(), _disableDraggable);
			});

			on(ownerDocument, 'dragover', nearestEmptyInsertDetectEvent);
			on(ownerDocument, 'mousemove', nearestEmptyInsertDetectEvent);
			on(ownerDocument, 'touchmove', nearestEmptyInsertDetectEvent);

			on(ownerDocument, 'mouseup', _this._onDrop);
			on(ownerDocument, 'touchend', _this._onDrop);
			on(ownerDocument, 'touchcancel', _this._onDrop);

			// Make dragEl draggable (must be before delay for FireFox)
			if (FireFox && this.nativeDraggable) {
				this.options.touchStartThreshold = 4;
				dragEl.draggable = true;
			}

			pluginEvent('delayStart', this, { evt });

			// Delay is impossible for native DnD in Edge or IE
			if (options.delay && (!options.delayOnTouchOnly || touch) && (!this.nativeDraggable || !(Edge || IE11OrLess))) {
				if (Sortable.eventCanceled) {
					this._onDrop();
					return;
				}
				// If the user moves the pointer or let go the click or touch
				// before the delay has been reached:
				// disable the delayed drag
				on(ownerDocument, 'mouseup', _this._disableDelayedDrag);
				on(ownerDocument, 'touchend', _this._disableDelayedDrag);
				on(ownerDocument, 'touchcancel', _this._disableDelayedDrag);
				on(ownerDocument, 'mousemove', _this._delayedDragTouchMoveHandler);
				on(ownerDocument, 'touchmove', _this._delayedDragTouchMoveHandler);
				options.supportPointer && on(ownerDocument, 'pointermove', _this._delayedDragTouchMoveHandler);

				_this._dragStartTimer = setTimeout(dragStartFn, options.delay);
			} else {
				dragStartFn();
			}
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/** Event */evt, /** Touch */touch, /** HTMLElement */target) {
		let _this = this,
			el = _this.el,
			options = _this.options,
			ownerDocument = el.ownerDocument,
			dragStartFn;

		if (target && !dragEl && (target.parentNode === el)) {
			let dragRect = getRect(target);
			rootEl = el;
			dragEl = target;
			parentEl = dragEl.parentNode;
			nextEl = dragEl.nextSibling;
			lastDownEl = target;
			activeGroup = options.group;

			Sortable.dragged = dragEl;

			tapEvt = {
				target: dragEl,
				clientX: (touch || evt).clientX,
				clientY: (touch || evt).clientY
			};

			tapDistanceLeft = tapEvt.clientX - dragRect.left;
			tapDistanceTop = tapEvt.clientY - dragRect.top;

			this._lastX = (touch || evt).clientX;
			this._lastY = (touch || evt).clientY;

			dragEl.style['will-change'] = 'all';

			dragStartFn = function () {
				pluginEvent('delayEnded', _this, { evt });
				if (Sortable.eventCanceled) {
					_this._onDrop();
					return;
				}
				// Delayed drag has been triggered
				// we can re-enable the events: touchmove/mousemove
				_this._disableDelayedDragEvents();

				if (!FireFox && _this.nativeDraggable) {
					dragEl.draggable = true;
				}

				// Bind the events: dragstart/dragend
				_this._triggerDragStart(evt, touch);

				// Drag start event
				_dispatchEvent({
					sortable: _this,
					name: 'choose',
					originalEvent: evt
				});

				// Chosen item
				toggleClass(dragEl, options.chosenClass, true);
			};

			// Disable "draggable"
			options.ignore.split(',').forEach(function (criteria) {
				find(dragEl, criteria.trim(), _disableDraggable);
			});

			on(ownerDocument, 'dragover', nearestEmptyInsertDetectEvent);
			on(ownerDocument, 'mousemove', nearestEmptyInsertDetectEvent);
			on(ownerDocument, 'touchmove', nearestEmptyInsertDetectEvent);

			if (options.supportPointer) {
				on(ownerDocument, 'pointerup', _this._onDrop);
				// Native D&D triggers pointercancel
				!this.nativeDraggable && on(ownerDocument, 'pointercancel', _this._onDrop);
			} else {
				on(ownerDocument, 'mouseup', _this._onDrop);
				on(ownerDocument, 'touchend', _this._onDrop);
				on(ownerDocument, 'touchcancel', _this._onDrop);
			}

			// Make dragEl draggable (must be before delay for FireFox)
			if (FireFox && this.nativeDraggable) {
				this.options.touchStartThreshold = 4;
				dragEl.draggable = true;
			}

			pluginEvent('delayStart', this, { evt });

			// Delay is impossible for native DnD in Edge or IE
			if (options.delay && (!options.delayOnTouchOnly || touch) && (!this.nativeDraggable || !(Edge || IE11OrLess))) {
				if (Sortable.eventCanceled) {
					this._onDrop();
					return;
				}
				// If the user moves the pointer or let go the click or touch
				// before the delay has been reached:
				// disable the delayed drag
				if (options.supportPointer) {
					on(ownerDocument, 'pointerup', _this._disableDelayedDrag);
					on(ownerDocument, 'pointercancel', _this._disableDelayedDrag);
				} else {
					on(ownerDocument, 'mouseup', _this._disableDelayedDrag);
					on(ownerDocument, 'touchend', _this._disableDelayedDrag);
					on(ownerDocument, 'touchcancel', _this._disableDelayedDrag);
				}
				on(ownerDocument, 'mousemove', _this._delayedDragTouchMoveHandler);
				on(ownerDocument, 'touchmove', _this._delayedDragTouchMoveHandler);
				options.supportPointer && on(ownerDocument, 'pointermove', _this._delayedDragTouchMoveHandler);

				_this._dragStartTimer = setTimeout(dragStartFn, options.delay);
			} else {
				dragStartFn();
			}
		}
	}
```

### 🔹 函式: `_offUpEvents()`
- **變更前簽章 (Before)**: `_offUpEvents()` (L1330~L1338)
- **變更後簽章 (After)**: `_offUpEvents()` (L1342~L1351)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function () {
		let ownerDocument = this.el.ownerDocument;

		off(ownerDocument, 'mouseup', this._onDrop);
		off(ownerDocument, 'touchend', this._onDrop);
		off(ownerDocument, 'pointerup', this._onDrop);
		off(ownerDocument, 'touchcancel', this._onDrop);
		off(document, 'selectstart', this);
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function () {
		let ownerDocument = this.el.ownerDocument;

		off(ownerDocument, 'mouseup', this._onDrop);
		off(ownerDocument, 'touchend', this._onDrop);
		off(ownerDocument, 'pointerup', this._onDrop);
		off(ownerDocument, 'pointercancel', this._onDrop);
		off(ownerDocument, 'touchcancel', this._onDrop);
		off(document, 'selectstart', this);
	}
```

### 🔹 函式: `_triggerDragStart()`
- **變更前簽章 (Before)**: `_triggerDragStart(/** Event */evt, /** Touch */touch)` (L688~L715)
- **變更後簽章 (After)**: `_triggerDragStart(/** Event */evt, /** Touch */touch)` (L701~L727)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/** Event */evt, /** Touch */touch) {
		touch = touch || (evt.pointerType == 'touch' && evt);

		if (!this.nativeDraggable || touch) {
			if (this.options.supportPointer) {
				on(document, 'pointermove', this._onTouchMove);
			} else if (touch) {
				on(document, 'touchmove', this._onTouchMove);
			} else {
				on(document, 'mousemove', this._onTouchMove);
			}
		} else {
			on(dragEl, 'dragend', this);
			on(rootEl, 'dragstart', this._onDragStart);
		}

		try {
			if (document.selection) {
				// Timeout neccessary for IE9
				_nextTick(function () {
					document.selection.empty();
				});
			} else {
				window.getSelection().removeAllRanges();
			}
		} catch (err) {
		}
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/** Event */evt, /** Touch */touch) {
		touch = touch || (evt.pointerType == 'touch' && evt);

		if (!this.nativeDraggable || touch) {
			if (this.options.supportPointer) {
				on(document, 'pointermove', this._onTouchMove);
			} else if (touch) {
				on(document, 'touchmove', this._onTouchMove);
			} else {
				on(document, 'mousemove', this._onTouchMove);
			}
		} else {
			on(dragEl, 'dragend', this);
			on(rootEl, 'dragstart', this._onDragStart);
		}

		try {
			_nextTick(function () {
				if (document.selection) {
					document.selection.empty();
				} else {
					window.getSelection().removeAllRanges();
				}
			});
		} catch (err) {
		}
	}
```

### 🔹 函式: `_disableDelayedDragEvents()`
- **變更前簽章 (Before)**: `_disableDelayedDragEvents()` (L678~L686)
- **變更後簽章 (After)**: `_disableDelayedDragEvents()` (L689~L699)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function () {
		let ownerDocument = this.el.ownerDocument;
		off(ownerDocument, 'mouseup', this._disableDelayedDrag);
		off(ownerDocument, 'touchend', this._disableDelayedDrag);
		off(ownerDocument, 'touchcancel', this._disableDelayedDrag);
		off(ownerDocument, 'mousemove', this._delayedDragTouchMoveHandler);
		off(ownerDocument, 'touchmove', this._delayedDragTouchMoveHandler);
		off(ownerDocument, 'pointermove', this._delayedDragTouchMoveHandler);
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function () {
		let ownerDocument = this.el.ownerDocument;
		off(ownerDocument, 'mouseup', this._disableDelayedDrag);
		off(ownerDocument, 'touchend', this._disableDelayedDrag);
		off(ownerDocument, 'touchcancel', this._disableDelayedDrag);
		off(ownerDocument, 'pointerup', this._disableDelayedDrag);
		off(ownerDocument, 'pointercancel', this._disableDelayedDrag);
		off(ownerDocument, 'mousemove', this._delayedDragTouchMoveHandler);
		off(ownerDocument, 'touchmove', this._delayedDragTouchMoveHandler);
		off(ownerDocument, 'pointermove', this._delayedDragTouchMoveHandler);
	}
```


---

### 🔹 Commit #06: `3eb35640`
- **完整 Hash**: `3eb35640f095a716782fa5e4f476e1b3a73c3751`
- **說明 (Ground Truth)**: fix the drag position problem when existing non draggable elements at the end of the list
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:104, E:124, A:3) ➔ After(N:104, E:124, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_onDragOver()`
- **變更前簽章 (Before)**: `_onDragOver(/**Event*/evt)` (L992~L1310)
- **變更後簽章 (After)**: `_onDragOver(/**Event*/evt)` (L992~L1315)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/**Event*/evt) {
		let el = this.el,
			target = evt.target,
			dragRect,
			targetRect,
			revert,
			options = this.options,
			group = options.group,
			activeSortable = Sortable.active,
			isOwner = (activeGroup === group),
			canSort = options.sort,
			fromSortable = (putSortable || activeSortable),
			vertical,
			_this = this,
			completedFired = false;

		if (_silent) return;

		function dragOverEvent(name, extra) {
			pluginEvent(name, _this, {
				evt,
				isOwner,
				axis: vertical ? 'vertical' : 'horizontal',
				revert,
				dragRect,
				targetRect,
				canSort,
				fromSortable,
				target,
				completed,
				onMove(target, after) {
					return onMove(rootEl, el, dragEl, dragRect, target, getRect(target), evt, after);
				},
				changed,
				...extra
			});
		}

		// Capture animation state
		function capture() {
			dragOverEvent('dragOverAnimationCapture');

			_this.captureAnimationState();
			if (_this !== fromSortable) {
				fromSortable.captureAnimationState();
			}
		}

		// Return invocation when dragEl is inserted (or completed)
		function completed(insertion) {
			dragOverEvent('dragOverCompleted', { insertion });

			if (insertion) {
				// Clones must be hidden before folding animation to capture dragRectAbsolute properly
				if (isOwner) {
					activeSortable._hideClone();
				} else {
					activeSortable._showClone(_this);
				}

				if (_this !== fromSortable) {
					// Set ghost class to new sortable's ghost class
					toggleClass(dragEl, putSortable ? putSortable.options.ghostClass : activeSortable.options.ghostClass, false);
					toggleClass(dragEl, options.ghostClass, true);
				}

				if (putSortable !== _this && _this !== Sortable.active) {
					putSortable = _this;
				} else if (_this === Sortable.active && putSortable) {
					putSortable = null;
				}

				// Animation
				if (fromSortable === _this) {
					_this._ignoreWhileAnimating = target;
				}
				_this.animateAll(function() {
					dragOverEvent('dragOverAnimationComplete');
					_this._ignoreWhileAnimating = null;
				});
				if (_this !== fromSortable) {
					fromSortable.animateAll();
					fromSortable._ignoreWhileAnimating = null;
				}
			}


			// Null lastTarget if it is not inside a previously swapped element
			if ((target === dragEl && !dragEl.animated) || (target === el && !target.animated)) {
				lastTarget = null;
			}

			// no bubbling and not fallback
			if (!options.dragoverBubble && !evt.rootEl && target !== document) {
				dragEl.parentNode[expando]._isOutsideThisEl(evt.target);

				// Do not detect for empty insert if already inserted
				!insertion && nearestEmptyInsertDetectEvent(evt);
			}

			!options.dragoverBubble && evt.stopPropagation && evt.stopPropagation();

			return (completedFired = true);
		}

		// Call when dragEl has been inserted
		function changed() {
			newIndex = index(dragEl);
			newDraggableIndex = index(dragEl, options.draggable);
			_dispatchEvent({
				sortable: _this,
				name: 'change',
				toEl: el,
				newIndex,
				newDraggableIndex,
				originalEvent: evt
			});
		}


		if (evt.preventDefault !== void 0) {
			evt.cancelable && evt.preventDefault();
		}


		target = closest(target, options.draggable, el, true);

		dragOverEvent('dragOver');
		if (Sortable.eventCanceled) return completedFired;

		if (
			dragEl.contains(evt.target) ||
			target.animated && target.animatingX && target.animatingY ||
			_this._ignoreWhileAnimating === target
		) {
			return completed(false);
		}

		ignoreNextClick = false;

		if (activeSortable && !options.disabled &&
			(isOwner
				? canSort || (revert = parentEl !== rootEl) // Reverting item into the original list
				: (
					putSortable === this ||
					(
						(this.lastPutMode = activeGroup.checkPull(this, activeSortable, dragEl, evt)) &&
						group.checkPut(this, activeSortable, dragEl, evt)
					)
				)
			)
		) {
			vertical = this._getDirection(evt, target) === 'vertical';

			dragRect = getRect(dragEl);

			dragOverEvent('dragOverValid');
			if (Sortable.eventCanceled) return completedFired;

			if (revert) {
				parentEl = rootEl; // actualization
				capture();

				this._hideClone();

				dragOverEvent('revert');

				if (!Sortable.eventCanceled) {
					if (nextEl) {
						rootEl.insertBefore(dragEl, nextEl);
					} else {
						rootEl.appendChild(dragEl);
					}
				}

				return completed(true);
			}

			let elLastChild = lastChild(el, options.draggable);

			if (!elLastChild || _ghostIsLast(evt, vertical, this) && !elLastChild.animated) {
				// Insert to end of list

				// If already at end of list: Do not insert
				if (elLastChild === dragEl) {
					return completed(false);
				}

				// if there is a last element, it is the target
				if (elLastChild && el === evt.target) {
					target = elLastChild;
				}

				if (target) {
					targetRect = getRect(target);
				}

				if (onMove(rootEl, el, dragEl, dragRect, target, targetRect, evt, !!target) !== false) {
					capture();
					el.appendChild(dragEl);
					parentEl = el; // actualization

					changed();
					return completed(true);
				}
			}
			else if (elLastChild && _ghostIsFirst(evt, vertical, this)) {
				// Insert to start of list
				let firstChild = getChild(el, 0, options, true);
				if (firstChild === dragEl) {
					return completed(false);
				}
				target = firstChild;
				targetRect = getRect(target);

				if (onMove(rootEl, el, dragEl, dragRect, target, targetRect, evt, false) !== false) {
					capture();
					el.insertBefore(dragEl, firstChild);
					parentEl = el; // actualization

					changed();
					return completed(true);
				}
			}
			else if (target.parentNode === el) {
				targetRect = getRect(target);
				let direction = 0,
					targetBeforeFirstSwap,
					differentLevel = dragEl.parentNode !== el,
					differentRowCol = !_dragElInRowColumn(dragEl.animated && dragEl.toRect || dragRect, target.animated && target.toRect || targetRect, vertical),
					side1 = vertical ? 'top' : 'left',
					scrolledPastTop = isScrolledPast(target, 'top', 'top') || isScrolledPast(dragEl, 'top', 'top'),
					scrollBefore = scrolledPastTop ? scrolledPastTop.scrollTop : void 0;


				if (lastTarget !== target) {
					targetBeforeFirstSwap = targetRect[side1];
					pastFirstInvertThresh = false;
					isCircumstantialInvert = (!differentRowCol && options.invertSwap) || differentLevel;
				}

				direction = _getSwapDirection(
					evt, target, targetRect, vertical,
					differentRowCol ? 1 : options.swapThreshold,
					options.invertedSwapThreshold == null ? options.swapThreshold : options.invertedSwapThreshold,
					isCircumstantialInvert,
					lastTarget === target
				);

				let sibling;

				if (direction !== 0) {
					// Check if target is beside dragEl in respective direction (ignoring hidden elements)
					let dragIndex = index(dragEl);

					do {
						dragIndex -= direction;
						sibling = parentEl.children[dragIndex];
					} while (sibling && (css(sibling, 'display') === 'none' || sibling === ghostEl));
				}
				// If dragEl is already beside target: Do not insert
				if (
					direction === 0 ||
					sibling === target
				) {
					return completed(false);
				}

				lastTarget = target;

				lastDirection = direction;

				let nextSibling = target.nextElementSibling,
					after = false;

				after = direction === 1;

				let moveVector = onMove(rootEl, el, dragEl, dragRect, target, targetRect, evt, after);

				if (moveVector !== false) {
					if (moveVector === 1 || moveVector === -1) {
						after = (moveVector === 1);
					}

					_silent = true;
					setTimeout(_unsilent, 30);

					capture();

					if (after && !nextSibling) {
						el.appendChild(dragEl);
					} else {
						target.parentNode.insertBefore(dragEl, after ? nextSibling : target);
					}

					// Undo chrome's scroll adjustment (has no effect on other browsers)
					if (scrolledPastTop) {
						scrollBy(scrolledPastTop, 0, scrollBefore - scrolledPastTop.scrollTop);
					}

					parentEl = dragEl.parentNode; // actualization

					// must be done before animation
					if (targetBeforeFirstSwap !== undefined && !isCircumstantialInvert) {
						targetMoveDistance = Math.abs(targetBeforeFirstSwap - getRect(target)[side1]);
					}
					changed();

					return completed(true);
				}
			}

			if (el.contains(dragEl)) {
				return completed(false);
			}
		}

		return false;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/**Event*/evt) {
		let el = this.el,
			target = evt.target,
			dragRect,
			targetRect,
			revert,
			options = this.options,
			group = options.group,
			activeSortable = Sortable.active,
			isOwner = (activeGroup === group),
			canSort = options.sort,
			fromSortable = (putSortable || activeSortable),
			vertical,
			_this = this,
			completedFired = false;

		if (_silent) return;

		function dragOverEvent(name, extra) {
			pluginEvent(name, _this, {
				evt,
				isOwner,
				axis: vertical ? 'vertical' : 'horizontal',
				revert,
				dragRect,
				targetRect,
				canSort,
				fromSortable,
				target,
				completed,
				onMove(target, after) {
					return onMove(rootEl, el, dragEl, dragRect, target, getRect(target), evt, after);
				},
				changed,
				...extra
			});
		}

		// Capture animation state
		function capture() {
			dragOverEvent('dragOverAnimationCapture');

			_this.captureAnimationState();
			if (_this !== fromSortable) {
				fromSortable.captureAnimationState();
			}
		}

		// Return invocation when dragEl is inserted (or completed)
		function completed(insertion) {
			dragOverEvent('dragOverCompleted', { insertion });

			if (insertion) {
				// Clones must be hidden before folding animation to capture dragRectAbsolute properly
				if (isOwner) {
					activeSortable._hideClone();
				} else {
					activeSortable._showClone(_this);
				}

				if (_this !== fromSortable) {
					// Set ghost class to new sortable's ghost class
					toggleClass(dragEl, putSortable ? putSortable.options.ghostClass : activeSortable.options.ghostClass, false);
					toggleClass(dragEl, options.ghostClass, true);
				}

				if (putSortable !== _this && _this !== Sortable.active) {
					putSortable = _this;
				} else if (_this === Sortable.active && putSortable) {
					putSortable = null;
				}

				// Animation
				if (fromSortable === _this) {
					_this._ignoreWhileAnimating = target;
				}
				_this.animateAll(function() {
					dragOverEvent('dragOverAnimationComplete');
					_this._ignoreWhileAnimating = null;
				});
				if (_this !== fromSortable) {
					fromSortable.animateAll();
					fromSortable._ignoreWhileAnimating = null;
				}
			}


			// Null lastTarget if it is not inside a previously swapped element
			if ((target === dragEl && !dragEl.animated) || (target === el && !target.animated)) {
				lastTarget = null;
			}

			// no bubbling and not fallback
			if (!options.dragoverBubble && !evt.rootEl && target !== document) {
				dragEl.parentNode[expando]._isOutsideThisEl(evt.target);

				// Do not detect for empty insert if already inserted
				!insertion && nearestEmptyInsertDetectEvent(evt);
			}

			!options.dragoverBubble && evt.stopPropagation && evt.stopPropagation();

			return (completedFired = true);
		}

		// Call when dragEl has been inserted
		function changed() {
			newIndex = index(dragEl);
			newDraggableIndex = index(dragEl, options.draggable);
			_dispatchEvent({
				sortable: _this,
				name: 'change',
				toEl: el,
				newIndex,
				newDraggableIndex,
				originalEvent: evt
			});
		}


		if (evt.preventDefault !== void 0) {
			evt.cancelable && evt.preventDefault();
		}


		target = closest(target, options.draggable, el, true);

		dragOverEvent('dragOver');
		if (Sortable.eventCanceled) return completedFired;

		if (
			dragEl.contains(evt.target) ||
			target.animated && target.animatingX && target.animatingY ||
			_this._ignoreWhileAnimating === target
		) {
			return completed(false);
		}

		ignoreNextClick = false;

		if (activeSortable && !options.disabled &&
			(isOwner
				? canSort || (revert = parentEl !== rootEl) // Reverting item into the original list
				: (
					putSortable === this ||
					(
						(this.lastPutMode = activeGroup.checkPull(this, activeSortable, dragEl, evt)) &&
						group.checkPut(this, activeSortable, dragEl, evt)
					)
				)
			)
		) {
			vertical = this._getDirection(evt, target) === 'vertical';

			dragRect = getRect(dragEl);

			dragOverEvent('dragOverValid');
			if (Sortable.eventCanceled) return completedFired;

			if (revert) {
				parentEl = rootEl; // actualization
				capture();

				this._hideClone();

				dragOverEvent('revert');

				if (!Sortable.eventCanceled) {
					if (nextEl) {
						rootEl.insertBefore(dragEl, nextEl);
					} else {
						rootEl.appendChild(dragEl);
					}
				}

				return completed(true);
			}

			let elLastChild = lastChild(el, options.draggable);

			if (!elLastChild || _ghostIsLast(evt, vertical, this) && !elLastChild.animated) {
				// Insert to end of list

				// If already at end of list: Do not insert
				if (elLastChild === dragEl) {
					return completed(false);
				}

				// if there is a last element, it is the target
				if (elLastChild && el === evt.target) {
					target = elLastChild;
				}

				if (target) {
					targetRect = getRect(target);
				}

				if (onMove(rootEl, el, dragEl, dragRect, target, targetRect, evt, !!target) !== false) {
					capture();
					if (elLastChild && elLastChild.nextSibling) { // the last draggable element is not the last node
						el.insertBefore(dragEl, elLastChild.nextSibling);
					}
					else {
						el.appendChild(dragEl);
					}
					parentEl = el; // actualization

					changed();
					return completed(true);
				}
			}
			else if (elLastChild && _ghostIsFirst(evt, vertical, this)) {
				// Insert to start of list
				let firstChild = getChild(el, 0, options, true);
				if (firstChild === dragEl) {
					return completed(false);
				}
				target = firstChild;
				targetRect = getRect(target);

				if (onMove(rootEl, el, dragEl, dragRect, target, targetRect, evt, false) !== false) {
					capture();
					el.insertBefore(dragEl, firstChild);
					parentEl = el; // actualization

					changed();
					return completed(true);
				}
			}
			else if (target.parentNode === el) {
				targetRect = getRect(target);
				let direction = 0,
					targetBeforeFirstSwap,
					differentLevel = dragEl.parentNode !== el,
					differentRowCol = !_dragElInRowColumn(dragEl.animated && dragEl.toRect || dragRect, target.animated && target.toRect || targetRect, vertical),
					side1 = vertical ? 'top' : 'left',
					scrolledPastTop = isScrolledPast(target, 'top', 'top') || isScrolledPast(dragEl, 'top', 'top'),
					scrollBefore = scrolledPastTop ? scrolledPastTop.scrollTop : void 0;


				if (lastTarget !== target) {
					targetBeforeFirstSwap = targetRect[side1];
					pastFirstInvertThresh = false;
					isCircumstantialInvert = (!differentRowCol && options.invertSwap) || differentLevel;
				}

				direction = _getSwapDirection(
					evt, target, targetRect, vertical,
					differentRowCol ? 1 : options.swapThreshold,
					options.invertedSwapThreshold == null ? options.swapThreshold : options.invertedSwapThreshold,
					isCircumstantialInvert,
					lastTarget === target
				);

				let sibling;

				if (direction !== 0) {
					// Check if target is beside dragEl in respective direction (ignoring hidden elements)
					let dragIndex = index(dragEl);

					do {
						dragIndex -= direction;
						sibling = parentEl.children[dragIndex];
					} while (sibling && (css(sibling, 'display') === 'none' || sibling === ghostEl));
				}
				// If dragEl is already beside target: Do not insert
				if (
					direction === 0 ||
					sibling === target
				) {
					return completed(false);
				}

				lastTarget = target;

				lastDirection = direction;

				let nextSibling = target.nextElementSibling,
					after = false;

				after = direction === 1;

				let moveVector = onMove(rootEl, el, dragEl, dragRect, target, targetRect, evt, after);

				if (moveVector !== false) {
					if (moveVector === 1 || moveVector === -1) {
						after = (moveVector === 1);
					}

					_silent = true;
					setTimeout(_unsilent, 30);

					capture();

					if (after && !nextSibling) {
						el.appendChild(dragEl);
					} else {
						target.parentNode.insertBefore(dragEl, after ? nextSibling : target);
					}

					// Undo chrome's scroll adjustment (has no effect on other browsers)
					if (scrolledPastTop) {
						scrollBy(scrolledPastTop, 0, scrollBefore - scrolledPastTop.scrollTop);
					}

					parentEl = dragEl.parentNode; // actualization

					// must be done before animation
					if (targetBeforeFirstSwap !== undefined && !isCircumstantialInvert) {
						targetMoveDistance = Math.abs(targetBeforeFirstSwap - getRect(target)[side1]);
					}
					changed();

					return completed(true);
				}
			}

			if (el.contains(dragEl)) {
				return completed(false);
			}
		}

		return false;
	}
```


---

### 🔹 Commit #07: `a0e160a5`
- **完整 Hash**: `a0e160a5189cdbb09a6e310413a2e4e719be6323`
- **說明 (Ground Truth)**: #1571: Dont use pointer events in Safari
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:103, E:120, A:3) ➔ After(N:103, E:120, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Sortable()`
- **變更前簽章 (Before)**: `function Sortable(el, options)` (L347~L443)
- **變更後簽章 (After)**: `function Sortable(el, options)` (L347~L443)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function Sortable(el, options) {
	if (!(el && el.nodeType && el.nodeType === 1)) {
		throw `Sortable: \`el\` must be an HTMLElement, not ${ {}.toString.call(el) }`;
	}

	this.el = el; // root element
	this.options = options = Object.assign({}, options);


	// Export instance
	el[expando] = this;

	let defaults = {
		group: null,
		sort: true,
		disabled: false,
		store: null,
		handle: null,
		draggable: /^[uo]l$/i.test(el.nodeName) ? '>li' : '>*',
		swapThreshold: 1, // percentage; 0 <= x <= 1
		invertSwap: false, // invert always
		invertedSwapThreshold: null, // will be set to same as swapThreshold if default
		removeCloneOnHide: true,
		direction: function() {
			return _detectDirection(el, this.options);
		},
		ghostClass: 'sortable-ghost',
		chosenClass: 'sortable-chosen',
		dragClass: 'sortable-drag',
		ignore: 'a, img',
		filter: null,
		preventOnFilter: true,
		animation: 0,
		easing: null,
		setData: function (dataTransfer, dragEl) {
			dataTransfer.setData('Text', dragEl.textContent);
		},
		dropBubble: false,
		dragoverBubble: false,
		dataIdAttr: 'data-id',
		delay: 0,
		delayOnTouchOnly: false,
		touchStartThreshold: (Number.parseInt ? Number : window).parseInt(window.devicePixelRatio, 10) || 1,
		forceFallback: false,
		fallbackClass: 'sortable-fallback',
		fallbackOnBody: false,
		fallbackTolerance: 0,
		fallbackOffset: {x: 0, y: 0},
		supportPointer: Sortable.supportPointer !== false && ('PointerEvent' in window),
		emptyInsertThreshold: 5
	};

	PluginManager.initializePlugins(this, el, defaults);

	// Set default options
	for (let name in defaults) {
		!(name in options) && (options[name] = defaults[name]);
	}

	_prepareGroup(options);

	// Bind all private methods
	for (let fn in this) {
		if (fn.charAt(0) === '_' && typeof this[fn] === 'function') {
			this[fn] = this[fn].bind(this);
		}
	}

	// Setup drag mode
	this.nativeDraggable = options.forceFallback ? false : supportDraggable;

	if (this.nativeDraggable) {
		// Touch start threshold cannot be greater than the native dragstart threshold
		this.options.touchStartThreshold = 1;
	}

	// Bind events
	if (options.supportPointer) {
		on(el, 'pointerdown', this._onTapStart);
	} else {
		on(el, 'mousedown', this._onTapStart);
		on(el, 'touchstart', this._onTapStart);
	}

	if (this.nativeDraggable) {
		on(el, 'dragover', this);
		on(el, 'dragenter', this);
	}

	sortables.push(this.el);

	// Restore sorting
	options.store && options.store.get && this.sort(options.store.get(this) || []);

	// Add animation state manager
	Object.assign(this, AnimationStateManager());
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function Sortable(el, options) {
	if (!(el && el.nodeType && el.nodeType === 1)) {
		throw `Sortable: \`el\` must be an HTMLElement, not ${ {}.toString.call(el) }`;
	}

	this.el = el; // root element
	this.options = options = Object.assign({}, options);


	// Export instance
	el[expando] = this;

	let defaults = {
		group: null,
		sort: true,
		disabled: false,
		store: null,
		handle: null,
		draggable: /^[uo]l$/i.test(el.nodeName) ? '>li' : '>*',
		swapThreshold: 1, // percentage; 0 <= x <= 1
		invertSwap: false, // invert always
		invertedSwapThreshold: null, // will be set to same as swapThreshold if default
		removeCloneOnHide: true,
		direction: function() {
			return _detectDirection(el, this.options);
		},
		ghostClass: 'sortable-ghost',
		chosenClass: 'sortable-chosen',
		dragClass: 'sortable-drag',
		ignore: 'a, img',
		filter: null,
		preventOnFilter: true,
		animation: 0,
		easing: null,
		setData: function (dataTransfer, dragEl) {
			dataTransfer.setData('Text', dragEl.textContent);
		},
		dropBubble: false,
		dragoverBubble: false,
		dataIdAttr: 'data-id',
		delay: 0,
		delayOnTouchOnly: false,
		touchStartThreshold: (Number.parseInt ? Number : window).parseInt(window.devicePixelRatio, 10) || 1,
		forceFallback: false,
		fallbackClass: 'sortable-fallback',
		fallbackOnBody: false,
		fallbackTolerance: 0,
		fallbackOffset: {x: 0, y: 0},
		supportPointer: Sortable.supportPointer !== false && ('PointerEvent' in window) && !Safari,
		emptyInsertThreshold: 5
	};

	PluginManager.initializePlugins(this, el, defaults);

	// Set default options
	for (let name in defaults) {
		!(name in options) && (options[name] = defaults[name]);
	}

	_prepareGroup(options);

	// Bind all private methods
	for (let fn in this) {
		if (fn.charAt(0) === '_' && typeof this[fn] === 'function') {
			this[fn] = this[fn].bind(this);
		}
	}

	// Setup drag mode
	this.nativeDraggable = options.forceFallback ? false : supportDraggable;

	if (this.nativeDraggable) {
		// Touch start threshold cannot be greater than the native dragstart threshold
		this.options.touchStartThreshold = 1;
	}

	// Bind events
	if (options.supportPointer) {
		on(el, 'pointerdown', this._onTapStart);
	} else {
		on(el, 'mousedown', this._onTapStart);
		on(el, 'touchstart', this._onTapStart);
	}

	if (this.nativeDraggable) {
		on(el, 'dragover', this);
		on(el, 'dragenter', this);
	}

	sortables.push(this.el);

	// Restore sorting
	options.store && options.store.get && this.sort(options.store.get(this) || []);

	// Add animation state manager
	Object.assign(this, AnimationStateManager());
}
```


---

### 🔹 Commit #08: `e9793701`
- **完整 Hash**: `e97937010a112b4550b613e47f9e0019624d827d`
- **說明 (Ground Truth)**: #1644: Remove transform on drop
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:103, E:120, A:3) ➔ After(N:103, E:120, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_onDrop()`
- **變更前簽章 (Before)**: `_onDrop(/**Event*/evt)` (L1308~L1475)
- **變更後簽章 (After)**: `_onDrop(/**Event*/evt)` (L1308~L1476)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/**Event*/evt) {
		let el = this.el,
			options = this.options;

		// Get the index of the dragged element within its parent
		newIndex = index(dragEl);
		newDraggableIndex = index(dragEl, options.draggable);

		pluginEvent('drop', this, {
			evt
		});

		parentEl = dragEl && dragEl.parentNode;

		// Get again after plugin event
		newIndex = index(dragEl);
		newDraggableIndex = index(dragEl, options.draggable);

		if (Sortable.eventCanceled) {
			this._nulling();
			return;
		}

		awaitingDragStarted = false;
		isCircumstantialInvert = false;
		pastFirstInvertThresh = false;

		clearInterval(this._loopId);

		clearTimeout(this._dragStartTimer);

		_cancelNextTick(this.cloneId);
		_cancelNextTick(this._dragStartId);

		// Unbind events
		if (this.nativeDraggable) {
			off(document, 'drop', this);
			off(el, 'dragstart', this._onDragStart);
		}
		this._offMoveEvents();
		this._offUpEvents();


		if (Safari) {
			css(document.body, 'user-select', '');
		}


		if (evt) {
			if (moved) {
				evt.cancelable && evt.preventDefault();
				!options.dropBubble && evt.stopPropagation();
			}

			ghostEl && ghostEl.parentNode && ghostEl.parentNode.removeChild(ghostEl);

			if (rootEl === parentEl || (putSortable && putSortable.lastPutMode !== 'clone')) {
				// Remove clone(s)
				cloneEl && cloneEl.parentNode && cloneEl.parentNode.removeChild(cloneEl);
			}

			if (dragEl) {
				if (this.nativeDraggable) {
					off(dragEl, 'dragend', this);
				}

				_disableDraggable(dragEl);
				dragEl.style['will-change'] = '';

				// Remove classes
				// ghostClass is added in dragStarted
				if (moved && !awaitingDragStarted) {
					toggleClass(dragEl, putSortable ? putSortable.options.ghostClass : this.options.ghostClass, false);
				}
				toggleClass(dragEl, this.options.chosenClass, false);

				// Drag stop event
				_dispatchEvent({
					sortable: this,
					name: 'unchoose',
					toEl: parentEl,
					newIndex: null,
					newDraggableIndex: null,
					originalEvent: evt
				});


				if (rootEl !== parentEl) {

					if (newIndex >= 0) {
						// Add event
						_dispatchEvent({
							rootEl: parentEl,
							name: 'add',
							toEl: parentEl,
							fromEl: rootEl,
							originalEvent: evt
						});

						// Remove event
						_dispatchEvent({
							sortable: this,
							name: 'remove',
							toEl: parentEl,
							originalEvent: evt
						});

						// drag from one list and drop into another
						_dispatchEvent({
							rootEl: parentEl,
							name: 'sort',
							toEl: parentEl,
							fromEl: rootEl,
							originalEvent: evt
						});

						_dispatchEvent({
							sortable: this,
							name: 'sort',
							toEl: parentEl,
							originalEvent: evt
						});
					}

					putSortable && putSortable.save();
				} else {
					if (newIndex !== oldIndex) {
						if (newIndex >= 0) {
							// drag & drop within the same list
							_dispatchEvent({
								sortable: this,
								name: 'update',
								toEl: parentEl,
								originalEvent: evt
							});

							_dispatchEvent({
								sortable: this,
								name: 'sort',
								toEl: parentEl,
								originalEvent: evt
							});
						}
					}
				}

				if (Sortable.active) {
					/* jshint eqnull:true */
					if (newIndex == null || newIndex === -1) {
						newIndex = oldIndex;
						newDraggableIndex = oldDraggableIndex;
					}

					_dispatchEvent({
						sortable: this,
						name: 'end',
						toEl: parentEl,
						originalEvent: evt
					});

					// Save sorting
					this.save();
				}
			}

		}
		this._nulling();
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/**Event*/evt) {
		let el = this.el,
			options = this.options;

		// Get the index of the dragged element within its parent
		newIndex = index(dragEl);
		newDraggableIndex = index(dragEl, options.draggable);

		pluginEvent('drop', this, {
			evt
		});

		parentEl = dragEl && dragEl.parentNode;

		// Get again after plugin event
		newIndex = index(dragEl);
		newDraggableIndex = index(dragEl, options.draggable);

		if (Sortable.eventCanceled) {
			this._nulling();
			return;
		}

		awaitingDragStarted = false;
		isCircumstantialInvert = false;
		pastFirstInvertThresh = false;

		clearInterval(this._loopId);

		clearTimeout(this._dragStartTimer);

		_cancelNextTick(this.cloneId);
		_cancelNextTick(this._dragStartId);

		// Unbind events
		if (this.nativeDraggable) {
			off(document, 'drop', this);
			off(el, 'dragstart', this._onDragStart);
		}
		this._offMoveEvents();
		this._offUpEvents();


		if (Safari) {
			css(document.body, 'user-select', '');
		}

		css(dragEl, 'transform', '');

		if (evt) {
			if (moved) {
				evt.cancelable && evt.preventDefault();
				!options.dropBubble && evt.stopPropagation();
			}

			ghostEl && ghostEl.parentNode && ghostEl.parentNode.removeChild(ghostEl);

			if (rootEl === parentEl || (putSortable && putSortable.lastPutMode !== 'clone')) {
				// Remove clone(s)
				cloneEl && cloneEl.parentNode && cloneEl.parentNode.removeChild(cloneEl);
			}

			if (dragEl) {
				if (this.nativeDraggable) {
					off(dragEl, 'dragend', this);
				}

				_disableDraggable(dragEl);
				dragEl.style['will-change'] = '';

				// Remove classes
				// ghostClass is added in dragStarted
				if (moved && !awaitingDragStarted) {
					toggleClass(dragEl, putSortable ? putSortable.options.ghostClass : this.options.ghostClass, false);
				}
				toggleClass(dragEl, this.options.chosenClass, false);

				// Drag stop event
				_dispatchEvent({
					sortable: this,
					name: 'unchoose',
					toEl: parentEl,
					newIndex: null,
					newDraggableIndex: null,
					originalEvent: evt
				});


				if (rootEl !== parentEl) {

					if (newIndex >= 0) {
						// Add event
						_dispatchEvent({
							rootEl: parentEl,
							name: 'add',
							toEl: parentEl,
							fromEl: rootEl,
							originalEvent: evt
						});

						// Remove event
						_dispatchEvent({
							sortable: this,
							name: 'remove',
							toEl: parentEl,
							originalEvent: evt
						});

						// drag from one list and drop into another
						_dispatchEvent({
							rootEl: parentEl,
							name: 'sort',
							toEl: parentEl,
							fromEl: rootEl,
							originalEvent: evt
						});

						_dispatchEvent({
							sortable: this,
							name: 'sort',
							toEl: parentEl,
							originalEvent: evt
						});
					}

					putSortable && putSortable.save();
				} else {
					if (newIndex !== oldIndex) {
						if (newIndex >= 0) {
							// drag & drop within the same list
							_dispatchEvent({
								sortable: this,
								name: 'update',
								toEl: parentEl,
								originalEvent: evt
							});

							_dispatchEvent({
								sortable: this,
								name: 'sort',
								toEl: parentEl,
								originalEvent: evt
							});
						}
					}
				}

				if (Sortable.active) {
					/* jshint eqnull:true */
					if (newIndex == null || newIndex === -1) {
						newIndex = oldIndex;
						newDraggableIndex = oldDraggableIndex;
					}

					_dispatchEvent({
						sortable: this,
						name: 'end',
						toEl: parentEl,
						originalEvent: evt
					});

					// Save sorting
					this.save();
				}
			}

		}
		this._nulling();
	}
```


---

### 🔹 Commit #09: `425cd357`
- **完整 Hash**: `425cd3576d5e5314644137a494561472a3d7081b`
- **說明 (Ground Truth)**: disable delayed drag events during destory
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:102, E:120, A:3) ➔ After(N:102, E:120, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `destroy()`
- **變更前簽章 (Before)**: `destroy()` (L1634~L1658)
- **變更後簽章 (After)**: `destroy()` (L1634~L1660)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function () {
		pluginEvent('destroy', this);
		let el = this.el;

		el[expando] = null;

		off(el, 'mousedown', this._onTapStart);
		off(el, 'touchstart', this._onTapStart);
		off(el, 'pointerdown', this._onTapStart);

		if (this.nativeDraggable) {
			off(el, 'dragover', this);
			off(el, 'dragenter', this);
		}
		// Remove draggable attributes
		Array.prototype.forEach.call(el.querySelectorAll('[draggable]'), function (el) {
			el.removeAttribute('draggable');
		});

		this._onDrop();

		sortables.splice(sortables.indexOf(this.el), 1);

		this.el = el = null;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function () {
		pluginEvent('destroy', this);
		let el = this.el;

		el[expando] = null;

		off(el, 'mousedown', this._onTapStart);
		off(el, 'touchstart', this._onTapStart);
		off(el, 'pointerdown', this._onTapStart);

		if (this.nativeDraggable) {
			off(el, 'dragover', this);
			off(el, 'dragenter', this);
		}
		// Remove draggable attributes
		Array.prototype.forEach.call(el.querySelectorAll('[draggable]'), function (el) {
			el.removeAttribute('draggable');
		});

		this._onDrop();

		this._disableDelayedDragEvents();

		sortables.splice(sortables.indexOf(this.el), 1);

		this.el = el = null;
	}
```


---

### 🔹 Commit #10: `0e4eabfe`
- **完整 Hash**: `0e4eabfef572f61df7a9cc38b5f56bbbc75d11ff`
- **說明 (Ground Truth)**: #1611: Remove MultiDrag events on GLOBAL destroy
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:102, E:119, A:3) ➔ After(N:102, E:119, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_onDrop()`
- **變更前簽章 (Before)**: `_onDrop(/**Event*/evt)` (L1275~L1442)
- **變更後簽章 (After)**: `_onDrop(/**Event*/evt)` (L1275~L1442)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/**Event*/evt) {
		let el = this.el,
			options = this.options;

		// Get the index of the dragged element within its parent
		newIndex = index(dragEl);
		newDraggableIndex = index(dragEl, options.draggable);

		pluginEvent('drop', this, {
			evt
		});

		parentEl = dragEl.parentNode;

		// Get again after plugin event
		newIndex = index(dragEl);
		newDraggableIndex = index(dragEl, options.draggable);

		if (Sortable.eventCanceled) {
			this._nulling();
			return;
		}

		awaitingDragStarted = false;
		isCircumstantialInvert = false;
		pastFirstInvertThresh = false;

		clearInterval(this._loopId);

		clearTimeout(this._dragStartTimer);

		_cancelNextTick(this.cloneId);
		_cancelNextTick(this._dragStartId);

		// Unbind events
		if (this.nativeDraggable) {
			off(document, 'drop', this);
			off(el, 'dragstart', this._onDragStart);
		}
		this._offMoveEvents();
		this._offUpEvents();


		if (Safari) {
			css(document.body, 'user-select', '');
		}


		if (evt) {
			if (moved) {
				evt.cancelable && evt.preventDefault();
				!options.dropBubble && evt.stopPropagation();
			}

			ghostEl && ghostEl.parentNode && ghostEl.parentNode.removeChild(ghostEl);

			if (rootEl === parentEl || (putSortable && putSortable.lastPutMode !== 'clone')) {
				// Remove clone(s)
				cloneEl && cloneEl.parentNode && cloneEl.parentNode.removeChild(cloneEl);
			}

			if (dragEl) {
				if (this.nativeDraggable) {
					off(dragEl, 'dragend', this);
				}

				_disableDraggable(dragEl);
				dragEl.style['will-change'] = '';

				// Remove classes
				// ghostClass is added in dragStarted
				if (moved && !awaitingDragStarted) {
					toggleClass(dragEl, putSortable ? putSortable.options.ghostClass : this.options.ghostClass, false);
				}
				toggleClass(dragEl, this.options.chosenClass, false);

				// Drag stop event
				_dispatchEvent({
					sortable: this,
					name: 'unchoose',
					toEl: parentEl,
					newIndex: null,
					newDraggableIndex: null,
					originalEvent: evt
				});


				if (rootEl !== parentEl) {

					if (newIndex >= 0) {
						// Add event
						_dispatchEvent({
							rootEl: parentEl,
							name: 'add',
							toEl: parentEl,
							fromEl: rootEl,
							originalEvent: evt
						});

						// Remove event
						_dispatchEvent({
							sortable: this,
							name: 'remove',
							toEl: parentEl,
							originalEvent: evt
						});

						// drag from one list and drop into another
						_dispatchEvent({
							rootEl: parentEl,
							name: 'sort',
							toEl: parentEl,
							fromEl: rootEl,
							originalEvent: evt
						});

						_dispatchEvent({
							sortable: this,
							name: 'sort',
							toEl: parentEl,
							originalEvent: evt
						});
					}

					putSortable && putSortable.save();
				} else {
					if (newIndex !== oldIndex) {
						if (newIndex >= 0) {
							// drag & drop within the same list
							_dispatchEvent({
								sortable: this,
								name: 'update',
								toEl: parentEl,
								originalEvent: evt
							});

							_dispatchEvent({
								sortable: this,
								name: 'sort',
								toEl: parentEl,
								originalEvent: evt
							});
						}
					}
				}

				if (Sortable.active) {
					/* jshint eqnull:true */
					if (newIndex == null || newIndex === -1) {
						newIndex = oldIndex;
						newDraggableIndex = oldDraggableIndex;
					}

					_dispatchEvent({
						sortable: this,
						name: 'end',
						toEl: parentEl,
						originalEvent: evt
					});

					// Save sorting
					this.save();
				}
			}

		}
		this._nulling();
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/**Event*/evt) {
		let el = this.el,
			options = this.options;

		// Get the index of the dragged element within its parent
		newIndex = index(dragEl);
		newDraggableIndex = index(dragEl, options.draggable);

		pluginEvent('drop', this, {
			evt
		});

		parentEl = dragEl && dragEl.parentNode;

		// Get again after plugin event
		newIndex = index(dragEl);
		newDraggableIndex = index(dragEl, options.draggable);

		if (Sortable.eventCanceled) {
			this._nulling();
			return;
		}

		awaitingDragStarted = false;
		isCircumstantialInvert = false;
		pastFirstInvertThresh = false;

		clearInterval(this._loopId);

		clearTimeout(this._dragStartTimer);

		_cancelNextTick(this.cloneId);
		_cancelNextTick(this._dragStartId);

		// Unbind events
		if (this.nativeDraggable) {
			off(document, 'drop', this);
			off(el, 'dragstart', this._onDragStart);
		}
		this._offMoveEvents();
		this._offUpEvents();


		if (Safari) {
			css(document.body, 'user-select', '');
		}


		if (evt) {
			if (moved) {
				evt.cancelable && evt.preventDefault();
				!options.dropBubble && evt.stopPropagation();
			}

			ghostEl && ghostEl.parentNode && ghostEl.parentNode.removeChild(ghostEl);

			if (rootEl === parentEl || (putSortable && putSortable.lastPutMode !== 'clone')) {
				// Remove clone(s)
				cloneEl && cloneEl.parentNode && cloneEl.parentNode.removeChild(cloneEl);
			}

			if (dragEl) {
				if (this.nativeDraggable) {
					off(dragEl, 'dragend', this);
				}

				_disableDraggable(dragEl);
				dragEl.style['will-change'] = '';

				// Remove classes
				// ghostClass is added in dragStarted
				if (moved && !awaitingDragStarted) {
					toggleClass(dragEl, putSortable ? putSortable.options.ghostClass : this.options.ghostClass, false);
				}
				toggleClass(dragEl, this.options.chosenClass, false);

				// Drag stop event
				_dispatchEvent({
					sortable: this,
					name: 'unchoose',
					toEl: parentEl,
					newIndex: null,
					newDraggableIndex: null,
					originalEvent: evt
				});


				if (rootEl !== parentEl) {

					if (newIndex >= 0) {
						// Add event
						_dispatchEvent({
							rootEl: parentEl,
							name: 'add',
							toEl: parentEl,
							fromEl: rootEl,
							originalEvent: evt
						});

						// Remove event
						_dispatchEvent({
							sortable: this,
							name: 'remove',
							toEl: parentEl,
							originalEvent: evt
						});

						// drag from one list and drop into another
						_dispatchEvent({
							rootEl: parentEl,
							name: 'sort',
							toEl: parentEl,
							fromEl: rootEl,
							originalEvent: evt
						});

						_dispatchEvent({
							sortable: this,
							name: 'sort',
							toEl: parentEl,
							originalEvent: evt
						});
					}

					putSortable && putSortable.save();
				} else {
					if (newIndex !== oldIndex) {
						if (newIndex >= 0) {
							// drag & drop within the same list
							_dispatchEvent({
								sortable: this,
								name: 'update',
								toEl: parentEl,
								originalEvent: evt
							});

							_dispatchEvent({
								sortable: this,
								name: 'sort',
								toEl: parentEl,
								originalEvent: evt
							});
						}
					}
				}

				if (Sortable.active) {
					/* jshint eqnull:true */
					if (newIndex == null || newIndex === -1) {
						newIndex = oldIndex;
						newDraggableIndex = oldDraggableIndex;
					}

					_dispatchEvent({
						sortable: this,
						name: 'end',
						toEl: parentEl,
						originalEvent: evt
					});

					// Save sorting
					this.save();
				}
			}

		}
		this._nulling();
	}
```


---

### 🔹 Commit #11: `1fed4eeb`
- **完整 Hash**: `1fed4eeb97c097bb0aa05bb65a52d833a53065b7`
- **說明 (Ground Truth)**: Improve OnSpill support with multiple sortables + fix drop events
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:102, E:119, A:3) ➔ After(N:102, E:119, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_onDrop()`
- **變更前簽章 (Before)**: `_onDrop(/**Event*/evt)` (L1275~L1440)
- **變更後簽章 (After)**: `_onDrop(/**Event*/evt)` (L1275~L1442)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function (/**Event*/evt) {
		let el = this.el,
			options = this.options;

		// Get the index of the dragged element within its parent
		newIndex = index(dragEl);
		newDraggableIndex = index(dragEl, options.draggable);

		pluginEvent('drop', this, {
			evt
		});

		// Get again after plugin event
		newIndex = index(dragEl);
		newDraggableIndex = index(dragEl, options.draggable);

		if (Sortable.eventCanceled) {
			this._nulling();
			return;
		}

		awaitingDragStarted = false;
		isCircumstantialInvert = false;
		pastFirstInvertThresh = false;

		clearInterval(this._loopId);

		clearTimeout(this._dragStartTimer);

		_cancelNextTick(this.cloneId);
		_cancelNextTick(this._dragStartId);

		// Unbind events
		if (this.nativeDraggable) {
			off(document, 'drop', this);
			off(el, 'dragstart', this._onDragStart);
		}
		this._offMoveEvents();
		this._offUpEvents();


		if (Safari) {
			css(document.body, 'user-select', '');
		}


		if (evt) {
			if (moved) {
				evt.cancelable && evt.preventDefault();
				!options.dropBubble && evt.stopPropagation();
			}

			ghostEl && ghostEl.parentNode && ghostEl.parentNode.removeChild(ghostEl);

			if (rootEl === parentEl || (putSortable && putSortable.lastPutMode !== 'clone')) {
				// Remove clone(s)
				cloneEl && cloneEl.parentNode && cloneEl.parentNode.removeChild(cloneEl);
			}

			if (dragEl) {
				if (this.nativeDraggable) {
					off(dragEl, 'dragend', this);
				}

				_disableDraggable(dragEl);
				dragEl.style['will-change'] = '';

				// Remove classes
				// ghostClass is added in dragStarted
				if (moved && !awaitingDragStarted) {
					toggleClass(dragEl, putSortable ? putSortable.options.ghostClass : this.options.ghostClass, false);
				}
				toggleClass(dragEl, this.options.chosenClass, false);

				// Drag stop event
				_dispatchEvent({
					sortable: this,
					name: 'unchoose',
					toEl: parentEl,
					newIndex: null,
					newDraggableIndex: null,
					originalEvent: evt
				});


				if (rootEl !== parentEl) {

					if (newIndex >= 0) {
						// Add event
						_dispatchEvent({
							rootEl: parentEl,
							name: 'add',
							toEl: parentEl,
							fromEl: rootEl,
							originalEvent: evt
						});

						// Remove event
						_dispatchEvent({
							sortable: this,
							name: 'remove',
							toEl: parentEl,
							originalEvent: evt
						});

						// drag from one list and drop into another
						_dispatchEvent({
							rootEl: parentEl,
							name: 'sort',
							toEl: parentEl,
							fromEl: rootEl,
							originalEvent: evt
						});

						_dispatchEvent({
							sortable: this,
							name: 'sort',
							toEl: parentEl,
							originalEvent: evt
						});
					}

					putSortable && putSortable.save();
				} else {
					if (newIndex !== oldIndex) {
						if (newIndex >= 0) {
							// drag & drop within the same list
							_dispatchEvent({
								sortable: this,
								name: 'update',
								toEl: parentEl,
								originalEvent: evt
							});

							_dispatchEvent({
								sortable: this,
								name: 'sort',
								toEl: parentEl,
								originalEvent: evt
							});
						}
					}
				}

				if (Sortable.active) {
					/* jshint eqnull:true */
					if (newIndex == null || newIndex === -1) {
						newIndex = oldIndex;
						newDraggableIndex = oldDraggableIndex;
					}

					_dispatchEvent({
						sortable: this,
						name: 'end',
						toEl: parentEl,
						originalEvent: evt
					});

					// Save sorting
					this.save();
				}
			}

		}
		this._nulling();
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function (/**Event*/evt) {
		let el = this.el,
			options = this.options;

		// Get the index of the dragged element within its parent
		newIndex = index(dragEl);
		newDraggableIndex = index(dragEl, options.draggable);

		pluginEvent('drop', this, {
			evt
		});

		parentEl = dragEl.parentNode;

		// Get again after plugin event
		newIndex = index(dragEl);
		newDraggableIndex = index(dragEl, options.draggable);

		if (Sortable.eventCanceled) {
			this._nulling();
			return;
		}

		awaitingDragStarted = false;
		isCircumstantialInvert = false;
		pastFirstInvertThresh = false;

		clearInterval(this._loopId);

		clearTimeout(this._dragStartTimer);

		_cancelNextTick(this.cloneId);
		_cancelNextTick(this._dragStartId);

		// Unbind events
		if (this.nativeDraggable) {
			off(document, 'drop', this);
			off(el, 'dragstart', this._onDragStart);
		}
		this._offMoveEvents();
		this._offUpEvents();


		if (Safari) {
			css(document.body, 'user-select', '');
		}


		if (evt) {
			if (moved) {
				evt.cancelable && evt.preventDefault();
				!options.dropBubble && evt.stopPropagation();
			}

			ghostEl && ghostEl.parentNode && ghostEl.parentNode.removeChild(ghostEl);

			if (rootEl === parentEl || (putSortable && putSortable.lastPutMode !== 'clone')) {
				// Remove clone(s)
				cloneEl && cloneEl.parentNode && cloneEl.parentNode.removeChild(cloneEl);
			}

			if (dragEl) {
				if (this.nativeDraggable) {
					off(dragEl, 'dragend', this);
				}

				_disableDraggable(dragEl);
				dragEl.style['will-change'] = '';

				// Remove classes
				// ghostClass is added in dragStarted
				if (moved && !awaitingDragStarted) {
					toggleClass(dragEl, putSortable ? putSortable.options.ghostClass : this.options.ghostClass, false);
				}
				toggleClass(dragEl, this.options.chosenClass, false);

				// Drag stop event
				_dispatchEvent({
					sortable: this,
					name: 'unchoose',
					toEl: parentEl,
					newIndex: null,
					newDraggableIndex: null,
					originalEvent: evt
				});


				if (rootEl !== parentEl) {

					if (newIndex >= 0) {
						// Add event
						_dispatchEvent({
							rootEl: parentEl,
							name: 'add',
							toEl: parentEl,
							fromEl: rootEl,
							originalEvent: evt
						});

						// Remove event
						_dispatchEvent({
							sortable: this,
							name: 'remove',
							toEl: parentEl,
							originalEvent: evt
						});

						// drag from one list and drop into another
						_dispatchEvent({
							rootEl: parentEl,
							name: 'sort',
							toEl: parentEl,
							fromEl: rootEl,
							originalEvent: evt
						});

						_dispatchEvent({
							sortable: this,
							name: 'sort',
							toEl: parentEl,
							originalEvent: evt
						});
					}

					putSortable && putSortable.save();
				} else {
					if (newIndex !== oldIndex) {
						if (newIndex >= 0) {
							// drag & drop within the same list
							_dispatchEvent({
								sortable: this,
								name: 'update',
								toEl: parentEl,
								originalEvent: evt
							});

							_dispatchEvent({
								sortable: this,
								name: 'sort',
								toEl: parentEl,
								originalEvent: evt
							});
						}
					}
				}

				if (Sortable.active) {
					/* jshint eqnull:true */
					if (newIndex == null || newIndex === -1) {
						newIndex = oldIndex;
						newDraggableIndex = oldDraggableIndex;
					}

					_dispatchEvent({
						sortable: this,
						name: 'end',
						toEl: parentEl,
						originalEvent: evt
					});

					// Save sorting
					this.save();
				}
			}

		}
		this._nulling();
	}
```


---

### 🔹 Commit #12: `e5b23967`
- **完整 Hash**: `e5b239674b76893f244c4a5248ea9e2962dd8ae0`
- **說明 (Ground Truth)**: Mark IOS as not supporting native drag & drop
- **變更檔案數**: 1

#### 📄 檔案: `src/Sortable.js`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:101, E:119, A:3) ➔ After(N:101, E:119, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_unhideGhostForTarget** `(Control)`
    └── 🎯 [CALLS] `on (External/Unresolved)()`
  🌲 **#document** `(Control)`
    └── ⚡ **on('click')**
        └── 🎯 [TRIGGERS] `on('click')_handler()`
  🌲 **#el** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #13: `87c9a063`
- **完整 Hash**: `87c9a063f82eeadf7d2a1f3a4c1f1dc61d2645e1`
- **說明 (Ground Truth)**: #1527: Added MultiDrag indicies event options
- **變更檔案數**: 1

#### 📄 檔案: `src/PluginManager.js`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:7, E:0, A:0) ➔ After(N:7, E:0, A:0)
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

### 🔹 函式: `getEventOptions()`
- **變更前簽章 (Before)**: `getEventOptions(name, sortable)` (L57~L67)
- **變更後簽章 (After)**: `getEventOptions(name, sortable)` (L57~L64)

#### ◀️ 變更前實作碼 (Before Implementation):
```
getEventOptions(name, sortable) {
		let eventOptions = {};
		for (let i in plugins) {
			if (typeof(plugins[i].eventOptions) !== 'function') continue;
			eventOptions = {
				...eventOptions,
				...plugins[i].eventOptions(name, sortable)
			};
		}
		return eventOptions;
	}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
getEventOptions(name, sortable) {
		let eventOptions = {};
		for (let i in plugins) {
			if (typeof(plugins[i].eventOptions) !== 'function') continue;
			Object.assign(eventOptions, plugins[i].eventOptions.call(sortable, name));
		}
		return eventOptions;
	}
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/Sortable show bd74abb22ade431c0e1af0cd552796ec1e0bcb0c
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff bd74abb22ade431c0e1af0cd552796ec1e0bcb0c~1 --file test_repos/Sortable/src/utils.js
   ```
