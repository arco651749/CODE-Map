# 🔬 CODE-Map 基準審查獨立驗證報告: `xstate`
> **技術生態**: `TypeScript (有限狀態機 / Actor 模型)`  
> **本地倉庫路徑**: `test_repos/xstate`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 30 Files  
> **報告生成時間**: 2026-10-20 21:40:42  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `14` / `30` | `46.7%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `9` / `30` | `30.0%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `7` / `30` | `23.3%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`23` / `30`** | **`76.7%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `30` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `016daa76`
- **完整 Hash**: `016daa76a45c4baaeade00034996f2617b45a7fa`
- **說明 (Ground Truth)**: fix(vue): update useSelector's selected value when the actor errors (#5812)
- **變更檔案數**: 1

#### 📄 檔案: `packages/xstate-vue/src/useSelector.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:11, E:8, A:0) ➔ After(N:12, E:10, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `error` (FUNCTION_DEF)
  • + [新增呼叫邊] `error` ──[CALLS]──> `updateSelectedIfChanged`
  • + [新增呼叫邊] `error` ──[CALLS]──> `selector (External/Unresolved)`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'updateSelectedIfChanged' 被深鎖在內部閉包 (scope:useSelector@after/packages/xstate-vue/src/useSelector.ts:L12C8)，外部無法調用！ (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `useSelector()`
- **變更前簽章 (Before)**: `function useSelector<
  TActor extends Pick<AnyActorRef, 'getSnapshot' | 'subscribe'> | undefined,
  T
>(
  actor: TActor | Ref<TActor>,
  selector: (
    snapshot: TActor extends` (L12~L55)
- **變更後簽章 (After)**: `function useSelector<
  TActor extends Pick<AnyActorRef, 'getSnapshot' | 'subscribe'> | undefined,
  T
>(
  actor: TActor | Ref<TActor>,
  selector: (
    snapshot: TActor extends` (L12~L58)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function useSelector<
  TActor extends Pick<AnyActorRef, 'getSnapshot' | 'subscribe'> | undefined,
  T
>(
  actor: TActor | Ref<TActor>,
  selector: (
    snapshot: TActor extends { getSnapshot(): infer TSnapshot }
      ? TSnapshot
      : undefined
  ) => T,
  compare: (a: T, b: T) => boolean = defaultCompare
): Ref<T> {
  const actorRefRef: Ref<TActor> = isRef(actor) ? actor : shallowRef(actor);
  const selected = shallowRef(selector(actorRefRef.value?.getSnapshot()));

  const updateSelectedIfChanged = (nextSelected: T) => {
    if (!compare(selected.value, nextSelected)) {
      selected.value = nextSelected;
    }
  };

  watch(
    actorRefRef,
    (newActor, _, onCleanup) => {
      selected.value = selector(newActor?.getSnapshot());
      if (!newActor) {
        return;
      }
      const sub = newActor.subscribe({
        next: (emitted) => {
          updateSelectedIfChanged(selector(emitted));
        },
        error: noop,
        complete: noop
      });
      onCleanup(() => sub.unsubscribe());
    },
    {
      immediate: true
    }
  );

  return selected;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function useSelector<
  TActor extends Pick<AnyActorRef, 'getSnapshot' | 'subscribe'> | undefined,
  T
>(
  actor: TActor | Ref<TActor>,
  selector: (
    snapshot: TActor extends { getSnapshot(): infer TSnapshot }
      ? TSnapshot
      : undefined
  ) => T,
  compare: (a: T, b: T) => boolean = defaultCompare
): Ref<T> {
  const actorRefRef: Ref<TActor> = isRef(actor) ? actor : shallowRef(actor);
  const selected = shallowRef(selector(actorRefRef.value?.getSnapshot()));

  const updateSelectedIfChanged = (nextSelected: T) => {
    if (!compare(selected.value, nextSelected)) {
      selected.value = nextSelected;
    }
  };

  watch(
    actorRefRef,
    (newActor, _, onCleanup) => {
      selected.value = selector(newActor?.getSnapshot());
      if (!newActor) {
        return;
      }
      const sub = newActor.subscribe({
        next: (emitted) => {
          updateSelectedIfChanged(selector(emitted));
        },
        error: () => {
          // the error snapshot is not delivered through `next`
          updateSelectedIfChanged(selector(newActor.getSnapshot()));
        },
        complete: noop
      });
      onCleanup(() => sub.unsubscribe());
    },
    {
      immediate: true
    }
  );

  return selected;
}
```


---

### 🔹 Commit #02: `78431d69`
- **完整 Hash**: `78431d69939969cf9355ec55439b53413bd404a1`
- **說明 (Ground Truth)**: fix(core): stop child actors when an invoked actor's error is unhandled (#5792)
- **變更檔案數**: 1

#### 📄 檔案: `packages/core/src/stateUtils.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:82, E:124, A:0) ➔ After(N:82, E:124, A:0)
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

### 🔹 函式: `macrostep()`
- **變更前簽章 (Before)**: `function macrostep(
  snapshot: AnyMachineSnapshot,
  event: EventObject,
  actorScope: AnyActorScope,
  internalQueue: AnyEventObject[]
):` (L1675~L1807)
- **變更後簽章 (After)**: `function macrostep(
  snapshot: AnyMachineSnapshot,
  event: EventObject,
  actorScope: AnyActorScope,
  internalQueue: AnyEventObject[]
):` (L1675~L1810)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function macrostep(
  snapshot: AnyMachineSnapshot,
  event: EventObject,
  actorScope: AnyActorScope,
  internalQueue: AnyEventObject[]
): {
  snapshot: typeof snapshot;
  microsteps: Microstep[];
} {
  if (isDevelopment && event.type === WILDCARD) {
    throw new Error(`An event cannot have the wildcard type ('${WILDCARD}')`);
  }

  let nextSnapshot = snapshot;
  const microsteps: Microstep[] = [];

  function addMicrostep(
    step: Microstep,
    event: AnyEventObject,
    transitions: AnyTransitionDefinition[]
  ) {
    actorScope.system._sendInspectionEvent({
      type: '@xstate.microstep',
      actorRef: actorScope.self,
      event,
      snapshot: step[0],
      _transitions: transitions
    });
    microsteps.push(step);
  }

  // Handle stop event
  if (event.type === XSTATE_STOP) {
    nextSnapshot = cloneMachineSnapshot(
      stopChildren(nextSnapshot, event, actorScope),
      {
        status: 'stopped'
      }
    );
    addMicrostep([nextSnapshot, []], event, []);
    return {
      snapshot: nextSnapshot,
      microsteps
    };
  }

  let nextEvent = event;

  // Assume the state is at rest (no raised events)
  // Determine the next state based on the next microstep
  if (nextEvent.type !== XSTATE_INIT) {
    const currentEvent = nextEvent;
    const isErr = isErrorActorEvent(currentEvent);

    const transitions = selectTransitions(currentEvent, nextSnapshot);

    if (isErr && !transitions.length) {
      // TODO: we should likely only allow transitions selected by very explicit descriptors
      // `*` shouldn't be matched, likely `xstate.error.*` shouldn't be either
      // similarly `xstate.error.actor.*` and `xstate.error.actor.todo.*` have to be considered too
      nextSnapshot = cloneMachineSnapshot<typeof snapshot>(snapshot, {
        status: 'error',
        error: currentEvent.error
      });
      addMicrostep([nextSnapshot, []], currentEvent, []);
      return {
        snapshot: nextSnapshot,
        microsteps
      };
    }
    const step = microstep(
      transitions,
      snapshot,
      actorScope,
      nextEvent,
      false, // isInitial
      internalQueue
    );
    nextSnapshot = step[0];
    addMicrostep(step, currentEvent, transitions);
  }

  let shouldSelectEventlessTransitions = true;
  const maxIterations = snapshot.machine.options?.maxIterations ?? Infinity;
  let iterationCount = 0;

  while (nextSnapshot.status === 'active') {
    iterationCount++;
    if (iterationCount > maxIterations) {
      throw new Error(
        `Infinite loop detected: the machine has processed more than ${maxIterations} microsteps without reaching a stable state. This usually happens when there's a cycle of transitions (e.g., eventless transitions or raised events causing state A -> B -> C -> A).`
      );
    }

    let enabledTransitions: AnyTransitionDefinition[] =
      shouldSelectEventlessTransitions
        ? selectEventlessTransitions(nextSnapshot, nextEvent)
        : [];

    // eventless transitions should always be selected after selecting *regular* transitions
    // by assigning `undefined` to `previousState` we ensure that `shouldSelectEventlessTransitions` gets always computed to true in such a case
    const previousState = enabledTransitions.length ? nextSnapshot : undefined;

    if (!enabledTransitions.length) {
      if (!internalQueue.length) {
        break;
      }
      nextEvent = internalQueue.shift()!;
      enabledTransitions = selectTransitions(nextEvent, nextSnapshot);
    }

    const step = microstep(
      enabledTransitions,
      nextSnapshot,
      actorScope,
      nextEvent,
      false,
      internalQueue
    );
    nextSnapshot = step[0];
    shouldSelectEventlessTransitions = nextSnapshot !== previousState;
    addMicrostep(step, nextEvent, enabledTransitions);
  }

  if (nextSnapshot.status !== 'active') {
    stopChildren(nextSnapshot, nextEvent, actorScope);
  }

  return {
    snapshot: nextSnapshot,
    microsteps
  };
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function macrostep(
  snapshot: AnyMachineSnapshot,
  event: EventObject,
  actorScope: AnyActorScope,
  internalQueue: AnyEventObject[]
): {
  snapshot: typeof snapshot;
  microsteps: Microstep[];
} {
  if (isDevelopment && event.type === WILDCARD) {
    throw new Error(`An event cannot have the wildcard type ('${WILDCARD}')`);
  }

  let nextSnapshot = snapshot;
  const microsteps: Microstep[] = [];

  function addMicrostep(
    step: Microstep,
    event: AnyEventObject,
    transitions: AnyTransitionDefinition[]
  ) {
    actorScope.system._sendInspectionEvent({
      type: '@xstate.microstep',
      actorRef: actorScope.self,
      event,
      snapshot: step[0],
      _transitions: transitions
    });
    microsteps.push(step);
  }

  // Handle stop event
  if (event.type === XSTATE_STOP) {
    nextSnapshot = cloneMachineSnapshot(
      stopChildren(nextSnapshot, event, actorScope),
      {
        status: 'stopped'
      }
    );
    addMicrostep([nextSnapshot, []], event, []);
    return {
      snapshot: nextSnapshot,
      microsteps
    };
  }

  let nextEvent = event;

  // Assume the state is at rest (no raised events)
  // Determine the next state based on the next microstep
  if (nextEvent.type !== XSTATE_INIT) {
    const currentEvent = nextEvent;
    const isErr = isErrorActorEvent(currentEvent);

    const transitions = selectTransitions(currentEvent, nextSnapshot);

    if (isErr && !transitions.length) {
      // TODO: we should likely only allow transitions selected by very explicit descriptors
      // `*` shouldn't be matched, likely `xstate.error.*` shouldn't be either
      // similarly `xstate.error.actor.*` and `xstate.error.actor.todo.*` have to be considered too
      nextSnapshot = cloneMachineSnapshot<typeof snapshot>(
        stopChildren(nextSnapshot, currentEvent, actorScope),
        {
          status: 'error',
          error: currentEvent.error
        }
      );
      addMicrostep([nextSnapshot, []], currentEvent, []);
      return {
        snapshot: nextSnapshot,
        microsteps
      };
    }
    const step = microstep(
      transitions,
      snapshot,
      actorScope,
      nextEvent,
      false, // isInitial
      internalQueue
    );
    nextSnapshot = step[0];
    addMicrostep(step, currentEvent, transitions);
  }

  let shouldSelectEventlessTransitions = true;
  const maxIterations = snapshot.machine.options?.maxIterations ?? Infinity;
  let iterationCount = 0;

  while (nextSnapshot.status === 'active') {
    iterationCount++;
    if (iterationCount > maxIterations) {
      throw new Error(
        `Infinite loop detected: the machine has processed more than ${maxIterations} microsteps without reaching a stable state. This usually happens when there's a cycle of transitions (e.g., eventless transitions or raised events causing state A -> B -> C -> A).`
      );
    }

    let enabledTransitions: AnyTransitionDefinition[] =
      shouldSelectEventlessTransitions
        ? selectEventlessTransitions(nextSnapshot, nextEvent)
        : [];

    // eventless transitions should always be selected after selecting *regular* transitions
    // by assigning `undefined` to `previousState` we ensure that `shouldSelectEventlessTransitions` gets always computed to true in such a case
    const previousState = enabledTransitions.length ? nextSnapshot : undefined;

    if (!enabledTransitions.length) {
      if (!internalQueue.length) {
        break;
      }
      nextEvent = internalQueue.shift()!;
      enabledTransitions = selectTransitions(nextEvent, nextSnapshot);
    }

    const step = microstep(
      enabledTransitions,
      nextSnapshot,
      actorScope,
      nextEvent,
      false,
      internalQueue
    );
    nextSnapshot = step[0];
    shouldSelectEventlessTransitions = nextSnapshot !== previousState;
    addMicrostep(step, nextEvent, enabledTransitions);
  }

  if (nextSnapshot.status !== 'active') {
    stopChildren(nextSnapshot, nextEvent, actorScope);
  }

  return {
    snapshot: nextSnapshot,
    microsteps
  };
}
```


---

### 🔹 Commit #03: `397b4253`
- **完整 Hash**: `397b42536f53b899e6914219ac829616d5100823`
- **說明 (Ground Truth)**: Fix machine snapshot shape after initialization errors (#5678)
- **變更檔案數**: 1

#### 📄 檔案: `packages/core/src/StateMachine.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:37, E:29, A:0) ➔ After(N:38, E:31, A:0)
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
  • + [新增節點] `cloneMachineSnapshot (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `getInitialSnapshot` ──[CALLS]──> `createMachineSnapshot (External/Unresolved)`
  • + [新增呼叫邊] `getInitialSnapshot` ──[CALLS]──> `cloneMachineSnapshot (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `getInitialSnapshot()`
- **變更前簽章 (Before)**: `getInitialSnapshot(
    actorScope: ActorScope<
      MachineSnapshot<
        TContext,
        TEvent,
        TChildren,
        TStateValue,
        TTag,
        TOutput,
        TMeta,
        TStateSchema
      >,
      TEvent,
      AnyActorSystem,
      TEmitted
    >,
    input?: TInput
  )` (L412~L462)
- **變更後簽章 (After)**: `getInitialSnapshot(
    actorScope: ActorScope<
      MachineSnapshot<
        TContext,
        TEvent,
        TChildren,
        TStateValue,
        TTag,
        TOutput,
        TMeta,
        TStateSchema
      >,
      TEvent,
      AnyActorSystem,
      TEmitted
    >,
    input?: TInput
  )` (L413~L479)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public getInitialSnapshot(
    actorScope: ActorScope<
      MachineSnapshot<
        TContext,
        TEvent,
        TChildren,
        TStateValue,
        TTag,
        TOutput,
        TMeta,
        TStateSchema
      >,
      TEvent,
      AnyActorSystem,
      TEmitted
    >,
    input?: TInput
  ): MachineSnapshot<
    TContext,
    TEvent,
    TChildren,
    TStateValue,
    TTag,
    TOutput,
    TMeta,
    TStateSchema
  > {
    const initEvent = createInitEvent(input) as unknown as TEvent; // TODO: fix;
    const internalQueue: AnyEventObject[] = [];
    const preInitialState = this._getPreInitialState(
      actorScope,
      initEvent,
      internalQueue
    );
    const [nextState] = initialMicrostep(
      this.root,
      preInitialState,
      actorScope,
      initEvent,
      internalQueue
    );

    const { snapshot: macroState } = macrostep(
      nextState,
      initEvent as AnyEventObject,
      actorScope,
      internalQueue
    );

    return macroState as SnapshotFrom<this>;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public getInitialSnapshot(
    actorScope: ActorScope<
      MachineSnapshot<
        TContext,
        TEvent,
        TChildren,
        TStateValue,
        TTag,
        TOutput,
        TMeta,
        TStateSchema
      >,
      TEvent,
      AnyActorSystem,
      TEmitted
    >,
    input?: TInput
  ): MachineSnapshot<
    TContext,
    TEvent,
    TChildren,
    TStateValue,
    TTag,
    TOutput,
    TMeta,
    TStateSchema
  > {
    const initEvent = createInitEvent(input) as unknown as TEvent; // TODO: fix;
    const internalQueue: AnyEventObject[] = [];
    let snapshot = createMachineSnapshot(
      {
        context:
          typeof this.config.context !== 'function' && this.config.context
            ? this.config.context
            : ({} as TContext),
        _nodes: [this.root],
        children: {},
        status: 'active'
      },
      this
    ) as ReturnType<typeof this._getPreInitialState>;

    try {
      snapshot = this._getPreInitialState(actorScope, initEvent, internalQueue);
      const [nextState] = initialMicrostep(
        this.root,
        snapshot,
        actorScope,
        initEvent,
        internalQueue
      );

      const { snapshot: macroState } = macrostep(
        nextState,
        initEvent as AnyEventObject,
        actorScope,
        internalQueue
      );

      return macroState as SnapshotFrom<this>;
    } catch (error) {
      return cloneMachineSnapshot(snapshot, {
        status: 'error',
        error
      }) as SnapshotFrom<this>;
    }
  }
```


---

### 🔹 Commit #04: `345e04ce`
- **完整 Hash**: `345e04ce66963c2a5a2a879bb4928a1b179de7f6`
- **說明 (Ground Truth)**: fix(core): don't throw when warning about unserializable event sent to stopped actor (#5603)
- **變更檔案數**: 1

#### 📄 檔案: `packages/core/src/createActor.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:51, E:21, A:0) ➔ After(N:52, E:22, A:0)
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
  • + [新增節點] `String (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `_send` ──[CALLS [guard: (this._processingStatus === ProcessingStatus.Stopped)]]──> `String (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_send()`
- **變更前簽章 (Before)**: `_send(event: EventFromLogic<TLogic>)` (L728~L742)
- **變更後簽章 (After)**: `_send(event: EventFromLogic<TLogic>)` (L728~L747)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public _send(event: EventFromLogic<TLogic>) {
    if (this._processingStatus === ProcessingStatus.Stopped) {
      // do nothing
      if (isDevelopment) {
        const eventString = JSON.stringify(event);

        console.warn(
          `Event "${event.type}" was sent to stopped actor "${this.id} (${this.sessionId})". This actor has already reached its final state, and will not transition.\nEvent: ${eventString}`
        );
      }
      return;
    }

    this.mailbox.enqueue(event);
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public _send(event: EventFromLogic<TLogic>) {
    if (this._processingStatus === ProcessingStatus.Stopped) {
      // do nothing
      if (isDevelopment) {
        let eventString: string;
        try {
          eventString = JSON.stringify(event);
        } catch {
          eventString = String(event);
        }

        console.warn(
          `Event "${event.type}" was sent to stopped actor "${this.id} (${this.sessionId})". This actor has already reached its final state, and will not transition.\nEvent: ${eventString}`
        );
      }
      return;
    }

    this.mailbox.enqueue(event);
  }
```


---

### 🔹 Commit #05: `830db8b6`
- **完整 Hash**: `830db8b6b4ac81331bdcae44aa7ec522fa959960`
- **說明 (Ground Truth)**: fix(core): prevent 'systemId already exists' in pure transition functions (#5575)
- **變更檔案數**: 1

#### 📄 檔案: `packages/core/src/getNextSnapshot.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:9, E:3, A:0) ➔ After(N:10, E:4, A:0)
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
  • + [新增節點] `createSystem (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `createInertActorScope` ──[CALLS]──> `createSystem (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `createInertActorScope()`
- **變更前簽章 (Before)**: `function createInertActorScope<T extends AnyActorLogic>(
  actorLogic: T
): AnyActorScope` (L13~L35)
- **變更後簽章 (After)**: `function createInertActorScope<T extends AnyActorLogic>(
  actorLogic: T
): AnyActorScope` (L14~L48)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createInertActorScope<T extends AnyActorLogic>(
  actorLogic: T
): AnyActorScope {
  const self = createActor(actorLogic as AnyActorLogic);
  const inertActorScope: ActorScope<
    SnapshotFrom<T>,
    EventFromLogic<T>,
    any,
    EmittedFrom<T>
  > = {
    self,
    defer: () => {},
    id: '',
    logger: () => {},
    sessionId: '',
    stopChild: () => {},
    system: self.system,
    emit: () => {},
    actionExecutor: () => {}
  };

  return inertActorScope;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createInertActorScope<T extends AnyActorLogic>(
  actorLogic: T
): AnyActorScope {
  const self = createActor(actorLogic as AnyActorLogic);
  // The Actor constructor eagerly calls `getInitialSnapshot` during `_initState`,
  // which can register child actors with `systemId` in `self.system`.
  // Replace `self.system` with a fresh system so that child actors spawned by
  // the *caller's* explicit `getInitialSnapshot` / `transition` call register
  // into a clean system and do not collide with those from the eager
  // construction call.  This is what makes `initialTransition(machine)` safe
  // even when invoked actors carry a `systemId`.
  const freshSystem = createSystem(self, {
    clock: self.system._clock,
    logger: self.system._logger
  });
  (self as any).system = freshSystem;
  const inertActorScope: ActorScope<
    SnapshotFrom<T>,
    EventFromLogic<T>,
    any,
    EmittedFrom<T>
  > = {
    self,
    defer: () => {},
    id: '',
    logger: () => {},
    sessionId: '',
    stopChild: () => {},
    system: freshSystem,
    emit: () => {},
    actionExecutor: () => {}
  };

  return inertActorScope;
}
```


---

### 🔹 Commit #06: `8a535310`
- **完整 Hash**: `8a5353105522aaee7a4f7031136372edec327a79`
- **說明 (Ground Truth)**: fix(core): fall back to wildcard descriptors when exact guard fails (#5548)
- **變更檔案數**: 1

#### 📄 檔案: `packages/core/src/stateUtils.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:81, E:124, A:0) ➔ After(N:82, E:124, A:0)
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
  • + [新增節點] `wildcardCandidates` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `getCandidates()`
- **變更前簽章 (Before)**: `function getCandidates<TEvent extends EventObject>(
  stateNode: StateNode<any, TEvent>,
  receivedEventType: TEvent['type']
): Array<TransitionDefinition<any, TEvent>>` (L212~L226)
- **變更後簽章 (After)**: `function getCandidates<TEvent extends EventObject>(
  stateNode: StateNode<any, TEvent>,
  receivedEventType: TEvent['type']
): Array<TransitionDefinition<any, TEvent>>` (L212~L229)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function getCandidates<TEvent extends EventObject>(
  stateNode: StateNode<any, TEvent>,
  receivedEventType: TEvent['type']
): Array<TransitionDefinition<any, TEvent>> {
  const candidates =
    stateNode.transitions.get(receivedEventType) ||
    [...stateNode.transitions.keys()]
      .filter((eventDescriptor) =>
        matchesEventDescriptor(receivedEventType, eventDescriptor)
      )
      .sort((a, b) => b.length - a.length)
      .flatMap((key) => stateNode.transitions.get(key)!);

  return candidates;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function getCandidates<TEvent extends EventObject>(
  stateNode: StateNode<any, TEvent>,
  receivedEventType: TEvent['type']
): Array<TransitionDefinition<any, TEvent>> {
  const exactMatch = stateNode.transitions.get(receivedEventType);
  const wildcardCandidates = [...stateNode.transitions.keys()]
    .filter(
      (eventDescriptor) =>
        eventDescriptor !== receivedEventType &&
        matchesEventDescriptor(receivedEventType, eventDescriptor)
    )
    .sort((a, b) => b.length - a.length)
    .flatMap((key) => stateNode.transitions.get(key)!);

  return exactMatch
    ? [...exactMatch, ...wildcardCandidates]
    : wildcardCandidates;
}
```


---

### 🔹 Commit #07: `41c0a5a2`
- **完整 Hash**: `41c0a5a2878713bde019c61099f9486fae2c70f8`
- **說明 (Ground Truth)**: fix(core): resolve children snapshot union pollution for typed invoke ids (#5516)
- **變更檔案數**: 2

#### 📄 檔案: `packages/core/src/setup.ts`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:5, E:1, A:0) ➔ After(N:5, E:1, A:0)
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

#### 📄 檔案: `packages/core/src/types.ts`
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

### 🔹 Commit #08: `f79ea13f`
- **完整 Hash**: `f79ea13febe44956d309811a64b9b79f4f3d9295`
- **說明 (Ground Truth)**: [core] Fix route string guard resolution (#5525)
- **變更檔案數**: 1

#### 📄 檔案: `packages/core/src/stateUtils.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:81, E:124, A:0) ➔ After(N:81, E:124, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 2, +Edges: 1, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `and (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `routeMatches` (FUNCTION_DEF)
  • - [移除節點] `routeGuard` (FUNCTION_DEF)
  • - [移除節點] `userGuard (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `collectRoutes` ──[CALLS [guard: (sn.config.route && sn.config.id)]]──> `and (External/Unresolved)`
  • - [移除呼叫邊] `routeGuard` ──[CALLS]──> `userGuard (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `formatRouteTransitions()`
- **變更前簽章 (Before)**: `function formatRouteTransitions(rootStateNode: AnyStateNode): void` (L391~L432)
- **變更後簽章 (After)**: `function formatRouteTransitions(rootStateNode: AnyStateNode): void` (L391~L420)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function formatRouteTransitions(rootStateNode: AnyStateNode): void {
  const routeTransitions: AnyTransitionDefinition[] = [];
  const collectRoutes = (states: Record<string, AnyStateNode>) => {
    Object.values(states).forEach((sn) => {
      if (sn.config.route && sn.config.id) {
        const routeId = sn.config.id;
        const userGuard = sn.config.route.guard;
        const routeGuard = (
          args: { context: any; event: any },
          params: any
        ) => {
          if (args.event.to !== `#${routeId}`) {
            return false;
          }
          if (!userGuard) {
            return true;
          }
          if (typeof userGuard === 'function') {
            return userGuard(args, params);
          }
          return true;
        };
        const transition: AnyTransitionConfig = {
          ...sn.config.route,
          guard: routeGuard,
          target: `#${routeId}`
        };

        routeTransitions.push(
          formatTransition(rootStateNode, 'xstate.route', transition)
        );
      }
      if (sn.states) {
        collectRoutes(sn.states);
      }
    });
  };
  collectRoutes(rootStateNode.states);
  if (routeTransitions.length > 0) {
    rootStateNode.transitions.set('xstate.route', routeTransitions);
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function formatRouteTransitions(rootStateNode: AnyStateNode): void {
  const routeTransitions: AnyTransitionDefinition[] = [];
  const collectRoutes = (states: Record<string, AnyStateNode>) => {
    Object.values(states).forEach((sn) => {
      if (sn.config.route && sn.config.id) {
        const routeId = sn.config.id;
        const userGuard = sn.config.route.guard;
        const routeMatches = ({ event }: { event: any }) =>
          event.to === `#${routeId}`;

        const transition: AnyTransitionConfig = {
          ...sn.config.route,
          guard: userGuard ? and([routeMatches, userGuard]) : routeMatches,
          target: `#${routeId}`
        };

        routeTransitions.push(
          formatTransition(rootStateNode, 'xstate.route', transition)
        );
      }
      if (sn.states) {
        collectRoutes(sn.states);
      }
    });
  };
  collectRoutes(rootStateNode.states);
  if (routeTransitions.length > 0) {
    rootStateNode.transitions.set('xstate.route', routeTransitions);
  }
}
```

### 🔹 函式: `collectRoutes()`
- **變更前簽章 (Before)**: `collectRoutes(states: Record<string, AnyStateNode>)` (L393~L427)
- **變更後簽章 (After)**: `collectRoutes(states: Record<string, AnyStateNode>)` (L393~L415)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(states: Record<string, AnyStateNode>) => {
    Object.values(states).forEach((sn) => {
      if (sn.config.route && sn.config.id) {
        const routeId = sn.config.id;
        const userGuard = sn.config.route.guard;
        const routeGuard = (
          args: { context: any; event: any },
          params: any
        ) => {
          if (args.event.to !== `#${routeId}`) {
            return false;
          }
          if (!userGuard) {
            return true;
          }
          if (typeof userGuard === 'function') {
            return userGuard(args, params);
          }
          return true;
        };
        const transition: AnyTransitionConfig = {
          ...sn.config.route,
          guard: routeGuard,
          target: `#${routeId}`
        };

        routeTransitions.push(
          formatTransition(rootStateNode, 'xstate.route', transition)
        );
      }
      if (sn.states) {
        collectRoutes(sn.states);
      }
    });
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(states: Record<string, AnyStateNode>) => {
    Object.values(states).forEach((sn) => {
      if (sn.config.route && sn.config.id) {
        const routeId = sn.config.id;
        const userGuard = sn.config.route.guard;
        const routeMatches = ({ event }: { event: any }) =>
          event.to === `#${routeId}`;

        const transition: AnyTransitionConfig = {
          ...sn.config.route,
          guard: userGuard ? and([routeMatches, userGuard]) : routeMatches,
          target: `#${routeId}`
        };

        routeTransitions.push(
          formatTransition(rootStateNode, 'xstate.route', transition)
        );
      }
      if (sn.states) {
        collectRoutes(sn.states);
      }
    });
  }
