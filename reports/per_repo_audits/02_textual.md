# 🔬 CODE-Map 基準審查獨立驗證報告: `textual`
> **技術生態**: `Python (現代非同步 TUI 框架)`  
> **本地倉庫路徑**: `test_repos/textual`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 32 Files  
> **報告生成時間**: 2026-10-20 21:40:26  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `20` / `32` | `62.5%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `7` / `32` | `21.9%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `5` / `32` | `15.6%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`27` / `32`** | **`84.4%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `32` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `01fb6fd7`
- **完整 Hash**: `01fb6fd73af092fe6e5da03c032d3e9c3fa161f1`
- **說明 (Ground Truth)**: ctrl+backspace binding
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/widgets/_text_area.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:256, E:298, A:0) ➔ After(N:256, E:298, A:0)
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

### 🔹 Commit #02: `79526f7a`
- **完整 Hash**: `79526f7a3aa7ac4c74ef341184077de032f7d8d0`
- **說明 (Ground Truth)**: cache key processing
- **變更檔案數**: 3

#### 📄 檔案: `src/textual/_xterm_parser.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:51, E:64, A:2) ➔ After(N:53, E:68, A:2)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 10, -Edges: 6, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#app** `(Widget)`
    └── ⚡ **on('token')**
        └── 🎯 [TRIGGERS] `XTermParser.on_token()`
            └── 🎯 [CALLS] `XTermParser.debug_log()`
                └── 🎯 [CALLS] `flush (External/Unresolved)()`
            └── 🎯 [CALLS] `token_callback (External/Unresolved)()`
  🌲 **#key** `(Widget)`
    └── ⚡ **on('token')**
        └── 🎯 [TRIGGERS] `XTermParser.on_key_token()`
            └── 🎯 [CALLS] `XTermParser.on_token()`
                └── 🎯 [CALLS] `XTermParser.debug_log()`
                    └── 🎯 [CALLS] `flush (External/Unresolved)()`
                └── 🎯 [CALLS] `token_callback (External/Unresolved)()`
            └── *ref:`XTermParser.debug_log` [已折疊指針]

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `lru_cache (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `XTermParser._parse_extended_key` (FUNCTION_DEF)
  • + [新增呼叫邊] `XTermParser._parse_extended_key` ──[CALLS]──> `lru_cache (External/Unresolved)`
  • + [新增呼叫邊] `XTermParser._parse_extended_key` ──[CALLS]──> `fullmatch (External/Unresolved)`
  • + [新增呼叫邊] `XTermParser._parse_extended_key` ──[CALLS]──> `groups (External/Unresolved)`
  • + [新增呼叫邊] `XTermParser._parse_extended_key` ──[CALLS]──> `chr (External/Unresolved)`
  • + [新增呼叫邊] `XTermParser._parse_extended_key` ──[CALLS]──> `_character_to_key (External/Unresolved)`
  • + [新增呼叫邊] `XTermParser._parse_extended_key` ──[CALLS]──> `isspace (External/Unresolved)`
  • + [新增呼叫邊] `XTermParser._parse_extended_key` ──[CALLS]──> `enumerate (External/Unresolved)`
  • + [新增呼叫邊] `XTermParser._parse_extended_key` ──[CALLS]──> `sort (External/Unresolved)`
  • + [新增呼叫邊] `XTermParser._parse_extended_key` ──[CALLS]──> `Key (External/Unresolved)`
  • + [新增呼叫邊] `XTermParser._sequence_to_key_events` ──[CALLS]──> `XTermParser._parse_extended_key`
  • - [移除呼叫邊] `XTermParser._sequence_to_key_events` ──[CALLS]──> `fullmatch (External/Unresolved)`
  • - [移除呼叫邊] `XTermParser._sequence_to_key_events` ──[CALLS]──> `groups (External/Unresolved)`
  • - [移除呼叫邊] `XTermParser._sequence_to_key_events` ──[CALLS]──> `chr (External/Unresolved)`
  • _... 以及其餘 3 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `XTermParser._sequence_to_key_events()`
- **變更前簽章 (Before)**: `def _sequence_to_key_events( self, sequence: str, alt: bool = False ) -> Iterable[events.Key]` (L335~L424)
- **變更後簽章 (After)**: `def _sequence_to_key_events( self, sequence: str, alt: bool = False ) -> Iterable[events.Key]` (L384~L440)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _sequence_to_key_events(
        self, sequence: str, alt: bool = False
    ) -> Iterable[events.Key]:
        """Map a sequence of code points on to a sequence of keys.

        Args:
            sequence: Sequence of code points.

        Returns:
            Iterable of key events.
        """

        if (match := _re_extended_key.fullmatch(sequence)) is not None:
            codes, end = match.groups(default="")
            codepoint_str, modifiers_str, text_str, *_ = codes.split(";") + ["", "", ""]

            codepoint = int(codepoint_str or "1")
            modifiers = int(modifiers_str or "0")
            text = chr(int(text_str)) if text_str else None

            if not (key := FUNCTIONAL_KEYS.get(f"{codepoint}{end}", "")):
                key = _character_to_key(text if text else chr(codepoint))

            key_tokens: list[str] = []
            # The modifier is redundant on a modifier key
            if (
                modifiers
                and key not in MODIFIER_FUNCTIONAL_KEYS
                and text_str is not None
            ):
                modifier_bits = int(modifiers) - 1
                # Not convinced of the utility in reporting caps_lock and num_lock
                MODIFIERS = ("alt", "ctrl", "super", "hyper", "meta")
                # Ignore caps_lock and num_lock modifiers
                if modifier_bits & 1 and (text is None or text.isspace()):
                    key_tokens.append("shift")
                for bit, modifier in enumerate(MODIFIERS, 1):
                    if modifier == "alt" and text is not None:
                        continue
                    if modifier_bits & (1 << bit):
                        key_tokens.append(modifier)

            key_tokens.sort()
            if key is not None:
                key_tokens.append(key)
            yield events.Key(
                "+".join(key_tokens),
                text
                or (None if modifiers else SPECIAL_KEY_TO_CHARACTER.get(key, None)),
            )
            return

        keys = ANSI_SEQUENCES_KEYS.get(sequence)
        # If we're being asked to ignore the key...
        if keys is IGNORE_SEQUENCE:
            # ...build a special ignore key event, which has the ignore
            # name as the key (that is, the key this sequence is bound
            # to is the ignore key) and the sequence that was ignored as
            # the character.
            yield events.Key(Keys.Ignore, sequence)
            return
        if isinstance(keys, tuple):
            # If the sequence mapped to a tuple, then it's values from the
            # `Keys` enum. Raise key events from what we find in the tuple.
            for key in keys:
                yield events.Key(key.value, sequence if len(sequence) == 1 else None)
            return
        # If keys is a string, the intention is that it's a mapping to a
        # character, which should really be treated as the sequence for the
        # purposes of the next step...
        if isinstance(keys, str):
            sequence = keys
        # If the sequence is a single character, attempt to process it as a
        # key.

        if len(sequence) == 1:
            try:
                if not sequence.isalnum():
                    name = _character_to_key(sequence)
                else:
                    name = sequence

                name = KEY_NAME_REPLACEMENTS.get(name, name)
                if len(name) == 1 and alt:
                    if name.isupper():
                        name = f"shift+{name.lower()}"
                    name = f"alt+{name}"
                yield events.Key(name, sequence)
            except Exception:
                yield events.Key(sequence, sequence)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _sequence_to_key_events(
        self, sequence: str, alt: bool = False
    ) -> Iterable[events.Key]:
        """Map a sequence of code points on to a sequence of keys.

        Args:
            sequence: Sequence of code points.

        Returns:
            Iterable of key events.
        """

        if (
            not constants.DISABLE_KITTY_KEY
            and (key := self._parse_extended_key(sequence)) is not None
        ):
            yield key
            return

        keys = ANSI_SEQUENCES_KEYS.get(sequence)
        # If we're being asked to ignore the key...
        if keys is IGNORE_SEQUENCE:
            # ...build a special ignore key event, which has the ignore
            # name as the key (that is, the key this sequence is bound
            # to is the ignore key) and the sequence that was ignored as
            # the character.
            yield events.Key(Keys.Ignore, sequence)
            return
        if isinstance(keys, tuple):
            # If the sequence mapped to a tuple, then it's values from the
            # `Keys` enum. Raise key events from what we find in the tuple.
            for key in keys:
                yield events.Key(key.value, sequence if len(sequence) == 1 else None)
            return
        # If keys is a string, the intention is that it's a mapping to a
        # character, which should really be treated as the sequence for the
        # purposes of the next step...
        if isinstance(keys, str):
            sequence = keys
        # If the sequence is a single character, attempt to process it as a
        # key.

        if len(sequence) == 1:
            try:
                if not sequence.isalnum():
                    name = _character_to_key(sequence)
                else:
                    name = sequence

                name = KEY_NAME_REPLACEMENTS.get(name, name)
                if len(name) == 1 and alt:
                    if name.isupper():
                        name = f"shift+{name.lower()}"
                    name = f"alt+{name}"
                yield events.Key(name, sequence)
            except Exception:
                yield events.Key(sequence, sequence)
```


#### 📄 檔案: `src/textual/constants.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:10, E:7, A:0) ➔ After(N:10, E:7, A:0)
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

#### 📄 檔案: `src/textual/drivers/linux_driver.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:75, E:83, A:1) ➔ After(N:75, E:83, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#terminal** `(Widget)`
    └── ⚡ **on('resize')**
        └── 🎯 [TRIGGERS] `LinuxDriver.on_terminal_resize()`
            └── 🎯 [CALLS] `LinuxDriver.send_size_event()`
                └── 🎯 [CALLS] `LinuxDriver._get_terminal_size()`
                    └── 🎯 [CALLS] `get_terminal_size (External/Unresolved)()`
                └── 🎯 [CALLS] `Resize (External/Unresolved)()`
                └── 🎯 [CALLS] `Size (External/Unresolved)()`
                └── 🎯 [CALLS] `_post_message (External/Unresolved)()`
                └── 🎯 [CALLS] `run_coroutine_threadsafe (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `LinuxDriver.start_application_mode()`
- **變更前簽章 (Before)**: `def start_application_mode(self)` (L196~L312)
- **變更後簽章 (After)**: `def start_application_mode(self)` (L196~L313)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def start_application_mode(self):
        """Start application mode."""

        def _stop_again(*_) -> None:
            """Signal handler that will put the application back to sleep."""
            os.kill(os.getpid(), signal.SIGSTOP)

        # If we're working with an actual tty...
        # https://github.com/Textualize/textual/issues/4104
        if os.isatty(self.fileno):
            # Set up handlers to ensure that, if there's a SIGTTOU or a SIGTTIN,
            # we go back to sleep.
            signal.signal(signal.SIGTTOU, _stop_again)
            signal.signal(signal.SIGTTIN, _stop_again)
            try:
                # Here we perform a NOP tcsetattr. The reason for this is
                # that, if we're suspended and the user has performed a `bg`
                # in the shell, we'll SIGCONT *but* we won't be allowed to
                # do terminal output; so rather than get into the business
                # of spinning up application mode again and then finding
                # out, we perform a no-consequence change and detect the
                # problem right away.
                termios.tcsetattr(
                    self.fileno, termios.TCSANOW, termios.tcgetattr(self.fileno)
                )
            except termios.error:
                # There was an error doing the tcsetattr; there is no sense
                # in carrying on because we'll be doing a SIGSTOP (see
                # above).
                return
            finally:
                # We don't need to be hooking SIGTTOU or SIGTTIN any more.
                signal.signal(signal.SIGTTOU, signal.SIG_DFL)
                signal.signal(signal.SIGTTIN, signal.SIG_DFL)

        loop = asyncio.get_running_loop()

        def send_size_event() -> None:
            terminal_size = self._get_terminal_size()
            width, height = terminal_size
            textual_size = Size(width, height)
            event = events.Resize(textual_size, textual_size)
            asyncio.run_coroutine_threadsafe(
                self._app._post_message(event),
                loop=loop,
            )

        self._writer_thread = WriterThread(self._file)
        self._writer_thread.start()

        def on_terminal_resize(signum, stack) -> None:
            if not self._in_band_window_resize:
                send_size_event()

        signal.signal(signal.SIGWINCH, on_terminal_resize)
        send_size_event()

        self.write("\x1b[?1049h")  # Alt screen

        self._enable_mouse_support()
        try:
            self.attrs_before = termios.tcgetattr(self.fileno)
        except termios.error:
            # Ignore attribute errors.
            self.attrs_before = None

        try:
            newattr = termios.tcgetattr(self.fileno)
        except termios.error:
            pass
        else:
            newattr[tty.LFLAG] = self._patch_lflag(newattr[tty.LFLAG])
            newattr[tty.IFLAG] = self._patch_iflag(newattr[tty.IFLAG])

            # VMIN defines the number of characters read at a time in
            # non-canonical mode. It seems to default to 1 on Linux, but on
            # Solaris and derived operating systems it defaults to 4. (This is
            # because the VMIN slot is the same as the VEOF slot, which
            # defaults to ASCII EOT = Ctrl-D = 4.)
            newattr[tty.CC][termios.VMIN] = 1

            try:
                termios.tcsetattr(self.fileno, termios.TCSANOW, newattr)
            except termios.error:
                pass

        self.write("\x1b[?25l")  # Hide cursor
        self.write("\x1b[?1004h")  # Enable FocusIn/FocusOut.

        # https://sw.kovidgoyal.net/kitty/keyboard-protocol/
        KITTY_PROTOCOL_FLAG = (
            KITTY_DISAMBIGUATE_ESCAPE_CODES
            | KITTY_REPORT_ALL_KEYS
            | KITTY_REPORT_ASSOCIATED_TEXT
        )
        self.write(f"\x1b[>{KITTY_PROTOCOL_FLAG}u")

        self.flush()
        self._key_thread = Thread(target=self._run_input_thread, name="textual-input")

        self._key_thread.start()
        self._request_terminal_sync_mode_support()
        self._query_in_band_window_resize()
        self._enable_bracketed_paste()
        self._disable_line_wrap()

        # Appears to fix an issue enabling mouse support in iTerm 3.5.0
        self._enable_mouse_support()

        # If we need to ask the app to signal that we've come back from a
        # SIGTSTP...
        if self._must_signal_resume:
            self._must_signal_resume = False
            asyncio.run_coroutine_threadsafe(
                self._app._post_message(self.SignalResume()),
                loop=loop,
            )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def start_application_mode(self):
        """Start application mode."""

        def _stop_again(*_) -> None:
            """Signal handler that will put the application back to sleep."""
            os.kill(os.getpid(), signal.SIGSTOP)

        # If we're working with an actual tty...
        # https://github.com/Textualize/textual/issues/4104
        if os.isatty(self.fileno):
            # Set up handlers to ensure that, if there's a SIGTTOU or a SIGTTIN,
            # we go back to sleep.
            signal.signal(signal.SIGTTOU, _stop_again)
            signal.signal(signal.SIGTTIN, _stop_again)
            try:
                # Here we perform a NOP tcsetattr. The reason for this is
                # that, if we're suspended and the user has performed a `bg`
                # in the shell, we'll SIGCONT *but* we won't be allowed to
                # do terminal output; so rather than get into the business
                # of spinning up application mode again and then finding
                # out, we perform a no-consequence change and detect the
                # problem right away.
                termios.tcsetattr(
                    self.fileno, termios.TCSANOW, termios.tcgetattr(self.fileno)
                )
            except termios.error:
                # There was an error doing the tcsetattr; there is no sense
                # in carrying on because we'll be doing a SIGSTOP (see
                # above).
                return
            finally:
                # We don't need to be hooking SIGTTOU or SIGTTIN any more.
                signal.signal(signal.SIGTTOU, signal.SIG_DFL)
                signal.signal(signal.SIGTTIN, signal.SIG_DFL)

        loop = asyncio.get_running_loop()

        def send_size_event() -> None:
            terminal_size = self._get_terminal_size()
            width, height = terminal_size
            textual_size = Size(width, height)
            event = events.Resize(textual_size, textual_size)
            asyncio.run_coroutine_threadsafe(
                self._app._post_message(event),
                loop=loop,
            )

        self._writer_thread = WriterThread(self._file)
        self._writer_thread.start()

        def on_terminal_resize(signum, stack) -> None:
            if not self._in_band_window_resize:
                send_size_event()

        signal.signal(signal.SIGWINCH, on_terminal_resize)
        send_size_event()

        self.write("\x1b[?1049h")  # Alt screen

        self._enable_mouse_support()
        try:
            self.attrs_before = termios.tcgetattr(self.fileno)
        except termios.error:
            # Ignore attribute errors.
            self.attrs_before = None

        try:
            newattr = termios.tcgetattr(self.fileno)
        except termios.error:
            pass
        else:
            newattr[tty.LFLAG] = self._patch_lflag(newattr[tty.LFLAG])
            newattr[tty.IFLAG] = self._patch_iflag(newattr[tty.IFLAG])

            # VMIN defines the number of characters read at a time in
            # non-canonical mode. It seems to default to 1 on Linux, but on
            # Solaris and derived operating systems it defaults to 4. (This is
            # because the VMIN slot is the same as the VEOF slot, which
            # defaults to ASCII EOT = Ctrl-D = 4.)
            newattr[tty.CC][termios.VMIN] = 1

            try:
                termios.tcsetattr(self.fileno, termios.TCSANOW, newattr)
            except termios.error:
                pass

        self.write("\x1b[?25l")  # Hide cursor
        self.write("\x1b[?1004h")  # Enable FocusIn/FocusOut.

        if not constants.DISABLE_KITTY_KEY:
            # https://sw.kovidgoyal.net/kitty/keyboard-protocol/
            KITTY_PROTOCOL_FLAG = (
                KITTY_DISAMBIGUATE_ESCAPE_CODES
                | KITTY_REPORT_ALL_KEYS
                | KITTY_REPORT_ASSOCIATED_TEXT
            )
            self.write(f"\x1b[>{KITTY_PROTOCOL_FLAG}u")

        self.flush()
        self._key_thread = Thread(target=self._run_input_thread, name="textual-input")

        self._key_thread.start()
        self._request_terminal_sync_mode_support()
        self._query_in_band_window_resize()
        self._enable_bracketed_paste()
        self._disable_line_wrap()

        # Appears to fix an issue enabling mouse support in iTerm 3.5.0
        self._enable_mouse_support()

        # If we need to ask the app to signal that we've come back from a
        # SIGTSTP...
        if self._must_signal_resume:
            self._must_signal_resume = False
            asyncio.run_coroutine_threadsafe(
                self._app._post_message(self.SignalResume()),
                loop=loop,
            )
```


---

### 🔹 Commit #03: `cd542be4`
- **完整 Hash**: `cd542be423fca7fe53e3f0dfc548dc3ef8c9fb9a`
- **說明 (Ground Truth)**: Restore space to key dict
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/_ansi_sequences.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:1, E:0, A:0) ➔ After(N:1, E:0, A:0)
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

### 🔹 Commit #04: `2d73ddb3`
- **完整 Hash**: `2d73ddb3be21d19e49c708b761d7ef09c763bb53`
- **說明 (Ground Truth)**: scroll mechanics
- **變更檔案數**: 4

