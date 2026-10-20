# 🔬 CODE-Map 基準審查獨立驗證報告: `zustand`
> **技術生態**: `TypeScript (全域狀態 / 閉包不可變性)`  
> **本地倉庫路徑**: `test_repos/zustand`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 24 Files  
> **報告生成時間**: 2026-10-20 21:42:44  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `6` / `24` | `25.0%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `13` / `24` | `54.2%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `5` / `24` | `20.8%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`19` / `24`** | **`79.2%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `24` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `3febf8c6`
- **完整 Hash**: `3febf8c6d4f6670f886cc6b628b01a128d2888bd`
- **說明 (Ground Truth)**: fix(persist): clearStorage() should invalidate concurrent async rehydration (#3555)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/persist.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:34, E:21, A:0) ➔ After(N:34, E:21, A:0)
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
  - 💥 作用域阻隔: 函式 'setItem' 被深鎖在內部閉包 (scope:createJSONStorage@after/src/middleware/persist.ts:L31C8)，外部無法調用！
  - 💥 作用域阻隔: 函式 'hydrate' 被深鎖在內部閉包 (scope:arrow@after/src/middleware/persist.ts:L187C59)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `clearStorage()`
- **變更前簽章 (Before)**: `clearStorage()` (L348~L350)
- **變更後簽章 (After)**: `clearStorage()` (L348~L351)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
      storage?.removeItem(options.name)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
      ++hydrationVersion
      storage?.removeItem(options.name)
    }
```

### 🔹 函式: `persistImpl()`
- **變更前簽章 (Before)**: `persistImpl(config, baseOptions)` (L187~L375)
- **變更後簽章 (After)**: `persistImpl(config, baseOptions)` (L187~L376)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(config, baseOptions) => (set, get, api) => {
  type S = ReturnType<typeof config>
  let options = {
    storage: createJSONStorage<S, void>(() => window.localStorage),
    partialize: (state: S) => state,
    version: 0,
    merge: (persistedState: unknown, currentState: S) => ({
      ...currentState,
      ...(persistedState as object),
    }),
    ...baseOptions,
  }

  let hasHydrated = false
  // Counter to track hydration versions and prevent race conditions
  // when multiple rehydrate() calls happen concurrently
  let hydrationVersion = 0
  const hydrationListeners = new Set<PersistListener<S>>()
  const finishHydrationListeners = new Set<PersistListener<S>>()
  let storage = options.storage

  if (!storage) {
    return config(
      (...args) => {
        console.warn(
          `[zustand persist middleware] Unable to update item '${options.name}', the given storage is currently unavailable.`,
        )
        set(...(args as Parameters<typeof set>))
      },
      get,
      api,
    )
  }

  const setItem = () => {
    const state = options.partialize({ ...get() })
    return (storage as PersistStorage<S, unknown>).setItem(options.name, {
      state,
      version: options.version,
    })
  }

  const savedSetState = api.setState

  api.setState = (state, replace) => {
    savedSetState(state, replace as any)
    return setItem()
  }

  const configResult = config(
    (...args) => {
      set(...(args as Parameters<typeof set>))
      return setItem()
    },
    get,
    api,
  )

  api.getInitialState = () => configResult

  // a workaround to solve the issue of not storing rehydrated state in sync storage
  // the set(state) value would be later overridden with initial state by create()
  // to avoid this, we merge the state from localStorage into the initial state.
  let stateFromStorage: S | undefined

  // rehydrate initial state with existing stored state
  const hydrate = () => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    // Increment version to invalidate any in-flight hydration
    const currentVersion = ++hydrationVersion
    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(get(), undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(undefined, e)
      })
  }

  ;(api as StoreApi<S> & StorePersist<StoreApi<S>, S, unknown>).persist = {
    setOptions: (newOptions) => {
      options = {
        ...options,
        ...newOptions,
      }

      if (newOptions.storage) {
        storage = newOptions.storage
      }
    },
    clearStorage: () => {
      storage?.removeItem(options.name)
    },
    getOptions: () => options,
    rehydrate: () => hydrate() as Promise<void>,
    hasHydrated: () => hasHydrated,
    onHydrate: (cb) => {
      hydrationListeners.add(cb)

      return () => {
        hydrationListeners.delete(cb)
      }
    },
    onFinishHydration: (cb) => {
      finishHydrationListeners.add(cb)

      return () => {
        finishHydrationListeners.delete(cb)
      }
    },
  }

  if (!options.skipHydration) {
    hydrate()
  }

  return stateFromStorage || configResult
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(config, baseOptions) => (set, get, api) => {
  type S = ReturnType<typeof config>
  let options = {
    storage: createJSONStorage<S, void>(() => window.localStorage),
    partialize: (state: S) => state,
    version: 0,
    merge: (persistedState: unknown, currentState: S) => ({
      ...currentState,
      ...(persistedState as object),
    }),
    ...baseOptions,
  }

  let hasHydrated = false
  // Counter to track hydration versions and prevent race conditions
  // when multiple rehydrate() calls happen concurrently
  let hydrationVersion = 0
  const hydrationListeners = new Set<PersistListener<S>>()
  const finishHydrationListeners = new Set<PersistListener<S>>()
  let storage = options.storage

  if (!storage) {
    return config(
      (...args) => {
        console.warn(
          `[zustand persist middleware] Unable to update item '${options.name}', the given storage is currently unavailable.`,
        )
        set(...(args as Parameters<typeof set>))
      },
      get,
      api,
    )
  }

  const setItem = () => {
    const state = options.partialize({ ...get() })
    return (storage as PersistStorage<S, unknown>).setItem(options.name, {
      state,
      version: options.version,
    })
  }

  const savedSetState = api.setState

  api.setState = (state, replace) => {
    savedSetState(state, replace as any)
    return setItem()
  }

  const configResult = config(
    (...args) => {
      set(...(args as Parameters<typeof set>))
      return setItem()
    },
    get,
    api,
  )

  api.getInitialState = () => configResult

  // a workaround to solve the issue of not storing rehydrated state in sync storage
  // the set(state) value would be later overridden with initial state by create()
  // to avoid this, we merge the state from localStorage into the initial state.
  let stateFromStorage: S | undefined

  // rehydrate initial state with existing stored state
  const hydrate = () => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    // Increment version to invalidate any in-flight hydration
    const currentVersion = ++hydrationVersion
    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(get(), undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(undefined, e)
      })
  }

  ;(api as StoreApi<S> & StorePersist<StoreApi<S>, S, unknown>).persist = {
    setOptions: (newOptions) => {
      options = {
        ...options,
        ...newOptions,
      }

      if (newOptions.storage) {
        storage = newOptions.storage
      }
    },
    clearStorage: () => {
      ++hydrationVersion
      storage?.removeItem(options.name)
    },
    getOptions: () => options,
    rehydrate: () => hydrate() as Promise<void>,
    hasHydrated: () => hasHydrated,
    onHydrate: (cb) => {
      hydrationListeners.add(cb)

      return () => {
        hydrationListeners.delete(cb)
      }
    },
    onFinishHydration: (cb) => {
      finishHydrationListeners.add(cb)

      return () => {
        finishHydrationListeners.delete(cb)
      }
    },
  }

  if (!options.skipHydration) {
    hydrate()
  }

  return stateFromStorage || configResult
}
```


---

### 🔹 Commit #02: `f44cecc7`
- **完整 Hash**: `f44cecc72a8ec39fbd270fc29e2058806932bf2a`
- **說明 (Ground Truth)**: fix(devtools): correct V8 stack regex when source path contains spaces (#3531)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/devtools.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:19, E:13, A:0) ➔ After(N:19, E:13, A:0)
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

### 🔹 函式: `v8StackLineRe()`
- **變更前簽章 (Before)**: `[Module State] v8StackLineRe` (L170~L170)
- **變更後簽章 (After)**: `[Module State] v8StackLineRe` (L170~L170)

#### ◀️ 變更前實作碼 (Before Implementation):
```
v8StackLineRe = /.+ (.+) .+/
```

#### ▶️ 變更後實作碼 (After Implementation):
```
v8StackLineRe = /^at (?:new |async )?(.+?) \(/
```


---

### 🔹 Commit #03: `ad77bd3b`
- **完整 Hash**: `ad77bd3bb6f7bbd12fea8b458ed5c0673df0793a`
- **說明 (Ground Truth)**: fix(devtools): improve type inference for Devtools initializer (#3511)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/devtools.ts`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:19, E:13, A:0) ➔ After(N:19, E:13, A:0)
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

### 🔹 Commit #04: `4e9bcf0c`
- **完整 Hash**: `4e9bcf0c82938cfe2463495a845806cd5ec3e59b`
- **說明 (Ground Truth)**: fix(devtools): support Firefox/Safari stack format in findCallerName (#3469)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/devtools.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:17, E:13, A:0) ➔ After(N:19, E:13, A:0)
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
  • + [新增節點] `v8StackLineRe` (MODULE_STATE)
  • + [新增節點] `geckoStackLineRe` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `findCallerName()`
- **變更前簽章 (Before)**: `findCallerName(stack: string | undefined)` (L169~L178)
- **變更後簽章 (After)**: `function findCallerName(stack: string | undefined)` (L174~L186)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(stack: string | undefined) => {
  if (!stack) return undefined
  const traceLines = stack.split('\n')
  const apiSetStateLineIndex = traceLines.findIndex((traceLine) =>
    traceLine.includes('api.setState'),
  )
  if (apiSetStateLineIndex < 0) return undefined
  const callerLine = traceLines[apiSetStateLineIndex + 1]?.trim() || ''
  return /.+ (.+) .+/.exec(callerLine)?.[1]
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function findCallerName(stack: string | undefined) {
  if (!stack) return undefined
  const traceLines = stack.split('\n')
  const apiSetStateLineIndex = traceLines.findIndex((traceLine) =>
    traceLine.includes('api.setState'),
  )
  if (apiSetStateLineIndex < 0) return undefined
  const callerLine = traceLines[apiSetStateLineIndex + 1]?.trim() || ''
  return (
    v8StackLineRe.exec(callerLine)?.[1] ||
    geckoStackLineRe.exec(callerLine)?.[1]
  )
}
```


---

### 🔹 Commit #05: `89ebcd73`
- **完整 Hash**: `89ebcd73134ed32689ae767a5ce5ad8f24bd5ee1`
- **說明 (Ground Truth)**: fix(devtools): correct redux devtools config type extension (#3414)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/devtools.ts`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:17, E:13, A:0) ➔ After(N:17, E:13, A:0)
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

### 🔹 Commit #06: `6213fc11`
- **完整 Hash**: `6213fc11bdf096301a82ae5c236b5a666a4ee3ca`
- **說明 (Ground Truth)**: fix(persist): use latest state in post-rehydration callback (#3391)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/persist.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:34, E:21, A:0) ➔ After(N:34, E:21, A:0)
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
  - 💥 作用域阻隔: 函式 'setItem' 被深鎖在內部閉包 (scope:createJSONStorage@after/src/middleware/persist.ts:L31C8)，外部無法調用！
  - 💥 作用域阻隔: 函式 'hydrate' 被深鎖在內部閉包 (scope:arrow@after/src/middleware/persist.ts:L187C59)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `hydrate()`
- **變更前簽章 (Before)**: `hydrate()` (L253~L340)
- **變更後簽章 (After)**: `hydrate()` (L253~L335)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    // Increment version to invalidate any in-flight hydration
    const currentVersion = ++hydrationVersion
    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(undefined, e)
      })
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    // Increment version to invalidate any in-flight hydration
    const currentVersion = ++hydrationVersion
    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(get(), undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(undefined, e)
      })
  }