```


---

### 🔹 Commit #09: `ca8306f8`
- **完整 Hash**: `ca8306f865475fa0404c419730a24e3a5e392521`
- **說明 (Ground Truth)**: Actor select (#5299)
- **變更檔案數**: 2

#### 📄 檔案: `packages/core/src/createActor.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:46, E:17, A:0) ➔ After(N:51, E:21, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 0, +Edges: 4, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `equalityFn (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `select` (FUNCTION_DEF)
  • + [新增節點] `get` (FUNCTION_DEF)
  • + [新增節點] `subscribe` (FUNCTION_DEF)
  • + [新增節點] `selector (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `subscribe` ──[CALLS]──> `toObserver (External/Unresolved)`
  • + [新增呼叫邊] `subscribe` ──[CALLS]──> `selector (External/Unresolved)`
  • + [新增呼叫邊] `subscribe` ──[CALLS [guard: (!equalityFn(previousSelected, nextSelected))]]──> `equalityFn (External/Unresolved)`
  • + [新增呼叫邊] `get` ──[CALLS]──> `selector (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `packages/core/src/types.ts`
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

### 🔹 Commit #10: `3b8c68e2`
- **完整 Hash**: `3b8c68e20057885f19b8897f4b4cb29380e8f7de`
- **說明 (Ground Truth)**: [@xstate/store] Add event persistence (#5479)
- **變更檔案數**: 1

#### 📄 檔案: `packages/xstate-store/src/persist.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:26, E:14, A:0) ➔ After(N:39, E:28, A:0)
- **差分統計**: +Nodes: 17, -Nodes: 4, +Edges: 22, -Edges: 8, ΔFuncs: 6, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `serializeEventValue` (FUNCTION_DEF)
  • + [新增節點] `persistEffect` (FUNCTION_DEF)
  • + [新增節點] `writeSnapshotToStorage` (FUNCTION_DEF)
  • + [新增節點] `deserializeSnapshotValue` (FUNCTION_DEF)
  • + [新增節點] `serializeSnapshotValue` (FUNCTION_DEF)
  • + [新增節點] `persistEventFromLogic` (FUNCTION_DEF)
  • + [新增節點] `deserializeEventValue` (FUNCTION_DEF)
  • + [新增節點] `transition` (FUNCTION_DEF)
  • + [新增節點] `isEventStrategy` (FUNCTION_DEF)
  • + [新增節點] `migrateEventsIfNeeded` (FUNCTION_DEF)
  • + [新增節點] `persistEffect` (FUNCTION_DEF)
  • + [新增節點] `replayEvents` (FUNCTION_DEF)
  • + [新增節點] `writeEventsToStorage` (FUNCTION_DEF)
  • + [新增節點] `isHydrated` (FUNCTION_DEF)
  • + [新增節點] `getInitialSnapshot` (FUNCTION_DEF)
  • _... 以及其餘 36 項拓樸變更_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'replayEvents' 被深鎖在內部閉包 (scope:persistEventFromLogic@after/packages/xstate-store/src/persist.ts:L467C1)，外部無法調用！ (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `persistEffect()`
- **變更前簽章 (Before)**: `persistEffect()` (L327~L329)
- **變更後簽章 (After)**: `persistEffect()` (L454~L456)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
        writeToStorage(internals, nextSnapshot.context);
      }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
        writeSnapshotToStorage(internals as any, nextSnapshot.context);
      }