#### 📄 檔案: `src/textual/app.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:507, E:615, A:2) ➔ After(N:507, E:615, A:2)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#app** `(Widget)`
    └── ⚡ **on('ready')**
        └── 🎯 [TRIGGERS] `App.on_app_ready()`
            └── 🎯 [CALLS] `set (External/Unresolved)()`
    └── ⚡ **on('event')**
        └── 🎯 [TRIGGERS] `App.on_event()`
            └── 🎯 [CALLS] `App._check_bindings()`
                └── 🎯 [CALLS] `App.run_action()`
                    └── 🎯 [CALLS] `App._dispatch_action()`
                        └── 🎯 [CALLS] `callable (External/Unresolved)()`
                        └── 🎯 [CALLS] `getattr (External/Unresolved)()`
                        └── 🎯 [CALLS] `invoke (External/Unresolved)()`
                        └── 🎯 [CALLS] `system (External/Unresolved)()`
                    └── 🎯 [CALLS] `App._parse_action()`
                        └── *ref:`getattr (External/Unresolved)` [已折疊指針]
                        └── 🎯 [CALLS] `parse (External/Unresolved)()`
                    └── 🎯 [CALLS] `check_action (External/Unresolved)()`
                └── 🎯 [CALLS] `reversed (External/Unresolved)()`
            └── 🎯 [CALLS] `App._init_mode()`
                └── 🎯 [CALLS] `App._get_screen()`
                    └── 🎯 [CALLS] `App._register()`
                        └── *ref:`App._register` [已折疊指針]
                        └── 🎯 [CALLS] `App._register_child()`
                            └── 🎯 [CALLS] `_append (External/Unresolved)()`
                            └── 🎯 [CALLS] `_attach (External/Unresolved)()`
                            └── 🎯 [CALLS] `_insert (External/Unresolved)()`
                            └── 🎯 [CALLS] `_post_register (External/Unresolved)()`
                            └── 🎯 [CALLS] `add (External/Unresolved)()`
                        └── 🎯 [CALLS] `_start_messages (External/Unresolved)()`
                        └── 🎯 [CALLS] `add_new_widget (External/Unresolved)()`
                        └── 🎯 [CALLS] `apply_stylesheet (External/Unresolved)()`
                        └── 🎯 [CALLS] `list (External/Unresolved)()`
                        └── *ref:`reversed (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `App.get_screen()`
                        └── 🎯 [CALLS] `KeyError (External/Unresolved)()`
                        └── 🎯 [CALLS] `TypeError (External/Unresolved)()`
                        └── *ref:`callable (External/Unresolved)` [已折疊指針]
                        └── 🎯 [CALLS] `next_screen (External/Unresolved)()`
                        └── 🎯 [CALLS] `type (External/Unresolved)()`
                    └── 🎯 [CALLS] `AwaitMount (External/Unresolved)()`
                    └── 🎯 [CALLS] `call_next (External/Unresolved)()`
                └── 🎯 [CALLS] `App._load_screen_css()`
                    └── 🎯 [CALLS] `add_paths (External/Unresolved)()`
                    └── 🎯 [CALLS] `add_source (External/Unresolved)()`
                    └── 🎯 [CALLS] `getfile (External/Unresolved)()`
                    └── 🎯 [CALLS] `has_source (External/Unresolved)()`
                    └── 🎯 [CALLS] `reparse (External/Unresolved)()`
                    └── 🎯 [CALLS] `update (External/Unresolved)()`
                └── *ref:`App._register` [已折疊指針]
                └── 🎯 [CALLS] `App.get_default_screen()`
                    └── 🎯 [CALLS] `Screen (External/Unresolved)()`
                └── 🎯 [CALLS] `App.refresh_css()`
                    └── 🎯 [CALLS] `App.get_css_variables()`
                        └── 🎯 [CALLS] `App.get_theme_variable_defaults()`
                        └── 🎯 [CALLS] `generate (External/Unresolved)()`
                        └── 🎯 [CALLS] `to_color_system (External/Unresolved)()`
                    └── 🎯 [CALLS] `_refresh_layout (External/Unresolved)()`
                    └── *ref:`reparse (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `set_variables (External/Unresolved)()`
                    └── *ref:`update (External/Unresolved)` [已折疊指針]
                └── *ref:`AwaitMount (External/Unresolved)` [已折疊指針]
                └── 🎯 [CALLS] `ScreenResume (External/Unresolved)()`
                └── *ref:`TypeError (External/Unresolved)` [已折疊指針]
                └── 🎯 [CALLS] `_screen (External/Unresolved)()`
                └── 🎯 [CALLS] `_screen_resized (External/Unresolved)()`
                └── *ref:`callable (External/Unresolved)` [已折疊指針]
                └── 🎯 [CALLS] `post_message (External/Unresolved)()`
                └── *ref:`type (External/Unresolved)` [已折疊指針]
            └── 🎯 [CALLS] `App.get_widget_at()`
                └── *ref:`App.get_widget_at` [已折疊指針]
            └── *ref:`App.on_event` [已折疊指針]
            └── 🎯 [CALLS] `Offset (External/Unresolved)()`
            └── 🎯 [CALLS] `_clear_tooltip (External/Unresolved)()`
            └── 🎯 [CALLS] `_forward_event (External/Unresolved)()`
            └── 🎯 [CALLS] `from_event (External/Unresolved)()`
            └── 🎯 [CALLS] `minimize (External/Unresolved)()`
            └── 🎯 [CALLS] `super (External/Unresolved)()`
    └── 🎯 [CALLS] `TypeVar (External/Unresolved)()`
  🌲 **#self** `(Control)`
    └── ⚡ **devtools.connect**
        └── 🎯 [TRIGGERS] `) (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `App.on_event()`
- **變更前簽章 (Before)**: `async def on_event(self, event: events.Event) -> None: # Handle input events that haven't been forwarded # If the event has been forwarded it may have bubbled up back to the App` (L4019~L4106)
- **變更後簽章 (After)**: `async def on_event(self, event: events.Event) -> None: # Handle input events that haven't been forwarded # If the event has been forwarded it may have bubbled up back to the App` (L4024~L4112)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def on_event(self, event: events.Event) -> None:
        # Handle input events that haven't been forwarded
        # If the event has been forwarded it may have bubbled up back to the App
        if isinstance(event, events.Compose):
            await self._init_mode(self._current_mode)
            await super().on_event(event)
        elif isinstance(event, events.InputEvent) and not event.is_forwarded:
            if not self.app_focus and isinstance(event, (events.Key, events.MouseDown)):
                self.app_focus = True
            if isinstance(event, events.MouseEvent):
                # Record current mouse position on App
                self.mouse_position = Offset(event.x, event.y)
                if isinstance(event, events.MouseDown):
                    try:
                        self._mouse_down_widget, _ = self.get_widget_at(
                            event.x, event.y
                        )
                    except NoWidget:
                        # Shouldn't occur, since at the very least this will find the Screen
                        self._mouse_down_widget = None

                self.screen._forward_event(event)

                # If a MouseUp occurs at the same widget as a MouseDown, then we should
                # consider it a click, and produce a Click event.
                if (
                    isinstance(event, events.MouseUp)
                    and self._mouse_down_widget is not None
                ):
                    try:
                        screen_offset = event.screen_offset
                        mouse_down_widget = self._mouse_down_widget
                        mouse_up_widget, _ = self.get_widget_at(*screen_offset)
                        if mouse_up_widget is mouse_down_widget:
                            same_offset = (
                                self._click_chain_last_offset is not None
                                and self._click_chain_last_offset == screen_offset
                            )
                            within_time_threshold = (
                                self._click_chain_last_time is not None
                                and event.time - self._click_chain_last_time
                                <= self.CLICK_CHAIN_TIME_THRESHOLD
                            )

                            if same_offset and within_time_threshold:
                                self._chained_clicks += 1
                            else:
                                self._chained_clicks = 1

                            click_event = events.Click.from_event(
                                mouse_down_widget, event, chain=self._chained_clicks
                            )

                            self._click_chain_last_time = event.time
                            self._click_chain_last_offset = screen_offset

                            self.screen._forward_event(click_event)
                    except NoWidget:
                        pass

            elif isinstance(event, events.Key):
                # Special case for maximized widgets
                # If something is maximized, then escape should minimize
                if (
                    self.screen.maximized is not None
                    and event.key == "escape"
                    and self.escape_to_minimize
                ):
                    self.screen.minimize()
                    return
                if self.focused:
                    try:
                        self.screen._clear_tooltip()
                    except NoScreen:
                        pass
                if not await self._check_bindings(event.key, priority=True):
                    forward_target = self.focused or self.screen
                    forward_target._forward_event(event)
            else:
                self.screen._forward_event(event)

        elif isinstance(event, events.Paste) and not event.is_forwarded:
            if self.focused is not None:
                self.focused._forward_event(event)
            else:
                self.screen._forward_event(event)
        else:
            await super().on_event(event)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def on_event(self, event: events.Event) -> None:
        # Handle input events that haven't been forwarded
        # If the event has been forwarded it may have bubbled up back to the App
        if isinstance(event, events.Compose):
            await self._init_mode(self._current_mode)
            await super().on_event(event)
        elif isinstance(event, events.InputEvent) and not event.is_forwarded:
            if not self.app_focus and isinstance(event, (events.Key, events.MouseDown)):
                self.app_focus = True
            if isinstance(event, events.MouseEvent):
                # Record current mouse position on App
                self.mouse_position = Offset(event.x, event.y)
                self.mouse_position_high_resolution = (event.screen_x, event.screen_y)
                if isinstance(event, events.MouseDown):
                    try:
                        self._mouse_down_widget, _ = self.get_widget_at(
                            event.x, event.y
                        )
                    except NoWidget:
                        # Shouldn't occur, since at the very least this will find the Screen
                        self._mouse_down_widget = None

                self.screen._forward_event(event)

                # If a MouseUp occurs at the same widget as a MouseDown, then we should
                # consider it a click, and produce a Click event.
                if (
                    isinstance(event, events.MouseUp)
                    and self._mouse_down_widget is not None
                ):
                    try:
                        screen_offset = event.screen_offset
                        mouse_down_widget = self._mouse_down_widget
                        mouse_up_widget, _ = self.get_widget_at(*screen_offset)
                        if mouse_up_widget is mouse_down_widget:
                            same_offset = (
                                self._click_chain_last_offset is not None
                                and self._click_chain_last_offset == screen_offset
                            )
                            within_time_threshold = (
                                self._click_chain_last_time is not None
                                and event.time - self._click_chain_last_time
                                <= self.CLICK_CHAIN_TIME_THRESHOLD
                            )

                            if same_offset and within_time_threshold:
                                self._chained_clicks += 1
                            else:
                                self._chained_clicks = 1

                            click_event = events.Click.from_event(
                                mouse_down_widget, event, chain=self._chained_clicks
                            )

                            self._click_chain_last_time = event.time
                            self._click_chain_last_offset = screen_offset

                            self.screen._forward_event(click_event)
                    except NoWidget:
                        pass

            elif isinstance(event, events.Key):
                # Special case for maximized widgets
                # If something is maximized, then escape should minimize
                if (
                    self.screen.maximized is not None
                    and event.key == "escape"
                    and self.escape_to_minimize
                ):
                    self.screen.minimize()
                    return
                if self.focused:
                    try:
                        self.screen._clear_tooltip()
                    except NoScreen:
                        pass
                if not await self._check_bindings(event.key, priority=True):
                    forward_target = self.focused or self.screen
                    forward_target._forward_event(event)
            else:
                self.screen._forward_event(event)

        elif isinstance(event, events.Paste) and not event.is_forwarded:
            if self.focused is not None:
                self.focused._forward_event(event)
            else:
                self.screen._forward_event(event)
        else:
            await super().on_event(event)
```

### 🔹 函式: `App.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, driver_class: Type[Driver] | None = None, css_path: CSSPathType | None = None, watch_css: bool = False, ansi_color: bool = False, )` (L560~L872)
- **變更後簽章 (After)**: `def __init__( self, driver_class: Type[Driver] | None = None, css_path: CSSPathType | None = None, watch_css: bool = False, ansi_color: bool = False, )` (L560~L877)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        driver_class: Type[Driver] | None = None,
        css_path: CSSPathType | None = None,
        watch_css: bool = False,
        ansi_color: bool = False,
    ):
        """Create an instance of an app.

        Args:
            driver_class: Driver class or `None` to auto-detect.
                This will be used by some Textual tools.
            css_path: Path to CSS or `None` to use the `CSS_PATH` class variable.
                To load multiple CSS files, pass a list of strings or paths which
                will be loaded in order.
            watch_css: Reload CSS if the files changed. This is set automatically if
                you are using `textual run` with the `dev` switch.
            ansi_color: Allow ANSI colors if `True`, or convert ANSI colors to RGB if `False`.

        Raises:
            CssPathError: When the supplied CSS path(s) are an unexpected type.
        """
        self._start_time = perf_counter()
        super().__init__(classes=self.DEFAULT_CLASSES)
        self.features: frozenset[FeatureFlag] = parse_features(os.getenv("TEXTUAL", ""))

        self._registered_themes: dict[str, Theme] = {}
        """Themes that have been registered with the App using `App.register_theme`.
        
        This excludes the built-in themes."""

        for theme in BUILTIN_THEMES.values():
            self.register_theme(theme)

        ansi_theme = (
            self.ansi_theme_dark if self.current_theme.dark else self.ansi_theme_light
        )
        self.set_reactive(App.ansi_color, ansi_color)
        self._filters: list[LineFilter] = [
            ANSIToTruecolor(ansi_theme, enabled=not ansi_color)
        ]
        environ = dict(os.environ)
        self.no_color = environ.pop("NO_COLOR", None) is not None
        if self.no_color:
            self._filters.append(NoColor() if self.ansi_color else Monochrome())

        for filter_name in constants.FILTERS.split(","):
            filter = filter_name.lower().strip()
            if filter == "dim":
                self._filters.append(DimFilter())

        self.console = Console(
            color_system=constants.COLOR_SYSTEM,
            file=_NullFile(),
            markup=True,
            highlight=False,
            emoji=False,
            legacy_windows=False,
            _environ=environ,
            force_terminal=True,
            safe_box=False,
            soft_wrap=False,
        )
        self._workers = WorkerManager(self)
        self.error_console = Console(markup=False, highlight=False, stderr=True)
        self.driver_class = driver_class or self.get_driver_class()
        self._screen_stacks: dict[str, list[Screen[Any]]] = {self.DEFAULT_MODE: []}
        """A stack of screens per mode."""
        self._current_mode: str = self.DEFAULT_MODE
        """The current mode the app is in."""
        self._sync_available = False

        self.mouse_over: Widget | None = None
        """The widget directly under the mouse."""
        self.hover_over: Widget | None = None
        """The first widget with a hover style under the mouse."""
        self.mouse_captured: Widget | None = None
        self._driver: Driver | None = None
        self._exit_renderables: list[RenderableType] = []

        self._action_targets = {"app", "screen", "focused"}
        self._animator = Animator(self)
        self._animate = self._animator.bind(self)
        self.mouse_position = Offset(0, 0)

        self._mouse_down_widget: Widget | None = None
        """The widget that was most recently mouse downed (used to create click events)."""

        self._click_chain_last_offset: Offset | None = None
        """The last offset at which a Click occurred, in screen-space."""

        self._click_chain_last_time: float | None = None
        """The last time at which a Click occurred."""

        self._chained_clicks: int = 1
        """Counter which tracks the number of clicks received in a row."""

        self._previous_cursor_position = Offset(0, 0)
        """The previous cursor position"""

        self.cursor_position = Offset(0, 0)
        """The position of the terminal cursor in screen-space.

        This can be set by widgets and is useful for controlling the
        positioning of OS IME and emoji popup menus."""

        self._exception: Exception | None = None
        """The unhandled exception which is leading to the app shutting down,
        or None if the app is still running with no unhandled exceptions."""

        self.title = (
            self.TITLE if self.TITLE is not None else f"{self.__class__.__name__}"
        )
        """The title for the application.

        The initial value for `title` will be set to the `TITLE` class variable if it exists, or
        the name of the app if it doesn't.

        Assign a new value to this attribute to change the title.
        The new value is always converted to string.
        """

        self.sub_title = self.SUB_TITLE if self.SUB_TITLE is not None else ""
        """The sub-title for the application.

        The initial value for `sub_title` will be set to the `SUB_TITLE` class variable if it exists, or
        an empty string if it doesn't.

        Sub-titles are typically used to show the high-level state of the app, such as the current mode, or path to
        the file being worked on.

        Assign a new value to this attribute to change the sub-title.
        The new value is always converted to string.
        """

        self.use_command_palette: bool = self.ENABLE_COMMAND_PALETTE
        """A flag to say if the application should use the command palette.

        If set to `False` any call to
        [`action_command_palette`][textual.app.App.action_command_palette]
        will be ignored.
        """

        self._logger = Logger(self._log, app=self)

        self._css_has_errors = False

        self.theme_variables: dict[str, str] = {}
        """Variables generated from the current theme."""

        # Note that the theme must be set *before* self.get_css_variables() is called
        # to ensure that the variables are retrieved from the currently active theme.
        self.stylesheet = Stylesheet(variables=self.get_css_variables())

        css_path = css_path or self.CSS_PATH
        css_paths = [
            _make_path_object_relative(css_path, self)
            for css_path in (
                _css_path_type_as_list(css_path) if css_path is not None else []
            )
        ]
        self.css_path = css_paths

        self._registry: WeakSet[DOMNode] = WeakSet()

        self._keymap: Keymap = {}

        # Sensitivity on X is double the sensitivity on Y to account for
        # cells being twice as tall as wide
        self.scroll_sensitivity_x: float = 4.0
        """Number of columns to scroll in the X direction with wheel or trackpad."""
        self.scroll_sensitivity_y: float = 2.0
        """Number of lines to scroll in the Y direction with wheel or trackpad."""

        self._installed_screens: dict[str, Screen | Callable[[], Screen]] = {}
        self._installed_screens.update(**self.SCREENS)
        self._modes: dict[str, str | Callable[[], Screen]] = self.MODES.copy()
        """Contains the working-copy of the `MODES` for each instance."""

        self._compose_stacks: list[list[Widget]] = []
        self._composed: list[list[Widget]] = []
        self._recompose_required = False

        self.devtools: DevtoolsClient | None = None
        self._devtools_redirector: StdoutRedirector | None = None
        if "devtools" in self.features:
            try:
                from textual_dev.client import DevtoolsClient
                from textual_dev.redirect_output import StdoutRedirector
            except ImportError:
                # Dev dependencies not installed
                pass
            else:
                self.devtools = DevtoolsClient(constants.DEVTOOLS_HOST)
                self._devtools_redirector = StdoutRedirector(self.devtools)

        self._loop: asyncio.AbstractEventLoop | None = None
        self._return_value: ReturnType | None = None
        """Internal attribute used to set the return value for the app."""
        self._return_code: int | None = None
        """Internal attribute used to set the return code for the app."""
        self._exit = False
        self._disable_tooltips = False
        self._disable_notifications = False

        self.css_monitor = (
            FileMonitor(self.css_path, self._on_css_change)
            if watch_css or self.debug
            else None
        )
        self._screenshot: str | None = None
        self._dom_ready = False
        self._batch_count = 0
        self._notifications = Notifications()

        self._capture_print: WeakKeyDictionary[MessageTarget, tuple[bool, bool]] = (
            WeakKeyDictionary()
        )
        """Registry of the MessageTargets which are capturing output at any given time."""
        self._capture_stdout = _PrintCapture(self, stderr=False)
        """File-like object capturing data written to stdout."""
        self._capture_stderr = _PrintCapture(self, stderr=True)
        """File-like object capturing data written to stderr."""
        self._original_stdout = sys.__stdout__
        """The original stdout stream (before redirection etc)."""
        self._original_stderr = sys.__stderr__
        """The original stderr stream (before redirection etc)."""

        self.theme_changed_signal: Signal[Theme] = Signal(self, "theme-changed")
        """Signal that is published when the App's theme is changed.
        
        Subscribers will receive the new theme object as an argument to the callback.
        """

        self.app_suspend_signal: Signal[App] = Signal(self, "app-suspend")
        """The signal that is published when the app is suspended.

        When [`App.suspend`][textual.app.App.suspend] is called this signal
        will be [published][textual.signal.Signal.publish];
        [subscribe][textual.signal.Signal.subscribe] to this signal to
        perform work before the suspension takes place.
        """
        self.app_resume_signal: Signal[App] = Signal(self, "app-resume")
        """The signal that is published when the app is resumed after a suspend.

        When the app is resumed after a
        [`App.suspend`][textual.app.App.suspend] call this signal will be
        [published][textual.signal.Signal.publish];
        [subscribe][textual.signal.Signal.subscribe] to this signal to
        perform work after the app has resumed.
        """

        self.mode_change_signal: Signal[str] = Signal(self, "mode-change")
        """A signal published when the current screen mode changes."""

        self.screen_change_signal: Signal[Screen] = Signal(self, "screen-change")
        """A signal published when the current screen changes."""

        self.set_class(self.current_theme.dark, "-dark-mode", update=False)
        self.set_class(not self.current_theme.dark, "-light-mode", update=False)

        self.animation_level: AnimationLevel = constants.TEXTUAL_ANIMATIONS
        """Determines what type of animations the app will display.

        See [`textual.constants.TEXTUAL_ANIMATIONS`][textual.constants.TEXTUAL_ANIMATIONS].
        """

        self._last_focused_on_app_blur: Widget | None = None
        """The widget that had focus when the last `AppBlur` happened.

        This will be used to restore correct focus when an `AppFocus`
        happens.
        """

        self._previous_inline_height: int | None = None
        """Size of previous inline update."""

        self._resize_event: events.Resize | None = None
        """A pending resize event, sent on idle."""

        self._size: Size | None = None

        self._css_update_count: int = 0
        """Incremented when CSS is invalidated."""

        self._clipboard: str = ""
        """Contents of local clipboard."""

        self.supports_smooth_scrolling: bool = False
        """Does the terminal support smooth scrolling?"""

        self._compose_screen: Screen | None = None
        """The screen composed by App.compose."""

        self._realtime_animation_count = 0
        """Number of current realtime animations, such as scrolling."""

        if self.ENABLE_COMMAND_PALETTE:
            for _key, binding in self._bindings:
                if binding.action in {"command_palette", "app.command_palette"}:
                    break
            else:
                self._bindings._add_binding(
                    Binding(
                        self.COMMAND_PALETTE_BINDING,
                        "command_palette",
                        "palette",
                        show=False,
                        key_display=self.COMMAND_PALETTE_DISPLAY,
                        priority=True,
                        tooltip="Open the command palette",
                    )
                )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        driver_class: Type[Driver] | None = None,
        css_path: CSSPathType | None = None,
        watch_css: bool = False,
        ansi_color: bool = False,
    ):
        """Create an instance of an app.

        Args:
            driver_class: Driver class or `None` to auto-detect.
                This will be used by some Textual tools.
            css_path: Path to CSS or `None` to use the `CSS_PATH` class variable.
                To load multiple CSS files, pass a list of strings or paths which
                will be loaded in order.
            watch_css: Reload CSS if the files changed. This is set automatically if
                you are using `textual run` with the `dev` switch.
            ansi_color: Allow ANSI colors if `True`, or convert ANSI colors to RGB if `False`.

        Raises:
            CssPathError: When the supplied CSS path(s) are an unexpected type.
        """
        self._start_time = perf_counter()
        super().__init__(classes=self.DEFAULT_CLASSES)
        self.features: frozenset[FeatureFlag] = parse_features(os.getenv("TEXTUAL", ""))

        self._registered_themes: dict[str, Theme] = {}
        """Themes that have been registered with the App using `App.register_theme`.
        
        This excludes the built-in themes."""

        for theme in BUILTIN_THEMES.values():
            self.register_theme(theme)

        ansi_theme = (
            self.ansi_theme_dark if self.current_theme.dark else self.ansi_theme_light
        )
        self.set_reactive(App.ansi_color, ansi_color)
        self._filters: list[LineFilter] = [
            ANSIToTruecolor(ansi_theme, enabled=not ansi_color)
        ]
        environ = dict(os.environ)
        self.no_color = environ.pop("NO_COLOR", None) is not None
        if self.no_color:
            self._filters.append(NoColor() if self.ansi_color else Monochrome())

        for filter_name in constants.FILTERS.split(","):
            filter = filter_name.lower().strip()
            if filter == "dim":
                self._filters.append(DimFilter())

        self.console = Console(
            color_system=constants.COLOR_SYSTEM,
            file=_NullFile(),
            markup=True,
            highlight=False,
            emoji=False,
            legacy_windows=False,
            _environ=environ,
            force_terminal=True,
            safe_box=False,
            soft_wrap=False,
        )
        self._workers = WorkerManager(self)
        self.error_console = Console(markup=False, highlight=False, stderr=True)
        self.driver_class = driver_class or self.get_driver_class()
        self._screen_stacks: dict[str, list[Screen[Any]]] = {self.DEFAULT_MODE: []}
        """A stack of screens per mode."""
        self._current_mode: str = self.DEFAULT_MODE
        """The current mode the app is in."""
        self._sync_available = False

        self.mouse_over: Widget | None = None
        """The widget directly under the mouse."""
        self.hover_over: Widget | None = None
        """The first widget with a hover style under the mouse."""
        self.mouse_captured: Widget | None = None
        self._driver: Driver | None = None
        self._exit_renderables: list[RenderableType] = []

        self._action_targets = {"app", "screen", "focused"}
        self._animator = Animator(self)
        self._animate = self._animator.bind(self)

        self.mouse_position = Offset(0, 0)
        """The current screen-space mouse position."""

        self.mouse_position_high_resolution: tuple[float, float] = (0.0, 0.0)
        """A high resolution (floating point) mouse position. If supported by the terminal, this may be more granular than `mouse_position`"""

        self._mouse_down_widget: Widget | None = None
        """The widget that was most recently mouse downed (used to create click events)."""

        self._click_chain_last_offset: Offset | None = None
        """The last offset at which a Click occurred, in screen-space."""

        self._click_chain_last_time: float | None = None
        """The last time at which a Click occurred."""

        self._chained_clicks: int = 1
        """Counter which tracks the number of clicks received in a row."""

        self._previous_cursor_position = Offset(0, 0)
        """The previous cursor position"""

        self.cursor_position = Offset(0, 0)
        """The position of the terminal cursor in screen-space.

        This can be set by widgets and is useful for controlling the
        positioning of OS IME and emoji popup menus."""

        self._exception: Exception | None = None
        """The unhandled exception which is leading to the app shutting down,
        or None if the app is still running with no unhandled exceptions."""

        self.title = (
            self.TITLE if self.TITLE is not None else f"{self.__class__.__name__}"
        )
        """The title for the application.

        The initial value for `title` will be set to the `TITLE` class variable if it exists, or
        the name of the app if it doesn't.

        Assign a new value to this attribute to change the title.
        The new value is always converted to string.
        """

        self.sub_title = self.SUB_TITLE if self.SUB_TITLE is not None else ""
        """The sub-title for the application.

        The initial value for `sub_title` will be set to the `SUB_TITLE` class variable if it exists, or
        an empty string if it doesn't.

        Sub-titles are typically used to show the high-level state of the app, such as the current mode, or path to
        the file being worked on.

        Assign a new value to this attribute to change the sub-title.
        The new value is always converted to string.
        """

        self.use_command_palette: bool = self.ENABLE_COMMAND_PALETTE
        """A flag to say if the application should use the command palette.

        If set to `False` any call to
        [`action_command_palette`][textual.app.App.action_command_palette]
        will be ignored.
        """

        self._logger = Logger(self._log, app=self)

        self._css_has_errors = False

        self.theme_variables: dict[str, str] = {}
        """Variables generated from the current theme."""

        # Note that the theme must be set *before* self.get_css_variables() is called
        # to ensure that the variables are retrieved from the currently active theme.
        self.stylesheet = Stylesheet(variables=self.get_css_variables())

        css_path = css_path or self.CSS_PATH
        css_paths = [
            _make_path_object_relative(css_path, self)
            for css_path in (
                _css_path_type_as_list(css_path) if css_path is not None else []
            )
        ]
        self.css_path = css_paths

        self._registry: WeakSet[DOMNode] = WeakSet()

        self._keymap: Keymap = {}

        # Sensitivity on X is double the sensitivity on Y to account for
        # cells being twice as tall as wide
        self.scroll_sensitivity_x: float = 4.0
        """Number of columns to scroll in the X direction with wheel or trackpad."""
        self.scroll_sensitivity_y: float = 2.0
        """Number of lines to scroll in the Y direction with wheel or trackpad."""

        self._installed_screens: dict[str, Screen | Callable[[], Screen]] = {}
        self._installed_screens.update(**self.SCREENS)
        self._modes: dict[str, str | Callable[[], Screen]] = self.MODES.copy()
        """Contains the working-copy of the `MODES` for each instance."""

        self._compose_stacks: list[list[Widget]] = []
        self._composed: list[list[Widget]] = []
        self._recompose_required = False

        self.devtools: DevtoolsClient | None = None
        self._devtools_redirector: StdoutRedirector | None = None
        if "devtools" in self.features:
            try:
                from textual_dev.client import DevtoolsClient
                from textual_dev.redirect_output import StdoutRedirector
            except ImportError:
                # Dev dependencies not installed
                pass
            else:
                self.devtools = DevtoolsClient(constants.DEVTOOLS_HOST)
                self._devtools_redirector = StdoutRedirector(self.devtools)

        self._loop: asyncio.AbstractEventLoop | None = None
        self._return_value: ReturnType | None = None
        """Internal attribute used to set the return value for the app."""
        self._return_code: int | None = None
        """Internal attribute used to set the return code for the app."""
        self._exit = False
        self._disable_tooltips = False
        self._disable_notifications = False

        self.css_monitor = (
            FileMonitor(self.css_path, self._on_css_change)
            if watch_css or self.debug
            else None
        )
        self._screenshot: str | None = None
        self._dom_ready = False
        self._batch_count = 0
        self._notifications = Notifications()

        self._capture_print: WeakKeyDictionary[MessageTarget, tuple[bool, bool]] = (
            WeakKeyDictionary()
        )
        """Registry of the MessageTargets which are capturing output at any given time."""
        self._capture_stdout = _PrintCapture(self, stderr=False)
        """File-like object capturing data written to stdout."""
        self._capture_stderr = _PrintCapture(self, stderr=True)
        """File-like object capturing data written to stderr."""
        self._original_stdout = sys.__stdout__
        """The original stdout stream (before redirection etc)."""
        self._original_stderr = sys.__stderr__
        """The original stderr stream (before redirection etc)."""

        self.theme_changed_signal: Signal[Theme] = Signal(self, "theme-changed")
        """Signal that is published when the App's theme is changed.
        
        Subscribers will receive the new theme object as an argument to the callback.
        """

        self.app_suspend_signal: Signal[App] = Signal(self, "app-suspend")
        """The signal that is published when the app is suspended.

        When [`App.suspend`][textual.app.App.suspend] is called this signal
        will be [published][textual.signal.Signal.publish];
        [subscribe][textual.signal.Signal.subscribe] to this signal to
        perform work before the suspension takes place.
        """
        self.app_resume_signal: Signal[App] = Signal(self, "app-resume")
        """The signal that is published when the app is resumed after a suspend.

        When the app is resumed after a
        [`App.suspend`][textual.app.App.suspend] call this signal will be
        [published][textual.signal.Signal.publish];
        [subscribe][textual.signal.Signal.subscribe] to this signal to
        perform work after the app has resumed.
        """

        self.mode_change_signal: Signal[str] = Signal(self, "mode-change")
        """A signal published when the current screen mode changes."""

        self.screen_change_signal: Signal[Screen] = Signal(self, "screen-change")
        """A signal published when the current screen changes."""

        self.set_class(self.current_theme.dark, "-dark-mode", update=False)
        self.set_class(not self.current_theme.dark, "-light-mode", update=False)

        self.animation_level: AnimationLevel = constants.TEXTUAL_ANIMATIONS
        """Determines what type of animations the app will display.

        See [`textual.constants.TEXTUAL_ANIMATIONS`][textual.constants.TEXTUAL_ANIMATIONS].
        """

        self._last_focused_on_app_blur: Widget | None = None
        """The widget that had focus when the last `AppBlur` happened.

        This will be used to restore correct focus when an `AppFocus`
        happens.
        """

        self._previous_inline_height: int | None = None
        """Size of previous inline update."""

        self._resize_event: events.Resize | None = None
        """A pending resize event, sent on idle."""

        self._size: Size | None = None

        self._css_update_count: int = 0
        """Incremented when CSS is invalidated."""

        self._clipboard: str = ""
        """Contents of local clipboard."""

        self.supports_smooth_scrolling: bool = False
        """Does the terminal support smooth scrolling?"""

        self._compose_screen: Screen | None = None
        """The screen composed by App.compose."""

        self._realtime_animation_count = 0
        """Number of current realtime animations, such as scrolling."""

        if self.ENABLE_COMMAND_PALETTE:
            for _key, binding in self._bindings:
                if binding.action in {"command_palette", "app.command_palette"}:
                    break
            else:
                self._bindings._add_binding(
                    Binding(
                        self.COMMAND_PALETTE_BINDING,
                        "command_palette",
                        "palette",
                        show=False,
                        key_display=self.COMMAND_PALETTE_DISPLAY,
                        priority=True,
                        tooltip="Open the command palette",
                    )
                )
```


