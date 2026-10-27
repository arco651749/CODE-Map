---
name: code-map
description: >-
  Use this skill whenever performing structural/behavioral code analysis, UI/CLI event wiring inspection,
  cross-file import/export dependency resolution, git semantic diffing, SWE-bench bidirectional fault localization,
  Two-Tier Spec-Driven Development verification (SpecVerifier), or Subagent Spec Objection anti-forgery verification
  across C# (.cs), Avalonia/WPF XAML (.axaml/.xaml), Python (.py), Rust (.rs), TypeScript/TSX (.ts/.tsx),
  JavaScript/JSX (.js/.jsx), Go (.go), HTML/Vue (.html/.vue), and C/C++ (.c/.cpp/.h/.hpp).
  Trigger on: 'CODE-Map', 'codemap', 'causal graph', 'wiring verification', 'semantic diff', 'spec verify',
  'locate symbol', 'forward slice', 'Avalonia MVVM binding check', or Maker-Checker subagent code verification.
---

# 🌲 CODE-Map: Causal Operation & Dependency Evaluation Map

**CODE-Map** is a Tree-sitter AST & NetworkX-powered **Behavioral Causal Graph Engine** (`d:\AntiGravity\UIA_Coder`). Unlike line-based `git diff` or flat text search, CODE-Map builds a formal directed graph of UI/CLI Entry Anchors (`UI_CONTROL`), Event Bindings (`EVENT_BINDING`), Executable Functions (`FUNCTION_DEF`), and Module/Contract States (`MODULE_STATE`), enforcing topological invariants and SHA-256 token-level executable fingerprints.

---

## 1. Supported Languages & Verified Capture Rates

CODE-Map has been benchmarked across **39 top open-source repositories (1,054 files)** with **0% crash rate** and **95.7% raw / 99.9%+ executable logic capture**:

| Ecosystem | Extensions | Key Semantic Capabilities |
| :--- | :--- | :--- |
| **C# + Avalonia / WPF** | `.cs`, `.axaml`, `.xaml` | `[RelayCommand]` MVVM mapping (`SaveAsync` -> `SaveCommand`), `StyledProperty` / `DirectProperty` registration, `AddHandler` routed events, `.axaml` `x:Class` <-> `.axaml.cs` cross-file linking, `{Binding}` & `Command` verification |
| **Python** | `.py` | Top-level functions, class methods, async/await flows, decorator fingerprints (`@app.get`, `@validator`), Pydantic/Dataclass typed fields, module constants, `time.sleep` blocking hazard detection |
| **Rust** | `.rs` | `fn`, generic `impl<T> Trait for Type<T>` resolution, `struct` / `enum` / `trait` / `const` / `static` / `type` / `macro_rules!`, leading `#[derive(...)]` attribute tracking, macro call scanning inside `token_tree` (`tokio::spawn!`), `.unwrap()` / `thread::sleep` hazards |
| **TypeScript & JavaScript** | `.ts`, `.tsx`, `.js`, `.jsx` | React/JSX event props (`onClick`), DOM `addEventListener`, class field arrow functions (`handleClick = () => {}`), `export default <expr>`, top-level guards/framework calls, dual-track fingerprinting (stripping parameter type noise on `FUNCTION_DEF` while capturing top-level `interface` / `type` / `enum` contracts) |
| **Go** | `.go` | `func`, generic receivers `func (r *Client[T])`, `type_spec` (`struct`, `interface`) & `type_alias`, unpacked `const_spec` / `var_spec` (including `_ Interface = (*Impl)(nil)` assertions), Goroutine `go` async edges, HTTP/Cobra router wiring (`.GET`, `.POST`, `HandleFunc`, `AddCommand`), `panic()` / `time.Sleep` hazards |
| **Web / C / C++** | `.html`, `.vue`, `.c`, `.cpp`, `.h`, `.hpp` | Vue SFC `<template>` + `<script>` binding, Win32/Qt/POSIX C/C++ entry and call graph analysis |

---

## 2. Core CLI Workflows (`codemap.py`)

Always run `codemap.py` with `python.exe -X utf8`:

### A. Single-File or Multi-File Causal Graph & Invariant Check
 Inspect all UI/CLI entry points, event bindings, call chains, scope isolation errors (`BLOCKED_SCOPE`), dangling handlers (`DANGLING_HANDLER`), and blocking hazards (`BLOCKED_INVARIANT`):

