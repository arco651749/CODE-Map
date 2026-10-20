# 🔬 CODE-Map 基準審查獨立驗證報告: `bevy`
> **技術生態**: `Rust (ECS 遊戲引擎 / 資料導向排程器)`  
> **本地倉庫路徑**: `test_repos/bevy`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 35 Files  
> **報告生成時間**: 2026-10-20 21:44:53  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `26` / `35` | `74.3%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `3` / `35` | `8.6%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `6` / `35` | `17.1%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`29` / `35`** | **`82.9%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `35` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `36d1b051`
- **完整 Hash**: `36d1b0514127c6b416180bded0799ef01a33dc68`
- **說明 (Ground Truth)**: Fix AssetSaver docs not mentioning `save_using_saver`. (#26203)
- **變更檔案數**: 1

#### 📄 檔案: `crates/bevy_asset/src/saver.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:176, E:249, A:0) ➔ After(N:176, E:249, A:0)
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

### 🔹 Commit #02: `d0fb069d`
- **完整 Hash**: `d0fb069d6ee3b9fa138df8b6e2ca6d430b3de51a`
- **說明 (Ground Truth)**: Improving docs for `Named Entity References` (the `#MyName` inside `bsn`) (#26179)
- **變更檔案數**: 1

#### 📄 檔案: `crates/bevy_scene/src/lib.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:451, E:855, A:0) ➔ After(N:451, E:855, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

ℹ️ **存量環境提醒**: 檔案內含 2 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #03: `c01a7fa4`
- **完整 Hash**: `c01a7fa4a2a34b9e52f2598cd8a072dc75ab07d0`
- **說明 (Ground Truth)**: Fix unneeded uniqueness check in parallel query iterators (#26135)
- **變更檔案數**: 2

#### 📄 檔案: `crates/bevy_ecs/src/query/mod.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:271, E:368, A:0) ➔ After(N:290, E:391, A:0)
- **差分統計**: +Nodes: 19, -Nodes: 0, +Edges: 23, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state.get_mut(&mut world).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `query.par_iter_many_unique (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `entities.iter().copied().step_by(2).collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.spawn_batch((0..1000).map(|i| (A(i), B(0)))).collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `par_iter_many_unique_visits_each_listed_entity_once` (FUNCTION_DEF)
  • + [新增節點] `AtomicUsize::new (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `entities.iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `(0..1000).map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `SystemState::<Query<(&A, &mut B)>>::new (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `entities.iter().enumerate (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `bevy_tasks::ComputeTaskPool::get_or_init (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `query.par_iter_many_unique_mut (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `entities.iter().copied (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `entities.iter().copied().step_by (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `query.par_iter_many_unique(&subset).for_each (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 27 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `crates/bevy_ecs/src/system/query.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:139, E:182, A:0) ➔ After(N:140, E:182, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 2, -Edges: 2, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `entities.into_iter().collect_set (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Query::par_iter_many_unique` ──[CALLS]──> `entities.into_iter().collect_set (External/Unresolved)`
  • + [新增呼叫邊] `Query::par_iter_many_unique_mut` ──[CALLS]──> `entities.into_iter().collect_set (External/Unresolved)`
  • - [移除呼叫邊] `Query::par_iter_many_unique` ──[CALLS]──> `entities.into_iter().collect (External/Unresolved)`
  • - [移除呼叫邊] `Query::par_iter_many_unique_mut` ──[CALLS]──> `entities.into_iter().collect (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Query::par_iter_many_unique_mut()`
- **變更前簽章 (Before)**: `fn Query::par_iter_many_unique_mut(
        &mut self,
        entities: EntityList,
    )` (L1461~L1476)
- **變更後簽章 (After)**: `fn Query::par_iter_many_unique_mut(
        &mut self,
        entities: EntityList,
    )` (L1461~L1476)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn par_iter_many_unique_mut<EntityList: EntitySet<Item: Sync>>(
        &mut self,
        entities: EntityList,
    ) -> QueryParManyUniqueIter<'_, 's, D, F, EntityList::Item>
    where
        D: IterQueryData,
    {
        QueryParManyUniqueIter {
            world: self.world,
            state: self.state,
            entity_list: entities.into_iter().collect(),
            last_run: self.last_run,
            this_run: self.this_run,
            batching_strategy: BatchingStrategy::new(),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn par_iter_many_unique_mut<EntityList: EntitySet<Item: Sync>>(
        &mut self,
        entities: EntityList,
    ) -> QueryParManyUniqueIter<'_, 's, D, F, EntityList::Item>
    where
        D: IterQueryData,
    {
        QueryParManyUniqueIter {
            world: self.world,
            state: self.state,
            entity_list: entities.into_iter().collect_set(),
            last_run: self.last_run,
            this_run: self.this_run,
            batching_strategy: BatchingStrategy::new(),
        }
    }
```

### 🔹 函式: `Query::par_iter_many_unique()`
- **變更前簽章 (Before)**: `fn Query::par_iter_many_unique(
        &self,
        entities: EntityList,
    )` (L1431~L1443)
- **變更後簽章 (After)**: `fn Query::par_iter_many_unique(
        &self,
        entities: EntityList,
    )` (L1431~L1443)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn par_iter_many_unique<EntityList: EntitySet<Item: Sync>>(
        &self,
        entities: EntityList,
    ) -> QueryParManyUniqueIter<'_, 's, D::ReadOnly, F, EntityList::Item> {
        QueryParManyUniqueIter {
            world: self.world,
            state: self.state.as_readonly(),
            entity_list: entities.into_iter().collect(),
            last_run: self.last_run,
            this_run: self.this_run,
            batching_strategy: BatchingStrategy::new(),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn par_iter_many_unique<EntityList: EntitySet<Item: Sync>>(
        &self,
        entities: EntityList,
    ) -> QueryParManyUniqueIter<'_, 's, D::ReadOnly, F, EntityList::Item> {
        QueryParManyUniqueIter {
            world: self.world,
            state: self.state.as_readonly(),
            entity_list: entities.into_iter().collect_set(),
            last_run: self.last_run,
            this_run: self.this_run,
            batching_strategy: BatchingStrategy::new(),
        }
    }
```


---

### 🔹 Commit #04: `c38fa547`
- **完整 Hash**: `c38fa547bf232b29a6a8c0688876e4eb1347e504`
- **說明 (Ground Truth)**: Stop sending orphaned entity IDs through ancestor-chain traversal (#25419)
- **變更檔案數**: 1

#### 📄 檔案: `crates/bevy_transform/src/systems.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:236, E:309, A:0) ➔ After(N:256, E:336, A:0)
- **差分統計**: +Nodes: 20, -Nodes: 0, +Edges: 27, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `children.iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `roots
            .iter()
            .flat_map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `CHILDREN_PER_ROOT` (MODULE_STATE)
  • + [新增節點] `world
                    .spawn (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `(0..ROOT_COUNT)
            .map(|i| {
                world
                    .spawn(Transform::from_xyz(10.0 + i as f32, 0.0, 0.0))
                    .id()
            })
            .collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world
                    .spawn(Transform::from_xyz(10.0 + i as f32, 0.0, 0.0))
                    .id (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `ROOT_COUNT` (MODULE_STATE)
  • + [新增節點] `roots
            .iter()
            .flat_map(|&root| world.get::<Children>(root).unwrap().iter())
            .collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.get::<Transform> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `spawn_children (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.get::<Children>(root).unwrap().iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `did_propagate_after_entity_index_reuse` (FUNCTION_DEF)
  • + [新增節點] `world.get::<Children> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.despawn (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `child_of.parent (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 32 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `mark_dirty_trees()`
- **變更前簽章 (Before)**: `fn mark_dirty_trees(
    changed: Query<Entity, Or<(Changed<Transform>, Changed<ChildOf>, Added<GlobalTransform>)>>,
    mut orphaned: RemovedComponents<ChildOf>,
    mut transforms: Query<&mut TransformTreeChanged>,
    parents: Query<&ChildOf>,
    static_optimizations: Res<StaticTransformOptimizations>,
    // Cached allocations for multi-threaded parallel implementation
    #[cfg(feature = "multi_threaded")] mut shared_bitset: Local<
        alloc::vec::Vec<core::sync::atomic::AtomicU64>,
    >,
    #[cfg(feature = "multi_threaded")] mut local_bitset: Local<
        bevy_utils::Parallel<alloc::vec::Vec<u64>>,
    >,
    #[cfg(feature = "multi_threaded")] mut consumer_channels: Local<
        bevy_utils::BufferedChannel<Entity>,
    >,
    #[cfg(feature = "multi_threaded")] mut traversal_channels: Local<
        bevy_utils::BufferedChannel<Entity>,
    >,
)` (L111~L306)
- **變更後簽章 (After)**: `fn mark_dirty_trees(
    changed: Query<Entity, Or<(Changed<Transform>, Changed<ChildOf>, Added<GlobalTransform>)>>,
    mut orphaned: RemovedComponents<ChildOf>,
    mut transforms: Query<&mut TransformTreeChanged>,
    parents: Query<&ChildOf>,
    static_optimizations: Res<StaticTransformOptimizations>,
    // Cached allocations for multi-threaded parallel implementation
    #[cfg(feature = "multi_threaded")] mut shared_bitset: Local<
        alloc::vec::Vec<core::sync::atomic::AtomicU64>,
    >,
    #[cfg(feature = "multi_threaded")] mut local_bitset: Local<
        bevy_utils::Parallel<alloc::vec::Vec<u64>>,
    >,
    #[cfg(feature = "multi_threaded")] mut consumer_channels: Local<
        bevy_utils::BufferedChannel<Entity>,
    >,
    #[cfg(feature = "multi_threaded")] mut traversal_channels: Local<
        bevy_utils::BufferedChannel<Entity>,
    >,
)` (L111~L305)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn mark_dirty_trees(
    changed: Query<Entity, Or<(Changed<Transform>, Changed<ChildOf>, Added<GlobalTransform>)>>,
    mut orphaned: RemovedComponents<ChildOf>,
    mut transforms: Query<&mut TransformTreeChanged>,
    parents: Query<&ChildOf>,
    static_optimizations: Res<StaticTransformOptimizations>,
    // Cached allocations for multi-threaded parallel implementation
    #[cfg(feature = "multi_threaded")] mut shared_bitset: Local<
        alloc::vec::Vec<core::sync::atomic::AtomicU64>,
    >,
    #[cfg(feature = "multi_threaded")] mut local_bitset: Local<
        bevy_utils::Parallel<alloc::vec::Vec<u64>>,
    >,
    #[cfg(feature = "multi_threaded")] mut consumer_channels: Local<
        bevy_utils::BufferedChannel<Entity>,
    >,
    #[cfg(feature = "multi_threaded")] mut traversal_channels: Local<
        bevy_utils::BufferedChannel<Entity>,
    >,
) {
    if !static_optimizations.is_enabled() {
        return;
    }

    // Simple serial implementation that iterates changed entities and traverses the tree.
    #[cfg(not(feature = "multi_threaded"))]
    for entity in changed.iter().chain(orphaned.read()) {
        let mut next = entity;
        while let Ok(mut tree) = transforms.get_mut(next) {
            if tree.is_changed() && !tree.is_added() {
                // If the component was changed, this part of the tree has already been processed.
                // Ignore this if the change was caused by the component being added.
                break;
            }
            tree.set_changed();
            if let Ok(parent) = parents.get(next).map(ChildOf::parent) {
                next = parent;
            } else {
                break;
            };
        }
    }

    // Concurrent and parallel implementation with three sets of asynchronous workers:
    //
    // - producer: (single) finds all changed or orphaned entities and sends a message in a channel
    // - traversal: (many) read incoming messages from producer, traverse hierarchy using atomics to
    //      cooperatively early exit across threads, send newly changed entities to consumer.
    // - consumer: (single) read incoming messages from traversal
    //
    // These workers are all running both parallelly and concurrently. They are spawned at the start
    // of the scope and asynchronously await incoming batches of work. This allows the entire
    // pipeline to start working as soon as there is available work to process, instead of running
    // each stage serially with inner parallelism.
    #[cfg(feature = "multi_threaded")]
    {
        use bevy_tasks::ComputeTaskPool;
        use core::sync::atomic::Ordering;
        #[cfg(feature = "trace")]
        use tracing::{info_span, Instrument};

        ComputeTaskPool::get().scope(|scope| {
            traversal_channels.chunk_size = 1024;
            consumer_channels.chunk_size = 1024;
            let (traversal_rx, mut traversal_tx) = traversal_channels.unbounded();
            let (consumer_rx, mut consumer_tx) = consumer_channels.unbounded();
            let shared_bitset: &[core::sync::atomic::AtomicU64] = &shared_bitset;
            let local_bitset = &*local_bitset;
            let parents_ref = &parents;

            // Consumer: drain the channel of moved entities and call set_changed() on the marker.
            scope.spawn({
                let fut = async move {
                    while let Ok(mut chunk) = consumer_rx.recv().await {
                        for entity in chunk.drain() {
                            if let Ok(mut tree) = transforms.get_mut(entity) {
                                tree.set_changed();
                            }
                        }
                    }
                };
                #[cfg(feature = "trace")]
                let fut = fut.instrument(info_span!("consumer_mark_dirty"));
                fut
            });

            // Traversal: each task loops until the producer channel is exhausted, walking each
            // entity's ancestor chain and forwarding newly marked entities to the consumer task.
            for _ in 0..(ComputeTaskPool::get().thread_num() - 1).max(1) {
                let traversal_rx = traversal_rx.clone();
                let mut consumer_tx = consumer_tx.clone();
                scope.spawn({
                    let fut = async move {
                        while let Ok(mut chunk) = traversal_rx.recv().await {
                            for mut entity in chunk.drain() {
                                let mut first_iteration = true;
                                'traverse_hierarchy: loop {
                                    let idx = entity.index().index() as usize;
                                    let word = idx / 64;
                                    let bit = 1u64 << (idx % 64);

                                    #[expect(
                                        clippy::redundant_else,
                                        reason = "Without the else, fails to compile due to async"
                                    )]
                                    if word < shared_bitset.len()
                                        && shared_bitset[word].fetch_or(bit, Ordering::Relaxed)
                                            & bit
                                            != 0
                                    {
                                        // Common path: atomic OR into the shared bitset.
                                        // If the entity was already visited, we can stop climbing.
                                        break 'traverse_hierarchy;
                                    } else {
                                        // Overflow: entity index exceeds shared bitset capacity.
                                        // Use a per-task local bitset for intra-task early exit.
                                        let overflow = &mut *local_bitset.borrow_local_mut();
                                        if word < overflow.len() && overflow[word] & bit != 0 {
                                            break 'traverse_hierarchy;
                                        }
                                        if word >= overflow.len() {
                                            overflow.resize(word + 1, 0u64);
                                        }
                                        overflow[word] |= bit;
                                    }

                                    // If we have not hit a break yet, it's the first time we've
                                    // seen this entity, so it should be sent to the consumer.
                                    if first_iteration {
                                        first_iteration = false;
                                    } else {
                                        // The first iteration (leaf) has already been sent to the
                                        // consumer by the producer; we don't need to send it again.
                                        consumer_tx.send(entity).await.ok();
                                    }

                                    match parents_ref.get(entity).ok().map(ChildOf::parent) {
                                        Some(parent) => entity = parent,
                                        None => break 'traverse_hierarchy,
                                    }
                                }
                            }
                        }
                    };
                    #[cfg(feature = "trace")]
                    let fut = fut.instrument(info_span!("par_traversal_mark_dirty"));
                    fut
                });
            }

            // Producer: Feed changed entities and orphans into producer tasks. The senders are
            // dropped at the end of this closure, closing the channel and allowing the other tasks
            // to exit.
            //
            // Note that we send the entity directly to the consumer as well, we do this to start
            // feeding it work as soon as possible. The traversal worker should skip sending these
            // leaves to the consumer because it has already been sent here.
            let mut producer = move || {
                for entity in orphaned.read() {
                    let _ = traversal_tx.send_blocking(entity);
                    let _ = consumer_tx.send_blocking(entity);
                }
                // Changed<> table scans are slow, so we parallelize them to improve performance.
                changed.par_iter().for_each_init(
                    || (traversal_tx.clone(), consumer_tx.clone()),
                    |(traversal_tx, consumer_tx), entity| {
                        let _ = traversal_tx.send_blocking(entity);
                        let _ = consumer_tx.send_blocking(entity);
                    },
                );
            };
            #[cfg(feature = "trace")]
            info_span!("producer_mark_dirty").in_scope(&mut producer);
            #[cfg(not(feature = "trace"))]
            producer();
        });

        // Merge thread-local bitsets into the shared bitset, growing it to accommodate the largest
        // entity index we have encountered so far. At steady-state, these local bitsets stay empty.
        for local_bitset in local_bitset.iter_mut() {
            if local_bitset.is_empty() {
                continue;
            }
            if local_bitset.len() > shared_bitset.len() {
                shared_bitset.resize_with(local_bitset.len(), Default::default);
            }
            local_bitset.clear();
        }

        // Reset the bitset for the next frame while preserving the `Vec` length. Using `clear()`
        // would shrink the length to 0 and force every entity through the overflow path next frame.
        for w in shared_bitset.iter() {
            w.store(0, Ordering::Relaxed);
        }
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn mark_dirty_trees(
    changed: Query<Entity, Or<(Changed<Transform>, Changed<ChildOf>, Added<GlobalTransform>)>>,
    mut orphaned: RemovedComponents<ChildOf>,
    mut transforms: Query<&mut TransformTreeChanged>,
    parents: Query<&ChildOf>,
    static_optimizations: Res<StaticTransformOptimizations>,
    // Cached allocations for multi-threaded parallel implementation
    #[cfg(feature = "multi_threaded")] mut shared_bitset: Local<
        alloc::vec::Vec<core::sync::atomic::AtomicU64>,
    >,
    #[cfg(feature = "multi_threaded")] mut local_bitset: Local<
        bevy_utils::Parallel<alloc::vec::Vec<u64>>,
    >,
    #[cfg(feature = "multi_threaded")] mut consumer_channels: Local<
        bevy_utils::BufferedChannel<Entity>,
    >,
    #[cfg(feature = "multi_threaded")] mut traversal_channels: Local<
        bevy_utils::BufferedChannel<Entity>,
    >,
) {
    if !static_optimizations.is_enabled() {
        return;
    }

    // Simple serial implementation that iterates changed entities and traverses the tree.
    #[cfg(not(feature = "multi_threaded"))]
    for entity in changed.iter().chain(orphaned.read()) {
        let mut next = entity;
        while let Ok(mut tree) = transforms.get_mut(next) {
            if tree.is_changed() && !tree.is_added() {
                // If the component was changed, this part of the tree has already been processed.
                // Ignore this if the change was caused by the component being added.
                break;
            }
            tree.set_changed();
            if let Ok(parent) = parents.get(next).map(ChildOf::parent) {
                next = parent;
            } else {
                break;
            };
        }
    }

    // Concurrent and parallel implementation with three sets of asynchronous workers:
    //
    // - producer: (single) finds all changed or orphaned entities and sends a message in a channel
    // - traversal: (many) read incoming messages from producer, traverse hierarchy using atomics to
    //      cooperatively early exit across threads, send newly changed entities to consumer.
    // - consumer: (single) read incoming messages from traversal
    //
    // These workers are all running both parallelly and concurrently. They are spawned at the start
    // of the scope and asynchronously await incoming batches of work. This allows the entire
    // pipeline to start working as soon as there is available work to process, instead of running
    // each stage serially with inner parallelism.
    #[cfg(feature = "multi_threaded")]
    {
        use bevy_tasks::ComputeTaskPool;
        use core::sync::atomic::Ordering;
        #[cfg(feature = "trace")]
        use tracing::{info_span, Instrument};

        ComputeTaskPool::get().scope(|scope| {
            traversal_channels.chunk_size = 1024;
            consumer_channels.chunk_size = 1024;
            let (traversal_rx, traversal_tx) = traversal_channels.unbounded();
            let (consumer_rx, mut consumer_tx) = consumer_channels.unbounded();
            let shared_bitset: &[core::sync::atomic::AtomicU64] = &shared_bitset;
            let local_bitset = &*local_bitset;
            let parents_ref = &parents;

            // Consumer: drain the channel of moved entities and call set_changed() on the marker.
            scope.spawn({
                let fut = async move {
                    while let Ok(mut chunk) = consumer_rx.recv().await {
                        for entity in chunk.drain() {
                            if let Ok(mut tree) = transforms.get_mut(entity) {
                                tree.set_changed();
                            }
                        }
                    }
                };
                #[cfg(feature = "trace")]
                let fut = fut.instrument(info_span!("consumer_mark_dirty"));
                fut
            });

            // Traversal: each task loops until the producer channel is exhausted, walking each
            // entity's ancestor chain and forwarding newly marked entities to the consumer task.
            for _ in 0..(ComputeTaskPool::get().thread_num() - 1).max(1) {
                let traversal_rx = traversal_rx.clone();
                let mut consumer_tx = consumer_tx.clone();
                scope.spawn({
                    let fut = async move {
                        while let Ok(mut chunk) = traversal_rx.recv().await {
                            for mut entity in chunk.drain() {
                                let mut first_iteration = true;
                                'traverse_hierarchy: loop {
                                    let idx = entity.index().index() as usize;
                                    let word = idx / 64;
                                    let bit = 1u64 << (idx % 64);

                                    #[expect(
                                        clippy::redundant_else,
                                        reason = "Without the else, fails to compile due to async"
                                    )]
                                    if word < shared_bitset.len()
                                        && shared_bitset[word].fetch_or(bit, Ordering::Relaxed)
                                            & bit
                                            != 0
                                    {
                                        // Common path: atomic OR into the shared bitset.
                                        // If the entity was already visited, we can stop climbing.
                                        break 'traverse_hierarchy;
                                    } else {
                                        // Overflow: entity index exceeds shared bitset capacity.
                                        // Use a per-task local bitset for intra-task early exit.
                                        let overflow = &mut *local_bitset.borrow_local_mut();
                                        if word < overflow.len() && overflow[word] & bit != 0 {
                                            break 'traverse_hierarchy;
                                        }
                                        if word >= overflow.len() {
                                            overflow.resize(word + 1, 0u64);
                                        }
                                        overflow[word] |= bit;
                                    }

                                    // If we have not hit a break yet, it's the first time we've
                                    // seen this entity, so it should be sent to the consumer.
                                    if first_iteration {
                                        first_iteration = false;
                                    } else {
                                        // The first iteration (leaf) has already been sent to the
                                        // consumer by the producer; we don't need to send it again.
                                        consumer_tx.send(entity).await.ok();
                                    }

                                    match parents_ref.get(entity).ok().map(ChildOf::parent) {
                                        Some(parent) => entity = parent,
                                        None => break 'traverse_hierarchy,
                                    }
                                }
                            }
                        }
                    };
                    #[cfg(feature = "trace")]
                    let fut = fut.instrument(info_span!("par_traversal_mark_dirty"));
                    fut
                });
            }

            // Producer: Feed changed entities and orphans into producer tasks. The senders are
            // dropped at the end of this closure, closing the channel and allowing the other tasks
            // to exit.
            //
            // Note that we send changed entities directly to the consumer as well; we do this to
            // start feeding it work as soon as possible. The traversal worker should skip sending
            // these leaves to the consumer because they have already been sent here.
            let mut producer = move || {
                for entity in orphaned.read() {
                    let _ = consumer_tx.send_blocking(entity);
                }
                // Changed<> table scans are slow, so we parallelize them to improve performance.
                changed.par_iter().for_each_init(
                    || (traversal_tx.clone(), consumer_tx.clone()),
                    |(traversal_tx, consumer_tx), entity| {
                        let _ = traversal_tx.send_blocking(entity);
                        let _ = consumer_tx.send_blocking(entity);
                    },
                );
            };
            #[cfg(feature = "trace")]
            info_span!("producer_mark_dirty").in_scope(&mut producer);
            #[cfg(not(feature = "trace"))]
            producer();
        });

        // Merge thread-local bitsets into the shared bitset, growing it to accommodate the largest
        // entity index we have encountered so far. At steady-state, these local bitsets stay empty.
        for local_bitset in local_bitset.iter_mut() {
            if local_bitset.is_empty() {
                continue;
            }
            if local_bitset.len() > shared_bitset.len() {
                shared_bitset.resize_with(local_bitset.len(), Default::default);
            }
            local_bitset.clear();
        }

        // Reset the bitset for the next frame while preserving the `Vec` length. Using `clear()`
        // would shrink the length to 0 and force every entity through the overflow path next frame.
        for w in shared_bitset.iter() {
            w.store(0, Ordering::Relaxed);
        }
    }
}
```


---

### 🔹 Commit #05: `0de7fb77`
- **完整 Hash**: `0de7fb777a27465463cb3f94b558fda8613d8248`
- **說明 (Ground Truth)**: Fix incorrect debug asserts in contiguous par_iter (#26173)
- **變更檔案數**: 2

#### 📄 檔案: `crates/bevy_ecs/src/query/fetch.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:569, E:511, A:0) ➔ After(N:569, E:511, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 2, -Edges: 2, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `debug_assert! (Macro)` (FUNCTION_DEF)
  • - [移除節點] `debug_assert_eq! (Macro)` (FUNCTION_DEF)
  • + [新增呼叫邊] `T::fetch_contiguous` ──[CALLS]──> `debug_assert! (Macro)`
  • + [新增呼叫邊] `Ref::fetch_contiguous` ──[CALLS]──> `debug_assert! (Macro)`
  • - [移除呼叫邊] `T::fetch_contiguous` ──[CALLS]──> `debug_assert_eq! (Macro)`
  • - [移除呼叫邊] `Ref::fetch_contiguous` ──[CALLS]──> `debug_assert_eq! (Macro)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `T::fetch_contiguous()`
- **變更前簽章 (Before)**: `fn T::fetch_contiguous(
        _state: &'s Self::State,
        fetch: &mut Self::Fetch<'w>,
        entities: &'w [Entity],
        range: Range<u32>,
    )` (L2023~L2054)
- **變更後簽章 (After)**: `fn T::fetch_contiguous(
        _state: &'s Self::State,
        fetch: &mut Self::Fetch<'w>,
        entities: &'w [Entity],
        range: Range<u32>,
    )` (L2023~L2056)

#### ◀️ 變更前實作碼 (Before Implementation):
```
unsafe fn fetch_contiguous<'w, 's>(
        _state: &'s Self::State,
        fetch: &mut Self::Fetch<'w>,
        entities: &'w [Entity],
        range: Range<u32>,
    ) -> Self::Contiguous<'w, 's> {
        fetch.components.extract(
            |table| {
                // SAFETY: The caller ensures `set_table` was previously called
                let table = unsafe { table.debug_checked_unwrap() };
                // SAFETY:
                // - `table` is `entities.len()` long
                // - `UnsafeCell<T>` has the same layout as `T`
                // - `range` refers to a valid range of the table
                // - `range.start` is less than or equal to `range.end`
                let slice = unsafe {
                    table
                        .cast()
                        .slice_unchecked((range.start as usize)..(range.end as usize))
                };
                debug_assert_eq!(slice.len(), entities.len());
                slice
            },
            |_| {
                #[cfg(debug_assertions)]
                unreachable!();
                // SAFETY: The caller ensures query is dense
                #[cfg(not(debug_assertions))]
                core::hint::unreachable_unchecked();
            },
        )
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
unsafe fn fetch_contiguous<'w, 's>(
        _state: &'s Self::State,
        fetch: &mut Self::Fetch<'w>,
        entities: &'w [Entity],
        range: Range<u32>,
    ) -> Self::Contiguous<'w, 's> {
        // `entities` covers the whole table; `range` may cover only part of it.
        debug_assert!(range.start < range.end);
        debug_assert!(range.end as usize <= entities.len());

        fetch.components.extract(
            |table| {
                // SAFETY: The caller ensures `set_table` was previously called
                let table = unsafe { table.debug_checked_unwrap() };
                // SAFETY:
                // - `table` is `entities.len()` long
                // - `UnsafeCell<T>` has the same layout as `T`
                // - `range` refers to a valid range of the table
                // - `range.start` is less than or equal to `range.end`
                unsafe {
                    table
                        .cast()
                        .slice_unchecked((range.start as usize)..(range.end as usize))
                }
            },
            |_| {
                #[cfg(debug_assertions)]
                unreachable!();
                // SAFETY: The caller ensures query is dense
                #[cfg(not(debug_assertions))]
                core::hint::unreachable_unchecked();
            },
        )
    }
```

### 🔹 函式: `Ref::fetch_contiguous()`
- **變更前簽章 (Before)**: `fn Ref::fetch_contiguous(
        _state: &'s Self::State,
        fetch: &mut Self::Fetch<'w>,
        entities: &'w [Entity],
        range: Range<u32>,
    )` (L2311~L2357)
- **變更後簽章 (After)**: `fn Ref::fetch_contiguous(
        _state: &'s Self::State,
        fetch: &mut Self::Fetch<'w>,
        entities: &'w [Entity],
        range: Range<u32>,
    )` (L2313~L2359)

#### ◀️ 變更前實作碼 (Before Implementation):
```
unsafe fn fetch_contiguous<'w, 's>(
        _state: &'s Self::State,
        fetch: &mut Self::Fetch<'w>,
        entities: &'w [Entity],
        range: Range<u32>,
    ) -> Self::Contiguous<'w, 's> {
        fetch.components.extract(
            |table| {
                // SAFETY: set_table was previously called
                let (table_components, added_ticks, changed_ticks, summary_tick, callers) =
                    unsafe { table.debug_checked_unwrap() };

                let range = (range.start as usize)..(range.end as usize);

                let contiguous_ref = ContiguousRef {
                    // SAFETY: `entities` has the same length as the rows in the set table.
                    value: unsafe { table_components.cast().slice_unchecked(range.clone()) },
                    // SAFETY:
                    // - The caller ensures the permission to access ticks.
                    // - `entities` has the same length as the rows in the set table hence the
                    // ticks.
                    ticks: unsafe {
                        ContiguousComponentTicksRef::from_slice_ptrs(
                            added_ticks,
                            changed_ticks,
                            summary_tick,
                            callers,
                            range,
                            fetch.this_run,
                            fetch.last_run,
                        )
                    },
                };

                debug_assert_eq!(entities.len(), contiguous_ref.value.len());

                contiguous_ref
            },
            |_| {
                #[cfg(debug_assertions)]
                unreachable!();
                // SAFETY: the caller ensures that [`Self::set_table`] was called beforehand.
                #[cfg(not(debug_assertions))]
                core::hint::unreachable_unchecked();
            },
        )
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
unsafe fn fetch_contiguous<'w, 's>(
        _state: &'s Self::State,
        fetch: &mut Self::Fetch<'w>,
        entities: &'w [Entity],
        range: Range<u32>,
    ) -> Self::Contiguous<'w, 's> {
        // `entities` covers the whole table; `range` may cover only part of it.
        debug_assert!(range.start < range.end);
        debug_assert!(range.end as usize <= entities.len());

        fetch.components.extract(
            |table| {
                // SAFETY: set_table was previously called
                let (table_components, added_ticks, changed_ticks, summary_tick, callers) =
                    unsafe { table.debug_checked_unwrap() };

                let range = (range.start as usize)..(range.end as usize);

                ContiguousRef {
                    // SAFETY: `entities` has the same length as the rows in the set table.
                    value: unsafe { table_components.cast().slice_unchecked(range.clone()) },
                    // SAFETY:
                    // - The caller ensures the permission to access ticks.
                    // - `entities` has the same length as the rows in the set table hence the
                    // ticks.
                    ticks: unsafe {
                        ContiguousComponentTicksRef::from_slice_ptrs(
                            added_ticks,
                            changed_ticks,
                            summary_tick,
                            callers,
                            range,
                            fetch.this_run,
                            fetch.last_run,
                        )
                    },
                }
            },
            |_| {
                #[cfg(debug_assertions)]
                unreachable!();
                // SAFETY: the caller ensures that [`Self::set_table`] was called beforehand.
                #[cfg(not(debug_assertions))]
                core::hint::unreachable_unchecked();
            },
        )
    }
```


#### 📄 檔案: `crates/bevy_ecs/src/query/state.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:381, E:590, A:0) ➔ After(N:381, E:590, A:0)
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

### 🔹 函式: `QueryState::contiguous_par_fold_init_unchecked_manual()`
- **變更前簽章 (Before)**: `fn QueryState::contiguous_par_fold_init_unchecked_manual(
        &'s self,
        init_accum: impl Fn() -> T + Send + Sync + Clone,
        world: UnsafeWorldCell<'w>,
        batch_size: u32,
        func: impl Fn(T, D::Contiguous<'w, 's>) -> T + Send + Sync + Clone,
        last_run: Tick,
        this_run: Tick,
    )` (L1828~L1928)
- **變更後簽章 (After)**: `fn QueryState::contiguous_par_fold_init_unchecked_manual(
        &'s self,
        init_accum: impl Fn() -> T + Send + Sync + Clone,
        world: UnsafeWorldCell<'w>,
        batch_size: u32,
        func: impl Fn(T, D::Contiguous<'w, 's>) -> T + Send + Sync + Clone,
        last_run: Tick,
        this_run: Tick,
    )` (L1828~L1931)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) unsafe fn contiguous_par_fold_init_unchecked_manual<'w, 's, T>(
        &'s self,
        init_accum: impl Fn() -> T + Send + Sync + Clone,
        world: UnsafeWorldCell<'w>,
        batch_size: u32,
        func: impl Fn(T, D::Contiguous<'w, 's>) -> T + Send + Sync + Clone,
        last_run: Tick,
        this_run: Tick,
    ) where
        D: ContiguousQueryData,
        F: ArchetypeFilter,
    {
        debug_assert!(self.is_dense);

        // The maximum number of tables we can accumulate before we must flush
        // them into a batch.
        const MAX_TABLES_PER_BATCH: usize = 32;

        bevy_tasks::ComputeTaskPool::get().scope(|scope| {
            use core::ops::Range;

            use smallvec::SmallVec;

            // SAFETY: We only access table data that has been registered in
            // `self.component_access`.
            let tables = unsafe { &world.storages().tables };

            // Unlike ordinary parallel iteration, contiguous iteration uses a
            // unified queuing system that accumulates row *ranges* from
            // multiple tables, not tables as a whole. This allows individual
            // jobs to include any combination of entire tables and portions of
            // tables.
            let mut batch_queue: SmallVec<[(TableId, Range<u32>); 4]> = SmallVec::new();
            let mut queue_entity_count = 0;

            // Submits a full batch.
            let submit_batch_queue = |queue: SmallVec<[(TableId, Range<u32>); 4]>| {
                let (func, init_accum) = (func.clone(), init_accum.clone());
                scope.spawn(async move {
                    #[cfg(feature = "trace")]
                    let _span = self.par_iter_span.enter();
                    // SAFETY: Contiguous iteration can only process tables, so
                    // we must have a table here.
                    let tables = unsafe { &world.storages().tables };
                    let mut fetch = D::init_fetch(world, &self.fetch_state, last_run, this_run);
                    let mut accum = init_accum();
                    for (table_id, range) in queue {
                        let table = &tables[table_id];
                        D::set_table(&mut fetch, &self.fetch_state, table);
                        let item = D::fetch_contiguous(
                            &self.fetch_state,
                            &mut fetch,
                            table.entities(),
                            range,
                        );
                        accum = func(accum, item);
                    }
                });
            };

            // Go over all the tables.
            for storage_id in &self.matched_storage_ids {
                let table_id = storage_id.table_id;
                let row_count = tables[table_id].entity_count();

                // Accumulate rows until we either hit the `batch_size` or hit
                // the maximum number of tables.
                let mut row_start_offset = 0;
                while row_start_offset < row_count {
                    // If we hit the maximum number of tables, force a submit.
                    if batch_queue.len() == MAX_TABLES_PER_BATCH {
                        submit_batch_queue(core::mem::take(&mut batch_queue));
                        queue_entity_count = 0;
                    }

                    // Can we include the entire remainder of the table, or do
                    // we need to split it?
                    if queue_entity_count + row_count - row_start_offset > batch_size {
                        // We need to split the table. Push the portion that fits.
                        let row_end_offset = row_start_offset + (batch_size - queue_entity_count);
                        batch_queue.push((table_id, row_start_offset..row_end_offset));
                        row_start_offset = row_end_offset;

                        // And submit it.
                        submit_batch_queue(core::mem::take(&mut batch_queue));
                        queue_entity_count = 0;
                    } else {
                        // We can fit the entire remainder of the table.
                        batch_queue.push((table_id, row_start_offset..row_count));
                        queue_entity_count += row_count - row_start_offset;
                        break;
                    }
                }
            }

            // If we have any rows left over, submit them now.
            if !batch_queue.is_empty() {
                submit_batch_queue(batch_queue);
            }
        });
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) unsafe fn contiguous_par_fold_init_unchecked_manual<'w, 's, T>(
        &'s self,
        init_accum: impl Fn() -> T + Send + Sync + Clone,
        world: UnsafeWorldCell<'w>,
        batch_size: u32,
        func: impl Fn(T, D::Contiguous<'w, 's>) -> T + Send + Sync + Clone,
        last_run: Tick,
        this_run: Tick,
    ) where
        D: ContiguousQueryData,
        F: ArchetypeFilter,
    {
        debug_assert!(self.is_dense);
        // The caller ensures a batch size of at least 1.
        debug_assert!(batch_size > 0);

        // The maximum number of tables we can accumulate before we must flush
        // them into a batch.
        const MAX_TABLES_PER_BATCH: usize = 32;

        bevy_tasks::ComputeTaskPool::get().scope(|scope| {
            use core::ops::Range;

            use smallvec::SmallVec;

            // SAFETY: We only access table data that has been registered in
            // `self.component_access`.
            let tables = unsafe { &world.storages().tables };

            // Unlike ordinary parallel iteration, contiguous iteration uses a
            // unified queuing system that accumulates row *ranges* from
            // multiple tables, not tables as a whole. This allows individual
            // jobs to include any combination of entire tables and portions of
            // tables.
            let mut batch_queue: SmallVec<[(TableId, Range<u32>); 4]> = SmallVec::new();
            let mut queue_entity_count = 0;

            // Submits a full batch.
            let submit_batch_queue = |queue: SmallVec<[(TableId, Range<u32>); 4]>| {
                let (func, init_accum) = (func.clone(), init_accum.clone());
                scope.spawn(async move {
                    #[cfg(feature = "trace")]
                    let _span = self.par_iter_span.enter();
                    // SAFETY: Contiguous iteration can only process tables, so
                    // we must have a table here.
                    let tables = unsafe { &world.storages().tables };
                    let mut fetch = D::init_fetch(world, &self.fetch_state, last_run, this_run);
                    let mut accum = init_accum();
                    for (table_id, range) in queue {
                        let table = &tables[table_id];
                        D::set_table(&mut fetch, &self.fetch_state, table);
                        let item = D::fetch_contiguous(
                            &self.fetch_state,
                            &mut fetch,
                            table.entities(),
                            range,
                        );
                        accum = func(accum, item);
                    }
                });
            };

            // Go over all the tables.
            for storage_id in &self.matched_storage_ids {
                let table_id = storage_id.table_id;
                let row_count = tables[table_id].entity_count();

                // Accumulate rows until we either hit the `batch_size` or hit
                // the maximum number of tables.
                let mut row_start_offset = 0;
                while row_start_offset < row_count {
                    // If we hit the maximum number of tables, force a submit.
                    if batch_queue.len() == MAX_TABLES_PER_BATCH {
                        submit_batch_queue(core::mem::take(&mut batch_queue));
                        queue_entity_count = 0;
                    }

                    // Can the remaining rows fill the batch?
                    // Submit exact fits too, so the next table cannot add an empty range
                    // to a full batch.
                    if queue_entity_count + row_count - row_start_offset >= batch_size {
                        // Push enough rows to fill the batch.
                        let row_end_offset = row_start_offset + (batch_size - queue_entity_count);
                        batch_queue.push((table_id, row_start_offset..row_end_offset));
                        row_start_offset = row_end_offset;

                        // And submit it.
                        submit_batch_queue(core::mem::take(&mut batch_queue));
                        queue_entity_count = 0;
                    } else {
                        // We can fit the entire remainder of the table.
                        batch_queue.push((table_id, row_start_offset..row_count));
                        queue_entity_count += row_count - row_start_offset;
                        break;
                    }
                }
            }

            // If we have any rows left over, submit them now.
            if !batch_queue.is_empty() {
                submit_batch_queue(batch_queue);
            }
        });
    }
```


---

### 🔹 Commit #06: `81a3f2f6`
- **完整 Hash**: `81a3f2f6d396a29e7edac86891df10448b48f1d0`
- **說明 (Ground Truth)**: fix(bevy_color): resolve clippy::needless_update in hsla/hsl (#26106)
- **變更檔案數**: 1

#### 📄 檔案: `crates/bevy_color/src/color.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:118, E:225, A:0) ➔ After(N:119, E:227, A:0)
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
  • + [新增節點] `Hsla::new (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Color::hsla` ──[CALLS]──> `Hsla::new (External/Unresolved)`
  • + [新增呼叫邊] `Color::hsl` ──[CALLS]──> `Hsla::new (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Color::hsl()`
- **變更前簽章 (Before)**: `fn Color::hsl(hue: f32, saturation: f32, lightness: f32)` (L274~L281)
- **變更後簽章 (After)**: `fn Color::hsl(hue: f32, saturation: f32, lightness: f32)` (L269~L271)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub const fn hsl(hue: f32, saturation: f32, lightness: f32) -> Self {
        Self::Hsla(Hsla {
            hue,
            saturation,
            lightness,
            alpha: 1.0,
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub const fn hsl(hue: f32, saturation: f32, lightness: f32) -> Self {
        Self::Hsla(Hsla::new(hue, saturation, lightness, 1.0))
    }
```

### 🔹 函式: `Color::hsla()`
- **變更前簽章 (Before)**: `fn Color::hsla(hue: f32, saturation: f32, lightness: f32, alpha: f32)` (L258~L265)
- **變更後簽章 (After)**: `fn Color::hsla(hue: f32, saturation: f32, lightness: f32, alpha: f32)` (L258~L260)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub const fn hsla(hue: f32, saturation: f32, lightness: f32, alpha: f32) -> Self {
        Self::Hsla(Hsla {
            hue,
            saturation,
            lightness,
            alpha,
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub const fn hsla(hue: f32, saturation: f32, lightness: f32, alpha: f32) -> Self {
        Self::Hsla(Hsla::new(hue, saturation, lightness, alpha))
    }
```


---

### 🔹 Commit #07: `0b51329a`
- **完整 Hash**: `0b51329a2fbeb152d0e04d0564033e5cf669451d`
- **說明 (Ground Truth)**: Include type paths in component inspection results (#26172)
- **變更檔案數**: 3

#### 📄 檔案: `crates/bevy_dev_tools/src/inspection/component_inspection.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:99, E:142, A:0) ➔ After(N:120, E:198, A:0)
- **差分統計**: +Nodes: 21, -Nodes: 0, +Edges: 56, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `ComponentTypeMetadata::new(&world, id).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `type_path_is_reported_for_reflected_components` (FUNCTION_DEF)
  • + [新增節點] `registration.type_info().type_path (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Health::type_path (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Plain (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.components().valid_component_id::<Plain> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `type_path_is_absent_for_unreflected_components` (FUNCTION_DEF)
  • + [新增節點] `Some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world
                .inspect_component_by_id (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world
                .inspect_component_by_id(
                    id,
                    entity,
                    &metadata,
                    ComponentInspectionSettings::default(),
                )
                .unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `serde_json::to_value (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.components().valid_component_id::<Plain>().unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.spawn(Plain(1)).id (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `type_registration
            .as_ref()
            .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `type_registration
            .as_ref (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 62 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `ComponentTypeMetadata::new()`
- **變更前簽章 (Before)**: `fn ComponentTypeMetadata::new(world: &World, component_id: ComponentId)` (L134~L165)
- **變更後簽章 (After)**: `fn ComponentTypeMetadata::new(world: &World, component_id: ComponentId)` (L147~L183)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn new(world: &World, component_id: ComponentId) -> Result<Self, ComponentInspectionError> {
        let component_info = world.components().get_info(component_id).ok_or(
            ComponentInspectionError::ComponentIdNotRegistered(component_id),
        )?;

        let type_id = component_info.type_id();

        let type_registration = type_id.and_then(|type_id| {
            world
                .get_resource::<AppTypeRegistry>()
                .and_then(|type_registry| type_registry.read().get(type_id).cloned())
        });

        let label_definition_priority = type_id.and_then(|type_id| {
            world
                .get_resource::<LabelResolutionRegistry>()
                .and_then(|registry| registry.get_priority_by_type_id(type_id))
        });

        Ok(Self {
            component_id,
            name: component_info.name(),
            type_id,
            memory_size: MemorySize::new(component_info.layout().size()),
            label_definition_priority,
            mutable: component_info.mutable(),
            storage_type: component_info.storage_type(),
            is_send_and_sync: component_info.is_send_and_sync(),
            required_components: component_info.required_components().iter_ids().collect(),
            type_registration,
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn new(world: &World, component_id: ComponentId) -> Result<Self, ComponentInspectionError> {
        let component_info = world.components().get_info(component_id).ok_or(
            ComponentInspectionError::ComponentIdNotRegistered(component_id),
        )?;

        let type_id = component_info.type_id();

        let type_registration = type_id.and_then(|type_id| {
            world
                .get_resource::<AppTypeRegistry>()
                .and_then(|type_registry| type_registry.read().get(type_id).cloned())
        });

        let label_definition_priority = type_id.and_then(|type_id| {
            world
                .get_resource::<LabelResolutionRegistry>()
                .and_then(|registry| registry.get_priority_by_type_id(type_id))
        });

        let type_path = type_registration
            .as_ref()
            .map(|registration| registration.type_info().type_path().to_string());

        Ok(Self {
            component_id,
            name: component_info.name(),
            type_id,
            type_path,
            memory_size: MemorySize::new(component_info.layout().size()),
            label_definition_priority,
            mutable: component_info.mutable(),
            storage_type: component_info.storage_type(),
            is_send_and_sync: component_info.is_send_and_sync(),
            required_components: component_info.required_components().iter_ids().collect(),
            type_registration,
        })
    }
```

### 🔹 函式: `ComponentInspection::clone()`
- **變更前簽章 (Before)**: `fn ComponentInspection::clone(&self)` (L56~L72)
- **變更後簽章 (After)**: `fn ComponentInspection::clone(&self)` (L62~L79)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn clone(&self) -> Self {
        let reflected_value = self
            .reflected_value
            .as_deref()
            .and_then(|reflected| clone_incomplete(reflected).ok());

        Self {
            entity: self.entity,
            component_id: self.component_id,
            name: self.name.clone(),
            memory_size: self.memory_size,
            value: self.value.clone(),
            reflected_value,
            #[cfg(feature = "serialize")]
            serialized_value: self.serialized_value.clone(),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn clone(&self) -> Self {
        let reflected_value = self
            .reflected_value
            .as_deref()
            .and_then(|reflected| clone_incomplete(reflected).ok());

        Self {
            entity: self.entity,
            component_id: self.component_id,
            name: self.name.clone(),
            type_path: self.type_path.clone(),
            memory_size: self.memory_size,
            value: self.value.clone(),
            reflected_value,
            #[cfg(feature = "serialize")]
            serialized_value: self.serialized_value.clone(),
        }
    }
```


#### 📄 檔案: `crates/bevy_dev_tools/src/inspection/extension_methods.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:124, E:156, A:0) ➔ After(N:125, E:157, A:0)
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
  • + [新增節點] `metadata.type_path.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `World::inspect_component_by_id` ──[CALLS]──> `metadata.type_path.clone (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `World::inspect_component_by_id()`
- **變更前簽章 (Before)**: `fn World::inspect_component_by_id(
        &self,
        component_id: ComponentId,
        entity: Entity,
        metadata: &ComponentTypeMetadata,
        settings: ComponentInspectionSettings,
    )` (L164~L225)
- **變更後簽章 (After)**: `fn World::inspect_component_by_id(
        &self,
        component_id: ComponentId,
        entity: Entity,
        metadata: &ComponentTypeMetadata,
        settings: ComponentInspectionSettings,
    )` (L164~L226)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn inspect_component_by_id(
        &self,
        component_id: ComponentId,
        entity: Entity,
        metadata: &ComponentTypeMetadata,
        settings: ComponentInspectionSettings,
    ) -> Result<ComponentInspection, ComponentInspectionError> {
        let component_info = self.components().get_info(component_id).ok_or(
            ComponentInspectionError::ComponentIdNotRegistered(component_id),
        )?;
        let memory_size = MemorySize::new(component_info.layout().size());
        let name = component_info.name();

        let entity_ref = self
            .get_entity(entity)
            .map_err(|_| ComponentInspectionError::ComponentNotFound(component_id))?;

        if !entity_ref.contains_id(component_id) {
            return Err(ComponentInspectionError::ComponentNotFound(component_id));
        }

        let value = if settings.detail_level == ComponentDetailLevel::Names {
            None
        } else {
            Some(component_value_to_string(
                self,
                entity,
                metadata.type_id,
                settings.full_type_names,
            ))
        };

        let reflected_value = if settings.store_reflected_value {
            metadata
                .type_id
                .and_then(|type_id| self.get_reflect(entity, type_id).ok())
                .and_then(|reflected| clone_incomplete(reflected.as_partial_reflect()).ok())
        } else {
            None
        };

        #[cfg(feature = "serialize")]
        let serialized_value = if settings.include_serialized_value {
            metadata
                .type_id
                .and_then(|type_id| self.get_reflect(entity, type_id).ok())
                .and_then(|reflected| reflect_to_json_value(self, reflected.as_partial_reflect()))
        } else {
            None
        };

        Ok(ComponentInspection {
            entity,
            component_id,
            name,
            memory_size,
            value,
            reflected_value,
            #[cfg(feature = "serialize")]
            serialized_value,
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn inspect_component_by_id(
        &self,
        component_id: ComponentId,
        entity: Entity,
        metadata: &ComponentTypeMetadata,
        settings: ComponentInspectionSettings,
    ) -> Result<ComponentInspection, ComponentInspectionError> {
        let component_info = self.components().get_info(component_id).ok_or(
            ComponentInspectionError::ComponentIdNotRegistered(component_id),
        )?;
        let memory_size = MemorySize::new(component_info.layout().size());
        let name = component_info.name();

        let entity_ref = self
            .get_entity(entity)
            .map_err(|_| ComponentInspectionError::ComponentNotFound(component_id))?;

        if !entity_ref.contains_id(component_id) {
            return Err(ComponentInspectionError::ComponentNotFound(component_id));
        }

        let value = if settings.detail_level == ComponentDetailLevel::Names {
            None
        } else {
            Some(component_value_to_string(
                self,
                entity,
                metadata.type_id,
                settings.full_type_names,
            ))
        };

        let reflected_value = if settings.store_reflected_value {
            metadata
                .type_id
                .and_then(|type_id| self.get_reflect(entity, type_id).ok())
                .and_then(|reflected| clone_incomplete(reflected.as_partial_reflect()).ok())
        } else {
            None
        };

        #[cfg(feature = "serialize")]
        let serialized_value = if settings.include_serialized_value {
            metadata
                .type_id
                .and_then(|type_id| self.get_reflect(entity, type_id).ok())
                .and_then(|reflected| reflect_to_json_value(self, reflected.as_partial_reflect()))
        } else {
            None
        };

        Ok(ComponentInspection {
            entity,
            component_id,
            name,
            type_path: metadata.type_path.clone(),
            memory_size,
            value,
            reflected_value,
            #[cfg(feature = "serialize")]
            serialized_value,
        })
    }
```


#### 📄 檔案: `crates/bevy_remote/src/inspection_methods.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:96, E:170, A:0) ➔ After(N:96, E:170, A:0)
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

### 🔹 函式: `inspect_component_by_type_path()`
- **變更前簽章 (Before)**: `fn inspect_component_by_type_path()` (L361~L374)
- **變更後簽章 (After)**: `fn inspect_component_by_type_path()` (L362~L376)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn inspect_component_by_type_path() {
        let mut world = test_world();
        let entity = world.spawn(Health(7)).id();

        let result = process_remote_inspect_component_request(
            In(Some(
                json!({ "entity": entity, "component": health_type_path() }),
            )),
            &world,
        )
        .expect("the component should be inspectable");

        assert_eq!(result["serialized_value"], json!(7));
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn inspect_component_by_type_path() {
        let mut world = test_world();
        let entity = world.spawn(Health(7)).id();

        let result = process_remote_inspect_component_request(
            In(Some(
                json!({ "entity": entity, "component": health_type_path() }),
            )),
            &world,
        )
        .expect("the component should be inspectable");

        assert_eq!(result["serialized_value"], json!(7));
        assert_eq!(result["type_path"], json!(health_type_path()));
    }
```

### 🔹 函式: `component_metadata_contains_registered_component()`
- **變更前簽章 (Before)**: `fn component_metadata_contains_registered_component()` (L445~L456)
- **變更後簽章 (After)**: `fn component_metadata_contains_registered_component()` (L447~L459)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn component_metadata_contains_registered_component() {
        let mut world = test_world();
        world.spawn(Health(7));

        let result = process_remote_component_metadata_request(In(None), &world)
            .expect("the metadata map should be serializable");

        let map = result["map"].as_object().unwrap();
        assert!(map
            .values()
            .any(|metadata| metadata["name"] == json!(health_type_path())));
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn component_metadata_contains_registered_component() {
        let mut world = test_world();
        world.spawn(Health(7));

        let result = process_remote_component_metadata_request(In(None), &world)
            .expect("the metadata map should be serializable");

        let map = result["map"].as_object().unwrap();
        assert!(map
            .values()
            .any(|metadata| metadata["name"] == json!(health_type_path())
                && metadata["type_path"] == json!(health_type_path())));
    }
```

### 🔹 函式: `inspect_returns_label_and_serialized_component()`
- **變更前簽章 (Before)**: `fn inspect_returns_label_and_serialized_component()` (L304~L319)
- **變更後簽章 (After)**: `fn inspect_returns_label_and_serialized_component()` (L304~L320)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn inspect_returns_label_and_serialized_component() {
        let mut world = test_world();
        let entity = world.spawn((Name::new("Player"), Health(7))).id();

        let result = process_remote_inspect_request(In(Some(json!({ "entity": entity }))), &world)
            .expect("the entity should be inspectable");

        assert_eq!(result["label"]["label"], json!("Player"));

        let components = result["components"].as_array().unwrap();
        let health = components
            .iter()
            .find(|component| component["name"] == json!(health_type_path()))
            .expect("the `Health` component should be inspected");
        assert_eq!(health["serialized_value"], json!(7));
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn inspect_returns_label_and_serialized_component() {
        let mut world = test_world();
        let entity = world.spawn((Name::new("Player"), Health(7))).id();

        let result = process_remote_inspect_request(In(Some(json!({ "entity": entity }))), &world)
            .expect("the entity should be inspectable");

        assert_eq!(result["label"]["label"], json!("Player"));

        let components = result["components"].as_array().unwrap();
        let health = components
            .iter()
            .find(|component| component["name"] == json!(health_type_path()))
            .expect("the `Health` component should be inspected");
        assert_eq!(health["serialized_value"], json!(7));
        assert_eq!(health["type_path"], json!(health_type_path()));
    }
```


---

### 🔹 Commit #08: `ae9a94fc`
- **完整 Hash**: `ae9a94fcd49a2b1205d80731a18e1ac1984375cc`
- **說明 (Ground Truth)**: Ignore ecs tests that require the `debug` feature when it isn't enabled (#26109)
- **變更檔案數**: 3

#### 📄 檔案: `crates/bevy_ecs/src/error/bevy_error.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:110, E:131, A:0) ➔ After(N:110, E:131, A:0)
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

#### 📄 檔案: `crates/bevy_ecs/src/system/combinator.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:83, E:92, A:0) ➔ After(N:83, E:92, A:0)
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

#### 📄 檔案: `crates/bevy_ecs/src/system/system_param.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:374, E:407, A:0) ➔ After(N:374, E:407, A:0)
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

### 🔹 Commit #09: `48ae9fc0`
- **完整 Hash**: `48ae9fc0a1a445dba9f3c5fe55fb5d8de3186ac7`
- **說明 (Ground Truth)**: fix UninitBufferVec to use shader's size for each entry instead of Ru… (#26090)
- **變更檔案數**: 1

#### 📄 檔案: `crates/bevy_render/src/render_resource/buffer_vec.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:112, E:153, A:0) ➔ After(N:114, E:155, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 3, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `assert_eq! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `uninit_buffer_vec_uses_shader_size` (FUNCTION_DEF)
  • + [新增呼叫邊] `UninitBufferVec::new` ──[CALLS]──> `AtomicRawBufferVec::get`
  • + [新增呼叫邊] `uninit_buffer_vec_uses_shader_size` ──[CALLS]──> `assert_eq! (Macro)`
  • + [新增呼叫邊] `uninit_buffer_vec_uses_shader_size` ──[CALLS]──> `PartialBufferVec::new`
  • - [移除呼叫邊] `UninitBufferVec::new` ──[CALLS]──> `size_of::<T> (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `UninitBufferVec::new()`
- **變更前簽章 (Before)**: `fn UninitBufferVec::new(buffer_usage: BufferUsages)` (L708~L719)
- **變更後簽章 (After)**: `fn UninitBufferVec::new(buffer_usage: BufferUsages)` (L708~L719)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub const fn new(buffer_usage: BufferUsages) -> Self {
        Self {
            len: 0,
            buffer: None,
            capacity: 0,
            item_size: size_of::<T>(),
            buffer_usage,
            label: None,
            label_changed: false,
            phantom: PhantomData,
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub const fn new(buffer_usage: BufferUsages) -> Self {
        Self {
            len: 0,
            buffer: None,
            capacity: 0,
            item_size: T::SHADER_SIZE.get() as usize,
            buffer_usage,
            label: None,
            label_changed: false,
            phantom: PhantomData,
        }
    }
```


---

### 🔹 Commit #10: `c9c21c2b`
- **完整 Hash**: `c9c21c2b7af92a396b5f93ecfa1536a8a2afcc68`
- **說明 (Ground Truth)**: Enter the schedule span on worker threads in the multi-threaded executor (#25911)
- **變更檔案數**: 2

#### 📄 檔案: `crates/bevy_ecs/src/schedule/schedule.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:585, E:984, A:0) ➔ After(N:590, E:991, A:0)
- **差分統計**: +Nodes: 6, -Nodes: 1, +Edges: 9, -Edges: 2, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `(Span::current().id() != self.span.id()).then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.span.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Span::current().id (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.span.clone().entered (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Span::current (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.span.id (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `info_span!("schedule", name = ?self.label).entered (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Schedule::new` ──[CALLS]──> `info_span! (Macro)`
  • + [新增呼叫邊] `Schedule::run` ──[CALLS]──> `self.span.clone().entered (External/Unresolved)`
  • + [新增呼叫邊] `Schedule::run` ──[CALLS]──> `self.span.clone (External/Unresolved)`
  • + [新增呼叫邊] `Schedule::initialize` ──[CALLS]──> `(Span::current().id() != self.span.id()).then (External/Unresolved)`
  • + [新增呼叫邊] `Schedule::initialize` ──[CALLS]──> `Span::current().id (External/Unresolved)`
  • + [新增呼叫邊] `Schedule::initialize` ──[CALLS]──> `Span::current (External/Unresolved)`
  • + [新增呼叫邊] `Schedule::initialize` ──[CALLS]──> `self.span.id (External/Unresolved)`
  • + [新增呼叫邊] `Schedule::initialize` ──[CALLS]──> `self.span.clone().entered (External/Unresolved)`
  • _... 以及其餘 3 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Schedule::new()`
- **變更前簽章 (Before)**: `fn Schedule::new(label: impl ScheduleLabel)` (L436~L447)
- **變更後簽章 (After)**: `fn Schedule::new(label: impl ScheduleLabel)` (L438~L452)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn new(label: impl ScheduleLabel) -> Self {
        let mut this = Self {
            label: label.intern(),
            graph: ScheduleGraph::new(),
            executable: SystemSchedule::new(),
            executor: default_executor(),
            executor_initialized: false,
        };
        // Call `set_build_settings` to add any default build passes
        this.set_build_settings(Default::default());
        this
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn new(label: impl ScheduleLabel) -> Self {
        let label = label.intern();
        let mut this = Self {
            label,
            graph: ScheduleGraph::new(),
            executable: SystemSchedule::new(),
            executor: default_executor(),
            executor_initialized: false,
            #[cfg(feature = "trace")]
            span: info_span!(parent: None, "schedule", name = ?label),
        };
        // Call `set_build_settings` to add any default build passes
        this.set_build_settings(Default::default());
        this
    }
```

### 🔹 函式: `Schedule::initialize()`
- **變更前簽章 (Before)**: `fn Schedule::initialize(
        &mut self,
        world: &mut World,
    )` (L632~L666)
- **變更後簽章 (After)**: `fn Schedule::initialize(
        &mut self,
        world: &mut World,
    )` (L637~L674)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn initialize(
        &mut self,
        world: &mut World,
    ) -> Result<Option<ScheduleBuildMetadata>, ScheduleBuildError> {
        let mut build_metadata = None;
        if self.graph.changed {
            self.graph.initialize(world);
            let ignored_ambiguities = world
                .get_resource_or_init::<Schedules>()
                .ignored_scheduling_ambiguities
                .clone();

            let mut event = ScheduleBuilt {
                label: self.label,
                build_metadata: self.graph.update_schedule(
                    world,
                    &mut self.executable,
                    &ignored_ambiguities,
                    self.label,
                )?,
            };
            self.graph.changed = false;
            self.executor_initialized = false;

            world.trigger_ref(&mut event);
            build_metadata = Some(event.build_metadata);
        }

        if !self.executor_initialized {
            self.executor.init(&self.executable);
            self.executor_initialized = true;
        }

        Ok(build_metadata)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn initialize(
        &mut self,
        world: &mut World,
    ) -> Result<Option<ScheduleBuildMetadata>, ScheduleBuildError> {
        let mut build_metadata = None;
        if self.graph.changed {
            #[cfg(feature = "trace")]
            let _span =
                (Span::current().id() != self.span.id()).then(|| self.span.clone().entered());
            self.graph.initialize(world);
            let ignored_ambiguities = world
                .get_resource_or_init::<Schedules>()
                .ignored_scheduling_ambiguities
                .clone();

            let mut event = ScheduleBuilt {
                label: self.label,
                build_metadata: self.graph.update_schedule(
                    world,
                    &mut self.executable,
                    &ignored_ambiguities,
                    self.label,
                )?,
            };
            self.graph.changed = false;
            self.executor_initialized = false;

            world.trigger_ref(&mut event);
            build_metadata = Some(event.build_metadata);
        }

        if !self.executor_initialized {
            self.executor.init(&self.executable);
            self.executor_initialized = true;
        }

        Ok(build_metadata)
    }
```

### 🔹 函式: `Schedule::run()`
- **變更前簽章 (Before)**: `fn Schedule::run(&mut self, world: &mut World)` (L591~L624)
- **變更後簽章 (After)**: `fn Schedule::run(&mut self, world: &mut World)` (L596~L629)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn run(&mut self, world: &mut World) {
        #[cfg(feature = "trace")]
        let _span = info_span!("schedule", name = ?self.label).entered();

        world.check_change_ticks();
        self.initialize(world).unwrap_or_else(|e| {
            panic!(
                "Error when initializing schedule {:?}: {}",
                self.label,
                e.to_string(self.graph(), world)
            )
        });

        let error_handler = world.fallback_error_handler();

        #[cfg(not(feature = "bevy_debug_stepping"))]
        self.executor
            .run(&mut self.executable, world, None, error_handler);

        #[cfg(feature = "bevy_debug_stepping")]
        {
            let skip_systems = match world.get_resource_mut::<Stepping>() {
                None => None,
                Some(mut stepping) => stepping.skipped_systems(self),
            };

            self.executor.run(
                &mut self.executable,
                world,
                skip_systems.as_ref(),
                error_handler,
            );
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn run(&mut self, world: &mut World) {
        #[cfg(feature = "trace")]
        let _span = self.span.clone().entered();

        world.check_change_ticks();
        self.initialize(world).unwrap_or_else(|e| {
            panic!(
                "Error when initializing schedule {:?}: {}",
                self.label,
                e.to_string(self.graph(), world)
            )
        });

        let error_handler = world.fallback_error_handler();

        #[cfg(not(feature = "bevy_debug_stepping"))]
        self.executor
            .run(&mut self.executable, world, None, error_handler);

        #[cfg(feature = "bevy_debug_stepping")]
        {
            let skip_systems = match world.get_resource_mut::<Stepping>() {
                None => None,
                Some(mut stepping) => stepping.skipped_systems(self),
            };

            self.executor.run(
                &mut self.executable,
                world,
                skip_systems.as_ref(),
                error_handler,
            );
        }
    }
```


#### 📄 檔案: `crates/bevy_ecs/src/system/function_system.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:130, E:132, A:0) ➔ After(N:134, E:139, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 7, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `self.system_meta.name.clone().to_string (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Span::current (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `parent.metadata (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `parent.metadata().is_some_and (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `FunctionSystem::initialize` ──[CALLS]──> `Span::current (External/Unresolved)`
  • + [新增呼叫邊] `FunctionSystem::initialize` ──[CALLS]──> `parent.metadata().is_some_and (External/Unresolved)`
  • + [新增呼叫邊] `FunctionSystem::initialize` ──[CALLS]──> `parent.metadata (External/Unresolved)`
  • + [新增呼叫邊] `FunctionSystem::initialize` ──[CALLS]──> `FunctionSystem::name`
  • + [新增呼叫邊] `FunctionSystem::initialize` ──[CALLS]──> `self.system_meta.name.clone().to_string (External/Unresolved)`
  • + [新增呼叫邊] `FunctionSystem::initialize` ──[CALLS]──> `FunctionSystem::clone`
  • + [新增呼叫邊] `FunctionSystem::initialize` ──[CALLS]──> `info_span! (Macro)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FunctionSystem::initialize()`
- **變更前簽章 (Before)**: `fn FunctionSystem::initialize(&mut self, world: &mut World)` (L880~L897)
- **變更後簽章 (After)**: `fn FunctionSystem::initialize(&mut self, world: &mut World)` (L880~L906)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn initialize(&mut self, world: &mut World) -> SystemAccess {
        if let Some(state) = &self.state {
            assert_eq!(
                state.world_id,
                world.id(),
                "System built with a different world than the one it was added to.",
            );
        }
        let state = self.state.get_or_insert_with(|| FunctionSystemState {
            param: F::Param::init_state(world),
            world_id: world.id(),
        });
        self.system_meta.last_run = world.change_tick().relative_to(Tick::MAX);
        let access =
            init_param_or_panic::<F::Param>(&state.param, &mut self.system_meta, world.into());
        self.is_exclusive = access.is_exclusive();
        access
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn initialize(&mut self, world: &mut World) -> SystemAccess {
        if let Some(state) = &self.state {
            assert_eq!(
                state.world_id,
                world.id(),
                "System built with a different world than the one it was added to.",
            );
        }
        let state = self.state.get_or_insert_with(|| FunctionSystemState {
            param: F::Param::init_state(world),
            world_id: world.id(),
        });
        #[cfg(feature = "trace")]
        {
            // Only a schedule's own span becomes the parent, never e.g. the "plugin build" span.
            let parent = Span::current();
            if parent.metadata().is_some_and(|m| m.name() == "schedule") {
                let name = self.system_meta.name.clone().to_string();
                self.system_meta.system_span = info_span!(parent: &parent, "system", name = name);
            }
        }
        self.system_meta.last_run = world.change_tick().relative_to(Tick::MAX);
        let access =
            init_param_or_panic::<F::Param>(&state.param, &mut self.system_meta, world.into());
        self.is_exclusive = access.is_exclusive();
        access
    }
```


---

### 🔹 Commit #11: `5a037496`
- **完整 Hash**: `5a03749600e04697bf2ad9c90b9f0919af948d43`
- **說明 (Ground Truth)**: Fix `replace_related` allowing duplicate entities (#26048)
- **變更檔案數**: 2

#### 📄 檔案: `crates/bevy_ecs/src/hierarchy.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:117, E:234, A:0) ➔ After(N:119, E:243, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 9, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `world.entity_mut(parent).clear (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `replace_children_duplicates` (FUNCTION_DEF)
  • + [新增呼叫邊] `replace_children_duplicates` ──[CALLS]──> `Node::new`
  • + [新增呼叫邊] `replace_children_duplicates` ──[CALLS]──> `world.spawn_empty().id (External/Unresolved)`
  • + [新增呼叫邊] `replace_children_duplicates` ──[CALLS]──> `world.spawn_empty (External/Unresolved)`
  • + [新增呼叫邊] `replace_children_duplicates` ──[CALLS]──> `replace_children`
  • + [新增呼叫邊] `replace_children_duplicates` ──[CALLS]──> `add_children`
  • + [新增呼叫邊] `replace_children_duplicates` ──[CALLS]──> `world
            .entity_mut (External/Unresolved)`
  • + [新增呼叫邊] `replace_children_duplicates` ──[CALLS]──> `assert_eq! (Macro)`
  • + [新增呼叫邊] `replace_children_duplicates` ──[CALLS]──> `world.entity_mut(parent).clear (External/Unresolved)`
  • + [新增呼叫邊] `replace_children_duplicates` ──[CALLS]──> `world.entity_mut (External/Unresolved)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `crates/bevy_ecs/src/relationship/related_methods.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:177, E:250, A:0) ➔ After(N:179, E:251, A:0)
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
  • + [新增節點] `final_relations.difference (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `existing_relations.difference (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `EntityIndexSet::from_iter (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `potential_relations.remove (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `EntityWorldMut::replace_related` ──[CALLS]──> `EntityIndexSet::from_iter (External/Unresolved)`
  • + [新增呼叫邊] `EntityWorldMut::replace_related` ──[CALLS]──> `existing_relations.difference (External/Unresolved)`
  • + [新增呼叫邊] `EntityWorldMut::replace_related` ──[CALLS]──> `final_relations.difference (External/Unresolved)`
  • - [移除呼叫邊] `EntityWorldMut::replace_related` ──[CALLS]──> `EntityHashSet::from_iter (External/Unresolved)`
  • - [移除呼叫邊] `EntityWorldMut::replace_related` ──[CALLS]──> `potential_relations.remove (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `EntityWorldMut::replace_related_with_difference()`
- **變更前簽章 (Before)**: `fn EntityWorldMut::replace_related_with_difference(
        &mut self,
        entities_to_unrelate: &[Entity],
        entities_to_relate: &[Entity],
        newly_related_entities: &[Entity],
    )` (L216~L290)
- **變更後簽章 (After)**: `fn EntityWorldMut::replace_related_with_difference(
        &mut self,
        entities_to_unrelate: &[Entity],
        entities_to_relate: &[Entity],
        newly_related_entities: &[Entity],
    )` (L219~L294)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn replace_related_with_difference<R: Relationship>(
        &mut self,
        entities_to_unrelate: &[Entity],
        entities_to_relate: &[Entity],
        newly_related_entities: &[Entity],
    ) -> &mut Self {
        #[cfg(debug_assertions)]
        {
            let entities_to_relate = EntityHashSet::from_iter(entities_to_relate.iter().copied());
            let entities_to_unrelate =
                EntityHashSet::from_iter(entities_to_unrelate.iter().copied());
            let mut newly_related_entities =
                EntityHashSet::from_iter(newly_related_entities.iter().copied());
            assert!(
                entities_to_relate.is_disjoint(&entities_to_unrelate),
                "`entities_to_relate` ({entities_to_relate:?}) shared entities with `entities_to_unrelate` ({entities_to_unrelate:?})"
            );
            assert!(
                newly_related_entities.is_disjoint(&entities_to_unrelate),
                "`newly_related_entities` ({newly_related_entities:?}) shared entities with `entities_to_unrelate ({entities_to_unrelate:?})`"
            );
            assert!(
                newly_related_entities.is_subset(&entities_to_relate),
                "`newly_related_entities` ({newly_related_entities:?}) wasn't a subset of `entities_to_relate` ({entities_to_relate:?})"
            );

            if let Some(target) = self.get::<R::RelationshipTarget>() {
                let existing_relationships: EntityHashSet = target.collection().iter().collect();

                assert!(
                    existing_relationships.is_disjoint(&newly_related_entities),
                    "`newly_related_entities` contains an entity that wouldn't be newly related"
                );

                newly_related_entities.extend(existing_relationships);
                newly_related_entities -= &entities_to_unrelate;
            }

            assert_eq!(newly_related_entities, entities_to_relate, "`entities_to_relate` ({entities_to_relate:?}) didn't contain all entities that would end up related");
        };

        match self.get_mut::<R::RelationshipTarget>() {
            None => {
                self.add_related::<R>(entities_to_relate);

                return self;
            }
            Some(mut target) => {
                // SAFETY: The invariants expected by this function mean we'll only be inserting entities that are already related.
                let collection = target.collection_mut_risky();
                collection.clear();

                collection.extend_from_iter(entities_to_relate.iter().copied());
            }
        }

        let this = self.id();
        self.world_scope(|world| {
            for unrelate in entities_to_unrelate {
                world.entity_mut(*unrelate).remove::<R>();
            }

            for new_relation in newly_related_entities {
                // We changed the target collection manually so don't run the insert hook
                world
                    .entity_mut(*new_relation)
                    .modify_or_insert_relation_with_relationship_hook_mode::<R>(
                        this,
                        RelationshipHookMode::Skip,
                    );
            }
        });

        self
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn replace_related_with_difference<R: Relationship>(
        &mut self,
        entities_to_unrelate: &[Entity],
        entities_to_relate: &[Entity],
        newly_related_entities: &[Entity],
    ) -> &mut Self {
        #[cfg(debug_assertions)]
        {
            use crate::entity::hash_set::EntityHashSet;
            let entities_to_relate = EntityHashSet::from_iter(entities_to_relate.iter().copied());
            let entities_to_unrelate =
                EntityHashSet::from_iter(entities_to_unrelate.iter().copied());
            let mut newly_related_entities =
                EntityHashSet::from_iter(newly_related_entities.iter().copied());
            assert!(
                entities_to_relate.is_disjoint(&entities_to_unrelate),
                "`entities_to_relate` ({entities_to_relate:?}) shared entities with `entities_to_unrelate` ({entities_to_unrelate:?})"
            );
            assert!(
                newly_related_entities.is_disjoint(&entities_to_unrelate),
                "`newly_related_entities` ({newly_related_entities:?}) shared entities with `entities_to_unrelate ({entities_to_unrelate:?})`"
            );
            assert!(
                newly_related_entities.is_subset(&entities_to_relate),
                "`newly_related_entities` ({newly_related_entities:?}) wasn't a subset of `entities_to_relate` ({entities_to_relate:?})"
            );

            if let Some(target) = self.get::<R::RelationshipTarget>() {
                let existing_relationships: EntityHashSet = target.collection().iter().collect();

                assert!(
                    existing_relationships.is_disjoint(&newly_related_entities),
                    "`newly_related_entities` contains an entity that wouldn't be newly related"
                );

                newly_related_entities.extend(existing_relationships);
                newly_related_entities -= &entities_to_unrelate;
            }

            assert_eq!(newly_related_entities, entities_to_relate, "`entities_to_relate` ({entities_to_relate:?}) didn't contain all entities that would end up related");
        };

        match self.get_mut::<R::RelationshipTarget>() {
            None => {
                self.add_related::<R>(entities_to_relate);

                return self;
            }
            Some(mut target) => {
                // SAFETY: The invariants expected by this function mean we'll only be inserting entities that are already related.
                let collection = target.collection_mut_risky();
                collection.clear();

                collection.extend_from_iter(entities_to_relate.iter().copied());
            }
        }

        let this = self.id();
        self.world_scope(|world| {
            for unrelate in entities_to_unrelate {
                world.entity_mut(*unrelate).remove::<R>();
            }

            for new_relation in newly_related_entities {
                // We changed the target collection manually so don't run the insert hook
                world
                    .entity_mut(*new_relation)
                    .modify_or_insert_relation_with_relationship_hook_mode::<R>(
                        this,
                        RelationshipHookMode::Skip,
                    );
            }
        });

        self
    }
```

### 🔹 函式: `EntityWorldMut::replace_related()`
- **變更前簽章 (Before)**: `fn EntityWorldMut::replace_related(&mut self, related: &[Entity])` (L142~L194)
- **變更後簽章 (After)**: `fn EntityWorldMut::replace_related(&mut self, related: &[Entity])` (L144~L197)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn replace_related<R: Relationship>(&mut self, related: &[Entity]) -> &mut Self {
        type Collection<R> =
            <<R as Relationship>::RelationshipTarget as RelationshipTarget>::Collection;

        if related.is_empty() {
            self.remove::<R::RelationshipTarget>();

            return self;
        }

        let Some(existing_relations) = self.get_mut::<R::RelationshipTarget>() else {
            return self.add_related::<R>(related);
        };

        // We replace the component here with a dummy value so we can modify it without taking it (this would create archetype move).
        // SAFETY: We eventually return the correctly initialized collection into the target.
        let mut relations = mem::replace(
            existing_relations.into_inner(),
            <R as Relationship>::RelationshipTarget::from_collection_risky(
                Collection::<R>::with_capacity(0),
            ),
        );

        let collection = relations.collection_mut_risky();

        let mut potential_relations = EntityHashSet::from_iter(related.iter().copied());

        let id = self.id();
        self.world_scope(|world| {
            for related in collection.iter() {
                if !potential_relations.remove(related) {
                    world.entity_mut(related).remove::<R>();
                }
            }

            for related in potential_relations {
                // SAFETY: We'll manually be adjusting the contents of the `RelationshipTarget` to fit the final state.
                world
                    .entity_mut(related)
                    .modify_or_insert_relation_with_relationship_hook_mode::<R>(
                        id,
                        RelationshipHookMode::Skip,
                    );
            }
        });

        // SAFETY: The entities we're inserting will be the entities that were either already there or entities that we've just inserted.
        collection.clear();
        collection.extend_from_iter(related.iter().copied());
        self.insert(relations);

        self
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn replace_related<R: Relationship>(&mut self, related: &[Entity]) -> &mut Self {
        type Collection<R> =
            <<R as Relationship>::RelationshipTarget as RelationshipTarget>::Collection;

        if related.is_empty() {
            self.remove::<R::RelationshipTarget>();

            return self;
        }

        let Some(existing_relations) = self.get_mut::<R::RelationshipTarget>() else {
            return self.add_related::<R>(related);
        };

        // We replace the component here with a dummy value so we can modify it without taking it (this would create archetype move).
        // SAFETY: We eventually return the correctly initialized collection into the target.
        let mut relations = mem::replace(
            existing_relations.into_inner(),
            <R as Relationship>::RelationshipTarget::from_collection_risky(
                Collection::<R>::with_capacity(0),
            ),
        );

        let collection = relations.collection_mut_risky();

        let existing_relations = EntityIndexSet::from_iter(collection.iter());
        let final_relations = EntityIndexSet::from_iter(related.iter().copied());

        let id = self.id();
        self.world_scope(|world| {
            // Remove the existing relations that we won't keep
            for &related in existing_relations.difference(&final_relations) {
                world.entity_mut(related).remove::<R>();
            }

            // Add the final relations that don't exist yet.
            for &related in final_relations.difference(&existing_relations) {
                // SAFETY: We'll manually be adjusting the contents of the `RelationshipTarget` to fit the final state.
                world
                    .entity_mut(related)
                    .modify_or_insert_relation_with_relationship_hook_mode::<R>(
                        id,
                        RelationshipHookMode::Skip,
                    );
            }
        });

        // SAFETY: The entities we're inserting will be the entities that were either already there or entities that we've just inserted.
        collection.clear();
        collection.extend_from_iter(final_relations);
        self.insert(relations);

        self
    }
```


---

### 🔹 Commit #12: `d08bd605`
- **完整 Hash**: `d08bd60564981fe76b5406322ccce505398f9cf8`
- **說明 (Ground Truth)**: Fix UI surface rounding (#26026)
- **變更檔案數**: 2

#### 📄 檔案: `crates/bevy_ui/src/layout/mod.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:468, E:907, A:0) ➔ After(N:472, E:919, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 12, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `app.world_mut().get_mut::<Node>(root).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app
            .world_mut()
            .spawn(Node {
                width: px(100.),
                height: px(100.),
                ..default()
            })
            .with_child((
                Node::default(),
                LayoutConfig {
                    use_rounding: false,
                },
            ))
            .id (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `rounding_test` (FUNCTION_DEF)
  • + [新增節點] `app
            .world_mut()
            .spawn(Node {
                width: px(100.),
                height: px(100.),
                ..default()
            })
            .with_child (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `rounding_test` ──[CALLS]──> `setup_ui_test_app`
  • + [新增呼叫邊] `rounding_test` ──[CALLS]──> `app
            .world_mut()
            .spawn(Node {
                width: px(100.),
                height: px(100.),
                ..default()
            })
            .with_child((
                Node::default(),
                LayoutConfig {
                    use_rounding: false,
                },
            ))
            .id (External/Unresolved)`
  • + [新增呼叫邊] `rounding_test` ──[CALLS]──> `app
            .world_mut()
            .spawn(Node {
                width: px(100.),
                height: px(100.),
                ..default()
            })
            .with_child (External/Unresolved)`
  • + [新增呼叫邊] `rounding_test` ──[CALLS]──> `app
            .world_mut()
            .spawn (External/Unresolved)`
  • + [新增呼叫邊] `rounding_test` ──[CALLS]──> `app
            .world_mut (External/Unresolved)`
  • + [新增呼叫邊] `rounding_test` ──[CALLS]──> `px (External/Unresolved)`
  • + [新增呼叫邊] `rounding_test` ──[CALLS]──> `LayoutContext::default`
  • + [新增呼叫邊] `rounding_test` ──[CALLS]──> `app.update (External/Unresolved)`
  • + [新增呼叫邊] `rounding_test` ──[CALLS]──> `assert_eq! (Macro)`
  • + [新增呼叫邊] `rounding_test` ──[CALLS]──> `app.world_mut().get_mut::<Node>(root).unwrap (External/Unresolved)`
  • + [新增呼叫邊] `rounding_test` ──[CALLS]──> `app.world_mut().get_mut::<Node> (External/Unresolved)`
  • _... 以及其餘 1 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `crates/bevy_ui/src/layout/ui_surface.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:138, E:166, A:0) ➔ After(N:138, E:167, A:0)
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
  • + [新增呼叫邊] `UiSurface::compute_layout` ──[CALLS]──> `self.taffy.enable_rounding (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `UiSurface::get_layout()`
- **變更前簽章 (Before)**: `fn UiSurface::get_layout(
        &mut self,
        entity: Entity,
        use_rounding: bool,
    )` (L309~L336)
- **變更後簽章 (After)**: `fn UiSurface::get_layout(
        &mut self,
        entity: Entity,
        use_rounding: bool,
    )` (L313~L342)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn get_layout(
        &mut self,
        entity: Entity,
        use_rounding: bool,
    ) -> Result<(taffy::Layout, Vec2), UiSurfaceError> {
        let Some(taffy_node) = self.entity_to_taffy.get(&entity) else {
            return Err(UiSurfaceError::NoAssociatedTaffyNode);
        };

        if use_rounding {
            self.taffy.enable_rounding();
        } else {
            self.taffy.disable_rounding();
        }

        let out = match self.taffy.layout(taffy_node.id).cloned() {
            Ok(layout) => {
                self.taffy.disable_rounding();
                let taffy_size = self.taffy.layout(taffy_node.id).unwrap().size;
                let unrounded_size = Vec2::new(taffy_size.width, taffy_size.height);
                Ok((layout, unrounded_size))
            }
            Err(taffy_error) => Err(UiSurfaceError::TaffyError(taffy_error)),
        };

        self.taffy.enable_rounding();
        out
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn get_layout(
        &mut self,
        entity: Entity,
        use_rounding: bool,
    ) -> Result<(taffy::Layout, Vec2), UiSurfaceError> {
        let Some(taffy_node) = self.entity_to_taffy.get(&entity) else {
            return Err(UiSurfaceError::NoAssociatedTaffyNode);
        };

        // Note: Taffy's enable/disable_rounding has a dual purpose:
        // 1. It controls whether rounded geometry is generated during compute_layout.
        // 2. It controls whether the per-node layout() getter returns rounded or unrounded geometry.
        // Here we temporarily toggle it to fetch the unrounded size regardless of the global state.
        if use_rounding {
            self.taffy.enable_rounding();
        } else {
            self.taffy.disable_rounding();
        }

        let layout = self.taffy.layout(taffy_node.id).cloned();

        self.taffy.disable_rounding();
        let taffy_size = self.taffy.layout(taffy_node.id).unwrap().size;
        let unrounded_size = Vec2::new(taffy_size.width, taffy_size.height);

        match layout {
            Ok(l) => Ok((l, unrounded_size)),
            Err(taffy_error) => Err(UiSurfaceError::TaffyError(taffy_error)),
        }
    }
```

### 🔹 函式: `UiSurface::compute_layout()`
- **變更前簽章 (Before)**: `fn UiSurface::compute_layout(
        &mut self,
        ui_root_entity: Entity,
        render_target_resolution: UVec2,
        buffer_query: &'a mut bevy_ecs::prelude::Query<&mut bevy_text::ComputedTextBlock>,
        font_system: &'a mut FontCx,
    )` (L226~L287)
- **變更後簽章 (After)**: `fn UiSurface::compute_layout(
        &mut self,
        ui_root_entity: Entity,
        render_target_resolution: UVec2,
        buffer_query: &'a mut bevy_ecs::prelude::Query<&mut bevy_text::ComputedTextBlock>,
        font_system: &'a mut FontCx,
    )` (L226~L291)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn compute_layout<'a>(
        &mut self,
        ui_root_entity: Entity,
        render_target_resolution: UVec2,
        buffer_query: &'a mut bevy_ecs::prelude::Query<&mut bevy_text::ComputedTextBlock>,
        font_system: &'a mut FontCx,
    ) {
        let implicit_viewport_node = self.get_or_insert_taffy_viewport_node(ui_root_entity);

        let available_space = taffy::geometry::Size {
            width: taffy::style::AvailableSpace::Definite(render_target_resolution.x as f32),
            height: taffy::style::AvailableSpace::Definite(render_target_resolution.y as f32),
        };

        self.taffy
            .compute_layout_with_measure(
                implicit_viewport_node,
                available_space,
                |layout_input: taffy::LayoutInput,
                 _node_id: NodeId,
                 context: Option<&mut NodeMeasure>,
                 style: &Style|
                 -> taffy::LayoutOutput {
                    taffy::compute_leaf_layout(
                        layout_input,
                        style,
                        |_, _| 0.0,
                        |known_dimensions, available_space| {
                            context
                                .map(|ctx| {
                                    let mut measure_args = MeasureArgs {
                                        known_width: known_dimensions.width,
                                        known_height: known_dimensions.height,
                                        available_width: available_space.width,
                                        available_height: available_space.height,
                                        font_system,
                                        buffer: None,
                                        style,
                                    };
                                    let buffer = get_text_buffer(
                                        crate::widget::TextMeasure::needs_buffer(
                                            measure_args.resolve_width().effective,
                                            measure_args.resolve_height().effective,
                                            available_space.width,
                                        ),
                                        ctx,
                                        buffer_query,
                                    );
                                    measure_args.buffer = buffer;
                                    let size = ctx.measure(measure_args);
                                    taffy::Size {
                                        width: size.x,
                                        height: size.y,
                                    }
                                })
                                .unwrap_or(taffy::Size::ZERO)
                        },
                    )
                },
            )
            .unwrap();
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn compute_layout<'a>(
        &mut self,
        ui_root_entity: Entity,
        render_target_resolution: UVec2,
        buffer_query: &'a mut bevy_ecs::prelude::Query<&mut bevy_text::ComputedTextBlock>,
        font_system: &'a mut FontCx,
    ) {
        let implicit_viewport_node = self.get_or_insert_taffy_viewport_node(ui_root_entity);

        // Ensure rounding is enabled globally before computing the layout tree,
        // as enable/disable_rounding controls whether rounded node geometry is created during layout.
        self.taffy.enable_rounding();

        let available_space = taffy::geometry::Size {
            width: taffy::style::AvailableSpace::Definite(render_target_resolution.x as f32),
            height: taffy::style::AvailableSpace::Definite(render_target_resolution.y as f32),
        };

        self.taffy
            .compute_layout_with_measure(
                implicit_viewport_node,
                available_space,
                |layout_input: taffy::LayoutInput,
                 _node_id: NodeId,
                 context: Option<&mut NodeMeasure>,
                 style: &Style|
                 -> taffy::LayoutOutput {
                    taffy::compute_leaf_layout(
                        layout_input,
                        style,
                        |_, _| 0.0,
                        |known_dimensions, available_space| {
                            context
                                .map(|ctx| {
                                    let mut measure_args = MeasureArgs {
                                        known_width: known_dimensions.width,
                                        known_height: known_dimensions.height,
                                        available_width: available_space.width,
                                        available_height: available_space.height,
                                        font_system,
                                        buffer: None,
                                        style,
                                    };
                                    let buffer = get_text_buffer(
                                        crate::widget::TextMeasure::needs_buffer(
                                            measure_args.resolve_width().effective,
                                            measure_args.resolve_height().effective,
                                            available_space.width,
                                        ),
                                        ctx,
                                        buffer_query,
                                    );
                                    measure_args.buffer = buffer;
                                    let size = ctx.measure(measure_args);
                                    taffy::Size {
                                        width: size.x,
                                        height: size.y,
                                    }
                                })
                                .unwrap_or(taffy::Size::ZERO)
                        },
                    )
                },
            )
            .unwrap();
    }
```


---

### 🔹 Commit #13: `a55191f0`
- **完整 Hash**: `a55191f0e5e9178e908f300e284cb4390d5e01a4`
- **說明 (Ground Truth)**: Fix timer remaining-time panic and completion-count overflow (#25995)
- **變更檔案數**: 1

#### 📄 檔案: `crates/bevy_time/src/timer.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:51, E:88, A:0) ➔ After(N:59, E:111, A:0)
- **差分統計**: +Nodes: 9, -Nodes: 1, +Edges: 24, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `self
                    .elapsed()
                    .as_nanos()
                    .checked_div(self.duration().as_nanos())
                    .and_then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `remaining_after_shortening_duration` (FUNCTION_DEF)
  • + [新增節點] `self
                    .elapsed()
                    .as_nanos()
                    .checked_div(self.duration().as_nanos())
                    .and_then(|x| u32::try_from(x).ok())
                    .unwrap_or (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `u32::try_from (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.duration().saturating_sub (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `times_finished_this_tick_saturates` (FUNCTION_DEF)
  • + [新增節點] `remaining_after_setting_elapsed_past_duration` (FUNCTION_DEF)
  • + [新增節點] `u32::try_from(x).ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `u64::from (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `self
                    .elapsed()
                    .as_nanos()
                    .checked_div(self.duration().as_nanos())
                    .map_or (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Timer::tick` ──[CALLS]──> `self
                    .elapsed()
                    .as_nanos()
                    .checked_div(self.duration().as_nanos())
                    .and_then(|x| u32::try_from(x).ok())
                    .unwrap_or (External/Unresolved)`
  • + [新增呼叫邊] `Timer::tick` ──[CALLS]──> `self
                    .elapsed()
                    .as_nanos()
                    .checked_div(self.duration().as_nanos())
                    .and_then (External/Unresolved)`
  • + [新增呼叫邊] `Timer::tick` ──[CALLS]──> `u32::try_from(x).ok (External/Unresolved)`
  • + [新增呼叫邊] `Timer::tick` ──[CALLS]──> `u32::try_from (External/Unresolved)`
  • + [新增呼叫邊] `Timer::remaining` ──[CALLS]──> `self.duration().saturating_sub (External/Unresolved)`
  • _... 以及其餘 20 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Timer::tick()`
- **變更前簽章 (Before)**: `fn Timer::tick(&mut self, delta: Duration)` (L280~L319)
- **變更後簽章 (After)**: `fn Timer::tick(&mut self, delta: Duration)` (L280~L320)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn tick(&mut self, delta: Duration) -> &Self {
        if self.is_paused() {
            self.times_finished_this_tick = 0;
            if self.mode == TimerMode::Repeating {
                self.finished = false;
            }
            return self;
        }

        if self.mode != TimerMode::Repeating && self.is_finished() {
            self.times_finished_this_tick = 0;
            return self;
        }

        self.stopwatch.tick(delta);
        self.finished = self.elapsed() >= self.duration();

        if self.is_finished() {
            if self.mode == TimerMode::Repeating {
                self.times_finished_this_tick = self
                    .elapsed()
                    .as_nanos()
                    .checked_div(self.duration().as_nanos())
                    .map_or(u32::MAX, |x| x as u32);
                self.set_elapsed(
                    self.elapsed()
                        .as_nanos()
                        .checked_rem(self.duration().as_nanos())
                        .map_or(Duration::ZERO, |x| Duration::from_nanos(x as u64)),
                );
            } else {
                self.times_finished_this_tick = 1;
                self.set_elapsed(self.duration());
            }
        } else {
            self.times_finished_this_tick = 0;
        }

        self
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn tick(&mut self, delta: Duration) -> &Self {
        if self.is_paused() {
            self.times_finished_this_tick = 0;
            if self.mode == TimerMode::Repeating {
                self.finished = false;
            }
            return self;
        }

        if self.mode != TimerMode::Repeating && self.is_finished() {
            self.times_finished_this_tick = 0;
            return self;
        }

        self.stopwatch.tick(delta);
        self.finished = self.elapsed() >= self.duration();

        if self.is_finished() {
            if self.mode == TimerMode::Repeating {
                self.times_finished_this_tick = self
                    .elapsed()
                    .as_nanos()
                    .checked_div(self.duration().as_nanos())
                    .and_then(|x| u32::try_from(x).ok())
                    .unwrap_or(u32::MAX);
                self.set_elapsed(
                    self.elapsed()
                        .as_nanos()
                        .checked_rem(self.duration().as_nanos())
                        .map_or(Duration::ZERO, |x| Duration::from_nanos(x as u64)),
                );
            } else {
                self.times_finished_this_tick = 1;
                self.set_elapsed(self.duration());
            }
        } else {
            self.times_finished_this_tick = 0;
        }

        self
    }
```

### 🔹 函式: `Timer::remaining()`
- **變更前簽章 (Before)**: `fn Timer::remaining(&self)` (L461~L463)
- **變更後簽章 (After)**: `fn Timer::remaining(&self)` (L462~L464)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn remaining(&self) -> Duration {
        self.duration() - self.elapsed()
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn remaining(&self) -> Duration {
        self.duration().saturating_sub(self.elapsed())
    }
```


---

### 🔹 Commit #14: `7c82c4c2`
- **完整 Hash**: `7c82c4c24aef005eb8c8c026e06bd144fd35e4fe`
- **說明 (Ground Truth)**: Resolve pending render entities by main entity (#25816)
- **變更檔案數**: 1

#### 📄 檔案: `crates/bevy_render/src/camera.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:282, E:317, A:0) ➔ After(N:279, E:315, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 5, +Edges: 4, -Edges: 6, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `last_frame_view_pending_queues
                .iter()
                .filter_map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `(if self.must_wipe_specializations_for_view(view) {
            Either::Left(render_visible_mesh_entities.iter_visible())
        } else {
            Either::Right(
                render_visible_mesh_entities
                    .added_entities()
                    .iter()
                    .map(|(entity, main_entity)| (entity, main_entity))
                    .chain(self.changed_renderables.iter().filter_map(|main_entity| {
                        self.entity_pair_from_visible_main_entity(
                            render_visible_mesh_entities,
                            main_entity,
                        )
                    })),
            )
        })
        .chain(
            last_frame_view_pending_queues
                .iter()
                .filter_map(|(_, main_entity)| {
                    // Resolve pending entries against the current visible entities.
                    self.entity_pair_from_visible_main_entity(
                        render_visible_mesh_entities,
                        main_entity,
                    )
                }),
        )
        .filter (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `(if self.must_wipe_specializations_for_view(view) {
            Either::Left(render_visible_mesh_entities.iter_visible())
        } else {
            Either::Right(
                render_visible_mesh_entities
                    .added_entities()
                    .iter()
                    .map(|(entity, main_entity)| (entity, main_entity))
                    .chain(self.changed_renderables.iter().filter_map(|main_entity| {
                        self.entity_pair_from_visible_main_entity(
                            render_visible_mesh_entities,
                            main_entity,
                        )
                    })),
            )
        })
        .chain(
            last_frame_view_pending_queues
                .iter()
                .map(|(entity, main_entity)| (entity, main_entity)),
        )
        .filter (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `last_frame_view_pending_queues
                .iter()
                .map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `last_frame_view_pending_queues.iter().filter_map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `last_frame_view_pending_queues.iter (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `render_view_visible_mesh_entities.entity_pair_is_visible (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `DirtySpecializations::iter_to_specialize` ──[CALLS]──> `last_frame_view_pending_queues
                .iter()
                .filter_map (External/Unresolved)`
  • + [新增呼叫邊] `DirtySpecializations::iter_to_specialize` ──[CALLS]──> `last_frame_view_pending_queues
                .iter (External/Unresolved)`
  • + [新增呼叫邊] `DirtySpecializations::iter_to_queue` ──[CALLS]──> `(if self.must_wipe_specializations_for_view(view) {
            Either::Left(render_visible_mesh_entities.iter_visible())
        } else {
            Either::Right(
                render_visible_mesh_entities
                    .added_entities()
                    .iter()
                    .map(|(entity, main_entity)| (entity, main_entity))
                    .chain(self.changed_renderables.iter().filter_map(|main_entity| {
                        self.entity_pair_from_visible_main_entity(
                            render_visible_mesh_entities,
                            main_entity,
                        )
                    })),
            )
        })
        .chain(
            last_frame_view_pending_queues
                .iter()
                .filter_map(|(_, main_entity)| {
                    // Resolve pending entries against the current visible entities.
                    self.entity_pair_from_visible_main_entity(
                        render_visible_mesh_entities,
                        main_entity,
                    )
                }),
        )
        .filter (External/Unresolved)`
  • + [新增呼叫邊] `DirtySpecializations::iter_to_queue` ──[CALLS]──> `last_frame_view_pending_queues
                .iter()
                .filter_map (External/Unresolved)`
  • - [移除呼叫邊] `DirtySpecializations::iter_to_specialize` ──[CALLS]──> `last_frame_view_pending_queues.iter().filter_map (External/Unresolved)`
  • - [移除呼叫邊] `DirtySpecializations::iter_to_specialize` ──[CALLS]──> `last_frame_view_pending_queues.iter (External/Unresolved)`
  • - [移除呼叫邊] `DirtySpecializations::iter_to_specialize` ──[CALLS]──> `render_view_visible_mesh_entities.entity_pair_is_visible (External/Unresolved)`
  • - [移除呼叫邊] `DirtySpecializations::iter_to_specialize` ──[CALLS]──> `Some (External/Unresolved)`
  • _... 以及其餘 2 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `DirtySpecializations::iter_to_queue()`
- **變更前簽章 (Before)**: `fn DirtySpecializations::iter_to_queue(
        &'a self,
        view: RetainedViewEntity,
        render_visible_mesh_entities: &'a RenderVisibleEntitiesClass,
        last_frame_view_pending_queues: &'a HashSet<(Entity, MainEntity)>,
        mesh_instances_queued_this_iteration_scratch_space: &'a mut MainEntityHashSet,
    )` (L1065~L1102)
- **變更後簽章 (After)**: `fn DirtySpecializations::iter_to_queue(
        &'a self,
        view: RetainedViewEntity,
        render_visible_mesh_entities: &'a RenderVisibleEntitiesClass,
        last_frame_view_pending_queues: &'a HashSet<(Entity, MainEntity)>,
        mesh_instances_queued_this_iteration_scratch_space: &'a mut MainEntityHashSet,
    )` (L1067~L1110)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn iter_to_queue<'a>(
        &'a self,
        view: RetainedViewEntity,
        render_visible_mesh_entities: &'a RenderVisibleEntitiesClass,
        last_frame_view_pending_queues: &'a HashSet<(Entity, MainEntity)>,
        mesh_instances_queued_this_iteration_scratch_space: &'a mut MainEntityHashSet,
    ) -> impl Iterator<Item = (&'a Entity, &'a MainEntity)> {
        mesh_instances_queued_this_iteration_scratch_space.clear();

        // Use `mesh_instances_queued_this_iteration_scratch_space` to avoid
        // yielding the same mesh instance twice.
        // Yielding a mesh instance twice would result in binning it twice,
        // which is illegal.
        (if self.must_wipe_specializations_for_view(view) {
            Either::Left(render_visible_mesh_entities.iter_visible())
        } else {
            Either::Right(
                render_visible_mesh_entities
                    .added_entities()
                    .iter()
                    .map(|(entity, main_entity)| (entity, main_entity))
                    .chain(self.changed_renderables.iter().filter_map(|main_entity| {
                        self.entity_pair_from_visible_main_entity(
                            render_visible_mesh_entities,
                            main_entity,
                        )
                    })),
            )
        })
        .chain(
            last_frame_view_pending_queues
                .iter()
                .map(|(entity, main_entity)| (entity, main_entity)),
        )
        .filter(|(_, main_entity)| {
            mesh_instances_queued_this_iteration_scratch_space.insert(**main_entity)
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn iter_to_queue<'a>(
        &'a self,
        view: RetainedViewEntity,
        render_visible_mesh_entities: &'a RenderVisibleEntitiesClass,
        last_frame_view_pending_queues: &'a HashSet<(Entity, MainEntity)>,
        mesh_instances_queued_this_iteration_scratch_space: &'a mut MainEntityHashSet,
    ) -> impl Iterator<Item = (&'a Entity, &'a MainEntity)> {
        mesh_instances_queued_this_iteration_scratch_space.clear();

        // Use `mesh_instances_queued_this_iteration_scratch_space` to avoid
        // yielding the same mesh instance twice.
        // Yielding a mesh instance twice would result in binning it twice,
        // which is illegal.
        (if self.must_wipe_specializations_for_view(view) {
            Either::Left(render_visible_mesh_entities.iter_visible())
        } else {
            Either::Right(
                render_visible_mesh_entities
                    .added_entities()
                    .iter()
                    .map(|(entity, main_entity)| (entity, main_entity))
                    .chain(self.changed_renderables.iter().filter_map(|main_entity| {
                        self.entity_pair_from_visible_main_entity(
                            render_visible_mesh_entities,
                            main_entity,
                        )
                    })),
            )
        })
        .chain(
            last_frame_view_pending_queues
                .iter()
                .filter_map(|(_, main_entity)| {
                    // Resolve pending entries against the current visible entities.
                    self.entity_pair_from_visible_main_entity(
                        render_visible_mesh_entities,
                        main_entity,
                    )
                }),
        )
        .filter(|(_, main_entity)| {
            mesh_instances_queued_this_iteration_scratch_space.insert(**main_entity)
        })
    }
```

### 🔹 函式: `DirtySpecializations::iter_to_specialize()`
- **變更前簽章 (Before)**: `fn DirtySpecializations::iter_to_specialize(
        &'a self,
        view: RetainedViewEntity,
        render_view_visible_mesh_entities: &'a RenderVisibleEntitiesClass,
        last_frame_view_pending_queues: &'a HashSet<(Entity, MainEntity)>,
    )` (L985~L1016)
- **變更後簽章 (After)**: `fn DirtySpecializations::iter_to_specialize(
        &'a self,
        view: RetainedViewEntity,
        render_view_visible_mesh_entities: &'a RenderVisibleEntitiesClass,
        last_frame_view_pending_queues: &'a HashSet<(Entity, MainEntity)>,
    )` (L985~L1018)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn iter_to_specialize<'a>(
        &'a self,
        view: RetainedViewEntity,
        render_view_visible_mesh_entities: &'a RenderVisibleEntitiesClass,
        last_frame_view_pending_queues: &'a HashSet<(Entity, MainEntity)>,
    ) -> impl Iterator<Item = (&'a Entity, &'a MainEntity)> {
        (if self.must_wipe_specializations_for_view(view) {
            Either::Left(render_view_visible_mesh_entities.iter_visible())
        } else {
            Either::Right(
                render_view_visible_mesh_entities
                    .added_entities()
                    .iter()
                    .map(|(entity, main_entity)| (entity, main_entity))
                    .chain(self.changed_renderables.iter().filter_map(|main_entity| {
                        self.entity_pair_from_visible_main_entity(
                            render_view_visible_mesh_entities,
                            main_entity,
                        )
                    })),
            )
        })
        .chain(last_frame_view_pending_queues.iter().filter_map(
            |(entity, main_entity)| {
                if render_view_visible_mesh_entities.entity_pair_is_visible(*entity, *main_entity) {
                    Some((entity, main_entity))
                } else {
                    None
                }
            },
        ))
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn iter_to_specialize<'a>(
        &'a self,
        view: RetainedViewEntity,
        render_view_visible_mesh_entities: &'a RenderVisibleEntitiesClass,
        last_frame_view_pending_queues: &'a HashSet<(Entity, MainEntity)>,
    ) -> impl Iterator<Item = (&'a Entity, &'a MainEntity)> {
        (if self.must_wipe_specializations_for_view(view) {
            Either::Left(render_view_visible_mesh_entities.iter_visible())
        } else {
            Either::Right(
                render_view_visible_mesh_entities
                    .added_entities()
                    .iter()
                    .map(|(entity, main_entity)| (entity, main_entity))
                    .chain(self.changed_renderables.iter().filter_map(|main_entity| {
                        self.entity_pair_from_visible_main_entity(
                            render_view_visible_mesh_entities,
                            main_entity,
                        )
                    })),
            )
        })
        .chain(
            last_frame_view_pending_queues
                .iter()
                .filter_map(|(_, main_entity)| {
                    // Resolve pending entries against the current visible entities.
                    self.entity_pair_from_visible_main_entity(
                        render_view_visible_mesh_entities,
                        main_entity,
                    )
                }),
        )
    }
```


---

### 🔹 Commit #15: `31236b72`
- **完整 Hash**: `31236b7221cf36a70cae1445240c60002d31289f`
- **說明 (Ground Truth)**: Fix warning when loading the sprite_material.wesl shader (#26002)
- **變更檔案數**: 2

#### 📄 檔案: `crates/bevy_sprite_render/src/mesh2d/material.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:242, E:247, A:0) ➔ After(N:239, E:245, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 8, +Edges: 7, -Edges: 9, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `render_app
                .init_resource::<PendingMeshMaterial2dQueues>()
                .allow_ambiguous_resource::<PendingMeshMaterial2dQueues>()
                .add_systems (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `initialize_material2d_shaders::<M>.after (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_app
                .init_resource::<PendingMeshMaterial2dQueues>()
                .allow_ambiguous_resource::<PendingMeshMaterial2dQueues> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_app
                .init_resource::<PendingMeshMaterial2dQueues>()
                .allow_ambiguous_resource::<PendingMeshMaterial2dQueues>()
                .add_systems(
                    RenderStartup,
                    (
                        // mesh2d_bindings depends on runtime values so we need to load material2d
                        // shaders after it's already loaded
                        initialize_material2d_shaders::<M>.after(load_mesh2d_bindings),
                        add_material2d_bind_group_allocator::<M>,
                    ),
                )
                .add_systems (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_app
                .init_resource::<PendingMeshMaterial2dQueues> (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `initialize_material2d_shaders::<M> (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `render_app.world (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `render_app
                .insert_resource (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `render_app
                .insert_resource(Material2dShaders::<M>::with_shader_cache(shaders))
                .init_resource::<PendingMeshMaterial2dQueues>()
                .allow_ambiguous_resource::<PendingMeshMaterial2dQueues> (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `render_app
                .insert_resource(Material2dShaders::<M>::with_shader_cache(shaders))
                .init_resource::<PendingMeshMaterial2dQueues>()
                .allow_ambiguous_resource::<PendingMeshMaterial2dQueues>()
                .add_systems(RenderStartup, add_material2d_bind_group_allocator::<M>)
                .add_systems (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `render_app
                .insert_resource(Material2dShaders::<M>::with_shader_cache(shaders))
                .init_resource::<PendingMeshMaterial2dQueues>()
                .allow_ambiguous_resource::<PendingMeshMaterial2dQueues>()
                .add_systems (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `render_world.resource::<AssetServer> (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `render_app
                .insert_resource(Material2dShaders::<M>::with_shader_cache(shaders))
                .init_resource::<PendingMeshMaterial2dQueues> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Material2dPlugin::build` ──[CALLS]──> `render_app
                .init_resource::<PendingMeshMaterial2dQueues>()
                .allow_ambiguous_resource::<PendingMeshMaterial2dQueues>()
                .add_systems(
                    RenderStartup,
                    (
                        // mesh2d_bindings depends on runtime values so we need to load material2d
                        // shaders after it's already loaded
                        initialize_material2d_shaders::<M>.after(load_mesh2d_bindings),
                        add_material2d_bind_group_allocator::<M>,
                    ),
                )
                .add_systems (External/Unresolved)`
  • + [新增呼叫邊] `Material2dPlugin::build` ──[CALLS]──> `render_app
                .init_resource::<PendingMeshMaterial2dQueues>()
                .allow_ambiguous_resource::<PendingMeshMaterial2dQueues>()
                .add_systems (External/Unresolved)`
  • _... 以及其餘 14 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Material2dPlugin::build()`
- **變更前簽章 (Before)**: `fn Material2dPlugin::build(&self, app: &mut App)` (L338~L372)
- **變更後簽章 (After)**: `fn Material2dPlugin::build(&self, app: &mut App)` (L338~L378)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn build(&self, app: &mut App) {
        app.init_asset::<M>()
            .init_resource::<EntitiesNeedingSpecialization<M>>()
            .register_type::<MeshMaterial2d<M>>()
            .add_plugins(ErasedRenderAssetPlugin::<MeshMaterial2d<M>>::default())
            .add_systems(
                PostUpdate,
                (
                    mark_2d_meshes_as_changed_if_their_materials_changed::<M>.ambiguous_with_all(),
                    check_entities_needing_specialization::<M>
                        .after(AssetEventSystems)
                        .ambiguous_with_all(),
                )
                    .chain(),
            );

        if let Some(render_app) = app.get_sub_app_mut(RenderApp) {
            let shaders = initialize_material2d_shaders::<M>(render_app.world());
            render_app
                .insert_resource(Material2dShaders::<M>::with_shader_cache(shaders))
                .init_resource::<PendingMeshMaterial2dQueues>()
                .allow_ambiguous_resource::<PendingMeshMaterial2dQueues>()
                .add_systems(RenderStartup, add_material2d_bind_group_allocator::<M>)
                .add_systems(
                    ExtractSchedule,
                    (
                        extract_entities_needs_specialization::<M>
                            .in_set(DirtySpecializationSystems::CheckForChanges),
                        extract_entities_that_need_specializations_removed::<M>
                            .in_set(DirtySpecializationSystems::CheckForRemovals),
                        extract_mesh_materials_2d::<M>.before(extract_2d_meshes),
                    ),
                );
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn build(&self, app: &mut App) {
        app.init_asset::<M>()
            .init_resource::<EntitiesNeedingSpecialization<M>>()
            .register_type::<MeshMaterial2d<M>>()
            .add_plugins(ErasedRenderAssetPlugin::<MeshMaterial2d<M>>::default())
            .add_systems(
                PostUpdate,
                (
                    mark_2d_meshes_as_changed_if_their_materials_changed::<M>.ambiguous_with_all(),
                    check_entities_needing_specialization::<M>
                        .after(AssetEventSystems)
                        .ambiguous_with_all(),
                )
                    .chain(),
            );

        if let Some(render_app) = app.get_sub_app_mut(RenderApp) {
            render_app
                .init_resource::<PendingMeshMaterial2dQueues>()
                .allow_ambiguous_resource::<PendingMeshMaterial2dQueues>()
                .add_systems(
                    RenderStartup,
                    (
                        // mesh2d_bindings depends on runtime values so we need to load material2d
                        // shaders after it's already loaded
                        initialize_material2d_shaders::<M>.after(load_mesh2d_bindings),
                        add_material2d_bind_group_allocator::<M>,
                    ),
                )
                .add_systems(
                    ExtractSchedule,
                    (
                        extract_entities_needs_specialization::<M>
                            .in_set(DirtySpecializationSystems::CheckForChanges),
                        extract_entities_that_need_specializations_removed::<M>
                            .in_set(DirtySpecializationSystems::CheckForRemovals),
                        extract_mesh_materials_2d::<M>.before(extract_2d_meshes),
                    ),
                );
        }
    }
```

### 🔹 函式: `initialize_material2d_shaders()`
- **變更前簽章 (Before)**: `fn initialize_material2d_shaders(
    render_world: &World,
)` (L1428~L1452)
- **變更後簽章 (After)**: `fn initialize_material2d_shaders(mut commands: Commands, asset_server: Res<AssetServer>)` (L1434~L1455)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn initialize_material2d_shaders<M>(
    render_world: &World,
) -> SmallVec<[(InternedShaderLabel, Handle<Shader>); 6]>
where
    M: Material2d,
{
    let asset_server = render_world.resource::<AssetServer>();
    let mut shaders = SmallVec::new();

    let mut add_shader = |label: InternedShaderLabel, shader_ref: ShaderRef| {
        let maybe_shader = match shader_ref {
            ShaderRef::Default => None,
            ShaderRef::Handle(handle) => Some(handle),
            ShaderRef::Path(path) => Some(asset_server.load(path)),
        };
        if let Some(shader) = maybe_shader {
            shaders.push((label, shader));
        }
    };

    add_shader(Material2dVertexShader.intern(), M::vertex_shader());
    add_shader(Material2dFragmentShader.intern(), M::fragment_shader());

    shaders
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn initialize_material2d_shaders<M>(mut commands: Commands, asset_server: Res<AssetServer>)
where
    M: Material2d,
{
    let mut shaders = SmallVec::new();

    let mut add_shader = |label: InternedShaderLabel, shader_ref: ShaderRef| {
        let maybe_shader = match shader_ref {
            ShaderRef::Default => None,
            ShaderRef::Handle(handle) => Some(handle),
            ShaderRef::Path(path) => Some(asset_server.load(path)),
        };
        if let Some(shader) = maybe_shader {
            shaders.push((label, shader));
        }
    };

    add_shader(Material2dVertexShader.intern(), M::vertex_shader());
    add_shader(Material2dFragmentShader.intern(), M::fragment_shader());

    commands.insert_resource(Material2dShaders::<M>::with_shader_cache(shaders));
}
```


#### 📄 檔案: `crates/bevy_sprite_render/src/mesh2d/mesh.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:229, E:229, A:0) ➔ After(N:229, E:229, A:0)
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

### 🔹 函式: `load_mesh2d_bindings()`
- **變更前簽章 (Before)**: `fn load_mesh2d_bindings(render_device: Res<RenderDevice>, asset_server: Res<AssetServer>)` (L185~L212)
- **變更後簽章 (After)**: `fn load_mesh2d_bindings(
    render_device: Res<RenderDevice>,
    asset_server: Res<AssetServer>,
)` (L185~L215)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn load_mesh2d_bindings(render_device: Res<RenderDevice>, asset_server: Res<AssetServer>) {
    let mut mesh_bindings_shader_defs = Vec::with_capacity(1);

    if let Some(per_object_buffer_batch_size) =
        GpuArrayBuffer::<Mesh2dUniform>::batch_size(&render_device.limits())
    {
        mesh_bindings_shader_defs.push(ShaderDefVal::UInt(
            "PER_OBJECT_BUFFER_BATCH_SIZE".into(),
            per_object_buffer_batch_size,
        ));
    }

    if bevy_render::storage_buffers_are_unsupported(&render_device.limits()) {
        mesh_bindings_shader_defs.push("METADATA_USE_UNIFORM_BUFFERS".into());
    }

    // Load the mesh_bindings shader module here as it depends on runtime information about
    // whether storage buffers are supported, or the maximum uniform buffer binding size.
    let handle: Handle<Shader> =
        load_embedded_asset!(asset_server.as_ref(), "bindings.wesl", move |settings| {
            *settings = ShaderSettings {
                shader_defs: mesh_bindings_shader_defs.clone(),
            };
        });
    // Forget the handle so we don't have to store it anywhere, and we keep the embedded asset
    // loaded. Note: This is what happens in `load_shader_library` internally.
    mem::forget(handle);
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn load_mesh2d_bindings(
    render_device: Res<RenderDevice>,
    asset_server: Res<AssetServer>,
) {
    let mut mesh_bindings_shader_defs = Vec::with_capacity(1);

    if let Some(per_object_buffer_batch_size) =
        GpuArrayBuffer::<Mesh2dUniform>::batch_size(&render_device.limits())
    {
        mesh_bindings_shader_defs.push(ShaderDefVal::UInt(
            "PER_OBJECT_BUFFER_BATCH_SIZE".into(),
            per_object_buffer_batch_size,
        ));
    }

    if bevy_render::storage_buffers_are_unsupported(&render_device.limits()) {
        mesh_bindings_shader_defs.push("METADATA_USE_UNIFORM_BUFFERS".into());
    }

    // Load the mesh_bindings shader module here as it depends on runtime information about
    // whether storage buffers are supported, or the maximum uniform buffer binding size.
    let handle: Handle<Shader> =
        load_embedded_asset!(asset_server.as_ref(), "bindings.wesl", move |settings| {
            *settings = ShaderSettings {
                shader_defs: mesh_bindings_shader_defs.clone(),
            };
        });
    // Forget the handle so we don't have to store it anywhere, and we keep the embedded asset
    // loaded. Note: This is what happens in `load_shader_library` internally.
    mem::forget(handle);
}
```


---

### 🔹 Commit #16: `85cf6e4d`
- **完整 Hash**: `85cf6e4d1db3270269dc1c4589782259cbbe0d5e`
- **說明 (Ground Truth)**: Fix 9 slicing (#26011)
- **變更檔案數**: 2

#### 📄 檔案: `crates/bevy_sprite/src/sprite.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:65, E:115, A:0) ➔ After(N:68, E:117, A:0)
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
  • + [新增節點] `(slicer.border.min_inset + slicer.border.max_inset)
                .cmpge(image_size)
                .any (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `(slicer.border.min_inset + slicer.border.max_inset)
                .cmpge (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `SpriteImageMode::slice_border_out_of_bounds` (FUNCTION_DEF)
  • + [新增呼叫邊] `SpriteImageMode::slice_border_out_of_bounds` ──[CALLS]──> `(slicer.border.min_inset + slicer.border.max_inset)
                .cmpge(image_size)
                .any (External/Unresolved)`
  • + [新增呼叫邊] `SpriteImageMode::slice_border_out_of_bounds` ──[CALLS]──> `(slicer.border.min_inset + slicer.border.max_inset)
                .cmpge (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `crates/bevy_sprite_render/src/sprite_mesh/sprite_mesh_material.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:37, E:33, A:0) ➔ After(N:41, E:37, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 1, +Edges: 5, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `coef
                        .min_element (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.image_mode.slice_border_out_of_bounds (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `tracing::error! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `coef
                        .min_element()
                        .min(slicer.max_corner_scale)
                        .max (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `coef
                        .min_element()
                        .min (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `slicer.max_corner_scale.clamp (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `SpriteMeshMaterial::as_bind_group_shader_type` ──[CALLS]──> `self.image_mode.slice_border_out_of_bounds (External/Unresolved)`
  • + [新增呼叫邊] `SpriteMeshMaterial::as_bind_group_shader_type` ──[CALLS]──> `tracing::error! (Macro)`
  • + [新增呼叫邊] `SpriteMeshMaterial::as_bind_group_shader_type` ──[CALLS]──> `coef
                        .min_element()
                        .min(slicer.max_corner_scale)
                        .max (External/Unresolved)`
  • + [新增呼叫邊] `SpriteMeshMaterial::as_bind_group_shader_type` ──[CALLS]──> `coef
                        .min_element()
                        .min (External/Unresolved)`
  • + [新增呼叫邊] `SpriteMeshMaterial::as_bind_group_shader_type` ──[CALLS]──> `coef
                        .min_element (External/Unresolved)`
  • - [移除呼叫邊] `SpriteMeshMaterial::as_bind_group_shader_type` ──[CALLS]──> `slicer.max_corner_scale.clamp (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SpriteMeshMaterial::as_bind_group_shader_type()`
- **變更前簽章 (Before)**: `fn SpriteMeshMaterial::as_bind_group_shader_type(
        &self,
        images: &RenderAssets<bevy_render::texture::GpuImage>,
    )` (L99~L309)
- **變更後簽章 (After)**: `fn SpriteMeshMaterial::as_bind_group_shader_type(
        &self,
        images: &RenderAssets<bevy_render::texture::GpuImage>,
    )` (L99~L312)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn as_bind_group_shader_type(
        &self,
        images: &RenderAssets<bevy_render::texture::GpuImage>,
    ) -> SpriteMeshMaterialUniform {
        let Some(image) = images.get(self.image.id()) else {
            return SpriteMeshMaterialUniform::default();
        };

        let mut flags = SpriteMeshMaterialFlags::NONE;
        let mut alpha_cutoff = 0.5;
        match self.alpha_mode {
            AlphaMode2d::Opaque => flags |= SpriteMeshMaterialFlags::ALPHA_MODE_OPAQUE,
            AlphaMode2d::Mask(c) => {
                alpha_cutoff = c;
                flags |= SpriteMeshMaterialFlags::ALPHA_MODE_MASK;
            }
            AlphaMode2d::Blend => flags |= SpriteMeshMaterialFlags::ALPHA_MODE_BLEND,
        };

        if self.flip_x {
            flags |= SpriteMeshMaterialFlags::FLIP_X;
        }
        if self.flip_y {
            flags |= SpriteMeshMaterialFlags::FLIP_Y;
        }

        let mut image_size = image.size_2d().as_vec2();

        let mut quad_size = image_size;
        let mut quad_offset = Vec2::ZERO;
        let mut uv_transform = Affine2::default();

        if let Some(texture_atlas_layout) = &self.texture_atlas_layout {
            let index = self
                .texture_atlas_index
                .clamp(0, texture_atlas_layout.textures.len() - 1);

            let rect = texture_atlas_layout.textures[index].as_rect();

            let ratio = rect.size() / image_size;

            uv_transform *= Affine2::from_scale(ratio);
            uv_transform *= Affine2::from_translation(vec2(
                rect.min.x / rect.size().x,
                rect.min.y / rect.size().y,
            ));

            quad_size = rect.size();
            image_size = rect.size();
        }

        // rect selects a slice of the image to render, map the uv and change the quad scale to match the rect
        if let Some(rect) = self.rect {
            let ratio = rect.size() / image_size;

            uv_transform *= Affine2::from_scale(ratio);
            uv_transform *= Affine2::from_translation(vec2(
                rect.min.x / rect.size().x,
                rect.min.y / rect.size().y,
            ));

            quad_size = rect.size();
            image_size = rect.size();
        }

        let mut tile_stretch_value = Vec2::ZERO;

        let mut scale = Vec2::ZERO;
        let mut min_inset = Vec2::ZERO;
        let mut max_inset = Vec2::ZERO;
        let mut side_stretch_value = Vec2::ZERO;
        let mut center_stretch_value = Vec2::ZERO;

        if let Some(custom_size) = self.custom_size {
            match &self.image_mode {
                SpriteImageMode::Auto => {
                    quad_size = custom_size;
                }
                SpriteImageMode::Scale(scaling_mode) => {
                    let quad_ratio = quad_size.x / quad_size.y;
                    let custom_ratio = custom_size.x / custom_size.y;

                    let fill_size = || {
                        if quad_ratio > custom_ratio {
                            vec2(custom_size.y * quad_ratio, custom_size.y)
                        } else {
                            vec2(custom_size.x, custom_size.x / quad_ratio)
                        }
                    };

                    let fit_size = || {
                        if quad_ratio > custom_ratio {
                            vec2(custom_size.x, custom_size.x / quad_ratio)
                        } else {
                            vec2(custom_size.y * quad_ratio, custom_size.y)
                        }
                    };

                    match scaling_mode {
                        // Filling requires scaling the texture and cutting out the 'overflow'
                        // which is why we need to manipulate the UV.
                        SpriteScalingMode::FillCenter => {
                            let fill_size = fill_size();
                            uv_transform *= Affine2::from_scale(custom_size / fill_size);
                            uv_transform *= Affine2::from_translation(
                                (fill_size - custom_size) * 0.5 / custom_size,
                            );
                            quad_size = custom_size;
                        }
                        SpriteScalingMode::FillStart => {
                            let fill_size = fill_size();
                            uv_transform *= Affine2::from_scale(custom_size / fill_size);
                            quad_size = custom_size;
                        }
                        SpriteScalingMode::FillEnd => {
                            let fill_size = fill_size();
                            uv_transform *= Affine2::from_scale(custom_size / fill_size);
                            uv_transform *=
                                Affine2::from_translation((fill_size - custom_size) / custom_size);
                            quad_size = custom_size;
                        }

                        // Fitting is easier since the whole texture will still be visible,
                        // so it's enough to just translate the quad and keep the UV as is.
                        SpriteScalingMode::FitCenter => {
                            let fit_size = fit_size();
                            quad_size = fit_size;
                        }
                        SpriteScalingMode::FitStart => {
                            let fit_size = fit_size();
                            quad_offset += (custom_size - fit_size) * vec2(-0.5, 0.5);
                            quad_size = fit_size;
                        }
                        SpriteScalingMode::FitEnd => {
                            let fit_size = fit_size();
                            quad_offset += (custom_size - fit_size) * vec2(0.5, -0.5);
                            quad_size = fit_size;
                        }
                    }
                }
                SpriteImageMode::Tiled {
                    tile_x,
                    tile_y,
                    stretch_value,
                } => {
                    if *tile_x {
                        flags |= SpriteMeshMaterialFlags::TILE_X;
                    }
                    if *tile_y {
                        flags |= SpriteMeshMaterialFlags::TILE_Y;
                    }

                    // This is the [0-1] x and y of where the UV should start repeating.
                    // E.g. if the stretch_value x is 0.2 and the UV x is 0.5, it will be mapped to 0.1 (0.5 - 0.2 * 2)
                    // and then be stretched over [0, 0.2] by translating it to (0.1 / 0.2) = 0.5,
                    // so it corresponds to the center of the texture.
                    tile_stretch_value = (image_size * stretch_value) / custom_size;
                    quad_size = custom_size;
                }
                SpriteImageMode::Sliced(slicer) => {
                    let quad_ratio = quad_size.x / quad_size.y;
                    let custom_ratio = custom_size.x / custom_size.y;

                    if quad_ratio > custom_ratio {
                        scale = vec2(1.0, quad_ratio / custom_ratio);
                    } else {
                        scale = vec2(custom_ratio / quad_ratio, 1.0);
                    }

                    min_inset = slicer.border.min_inset / quad_size;
                    max_inset = slicer.border.max_inset / quad_size;

                    let corner_scale = slicer.max_corner_scale.clamp(f32::EPSILON, 1.0);
                    scale /= corner_scale;

                    if let SliceScaleMode::Tile { stretch_value } = slicer.sides_scale_mode {
                        side_stretch_value = stretch_value
                            * (image_size * (1.0 - max_inset - min_inset))
                            / (custom_size * (1.0 - max_inset / scale - min_inset / scale));
                    }

                    if let SliceScaleMode::Tile { stretch_value } = slicer.center_scale_mode {
                        center_stretch_value = stretch_value
                            * (image_size * (1.0 - max_inset - min_inset))
                            / (custom_size * (1.0 - max_inset / scale - min_inset / scale));
                    }

                    quad_size = custom_size;
                }
            }
        }

        quad_offset -= quad_size * self.anchor;

        SpriteMeshMaterialUniform {
            color: self.color.to_linear().to_vec4(),
            flags: flags.bits(),
            alpha_cutoff,
            vertex_scale: quad_size,
            vertex_offset: quad_offset,
            uv_transform: uv_transform.into(),

            tile_stretch_value,

            scale,
            min_inset,
            max_inset,
            side_stretch_value,
            center_stretch_value,
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn as_bind_group_shader_type(
        &self,
        images: &RenderAssets<bevy_render::texture::GpuImage>,
    ) -> SpriteMeshMaterialUniform {
        let Some(image) = images.get(self.image.id()) else {
            return SpriteMeshMaterialUniform::default();
        };

        let mut flags = SpriteMeshMaterialFlags::NONE;
        let mut alpha_cutoff = 0.5;
        match self.alpha_mode {
            AlphaMode2d::Opaque => flags |= SpriteMeshMaterialFlags::ALPHA_MODE_OPAQUE,
            AlphaMode2d::Mask(c) => {
                alpha_cutoff = c;
                flags |= SpriteMeshMaterialFlags::ALPHA_MODE_MASK;
            }
            AlphaMode2d::Blend => flags |= SpriteMeshMaterialFlags::ALPHA_MODE_BLEND,
        };

        if self.flip_x {
            flags |= SpriteMeshMaterialFlags::FLIP_X;
        }
        if self.flip_y {
            flags |= SpriteMeshMaterialFlags::FLIP_Y;
        }

        let mut image_size = image.size_2d().as_vec2();

        let mut quad_size = image_size;
        let mut quad_offset = Vec2::ZERO;
        let mut uv_transform = Affine2::default();

        if let Some(texture_atlas_layout) = &self.texture_atlas_layout {
            let index = self
                .texture_atlas_index
                .clamp(0, texture_atlas_layout.textures.len() - 1);

            let rect = texture_atlas_layout.textures[index].as_rect();

            let ratio = rect.size() / image_size;

            uv_transform *= Affine2::from_scale(ratio);
            uv_transform *= Affine2::from_translation(vec2(
                rect.min.x / rect.size().x,
                rect.min.y / rect.size().y,
            ));

            quad_size = rect.size();
            image_size = rect.size();
        }

        // rect selects a slice of the image to render, map the uv and change the quad scale to match the rect
        if let Some(rect) = self.rect {
            let ratio = rect.size() / image_size;

            uv_transform *= Affine2::from_scale(ratio);
            uv_transform *= Affine2::from_translation(vec2(
                rect.min.x / rect.size().x,
                rect.min.y / rect.size().y,
            ));

            quad_size = rect.size();
            image_size = rect.size();
        }

        let mut tile_stretch_value = Vec2::ZERO;

        let mut scale = Vec2::ZERO;
        let mut min_inset = Vec2::ZERO;
        let mut max_inset = Vec2::ZERO;
        let mut side_stretch_value = Vec2::ZERO;
        let mut center_stretch_value = Vec2::ZERO;

        if let Some(custom_size) = self.custom_size {
            match &self.image_mode {
                SpriteImageMode::Auto => {
                    quad_size = custom_size;
                }
                SpriteImageMode::Scale(scaling_mode) => {
                    let quad_ratio = quad_size.x / quad_size.y;
                    let custom_ratio = custom_size.x / custom_size.y;

                    let fill_size = || {
                        if quad_ratio > custom_ratio {
                            vec2(custom_size.y * quad_ratio, custom_size.y)
                        } else {
                            vec2(custom_size.x, custom_size.x / quad_ratio)
                        }
                    };

                    let fit_size = || {
                        if quad_ratio > custom_ratio {
                            vec2(custom_size.x, custom_size.x / quad_ratio)
                        } else {
                            vec2(custom_size.y * quad_ratio, custom_size.y)
                        }
                    };

                    match scaling_mode {
                        // Filling requires scaling the texture and cutting out the 'overflow'
                        // which is why we need to manipulate the UV.
                        SpriteScalingMode::FillCenter => {
                            let fill_size = fill_size();
                            uv_transform *= Affine2::from_scale(custom_size / fill_size);
                            uv_transform *= Affine2::from_translation(
                                (fill_size - custom_size) * 0.5 / custom_size,
                            );
                            quad_size = custom_size;
                        }
                        SpriteScalingMode::FillStart => {
                            let fill_size = fill_size();
                            uv_transform *= Affine2::from_scale(custom_size / fill_size);
                            quad_size = custom_size;
                        }
                        SpriteScalingMode::FillEnd => {
                            let fill_size = fill_size();
                            uv_transform *= Affine2::from_scale(custom_size / fill_size);
                            uv_transform *=
                                Affine2::from_translation((fill_size - custom_size) / custom_size);
                            quad_size = custom_size;
                        }

                        // Fitting is easier since the whole texture will still be visible,
                        // so it's enough to just translate the quad and keep the UV as is.
                        SpriteScalingMode::FitCenter => {
                            let fit_size = fit_size();
                            quad_size = fit_size;
                        }
                        SpriteScalingMode::FitStart => {
                            let fit_size = fit_size();
                            quad_offset += (custom_size - fit_size) * vec2(-0.5, 0.5);
                            quad_size = fit_size;
                        }
                        SpriteScalingMode::FitEnd => {
                            let fit_size = fit_size();
                            quad_offset += (custom_size - fit_size) * vec2(0.5, -0.5);
                            quad_size = fit_size;
                        }
                    }
                }
                SpriteImageMode::Tiled {
                    tile_x,
                    tile_y,
                    stretch_value,
                } => {
                    if *tile_x {
                        flags |= SpriteMeshMaterialFlags::TILE_X;
                    }
                    if *tile_y {
                        flags |= SpriteMeshMaterialFlags::TILE_Y;
                    }

                    // This is the [0-1] x and y of where the UV should start repeating.
                    // E.g. if the stretch_value x is 0.2 and the UV x is 0.5, it will be mapped to 0.1 (0.5 - 0.2 * 2)
                    // and then be stretched over [0, 0.2] by translating it to (0.1 / 0.2) = 0.5,
                    // so it corresponds to the center of the texture.
                    tile_stretch_value = (image_size * stretch_value) / custom_size;
                    quad_size = custom_size;
                }
                SpriteImageMode::Sliced(_)
                    if self.image_mode.slice_border_out_of_bounds(quad_size) =>
                {
                    tracing::error!(
                        "TextureSlicer::border has out of bounds values. No slicing will be applied."
                    );
                    quad_size = custom_size;
                }
                SpriteImageMode::Sliced(slicer) => {
                    min_inset = slicer.border.min_inset / quad_size;
                    max_inset = slicer.border.max_inset / quad_size;

                    let coef = custom_size / quad_size;
                    let corner_scale = coef
                        .min_element()
                        .min(slicer.max_corner_scale)
                        .max(f32::EPSILON);
                    scale = coef / corner_scale;

                    if let SliceScaleMode::Tile { stretch_value } = slicer.sides_scale_mode {
                        side_stretch_value = stretch_value
                            * (image_size * (1.0 - max_inset - min_inset))
                            / (custom_size * (1.0 - max_inset / scale - min_inset / scale));
                    }

                    if let SliceScaleMode::Tile { stretch_value } = slicer.center_scale_mode {
                        center_stretch_value = stretch_value
                            * (image_size * (1.0 - max_inset - min_inset))
                            / (custom_size * (1.0 - max_inset / scale - min_inset / scale));
                    }

                    quad_size = custom_size;
                }
            }
        }

        quad_offset -= quad_size * self.anchor;

        SpriteMeshMaterialUniform {
            color: self.color.to_linear().to_vec4(),
            flags: flags.bits(),
            alpha_cutoff,
            vertex_scale: quad_size,
            vertex_offset: quad_offset,
            uv_transform: uv_transform.into(),

            tile_stretch_value,

            scale,
            min_inset,
            max_inset,
            side_stretch_value,
            center_stretch_value,
        }
    }
```


---

### 🔹 Commit #17: `a31a24fa`
- **完整 Hash**: `a31a24fabd96df017734b386d1634f55c646aaf9`
- **說明 (Ground Truth)**: Add a tracing span around apply_deferred in the schedule executors (#25908)
- **變更檔案數**: 2

#### 📄 檔案: `crates/bevy_ecs/src/schedule/executor/multi_threaded.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:189, E:230, A:0) ➔ After(N:190, E:232, A:0)
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
  • + [新增節點] `info_span!("apply_deferred").entered (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `apply_deferred` ──[CALLS]──> `info_span!("apply_deferred").entered (External/Unresolved)`
  • + [新增呼叫邊] `apply_deferred` ──[CALLS]──> `info_span! (Macro)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `apply_deferred()`
- **變更前簽章 (Before)**: `fn apply_deferred(
    unapplied_systems: &FixedBitSet,
    systems: &[SyncUnsafeCell<SystemWithAccess>],
    world: &mut World,
    error_handler: ErrorHandler,
)` (L764~L784)
- **變更後簽章 (After)**: `fn apply_deferred(
    unapplied_systems: &FixedBitSet,
    systems: &[SyncUnsafeCell<SystemWithAccess>],
    world: &mut World,
    error_handler: ErrorHandler,
)` (L764~L787)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn apply_deferred(
    unapplied_systems: &FixedBitSet,
    systems: &[SyncUnsafeCell<SystemWithAccess>],
    world: &mut World,
    error_handler: ErrorHandler,
) -> Result<(), Box<dyn Any + Send>> {
    for system_index in unapplied_systems.ones() {
        // SAFETY: none of these systems are running, no other references exist
        let system = &mut unsafe { &mut *systems[system_index].get() }.system;
        handle_errors(
            |system| {
                system.apply_deferred(world);
                Ok(())
            },
            system,
            error_handler,
            "Encountered a panic while applying system buffers",
        )?;
    }
    Ok(())
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn apply_deferred(
    unapplied_systems: &FixedBitSet,
    systems: &[SyncUnsafeCell<SystemWithAccess>],
    world: &mut World,
    error_handler: ErrorHandler,
) -> Result<(), Box<dyn Any + Send>> {
    #[cfg(feature = "trace")]
    let _span = info_span!("apply_deferred").entered();

    for system_index in unapplied_systems.ones() {
        // SAFETY: none of these systems are running, no other references exist
        let system = &mut unsafe { &mut *systems[system_index].get() }.system;
        handle_errors(
            |system| {
                system.apply_deferred(world);
                Ok(())
            },
            system,
            error_handler,
            "Encountered a panic while applying system buffers",
        )?;
    }
    Ok(())
}
```


#### 📄 檔案: `crates/bevy_ecs/src/schedule/executor/single_threaded.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:56, E:70, A:0) ➔ After(N:57, E:72, A:0)
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
  • + [新增節點] `info_span!("apply_deferred").entered (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `SingleThreadedExecutor::apply_deferred` ──[CALLS]──> `info_span!("apply_deferred").entered (External/Unresolved)`
  • + [新增呼叫邊] `SingleThreadedExecutor::apply_deferred` ──[CALLS]──> `info_span! (Macro)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `SingleThreadedExecutor::apply_deferred()`
- **變更前簽章 (Before)**: `fn SingleThreadedExecutor::apply_deferred(
        &mut self,
        schedule: &mut SystemSchedule,
        world: &mut World,
        error_handler: ErrorHandler,
    )` (L190~L216)
- **變更後簽章 (After)**: `fn SingleThreadedExecutor::apply_deferred(
        &mut self,
        schedule: &mut SystemSchedule,
        world: &mut World,
        error_handler: ErrorHandler,
    )` (L190~L219)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn apply_deferred(
        &mut self,
        schedule: &mut SystemSchedule,
        world: &mut World,
        error_handler: ErrorHandler,
    ) {
        for system_index in self.unapplied_systems.ones() {
            let system = &mut schedule.systems[system_index].system;
            #[cfg(not(feature = "std"))]
            {
                system.apply_deferred(world);
                let _ = error_handler;
            }

            #[cfg(feature = "std")]
            {
                handle_unwind(
                    |system| system.apply_deferred(world),
                    system,
                    error_handler,
                    "Encountered a panic while applying system buffers",
                );
            }
        }

        self.unapplied_systems.clear();
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn apply_deferred(
        &mut self,
        schedule: &mut SystemSchedule,
        world: &mut World,
        error_handler: ErrorHandler,
    ) {
        #[cfg(feature = "trace")]
        let _span = info_span!("apply_deferred").entered();

        for system_index in self.unapplied_systems.ones() {
            let system = &mut schedule.systems[system_index].system;
            #[cfg(not(feature = "std"))]
            {
                system.apply_deferred(world);
                let _ = error_handler;
            }

            #[cfg(feature = "std")]
            {
                handle_unwind(
                    |system| system.apply_deferred(world),
                    system,
                    error_handler,
                    "Encountered a panic while applying system buffers",
                );
            }
        }

        self.unapplied_systems.clear();
    }
```


---

### 🔹 Commit #18: `157e1ce6`
- **完整 Hash**: `157e1ce6bc66fadca9f57260c18a16d743c11ed5`
- **說明 (Ground Truth)**: Fix `EntityEquivalentIndexSet` unsoundness (#25940)
- **變更檔案數**: 2

#### 📄 檔案: `crates/bevy_ecs/src/entity/index_set.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:137, E:164, A:0) ➔ After(N:180, E:208, A:0)
- **差分統計**: +Nodes: 45, -Nodes: 2, +Edges: 45, -Edges: 1, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `EntityEquivalentIndexSet::sort_by_cached_key` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::sort_by` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::clear` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::pop_if` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::sort_unstable_by` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::reserve` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::swap_take` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::insert_sorted` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::shift_remove_full` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::swap_remove_index` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::try_reserve_exact` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::try_reserve` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::shift_remove` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::pop` (FUNCTION_DEF)
  • + [新增節點] `EntityEquivalentIndexSet::insert_before` (FUNCTION_DEF)
  • _... 以及其餘 78 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `crates/bevy_ecs/src/relationship/relationship_source_collection.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:143, E:220, A:0) ➔ After(N:142, E:216, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 1, -Edges: 5, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `self.deref_mut().shift_remove (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `EntityIndexSet::remove` ──[CALLS]──> `self.shift_remove (External/Unresolved)`
  • - [移除呼叫邊] `EntityIndexSet::reserve` ──[CALLS]──> `self.deref_mut (External/Unresolved)`
  • - [移除呼叫邊] `EntityIndexSet::remove` ──[CALLS]──> `self.deref_mut().shift_remove (External/Unresolved)`
  • - [移除呼叫邊] `EntityIndexSet::remove` ──[CALLS]──> `self.deref_mut (External/Unresolved)`
  • - [移除呼叫邊] `EntityIndexSet::clear` ──[CALLS]──> `self.deref_mut (External/Unresolved)`
  • - [移除呼叫邊] `EntityIndexSet::shrink_to_fit` ──[CALLS]──> `self.deref_mut (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `EntityIndexSet::shrink_to_fit()`
- **變更前簽章 (Before)**: `fn EntityIndexSet::shrink_to_fit(&mut self)` (L530~L532)
- **變更後簽章 (After)**: `fn EntityIndexSet::shrink_to_fit(&mut self)` (L530~L532)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn shrink_to_fit(&mut self) {
        self.deref_mut().shrink_to_fit();
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn shrink_to_fit(&mut self) {
        self.shrink_to_fit();
    }
```

### 🔹 函式: `EntityIndexSet::reserve()`
- **變更前簽章 (Before)**: `fn EntityIndexSet::reserve(&mut self, additional: usize)` (L502~L504)
- **變更後簽章 (After)**: `fn EntityIndexSet::reserve(&mut self, additional: usize)` (L502~L504)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn reserve(&mut self, additional: usize) {
        self.deref_mut().reserve(additional);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn reserve(&mut self, additional: usize) {
        self.reserve(additional);
    }
```

### 🔹 函式: `EntityIndexSet::clear()`
- **變更前簽章 (Before)**: `fn EntityIndexSet::clear(&mut self)` (L526~L528)
- **變更後簽章 (After)**: `fn EntityIndexSet::clear(&mut self)` (L526~L528)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn clear(&mut self) {
        self.deref_mut().clear();
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn clear(&mut self) {
        self.clear();
    }
```

### 🔹 函式: `EntityIndexSet::remove()`
- **變更前簽章 (Before)**: `fn EntityIndexSet::remove(&mut self, entity: Entity)` (L514~L516)
- **變更後簽章 (After)**: `fn EntityIndexSet::remove(&mut self, entity: Entity)` (L514~L516)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn remove(&mut self, entity: Entity) -> bool {
        self.deref_mut().shift_remove(&entity)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn remove(&mut self, entity: Entity) -> bool {
        self.shift_remove(&entity)
    }
```


---

### 🔹 Commit #19: `e0d0afd6`
- **完整 Hash**: `e0d0afd69a3a49d6606dae4be3046561bb4de3f0`
- **說明 (Ground Truth)**: Entity grouping code for entity inspector (#25010)
- **變更檔案數**: 2

#### 📄 檔案: `crates/bevy_dev_tools/src/inspection/entity_grouping.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:232, E:382, A:0)
- **差分統計**: +Nodes: 232, -Nodes: 0, +Edges: 382, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `entities_by_archetype.keys (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world
            .spawn (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Entity::from_index_and_generation (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `clusters.pop (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `[
            ComponentId::new(0),
            ComponentId::new(1),
            ComponentId::new(2),
        ]
        .into_iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `jaccard_distance_partial_overlap_matches_expected_fraction` (FUNCTION_DEF)
  • + [新增節點] `order_siblings` (FUNCTION_DEF)
  • + [新增節點] `entities_by_archetype
            .into_iter()
            .next (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `flat.iter().position (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `left_cluster
        .signature
        .intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.spawn_empty().set_parent_in_place (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.spawn_empty().set_parent_in_place(e).id (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `[ComponentId::new(0)].into_iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `union_size.max (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `children
            .iter (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 599 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `crates/bevy_dev_tools/src/inspection/mod.rs`
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

### 🔹 Commit #20: `74884ffd`
- **完整 Hash**: `74884ffda7831d2b4576ade270199d671bb2e8f9`
- **說明 (Ground Truth)**: Fix exclusive system change detection (#25864)
- **變更檔案數**: 2

#### 📄 檔案: `crates/bevy_ecs/src/schedule/mod.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:230, E:490, A:0) ➔ After(N:246, E:512, A:0)
- **差分統計**: +Nodes: 16, -Nodes: 0, +Edges: 22, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `system.initialize (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.resource_mut::<ChangeHistory> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.init_resource::<TestResource> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `system.run (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `"intentional failure".into (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `IntoSystem::<(), (), _>::into_system (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `exclusive_system_change_detection` (FUNCTION_DEF)
  • + [新增節點] `world.resource_mut::<TestResource> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `fallible_system` (FUNCTION_DEF)
  • + [新增節點] `exclusive_system` (FUNCTION_DEF)
  • + [新增節點] `failed_systems_should_update_change_ticks` (FUNCTION_DEF)
  • + [新增節點] `world.is_resource_changed::<TestResource> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.resource_mut::<ChangeHistory>().0.push (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `res.is_changed (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.init_resource::<ChangeHistory> (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 23 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `crates/bevy_ecs/src/system/function_system.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:123, E:125, A:0) ➔ After(N:130, E:132, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 7, -Edges: 0, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `LastTickGuard::drop` (FUNCTION_DEF)
  • + [新增節點] `exclusive_world.change_tick (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `exclusive_world.last_change_tick (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `access.is_exclusive (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.world.world_mut (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.flush (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `world.world_mut (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `FunctionSystem::run_unsafe` ──[CALLS]──> `world.world_mut (External/Unresolved)`
  • + [新增呼叫邊] `FunctionSystem::run_unsafe` ──[CALLS]──> `exclusive_world.change_tick (External/Unresolved)`
  • + [新增呼叫邊] `FunctionSystem::run_unsafe` ──[CALLS]──> `exclusive_world.last_change_tick (External/Unresolved)`
  • + [新增呼叫邊] `FunctionSystem::run_unsafe` ──[CALLS]──> `Some (External/Unresolved)`
  • + [新增呼叫邊] `FunctionSystem::run_unsafe` ──[CALLS]──> `world.flush (External/Unresolved)`
  • + [新增呼叫邊] `LastTickGuard::drop` ──[CALLS]──> `self.world.world_mut (External/Unresolved)`
  • + [新增呼叫邊] `FunctionSystem::initialize` ──[CALLS]──> `access.is_exclusive (External/Unresolved)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FunctionSystem::new()`
- **變更前簽章 (Before)**: `fn FunctionSystem::new(func: F, system_meta: SystemMeta, state: Option<FunctionSystemState<F::Param>>)` (L525~L535)
- **變更後簽章 (After)**: `fn FunctionSystem::new(func: F, system_meta: SystemMeta, state: Option<FunctionSystemState<F::Param>>)` (L529~L540)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn new(func: F, system_meta: SystemMeta, state: Option<FunctionSystemState<F::Param>>) -> Self {
        Self {
            func,
            #[cfg(feature = "hotpatching")]
            current_ptr: subsecond::HotFn::current(<F as SystemParamFunction<Marker>>::run)
                .ptr_address(),
            state,
            system_meta,
            marker: PhantomData,
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn new(func: F, system_meta: SystemMeta, state: Option<FunctionSystemState<F::Param>>) -> Self {
        Self {
            func,
            #[cfg(feature = "hotpatching")]
            current_ptr: subsecond::HotFn::current(<F as SystemParamFunction<Marker>>::run)
                .ptr_address(),
            state,
            system_meta,
            is_exclusive: false,
            marker: PhantomData,
        }
    }
```

### 🔹 函式: `FunctionSystem::initialize()`
- **變更前簽章 (Before)**: `fn FunctionSystem::initialize(&mut self, world: &mut World)` (L831~L845)
- **變更後簽章 (After)**: `fn FunctionSystem::initialize(&mut self, world: &mut World)` (L881~L898)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn initialize(&mut self, world: &mut World) -> SystemAccess {
        if let Some(state) = &self.state {
            assert_eq!(
                state.world_id,
                world.id(),
                "System built with a different world than the one it was added to.",
            );
        }
        let state = self.state.get_or_insert_with(|| FunctionSystemState {
            param: F::Param::init_state(world),
            world_id: world.id(),
        });
        self.system_meta.last_run = world.change_tick().relative_to(Tick::MAX);
        init_param_or_panic::<F::Param>(&state.param, &mut self.system_meta, world.into())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn initialize(&mut self, world: &mut World) -> SystemAccess {
        if let Some(state) = &self.state {
            assert_eq!(
                state.world_id,
                world.id(),
                "System built with a different world than the one it was added to.",
            );
        }
        let state = self.state.get_or_insert_with(|| FunctionSystemState {
            param: F::Param::init_state(world),
            world_id: world.id(),
        });
        self.system_meta.last_run = world.change_tick().relative_to(Tick::MAX);
        let access =
            init_param_or_panic::<F::Param>(&state.param, &mut self.system_meta, world.into());
        self.is_exclusive = access.is_exclusive();
        access
    }
```

### 🔹 函式: `FunctionSystem::clone()`
- **變更前簽章 (Before)**: `fn FunctionSystem::clone(&self)` (L551~L561)
- **變更後簽章 (After)**: `fn FunctionSystem::clone(&self)` (L556~L567)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn clone(&self) -> Self {
        Self {
            func: self.func.clone(),
            #[cfg(feature = "hotpatching")]
            current_ptr: subsecond::HotFn::current(<F as SystemParamFunction<Marker>>::run)
                .ptr_address(),
            state: None,
            system_meta: SystemMeta::new::<F>(),
            marker: PhantomData,
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn clone(&self) -> Self {
        Self {
            func: self.func.clone(),
            #[cfg(feature = "hotpatching")]
            current_ptr: subsecond::HotFn::current(<F as SystemParamFunction<Marker>>::run)
                .ptr_address(),
            state: None,
            system_meta: SystemMeta::new::<F>(),
            is_exclusive: false,
            marker: PhantomData,
        }
    }
```

### 🔹 函式: `FunctionSystem::run_unsafe()`
- **變更前簽章 (Before)**: `fn FunctionSystem::run_unsafe(
        &mut self,
        input: SystemIn<'_, Self>,
        world: UnsafeWorldCell,
    )` (L768~L806)
- **變更後簽章 (After)**: `fn FunctionSystem::run_unsafe(
        &mut self,
        input: SystemIn<'_, Self>,
        world: UnsafeWorldCell,
    )` (L774~L856)

#### ◀️ 變更前實作碼 (Before Implementation):
```
unsafe fn run_unsafe(
        &mut self,
        input: SystemIn<'_, Self>,
        world: UnsafeWorldCell,
    ) -> Result<Self::Out, RunSystemError> {
        #[cfg(feature = "trace")]
        let _span_guard = self.system_meta.system_span.enter();

        let change_tick = world.increment_change_tick();

        let input = F::In::from_inner(input);

        let state = self.state.as_mut().expect(Self::ERROR_UNINITIALIZED);
        assert_eq!(state.world_id, world.id(), "Encountered a mismatched World. A System cannot be used with Worlds other than the one it was initialized with.");
        // SAFETY:
        // - The above assert ensures the world matches.
        // - All world accesses used by `F::Param` have been registered, so the caller
        //   will ensure that there are no data access conflicts.
        let params = unsafe {
            F::Param::get_param(&mut state.param, &self.system_meta, world, change_tick)
        }?;

        #[cfg(feature = "hotpatching")]
        let out = {
            let mut hot_fn = subsecond::HotFn::current(<F as SystemParamFunction<Marker>>::run);
            // SAFETY:
            // - pointer used to call is from the current jump table
            unsafe {
                hot_fn
                    .try_call_with_ptr(self.current_ptr, (&mut self.func, input, params))
                    .expect("Error calling hotpatched system. Run a full rebuild")
            }
        };
        #[cfg(not(feature = "hotpatching"))]
        let out = self.func.run(input, params);

        self.system_meta.last_run = change_tick;
        IntoResult::into_result(out)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
unsafe fn run_unsafe(
        &mut self,
        input: SystemIn<'_, Self>,
        world: UnsafeWorldCell,
    ) -> Result<Self::Out, RunSystemError> {
        // This guard is used by exclusive systems to temporarily set the world's
        // last change tick to the system's last run tick, and then restore it
        // when the system finishes running, regardless of whether the system
        // completes successfully or panics.
        struct LastTickGuard<'a> {
            world: UnsafeWorldCell<'a>,
            last_tick: Tick,
        }
        // By setting the change tick in the drop impl, we ensure that
        // the change tick gets reset even if a panic occurs during the scope.
        impl Drop for LastTickGuard<'_> {
            fn drop(&mut self) {
                // SAFETY: The guard was only created under exclusive access to
                // the world, and nothing else is accessing the world mutably
                // when this drop occurs.
                let world = unsafe { self.world.world_mut() };
                world.last_change_tick = self.last_tick;
            }
        }

        #[cfg(feature = "trace")]
        let _span_guard = self.system_meta.system_span.enter();

        let input = F::In::from_inner(input);

        let state = self.state.as_mut().expect(Self::ERROR_UNINITIALIZED);
        assert_eq!(state.world_id, world.id(), "Encountered a mismatched World. A System cannot be used with Worlds other than the one it was initialized with.");

        let (change_tick, _guard) = if self.is_exclusive {
            // SAFETY: an exclusive system has sole access to the world.
            let exclusive_world = unsafe { world.world_mut() };
            let change_tick = exclusive_world.change_tick();
            let previous_tick = exclusive_world.last_change_tick();
            exclusive_world.last_change_tick = self.system_meta.last_run;

            (
                change_tick,
                Some(LastTickGuard {
                    world,
                    last_tick: previous_tick,
                }),
            )
        } else {
            (world.increment_change_tick(), None)
        };

        // SAFETY:
        // - The above assert ensures the world matches.
        // - All world accesses used by `F::Param` have been registered, so the caller
        //   will ensure that there are no data access conflicts.
        let params = unsafe {
            F::Param::get_param(&mut state.param, &self.system_meta, world, change_tick)
        }?;

        #[cfg(feature = "hotpatching")]
        let out = {
            let mut hot_fn = subsecond::HotFn::current(<F as SystemParamFunction<Marker>>::run);
            // SAFETY:
            // - pointer used to call is from the current jump table
            unsafe {
                hot_fn
                    .try_call_with_ptr(self.current_ptr, (&mut self.func, input, params))
                    .expect("Error calling hotpatched system. Run a full rebuild")
            }
        };
        #[cfg(not(feature = "hotpatching"))]
        let out = self.func.run(input, params);

        if self.is_exclusive {
            // SAFETY: The system has exclusive access to the world.
            let world = unsafe { world.world_mut() };
            world.flush();
            self.system_meta.last_run = world.increment_change_tick();
        } else {
            self.system_meta.last_run = change_tick;
        }
        IntoResult::into_result(out)
    }
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/bevy show 36d1b0514127c6b416180bded0799ef01a33dc68
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 36d1b0514127c6b416180bded0799ef01a33dc68~1 --file test_repos/bevy/crates/bevy_asset/src/saver.rs
   ```
