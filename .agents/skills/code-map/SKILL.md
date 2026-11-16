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

### F. Hybrid Decision API + LLM Semantic Lint (`--ai-lint`)
Run a **Fail-Open** two-stage semantic review (`Gatekeeper` Decision API -> `Explainer` LLM) on top of deterministic CODE-Map analysis, using externalized rules in `rules/codemap_lint_rules.json`.

> **CRITICAL — Output & Exit Code Semantics:**
> - `驗收裁決: 🟢 READY_TO_SHIP` reflects **ONLY** deterministic AST/topology checks (`check_invariants()`), **NOT** `--ai-lint`!
> - By default (`WarningOnly`), `--ai-lint` exits `0` even if `🔴 BLOCK` violations are found. **You MUST pass `--strict` to exit `1` on `🔴 BLOCK` violations.**
> - On API key absence, network timeout, or provider failure, `--ai-lint` **Fails Open** (prints `⚠️ [AI-LINT-SERVICE-WARN]` and exits `0` so it never blocks deterministic CODE-Map). Never confuse Fail-Open with passing semantic lint!
> - **Node Cap (`--max-lint-nodes`)**: Default is `15` nodes per invocation. For large files, always prefer `--git-diff HEAD~1 --ai-lint` or `--lint-symbol <name>`, or raise `--max-lint-nodes`.

**Prerequisites & Provider Selection:**
- Default `Gatekeeper` = `GeminiDecision` (`gemini-decision-1`) and default `Explainer` = `GeminiHttp` (`gemini-3.1-flash-lite`); both read `$env:GOOGLE_API_KEY` (or `--api-key <KEY>`).
- **No-API-Key / Local CLI Mode**: Override `Gatekeeper` to `Disabled` and `Explainer` to `AgyCli` (uses local `agy` CLI) or `Ollama`. Note that `AgyCli` spawns a local CLI process (~8–10s per node), so always pair it with `--lint-symbol` or `--git-diff`:
  - Supported `Gatekeeper` (`--gatekeeper`): `GeminiDecision`, `OpenAiCompatible`, `HttpTemplate`, `Disabled`
  - Supported `Explainer` (`--explainer`): `GeminiHttp`, `AgyCli`, `ClaudeCli`, `CodexCli`, `Ollama`, `OpenAiCompatible`, `CustomCli`, `Disabled`

```powershell
# 1. Diff-scoped lint (recommended: inspects only added/modified functions in git diff)
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --repo . --file src/app.py --git-diff HEAD~1 --ai-lint --strict

# 2. Full strict check with explicit API key and JSON report export
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --file src/app.py --check --ai-lint --strict --api-key "$env:GOOGLE_API_KEY" --lint-json reports/ai_lint.json

# 3. Local CLI / Offline mode (no GOOGLE_API_KEY needed)
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --file src/app.py --ai-lint --gatekeeper Disabled --explainer AgyCli --lint-model gemini-3.8-flash-low

# 4. Target specific symbol & print all Decision API probabilities (including PASS)
python.exe -X utf8 "d:\AntiGravity\UIA_Coder\codemap.py" --file src/app.py --ai-lint --lint-symbol handleDelete --show-all-decisions --rules rules/custom_rules.json
```

**All AI Lint CLI Flags:**
| Flag | Default | Purpose |
| :--- | :--- | :--- |
| `--ai-lint` | `false` | Enable two-stage semantic lint (`Gatekeeper` -> `Explainer`) |
| `--strict` | `false` | Exit `1` when any rule reaches `🔴 BLOCK` (service errors still Fail-Open) |
| `--rules <path>` | `rules/codemap_lint_rules.json` | Path to external JSON config & rules file |
| `--gatekeeper <name>` | `GeminiDecision` | Override Gatekeeper provider (`Disabled` skips Stage 1) |
| `--explainer <name>` | `GeminiHttp` | Override Explainer provider (`Disabled` skips Stage 2) |
| `--lint-model <name>` | Provider default | Override Explainer LLM model (e.g. `gemini-3.8-flash-low`, `qwen2.5-coder:7b`) |
| `--api-key <key>` | `$GOOGLE_API_KEY` | Explicit API key override |
| `--lint-symbol <kw>` | None | Restrict AI lint to nodes matching `<kw>` (case-insensitive substring match on function/method name or node ID) |
| `--max-lint-nodes <N>` | `15` | Max executable nodes inspected per run |
| `--show-all-decisions` | `false` | Show `🟢 PASS` scores alongside `WARN` / `BLOCK` |
| `--lint-json <path>` | None | Export full JSON report (`verdicts`, `explanation`, `service_warnings`) |

---

### G. Configuring Providers & Writing Custom Rules (`rules/codemap_lint_rules.json`)