#### 📄 檔案: `src/textual/screen.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:230, E:272, A:0) ➔ After(N:221, E:258, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 10, +Edges: 1, -Edges: 15, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Offset (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `SpatialMap (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `from_corners (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `get_values_in_region (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `filter_children_overlapping_region (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `_get_scroll_container (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `union (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `Region (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `overlaps (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `log (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `from_union (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Screen._check_auto_scroll` ──[CALLS]──> `Offset (External/Unresolved)`
  • - [移除呼叫邊] `Screen._watch__select_end` ──[CALLS]──> `sorted (External/Unresolved)`
  • - [移除呼叫邊] `Screen._watch__select_end` ──[CALLS]──> `Region (External/Unresolved)`
  • - [移除呼叫邊] `Screen._watch__select_end` ──[CALLS]──> `filter_children_overlapping_region (External/Unresolved)`
  • _... 以及其餘 12 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Screen._forward_event()`
- **變更前簽章 (Before)**: `def _forward_event(self, event: events.Event) -> None` (L1826~L1944)
- **變更後簽章 (After)**: `def _forward_event(self, event: events.Event) -> None` (L1828~L1948)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _forward_event(self, event: events.Event) -> None:
        if event.is_forwarded:
            return
        event._set_forwarded()

        if isinstance(event, (events.Enter, events.Leave)):
            self.post_message(event)

        elif isinstance(event, events.MouseMove):
            event.style = self.get_style_at(event.screen_x, event.screen_y)
            self._handle_mouse_move(event)

            if self._selecting and self._select_start is not None:

                self._box_select = event.shift
                select_widget, select_offset = self.get_widget_and_offset_at(
                    event.x, event.y
                )
                if (
                    self._select_end is not None
                    and select_offset is None
                    and event.y > self._select_end[1].y
                ):
                    end_widget = self._select_end[0]
                    select_offset = end_widget.content_region.bottom_right_inclusive
                    self._select_end = (
                        end_widget,
                        event.screen_offset,
                        select_offset,
                    )

                elif (
                    select_widget is not None
                    and select_widget.allow_select
                    and select_offset is not None
                ):
                    self._select_end = (
                        select_widget,
                        event.screen_offset,
                        select_offset,
                    )

                if select_widget is not None:
                    self._check_auto_scroll(select_widget, event.screen_offset)
                else:
                    print("select widget is None")
                    self._stop_auto_scroll()

        elif isinstance(event, events.MouseEvent):
            if isinstance(event, events.MouseUp):
                if (
                    self._mouse_down_offset is not None
                    and self._mouse_down_offset == event.screen_offset
                ):
                    # A click elsewhere should clear the selection
                    select_widget, select_offset = self.get_widget_and_offset_at(
                        event.x, event.y
                    )
                    # Exclude scrollbars, so the user may navigate without clearing the selection
                    if select_widget is None or not select_widget.has_class(
                        "-textual-system"
                    ):
                        self.clear_selection()

                self._mouse_down_offset = None
                self._selecting = False
                self.post_message(events.TextSelected())

            elif isinstance(event, events.MouseDown) and not self.app.mouse_captured:
                self._box_select = event.shift
                self._mouse_down_offset = event.screen_offset
                select_widget, select_offset = self.get_widget_and_offset_at(
                    event.screen_x, event.screen_y
                )
                if (
                    select_widget is not None
                    and select_widget.allow_select
                    and self.screen.allow_select
                    and self.app.ALLOW_SELECT
                ):
                    self._selecting = True
                    if select_widget is not None and select_offset is not None:
                        self.text_selection_started_signal.publish(self)
                        self._select_start = (
                            select_widget,
                            event.screen_offset,
                            select_offset,
                        )
                else:
                    self._selecting = False

            try:
                if self.app.mouse_captured:
                    widget = self.app.mouse_captured
                    region = self.find_widget(widget).region
                else:
                    widget, region = self.get_widget_at(event.x, event.y)
            except errors.NoWidget:
                self.set_focus(None)
            else:
                if isinstance(event, events.MouseDown):
                    focusable_widget = self.get_focusable_widget_at(event.x, event.y)
                    if (
                        focusable_widget is not None
                        and focusable_widget.focus_on_click()
                    ):
                        self.set_focus(focusable_widget, scroll_visible=False)
                event.style = self.get_style_at(event.screen_x, event.screen_y)
                if widget.loading:
                    return
                if widget is self:
                    event._set_forwarded()
                    self.post_message(event)
                else:
                    widget._forward_event(event._apply_offset(-region.x, -region.y))

        else:
            self.post_message(event)
        self.update_pointer_shape()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _forward_event(self, event: events.Event) -> None:
        if event.is_forwarded:
            return
        event._set_forwarded()

        if isinstance(event, (events.Enter, events.Leave)):
            self.post_message(event)

        elif isinstance(event, events.MouseMove):
            event.style = self.get_style_at(event.screen_x, event.screen_y)
            self._handle_mouse_move(event)

            if self._selecting and self._select_start is not None:

                self._box_select = event.shift
                select_widget, select_offset = self.get_widget_and_offset_at(
                    event.x, event.y
                )
                if (
                    self._select_end is not None
                    and select_offset is None
                    and event.y > self._select_end[1].y
                ):
                    end_widget = self._select_end[0]
                    select_offset = end_widget.content_region.bottom_right_inclusive
                    self._select_end = (
                        end_widget,
                        event.screen_offset,
                        select_offset,
                    )

                elif (
                    select_widget is not None
                    and select_widget.allow_select
                    and select_offset is not None
                ):
                    self._select_end = (
                        select_widget,
                        event.screen_offset,
                        select_offset,
                    )

                if select_widget is not None:
                    self._check_auto_scroll(
                        select_widget, (event.pointer_screen_x, event.pointer_screen_y)
                    )
                else:
                    print("select widget is None")
                    self._stop_auto_scroll()

        elif isinstance(event, events.MouseEvent):
            if isinstance(event, events.MouseUp):
                if (
                    self._mouse_down_offset is not None
                    and self._mouse_down_offset == event.screen_offset
                ):
                    # A click elsewhere should clear the selection
                    select_widget, select_offset = self.get_widget_and_offset_at(
                        event.x, event.y
                    )
                    # Exclude scrollbars, so the user may navigate without clearing the selection
                    if select_widget is None or not select_widget.has_class(
                        "-textual-system"
                    ):
                        self.clear_selection()

                self._mouse_down_offset = None
                self._selecting = False
                self.post_message(events.TextSelected())

            elif isinstance(event, events.MouseDown) and not self.app.mouse_captured:
                self._box_select = event.shift
                self._mouse_down_offset = event.screen_offset
                select_widget, select_offset = self.get_widget_and_offset_at(
                    event.screen_x, event.screen_y
                )
                if (
                    select_widget is not None
                    and select_widget.allow_select
                    and self.screen.allow_select
                    and self.app.ALLOW_SELECT
                ):
                    self._selecting = True
                    if select_widget is not None and select_offset is not None:
                        self.text_selection_started_signal.publish(self)
                        self._select_start = (
                            select_widget,
                            event.screen_offset,
                            select_offset,
                        )
                else:
                    self._selecting = False

            try:
                if self.app.mouse_captured:
                    widget = self.app.mouse_captured
                    region = self.find_widget(widget).region
                else:
                    widget, region = self.get_widget_at(event.x, event.y)
            except errors.NoWidget:
                self.set_focus(None)
            else:
                if isinstance(event, events.MouseDown):
                    focusable_widget = self.get_focusable_widget_at(event.x, event.y)
                    if (
                        focusable_widget is not None
                        and focusable_widget.focus_on_click()
                    ):
                        self.set_focus(focusable_widget, scroll_visible=False)
                event.style = self.get_style_at(event.screen_x, event.screen_y)
                if widget.loading:
                    return
                if widget is self:
                    event._set_forwarded()
                    self.post_message(event)
                else:
                    widget._forward_event(event._apply_offset(-region.x, -region.y))

        else:
            self.post_message(event)
        self.update_pointer_shape()
```