```

### 🔹 函式: `flush()`
- **變更前簽章 (Before)**: `flush()` (L160~L169)
- **變更後簽章 (After)**: `flush()` (L272~L296)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
      if (internals.flushTimeoutId !== null) {
        clearTimeout(internals.flushTimeoutId);
        internals.flushTimeoutId = null;
      }
      if (internals.pendingContext !== null) {
        writeToStorage(internals, internals.pendingContext as TContext);
        internals.pendingContext = null;
      }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
      if (internals.flushTimeoutId !== null) {
        clearTimeout(internals.flushTimeoutId);
        internals.flushTimeoutId = null;
      }
      if (isEventStrategy(options)) {
        if (internals.pendingEvents !== null) {
          writeEventsToStorage(
            internals,
            internals.pendingEvents,
            internals.pendingCheckpoint
          );
          internals.pendingEvents = null;
          internals.pendingCheckpoint = null;
        }
      } else {
        if (internals.pendingContext !== null) {
          writeSnapshotToStorage(
            internals as any,
            internals.pendingContext as TContext
          );
          internals.pendingContext = null;
        }
      }
    }
```

### 🔹 函式: `getInitialSnapshot()`
- **變更前簽章 (Before)**: `getInitialSnapshot()` (L190~L244)
- **變更後簽章 (After)**: `getInitialSnapshot()` (L317~L371)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
      const baseSnapshot = logic.getInitialSnapshot();

      if (options.skipHydration) {
        return {
          ...baseSnapshot,
          _persist: { hydrated: false },
          [PERSIST_INTERNALS]: internals
        };
      }

      // Attempt sync read
      try {
        const storedValue = storage.getItem(options.name);

        // Async storage — can't hydrate synchronously
        if (storedValue instanceof Promise) {
          return {
            ...baseSnapshot,
            _persist: { hydrated: false },
            [PERSIST_INTERNALS]: internals
          };
        }

        if (storedValue === null) {
          return {
            ...baseSnapshot,
            _persist: { hydrated: true },
            [PERSIST_INTERNALS]: internals
          };
        }

        const parsed = deserializeValue(options, storedValue);
        const persistedContext = migrateIfNeeded(options, parsed);
        const mergedContext = mergeContext(
          options,
          persistedContext,
          baseSnapshot.context
        );

        return {
          ...baseSnapshot,
          context: mergedContext,
          _persist: { hydrated: true },
          [PERSIST_INTERNALS]: internals
        };
      } catch (err) {
        options.onError?.(err);
        return {
          ...baseSnapshot,
          _persist: { hydrated: true },
          [PERSIST_INTERNALS]: internals
        };
      }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
      const baseSnapshot = logic.getInitialSnapshot();

      if (options.skipHydration) {
        return {
          ...baseSnapshot,
          _persist: { hydrated: false },
          [PERSIST_INTERNALS]: internals
        };
      }

      // Attempt sync read
      try {
        const storedValue = storage.getItem(options.name);

        // Async storage — can't hydrate synchronously
        if (storedValue instanceof Promise) {
          return {
            ...baseSnapshot,
            _persist: { hydrated: false },
            [PERSIST_INTERNALS]: internals
          };
        }

        if (storedValue === null) {
          return {
            ...baseSnapshot,
            _persist: { hydrated: true },
            [PERSIST_INTERNALS]: internals
          };
        }

        const parsed = deserializeSnapshotValue(options, storedValue);
        const persistedContext = migrateSnapshotIfNeeded(options, parsed);
        const mergedContext = mergeContext(
          options,
          persistedContext,
          baseSnapshot.context
        );

        return {
          ...baseSnapshot,
          context: mergedContext,
          _persist: { hydrated: true },
          [PERSIST_INTERNALS]: internals
        };
      } catch (err) {
        options.onError?.(err);
        return {
          ...baseSnapshot,
          _persist: { hydrated: true },
          [PERSIST_INTERNALS]: internals
        };
      }
    }
```

### 🔹 函式: `createInternals()`
- **變更前簽章 (Before)**: `function createInternals<TContext>(
  options: PersistOptions<TContext, any>
): PersistInternals<TContext>` (L150~L173)
- **變更後簽章 (After)**: `function createInternals<TContext, TEvent extends EventObject>(
  options: PersistOptions<TContext, TEvent>
): PersistInternals<TContext, TEvent>` (L260~L300)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createInternals<TContext>(
  options: PersistOptions<TContext, any>
): PersistInternals<TContext> {
  const storage = getStorage(options);

  const internals: PersistInternals<TContext> = {
    options,
    storage,
    pendingContext: null,
    flushTimeoutId: null,
    flush: () => {
      if (internals.flushTimeoutId !== null) {
        clearTimeout(internals.flushTimeoutId);
        internals.flushTimeoutId = null;
      }
      if (internals.pendingContext !== null) {
        writeToStorage(internals, internals.pendingContext as TContext);
        internals.pendingContext = null;
      }
    }
  };

  return internals;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createInternals<TContext, TEvent extends EventObject>(
  options: PersistOptions<TContext, TEvent>
): PersistInternals<TContext, TEvent> {
  const storage = getStorage(options);

  const internals: PersistInternals<TContext, TEvent> = {
    options,
    storage,
    pendingContext: null,
    pendingEvents: null,
    pendingCheckpoint: null,
    flushTimeoutId: null,
    flush: () => {
      if (internals.flushTimeoutId !== null) {
        clearTimeout(internals.flushTimeoutId);
        internals.flushTimeoutId = null;
      }
      if (isEventStrategy(options)) {
        if (internals.pendingEvents !== null) {
          writeEventsToStorage(
            internals,
            internals.pendingEvents,
            internals.pendingCheckpoint
          );
          internals.pendingEvents = null;
          internals.pendingCheckpoint = null;
        }
      } else {
        if (internals.pendingContext !== null) {
          writeSnapshotToStorage(
            internals as any,
            internals.pendingContext as TContext
          );
          internals.pendingContext = null;
        }
      }
    }
  };

  return internals;
}
```

