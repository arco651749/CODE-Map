# 🔬 CODE-Map 基準審查獨立驗證報告: `nest`
> **技術生態**: `TypeScript (企業級 IoC / 裝飾器管線)`  
> **本地倉庫路徑**: `test_repos/nest`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 24 Files  
> **報告生成時間**: 2026-10-20 21:42:37  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `8` / `24` | `33.3%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `15` / `24` | `62.5%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `1` / `24` | `4.2%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`23` / `24`** | **`95.8%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `24` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `284ca7d5`
- **完整 Hash**: `284ca7d54f97ac87308cd3c5c1a669f4f8b3ecec`
- **說明 (Ground Truth)**: fix(microservices): send the record headers of nats as message headers (#18197)
- **變更檔案數**: 1

#### 📄 檔案: `packages/microservices/client/client-nats.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:25, E:10, A:0) ➔ After(N:26, E:13, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 3, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `isMsgHdrs` (FUNCTION_DEF)
  • + [新增呼叫邊] `isMsgHdrs` ──[CALLS [guarded]]──> `isObject (External/Unresolved)`
  • + [新增呼叫邊] `mergeHeaders` ──[CALLS [guard: (!requestHeaders && !this.options?.headers)]]──> `isMsgHdrs`
  • + [新增呼叫邊] `mergeHeaders` ──[CALLS [guard: (!requestHeaders && !this.options?.headers)]]──> `isObject (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `mergeHeaders()`
- **變更前簽章 (Before)**: `mergeHeaders(requestHeaders?: THeaders)` (L386~L400)
- **變更後簽章 (After)**: `mergeHeaders(requestHeaders?: THeaders)` (L390~L425)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected mergeHeaders<THeaders = any>(requestHeaders?: THeaders) {
    if (!requestHeaders && !this.options?.headers) {
      return undefined;
    }

    const headers = requestHeaders ?? natsPackage.headers();

    for (const [key, value] of Object.entries(this.options?.headers || {})) {
      if (!headers.has(key)) {
        headers.set(key, value);
      }
    }

    return headers;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected mergeHeaders<THeaders = any>(requestHeaders?: THeaders) {
    if (!requestHeaders && !this.options?.headers) {
      return undefined;
    }

    // nats.js encodes the headers of a publish with "MsgHdrs.encode()", so
    // anything that is not a "MsgHdrs" cannot be sent. "NatsRecordBuilder"
    // takes the headers of a record as they are given to it, and the packet
    // headers of "send()" are a plain object, so both are copied into a
    // "MsgHdrs" here rather than passed on.
    const headers = natsPackage.headers();

    // The packet headers win over the static ones, as they always did.
    if (isMsgHdrs(requestHeaders)) {
      // A "MsgHdrs" keeps its headers in a map that "Object.entries()" does
      // not expose.
      for (const key of requestHeaders.keys()) {
        for (const value of requestHeaders.values(key)) {
          // "set()" would keep only the last value of a multi-valued header
          headers.append(key, value);
        }
      }
    } else if (isObject(requestHeaders)) {
      for (const [key, value] of Object.entries(requestHeaders)) {
        headers.set(key, value as string);
      }
    }

    for (const [key, value] of Object.entries(this.options?.headers || {})) {
      if (!headers.has(key)) {
        headers.set(key, value);
      }
    }

    return headers;
  }
```


---

### 🔹 Commit #02: `2786cbeb`
- **完整 Hash**: `2786cbeb9394dd4900a440ea85c569e4a4dfa810`
- **說明 (Ground Truth)**: fix(core): resolve request-scoped forward refs for concurrent requests (#18200)
- **變更檔案數**: 2

#### 📄 檔案: `packages/core/injector/injector.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:80, E:31, A:0) ➔ After(N:83, E:31, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 1, -Edges: 1, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `constructor` (FUNCTION_DEF)
  • + [新增節點] `insertSettlementRef` (FUNCTION_DEF)
  • + [新增節點] `settlementSignal` (FUNCTION_DEF)
  • + [新增呼叫邊] `constructor` ──[CALLS [guard: (options?.instanceDecorator)]]──> `makeSafeInstanceDecorator (External/Unresolved)`
  • - [移除呼叫邊] `constructor` ──[CALLS]──> `makeSafeInstanceDecorator (External/Unresolved)`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'callback' 被深鎖在內部閉包 (scope:loadInstance@after/packages/core/injector/injector.ts:L183C3)，外部無法調用！ (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `applySettlementSignal()`
- **變更前簽章 (Before)**: `applySettlementSignal(
    instancePerContext: InstancePerContext<T>,
    host: InstanceWrapper<T>,
  )` (L372~L382)
- **變更後簽章 (After)**: `applySettlementSignal(
    instancePerContext: InstancePerContext<T>,
    host: InstanceWrapper<T>,
  )` (L387~L398)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public applySettlementSignal<T>(
    instancePerContext: InstancePerContext<T>,
    host: InstanceWrapper<T>,
  ) {
    const settlementSignal = new SettlementSignal();
    instancePerContext.donePromise = settlementSignal.asPromise();
    instancePerContext.isPending = true;
    host.settlementSignal = settlementSignal;

    return settlementSignal;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public applySettlementSignal<T>(
    instancePerContext: InstancePerContext<T>,
    host: InstanceWrapper<T>,
  ) {
    const settlementSignal = new SettlementSignal();
    instancePerContext.donePromise = settlementSignal.asPromise();
    instancePerContext.isPending = true;
    instancePerContext.settlementSignal = settlementSignal;
    host.settlementSignal = settlementSignal;

    return settlementSignal;
  }
```

### 🔹 函式: `loadInstance()`
- **變更前簽章 (Before)**: `loadInstance(
    wrapper: InstanceWrapper<T>,
    collection: Map<InjectionToken, InstanceWrapper>,
    moduleRef: Module,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  )` (L168~L267)
- **變更後簽章 (After)**: `loadInstance(
    wrapper: InstanceWrapper<T>,
    collection: Map<InjectionToken, InstanceWrapper>,
    moduleRef: Module,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  )` (L183~L282)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async loadInstance<T>(
    wrapper: InstanceWrapper<T>,
    collection: Map<InjectionToken, InstanceWrapper>,
    moduleRef: Module,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  ) {
    const inquirerId = this.getContextInquirerId(resolutionContext);
    const hostContextId = this.getContextId(
      resolutionContext.contextId,
      wrapper,
    );
    const instanceHost = this.getInstanceHost(
      wrapper,
      hostContextId,
      inquirerId,
    );

    if (instanceHost.isPending) {
      const settlementSignal = wrapper.settlementSignal;
      if (
        resolutionContext.inquirer &&
        settlementSignal?.isCycle(resolutionContext.inquirer.id)
      ) {
        throw new CircularDependencyException(`"${wrapper.name}"`);
      }

      return instanceHost.donePromise!.then((err?: unknown) => {
        if (err) {
          throw err;
        }
        if (this.failedInstances.has(instanceHost)) {
          throw this.failedInstances.get(instanceHost);
        }
        this.linkDurableDeferredLoads(
          wrapper,
          resolutionContext.contextId,
          hostContextId,
        );
      });
    }

    const settlementSignal = this.applySettlementSignal(instanceHost, wrapper);
    const token = wrapper.token || wrapper.name;

    const { inject } = wrapper;
    const targetWrapper = collection.get(token);
    if (isUndefined(targetWrapper)) {
      throw new RuntimeException();
    }
    if (instanceHost.isResolved) {
      return settlementSignal.complete();
    }
    try {
      const t0 = this.getNowTimestamp();
      const localResolutionContext = this.createResolutionContext(
        resolutionContext.contextId,
        wrapper,
        inquirerId,
      );
      const callback = async (instances: unknown[], depth = 0) => {
        const properties = await this.resolveProperties(
          wrapper,
          moduleRef,
          inject as InjectionToken[],
          localResolutionContext,
          resolutionContext.inquirer,
        );
        const instance = await this.instantiateClass(
          instances,
          wrapper,
          targetWrapper,
          wrapper.isTransient ? localResolutionContext : resolutionContext,
        );
        this.applyProperties(instance, properties);

        wrapper.hierarchyLevel = depth + 1;
        wrapper.initTime = this.getNowTimestamp() - t0;
        settlementSignal.complete();
      };
      await this.resolveConstructorParams<T>(
        wrapper,
        moduleRef,
        inject as InjectionToken[],
        callback,
        localResolutionContext,
        resolutionContext.inquirer,
      );
      if (!instanceHost.isResolved) {
        settlementSignal.complete();
      }
    } catch (err) {
      wrapper.removeInstanceByContextId(
        this.getContextId(resolutionContext.contextId, wrapper),
        inquirerId,
      );

      settlementSignal.error(err);
      throw err;
    }
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async loadInstance<T>(
    wrapper: InstanceWrapper<T>,
    collection: Map<InjectionToken, InstanceWrapper>,
    moduleRef: Module,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  ) {
    const inquirerId = this.getContextInquirerId(resolutionContext);
    const hostContextId = this.getContextId(
      resolutionContext.contextId,
      wrapper,
    );
    const instanceHost = this.getInstanceHost(
      wrapper,
      hostContextId,
      inquirerId,
    );

    if (instanceHost.isPending) {
      const settlementSignal = instanceHost.settlementSignal;
      if (
        resolutionContext.inquirer &&
        settlementSignal?.isCycle(resolutionContext.inquirer.id)
      ) {
        throw new CircularDependencyException(`"${wrapper.name}"`);
      }

      return instanceHost.donePromise!.then((err?: unknown) => {
        if (err) {
          throw err;
        }
        if (this.failedInstances.has(instanceHost)) {
          throw this.failedInstances.get(instanceHost);
        }
        this.linkDurableDeferredLoads(
          wrapper,
          resolutionContext.contextId,
          hostContextId,
        );
      });
    }

    const settlementSignal = this.applySettlementSignal(instanceHost, wrapper);
    const token = wrapper.token || wrapper.name;

    const { inject } = wrapper;
    const targetWrapper = collection.get(token);
    if (isUndefined(targetWrapper)) {
      throw new RuntimeException();
    }
    if (instanceHost.isResolved) {
      return settlementSignal.complete();
    }
    try {
      const t0 = this.getNowTimestamp();
      const localResolutionContext = this.createResolutionContext(
        resolutionContext.contextId,
        wrapper,
        inquirerId,
      );
      const callback = async (instances: unknown[], depth = 0) => {
        const properties = await this.resolveProperties(
          wrapper,
          moduleRef,
          inject as InjectionToken[],
          localResolutionContext,
          resolutionContext.inquirer,
        );
        const instance = await this.instantiateClass(
          instances,
          wrapper,
          targetWrapper,
          wrapper.isTransient ? localResolutionContext : resolutionContext,
        );
        this.applyProperties(instance, properties);

        wrapper.hierarchyLevel = depth + 1;
        wrapper.initTime = this.getNowTimestamp() - t0;
        settlementSignal.complete();
      };
      await this.resolveConstructorParams<T>(
        wrapper,
        moduleRef,
        inject as InjectionToken[],
        callback,
        localResolutionContext,
        resolutionContext.inquirer,
      );
      if (!instanceHost.isResolved) {
        settlementSignal.complete();
      }
    } catch (err) {
      wrapper.removeInstanceByContextId(
        this.getContextId(resolutionContext.contextId, wrapper),
        inquirerId,
      );

      settlementSignal.error(err);
      throw err;
    }
  }
```

### 🔹 函式: `constructor()`
- **變更前簽章 (Before)**: `constructor(
    private readonly options?: {
      /**
       * Whether to enable preview mode.
       */
      preview: boolean;
      /**
       * Whether to enable deterministic graph snapshot generation.
       */
      snapshot?: boolean;
      /**
       * Function to decorate a freshly created instance.
       */
      instanceDecorator?: (target: unknown) => unknown;
    },
  )` (L127~L148)
- **變更後簽章 (After)**: `constructor(
    public readonly id: string,
    private readonly host: InstancePerContext<unknown>,
  )` (L101~L104)

#### ◀️ 變更前實作碼 (Before Implementation):
```
constructor(
    private readonly options?: {
      /**
       * Whether to enable preview mode.
       */
      preview: boolean;
      /**
       * Whether to enable deterministic graph snapshot generation.
       */
      snapshot?: boolean;
      /**
       * Function to decorate a freshly created instance.
       */
      instanceDecorator?: (target: unknown) => unknown;
    },
  ) {
    if (options?.instanceDecorator) {
      this.instanceDecorator = makeSafeInstanceDecorator(
        options.instanceDecorator,
      );
    }
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
constructor(
    public readonly id: string,
    private readonly host: InstancePerContext<unknown>,
  ) {}
```

### 🔹 函式: `resolveComponentHost()`
- **變更前簽章 (Before)**: `resolveComponentHost(
    moduleRef: Module,
    instanceWrapper: InstanceWrapper<T | Promise<T>>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  )` (L666~L756)
- **變更後簽章 (After)**: `resolveComponentHost(
    moduleRef: Module,
    instanceWrapper: InstanceWrapper<T | Promise<T>>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  )` (L682~L778)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async resolveComponentHost<T>(
    moduleRef: Module,
    instanceWrapper: InstanceWrapper<T | Promise<T>>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  ): Promise<InstanceWrapper> {
    const inquirerId = this.getContextInquirerId(resolutionContext);
    const instanceHost = this.getInstanceHost(
      instanceWrapper,
      this.getContextId(resolutionContext.contextId, instanceWrapper),
      inquirerId,
    );
    if (!instanceHost.isResolved && !instanceWrapper.forwardRef) {
      resolutionContext.inquirer?.settlementSignal?.insertRef(instanceWrapper);

      await this.loadProvider(
        instanceWrapper,
        instanceWrapper.host ?? moduleRef,
        resolutionContext,
      );
    } else if (
      !instanceHost.isResolved &&
      instanceWrapper.forwardRef &&
      (resolutionContext.contextId !== STATIC_CONTEXT || !!inquirerId)
    ) {
      /**
       * When circular dependency has been detected between
       * either request/transient providers, we have to asynchronously
       * resolve instance host for a specific contextId or inquirer, to ensure
       * that eventual lazily created instance will be merged with the prototype
       * instantiated beforehand.
       */
      if (instanceHost.donePromise) {
        const deferredLoad = instanceHost.donePromise.then((err?: unknown) => {
          // The placeholder handed out belongs to the load that failed
          if (err) {
            throw err;
          }
          return this.loadProvider(
            instanceWrapper,
            instanceWrapper.host ?? moduleRef,
            resolutionContext,
          );
        });
        void deferredLoad.catch(err => {
          instanceWrapper.settlementSignal?.error(err);
        });
        this.addDeferredLoad(resolutionContext.contextId, deferredLoad);
        this.trackDurableDeferredLoad(
          instanceWrapper,
          resolutionContext.contextId,
          deferredLoad,
        );
      } else {
        /**
         * No load has ever been scheduled for this context (e.g., request-scoped
         * providers are no longer instantiated during static bootstrap, so a fresh
         * durable/request sub-tree host has no inherited `donePromise`).
         * Record the edge before loading it, so that if this load reaches the
         * inquirer while it is still pending, `isCycle()` sees the cycle and throws
         * instead of awaiting a `donePromise` that depends on itself.
         */
        resolutionContext.inquirer?.settlementSignal?.insertRef(
          instanceWrapper,
        );

        await this.loadProvider(
          instanceWrapper,
          instanceWrapper.host ?? moduleRef,
          resolutionContext,
        );
      }
    }
    if (instanceWrapper.async) {
      const host = instanceWrapper.getInstanceByContextId(
        this.getContextId(resolutionContext.contextId, instanceWrapper),
        inquirerId,
      );
      host.instance = await host.instance;
      instanceWrapper.setInstanceByContextId(
        resolutionContext.contextId,
        host,
        inquirerId,
      );
    }
    this.linkDurableDeferredLoads(
      instanceWrapper,
      resolutionContext.contextId,
      this.getContextId(resolutionContext.contextId, instanceWrapper),
    );
    return instanceWrapper;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async resolveComponentHost<T>(
    moduleRef: Module,
    instanceWrapper: InstanceWrapper<T | Promise<T>>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  ): Promise<InstanceWrapper> {
    const inquirerId = this.getContextInquirerId(resolutionContext);
    const instanceHost = this.getInstanceHost(
      instanceWrapper,
      this.getContextId(resolutionContext.contextId, instanceWrapper),
      inquirerId,
    );
    if (!instanceHost.isResolved && !instanceWrapper.forwardRef) {
      this.insertSettlementRef(
        resolutionContext,
        instanceWrapper,
        instanceHost,
      );

      await this.loadProvider(
        instanceWrapper,
        instanceWrapper.host ?? moduleRef,
        resolutionContext,
      );
    } else if (
      !instanceHost.isResolved &&
      instanceWrapper.forwardRef &&
      (resolutionContext.contextId !== STATIC_CONTEXT || !!inquirerId)
    ) {
      /**
       * When circular dependency has been detected between
       * either request/transient providers, we have to asynchronously
       * resolve instance host for a specific contextId or inquirer, to ensure
       * that eventual lazily created instance will be merged with the prototype
       * instantiated beforehand.
       */
      if (instanceHost.donePromise) {
        const deferredLoad = instanceHost.donePromise.then((err?: unknown) => {
          // The placeholder handed out belongs to the load that failed
          if (err) {
            throw err;
          }
          return this.loadProvider(
            instanceWrapper,
            instanceWrapper.host ?? moduleRef,
            resolutionContext,
          );
        });
        void deferredLoad.catch(err => {
          instanceHost.settlementSignal?.error(err);
        });
        this.addDeferredLoad(resolutionContext.contextId, deferredLoad);
        this.trackDurableDeferredLoad(
          instanceWrapper,
          resolutionContext.contextId,
          deferredLoad,
        );
      } else {
        /**
         * No load has ever been scheduled for this context (e.g., request-scoped
         * providers are no longer instantiated during static bootstrap, so a fresh
         * durable/request sub-tree host has no inherited `donePromise`).
         * Record the edge before loading it, so that if this load reaches the
         * inquirer while it is still pending, `isCycle()` sees the cycle and throws
         * instead of awaiting a `donePromise` that depends on itself.
         */
        this.insertSettlementRef(
          resolutionContext,
          instanceWrapper,
          instanceHost,
        );

        await this.loadProvider(
          instanceWrapper,
          instanceWrapper.host ?? moduleRef,
          resolutionContext,
        );
      }
    }
    if (instanceWrapper.async) {
      const host = instanceWrapper.getInstanceByContextId(
        this.getContextId(resolutionContext.contextId, instanceWrapper),
        inquirerId,
      );
      host.instance = await host.instance;
      instanceWrapper.setInstanceByContextId(
        resolutionContext.contextId,
        host,
        inquirerId,
      );
    }
    this.linkDurableDeferredLoads(
      instanceWrapper,
      resolutionContext.contextId,
      this.getContextId(resolutionContext.contextId, instanceWrapper),
    );
    return instanceWrapper;
  }
```


#### 📄 檔案: `packages/core/injector/instance-wrapper.ts`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:67, E:19, A:0) ➔ After(N:67, E:19, A:0)
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

### 🔹 Commit #03: `876a182c`
- **完整 Hash**: `876a182c60a10a034e8d8c46d0acfa7a47897d7a`
- **說明 (Ground Truth)**: fix(express): send the standard body for an exception wrapping an error (#18199)
- **變更檔案數**: 1

#### 📄 檔案: `packages/platform-express/adapters/express-adapter.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:69, E:33, A:0) ➔ After(N:69, E:33, A:0)
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

### 🔹 函式: `reply()`
- **變更前簽章 (Before)**: `reply(response: any, body: any, statusCode?: number)` (L165~L220)
- **變更後簽章 (After)**: `reply(response: any, body: any, statusCode?: number)` (L165~L231)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public reply(response: any, body: any, statusCode?: number) {
    if (!isNil(statusCode)) {
      response.status(statusCode);
    }
    if (isNil(body)) {
      return response.send();
    }
    if (body instanceof StreamableFile) {
      // A stream that failed before the reply (e.g. while an interceptor
      // awaited) has already emitted its 'error' event.
      const { errored } = body.getStream();
      if (errored) {
        return body.errorHandler(errored, response);
      }
      this.applyStreamHeaders(response, body);
      const stream = body.getStream();
      stream.once('error', err => {
        body.errorHandler(err, response);
      });
      // pipe() leaves the source open when the client disconnects early,
      // also before reply() runs ("close" has already fired by then)
      finished(response, () => {
        if (!stream.readableEnded) {
          stream.destroy();
        }
      });
      // Node discards the body of a HEAD response without ever applying
      // backpressure, so piping would read the whole source. The response
      // ends once the source is readable instead, which still leaves an
      // error opening it (e.g. a missing file) to the error handler.
      if (response.req?.method === 'HEAD') {
        stream.once('readable', () => response.end());
        return response.on('error', (err: Error) => body.errorLogger(err));
      }
      return stream
        .pipe<Writable>(response)
        .on('error', (err: Error) => body.errorLogger(err));
    }
    const responseContentType = response.getHeader('Content-Type');
    if (
      typeof responseContentType === 'string' &&
      !isJsonContentType(responseContentType) &&
      (body?.statusCode >= HttpStatus.BAD_REQUEST ||
        // A custom error body (e.g. "new HttpException({ ... }, 404)") need
        // not have a "statusCode" of its own
        (isObject(body) &&
          !isNil(statusCode) &&
          statusCode >= HttpStatus.BAD_REQUEST))
    ) {
      this.logger.warn(
        "Content-Type doesn't match Reply body, you might need a custom ExceptionFilter for non-JSON responses",
      );
      response.setHeader('Content-Type', 'application/json');
    }
    return isObject(body) ? response.json(body) : response.send(String(body));
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public reply(response: any, body: any, statusCode?: number) {
    if (!isNil(statusCode)) {
      response.status(statusCode);
    }
    if (isNil(body)) {
      return response.send();
    }
    if (body instanceof StreamableFile) {
      // A stream that failed before the reply (e.g. while an interceptor
      // awaited) has already emitted its 'error' event.
      const { errored } = body.getStream();
      if (errored) {
        return body.errorHandler(errored, response);
      }
      this.applyStreamHeaders(response, body);
      const stream = body.getStream();
      stream.once('error', err => {
        body.errorHandler(err, response);
      });
      // pipe() leaves the source open when the client disconnects early,
      // also before reply() runs ("close" has already fired by then)
      finished(response, () => {
        if (!stream.readableEnded) {
          stream.destroy();
        }
      });
      // Node discards the body of a HEAD response without ever applying
      // backpressure, so piping would read the whole source. The response
      // ends once the source is readable instead, which still leaves an
      // error opening it (e.g. a missing file) to the error handler.
      if (response.req?.method === 'HEAD') {
        stream.once('readable', () => response.end());
        return response.on('error', (err: Error) => body.errorLogger(err));
      }
      return stream
        .pipe<Writable>(response)
        .on('error', (err: Error) => body.errorLogger(err));
    }
    // response.json() serializes the enumerable properties of an Error, e.g.
    // the request config of an HTTP client error.
    if (
      body instanceof Error &&
      response.statusCode >= HttpStatus.BAD_REQUEST
    ) {
      body = {
        statusCode: response.statusCode,
        message: http.STATUS_CODES[response.statusCode] ?? 'Error',
      };
    }
    const responseContentType = response.getHeader('Content-Type');
    if (
      typeof responseContentType === 'string' &&
      !isJsonContentType(responseContentType) &&
      (body?.statusCode >= HttpStatus.BAD_REQUEST ||
        // A custom error body (e.g. "new HttpException({ ... }, 404)") need
        // not have a "statusCode" of its own
        (isObject(body) &&
          !isNil(statusCode) &&
          statusCode >= HttpStatus.BAD_REQUEST))
    ) {
      this.logger.warn(
        "Content-Type doesn't match Reply body, you might need a custom ExceptionFilter for non-JSON responses",
      );
      response.setHeader('Content-Type', 'application/json');
    }
    return isObject(body) ? response.json(body) : response.send(String(body));
  }
```


---

### 🔹 Commit #04: `614d1ac7`
- **完整 Hash**: `614d1ac7eacef022da050adba2408810a8a1b408`
- **說明 (Ground Truth)**: fix(fastify): send the status of an exception whose body is an error
- **變更檔案數**: 1

#### 📄 檔案: `packages/platform-fastify/adapters/fastify-adapter.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:119, E:39, A:0) ➔ After(N:119, E:39, A:0)
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

### 🔹 函式: `reply()`
- **變更前簽章 (Before)**: `reply(
    response: TRawResponse | TReply,
    body: any,
    statusCode?: number,
  )` (L689~L766)
- **變更後簽章 (After)**: `reply(
    response: TRawResponse | TReply,
    body: any,
    statusCode?: number,
  )` (L689~L780)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public reply(
    response: TRawResponse | TReply,
    body: any,
    statusCode?: number,
  ) {
    const fastifyReply: TReply = this.isNativeResponse(response)
      ? new Reply(
          response,
          {
            [kRouteContext]: {
              preSerialization: null,
              preValidation: [],
              preHandler: [],
              onSend: [],
              onError: [],
            },
          },
          {},
        )
      : response;

    if (!isNil(statusCode)) {
      fastifyReply.status(statusCode);
    }
    if (body instanceof StreamableFile) {
      const stream = body.getStream();
      // Once the reply was sent (e.g. by `handlerTimeout`), send() drops the
      // stream without consuming or destroying it.
      if (fastifyReply.sent && isFunction(stream?.destroy)) {
        stream.destroy();
      }
      const streamHeaders = body.getHeaders();
      if (
        fastifyReply.getHeader('Content-Type') === undefined &&
        streamHeaders.type !== undefined
      ) {
        fastifyReply.header('Content-Type', streamHeaders.type);
      }
      if (
        fastifyReply.getHeader('Content-Disposition') === undefined &&
        streamHeaders.disposition !== undefined
      ) {
        fastifyReply.header('Content-Disposition', streamHeaders.disposition);
      }
      if (
        fastifyReply.getHeader('Content-Length') === undefined &&
        streamHeaders.length !== undefined
      ) {
        fastifyReply.header('Content-Length', streamHeaders.length);
      }
      body = stream;
      // Fastify's HEAD route handler resumes a stream payload, and a route
      // declared for HEAD (or a raw response) pipes it into a response that
      // discards it, so the whole source would be read for nothing. Fastify
      // gets an empty stream instead, as an empty body would reset
      // Content-Length to 0.
      if (
        fastifyReply.raw?.req?.method === 'HEAD' &&
        isFunction(stream?.destroy)
      ) {
        stream.destroy();
        body = Readable.from([]);
      }
    }
    const responseContentType = fastifyReply.getHeader('Content-Type');
    if (
      typeof responseContentType === 'string' &&
      !isJsonContentType(responseContentType) &&
      body?.statusCode >= HttpStatus.BAD_REQUEST
    ) {
      Logger.warn(
        "Content-Type doesn't match Reply body, you might need a custom ExceptionFilter for non-JSON responses",
        FastifyAdapter.name,
      );
      fastifyReply.header('Content-Type', 'application/json');
    }
    return fastifyReply.send(body);
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public reply(
    response: TRawResponse | TReply,
    body: any,
    statusCode?: number,
  ) {
    const fastifyReply: TReply = this.isNativeResponse(response)
      ? new Reply(
          response,
          {
            [kRouteContext]: {
              preSerialization: null,
              preValidation: [],
              preHandler: [],
              onSend: [],
              onError: [],
            },
          },
          {},
        )
      : response;

    if (!isNil(statusCode)) {
      fastifyReply.status(statusCode);
    }
    if (body instanceof StreamableFile) {
      const stream = body.getStream();
      // Once the reply was sent (e.g. by `handlerTimeout`), send() drops the
      // stream without consuming or destroying it.
      if (fastifyReply.sent && isFunction(stream?.destroy)) {
        stream.destroy();
      }
      const streamHeaders = body.getHeaders();
      if (
        fastifyReply.getHeader('Content-Type') === undefined &&
        streamHeaders.type !== undefined
      ) {
        fastifyReply.header('Content-Type', streamHeaders.type);
      }
      if (
        fastifyReply.getHeader('Content-Disposition') === undefined &&
        streamHeaders.disposition !== undefined
      ) {
        fastifyReply.header('Content-Disposition', streamHeaders.disposition);
      }
      if (
        fastifyReply.getHeader('Content-Length') === undefined &&
        streamHeaders.length !== undefined
      ) {
        fastifyReply.header('Content-Length', streamHeaders.length);
      }
      body = stream;
      // Fastify's HEAD route handler resumes a stream payload, and a route
      // declared for HEAD (or a raw response) pipes it into a response that
      // discards it, so the whole source would be read for nothing. Fastify
      // gets an empty stream instead, as an empty body would reset
      // Content-Length to 0.
      if (
        fastifyReply.raw?.req?.method === 'HEAD' &&
        isFunction(stream?.destroy)
      ) {
        stream.destroy();
        body = Readable.from([]);
      }
    }
    // Fastify passes an Error payload to the error handler instead of
    // sending it, and the reply around a raw response (e.g. the one
    // middleware gets) has none. An Error body sent with an error status,
    // as for `new UnauthorizedException(err)`, gets the standard body of the
    // status instead, without the properties of the Error.
    if (
      body instanceof Error &&
      fastifyReply.statusCode >= HttpStatus.BAD_REQUEST
    ) {
      body = {
        statusCode: fastifyReply.statusCode,
        message: http.STATUS_CODES[fastifyReply.statusCode] ?? 'Error',
      };
    }
    const responseContentType = fastifyReply.getHeader('Content-Type');
    if (
      typeof responseContentType === 'string' &&
      !isJsonContentType(responseContentType) &&
      body?.statusCode >= HttpStatus.BAD_REQUEST
    ) {
      Logger.warn(
        "Content-Type doesn't match Reply body, you might need a custom ExceptionFilter for non-JSON responses",
        FastifyAdapter.name,
      );
      fastifyReply.header('Content-Type', 'application/json');
    }
    return fastifyReply.send(body);
  }
```


---

### 🔹 Commit #05: `ecc5b26d`
- **完整 Hash**: `ecc5b26d43732504449f0fdb23ab4a7c846695bb`
- **說明 (Ground Truth)**: fix(microservices): handle malformed kafka reply assigner metadata (#18182)
- **變更檔案數**: 1

#### 📄 檔案: `packages/microservices/helpers/kafka-reply-partition-assigner.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:15, E:3, A:0) ➔ After(N:16, E:3, A:0)
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
  • + [新增節點] `decodePreviousAssignment` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `assign()`
- **變更前簽章 (Before)**: `assign(group: {
    members: GroupMember[];
    topics: string[];
  })` (L38~L162)
- **變更後簽章 (After)**: `assign(group: {
    members: GroupMember[];
    topics: string[];
  })` (L38~L162)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async assign(group: {
    members: GroupMember[];
    topics: string[];
  }): Promise<GroupMemberAssignment[]> {
    kafkaPackage = await kafkaPackage;
    const assignment = {};
    const previousAssignment = {};

    const membersCount = group.members.length;
    const decodedMembers = group.members.map(member =>
      this.decodeMember(member),
    );
    const sortedMemberIds = decodedMembers
      .map(member => member.memberId)
      .sort();

    // build the previous assignment and an inverse map of topic > partition > memberId for lookup
    decodedMembers.forEach(member => {
      if (
        !previousAssignment[member.memberId] &&
        Object.keys(member.previousAssignment).length > 0
      ) {
        previousAssignment[member.memberId] = member.previousAssignment;
      }
    });

    // build a collection of topics and partitions
    const topicsPartitions = group.topics.flatMap(topic => {
      const partitionMetadata =
        this.config.cluster.findTopicPartitionMetadata(topic);
      return partitionMetadata.map(m => ({
        topic,
        partitionId: m.partitionId,
      }));
    });

    // create the new assignment by populating the members with the first partition of the topics
    sortedMemberIds.forEach(assignee => {
      if (!assignment[assignee]) {
        assignment[assignee] = {};
      }

      // add topics to each member
      group.topics.forEach(topic => {
        if (!assignment[assignee][topic]) {
          assignment[assignee][topic] = [];
        }

        // see if the topic and partition belong to a previous assignment
        if (
          previousAssignment[assignee] &&
          !isUndefined(previousAssignment[assignee][topic])
        ) {
          // take the minimum partition since replies will be sent to the minimum partition
          const firstPartition = previousAssignment[assignee][topic];

          // create the assignment with the first partition
          assignment[assignee][topic].push(firstPartition);

          // find and remove this topic and partition from the topicPartitions to be assigned later
          const topicsPartitionsIndex = topicsPartitions.findIndex(
            topicPartition => {
              return (
                topicPartition.topic === topic &&
                topicPartition.partitionId === firstPartition
              );
            },
          );

          // only continue if we found a partition matching this topic
          if (topicsPartitionsIndex !== -1) {
            // remove inline
            topicsPartitions.splice(topicsPartitionsIndex, 1);
          }
        }
      });
    });

    // check for member topics that have a partition length of 0
    sortedMemberIds.forEach(assignee => {
      group.topics.forEach(topic => {
        // only continue if there are no partitions for assignee's topic
        if (assignment[assignee][topic].length === 0) {
          // find the first partition for this topic
          const topicsPartitionsIndex = topicsPartitions.findIndex(
            topicPartition => {
              return topicPartition.topic === topic;
            },
          );

          if (topicsPartitionsIndex !== -1) {
            // find and set the topic partition
            const partition =
              topicsPartitions[topicsPartitionsIndex].partitionId;

            assignment[assignee][topic].push(partition);

            // remove this partition from the topics partitions collection
            topicsPartitions.splice(topicsPartitionsIndex, 1);
          }
        }
      });
    });

    // then balance out the rest of the topic partitions across the members
    const insertAssignmentsByTopic = (topicPartition, i) => {
      const assignee = sortedMemberIds[i % membersCount];

      assignment[assignee][topicPartition.topic].push(
        topicPartition.partitionId,
      );
    };

    // build the assignments
    topicsPartitions.forEach(insertAssignmentsByTopic);

    // encode the end result
    return Object.keys(assignment).map(memberId => ({
      memberId,
      memberAssignment: kafkaPackage.AssignerProtocol.MemberAssignment.encode({
        version: this.version,
        assignment: assignment[memberId],
      }),
    }));
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async assign(group: {
    members: GroupMember[];
    topics: string[];
  }): Promise<GroupMemberAssignment[]> {
    kafkaPackage = await kafkaPackage;
    const assignment = {};
    const previousAssignment = {};

    const membersCount = group.members.length;
    const decodedMembers = group.members.map(member =>
      this.decodeMember(member),
    );
    const sortedMemberIds = decodedMembers
      .map(member => member.memberId)
      .sort();

    // build the previous assignment and an inverse map of topic > partition > memberId for lookup
    decodedMembers.forEach(member => {
      if (
        !previousAssignment[member.memberId] &&
        Object.keys(member.previousAssignment).length > 0
      ) {
        previousAssignment[member.memberId] = member.previousAssignment;
      }
    });

    // build a collection of topics and partitions
    const topicsPartitions = group.topics.flatMap(topic => {
      const partitionMetadata =
        this.config.cluster.findTopicPartitionMetadata(topic);
      return partitionMetadata.map(m => ({
        topic,
        partitionId: m.partitionId,
      }));
    });

    // create the new assignment by populating the members with the first partition of the topics
    sortedMemberIds.forEach(assignee => {
      if (!assignment[assignee]) {
        assignment[assignee] = {};
      }

      // add topics to each member
      group.topics.forEach(topic => {
        if (!assignment[assignee][topic]) {
          assignment[assignee][topic] = [];
        }

        // see if the topic and partition belong to a previous assignment
        if (
          previousAssignment[assignee] &&
          !isUndefined(previousAssignment[assignee][topic])
        ) {
          // take the minimum partition since replies will be sent to the minimum partition
          const firstPartition = previousAssignment[assignee][topic];

          // find and remove this topic and partition from the topicPartitions to be assigned later
          const topicsPartitionsIndex = topicsPartitions.findIndex(
            topicPartition => {
              return (
                topicPartition.topic === topic &&
                topicPartition.partitionId === firstPartition
              );
            },
          );

          // only keep a partition that exists and is not taken yet, otherwise
          // the member gets a free partition below
          if (topicsPartitionsIndex !== -1) {
            // create the assignment with the first partition
            assignment[assignee][topic].push(firstPartition);
            // remove inline
            topicsPartitions.splice(topicsPartitionsIndex, 1);
          }
        }
      });
    });

    // check for member topics that have a partition length of 0
    sortedMemberIds.forEach(assignee => {
      group.topics.forEach(topic => {
        // only continue if there are no partitions for assignee's topic
        if (assignment[assignee][topic].length === 0) {
          // find the first partition for this topic
          const topicsPartitionsIndex = topicsPartitions.findIndex(
            topicPartition => {
              return topicPartition.topic === topic;
            },
          );

          if (topicsPartitionsIndex !== -1) {
            // find and set the topic partition
            const partition =
              topicsPartitions[topicsPartitionsIndex].partitionId;

            assignment[assignee][topic].push(partition);

            // remove this partition from the topics partitions collection
            topicsPartitions.splice(topicsPartitionsIndex, 1);
          }
        }
      });
    });

    // then balance out the rest of the topic partitions across the members
    const insertAssignmentsByTopic = (topicPartition, i) => {
      const assignee = sortedMemberIds[i % membersCount];

      assignment[assignee][topicPartition.topic].push(
        topicPartition.partitionId,
      );
    };

    // build the assignments
    topicsPartitions.forEach(insertAssignmentsByTopic);

    // encode the end result
    return Object.keys(assignment).map(memberId => ({
      memberId,
      memberAssignment: kafkaPackage.AssignerProtocol.MemberAssignment.encode({
        version: this.version,
        assignment: assignment[memberId],
      }),
    }));
  }
```

### 🔹 函式: `decodeMember()`
- **變更前簽章 (Before)**: `decodeMember(member: GroupMember)` (L187~L199)
- **變更後簽章 (After)**: `decodeMember(member: GroupMember)` (L187~L205)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public decodeMember(member: GroupMember) {
    // kafkaPackage must be resolved before calling this method
    // (it is resolved in assign() which calls decodeMember)
    const memberMetadata = kafkaPackage.AssignerProtocol.MemberMetadata.decode(
      member.memberMetadata,
    ) as MemberMetadata;
    const memberUserData = JSON.parse(memberMetadata.userData.toString());

    return {
      memberId: member.memberId,
      previousAssignment: memberUserData.previousAssignment,
    };
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public decodeMember(member: GroupMember) {
    // kafkaPackage must be resolved before calling this method
    // (it is resolved in assign() which calls decodeMember)
    let memberMetadata: MemberMetadata;
    try {
      memberMetadata = kafkaPackage.AssignerProtocol.MemberMetadata.decode(
        member.memberMetadata,
      ) as MemberMetadata;
    } catch {
      return { memberId: member.memberId, previousAssignment: {} };
    }

    return {
      memberId: member.memberId,
      previousAssignment: this.decodePreviousAssignment(
        memberMetadata.userData,
      ),
    };
  }
```


---

### 🔹 Commit #06: `83a55aa9`
- **完整 Hash**: `83a55aa9dc55e861d4b14d9b2e4abb18f20a8571`
- **說明 (Ground Truth)**: fix(microservices): leave the init hooks to the hybrid application
- **變更檔案數**: 1

#### 📄 檔案: `packages/microservices/nest-microservice.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:32, E:5, A:0) ➔ After(N:32, E:5, A:0)
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

### 🔹 函式: `registerModules()`
- **變更前簽章 (Before)**: `registerModules()` (L119~L144)
- **變更後簽章 (After)**: `registerModules()` (L119~L149)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async registerModules(): Promise<any> {
    // A hybrid application binds the gateways itself, to its HTTP server and
    // with its own global enhancers
    if (!this.isConnectedToApplication) {
      await this.loadSocketModule();
      this.socketModule &&
        (await this.socketModule.register(
          this.container,
          this.applicationConfig,
          this.graphInspector,
          this.appOptions,
        ));
    }

    if (!this.appOptions.preview) {
      this.microservicesModule.setupClients(this.container);
      this.registerListeners();
    }

    this.setIsInitialized(true);

    if (!this.wasInitHookCalled) {
      await this.callInitHook();
      await this.callBootstrapHook();
    }
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async registerModules(): Promise<any> {
    if (this.isConnectedToApplication) {
      // The hybrid application sets up the container it shares with the
      // microservice itself: it binds the gateways, to its HTTP server and
      // with its own global enhancers, assigns the clients and calls the
      // lifecycle hooks
      !this.appOptions.preview && this.registerListeners();
      this.setIsInitialized(true);
      return;
    }
    await this.loadSocketModule();
    this.socketModule &&
      (await this.socketModule.register(
        this.container,
        this.applicationConfig,
        this.graphInspector,
        this.appOptions,
      ));

    if (!this.appOptions.preview) {
      this.microservicesModule.setupClients(this.container);
      this.registerListeners();
    }

    this.setIsInitialized(true);

    if (!this.wasInitHookCalled) {
      await this.callInitHook();
      await this.callBootstrapHook();
    }
  }
```


---

### 🔹 Commit #07: `ffd27afe`
- **完整 Hash**: `ffd27afe100cae0a37c381ae0fcc2a8b3e63d7a7`
- **說明 (Ground Truth)**: fix(microservices): call the init hooks once when init() is called
- **變更檔案數**: 1

#### 📄 檔案: `packages/microservices/nest-microservice.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:32, E:5, A:0) ➔ After(N:32, E:5, A:0)
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

### 🔹 函式: `init()`
- **變更前簽章 (Before)**: `init()` (L278~L292)
- **變更後簽章 (After)**: `init()` (L278~L293)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async init(): Promise<this> {
    if (this.isInitialized) {
      return this;
    }

    try {
      // Lazy-load optional socket module (ESM-compatible)
      await this.loadSocketModule();
      await super.init();
      await this.registerModules();
    } finally {
      this.flushLogsIfAutoFlushEnabled();
    }
    return this;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async init(): Promise<this> {
    if (this.isInitialized) {
      return this;
    }

    try {
      // Lazy-load optional socket module (ESM-compatible)
      await this.loadSocketModule();
      // Calls the init hooks as well, as on "listen()", once the gateways,
      // clients and listeners are set up
      await this.registerModules();
    } finally {
      this.flushLogsIfAutoFlushEnabled();
    }
    return this;
  }
```


---

### 🔹 Commit #08: `85d0a0be`
- **完整 Hash**: `85d0a0be92baff22998d17c61cbfeb462970200f`
- **說明 (Ground Truth)**: fix(core): run interceptor, pipe and filter classes without a name
- **變更檔案數**: 3

#### 📄 檔案: `packages/core/exceptions/base-exception-filter-context.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:8, E:3, A:0) ➔ After(N:8, E:3, A:0)
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

### 🔹 函式: `createConcreteContext()`
- **變更前簽章 (Before)**: `createConcreteContext(
    metadata: T,
    contextId = STATIC_CONTEXT,
    inquirerId?: string,
  )` (L20~L39)
- **變更後簽章 (After)**: `createConcreteContext(
    metadata: T,
    contextId = STATIC_CONTEXT,
    inquirerId?: string,
  )` (L20~L40)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public createConcreteContext<T extends any[], R extends any[]>(
    metadata: T,
    contextId = STATIC_CONTEXT,
    inquirerId?: string,
  ): R {
    if (isEmpty(metadata)) {
      return [] as any[] as R;
    }
    return iterate(metadata)
      .filter(
        instance => instance && (isFunction(instance.catch) || instance.name),
      )
      .map(filter => this.getFilterInstance(filter, contextId, inquirerId))
      .filter(item => !!item)
      .map(instance => ({
        func: instance!.catch.bind(instance),
        exceptionMetatypes: this.reflectCatchExceptions(instance!),
      }))
      .toArray() as R;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public createConcreteContext<T extends any[], R extends any[]>(
    metadata: T,
    contextId = STATIC_CONTEXT,
    inquirerId?: string,
  ): R {
    if (isEmpty(metadata)) {
      return [] as any[] as R;
    }
    return iterate(metadata)
      .filter(
        instance =>
          instance && (isFunction(instance.catch) || isFunction(instance)),
      )
      .map(filter => this.getFilterInstance(filter, contextId, inquirerId))
      .filter(item => !!item)
      .map(instance => ({
        func: instance!.catch.bind(instance),
        exceptionMetatypes: this.reflectCatchExceptions(instance!),
      }))
      .toArray() as R;
  }
```


#### 📄 檔案: `packages/core/interceptors/interceptors-context-creator.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:9, E:4, A:0) ➔ After(N:9, E:4, A:0)
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

### 🔹 函式: `createConcreteContext()`
- **變更前簽章 (Before)**: `createConcreteContext(
    metadata: T,
    contextId = STATIC_CONTEXT,
    inquirerId?: string,
  )` (L42~L63)
- **變更後簽章 (After)**: `createConcreteContext(
    metadata: T,
    contextId = STATIC_CONTEXT,
    inquirerId?: string,
  )` (L42~L63)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public createConcreteContext<T extends any[], R extends any[]>(
    metadata: T,
    contextId = STATIC_CONTEXT,
    inquirerId?: string,
  ): R {
    if (isEmpty(metadata)) {
      return [] as any[] as R;
    }
    return iterate(metadata)
      .filter(
        interceptor =>
          interceptor && (interceptor.name || interceptor.intercept),
      )
      .map(
        interceptor =>
          this.getInterceptorInstance(interceptor, contextId, inquirerId)!,
      )
      .filter((interceptor: NestInterceptor) =>
        interceptor ? isFunction(interceptor.intercept) : false,
      )
      .toArray() as R;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public createConcreteContext<T extends any[], R extends any[]>(
    metadata: T,
    contextId = STATIC_CONTEXT,
    inquirerId?: string,
  ): R {
    if (isEmpty(metadata)) {
      return [] as any[] as R;
    }
    return iterate(metadata)
      .filter(
        interceptor =>
          interceptor &&
          (isFunction(interceptor) || isFunction(interceptor.intercept)),
      )
      .map(interceptor =>
        this.getInterceptorInstance(interceptor, contextId, inquirerId)!,
      )
      .filter((interceptor: NestInterceptor) =>
        interceptor ? isFunction(interceptor.intercept) : false,
      )
      .toArray() as R;
  }
```


#### 📄 檔案: `packages/core/pipes/pipes-context-creator.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:10, E:4, A:0) ➔ After(N:10, E:4, A:0)
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

### 🔹 函式: `createConcreteContext()`
- **變更前簽章 (Before)**: `createConcreteContext(
    metadata: T,
    contextId = STATIC_CONTEXT,
    inquirerId?: string,
  )` (L42~L55)
- **變更後簽章 (After)**: `createConcreteContext(
    metadata: T,
    contextId = STATIC_CONTEXT,
    inquirerId?: string,
  )` (L42~L57)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public createConcreteContext<T extends any[], R extends any[]>(
    metadata: T,
    contextId = STATIC_CONTEXT,
    inquirerId?: string,
  ): R {
    if (isEmpty(metadata)) {
      return [] as any[] as R;
    }
    return iterate(metadata)
      .filter((pipe: any) => pipe && (pipe.name || pipe.transform))
      .map(pipe => this.getPipeInstance(pipe, contextId, inquirerId))
      .filter(pipe => !!pipe && pipe.transform && isFunction(pipe.transform))
      .toArray() as R;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public createConcreteContext<T extends any[], R extends any[]>(
    metadata: T,
    contextId = STATIC_CONTEXT,
    inquirerId?: string,
  ): R {
    if (isEmpty(metadata)) {
      return [] as any[] as R;
    }
    return iterate(metadata)
      .filter(
        (pipe: any) => pipe && (isFunction(pipe) || isFunction(pipe.transform)),
      )
      .map(pipe => this.getPipeInstance(pipe, contextId, inquirerId))
      .filter(pipe => !!pipe && pipe.transform && isFunction(pipe.transform))
      .toArray() as R;
  }
```


---

### 🔹 Commit #09: `8a53d08b`
- **完整 Hash**: `8a53d08bee6a633667736dc2018a6bafe931845f`
- **說明 (Ground Truth)**: fix(core): detect cycles in request-scoped forward references (#18186)
- **變更檔案數**: 1

#### 📄 檔案: `packages/core/injector/injector.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:80, E:31, A:0) ➔ After(N:80, E:31, A:0)
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
  - 💥 作用域阻隔: 函式 'callback' 被深鎖在內部閉包 (scope:loadInstance@after/packages/core/injector/injector.ts:L168C3)，外部無法調用！ (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `resolveComponentHost()`
- **變更前簽章 (Before)**: `resolveComponentHost(
    moduleRef: Module,
    instanceWrapper: InstanceWrapper<T | Promise<T>>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  )` (L666~L751)
- **變更後簽章 (After)**: `resolveComponentHost(
    moduleRef: Module,
    instanceWrapper: InstanceWrapper<T | Promise<T>>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  )` (L666~L756)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async resolveComponentHost<T>(
    moduleRef: Module,
    instanceWrapper: InstanceWrapper<T | Promise<T>>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  ): Promise<InstanceWrapper> {
    const inquirerId = this.getContextInquirerId(resolutionContext);
    const instanceHost = this.getInstanceHost(
      instanceWrapper,
      this.getContextId(resolutionContext.contextId, instanceWrapper),
      inquirerId,
    );
    if (!instanceHost.isResolved && !instanceWrapper.forwardRef) {
      resolutionContext.inquirer?.settlementSignal?.insertRef(instanceWrapper);

      await this.loadProvider(
        instanceWrapper,
        instanceWrapper.host ?? moduleRef,
        resolutionContext,
      );
    } else if (
      !instanceHost.isResolved &&
      instanceWrapper.forwardRef &&
      (resolutionContext.contextId !== STATIC_CONTEXT || !!inquirerId)
    ) {
      /**
       * When circular dependency has been detected between
       * either request/transient providers, we have to asynchronously
       * resolve instance host for a specific contextId or inquirer, to ensure
       * that eventual lazily created instance will be merged with the prototype
       * instantiated beforehand.
       */
      if (instanceHost.donePromise) {
        const deferredLoad = instanceHost.donePromise.then((err?: unknown) => {
          // The placeholder handed out belongs to the load that failed
          if (err) {
            throw err;
          }
          return this.loadProvider(
            instanceWrapper,
            instanceWrapper.host ?? moduleRef,
            resolutionContext,
          );
        });
        void deferredLoad.catch(err => {
          instanceWrapper.settlementSignal?.error(err);
        });
        this.addDeferredLoad(resolutionContext.contextId, deferredLoad);
        this.trackDurableDeferredLoad(
          instanceWrapper,
          resolutionContext.contextId,
          deferredLoad,
        );
      } else {
        /**
         * No load has ever been scheduled for this context (e.g., request-scoped
         * providers are no longer instantiated during static bootstrap, so a fresh
         * durable/request sub-tree host has no inherited `donePromise`).
         * Load it now; if a circular dependency is truly in-flight, the nested
         * lookup will find this host pending and defer through its `donePromise`.
         */
        await this.loadProvider(
          instanceWrapper,
          instanceWrapper.host ?? moduleRef,
          resolutionContext,
        );
      }
    }
    if (instanceWrapper.async) {
      const host = instanceWrapper.getInstanceByContextId(
        this.getContextId(resolutionContext.contextId, instanceWrapper),
        inquirerId,
      );
      host.instance = await host.instance;
      instanceWrapper.setInstanceByContextId(
        resolutionContext.contextId,
        host,
        inquirerId,
      );
    }
    this.linkDurableDeferredLoads(
      instanceWrapper,
      resolutionContext.contextId,
      this.getContextId(resolutionContext.contextId, instanceWrapper),
    );
    return instanceWrapper;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async resolveComponentHost<T>(
    moduleRef: Module,
    instanceWrapper: InstanceWrapper<T | Promise<T>>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  ): Promise<InstanceWrapper> {
    const inquirerId = this.getContextInquirerId(resolutionContext);
    const instanceHost = this.getInstanceHost(
      instanceWrapper,
      this.getContextId(resolutionContext.contextId, instanceWrapper),
      inquirerId,
    );
    if (!instanceHost.isResolved && !instanceWrapper.forwardRef) {
      resolutionContext.inquirer?.settlementSignal?.insertRef(instanceWrapper);

      await this.loadProvider(
        instanceWrapper,
        instanceWrapper.host ?? moduleRef,
        resolutionContext,
      );
    } else if (
      !instanceHost.isResolved &&
      instanceWrapper.forwardRef &&
      (resolutionContext.contextId !== STATIC_CONTEXT || !!inquirerId)
    ) {
      /**
       * When circular dependency has been detected between
       * either request/transient providers, we have to asynchronously
       * resolve instance host for a specific contextId or inquirer, to ensure
       * that eventual lazily created instance will be merged with the prototype
       * instantiated beforehand.
       */
      if (instanceHost.donePromise) {
        const deferredLoad = instanceHost.donePromise.then((err?: unknown) => {
          // The placeholder handed out belongs to the load that failed
          if (err) {
            throw err;
          }
          return this.loadProvider(
            instanceWrapper,
            instanceWrapper.host ?? moduleRef,
            resolutionContext,
          );
        });
        void deferredLoad.catch(err => {
          instanceWrapper.settlementSignal?.error(err);
        });
        this.addDeferredLoad(resolutionContext.contextId, deferredLoad);
        this.trackDurableDeferredLoad(
          instanceWrapper,
          resolutionContext.contextId,
          deferredLoad,
        );
      } else {
        /**
         * No load has ever been scheduled for this context (e.g., request-scoped
         * providers are no longer instantiated during static bootstrap, so a fresh
         * durable/request sub-tree host has no inherited `donePromise`).
         * Record the edge before loading it, so that if this load reaches the
         * inquirer while it is still pending, `isCycle()` sees the cycle and throws
         * instead of awaiting a `donePromise` that depends on itself.
         */
        resolutionContext.inquirer?.settlementSignal?.insertRef(
          instanceWrapper,
        );

        await this.loadProvider(
          instanceWrapper,
          instanceWrapper.host ?? moduleRef,
          resolutionContext,
        );
      }
    }
    if (instanceWrapper.async) {
      const host = instanceWrapper.getInstanceByContextId(
        this.getContextId(resolutionContext.contextId, instanceWrapper),
        inquirerId,
      );
      host.instance = await host.instance;
      instanceWrapper.setInstanceByContextId(
        resolutionContext.contextId,
        host,
        inquirerId,
      );
    }
    this.linkDurableDeferredLoads(
      instanceWrapper,
      resolutionContext.contextId,
      this.getContextId(resolutionContext.contextId, instanceWrapper),
    );
    return instanceWrapper;
  }
```


---

### 🔹 Commit #10: `770c6f1a`
- **完整 Hash**: `770c6f1a191830b1c9a19f33b0f0e08cb45f8a8e`
- **說明 (Ground Truth)**: fix(common): match a file type string up to the end of a name
- **變更檔案數**: 1

#### 📄 檔案: `packages/common/pipes/file/file-type.validator.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:7, E:3, A:0) ➔ After(N:7, E:3, A:0)
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

### 🔹 函式: `matchesFileType()`
- **變更前簽章 (Before)**: `matchesFileType(mimetype: string)` (L191~L203)
- **變更後簽章 (After)**: `matchesFileType(mimetype: string)` (L195~L213)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private matchesFileType(mimetype: string): boolean {
    const { fileType } = this.validationOptions;
    // A string is coerced into a RegExp by `String#match`, so MIME types holding
    // regex metacharacters (the `+` in `image/svg+xml`) never match themselves.
    if (typeof fileType === 'string' && mimetype === fileType) {
      return true;
    }
    // Stateful expressions must start at zero for each file, without changing
    // the caller's lastIndex (the validator can be reused across uploads).
    const pattern =
      typeof fileType === 'string' ? fileType : new RegExp(fileType);
    return !!mimetype.match(pattern);
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private matchesFileType(mimetype: string): boolean {
    const { fileType } = this.validationOptions;
    // A string is coerced into a RegExp by `String#match`, so MIME types holding
    // regex metacharacters (the `+` in `image/svg+xml`) never match themselves.
    if (typeof fileType === 'string' && mimetype === fileType) {
      return true;
    }
    if (typeof fileType === 'string') {
      // A string that ends in a letter or a digit must match up to the end
      // of a name, or "audio/wav" would accept "audio/wavpack" and
      // "font/woff" would accept "font/woff2".
      return !!mimetype.match(
        /[a-z\d]$/i.test(fileType) ? `(?:${fileType})(?![\\w-])` : fileType,
      );
    }
    // Stateful expressions must start at zero for each file, without changing
    // the caller's lastIndex (the validator can be reused across uploads).
    return !!mimetype.match(new RegExp(fileType));
  }
```


---

### 🔹 Commit #11: `8c5a59bf`
- **完整 Hash**: `8c5a59bf63c0d68a462c085ee2976a7d5b1aba9a`
- **說明 (Ground Truth)**: fix(common): stop exposing the validated object on validation errors
- **變更檔案數**: 1

#### 📄 檔案: `packages/common/pipes/validation.pipe.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:28, E:10, A:0) ➔ After(N:28, E:10, A:0)
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

### 🔹 函式: `transform()`
- **變更前簽章 (Before)**: `transform(value: unknown, metadata: ArgumentMetadata)` (L151~L237)
- **變更後簽章 (After)**: `transform(value: unknown, metadata: ArgumentMetadata)` (L151~L246)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async transform(value: unknown, metadata: ArgumentMetadata) {
    if (this.expectedType) {
      metadata = { ...metadata, metatype: this.expectedType };
    }

    const metatype = metadata.metatype;
    if (!metatype || !this.toValidate(metadata)) {
      return this.isTransformEnabled
        ? this.transformPrimitive(value, metadata)
        : value;
    }

    classValidator = (await classValidator) as ValidatorPackage;
    classTransformer = (await classTransformer) as TransformerPackage;

    const originalValue = value;
    value = this.toEmptyIfNil(value, metatype);

    const isNil = value !== originalValue;
    const isPrimitive = this.isPrimitive(value);
    this.stripProtoKeys(value);
    let entity = classTransformer.plainToInstance(
      metatype,
      value,
      this.transformOptions,
    );

    const originalEntity = entity;
    const isCtorNotEqual = entity.constructor !== metatype;

    if (isCtorNotEqual && !isPrimitive) {
      entity.constructor = metatype;
    } else if (isCtorNotEqual) {
      // when "entity" is a primitive value, we have to temporarily
      // replace the entity to perform the validation against the original
      // metatype defined inside the handler
      entity = { constructor: metatype };
    }

    const errors = await this.validate(entity, this.validatorOptions);
    if (errors.length > 0) {
      throw await this.exceptionFactory(errors);
    }
    if (
      isCtorNotEqual &&
      (isPrimitive || Array.isArray(value)) &&
      (await this.hasValidationRules(metatype))
    ) {
      // An array or a primitive is never an instance of the class: the
      // validation above has only seen a stand-in without any property set,
      // which passes when none of them is required.
      throw await this.exceptionFactory([
        {
          property: metadata.data || metadata.type,
          constraints: { isObject: 'Validation failed (object is expected)' },
          children: [],
        },
      ]);
    }

    if (originalValue === undefined && originalEntity === '') {
      // Since SWC requires empty string for validation (to avoid an error),
      // a fallback is needed to revert to the original value (when undefined).
      // @see [https://github.com/nestjs/nest/issues/14430](https://github.com/nestjs/nest/issues/14430)
      return originalValue;
    }
    if (isPrimitive) {
      // if the value is a primitive value and the validation process has been successfully completed
      // we have to revert the original value passed through the pipe
      entity = originalEntity;
    }
    if (this.isTransformEnabled) {
      return entity;
    }
    if (isNil) {
      // if the value was originally undefined or null, revert it back
      return originalValue;
    }

    // we check if the number of keys of the "validatorOptions" is higher than 1 (instead of 0)
    // because the "forbidUnknownValues" now fallbacks to "false" (in case it wasn't explicitly specified)
    const shouldTransformToPlain =
      Object.keys(this.validatorOptions).length > 1;
    return shouldTransformToPlain
      ? classTransformer.classToPlain(entity, this.transformOptions)
      : value;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async transform(value: unknown, metadata: ArgumentMetadata) {
    if (this.expectedType) {
      metadata = { ...metadata, metatype: this.expectedType };
    }

    const metatype = metadata.metatype;
    if (!metatype || !this.toValidate(metadata)) {
      return this.isTransformEnabled
        ? this.transformPrimitive(value, metadata)
        : value;
    }

    classValidator = (await classValidator) as ValidatorPackage;
    classTransformer = (await classTransformer) as TransformerPackage;

    const originalValue = value;
    value = this.toEmptyIfNil(value, metatype);

    const isNil = value !== originalValue;
    const isPrimitive = this.isPrimitive(value);
    this.stripProtoKeys(value);
    let entity = classTransformer.plainToInstance(
      metatype,
      value,
      this.transformOptions,
    );

    const originalEntity = entity;
    const isCtorNotEqual = entity.constructor !== metatype;

    if (isCtorNotEqual && !isPrimitive) {
      entity.constructor = metatype;
    } else if (isCtorNotEqual) {
      // when "entity" is a primitive value, we have to temporarily
      // replace the entity to perform the validation against the original
      // metatype defined inside the handler
      entity = { constructor: metatype };
    }

    const errors = await this.validate(entity, {
      ...this.validatorOptions,
      // The target of an error is the whole object it was found in, so an
      // exception factory that sends the errors would repeat that object
      // once per error.
      validationError: {
        target: false,
        ...this.validatorOptions.validationError,
      },
    });
    if (errors.length > 0) {
      throw await this.exceptionFactory(errors);
    }
    if (
      isCtorNotEqual &&
      (isPrimitive || Array.isArray(value)) &&
      (await this.hasValidationRules(metatype))
    ) {
      // An array or a primitive is never an instance of the class: the
      // validation above has only seen a stand-in without any property set,
      // which passes when none of them is required.
      throw await this.exceptionFactory([
        {
          property: metadata.data || metadata.type,
          constraints: { isObject: 'Validation failed (object is expected)' },
          children: [],
        },
      ]);
    }

    if (originalValue === undefined && originalEntity === '') {
      // Since SWC requires empty string for validation (to avoid an error),
      // a fallback is needed to revert to the original value (when undefined).
      // @see [https://github.com/nestjs/nest/issues/14430](https://github.com/nestjs/nest/issues/14430)
      return originalValue;
    }
    if (isPrimitive) {
      // if the value is a primitive value and the validation process has been successfully completed
      // we have to revert the original value passed through the pipe
      entity = originalEntity;
    }
    if (this.isTransformEnabled) {
      return entity;
    }
    if (isNil) {
      // if the value was originally undefined or null, revert it back
      return originalValue;
    }

    // we check if the number of keys of the "validatorOptions" is higher than 1 (instead of 0)
    // because the "forbidUnknownValues" now fallbacks to "false" (in case it wasn't explicitly specified)
    const shouldTransformToPlain =
      Object.keys(this.validatorOptions).length > 1;
    return shouldTransformToPlain
      ? classTransformer.classToPlain(entity, this.transformOptions)
      : value;
  }
```


---

### 🔹 Commit #12: `086c1c51`
- **完整 Hash**: `086c1c514faf8e04922c63fb4cd8bca87d90ced3`
- **說明 (Ground Truth)**: fix(common): limit the length of validation error messages by default
- **變更檔案數**: 1

#### 📄 檔案: `packages/common/pipes/validation.pipe.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:25, E:9, A:0) ➔ After(N:28, E:10, A:0)
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
  • + [新增節點] `DEFAULT_MAX_ERROR_MESSAGES_LENGTH` (MODULE_STATE)
  • + [新增節點] `OMITTED_ERRORS_MESSAGE` (MODULE_STATE)
  • + [新增節點] `limitValidationErrors` (FUNCTION_DEF)
  • + [新增呼叫邊] `limitValidationErrors` ──[CALLS [guarded]]──> `String (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `constructor()`
- **變更前簽章 (Before)**: `constructor(@Optional() options?: ValidationPipeOptions)` (L76~L106)
- **變更後簽章 (After)**: `constructor(@Optional() options?: ValidationPipeOptions)` (L90~L123)

#### ◀️ 變更前實作碼 (Before Implementation):
```
constructor(@Optional() options?: ValidationPipeOptions) {
    options = options || {};
    const {
      transform,
      disableErrorMessages,
      errorHttpStatusCode,
      expectedType,
      transformOptions,
      exceptionFactory,
      validatorPackage,
      transformerPackage,
      validateCustomDecorators,
      errorFormat,
      ...validatorOptions
    } = options;

    // @see [https://github.com/nestjs/nest/issues/10683#issuecomment-1413690508](https://github.com/nestjs/nest/issues/10683#issuecomment-1413690508)
    this.validatorOptions = { forbidUnknownValues: false, ...validatorOptions };

    this.isTransformEnabled = !!transform;
    this.transformOptions = transformOptions;
    this.isDetailedOutputDisabled = disableErrorMessages;
    this.validateCustomDecorators = validateCustomDecorators || false;
    this.errorHttpStatusCode = errorHttpStatusCode || HttpStatus.BAD_REQUEST;
    this.expectedType = expectedType;
    this.errorFormat = errorFormat || 'list';
    this.exceptionFactory = exceptionFactory || this.createExceptionFactory();

    classValidator = this.loadValidator(validatorPackage);
    classTransformer = this.loadTransformer(transformerPackage);
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
constructor(@Optional() options?: ValidationPipeOptions) {
    options = options || {};
    const {
      transform,
      disableErrorMessages,
      errorHttpStatusCode,
      expectedType,
      transformOptions,
      exceptionFactory,
      validatorPackage,
      transformerPackage,
      validateCustomDecorators,
      errorFormat,
      maxErrorMessagesLength,
      ...validatorOptions
    } = options;

    // @see [https://github.com/nestjs/nest/issues/10683#issuecomment-1413690508](https://github.com/nestjs/nest/issues/10683#issuecomment-1413690508)
    this.validatorOptions = { forbidUnknownValues: false, ...validatorOptions };

    this.isTransformEnabled = !!transform;
    this.transformOptions = transformOptions;
    this.isDetailedOutputDisabled = disableErrorMessages;
    this.validateCustomDecorators = validateCustomDecorators || false;
    this.errorHttpStatusCode = errorHttpStatusCode || HttpStatus.BAD_REQUEST;
    this.expectedType = expectedType;
    this.errorFormat = errorFormat || 'list';
    this.maxErrorMessagesLength =
      maxErrorMessagesLength ?? DEFAULT_MAX_ERROR_MESSAGES_LENGTH;
    this.exceptionFactory = exceptionFactory || this.createExceptionFactory();

    classValidator = this.loadValidator(validatorPackage);
    classTransformer = this.loadTransformer(transformerPackage);
  }
```

### 🔹 函式: `createExceptionFactory()`
- **變更前簽章 (Before)**: `createExceptionFactory()` (L222~L244)
- **變更後簽章 (After)**: `createExceptionFactory()` (L239~L272)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public createExceptionFactory() {
    return (validationErrors: ValidationError[] = []) => {
      if (this.isDetailedOutputDisabled) {
        return new HttpErrorByCode[this.errorHttpStatusCode]();
      }
      if (this.errorFormat === 'grouped') {
        const errors = this.groupValidationErrors(validationErrors);
        // Custom (object) bodies are returned verbatim by
        // `HttpException.createBody`, so add the standard envelope fields
        // explicitly to match the shape of the "list" format.
        const { message: error, statusCode } = (
          new HttpErrorByCode[this.errorHttpStatusCode]() as HttpException
        ).getResponse() as { message: string; statusCode: number };
        return new HttpErrorByCode[this.errorHttpStatusCode]({
          message: errors,
          error,
          statusCode,
        });
      }
      const errors = this.flattenValidationErrors(validationErrors);
      return new HttpErrorByCode[this.errorHttpStatusCode](errors);
    };
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public createExceptionFactory() {
    return (validationErrors: ValidationError[] = []) => {
      if (this.isDetailedOutputDisabled) {
        return new HttpErrorByCode[this.errorHttpStatusCode]();
      }
      const budget = {
        remaining: this.maxErrorMessagesLength,
        isExceeded: false,
      };
      validationErrors = this.limitValidationErrors(validationErrors, budget);
      if (this.errorFormat === 'grouped') {
        let errors = this.groupValidationErrors(validationErrors);
        if (budget.isExceeded) {
          errors = { ...errors, '...': [OMITTED_ERRORS_MESSAGE] };
        }
        // Custom (object) bodies are returned verbatim by
        // `HttpException.createBody`, so add the standard envelope fields
        // explicitly to match the shape of the "list" format.
        const { message: error, statusCode } = (
          new HttpErrorByCode[this.errorHttpStatusCode]() as HttpException
        ).getResponse() as { message: string; statusCode: number };
        return new HttpErrorByCode[this.errorHttpStatusCode]({
          message: errors,
          error,
          statusCode,
        });
      }
      let errors = this.flattenValidationErrors(validationErrors);
      if (budget.isExceeded) {
        errors = [...errors, OMITTED_ERRORS_MESSAGE];
      }
      return new HttpErrorByCode[this.errorHttpStatusCode](errors);
    };
  }
```


---

### 🔹 Commit #13: `8b420f78`
- **完整 Hash**: `8b420f788f05eb30ee8013529f4c359125e1391c`
- **說明 (Ground Truth)**: fix(fastify): apply middleware to plugins registered before init
- **變更檔案數**: 1

#### 📄 檔案: `packages/platform-fastify/adapters/fastify-adapter.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:118, E:38, A:0) ➔ After(N:119, E:39, A:0)
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
  • + [新增節點] `createMiddleware` (FUNCTION_DEF)
  • + [新增呼叫邊] `createMiddlewareFactory` ──[CALLS [guarded]]──> `createMiddleware`
  • + [新增呼叫邊] `createMiddleware` ──[CALLS [guard: (normalizedPath)]]──> `next (External/Unresolved)`
  • - [移除呼叫邊] `createMiddlewareFactory` ──[CALLS]──> `next (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `createMiddlewareFactory()`
- **變更前簽章 (Before)**: `createMiddlewareFactory(
    requestMethod: RequestMethod,
  )` (L1104~L1184)
- **變更後簽章 (After)**: `createMiddlewareFactory(
    requestMethod: RequestMethod,
  )` (L1107~L1198)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async createMiddlewareFactory(
    requestMethod: RequestMethod,
  ): Promise<(path: string, callback: Function) => any> {
    if (!this.isMiddieRegistered) {
      await this.registerMiddie();
    }
    return (path: string, callback: Function) => {
      const hasEndOfStringCharacter = path.endsWith('$');
      path = hasEndOfStringCharacter ? path.slice(0, -1) : path;

      let normalizedPath = LegacyRouteConverter.tryConvert(path);

      // Fallback to "*path" to support plugins like GraphQL
      normalizedPath = normalizedPath === '/*path' ? '*path' : normalizedPath;

      // Normalize the path to support the prefix if it set in application
      if (
        this._pathPrefix &&
        !normalizedPath.startsWith(this._pathPrefix) &&
        (normalizedPath === '/' || normalizedPath === '')
      ) {
        normalizedPath = `${this._pathPrefix}${normalizedPath}`;
        if (normalizedPath.endsWith('/')) {
          normalizedPath = `${normalizedPath}{*path}`;
        }
      }

      try {
        let { regexp: re } = pathToRegexp(normalizedPath);
        re = hasEndOfStringCharacter
          ? new RegExp(re.source + '$', re.flags)
          : re;

        // A case-insensitive router lower-cases the decoded path, where some
        // characters only fold to ASCII ("%E2%84%AA", KELVIN SIGN, is routed
        // as "k"). The RegExp of @fastify/middie does not fold them, so on
        // such a router the middleware is registered for every path and the
        // path is only matched below.
        const { caseSensitive } = this.getRouteMatchingOptions();

        // The following type assertion is valid as we use import('@fastify/middie') rather than require('@fastify/middie')
        // ref https://github.com/fastify/middie/pull/55
        this.instance.use(
          caseSensitive ? normalizedPath : '/',
          (req: any, res: any, next: (err?: Error) => void) => {
            const queryParamsIndex = req.originalUrl.indexOf('?');
            let pathname =
              queryParamsIndex >= 0
                ? req.originalUrl.slice(0, queryParamsIndex)
                : req.originalUrl;

            pathname = this.sanitizeUrl(pathname);

            if (normalizedPath) {
              const pathToCheck = pathname.endsWith('/')
                ? pathname
                : `${pathname}/`;
              if (!re.exec(pathToCheck)) {
                return next();
              }
              if (!caseSensitive) {
                // Strips the path from "req.url", as @fastify/middie does
                // when it matches the path itself
                const suffixIndex = req.originalUrl.search(/[?#]/);
                req.url =
                  suffixIndex >= 0
                    ? `/${req.originalUrl.slice(suffixIndex)}`
                    : '/';
              }
            }
            this.runMiddleware(callback, req, res, next);
          },
        );
      } catch (e) {
        if (e instanceof TypeError) {
          LegacyRouteConverter.printError(path);
        }
        throw e;
      }
    };
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async createMiddlewareFactory(
    requestMethod: RequestMethod,
  ): Promise<(path: string, callback: Function) => any> {
    if (!this.isMiddieRegistered) {
      await this.registerMiddie();
    }
    return (path: string, callback: Function) => {
      const hasEndOfStringCharacter = path.endsWith('$');
      path = hasEndOfStringCharacter ? path.slice(0, -1) : path;

      let normalizedPath = LegacyRouteConverter.tryConvert(path);

      // Fallback to "*path" to support plugins like GraphQL
      normalizedPath = normalizedPath === '/*path' ? '*path' : normalizedPath;

      // Normalize the path to support the prefix if it set in application
      if (
        this._pathPrefix &&
        !normalizedPath.startsWith(this._pathPrefix) &&
        (normalizedPath === '/' || normalizedPath === '')
      ) {
        normalizedPath = `${this._pathPrefix}${normalizedPath}`;
        if (normalizedPath.endsWith('/')) {
          normalizedPath = `${normalizedPath}{*path}`;
        }
      }

      try {
        let { regexp: re } = pathToRegexp(normalizedPath);
        re = hasEndOfStringCharacter
          ? new RegExp(re.source + '$', re.flags)
          : re;

        // A case-insensitive router lower-cases the decoded path, where some
        // characters only fold to ASCII ("%E2%84%AA", KELVIN SIGN, is routed
        // as "k"). The RegExp of @fastify/middie does not fold them, so on
        // such a router the middleware is registered for every path and the
        // path is only matched below.
        const { caseSensitive } = this.getRouteMatchingOptions();

        const createMiddleware =
          (stripsPath: boolean) =>
          (req: any, res: any, next: (err?: Error) => void) => {
            const queryParamsIndex = req.originalUrl.indexOf('?');
            let pathname =
              queryParamsIndex >= 0
                ? req.originalUrl.slice(0, queryParamsIndex)
                : req.originalUrl;

            pathname = this.sanitizeUrl(pathname);

            if (normalizedPath) {
              const pathToCheck = pathname.endsWith('/')
                ? pathname
                : `${pathname}/`;
              if (!re.exec(pathToCheck)) {
                return next();
              }
              if (stripsPath) {
                // Strips the path from "req.url", as @fastify/middie does
                // when it matches the path itself
                const suffixIndex = req.originalUrl.search(/[?#]/);
                req.url =
                  suffixIndex >= 0
                    ? `/${req.originalUrl.slice(suffixIndex)}`
                    : '/';
              }
            }
            this.runMiddleware(callback, req, res, next);
          };

        // The following type assertion is valid as we use import('@fastify/middie') rather than require('@fastify/middie')
        // ref https://github.com/fastify/middie/pull/55
        this.instance.use(
          caseSensitive ? normalizedPath : '/',
          createMiddleware(!caseSensitive),
        );
        // The contexts created since middie was registered have a copy of the
        // middleware of their parent without this one (see `registerMiddie()`).
        // It is registered there without its path, which middie would prefix
        // with the one of the context.
        for (const context of this.middieContexts) {
          context.use(createMiddleware(true));
        }
      } catch (e) {
        if (e instanceof TypeError) {
          LegacyRouteConverter.printError(path);
        }
        throw e;
      }
    };
  }
```

### 🔹 函式: `registerMiddie()`
- **變更前簽章 (Before)**: `registerMiddie()` (L1359~L1364)
- **變更後簽章 (After)**: `registerMiddie()` (L1373~L1387)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private async registerMiddie() {
    this.isMiddieRegistered = true;
    await this.register(
      middie as unknown as Parameters<TInstance['register']>[0],
    );
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private async registerMiddie() {
    this.isMiddieRegistered = true;
    await this.register(
      middie as unknown as Parameters<TInstance['register']>[0],
    );
    // middie gives each encapsulated context created from now on a copy of
    // the middleware of its parent, as it is at that time. As
    // `NestFactory.create()` registers middie before `main.ts` runs, a
    // plugin registered there with an awaited `register()` gets a context
    // without the Nest middleware `app.init()` registers later, so
    // `createMiddlewareFactory()` adds it to the contexts tracked here.
    this.instance.addHook('onRegister', instance => {
      this.middieContexts.push(instance as TInstance);
    });
  }
```


---

### 🔹 Commit #14: `b080b4cb`
- **完整 Hash**: `b080b4cbb1fda8eeb888c415413fb1028fbbce6f`
- **說明 (Ground Truth)**: fix(fastify): keep raw-response cookies in the header helpers (#18175)
- **變更檔案數**: 1

#### 📄 檔案: `packages/platform-fastify/adapters/fastify-adapter.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:118, E:38, A:0) ➔ After(N:118, E:38, A:0)
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

### 🔹 函式: `setHeader()`
- **變更前簽章 (Before)**: `setHeader(response: TReply, name: string, value: string)` (L956~L958)
- **變更後簽章 (After)**: `setHeader(
    response: TRawResponse | TReply,
    name: string,
    value: string,
  )` (L956~L966)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public setHeader(response: TReply, name: string, value: string) {
    return response.header(name, value);
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public setHeader(
    response: TRawResponse | TReply,
    name: string,
    value: string,
  ) {
    if (this.isNativeResponse(response)) {
      return response.setHeader(name, value);
    }
    const reply: TReply = response;
    return reply.header(name, value);
  }
```

### 🔹 函式: `appendHeader()`
- **變更前簽章 (Before)**: `appendHeader(response: any, name: string, value: string)` (L960~L972)
- **變更後簽章 (After)**: `appendHeader(
    response: TRawResponse | TReply,
    name: string,
    value: string,
  )` (L968~L1004)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public appendHeader(response: any, name: string, value: string) {
    const current = response.getHeader(name);
    if (current === undefined) {
      return response.header(name, value);
    }
    // Fastify Reply.header() already concatenates set-cookie.
    // Re-passing the accumulated list would duplicate previous cookies.
    if (String(name).toLowerCase() === 'set-cookie') {
      return response.header(name, value);
    }
    const values = Array.isArray(current) ? current : [current];
    return response.header(name, values.concat(value));
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public appendHeader(
    response: TRawResponse | TReply,
    name: string,
    value: string,
  ) {
    if (this.isNativeResponse(response)) {
      const current = response.getHeader(name);
      return response.setHeader(
        name,
        current === undefined ? value : [current, value].flat().map(String),
      );
    }
    const reply: TReply = response;
    // A set-cookie value can live on the reply or only on the raw response
    // (e.g., set by a middleware). Reply.getHeader() reads both, and the
    // merged list is written to both: reply.send() sends the reply headers,
    // while a hijacked reply or a handler that ends reply.raw sends the raw
    // ones.
    if (String(name).toLowerCase() === 'set-cookie') {
      const current = reply.getHeader(name);
      const values =
        current === undefined ? [value] : [current, value].flat().map(String);
      reply.removeHeader(name);
      reply.header(name, values);
      if (!reply.raw.headersSent) {
        // A copy, so a later reply.header() call does not change the raw header
        reply.raw.setHeader(name, [...values]);
      }
      return reply;
    }
    const current = reply.getHeader(name);
    if (current === undefined) {
      return reply.header(name, value);
    }
    const values = Array.isArray(current) ? current : [current];
    return reply.header(name, values.concat(value));
  }
```


---

### 🔹 Commit #15: `2eb7be8d`
- **完整 Hash**: `2eb7be8dc3410ac5b89aa84fd334e6813b53059c`
- **說明 (Ground Truth)**: fix(microservices): preserve request order during deferred replay (#18179)
- **變更檔案數**: 1

#### 📄 檔案: `packages/microservices/server/server-grpc.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:74, E:63, A:0) ➔ After(N:74, E:63, A:0)
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
  - 💥 作用域阻隔: 函式 'next' 被深鎖在內部閉包 (scope:arrow@after/packages/microservices/server/server-grpc.ts:L354C9)，外部無法調用！
  - 💥 作用域阻隔: 函式 'complete' 被深鎖在內部閉包 (scope:arrow@after/packages/microservices/server/server-grpc.ts:L447C24)，外部無法調用！
  - 💥 作用域阻隔: 函式 'error' 被深鎖在內部閉包 (scope:arrow@after/packages/microservices/server/server-grpc.ts:L354C9)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `next()`
- **變更前簽章 (Before)**: `next(value: T)` (L963~L968)
- **變更後簽章 (After)**: `next(value: T)` (L963~L970)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(value: T) => {
        if (!hasDrained) {
          replayBuffer!.next(value);
        }
        subject.next(value);
      }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(value: T) => {
        if (replayBuffer) {
          replayBuffer.next(value);
        }
        if (!hasDrained || !replayBuffer) {
          subject.next(value);
        }
      }
```

### 🔹 函式: `bufferUntilDrained()`
- **變更前簽章 (Before)**: `bufferUntilDrained()` (L921~L985)
- **變更後簽章 (After)**: `bufferUntilDrained()` (L921~L987)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private bufferUntilDrained<T>() {
    type DrainableSubject<T> = Subject<T> & { drainBuffer: () => void };

    const subject = new Subject<T>();
    let replayBuffer: ReplaySubject<T> | null = new ReplaySubject<T>();
    let hasDrained = false;

    function drainBuffer(this: DrainableSubject<T>) {
      if (hasDrained || !replayBuffer) {
        return;
      }
      hasDrained = true;

      // Replay buffered values to the new subscriber
      setImmediate(() => {
        const subscription = replayBuffer!.subscribe(subject);
        subscription.unsubscribe();
        replayBuffer = null;
      });
    }

    return {
      subject: new Proxy<DrainableSubject<T>>(subject as DrainableSubject<T>, {
        get(target, prop, receiver) {
          if (prop === 'asObservable') {
            return () => {
              const stream = subject.asObservable();

              // "drainBuffer" will be called before the evaluation of the handler
              // but after any enhancers have been applied (e.g., `interceptors`)
              Object.defineProperty(stream, drainBuffer.name, {
                value: drainBuffer,
              });
              return stream;
            };
          }
          if (hasDrained) {
            return Reflect.get(target, prop, receiver);
          }
          return Reflect.get(replayBuffer!, prop, receiver);
        },
      }),
      next: (value: T) => {
        if (!hasDrained) {
          replayBuffer!.next(value);
        }
        subject.next(value);
      },
      error: (err: any) => {
        replayBuffer?.error(err);
        subject.error(err);
      },
      complete: () => {
        if (replayBuffer) {
          // The subject completes once the buffer has been replayed into it,
          // which "drainBuffer" does after the handler has subscribed. The
          // buffer is kept until then: dropping it here would leave a handler
          // that has not run yet without its messages and without completion.
          replayBuffer.complete();
          return;
        }
        subject.complete();
      },
    };
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private bufferUntilDrained<T>() {
    type DrainableSubject<T> = Subject<T> & { drainBuffer: () => void };

    const subject = new Subject<T>();
    let replayBuffer: ReplaySubject<T> | null = new ReplaySubject<T>();
    let hasDrained = false;

    function drainBuffer(this: DrainableSubject<T>) {
      if (hasDrained || !replayBuffer) {
        return;
      }
      hasDrained = true;

      // Replay buffered values to the new subscriber
      setImmediate(() => {
        const subscription = replayBuffer!.subscribe(subject);
        subscription.unsubscribe();
        replayBuffer = null;
      });
    }

    return {
      subject: new Proxy<DrainableSubject<T>>(subject as DrainableSubject<T>, {
        get(target, prop, receiver) {
          if (prop === 'asObservable') {
            return () => {
              const stream = subject.asObservable();

              // "drainBuffer" will be called before the evaluation of the handler
              // but after any enhancers have been applied (e.g., `interceptors`)
              Object.defineProperty(stream, drainBuffer.name, {
                value: drainBuffer,
              });
              return stream;
            };
          }
          if (hasDrained) {
            return Reflect.get(target, prop, receiver);
          }
          return Reflect.get(replayBuffer!, prop, receiver);
        },
      }),
      next: (value: T) => {
        if (replayBuffer) {
          replayBuffer.next(value);
        }
        if (!hasDrained || !replayBuffer) {
          subject.next(value);
        }
      },
      error: (err: any) => {
        replayBuffer?.error(err);
        subject.error(err);
      },
      complete: () => {
        if (replayBuffer) {
          // The subject completes once the buffer has been replayed into it,
          // which "drainBuffer" does after the handler has subscribed. The
          // buffer is kept until then: dropping it here would leave a handler
          // that has not run yet without its messages and without completion.
          replayBuffer.complete();
          return;
        }
        subject.complete();
      },
    };
  }
```


---

### 🔹 Commit #16: `92136a61`
- **完整 Hash**: `92136a6113675f50a44ff636e9b010bdf3de4cb6`
- **說明 (Ground Truth)**: fix(core): give a module that extends another module its own id (#18180)
- **變更檔案數**: 1

#### 📄 檔案: `packages/core/injector/opaque-key-factory/by-reference-module-opaque-key-factory.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:10, E:2, A:0) ➔ After(N:10, E:2, A:0)
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

### 🔹 函式: `getOrCreateModuleId()`
- **變更前簽章 (Before)**: `getOrCreateModuleId(
    moduleCls: Type<unknown>,
    dynamicMetadata: Partial<DynamicModule> | undefined,
    originalRef: Type | DynamicModule | ForwardReference,
  )` (L30~L51)
- **變更後簽章 (After)**: `getOrCreateModuleId(
    moduleCls: Type<unknown>,
    dynamicMetadata: Partial<DynamicModule> | undefined,
    originalRef: Type | DynamicModule | ForwardReference,
  )` (L30~L52)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private getOrCreateModuleId(
    moduleCls: Type<unknown>,
    dynamicMetadata: Partial<DynamicModule> | undefined,
    originalRef: Type | DynamicModule | ForwardReference,
  ): string {
    if (originalRef[K_MODULE_ID]) {
      return originalRef[K_MODULE_ID];
    }

    let moduleId: string;
    if (this.keyGenerationStrategy === 'random') {
      moduleId = this.generateRandomString();
    } else {
      const delimiter = ':';
      moduleId = dynamicMetadata
        ? `${this.generateRandomString()}${delimiter}${this.hashString(moduleCls.name + JSON.stringify(dynamicMetadata))}`
        : `${this.generateRandomString()}${delimiter}${this.hashString(moduleCls.toString())}`;
    }

    originalRef[K_MODULE_ID] = moduleId;
    return moduleId;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private getOrCreateModuleId(
    moduleCls: Type<unknown>,
    dynamicMetadata: Partial<DynamicModule> | undefined,
    originalRef: Type | DynamicModule | ForwardReference,
  ): string {
    // Own property only: a subclass would inherit the id of the module it extends.
    if (Object.prototype.hasOwnProperty.call(originalRef, K_MODULE_ID)) {
      return originalRef[K_MODULE_ID];
    }

    let moduleId: string;
    if (this.keyGenerationStrategy === 'random') {
      moduleId = this.generateRandomString();
    } else {
      const delimiter = ':';
      moduleId = dynamicMetadata
        ? `${this.generateRandomString()}${delimiter}${this.hashString(moduleCls.name + JSON.stringify(dynamicMetadata))}`
        : `${this.generateRandomString()}${delimiter}${this.hashString(moduleCls.toString())}`;
    }

    originalRef[K_MODULE_ID] = moduleId;
    return moduleId;
  }
```


---

### 🔹 Commit #17: `462da914`
- **完整 Hash**: `462da9143489f6a6c61e160a8b2a8186ed569104`
- **說明 (Ground Truth)**: fix(testing): share one auto-mock between providers of the same token (#18170)
- **變更檔案數**: 1

#### 📄 檔案: `packages/testing/testing-injector.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:6, E:0, A:0) ➔ After(N:6, E:0, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 4, ΔTrans: 0
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

### 🔹 函式: `resolveComponentWrapper()`
- **變更前簽章 (Before)**: `resolveComponentWrapper(
    moduleRef: Module,
    name: any,
    dependencyContext: InjectorDependencyContext,
    wrapper: InstanceWrapper<T>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
    keyOrIndex?: string | number,
  )` (L47~L68)
- **變更後簽章 (After)**: `resolveComponentWrapper(
    moduleRef: Module,
    name: any,
    dependencyContext: InjectorDependencyContext,
    wrapper: InstanceWrapper<T>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
    keyOrIndex?: string | number,
  )` (L50~L71)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async resolveComponentWrapper<T>(
    moduleRef: Module,
    name: any,
    dependencyContext: InjectorDependencyContext,
    wrapper: InstanceWrapper<T>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
    keyOrIndex?: string | number,
  ): Promise<InstanceWrapper> {
    try {
      const existingProviderWrapper = await super.resolveComponentWrapper(
        moduleRef,
        name,
        dependencyContext,
        wrapper,
        resolutionContext,
        keyOrIndex,
      );
      return existingProviderWrapper;
    } catch (err) {
      return this.mockWrapper(err, moduleRef, name, wrapper);
    }
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async resolveComponentWrapper<T>(
    moduleRef: Module,
    name: any,
    dependencyContext: InjectorDependencyContext,
    wrapper: InstanceWrapper<T>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
    keyOrIndex?: string | number,
  ): Promise<InstanceWrapper> {
    try {
      const existingProviderWrapper = await super.resolveComponentWrapper(
        moduleRef,
        name,
        dependencyContext,
        wrapper,
        resolutionContext,
        keyOrIndex,
      );
      return existingProviderWrapper;
    } catch (err) {
      return this.mockWrapper(err, moduleRef, name, name, wrapper);
    }
  }
```

### 🔹 函式: `setMocker()`
- **變更前簽章 (Before)**: `setMocker(mocker: MockFactory)` (L25~L27)
- **變更後簽章 (After)**: `setMocker(mocker: MockFactory)` (L27~L30)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public setMocker(mocker: MockFactory) {
    this.mocker = mocker;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public setMocker(mocker: MockFactory) {
    this.mocker = mocker;
    this.mockedInstances.clear();
  }
```

### 🔹 函式: `mockWrapper()`
- **變更前簽章 (Before)**: `mockWrapper(
    err: Error,
    moduleRef: Module,
    name: any,
    wrapper: InstanceWrapper<T>,
  )` (L92~L132)
- **變更後簽章 (After)**: `mockWrapper(
    err: Error,
    moduleRef: Module,
    name: any,
    token: InjectionToken,
    wrapper: InstanceWrapper<T>,
  )` (L96~L143)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private async mockWrapper<T>(
    err: Error,
    moduleRef: Module,
    name: any,
    wrapper: InstanceWrapper<T>,
  ): Promise<InstanceWrapper> {
    if (!this.mocker) {
      throw err;
    }

    const mockedInstance = this.mocker(name);
    if (!mockedInstance) {
      throw err;
    }
    // The mock is a single value, so it stays static whatever the scope of
    // the provider it replaces or the provider that depends on it.
    const newWrapper = new InstanceWrapper({
      name,
      isAlias: false,
      instance: mockedInstance,
      isResolved: true,
      host: moduleRef,
      metatype: wrapper.metatype,
    });
    const internalCoreModule = this.container.getInternalCoreModuleRef();
    if (!internalCoreModule) {
      throw new Error(
        'Expected to have internal core module reference at this point.',
      );
    }

    internalCoreModule.addCustomProvider(
      {
        provide: name,
        useValue: mockedInstance,
      },
      internalCoreModule.providers,
    );
    internalCoreModule.addExportedProviderOrModule(name);
    return newWrapper;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private async mockWrapper<T>(
    err: Error,
    moduleRef: Module,
    name: any,
    token: InjectionToken,
    wrapper: InstanceWrapper<T>,
  ): Promise<InstanceWrapper> {
    if (!this.mocker) {
      throw err;
    }

    // Every provider that depends on the token must get the same mock,
    // the one `get()` returns.
    let mockedInstance = this.mockedInstances.get(token);
    if (!mockedInstance) {
      mockedInstance = this.mocker(name);
      if (!mockedInstance) {
        throw err;
      }
      this.mockedInstances.set(token, mockedInstance);
    }
    // The mock is a single value, so it stays static whatever the scope of
    // the provider it replaces or the provider that depends on it.
    const newWrapper = new InstanceWrapper({
      name,
      isAlias: false,
      instance: mockedInstance,
      isResolved: true,
      host: moduleRef,
      metatype: wrapper.metatype,
    });
    const internalCoreModule = this.container.getInternalCoreModuleRef();
    if (!internalCoreModule) {
      throw new Error(
        'Expected to have internal core module reference at this point.',
      );
    }

    internalCoreModule.addCustomProvider(
      {
        provide: name,
        useValue: mockedInstance,
      },
      internalCoreModule.providers,
    );
    internalCoreModule.addExportedProviderOrModule(name);
    return newWrapper;
  }
```

### 🔹 函式: `resolveComponentHost()`
- **變更前簽章 (Before)**: `resolveComponentHost(
    moduleRef: Module,
    instanceWrapper: InstanceWrapper<T>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  )` (L70~L90)
- **變更後簽章 (After)**: `resolveComponentHost(
    moduleRef: Module,
    instanceWrapper: InstanceWrapper<T>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  )` (L73~L94)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async resolveComponentHost<T>(
    moduleRef: Module,
    instanceWrapper: InstanceWrapper<T>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  ): Promise<InstanceWrapper> {
    try {
      const existingProviderWrapper = await super.resolveComponentHost(
        moduleRef,
        instanceWrapper,
        resolutionContext,
      );
      return existingProviderWrapper;
    } catch (err) {
      return this.mockWrapper(
        err,
        moduleRef,
        instanceWrapper.name,
        instanceWrapper,
      );
    }
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async resolveComponentHost<T>(
    moduleRef: Module,
    instanceWrapper: InstanceWrapper<T>,
    resolutionContext: ResolutionContext = { contextId: STATIC_CONTEXT },
  ): Promise<InstanceWrapper> {
    try {
      const existingProviderWrapper = await super.resolveComponentHost(
        moduleRef,
        instanceWrapper,
        resolutionContext,
      );
      return existingProviderWrapper;
    } catch (err) {
      return this.mockWrapper(
        err,
        moduleRef,
        instanceWrapper.name,
        instanceWrapper.token,
        instanceWrapper,
      );
    }
  }
```


---

### 🔹 Commit #18: `c215fd9b`
- **完整 Hash**: `c215fd9b4f583486c6ce39a3c43f257dc67e8329`
- **說明 (Ground Truth)**: fix(fastify): match middleware paths like a case-insensitive router
- **變更檔案數**: 1

#### 📄 檔案: `packages/platform-fastify/adapters/fastify-adapter.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:118, E:38, A:0) ➔ After(N:118, E:38, A:0)
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

### 🔹 函式: `sanitizeUrl()`
- **變更前簽章 (Before)**: `sanitizeUrl(url: string)` (L1458~L1489)
- **變更後簽章 (After)**: `sanitizeUrl(url: string)` (L1474~L1505)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private sanitizeUrl(url: string): string {
    const initialConfig = this.instance.initialConfig as FastifyServerOptions;
    const routerOptions = (initialConfig.routerOptions ??
      {}) as Partial<FastifyServerOptions>;

    // Absolute-form request targets ("GET http://host/path HTTP/1.1") must be
    // resolved to their path before any other normalization, as the Fastify
    // router does, so that middleware and routes always match the same path.
    url = this.getPathFromRequestTarget(url);

    if (
      routerOptions.ignoreDuplicateSlashes ||
      initialConfig.ignoreDuplicateSlashes
    ) {
      url = this.removeDuplicateSlashes(url);
    }

    const { caseSensitive, ignoreTrailingSlash } =
      this.getRouteMatchingOptions();
    if (ignoreTrailingSlash) {
      url = this.trimLastSlash(url);
    }

    if (!caseSensitive) {
      url = url.toLowerCase();
    }
    return safeDecodeURI(
      url,
      routerOptions.useSemicolonDelimiter ||
        initialConfig.useSemicolonDelimiter,
    ).path;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private sanitizeUrl(url: string): string {
    const initialConfig = this.instance.initialConfig as FastifyServerOptions;
    const routerOptions = (initialConfig.routerOptions ??
      {}) as Partial<FastifyServerOptions>;

    // Absolute-form request targets ("GET http://host/path HTTP/1.1") must be
    // resolved to their path before any other normalization, as the Fastify
    // router does, so that middleware and routes always match the same path.
    url = this.getPathFromRequestTarget(url);

    if (
      routerOptions.ignoreDuplicateSlashes ||
      initialConfig.ignoreDuplicateSlashes
    ) {
      url = this.removeDuplicateSlashes(url);
    }

    const { caseSensitive, ignoreTrailingSlash } =
      this.getRouteMatchingOptions();
    if (ignoreTrailingSlash) {
      url = this.trimLastSlash(url);
    }

    const { path } = safeDecodeURI(
      url,
      routerOptions.useSemicolonDelimiter ||
        initialConfig.useSemicolonDelimiter,
    );
    // Lower-cased once decoded, as the router does: "%E2%84%AA" (KELVIN
    // SIGN) only lower-cases to "k" then
    return caseSensitive ? path : path.toLowerCase();
  }
```

### 🔹 函式: `createMiddlewareFactory()`
- **變更前簽章 (Before)**: `createMiddlewareFactory(
    requestMethod: RequestMethod,
  )` (L1072~L1136)
- **變更後簽章 (After)**: `createMiddlewareFactory(
    requestMethod: RequestMethod,
  )` (L1072~L1152)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async createMiddlewareFactory(
    requestMethod: RequestMethod,
  ): Promise<(path: string, callback: Function) => any> {
    if (!this.isMiddieRegistered) {
      await this.registerMiddie();
    }
    return (path: string, callback: Function) => {
      const hasEndOfStringCharacter = path.endsWith('$');
      path = hasEndOfStringCharacter ? path.slice(0, -1) : path;

      let normalizedPath = LegacyRouteConverter.tryConvert(path);

      // Fallback to "*path" to support plugins like GraphQL
      normalizedPath = normalizedPath === '/*path' ? '*path' : normalizedPath;

      // Normalize the path to support the prefix if it set in application
      if (
        this._pathPrefix &&
        !normalizedPath.startsWith(this._pathPrefix) &&
        (normalizedPath === '/' || normalizedPath === '')
      ) {
        normalizedPath = `${this._pathPrefix}${normalizedPath}`;
        if (normalizedPath.endsWith('/')) {
          normalizedPath = `${normalizedPath}{*path}`;
        }
      }

      try {
        let { regexp: re } = pathToRegexp(normalizedPath);
        re = hasEndOfStringCharacter
          ? new RegExp(re.source + '$', re.flags)
          : re;

        // The following type assertion is valid as we use import('@fastify/middie') rather than require('@fastify/middie')
        // ref https://github.com/fastify/middie/pull/55
        this.instance.use(
          normalizedPath,
          (req: any, res: any, next: (err?: Error) => void) => {
            const queryParamsIndex = req.originalUrl.indexOf('?');
            let pathname =
              queryParamsIndex >= 0
                ? req.originalUrl.slice(0, queryParamsIndex)
                : req.originalUrl;

            pathname = this.sanitizeUrl(pathname);

            if (normalizedPath) {
              const pathToCheck = pathname.endsWith('/')
                ? pathname
                : `${pathname}/`;
              if (!re.exec(pathToCheck)) {
                return next();
              }
            }
            this.runMiddleware(callback, req, res, next);
          },
        );
      } catch (e) {
        if (e instanceof TypeError) {
          LegacyRouteConverter.printError(path);
        }
        throw e;
      }
    };
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async createMiddlewareFactory(
    requestMethod: RequestMethod,
  ): Promise<(path: string, callback: Function) => any> {
    if (!this.isMiddieRegistered) {
      await this.registerMiddie();
    }
    return (path: string, callback: Function) => {
      const hasEndOfStringCharacter = path.endsWith('$');
      path = hasEndOfStringCharacter ? path.slice(0, -1) : path;

      let normalizedPath = LegacyRouteConverter.tryConvert(path);

      // Fallback to "*path" to support plugins like GraphQL
      normalizedPath = normalizedPath === '/*path' ? '*path' : normalizedPath;

      // Normalize the path to support the prefix if it set in application
      if (
        this._pathPrefix &&
        !normalizedPath.startsWith(this._pathPrefix) &&
        (normalizedPath === '/' || normalizedPath === '')
      ) {
        normalizedPath = `${this._pathPrefix}${normalizedPath}`;
        if (normalizedPath.endsWith('/')) {
          normalizedPath = `${normalizedPath}{*path}`;
        }
      }

      try {
        let { regexp: re } = pathToRegexp(normalizedPath);
        re = hasEndOfStringCharacter
          ? new RegExp(re.source + '$', re.flags)
          : re;

        // A case-insensitive router lower-cases the decoded path, where some
        // characters only fold to ASCII ("%E2%84%AA", KELVIN SIGN, is routed
        // as "k"). The RegExp of @fastify/middie does not fold them, so on
        // such a router the middleware is registered for every path and the
        // path is only matched below.
        const { caseSensitive } = this.getRouteMatchingOptions();

        // The following type assertion is valid as we use import('@fastify/middie') rather than require('@fastify/middie')
        // ref https://github.com/fastify/middie/pull/55
        this.instance.use(
          caseSensitive ? normalizedPath : '/',
          (req: any, res: any, next: (err?: Error) => void) => {
            const queryParamsIndex = req.originalUrl.indexOf('?');
            let pathname =
              queryParamsIndex >= 0
                ? req.originalUrl.slice(0, queryParamsIndex)
                : req.originalUrl;

            pathname = this.sanitizeUrl(pathname);

            if (normalizedPath) {
              const pathToCheck = pathname.endsWith('/')
                ? pathname
                : `${pathname}/`;
              if (!re.exec(pathToCheck)) {
                return next();
              }
              if (!caseSensitive) {
                // Strips the path from "req.url", as @fastify/middie does
                // when it matches the path itself
                const suffixIndex = req.originalUrl.search(/[?#]/);
                req.url =
                  suffixIndex >= 0
                    ? `/${req.originalUrl.slice(suffixIndex)}`
                    : '/';
              }
            }
            this.runMiddleware(callback, req, res, next);
          },
        );
      } catch (e) {
        if (e instanceof TypeError) {
          LegacyRouteConverter.printError(path);
        }
        throw e;
      }
    };
  }
```


---

### 🔹 Commit #19: `1435ed22`
- **完整 Hash**: `1435ed22f4ce494cf9f95f6601fc8ab1310bf42c`
- **說明 (Ground Truth)**: fix(fastify): pass middleware rejections to the error handler
- **變更檔案數**: 1

#### 📄 檔案: `packages/platform-fastify/adapters/fastify-adapter.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:116, E:36, A:0) ➔ After(N:118, E:38, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 1, +Edges: 3, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `middleware (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `nextOnce` (FUNCTION_DEF)
  • + [新增節點] `runMiddleware` (FUNCTION_DEF)
  • - [移除節點] `callback (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `runMiddleware` ──[CALLS]──> `middleware (External/Unresolved)`
  • + [新增呼叫邊] `runMiddleware` ──[CALLS]──> `nextOnce`
  • + [新增呼叫邊] `nextOnce` ──[CALLS [guard: (completed)]]──> `next (External/Unresolved)`
  • - [移除呼叫邊] `createMiddlewareFactory` ──[CALLS]──> `callback (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `createMiddlewareFactory()`
- **變更前簽章 (Before)**: `createMiddlewareFactory(
    requestMethod: RequestMethod,
  )` (L1046~L1110)
- **變更後簽章 (After)**: `createMiddlewareFactory(
    requestMethod: RequestMethod,
  )` (L1046~L1110)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async createMiddlewareFactory(
    requestMethod: RequestMethod,
  ): Promise<(path: string, callback: Function) => any> {
    if (!this.isMiddieRegistered) {
      await this.registerMiddie();
    }
    return (path: string, callback: Function) => {
      const hasEndOfStringCharacter = path.endsWith('$');
      path = hasEndOfStringCharacter ? path.slice(0, -1) : path;

      let normalizedPath = LegacyRouteConverter.tryConvert(path);

      // Fallback to "*path" to support plugins like GraphQL
      normalizedPath = normalizedPath === '/*path' ? '*path' : normalizedPath;

      // Normalize the path to support the prefix if it set in application
      if (
        this._pathPrefix &&
        !normalizedPath.startsWith(this._pathPrefix) &&
        (normalizedPath === '/' || normalizedPath === '')
      ) {
        normalizedPath = `${this._pathPrefix}${normalizedPath}`;
        if (normalizedPath.endsWith('/')) {
          normalizedPath = `${normalizedPath}{*path}`;
        }
      }

      try {
        let { regexp: re } = pathToRegexp(normalizedPath);
        re = hasEndOfStringCharacter
          ? new RegExp(re.source + '$', re.flags)
          : re;

        // The following type assertion is valid as we use import('@fastify/middie') rather than require('@fastify/middie')
        // ref https://github.com/fastify/middie/pull/55
        this.instance.use(
          normalizedPath,
          (req: any, res: any, next: Function) => {
            const queryParamsIndex = req.originalUrl.indexOf('?');
            let pathname =
              queryParamsIndex >= 0
                ? req.originalUrl.slice(0, queryParamsIndex)
                : req.originalUrl;

            pathname = this.sanitizeUrl(pathname);

            if (normalizedPath) {
              const pathToCheck = pathname.endsWith('/')
                ? pathname
                : `${pathname}/`;
              if (!re.exec(pathToCheck)) {
                return next();
              }
            }
            return callback(req, res, next);
          },
        );
      } catch (e) {
        if (e instanceof TypeError) {
          LegacyRouteConverter.printError(path);
        }
        throw e;
      }
    };
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async createMiddlewareFactory(
    requestMethod: RequestMethod,
  ): Promise<(path: string, callback: Function) => any> {
    if (!this.isMiddieRegistered) {
      await this.registerMiddie();
    }
    return (path: string, callback: Function) => {
      const hasEndOfStringCharacter = path.endsWith('$');
      path = hasEndOfStringCharacter ? path.slice(0, -1) : path;

      let normalizedPath = LegacyRouteConverter.tryConvert(path);

      // Fallback to "*path" to support plugins like GraphQL
      normalizedPath = normalizedPath === '/*path' ? '*path' : normalizedPath;

      // Normalize the path to support the prefix if it set in application
      if (
        this._pathPrefix &&
        !normalizedPath.startsWith(this._pathPrefix) &&
        (normalizedPath === '/' || normalizedPath === '')
      ) {
        normalizedPath = `${this._pathPrefix}${normalizedPath}`;
        if (normalizedPath.endsWith('/')) {
          normalizedPath = `${normalizedPath}{*path}`;
        }
      }

      try {
        let { regexp: re } = pathToRegexp(normalizedPath);
        re = hasEndOfStringCharacter
          ? new RegExp(re.source + '$', re.flags)
          : re;

        // The following type assertion is valid as we use import('@fastify/middie') rather than require('@fastify/middie')
        // ref https://github.com/fastify/middie/pull/55
        this.instance.use(
          normalizedPath,
          (req: any, res: any, next: (err?: Error) => void) => {
            const queryParamsIndex = req.originalUrl.indexOf('?');
            let pathname =
              queryParamsIndex >= 0
                ? req.originalUrl.slice(0, queryParamsIndex)
                : req.originalUrl;

            pathname = this.sanitizeUrl(pathname);

            if (normalizedPath) {
              const pathToCheck = pathname.endsWith('/')
                ? pathname
                : `${pathname}/`;
              if (!re.exec(pathToCheck)) {
                return next();
              }
            }
            this.runMiddleware(callback, req, res, next);
          },
        );
      } catch (e) {
        if (e instanceof TypeError) {
          LegacyRouteConverter.printError(path);
        }
        throw e;
      }
    };
  }
```


---

### 🔹 Commit #20: `e419ff54`
- **完整 Hash**: `e419ff540b261ce23dde58e80b19daefa46e89ba`
- **說明 (Ground Truth)**: fix(microservices): limit the number of kafka header values
- **變更檔案數**: 2

#### 📄 檔案: `packages/microservices/errors/max-kafka-headers-exceeded.exception.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:1, E:0, A:0)
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
  • + [新增節點] `constructor` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `packages/microservices/serializers/kafka-request.serializer.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:7, E:6, A:0) ➔ After(N:8, E:6, A:0)
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
  • + [新增節點] `MAX_HEADER_VALUES` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `serialize()`
- **變更前簽章 (Before)**: `serialize(value: any)` (L23~L46)
- **變更後簽章 (After)**: `serialize(value: any)` (L28~L61)

#### ◀️ 變更前實作碼 (Before Implementation):
```
serialize(value: any): any {
    const isNotKafkaMessage =
      isNil(value) ||
      !isObject(value) ||
      (!('key' in value) && !('value' in value));

    // Serialize a copy, headers included: ClientKafka and ServerKafka write
    // correlation metadata into the returned headers, and the caller's record
    // may be frozen, reused or sent concurrently.
    const record = (isNotKafkaMessage ? { value } : value) as KafkaRequest;
    // Spreading a string or an array (as an echo handler may return them)
    // would turn each of its characters or items into a header
    const headers =
      isObject(record.headers) && !Array.isArray(record.headers)
        ? { ...record.headers }
        : {};
    const request: KafkaRequest = { ...record, headers };

    request.value = this.encode(request.value);
    if (!isNil(request.key)) {
      request.key = this.encode(request.key);
    }
    return request;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
serialize(value: any): any {
    const isNotKafkaMessage =
      isNil(value) ||
      !isObject(value) ||
      (!('key' in value) && !('value' in value));

    // Serialize a copy, headers included: ClientKafka and ServerKafka write
    // correlation metadata into the returned headers, and the caller's record
    // may be frozen, reused or sent concurrently.
    const record = (isNotKafkaMessage ? { value } : value) as KafkaRequest;
    // Spreading a string or an array (as an echo handler may return them)
    // would turn each of its characters or items into a header
    const headers =
      isObject(record.headers) && !Array.isArray(record.headers)
        ? record.headers
        : {};
    let headerValues = 0;
    for (const headerValue of Object.values(headers)) {
      headerValues += Array.isArray(headerValue) ? headerValue.length : 1;
    }
    if (headerValues > MAX_HEADER_VALUES) {
      throw new MaxKafkaHeadersExceededException(
        headerValues,
        MAX_HEADER_VALUES,
      );
    }
    const request: KafkaRequest = { ...record, headers: { ...headers } };

    request.value = this.encode(request.value);
    if (!isNil(request.key)) {
      request.key = this.encode(request.key);
    }
    return request;
  }
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/nest show 284ca7d54f97ac87308cd3c5c1a669f4f8b3ecec
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 284ca7d54f97ac87308cd3c5c1a669f4f8b3ecec~1 --file test_repos/nest/packages/microservices/client/client-nats.ts
   ```