### 🔹 函式: `Screen._watch__select_end()`
- **變更前簽章 (Before)**: `def _watch__select_end( self, select_end: tuple[Widget, Offset, Offset] | None ) -> None` (L1995~L2219)
- **變更後簽章 (After)**: `def _watch__select_end( self, select_end: tuple[Widget, Offset, Offset] | None ) -> None` (L1999~L2063)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _watch__select_end(
        self, select_end: tuple[Widget, Offset, Offset] | None
    ) -> None:
        """When select_end changes, we need to compute which widgets and regions are selected.

        Args:
            select_end: The end selection.
        """

        if select_end is None or self._select_start is None:
            # Nothing to select
            return

        start_widget, screen_start, start_offset = self._select_start

        end_widget, screen_end, end_offset = select_end
        if start_widget is end_widget:
            # Simplest case, selection starts and ends on the same widget
            self.selections = {
                start_widget: Selection.from_offsets(
                    start_offset,
                    end_offset + (1, 0),
                )
            }
            return

        # The start selection may have been scrolled since it was saved
        # We need to adjust to the new screen-space position
        select_start = (start_widget, start_widget.region.offset, start_offset)

        bounds_start, bounds_end = sorted(
            [select_start[1] + select_start[2], self.app.mouse_position],
            key=lambda bounds: bounds.transpose,
        )

        selection_bounds = Shape.selection_bounds(
            self.size.region, bounds_start, bounds_end
        )

        if start_widget.region.offset.transpose > end_widget.region.offset.transpose:
            start_widget, end_widget = end_widget, start_widget

        container_widget = Widget.get_common_ancestor(start_widget, end_widget)

        select_widgets = self._collect_select_widgets(
            selection_bounds, container_widget, start_widget, end_widget
        )

        select_all = SELECT_ALL

        self.selections = {widget: SELECT_ALL for widget in select_widgets}

        # selections: dict[Widget, Selection] = {}
        # for widget, map_geometry in self._compositor.full_map.items():
        #     if selection_bounds.overlaps(map_geometry.region):
        #         selections[widget] = select_all

        # self.selections = selections

        # start_widget, end_widget = sorted(
        #     [start_widget, end_widget],
        #     key=lambda widget: widget.region.offset.transpose,
        # )

        return

        mouse_position = self.app.mouse_position
        selection_start_offset = start_widget.region.offset + start_offset
        selection_end_offset = mouse_position

        (start_widget, selection_start_offset), (end_widget, selection_end_offset) = (
            sorted(
                [
                    (start_widget, selection_start_offset),
                    (end_widget, selection_end_offset),
                ],
                key=lambda widget_offset: widget_offset[1].transpose,
            )
        )

        # print(selection_start_offset, selection_end_offset)
        # select_region = Region.from_corners(
        #     *selection_start_offset, *selection_end_offset
        # )

        select_container = start_widget.select_container
        select_region = Region(
            0,
            selection_start_offset.y,
            select_container.region.width,
            selection_end_offset.y - selection_start_offset.y,
        )

        parent_select_widgets = select_container.filter_children_overlapping_region(
            select_region
        )

        select_widgets = set(
            self._collect_select_widgets(select_region, parent_select_widgets)
        )
        select_widgets -= {self, start_widget, end_widget}

        select_all = SELECT_ALL

        self.selections = {
            start_widget: Selection(start_offset, None),
            **{
                widget: select_all
                for widget in sorted(
                    select_widgets,
                    key=lambda widget: widget.content_region.offset.transpose,
                )
            },
            end_widget: Selection(None, end_offset),
        }

        return

        screen_start = start_widget.region.offset
        print("START", screen_start)

        select_container = start_widget.select_container

        # select_container.region.intersection(
        #     Region.from_corners(select_container)
        # )

        screen_start, screen_end = sorted(
            [screen_start, screen_end],
            key=lambda offset: offset.transpose,
        )
        print(start_offset, end_offset)
        select_region = Region.from_corners(*start_offset, *end_offset)

        print(select_region)
        # select_widgets:list[Widget] = []
        # for widget in self.filter_children_overlapping_region(select_container.region):

        # select_container = start_widget.select_container

        # for widget in select_container:

        return
        select_start, select_end = sorted(
            [select_start, select_end],
            key=lambda selection: (selection[0].region.offset.transpose),
        )

        start_widget, _screen_start, start_offset = select_start
        end_widget, _screen_end, end_offset = select_end
        end_offset += (1, 0)

        select_regions: list[Region] = []
        start_region = start_widget.content_region
        end_region = end_widget.content_region
        if end_region.y <= start_region.bottom or self._box_select:
            select_regions.append(Region.union(start_region, end_region))
        else:
            try:
                container_region = Region.from_union(
                    [
                        start_widget.select_container.content_region,
                        end_widget.select_container.content_region,
                    ]
                )
            except NoMatches:
                return

            start_region = Region.from_corners(
                start_region.x,
                start_region.y,
                container_region.right,
                start_region.bottom,
            )
            end_region = Region.from_corners(
                container_region.x,
                end_region.y,
                end_region.right,
                end_region.bottom,
            )
            select_regions.append(start_region)
            select_regions.append(end_region)
            mid_height = end_region.y - start_region.bottom
            if mid_height > 0:
                mid_region = Region.from_corners(
                    container_region.x,
                    start_region.bottom,
                    container_region.right,
                    start_region.bottom + mid_height,
                )
                select_regions.append(mid_region)

        scroll_container = self._get_scroll_container(start_widget)
        print("scroll_container", scroll_container)
        widgets = list(scroll_container.query("*"))

        spatial_map: SpatialMap[Widget] = SpatialMap()
        spatial_map.insert(
            [(widget.region, NULL_OFFSET, False, False, widget) for widget in widgets]
        )

        highlighted_widgets: set[Widget] = set()
        for region in select_regions:
            covered_widgets = spatial_map.get_values_in_region(region)
            covered_widgets = [
                widget
                for widget in covered_widgets
                if region.overlaps(widget.content_region)
            ]
            highlighted_widgets.update(covered_widgets)
        highlighted_widgets -= {self, start_widget, end_widget}

        select_all = SELECT_ALL
        self.selections = {
            start_widget: Selection(start_offset, None),
            **{
                widget: select_all
                for widget in sorted(
                    highlighted_widgets,
                    key=lambda widget: widget.content_region.offset.transpose,
                )
            },
            end_widget: Selection(None, end_offset),
        }
        self.log(self.selections)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _watch__select_end(
        self, select_end: tuple[Widget, Offset, Offset] | None
    ) -> None:
        """When select_end changes, we need to compute which widgets and regions are selected.

        Args:
            select_end: The end selection.
        """

        if select_end is None or self._select_start is None:
            # Nothing to select
            return

        start_widget, screen_start, start_offset = self._select_start
        end_widget, screen_end, end_offset = select_end

        if start_widget is end_widget:
            # Simplest case, selection starts and ends on the same widget
            self.selections = {
                start_widget: Selection.from_offsets(
                    start_offset,
                    end_offset + (1, 0),
                )
            }
            return

        # The start selection may have been scrolled since it was saved
        # We need to adjust to the new screen-space position
        select_start = (start_widget, start_widget.region.offset, start_offset)

        if select_start[0]._selection_order > select_end[0]._selection_order:
            select_start, select_end = select_end, select_start

        start_widget, screen_start, start_offset = select_start
        end_widget, screen_end, end_offset = select_end

        if (screen_start + start_offset).transpose > (
            screen_end + end_offset
        ).transpose:
            start_widget, end_widget = end_widget, start_widget

        container_widget = Widget.get_common_ancestor(start_widget, end_widget)

        bounds_start = select_start[1] + select_start[2]
        bounds_end = self.app.mouse_position
        if bounds_end.transpose < bounds_start.transpose:
            bounds_end, bounds_start = bounds_start, bounds_end

        selection_bounds = Shape.selection_bounds(
            container_widget.region, bounds_start, bounds_end
        )

        select_widgets = self._collect_select_widgets(
            selection_bounds,
            container_widget,
            start_widget,
            end_widget,
        )

        select_all = SELECT_ALL
        self.selections = {
            start_widget: Selection(start_offset, None),
            **{widget: select_all for widget in select_widgets},
            end_widget: Selection(None, end_offset + (1, 0)),
        }
```

### 🔹 函式: `Screen._collect_select_widgets()`
- **變更前簽章 (Before)**: `def _collect_select_widgets( cls, selection_bounds: Shape, container: Widget, start_widget: Widget, end_widget: Widget, ) -> list[Widget]` (L1954~L1993)
- **變更後簽章 (After)**: `def _collect_select_widgets( cls, selection_bounds: Shape, container: Widget, start_widget: Widget, end_widget: Widget, ) -> list[Widget]` (L1958~L1997)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _collect_select_widgets(
        cls,
        selection_bounds: Shape,
        container: Widget,
        start_widget: Widget,
        end_widget: Widget,
    ) -> list[Widget]:
        """Get widgets between two widgets (inclusive).

        Args:
            container: A parent widgets.
            start_widget: First widget.
            end_widget: Second widget.

        Returns:
            Widgets between start and end, in select sort order.
        """

        widgets = list(
            walk_selectable_widgets(
                container,
                selection_bounds,
                {start_widget, end_widget},
            )
        )

        index1: int | None = None
        index2: int | None = None
        try:
            index1 = widgets.index(start_widget)
        except ValueError:
            pass

        try:
            index2 = widgets.index(end_widget) + 1
        except ValueError:
            pass

        results = widgets[index1:index2]
        return results
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _collect_select_widgets(
        cls,
        selection_bounds: Shape,
        container: Widget,
        start_widget: Widget,
        end_widget: Widget,
    ) -> list[Widget]:
        """Get widgets between two widgets (inclusive).

        Args:
            container: A parent widgets.
            start_widget: First widget.
            end_widget: Second widget.

        Returns:
            Widgets between start and end, in select sort order.
        """

        widgets = list(
            walk_selectable_widgets(
                container,
                selection_bounds,
                {start_widget, end_widget},
            )
        )

        index1: int | None = None
        try:
            index1 = widgets.index(start_widget) + 1
        except ValueError:
            pass

        index2: int | None = None
        try:
            index2 = widgets.index(end_widget)
        except ValueError:
            pass

        results = widgets[index1:index2]
        return results
```

### 🔹 函式: `Screen._check_auto_scroll()`
- **變更前簽章 (Before)**: `def _check_auto_scroll( self, select_widget: Widget, mouse_coordinate: Offset ) -> None` (L1741~L1789)
- **變更後簽章 (After)**: `def _check_auto_scroll( self, select_widget: Widget, mouse_coordinate: tuple[float, float] ) -> None` (L1740~L1791)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _check_auto_scroll(
        self, select_widget: Widget, mouse_coordinate: Offset
    ) -> None:
        """Check auto-scrolling when selecting.

        This will start, update, or stop a timer used to move the scroll position.

        Args:
            select_widget: The widget under the mouise pointer.
            mouse_coordinate: The screen-space mouse pointer.
        """

        if not self.app.ENABLE_SELECT_AUTO_SCROLL:
            # Disabled by app
            return

        # We want to find any scrollable regions further up the DOM,
        # and apply auto scrolling if we are in a region at the top or bottom
        for ancestor in select_widget.ancestors_with_self:
            if not isinstance(ancestor, Widget):
                break
            if not ancestor.allow_vertical_scroll:
                # Can't scroll, so check the next ancestor
                continue
            ancestor_region = ancestor.content_region
            scroll_lines = self.app.SELECT_AUTO_SCROLL_LINES
            up_region, down_region = get_auto_scroll_regions(
                ancestor_region,
                auto_scroll_lines=scroll_lines,
            )
            if mouse_coordinate in up_region:
                # Mouse is in the up region
                if ancestor.scroll_y > 0:
                    # And there is room to scroll
                    # Speed increases the closer we are to the edge
                    speed = (
                        (scroll_lines - (mouse_coordinate.y - up_region.y))
                    ) / scroll_lines
                    self._start_auto_scroll(ancestor, -1, speed)
                    return
            elif mouse_coordinate in down_region:
                # Mouse is in the down region
                if ancestor.scroll_y < ancestor.max_scroll_y:
                    # And there is room to scroll
                    speed = (mouse_coordinate.y - down_region.y + 1) / scroll_lines
                    self._start_auto_scroll(ancestor, +1, speed)
                    return
        # Nothing to auto scroll, so stop the timer
        self._stop_auto_scroll()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _check_auto_scroll(
        self, select_widget: Widget, mouse_coordinate: tuple[float, float]
    ) -> None:
        """Check auto-scrolling when selecting.

        This will start, update, or stop a timer used to move the scroll position.

        Args:
            select_widget: The widget under the mouise pointer.
            mouse_coordinate: The screen-space mouse pointer.
        """

        if not self.app.ENABLE_SELECT_AUTO_SCROLL:
            # Disabled by app
            return

        mouse_x, mouse_y = mouse_coordinate
        mouse_offset = Offset(int(mouse_x), int(mouse_y))

        # We want to find any scrollable regions further up the DOM,
        # and apply auto scrolling if we are in a region at the top or bottom
        for ancestor in select_widget.ancestors_with_self:
            if not isinstance(ancestor, Widget):
                break
            if not ancestor.allow_vertical_scroll:
                # Can't scroll, so check the next ancestor
                continue
            ancestor_region = ancestor.content_region
            scroll_lines = self.app.SELECT_AUTO_SCROLL_LINES
            up_region, down_region = get_auto_scroll_regions(
                ancestor_region,
                auto_scroll_lines=scroll_lines,
            )
            if mouse_offset in up_region:
                # Mouse is in the up region
                if ancestor.scroll_y > 0:
                    # And there is room to scroll
                    # Speed increases the closer we are to the edge
                    speed = (scroll_lines - (mouse_y - up_region.y)) / scroll_lines
                    if speed:
                        self._start_auto_scroll(ancestor, -1, speed)
                        return
            elif mouse_offset in down_region:
                # Mouse is in the down region
                if ancestor.scroll_y < ancestor.max_scroll_y:
                    # And there is room to scroll
                    speed = (mouse_y - down_region.y) / scroll_lines
                    if speed:
                        self._start_auto_scroll(ancestor, +1, speed)
                        return
        # Nothing to auto scroll, so stop the timer
        self._stop_auto_scroll()
