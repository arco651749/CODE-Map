# Windows OS and Shell Rules

- **Target Operating System**: The user's operating system is Windows. Always assume a Windows environment.
- **No Unix Command Assumptions**: Do NOT assume Linux/Unix commands (such as grep, sed, awk, etc.) are installed in the %PATH%.
- **Use PowerShell Directly**: The terminal is already running native Windows PowerShell. Execute native PowerShell commands, pipelines, and scripts DIRECTLY without wrapping in redundant 'powershell -Command "..."' (which causes double variable expansion and parsing bugs).

# Windows Shell Command Rules

- On Windows PowerShell, Node.js-based CLI tools (like npm and npx) can fail to load because of execution policies blocking .ps1 script execution.
- To prevent these errors, always use the .cmd versions of these commands (i.e., npm.cmd and npx.cmd) instead of npm and npx.
- **Direct PowerShell Execution**: Write PowerShell scripts and pipelines directly. If explicitly invoking child powershell.exe, always use single quotes '' or escape variables with backticks ($var) to prevent premature variable expansion.

# Python Execution and Encoding Rules

- **Force UTF-8 Encoding**: On Windows environments, Python scripts (python.exe) must always be executed with UTF-8 mode (e.g. python.exe -X utf8 or $env:PYTHONUTF8=1) and include import sys; sys.stdout.reconfigure(encoding="utf-8") at the top of script files to prevent UnicodeEncodeError: 'cp950' crashes and terminal mojibake when printing Chinese characters, Emojis, or special Unicode symbols.

# AI Agent Behavior and Communication Rules

- **Explain Before Doing**: Always explain what you are about to do and your rationale before invoking any tools, executing shell commands, running Python scripts (python.exe), reading/writing files, or performing web searches. 
- **Action Notice Prefix**: Before invoking any tools or running commands/scripts, the explanation MUST begin with the action notice prefix '<span style="color:#4285f4;">✦</span> ' so the user can easily distinguish action notifications from regular conversational responses.
- **Build Trust through Transparency**: Do not perform silent actions or trigger sudden tool executions (like running shell commands or python scripts) without explicitly introducing the action first in the chat. This ensures the user is aligned with your progress and understands why an action is necessary.
- **Objective Rationality over Flattery**: 所有分析和回答都是以理性為出發點，不需迎合使用者是否會因這個回答而產生負面情緒！保持客觀、真實與批判性思維，直球點出問題、瓶頸與本質，不刻意安慰或迎合情緒。

# Speech-to-Text (STT) Rules

- **Default STT Engine**: All audio transcription and speech-to-text tasks must strictly use **whisper-cli** (whisper-cli.exe with Vulkan AMD GPU acceleration and GGML models) instead of unquantized PyTorch openai-whisper.
- **Model & VAD Configuration**: Use the GGML Large-v3 model at D:\Users\arco0\.cache\hyperframes\whisper\models\ggml-large-v3.bin and enable Silero VAD (--vad -vm D:\Users\arco0\.cache\hyperframes\whisper\models\ggml-silero-vad.bin) to prevent hallucinations and excessive memory consumption.

# Marimo Living Documentation & Python Tool Rules

- **Default to Marimo for Reusable Python Code**: Whenever implementing, refactoring, or providing reusable Python utilities, data transformers, or tools in this workspace, always author and curate them directly inside the project's `.marimo/<session_id>/marimo_session.py` notebook (or `.marimo/shared_toolbox.py` for cross-session project-wide utilities) rather than scattered temporary scripts.
- **Two-Tier Session & Shared Architecture**: Each chat session has its dedicated directory `.marimo/<session_id>/marimo_session.py` preventing DAG collisions across conversations, while `.marimo/shared_toolbox.py` serves as the permanent cross-session toolbox.
- **Closed-Loop Verification via `marimo_agent_cli.py`**: After any edit to a Marimo `.py` notebook, ALWAYS run `python.exe -X utf8 "D:\Users\arco0\.gemini\config\plugins\antigravity-marimo\skills\marimo-notebook\scripts\marimo_agent_cli.py" check --file "<notebook_path>"` to strip any accidental UTF-8 BOM, verify no `@app.cell` / `@app.function` appears after `if __name__ == "__main__":`, and pass `marimo check` with zero DAG errors.
- **Marimo Cell `stdout` Guard**: Inside a Marimo `@app.cell`, `sys.stdout` is wrapped by `ThreadSafeStream`. Always guard `reconfigure` with `if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")`.
- **Three-Block Pattern Requirement**: Every tool in a Marimo notebook must strictly adhere to the three-block structure:
  1. `mo.md` living documentation capturing context, Gotchas (e.g. Windows UTF-8/CP950 quirks, API rate limits), and changelog/rationale.
  2. Pure Python function/logic (`@app.function` or `@app.cell`) returning clean callable functions without global variable naming collisions.
  3. `mo.ui` interactive self-service test panel (keep display cell trailing `return` empty so generic UI variable names never collide in the DAG).
- **Surface Auxiliary Panel Link**: After creating, modifying, or fixing any tool in Marimo, always provide the user with the direct sidecar navigation pill: `[開啟 Marimo 筆記本](sidecar://antigravity-marimo/panel/)`.
- **Standalone Export Support**: Ensure tools remain decoupled from UI so they can be exported to standalone production scripts via `marimo export script` on demand.