```

### 🔹 函式: `persistImpl()`
- **變更前簽章 (Before)**: `persistImpl(config, baseOptions)` (L187~L380)
- **變更後簽章 (After)**: `persistImpl(config, baseOptions)` (L187~L375)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(config, baseOptions) => (set, get, api) => {
  type S = ReturnType<typeof config>
  let options = {
    storage: createJSONStorage<S, void>(() => window.localStorage),
    partialize: (state: S) => state,
    version: 0,
    merge: (persistedState: unknown, currentState: S) => ({
      ...currentState,
      ...(persistedState as object),
    }),
    ...baseOptions,
  }

  let hasHydrated = false
  // Counter to track hydration versions and prevent race conditions
  // when multiple rehydrate() calls happen concurrently
  let hydrationVersion = 0
  const hydrationListeners = new Set<PersistListener<S>>()
  const finishHydrationListeners = new Set<PersistListener<S>>()
  let storage = options.storage

  if (!storage) {
    return config(
      (...args) => {
        console.warn(
          `[zustand persist middleware] Unable to update item '${options.name}', the given storage is currently unavailable.`,
        )
        set(...(args as Parameters<typeof set>))
      },
      get,
      api,
    )
  }

  const setItem = () => {
    const state = options.partialize({ ...get() })
    return (storage as PersistStorage<S, unknown>).setItem(options.name, {
      state,
      version: options.version,
    })
  }

  const savedSetState = api.setState

  api.setState = (state, replace) => {
    savedSetState(state, replace as any)
    return setItem()
  }

  const configResult = config(
    (...args) => {
      set(...(args as Parameters<typeof set>))
      return setItem()
    },
    get,
    api,
  )

  api.getInitialState = () => configResult

  // a workaround to solve the issue of not storing rehydrated state in sync storage
  // the set(state) value would be later overridden with initial state by create()
  // to avoid this, we merge the state from localStorage into the initial state.
  let stateFromStorage: S | undefined

  // rehydrate initial state with existing stored state
  const hydrate = () => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    // Increment version to invalidate any in-flight hydration
    const currentVersion = ++hydrationVersion
    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(undefined, e)
      })
  }

  ;(api as StoreApi<S> & StorePersist<StoreApi<S>, S, unknown>).persist = {
    setOptions: (newOptions) => {
      options = {
        ...options,
        ...newOptions,
      }

      if (newOptions.storage) {
        storage = newOptions.storage
      }
    },
    clearStorage: () => {
      storage?.removeItem(options.name)
    },
    getOptions: () => options,
    rehydrate: () => hydrate() as Promise<void>,
    hasHydrated: () => hasHydrated,
    onHydrate: (cb) => {
      hydrationListeners.add(cb)

      return () => {
        hydrationListeners.delete(cb)
      }
    },
    onFinishHydration: (cb) => {
      finishHydrationListeners.add(cb)

      return () => {
        finishHydrationListeners.delete(cb)
      }
    },
  }

  if (!options.skipHydration) {
    hydrate()
  }

  return stateFromStorage || configResult
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(config, baseOptions) => (set, get, api) => {
  type S = ReturnType<typeof config>
  let options = {
    storage: createJSONStorage<S, void>(() => window.localStorage),
    partialize: (state: S) => state,
    version: 0,
    merge: (persistedState: unknown, currentState: S) => ({
      ...currentState,
      ...(persistedState as object),
    }),
    ...baseOptions,
  }

  let hasHydrated = false
  // Counter to track hydration versions and prevent race conditions
  // when multiple rehydrate() calls happen concurrently
  let hydrationVersion = 0
  const hydrationListeners = new Set<PersistListener<S>>()
  const finishHydrationListeners = new Set<PersistListener<S>>()
  let storage = options.storage

  if (!storage) {
    return config(
      (...args) => {
        console.warn(
          `[zustand persist middleware] Unable to update item '${options.name}', the given storage is currently unavailable.`,
        )
        set(...(args as Parameters<typeof set>))
      },
      get,
      api,
    )
  }

  const setItem = () => {
    const state = options.partialize({ ...get() })
    return (storage as PersistStorage<S, unknown>).setItem(options.name, {
      state,
      version: options.version,
    })
  }

  const savedSetState = api.setState

  api.setState = (state, replace) => {
    savedSetState(state, replace as any)
    return setItem()
  }

  const configResult = config(
    (...args) => {
      set(...(args as Parameters<typeof set>))
      return setItem()
    },
    get,
    api,
  )

  api.getInitialState = () => configResult

  // a workaround to solve the issue of not storing rehydrated state in sync storage
  // the set(state) value would be later overridden with initial state by create()
  // to avoid this, we merge the state from localStorage into the initial state.
  let stateFromStorage: S | undefined

  // rehydrate initial state with existing stored state
  const hydrate = () => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    // Increment version to invalidate any in-flight hydration
    const currentVersion = ++hydrationVersion
    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(get(), undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(undefined, e)
      })
  }

  ;(api as StoreApi<S> & StorePersist<StoreApi<S>, S, unknown>).persist = {
    setOptions: (newOptions) => {
      options = {
        ...options,
        ...newOptions,
      }

      if (newOptions.storage) {
        storage = newOptions.storage
      }
    },
    clearStorage: () => {
      storage?.removeItem(options.name)
    },
    getOptions: () => options,
    rehydrate: () => hydrate() as Promise<void>,
    hasHydrated: () => hasHydrated,
    onHydrate: (cb) => {
      hydrationListeners.add(cb)

      return () => {
        hydrationListeners.delete(cb)
      }
    },
    onFinishHydration: (cb) => {
      finishHydrationListeners.add(cb)

      return () => {
        finishHydrationListeners.delete(cb)
      }
    },
  }

  if (!options.skipHydration) {
    hydrate()
  }

  return stateFromStorage || configResult
}
```


---

### 🔹 Commit #07: `3871d539`
- **完整 Hash**: `3871d5392400db9ca3cabf8c52fbef2b259a5a83`
- **說明 (Ground Truth)**: fix(immer): Proper typing for immer middleware in combination with slices  (#3371)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/immer.ts`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:6, E:3, A:0) ➔ After(N:6, E:3, A:0)
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

### 🔹 Commit #08: `9b505ac3`
- **完整 Hash**: `9b505ac392b8a9a68db07ec1b9063c3f3bc6cd1f`
- **說明 (Ground Truth)**: fix(persist): use window.localStorage as default storage reference (#3367)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/persist.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:34, E:21, A:0) ➔ After(N:34, E:21, A:0)
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
  - 💥 作用域阻隔: 函式 'setItem' 被深鎖在內部閉包 (scope:createJSONStorage@after/src/middleware/persist.ts:L31C8)，外部無法調用！
  - 💥 作用域阻隔: 函式 'hydrate' 被深鎖在內部閉包 (scope:arrow@after/src/middleware/persist.ts:L187C59)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `persistImpl()`
- **變更前簽章 (Before)**: `persistImpl(config, baseOptions)` (L187~L380)
- **變更後簽章 (After)**: `persistImpl(config, baseOptions)` (L187~L380)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(config, baseOptions) => (set, get, api) => {
  type S = ReturnType<typeof config>
  let options = {
    storage: createJSONStorage<S, void>(() => localStorage),
    partialize: (state: S) => state,
    version: 0,
    merge: (persistedState: unknown, currentState: S) => ({
      ...currentState,
      ...(persistedState as object),
    }),
    ...baseOptions,
  }

  let hasHydrated = false
  // Counter to track hydration versions and prevent race conditions
  // when multiple rehydrate() calls happen concurrently
  let hydrationVersion = 0
  const hydrationListeners = new Set<PersistListener<S>>()
  const finishHydrationListeners = new Set<PersistListener<S>>()
  let storage = options.storage

  if (!storage) {
    return config(
      (...args) => {
        console.warn(
          `[zustand persist middleware] Unable to update item '${options.name}', the given storage is currently unavailable.`,
        )
        set(...(args as Parameters<typeof set>))
      },
      get,
      api,
    )
  }

  const setItem = () => {
    const state = options.partialize({ ...get() })
    return (storage as PersistStorage<S, unknown>).setItem(options.name, {
      state,
      version: options.version,
    })
  }

  const savedSetState = api.setState

  api.setState = (state, replace) => {
    savedSetState(state, replace as any)
    return setItem()
  }

  const configResult = config(
    (...args) => {
      set(...(args as Parameters<typeof set>))
      return setItem()
    },
    get,
    api,
  )

  api.getInitialState = () => configResult

  // a workaround to solve the issue of not storing rehydrated state in sync storage
  // the set(state) value would be later overridden with initial state by create()
  // to avoid this, we merge the state from localStorage into the initial state.
  let stateFromStorage: S | undefined

  // rehydrate initial state with existing stored state
  const hydrate = () => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    // Increment version to invalidate any in-flight hydration
    const currentVersion = ++hydrationVersion
    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(undefined, e)
      })
  }

  ;(api as StoreApi<S> & StorePersist<StoreApi<S>, S, unknown>).persist = {
    setOptions: (newOptions) => {
      options = {
        ...options,
        ...newOptions,
      }

      if (newOptions.storage) {
        storage = newOptions.storage
      }
    },
    clearStorage: () => {
      storage?.removeItem(options.name)
    },
    getOptions: () => options,
    rehydrate: () => hydrate() as Promise<void>,
    hasHydrated: () => hasHydrated,
    onHydrate: (cb) => {
      hydrationListeners.add(cb)

      return () => {
        hydrationListeners.delete(cb)
      }
    },
    onFinishHydration: (cb) => {
      finishHydrationListeners.add(cb)

      return () => {
        finishHydrationListeners.delete(cb)
      }
    },
  }

  if (!options.skipHydration) {
    hydrate()
  }

  return stateFromStorage || configResult
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(config, baseOptions) => (set, get, api) => {
  type S = ReturnType<typeof config>
  let options = {
    storage: createJSONStorage<S, void>(() => window.localStorage),
    partialize: (state: S) => state,
    version: 0,
    merge: (persistedState: unknown, currentState: S) => ({
      ...currentState,
      ...(persistedState as object),
    }),
    ...baseOptions,
  }

  let hasHydrated = false
  // Counter to track hydration versions and prevent race conditions
  // when multiple rehydrate() calls happen concurrently
  let hydrationVersion = 0
  const hydrationListeners = new Set<PersistListener<S>>()
  const finishHydrationListeners = new Set<PersistListener<S>>()
  let storage = options.storage

  if (!storage) {
    return config(
      (...args) => {
        console.warn(
          `[zustand persist middleware] Unable to update item '${options.name}', the given storage is currently unavailable.`,
        )
        set(...(args as Parameters<typeof set>))
      },
      get,
      api,
    )
  }

  const setItem = () => {
    const state = options.partialize({ ...get() })
    return (storage as PersistStorage<S, unknown>).setItem(options.name, {
      state,
      version: options.version,
    })
  }

  const savedSetState = api.setState

  api.setState = (state, replace) => {
    savedSetState(state, replace as any)
    return setItem()
  }

  const configResult = config(
    (...args) => {
      set(...(args as Parameters<typeof set>))
      return setItem()
    },
    get,
    api,
  )

  api.getInitialState = () => configResult

  // a workaround to solve the issue of not storing rehydrated state in sync storage
  // the set(state) value would be later overridden with initial state by create()
  // to avoid this, we merge the state from localStorage into the initial state.
  let stateFromStorage: S | undefined

  // rehydrate initial state with existing stored state
  const hydrate = () => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    // Increment version to invalidate any in-flight hydration
    const currentVersion = ++hydrationVersion
    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(undefined, e)
      })
  }

  ;(api as StoreApi<S> & StorePersist<StoreApi<S>, S, unknown>).persist = {
    setOptions: (newOptions) => {
      options = {
        ...options,
        ...newOptions,
      }

      if (newOptions.storage) {
        storage = newOptions.storage
      }
    },
    clearStorage: () => {
      storage?.removeItem(options.name)
    },
    getOptions: () => options,
    rehydrate: () => hydrate() as Promise<void>,
    hasHydrated: () => hasHydrated,
    onHydrate: (cb) => {
      hydrationListeners.add(cb)

      return () => {
        hydrationListeners.delete(cb)
      }
    },
    onFinishHydration: (cb) => {
      finishHydrationListeners.add(cb)

      return () => {
        finishHydrationListeners.delete(cb)
      }
    },
  }

  if (!options.skipHydration) {
    hydrate()
  }

  return stateFromStorage || configResult
}
```


---

### 🔹 Commit #09: `6e026d75`
- **完整 Hash**: `6e026d7530966146c963d5767433c0d838950b8f`
- **說明 (Ground Truth)**: chore: improve typing in devtools middleware (#3362)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/devtools.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:15, E:11, A:0) ➔ After(N:17, E:13, A:0)
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
  • + [新增節點] `originalDispatch (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `shouldDispatchFromDevtools` (FUNCTION_DEF)
  • + [新增呼叫邊] `devtoolsImpl` ──[CALLS [guard: (action.type === '__setState')]]──> `shouldDispatchFromDevtools`
  • + [新增呼叫邊] `dispatch` ──[CALLS]──> `originalDispatch (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `dispatch()`
- **變更前簽章 (Before)**: `dispatch(...args: any[])` (L279~L292)
- **變更後簽章 (After)**: `dispatch(...args: any[])` (L285~L298)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(...args: any[]) => {
        if (
          import.meta.env?.MODE !== 'production' &&
          args[0].type === '__setState' &&
          !didWarnAboutReservedActionType
        ) {
          console.warn(
            '[zustand devtools middleware] "__setState" action type is reserved ' +
              'to set state from the devtools. Avoid using it.',
          )
          didWarnAboutReservedActionType = true
        }
        ;(originalDispatch as any)(...args)
      }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(...args: any[]) => {
        if (
          import.meta.env?.MODE !== 'production' &&
          args[0].type === '__setState' &&
          !didWarnAboutReservedActionType
        ) {
          console.warn(
            '[zustand devtools middleware] "__setState" action type is reserved ' +
              'to set state from the devtools. Avoid using it.',
          )
          didWarnAboutReservedActionType = true
        }
        originalDispatch(...args)
      }
```

### 🔹 函式: `devtoolsImpl()`
- **變更前簽章 (Before)**: `devtoolsImpl(fn, devtoolsOptions = {})` (L179~L417)
- **變更後簽章 (After)**: `devtoolsImpl(fn, devtoolsOptions = {})` (L188~L423)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(fn, devtoolsOptions = {}) =>
  (set, get, api) => {
    const { enabled, anonymousActionType, store, ...options } = devtoolsOptions

    type S = ReturnType<typeof fn> & {
      [store: string]: ReturnType<typeof fn>
    }
    type PartialState = Partial<S> | ((s: S) => Partial<S>)

    let extensionConnector:
      | (typeof window)['__REDUX_DEVTOOLS_EXTENSION__']
      | false
    try {
      extensionConnector =
        (enabled ?? import.meta.env?.MODE !== 'production') &&
        window.__REDUX_DEVTOOLS_EXTENSION__
    } catch {
      // ignored
    }

    if (!extensionConnector) {
      return fn(set, get, api)
    }

    const { connection, ...connectionInformation } =
      extractConnectionInformation(store, extensionConnector, options)

    let isRecording = true
    ;(api.setState as any) = ((state, replace, nameOrAction: Action) => {
      const r = set(state, replace as any)
      if (!isRecording) return r
      const action: { type: string } =
        nameOrAction === undefined
          ? {
              type:
                anonymousActionType ||
                findCallerName(new Error().stack) ||
                'anonymous',
            }
          : typeof nameOrAction === 'string'
            ? { type: nameOrAction }
            : nameOrAction
      if (store === undefined) {
        connection?.send(action, get())
        return r
      }
      connection?.send(
        {
          ...action,
          type: `${store}/${action.type}`,
        },
        {
          ...getTrackedConnectionState(options.name),
          [store]: api.getState(),
        },
      )
      return r
    }) as NamedSet<S>
    ;(api as StoreApi<S> & StoreDevtools<S>).devtools = {
      cleanup: () => {
        if (
          connection &&
          typeof (connection as any).unsubscribe === 'function'
        ) {
          ;(connection as any).unsubscribe()
        }
        removeStoreFromTrackedConnections(options.name, store)
      },
    }

    const setStateFromDevtools: StoreApi<S>['setState'] = (...a) => {
      const originalIsRecording = isRecording
      isRecording = false
      set(...(a as Parameters<typeof set>))
      isRecording = originalIsRecording
    }

    const initialState = fn(api.setState, get, api)
    if (connectionInformation.type === 'untracked') {
      connection?.init(initialState)
    } else {
      connectionInformation.stores[connectionInformation.store] = api
      connection?.init(
        Object.fromEntries(
          Object.entries(connectionInformation.stores).map(([key, store]) => [
            key,
            key === connectionInformation.store
              ? initialState
              : store.getState(),
          ]),
        ),
      )
    }

    if (
      (api as any).dispatchFromDevtools &&
      typeof (api as any).dispatch === 'function'
    ) {
      let didWarnAboutReservedActionType = false
      const originalDispatch = (api as any).dispatch
      ;(api as any).dispatch = (...args: any[]) => {
        if (
          import.meta.env?.MODE !== 'production' &&
          args[0].type === '__setState' &&
          !didWarnAboutReservedActionType
        ) {
          console.warn(
            '[zustand devtools middleware] "__setState" action type is reserved ' +
              'to set state from the devtools. Avoid using it.',
          )
          didWarnAboutReservedActionType = true
        }
        ;(originalDispatch as any)(...args)
      }
    }

    ;(
      connection as unknown as {
        // FIXME https://github.com/reduxjs/redux-devtools/issues/1097
        subscribe: (
          listener: (message: Message) => void,
        ) => (() => void) | undefined
      }
    ).subscribe((message: any) => {
      switch (message.type) {
        case 'ACTION':
          if (typeof message.payload !== 'string') {
            console.error(
              '[zustand devtools middleware] Unsupported action format',
            )
            return
          }
          return parseJsonThen<{ type: unknown; state?: PartialState }>(
            message.payload,
            (action) => {
              if (action.type === '__setState') {
                if (store === undefined) {
                  setStateFromDevtools(action.state as PartialState)
                  return
                }
                if (Object.keys(action.state as S).length !== 1) {
                  console.error(
                    `
                    [zustand devtools middleware] Unsupported __setState action format.
                    When using 'store' option in devtools(), the 'state' should have only one key, which is a value of 'store' that was passed in devtools(),
                    and value of this only key should be a state object. Example: { "type": "__setState", "state": { "abc123Store": { "foo": "bar" } } }
                    `,
                  )
                }
                const stateFromDevtools = (action.state as S)[store]
                if (
                  stateFromDevtools === undefined ||
                  stateFromDevtools === null
                ) {
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(stateFromDevtools)
                ) {
                  setStateFromDevtools(stateFromDevtools)
                }
                return
              }

              if (!(api as any).dispatchFromDevtools) return
              if (typeof (api as any).dispatch !== 'function') return
              ;(api as any).dispatch(action)
            },
          )

        case 'DISPATCH':
          switch (message.payload.type) {
            case 'RESET':
              setStateFromDevtools(initialState as S)
              if (store === undefined) {
                return connection?.init(api.getState())
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'COMMIT':
              if (store === undefined) {
                connection?.init(api.getState())
                return
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'ROLLBACK':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  connection?.init(api.getState())
                  return
                }
                setStateFromDevtools(state[store] as S)
                connection?.init(getTrackedConnectionState(options.name))
              })

            case 'JUMP_TO_STATE':
            case 'JUMP_TO_ACTION':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(state[store])
                ) {
                  setStateFromDevtools(state[store] as S)
                }
              })

            case 'IMPORT_STATE': {
              const { nextLiftedState } = message.payload
              const lastComputedState =
                nextLiftedState.computedStates.slice(-1)[0]?.state
              if (!lastComputedState) return
              if (store === undefined) {
                setStateFromDevtools(lastComputedState)
              } else {
                setStateFromDevtools(lastComputedState[store])
              }
              connection?.send(
                null as any, // FIXME no-any
                nextLiftedState,
              )
              return
            }

            case 'PAUSE_RECORDING':
              return (isRecording = !isRecording)
          }
          return
      }
    })

    return initialState
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(fn, devtoolsOptions = {}) =>
  (set, get, api) => {
    const { enabled, anonymousActionType, store, ...options } = devtoolsOptions

    type S = ReturnType<typeof fn> & {
      [store: string]: ReturnType<typeof fn>
    }
    type PartialState = Partial<S> | ((s: S) => Partial<S>)

    let extensionConnector:
      | (typeof window)['__REDUX_DEVTOOLS_EXTENSION__']
      | false
    try {
      extensionConnector =
        (enabled ?? import.meta.env?.MODE !== 'production') &&
        window.__REDUX_DEVTOOLS_EXTENSION__
    } catch {
      // ignored
    }

    if (!extensionConnector) {
      return fn(set, get, api)
    }

    const { connection, ...connectionInformation } =
      extractConnectionInformation(store, extensionConnector, options)

    let isRecording = true
    api.setState = ((state, replace, nameOrAction: Action) => {
      const r = set(state, replace as any)
      if (!isRecording) return r
      const action: { type: string } =
        nameOrAction === undefined
          ? {
              type:
                anonymousActionType ||
                findCallerName(new Error().stack) ||
                'anonymous',
            }
          : typeof nameOrAction === 'string'
            ? { type: nameOrAction }
            : nameOrAction
      if (store === undefined) {
        connection?.send(action, get())
        return r
      }
      connection?.send(
        {
          ...action,
          type: `${store}/${action.type}`,
        },
        {
          ...getTrackedConnectionState(options.name),
          [store]: api.getState(),
        },
      )
      return r
    }) as NamedSet<S>
    ;(api as StoreApi<S> & StoreDevtools<S>).devtools = {
      cleanup: () => {
        if (
          connection &&
          typeof (connection as any).unsubscribe === 'function'
        ) {
          ;(connection as any).unsubscribe()
        }
        removeStoreFromTrackedConnections(options.name, store)
      },
    }

    const setStateFromDevtools: StoreApi<S>['setState'] = (...a) => {
      const originalIsRecording = isRecording
      isRecording = false
      set(...(a as Parameters<typeof set>))
      isRecording = originalIsRecording
    }

    const initialState = fn(api.setState, get, api)
    if (connectionInformation.type === 'untracked') {
      connection?.init(initialState)
    } else {
      connectionInformation.stores[connectionInformation.store] = api
      connection?.init(
        Object.fromEntries(
          Object.entries(connectionInformation.stores).map(([key, store]) => [
            key,
            key === connectionInformation.store
              ? initialState
              : store.getState(),
          ]),
        ),
      )
    }

    if (shouldDispatchFromDevtools(api)) {
      let didWarnAboutReservedActionType = false
      const originalDispatch = api.dispatch
      api.dispatch = (...args: any[]) => {
        if (
          import.meta.env?.MODE !== 'production' &&
          args[0].type === '__setState' &&
          !didWarnAboutReservedActionType
        ) {
          console.warn(
            '[zustand devtools middleware] "__setState" action type is reserved ' +
              'to set state from the devtools. Avoid using it.',
          )
          didWarnAboutReservedActionType = true
        }
        originalDispatch(...args)
      }
    }

    ;(
      connection as unknown as {
        // FIXME https://github.com/reduxjs/redux-devtools/issues/1097
        subscribe: (
          listener: (message: Message) => void,
        ) => (() => void) | undefined
      }
    ).subscribe((message) => {
      switch (message.type) {
        case 'ACTION':
          if (typeof message.payload !== 'string') {
            console.error(
              '[zustand devtools middleware] Unsupported action format',
            )
            return
          }
          return parseJsonThen<{ type: unknown; state?: PartialState }>(
            message.payload,
            (action) => {
              if (action.type === '__setState') {
                if (store === undefined) {
                  setStateFromDevtools(action.state as PartialState)
                  return
                }
                if (Object.keys(action.state as S).length !== 1) {
                  console.error(
                    `
                    [zustand devtools middleware] Unsupported __setState action format.
                    When using 'store' option in devtools(), the 'state' should have only one key, which is a value of 'store' that was passed in devtools(),
                    and value of this only key should be a state object. Example: { "type": "__setState", "state": { "abc123Store": { "foo": "bar" } } }
                    `,
                  )
                }
                const stateFromDevtools = (action.state as S)[store]
                if (
                  stateFromDevtools === undefined ||
                  stateFromDevtools === null
                ) {
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(stateFromDevtools)
                ) {
                  setStateFromDevtools(stateFromDevtools)
                }
                return
              }

              if (shouldDispatchFromDevtools(api)) {
                api.dispatch(action)
              }
            },
          )

        case 'DISPATCH':
          switch (message.payload.type) {
            case 'RESET':
              setStateFromDevtools(initialState as S)
              if (store === undefined) {
                return connection?.init(api.getState())
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'COMMIT':
              if (store === undefined) {
                connection?.init(api.getState())
                return
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'ROLLBACK':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  connection?.init(api.getState())
                  return
                }
                setStateFromDevtools(state[store] as S)
                connection?.init(getTrackedConnectionState(options.name))
              })

            case 'JUMP_TO_STATE':
            case 'JUMP_TO_ACTION':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(state[store])
                ) {
                  setStateFromDevtools(state[store] as S)
                }
              })

            case 'IMPORT_STATE': {
              const { nextLiftedState } = message.payload
              const lastComputedState =
                nextLiftedState.computedStates.slice(-1)[0]?.state
              if (!lastComputedState) return
              if (store === undefined) {
                setStateFromDevtools(lastComputedState)
              } else {
                setStateFromDevtools(lastComputedState[store])
              }
              connection?.send(
                null as any, // FIXME no-any
                nextLiftedState,
              )
              return
            }

            case 'PAUSE_RECORDING':
              return (isRecording = !isRecording)
          }
          return
      }
    })

    return initialState
  }
