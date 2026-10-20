# 🔬 CODE-Map 基準審查獨立驗證報告: `ripgrep`
> **技術生態**: `Rust (高併發搜尋 / Mmap / 執行緒池)`  
> **本地倉庫路徑**: `test_repos/ripgrep`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 26 Files  
> **報告生成時間**: 2026-10-20 21:41:53  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `20` / `26` | `76.9%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `5` / `26` | `19.2%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `1` / `26` | `3.8%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`25` / `26`** | **`96.2%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `26` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `020687a7`
- **完整 Hash**: `020687a77d13146923333f0beb274eeabd54a270`
- **說明 (Ground Truth)**: ignore,globset: increase pool capacity
- **變更檔案數**: 2

#### 📄 檔案: `crates/ignore/src/gitignore.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:175, E:267, A:0) ➔ After(N:176, E:268, A:0)
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
  • + [新增節點] `Pool::with_available_parallelism_capacity (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `GitignoreBuilder::build` ──[CALLS]──> `Pool::with_available_parallelism_capacity (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `GitignoreBuilder::build()`
- **變更前簽章 (Before)**: `fn GitignoreBuilder::build(&self)` (L349~L364)
- **變更後簽章 (After)**: `fn GitignoreBuilder::build(&self)` (L349~L366)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn build(&self) -> Result<Gitignore, Error> {
        let nignore = self.globs.iter().filter(|g| !g.is_whitelist()).count();
        let nwhite = self.globs.iter().filter(|g| g.is_whitelist()).count();
        let set = self
            .builder
            .build()
            .map_err(|err| Error::Glob { glob: None, err: err.to_string() })?;
        Ok(Gitignore {
            set,
            root: self.root.clone(),
            globs: self.globs.clone(),
            num_ignores: nignore as u64,
            num_whitelists: nwhite as u64,
            matches: Some(Arc::new(Pool::new(|| vec![]))),
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn build(&self) -> Result<Gitignore, Error> {
        let nignore = self.globs.iter().filter(|g| !g.is_whitelist()).count();
        let nwhite = self.globs.iter().filter(|g| g.is_whitelist()).count();
        let set = self
            .builder
            .build()
            .map_err(|err| Error::Glob { glob: None, err: err.to_string() })?;
        Ok(Gitignore {
            set,
            root: self.root.clone(),
            globs: self.globs.clone(),
            num_ignores: nignore as u64,
            num_whitelists: nwhite as u64,
            matches: Some(Arc::new(
                Pool::with_available_parallelism_capacity(|| vec![]),
            )),
        })
    }
```


#### 📄 檔案: `crates/ignore/src/types.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:87, E:108, A:0) ➔ After(N:88, E:110, A:0)
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
  • + [新增節點] `Pool::with_available_parallelism_capacity (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Types::empty` ──[CALLS]──> `Pool::with_available_parallelism_capacity (External/Unresolved)`
  • + [新增呼叫邊] `TypesBuilder::build` ──[CALLS]──> `Pool::with_available_parallelism_capacity (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TypesBuilder::build()`
- **變更前簽章 (Before)**: `fn TypesBuilder::build(&self)` (L322~L362)
- **變更後簽章 (After)**: `fn TypesBuilder::build(&self)` (L324~L366)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn build(&self) -> Result<Types, Error> {
        let defs = self.definitions();
        let has_selected = self.selections.iter().any(|s| !s.is_negated());

        let mut selections = vec![];
        let mut glob_to_selection = vec![];
        let mut build_set = GlobSetBuilder::new();
        for (isel, selection) in self.selections.iter().enumerate() {
            let def = match self.types.get(selection.name()) {
                Some(def) => def.clone(),
                None => {
                    let name = selection.name().to_string();
                    return Err(Error::UnrecognizedFileType(name));
                }
            };
            for (iglob, glob) in def.globs.iter().enumerate() {
                build_set.add(
                    GlobBuilder::new(glob)
                        .literal_separator(true)
                        .build()
                        .map_err(|err| Error::Glob {
                            glob: Some(glob.to_string()),
                            err: err.kind().to_string(),
                        })?,
                );
                glob_to_selection.push((isel, iglob));
            }
            selections.push(selection.clone().map(move |_| def));
        }
        let set = build_set
            .build()
            .map_err(|err| Error::Glob { glob: None, err: err.to_string() })?;
        Ok(Types {
            defs,
            selections,
            has_selected,
            glob_to_selection,
            set,
            matches: Arc::new(Pool::new(|| vec![])),
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn build(&self) -> Result<Types, Error> {
        let defs = self.definitions();
        let has_selected = self.selections.iter().any(|s| !s.is_negated());

        let mut selections = vec![];
        let mut glob_to_selection = vec![];
        let mut build_set = GlobSetBuilder::new();
        for (isel, selection) in self.selections.iter().enumerate() {
            let def = match self.types.get(selection.name()) {
                Some(def) => def.clone(),
                None => {
                    let name = selection.name().to_string();
                    return Err(Error::UnrecognizedFileType(name));
                }
            };
            for (iglob, glob) in def.globs.iter().enumerate() {
                build_set.add(
                    GlobBuilder::new(glob)
                        .literal_separator(true)
                        .build()
                        .map_err(|err| Error::Glob {
                            glob: Some(glob.to_string()),
                            err: err.kind().to_string(),
                        })?,
                );
                glob_to_selection.push((isel, iglob));
            }
            selections.push(selection.clone().map(move |_| def));
        }
        let set = build_set
            .build()
            .map_err(|err| Error::Glob { glob: None, err: err.to_string() })?;
        Ok(Types {
            defs,
            selections,
            has_selected,
            glob_to_selection,
            set,
            matches: Arc::new(Pool::with_available_parallelism_capacity(
                || vec![],
            )),
        })
    }
```

### 🔹 函式: `Types::empty()`
- **變更前簽章 (Before)**: `fn Types::empty()` (L227~L236)
- **變更後簽章 (After)**: `fn Types::empty()` (L227~L238)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn empty() -> Types {
        Types {
            defs: vec![],
            selections: vec![],
            has_selected: false,
            glob_to_selection: vec![],
            set: GlobSetBuilder::new().build().unwrap(),
            matches: Arc::new(Pool::new(|| vec![])),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn empty() -> Types {
        Types {
            defs: vec![],
            selections: vec![],
            has_selected: false,
            glob_to_selection: vec![],
            set: GlobSetBuilder::new().build().unwrap(),
            matches: Arc::new(Pool::with_available_parallelism_capacity(
                || vec![],
            )),
        }
    }
```


---

### 🔹 Commit #02: `435f59fc`
- **完整 Hash**: `435f59fc4b43af3ab32f34d53fa34978f393fe52`
- **說明 (Ground Truth)**: ignore: skip loading unreachable ignore files
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/walk.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:412, E:740, A:0) ➔ After(N:419, E:758, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 18, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `builder
            .build()
            .find_map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `max_depth_does_not_load_unreachable_ignore_files` (FUNCTION_DEF)
  • + [新增節點] `builder
            .build()
            .find_map(|result| {
                let entry = result.unwrap();
                (entry.path() == leaf).then_some(entry)
            })
            .unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.ig.add_child_with_entries (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `(entry.path() == leaf).then_some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `leaf.join (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `result.unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Walk::next` ──[CALLS]──> `self.ig.add_child_with_entries (External/Unresolved)`
  • + [新增呼叫邊] `Walk::next` ──[CALLS]──> `DirEntryRaw::depth`
  • + [新增呼叫邊] `max_depth_does_not_load_unreachable_ignore_files` ──[CALLS]──> `tmpdir`
  • + [新增呼叫邊] `max_depth_does_not_load_unreachable_ignore_files` ──[CALLS]──> `td.path().join (External/Unresolved)`
  • + [新增呼叫邊] `max_depth_does_not_load_unreachable_ignore_files` ──[CALLS]──> `DirEntryRaw::path`
  • + [新增呼叫邊] `max_depth_does_not_load_unreachable_ignore_files` ──[CALLS]──> `mkdirp`
  • + [新增呼叫邊] `max_depth_does_not_load_unreachable_ignore_files` ──[CALLS]──> `wfile`
  • + [新增呼叫邊] `max_depth_does_not_load_unreachable_ignore_files` ──[CALLS]──> `leaf.join (External/Unresolved)`
  • _... 以及其餘 10 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Walk::next()`
- **變更前簽章 (Before)**: `fn Walk::next(&mut self)` (L1188~L1254)
- **變更後簽章 (After)**: `fn Walk::next(&mut self)` (L1190~L1261)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn next(&mut self) -> Option<Result<DirEntry, Error>> {
        loop {
            let ev = match self.it.as_mut().and_then(|it| it.next()) {
                Some(ev) => ev,
                None => {
                    match self.its.next() {
                        None => return None,
                        Some((_, None)) => {
                            return Some(Ok(DirEntry::new_stdin()));
                        }
                        Some((path, Some(it))) => {
                            self.it = Some(it);
                            if path.is_dir() {
                                let (ig, err) = self.ig_root.add_parents(path);
                                self.ig = ig;
                                if let Some(err) = err {
                                    return Some(Err(err));
                                }
                            } else {
                                self.ig = self.ig_root.clone();
                            }
                        }
                    }
                    continue;
                }
            };
            match ev {
                Err(err) => {
                    return Some(Err(Error::from_walkdir(err)));
                }
                Ok(WalkEvent::Exit) => {
                    self.ig = self.ig.parent().unwrap();
                }
                Ok(WalkEvent::Dir(ent)) => {
                    let mut ent = DirEntry::new_walkdir(ent, None);
                    let should_skip = match self.skip_entry(&ent) {
                        Err(err) => return Some(Err(err)),
                        Ok(should_skip) => should_skip,
                    };
                    if should_skip {
                        self.it.as_mut().unwrap().it.skip_current_dir();
                        // Still need to push this on the stack because
                        // we'll get a WalkEvent::Exit event for this dir.
                        // We don't care if it errors though.
                        let (igtmp, _) = self.ig.add_child(ent.path());
                        self.ig = igtmp;
                        continue;
                    }
                    let (igtmp, err) = self.ig.add_child(ent.path());
                    self.ig = igtmp;
                    ent.err = err;
                    return Some(Ok(ent));
                }
                Ok(WalkEvent::File(ent)) => {
                    let ent = DirEntry::new_walkdir(ent, None);
                    let should_skip = match self.skip_entry(&ent) {
                        Err(err) => return Some(Err(err)),
                        Ok(should_skip) => should_skip,
                    };
                    if should_skip {
                        continue;
                    }
                    return Some(Ok(ent));
                }
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn next(&mut self) -> Option<Result<DirEntry, Error>> {
        loop {
            let ev = match self.it.as_mut().and_then(|it| it.next()) {
                Some(ev) => ev,
                None => {
                    match self.its.next() {
                        None => return None,
                        Some((_, None)) => {
                            return Some(Ok(DirEntry::new_stdin()));
                        }
                        Some((path, Some(it))) => {
                            self.it = Some(it);
                            if path.is_dir() {
                                let (ig, err) = self.ig_root.add_parents(path);
                                self.ig = ig;
                                if let Some(err) = err {
                                    return Some(Err(err));
                                }
                            } else {
                                self.ig = self.ig_root.clone();
                            }
                        }
                    }
                    continue;
                }
            };
            match ev {
                Err(err) => {
                    return Some(Err(Error::from_walkdir(err)));
                }
                Ok(WalkEvent::Exit) => {
                    self.ig = self.ig.parent().unwrap();
                }
                Ok(WalkEvent::Dir(ent)) => {
                    let mut ent = DirEntry::new_walkdir(ent, None);
                    let should_skip = match self.skip_entry(&ent) {
                        Err(err) => return Some(Err(err)),
                        Ok(should_skip) => should_skip,
                    };
                    if should_skip {
                        self.it.as_mut().unwrap().it.skip_current_dir();
                        // Still need to push this on the stack because
                        // we'll get a WalkEvent::Exit event for this dir.
                        // Its ignore files cannot apply to any visited entry.
                        let (igtmp, _) =
                            self.ig.add_child_with_entries(ent.path(), &[]);
                        self.ig = igtmp;
                        continue;
                    }
                    let (igtmp, err) = if self.max_depth == Some(ent.depth()) {
                        self.ig.add_child_with_entries(ent.path(), &[])
                    } else {
                        self.ig.add_child(ent.path())
                    };
                    self.ig = igtmp;
                    ent.err = err;
                    return Some(Ok(ent));
                }
                Ok(WalkEvent::File(ent)) => {
                    let ent = DirEntry::new_walkdir(ent, None);
                    let should_skip = match self.skip_entry(&ent) {
                        Err(err) => return Some(Err(err)),
                        Ok(should_skip) => should_skip,
                    };
                    if should_skip {
                        continue;
                    }
                    return Some(Ok(ent));
                }
            }
        }
    }
```

### 🔹 函式: `WalkBuilder::build()`
- **變更前簽章 (Before)**: `fn WalkBuilder::build(&self)` (L593~L643)
- **變更後簽章 (After)**: `fn WalkBuilder::build(&self)` (L593~L644)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn build(&self) -> Walk {
        let follow_links = self.follow_links;
        let max_depth = self.max_depth;
        let min_depth = self.min_depth;
        let sorter = self.sorter.clone();
        let its = self
            .paths
            .iter()
            .map(move |p| {
                if p == Path::new("-") {
                    (p.to_path_buf(), None)
                } else {
                    let mut wd = WalkDir::new(p);
                    wd = wd.follow_links(follow_links || p.is_file());
                    wd = wd.same_file_system(self.same_file_system);
                    if let Some(max_depth) = max_depth {
                        wd = wd.max_depth(max_depth);
                    }
                    if let Some(min_depth) = min_depth {
                        wd = wd.min_depth(min_depth);
                    }
                    if let Some(ref sorter) = sorter {
                        match sorter.clone() {
                            Sorter::ByName(cmp) => {
                                wd = wd.sort_by(move |a, b| {
                                    cmp(a.file_name(), b.file_name())
                                });
                            }
                            Sorter::ByPath(cmp) => {
                                wd = wd.sort_by(move |a, b| {
                                    cmp(a.path(), b.path())
                                });
                            }
                        }
                    }
                    (p.to_path_buf(), Some(WalkEventIter::from(wd)))
                }
            })
            .collect::<Vec<_>>()
            .into_iter();
        let ig_root = self.build_ignore();
        Walk {
            its,
            it: None,
            ig_root: ig_root.clone(),
            ig: ig_root.clone(),
            max_filesize: self.max_filesize,
            skip: self.skip.clone(),
            filter: self.filter.clone(),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn build(&self) -> Walk {
        let follow_links = self.follow_links;
        let max_depth = self.max_depth;
        let min_depth = self.min_depth;
        let sorter = self.sorter.clone();
        let its = self
            .paths
            .iter()
            .map(move |p| {
                if p == Path::new("-") {
                    (p.to_path_buf(), None)
                } else {
                    let mut wd = WalkDir::new(p);
                    wd = wd.follow_links(follow_links || p.is_file());
                    wd = wd.same_file_system(self.same_file_system);
                    if let Some(max_depth) = max_depth {
                        wd = wd.max_depth(max_depth);
                    }
                    if let Some(min_depth) = min_depth {
                        wd = wd.min_depth(min_depth);
                    }
                    if let Some(ref sorter) = sorter {
                        match sorter.clone() {
                            Sorter::ByName(cmp) => {
                                wd = wd.sort_by(move |a, b| {
                                    cmp(a.file_name(), b.file_name())
                                });
                            }
                            Sorter::ByPath(cmp) => {
                                wd = wd.sort_by(move |a, b| {
                                    cmp(a.path(), b.path())
                                });
                            }
                        }
                    }
                    (p.to_path_buf(), Some(WalkEventIter::from(wd)))
                }
            })
            .collect::<Vec<_>>()
            .into_iter();
        let ig_root = self.build_ignore();
        Walk {
            its,
            it: None,
            ig_root: ig_root.clone(),
            ig: ig_root.clone(),
            max_depth: self.max_depth,
            max_filesize: self.max_filesize,
            skip: self.skip.clone(),
            filter: self.filter.clone(),
        }
    }
```


---

### 🔹 Commit #03: `b621e65b`
- **完整 Hash**: `b621e65b4fc8a50b55576b07526f21c5d051ad71`
- **說明 (Ground Truth)**: ignore: add incremental checking
- **變更檔案數**: 4

#### 📄 檔案: `crates/ignore/src/dir.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:254, E:463, A:0) ➔ After(N:255, E:463, A:0)
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
  • + [新增節點] `IgnoreBuilder::is_hidden` (FUNCTION_DEF)

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Ignore::matched()`
- **變更前簽章 (Before)**: `fn Ignore::matched(
        &'a self,
        path: P,
        is_dir: bool,
    )` (L500~L544)
- **變更後簽章 (After)**: `fn Ignore::matched(
        &'a self,
        path: P,
        is_dir: bool,
    )` (L500~L544)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn matched<'a, P: AsRef<Path>>(
        &'a self,
        path: P,
        is_dir: bool,
    ) -> Match<IgnoreMatch<'a>> {
        // We need to be careful with our path. If it has a leading ./, then
        // strip it because it causes nothing but trouble.
        let mut path = path.as_ref();
        if let Some(p) = strip_prefix("./", path) {
            path = p;
        }
        // Match against the override patterns. If an override matches
        // regardless of whether it's whitelist/ignore, then we quit and
        // return that result immediately. Overrides have the highest
        // precedence.
        if !self.inner.overrides.is_empty() {
            let mat = self
                .inner
                .overrides
                .matched(path, is_dir)
                .map(IgnoreMatch::overrides);
            if !mat.is_none() {
                return mat;
            }
        }
        let mut whitelisted = Match::None;
        if self.has_any_ignore_rules() {
            let mat = self.matched_ignore(path, is_dir);
            if mat.is_ignore() {
                return mat;
            } else if mat.is_whitelist() {
                whitelisted = mat;
            }
        }
        if !self.inner.types.is_empty() {
            let mat =
                self.inner.types.matched(path, is_dir).map(IgnoreMatch::types);
            if mat.is_ignore() {
                return mat;
            } else if mat.is_whitelist() {
                whitelisted = mat;
            }
        }
        whitelisted
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn matched<'a, P: AsRef<Path>>(
        &'a self,
        path: P,
        is_dir: bool,
    ) -> Match<IgnoreMatch<'a>> {
        // We need to be careful with our path. If it has a leading ./, then
        // strip it because it causes nothing but trouble.
        let mut path = path.as_ref();
        if let Some(p) = strip_prefix("./", path) {
            path = p;
        }
        // Match against the override patterns. If an override matches
        // regardless of whether it's whitelist/ignore, then we quit and
        // return that result immediately. Overrides have the highest
        // precedence.
        if !self.inner.overrides.is_empty() {
            let mat = self
                .inner
                .overrides
                .matched(path, is_dir)
                .map(IgnoreMatch::overrides);
            if !mat.is_none() {
                return mat;
            }
        }
        let mut whitelisted = Match::None;
        if self.has_any_ignore_rules() {
            let mat = self.matched_ignore(path, is_dir);
            if mat.is_ignore() {
                return mat;
            } else if mat.is_whitelist() {
                whitelisted = mat;
            }
        }
        if !self.inner.types.is_empty() {
            let mat =
                self.inner.types.matched(path, is_dir).map(IgnoreMatch::types);
            if mat.is_ignore() {
                return mat;
            } else if mat.is_whitelist() {
                whitelisted = mat;
            }
        }
        whitelisted
    }
```

### 🔹 函式: `Ignore::matched_ignore()`
- **變更前簽章 (Before)**: `fn Ignore::matched_ignore(
        &'a self,
        path: &Path,
        is_dir: bool,
    )` (L548~L685)
- **變更後簽章 (After)**: `fn Ignore::matched_ignore(
        &'a self,
        path: &Path,
        is_dir: bool,
    )` (L548~L685)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn matched_ignore<'a>(
        &'a self,
        path: &Path,
        is_dir: bool,
    ) -> Match<IgnoreMatch<'a>> {
        let (
            mut m_custom_ignore,
            mut m_ignore,
            mut m_gi,
            mut m_gi_exclude,
            mut m_explicit,
        ) = (Match::None, Match::None, Match::None, Match::None, Match::None);
        let any_git = !self.inner.opts.require_git
            || self.parents().any(|ig| ig.inner.has_git);
        let mut saw_git = false;
        for ig in self.parents().take_while(|ig| !ig.inner.is_absolute_parent)
        {
            if m_custom_ignore.is_none() {
                m_custom_ignore = ig
                    .inner
                    .custom_ignore_matcher
                    .matched(path, is_dir)
                    .map(IgnoreMatch::gitignore);
            }
            if m_ignore.is_none() {
                m_ignore = ig
                    .inner
                    .ignore_matcher
                    .matched(path, is_dir)
                    .map(IgnoreMatch::gitignore);
            }
            if any_git && !saw_git && m_gi.is_none() {
                m_gi = ig
                    .inner
                    .git_ignore_matcher
                    .matched(path, is_dir)
                    .map(IgnoreMatch::gitignore);
            }
            if any_git && !saw_git && m_gi_exclude.is_none() {
                m_gi_exclude = ig
                    .inner
                    .git_exclude_matcher
                    .matched(path, is_dir)
                    .map(IgnoreMatch::gitignore);
            }
            saw_git = saw_git || ig.inner.has_git;
        }
        if self.inner.opts.parents {
            if let Some(abs_parent_path) = self.absolute_base() {
                // What we want to do here is take the absolute base path of
                // this directory and join it with the path we're searching.
                // The main issue we want to avoid is accidentally duplicating
                // directory components, so we try to strip any common prefix
                // off of `path`. Overall, this seems a little ham-fisted, but
                // it does fix a nasty bug. It should do fine until we overhaul
                // this crate.
                let path = abs_parent_path.join(
                    self.parents()
                        .take_while(|ig| !ig.inner.is_absolute_parent)
                        .last()
                        .map_or(path, |ig| {
                            // This is a weird special case when ripgrep users
                            // search with just a `.`, as some tools do
                            // automatically (like consult). In this case, if
                            // we don't bail out now, the code below will strip
                            // a leading `.` from `path`, which might mangle
                            // a hidden file name!
                            if ig.inner.dir.as_path() == Path::new(".") {
                                return path;
                            }
                            let without_dot_slash = strip_if_is_prefix(
                                "./",
                                ig.inner.dir.as_path(),
                            );
                            let relative_base =
                                strip_if_is_prefix(without_dot_slash, path);
                            strip_if_is_prefix("/", relative_base)
                        }),
                );

                for ig in self
                    .parents()
                    .skip_while(|ig| !ig.inner.is_absolute_parent)
                {
                    if m_custom_ignore.is_none() {
                        m_custom_ignore = ig
                            .inner
                            .custom_ignore_matcher
                            .matched(&path, is_dir)
                            .map(IgnoreMatch::gitignore);
                    }
                    if m_ignore.is_none() {
                        m_ignore = ig
                            .inner
                            .ignore_matcher
                            .matched(&path, is_dir)
                            .map(IgnoreMatch::gitignore);
                    }
                    if any_git && !saw_git && m_gi.is_none() {
                        m_gi = ig
                            .inner
                            .git_ignore_matcher
                            .matched(&path, is_dir)
                            .map(IgnoreMatch::gitignore);
                    }
                    if any_git && !saw_git && m_gi_exclude.is_none() {
                        m_gi_exclude = ig
                            .inner
                            .git_exclude_matcher
                            .matched(&path, is_dir)
                            .map(IgnoreMatch::gitignore);
                    }
                    saw_git = saw_git || ig.inner.has_git;
                }
            }
        }
        for gi in self.inner.explicit_ignores.iter().rev() {
            if !m_explicit.is_none() {
                break;
            }
            m_explicit = gi.matched(&path, is_dir).map(IgnoreMatch::gitignore);
        }
        let m_global = if any_git {
            self.inner
                .git_global_matcher
                .matched(&path, is_dir)
                .map(IgnoreMatch::gitignore)
        } else {
            Match::None
        };

        m_custom_ignore
            .or(m_ignore)
            .or(m_gi)
            .or(m_gi_exclude)
            .or(m_global)
            .or(m_explicit)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn matched_ignore<'a>(
        &'a self,
        path: &Path,
        is_dir: bool,
    ) -> Match<IgnoreMatch<'a>> {
        let (
            mut m_custom_ignore,
            mut m_ignore,
            mut m_gi,
            mut m_gi_exclude,
            mut m_explicit,
        ) = (Match::None, Match::None, Match::None, Match::None, Match::None);
        let any_git = !self.inner.opts.require_git
            || self.parents().any(|ig| ig.inner.has_git);
        let mut saw_git = false;
        for ig in self.parents().take_while(|ig| !ig.inner.is_absolute_parent)
        {
            if m_custom_ignore.is_none() {
                m_custom_ignore = ig
                    .inner
                    .custom_ignore_matcher
                    .matched(path, is_dir)
                    .map(IgnoreMatch::gitignore);
            }
            if m_ignore.is_none() {
                m_ignore = ig
                    .inner
                    .ignore_matcher
                    .matched(path, is_dir)
                    .map(IgnoreMatch::gitignore);
            }
            if any_git && !saw_git && m_gi.is_none() {
                m_gi = ig
                    .inner
                    .git_ignore_matcher
                    .matched(path, is_dir)
                    .map(IgnoreMatch::gitignore);
            }
            if any_git && !saw_git && m_gi_exclude.is_none() {
                m_gi_exclude = ig
                    .inner
                    .git_exclude_matcher
                    .matched(path, is_dir)
                    .map(IgnoreMatch::gitignore);
            }
            saw_git = saw_git || ig.inner.has_git;
        }
        if self.inner.opts.parents {
            if let Some(abs_parent_path) = self.absolute_base() {
                // What we want to do here is take the absolute base path of
                // this directory and join it with the path we're searching.
                // The main issue we want to avoid is accidentally duplicating
                // directory components, so we try to strip any common prefix
                // off of `path`. Overall, this seems a little ham-fisted, but
                // it does fix a nasty bug. It should do fine until we overhaul
                // this crate.
                let path = abs_parent_path.join(
                    self.parents()
                        .take_while(|ig| !ig.inner.is_absolute_parent)
                        .last()
                        .map_or(path, |ig| {
                            // This is a weird special case when ripgrep users
                            // search with just a `.`, as some tools do
                            // automatically (like consult). In this case, if
                            // we don't bail out now, the code below will strip
                            // a leading `.` from `path`, which might mangle
                            // a hidden file name!
                            if ig.inner.dir.as_path() == Path::new(".") {
                                return path;
                            }
                            let without_dot_slash = strip_if_is_prefix(
                                "./",
                                ig.inner.dir.as_path(),
                            );
                            let relative_base =
                                strip_if_is_prefix(without_dot_slash, path);
                            strip_if_is_prefix("/", relative_base)
                        }),
                );

                for ig in self
                    .parents()
                    .skip_while(|ig| !ig.inner.is_absolute_parent)
                {
                    if m_custom_ignore.is_none() {
                        m_custom_ignore = ig
                            .inner
                            .custom_ignore_matcher
                            .matched(&path, is_dir)
                            .map(IgnoreMatch::gitignore);
                    }
                    if m_ignore.is_none() {
                        m_ignore = ig
                            .inner
                            .ignore_matcher
                            .matched(&path, is_dir)
                            .map(IgnoreMatch::gitignore);
                    }
                    if any_git && !saw_git && m_gi.is_none() {
                        m_gi = ig
                            .inner
                            .git_ignore_matcher
                            .matched(&path, is_dir)
                            .map(IgnoreMatch::gitignore);
                    }
                    if any_git && !saw_git && m_gi_exclude.is_none() {
                        m_gi_exclude = ig
                            .inner
                            .git_exclude_matcher
                            .matched(&path, is_dir)
                            .map(IgnoreMatch::gitignore);
                    }
                    saw_git = saw_git || ig.inner.has_git;
                }
            }
        }
        for gi in self.inner.explicit_ignores.iter().rev() {
            if !m_explicit.is_none() {
                break;
            }
            m_explicit = gi.matched(&path, is_dir).map(IgnoreMatch::gitignore);
        }
        let m_global = if any_git {
            self.inner
                .git_global_matcher
                .matched(&path, is_dir)
                .map(IgnoreMatch::gitignore)
        } else {
            Match::None
        };

        m_custom_ignore
            .or(m_ignore)
            .or(m_gi)
            .or(m_gi_exclude)
            .or(m_global)
            .or(m_explicit)
    }
```


#### 📄 檔案: `crates/ignore/src/incremental.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:175, E:448, A:0)
- **差分統計**: +Nodes: 175, -Nodes: 0, +Edges: 448, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `b.max_depth (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `IncrementalMatch::should_descend` (FUNCTION_DEF)
  • + [新增節點] `normalized.push (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `relative.components (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `relative.is_absolute (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `WalkBuilder::from_iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `respects_git_repository_boundaries` (FUNCTION_DEF)
  • + [新增節點] `normalized.pop (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `builder.git_ignore(false).git_exclude (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `matchers.pop().unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert_eq! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `file.write_all(contents.as_bytes()).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `overrides.build (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `b.hidden (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert! (Macro)` (FUNCTION_DEF)
  • _... 以及其餘 608 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `crates/ignore/src/lib.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:72, E:81, A:0) ➔ After(N:72, E:81, A:0)
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

#### 📄 檔案: `crates/ignore/src/walk.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:403, E:735, A:0) ➔ After(N:412, E:740, A:0)
- **差分統計**: +Nodes: 11, -Nodes: 2, +Edges: 18, -Edges: 13, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `options.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.ig_builder.is_hidden (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.paths
            .iter()
            .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `path.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.paths
            .iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `ignore.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.get_or_set_current_dir()
            .map(|cwd| self.ig_builder.build_with_cwd(Some(cwd.to_path_buf())))
            .unwrap_or_else (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.paths
            .iter()
            .map(move |path| {
                IncrementalIgnore::new(
                    path.clone(),
                    ignore.clone(),
                    options.clone(),
                )
            })
            .collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `WalkBuilder::build_ignore` (FUNCTION_DEF)
  • + [新增節點] `WalkBuilder::build_matchers` (FUNCTION_DEF)
  • + [新增節點] `self.get_or_set_current_dir()
            .map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `self
            .get_or_set_current_dir()
            .map(|cwd| self.ig_builder.build_with_cwd(Some(cwd.to_path_buf())))
            .unwrap_or_else (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `self
            .get_or_set_current_dir()
            .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `WalkBuilder::build` ──[CALLS]──> `WalkBuilder::build_ignore`
  • + [新增呼叫邊] `WalkBuilder::build_matchers` ──[CALLS]──> `WalkBuilder::build_ignore`
  • _... 以及其餘 29 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `WalkBuilder::build_parallel()`
- **變更前簽章 (Before)**: `fn WalkBuilder::build_parallel(&self)` (L652~L669)
- **變更後簽章 (After)**: `fn WalkBuilder::build_parallel(&self)` (L700~L714)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn build_parallel(&self) -> WalkParallel {
        let ig_root = self
            .get_or_set_current_dir()
            .map(|cwd| self.ig_builder.build_with_cwd(Some(cwd.to_path_buf())))
            .unwrap_or_else(|| self.ig_builder.build());
        WalkParallel {
            paths: self.paths.clone().into_iter(),
            ig_root,
            max_depth: self.max_depth,
            min_depth: self.min_depth,
            max_filesize: self.max_filesize,
            follow_links: self.follow_links,
            same_file_system: self.same_file_system,
            threads: self.threads,
            skip: self.skip.clone(),
            filter: self.filter.clone(),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn build_parallel(&self) -> WalkParallel {
        let ig_root = self.build_ignore();
        WalkParallel {
            paths: self.paths.clone().into_iter(),
            ig_root,
            max_depth: self.max_depth,
            min_depth: self.min_depth,
            max_filesize: self.max_filesize,
            follow_links: self.follow_links,
            same_file_system: self.same_file_system,
            threads: self.threads,
            skip: self.skip.clone(),
            filter: self.filter.clone(),
        }
    }
```

### 🔹 函式: `WalkBuilder::build()`
- **變更前簽章 (Before)**: `fn WalkBuilder::build(&self)` (L592~L645)
- **變更後簽章 (After)**: `fn WalkBuilder::build(&self)` (L593~L643)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn build(&self) -> Walk {
        let follow_links = self.follow_links;
        let max_depth = self.max_depth;
        let min_depth = self.min_depth;
        let sorter = self.sorter.clone();
        let its = self
            .paths
            .iter()
            .map(move |p| {
                if p == Path::new("-") {
                    (p.to_path_buf(), None)
                } else {
                    let mut wd = WalkDir::new(p);
                    wd = wd.follow_links(follow_links || p.is_file());
                    wd = wd.same_file_system(self.same_file_system);
                    if let Some(max_depth) = max_depth {
                        wd = wd.max_depth(max_depth);
                    }
                    if let Some(min_depth) = min_depth {
                        wd = wd.min_depth(min_depth);
                    }
                    if let Some(ref sorter) = sorter {
                        match sorter.clone() {
                            Sorter::ByName(cmp) => {
                                wd = wd.sort_by(move |a, b| {
                                    cmp(a.file_name(), b.file_name())
                                });
                            }
                            Sorter::ByPath(cmp) => {
                                wd = wd.sort_by(move |a, b| {
                                    cmp(a.path(), b.path())
                                });
                            }
                        }
                    }
                    (p.to_path_buf(), Some(WalkEventIter::from(wd)))
                }
            })
            .collect::<Vec<_>>()
            .into_iter();
        let ig_root = self
            .get_or_set_current_dir()
            .map(|cwd| self.ig_builder.build_with_cwd(Some(cwd.to_path_buf())))
            .unwrap_or_else(|| self.ig_builder.build());
        Walk {
            its,
            it: None,
            ig_root: ig_root.clone(),
            ig: ig_root.clone(),
            max_filesize: self.max_filesize,
            skip: self.skip.clone(),
            filter: self.filter.clone(),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn build(&self) -> Walk {
        let follow_links = self.follow_links;
        let max_depth = self.max_depth;
        let min_depth = self.min_depth;
        let sorter = self.sorter.clone();
        let its = self
            .paths
            .iter()
            .map(move |p| {
                if p == Path::new("-") {
                    (p.to_path_buf(), None)
                } else {
                    let mut wd = WalkDir::new(p);
                    wd = wd.follow_links(follow_links || p.is_file());
                    wd = wd.same_file_system(self.same_file_system);
                    if let Some(max_depth) = max_depth {
                        wd = wd.max_depth(max_depth);
                    }
                    if let Some(min_depth) = min_depth {
                        wd = wd.min_depth(min_depth);
                    }
                    if let Some(ref sorter) = sorter {
                        match sorter.clone() {
                            Sorter::ByName(cmp) => {
                                wd = wd.sort_by(move |a, b| {
                                    cmp(a.file_name(), b.file_name())
                                });
                            }
                            Sorter::ByPath(cmp) => {
                                wd = wd.sort_by(move |a, b| {
                                    cmp(a.path(), b.path())
                                });
                            }
                        }
                    }
                    (p.to_path_buf(), Some(WalkEventIter::from(wd)))
                }
            })
            .collect::<Vec<_>>()
            .into_iter();
        let ig_root = self.build_ignore();
        Walk {
            its,
            it: None,
            ig_root: ig_root.clone(),
            ig: ig_root.clone(),
            max_filesize: self.max_filesize,
            skip: self.skip.clone(),
            filter: self.filter.clone(),
        }
    }
```


---

### 🔹 Commit #04: `c55818fd`
- **完整 Hash**: `c55818fd32d68cf742aea67bce86529f198bc985`
- **說明 (Ground Truth)**: ignore: more pathutil clean-up
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/pathutil.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:52, E:60, A:0) ➔ After(N:47, E:53, A:0)
- **差分統計**: +Nodes: 12, -Nodes: 17, +Edges: 36, -Edges: 43, ΔFuncs: 6, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `path.as_ref()
            .parent()
            .map(|p| p.as_os_str().is_empty())
            .unwrap_or (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `name.as_encoded_bytes (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `path.as_ref()
            .parent()
            .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `imp` (FUNCTION_DEF)
  • + [新增節點] `memchr::memchr (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `name.as_encoded_bytes().starts_with (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `prefix.as_os_str().as_bytes (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `memchr::memchr(b'/', path.as_ref().as_os_str().as_encoded_bytes())
            .is_none (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `imp` (FUNCTION_DEF)
  • + [新增節點] `path.as_ref().as_os_str().as_encoded_bytes (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `path.as_ref()
            .parent (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `prefix.as_os_str (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `path.as_ref().parent().map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `s.starts_with (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `name.as_bytes (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 93 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `strip_prefix()`
- **變更前簽章 (Before)**: `fn strip_prefix(
    prefix: &'a P,
    path: &'a Path,
)` (L113~L126)
- **變更後簽章 (After)**: `fn strip_prefix(
    prefix: &'a P,
    path: &'a Path,
)` (L96~L119)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn strip_prefix<'a, P: AsRef<Path> + ?Sized>(
    prefix: &'a P,
    path: &'a Path,
) -> Option<&'a Path> {
    use std::os::unix::ffi::OsStrExt;

    let prefix = prefix.as_ref().as_os_str().as_bytes();
    let path = path.as_os_str().as_bytes();
    if prefix.len() > path.len() || prefix != &path[0..prefix.len()] {
        None
    } else {
        Some(&Path::new(OsStr::from_bytes(&path[prefix.len()..])))
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn strip_prefix<'a, P: AsRef<Path> + ?Sized>(
    prefix: &'a P,
    path: &'a Path,
) -> Option<&'a Path> {
    #[cfg(unix)]
    fn imp<'a>(prefix: &'a Path, path: &'a Path) -> Option<&'a Path> {
        use std::os::unix::ffi::OsStrExt;

        let prefix = prefix.as_os_str().as_bytes();
        let path = path.as_os_str().as_bytes();
        if prefix.len() > path.len() || prefix != &path[0..prefix.len()] {
            None
        } else {
            Some(&Path::new(OsStr::from_bytes(&path[prefix.len()..])))
        }
    }

    #[cfg(not(unix))]
    fn imp<'a>(prefix: &'a Path, path: &'a Path) -> Option<&'a Path> {
        path.strip_prefix(prefix).ok()
    }

    imp(prefix.as_ref(), path)
}
```

### 🔹 函式: `is_file_name()`
- **變更前簽章 (Before)**: `fn is_file_name(path: P)` (L142~L149)
- **變更後簽章 (After)**: `fn is_file_name(path: P)` (L123~L136)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn is_file_name<P: AsRef<Path>>(path: P) -> bool {
    use std::os::unix::ffi::OsStrExt;

    use memchr::memchr;

    let path = path.as_ref().as_os_str().as_bytes();
    memchr(b'/', path).is_none()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn is_file_name<P: AsRef<Path>>(path: P) -> bool {
    #[cfg(unix)]
    {
        memchr::memchr(b'/', path.as_ref().as_os_str().as_encoded_bytes())
            .is_none()
    }
    #[cfg(not(unix))]
    {
        path.as_ref()
            .parent()
            .map(|p| p.as_os_str().is_empty())
            .unwrap_or(false)
    }
}
```

### 🔹 函式: `imp()`
- **變更前簽章 (Before)**: `fn imp(path: &Path)` (L98~L104)
- **變更後簽章 (After)**: `fn imp(prefix: &'a Path, path: &'a Path)` (L114~L116)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn imp(path: &Path) -> bool {
        if let Some(name) = file_name(path) {
            name.to_str().map(|s| s.starts_with(".")).unwrap_or(false)
        } else {
            false
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn imp<'a>(prefix: &'a Path, path: &'a Path) -> Option<&'a Path> {
        path.strip_prefix(prefix).ok()
    }
```

### 🔹 函式: `file_name()`
- **變更前簽章 (Before)**: `fn file_name(
    path: &'a P,
)` (L163~L181)
- **變更後簽章 (After)**: `fn file_name(
    path: &'a P,
)` (L142~L171)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn file_name<'a, P: AsRef<Path> + ?Sized>(
    path: &'a P,
) -> Option<&'a OsStr> {
    use memchr::memrchr;
    use std::os::unix::ffi::OsStrExt;

    let path = path.as_ref().as_os_str().as_bytes();
    if path.is_empty() {
        return None;
    } else if path.len() == 1 && path[0] == b'.' {
        return None;
    } else if path.last() == Some(&b'.') {
        return None;
    } else if path.len() >= 2 && &path[path.len() - 2..] == &b".."[..] {
        return None;
    }
    let last_slash = memrchr(b'/', path).map(|i| i + 1).unwrap_or(0);
    Some(OsStr::from_bytes(&path[last_slash..]))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn file_name<'a, P: AsRef<Path> + ?Sized>(
    path: &'a P,
) -> Option<&'a OsStr> {
    #[cfg(unix)]
    fn imp(path: &Path) -> Option<&OsStr> {
        use std::os::unix::ffi::OsStrExt;

        use memchr::memrchr;

        let path = path.as_os_str().as_bytes();
        if path.is_empty() {
            return None;
        } else if path.len() == 1 && path[0] == b'.' {
            return None;
        } else if path.last() == Some(&b'.') {
            return None;
        } else if path.len() >= 2 && &path[path.len() - 2..] == &b".."[..] {
            return None;
        }
        let last_slash = memrchr(b'/', path).map(|i| i + 1).unwrap_or(0);
        Some(OsStr::from_bytes(&path[last_slash..]))
    }

    #[cfg(not(unix))]
    fn imp(path: &Path) -> Option<&OsStr> {
        path.file_name()
    }

    imp(path.as_ref())
}
```

### 🔹 函式: `is_hidden_path_only()`
- **變更前簽章 (Before)**: `fn is_hidden_path_only(path: &Path)` (L85~L107)
- **變更後簽章 (After)**: `fn is_hidden_path_only(path: &Path)` (L85~L91)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn is_hidden_path_only(path: &Path) -> bool {
    #[cfg(unix)]
    fn imp(path: &Path) -> bool {
        use std::os::unix::ffi::OsStrExt;

        if let Some(name) = file_name(path) {
            name.as_bytes().get(0) == Some(&b'.')
        } else {
            false
        }
    }

    #[cfg(not(unix))]
    fn imp(path: &Path) -> bool {
        if let Some(name) = file_name(path) {
            name.to_str().map(|s| s.starts_with(".")).unwrap_or(false)
        } else {
            false
        }
    }

    imp(path)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn is_hidden_path_only(path: &Path) -> bool {
    if let Some(name) = file_name(path) {
        name.as_encoded_bytes().starts_with(b".")
    } else {
        false
    }
}
```

### 🔹 函式: `imp()`
- **變更前簽章 (Before)**: `fn imp(path: &Path)` (L87~L95)
- **變更後簽章 (After)**: `fn imp(prefix: &'a Path, path: &'a Path)` (L101~L111)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn imp(path: &Path) -> bool {
        use std::os::unix::ffi::OsStrExt;

        if let Some(name) = file_name(path) {
            name.as_bytes().get(0) == Some(&b'.')
        } else {
            false
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn imp<'a>(prefix: &'a Path, path: &'a Path) -> Option<&'a Path> {
        use std::os::unix::ffi::OsStrExt;

        let prefix = prefix.as_os_str().as_bytes();
        let path = path.as_os_str().as_bytes();
        if prefix.len() > path.len() || prefix != &path[0..prefix.len()] {
            None
        } else {
            Some(&Path::new(OsStr::from_bytes(&path[prefix.len()..])))
        }
    }
```


---

### 🔹 Commit #05: `6e527e92`
- **完整 Hash**: `6e527e9202f85a39ab2c4698636710204eb096e0`
- **說明 (Ground Truth)**: ignore: add routine for checking if a path is hidden or not
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/pathutil.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:46, E:57, A:0) ➔ After(N:52, E:60, A:0)
- **差分統計**: +Nodes: 6, -Nodes: 0, +Edges: 21, -Edges: 18, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `path.metadata (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `is_hidden_path` (FUNCTION_DEF)
  • + [新增節點] `imp` (FUNCTION_DEF)
  • + [新增節點] `imp` (FUNCTION_DEF)
  • + [新增節點] `is_hidden_path_only` (FUNCTION_DEF)
  • + [新增節點] `imp` (FUNCTION_DEF)
  • + [新增呼叫邊] `is_hidden_path` ──[CALLS]──> `imp`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `is_hidden_path_only`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `path.metadata (External/Unresolved)`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `is_hidden_path_only`
  • + [新增呼叫邊] `is_hidden_entry` ──[CALLS]──> `imp`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `is_hidden_path_only`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `dent.metadata (External/Unresolved)`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `file::is_hidden (External/Unresolved)`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `md.file_attributes (External/Unresolved)`
  • _... 以及其餘 30 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `is_hidden_entry()`
- **變更前簽章 (Before)**: `fn is_hidden_entry(dent: &DirEntry)` (L20~L62)
- **變更後簽章 (After)**: `fn is_hidden_entry(dent: &DirEntry)` (L56~L79)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn is_hidden_entry(dent: &DirEntry) -> bool {
    #[cfg(unix)]
    fn imp(dent: &DirEntry) -> bool {
        use std::os::unix::ffi::OsStrExt;

        if let Some(name) = file_name(dent.path()) {
            name.as_bytes().get(0) == Some(&b'.')
        } else {
            false
        }
    }

    #[cfg(windows)]
    fn imp(dent: &DirEntry) -> bool {
        use std::os::windows::fs::MetadataExt;
        use winapi_util::file;

        // This looks like we're doing an extra stat call, but on Windows, the
        // directory traverser reuses the metadata retrieved from each directory
        // entry and stores it on the DirEntry itself. So this is "free."
        if let Ok(md) = dent.metadata() {
            if file::is_hidden(md.file_attributes() as u64) {
                return true;
            }
        }
        if let Some(name) = file_name(dent.path()) {
            name.to_str().map(|s| s.starts_with(".")).unwrap_or(false)
        } else {
            false
        }
    }

    #[cfg(not(any(unix, windows)))]
    fn imp(dent: &DirEntry) -> bool {
        if let Some(name) = file_name(dent.path()) {
            name.to_str().map(|s| s.starts_with(".")).unwrap_or(false)
        } else {
            false
        }
    }

    imp(dent)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn is_hidden_entry(dent: &DirEntry) -> bool {
    #[cfg(not(windows))]
    fn imp(dent: &DirEntry) -> bool {
        is_hidden_path_only(dent.path())
    }

    #[cfg(windows)]
    fn imp(dent: &DirEntry) -> bool {
        use std::os::windows::fs::MetadataExt;
        use winapi_util::file;

        // This looks like we're doing an extra stat call, but on Windows, the
        // directory traverser reuses the metadata retrieved from each directory
        // entry and stores it on the DirEntry itself. So this is "free."
        if let Ok(md) = dent.metadata() {
            if file::is_hidden(md.file_attributes() as u64) {
                return true;
            }
        }
        is_hidden_path_only(dent.path())
    }

    imp(dent)
}
```

### 🔹 函式: `imp()`
- **變更前簽章 (Before)**: `fn imp(dent: &DirEntry)` (L33~L50)
- **變更後簽章 (After)**: `fn imp(path: &Path)` (L26~L36)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn imp(dent: &DirEntry) -> bool {
        use std::os::windows::fs::MetadataExt;
        use winapi_util::file;

        // This looks like we're doing an extra stat call, but on Windows, the
        // directory traverser reuses the metadata retrieved from each directory
        // entry and stores it on the DirEntry itself. So this is "free."
        if let Ok(md) = dent.metadata() {
            if file::is_hidden(md.file_attributes() as u64) {
                return true;
            }
        }
        if let Some(name) = file_name(dent.path()) {
            name.to_str().map(|s| s.starts_with(".")).unwrap_or(false)
        } else {
            false
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn imp(path: &Path) -> bool {
        use std::os::windows::fs::MetadataExt;
        use winapi_util::file;

        if let Ok(md) = path.metadata() {
            if file::is_hidden(md.file_attributes() as u64) {
                return true;
            }
        }
        is_hidden_path_only(path)
    }
```

### 🔹 函式: `imp()`
- **變更前簽章 (Before)**: `fn imp(dent: &DirEntry)` (L22~L30)
- **變更後簽章 (After)**: `fn imp(path: &Path)` (L21~L23)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn imp(dent: &DirEntry) -> bool {
        use std::os::unix::ffi::OsStrExt;

        if let Some(name) = file_name(dent.path()) {
            name.as_bytes().get(0) == Some(&b'.')
        } else {
            false
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn imp(path: &Path) -> bool {
        is_hidden_path_only(path)
    }
```

### 🔹 函式: `imp()`
- **變更前簽章 (Before)**: `fn imp(dent: &DirEntry)` (L53~L59)
- **變更後簽章 (After)**: `fn imp(dent: &DirEntry)` (L58~L60)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn imp(dent: &DirEntry) -> bool {
        if let Some(name) = file_name(dent.path()) {
            name.to_str().map(|s| s.starts_with(".")).unwrap_or(false)
        } else {
            false
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn imp(dent: &DirEntry) -> bool {
        is_hidden_path_only(dent.path())
    }
```


---

### 🔹 Commit #06: `626b8951`
- **完整 Hash**: `626b8951acbced7ff710f4e01624a05f219eec38`
- **說明 (Ground Truth)**: ignore: refactor `is_hidden`
- **變更檔案數**: 2

#### 📄 檔案: `crates/ignore/src/dir.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:254, E:463, A:0) ➔ After(N:254, E:463, A:0)
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
  • + [新增節點] `is_hidden_entry (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `is_hidden (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Ignore::matched_dir_entry` ──[CALLS]──> `is_hidden_entry (External/Unresolved)`
  • - [移除呼叫邊] `Ignore::matched_dir_entry` ──[CALLS]──> `is_hidden (External/Unresolved)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Ignore::matched_dir_entry()`
- **變更前簽章 (Before)**: `fn Ignore::matched_dir_entry(
        &'a self,
        dent: &DirEntry,
    )` (L485~L494)
- **變更後簽章 (After)**: `fn Ignore::matched_dir_entry(
        &'a self,
        dent: &DirEntry,
    )` (L485~L494)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn matched_dir_entry<'a>(
        &'a self,
        dent: &DirEntry,
    ) -> Match<IgnoreMatch<'a>> {
        let m = self.matched(dent.path(), dent.is_dir());
        if m.is_none() && self.inner.opts.hidden && is_hidden(dent) {
            return Match::Ignore(IgnoreMatch::hidden());
        }
        m
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn matched_dir_entry<'a>(
        &'a self,
        dent: &DirEntry,
    ) -> Match<IgnoreMatch<'a>> {
        let m = self.matched(dent.path(), dent.is_dir());
        if m.is_none() && self.inner.opts.hidden && is_hidden_entry(dent) {
            return Match::Ignore(IgnoreMatch::hidden());
        }
        m
    }
```


#### 📄 檔案: `crates/ignore/src/pathutil.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:44, E:56, A:0) ➔ After(N:46, E:57, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 3, +Edges: 21, -Edges: 20, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `is_hidden_entry` (FUNCTION_DEF)
  • + [新增節點] `imp` (FUNCTION_DEF)
  • + [新增節點] `imp` (FUNCTION_DEF)
  • + [新增節點] `file::is_hidden (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `imp` (FUNCTION_DEF)
  • - [移除節點] `is_hidden` (FUNCTION_DEF)
  • - [移除節點] `is_hidden` (FUNCTION_DEF)
  • - [移除節點] `is_hidden` (FUNCTION_DEF)
  • + [新增呼叫邊] `is_hidden_entry` ──[CALLS]──> `imp`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `file_name`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `dent.path (External/Unresolved)`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `name.as_bytes().get (External/Unresolved)`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `name.as_bytes (External/Unresolved)`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `Some (External/Unresolved)`
  • + [新增呼叫邊] `imp` ──[CALLS]──> `dent.metadata (External/Unresolved)`
  • _... 以及其餘 34 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #07: `0d7054d8`
- **完整 Hash**: `0d7054d8e466d6aa0a6bb6cf121e87225d26df44`
- **說明 (Ground Truth)**: ignore: fix deadlock when visitor panics
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/walk.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:395, E:711, A:0) ➔ After(N:403, E:735, A:0)
- **差分統計**: +Nodes: 12, -Nodes: 4, +Edges: 28, -Edges: 4, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `workers
                .into_iter()
                .map(|worker| s.spawn(|| worker.run()))
                .collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Worker::drop` (FUNCTION_DEF)
  • + [新增節點] `panic! [未完成實作/執行期中斷]` (FUNCTION_DEF)
  • + [新增節點] `std::thread::panicking (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `panic_in_parallel` (FUNCTION_DEF)
  • + [新增節點] `panic! [未完成實作/執行期中斷]` (FUNCTION_DEF)
  • + [新增節點] `workers
                .into_iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `workers
                .into_iter()
                .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `stacks
            .into_iter()
            .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `panic_in_parallel_builder` (FUNCTION_DEF)
  • + [新增節點] `stacks
            .into_iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `stacks
            .into_iter()
            .map(|stack| Worker {
                visitor: builder.build(),
                stack,
                quit_now: quit_now.clone(),
                active_workers: active_workers.clone(),
                max_depth: self.max_depth,
                min_depth: self.min_depth,
                max_filesize: self.max_filesize,
                follow_links: self.follow_links,
                skip: self.skip.clone(),
                filter: self.filter.clone(),
            })
            .collect (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `stacks
                .into_iter()
                .map(|stack| Worker {
                    visitor: builder.build(),
                    stack,
                    quit_now: quit_now.clone(),
                    active_workers: active_workers.clone(),
                    max_depth: self.max_depth,
                    min_depth: self.min_depth,
                    max_filesize: self.max_filesize,
                    follow_links: self.follow_links,
                    skip: self.skip.clone(),
                    filter: self.filter.clone(),
                })
                .map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `stacks
                .into_iter (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `stacks
                .into_iter()
                .map (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 33 項拓樸變更_

⚠️ **本次 Commit 新引入之危害操作 (New Hazards):**
  - 呼叫了未完成實作或執行期中斷巨集: panic!() (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `WalkParallel::visit()`
- **變更前簽章 (Before)**: `fn WalkParallel::visit(mut self, builder: &mut dyn ParallelVisitorBuilder<'_>)` (L1393~L1469)
- **變更後簽章 (After)**: `fn WalkParallel::visit(mut self, builder: &mut dyn ParallelVisitorBuilder<'_>)` (L1393~L1476)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn visit(mut self, builder: &mut dyn ParallelVisitorBuilder<'_>) {
        let threads = self.threads();
        let mut stack = vec![];
        {
            let mut visitor = builder.build();
            let mut paths = Vec::new().into_iter();
            std::mem::swap(&mut paths, &mut self.paths);
            // Send the initial set of root paths to the pool of workers. Note
            // that we only send directories. For files, we send to them the
            // callback directly.
            for path in paths {
                let (dent, root_device) = if path == Path::new("-") {
                    (DirEntry::new_stdin(), None)
                } else {
                    let root_device = if !self.same_file_system {
                        None
                    } else {
                        match device_num(&path) {
                            Ok(root_device) => Some(root_device),
                            Err(err) => {
                                let err = Error::Io(err).with_path(path);
                                if visitor.visit(Err(err)).is_quit() {
                                    return;
                                }
                                continue;
                            }
                        }
                    };
                    match DirEntryRaw::from_path(0, path, false) {
                        Ok(dent) => {
                            (DirEntry::new_raw(dent, None), root_device)
                        }
                        Err(err) => {
                            if visitor.visit(Err(err)).is_quit() {
                                return;
                            }
                            continue;
                        }
                    }
                };
                stack.push(Message::Work(Work {
                    dent,
                    ignore: self.ig_root.clone(),
                    root_device,
                }));
            }
            // ... but there's no need to start workers if we don't need them.
            if stack.is_empty() {
                return;
            }
        }
        // Create the workers and then wait for them to finish.
        let quit_now = Arc::new(AtomicBool::new(false));
        let active_workers = Arc::new(AtomicUsize::new(threads));
        let stacks = Stack::new_for_each_thread(threads, stack);
        std::thread::scope(|s| {
            let handles: Vec<_> = stacks
                .into_iter()
                .map(|stack| Worker {
                    visitor: builder.build(),
                    stack,
                    quit_now: quit_now.clone(),
                    active_workers: active_workers.clone(),
                    max_depth: self.max_depth,
                    min_depth: self.min_depth,
                    max_filesize: self.max_filesize,
                    follow_links: self.follow_links,
                    skip: self.skip.clone(),
                    filter: self.filter.clone(),
                })
                .map(|worker| s.spawn(|| worker.run()))
                .collect();
            for handle in handles {
                handle.join().unwrap();
            }
        });
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn visit(mut self, builder: &mut dyn ParallelVisitorBuilder<'_>) {
        let threads = self.threads();
        let mut stack = vec![];
        {
            let mut visitor = builder.build();
            let mut paths = Vec::new().into_iter();
            std::mem::swap(&mut paths, &mut self.paths);
            // Send the initial set of root paths to the pool of workers. Note
            // that we only send directories. For files, we send to them the
            // callback directly.
            for path in paths {
                let (dent, root_device) = if path == Path::new("-") {
                    (DirEntry::new_stdin(), None)
                } else {
                    let root_device = if !self.same_file_system {
                        None
                    } else {
                        match device_num(&path) {
                            Ok(root_device) => Some(root_device),
                            Err(err) => {
                                let err = Error::Io(err).with_path(path);
                                if visitor.visit(Err(err)).is_quit() {
                                    return;
                                }
                                continue;
                            }
                        }
                    };
                    match DirEntryRaw::from_path(0, path, false) {
                        Ok(dent) => {
                            (DirEntry::new_raw(dent, None), root_device)
                        }
                        Err(err) => {
                            if visitor.visit(Err(err)).is_quit() {
                                return;
                            }
                            continue;
                        }
                    }
                };
                stack.push(Message::Work(Work {
                    dent,
                    ignore: self.ig_root.clone(),
                    root_device,
                }));
            }
            // ... but there's no need to start workers if we don't need them.
            if stack.is_empty() {
                return;
            }
        }
        // Create the workers and then wait for them to finish.
        let quit_now = Arc::new(AtomicBool::new(false));
        let active_workers = Arc::new(AtomicUsize::new(threads));
        let stacks = Stack::new_for_each_thread(threads, stack);
        // Collect all of the workers first. In the case that
        // `builder.build()` panics, we want that to happen and
        // propagate before we actually start to run any of the
        // workers.
        let workers: Vec<_> = stacks
            .into_iter()
            .map(|stack| Worker {
                visitor: builder.build(),
                stack,
                quit_now: quit_now.clone(),
                active_workers: active_workers.clone(),
                max_depth: self.max_depth,
                min_depth: self.min_depth,
                max_filesize: self.max_filesize,
                follow_links: self.follow_links,
                skip: self.skip.clone(),
                filter: self.filter.clone(),
            })
            .collect();
        std::thread::scope(|s| {
            let handles: Vec<_> = workers
                .into_iter()
                .map(|worker| s.spawn(|| worker.run()))
                .collect();
            for handle in handles {
                handle.join().unwrap();
            }
        });
    }
```

### 🔹 函式: `Worker::get_work()`
- **變更前簽章 (Before)**: `fn Worker::get_work(&mut self)` (L1876~L1923)
- **變更後簽章 (After)**: `fn Worker::get_work(&mut self)` (L1883~L1933)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn get_work(&mut self) -> Option<Work> {
        let mut value = self.recv();
        loop {
            // Simulate a priority channel: If quit_now flag is set, we can
            // receive only quit messages.
            if self.is_quit_now() {
                value = Some(Message::Quit)
            }
            match value {
                Some(Message::Work(work)) => {
                    return Some(work);
                }
                Some(Message::Quit) => {
                    // Repeat quit message to wake up sleeping threads, if
                    // any. The domino effect will ensure that every thread
                    // will quit.
                    self.send_quit();
                    return None;
                }
                None => {
                    if self.deactivate_worker() == 0 {
                        // If deactivate_worker() returns 0, every worker thread
                        // is currently within the critical section between the
                        // acquire in deactivate_worker() and the release in
                        // activate_worker() below.  For this to happen, every
                        // worker's local deque must be simultaneously empty,
                        // meaning there is no more work left at all.
                        self.send_quit();
                        return None;
                    }
                    // Wait for next `Work` or `Quit` message.
                    loop {
                        if let Some(v) = self.recv() {
                            self.activate_worker();
                            value = Some(v);
                            break;
                        }
                        // Our stack isn't blocking. Instead of burning the
                        // CPU waiting, we let the thread sleep for a bit. In
                        // general, this tends to only occur once the search is
                        // approaching termination.
                        let dur = std::time::Duration::from_millis(1);
                        std::thread::sleep(dur);
                    }
                }
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn get_work(&mut self) -> Option<Work> {
        let mut value = self.recv();
        loop {
            // Simulate a priority channel: If quit_now flag is set, we can
            // receive only quit messages.
            if self.is_quit_now() {
                value = Some(Message::Quit)
            }
            match value {
                Some(Message::Work(work)) => {
                    return Some(work);
                }
                Some(Message::Quit) => {
                    // Repeat quit message to wake up sleeping threads, if
                    // any. The domino effect will ensure that every thread
                    // will quit.
                    self.send_quit();
                    return None;
                }
                None => {
                    if self.deactivate_worker() == 0 {
                        // If deactivate_worker() returns 0, every worker thread
                        // is currently within the critical section between the
                        // acquire in deactivate_worker() and the release in
                        // activate_worker() below.  For this to happen, every
                        // worker's local deque must be simultaneously empty,
                        // meaning there is no more work left at all.
                        self.send_quit();
                        return None;
                    }
                    // Wait for next `Work` or `Quit` message.
                    loop {
                        if self.is_quit_now() {
                            return None;
                        }
                        if let Some(v) = self.recv() {
                            self.activate_worker();
                            value = Some(v);
                            break;
                        }
                        // Our stack isn't blocking. Instead of burning the
                        // CPU waiting, we let the thread sleep for a bit. In
                        // general, this tends to only occur once the search is
                        // approaching termination.
                        let dur = std::time::Duration::from_millis(1);
                        std::thread::sleep(dur);
                    }
                }
            }
        }
    }
```


---

### 🔹 Commit #08: `241b87b3`
- **完整 Hash**: `241b87b3377136659ef0f57948b8e0739e9a691b`
- **說明 (Ground Truth)**: ignore: support `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` for `core.excludesFile`
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/gitignore.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:160, E:236, A:0) ➔ After(N:175, E:267, A:0)
- **差分統計**: +Nodes: 20, -Nodes: 5, +Edges: 45, -Edges: 14, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `gitconfig_global_env_contents()
        .and_then(|x| parse_excludes_file(&x))
        .or_else(|| {
            gitconfig_home_contents().and_then(|x| parse_excludes_file(&x))
        })
        .or_else (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `gitconfig_global_env_contents()
        .and_then(|x| parse_excludes_file(&x))
        .or_else (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `std::env::var_os("XDG_CONFIG_HOME")
        .map(PathBuf::from)
        .filter(|x| !x.as_os_str().is_empty())
        .or_else(|| home_dir().map(|p| p.join(".config")))
        .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `std::env::var_os("XDG_CONFIG_HOME")
        .map(PathBuf::from)
        .filter(|x| !x.as_os_str().is_empty())
        .or_else (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `gitconfig_system_contents` (FUNCTION_DEF)
  • + [新增節點] `gitconfig_system_contents().and_then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `gitconfig_global_env_contents()
        .and_then(|x| parse_excludes_file(&x))
        .or_else(|| {
            gitconfig_home_contents().and_then(|x| parse_excludes_file(&x))
        })
        .or_else(|| {
            gitconfig_xdg_contents().and_then(|x| parse_excludes_file(&x))
        })
        // System-level config has the lowest priority for core.excludesFile.
        // GIT_CONFIG_SYSTEM overrides the default /etc/gitconfig path.
        .or_else(|| {
            gitconfig_system_contents().and_then(|x| parse_excludes_file(&x))
        })
        .or_else (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `File::open(path).ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `std::env::var_os("GIT_CONFIG_SYSTEM")
        .map(PathBuf::from)
        .filter(|x| !x.as_os_str().is_empty())
        .unwrap_or_else (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `std::env::var_os("GIT_CONFIG_GLOBAL").map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `gitconfig_global_env_contents()
        .and_then(|x| parse_excludes_file(&x))
        .or_else(|| {
            gitconfig_home_contents().and_then(|x| parse_excludes_file(&x))
        })
        .or_else(|| {
            gitconfig_xdg_contents().and_then(|x| parse_excludes_file(&x))
        })
        // System-level config has the lowest priority for core.excludesFile.
        // GIT_CONFIG_SYSTEM overrides the default /etc/gitconfig path.
        .or_else (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `std::env::var_os("GIT_CONFIG_SYSTEM")
        .map(PathBuf::from)
        .filter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `File::open(home.join(".gitconfig")).ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `std::env::var_os("GIT_CONFIG_SYSTEM")
        .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `x.as_os_str (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 69 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `gitconfig_xdg_contents()`
- **變更前簽章 (Before)**: `fn gitconfig_xdg_contents()` (L603~L614)
- **變更後簽章 (After)**: `fn gitconfig_xdg_contents()` (L638~L647)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn gitconfig_xdg_contents() -> Option<Vec<u8>> {
    let path = std::env::var_os("XDG_CONFIG_HOME")
        .and_then(|x| if x.is_empty() { None } else { Some(PathBuf::from(x)) })
        .or_else(|| home_dir().map(|p| p.join(".config")))
        .map(|x| x.join("git/config"));
    let mut file = match path.and_then(|p| File::open(p).ok()) {
        None => return None,
        Some(file) => BufReader::new(file),
    };
    let mut contents = vec![];
    file.read_to_end(&mut contents).ok().map(|_| contents)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn gitconfig_xdg_contents() -> Option<Vec<u8>> {
    let path = std::env::var_os("XDG_CONFIG_HOME")
        .map(PathBuf::from)
        .filter(|x| !x.as_os_str().is_empty())
        .or_else(|| home_dir().map(|p| p.join(".config")))
        .map(|x| x.join("git/config"))?;
    let mut file = BufReader::new(File::open(path).ok()?);
    let mut contents = vec![];
    file.read_to_end(&mut contents).ok().map(|_| contents)
}
```

### 🔹 函式: `gitconfig_excludes_path()`
- **變更前簽章 (Before)**: `fn gitconfig_excludes_path()` (L570~L584)
- **變更後簽章 (After)**: `fn gitconfig_excludes_path()` (L581~L600)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn gitconfig_excludes_path() -> Option<PathBuf> {
    // git supports $HOME/.gitconfig and $XDG_CONFIG_HOME/git/config. Notably,
    // both can be active at the same time, where $HOME/.gitconfig takes
    // precedent. So if $HOME/.gitconfig defines a `core.excludesFile`, then
    // we're done.
    match gitconfig_home_contents().and_then(|x| parse_excludes_file(&x)) {
        Some(path) => return Some(path),
        None => {}
    }
    match gitconfig_xdg_contents().and_then(|x| parse_excludes_file(&x)) {
        Some(path) => return Some(path),
        None => {}
    }
    excludes_file_default()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn gitconfig_excludes_path() -> Option<PathBuf> {
    // When GIT_CONFIG_GLOBAL is set, it replaces both $HOME/.gitconfig and
    // $XDG_CONFIG_HOME/git/config (per git 2.32+). Otherwise, git supports
    // $HOME/.gitconfig and $XDG_CONFIG_HOME/git/config simultaneously, where
    // $HOME/.gitconfig takes precedent.
    gitconfig_global_env_contents()
        .and_then(|x| parse_excludes_file(&x))
        .or_else(|| {
            gitconfig_home_contents().and_then(|x| parse_excludes_file(&x))
        })
        .or_else(|| {
            gitconfig_xdg_contents().and_then(|x| parse_excludes_file(&x))
        })
        // System-level config has the lowest priority for core.excludesFile.
        // GIT_CONFIG_SYSTEM overrides the default /etc/gitconfig path.
        .or_else(|| {
            gitconfig_system_contents().and_then(|x| parse_excludes_file(&x))
        })
        .or_else(excludes_file_default)
}
```

### 🔹 函式: `gitconfig_home_contents()`
- **變更前簽章 (Before)**: `fn gitconfig_home_contents()` (L588~L599)
- **變更後簽章 (After)**: `fn gitconfig_home_contents()` (L629~L634)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn gitconfig_home_contents() -> Option<Vec<u8>> {
    let home = match home_dir() {
        None => return None,
        Some(home) => home,
    };
    let mut file = match File::open(home.join(".gitconfig")) {
        Err(_) => return None,
        Ok(file) => BufReader::new(file),
    };
    let mut contents = vec![];
    file.read_to_end(&mut contents).ok().map(|_| contents)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn gitconfig_home_contents() -> Option<Vec<u8>> {
    let home = home_dir()?;
    let mut file = BufReader::new(File::open(home.join(".gitconfig")).ok()?);
    let mut contents = vec![];
    file.read_to_end(&mut contents).ok().map(|_| contents)
}
```

### 🔹 函式: `excludes_file_default()`
- **變更前簽章 (Before)**: `fn excludes_file_default()` (L619~L624)
- **變更後簽章 (After)**: `fn excludes_file_default()` (L652~L658)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn excludes_file_default() -> Option<PathBuf> {
    std::env::var_os("XDG_CONFIG_HOME")
        .and_then(|x| if x.is_empty() { None } else { Some(PathBuf::from(x)) })
        .or_else(|| home_dir().map(|p| p.join(".config")))
        .map(|x| x.join("git/ignore"))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn excludes_file_default() -> Option<PathBuf> {
    std::env::var_os("XDG_CONFIG_HOME")
        .map(PathBuf::from)
        .filter(|x| !x.as_os_str().is_empty())
        .or_else(|| home_dir().map(|p| p.join(".config")))
        .map(|x| x.join("git/ignore"))
}
```


---

### 🔹 Commit #09: `b6849dae`
- **完整 Hash**: `b6849daee84a67b42b0844b2f6a91e47c24705b1`
- **說明 (Ground Truth)**: ignore/walk: add `WalkBuilder::empty` and `WalkBuilder::from_iter`
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/walk.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:389, E:691, A:0) ➔ After(N:395, E:711, A:0)
- **差分統計**: +Nodes: 6, -Nodes: 0, +Edges: 22, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Walk::from_iter` (FUNCTION_DEF)
  • + [新增節點] `empty` (FUNCTION_DEF)
  • + [新增節點] `paths.into_iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `WalkBuilder::from_iter` (FUNCTION_DEF)
  • + [新增節點] `WalkBuilder::empty` (FUNCTION_DEF)
  • + [新增節點] `from_iter` (FUNCTION_DEF)
  • + [新增呼叫邊] `WalkBuilder::new` ──[CALLS]──> `WalkBuilder::from_iter`
  • + [新增呼叫邊] `WalkBuilder::empty` ──[CALLS]──> `vec! (Macro)`
  • + [新增呼叫邊] `WalkBuilder::empty` ──[CALLS]──> `WalkBuilder::new`
  • + [新增呼叫邊] `WalkBuilder::from_iter` ──[CALLS]──> `WalkBuilder::empty`
  • + [新增呼叫邊] `WalkBuilder::from_iter` ──[CALLS]──> `paths.into_iter (External/Unresolved)`
  • + [新增呼叫邊] `WalkBuilder::from_iter` ──[CALLS]──> `WalkBuilder::add`
  • + [新增呼叫邊] `Walk::from_iter` ──[CALLS]──> `FnBuilder::build`
  • + [新增呼叫邊] `Walk::from_iter` ──[CALLS]──> `WalkBuilder::from_iter`
  • + [新增呼叫邊] `empty` ──[CALLS]──> `tmpdir`
  • _... 以及其餘 15 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `WalkBuilder::new()`
- **變更前簽章 (Before)**: `fn WalkBuilder::new(path: P)` (L551~L566)
- **變更後簽章 (After)**: `fn WalkBuilder::new(path: P)` (L551~L553)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn new<P: AsRef<Path>>(path: P) -> WalkBuilder {
        WalkBuilder {
            paths: vec![path.as_ref().to_path_buf()],
            ig_builder: IgnoreBuilder::new(),
            max_depth: None,
            min_depth: None,
            max_filesize: None,
            follow_links: false,
            same_file_system: false,
            sorter: None,
            threads: 0,
            skip: None,
            filter: None,
            global_gitignores_relative_to: OnceLock::new(),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn new<P: AsRef<Path>>(path: P) -> WalkBuilder {
        WalkBuilder::from_iter([path])
    }
```


---

### 🔹 Commit #10: `9548e86b`
- **完整 Hash**: `9548e86b14f1aa853911239f439e27a20c10fb69`
- **說明 (Ground Truth)**: ignore/types: add PKGBUILD type
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/default_types.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:7, E:6, A:0) ➔ After(N:7, E:6, A:0)
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

### 🔹 函式: `DEFAULT_TYPES()`
- **變更前簽章 (Before)**: `[Module State] DEFAULT_TYPES` (L12~L345)
- **變更後簽章 (After)**: `[Module State] DEFAULT_TYPES` (L12~L346)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) const DEFAULT_TYPES: &[(&[&str], &[&str])] = &[
    (&["ada"], &["*.adb", "*.ads"]),
    (&["agda"], &["*.agda", "*.lagda"]),
    (&["aidl"], &["*.aidl"]),
    (&["alire"], &["alire.toml"]),
    (&["amake"], &["*.mk", "*.bp"]),
    (&["asciidoc"], &["*.adoc", "*.asc", "*.asciidoc"]),
    (&["asm"], &["*.asm", "*.s", "*.S"]),
    (&["asp"], &[
        "*.aspx", "*.aspx.cs", "*.aspx.vb", "*.ascx", "*.ascx.cs",
        "*.ascx.vb", "*.asp"
    ]),
    (&["ats"], &["*.ats", "*.dats", "*.sats", "*.hats"]),
    (&["avro"], &["*.avdl", "*.avpr", "*.avsc"]),
    (&["awk"], &["*.awk"]),
    (&["bat", "batch"], &["*.bat"]),
    (&["bazel"], &[
        "*.bazel", "*.bzl", "*.BUILD", "*.bazelrc", "BUILD", "MODULE.bazel",
        "WORKSPACE", "WORKSPACE.bazel", "WORKSPACE.bzlmod",
    ]),
    (&["bitbake"], &["*.bb", "*.bbappend", "*.bbclass", "*.conf", "*.inc"]),
    (&["boxlang"], &["*.bx", "*.bxm", "*.bxs"]),
    (&["brotli"], &["*.br"]),
    (&["buildstream"], &["*.bst"]),
    (&["bzip2"], &["*.bz2", "*.tbz2"]),
    (&["c"], &["*.[chH]", "*.[chH].in", "*.cats"]),
    (&["cabal"], &["*.cabal"]),
    (&["candid"], &["*.did"]),
    (&["carp"], &["*.carp"]),
    (&["cbor"], &["*.cbor"]),
    (&["ceylon"], &["*.ceylon"]),
    (&["cfml"], &["*.cfc", "*.cfm"]),
    (&["clojure"], &["*.clj", "*.cljc", "*.cljs", "*.cljx"]),
    (&["cmake"], &["*.cmake", "CMakeLists.txt"]),
    (&["cmd"], &["*.bat", "*.cmd"]),
    (&["cml"], &["*.cml"]),
    (&["coffeescript"], &["*.coffee"]),
    (&["config"], &["*.cfg", "*.conf", "*.config", "*.ini"]),
    (&["container"], &["*Containerfile*", "*Dockerfile*"]),
    (&["coq"], &["*.v"]),
    (&["cpp"], &[
        "*.[ChH]", "*.cc", "*.[ch]pp", "*.[ch]xx", "*.hh",  "*.inl",
        "*.[ChH].in", "*.cc.in", "*.[ch]pp.in", "*.[ch]xx.in", "*.hh.in",
    ]),
    (&["creole"], &["*.creole"]),
    (&["crystal"], &["Projectfile", "*.cr", "*.ecr", "shard.yml"]),
    (&["cs"], &["*.cs"]),
    (&["csharp"], &["*.cs"]),
    (&["cshtml"], &["*.cshtml"]),
    (&["csproj"], &["*.csproj"]),
    (&["css"], &["*.css", "*.scss"]),
    (&["csv"], &["*.csv"]),
    (&["cuda"], &["*.cu", "*.cuh"]),
    (&["cython"], &["*.pyx", "*.pxi", "*.pxd"]),
    (&["d"], &["*.d"]),
    (&["dart"], &["*.dart"]),
    (&["devicetree"], &["*.dts", "*.dtsi", "*.dtso"]),
    (&["dhall"], &["*.dhall"]),
    (&["diff"], &["*.patch", "*.diff"]),
    (&["dita"], &["*.dita", "*.ditamap", "*.ditaval"]),
    (&["docker"], &["*Dockerfile*"]),
    (&["dockercompose"], &["docker-compose.yml", "docker-compose.*.yml"]),
    (&["dts"], &["*.dts", "*.dtsi"]),
    (&["dvc"], &["Dvcfile", "*.dvc"]),
    (&["ebuild"], &["*.ebuild", "*.eclass"]),
    (&["edn"], &["*.edn"]),
    (&["elisp"], &["*.el"]),
    (&["elixir"], &["*.ex", "*.eex", "*.exs", "*.heex", "*.leex", "*.livemd"]),
    (&["elm"], &["*.elm"]),
    (&["erb"], &["*.erb"]),
    (&["erlang"], &["*.erl", "*.hrl"]),
    (&["fennel"], &["*.fnl"]),
    (&["fidl"], &["*.fidl"]),
    (&["fish"], &["*.fish"]),
    (&["flatbuffers"], &["*.fbs"]),
    (&["fortran"], &[
        "*.f", "*.F", "*.f77", "*.F77", "*.pfo",
        "*.f90", "*.F90", "*.f95", "*.F95",
    ]),
    (&["fsharp"], &["*.fs", "*.fsx", "*.fsi"]),
    (&["fut"], &["*.fut"]),
    (&["gap"], &["*.g", "*.gap", "*.gi", "*.gd", "*.tst"]),
    (&["gdscript"], &["*.gd"]),
    (&["gleam"], &["*.gleam"]),
    (&["gn"], &["*.gn", "*.gni"]),
    (&["go"], &["*.go"]),
    (&["gprbuild"], &["*.gpr"]),
    (&["gradle"], &[
        "*.gradle", "*.gradle.kts", "gradle.properties", "gradle-wrapper.*",
        "gradlew", "gradlew.bat",
    ]),
    (&["graphql"], &["*.graphql", "*.graphqls"]),
    (&["groovy"], &["*.groovy", "*.gradle"]),
    (&["gzip"], &["*.gz", "*.tgz"]),
    (&["h"], &["*.h", "*.hh", "*.hpp"]),
    (&["haml"], &["*.haml"]),
    (&["hare"], &["*.ha"]),
    (&["haskell"], &["*.hs", "*.lhs", "*.cpphs", "*.c2hs", "*.hsc"]),
    (&["hbs"], &["*.hbs"]),
    (&["hs"], &["*.hs", "*.lhs"]),
    (&["html"], &["*.htm", "*.html", "*.ejs"]),
    (&["hurl"], &["*.hurl"]),
    (&["hy"], &["*.hy"]),
    (&["idris"], &["*.idr", "*.lidr"]),
    (&["janet"], &["*.janet"]),
    (&["java"], &["*.java", "*.jsp", "*.jspx", "*.properties"]),
    (&["jinja"], &["*.j2", "*.jinja", "*.jinja2"]),
    (&["jl"], &["*.jl"]),
    (&["js"], &["*.js", "*.jsx", "*.vue", "*.cjs", "*.mjs"]),
    (&["json"], &["*.json", "composer.lock", "*.sarif"]),
    (&["jsonl"], &["*.jsonl"]),
    (&["julia"], &["*.jl"]),
    (&["jupyter"], &["*.ipynb", "*.jpynb"]),
    (&["k"], &["*.k"]),
    (&["kconfig"], &["Kconfig", "Kconfig.*"]),
    (&["kotlin"], &["*.kt", "*.kts"]),
    (&["lean"], &["*.lean"]),
    (&["less"], &["*.less"]),
    (&["license"], &[
        // General
        "COPYING", "COPYING[.-]*",
        "COPYRIGHT", "COPYRIGHT[.-]*",
        "EULA", "EULA[.-]*",
        "licen[cs]e", "licen[cs]e.*",
        "LICEN[CS]E", "LICEN[CS]E[.-]*", "*[.-]LICEN[CS]E*",
        "NOTICE", "NOTICE[.-]*",
        "PATENTS", "PATENTS[.-]*",
        "UNLICEN[CS]E", "UNLICEN[CS]E[.-]*",
        // GPL (gpl.txt, etc.)
        "agpl[.-]*",
        "gpl[.-]*",
        "lgpl[.-]*",
        // Other license-specific (APACHE-2.0.txt, etc.)
        "AGPL-*[0-9]*",
        "APACHE-*[0-9]*",
        "BSD-*[0-9]*",
        "CC-BY-*",
        "GFDL-*[0-9]*",
        "GNU-*[0-9]*",
        "GPL-*[0-9]*",
        "LGPL-*[0-9]*",
        "MIT-*[0-9]*",
        "MPL-*[0-9]*",
        "OFL-*[0-9]*",
    ]),
    (&["lilypond"], &["*.ly", "*.ily"]),
    (&["lisp"], &["*.el", "*.jl", "*.lisp", "*.lsp", "*.sc", "*.scm"]),
    (&["llvm"], &["*.ll"]),
    (&["lock"], &["*.lock", "package-lock.json"]),
    (&["log"], &["*.log"]),
    (&["lua"], &["*.lua"]),
    (&["lz4"], &["*.lz4"]),
    (&["lzma"], &["*.lzma"]),
    (&["m4"], &["*.ac", "*.m4"]),
    (&["make"], &[
        "[Gg][Nn][Uu]makefile", "[Mm]akefile",
        "[Gg][Nn][Uu]makefile.am", "[Mm]akefile.am",
        "[Gg][Nn][Uu]makefile.in", "[Mm]akefile.in",
        "Makefile.*",
        "*.mk", "*.mak"
    ]),
    (&["mako"], &["*.mako", "*.mao"]),
    (&["man"], &["*.[0-9lnpx]", "*.[0-9][cEFMmpSx]"]),
    (&["markdown", "md"], &[
        "*.markdown",
        "*.md",
        "*.mdown",
        "*.mdwn",
        "*.mkd",
        "*.mkdn",
        "*.mdx",
    ]),
    (&["matlab"], &["*.m"]),
    (&["meson"], &["meson.build", "meson_options.txt", "meson.options"]),
    (&["minified"], &["*.min.html", "*.min.css", "*.min.js"]),
    (&["mint"], &["*.mint"]),
    (&["mk"], &["mkfile"]),
    (&["ml"], &["*.ml"]),
    (&["mojo"], &["*.mojo"]),
    (&["motoko"], &["*.mo"]),
    (&["msbuild"], &[
        "*.csproj", "*.fsproj", "*.vcxproj", "*.proj", "*.props", "*.targets",
        "*.sln", "*.slnf"
    ]),
    (&["nim"], &["*.nim", "*.nimf", "*.nimble", "*.nims"]),
    (&["nix"], &["*.nix"]),
    (&["objc"], &["*.h", "*.m"]),
    (&["objcpp"], &["*.h", "*.mm"]),
    (&["ocaml"], &["*.ml", "*.mli", "*.mll", "*.mly"]),
    (&["org"], &["*.org", "*.org_archive"]),
    (&["pants"], &["BUILD"]),
    (&["pascal"], &["*.pas", "*.dpr", "*.lpr", "*.pp", "*.inc"]),
    (&["pdf"], &["*.pdf"]),
    (&["perl"], &["*.perl", "*.pl", "*.PL", "*.plh", "*.plx", "*.pm", "*.t"]),
    (&["php"], &[
        // note that PHP 6 doesn't exist
        // See: https://wiki.php.net/rfc/php6
        "*.php", "*.php3", "*.php4", "*.php5", "*.php7", "*.php8",
        "*.pht", "*.phtml"
    ]),
    (&["po"], &["*.po"]),
    (&["pod"], &["*.pod"]),
    (&["postscript"], &["*.eps", "*.ps"]),
    (&["prolog"], &["*.pl", "*.pro", "*.prolog", "*.P"]),
    (&["proto", "protobuf"], &["*.proto"]),
    (&["ps"], &["*.cdxml", "*.ps1", "*.ps1xml", "*.psd1", "*.psm1"]),
    (&["puppet"], &["*.epp", "*.erb", "*.pp", "*.rb"]),
    (&["purs"], &["*.purs"]),
    (&["py", "python"], &["*.py", "*.pyi"]),
    (&["qmake"], &["*.pro", "*.pri", "*.prf"]),
    (&["qml"], &["*.qml"]),
    (&["qrc"], &["*.qrc"]),
    (&["qui"], &["*.ui"]),
    (&["r"], &["*.R", "*.r", "*.Rmd", "*.rmd", "*.Rnw", "*.rnw"]),
    (&["racket"], &["*.rkt"]),
    (&["raku"], &[
        "*.raku", "*.rakumod", "*.rakudoc", "*.rakutest",
        "*.p6", "*.pl6", "*.pm6"
    ]),
    (&["rdoc"], &["*.rdoc"]),
    (&["readme"], &["README*", "*README"]),
    (&["reasonml"], &["*.re", "*.rei"]),
    (&["red"], &["*.r", "*.red", "*.reds"]),
    (&["rescript"], &["*.res", "*.resi"]),
    (&["robot"], &["*.robot"]),
    (&["rocq"], &["*.v"]),
    (&["rst"], &["*.rst"]),
    (&["ruby"], &[
        // Idiomatic files
        "config.ru", "Gemfile", ".irbrc", "Rakefile",
        // Extensions
        "*.gemspec", "*.rb", "*.rbw", "*.rake"
    ]),
    (&["rust"], &["*.rs"]),
    (&["sass"], &["*.sass", "*.scss"]),
    (&["scala"], &["*.scala", "*.sbt"]),
    (&["scdoc"], &["*.scd", "*.scdoc"]),
    (&["seed7"], &["*.sd7", "*.s7i"]),
    (&["sh"], &[
        // Portable/misc. init files
        ".env", ".login", ".logout", ".profile", "profile",
        // bash-specific init files
        ".bash_login", "bash_login",
        ".bash_logout", "bash_logout",
        ".bash_profile", "bash_profile",
        ".bashrc", "bashrc", "*.bashrc",
        // csh-specific init files
        ".cshrc", "*.cshrc",
        // ksh-specific init files
        ".kshrc", "*.kshrc",
        // tcsh-specific init files
        ".tcshrc",
        // zsh-specific init files
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        // Extensions
        "*.bash", "*.csh", "*.env", "*.ksh", "*.sh", "*.tcsh", "*.zsh",
    ]),
    (&["slim"], &["*.skim", "*.slim", "*.slime"]),
    (&["smarty"], &["*.tpl"]),
    (&["sml"], &["*.sml", "*.sig"]),
    (&["solidity"], &["*.sol"]),
    (&["soy"], &["*.soy"]),
    (&["spark"], &["*.spark"]),
    (&["spec"], &["*.spec"]),
    (&["sql"], &["*.sql", "*.psql"]),
    (&["ssa"], &["*.ssa"]),
    (&["stylus"], &["*.styl"]),
    (&["sv"], &["*.v", "*.vg", "*.sv", "*.svh", "*.h"]),
    (&["svelte"], &["*.svelte", "*.svelte.ts"]),
    (&["svg"], &["*.svg"]),
    (&["swift"], &["*.swift"]),
    (&["swig"], &["*.def", "*.i"]),
    (&["systemd"], &[
        "*.automount", "*.conf", "*.device", "*.link", "*.mount", "*.path",
        "*.scope", "*.service", "*.slice", "*.socket", "*.swap", "*.target",
        "*.timer",
    ]),
    (&["taskpaper"], &["*.taskpaper"]),
    (&["tcl"], &["*.tcl"]),
    (&["tex"], &["*.tex", "*.ltx", "*.cls", "*.sty", "*.bib", "*.dtx", "*.ins"]),
    (&["texinfo"], &["*.texi"]),
    (&["textile"], &["*.textile"]),
    (&["tf"], &[
        "*.tf", "*.tf.json", "*.tfvars", "*.tfvars.json",
        "*.terraformrc", "terraform.rc", "*.tfrc", "*.terraform.lock.hcl",
    ]),
    (&["thrift"], &["*.thrift"]),
    (&["toml"], &["*.toml", "Cargo.lock"]),
    (&["ts", "typescript"], &["*.ts", "*.tsx", "*.cts", "*.mts"]),
    (&["twig"], &["*.twig"]),
    (&["txt"], &["*.txt"]),
    (&["typoscript"], &["*.typoscript", "*.ts"]),
    (&["typst"], &["*.typ"]),
    (&["usd"], &["*.usd", "*.usda", "*.usdc"]),
    (&["v"], &["*.v", "*.vsh"]),
    (&["vala"], &["*.vala"]),
    (&["vb"], &["*.vb"]),
    (&["vcl"], &["*.vcl"]),
    (&["verilog"], &["*.v", "*.vh", "*.sv", "*.svh"]),
    (&["vhdl"], &["*.vhd", "*.vhdl"]),
    (&["vim"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vimscript"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vue"], &["*.vue"]),
    (&["webidl"], &["*.idl", "*.webidl", "*.widl"]),
    (&["wgsl"], &["*.wgsl"]),
    (&["wiki"], &["*.mediawiki", "*.wiki"]),
    (&["xml"], &[
        "*.xml", "*.xml.dist", "*.dtd", "*.xsl", "*.xslt", "*.xsd", "*.xjb",
        "*.rng", "*.sch", "*.xhtml",
    ]),
    (&["xz"], &["*.xz", "*.txz"]),
    (&["yacc"], &["*.y"]),
    (&["yaml"], &["*.yaml", "*.yml"]),
    (&["yang"], &["*.yang"]),
    (&["z"], &["*.Z"]),
    (&["zig"], &["*.zig"]),
    (&["zsh"], &[
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        "*.zsh",
    ]),
    (&["zstd"], &["*.zst", "*.zstd"]),
];
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) const DEFAULT_TYPES: &[(&[&str], &[&str])] = &[
    (&["ada"], &["*.adb", "*.ads"]),
    (&["agda"], &["*.agda", "*.lagda"]),
    (&["aidl"], &["*.aidl"]),
    (&["alire"], &["alire.toml"]),
    (&["amake"], &["*.mk", "*.bp"]),
    (&["asciidoc"], &["*.adoc", "*.asc", "*.asciidoc"]),
    (&["asm"], &["*.asm", "*.s", "*.S"]),
    (&["asp"], &[
        "*.aspx", "*.aspx.cs", "*.aspx.vb", "*.ascx", "*.ascx.cs",
        "*.ascx.vb", "*.asp"
    ]),
    (&["ats"], &["*.ats", "*.dats", "*.sats", "*.hats"]),
    (&["avro"], &["*.avdl", "*.avpr", "*.avsc"]),
    (&["awk"], &["*.awk"]),
    (&["bat", "batch"], &["*.bat"]),
    (&["bazel"], &[
        "*.bazel", "*.bzl", "*.BUILD", "*.bazelrc", "BUILD", "MODULE.bazel",
        "WORKSPACE", "WORKSPACE.bazel", "WORKSPACE.bzlmod",
    ]),
    (&["bitbake"], &["*.bb", "*.bbappend", "*.bbclass", "*.conf", "*.inc"]),
    (&["boxlang"], &["*.bx", "*.bxm", "*.bxs"]),
    (&["brotli"], &["*.br"]),
    (&["buildstream"], &["*.bst"]),
    (&["bzip2"], &["*.bz2", "*.tbz2"]),
    (&["c"], &["*.[chH]", "*.[chH].in", "*.cats"]),
    (&["cabal"], &["*.cabal"]),
    (&["candid"], &["*.did"]),
    (&["carp"], &["*.carp"]),
    (&["cbor"], &["*.cbor"]),
    (&["ceylon"], &["*.ceylon"]),
    (&["cfml"], &["*.cfc", "*.cfm"]),
    (&["clojure"], &["*.clj", "*.cljc", "*.cljs", "*.cljx"]),
    (&["cmake"], &["*.cmake", "CMakeLists.txt"]),
    (&["cmd"], &["*.bat", "*.cmd"]),
    (&["cml"], &["*.cml"]),
    (&["coffeescript"], &["*.coffee"]),
    (&["config"], &["*.cfg", "*.conf", "*.config", "*.ini"]),
    (&["container"], &["*Containerfile*", "*Dockerfile*"]),
    (&["coq"], &["*.v"]),
    (&["cpp"], &[
        "*.[ChH]", "*.cc", "*.[ch]pp", "*.[ch]xx", "*.hh",  "*.inl",
        "*.[ChH].in", "*.cc.in", "*.[ch]pp.in", "*.[ch]xx.in", "*.hh.in",
    ]),
    (&["creole"], &["*.creole"]),
    (&["crystal"], &["Projectfile", "*.cr", "*.ecr", "shard.yml"]),
    (&["cs"], &["*.cs"]),
    (&["csharp"], &["*.cs"]),
    (&["cshtml"], &["*.cshtml"]),
    (&["csproj"], &["*.csproj"]),
    (&["css"], &["*.css", "*.scss"]),
    (&["csv"], &["*.csv"]),
    (&["cuda"], &["*.cu", "*.cuh"]),
    (&["cython"], &["*.pyx", "*.pxi", "*.pxd"]),
    (&["d"], &["*.d"]),
    (&["dart"], &["*.dart"]),
    (&["devicetree"], &["*.dts", "*.dtsi", "*.dtso"]),
    (&["dhall"], &["*.dhall"]),
    (&["diff"], &["*.patch", "*.diff"]),
    (&["dita"], &["*.dita", "*.ditamap", "*.ditaval"]),
    (&["docker"], &["*Dockerfile*"]),
    (&["dockercompose"], &["docker-compose.yml", "docker-compose.*.yml"]),
    (&["dts"], &["*.dts", "*.dtsi"]),
    (&["dvc"], &["Dvcfile", "*.dvc"]),
    (&["ebuild"], &["*.ebuild", "*.eclass"]),
    (&["edn"], &["*.edn"]),
    (&["elisp"], &["*.el"]),
    (&["elixir"], &["*.ex", "*.eex", "*.exs", "*.heex", "*.leex", "*.livemd"]),
    (&["elm"], &["*.elm"]),
    (&["erb"], &["*.erb"]),
    (&["erlang"], &["*.erl", "*.hrl"]),
    (&["fennel"], &["*.fnl"]),
    (&["fidl"], &["*.fidl"]),
    (&["fish"], &["*.fish"]),
    (&["flatbuffers"], &["*.fbs"]),
    (&["fortran"], &[
        "*.f", "*.F", "*.f77", "*.F77", "*.pfo",
        "*.f90", "*.F90", "*.f95", "*.F95",
    ]),
    (&["fsharp"], &["*.fs", "*.fsx", "*.fsi"]),
    (&["fut"], &["*.fut"]),
    (&["gap"], &["*.g", "*.gap", "*.gi", "*.gd", "*.tst"]),
    (&["gdscript"], &["*.gd"]),
    (&["gleam"], &["*.gleam"]),
    (&["gn"], &["*.gn", "*.gni"]),
    (&["go"], &["*.go"]),
    (&["gprbuild"], &["*.gpr"]),
    (&["gradle"], &[
        "*.gradle", "*.gradle.kts", "gradle.properties", "gradle-wrapper.*",
        "gradlew", "gradlew.bat",
    ]),
    (&["graphql"], &["*.graphql", "*.graphqls"]),
    (&["groovy"], &["*.groovy", "*.gradle"]),
    (&["gzip"], &["*.gz", "*.tgz"]),
    (&["h"], &["*.h", "*.hh", "*.hpp"]),
    (&["haml"], &["*.haml"]),
    (&["hare"], &["*.ha"]),
    (&["haskell"], &["*.hs", "*.lhs", "*.cpphs", "*.c2hs", "*.hsc"]),
    (&["hbs"], &["*.hbs"]),
    (&["hs"], &["*.hs", "*.lhs"]),
    (&["html"], &["*.htm", "*.html", "*.ejs"]),
    (&["hurl"], &["*.hurl"]),
    (&["hy"], &["*.hy"]),
    (&["idris"], &["*.idr", "*.lidr"]),
    (&["janet"], &["*.janet"]),
    (&["java"], &["*.java", "*.jsp", "*.jspx", "*.properties"]),
    (&["jinja"], &["*.j2", "*.jinja", "*.jinja2"]),
    (&["jl"], &["*.jl"]),
    (&["js"], &["*.js", "*.jsx", "*.vue", "*.cjs", "*.mjs"]),
    (&["json"], &["*.json", "composer.lock", "*.sarif"]),
    (&["jsonl"], &["*.jsonl"]),
    (&["julia"], &["*.jl"]),
    (&["jupyter"], &["*.ipynb", "*.jpynb"]),
    (&["k"], &["*.k"]),
    (&["kconfig"], &["Kconfig", "Kconfig.*"]),
    (&["kotlin"], &["*.kt", "*.kts"]),
    (&["lean"], &["*.lean"]),
    (&["less"], &["*.less"]),
    (&["license"], &[
        // General
        "COPYING", "COPYING[.-]*",
        "COPYRIGHT", "COPYRIGHT[.-]*",
        "EULA", "EULA[.-]*",
        "licen[cs]e", "licen[cs]e.*",
        "LICEN[CS]E", "LICEN[CS]E[.-]*", "*[.-]LICEN[CS]E*",
        "NOTICE", "NOTICE[.-]*",
        "PATENTS", "PATENTS[.-]*",
        "UNLICEN[CS]E", "UNLICEN[CS]E[.-]*",
        // GPL (gpl.txt, etc.)
        "agpl[.-]*",
        "gpl[.-]*",
        "lgpl[.-]*",
        // Other license-specific (APACHE-2.0.txt, etc.)
        "AGPL-*[0-9]*",
        "APACHE-*[0-9]*",
        "BSD-*[0-9]*",
        "CC-BY-*",
        "GFDL-*[0-9]*",
        "GNU-*[0-9]*",
        "GPL-*[0-9]*",
        "LGPL-*[0-9]*",
        "MIT-*[0-9]*",
        "MPL-*[0-9]*",
        "OFL-*[0-9]*",
    ]),
    (&["lilypond"], &["*.ly", "*.ily"]),
    (&["lisp"], &["*.el", "*.jl", "*.lisp", "*.lsp", "*.sc", "*.scm"]),
    (&["llvm"], &["*.ll"]),
    (&["lock"], &["*.lock", "package-lock.json"]),
    (&["log"], &["*.log"]),
    (&["lua"], &["*.lua"]),
    (&["lz4"], &["*.lz4"]),
    (&["lzma"], &["*.lzma"]),
    (&["m4"], &["*.ac", "*.m4"]),
    (&["make"], &[
        "[Gg][Nn][Uu]makefile", "[Mm]akefile",
        "[Gg][Nn][Uu]makefile.am", "[Mm]akefile.am",
        "[Gg][Nn][Uu]makefile.in", "[Mm]akefile.in",
        "Makefile.*",
        "*.mk", "*.mak"
    ]),
    (&["mako"], &["*.mako", "*.mao"]),
    (&["man"], &["*.[0-9lnpx]", "*.[0-9][cEFMmpSx]"]),
    (&["markdown", "md"], &[
        "*.markdown",
        "*.md",
        "*.mdown",
        "*.mdwn",
        "*.mkd",
        "*.mkdn",
        "*.mdx",
    ]),
    (&["matlab"], &["*.m"]),
    (&["meson"], &["meson.build", "meson_options.txt", "meson.options"]),
    (&["minified"], &["*.min.html", "*.min.css", "*.min.js"]),
    (&["mint"], &["*.mint"]),
    (&["mk"], &["mkfile"]),
    (&["ml"], &["*.ml"]),
    (&["mojo"], &["*.mojo"]),
    (&["motoko"], &["*.mo"]),
    (&["msbuild"], &[
        "*.csproj", "*.fsproj", "*.vcxproj", "*.proj", "*.props", "*.targets",
        "*.sln", "*.slnf"
    ]),
    (&["nim"], &["*.nim", "*.nimf", "*.nimble", "*.nims"]),
    (&["nix"], &["*.nix"]),
    (&["objc"], &["*.h", "*.m"]),
    (&["objcpp"], &["*.h", "*.mm"]),
    (&["ocaml"], &["*.ml", "*.mli", "*.mll", "*.mly"]),
    (&["org"], &["*.org", "*.org_archive"]),
    (&["pants"], &["BUILD"]),
    (&["pascal"], &["*.pas", "*.dpr", "*.lpr", "*.pp", "*.inc"]),
    (&["pdf"], &["*.pdf"]),
    (&["perl"], &["*.perl", "*.pl", "*.PL", "*.plh", "*.plx", "*.pm", "*.t"]),
    (&["php"], &[
        // note that PHP 6 doesn't exist
        // See: https://wiki.php.net/rfc/php6
        "*.php", "*.php3", "*.php4", "*.php5", "*.php7", "*.php8",
        "*.pht", "*.phtml"
    ]),
    (&["pkgbuild"], &["PKGBUILD"]),
    (&["po"], &["*.po"]),
    (&["pod"], &["*.pod"]),
    (&["postscript"], &["*.eps", "*.ps"]),
    (&["prolog"], &["*.pl", "*.pro", "*.prolog", "*.P"]),
    (&["proto", "protobuf"], &["*.proto"]),
    (&["ps"], &["*.cdxml", "*.ps1", "*.ps1xml", "*.psd1", "*.psm1"]),
    (&["puppet"], &["*.epp", "*.erb", "*.pp", "*.rb"]),
    (&["purs"], &["*.purs"]),
    (&["py", "python"], &["*.py", "*.pyi"]),
    (&["qmake"], &["*.pro", "*.pri", "*.prf"]),
    (&["qml"], &["*.qml"]),
    (&["qrc"], &["*.qrc"]),
    (&["qui"], &["*.ui"]),
    (&["r"], &["*.R", "*.r", "*.Rmd", "*.rmd", "*.Rnw", "*.rnw"]),
    (&["racket"], &["*.rkt"]),
    (&["raku"], &[
        "*.raku", "*.rakumod", "*.rakudoc", "*.rakutest",
        "*.p6", "*.pl6", "*.pm6"
    ]),
    (&["rdoc"], &["*.rdoc"]),
    (&["readme"], &["README*", "*README"]),
    (&["reasonml"], &["*.re", "*.rei"]),
    (&["red"], &["*.r", "*.red", "*.reds"]),
    (&["rescript"], &["*.res", "*.resi"]),
    (&["robot"], &["*.robot"]),
    (&["rocq"], &["*.v"]),
    (&["rst"], &["*.rst"]),
    (&["ruby"], &[
        // Idiomatic files
        "config.ru", "Gemfile", ".irbrc", "Rakefile",
        // Extensions
        "*.gemspec", "*.rb", "*.rbw", "*.rake"
    ]),
    (&["rust"], &["*.rs"]),
    (&["sass"], &["*.sass", "*.scss"]),
    (&["scala"], &["*.scala", "*.sbt"]),
    (&["scdoc"], &["*.scd", "*.scdoc"]),
    (&["seed7"], &["*.sd7", "*.s7i"]),
    (&["sh"], &[
        // Portable/misc. init files
        ".env", ".login", ".logout", ".profile", "profile",
        // bash-specific init files
        ".bash_login", "bash_login",
        ".bash_logout", "bash_logout",
        ".bash_profile", "bash_profile",
        ".bashrc", "bashrc", "*.bashrc",
        // csh-specific init files
        ".cshrc", "*.cshrc",
        // ksh-specific init files
        ".kshrc", "*.kshrc",
        // tcsh-specific init files
        ".tcshrc",
        // zsh-specific init files
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        // Extensions
        "*.bash", "*.csh", "*.env", "*.ksh", "*.sh", "*.tcsh", "*.zsh",
    ]),
    (&["slim"], &["*.skim", "*.slim", "*.slime"]),
    (&["smarty"], &["*.tpl"]),
    (&["sml"], &["*.sml", "*.sig"]),
    (&["solidity"], &["*.sol"]),
    (&["soy"], &["*.soy"]),
    (&["spark"], &["*.spark"]),
    (&["spec"], &["*.spec"]),
    (&["sql"], &["*.sql", "*.psql"]),
    (&["ssa"], &["*.ssa"]),
    (&["stylus"], &["*.styl"]),
    (&["sv"], &["*.v", "*.vg", "*.sv", "*.svh", "*.h"]),
    (&["svelte"], &["*.svelte", "*.svelte.ts"]),
    (&["svg"], &["*.svg"]),
    (&["swift"], &["*.swift"]),
    (&["swig"], &["*.def", "*.i"]),
    (&["systemd"], &[
        "*.automount", "*.conf", "*.device", "*.link", "*.mount", "*.path",
        "*.scope", "*.service", "*.slice", "*.socket", "*.swap", "*.target",
        "*.timer",
    ]),
    (&["taskpaper"], &["*.taskpaper"]),
    (&["tcl"], &["*.tcl"]),
    (&["tex"], &["*.tex", "*.ltx", "*.cls", "*.sty", "*.bib", "*.dtx", "*.ins"]),
    (&["texinfo"], &["*.texi"]),
    (&["textile"], &["*.textile"]),
    (&["tf"], &[
        "*.tf", "*.tf.json", "*.tfvars", "*.tfvars.json",
        "*.terraformrc", "terraform.rc", "*.tfrc", "*.terraform.lock.hcl",
    ]),
    (&["thrift"], &["*.thrift"]),
    (&["toml"], &["*.toml", "Cargo.lock"]),
    (&["ts", "typescript"], &["*.ts", "*.tsx", "*.cts", "*.mts"]),
    (&["twig"], &["*.twig"]),
    (&["txt"], &["*.txt"]),
    (&["typoscript"], &["*.typoscript", "*.ts"]),
    (&["typst"], &["*.typ"]),
    (&["usd"], &["*.usd", "*.usda", "*.usdc"]),
    (&["v"], &["*.v", "*.vsh"]),
    (&["vala"], &["*.vala"]),
    (&["vb"], &["*.vb"]),
    (&["vcl"], &["*.vcl"]),
    (&["verilog"], &["*.v", "*.vh", "*.sv", "*.svh"]),
    (&["vhdl"], &["*.vhd", "*.vhdl"]),
    (&["vim"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vimscript"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vue"], &["*.vue"]),
    (&["webidl"], &["*.idl", "*.webidl", "*.widl"]),
    (&["wgsl"], &["*.wgsl"]),
    (&["wiki"], &["*.mediawiki", "*.wiki"]),
    (&["xml"], &[
        "*.xml", "*.xml.dist", "*.dtd", "*.xsl", "*.xslt", "*.xsd", "*.xjb",
        "*.rng", "*.sch", "*.xhtml",
    ]),
    (&["xz"], &["*.xz", "*.txz"]),
    (&["yacc"], &["*.y"]),
    (&["yaml"], &["*.yaml", "*.yml"]),
    (&["yang"], &["*.yang"]),
    (&["z"], &["*.Z"]),
    (&["zig"], &["*.zig"]),
    (&["zsh"], &[
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        "*.zsh",
    ]),
    (&["zstd"], &["*.zst", "*.zstd"]),
];
```


---

### 🔹 Commit #11: `bc3ad92b`
- **完整 Hash**: `bc3ad92b345eeddc48afff3194a5e2385e3d6a3b`
- **說明 (Ground Truth)**: ignore/types: add Rocq `.v` files
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/default_types.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:7, E:6, A:0) ➔ After(N:7, E:6, A:0)
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

### 🔹 函式: `DEFAULT_TYPES()`
- **變更前簽章 (Before)**: `[Module State] DEFAULT_TYPES` (L12~L344)
- **變更後簽章 (After)**: `[Module State] DEFAULT_TYPES` (L12~L345)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) const DEFAULT_TYPES: &[(&[&str], &[&str])] = &[
    (&["ada"], &["*.adb", "*.ads"]),
    (&["agda"], &["*.agda", "*.lagda"]),
    (&["aidl"], &["*.aidl"]),
    (&["alire"], &["alire.toml"]),
    (&["amake"], &["*.mk", "*.bp"]),
    (&["asciidoc"], &["*.adoc", "*.asc", "*.asciidoc"]),
    (&["asm"], &["*.asm", "*.s", "*.S"]),
    (&["asp"], &[
        "*.aspx", "*.aspx.cs", "*.aspx.vb", "*.ascx", "*.ascx.cs",
        "*.ascx.vb", "*.asp"
    ]),
    (&["ats"], &["*.ats", "*.dats", "*.sats", "*.hats"]),
    (&["avro"], &["*.avdl", "*.avpr", "*.avsc"]),
    (&["awk"], &["*.awk"]),
    (&["bat", "batch"], &["*.bat"]),
    (&["bazel"], &[
        "*.bazel", "*.bzl", "*.BUILD", "*.bazelrc", "BUILD", "MODULE.bazel",
        "WORKSPACE", "WORKSPACE.bazel", "WORKSPACE.bzlmod",
    ]),
    (&["bitbake"], &["*.bb", "*.bbappend", "*.bbclass", "*.conf", "*.inc"]),
    (&["boxlang"], &["*.bx", "*.bxm", "*.bxs"]),
    (&["brotli"], &["*.br"]),
    (&["buildstream"], &["*.bst"]),
    (&["bzip2"], &["*.bz2", "*.tbz2"]),
    (&["c"], &["*.[chH]", "*.[chH].in", "*.cats"]),
    (&["cabal"], &["*.cabal"]),
    (&["candid"], &["*.did"]),
    (&["carp"], &["*.carp"]),
    (&["cbor"], &["*.cbor"]),
    (&["ceylon"], &["*.ceylon"]),
    (&["cfml"], &["*.cfc", "*.cfm"]),
    (&["clojure"], &["*.clj", "*.cljc", "*.cljs", "*.cljx"]),
    (&["cmake"], &["*.cmake", "CMakeLists.txt"]),
    (&["cmd"], &["*.bat", "*.cmd"]),
    (&["cml"], &["*.cml"]),
    (&["coffeescript"], &["*.coffee"]),
    (&["config"], &["*.cfg", "*.conf", "*.config", "*.ini"]),
    (&["container"], &["*Containerfile*", "*Dockerfile*"]),
    (&["coq"], &["*.v"]),
    (&["cpp"], &[
        "*.[ChH]", "*.cc", "*.[ch]pp", "*.[ch]xx", "*.hh",  "*.inl",
        "*.[ChH].in", "*.cc.in", "*.[ch]pp.in", "*.[ch]xx.in", "*.hh.in",
    ]),
    (&["creole"], &["*.creole"]),
    (&["crystal"], &["Projectfile", "*.cr", "*.ecr", "shard.yml"]),
    (&["cs"], &["*.cs"]),
    (&["csharp"], &["*.cs"]),
    (&["cshtml"], &["*.cshtml"]),
    (&["csproj"], &["*.csproj"]),
    (&["css"], &["*.css", "*.scss"]),
    (&["csv"], &["*.csv"]),
    (&["cuda"], &["*.cu", "*.cuh"]),
    (&["cython"], &["*.pyx", "*.pxi", "*.pxd"]),
    (&["d"], &["*.d"]),
    (&["dart"], &["*.dart"]),
    (&["devicetree"], &["*.dts", "*.dtsi", "*.dtso"]),
    (&["dhall"], &["*.dhall"]),
    (&["diff"], &["*.patch", "*.diff"]),
    (&["dita"], &["*.dita", "*.ditamap", "*.ditaval"]),
    (&["docker"], &["*Dockerfile*"]),
    (&["dockercompose"], &["docker-compose.yml", "docker-compose.*.yml"]),
    (&["dts"], &["*.dts", "*.dtsi"]),
    (&["dvc"], &["Dvcfile", "*.dvc"]),
    (&["ebuild"], &["*.ebuild", "*.eclass"]),
    (&["edn"], &["*.edn"]),
    (&["elisp"], &["*.el"]),
    (&["elixir"], &["*.ex", "*.eex", "*.exs", "*.heex", "*.leex", "*.livemd"]),
    (&["elm"], &["*.elm"]),
    (&["erb"], &["*.erb"]),
    (&["erlang"], &["*.erl", "*.hrl"]),
    (&["fennel"], &["*.fnl"]),
    (&["fidl"], &["*.fidl"]),
    (&["fish"], &["*.fish"]),
    (&["flatbuffers"], &["*.fbs"]),
    (&["fortran"], &[
        "*.f", "*.F", "*.f77", "*.F77", "*.pfo",
        "*.f90", "*.F90", "*.f95", "*.F95",
    ]),
    (&["fsharp"], &["*.fs", "*.fsx", "*.fsi"]),
    (&["fut"], &["*.fut"]),
    (&["gap"], &["*.g", "*.gap", "*.gi", "*.gd", "*.tst"]),
    (&["gdscript"], &["*.gd"]),
    (&["gleam"], &["*.gleam"]),
    (&["gn"], &["*.gn", "*.gni"]),
    (&["go"], &["*.go"]),
    (&["gprbuild"], &["*.gpr"]),
    (&["gradle"], &[
        "*.gradle", "*.gradle.kts", "gradle.properties", "gradle-wrapper.*",
        "gradlew", "gradlew.bat",
    ]),
    (&["graphql"], &["*.graphql", "*.graphqls"]),
    (&["groovy"], &["*.groovy", "*.gradle"]),
    (&["gzip"], &["*.gz", "*.tgz"]),
    (&["h"], &["*.h", "*.hh", "*.hpp"]),
    (&["haml"], &["*.haml"]),
    (&["hare"], &["*.ha"]),
    (&["haskell"], &["*.hs", "*.lhs", "*.cpphs", "*.c2hs", "*.hsc"]),
    (&["hbs"], &["*.hbs"]),
    (&["hs"], &["*.hs", "*.lhs"]),
    (&["html"], &["*.htm", "*.html", "*.ejs"]),
    (&["hurl"], &["*.hurl"]),
    (&["hy"], &["*.hy"]),
    (&["idris"], &["*.idr", "*.lidr"]),
    (&["janet"], &["*.janet"]),
    (&["java"], &["*.java", "*.jsp", "*.jspx", "*.properties"]),
    (&["jinja"], &["*.j2", "*.jinja", "*.jinja2"]),
    (&["jl"], &["*.jl"]),
    (&["js"], &["*.js", "*.jsx", "*.vue", "*.cjs", "*.mjs"]),
    (&["json"], &["*.json", "composer.lock", "*.sarif"]),
    (&["jsonl"], &["*.jsonl"]),
    (&["julia"], &["*.jl"]),
    (&["jupyter"], &["*.ipynb", "*.jpynb"]),
    (&["k"], &["*.k"]),
    (&["kconfig"], &["Kconfig", "Kconfig.*"]),
    (&["kotlin"], &["*.kt", "*.kts"]),
    (&["lean"], &["*.lean"]),
    (&["less"], &["*.less"]),
    (&["license"], &[
        // General
        "COPYING", "COPYING[.-]*",
        "COPYRIGHT", "COPYRIGHT[.-]*",
        "EULA", "EULA[.-]*",
        "licen[cs]e", "licen[cs]e.*",
        "LICEN[CS]E", "LICEN[CS]E[.-]*", "*[.-]LICEN[CS]E*",
        "NOTICE", "NOTICE[.-]*",
        "PATENTS", "PATENTS[.-]*",
        "UNLICEN[CS]E", "UNLICEN[CS]E[.-]*",
        // GPL (gpl.txt, etc.)
        "agpl[.-]*",
        "gpl[.-]*",
        "lgpl[.-]*",
        // Other license-specific (APACHE-2.0.txt, etc.)
        "AGPL-*[0-9]*",
        "APACHE-*[0-9]*",
        "BSD-*[0-9]*",
        "CC-BY-*",
        "GFDL-*[0-9]*",
        "GNU-*[0-9]*",
        "GPL-*[0-9]*",
        "LGPL-*[0-9]*",
        "MIT-*[0-9]*",
        "MPL-*[0-9]*",
        "OFL-*[0-9]*",
    ]),
    (&["lilypond"], &["*.ly", "*.ily"]),
    (&["lisp"], &["*.el", "*.jl", "*.lisp", "*.lsp", "*.sc", "*.scm"]),
    (&["llvm"], &["*.ll"]),
    (&["lock"], &["*.lock", "package-lock.json"]),
    (&["log"], &["*.log"]),
    (&["lua"], &["*.lua"]),
    (&["lz4"], &["*.lz4"]),
    (&["lzma"], &["*.lzma"]),
    (&["m4"], &["*.ac", "*.m4"]),
    (&["make"], &[
        "[Gg][Nn][Uu]makefile", "[Mm]akefile",
        "[Gg][Nn][Uu]makefile.am", "[Mm]akefile.am",
        "[Gg][Nn][Uu]makefile.in", "[Mm]akefile.in",
        "Makefile.*",
        "*.mk", "*.mak"
    ]),
    (&["mako"], &["*.mako", "*.mao"]),
    (&["man"], &["*.[0-9lnpx]", "*.[0-9][cEFMmpSx]"]),
    (&["markdown", "md"], &[
        "*.markdown",
        "*.md",
        "*.mdown",
        "*.mdwn",
        "*.mkd",
        "*.mkdn",
        "*.mdx",
    ]),
    (&["matlab"], &["*.m"]),
    (&["meson"], &["meson.build", "meson_options.txt", "meson.options"]),
    (&["minified"], &["*.min.html", "*.min.css", "*.min.js"]),
    (&["mint"], &["*.mint"]),
    (&["mk"], &["mkfile"]),
    (&["ml"], &["*.ml"]),
    (&["mojo"], &["*.mojo"]),
    (&["motoko"], &["*.mo"]),
    (&["msbuild"], &[
        "*.csproj", "*.fsproj", "*.vcxproj", "*.proj", "*.props", "*.targets",
        "*.sln", "*.slnf"
    ]),
    (&["nim"], &["*.nim", "*.nimf", "*.nimble", "*.nims"]),
    (&["nix"], &["*.nix"]),
    (&["objc"], &["*.h", "*.m"]),
    (&["objcpp"], &["*.h", "*.mm"]),
    (&["ocaml"], &["*.ml", "*.mli", "*.mll", "*.mly"]),
    (&["org"], &["*.org", "*.org_archive"]),
    (&["pants"], &["BUILD"]),
    (&["pascal"], &["*.pas", "*.dpr", "*.lpr", "*.pp", "*.inc"]),
    (&["pdf"], &["*.pdf"]),
    (&["perl"], &["*.perl", "*.pl", "*.PL", "*.plh", "*.plx", "*.pm", "*.t"]),
    (&["php"], &[
        // note that PHP 6 doesn't exist
        // See: https://wiki.php.net/rfc/php6
        "*.php", "*.php3", "*.php4", "*.php5", "*.php7", "*.php8",
        "*.pht", "*.phtml"
    ]),
    (&["po"], &["*.po"]),
    (&["pod"], &["*.pod"]),
    (&["postscript"], &["*.eps", "*.ps"]),
    (&["prolog"], &["*.pl", "*.pro", "*.prolog", "*.P"]),
    (&["proto", "protobuf"], &["*.proto"]),
    (&["ps"], &["*.cdxml", "*.ps1", "*.ps1xml", "*.psd1", "*.psm1"]),
    (&["puppet"], &["*.epp", "*.erb", "*.pp", "*.rb"]),
    (&["purs"], &["*.purs"]),
    (&["py", "python"], &["*.py", "*.pyi"]),
    (&["qmake"], &["*.pro", "*.pri", "*.prf"]),
    (&["qml"], &["*.qml"]),
    (&["qrc"], &["*.qrc"]),
    (&["qui"], &["*.ui"]),
    (&["r"], &["*.R", "*.r", "*.Rmd", "*.rmd", "*.Rnw", "*.rnw"]),
    (&["racket"], &["*.rkt"]),
    (&["raku"], &[
        "*.raku", "*.rakumod", "*.rakudoc", "*.rakutest",
        "*.p6", "*.pl6", "*.pm6"
    ]),
    (&["rdoc"], &["*.rdoc"]),
    (&["readme"], &["README*", "*README"]),
    (&["reasonml"], &["*.re", "*.rei"]),
    (&["red"], &["*.r", "*.red", "*.reds"]),
    (&["rescript"], &["*.res", "*.resi"]),
    (&["robot"], &["*.robot"]),
    (&["rst"], &["*.rst"]),
    (&["ruby"], &[
        // Idiomatic files
        "config.ru", "Gemfile", ".irbrc", "Rakefile",
        // Extensions
        "*.gemspec", "*.rb", "*.rbw", "*.rake"
    ]),
    (&["rust"], &["*.rs"]),
    (&["sass"], &["*.sass", "*.scss"]),
    (&["scala"], &["*.scala", "*.sbt"]),
    (&["scdoc"], &["*.scd", "*.scdoc"]),
    (&["seed7"], &["*.sd7", "*.s7i"]),
    (&["sh"], &[
        // Portable/misc. init files
        ".env", ".login", ".logout", ".profile", "profile",
        // bash-specific init files
        ".bash_login", "bash_login",
        ".bash_logout", "bash_logout",
        ".bash_profile", "bash_profile",
        ".bashrc", "bashrc", "*.bashrc",
        // csh-specific init files
        ".cshrc", "*.cshrc",
        // ksh-specific init files
        ".kshrc", "*.kshrc",
        // tcsh-specific init files
        ".tcshrc",
        // zsh-specific init files
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        // Extensions
        "*.bash", "*.csh", "*.env", "*.ksh", "*.sh", "*.tcsh", "*.zsh",
    ]),
    (&["slim"], &["*.skim", "*.slim", "*.slime"]),
    (&["smarty"], &["*.tpl"]),
    (&["sml"], &["*.sml", "*.sig"]),
    (&["solidity"], &["*.sol"]),
    (&["soy"], &["*.soy"]),
    (&["spark"], &["*.spark"]),
    (&["spec"], &["*.spec"]),
    (&["sql"], &["*.sql", "*.psql"]),
    (&["ssa"], &["*.ssa"]),
    (&["stylus"], &["*.styl"]),
    (&["sv"], &["*.v", "*.vg", "*.sv", "*.svh", "*.h"]),
    (&["svelte"], &["*.svelte", "*.svelte.ts"]),
    (&["svg"], &["*.svg"]),
    (&["swift"], &["*.swift"]),
    (&["swig"], &["*.def", "*.i"]),
    (&["systemd"], &[
        "*.automount", "*.conf", "*.device", "*.link", "*.mount", "*.path",
        "*.scope", "*.service", "*.slice", "*.socket", "*.swap", "*.target",
        "*.timer",
    ]),
    (&["taskpaper"], &["*.taskpaper"]),
    (&["tcl"], &["*.tcl"]),
    (&["tex"], &["*.tex", "*.ltx", "*.cls", "*.sty", "*.bib", "*.dtx", "*.ins"]),
    (&["texinfo"], &["*.texi"]),
    (&["textile"], &["*.textile"]),
    (&["tf"], &[
        "*.tf", "*.tf.json", "*.tfvars", "*.tfvars.json",
        "*.terraformrc", "terraform.rc", "*.tfrc", "*.terraform.lock.hcl",
    ]),
    (&["thrift"], &["*.thrift"]),
    (&["toml"], &["*.toml", "Cargo.lock"]),
    (&["ts", "typescript"], &["*.ts", "*.tsx", "*.cts", "*.mts"]),
    (&["twig"], &["*.twig"]),
    (&["txt"], &["*.txt"]),
    (&["typoscript"], &["*.typoscript", "*.ts"]),
    (&["typst"], &["*.typ"]),
    (&["usd"], &["*.usd", "*.usda", "*.usdc"]),
    (&["v"], &["*.v", "*.vsh"]),
    (&["vala"], &["*.vala"]),
    (&["vb"], &["*.vb"]),
    (&["vcl"], &["*.vcl"]),
    (&["verilog"], &["*.v", "*.vh", "*.sv", "*.svh"]),
    (&["vhdl"], &["*.vhd", "*.vhdl"]),
    (&["vim"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vimscript"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vue"], &["*.vue"]),
    (&["webidl"], &["*.idl", "*.webidl", "*.widl"]),
    (&["wgsl"], &["*.wgsl"]),
    (&["wiki"], &["*.mediawiki", "*.wiki"]),
    (&["xml"], &[
        "*.xml", "*.xml.dist", "*.dtd", "*.xsl", "*.xslt", "*.xsd", "*.xjb",
        "*.rng", "*.sch", "*.xhtml",
    ]),
    (&["xz"], &["*.xz", "*.txz"]),
    (&["yacc"], &["*.y"]),
    (&["yaml"], &["*.yaml", "*.yml"]),
    (&["yang"], &["*.yang"]),
    (&["z"], &["*.Z"]),
    (&["zig"], &["*.zig"]),
    (&["zsh"], &[
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        "*.zsh",
    ]),
    (&["zstd"], &["*.zst", "*.zstd"]),
];
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) const DEFAULT_TYPES: &[(&[&str], &[&str])] = &[
    (&["ada"], &["*.adb", "*.ads"]),
    (&["agda"], &["*.agda", "*.lagda"]),
    (&["aidl"], &["*.aidl"]),
    (&["alire"], &["alire.toml"]),
    (&["amake"], &["*.mk", "*.bp"]),
    (&["asciidoc"], &["*.adoc", "*.asc", "*.asciidoc"]),
    (&["asm"], &["*.asm", "*.s", "*.S"]),
    (&["asp"], &[
        "*.aspx", "*.aspx.cs", "*.aspx.vb", "*.ascx", "*.ascx.cs",
        "*.ascx.vb", "*.asp"
    ]),
    (&["ats"], &["*.ats", "*.dats", "*.sats", "*.hats"]),
    (&["avro"], &["*.avdl", "*.avpr", "*.avsc"]),
    (&["awk"], &["*.awk"]),
    (&["bat", "batch"], &["*.bat"]),
    (&["bazel"], &[
        "*.bazel", "*.bzl", "*.BUILD", "*.bazelrc", "BUILD", "MODULE.bazel",
        "WORKSPACE", "WORKSPACE.bazel", "WORKSPACE.bzlmod",
    ]),
    (&["bitbake"], &["*.bb", "*.bbappend", "*.bbclass", "*.conf", "*.inc"]),
    (&["boxlang"], &["*.bx", "*.bxm", "*.bxs"]),
    (&["brotli"], &["*.br"]),
    (&["buildstream"], &["*.bst"]),
    (&["bzip2"], &["*.bz2", "*.tbz2"]),
    (&["c"], &["*.[chH]", "*.[chH].in", "*.cats"]),
    (&["cabal"], &["*.cabal"]),
    (&["candid"], &["*.did"]),
    (&["carp"], &["*.carp"]),
    (&["cbor"], &["*.cbor"]),
    (&["ceylon"], &["*.ceylon"]),
    (&["cfml"], &["*.cfc", "*.cfm"]),
    (&["clojure"], &["*.clj", "*.cljc", "*.cljs", "*.cljx"]),
    (&["cmake"], &["*.cmake", "CMakeLists.txt"]),
    (&["cmd"], &["*.bat", "*.cmd"]),
    (&["cml"], &["*.cml"]),
    (&["coffeescript"], &["*.coffee"]),
    (&["config"], &["*.cfg", "*.conf", "*.config", "*.ini"]),
    (&["container"], &["*Containerfile*", "*Dockerfile*"]),
    (&["coq"], &["*.v"]),
    (&["cpp"], &[
        "*.[ChH]", "*.cc", "*.[ch]pp", "*.[ch]xx", "*.hh",  "*.inl",
        "*.[ChH].in", "*.cc.in", "*.[ch]pp.in", "*.[ch]xx.in", "*.hh.in",
    ]),
    (&["creole"], &["*.creole"]),
    (&["crystal"], &["Projectfile", "*.cr", "*.ecr", "shard.yml"]),
    (&["cs"], &["*.cs"]),
    (&["csharp"], &["*.cs"]),
    (&["cshtml"], &["*.cshtml"]),
    (&["csproj"], &["*.csproj"]),
    (&["css"], &["*.css", "*.scss"]),
    (&["csv"], &["*.csv"]),
    (&["cuda"], &["*.cu", "*.cuh"]),
    (&["cython"], &["*.pyx", "*.pxi", "*.pxd"]),
    (&["d"], &["*.d"]),
    (&["dart"], &["*.dart"]),
    (&["devicetree"], &["*.dts", "*.dtsi", "*.dtso"]),
    (&["dhall"], &["*.dhall"]),
    (&["diff"], &["*.patch", "*.diff"]),
    (&["dita"], &["*.dita", "*.ditamap", "*.ditaval"]),
    (&["docker"], &["*Dockerfile*"]),
    (&["dockercompose"], &["docker-compose.yml", "docker-compose.*.yml"]),
    (&["dts"], &["*.dts", "*.dtsi"]),
    (&["dvc"], &["Dvcfile", "*.dvc"]),
    (&["ebuild"], &["*.ebuild", "*.eclass"]),
    (&["edn"], &["*.edn"]),
    (&["elisp"], &["*.el"]),
    (&["elixir"], &["*.ex", "*.eex", "*.exs", "*.heex", "*.leex", "*.livemd"]),
    (&["elm"], &["*.elm"]),
    (&["erb"], &["*.erb"]),
    (&["erlang"], &["*.erl", "*.hrl"]),
    (&["fennel"], &["*.fnl"]),
    (&["fidl"], &["*.fidl"]),
    (&["fish"], &["*.fish"]),
    (&["flatbuffers"], &["*.fbs"]),
    (&["fortran"], &[
        "*.f", "*.F", "*.f77", "*.F77", "*.pfo",
        "*.f90", "*.F90", "*.f95", "*.F95",
    ]),
    (&["fsharp"], &["*.fs", "*.fsx", "*.fsi"]),
    (&["fut"], &["*.fut"]),
    (&["gap"], &["*.g", "*.gap", "*.gi", "*.gd", "*.tst"]),
    (&["gdscript"], &["*.gd"]),
    (&["gleam"], &["*.gleam"]),
    (&["gn"], &["*.gn", "*.gni"]),
    (&["go"], &["*.go"]),
    (&["gprbuild"], &["*.gpr"]),
    (&["gradle"], &[
        "*.gradle", "*.gradle.kts", "gradle.properties", "gradle-wrapper.*",
        "gradlew", "gradlew.bat",
    ]),
    (&["graphql"], &["*.graphql", "*.graphqls"]),
    (&["groovy"], &["*.groovy", "*.gradle"]),
    (&["gzip"], &["*.gz", "*.tgz"]),
    (&["h"], &["*.h", "*.hh", "*.hpp"]),
    (&["haml"], &["*.haml"]),
    (&["hare"], &["*.ha"]),
    (&["haskell"], &["*.hs", "*.lhs", "*.cpphs", "*.c2hs", "*.hsc"]),
    (&["hbs"], &["*.hbs"]),
    (&["hs"], &["*.hs", "*.lhs"]),
    (&["html"], &["*.htm", "*.html", "*.ejs"]),
    (&["hurl"], &["*.hurl"]),
    (&["hy"], &["*.hy"]),
    (&["idris"], &["*.idr", "*.lidr"]),
    (&["janet"], &["*.janet"]),
    (&["java"], &["*.java", "*.jsp", "*.jspx", "*.properties"]),
    (&["jinja"], &["*.j2", "*.jinja", "*.jinja2"]),
    (&["jl"], &["*.jl"]),
    (&["js"], &["*.js", "*.jsx", "*.vue", "*.cjs", "*.mjs"]),
    (&["json"], &["*.json", "composer.lock", "*.sarif"]),
    (&["jsonl"], &["*.jsonl"]),
    (&["julia"], &["*.jl"]),
    (&["jupyter"], &["*.ipynb", "*.jpynb"]),
    (&["k"], &["*.k"]),
    (&["kconfig"], &["Kconfig", "Kconfig.*"]),
    (&["kotlin"], &["*.kt", "*.kts"]),
    (&["lean"], &["*.lean"]),
    (&["less"], &["*.less"]),
    (&["license"], &[
        // General
        "COPYING", "COPYING[.-]*",
        "COPYRIGHT", "COPYRIGHT[.-]*",
        "EULA", "EULA[.-]*",
        "licen[cs]e", "licen[cs]e.*",
        "LICEN[CS]E", "LICEN[CS]E[.-]*", "*[.-]LICEN[CS]E*",
        "NOTICE", "NOTICE[.-]*",
        "PATENTS", "PATENTS[.-]*",
        "UNLICEN[CS]E", "UNLICEN[CS]E[.-]*",
        // GPL (gpl.txt, etc.)
        "agpl[.-]*",
        "gpl[.-]*",
        "lgpl[.-]*",
        // Other license-specific (APACHE-2.0.txt, etc.)
        "AGPL-*[0-9]*",
        "APACHE-*[0-9]*",
        "BSD-*[0-9]*",
        "CC-BY-*",
        "GFDL-*[0-9]*",
        "GNU-*[0-9]*",
        "GPL-*[0-9]*",
        "LGPL-*[0-9]*",
        "MIT-*[0-9]*",
        "MPL-*[0-9]*",
        "OFL-*[0-9]*",
    ]),
    (&["lilypond"], &["*.ly", "*.ily"]),
    (&["lisp"], &["*.el", "*.jl", "*.lisp", "*.lsp", "*.sc", "*.scm"]),
    (&["llvm"], &["*.ll"]),
    (&["lock"], &["*.lock", "package-lock.json"]),
    (&["log"], &["*.log"]),
    (&["lua"], &["*.lua"]),
    (&["lz4"], &["*.lz4"]),
    (&["lzma"], &["*.lzma"]),
    (&["m4"], &["*.ac", "*.m4"]),
    (&["make"], &[
        "[Gg][Nn][Uu]makefile", "[Mm]akefile",
        "[Gg][Nn][Uu]makefile.am", "[Mm]akefile.am",
        "[Gg][Nn][Uu]makefile.in", "[Mm]akefile.in",
        "Makefile.*",
        "*.mk", "*.mak"
    ]),
    (&["mako"], &["*.mako", "*.mao"]),
    (&["man"], &["*.[0-9lnpx]", "*.[0-9][cEFMmpSx]"]),
    (&["markdown", "md"], &[
        "*.markdown",
        "*.md",
        "*.mdown",
        "*.mdwn",
        "*.mkd",
        "*.mkdn",
        "*.mdx",
    ]),
    (&["matlab"], &["*.m"]),
    (&["meson"], &["meson.build", "meson_options.txt", "meson.options"]),
    (&["minified"], &["*.min.html", "*.min.css", "*.min.js"]),
    (&["mint"], &["*.mint"]),
    (&["mk"], &["mkfile"]),
    (&["ml"], &["*.ml"]),
    (&["mojo"], &["*.mojo"]),
    (&["motoko"], &["*.mo"]),
    (&["msbuild"], &[
        "*.csproj", "*.fsproj", "*.vcxproj", "*.proj", "*.props", "*.targets",
        "*.sln", "*.slnf"
    ]),
    (&["nim"], &["*.nim", "*.nimf", "*.nimble", "*.nims"]),
    (&["nix"], &["*.nix"]),
    (&["objc"], &["*.h", "*.m"]),
    (&["objcpp"], &["*.h", "*.mm"]),
    (&["ocaml"], &["*.ml", "*.mli", "*.mll", "*.mly"]),
    (&["org"], &["*.org", "*.org_archive"]),
    (&["pants"], &["BUILD"]),
    (&["pascal"], &["*.pas", "*.dpr", "*.lpr", "*.pp", "*.inc"]),
    (&["pdf"], &["*.pdf"]),
    (&["perl"], &["*.perl", "*.pl", "*.PL", "*.plh", "*.plx", "*.pm", "*.t"]),
    (&["php"], &[
        // note that PHP 6 doesn't exist
        // See: https://wiki.php.net/rfc/php6
        "*.php", "*.php3", "*.php4", "*.php5", "*.php7", "*.php8",
        "*.pht", "*.phtml"
    ]),
    (&["po"], &["*.po"]),
    (&["pod"], &["*.pod"]),
    (&["postscript"], &["*.eps", "*.ps"]),
    (&["prolog"], &["*.pl", "*.pro", "*.prolog", "*.P"]),
    (&["proto", "protobuf"], &["*.proto"]),
    (&["ps"], &["*.cdxml", "*.ps1", "*.ps1xml", "*.psd1", "*.psm1"]),
    (&["puppet"], &["*.epp", "*.erb", "*.pp", "*.rb"]),
    (&["purs"], &["*.purs"]),
    (&["py", "python"], &["*.py", "*.pyi"]),
    (&["qmake"], &["*.pro", "*.pri", "*.prf"]),
    (&["qml"], &["*.qml"]),
    (&["qrc"], &["*.qrc"]),
    (&["qui"], &["*.ui"]),
    (&["r"], &["*.R", "*.r", "*.Rmd", "*.rmd", "*.Rnw", "*.rnw"]),
    (&["racket"], &["*.rkt"]),
    (&["raku"], &[
        "*.raku", "*.rakumod", "*.rakudoc", "*.rakutest",
        "*.p6", "*.pl6", "*.pm6"
    ]),
    (&["rdoc"], &["*.rdoc"]),
    (&["readme"], &["README*", "*README"]),
    (&["reasonml"], &["*.re", "*.rei"]),
    (&["red"], &["*.r", "*.red", "*.reds"]),
    (&["rescript"], &["*.res", "*.resi"]),
    (&["robot"], &["*.robot"]),
    (&["rocq"], &["*.v"]),
    (&["rst"], &["*.rst"]),
    (&["ruby"], &[
        // Idiomatic files
        "config.ru", "Gemfile", ".irbrc", "Rakefile",
        // Extensions
        "*.gemspec", "*.rb", "*.rbw", "*.rake"
    ]),
    (&["rust"], &["*.rs"]),
    (&["sass"], &["*.sass", "*.scss"]),
    (&["scala"], &["*.scala", "*.sbt"]),
    (&["scdoc"], &["*.scd", "*.scdoc"]),
    (&["seed7"], &["*.sd7", "*.s7i"]),
    (&["sh"], &[
        // Portable/misc. init files
        ".env", ".login", ".logout", ".profile", "profile",
        // bash-specific init files
        ".bash_login", "bash_login",
        ".bash_logout", "bash_logout",
        ".bash_profile", "bash_profile",
        ".bashrc", "bashrc", "*.bashrc",
        // csh-specific init files
        ".cshrc", "*.cshrc",
        // ksh-specific init files
        ".kshrc", "*.kshrc",
        // tcsh-specific init files
        ".tcshrc",
        // zsh-specific init files
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        // Extensions
        "*.bash", "*.csh", "*.env", "*.ksh", "*.sh", "*.tcsh", "*.zsh",
    ]),
    (&["slim"], &["*.skim", "*.slim", "*.slime"]),
    (&["smarty"], &["*.tpl"]),
    (&["sml"], &["*.sml", "*.sig"]),
    (&["solidity"], &["*.sol"]),
    (&["soy"], &["*.soy"]),
    (&["spark"], &["*.spark"]),
    (&["spec"], &["*.spec"]),
    (&["sql"], &["*.sql", "*.psql"]),
    (&["ssa"], &["*.ssa"]),
    (&["stylus"], &["*.styl"]),
    (&["sv"], &["*.v", "*.vg", "*.sv", "*.svh", "*.h"]),
    (&["svelte"], &["*.svelte", "*.svelte.ts"]),
    (&["svg"], &["*.svg"]),
    (&["swift"], &["*.swift"]),
    (&["swig"], &["*.def", "*.i"]),
    (&["systemd"], &[
        "*.automount", "*.conf", "*.device", "*.link", "*.mount", "*.path",
        "*.scope", "*.service", "*.slice", "*.socket", "*.swap", "*.target",
        "*.timer",
    ]),
    (&["taskpaper"], &["*.taskpaper"]),
    (&["tcl"], &["*.tcl"]),
    (&["tex"], &["*.tex", "*.ltx", "*.cls", "*.sty", "*.bib", "*.dtx", "*.ins"]),
    (&["texinfo"], &["*.texi"]),
    (&["textile"], &["*.textile"]),
    (&["tf"], &[
        "*.tf", "*.tf.json", "*.tfvars", "*.tfvars.json",
        "*.terraformrc", "terraform.rc", "*.tfrc", "*.terraform.lock.hcl",
    ]),
    (&["thrift"], &["*.thrift"]),
    (&["toml"], &["*.toml", "Cargo.lock"]),
    (&["ts", "typescript"], &["*.ts", "*.tsx", "*.cts", "*.mts"]),
    (&["twig"], &["*.twig"]),
    (&["txt"], &["*.txt"]),
    (&["typoscript"], &["*.typoscript", "*.ts"]),
    (&["typst"], &["*.typ"]),
    (&["usd"], &["*.usd", "*.usda", "*.usdc"]),
    (&["v"], &["*.v", "*.vsh"]),
    (&["vala"], &["*.vala"]),
    (&["vb"], &["*.vb"]),
    (&["vcl"], &["*.vcl"]),
    (&["verilog"], &["*.v", "*.vh", "*.sv", "*.svh"]),
    (&["vhdl"], &["*.vhd", "*.vhdl"]),
    (&["vim"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vimscript"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vue"], &["*.vue"]),
    (&["webidl"], &["*.idl", "*.webidl", "*.widl"]),
    (&["wgsl"], &["*.wgsl"]),
    (&["wiki"], &["*.mediawiki", "*.wiki"]),
    (&["xml"], &[
        "*.xml", "*.xml.dist", "*.dtd", "*.xsl", "*.xslt", "*.xsd", "*.xjb",
        "*.rng", "*.sch", "*.xhtml",
    ]),
    (&["xz"], &["*.xz", "*.txz"]),
    (&["yacc"], &["*.y"]),
    (&["yaml"], &["*.yaml", "*.yml"]),
    (&["yang"], &["*.yang"]),
    (&["z"], &["*.Z"]),
    (&["zig"], &["*.zig"]),
    (&["zsh"], &[
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        "*.zsh",
    ]),
    (&["zstd"], &["*.zst", "*.zstd"]),
];
```


---

### 🔹 Commit #12: `93acfe2d`
- **完整 Hash**: `93acfe2d47d46bc2f92a78f1e64098ad0a7b34b5`
- **說明 (Ground Truth)**: ignore/types: add `proto` for filtering to protobuf files
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/default_types.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:6, E:4, A:0) ➔ After(N:7, E:6, A:0)
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
  • + [新增節點] `default_types_aliases_are_sorted` (FUNCTION_DEF)
  • + [新增呼叫邊] `default_types_aliases_are_sorted` ──[CALLS]──> `DEFAULT_TYPES.iter (External/Unresolved)`
  • + [新增呼叫邊] `default_types_aliases_are_sorted` ──[CALLS]──> `assert! (Macro)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `DEFAULT_TYPES()`
- **變更前簽章 (Before)**: `[Module State] DEFAULT_TYPES` (L12~L344)
- **變更後簽章 (After)**: `[Module State] DEFAULT_TYPES` (L12~L344)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) const DEFAULT_TYPES: &[(&[&str], &[&str])] = &[
    (&["ada"], &["*.adb", "*.ads"]),
    (&["agda"], &["*.agda", "*.lagda"]),
    (&["aidl"], &["*.aidl"]),
    (&["alire"], &["alire.toml"]),
    (&["amake"], &["*.mk", "*.bp"]),
    (&["asciidoc"], &["*.adoc", "*.asc", "*.asciidoc"]),
    (&["asm"], &["*.asm", "*.s", "*.S"]),
    (&["asp"], &[
        "*.aspx", "*.aspx.cs", "*.aspx.vb", "*.ascx", "*.ascx.cs",
        "*.ascx.vb", "*.asp"
    ]),
    (&["ats"], &["*.ats", "*.dats", "*.sats", "*.hats"]),
    (&["avro"], &["*.avdl", "*.avpr", "*.avsc"]),
    (&["awk"], &["*.awk"]),
    (&["bat", "batch"], &["*.bat"]),
    (&["bazel"], &[
        "*.bazel", "*.bzl", "*.BUILD", "*.bazelrc", "BUILD", "MODULE.bazel",
        "WORKSPACE", "WORKSPACE.bazel", "WORKSPACE.bzlmod",
    ]),
    (&["bitbake"], &["*.bb", "*.bbappend", "*.bbclass", "*.conf", "*.inc"]),
    (&["boxlang"], &["*.bx", "*.bxm", "*.bxs"]),
    (&["brotli"], &["*.br"]),
    (&["buildstream"], &["*.bst"]),
    (&["bzip2"], &["*.bz2", "*.tbz2"]),
    (&["c"], &["*.[chH]", "*.[chH].in", "*.cats"]),
    (&["cabal"], &["*.cabal"]),
    (&["candid"], &["*.did"]),
    (&["carp"], &["*.carp"]),
    (&["cbor"], &["*.cbor"]),
    (&["ceylon"], &["*.ceylon"]),
    (&["cfml"], &["*.cfc", "*.cfm"]),
    (&["clojure"], &["*.clj", "*.cljc", "*.cljs", "*.cljx"]),
    (&["cmake"], &["*.cmake", "CMakeLists.txt"]),
    (&["cmd"], &["*.bat", "*.cmd"]),
    (&["cml"], &["*.cml"]),
    (&["coffeescript"], &["*.coffee"]),
    (&["config"], &["*.cfg", "*.conf", "*.config", "*.ini"]),
    (&["container"], &["*Containerfile*", "*Dockerfile*"]),
    (&["coq"], &["*.v"]),
    (&["cpp"], &[
        "*.[ChH]", "*.cc", "*.[ch]pp", "*.[ch]xx", "*.hh",  "*.inl",
        "*.[ChH].in", "*.cc.in", "*.[ch]pp.in", "*.[ch]xx.in", "*.hh.in",
    ]),
    (&["creole"], &["*.creole"]),
    (&["crystal"], &["Projectfile", "*.cr", "*.ecr", "shard.yml"]),
    (&["cs"], &["*.cs"]),
    (&["csharp"], &["*.cs"]),
    (&["cshtml"], &["*.cshtml"]),
    (&["csproj"], &["*.csproj"]),
    (&["css"], &["*.css", "*.scss"]),
    (&["csv"], &["*.csv"]),
    (&["cuda"], &["*.cu", "*.cuh"]),
    (&["cython"], &["*.pyx", "*.pxi", "*.pxd"]),
    (&["d"], &["*.d"]),
    (&["dart"], &["*.dart"]),
    (&["devicetree"], &["*.dts", "*.dtsi", "*.dtso"]),
    (&["dhall"], &["*.dhall"]),
    (&["diff"], &["*.patch", "*.diff"]),
    (&["dita"], &["*.dita", "*.ditamap", "*.ditaval"]),
    (&["docker"], &["*Dockerfile*"]),
    (&["dockercompose"], &["docker-compose.yml", "docker-compose.*.yml"]),
    (&["dts"], &["*.dts", "*.dtsi"]),
    (&["dvc"], &["Dvcfile", "*.dvc"]),
    (&["ebuild"], &["*.ebuild", "*.eclass"]),
    (&["edn"], &["*.edn"]),
    (&["elisp"], &["*.el"]),
    (&["elixir"], &["*.ex", "*.eex", "*.exs", "*.heex", "*.leex", "*.livemd"]),
    (&["elm"], &["*.elm"]),
    (&["erb"], &["*.erb"]),
    (&["erlang"], &["*.erl", "*.hrl"]),
    (&["fennel"], &["*.fnl"]),
    (&["fidl"], &["*.fidl"]),
    (&["fish"], &["*.fish"]),
    (&["flatbuffers"], &["*.fbs"]),
    (&["fortran"], &[
        "*.f", "*.F", "*.f77", "*.F77", "*.pfo",
        "*.f90", "*.F90", "*.f95", "*.F95",
    ]),
    (&["fsharp"], &["*.fs", "*.fsx", "*.fsi"]),
    (&["fut"], &["*.fut"]),
    (&["gap"], &["*.g", "*.gap", "*.gi", "*.gd", "*.tst"]),
    (&["gdscript"], &["*.gd"]),
    (&["gleam"], &["*.gleam"]),
    (&["gn"], &["*.gn", "*.gni"]),
    (&["go"], &["*.go"]),
    (&["gprbuild"], &["*.gpr"]),
    (&["gradle"], &[
        "*.gradle", "*.gradle.kts", "gradle.properties", "gradle-wrapper.*",
        "gradlew", "gradlew.bat",
    ]),
    (&["graphql"], &["*.graphql", "*.graphqls"]),
    (&["groovy"], &["*.groovy", "*.gradle"]),
    (&["gzip"], &["*.gz", "*.tgz"]),
    (&["h"], &["*.h", "*.hh", "*.hpp"]),
    (&["haml"], &["*.haml"]),
    (&["hare"], &["*.ha"]),
    (&["haskell"], &["*.hs", "*.lhs", "*.cpphs", "*.c2hs", "*.hsc"]),
    (&["hbs"], &["*.hbs"]),
    (&["hs"], &["*.hs", "*.lhs"]),
    (&["html"], &["*.htm", "*.html", "*.ejs"]),
    (&["hurl"], &["*.hurl"]),
    (&["hy"], &["*.hy"]),
    (&["idris"], &["*.idr", "*.lidr"]),
    (&["janet"], &["*.janet"]),
    (&["java"], &["*.java", "*.jsp", "*.jspx", "*.properties"]),
    (&["jinja"], &["*.j2", "*.jinja", "*.jinja2"]),
    (&["jl"], &["*.jl"]),
    (&["js"], &["*.js", "*.jsx", "*.vue", "*.cjs", "*.mjs"]),
    (&["json"], &["*.json", "composer.lock", "*.sarif"]),
    (&["jsonl"], &["*.jsonl"]),
    (&["julia"], &["*.jl"]),
    (&["jupyter"], &["*.ipynb", "*.jpynb"]),
    (&["k"], &["*.k"]),
    (&["kconfig"], &["Kconfig", "Kconfig.*"]),
    (&["kotlin"], &["*.kt", "*.kts"]),
    (&["lean"], &["*.lean"]),
    (&["less"], &["*.less"]),
    (&["license"], &[
        // General
        "COPYING", "COPYING[.-]*",
        "COPYRIGHT", "COPYRIGHT[.-]*",
        "EULA", "EULA[.-]*",
        "licen[cs]e", "licen[cs]e.*",
        "LICEN[CS]E", "LICEN[CS]E[.-]*", "*[.-]LICEN[CS]E*",
        "NOTICE", "NOTICE[.-]*",
        "PATENTS", "PATENTS[.-]*",
        "UNLICEN[CS]E", "UNLICEN[CS]E[.-]*",
        // GPL (gpl.txt, etc.)
        "agpl[.-]*",
        "gpl[.-]*",
        "lgpl[.-]*",
        // Other license-specific (APACHE-2.0.txt, etc.)
        "AGPL-*[0-9]*",
        "APACHE-*[0-9]*",
        "BSD-*[0-9]*",
        "CC-BY-*",
        "GFDL-*[0-9]*",
        "GNU-*[0-9]*",
        "GPL-*[0-9]*",
        "LGPL-*[0-9]*",
        "MIT-*[0-9]*",
        "MPL-*[0-9]*",
        "OFL-*[0-9]*",
    ]),
    (&["lilypond"], &["*.ly", "*.ily"]),
    (&["lisp"], &["*.el", "*.jl", "*.lisp", "*.lsp", "*.sc", "*.scm"]),
    (&["llvm"], &["*.ll"]),
    (&["lock"], &["*.lock", "package-lock.json"]),
    (&["log"], &["*.log"]),
    (&["lua"], &["*.lua"]),
    (&["lz4"], &["*.lz4"]),
    (&["lzma"], &["*.lzma"]),
    (&["m4"], &["*.ac", "*.m4"]),
    (&["make"], &[
        "[Gg][Nn][Uu]makefile", "[Mm]akefile",
        "[Gg][Nn][Uu]makefile.am", "[Mm]akefile.am",
        "[Gg][Nn][Uu]makefile.in", "[Mm]akefile.in",
        "Makefile.*",
        "*.mk", "*.mak"
    ]),
    (&["mako"], &["*.mako", "*.mao"]),
    (&["man"], &["*.[0-9lnpx]", "*.[0-9][cEFMmpSx]"]),
    (&["markdown", "md"], &[
        "*.markdown",
        "*.md",
        "*.mdown",
        "*.mdwn",
        "*.mkd",
        "*.mkdn",
        "*.mdx",
    ]),
    (&["matlab"], &["*.m"]),
    (&["meson"], &["meson.build", "meson_options.txt", "meson.options"]),
    (&["minified"], &["*.min.html", "*.min.css", "*.min.js"]),
    (&["mint"], &["*.mint"]),
    (&["mk"], &["mkfile"]),
    (&["ml"], &["*.ml"]),
    (&["mojo"], &["*.mojo"]),
    (&["motoko"], &["*.mo"]),
    (&["msbuild"], &[
        "*.csproj", "*.fsproj", "*.vcxproj", "*.proj", "*.props", "*.targets",
        "*.sln", "*.slnf"
    ]),
    (&["nim"], &["*.nim", "*.nimf", "*.nimble", "*.nims"]),
    (&["nix"], &["*.nix"]),
    (&["objc"], &["*.h", "*.m"]),
    (&["objcpp"], &["*.h", "*.mm"]),
    (&["ocaml"], &["*.ml", "*.mli", "*.mll", "*.mly"]),
    (&["org"], &["*.org", "*.org_archive"]),
    (&["pants"], &["BUILD"]),
    (&["pascal"], &["*.pas", "*.dpr", "*.lpr", "*.pp", "*.inc"]),
    (&["pdf"], &["*.pdf"]),
    (&["perl"], &["*.perl", "*.pl", "*.PL", "*.plh", "*.plx", "*.pm", "*.t"]),
    (&["php"], &[
        // note that PHP 6 doesn't exist
        // See: https://wiki.php.net/rfc/php6
        "*.php", "*.php3", "*.php4", "*.php5", "*.php7", "*.php8",
        "*.pht", "*.phtml"
    ]),
    (&["po"], &["*.po"]),
    (&["pod"], &["*.pod"]),
    (&["postscript"], &["*.eps", "*.ps"]),
    (&["prolog"], &["*.pl", "*.pro", "*.prolog", "*.P"]),
    (&["protobuf"], &["*.proto"]),
    (&["ps"], &["*.cdxml", "*.ps1", "*.ps1xml", "*.psd1", "*.psm1"]),
    (&["puppet"], &["*.epp", "*.erb", "*.pp", "*.rb"]),
    (&["purs"], &["*.purs"]),
    (&["py", "python"], &["*.py", "*.pyi"]),
    (&["qmake"], &["*.pro", "*.pri", "*.prf"]),
    (&["qml"], &["*.qml"]),
    (&["qrc"], &["*.qrc"]),
    (&["qui"], &["*.ui"]),
    (&["r"], &["*.R", "*.r", "*.Rmd", "*.rmd", "*.Rnw", "*.rnw"]),
    (&["racket"], &["*.rkt"]),
    (&["raku"], &[
        "*.raku", "*.rakumod", "*.rakudoc", "*.rakutest",
        "*.p6", "*.pl6", "*.pm6"
    ]),
    (&["rdoc"], &["*.rdoc"]),
    (&["readme"], &["README*", "*README"]),
    (&["reasonml"], &["*.re", "*.rei"]),
    (&["red"], &["*.r", "*.red", "*.reds"]),
    (&["rescript"], &["*.res", "*.resi"]),
    (&["robot"], &["*.robot"]),
    (&["rst"], &["*.rst"]),
    (&["ruby"], &[
        // Idiomatic files
        "config.ru", "Gemfile", ".irbrc", "Rakefile",
        // Extensions
        "*.gemspec", "*.rb", "*.rbw", "*.rake"
    ]),
    (&["rust"], &["*.rs"]),
    (&["sass"], &["*.sass", "*.scss"]),
    (&["scala"], &["*.scala", "*.sbt"]),
    (&["scdoc"], &["*.scd", "*.scdoc"]),
    (&["seed7"], &["*.sd7", "*.s7i"]),
    (&["sh"], &[
        // Portable/misc. init files
        ".env", ".login", ".logout", ".profile", "profile",
        // bash-specific init files
        ".bash_login", "bash_login",
        ".bash_logout", "bash_logout",
        ".bash_profile", "bash_profile",
        ".bashrc", "bashrc", "*.bashrc",
        // csh-specific init files
        ".cshrc", "*.cshrc",
        // ksh-specific init files
        ".kshrc", "*.kshrc",
        // tcsh-specific init files
        ".tcshrc",
        // zsh-specific init files
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        // Extensions
        "*.bash", "*.csh", "*.env", "*.ksh", "*.sh", "*.tcsh", "*.zsh",
    ]),
    (&["slim"], &["*.skim", "*.slim", "*.slime"]),
    (&["smarty"], &["*.tpl"]),
    (&["sml"], &["*.sml", "*.sig"]),
    (&["solidity"], &["*.sol"]),
    (&["soy"], &["*.soy"]),
    (&["spark"], &["*.spark"]),
    (&["spec"], &["*.spec"]),
    (&["sql"], &["*.sql", "*.psql"]),
    (&["ssa"], &["*.ssa"]),
    (&["stylus"], &["*.styl"]),
    (&["sv"], &["*.v", "*.vg", "*.sv", "*.svh", "*.h"]),
    (&["svelte"], &["*.svelte", "*.svelte.ts"]),
    (&["svg"], &["*.svg"]),
    (&["swift"], &["*.swift"]),
    (&["swig"], &["*.def", "*.i"]),
    (&["systemd"], &[
        "*.automount", "*.conf", "*.device", "*.link", "*.mount", "*.path",
        "*.scope", "*.service", "*.slice", "*.socket", "*.swap", "*.target",
        "*.timer",
    ]),
    (&["taskpaper"], &["*.taskpaper"]),
    (&["tcl"], &["*.tcl"]),
    (&["tex"], &["*.tex", "*.ltx", "*.cls", "*.sty", "*.bib", "*.dtx", "*.ins"]),
    (&["texinfo"], &["*.texi"]),
    (&["textile"], &["*.textile"]),
    (&["tf"], &[
        "*.tf", "*.tf.json", "*.tfvars", "*.tfvars.json",
        "*.terraformrc", "terraform.rc", "*.tfrc", "*.terraform.lock.hcl",
    ]),
    (&["thrift"], &["*.thrift"]),
    (&["toml"], &["*.toml", "Cargo.lock"]),
    (&["ts", "typescript"], &["*.ts", "*.tsx", "*.cts", "*.mts"]),
    (&["twig"], &["*.twig"]),
    (&["txt"], &["*.txt"]),
    (&["typoscript"], &["*.typoscript", "*.ts"]),
    (&["typst"], &["*.typ"]),
    (&["usd"], &["*.usd", "*.usda", "*.usdc"]),
    (&["v"], &["*.v", "*.vsh"]),
    (&["vala"], &["*.vala"]),
    (&["vb"], &["*.vb"]),
    (&["vcl"], &["*.vcl"]),
    (&["verilog"], &["*.v", "*.vh", "*.sv", "*.svh"]),
    (&["vhdl"], &["*.vhd", "*.vhdl"]),
    (&["vim"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vimscript"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vue"], &["*.vue"]),
    (&["webidl"], &["*.idl", "*.webidl", "*.widl"]),
    (&["wgsl"], &["*.wgsl"]),
    (&["wiki"], &["*.mediawiki", "*.wiki"]),
    (&["xml"], &[
        "*.xml", "*.xml.dist", "*.dtd", "*.xsl", "*.xslt", "*.xsd", "*.xjb",
        "*.rng", "*.sch", "*.xhtml",
    ]),
    (&["xz"], &["*.xz", "*.txz"]),
    (&["yacc"], &["*.y"]),
    (&["yaml"], &["*.yaml", "*.yml"]),
    (&["yang"], &["*.yang"]),
    (&["z"], &["*.Z"]),
    (&["zig"], &["*.zig"]),
    (&["zsh"], &[
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        "*.zsh",
    ]),
    (&["zstd"], &["*.zst", "*.zstd"]),
];
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) const DEFAULT_TYPES: &[(&[&str], &[&str])] = &[
    (&["ada"], &["*.adb", "*.ads"]),
    (&["agda"], &["*.agda", "*.lagda"]),
    (&["aidl"], &["*.aidl"]),
    (&["alire"], &["alire.toml"]),
    (&["amake"], &["*.mk", "*.bp"]),
    (&["asciidoc"], &["*.adoc", "*.asc", "*.asciidoc"]),
    (&["asm"], &["*.asm", "*.s", "*.S"]),
    (&["asp"], &[
        "*.aspx", "*.aspx.cs", "*.aspx.vb", "*.ascx", "*.ascx.cs",
        "*.ascx.vb", "*.asp"
    ]),
    (&["ats"], &["*.ats", "*.dats", "*.sats", "*.hats"]),
    (&["avro"], &["*.avdl", "*.avpr", "*.avsc"]),
    (&["awk"], &["*.awk"]),
    (&["bat", "batch"], &["*.bat"]),
    (&["bazel"], &[
        "*.bazel", "*.bzl", "*.BUILD", "*.bazelrc", "BUILD", "MODULE.bazel",
        "WORKSPACE", "WORKSPACE.bazel", "WORKSPACE.bzlmod",
    ]),
    (&["bitbake"], &["*.bb", "*.bbappend", "*.bbclass", "*.conf", "*.inc"]),
    (&["boxlang"], &["*.bx", "*.bxm", "*.bxs"]),
    (&["brotli"], &["*.br"]),
    (&["buildstream"], &["*.bst"]),
    (&["bzip2"], &["*.bz2", "*.tbz2"]),
    (&["c"], &["*.[chH]", "*.[chH].in", "*.cats"]),
    (&["cabal"], &["*.cabal"]),
    (&["candid"], &["*.did"]),
    (&["carp"], &["*.carp"]),
    (&["cbor"], &["*.cbor"]),
    (&["ceylon"], &["*.ceylon"]),
    (&["cfml"], &["*.cfc", "*.cfm"]),
    (&["clojure"], &["*.clj", "*.cljc", "*.cljs", "*.cljx"]),
    (&["cmake"], &["*.cmake", "CMakeLists.txt"]),
    (&["cmd"], &["*.bat", "*.cmd"]),
    (&["cml"], &["*.cml"]),
    (&["coffeescript"], &["*.coffee"]),
    (&["config"], &["*.cfg", "*.conf", "*.config", "*.ini"]),
    (&["container"], &["*Containerfile*", "*Dockerfile*"]),
    (&["coq"], &["*.v"]),
    (&["cpp"], &[
        "*.[ChH]", "*.cc", "*.[ch]pp", "*.[ch]xx", "*.hh",  "*.inl",
        "*.[ChH].in", "*.cc.in", "*.[ch]pp.in", "*.[ch]xx.in", "*.hh.in",
    ]),
    (&["creole"], &["*.creole"]),
    (&["crystal"], &["Projectfile", "*.cr", "*.ecr", "shard.yml"]),
    (&["cs"], &["*.cs"]),
    (&["csharp"], &["*.cs"]),
    (&["cshtml"], &["*.cshtml"]),
    (&["csproj"], &["*.csproj"]),
    (&["css"], &["*.css", "*.scss"]),
    (&["csv"], &["*.csv"]),
    (&["cuda"], &["*.cu", "*.cuh"]),
    (&["cython"], &["*.pyx", "*.pxi", "*.pxd"]),
    (&["d"], &["*.d"]),
    (&["dart"], &["*.dart"]),
    (&["devicetree"], &["*.dts", "*.dtsi", "*.dtso"]),
    (&["dhall"], &["*.dhall"]),
    (&["diff"], &["*.patch", "*.diff"]),
    (&["dita"], &["*.dita", "*.ditamap", "*.ditaval"]),
    (&["docker"], &["*Dockerfile*"]),
    (&["dockercompose"], &["docker-compose.yml", "docker-compose.*.yml"]),
    (&["dts"], &["*.dts", "*.dtsi"]),
    (&["dvc"], &["Dvcfile", "*.dvc"]),
    (&["ebuild"], &["*.ebuild", "*.eclass"]),
    (&["edn"], &["*.edn"]),
    (&["elisp"], &["*.el"]),
    (&["elixir"], &["*.ex", "*.eex", "*.exs", "*.heex", "*.leex", "*.livemd"]),
    (&["elm"], &["*.elm"]),
    (&["erb"], &["*.erb"]),
    (&["erlang"], &["*.erl", "*.hrl"]),
    (&["fennel"], &["*.fnl"]),
    (&["fidl"], &["*.fidl"]),
    (&["fish"], &["*.fish"]),
    (&["flatbuffers"], &["*.fbs"]),
    (&["fortran"], &[
        "*.f", "*.F", "*.f77", "*.F77", "*.pfo",
        "*.f90", "*.F90", "*.f95", "*.F95",
    ]),
    (&["fsharp"], &["*.fs", "*.fsx", "*.fsi"]),
    (&["fut"], &["*.fut"]),
    (&["gap"], &["*.g", "*.gap", "*.gi", "*.gd", "*.tst"]),
    (&["gdscript"], &["*.gd"]),
    (&["gleam"], &["*.gleam"]),
    (&["gn"], &["*.gn", "*.gni"]),
    (&["go"], &["*.go"]),
    (&["gprbuild"], &["*.gpr"]),
    (&["gradle"], &[
        "*.gradle", "*.gradle.kts", "gradle.properties", "gradle-wrapper.*",
        "gradlew", "gradlew.bat",
    ]),
    (&["graphql"], &["*.graphql", "*.graphqls"]),
    (&["groovy"], &["*.groovy", "*.gradle"]),
    (&["gzip"], &["*.gz", "*.tgz"]),
    (&["h"], &["*.h", "*.hh", "*.hpp"]),
    (&["haml"], &["*.haml"]),
    (&["hare"], &["*.ha"]),
    (&["haskell"], &["*.hs", "*.lhs", "*.cpphs", "*.c2hs", "*.hsc"]),
    (&["hbs"], &["*.hbs"]),
    (&["hs"], &["*.hs", "*.lhs"]),
    (&["html"], &["*.htm", "*.html", "*.ejs"]),
    (&["hurl"], &["*.hurl"]),
    (&["hy"], &["*.hy"]),
    (&["idris"], &["*.idr", "*.lidr"]),
    (&["janet"], &["*.janet"]),
    (&["java"], &["*.java", "*.jsp", "*.jspx", "*.properties"]),
    (&["jinja"], &["*.j2", "*.jinja", "*.jinja2"]),
    (&["jl"], &["*.jl"]),
    (&["js"], &["*.js", "*.jsx", "*.vue", "*.cjs", "*.mjs"]),
    (&["json"], &["*.json", "composer.lock", "*.sarif"]),
    (&["jsonl"], &["*.jsonl"]),
    (&["julia"], &["*.jl"]),
    (&["jupyter"], &["*.ipynb", "*.jpynb"]),
    (&["k"], &["*.k"]),
    (&["kconfig"], &["Kconfig", "Kconfig.*"]),
    (&["kotlin"], &["*.kt", "*.kts"]),
    (&["lean"], &["*.lean"]),
    (&["less"], &["*.less"]),
    (&["license"], &[
        // General
        "COPYING", "COPYING[.-]*",
        "COPYRIGHT", "COPYRIGHT[.-]*",
        "EULA", "EULA[.-]*",
        "licen[cs]e", "licen[cs]e.*",
        "LICEN[CS]E", "LICEN[CS]E[.-]*", "*[.-]LICEN[CS]E*",
        "NOTICE", "NOTICE[.-]*",
        "PATENTS", "PATENTS[.-]*",
        "UNLICEN[CS]E", "UNLICEN[CS]E[.-]*",
        // GPL (gpl.txt, etc.)
        "agpl[.-]*",
        "gpl[.-]*",
        "lgpl[.-]*",
        // Other license-specific (APACHE-2.0.txt, etc.)
        "AGPL-*[0-9]*",
        "APACHE-*[0-9]*",
        "BSD-*[0-9]*",
        "CC-BY-*",
        "GFDL-*[0-9]*",
        "GNU-*[0-9]*",
        "GPL-*[0-9]*",
        "LGPL-*[0-9]*",
        "MIT-*[0-9]*",
        "MPL-*[0-9]*",
        "OFL-*[0-9]*",
    ]),
    (&["lilypond"], &["*.ly", "*.ily"]),
    (&["lisp"], &["*.el", "*.jl", "*.lisp", "*.lsp", "*.sc", "*.scm"]),
    (&["llvm"], &["*.ll"]),
    (&["lock"], &["*.lock", "package-lock.json"]),
    (&["log"], &["*.log"]),
    (&["lua"], &["*.lua"]),
    (&["lz4"], &["*.lz4"]),
    (&["lzma"], &["*.lzma"]),
    (&["m4"], &["*.ac", "*.m4"]),
    (&["make"], &[
        "[Gg][Nn][Uu]makefile", "[Mm]akefile",
        "[Gg][Nn][Uu]makefile.am", "[Mm]akefile.am",
        "[Gg][Nn][Uu]makefile.in", "[Mm]akefile.in",
        "Makefile.*",
        "*.mk", "*.mak"
    ]),
    (&["mako"], &["*.mako", "*.mao"]),
    (&["man"], &["*.[0-9lnpx]", "*.[0-9][cEFMmpSx]"]),
    (&["markdown", "md"], &[
        "*.markdown",
        "*.md",
        "*.mdown",
        "*.mdwn",
        "*.mkd",
        "*.mkdn",
        "*.mdx",
    ]),
    (&["matlab"], &["*.m"]),
    (&["meson"], &["meson.build", "meson_options.txt", "meson.options"]),
    (&["minified"], &["*.min.html", "*.min.css", "*.min.js"]),
    (&["mint"], &["*.mint"]),
    (&["mk"], &["mkfile"]),
    (&["ml"], &["*.ml"]),
    (&["mojo"], &["*.mojo"]),
    (&["motoko"], &["*.mo"]),
    (&["msbuild"], &[
        "*.csproj", "*.fsproj", "*.vcxproj", "*.proj", "*.props", "*.targets",
        "*.sln", "*.slnf"
    ]),
    (&["nim"], &["*.nim", "*.nimf", "*.nimble", "*.nims"]),
    (&["nix"], &["*.nix"]),
    (&["objc"], &["*.h", "*.m"]),
    (&["objcpp"], &["*.h", "*.mm"]),
    (&["ocaml"], &["*.ml", "*.mli", "*.mll", "*.mly"]),
    (&["org"], &["*.org", "*.org_archive"]),
    (&["pants"], &["BUILD"]),
    (&["pascal"], &["*.pas", "*.dpr", "*.lpr", "*.pp", "*.inc"]),
    (&["pdf"], &["*.pdf"]),
    (&["perl"], &["*.perl", "*.pl", "*.PL", "*.plh", "*.plx", "*.pm", "*.t"]),
    (&["php"], &[
        // note that PHP 6 doesn't exist
        // See: https://wiki.php.net/rfc/php6
        "*.php", "*.php3", "*.php4", "*.php5", "*.php7", "*.php8",
        "*.pht", "*.phtml"
    ]),
    (&["po"], &["*.po"]),
    (&["pod"], &["*.pod"]),
    (&["postscript"], &["*.eps", "*.ps"]),
    (&["prolog"], &["*.pl", "*.pro", "*.prolog", "*.P"]),
    (&["proto", "protobuf"], &["*.proto"]),
    (&["ps"], &["*.cdxml", "*.ps1", "*.ps1xml", "*.psd1", "*.psm1"]),
    (&["puppet"], &["*.epp", "*.erb", "*.pp", "*.rb"]),
    (&["purs"], &["*.purs"]),
    (&["py", "python"], &["*.py", "*.pyi"]),
    (&["qmake"], &["*.pro", "*.pri", "*.prf"]),
    (&["qml"], &["*.qml"]),
    (&["qrc"], &["*.qrc"]),
    (&["qui"], &["*.ui"]),
    (&["r"], &["*.R", "*.r", "*.Rmd", "*.rmd", "*.Rnw", "*.rnw"]),
    (&["racket"], &["*.rkt"]),
    (&["raku"], &[
        "*.raku", "*.rakumod", "*.rakudoc", "*.rakutest",
        "*.p6", "*.pl6", "*.pm6"
    ]),
    (&["rdoc"], &["*.rdoc"]),
    (&["readme"], &["README*", "*README"]),
    (&["reasonml"], &["*.re", "*.rei"]),
    (&["red"], &["*.r", "*.red", "*.reds"]),
    (&["rescript"], &["*.res", "*.resi"]),
    (&["robot"], &["*.robot"]),
    (&["rst"], &["*.rst"]),
    (&["ruby"], &[
        // Idiomatic files
        "config.ru", "Gemfile", ".irbrc", "Rakefile",
        // Extensions
        "*.gemspec", "*.rb", "*.rbw", "*.rake"
    ]),
    (&["rust"], &["*.rs"]),
    (&["sass"], &["*.sass", "*.scss"]),
    (&["scala"], &["*.scala", "*.sbt"]),
    (&["scdoc"], &["*.scd", "*.scdoc"]),
    (&["seed7"], &["*.sd7", "*.s7i"]),
    (&["sh"], &[
        // Portable/misc. init files
        ".env", ".login", ".logout", ".profile", "profile",
        // bash-specific init files
        ".bash_login", "bash_login",
        ".bash_logout", "bash_logout",
        ".bash_profile", "bash_profile",
        ".bashrc", "bashrc", "*.bashrc",
        // csh-specific init files
        ".cshrc", "*.cshrc",
        // ksh-specific init files
        ".kshrc", "*.kshrc",
        // tcsh-specific init files
        ".tcshrc",
        // zsh-specific init files
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        // Extensions
        "*.bash", "*.csh", "*.env", "*.ksh", "*.sh", "*.tcsh", "*.zsh",
    ]),
    (&["slim"], &["*.skim", "*.slim", "*.slime"]),
    (&["smarty"], &["*.tpl"]),
    (&["sml"], &["*.sml", "*.sig"]),
    (&["solidity"], &["*.sol"]),
    (&["soy"], &["*.soy"]),
    (&["spark"], &["*.spark"]),
    (&["spec"], &["*.spec"]),
    (&["sql"], &["*.sql", "*.psql"]),
    (&["ssa"], &["*.ssa"]),
    (&["stylus"], &["*.styl"]),
    (&["sv"], &["*.v", "*.vg", "*.sv", "*.svh", "*.h"]),
    (&["svelte"], &["*.svelte", "*.svelte.ts"]),
    (&["svg"], &["*.svg"]),
    (&["swift"], &["*.swift"]),
    (&["swig"], &["*.def", "*.i"]),
    (&["systemd"], &[
        "*.automount", "*.conf", "*.device", "*.link", "*.mount", "*.path",
        "*.scope", "*.service", "*.slice", "*.socket", "*.swap", "*.target",
        "*.timer",
    ]),
    (&["taskpaper"], &["*.taskpaper"]),
    (&["tcl"], &["*.tcl"]),
    (&["tex"], &["*.tex", "*.ltx", "*.cls", "*.sty", "*.bib", "*.dtx", "*.ins"]),
    (&["texinfo"], &["*.texi"]),
    (&["textile"], &["*.textile"]),
    (&["tf"], &[
        "*.tf", "*.tf.json", "*.tfvars", "*.tfvars.json",
        "*.terraformrc", "terraform.rc", "*.tfrc", "*.terraform.lock.hcl",
    ]),
    (&["thrift"], &["*.thrift"]),
    (&["toml"], &["*.toml", "Cargo.lock"]),
    (&["ts", "typescript"], &["*.ts", "*.tsx", "*.cts", "*.mts"]),
    (&["twig"], &["*.twig"]),
    (&["txt"], &["*.txt"]),
    (&["typoscript"], &["*.typoscript", "*.ts"]),
    (&["typst"], &["*.typ"]),
    (&["usd"], &["*.usd", "*.usda", "*.usdc"]),
    (&["v"], &["*.v", "*.vsh"]),
    (&["vala"], &["*.vala"]),
    (&["vb"], &["*.vb"]),
    (&["vcl"], &["*.vcl"]),
    (&["verilog"], &["*.v", "*.vh", "*.sv", "*.svh"]),
    (&["vhdl"], &["*.vhd", "*.vhdl"]),
    (&["vim"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vimscript"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vue"], &["*.vue"]),
    (&["webidl"], &["*.idl", "*.webidl", "*.widl"]),
    (&["wgsl"], &["*.wgsl"]),
    (&["wiki"], &["*.mediawiki", "*.wiki"]),
    (&["xml"], &[
        "*.xml", "*.xml.dist", "*.dtd", "*.xsl", "*.xslt", "*.xsd", "*.xjb",
        "*.rng", "*.sch", "*.xhtml",
    ]),
    (&["xz"], &["*.xz", "*.txz"]),
    (&["yacc"], &["*.y"]),
    (&["yaml"], &["*.yaml", "*.yml"]),
    (&["yang"], &["*.yang"]),
    (&["z"], &["*.Z"]),
    (&["zig"], &["*.zig"]),
    (&["zsh"], &[
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        "*.zsh",
    ]),
    (&["zstd"], &["*.zst", "*.zstd"]),
];
```


---

### 🔹 Commit #13: `77d27e82`
- **完整 Hash**: `77d27e82fabfd80de83960a73c2357ac1a03827a`
- **說明 (Ground Truth)**: ignore/types: add Mojo type
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/default_types.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:6, E:4, A:0) ➔ After(N:6, E:4, A:0)
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

### 🔹 函式: `DEFAULT_TYPES()`
- **變更前簽章 (Before)**: `[Module State] DEFAULT_TYPES` (L12~L343)
- **變更後簽章 (After)**: `[Module State] DEFAULT_TYPES` (L12~L344)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) const DEFAULT_TYPES: &[(&[&str], &[&str])] = &[
    (&["ada"], &["*.adb", "*.ads"]),
    (&["agda"], &["*.agda", "*.lagda"]),
    (&["aidl"], &["*.aidl"]),
    (&["alire"], &["alire.toml"]),
    (&["amake"], &["*.mk", "*.bp"]),
    (&["asciidoc"], &["*.adoc", "*.asc", "*.asciidoc"]),
    (&["asm"], &["*.asm", "*.s", "*.S"]),
    (&["asp"], &[
        "*.aspx", "*.aspx.cs", "*.aspx.vb", "*.ascx", "*.ascx.cs",
        "*.ascx.vb", "*.asp"
    ]),
    (&["ats"], &["*.ats", "*.dats", "*.sats", "*.hats"]),
    (&["avro"], &["*.avdl", "*.avpr", "*.avsc"]),
    (&["awk"], &["*.awk"]),
    (&["bat", "batch"], &["*.bat"]),
    (&["bazel"], &[
        "*.bazel", "*.bzl", "*.BUILD", "*.bazelrc", "BUILD", "MODULE.bazel",
        "WORKSPACE", "WORKSPACE.bazel", "WORKSPACE.bzlmod",
    ]),
    (&["bitbake"], &["*.bb", "*.bbappend", "*.bbclass", "*.conf", "*.inc"]),
    (&["boxlang"], &["*.bx", "*.bxm", "*.bxs"]),
    (&["brotli"], &["*.br"]),
    (&["buildstream"], &["*.bst"]),
    (&["bzip2"], &["*.bz2", "*.tbz2"]),
    (&["c"], &["*.[chH]", "*.[chH].in", "*.cats"]),
    (&["cabal"], &["*.cabal"]),
    (&["candid"], &["*.did"]),
    (&["carp"], &["*.carp"]),
    (&["cbor"], &["*.cbor"]),
    (&["ceylon"], &["*.ceylon"]),
    (&["cfml"], &["*.cfc", "*.cfm"]),
    (&["clojure"], &["*.clj", "*.cljc", "*.cljs", "*.cljx"]),
    (&["cmake"], &["*.cmake", "CMakeLists.txt"]),
    (&["cmd"], &["*.bat", "*.cmd"]),
    (&["cml"], &["*.cml"]),
    (&["coffeescript"], &["*.coffee"]),
    (&["config"], &["*.cfg", "*.conf", "*.config", "*.ini"]),
    (&["container"], &["*Containerfile*", "*Dockerfile*"]),
    (&["coq"], &["*.v"]),
    (&["cpp"], &[
        "*.[ChH]", "*.cc", "*.[ch]pp", "*.[ch]xx", "*.hh",  "*.inl",
        "*.[ChH].in", "*.cc.in", "*.[ch]pp.in", "*.[ch]xx.in", "*.hh.in",
    ]),
    (&["creole"], &["*.creole"]),
    (&["crystal"], &["Projectfile", "*.cr", "*.ecr", "shard.yml"]),
    (&["cs"], &["*.cs"]),
    (&["csharp"], &["*.cs"]),
    (&["cshtml"], &["*.cshtml"]),
    (&["csproj"], &["*.csproj"]),
    (&["css"], &["*.css", "*.scss"]),
    (&["csv"], &["*.csv"]),
    (&["cuda"], &["*.cu", "*.cuh"]),
    (&["cython"], &["*.pyx", "*.pxi", "*.pxd"]),
    (&["d"], &["*.d"]),
    (&["dart"], &["*.dart"]),
    (&["devicetree"], &["*.dts", "*.dtsi", "*.dtso"]),
    (&["dhall"], &["*.dhall"]),
    (&["diff"], &["*.patch", "*.diff"]),
    (&["dita"], &["*.dita", "*.ditamap", "*.ditaval"]),
    (&["docker"], &["*Dockerfile*"]),
    (&["dockercompose"], &["docker-compose.yml", "docker-compose.*.yml"]),
    (&["dts"], &["*.dts", "*.dtsi"]),
    (&["dvc"], &["Dvcfile", "*.dvc"]),
    (&["ebuild"], &["*.ebuild", "*.eclass"]),
    (&["edn"], &["*.edn"]),
    (&["elisp"], &["*.el"]),
    (&["elixir"], &["*.ex", "*.eex", "*.exs", "*.heex", "*.leex", "*.livemd"]),
    (&["elm"], &["*.elm"]),
    (&["erb"], &["*.erb"]),
    (&["erlang"], &["*.erl", "*.hrl"]),
    (&["fennel"], &["*.fnl"]),
    (&["fidl"], &["*.fidl"]),
    (&["fish"], &["*.fish"]),
    (&["flatbuffers"], &["*.fbs"]),
    (&["fortran"], &[
        "*.f", "*.F", "*.f77", "*.F77", "*.pfo",
        "*.f90", "*.F90", "*.f95", "*.F95",
    ]),
    (&["fsharp"], &["*.fs", "*.fsx", "*.fsi"]),
    (&["fut"], &["*.fut"]),
    (&["gap"], &["*.g", "*.gap", "*.gi", "*.gd", "*.tst"]),
    (&["gdscript"], &["*.gd"]),
    (&["gleam"], &["*.gleam"]),
    (&["gn"], &["*.gn", "*.gni"]),
    (&["go"], &["*.go"]),
    (&["gprbuild"], &["*.gpr"]),
    (&["gradle"], &[
        "*.gradle", "*.gradle.kts", "gradle.properties", "gradle-wrapper.*",
        "gradlew", "gradlew.bat",
    ]),
    (&["graphql"], &["*.graphql", "*.graphqls"]),
    (&["groovy"], &["*.groovy", "*.gradle"]),
    (&["gzip"], &["*.gz", "*.tgz"]),
    (&["h"], &["*.h", "*.hh", "*.hpp"]),
    (&["haml"], &["*.haml"]),
    (&["hare"], &["*.ha"]),
    (&["haskell"], &["*.hs", "*.lhs", "*.cpphs", "*.c2hs", "*.hsc"]),
    (&["hbs"], &["*.hbs"]),
    (&["hs"], &["*.hs", "*.lhs"]),
    (&["html"], &["*.htm", "*.html", "*.ejs"]),
    (&["hurl"], &["*.hurl"]),
    (&["hy"], &["*.hy"]),
    (&["idris"], &["*.idr", "*.lidr"]),
    (&["janet"], &["*.janet"]),
    (&["java"], &["*.java", "*.jsp", "*.jspx", "*.properties"]),
    (&["jinja"], &["*.j2", "*.jinja", "*.jinja2"]),
    (&["jl"], &["*.jl"]),
    (&["js"], &["*.js", "*.jsx", "*.vue", "*.cjs", "*.mjs"]),
    (&["json"], &["*.json", "composer.lock", "*.sarif"]),
    (&["jsonl"], &["*.jsonl"]),
    (&["julia"], &["*.jl"]),
    (&["jupyter"], &["*.ipynb", "*.jpynb"]),
    (&["k"], &["*.k"]),
    (&["kconfig"], &["Kconfig", "Kconfig.*"]),
    (&["kotlin"], &["*.kt", "*.kts"]),
    (&["lean"], &["*.lean"]),
    (&["less"], &["*.less"]),
    (&["license"], &[
        // General
        "COPYING", "COPYING[.-]*",
        "COPYRIGHT", "COPYRIGHT[.-]*",
        "EULA", "EULA[.-]*",
        "licen[cs]e", "licen[cs]e.*",
        "LICEN[CS]E", "LICEN[CS]E[.-]*", "*[.-]LICEN[CS]E*",
        "NOTICE", "NOTICE[.-]*",
        "PATENTS", "PATENTS[.-]*",
        "UNLICEN[CS]E", "UNLICEN[CS]E[.-]*",
        // GPL (gpl.txt, etc.)
        "agpl[.-]*",
        "gpl[.-]*",
        "lgpl[.-]*",
        // Other license-specific (APACHE-2.0.txt, etc.)
        "AGPL-*[0-9]*",
        "APACHE-*[0-9]*",
        "BSD-*[0-9]*",
        "CC-BY-*",
        "GFDL-*[0-9]*",
        "GNU-*[0-9]*",
        "GPL-*[0-9]*",
        "LGPL-*[0-9]*",
        "MIT-*[0-9]*",
        "MPL-*[0-9]*",
        "OFL-*[0-9]*",
    ]),
    (&["lilypond"], &["*.ly", "*.ily"]),
    (&["lisp"], &["*.el", "*.jl", "*.lisp", "*.lsp", "*.sc", "*.scm"]),
    (&["llvm"], &["*.ll"]),
    (&["lock"], &["*.lock", "package-lock.json"]),
    (&["log"], &["*.log"]),
    (&["lua"], &["*.lua"]),
    (&["lz4"], &["*.lz4"]),
    (&["lzma"], &["*.lzma"]),
    (&["m4"], &["*.ac", "*.m4"]),
    (&["make"], &[
        "[Gg][Nn][Uu]makefile", "[Mm]akefile",
        "[Gg][Nn][Uu]makefile.am", "[Mm]akefile.am",
        "[Gg][Nn][Uu]makefile.in", "[Mm]akefile.in",
        "Makefile.*",
        "*.mk", "*.mak"
    ]),
    (&["mako"], &["*.mako", "*.mao"]),
    (&["man"], &["*.[0-9lnpx]", "*.[0-9][cEFMmpSx]"]),
    (&["markdown", "md"], &[
        "*.markdown",
        "*.md",
        "*.mdown",
        "*.mdwn",
        "*.mkd",
        "*.mkdn",
        "*.mdx",
    ]),
    (&["matlab"], &["*.m"]),
    (&["meson"], &["meson.build", "meson_options.txt", "meson.options"]),
    (&["minified"], &["*.min.html", "*.min.css", "*.min.js"]),
    (&["mint"], &["*.mint"]),
    (&["mk"], &["mkfile"]),
    (&["ml"], &["*.ml"]),
    (&["motoko"], &["*.mo"]),
    (&["msbuild"], &[
        "*.csproj", "*.fsproj", "*.vcxproj", "*.proj", "*.props", "*.targets",
        "*.sln", "*.slnf"
    ]),
    (&["nim"], &["*.nim", "*.nimf", "*.nimble", "*.nims"]),
    (&["nix"], &["*.nix"]),
    (&["objc"], &["*.h", "*.m"]),
    (&["objcpp"], &["*.h", "*.mm"]),
    (&["ocaml"], &["*.ml", "*.mli", "*.mll", "*.mly"]),
    (&["org"], &["*.org", "*.org_archive"]),
    (&["pants"], &["BUILD"]),
    (&["pascal"], &["*.pas", "*.dpr", "*.lpr", "*.pp", "*.inc"]),
    (&["pdf"], &["*.pdf"]),
    (&["perl"], &["*.perl", "*.pl", "*.PL", "*.plh", "*.plx", "*.pm", "*.t"]),
    (&["php"], &[
        // note that PHP 6 doesn't exist
        // See: https://wiki.php.net/rfc/php6
        "*.php", "*.php3", "*.php4", "*.php5", "*.php7", "*.php8",
        "*.pht", "*.phtml"
    ]),
    (&["po"], &["*.po"]),
    (&["pod"], &["*.pod"]),
    (&["postscript"], &["*.eps", "*.ps"]),
    (&["prolog"], &["*.pl", "*.pro", "*.prolog", "*.P"]),
    (&["protobuf"], &["*.proto"]),
    (&["ps"], &["*.cdxml", "*.ps1", "*.ps1xml", "*.psd1", "*.psm1"]),
    (&["puppet"], &["*.epp", "*.erb", "*.pp", "*.rb"]),
    (&["purs"], &["*.purs"]),
    (&["py", "python"], &["*.py", "*.pyi"]),
    (&["qmake"], &["*.pro", "*.pri", "*.prf"]),
    (&["qml"], &["*.qml"]),
    (&["qrc"], &["*.qrc"]),
    (&["qui"], &["*.ui"]),
    (&["r"], &["*.R", "*.r", "*.Rmd", "*.rmd", "*.Rnw", "*.rnw"]),
    (&["racket"], &["*.rkt"]),
    (&["raku"], &[
        "*.raku", "*.rakumod", "*.rakudoc", "*.rakutest",
        "*.p6", "*.pl6", "*.pm6"
    ]),
    (&["rdoc"], &["*.rdoc"]),
    (&["readme"], &["README*", "*README"]),
    (&["reasonml"], &["*.re", "*.rei"]),
    (&["red"], &["*.r", "*.red", "*.reds"]),
    (&["rescript"], &["*.res", "*.resi"]),
    (&["robot"], &["*.robot"]),
    (&["rst"], &["*.rst"]),
    (&["ruby"], &[
        // Idiomatic files
        "config.ru", "Gemfile", ".irbrc", "Rakefile",
        // Extensions
        "*.gemspec", "*.rb", "*.rbw", "*.rake"
    ]),
    (&["rust"], &["*.rs"]),
    (&["sass"], &["*.sass", "*.scss"]),
    (&["scala"], &["*.scala", "*.sbt"]),
    (&["scdoc"], &["*.scd", "*.scdoc"]),
    (&["seed7"], &["*.sd7", "*.s7i"]),
    (&["sh"], &[
        // Portable/misc. init files
        ".env", ".login", ".logout", ".profile", "profile",
        // bash-specific init files
        ".bash_login", "bash_login",
        ".bash_logout", "bash_logout",
        ".bash_profile", "bash_profile",
        ".bashrc", "bashrc", "*.bashrc",
        // csh-specific init files
        ".cshrc", "*.cshrc",
        // ksh-specific init files
        ".kshrc", "*.kshrc",
        // tcsh-specific init files
        ".tcshrc",
        // zsh-specific init files
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        // Extensions
        "*.bash", "*.csh", "*.env", "*.ksh", "*.sh", "*.tcsh", "*.zsh",
    ]),
    (&["slim"], &["*.skim", "*.slim", "*.slime"]),
    (&["smarty"], &["*.tpl"]),
    (&["sml"], &["*.sml", "*.sig"]),
    (&["solidity"], &["*.sol"]),
    (&["soy"], &["*.soy"]),
    (&["spark"], &["*.spark"]),
    (&["spec"], &["*.spec"]),
    (&["sql"], &["*.sql", "*.psql"]),
    (&["ssa"], &["*.ssa"]),
    (&["stylus"], &["*.styl"]),
    (&["sv"], &["*.v", "*.vg", "*.sv", "*.svh", "*.h"]),
    (&["svelte"], &["*.svelte", "*.svelte.ts"]),
    (&["svg"], &["*.svg"]),
    (&["swift"], &["*.swift"]),
    (&["swig"], &["*.def", "*.i"]),
    (&["systemd"], &[
        "*.automount", "*.conf", "*.device", "*.link", "*.mount", "*.path",
        "*.scope", "*.service", "*.slice", "*.socket", "*.swap", "*.target",
        "*.timer",
    ]),
    (&["taskpaper"], &["*.taskpaper"]),
    (&["tcl"], &["*.tcl"]),
    (&["tex"], &["*.tex", "*.ltx", "*.cls", "*.sty", "*.bib", "*.dtx", "*.ins"]),
    (&["texinfo"], &["*.texi"]),
    (&["textile"], &["*.textile"]),
    (&["tf"], &[
        "*.tf", "*.tf.json", "*.tfvars", "*.tfvars.json",
        "*.terraformrc", "terraform.rc", "*.tfrc", "*.terraform.lock.hcl",
    ]),
    (&["thrift"], &["*.thrift"]),
    (&["toml"], &["*.toml", "Cargo.lock"]),
    (&["ts", "typescript"], &["*.ts", "*.tsx", "*.cts", "*.mts"]),
    (&["twig"], &["*.twig"]),
    (&["txt"], &["*.txt"]),
    (&["typoscript"], &["*.typoscript", "*.ts"]),
    (&["typst"], &["*.typ"]),
    (&["usd"], &["*.usd", "*.usda", "*.usdc"]),
    (&["v"], &["*.v", "*.vsh"]),
    (&["vala"], &["*.vala"]),
    (&["vb"], &["*.vb"]),
    (&["vcl"], &["*.vcl"]),
    (&["verilog"], &["*.v", "*.vh", "*.sv", "*.svh"]),
    (&["vhdl"], &["*.vhd", "*.vhdl"]),
    (&["vim"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vimscript"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vue"], &["*.vue"]),
    (&["webidl"], &["*.idl", "*.webidl", "*.widl"]),
    (&["wgsl"], &["*.wgsl"]),
    (&["wiki"], &["*.mediawiki", "*.wiki"]),
    (&["xml"], &[
        "*.xml", "*.xml.dist", "*.dtd", "*.xsl", "*.xslt", "*.xsd", "*.xjb",
        "*.rng", "*.sch", "*.xhtml",
    ]),
    (&["xz"], &["*.xz", "*.txz"]),
    (&["yacc"], &["*.y"]),
    (&["yaml"], &["*.yaml", "*.yml"]),
    (&["yang"], &["*.yang"]),
    (&["z"], &["*.Z"]),
    (&["zig"], &["*.zig"]),
    (&["zsh"], &[
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        "*.zsh",
    ]),
    (&["zstd"], &["*.zst", "*.zstd"]),
];
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) const DEFAULT_TYPES: &[(&[&str], &[&str])] = &[
    (&["ada"], &["*.adb", "*.ads"]),
    (&["agda"], &["*.agda", "*.lagda"]),
    (&["aidl"], &["*.aidl"]),
    (&["alire"], &["alire.toml"]),
    (&["amake"], &["*.mk", "*.bp"]),
    (&["asciidoc"], &["*.adoc", "*.asc", "*.asciidoc"]),
    (&["asm"], &["*.asm", "*.s", "*.S"]),
    (&["asp"], &[
        "*.aspx", "*.aspx.cs", "*.aspx.vb", "*.ascx", "*.ascx.cs",
        "*.ascx.vb", "*.asp"
    ]),
    (&["ats"], &["*.ats", "*.dats", "*.sats", "*.hats"]),
    (&["avro"], &["*.avdl", "*.avpr", "*.avsc"]),
    (&["awk"], &["*.awk"]),
    (&["bat", "batch"], &["*.bat"]),
    (&["bazel"], &[
        "*.bazel", "*.bzl", "*.BUILD", "*.bazelrc", "BUILD", "MODULE.bazel",
        "WORKSPACE", "WORKSPACE.bazel", "WORKSPACE.bzlmod",
    ]),
    (&["bitbake"], &["*.bb", "*.bbappend", "*.bbclass", "*.conf", "*.inc"]),
    (&["boxlang"], &["*.bx", "*.bxm", "*.bxs"]),
    (&["brotli"], &["*.br"]),
    (&["buildstream"], &["*.bst"]),
    (&["bzip2"], &["*.bz2", "*.tbz2"]),
    (&["c"], &["*.[chH]", "*.[chH].in", "*.cats"]),
    (&["cabal"], &["*.cabal"]),
    (&["candid"], &["*.did"]),
    (&["carp"], &["*.carp"]),
    (&["cbor"], &["*.cbor"]),
    (&["ceylon"], &["*.ceylon"]),
    (&["cfml"], &["*.cfc", "*.cfm"]),
    (&["clojure"], &["*.clj", "*.cljc", "*.cljs", "*.cljx"]),
    (&["cmake"], &["*.cmake", "CMakeLists.txt"]),
    (&["cmd"], &["*.bat", "*.cmd"]),
    (&["cml"], &["*.cml"]),
    (&["coffeescript"], &["*.coffee"]),
    (&["config"], &["*.cfg", "*.conf", "*.config", "*.ini"]),
    (&["container"], &["*Containerfile*", "*Dockerfile*"]),
    (&["coq"], &["*.v"]),
    (&["cpp"], &[
        "*.[ChH]", "*.cc", "*.[ch]pp", "*.[ch]xx", "*.hh",  "*.inl",
        "*.[ChH].in", "*.cc.in", "*.[ch]pp.in", "*.[ch]xx.in", "*.hh.in",
    ]),
    (&["creole"], &["*.creole"]),
    (&["crystal"], &["Projectfile", "*.cr", "*.ecr", "shard.yml"]),
    (&["cs"], &["*.cs"]),
    (&["csharp"], &["*.cs"]),
    (&["cshtml"], &["*.cshtml"]),
    (&["csproj"], &["*.csproj"]),
    (&["css"], &["*.css", "*.scss"]),
    (&["csv"], &["*.csv"]),
    (&["cuda"], &["*.cu", "*.cuh"]),
    (&["cython"], &["*.pyx", "*.pxi", "*.pxd"]),
    (&["d"], &["*.d"]),
    (&["dart"], &["*.dart"]),
    (&["devicetree"], &["*.dts", "*.dtsi", "*.dtso"]),
    (&["dhall"], &["*.dhall"]),
    (&["diff"], &["*.patch", "*.diff"]),
    (&["dita"], &["*.dita", "*.ditamap", "*.ditaval"]),
    (&["docker"], &["*Dockerfile*"]),
    (&["dockercompose"], &["docker-compose.yml", "docker-compose.*.yml"]),
    (&["dts"], &["*.dts", "*.dtsi"]),
    (&["dvc"], &["Dvcfile", "*.dvc"]),
    (&["ebuild"], &["*.ebuild", "*.eclass"]),
    (&["edn"], &["*.edn"]),
    (&["elisp"], &["*.el"]),
    (&["elixir"], &["*.ex", "*.eex", "*.exs", "*.heex", "*.leex", "*.livemd"]),
    (&["elm"], &["*.elm"]),
    (&["erb"], &["*.erb"]),
    (&["erlang"], &["*.erl", "*.hrl"]),
    (&["fennel"], &["*.fnl"]),
    (&["fidl"], &["*.fidl"]),
    (&["fish"], &["*.fish"]),
    (&["flatbuffers"], &["*.fbs"]),
    (&["fortran"], &[
        "*.f", "*.F", "*.f77", "*.F77", "*.pfo",
        "*.f90", "*.F90", "*.f95", "*.F95",
    ]),
    (&["fsharp"], &["*.fs", "*.fsx", "*.fsi"]),
    (&["fut"], &["*.fut"]),
    (&["gap"], &["*.g", "*.gap", "*.gi", "*.gd", "*.tst"]),
    (&["gdscript"], &["*.gd"]),
    (&["gleam"], &["*.gleam"]),
    (&["gn"], &["*.gn", "*.gni"]),
    (&["go"], &["*.go"]),
    (&["gprbuild"], &["*.gpr"]),
    (&["gradle"], &[
        "*.gradle", "*.gradle.kts", "gradle.properties", "gradle-wrapper.*",
        "gradlew", "gradlew.bat",
    ]),
    (&["graphql"], &["*.graphql", "*.graphqls"]),
    (&["groovy"], &["*.groovy", "*.gradle"]),
    (&["gzip"], &["*.gz", "*.tgz"]),
    (&["h"], &["*.h", "*.hh", "*.hpp"]),
    (&["haml"], &["*.haml"]),
    (&["hare"], &["*.ha"]),
    (&["haskell"], &["*.hs", "*.lhs", "*.cpphs", "*.c2hs", "*.hsc"]),
    (&["hbs"], &["*.hbs"]),
    (&["hs"], &["*.hs", "*.lhs"]),
    (&["html"], &["*.htm", "*.html", "*.ejs"]),
    (&["hurl"], &["*.hurl"]),
    (&["hy"], &["*.hy"]),
    (&["idris"], &["*.idr", "*.lidr"]),
    (&["janet"], &["*.janet"]),
    (&["java"], &["*.java", "*.jsp", "*.jspx", "*.properties"]),
    (&["jinja"], &["*.j2", "*.jinja", "*.jinja2"]),
    (&["jl"], &["*.jl"]),
    (&["js"], &["*.js", "*.jsx", "*.vue", "*.cjs", "*.mjs"]),
    (&["json"], &["*.json", "composer.lock", "*.sarif"]),
    (&["jsonl"], &["*.jsonl"]),
    (&["julia"], &["*.jl"]),
    (&["jupyter"], &["*.ipynb", "*.jpynb"]),
    (&["k"], &["*.k"]),
    (&["kconfig"], &["Kconfig", "Kconfig.*"]),
    (&["kotlin"], &["*.kt", "*.kts"]),
    (&["lean"], &["*.lean"]),
    (&["less"], &["*.less"]),
    (&["license"], &[
        // General
        "COPYING", "COPYING[.-]*",
        "COPYRIGHT", "COPYRIGHT[.-]*",
        "EULA", "EULA[.-]*",
        "licen[cs]e", "licen[cs]e.*",
        "LICEN[CS]E", "LICEN[CS]E[.-]*", "*[.-]LICEN[CS]E*",
        "NOTICE", "NOTICE[.-]*",
        "PATENTS", "PATENTS[.-]*",
        "UNLICEN[CS]E", "UNLICEN[CS]E[.-]*",
        // GPL (gpl.txt, etc.)
        "agpl[.-]*",
        "gpl[.-]*",
        "lgpl[.-]*",
        // Other license-specific (APACHE-2.0.txt, etc.)
        "AGPL-*[0-9]*",
        "APACHE-*[0-9]*",
        "BSD-*[0-9]*",
        "CC-BY-*",
        "GFDL-*[0-9]*",
        "GNU-*[0-9]*",
        "GPL-*[0-9]*",
        "LGPL-*[0-9]*",
        "MIT-*[0-9]*",
        "MPL-*[0-9]*",
        "OFL-*[0-9]*",
    ]),
    (&["lilypond"], &["*.ly", "*.ily"]),
    (&["lisp"], &["*.el", "*.jl", "*.lisp", "*.lsp", "*.sc", "*.scm"]),
    (&["llvm"], &["*.ll"]),
    (&["lock"], &["*.lock", "package-lock.json"]),
    (&["log"], &["*.log"]),
    (&["lua"], &["*.lua"]),
    (&["lz4"], &["*.lz4"]),
    (&["lzma"], &["*.lzma"]),
    (&["m4"], &["*.ac", "*.m4"]),
    (&["make"], &[
        "[Gg][Nn][Uu]makefile", "[Mm]akefile",
        "[Gg][Nn][Uu]makefile.am", "[Mm]akefile.am",
        "[Gg][Nn][Uu]makefile.in", "[Mm]akefile.in",
        "Makefile.*",
        "*.mk", "*.mak"
    ]),
    (&["mako"], &["*.mako", "*.mao"]),
    (&["man"], &["*.[0-9lnpx]", "*.[0-9][cEFMmpSx]"]),
    (&["markdown", "md"], &[
        "*.markdown",
        "*.md",
        "*.mdown",
        "*.mdwn",
        "*.mkd",
        "*.mkdn",
        "*.mdx",
    ]),
    (&["matlab"], &["*.m"]),
    (&["meson"], &["meson.build", "meson_options.txt", "meson.options"]),
    (&["minified"], &["*.min.html", "*.min.css", "*.min.js"]),
    (&["mint"], &["*.mint"]),
    (&["mk"], &["mkfile"]),
    (&["ml"], &["*.ml"]),
    (&["mojo"], &["*.mojo"]),
    (&["motoko"], &["*.mo"]),
    (&["msbuild"], &[
        "*.csproj", "*.fsproj", "*.vcxproj", "*.proj", "*.props", "*.targets",
        "*.sln", "*.slnf"
    ]),
    (&["nim"], &["*.nim", "*.nimf", "*.nimble", "*.nims"]),
    (&["nix"], &["*.nix"]),
    (&["objc"], &["*.h", "*.m"]),
    (&["objcpp"], &["*.h", "*.mm"]),
    (&["ocaml"], &["*.ml", "*.mli", "*.mll", "*.mly"]),
    (&["org"], &["*.org", "*.org_archive"]),
    (&["pants"], &["BUILD"]),
    (&["pascal"], &["*.pas", "*.dpr", "*.lpr", "*.pp", "*.inc"]),
    (&["pdf"], &["*.pdf"]),
    (&["perl"], &["*.perl", "*.pl", "*.PL", "*.plh", "*.plx", "*.pm", "*.t"]),
    (&["php"], &[
        // note that PHP 6 doesn't exist
        // See: https://wiki.php.net/rfc/php6
        "*.php", "*.php3", "*.php4", "*.php5", "*.php7", "*.php8",
        "*.pht", "*.phtml"
    ]),
    (&["po"], &["*.po"]),
    (&["pod"], &["*.pod"]),
    (&["postscript"], &["*.eps", "*.ps"]),
    (&["prolog"], &["*.pl", "*.pro", "*.prolog", "*.P"]),
    (&["protobuf"], &["*.proto"]),
    (&["ps"], &["*.cdxml", "*.ps1", "*.ps1xml", "*.psd1", "*.psm1"]),
    (&["puppet"], &["*.epp", "*.erb", "*.pp", "*.rb"]),
    (&["purs"], &["*.purs"]),
    (&["py", "python"], &["*.py", "*.pyi"]),
    (&["qmake"], &["*.pro", "*.pri", "*.prf"]),
    (&["qml"], &["*.qml"]),
    (&["qrc"], &["*.qrc"]),
    (&["qui"], &["*.ui"]),
    (&["r"], &["*.R", "*.r", "*.Rmd", "*.rmd", "*.Rnw", "*.rnw"]),
    (&["racket"], &["*.rkt"]),
    (&["raku"], &[
        "*.raku", "*.rakumod", "*.rakudoc", "*.rakutest",
        "*.p6", "*.pl6", "*.pm6"
    ]),
    (&["rdoc"], &["*.rdoc"]),
    (&["readme"], &["README*", "*README"]),
    (&["reasonml"], &["*.re", "*.rei"]),
    (&["red"], &["*.r", "*.red", "*.reds"]),
    (&["rescript"], &["*.res", "*.resi"]),
    (&["robot"], &["*.robot"]),
    (&["rst"], &["*.rst"]),
    (&["ruby"], &[
        // Idiomatic files
        "config.ru", "Gemfile", ".irbrc", "Rakefile",
        // Extensions
        "*.gemspec", "*.rb", "*.rbw", "*.rake"
    ]),
    (&["rust"], &["*.rs"]),
    (&["sass"], &["*.sass", "*.scss"]),
    (&["scala"], &["*.scala", "*.sbt"]),
    (&["scdoc"], &["*.scd", "*.scdoc"]),
    (&["seed7"], &["*.sd7", "*.s7i"]),
    (&["sh"], &[
        // Portable/misc. init files
        ".env", ".login", ".logout", ".profile", "profile",
        // bash-specific init files
        ".bash_login", "bash_login",
        ".bash_logout", "bash_logout",
        ".bash_profile", "bash_profile",
        ".bashrc", "bashrc", "*.bashrc",
        // csh-specific init files
        ".cshrc", "*.cshrc",
        // ksh-specific init files
        ".kshrc", "*.kshrc",
        // tcsh-specific init files
        ".tcshrc",
        // zsh-specific init files
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        // Extensions
        "*.bash", "*.csh", "*.env", "*.ksh", "*.sh", "*.tcsh", "*.zsh",
    ]),
    (&["slim"], &["*.skim", "*.slim", "*.slime"]),
    (&["smarty"], &["*.tpl"]),
    (&["sml"], &["*.sml", "*.sig"]),
    (&["solidity"], &["*.sol"]),
    (&["soy"], &["*.soy"]),
    (&["spark"], &["*.spark"]),
    (&["spec"], &["*.spec"]),
    (&["sql"], &["*.sql", "*.psql"]),
    (&["ssa"], &["*.ssa"]),
    (&["stylus"], &["*.styl"]),
    (&["sv"], &["*.v", "*.vg", "*.sv", "*.svh", "*.h"]),
    (&["svelte"], &["*.svelte", "*.svelte.ts"]),
    (&["svg"], &["*.svg"]),
    (&["swift"], &["*.swift"]),
    (&["swig"], &["*.def", "*.i"]),
    (&["systemd"], &[
        "*.automount", "*.conf", "*.device", "*.link", "*.mount", "*.path",
        "*.scope", "*.service", "*.slice", "*.socket", "*.swap", "*.target",
        "*.timer",
    ]),
    (&["taskpaper"], &["*.taskpaper"]),
    (&["tcl"], &["*.tcl"]),
    (&["tex"], &["*.tex", "*.ltx", "*.cls", "*.sty", "*.bib", "*.dtx", "*.ins"]),
    (&["texinfo"], &["*.texi"]),
    (&["textile"], &["*.textile"]),
    (&["tf"], &[
        "*.tf", "*.tf.json", "*.tfvars", "*.tfvars.json",
        "*.terraformrc", "terraform.rc", "*.tfrc", "*.terraform.lock.hcl",
    ]),
    (&["thrift"], &["*.thrift"]),
    (&["toml"], &["*.toml", "Cargo.lock"]),
    (&["ts", "typescript"], &["*.ts", "*.tsx", "*.cts", "*.mts"]),
    (&["twig"], &["*.twig"]),
    (&["txt"], &["*.txt"]),
    (&["typoscript"], &["*.typoscript", "*.ts"]),
    (&["typst"], &["*.typ"]),
    (&["usd"], &["*.usd", "*.usda", "*.usdc"]),
    (&["v"], &["*.v", "*.vsh"]),
    (&["vala"], &["*.vala"]),
    (&["vb"], &["*.vb"]),
    (&["vcl"], &["*.vcl"]),
    (&["verilog"], &["*.v", "*.vh", "*.sv", "*.svh"]),
    (&["vhdl"], &["*.vhd", "*.vhdl"]),
    (&["vim"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vimscript"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vue"], &["*.vue"]),
    (&["webidl"], &["*.idl", "*.webidl", "*.widl"]),
    (&["wgsl"], &["*.wgsl"]),
    (&["wiki"], &["*.mediawiki", "*.wiki"]),
    (&["xml"], &[
        "*.xml", "*.xml.dist", "*.dtd", "*.xsl", "*.xslt", "*.xsd", "*.xjb",
        "*.rng", "*.sch", "*.xhtml",
    ]),
    (&["xz"], &["*.xz", "*.txz"]),
    (&["yacc"], &["*.y"]),
    (&["yaml"], &["*.yaml", "*.yml"]),
    (&["yang"], &["*.yang"]),
    (&["z"], &["*.Z"]),
    (&["zig"], &["*.zig"]),
    (&["zsh"], &[
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        "*.zsh",
    ]),
    (&["zstd"], &["*.zst", "*.zstd"]),
];
```


---

### 🔹 Commit #14: `f55548ba`
- **完整 Hash**: `f55548ba9f24dda192880d4a3da2b52e90f6e194`
- **說明 (Ground Truth)**: globset: fix `matches_all` false positives
- **變更檔案數**: 1

#### 📄 檔案: `crates/globset/src/lib.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:190, E:275, A:0) ➔ After(N:210, E:317, A:0)
- **差分統計**: +Nodes: 23, -Nodes: 3, +Edges: 56, -Edges: 14, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `matches_all_extensions` (FUNCTION_DEF)
  • + [新增節點] `SuffixStrategy::matches_all` (FUNCTION_DEF)
  • + [新增節點] `GlobSet::new(&[
            GlobBuilder::new("c*").case_insensitive(true).build().unwrap(),
            Glob::new("*{rs,c}").unwrap(),
        ])
        .unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `RegexSetStrategy::matches_all` (FUNCTION_DEF)
  • + [新增節點] `Glob::new("*{rs,c}").unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `RequiredExtensionStrategy::matches_all` (FUNCTION_DEF)
  • + [新增節點] `build_glob_set` (FUNCTION_DEF)
  • + [新增節點] `matches_all_literals` (FUNCTION_DEF)
  • + [新增節點] `RegexSetStrategy::find_matches` (FUNCTION_DEF)
  • + [新增節點] `matches_all_suffix` (FUNCTION_DEF)
  • + [新增節點] `matches_all_required_extensions` (FUNCTION_DEF)
  • + [新增節點] `LiteralStrategy::matches_all` (FUNCTION_DEF)
  • + [新增節點] `PrefixStrategy::matches_all` (FUNCTION_DEF)
  • + [新增節點] `GlobSetMatchStrategy::matches_all` (FUNCTION_DEF)
  • + [新增節點] `GlobBuilder::new("c*").case_insensitive (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 81 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `GlobSet::matches_all_candidate()`
- **變更前簽章 (Before)**: `fn GlobSet::matches_all_candidate(&self, path: &Candidate<'_>)` (L390~L397)
- **變更後簽章 (After)**: `fn GlobSet::matches_all_candidate(&self, path: &Candidate<'_>)` (L390~L397)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn matches_all_candidate(&self, path: &Candidate<'_>) -> bool {
        for strat in &self.strats {
            if !strat.is_match(path) {
                return false;
            }
        }
        true
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn matches_all_candidate(&self, path: &Candidate<'_>) -> bool {
        for strat in &self.strats {
            if !strat.matches_all(path) {
                return false;
            }
        }
        true
    }
```

### 🔹 函式: `set_works()`
- **變更前簽章 (Before)**: `fn set_works()` (L1061~L1079)
- **變更後簽章 (After)**: `fn set_works()` (L1149~L1166)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn set_works() {
        let mut builder = GlobSetBuilder::new();
        builder.add(Glob::new("src/**/*.rs").unwrap());
        builder.add(Glob::new("*.c").unwrap());
        builder.add(Glob::new("src/lib.rs").unwrap());
        let set = builder.build().unwrap();

        assert!(set.is_match("foo.c"));
        assert!(set.is_match("src/foo.c"));
        assert!(!set.is_match("foo.rs"));
        assert!(!set.is_match("tests/foo.rs"));
        assert!(set.is_match("src/foo.rs"));
        assert!(set.is_match("src/grep/src/main.rs"));

        let matches = set.matches("src/lib.rs");
        assert_eq!(2, matches.len());
        assert_eq!(0, matches[0]);
        assert_eq!(2, matches[1]);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn set_works() {
        let set = build_glob_set(&["src/**/*.rs", "*.c", "src/lib.rs"]);

        assert!(set.is_match("foo.c"));
        assert!(set.is_match("src/foo.c"));
        assert!(!set.is_match("foo.rs"));
        assert!(!set.is_match("tests/foo.rs"));
        assert!(set.is_match("src/foo.rs"));
        assert!(set.is_match("src/grep/src/main.rs"));

        assert!(!set.matches_all("src/lib.rs"));
        assert!(!set.matches_all("src/a/b.c"));

        let matches = set.matches("src/lib.rs");
        assert_eq!(2, matches.len());
        assert_eq!(0, matches[0]);
        assert_eq!(2, matches[1]);
    }
```

### 🔹 函式: `RegexSetStrategy::matches_into()`
- **變更前簽章 (Before)**: `fn RegexSetStrategy::matches_into(
        &self,
        candidate: &Candidate<'_>,
        matches: &mut Vec<usize>,
    )` (L919~L932)
- **變更後簽章 (After)**: `fn RegexSetStrategy::matches_into(
        &self,
        candidate: &Candidate<'_>,
        matches: &mut Vec<usize>,
    )` (L1002~L1012)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn matches_into(
        &self,
        candidate: &Candidate<'_>,
        matches: &mut Vec<usize>,
    ) {
        let input = regex_automata::Input::new(candidate.path.as_bytes());
        let mut patset = self.patset.get();
        patset.clear();
        self.matcher.which_overlapping_matches(&input, &mut patset);
        for i in patset.iter() {
            matches.push(self.map[i]);
        }
        PoolGuard::put(patset);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn matches_into(
        &self,
        candidate: &Candidate<'_>,
        matches: &mut Vec<usize>,
    ) {
        let patset = self.find_matches(candidate);
        for i in patset.iter() {
            matches.push(self.map[i]);
        }
        PoolGuard::put(patset);
    }
```


---

### 🔹 Commit #15: `68b3c9e0`
- **完整 Hash**: `68b3c9e0d95950cfc835fb07924457919a4ec07d`
- **說明 (Ground Truth)**: ignore: fetch directory entry metadata in batches
- **變更檔案數**: 2

#### 📄 檔案: `crates/ignore/src/dir.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:236, E:440, A:0) ➔ After(N:254, E:463, A:0)
- **差分統計**: +Nodes: 18, -Nodes: 0, +Edges: 47, -Edges: 24, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `entry.file_name (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self
                    .inner
                    .custom_ignore_filenames
                    .iter()
                    .zip(m.custom_ignore_files.iter())
                    .filter(|&(_, &matched)| matched)
                    .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `name.as_os_str (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.inner.custom_ignore_filenames.iter().collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.inner.custom_ignore_filenames.iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `m.custom_ignore_files.iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self
                    .inner
                    .custom_ignore_filenames
                    .iter()
                    .zip(m.custom_ignore_files.iter())
                    .filter(|&(_, &matched)| matched)
                    .map(|(name, _)| name)
                    .collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Ignore::collect_ignore_files` (FUNCTION_DEF)
  • + [新增節點] `Ignore::add_child_with_entries` (FUNCTION_DEF)
  • + [新增節點] `self
                    .inner
                    .custom_ignore_filenames
                    .iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `custom_ignore_names.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self
                    .inner
                    .custom_ignore_filenames
                    .iter()
                    .zip (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `custom_ignore_filenames.iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `custom_ignore_filenames.iter().enumerate (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Ignore::add_child_path_with_found_ignore_files` (FUNCTION_DEF)
  • _... 以及其餘 74 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Ignore::add_child_path()`
- **變更前簽章 (Before)**: `fn Ignore::add_child_path(&self, dir: &Path)` (L283~L378)
- **變更後簽章 (After)**: `fn Ignore::add_child_path(&self, dir: &Path)` (L304~L306)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn add_child_path(&self, dir: &Path) -> (IgnoreInner, Option<Error>) {
        let check_vcs_dir = self.inner.opts.require_git
            && (self.inner.opts.git_ignore || self.inner.opts.git_exclude);
        let git_type = if check_vcs_dir {
            dir.join(".git").metadata().ok().map(|md| md.file_type())
        } else {
            None
        };
        let has_git =
            check_vcs_dir && (git_type.is_some() || dir.join(".jj").exists());

        let mut errs = PartialErrorBuilder::default();
        let custom_ig_matcher =
            if self.inner.custom_ignore_filenames.is_empty() {
                Gitignore::empty()
            } else {
                let (m, err) = create_gitignore(
                    &dir,
                    &dir,
                    &self.inner.custom_ignore_filenames,
                    self.inner.opts.ignore_case_insensitive,
                );
                errs.maybe_push(err);
                m
            };
        let ig_matcher = if !self.inner.opts.ignore {
            Gitignore::empty()
        } else {
            let (m, err) = create_gitignore(
                &dir,
                &dir,
                &[".ignore"],
                self.inner.opts.ignore_case_insensitive,
            );
            errs.maybe_push(err);
            m
        };
        let gi_matcher = if !self.inner.opts.git_ignore {
            Gitignore::empty()
        } else {
            let (m, err) = create_gitignore(
                &dir,
                &dir,
                &[".gitignore"],
                self.inner.opts.ignore_case_insensitive,
            );
            errs.maybe_push(err);
            m
        };

        let gi_exclude_matcher = if !self.inner.opts.git_exclude {
            Gitignore::empty()
        } else {
            match resolve_git_commondir(dir, git_type) {
                Ok(git_dir) => {
                    let (m, err) = create_gitignore(
                        &dir,
                        &git_dir,
                        &["info/exclude"],
                        self.inner.opts.ignore_case_insensitive,
                    );
                    errs.maybe_push(err);
                    m
                }
                Err(err) => {
                    errs.maybe_push(err);
                    Gitignore::empty()
                }
            }
        };
        let ig = IgnoreInner {
            compiled: self.inner.compiled.clone(),
            dir: dir.to_path_buf(),
            overrides: self.inner.overrides.clone(),
            types: self.inner.types.clone(),
            parent: Some(self.inner.clone()),
            is_absolute_parent: false,
            global_gitignores_relative_to: self
                .inner
                .global_gitignores_relative_to
                .clone(),
            explicit_ignores: self.inner.explicit_ignores.clone(),
            custom_ignore_filenames: self
                .inner
                .custom_ignore_filenames
                .clone(),
            custom_ignore_matcher: custom_ig_matcher,
            ignore_matcher: ig_matcher,
            git_global_matcher: self.inner.git_global_matcher.clone(),
            git_ignore_matcher: gi_matcher,
            git_exclude_matcher: gi_exclude_matcher,
            has_git,
            opts: self.inner.opts,
        };
        (ig, errs.into_error_option())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn add_child_path(&self, dir: &Path) -> (IgnoreInner, Option<Error>) {
        self.add_child_path_with_found_ignore_files(dir, None)
    }
```


#### 📄 檔案: `crates/ignore/src/walk.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:385, E:685, A:0) ➔ After(N:389, E:691, A:0)
- **差分統計**: +Nodes: 6, -Nodes: 2, +Edges: 10, -Edges: 4, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `ReadDirResult::default (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self
            .ignore
            .add_child_with_entries (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Work::add_ignore` (FUNCTION_DEF)
  • + [新增節點] `Error::from(err)
                        .with_path (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Error::from(err)
                        .with_path(self.dent.path())
                        .with_depth (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.max_depth.is_none_or (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `Error::from(err).with_depth (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `self.max_depth.map_or (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Work::add_ignore` ──[CALLS]──> `self.ignore.add_child (External/Unresolved)`
  • + [新增呼叫邊] `Work::add_ignore` ──[CALLS]──> `DirEntryRaw::path`
  • + [新增呼叫邊] `Work::read_dir` ──[CALLS]──> `ReadDirResult::default (External/Unresolved)`
  • + [新增呼叫邊] `Work::read_dir` ──[CALLS]──> `Stack::push`
  • + [新增呼叫邊] `Work::read_dir` ──[CALLS]──> `Error::from(err)
                        .with_path(self.dent.path())
                        .with_depth (External/Unresolved)`
  • + [新增呼叫邊] `Work::read_dir` ──[CALLS]──> `Error::from(err)
                        .with_path (External/Unresolved)`
  • + [新增呼叫邊] `Work::read_dir` ──[CALLS]──> `self
            .ignore
            .add_child_with_entries (External/Unresolved)`
  • _... 以及其餘 7 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Worker::run_one()`
- **變更前簽章 (Before)**: `fn Worker::run_one(&mut self, mut work: Work)` (L1642~L1720)
- **變更後簽章 (After)**: `fn Worker::run_one(&mut self, mut work: Work)` (L1669~L1759)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn run_one(&mut self, mut work: Work) -> WalkState {
        let should_visit = self
            .min_depth
            .map(|min_depth| work.dent.depth() >= min_depth)
            .unwrap_or(true);

        // If the work is not a directory, then we can just execute the
        // caller's callback immediately and move on.
        if work.is_symlink() || !work.is_dir() {
            return if should_visit {
                self.visitor.visit(Ok(work.dent))
            } else {
                WalkState::Continue
            };
        }
        if let Some(err) = work.add_parents() {
            let state = self.visitor.visit(Err(err));
            if state.is_quit() {
                return state;
            }
        }

        let descend = if let Some(root_device) = work.root_device {
            match is_same_file_system(root_device, work.dent.path()) {
                Ok(true) => true,
                Ok(false) => false,
                Err(err) => {
                    let state = self.visitor.visit(Err(err));
                    if state.is_quit() {
                        return state;
                    }
                    false
                }
            }
        } else {
            true
        };

        // Try to read the directory first before we transfer ownership
        // to the provided closure. Do not unwrap it immediately, though,
        // as we may receive an `Err` value e.g. in the case when we do not
        // have sufficient read permissions to list the directory.
        // In that case we still want to provide the closure with a valid
        // entry before passing the error value.
        let readdir = work.read_dir();
        let depth = work.dent.depth();
        if should_visit {
            let state = self.visitor.visit(Ok(work.dent));
            if !state.is_continue() {
                return state;
            }
        }
        if !descend {
            return WalkState::Skip;
        }

        let readdir = match readdir {
            Ok(readdir) => readdir,
            Err(err) => {
                return self.visitor.visit(Err(err));
            }
        };

        if self.max_depth.map_or(false, |max| depth >= max) {
            return WalkState::Skip;
        }
        for result in readdir {
            let state = self.generate_work(
                &work.ignore,
                depth + 1,
                work.root_device,
                result,
            );
            if state.is_quit() {
                return state;
            }
        }
        WalkState::Continue
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn run_one(&mut self, mut work: Work) -> WalkState {
        let should_visit = self
            .min_depth
            .map(|min_depth| work.dent.depth() >= min_depth)
            .unwrap_or(true);

        // If the work is not a directory, then we can just execute the
        // caller's callback immediately and move on.
        if work.is_symlink() || !work.is_dir() {
            return if should_visit {
                self.visitor.visit(Ok(work.dent))
            } else {
                WalkState::Continue
            };
        }
        if let Some(err) = work.add_parents() {
            let state = self.visitor.visit(Err(err));
            if state.is_quit() {
                return state;
            }
        }

        let descend = if let Some(root_device) = work.root_device {
            match is_same_file_system(root_device, work.dent.path()) {
                Ok(true) => true,
                Ok(false) => false,
                Err(err) => {
                    let state = self.visitor.visit(Err(err));
                    if state.is_quit() {
                        return state;
                    }
                    false
                }
            }
        } else {
            true
        };

        // Try to read the directory first before we transfer ownership
        // to the provided closure. Do not unwrap it immediately, though,
        // as we may receive an `Err` value e.g. in the case when we do not
        // have sufficient read permissions to list the directory.
        // In that case we still want to provide the closure with a valid
        // entry before passing the error value.
        let depth = work.dent.depth();
        let readdir = if descend && self.max_depth.is_none_or(|m| depth < m) {
            Some(work.read_dir())
        } else {
            work.add_ignore();
            None
        };
        if should_visit {
            let state = self.visitor.visit(Ok(work.dent));
            if !state.is_continue() {
                return state;
            }
        }
        if !descend {
            return WalkState::Skip;
        }

        let readdir = match readdir {
            Some(readdir) => readdir,
            None => return WalkState::Skip,
        };
        let readdir = match readdir {
            Ok(readdir) => readdir,
            Err(err) => {
                return self.visitor.visit(Err(err));
            }
        };

        for result in readdir.entries {
            let state = self.generate_work(
                &work.ignore,
                depth + 1,
                work.root_device,
                result,
            );
            if state.is_quit() {
                return state;
            }
        }
        for err in readdir.errors {
            let state = self.visitor.visit(Err(err));
            if state.is_quit() {
                return state;
            }
        }
        WalkState::Continue
    }
```

### 🔹 函式: `Work::read_dir()`
- **變更前簽章 (Before)**: `fn Work::read_dir(&mut self)` (L1503~L1517)
- **變更後簽章 (After)**: `fn Work::read_dir(&mut self)` (L1516~L1544)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn read_dir(&mut self) -> Result<fs::ReadDir, Error> {
        let readdir = match fs::read_dir(self.dent.path()) {
            Ok(readdir) => readdir,
            Err(err) => {
                let err = Error::from(err)
                    .with_path(self.dent.path())
                    .with_depth(self.dent.depth());
                return Err(err);
            }
        };
        let (ig, err) = self.ignore.add_child(self.dent.path());
        self.ignore = ig;
        self.dent.err = err;
        Ok(readdir)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn read_dir(&mut self) -> Result<ReadDirResult, Error> {
        let readdir = match fs::read_dir(self.dent.path()) {
            Ok(readdir) => readdir,
            Err(err) => {
                let err = Error::from(err)
                    .with_path(self.dent.path())
                    .with_depth(self.dent.depth());
                return Err(err);
            }
        };
        // Actually descend into the directory and read its contents
        let mut result = ReadDirResult::default();
        for entry in readdir {
            match entry {
                Ok(entry) => result.entries.push(entry),
                Err(err) => result.errors.push(
                    Error::from(err)
                        .with_path(self.dent.path())
                        .with_depth(self.dent.depth() + 1),
                ),
            }
        }
        let (ig, err) = self
            .ignore
            .add_child_with_entries(self.dent.path(), &result.entries);
        self.ignore = ig;
        self.dent.err = err;
        Ok(result)
    }
```

### 🔹 函式: `Worker::generate_work()`
- **變更前簽章 (Before)**: `fn Worker::generate_work(
        &mut self,
        ig: &Ignore,
        depth: usize,
        root_device: Option<u64>,
        result: Result<fs::DirEntry, io::Error>,
    )` (L1735~L1805)
- **變更後簽章 (After)**: `fn Worker::generate_work(
        &mut self,
        ig: &Ignore,
        depth: usize,
        root_device: Option<u64>,
        fs_dent: fs::DirEntry,
    )` (L1774~L1836)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn generate_work(
        &mut self,
        ig: &Ignore,
        depth: usize,
        root_device: Option<u64>,
        result: Result<fs::DirEntry, io::Error>,
    ) -> WalkState {
        let fs_dent = match result {
            Ok(fs_dent) => fs_dent,
            Err(err) => {
                return self
                    .visitor
                    .visit(Err(Error::from(err).with_depth(depth)));
            }
        };
        let mut dent = match DirEntryRaw::from_entry(depth, &fs_dent) {
            Ok(dent) => DirEntry::new_raw(dent, None),
            Err(err) => {
                return self.visitor.visit(Err(err));
            }
        };
        let is_symlink = dent.file_type().map_or(false, |ft| ft.is_symlink());
        if self.follow_links && is_symlink {
            let path = dent.path().to_path_buf();
            dent = match DirEntryRaw::from_path(depth, path, true) {
                Ok(dent) => DirEntry::new_raw(dent, None),
                Err(err) => {
                    return self.visitor.visit(Err(err));
                }
            };
            if dent.is_dir() {
                if let Err(err) = check_symlink_loop(ig, dent.path(), depth) {
                    return self.visitor.visit(Err(err));
                }
            }
        }
        // N.B. See analogous call in the single-threaded implementation about
        // why it's important for this to come before the checks below.
        if should_skip_entry(ig, &dent) {
            return WalkState::Continue;
        }
        if let Some(ref stdout) = self.skip {
            let is_stdout = match path_equals(&dent, stdout) {
                Ok(is_stdout) => is_stdout,
                Err(err) => return self.visitor.visit(Err(err)),
            };
            if is_stdout {
                return WalkState::Continue;
            }
        }
        let should_skip_filesize =
            if self.max_filesize.is_some() && !dent.is_dir() {
                skip_filesize(
                    self.max_filesize.unwrap(),
                    dent.path(),
                    &dent.metadata().ok(),
                )
            } else {
                false
            };
        let should_skip_filtered =
            if let Some(Filter(predicate)) = &self.filter {
                !predicate(&dent)
            } else {
                false
            };
        if !should_skip_filesize && !should_skip_filtered {
            self.send(Work { dent, ignore: ig.clone(), root_device });
        }
        WalkState::Continue
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn generate_work(
        &mut self,
        ig: &Ignore,
        depth: usize,
        root_device: Option<u64>,
        fs_dent: fs::DirEntry,
    ) -> WalkState {
        let mut dent = match DirEntryRaw::from_entry(depth, &fs_dent) {
            Ok(dent) => DirEntry::new_raw(dent, None),
            Err(err) => {
                return self.visitor.visit(Err(err));
            }
        };
        let is_symlink = dent.file_type().map_or(false, |ft| ft.is_symlink());
        if self.follow_links && is_symlink {
            let path = dent.path().to_path_buf();
            dent = match DirEntryRaw::from_path(depth, path, true) {
                Ok(dent) => DirEntry::new_raw(dent, None),
                Err(err) => {
                    return self.visitor.visit(Err(err));
                }
            };
            if dent.is_dir() {
                if let Err(err) = check_symlink_loop(ig, dent.path(), depth) {
                    return self.visitor.visit(Err(err));
                }
            }
        }
        // N.B. See analogous call in the single-threaded implementation about
        // why it's important for this to come before the checks below.
        if should_skip_entry(ig, &dent) {
            return WalkState::Continue;
        }
        if let Some(ref stdout) = self.skip {
            let is_stdout = match path_equals(&dent, stdout) {
                Ok(is_stdout) => is_stdout,
                Err(err) => return self.visitor.visit(Err(err)),
            };
            if is_stdout {
                return WalkState::Continue;
            }
        }
        let should_skip_filesize =
            if self.max_filesize.is_some() && !dent.is_dir() {
                skip_filesize(
                    self.max_filesize.unwrap(),
                    dent.path(),
                    &dent.metadata().ok(),
                )
            } else {
                false
            };
        let should_skip_filtered =
            if let Some(Filter(predicate)) = &self.filter {
                !predicate(&dent)
            } else {
                false
            };
        if !should_skip_filesize && !should_skip_filtered {
            self.send(Work { dent, ignore: ig.clone(), root_device });
        }
        WalkState::Continue
    }
```


---

### 🔹 Commit #16: `653d7f5b`
- **完整 Hash**: `653d7f5bd13762b97cf0bd6b7c5890cf3f54db4d`
- **說明 (Ground Truth)**: ignore: add multi-root parent matcher regression tests
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/dir.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:229, E:403, A:0) ➔ After(N:236, E:440, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 37, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `std::env::current_dir().unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `td.path().strip_prefix (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `multi_root_custom_ignore_order_independent` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `root.join (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `multi_root_gitignore_order_independent` (FUNCTION_DEF)
  • + [新增節點] `td.path().strip_prefix(&cwd).unwrap_or (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `multi_root_gitignore_order_independent` ──[CALLS]──> `tmpdir`
  • + [新增呼叫邊] `multi_root_gitignore_order_independent` ──[CALLS]──> `std::env::current_dir().unwrap (External/Unresolved)`
  • + [新增呼叫邊] `multi_root_gitignore_order_independent` ──[CALLS]──> `IgnoreBuilder::current_dir`
  • + [新增呼叫邊] `multi_root_gitignore_order_independent` ──[CALLS]──> `td.path().strip_prefix(&cwd).unwrap_or (External/Unresolved)`
  • + [新增呼叫邊] `multi_root_gitignore_order_independent` ──[CALLS]──> `td.path().strip_prefix (External/Unresolved)`
  • + [新增呼叫邊] `multi_root_gitignore_order_independent` ──[CALLS]──> `IgnoreRef::path`
  • + [新增呼叫邊] `multi_root_gitignore_order_independent` ──[CALLS]──> `root.join (External/Unresolved)`
  • + [新增呼叫邊] `multi_root_gitignore_order_independent` ──[CALLS]──> `mkdirp`
  • _... 以及其餘 29 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #17: `f127579b`
- **完整 Hash**: `f127579b006d9fb388050281d7d7146799a9cd4c`
- **說明 (Ground Truth)**: ignore: add depth to more errors
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/walk.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:379, E:679, A:0) ➔ After(N:385, E:685, A:0)
- **差分統計**: +Nodes: 9, -Nodes: 3, +Edges: 20, -Edges: 14, ΔFuncs: 7, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Error::Io(io::Error::from(err))
                    .with_depth(x.depth())
                    .with_path (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Error::Io(err).with_depth(self.depth).with_path (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Error::Io(err).with_depth (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Error::Io(err).with_depth(dent.depth()).with_path (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Handle::from_path(dent.path()).map(|h| &h == handle).map_err (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Error::Io(err).with_depth(depth).with_path (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `fs::metadata(&pb)
            .map_err (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Handle::from_path(dent.path()).map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Error::Io(io::Error::from(err))
                    .with_depth (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `Handle::from_path(dent.path())
        .map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `Handle::from_path(dent.path())
        .map(|h| &h == handle)
        .map_err (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `fs::metadata(&pb).map_err (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `DirEntryInner::metadata` ──[CALLS]──> `Error::Io(io::Error::from(err))
                    .with_depth(x.depth())
                    .with_path (External/Unresolved)`
  • + [新增呼叫邊] `DirEntryInner::metadata` ──[CALLS]──> `Error::Io(io::Error::from(err))
                    .with_depth (External/Unresolved)`
  • + [新增呼叫邊] `DirEntryInner::metadata` ──[CALLS]──> `DirEntryInner::depth`
  • _... 以及其餘 31 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `DirEntryInner::metadata()`
- **變更前簽章 (Before)**: `fn DirEntryInner::metadata(&self)` (L171~L186)
- **變更後簽章 (After)**: `fn DirEntryInner::metadata(&self)` (L171~L188)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn metadata(&self) -> Result<Metadata, Error> {
        use self::DirEntryInner::*;
        match *self {
            Stdin => {
                let err = Error::Io(io::Error::new(
                    io::ErrorKind::Other,
                    "<stdin> has no metadata",
                ));
                Err(err.with_path("<stdin>"))
            }
            Walkdir(ref x) => x.metadata().map_err(|err| {
                Error::Io(io::Error::from(err)).with_path(x.path())
            }),
            Raw(ref x) => x.metadata(),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn metadata(&self) -> Result<Metadata, Error> {
        use self::DirEntryInner::*;
        match *self {
            Stdin => {
                let err = Error::Io(io::Error::new(
                    io::ErrorKind::Other,
                    "<stdin> has no metadata",
                ));
                Err(err.with_path("<stdin>"))
            }
            Walkdir(ref x) => x.metadata().map_err(|err| {
                Error::Io(io::Error::from(err))
                    .with_depth(x.depth())
                    .with_path(x.path())
            }),
            Raw(ref x) => x.metadata(),
        }
    }
```

### 🔹 函式: `DirEntryRaw::from_entry()`
- **變更前簽章 (Before)**: `fn DirEntryRaw::from_entry(
        depth: usize,
        ent: &fs::DirEntry,
    )` (L322~L331)
- **變更後簽章 (After)**: `fn DirEntryRaw::from_entry(
        depth: usize,
        ent: &fs::DirEntry,
    )` (L326~L335)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn from_entry(
        depth: usize,
        ent: &fs::DirEntry,
    ) -> Result<DirEntryRaw, Error> {
        let ty = ent.file_type().map_err(|err| {
            let err = Error::Io(io::Error::from(err)).with_path(ent.path());
            Error::WithDepth { depth, err: Box::new(err) }
        })?;
        DirEntryRaw::from_entry_os(depth, ent, ty)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn from_entry(
        depth: usize,
        ent: &fs::DirEntry,
    ) -> Result<DirEntryRaw, Error> {
        let ty = ent.file_type().map_err(|err| {
            let err = Error::Io(err).with_depth(depth).with_path(ent.path());
            Error::WithDepth { depth, err: Box::new(err) }
        })?;
        DirEntryRaw::from_entry_os(depth, ent, ty)
    }
```

### 🔹 函式: `DirEntryRaw::metadata_internal()`
- **變更前簽章 (Before)**: `fn DirEntryRaw::metadata_internal(&self)` (L296~L303)
- **變更後簽章 (After)**: `fn DirEntryRaw::metadata_internal(&self)` (L298~L307)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn metadata_internal(&self) -> Result<fs::Metadata, Error> {
        if self.follow_link {
            fs::metadata(&self.path)
        } else {
            fs::symlink_metadata(&self.path)
        }
        .map_err(|err| Error::Io(io::Error::from(err)).with_path(&self.path))
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn metadata_internal(&self) -> Result<fs::Metadata, Error> {
        if self.follow_link {
            fs::metadata(&self.path)
        } else {
            fs::symlink_metadata(&self.path)
        }
        .map_err(|err| {
            Error::Io(err).with_depth(self.depth).with_path(&self.path)
        })
    }
```

### 🔹 函式: `DirEntryRaw::from_entry_os()`
- **變更前簽章 (Before)**: `fn DirEntryRaw::from_entry_os(
        depth: usize,
        ent: &fs::DirEntry,
        ty: fs::FileType,
    )` (L334~L350)
- **變更後簽章 (After)**: `fn DirEntryRaw::from_entry_os(
        depth: usize,
        ent: &fs::DirEntry,
        ty: fs::FileType,
    )` (L338~L354)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn from_entry_os(
        depth: usize,
        ent: &fs::DirEntry,
        ty: fs::FileType,
    ) -> Result<DirEntryRaw, Error> {
        let md = ent.metadata().map_err(|err| {
            let err = Error::Io(io::Error::from(err)).with_path(ent.path());
            Error::WithDepth { depth, err: Box::new(err) }
        })?;
        Ok(DirEntryRaw {
            path: ent.path(),
            ty,
            follow_link: false,
            depth,
            metadata: md,
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn from_entry_os(
        depth: usize,
        ent: &fs::DirEntry,
        ty: fs::FileType,
    ) -> Result<DirEntryRaw, Error> {
        let md = ent.metadata().map_err(|err| {
            let err = Error::Io(err).with_depth(depth).with_path(ent.path());
            Error::WithDepth { depth, err: Box::new(err) }
        })?;
        Ok(DirEntryRaw {
            path: ent.path(),
            ty,
            follow_link: false,
            depth,
            metadata: md,
        })
    }
```

### 🔹 函式: `path_equals()`
- **變更前簽章 (Before)**: `fn path_equals(dent: &DirEntry, handle: &Handle)` (L1977~L1996)
- **變更後簽章 (After)**: `fn path_equals(dent: &DirEntry, handle: &Handle)` (L1981~L2000)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn path_equals(dent: &DirEntry, handle: &Handle) -> Result<bool, Error> {
    #[cfg(unix)]
    fn never_equal(dent: &DirEntry, handle: &Handle) -> bool {
        dent.ino() != Some(handle.ino())
    }

    #[cfg(not(unix))]
    fn never_equal(_: &DirEntry, _: &Handle) -> bool {
        false
    }

    // If we know for sure that these two things aren't equal, then avoid
    // the costly extra stat call to determine equality.
    if dent.is_stdin() || never_equal(dent, handle) {
        return Ok(false);
    }
    Handle::from_path(dent.path())
        .map(|h| &h == handle)
        .map_err(|err| Error::Io(err).with_path(dent.path()))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn path_equals(dent: &DirEntry, handle: &Handle) -> Result<bool, Error> {
    #[cfg(unix)]
    fn never_equal(dent: &DirEntry, handle: &Handle) -> bool {
        dent.ino() != Some(handle.ino())
    }

    #[cfg(not(unix))]
    fn never_equal(_: &DirEntry, _: &Handle) -> bool {
        false
    }

    // If we know for sure that these two things aren't equal, then avoid
    // the costly extra stat call to determine equality.
    if dent.is_stdin() || never_equal(dent, handle) {
        return Ok(false);
    }
    Handle::from_path(dent.path()).map(|h| &h == handle).map_err(|err| {
        Error::Io(err).with_depth(dent.depth()).with_path(dent.path())
    })
}
```

### 🔹 函式: `DirEntryRaw::from_path()`
- **變更前簽章 (Before)**: `fn DirEntryRaw::from_path(
        depth: usize,
        pb: PathBuf,
        link: bool,
    )` (L384~L398)
- **變更後簽章 (After)**: `fn DirEntryRaw::from_path(
        depth: usize,
        pb: PathBuf,
        link: bool,
    )` (L388~L402)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn from_path(
        depth: usize,
        pb: PathBuf,
        link: bool,
    ) -> Result<DirEntryRaw, Error> {
        let md =
            fs::metadata(&pb).map_err(|err| Error::Io(err).with_path(&pb))?;
        Ok(DirEntryRaw {
            path: pb,
            ty: md.file_type(),
            follow_link: link,
            depth,
            metadata: md,
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn from_path(
        depth: usize,
        pb: PathBuf,
        link: bool,
    ) -> Result<DirEntryRaw, Error> {
        let md = fs::metadata(&pb)
            .map_err(|err| Error::Io(err).with_depth(depth).with_path(&pb))?;
        Ok(DirEntryRaw {
            path: pb,
            ty: md.file_type(),
            follow_link: link,
            depth,
            metadata: md,
        })
    }
```

### 🔹 函式: `DirEntryRaw::from_path()`
- **變更前簽章 (Before)**: `fn DirEntryRaw::from_path(
        depth: usize,
        pb: PathBuf,
        link: bool,
    )` (L401~L417)
- **變更後簽章 (After)**: `fn DirEntryRaw::from_path(
        depth: usize,
        pb: PathBuf,
        link: bool,
    )` (L405~L421)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn from_path(
        depth: usize,
        pb: PathBuf,
        link: bool,
    ) -> Result<DirEntryRaw, Error> {
        use std::os::unix::fs::MetadataExt;

        let md =
            fs::metadata(&pb).map_err(|err| Error::Io(err).with_path(&pb))?;
        Ok(DirEntryRaw {
            path: pb,
            ty: md.file_type(),
            follow_link: link,
            depth,
            ino: md.ino(),
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn from_path(
        depth: usize,
        pb: PathBuf,
        link: bool,
    ) -> Result<DirEntryRaw, Error> {
        use std::os::unix::fs::MetadataExt;

        let md = fs::metadata(&pb)
            .map_err(|err| Error::Io(err).with_depth(depth).with_path(&pb))?;
        Ok(DirEntryRaw {
            path: pb,
            ty: md.file_type(),
            follow_link: link,
            depth,
            ino: md.ino(),
        })
    }
```


---

### 🔹 Commit #18: `c10f151e`
- **完整 Hash**: `c10f151e4436da7c37d34359cdfe10d6f5aa0bb4`
- **說明 (Ground Truth)**: ignore: always include depth in errors
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/lib.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:72, E:81, A:0) ➔ After(N:72, E:81, A:0)
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

### 🔹 函式: `Error::from_walkdir()`
- **變更前簽章 (Before)**: `fn Error::from_walkdir(err: walkdir::Error)` (L285~L302)
- **變更後簽章 (After)**: `fn Error::from_walkdir(err: walkdir::Error)` (L285~L305)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn from_walkdir(err: walkdir::Error) -> Error {
        let depth = err.depth();
        if let (Some(anc), Some(child)) = (err.loop_ancestor(), err.path()) {
            return Error::WithDepth {
                depth,
                err: Box::new(Error::Loop {
                    ancestor: anc.to_path_buf(),
                    child: child.to_path_buf(),
                }),
            };
        }
        let path = err.path().map(|p| p.to_path_buf());
        let mut ig_err = Error::Io(std::io::Error::from(err));
        if let Some(path) = path {
            ig_err = Error::WithPath { path, err: Box::new(ig_err) };
        }
        ig_err
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn from_walkdir(err: walkdir::Error) -> Error {
        let depth = err.depth();
        if let (Some(anc), Some(child)) = (err.loop_ancestor(), err.path()) {
            return Error::WithDepth {
                depth,
                err: Box::new(Error::Loop {
                    ancestor: anc.to_path_buf(),
                    child: child.to_path_buf(),
                }),
            };
        }
        let path = err.path().map(|p| p.to_path_buf());
        let mut ig_err = Error::WithDepth {
            depth,
            err: Box::new(Error::Io(std::io::Error::from(err))),
        };
        if let Some(path) = path {
            ig_err = Error::WithPath { path, err: Box::new(ig_err) };
        }
        ig_err
    }
```


---

### 🔹 Commit #19: `dfe4a81d`
- **完整 Hash**: `dfe4a81d2591daca76d25ae4e052c34b26578155`
- **說明 (Ground Truth)**: ignore/types: add Hurl
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/default_types.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:6, E:4, A:0) ➔ After(N:6, E:4, A:0)
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

### 🔹 函式: `DEFAULT_TYPES()`
- **變更前簽章 (Before)**: `[Module State] DEFAULT_TYPES` (L12~L342)
- **變更後簽章 (After)**: `[Module State] DEFAULT_TYPES` (L12~L343)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) const DEFAULT_TYPES: &[(&[&str], &[&str])] = &[
    (&["ada"], &["*.adb", "*.ads"]),
    (&["agda"], &["*.agda", "*.lagda"]),
    (&["aidl"], &["*.aidl"]),
    (&["alire"], &["alire.toml"]),
    (&["amake"], &["*.mk", "*.bp"]),
    (&["asciidoc"], &["*.adoc", "*.asc", "*.asciidoc"]),
    (&["asm"], &["*.asm", "*.s", "*.S"]),
    (&["asp"], &[
        "*.aspx", "*.aspx.cs", "*.aspx.vb", "*.ascx", "*.ascx.cs",
        "*.ascx.vb", "*.asp"
    ]),
    (&["ats"], &["*.ats", "*.dats", "*.sats", "*.hats"]),
    (&["avro"], &["*.avdl", "*.avpr", "*.avsc"]),
    (&["awk"], &["*.awk"]),
    (&["bat", "batch"], &["*.bat"]),
    (&["bazel"], &[
        "*.bazel", "*.bzl", "*.BUILD", "*.bazelrc", "BUILD", "MODULE.bazel",
        "WORKSPACE", "WORKSPACE.bazel", "WORKSPACE.bzlmod",
    ]),
    (&["bitbake"], &["*.bb", "*.bbappend", "*.bbclass", "*.conf", "*.inc"]),
    (&["boxlang"], &["*.bx", "*.bxm", "*.bxs"]),
    (&["brotli"], &["*.br"]),
    (&["buildstream"], &["*.bst"]),
    (&["bzip2"], &["*.bz2", "*.tbz2"]),
    (&["c"], &["*.[chH]", "*.[chH].in", "*.cats"]),
    (&["cabal"], &["*.cabal"]),
    (&["candid"], &["*.did"]),
    (&["carp"], &["*.carp"]),
    (&["cbor"], &["*.cbor"]),
    (&["ceylon"], &["*.ceylon"]),
    (&["cfml"], &["*.cfc", "*.cfm"]),
    (&["clojure"], &["*.clj", "*.cljc", "*.cljs", "*.cljx"]),
    (&["cmake"], &["*.cmake", "CMakeLists.txt"]),
    (&["cmd"], &["*.bat", "*.cmd"]),
    (&["cml"], &["*.cml"]),
    (&["coffeescript"], &["*.coffee"]),
    (&["config"], &["*.cfg", "*.conf", "*.config", "*.ini"]),
    (&["container"], &["*Containerfile*", "*Dockerfile*"]),
    (&["coq"], &["*.v"]),
    (&["cpp"], &[
        "*.[ChH]", "*.cc", "*.[ch]pp", "*.[ch]xx", "*.hh",  "*.inl",
        "*.[ChH].in", "*.cc.in", "*.[ch]pp.in", "*.[ch]xx.in", "*.hh.in",
    ]),
    (&["creole"], &["*.creole"]),
    (&["crystal"], &["Projectfile", "*.cr", "*.ecr", "shard.yml"]),
    (&["cs"], &["*.cs"]),
    (&["csharp"], &["*.cs"]),
    (&["cshtml"], &["*.cshtml"]),
    (&["csproj"], &["*.csproj"]),
    (&["css"], &["*.css", "*.scss"]),
    (&["csv"], &["*.csv"]),
    (&["cuda"], &["*.cu", "*.cuh"]),
    (&["cython"], &["*.pyx", "*.pxi", "*.pxd"]),
    (&["d"], &["*.d"]),
    (&["dart"], &["*.dart"]),
    (&["devicetree"], &["*.dts", "*.dtsi", "*.dtso"]),
    (&["dhall"], &["*.dhall"]),
    (&["diff"], &["*.patch", "*.diff"]),
    (&["dita"], &["*.dita", "*.ditamap", "*.ditaval"]),
    (&["docker"], &["*Dockerfile*"]),
    (&["dockercompose"], &["docker-compose.yml", "docker-compose.*.yml"]),
    (&["dts"], &["*.dts", "*.dtsi"]),
    (&["dvc"], &["Dvcfile", "*.dvc"]),
    (&["ebuild"], &["*.ebuild", "*.eclass"]),
    (&["edn"], &["*.edn"]),
    (&["elisp"], &["*.el"]),
    (&["elixir"], &["*.ex", "*.eex", "*.exs", "*.heex", "*.leex", "*.livemd"]),
    (&["elm"], &["*.elm"]),
    (&["erb"], &["*.erb"]),
    (&["erlang"], &["*.erl", "*.hrl"]),
    (&["fennel"], &["*.fnl"]),
    (&["fidl"], &["*.fidl"]),
    (&["fish"], &["*.fish"]),
    (&["flatbuffers"], &["*.fbs"]),
    (&["fortran"], &[
        "*.f", "*.F", "*.f77", "*.F77", "*.pfo",
        "*.f90", "*.F90", "*.f95", "*.F95",
    ]),
    (&["fsharp"], &["*.fs", "*.fsx", "*.fsi"]),
    (&["fut"], &["*.fut"]),
    (&["gap"], &["*.g", "*.gap", "*.gi", "*.gd", "*.tst"]),
    (&["gdscript"], &["*.gd"]),
    (&["gleam"], &["*.gleam"]),
    (&["gn"], &["*.gn", "*.gni"]),
    (&["go"], &["*.go"]),
    (&["gprbuild"], &["*.gpr"]),
    (&["gradle"], &[
        "*.gradle", "*.gradle.kts", "gradle.properties", "gradle-wrapper.*",
        "gradlew", "gradlew.bat",
    ]),
    (&["graphql"], &["*.graphql", "*.graphqls"]),
    (&["groovy"], &["*.groovy", "*.gradle"]),
    (&["gzip"], &["*.gz", "*.tgz"]),
    (&["h"], &["*.h", "*.hh", "*.hpp"]),
    (&["haml"], &["*.haml"]),
    (&["hare"], &["*.ha"]),
    (&["haskell"], &["*.hs", "*.lhs", "*.cpphs", "*.c2hs", "*.hsc"]),
    (&["hbs"], &["*.hbs"]),
    (&["hs"], &["*.hs", "*.lhs"]),
    (&["html"], &["*.htm", "*.html", "*.ejs"]),
    (&["hy"], &["*.hy"]),
    (&["idris"], &["*.idr", "*.lidr"]),
    (&["janet"], &["*.janet"]),
    (&["java"], &["*.java", "*.jsp", "*.jspx", "*.properties"]),
    (&["jinja"], &["*.j2", "*.jinja", "*.jinja2"]),
    (&["jl"], &["*.jl"]),
    (&["js"], &["*.js", "*.jsx", "*.vue", "*.cjs", "*.mjs"]),
    (&["json"], &["*.json", "composer.lock", "*.sarif"]),
    (&["jsonl"], &["*.jsonl"]),
    (&["julia"], &["*.jl"]),
    (&["jupyter"], &["*.ipynb", "*.jpynb"]),
    (&["k"], &["*.k"]),
    (&["kconfig"], &["Kconfig", "Kconfig.*"]),
    (&["kotlin"], &["*.kt", "*.kts"]),
    (&["lean"], &["*.lean"]),
    (&["less"], &["*.less"]),
    (&["license"], &[
        // General
        "COPYING", "COPYING[.-]*",
        "COPYRIGHT", "COPYRIGHT[.-]*",
        "EULA", "EULA[.-]*",
        "licen[cs]e", "licen[cs]e.*",
        "LICEN[CS]E", "LICEN[CS]E[.-]*", "*[.-]LICEN[CS]E*",
        "NOTICE", "NOTICE[.-]*",
        "PATENTS", "PATENTS[.-]*",
        "UNLICEN[CS]E", "UNLICEN[CS]E[.-]*",
        // GPL (gpl.txt, etc.)
        "agpl[.-]*",
        "gpl[.-]*",
        "lgpl[.-]*",
        // Other license-specific (APACHE-2.0.txt, etc.)
        "AGPL-*[0-9]*",
        "APACHE-*[0-9]*",
        "BSD-*[0-9]*",
        "CC-BY-*",
        "GFDL-*[0-9]*",
        "GNU-*[0-9]*",
        "GPL-*[0-9]*",
        "LGPL-*[0-9]*",
        "MIT-*[0-9]*",
        "MPL-*[0-9]*",
        "OFL-*[0-9]*",
    ]),
    (&["lilypond"], &["*.ly", "*.ily"]),
    (&["lisp"], &["*.el", "*.jl", "*.lisp", "*.lsp", "*.sc", "*.scm"]),
    (&["llvm"], &["*.ll"]),
    (&["lock"], &["*.lock", "package-lock.json"]),
    (&["log"], &["*.log"]),
    (&["lua"], &["*.lua"]),
    (&["lz4"], &["*.lz4"]),
    (&["lzma"], &["*.lzma"]),
    (&["m4"], &["*.ac", "*.m4"]),
    (&["make"], &[
        "[Gg][Nn][Uu]makefile", "[Mm]akefile",
        "[Gg][Nn][Uu]makefile.am", "[Mm]akefile.am",
        "[Gg][Nn][Uu]makefile.in", "[Mm]akefile.in",
        "Makefile.*",
        "*.mk", "*.mak"
    ]),
    (&["mako"], &["*.mako", "*.mao"]),
    (&["man"], &["*.[0-9lnpx]", "*.[0-9][cEFMmpSx]"]),
    (&["markdown", "md"], &[
        "*.markdown",
        "*.md",
        "*.mdown",
        "*.mdwn",
        "*.mkd",
        "*.mkdn",
        "*.mdx",
    ]),
    (&["matlab"], &["*.m"]),
    (&["meson"], &["meson.build", "meson_options.txt", "meson.options"]),
    (&["minified"], &["*.min.html", "*.min.css", "*.min.js"]),
    (&["mint"], &["*.mint"]),
    (&["mk"], &["mkfile"]),
    (&["ml"], &["*.ml"]),
    (&["motoko"], &["*.mo"]),
    (&["msbuild"], &[
        "*.csproj", "*.fsproj", "*.vcxproj", "*.proj", "*.props", "*.targets",
        "*.sln", "*.slnf"
    ]),
    (&["nim"], &["*.nim", "*.nimf", "*.nimble", "*.nims"]),
    (&["nix"], &["*.nix"]),
    (&["objc"], &["*.h", "*.m"]),
    (&["objcpp"], &["*.h", "*.mm"]),
    (&["ocaml"], &["*.ml", "*.mli", "*.mll", "*.mly"]),
    (&["org"], &["*.org", "*.org_archive"]),
    (&["pants"], &["BUILD"]),
    (&["pascal"], &["*.pas", "*.dpr", "*.lpr", "*.pp", "*.inc"]),
    (&["pdf"], &["*.pdf"]),
    (&["perl"], &["*.perl", "*.pl", "*.PL", "*.plh", "*.plx", "*.pm", "*.t"]),
    (&["php"], &[
        // note that PHP 6 doesn't exist
        // See: https://wiki.php.net/rfc/php6
        "*.php", "*.php3", "*.php4", "*.php5", "*.php7", "*.php8",
        "*.pht", "*.phtml"
    ]),
    (&["po"], &["*.po"]),
    (&["pod"], &["*.pod"]),
    (&["postscript"], &["*.eps", "*.ps"]),
    (&["prolog"], &["*.pl", "*.pro", "*.prolog", "*.P"]),
    (&["protobuf"], &["*.proto"]),
    (&["ps"], &["*.cdxml", "*.ps1", "*.ps1xml", "*.psd1", "*.psm1"]),
    (&["puppet"], &["*.epp", "*.erb", "*.pp", "*.rb"]),
    (&["purs"], &["*.purs"]),
    (&["py", "python"], &["*.py", "*.pyi"]),
    (&["qmake"], &["*.pro", "*.pri", "*.prf"]),
    (&["qml"], &["*.qml"]),
    (&["qrc"], &["*.qrc"]),
    (&["qui"], &["*.ui"]),
    (&["r"], &["*.R", "*.r", "*.Rmd", "*.rmd", "*.Rnw", "*.rnw"]),
    (&["racket"], &["*.rkt"]),
    (&["raku"], &[
        "*.raku", "*.rakumod", "*.rakudoc", "*.rakutest",
        "*.p6", "*.pl6", "*.pm6"
    ]),
    (&["rdoc"], &["*.rdoc"]),
    (&["readme"], &["README*", "*README"]),
    (&["reasonml"], &["*.re", "*.rei"]),
    (&["red"], &["*.r", "*.red", "*.reds"]),
    (&["rescript"], &["*.res", "*.resi"]),
    (&["robot"], &["*.robot"]),
    (&["rst"], &["*.rst"]),
    (&["ruby"], &[
        // Idiomatic files
        "config.ru", "Gemfile", ".irbrc", "Rakefile",
        // Extensions
        "*.gemspec", "*.rb", "*.rbw", "*.rake"
    ]),
    (&["rust"], &["*.rs"]),
    (&["sass"], &["*.sass", "*.scss"]),
    (&["scala"], &["*.scala", "*.sbt"]),
    (&["scdoc"], &["*.scd", "*.scdoc"]),
    (&["seed7"], &["*.sd7", "*.s7i"]),
    (&["sh"], &[
        // Portable/misc. init files
        ".env", ".login", ".logout", ".profile", "profile",
        // bash-specific init files
        ".bash_login", "bash_login",
        ".bash_logout", "bash_logout",
        ".bash_profile", "bash_profile",
        ".bashrc", "bashrc", "*.bashrc",
        // csh-specific init files
        ".cshrc", "*.cshrc",
        // ksh-specific init files
        ".kshrc", "*.kshrc",
        // tcsh-specific init files
        ".tcshrc",
        // zsh-specific init files
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        // Extensions
        "*.bash", "*.csh", "*.env", "*.ksh", "*.sh", "*.tcsh", "*.zsh",
    ]),
    (&["slim"], &["*.skim", "*.slim", "*.slime"]),
    (&["smarty"], &["*.tpl"]),
    (&["sml"], &["*.sml", "*.sig"]),
    (&["solidity"], &["*.sol"]),
    (&["soy"], &["*.soy"]),
    (&["spark"], &["*.spark"]),
    (&["spec"], &["*.spec"]),
    (&["sql"], &["*.sql", "*.psql"]),
    (&["ssa"], &["*.ssa"]),
    (&["stylus"], &["*.styl"]),
    (&["sv"], &["*.v", "*.vg", "*.sv", "*.svh", "*.h"]),
    (&["svelte"], &["*.svelte", "*.svelte.ts"]),
    (&["svg"], &["*.svg"]),
    (&["swift"], &["*.swift"]),
    (&["swig"], &["*.def", "*.i"]),
    (&["systemd"], &[
        "*.automount", "*.conf", "*.device", "*.link", "*.mount", "*.path",
        "*.scope", "*.service", "*.slice", "*.socket", "*.swap", "*.target",
        "*.timer",
    ]),
    (&["taskpaper"], &["*.taskpaper"]),
    (&["tcl"], &["*.tcl"]),
    (&["tex"], &["*.tex", "*.ltx", "*.cls", "*.sty", "*.bib", "*.dtx", "*.ins"]),
    (&["texinfo"], &["*.texi"]),
    (&["textile"], &["*.textile"]),
    (&["tf"], &[
        "*.tf", "*.tf.json", "*.tfvars", "*.tfvars.json",
        "*.terraformrc", "terraform.rc", "*.tfrc", "*.terraform.lock.hcl",
    ]),
    (&["thrift"], &["*.thrift"]),
    (&["toml"], &["*.toml", "Cargo.lock"]),
    (&["ts", "typescript"], &["*.ts", "*.tsx", "*.cts", "*.mts"]),
    (&["twig"], &["*.twig"]),
    (&["txt"], &["*.txt"]),
    (&["typoscript"], &["*.typoscript", "*.ts"]),
    (&["typst"], &["*.typ"]),
    (&["usd"], &["*.usd", "*.usda", "*.usdc"]),
    (&["v"], &["*.v", "*.vsh"]),
    (&["vala"], &["*.vala"]),
    (&["vb"], &["*.vb"]),
    (&["vcl"], &["*.vcl"]),
    (&["verilog"], &["*.v", "*.vh", "*.sv", "*.svh"]),
    (&["vhdl"], &["*.vhd", "*.vhdl"]),
    (&["vim"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vimscript"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vue"], &["*.vue"]),
    (&["webidl"], &["*.idl", "*.webidl", "*.widl"]),
    (&["wgsl"], &["*.wgsl"]),
    (&["wiki"], &["*.mediawiki", "*.wiki"]),
    (&["xml"], &[
        "*.xml", "*.xml.dist", "*.dtd", "*.xsl", "*.xslt", "*.xsd", "*.xjb",
        "*.rng", "*.sch", "*.xhtml",
    ]),
    (&["xz"], &["*.xz", "*.txz"]),
    (&["yacc"], &["*.y"]),
    (&["yaml"], &["*.yaml", "*.yml"]),
    (&["yang"], &["*.yang"]),
    (&["z"], &["*.Z"]),
    (&["zig"], &["*.zig"]),
    (&["zsh"], &[
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        "*.zsh",
    ]),
    (&["zstd"], &["*.zst", "*.zstd"]),
];
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) const DEFAULT_TYPES: &[(&[&str], &[&str])] = &[
    (&["ada"], &["*.adb", "*.ads"]),
    (&["agda"], &["*.agda", "*.lagda"]),
    (&["aidl"], &["*.aidl"]),
    (&["alire"], &["alire.toml"]),
    (&["amake"], &["*.mk", "*.bp"]),
    (&["asciidoc"], &["*.adoc", "*.asc", "*.asciidoc"]),
    (&["asm"], &["*.asm", "*.s", "*.S"]),
    (&["asp"], &[
        "*.aspx", "*.aspx.cs", "*.aspx.vb", "*.ascx", "*.ascx.cs",
        "*.ascx.vb", "*.asp"
    ]),
    (&["ats"], &["*.ats", "*.dats", "*.sats", "*.hats"]),
    (&["avro"], &["*.avdl", "*.avpr", "*.avsc"]),
    (&["awk"], &["*.awk"]),
    (&["bat", "batch"], &["*.bat"]),
    (&["bazel"], &[
        "*.bazel", "*.bzl", "*.BUILD", "*.bazelrc", "BUILD", "MODULE.bazel",
        "WORKSPACE", "WORKSPACE.bazel", "WORKSPACE.bzlmod",
    ]),
    (&["bitbake"], &["*.bb", "*.bbappend", "*.bbclass", "*.conf", "*.inc"]),
    (&["boxlang"], &["*.bx", "*.bxm", "*.bxs"]),
    (&["brotli"], &["*.br"]),
    (&["buildstream"], &["*.bst"]),
    (&["bzip2"], &["*.bz2", "*.tbz2"]),
    (&["c"], &["*.[chH]", "*.[chH].in", "*.cats"]),
    (&["cabal"], &["*.cabal"]),
    (&["candid"], &["*.did"]),
    (&["carp"], &["*.carp"]),
    (&["cbor"], &["*.cbor"]),
    (&["ceylon"], &["*.ceylon"]),
    (&["cfml"], &["*.cfc", "*.cfm"]),
    (&["clojure"], &["*.clj", "*.cljc", "*.cljs", "*.cljx"]),
    (&["cmake"], &["*.cmake", "CMakeLists.txt"]),
    (&["cmd"], &["*.bat", "*.cmd"]),
    (&["cml"], &["*.cml"]),
    (&["coffeescript"], &["*.coffee"]),
    (&["config"], &["*.cfg", "*.conf", "*.config", "*.ini"]),
    (&["container"], &["*Containerfile*", "*Dockerfile*"]),
    (&["coq"], &["*.v"]),
    (&["cpp"], &[
        "*.[ChH]", "*.cc", "*.[ch]pp", "*.[ch]xx", "*.hh",  "*.inl",
        "*.[ChH].in", "*.cc.in", "*.[ch]pp.in", "*.[ch]xx.in", "*.hh.in",
    ]),
    (&["creole"], &["*.creole"]),
    (&["crystal"], &["Projectfile", "*.cr", "*.ecr", "shard.yml"]),
    (&["cs"], &["*.cs"]),
    (&["csharp"], &["*.cs"]),
    (&["cshtml"], &["*.cshtml"]),
    (&["csproj"], &["*.csproj"]),
    (&["css"], &["*.css", "*.scss"]),
    (&["csv"], &["*.csv"]),
    (&["cuda"], &["*.cu", "*.cuh"]),
    (&["cython"], &["*.pyx", "*.pxi", "*.pxd"]),
    (&["d"], &["*.d"]),
    (&["dart"], &["*.dart"]),
    (&["devicetree"], &["*.dts", "*.dtsi", "*.dtso"]),
    (&["dhall"], &["*.dhall"]),
    (&["diff"], &["*.patch", "*.diff"]),
    (&["dita"], &["*.dita", "*.ditamap", "*.ditaval"]),
    (&["docker"], &["*Dockerfile*"]),
    (&["dockercompose"], &["docker-compose.yml", "docker-compose.*.yml"]),
    (&["dts"], &["*.dts", "*.dtsi"]),
    (&["dvc"], &["Dvcfile", "*.dvc"]),
    (&["ebuild"], &["*.ebuild", "*.eclass"]),
    (&["edn"], &["*.edn"]),
    (&["elisp"], &["*.el"]),
    (&["elixir"], &["*.ex", "*.eex", "*.exs", "*.heex", "*.leex", "*.livemd"]),
    (&["elm"], &["*.elm"]),
    (&["erb"], &["*.erb"]),
    (&["erlang"], &["*.erl", "*.hrl"]),
    (&["fennel"], &["*.fnl"]),
    (&["fidl"], &["*.fidl"]),
    (&["fish"], &["*.fish"]),
    (&["flatbuffers"], &["*.fbs"]),
    (&["fortran"], &[
        "*.f", "*.F", "*.f77", "*.F77", "*.pfo",
        "*.f90", "*.F90", "*.f95", "*.F95",
    ]),
    (&["fsharp"], &["*.fs", "*.fsx", "*.fsi"]),
    (&["fut"], &["*.fut"]),
    (&["gap"], &["*.g", "*.gap", "*.gi", "*.gd", "*.tst"]),
    (&["gdscript"], &["*.gd"]),
    (&["gleam"], &["*.gleam"]),
    (&["gn"], &["*.gn", "*.gni"]),
    (&["go"], &["*.go"]),
    (&["gprbuild"], &["*.gpr"]),
    (&["gradle"], &[
        "*.gradle", "*.gradle.kts", "gradle.properties", "gradle-wrapper.*",
        "gradlew", "gradlew.bat",
    ]),
    (&["graphql"], &["*.graphql", "*.graphqls"]),
    (&["groovy"], &["*.groovy", "*.gradle"]),
    (&["gzip"], &["*.gz", "*.tgz"]),
    (&["h"], &["*.h", "*.hh", "*.hpp"]),
    (&["haml"], &["*.haml"]),
    (&["hare"], &["*.ha"]),
    (&["haskell"], &["*.hs", "*.lhs", "*.cpphs", "*.c2hs", "*.hsc"]),
    (&["hbs"], &["*.hbs"]),
    (&["hs"], &["*.hs", "*.lhs"]),
    (&["html"], &["*.htm", "*.html", "*.ejs"]),
    (&["hurl"], &["*.hurl"]),
    (&["hy"], &["*.hy"]),
    (&["idris"], &["*.idr", "*.lidr"]),
    (&["janet"], &["*.janet"]),
    (&["java"], &["*.java", "*.jsp", "*.jspx", "*.properties"]),
    (&["jinja"], &["*.j2", "*.jinja", "*.jinja2"]),
    (&["jl"], &["*.jl"]),
    (&["js"], &["*.js", "*.jsx", "*.vue", "*.cjs", "*.mjs"]),
    (&["json"], &["*.json", "composer.lock", "*.sarif"]),
    (&["jsonl"], &["*.jsonl"]),
    (&["julia"], &["*.jl"]),
    (&["jupyter"], &["*.ipynb", "*.jpynb"]),
    (&["k"], &["*.k"]),
    (&["kconfig"], &["Kconfig", "Kconfig.*"]),
    (&["kotlin"], &["*.kt", "*.kts"]),
    (&["lean"], &["*.lean"]),
    (&["less"], &["*.less"]),
    (&["license"], &[
        // General
        "COPYING", "COPYING[.-]*",
        "COPYRIGHT", "COPYRIGHT[.-]*",
        "EULA", "EULA[.-]*",
        "licen[cs]e", "licen[cs]e.*",
        "LICEN[CS]E", "LICEN[CS]E[.-]*", "*[.-]LICEN[CS]E*",
        "NOTICE", "NOTICE[.-]*",
        "PATENTS", "PATENTS[.-]*",
        "UNLICEN[CS]E", "UNLICEN[CS]E[.-]*",
        // GPL (gpl.txt, etc.)
        "agpl[.-]*",
        "gpl[.-]*",
        "lgpl[.-]*",
        // Other license-specific (APACHE-2.0.txt, etc.)
        "AGPL-*[0-9]*",
        "APACHE-*[0-9]*",
        "BSD-*[0-9]*",
        "CC-BY-*",
        "GFDL-*[0-9]*",
        "GNU-*[0-9]*",
        "GPL-*[0-9]*",
        "LGPL-*[0-9]*",
        "MIT-*[0-9]*",
        "MPL-*[0-9]*",
        "OFL-*[0-9]*",
    ]),
    (&["lilypond"], &["*.ly", "*.ily"]),
    (&["lisp"], &["*.el", "*.jl", "*.lisp", "*.lsp", "*.sc", "*.scm"]),
    (&["llvm"], &["*.ll"]),
    (&["lock"], &["*.lock", "package-lock.json"]),
    (&["log"], &["*.log"]),
    (&["lua"], &["*.lua"]),
    (&["lz4"], &["*.lz4"]),
    (&["lzma"], &["*.lzma"]),
    (&["m4"], &["*.ac", "*.m4"]),
    (&["make"], &[
        "[Gg][Nn][Uu]makefile", "[Mm]akefile",
        "[Gg][Nn][Uu]makefile.am", "[Mm]akefile.am",
        "[Gg][Nn][Uu]makefile.in", "[Mm]akefile.in",
        "Makefile.*",
        "*.mk", "*.mak"
    ]),
    (&["mako"], &["*.mako", "*.mao"]),
    (&["man"], &["*.[0-9lnpx]", "*.[0-9][cEFMmpSx]"]),
    (&["markdown", "md"], &[
        "*.markdown",
        "*.md",
        "*.mdown",
        "*.mdwn",
        "*.mkd",
        "*.mkdn",
        "*.mdx",
    ]),
    (&["matlab"], &["*.m"]),
    (&["meson"], &["meson.build", "meson_options.txt", "meson.options"]),
    (&["minified"], &["*.min.html", "*.min.css", "*.min.js"]),
    (&["mint"], &["*.mint"]),
    (&["mk"], &["mkfile"]),
    (&["ml"], &["*.ml"]),
    (&["motoko"], &["*.mo"]),
    (&["msbuild"], &[
        "*.csproj", "*.fsproj", "*.vcxproj", "*.proj", "*.props", "*.targets",
        "*.sln", "*.slnf"
    ]),
    (&["nim"], &["*.nim", "*.nimf", "*.nimble", "*.nims"]),
    (&["nix"], &["*.nix"]),
    (&["objc"], &["*.h", "*.m"]),
    (&["objcpp"], &["*.h", "*.mm"]),
    (&["ocaml"], &["*.ml", "*.mli", "*.mll", "*.mly"]),
    (&["org"], &["*.org", "*.org_archive"]),
    (&["pants"], &["BUILD"]),
    (&["pascal"], &["*.pas", "*.dpr", "*.lpr", "*.pp", "*.inc"]),
    (&["pdf"], &["*.pdf"]),
    (&["perl"], &["*.perl", "*.pl", "*.PL", "*.plh", "*.plx", "*.pm", "*.t"]),
    (&["php"], &[
        // note that PHP 6 doesn't exist
        // See: https://wiki.php.net/rfc/php6
        "*.php", "*.php3", "*.php4", "*.php5", "*.php7", "*.php8",
        "*.pht", "*.phtml"
    ]),
    (&["po"], &["*.po"]),
    (&["pod"], &["*.pod"]),
    (&["postscript"], &["*.eps", "*.ps"]),
    (&["prolog"], &["*.pl", "*.pro", "*.prolog", "*.P"]),
    (&["protobuf"], &["*.proto"]),
    (&["ps"], &["*.cdxml", "*.ps1", "*.ps1xml", "*.psd1", "*.psm1"]),
    (&["puppet"], &["*.epp", "*.erb", "*.pp", "*.rb"]),
    (&["purs"], &["*.purs"]),
    (&["py", "python"], &["*.py", "*.pyi"]),
    (&["qmake"], &["*.pro", "*.pri", "*.prf"]),
    (&["qml"], &["*.qml"]),
    (&["qrc"], &["*.qrc"]),
    (&["qui"], &["*.ui"]),
    (&["r"], &["*.R", "*.r", "*.Rmd", "*.rmd", "*.Rnw", "*.rnw"]),
    (&["racket"], &["*.rkt"]),
    (&["raku"], &[
        "*.raku", "*.rakumod", "*.rakudoc", "*.rakutest",
        "*.p6", "*.pl6", "*.pm6"
    ]),
    (&["rdoc"], &["*.rdoc"]),
    (&["readme"], &["README*", "*README"]),
    (&["reasonml"], &["*.re", "*.rei"]),
    (&["red"], &["*.r", "*.red", "*.reds"]),
    (&["rescript"], &["*.res", "*.resi"]),
    (&["robot"], &["*.robot"]),
    (&["rst"], &["*.rst"]),
    (&["ruby"], &[
        // Idiomatic files
        "config.ru", "Gemfile", ".irbrc", "Rakefile",
        // Extensions
        "*.gemspec", "*.rb", "*.rbw", "*.rake"
    ]),
    (&["rust"], &["*.rs"]),
    (&["sass"], &["*.sass", "*.scss"]),
    (&["scala"], &["*.scala", "*.sbt"]),
    (&["scdoc"], &["*.scd", "*.scdoc"]),
    (&["seed7"], &["*.sd7", "*.s7i"]),
    (&["sh"], &[
        // Portable/misc. init files
        ".env", ".login", ".logout", ".profile", "profile",
        // bash-specific init files
        ".bash_login", "bash_login",
        ".bash_logout", "bash_logout",
        ".bash_profile", "bash_profile",
        ".bashrc", "bashrc", "*.bashrc",
        // csh-specific init files
        ".cshrc", "*.cshrc",
        // ksh-specific init files
        ".kshrc", "*.kshrc",
        // tcsh-specific init files
        ".tcshrc",
        // zsh-specific init files
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        // Extensions
        "*.bash", "*.csh", "*.env", "*.ksh", "*.sh", "*.tcsh", "*.zsh",
    ]),
    (&["slim"], &["*.skim", "*.slim", "*.slime"]),
    (&["smarty"], &["*.tpl"]),
    (&["sml"], &["*.sml", "*.sig"]),
    (&["solidity"], &["*.sol"]),
    (&["soy"], &["*.soy"]),
    (&["spark"], &["*.spark"]),
    (&["spec"], &["*.spec"]),
    (&["sql"], &["*.sql", "*.psql"]),
    (&["ssa"], &["*.ssa"]),
    (&["stylus"], &["*.styl"]),
    (&["sv"], &["*.v", "*.vg", "*.sv", "*.svh", "*.h"]),
    (&["svelte"], &["*.svelte", "*.svelte.ts"]),
    (&["svg"], &["*.svg"]),
    (&["swift"], &["*.swift"]),
    (&["swig"], &["*.def", "*.i"]),
    (&["systemd"], &[
        "*.automount", "*.conf", "*.device", "*.link", "*.mount", "*.path",
        "*.scope", "*.service", "*.slice", "*.socket", "*.swap", "*.target",
        "*.timer",
    ]),
    (&["taskpaper"], &["*.taskpaper"]),
    (&["tcl"], &["*.tcl"]),
    (&["tex"], &["*.tex", "*.ltx", "*.cls", "*.sty", "*.bib", "*.dtx", "*.ins"]),
    (&["texinfo"], &["*.texi"]),
    (&["textile"], &["*.textile"]),
    (&["tf"], &[
        "*.tf", "*.tf.json", "*.tfvars", "*.tfvars.json",
        "*.terraformrc", "terraform.rc", "*.tfrc", "*.terraform.lock.hcl",
    ]),
    (&["thrift"], &["*.thrift"]),
    (&["toml"], &["*.toml", "Cargo.lock"]),
    (&["ts", "typescript"], &["*.ts", "*.tsx", "*.cts", "*.mts"]),
    (&["twig"], &["*.twig"]),
    (&["txt"], &["*.txt"]),
    (&["typoscript"], &["*.typoscript", "*.ts"]),
    (&["typst"], &["*.typ"]),
    (&["usd"], &["*.usd", "*.usda", "*.usdc"]),
    (&["v"], &["*.v", "*.vsh"]),
    (&["vala"], &["*.vala"]),
    (&["vb"], &["*.vb"]),
    (&["vcl"], &["*.vcl"]),
    (&["verilog"], &["*.v", "*.vh", "*.sv", "*.svh"]),
    (&["vhdl"], &["*.vhd", "*.vhdl"]),
    (&["vim"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vimscript"], &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    (&["vue"], &["*.vue"]),
    (&["webidl"], &["*.idl", "*.webidl", "*.widl"]),
    (&["wgsl"], &["*.wgsl"]),
    (&["wiki"], &["*.mediawiki", "*.wiki"]),
    (&["xml"], &[
        "*.xml", "*.xml.dist", "*.dtd", "*.xsl", "*.xslt", "*.xsd", "*.xjb",
        "*.rng", "*.sch", "*.xhtml",
    ]),
    (&["xz"], &["*.xz", "*.txz"]),
    (&["yacc"], &["*.y"]),
    (&["yaml"], &["*.yaml", "*.yml"]),
    (&["yang"], &["*.yang"]),
    (&["z"], &["*.Z"]),
    (&["zig"], &["*.zig"]),
    (&["zsh"], &[
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        "*.zsh",
    ]),
    (&["zstd"], &["*.zst", "*.zstd"]),
];
```


---

### 🔹 Commit #20: `43e2f08e`
- **完整 Hash**: `43e2f08edef8c00e5d7719212c3e6a869bca1151`
- **說明 (Ground Truth)**: ignore: fix parent gitignore matching across multiple roots
- **變更檔案數**: 1

#### 📄 檔案: `crates/ignore/src/dir.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:223, E:389, A:0) ➔ After(N:229, E:403, A:0)
- **差分統計**: +Nodes: 12, -Nodes: 6, +Edges: 41, -Edges: 27, ΔFuncs: 8, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `self.inner.parent.as_ref().map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.absolute_base.as_ref().map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.inner.parent.as_ref (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `IgnoreRef::path` (FUNCTION_DEF)
  • + [新增節點] `absolute_parent_matchers_are_cached_across_roots` (FUNCTION_DEF)
  • + [新增節點] `self.inner.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `ig
                    .inner
                    .parent
                    .as_deref()
                    .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `IgnoreRef::is_absolute_parent` (FUNCTION_DEF)
  • + [新增節點] `self.absolute_base.as_ref (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `ig
                    .inner
                    .parent
                    .as_deref (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.absolute_base.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `parent.clone (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `ig.inner.parent.as_ref (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `Ignore::is_absolute_parent` (FUNCTION_DEF)
  • - [移除節點] `self.inner.parent.clone (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 71 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Ignore::add_child_path()`
- **變更前簽章 (Before)**: `fn Ignore::add_child_path(&self, dir: &Path)` (L260~L356)
- **變更後簽章 (After)**: `fn Ignore::add_child_path(&self, dir: &Path)` (L273~L368)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn add_child_path(&self, dir: &Path) -> (IgnoreInner, Option<Error>) {
        let check_vcs_dir = self.inner.opts.require_git
            && (self.inner.opts.git_ignore || self.inner.opts.git_exclude);
        let git_type = if check_vcs_dir {
            dir.join(".git").metadata().ok().map(|md| md.file_type())
        } else {
            None
        };
        let has_git =
            check_vcs_dir && (git_type.is_some() || dir.join(".jj").exists());

        let mut errs = PartialErrorBuilder::default();
        let custom_ig_matcher =
            if self.inner.custom_ignore_filenames.is_empty() {
                Gitignore::empty()
            } else {
                let (m, err) = create_gitignore(
                    &dir,
                    &dir,
                    &self.inner.custom_ignore_filenames,
                    self.inner.opts.ignore_case_insensitive,
                );
                errs.maybe_push(err);
                m
            };
        let ig_matcher = if !self.inner.opts.ignore {
            Gitignore::empty()
        } else {
            let (m, err) = create_gitignore(
                &dir,
                &dir,
                &[".ignore"],
                self.inner.opts.ignore_case_insensitive,
            );
            errs.maybe_push(err);
            m
        };
        let gi_matcher = if !self.inner.opts.git_ignore {
            Gitignore::empty()
        } else {
            let (m, err) = create_gitignore(
                &dir,
                &dir,
                &[".gitignore"],
                self.inner.opts.ignore_case_insensitive,
            );
            errs.maybe_push(err);
            m
        };

        let gi_exclude_matcher = if !self.inner.opts.git_exclude {
            Gitignore::empty()
        } else {
            match resolve_git_commondir(dir, git_type) {
                Ok(git_dir) => {
                    let (m, err) = create_gitignore(
                        &dir,
                        &git_dir,
                        &["info/exclude"],
                        self.inner.opts.ignore_case_insensitive,
                    );
                    errs.maybe_push(err);
                    m
                }
                Err(err) => {
                    errs.maybe_push(err);
                    Gitignore::empty()
                }
            }
        };
        let ig = IgnoreInner {
            compiled: self.inner.compiled.clone(),
            dir: dir.to_path_buf(),
            overrides: self.inner.overrides.clone(),
            types: self.inner.types.clone(),
            parent: Some(self.clone()),
            is_absolute_parent: false,
            absolute_base: self.inner.absolute_base.clone(),
            global_gitignores_relative_to: self
                .inner
                .global_gitignores_relative_to
                .clone(),
            explicit_ignores: self.inner.explicit_ignores.clone(),
            custom_ignore_filenames: self
                .inner
                .custom_ignore_filenames
                .clone(),
            custom_ignore_matcher: custom_ig_matcher,
            ignore_matcher: ig_matcher,
            git_global_matcher: self.inner.git_global_matcher.clone(),
            git_ignore_matcher: gi_matcher,
            git_exclude_matcher: gi_exclude_matcher,
            has_git,
            opts: self.inner.opts,
        };
        (ig, errs.into_error_option())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn add_child_path(&self, dir: &Path) -> (IgnoreInner, Option<Error>) {
        let check_vcs_dir = self.inner.opts.require_git
            && (self.inner.opts.git_ignore || self.inner.opts.git_exclude);
        let git_type = if check_vcs_dir {
            dir.join(".git").metadata().ok().map(|md| md.file_type())
        } else {
            None
        };
        let has_git =
            check_vcs_dir && (git_type.is_some() || dir.join(".jj").exists());

        let mut errs = PartialErrorBuilder::default();
        let custom_ig_matcher =
            if self.inner.custom_ignore_filenames.is_empty() {
                Gitignore::empty()
            } else {
                let (m, err) = create_gitignore(
                    &dir,
                    &dir,
                    &self.inner.custom_ignore_filenames,
                    self.inner.opts.ignore_case_insensitive,
                );
                errs.maybe_push(err);
                m
            };
        let ig_matcher = if !self.inner.opts.ignore {
            Gitignore::empty()
        } else {
            let (m, err) = create_gitignore(
                &dir,
                &dir,
                &[".ignore"],
                self.inner.opts.ignore_case_insensitive,
            );
            errs.maybe_push(err);
            m
        };
        let gi_matcher = if !self.inner.opts.git_ignore {
            Gitignore::empty()
        } else {
            let (m, err) = create_gitignore(
                &dir,
                &dir,
                &[".gitignore"],
                self.inner.opts.ignore_case_insensitive,
            );
            errs.maybe_push(err);
            m
        };

        let gi_exclude_matcher = if !self.inner.opts.git_exclude {
            Gitignore::empty()
        } else {
            match resolve_git_commondir(dir, git_type) {
                Ok(git_dir) => {
                    let (m, err) = create_gitignore(
                        &dir,
                        &git_dir,
                        &["info/exclude"],
                        self.inner.opts.ignore_case_insensitive,
                    );
                    errs.maybe_push(err);
                    m
                }
                Err(err) => {
                    errs.maybe_push(err);
                    Gitignore::empty()
                }
            }
        };
        let ig = IgnoreInner {
            compiled: self.inner.compiled.clone(),
            dir: dir.to_path_buf(),
            overrides: self.inner.overrides.clone(),
            types: self.inner.types.clone(),
            parent: Some(self.inner.clone()),
            is_absolute_parent: false,
            global_gitignores_relative_to: self
                .inner
                .global_gitignores_relative_to
                .clone(),
            explicit_ignores: self.inner.explicit_ignores.clone(),
            custom_ignore_filenames: self
                .inner
                .custom_ignore_filenames
                .clone(),
            custom_ignore_matcher: custom_ig_matcher,
            ignore_matcher: ig_matcher,
            git_global_matcher: self.inner.git_global_matcher.clone(),
            git_ignore_matcher: gi_matcher,
            git_exclude_matcher: gi_exclude_matcher,
            has_git,
            opts: self.inner.opts,
        };
        (ig, errs.into_error_option())
    }
```

### 🔹 函式: `Ignore::add_child()`
- **變更前簽章 (Before)**: `fn Ignore::add_child(
        &self,
        dir: P,
    )` (L251~L257)
- **變更後簽章 (After)**: `fn Ignore::add_child(
        &self,
        dir: P,
    )` (L258~L270)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn add_child<P: AsRef<Path>>(
        &self,
        dir: P,
    ) -> (Ignore, Option<Error>) {
        let (ig, err) = self.add_child_path(dir.as_ref());
        (Ignore { inner: Arc::new(ig) }, err)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn add_child<P: AsRef<Path>>(
        &self,
        dir: P,
    ) -> (Ignore, Option<Error>) {
        let (ig, err) = self.add_child_path(dir.as_ref());
        (
            Ignore {
                inner: Arc::new(ig),
                absolute_base: self.absolute_base.clone(),
            },
            err,
        )
    }
```

### 🔹 函式: `Ignore::parents()`
- **變更前簽章 (Before)**: `fn Ignore::parents(&self)` (L577~L579)
- **變更後簽章 (After)**: `fn Ignore::parents(&self)` (L589~L591)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn parents(&self) -> Parents<'_> {
        Parents(Some(self))
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn parents(&self) -> Parents<'_> {
        Parents(Some(IgnoreRef { inner: &self.inner }))
    }
```

### 🔹 函式: `IgnoreBuilder::build_with_cwd()`
- **變更前簽章 (Before)**: `fn IgnoreBuilder::build_with_cwd(&self, cwd: Option<PathBuf>)` (L673~L718)
- **變更後簽章 (After)**: `fn IgnoreBuilder::build_with_cwd(&self, cwd: Option<PathBuf>)` (L702~L747)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn build_with_cwd(&self, cwd: Option<PathBuf>) -> Ignore {
        let global_gitignores_relative_to =
            cwd.or_else(|| self.global_gitignores_relative_to.clone());
        let git_global_matcher = if !self.opts.git_global {
            Gitignore::empty()
        } else if let Some(ref cwd) = global_gitignores_relative_to {
            let mut builder = GitignoreBuilder::new(cwd);
            builder
                .case_insensitive(self.opts.ignore_case_insensitive)
                .unwrap();
            let (gi, err) = builder.build_global();
            if let Some(err) = err {
                log::debug!("{}", err);
            }
            gi
        } else {
            log::debug!(
                "ignoring global gitignore file because CWD is not known"
            );
            Gitignore::empty()
        };

        Ignore {
            inner: Arc::new(IgnoreInner {
                compiled: Arc::new(RwLock::new(HashMap::new())),
                dir: self.dir.clone(),
                overrides: self.overrides.clone(),
                types: self.types.clone(),
                parent: None,
                is_absolute_parent: true,
                absolute_base: None,
                global_gitignores_relative_to,
                explicit_ignores: Arc::new(self.explicit_ignores.clone()),
                custom_ignore_filenames: Arc::new(
                    self.custom_ignore_filenames.clone(),
                ),
                custom_ignore_matcher: Gitignore::empty(),
                ignore_matcher: Gitignore::empty(),
                git_global_matcher: Arc::new(git_global_matcher),
                git_ignore_matcher: Gitignore::empty(),
                git_exclude_matcher: Gitignore::empty(),
                has_git: false,
                opts: self.opts,
            }),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn build_with_cwd(&self, cwd: Option<PathBuf>) -> Ignore {
        let global_gitignores_relative_to =
            cwd.or_else(|| self.global_gitignores_relative_to.clone());
        let git_global_matcher = if !self.opts.git_global {
            Gitignore::empty()
        } else if let Some(ref cwd) = global_gitignores_relative_to {
            let mut builder = GitignoreBuilder::new(cwd);
            builder
                .case_insensitive(self.opts.ignore_case_insensitive)
                .unwrap();
            let (gi, err) = builder.build_global();
            if let Some(err) = err {
                log::debug!("{}", err);
            }
            gi
        } else {
            log::debug!(
                "ignoring global gitignore file because CWD is not known"
            );
            Gitignore::empty()
        };

        Ignore {
            inner: Arc::new(IgnoreInner {
                compiled: Arc::new(RwLock::new(HashMap::new())),
                dir: self.dir.clone(),
                overrides: self.overrides.clone(),
                types: self.types.clone(),
                parent: None,
                is_absolute_parent: true,
                global_gitignores_relative_to,
                explicit_ignores: Arc::new(self.explicit_ignores.clone()),
                custom_ignore_filenames: Arc::new(
                    self.custom_ignore_filenames.clone(),
                ),
                custom_ignore_matcher: Gitignore::empty(),
                ignore_matcher: Gitignore::empty(),
                git_global_matcher: Arc::new(git_global_matcher),
                git_ignore_matcher: Gitignore::empty(),
                git_exclude_matcher: Gitignore::empty(),
                has_git: false,
                opts: self.opts,
            }),
            absolute_base: None,
        }
    }
```

### 🔹 函式: `Ignore::add_parents()`
- **變更前簽章 (Before)**: `fn Ignore::add_parents(
        &self,
        path: P,
    )` (L180~L241)
- **變更後簽章 (After)**: `fn Ignore::add_parents(
        &self,
        path: P,
    )` (L182~L248)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn add_parents<P: AsRef<Path>>(
        &self,
        path: P,
    ) -> (Ignore, Option<Error>) {
        if !self.inner.opts.parents
            && !self.inner.opts.git_ignore
            && !self.inner.opts.git_exclude
            && !self.inner.opts.git_global
        {
            // If we never need info from parent directories, then don't do
            // anything.
            return (self.clone(), None);
        }
        if !self.is_root() {
            panic!("Ignore::add_parents called on non-root matcher");
        }
        let absolute_base = match path.as_ref().canonicalize() {
            Ok(path) => Arc::new(path),
            Err(_) => {
                // There's not much we can do here, so just return our
                // existing matcher. We drop the error to be consistent
                // with our general pattern of ignoring I/O errors when
                // processing ignore files.
                return (self.clone(), None);
            }
        };
        // List of parents, from child to root.
        let mut parents = vec![];
        let mut path = &**absolute_base;
        while let Some(parent) = path.parent() {
            parents.push(parent);
            path = parent;
        }
        let mut errs = PartialErrorBuilder::default();
        let mut ig = self.clone();
        for parent in parents.into_iter().rev() {
            let mut compiled = self.inner.compiled.write().unwrap();
            if let Some(weak) = compiled.get(parent.as_os_str()) {
                if let Some(prebuilt) = weak.upgrade() {
                    ig = Ignore { inner: prebuilt };
                    continue;
                }
            }
            let (mut igtmp, err) = ig.add_child_path(parent);
            errs.maybe_push(err);
            igtmp.is_absolute_parent = true;
            igtmp.absolute_base = Some(absolute_base.clone());
            igtmp.has_git =
                if self.inner.opts.require_git && self.inner.opts.git_ignore {
                    parent.join(".git").exists() || parent.join(".jj").exists()
                } else {
                    false
                };
            let ig_arc = Arc::new(igtmp);
            ig = Ignore { inner: ig_arc.clone() };
            compiled.insert(
                parent.as_os_str().to_os_string(),
                Arc::downgrade(&ig_arc),
            );
        }
        (ig, errs.into_error_option())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn add_parents<P: AsRef<Path>>(
        &self,
        path: P,
    ) -> (Ignore, Option<Error>) {
        if !self.inner.opts.parents
            && !self.inner.opts.git_ignore
            && !self.inner.opts.git_exclude
            && !self.inner.opts.git_global
        {
            // If we never need info from parent directories, then don't do
            // anything.
            return (self.clone(), None);
        }
        if !self.is_root() {
            panic!("Ignore::add_parents called on non-root matcher");
        }
        let absolute_base = match path.as_ref().canonicalize() {
            Ok(path) => Arc::new(path),
            Err(_) => {
                // There's not much we can do here, so just return our
                // existing matcher. We drop the error to be consistent
                // with our general pattern of ignoring I/O errors when
                // processing ignore files.
                return (self.clone(), None);
            }
        };
        // List of parents, from child to root.
        let mut parents = vec![];
        let mut path = &**absolute_base;
        while let Some(parent) = path.parent() {
            parents.push(parent);
            path = parent;
        }
        let mut errs = PartialErrorBuilder::default();
        let mut ig = self.clone();
        for parent in parents.into_iter().rev() {
            let mut compiled = self.inner.compiled.write().unwrap();
            if let Some(weak) = compiled.get(parent.as_os_str()) {
                if let Some(prebuilt) = weak.upgrade() {
                    ig = Ignore {
                        inner: prebuilt,
                        absolute_base: Some(absolute_base.clone()),
                    };
                    continue;
                }
            }
            let (mut igtmp, err) = ig.add_child_path(parent);
            errs.maybe_push(err);
            igtmp.is_absolute_parent = true;
            igtmp.has_git =
                if self.inner.opts.require_git && self.inner.opts.git_ignore {
                    parent.join(".git").exists() || parent.join(".jj").exists()
                } else {
                    false
                };
            let ig_arc = Arc::new(igtmp);
            ig = Ignore {
                inner: ig_arc.clone(),
                absolute_base: Some(absolute_base.clone()),
            };
            compiled.insert(
                parent.as_os_str().to_os_string(),
                Arc::downgrade(&ig_arc),
            );
        }
        (ig, errs.into_error_option())
    }
```

### 🔹 函式: `Ignore::absolute_base()`
- **變更前簽章 (Before)**: `fn Ignore::absolute_base(&self)` (L583~L585)
- **變更後簽章 (After)**: `fn Ignore::absolute_base(&self)` (L595~L597)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn absolute_base(&self) -> Option<&Path> {
        self.inner.absolute_base.as_ref().map(|p| &***p)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn absolute_base(&self) -> Option<&Path> {
        self.absolute_base.as_ref().map(|p| &***p)
    }
```

### 🔹 函式: `Parents::next()`
- **變更前簽章 (Before)**: `fn Parents::next(&mut self)` (L596~L604)
- **變更後簽章 (After)**: `fn Parents::next(&mut self)` (L621~L633)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn next(&mut self) -> Option<&'a Ignore> {
        match self.0.take() {
            None => None,
            Some(ig) => {
                self.0 = ig.inner.parent.as_ref();
                Some(ig)
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn next(&mut self) -> Option<IgnoreRef<'a>> {
        match self.0.take() {
            None => None,
            Some(ig) => {
                self.0 = ig
                    .inner
                    .parent
                    .as_deref()
                    .map(|inner| IgnoreRef { inner });
                Some(ig)
            }
        }
    }
```

### 🔹 函式: `Ignore::parent()`
- **變更前簽章 (Before)**: `fn Ignore::parent(&self)` (L172~L174)
- **變更後簽章 (After)**: `fn Ignore::parent(&self)` (L171~L176)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn parent(&self) -> Option<Ignore> {
        self.inner.parent.clone()
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn parent(&self) -> Option<Ignore> {
        self.inner.parent.as_ref().map(|parent| Ignore {
            inner: parent.clone(),
            absolute_base: self.absolute_base.clone(),
        })
    }
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/ripgrep show 020687a77d13146923333f0beb274eeabd54a270
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 020687a77d13146923333f0beb274eeabd54a270~1 --file test_repos/ripgrep/crates/ignore/src/gitignore.rs
   ```