```


#### 📄 檔案: `src/textual/walk.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:20, E:17, A:0) ➔ After(N:21, E:18, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `attrgetter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `get_children` ──[CALLS]──> `attrgetter (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `get_children()`
- **變更前簽章 (Before)**: `def get_children(node: DOMNode) -> list[Widget]` (L192~L207)
- **變更後簽章 (After)**: `def get_children(node: DOMNode) -> list[Widget]` (L193~L207)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def get_children(node: DOMNode) -> list[Widget]:
        """Get children, sorted in selection order, and potentially filtered by selection bounds.

        Args:
            node: A root node.

        Returns:
            A list of child widgets.
        """
        children = sorted(
            node.displayed_and_visible_children,
            key=lambda node: node.region.offset.transpose,
        )
        if node in bounded:
            children = [child for child in children if bounds.overlaps(child.region)]
        return children
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def get_children(node: DOMNode) -> list[Widget]:
        """Get children, sorted in selection order, and potentially filtered by selection bounds.

        Args:
            node: A root node.

        Returns:
            A list of child widgets.
        """
        children = sorted(
            node.displayed_and_visible_children, key=attrgetter("_selection_order")
        )
        if node in bounded:
            children = [child for child in children if bounds.overlaps(child.region)]
        return children
```

### 🔹 函式: `walk_selectable_widgets()`
- **變更前簽章 (Before)**: `def walk_selectable_widgets( root: DOMNode, bounds: Shape, bounded: set[DOMNode] ) -> Iterable[Widget]` (L175~L218)
- **變更後簽章 (After)**: `def walk_selectable_widgets( root: DOMNode, bounds: Shape, bounded: set[DOMNode] ) -> Iterable[Widget]` (L176~L218)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def walk_selectable_widgets(
    root: DOMNode, bounds: Shape, bounded: set[DOMNode]
) -> Iterable[Widget]:
    """Walk the tree depth first in select order (top to bottom, then left to right).

    Args:
        root: The root note (starting point).
        bounds: A Shape object that defines the selection bounds.
        bounded: Container widgets that require a bounds check.

    Returns:
        An iterable of DOMNodes.
    """
    stack: list[Iterator[Widget]] = [iter(root.children)]
    pop = stack.pop
    push = stack.append

    def get_children(node: DOMNode) -> list[Widget]:
        """Get children, sorted in selection order, and potentially filtered by selection bounds.

        Args:
            node: A root node.

        Returns:
            A list of child widgets.
        """
        children = sorted(
            node.displayed_and_visible_children,
            key=lambda node: node.region.offset.transpose,
        )
        if node in bounded:
            children = [child for child in children if bounds.overlaps(child.region)]
        return children

    children = get_children(root)

    while stack:
        if (node := next(stack[-1], None)) is None:
            pop()
        else:
            yield node
            children = get_children(node)
            if children:
                push(iter(children))
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def walk_selectable_widgets(
    root: DOMNode, bounds: Shape, bounded: set[DOMNode]
) -> Iterable[Widget]:
    """Walk the tree depth first in select order (top to bottom, then left to right).

    Args:
        root: The root note (starting point).
        bounds: A Shape object that defines the selection bounds.
        bounded: Container widgets that require a bounds check.

    Returns:
        An iterable of DOMNodes.
    """
    stack: list[Iterator[Widget]] = [iter(root.children)]
    pop = stack.pop
    push = stack.append

    def get_children(node: DOMNode) -> list[Widget]:
        """Get children, sorted in selection order, and potentially filtered by selection bounds.

        Args:
            node: A root node.

        Returns:
            A list of child widgets.
        """
        children = sorted(
            node.displayed_and_visible_children, key=attrgetter("_selection_order")
        )
        if node in bounded:
            children = [child for child in children if bounds.overlaps(child.region)]
        return children

    children = get_children(root)

    while stack:
        if (node := next(stack[-1], None)) is None:
            pop()
        else:
            yield node
            children = get_children(node)
            if children:
                push(iter(children))
```


#### 📄 檔案: `src/textual/widget.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:425, E:442, A:1) ➔ After(N:426, E:443, A:1)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#app** `(Widget)`
    └── ⚡ **on('prune')**
        └── 🎯 [TRIGGERS] `Widget.on_prune()`
            └── 🎯 [CALLS] `_close_messages (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Widget._selection_order` (FUNCTION_DEF)
  • + [新增呼叫邊] `Widget._selection_order` ──[CALLS]──> `find_widget (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #05: `39224a83`
- **完整 Hash**: `39224a837a86e1ec95af31a04f363cac91ca60a3`
- **說明 (Ground Truth)**: auto scroll
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/_auto_scroll.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:5, E:4, A:0)
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
  • + [新增節點] `Region (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `split_horizontal (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `get_auto_scroll_regions` (FUNCTION_DEF)
  • + [新增節點] `grow (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `get_auto_scroll_regions` ──[CALLS]──> `split_horizontal (External/Unresolved)`
  • + [新增呼叫邊] `get_auto_scroll_regions` ──[CALLS]──> `grow (External/Unresolved)`
  • + [新增呼叫邊] `get_auto_scroll_regions` ──[CALLS]──> `intersection (External/Unresolved)`
  • + [新增呼叫邊] `get_auto_scroll_regions` ──[CALLS]──> `Region (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #06: `08663e58`
- **完整 Hash**: `08663e58697aa9cb13650c464f0e74407f415b30`
- **說明 (Ground Truth)**: scroll selectable containers
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/screen.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:214, E:246, A:0) ➔ After(N:220, E:256, A:0)
- **差分統計**: +Nodes: 6, -Nodes: 0, +Edges: 10, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `get_auto_scroll_regions (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Screen._auto_scroll_y` (FUNCTION_DEF)
  • + [新增節點] `log (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Screen._check_auto_scroll` (FUNCTION_DEF)
  • + [新增節點] `Screen._watch__selecting` (FUNCTION_DEF)
  • + [新增節點] `Screen._update_select` (FUNCTION_DEF)
  • + [新增呼叫邊] `Screen._check_auto_scroll` ──[CALLS]──> `get_auto_scroll_regions (External/Unresolved)`
  • + [新增呼叫邊] `Screen._check_auto_scroll` ──[CALLS]──> `stop (External/Unresolved)`
  • + [新增呼叫邊] `Screen._check_auto_scroll` ──[CALLS]──> `set_interval (External/Unresolved)`
  • + [新增呼叫邊] `Screen._check_auto_scroll` ──[CALLS]──> `partial (External/Unresolved)`
  • + [新增呼叫邊] `Screen._auto_scroll_y` ──[CALLS]──> `Screen._update_select`
  • + [新增呼叫邊] `Screen._update_select` ──[CALLS]──> `Screen.get_widget_and_offset_at`
  • + [新增呼叫邊] `Screen._forward_event` ──[CALLS]──> `Screen._check_auto_scroll`
  • + [新增呼叫邊] `Screen._forward_event` ──[CALLS]──> `has_class (External/Unresolved)`
  • + [新增呼叫邊] `Screen._watch__selecting` ──[CALLS]──> `stop (External/Unresolved)`
  • _... 以及其餘 1 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Screen._forward_event()`
- **變更前簽章 (Before)**: `def _forward_event(self, event: events.Event) -> None` (L1683~L1785)
- **變更後簽章 (After)**: `def _forward_event(self, event: events.Event) -> None` (L1745~L1858)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _forward_event(self, event: events.Event) -> None:
        if event.is_forwarded:
            return
        event._set_forwarded()

        if isinstance(event, (events.Enter, events.Leave)):
            self.post_message(event)

        elif isinstance(event, events.MouseMove):
            event.style = self.get_style_at(event.screen_x, event.screen_y)
            self._handle_mouse_move(event)

            if self._selecting:
                self._box_select = event.shift
                select_widget, select_offset = self.get_widget_and_offset_at(
                    event.x, event.y
                )
                if (
                    self._select_end is not None
                    and select_offset is None
                    and event.y > self._select_end[1].y
                ):
                    end_widget = self._select_end[0]
                    select_offset = end_widget.content_region.bottom_right_inclusive
                    self._select_end = (
                        end_widget,
                        event.screen_offset,
                        select_offset,
                    )

                elif (
                    select_widget is not None
                    and select_widget.allow_select
                    and select_offset is not None
                ):
                    self._select_end = (
                        select_widget,
                        event.screen_offset,
                        select_offset,
                    )

        elif isinstance(event, events.MouseEvent):
            if isinstance(event, events.MouseUp):
                if (
                    self._mouse_down_offset is not None
                    and self._mouse_down_offset == event.screen_offset
                ):
                    self.clear_selection()
                self._mouse_down_offset = None
                self._selecting = False
                self.post_message(events.TextSelected())

            elif isinstance(event, events.MouseDown) and not self.app.mouse_captured:
                self._box_select = event.shift
                self._mouse_down_offset = event.screen_offset
                select_widget, select_offset = self.get_widget_and_offset_at(
                    event.screen_x, event.screen_y
                )
                if (
                    select_widget is not None
                    and select_widget.allow_select
                    and self.screen.allow_select
                    and self.app.ALLOW_SELECT
                ):
                    self._selecting = True
                    if select_widget is not None and select_offset is not None:
                        self.text_selection_started_signal.publish(self)
                        self._select_start = (
                            select_widget,
                            event.screen_offset,
                            select_offset,
                        )
                else:
                    self._selecting = False

            try:
                if self.app.mouse_captured:
                    widget = self.app.mouse_captured
                    region = self.find_widget(widget).region
                else:
                    widget, region = self.get_widget_at(event.x, event.y)
            except errors.NoWidget:
                self.set_focus(None)
            else:
                if isinstance(event, events.MouseDown):
                    focusable_widget = self.get_focusable_widget_at(event.x, event.y)
                    if (
                        focusable_widget is not None
                        and focusable_widget.focus_on_click()
                    ):
                        self.set_focus(focusable_widget, scroll_visible=False)
                event.style = self.get_style_at(event.screen_x, event.screen_y)
                if widget.loading:
                    return
                if widget is self:
                    event._set_forwarded()
                    self.post_message(event)
                else:
                    widget._forward_event(event._apply_offset(-region.x, -region.y))

        else:
            self.post_message(event)
        self.update_pointer_shape()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _forward_event(self, event: events.Event) -> None:
        if event.is_forwarded:
            return
        event._set_forwarded()

        if isinstance(event, (events.Enter, events.Leave)):
            self.post_message(event)

        elif isinstance(event, events.MouseMove):
            event.style = self.get_style_at(event.screen_x, event.screen_y)
            self._handle_mouse_move(event)

            if self._selecting:
                self._box_select = event.shift
                select_widget, select_offset = self.get_widget_and_offset_at(
                    event.x, event.y
                )
                if (
                    self._select_end is not None
                    and select_offset is None
                    and event.y > self._select_end[1].y
                ):
                    end_widget = self._select_end[0]
                    select_offset = end_widget.content_region.bottom_right_inclusive
                    self._select_end = (
                        end_widget,
                        event.screen_offset,
                        select_offset,
                    )

                elif (
                    select_widget is not None
                    and select_widget.allow_select
                    and select_offset is not None
                ):
                    self._select_end = (
                        select_widget,
                        event.screen_offset,
                        select_offset,
                    )

                if select_widget is not None:
                    self._check_auto_scroll(select_widget, event.screen_offset)

        elif isinstance(event, events.MouseEvent):
            if isinstance(event, events.MouseUp):
                if (
                    self._mouse_down_offset is not None
                    and self._mouse_down_offset == event.screen_offset
                ):
                    # A click elsewhere should clear the selection
                    select_widget, select_offset = self.get_widget_and_offset_at(
                        event.x, event.y
                    )
                    # Exclude scrollbars, so the user may navigate without clearing the selection
                    if select_widget is None or not select_widget.has_class(
                        "-textual-system"
                    ):
                        self.clear_selection()
                self._mouse_down_offset = None
                self._selecting = False
                self.post_message(events.TextSelected())

            elif isinstance(event, events.MouseDown) and not self.app.mouse_captured:
                self._box_select = event.shift
                self._mouse_down_offset = event.screen_offset
                select_widget, select_offset = self.get_widget_and_offset_at(
                    event.screen_x, event.screen_y
                )
                if (
                    select_widget is not None
                    and select_widget.allow_select
                    and self.screen.allow_select
                    and self.app.ALLOW_SELECT
                ):
                    self._selecting = True
                    if select_widget is not None and select_offset is not None:
                        self.text_selection_started_signal.publish(self)
                        self._select_start = (
                            select_widget,
                            event.screen_offset,
                            select_offset,
                        )
                else:
                    self._selecting = False

            try:
                if self.app.mouse_captured:
                    widget = self.app.mouse_captured
                    region = self.find_widget(widget).region
                else:
                    widget, region = self.get_widget_at(event.x, event.y)
            except errors.NoWidget:
                self.set_focus(None)
            else:
                if isinstance(event, events.MouseDown):
                    focusable_widget = self.get_focusable_widget_at(event.x, event.y)
                    if (
                        focusable_widget is not None
                        and focusable_widget.focus_on_click()
                    ):
                        self.set_focus(focusable_widget, scroll_visible=False)
                event.style = self.get_style_at(event.screen_x, event.screen_y)
                if widget.loading:
                    return
                if widget is self:
                    event._set_forwarded()
                    self.post_message(event)
                else:
                    widget._forward_event(event._apply_offset(-region.x, -region.y))

        else:
            self.post_message(event)
        self.update_pointer_shape()
```

### 🔹 函式: `Screen._watch__select_end()`
- **變更前簽章 (Before)**: `def _watch__select_end( self, select_end: tuple[Widget, Offset, Offset] | None ) -> None` (L1790~L1890)
- **變更後簽章 (After)**: `def _watch__select_end( self, select_end: tuple[Widget, Offset, Offset] | None ) -> None` (L1868~L1971)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _watch__select_end(
        self, select_end: tuple[Widget, Offset, Offset] | None
    ) -> None:
        """When select_end changes, we need to compute which widgets and regions are selected.

        Args:
            select_end: The end selection.
        """
        if select_end is None or self._select_start is None:
            # Nothing to select
            return

        select_start = self._select_start
        start_widget, screen_start, start_offset = select_start
        end_widget, screen_end, end_offset = select_end
        if start_widget is end_widget:
            # Simplest case, selection starts and ends on the same widget
            self.selections = {
                start_widget: Selection.from_offsets(start_offset, end_offset)
            }
            return

        select_start, select_end = sorted(
            [select_start, select_end],
            key=lambda selection: (selection[0].region.offset.transpose),
        )

        start_widget, _screen_start, start_offset = select_start
        end_widget, _screen_end, end_offset = select_end

        select_regions: list[Region] = []
        start_region = start_widget.content_region
        end_region = end_widget.content_region
        if end_region.y <= start_region.bottom or self._box_select:
            select_regions.append(Region.union(start_region, end_region))
        else:
            try:
                container_region = Region.from_union(
                    [
                        start_widget.select_container.content_region,
                        end_widget.select_container.content_region,
                    ]
                )
            except NoMatches:
                return

            start_region = Region.from_corners(
                start_region.x,
                start_region.y,
                container_region.right,
                start_region.bottom,
            )
            end_region = Region.from_corners(
                container_region.x,
                end_region.y,
                end_region.right,
                end_region.bottom,
            )
            select_regions.append(start_region)
            select_regions.append(end_region)
            mid_height = end_region.y - start_region.bottom
            if mid_height > 0:
                mid_region = Region.from_corners(
                    container_region.x,
                    start_region.bottom,
                    container_region.right,
                    start_region.bottom + mid_height,
                )
                select_regions.append(mid_region)

        spatial_map: SpatialMap[Widget] = SpatialMap()
        spatial_map.insert(
            [
                (widget.region, NULL_OFFSET, False, False, widget)
                for widget in self._compositor.visible_widgets.keys()
            ]
        )

        highlighted_widgets: set[Widget] = set()
        for region in select_regions:
            covered_widgets = spatial_map.get_values_in_region(region)
            covered_widgets = [
                widget
                for widget in covered_widgets
                if region.overlaps(widget.content_region)
            ]
            highlighted_widgets.update(covered_widgets)
        highlighted_widgets -= {self, start_widget, end_widget}

        select_all = SELECT_ALL
        self.selections = {
            start_widget: Selection(start_offset, None),
            **{
                widget: select_all
                for widget in sorted(
                    highlighted_widgets,
                    key=lambda widget: widget.content_region.offset.transpose,
                )
            },
            end_widget: Selection(None, end_offset),
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _watch__select_end(
        self, select_end: tuple[Widget, Offset, Offset] | None
    ) -> None:
        """When select_end changes, we need to compute which widgets and regions are selected.

        Args:
            select_end: The end selection.
        """
        if select_end is None or self._select_start is None:
            # Nothing to select
            return

        select_start = self._select_start
        start_widget, screen_start, start_offset = select_start
        end_widget, screen_end, end_offset = select_end
        if start_widget is end_widget:
            # Simplest case, selection starts and ends on the same widget
            self.selections = {
                start_widget: Selection.from_offsets(start_offset, end_offset + (1, 0))
            }
            self.log(self.selections)
            return

        select_start, select_end = sorted(
            [select_start, select_end],
            key=lambda selection: (selection[0].region.offset.transpose),
        )

        start_widget, _screen_start, start_offset = select_start
        end_widget, _screen_end, end_offset = select_end
        end_offset += (1, 0)

        select_regions: list[Region] = []
        start_region = start_widget.content_region
        end_region = end_widget.content_region
        if end_region.y <= start_region.bottom or self._box_select:
            select_regions.append(Region.union(start_region, end_region))
        else:
            try:
                container_region = Region.from_union(
                    [
                        start_widget.select_container.content_region,
                        end_widget.select_container.content_region,
                    ]
                )
            except NoMatches:
                return

            start_region = Region.from_corners(
                start_region.x,
                start_region.y,
                container_region.right,
                start_region.bottom,
            )
            end_region = Region.from_corners(
                container_region.x,
                end_region.y,
                end_region.right,
                end_region.bottom,
            )
            select_regions.append(start_region)
            select_regions.append(end_region)
            mid_height = end_region.y - start_region.bottom
            if mid_height > 0:
                mid_region = Region.from_corners(
                    container_region.x,
                    start_region.bottom,
                    container_region.right,
                    start_region.bottom + mid_height,
                )
                select_regions.append(mid_region)

        spatial_map: SpatialMap[Widget] = SpatialMap()
        spatial_map.insert(
            [
                (widget.region, NULL_OFFSET, False, False, widget)
                for widget in self._compositor.visible_widgets.keys()
            ]
        )

        highlighted_widgets: set[Widget] = set()
        for region in select_regions:
            covered_widgets = spatial_map.get_values_in_region(region)
            covered_widgets = [
                widget
                for widget in covered_widgets
                if region.overlaps(widget.content_region)
            ]
            highlighted_widgets.update(covered_widgets)
        highlighted_widgets -= {self, start_widget, end_widget}

        select_all = SELECT_ALL
        self.selections = {
            start_widget: Selection(start_offset, None),
            **{
                widget: select_all
                for widget in sorted(
                    highlighted_widgets,
                    key=lambda widget: widget.content_region.offset.transpose,
                )
            },
            end_widget: Selection(None, end_offset),
        }
        self.log(self.selections)
```

### 🔹 函式: `Screen.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, name: str | None = None, id: str | None = None, classes: str | None = None, ) -> None` (L274~L329)
- **變更後簽章 (After)**: `def __init__( self, name: str | None = None, id: str | None = None, classes: str | None = None, ) -> None` (L275~L333)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        """
        Initialize the screen.

        Args:
            name: The name of the screen.
            id: The ID of the screen in the DOM.
            classes: The CSS classes for the screen.
        """
        self._modal = False
        super().__init__(name=name, id=id, classes=classes)
        self._compositor = Compositor()
        self._dirty_widgets: set[Widget] = set()
        self.__update_timer: Timer | None = None
        self._callbacks: list[tuple[CallbackType, MessagePump]] = []
        self._result_callbacks: list[ResultCallback[ScreenResultType | None]] = []

        self._tooltip_widget: Widget | None = None
        self._tooltip_timer: Timer | None = None

        css_paths = [
            _make_path_object_relative(css_path, self)
            for css_path in (
                _css_path_type_as_list(self.CSS_PATH)
                if self.CSS_PATH is not None
                else []
            )
        ]
        self.css_path = css_paths

        self.title = self.TITLE
        self.sub_title = self.SUB_TITLE

        self.screen_layout_refresh_signal: Signal[Screen] = Signal(
            self, "layout-refresh"
        )
        """The signal that is published when the screen's layout is refreshed."""

        self.bindings_updated_signal: Signal[Screen] = Signal(self, "bindings_updated")
        """A signal published when the bindings have been updated"""

        self.text_selection_started_signal: Signal[Screen] = Signal(
            self, "selection_started"
        )
        """A signal published when text selection has started."""

        self._css_update_count = -1
        """Track updates to CSS."""

        self._layout_widgets: dict[DOMNode, set[Widget]] = {}
        """Widgets whose layout may have changed."""
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        """
        Initialize the screen.

        Args:
            name: The name of the screen.
            id: The ID of the screen in the DOM.
            classes: The CSS classes for the screen.
        """
        self._modal = False
        super().__init__(name=name, id=id, classes=classes)
        self._compositor = Compositor()
        self._dirty_widgets: set[Widget] = set()
        self.__update_timer: Timer | None = None
        self._callbacks: list[tuple[CallbackType, MessagePump]] = []
        self._result_callbacks: list[ResultCallback[ScreenResultType | None]] = []

        self._tooltip_widget: Widget | None = None
        self._tooltip_timer: Timer | None = None

        css_paths = [
            _make_path_object_relative(css_path, self)
            for css_path in (
                _css_path_type_as_list(self.CSS_PATH)
                if self.CSS_PATH is not None
                else []
            )
        ]
        self.css_path = css_paths

        self.title = self.TITLE
        self.sub_title = self.SUB_TITLE

        self.screen_layout_refresh_signal: Signal[Screen] = Signal(
            self, "layout-refresh"
        )
        """The signal that is published when the screen's layout is refreshed."""

        self.bindings_updated_signal: Signal[Screen] = Signal(self, "bindings_updated")
        """A signal published when the bindings have been updated"""

        self.text_selection_started_signal: Signal[Screen] = Signal(
            self, "selection_started"
        )
        """A signal published when text selection has started."""

        self._css_update_count = -1
        """Track updates to CSS."""

        self._layout_widgets: dict[DOMNode, set[Widget]] = {}
        """Widgets whose layout may have changed."""

        self._auto_select_scroll_timer: Timer | None = None
        """A timer to auto scroll a container."""
```


---

### 🔹 Commit #07: `1e90c2fd`
- **完整 Hash**: `1e90c2fd73adb69cf07ec985f32374113eaedafc`
- **說明 (Ground Truth)**: restore virtual size layout
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/widget.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:417, E:435, A:1) ➔ After(N:416, E:434, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 0, -Edges: 1, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#app** `(Widget)`
    └── ⚡ **on('prune')**
        └── 🎯 [TRIGGERS] `Widget.on_prune()`
            └── 🎯 [CALLS] `_close_messages (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `Widget.watch_virtual_size` (FUNCTION_DEF)
  • - [移除呼叫邊] `Widget.watch_virtual_size` ──[CALLS]──> `Widget.refresh`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #08: `959796bb`
- **完整 Hash**: `959796bba49f914881574c6c62fdcb0d23f9ec58`
- **說明 (Ground Truth)**: node refresh
- **變更檔案數**: 3

#### 📄 檔案: `src/textual/app.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:500, E:604, A:2) ➔ After(N:500, E:606, A:2)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#app** `(Widget)`
    └── ⚡ **on('ready')**
        └── 🎯 [TRIGGERS] `App.on_app_ready()`
            └── 🎯 [CALLS] `set (External/Unresolved)()`
    └── ⚡ **on('event')**
        └── 🎯 [TRIGGERS] `App.on_event()`
            └── 🎯 [CALLS] `App._check_bindings()`
                └── 🎯 [CALLS] `App.run_action()`
                    └── 🎯 [CALLS] `App._dispatch_action()`
                        └── 🎯 [CALLS] `callable (External/Unresolved)()`
                        └── 🎯 [CALLS] `getattr (External/Unresolved)()`
                        └── 🎯 [CALLS] `invoke (External/Unresolved)()`
                        └── 🎯 [CALLS] `system (External/Unresolved)()`
                    └── 🎯 [CALLS] `App._parse_action()`
                        └── *ref:`getattr (External/Unresolved)` [已折疊指針]
                        └── 🎯 [CALLS] `parse (External/Unresolved)()`
                    └── 🎯 [CALLS] `check_action (External/Unresolved)()`
                └── 🎯 [CALLS] `reversed (External/Unresolved)()`
            └── 🎯 [CALLS] `App._init_mode()`
                └── 🎯 [CALLS] `App._get_screen()`
                    └── 🎯 [CALLS] `App._register()`
                        └── *ref:`App._register` [已折疊指針]
                        └── 🎯 [CALLS] `App._register_child()`
                            └── 🎯 [CALLS] `_append (External/Unresolved)()`
                            └── 🎯 [CALLS] `_attach (External/Unresolved)()`
                            └── 🎯 [CALLS] `_insert (External/Unresolved)()`
                            └── 🎯 [CALLS] `_post_register (External/Unresolved)()`
                            └── 🎯 [CALLS] `add (External/Unresolved)()`
                        └── 🎯 [CALLS] `_start_messages (External/Unresolved)()`
                        └── 🎯 [CALLS] `add_new_widget (External/Unresolved)()`
                        └── 🎯 [CALLS] `apply_stylesheet (External/Unresolved)()`
                        └── 🎯 [CALLS] `list (External/Unresolved)()`
                        └── *ref:`reversed (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `App.get_screen()`
                        └── 🎯 [CALLS] `KeyError (External/Unresolved)()`
                        └── 🎯 [CALLS] `TypeError (External/Unresolved)()`
                        └── *ref:`callable (External/Unresolved)` [已折疊指針]
                        └── 🎯 [CALLS] `next_screen (External/Unresolved)()`
                        └── 🎯 [CALLS] `type (External/Unresolved)()`
                    └── 🎯 [CALLS] `AwaitMount (External/Unresolved)()`
                    └── 🎯 [CALLS] `call_next (External/Unresolved)()`
                └── 🎯 [CALLS] `App._load_screen_css()`
                    └── 🎯 [CALLS] `add_paths (External/Unresolved)()`
                    └── 🎯 [CALLS] `add_source (External/Unresolved)()`
                    └── 🎯 [CALLS] `getfile (External/Unresolved)()`
                    └── 🎯 [CALLS] `has_source (External/Unresolved)()`
                    └── 🎯 [CALLS] `reparse (External/Unresolved)()`
                    └── 🎯 [CALLS] `update (External/Unresolved)()`
                └── *ref:`App._register` [已折疊指針]
                └── 🎯 [CALLS] `App.get_default_screen()`
                    └── 🎯 [CALLS] `Screen (External/Unresolved)()`
                └── 🎯 [CALLS] `App.refresh_css()`
                    └── 🎯 [CALLS] `App.get_css_variables()`
                        └── 🎯 [CALLS] `App.get_theme_variable_defaults()`
                        └── 🎯 [CALLS] `generate (External/Unresolved)()`
                        └── 🎯 [CALLS] `to_color_system (External/Unresolved)()`
                    └── 🎯 [CALLS] `_refresh_layout (External/Unresolved)()`
                    └── *ref:`reparse (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `set_variables (External/Unresolved)()`
                    └── *ref:`update (External/Unresolved)` [已折疊指針]
                └── *ref:`AwaitMount (External/Unresolved)` [已折疊指針]
                └── 🎯 [CALLS] `ScreenResume (External/Unresolved)()`
                └── *ref:`TypeError (External/Unresolved)` [已折疊指針]
                └── 🎯 [CALLS] `_screen (External/Unresolved)()`
                └── 🎯 [CALLS] `_screen_resized (External/Unresolved)()`
                └── *ref:`callable (External/Unresolved)` [已折疊指針]
                └── 🎯 [CALLS] `post_message (External/Unresolved)()`
                └── *ref:`type (External/Unresolved)` [已折疊指針]
            └── 🎯 [CALLS] `App.get_widget_at()`
                └── *ref:`App.get_widget_at` [已折疊指針]
            └── *ref:`App.on_event` [已折疊指針]
            └── 🎯 [CALLS] `Offset (External/Unresolved)()`
            └── 🎯 [CALLS] `_clear_tooltip (External/Unresolved)()`
            └── 🎯 [CALLS] `_forward_event (External/Unresolved)()`
            └── 🎯 [CALLS] `from_event (External/Unresolved)()`
            └── 🎯 [CALLS] `minimize (External/Unresolved)()`
            └── 🎯 [CALLS] `super (External/Unresolved)()`
    └── 🎯 [CALLS] `TypeVar (External/Unresolved)()`
  🌲 **#self** `(Control)`
    └── ⚡ **devtools.connect**
        └── 🎯 [TRIGGERS] `) (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `App.update_styles` ──[CALLS]──> `reversed (External/Unresolved)`
  • + [新增呼叫邊] `App.update_styles` ──[CALLS]──> `update_node_styles (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `App.update_styles()`
- **變更前簽章 (Before)**: `def update_styles(self, node: DOMNode) -> None` (L2405~L2414)
- **變更後簽章 (After)**: `def update_styles(self, node: DOMNode, animate: bool = True) -> None` (L2405~L2420)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def update_styles(self, node: DOMNode) -> None:
        """Immediately update the styles of this node and all descendant nodes.

        Should be called whenever CSS classes / pseudo classes change.
        For example, when you hover over a button, the :hover pseudo class
        will be added, and this method is called to apply the corresponding
        :hover styles.
        """
        descendants = node.walk_children(with_self=True)
        self.stylesheet.update_nodes(descendants, animate=True)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def update_styles(self, node: DOMNode, animate: bool = True) -> None:
        """Immediately update the styles of this node and all descendant nodes.

        Should be called whenever CSS classes / pseudo classes change.
        For example, when you hover over a button, the :hover pseudo class
        will be added, and this method is called to apply the corresponding
        :hover styles.
        """
        if isinstance(node, App):
            for screen in reversed(self.screen_stack):
                screen.update_node_styles(animate=animate)
                if not (screen.is_modal and screen.styles.background.a < 1):
                    break
        else:
            descendants = node.walk_children(with_self=True)
            self.stylesheet.update_nodes(descendants, animate=animate)
```


#### 📄 檔案: `src/textual/dom.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:203, E:204, A:0) ➔ After(N:203, E:204, A:0)
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

### 🔹 函式: `DOMNode.update_node_styles()`
- **變更前簽章 (Before)**: `def update_node_styles(self) -> None` (L1736~L1744)
- **變更後簽章 (After)**: `def update_node_styles(self, animate: bool = True) -> None` (L1736~L1744)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def update_node_styles(self) -> None:
        """Request an update of this node's styles.

        Called by Textual whenever CSS classes / pseudo classes change.
        """
        try:
            self.app.update_styles(self)
        except NoActiveAppError:
            pass
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def update_node_styles(self, animate: bool = True) -> None:
        """Request an update of this node's styles.

        Called by Textual whenever CSS classes / pseudo classes change.
        """
        try:
            self.app.update_styles(self, animate=animate)
        except NoActiveAppError:
            pass
```


#### 📄 檔案: `src/textual/screen.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:212, E:245, A:0) ➔ After(N:213, E:245, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `update_node_styles (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Screen._on_screen_resume` ──[CALLS]──> `update_node_styles (External/Unresolved)`
  • - [移除呼叫邊] `Screen._on_screen_resume` ──[CALLS]──> `update (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Screen._on_screen_resume()`
- **變更前簽章 (Before)**: `def _on_screen_resume(self) -> None` (L1430~L1447)
- **變更後簽章 (After)**: `def _on_screen_resume(self) -> None` (L1430~L1446)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _on_screen_resume(self) -> None:
        """Screen has resumed."""
        if self.app.SUSPENDED_SCREEN_CLASS:
            self.remove_class(self.app.SUSPENDED_SCREEN_CLASS)

        self.stack_updates += 1

        self.app._refresh_notifications()
        size = self.app.size

        self._update_auto_focus()

        if self.is_attached:
            self._compositor_refresh()
            if self.stack_updates == 1:
                self.app.stylesheet.update(self)
            self._refresh_layout(size)
            self.refresh()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _on_screen_resume(self) -> None:
        """Screen has resumed."""
        if self.app.SUSPENDED_SCREEN_CLASS:
            self.remove_class(self.app.SUSPENDED_SCREEN_CLASS)

        self.stack_updates += 1

        self.app._refresh_notifications()
        size = self.app.size

        self._update_auto_focus()

        if self.is_attached:
            self._compositor_refresh()
            self.update_node_styles(animate=False)
            self._refresh_layout(size)
            self.refresh()
```


---

### 🔹 Commit #09: `f26eec89`
- **完整 Hash**: `f26eec8912fc47f85230ea83977667f5fe5be7cb`
- **說明 (Ground Truth)**: key test
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/_xterm_parser.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:48, E:61, A:2) ➔ After(N:48, E:61, A:2)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#app** `(Widget)`
    └── ⚡ **on('token')**
        └── 🎯 [TRIGGERS] `XTermParser.on_token()`
            └── 🎯 [CALLS] `XTermParser.debug_log()`
                └── 🎯 [CALLS] `flush (External/Unresolved)()`
            └── 🎯 [CALLS] `token_callback (External/Unresolved)()`
  🌲 **#key** `(Widget)`
    └── ⚡ **on('token')**
        └── 🎯 [TRIGGERS] `XTermParser.on_key_token()`
            └── 🎯 [CALLS] `XTermParser.on_token()`
                └── 🎯 [CALLS] `XTermParser.debug_log()`
                    └── 🎯 [CALLS] `flush (External/Unresolved)()`
                └── 🎯 [CALLS] `token_callback (External/Unresolved)()`
            └── *ref:`XTermParser.debug_log` [已折疊指針]

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #10: `ea8d69bf`
- **完整 Hash**: `ea8d69bf7e4355be3e36d0fef9ee5361c67ccbbf`
- **說明 (Ground Truth)**: fix textarea scrollbar refresh
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/widgets/_text_area.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:255, E:296, A:0) ➔ After(N:256, E:297, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `_refresh_scrollbars (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `TextArea._refresh_size` ──[CALLS]──> `_refresh_scrollbars (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TextArea.edit()`
- **變更前簽章 (Before)**: `def edit(self, edit: Edit) -> EditResult` (L1536~L1569)
- **變更後簽章 (After)**: `def edit(self, edit: Edit) -> EditResult` (L1537~L1570)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def edit(self, edit: Edit) -> EditResult:
        """Perform an Edit.

        Args:
            edit: The Edit to perform.

        Returns:
            Data relating to the edit that may be useful. The data returned
            may be different depending on the edit performed.
        """
        if self.suggestion.startswith(edit.text):
            self.suggestion = self.suggestion[len(edit.text) :]
        else:
            self.suggestion = ""
        old_gutter_width = self.gutter_width
        result = edit.do(self)
        self.history.record(edit)
        new_gutter_width = self.gutter_width

        if old_gutter_width != new_gutter_width:
            self.wrapped_document.wrap(self.wrap_width, self.indent_width)
        else:
            self.wrapped_document.wrap_range(
                edit.top,
                edit.bottom,
                result.end_location,
            )

        self._refresh_size()
        edit.after(self)
        self._build_highlight_map()
        self.post_message(self.Changed(self))
        self.update_suggestion()
        return result
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def edit(self, edit: Edit) -> EditResult:
        """Perform an Edit.

        Args:
            edit: The Edit to perform.

        Returns:
            Data relating to the edit that may be useful. The data returned
            may be different depending on the edit performed.
        """
        if self.suggestion.startswith(edit.text):
            self.suggestion = self.suggestion[len(edit.text) :]
        else:
            self.suggestion = ""
        old_gutter_width = self.gutter_width
        result = edit.do(self)
        self.history.record(edit)
        new_gutter_width = self.gutter_width

        if old_gutter_width != new_gutter_width:
            self.wrapped_document.wrap(self.wrap_width, self.indent_width)
        else:
            self.wrapped_document.wrap_range(
                edit.top,
                edit.bottom,
                result.end_location,
            )

        edit.after(self)
        self._build_highlight_map()
        self.post_message(self.Changed(self))
        self.update_suggestion()
        self._refresh_size()
        return result
```

### 🔹 函式: `TextArea._refresh_size()`
- **變更前簽章 (Before)**: `def _refresh_size(self) -> None` (L1153~L1160)
- **變更後簽章 (After)**: `def _refresh_size(self) -> None` (L1153~L1161)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _refresh_size(self) -> None:
        """Update the virtual size of the TextArea."""
        if self.soft_wrap:
            self.virtual_size = Size(0, self.wrapped_document.height)
        else:
            # +1 width to make space for the cursor resting at the end of the line
            width, height = self.document.get_size(self.indent_width)
            self.virtual_size = Size(width + self.gutter_width + 1, height)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _refresh_size(self) -> None:
        """Update the virtual size of the TextArea."""
        if self.soft_wrap:
            self.virtual_size = Size(0, self.wrapped_document.height)
        else:
            # +1 width to make space for the cursor resting at the end of the line
            width, height = self.document.get_size(self.indent_width)
            self.virtual_size = Size(width + self.gutter_width + 1, height)
        self._refresh_scrollbars()
```


---

### 🔹 Commit #11: `fec3466d`
- **完整 Hash**: `fec3466dc83d69c2c2969129d2d2cfe6da9371cd`
- **說明 (Ground Truth)**: Focus on click and moount_compose
- **變更檔案數**: 3

#### 📄 檔案: `src/textual/app.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:500, E:604, A:2) ➔ After(N:500, E:604, A:2)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#app** `(Widget)`
    └── ⚡ **on('ready')**
        └── 🎯 [TRIGGERS] `App.on_app_ready()`
            └── 🎯 [CALLS] `set (External/Unresolved)()`
    └── ⚡ **on('event')**
        └── 🎯 [TRIGGERS] `App.on_event()`
            └── 🎯 [CALLS] `App._check_bindings()`
                └── 🎯 [CALLS] `App.run_action()`
                    └── 🎯 [CALLS] `App._dispatch_action()`
                        └── 🎯 [CALLS] `callable (External/Unresolved)()`
                        └── 🎯 [CALLS] `getattr (External/Unresolved)()`
                        └── 🎯 [CALLS] `invoke (External/Unresolved)()`
                        └── 🎯 [CALLS] `system (External/Unresolved)()`
                    └── 🎯 [CALLS] `App._parse_action()`
                        └── *ref:`getattr (External/Unresolved)` [已折疊指針]
                        └── 🎯 [CALLS] `parse (External/Unresolved)()`
                    └── 🎯 [CALLS] `check_action (External/Unresolved)()`
                └── 🎯 [CALLS] `reversed (External/Unresolved)()`
            └── 🎯 [CALLS] `App._init_mode()`
                └── 🎯 [CALLS] `App._get_screen()`
                    └── 🎯 [CALLS] `App._register()`
                        └── *ref:`App._register` [已折疊指針]
                        └── 🎯 [CALLS] `App._register_child()`
                            └── 🎯 [CALLS] `_append (External/Unresolved)()`
                            └── 🎯 [CALLS] `_attach (External/Unresolved)()`
                            └── 🎯 [CALLS] `_insert (External/Unresolved)()`
                            └── 🎯 [CALLS] `_post_register (External/Unresolved)()`
                            └── 🎯 [CALLS] `add (External/Unresolved)()`
                        └── 🎯 [CALLS] `_start_messages (External/Unresolved)()`
                        └── 🎯 [CALLS] `add_new_widget (External/Unresolved)()`
                        └── 🎯 [CALLS] `apply_stylesheet (External/Unresolved)()`
                        └── 🎯 [CALLS] `list (External/Unresolved)()`
                        └── *ref:`reversed (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `App.get_screen()`
                        └── 🎯 [CALLS] `KeyError (External/Unresolved)()`
                        └── 🎯 [CALLS] `TypeError (External/Unresolved)()`
                        └── *ref:`callable (External/Unresolved)` [已折疊指針]
                        └── 🎯 [CALLS] `next_screen (External/Unresolved)()`
                        └── 🎯 [CALLS] `type (External/Unresolved)()`
                    └── 🎯 [CALLS] `AwaitMount (External/Unresolved)()`
                    └── 🎯 [CALLS] `call_next (External/Unresolved)()`
                └── 🎯 [CALLS] `App._load_screen_css()`
                    └── 🎯 [CALLS] `add_paths (External/Unresolved)()`
                    └── 🎯 [CALLS] `add_source (External/Unresolved)()`
                    └── 🎯 [CALLS] `getfile (External/Unresolved)()`
                    └── 🎯 [CALLS] `has_source (External/Unresolved)()`
                    └── 🎯 [CALLS] `reparse (External/Unresolved)()`
                    └── 🎯 [CALLS] `update (External/Unresolved)()`
                └── *ref:`App._register` [已折疊指針]
                └── 🎯 [CALLS] `App.get_default_screen()`
                    └── 🎯 [CALLS] `Screen (External/Unresolved)()`
                └── 🎯 [CALLS] `App.refresh_css()`
                    └── 🎯 [CALLS] `App.get_css_variables()`
                        └── 🎯 [CALLS] `App.get_theme_variable_defaults()`
                        └── 🎯 [CALLS] `generate (External/Unresolved)()`
                        └── 🎯 [CALLS] `to_color_system (External/Unresolved)()`
                    └── 🎯 [CALLS] `_refresh_layout (External/Unresolved)()`
                    └── *ref:`reparse (External/Unresolved)` [已折疊指針]
                    └── 🎯 [CALLS] `set_variables (External/Unresolved)()`
                    └── *ref:`update (External/Unresolved)` [已折疊指針]
                └── *ref:`AwaitMount (External/Unresolved)` [已折疊指針]
                └── 🎯 [CALLS] `ScreenResume (External/Unresolved)()`
                └── *ref:`TypeError (External/Unresolved)` [已折疊指針]
                └── 🎯 [CALLS] `_screen (External/Unresolved)()`
                └── 🎯 [CALLS] `_screen_resized (External/Unresolved)()`
                └── *ref:`callable (External/Unresolved)` [已折疊指針]
                └── 🎯 [CALLS] `post_message (External/Unresolved)()`
                └── *ref:`type (External/Unresolved)` [已折疊指針]
            └── 🎯 [CALLS] `App.get_widget_at()`
                └── *ref:`App.get_widget_at` [已折疊指針]
            └── *ref:`App.on_event` [已折疊指針]
            └── 🎯 [CALLS] `Offset (External/Unresolved)()`
            └── 🎯 [CALLS] `_clear_tooltip (External/Unresolved)()`
            └── 🎯 [CALLS] `_forward_event (External/Unresolved)()`
            └── 🎯 [CALLS] `from_event (External/Unresolved)()`
            └── 🎯 [CALLS] `minimize (External/Unresolved)()`
            └── 🎯 [CALLS] `super (External/Unresolved)()`
    └── 🎯 [CALLS] `TypeVar (External/Unresolved)()`
  🌲 **#self** `(Control)`
    └── ⚡ **devtools.connect**
        └── 🎯 [TRIGGERS] `) (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `src/textual/screen.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:209, E:242, A:0) ➔ After(N:210, E:243, A:0)
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
  • + [新增節點] `focus_on_click (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Screen._forward_event` ──[CALLS]──> `focus_on_click (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Screen._forward_event()`
- **變更前簽章 (Before)**: `def _forward_event(self, event: events.Event) -> None` (L1640~L1737)
- **變更後簽章 (After)**: `def _forward_event(self, event: events.Event) -> None` (L1640~L1737)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _forward_event(self, event: events.Event) -> None:
        if event.is_forwarded:
            return
        event._set_forwarded()

        if isinstance(event, (events.Enter, events.Leave)):
            self.post_message(event)

        elif isinstance(event, events.MouseMove):
            event.style = self.get_style_at(event.screen_x, event.screen_y)
            self._handle_mouse_move(event)

            if self._selecting:
                self._box_select = event.shift
                select_widget, select_offset = self.get_widget_and_offset_at(
                    event.x, event.y
                )
                if (
                    self._select_end is not None
                    and select_offset is None
                    and event.y > self._select_end[1].y
                ):
                    end_widget = self._select_end[0]
                    select_offset = end_widget.content_region.bottom_right_inclusive
                    self._select_end = (
                        end_widget,
                        event.screen_offset,
                        select_offset,
                    )

                elif (
                    select_widget is not None
                    and select_widget.allow_select
                    and select_offset is not None
                ):
                    self._select_end = (
                        select_widget,
                        event.screen_offset,
                        select_offset,
                    )

        elif isinstance(event, events.MouseEvent):
            if isinstance(event, events.MouseUp):
                if (
                    self._mouse_down_offset is not None
                    and self._mouse_down_offset == event.screen_offset
                ):
                    self.clear_selection()
                self._mouse_down_offset = None
                self._selecting = False

            elif isinstance(event, events.MouseDown) and not self.app.mouse_captured:
                self._box_select = event.shift
                self._mouse_down_offset = event.screen_offset
                select_widget, select_offset = self.get_widget_and_offset_at(
                    event.screen_x, event.screen_y
                )
                if (
                    select_widget is not None
                    and select_widget.allow_select
                    and self.screen.allow_select
                    and self.app.ALLOW_SELECT
                ):
                    self._selecting = True
                    if select_widget is not None and select_offset is not None:
                        self.text_selection_started_signal.publish(self)
                        self._select_start = (
                            select_widget,
                            event.screen_offset,
                            select_offset,
                        )
                else:
                    self._selecting = False

            try:
                if self.app.mouse_captured:
                    widget = self.app.mouse_captured
                    region = self.find_widget(widget).region
                else:
                    widget, region = self.get_widget_at(event.x, event.y)
            except errors.NoWidget:
                self.set_focus(None)
            else:
                if isinstance(event, events.MouseDown):
                    focusable_widget = self.get_focusable_widget_at(event.x, event.y)
                    if focusable_widget:
                        self.set_focus(focusable_widget, scroll_visible=False)
                event.style = self.get_style_at(event.screen_x, event.screen_y)
                if widget.loading:
                    return
                if widget is self:
                    event._set_forwarded()
                    self.post_message(event)
                else:
                    widget._forward_event(event._apply_offset(-region.x, -region.y))

        else:
            self.post_message(event)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _forward_event(self, event: events.Event) -> None:
        if event.is_forwarded:
            return
        event._set_forwarded()

        if isinstance(event, (events.Enter, events.Leave)):
            self.post_message(event)

        elif isinstance(event, events.MouseMove):
            event.style = self.get_style_at(event.screen_x, event.screen_y)
            self._handle_mouse_move(event)

            if self._selecting:
                self._box_select = event.shift
                select_widget, select_offset = self.get_widget_and_offset_at(
                    event.x, event.y
                )
                if (
                    self._select_end is not None
                    and select_offset is None
                    and event.y > self._select_end[1].y
                ):
                    end_widget = self._select_end[0]
                    select_offset = end_widget.content_region.bottom_right_inclusive
                    self._select_end = (
                        end_widget,
                        event.screen_offset,
                        select_offset,
                    )

                elif (
                    select_widget is not None
                    and select_widget.allow_select
                    and select_offset is not None
                ):
                    self._select_end = (
                        select_widget,
                        event.screen_offset,
                        select_offset,
                    )

        elif isinstance(event, events.MouseEvent):
            if isinstance(event, events.MouseUp):
                if (
                    self._mouse_down_offset is not None
                    and self._mouse_down_offset == event.screen_offset
                ):
                    self.clear_selection()
                self._mouse_down_offset = None
                self._selecting = False

            elif isinstance(event, events.MouseDown) and not self.app.mouse_captured:
                self._box_select = event.shift
                self._mouse_down_offset = event.screen_offset
                select_widget, select_offset = self.get_widget_and_offset_at(
                    event.screen_x, event.screen_y
                )
                if (
                    select_widget is not None
                    and select_widget.allow_select
                    and self.screen.allow_select
                    and self.app.ALLOW_SELECT
                ):
                    self._selecting = True
                    if select_widget is not None and select_offset is not None:
                        self.text_selection_started_signal.publish(self)
                        self._select_start = (
                            select_widget,
                            event.screen_offset,
                            select_offset,
                        )
                else:
                    self._selecting = False

            try:
                if self.app.mouse_captured:
                    widget = self.app.mouse_captured
                    region = self.find_widget(widget).region
                else:
                    widget, region = self.get_widget_at(event.x, event.y)
            except errors.NoWidget:
                self.set_focus(None)
            else:
                if isinstance(event, events.MouseDown):
                    focusable_widget = self.get_focusable_widget_at(event.x, event.y)
                    if focusable_widget and focusable_widget.focus_on_click():
                        self.set_focus(focusable_widget, scroll_visible=False)
                event.style = self.get_style_at(event.screen_x, event.screen_y)
                if widget.loading:
                    return
                if widget is self:
                    event._set_forwarded()
                    self.post_message(event)
                else:
                    widget._forward_event(event._apply_offset(-region.x, -region.y))

        else:
            self.post_message(event)
```


#### 📄 檔案: `src/textual/widget.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:414, E:431, A:1) ➔ After(N:416, E:433, A:1)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#app** `(Widget)`
    └── ⚡ **on('prune')**
        └── 🎯 [TRIGGERS] `Widget.on_prune()`
            └── 🎯 [CALLS] `_close_messages (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Widget.focus_on_click` (FUNCTION_DEF)
  • + [新增節點] `Widget.mount_compose` (FUNCTION_DEF)
  • + [新增呼叫邊] `Widget.mount_compose` ──[CALLS]──> `Widget.mount_all`
  • + [新增呼叫邊] `Widget.mount_compose` ──[CALLS]──> `Widget.compose`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #12: `a7a9c1e1`
- **完整 Hash**: `a7a9c1e1a52b279d07e3439aff684ad9bc7a3964`
- **說明 (Ground Truth)**: add refresh
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/widget.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:415, E:432, A:1) ➔ After(N:415, E:433, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#app** `(Widget)`
    └── ⚡ **on('prune')**
        └── 🎯 [TRIGGERS] `Widget.on_prune()`
            └── 🎯 [CALLS] `_close_messages (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `Widget.focus` ──[CALLS]──> `Widget.refresh`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Widget.focus()`
- **變更前簽章 (Before)**: `def focus(self, scroll_visible: bool = True) -> Self` (L4446~L4464)
- **變更後簽章 (After)**: `def focus(self, scroll_visible: bool = True) -> Self` (L4446~L4465)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def focus(self, scroll_visible: bool = True) -> Self:
        """Give focus to this widget.

        Args:
            scroll_visible: Scroll parent to make this widget visible.

        Returns:
            The `Widget` instance.
        """

        def set_focus(widget: Widget) -> None:
            """Callback to set the focus."""
            try:
                widget.screen.set_focus(self, scroll_visible=scroll_visible)
            except NoScreen:
                pass

        self.app.call_later(set_focus, self)
        return self
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def focus(self, scroll_visible: bool = True) -> Self:
        """Give focus to this widget.

        Args:
            scroll_visible: Scroll parent to make this widget visible.

        Returns:
            The `Widget` instance.
        """

        def set_focus(widget: Widget) -> None:
            """Callback to set the focus."""
            try:
                widget.screen.set_focus(self, scroll_visible=scroll_visible)
            except NoScreen:
                pass

        self.refresh()
        self.app.call_later(set_focus, self)
        return self
```


---

### 🔹 Commit #13: `20a2db93`
- **完整 Hash**: `20a2db934c3239b6ae082b7d4ff7997259019166`
- **說明 (Ground Truth)**: trap focus
- **變更檔案數**: 2

#### 📄 檔案: `src/textual/dom.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:202, E:204, A:0) ➔ After(N:203, E:204, A:0)
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
  • + [新增節點] `DOMNode.trap_focus` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `DOMNode.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, *, name: str | None = None, id: str | None = None, classes: str | None = None, ) -> None` (L185~L232)
- **變更後簽章 (After)**: `def __init__( self, *, name: str | None = None, id: str | None = None, classes: str | None = None, ) -> None` (L185~L233)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        self._classes: set[str] = set()
        self._name = name
        self._id = None
        if id is not None:
            check_identifiers("id", id)
            self._id = id

        _classes = classes.split() if classes else []
        check_identifiers("class name", *_classes)
        self._classes.update(_classes)

        self._nodes: NodeList = NodeList(self)
        self._css_styles: Styles = Styles(self)
        self._inline_styles: Styles = Styles(self)
        self.styles: RenderStyles = RenderStyles(
            self, self._css_styles, self._inline_styles
        )
        # A mapping of class names to Styles set in COMPONENT_CLASSES
        self._component_styles: dict[str, RenderStyles] = {}

        self._auto_refresh: float | None = None
        self._auto_refresh_timer: Timer | None = None
        self._css_types = {cls.__name__ for cls in self._css_bases(self.__class__)}
        self._bindings = (
            BindingsMap()
            if self._merged_bindings is None
            else self._merged_bindings.copy()
        )
        self._has_hover_style: bool = False
        self._has_focus_within: bool = False
        self._has_order_style: bool = False
        """The node has an ordered dependent pseudo-style (`:odd`, `:even`, `:first-of-type`, `:last-of-type`, `:first-child`, `:last-child`)"""
        self._has_odd_or_even: bool = False
        """The node has the pseudo class `odd` or `even`."""
        self._reactive_connect: (
            dict[str, tuple[MessagePump, Reactive[object] | object]] | None
        ) = None
        self._pruning = False
        self._query_one_cache: LRUCache[QueryOneCacheKey, DOMNode] = LRUCache(1024)

        super().__init__()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        self._classes: set[str] = set()
        self._name = name
        self._id = None
        if id is not None:
            check_identifiers("id", id)
            self._id = id

        _classes = classes.split() if classes else []
        check_identifiers("class name", *_classes)
        self._classes.update(_classes)

        self._nodes: NodeList = NodeList(self)
        self._css_styles: Styles = Styles(self)
        self._inline_styles: Styles = Styles(self)
        self.styles: RenderStyles = RenderStyles(
            self, self._css_styles, self._inline_styles
        )
        # A mapping of class names to Styles set in COMPONENT_CLASSES
        self._component_styles: dict[str, RenderStyles] = {}

        self._auto_refresh: float | None = None
        self._auto_refresh_timer: Timer | None = None
        self._css_types = {cls.__name__ for cls in self._css_bases(self.__class__)}
        self._bindings = (
            BindingsMap()
            if self._merged_bindings is None
            else self._merged_bindings.copy()
        )
        self._has_hover_style: bool = False
        self._has_focus_within: bool = False
        self._has_order_style: bool = False
        """The node has an ordered dependent pseudo-style (`:odd`, `:even`, `:first-of-type`, `:last-of-type`, `:first-child`, `:last-child`)"""
        self._has_odd_or_even: bool = False
        """The node has the pseudo class `odd` or `even`."""
        self._reactive_connect: (
            dict[str, tuple[MessagePump, Reactive[object] | object]] | None
        ) = None
        self._pruning = False
        self._query_one_cache: LRUCache[QueryOneCacheKey, DOMNode] = LRUCache(1024)
        self._trap_focus = False

        super().__init__()
```


#### 📄 檔案: `src/textual/screen.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:209, E:242, A:0) ➔ After(N:209, E:242, A:0)
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

### 🔹 函式: `Screen.focus_chain()`
- **變更前簽章 (Before)**: `def focus_chain(self) -> list[Widget]` (L734~L779)
- **變更後簽章 (After)**: `def focus_chain(self) -> list[Widget]` (L734~L788)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def focus_chain(self) -> list[Widget]:
        """A list of widgets that may receive focus, in focus order."""
        # TODO: Calculating a focus chain is moderately expensive.
        # Suspect we can move focus without calculating the entire thing again.

        widgets: list[Widget] = []
        add_widget = widgets.append
        focus_sorter = attrgetter("_focus_sort_key")
        # We traverse the DOM and keep track of where we are at with a node stack.
        # Additionally, we manually keep track of the visibility of the DOM
        # instead of relying on the property `.visible` to save on DOM traversals.
        # node_stack: list[tuple[iterator over node children, node visibility]]
        node_stack: list[tuple[Iterator[Widget], bool]] = [
            (
                iter(sorted(self.displayed_children, key=focus_sorter)),
                self.visible,
            )
        ]
        pop = node_stack.pop
        push = node_stack.append

        while node_stack:
            children_iterator, parent_visibility = node_stack[-1]
            node = next(children_iterator, None)
            if node is None:
                pop()
            else:
                if node._check_disabled():
                    continue
                node_styles_visibility = node.styles.get_rule("visibility")
                node_is_visible = (
                    node_styles_visibility != "hidden"
                    if node_styles_visibility
                    else parent_visibility  # Inherit visibility if the style is unset.
                )
                if node.is_container and node.allow_focus_children():
                    sorted_displayed_children = sorted(
                        node.displayed_children, key=focus_sorter
                    )
                    push((iter(sorted_displayed_children), node_is_visible))
                # Same check as `if node.focusable`, but we cached inherited visibility
                # and we also skipped disabled nodes altogether.
                if node_is_visible and node.allow_focus():
                    add_widget(node)

        return widgets
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def focus_chain(self) -> list[Widget]:
        """A list of widgets that may receive focus, in focus order."""
        # TODO: Calculating a focus chain is moderately expensive.
        # Suspect we can move focus without calculating the entire thing again.

        widgets: list[Widget] = []
        add_widget = widgets.append
        focus_sorter = attrgetter("_focus_sort_key")
        # We traverse the DOM and keep track of where we are at with a node stack.
        # Additionally, we manually keep track of the visibility of the DOM
        # instead of relying on the property `.visible` to save on DOM traversals.
        # node_stack: list[tuple[iterator over node children, node visibility]]

        root_node = self.screen

        if (focused := self.focused) is not None:
            for node in focused.ancestors_with_self:
                if node._trap_focus:
                    root_node = node
                    break

        node_stack: list[tuple[Iterator[Widget], bool]] = [
            (
                iter(sorted(root_node.displayed_children, key=focus_sorter)),
                self.visible,
            )
        ]
        pop = node_stack.pop
        push = node_stack.append

        while node_stack:
            children_iterator, parent_visibility = node_stack[-1]
            node = next(children_iterator, None)
            if node is None:
                pop()
            else:
                if node._check_disabled():
                    continue
                node_styles_visibility = node.styles.get_rule("visibility")
                node_is_visible = (
                    node_styles_visibility != "hidden"
                    if node_styles_visibility
                    else parent_visibility  # Inherit visibility if the style is unset.
                )
                if node.is_container and node.allow_focus_children():
                    sorted_displayed_children = sorted(
                        node.displayed_children, key=focus_sorter
                    )
                    push((iter(sorted_displayed_children), node_is_visible))
                # Same check as `if node.focusable`, but we cached inherited visibility
                # and we also skipped disabled nodes altogether.
                if node_is_visible and node.allow_focus():
                    add_widget(node)

        return widgets
```


---

### 🔹 Commit #14: `1e047c76`
- **完整 Hash**: `1e047c767818a664564501f0d91fe99edfb3379e`
- **說明 (Ground Truth)**: restore layout behavior
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/widget.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:415, E:432, A:1) ➔ After(N:415, E:432, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#app** `(Widget)`
    └── ⚡ **on('prune')**
        └── 🎯 [TRIGGERS] `Widget.on_prune()`
            └── 🎯 [CALLS] `_close_messages (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Widget._size_updated()`
- **變更前簽章 (Before)**: `def _size_updated( self, size: Size, virtual_size: Size, container_size: Size, layout: bool = True ) -> bool` (L3995~L4028)
- **變更後簽章 (After)**: `def _size_updated( self, size: Size, virtual_size: Size, container_size: Size, layout: bool = True ) -> bool` (L3995~L4028)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _size_updated(
        self, size: Size, virtual_size: Size, container_size: Size, layout: bool = True
    ) -> bool:
        """Called when the widget's size is updated.

        Args:
            size: Screen size.
            virtual_size: Virtual (scrollable) size.
            container_size: Container size (size of parent).
            layout: Perform layout if required.

        Returns:
            True if a resize event should be sent, otherwise False.
        """

        self._layout_cache.clear()
        if (
            self._size != size
            or self.virtual_size != virtual_size
            or self._container_size != container_size
        ):
            if self._size != size:
                self._set_dirty()
            self._size = size
            # if layout:
            #     self.virtual_size = virtual_size
            # else:
            self.set_reactive(Widget.virtual_size, virtual_size)
            self._container_size = container_size
            if self.is_scrollable:
                self._scroll_update(virtual_size)
            return True
        else:
            return False
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _size_updated(
        self, size: Size, virtual_size: Size, container_size: Size, layout: bool = True
    ) -> bool:
        """Called when the widget's size is updated.

        Args:
            size: Screen size.
            virtual_size: Virtual (scrollable) size.
            container_size: Container size (size of parent).
            layout: Perform layout if required.

        Returns:
            True if a resize event should be sent, otherwise False.
        """

        self._layout_cache.clear()
        if (
            self._size != size
            or self.virtual_size != virtual_size
            or self._container_size != container_size
        ):
            if self._size != size:
                self._set_dirty()
            self._size = size
            if layout:
                self.virtual_size = virtual_size
            else:
                self.set_reactive(Widget.virtual_size, virtual_size)
            self._container_size = container_size
            if self.is_scrollable:
                self._scroll_update(virtual_size)
            return True
        else:
            return False
```


---

### 🔹 Commit #15: `02a7b7bb`
- **完整 Hash**: `02a7b7bb3051bd45ebb10f8fcec6b27d09c591cd`
- **說明 (Ground Truth)**: reduce layout
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/screen.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:209, E:242, A:0) ➔ After(N:209, E:242, A:0)
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

### 🔹 函式: `Screen._on_layout()`
- **變更前簽章 (Before)**: `async def _on_layout(self, message: messages.Layout) -> None` (L1353~L1373)
- **變更後簽章 (After)**: `async def _on_layout(self, message: messages.Layout) -> None` (L1353~L1373)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def _on_layout(self, message: messages.Layout) -> None:
        message.stop()
        message.prevent_default()

        layout_required = False
        widget: DOMNode = message.widget
        for ancestor in message.widget.ancestors:
            if not isinstance(ancestor, Widget):
                break
            if ancestor not in self._layout_widgets:
                self._layout_widgets[ancestor] = set()
            if widget not in self._layout_widgets:
                self._layout_widgets[ancestor].add(widget)
                layout_required = True
            if not ancestor.styles.auto_dimensions:
                break
            widget = ancestor

        if layout_required:
            self._layout_required = True
            self.check_idle()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def _on_layout(self, message: messages.Layout) -> None:
        message.stop()
        message.prevent_default()

        layout_required = False
        widget: DOMNode = message.widget
        for ancestor in message.widget.ancestors:
            if not isinstance(ancestor, Widget):
                break
            if ancestor not in self._layout_widgets:
                self._layout_widgets[ancestor] = set()
            if widget not in self._layout_widgets:
                self._layout_widgets[ancestor].add(widget)
                layout_required = True
            if not ancestor.styles.auto_dimensions:
                break
            widget = ancestor

        if layout_required and not self._layout_required:
            self._layout_required = True
            self.check_idle()
```


---

### 🔹 Commit #16: `374d2968`
- **完整 Hash**: `374d29683f6961bbda8354fccdadb94d064a9560`
- **說明 (Ground Truth)**: Skip bindings change on first refresh
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/widgets/_footer.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:41, E:37, A:2) ➔ After(N:39, E:35, A:2)
- **差分統計**: +Nodes: 0, -Nodes: 2, +Edges: 0, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#app** `(Widget)`
    └── ⚡ **on('mount')**
        └── 🎯 [TRIGGERS] `Footer.on_mount()`
-           └── [CALLS] `call_next (External/Unresolved)()` [已拆除]
-           └── [CALLS] `sleep (External/Unresolved)()` [已拆除]
            └── 🎯 [CALLS] `subscribe (External/Unresolved)()`
    └── ⚡ **on('unmount')**
        └── 🎯 [TRIGGERS] `Footer.on_unmount()`
            └── 🎯 [CALLS] `unsubscribe (External/Unresolved)()`
  🌲 **#mouse** `(Widget)`
    └── ⚡ **on('down')**
        └── 🎯 [TRIGGERS] `FooterKey.on_mouse_down()`
            └── 🎯 [CALLS] `bell (External/Unresolved)()`
            └── 🎯 [CALLS] `simulate_key (External/Unresolved)()`
    └── 🎯 [CALLS] `reactive (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `sleep (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `call_next (External/Unresolved)` (FUNCTION_DEF)
  • - [移除呼叫邊] `Footer.on_mount` ──[CALLS]──> `sleep (External/Unresolved)`
  • - [移除呼叫邊] `Footer.on_mount` ──[CALLS]──> `call_next (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Footer.on_mount()`
- **變更前簽章 (Before)**: `async def on_mount(self) -> None` (L351~L354)
- **變更後簽章 (After)**: `async def on_mount(self) -> None` (L350~L351)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def on_mount(self) -> None:
        await asyncio.sleep(0)
        self.call_next(self.bindings_changed, self.screen)
        self.screen.bindings_updated_signal.subscribe(self, self.bindings_changed)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def on_mount(self) -> None:
        self.screen.bindings_updated_signal.subscribe(self, self.bindings_changed)
```


---

### 🔹 Commit #17: `26610ef5`
- **完整 Hash**: `26610ef5f84fd0a36770337f3fd063763be8886e`
- **說明 (Ground Truth)**: wait for refresh before click
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/pilot.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:40, E:40, A:0) ➔ After(N:41, E:41, A:0)
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
  • + [新增節點] `wait_for_refresh (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Pilot.click` ──[CALLS]──> `wait_for_refresh (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Pilot.click()`
- **變更前簽章 (Before)**: `async def click( self, widget: Widget | type[Widget] | str | None = None, offset: tuple[int, int] = (0, 0), shift: bool = False, meta: bool = False, control: bool = False, times: int = 1, ) -> bool` (L190~L245)
- **變更後簽章 (After)**: `async def click( self, widget: Widget | type[Widget] | str | None = None, offset: tuple[int, int] = (0, 0), shift: bool = False, meta: bool = False, control: bool = False, times: int = 1, ) -> bool` (L190~L246)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def click(
        self,
        widget: Widget | type[Widget] | str | None = None,
        offset: tuple[int, int] = (0, 0),
        shift: bool = False,
        meta: bool = False,
        control: bool = False,
        times: int = 1,
    ) -> bool:
        """Simulate clicking with the mouse at a specified position.

        The final position to be clicked is computed based on the selector provided and
        the offset specified and it must be within the visible area of the screen.

        Implementation note: This method bypasses the normal event processing in `App.on_event`.

        Example:
            The code below runs an app and clicks its only button right in the middle:
            ```py
            async with SingleButtonApp().run_test() as pilot:
                await pilot.click(Button, offset=(8, 1))
            ```

        Args:
            widget: A widget or selector used as an origin
                for the click offset. If this is not specified, the offset is interpreted
                relative to the screen. You can use this parameter to try to click on a
                specific widget. However, if the widget is currently hidden or obscured by
                another widget, the click may not land on the widget you specified.
            offset: The offset to click. The offset is relative to the widget / selector provided
                or to the screen, if no selector is provided.
            shift: Click with the shift key held down.
            meta: Click with the meta key held down.
            control: Click with the control key held down.
            times: The number of times to click. 2 will double-click, 3 will triple-click, etc.

        Raises:
            OutOfBounds: If the position to be clicked is outside of the (visible) screen.

        Returns:
            True if no selector was specified or if the click landed on the selected
                widget, False otherwise.
        """
        try:
            return await self._post_mouse_events(
                [MouseDown, MouseUp, Click],
                widget=widget,
                offset=offset,
                button=1,
                shift=shift,
                meta=meta,
                control=control,
                times=times,
            )
        except OutOfBounds as error:
            raise error from None
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def click(
        self,
        widget: Widget | type[Widget] | str | None = None,
        offset: tuple[int, int] = (0, 0),
        shift: bool = False,
        meta: bool = False,
        control: bool = False,
        times: int = 1,
    ) -> bool:
        """Simulate clicking with the mouse at a specified position.

        The final position to be clicked is computed based on the selector provided and
        the offset specified and it must be within the visible area of the screen.

        Implementation note: This method bypasses the normal event processing in `App.on_event`.

        Example:
            The code below runs an app and clicks its only button right in the middle:
            ```py
            async with SingleButtonApp().run_test() as pilot:
                await pilot.click(Button, offset=(8, 1))
            ```

        Args:
            widget: A widget or selector used as an origin
                for the click offset. If this is not specified, the offset is interpreted
                relative to the screen. You can use this parameter to try to click on a
                specific widget. However, if the widget is currently hidden or obscured by
                another widget, the click may not land on the widget you specified.
            offset: The offset to click. The offset is relative to the widget / selector provided
                or to the screen, if no selector is provided.
            shift: Click with the shift key held down.
            meta: Click with the meta key held down.
            control: Click with the control key held down.
            times: The number of times to click. 2 will double-click, 3 will triple-click, etc.

        Raises:
            OutOfBounds: If the position to be clicked is outside of the (visible) screen.

        Returns:
            True if no selector was specified or if the click landed on the selected
                widget, False otherwise.
        """
        await self.app.wait_for_refresh()
        try:
            return await self._post_mouse_events(
                [MouseDown, MouseUp, Click],
                widget=widget,
                offset=offset,
                button=1,
                shift=shift,
                meta=meta,
                control=control,
                times=times,
            )
        except OutOfBounds as error:
            raise error from None
```


---

### 🔹 Commit #18: `6bfb7e8e`
- **完整 Hash**: `6bfb7e8ee683a78644e6683a1358cb790f606c4b`
- **說明 (Ground Truth)**: Fix `DataTable.header_height` reactive visual glitch and crash (#6128)
- **變更檔案數**: 1

#### 📄 檔案: `src/textual/widgets/_data_table.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:212, E:322, A:0) ➔ After(N:213, E:323, A:0)
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
  • + [新增節點] `DataTable.watch_header_height` (FUNCTION_DEF)
  • + [新增呼叫邊] `DataTable.watch_header_height` ──[CALLS]──> `DataTable._clear_caches`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #19: `9d427840`
- **完整 Hash**: `9d427840349d9a5e9e1f2a25db44af65f72656b4`
- **說明 (Ground Truth)**: process layout hook
- **變更檔案數**: 2

#### 📄 檔案: `src/textual/_arrange.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:31, E:38, A:0) ➔ After(N:32, E:39, A:0)
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
  • + [新增節點] `process_layout (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `arrange` ──[CALLS]──> `process_layout (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `arrange()`
- **變更前簽章 (Before)**: `def arrange( widget: Widget, children: Sequence[Widget], size: Size, viewport: Size, optimal: bool = False, ) -> DockArrangeResult` (L39~L124)
- **變更後簽章 (After)**: `def arrange( widget: Widget, children: Sequence[Widget], size: Size, viewport: Size, optimal: bool = False, ) -> DockArrangeResult` (L39~L126)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def arrange(
    widget: Widget,
    children: Sequence[Widget],
    size: Size,
    viewport: Size,
    optimal: bool = False,
) -> DockArrangeResult:
    """Arrange widgets by applying docks and calling layouts

    Args:
        widget: The parent (container) widget.
        size: The size of the available area.
        viewport: The size of the viewport (terminal).

    Returns:
        Widget arrangement information.
    """

    placements: list[WidgetPlacement] = []
    scroll_spacing = NULL_SPACING
    styles = widget.styles

    # Widgets which will be displayed
    # display_widgets = [child for child in children if get_display(child) != "none"]
    display_widgets = list(filter(_get_display, children))
    # Widgets organized into layers
    layers = _build_layers(display_widgets)

    for widgets in layers.values():
        # Partition widgets into split widgets and non-split widgets
        non_split_widgets, split_widgets = partition(_get_split, widgets)
        if split_widgets:
            _split_placements, dock_region = _arrange_split_widgets(
                split_widgets, size, viewport
            )
            placements.extend(_split_placements)
        else:
            dock_region = size.region

        split_spacing = size.region.get_spacing_between(dock_region)

        # Partition widgets into "layout" widgets (those that appears in the normal 'flow' of the
        # document), and "dock" widgets which are positioned relative to an edge
        layout_widgets, dock_widgets = partition(_get_dock, non_split_widgets)

        # Arrange docked widgets
        if dock_widgets:
            _dock_placements, dock_spacing = _arrange_dock_widgets(
                dock_widgets, dock_region, viewport, greedy=not optimal
            )
            placements.extend(_dock_placements)
            dock_region = dock_region.shrink(dock_spacing)
        else:
            dock_spacing = Spacing()

        dock_spacing += split_spacing

        if layout_widgets:
            # Arrange layout widgets (i.e. not docked)
            layout_placements = widget.layout.arrange(
                widget, layout_widgets, dock_region.size, greedy=not optimal
            )
            scroll_spacing = scroll_spacing.grow_maximum(dock_spacing)
            placement_offset = dock_region.offset
            # Perform any alignment of the widgets.
            if styles.align_horizontal != "left" or styles.align_vertical != "top":
                bounding_region = WidgetPlacement.get_bounds(layout_placements)
                container_width, container_height = dock_region.size
                placement_offset += styles._align_size(
                    bounding_region.size,
                    widget._extrema.apply_dimensions(
                        0 if styles.is_auto_width else container_width,
                        0 if styles.is_auto_height else container_height,
                    ),
                ).clamped

            if placement_offset:
                # Translate placements if required.
                layout_placements = WidgetPlacement.translate(
                    layout_placements, placement_offset
                )

            WidgetPlacement.apply_absolute(layout_placements)
            placements.extend(layout_placements)

    return DockArrangeResult(placements, set(display_widgets), scroll_spacing)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def arrange(
    widget: Widget,
    children: Sequence[Widget],
    size: Size,
    viewport: Size,
    optimal: bool = False,
) -> DockArrangeResult:
    """Arrange widgets by applying docks and calling layouts

    Args:
        widget: The parent (container) widget.
        size: The size of the available area.
        viewport: The size of the viewport (terminal).

    Returns:
        Widget arrangement information.
    """

    placements: list[WidgetPlacement] = []
    scroll_spacing = NULL_SPACING
    styles = widget.styles

    # Widgets which will be displayed
    # display_widgets = [child for child in children if get_display(child) != "none"]
    display_widgets = list(filter(_get_display, children))
    # Widgets organized into layers
    layers = _build_layers(display_widgets)

    for widgets in layers.values():
        # Partition widgets into split widgets and non-split widgets
        non_split_widgets, split_widgets = partition(_get_split, widgets)
        if split_widgets:
            _split_placements, dock_region = _arrange_split_widgets(
                split_widgets, size, viewport
            )
            placements.extend(_split_placements)
        else:
            dock_region = size.region

        split_spacing = size.region.get_spacing_between(dock_region)

        # Partition widgets into "layout" widgets (those that appears in the normal 'flow' of the
        # document), and "dock" widgets which are positioned relative to an edge
        layout_widgets, dock_widgets = partition(_get_dock, non_split_widgets)

        # Arrange docked widgets
        if dock_widgets:
            _dock_placements, dock_spacing = _arrange_dock_widgets(
                dock_widgets, dock_region, viewport, greedy=not optimal
            )
            placements.extend(_dock_placements)
            dock_region = dock_region.shrink(dock_spacing)
        else:
            dock_spacing = Spacing()

        dock_spacing += split_spacing

        if layout_widgets:
            # Arrange layout widgets (i.e. not docked)
            layout_placements = widget.process_layout(
                widget.layout.arrange(
                    widget, layout_widgets, dock_region.size, greedy=not optimal
                )
            )
            scroll_spacing = scroll_spacing.grow_maximum(dock_spacing)
            placement_offset = dock_region.offset
            # Perform any alignment of the widgets.
            if styles.align_horizontal != "left" or styles.align_vertical != "top":
                bounding_region = WidgetPlacement.get_bounds(layout_placements)
                container_width, container_height = dock_region.size
                placement_offset += styles._align_size(
                    bounding_region.size,
                    widget._extrema.apply_dimensions(
                        0 if styles.is_auto_width else container_width,
                        0 if styles.is_auto_height else container_height,
                    ),
                ).clamped

            if placement_offset:
                # Translate placements if required.
                layout_placements = WidgetPlacement.translate(
                    layout_placements, placement_offset
                )

            WidgetPlacement.apply_absolute(layout_placements)
            placements.extend(layout_placements)

    return DockArrangeResult(placements, set(display_widgets), scroll_spacing)
```


#### 📄 檔案: `src/textual/widget.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:414, E:431, A:1) ➔ After(N:415, E:431, A:1)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#app** `(Widget)`
    └── ⚡ **on('prune')**
        └── 🎯 [TRIGGERS] `Widget.on_prune()`
            └── 🎯 [CALLS] `_close_messages (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Widget.process_layout` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #20: `f047dc1b`
- **完整 Hash**: `f047dc1b117ad9a7798bc06c56f7660a4c54aaf1`
- **說明 (Ground Truth)**: revert UserInsert message
- **變更檔案數**: 2

#### 📄 檔案: `src/textual/content.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:125, E:145, A:0) ➔ After(N:125, E:145, A:0)
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

### 🔹 函式: `Content.highlight_regex()`
- **變更前簽章 (Before)**: `def highlight_regex( self, highlight_regex: re.Pattern[str] | str, *, style: Style | str, maximum_highlights: int | None = None, ) -> Content` (L1479~L1512)
- **變更後簽章 (After)**: `def highlight_regex( self, highlight_regex: re.Pattern[str] | str, *, style: Style | str, maximum_highlights: int | None = None, ) -> Content` (L1479~L1514)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def highlight_regex(
        self,
        highlight_regex: re.Pattern[str] | str,
        *,
        style: Style | str,
        maximum_highlights: int | None = None,
    ) -> Content:
        """Apply a style to text that matches a regular expression.

        Args:
            highlight_regex: Regular expression as a string, or compiled.
            style: Style to apply.
            maximum_highlights: Maximum number of matches to highlight, or `None` for no maximum.

        Returns:
            new content.
        """
        spans: list[Span] = self._spans.copy()
        append_span = spans.append
        _Span = Span
        plain = self.plain
        if isinstance(highlight_regex, str):
            re_highlight = re.compile(highlight_regex)
        count = 0
        for match in re_highlight.finditer(plain):
            start, end = match.span()
            if end > start:
                append_span(_Span(start, end, style))
            if (
                maximum_highlights is not None
                and (count := count + 1) >= maximum_highlights
            ):
                break
        return Content(self._text, spans)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def highlight_regex(
        self,
        highlight_regex: re.Pattern[str] | str,
        *,
        style: Style | str,
        maximum_highlights: int | None = None,
    ) -> Content:
        """Apply a style to text that matches a regular expression.

        Args:
            highlight_regex: Regular expression as a string, or compiled.
            style: Style to apply.
            maximum_highlights: Maximum number of matches to highlight, or `None` for no maximum.

        Returns:
            new content.
        """
        spans: list[Span] = self._spans.copy()
        append_span = spans.append
        _Span = Span
        plain = self.plain
        if isinstance(highlight_regex, str):
            re_highlight = re.compile(highlight_regex)
        else:
            re_highlight = highlight_regex
        count = 0
        for match in re_highlight.finditer(plain):
            start, end = match.span()
            if end > start:
                append_span(_Span(start, end, style))
            if (
                maximum_highlights is not None
                and (count := count + 1) >= maximum_highlights
            ):
                break
        return Content(self._text, spans)
```


#### 📄 檔案: `src/textual/widgets/_text_area.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:254, E:290, A:0) ➔ After(N:253, E:289, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 0, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `UserInsert.control` (FUNCTION_DEF)
  • - [移除呼叫邊] `TextArea._replace_via_keyboard` ──[CALLS]──> `post_message (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TextArea._replace_via_keyboard()`
- **變更前簽章 (Before)**: `def _replace_via_keyboard( self, insert: str, start: Location, end: Location, ) -> EditResult | None` (L2428~L2447)
- **變更後簽章 (After)**: `def _replace_via_keyboard( self, insert: str, start: Location, end: Location, ) -> EditResult | None` (L2411~L2429)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _replace_via_keyboard(
        self,
        insert: str,
        start: Location,
        end: Location,
    ) -> EditResult | None:
        """Handle a replacement performed using a keyboard (as opposed to the API).

        Args:
            insert: The text to insert into the document.
            start: The start location of the text to replace.
            end: The end location of the text to replace.

        Returns:
            An EditResult or None if no edit was performed (e.g. on read-only mode).
        """
        if self.read_only:
            return None
        self.post_message(self.UserInsert(start, insert, self))
        return self.replace(insert, start, end, maintain_selection_offset=False)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _replace_via_keyboard(
        self,
        insert: str,
        start: Location,
        end: Location,
    ) -> EditResult | None:
        """Handle a replacement performed using a keyboard (as opposed to the API).

        Args:
            insert: The text to insert into the document.
            start: The start location of the text to replace.
            end: The end location of the text to replace.

        Returns:
            An EditResult or None if no edit was performed (e.g. on read-only mode).
        """
        if self.read_only:
            return None
        return self.replace(insert, start, end, maintain_selection_offset=False)
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/textual show 01fb6fd73af092fe6e5da03c032d3e9c3fa161f1
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 01fb6fd73af092fe6e5da03c032d3e9c3fa161f1~1 --file test_repos/textual/src/textual/widgets/_text_area.py
   ```