```


---

### 🔹 Commit #10: `d0cb549f`
- **完整 Hash**: `d0cb549ff67ab2ecc62202a5d261f4cffcedb9f4`
- **說明 (Ground Truth)**: fix(persist): prevent race condition during concurrent rehydrate calls (#3336)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/persist.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:34, E:21, A:0) ➔ After(N:34, E:21, A:0)
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
  - 💥 作用域阻隔: 函式 'setItem' 被深鎖在內部閉包 (scope:createJSONStorage@after/src/middleware/persist.ts:L31C8)，外部無法調用！
  - 💥 作用域阻隔: 函式 'hydrate' 被深鎖在內部閉包 (scope:arrow@after/src/middleware/persist.ts:L187C59)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `hydrate()`
- **變更前簽章 (Before)**: `hydrate()` (L250~L323)
- **變更後簽章 (After)**: `hydrate()` (L253~L340)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        postRehydrationCallback?.(undefined, e)
      })
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    // Increment version to invalidate any in-flight hydration
    const currentVersion = ++hydrationVersion
    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(undefined, e)
      })
  }
```

### 🔹 函式: `persistImpl()`
- **變更前簽章 (Before)**: `persistImpl(config, baseOptions)` (L187~L363)
- **變更後簽章 (After)**: `persistImpl(config, baseOptions)` (L187~L380)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(config, baseOptions) => (set, get, api) => {
  type S = ReturnType<typeof config>
  let options = {
    storage: createJSONStorage<S, void>(() => localStorage),
    partialize: (state: S) => state,
    version: 0,
    merge: (persistedState: unknown, currentState: S) => ({
      ...currentState,
      ...(persistedState as object),
    }),
    ...baseOptions,
  }

  let hasHydrated = false
  const hydrationListeners = new Set<PersistListener<S>>()
  const finishHydrationListeners = new Set<PersistListener<S>>()
  let storage = options.storage

  if (!storage) {
    return config(
      (...args) => {
        console.warn(
          `[zustand persist middleware] Unable to update item '${options.name}', the given storage is currently unavailable.`,
        )
        set(...(args as Parameters<typeof set>))
      },
      get,
      api,
    )
  }

  const setItem = () => {
    const state = options.partialize({ ...get() })
    return (storage as PersistStorage<S, unknown>).setItem(options.name, {
      state,
      version: options.version,
    })
  }

  const savedSetState = api.setState

  api.setState = (state, replace) => {
    savedSetState(state, replace as any)
    return setItem()
  }

  const configResult = config(
    (...args) => {
      set(...(args as Parameters<typeof set>))
      return setItem()
    },
    get,
    api,
  )

  api.getInitialState = () => configResult

  // a workaround to solve the issue of not storing rehydrated state in sync storage
  // the set(state) value would be later overridden with initial state by create()
  // to avoid this, we merge the state from localStorage into the initial state.
  let stateFromStorage: S | undefined

  // rehydrate initial state with existing stored state
  const hydrate = () => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        postRehydrationCallback?.(undefined, e)
      })
  }

  ;(api as StoreApi<S> & StorePersist<StoreApi<S>, S, unknown>).persist = {
    setOptions: (newOptions) => {
      options = {
        ...options,
        ...newOptions,
      }

      if (newOptions.storage) {
        storage = newOptions.storage
      }
    },
    clearStorage: () => {
      storage?.removeItem(options.name)
    },
    getOptions: () => options,
    rehydrate: () => hydrate() as Promise<void>,
    hasHydrated: () => hasHydrated,
    onHydrate: (cb) => {
      hydrationListeners.add(cb)

      return () => {
        hydrationListeners.delete(cb)
      }
    },
    onFinishHydration: (cb) => {
      finishHydrationListeners.add(cb)

      return () => {
        finishHydrationListeners.delete(cb)
      }
    },
  }

  if (!options.skipHydration) {
    hydrate()
  }

  return stateFromStorage || configResult
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(config, baseOptions) => (set, get, api) => {
  type S = ReturnType<typeof config>
  let options = {
    storage: createJSONStorage<S, void>(() => localStorage),
    partialize: (state: S) => state,
    version: 0,
    merge: (persistedState: unknown, currentState: S) => ({
      ...currentState,
      ...(persistedState as object),
    }),
    ...baseOptions,
  }

  let hasHydrated = false
  // Counter to track hydration versions and prevent race conditions
  // when multiple rehydrate() calls happen concurrently
  let hydrationVersion = 0
  const hydrationListeners = new Set<PersistListener<S>>()
  const finishHydrationListeners = new Set<PersistListener<S>>()
  let storage = options.storage

  if (!storage) {
    return config(
      (...args) => {
        console.warn(
          `[zustand persist middleware] Unable to update item '${options.name}', the given storage is currently unavailable.`,
        )
        set(...(args as Parameters<typeof set>))
      },
      get,
      api,
    )
  }

  const setItem = () => {
    const state = options.partialize({ ...get() })
    return (storage as PersistStorage<S, unknown>).setItem(options.name, {
      state,
      version: options.version,
    })
  }

  const savedSetState = api.setState

  api.setState = (state, replace) => {
    savedSetState(state, replace as any)
    return setItem()
  }

  const configResult = config(
    (...args) => {
      set(...(args as Parameters<typeof set>))
      return setItem()
    },
    get,
    api,
  )

  api.getInitialState = () => configResult

  // a workaround to solve the issue of not storing rehydrated state in sync storage
  // the set(state) value would be later overridden with initial state by create()
  // to avoid this, we merge the state from localStorage into the initial state.
  let stateFromStorage: S | undefined

  // rehydrate initial state with existing stored state
  const hydrate = () => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    // Increment version to invalidate any in-flight hydration
    const currentVersion = ++hydrationVersion
    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        // Abort if a newer hydration has started
        if (currentVersion !== hydrationVersion) {
          return
        }
        postRehydrationCallback?.(undefined, e)
      })
  }

  ;(api as StoreApi<S> & StorePersist<StoreApi<S>, S, unknown>).persist = {
    setOptions: (newOptions) => {
      options = {
        ...options,
        ...newOptions,
      }

      if (newOptions.storage) {
        storage = newOptions.storage
      }
    },
    clearStorage: () => {
      storage?.removeItem(options.name)
    },
    getOptions: () => options,
    rehydrate: () => hydrate() as Promise<void>,
    hasHydrated: () => hasHydrated,
    onHydrate: (cb) => {
      hydrationListeners.add(cb)

      return () => {
        hydrationListeners.delete(cb)
      }
    },
    onFinishHydration: (cb) => {
      finishHydrationListeners.add(cb)

      return () => {
        finishHydrationListeners.delete(cb)
      }
    },
  }

  if (!options.skipHydration) {
    hydrate()
  }

  return stateFromStorage || configResult
}
```


---

### 🔹 Commit #11: `f9990222`
- **完整 Hash**: `f99902226a1791653aaaa213d786fa3cd1d6731e`
- **說明 (Ground Truth)**: experimental: unstable ssrSafe middleware (#3308)
- **變更檔案數**: 2

#### 📄 檔案: `src/middleware.ts`
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

#### 📄 檔案: `src/middleware/ssrSafe.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:3, E:1, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `config (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `ssrSafe` (FUNCTION_DEF)
  • + [新增節點] `ssrSet` (FUNCTION_DEF)
  • + [新增呼叫邊] `ssrSafe` ──[CALLS [guard: (!isSSR)]]──> `config (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #12: `feddc0c2`
- **完整 Hash**: `feddc0c210c555fc58d9c9a7100545603f568cf5`
- **說明 (Ground Truth)**: feat(middleare/persist): return storage promise from setState (#3206)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/persist.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:34, E:21, A:0) ➔ After(N:34, E:21, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'setItem' 被深鎖在內部閉包 (scope:createJSONStorage@after/src/middleware/persist.ts:L31C8)，外部無法調用！
  - 💥 作用域阻隔: 函式 'hydrate' 被深鎖在內部閉包 (scope:arrow@after/src/middleware/persist.ts:L187C59)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `configResult()`
- **變更前簽章 (Before)**: `configResult(...args)` (L219~L222)
- **變更後簽章 (After)**: `configResult(...args)` (L234~L237)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(...args) => {
      set(...(args as Parameters<typeof set>))
      void setItem()
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(...args) => {
      set(...(args as Parameters<typeof set>))
      return setItem()
    }
```

### 🔹 函式: `setState()`
- **變更前簽章 (Before)**: `setState(state, replace)` (L213~L216)
- **變更後簽章 (After)**: `setState(state, replace)` (L228~L231)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(state, replace) => {
    savedSetState(state, replace as any)
    void setItem()
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(state, replace) => {
    savedSetState(state, replace as any)
    return setItem()
  }
```

### 🔹 函式: `persistImpl()`
- **變更前簽章 (Before)**: `persistImpl(config, baseOptions)` (L172~L348)
- **變更後簽章 (After)**: `persistImpl(config, baseOptions)` (L187~L363)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(config, baseOptions) => (set, get, api) => {
  type S = ReturnType<typeof config>
  let options = {
    storage: createJSONStorage<S>(() => localStorage),
    partialize: (state: S) => state,
    version: 0,
    merge: (persistedState: unknown, currentState: S) => ({
      ...currentState,
      ...(persistedState as object),
    }),
    ...baseOptions,
  }

  let hasHydrated = false
  const hydrationListeners = new Set<PersistListener<S>>()
  const finishHydrationListeners = new Set<PersistListener<S>>()
  let storage = options.storage

  if (!storage) {
    return config(
      (...args) => {
        console.warn(
          `[zustand persist middleware] Unable to update item '${options.name}', the given storage is currently unavailable.`,
        )
        set(...(args as Parameters<typeof set>))
      },
      get,
      api,
    )
  }

  const setItem = () => {
    const state = options.partialize({ ...get() })
    return (storage as PersistStorage<S>).setItem(options.name, {
      state,
      version: options.version,
    })
  }

  const savedSetState = api.setState

  api.setState = (state, replace) => {
    savedSetState(state, replace as any)
    void setItem()
  }

  const configResult = config(
    (...args) => {
      set(...(args as Parameters<typeof set>))
      void setItem()
    },
    get,
    api,
  )

  api.getInitialState = () => configResult

  // a workaround to solve the issue of not storing rehydrated state in sync storage
  // the set(state) value would be later overridden with initial state by create()
  // to avoid this, we merge the state from localStorage into the initial state.
  let stateFromStorage: S | undefined

  // rehydrate initial state with existing stored state
  const hydrate = () => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        postRehydrationCallback?.(undefined, e)
      })
  }

  ;(api as StoreApi<S> & StorePersist<S, S>).persist = {
    setOptions: (newOptions) => {
      options = {
        ...options,
        ...newOptions,
      }

      if (newOptions.storage) {
        storage = newOptions.storage
      }
    },
    clearStorage: () => {
      storage?.removeItem(options.name)
    },
    getOptions: () => options,
    rehydrate: () => hydrate() as Promise<void>,
    hasHydrated: () => hasHydrated,
    onHydrate: (cb) => {
      hydrationListeners.add(cb)

      return () => {
        hydrationListeners.delete(cb)
      }
    },
    onFinishHydration: (cb) => {
      finishHydrationListeners.add(cb)

      return () => {
        finishHydrationListeners.delete(cb)
      }
    },
  }

  if (!options.skipHydration) {
    hydrate()
  }

  return stateFromStorage || configResult
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(config, baseOptions) => (set, get, api) => {
  type S = ReturnType<typeof config>
  let options = {
    storage: createJSONStorage<S, void>(() => localStorage),
    partialize: (state: S) => state,
    version: 0,
    merge: (persistedState: unknown, currentState: S) => ({
      ...currentState,
      ...(persistedState as object),
    }),
    ...baseOptions,
  }

  let hasHydrated = false
  const hydrationListeners = new Set<PersistListener<S>>()
  const finishHydrationListeners = new Set<PersistListener<S>>()
  let storage = options.storage

  if (!storage) {
    return config(
      (...args) => {
        console.warn(
          `[zustand persist middleware] Unable to update item '${options.name}', the given storage is currently unavailable.`,
        )
        set(...(args as Parameters<typeof set>))
      },
      get,
      api,
    )
  }

  const setItem = () => {
    const state = options.partialize({ ...get() })
    return (storage as PersistStorage<S, unknown>).setItem(options.name, {
      state,
      version: options.version,
    })
  }

  const savedSetState = api.setState

  api.setState = (state, replace) => {
    savedSetState(state, replace as any)
    return setItem()
  }

  const configResult = config(
    (...args) => {
      set(...(args as Parameters<typeof set>))
      return setItem()
    },
    get,
    api,
  )

  api.getInitialState = () => configResult

  // a workaround to solve the issue of not storing rehydrated state in sync storage
  // the set(state) value would be later overridden with initial state by create()
  // to avoid this, we merge the state from localStorage into the initial state.
  let stateFromStorage: S | undefined

  // rehydrate initial state with existing stored state
  const hydrate = () => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        postRehydrationCallback?.(undefined, e)
      })
  }

  ;(api as StoreApi<S> & StorePersist<StoreApi<S>, S, unknown>).persist = {
    setOptions: (newOptions) => {
      options = {
        ...options,
        ...newOptions,
      }

      if (newOptions.storage) {
        storage = newOptions.storage
      }
    },
    clearStorage: () => {
      storage?.removeItem(options.name)
    },
    getOptions: () => options,
    rehydrate: () => hydrate() as Promise<void>,
    hasHydrated: () => hasHydrated,
    onHydrate: (cb) => {
      hydrationListeners.add(cb)

      return () => {
        hydrationListeners.delete(cb)
      }
    },
    onFinishHydration: (cb) => {
      finishHydrationListeners.add(cb)

      return () => {
        finishHydrationListeners.delete(cb)
      }
    },
  }

  if (!options.skipHydration) {
    hydrate()
  }

  return stateFromStorage || configResult
}
```


---

### 🔹 Commit #13: `2cc19881`
- **完整 Hash**: `2cc19881fad6defaabe4a2628609ab79fce6068f`
- **說明 (Ground Truth)**: fix(shallow): undefined value (#3205)
- **變更檔案數**: 1

#### 📄 檔案: `src/vanilla/shallow.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:7, E:4, A:0) ➔ After(N:7, E:4, A:0)
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