### 🔹 函式: `transition()`
- **變更前簽章 (Before)**: `transition(snapshot, event)` (L246~L332)
- **變更後簽章 (After)**: `transition(snapshot, event)` (L373~L459)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(snapshot, event) => {
      // Internal rehydrate event (not exposed in trigger types)
      if (event.type === '__persist.rehydrate') {
        const rawState = event.state as string | null | undefined;

        if (!rawState) {
          return [
            { ...snapshot, _persist: { ...snapshot._persist, hydrated: true } },
            []
          ];
        }

        try {
          const parsed = deserializeValue(options, rawState);
          const persistedContext = migrateIfNeeded(options, parsed);
          const mergedContext = mergeContext(
            options,
            persistedContext,
            snapshot.context
          );

          return [
            {
              ...snapshot,
              context: mergedContext,
              _persist: { ...snapshot._persist, hydrated: true }
            },
            []
          ];
        } catch (err) {
          options.onError?.(err);
          return [
            {
              ...snapshot,
              _persist: { ...snapshot._persist, hydrated: true }
            },
            []
          ];
        }
      }

      // Delegate to wrapped logic
      const [nextSnapshot, effects] = logic.transition(snapshot, event);

      // Preserve _persist metadata
      const snapshotWithMeta = {
        ...nextSnapshot,
        _persist: snapshot._persist ?? { hydrated: false },
        [PERSIST_INTERNALS]: internals
      };

      // Don't write to storage until hydrated
      if (!snapshotWithMeta._persist?.hydrated) {
        return [snapshotWithMeta, effects];
      }

      // Check filter
      if (options.filter && !options.filter(event as TEvent)) {
        return [snapshotWithMeta, effects];
      }

      // Schedule storage write
      if (throttleMs > 0) {
        // Throttled: buffer context, schedule delayed write
        internals.pendingContext = options.pick
          ? (options.pick(nextSnapshot.context) as any)
          : nextSnapshot.context;

        if (internals.flushTimeoutId === null) {
          const persistEffect = () => {
            internals.flushTimeoutId = setTimeout(() => {
              internals.flush();
            }, throttleMs);
          };
          return [snapshotWithMeta, [...effects, persistEffect]];
        }

        return [snapshotWithMeta, effects];
      }

      // Immediate write as effect
      const persistEffect = () => {
        writeToStorage(internals, nextSnapshot.context);
      };

      return [snapshotWithMeta, [...effects, persistEffect]];
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(snapshot, event) => {
      // Internal rehydrate event (not exposed in trigger types)
      if (event.type === '__persist.rehydrate') {
        const rawState = event.state as string | null | undefined;

        if (!rawState) {
          return [
            { ...snapshot, _persist: { ...snapshot._persist, hydrated: true } },
            []
          ];
        }

        try {
          const parsed = deserializeSnapshotValue(options, rawState);
          const persistedContext = migrateSnapshotIfNeeded(options, parsed);
          const mergedContext = mergeContext(
            options,
            persistedContext,
            snapshot.context
          );

          return [
            {
              ...snapshot,
              context: mergedContext,
              _persist: { ...snapshot._persist, hydrated: true }
            },
            []
          ];
        } catch (err) {
          options.onError?.(err);
          return [
            {
              ...snapshot,
              _persist: { ...snapshot._persist, hydrated: true }
            },
            []
          ];
        }
      }

      // Delegate to wrapped logic
      const [nextSnapshot, effects] = logic.transition(snapshot, event);

      // Preserve _persist metadata
      const snapshotWithMeta = {
        ...nextSnapshot,
        _persist: snapshot._persist ?? { hydrated: false },
        [PERSIST_INTERNALS]: internals
      };

      // Don't write to storage until hydrated
      if (!snapshotWithMeta._persist?.hydrated) {
        return [snapshotWithMeta, effects];
      }

      // Check filter
      if (options.filter && !options.filter(event as TEvent)) {
        return [snapshotWithMeta, effects];
      }

      // Schedule storage write
      if (throttleMs > 0) {
        // Throttled: buffer context, schedule delayed write
        internals.pendingContext = options.pick
          ? (options.pick(nextSnapshot.context) as any)
          : nextSnapshot.context;

        if (internals.flushTimeoutId === null) {
          const persistEffect = () => {
            internals.flushTimeoutId = setTimeout(() => {
              internals.flush();
            }, throttleMs);
          };
          return [snapshotWithMeta, [...effects, persistEffect]];
        }

        return [snapshotWithMeta, effects];
      }

      // Immediate write as effect
      const persistEffect = () => {
        writeSnapshotToStorage(internals as any, nextSnapshot.context);
      };

      return [snapshotWithMeta, [...effects, persistEffect]];
    }
```

### 🔹 函式: `persistFromLogic()`
- **變更前簽章 (Before)**: `function persistFromLogic<
  TContext extends StoreContext,
  TEvent extends EventObject,
  TEmitted extends EventObject
>(
  logic: StoreLogic<StoreSnapshot<TContext>, TEvent, TEmitted>,
  options: PersistOptions<TContext, TEvent>
): StoreLogic<StoreSnapshot<TContext>, TEvent, TEmitted>` (L177~L336)
- **變更後簽章 (After)**: `function persistFromLogic<
  TContext extends StoreContext,
  TEvent extends EventObject,
  TEmitted extends EventObject
>(
  logic: StoreLogic<StoreSnapshot<TContext>, TEvent, TEmitted>,
  options: PersistOptions<TContext, TEvent>
): StoreLogic<StoreSnapshot<TContext>, TEvent, TEmitted>` (L674~L692)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function persistFromLogic<
  TContext extends StoreContext,
  TEvent extends EventObject,
  TEmitted extends EventObject
>(
  logic: StoreLogic<StoreSnapshot<TContext>, TEvent, TEmitted>,
  options: PersistOptions<TContext, TEvent>
): StoreLogic<StoreSnapshot<TContext>, TEvent, TEmitted> {
  const internals = createInternals(options);
  const { storage } = internals;
  const throttleMs = options.throttle ?? 0;

  const enhancedLogic: AnyStoreLogic = {
    getInitialSnapshot: () => {
      const baseSnapshot = logic.getInitialSnapshot();

      if (options.skipHydration) {
        return {
          ...baseSnapshot,
          _persist: { hydrated: false },
          [PERSIST_INTERNALS]: internals
        };
      }

      // Attempt sync read
      try {
        const storedValue = storage.getItem(options.name);

        // Async storage — can't hydrate synchronously
        if (storedValue instanceof Promise) {
          return {
            ...baseSnapshot,
            _persist: { hydrated: false },
            [PERSIST_INTERNALS]: internals
          };
        }

        if (storedValue === null) {
          return {
            ...baseSnapshot,
            _persist: { hydrated: true },
            [PERSIST_INTERNALS]: internals
          };
        }

        const parsed = deserializeValue(options, storedValue);
        const persistedContext = migrateIfNeeded(options, parsed);
        const mergedContext = mergeContext(
          options,
          persistedContext,
          baseSnapshot.context
        );

        return {
          ...baseSnapshot,
          context: mergedContext,
          _persist: { hydrated: true },
          [PERSIST_INTERNALS]: internals
        };
      } catch (err) {
        options.onError?.(err);
        return {
          ...baseSnapshot,
          _persist: { hydrated: true },
          [PERSIST_INTERNALS]: internals
        };
      }
    },

    transition: (snapshot, event) => {
      // Internal rehydrate event (not exposed in trigger types)
      if (event.type === '__persist.rehydrate') {
        const rawState = event.state as string | null | undefined;

        if (!rawState) {
          return [
            { ...snapshot, _persist: { ...snapshot._persist, hydrated: true } },
            []
          ];
        }

        try {
          const parsed = deserializeValue(options, rawState);
          const persistedContext = migrateIfNeeded(options, parsed);
          const mergedContext = mergeContext(
            options,
            persistedContext,
            snapshot.context
          );

          return [
            {
              ...snapshot,
              context: mergedContext,
              _persist: { ...snapshot._persist, hydrated: true }
            },
            []
          ];
        } catch (err) {
          options.onError?.(err);
          return [
            {
              ...snapshot,
              _persist: { ...snapshot._persist, hydrated: true }
            },
            []
          ];
        }
      }

      // Delegate to wrapped logic
      const [nextSnapshot, effects] = logic.transition(snapshot, event);

      // Preserve _persist metadata
      const snapshotWithMeta = {
        ...nextSnapshot,
        _persist: snapshot._persist ?? { hydrated: false },
        [PERSIST_INTERNALS]: internals
      };

      // Don't write to storage until hydrated
      if (!snapshotWithMeta._persist?.hydrated) {
        return [snapshotWithMeta, effects];
      }

      // Check filter
      if (options.filter && !options.filter(event as TEvent)) {
        return [snapshotWithMeta, effects];
      }

      // Schedule storage write
      if (throttleMs > 0) {
        // Throttled: buffer context, schedule delayed write
        internals.pendingContext = options.pick
          ? (options.pick(nextSnapshot.context) as any)
          : nextSnapshot.context;

        if (internals.flushTimeoutId === null) {
          const persistEffect = () => {
            internals.flushTimeoutId = setTimeout(() => {
              internals.flush();
            }, throttleMs);
          };
          return [snapshotWithMeta, [...effects, persistEffect]];
        }

        return [snapshotWithMeta, effects];
      }

      // Immediate write as effect
      const persistEffect = () => {
        writeToStorage(internals, nextSnapshot.context);
      };

      return [snapshotWithMeta, [...effects, persistEffect]];
    }
  };

  return enhancedLogic;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function persistFromLogic<
  TContext extends StoreContext,
  TEvent extends EventObject,
  TEmitted extends EventObject
>(
  logic: StoreLogic<StoreSnapshot<TContext>, TEvent, TEmitted>,
  options: PersistOptions<TContext, TEvent>
): StoreLogic<StoreSnapshot<TContext>, TEvent, TEmitted> {
  if (isEventStrategy(options)) {
    return persistEventFromLogic(
      logic,
      options as PersistEventOptions<TContext, TEvent>
    );
  }
  return persistSnapshotFromLogic(
    logic,
    options as PersistSnapshotOptions<TContext, TEvent>
  );
}
```


---

### 🔹 Commit #11: `703c3a10`
- **完整 Hash**: `703c3a109c824f2334ede31d8428e923d2727e6e`
- **說明 (Ground Truth)**: [core] Add `getNextTransitions(state)` (#5406)
- **變更檔案數**: 3

#### 📄 檔案: `packages/core/src/index.ts`
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

#### 📄 檔案: `packages/core/src/stateUtils.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:74, E:117, A:0) ➔ After(N:74, E:117, A:0)
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

### 🔹 函式: `isAtomicStateNode()`
- **變更前簽章 (Before)**: `isAtomicStateNode(stateNode: StateNode<any, any>)` (L60~L61)
- **變更後簽章 (After)**: `function isAtomicStateNode(stateNode: StateNode<any, any>)` (L60~L62)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(stateNode: StateNode<any, any>) =>
  stateNode.type === 'atomic' || stateNode.type === 'final'
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function isAtomicStateNode(stateNode: StateNode<any, any>) {
  return stateNode.type === 'atomic' || stateNode.type === 'final';
}
```


#### 📄 檔案: `packages/core/src/transition.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:5, E:2, A:0) ➔ After(N:7, E:3, A:0)
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
  • + [新增節點] `getNextTransitions` (FUNCTION_DEF)
  • + [新增節點] `getProperAncestors (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `getNextTransitions` ──[CALLS [guarded]]──> `getProperAncestors (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #12: `7cd82a27`
- **完整 Hash**: `7cd82a27bc0b7dbfd9a3f8aa1ea3b424bb91d741`
- **說明 (Ground Truth)**: Fix memory leaks in actor cleanup (#5408)
- **變更檔案數**: 3

#### 📄 檔案: `packages/core/src/actors/callback.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:11, E:2, A:0) ➔ After(N:11, E:2, A:0)
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

### 🔹 函式: `fromCallback()`
- **變更前簽章 (Before)**: `function fromCallback<
  TEvent extends EventObject,
  TInput = NonReducibleUnknown,
  TEmitted extends EventObject = EventObject
>(
  callback: CallbackLogicFunction<TEvent, AnyEventObject, TInput, TEmitted>
): CallbackActorLogic<TEvent, TInput, TEmitted>` (L183~L254)
- **變更後簽章 (After)**: `function fromCallback<
  TEvent extends EventObject,
  TInput = NonReducibleUnknown,
  TEmitted extends EventObject = EventObject
>(
  callback: CallbackLogicFunction<TEvent, AnyEventObject, TInput, TEmitted>
): CallbackActorLogic<TEvent, TInput, TEmitted>` (L183~L256)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function fromCallback<
  TEvent extends EventObject,
  TInput = NonReducibleUnknown,
  TEmitted extends EventObject = EventObject
>(
  callback: CallbackLogicFunction<TEvent, AnyEventObject, TInput, TEmitted>
): CallbackActorLogic<TEvent, TInput, TEmitted> {
  const logic: CallbackActorLogic<TEvent, TInput, TEmitted> = {
    config: callback,
    start: (state, actorScope) => {
      const { self, system, emit } = actorScope;

      const callbackState: CallbackInstanceState<TEvent> = {
        receivers: undefined,
        dispose: undefined
      };

      instanceStates.set(self, callbackState);

      callbackState.dispose = callback({
        input: state.input,
        system,
        self,
        sendBack: (event) => {
          if (self.getSnapshot().status === 'stopped') {
            return;
          }
          if (self._parent) {
            system._relay(self, self._parent, event);
          }
        },
        receive: (listener) => {
          callbackState.receivers ??= new Set();
          callbackState.receivers.add(listener);
        },
        emit
      });
    },
    transition: (state, event, actorScope) => {
      const callbackState: CallbackInstanceState<TEvent> = instanceStates.get(
        actorScope.self
      )!;

      if (event.type === XSTATE_STOP) {
        state = {
          ...state,
          status: 'stopped',
          error: undefined
        };

        callbackState.dispose?.();
        return state;
      }

      callbackState.receivers?.forEach((receiver) => receiver(event));

      return state;
    },
    getInitialSnapshot: (_, input) => {
      return {
        status: 'active',
        output: undefined,
        error: undefined,
        input
      };
    },
    getPersistedSnapshot: (snapshot) => snapshot,
    restoreSnapshot: (snapshot: any) => snapshot
  };

  return logic;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function fromCallback<
  TEvent extends EventObject,
  TInput = NonReducibleUnknown,
  TEmitted extends EventObject = EventObject
>(
  callback: CallbackLogicFunction<TEvent, AnyEventObject, TInput, TEmitted>
): CallbackActorLogic<TEvent, TInput, TEmitted> {
  const logic: CallbackActorLogic<TEvent, TInput, TEmitted> = {
    config: callback,
    start: (state, actorScope) => {
      const { self, system, emit } = actorScope;

      const callbackState: CallbackInstanceState<TEvent> = {
        receivers: undefined,
        dispose: undefined
      };

      instanceStates.set(self, callbackState);

      callbackState.dispose = callback({
        input: state.input,
        system,
        self,
        sendBack: (event) => {
          if (self.getSnapshot().status === 'stopped') {
            return;
          }
          if (self._parent) {
            system._relay(self, self._parent, event);
          }
        },
        receive: (listener) => {
          callbackState.receivers ??= new Set();
          callbackState.receivers.add(listener);
        },
        emit
      });
    },
    transition: (state, event, actorScope) => {
      const callbackState: CallbackInstanceState<TEvent> = instanceStates.get(
        actorScope.self
      )!;

      if (event.type === XSTATE_STOP) {
        state = {
          ...state,
          status: 'stopped',
          error: undefined
        };

        instanceStates.delete(actorScope.self);
        callbackState.receivers?.clear();
        callbackState.dispose?.();
        return state;
      }

      callbackState.receivers?.forEach((receiver) => receiver(event));

      return state;
    },
    getInitialSnapshot: (_, input) => {
      return {
        status: 'active',
        output: undefined,
        error: undefined,
        input
      };
    },
    getPersistedSnapshot: (snapshot) => snapshot,
    restoreSnapshot: (snapshot: any) => snapshot
  };

  return logic;
}
```

### 🔹 函式: `transition()`
- **變更前簽章 (Before)**: `transition(state, event, actorScope)` (L221~L240)
- **變更後簽章 (After)**: `transition(state, event, actorScope)` (L221~L242)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(state, event, actorScope) => {
      const callbackState: CallbackInstanceState<TEvent> = instanceStates.get(
        actorScope.self
      )!;

      if (event.type === XSTATE_STOP) {
        state = {
          ...state,
          status: 'stopped',
          error: undefined
        };

        callbackState.dispose?.();
        return state;
      }

      callbackState.receivers?.forEach((receiver) => receiver(event));

      return state;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(state, event, actorScope) => {
      const callbackState: CallbackInstanceState<TEvent> = instanceStates.get(
        actorScope.self
      )!;

      if (event.type === XSTATE_STOP) {
        state = {
          ...state,
          status: 'stopped',
          error: undefined
        };

        instanceStates.delete(actorScope.self);
        callbackState.receivers?.clear();
        callbackState.dispose?.();
        return state;
      }

      callbackState.receivers?.forEach((receiver) => receiver(event));

      return state;
    }
```


#### 📄 檔案: `packages/core/src/actors/promise.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:10, E:1, A:0) ➔ After(N:10, E:1, A:0)
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

### 🔹 函式: `fromPromise()`
- **變更前簽章 (Before)**: `function fromPromise<
  TOutput,
  TInput = NonReducibleUnknown,
  TEmitted extends EventObject = EventObject
>(
  promiseCreator: (` (L120~L232)
- **變更後簽章 (After)**: `function fromPromise<
  TOutput,
  TInput = NonReducibleUnknown,
  TEmitted extends EventObject = EventObject
>(
  promiseCreator: (` (L120~L233)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function fromPromise<
  TOutput,
  TInput = NonReducibleUnknown,
  TEmitted extends EventObject = EventObject
>(
  promiseCreator: ({
    input,
    system,
    self,
    signal,
    emit
  }: {
    /** Data that was provided to the promise actor */
    input: TInput;
    /** The actor system to which the promise actor belongs */
    system: AnyActorSystem;
    /** The parent actor of the promise actor */
    self: PromiseActorRef<TOutput>;
    signal: AbortSignal;
    emit: (emitted: TEmitted) => void;
  }) => PromiseLike<TOutput>
): PromiseActorLogic<TOutput, TInput, TEmitted> {
  const logic: PromiseActorLogic<TOutput, TInput, TEmitted> = {
    config: promiseCreator,
    transition: (state, event, scope) => {
      if (state.status !== 'active') {
        return state;
      }

      switch (event.type) {
        case XSTATE_PROMISE_RESOLVE: {
          const resolvedValue = (event as any).data;
          return {
            ...state,
            status: 'done',
            output: resolvedValue,
            input: undefined
          };
        }
        case XSTATE_PROMISE_REJECT:
          return {
            ...state,
            status: 'error',
            error: (event as any).data,
            input: undefined
          };
        case XSTATE_STOP: {
          controllerMap.get(scope.self)?.abort();
          return {
            ...state,
            status: 'stopped',
            input: undefined
          };
        }
        default:
          return state;
      }
    },
    start: (state, { self, system, emit }) => {
      // TODO: determine how to allow customizing this so that promises
      // can be restarted if necessary
      if (state.status !== 'active') {
        return;
      }
      const controller = new AbortController();
      controllerMap.set(self, controller);
      const resolvedPromise = Promise.resolve(
        promiseCreator({
          input: state.input!,
          system,
          self,
          signal: controller.signal,
          emit
        })
      );

      resolvedPromise.then(
        (response) => {
          if (self.getSnapshot().status !== 'active') {
            return;
          }
          controllerMap.delete(self);
          system._relay(self, self, {
            type: XSTATE_PROMISE_RESOLVE,
            data: response
          });
        },
        (errorData) => {
          if (self.getSnapshot().status !== 'active') {
            return;
          }
          controllerMap.delete(self);
          system._relay(self, self, {
            type: XSTATE_PROMISE_REJECT,
            data: errorData
          });
        }
      );
    },
    getInitialSnapshot: (_, input) => {
      return {
        status: 'active',
        output: undefined,
        error: undefined,
        input
      };
    },
    getPersistedSnapshot: (snapshot) => snapshot,
    restoreSnapshot: (snapshot: any) => snapshot
  };

  return logic;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function fromPromise<
  TOutput,
  TInput = NonReducibleUnknown,
  TEmitted extends EventObject = EventObject
>(
  promiseCreator: ({
    input,
    system,
    self,
    signal,
    emit
  }: {
    /** Data that was provided to the promise actor */
    input: TInput;
    /** The actor system to which the promise actor belongs */
    system: AnyActorSystem;
    /** The parent actor of the promise actor */
    self: PromiseActorRef<TOutput>;
    signal: AbortSignal;
    emit: (emitted: TEmitted) => void;
  }) => PromiseLike<TOutput>
): PromiseActorLogic<TOutput, TInput, TEmitted> {
  const logic: PromiseActorLogic<TOutput, TInput, TEmitted> = {
    config: promiseCreator,
    transition: (state, event, scope) => {
      if (state.status !== 'active') {
        return state;
      }

      switch (event.type) {
        case XSTATE_PROMISE_RESOLVE: {
          const resolvedValue = (event as any).data;
          return {
            ...state,
            status: 'done',
            output: resolvedValue,
            input: undefined
          };
        }
        case XSTATE_PROMISE_REJECT:
          return {
            ...state,
            status: 'error',
            error: (event as any).data,
            input: undefined
          };
        case XSTATE_STOP: {
          controllerMap.get(scope.self)?.abort();
          controllerMap.delete(scope.self);
          return {
            ...state,
            status: 'stopped',
            input: undefined
          };
        }
        default:
          return state;
      }
    },
    start: (state, { self, system, emit }) => {
      // TODO: determine how to allow customizing this so that promises
      // can be restarted if necessary
      if (state.status !== 'active') {
        return;
      }
      const controller = new AbortController();
      controllerMap.set(self, controller);
      const resolvedPromise = Promise.resolve(
        promiseCreator({
          input: state.input!,
          system,
          self,
          signal: controller.signal,
          emit
        })
      );

      resolvedPromise.then(
        (response) => {
          if (self.getSnapshot().status !== 'active') {
            return;
          }
          controllerMap.delete(self);
          system._relay(self, self, {
            type: XSTATE_PROMISE_RESOLVE,
            data: response
          });
        },
        (errorData) => {
          if (self.getSnapshot().status !== 'active') {
            return;
          }
          controllerMap.delete(self);
          system._relay(self, self, {
            type: XSTATE_PROMISE_REJECT,
            data: errorData
          });
        }
      );
    },
    getInitialSnapshot: (_, input) => {
      return {
        status: 'active',
        output: undefined,
        error: undefined,
        input
      };
    },
    getPersistedSnapshot: (snapshot) => snapshot,
    restoreSnapshot: (snapshot: any) => snapshot
  };

  return logic;
}
```

### 🔹 函式: `transition()`
- **變更前簽章 (Before)**: `transition(state, event, scope)` (L144~L177)
- **變更後簽章 (After)**: `transition(state, event, scope)` (L144~L178)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(state, event, scope) => {
      if (state.status !== 'active') {
        return state;
      }

      switch (event.type) {
        case XSTATE_PROMISE_RESOLVE: {
          const resolvedValue = (event as any).data;
          return {
            ...state,
            status: 'done',
            output: resolvedValue,
            input: undefined
          };
        }
        case XSTATE_PROMISE_REJECT:
          return {
            ...state,
            status: 'error',
            error: (event as any).data,
            input: undefined
          };
        case XSTATE_STOP: {
          controllerMap.get(scope.self)?.abort();
          return {
            ...state,
            status: 'stopped',
            input: undefined
          };
        }
        default:
          return state;
      }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(state, event, scope) => {
      if (state.status !== 'active') {
        return state;
      }

      switch (event.type) {
        case XSTATE_PROMISE_RESOLVE: {
          const resolvedValue = (event as any).data;
          return {
            ...state,
            status: 'done',
            output: resolvedValue,
            input: undefined
          };
        }
        case XSTATE_PROMISE_REJECT:
          return {
            ...state,
            status: 'error',
            error: (event as any).data,
            input: undefined
          };
        case XSTATE_STOP: {
          controllerMap.get(scope.self)?.abort();
          controllerMap.delete(scope.self);
          return {
            ...state,
            status: 'stopped',
            input: undefined
          };
        }
        default:
          return state;
      }
    }
```


#### 📄 檔案: `packages/core/src/createActor.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:46, E:17, A:0) ➔ After(N:46, E:17, A:0)
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

### 🔹 函式: `_complete()`
- **變更前簽章 (Before)**: `_complete()` (L629~L638)
- **變更後簽章 (After)**: `_complete()` (L629~L639)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private _complete(): void {
    for (const observer of this.observers) {
      try {
        observer.complete?.();
      } catch (err) {
        reportUnhandledError(err);
      }
    }
    this.observers.clear();
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private _complete(): void {
    for (const observer of this.observers) {
      try {
        observer.complete?.();
      } catch (err) {
        reportUnhandledError(err);
      }
    }
    this.observers.clear();
    this.eventListeners.clear();
  }
```

### 🔹 函式: `_reportError()`
- **變更前簽章 (Before)**: `_reportError(err: unknown)` (L639~L661)
- **變更後簽章 (After)**: `_reportError(err: unknown)` (L640~L664)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private _reportError(err: unknown): void {
    if (!this.observers.size) {
      if (!this._parent) {
        reportUnhandledError(err);
      }
      return;
    }
    let reportError = false;

    for (const observer of this.observers) {
      const errorListener = observer.error;
      reportError ||= !errorListener;
      try {
        errorListener?.(err);
      } catch (err2) {
        reportUnhandledError(err2);
      }
    }
    this.observers.clear();
    if (reportError) {
      reportUnhandledError(err);
    }
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private _reportError(err: unknown): void {
    if (!this.observers.size) {
      if (!this._parent) {
        reportUnhandledError(err);
      }
      this.eventListeners.clear();
      return;
    }
    let reportError = false;

    for (const observer of this.observers) {
      const errorListener = observer.error;
      reportError ||= !errorListener;
      try {
        errorListener?.(err);
      } catch (err2) {
        reportUnhandledError(err2);
      }
    }
    this.observers.clear();
    this.eventListeners.clear();
    if (reportError) {
      reportUnhandledError(err);
    }
  }
```


---

### 🔹 Commit #13: `329297b3`
- **完整 Hash**: `329297b3bf859668ed1dfc260c14e773a0413fd4`
- **說明 (Ground Truth)**: [core] Add support for partial event descriptors in `assertEvent(…)` (#5422)
- **變更檔案數**: 3

#### 📄 檔案: `packages/core/src/assert.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:2, E:1, A:0) ➔ After(N:4, E:2, A:0)
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
  • + [新增節點] `matchesEventDescriptor (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `matches` (FUNCTION_DEF)
  • + [新增呼叫邊] `matches` ──[CALLS]──> `matchesEventDescriptor (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `assertEvent()`
- **變更前簽章 (Before)**: `function assertEvent<
  TEvent extends EventObject,
  TAssertedType extends TEvent['type']
>(
  event: TEvent,
  type: TAssertedType | TAssertedType[]
): asserts event is TEvent &` (L27~L44)
- **變更後簽章 (After)**: `function assertEvent<
  TEvent extends EventObject,
  TAssertedDescriptor extends EventDescriptor<TEvent>
>(
  event: TEvent,
  type: TAssertedDescriptor | readonly TAssertedDescriptor[]
): asserts event is ExtractEvent<TEvent, TAssertedDescriptor>` (L27~L49)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function assertEvent<
  TEvent extends EventObject,
  TAssertedType extends TEvent['type']
>(
  event: TEvent,
  type: TAssertedType | TAssertedType[]
): asserts event is TEvent & { type: TAssertedType } {
  const types = toArray(type);
  if (!types.includes(event.type as any)) {
    const typesText =
      types.length === 1
        ? `type "${types[0]}"`
        : `one of types "${types.join('", "')}"`;
    throw new Error(
      `Expected event ${JSON.stringify(event)} to have ${typesText}`
    );
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function assertEvent<
  TEvent extends EventObject,
  TAssertedDescriptor extends EventDescriptor<TEvent>
>(
  event: TEvent,
  type: TAssertedDescriptor | readonly TAssertedDescriptor[]
): asserts event is ExtractEvent<TEvent, TAssertedDescriptor> {
  const types = toArray(type);

  const matches = types.some((descriptor) =>
    matchesEventDescriptor(event.type, descriptor as string)
  );

  if (!matches) {
    const typesText =
      types.length === 1
        ? `type matching "${types[0]}"`
        : `one of types matching "${types.join('", "')}"`;
    throw new Error(
      `Expected event ${JSON.stringify(event)} to have ${typesText}`
    );
  }
}
```


#### 📄 檔案: `packages/core/src/stateUtils.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:73, E:116, A:0) ➔ After(N:74, E:117, A:0)
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
  • + [新增節點] `matchesEventDescriptor (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `getCandidates` ──[CALLS]──> `matchesEventDescriptor (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `getCandidates()`
- **變更前簽章 (Before)**: `function getCandidates<TEvent extends EventObject>(
  stateNode: StateNode<any, TEvent>,
  receivedEventType: TEvent['type']
): Array<TransitionDefinition<any, TEvent>>` (L209~L267)
- **變更後簽章 (After)**: `function getCandidates<TEvent extends EventObject>(
  stateNode: StateNode<any, TEvent>,
  receivedEventType: TEvent['type']
): Array<TransitionDefinition<any, TEvent>>` (L210~L224)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function getCandidates<TEvent extends EventObject>(
  stateNode: StateNode<any, TEvent>,
  receivedEventType: TEvent['type']
): Array<TransitionDefinition<any, TEvent>> {
  const candidates =
    stateNode.transitions.get(receivedEventType) ||
    [...stateNode.transitions.keys()]
      .filter((eventDescriptor) => {
        // check if transition is a wildcard transition,
        // which matches any non-transient events
        if (eventDescriptor === WILDCARD) {
          return true;
        }

        if (!eventDescriptor.endsWith('.*')) {
          return false;
        }

        if (isDevelopment && /.*\*.+/.test(eventDescriptor)) {
          console.warn(
            `Wildcards can only be the last token of an event descriptor (e.g., "event.*") or the entire event descriptor ("*"). Check the "${eventDescriptor}" event.`
          );
        }

        const partialEventTokens = eventDescriptor.split('.');
        const eventTokens = receivedEventType.split('.');

        for (
          let tokenIndex = 0;
          tokenIndex < partialEventTokens.length;
          tokenIndex++
        ) {
          const partialEventToken = partialEventTokens[tokenIndex];
          const eventToken = eventTokens[tokenIndex];

          if (partialEventToken === '*') {
            const isLastToken = tokenIndex === partialEventTokens.length - 1;

            if (isDevelopment && !isLastToken) {
              console.warn(
                `Infix wildcards in transition events are not allowed. Check the "${eventDescriptor}" transition.`
              );
            }

            return isLastToken;
          }

          if (partialEventToken !== eventToken) {
            return false;
          }
        }

        return true;
      })
      .sort((a, b) => b.length - a.length)
      .flatMap((key) => stateNode.transitions.get(key)!);

  return candidates;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function getCandidates<TEvent extends EventObject>(
  stateNode: StateNode<any, TEvent>,
  receivedEventType: TEvent['type']
): Array<TransitionDefinition<any, TEvent>> {
  const candidates =
    stateNode.transitions.get(receivedEventType) ||
    [...stateNode.transitions.keys()]
      .filter((eventDescriptor) =>
        matchesEventDescriptor(receivedEventType, eventDescriptor)
      )
      .sort((a, b) => b.length - a.length)
      .flatMap((key) => stateNode.transitions.get(key)!);

  return candidates;
}
```


#### 📄 檔案: `packages/core/src/utils.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:19, E:12, A:0) ➔ After(N:20, E:12, A:0)
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
  • + [新增節點] `matchesEventDescriptor` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #14: `d345e1fa`
- **完整 Hash**: `d345e1fa497c2196e296512937ed52e1c76fd6be`
- **說明 (Ground Truth)**: [@xstate/store] Fix emit event types (#5401)
- **變更檔案數**: 1

#### 📄 檔案: `packages/xstate-store/src/undo.ts`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:5, E:1, A:0) ➔ After(N:5, E:1, A:0)
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

### 🔹 Commit #15: `4b6a513e`
- **完整 Hash**: `4b6a513ebd7ee1ab067856be4b431651b491cba5`
- **說明 (Ground Truth)**: [@xstate/store] Fix event type overwriting (#5383)
- **變更檔案數**: 1

#### 📄 檔案: `packages/xstate-store/src/store.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:36, E:18, A:0) ➔ After(N:36, E:18, A:0)
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
  - 💥 作用域阻隔: 函式 'effect' 被深鎖在內部閉包 (scope:arrow@after/packages/xstate-store/src/store.ts:L420C10)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `createStoreCore()`
- **變更前簽章 (Before)**: `function createStoreCore<
  TContext extends StoreContext,
  TSnapshot extends StoreSnapshot<any>,
  TEventPayloadMap extends EventPayloadMap,
  TEmitted extends EventObject
>(
  logic: StoreLogic<TSnapshot, ExtractEvents<TEventPayloadMap>, TEmitted>,
  emits?: Record<string, (payload: any) => void> // TODO: improve this type
): Store<TContext, ExtractEvents<TEventPayloadMap>, TEmitted>` (L51~L205)
- **變更後簽章 (After)**: `function createStoreCore<
  TContext extends StoreContext,
  TSnapshot extends StoreSnapshot<any>,
  TEventPayloadMap extends EventPayloadMap,
  TEmitted extends EventObject
>(
  logic: StoreLogic<TSnapshot, ExtractEvents<TEventPayloadMap>, TEmitted>,
  emits?: Record<string, (payload: any) => void> // TODO: improve this type
): Store<TContext, ExtractEvents<TEventPayloadMap>, TEmitted>` (L51~L205)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createStoreCore<
  TContext extends StoreContext,
  TSnapshot extends StoreSnapshot<any>,
  TEventPayloadMap extends EventPayloadMap,
  TEmitted extends EventObject
>(
  logic: StoreLogic<TSnapshot, ExtractEvents<TEventPayloadMap>, TEmitted>,
  emits?: Record<string, (payload: any) => void> // TODO: improve this type
): Store<TContext, ExtractEvents<TEventPayloadMap>, TEmitted> {
  type StoreEvent = ExtractEvents<TEventPayloadMap>;
  let listeners: Map<TEmitted['type'], Set<any>> | undefined;
  const initialSnapshot = logic.getInitialSnapshot();
  let currentSnapshot: TSnapshot = initialSnapshot;
  const atom = createAtom<StoreSnapshot<TContext>>(currentSnapshot);

  const emit = (ev: TEmitted) => {
    if (!listeners) {
      return;
    }
    const type = ev.type;
    const typeListeners = listeners.get(type);
    if (typeListeners) {
      typeListeners.forEach((listener) => listener(ev));
    }
  };

  const transition = logic.transition;

  function receive(event: StoreEvent) {
    let effects: StoreEffect<TEmitted>[];
    [currentSnapshot, effects] = transition(currentSnapshot, event);

    inspectionObservers.get(store)?.forEach((observer) => {
      observer.next?.({
        type: '@xstate.snapshot',
        event,
        snapshot: currentSnapshot,
        actorRef: store,
        rootId: store.sessionId
      });
    });

    atom.set(currentSnapshot);

    for (const effect of effects) {
      if (typeof effect === 'function') {
        effect();
      } else {
        // handle the inherent effect first
        emits?.[effect.type]?.(effect);
        emit(effect);
      }
    }
  }

  const store: Store<TContext, StoreEvent, TEmitted> &
    Pick<InternalBaseAtom<any>, '_snapshot'> = {
    get _snapshot() {
      return (atom as unknown as InternalBaseAtom<any>)._snapshot;
    },
    on(emittedEventType, handler) {
      if (!listeners) {
        listeners = new Map();
      }
      let eventListeners = listeners.get(emittedEventType);
      if (!eventListeners) {
        eventListeners = new Set();
        listeners.set(emittedEventType, eventListeners);
      }
      const wrappedHandler = handler.bind(undefined);
      eventListeners.add(wrappedHandler);

      return {
        unsubscribe() {
          eventListeners.delete(wrappedHandler);
        }
      };
    },
    transition: logic.transition as any, // TODO: fix this
    sessionId: uniqueId(),
    send(event) {
      inspectionObservers.get(store)?.forEach((observer) => {
        observer.next?.({
          type: '@xstate.event',
          event,
          sourceRef: undefined,
          actorRef: store,
          rootId: store.sessionId
        });
      });
      receive(event as unknown as StoreEvent);
    },
    getSnapshot() {
      return currentSnapshot;
    },
    get() {
      return atom.get();
    },
    getInitialSnapshot() {
      return initialSnapshot;
    },
    subscribe: atom.subscribe.bind(atom),
    [symbolObservable](): InteropSubscribable<StoreSnapshot<TContext>> {
      return this;
    },
    inspect: (observerOrFn) => {
      const observer = toObserver(observerOrFn);
      inspectionObservers.set(
        store,
        inspectionObservers.get(store) ?? new Set()
      );
      inspectionObservers.get(store)!.add(observer);

      observer.next?.({
        type: '@xstate.actor',
        actorRef: store,
        rootId: store.sessionId
      });

      observer.next?.({
        type: '@xstate.snapshot',
        snapshot: initialSnapshot,
        event: { type: '@xstate.init' },
        actorRef: store,
        rootId: store.sessionId
      });

      return {
        unsubscribe() {
          return inspectionObservers.get(store)?.delete(observer);
        }
      };
    },
    trigger: new Proxy({} as Store<TContext, StoreEvent, TEmitted>['trigger'], {
      get: (_, eventType: string) => {
        return (payload: any) => {
          store.send({
            type: eventType,
            ...payload
          });
        };
      }
    }),
    select<TSelected>(
      selector: Selector<TContext, TSelected>,
      equalityFn: (a: TSelected, b: TSelected) => boolean = Object.is
    ): Selection<TSelected> {
      return createAtom(() => selector(store.get().context), {
        compare: equalityFn
      });
    }
  };

  return store;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createStoreCore<
  TContext extends StoreContext,
  TSnapshot extends StoreSnapshot<any>,
  TEventPayloadMap extends EventPayloadMap,
  TEmitted extends EventObject
>(
  logic: StoreLogic<TSnapshot, ExtractEvents<TEventPayloadMap>, TEmitted>,
  emits?: Record<string, (payload: any) => void> // TODO: improve this type
): Store<TContext, ExtractEvents<TEventPayloadMap>, TEmitted> {
  type StoreEvent = ExtractEvents<TEventPayloadMap>;
  let listeners: Map<TEmitted['type'], Set<any>> | undefined;
  const initialSnapshot = logic.getInitialSnapshot();
  let currentSnapshot: TSnapshot = initialSnapshot;
  const atom = createAtom<StoreSnapshot<TContext>>(currentSnapshot);

  const emit = (ev: TEmitted) => {
    if (!listeners) {
      return;
    }
    const type = ev.type;
    const typeListeners = listeners.get(type);
    if (typeListeners) {
      typeListeners.forEach((listener) => listener(ev));
    }
  };

  const transition = logic.transition;

  function receive(event: StoreEvent) {
    let effects: StoreEffect<TEmitted>[];
    [currentSnapshot, effects] = transition(currentSnapshot, event);

    inspectionObservers.get(store)?.forEach((observer) => {
      observer.next?.({
        type: '@xstate.snapshot',
        event,
        snapshot: currentSnapshot,
        actorRef: store,
        rootId: store.sessionId
      });
    });

    atom.set(currentSnapshot);

    for (const effect of effects) {
      if (typeof effect === 'function') {
        effect();
      } else {
        // handle the inherent effect first
        emits?.[effect.type]?.(effect);
        emit(effect);
      }
    }
  }

  const store: Store<TContext, StoreEvent, TEmitted> &
    Pick<InternalBaseAtom<any>, '_snapshot'> = {
    get _snapshot() {
      return (atom as unknown as InternalBaseAtom<any>)._snapshot;
    },
    on(emittedEventType, handler) {
      if (!listeners) {
        listeners = new Map();
      }
      let eventListeners = listeners.get(emittedEventType);
      if (!eventListeners) {
        eventListeners = new Set();
        listeners.set(emittedEventType, eventListeners);
      }
      const wrappedHandler = handler.bind(undefined);
      eventListeners.add(wrappedHandler);

      return {
        unsubscribe() {
          eventListeners.delete(wrappedHandler);
        }
      };
    },
    transition: logic.transition as any, // TODO: fix this
    sessionId: uniqueId(),
    send(event) {
      inspectionObservers.get(store)?.forEach((observer) => {
        observer.next?.({
          type: '@xstate.event',
          event,
          sourceRef: undefined,
          actorRef: store,
          rootId: store.sessionId
        });
      });
      receive(event as unknown as StoreEvent);
    },
    getSnapshot() {
      return currentSnapshot;
    },
    get() {
      return atom.get();
    },
    getInitialSnapshot() {
      return initialSnapshot;
    },
    subscribe: atom.subscribe.bind(atom),
    [symbolObservable](): InteropSubscribable<StoreSnapshot<TContext>> {
      return this;
    },
    inspect: (observerOrFn) => {
      const observer = toObserver(observerOrFn);
      inspectionObservers.set(
        store,
        inspectionObservers.get(store) ?? new Set()
      );
      inspectionObservers.get(store)!.add(observer);

      observer.next?.({
        type: '@xstate.actor',
        actorRef: store,
        rootId: store.sessionId
      });

      observer.next?.({
        type: '@xstate.snapshot',
        snapshot: initialSnapshot,
        event: { type: '@xstate.init' },
        actorRef: store,
        rootId: store.sessionId
      });

      return {
        unsubscribe() {
          return inspectionObservers.get(store)?.delete(observer);
        }
      };
    },
    trigger: new Proxy({} as Store<TContext, StoreEvent, TEmitted>['trigger'], {
      get: (_, eventType: string) => {
        return (payload: any) => {
          store.send({
            ...payload,
            type: eventType
          });
        };
      }
    }),
    select<TSelected>(
      selector: Selector<TContext, TSelected>,
      equalityFn: (a: TSelected, b: TSelected) => boolean = Object.is
    ): Selection<TSelected> {
      return createAtom(() => selector(store.get().context), {
        compare: equalityFn
      });
    }
  };

  return store;
}
```

### 🔹 函式: `get()`
- **變更前簽章 (Before)**: `get(_, eventType: string)` (L185~L192)
- **變更後簽章 (After)**: `get(_, eventType: string)` (L185~L192)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(_, eventType: string) => {
        return (payload: any) => {
          store.send({
            type: eventType,
            ...payload
          });
        };
      }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(_, eventType: string) => {
        return (payload: any) => {
          store.send({
            ...payload,
            type: eventType
          });
        };
      }
```


---

### 🔹 Commit #16: `98f9ddde`
- **完整 Hash**: `98f9ddde939320fb698ef382f6712a0753d55ca5`
- **說明 (Ground Truth)**: [core] Make `actor.systemId` public (#5379)
- **變更檔案數**: 2

#### 📄 檔案: `packages/core/src/State.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:13, E:6, A:0) ➔ After(N:13, E:6, A:0)
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

### 🔹 函式: `getPersistedSnapshot()`
- **變更前簽章 (Before)**: `function getPersistedSnapshot<
  TContext extends MachineContext,
  TEvent extends EventObject,
  TChildren extends Record<string, AnyActorRef | undefined>,
  TStateValue extends StateValue,
  TTag extends string,
  TOutput,
  TMeta extends MetaObject
>(
  snapshot: MachineSnapshot<
    TContext,
    TEvent,
    TChildren,
    TStateValue,
    TTag,
    TOutput,
    TMeta,
    any // state schema
  >,
  options?: unknown
): Snapshot<unknown>` (L420~L484)
- **變更後簽章 (After)**: `function getPersistedSnapshot<
  TContext extends MachineContext,
  TEvent extends EventObject,
  TChildren extends Record<string, AnyActorRef | undefined>,
  TStateValue extends StateValue,
  TTag extends string,
  TOutput,
  TMeta extends MetaObject
>(
  snapshot: MachineSnapshot<
    TContext,
    TEvent,
    TChildren,
    TStateValue,
    TTag,
    TOutput,
    TMeta,
    any // state schema
  >,
  options?: unknown
): Snapshot<unknown>` (L420~L484)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function getPersistedSnapshot<
  TContext extends MachineContext,
  TEvent extends EventObject,
  TChildren extends Record<string, AnyActorRef | undefined>,
  TStateValue extends StateValue,
  TTag extends string,
  TOutput,
  TMeta extends MetaObject
>(
  snapshot: MachineSnapshot<
    TContext,
    TEvent,
    TChildren,
    TStateValue,
    TTag,
    TOutput,
    TMeta,
    any // state schema
  >,
  options?: unknown
): Snapshot<unknown> {
  const {
    _nodes: nodes,
    tags,
    machine,
    children,
    context,
    can,
    hasTag,
    matches,
    getMeta,
    toJSON,
    ...jsonValues
  } = snapshot;

  const childrenJson: Record<string, unknown> = {};

  for (const id in children) {
    const child = children[id] as any;
    if (
      isDevelopment &&
      typeof child.src !== 'string' &&
      (!options || !('__unsafeAllowInlineActors' in (options as object)))
    ) {
      throw new Error('An inline child actor cannot be persisted.');
    }
    childrenJson[id as keyof typeof childrenJson] = {
      snapshot: child.getPersistedSnapshot(options),
      src: child.src,
      systemId: child._systemId,
      syncSnapshot: child._syncSnapshot
    };
  }

  const persisted = {
    ...jsonValues,
    context: persistContext(context) as any,
    children: childrenJson,
    historyValue: serializeHistoryValue<TContext, TEvent>(
      jsonValues.historyValue
    )
  };

  return persisted;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function getPersistedSnapshot<
  TContext extends MachineContext,
  TEvent extends EventObject,
  TChildren extends Record<string, AnyActorRef | undefined>,
  TStateValue extends StateValue,
  TTag extends string,
  TOutput,
  TMeta extends MetaObject
>(
  snapshot: MachineSnapshot<
    TContext,
    TEvent,
    TChildren,
    TStateValue,
    TTag,
    TOutput,
    TMeta,
    any // state schema
  >,
  options?: unknown
): Snapshot<unknown> {
  const {
    _nodes: nodes,
    tags,
    machine,
    children,
    context,
    can,
    hasTag,
    matches,
    getMeta,
    toJSON,
    ...jsonValues
  } = snapshot;

  const childrenJson: Record<string, unknown> = {};

  for (const id in children) {
    const child = children[id] as any;
    if (
      isDevelopment &&
      typeof child.src !== 'string' &&
      (!options || !('__unsafeAllowInlineActors' in (options as object)))
    ) {
      throw new Error('An inline child actor cannot be persisted.');
    }
    childrenJson[id as keyof typeof childrenJson] = {
      snapshot: child.getPersistedSnapshot(options),
      src: child.src,
      systemId: child.systemId,
      syncSnapshot: child._syncSnapshot
    };
  }

  const persisted = {
    ...jsonValues,
    context: persistContext(context) as any,
    children: childrenJson,
    historyValue: serializeHistoryValue<TContext, TEvent>(
      jsonValues.historyValue
    )
  };

  return persisted;
}
```


#### 📄 檔案: `packages/core/src/createActor.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:46, E:17, A:0) ➔ After(N:46, E:17, A:0)
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

### 🔹 函式: `constructor()`
- **變更前簽章 (Before)**: `constructor(
    public logic: TLogic,
    options?: ActorOptions<TLogic>
  )` (L141~L258)
- **變更後簽章 (After)**: `constructor(
    public logic: TLogic,
    options?: ActorOptions<TLogic>
  )` (L141~L258)

#### ◀️ 變更前實作碼 (Before Implementation):
```
constructor(
    public logic: TLogic,
    options?: ActorOptions<TLogic>
  ) {
    const resolvedOptions = {
      ...defaultOptions,
      ...options
    };

    const { clock, logger, parent, syncSnapshot, id, systemId, inspect } =
      resolvedOptions;

    this.system = parent
      ? parent.system
      : createSystem(this, {
          clock,
          logger
        });

    if (inspect && !parent) {
      // Always inspect at the system-level
      this.system.inspect(toObserver(inspect));
    }

    this.sessionId = this.system._bookId();
    this.id = id ?? this.sessionId;
    this.logger = options?.logger ?? this.system._logger;
    this.clock = options?.clock ?? this.system._clock;
    this._parent = parent;
    this._syncSnapshot = syncSnapshot;
    this.options = resolvedOptions as ActorOptions<TLogic> &
      typeof defaultOptions;
    this.src = resolvedOptions.src ?? logic;
    this.ref = this;
    this._actorScope = {
      self: this,
      id: this.id,
      sessionId: this.sessionId,
      logger: this.logger,
      defer: (fn) => {
        this._deferred.push(fn);
      },
      system: this.system,
      stopChild: (child) => {
        if (child._parent !== this) {
          throw new Error(
            `Cannot stop child actor ${child.id} of ${this.id} because it is not a child`
          );
        }
        (child as any)._stop();
      },
      emit: (emittedEvent) => {
        const listeners = this.eventListeners.get(emittedEvent.type);
        const wildcardListener = this.eventListeners.get('*');
        if (!listeners && !wildcardListener) {
          return;
        }
        const allListeners = [
          ...(listeners ? listeners.values() : []),
          ...(wildcardListener ? wildcardListener.values() : [])
        ];
        for (const handler of allListeners) {
          try {
            handler(emittedEvent);
          } catch (err) {
            reportUnhandledError(err);
          }
        }
      },
      actionExecutor: (action) => {
        const exec = () => {
          this._actorScope.system._sendInspectionEvent({
            type: '@xstate.action',
            actorRef: this,
            action: {
              type: action.type,
              params: action.params
            }
          });
          if (!action.exec) {
            return;
          }
          const saveExecutingCustomAction = executingCustomAction;
          try {
            executingCustomAction = true;
            action.exec(action.info, action.params);
          } finally {
            executingCustomAction = saveExecutingCustomAction;
          }
        };
        if (this._processingStatus === ProcessingStatus.Running) {
          exec();
        } else {
          this._deferred.push(exec);
        }
      }
    };

    // Ensure that the send method is bound to this Actor instance
    // if destructured
    this.send = this.send.bind(this);

    this.system._sendInspectionEvent({
      type: '@xstate.actor',
      actorRef: this
    });

    if (systemId) {
      this._systemId = systemId;
      this.system._set(systemId, this);
    }

    this._initState(options?.snapshot ?? options?.state);

    if (systemId && (this._snapshot as any).status !== 'active') {
      this.system._unregister(this);
    }
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
constructor(
    public logic: TLogic,
    options?: ActorOptions<TLogic>
  ) {
    const resolvedOptions = {
      ...defaultOptions,
      ...options
    };

    const { clock, logger, parent, syncSnapshot, id, systemId, inspect } =
      resolvedOptions;

    this.system = parent
      ? parent.system
      : createSystem(this, {
          clock,
          logger
        });

    if (inspect && !parent) {
      // Always inspect at the system-level
      this.system.inspect(toObserver(inspect));
    }

    this.sessionId = this.system._bookId();
    this.id = id ?? this.sessionId;
    this.logger = options?.logger ?? this.system._logger;
    this.clock = options?.clock ?? this.system._clock;
    this._parent = parent;
    this._syncSnapshot = syncSnapshot;
    this.options = resolvedOptions as ActorOptions<TLogic> &
      typeof defaultOptions;
    this.src = resolvedOptions.src ?? logic;
    this.ref = this;
    this._actorScope = {
      self: this,
      id: this.id,
      sessionId: this.sessionId,
      logger: this.logger,
      defer: (fn) => {
        this._deferred.push(fn);
      },
      system: this.system,
      stopChild: (child) => {
        if (child._parent !== this) {
          throw new Error(
            `Cannot stop child actor ${child.id} of ${this.id} because it is not a child`
          );
        }
        (child as any)._stop();
      },
      emit: (emittedEvent) => {
        const listeners = this.eventListeners.get(emittedEvent.type);
        const wildcardListener = this.eventListeners.get('*');
        if (!listeners && !wildcardListener) {
          return;
        }
        const allListeners = [
          ...(listeners ? listeners.values() : []),
          ...(wildcardListener ? wildcardListener.values() : [])
        ];
        for (const handler of allListeners) {
          try {
            handler(emittedEvent);
          } catch (err) {
            reportUnhandledError(err);
          }
        }
      },
      actionExecutor: (action) => {
        const exec = () => {
          this._actorScope.system._sendInspectionEvent({
            type: '@xstate.action',
            actorRef: this,
            action: {
              type: action.type,
              params: action.params
            }
          });
          if (!action.exec) {
            return;
          }
          const saveExecutingCustomAction = executingCustomAction;
          try {
            executingCustomAction = true;
            action.exec(action.info, action.params);
          } finally {
            executingCustomAction = saveExecutingCustomAction;
          }
        };
        if (this._processingStatus === ProcessingStatus.Running) {
          exec();
        } else {
          this._deferred.push(exec);
        }
      }
    };

    // Ensure that the send method is bound to this Actor instance
    // if destructured
    this.send = this.send.bind(this);

    this.system._sendInspectionEvent({
      type: '@xstate.actor',
      actorRef: this
    });

    if (systemId) {
      this.systemId = systemId;
      this.system._set(systemId, this);
    }

    this._initState(options?.snapshot ?? options?.state);

    if (systemId && (this._snapshot as any).status !== 'active') {
      this.system._unregister(this);
    }
  }
```

### 🔹 函式: `start()`
- **變更前簽章 (Before)**: `start()` (L490~L573)
- **變更後簽章 (After)**: `start()` (L490~L573)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public start(): this {
    if (this._processingStatus === ProcessingStatus.Running) {
      // Do not restart the service if it is already started
      return this;
    }

    if (this._syncSnapshot) {
      this.subscribe({
        next: (snapshot: Snapshot<unknown>) => {
          if (snapshot.status === 'active') {
            this.system._relay(this, this._parent!, {
              type: `xstate.snapshot.${this.id}`,
              snapshot
            });
          }
        },
        error: () => {}
      });
    }

    this.system._register(this.sessionId, this);
    if (this._systemId) {
      this.system._set(this._systemId, this);
    }
    this._processingStatus = ProcessingStatus.Running;

    // TODO: this isn't correct when rehydrating
    const initEvent = createInitEvent(this.options.input);

    this.system._sendInspectionEvent({
      type: '@xstate.event',
      sourceRef: this._parent,
      actorRef: this,
      event: initEvent
    });

    const status = (this._snapshot as any).status;

    switch (status) {
      case 'done':
        // a state machine can be "done" upon initialization (it could reach a final state using initial microsteps)
        // we still need to complete observers, flush deferreds etc
        this.update(
          this._snapshot,
          initEvent as unknown as EventFromLogic<TLogic>
        );
        // TODO: rethink cleanup of observers, mailbox, etc
        return this;
      case 'error':
        this._error((this._snapshot as any).error);
        return this;
    }

    if (!this._parent) {
      this.system.start();
    }

    if (this.logic.start) {
      try {
        this.logic.start(this._snapshot, this._actorScope);
      } catch (err) {
        this._snapshot = {
          ...(this._snapshot as any),
          status: 'error',
          error: err
        };
        this._error(err);
        return this;
      }
    }

    // TODO: this notifies all subscribers but usually this is redundant
    // there is no real change happening here
    // we need to rethink if this needs to be refactored
    this.update(this._snapshot, initEvent as unknown as EventFromLogic<TLogic>);

    if (this.options.devTools) {
      this.attachDevTools();
    }

    this.mailbox.start();

    return this;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public start(): this {
    if (this._processingStatus === ProcessingStatus.Running) {
      // Do not restart the service if it is already started
      return this;
    }

    if (this._syncSnapshot) {
      this.subscribe({
        next: (snapshot: Snapshot<unknown>) => {
          if (snapshot.status === 'active') {
            this.system._relay(this, this._parent!, {
              type: `xstate.snapshot.${this.id}`,
              snapshot
            });
          }
        },
        error: () => {}
      });
    }

    this.system._register(this.sessionId, this);
    if (this.systemId) {
      this.system._set(this.systemId, this);
    }
    this._processingStatus = ProcessingStatus.Running;

    // TODO: this isn't correct when rehydrating
    const initEvent = createInitEvent(this.options.input);

    this.system._sendInspectionEvent({
      type: '@xstate.event',
      sourceRef: this._parent,
      actorRef: this,
      event: initEvent
    });

    const status = (this._snapshot as any).status;

    switch (status) {
      case 'done':
        // a state machine can be "done" upon initialization (it could reach a final state using initial microsteps)
        // we still need to complete observers, flush deferreds etc
        this.update(
          this._snapshot,
          initEvent as unknown as EventFromLogic<TLogic>
        );
        // TODO: rethink cleanup of observers, mailbox, etc
        return this;
      case 'error':
        this._error((this._snapshot as any).error);
        return this;
    }

    if (!this._parent) {
      this.system.start();
    }

    if (this.logic.start) {
      try {
        this.logic.start(this._snapshot, this._actorScope);
      } catch (err) {
        this._snapshot = {
          ...(this._snapshot as any),
          status: 'error',
          error: err
        };
        this._error(err);
        return this;
      }
    }

    // TODO: this notifies all subscribers but usually this is redundant
    // there is no real change happening here
    // we need to rethink if this needs to be refactored
    this.update(this._snapshot, initEvent as unknown as EventFromLogic<TLogic>);

    if (this.options.devTools) {
      this.attachDevTools();
    }

    this.mailbox.start();

    return this;
  }
```


---

### 🔹 Commit #17: `15e15b5e`
- **完整 Hash**: `15e15b5e38e2fb3c2bd67ae584aa4e019d12699c`
- **說明 (Ground Truth)**: [core] Add `.createStateConfig(…)` to machine setup (#5364)
- **變更檔案數**: 1

#### 📄 檔案: `packages/core/src/setup.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:2, E:0, A:0) ➔ After(N:3, E:0, A:0)
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
  • + [新增節點] `createStateConfig` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `setup()`
- **變更前簽章 (Before)**: `function setup<
  TContext extends MachineContext,
  TEvent extends AnyEventObject, // TODO: consider using a stricter `EventObject` here
  TActors extends Record<string, UnknownActorLogic> =` (L72~L196)
- **變更後簽章 (After)**: `function setup<
  TContext extends MachineContext,
  TEvent extends AnyEventObject, // TODO: consider using a stricter `EventObject` here
  TActors extends Record<string, UnknownActorLogic> =` (L73~L243)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function setup<
  TContext extends MachineContext,
  TEvent extends AnyEventObject, // TODO: consider using a stricter `EventObject` here
  TActors extends Record<string, UnknownActorLogic> = {},
  TChildrenMap extends Record<string, string> = {},
  TActions extends Record<
    string,
    ParameterizedObject['params'] | undefined
  > = {},
  TGuards extends Record<
    string,
    ParameterizedObject['params'] | undefined
  > = {},
  TDelay extends string = never,
  TTag extends string = string,
  TInput = NonReducibleUnknown,
  TOutput extends NonReducibleUnknown = NonReducibleUnknown,
  TEmitted extends EventObject = EventObject,
  TMeta extends MetaObject = MetaObject
>({
  schemas,
  actors,
  actions,
  guards,
  delays
}: {
  schemas?: unknown;
  types?: SetupTypes<
    TContext,
    TEvent,
    TChildrenMap,
    TTag,
    TInput,
    TOutput,
    TEmitted,
    TMeta
  >;
  actors?: {
    // union here enforces that all configured children have to be provided in actors
    // it makes those values required here
    [K in keyof TActors | Values<TChildrenMap>]: K extends keyof TActors
      ? TActors[K]
      : never;
  };
  actions?: {
    [K in keyof TActions]: ActionFunction<
      TContext,
      TEvent,
      TEvent,
      TActions[K],
      ToProvidedActor<TChildrenMap, TActors>,
      ToParameterizedObject<TActions>,
      ToParameterizedObject<TGuards>,
      TDelay,
      TEmitted
    >;
  };
  guards?: {
    [K in keyof TGuards]: GuardPredicate<
      TContext,
      TEvent,
      TGuards[K],
      ToParameterizedObject<TGuards>
    >;
  };
  delays?: {
    [K in TDelay]: DelayConfig<
      TContext,
      TEvent,
      ToParameterizedObject<TActions>['params'],
      TEvent
    >;
  };
} & {
  [K in RequiredSetupKeys<TChildrenMap>]: unknown;
}): {
  createMachine: <
    const TConfig extends MachineConfig<
      TContext,
      TEvent,
      ToProvidedActor<TChildrenMap, TActors>,
      ToParameterizedObject<TActions>,
      ToParameterizedObject<TGuards>,
      TDelay,
      TTag,
      TInput,
      TOutput,
      TEmitted,
      TMeta
    >
  >(
    config: TConfig
  ) => StateMachine<
    TContext,
    TEvent,
    Cast<
      ToChildren<ToProvidedActor<TChildrenMap, TActors>>,
      Record<string, AnyActorRef | undefined>
    >,
    ToProvidedActor<TChildrenMap, TActors>,
    ToParameterizedObject<TActions>,
    ToParameterizedObject<TGuards>,
    TDelay,
    ToStateValue<TConfig>,
    TTag,
    TInput,
    TOutput,
    TEmitted,
    TMeta,
    TConfig
  >;
} {
  return {
    createMachine: (config) =>
      (createMachine as any)(
        { ...config, schemas },
        {
          actors,
          actions,
          guards,
          delays
        }
      )
  };
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function setup<
  TContext extends MachineContext,
  TEvent extends AnyEventObject, // TODO: consider using a stricter `EventObject` here
  TActors extends Record<string, UnknownActorLogic> = {},
  TChildrenMap extends Record<string, string> = {},
  TActions extends Record<
    string,
    ParameterizedObject['params'] | undefined
  > = {},
  TGuards extends Record<
    string,
    ParameterizedObject['params'] | undefined
  > = {},
  TDelay extends string = never,
  TTag extends string = string,
  TInput = NonReducibleUnknown,
  TOutput extends NonReducibleUnknown = NonReducibleUnknown,
  TEmitted extends EventObject = EventObject,
  TMeta extends MetaObject = MetaObject
>({
  schemas,
  actors,
  actions,
  guards,
  delays
}: {
  schemas?: unknown;
  types?: SetupTypes<
    TContext,
    TEvent,
    TChildrenMap,
    TTag,
    TInput,
    TOutput,
    TEmitted,
    TMeta
  >;
  actors?: {
    // union here enforces that all configured children have to be provided in actors
    // it makes those values required here
    [K in keyof TActors | Values<TChildrenMap>]: K extends keyof TActors
      ? TActors[K]
      : never;
  };
  actions?: {
    [K in keyof TActions]: ActionFunction<
      TContext,
      TEvent,
      TEvent,
      TActions[K],
      ToProvidedActor<TChildrenMap, TActors>,
      ToParameterizedObject<TActions>,
      ToParameterizedObject<TGuards>,
      TDelay,
      TEmitted
    >;
  };
  guards?: {
    [K in keyof TGuards]: GuardPredicate<
      TContext,
      TEvent,
      TGuards[K],
      ToParameterizedObject<TGuards>
    >;
  };
  delays?: {
    [K in TDelay]: DelayConfig<
      TContext,
      TEvent,
      ToParameterizedObject<TActions>['params'],
      TEvent
    >;
  };
} & {
  [K in RequiredSetupKeys<TChildrenMap>]: unknown;
}): {
  /**
   * Creates a state config that is strongly typed. This state config can be
   * used to create a machine.
   *
   * @example
   *
   * ```ts
   * const lightMachineSetup = setup({
   *   // ...
   * });
   *
   * const green = lightMachineSetup.createStateConfig({
   *   on: {
   *     timer: {
   *       actions: 'doSomething'
   *     }
   *   }
   * });
   *
   * const machine = lightMachineSetup.createMachine({
   *   initial: 'green',
   *   states: {
   *     green,
   *     yellow,
   *     red
   *   }
   * });
   * ```
   */
  createStateConfig: <
    TStateConfig extends StateNodeConfig<
      TContext,
      TEvent,
      ToProvidedActor<TChildrenMap, TActors>,
      ToParameterizedObject<TActions>,
      ToParameterizedObject<TGuards>,
      TDelay,
      TTag,
      unknown,
      TEmitted,
      TMeta
    >
  >(
    config: TStateConfig
  ) => TStateConfig;
  createMachine: <
    const TConfig extends MachineConfig<
      TContext,
      TEvent,
      ToProvidedActor<TChildrenMap, TActors>,
      ToParameterizedObject<TActions>,
      ToParameterizedObject<TGuards>,
      TDelay,
      TTag,
      TInput,
      TOutput,
      TEmitted,
      TMeta
    >
  >(
    config: TConfig
  ) => StateMachine<
    TContext,
    TEvent,
    Cast<
      ToChildren<ToProvidedActor<TChildrenMap, TActors>>,
      Record<string, AnyActorRef | undefined>
    >,
    ToProvidedActor<TChildrenMap, TActors>,
    ToParameterizedObject<TActions>,
    ToParameterizedObject<TGuards>,
    TDelay,
    ToStateValue<TConfig>,
    TTag,
    TInput,
    TOutput,
    TEmitted,
    TMeta,
    TConfig
  >;
} {
  return {
    createStateConfig: (config) => config,
    createMachine: (config) =>
      (createMachine as any)(
        { ...config, schemas },
        {
          actors,
          actions,
          guards,
          delays
        }
      )
  };
}
```


---

### 🔹 Commit #18: `71387ff0`
- **完整 Hash**: `71387ff0af86715fe233c33236fe6e6a8746e56f`
- **說明 (Ground Truth)**: [core] Fix emit callback error crashing actor (#5351)
- **變更檔案數**: 1

#### 📄 檔案: `packages/core/src/createActor.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:46, E:16, A:0) ➔ After(N:46, E:17, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `emit` ──[CALLS [guarded]]──> `reportUnhandledError (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `constructor()`
- **變更前簽章 (Before)**: `constructor(
    public logic: TLogic,
    options?: ActorOptions<TLogic>
  )` (L141~L254)
- **變更後簽章 (After)**: `constructor(
    public logic: TLogic,
    options?: ActorOptions<TLogic>
  )` (L141~L258)

#### ◀️ 變更前實作碼 (Before Implementation):
```
constructor(
    public logic: TLogic,
    options?: ActorOptions<TLogic>
  ) {
    const resolvedOptions = {
      ...defaultOptions,
      ...options
    };

    const { clock, logger, parent, syncSnapshot, id, systemId, inspect } =
      resolvedOptions;

    this.system = parent
      ? parent.system
      : createSystem(this, {
          clock,
          logger
        });

    if (inspect && !parent) {
      // Always inspect at the system-level
      this.system.inspect(toObserver(inspect));
    }

    this.sessionId = this.system._bookId();
    this.id = id ?? this.sessionId;
    this.logger = options?.logger ?? this.system._logger;
    this.clock = options?.clock ?? this.system._clock;
    this._parent = parent;
    this._syncSnapshot = syncSnapshot;
    this.options = resolvedOptions as ActorOptions<TLogic> &
      typeof defaultOptions;
    this.src = resolvedOptions.src ?? logic;
    this.ref = this;
    this._actorScope = {
      self: this,
      id: this.id,
      sessionId: this.sessionId,
      logger: this.logger,
      defer: (fn) => {
        this._deferred.push(fn);
      },
      system: this.system,
      stopChild: (child) => {
        if (child._parent !== this) {
          throw new Error(
            `Cannot stop child actor ${child.id} of ${this.id} because it is not a child`
          );
        }
        (child as any)._stop();
      },
      emit: (emittedEvent) => {
        const listeners = this.eventListeners.get(emittedEvent.type);
        const wildcardListener = this.eventListeners.get('*');
        if (!listeners && !wildcardListener) {
          return;
        }
        const allListeners = [
          ...(listeners ? listeners.values() : []),
          ...(wildcardListener ? wildcardListener.values() : [])
        ];
        for (const handler of allListeners) {
          handler(emittedEvent);
        }
      },
      actionExecutor: (action) => {
        const exec = () => {
          this._actorScope.system._sendInspectionEvent({
            type: '@xstate.action',
            actorRef: this,
            action: {
              type: action.type,
              params: action.params
            }
          });
          if (!action.exec) {
            return;
          }
          const saveExecutingCustomAction = executingCustomAction;
          try {
            executingCustomAction = true;
            action.exec(action.info, action.params);
          } finally {
            executingCustomAction = saveExecutingCustomAction;
          }
        };
        if (this._processingStatus === ProcessingStatus.Running) {
          exec();
        } else {
          this._deferred.push(exec);
        }
      }
    };

    // Ensure that the send method is bound to this Actor instance
    // if destructured
    this.send = this.send.bind(this);

    this.system._sendInspectionEvent({
      type: '@xstate.actor',
      actorRef: this
    });

    if (systemId) {
      this._systemId = systemId;
      this.system._set(systemId, this);
    }

    this._initState(options?.snapshot ?? options?.state);

    if (systemId && (this._snapshot as any).status !== 'active') {
      this.system._unregister(this);
    }
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
constructor(
    public logic: TLogic,
    options?: ActorOptions<TLogic>
  ) {
    const resolvedOptions = {
      ...defaultOptions,
      ...options
    };

    const { clock, logger, parent, syncSnapshot, id, systemId, inspect } =
      resolvedOptions;

    this.system = parent
      ? parent.system
      : createSystem(this, {
          clock,
          logger
        });

    if (inspect && !parent) {
      // Always inspect at the system-level
      this.system.inspect(toObserver(inspect));
    }

    this.sessionId = this.system._bookId();
    this.id = id ?? this.sessionId;
    this.logger = options?.logger ?? this.system._logger;
    this.clock = options?.clock ?? this.system._clock;
    this._parent = parent;
    this._syncSnapshot = syncSnapshot;
    this.options = resolvedOptions as ActorOptions<TLogic> &
      typeof defaultOptions;
    this.src = resolvedOptions.src ?? logic;
    this.ref = this;
    this._actorScope = {
      self: this,
      id: this.id,
      sessionId: this.sessionId,
      logger: this.logger,
      defer: (fn) => {
        this._deferred.push(fn);
      },
      system: this.system,
      stopChild: (child) => {
        if (child._parent !== this) {
          throw new Error(
            `Cannot stop child actor ${child.id} of ${this.id} because it is not a child`
          );
        }
        (child as any)._stop();
      },
      emit: (emittedEvent) => {
        const listeners = this.eventListeners.get(emittedEvent.type);
        const wildcardListener = this.eventListeners.get('*');
        if (!listeners && !wildcardListener) {
          return;
        }
        const allListeners = [
          ...(listeners ? listeners.values() : []),
          ...(wildcardListener ? wildcardListener.values() : [])
        ];
        for (const handler of allListeners) {
          try {
            handler(emittedEvent);
          } catch (err) {
            reportUnhandledError(err);
          }
        }
      },
      actionExecutor: (action) => {
        const exec = () => {
          this._actorScope.system._sendInspectionEvent({
            type: '@xstate.action',
            actorRef: this,
            action: {
              type: action.type,
              params: action.params
            }
          });
          if (!action.exec) {
            return;
          }
          const saveExecutingCustomAction = executingCustomAction;
          try {
            executingCustomAction = true;
            action.exec(action.info, action.params);
          } finally {
            executingCustomAction = saveExecutingCustomAction;
          }
        };
        if (this._processingStatus === ProcessingStatus.Running) {
          exec();
        } else {
          this._deferred.push(exec);
        }
      }
    };

    // Ensure that the send method is bound to this Actor instance
    // if destructured
    this.send = this.send.bind(this);

    this.system._sendInspectionEvent({
      type: '@xstate.actor',
      actorRef: this
    });

    if (systemId) {
      this._systemId = systemId;
      this.system._set(systemId, this);
    }

    this._initState(options?.snapshot ?? options?.state);

    if (systemId && (this._snapshot as any).status !== 'active') {
      this.system._unregister(this);
    }
  }
```

### 🔹 函式: `emit()`
- **變更前簽章 (Before)**: `emit(emittedEvent)` (L192~L205)
- **變更後簽章 (After)**: `emit(emittedEvent)` (L192~L209)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(emittedEvent) => {
        const listeners = this.eventListeners.get(emittedEvent.type);
        const wildcardListener = this.eventListeners.get('*');
        if (!listeners && !wildcardListener) {
          return;
        }
        const allListeners = [
          ...(listeners ? listeners.values() : []),
          ...(wildcardListener ? wildcardListener.values() : [])
        ];
        for (const handler of allListeners) {
          handler(emittedEvent);
        }
      }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(emittedEvent) => {
        const listeners = this.eventListeners.get(emittedEvent.type);
        const wildcardListener = this.eventListeners.get('*');
        if (!listeners && !wildcardListener) {
          return;
        }
        const allListeners = [
          ...(listeners ? listeners.values() : []),
          ...(wildcardListener ? wildcardListener.values() : [])
        ];
        for (const handler of allListeners) {
          try {
            handler(emittedEvent);
          } catch (err) {
            reportUnhandledError(err);
          }
        }
      }
```


---

### 🔹 Commit #19: `e8891030`
- **完整 Hash**: `e8891030162214acc751a9f79a5d57ec916565ee`
- **說明 (Ground Truth)**: [@xstate/store] Fix distributive event payload types (#5247)
- **變更檔案數**: 1

#### 📄 檔案: `packages/xstate-store/src/types.ts`
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

### 🔹 Commit #20: `13279166`
- **完整 Hash**: `13279166ed9fa3d3626a2129bd257f6cd663fd0e`
- **說明 (Ground Truth)**: [@xstate/store] Add `store.transition(…)` API (#5215)
- **變更檔案數**: 2

#### 📄 檔案: `packages/xstate-store/src/store.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:37, E:19, A:0) ➔ After(N:37, E:19, A:0)
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
  - 💥 作用域阻隔: 函式 'effect' 被深鎖在內部閉包 (scope:arrow@after/packages/xstate-store/src/store.ts:L471C10)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `createStoreCore()`
- **變更前簽章 (Before)**: `function createStoreCore<
  TContext extends StoreContext,
  TEventPayloadMap extends EventPayloadMap,
  TEmitted extends EventObject
>(
  initialContext: TContext,
  transitions:` (L45~L228)
- **變更後簽章 (After)**: `function createStoreCore<
  TContext extends StoreContext,
  TEventPayloadMap extends EventPayloadMap,
  TEmitted extends EventObject
>(
  initialContext: TContext,
  transitions:` (L45~L229)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createStoreCore<
  TContext extends StoreContext,
  TEventPayloadMap extends EventPayloadMap,
  TEmitted extends EventObject
>(
  initialContext: TContext,
  transitions: {
    [K in keyof TEventPayloadMap & string]: StoreAssigner<
      NoInfer<TContext>,
      { type: K } & TEventPayloadMap[K],
      TEmitted
    >;
  },
  emits?: Record<string, (payload: any) => void>, // TODO: improve this type
  producer?: (
    context: NoInfer<TContext>,
    recipe: (context: NoInfer<TContext>) => void
  ) => NoInfer<TContext>
): Store<TContext, ExtractEvents<TEventPayloadMap>, TEmitted> {
  type StoreEvent = ExtractEvents<TEventPayloadMap>;
  let observers: Set<Observer<StoreSnapshot<TContext>>> | undefined;
  let listeners: Map<TEmitted['type'], Set<any>> | undefined;
  const initialSnapshot: StoreSnapshot<TContext> = {
    context: initialContext,
    status: 'active',
    output: undefined,
    error: undefined
  };
  let currentSnapshot: StoreSnapshot<TContext> = initialSnapshot;

  const emit = (ev: TEmitted) => {
    if (!listeners) {
      return;
    }
    const type = ev.type;
    const typeListeners = listeners.get(type);
    if (typeListeners) {
      typeListeners.forEach((listener) => listener(ev));
    }
  };

  const transition = createStoreTransition(transitions, producer);

  function receive(event: StoreEvent) {
    let effects: StoreEffect<TEmitted>[];
    [currentSnapshot, effects] = transition(currentSnapshot, event);

    inspectionObservers.get(store)?.forEach((observer) => {
      observer.next?.({
        type: '@xstate.snapshot',
        event,
        snapshot: currentSnapshot,
        actorRef: store,
        rootId: store.sessionId
      });
    });

    observers?.forEach((o) => o.next?.(currentSnapshot));

    for (const effect of effects) {
      if (typeof effect === 'function') {
        effect();
      } else {
        // handle the inherent effect first
        emits?.[effect.type]?.(effect);
        emit(effect);
      }
    }
  }

  const store: Store<TContext, StoreEvent, TEmitted> = {
    on(emittedEventType, handler) {
      if (!listeners) {
        listeners = new Map();
      }
      let eventListeners = listeners.get(emittedEventType);
      if (!eventListeners) {
        eventListeners = new Set();
        listeners.set(emittedEventType, eventListeners);
      }
      const wrappedHandler = handler.bind(undefined);
      eventListeners.add(wrappedHandler);

      return {
        unsubscribe() {
          eventListeners.delete(wrappedHandler);
        }
      };
    },
    sessionId: uniqueId(),
    send(event) {
      inspectionObservers.get(store)?.forEach((observer) => {
        observer.next?.({
          type: '@xstate.event',
          event,
          sourceRef: undefined,
          actorRef: store,
          rootId: store.sessionId
        });
      });
      receive(event as unknown as StoreEvent);
    },
    getSnapshot() {
      return currentSnapshot;
    },
    getInitialSnapshot() {
      return initialSnapshot;
    },
    subscribe(observerOrFn) {
      const observer = toObserver(observerOrFn);
      observers ??= new Set();
      observers.add(observer);

      return {
        unsubscribe() {
          return observers?.delete(observer);
        }
      };
    },
    [symbolObservable](): InteropSubscribable<StoreSnapshot<TContext>> {
      return this;
    },
    inspect: (observerOrFn) => {
      const observer = toObserver(observerOrFn);
      inspectionObservers.set(
        store,
        inspectionObservers.get(store) ?? new Set()
      );
      inspectionObservers.get(store)!.add(observer);

      observer.next?.({
        type: '@xstate.actor',
        actorRef: store,
        rootId: store.sessionId
      });

      observer.next?.({
        type: '@xstate.snapshot',
        snapshot: initialSnapshot,
        event: { type: '@xstate.init' },
        actorRef: store,
        rootId: store.sessionId
      });

      return {
        unsubscribe() {
          return inspectionObservers.get(store)?.delete(observer);
        }
      };
    },
    trigger: new Proxy({} as Store<TContext, StoreEvent, TEmitted>['trigger'], {
      get: (_, eventType: string) => {
        return (payload: any) => {
          store.send({
            type: eventType,
            ...payload
          });
        };
      }
    }),
    select<TSelected>(
      selector: Selector<TContext, TSelected>,
      equalityFn: (a: TSelected, b: TSelected) => boolean = Object.is
    ): Selection<TSelected> {
      return {
        subscribe: (observerOrFn) => {
          const observer = toObserver(observerOrFn);
          let previousSelected = selector(this.getSnapshot().context);

          return this.subscribe((snapshot) => {
            const nextSelected = selector(snapshot.context);
            if (!equalityFn(previousSelected, nextSelected)) {
              previousSelected = nextSelected;
              observer.next?.(nextSelected);
            }
          });
        },
        get: () => selector(this.getSnapshot().context)
      };
    }
  };

  return store;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createStoreCore<
  TContext extends StoreContext,
  TEventPayloadMap extends EventPayloadMap,
  TEmitted extends EventObject
>(
  initialContext: TContext,
  transitions: {
    [K in keyof TEventPayloadMap & string]: StoreAssigner<
      NoInfer<TContext>,
      { type: K } & TEventPayloadMap[K],
      TEmitted
    >;
  },
  emits?: Record<string, (payload: any) => void>, // TODO: improve this type
  producer?: (
    context: NoInfer<TContext>,
    recipe: (context: NoInfer<TContext>) => void
  ) => NoInfer<TContext>
): Store<TContext, ExtractEvents<TEventPayloadMap>, TEmitted> {
  type StoreEvent = ExtractEvents<TEventPayloadMap>;
  let observers: Set<Observer<StoreSnapshot<TContext>>> | undefined;
  let listeners: Map<TEmitted['type'], Set<any>> | undefined;
  const initialSnapshot: StoreSnapshot<TContext> = {
    context: initialContext,
    status: 'active',
    output: undefined,
    error: undefined
  };
  let currentSnapshot: StoreSnapshot<TContext> = initialSnapshot;

  const emit = (ev: TEmitted) => {
    if (!listeners) {
      return;
    }
    const type = ev.type;
    const typeListeners = listeners.get(type);
    if (typeListeners) {
      typeListeners.forEach((listener) => listener(ev));
    }
  };

  const transition = createStoreTransition(transitions, producer);

  function receive(event: StoreEvent) {
    let effects: StoreEffect<TEmitted>[];
    [currentSnapshot, effects] = transition(currentSnapshot, event);

    inspectionObservers.get(store)?.forEach((observer) => {
      observer.next?.({
        type: '@xstate.snapshot',
        event,
        snapshot: currentSnapshot,
        actorRef: store,
        rootId: store.sessionId
      });
    });

    observers?.forEach((o) => o.next?.(currentSnapshot));

    for (const effect of effects) {
      if (typeof effect === 'function') {
        effect();
      } else {
        // handle the inherent effect first
        emits?.[effect.type]?.(effect);
        emit(effect);
      }
    }
  }

  const store: Store<TContext, StoreEvent, TEmitted> = {
    on(emittedEventType, handler) {
      if (!listeners) {
        listeners = new Map();
      }
      let eventListeners = listeners.get(emittedEventType);
      if (!eventListeners) {
        eventListeners = new Set();
        listeners.set(emittedEventType, eventListeners);
      }
      const wrappedHandler = handler.bind(undefined);
      eventListeners.add(wrappedHandler);

      return {
        unsubscribe() {
          eventListeners.delete(wrappedHandler);
        }
      };
    },
    transition,
    sessionId: uniqueId(),
    send(event) {
      inspectionObservers.get(store)?.forEach((observer) => {
        observer.next?.({
          type: '@xstate.event',
          event,
          sourceRef: undefined,
          actorRef: store,
          rootId: store.sessionId
        });
      });
      receive(event as unknown as StoreEvent);
    },
    getSnapshot() {
      return currentSnapshot;
    },
    getInitialSnapshot() {
      return initialSnapshot;
    },
    subscribe(observerOrFn) {
      const observer = toObserver(observerOrFn);
      observers ??= new Set();
      observers.add(observer);

      return {
        unsubscribe() {
          return observers?.delete(observer);
        }
      };
    },
    [symbolObservable](): InteropSubscribable<StoreSnapshot<TContext>> {
      return this;
    },
    inspect: (observerOrFn) => {
      const observer = toObserver(observerOrFn);
      inspectionObservers.set(
        store,
        inspectionObservers.get(store) ?? new Set()
      );
      inspectionObservers.get(store)!.add(observer);

      observer.next?.({
        type: '@xstate.actor',
        actorRef: store,
        rootId: store.sessionId
      });

      observer.next?.({
        type: '@xstate.snapshot',
        snapshot: initialSnapshot,
        event: { type: '@xstate.init' },
        actorRef: store,
        rootId: store.sessionId
      });

      return {
        unsubscribe() {
          return inspectionObservers.get(store)?.delete(observer);
        }
      };
    },
    trigger: new Proxy({} as Store<TContext, StoreEvent, TEmitted>['trigger'], {
      get: (_, eventType: string) => {
        return (payload: any) => {
          store.send({
            type: eventType,
            ...payload
          });
        };
      }
    }),
    select<TSelected>(
      selector: Selector<TContext, TSelected>,
      equalityFn: (a: TSelected, b: TSelected) => boolean = Object.is
    ): Selection<TSelected> {
      return {
        subscribe: (observerOrFn) => {
          const observer = toObserver(observerOrFn);
          let previousSelected = selector(this.getSnapshot().context);

          return this.subscribe((snapshot) => {
            const nextSelected = selector(snapshot.context);
            if (!equalityFn(previousSelected, nextSelected)) {
              previousSelected = nextSelected;
              observer.next?.(nextSelected);
            }
          });
        },
        get: () => selector(this.getSnapshot().context)
      };
    }
  };

  return store;
}
```


#### 📄 檔案: `packages/xstate-store/src/types.ts`
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

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/xstate show 016daa76a45c4baaeade00034996f2617b45a7fa
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 016daa76a45c4baaeade00034996f2617b45a7fa~1 --file test_repos/xstate/packages/xstate-vue/src/useSelector.ts
   ```