```powershell
# Single file analysis + formal invariant check
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --file path/to/file.cs --check

# Multi-file joint resolution (e.g., Avalonia View.axaml + View.axaml.cs + ViewModel.cs, or TS/Python modules)
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --files View.axaml View.axaml.cs ViewModel.cs --check

# Entire directory workspace graph
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --dir src/ --check
```

### B. Bidirectional Fault Localization (`--locate`) & Causal Slicing (`--bundle` / `--slice`)
Before editing unfamiliar code, extract the exact **Upstream Callers + Target Implementation + Downstream Callees** source bundle without reading thousands of unrelated lines:

```powershell
# Bidirectional fault localization by symbol/keyword
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --dir src/ --locate "handleDelete"

# Extract full source code bundle triggered by a specific UI control or anchor
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --file app.py --bundle "btn_submit"

# Forward graph slice from a specific anchor ID
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --file app.py --slice "ctrl:btn_submit@app.py:L42"
```

### C. Semantic Graph Diffing (`--diff-files` & `--git-diff`)
Compare two versions of a file or inspect a Git commit at the semantic AST/graph level (distinguishing structural topology changes from body-level token fingerprint edits, while ignoring pure comments/formatting):

```powershell
# Compare two files (e.g., before vs. after refactor)
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --diff-files before.rs after.rs

# Compare a file against Git history (default HEAD~1, or specify commit range)
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --repo . --file src/main.go --git-diff HEAD~1
```

### D. Two-Tier Spec Verification (`--verify-spec`) & Subagent Objection Anti-Forgery (`--verify-objection`)
When acting as the **Architect (Checker)** reviewing a **Subagent (Maker)**:

```powershell
# Verify implementation against a Target Graph Spec (YAML/JSON)
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --files src/modal.ts src/api.ts --verify-spec spec.yaml

# Verify whether a Subagent's Spec Objection claim ("symbol X does not exist in file Y") is genuine or falsified
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --repo . --verify-objection objection.yaml
```

### E. Interactive Dual-Pane HTML Causal Dashboard (`--html`)
Export a standalone interactive HTML dashboard linking the causal topology tree to source code lines:

```powershell
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --file src/app.py --html reports/dashboard.html
```

---

## 3. Programmatic Python API Usage

When writing custom verification or benchmark scripts in Python, import `code_map` (adding `d:\AntiGravity\UIA_Coder` to `sys.path` if running outside the repo):

```python
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"d:\AntiGravity\UIA_Coder")

from code_map import (
    get_adapter_for_file,
    WorkspaceGraphBuilder,
    CodeMapDiffer,
    SpecVerifier,
    verify_objection,
)

# 1. Parse a single file
adapter = get_adapter_for_file("MainWindow.axaml.cs")
graph = adapter.parse_and_build(source_code, file_path="MainWindow.axaml.cs")
inv = graph.check_invariants()  # {'passed': True, 'verdict': '🟢 PASSED', ...}

# 2. Build a multi-file workspace graph (resolves cross-file imports & Avalonia x:Class / DataType)
ws_graph = WorkspaceGraphBuilder.build_from_files(["MainWindow.axaml", "MainWindow.axaml.cs", "MainViewModel.cs"])

# 3. Semantic diff between two source strings or git commits
diff_res = CodeMapDiffer.diff_source(before_code, after_code, ext=".ts", file_path="store.ts")
print(diff_res.to_diff_markdown())
```

---

## 4. Maker-Checker Subagent Workflow Protocol

When using **CODE-Map** in the **Architect + Flash Subagent** pair workflow:
1. **Locate & Spec First**: Use `--locate` or `WorkspaceGraphBuilder` to inspect the existing call topology and author a clear Target Spec (including pre/post-conditions and branch-to-edge mappings).
2. **Surgical Patching**: Instruct the Subagent to patch only the target `FUNCTION_DEF` / `MODULE_STATE` nodes via `edit_file` without rewriting the entire file.
3. **Deterministic Binary Gate**: Immediately after edits, run `codemap.py --check`, `--verify-spec`, or `--diff-files` alongside unit tests (`pytest`). Treat the formal verdict (`PASSED` / `FAILED`) as the sole stopping criterion to prevent agent thrashing.