### 🔹 函式: `compareEntries()`
- **變更前簽章 (Before)**: `compareEntries(
  valueA: { entries(): Iterable<[unknown, unknown]> },
  valueB: { entries(): Iterable<[unknown, unknown]> },
)` (L12~L27)
- **變更後簽章 (After)**: `compareEntries(
  valueA: { entries(): Iterable<[unknown, unknown]> },
  valueB: { entries(): Iterable<[unknown, unknown]> },
)` (L12~L27)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(
  valueA: { entries(): Iterable<[unknown, unknown]> },
  valueB: { entries(): Iterable<[unknown, unknown]> },
) => {
  const mapA = valueA instanceof Map ? valueA : new Map(valueA.entries())
  const mapB = valueB instanceof Map ? valueB : new Map(valueB.entries())
  if (mapA.size !== mapB.size) {
    return false
  }
  for (const [key, value] of mapA) {
    if (!Object.is(value, mapB.get(key))) {
      return false
    }
  }
  return true
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(
  valueA: { entries(): Iterable<[unknown, unknown]> },
  valueB: { entries(): Iterable<[unknown, unknown]> },
) => {
  const mapA = valueA instanceof Map ? valueA : new Map(valueA.entries())
  const mapB = valueB instanceof Map ? valueB : new Map(valueB.entries())
  if (mapA.size !== mapB.size) {
    return false
  }
  for (const [key, value] of mapA) {
    if (!mapB.has(key) || !Object.is(value, mapB.get(key))) {
      return false
    }
  }
  return true
}
```


---

### 🔹 Commit #14: `5aa923e8`
- **完整 Hash**: `5aa923e8c3b84c2ba23297210deb13c218b8cfa1`
- **說明 (Ground Truth)**: fix(react): useCallback for getSnapshot (#3192)
- **變更檔案數**: 1

#### 📄 檔案: `src/react.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:9, E:4, A:0) ➔ After(N:7, E:3, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 2, +Edges: 1, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `slice` (FUNCTION_DEF)
  • - [移除節點] `slice` (FUNCTION_DEF)
  • + [新增呼叫邊] `useStore` ──[CALLS]──> `selector (External/Unresolved)`
  • - [移除呼叫邊] `slice` ──[CALLS]──> `selector (External/Unresolved)`
  • - [移除呼叫邊] `slice` ──[CALLS]──> `selector (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `useStore()`
- **變更前簽章 (Before)**: `function useStore<TState, StateSlice>(
  api: ReadonlyStoreApi<TState>,
  selector: (state: TState) => StateSlice = identity as any,
)` (L26~L37)
- **變更後簽章 (After)**: `function useStore<TState, StateSlice>(
  api: ReadonlyStoreApi<TState>,
  selector: (state: TState) => StateSlice = identity as any,
)` (L26~L37)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function useStore<TState, StateSlice>(
  api: ReadonlyStoreApi<TState>,
  selector: (state: TState) => StateSlice = identity as any,
) {
  const slice = React.useSyncExternalStore(
    api.subscribe,
    () => selector(api.getState()),
    () => selector(api.getInitialState()),
  )
  React.useDebugValue(slice)
  return slice
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function useStore<TState, StateSlice>(
  api: ReadonlyStoreApi<TState>,
  selector: (state: TState) => StateSlice = identity as any,
) {
  const slice = React.useSyncExternalStore(
    api.subscribe,
    React.useCallback(() => selector(api.getState()), [api, selector]),
    React.useCallback(() => selector(api.getInitialState()), [api, selector]),
  )
  React.useDebugValue(slice)
  return slice
}
```


---

### 🔹 Commit #15: `5bc717b6`
- **完整 Hash**: `5bc717b66334e407dfdff0fa1b15330d81f290dd`
- **說明 (Ground Truth)**: refactor(middleware): replace export * with explicit named and type exports (#3151)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware.ts`
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

### 🔹 Commit #16: `ca08a5eb`
- **完整 Hash**: `ca08a5ebf944bf4add0a78d0573edbb6a52e41ae`
- **說明 (Ground Truth)**: perf(devtools): avoid inferring action type when explicit action name is provided (#3147)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/devtools.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:15, E:11, A:0) ➔ After(N:15, E:11, A:0)
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

### 🔹 函式: `devtoolsImpl()`
- **變更前簽章 (Before)**: `devtoolsImpl(fn, devtoolsOptions = {})` (L179~L413)
- **變更後簽章 (After)**: `devtoolsImpl(fn, devtoolsOptions = {})` (L179~L417)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(fn, devtoolsOptions = {}) =>
  (set, get, api) => {
    const { enabled, anonymousActionType, store, ...options } = devtoolsOptions

    type S = ReturnType<typeof fn> & {
      [store: string]: ReturnType<typeof fn>
    }
    type PartialState = Partial<S> | ((s: S) => Partial<S>)

    let extensionConnector:
      | (typeof window)['__REDUX_DEVTOOLS_EXTENSION__']
      | false
    try {
      extensionConnector =
        (enabled ?? import.meta.env?.MODE !== 'production') &&
        window.__REDUX_DEVTOOLS_EXTENSION__
    } catch {
      // ignored
    }

    if (!extensionConnector) {
      return fn(set, get, api)
    }

    const { connection, ...connectionInformation } =
      extractConnectionInformation(store, extensionConnector, options)

    let isRecording = true
    ;(api.setState as any) = ((state, replace, nameOrAction: Action) => {
      const r = set(state, replace as any)
      if (!isRecording) return r
      const inferredActionType = findCallerName(new Error().stack)
      const action: { type: string } =
        nameOrAction === undefined
          ? { type: anonymousActionType || inferredActionType || 'anonymous' }
          : typeof nameOrAction === 'string'
            ? { type: nameOrAction }
            : nameOrAction
      if (store === undefined) {
        connection?.send(action, get())
        return r
      }
      connection?.send(
        {
          ...action,
          type: `${store}/${action.type}`,
        },
        {
          ...getTrackedConnectionState(options.name),
          [store]: api.getState(),
        },
      )
      return r
    }) as NamedSet<S>
    ;(api as StoreApi<S> & StoreDevtools<S>).devtools = {
      cleanup: () => {
        if (
          connection &&
          typeof (connection as any).unsubscribe === 'function'
        ) {
          ;(connection as any).unsubscribe()
        }
        removeStoreFromTrackedConnections(options.name, store)
      },
    }

    const setStateFromDevtools: StoreApi<S>['setState'] = (...a) => {
      const originalIsRecording = isRecording
      isRecording = false
      set(...(a as Parameters<typeof set>))
      isRecording = originalIsRecording
    }

    const initialState = fn(api.setState, get, api)
    if (connectionInformation.type === 'untracked') {
      connection?.init(initialState)
    } else {
      connectionInformation.stores[connectionInformation.store] = api
      connection?.init(
        Object.fromEntries(
          Object.entries(connectionInformation.stores).map(([key, store]) => [
            key,
            key === connectionInformation.store
              ? initialState
              : store.getState(),
          ]),
        ),
      )
    }

    if (
      (api as any).dispatchFromDevtools &&
      typeof (api as any).dispatch === 'function'
    ) {
      let didWarnAboutReservedActionType = false
      const originalDispatch = (api as any).dispatch
      ;(api as any).dispatch = (...args: any[]) => {
        if (
          import.meta.env?.MODE !== 'production' &&
          args[0].type === '__setState' &&
          !didWarnAboutReservedActionType
        ) {
          console.warn(
            '[zustand devtools middleware] "__setState" action type is reserved ' +
              'to set state from the devtools. Avoid using it.',
          )
          didWarnAboutReservedActionType = true
        }
        ;(originalDispatch as any)(...args)
      }
    }

    ;(
      connection as unknown as {
        // FIXME https://github.com/reduxjs/redux-devtools/issues/1097
        subscribe: (
          listener: (message: Message) => void,
        ) => (() => void) | undefined
      }
    ).subscribe((message: any) => {
      switch (message.type) {
        case 'ACTION':
          if (typeof message.payload !== 'string') {
            console.error(
              '[zustand devtools middleware] Unsupported action format',
            )
            return
          }
          return parseJsonThen<{ type: unknown; state?: PartialState }>(
            message.payload,
            (action) => {
              if (action.type === '__setState') {
                if (store === undefined) {
                  setStateFromDevtools(action.state as PartialState)
                  return
                }
                if (Object.keys(action.state as S).length !== 1) {
                  console.error(
                    `
                    [zustand devtools middleware] Unsupported __setState action format.
                    When using 'store' option in devtools(), the 'state' should have only one key, which is a value of 'store' that was passed in devtools(),
                    and value of this only key should be a state object. Example: { "type": "__setState", "state": { "abc123Store": { "foo": "bar" } } }
                    `,
                  )
                }
                const stateFromDevtools = (action.state as S)[store]
                if (
                  stateFromDevtools === undefined ||
                  stateFromDevtools === null
                ) {
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(stateFromDevtools)
                ) {
                  setStateFromDevtools(stateFromDevtools)
                }
                return
              }

              if (!(api as any).dispatchFromDevtools) return
              if (typeof (api as any).dispatch !== 'function') return
              ;(api as any).dispatch(action)
            },
          )

        case 'DISPATCH':
          switch (message.payload.type) {
            case 'RESET':
              setStateFromDevtools(initialState as S)
              if (store === undefined) {
                return connection?.init(api.getState())
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'COMMIT':
              if (store === undefined) {
                connection?.init(api.getState())
                return
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'ROLLBACK':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  connection?.init(api.getState())
                  return
                }
                setStateFromDevtools(state[store] as S)
                connection?.init(getTrackedConnectionState(options.name))
              })

            case 'JUMP_TO_STATE':
            case 'JUMP_TO_ACTION':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(state[store])
                ) {
                  setStateFromDevtools(state[store] as S)
                }
              })

            case 'IMPORT_STATE': {
              const { nextLiftedState } = message.payload
              const lastComputedState =
                nextLiftedState.computedStates.slice(-1)[0]?.state
              if (!lastComputedState) return
              if (store === undefined) {
                setStateFromDevtools(lastComputedState)
              } else {
                setStateFromDevtools(lastComputedState[store])
              }
              connection?.send(
                null as any, // FIXME no-any
                nextLiftedState,
              )
              return
            }

            case 'PAUSE_RECORDING':
              return (isRecording = !isRecording)
          }
          return
      }
    })

    return initialState
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(fn, devtoolsOptions = {}) =>
  (set, get, api) => {
    const { enabled, anonymousActionType, store, ...options } = devtoolsOptions

    type S = ReturnType<typeof fn> & {
      [store: string]: ReturnType<typeof fn>
    }
    type PartialState = Partial<S> | ((s: S) => Partial<S>)

    let extensionConnector:
      | (typeof window)['__REDUX_DEVTOOLS_EXTENSION__']
      | false
    try {
      extensionConnector =
        (enabled ?? import.meta.env?.MODE !== 'production') &&
        window.__REDUX_DEVTOOLS_EXTENSION__
    } catch {
      // ignored
    }

    if (!extensionConnector) {
      return fn(set, get, api)
    }

    const { connection, ...connectionInformation } =
      extractConnectionInformation(store, extensionConnector, options)

    let isRecording = true
    ;(api.setState as any) = ((state, replace, nameOrAction: Action) => {
      const r = set(state, replace as any)
      if (!isRecording) return r
      const action: { type: string } =
        nameOrAction === undefined
          ? {
              type:
                anonymousActionType ||
                findCallerName(new Error().stack) ||
                'anonymous',
            }
          : typeof nameOrAction === 'string'
            ? { type: nameOrAction }
            : nameOrAction
      if (store === undefined) {
        connection?.send(action, get())
        return r
      }
      connection?.send(
        {
          ...action,
          type: `${store}/${action.type}`,
        },
        {
          ...getTrackedConnectionState(options.name),
          [store]: api.getState(),
        },
      )
      return r
    }) as NamedSet<S>
    ;(api as StoreApi<S> & StoreDevtools<S>).devtools = {
      cleanup: () => {
        if (
          connection &&
          typeof (connection as any).unsubscribe === 'function'
        ) {
          ;(connection as any).unsubscribe()
        }
        removeStoreFromTrackedConnections(options.name, store)
      },
    }

    const setStateFromDevtools: StoreApi<S>['setState'] = (...a) => {
      const originalIsRecording = isRecording
      isRecording = false
      set(...(a as Parameters<typeof set>))
      isRecording = originalIsRecording
    }

    const initialState = fn(api.setState, get, api)
    if (connectionInformation.type === 'untracked') {
      connection?.init(initialState)
    } else {
      connectionInformation.stores[connectionInformation.store] = api
      connection?.init(
        Object.fromEntries(
          Object.entries(connectionInformation.stores).map(([key, store]) => [
            key,
            key === connectionInformation.store
              ? initialState
              : store.getState(),
          ]),
        ),
      )
    }

    if (
      (api as any).dispatchFromDevtools &&
      typeof (api as any).dispatch === 'function'
    ) {
      let didWarnAboutReservedActionType = false
      const originalDispatch = (api as any).dispatch
      ;(api as any).dispatch = (...args: any[]) => {
        if (
          import.meta.env?.MODE !== 'production' &&
          args[0].type === '__setState' &&
          !didWarnAboutReservedActionType
        ) {
          console.warn(
            '[zustand devtools middleware] "__setState" action type is reserved ' +
              'to set state from the devtools. Avoid using it.',
          )
          didWarnAboutReservedActionType = true
        }
        ;(originalDispatch as any)(...args)
      }
    }

    ;(
      connection as unknown as {
        // FIXME https://github.com/reduxjs/redux-devtools/issues/1097
        subscribe: (
          listener: (message: Message) => void,
        ) => (() => void) | undefined
      }
    ).subscribe((message: any) => {
      switch (message.type) {
        case 'ACTION':
          if (typeof message.payload !== 'string') {
            console.error(
              '[zustand devtools middleware] Unsupported action format',
            )
            return
          }
          return parseJsonThen<{ type: unknown; state?: PartialState }>(
            message.payload,
            (action) => {
              if (action.type === '__setState') {
                if (store === undefined) {
                  setStateFromDevtools(action.state as PartialState)
                  return
                }
                if (Object.keys(action.state as S).length !== 1) {
                  console.error(
                    `
                    [zustand devtools middleware] Unsupported __setState action format.
                    When using 'store' option in devtools(), the 'state' should have only one key, which is a value of 'store' that was passed in devtools(),
                    and value of this only key should be a state object. Example: { "type": "__setState", "state": { "abc123Store": { "foo": "bar" } } }
                    `,
                  )
                }
                const stateFromDevtools = (action.state as S)[store]
                if (
                  stateFromDevtools === undefined ||
                  stateFromDevtools === null
                ) {
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(stateFromDevtools)
                ) {
                  setStateFromDevtools(stateFromDevtools)
                }
                return
              }

              if (!(api as any).dispatchFromDevtools) return
              if (typeof (api as any).dispatch !== 'function') return
              ;(api as any).dispatch(action)
            },
          )

        case 'DISPATCH':
          switch (message.payload.type) {
            case 'RESET':
              setStateFromDevtools(initialState as S)
              if (store === undefined) {
                return connection?.init(api.getState())
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'COMMIT':
              if (store === undefined) {
                connection?.init(api.getState())
                return
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'ROLLBACK':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  connection?.init(api.getState())
                  return
                }
                setStateFromDevtools(state[store] as S)
                connection?.init(getTrackedConnectionState(options.name))
              })

            case 'JUMP_TO_STATE':
            case 'JUMP_TO_ACTION':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(state[store])
                ) {
                  setStateFromDevtools(state[store] as S)
                }
              })

            case 'IMPORT_STATE': {
              const { nextLiftedState } = message.payload
              const lastComputedState =
                nextLiftedState.computedStates.slice(-1)[0]?.state
              if (!lastComputedState) return
              if (store === undefined) {
                setStateFromDevtools(lastComputedState)
              } else {
                setStateFromDevtools(lastComputedState[store])
              }
              connection?.send(
                null as any, // FIXME no-any
                nextLiftedState,
              )
              return
            }

            case 'PAUSE_RECORDING':
              return (isRecording = !isRecording)
          }
          return
      }
    })

    return initialState
  }
