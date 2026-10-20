# 🔬 CODE-Map 基準審查獨立驗證報告: `bat`
> **技術生態**: `Rust (現代語法高亮終端分頁器 / CLI)`  
> **本地倉庫路徑**: `test_repos/bat`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 25 Files  
> **報告生成時間**: 2026-10-20 21:42:27  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `20` / `25` | `80.0%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `4` / `25` | `16.0%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `1` / `25` | `4.0%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`24` / `25`** | **`96.0%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `25` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `c2adbf6c`
- **完整 Hash**: `c2adbf6caad083b137beff082426f228a840e007`
- **說明 (Ground Truth)**: Fix the first line of UTF-16BE input swallowing the second line
- **變更檔案數**: 1

#### 📄 檔案: `src/input.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:128, E:172, A:0) ➔ After(N:129, E:173, A:0)
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
  • + [新增節點] `first_line.ends_with (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `InputReader::try_new` ──[CALLS]──> `first_line.ends_with (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `InputReader::try_new()`
- **變更前簽章 (Before)**: `fn InputReader::try_new(mut reader: R)` (L267~L304)
- **變更後簽章 (After)**: `fn InputReader::try_new(mut reader: R)` (L267~L309)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn try_new<R: BufRead + 'a>(mut reader: R) -> io::Result<InputReader<'a>> {
        // content_inspector scans at most 1024 bytes. Capture the already-buffered
        // prefix before splitting out the first line so an early newline in binary
        // data does not shorten the inspected content. This does not consume input
        // or perform an additional read beyond the one read_until needs anyway.
        let mut inspection_prefix = {
            let buffered = reader.fill_buf()?;
            buffered[..buffered.len().min(CONTENT_INSPECTION_LIMIT)].to_vec()
        };

        let mut first_line = vec![];
        if !inspection_prefix.is_empty() {
            reader.read_until(b'\n', &mut first_line)?;
        }

        // A custom BufRead implementation may expose less than 1024 bytes at a
        // time. Keep the old behavior for long first lines in that case.
        let first_line_prefix_len = first_line.len().min(CONTENT_INSPECTION_LIMIT);
        if first_line_prefix_len > inspection_prefix.len() {
            inspection_prefix.clear();
            inspection_prefix.extend_from_slice(&first_line[..first_line_prefix_len]);
        }

        let content_type = inspect_content_type(&inspection_prefix);

        if content_type == Some(ContentType::UTF_16LE) {
            read_utf16_line(&mut reader, &mut first_line, 0x00, 0x0A)?;
        } else if content_type == Some(ContentType::UTF_16BE) {
            read_utf16_line(&mut reader, &mut first_line, 0x0A, 0x00)?;
        }

        Ok(InputReader {
            inner: Box::new(reader),
            first_line,
            content_type,
            unbuffered: false,
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn try_new<R: BufRead + 'a>(mut reader: R) -> io::Result<InputReader<'a>> {
        // content_inspector scans at most 1024 bytes. Capture the already-buffered
        // prefix before splitting out the first line so an early newline in binary
        // data does not shorten the inspected content. This does not consume input
        // or perform an additional read beyond the one read_until needs anyway.
        let mut inspection_prefix = {
            let buffered = reader.fill_buf()?;
            buffered[..buffered.len().min(CONTENT_INSPECTION_LIMIT)].to_vec()
        };

        let mut first_line = vec![];
        if !inspection_prefix.is_empty() {
            reader.read_until(b'\n', &mut first_line)?;
        }

        // A custom BufRead implementation may expose less than 1024 bytes at a
        // time. Keep the old behavior for long first lines in that case.
        let first_line_prefix_len = first_line.len().min(CONTENT_INSPECTION_LIMIT);
        if first_line_prefix_len > inspection_prefix.len() {
            inspection_prefix.clear();
            inspection_prefix.extend_from_slice(&first_line[..first_line_prefix_len]);
        }

        let content_type = inspect_content_type(&inspection_prefix);

        if content_type == Some(ContentType::UTF_16LE) {
            read_utf16_line(&mut reader, &mut first_line, 0x00, 0x0A)?;
        } else if content_type == Some(ContentType::UTF_16BE)
            // In UTF-16BE a newline is encoded as 0x00 0x0A, so `read_until(b'\n')` above
            // may already have read a complete first line. Only keep reading if it did not
            // (e.g. the 0x0A byte was part of another character such as U+4E0A).
            && !(first_line.len() % 2 == 0 && first_line.ends_with(&[0x00, 0x0A]))
        {
            read_utf16_line(&mut reader, &mut first_line, 0x0A, 0x00)?;
        }

        Ok(InputReader {
            inner: Box::new(reader),
            first_line,
            content_type,
            unbuffered: false,
        })
    }
```


---

### 🔹 Commit #02: `a56bca50`
- **完整 Hash**: `a56bca503b3de78eae4903566cee1388d4bd67d0`
- **說明 (Ground Truth)**: Fix doc comments on four Config fields
- **變更檔案數**: 1

#### 📄 檔案: `src/config.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:25, E:41, A:0) ➔ After(N:25, E:41, A:0)
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

### 🔹 Commit #03: `b8430080`
- **完整 Hash**: `b8430080f071a8cc9853b12dd4ea6234ba8d8357`
- **說明 (Ground Truth)**: fix: use last occurrence in combined short flags
- **變更檔案數**: 1

#### 📄 檔案: `src/bin/bat/app.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:216, E:251, A:0) ➔ After(N:216, E:251, A:0)
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
  • + [新增節點] `chars.iter().rposition (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `chars.iter().position (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `App::new` ──[CALLS]──> `chars.iter().rposition (External/Unresolved)`
  • - [移除呼叫邊] `App::new` ──[CALLS]──> `chars.iter().position (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `App::new()`
- **變更前簽章 (Before)**: `fn App::new()` (L69~L171)
- **變更後簽章 (After)**: `fn App::new()` (L69~L171)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn new() -> Result<Self> {
        #[cfg(windows)]
        let _ = nu_ansi_term::enable_ansi_support();

        let interactive_output = std::io::stdout().is_terminal();

        // Check if the -n / --number option was passed on the command line
        // (before merging with config file and environment variables).
        // This is needed to honor the -n flag when piping output, similar to `cat -n`.
        // We need to handle both standalone (-n, --number) and combined short flags (-pn, -An, etc.)
        // Note: We only check if -n appears and is not overridden by -p in the same combined flag.
        // For combined flags like -np, -p comes after -n and overrides it, so we don't count it.
        // For combined flags like -pn, -n comes after -p and takes effect.
        let number_from_cli = wild::args_os().any(|arg| {
            let arg_str = arg.to_string_lossy();
            if arg_str == "-n" || arg_str == "--number" {
                return true;
            }
            // Handle combined short flags
            // Only count -n if it's the LAST flag in the combined form (so -p doesn't override it)
            // or if -p is not present in the combined form
            if arg_str.starts_with('-') && !arg_str.starts_with("--") && arg_str.len() > 2 {
                let chars: Vec<char> = arg_str.chars().skip(1).collect();
                let n_pos = chars.iter().position(|&c| c == 'n');
                let p_pos = chars.iter().position(|&c| c == 'p');
                // -n is in the combined flag and either:
                // - -p is not present, OR
                // - -n comes after -p (so -n takes effect)
                if let Some(n) = n_pos {
                    if p_pos.is_none() || n > p_pos.unwrap() {
                        return true;
                    }
                }
            }
            false
        });

        // Check if the -b / --number-nonblank option was passed on the command line
        // (before merging with config file and environment variables).
        // This is needed to honor the -b flag when piping output, similar to `cat -b`.
        // The same combined-flag logic applies as for -n above.
        let number_nonblank_from_cli = wild::args_os().any(|arg| {
            let arg_str = arg.to_string_lossy();
            if arg_str == "-b" || arg_str == "--number-nonblank" {
                return true;
            }
            // Handle combined short flags
            if arg_str.starts_with('-') && !arg_str.starts_with("--") && arg_str.len() > 2 {
                let chars: Vec<char> = arg_str.chars().skip(1).collect();
                let b_pos = chars.iter().position(|&c| c == 'b');
                let p_pos = chars.iter().position(|&c| c == 'p');
                if let Some(b) = b_pos {
                    if p_pos.is_none() || b > p_pos.unwrap() {
                        return true;
                    }
                }
            }
            false
        });

        let matches = Self::matches(interactive_output)?;

        if matches.get_flag("help") {
            let help_type = if wild::args_os().any(|arg| arg == "--help") {
                HelpType::Long
            } else {
                HelpType::Short
            };

            let use_pager = match matches.get_one::<String>("paging").map(|s| s.as_str()) {
                Some("never") => false,
                _ => !matches.get_flag("no-paging"),
            };

            let use_color = match matches.get_one::<String>("color").map(|s| s.as_str()) {
                Some("always") => true,
                Some("never") => false,
                _ => interactive_output, // auto: use color if interactive
            };

            let pager = matches.get_one::<String>("pager").map(|s| s.as_str());
            let theme_options = Self::theme_options_from_matches(&matches);
            let use_custom_assets = !matches.get_flag("no-custom-assets");

            Self::display_help(
                interactive_output,
                help_type,
                use_pager,
                use_color,
                pager,
                theme_options,
                use_custom_assets,
            )?;
            std::process::exit(0);
        }

        Ok(App {
            matches,
            interactive_output,
            number_from_cli,
            number_nonblank_from_cli,
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn new() -> Result<Self> {
        #[cfg(windows)]
        let _ = nu_ansi_term::enable_ansi_support();

        let interactive_output = std::io::stdout().is_terminal();

        // Check if the -n / --number option was passed on the command line
        // (before merging with config file and environment variables).
        // This is needed to honor the -n flag when piping output, similar to `cat -n`.
        // We need to handle both standalone (-n, --number) and combined short flags (-pn, -An, etc.)
        // Note: We only check if -n appears and is not overridden by -p in the same combined flag.
        // For combined flags like -np, -p comes after -n and overrides it, so we don't count it.
        // For combined flags like -pn, -n comes after -p and takes effect.
        let number_from_cli = wild::args_os().any(|arg| {
            let arg_str = arg.to_string_lossy();
            if arg_str == "-n" || arg_str == "--number" {
                return true;
            }
            // Handle combined short flags
            // Only count -n if its last occurrence comes after the last -p,
            // or if -p is not present in the combined form.
            if arg_str.starts_with('-') && !arg_str.starts_with("--") && arg_str.len() > 2 {
                let chars: Vec<char> = arg_str.chars().skip(1).collect();
                let n_pos = chars.iter().rposition(|&c| c == 'n');
                let p_pos = chars.iter().rposition(|&c| c == 'p');
                // -n is in the combined flag and either:
                // - -p is not present, OR
                // - -n comes after -p (so -n takes effect)
                if let Some(n) = n_pos {
                    if p_pos.is_none() || n > p_pos.unwrap() {
                        return true;
                    }
                }
            }
            false
        });

        // Check if the -b / --number-nonblank option was passed on the command line
        // (before merging with config file and environment variables).
        // This is needed to honor the -b flag when piping output, similar to `cat -b`.
        // The same combined-flag logic applies as for -n above.
        let number_nonblank_from_cli = wild::args_os().any(|arg| {
            let arg_str = arg.to_string_lossy();
            if arg_str == "-b" || arg_str == "--number-nonblank" {
                return true;
            }
            // Handle combined short flags by comparing the last -b and -p occurrences.
            if arg_str.starts_with('-') && !arg_str.starts_with("--") && arg_str.len() > 2 {
                let chars: Vec<char> = arg_str.chars().skip(1).collect();
                let b_pos = chars.iter().rposition(|&c| c == 'b');
                let p_pos = chars.iter().rposition(|&c| c == 'p');
                if let Some(b) = b_pos {
                    if p_pos.is_none() || b > p_pos.unwrap() {
                        return true;
                    }
                }
            }
            false
        });

        let matches = Self::matches(interactive_output)?;

        if matches.get_flag("help") {
            let help_type = if wild::args_os().any(|arg| arg == "--help") {
                HelpType::Long
            } else {
                HelpType::Short
            };

            let use_pager = match matches.get_one::<String>("paging").map(|s| s.as_str()) {
                Some("never") => false,
                _ => !matches.get_flag("no-paging"),
            };

            let use_color = match matches.get_one::<String>("color").map(|s| s.as_str()) {
                Some("always") => true,
                Some("never") => false,
                _ => interactive_output, // auto: use color if interactive
            };

            let pager = matches.get_one::<String>("pager").map(|s| s.as_str());
            let theme_options = Self::theme_options_from_matches(&matches);
            let use_custom_assets = !matches.get_flag("no-custom-assets");

            Self::display_help(
                interactive_output,
                help_type,
                use_pager,
                use_color,
                pager,
                theme_options,
                use_custom_assets,
            )?;
            std::process::exit(0);
        }

        Ok(App {
            matches,
            interactive_output,
            number_from_cli,
            number_nonblank_from_cli,
        })
    }
```


---

### 🔹 Commit #04: `a96b9e22`
- **完整 Hash**: `a96b9e2230e1d0b7293b47feeab6297fd85888cd`
- **說明 (Ground Truth)**: Detect binary content beyond the first line
- **變更檔案數**: 1

#### 📄 檔案: `src/input.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:107, E:144, A:0) ➔ After(N:128, E:172, A:0)
- **差分統計**: +Nodes: 21, -Nodes: 0, +Edges: 28, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `OneRead (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `binary_detection_scans_beyond_first_line_and_preserves_input` (FUNCTION_DEF)
  • + [新增節點] `input_detection_does_not_read_twice` (FUNCTION_DEF)
  • + [新增節點] `inspection_prefix.len (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `OneRead::read` (FUNCTION_DEF)
  • + [新增節點] `buf[..content.len()].copy_from_slice (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `buffered.len (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `buffered.len().min (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `first_line.len().min (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `CONTENT_INSPECTION_LIMIT` (MODULE_STATE)
  • + [新增節點] `first_line.len (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `reader.read_line(&mut replayed).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `reader.fill_buf (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `inspection_prefix.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `inspection_prefix.clear (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 34 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `InputReader::try_new()`
- **變更前簽章 (Before)**: `fn InputReader::try_new(mut reader: R)` (L265~L283)
- **變更後簽章 (After)**: `fn InputReader::try_new(mut reader: R)` (L267~L304)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn try_new<R: BufRead + 'a>(mut reader: R) -> io::Result<InputReader<'a>> {
        let mut first_line = vec![];
        reader.read_until(b'\n', &mut first_line)?;

        let content_type = inspect_content_type(&first_line);

        if content_type == Some(ContentType::UTF_16LE) {
            read_utf16_line(&mut reader, &mut first_line, 0x00, 0x0A)?;
        } else if content_type == Some(ContentType::UTF_16BE) {
            read_utf16_line(&mut reader, &mut first_line, 0x0A, 0x00)?;
        }

        Ok(InputReader {
            inner: Box::new(reader),
            first_line,
            content_type,
            unbuffered: false,
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn try_new<R: BufRead + 'a>(mut reader: R) -> io::Result<InputReader<'a>> {
        // content_inspector scans at most 1024 bytes. Capture the already-buffered
        // prefix before splitting out the first line so an early newline in binary
        // data does not shorten the inspected content. This does not consume input
        // or perform an additional read beyond the one read_until needs anyway.
        let mut inspection_prefix = {
            let buffered = reader.fill_buf()?;
            buffered[..buffered.len().min(CONTENT_INSPECTION_LIMIT)].to_vec()
        };

        let mut first_line = vec![];
        if !inspection_prefix.is_empty() {
            reader.read_until(b'\n', &mut first_line)?;
        }

        // A custom BufRead implementation may expose less than 1024 bytes at a
        // time. Keep the old behavior for long first lines in that case.
        let first_line_prefix_len = first_line.len().min(CONTENT_INSPECTION_LIMIT);
        if first_line_prefix_len > inspection_prefix.len() {
            inspection_prefix.clear();
            inspection_prefix.extend_from_slice(&first_line[..first_line_prefix_len]);
        }

        let content_type = inspect_content_type(&inspection_prefix);

        if content_type == Some(ContentType::UTF_16LE) {
            read_utf16_line(&mut reader, &mut first_line, 0x00, 0x0A)?;
        } else if content_type == Some(ContentType::UTF_16BE) {
            read_utf16_line(&mut reader, &mut first_line, 0x0A, 0x00)?;
        }

        Ok(InputReader {
            inner: Box::new(reader),
            first_line,
            content_type,
            unbuffered: false,
        })
    }
```


---

### 🔹 Commit #05: `c2cc79da`
- **完整 Hash**: `c2cc79daa747bbbfcdec22bf1eea95a1d1ef8aa2`
- **說明 (Ground Truth)**: Fix --sanitize passing through the bidi control characters U+200E, U+200F and U+061C
- **變更檔案數**: 1

#### 📄 檔案: `src/preprocessor.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:88, E:102, A:0) ➔ After(N:90, E:104, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `test_sanitize_preserves_arabic_sharing_the_alm_lead_byte` (FUNCTION_DEF)
  • + [新增節點] `test_sanitize_substitutes_every_bidi_control` (FUNCTION_DEF)
  • + [新增呼叫邊] `test_sanitize_substitutes_every_bidi_control` ──[CALLS]──> `assert_eq! (Macro)`
  • + [新增呼叫邊] `test_sanitize_preserves_arabic_sharing_the_alm_lead_byte` ──[CALLS]──> `assert_eq! (Macro)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `sanitize_at()`
- **變更前簽章 (Before)**: `fn sanitize_at(
    bytes: &[u8],
    i: usize,
    full: &str,
    buffer: &mut String,
    start: &mut usize,
)` (L176~L216)
- **變更後簽章 (After)**: `fn sanitize_at(
    bytes: &[u8],
    i: usize,
    full: &str,
    buffer: &mut String,
    start: &mut usize,
)` (L176~L222)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn sanitize_at(
    bytes: &[u8],
    i: usize,
    full: &str,
    buffer: &mut String,
    start: &mut usize,
) -> usize {
    buffer.push_str(&full[*start..i]);
    let consumed = match bytes[i] {
        b'\r' if bytes.get(i + 1) == Some(&b'\n') => {
            buffer.push_str("\r\n");
            2
        }
        // 0xC2 leads U+0080..U+00FF; filter the C1 range.
        0xC2 if matches!(bytes.get(i + 1), Some(0x80..=0x9F)) => {
            buffer.push('\u{FFFD}');
            2
        }
        0xE2 if is_dangerous_e2(bytes, i) => {
            buffer.push('\u{FFFD}');
            3
        }
        // 0xEF 0xBB 0xBF = U+FEFF (BOM / zero-width no-break space).
        0xEF if bytes.get(i + 1) == Some(&0xBB) && bytes.get(i + 2) == Some(&0xBF) => {
            buffer.push('\u{FFFD}');
            3
        }
        // False-alarm trigger: pass the full UTF-8 sequence through.
        lead @ (0xC2 | 0xE2 | 0xEF) => {
            let n = utf8_len_from_lead(lead);
            buffer.push_str(&full[i..i + n]);
            n
        }
        _ => {
            buffer.push('\u{FFFD}');
            1
        }
    };
    *start = i + consumed;
    consumed
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn sanitize_at(
    bytes: &[u8],
    i: usize,
    full: &str,
    buffer: &mut String,
    start: &mut usize,
) -> usize {
    buffer.push_str(&full[*start..i]);
    let consumed = match bytes[i] {
        b'\r' if bytes.get(i + 1) == Some(&b'\n') => {
            buffer.push_str("\r\n");
            2
        }
        // 0xC2 leads U+0080..U+00FF; filter the C1 range.
        0xC2 if matches!(bytes.get(i + 1), Some(0x80..=0x9F)) => {
            buffer.push('\u{FFFD}');
            2
        }
        0xE2 if is_dangerous_e2(bytes, i) => {
            buffer.push('\u{FFFD}');
            3
        }
        // 0xEF 0xBB 0xBF = U+FEFF (BOM / zero-width no-break space).
        0xEF if bytes.get(i + 1) == Some(&0xBB) && bytes.get(i + 2) == Some(&0xBF) => {
            buffer.push('\u{FFFD}');
            3
        }
        // 0xD8 0x9C = U+061C (Arabic letter mark, a bidi control). The rest of
        // the 0xD8 block is ordinary Arabic text.
        0xD8 if bytes.get(i + 1) == Some(&0x9C) => {
            buffer.push('\u{FFFD}');
            2
        }
        // False-alarm trigger: pass the full UTF-8 sequence through.
        lead @ (0xC2 | 0xD8 | 0xE2 | 0xEF) => {
            let n = utf8_len_from_lead(lead);
            buffer.push_str(&full[i..i + n]);
            n
        }
        _ => {
            buffer.push('\u{FFFD}');
            1
        }
    };
    *start = i + consumed;
    consumed
}
```

### 🔹 函式: `is_dangerous_e2()`
- **變更前簽章 (Before)**: `fn is_dangerous_e2(bytes: &[u8], i: usize)` (L219~L225)
- **變更後簽章 (After)**: `fn is_dangerous_e2(bytes: &[u8], i: usize)` (L225~L232)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn is_dangerous_e2(bytes: &[u8], i: usize) -> bool {
    // U+200B..D (zero-width), U+202A..E (bidi controls), U+2066..9 (isolates).
    matches!(
        (bytes.get(i + 1), bytes.get(i + 2)),
        (Some(0x80), Some(0x8B..=0x8D | 0xAA..=0xAE)) | (Some(0x81), Some(0xA6..=0xA9))
    )
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn is_dangerous_e2(bytes: &[u8], i: usize) -> bool {
    // U+200B..D (zero-width), U+200E..F (LRM/RLM), U+202A..E (bidi embedding
    // and override), U+2066..9 (bidi isolates).
    matches!(
        (bytes.get(i + 1), bytes.get(i + 2)),
        (Some(0x80), Some(0x8B..=0x8F | 0xAA..=0xAE)) | (Some(0x81), Some(0xA6..=0xA9))
    )
}
```

### 🔹 函式: `is_sanitize_trigger()`
- **變更前簽章 (Before)**: `fn is_sanitize_trigger(b: u8)` (L169~L172)
- **變更後簽章 (After)**: `fn is_sanitize_trigger(b: u8)` (L169~L172)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn is_sanitize_trigger(b: u8) -> bool {
    // C0 controls minus \t \n \f; DEL; UTF-8 leads with dangerous codepoints.
    matches!(b, 0x00..=0x08 | 0x0B | 0x0D..=0x1F | 0x7F | 0xC2 | 0xE2 | 0xEF)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn is_sanitize_trigger(b: u8) -> bool {
    // C0 controls minus \t \n \f; DEL; UTF-8 leads with dangerous codepoints.
    matches!(b, 0x00..=0x08 | 0x0B | 0x0D..=0x1F | 0x7F | 0xC2 | 0xD8 | 0xE2 | 0xEF)
}
```


---

### 🔹 Commit #06: `c75cc01e`
- **完整 Hash**: `c75cc01eef9b1a61611c9e10e767e7b90e44e29b`
- **說明 (Ground Truth)**: Fix --ignored-suffix to fall back to first-line detection
- **變更檔案數**: 1

#### 📄 檔案: `src/assets.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:185, E:262, A:0) ➔ After(N:188, E:265, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 4, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `test.syntax_mapping.insert_ignored_suffix (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `syntax_detection_ignored_suffix_falls_back_to_first_line` (FUNCTION_DEF)
  • + [新增節點] `self.get_syntax_for_file_extension(stripped_file_name, ignored_suffixes)
                    .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `HighlightingAssets::get_syntax_for_file_extension` ──[CALLS]──> `self.get_syntax_for_file_extension(stripped_file_name, ignored_suffixes)
                    .map (External/Unresolved)`
  • + [新增呼叫邊] `syntax_detection_ignored_suffix_falls_back_to_first_line` ──[CALLS]──> `SyntaxDetectionTest::new`
  • + [新增呼叫邊] `syntax_detection_ignored_suffix_falls_back_to_first_line` ──[CALLS]──> `assert_eq! (Macro)`
  • + [新增呼叫邊] `syntax_detection_ignored_suffix_falls_back_to_first_line` ──[CALLS]──> `test.syntax_mapping.insert_ignored_suffix (External/Unresolved)`
  • - [移除呼叫邊] `HighlightingAssets::get_syntax_for_file_extension` ──[CALLS]──> `syntax.is_none (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `HighlightingAssets::get_syntax_for_file_extension()`
- **變更前簽章 (Before)**: `fn HighlightingAssets::get_syntax_for_file_extension(
        &self,
        file_name: &OsStr,
        ignored_suffixes: &IgnoredSuffixes,
    )` (L345~L359)
- **變更後簽章 (After)**: `fn HighlightingAssets::get_syntax_for_file_extension(
        &self,
        file_name: &OsStr,
        ignored_suffixes: &IgnoredSuffixes,
    )` (L345~L359)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn get_syntax_for_file_extension(
        &self,
        file_name: &OsStr,
        ignored_suffixes: &IgnoredSuffixes,
    ) -> Result<Option<SyntaxReferenceInSet<'_>>> {
        let mut syntax = self.find_syntax_by_extension(Path::new(file_name).extension())?;
        if syntax.is_none() {
            syntax =
                ignored_suffixes.try_with_stripped_suffix(file_name, |stripped_file_name| {
                    // Note: recursion
                    self.get_syntax_for_file_extension(stripped_file_name, ignored_suffixes)
                })?;
        }
        Ok(syntax)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn get_syntax_for_file_extension(
        &self,
        file_name: &OsStr,
        ignored_suffixes: &IgnoredSuffixes,
    ) -> Result<Option<SyntaxReferenceInSet<'_>>> {
        let stripped =
            ignored_suffixes.try_with_stripped_suffix(file_name, |stripped_file_name| {
                self.get_syntax_for_file_extension(stripped_file_name, ignored_suffixes)
                    .map(Some)
            })?;
        match stripped {
            Some(syntax) => Ok(syntax),
            None => self.find_syntax_by_extension(Path::new(file_name).extension()),
        }
    }
```


---

### 🔹 Commit #07: `df164cc2`
- **完整 Hash**: `df164cc2e3cacb286551a99ff172fae6e135d4ce`
- **說明 (Ground Truth)**: fix immediate dereference of reference
- **變更檔案數**: 1

#### 📄 檔案: `src/diff.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:69, E:87, A:0) ➔ After(N:69, E:87, A:0)
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

### 🔹 函式: `create_and_track_file()`
- **變更前簽章 (Before)**: `fn create_and_track_file(repo: &tempfile::TempDir, filename: &str)` (L116~L123)
- **變更後簽章 (After)**: `fn create_and_track_file(repo: &tempfile::TempDir, filename: &str)` (L116~L123)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn create_and_track_file(repo: &tempfile::TempDir, filename: &str) -> PathBuf {
        let filepath = repo.path().join(filename);
        std::fs::write(&filepath, "file\n").expect("can write file");
        git(repo.path(), &["add", &filename]);
        git(repo.path(), &["commit", "-m", "initial"]);

        filepath.to_owned()
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn create_and_track_file(repo: &tempfile::TempDir, filename: &str) -> PathBuf {
        let filepath = repo.path().join(filename);
        std::fs::write(&filepath, "file\n").expect("can write file");
        git(repo.path(), &["add", filename]);
        git(repo.path(), &["commit", "-m", "initial"]);

        filepath.to_owned()
    }
```


---

### 🔹 Commit #08: `fa00fb8c`
- **完整 Hash**: `fa00fb8ce8a9b3d139166cd7f7c225f9ae52f2d6`
- **說明 (Ground Truth)**: fix(list-languages): clamp desired_width to avoid usize underflow at tiny --terminal-width
- **變更檔案數**: 1

#### 📄 檔案: `src/bin/bat/main.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:167, E:179, A:1) ➔ After(N:169, E:181, A:1)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#CLI: main** `(CLI Entry)`
    └── ⚡ **run()**
        └── 🎯 [TRIGGERS] `main()`
            └── 🎯 [CALLS] `default_error_handler (External/Unresolved)()`
            └── 🎯 [CALLS] `process::exit (External/Unresolved)()`
            └── 🎯 [CALLS] `std::io::stderr (External/Unresolved)()`
            └── 🎯 [CALLS] `stderr.lock (External/Unresolved)()`
            └── 🎯 [CALLS] `run()`
                └── 🎯 [CALLS] `App::new (External/Unresolved)()`
                └── 🎯 [CALLS] `Default::default (External/Unresolved)()`
                └── 🎯 [CALLS] `Ok (External/Unresolved)()`
                └── 🎯 [CALLS] `PROJECT_DIRS.cache_dir (External/Unresolved)()`
                └── 🎯 [CALLS] `PROJECT_DIRS.config_dir (External/Unresolved)()`
                └── 🎯 [CALLS] `StyleComponent::Plain.components (External/Unresolved)()`
                └── 🎯 [CALLS] `StyleComponents::new (External/Unresolved)()`
                └── 🎯 [CALLS] `app.config (External/Unresolved)()`
                └── 🎯 [CALLS] `app.inputs (External/Unresolved)()`
                └── 🎯 [CALLS] `app.matches.get_flag (External/Unresolved)()`
                └── 🎯 [CALLS] `app.matches.get_one::<String> (External/Unresolved)()`
                └── 🎯 [CALLS] `app.matches.subcommand (External/Unresolved)()`
                └── 🎯 [CALLS] `app.theme_options (External/Unresolved)()`
                └── 🎯 [CALLS] `cache_matches.args_present (External/Unresolved)()`
                └── 🎯 [CALLS] `generate_config_file (External/Unresolved)()`
                └── 🎯 [CALLS] `println! (Macro)()`
                └── 🎯 [CALLS] `shell.as_str (External/Unresolved)()`
                └── 🎯 [CALLS] `unreachable! (Macro)()`
                └── 🎯 [CALLS] `vec! (Macro)()`
                └── 🎯 [CALLS] `writeln! (Macro)()`
                └── 🎯 [CALLS] `get_languages()`
+                   └── 🟢 [CALLS] `config
            .term_width
            .saturating_sub (External/Unresolved)()` [新增因果]
+                   └── 🟢 [CALLS] `config
            .term_width
            .saturating_sub(longest)
            .saturating_sub (External/Unresolved)()` [新增因果]
                    └── 🎯 [CALLS] `Green.normal (External/Unresolved)()`
                    └── *ref:`Ok (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `Path::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `Path::new("test").with_extension (External/Unresolved)()`
                    └── 🎯 [CALLS] `Path::new(extension).extension (External/Unresolved)()`
                    └── 🎯 [CALLS] `Path::new(extension).extension().is_some (External/Unresolved)()`
                    └── 🎯 [CALLS] `String::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `Style::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `additional_paths.iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `additional_paths.iter().cloned (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter()
        .filter (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter()
        .filter(|syntax| !syntax.hidden && !syntax.file_extensions.is_empty())
        .cloned (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter()
        .filter(|syntax| !syntax.hidden && !syntax.file_extensions.is_empty())
        .cloned()
        .collect::<Vec<_>> (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets.get_syntax_for_path (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets_from_cache_or_binary (External/Unresolved)()`
                    └── 🎯 [CALLS] `comma_separator.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `config.syntax_mapping.all_mappings (External/Unresolved)()`
                    └── 🎯 [CALLS] `configured_languages.get (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.next (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.peek (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.peek().is_some (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.starts_with (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions
                .extend (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions.iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions.iter().peekable (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions.retain (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.name.as_str (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.name.clone (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.name.to_uppercase (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter()
            .map (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter()
            .map(|syntax| syntax.name.len())
            .max (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter()
            .map(|syntax| syntax.name.len())
            .max()
            .unwrap_or (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages.sort_by_key (External/Unresolved)()`
                    └── 🎯 [CALLS] `matches! (Macro)()`
                    └── 🎯 [CALLS] `separator.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `syntax.file_extensions.is_empty (External/Unresolved)()`
                    └── 🎯 [CALLS] `syntax.name.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `word.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `write! (Macro)()`
                    └── 🎯 [CALLS] `write!(result, "\n{:width$}{separator}", "", width = longest).ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `write!(result, "{:width$}{separator}", lang.name, width = longest).ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `write!(result, "{}", style.paint(&word[..])).ok (External/Unresolved)()`
                    └── *ref:`writeln! (Macro)` [已折疊指針]
                    └── 🎯 [CALLS] `writeln!(result, "{}:{}", lang.name, lang.file_extensions.join(",")).ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `get_syntax_mapping_to_paths()`
                        └── 🎯 [CALLS] `HashMap::new (External/Unresolved)()`
                        └── 🎯 [CALLS] `globs.push (External/Unresolved)()`
                        └── 🎯 [CALLS] `map.entry (External/Unresolved)()`
                        └── 🎯 [CALLS] `map.entry(*s).or_insert_with (External/Unresolved)()`
                        └── 🎯 [CALLS] `matcher.glob (External/Unresolved)()`
                        └── 🎯 [CALLS] `matcher.glob().glob (External/Unresolved)()`
                        └── 🎯 [CALLS] `matcher.glob().glob().into (External/Unresolved)()`
                └── 🎯 [CALLS] `invoke_bugreport()`
                    └── 🎯 [CALLS] `"less".to_owned (External/Unresolved)()`
                    └── 🎯 [CALLS] `CommandLine::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `CommandOutput::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `CompileTimeInformation::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `DirectoryEntries::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `EnvironmentVariables::list (External/Unresolved)()`
                    └── 🎯 [CALLS] `FileContent::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `OperatingSystem::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `SoftwareVersion::default (External/Unresolved)()`
                    └── *ref:`app.matches.get_one::<String> (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `app.matches.get_one::<String>("pager").map (External/Unresolved)()`
                    └── 🎯 [CALLS] `bat::config::get_pager_executable (External/Unresolved)()`
                    └── 🎯 [CALLS] `bat::config::get_pager_executable(
        app.matches.get_one::<String>("pager").map(|s| s.as_str()),
    )
    .unwrap_or_else (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport! (Macro)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `cache_dir.to_path_buf (External/Unresolved)()`
                    └── 🎯 [CALLS] `config_file (External/Unresolved)()`
                    └── 🎯 [CALLS] `custom_assets_metadata.push (External/Unresolved)()`
                    └── 🎯 [CALLS] `grep_cli::resolve_binary (External/Unresolved)()`
                    └── 🎯 [CALLS] `report.info (External/Unresolved)()`
                    └── 🎯 [CALLS] `report.print::<Markdown> (External/Unresolved)()`
                    └── 🎯 [CALLS] `s.as_str (External/Unresolved)()`
                    └── 🎯 [CALLS] `system_config_file (External/Unresolved)()`
                └── 🎯 [CALLS] `list_themes()`
                    └── 🎯 [CALLS] `Controller::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `Controller::new(&config, &assets)
                .run(vec![theme_preview_file()], Some(&mut handle))
                .ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `HashSet::new (External/Unresolved)()`
                    └── *ref:`Ok (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `OutputHandle::FmtWrite (External/Unresolved)()`
                    └── 🎯 [CALLS] `OutputType::from_mode (External/Unresolved)()`
                    └── 🎯 [CALLS] `Some (External/Unresolved)()`
                    └── *ref:`String::new (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `StyleComponents (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets.themes (External/Unresolved)()`
                    └── *ref:`assets_from_cache_or_binary (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `cfg.clone (External/Unresolved)()`
                    └── 🎯 [CALLS] `default_theme (External/Unresolved)()`
                    └── 🎯 [CALLS] `format_args! (Macro)()`
                    └── 🎯 [CALLS] `handle.write_fmt (External/Unresolved)()`
                    └── 🎯 [CALLS] `output_type.handle (External/Unresolved)()`
                    └── 🎯 [CALLS] `style.insert (External/Unresolved)()`
                    └── 🎯 [CALLS] `theme (External/Unresolved)()`
                    └── 🎯 [CALLS] `theme(theme_options).to_string (External/Unresolved)()`
                    └── 🎯 [CALLS] `theme.to_string (External/Unresolved)()`
                    └── *ref:`vec! (Macro)` [已折疊指針]
                    └── 🎯 [CALLS] `writer.write_fmt (External/Unresolved)()`
                    └── *ref:`run` [已折疊指針]
                └── 🎯 [CALLS] `run_cache_subcommand()`
                    └── 🎯 [CALLS] `build_assets()`
                        └── 🎯 [CALLS] `bat::assets::build (External/Unresolved)()`
                        └── 🎯 [CALLS] `clap::crate_version! (Macro)()`
                        └── 🎯 [CALLS] `matches
        .get_one::<String> (External/Unresolved)()`
                        └── 🎯 [CALLS] `matches
        .get_one::<String>("source")
        .map (External/Unresolved)()`
                        └── 🎯 [CALLS] `matches
        .get_one::<String>("source")
        .map(Path::new)
        .unwrap_or_else (External/Unresolved)()`
                        └── 🎯 [CALLS] `matches.get_flag (External/Unresolved)()`
                    └── *ref:`Ok (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `clear_assets (External/Unresolved)()`
                    └── *ref:`matches
        .get_one::<String> (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `matches
        .get_one::<String>("target")
        .map (External/Unresolved)()`
                    └── 🎯 [CALLS] `matches
        .get_one::<String>("target")
        .map(Path::new)
        .unwrap_or_else (External/Unresolved)()`
                    └── *ref:`matches.get_flag (External/Unresolved)` [已折疊指針]
                    └── *ref:`println! (Macro)` [已折疊指針]
                └── 🎯 [CALLS] `run_controller()`
                    └── *ref:`Controller::new (External/Unresolved)` [已折疊指針]
                    └── *ref:`assets_from_cache_or_binary (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `get_new_terminal_title()`
                        └── 🎯 [CALLS] `ColorSchemeCollector::description()`
                        └── 🎯 [CALLS] `"bat: ".to_string (External/Unresolved)()`
                        └── 🎯 [CALLS] `input.description().title (External/Unresolved)()`
                        └── 🎯 [CALLS] `inputs.iter (External/Unresolved)()`
                        └── 🎯 [CALLS] `inputs.iter().enumerate (External/Unresolved)()`
                        └── 🎯 [CALLS] `inputs.len (External/Unresolved)()`
                    └── *ref:`run` [已折疊指針]
                    └── 🎯 [CALLS] `set_terminal_title_to()`
                        └── 🎯 [CALLS] `bat::sanitize_for_terminal (External/Unresolved)()`
                        └── 🎯 [CALLS] `io::stdout (External/Unresolved)()`
                        └── 🎯 [CALLS] `io::stdout().flush (External/Unresolved)()`
                        └── 🎯 [CALLS] `io::stdout().flush().unwrap (External/Unresolved)()`
                        └── 🎯 [CALLS] `print! (Macro)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `config
            .term_width
            .saturating_sub(longest)
            .saturating_sub (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `config
            .term_width
            .saturating_sub (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `get_languages` ──[CALLS]──> `config
            .term_width
            .saturating_sub(longest)
            .saturating_sub (External/Unresolved)`
  • + [新增呼叫邊] `get_languages` ──[CALLS]──> `config
            .term_width
            .saturating_sub (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `get_languages()`
- **變更前簽章 (Before)**: `fn get_languages(config: &Config, cache_dir: &Path)` (L100~L189)
- **變更後簽章 (After)**: `fn get_languages(config: &Config, cache_dir: &Path)` (L100~L196)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn get_languages(config: &Config, cache_dir: &Path) -> Result<String> {
    let mut result: String = String::new();

    let assets = assets_from_cache_or_binary(config.use_custom_assets, cache_dir)?;
    let mut languages = assets
        .get_syntaxes()?
        .iter()
        .filter(|syntax| !syntax.hidden && !syntax.file_extensions.is_empty())
        .cloned()
        .collect::<Vec<_>>();

    // Handling of file-extension conflicts, see issue #1076
    for lang in &mut languages {
        let lang_name = lang.name.clone();
        lang.file_extensions.retain(|extension| {
            // The 'extension' variable is not certainly a real extension.
            //
            // Skip if 'extension' starts with '.', likely a hidden file like '.vimrc'
            // Also skip if the 'extension' contains another real extension, likely
            // that is a full match file name like 'CMakeLists.txt' and 'Cargo.lock'
            if extension.starts_with('.') || Path::new(extension).extension().is_some() {
                return true;
            }

            let test_file = Path::new("test").with_extension(extension);
            let syntax_in_set = assets.get_syntax_for_path(test_file, &config.syntax_mapping);
            matches!(syntax_in_set, Ok(syntax_in_set) if syntax_in_set.syntax.name == lang_name)
        });
    }

    languages.sort_by_key(|lang| lang.name.to_uppercase());

    let configured_languages = get_syntax_mapping_to_paths(config.syntax_mapping.all_mappings());

    for lang in &mut languages {
        if let Some(additional_paths) = configured_languages.get(lang.name.as_str()) {
            lang.file_extensions
                .extend(additional_paths.iter().cloned());
        }
    }

    if config.loop_through {
        for lang in languages {
            writeln!(result, "{}:{}", lang.name, lang.file_extensions.join(",")).ok();
        }
    } else {
        let longest = languages
            .iter()
            .map(|syntax| syntax.name.len())
            .max()
            .unwrap_or(32); // Fallback width if they have no language definitions.

        let comma_separator = ", ";
        let separator = " ";
        // Line-wrapping for the possible file extension overflow.
        let desired_width = config.term_width - longest - separator.len();

        let style = if config.colored_output {
            Green.normal()
        } else {
            Style::default()
        };

        for lang in languages {
            write!(result, "{:width$}{separator}", lang.name, width = longest).ok();

            // Number of characters on this line so far, wrap before `desired_width`
            let mut num_chars = 0;

            let mut extension = lang.file_extensions.iter().peekable();
            while let Some(word) = extension.next() {
                // If we can't fit this word in, then create a line break and align it in.
                let new_chars = word.len() + comma_separator.len();
                if num_chars + new_chars >= desired_width {
                    num_chars = 0;
                    write!(result, "\n{:width$}{separator}", "", width = longest).ok();
                }

                num_chars += new_chars;
                write!(result, "{}", style.paint(&word[..])).ok();
                if extension.peek().is_some() {
                    result += comma_separator;
                }
            }
            result += "\n";
        }
    }

    Ok(result)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn get_languages(config: &Config, cache_dir: &Path) -> Result<String> {
    let mut result: String = String::new();

    let assets = assets_from_cache_or_binary(config.use_custom_assets, cache_dir)?;
    let mut languages = assets
        .get_syntaxes()?
        .iter()
        .filter(|syntax| !syntax.hidden && !syntax.file_extensions.is_empty())
        .cloned()
        .collect::<Vec<_>>();

    // Handling of file-extension conflicts, see issue #1076
    for lang in &mut languages {
        let lang_name = lang.name.clone();
        lang.file_extensions.retain(|extension| {
            // The 'extension' variable is not certainly a real extension.
            //
            // Skip if 'extension' starts with '.', likely a hidden file like '.vimrc'
            // Also skip if the 'extension' contains another real extension, likely
            // that is a full match file name like 'CMakeLists.txt' and 'Cargo.lock'
            if extension.starts_with('.') || Path::new(extension).extension().is_some() {
                return true;
            }

            let test_file = Path::new("test").with_extension(extension);
            let syntax_in_set = assets.get_syntax_for_path(test_file, &config.syntax_mapping);
            matches!(syntax_in_set, Ok(syntax_in_set) if syntax_in_set.syntax.name == lang_name)
        });
    }

    languages.sort_by_key(|lang| lang.name.to_uppercase());

    let configured_languages = get_syntax_mapping_to_paths(config.syntax_mapping.all_mappings());

    for lang in &mut languages {
        if let Some(additional_paths) = configured_languages.get(lang.name.as_str()) {
            lang.file_extensions
                .extend(additional_paths.iter().cloned());
        }
    }

    if config.loop_through {
        for lang in languages {
            writeln!(result, "{}:{}", lang.name, lang.file_extensions.join(",")).ok();
        }
    } else {
        let longest = languages
            .iter()
            .map(|syntax| syntax.name.len())
            .max()
            .unwrap_or(32); // Fallback width if they have no language definitions.

        let comma_separator = ", ";
        let separator = " ";
        // Line-wrapping for the possible file extension overflow.
        // Clamp instead of subtracting: a tiny `--terminal-width` (smaller than the
        // longest language name) would otherwise underflow `usize` and wrap to a huge
        // value, silently disabling wrapping (and panicking in debug/overflow-checked
        // builds). Mirrors the `saturating_sub` fix applied to `print_snip` in #3804.
        let desired_width = config
            .term_width
            .saturating_sub(longest)
            .saturating_sub(separator.len());

        let style = if config.colored_output {
            Green.normal()
        } else {
            Style::default()
        };

        for lang in languages {
            write!(result, "{:width$}{separator}", lang.name, width = longest).ok();

            // Number of characters on this line so far, wrap before `desired_width`
            let mut num_chars = 0;

            let mut extension = lang.file_extensions.iter().peekable();
            while let Some(word) = extension.next() {
                // If we can't fit this word in, then create a line break and align it in.
                let new_chars = word.len() + comma_separator.len();
                if num_chars + new_chars >= desired_width {
                    num_chars = 0;
                    write!(result, "\n{:width$}{separator}", "", width = longest).ok();
                }

                num_chars += new_chars;
                write!(result, "{}", style.paint(&word[..])).ok();
                if extension.peek().is_some() {
                    result += comma_separator;
                }
            }
            result += "\n";
        }
    }

    Ok(result)
}
```


---

### 🔹 Commit #09: `d28aa4a8`
- **完整 Hash**: `d28aa4a8b4d9fe4fb5567e708cde82d03953f1ee`
- **說明 (Ground Truth)**: Fix capacity-overflow panic in print_snip at --terminal-width 1
- **變更檔案數**: 1

#### 📄 檔案: `src/printer.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:160, E:190, A:0) ➔ After(N:163, E:193, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 3, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `self.config
                .term_width
                .saturating_sub (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.config
                .term_width
                .saturating_sub(panel_count)
                .saturating_sub (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.config
                .term_width
                .saturating_sub(panel_count)
                .saturating_sub(snip_left_count)
                .saturating_sub (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `InteractivePrinter::print_snip` ──[CALLS]──> `self.config
                .term_width
                .saturating_sub(panel_count)
                .saturating_sub (External/Unresolved)`
  • + [新增呼叫邊] `InteractivePrinter::print_snip` ──[CALLS]──> `self.config
                .term_width
                .saturating_sub (External/Unresolved)`
  • + [新增呼叫邊] `InteractivePrinter::print_snip` ──[CALLS]──> `self.config
                .term_width
                .saturating_sub(panel_count)
                .saturating_sub(snip_left_count)
                .saturating_sub (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `InteractivePrinter::print_snip()`
- **變更前簽章 (Before)**: `fn InteractivePrinter::print_snip(&mut self, handle: &mut OutputHandle)` (L599~L621)
- **變更後簽章 (After)**: `fn InteractivePrinter::print_snip(&mut self, handle: &mut OutputHandle)` (L599~L633)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn print_snip(&mut self, handle: &mut OutputHandle) -> Result<()> {
        let panel = self.create_fake_panel(" ...");
        let panel_count = panel.chars().count();

        let title = "8<";
        let title_count = title.chars().count();

        let snip_left = "─ ".repeat((self.config.term_width - panel_count - (title_count / 2)) / 4);
        let snip_left_count = snip_left.chars().count(); // Can't use .len() with Unicode.

        let snip_right =
            " ─".repeat((self.config.term_width - panel_count - snip_left_count - title_count) / 2);

        writeln!(
            handle,
            "{}",
            self.colors
                .grid
                .paint(format!("{panel}{snip_left}{title}{snip_right}"))
        )?;

        Ok(())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn print_snip(&mut self, handle: &mut OutputHandle) -> Result<()> {
        let panel = self.create_fake_panel(" ...");
        let panel_count = panel.chars().count();

        let title = "8<";
        let title_count = title.chars().count();

        let snip_left = "─ ".repeat(
            self.config
                .term_width
                .saturating_sub(panel_count)
                .saturating_sub(title_count / 2)
                / 4,
        );
        let snip_left_count = snip_left.chars().count(); // Can't use .len() with Unicode.

        let snip_right = " ─".repeat(
            self.config
                .term_width
                .saturating_sub(panel_count)
                .saturating_sub(snip_left_count)
                .saturating_sub(title_count)
                / 2,
        );

        writeln!(
            handle,
            "{}",
            self.colors
                .grid
                .paint(format!("{panel}{snip_left}{title}{snip_right}"))
        )?;

        Ok(())
    }
```


---

### 🔹 Commit #10: `530e83a4`
- **完整 Hash**: `530e83a45506a4792e788944a75a2e89b82518ab`
- **說明 (Ground Truth)**: feat: bat auto-detects language from stdin via first-line patterns
- **變更檔案數**: 1

#### 📄 檔案: `src/assets.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:185, E:262, A:0) ➔ After(N:184, E:261, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 5, +Edges: 4, -Edges: 5, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `std::str::from_utf8(&reader.first_line)
            .ok()
            .and_then(|l| {
                // Strip UTF-8 BOM if present
                let line = l.strip_prefix('\u{feff}').unwrap_or(l);
                syntax_set.find_syntax_by_first_line(line)
            })
            .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `std::str::from_utf8(&reader.first_line)
            .ok()
            .and_then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `std::str::from_utf8(&reader.first_line)
            .ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `std::str::from_utf8 (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `String::from_utf8(reader.first_line.clone())
            .ok()
            .and_then(|l| {
                // Strip UTF-8 BOM if present
                let line = l.strip_prefix('\u{feff}').unwrap_or(&l);
                syntax_set.find_syntax_by_first_line(line)
            })
            .map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `String::from_utf8(reader.first_line.clone())
            .ok (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `reader.first_line.clone (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `String::from_utf8 (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `String::from_utf8(reader.first_line.clone())
            .ok()
            .and_then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `HighlightingAssets::get_first_line_syntax` ──[CALLS]──> `std::str::from_utf8(&reader.first_line)
            .ok()
            .and_then(|l| {
                // Strip UTF-8 BOM if present
                let line = l.strip_prefix('\u{feff}').unwrap_or(l);
                syntax_set.find_syntax_by_first_line(line)
            })
            .map (External/Unresolved)`
  • + [新增呼叫邊] `HighlightingAssets::get_first_line_syntax` ──[CALLS]──> `std::str::from_utf8(&reader.first_line)
            .ok()
            .and_then (External/Unresolved)`
  • + [新增呼叫邊] `HighlightingAssets::get_first_line_syntax` ──[CALLS]──> `std::str::from_utf8(&reader.first_line)
            .ok (External/Unresolved)`
  • + [新增呼叫邊] `HighlightingAssets::get_first_line_syntax` ──[CALLS]──> `std::str::from_utf8 (External/Unresolved)`
  • - [移除呼叫邊] `HighlightingAssets::get_first_line_syntax` ──[CALLS]──> `String::from_utf8(reader.first_line.clone())
            .ok()
            .and_then(|l| {
                // Strip UTF-8 BOM if present
                let line = l.strip_prefix('\u{feff}').unwrap_or(&l);
                syntax_set.find_syntax_by_first_line(line)
            })
            .map (External/Unresolved)`
  • - [移除呼叫邊] `HighlightingAssets::get_first_line_syntax` ──[CALLS]──> `String::from_utf8(reader.first_line.clone())
            .ok()
            .and_then (External/Unresolved)`
  • _... 以及其餘 3 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `HighlightingAssets::get_first_line_syntax()`
- **變更前簽章 (Before)**: `fn HighlightingAssets::get_first_line_syntax(
        &self,
        reader: &mut InputReader,
    )` (L355~L368)
- **變更後簽章 (After)**: `fn HighlightingAssets::get_first_line_syntax(
        &self,
        reader: &mut InputReader,
    )` (L355~L368)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn get_first_line_syntax(
        &self,
        reader: &mut InputReader,
    ) -> Result<Option<SyntaxReferenceInSet<'_>>> {
        let syntax_set = self.get_syntax_set()?;
        Ok(String::from_utf8(reader.first_line.clone())
            .ok()
            .and_then(|l| {
                // Strip UTF-8 BOM if present
                let line = l.strip_prefix('\u{feff}').unwrap_or(&l);
                syntax_set.find_syntax_by_first_line(line)
            })
            .map(|syntax| SyntaxReferenceInSet { syntax, syntax_set }))
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn get_first_line_syntax(
        &self,
        reader: &mut InputReader,
    ) -> Result<Option<SyntaxReferenceInSet<'_>>> {
        let syntax_set = self.get_syntax_set()?;
        Ok(std::str::from_utf8(&reader.first_line)
            .ok()
            .and_then(|l| {
                // Strip UTF-8 BOM if present
                let line = l.strip_prefix('\u{feff}').unwrap_or(l);
                syntax_set.find_syntax_by_first_line(line)
            })
            .map(|syntax| SyntaxReferenceInSet { syntax, syntax_set }))
    }
```


---

### 🔹 Commit #11: `c437ad4d`
- **完整 Hash**: `c437ad4d27d3d082397cbfc37db6379f06548e4c`
- **說明 (Ground Truth)**: fix command injection in LESS template
- **變更檔案數**: 1

#### 📄 檔案: `src/lessopen.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:65, E:88, A:0) ➔ After(N:75, E:99, A:0)
- **差分統計**: +Nodes: 13, -Nodes: 3, +Edges: 14, -Edges: 3, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `s.chars (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `s.len (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `shell_substitute` (FUNCTION_DEF)
  • + [新增節點] `shell_quote_plain_filename` (FUNCTION_DEF)
  • + [新增節點] `shell_quote_embedded_single_quote` (FUNCTION_DEF)
  • + [新增節點] `quoted.push (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `shell_substitute_only_replaces_first_percent_s` (FUNCTION_DEF)
  • + [新增節點] `String::with_capacity (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `shell_substitute_protects_against_filename_injection` (FUNCTION_DEF)
  • + [新增節點] `quoted.push_str (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `shell_quote` (FUNCTION_DEF)
  • + [新增節點] `shell_quote_metacharacters_neutralised` (FUNCTION_DEF)
  • + [新增節點] `template.replacen (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `s.replacen (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `s.replacen("%s", &path_str, 1).replacen (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 18 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `LessOpenPreprocessor::open()`
- **變更前簽章 (Before)**: `fn LessOpenPreprocessor::open(
        &self,
        input: Input<'a>,
        mut stdin: R,
        stdout_identifier: Option<&Identifier>,
    )` (L77~L199)
- **變更後簽章 (After)**: `fn LessOpenPreprocessor::open(
        &self,
        input: Input<'a>,
        mut stdin: R,
        stdout_identifier: Option<&Identifier>,
    )` (L97~L219)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn open<'a, R: BufRead + 'a>(
        &self,
        input: Input<'a>,
        mut stdin: R,
        stdout_identifier: Option<&Identifier>,
    ) -> Result<OpenedInput<'a>> {
        let (lessopen_stdout, path_str, kind) = match input.kind {
            InputKind::OrdinaryFile(ref path) => {
                let path_str = match path.to_str() {
                    Some(str) => str,
                    None => return input.open(stdin, stdout_identifier),
                };

                let mut lessopen_command = shell(self.lessopen.replacen("%s", path_str, 1));
                lessopen_command.stdout(Stdio::piped());

                let lessopen_output = match lessopen_command.execute_output() {
                    Ok(output) => output,
                    Err(_) => return input.open(stdin, stdout_identifier),
                };

                if self.fall_back_to_original_file(&lessopen_output.stdout, lessopen_output.status)
                {
                    return input.open(stdin, stdout_identifier);
                }

                (
                    lessopen_output.stdout,
                    path_str.to_string(),
                    OpenedInputKind::OrdinaryFile(path.to_path_buf()),
                )
            }
            InputKind::StdIn => {
                if self.preprocess_stdin {
                    if let Some(stdout) = stdout_identifier {
                        let input_identifier = Identifier::try_from(clircle::Stdio::Stdin)
                            .map_err(|e| format!("Stdin: Error identifying file: {e}"))?;
                        if stdout.surely_conflicts_with(&input_identifier) {
                            return Err("IO circle detected. The input from stdin is also an output. Aborting to avoid infinite loop.".into());
                        }
                    }

                    // stdin isn't Clone or AsRef<[u8]>, so move it into a cloneable buffer
                    // so the data can be used multiple times if necessary
                    // NOTE: stdin will be empty from this point onwards
                    let mut stdin_buffer = Vec::new();
                    stdin.read_to_end(&mut stdin_buffer)?;

                    let mut lessopen_command = shell(self.lessopen.replacen("%s", "-", 1));
                    lessopen_command.stdout(Stdio::piped());

                    let lessopen_output = match lessopen_command.execute_input_output(&stdin_buffer)
                    {
                        Ok(output) => output,
                        Err(_) => {
                            return input.open(Cursor::new(stdin_buffer), stdout_identifier);
                        }
                    };

                    if self
                        .fall_back_to_original_file(&lessopen_output.stdout, lessopen_output.status)
                    {
                        return input.open(Cursor::new(stdin_buffer), stdout_identifier);
                    }

                    (
                        lessopen_output.stdout,
                        "-".to_string(),
                        OpenedInputKind::StdIn,
                    )
                } else {
                    return input.open(stdin, stdout_identifier);
                }
            }
            InputKind::CustomReader(_) => {
                return input.open(stdin, stdout_identifier);
            }
        };

        Ok(OpenedInput {
            kind,
            reader: InputReader::try_new(BufReader::new(
                if matches!(self.kind, LessOpenKind::TempFile) {
                    let lessopen_string = match String::from_utf8(lessopen_stdout) {
                        Ok(string) => string,
                        Err(_) => {
                            return input.open(stdin, stdout_identifier);
                        }
                    };
                    // Remove newline at end of temporary file path returned by $LESSOPEN
                    let stdout = match lessopen_string.strip_suffix("\n") {
                        Some(stripped) => stripped.to_owned(),
                        None => lessopen_string,
                    };

                    let file = match File::open(PathBuf::from(&stdout)) {
                        Ok(file) => file,
                        Err(_) => {
                            return input.open(stdin, stdout_identifier);
                        }
                    };

                    Preprocessed {
                        kind: PreprocessedKind::TempFile(file),
                        lessclose: self
                            .lessclose
                            .as_ref()
                            .map(|s| s.replacen("%s", &path_str, 1).replacen("%s", &stdout, 1)),
                    }
                } else {
                    Preprocessed {
                        kind: PreprocessedKind::Piped(Cursor::new(lessopen_stdout)),
                        lessclose: self
                            .lessclose
                            .as_ref()
                            .map(|s| s.replacen("%s", &path_str, 1).replacen("%s", "-", 1)),
                    }
                },
            ))?,
            metadata: input.metadata,
            description: input.description,
        })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn open<'a, R: BufRead + 'a>(
        &self,
        input: Input<'a>,
        mut stdin: R,
        stdout_identifier: Option<&Identifier>,
    ) -> Result<OpenedInput<'a>> {
        let (lessopen_stdout, path_str, kind) = match input.kind {
            InputKind::OrdinaryFile(ref path) => {
                let path_str = match path.to_str() {
                    Some(str) => str,
                    None => return input.open(stdin, stdout_identifier),
                };

                let mut lessopen_command = shell(shell_substitute(&self.lessopen, path_str));
                lessopen_command.stdout(Stdio::piped());

                let lessopen_output = match lessopen_command.execute_output() {
                    Ok(output) => output,
                    Err(_) => return input.open(stdin, stdout_identifier),
                };

                if self.fall_back_to_original_file(&lessopen_output.stdout, lessopen_output.status)
                {
                    return input.open(stdin, stdout_identifier);
                }

                (
                    lessopen_output.stdout,
                    path_str.to_string(),
                    OpenedInputKind::OrdinaryFile(path.to_path_buf()),
                )
            }
            InputKind::StdIn => {
                if self.preprocess_stdin {
                    if let Some(stdout) = stdout_identifier {
                        let input_identifier = Identifier::try_from(clircle::Stdio::Stdin)
                            .map_err(|e| format!("Stdin: Error identifying file: {e}"))?;
                        if stdout.surely_conflicts_with(&input_identifier) {
                            return Err("IO circle detected. The input from stdin is also an output. Aborting to avoid infinite loop.".into());
                        }
                    }

                    // stdin isn't Clone or AsRef<[u8]>, so move it into a cloneable buffer
                    // so the data can be used multiple times if necessary
                    // NOTE: stdin will be empty from this point onwards
                    let mut stdin_buffer = Vec::new();
                    stdin.read_to_end(&mut stdin_buffer)?;

                    let mut lessopen_command = shell(shell_substitute(&self.lessopen, "-"));
                    lessopen_command.stdout(Stdio::piped());

                    let lessopen_output = match lessopen_command.execute_input_output(&stdin_buffer)
                    {
                        Ok(output) => output,
                        Err(_) => {
                            return input.open(Cursor::new(stdin_buffer), stdout_identifier);
                        }
                    };

                    if self
                        .fall_back_to_original_file(&lessopen_output.stdout, lessopen_output.status)
                    {
                        return input.open(Cursor::new(stdin_buffer), stdout_identifier);
                    }

                    (
                        lessopen_output.stdout,
                        "-".to_string(),
                        OpenedInputKind::StdIn,
                    )
                } else {
                    return input.open(stdin, stdout_identifier);
                }
            }
            InputKind::CustomReader(_) => {
                return input.open(stdin, stdout_identifier);
            }
        };

        Ok(OpenedInput {
            kind,
            reader: InputReader::try_new(BufReader::new(
                if matches!(self.kind, LessOpenKind::TempFile) {
                    let lessopen_string = match String::from_utf8(lessopen_stdout) {
                        Ok(string) => string,
                        Err(_) => {
                            return input.open(stdin, stdout_identifier);
                        }
                    };
                    // Remove newline at end of temporary file path returned by $LESSOPEN
                    let stdout = match lessopen_string.strip_suffix("\n") {
                        Some(stripped) => stripped.to_owned(),
                        None => lessopen_string,
                    };

                    let file = match File::open(PathBuf::from(&stdout)) {
                        Ok(file) => file,
                        Err(_) => {
                            return input.open(stdin, stdout_identifier);
                        }
                    };

                    Preprocessed {
                        kind: PreprocessedKind::TempFile(file),
                        lessclose: self
                            .lessclose
                            .as_ref()
                            .map(|s| shell_substitute(&shell_substitute(s, &path_str), &stdout)),
                    }
                } else {
                    Preprocessed {
                        kind: PreprocessedKind::Piped(Cursor::new(lessopen_stdout)),
                        lessclose: self
                            .lessclose
                            .as_ref()
                            .map(|s| shell_substitute(&shell_substitute(s, &path_str), "-")),
                    }
                },
            ))?,
            metadata: input.metadata,
            description: input.description,
        })
    }
```


---

### 🔹 Commit #12: `c3df0e6a`
- **完整 Hash**: `c3df0e6a883f128974e4ccb7d71555cf4166045b`
- **說明 (Ground Truth)**: Fixed a bug with hardcoded terminal probing when `--list-themes` is called
- **變更檔案數**: 2

#### 📄 檔案: `src/bin/bat/app.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:212, E:246, A:0) ➔ After(N:212, E:246, A:0)
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

### 🔹 函式: `App::theme_options()`
- **變更前簽章 (Before)**: `fn App::theme_options(&self)` (L648~L650)
- **變更後簽章 (After)**: `fn App::theme_options(&self)` (L648~L650)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn theme_options(&self) -> ThemeOptions {
        Self::theme_options_from_matches(&self.matches)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn theme_options(&self) -> ThemeOptions {
        Self::theme_options_from_matches(&self.matches)
    }
```


#### 📄 檔案: `src/bin/bat/main.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:166, E:178, A:1) ➔ After(N:166, E:178, A:1)
- **差分統計**: +Nodes: 3, -Nodes: 3, +Edges: 3, -Edges: 3, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#CLI: main** `(CLI Entry)`
    └── ⚡ **run()**
        └── 🎯 [TRIGGERS] `main()`
            └── 🎯 [CALLS] `default_error_handler (External/Unresolved)()`
            └── 🎯 [CALLS] `process::exit (External/Unresolved)()`
            └── 🎯 [CALLS] `std::io::stderr (External/Unresolved)()`
            └── 🎯 [CALLS] `stderr.lock (External/Unresolved)()`
            └── 🎯 [CALLS] `run()`
-               └── [CALLS] `DetectColorScheme::default (External/Unresolved)()` [已拆除]
+               └── 🟢 [CALLS] `app.theme_options (External/Unresolved)()` [新增因果]
                └── 🎯 [CALLS] `App::new (External/Unresolved)()`
                └── 🎯 [CALLS] `Default::default (External/Unresolved)()`
                └── 🎯 [CALLS] `Ok (External/Unresolved)()`
                └── 🎯 [CALLS] `PROJECT_DIRS.cache_dir (External/Unresolved)()`
                └── 🎯 [CALLS] `PROJECT_DIRS.config_dir (External/Unresolved)()`
                └── 🎯 [CALLS] `StyleComponent::Plain.components (External/Unresolved)()`
                └── 🎯 [CALLS] `StyleComponents::new (External/Unresolved)()`
                └── 🎯 [CALLS] `app.config (External/Unresolved)()`
                └── 🎯 [CALLS] `app.inputs (External/Unresolved)()`
                └── 🎯 [CALLS] `app.matches.get_flag (External/Unresolved)()`
                └── 🎯 [CALLS] `app.matches.get_one::<String> (External/Unresolved)()`
                └── 🎯 [CALLS] `app.matches.subcommand (External/Unresolved)()`
                └── 🎯 [CALLS] `cache_matches.args_present (External/Unresolved)()`
                └── 🎯 [CALLS] `generate_config_file (External/Unresolved)()`
                └── 🎯 [CALLS] `println! (Macro)()`
                └── 🎯 [CALLS] `shell.as_str (External/Unresolved)()`
                └── 🎯 [CALLS] `unreachable! (Macro)()`
                └── 🎯 [CALLS] `vec! (Macro)()`
                └── 🎯 [CALLS] `writeln! (Macro)()`
                └── 🎯 [CALLS] `get_languages()`
                    └── 🎯 [CALLS] `Green.normal (External/Unresolved)()`
                    └── *ref:`Ok (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `Path::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `Path::new("test").with_extension (External/Unresolved)()`
                    └── 🎯 [CALLS] `Path::new(extension).extension (External/Unresolved)()`
                    └── 🎯 [CALLS] `Path::new(extension).extension().is_some (External/Unresolved)()`
                    └── 🎯 [CALLS] `String::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `Style::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `additional_paths.iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `additional_paths.iter().cloned (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter()
        .filter (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter()
        .filter(|syntax| !syntax.hidden && !syntax.file_extensions.is_empty())
        .cloned (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter()
        .filter(|syntax| !syntax.hidden && !syntax.file_extensions.is_empty())
        .cloned()
        .collect::<Vec<_>> (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets.get_syntax_for_path (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets_from_cache_or_binary (External/Unresolved)()`
                    └── 🎯 [CALLS] `comma_separator.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `config.syntax_mapping.all_mappings (External/Unresolved)()`
                    └── 🎯 [CALLS] `configured_languages.get (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.next (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.peek (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.peek().is_some (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.starts_with (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions
                .extend (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions.iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions.iter().peekable (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions.retain (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.name.as_str (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.name.clone (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.name.to_uppercase (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter()
            .map (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter()
            .map(|syntax| syntax.name.len())
            .max (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter()
            .map(|syntax| syntax.name.len())
            .max()
            .unwrap_or (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages.sort_by_key (External/Unresolved)()`
                    └── 🎯 [CALLS] `matches! (Macro)()`
                    └── 🎯 [CALLS] `separator.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `syntax.file_extensions.is_empty (External/Unresolved)()`
                    └── 🎯 [CALLS] `syntax.name.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `word.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `write! (Macro)()`
                    └── 🎯 [CALLS] `write!(result, "\n{:width$}{separator}", "", width = longest).ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `write!(result, "{:width$}{separator}", lang.name, width = longest).ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `write!(result, "{}", style.paint(&word[..])).ok (External/Unresolved)()`
                    └── *ref:`writeln! (Macro)` [已折疊指針]
                    └── 🎯 [CALLS] `writeln!(result, "{}:{}", lang.name, lang.file_extensions.join(",")).ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `get_syntax_mapping_to_paths()`
                        └── 🎯 [CALLS] `HashMap::new (External/Unresolved)()`
                        └── 🎯 [CALLS] `globs.push (External/Unresolved)()`
                        └── 🎯 [CALLS] `map.entry (External/Unresolved)()`
                        └── 🎯 [CALLS] `map.entry(*s).or_insert_with (External/Unresolved)()`
                        └── 🎯 [CALLS] `matcher.glob (External/Unresolved)()`
                        └── 🎯 [CALLS] `matcher.glob().glob (External/Unresolved)()`
                        └── 🎯 [CALLS] `matcher.glob().glob().into (External/Unresolved)()`
                └── 🎯 [CALLS] `invoke_bugreport()`
                    └── 🎯 [CALLS] `"less".to_owned (External/Unresolved)()`
                    └── 🎯 [CALLS] `CommandLine::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `CommandOutput::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `CompileTimeInformation::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `DirectoryEntries::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `EnvironmentVariables::list (External/Unresolved)()`
                    └── 🎯 [CALLS] `FileContent::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `OperatingSystem::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `SoftwareVersion::default (External/Unresolved)()`
                    └── *ref:`app.matches.get_one::<String> (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `app.matches.get_one::<String>("pager").map (External/Unresolved)()`
                    └── 🎯 [CALLS] `bat::config::get_pager_executable (External/Unresolved)()`
                    └── 🎯 [CALLS] `bat::config::get_pager_executable(
        app.matches.get_one::<String>("pager").map(|s| s.as_str()),
    )
    .unwrap_or_else (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport! (Macro)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `cache_dir.to_path_buf (External/Unresolved)()`
                    └── 🎯 [CALLS] `config_file (External/Unresolved)()`
                    └── 🎯 [CALLS] `custom_assets_metadata.push (External/Unresolved)()`
                    └── 🎯 [CALLS] `grep_cli::resolve_binary (External/Unresolved)()`
                    └── 🎯 [CALLS] `report.info (External/Unresolved)()`
                    └── 🎯 [CALLS] `report.print::<Markdown> (External/Unresolved)()`
                    └── 🎯 [CALLS] `s.as_str (External/Unresolved)()`
                    └── 🎯 [CALLS] `system_config_file (External/Unresolved)()`
                └── 🎯 [CALLS] `list_themes()`
-                   └── [CALLS] `color_scheme (External/Unresolved)()` [已拆除]
-                   └── [CALLS] `color_scheme(detect_color_scheme).unwrap_or_default (External/Unresolved)()` [已拆除]
+                   └── 🟢 [CALLS] `theme (External/Unresolved)()` [新增因果]
+                   └── 🟢 [CALLS] `theme(theme_options).to_string (External/Unresolved)()` [新增因果]
                    └── 🎯 [CALLS] `Controller::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `Controller::new(&config, &assets)
                .run(vec![theme_preview_file()], Some(&mut handle))
                .ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `HashSet::new (External/Unresolved)()`
                    └── *ref:`Ok (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `OutputHandle::FmtWrite (External/Unresolved)()`
                    └── 🎯 [CALLS] `OutputType::from_mode (External/Unresolved)()`
                    └── 🎯 [CALLS] `Some (External/Unresolved)()`
                    └── *ref:`String::new (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `StyleComponents (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets.themes (External/Unresolved)()`
                    └── *ref:`assets_from_cache_or_binary (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `cfg.clone (External/Unresolved)()`
                    └── 🎯 [CALLS] `default_theme (External/Unresolved)()`
                    └── 🎯 [CALLS] `format_args! (Macro)()`
                    └── 🎯 [CALLS] `handle.write_fmt (External/Unresolved)()`
                    └── 🎯 [CALLS] `output_type.handle (External/Unresolved)()`
                    └── 🎯 [CALLS] `style.insert (External/Unresolved)()`
                    └── 🎯 [CALLS] `theme.to_string (External/Unresolved)()`
                    └── *ref:`vec! (Macro)` [已折疊指針]
                    └── 🎯 [CALLS] `writer.write_fmt (External/Unresolved)()`
                    └── *ref:`run` [已折疊指針]
                └── 🎯 [CALLS] `run_cache_subcommand()`
                    └── 🎯 [CALLS] `build_assets()`
                        └── 🎯 [CALLS] `bat::assets::build (External/Unresolved)()`
                        └── 🎯 [CALLS] `clap::crate_version! (Macro)()`
                        └── 🎯 [CALLS] `matches
        .get_one::<String> (External/Unresolved)()`
                        └── 🎯 [CALLS] `matches
        .get_one::<String>("source")
        .map (External/Unresolved)()`
                        └── 🎯 [CALLS] `matches
        .get_one::<String>("source")
        .map(Path::new)
        .unwrap_or_else (External/Unresolved)()`
                        └── 🎯 [CALLS] `matches.get_flag (External/Unresolved)()`
                    └── *ref:`Ok (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `clear_assets (External/Unresolved)()`
                    └── *ref:`matches
        .get_one::<String> (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `matches
        .get_one::<String>("target")
        .map (External/Unresolved)()`
                    └── 🎯 [CALLS] `matches
        .get_one::<String>("target")
        .map(Path::new)
        .unwrap_or_else (External/Unresolved)()`
                    └── *ref:`matches.get_flag (External/Unresolved)` [已折疊指針]
                    └── *ref:`println! (Macro)` [已折疊指針]
                └── 🎯 [CALLS] `run_controller()`
                    └── *ref:`Controller::new (External/Unresolved)` [已折疊指針]
                    └── *ref:`assets_from_cache_or_binary (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `get_new_terminal_title()`
                        └── 🎯 [CALLS] `ColorSchemeCollector::description()`
                        └── 🎯 [CALLS] `"bat: ".to_string (External/Unresolved)()`
                        └── 🎯 [CALLS] `input.description().title (External/Unresolved)()`
                        └── 🎯 [CALLS] `inputs.iter (External/Unresolved)()`
                        └── 🎯 [CALLS] `inputs.iter().enumerate (External/Unresolved)()`
                        └── 🎯 [CALLS] `inputs.len (External/Unresolved)()`
                    └── *ref:`run` [已折疊指針]
                    └── 🎯 [CALLS] `set_terminal_title_to()`
                        └── 🎯 [CALLS] `io::stdout (External/Unresolved)()`
                        └── 🎯 [CALLS] `io::stdout().flush (External/Unresolved)()`
                        └── 🎯 [CALLS] `io::stdout().flush().unwrap (External/Unresolved)()`
                        └── 🎯 [CALLS] `print! (Macro)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `theme(theme_options).to_string (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `theme (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.theme_options (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `DetectColorScheme::default (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `color_scheme(detect_color_scheme).unwrap_or_default (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `color_scheme (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `list_themes` ──[CALLS]──> `theme(theme_options).to_string (External/Unresolved)`
  • + [新增呼叫邊] `list_themes` ──[CALLS]──> `theme (External/Unresolved)`
  • + [新增呼叫邊] `run` ──[CALLS]──> `app.theme_options (External/Unresolved)`
  • - [移除呼叫邊] `list_themes` ──[CALLS]──> `color_scheme(detect_color_scheme).unwrap_or_default (External/Unresolved)`
  • - [移除呼叫邊] `list_themes` ──[CALLS]──> `color_scheme (External/Unresolved)`
  • - [移除呼叫邊] `run` ──[CALLS]──> `DetectColorScheme::default (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `run()`
- **變更前簽章 (Before)**: `fn run()` (L370~L451)
- **變更後簽章 (After)**: `fn run()` (L369~L450)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn run() -> Result<bool> {
    let app = App::new()?;
    let config_dir = PROJECT_DIRS.config_dir();
    let cache_dir = PROJECT_DIRS.cache_dir();

    if app.matches.get_flag("diagnostic") {
        #[cfg(feature = "bugreport")]
        invoke_bugreport(&app, cache_dir);
        #[cfg(not(feature = "bugreport"))]
        println!("bat has been built without the 'bugreport' feature. The '--diagnostic' option is not available.");
        return Ok(true);
    }

    #[cfg(feature = "application")]
    if let Some(shell) = app.matches.get_one::<String>("completion") {
        match shell.as_str() {
            "bash" => println!("{}", completions::BASH_COMPLETION),
            "fish" => println!("{}", completions::FISH_COMPLETION),
            "ps1" => println!("{}", completions::PS1_COMPLETION),
            "zsh" => println!("{}", completions::ZSH_COMPLETION),
            _ => unreachable!("No completion for shell '{shell}' available."),
        }
        return Ok(true);
    }

    match app.matches.subcommand() {
        Some(("cache", cache_matches)) => {
            // If there is a file named 'cache' in the current working directory,
            // arguments for subcommand 'cache' are not mandatory.
            // If there are non-zero arguments, execute the subcommand cache, else, open the file cache.
            if cache_matches.args_present() {
                run_cache_subcommand(
                    cache_matches,
                    #[cfg(feature = "build-assets")]
                    config_dir,
                    cache_dir,
                )?;
                Ok(true)
            } else {
                let inputs = vec![Input::ordinary_file("cache")];
                let config = app.config(&inputs)?;

                run_controller(inputs, &config, cache_dir)
            }
        }
        _ => {
            let inputs = app.inputs()?;
            let config = app.config(&inputs)?;

            if app.matches.get_flag("list-languages") {
                let languages: String = get_languages(&config, cache_dir)?;
                let inputs: Vec<Input> = vec![Input::from_reader(Box::new(languages.as_bytes()))];
                let plain_config = Config {
                    style_components: StyleComponents::new(StyleComponent::Plain.components(false)),
                    paging_mode: PagingMode::QuitIfOneScreen,
                    ..Default::default()
                };
                run_controller(inputs, &plain_config, cache_dir)
            } else if app.matches.get_flag("list-themes") {
                list_themes(&config, config_dir, cache_dir, DetectColorScheme::default())?;
                Ok(true)
            } else if app.matches.get_flag("config-file") {
                println!("{}", config_file().to_string_lossy());
                Ok(true)
            } else if app.matches.get_flag("generate-config-file") {
                generate_config_file()?;
                Ok(true)
            } else if app.matches.get_flag("config-dir") {
                writeln!(io::stdout(), "{}", config_dir.to_string_lossy())?;
                Ok(true)
            } else if app.matches.get_flag("cache-dir") {
                writeln!(io::stdout(), "{}", cache_dir.to_string_lossy())?;
                Ok(true)
            } else if app.matches.get_flag("acknowledgements") {
                writeln!(io::stdout(), "{}", bat::assets::get_acknowledgements())?;
                Ok(true)
            } else {
                run_controller(inputs, &config, cache_dir)
            }
        }
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn run() -> Result<bool> {
    let app = App::new()?;
    let config_dir = PROJECT_DIRS.config_dir();
    let cache_dir = PROJECT_DIRS.cache_dir();

    if app.matches.get_flag("diagnostic") {
        #[cfg(feature = "bugreport")]
        invoke_bugreport(&app, cache_dir);
        #[cfg(not(feature = "bugreport"))]
        println!("bat has been built without the 'bugreport' feature. The '--diagnostic' option is not available.");
        return Ok(true);
    }

    #[cfg(feature = "application")]
    if let Some(shell) = app.matches.get_one::<String>("completion") {
        match shell.as_str() {
            "bash" => println!("{}", completions::BASH_COMPLETION),
            "fish" => println!("{}", completions::FISH_COMPLETION),
            "ps1" => println!("{}", completions::PS1_COMPLETION),
            "zsh" => println!("{}", completions::ZSH_COMPLETION),
            _ => unreachable!("No completion for shell '{shell}' available."),
        }
        return Ok(true);
    }

    match app.matches.subcommand() {
        Some(("cache", cache_matches)) => {
            // If there is a file named 'cache' in the current working directory,
            // arguments for subcommand 'cache' are not mandatory.
            // If there are non-zero arguments, execute the subcommand cache, else, open the file cache.
            if cache_matches.args_present() {
                run_cache_subcommand(
                    cache_matches,
                    #[cfg(feature = "build-assets")]
                    config_dir,
                    cache_dir,
                )?;
                Ok(true)
            } else {
                let inputs = vec![Input::ordinary_file("cache")];
                let config = app.config(&inputs)?;

                run_controller(inputs, &config, cache_dir)
            }
        }
        _ => {
            let inputs = app.inputs()?;
            let config = app.config(&inputs)?;

            if app.matches.get_flag("list-languages") {
                let languages: String = get_languages(&config, cache_dir)?;
                let inputs: Vec<Input> = vec![Input::from_reader(Box::new(languages.as_bytes()))];
                let plain_config = Config {
                    style_components: StyleComponents::new(StyleComponent::Plain.components(false)),
                    paging_mode: PagingMode::QuitIfOneScreen,
                    ..Default::default()
                };
                run_controller(inputs, &plain_config, cache_dir)
            } else if app.matches.get_flag("list-themes") {
                list_themes(&config, config_dir, cache_dir, app.theme_options())?;
                Ok(true)
            } else if app.matches.get_flag("config-file") {
                println!("{}", config_file().to_string_lossy());
                Ok(true)
            } else if app.matches.get_flag("generate-config-file") {
                generate_config_file()?;
                Ok(true)
            } else if app.matches.get_flag("config-dir") {
                writeln!(io::stdout(), "{}", config_dir.to_string_lossy())?;
                Ok(true)
            } else if app.matches.get_flag("cache-dir") {
                writeln!(io::stdout(), "{}", cache_dir.to_string_lossy())?;
                Ok(true)
            } else if app.matches.get_flag("acknowledgements") {
                writeln!(io::stdout(), "{}", bat::assets::get_acknowledgements())?;
                Ok(true)
            } else {
                run_controller(inputs, &config, cache_dir)
            }
        }
    }
}
```

### 🔹 函式: `list_themes()`
- **變更前簽章 (Before)**: `fn list_themes(
    cfg: &Config,
    config_dir: &Path,
    cache_dir: &Path,
    detect_color_scheme: DetectColorScheme,
)` (L196~L257)
- **變更後簽章 (After)**: `fn list_themes(
    cfg: &Config,
    config_dir: &Path,
    cache_dir: &Path,
    theme_options: ThemeOptions,
)` (L195~L256)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn list_themes(
    cfg: &Config,
    config_dir: &Path,
    cache_dir: &Path,
    detect_color_scheme: DetectColorScheme,
) -> Result<()> {
    let assets = assets_from_cache_or_binary(cfg.use_custom_assets, cache_dir)?;
    let mut config = cfg.clone();
    let mut style = HashSet::new();
    style.insert(StyleComponent::Plain);
    config.language = Some("Rust");
    config.style_components = StyleComponents(style);

    let default_theme_name = default_theme(color_scheme(detect_color_scheme).unwrap_or_default());
    let mut buf = String::new();
    let mut handle = OutputHandle::FmtWrite(&mut buf);

    for theme in assets.themes() {
        let default_theme_info = if default_theme_name == theme {
            " (default)"
        } else if default_theme(ColorScheme::Dark) == theme {
            " (default dark)"
        } else if default_theme(ColorScheme::Light) == theme {
            " (default light)"
        } else {
            ""
        };

        if config.colored_output {
            handle.write_fmt(format_args!(
                "{}{default_theme_info}\n\n",
                Style::new().bold().paint(theme.to_string()),
            ))?;
            config.theme = theme.to_string();
            Controller::new(&config, &assets)
                .run(vec![theme_preview_file()], Some(&mut handle))
                .ok();
            handle.write_fmt(format_args!("\n"))?;
        } else if config.loop_through {
            handle.write_fmt(format_args!("{theme}\n"))?;
        } else {
            handle.write_fmt(format_args!("{theme}{default_theme_info}\n"))?;
        }
    }

    if config.colored_output {
        handle.write_fmt(format_args!(
            "Further themes can be installed to '{}', \
            and are added to the cache with `bat cache --build`. \
            For more information, see:\n\n  \
            https://github.com/sharkdp/bat#adding-new-themes",
            config_dir.join("themes").to_string_lossy()
        ))?;
    }

    let mut output_type =
        OutputType::from_mode(config.paging_mode, config.wrapping_mode, config.pager)?;
    let mut writer = output_type.handle()?;
    writer.write_fmt(format_args!("{buf}"))?;

    Ok(())
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn list_themes(
    cfg: &Config,
    config_dir: &Path,
    cache_dir: &Path,
    theme_options: ThemeOptions,
) -> Result<()> {
    let assets = assets_from_cache_or_binary(cfg.use_custom_assets, cache_dir)?;
    let mut config = cfg.clone();
    let mut style = HashSet::new();
    style.insert(StyleComponent::Plain);
    config.language = Some("Rust");
    config.style_components = StyleComponents(style);

    let default_theme_name = theme(theme_options).to_string();
    let mut buf = String::new();
    let mut handle = OutputHandle::FmtWrite(&mut buf);

    for theme in assets.themes() {
        let default_theme_info = if default_theme_name == theme {
            " (default)"
        } else if default_theme(ColorScheme::Dark) == theme {
            " (default dark)"
        } else if default_theme(ColorScheme::Light) == theme {
            " (default light)"
        } else {
            ""
        };

        if config.colored_output {
            handle.write_fmt(format_args!(
                "{}{default_theme_info}\n\n",
                Style::new().bold().paint(theme.to_string()),
            ))?;
            config.theme = theme.to_string();
            Controller::new(&config, &assets)
                .run(vec![theme_preview_file()], Some(&mut handle))
                .ok();
            handle.write_fmt(format_args!("\n"))?;
        } else if config.loop_through {
            handle.write_fmt(format_args!("{theme}\n"))?;
        } else {
            handle.write_fmt(format_args!("{theme}{default_theme_info}\n"))?;
        }
    }

    if config.colored_output {
        handle.write_fmt(format_args!(
            "Further themes can be installed to '{}', \
            and are added to the cache with `bat cache --build`. \
            For more information, see:\n\n  \
            https://github.com/sharkdp/bat#adding-new-themes",
            config_dir.join("themes").to_string_lossy()
        ))?;
    }

    let mut output_type =
        OutputType::from_mode(config.paging_mode, config.wrapping_mode, config.pager)?;
    let mut writer = output_type.handle()?;
    writer.write_fmt(format_args!("{buf}"))?;

    Ok(())
}
```


---

### 🔹 Commit #13: `a9137fab`
- **完整 Hash**: `a9137fab05f8204804c5cfecf480f4c8f2d7ab82`
- **說明 (Ground Truth)**: Support BAT_WIDTH as an alias for --terminal-width
- **變更檔案數**: 3

#### 📄 檔案: `src/bin/bat/clap_app.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:427, E:425, A:0) ➔ After(N:429, E:427, A:0)
- **差分統計**: +Nodes: 30, -Nodes: 28, +Edges: 30, -Edges: 28, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg(
            Arg::new("decorations")
                .long("decorations")
                .overrides_with("decorations")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("When to show the decorations (*auto*, never, always).")
                .long_help(
                    "Specify when to use the decorations that have been specified \
                    via '--style'. The automatic mode only enables decorations if \
                    an interactive terminal is detected. The always mode will show \
                    decorations even when piping output. Possible values: *auto*, never, always.",
                )
        )
        .arg(
            Arg::new("force-colorization")
                .long("force-colorization")
                .short('f')
                .action(ArgAction::SetTrue)
                .conflicts_with("color")
                .conflicts_with("decorations")
                .overrides_with("force-colorization")
                .hide_short_help(true)
                .long_help("Alias for '--decorations=always --color=always'. This is useful \
                        if the output of bat is piped to another program, but you want \
                        to keep the colorization/decorations.")
        )
        .arg(
            Arg::new("paging")
                .long("paging")
                .overrides_with("paging")
                .overrides_with("no-paging")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify when to use the pager, or use `-P` to disable (*auto*, never, always).")
                .long_help(
                    "Specify when to use the pager. To disable the pager, use \
                    '--paging=never' or its alias,'-P'. To disable the pager permanently, \
                    set BAT_PAGING to 'never'. To control which pager is used, see the \
                    '--pager' option. Possible values: *auto*, never, always."
                ),
        )
        .arg(
            Arg::new("no-paging")
                .short('P')
                .long("no-paging")
                .alias("no-pager")
                .action(ArgAction::SetTrue)
                .overrides_with("no-paging")
                .hide(true)
                .hide_short_help(true)
                .help("Alias for '--paging=never'")
            )
        .arg(
            Arg::new("pager")
                .long("pager")
                .overrides_with("pager")
                .value_name("command")
                .hide_short_help(true)
                .help("Determine which pager to use.")
                .long_help(
                    "Determine which pager is used. This option will override the \
                    PAGER and BAT_PAGER environment variables. The default pager is 'less'. \
                    If you provide '--pager=builtin', use the built-in 'minus' pager. \
                    To control when the pager is used, see the '--paging' option. \
                    Example: '--pager \"less -RF\"'."
                ),
        )
        .arg(
            Arg::new("map-syntax")
                .short('m')
                .long("map-syntax")
                .action(ArgAction::Append)
                .value_name("glob:syntax")
                .help("Use the specified syntax for files matching the glob pattern ('*.cpp:C++').")
                .long_help(
                    "Map a glob pattern to an existing syntax name. The glob pattern is matched \
                     on the full path and the filename. For example, to highlight *.build files \
                     with the Python syntax, use -m '*.build:Python'. To highlight files named \
                     '.myignore' with the Git Ignore syntax, use -m '.myignore:Git Ignore'. Note \
                     that the right-hand side is the *name* of the syntax, not a file extension.",
                )
        )
        .arg(
            Arg::new("ignored-suffix")
                .action(ArgAction::Append)
                .long("ignored-suffix")
                .hide_short_help(true)
                .help(
                    "Ignore extension. For example:\n  \
                    'bat --ignored-suffix \".dev\" my_file.json.dev' will use JSON syntax, and ignore '.dev'"
                )
        )
        .arg(
            Arg::new("theme")
                .long("theme")
                .overrides_with("theme")
                .help("Set the color theme for syntax highlighting.")
                .long_help(
                    "Set the theme for syntax highlighting. Use '--list-themes' to \
                     see all available themes. To set a default theme, add the \
                     '--theme=\"...\"' option to the configuration file or export the \
                     BAT_THEME environment variable (e.g.: export \
                     BAT_THEME=\"...\").\n\n\
                     Special values:\n\n  \
                     * auto: Picks a dark or light theme depending on the terminal's colors (default).\n          \
                     Use '--theme-light' and '--theme-dark' to customize the selected theme.\n    \
                     * auto:always: Detect the terminal's colors even when the output is redirected.\n    \
                     * auto:system: Detect the color scheme from the system-wide preference (macOS only).\n  \
                     * dark: Use the dark theme specified by '--theme-dark'.\n  \
                     * light: Use the light theme specified by '--theme-light'.",
                ),
        )
        .arg(
            Arg::new("theme-light")
                .long("theme-light")
                .overrides_with("theme-light")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for light backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a light background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-light=\"...\" option to the configuration file or export the BAT_THEME_LIGHT \
                    environment variable (e.g. export BAT_THEME_LIGHT=\"...\")."),
        )
        .arg(
            Arg::new("theme-dark")
                .long("theme-dark")
                .overrides_with("theme-dark")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for dark backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a dark background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-dark=\"...\" option to the configuration file or export the BAT_THEME_DARK \
                    environment variable (e.g. export BAT_THEME_DARK=\"...\")."),
        )
        .arg(
            Arg::new("list-themes")
                .long("list-themes")
                .action(ArgAction::SetTrue)
                .help("Display all supported highlighting themes.")
                .long_help("Display a list of supported themes for syntax highlighting."),
        )
        .arg(
            Arg::new("squeeze-blank")
                .long("squeeze-blank")
                .short('s')
                .action(ArgAction::SetTrue)
                .help("Squeeze consecutive empty lines.")
                .long_help("Squeeze consecutive empty lines into a single empty line.")
        )
        .arg(
            Arg::new("squeeze-limit")
                .long("squeeze-limit")
                .value_parser(|s: &str| s.parse::<usize>().map_err(|_| "Requires a non-negative number".to_owned()))
                .long_help("Set the maximum number of consecutive empty lines to be printed.")
                .hide_short_help(true)
        )
        .arg(
            Arg::new("strip-ansi")
                .long("strip-ansi")
                .overrides_with("strip-ansi")
                .value_name("when")
                .value_parser(["auto", "always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Strip colors from the input (auto, always, *never*)")
                .long_help("Specify when to strip ANSI escape sequences from the input. \
                The automatic mode will remove escape sequences unless the syntax highlighting \
                language is plain text. Possible values: auto, always, *never*.")
                .hide_short_help(true)
        )
        .arg(
            Arg::new("style")
                .long("style")
                .action(ArgAction::Append)
                .value_name("components")
                // Cannot use claps built in validation because we have to turn off clap's delimiters
                .value_parser(|val: &str| {
                    match StyleComponentList::from_str(val) {
                        Err(err) => Err(err),
                        Ok(_) => Ok(val.to_owned()),
                    }
                })
                .help(
                    "Comma-separated list of style elements to display \
                     (*default*, auto, full, plain, changes, header, header-filename, header-filesize, grid, rule, numbers, snip).",
                )
                .long_help(
                    "Configure which elements (line numbers, file headers, grid \
                     borders, Git modifications, ..) to display in addition to the \
                     file contents. The argument is a comma-separated list of \
                     components to display (e.g. 'numbers,changes,grid') or a \
                     pre-defined style ('full'). To set a default style, add the \
                     '--style=\"..\"' option to the configuration file or export the \
                     BAT_STYLE environment variable (e.g.: export BAT_STYLE=\"..\").\n\n\
                     When styles are specified in multiple places, the \"nearest\" set \
                     of styles take precedence. The command-line arguments are the highest \
                     priority, followed by the BAT_STYLE environment variable, and then \
                     the configuration file. If any set of styles consists entirely of \
                     components prefixed with \"+\" or \"-\", it will modify the \
                     previous set of styles instead of replacing them.\n\n\
                     By default, the following components are enabled:\n  \
                        changes, grid, header-filename, numbers, snip\n\n\
                     Possible values:\n\n  \
                     * default: enables recommended style components (default).\n  \
                     * full: enables all available components.\n  \
                     * auto: same as 'default', unless the output is piped.\n  \
                     * plain: disables all available components.\n  \
                     * changes: show Git modification markers.\n  \
                     * header: alias for 'header-filename'.\n  \
                     * header-filename: show filenames before the content.\n  \
                     * header-filesize: show file sizes before the content.\n  \
                     * grid: vertical/horizontal lines to separate side bar\n          \
                       and the header from the content.\n  \
                     * rule: horizontal lines to delimit files.\n  \
                     * numbers: show line numbers in the side bar.\n  \
                     * snip: draw separation lines between distinct line ranges.",
                ),
        )
        .arg(
            Arg::new("line-range")
                .long("line-range")
                .short('r')
                .action(ArgAction::Append)
                .value_name("N:M")
                .allow_hyphen_values(true)
                .help("Only print the lines from N to M.")
                .long_help(
                    "Only print the specified range of lines for each file. \
                     For example:\n  \
                     '--line-range 30:40' prints lines 30 to 40\n  \
                     '--line-range :40' prints lines 1 to 40\n  \
                     '--line-range 40:' prints lines 40 to the end of the file\n  \
                     '--line-range 40' only prints line 40\n  \
                     '--line-range -10:' prints the last 10 lines\n  \
                     '--line-range 30:+10' prints lines 30 to 40\n  \
                     '--line-range 35::5' prints lines 30 to 40 (line 35 with 5 lines of context)\n  \
                     '--line-range 30:40:2' prints lines 28 to 42 (range 30-40 with 2 lines of context)",
                ),
        )
        .arg(
            Arg::new("list-languages")
                .long("list-languages")
                .short('L')
                .action(ArgAction::SetTrue)
                .conflicts_with("list-themes")
                .help("Display all supported languages.")
                .long_help("Display a list of supported languages for syntax highlighting."),
        )
        .arg(
            Arg::new("unbuffered")
                .short('u')
                .long("unbuffered")
                .action(ArgAction::SetTrue)
                .help("Enable unbuffered input reading for streaming use cases.")
                .long_help(
                    "Enable unbuffered input reading. When this flag is set, bat will \
                     display data as soon as it is available, without waiting for a \
                     complete line. This is useful for streaming use cases like \
                     'tail -f logfile | bat -u --paging=never'. Note that line numbers \
                     are automatically disabled in unbuffered mode, and syntax \
                     highlighting may be imperfect on partial lines.",
                ),
        )
        .arg(
            Arg::new("no-config")
                .long("no-config")
                .action(ArgAction::SetTrue)
                .hide(true)
                .help("Do not use the configuration file"),
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg(
            Arg::new("decorations")
                .long("decorations")
                .overrides_with("decorations")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("When to show the decorations (*auto*, never, always).")
                .long_help(
                    "Specify when to use the decorations that have been specified \
                    via '--style'. The automatic mode only enables decorations if \
                    an interactive terminal is detected. The always mode will show \
                    decorations even when piping output. Possible values: *auto*, never, always.",
                )
        )
        .arg(
            Arg::new("force-colorization")
                .long("force-colorization")
                .short('f')
                .action(ArgAction::SetTrue)
                .conflicts_with("color")
                .conflicts_with("decorations")
                .overrides_with("force-colorization")
                .hide_short_help(true)
                .long_help("Alias for '--decorations=always --color=always'. This is useful \
                        if the output of bat is piped to another program, but you want \
                        to keep the colorization/decorations.")
        )
        .arg(
            Arg::new("paging")
                .long("paging")
                .overrides_with("paging")
                .overrides_with("no-paging")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify when to use the pager, or use `-P` to disable (*auto*, never, always).")
                .long_help(
                    "Specify when to use the pager. To disable the pager, use \
                    '--paging=never' or its alias,'-P'. To disable the pager permanently, \
                    set BAT_PAGING to 'never'. To control which pager is used, see the \
                    '--pager' option. Possible values: *auto*, never, always."
                ),
        )
        .arg(
            Arg::new("no-paging")
                .short('P')
                .long("no-paging")
                .alias("no-pager")
                .action(ArgAction::SetTrue)
                .overrides_with("no-paging")
                .hide(true)
                .hide_short_help(true)
                .help("Alias for '--paging=never'")
            )
        .arg(
            Arg::new("pager")
                .long("pager")
                .overrides_with("pager")
                .value_name("command")
                .hide_short_help(true)
                .help("Determine which pager to use.")
                .long_help(
                    "Determine which pager is used. This option will override the \
                    PAGER and BAT_PAGER environment variables. The default pager is 'less'. \
                    If you provide '--pager=builtin', use the built-in 'minus' pager. \
                    To control when the pager is used, see the '--paging' option. \
                    Example: '--pager \"less -RF\"'."
                ),
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg(
            Arg::new("decorations")
                .long("decorations")
                .overrides_with("decorations")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("When to show the decorations (*auto*, never, always).")
                .long_help(
                    "Specify when to use the decorations that have been specified \
                    via '--style'. The automatic mode only enables decorations if \
                    an interactive terminal is detected. The always mode will show \
                    decorations even when piping output. Possible values: *auto*, never, always.",
                )
        )
        .arg(
            Arg::new("force-colorization")
                .long("force-colorization")
                .short('f')
                .action(ArgAction::SetTrue)
                .conflicts_with("color")
                .conflicts_with("decorations")
                .overrides_with("force-colorization")
                .hide_short_help(true)
                .long_help("Alias for '--decorations=always --color=always'. This is useful \
                        if the output of bat is piped to another program, but you want \
                        to keep the colorization/decorations.")
        )
        .arg(
            Arg::new("paging")
                .long("paging")
                .overrides_with("paging")
                .overrides_with("no-paging")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify when to use the pager, or use `-P` to disable (*auto*, never, always).")
                .long_help(
                    "Specify when to use the pager. To disable the pager, use \
                    '--paging=never' or its alias,'-P'. To disable the pager permanently, \
                    set BAT_PAGING to 'never'. To control which pager is used, see the \
                    '--pager' option. Possible values: *auto*, never, always."
                ),
        )
        .arg(
            Arg::new("no-paging")
                .short('P')
                .long("no-paging")
                .alias("no-pager")
                .action(ArgAction::SetTrue)
                .overrides_with("no-paging")
                .hide(true)
                .hide_short_help(true)
                .help("Alias for '--paging=never'")
            )
        .arg(
            Arg::new("pager")
                .long("pager")
                .overrides_with("pager")
                .value_name("command")
                .hide_short_help(true)
                .help("Determine which pager to use.")
                .long_help(
                    "Determine which pager is used. This option will override the \
                    PAGER and BAT_PAGER environment variables. The default pager is 'less'. \
                    If you provide '--pager=builtin', use the built-in 'minus' pager. \
                    To control when the pager is used, see the '--paging' option. \
                    Example: '--pager \"less -RF\"'."
                ),
        )
        .arg(
            Arg::new("map-syntax")
                .short('m')
                .long("map-syntax")
                .action(ArgAction::Append)
                .value_name("glob:syntax")
                .help("Use the specified syntax for files matching the glob pattern ('*.cpp:C++').")
                .long_help(
                    "Map a glob pattern to an existing syntax name. The glob pattern is matched \
                     on the full path and the filename. For example, to highlight *.build files \
                     with the Python syntax, use -m '*.build:Python'. To highlight files named \
                     '.myignore' with the Git Ignore syntax, use -m '.myignore:Git Ignore'. Note \
                     that the right-hand side is the *name* of the syntax, not a file extension.",
                )
        )
        .arg(
            Arg::new("ignored-suffix")
                .action(ArgAction::Append)
                .long("ignored-suffix")
                .hide_short_help(true)
                .help(
                    "Ignore extension. For example:\n  \
                    'bat --ignored-suffix \".dev\" my_file.json.dev' will use JSON syntax, and ignore '.dev'"
                )
        )
        .arg(
            Arg::new("theme")
                .long("theme")
                .overrides_with("theme")
                .help("Set the color theme for syntax highlighting.")
                .long_help(
                    "Set the theme for syntax highlighting. Use '--list-themes' to \
                     see all available themes. To set a default theme, add the \
                     '--theme=\"...\"' option to the configuration file or export the \
                     BAT_THEME environment variable (e.g.: export \
                     BAT_THEME=\"...\").\n\n\
                     Special values:\n\n  \
                     * auto: Picks a dark or light theme depending on the terminal's colors (default).\n          \
                     Use '--theme-light' and '--theme-dark' to customize the selected theme.\n    \
                     * auto:always: Detect the terminal's colors even when the output is redirected.\n    \
                     * auto:system: Detect the color scheme from the system-wide preference (macOS only).\n  \
                     * dark: Use the dark theme specified by '--theme-dark'.\n  \
                     * light: Use the light theme specified by '--theme-light'.",
                ),
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg(
            Arg::new("decorations")
                .long("decorations")
                .overrides_with("decorations")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("When to show the decorations (*auto*, never, always).")
                .long_help(
                    "Specify when to use the decorations that have been specified \
                    via '--style'. The automatic mode only enables decorations if \
                    an interactive terminal is detected. The always mode will show \
                    decorations even when piping output. Possible values: *auto*, never, always.",
                )
        )
        .arg(
            Arg::new("force-colorization")
                .long("force-colorization")
                .short('f')
                .action(ArgAction::SetTrue)
                .conflicts_with("color")
                .conflicts_with("decorations")
                .overrides_with("force-colorization")
                .hide_short_help(true)
                .long_help("Alias for '--decorations=always --color=always'. This is useful \
                        if the output of bat is piped to another program, but you want \
                        to keep the colorization/decorations.")
        )
        .arg(
            Arg::new("paging")
                .long("paging")
                .overrides_with("paging")
                .overrides_with("no-paging")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify when to use the pager, or use `-P` to disable (*auto*, never, always).")
                .long_help(
                    "Specify when to use the pager. To disable the pager, use \
                    '--paging=never' or its alias,'-P'. To disable the pager permanently, \
                    set BAT_PAGING to 'never'. To control which pager is used, see the \
                    '--pager' option. Possible values: *auto*, never, always."
                ),
        )
        .arg(
            Arg::new("no-paging")
                .short('P')
                .long("no-paging")
                .alias("no-pager")
                .action(ArgAction::SetTrue)
                .overrides_with("no-paging")
                .hide(true)
                .hide_short_help(true)
                .help("Alias for '--paging=never'")
            )
        .arg(
            Arg::new("pager")
                .long("pager")
                .overrides_with("pager")
                .value_name("command")
                .hide_short_help(true)
                .help("Determine which pager to use.")
                .long_help(
                    "Determine which pager is used. This option will override the \
                    PAGER and BAT_PAGER environment variables. The default pager is 'less'. \
                    If you provide '--pager=builtin', use the built-in 'minus' pager. \
                    To control when the pager is used, see the '--paging' option. \
                    Example: '--pager \"less -RF\"'."
                ),
        )
        .arg(
            Arg::new("map-syntax")
                .short('m')
                .long("map-syntax")
                .action(ArgAction::Append)
                .value_name("glob:syntax")
                .help("Use the specified syntax for files matching the glob pattern ('*.cpp:C++').")
                .long_help(
                    "Map a glob pattern to an existing syntax name. The glob pattern is matched \
                     on the full path and the filename. For example, to highlight *.build files \
                     with the Python syntax, use -m '*.build:Python'. To highlight files named \
                     '.myignore' with the Git Ignore syntax, use -m '.myignore:Git Ignore'. Note \
                     that the right-hand side is the *name* of the syntax, not a file extension.",
                )
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg(
            Arg::new("decorations")
                .long("decorations")
                .overrides_with("decorations")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("When to show the decorations (*auto*, never, always).")
                .long_help(
                    "Specify when to use the decorations that have been specified \
                    via '--style'. The automatic mode only enables decorations if \
                    an interactive terminal is detected. The always mode will show \
                    decorations even when piping output. Possible values: *auto*, never, always.",
                )
        )
        .arg(
            Arg::new("force-colorization")
                .long("force-colorization")
                .short('f')
                .action(ArgAction::SetTrue)
                .conflicts_with("color")
                .conflicts_with("decorations")
                .overrides_with("force-colorization")
                .hide_short_help(true)
                .long_help("Alias for '--decorations=always --color=always'. This is useful \
                        if the output of bat is piped to another program, but you want \
                        to keep the colorization/decorations.")
        )
        .arg(
            Arg::new("paging")
                .long("paging")
                .overrides_with("paging")
                .overrides_with("no-paging")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify when to use the pager, or use `-P` to disable (*auto*, never, always).")
                .long_help(
                    "Specify when to use the pager. To disable the pager, use \
                    '--paging=never' or its alias,'-P'. To disable the pager permanently, \
                    set BAT_PAGING to 'never'. To control which pager is used, see the \
                    '--pager' option. Possible values: *auto*, never, always."
                ),
        )
        .arg(
            Arg::new("no-paging")
                .short('P')
                .long("no-paging")
                .alias("no-pager")
                .action(ArgAction::SetTrue)
                .overrides_with("no-paging")
                .hide(true)
                .hide_short_help(true)
                .help("Alias for '--paging=never'")
            )
        .arg(
            Arg::new("pager")
                .long("pager")
                .overrides_with("pager")
                .value_name("command")
                .hide_short_help(true)
                .help("Determine which pager to use.")
                .long_help(
                    "Determine which pager is used. This option will override the \
                    PAGER and BAT_PAGER environment variables. The default pager is 'less'. \
                    If you provide '--pager=builtin', use the built-in 'minus' pager. \
                    To control when the pager is used, see the '--paging' option. \
                    Example: '--pager \"less -RF\"'."
                ),
        )
        .arg(
            Arg::new("map-syntax")
                .short('m')
                .long("map-syntax")
                .action(ArgAction::Append)
                .value_name("glob:syntax")
                .help("Use the specified syntax for files matching the glob pattern ('*.cpp:C++').")
                .long_help(
                    "Map a glob pattern to an existing syntax name. The glob pattern is matched \
                     on the full path and the filename. For example, to highlight *.build files \
                     with the Python syntax, use -m '*.build:Python'. To highlight files named \
                     '.myignore' with the Git Ignore syntax, use -m '.myignore:Git Ignore'. Note \
                     that the right-hand side is the *name* of the syntax, not a file extension.",
                )
        )
        .arg(
            Arg::new("ignored-suffix")
                .action(ArgAction::Append)
                .long("ignored-suffix")
                .hide_short_help(true)
                .help(
                    "Ignore extension. For example:\n  \
                    'bat --ignored-suffix \".dev\" my_file.json.dev' will use JSON syntax, and ignore '.dev'"
                )
        )
        .arg(
            Arg::new("theme")
                .long("theme")
                .overrides_with("theme")
                .help("Set the color theme for syntax highlighting.")
                .long_help(
                    "Set the theme for syntax highlighting. Use '--list-themes' to \
                     see all available themes. To set a default theme, add the \
                     '--theme=\"...\"' option to the configuration file or export the \
                     BAT_THEME environment variable (e.g.: export \
                     BAT_THEME=\"...\").\n\n\
                     Special values:\n\n  \
                     * auto: Picks a dark or light theme depending on the terminal's colors (default).\n          \
                     Use '--theme-light' and '--theme-dark' to customize the selected theme.\n    \
                     * auto:always: Detect the terminal's colors even when the output is redirected.\n    \
                     * auto:system: Detect the color scheme from the system-wide preference (macOS only).\n  \
                     * dark: Use the dark theme specified by '--theme-dark'.\n  \
                     * light: Use the light theme specified by '--theme-light'.",
                ),
        )
        .arg(
            Arg::new("theme-light")
                .long("theme-light")
                .overrides_with("theme-light")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for light backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a light background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-light=\"...\" option to the configuration file or export the BAT_THEME_LIGHT \
                    environment variable (e.g. export BAT_THEME_LIGHT=\"...\")."),
        )
        .arg(
            Arg::new("theme-dark")
                .long("theme-dark")
                .overrides_with("theme-dark")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for dark backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a dark background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-dark=\"...\" option to the configuration file or export the BAT_THEME_DARK \
                    environment variable (e.g. export BAT_THEME_DARK=\"...\")."),
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg(
            Arg::new("decorations")
                .long("decorations")
                .overrides_with("decorations")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("When to show the decorations (*auto*, never, always).")
                .long_help(
                    "Specify when to use the decorations that have been specified \
                    via '--style'. The automatic mode only enables decorations if \
                    an interactive terminal is detected. The always mode will show \
                    decorations even when piping output. Possible values: *auto*, never, always.",
                )
        )
        .arg(
            Arg::new("force-colorization")
                .long("force-colorization")
                .short('f')
                .action(ArgAction::SetTrue)
                .conflicts_with("color")
                .conflicts_with("decorations")
                .overrides_with("force-colorization")
                .hide_short_help(true)
                .long_help("Alias for '--decorations=always --color=always'. This is useful \
                        if the output of bat is piped to another program, but you want \
                        to keep the colorization/decorations.")
        )
        .arg(
            Arg::new("paging")
                .long("paging")
                .overrides_with("paging")
                .overrides_with("no-paging")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify when to use the pager, or use `-P` to disable (*auto*, never, always).")
                .long_help(
                    "Specify when to use the pager. To disable the pager, use \
                    '--paging=never' or its alias,'-P'. To disable the pager permanently, \
                    set BAT_PAGING to 'never'. To control which pager is used, see the \
                    '--pager' option. Possible values: *auto*, never, always."
                ),
        )
        .arg(
            Arg::new("no-paging")
                .short('P')
                .long("no-paging")
                .alias("no-pager")
                .action(ArgAction::SetTrue)
                .overrides_with("no-paging")
                .hide(true)
                .hide_short_help(true)
                .help("Alias for '--paging=never'")
            )
        .arg(
            Arg::new("pager")
                .long("pager")
                .overrides_with("pager")
                .value_name("command")
                .hide_short_help(true)
                .help("Determine which pager to use.")
                .long_help(
                    "Determine which pager is used. This option will override the \
                    PAGER and BAT_PAGER environment variables. The default pager is 'less'. \
                    If you provide '--pager=builtin', use the built-in 'minus' pager. \
                    To control when the pager is used, see the '--paging' option. \
                    Example: '--pager \"less -RF\"'."
                ),
        )
        .arg(
            Arg::new("map-syntax")
                .short('m')
                .long("map-syntax")
                .action(ArgAction::Append)
                .value_name("glob:syntax")
                .help("Use the specified syntax for files matching the glob pattern ('*.cpp:C++').")
                .long_help(
                    "Map a glob pattern to an existing syntax name. The glob pattern is matched \
                     on the full path and the filename. For example, to highlight *.build files \
                     with the Python syntax, use -m '*.build:Python'. To highlight files named \
                     '.myignore' with the Git Ignore syntax, use -m '.myignore:Git Ignore'. Note \
                     that the right-hand side is the *name* of the syntax, not a file extension.",
                )
        )
        .arg(
            Arg::new("ignored-suffix")
                .action(ArgAction::Append)
                .long("ignored-suffix")
                .hide_short_help(true)
                .help(
                    "Ignore extension. For example:\n  \
                    'bat --ignored-suffix \".dev\" my_file.json.dev' will use JSON syntax, and ignore '.dev'"
                )
        )
        .arg(
            Arg::new("theme")
                .long("theme")
                .overrides_with("theme")
                .help("Set the color theme for syntax highlighting.")
                .long_help(
                    "Set the theme for syntax highlighting. Use '--list-themes' to \
                     see all available themes. To set a default theme, add the \
                     '--theme=\"...\"' option to the configuration file or export the \
                     BAT_THEME environment variable (e.g.: export \
                     BAT_THEME=\"...\").\n\n\
                     Special values:\n\n  \
                     * auto: Picks a dark or light theme depending on the terminal's colors (default).\n          \
                     Use '--theme-light' and '--theme-dark' to customize the selected theme.\n    \
                     * auto:always: Detect the terminal's colors even when the output is redirected.\n    \
                     * auto:system: Detect the color scheme from the system-wide preference (macOS only).\n  \
                     * dark: Use the dark theme specified by '--theme-dark'.\n  \
                     * light: Use the light theme specified by '--theme-light'.",
                ),
        )
        .arg(
            Arg::new("theme-light")
                .long("theme-light")
                .overrides_with("theme-light")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for light backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a light background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-light=\"...\" option to the configuration file or export the BAT_THEME_LIGHT \
                    environment variable (e.g. export BAT_THEME_LIGHT=\"...\")."),
        )
        .arg(
            Arg::new("theme-dark")
                .long("theme-dark")
                .overrides_with("theme-dark")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for dark backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a dark background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-dark=\"...\" option to the configuration file or export the BAT_THEME_DARK \
                    environment variable (e.g. export BAT_THEME_DARK=\"...\")."),
        )
        .arg(
            Arg::new("list-themes")
                .long("list-themes")
                .action(ArgAction::SetTrue)
                .help("Display all supported highlighting themes.")
                .long_help("Display a list of supported themes for syntax highlighting."),
        )
        .arg(
            Arg::new("squeeze-blank")
                .long("squeeze-blank")
                .short('s')
                .action(ArgAction::SetTrue)
                .help("Squeeze consecutive empty lines.")
                .long_help("Squeeze consecutive empty lines into a single empty line.")
        )
        .arg(
            Arg::new("squeeze-limit")
                .long("squeeze-limit")
                .value_parser(|s: &str| s.parse::<usize>().map_err(|_| "Requires a non-negative number".to_owned()))
                .long_help("Set the maximum number of consecutive empty lines to be printed.")
                .hide_short_help(true)
        )
        .arg(
            Arg::new("strip-ansi")
                .long("strip-ansi")
                .overrides_with("strip-ansi")
                .value_name("when")
                .value_parser(["auto", "always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Strip colors from the input (auto, always, *never*)")
                .long_help("Specify when to strip ANSI escape sequences from the input. \
                The automatic mode will remove escape sequences unless the syntax highlighting \
                language is plain text. Possible values: auto, always, *never*.")
                .hide_short_help(true)
        )
        .arg(
            Arg::new("style")
                .long("style")
                .action(ArgAction::Append)
                .value_name("components")
                // Cannot use claps built in validation because we have to turn off clap's delimiters
                .value_parser(|val: &str| {
                    match StyleComponentList::from_str(val) {
                        Err(err) => Err(err),
                        Ok(_) => Ok(val.to_owned()),
                    }
                })
                .help(
                    "Comma-separated list of style elements to display \
                     (*default*, auto, full, plain, changes, header, header-filename, header-filesize, grid, rule, numbers, snip).",
                )
                .long_help(
                    "Configure which elements (line numbers, file headers, grid \
                     borders, Git modifications, ..) to display in addition to the \
                     file contents. The argument is a comma-separated list of \
                     components to display (e.g. 'numbers,changes,grid') or a \
                     pre-defined style ('full'). To set a default style, add the \
                     '--style=\"..\"' option to the configuration file or export the \
                     BAT_STYLE environment variable (e.g.: export BAT_STYLE=\"..\").\n\n\
                     When styles are specified in multiple places, the \"nearest\" set \
                     of styles take precedence. The command-line arguments are the highest \
                     priority, followed by the BAT_STYLE environment variable, and then \
                     the configuration file. If any set of styles consists entirely of \
                     components prefixed with \"+\" or \"-\", it will modify the \
                     previous set of styles instead of replacing them.\n\n\
                     By default, the following components are enabled:\n  \
                        changes, grid, header-filename, numbers, snip\n\n\
                     Possible values:\n\n  \
                     * default: enables recommended style components (default).\n  \
                     * full: enables all available components.\n  \
                     * auto: same as 'default', unless the output is piped.\n  \
                     * plain: disables all available components.\n  \
                     * changes: show Git modification markers.\n  \
                     * header: alias for 'header-filename'.\n  \
                     * header-filename: show filenames before the content.\n  \
                     * header-filesize: show file sizes before the content.\n  \
                     * grid: vertical/horizontal lines to separate side bar\n          \
                       and the header from the content.\n  \
                     * rule: horizontal lines to delimit files.\n  \
                     * numbers: show line numbers in the side bar.\n  \
                     * snip: draw separation lines between distinct line ranges.",
                ),
        )
        .arg(
            Arg::new("line-range")
                .long("line-range")
                .short('r')
                .action(ArgAction::Append)
                .value_name("N:M")
                .allow_hyphen_values(true)
                .help("Only print the lines from N to M.")
                .long_help(
                    "Only print the specified range of lines for each file. \
                     For example:\n  \
                     '--line-range 30:40' prints lines 30 to 40\n  \
                     '--line-range :40' prints lines 1 to 40\n  \
                     '--line-range 40:' prints lines 40 to the end of the file\n  \
                     '--line-range 40' only prints line 40\n  \
                     '--line-range -10:' prints the last 10 lines\n  \
                     '--line-range 30:+10' prints lines 30 to 40\n  \
                     '--line-range 35::5' prints lines 30 to 40 (line 35 with 5 lines of context)\n  \
                     '--line-range 30:40:2' prints lines 28 to 42 (range 30-40 with 2 lines of context)",
                ),
        )
        .arg(
            Arg::new("list-languages")
                .long("list-languages")
                .short('L')
                .action(ArgAction::SetTrue)
                .conflicts_with("list-themes")
                .help("Display all supported languages.")
                .long_help("Display a list of supported languages for syntax highlighting."),
        )
        .arg(
            Arg::new("unbuffered")
                .short('u')
                .long("unbuffered")
                .action(ArgAction::SetTrue)
                .help("Enable unbuffered input reading for streaming use cases.")
                .long_help(
                    "Enable unbuffered input reading. When this flag is set, bat will \
                     display data as soon as it is available, without waiting for a \
                     complete line. This is useful for streaming use cases like \
                     'tail -f logfile | bat -u --paging=never'. Note that line numbers \
                     are automatically disabled in unbuffered mode, and syntax \
                     highlighting may be imperfect on partial lines.",
                ),
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg(
            Arg::new("decorations")
                .long("decorations")
                .overrides_with("decorations")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("When to show the decorations (*auto*, never, always).")
                .long_help(
                    "Specify when to use the decorations that have been specified \
                    via '--style'. The automatic mode only enables decorations if \
                    an interactive terminal is detected. The always mode will show \
                    decorations even when piping output. Possible values: *auto*, never, always.",
                )
        )
        .arg(
            Arg::new("force-colorization")
                .long("force-colorization")
                .short('f')
                .action(ArgAction::SetTrue)
                .conflicts_with("color")
                .conflicts_with("decorations")
                .overrides_with("force-colorization")
                .hide_short_help(true)
                .long_help("Alias for '--decorations=always --color=always'. This is useful \
                        if the output of bat is piped to another program, but you want \
                        to keep the colorization/decorations.")
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg(
            Arg::new("decorations")
                .long("decorations")
                .overrides_with("decorations")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("When to show the decorations (*auto*, never, always).")
                .long_help(
                    "Specify when to use the decorations that have been specified \
                    via '--style'. The automatic mode only enables decorations if \
                    an interactive terminal is detected. The always mode will show \
                    decorations even when piping output. Possible values: *auto*, never, always.",
                )
        )
        .arg(
            Arg::new("force-colorization")
                .long("force-colorization")
                .short('f')
                .action(ArgAction::SetTrue)
                .conflicts_with("color")
                .conflicts_with("decorations")
                .overrides_with("force-colorization")
                .hide_short_help(true)
                .long_help("Alias for '--decorations=always --color=always'. This is useful \
                        if the output of bat is piped to another program, but you want \
                        to keep the colorization/decorations.")
        )
        .arg(
            Arg::new("paging")
                .long("paging")
                .overrides_with("paging")
                .overrides_with("no-paging")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify when to use the pager, or use `-P` to disable (*auto*, never, always).")
                .long_help(
                    "Specify when to use the pager. To disable the pager, use \
                    '--paging=never' or its alias,'-P'. To disable the pager permanently, \
                    set BAT_PAGING to 'never'. To control which pager is used, see the \
                    '--pager' option. Possible values: *auto*, never, always."
                ),
        )
        .arg(
            Arg::new("no-paging")
                .short('P')
                .long("no-paging")
                .alias("no-pager")
                .action(ArgAction::SetTrue)
                .overrides_with("no-paging")
                .hide(true)
                .hide_short_help(true)
                .help("Alias for '--paging=never'")
            )
        .arg(
            Arg::new("pager")
                .long("pager")
                .overrides_with("pager")
                .value_name("command")
                .hide_short_help(true)
                .help("Determine which pager to use.")
                .long_help(
                    "Determine which pager is used. This option will override the \
                    PAGER and BAT_PAGER environment variables. The default pager is 'less'. \
                    If you provide '--pager=builtin', use the built-in 'minus' pager. \
                    To control when the pager is used, see the '--paging' option. \
                    Example: '--pager \"less -RF\"'."
                ),
        )
        .arg(
            Arg::new("map-syntax")
                .short('m')
                .long("map-syntax")
                .action(ArgAction::Append)
                .value_name("glob:syntax")
                .help("Use the specified syntax for files matching the glob pattern ('*.cpp:C++').")
                .long_help(
                    "Map a glob pattern to an existing syntax name. The glob pattern is matched \
                     on the full path and the filename. For example, to highlight *.build files \
                     with the Python syntax, use -m '*.build:Python'. To highlight files named \
                     '.myignore' with the Git Ignore syntax, use -m '.myignore:Git Ignore'. Note \
                     that the right-hand side is the *name* of the syntax, not a file extension.",
                )
        )
        .arg(
            Arg::new("ignored-suffix")
                .action(ArgAction::Append)
                .long("ignored-suffix")
                .hide_short_help(true)
                .help(
                    "Ignore extension. For example:\n  \
                    'bat --ignored-suffix \".dev\" my_file.json.dev' will use JSON syntax, and ignore '.dev'"
                )
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg(
            Arg::new("decorations")
                .long("decorations")
                .overrides_with("decorations")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("When to show the decorations (*auto*, never, always).")
                .long_help(
                    "Specify when to use the decorations that have been specified \
                    via '--style'. The automatic mode only enables decorations if \
                    an interactive terminal is detected. The always mode will show \
                    decorations even when piping output. Possible values: *auto*, never, always.",
                )
        )
        .arg(
            Arg::new("force-colorization")
                .long("force-colorization")
                .short('f')
                .action(ArgAction::SetTrue)
                .conflicts_with("color")
                .conflicts_with("decorations")
                .overrides_with("force-colorization")
                .hide_short_help(true)
                .long_help("Alias for '--decorations=always --color=always'. This is useful \
                        if the output of bat is piped to another program, but you want \
                        to keep the colorization/decorations.")
        )
        .arg(
            Arg::new("paging")
                .long("paging")
                .overrides_with("paging")
                .overrides_with("no-paging")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify when to use the pager, or use `-P` to disable (*auto*, never, always).")
                .long_help(
                    "Specify when to use the pager. To disable the pager, use \
                    '--paging=never' or its alias,'-P'. To disable the pager permanently, \
                    set BAT_PAGING to 'never'. To control which pager is used, see the \
                    '--pager' option. Possible values: *auto*, never, always."
                ),
        )
        .arg(
            Arg::new("no-paging")
                .short('P')
                .long("no-paging")
                .alias("no-pager")
                .action(ArgAction::SetTrue)
                .overrides_with("no-paging")
                .hide(true)
                .hide_short_help(true)
                .help("Alias for '--paging=never'")
            )
        .arg(
            Arg::new("pager")
                .long("pager")
                .overrides_with("pager")
                .value_name("command")
                .hide_short_help(true)
                .help("Determine which pager to use.")
                .long_help(
                    "Determine which pager is used. This option will override the \
                    PAGER and BAT_PAGER environment variables. The default pager is 'less'. \
                    If you provide '--pager=builtin', use the built-in 'minus' pager. \
                    To control when the pager is used, see the '--paging' option. \
                    Example: '--pager \"less -RF\"'."
                ),
        )
        .arg(
            Arg::new("map-syntax")
                .short('m')
                .long("map-syntax")
                .action(ArgAction::Append)
                .value_name("glob:syntax")
                .help("Use the specified syntax for files matching the glob pattern ('*.cpp:C++').")
                .long_help(
                    "Map a glob pattern to an existing syntax name. The glob pattern is matched \
                     on the full path and the filename. For example, to highlight *.build files \
                     with the Python syntax, use -m '*.build:Python'. To highlight files named \
                     '.myignore' with the Git Ignore syntax, use -m '.myignore:Git Ignore'. Note \
                     that the right-hand side is the *name* of the syntax, not a file extension.",
                )
        )
        .arg(
            Arg::new("ignored-suffix")
                .action(ArgAction::Append)
                .long("ignored-suffix")
                .hide_short_help(true)
                .help(
                    "Ignore extension. For example:\n  \
                    'bat --ignored-suffix \".dev\" my_file.json.dev' will use JSON syntax, and ignore '.dev'"
                )
        )
        .arg(
            Arg::new("theme")
                .long("theme")
                .overrides_with("theme")
                .help("Set the color theme for syntax highlighting.")
                .long_help(
                    "Set the theme for syntax highlighting. Use '--list-themes' to \
                     see all available themes. To set a default theme, add the \
                     '--theme=\"...\"' option to the configuration file or export the \
                     BAT_THEME environment variable (e.g.: export \
                     BAT_THEME=\"...\").\n\n\
                     Special values:\n\n  \
                     * auto: Picks a dark or light theme depending on the terminal's colors (default).\n          \
                     Use '--theme-light' and '--theme-dark' to customize the selected theme.\n    \
                     * auto:always: Detect the terminal's colors even when the output is redirected.\n    \
                     * auto:system: Detect the color scheme from the system-wide preference (macOS only).\n  \
                     * dark: Use the dark theme specified by '--theme-dark'.\n  \
                     * light: Use the light theme specified by '--theme-light'.",
                ),
        )
        .arg(
            Arg::new("theme-light")
                .long("theme-light")
                .overrides_with("theme-light")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for light backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a light background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-light=\"...\" option to the configuration file or export the BAT_THEME_LIGHT \
                    environment variable (e.g. export BAT_THEME_LIGHT=\"...\")."),
        )
        .arg(
            Arg::new("theme-dark")
                .long("theme-dark")
                .overrides_with("theme-dark")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for dark backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a dark background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-dark=\"...\" option to the configuration file or export the BAT_THEME_DARK \
                    environment variable (e.g. export BAT_THEME_DARK=\"...\")."),
        )
        .arg(
            Arg::new("list-themes")
                .long("list-themes")
                .action(ArgAction::SetTrue)
                .help("Display all supported highlighting themes.")
                .long_help("Display a list of supported themes for syntax highlighting."),
        )
        .arg(
            Arg::new("squeeze-blank")
                .long("squeeze-blank")
                .short('s')
                .action(ArgAction::SetTrue)
                .help("Squeeze consecutive empty lines.")
                .long_help("Squeeze consecutive empty lines into a single empty line.")
        )
        .arg(
            Arg::new("squeeze-limit")
                .long("squeeze-limit")
                .value_parser(|s: &str| s.parse::<usize>().map_err(|_| "Requires a non-negative number".to_owned()))
                .long_help("Set the maximum number of consecutive empty lines to be printed.")
                .hide_short_help(true)
        )
        .arg(
            Arg::new("strip-ansi")
                .long("strip-ansi")
                .overrides_with("strip-ansi")
                .value_name("when")
                .value_parser(["auto", "always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Strip colors from the input (auto, always, *never*)")
                .long_help("Specify when to strip ANSI escape sequences from the input. \
                The automatic mode will remove escape sequences unless the syntax highlighting \
                language is plain text. Possible values: auto, always, *never*.")
                .hide_short_help(true)
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg(
            Arg::new("decorations")
                .long("decorations")
                .overrides_with("decorations")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("When to show the decorations (*auto*, never, always).")
                .long_help(
                    "Specify when to use the decorations that have been specified \
                    via '--style'. The automatic mode only enables decorations if \
                    an interactive terminal is detected. The always mode will show \
                    decorations even when piping output. Possible values: *auto*, never, always.",
                )
        )
        .arg(
            Arg::new("force-colorization")
                .long("force-colorization")
                .short('f')
                .action(ArgAction::SetTrue)
                .conflicts_with("color")
                .conflicts_with("decorations")
                .overrides_with("force-colorization")
                .hide_short_help(true)
                .long_help("Alias for '--decorations=always --color=always'. This is useful \
                        if the output of bat is piped to another program, but you want \
                        to keep the colorization/decorations.")
        )
        .arg(
            Arg::new("paging")
                .long("paging")
                .overrides_with("paging")
                .overrides_with("no-paging")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify when to use the pager, or use `-P` to disable (*auto*, never, always).")
                .long_help(
                    "Specify when to use the pager. To disable the pager, use \
                    '--paging=never' or its alias,'-P'. To disable the pager permanently, \
                    set BAT_PAGING to 'never'. To control which pager is used, see the \
                    '--pager' option. Possible values: *auto*, never, always."
                ),
        )
        .arg(
            Arg::new("no-paging")
                .short('P')
                .long("no-paging")
                .alias("no-pager")
                .action(ArgAction::SetTrue)
                .overrides_with("no-paging")
                .hide(true)
                .hide_short_help(true)
                .help("Alias for '--paging=never'")
            )
        .arg(
            Arg::new("pager")
                .long("pager")
                .overrides_with("pager")
                .value_name("command")
                .hide_short_help(true)
                .help("Determine which pager to use.")
                .long_help(
                    "Determine which pager is used. This option will override the \
                    PAGER and BAT_PAGER environment variables. The default pager is 'less'. \
                    If you provide '--pager=builtin', use the built-in 'minus' pager. \
                    To control when the pager is used, see the '--paging' option. \
                    Example: '--pager \"less -RF\"'."
                ),
        )
        .arg(
            Arg::new("map-syntax")
                .short('m')
                .long("map-syntax")
                .action(ArgAction::Append)
                .value_name("glob:syntax")
                .help("Use the specified syntax for files matching the glob pattern ('*.cpp:C++').")
                .long_help(
                    "Map a glob pattern to an existing syntax name. The glob pattern is matched \
                     on the full path and the filename. For example, to highlight *.build files \
                     with the Python syntax, use -m '*.build:Python'. To highlight files named \
                     '.myignore' with the Git Ignore syntax, use -m '.myignore:Git Ignore'. Note \
                     that the right-hand side is the *name* of the syntax, not a file extension.",
                )
        )
        .arg(
            Arg::new("ignored-suffix")
                .action(ArgAction::Append)
                .long("ignored-suffix")
                .hide_short_help(true)
                .help(
                    "Ignore extension. For example:\n  \
                    'bat --ignored-suffix \".dev\" my_file.json.dev' will use JSON syntax, and ignore '.dev'"
                )
        )
        .arg(
            Arg::new("theme")
                .long("theme")
                .overrides_with("theme")
                .help("Set the color theme for syntax highlighting.")
                .long_help(
                    "Set the theme for syntax highlighting. Use '--list-themes' to \
                     see all available themes. To set a default theme, add the \
                     '--theme=\"...\"' option to the configuration file or export the \
                     BAT_THEME environment variable (e.g.: export \
                     BAT_THEME=\"...\").\n\n\
                     Special values:\n\n  \
                     * auto: Picks a dark or light theme depending on the terminal's colors (default).\n          \
                     Use '--theme-light' and '--theme-dark' to customize the selected theme.\n    \
                     * auto:always: Detect the terminal's colors even when the output is redirected.\n    \
                     * auto:system: Detect the color scheme from the system-wide preference (macOS only).\n  \
                     * dark: Use the dark theme specified by '--theme-dark'.\n  \
                     * light: Use the light theme specified by '--theme-light'.",
                ),
        )
        .arg(
            Arg::new("theme-light")
                .long("theme-light")
                .overrides_with("theme-light")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for light backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a light background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-light=\"...\" option to the configuration file or export the BAT_THEME_LIGHT \
                    environment variable (e.g. export BAT_THEME_LIGHT=\"...\")."),
        )
        .arg(
            Arg::new("theme-dark")
                .long("theme-dark")
                .overrides_with("theme-dark")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for dark backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a dark background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-dark=\"...\" option to the configuration file or export the BAT_THEME_DARK \
                    environment variable (e.g. export BAT_THEME_DARK=\"...\")."),
        )
        .arg(
            Arg::new("list-themes")
                .long("list-themes")
                .action(ArgAction::SetTrue)
                .help("Display all supported highlighting themes.")
                .long_help("Display a list of supported themes for syntax highlighting."),
        )
        .arg(
            Arg::new("squeeze-blank")
                .long("squeeze-blank")
                .short('s')
                .action(ArgAction::SetTrue)
                .help("Squeeze consecutive empty lines.")
                .long_help("Squeeze consecutive empty lines into a single empty line.")
        )
        .arg(
            Arg::new("squeeze-limit")
                .long("squeeze-limit")
                .value_parser(|s: &str| s.parse::<usize>().map_err(|_| "Requires a non-negative number".to_owned()))
                .long_help("Set the maximum number of consecutive empty lines to be printed.")
                .hide_short_help(true)
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 101 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `build_app()`
- **變更前簽章 (Before)**: `fn build_app(interactive_output: bool)` (L21~L776)
- **變更後簽章 (After)**: `fn build_app(interactive_output: bool)` (L21~L780)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn build_app(interactive_output: bool) -> Command {
    let color_when = if interactive_output && !crate::app::env_no_color() {
        ColorChoice::Auto
    } else {
        ColorChoice::Never
    };

    let mut app = Command::new(crate_name!())
        .version(VERSION.as_str())
        .color(color_when)
        .hide_possible_values(true)
        .args_conflicts_with_subcommands(true)
        .allow_external_subcommands(true)
        .disable_help_subcommand(true)
        .disable_help_flag(true)
        .disable_version_flag(true)
        .max_term_width(100)
        .about("A cat(1) clone with wings.")
        .long_about("A cat(1) clone with syntax highlighting and Git integration.")
        .arg(
            Arg::new("FILE")
                .help("File(s) to print / concatenate. Use '-' for standard input.")
                .long_help(
                    "File(s) to print / concatenate. Use a dash ('-') or no argument at all \
                     to read from standard input.",
                )
                .num_args(1..)
                .value_parser(value_parser!(PathBuf)),
        )
        .arg(
            Arg::new("show-all")
                .long("show-all")
                .alias("show-nonprintable")
                .short('A')
                .action(ArgAction::SetTrue)
                .conflicts_with("language")
                .help("Show non-printable characters (space, tab, newline, ..).")
                .long_help(
                    "Show non-printable characters like space, tab or newline. \
                     This option can also be used to print binary files. \
                     Use '--tabs' to control the width of the tab-placeholders.",
                ),
        )
        .arg(
            Arg::new("nonprintable-notation")
                .long("nonprintable-notation")
                .action(ArgAction::Set)
                .default_value("unicode")
                .value_parser(["unicode", "caret"])
                .value_name("notation")
                .hide_default_value(true)
                .help("Set notation for non-printable characters.")
                .long_help(
                    "Set notation for non-printable characters.\n\n\
                    Possible values:\n  \
                    * unicode (␇, ␊, ␀, ..)\n  \
                    * caret   (^G, ^J, ^@, ..)",
                ),
        )
        .arg(
            Arg::new("binary")
                .long("binary")
                .action(ArgAction::Set)
                .default_value("no-printing")
                .value_parser(["no-printing", "as-text"])
                .value_name("behavior")
                .hide_default_value(true)
                .help("How to treat binary content. (default: no-printing)")
                .long_help(
                    "How to treat binary content. (default: no-printing)\n\n\
                    Possible values:\n  \
                    * no-printing: do not print any binary content\n  \
                    * as-text: treat binary content as normal text",
                ),
        )
        .arg(
            Arg::new("plain")
                .overrides_with("plain")
                .overrides_with("number")
                .short('p')
                .long("plain")
                .action(ArgAction::Count)
                .help("Show plain style (alias for '--style=plain').")
                .long_help(
                    "Only show plain style, no decorations. This is an alias for \
                     '--style=plain'. When '-p' is used twice ('-pp'), it also disables \
                     automatic paging (alias for '--style=plain --paging=never').",
                ),
        )
        .arg(
            Arg::new("language")
                .short('l')
                .long("language")
                .overrides_with("language")
                .help("Set the language for syntax highlighting.")
                .long_help(
                    "Explicitly set the language for syntax highlighting. The language can be \
                     specified as a name (like 'C++' or 'LaTeX') or possible file extension \
                     (like 'cpp', 'hpp' or 'md'). Use '--list-languages' to show all supported \
                     language names and file extensions.",
                ),
        )
        .arg(
            Arg::new("fallback-syntax")
                .long("fallback-syntax")
                .visible_alias("fallback-language")
                .help("Set a fallback language for undetected syntaxes.")
                .long_help(
                    "Set a fallback language for syntax highlighting when auto-detection fails. \
                     Unlike '--language', this is only used when no syntax could be detected from \
                     filename, custom syntax mappings, or first-line detection.",
                ),
        )
        .arg(
            Arg::new("highlight-line")
                .long("highlight-line")
                .short('H')
                .action(ArgAction::Append)
                .value_name("N:M")
                .help("Highlight lines N through M.")
                .long_help(
                    "Highlight the specified line ranges with a different background color \
                     For example:\n  \
                     '--highlight-line 40' highlights line 40\n  \
                     '--highlight-line 30:40' highlights lines 30 to 40\n  \
                     '--highlight-line :40' highlights lines 1 to 40\n  \
                     '--highlight-line 40:' highlights lines 40 to the end of the file\n  \
                     '--highlight-line 30:+10' highlights lines 30 to 40",
                ),
        )
        .arg(
            Arg::new("file-name")
                .long("file-name")
                .action(ArgAction::Append)
                .value_name("name")
                .value_parser(value_parser!(PathBuf))
                .help("Specify the name to display for a file.")
                .long_help(
                    "Specify the name to display for a file. Useful when piping \
                     data to bat from STDIN when bat does not otherwise know \
                     the filename. Note that the provided file name is also \
                     used for syntax detection.",
                ),
        );

    #[cfg(feature = "git")]
    {
        app = app
                .arg(
                    Arg::new("diff")
                        .long("diff")
                        .short('d')
                        .action(ArgAction::SetTrue)
                        .conflicts_with("line-range")
                        .help("Only show lines that have been added/removed/modified.")
                        .long_help(
                            "Only show lines that have been added/removed/modified with respect \
                     to the Git index. Use --diff-context=N to control how much context you want to see.",
                        ),
                )
                .arg(
                    Arg::new("diff-context")
                        .long("diff-context")
                        .overrides_with("diff-context")
                        .value_name("N")
                        .value_parser(
                            |n: &str| {
                                n.parse::<usize>()
                                    .map_err(|_| "must be a number")
                                    .map(|_| n.to_owned()) // Convert to Result<String, &str>
                                    .map_err(|e| e.to_string())
                            }, // Convert to Result<(), String>
                        )
                        .hide_short_help(true)
                        .long_help(
                            "Include N lines of context around added/removed/modified lines when using '--diff'.",
                        ),
                )
    }

    app = app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg(
            Arg::new("decorations")
                .long("decorations")
                .overrides_with("decorations")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("When to show the decorations (*auto*, never, always).")
                .long_help(
                    "Specify when to use the decorations that have been specified \
                    via '--style'. The automatic mode only enables decorations if \
                    an interactive terminal is detected. The always mode will show \
                    decorations even when piping output. Possible values: *auto*, never, always.",
                )
        )
        .arg(
            Arg::new("force-colorization")
                .long("force-colorization")
                .short('f')
                .action(ArgAction::SetTrue)
                .conflicts_with("color")
                .conflicts_with("decorations")
                .overrides_with("force-colorization")
                .hide_short_help(true)
                .long_help("Alias for '--decorations=always --color=always'. This is useful \
                        if the output of bat is piped to another program, but you want \
                        to keep the colorization/decorations.")
        )
        .arg(
            Arg::new("paging")
                .long("paging")
                .overrides_with("paging")
                .overrides_with("no-paging")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify when to use the pager, or use `-P` to disable (*auto*, never, always).")
                .long_help(
                    "Specify when to use the pager. To disable the pager, use \
                    '--paging=never' or its alias,'-P'. To disable the pager permanently, \
                    set BAT_PAGING to 'never'. To control which pager is used, see the \
                    '--pager' option. Possible values: *auto*, never, always."
                ),
        )
        .arg(
            Arg::new("no-paging")
                .short('P')
                .long("no-paging")
                .alias("no-pager")
                .action(ArgAction::SetTrue)
                .overrides_with("no-paging")
                .hide(true)
                .hide_short_help(true)
                .help("Alias for '--paging=never'")
            )
        .arg(
            Arg::new("pager")
                .long("pager")
                .overrides_with("pager")
                .value_name("command")
                .hide_short_help(true)
                .help("Determine which pager to use.")
                .long_help(
                    "Determine which pager is used. This option will override the \
                    PAGER and BAT_PAGER environment variables. The default pager is 'less'. \
                    If you provide '--pager=builtin', use the built-in 'minus' pager. \
                    To control when the pager is used, see the '--paging' option. \
                    Example: '--pager \"less -RF\"'."
                ),
        )
        .arg(
            Arg::new("map-syntax")
                .short('m')
                .long("map-syntax")
                .action(ArgAction::Append)
                .value_name("glob:syntax")
                .help("Use the specified syntax for files matching the glob pattern ('*.cpp:C++').")
                .long_help(
                    "Map a glob pattern to an existing syntax name. The glob pattern is matched \
                     on the full path and the filename. For example, to highlight *.build files \
                     with the Python syntax, use -m '*.build:Python'. To highlight files named \
                     '.myignore' with the Git Ignore syntax, use -m '.myignore:Git Ignore'. Note \
                     that the right-hand side is the *name* of the syntax, not a file extension.",
                )
        )
        .arg(
            Arg::new("ignored-suffix")
                .action(ArgAction::Append)
                .long("ignored-suffix")
                .hide_short_help(true)
                .help(
                    "Ignore extension. For example:\n  \
                    'bat --ignored-suffix \".dev\" my_file.json.dev' will use JSON syntax, and ignore '.dev'"
                )
        )
        .arg(
            Arg::new("theme")
                .long("theme")
                .overrides_with("theme")
                .help("Set the color theme for syntax highlighting.")
                .long_help(
                    "Set the theme for syntax highlighting. Use '--list-themes' to \
                     see all available themes. To set a default theme, add the \
                     '--theme=\"...\"' option to the configuration file or export the \
                     BAT_THEME environment variable (e.g.: export \
                     BAT_THEME=\"...\").\n\n\
                     Special values:\n\n  \
                     * auto: Picks a dark or light theme depending on the terminal's colors (default).\n          \
                     Use '--theme-light' and '--theme-dark' to customize the selected theme.\n    \
                     * auto:always: Detect the terminal's colors even when the output is redirected.\n    \
                     * auto:system: Detect the color scheme from the system-wide preference (macOS only).\n  \
                     * dark: Use the dark theme specified by '--theme-dark'.\n  \
                     * light: Use the light theme specified by '--theme-light'.",
                ),
        )
        .arg(
            Arg::new("theme-light")
                .long("theme-light")
                .overrides_with("theme-light")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for light backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a light background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-light=\"...\" option to the configuration file or export the BAT_THEME_LIGHT \
                    environment variable (e.g. export BAT_THEME_LIGHT=\"...\")."),
        )
        .arg(
            Arg::new("theme-dark")
                .long("theme-dark")
                .overrides_with("theme-dark")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for dark backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a dark background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-dark=\"...\" option to the configuration file or export the BAT_THEME_DARK \
                    environment variable (e.g. export BAT_THEME_DARK=\"...\")."),
        )
        .arg(
            Arg::new("list-themes")
                .long("list-themes")
                .action(ArgAction::SetTrue)
                .help("Display all supported highlighting themes.")
                .long_help("Display a list of supported themes for syntax highlighting."),
        )
        .arg(
            Arg::new("squeeze-blank")
                .long("squeeze-blank")
                .short('s')
                .action(ArgAction::SetTrue)
                .help("Squeeze consecutive empty lines.")
                .long_help("Squeeze consecutive empty lines into a single empty line.")
        )
        .arg(
            Arg::new("squeeze-limit")
                .long("squeeze-limit")
                .value_parser(|s: &str| s.parse::<usize>().map_err(|_| "Requires a non-negative number".to_owned()))
                .long_help("Set the maximum number of consecutive empty lines to be printed.")
                .hide_short_help(true)
        )
        .arg(
            Arg::new("strip-ansi")
                .long("strip-ansi")
                .overrides_with("strip-ansi")
                .value_name("when")
                .value_parser(["auto", "always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Strip colors from the input (auto, always, *never*)")
                .long_help("Specify when to strip ANSI escape sequences from the input. \
                The automatic mode will remove escape sequences unless the syntax highlighting \
                language is plain text. Possible values: auto, always, *never*.")
                .hide_short_help(true)
        )
        .arg(
            Arg::new("style")
                .long("style")
                .action(ArgAction::Append)
                .value_name("components")
                // Cannot use claps built in validation because we have to turn off clap's delimiters
                .value_parser(|val: &str| {
                    match StyleComponentList::from_str(val) {
                        Err(err) => Err(err),
                        Ok(_) => Ok(val.to_owned()),
                    }
                })
                .help(
                    "Comma-separated list of style elements to display \
                     (*default*, auto, full, plain, changes, header, header-filename, header-filesize, grid, rule, numbers, snip).",
                )
                .long_help(
                    "Configure which elements (line numbers, file headers, grid \
                     borders, Git modifications, ..) to display in addition to the \
                     file contents. The argument is a comma-separated list of \
                     components to display (e.g. 'numbers,changes,grid') or a \
                     pre-defined style ('full'). To set a default style, add the \
                     '--style=\"..\"' option to the configuration file or export the \
                     BAT_STYLE environment variable (e.g.: export BAT_STYLE=\"..\").\n\n\
                     When styles are specified in multiple places, the \"nearest\" set \
                     of styles take precedence. The command-line arguments are the highest \
                     priority, followed by the BAT_STYLE environment variable, and then \
                     the configuration file. If any set of styles consists entirely of \
                     components prefixed with \"+\" or \"-\", it will modify the \
                     previous set of styles instead of replacing them.\n\n\
                     By default, the following components are enabled:\n  \
                        changes, grid, header-filename, numbers, snip\n\n\
                     Possible values:\n\n  \
                     * default: enables recommended style components (default).\n  \
                     * full: enables all available components.\n  \
                     * auto: same as 'default', unless the output is piped.\n  \
                     * plain: disables all available components.\n  \
                     * changes: show Git modification markers.\n  \
                     * header: alias for 'header-filename'.\n  \
                     * header-filename: show filenames before the content.\n  \
                     * header-filesize: show file sizes before the content.\n  \
                     * grid: vertical/horizontal lines to separate side bar\n          \
                       and the header from the content.\n  \
                     * rule: horizontal lines to delimit files.\n  \
                     * numbers: show line numbers in the side bar.\n  \
                     * snip: draw separation lines between distinct line ranges.",
                ),
        )
        .arg(
            Arg::new("line-range")
                .long("line-range")
                .short('r')
                .action(ArgAction::Append)
                .value_name("N:M")
                .allow_hyphen_values(true)
                .help("Only print the lines from N to M.")
                .long_help(
                    "Only print the specified range of lines for each file. \
                     For example:\n  \
                     '--line-range 30:40' prints lines 30 to 40\n  \
                     '--line-range :40' prints lines 1 to 40\n  \
                     '--line-range 40:' prints lines 40 to the end of the file\n  \
                     '--line-range 40' only prints line 40\n  \
                     '--line-range -10:' prints the last 10 lines\n  \
                     '--line-range 30:+10' prints lines 30 to 40\n  \
                     '--line-range 35::5' prints lines 30 to 40 (line 35 with 5 lines of context)\n  \
                     '--line-range 30:40:2' prints lines 28 to 42 (range 30-40 with 2 lines of context)",
                ),
        )
        .arg(
            Arg::new("list-languages")
                .long("list-languages")
                .short('L')
                .action(ArgAction::SetTrue)
                .conflicts_with("list-themes")
                .help("Display all supported languages.")
                .long_help("Display a list of supported languages for syntax highlighting."),
        )
        .arg(
            Arg::new("unbuffered")
                .short('u')
                .long("unbuffered")
                .action(ArgAction::SetTrue)
                .help("Enable unbuffered input reading for streaming use cases.")
                .long_help(
                    "Enable unbuffered input reading. When this flag is set, bat will \
                     display data as soon as it is available, without waiting for a \
                     complete line. This is useful for streaming use cases like \
                     'tail -f logfile | bat -u --paging=never'. Note that line numbers \
                     are automatically disabled in unbuffered mode, and syntax \
                     highlighting may be imperfect on partial lines.",
                ),
        )
        .arg(
            Arg::new("no-config")
                .long("no-config")
                .action(ArgAction::SetTrue)
                .hide(true)
                .help("Do not use the configuration file"),
        )
        .arg(
            Arg::new("no-custom-assets")
                .long("no-custom-assets")
                .action(ArgAction::SetTrue)
                .hide(true)
                .help("Do not load custom assets"),
        );

    #[cfg(feature = "application")]
    {
        app = app.arg(
            Arg::new("completion")
            .long("completion")
            .value_name("SHELL")
            .value_parser(["bash", "fish", "ps1", "zsh"])
            .help("Show shell completion for a certain shell. [possible values: bash, fish, zsh, ps1]"),
        );
    }

    #[cfg(feature = "lessopen")]
    {
        app = app
            .arg(
                Arg::new("lessopen")
                    .long("lessopen")
                    .action(ArgAction::SetTrue)
                    .help("Enable the $LESSOPEN preprocessor"),
            )
            .arg(
                Arg::new("no-lessopen")
                    .long("no-lessopen")
                    .action(ArgAction::SetTrue)
                    .overrides_with("lessopen")
                    .hide(true)
                    .help("Disable the $LESSOPEN preprocessor if enabled (overrides --lessopen)"),
            )
    }

    app = app
        .arg(
            Arg::new("config-file")
                .long("config-file")
                .action(ArgAction::SetTrue)
                .conflicts_with("list-languages")
                .conflicts_with("list-themes")
                .hide(true)
                .help("Show path to the configuration file."),
        )
        .arg(
            Arg::new("generate-config-file")
                .long("generate-config-file")
                .action(ArgAction::SetTrue)
                .conflicts_with("list-languages")
                .conflicts_with("list-themes")
                .hide(true)
                .help("Generates a default configuration file."),
        )
        .arg(
            Arg::new("config-dir")
                .long("config-dir")
                .action(ArgAction::SetTrue)
                .hide(true)
                .help("Show bat's configuration directory."),
        )
        .arg(
            Arg::new("cache-dir")
                .long("cache-dir")
                .action(ArgAction::SetTrue)
                .hide(true)
                .help("Show bat's cache directory."),
        )
        .arg(
            Arg::new("diagnostic")
                .long("diagnostic")
                .alias("diagnostics")
                .action(ArgAction::SetTrue)
                .hide_short_help(true)
                .help("Show diagnostic information for bug reports."),
        )
        .arg(
            Arg::new("quiet-empty")
                .long("quiet-empty")
                .short('E')
                .action(ArgAction::SetTrue)
                .help("Produce no output when the input is empty.")
                .long_help(
                    "When this flag is set, bat will produce no output at all when \
                     the input is empty. This is useful when piping commands that may \
                     produce empty output, like 'git diff'.",
                ),
        )
        .arg(
            Arg::new("acknowledgements")
                .long("acknowledgements")
                .action(ArgAction::SetTrue)
                .hide_short_help(true)
                .help("Show acknowledgements."),
        )
        .arg(
            Arg::new("set-terminal-title")
                .long("set-terminal-title")
                .action(ArgAction::SetTrue)
                .hide_short_help(true)
                .help("Sets terminal title to filenames when using a pager."),
        )
        .arg(
            Arg::new("help")
                .short('h')
                .long("help")
                .action(ArgAction::SetTrue)
                .help("Print help (see more with '--help')")
                .long_help("Print help (see a summary with '-h')"),
        )
        .arg(
            Arg::new("version")
                .long("version")
                .short('V')
                .action(ArgAction::Version)
                .help("Print version"),
        );

    // Check if the current directory contains a file name cache. Otherwise,
    // enable the 'bat cache' subcommand.
    if Path::new("cache").exists() {
        app
    } else {
        app.subcommand(
            Command::new("cache")
                .hide(true)
                .about("Modify the syntax-definition and theme cache")
                .arg_required_else_help(true)
                .arg(
                    Arg::new("help")
                        .short('h')
                        .long("help")
                        .action(ArgAction::Help)
                        .help("Print help"),
                )
                .arg(
                    Arg::new("build")
                        .long("build")
                        .short('b')
                        .action(ArgAction::SetTrue)
                        .conflicts_with("clear")
                        .help("Initialize (or update) the syntax/theme cache.")
                        .long_help(
                            "Initialize (or update) the syntax/theme cache by loading from \
                             the source directory (default: the configuration directory).",
                        ),
                )
                .arg(
                    Arg::new("clear")
                        .long("clear")
                        .short('c')
                        .action(ArgAction::SetTrue)
                        .conflicts_with("build")
                        .help("Remove the cached syntax definitions and themes."),
                )
                .arg(
                    Arg::new("source")
                        .long("source")
                        .requires("build")
                        .value_name("dir")
                        .help("Use a different directory to load syntaxes and themes from."),
                )
                .arg(
                    Arg::new("target")
                        .long("target")
                        .requires("build")
                        .value_name("dir")
                        .help(
                            "Use a different directory to store the cached syntax and theme set.",
                        ),
                )
                .arg(
                    Arg::new("blank")
                        .long("blank")
                        .action(ArgAction::SetTrue)
                        .requires("build")
                        .help(
                            "Create completely new syntax and theme sets \
                             (instead of appending to the default sets).",
                        ),
                )
                .arg(
                    Arg::new("acknowledgements")
                        .long("acknowledgements")
                        .action(ArgAction::SetTrue)
                        .requires("build")
                        .help("Build acknowledgements.bin."),
                ),
        )
        .after_long_help(
            "You can use 'bat cache' to customize syntaxes and themes. \
            See 'bat cache --help' for more information",
        )
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn build_app(interactive_output: bool) -> Command {
    let color_when = if interactive_output && !crate::app::env_no_color() {
        ColorChoice::Auto
    } else {
        ColorChoice::Never
    };

    let mut app = Command::new(crate_name!())
        .version(VERSION.as_str())
        .color(color_when)
        .hide_possible_values(true)
        .args_conflicts_with_subcommands(true)
        .allow_external_subcommands(true)
        .disable_help_subcommand(true)
        .disable_help_flag(true)
        .disable_version_flag(true)
        .max_term_width(100)
        .about("A cat(1) clone with wings.")
        .long_about("A cat(1) clone with syntax highlighting and Git integration.")
        .arg(
            Arg::new("FILE")
                .help("File(s) to print / concatenate. Use '-' for standard input.")
                .long_help(
                    "File(s) to print / concatenate. Use a dash ('-') or no argument at all \
                     to read from standard input.",
                )
                .num_args(1..)
                .value_parser(value_parser!(PathBuf)),
        )
        .arg(
            Arg::new("show-all")
                .long("show-all")
                .alias("show-nonprintable")
                .short('A')
                .action(ArgAction::SetTrue)
                .conflicts_with("language")
                .help("Show non-printable characters (space, tab, newline, ..).")
                .long_help(
                    "Show non-printable characters like space, tab or newline. \
                     This option can also be used to print binary files. \
                     Use '--tabs' to control the width of the tab-placeholders.",
                ),
        )
        .arg(
            Arg::new("nonprintable-notation")
                .long("nonprintable-notation")
                .action(ArgAction::Set)
                .default_value("unicode")
                .value_parser(["unicode", "caret"])
                .value_name("notation")
                .hide_default_value(true)
                .help("Set notation for non-printable characters.")
                .long_help(
                    "Set notation for non-printable characters.\n\n\
                    Possible values:\n  \
                    * unicode (␇, ␊, ␀, ..)\n  \
                    * caret   (^G, ^J, ^@, ..)",
                ),
        )
        .arg(
            Arg::new("binary")
                .long("binary")
                .action(ArgAction::Set)
                .default_value("no-printing")
                .value_parser(["no-printing", "as-text"])
                .value_name("behavior")
                .hide_default_value(true)
                .help("How to treat binary content. (default: no-printing)")
                .long_help(
                    "How to treat binary content. (default: no-printing)\n\n\
                    Possible values:\n  \
                    * no-printing: do not print any binary content\n  \
                    * as-text: treat binary content as normal text",
                ),
        )
        .arg(
            Arg::new("plain")
                .overrides_with("plain")
                .overrides_with("number")
                .short('p')
                .long("plain")
                .action(ArgAction::Count)
                .help("Show plain style (alias for '--style=plain').")
                .long_help(
                    "Only show plain style, no decorations. This is an alias for \
                     '--style=plain'. When '-p' is used twice ('-pp'), it also disables \
                     automatic paging (alias for '--style=plain --paging=never').",
                ),
        )
        .arg(
            Arg::new("language")
                .short('l')
                .long("language")
                .overrides_with("language")
                .help("Set the language for syntax highlighting.")
                .long_help(
                    "Explicitly set the language for syntax highlighting. The language can be \
                     specified as a name (like 'C++' or 'LaTeX') or possible file extension \
                     (like 'cpp', 'hpp' or 'md'). Use '--list-languages' to show all supported \
                     language names and file extensions.",
                ),
        )
        .arg(
            Arg::new("fallback-syntax")
                .long("fallback-syntax")
                .visible_alias("fallback-language")
                .help("Set a fallback language for undetected syntaxes.")
                .long_help(
                    "Set a fallback language for syntax highlighting when auto-detection fails. \
                     Unlike '--language', this is only used when no syntax could be detected from \
                     filename, custom syntax mappings, or first-line detection.",
                ),
        )
        .arg(
            Arg::new("highlight-line")
                .long("highlight-line")
                .short('H')
                .action(ArgAction::Append)
                .value_name("N:M")
                .help("Highlight lines N through M.")
                .long_help(
                    "Highlight the specified line ranges with a different background color \
                     For example:\n  \
                     '--highlight-line 40' highlights line 40\n  \
                     '--highlight-line 30:40' highlights lines 30 to 40\n  \
                     '--highlight-line :40' highlights lines 1 to 40\n  \
                     '--highlight-line 40:' highlights lines 40 to the end of the file\n  \
                     '--highlight-line 30:+10' highlights lines 30 to 40",
                ),
        )
        .arg(
            Arg::new("file-name")
                .long("file-name")
                .action(ArgAction::Append)
                .value_name("name")
                .value_parser(value_parser!(PathBuf))
                .help("Specify the name to display for a file.")
                .long_help(
                    "Specify the name to display for a file. Useful when piping \
                     data to bat from STDIN when bat does not otherwise know \
                     the filename. Note that the provided file name is also \
                     used for syntax detection.",
                ),
        );

    #[cfg(feature = "git")]
    {
        app = app
                .arg(
                    Arg::new("diff")
                        .long("diff")
                        .short('d')
                        .action(ArgAction::SetTrue)
                        .conflicts_with("line-range")
                        .help("Only show lines that have been added/removed/modified.")
                        .long_help(
                            "Only show lines that have been added/removed/modified with respect \
                     to the Git index. Use --diff-context=N to control how much context you want to see.",
                        ),
                )
                .arg(
                    Arg::new("diff-context")
                        .long("diff-context")
                        .overrides_with("diff-context")
                        .value_name("N")
                        .value_parser(
                            |n: &str| {
                                n.parse::<usize>()
                                    .map_err(|_| "must be a number")
                                    .map(|_| n.to_owned()) // Convert to Result<String, &str>
                                    .map_err(|e| e.to_string())
                            }, // Convert to Result<(), String>
                        )
                        .hide_short_help(true)
                        .long_help(
                            "Include N lines of context around added/removed/modified lines when using '--diff'.",
                        ),
                )
    }

    app = app.arg(
        Arg::new("tabs")
            .long("tabs")
            .overrides_with("tabs")
            .value_name("T")
            .value_parser(
                |t: &str| {
                    t.parse::<u32>()
                        .map_err(|_t| "must be a number")
                        .map(|_t| t.to_owned()) // Convert to Result<String, &str>
                        .map_err(|e| e.to_string())
                }, // Convert to Result<(), String>
            )
            .help("Set the tab width to T spaces.")
            .long_help(
                "Set the tab width to T spaces. Use a width of 0 to pass tabs through \
                     directly",
            ),
    )
        .arg(
            Arg::new("wrap")
                .long("wrap")
                .overrides_with("wrap")
                .value_name("mode")
                .value_parser(["auto", "never", "character", "word"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify the text-wrapping mode (*auto*, never, character, word).")
                .long_help("Specify the text-wrapping mode (*auto*, never, character, word). \
                           The '--terminal-width' option can be used in addition to \
                           control the output width."),
        )
        .arg(
            Arg::new("chop-long-lines")
                .long("chop-long-lines")
                .short('S')
                .action(ArgAction::SetTrue)
                .help("Truncate all lines longer than screen width. Alias for '--wrap=never'."),
        )
        .arg(
            Arg::new("terminal-width")
                .long("terminal-width")
                .overrides_with("terminal-width")
                .value_name("width")
                .hide_short_help(true)
                .allow_hyphen_values(true)
                .value_parser(
                    |t: &str| {
                        let is_offset = t.starts_with('+') || t.starts_with('-');
                        t.parse::<i32>()
                            .map_err(|_e| "must be an offset or number")
                            .and_then(|v| if v == 0 && !is_offset {
                                Err("terminal width cannot be zero")
                            } else {
                                Ok(t.to_owned())
                            })
                            .map_err(|e| e.to_string())
                    })
                .help("Explicitly set the width of the terminal instead of determining it automatically.")
                .long_help(
                    "Explicitly set the width of the terminal instead of determining it \
                     automatically. If prefixed with '+' or '-', the value will be treated \
                     as an offset to the actual terminal width. This can also be configured \
                     via the BAT_WIDTH environment variable (e.g. export BAT_WIDTH=\"100\"). \
                     See also: '--wrap'.",
                ),
        )
        .arg(
            Arg::new("number")
                .long("number")
                .overrides_with("number")
                .short('n')
                .action(ArgAction::SetTrue)
                .help("Show line numbers (alias for '--style=numbers').")
                .long_help(
                    "Only show line numbers, no other decorations. This is an alias for \
                     '--style=numbers'",
                ),
        )
        .arg(
            Arg::new("color")
                .long("color")
                .overrides_with("color")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .hide_default_value(true)
                .default_value("auto")
                .help("When to use colors (*auto*, never, always).")
                .long_help(
                    "Specify when to use colored output. The automatic mode \
                     only enables colors if an interactive terminal is detected - \
                     colors are automatically disabled if the output goes to a pipe.\n\
                     Possible values: *auto*, never, always.",
                ),
        )
        .arg(
            Arg::new("italic-text")
                .long("italic-text")
                .value_name("when")
                .value_parser(["always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Use italics in output (always, *never*)")
                .long_help("Specify when to use ANSI sequences for italic text in the output. Possible values: always, *never*."),
        )
        .arg(
            Arg::new("decorations")
                .long("decorations")
                .overrides_with("decorations")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("When to show the decorations (*auto*, never, always).")
                .long_help(
                    "Specify when to use the decorations that have been specified \
                    via '--style'. The automatic mode only enables decorations if \
                    an interactive terminal is detected. The always mode will show \
                    decorations even when piping output. Possible values: *auto*, never, always.",
                )
        )
        .arg(
            Arg::new("force-colorization")
                .long("force-colorization")
                .short('f')
                .action(ArgAction::SetTrue)
                .conflicts_with("color")
                .conflicts_with("decorations")
                .overrides_with("force-colorization")
                .hide_short_help(true)
                .long_help("Alias for '--decorations=always --color=always'. This is useful \
                        if the output of bat is piped to another program, but you want \
                        to keep the colorization/decorations.")
        )
        .arg(
            Arg::new("paging")
                .long("paging")
                .overrides_with("paging")
                .overrides_with("no-paging")
                .value_name("when")
                .value_parser(["auto", "never", "always"])
                .default_value("auto")
                .hide_default_value(true)
                .help("Specify when to use the pager, or use `-P` to disable (*auto*, never, always).")
                .long_help(
                    "Specify when to use the pager. To disable the pager, use \
                    '--paging=never' or its alias,'-P'. To disable the pager permanently, \
                    set BAT_PAGING to 'never'. To control which pager is used, see the \
                    '--pager' option. Possible values: *auto*, never, always."
                ),
        )
        .arg(
            Arg::new("no-paging")
                .short('P')
                .long("no-paging")
                .alias("no-pager")
                .action(ArgAction::SetTrue)
                .overrides_with("no-paging")
                .hide(true)
                .hide_short_help(true)
                .help("Alias for '--paging=never'")
            )
        .arg(
            Arg::new("pager")
                .long("pager")
                .overrides_with("pager")
                .value_name("command")
                .hide_short_help(true)
                .help("Determine which pager to use.")
                .long_help(
                    "Determine which pager is used. This option will override the \
                    PAGER and BAT_PAGER environment variables. The default pager is 'less'. \
                    If you provide '--pager=builtin', use the built-in 'minus' pager. \
                    To control when the pager is used, see the '--paging' option. \
                    Example: '--pager \"less -RF\"'."
                ),
        )
        .arg(
            Arg::new("map-syntax")
                .short('m')
                .long("map-syntax")
                .action(ArgAction::Append)
                .value_name("glob:syntax")
                .help("Use the specified syntax for files matching the glob pattern ('*.cpp:C++').")
                .long_help(
                    "Map a glob pattern to an existing syntax name. The glob pattern is matched \
                     on the full path and the filename. For example, to highlight *.build files \
                     with the Python syntax, use -m '*.build:Python'. To highlight files named \
                     '.myignore' with the Git Ignore syntax, use -m '.myignore:Git Ignore'. Note \
                     that the right-hand side is the *name* of the syntax, not a file extension.",
                )
        )
        .arg(
            Arg::new("ignored-suffix")
                .action(ArgAction::Append)
                .long("ignored-suffix")
                .hide_short_help(true)
                .help(
                    "Ignore extension. For example:\n  \
                    'bat --ignored-suffix \".dev\" my_file.json.dev' will use JSON syntax, and ignore '.dev'"
                )
        )
        .arg(
            Arg::new("theme")
                .long("theme")
                .overrides_with("theme")
                .help("Set the color theme for syntax highlighting.")
                .long_help(
                    "Set the theme for syntax highlighting. Use '--list-themes' to \
                     see all available themes. To set a default theme, add the \
                     '--theme=\"...\"' option to the configuration file or export the \
                     BAT_THEME environment variable (e.g.: export \
                     BAT_THEME=\"...\").\n\n\
                     Special values:\n\n  \
                     * auto: Picks a dark or light theme depending on the terminal's colors (default).\n          \
                     Use '--theme-light' and '--theme-dark' to customize the selected theme.\n    \
                     * auto:always: Detect the terminal's colors even when the output is redirected.\n    \
                     * auto:system: Detect the color scheme from the system-wide preference (macOS only).\n  \
                     * dark: Use the dark theme specified by '--theme-dark'.\n  \
                     * light: Use the light theme specified by '--theme-light'.",
                ),
        )
        .arg(
            Arg::new("theme-light")
                .long("theme-light")
                .overrides_with("theme-light")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for light backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a light background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-light=\"...\" option to the configuration file or export the BAT_THEME_LIGHT \
                    environment variable (e.g. export BAT_THEME_LIGHT=\"...\")."),
        )
        .arg(
            Arg::new("theme-dark")
                .long("theme-dark")
                .overrides_with("theme-dark")
                .value_name("theme")
                .help("Sets the color theme for syntax highlighting used for dark backgrounds.")
                .long_help(
                    "Sets the theme name for syntax highlighting used when the terminal uses a dark background. \
                    Use '--list-themes' to see all available themes. To set a default theme, add the \
                    '--theme-dark=\"...\" option to the configuration file or export the BAT_THEME_DARK \
                    environment variable (e.g. export BAT_THEME_DARK=\"...\")."),
        )
        .arg(
            Arg::new("list-themes")
                .long("list-themes")
                .action(ArgAction::SetTrue)
                .help("Display all supported highlighting themes.")
                .long_help("Display a list of supported themes for syntax highlighting."),
        )
        .arg(
            Arg::new("squeeze-blank")
                .long("squeeze-blank")
                .short('s')
                .action(ArgAction::SetTrue)
                .help("Squeeze consecutive empty lines.")
                .long_help("Squeeze consecutive empty lines into a single empty line.")
        )
        .arg(
            Arg::new("squeeze-limit")
                .long("squeeze-limit")
                .value_parser(|s: &str| s.parse::<usize>().map_err(|_| "Requires a non-negative number".to_owned()))
                .long_help("Set the maximum number of consecutive empty lines to be printed.")
                .hide_short_help(true)
        )
        .arg(
            Arg::new("strip-ansi")
                .long("strip-ansi")
                .overrides_with("strip-ansi")
                .value_name("when")
                .value_parser(["auto", "always", "never"])
                .default_value("never")
                .hide_default_value(true)
                .help("Strip colors from the input (auto, always, *never*)")
                .long_help("Specify when to strip ANSI escape sequences from the input. \
                The automatic mode will remove escape sequences unless the syntax highlighting \
                language is plain text. Possible values: auto, always, *never*.")
                .hide_short_help(true)
        )
        .arg(
            Arg::new("style")
                .long("style")
                .action(ArgAction::Append)
                .value_name("components")
                // Cannot use claps built in validation because we have to turn off clap's delimiters
                .value_parser(|val: &str| {
                    match StyleComponentList::from_str(val) {
                        Err(err) => Err(err),
                        Ok(_) => Ok(val.to_owned()),
                    }
                })
                .help(
                    "Comma-separated list of style elements to display \
                     (*default*, auto, full, plain, changes, header, header-filename, header-filesize, grid, rule, numbers, snip).",
                )
                .long_help(
                    "Configure which elements (line numbers, file headers, grid \
                     borders, Git modifications, ..) to display in addition to the \
                     file contents. The argument is a comma-separated list of \
                     components to display (e.g. 'numbers,changes,grid') or a \
                     pre-defined style ('full'). To set a default style, add the \
                     '--style=\"..\"' option to the configuration file or export the \
                     BAT_STYLE environment variable (e.g.: export BAT_STYLE=\"..\").\n\n\
                     When styles are specified in multiple places, the \"nearest\" set \
                     of styles take precedence. The command-line arguments are the highest \
                     priority, followed by the BAT_STYLE environment variable, and then \
                     the configuration file. If any set of styles consists entirely of \
                     components prefixed with \"+\" or \"-\", it will modify the \
                     previous set of styles instead of replacing them.\n\n\
                     By default, the following components are enabled:\n  \
                        changes, grid, header-filename, numbers, snip\n\n\
                     Possible values:\n\n  \
                     * default: enables recommended style components (default).\n  \
                     * full: enables all available components.\n  \
                     * auto: same as 'default', unless the output is piped.\n  \
                     * plain: disables all available components.\n  \
                     * changes: show Git modification markers.\n  \
                     * header: alias for 'header-filename'.\n  \
                     * header-filename: show filenames before the content.\n  \
                     * header-filesize: show file sizes before the content.\n  \
                     * grid: vertical/horizontal lines to separate side bar\n          \
                       and the header from the content.\n  \
                     * rule: horizontal lines to delimit files.\n  \
                     * numbers: show line numbers in the side bar.\n  \
                     * snip: draw separation lines between distinct line ranges.",
                ),
        )
        .arg(
            Arg::new("line-range")
                .long("line-range")
                .short('r')
                .action(ArgAction::Append)
                .value_name("N:M")
                .allow_hyphen_values(true)
                .help("Only print the lines from N to M.")
                .long_help(
                    "Only print the specified range of lines for each file. \
                     For example:\n  \
                     '--line-range 30:40' prints lines 30 to 40\n  \
                     '--line-range :40' prints lines 1 to 40\n  \
                     '--line-range 40:' prints lines 40 to the end of the file\n  \
                     '--line-range 40' only prints line 40\n  \
                     '--line-range -10:' prints the last 10 lines\n  \
                     '--line-range 30:+10' prints lines 30 to 40\n  \
                     '--line-range 35::5' prints lines 30 to 40 (line 35 with 5 lines of context)\n  \
                     '--line-range 30:40:2' prints lines 28 to 42 (range 30-40 with 2 lines of context)",
                ),
        )
        .arg(
            Arg::new("list-languages")
                .long("list-languages")
                .short('L')
                .action(ArgAction::SetTrue)
                .conflicts_with("list-themes")
                .help("Display all supported languages.")
                .long_help("Display a list of supported languages for syntax highlighting."),
        )
        .arg(
            Arg::new("unbuffered")
                .short('u')
                .long("unbuffered")
                .action(ArgAction::SetTrue)
                .help("Enable unbuffered input reading for streaming use cases.")
                .long_help(
                    "Enable unbuffered input reading. When this flag is set, bat will \
                     display data as soon as it is available, without waiting for a \
                     complete line. This is useful for streaming use cases like \
                     'tail -f logfile | bat -u --paging=never'. Note that line numbers \
                     are automatically disabled in unbuffered mode, and syntax \
                     highlighting may be imperfect on partial lines.",
                ),
        )
        .arg(
            Arg::new("no-config")
                .long("no-config")
                .action(ArgAction::SetTrue)
                .hide(true)
                .help("Do not use the configuration file"),
        )
        .arg(
            Arg::new("no-custom-assets")
                .long("no-custom-assets")
                .action(ArgAction::SetTrue)
                .hide(true)
                .help("Do not load custom assets"),
        );

    #[cfg(feature = "application")]
    {
        app = app.arg(
            Arg::new("completion")
            .long("completion")
            .value_name("SHELL")
            .value_parser(["bash", "fish", "ps1", "zsh"])
            .help("Show shell completion for a certain shell. [possible values: bash, fish, zsh, ps1]"),
        );
    }

    #[cfg(feature = "lessopen")]
    {
        app = app
            .arg(
                Arg::new("lessopen")
                    .long("lessopen")
                    .action(ArgAction::SetTrue)
                    .help("Enable the $LESSOPEN preprocessor"),
            )
            .arg(
                Arg::new("no-lessopen")
                    .long("no-lessopen")
                    .action(ArgAction::SetTrue)
                    .overrides_with("lessopen")
                    .hide(true)
                    .help("Disable the $LESSOPEN preprocessor if enabled (overrides --lessopen)"),
            )
    }

    app = app
        .arg(
            Arg::new("config-file")
                .long("config-file")
                .action(ArgAction::SetTrue)
                .conflicts_with("list-languages")
                .conflicts_with("list-themes")
                .hide(true)
                .help("Show path to the configuration file."),
        )
        .arg(
            Arg::new("generate-config-file")
                .long("generate-config-file")
                .action(ArgAction::SetTrue)
                .conflicts_with("list-languages")
                .conflicts_with("list-themes")
                .hide(true)
                .help("Generates a default configuration file."),
        )
        .arg(
            Arg::new("config-dir")
                .long("config-dir")
                .action(ArgAction::SetTrue)
                .hide(true)
                .help("Show bat's configuration directory."),
        )
        .arg(
            Arg::new("cache-dir")
                .long("cache-dir")
                .action(ArgAction::SetTrue)
                .hide(true)
                .help("Show bat's cache directory."),
        )
        .arg(
            Arg::new("diagnostic")
                .long("diagnostic")
                .alias("diagnostics")
                .action(ArgAction::SetTrue)
                .hide_short_help(true)
                .help("Show diagnostic information for bug reports."),
        )
        .arg(
            Arg::new("quiet-empty")
                .long("quiet-empty")
                .short('E')
                .action(ArgAction::SetTrue)
                .help("Produce no output when the input is empty.")
                .long_help(
                    "When this flag is set, bat will produce no output at all when \
                     the input is empty. This is useful when piping commands that may \
                     produce empty output, like 'git diff'.",
                ),
        )
        .arg(
            Arg::new("acknowledgements")
                .long("acknowledgements")
                .action(ArgAction::SetTrue)
                .hide_short_help(true)
                .help("Show acknowledgements."),
        )
        .arg(
            Arg::new("set-terminal-title")
                .long("set-terminal-title")
                .action(ArgAction::SetTrue)
                .hide_short_help(true)
                .help("Sets terminal title to filenames when using a pager."),
        )
        .arg(
            Arg::new("help")
                .short('h')
                .long("help")
                .action(ArgAction::SetTrue)
                .help("Print help (see more with '--help')")
                .long_help("Print help (see a summary with '-h')"),
        )
        .arg(
            Arg::new("version")
                .long("version")
                .short('V')
                .action(ArgAction::Version)
                .help("Print version"),
        );

    // Check if the current directory contains a file name cache. Otherwise,
    // enable the 'bat cache' subcommand.
    if Path::new("cache").exists() {
        app
    } else {
        app.subcommand(
            Command::new("cache")
                .hide(true)
                .about("Modify the syntax-definition and theme cache")
                .arg_required_else_help(true)
                .arg(
                    Arg::new("help")
                        .short('h')
                        .long("help")
                        .action(ArgAction::Help)
                        .help("Print help"),
                )
                .arg(
                    Arg::new("build")
                        .long("build")
                        .short('b')
                        .action(ArgAction::SetTrue)
                        .conflicts_with("clear")
                        .help("Initialize (or update) the syntax/theme cache.")
                        .long_help(
                            "Initialize (or update) the syntax/theme cache by loading from \
                             the source directory (default: the configuration directory).",
                        ),
                )
                .arg(
                    Arg::new("clear")
                        .long("clear")
                        .short('c')
                        .action(ArgAction::SetTrue)
                        .conflicts_with("build")
                        .help("Remove the cached syntax definitions and themes."),
                )
                .arg(
                    Arg::new("source")
                        .long("source")
                        .requires("build")
                        .value_name("dir")
                        .help("Use a different directory to load syntaxes and themes from."),
                )
                .arg(
                    Arg::new("target")
                        .long("target")
                        .requires("build")
                        .value_name("dir")
                        .help(
                            "Use a different directory to store the cached syntax and theme set.",
                        ),
                )
                .arg(
                    Arg::new("blank")
                        .long("blank")
                        .action(ArgAction::SetTrue)
                        .requires("build")
                        .help(
                            "Create completely new syntax and theme sets \
                             (instead of appending to the default sets).",
                        ),
                )
                .arg(
                    Arg::new("acknowledgements")
                        .long("acknowledgements")
                        .action(ArgAction::SetTrue)
                        .requires("build")
                        .help("Build acknowledgements.bin."),
                ),
        )
        .after_long_help(
            "You can use 'bat cache' to customize syntaxes and themes. \
            See 'bat cache --help' for more information",
        )
    }
}
```


#### 📄 檔案: `src/bin/bat/config.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:90, E:104, A:0) ➔ After(N:90, E:104, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 4, +Edges: 4, -Edges: 4, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `[
        ("--tabs", "BAT_TABS"),
        ("--terminal-width", "BAT_WIDTH"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map(|(flag, key)| {
        env::var(key)
            .ok()
            .map(|var| [flag.to_string(), var].join("="))
    })
    .map(|a| a.into())
    .collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `[
        ("--tabs", "BAT_TABS"),
        ("--terminal-width", "BAT_WIDTH"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map(|(flag, key)| {
        env::var(key)
            .ok()
            .map(|var| [flag.to_string(), var].join("="))
    })
    .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `[
        ("--tabs", "BAT_TABS"),
        ("--terminal-width", "BAT_WIDTH"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `[
        ("--tabs", "BAT_TABS"),
        ("--terminal-width", "BAT_WIDTH"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `[
        ("--tabs", "BAT_TABS"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `[
        ("--tabs", "BAT_TABS"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map(|(flag, key)| {
        env::var(key)
            .ok()
            .map(|var| [flag.to_string(), var].join("="))
    })
    .map(|a| a.into())
    .collect (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `[
        ("--tabs", "BAT_TABS"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `[
        ("--tabs", "BAT_TABS"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map(|(flag, key)| {
        env::var(key)
            .ok()
            .map(|var| [flag.to_string(), var].join("="))
    })
    .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `get_args_from_env_vars` ──[CALLS]──> `[
        ("--tabs", "BAT_TABS"),
        ("--terminal-width", "BAT_WIDTH"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map(|(flag, key)| {
        env::var(key)
            .ok()
            .map(|var| [flag.to_string(), var].join("="))
    })
    .map(|a| a.into())
    .collect (External/Unresolved)`
  • + [新增呼叫邊] `get_args_from_env_vars` ──[CALLS]──> `[
        ("--tabs", "BAT_TABS"),
        ("--terminal-width", "BAT_WIDTH"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map(|(flag, key)| {
        env::var(key)
            .ok()
            .map(|var| [flag.to_string(), var].join("="))
    })
    .map (External/Unresolved)`
  • + [新增呼叫邊] `get_args_from_env_vars` ──[CALLS]──> `[
        ("--tabs", "BAT_TABS"),
        ("--terminal-width", "BAT_WIDTH"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map (External/Unresolved)`
  • + [新增呼叫邊] `get_args_from_env_vars` ──[CALLS]──> `[
        ("--tabs", "BAT_TABS"),
        ("--terminal-width", "BAT_WIDTH"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter (External/Unresolved)`
  • - [移除呼叫邊] `get_args_from_env_vars` ──[CALLS]──> `[
        ("--tabs", "BAT_TABS"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map(|(flag, key)| {
        env::var(key)
            .ok()
            .map(|var| [flag.to_string(), var].join("="))
    })
    .map(|a| a.into())
    .collect (External/Unresolved)`
  • - [移除呼叫邊] `get_args_from_env_vars` ──[CALLS]──> `[
        ("--tabs", "BAT_TABS"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map(|(flag, key)| {
        env::var(key)
            .ok()
            .map(|var| [flag.to_string(), var].join("="))
    })
    .map (External/Unresolved)`
  • - [移除呼叫邊] `get_args_from_env_vars` ──[CALLS]──> `[
        ("--tabs", "BAT_TABS"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map (External/Unresolved)`
  • _... 以及其餘 1 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `get_args_from_env_vars()`
- **變更前簽章 (Before)**: `fn get_args_from_env_vars()` (L153~L171)
- **變更後簽章 (After)**: `fn get_args_from_env_vars()` (L153~L172)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn get_args_from_env_vars() -> Vec<OsString> {
    [
        ("--tabs", "BAT_TABS"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map(|(flag, key)| {
        env::var(key)
            .ok()
            .map(|var| [flag.to_string(), var].join("="))
    })
    .map(|a| a.into())
    .collect()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn get_args_from_env_vars() -> Vec<OsString> {
    [
        ("--tabs", "BAT_TABS"),
        ("--terminal-width", "BAT_WIDTH"),
        ("--theme", bat::theme::env::BAT_THEME),
        ("--theme-dark", bat::theme::env::BAT_THEME_DARK),
        ("--theme-light", bat::theme::env::BAT_THEME_LIGHT),
        ("--pager", "BAT_PAGER"),
        ("--paging", "BAT_PAGING"),
        ("--style", "BAT_STYLE"),
    ]
    .iter()
    .filter_map(|(flag, key)| {
        env::var(key)
            .ok()
            .map(|var| [flag.to_string(), var].join("="))
    })
    .map(|a| a.into())
    .collect()
}
```


#### 📄 檔案: `src/bin/bat/main.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:166, E:178, A:1) ➔ After(N:166, E:178, A:1)
- **差分統計**: +Nodes: 6, -Nodes: 6, +Edges: 6, -Edges: 6, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#CLI: main** `(CLI Entry)`
    └── ⚡ **run()**
        └── 🎯 [TRIGGERS] `main()`
            └── 🎯 [CALLS] `default_error_handler (External/Unresolved)()`
            └── 🎯 [CALLS] `process::exit (External/Unresolved)()`
            └── 🎯 [CALLS] `std::io::stderr (External/Unresolved)()`
            └── 🎯 [CALLS] `stderr.lock (External/Unresolved)()`
            └── 🎯 [CALLS] `run()`
                └── 🎯 [CALLS] `App::new (External/Unresolved)()`
                └── 🎯 [CALLS] `Default::default (External/Unresolved)()`
                └── 🎯 [CALLS] `DetectColorScheme::default (External/Unresolved)()`
                └── 🎯 [CALLS] `Ok (External/Unresolved)()`
                └── 🎯 [CALLS] `PROJECT_DIRS.cache_dir (External/Unresolved)()`
                └── 🎯 [CALLS] `PROJECT_DIRS.config_dir (External/Unresolved)()`
                └── 🎯 [CALLS] `StyleComponent::Plain.components (External/Unresolved)()`
                └── 🎯 [CALLS] `StyleComponents::new (External/Unresolved)()`
                └── 🎯 [CALLS] `app.config (External/Unresolved)()`
                └── 🎯 [CALLS] `app.inputs (External/Unresolved)()`
                └── 🎯 [CALLS] `app.matches.get_flag (External/Unresolved)()`
                └── 🎯 [CALLS] `app.matches.get_one::<String> (External/Unresolved)()`
                └── 🎯 [CALLS] `app.matches.subcommand (External/Unresolved)()`
                └── 🎯 [CALLS] `cache_matches.args_present (External/Unresolved)()`
                └── 🎯 [CALLS] `generate_config_file (External/Unresolved)()`
                └── 🎯 [CALLS] `println! (Macro)()`
                └── 🎯 [CALLS] `shell.as_str (External/Unresolved)()`
                └── 🎯 [CALLS] `unreachable! (Macro)()`
                └── 🎯 [CALLS] `vec! (Macro)()`
                └── 🎯 [CALLS] `writeln! (Macro)()`
                └── 🎯 [CALLS] `get_languages()`
                    └── 🎯 [CALLS] `Green.normal (External/Unresolved)()`
                    └── *ref:`Ok (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `Path::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `Path::new("test").with_extension (External/Unresolved)()`
                    └── 🎯 [CALLS] `Path::new(extension).extension (External/Unresolved)()`
                    └── 🎯 [CALLS] `Path::new(extension).extension().is_some (External/Unresolved)()`
                    └── 🎯 [CALLS] `String::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `Style::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `additional_paths.iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `additional_paths.iter().cloned (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter()
        .filter (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter()
        .filter(|syntax| !syntax.hidden && !syntax.file_extensions.is_empty())
        .cloned (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter()
        .filter(|syntax| !syntax.hidden && !syntax.file_extensions.is_empty())
        .cloned()
        .collect::<Vec<_>> (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets.get_syntax_for_path (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets_from_cache_or_binary (External/Unresolved)()`
                    └── 🎯 [CALLS] `comma_separator.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `config.syntax_mapping.all_mappings (External/Unresolved)()`
                    └── 🎯 [CALLS] `configured_languages.get (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.next (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.peek (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.peek().is_some (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.starts_with (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions
                .extend (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions.iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions.iter().peekable (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions.retain (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.name.as_str (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.name.clone (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.name.to_uppercase (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter()
            .map (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter()
            .map(|syntax| syntax.name.len())
            .max (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter()
            .map(|syntax| syntax.name.len())
            .max()
            .unwrap_or (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages.sort_by_key (External/Unresolved)()`
                    └── 🎯 [CALLS] `matches! (Macro)()`
                    └── 🎯 [CALLS] `separator.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `syntax.file_extensions.is_empty (External/Unresolved)()`
                    └── 🎯 [CALLS] `syntax.name.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `word.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `write! (Macro)()`
                    └── 🎯 [CALLS] `write!(result, "\n{:width$}{separator}", "", width = longest).ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `write!(result, "{:width$}{separator}", lang.name, width = longest).ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `write!(result, "{}", style.paint(&word[..])).ok (External/Unresolved)()`
                    └── *ref:`writeln! (Macro)` [已折疊指針]
                    └── 🎯 [CALLS] `writeln!(result, "{}:{}", lang.name, lang.file_extensions.join(",")).ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `get_syntax_mapping_to_paths()`
                        └── 🎯 [CALLS] `HashMap::new (External/Unresolved)()`
                        └── 🎯 [CALLS] `globs.push (External/Unresolved)()`
                        └── 🎯 [CALLS] `map.entry (External/Unresolved)()`
                        └── 🎯 [CALLS] `map.entry(*s).or_insert_with (External/Unresolved)()`
                        └── 🎯 [CALLS] `matcher.glob (External/Unresolved)()`
                        └── 🎯 [CALLS] `matcher.glob().glob (External/Unresolved)()`
                        └── 🎯 [CALLS] `matcher.glob().glob().into (External/Unresolved)()`
                └── 🎯 [CALLS] `invoke_bugreport()`
-                   └── [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info (External/Unresolved)()` [已拆除]
-                   └── [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info (External/Unresolved)()` [已拆除]
-                   └── [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info (External/Unresolved)()` [已拆除]
-                   └── [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info (External/Unresolved)()` [已拆除]
-                   └── [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info (External/Unresolved)()` [已拆除]
-                   └── [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info (External/Unresolved)()` [已拆除]
+                   └── 🟢 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info (External/Unresolved)()` [新增因果]
+                   └── 🟢 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info (External/Unresolved)()` [新增因果]
+                   └── 🟢 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info (External/Unresolved)()` [新增因果]
+                   └── 🟢 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info (External/Unresolved)()` [新增因果]
+                   └── 🟢 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info (External/Unresolved)()` [新增因果]
+                   └── 🟢 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info (External/Unresolved)()` [新增因果]
                    └── 🎯 [CALLS] `"less".to_owned (External/Unresolved)()`
                    └── 🎯 [CALLS] `CommandLine::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `CommandOutput::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `CompileTimeInformation::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `DirectoryEntries::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `EnvironmentVariables::list (External/Unresolved)()`
                    └── 🎯 [CALLS] `FileContent::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `OperatingSystem::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `SoftwareVersion::default (External/Unresolved)()`
                    └── *ref:`app.matches.get_one::<String> (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `app.matches.get_one::<String>("pager").map (External/Unresolved)()`
                    └── 🎯 [CALLS] `bat::config::get_pager_executable (External/Unresolved)()`
                    └── 🎯 [CALLS] `bat::config::get_pager_executable(
        app.matches.get_one::<String>("pager").map(|s| s.as_str()),
    )
    .unwrap_or_else (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport! (Macro)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `cache_dir.to_path_buf (External/Unresolved)()`
                    └── 🎯 [CALLS] `config_file (External/Unresolved)()`
                    └── 🎯 [CALLS] `custom_assets_metadata.push (External/Unresolved)()`
                    └── 🎯 [CALLS] `grep_cli::resolve_binary (External/Unresolved)()`
                    └── 🎯 [CALLS] `report.info (External/Unresolved)()`
                    └── 🎯 [CALLS] `report.print::<Markdown> (External/Unresolved)()`
                    └── 🎯 [CALLS] `s.as_str (External/Unresolved)()`
                    └── 🎯 [CALLS] `system_config_file (External/Unresolved)()`
                └── 🎯 [CALLS] `list_themes()`
                    └── 🎯 [CALLS] `Controller::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `Controller::new(&config, &assets)
                .run(vec![theme_preview_file()], Some(&mut handle))
                .ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `HashSet::new (External/Unresolved)()`
                    └── *ref:`Ok (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `OutputHandle::FmtWrite (External/Unresolved)()`
                    └── 🎯 [CALLS] `OutputType::from_mode (External/Unresolved)()`
                    └── 🎯 [CALLS] `Some (External/Unresolved)()`
                    └── *ref:`String::new (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `StyleComponents (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets.themes (External/Unresolved)()`
                    └── *ref:`assets_from_cache_or_binary (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `cfg.clone (External/Unresolved)()`
                    └── 🎯 [CALLS] `color_scheme (External/Unresolved)()`
                    └── 🎯 [CALLS] `color_scheme(detect_color_scheme).unwrap_or_default (External/Unresolved)()`
                    └── 🎯 [CALLS] `default_theme (External/Unresolved)()`
                    └── 🎯 [CALLS] `format_args! (Macro)()`
                    └── 🎯 [CALLS] `handle.write_fmt (External/Unresolved)()`
                    └── 🎯 [CALLS] `output_type.handle (External/Unresolved)()`
                    └── 🎯 [CALLS] `style.insert (External/Unresolved)()`
                    └── 🎯 [CALLS] `theme.to_string (External/Unresolved)()`
                    └── *ref:`vec! (Macro)` [已折疊指針]
                    └── 🎯 [CALLS] `writer.write_fmt (External/Unresolved)()`
                    └── *ref:`run` [已折疊指針]
                └── 🎯 [CALLS] `run_cache_subcommand()`
                    └── 🎯 [CALLS] `build_assets()`
                        └── 🎯 [CALLS] `bat::assets::build (External/Unresolved)()`
                        └── 🎯 [CALLS] `clap::crate_version! (Macro)()`
                        └── 🎯 [CALLS] `matches
        .get_one::<String> (External/Unresolved)()`
                        └── 🎯 [CALLS] `matches
        .get_one::<String>("source")
        .map (External/Unresolved)()`
                        └── 🎯 [CALLS] `matches
        .get_one::<String>("source")
        .map(Path::new)
        .unwrap_or_else (External/Unresolved)()`
                        └── 🎯 [CALLS] `matches.get_flag (External/Unresolved)()`
                    └── *ref:`Ok (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `clear_assets (External/Unresolved)()`
                    └── *ref:`matches
        .get_one::<String> (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `matches
        .get_one::<String>("target")
        .map (External/Unresolved)()`
                    └── 🎯 [CALLS] `matches
        .get_one::<String>("target")
        .map(Path::new)
        .unwrap_or_else (External/Unresolved)()`
                    └── *ref:`matches.get_flag (External/Unresolved)` [已折疊指針]
                    └── *ref:`println! (Macro)` [已折疊指針]
                └── 🎯 [CALLS] `run_controller()`
                    └── *ref:`Controller::new (External/Unresolved)` [已折疊指針]
                    └── *ref:`assets_from_cache_or_binary (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `get_new_terminal_title()`
                        └── 🎯 [CALLS] `ColorSchemeCollector::description()`
                        └── 🎯 [CALLS] `"bat: ".to_string (External/Unresolved)()`
                        └── 🎯 [CALLS] `input.description().title (External/Unresolved)()`
                        └── 🎯 [CALLS] `inputs.iter (External/Unresolved)()`
                        └── 🎯 [CALLS] `inputs.iter().enumerate (External/Unresolved)()`
                        └── 🎯 [CALLS] `inputs.len (External/Unresolved)()`
                    └── *ref:`run` [已折疊指針]
                    └── 🎯 [CALLS] `set_terminal_title_to()`
                        └── 🎯 [CALLS] `io::stdout (External/Unresolved)()`
                        └── 🎯 [CALLS] `io::stdout().flush (External/Unresolved)()`
                        └── 🎯 [CALLS] `io::stdout().flush().unwrap (External/Unresolved)()`
                        └── 🎯 [CALLS] `print! (Macro)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `invoke_bugreport` ──[CALLS]──> `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info (External/Unresolved)`
  • + [新增呼叫邊] `invoke_bugreport` ──[CALLS]──> `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info (External/Unresolved)`
  • + [新增呼叫邊] `invoke_bugreport` ──[CALLS]──> `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info (External/Unresolved)`
  • _... 以及其餘 9 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `invoke_bugreport()`
- **變更前簽章 (Before)**: `fn invoke_bugreport(app: &App, cache_dir: &Path)` (L287~L365)
- **變更後簽章 (After)**: `fn invoke_bugreport(app: &App, cache_dir: &Path)` (L287~L366)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn invoke_bugreport(app: &App, cache_dir: &Path) {
    use bugreport::{bugreport, collector::*, format::Markdown, report::ReportEntry};

    struct ColorSchemeCollector;

    impl Collector for ColorSchemeCollector {
        fn description(&self) -> &str {
            "Detected terminal color scheme"
        }

        fn collect(
            &mut self,
            _: &bugreport::CrateInfo,
        ) -> std::result::Result<ReportEntry, CollectionError> {
            let color_scheme = bat::theme::color_scheme(bat::theme::DetectColorScheme::Always);
            let text = match color_scheme {
                Some(bat::theme::ColorScheme::Dark) => "dark",
                Some(bat::theme::ColorScheme::Light) => "light",
                None => "not detected",
            };
            Ok(ReportEntry::Text(text.to_string()))
        }
    }
    let pager = bat::config::get_pager_executable(
        app.matches.get_one::<String>("pager").map(|s| s.as_str()),
    )
    .unwrap_or_else(|| "less".to_owned()); // FIXME: Avoid non-canonical path to "less".

    let mut custom_assets_metadata = cache_dir.to_path_buf();
    custom_assets_metadata.push("metadata.yaml");

    let mut report = bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info(CompileTimeInformation::default());

    #[cfg(feature = "paging")]
    if let Ok(resolved_path) = grep_cli::resolve_binary(pager) {
        report = report.info(CommandOutput::new(
            "Less version",
            resolved_path,
            &["--version"],
        ))
    };

    report.print::<Markdown>();
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn invoke_bugreport(app: &App, cache_dir: &Path) {
    use bugreport::{bugreport, collector::*, format::Markdown, report::ReportEntry};

    struct ColorSchemeCollector;

    impl Collector for ColorSchemeCollector {
        fn description(&self) -> &str {
            "Detected terminal color scheme"
        }

        fn collect(
            &mut self,
            _: &bugreport::CrateInfo,
        ) -> std::result::Result<ReportEntry, CollectionError> {
            let color_scheme = bat::theme::color_scheme(bat::theme::DetectColorScheme::Always);
            let text = match color_scheme {
                Some(bat::theme::ColorScheme::Dark) => "dark",
                Some(bat::theme::ColorScheme::Light) => "light",
                None => "not detected",
            };
            Ok(ReportEntry::Text(text.to_string()))
        }
    }
    let pager = bat::config::get_pager_executable(
        app.matches.get_one::<String>("pager").map(|s| s.as_str()),
    )
    .unwrap_or_else(|| "less".to_owned()); // FIXME: Avoid non-canonical path to "less".

    let mut custom_assets_metadata = cache_dir.to_path_buf();
    custom_assets_metadata.push("metadata.yaml");

    let mut report = bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            "BAT_WIDTH",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info(CompileTimeInformation::default());

    #[cfg(feature = "paging")]
    if let Ok(resolved_path) = grep_cli::resolve_binary(pager) {
        report = report.info(CommandOutput::new(
            "Less version",
            resolved_path,
            &["--version"],
        ))
    };

    report.print::<Markdown>();
}
```


---

### 🔹 Commit #14: `ba223289`
- **完整 Hash**: `ba223289ce7325ddb0c95d22b4bf74e2fb7ee3e5`
- **說明 (Ground Truth)**: Update --diagnostic output with detected terminal color scheme type
- **變更檔案數**: 1

#### 📄 檔案: `src/bin/bat/main.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:161, E:173, A:1) ➔ After(N:166, E:178, A:1)
- **差分統計**: +Nodes: 6, -Nodes: 1, +Edges: 6, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#CLI: main** `(CLI Entry)`
    └── ⚡ **run()**
        └── 🎯 [TRIGGERS] `main()`
            └── 🎯 [CALLS] `default_error_handler (External/Unresolved)()`
            └── 🎯 [CALLS] `process::exit (External/Unresolved)()`
            └── 🎯 [CALLS] `std::io::stderr (External/Unresolved)()`
            └── 🎯 [CALLS] `stderr.lock (External/Unresolved)()`
            └── 🎯 [CALLS] `run()`
                └── 🎯 [CALLS] `App::new (External/Unresolved)()`
                └── 🎯 [CALLS] `Default::default (External/Unresolved)()`
                └── 🎯 [CALLS] `DetectColorScheme::default (External/Unresolved)()`
                └── 🎯 [CALLS] `Ok (External/Unresolved)()`
                └── 🎯 [CALLS] `PROJECT_DIRS.cache_dir (External/Unresolved)()`
                └── 🎯 [CALLS] `PROJECT_DIRS.config_dir (External/Unresolved)()`
                └── 🎯 [CALLS] `StyleComponent::Plain.components (External/Unresolved)()`
                └── 🎯 [CALLS] `StyleComponents::new (External/Unresolved)()`
                └── 🎯 [CALLS] `app.config (External/Unresolved)()`
                └── 🎯 [CALLS] `app.inputs (External/Unresolved)()`
                └── 🎯 [CALLS] `app.matches.get_flag (External/Unresolved)()`
                └── 🎯 [CALLS] `app.matches.get_one::<String> (External/Unresolved)()`
                └── 🎯 [CALLS] `app.matches.subcommand (External/Unresolved)()`
                └── 🎯 [CALLS] `cache_matches.args_present (External/Unresolved)()`
                └── 🎯 [CALLS] `generate_config_file (External/Unresolved)()`
                └── 🎯 [CALLS] `println! (Macro)()`
                └── 🎯 [CALLS] `shell.as_str (External/Unresolved)()`
                └── 🎯 [CALLS] `unreachable! (Macro)()`
                └── 🎯 [CALLS] `vec! (Macro)()`
                └── 🎯 [CALLS] `writeln! (Macro)()`
                └── 🎯 [CALLS] `get_languages()`
                    └── 🎯 [CALLS] `Green.normal (External/Unresolved)()`
                    └── *ref:`Ok (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `Path::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `Path::new("test").with_extension (External/Unresolved)()`
                    └── 🎯 [CALLS] `Path::new(extension).extension (External/Unresolved)()`
                    └── 🎯 [CALLS] `Path::new(extension).extension().is_some (External/Unresolved)()`
                    └── 🎯 [CALLS] `String::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `Style::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `additional_paths.iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `additional_paths.iter().cloned (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter()
        .filter (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter()
        .filter(|syntax| !syntax.hidden && !syntax.file_extensions.is_empty())
        .cloned (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets
        .get_syntaxes()?
        .iter()
        .filter(|syntax| !syntax.hidden && !syntax.file_extensions.is_empty())
        .cloned()
        .collect::<Vec<_>> (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets.get_syntax_for_path (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets_from_cache_or_binary (External/Unresolved)()`
                    └── 🎯 [CALLS] `comma_separator.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `config.syntax_mapping.all_mappings (External/Unresolved)()`
                    └── 🎯 [CALLS] `configured_languages.get (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.next (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.peek (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.peek().is_some (External/Unresolved)()`
                    └── 🎯 [CALLS] `extension.starts_with (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions
                .extend (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions.iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions.iter().peekable (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.file_extensions.retain (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.name.as_str (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.name.clone (External/Unresolved)()`
                    └── 🎯 [CALLS] `lang.name.to_uppercase (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter()
            .map (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter()
            .map(|syntax| syntax.name.len())
            .max (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages
            .iter()
            .map(|syntax| syntax.name.len())
            .max()
            .unwrap_or (External/Unresolved)()`
                    └── 🎯 [CALLS] `languages.sort_by_key (External/Unresolved)()`
                    └── 🎯 [CALLS] `matches! (Macro)()`
                    └── 🎯 [CALLS] `separator.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `syntax.file_extensions.is_empty (External/Unresolved)()`
                    └── 🎯 [CALLS] `syntax.name.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `word.len (External/Unresolved)()`
                    └── 🎯 [CALLS] `write! (Macro)()`
                    └── 🎯 [CALLS] `write!(result, "\n{:width$}{separator}", "", width = longest).ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `write!(result, "{:width$}{separator}", lang.name, width = longest).ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `write!(result, "{}", style.paint(&word[..])).ok (External/Unresolved)()`
                    └── *ref:`writeln! (Macro)` [已折疊指針]
                    └── 🎯 [CALLS] `writeln!(result, "{}:{}", lang.name, lang.file_extensions.join(",")).ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `get_syntax_mapping_to_paths()`
                        └── 🎯 [CALLS] `HashMap::new (External/Unresolved)()`
                        └── 🎯 [CALLS] `globs.push (External/Unresolved)()`
                        └── 🎯 [CALLS] `map.entry (External/Unresolved)()`
                        └── 🎯 [CALLS] `map.entry(*s).or_insert_with (External/Unresolved)()`
                        └── 🎯 [CALLS] `matcher.glob (External/Unresolved)()`
                        └── 🎯 [CALLS] `matcher.glob().glob (External/Unresolved)()`
                        └── 🎯 [CALLS] `matcher.glob().glob().into (External/Unresolved)()`
                └── 🎯 [CALLS] `invoke_bugreport()`
+                   └── 🟢 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info (External/Unresolved)()` [新增因果]
                    └── 🎯 [CALLS] `"less".to_owned (External/Unresolved)()`
                    └── 🎯 [CALLS] `CommandLine::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `CommandOutput::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `CompileTimeInformation::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `DirectoryEntries::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `EnvironmentVariables::list (External/Unresolved)()`
                    └── 🎯 [CALLS] `FileContent::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `OperatingSystem::default (External/Unresolved)()`
                    └── 🎯 [CALLS] `SoftwareVersion::default (External/Unresolved)()`
                    └── *ref:`app.matches.get_one::<String> (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `app.matches.get_one::<String>("pager").map (External/Unresolved)()`
                    └── 🎯 [CALLS] `bat::config::get_pager_executable (External/Unresolved)()`
                    └── 🎯 [CALLS] `bat::config::get_pager_executable(
        app.matches.get_one::<String>("pager").map(|s| s.as_str()),
    )
    .unwrap_or_else (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport! (Macro)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info (External/Unresolved)()`
                    └── 🎯 [CALLS] `cache_dir.to_path_buf (External/Unresolved)()`
                    └── 🎯 [CALLS] `config_file (External/Unresolved)()`
                    └── 🎯 [CALLS] `custom_assets_metadata.push (External/Unresolved)()`
                    └── 🎯 [CALLS] `grep_cli::resolve_binary (External/Unresolved)()`
                    └── 🎯 [CALLS] `report.info (External/Unresolved)()`
                    └── 🎯 [CALLS] `report.print::<Markdown> (External/Unresolved)()`
                    └── 🎯 [CALLS] `s.as_str (External/Unresolved)()`
                    └── 🎯 [CALLS] `system_config_file (External/Unresolved)()`
                └── 🎯 [CALLS] `list_themes()`
                    └── 🎯 [CALLS] `Controller::new (External/Unresolved)()`
                    └── 🎯 [CALLS] `Controller::new(&config, &assets)
                .run(vec![theme_preview_file()], Some(&mut handle))
                .ok (External/Unresolved)()`
                    └── 🎯 [CALLS] `HashSet::new (External/Unresolved)()`
                    └── *ref:`Ok (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `OutputHandle::FmtWrite (External/Unresolved)()`
                    └── 🎯 [CALLS] `OutputType::from_mode (External/Unresolved)()`
                    └── 🎯 [CALLS] `Some (External/Unresolved)()`
                    └── *ref:`String::new (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `StyleComponents (External/Unresolved)()`
                    └── 🎯 [CALLS] `assets.themes (External/Unresolved)()`
                    └── *ref:`assets_from_cache_or_binary (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `cfg.clone (External/Unresolved)()`
                    └── 🎯 [CALLS] `color_scheme (External/Unresolved)()`
                    └── 🎯 [CALLS] `color_scheme(detect_color_scheme).unwrap_or_default (External/Unresolved)()`
                    └── 🎯 [CALLS] `default_theme (External/Unresolved)()`
                    └── 🎯 [CALLS] `format_args! (Macro)()`
                    └── 🎯 [CALLS] `handle.write_fmt (External/Unresolved)()`
                    └── 🎯 [CALLS] `output_type.handle (External/Unresolved)()`
                    └── 🎯 [CALLS] `style.insert (External/Unresolved)()`
                    └── 🎯 [CALLS] `theme.to_string (External/Unresolved)()`
                    └── *ref:`vec! (Macro)` [已折疊指針]
                    └── 🎯 [CALLS] `writer.write_fmt (External/Unresolved)()`
                    └── *ref:`run` [已折疊指針]
                └── 🎯 [CALLS] `run_cache_subcommand()`
                    └── 🎯 [CALLS] `build_assets()`
                        └── 🎯 [CALLS] `bat::assets::build (External/Unresolved)()`
                        └── 🎯 [CALLS] `clap::crate_version! (Macro)()`
                        └── 🎯 [CALLS] `matches
        .get_one::<String> (External/Unresolved)()`
                        └── 🎯 [CALLS] `matches
        .get_one::<String>("source")
        .map (External/Unresolved)()`
                        └── 🎯 [CALLS] `matches
        .get_one::<String>("source")
        .map(Path::new)
        .unwrap_or_else (External/Unresolved)()`
                        └── 🎯 [CALLS] `matches.get_flag (External/Unresolved)()`
                    └── *ref:`Ok (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `clear_assets (External/Unresolved)()`
                    └── *ref:`matches
        .get_one::<String> (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `matches
        .get_one::<String>("target")
        .map (External/Unresolved)()`
                    └── 🎯 [CALLS] `matches
        .get_one::<String>("target")
        .map(Path::new)
        .unwrap_or_else (External/Unresolved)()`
                    └── *ref:`matches.get_flag (External/Unresolved)` [已折疊指針]
                    └── *ref:`println! (Macro)` [已折疊指針]
                └── 🎯 [CALLS] `run_controller()`
                    └── *ref:`Controller::new (External/Unresolved)` [已折疊指針]
                    └── *ref:`assets_from_cache_or_binary (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `get_new_terminal_title()`
-                       └── [CALLS] `input.description (External/Unresolved)()` [已拆除]
+                       └── 🟢 [CALLS] `ColorSchemeCollector::description()` [新增因果]
                        └── 🎯 [CALLS] `"bat: ".to_string (External/Unresolved)()`
                        └── 🎯 [CALLS] `input.description().title (External/Unresolved)()`
                        └── 🎯 [CALLS] `inputs.iter (External/Unresolved)()`
                        └── 🎯 [CALLS] `inputs.iter().enumerate (External/Unresolved)()`
                        └── 🎯 [CALLS] `inputs.len (External/Unresolved)()`
                    └── *ref:`run` [已折疊指針]
                    └── 🎯 [CALLS] `set_terminal_title_to()`
                        └── 🎯 [CALLS] `io::stdout (External/Unresolved)()`
                        └── 🎯 [CALLS] `io::stdout().flush (External/Unresolved)()`
                        └── 🎯 [CALLS] `io::stdout().flush().unwrap (External/Unresolved)()`
                        └── 🎯 [CALLS] `print! (Macro)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `ColorSchemeCollector::description` (FUNCTION_DEF)
  • + [新增節點] `text.to_string (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `ReportEntry::Text (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `bat::theme::color_scheme (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `ColorSchemeCollector::collect` (FUNCTION_DEF)
  • - [移除節點] `input.description (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `get_new_terminal_title` ──[CALLS]──> `ColorSchemeCollector::description`
  • + [新增呼叫邊] `invoke_bugreport` ──[CALLS]──> `bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info (External/Unresolved)`
  • + [新增呼叫邊] `ColorSchemeCollector::collect` ──[CALLS]──> `bat::theme::color_scheme (External/Unresolved)`
  • + [新增呼叫邊] `ColorSchemeCollector::collect` ──[CALLS]──> `Ok (External/Unresolved)`
  • + [新增呼叫邊] `ColorSchemeCollector::collect` ──[CALLS]──> `ReportEntry::Text (External/Unresolved)`
  • + [新增呼叫邊] `ColorSchemeCollector::collect` ──[CALLS]──> `text.to_string (External/Unresolved)`
  • - [移除呼叫邊] `get_new_terminal_title` ──[CALLS]──> `input.description (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `invoke_bugreport()`
- **變更前簽章 (Before)**: `fn invoke_bugreport(app: &App, cache_dir: &Path)` (L287~L343)
- **變更後簽章 (After)**: `fn invoke_bugreport(app: &App, cache_dir: &Path)` (L287~L366)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn invoke_bugreport(app: &App, cache_dir: &Path) {
    use bugreport::{bugreport, collector::*, format::Markdown};
    let pager = bat::config::get_pager_executable(
        app.matches.get_one::<String>("pager").map(|s| s.as_str()),
    )
    .unwrap_or_else(|| "less".to_owned()); // FIXME: Avoid non-canonical path to "less".

    let mut custom_assets_metadata = cache_dir.to_path_buf();
    custom_assets_metadata.push("metadata.yaml");

    let mut report = bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(CompileTimeInformation::default());

    #[cfg(feature = "paging")]
    if let Ok(resolved_path) = grep_cli::resolve_binary(pager) {
        report = report.info(CommandOutput::new(
            "Less version",
            resolved_path,
            &["--version"],
        ))
    };

    report.print::<Markdown>();
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn invoke_bugreport(app: &App, cache_dir: &Path) {
    use bugreport::{bugreport, collector::*, format::Markdown, report::ReportEntry};

    struct ColorSchemeCollector;

    impl Collector for ColorSchemeCollector {
        fn description(&self) -> &str {
            "Detected terminal color scheme"
        }

        fn collect(
            &mut self,
            _: &bugreport::CrateInfo,
        ) -> std::result::Result<ReportEntry, CollectionError> {
            let color_scheme =
                bat::theme::color_scheme(bat::theme::DetectColorScheme::Always);
            let text = match color_scheme {
                Some(bat::theme::ColorScheme::Dark) => "dark",
                Some(bat::theme::ColorScheme::Light) => "light",
                None => "not detected",
            };
            Ok(ReportEntry::Text(text.to_string()))
        }
    }
    let pager = bat::config::get_pager_executable(
        app.matches.get_one::<String>("pager").map(|s| s.as_str()),
    )
    .unwrap_or_else(|| "less".to_owned()); // FIXME: Avoid non-canonical path to "less".

    let mut custom_assets_metadata = cache_dir.to_path_buf();
    custom_assets_metadata.push("metadata.yaml");

    let mut report = bugreport!()
        .info(SoftwareVersion::default())
        .info(OperatingSystem::default())
        .info(CommandLine::default())
        .info(EnvironmentVariables::list(&[
            "BAT_CACHE_PATH",
            "BAT_CONFIG_PATH",
            "BAT_OPTS",
            "BAT_PAGER",
            "BAT_PAGING",
            "BAT_STYLE",
            "BAT_TABS",
            "BAT_THEME",
            bat::theme::env::BAT_THEME_DARK,
            bat::theme::env::BAT_THEME_LIGHT,
            "COLORTERM",
            "LANG",
            "LC_ALL",
            "LESS",
            "MANPAGER",
            "NO_COLOR",
            "PAGER",
            "SHELL",
            "TERM",
            "XDG_CACHE_HOME",
            "XDG_CONFIG_HOME",
        ]))
        .info(FileContent::new("System Config file", system_config_file()))
        .info(FileContent::new("Config file", config_file()))
        .info(FileContent::new(
            "Custom assets metadata",
            custom_assets_metadata,
        ))
        .info(DirectoryEntries::new("Custom assets", cache_dir))
        .info(ColorSchemeCollector)
        .info(CompileTimeInformation::default());

    #[cfg(feature = "paging")]
    if let Ok(resolved_path) = grep_cli::resolve_binary(pager) {
        report = report.info(CommandOutput::new(
            "Less version",
            resolved_path,
            &["--version"],
        ))
    };

    report.print::<Markdown>();
}
```


---

### 🔹 Commit #15: `7ff1fb32`
- **完整 Hash**: `7ff1fb3278b756e73a71911d1ae9a702af1c221f`
- **說明 (Ground Truth)**: fix: warn when $LESSCLOSE fails, not when it succeeds
- **變更檔案數**: 1

#### 📄 檔案: `src/lessopen.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:64, E:87, A:0) ➔ After(N:64, E:87, A:0)
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

### 🔹 函式: `Preprocessed::drop()`
- **變更前簽章 (Before)**: `fn Preprocessed::drop(&mut self)` (L252~L268)
- **變更後簽章 (After)**: `fn Preprocessed::drop(&mut self)` (L252~L268)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn drop(&mut self) {
        if let Some(lessclose) = self.lessclose.clone() {
            let mut lessclose_command = shell(lessclose);

            let lessclose_output = match lessclose_command.execute_output() {
                Ok(output) => output,
                Err(_) => {
                    bat_warning!("failed to run $LESSCLOSE to clean up temporary file");
                    return;
                }
            };

            if lessclose_output.status.success() {
                bat_warning!("$LESSCLOSE exited with nonzero exit code",)
            };
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn drop(&mut self) {
        if let Some(lessclose) = self.lessclose.clone() {
            let mut lessclose_command = shell(lessclose);

            let lessclose_output = match lessclose_command.execute_output() {
                Ok(output) => output,
                Err(_) => {
                    bat_warning!("failed to run $LESSCLOSE to clean up temporary file");
                    return;
                }
            };

            if !lessclose_output.status.success() {
                bat_warning!("$LESSCLOSE exited with nonzero exit code",)
            };
        }
    }
```


---

### 🔹 Commit #16: `87e043b9`
- **完整 Hash**: `87e043b91ce47f95829ad74ac06e04d0a163dccf`
- **說明 (Ground Truth)**: Add Home/End key bindings to builtin minus pager
- **變更檔案數**: 1

#### 📄 檔案: `src/output.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:49, E:50, A:0) ➔ After(N:54, E:55, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 0, +Edges: 5, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `minus::input::InputEvent::UpdateUpperMark (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `input_register.add_key_events (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `minus::input::HashedEventRegister::default (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `pager
            .set_input_classifier(Box::new(input_register))
            .expect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `pager
            .set_input_classifier (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `BuiltinPager::new` ──[CALLS]──> `minus::input::HashedEventRegister::default (External/Unresolved)`
  • + [新增呼叫邊] `BuiltinPager::new` ──[CALLS]──> `input_register.add_key_events (External/Unresolved)`
  • + [新增呼叫邊] `BuiltinPager::new` ──[CALLS]──> `minus::input::InputEvent::UpdateUpperMark (External/Unresolved)`
  • + [新增呼叫邊] `BuiltinPager::new` ──[CALLS]──> `pager
            .set_input_classifier(Box::new(input_register))
            .expect (External/Unresolved)`
  • + [新增呼叫邊] `BuiltinPager::new` ──[CALLS]──> `pager
            .set_input_classifier (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `BuiltinPager::new()`
- **變更前簽章 (Before)**: `fn BuiltinPager::new()` (L24~L33)
- **變更後簽章 (After)**: `fn BuiltinPager::new()` (L24~L45)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn new() -> Self {
        let pager = minus::Pager::new();
        let handle = {
            let pager = pager.clone();
            Some(spawn(move || {
                minus::dynamic_paging(pager).map_err(Error::from)
            }))
        };
        Self { pager, handle }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn new() -> Self {
        let pager = minus::Pager::new();

        let mut input_register = minus::input::HashedEventRegister::default();
        input_register.add_key_events(&["home"], |_, _| {
            minus::input::InputEvent::UpdateUpperMark(0)
        });
        input_register.add_key_events(&["end"], |_, _| {
            minus::input::InputEvent::UpdateUpperMark(usize::MAX)
        });
        pager
            .set_input_classifier(Box::new(input_register))
            .expect("failed to set input classifier on newly created pager");

        let handle = {
            let pager = pager.clone();
            Some(spawn(move || {
                minus::dynamic_paging(pager).map_err(Error::from)
            }))
        };
        Self { pager, handle }
    }
```


---

### 🔹 Commit #17: `e60875ac`
- **完整 Hash**: `e60875ac125f6698775679fa9a8beb495299b4e5`
- **說明 (Ground Truth)**: fix: gate Changes component on git feature flag
- **變更檔案數**: 1

#### 📄 檔案: `src/bin/bat/app.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:212, E:246, A:0) ➔ After(N:212, E:246, A:0)
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

### 🔹 函式: `App::forced_style_components()`
- **變更前簽章 (Before)**: `fn App::forced_style_components(&self)` (L573~L607)
- **變更後簽章 (After)**: `fn App::forced_style_components(&self)` (L573~L608)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn forced_style_components(&self) -> Option<StyleComponents> {
        // No components if `--decorations=never``.
        if self
            .matches
            .get_one::<String>("decorations")
            .map(|s| s.as_str())
            == Some("never")
        {
            return Some(StyleComponents(HashSet::new()));
        }

        // Only line numbers if `--number`.
        if self.matches.get_flag("number") {
            return Some(StyleComponents(HashSet::from([
                StyleComponent::LineNumbers,
            ])));
        }

        // Plain if `--plain` is specified at least once.
        if self.matches.get_count("plain") > 0 {
            let mut components = HashSet::from([StyleComponent::Plain]);
            // When --diff is active, preserve change markers and snip separators
            // so that diff output remains visually useful.
            if self.matches.try_contains_id("diff").unwrap_or_default()
                && self.matches.get_flag("diff")
            {
                components.insert(StyleComponent::Changes);
                components.insert(StyleComponent::Snip);
            }
            return Some(StyleComponents(components));
        }

        // Default behavior.
        None
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn forced_style_components(&self) -> Option<StyleComponents> {
        // No components if `--decorations=never``.
        if self
            .matches
            .get_one::<String>("decorations")
            .map(|s| s.as_str())
            == Some("never")
        {
            return Some(StyleComponents(HashSet::new()));
        }

        // Only line numbers if `--number`.
        if self.matches.get_flag("number") {
            return Some(StyleComponents(HashSet::from([
                StyleComponent::LineNumbers,
            ])));
        }

        // Plain if `--plain` is specified at least once.
        if self.matches.get_count("plain") > 0 {
            let mut components = HashSet::from([StyleComponent::Plain]);
            // When --diff is active, preserve change markers and snip separators
            // so that diff output remains visually useful.
            if self.matches.try_contains_id("diff").unwrap_or_default()
                && self.matches.get_flag("diff")
            {
                #[cfg(feature = "git")]
                components.insert(StyleComponent::Changes);
                components.insert(StyleComponent::Snip);
            }
            return Some(StyleComponents(components));
        }

        // Default behavior.
        None
    }
```


---

### 🔹 Commit #18: `fc94a0ec`
- **完整 Hash**: `fc94a0ec49dcea3d5c022d38299f82b1f894f844`
- **說明 (Ground Truth)**: fix: account for caret notation width in text wrapping
- **變更檔案數**: 1

#### 📄 檔案: `src/printer.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:160, E:190, A:0) ➔ After(N:160, E:190, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 5, +Edges: 7, -Edges: 7, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `char_width` (FUNCTION_DEF)
  • + [新增節點] `remainder.chars (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `remainder.chars().map(char_width).sum (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `c.is_control (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `remainder.chars().map (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `ch.width().unwrap_or (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `remainder
                                            .chars()
                                            .map(|ch| ch.width().unwrap_or(0))
                                            .sum (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `remainder
                                            .chars (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `ch.width (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `remainder
                                            .chars()
                                            .map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `char_width` ──[CALLS]──> `c.width().unwrap_or (External/Unresolved)`
  • + [新增呼叫邊] `char_width` ──[CALLS]──> `c.width (External/Unresolved)`
  • + [新增呼叫邊] `char_width` ──[CALLS]──> `c.is_control (External/Unresolved)`
  • + [新增呼叫邊] `InteractivePrinter::print_line` ──[CALLS]──> `char_width`
  • + [新增呼叫邊] `InteractivePrinter::print_line` ──[CALLS]──> `remainder.chars().map(char_width).sum (External/Unresolved)`
  • _... 以及其餘 9 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `InteractivePrinter::print_line()`
- **變更前簽章 (Before)**: `fn InteractivePrinter::print_line(
        &mut self,
        out_of_range: bool,
        handle: &mut OutputHandle,
        line_number: usize,
        line_buffer: &[u8],
        max_buffered_line_number: MaxBufferedLineNumber,
    )` (L609~L934)
- **變更後簽章 (After)**: `fn InteractivePrinter::print_line(
        &mut self,
        out_of_range: bool,
        handle: &mut OutputHandle,
        line_number: usize,
        line_buffer: &[u8],
        max_buffered_line_number: MaxBufferedLineNumber,
    )` (L619~L942)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn print_line(
        &mut self,
        out_of_range: bool,
        handle: &mut OutputHandle,
        line_number: usize,
        line_buffer: &[u8],
        max_buffered_line_number: MaxBufferedLineNumber,
    ) -> Result<()> {
        let line = if self.config.show_nonprintable {
            replace_nonprintable(
                line_buffer,
                self.config.tab_width,
                self.config.nonprintable_notation,
            )
            .into()
        } else {
            let mut line = match self.content_type {
                Some(ContentType::BINARY) | None
                    if !matches!(self.config.binary, BinaryBehavior::AsText) =>
                {
                    return Ok(());
                }
                Some(ContentType::UTF_16LE) => UTF_16LE.decode_with_bom_removal(line_buffer).0,
                Some(ContentType::UTF_16BE) => UTF_16BE.decode_with_bom_removal(line_buffer).0,
                _ => {
                    let line = String::from_utf8_lossy(line_buffer);
                    if line_number == 1 {
                        match line.strip_prefix('\u{feff}') {
                            Some(stripped) => stripped.to_string().into(),
                            None => line,
                        }
                    } else {
                        line
                    }
                }
            };

            if self.strip_overstrike {
                if let Some(pos) = line.find('\x08') {
                    line = strip_overstrike(&line, pos).into();
                }
            }

            // If ANSI escape sequences are supposed to be stripped, do it before syntax highlighting.
            if self.strip_ansi {
                line = strip_ansi(&line).into()
            }

            line
        };

        let regions = self.highlight_regions_for_line(&line)?;
        if out_of_range {
            return Ok(());
        }

        // Skip squeezed lines.
        if let Some(squeeze_limit) = self.config.squeeze_lines {
            if line.trim_end_matches(['\r', '\n']).is_empty() {
                self.consecutive_empty_lines += 1;
                if self.consecutive_empty_lines > squeeze_limit {
                    return Ok(());
                }
            } else {
                self.consecutive_empty_lines = 0;
            }
        }

        let mut cursor: usize = 0;
        let mut cursor_max: usize = self.config.term_width;
        let mut cursor_total: usize = 0;
        let mut panel_wrap: Option<String> = None;

        // Line highlighting
        let highlight_this_line = self
            .config
            .highlighted_lines
            .0
            .check(line_number, max_buffered_line_number)
            == RangeCheckResult::InRange;

        if highlight_this_line && self.config.theme == "ansi" {
            self.ansi_style.update(ANSI_UNDERLINE_ENABLE);
        }

        let background_color = self
            .background_color_highlight
            .filter(|_| highlight_this_line);

        // Line decorations.
        if self.panel_width > 0 {
            let decorations = self
                .decorations
                .iter()
                .map(|d| d.generate(line_number, false, self));

            for deco in decorations {
                write!(handle, "{} ", deco.text)?;
                cursor_max -= deco.width + 1;
            }
        }

        // Line contents.
        if matches!(self.config.wrapping_mode, WrappingMode::NoWrapping(_)) {
            let true_color = self.config.true_color;
            let colored_output = self.config.colored_output;
            let italics = self.config.use_italic_text;

            for &(style, region) in &regions {
                let ansi_iterator = EscapeSequenceIterator::new(region);
                for chunk in ansi_iterator {
                    match chunk {
                        // Regular text.
                        EscapeSequence::Text(text) => {
                            let text = self.preprocess(text, &mut cursor_total);
                            let text_trimmed = text.trim_end_matches(['\r', '\n']);

                            write!(
                                handle,
                                "{}{}",
                                as_terminal_escaped(
                                    style,
                                    &format!("{}{text_trimmed}", self.ansi_style),
                                    true_color,
                                    colored_output,
                                    italics,
                                    background_color
                                ),
                                self.ansi_style.to_reset_sequence(),
                            )?;

                            // Pad the rest of the line.
                            if text.len() != text_trimmed.len() {
                                if let Some(background_color) = background_color {
                                    let ansi_style = Style {
                                        background: to_ansi_color(background_color, true_color),
                                        ..Default::default()
                                    };

                                    let width = if cursor_total <= cursor_max {
                                        cursor_max - cursor_total + 1
                                    } else {
                                        0
                                    };
                                    write!(handle, "{}", ansi_style.paint(" ".repeat(width)))?;
                                }
                                write!(handle, "{}", &text[text_trimmed.len()..])?;
                            }
                        }

                        // ANSI escape passthrough.
                        _ => {
                            write!(handle, "{}", chunk.raw())?;
                            self.ansi_style.update(chunk);
                        }
                    }
                }
            }

            if !self.config.style_components.plain() && line.bytes().next_back() != Some(b'\n') {
                writeln!(handle)?;
            }
        } else {
            for &(style, region) in &regions {
                let ansi_iterator = EscapeSequenceIterator::new(region);
                for chunk in ansi_iterator {
                    match chunk {
                        // Regular text.
                        EscapeSequence::Text(text) => {
                            let text = self
                                .preprocess(text.trim_end_matches(['\r', '\n']), &mut cursor_total);

                            let mut max_width = cursor_max - cursor;

                            // line buffer (avoid calling write! for every character)
                            let mut line_buf = String::with_capacity(max_width * 4);

                            // Displayed width of line_buf
                            let mut current_width = 0;

                            let word_wrap = matches!(self.config.wrapping_mode, WrappingMode::Word);

                            // For word wrapping, track last whitespace position.
                            let mut last_ws_idx: Option<usize> = None;

                            for c in text.chars() {
                                // calculate the displayed width for next character
                                let cw = c.width().unwrap_or(0);
                                current_width += cw;

                                // Track whitespace positions for word wrapping.
                                if word_wrap && c.is_whitespace() {
                                    last_ws_idx = Some(line_buf.len());
                                }

                                // if next character cannot be printed on this line,
                                // flush the buffer.
                                if current_width > max_width {
                                    // Generate wrap padding if not already generated.
                                    if panel_wrap.is_none() {
                                        panel_wrap = if self.panel_width > 0 {
                                            Some(format!(
                                                "{} ",
                                                self.decorations
                                                    .iter()
                                                    .map(|d| d
                                                        .generate(line_number, true, self)
                                                        .text)
                                                    .collect::<Vec<String>>()
                                                    .join(" ")
                                            ))
                                        } else {
                                            Some("".to_string())
                                        }
                                    }

                                    // Determine the break point and remainder
                                    // for word wrapping.
                                    let (emit_end, rest_start) = if word_wrap {
                                        if let Some(ws_idx) = last_ws_idx {
                                            // Skip the whitespace character itself
                                            // and carry the rest to the next line.
                                            let rs = ws_idx
                                                + line_buf[ws_idx..]
                                                    .chars()
                                                    .next()
                                                    .map(|ch| ch.len_utf8())
                                                    .unwrap_or(0);
                                            (ws_idx, Some(rs))
                                        } else {
                                            (line_buf.len(), None)
                                        }
                                    } else {
                                        (line_buf.len(), None)
                                    };

                                    // It wraps.
                                    write!(
                                        handle,
                                        "{}{}\n{}",
                                        as_terminal_escaped(
                                            style,
                                            &format!(
                                                "{}{}",
                                                self.ansi_style,
                                                &line_buf[..emit_end]
                                            ),
                                            self.config.true_color,
                                            self.config.colored_output,
                                            self.config.use_italic_text,
                                            background_color
                                        ),
                                        self.ansi_style.to_reset_sequence(),
                                        panel_wrap.clone().unwrap()
                                    )?;

                                    cursor = 0;
                                    max_width = cursor_max;

                                    if let Some(rs) = rest_start {
                                        // Word wrap: carry remainder to next line.
                                        let remainder = line_buf[rs..].to_string();
                                        let rem_width: usize = remainder
                                            .chars()
                                            .map(|ch| ch.width().unwrap_or(0))
                                            .sum();
                                        line_buf.clear();
                                        line_buf.push_str(&remainder);
                                        current_width = rem_width + cw;
                                    } else {
                                        line_buf.clear();
                                        current_width = cw;
                                    }
                                    last_ws_idx = None;
                                }

                                line_buf.push(c);
                            }

                            // flush the buffer
                            cursor += current_width;
                            write!(
                                handle,
                                "{}",
                                as_terminal_escaped(
                                    style,
                                    &format!("{}{line_buf}", self.ansi_style),
                                    self.config.true_color,
                                    self.config.colored_output,
                                    self.config.use_italic_text,
                                    background_color
                                )
                            )?;
                        }

                        // ANSI escape passthrough.
                        _ => {
                            write!(handle, "{}", chunk.raw())?;
                            self.ansi_style.update(chunk);
                        }
                    }
                }
            }

            if let Some(background_color) = background_color {
                let ansi_style = Style {
                    background: to_ansi_color(background_color, self.config.true_color),
                    ..Default::default()
                };

                write!(
                    handle,
                    "{}",
                    ansi_style.paint(" ".repeat(cursor_max - cursor))
                )?;
            }
            writeln!(handle)?;
        }

        if highlight_this_line && self.config.theme == "ansi" {
            write!(handle, "{}", ANSI_UNDERLINE_DISABLE.raw())?;
            self.ansi_style.update(ANSI_UNDERLINE_DISABLE);
        }

        Ok(())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn print_line(
        &mut self,
        out_of_range: bool,
        handle: &mut OutputHandle,
        line_number: usize,
        line_buffer: &[u8],
        max_buffered_line_number: MaxBufferedLineNumber,
    ) -> Result<()> {
        let line = if self.config.show_nonprintable {
            replace_nonprintable(
                line_buffer,
                self.config.tab_width,
                self.config.nonprintable_notation,
            )
            .into()
        } else {
            let mut line = match self.content_type {
                Some(ContentType::BINARY) | None
                    if !matches!(self.config.binary, BinaryBehavior::AsText) =>
                {
                    return Ok(());
                }
                Some(ContentType::UTF_16LE) => UTF_16LE.decode_with_bom_removal(line_buffer).0,
                Some(ContentType::UTF_16BE) => UTF_16BE.decode_with_bom_removal(line_buffer).0,
                _ => {
                    let line = String::from_utf8_lossy(line_buffer);
                    if line_number == 1 {
                        match line.strip_prefix('\u{feff}') {
                            Some(stripped) => stripped.to_string().into(),
                            None => line,
                        }
                    } else {
                        line
                    }
                }
            };

            if self.strip_overstrike {
                if let Some(pos) = line.find('\x08') {
                    line = strip_overstrike(&line, pos).into();
                }
            }

            // If ANSI escape sequences are supposed to be stripped, do it before syntax highlighting.
            if self.strip_ansi {
                line = strip_ansi(&line).into()
            }

            line
        };

        let regions = self.highlight_regions_for_line(&line)?;
        if out_of_range {
            return Ok(());
        }

        // Skip squeezed lines.
        if let Some(squeeze_limit) = self.config.squeeze_lines {
            if line.trim_end_matches(['\r', '\n']).is_empty() {
                self.consecutive_empty_lines += 1;
                if self.consecutive_empty_lines > squeeze_limit {
                    return Ok(());
                }
            } else {
                self.consecutive_empty_lines = 0;
            }
        }

        let mut cursor: usize = 0;
        let mut cursor_max: usize = self.config.term_width;
        let mut cursor_total: usize = 0;
        let mut panel_wrap: Option<String> = None;

        // Line highlighting
        let highlight_this_line = self
            .config
            .highlighted_lines
            .0
            .check(line_number, max_buffered_line_number)
            == RangeCheckResult::InRange;

        if highlight_this_line && self.config.theme == "ansi" {
            self.ansi_style.update(ANSI_UNDERLINE_ENABLE);
        }

        let background_color = self
            .background_color_highlight
            .filter(|_| highlight_this_line);

        // Line decorations.
        if self.panel_width > 0 {
            let decorations = self
                .decorations
                .iter()
                .map(|d| d.generate(line_number, false, self));

            for deco in decorations {
                write!(handle, "{} ", deco.text)?;
                cursor_max -= deco.width + 1;
            }
        }

        // Line contents.
        if matches!(self.config.wrapping_mode, WrappingMode::NoWrapping(_)) {
            let true_color = self.config.true_color;
            let colored_output = self.config.colored_output;
            let italics = self.config.use_italic_text;

            for &(style, region) in &regions {
                let ansi_iterator = EscapeSequenceIterator::new(region);
                for chunk in ansi_iterator {
                    match chunk {
                        // Regular text.
                        EscapeSequence::Text(text) => {
                            let text = self.preprocess(text, &mut cursor_total);
                            let text_trimmed = text.trim_end_matches(['\r', '\n']);

                            write!(
                                handle,
                                "{}{}",
                                as_terminal_escaped(
                                    style,
                                    &format!("{}{text_trimmed}", self.ansi_style),
                                    true_color,
                                    colored_output,
                                    italics,
                                    background_color
                                ),
                                self.ansi_style.to_reset_sequence(),
                            )?;

                            // Pad the rest of the line.
                            if text.len() != text_trimmed.len() {
                                if let Some(background_color) = background_color {
                                    let ansi_style = Style {
                                        background: to_ansi_color(background_color, true_color),
                                        ..Default::default()
                                    };

                                    let width = if cursor_total <= cursor_max {
                                        cursor_max - cursor_total + 1
                                    } else {
                                        0
                                    };
                                    write!(handle, "{}", ansi_style.paint(" ".repeat(width)))?;
                                }
                                write!(handle, "{}", &text[text_trimmed.len()..])?;
                            }
                        }

                        // ANSI escape passthrough.
                        _ => {
                            write!(handle, "{}", chunk.raw())?;
                            self.ansi_style.update(chunk);
                        }
                    }
                }
            }

            if !self.config.style_components.plain() && line.bytes().next_back() != Some(b'\n') {
                writeln!(handle)?;
            }
        } else {
            for &(style, region) in &regions {
                let ansi_iterator = EscapeSequenceIterator::new(region);
                for chunk in ansi_iterator {
                    match chunk {
                        // Regular text.
                        EscapeSequence::Text(text) => {
                            let text = self
                                .preprocess(text.trim_end_matches(['\r', '\n']), &mut cursor_total);

                            let mut max_width = cursor_max - cursor;

                            // line buffer (avoid calling write! for every character)
                            let mut line_buf = String::with_capacity(max_width * 4);

                            // Displayed width of line_buf
                            let mut current_width = 0;

                            let word_wrap = matches!(self.config.wrapping_mode, WrappingMode::Word);

                            // For word wrapping, track last whitespace position.
                            let mut last_ws_idx: Option<usize> = None;

                            for c in text.chars() {
                                // calculate the displayed width for next character
                                let cw = char_width(c);
                                current_width += cw;

                                // Track whitespace positions for word wrapping.
                                if word_wrap && c.is_whitespace() {
                                    last_ws_idx = Some(line_buf.len());
                                }

                                // if next character cannot be printed on this line,
                                // flush the buffer.
                                if current_width > max_width {
                                    // Generate wrap padding if not already generated.
                                    if panel_wrap.is_none() {
                                        panel_wrap = if self.panel_width > 0 {
                                            Some(format!(
                                                "{} ",
                                                self.decorations
                                                    .iter()
                                                    .map(|d| d
                                                        .generate(line_number, true, self)
                                                        .text)
                                                    .collect::<Vec<String>>()
                                                    .join(" ")
                                            ))
                                        } else {
                                            Some("".to_string())
                                        }
                                    }

                                    // Determine the break point and remainder
                                    // for word wrapping.
                                    let (emit_end, rest_start) = if word_wrap {
                                        if let Some(ws_idx) = last_ws_idx {
                                            // Skip the whitespace character itself
                                            // and carry the rest to the next line.
                                            let rs = ws_idx
                                                + line_buf[ws_idx..]
                                                    .chars()
                                                    .next()
                                                    .map(|ch| ch.len_utf8())
                                                    .unwrap_or(0);
                                            (ws_idx, Some(rs))
                                        } else {
                                            (line_buf.len(), None)
                                        }
                                    } else {
                                        (line_buf.len(), None)
                                    };

                                    // It wraps.
                                    write!(
                                        handle,
                                        "{}{}\n{}",
                                        as_terminal_escaped(
                                            style,
                                            &format!(
                                                "{}{}",
                                                self.ansi_style,
                                                &line_buf[..emit_end]
                                            ),
                                            self.config.true_color,
                                            self.config.colored_output,
                                            self.config.use_italic_text,
                                            background_color
                                        ),
                                        self.ansi_style.to_reset_sequence(),
                                        panel_wrap.clone().unwrap()
                                    )?;

                                    cursor = 0;
                                    max_width = cursor_max;

                                    if let Some(rs) = rest_start {
                                        // Word wrap: carry remainder to next line.
                                        let remainder = line_buf[rs..].to_string();
                                        let rem_width: usize =
                                            remainder.chars().map(char_width).sum();
                                        line_buf.clear();
                                        line_buf.push_str(&remainder);
                                        current_width = rem_width + cw;
                                    } else {
                                        line_buf.clear();
                                        current_width = cw;
                                    }
                                    last_ws_idx = None;
                                }

                                line_buf.push(c);
                            }

                            // flush the buffer
                            cursor += current_width;
                            write!(
                                handle,
                                "{}",
                                as_terminal_escaped(
                                    style,
                                    &format!("{}{line_buf}", self.ansi_style),
                                    self.config.true_color,
                                    self.config.colored_output,
                                    self.config.use_italic_text,
                                    background_color
                                )
                            )?;
                        }

                        // ANSI escape passthrough.
                        _ => {
                            write!(handle, "{}", chunk.raw())?;
                            self.ansi_style.update(chunk);
                        }
                    }
                }
            }

            if let Some(background_color) = background_color {
                let ansi_style = Style {
                    background: to_ansi_color(background_color, self.config.true_color),
                    ..Default::default()
                };

                write!(
                    handle,
                    "{}",
                    ansi_style.paint(" ".repeat(cursor_max - cursor))
                )?;
            }
            writeln!(handle)?;
        }

        if highlight_this_line && self.config.theme == "ansi" {
            write!(handle, "{}", ANSI_UNDERLINE_DISABLE.raw())?;
            self.ansi_style.update(ANSI_UNDERLINE_DISABLE);
        }

        Ok(())
    }
```


---

### 🔹 Commit #19: `2a29802d`
- **完整 Hash**: `2a29802dd57a202589e555e896432575225fe76b`
- **說明 (Ground Truth)**: Refactor: string-or-struct matcher syntax, Case enum, remove case_sensitive_mappings table
- **變更檔案數**: 2

#### 📄 檔案: `src/syntax_mapping.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:63, E:79, A:0) ➔ After(N:64, E:80, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 3, +Edges: 4, -Edges: 3, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `GlobBuilder::new(from)
        .case_insensitive(matches!(case, Case::Insensitive))
        .literal_separator(true)
        .build (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `GlobBuilder::new(from)
        .case_insensitive(matches!(case, Case::Insensitive))
        .literal_separator(true)
        .build()?
        .compile_matcher (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `matches! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `GlobBuilder::new(from)
        .case_insensitive(matches!(case, Case::Insensitive))
        .literal_separator (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator(true)
        .build (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator(true)
        .build()?
        .compile_matcher (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `make_glob_matcher` ──[CALLS]──> `GlobBuilder::new(from)
        .case_insensitive(matches!(case, Case::Insensitive))
        .literal_separator(true)
        .build()?
        .compile_matcher (External/Unresolved)`
  • + [新增呼叫邊] `make_glob_matcher` ──[CALLS]──> `GlobBuilder::new(from)
        .case_insensitive(matches!(case, Case::Insensitive))
        .literal_separator(true)
        .build (External/Unresolved)`
  • + [新增呼叫邊] `make_glob_matcher` ──[CALLS]──> `GlobBuilder::new(from)
        .case_insensitive(matches!(case, Case::Insensitive))
        .literal_separator (External/Unresolved)`
  • + [新增呼叫邊] `make_glob_matcher` ──[CALLS]──> `matches! (Macro)`
  • - [移除呼叫邊] `make_glob_matcher` ──[CALLS]──> `GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator(true)
        .build()?
        .compile_matcher (External/Unresolved)`
  • - [移除呼叫邊] `make_glob_matcher` ──[CALLS]──> `GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator(true)
        .build (External/Unresolved)`
  • - [移除呼叫邊] `make_glob_matcher` ──[CALLS]──> `GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `make_glob_matcher()`
- **變更前簽章 (Before)**: `fn make_glob_matcher(from: &str, case_insensitive: bool)` (L20~L27)
- **變更後簽章 (After)**: `fn make_glob_matcher(from: &str, case: Case)` (L27~L34)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn make_glob_matcher(from: &str, case_insensitive: bool) -> Result<GlobMatcher> {
    let matcher = GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator(true)
        .build()?
        .compile_matcher();
    Ok(matcher)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn make_glob_matcher(from: &str, case: Case) -> Result<GlobMatcher> {
    let matcher = GlobBuilder::new(from)
        .case_insensitive(matches!(case, Case::Insensitive))
        .literal_separator(true)
        .build()?
        .compile_matcher();
    Ok(matcher)
}
```

### 🔹 函式: `SyntaxMapping::insert_case_sensitive()`
- **變更前簽章 (Before)**: `fn SyntaxMapping::insert_case_sensitive(&mut self, from: &str, to: MappingTarget<'a>)` (L106~L110)
- **變更後簽章 (After)**: `fn SyntaxMapping::insert_case_sensitive(&mut self, from: &str, to: MappingTarget<'a>)` (L113~L117)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn insert_case_sensitive(&mut self, from: &str, to: MappingTarget<'a>) -> Result<()> {
        let matcher = make_glob_matcher(from, false)?;
        self.custom_mappings.push((matcher, to));
        Ok(())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn insert_case_sensitive(&mut self, from: &str, to: MappingTarget<'a>) -> Result<()> {
        let matcher = make_glob_matcher(from, Case::Sensitive)?;
        self.custom_mappings.push((matcher, to));
        Ok(())
    }
```

### 🔹 函式: `SyntaxMapping::insert()`
- **變更前簽章 (Before)**: `fn SyntaxMapping::insert(&mut self, from: &str, to: MappingTarget<'a>)` (L99~L103)
- **變更後簽章 (After)**: `fn SyntaxMapping::insert(&mut self, from: &str, to: MappingTarget<'a>)` (L106~L110)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn insert(&mut self, from: &str, to: MappingTarget<'a>) -> Result<()> {
        let matcher = make_glob_matcher(from, true)?;
        self.custom_mappings.push((matcher, to));
        Ok(())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn insert(&mut self, from: &str, to: MappingTarget<'a>) -> Result<()> {
        let matcher = make_glob_matcher(from, Case::Insensitive)?;
        self.custom_mappings.push((matcher, to));
        Ok(())
    }
```


#### 📄 檔案: `src/syntax_mapping/builtin.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:10, E:9, A:0) ➔ After(N:10, E:9, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 2, +Edges: 2, -Edges: 2, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `make_glob_matcher(from, case)
        .expect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `make_glob_matcher(&buf, case).ok (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `make_glob_matcher(from, case_insensitive)
        .expect (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `make_glob_matcher(&buf, case_insensitive).ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `build_matcher_fixed` ──[CALLS]──> `make_glob_matcher(from, case)
        .expect (External/Unresolved)`
  • + [新增呼叫邊] `build_matcher_dynamic` ──[CALLS]──> `make_glob_matcher(&buf, case).ok (External/Unresolved)`
  • - [移除呼叫邊] `build_matcher_fixed` ──[CALLS]──> `make_glob_matcher(from, case_insensitive)
        .expect (External/Unresolved)`
  • - [移除呼叫邊] `build_matcher_dynamic` ──[CALLS]──> `make_glob_matcher(&buf, case_insensitive).ok (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `build_matcher_fixed()`
- **變更前簽章 (Before)**: `fn build_matcher_fixed(from: &str, case_insensitive: bool)` (L56~L59)
- **變更後簽章 (After)**: `fn build_matcher_fixed(from: &str, case: Case)` (L56~L59)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn build_matcher_fixed(from: &str, case_insensitive: bool) -> GlobMatcher {
    make_glob_matcher(from, case_insensitive)
        .expect("A builtin fixed glob matcher failed to compile")
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn build_matcher_fixed(from: &str, case: Case) -> GlobMatcher {
    make_glob_matcher(from, case)
        .expect("A builtin fixed glob matcher failed to compile")
}
```

### 🔹 函式: `build_matcher_dynamic()`
- **變更前簽章 (Before)**: `fn build_matcher_dynamic(segs: &[MatcherSegment], case_insensitive: bool)` (L68~L83)
- **變更後簽章 (After)**: `fn build_matcher_dynamic(segs: &[MatcherSegment], case: Case)` (L68~L83)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn build_matcher_dynamic(segs: &[MatcherSegment], case_insensitive: bool) -> Option<GlobMatcher> {
    // join segments
    let mut buf = String::new();
    for seg in segs {
        match seg {
            MatcherSegment::Text(s) => buf.push_str(s),
            MatcherSegment::Env(var) => {
                let replaced = env::var(var).ok()?;
                buf.push_str(&replaced);
            }
        }
    }
    // compile glob matcher
    let matcher = make_glob_matcher(&buf, case_insensitive).ok()?;
    Some(matcher)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn build_matcher_dynamic(segs: &[MatcherSegment], case: Case) -> Option<GlobMatcher> {
    // join segments
    let mut buf = String::new();
    for seg in segs {
        match seg {
            MatcherSegment::Text(s) => buf.push_str(s),
            MatcherSegment::Env(var) => {
                let replaced = env::var(var).ok()?;
                buf.push_str(&replaced);
            }
        }
    }
    // compile glob matcher
    let matcher = make_glob_matcher(&buf, case).ok()?;
    Some(matcher)
}
```


---

### 🔹 Commit #20: `56fe0fa2`
- **完整 Hash**: `56fe0fa2260675c2603607ac35c4c367e5d8d797`
- **說明 (Ground Truth)**: Add case-sensitive glob support to syntax mapping
- **變更檔案數**: 2

#### 📄 檔案: `src/syntax_mapping.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:59, E:69, A:0) ➔ After(N:63, E:79, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 3, +Edges: 13, -Edges: 3, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator(true)
        .build (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator(true)
        .build()?
        .compile_matcher (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `map.insert_case_sensitive("MY_SPECIAL_FILE", MappingTarget::MapTo("Python"))
            .ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `SyntaxMapping::insert_case_sensitive` (FUNCTION_DEF)
  • + [新增節點] `case_sensitive_custom_mappings_work` (FUNCTION_DEF)
  • + [新增節點] `builtin_mappings_build_is_case_sensitive` (FUNCTION_DEF)
  • - [移除節點] `GlobBuilder::new(from)
        .case_insensitive(true)
        .literal_separator(true)
        .build()?
        .compile_matcher (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `GlobBuilder::new(from)
        .case_insensitive(true)
        .literal_separator(true)
        .build (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `GlobBuilder::new(from)
        .case_insensitive(true)
        .literal_separator (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `make_glob_matcher` ──[CALLS]──> `GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator(true)
        .build()?
        .compile_matcher (External/Unresolved)`
  • + [新增呼叫邊] `make_glob_matcher` ──[CALLS]──> `GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator(true)
        .build (External/Unresolved)`
  • + [新增呼叫邊] `make_glob_matcher` ──[CALLS]──> `GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator (External/Unresolved)`
  • + [新增呼叫邊] `SyntaxMapping::insert_case_sensitive` ──[CALLS]──> `make_glob_matcher`
  • + [新增呼叫邊] `SyntaxMapping::insert_case_sensitive` ──[CALLS]──> `self.custom_mappings.push (External/Unresolved)`
  • _... 以及其餘 11 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `make_glob_matcher()`
- **變更前簽章 (Before)**: `fn make_glob_matcher(from: &str)` (L20~L27)
- **變更後簽章 (After)**: `fn make_glob_matcher(from: &str, case_insensitive: bool)` (L20~L27)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn make_glob_matcher(from: &str) -> Result<GlobMatcher> {
    let matcher = GlobBuilder::new(from)
        .case_insensitive(true)
        .literal_separator(true)
        .build()?
        .compile_matcher();
    Ok(matcher)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn make_glob_matcher(from: &str, case_insensitive: bool) -> Result<GlobMatcher> {
    let matcher = GlobBuilder::new(from)
        .case_insensitive(case_insensitive)
        .literal_separator(true)
        .build()?
        .compile_matcher();
    Ok(matcher)
}
```

### 🔹 函式: `SyntaxMapping::insert()`
- **變更前簽章 (Before)**: `fn SyntaxMapping::insert(&mut self, from: &str, to: MappingTarget<'a>)` (L99~L103)
- **變更後簽章 (After)**: `fn SyntaxMapping::insert(&mut self, from: &str, to: MappingTarget<'a>)` (L99~L103)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn insert(&mut self, from: &str, to: MappingTarget<'a>) -> Result<()> {
        let matcher = make_glob_matcher(from)?;
        self.custom_mappings.push((matcher, to));
        Ok(())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn insert(&mut self, from: &str, to: MappingTarget<'a>) -> Result<()> {
        let matcher = make_glob_matcher(from, true)?;
        self.custom_mappings.push((matcher, to));
        Ok(())
    }
```


#### 📄 檔案: `src/syntax_mapping/builtin.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:10, E:9, A:0) ➔ After(N:10, E:9, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 2, +Edges: 2, -Edges: 2, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `make_glob_matcher(from, case_insensitive)
        .expect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `make_glob_matcher(&buf, case_insensitive).ok (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `make_glob_matcher(from).expect (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `make_glob_matcher(&buf).ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `build_matcher_fixed` ──[CALLS]──> `make_glob_matcher(from, case_insensitive)
        .expect (External/Unresolved)`
  • + [新增呼叫邊] `build_matcher_dynamic` ──[CALLS]──> `make_glob_matcher(&buf, case_insensitive).ok (External/Unresolved)`
  • - [移除呼叫邊] `build_matcher_fixed` ──[CALLS]──> `make_glob_matcher(from).expect (External/Unresolved)`
  • - [移除呼叫邊] `build_matcher_dynamic` ──[CALLS]──> `make_glob_matcher(&buf).ok (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `build_matcher_fixed()`
- **變更前簽章 (Before)**: `fn build_matcher_fixed(from: &str)` (L56~L58)
- **變更後簽章 (After)**: `fn build_matcher_fixed(from: &str, case_insensitive: bool)` (L56~L59)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn build_matcher_fixed(from: &str) -> GlobMatcher {
    make_glob_matcher(from).expect("A builtin fixed glob matcher failed to compile")
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn build_matcher_fixed(from: &str, case_insensitive: bool) -> GlobMatcher {
    make_glob_matcher(from, case_insensitive)
        .expect("A builtin fixed glob matcher failed to compile")
}
```

### 🔹 函式: `build_matcher_dynamic()`
- **變更前簽章 (Before)**: `fn build_matcher_dynamic(segs: &[MatcherSegment])` (L67~L82)
- **變更後簽章 (After)**: `fn build_matcher_dynamic(segs: &[MatcherSegment], case_insensitive: bool)` (L68~L83)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn build_matcher_dynamic(segs: &[MatcherSegment]) -> Option<GlobMatcher> {
    // join segments
    let mut buf = String::new();
    for seg in segs {
        match seg {
            MatcherSegment::Text(s) => buf.push_str(s),
            MatcherSegment::Env(var) => {
                let replaced = env::var(var).ok()?;
                buf.push_str(&replaced);
            }
        }
    }
    // compile glob matcher
    let matcher = make_glob_matcher(&buf).ok()?;
    Some(matcher)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn build_matcher_dynamic(segs: &[MatcherSegment], case_insensitive: bool) -> Option<GlobMatcher> {
    // join segments
    let mut buf = String::new();
    for seg in segs {
        match seg {
            MatcherSegment::Text(s) => buf.push_str(s),
            MatcherSegment::Env(var) => {
                let replaced = env::var(var).ok()?;
                buf.push_str(&replaced);
            }
        }
    }
    // compile glob matcher
    let matcher = make_glob_matcher(&buf, case_insensitive).ok()?;
    Some(matcher)
}
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/bat show c2adbf6caad083b137beff082426f228a840e007
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff c2adbf6caad083b137beff082426f228a840e007~1 --file test_repos/bat/src/input.rs
   ```
