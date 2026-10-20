# 🔬 CODE-Map 基準審查獨立驗證報告: `gin`
> **技術生態**: `Go (前綴樹路由 / 中介軟體管線)`  
> **本地倉庫路徑**: `test_repos/gin`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 22 Files  
> **報告生成時間**: 2026-10-20 21:41:46  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `13` / `22` | `59.1%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `7` / `22` | `31.8%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `2` / `22` | `9.1%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`20` / `22`** | **`90.9%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `22` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `ea9fab99`
- **完整 Hash**: `ea9fab99e01d55a5e4f8daacc0d11ccffaee0a15`
- **說明 (Ground Truth)**: fix(tree): grow skippedNodes when pooled capacity is stale (#4852)
- **變更檔案數**: 1

#### 📄 檔案: `tree.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:52, E:53, A:0) ➔ After(N:52, E:54, A:0)
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
  • + [新增呼叫邊] `node.getValue` ──[CALLS]──> `append (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `node.getValue()`
- **變更前簽章 (Before)**: `func node.getValue(path string, params *Params, skippedNodes *[]skippedNode, unescape bool)` (L418~L673)
- **變更後簽章 (After)**: `func node.getValue(path string, params *Params, skippedNodes *[]skippedNode, unescape bool)` (L418~L672)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (n *node) getValue(path string, params *Params, skippedNodes *[]skippedNode, unescape bool) (value nodeValue) {
	var globalParamsCount int16

	// Reset the skipped-nodes stack on entry. getValue is called once per
	// method tree (e.g. in the HandleMethodNotAllowed loop) reusing the same
	// pooled Context stack, and the walk below grows it via a raw reslice that
	// cannot exceed engine.maxSections. Without this reset the residue from a
	// previous tree leaks into the next call and can panic with "slice bounds
	// out of range" once the accumulated length passes the capacity.
	*skippedNodes = (*skippedNodes)[:0]

walk: // Outer loop for walking the tree
	for {
		prefix := n.path
		if len(path) > len(prefix) {
			if path[:len(prefix)] == prefix {
				path = path[len(prefix):]

				// Try all the non-wildcard children first by matching the indices
				idxc := path[0]
				for i, c := range []byte(n.indices) {
					if c == idxc {
						//  strings.HasPrefix(n.children[len(n.children)-1].path, ":") == n.wildChild
						if n.wildChild {
							index := len(*skippedNodes)
							*skippedNodes = (*skippedNodes)[:index+1]
							(*skippedNodes)[index] = skippedNode{
								path: prefix + path,
								node: &node{
									path:      n.path,
									wildChild: n.wildChild,
									nType:     n.nType,
									priority:  n.priority,
									children:  n.children,
									handlers:  n.handlers,
									fullPath:  n.fullPath,
								},
								paramsCount: globalParamsCount,
							}
						}

						n = n.children[i]
						continue walk
					}
				}

				if !n.wildChild {
					// If the path at the end of the loop is not equal to '/' and the current node has no child nodes
					// the current node needs to roll back to last valid skippedNode
					if path != "/" {
						for length := len(*skippedNodes); length > 0; length-- {
							skippedNode := (*skippedNodes)[length-1]
							*skippedNodes = (*skippedNodes)[:length-1]
							if strings.HasSuffix(skippedNode.path, path) {
								path = skippedNode.path
								n = skippedNode.node
								if value.params != nil {
									*value.params = (*value.params)[:skippedNode.paramsCount]
								}
								globalParamsCount = skippedNode.paramsCount
								continue walk
							}
						}
					}

					// Nothing found.
					// We can recommend to redirect to the same URL without a
					// trailing slash if a leaf exists for that path.
					value.tsr = path == "/" && n.handlers != nil
					return value
				}

				// Handle wildcard child, which is always at the end of the array
				n = n.children[len(n.children)-1]
				globalParamsCount++

				switch n.nType {
				case param:
					// fix truncate the parameter
					// tree_test.go  line: 204

					// Find param end (either '/' or path end)
					end := 0
					for end < len(path) && path[end] != '/' {
						end++
					}

					// Save param value
					if params != nil {
						// Preallocate capacity if necessary
						if cap(*params) < int(globalParamsCount) {
							newParams := make(Params, len(*params), globalParamsCount)
							copy(newParams, *params)
							*params = newParams
						}

						if value.params == nil {
							value.params = params
						}
						// Expand slice within preallocated capacity
						i := len(*value.params)
						*value.params = (*value.params)[:i+1]
						val := path[:end]
						if unescape {
							if v, err := url.QueryUnescape(val); err == nil {
								val = v
							}
						}
						(*value.params)[i] = Param{
							Key:   n.path[1:],
							Value: val,
						}
					}

					// we need to go deeper!
					if end < len(path) {
						if len(n.children) > 0 {
							path = path[end:]
							n = n.children[0]
							continue walk
						}

						// ... but we can't
						value.tsr = len(path) == end+1
						return value
					}

					if value.handlers = n.handlers; value.handlers != nil {
						value.fullPath = n.fullPath
						return value
					}
					if len(n.children) == 1 {
						// No handle found. Check if a handle for this path + a
						// trailing slash exists for TSR recommendation
						n = n.children[0]
						value.tsr = (n.path == "/" && n.handlers != nil) || (n.path == "" && n.indices == "/")
					}
					return value

				case catchAll:
					// Save param value
					if params != nil {
						// Preallocate capacity if necessary
						if cap(*params) < int(globalParamsCount) {
							newParams := make(Params, len(*params), globalParamsCount)
							copy(newParams, *params)
							*params = newParams
						}

						if value.params == nil {
							value.params = params
						}
						// Expand slice within preallocated capacity
						i := len(*value.params)
						*value.params = (*value.params)[:i+1]
						val := path
						if unescape {
							if v, err := url.QueryUnescape(path); err == nil {
								val = v
							}
						}
						(*value.params)[i] = Param{
							Key:   n.path[2:],
							Value: val,
						}
					}

					value.handlers = n.handlers
					value.fullPath = n.fullPath
					return value

				default:
					panic("invalid node type")
				}
			}
		}

		if path == prefix {
			// If the current path does not equal '/' and the node does not have a registered handle and the most recently matched node has a child node
			// the current node needs to roll back to last valid skippedNode
			if n.handlers == nil && path != "/" {
				for length := len(*skippedNodes); length > 0; length-- {
					skippedNode := (*skippedNodes)[length-1]
					*skippedNodes = (*skippedNodes)[:length-1]
					if strings.HasSuffix(skippedNode.path, path) {
						path = skippedNode.path
						n = skippedNode.node
						if value.params != nil {
							*value.params = (*value.params)[:skippedNode.paramsCount]
						}
						globalParamsCount = skippedNode.paramsCount
						continue walk
					}
				}
				//	n = latestNode.children[len(latestNode.children)-1]
			}
			// We should have reached the node containing the handle.
			// Check if this node has a handle registered.
			if value.handlers = n.handlers; value.handlers != nil {
				value.fullPath = n.fullPath
				return value
			}

			// If there is no handle for this route, but this route has a
			// wildcard child, there must be a handle for this path with an
			// additional trailing slash
			if path == "/" && n.wildChild && n.nType != root {
				value.tsr = true
				return value
			}

			if path == "/" && n.nType == static {
				value.tsr = true
				return value
			}

			// No handle found. Check if a handle for this path + a
			// trailing slash exists for trailing slash recommendation
			for i, c := range []byte(n.indices) {
				if c == '/' {
					n = n.children[i]
					value.tsr = (len(n.path) == 1 && n.handlers != nil) ||
						(n.nType == catchAll && n.children[0].handlers != nil)
					return value
				}
			}

			return value
		}

		// Nothing found. We can recommend to redirect to the same URL with an
		// extra trailing slash if a leaf exists for that path
		value.tsr = path == "/" ||
			(len(prefix) == len(path)+1 && prefix[len(path)] == '/' &&
				path == prefix[:len(prefix)-1] && n.handlers != nil)

		// roll back to last valid skippedNode
		if !value.tsr && path != "/" {
			for length := len(*skippedNodes); length > 0; length-- {
				skippedNode := (*skippedNodes)[length-1]
				*skippedNodes = (*skippedNodes)[:length-1]
				if strings.HasSuffix(skippedNode.path, path) {
					path = skippedNode.path
					n = skippedNode.node
					if value.params != nil {
						*value.params = (*value.params)[:skippedNode.paramsCount]
					}
					globalParamsCount = skippedNode.paramsCount
					continue walk
				}
			}
		}

		return value
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (n *node) getValue(path string, params *Params, skippedNodes *[]skippedNode, unescape bool) (value nodeValue) {
	var globalParamsCount int16

	// Reset the skipped-nodes stack on entry. getValue is called once per
	// method tree (e.g. in the HandleMethodNotAllowed loop) reusing the same
	// pooled Context stack. Without this reset the residue from a previous
	// tree leaks into the next call. The walk grows the stack with append:
	// a context allocated before addRoute raised maxSections must still be
	// able to record one more backtrack frame. A raw reslice of the capacity
	// captured at pool allocation panics with "slice bounds out of range".
	*skippedNodes = (*skippedNodes)[:0]

walk: // Outer loop for walking the tree
	for {
		prefix := n.path
		if len(path) > len(prefix) {
			if path[:len(prefix)] == prefix {
				path = path[len(prefix):]

				// Try all the non-wildcard children first by matching the indices
				idxc := path[0]
				for i, c := range []byte(n.indices) {
					if c == idxc {
						//  strings.HasPrefix(n.children[len(n.children)-1].path, ":") == n.wildChild
						if n.wildChild {
							*skippedNodes = append(*skippedNodes, skippedNode{
								path: prefix + path,
								node: &node{
									path:      n.path,
									wildChild: n.wildChild,
									nType:     n.nType,
									priority:  n.priority,
									children:  n.children,
									handlers:  n.handlers,
									fullPath:  n.fullPath,
								},
								paramsCount: globalParamsCount,
							})
						}

						n = n.children[i]
						continue walk
					}
				}

				if !n.wildChild {
					// If the path at the end of the loop is not equal to '/' and the current node has no child nodes
					// the current node needs to roll back to last valid skippedNode
					if path != "/" {
						for length := len(*skippedNodes); length > 0; length-- {
							skippedNode := (*skippedNodes)[length-1]
							*skippedNodes = (*skippedNodes)[:length-1]
							if strings.HasSuffix(skippedNode.path, path) {
								path = skippedNode.path
								n = skippedNode.node
								if value.params != nil {
									*value.params = (*value.params)[:skippedNode.paramsCount]
								}
								globalParamsCount = skippedNode.paramsCount
								continue walk
							}
						}
					}

					// Nothing found.
					// We can recommend to redirect to the same URL without a
					// trailing slash if a leaf exists for that path.
					value.tsr = path == "/" && n.handlers != nil
					return value
				}

				// Handle wildcard child, which is always at the end of the array
				n = n.children[len(n.children)-1]
				globalParamsCount++

				switch n.nType {
				case param:
					// fix truncate the parameter
					// tree_test.go  line: 204

					// Find param end (either '/' or path end)
					end := 0
					for end < len(path) && path[end] != '/' {
						end++
					}

					// Save param value
					if params != nil {
						// Preallocate capacity if necessary
						if cap(*params) < int(globalParamsCount) {
							newParams := make(Params, len(*params), globalParamsCount)
							copy(newParams, *params)
							*params = newParams
						}

						if value.params == nil {
							value.params = params
						}
						// Expand slice within preallocated capacity
						i := len(*value.params)
						*value.params = (*value.params)[:i+1]
						val := path[:end]
						if unescape {
							if v, err := url.QueryUnescape(val); err == nil {
								val = v
							}
						}
						(*value.params)[i] = Param{
							Key:   n.path[1:],
							Value: val,
						}
					}

					// we need to go deeper!
					if end < len(path) {
						if len(n.children) > 0 {
							path = path[end:]
							n = n.children[0]
							continue walk
						}

						// ... but we can't
						value.tsr = len(path) == end+1
						return value
					}

					if value.handlers = n.handlers; value.handlers != nil {
						value.fullPath = n.fullPath
						return value
					}
					if len(n.children) == 1 {
						// No handle found. Check if a handle for this path + a
						// trailing slash exists for TSR recommendation
						n = n.children[0]
						value.tsr = (n.path == "/" && n.handlers != nil) || (n.path == "" && n.indices == "/")
					}
					return value

				case catchAll:
					// Save param value
					if params != nil {
						// Preallocate capacity if necessary
						if cap(*params) < int(globalParamsCount) {
							newParams := make(Params, len(*params), globalParamsCount)
							copy(newParams, *params)
							*params = newParams
						}

						if value.params == nil {
							value.params = params
						}
						// Expand slice within preallocated capacity
						i := len(*value.params)
						*value.params = (*value.params)[:i+1]
						val := path
						if unescape {
							if v, err := url.QueryUnescape(path); err == nil {
								val = v
							}
						}
						(*value.params)[i] = Param{
							Key:   n.path[2:],
							Value: val,
						}
					}

					value.handlers = n.handlers
					value.fullPath = n.fullPath
					return value

				default:
					panic("invalid node type")
				}
			}
		}

		if path == prefix {
			// If the current path does not equal '/' and the node does not have a registered handle and the most recently matched node has a child node
			// the current node needs to roll back to last valid skippedNode
			if n.handlers == nil && path != "/" {
				for length := len(*skippedNodes); length > 0; length-- {
					skippedNode := (*skippedNodes)[length-1]
					*skippedNodes = (*skippedNodes)[:length-1]
					if strings.HasSuffix(skippedNode.path, path) {
						path = skippedNode.path
						n = skippedNode.node
						if value.params != nil {
							*value.params = (*value.params)[:skippedNode.paramsCount]
						}
						globalParamsCount = skippedNode.paramsCount
						continue walk
					}
				}
				//	n = latestNode.children[len(latestNode.children)-1]
			}
			// We should have reached the node containing the handle.
			// Check if this node has a handle registered.
			if value.handlers = n.handlers; value.handlers != nil {
				value.fullPath = n.fullPath
				return value
			}

			// If there is no handle for this route, but this route has a
			// wildcard child, there must be a handle for this path with an
			// additional trailing slash
			if path == "/" && n.wildChild && n.nType != root {
				value.tsr = true
				return value
			}

			if path == "/" && n.nType == static {
				value.tsr = true
				return value
			}

			// No handle found. Check if a handle for this path + a
			// trailing slash exists for trailing slash recommendation
			for i, c := range []byte(n.indices) {
				if c == '/' {
					n = n.children[i]
					value.tsr = (len(n.path) == 1 && n.handlers != nil) ||
						(n.nType == catchAll && n.children[0].handlers != nil)
					return value
				}
			}

			return value
		}

		// Nothing found. We can recommend to redirect to the same URL with an
		// extra trailing slash if a leaf exists for that path
		value.tsr = path == "/" ||
			(len(prefix) == len(path)+1 && prefix[len(path)] == '/' &&
				path == prefix[:len(prefix)-1] && n.handlers != nil)

		// roll back to last valid skippedNode
		if !value.tsr && path != "/" {
			for length := len(*skippedNodes); length > 0; length-- {
				skippedNode := (*skippedNodes)[length-1]
				*skippedNodes = (*skippedNodes)[:length-1]
				if strings.HasSuffix(skippedNode.path, path) {
					path = skippedNode.path
					n = skippedNode.node
					if value.params != nil {
						*value.params = (*value.params)[:skippedNode.paramsCount]
					}
					globalParamsCount = skippedNode.paramsCount
					continue walk
				}
			}
		}

		return value
	}
}
```


---

### 🔹 Commit #02: `e8f24969`
- **完整 Hash**: `e8f24969d59611428b03d02424b8f4bb55a1ef91`
- **說明 (Ground Truth)**: feat(routergroup): include HTTP QUERY method in Any (#4878)
- **變更檔案數**: 1

#### 📄 檔案: `routergroup.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:49, E:55, A:0) ➔ After(N:49, E:55, A:0)
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

---

### 🔹 Commit #03: `1bd0ecf2`
- **完整 Hash**: `1bd0ecf2d3e08da37efa270bb7be20c1eddb0d68`
- **說明 (Ground Truth)**: fix(context): load Keys under the mutex in Copy (#4854)
- **變更檔案數**: 1

#### 📄 檔案: `context.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:244, E:260, A:0) ➔ After(N:244, E:260, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
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

### 🔹 函式: `Context.Copy()`
- **變更前簽章 (Before)**: `func Context.Copy()` (L122~L155)
- **變更後簽章 (After)**: `func Context.Copy()` (L122~L154)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Context) Copy() *Context {
	cp := Context{
		writermem: c.writermem,
		Request:   c.Request,
		engine:    c.engine,
	}

	cp.writermem.ResponseWriter = nil
	cp.Writer = &cp.writermem
	cp.index = abortIndex
	cp.handlers = nil
	cp.fullPath = c.fullPath

	cKeys := c.Keys
	c.mu.RLock()
	cp.Keys = maps.Clone(cKeys)
	c.mu.RUnlock()

	cParams := c.Params
	cp.Params = make([]Param, len(cParams))
	copy(cp.Params, cParams)

	if c.Errors != nil {
		cp.Errors = make(errorMsgs, len(c.Errors))
		copy(cp.Errors, c.Errors)
	}

	if c.Accepted != nil {
		cp.Accepted = make([]string, len(c.Accepted))
		copy(cp.Accepted, c.Accepted)
	}

	return &cp
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Context) Copy() *Context {
	cp := Context{
		writermem: c.writermem,
		Request:   c.Request,
		engine:    c.engine,
	}

	cp.writermem.ResponseWriter = nil
	cp.Writer = &cp.writermem
	cp.index = abortIndex
	cp.handlers = nil
	cp.fullPath = c.fullPath

	c.mu.RLock()
	cp.Keys = maps.Clone(c.Keys)
	c.mu.RUnlock()

	cParams := c.Params
	cp.Params = make([]Param, len(cParams))
	copy(cp.Params, cParams)

	if c.Errors != nil {
		cp.Errors = make(errorMsgs, len(c.Errors))
		copy(cp.Errors, c.Errors)
	}

	if c.Accepted != nil {
		cp.Accepted = make([]string, len(c.Accepted))
		copy(cp.Accepted, c.Accepted)
	}

	return &cp
}
```


---

### 🔹 Commit #04: `3b08cd72`
- **完整 Hash**: `3b08cd7235bd5ad2f055aa9e38135f111f6c5926`
- **說明 (Ground Truth)**: fix: reset skipped-nodes stack on getValue entry to prevent slice overflow panic [#4818] (#4819)
- **變更檔案數**: 1

#### 📄 檔案: `tree.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:52, E:53, A:0) ➔ After(N:52, E:53, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
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

### 🔹 函式: `node.getValue()`
- **變更前簽章 (Before)**: `func node.getValue(path string, params *Params, skippedNodes *[]skippedNode, unescape bool)` (L418~L665)
- **變更後簽章 (After)**: `func node.getValue(path string, params *Params, skippedNodes *[]skippedNode, unescape bool)` (L418~L673)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (n *node) getValue(path string, params *Params, skippedNodes *[]skippedNode, unescape bool) (value nodeValue) {
	var globalParamsCount int16

walk: // Outer loop for walking the tree
	for {
		prefix := n.path
		if len(path) > len(prefix) {
			if path[:len(prefix)] == prefix {
				path = path[len(prefix):]

				// Try all the non-wildcard children first by matching the indices
				idxc := path[0]
				for i, c := range []byte(n.indices) {
					if c == idxc {
						//  strings.HasPrefix(n.children[len(n.children)-1].path, ":") == n.wildChild
						if n.wildChild {
							index := len(*skippedNodes)
							*skippedNodes = (*skippedNodes)[:index+1]
							(*skippedNodes)[index] = skippedNode{
								path: prefix + path,
								node: &node{
									path:      n.path,
									wildChild: n.wildChild,
									nType:     n.nType,
									priority:  n.priority,
									children:  n.children,
									handlers:  n.handlers,
									fullPath:  n.fullPath,
								},
								paramsCount: globalParamsCount,
							}
						}

						n = n.children[i]
						continue walk
					}
				}

				if !n.wildChild {
					// If the path at the end of the loop is not equal to '/' and the current node has no child nodes
					// the current node needs to roll back to last valid skippedNode
					if path != "/" {
						for length := len(*skippedNodes); length > 0; length-- {
							skippedNode := (*skippedNodes)[length-1]
							*skippedNodes = (*skippedNodes)[:length-1]
							if strings.HasSuffix(skippedNode.path, path) {
								path = skippedNode.path
								n = skippedNode.node
								if value.params != nil {
									*value.params = (*value.params)[:skippedNode.paramsCount]
								}
								globalParamsCount = skippedNode.paramsCount
								continue walk
							}
						}
					}

					// Nothing found.
					// We can recommend to redirect to the same URL without a
					// trailing slash if a leaf exists for that path.
					value.tsr = path == "/" && n.handlers != nil
					return value
				}

				// Handle wildcard child, which is always at the end of the array
				n = n.children[len(n.children)-1]
				globalParamsCount++

				switch n.nType {
				case param:
					// fix truncate the parameter
					// tree_test.go  line: 204

					// Find param end (either '/' or path end)
					end := 0
					for end < len(path) && path[end] != '/' {
						end++
					}

					// Save param value
					if params != nil {
						// Preallocate capacity if necessary
						if cap(*params) < int(globalParamsCount) {
							newParams := make(Params, len(*params), globalParamsCount)
							copy(newParams, *params)
							*params = newParams
						}

						if value.params == nil {
							value.params = params
						}
						// Expand slice within preallocated capacity
						i := len(*value.params)
						*value.params = (*value.params)[:i+1]
						val := path[:end]
						if unescape {
							if v, err := url.QueryUnescape(val); err == nil {
								val = v
							}
						}
						(*value.params)[i] = Param{
							Key:   n.path[1:],
							Value: val,
						}
					}

					// we need to go deeper!
					if end < len(path) {
						if len(n.children) > 0 {
							path = path[end:]
							n = n.children[0]
							continue walk
						}

						// ... but we can't
						value.tsr = len(path) == end+1
						return value
					}

					if value.handlers = n.handlers; value.handlers != nil {
						value.fullPath = n.fullPath
						return value
					}
					if len(n.children) == 1 {
						// No handle found. Check if a handle for this path + a
						// trailing slash exists for TSR recommendation
						n = n.children[0]
						value.tsr = (n.path == "/" && n.handlers != nil) || (n.path == "" && n.indices == "/")
					}
					return value

				case catchAll:
					// Save param value
					if params != nil {
						// Preallocate capacity if necessary
						if cap(*params) < int(globalParamsCount) {
							newParams := make(Params, len(*params), globalParamsCount)
							copy(newParams, *params)
							*params = newParams
						}

						if value.params == nil {
							value.params = params
						}
						// Expand slice within preallocated capacity
						i := len(*value.params)
						*value.params = (*value.params)[:i+1]
						val := path
						if unescape {
							if v, err := url.QueryUnescape(path); err == nil {
								val = v
							}
						}
						(*value.params)[i] = Param{
							Key:   n.path[2:],
							Value: val,
						}
					}

					value.handlers = n.handlers
					value.fullPath = n.fullPath
					return value

				default:
					panic("invalid node type")
				}
			}
		}

		if path == prefix {
			// If the current path does not equal '/' and the node does not have a registered handle and the most recently matched node has a child node
			// the current node needs to roll back to last valid skippedNode
			if n.handlers == nil && path != "/" {
				for length := len(*skippedNodes); length > 0; length-- {
					skippedNode := (*skippedNodes)[length-1]
					*skippedNodes = (*skippedNodes)[:length-1]
					if strings.HasSuffix(skippedNode.path, path) {
						path = skippedNode.path
						n = skippedNode.node
						if value.params != nil {
							*value.params = (*value.params)[:skippedNode.paramsCount]
						}
						globalParamsCount = skippedNode.paramsCount
						continue walk
					}
				}
				//	n = latestNode.children[len(latestNode.children)-1]
			}
			// We should have reached the node containing the handle.
			// Check if this node has a handle registered.
			if value.handlers = n.handlers; value.handlers != nil {
				value.fullPath = n.fullPath
				return value
			}

			// If there is no handle for this route, but this route has a
			// wildcard child, there must be a handle for this path with an
			// additional trailing slash
			if path == "/" && n.wildChild && n.nType != root {
				value.tsr = true
				return value
			}

			if path == "/" && n.nType == static {
				value.tsr = true
				return value
			}

			// No handle found. Check if a handle for this path + a
			// trailing slash exists for trailing slash recommendation
			for i, c := range []byte(n.indices) {
				if c == '/' {
					n = n.children[i]
					value.tsr = (len(n.path) == 1 && n.handlers != nil) ||
						(n.nType == catchAll && n.children[0].handlers != nil)
					return value
				}
			}

			return value
		}

		// Nothing found. We can recommend to redirect to the same URL with an
		// extra trailing slash if a leaf exists for that path
		value.tsr = path == "/" ||
			(len(prefix) == len(path)+1 && prefix[len(path)] == '/' &&
				path == prefix[:len(prefix)-1] && n.handlers != nil)

		// roll back to last valid skippedNode
		if !value.tsr && path != "/" {
			for length := len(*skippedNodes); length > 0; length-- {
				skippedNode := (*skippedNodes)[length-1]
				*skippedNodes = (*skippedNodes)[:length-1]
				if strings.HasSuffix(skippedNode.path, path) {
					path = skippedNode.path
					n = skippedNode.node
					if value.params != nil {
						*value.params = (*value.params)[:skippedNode.paramsCount]
					}
					globalParamsCount = skippedNode.paramsCount
					continue walk
				}
			}
		}

		return value
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (n *node) getValue(path string, params *Params, skippedNodes *[]skippedNode, unescape bool) (value nodeValue) {
	var globalParamsCount int16

	// Reset the skipped-nodes stack on entry. getValue is called once per
	// method tree (e.g. in the HandleMethodNotAllowed loop) reusing the same
	// pooled Context stack, and the walk below grows it via a raw reslice that
	// cannot exceed engine.maxSections. Without this reset the residue from a
	// previous tree leaks into the next call and can panic with "slice bounds
	// out of range" once the accumulated length passes the capacity.
	*skippedNodes = (*skippedNodes)[:0]

walk: // Outer loop for walking the tree
	for {
		prefix := n.path
		if len(path) > len(prefix) {
			if path[:len(prefix)] == prefix {
				path = path[len(prefix):]

				// Try all the non-wildcard children first by matching the indices
				idxc := path[0]
				for i, c := range []byte(n.indices) {
					if c == idxc {
						//  strings.HasPrefix(n.children[len(n.children)-1].path, ":") == n.wildChild
						if n.wildChild {
							index := len(*skippedNodes)
							*skippedNodes = (*skippedNodes)[:index+1]
							(*skippedNodes)[index] = skippedNode{
								path: prefix + path,
								node: &node{
									path:      n.path,
									wildChild: n.wildChild,
									nType:     n.nType,
									priority:  n.priority,
									children:  n.children,
									handlers:  n.handlers,
									fullPath:  n.fullPath,
								},
								paramsCount: globalParamsCount,
							}
						}

						n = n.children[i]
						continue walk
					}
				}

				if !n.wildChild {
					// If the path at the end of the loop is not equal to '/' and the current node has no child nodes
					// the current node needs to roll back to last valid skippedNode
					if path != "/" {
						for length := len(*skippedNodes); length > 0; length-- {
							skippedNode := (*skippedNodes)[length-1]
							*skippedNodes = (*skippedNodes)[:length-1]
							if strings.HasSuffix(skippedNode.path, path) {
								path = skippedNode.path
								n = skippedNode.node
								if value.params != nil {
									*value.params = (*value.params)[:skippedNode.paramsCount]
								}
								globalParamsCount = skippedNode.paramsCount
								continue walk
							}
						}
					}

					// Nothing found.
					// We can recommend to redirect to the same URL without a
					// trailing slash if a leaf exists for that path.
					value.tsr = path == "/" && n.handlers != nil
					return value
				}

				// Handle wildcard child, which is always at the end of the array
				n = n.children[len(n.children)-1]
				globalParamsCount++

				switch n.nType {
				case param:
					// fix truncate the parameter
					// tree_test.go  line: 204

					// Find param end (either '/' or path end)
					end := 0
					for end < len(path) && path[end] != '/' {
						end++
					}

					// Save param value
					if params != nil {
						// Preallocate capacity if necessary
						if cap(*params) < int(globalParamsCount) {
							newParams := make(Params, len(*params), globalParamsCount)
							copy(newParams, *params)
							*params = newParams
						}

						if value.params == nil {
							value.params = params
						}
						// Expand slice within preallocated capacity
						i := len(*value.params)
						*value.params = (*value.params)[:i+1]
						val := path[:end]
						if unescape {
							if v, err := url.QueryUnescape(val); err == nil {
								val = v
							}
						}
						(*value.params)[i] = Param{
							Key:   n.path[1:],
							Value: val,
						}
					}

					// we need to go deeper!
					if end < len(path) {
						if len(n.children) > 0 {
							path = path[end:]
							n = n.children[0]
							continue walk
						}

						// ... but we can't
						value.tsr = len(path) == end+1
						return value
					}

					if value.handlers = n.handlers; value.handlers != nil {
						value.fullPath = n.fullPath
						return value
					}
					if len(n.children) == 1 {
						// No handle found. Check if a handle for this path + a
						// trailing slash exists for TSR recommendation
						n = n.children[0]
						value.tsr = (n.path == "/" && n.handlers != nil) || (n.path == "" && n.indices == "/")
					}
					return value

				case catchAll:
					// Save param value
					if params != nil {
						// Preallocate capacity if necessary
						if cap(*params) < int(globalParamsCount) {
							newParams := make(Params, len(*params), globalParamsCount)
							copy(newParams, *params)
							*params = newParams
						}

						if value.params == nil {
							value.params = params
						}
						// Expand slice within preallocated capacity
						i := len(*value.params)
						*value.params = (*value.params)[:i+1]
						val := path
						if unescape {
							if v, err := url.QueryUnescape(path); err == nil {
								val = v
							}
						}
						(*value.params)[i] = Param{
							Key:   n.path[2:],
							Value: val,
						}
					}

					value.handlers = n.handlers
					value.fullPath = n.fullPath
					return value

				default:
					panic("invalid node type")
				}
			}
		}

		if path == prefix {
			// If the current path does not equal '/' and the node does not have a registered handle and the most recently matched node has a child node
			// the current node needs to roll back to last valid skippedNode
			if n.handlers == nil && path != "/" {
				for length := len(*skippedNodes); length > 0; length-- {
					skippedNode := (*skippedNodes)[length-1]
					*skippedNodes = (*skippedNodes)[:length-1]
					if strings.HasSuffix(skippedNode.path, path) {
						path = skippedNode.path
						n = skippedNode.node
						if value.params != nil {
							*value.params = (*value.params)[:skippedNode.paramsCount]
						}
						globalParamsCount = skippedNode.paramsCount
						continue walk
					}
				}
				//	n = latestNode.children[len(latestNode.children)-1]
			}
			// We should have reached the node containing the handle.
			// Check if this node has a handle registered.
			if value.handlers = n.handlers; value.handlers != nil {
				value.fullPath = n.fullPath
				return value
			}

			// If there is no handle for this route, but this route has a
			// wildcard child, there must be a handle for this path with an
			// additional trailing slash
			if path == "/" && n.wildChild && n.nType != root {
				value.tsr = true
				return value
			}

			if path == "/" && n.nType == static {
				value.tsr = true
				return value
			}

			// No handle found. Check if a handle for this path + a
			// trailing slash exists for trailing slash recommendation
			for i, c := range []byte(n.indices) {
				if c == '/' {
					n = n.children[i]
					value.tsr = (len(n.path) == 1 && n.handlers != nil) ||
						(n.nType == catchAll && n.children[0].handlers != nil)
					return value
				}
			}

			return value
		}

		// Nothing found. We can recommend to redirect to the same URL with an
		// extra trailing slash if a leaf exists for that path
		value.tsr = path == "/" ||
			(len(prefix) == len(path)+1 && prefix[len(path)] == '/' &&
				path == prefix[:len(prefix)-1] && n.handlers != nil)

		// roll back to last valid skippedNode
		if !value.tsr && path != "/" {
			for length := len(*skippedNodes); length > 0; length-- {
				skippedNode := (*skippedNodes)[length-1]
				*skippedNodes = (*skippedNodes)[:length-1]
				if strings.HasSuffix(skippedNode.path, path) {
					path = skippedNode.path
					n = skippedNode.node
					if value.params != nil {
						*value.params = (*value.params)[:skippedNode.paramsCount]
					}
					globalParamsCount = skippedNode.paramsCount
					continue walk
				}
			}
		}

		return value
	}
}
```


---

### 🔹 Commit #05: `d8f2d588`
- **完整 Hash**: `d8f2d588d7573b3438cfc95b7a47f9ec8966273c`
- **說明 (Ground Truth)**: fix(engine): add default ReadHeaderTimeout to http.Server in Run methods (#4800)
- **變更檔案數**: 1

#### 📄 檔案: `gin.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:125, E:175, A:0) ➔ After(N:127, E:178, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 3, -Edges: 0, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `defaultReadHeaderTimeout` (MODULE_STATE)
  • + [新增節點] `Engine.getReadHeaderTimeout` (FUNCTION_DEF)
  • + [新增呼叫邊] `Engine.Run` ──[CALLS]──> `Engine.getReadHeaderTimeout`
  • + [新增呼叫邊] `Engine.RunTLS` ──[CALLS]──> `Engine.getReadHeaderTimeout`
  • + [新增呼叫邊] `Engine.RunListener` ──[CALLS]──> `Engine.getReadHeaderTimeout`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Engine.RunTLS()`
- **變更前簽章 (Before)**: `func Engine.RunTLS(addr, certFile, keyFile string)` (L561~L576)
- **變更後簽章 (After)**: `func Engine.RunTLS(addr, certFile, keyFile string)` (L588~L604)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (engine *Engine) RunTLS(addr, certFile, keyFile string) (err error) {
	debugPrint("Listening and serving HTTPS on %s\n", addr)
	defer func() { debugPrintError(err) }()

	if engine.isUnsafeTrustedProxies() {
		debugPrint("[WARNING] You trusted all proxies, this is NOT safe. We recommend you to set a value.\n" +
			"Please check https://github.com/gin-gonic/gin/blob/master/docs/doc.md#dont-trust-all-proxies for details.")
	}

	server := &http.Server{ // #nosec G112
		Addr:    addr,
		Handler: engine.Handler(),
	}
	err = server.ListenAndServeTLS(certFile, keyFile)
	return
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (engine *Engine) RunTLS(addr, certFile, keyFile string) (err error) {
	debugPrint("Listening and serving HTTPS on %s\n", addr)
	defer func() { debugPrintError(err) }()

	if engine.isUnsafeTrustedProxies() {
		debugPrint("[WARNING] You trusted all proxies, this is NOT safe. We recommend you to set a value.\n" +
			"Please check https://github.com/gin-gonic/gin/blob/master/docs/doc.md#dont-trust-all-proxies for details.")
	}

	server := &http.Server{ // #nosec G112
		Addr:              addr,
		Handler:           engine.Handler(),
		ReadHeaderTimeout: engine.getReadHeaderTimeout(),
	}
	err = server.ListenAndServeTLS(certFile, keyFile)
	return
}
```

### 🔹 函式: `Engine.RunListener()`
- **變更前簽章 (Before)**: `func Engine.RunListener(listener net.Listener)` (L645~L659)
- **變更後簽章 (After)**: `func Engine.RunListener(listener net.Listener)` (L673~L688)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (engine *Engine) RunListener(listener net.Listener) (err error) {
	debugPrint("Listening and serving HTTP on listener what's bind with address@%s", listener.Addr())
	defer func() { debugPrintError(err) }()

	if engine.isUnsafeTrustedProxies() {
		debugPrint("[WARNING] You trusted all proxies, this is NOT safe. We recommend you to set a value.\n" +
			"Please check https://github.com/gin-gonic/gin/blob/master/docs/doc.md#dont-trust-all-proxies for details.")
	}

	server := &http.Server{ // #nosec G112
		Handler: engine.Handler(),
	}
	err = server.Serve(listener)
	return
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (engine *Engine) RunListener(listener net.Listener) (err error) {
	debugPrint("Listening and serving HTTP on listener what's bind with address@%s", listener.Addr())
	defer func() { debugPrintError(err) }()

	if engine.isUnsafeTrustedProxies() {
		debugPrint("[WARNING] You trusted all proxies, this is NOT safe. We recommend you to set a value.\n" +
			"Please check https://github.com/gin-gonic/gin/blob/master/docs/doc.md#dont-trust-all-proxies for details.")
	}

	server := &http.Server{ // #nosec G112
		Handler:           engine.Handler(),
		ReadHeaderTimeout: engine.getReadHeaderTimeout(),
	}
	err = server.Serve(listener)
	return
}
```

### 🔹 函式: `Engine.Run()`
- **變更前簽章 (Before)**: `func Engine.Run(addr ...string)` (L540~L556)
- **變更後簽章 (After)**: `func Engine.Run(addr ...string)` (L566~L583)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (engine *Engine) Run(addr ...string) (err error) {
	defer func() { debugPrintError(err) }()

	if engine.isUnsafeTrustedProxies() {
		debugPrint("[WARNING] You trusted all proxies, this is NOT safe. We recommend you to set a value.\n" +
			"Please check https://github.com/gin-gonic/gin/blob/master/docs/doc.md#dont-trust-all-proxies for details.")
	}
	engine.updateRouteTrees()
	address := resolveAddress(addr)
	debugPrint("Listening and serving HTTP on %s\n", address)
	server := &http.Server{ // #nosec G112
		Addr:    address,
		Handler: engine.Handler(),
	}
	err = server.ListenAndServe()
	return
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (engine *Engine) Run(addr ...string) (err error) {
	defer func() { debugPrintError(err) }()

	if engine.isUnsafeTrustedProxies() {
		debugPrint("[WARNING] You trusted all proxies, this is NOT safe. We recommend you to set a value.\n" +
			"Please check https://github.com/gin-gonic/gin/blob/master/docs/doc.md#dont-trust-all-proxies for details.")
	}
	engine.updateRouteTrees()
	address := resolveAddress(addr)
	debugPrint("Listening and serving HTTP on %s\n", address)
	server := &http.Server{ // #nosec G112
		Addr:              address,
		Handler:           engine.Handler(),
		ReadHeaderTimeout: engine.getReadHeaderTimeout(),
	}
	err = server.ListenAndServe()
	return
}
```

### 🔹 函式: `New()`
- **變更前簽章 (Before)**: `func New(opts ...OptionFunc)` (L202~L233)
- **變更後簽章 (After)**: `func New(opts ...OptionFunc)` (L215~L247)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func New(opts ...OptionFunc) *Engine {
	debugPrintWARNINGNew()
	engine := &Engine{
		RouterGroup: RouterGroup{
			Handlers: nil,
			basePath: "/",
			root:     true,
		},
		FuncMap:                template.FuncMap{},
		RedirectTrailingSlash:  true,
		RedirectFixedPath:      false,
		HandleMethodNotAllowed: false,
		ForwardedByClientIP:    true,
		RemoteIPHeaders:        []string{"X-Forwarded-For", "X-Real-IP"},
		TrustedPlatform:        defaultPlatform,
		UseRawPath:             false,
		UseEscapedPath:         false,
		RemoveExtraSlash:       false,
		UnescapePathValues:     true,
		MaxMultipartMemory:     defaultMultipartMemory,
		trees:                  make(methodTrees, 0, 9),
		delims:                 render.Delims{Left: "{{", Right: "}}"},
		secureJSONPrefix:       "while(1);",
		trustedProxies:         []string{"0.0.0.0/0", "::/0"},
		trustedCIDRs:           defaultTrustedCIDRs,
	}
	engine.engine = engine
	engine.pool.New = func() any {
		return engine.allocateContext(engine.maxParams)
	}
	return engine.With(opts...)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func New(opts ...OptionFunc) *Engine {
	debugPrintWARNINGNew()
	engine := &Engine{
		RouterGroup: RouterGroup{
			Handlers: nil,
			basePath: "/",
			root:     true,
		},
		FuncMap:                template.FuncMap{},
		RedirectTrailingSlash:  true,
		RedirectFixedPath:      false,
		HandleMethodNotAllowed: false,
		ForwardedByClientIP:    true,
		RemoteIPHeaders:        []string{"X-Forwarded-For", "X-Real-IP"},
		TrustedPlatform:        defaultPlatform,
		UseRawPath:             false,
		UseEscapedPath:         false,
		RemoveExtraSlash:       false,
		UnescapePathValues:     true,
		MaxMultipartMemory:     defaultMultipartMemory,
		ReadHeaderTimeout:      defaultReadHeaderTimeout,
		trees:                  make(methodTrees, 0, 9),
		delims:                 render.Delims{Left: "{{", Right: "}}"},
		secureJSONPrefix:       "while(1);",
		trustedProxies:         []string{"0.0.0.0/0", "::/0"},
		trustedCIDRs:           defaultTrustedCIDRs,
	}
	engine.engine = engine
	engine.pool.New = func() any {
		return engine.allocateContext(engine.maxParams)
	}
	return engine.With(opts...)
}
```


---

### 🔹 Commit #06: `b1f77cf5`
- **完整 Hash**: `b1f77cf536154f67e3332fc5d0965b891be86606`
- **說明 (Ground Truth)**: feat(gin): add support for the HTTP QUERY method (RFC 10008) (#4806)
- **變更檔案數**: 2

#### 📄 檔案: `ginS/gins.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:27, E:50, A:0) ➔ After(N:28, E:52, A:0)
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
  • + [新增節點] `QUERY` (FUNCTION_DEF)
  • + [新增呼叫邊] `QUERY` ──[CALLS]──> `QUERY`
  • + [新增呼叫邊] `QUERY` ──[CALLS]──> `engine (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `routergroup.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:49, E:55, A:0) ➔ After(N:49, E:55, A:0)
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
  • + [新增節點] `MethodQuery` (MODULE_STATE)
  • - [移除節點] `_` (MODULE_STATE)

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `RouterGroup.QUERY()`
- **變更前簽章 (Before)**: `func RouterGroup.QUERY(relativePath string, handlers ...HandlerFunc)` (L150~L152)
- **變更後簽章 (After)**: `func RouterGroup.QUERY(relativePath string, handlers ...HandlerFunc)` (L176~L178)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (group *RouterGroup) QUERY(relativePath string, handlers ...HandlerFunc) IRoutes {
	return group.handle("QUERY", relativePath, handlers)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (group *RouterGroup) QUERY(relativePath string, handlers ...HandlerFunc) IRoutes {
	return group.handle(MethodQuery, relativePath, handlers)
}
```


---

### 🔹 Commit #07: `5c6a15f8`
- **完整 Hash**: `5c6a15f8f9566612076bd209e623861bf92a6283`
- **說明 (Ground Truth)**: fix(context): handle missing HTML renderer (#4805)
- **變更檔案數**: 2

#### 📄 檔案: `context.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:244, E:260, A:0) ➔ After(N:244, E:260, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
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

### 🔹 函式: `Context.HTML()`
- **變更前簽章 (Before)**: `func Context.HTML(code int, name string, obj any)` (L1221~L1224)
- **變更後簽章 (After)**: `func Context.HTML(code int, name string, obj any)` (L1221~L1229)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Context) HTML(code int, name string, obj any) {
	instance := c.engine.HTMLRender.Instance(name, obj)
	c.Render(code, instance)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Context) HTML(code int, name string, obj any) {
	if c.engine.HTMLRender == nil {
		c.Render(code, render.HTML{})
		return
	}

	instance := c.engine.HTMLRender.Instance(name, obj)
	c.Render(code, instance)
}
```


#### 📄 檔案: `render/html.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:18, E:14, A:0) ➔ After(N:19, E:14, A:0)
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
  • + [新增節點] `errHTMLRendererNotConfigured` (MODULE_STATE)

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `HTML.Render()`
- **變更前簽章 (Before)**: `func HTML.Render(w http.ResponseWriter)` (L89~L96)
- **變更後簽章 (After)**: `func HTML.Render(w http.ResponseWriter)` (L92~L102)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (r HTML) Render(w http.ResponseWriter) error {
	r.WriteContentType(w)

	if r.Name == "" {
		return r.Template.Execute(w, r.Data)
	}
	return r.Template.ExecuteTemplate(w, r.Name, r.Data)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (r HTML) Render(w http.ResponseWriter) error {
	r.WriteContentType(w)
	if r.Template == nil {
		return errHTMLRendererNotConfigured
	}

	if r.Name == "" {
		return r.Template.Execute(w, r.Data)
	}
	return r.Template.ExecuteTemplate(w, r.Name, r.Data)
}
```


---

### 🔹 Commit #08: `2a1a14ff`
- **完整 Hash**: `2a1a14ff37a26ca6a76763ecc33727c23d9284e9`
- **說明 (Ground Truth)**: feat(router): add QUERY method shortcut for RFC 10008 (#4830)
- **變更檔案數**: 1

#### 📄 檔案: `routergroup.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:48, E:54, A:0) ➔ After(N:49, E:55, A:0)
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
  • + [新增節點] `RouterGroup.QUERY` (FUNCTION_DEF)
  • + [新增呼叫邊] `RouterGroup.QUERY` ──[CALLS]──> `RouterGroup.handle`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #09: `d9307dbc`
- **完整 Hash**: `d9307dbcbbe796a64d9e0ef23452da888dd7f904`
- **說明 (Ground Truth)**: fix(context): skip chmod on pre-existing dirs in SaveUploadedFile (#4702)
- **變更檔案數**: 1

#### 📄 檔案: `context.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:243, E:258, A:0) ➔ After(N:244, E:260, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `os.Stat (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Context.SaveUploadedFile` ──[CALLS]──> `os.Stat (External/Pkg)`
  • + [新增呼叫邊] `Context.SaveUploadedFile` ──[CALLS]──> `errors.Is (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Context.SaveUploadedFile()`
- **變更前簽章 (Before)**: `func Context.SaveUploadedFile(file *multipart.FileHeader, dst string, perm ...fs.FileMode)` (L729~L756)
- **變更後簽章 (After)**: `func Context.SaveUploadedFile(file *multipart.FileHeader, dst string, perm ...fs.FileMode)` (L734~L769)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Context) SaveUploadedFile(file *multipart.FileHeader, dst string, perm ...fs.FileMode) error {
	src, err := file.Open()
	if err != nil {
		return err
	}
	defer src.Close()

	var mode os.FileMode = 0o750
	if len(perm) > 0 {
		mode = perm[0]
	}
	dir := filepath.Dir(dst)
	if err = os.MkdirAll(dir, mode); err != nil {
		return err
	}
	if err = os.Chmod(dir, mode); err != nil {
		return err
	}

	out, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, src)
	return err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Context) SaveUploadedFile(file *multipart.FileHeader, dst string, perm ...fs.FileMode) error {
	src, err := file.Open()
	if err != nil {
		return err
	}
	defer src.Close()

	var mode os.FileMode = 0o750
	if len(perm) > 0 {
		mode = perm[0]
	}
	dir := filepath.Dir(dst)
	// Record whether the destination directory exists before MkdirAll, so we
	// only chmod a directory we just created. Chmod'ing a pre-existing directory
	// the process does not own (e.g. /tmp) fails with "operation not permitted"
	// (#4622). A non-ErrNotExist stat error also skips chmod and lets MkdirAll
	// surface the underlying failure.
	_, statErr := os.Stat(dir)
	if err = os.MkdirAll(dir, mode); err != nil {
		return err
	}
	if errors.Is(statErr, os.ErrNotExist) {
		if err = os.Chmod(dir, mode); err != nil {
			return err
		}
	}

	out, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, src)
	return err
}
```


---

### 🔹 Commit #10: `4a3eb31f`
- **完整 Hash**: `4a3eb31fb15b2a2d78b4bdbe0c31a2c564b1977a`
- **說明 (Ground Truth)**: fix(recovery): record recovered panics in c.Errors (#4698)
- **變更檔案數**: 1

#### 📄 檔案: `recovery.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:47, E:43, A:0) ➔ After(N:48, E:45, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `fmt.Errorf (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `defaultHandleRecovery` ──[CALLS]──> `fmt.Errorf (External/Pkg)`
  • + [新增呼叫邊] `defaultHandleRecovery` ──[CALLS]──> `c.Error (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `defaultHandleRecovery()`
- **變更前簽章 (Before)**: `func defaultHandleRecovery(c *Context, _ any)` (L109~L111)
- **變更後簽章 (After)**: `func defaultHandleRecovery(c *Context, err any)` (L109~L116)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func defaultHandleRecovery(c *Context, _ any) {
	c.AbortWithStatus(http.StatusInternalServerError)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func defaultHandleRecovery(c *Context, err any) {
	e, ok := err.(error)
	if !ok {
		e = fmt.Errorf("%v", err)
	}
	c.Error(e) //nolint: errcheck
	c.AbortWithStatus(http.StatusInternalServerError)
}
```


---

### 🔹 Commit #11: `293ad7ed`
- **完整 Hash**: `293ad7edebb3ae30369288bd6416ca0d78474727`
- **說明 (Ground Truth)**: fix(context): Copy() copies Errors and Accepted fields (#4695)
- **變更檔案數**: 1

#### 📄 檔案: `context.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:243, E:258, A:0) ➔ After(N:243, E:258, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
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

### 🔹 函式: `Context.Copy()`
- **變更前簽章 (Before)**: `func Context.Copy()` (L122~L145)
- **變更後簽章 (After)**: `func Context.Copy()` (L122~L155)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Context) Copy() *Context {
	cp := Context{
		writermem: c.writermem,
		Request:   c.Request,
		engine:    c.engine,
	}

	cp.writermem.ResponseWriter = nil
	cp.Writer = &cp.writermem
	cp.index = abortIndex
	cp.handlers = nil
	cp.fullPath = c.fullPath

	cKeys := c.Keys
	c.mu.RLock()
	cp.Keys = maps.Clone(cKeys)
	c.mu.RUnlock()

	cParams := c.Params
	cp.Params = make([]Param, len(cParams))
	copy(cp.Params, cParams)

	return &cp
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Context) Copy() *Context {
	cp := Context{
		writermem: c.writermem,
		Request:   c.Request,
		engine:    c.engine,
	}

	cp.writermem.ResponseWriter = nil
	cp.Writer = &cp.writermem
	cp.index = abortIndex
	cp.handlers = nil
	cp.fullPath = c.fullPath

	cKeys := c.Keys
	c.mu.RLock()
	cp.Keys = maps.Clone(cKeys)
	c.mu.RUnlock()

	cParams := c.Params
	cp.Params = make([]Param, len(cParams))
	copy(cp.Params, cParams)

	if c.Errors != nil {
		cp.Errors = make(errorMsgs, len(c.Errors))
		copy(cp.Errors, c.Errors)
	}

	if c.Accepted != nil {
		cp.Accepted = make([]string, len(c.Accepted))
		copy(cp.Accepted, c.Accepted)
	}

	return &cp
}
```


---

### 🔹 Commit #12: `d75fcd4c`
- **完整 Hash**: `d75fcd4c9ab260e5225de590f1f0f8c0e0e12d11`
- **說明 (Ground Truth)**: fix(response): panic on Hijack/CloseNotify when wrapper unsupported (#4645)
- **變更檔案數**: 1

#### 📄 檔案: `response_writer.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:16, E:12, A:0) ➔ After(N:16, E:12, A:0)
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

### 🔹 函式: `responseWriter.Hijack()`
- **變更前簽章 (Before)**: `func responseWriter.Hijack()` (L111~L121)
- **變更後簽章 (After)**: `func responseWriter.Hijack()` (L111~L125)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (w *responseWriter) Hijack() (net.Conn, *bufio.ReadWriter, error) {
	// Allow hijacking before any data is written (size == -1) or after headers are written (size == 0),
	// but not after body data is written (size > 0). For compatibility with websocket libraries (e.g., github.com/coder/websocket)
	if w.size > 0 {
		return nil, nil, errHijackAlreadyWritten
	}
	if w.size < 0 {
		w.size = 0
	}
	return w.ResponseWriter.(http.Hijacker).Hijack()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (w *responseWriter) Hijack() (net.Conn, *bufio.ReadWriter, error) {
	// Allow hijacking before any data is written (size == -1) or after headers are written (size == 0),
	// but not after body data is written (size > 0). For compatibility with websocket libraries (e.g., github.com/coder/websocket)
	if w.size > 0 {
		return nil, nil, errHijackAlreadyWritten
	}
	hijacker, ok := w.ResponseWriter.(http.Hijacker)
	if !ok {
		return nil, nil, http.ErrNotSupported
	}
	if w.size < 0 {
		w.size = 0
	}
	return hijacker.Hijack()
}
```

### 🔹 函式: `responseWriter.CloseNotify()`
- **變更前簽章 (Before)**: `func responseWriter.CloseNotify()` (L124~L126)
- **變更後簽章 (After)**: `func responseWriter.CloseNotify()` (L128~L133)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (w *responseWriter) CloseNotify() <-chan bool {
	return w.ResponseWriter.(http.CloseNotifier).CloseNotify()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (w *responseWriter) CloseNotify() <-chan bool {
	if cn, ok := w.ResponseWriter.(http.CloseNotifier); ok {
		return cn.CloseNotify()
	}
	return nil
}
```


---

### 🔹 Commit #13: `96ece6a1`
- **完整 Hash**: `96ece6a14123923d00081320486042f568adef32`
- **說明 (Ground Truth)**: feat(context): add Scheme() with proper reverse proxy support (#4655)
- **變更檔案數**: 1

#### 📄 檔案: `context.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:242, E:257, A:0) ➔ After(N:243, E:258, A:0)
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
  • + [新增節點] `Context.Scheme` (FUNCTION_DEF)
  • + [新增呼叫邊] `Context.Scheme` ──[CALLS]──> `Context.requestHeader`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #14: `c79f5d46`
- **完整 Hash**: `c79f5d466ee780c329663d5b599d40639b33cd93`
- **說明 (Ground Truth)**: refactor: optimize error message concatenation in default_validator (#4685)
- **變更檔案數**: 1

#### 📄 檔案: `binding/default_validator.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:26, E:25, A:0) ➔ After(N:26, E:25, A:0)
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

### 🔹 函式: `SliceValidationError.Error()`
- **變更前簽章 (Before)**: `func SliceValidationError.Error()` (L24~L39)
- **變更後簽章 (After)**: `func SliceValidationError.Error()` (L24~L42)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (err SliceValidationError) Error() string {
	if len(err) == 0 {
		return ""
	}

	var b strings.Builder
	for i := range len(err) {
		if err[i] != nil {
			if b.Len() > 0 {
				b.WriteString("\n")
			}
			b.WriteString("[" + strconv.Itoa(i) + "]: " + err[i].Error())
		}
	}
	return b.String()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (err SliceValidationError) Error() string {
	if len(err) == 0 {
		return ""
	}

	var b strings.Builder
	for i := range len(err) {
		if err[i] != nil {
			if b.Len() > 0 {
				b.WriteString("\n")
			}
			b.WriteString("[")
			b.WriteString(strconv.Itoa(i))
			b.WriteString("]: ")
			b.WriteString(err[i].Error())
		}
	}
	return b.String()
}
```


---

### 🔹 Commit #15: `472d086a`
- **完整 Hash**: `472d086af2acd924cb4b9d7be0525f7d790f69bc`
- **說明 (Ground Truth)**: fix(tree): panic in findCaseInsensitivePathRec with RedirectFixedPath (#4535)
- **變更檔案數**: 1

#### 📄 檔案: `tree.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:50, E:53, A:0) ➔ After(N:52, E:53, A:0)
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
  • + [新增節點] `off` (MODULE_STATE)
  • + [新增節點] `rv` (MODULE_STATE)

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `node.findCaseInsensitivePathRec()`
- **變更前簽章 (Before)**: `func node.findCaseInsensitivePathRec(path string, ciPath []byte, rb [4]byte, fixTrailingSlash bool)` (L703~L885)
- **變更後簽章 (After)**: `func node.findCaseInsensitivePathRec(path string, ciPath []byte, rb [4]byte, fixTrailingSlash bool)` (L703~L950)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (n *node) findCaseInsensitivePathRec(path string, ciPath []byte, rb [4]byte, fixTrailingSlash bool) []byte {
	npLen := len(n.path)

walk: // Outer loop for walking the tree
	for len(path) >= npLen && (npLen == 0 || strings.EqualFold(path[1:npLen], n.path[1:])) {
		// Add common prefix to result
		oldPath := path
		path = path[npLen:]
		ciPath = append(ciPath, n.path...)

		if len(path) == 0 {
			// We should have reached the node containing the handle.
			// Check if this node has a handle registered.
			if n.handlers != nil {
				return ciPath
			}

			// No handle found.
			// Try to fix the path by adding a trailing slash
			if fixTrailingSlash {
				for i, c := range []byte(n.indices) {
					if c == '/' {
						n = n.children[i]
						if (len(n.path) == 1 && n.handlers != nil) ||
							(n.nType == catchAll && n.children[0].handlers != nil) {
							return append(ciPath, '/')
						}
						return nil
					}
				}
			}
			return nil
		}

		// If this node does not have a wildcard (param or catchAll) child,
		// we can just look up the next child node and continue to walk down
		// the tree
		if !n.wildChild {
			// Skip rune bytes already processed
			rb = shiftNRuneBytes(rb, npLen)

			if rb[0] != 0 {
				// Old rune not finished
				idxc := rb[0]
				for i, c := range []byte(n.indices) {
					if c == idxc {
						// continue with child node
						n = n.children[i]
						npLen = len(n.path)
						continue walk
					}
				}
			} else {
				// Process a new rune
				var rv rune

				// Find rune start.
				// Runes are up to 4 byte long,
				// -4 would definitely be another rune.
				var off int
				for max_ := min(npLen, 3); off < max_; off++ {
					if i := npLen - off; utf8.RuneStart(oldPath[i]) {
						// read rune from cached path
						rv, _ = utf8.DecodeRuneInString(oldPath[i:])
						break
					}
				}

				// Calculate lowercase bytes of current rune
				lo := unicode.ToLower(rv)
				utf8.EncodeRune(rb[:], lo)

				// Skip already processed bytes
				rb = shiftNRuneBytes(rb, off)

				idxc := rb[0]
				for i, c := range []byte(n.indices) {
					// Lowercase matches
					if c == idxc {
						// must use a recursive approach since both the
						// uppercase byte and the lowercase byte might exist
						// as an index
						if out := n.children[i].findCaseInsensitivePathRec(
							path, ciPath, rb, fixTrailingSlash,
						); out != nil {
							return out
						}
						break
					}
				}

				// If we found no match, the same for the uppercase rune,
				// if it differs
				if up := unicode.ToUpper(rv); up != lo {
					utf8.EncodeRune(rb[:], up)
					rb = shiftNRuneBytes(rb, off)

					idxc := rb[0]
					for i, c := range []byte(n.indices) {
						// Uppercase matches
						if c == idxc {
							// Continue with child node
							n = n.children[i]
							npLen = len(n.path)
							continue walk
						}
					}
				}
			}

			// Nothing found. We can recommend to redirect to the same URL
			// without a trailing slash if a leaf exists for that path
			if fixTrailingSlash && path == "/" && n.handlers != nil {
				return ciPath
			}
			return nil
		}

		n = n.children[0]
		switch n.nType {
		case param:
			// Find param end (either '/' or path end)
			end := 0
			for end < len(path) && path[end] != '/' {
				end++
			}

			// Add param value to case insensitive path
			ciPath = append(ciPath, path[:end]...)

			// We need to go deeper!
			if end < len(path) {
				if len(n.children) > 0 {
					// Continue with child node
					n = n.children[0]
					npLen = len(n.path)
					path = path[end:]
					continue
				}

				// ... but we can't
				if fixTrailingSlash && len(path) == end+1 {
					return ciPath
				}
				return nil
			}

			if n.handlers != nil {
				return ciPath
			}

			if fixTrailingSlash && len(n.children) == 1 {
				// No handle found. Check if a handle for this path + a
				// trailing slash exists
				n = n.children[0]
				if n.path == "/" && n.handlers != nil {
					return append(ciPath, '/')
				}
			}

			return nil

		case catchAll:
			return append(ciPath, path...)

		default:
			panic("invalid node type")
		}
	}

	// Nothing found.
	// Try to fix the path by adding / removing a trailing slash
	if fixTrailingSlash {
		if path == "/" {
			return ciPath
		}
		if len(path)+1 == npLen && n.path[len(path)] == '/' &&
			strings.EqualFold(path[1:], n.path[1:len(path)]) && n.handlers != nil {
			return append(ciPath, n.path...)
		}
	}
	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (n *node) findCaseInsensitivePathRec(path string, ciPath []byte, rb [4]byte, fixTrailingSlash bool) []byte {
	npLen := len(n.path)

walk: // Outer loop for walking the tree
	for len(path) >= npLen && (npLen == 0 || strings.EqualFold(path[1:npLen], n.path[1:])) {
		// Add common prefix to result
		oldPath := path
		path = path[npLen:]
		ciPath = append(ciPath, n.path...)

		if len(path) == 0 {
			// We should have reached the node containing the handle.
			// Check if this node has a handle registered.
			if n.handlers != nil {
				return ciPath
			}

			// No handle found.
			// Try to fix the path by adding a trailing slash
			if fixTrailingSlash {
				for i, c := range []byte(n.indices) {
					if c == '/' {
						n = n.children[i]
						if (len(n.path) == 1 && n.handlers != nil) ||
							(n.nType == catchAll && n.children[0].handlers != nil) {
							return append(ciPath, '/')
						}
						return nil
					}
				}
			}
			return nil
		}

		// If this node does not have a wildcard (param or catchAll) child,
		// we can just look up the next child node and continue to walk down
		// the tree
		if !n.wildChild {
			// Skip rune bytes already processed
			rb = shiftNRuneBytes(rb, npLen)

			if rb[0] != 0 {
				// Old rune not finished
				idxc := rb[0]
				for i, c := range []byte(n.indices) {
					if c == idxc {
						// continue with child node
						n = n.children[i]
						npLen = len(n.path)
						continue walk
					}
				}
			} else {
				// Process a new rune
				var rv rune

				// Find rune start.
				// Runes are up to 4 byte long,
				// -4 would definitely be another rune.
				var off int
				for max_ := min(npLen, 3); off < max_; off++ {
					if i := npLen - off; utf8.RuneStart(oldPath[i]) {
						// read rune from cached path
						rv, _ = utf8.DecodeRuneInString(oldPath[i:])
						break
					}
				}

				// Calculate lowercase bytes of current rune
				lo := unicode.ToLower(rv)
				utf8.EncodeRune(rb[:], lo)

				// Skip already processed bytes
				rb = shiftNRuneBytes(rb, off)

				idxc := rb[0]
				for i, c := range []byte(n.indices) {
					// Lowercase matches
					if c == idxc {
						// must use a recursive approach since both the
						// uppercase byte and the lowercase byte might exist
						// as an index
						if out := n.children[i].findCaseInsensitivePathRec(
							path, ciPath, rb, fixTrailingSlash,
						); out != nil {
							return out
						}
						break
					}
				}

				// If we found no match, the same for the uppercase rune,
				// if it differs
				if up := unicode.ToUpper(rv); up != lo {
					utf8.EncodeRune(rb[:], up)
					rb = shiftNRuneBytes(rb, off)

					idxc := rb[0]
					for i, c := range []byte(n.indices) {
						// Uppercase matches
						if c == idxc {
							// Continue with child node
							n = n.children[i]
							npLen = len(n.path)
							continue walk
						}
					}
				}
			}

			// Nothing found. We can recommend to redirect to the same URL
			// without a trailing slash if a leaf exists for that path
			if fixTrailingSlash && path == "/" && n.handlers != nil {
				return ciPath
			}
			return nil
		}

		// When wildChild is true, try static children first (via indices)
		// before falling back to the wildcard child. This ensures that
		// case-insensitive lookups prefer static routes over param routes
		// (e.g., /PREFIX/XXX should resolve to /prefix/xxx, not match :id).
		if len(n.indices) > 0 {
			rb = shiftNRuneBytes(rb, npLen)

			if rb[0] != 0 {
				idxc := rb[0]
				for i, c := range []byte(n.indices) {
					if c == idxc {
						if out := n.children[i].findCaseInsensitivePathRec(
							path, ciPath, rb, fixTrailingSlash,
						); out != nil {
							return out
						}
						break
					}
				}
			} else {
				var rv rune
				var off int
				for max_ := min(npLen, 3); off < max_; off++ {
					if i := npLen - off; utf8.RuneStart(oldPath[i]) {
						rv, _ = utf8.DecodeRuneInString(oldPath[i:])
						break
					}
				}

				lo := unicode.ToLower(rv)
				utf8.EncodeRune(rb[:], lo)
				rb = shiftNRuneBytes(rb, off)

				idxc := rb[0]
				for i, c := range []byte(n.indices) {
					if c == idxc {
						if out := n.children[i].findCaseInsensitivePathRec(
							path, ciPath, rb, fixTrailingSlash,
						); out != nil {
							return out
						}
						break
					}
				}

				if up := unicode.ToUpper(rv); up != lo {
					utf8.EncodeRune(rb[:], up)
					rb = shiftNRuneBytes(rb, off)

					idxc := rb[0]
					for i, c := range []byte(n.indices) {
						if c == idxc {
							if out := n.children[i].findCaseInsensitivePathRec(
								path, ciPath, rb, fixTrailingSlash,
							); out != nil {
								return out
							}
							break
						}
					}
				}
			}
		}

		// Fall back to wildcard child, which is always at the end of the array
		n = n.children[len(n.children)-1]
		switch n.nType {
		case param:
			// Find param end (either '/' or path end)
			end := 0
			for end < len(path) && path[end] != '/' {
				end++
			}

			// Add param value to case insensitive path
			ciPath = append(ciPath, path[:end]...)

			// We need to go deeper!
			if end < len(path) {
				if len(n.children) > 0 {
					// Continue with child node
					n = n.children[0]
					npLen = len(n.path)
					path = path[end:]
					continue
				}

				// ... but we can't
				if fixTrailingSlash && len(path) == end+1 {
					return ciPath
				}
				return nil
			}

			if n.handlers != nil {
				return ciPath
			}

			if fixTrailingSlash && len(n.children) == 1 {
				// No handle found. Check if a handle for this path + a
				// trailing slash exists
				n = n.children[0]
				if n.path == "/" && n.handlers != nil {
					return append(ciPath, '/')
				}
			}

			return nil

		case catchAll:
			return append(ciPath, path...)

		default:
			panic("invalid node type")
		}
	}

	// Nothing found.
	// Try to fix the path by adding / removing a trailing slash
	if fixTrailingSlash {
		if path == "/" {
			return ciPath
		}
		if len(path)+1 == npLen && n.path[len(path)] == '/' &&
			strings.EqualFold(path[1:], n.path[1:len(path)]) && n.handlers != nil {
			return append(ciPath, n.path...)
		}
	}
	return nil
}
```


---

### 🔹 Commit #16: `fb258344`
- **完整 Hash**: `fb2583442c4d9bccb75e6d26f1aa6e7c01950db6`
- **說明 (Ground Truth)**: test(context): use http.StatusContinue constant instead of magic number 100 (#4542)
- **變更檔案數**: 1

#### 📄 檔案: `context.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:241, E:256, A:0) ➔ After(N:241, E:256, A:0)
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

---

### 🔹 Commit #17: `5c00df8a`
- **完整 Hash**: `5c00df8afadd06cc5be530dde00fe6d9fa4a2e4a`
- **說明 (Ground Truth)**: fix(render): write content length in Data.Render (#4206)
- **變更檔案數**: 1

#### 📄 檔案: `render/data.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:4, E:3, A:0) ➔ After(N:8, E:7, A:0)
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
  • + [新增節點] `len (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `w.Header().Set (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `w.Header (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `strconv.Itoa (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Data.Render` ──[CALLS]──> `len (External/Pkg)`
  • + [新增呼叫邊] `Data.Render` ──[CALLS]──> `w.Header().Set (External/Pkg)`
  • + [新增呼叫邊] `Data.Render` ──[CALLS]──> `w.Header (External/Pkg)`
  • + [新增呼叫邊] `Data.Render` ──[CALLS]──> `strconv.Itoa (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Data.Render()`
- **變更前簽章 (Before)**: `func Data.Render(w http.ResponseWriter)` (L16~L20)
- **變更後簽章 (After)**: `func Data.Render(w http.ResponseWriter)` (L19~L26)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (r Data) Render(w http.ResponseWriter) (err error) {
	r.WriteContentType(w)
	_, err = w.Write(r.Data)
	return
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (r Data) Render(w http.ResponseWriter) (err error) {
	r.WriteContentType(w)
	if len(r.Data) > 0 {
		w.Header().Set("Content-Length", strconv.Itoa(len(r.Data)))
	}
	_, err = w.Write(r.Data)
	return
}
```


---

### 🔹 Commit #18: `db309081`
- **完整 Hash**: `db309081bc5c137b2aa15701ef53f7f19788da25`
- **說明 (Ground Truth)**: chore(logger): allow skipping query string output (#4547)
- **變更檔案數**: 1

#### 📄 檔案: `logger.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:35, E:25, A:0) ➔ After(N:35, E:25, A:0)
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

### 🔹 函式: `LoggerWithConfig()`
- **變更前簽章 (Before)**: `func LoggerWithConfig(conf LoggerConfig)` (L240~L309)
- **變更後簽章 (After)**: `func LoggerWithConfig(conf LoggerConfig)` (L245~L314)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func LoggerWithConfig(conf LoggerConfig) HandlerFunc {
	formatter := conf.Formatter
	if formatter == nil {
		formatter = defaultLogFormatter
	}

	out := conf.Output
	if out == nil {
		out = DefaultWriter
	}

	notlogged := conf.SkipPaths

	isTerm := true

	if w, ok := out.(*os.File); !ok || os.Getenv("TERM") == "dumb" ||
		(!isatty.IsTerminal(w.Fd()) && !isatty.IsCygwinTerminal(w.Fd())) {
		isTerm = false
	}

	var skip map[string]struct{}

	if length := len(notlogged); length > 0 {
		skip = make(map[string]struct{}, length)

		for _, path := range notlogged {
			skip[path] = struct{}{}
		}
	}

	return func(c *Context) {
		// Start timer
		start := time.Now()
		path := c.Request.URL.Path
		raw := c.Request.URL.RawQuery

		// Process request
		c.Next()

		// Log only when it is not being skipped
		if _, ok := skip[path]; ok || (conf.Skip != nil && conf.Skip(c)) {
			return
		}

		param := LogFormatterParams{
			Request: c.Request,
			isTerm:  isTerm,
			Keys:    c.Keys,
		}

		// Stop timer
		param.TimeStamp = time.Now()
		param.Latency = param.TimeStamp.Sub(start)

		param.ClientIP = c.ClientIP()
		param.Method = c.Request.Method
		param.StatusCode = c.Writer.Status()
		param.ErrorMessage = c.Errors.ByType(ErrorTypePrivate).String()

		param.BodySize = c.Writer.Size()

		if raw != "" {
			path = path + "?" + raw
		}

		param.Path = path

		fmt.Fprint(out, formatter(param))
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func LoggerWithConfig(conf LoggerConfig) HandlerFunc {
	formatter := conf.Formatter
	if formatter == nil {
		formatter = defaultLogFormatter
	}

	out := conf.Output
	if out == nil {
		out = DefaultWriter
	}

	notlogged := conf.SkipPaths

	isTerm := true

	if w, ok := out.(*os.File); !ok || os.Getenv("TERM") == "dumb" ||
		(!isatty.IsTerminal(w.Fd()) && !isatty.IsCygwinTerminal(w.Fd())) {
		isTerm = false
	}

	var skip map[string]struct{}

	if length := len(notlogged); length > 0 {
		skip = make(map[string]struct{}, length)

		for _, path := range notlogged {
			skip[path] = struct{}{}
		}
	}

	return func(c *Context) {
		// Start timer
		start := time.Now()
		path := c.Request.URL.Path
		raw := c.Request.URL.RawQuery

		// Process request
		c.Next()

		// Log only when it is not being skipped
		if _, ok := skip[path]; ok || (conf.Skip != nil && conf.Skip(c)) {
			return
		}

		param := LogFormatterParams{
			Request: c.Request,
			isTerm:  isTerm,
			Keys:    c.Keys,
		}

		// Stop timer
		param.TimeStamp = time.Now()
		param.Latency = param.TimeStamp.Sub(start)

		param.ClientIP = c.ClientIP()
		param.Method = c.Request.Method
		param.StatusCode = c.Writer.Status()
		param.ErrorMessage = c.Errors.ByType(ErrorTypePrivate).String()

		param.BodySize = c.Writer.Size()

		if raw != "" && !conf.SkipQueryString {
			path = path + "?" + raw
		}

		param.Path = path

		fmt.Fprint(out, formatter(param))
	}
}
```


---

### 🔹 Commit #19: `cad29c5e`
- **完整 Hash**: `cad29c5e3f50a9764edbfc4787825c6caabd8579`
- **說明 (Ground Truth)**: perf(tree): reduce allocations in findCaseInsensitivePath (#4417)
- **變更檔案數**: 1

#### 📄 檔案: `tree.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:49, E:52, A:0) ➔ After(N:50, E:53, A:0)
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
  • + [新增節點] `max (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `node.findCaseInsensitivePath` ──[CALLS]──> `max (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `node.findCaseInsensitivePath()`
- **變更前簽章 (Before)**: `func node.findCaseInsensitivePath(path string, fixTrailingSlash bool)` (L671~L689)
- **變更後簽章 (After)**: `func node.findCaseInsensitivePath(path string, fixTrailingSlash bool)` (L671~L684)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (n *node) findCaseInsensitivePath(path string, fixTrailingSlash bool) ([]byte, bool) {
	const stackBufSize = 128

	// Use a static sized buffer on the stack in the common case.
	// If the path is too long, allocate a buffer on the heap instead.
	buf := make([]byte, 0, stackBufSize)
	if length := len(path) + 1; length > stackBufSize {
		buf = make([]byte, 0, length)
	}

	ciPath := n.findCaseInsensitivePathRec(
		path,
		buf,       // Preallocate enough memory for new path
		[4]byte{}, // Empty rune buffer
		fixTrailingSlash,
	)

	return ciPath, ciPath != nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (n *node) findCaseInsensitivePath(path string, fixTrailingSlash bool) ([]byte, bool) {
	const stackBufSize = 128

	buf := make([]byte, 0, max(stackBufSize, len(path)+1))

	ciPath := n.findCaseInsensitivePathRec(
		path,
		buf,       // Preallocate enough memory for new path
		[4]byte{}, // Empty rune buffer
		fixTrailingSlash,
	)

	return ciPath, ciPath != nil
}
```


---

### 🔹 Commit #20: `53410d2e`
- **完整 Hash**: `53410d2e07054369e0960fbe2eed97e1b9966f12`
- **說明 (Ground Truth)**: feat(context): add GetError and GetErrorSlice methods for error retrieval (#4502)
- **變更檔案數**: 1

#### 📄 檔案: `context.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:237, E:252, A:0) ➔ After(N:240, E:254, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `getTyped[error] (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `Context.GetErrorSlice` (FUNCTION_DEF)
  • + [新增節點] `Context.GetError` (FUNCTION_DEF)
  • + [新增呼叫邊] `Context.GetError` ──[CALLS]──> `getTyped[error] (External/Pkg)`
  • + [新增呼叫邊] `Context.GetErrorSlice` ──[CALLS]──> `getTyped`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/gin show ea9fab99e01d55a5e4f8daacc0d11ccffaee0a15
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff ea9fab99e01d55a5e4f8daacc0d11ccffaee0a15~1 --file test_repos/gin/tree.go
   ```