```


---

### 🔹 Commit #17: `670b60e1`
- **完整 Hash**: `670b60e19ab44789f41cdb60c476a5eeb647e3bb`
- **說明 (Ground Truth)**: feat(devtool): inferred action type (#2987)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/devtools.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:13, E:10, A:0) ➔ After(N:15, E:11, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `apiSetStateLineIndex` (FUNCTION_DEF)
  • + [新增節點] `findCallerName` (FUNCTION_DEF)
  • + [新增呼叫邊] `devtoolsImpl` ──[CALLS [guard: (!isRecording)]]──> `findCallerName`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `devtoolsImpl()`
- **變更前簽章 (Before)**: `devtoolsImpl(fn, devtoolsOptions = {})` (L166~L399)
- **變更後簽章 (After)**: `devtoolsImpl(fn, devtoolsOptions = {})` (L179~L413)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(fn, devtoolsOptions = {}) =>
  (set, get, api) => {
    const { enabled, anonymousActionType, store, ...options } = devtoolsOptions

    type S = ReturnType<typeof fn> & {
      [store: string]: ReturnType<typeof fn>
    }
    type PartialState = Partial<S> | ((s: S) => Partial<S>)

    let extensionConnector:
      | (typeof window)['__REDUX_DEVTOOLS_EXTENSION__']
      | false
    try {
      extensionConnector =
        (enabled ?? import.meta.env?.MODE !== 'production') &&
        window.__REDUX_DEVTOOLS_EXTENSION__
    } catch {
      // ignored
    }

    if (!extensionConnector) {
      return fn(set, get, api)
    }

    const { connection, ...connectionInformation } =
      extractConnectionInformation(store, extensionConnector, options)

    let isRecording = true
    ;(api.setState as any) = ((state, replace, nameOrAction: Action) => {
      const r = set(state, replace as any)
      if (!isRecording) return r
      const action: { type: string } =
        nameOrAction === undefined
          ? { type: anonymousActionType || 'anonymous' }
          : typeof nameOrAction === 'string'
            ? { type: nameOrAction }
            : nameOrAction
      if (store === undefined) {
        connection?.send(action, get())
        return r
      }
      connection?.send(
        {
          ...action,
          type: `${store}/${action.type}`,
        },
        {
          ...getTrackedConnectionState(options.name),
          [store]: api.getState(),
        },
      )
      return r
    }) as NamedSet<S>
    ;(api as StoreApi<S> & StoreDevtools<S>).devtools = {
      cleanup: () => {
        if (
          connection &&
          typeof (connection as any).unsubscribe === 'function'
        ) {
          ;(connection as any).unsubscribe()
        }
        removeStoreFromTrackedConnections(options.name, store)
      },
    }

    const setStateFromDevtools: StoreApi<S>['setState'] = (...a) => {
      const originalIsRecording = isRecording
      isRecording = false
      set(...(a as Parameters<typeof set>))
      isRecording = originalIsRecording
    }

    const initialState = fn(api.setState, get, api)
    if (connectionInformation.type === 'untracked') {
      connection?.init(initialState)
    } else {
      connectionInformation.stores[connectionInformation.store] = api
      connection?.init(
        Object.fromEntries(
          Object.entries(connectionInformation.stores).map(([key, store]) => [
            key,
            key === connectionInformation.store
              ? initialState
              : store.getState(),
          ]),
        ),
      )
    }

    if (
      (api as any).dispatchFromDevtools &&
      typeof (api as any).dispatch === 'function'
    ) {
      let didWarnAboutReservedActionType = false
      const originalDispatch = (api as any).dispatch
      ;(api as any).dispatch = (...args: any[]) => {
        if (
          import.meta.env?.MODE !== 'production' &&
          args[0].type === '__setState' &&
          !didWarnAboutReservedActionType
        ) {
          console.warn(
            '[zustand devtools middleware] "__setState" action type is reserved ' +
              'to set state from the devtools. Avoid using it.',
          )
          didWarnAboutReservedActionType = true
        }
        ;(originalDispatch as any)(...args)
      }
    }

    ;(
      connection as unknown as {
        // FIXME https://github.com/reduxjs/redux-devtools/issues/1097
        subscribe: (
          listener: (message: Message) => void,
        ) => (() => void) | undefined
      }
    ).subscribe((message: any) => {
      switch (message.type) {
        case 'ACTION':
          if (typeof message.payload !== 'string') {
            console.error(
              '[zustand devtools middleware] Unsupported action format',
            )
            return
          }
          return parseJsonThen<{ type: unknown; state?: PartialState }>(
            message.payload,
            (action) => {
              if (action.type === '__setState') {
                if (store === undefined) {
                  setStateFromDevtools(action.state as PartialState)
                  return
                }
                if (Object.keys(action.state as S).length !== 1) {
                  console.error(
                    `
                    [zustand devtools middleware] Unsupported __setState action format.
                    When using 'store' option in devtools(), the 'state' should have only one key, which is a value of 'store' that was passed in devtools(),
                    and value of this only key should be a state object. Example: { "type": "__setState", "state": { "abc123Store": { "foo": "bar" } } }
                    `,
                  )
                }
                const stateFromDevtools = (action.state as S)[store]
                if (
                  stateFromDevtools === undefined ||
                  stateFromDevtools === null
                ) {
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(stateFromDevtools)
                ) {
                  setStateFromDevtools(stateFromDevtools)
                }
                return
              }

              if (!(api as any).dispatchFromDevtools) return
              if (typeof (api as any).dispatch !== 'function') return
              ;(api as any).dispatch(action)
            },
          )

        case 'DISPATCH':
          switch (message.payload.type) {
            case 'RESET':
              setStateFromDevtools(initialState as S)
              if (store === undefined) {
                return connection?.init(api.getState())
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'COMMIT':
              if (store === undefined) {
                connection?.init(api.getState())
                return
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'ROLLBACK':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  connection?.init(api.getState())
                  return
                }
                setStateFromDevtools(state[store] as S)
                connection?.init(getTrackedConnectionState(options.name))
              })

            case 'JUMP_TO_STATE':
            case 'JUMP_TO_ACTION':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(state[store])
                ) {
                  setStateFromDevtools(state[store] as S)
                }
              })

            case 'IMPORT_STATE': {
              const { nextLiftedState } = message.payload
              const lastComputedState =
                nextLiftedState.computedStates.slice(-1)[0]?.state
              if (!lastComputedState) return
              if (store === undefined) {
                setStateFromDevtools(lastComputedState)
              } else {
                setStateFromDevtools(lastComputedState[store])
              }
              connection?.send(
                null as any, // FIXME no-any
                nextLiftedState,
              )
              return
            }

            case 'PAUSE_RECORDING':
              return (isRecording = !isRecording)
          }
          return
      }
    })

    return initialState
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(fn, devtoolsOptions = {}) =>
  (set, get, api) => {
    const { enabled, anonymousActionType, store, ...options } = devtoolsOptions

    type S = ReturnType<typeof fn> & {
      [store: string]: ReturnType<typeof fn>
    }
    type PartialState = Partial<S> | ((s: S) => Partial<S>)

    let extensionConnector:
      | (typeof window)['__REDUX_DEVTOOLS_EXTENSION__']
      | false
    try {
      extensionConnector =
        (enabled ?? import.meta.env?.MODE !== 'production') &&
        window.__REDUX_DEVTOOLS_EXTENSION__
    } catch {
      // ignored
    }

    if (!extensionConnector) {
      return fn(set, get, api)
    }

    const { connection, ...connectionInformation } =
      extractConnectionInformation(store, extensionConnector, options)

    let isRecording = true
    ;(api.setState as any) = ((state, replace, nameOrAction: Action) => {
      const r = set(state, replace as any)
      if (!isRecording) return r
      const inferredActionType = findCallerName(new Error().stack)
      const action: { type: string } =
        nameOrAction === undefined
          ? { type: anonymousActionType || inferredActionType || 'anonymous' }
          : typeof nameOrAction === 'string'
            ? { type: nameOrAction }
            : nameOrAction
      if (store === undefined) {
        connection?.send(action, get())
        return r
      }
      connection?.send(
        {
          ...action,
          type: `${store}/${action.type}`,
        },
        {
          ...getTrackedConnectionState(options.name),
          [store]: api.getState(),
        },
      )
      return r
    }) as NamedSet<S>
    ;(api as StoreApi<S> & StoreDevtools<S>).devtools = {
      cleanup: () => {
        if (
          connection &&
          typeof (connection as any).unsubscribe === 'function'
        ) {
          ;(connection as any).unsubscribe()
        }
        removeStoreFromTrackedConnections(options.name, store)
      },
    }

    const setStateFromDevtools: StoreApi<S>['setState'] = (...a) => {
      const originalIsRecording = isRecording
      isRecording = false
      set(...(a as Parameters<typeof set>))
      isRecording = originalIsRecording
    }

    const initialState = fn(api.setState, get, api)
    if (connectionInformation.type === 'untracked') {
      connection?.init(initialState)
    } else {
      connectionInformation.stores[connectionInformation.store] = api
      connection?.init(
        Object.fromEntries(
          Object.entries(connectionInformation.stores).map(([key, store]) => [
            key,
            key === connectionInformation.store
              ? initialState
              : store.getState(),
          ]),
        ),
      )
    }

    if (
      (api as any).dispatchFromDevtools &&
      typeof (api as any).dispatch === 'function'
    ) {
      let didWarnAboutReservedActionType = false
      const originalDispatch = (api as any).dispatch
      ;(api as any).dispatch = (...args: any[]) => {
        if (
          import.meta.env?.MODE !== 'production' &&
          args[0].type === '__setState' &&
          !didWarnAboutReservedActionType
        ) {
          console.warn(
            '[zustand devtools middleware] "__setState" action type is reserved ' +
              'to set state from the devtools. Avoid using it.',
          )
          didWarnAboutReservedActionType = true
        }
        ;(originalDispatch as any)(...args)
      }
    }

    ;(
      connection as unknown as {
        // FIXME https://github.com/reduxjs/redux-devtools/issues/1097
        subscribe: (
          listener: (message: Message) => void,
        ) => (() => void) | undefined
      }
    ).subscribe((message: any) => {
      switch (message.type) {
        case 'ACTION':
          if (typeof message.payload !== 'string') {
            console.error(
              '[zustand devtools middleware] Unsupported action format',
            )
            return
          }
          return parseJsonThen<{ type: unknown; state?: PartialState }>(
            message.payload,
            (action) => {
              if (action.type === '__setState') {
                if (store === undefined) {
                  setStateFromDevtools(action.state as PartialState)
                  return
                }
                if (Object.keys(action.state as S).length !== 1) {
                  console.error(
                    `
                    [zustand devtools middleware] Unsupported __setState action format.
                    When using 'store' option in devtools(), the 'state' should have only one key, which is a value of 'store' that was passed in devtools(),
                    and value of this only key should be a state object. Example: { "type": "__setState", "state": { "abc123Store": { "foo": "bar" } } }
                    `,
                  )
                }
                const stateFromDevtools = (action.state as S)[store]
                if (
                  stateFromDevtools === undefined ||
                  stateFromDevtools === null
                ) {
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(stateFromDevtools)
                ) {
                  setStateFromDevtools(stateFromDevtools)
                }
                return
              }

              if (!(api as any).dispatchFromDevtools) return
              if (typeof (api as any).dispatch !== 'function') return
              ;(api as any).dispatch(action)
            },
          )

        case 'DISPATCH':
          switch (message.payload.type) {
            case 'RESET':
              setStateFromDevtools(initialState as S)
              if (store === undefined) {
                return connection?.init(api.getState())
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'COMMIT':
              if (store === undefined) {
                connection?.init(api.getState())
                return
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'ROLLBACK':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  connection?.init(api.getState())
                  return
                }
                setStateFromDevtools(state[store] as S)
                connection?.init(getTrackedConnectionState(options.name))
              })

            case 'JUMP_TO_STATE':
            case 'JUMP_TO_ACTION':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(state[store])
                ) {
                  setStateFromDevtools(state[store] as S)
                }
              })

            case 'IMPORT_STATE': {
              const { nextLiftedState } = message.payload
              const lastComputedState =
                nextLiftedState.computedStates.slice(-1)[0]?.state
              if (!lastComputedState) return
              if (store === undefined) {
                setStateFromDevtools(lastComputedState)
              } else {
                setStateFromDevtools(lastComputedState[store])
              }
              connection?.send(
                null as any, // FIXME no-any
                nextLiftedState,
              )
              return
            }

            case 'PAUSE_RECORDING':
              return (isRecording = !isRecording)
          }
          return
      }
    })

    return initialState
  }
```