Rules are routed automatically by CODE-Map using **6 Domains** (`GLOBAL`, `UI`, `NETWORK`, `DISK_IO`, `CONCURRENCY`, `SECURITY`). `DomainDetectors` inspect node categories, UI/event topology (automatically excluding `#CLI` anchors from `UI`), callee labels, and source tokens so irrelevant rules are never sent.

**Minimal Config & Custom Rule Schema:**
```json
{
  "Mode": "WarningOnly",
  "Gatekeeper": {
    "Enabled": true,
    "Provider": "GeminiDecision",
    "Endpoint": "https://generativelanguage.googleapis.com/v1beta/decisions",
    "Model": "gemini-decision-1",
    "ApiKeyEnv": "$GOOGLE_API_KEY",
    "TimeoutSeconds": 15,
    "DefaultWarnThreshold": 0.65,
    "DefaultBlockThreshold": 0.85
  },
  "Explainer": {
    "Enabled": true,
    "TriggerOn": "WarnOrBlock",
    "Provider": "GeminiHttp",
    "EndpointOrCommand": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    "Model": "gemini-3.1-flash-lite",
    "ApiKeyEnv": "$GOOGLE_API_KEY",
    "TimeoutSeconds": 45,
    "Temperature": 0.0
  },
  "Rules": [
    {
      "Id": "CUSTOM-ERR-01",
      "Enabled": true,
      "Domain": "GLOBAL",
      "Severity": "BLOCK",
      "Title": "Do not swallow exceptions with dummy assignments",
      "Scope": { "Languages": ["python", "csharp"], "NodeCategories": ["FUNCTION_DEF"] },
      "AstPreFilter": { "ContainsAny": ["except", "catch"], "MinLines": 3 },
      "Decision": {
        "Type": "noul",
        "Instructions": "Does this function silently swallow exceptions or use dummy assignments to bypass linters?"
      },
      "Thresholds": { "Warn": 0.65, "Block": 0.85 }
    }
  ]
}
```
- **Domain Routing Tip**: Default custom rules to `"Domain": "GLOBAL"` so they run on all nodes. Only use `"UI"`, `"NETWORK"`, `"DISK_IO"`, `"CONCURRENCY"`, or `"SECURITY"` when the rule specifically targets calls matched by `DomainDetectors` (otherwise nodes without matching tokens/topology will skip the rule).
- **Decision `Type` options**: `"noul"` (Yes/No probability `0.0–1.0`), `"score"` (rubric `Levels`), or `"choice"` (`Criteria` is a flat key-to-description dict):
  ```json
  "Decision": {
    "Type": "choice",
    "Instructions": "Classify implementation integrity.",
    "Criteria": {
      "real_impl": "Genuine complete implementation.",
      "stub_or_mock": "Hardcoded mock return or TODO placeholder."
    }
  },
  "Thresholds": { "WarnChoices": [], "BlockChoices": ["stub_or_mock"], "MinChoiceConfidence": 0.78 }
  ```
- **Custom REST APIs (`HttpTemplate`)**: Set `Gatekeeper.Provider` to `"HttpTemplate"` with `Endpoint`, `Headers`, `PayloadTemplate` (`{input}`, `{questions}`, `{model}`), and `ResponseMapping` (`answers_path`, `score_field`, `choice_field`).
- **Local `Ollama` / `OpenAiCompatible`**: Set `Explainer.Provider` to `"Ollama"` (default `http://localhost:11434/api/chat`) or `"OpenAiCompatible"` with custom `EndpointOrCommand` and `Model`.

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
3. **Deterministic + Semantic Verification Gate**: Immediately after edits, run `codemap.py` with **both** deterministic checks and `--ai-lint --strict` (preferring `--git-diff HEAD~1` or `--lint-symbol` to focus on modified nodes and avoid the 15-node cap), alongside unit tests:
   - **Mandatory Strict Mode**: Always pass `--strict` when gating with `--ai-lint`; without `--strict`, `🔴 BLOCK` violations still exit `0`.
   - **Anti-False-Clearance Check**: Inspect `stdout` for `⚠️ [AI-LINT-SERVICE-WARN]` (or `service_warnings` in `--lint-json`). A clean exit caused by Fail-Open service degradation is **`UNVERIFIED`**, NOT a semantic pass—either supply `$GOOGLE_API_KEY` / switch to `--gatekeeper Disabled --explainer AgyCli` or explicitly flag the unverified state.
   - **Dual-Verdict Reconciliation**: Accept changes only when **all three** hold: (a) deterministic `check_invariants() == READY_TO_SHIP`, (b) `🔴 BLOCK == 0`, and (c) zero `[AI-LINT-SERVICE-WARN]` errors.
   - **Surgical Feedback Loop**: On `🔴 BLOCK`, use `--lint-json` (or `Explainer LLM` `問題行號` + `修正建議`) to send exact line-level fixes back to the Maker rather than rewriting the whole file.