---

### 🔹 Commit #18: `a1c7f1c2`
- **完整 Hash**: `a1c7f1c20f21cf595bc954d9183000a9f5a4d428`
- **說明 (Ground Truth)**: refactor(middleware): rename argument names like 'a', 'f' (#3032)
- **變更檔案數**: 4

#### 📄 檔案: `src/middleware/combine.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:1, E:0, A:0) ➔ After(N:1, E:0, A:0)
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

### 🔹 函式: `combine()`
- **變更前簽章 (Before)**: `function combine<
  T extends object,
  U extends object,
  Mps extends [StoreMutatorIdentifier, unknown][] = [],
  Mcs extends [StoreMutatorIdentifier, unknown][] = [],
>(
  initialState: T,
  create: StateCreator<T, Mps, Mcs, U>,
): StateCreator<Write<T, U>, Mps, Mcs>` (L5~L15)
- **變更後簽章 (After)**: `function combine<
  T extends object,
  U extends object,
  Mps extends [StoreMutatorIdentifier, unknown][] = [],
  Mcs extends [StoreMutatorIdentifier, unknown][] = [],
>(
  initialState: T,
  create: StateCreator<T, Mps, Mcs, U>,
): StateCreator<Write<T, U>, Mps, Mcs>` (L5~L15)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function combine<
  T extends object,
  U extends object,
  Mps extends [StoreMutatorIdentifier, unknown][] = [],
  Mcs extends [StoreMutatorIdentifier, unknown][] = [],
>(
  initialState: T,
  create: StateCreator<T, Mps, Mcs, U>,
): StateCreator<Write<T, U>, Mps, Mcs> {
  return (...a) => Object.assign({}, initialState, (create as any)(...a))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function combine<
  T extends object,
  U extends object,
  Mps extends [StoreMutatorIdentifier, unknown][] = [],
  Mcs extends [StoreMutatorIdentifier, unknown][] = [],
>(
  initialState: T,
  create: StateCreator<T, Mps, Mcs, U>,
): StateCreator<Write<T, U>, Mps, Mcs> {
  return (...args) => Object.assign({}, initialState, (create as any)(...args))
}
```


#### 📄 檔案: `src/middleware/devtools.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:12, E:9, A:0) ➔ After(N:11, E:9, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 1, -Edges: 1, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `f (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `parseJsonThen` ──[CALLS [guard: (parsed !== undefined)]]──> `fn (External/Unresolved)`
  • - [移除呼叫邊] `parseJsonThen` ──[CALLS]──> `f (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `dispatch()`
- **變更前簽章 (Before)**: `dispatch(...a: any[])` (L234~L247)
- **變更後簽章 (After)**: `dispatch(...args: any[])` (L234~L247)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(...a: any[]) => {
        if (
          import.meta.env?.MODE !== 'production' &&
          a[0].type === '__setState' &&
          !didWarnAboutReservedActionType
        ) {
          console.warn(
            '[zustand devtools middleware] "__setState" action type is reserved ' +
              'to set state from the devtools. Avoid using it.',
          )
          didWarnAboutReservedActionType = true
        }
        ;(originalDispatch as any)(...a)
      }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(...args: any[]) => {
        if (
          import.meta.env?.MODE !== 'production' &&
          args[0].type === '__setState' &&
          !didWarnAboutReservedActionType
        ) {
          console.warn(
            '[zustand devtools middleware] "__setState" action type is reserved ' +
              'to set state from the devtools. Avoid using it.',
          )
          didWarnAboutReservedActionType = true
        }
        ;(originalDispatch as any)(...args)
      }
```

### 🔹 函式: `devtoolsImpl()`
- **變更前簽章 (Before)**: `devtoolsImpl(fn, devtoolsOptions = {})` (L150~L372)
- **變更後簽章 (After)**: `devtoolsImpl(fn, devtoolsOptions = {})` (L150~L372)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(fn, devtoolsOptions = {}) =>
  (set, get, api) => {
    const { enabled, anonymousActionType, store, ...options } = devtoolsOptions

    type S = ReturnType<typeof fn> & {
      [store: string]: ReturnType<typeof fn>
    }
    type PartialState = Partial<S> | ((s: S) => Partial<S>)

    let extensionConnector:
      | (typeof window)['__REDUX_DEVTOOLS_EXTENSION__']
      | false
    try {
      extensionConnector =
        (enabled ?? import.meta.env?.MODE !== 'production') &&
        window.__REDUX_DEVTOOLS_EXTENSION__
    } catch {
      // ignored
    }

    if (!extensionConnector) {
      return fn(set, get, api)
    }

    const { connection, ...connectionInformation } =
      extractConnectionInformation(store, extensionConnector, options)

    let isRecording = true
    ;(api.setState as any) = ((state, replace, nameOrAction: Action) => {
      const r = set(state, replace as any)
      if (!isRecording) return r
      const action: { type: string } =
        nameOrAction === undefined
          ? { type: anonymousActionType || 'anonymous' }
          : typeof nameOrAction === 'string'
            ? { type: nameOrAction }
            : nameOrAction
      if (store === undefined) {
        connection?.send(action, get())
        return r
      }
      connection?.send(
        {
          ...action,
          type: `${store}/${action.type}`,
        },
        {
          ...getTrackedConnectionState(options.name),
          [store]: api.getState(),
        },
      )
      return r
    }) as NamedSet<S>

    const setStateFromDevtools: StoreApi<S>['setState'] = (...a) => {
      const originalIsRecording = isRecording
      isRecording = false
      set(...(a as Parameters<typeof set>))
      isRecording = originalIsRecording
    }

    const initialState = fn(api.setState, get, api)
    if (connectionInformation.type === 'untracked') {
      connection?.init(initialState)
    } else {
      connectionInformation.stores[connectionInformation.store] = api
      connection?.init(
        Object.fromEntries(
          Object.entries(connectionInformation.stores).map(([key, store]) => [
            key,
            key === connectionInformation.store
              ? initialState
              : store.getState(),
          ]),
        ),
      )
    }

    if (
      (api as any).dispatchFromDevtools &&
      typeof (api as any).dispatch === 'function'
    ) {
      let didWarnAboutReservedActionType = false
      const originalDispatch = (api as any).dispatch
      ;(api as any).dispatch = (...a: any[]) => {
        if (
          import.meta.env?.MODE !== 'production' &&
          a[0].type === '__setState' &&
          !didWarnAboutReservedActionType
        ) {
          console.warn(
            '[zustand devtools middleware] "__setState" action type is reserved ' +
              'to set state from the devtools. Avoid using it.',
          )
          didWarnAboutReservedActionType = true
        }
        ;(originalDispatch as any)(...a)
      }
    }

    ;(
      connection as unknown as {
        // FIXME https://github.com/reduxjs/redux-devtools/issues/1097
        subscribe: (
          listener: (message: Message) => void,
        ) => (() => void) | undefined
      }
    ).subscribe((message: any) => {
      switch (message.type) {
        case 'ACTION':
          if (typeof message.payload !== 'string') {
            console.error(
              '[zustand devtools middleware] Unsupported action format',
            )
            return
          }
          return parseJsonThen<{ type: unknown; state?: PartialState }>(
            message.payload,
            (action) => {
              if (action.type === '__setState') {
                if (store === undefined) {
                  setStateFromDevtools(action.state as PartialState)
                  return
                }
                if (Object.keys(action.state as S).length !== 1) {
                  console.error(
                    `
                    [zustand devtools middleware] Unsupported __setState action format.
                    When using 'store' option in devtools(), the 'state' should have only one key, which is a value of 'store' that was passed in devtools(),
                    and value of this only key should be a state object. Example: { "type": "__setState", "state": { "abc123Store": { "foo": "bar" } } }
                    `,
                  )
                }
                const stateFromDevtools = (action.state as S)[store]
                if (
                  stateFromDevtools === undefined ||
                  stateFromDevtools === null
                ) {
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(stateFromDevtools)
                ) {
                  setStateFromDevtools(stateFromDevtools)
                }
                return
              }

              if (!(api as any).dispatchFromDevtools) return
              if (typeof (api as any).dispatch !== 'function') return
              ;(api as any).dispatch(action)
            },
          )

        case 'DISPATCH':
          switch (message.payload.type) {
            case 'RESET':
              setStateFromDevtools(initialState as S)
              if (store === undefined) {
                return connection?.init(api.getState())
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'COMMIT':
              if (store === undefined) {
                connection?.init(api.getState())
                return
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'ROLLBACK':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  connection?.init(api.getState())
                  return
                }
                setStateFromDevtools(state[store] as S)
                connection?.init(getTrackedConnectionState(options.name))
              })

            case 'JUMP_TO_STATE':
            case 'JUMP_TO_ACTION':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(state[store])
                ) {
                  setStateFromDevtools(state[store] as S)
                }
              })

            case 'IMPORT_STATE': {
              const { nextLiftedState } = message.payload
              const lastComputedState =
                nextLiftedState.computedStates.slice(-1)[0]?.state
              if (!lastComputedState) return
              if (store === undefined) {
                setStateFromDevtools(lastComputedState)
              } else {
                setStateFromDevtools(lastComputedState[store])
              }
              connection?.send(
                null as any, // FIXME no-any
                nextLiftedState,
              )
              return
            }

            case 'PAUSE_RECORDING':
              return (isRecording = !isRecording)
          }
          return
      }
    })

    return initialState
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(fn, devtoolsOptions = {}) =>
  (set, get, api) => {
    const { enabled, anonymousActionType, store, ...options } = devtoolsOptions

    type S = ReturnType<typeof fn> & {
      [store: string]: ReturnType<typeof fn>
    }
    type PartialState = Partial<S> | ((s: S) => Partial<S>)

    let extensionConnector:
      | (typeof window)['__REDUX_DEVTOOLS_EXTENSION__']
      | false
    try {
      extensionConnector =
        (enabled ?? import.meta.env?.MODE !== 'production') &&
        window.__REDUX_DEVTOOLS_EXTENSION__
    } catch {
      // ignored
    }

    if (!extensionConnector) {
      return fn(set, get, api)
    }

    const { connection, ...connectionInformation } =
      extractConnectionInformation(store, extensionConnector, options)

    let isRecording = true
    ;(api.setState as any) = ((state, replace, nameOrAction: Action) => {
      const r = set(state, replace as any)
      if (!isRecording) return r
      const action: { type: string } =
        nameOrAction === undefined
          ? { type: anonymousActionType || 'anonymous' }
          : typeof nameOrAction === 'string'
            ? { type: nameOrAction }
            : nameOrAction
      if (store === undefined) {
        connection?.send(action, get())
        return r
      }
      connection?.send(
        {
          ...action,
          type: `${store}/${action.type}`,
        },
        {
          ...getTrackedConnectionState(options.name),
          [store]: api.getState(),
        },
      )
      return r
    }) as NamedSet<S>

    const setStateFromDevtools: StoreApi<S>['setState'] = (...a) => {
      const originalIsRecording = isRecording
      isRecording = false
      set(...(a as Parameters<typeof set>))
      isRecording = originalIsRecording
    }

    const initialState = fn(api.setState, get, api)
    if (connectionInformation.type === 'untracked') {
      connection?.init(initialState)
    } else {
      connectionInformation.stores[connectionInformation.store] = api
      connection?.init(
        Object.fromEntries(
          Object.entries(connectionInformation.stores).map(([key, store]) => [
            key,
            key === connectionInformation.store
              ? initialState
              : store.getState(),
          ]),
        ),
      )
    }

    if (
      (api as any).dispatchFromDevtools &&
      typeof (api as any).dispatch === 'function'
    ) {
      let didWarnAboutReservedActionType = false
      const originalDispatch = (api as any).dispatch
      ;(api as any).dispatch = (...args: any[]) => {
        if (
          import.meta.env?.MODE !== 'production' &&
          args[0].type === '__setState' &&
          !didWarnAboutReservedActionType
        ) {
          console.warn(
            '[zustand devtools middleware] "__setState" action type is reserved ' +
              'to set state from the devtools. Avoid using it.',
          )
          didWarnAboutReservedActionType = true
        }
        ;(originalDispatch as any)(...args)
      }
    }

    ;(
      connection as unknown as {
        // FIXME https://github.com/reduxjs/redux-devtools/issues/1097
        subscribe: (
          listener: (message: Message) => void,
        ) => (() => void) | undefined
      }
    ).subscribe((message: any) => {
      switch (message.type) {
        case 'ACTION':
          if (typeof message.payload !== 'string') {
            console.error(
              '[zustand devtools middleware] Unsupported action format',
            )
            return
          }
          return parseJsonThen<{ type: unknown; state?: PartialState }>(
            message.payload,
            (action) => {
              if (action.type === '__setState') {
                if (store === undefined) {
                  setStateFromDevtools(action.state as PartialState)
                  return
                }
                if (Object.keys(action.state as S).length !== 1) {
                  console.error(
                    `
                    [zustand devtools middleware] Unsupported __setState action format.
                    When using 'store' option in devtools(), the 'state' should have only one key, which is a value of 'store' that was passed in devtools(),
                    and value of this only key should be a state object. Example: { "type": "__setState", "state": { "abc123Store": { "foo": "bar" } } }
                    `,
                  )
                }
                const stateFromDevtools = (action.state as S)[store]
                if (
                  stateFromDevtools === undefined ||
                  stateFromDevtools === null
                ) {
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(stateFromDevtools)
                ) {
                  setStateFromDevtools(stateFromDevtools)
                }
                return
              }

              if (!(api as any).dispatchFromDevtools) return
              if (typeof (api as any).dispatch !== 'function') return
              ;(api as any).dispatch(action)
            },
          )

        case 'DISPATCH':
          switch (message.payload.type) {
            case 'RESET':
              setStateFromDevtools(initialState as S)
              if (store === undefined) {
                return connection?.init(api.getState())
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'COMMIT':
              if (store === undefined) {
                connection?.init(api.getState())
                return
              }
              return connection?.init(getTrackedConnectionState(options.name))

            case 'ROLLBACK':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  connection?.init(api.getState())
                  return
                }
                setStateFromDevtools(state[store] as S)
                connection?.init(getTrackedConnectionState(options.name))
              })

            case 'JUMP_TO_STATE':
            case 'JUMP_TO_ACTION':
              return parseJsonThen<S>(message.state, (state) => {
                if (store === undefined) {
                  setStateFromDevtools(state)
                  return
                }
                if (
                  JSON.stringify(api.getState()) !==
                  JSON.stringify(state[store])
                ) {
                  setStateFromDevtools(state[store] as S)
                }
              })

            case 'IMPORT_STATE': {
              const { nextLiftedState } = message.payload
              const lastComputedState =
                nextLiftedState.computedStates.slice(-1)[0]?.state
              if (!lastComputedState) return
              if (store === undefined) {
                setStateFromDevtools(lastComputedState)
              } else {
                setStateFromDevtools(lastComputedState[store])
              }
              connection?.send(
                null as any, // FIXME no-any
                nextLiftedState,
              )
              return
            }

            case 'PAUSE_RECORDING':
              return (isRecording = !isRecording)
          }
          return
      }
    })

    return initialState
  }
```

### 🔹 函式: `parseJsonThen()`
- **變更前簽章 (Before)**: `parseJsonThen(stringified: string, f: (parsed: T) => void)` (L375~L386)
- **變更後簽章 (After)**: `parseJsonThen(stringified: string, fn: (parsed: T) => void)` (L375~L386)

#### ◀️ 變更前實作碼 (Before Implementation):
```
<T>(stringified: string, f: (parsed: T) => void) => {
  let parsed: T | undefined
  try {
    parsed = JSON.parse(stringified)
  } catch (e) {
    console.error(
      '[zustand devtools middleware] Could not parse the received json',
      e,
    )
  }
  if (parsed !== undefined) f(parsed as T)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
<T>(stringified: string, fn: (parsed: T) => void) => {
  let parsed: T | undefined
  try {
    parsed = JSON.parse(stringified)
  } catch (e) {
    console.error(
      '[zustand devtools middleware] Could not parse the received json',
      e,
    )
  }
  if (parsed !== undefined) fn(parsed as T)
}
```


#### 📄 檔案: `src/middleware/immer.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:6, E:3, A:0) ➔ After(N:6, E:3, A:0)
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

### 🔹 函式: `immerImpl()`
- **變更前簽章 (Before)**: `immerImpl(initializer)` (L73~L85)
- **變更後簽章 (After)**: `immerImpl(initializer)` (L73~L85)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(initializer) => (set, get, store) => {
  type T = ReturnType<typeof initializer>

  store.setState = (updater, replace, ...a) => {
    const nextState = (
      typeof updater === 'function' ? produce(updater as any) : updater
    ) as ((s: T) => T) | T | Partial<T>

    return set(nextState, replace as any, ...a)
  }

  return initializer(store.setState, get, store)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(initializer) => (set, get, store) => {
  type T = ReturnType<typeof initializer>

  store.setState = (updater, replace, ...args) => {
    const nextState = (
      typeof updater === 'function' ? produce(updater as any) : updater
    ) as ((s: T) => T) | T | Partial<T>

    return set(nextState, replace as any, ...args)
  }

  return initializer(store.setState, get, store)
}
```

### 🔹 函式: `setState()`
- **變更前簽章 (Before)**: `setState(updater, replace, ...a)` (L76~L82)
- **變更後簽章 (After)**: `setState(updater, replace, ...args)` (L76~L82)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(updater, replace, ...a) => {
    const nextState = (
      typeof updater === 'function' ? produce(updater as any) : updater
    ) as ((s: T) => T) | T | Partial<T>

    return set(nextState, replace as any, ...a)
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(updater, replace, ...args) => {
    const nextState = (
      typeof updater === 'function' ? produce(updater as any) : updater
    ) as ((s: T) => T) | T | Partial<T>

    return set(nextState, replace as any, ...args)
  }
```


#### 📄 檔案: `src/middleware/redux.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:5, E:1, A:0) ➔ After(N:5, E:1, A:0)
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

### 🔹 函式: `dispatch()`
- **變更前簽章 (Before)**: `dispatch(...a)` (L48~L48)
- **變更後簽章 (After)**: `dispatch(...args)` (L48~L48)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(...a) => (api as any).dispatch(...a)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(...args) => (api as any).dispatch(...args)
```

### 🔹 函式: `reduxImpl()`
- **變更前簽章 (Before)**: `reduxImpl(reducer, initial)` (L39~L49)
- **變更後簽章 (After)**: `reduxImpl(reducer, initial)` (L39~L49)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(reducer, initial) => (set, _get, api) => {
  type S = typeof initial
  type A = Parameters<typeof reducer>[1]
  ;(api as any).dispatch = (action: A) => {
    ;(set as NamedSet<S>)((state: S) => reducer(state, action), false, action)
    return action
  }
  ;(api as any).dispatchFromDevtools = true

  return { dispatch: (...a) => (api as any).dispatch(...a), ...initial }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(reducer, initial) => (set, _get, api) => {
  type S = typeof initial
  type A = Parameters<typeof reducer>[1]
  ;(api as any).dispatch = (action: A) => {
    ;(set as NamedSet<S>)((state: S) => reducer(state, action), false, action)
    return action
  }
  ;(api as any).dispatchFromDevtools = true

  return { dispatch: (...args) => (api as any).dispatch(...args), ...initial }
}
```


---

### 🔹 Commit #19: `8ced2719`
- **完整 Hash**: `8ced2719ac13bcb06574ef0609207b3ead55ca7e`
- **說明 (Ground Truth)**: refactor(middleware/combine.ts): change exported function to 'function declaration' (#3030)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/combine.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:1, E:0, A:0) ➔ After(N:1, E:0, A:0)
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

### 🔹 函式: `combine()`
- **變更前簽章 (Before)**: `combine(initialState, create)` (L16~L18)
- **變更後簽章 (After)**: `function combine<
  T extends object,
  U extends object,
  Mps extends [StoreMutatorIdentifier, unknown][] = [],
  Mcs extends [StoreMutatorIdentifier, unknown][] = [],
>(
  initialState: T,
  create: StateCreator<T, Mps, Mcs, U>,
): StateCreator<Write<T, U>, Mps, Mcs>` (L5~L15)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(initialState, create) =>
  (...a) =>
    Object.assign({}, initialState, (create as any)(...a))
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function combine<
  T extends object,
  U extends object,
  Mps extends [StoreMutatorIdentifier, unknown][] = [],
  Mcs extends [StoreMutatorIdentifier, unknown][] = [],
>(
  initialState: T,
  create: StateCreator<T, Mps, Mcs, U>,
): StateCreator<Write<T, U>, Mps, Mcs> {
  return (...a) => Object.assign({}, initialState, (create as any)(...a))
}
```


---

### 🔹 Commit #20: `9bae0692`
- **完整 Hash**: `9bae06922a361d525757cb277fba576caae05524`
- **說明 (Ground Truth)**: fix(persist): fix async migrate on persist middleware (#2877)
- **變更檔案數**: 1

#### 📄 檔案: `src/middleware/persist.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:34, E:21, A:0) ➔ After(N:34, E:21, A:0)
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
  - 💥 作用域阻隔: 函式 'setItem' 被深鎖在內部閉包 (scope:createJSONStorage@after/src/middleware/persist.ts:L31C8)，外部無法調用！
  - 💥 作用域阻隔: 函式 'hydrate' 被深鎖在內部閉包 (scope:arrow@after/src/middleware/persist.ts:L175C59)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `hydrate()`
- **變更前簽章 (Before)**: `hydrate()` (L238~L310)
- **變更後簽章 (After)**: `hydrate()` (L238~L311)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              return [
                true,
                options.migrate(
                  deserializedStorageValue.state,
                  deserializedStorageValue.version,
                ),
              ] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        postRehydrationCallback?.(undefined, e)
      })
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        postRehydrationCallback?.(undefined, e)
      })
  }
```

### 🔹 函式: `persistImpl()`
- **變更前簽章 (Before)**: `persistImpl(config, baseOptions)` (L175~L350)
- **變更後簽章 (After)**: `persistImpl(config, baseOptions)` (L175~L351)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(config, baseOptions) => (set, get, api) => {
  type S = ReturnType<typeof config>
  let options = {
    storage: createJSONStorage<S>(() => localStorage),
    partialize: (state: S) => state,
    version: 0,
    merge: (persistedState: unknown, currentState: S) => ({
      ...currentState,
      ...(persistedState as object),
    }),
    ...baseOptions,
  }

  let hasHydrated = false
  const hydrationListeners = new Set<PersistListener<S>>()
  const finishHydrationListeners = new Set<PersistListener<S>>()
  let storage = options.storage

  if (!storage) {
    return config(
      (...args) => {
        console.warn(
          `[zustand persist middleware] Unable to update item '${options.name}', the given storage is currently unavailable.`,
        )
        set(...(args as Parameters<typeof set>))
      },
      get,
      api,
    )
  }

  const setItem = () => {
    const state = options.partialize({ ...get() })
    return (storage as PersistStorage<S>).setItem(options.name, {
      state,
      version: options.version,
    })
  }

  const savedSetState = api.setState

  api.setState = (state, replace) => {
    savedSetState(state, replace as any)
    void setItem()
  }

  const configResult = config(
    (...args) => {
      set(...(args as Parameters<typeof set>))
      void setItem()
    },
    get,
    api,
  )

  api.getInitialState = () => configResult

  // a workaround to solve the issue of not storing rehydrated state in sync storage
  // the set(state) value would be later overridden with initial state by create()
  // to avoid this, we merge the state from localStorage into the initial state.
  let stateFromStorage: S | undefined

  // rehydrate initial state with existing stored state
  const hydrate = () => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              return [
                true,
                options.migrate(
                  deserializedStorageValue.state,
                  deserializedStorageValue.version,
                ),
              ] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        postRehydrationCallback?.(undefined, e)
      })
  }

  ;(api as StoreApi<S> & StorePersist<S, S>).persist = {
    setOptions: (newOptions) => {
      options = {
        ...options,
        ...newOptions,
      }

      if (newOptions.storage) {
        storage = newOptions.storage
      }
    },
    clearStorage: () => {
      storage?.removeItem(options.name)
    },
    getOptions: () => options,
    rehydrate: () => hydrate() as Promise<void>,
    hasHydrated: () => hasHydrated,
    onHydrate: (cb) => {
      hydrationListeners.add(cb)

      return () => {
        hydrationListeners.delete(cb)
      }
    },
    onFinishHydration: (cb) => {
      finishHydrationListeners.add(cb)

      return () => {
        finishHydrationListeners.delete(cb)
      }
    },
  }

  if (!options.skipHydration) {
    hydrate()
  }

  return stateFromStorage || configResult
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(config, baseOptions) => (set, get, api) => {
  type S = ReturnType<typeof config>
  let options = {
    storage: createJSONStorage<S>(() => localStorage),
    partialize: (state: S) => state,
    version: 0,
    merge: (persistedState: unknown, currentState: S) => ({
      ...currentState,
      ...(persistedState as object),
    }),
    ...baseOptions,
  }

  let hasHydrated = false
  const hydrationListeners = new Set<PersistListener<S>>()
  const finishHydrationListeners = new Set<PersistListener<S>>()
  let storage = options.storage

  if (!storage) {
    return config(
      (...args) => {
        console.warn(
          `[zustand persist middleware] Unable to update item '${options.name}', the given storage is currently unavailable.`,
        )
        set(...(args as Parameters<typeof set>))
      },
      get,
      api,
    )
  }

  const setItem = () => {
    const state = options.partialize({ ...get() })
    return (storage as PersistStorage<S>).setItem(options.name, {
      state,
      version: options.version,
    })
  }

  const savedSetState = api.setState

  api.setState = (state, replace) => {
    savedSetState(state, replace as any)
    void setItem()
  }

  const configResult = config(
    (...args) => {
      set(...(args as Parameters<typeof set>))
      void setItem()
    },
    get,
    api,
  )

  api.getInitialState = () => configResult

  // a workaround to solve the issue of not storing rehydrated state in sync storage
  // the set(state) value would be later overridden with initial state by create()
  // to avoid this, we merge the state from localStorage into the initial state.
  let stateFromStorage: S | undefined

  // rehydrate initial state with existing stored state
  const hydrate = () => {
    if (!storage) return

    // On the first invocation of 'hydrate', state will not yet be defined (this is
    // true for both the 'asynchronous' and 'synchronous' case). Pass 'configResult'
    // as a backup  to 'get()' so listeners and 'onRehydrateStorage' are called with
    // the latest available state.

    hasHydrated = false
    hydrationListeners.forEach((cb) => cb(get() ?? configResult))

    const postRehydrationCallback =
      options.onRehydrateStorage?.(get() ?? configResult) || undefined

    // bind is used to avoid `TypeError: Illegal invocation` error
    return toThenable(storage.getItem.bind(storage))(options.name)
      .then((deserializedStorageValue) => {
        if (deserializedStorageValue) {
          if (
            typeof deserializedStorageValue.version === 'number' &&
            deserializedStorageValue.version !== options.version
          ) {
            if (options.migrate) {
              const migration = options.migrate(
                deserializedStorageValue.state,
                deserializedStorageValue.version,
              )
              if (migration instanceof Promise) {
                return migration.then((result) => [true, result] as const)
              }
              return [true, migration] as const
            }
            console.error(
              `State loaded from storage couldn't be migrated since no migrate function was provided`,
            )
          } else {
            return [false, deserializedStorageValue.state] as const
          }
        }
        return [false, undefined] as const
      })
      .then((migrationResult) => {
        const [migrated, migratedState] = migrationResult
        stateFromStorage = options.merge(
          migratedState as S,
          get() ?? configResult,
        )

        set(stateFromStorage as S, true)
        if (migrated) {
          return setItem()
        }
      })
      .then(() => {
        // TODO: In the asynchronous case, it's possible that the state has changed
        // since it was set in the prior callback. As such, it would be better to
        // pass 'get()' to the 'postRehydrationCallback' to ensure the most up-to-date
        // state is used. However, this could be a breaking change, so this isn't being
        // done now.
        postRehydrationCallback?.(stateFromStorage, undefined)

        // It's possible that 'postRehydrationCallback' updated the state. To ensure
        // that isn't overwritten when returning 'stateFromStorage' below
        // (synchronous-case only), update 'stateFromStorage' to point to the latest
        // state. In the asynchronous case, 'stateFromStorage' isn't used after this
        // callback, so there's no harm in updating it to match the latest state.
        stateFromStorage = get()
        hasHydrated = true
        finishHydrationListeners.forEach((cb) => cb(stateFromStorage as S))
      })
      .catch((e: Error) => {
        postRehydrationCallback?.(undefined, e)
      })
  }

  ;(api as StoreApi<S> & StorePersist<S, S>).persist = {
    setOptions: (newOptions) => {
      options = {
        ...options,
        ...newOptions,
      }

      if (newOptions.storage) {
        storage = newOptions.storage
      }
    },
    clearStorage: () => {
      storage?.removeItem(options.name)
    },
    getOptions: () => options,
    rehydrate: () => hydrate() as Promise<void>,
    hasHydrated: () => hasHydrated,
    onHydrate: (cb) => {
      hydrationListeners.add(cb)

      return () => {
        hydrationListeners.delete(cb)
      }
    },
    onFinishHydration: (cb) => {
      finishHydrationListeners.add(cb)

      return () => {
        finishHydrationListeners.delete(cb)
      }
    },
  }

  if (!options.skipHydration) {
    hydrate()
  }

  return stateFromStorage || configResult
}
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/zustand show 3febf8c6d4f6670f886cc6b628b01a128d2888bd
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 3febf8c6d4f6670f886cc6b628b01a128d2888bd~1 --file test_repos/zustand/src/middleware/persist.ts
   ```
