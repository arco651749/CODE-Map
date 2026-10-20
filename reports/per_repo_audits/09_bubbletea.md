# 🔬 CODE-Map 基準審查獨立驗證報告: `bubbletea`
> **技術生態**: `Go (TUI / Elm 現代響應架構)`  
> **本地倉庫路徑**: `test_repos/bubbletea`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 24 Files  
> **報告生成時間**: 2026-10-20 21:41:10  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `11` / `24` | `45.8%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `8` / `24` | `33.3%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `5` / `24` | `20.8%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`19` / `24`** | **`79.2%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `24` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `96d69d2f`
- **完整 Hash**: `96d69d2f7eb182bb311be08fc56ed2c208239aff`
- **說明 (Ground Truth)**: fix(tty): fall back to default dimensions when terminal size is 0x0 (#1836)
- **變更檔案數**: 2

#### 📄 檔案: `tea.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:159, E:209, A:0) ➔ After(N:160, E:210, A:0)
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
  • + [新增節點] `p.fallbackDimensions (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Program.Run` ──[CALLS]──> `p.fallbackDimensions (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Program.Run()`
- **變更前簽章 (Before)**: `func Program.Run()` (L1001~L1185)
- **變更後簽章 (After)**: `func Program.Run()` (L1001~L1185)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Program) Run() (returnModel Model, returnErr error) {
	if p.initialModel == nil {
		return nil, errors.New("bubbletea: InitialModel cannot be nil")
	}

	// Initialize context and teardown channel.
	p.handlers = channelHandlers{}
	cmds := make(chan Cmd)

	p.finished = make(chan struct{})
	defer func() {
		close(p.finished)
	}()

	defer p.cancel()

	if p.disableInput {
		p.input = nil
	} else if p.input == nil {
		p.input = os.Stdin
		if !term.IsTerminal(os.Stdin.Fd()) {
			ttyIn, _, err := OpenTTY()
			if err != nil {
				return p.initialModel, fmt.Errorf("bubbletea: error opening TTY: %w", err)
			}
			p.input = ttyIn
		}
	}

	// Handle signals.
	if !p.disableSignalHandler {
		p.handlers.add(p.handleSignals())
	}

	// Recover from panics.
	if !p.disableCatchPanics {
		defer func() {
			if r := recover(); r != nil {
				returnErr = fmt.Errorf("%w: %w", ErrProgramKilled, ErrProgramPanic)
				p.recoverFromPanic(r)
			}
		}()
	}

	// Check if output is a TTY before entering raw mode, hiding the cursor and
	// so on.
	if err := p.initTerminal(); err != nil {
		return p.initialModel, err
	}

	// Get the initial window size.
	width, height := p.width, p.height
	if p.ttyOutput != nil {
		// Set the initial size of the terminal.
		w, h, err := term.GetSize(p.ttyOutput.Fd())
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error getting terminal size: %w", err)
		}

		width, height = w, h
	}

	p.width, p.height = width, height
	resizeMsg := WindowSizeMsg{Width: p.width, Height: p.height}

	if p.renderer == nil {
		if p.disableRenderer {
			p.renderer = &nilRenderer{}
		} else {
			// If no renderer is set use the cursed one.
			r := newCursedRenderer(
				p.output,
				p.environ,
				p.width,
				p.height,
			)
			r.setLogger(p.logger)
			r.setNoInput(p.disableInput)
			// XXX: This breaks many things especially when we want the output
			// to be compatible with terminals that are not necessary a TTY.
			// This was originally done to work around a Wish emulated-pty
			// issue where when a PTY session is detected, and we don't
			// allocate a real PTY, the terminal settings (Termios and WinCon)
			// don't change and the we end up working in cooked mode instead of
			// raw mode. See issue #1572.
			mapNl := runtime.GOOS != "windows" && p.ttyInput == nil
			r.setOptimizations(p.useHardTabs, p.useBackspace, mapNl)
			p.renderer = r
		}
	}

	// Get the color profile and send it to the program.
	if p.profile == nil {
		cp := colorprofile.Detect(p.output, p.environ)
		p.profile = &cp
	}

	// Set the color profile on the renderer and send it to the program.
	p.renderer.setColorProfile(*p.profile)
	go p.Send(ColorProfileMsg{*p.profile})

	// Send the initial size to the program.
	go p.Send(resizeMsg)
	p.renderer.resize(resizeMsg.Width, resizeMsg.Height)

	// Send the environment variables used by the program.
	go p.Send(EnvMsg(p.environ))

	// Init the input reader and initial model.
	model := p.initialModel
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return model, err
		}
	}

	// Start the renderer.
	p.startRenderer()

	if !p.disableRenderer && shouldQuerySynchronizedOutput(p.environ) {
		// Query for synchronized updates support (mode 2026) and unicode core
		// (mode 2027). If the terminal supports it, the renderer will enable
		// it once we get the response.
		p.executeQuery(ansi.RequestModeSynchronizedOutput +
			ansi.RequestModeUnicodeCore)
	}

	// Initialize the program.
	initCmd := model.Init()
	if initCmd != nil {
		ch := make(chan struct{})
		p.handlers.add(ch)

		go func() {
			defer close(ch)

			select {
			case cmds <- initCmd:
			case <-p.ctx.Done():
			}
		}()
	}

	// Render the initial view.
	p.render(model)

	// Handle resize events.
	p.handlers.add(p.handleResize())

	// Process commands.
	p.handlers.add(p.handleCommands(cmds))

	// Run event loop, handle updates and draw.
	var err error
	model, err = p.eventLoop(model, cmds)

	if err == nil && len(p.errs) > 0 {
		err = <-p.errs // Drain a leftover error in case eventLoop crashed.
	}

	killed := p.externalCtx.Err() != nil || p.ctx.Err() != nil || err != nil
	if killed {
		if err == nil && p.externalCtx.Err() != nil {
			// Return also as context error the cancellation of an external context.
			// This is the context the user knows about and should be able to act on.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, p.externalCtx.Err())
		} else if err == nil && p.ctx.Err() != nil {
			// Return only that the program was killed (not the internal mechanism).
			// The user does not know or need to care about the internal program context.
			err = ErrProgramKilled
		} else {
			// Return that the program was killed and also the error that caused it.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, err)
		}
	} else {
		// Graceful shutdown of the program (not killed):
		// Ensure we rendered the final state of the model.
		p.render(model)
	}

	// Restore terminal state.
	p.shutdown(killed)

	return model, err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Program) Run() (returnModel Model, returnErr error) {
	if p.initialModel == nil {
		return nil, errors.New("bubbletea: InitialModel cannot be nil")
	}

	// Initialize context and teardown channel.
	p.handlers = channelHandlers{}
	cmds := make(chan Cmd)

	p.finished = make(chan struct{})
	defer func() {
		close(p.finished)
	}()

	defer p.cancel()

	if p.disableInput {
		p.input = nil
	} else if p.input == nil {
		p.input = os.Stdin
		if !term.IsTerminal(os.Stdin.Fd()) {
			ttyIn, _, err := OpenTTY()
			if err != nil {
				return p.initialModel, fmt.Errorf("bubbletea: error opening TTY: %w", err)
			}
			p.input = ttyIn
		}
	}

	// Handle signals.
	if !p.disableSignalHandler {
		p.handlers.add(p.handleSignals())
	}

	// Recover from panics.
	if !p.disableCatchPanics {
		defer func() {
			if r := recover(); r != nil {
				returnErr = fmt.Errorf("%w: %w", ErrProgramKilled, ErrProgramPanic)
				p.recoverFromPanic(r)
			}
		}()
	}

	// Check if output is a TTY before entering raw mode, hiding the cursor and
	// so on.
	if err := p.initTerminal(); err != nil {
		return p.initialModel, err
	}

	// Get the initial window size.
	width, height := p.width, p.height
	if p.ttyOutput != nil {
		// Set the initial size of the terminal.
		w, h, err := term.GetSize(p.ttyOutput.Fd())
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error getting terminal size: %w", err)
		}

		width, height = p.fallbackDimensions(w, h)
	}

	p.width, p.height = width, height
	resizeMsg := WindowSizeMsg{Width: p.width, Height: p.height}

	if p.renderer == nil {
		if p.disableRenderer {
			p.renderer = &nilRenderer{}
		} else {
			// If no renderer is set use the cursed one.
			r := newCursedRenderer(
				p.output,
				p.environ,
				p.width,
				p.height,
			)
			r.setLogger(p.logger)
			r.setNoInput(p.disableInput)
			// XXX: This breaks many things especially when we want the output
			// to be compatible with terminals that are not necessary a TTY.
			// This was originally done to work around a Wish emulated-pty
			// issue where when a PTY session is detected, and we don't
			// allocate a real PTY, the terminal settings (Termios and WinCon)
			// don't change and the we end up working in cooked mode instead of
			// raw mode. See issue #1572.
			mapNl := runtime.GOOS != "windows" && p.ttyInput == nil
			r.setOptimizations(p.useHardTabs, p.useBackspace, mapNl)
			p.renderer = r
		}
	}

	// Get the color profile and send it to the program.
	if p.profile == nil {
		cp := colorprofile.Detect(p.output, p.environ)
		p.profile = &cp
	}

	// Set the color profile on the renderer and send it to the program.
	p.renderer.setColorProfile(*p.profile)
	go p.Send(ColorProfileMsg{*p.profile})

	// Send the initial size to the program.
	go p.Send(resizeMsg)
	p.renderer.resize(resizeMsg.Width, resizeMsg.Height)

	// Send the environment variables used by the program.
	go p.Send(EnvMsg(p.environ))

	// Init the input reader and initial model.
	model := p.initialModel
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return model, err
		}
	}

	// Start the renderer.
	p.startRenderer()

	if !p.disableRenderer && shouldQuerySynchronizedOutput(p.environ) {
		// Query for synchronized updates support (mode 2026) and unicode core
		// (mode 2027). If the terminal supports it, the renderer will enable
		// it once we get the response.
		p.executeQuery(ansi.RequestModeSynchronizedOutput +
			ansi.RequestModeUnicodeCore)
	}

	// Initialize the program.
	initCmd := model.Init()
	if initCmd != nil {
		ch := make(chan struct{})
		p.handlers.add(ch)

		go func() {
			defer close(ch)

			select {
			case cmds <- initCmd:
			case <-p.ctx.Done():
			}
		}()
	}

	// Render the initial view.
	p.render(model)

	// Handle resize events.
	p.handlers.add(p.handleResize())

	// Process commands.
	p.handlers.add(p.handleCommands(cmds))

	// Run event loop, handle updates and draw.
	var err error
	model, err = p.eventLoop(model, cmds)

	if err == nil && len(p.errs) > 0 {
		err = <-p.errs // Drain a leftover error in case eventLoop crashed.
	}

	killed := p.externalCtx.Err() != nil || p.ctx.Err() != nil || err != nil
	if killed {
		if err == nil && p.externalCtx.Err() != nil {
			// Return also as context error the cancellation of an external context.
			// This is the context the user knows about and should be able to act on.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, p.externalCtx.Err())
		} else if err == nil && p.ctx.Err() != nil {
			// Return only that the program was killed (not the internal mechanism).
			// The user does not know or need to care about the internal program context.
			err = ErrProgramKilled
		} else {
			// Return that the program was killed and also the error that caused it.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, err)
		}
	} else {
		// Graceful shutdown of the program (not killed):
		// Ensure we rendered the final state of the model.
		p.render(model)
	}

	// Restore terminal state.
	p.shutdown(killed)

	return model, err
}
```


#### 📄 檔案: `tty.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:31, E:30, A:0) ➔ After(N:36, E:34, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 0, +Edges: 4, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `lines` (MODULE_STATE)
  • + [新增節點] `strconv.Atoi (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `cols` (MODULE_STATE)
  • + [新增節點] `os.Getenv (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `Program.fallbackDimensions` (FUNCTION_DEF)
  • + [新增呼叫邊] `Program.fallbackDimensions` ──[CALLS]──> `p.environ.Getenv (External/Pkg)`
  • + [新增呼叫邊] `Program.fallbackDimensions` ──[CALLS]──> `os.Getenv (External/Pkg)`
  • + [新增呼叫邊] `Program.fallbackDimensions` ──[CALLS]──> `strconv.Atoi (External/Pkg)`
  • + [新增呼叫邊] `Program.checkResize` ──[CALLS]──> `Program.fallbackDimensions`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Program.checkResize()`
- **變更前簽章 (Before)**: `func Program.checkResize()` (L109~L127)
- **變更後簽章 (After)**: `func Program.checkResize()` (L147~L167)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Program) checkResize() {
	if p.ttyOutput == nil {
		// can't query window size
		return
	}

	w, h, err := term.GetSize(p.ttyOutput.Fd())
	if err != nil {
		select {
		case <-p.ctx.Done():
		case p.errs <- err:
		}

		return
	}

	p.width, p.height = w, h
	p.Send(WindowSizeMsg{Width: w, Height: h})
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Program) checkResize() {
	if p.ttyOutput == nil {
		// can't query window size
		return
	}

	w, h, err := term.GetSize(p.ttyOutput.Fd())
	if err != nil {
		select {
		case <-p.ctx.Done():
		case p.errs <- err:
		}

		return
	}

	w, h = p.fallbackDimensions(w, h)

	p.width, p.height = w, h
	p.Send(WindowSizeMsg{Width: w, Height: h})
}
```


---

### 🔹 Commit #02: `ff51ba4c`
- **完整 Hash**: `ff51ba4c51f85875761b15a64f9ab9aa0eaa9fa1`
- **說明 (Ground Truth)**: fix: prevent signal goroutine deadlock on shutdown (#1806)
- **變更檔案數**: 1

#### 📄 檔案: `tea.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:158, E:209, A:0) ➔ After(N:159, E:209, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 1, +Edges: 1, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `msg` (MODULE_STATE)
  • + [新增節點] `func() {
		sig := make(chan os.Signal, 1)
		signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
		defer func() {
			signal.Stop(sig)
			close(ch)
		}()

		for {
			select {
			case <-p.ctx.Done():
				return

			case s := <-sig:
				if atomic.LoadUint32(&p.ignoreSignals) == 0 {
					var msg Msg = QuitMsg{}
					if s == syscall.SIGINT {
						msg = InterruptMsg{}
					}
					select {
					case p.msgs <- msg:
					case <-p.ctx.Done():
					}
					return
				}
			}
		}
	} (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `func() {
		sig := make(chan os.Signal, 1)
		signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
		defer func() {
			signal.Stop(sig)
			close(ch)
		}()

		for {
			select {
			case <-p.ctx.Done():
				return

			case s := <-sig:
				if atomic.LoadUint32(&p.ignoreSignals) == 0 {
					switch s {
					case syscall.SIGINT:
						p.msgs <- InterruptMsg{}
					default:
						p.msgs <- QuitMsg{}
					}
					return
				}
			}
		}
	} (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Program.handleSignals` ──[CALLS]──> `func() {
		sig := make(chan os.Signal, 1)
		signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
		defer func() {
			signal.Stop(sig)
			close(ch)
		}()

		for {
			select {
			case <-p.ctx.Done():
				return

			case s := <-sig:
				if atomic.LoadUint32(&p.ignoreSignals) == 0 {
					var msg Msg = QuitMsg{}
					if s == syscall.SIGINT {
						msg = InterruptMsg{}
					}
					select {
					case p.msgs <- msg:
					case <-p.ctx.Done():
					}
					return
				}
			}
		}
	} (External/Pkg)`
  • - [移除呼叫邊] `Program.handleSignals` ──[CALLS]──> `func() {
		sig := make(chan os.Signal, 1)
		signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
		defer func() {
			signal.Stop(sig)
			close(ch)
		}()

		for {
			select {
			case <-p.ctx.Done():
				return

			case s := <-sig:
				if atomic.LoadUint32(&p.ignoreSignals) == 0 {
					switch s {
					case syscall.SIGINT:
						p.msgs <- InterruptMsg{}
					default:
						p.msgs <- QuitMsg{}
					}
					return
				}
			}
		}
	} (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Program.handleSignals()`
- **變更前簽章 (Before)**: `func Program.handleSignals()` (L651~L690)
- **變更後簽章 (After)**: `func Program.handleSignals()` (L651~L692)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Program) handleSignals() chan struct{} {
	ch := make(chan struct{})

	// Listen for SIGINT and SIGTERM.
	//
	// In most cases ^C will not send an interrupt because the terminal will be
	// in raw mode and ^C will be captured as a keystroke and sent along to
	// Program.Update as a KeyMsg. When input is not a TTY, however, ^C will be
	// caught here.
	//
	// SIGTERM is sent by unix utilities (like kill) to terminate a process.
	go func() {
		sig := make(chan os.Signal, 1)
		signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
		defer func() {
			signal.Stop(sig)
			close(ch)
		}()

		for {
			select {
			case <-p.ctx.Done():
				return

			case s := <-sig:
				if atomic.LoadUint32(&p.ignoreSignals) == 0 {
					switch s {
					case syscall.SIGINT:
						p.msgs <- InterruptMsg{}
					default:
						p.msgs <- QuitMsg{}
					}
					return
				}
			}
		}
	}()

	return ch
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Program) handleSignals() chan struct{} {
	ch := make(chan struct{})

	// Listen for SIGINT and SIGTERM.
	//
	// In most cases ^C will not send an interrupt because the terminal will be
	// in raw mode and ^C will be captured as a keystroke and sent along to
	// Program.Update as a KeyMsg. When input is not a TTY, however, ^C will be
	// caught here.
	//
	// SIGTERM is sent by unix utilities (like kill) to terminate a process.
	go func() {
		sig := make(chan os.Signal, 1)
		signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
		defer func() {
			signal.Stop(sig)
			close(ch)
		}()

		for {
			select {
			case <-p.ctx.Done():
				return

			case s := <-sig:
				if atomic.LoadUint32(&p.ignoreSignals) == 0 {
					var msg Msg = QuitMsg{}
					if s == syscall.SIGINT {
						msg = InterruptMsg{}
					}
					select {
					case p.msgs <- msg:
					case <-p.ctx.Done():
					}
					return
				}
			}
		}
	}()

	return ch
}
```


---

### 🔹 Commit #03: `0d3e281d`
- **完整 Hash**: `0d3e281d1436499b40df085a352bb81b3c9de7d0`
- **說明 (Ground Truth)**: fix: restore kitty keyboard stack on exit (#1750)
- **變更檔案數**: 2

#### 📄 檔案: `cursed_renderer.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:108, E:161, A:0) ➔ After(N:112, E:165, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 6, -Edges: 2, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `ansi.PushKittyKeyboard (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `cursedRenderer.setNoInput` (FUNCTION_DEF)
  • + [新增節點] `ansi.PopKittyKeyboard (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `cursedRenderer.resetKeyboardEnhancements` (FUNCTION_DEF)
  • + [新增呼叫邊] `cursedRenderer.resetKeyboardEnhancements` ──[CALLS]──> `buf.WriteString (External/Pkg)`
  • + [新增呼叫邊] `cursedRenderer.resetKeyboardEnhancements` ──[CALLS]──> `ansi.PopKittyKeyboard (External/Pkg)`
  • + [新增呼叫邊] `cursedRenderer.start` ──[CALLS]──> `ansi.PushKittyKeyboard (External/Pkg)`
  • + [新增呼叫邊] `cursedRenderer.close` ──[CALLS]──> `ansi.PopKittyKeyboard (External/Pkg)`
  • + [新增呼叫邊] `cursedRenderer.flush` ──[CALLS]──> `ansi.PushKittyKeyboard (External/Pkg)`
  • + [新增呼叫邊] `cursedRenderer.flush` ──[CALLS]──> `cursedRenderer.resetKeyboardEnhancements`
  • - [移除呼叫邊] `cursedRenderer.start` ──[CALLS]──> `ansi.KittyKeyboard (External/Pkg)`
  • - [移除呼叫邊] `cursedRenderer.close` ──[CALLS]──> `ansi.KittyKeyboard (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `cursedRenderer.close()`
- **變更前簽章 (Before)**: `func cursedRenderer.close()` (L144~L247)
- **變更後簽章 (After)**: `func cursedRenderer.close()` (L172~L279)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *cursedRenderer) close() (err error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Exit the altScreen and show cursor before closing. It's important that
	// we don't change the [cursedRenderer] altScreen and cursorHidden states
	// so that we can restore them when we start the renderer again. This is
	// used when the user suspends the program and then resumes it.
	if lv := s.lastView; lv != nil { //nolint:nestif
		// NOTE: The Kitty keyboard specs specify that the terminal should have
		// two registries for the main and alt screens. We disable keyboard
		// enhancements whenever we enter/exit alt screen mode in
		// [cursedRenderer.flush].
		// Here, we reset the keyboard protocol of the last screen used
		// assuming the other screen is already reset when we switched screens.
		_, _ = s.buf.WriteString(ansi.ResetModifyOtherKeys)
		_, _ = s.buf.WriteString(ansi.KittyKeyboard(0, 1))

		// Go to the bottom of the screen.
		// We need to go to the bottom of the screen regardless of whether
		// we're in alt screen mode or not to avoid leaving the cursor in the
		// middle in terminals that don't support alt screen mode.
		s.scr.MoveTo(0, s.cellbuf.Height()-1)
		_ = s.scr.Flush() // we need to flush to write the cursor movement
		if lv.AltScreen {
			enableAltScreen(s, false, true)
		} else {
			_, _ = s.scr.WriteString(ansi.EraseScreenBelow)
		}
		if lv.Cursor == nil {
			enableTextCursor(s, true)
		}
		if !lv.DisableBracketedPasteMode {
			_, _ = s.scr.WriteString(ansi.ResetModeBracketedPaste)
		}
		if lv.ReportFocus {
			_, _ = s.scr.WriteString(ansi.ResetModeFocusEvent)
		}
		switch lv.MouseMode {
		case MouseModeNone:
		case MouseModeCellMotion, MouseModeAllMotion:
			_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent +
				ansi.ResetModeMouseAnyEvent +
				ansi.ResetModeMouseExtSgr)
		}

		if lv.WindowTitle != "" {
			// Clear the window title if it was set.
			_, _ = s.scr.WriteString(ansi.SetWindowTitle(""))
		}
		if lc := lv.Cursor; lc != nil {
			curShape := encodeCursorStyle(lc.Shape, lc.Blink)
			if curShape != 0 && curShape != 1 {
				// Reset the cursor style to default if it was set to something other
				// blinking block.
				_, _ = s.scr.WriteString(ansi.SetCursorStyle(0))
			}

			if lc.Color != nil {
				_, _ = s.scr.WriteString(ansi.ResetCursorColor)
			}
		}

		if lv.BackgroundColor != nil {
			_, _ = s.scr.WriteString(ansi.ResetBackgroundColor)
		}
		if lv.ForegroundColor != nil {
			_, _ = s.scr.WriteString(ansi.ResetForegroundColor)
		}
		if lv.ProgressBar != nil && lv.ProgressBar.State != ProgressBarNone {
			_, _ = s.scr.WriteString(ansi.ResetProgressBar)
		}
	}

	if s.cellbuf.Method == ansi.GraphemeWidth {
		// Make sure to turn off Unicode mode (2027)
		_, _ = s.scr.WriteString(ansi.ResetModeUnicodeCore)
	}

	if err := s.scr.Flush(); err != nil {
		return fmt.Errorf("bubbletea: error closing screen writer: %w", err)
	}

	if s.buf.Len() > 0 {
		if s.logger != nil {
			s.logger.Printf("output: %q", s.buf.String())
		}
		if _, err := io.Copy(s.w, &s.buf); err != nil {
			return fmt.Errorf("bubbletea: error writing to screen: %w", err)
		}
		s.buf.Reset()
	}

	x, y := s.scr.Position()

	// We want to clear the renderer state but not the cursor position. This is
	// because we might be putting the tea process in the background, run some
	// other process, and then return to the tea process. We want to keep the
	// cursor position so that we can continue where we left off.
	reset(s)
	s.scr.SetPosition(x, y)

	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *cursedRenderer) close() (err error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Exit the altScreen and show cursor before closing. It's important that
	// we don't change the [cursedRenderer] altScreen and cursorHidden states
	// so that we can restore them when we start the renderer again. This is
	// used when the user suspends the program and then resumes it.
	if lv := s.lastView; lv != nil { //nolint:nestif
		// NOTE: The Kitty keyboard specs specify that the terminal should have
		// two registries for the main and alt screens. We disable keyboard
		// enhancements whenever we enter/exit alt screen mode in
		// [cursedRenderer.flush].
		// Here, we pop the keyboard protocol of the last screen used
		// assuming the other screen is already popped when we switched
		// screens. With input disabled we never pushed an entry, so there is
		// nothing to pop.
		if !s.noInput {
			_, _ = s.buf.WriteString(ansi.ResetModifyOtherKeys)
			_, _ = s.buf.WriteString(ansi.PopKittyKeyboard(1))
		}

		// Go to the bottom of the screen.
		// We need to go to the bottom of the screen regardless of whether
		// we're in alt screen mode or not to avoid leaving the cursor in the
		// middle in terminals that don't support alt screen mode.
		s.scr.MoveTo(0, s.cellbuf.Height()-1)
		_ = s.scr.Flush() // we need to flush to write the cursor movement
		if lv.AltScreen {
			enableAltScreen(s, false, true)
		} else {
			_, _ = s.scr.WriteString(ansi.EraseScreenBelow)
		}
		if lv.Cursor == nil {
			enableTextCursor(s, true)
		}
		if !lv.DisableBracketedPasteMode {
			_, _ = s.scr.WriteString(ansi.ResetModeBracketedPaste)
		}
		if lv.ReportFocus {
			_, _ = s.scr.WriteString(ansi.ResetModeFocusEvent)
		}
		switch lv.MouseMode {
		case MouseModeNone:
		case MouseModeCellMotion, MouseModeAllMotion:
			_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent +
				ansi.ResetModeMouseAnyEvent +
				ansi.ResetModeMouseExtSgr)
		}

		if lv.WindowTitle != "" {
			// Clear the window title if it was set.
			_, _ = s.scr.WriteString(ansi.SetWindowTitle(""))
		}
		if lc := lv.Cursor; lc != nil {
			curShape := encodeCursorStyle(lc.Shape, lc.Blink)
			if curShape != 0 && curShape != 1 {
				// Reset the cursor style to default if it was set to something other
				// blinking block.
				_, _ = s.scr.WriteString(ansi.SetCursorStyle(0))
			}

			if lc.Color != nil {
				_, _ = s.scr.WriteString(ansi.ResetCursorColor)
			}
		}

		if lv.BackgroundColor != nil {
			_, _ = s.scr.WriteString(ansi.ResetBackgroundColor)
		}
		if lv.ForegroundColor != nil {
			_, _ = s.scr.WriteString(ansi.ResetForegroundColor)
		}
		if lv.ProgressBar != nil && lv.ProgressBar.State != ProgressBarNone {
			_, _ = s.scr.WriteString(ansi.ResetProgressBar)
		}
	}

	if s.cellbuf.Method == ansi.GraphemeWidth {
		// Make sure to turn off Unicode mode (2027)
		_, _ = s.scr.WriteString(ansi.ResetModeUnicodeCore)
	}

	if err := s.scr.Flush(); err != nil {
		return fmt.Errorf("bubbletea: error closing screen writer: %w", err)
	}

	if s.buf.Len() > 0 {
		if s.logger != nil {
			s.logger.Printf("output: %q", s.buf.String())
		}
		if _, err := io.Copy(s.w, &s.buf); err != nil {
			return fmt.Errorf("bubbletea: error writing to screen: %w", err)
		}
		s.buf.Reset()
	}

	x, y := s.scr.Position()

	// We want to clear the renderer state but not the cursor position. This is
	// because we might be putting the tea process in the background, run some
	// other process, and then return to the tea process. We want to keep the
	// cursor position so that we can continue where we left off.
	reset(s)
	s.scr.SetPosition(x, y)

	return nil
}
```

### 🔹 函式: `cursedRenderer.flush()`
- **變更前簽章 (Before)**: `func cursedRenderer.flush(closing bool)` (L258~L578)
- **變更後簽章 (After)**: `func cursedRenderer.flush(closing bool)` (L290~L624)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *cursedRenderer) flush(closing bool) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	view := s.view
	frameArea := uv.Rect(0, 0, s.width, s.height)
	if len(view.Content) == 0 {
		// If the component is nil, we should clear the screen buffer.
		frameArea.Max.Y = 0
	}

	content := uv.NewStyledString(view.Content)
	if !view.AltScreen {
		// We need to resizes the screen based on the frame height and
		// terminal width. This is because the frame height can change based on
		// the content of the frame. For example, if the frame contains a list
		// of items, the height of the frame will be the number of items in the
		// list. This is different from the alt screen buffer, which has a
		// fixed height and width.
		frameHeight := content.Height()
		if frameHeight != frameArea.Dy() {
			frameArea.Max.Y = frameHeight
		}
	}

	// Restore tab stops if we have tab optimizations enabled.
	if s.starting && s.hardTabs {
		_, _ = s.scr.WriteString(ansi.SetTabEvery8Columns)
	}

	if !s.starting && !closing && !s.pendingErase && s.lastView != nil && viewEquals(s.lastView, &view) && frameArea == s.cellbuf.Bounds() {
		// No changes, nothing to do.
		return nil
	}

	// We're no longer starting.
	s.starting = false
	s.pendingErase = false

	if frameArea != s.cellbuf.Bounds() {
		s.scr.Erase() // Force a full redraw to avoid artifacts.

		// We need to reset the touched lines buffer to match the new height.
		s.cellbuf.Touched = nil

		// Resize the screen buffer to match the frame area. This is necessary
		// to ensure that the screen buffer is the same size as the frame area
		// and to avoid rendering issues when the frame area is smaller than
		// the screen buffer.
		s.cellbuf.Resize(frameArea.Dx(), frameArea.Dy())
	}

	// Clear our screen buffer before copying the new frame into it to ensure
	// we erase any old content.
	s.cellbuf.Clear()
	content.Draw(s.cellbuf, s.cellbuf.Bounds())

	// If the frame height is greater than the screen height, we drop the
	// lines from the top of the buffer.
	if frameHeight := frameArea.Dy(); frameHeight > s.height {
		s.cellbuf.Lines = s.cellbuf.Lines[frameHeight-s.height:]
	}

	// Alt screen mode.
	shouldUpdateAltScreen := (s.lastView == nil && view.AltScreen) || (s.lastView != nil && s.lastView.AltScreen != view.AltScreen)
	if shouldUpdateAltScreen {
		// We want to enter/exit altscreen mode but defer writing the actual
		// sequences until we flush the rest of the updates. This is because we
		// control the cursor visibility and we need to ensure that happens
		// after entering/exiting alt screen mode. Some terminals have
		// different cursor visibility states for main and alt screen modes and
		// this ensures we handle that correctly.
		enableAltScreen(s, view.AltScreen, false)
	}

	// bracketed paste mode.
	if s.lastView == nil || view.DisableBracketedPasteMode != s.lastView.DisableBracketedPasteMode {
		if !view.DisableBracketedPasteMode {
			_, _ = s.scr.WriteString(ansi.SetModeBracketedPaste)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeBracketedPaste)
		}
	}

	// report focus events mode.
	if s.lastView == nil || s.lastView.ReportFocus != view.ReportFocus {
		if view.ReportFocus {
			_, _ = s.scr.WriteString(ansi.SetModeFocusEvent)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeFocusEvent)
		}
	}

	// mouse events mode.
	if s.lastView == nil || view.MouseMode != s.lastView.MouseMode {
		switch view.MouseMode {
		case MouseModeNone:
			if s.lastView != nil && s.lastView.MouseMode != MouseModeNone {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent +
					ansi.ResetModeMouseAnyEvent +
					ansi.ResetModeMouseExtSgr)
			}
		case MouseModeCellMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeAllMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseAnyEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseButtonEvent + ansi.SetModeMouseExtSgr)
		case MouseModeAllMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeCellMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseAnyEvent + ansi.SetModeMouseExtSgr)
		}
	}

	// Set window title.
	if s.lastView == nil || view.WindowTitle != s.lastView.WindowTitle {
		if s.lastView != nil || view.WindowTitle != "" {
			_, _ = s.scr.WriteString(ansi.SetWindowTitle(view.WindowTitle))
		}
	}

	// kitty keyboard protocol
	if s.lastView == nil || view.KeyboardEnhancements != s.lastView.KeyboardEnhancements ||
		view.AltScreen != s.lastView.AltScreen {
		// NOTE: We need to reset the keyboard protocol when switching
		// between main and alt screen. This is because the specs specify
		// two different states for the main and alt screen.

		// Enable modifyOtherKeys and Kitty keyboard protocol.
		_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys2)

		kittyFlags := keyboardEnhancementsFlags(view.KeyboardEnhancements)
		_, _ = s.scr.WriteString(ansi.KittyKeyboard(kittyFlags, 1))
		if !closing {
			// Request keyboard enhancements when they change
			_, _ = s.scr.WriteString(ansi.RequestKittyKeyboard)
		}
	}

	// Set terminal colors.
	var (
		cc, lcc  color.Color
		lfg, lbg color.Color
	)
	if view.Cursor != nil {
		cc = view.Cursor.Color
	}
	if s.lastView != nil {
		if s.lastView.Cursor != nil {
			lcc = s.lastView.Cursor.Color
		}
		lfg = s.lastView.ForegroundColor
		lbg = s.lastView.BackgroundColor
	}
	for _, c := range []struct {
		newColor color.Color
		oldColor color.Color
		reset    string
		setter   func(string) string
	}{
		{newColor: cc, oldColor: lcc, reset: ansi.ResetCursorColor, setter: ansi.SetCursorColor},
		{newColor: view.ForegroundColor, oldColor: lfg, reset: ansi.ResetForegroundColor, setter: ansi.SetForegroundColor},
		{newColor: view.BackgroundColor, oldColor: lbg, reset: ansi.ResetBackgroundColor, setter: ansi.SetBackgroundColor},
	} {
		if c.newColor != c.oldColor {
			if c.newColor == nil {
				// Reset the color if it was set to nil.
				_, _ = s.scr.WriteString(c.reset)
			} else {
				// Set the color.
				col, ok := colorful.MakeColor(c.newColor)
				if ok {
					_, _ = s.scr.WriteString(c.setter(col.Hex()))
				}
			}
		}
	}

	// Set cursor shape and blink if set.
	var ccStyle, lcStyle int
	var lcur *Cursor
	ccur := view.Cursor
	if lv := s.lastView; lv != nil {
		lcur = lv.Cursor
	}
	if ccur != nil {
		ccStyle = encodeCursorStyle(ccur.Shape, ccur.Blink)
	}
	if lcur != nil {
		lcStyle = encodeCursorStyle(lcur.Shape, lcur.Blink)
	}
	if ccStyle != lcStyle {
		_, _ = s.scr.WriteString(ansi.SetCursorStyle(ccStyle))
	}

	// Render progress bar if it's changed.
	if (s.lastView == nil && view.ProgressBar != nil && view.ProgressBar.State != ProgressBarNone) ||
		(s.lastView != nil && (s.lastView.ProgressBar == nil) != (view.ProgressBar == nil)) ||
		(s.lastView != nil && s.lastView.ProgressBar != nil && view.ProgressBar != nil && *s.lastView.ProgressBar != *view.ProgressBar) {
		// Render or clear the progress bar if it was added or removed.
		setProgressBar(s, view.ProgressBar)
	}

	// Render and queue changes to the screen buffer.
	s.scr.Render(s.cellbuf.RenderBuffer)

	if cur := view.Cursor; cur != nil {
		// MoveTo must come after [uv.TerminalRenderer.Render] because the
		// cursor position might get updated during rendering.
		s.scr.MoveTo(view.Cursor.X, view.Cursor.Y)
	} else if !view.AltScreen {
		// We don't want the cursor to be dangling at the end of the line in
		// inline mode because it can cause unwanted line wraps in some
		// terminals. So we move it to the beginning of the next line if
		// necessary.
		// This is only needed when the cursor is hidden because when it's
		// visible, we already set its position above.
		x, y := s.scr.Position()
		if x >= s.width-1 {
			s.scr.MoveTo(0, y)
		}
	}

	if err := s.scr.Flush(); err != nil {
		return fmt.Errorf("bubbletea: error flushing screen writer: %w", err)
	}

	// Check if we have any render updates to flush.
	hasUpdates := s.buf.Len() > 0

	// Cursor visibility.
	didShowCursor := s.lastView != nil && s.lastView.Cursor != nil
	showCursor := view.Cursor != nil
	hideCursor := !showCursor
	shouldUpdateCursorVis := (s.lastView == nil || didShowCursor != showCursor) || shouldUpdateAltScreen

	// Build final output buffer with synchronized output or hide/show cursor
	// updates. But first, enter/exit alt screen mode if needed.
	//
	// Here, we have two scenarios:
	// 1. Synchronized output updates are supported. In this case, we want to
	//    wrap all updates, unless it's just a cursor visibility change, in
	//    synchronized output mode. This is because synchronized output mode
	//    takes care of rendering the updates atomically. In the case of
	//    just a cursor visibility change, we don't need to enter
	//    synchronized output mode because it's just a single sequence to
	//    flush out to the terminal.
	//
	// 2. We don't have synchronized output updates support. In this case, and
	//    if the cursor is visible or should be visible, we wrap the updates
	//    with hide/show cursor sequences to try and mitigate cursor
	//    flickering. This is terminal dependent and may still result in
	//    flickering in some terminals. It's the best effort we can do instead
	//    of showing the cursor flying around the screen during updates.

	var buf bytes.Buffer
	if shouldUpdateAltScreen {
		// We always disable keyboard enhancements when switching screens
		// because the terminal is expected to have two different keyboard
		// registries for main and alt screens.
		_, _ = buf.WriteString(ansi.ResetModifyOtherKeys)
		_, _ = buf.WriteString(ansi.KittyKeyboard(0, 1))
		if view.AltScreen {
			// Entering alt screen mode.
			buf.WriteString(ansi.SetModeAltScreenSaveCursor)
		} else {
			// Exiting alt screen mode.
			buf.WriteString(ansi.ResetModeAltScreenSaveCursor)
		}
	}

	if s.syncdUpdates {
		if hasUpdates {
			// We have synchronized output updates enabled.
			buf.WriteString(ansi.SetModeSynchronizedOutput)
		}
		if shouldUpdateCursorVis && hideCursor {
			// Do we need to update the cursor visibility to hidden? If so, do
			// it here before writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
		}
	} else if (shouldUpdateCursorVis && hideCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
	}

	if hasUpdates {
		buf.Write(s.buf.Bytes())
	}

	if s.syncdUpdates {
		if shouldUpdateCursorVis && showCursor {
			// Do we need to update the cursor visibility to visible? If so, do
			// it here after writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
		}
		if hasUpdates {
			// Close synchronized output mode.
			buf.WriteString(ansi.ResetModeSynchronizedOutput)
		}
	} else if (shouldUpdateCursorVis && showCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
	}

	// Reset internal screen renderer buffer.
	s.buf.Reset()

	// If our updates flush buffer has content, write it to the output writer.
	if buf.Len() > 0 {
		if s.logger != nil {
			s.logger.Printf("output: %q", buf.String())
		}
		if _, err := io.Copy(s.w, &buf); err != nil {
			return fmt.Errorf("bubbletea: error flushing update to the writer: %w", err)
		}
	}

	s.lastView = &view

	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *cursedRenderer) flush(closing bool) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	view := s.view
	frameArea := uv.Rect(0, 0, s.width, s.height)
	if len(view.Content) == 0 {
		// If the component is nil, we should clear the screen buffer.
		frameArea.Max.Y = 0
	}

	content := uv.NewStyledString(view.Content)
	if !view.AltScreen {
		// We need to resizes the screen based on the frame height and
		// terminal width. This is because the frame height can change based on
		// the content of the frame. For example, if the frame contains a list
		// of items, the height of the frame will be the number of items in the
		// list. This is different from the alt screen buffer, which has a
		// fixed height and width.
		frameHeight := content.Height()
		if frameHeight != frameArea.Dy() {
			frameArea.Max.Y = frameHeight
		}
	}

	// Restore tab stops if we have tab optimizations enabled.
	if s.starting && s.hardTabs {
		_, _ = s.scr.WriteString(ansi.SetTabEvery8Columns)
	}

	if !s.starting && !closing && !s.pendingErase && s.lastView != nil && viewEquals(s.lastView, &view) && frameArea == s.cellbuf.Bounds() {
		// No changes, nothing to do.
		return nil
	}

	// We're no longer starting.
	s.starting = false
	s.pendingErase = false

	if frameArea != s.cellbuf.Bounds() {
		s.scr.Erase() // Force a full redraw to avoid artifacts.

		// We need to reset the touched lines buffer to match the new height.
		s.cellbuf.Touched = nil

		// Resize the screen buffer to match the frame area. This is necessary
		// to ensure that the screen buffer is the same size as the frame area
		// and to avoid rendering issues when the frame area is smaller than
		// the screen buffer.
		s.cellbuf.Resize(frameArea.Dx(), frameArea.Dy())
	}

	// Clear our screen buffer before copying the new frame into it to ensure
	// we erase any old content.
	s.cellbuf.Clear()
	content.Draw(s.cellbuf, s.cellbuf.Bounds())

	// If the frame height is greater than the screen height, we drop the
	// lines from the top of the buffer.
	if frameHeight := frameArea.Dy(); frameHeight > s.height {
		s.cellbuf.Lines = s.cellbuf.Lines[frameHeight-s.height:]
	}

	// Alt screen mode.
	shouldUpdateAltScreen := (s.lastView == nil && view.AltScreen) || (s.lastView != nil && s.lastView.AltScreen != view.AltScreen)
	if shouldUpdateAltScreen {
		// We want to enter/exit altscreen mode but defer writing the actual
		// sequences until we flush the rest of the updates. This is because we
		// control the cursor visibility and we need to ensure that happens
		// after entering/exiting alt screen mode. Some terminals have
		// different cursor visibility states for main and alt screen modes and
		// this ensures we handle that correctly.
		enableAltScreen(s, view.AltScreen, false)
	}

	// bracketed paste mode.
	if s.lastView == nil || view.DisableBracketedPasteMode != s.lastView.DisableBracketedPasteMode {
		if !view.DisableBracketedPasteMode {
			_, _ = s.scr.WriteString(ansi.SetModeBracketedPaste)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeBracketedPaste)
		}
	}

	// report focus events mode.
	if s.lastView == nil || s.lastView.ReportFocus != view.ReportFocus {
		if view.ReportFocus {
			_, _ = s.scr.WriteString(ansi.SetModeFocusEvent)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeFocusEvent)
		}
	}

	// mouse events mode.
	if s.lastView == nil || view.MouseMode != s.lastView.MouseMode {
		switch view.MouseMode {
		case MouseModeNone:
			if s.lastView != nil && s.lastView.MouseMode != MouseModeNone {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent +
					ansi.ResetModeMouseAnyEvent +
					ansi.ResetModeMouseExtSgr)
			}
		case MouseModeCellMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeAllMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseAnyEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseButtonEvent + ansi.SetModeMouseExtSgr)
		case MouseModeAllMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeCellMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseAnyEvent + ansi.SetModeMouseExtSgr)
		}
	}

	// Set window title.
	if s.lastView == nil || view.WindowTitle != s.lastView.WindowTitle {
		if s.lastView != nil || view.WindowTitle != "" {
			_, _ = s.scr.WriteString(ansi.SetWindowTitle(view.WindowTitle))
		}
	}

	// kitty keyboard protocol. Skipped entirely when input is disabled: the
	// enhancements only affect keyboard input, and querying the terminal
	// would leave its response unconsumed, leaking into the shell after
	// the program exits.
	if !s.noInput && (s.lastView == nil || view.KeyboardEnhancements != s.lastView.KeyboardEnhancements ||
		view.AltScreen != s.lastView.AltScreen) {
		// NOTE: We need to reset the keyboard protocol when switching
		// between main and alt screen. This is because the specs specify
		// two different states for the main and alt screen.

		// Enable modifyOtherKeys and Kitty keyboard protocol.
		_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys2)

		kittyFlags := keyboardEnhancementsFlags(view.KeyboardEnhancements)
		if s.lastView == nil || view.AltScreen != s.lastView.AltScreen {
			// First render or screen switch: the previous screen's entry
			// (if any) is popped below, so push a fresh one for this
			// screen.
			_, _ = s.scr.WriteString(ansi.PushKittyKeyboard(kittyFlags))
		} else {
			// Only the flags changed while the same screen stays active.
			// Update the topmost stack entry in place instead of popping
			// and re-pushing, so a keyboard change doesn't churn the
			// stack. Note that this overwrites whatever entry is currently
			// on top, which is normally ours.
			_, _ = s.scr.WriteString(ansi.KittyKeyboard(kittyFlags, 1))
		}
		if !closing {
			// Request keyboard enhancements when they change
			_, _ = s.scr.WriteString(ansi.RequestKittyKeyboard)
		}
	}

	// Set terminal colors.
	var (
		cc, lcc  color.Color
		lfg, lbg color.Color
	)
	if view.Cursor != nil {
		cc = view.Cursor.Color
	}
	if s.lastView != nil {
		if s.lastView.Cursor != nil {
			lcc = s.lastView.Cursor.Color
		}
		lfg = s.lastView.ForegroundColor
		lbg = s.lastView.BackgroundColor
	}
	for _, c := range []struct {
		newColor color.Color
		oldColor color.Color
		reset    string
		setter   func(string) string
	}{
		{newColor: cc, oldColor: lcc, reset: ansi.ResetCursorColor, setter: ansi.SetCursorColor},
		{newColor: view.ForegroundColor, oldColor: lfg, reset: ansi.ResetForegroundColor, setter: ansi.SetForegroundColor},
		{newColor: view.BackgroundColor, oldColor: lbg, reset: ansi.ResetBackgroundColor, setter: ansi.SetBackgroundColor},
	} {
		if c.newColor != c.oldColor {
			if c.newColor == nil {
				// Reset the color if it was set to nil.
				_, _ = s.scr.WriteString(c.reset)
			} else {
				// Set the color.
				col, ok := colorful.MakeColor(c.newColor)
				if ok {
					_, _ = s.scr.WriteString(c.setter(col.Hex()))
				}
			}
		}
	}

	// Set cursor shape and blink if set.
	var ccStyle, lcStyle int
	var lcur *Cursor
	ccur := view.Cursor
	if lv := s.lastView; lv != nil {
		lcur = lv.Cursor
	}
	if ccur != nil {
		ccStyle = encodeCursorStyle(ccur.Shape, ccur.Blink)
	}
	if lcur != nil {
		lcStyle = encodeCursorStyle(lcur.Shape, lcur.Blink)
	}
	if ccStyle != lcStyle {
		_, _ = s.scr.WriteString(ansi.SetCursorStyle(ccStyle))
	}

	// Render progress bar if it's changed.
	if (s.lastView == nil && view.ProgressBar != nil && view.ProgressBar.State != ProgressBarNone) ||
		(s.lastView != nil && (s.lastView.ProgressBar == nil) != (view.ProgressBar == nil)) ||
		(s.lastView != nil && s.lastView.ProgressBar != nil && view.ProgressBar != nil && *s.lastView.ProgressBar != *view.ProgressBar) {
		// Render or clear the progress bar if it was added or removed.
		setProgressBar(s, view.ProgressBar)
	}

	// Render and queue changes to the screen buffer.
	s.scr.Render(s.cellbuf.RenderBuffer)

	if cur := view.Cursor; cur != nil {
		// MoveTo must come after [uv.TerminalRenderer.Render] because the
		// cursor position might get updated during rendering.
		s.scr.MoveTo(view.Cursor.X, view.Cursor.Y)
	} else if !view.AltScreen {
		// We don't want the cursor to be dangling at the end of the line in
		// inline mode because it can cause unwanted line wraps in some
		// terminals. So we move it to the beginning of the next line if
		// necessary.
		// This is only needed when the cursor is hidden because when it's
		// visible, we already set its position above.
		x, y := s.scr.Position()
		if x >= s.width-1 {
			s.scr.MoveTo(0, y)
		}
	}

	if err := s.scr.Flush(); err != nil {
		return fmt.Errorf("bubbletea: error flushing screen writer: %w", err)
	}

	// Check if we have any render updates to flush.
	hasUpdates := s.buf.Len() > 0

	// Cursor visibility.
	didShowCursor := s.lastView != nil && s.lastView.Cursor != nil
	showCursor := view.Cursor != nil
	hideCursor := !showCursor
	shouldUpdateCursorVis := (s.lastView == nil || didShowCursor != showCursor) || shouldUpdateAltScreen

	// Build final output buffer with synchronized output or hide/show cursor
	// updates. But first, enter/exit alt screen mode if needed.
	//
	// Here, we have two scenarios:
	// 1. Synchronized output updates are supported. In this case, we want to
	//    wrap all updates, unless it's just a cursor visibility change, in
	//    synchronized output mode. This is because synchronized output mode
	//    takes care of rendering the updates atomically. In the case of
	//    just a cursor visibility change, we don't need to enter
	//    synchronized output mode because it's just a single sequence to
	//    flush out to the terminal.
	//
	// 2. We don't have synchronized output updates support. In this case, and
	//    if the cursor is visible or should be visible, we wrap the updates
	//    with hide/show cursor sequences to try and mitigate cursor
	//    flickering. This is terminal dependent and may still result in
	//    flickering in some terminals. It's the best effort we can do instead
	//    of showing the cursor flying around the screen during updates.

	var buf bytes.Buffer
	if shouldUpdateAltScreen {
		// We always reset keyboard enhancements when switching screens
		// because the terminal is expected to have two different keyboard
		// registries for main and alt screens.
		s.resetKeyboardEnhancements(&buf)
		if view.AltScreen {
			// Entering alt screen mode.
			buf.WriteString(ansi.SetModeAltScreenSaveCursor)
		} else {
			// Exiting alt screen mode.
			buf.WriteString(ansi.ResetModeAltScreenSaveCursor)
		}
	}

	if s.syncdUpdates {
		if hasUpdates {
			// We have synchronized output updates enabled.
			buf.WriteString(ansi.SetModeSynchronizedOutput)
		}
		if shouldUpdateCursorVis && hideCursor {
			// Do we need to update the cursor visibility to hidden? If so, do
			// it here before writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
		}
	} else if (shouldUpdateCursorVis && hideCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
	}

	if hasUpdates {
		buf.Write(s.buf.Bytes())
	}

	if s.syncdUpdates {
		if shouldUpdateCursorVis && showCursor {
			// Do we need to update the cursor visibility to visible? If so, do
			// it here after writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
		}
		if hasUpdates {
			// Close synchronized output mode.
			buf.WriteString(ansi.ResetModeSynchronizedOutput)
		}
	} else if (shouldUpdateCursorVis && showCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
	}

	// Reset internal screen renderer buffer.
	s.buf.Reset()

	// If our updates flush buffer has content, write it to the output writer.
	if buf.Len() > 0 {
		if s.logger != nil {
			s.logger.Printf("output: %q", buf.String())
		}
		if _, err := io.Copy(s.w, &buf); err != nil {
			return fmt.Errorf("bubbletea: error flushing update to the writer: %w", err)
		}
	}

	s.lastView = &view

	return nil
}
```

### 🔹 函式: `cursedRenderer.start()`
- **變更前簽章 (Before)**: `func cursedRenderer.start()` (L76~L141)
- **變更後簽章 (After)**: `func cursedRenderer.start()` (L100~L169)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *cursedRenderer) start() {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Mark that we're starting. This is used to restore some state when
	// starting the renderer again after it was stopped.
	s.starting = true

	if s.lastView == nil {
		return
	}

	if s.lastView.AltScreen {
		enableAltScreen(s, true, true)
	}
	enableTextCursor(s, s.lastView.Cursor != nil)
	if s.lastView.Cursor != nil {
		if s.lastView.Cursor.Color != nil {
			col, ok := colorful.MakeColor(s.lastView.Cursor.Color)
			if ok {
				_, _ = s.scr.WriteString(ansi.SetCursorColor(col.Hex()))
			}
		}
		curStyle := encodeCursorStyle(s.lastView.Cursor.Shape, s.lastView.Cursor.Blink)
		if curStyle != 0 && curStyle != 1 {
			_, _ = s.scr.WriteString(ansi.SetCursorStyle(curStyle))
		}
	}
	if s.lastView.ForegroundColor != nil {
		col, ok := colorful.MakeColor(s.lastView.ForegroundColor)
		if ok {
			_, _ = s.scr.WriteString(ansi.SetForegroundColor(col.Hex()))
		}
	}
	if s.lastView.BackgroundColor != nil {
		col, ok := colorful.MakeColor(s.lastView.BackgroundColor)
		if ok {
			_, _ = s.scr.WriteString(ansi.SetBackgroundColor(col.Hex()))
		}
	}
	if !s.lastView.DisableBracketedPasteMode {
		_, _ = s.scr.WriteString(ansi.SetModeBracketedPaste)
	}
	if s.lastView.ReportFocus {
		_, _ = s.scr.WriteString(ansi.SetModeFocusEvent)
	}
	switch s.lastView.MouseMode {
	case MouseModeNone:
	case MouseModeCellMotion:
		_, _ = s.scr.WriteString(ansi.SetModeMouseButtonEvent + ansi.SetModeMouseExtSgr)
	case MouseModeAllMotion:
		_, _ = s.scr.WriteString(ansi.SetModeMouseAnyEvent + ansi.SetModeMouseExtSgr)
	}
	if s.lastView.WindowTitle != "" {
		_, _ = s.scr.WriteString(ansi.SetWindowTitle(s.lastView.WindowTitle))
	}
	if s.lastView.ProgressBar != nil {
		setProgressBar(s, s.lastView.ProgressBar)
	}
	// Enable modifyOtherKeys and Kitty keyboard protocol.
	// Both can coexist; terminals ignore what they don't support.
	_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys2)

	kittyFlags := keyboardEnhancementsFlags(s.lastView.KeyboardEnhancements)
	_, _ = s.scr.WriteString(ansi.KittyKeyboard(kittyFlags, 1))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *cursedRenderer) start() {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Mark that we're starting. This is used to restore some state when
	// starting the renderer again after it was stopped.
	s.starting = true

	if s.lastView == nil {
		return
	}

	if s.lastView.AltScreen {
		enableAltScreen(s, true, true)
	}
	enableTextCursor(s, s.lastView.Cursor != nil)
	if s.lastView.Cursor != nil {
		if s.lastView.Cursor.Color != nil {
			col, ok := colorful.MakeColor(s.lastView.Cursor.Color)
			if ok {
				_, _ = s.scr.WriteString(ansi.SetCursorColor(col.Hex()))
			}
		}
		curStyle := encodeCursorStyle(s.lastView.Cursor.Shape, s.lastView.Cursor.Blink)
		if curStyle != 0 && curStyle != 1 {
			_, _ = s.scr.WriteString(ansi.SetCursorStyle(curStyle))
		}
	}
	if s.lastView.ForegroundColor != nil {
		col, ok := colorful.MakeColor(s.lastView.ForegroundColor)
		if ok {
			_, _ = s.scr.WriteString(ansi.SetForegroundColor(col.Hex()))
		}
	}
	if s.lastView.BackgroundColor != nil {
		col, ok := colorful.MakeColor(s.lastView.BackgroundColor)
		if ok {
			_, _ = s.scr.WriteString(ansi.SetBackgroundColor(col.Hex()))
		}
	}
	if !s.lastView.DisableBracketedPasteMode {
		_, _ = s.scr.WriteString(ansi.SetModeBracketedPaste)
	}
	if s.lastView.ReportFocus {
		_, _ = s.scr.WriteString(ansi.SetModeFocusEvent)
	}
	switch s.lastView.MouseMode {
	case MouseModeNone:
	case MouseModeCellMotion:
		_, _ = s.scr.WriteString(ansi.SetModeMouseButtonEvent + ansi.SetModeMouseExtSgr)
	case MouseModeAllMotion:
		_, _ = s.scr.WriteString(ansi.SetModeMouseAnyEvent + ansi.SetModeMouseExtSgr)
	}
	if s.lastView.WindowTitle != "" {
		_, _ = s.scr.WriteString(ansi.SetWindowTitle(s.lastView.WindowTitle))
	}
	if s.lastView.ProgressBar != nil {
		setProgressBar(s, s.lastView.ProgressBar)
	}
	if !s.noInput {
		// Enable modifyOtherKeys and Kitty keyboard protocol.
		// Both can coexist; terminals ignore what they don't support.
		_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys2)

		kittyFlags := keyboardEnhancementsFlags(s.lastView.KeyboardEnhancements)
		// The entry was popped when the renderer was stopped, so push a fresh
		// one for the screen we're about to restore.
		_, _ = s.scr.WriteString(ansi.PushKittyKeyboard(kittyFlags))
	}
}
```


#### 📄 檔案: `tea.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:156, E:206, A:0) ➔ After(N:157, E:207, A:0)
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
  • + [新增節點] `r.setNoInput (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Program.Run` ──[CALLS]──> `r.setNoInput (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Program.Run()`
- **變更前簽章 (Before)**: `func Program.Run()` (L999~L1182)
- **變更後簽章 (After)**: `func Program.Run()` (L999~L1183)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Program) Run() (returnModel Model, returnErr error) {
	if p.initialModel == nil {
		return nil, errors.New("bubbletea: InitialModel cannot be nil")
	}

	// Initialize context and teardown channel.
	p.handlers = channelHandlers{}
	cmds := make(chan Cmd)

	p.finished = make(chan struct{})
	defer func() {
		close(p.finished)
	}()

	defer p.cancel()

	if p.disableInput {
		p.input = nil
	} else if p.input == nil {
		p.input = os.Stdin
		if !term.IsTerminal(os.Stdin.Fd()) {
			ttyIn, _, err := OpenTTY()
			if err != nil {
				return p.initialModel, fmt.Errorf("bubbletea: error opening TTY: %w", err)
			}
			p.input = ttyIn
		}
	}

	// Handle signals.
	if !p.disableSignalHandler {
		p.handlers.add(p.handleSignals())
	}

	// Recover from panics.
	if !p.disableCatchPanics {
		defer func() {
			if r := recover(); r != nil {
				returnErr = fmt.Errorf("%w: %w", ErrProgramKilled, ErrProgramPanic)
				p.recoverFromPanic(r)
			}
		}()
	}

	// Check if output is a TTY before entering raw mode, hiding the cursor and
	// so on.
	if err := p.initTerminal(); err != nil {
		return p.initialModel, err
	}

	// Get the initial window size.
	width, height := p.width, p.height
	if p.ttyOutput != nil {
		// Set the initial size of the terminal.
		w, h, err := term.GetSize(p.ttyOutput.Fd())
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error getting terminal size: %w", err)
		}

		width, height = w, h
	}

	p.width, p.height = width, height
	resizeMsg := WindowSizeMsg{Width: p.width, Height: p.height}

	if p.renderer == nil {
		if p.disableRenderer {
			p.renderer = &nilRenderer{}
		} else {
			// If no renderer is set use the cursed one.
			r := newCursedRenderer(
				p.output,
				p.environ,
				p.width,
				p.height,
			)
			r.setLogger(p.logger)
			// XXX: This breaks many things especially when we want the output
			// to be compatible with terminals that are not necessary a TTY.
			// This was originally done to work around a Wish emulated-pty
			// issue where when a PTY session is detected, and we don't
			// allocate a real PTY, the terminal settings (Termios and WinCon)
			// don't change and the we end up working in cooked mode instead of
			// raw mode. See issue #1572.
			mapNl := runtime.GOOS != "windows" && p.ttyInput == nil
			r.setOptimizations(p.useHardTabs, p.useBackspace, mapNl)
			p.renderer = r
		}
	}

	// Get the color profile and send it to the program.
	if p.profile == nil {
		cp := colorprofile.Detect(p.output, p.environ)
		p.profile = &cp
	}

	// Set the color profile on the renderer and send it to the program.
	p.renderer.setColorProfile(*p.profile)
	go p.Send(ColorProfileMsg{*p.profile})

	// Send the initial size to the program.
	go p.Send(resizeMsg)
	p.renderer.resize(resizeMsg.Width, resizeMsg.Height)

	// Send the environment variables used by the program.
	go p.Send(EnvMsg(p.environ))

	// Init the input reader and initial model.
	model := p.initialModel
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return model, err
		}
	}

	// Start the renderer.
	p.startRenderer()

	if !p.disableRenderer && shouldQuerySynchronizedOutput(p.environ) {
		// Query for synchronized updates support (mode 2026) and unicode core
		// (mode 2027). If the terminal supports it, the renderer will enable
		// it once we get the response.
		p.execute(ansi.RequestModeSynchronizedOutput +
			ansi.RequestModeUnicodeCore)
	}

	// Initialize the program.
	initCmd := model.Init()
	if initCmd != nil {
		ch := make(chan struct{})
		p.handlers.add(ch)

		go func() {
			defer close(ch)

			select {
			case cmds <- initCmd:
			case <-p.ctx.Done():
			}
		}()
	}

	// Render the initial view.
	p.render(model)

	// Handle resize events.
	p.handlers.add(p.handleResize())

	// Process commands.
	p.handlers.add(p.handleCommands(cmds))

	// Run event loop, handle updates and draw.
	var err error
	model, err = p.eventLoop(model, cmds)

	if err == nil && len(p.errs) > 0 {
		err = <-p.errs // Drain a leftover error in case eventLoop crashed.
	}

	killed := p.externalCtx.Err() != nil || p.ctx.Err() != nil || err != nil
	if killed {
		if err == nil && p.externalCtx.Err() != nil {
			// Return also as context error the cancellation of an external context.
			// This is the context the user knows about and should be able to act on.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, p.externalCtx.Err())
		} else if err == nil && p.ctx.Err() != nil {
			// Return only that the program was killed (not the internal mechanism).
			// The user does not know or need to care about the internal program context.
			err = ErrProgramKilled
		} else {
			// Return that the program was killed and also the error that caused it.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, err)
		}
	} else {
		// Graceful shutdown of the program (not killed):
		// Ensure we rendered the final state of the model.
		p.render(model)
	}

	// Restore terminal state.
	p.shutdown(killed)

	return model, err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Program) Run() (returnModel Model, returnErr error) {
	if p.initialModel == nil {
		return nil, errors.New("bubbletea: InitialModel cannot be nil")
	}

	// Initialize context and teardown channel.
	p.handlers = channelHandlers{}
	cmds := make(chan Cmd)

	p.finished = make(chan struct{})
	defer func() {
		close(p.finished)
	}()

	defer p.cancel()

	if p.disableInput {
		p.input = nil
	} else if p.input == nil {
		p.input = os.Stdin
		if !term.IsTerminal(os.Stdin.Fd()) {
			ttyIn, _, err := OpenTTY()
			if err != nil {
				return p.initialModel, fmt.Errorf("bubbletea: error opening TTY: %w", err)
			}
			p.input = ttyIn
		}
	}

	// Handle signals.
	if !p.disableSignalHandler {
		p.handlers.add(p.handleSignals())
	}

	// Recover from panics.
	if !p.disableCatchPanics {
		defer func() {
			if r := recover(); r != nil {
				returnErr = fmt.Errorf("%w: %w", ErrProgramKilled, ErrProgramPanic)
				p.recoverFromPanic(r)
			}
		}()
	}

	// Check if output is a TTY before entering raw mode, hiding the cursor and
	// so on.
	if err := p.initTerminal(); err != nil {
		return p.initialModel, err
	}

	// Get the initial window size.
	width, height := p.width, p.height
	if p.ttyOutput != nil {
		// Set the initial size of the terminal.
		w, h, err := term.GetSize(p.ttyOutput.Fd())
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error getting terminal size: %w", err)
		}

		width, height = w, h
	}

	p.width, p.height = width, height
	resizeMsg := WindowSizeMsg{Width: p.width, Height: p.height}

	if p.renderer == nil {
		if p.disableRenderer {
			p.renderer = &nilRenderer{}
		} else {
			// If no renderer is set use the cursed one.
			r := newCursedRenderer(
				p.output,
				p.environ,
				p.width,
				p.height,
			)
			r.setLogger(p.logger)
			r.setNoInput(p.disableInput)
			// XXX: This breaks many things especially when we want the output
			// to be compatible with terminals that are not necessary a TTY.
			// This was originally done to work around a Wish emulated-pty
			// issue where when a PTY session is detected, and we don't
			// allocate a real PTY, the terminal settings (Termios and WinCon)
			// don't change and the we end up working in cooked mode instead of
			// raw mode. See issue #1572.
			mapNl := runtime.GOOS != "windows" && p.ttyInput == nil
			r.setOptimizations(p.useHardTabs, p.useBackspace, mapNl)
			p.renderer = r
		}
	}

	// Get the color profile and send it to the program.
	if p.profile == nil {
		cp := colorprofile.Detect(p.output, p.environ)
		p.profile = &cp
	}

	// Set the color profile on the renderer and send it to the program.
	p.renderer.setColorProfile(*p.profile)
	go p.Send(ColorProfileMsg{*p.profile})

	// Send the initial size to the program.
	go p.Send(resizeMsg)
	p.renderer.resize(resizeMsg.Width, resizeMsg.Height)

	// Send the environment variables used by the program.
	go p.Send(EnvMsg(p.environ))

	// Init the input reader and initial model.
	model := p.initialModel
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return model, err
		}
	}

	// Start the renderer.
	p.startRenderer()

	if !p.disableRenderer && shouldQuerySynchronizedOutput(p.environ) {
		// Query for synchronized updates support (mode 2026) and unicode core
		// (mode 2027). If the terminal supports it, the renderer will enable
		// it once we get the response.
		p.execute(ansi.RequestModeSynchronizedOutput +
			ansi.RequestModeUnicodeCore)
	}

	// Initialize the program.
	initCmd := model.Init()
	if initCmd != nil {
		ch := make(chan struct{})
		p.handlers.add(ch)

		go func() {
			defer close(ch)

			select {
			case cmds <- initCmd:
			case <-p.ctx.Done():
			}
		}()
	}

	// Render the initial view.
	p.render(model)

	// Handle resize events.
	p.handlers.add(p.handleResize())

	// Process commands.
	p.handlers.add(p.handleCommands(cmds))

	// Run event loop, handle updates and draw.
	var err error
	model, err = p.eventLoop(model, cmds)

	if err == nil && len(p.errs) > 0 {
		err = <-p.errs // Drain a leftover error in case eventLoop crashed.
	}

	killed := p.externalCtx.Err() != nil || p.ctx.Err() != nil || err != nil
	if killed {
		if err == nil && p.externalCtx.Err() != nil {
			// Return also as context error the cancellation of an external context.
			// This is the context the user knows about and should be able to act on.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, p.externalCtx.Err())
		} else if err == nil && p.ctx.Err() != nil {
			// Return only that the program was killed (not the internal mechanism).
			// The user does not know or need to care about the internal program context.
			err = ErrProgramKilled
		} else {
			// Return that the program was killed and also the error that caused it.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, err)
		}
	} else {
		// Graceful shutdown of the program (not killed):
		// Ensure we rendered the final state of the model.
		p.render(model)
	}

	// Restore terminal state.
	p.shutdown(killed)

	return model, err
}
```


---

### 🔹 Commit #04: `930e18c9`
- **完整 Hash**: `930e18c9668417db1908c7a694ee49676116b46e`
- **說明 (Ground Truth)**: fix: don't panic in ProgressBarState.String() for out-of-range values (#1748)
- **變更檔案數**: 1

#### 📄 檔案: `tea.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:156, E:206, A:0) ➔ After(N:156, E:206, A:0)
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

### 🔹 函式: `ProgressBarState.String()`
- **變更前簽章 (Before)**: `func ProgressBarState.String()` (L321~L329)
- **變更後簽章 (After)**: `func ProgressBarState.String()` (L322~L337)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s ProgressBarState) String() string {
	return [...]string{
		"None",
		"Default",
		"Error",
		"Indeterminate",
		"Warning",
	}[s]
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s ProgressBarState) String() string {
	switch s {
	case ProgressBarNone:
		return "None"
	case ProgressBarDefault:
		return "Default"
	case ProgressBarError:
		return "Error"
	case ProgressBarIndeterminate:
		return "Indeterminate"
	case ProgressBarWarning:
		return "Warning"
	default:
		return "Unknown"
	}
}
```


---

### 🔹 Commit #05: `faf4dcf5`
- **完整 Hash**: `faf4dcf54a92bab2fe3bf6f4715adf44f2fc245d`
- **說明 (Ground Truth)**: fix: pendingErase in cursedRenderer (#1755)
- **變更檔案數**: 1

#### 📄 檔案: `cursed_renderer.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:108, E:161, A:0) ➔ After(N:108, E:161, A:0)
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

### 🔹 函式: `cursedRenderer.clearScreen()`
- **變更前簽章 (Before)**: `func cursedRenderer.clearScreen()` (L634~L641)
- **變更後簽章 (After)**: `func cursedRenderer.clearScreen()` (L637~L645)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *cursedRenderer) clearScreen() {
	s.mu.Lock()
	// Move the cursor to the top left corner of the screen and trigger a full
	// screen redraw.
	s.scr.MoveTo(0, 0)
	s.scr.Erase()
	s.mu.Unlock()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *cursedRenderer) clearScreen() {
	s.mu.Lock()
	// Move the cursor to the top left corner of the screen and trigger a full
	// screen redraw.
	s.scr.MoveTo(0, 0)
	s.scr.Erase()
	s.pendingErase = true
	s.mu.Unlock()
}
```

### 🔹 函式: `cursedRenderer.flush()`
- **變更前簽章 (Before)**: `func cursedRenderer.flush(closing bool)` (L257~L576)
- **變更後簽章 (After)**: `func cursedRenderer.flush(closing bool)` (L258~L578)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *cursedRenderer) flush(closing bool) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	view := s.view
	frameArea := uv.Rect(0, 0, s.width, s.height)
	if len(view.Content) == 0 {
		// If the component is nil, we should clear the screen buffer.
		frameArea.Max.Y = 0
	}

	content := uv.NewStyledString(view.Content)
	if !view.AltScreen {
		// We need to resizes the screen based on the frame height and
		// terminal width. This is because the frame height can change based on
		// the content of the frame. For example, if the frame contains a list
		// of items, the height of the frame will be the number of items in the
		// list. This is different from the alt screen buffer, which has a
		// fixed height and width.
		frameHeight := content.Height()
		if frameHeight != frameArea.Dy() {
			frameArea.Max.Y = frameHeight
		}
	}

	// Restore tab stops if we have tab optimizations enabled.
	if s.starting && s.hardTabs {
		_, _ = s.scr.WriteString(ansi.SetTabEvery8Columns)
	}

	if !s.starting && !closing && s.lastView != nil && viewEquals(s.lastView, &view) && frameArea == s.cellbuf.Bounds() {
		// No changes, nothing to do.
		return nil
	}

	// We're no longer starting.
	s.starting = false

	if frameArea != s.cellbuf.Bounds() {
		s.scr.Erase() // Force a full redraw to avoid artifacts.

		// We need to reset the touched lines buffer to match the new height.
		s.cellbuf.Touched = nil

		// Resize the screen buffer to match the frame area. This is necessary
		// to ensure that the screen buffer is the same size as the frame area
		// and to avoid rendering issues when the frame area is smaller than
		// the screen buffer.
		s.cellbuf.Resize(frameArea.Dx(), frameArea.Dy())
	}

	// Clear our screen buffer before copying the new frame into it to ensure
	// we erase any old content.
	s.cellbuf.Clear()
	content.Draw(s.cellbuf, s.cellbuf.Bounds())

	// If the frame height is greater than the screen height, we drop the
	// lines from the top of the buffer.
	if frameHeight := frameArea.Dy(); frameHeight > s.height {
		s.cellbuf.Lines = s.cellbuf.Lines[frameHeight-s.height:]
	}

	// Alt screen mode.
	shouldUpdateAltScreen := (s.lastView == nil && view.AltScreen) || (s.lastView != nil && s.lastView.AltScreen != view.AltScreen)
	if shouldUpdateAltScreen {
		// We want to enter/exit altscreen mode but defer writing the actual
		// sequences until we flush the rest of the updates. This is because we
		// control the cursor visibility and we need to ensure that happens
		// after entering/exiting alt screen mode. Some terminals have
		// different cursor visibility states for main and alt screen modes and
		// this ensures we handle that correctly.
		enableAltScreen(s, view.AltScreen, false)
	}

	// bracketed paste mode.
	if s.lastView == nil || view.DisableBracketedPasteMode != s.lastView.DisableBracketedPasteMode {
		if !view.DisableBracketedPasteMode {
			_, _ = s.scr.WriteString(ansi.SetModeBracketedPaste)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeBracketedPaste)
		}
	}

	// report focus events mode.
	if s.lastView == nil || s.lastView.ReportFocus != view.ReportFocus {
		if view.ReportFocus {
			_, _ = s.scr.WriteString(ansi.SetModeFocusEvent)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeFocusEvent)
		}
	}

	// mouse events mode.
	if s.lastView == nil || view.MouseMode != s.lastView.MouseMode {
		switch view.MouseMode {
		case MouseModeNone:
			if s.lastView != nil && s.lastView.MouseMode != MouseModeNone {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent +
					ansi.ResetModeMouseAnyEvent +
					ansi.ResetModeMouseExtSgr)
			}
		case MouseModeCellMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeAllMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseAnyEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseButtonEvent + ansi.SetModeMouseExtSgr)
		case MouseModeAllMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeCellMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseAnyEvent + ansi.SetModeMouseExtSgr)
		}
	}

	// Set window title.
	if s.lastView == nil || view.WindowTitle != s.lastView.WindowTitle {
		if s.lastView != nil || view.WindowTitle != "" {
			_, _ = s.scr.WriteString(ansi.SetWindowTitle(view.WindowTitle))
		}
	}

	// kitty keyboard protocol
	if s.lastView == nil || view.KeyboardEnhancements != s.lastView.KeyboardEnhancements ||
		view.AltScreen != s.lastView.AltScreen {
		// NOTE: We need to reset the keyboard protocol when switching
		// between main and alt screen. This is because the specs specify
		// two different states for the main and alt screen.

		// Enable modifyOtherKeys and Kitty keyboard protocol.
		_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys2)

		kittyFlags := keyboardEnhancementsFlags(view.KeyboardEnhancements)
		_, _ = s.scr.WriteString(ansi.KittyKeyboard(kittyFlags, 1))
		if !closing {
			// Request keyboard enhancements when they change
			_, _ = s.scr.WriteString(ansi.RequestKittyKeyboard)
		}
	}

	// Set terminal colors.
	var (
		cc, lcc  color.Color
		lfg, lbg color.Color
	)
	if view.Cursor != nil {
		cc = view.Cursor.Color
	}
	if s.lastView != nil {
		if s.lastView.Cursor != nil {
			lcc = s.lastView.Cursor.Color
		}
		lfg = s.lastView.ForegroundColor
		lbg = s.lastView.BackgroundColor
	}
	for _, c := range []struct {
		newColor color.Color
		oldColor color.Color
		reset    string
		setter   func(string) string
	}{
		{newColor: cc, oldColor: lcc, reset: ansi.ResetCursorColor, setter: ansi.SetCursorColor},
		{newColor: view.ForegroundColor, oldColor: lfg, reset: ansi.ResetForegroundColor, setter: ansi.SetForegroundColor},
		{newColor: view.BackgroundColor, oldColor: lbg, reset: ansi.ResetBackgroundColor, setter: ansi.SetBackgroundColor},
	} {
		if c.newColor != c.oldColor {
			if c.newColor == nil {
				// Reset the color if it was set to nil.
				_, _ = s.scr.WriteString(c.reset)
			} else {
				// Set the color.
				col, ok := colorful.MakeColor(c.newColor)
				if ok {
					_, _ = s.scr.WriteString(c.setter(col.Hex()))
				}
			}
		}
	}

	// Set cursor shape and blink if set.
	var ccStyle, lcStyle int
	var lcur *Cursor
	ccur := view.Cursor
	if lv := s.lastView; lv != nil {
		lcur = lv.Cursor
	}
	if ccur != nil {
		ccStyle = encodeCursorStyle(ccur.Shape, ccur.Blink)
	}
	if lcur != nil {
		lcStyle = encodeCursorStyle(lcur.Shape, lcur.Blink)
	}
	if ccStyle != lcStyle {
		_, _ = s.scr.WriteString(ansi.SetCursorStyle(ccStyle))
	}

	// Render progress bar if it's changed.
	if (s.lastView == nil && view.ProgressBar != nil && view.ProgressBar.State != ProgressBarNone) ||
		(s.lastView != nil && (s.lastView.ProgressBar == nil) != (view.ProgressBar == nil)) ||
		(s.lastView != nil && s.lastView.ProgressBar != nil && view.ProgressBar != nil && *s.lastView.ProgressBar != *view.ProgressBar) {
		// Render or clear the progress bar if it was added or removed.
		setProgressBar(s, view.ProgressBar)
	}

	// Render and queue changes to the screen buffer.
	s.scr.Render(s.cellbuf.RenderBuffer)

	if cur := view.Cursor; cur != nil {
		// MoveTo must come after [uv.TerminalRenderer.Render] because the
		// cursor position might get updated during rendering.
		s.scr.MoveTo(view.Cursor.X, view.Cursor.Y)
	} else if !view.AltScreen {
		// We don't want the cursor to be dangling at the end of the line in
		// inline mode because it can cause unwanted line wraps in some
		// terminals. So we move it to the beginning of the next line if
		// necessary.
		// This is only needed when the cursor is hidden because when it's
		// visible, we already set its position above.
		x, y := s.scr.Position()
		if x >= s.width-1 {
			s.scr.MoveTo(0, y)
		}
	}

	if err := s.scr.Flush(); err != nil {
		return fmt.Errorf("bubbletea: error flushing screen writer: %w", err)
	}

	// Check if we have any render updates to flush.
	hasUpdates := s.buf.Len() > 0

	// Cursor visibility.
	didShowCursor := s.lastView != nil && s.lastView.Cursor != nil
	showCursor := view.Cursor != nil
	hideCursor := !showCursor
	shouldUpdateCursorVis := (s.lastView == nil || didShowCursor != showCursor) || shouldUpdateAltScreen

	// Build final output buffer with synchronized output or hide/show cursor
	// updates. But first, enter/exit alt screen mode if needed.
	//
	// Here, we have two scenarios:
	// 1. Synchronized output updates are supported. In this case, we want to
	//    wrap all updates, unless it's just a cursor visibility change, in
	//    synchronized output mode. This is because synchronized output mode
	//    takes care of rendering the updates atomically. In the case of
	//    just a cursor visibility change, we don't need to enter
	//    synchronized output mode because it's just a single sequence to
	//    flush out to the terminal.
	//
	// 2. We don't have synchronized output updates support. In this case, and
	//    if the cursor is visible or should be visible, we wrap the updates
	//    with hide/show cursor sequences to try and mitigate cursor
	//    flickering. This is terminal dependent and may still result in
	//    flickering in some terminals. It's the best effort we can do instead
	//    of showing the cursor flying around the screen during updates.

	var buf bytes.Buffer
	if shouldUpdateAltScreen {
		// We always disable keyboard enhancements when switching screens
		// because the terminal is expected to have two different keyboard
		// registries for main and alt screens.
		_, _ = buf.WriteString(ansi.ResetModifyOtherKeys)
		_, _ = buf.WriteString(ansi.KittyKeyboard(0, 1))
		if view.AltScreen {
			// Entering alt screen mode.
			buf.WriteString(ansi.SetModeAltScreenSaveCursor)
		} else {
			// Exiting alt screen mode.
			buf.WriteString(ansi.ResetModeAltScreenSaveCursor)
		}
	}

	if s.syncdUpdates {
		if hasUpdates {
			// We have synchronized output updates enabled.
			buf.WriteString(ansi.SetModeSynchronizedOutput)
		}
		if shouldUpdateCursorVis && hideCursor {
			// Do we need to update the cursor visibility to hidden? If so, do
			// it here before writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
		}
	} else if (shouldUpdateCursorVis && hideCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
	}

	if hasUpdates {
		buf.Write(s.buf.Bytes())
	}

	if s.syncdUpdates {
		if shouldUpdateCursorVis && showCursor {
			// Do we need to update the cursor visibility to visible? If so, do
			// it here after writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
		}
		if hasUpdates {
			// Close synchronized output mode.
			buf.WriteString(ansi.ResetModeSynchronizedOutput)
		}
	} else if (shouldUpdateCursorVis && showCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
	}

	// Reset internal screen renderer buffer.
	s.buf.Reset()

	// If our updates flush buffer has content, write it to the output writer.
	if buf.Len() > 0 {
		if s.logger != nil {
			s.logger.Printf("output: %q", buf.String())
		}
		if _, err := io.Copy(s.w, &buf); err != nil {
			return fmt.Errorf("bubbletea: error flushing update to the writer: %w", err)
		}
	}

	s.lastView = &view

	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *cursedRenderer) flush(closing bool) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	view := s.view
	frameArea := uv.Rect(0, 0, s.width, s.height)
	if len(view.Content) == 0 {
		// If the component is nil, we should clear the screen buffer.
		frameArea.Max.Y = 0
	}

	content := uv.NewStyledString(view.Content)
	if !view.AltScreen {
		// We need to resizes the screen based on the frame height and
		// terminal width. This is because the frame height can change based on
		// the content of the frame. For example, if the frame contains a list
		// of items, the height of the frame will be the number of items in the
		// list. This is different from the alt screen buffer, which has a
		// fixed height and width.
		frameHeight := content.Height()
		if frameHeight != frameArea.Dy() {
			frameArea.Max.Y = frameHeight
		}
	}

	// Restore tab stops if we have tab optimizations enabled.
	if s.starting && s.hardTabs {
		_, _ = s.scr.WriteString(ansi.SetTabEvery8Columns)
	}

	if !s.starting && !closing && !s.pendingErase && s.lastView != nil && viewEquals(s.lastView, &view) && frameArea == s.cellbuf.Bounds() {
		// No changes, nothing to do.
		return nil
	}

	// We're no longer starting.
	s.starting = false
	s.pendingErase = false

	if frameArea != s.cellbuf.Bounds() {
		s.scr.Erase() // Force a full redraw to avoid artifacts.

		// We need to reset the touched lines buffer to match the new height.
		s.cellbuf.Touched = nil

		// Resize the screen buffer to match the frame area. This is necessary
		// to ensure that the screen buffer is the same size as the frame area
		// and to avoid rendering issues when the frame area is smaller than
		// the screen buffer.
		s.cellbuf.Resize(frameArea.Dx(), frameArea.Dy())
	}

	// Clear our screen buffer before copying the new frame into it to ensure
	// we erase any old content.
	s.cellbuf.Clear()
	content.Draw(s.cellbuf, s.cellbuf.Bounds())

	// If the frame height is greater than the screen height, we drop the
	// lines from the top of the buffer.
	if frameHeight := frameArea.Dy(); frameHeight > s.height {
		s.cellbuf.Lines = s.cellbuf.Lines[frameHeight-s.height:]
	}

	// Alt screen mode.
	shouldUpdateAltScreen := (s.lastView == nil && view.AltScreen) || (s.lastView != nil && s.lastView.AltScreen != view.AltScreen)
	if shouldUpdateAltScreen {
		// We want to enter/exit altscreen mode but defer writing the actual
		// sequences until we flush the rest of the updates. This is because we
		// control the cursor visibility and we need to ensure that happens
		// after entering/exiting alt screen mode. Some terminals have
		// different cursor visibility states for main and alt screen modes and
		// this ensures we handle that correctly.
		enableAltScreen(s, view.AltScreen, false)
	}

	// bracketed paste mode.
	if s.lastView == nil || view.DisableBracketedPasteMode != s.lastView.DisableBracketedPasteMode {
		if !view.DisableBracketedPasteMode {
			_, _ = s.scr.WriteString(ansi.SetModeBracketedPaste)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeBracketedPaste)
		}
	}

	// report focus events mode.
	if s.lastView == nil || s.lastView.ReportFocus != view.ReportFocus {
		if view.ReportFocus {
			_, _ = s.scr.WriteString(ansi.SetModeFocusEvent)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeFocusEvent)
		}
	}

	// mouse events mode.
	if s.lastView == nil || view.MouseMode != s.lastView.MouseMode {
		switch view.MouseMode {
		case MouseModeNone:
			if s.lastView != nil && s.lastView.MouseMode != MouseModeNone {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent +
					ansi.ResetModeMouseAnyEvent +
					ansi.ResetModeMouseExtSgr)
			}
		case MouseModeCellMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeAllMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseAnyEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseButtonEvent + ansi.SetModeMouseExtSgr)
		case MouseModeAllMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeCellMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseAnyEvent + ansi.SetModeMouseExtSgr)
		}
	}

	// Set window title.
	if s.lastView == nil || view.WindowTitle != s.lastView.WindowTitle {
		if s.lastView != nil || view.WindowTitle != "" {
			_, _ = s.scr.WriteString(ansi.SetWindowTitle(view.WindowTitle))
		}
	}

	// kitty keyboard protocol
	if s.lastView == nil || view.KeyboardEnhancements != s.lastView.KeyboardEnhancements ||
		view.AltScreen != s.lastView.AltScreen {
		// NOTE: We need to reset the keyboard protocol when switching
		// between main and alt screen. This is because the specs specify
		// two different states for the main and alt screen.

		// Enable modifyOtherKeys and Kitty keyboard protocol.
		_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys2)

		kittyFlags := keyboardEnhancementsFlags(view.KeyboardEnhancements)
		_, _ = s.scr.WriteString(ansi.KittyKeyboard(kittyFlags, 1))
		if !closing {
			// Request keyboard enhancements when they change
			_, _ = s.scr.WriteString(ansi.RequestKittyKeyboard)
		}
	}

	// Set terminal colors.
	var (
		cc, lcc  color.Color
		lfg, lbg color.Color
	)
	if view.Cursor != nil {
		cc = view.Cursor.Color
	}
	if s.lastView != nil {
		if s.lastView.Cursor != nil {
			lcc = s.lastView.Cursor.Color
		}
		lfg = s.lastView.ForegroundColor
		lbg = s.lastView.BackgroundColor
	}
	for _, c := range []struct {
		newColor color.Color
		oldColor color.Color
		reset    string
		setter   func(string) string
	}{
		{newColor: cc, oldColor: lcc, reset: ansi.ResetCursorColor, setter: ansi.SetCursorColor},
		{newColor: view.ForegroundColor, oldColor: lfg, reset: ansi.ResetForegroundColor, setter: ansi.SetForegroundColor},
		{newColor: view.BackgroundColor, oldColor: lbg, reset: ansi.ResetBackgroundColor, setter: ansi.SetBackgroundColor},
	} {
		if c.newColor != c.oldColor {
			if c.newColor == nil {
				// Reset the color if it was set to nil.
				_, _ = s.scr.WriteString(c.reset)
			} else {
				// Set the color.
				col, ok := colorful.MakeColor(c.newColor)
				if ok {
					_, _ = s.scr.WriteString(c.setter(col.Hex()))
				}
			}
		}
	}

	// Set cursor shape and blink if set.
	var ccStyle, lcStyle int
	var lcur *Cursor
	ccur := view.Cursor
	if lv := s.lastView; lv != nil {
		lcur = lv.Cursor
	}
	if ccur != nil {
		ccStyle = encodeCursorStyle(ccur.Shape, ccur.Blink)
	}
	if lcur != nil {
		lcStyle = encodeCursorStyle(lcur.Shape, lcur.Blink)
	}
	if ccStyle != lcStyle {
		_, _ = s.scr.WriteString(ansi.SetCursorStyle(ccStyle))
	}

	// Render progress bar if it's changed.
	if (s.lastView == nil && view.ProgressBar != nil && view.ProgressBar.State != ProgressBarNone) ||
		(s.lastView != nil && (s.lastView.ProgressBar == nil) != (view.ProgressBar == nil)) ||
		(s.lastView != nil && s.lastView.ProgressBar != nil && view.ProgressBar != nil && *s.lastView.ProgressBar != *view.ProgressBar) {
		// Render or clear the progress bar if it was added or removed.
		setProgressBar(s, view.ProgressBar)
	}

	// Render and queue changes to the screen buffer.
	s.scr.Render(s.cellbuf.RenderBuffer)

	if cur := view.Cursor; cur != nil {
		// MoveTo must come after [uv.TerminalRenderer.Render] because the
		// cursor position might get updated during rendering.
		s.scr.MoveTo(view.Cursor.X, view.Cursor.Y)
	} else if !view.AltScreen {
		// We don't want the cursor to be dangling at the end of the line in
		// inline mode because it can cause unwanted line wraps in some
		// terminals. So we move it to the beginning of the next line if
		// necessary.
		// This is only needed when the cursor is hidden because when it's
		// visible, we already set its position above.
		x, y := s.scr.Position()
		if x >= s.width-1 {
			s.scr.MoveTo(0, y)
		}
	}

	if err := s.scr.Flush(); err != nil {
		return fmt.Errorf("bubbletea: error flushing screen writer: %w", err)
	}

	// Check if we have any render updates to flush.
	hasUpdates := s.buf.Len() > 0

	// Cursor visibility.
	didShowCursor := s.lastView != nil && s.lastView.Cursor != nil
	showCursor := view.Cursor != nil
	hideCursor := !showCursor
	shouldUpdateCursorVis := (s.lastView == nil || didShowCursor != showCursor) || shouldUpdateAltScreen

	// Build final output buffer with synchronized output or hide/show cursor
	// updates. But first, enter/exit alt screen mode if needed.
	//
	// Here, we have two scenarios:
	// 1. Synchronized output updates are supported. In this case, we want to
	//    wrap all updates, unless it's just a cursor visibility change, in
	//    synchronized output mode. This is because synchronized output mode
	//    takes care of rendering the updates atomically. In the case of
	//    just a cursor visibility change, we don't need to enter
	//    synchronized output mode because it's just a single sequence to
	//    flush out to the terminal.
	//
	// 2. We don't have synchronized output updates support. In this case, and
	//    if the cursor is visible or should be visible, we wrap the updates
	//    with hide/show cursor sequences to try and mitigate cursor
	//    flickering. This is terminal dependent and may still result in
	//    flickering in some terminals. It's the best effort we can do instead
	//    of showing the cursor flying around the screen during updates.

	var buf bytes.Buffer
	if shouldUpdateAltScreen {
		// We always disable keyboard enhancements when switching screens
		// because the terminal is expected to have two different keyboard
		// registries for main and alt screens.
		_, _ = buf.WriteString(ansi.ResetModifyOtherKeys)
		_, _ = buf.WriteString(ansi.KittyKeyboard(0, 1))
		if view.AltScreen {
			// Entering alt screen mode.
			buf.WriteString(ansi.SetModeAltScreenSaveCursor)
		} else {
			// Exiting alt screen mode.
			buf.WriteString(ansi.ResetModeAltScreenSaveCursor)
		}
	}

	if s.syncdUpdates {
		if hasUpdates {
			// We have synchronized output updates enabled.
			buf.WriteString(ansi.SetModeSynchronizedOutput)
		}
		if shouldUpdateCursorVis && hideCursor {
			// Do we need to update the cursor visibility to hidden? If so, do
			// it here before writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
		}
	} else if (shouldUpdateCursorVis && hideCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
	}

	if hasUpdates {
		buf.Write(s.buf.Bytes())
	}

	if s.syncdUpdates {
		if shouldUpdateCursorVis && showCursor {
			// Do we need to update the cursor visibility to visible? If so, do
			// it here after writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
		}
		if hasUpdates {
			// Close synchronized output mode.
			buf.WriteString(ansi.ResetModeSynchronizedOutput)
		}
	} else if (shouldUpdateCursorVis && showCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
	}

	// Reset internal screen renderer buffer.
	s.buf.Reset()

	// If our updates flush buffer has content, write it to the output writer.
	if buf.Len() > 0 {
		if s.logger != nil {
			s.logger.Printf("output: %q", buf.String())
		}
		if _, err := io.Copy(s.w, &buf); err != nil {
			return fmt.Errorf("bubbletea: error flushing update to the writer: %w", err)
		}
	}

	s.lastView = &view

	return nil
}
```

### 🔹 函式: `cursedRenderer.resize()`
- **變更前簽章 (Before)**: `func cursedRenderer.resize(w, h int)` (L619~L631)
- **變更後簽章 (After)**: `func cursedRenderer.resize(w, h int)` (L621~L634)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *cursedRenderer) resize(w, h int) {
	s.mu.Lock()
	// We need to mark the screen for clear to force a redraw. However, we
	// only do so if we're using alt screen or the width has changed.
	// That's because redrawing is expensive and we can avoid it if the
	// width hasn't changed in inline mode. On the other hand, when using
	// alt screen mode, we always want to redraw because some terminals
	// would scroll the screen and our content would be lost.
	s.scr.Erase()
	s.width, s.height = w, h
	s.scr.Resize(s.width, s.height)
	s.mu.Unlock()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *cursedRenderer) resize(w, h int) {
	s.mu.Lock()
	// We need to mark the screen for clear to force a redraw. However, we
	// only do so if we're using alt screen or the width has changed.
	// That's because redrawing is expensive and we can avoid it if the
	// width hasn't changed in inline mode. On the other hand, when using
	// alt screen mode, we always want to redraw because some terminals
	// would scroll the screen and our content would be lost.
	s.scr.Erase()
	s.width, s.height = w, h
	s.scr.Resize(s.width, s.height)
	s.pendingErase = true
	s.mu.Unlock()
}
```


---

### 🔹 Commit #06: `dc4b0175`
- **完整 Hash**: `dc4b01750c5262f511164148e24de2cc7aabff47`
- **說明 (Ground Truth)**: fix(key): map media record to ultraviolet code (#1757)
- **變更檔案數**: 1

#### 📄 檔案: `key.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:8, E:14, A:0) ➔ After(N:8, E:14, A:0)
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

### 🔹 Commit #07: `1862dfba`
- **完整 Hash**: `1862dfba1151de8f583b598d2ed1cfedf3f5b405`
- **說明 (Ground Truth)**: fix: assign MouseButton11 = uv.MouseButton11 (#1754)
- **變更檔案數**: 1

#### 📄 檔案: `mouse.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:9, E:14, A:0) ➔ After(N:9, E:14, A:0)
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

### 🔹 Commit #08: `c60f0c53`
- **完整 Hash**: `c60f0c53042238305ec13b486326588f12aea0ec`
- **說明 (Ground Truth)**: fix: prevent data race with cursedRenderer.onMouse (#1691)
- **變更檔案數**: 1

#### 📄 檔案: `cursed_renderer.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:108, E:159, A:0) ➔ After(N:108, E:161, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 3, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `onMouse` (MODULE_STATE)
  • - [移除節點] `s.lastView.OnMouse (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `cursedRenderer.onMouse` ──[CALLS]──> `s.mu.Lock (External/Pkg)`
  • + [新增呼叫邊] `cursedRenderer.onMouse` ──[CALLS]──> `s.mu.Unlock (External/Pkg)`
  • + [新增呼叫邊] `cursedRenderer.onMouse` ──[CALLS]──> `cursedRenderer.onMouse`
  • - [移除呼叫邊] `cursedRenderer.onMouse` ──[CALLS]──> `s.lastView.OnMouse (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `cursedRenderer.onMouse()`
- **變更前簽章 (Before)**: `func cursedRenderer.onMouse(m MouseMsg)` (L766~L771)
- **變更後簽章 (After)**: `func cursedRenderer.onMouse(m MouseMsg)` (L766~L777)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *cursedRenderer) onMouse(m MouseMsg) Cmd {
	if s.lastView != nil && s.lastView.OnMouse != nil {
		return s.lastView.OnMouse(m)
	}
	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *cursedRenderer) onMouse(m MouseMsg) Cmd {
	var onMouse func(MouseMsg) Cmd
	s.mu.Lock()
	if s.lastView != nil {
		onMouse = s.lastView.OnMouse
	}
	s.mu.Unlock()
	if onMouse != nil {
		return onMouse(m)
	}
	return nil
}
```


---

### 🔹 Commit #09: `074596e1`
- **完整 Hash**: `074596e14e2f5ca5e3986ee72e7c08f1569c4178`
- **說明 (Ground Truth)**: fix: skip input reader restore when input is disabled (#1680)
- **變更檔案數**: 1

#### 📄 檔案: `tea.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:156, E:206, A:0) ➔ After(N:156, E:206, A:0)
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

### 🔹 函式: `Program.RestoreTerminal()`
- **變更前簽章 (Before)**: `func Program.RestoreTerminal()` (L1344~L1364)
- **變更後簽章 (After)**: `func Program.RestoreTerminal()` (L1344~L1366)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Program) RestoreTerminal() error {
	atomic.StoreUint32(&p.ignoreSignals, 0)

	if err := p.initTerminal(); err != nil {
		return err
	}
	if err := p.initInputReader(false); err != nil {
		return err
	}

	p.startRenderer()

	// If the output is a terminal, it may have been resized while another
	// process was at the foreground, in which case we may not have received
	// SIGWINCH. Detect any size change now and propagate the new size as
	// needed.
	go p.checkResize()

	// Flush queued commands.
	return p.flush()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Program) RestoreTerminal() error {
	atomic.StoreUint32(&p.ignoreSignals, 0)

	if err := p.initTerminal(); err != nil {
		return err
	}
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return err
		}
	}

	p.startRenderer()

	// If the output is a terminal, it may have been resized while another
	// process was at the foreground, in which case we may not have received
	// SIGWINCH. Detect any size change now and propagate the new size as
	// needed.
	go p.checkResize()

	// Flush queued commands.
	return p.flush()
}
```


---

### 🔹 Commit #10: `ac355fe1`
- **完整 Hash**: `ac355fe194c3e9f07c0d2b061bcf51ad802103fb`
- **說明 (Ground Truth)**: fix(renderer): restore tab stops if hard tabs are enabled (#1677)
- **變更檔案數**: 1

#### 📄 檔案: `cursed_renderer.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:108, E:159, A:0) ➔ After(N:108, E:159, A:0)
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

### 🔹 函式: `cursedRenderer.setOptimizations()`
- **變更前簽章 (Before)**: `func cursedRenderer.setOptimizations(hardTabs, backspace, mapnl bool)` (L59~L68)
- **變更後簽章 (After)**: `func cursedRenderer.setOptimizations(hardTabs, backspace, mapnl bool)` (L59~L72)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *cursedRenderer) setOptimizations(hardTabs, backspace, mapnl bool) {
	s.mu.Lock()
	s.hardTabs = hardTabs
	s.backspace = backspace
	s.mapnl = mapnl
	s.scr.SetTabStops(s.width)
	s.scr.SetBackspace(s.backspace)
	s.scr.SetMapNewline(s.mapnl)
	s.mu.Unlock()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *cursedRenderer) setOptimizations(hardTabs, backspace, mapnl bool) {
	s.mu.Lock()
	s.hardTabs = hardTabs
	s.backspace = backspace
	s.mapnl = mapnl
	if s.hardTabs {
		s.scr.SetTabStops(s.width)
	} else {
		s.scr.SetTabStops(-1)
	}
	s.scr.SetBackspace(s.backspace)
	s.scr.SetMapNewline(s.mapnl)
	s.mu.Unlock()
}
```

### 🔹 函式: `reset()`
- **變更前簽章 (Before)**: `func reset(s *cursedRenderer)` (L584~L595)
- **變更後簽章 (After)**: `func reset(s *cursedRenderer)` (L593~L608)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func reset(s *cursedRenderer) {
	s.buf.Reset()
	scr := uv.NewTerminalRenderer(&s.buf, s.env)
	scr.SetColorProfile(s.profile)
	scr.SetRelativeCursor(true) // Always start in inline mode
	scr.SetFullscreen(false)    // Always start in inline mode
	scr.SetTabStops(s.width)
	scr.SetBackspace(s.backspace)
	scr.SetMapNewline(s.mapnl)
	scr.SetScrollOptim(runtime.GOOS != "windows") // disable scroll optimization on Windows due to bugs in some terminals
	s.scr = scr
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func reset(s *cursedRenderer) {
	s.buf.Reset()
	scr := uv.NewTerminalRenderer(&s.buf, s.env)
	scr.SetColorProfile(s.profile)
	scr.SetRelativeCursor(true) // Always start in inline mode
	scr.SetFullscreen(false)    // Always start in inline mode
	if s.hardTabs {
		scr.SetTabStops(s.width)
	} else {
		scr.SetTabStops(-1)
	}
	scr.SetBackspace(s.backspace)
	scr.SetMapNewline(s.mapnl)
	scr.SetScrollOptim(runtime.GOOS != "windows") // disable scroll optimization on Windows due to bugs in some terminals
	s.scr = scr
}
```

### 🔹 函式: `cursedRenderer.flush()`
- **變更前簽章 (Before)**: `func cursedRenderer.flush(closing bool)` (L253~L567)
- **變更後簽章 (After)**: `func cursedRenderer.flush(closing bool)` (L257~L576)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *cursedRenderer) flush(closing bool) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	view := s.view
	frameArea := uv.Rect(0, 0, s.width, s.height)
	if len(view.Content) == 0 {
		// If the component is nil, we should clear the screen buffer.
		frameArea.Max.Y = 0
	}

	content := uv.NewStyledString(view.Content)
	if !view.AltScreen {
		// We need to resizes the screen based on the frame height and
		// terminal width. This is because the frame height can change based on
		// the content of the frame. For example, if the frame contains a list
		// of items, the height of the frame will be the number of items in the
		// list. This is different from the alt screen buffer, which has a
		// fixed height and width.
		frameHeight := content.Height()
		if frameHeight != frameArea.Dy() {
			frameArea.Max.Y = frameHeight
		}
	}

	if !s.starting && !closing && s.lastView != nil && viewEquals(s.lastView, &view) && frameArea == s.cellbuf.Bounds() {
		// No changes, nothing to do.
		return nil
	}

	// We're no longer starting.
	s.starting = false

	if frameArea != s.cellbuf.Bounds() {
		s.scr.Erase() // Force a full redraw to avoid artifacts.

		// We need to reset the touched lines buffer to match the new height.
		s.cellbuf.Touched = nil

		// Resize the screen buffer to match the frame area. This is necessary
		// to ensure that the screen buffer is the same size as the frame area
		// and to avoid rendering issues when the frame area is smaller than
		// the screen buffer.
		s.cellbuf.Resize(frameArea.Dx(), frameArea.Dy())
	}

	// Clear our screen buffer before copying the new frame into it to ensure
	// we erase any old content.
	s.cellbuf.Clear()
	content.Draw(s.cellbuf, s.cellbuf.Bounds())

	// If the frame height is greater than the screen height, we drop the
	// lines from the top of the buffer.
	if frameHeight := frameArea.Dy(); frameHeight > s.height {
		s.cellbuf.Lines = s.cellbuf.Lines[frameHeight-s.height:]
	}

	// Alt screen mode.
	shouldUpdateAltScreen := (s.lastView == nil && view.AltScreen) || (s.lastView != nil && s.lastView.AltScreen != view.AltScreen)
	if shouldUpdateAltScreen {
		// We want to enter/exit altscreen mode but defer writing the actual
		// sequences until we flush the rest of the updates. This is because we
		// control the cursor visibility and we need to ensure that happens
		// after entering/exiting alt screen mode. Some terminals have
		// different cursor visibility states for main and alt screen modes and
		// this ensures we handle that correctly.
		enableAltScreen(s, view.AltScreen, false)
	}

	// bracketed paste mode.
	if s.lastView == nil || view.DisableBracketedPasteMode != s.lastView.DisableBracketedPasteMode {
		if !view.DisableBracketedPasteMode {
			_, _ = s.scr.WriteString(ansi.SetModeBracketedPaste)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeBracketedPaste)
		}
	}

	// report focus events mode.
	if s.lastView == nil || s.lastView.ReportFocus != view.ReportFocus {
		if view.ReportFocus {
			_, _ = s.scr.WriteString(ansi.SetModeFocusEvent)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeFocusEvent)
		}
	}

	// mouse events mode.
	if s.lastView == nil || view.MouseMode != s.lastView.MouseMode {
		switch view.MouseMode {
		case MouseModeNone:
			if s.lastView != nil && s.lastView.MouseMode != MouseModeNone {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent +
					ansi.ResetModeMouseAnyEvent +
					ansi.ResetModeMouseExtSgr)
			}
		case MouseModeCellMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeAllMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseAnyEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseButtonEvent + ansi.SetModeMouseExtSgr)
		case MouseModeAllMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeCellMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseAnyEvent + ansi.SetModeMouseExtSgr)
		}
	}

	// Set window title.
	if s.lastView == nil || view.WindowTitle != s.lastView.WindowTitle {
		if s.lastView != nil || view.WindowTitle != "" {
			_, _ = s.scr.WriteString(ansi.SetWindowTitle(view.WindowTitle))
		}
	}

	// kitty keyboard protocol
	if s.lastView == nil || view.KeyboardEnhancements != s.lastView.KeyboardEnhancements ||
		view.AltScreen != s.lastView.AltScreen {
		// NOTE: We need to reset the keyboard protocol when switching
		// between main and alt screen. This is because the specs specify
		// two different states for the main and alt screen.

		// Enable modifyOtherKeys and Kitty keyboard protocol.
		_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys2)

		kittyFlags := keyboardEnhancementsFlags(view.KeyboardEnhancements)
		_, _ = s.scr.WriteString(ansi.KittyKeyboard(kittyFlags, 1))
		if !closing {
			// Request keyboard enhancements when they change
			_, _ = s.scr.WriteString(ansi.RequestKittyKeyboard)
		}
	}

	// Set terminal colors.
	var (
		cc, lcc  color.Color
		lfg, lbg color.Color
	)
	if view.Cursor != nil {
		cc = view.Cursor.Color
	}
	if s.lastView != nil {
		if s.lastView.Cursor != nil {
			lcc = s.lastView.Cursor.Color
		}
		lfg = s.lastView.ForegroundColor
		lbg = s.lastView.BackgroundColor
	}
	for _, c := range []struct {
		newColor color.Color
		oldColor color.Color
		reset    string
		setter   func(string) string
	}{
		{newColor: cc, oldColor: lcc, reset: ansi.ResetCursorColor, setter: ansi.SetCursorColor},
		{newColor: view.ForegroundColor, oldColor: lfg, reset: ansi.ResetForegroundColor, setter: ansi.SetForegroundColor},
		{newColor: view.BackgroundColor, oldColor: lbg, reset: ansi.ResetBackgroundColor, setter: ansi.SetBackgroundColor},
	} {
		if c.newColor != c.oldColor {
			if c.newColor == nil {
				// Reset the color if it was set to nil.
				_, _ = s.scr.WriteString(c.reset)
			} else {
				// Set the color.
				col, ok := colorful.MakeColor(c.newColor)
				if ok {
					_, _ = s.scr.WriteString(c.setter(col.Hex()))
				}
			}
		}
	}

	// Set cursor shape and blink if set.
	var ccStyle, lcStyle int
	var lcur *Cursor
	ccur := view.Cursor
	if lv := s.lastView; lv != nil {
		lcur = lv.Cursor
	}
	if ccur != nil {
		ccStyle = encodeCursorStyle(ccur.Shape, ccur.Blink)
	}
	if lcur != nil {
		lcStyle = encodeCursorStyle(lcur.Shape, lcur.Blink)
	}
	if ccStyle != lcStyle {
		_, _ = s.scr.WriteString(ansi.SetCursorStyle(ccStyle))
	}

	// Render progress bar if it's changed.
	if (s.lastView == nil && view.ProgressBar != nil && view.ProgressBar.State != ProgressBarNone) ||
		(s.lastView != nil && (s.lastView.ProgressBar == nil) != (view.ProgressBar == nil)) ||
		(s.lastView != nil && s.lastView.ProgressBar != nil && view.ProgressBar != nil && *s.lastView.ProgressBar != *view.ProgressBar) {
		// Render or clear the progress bar if it was added or removed.
		setProgressBar(s, view.ProgressBar)
	}

	// Render and queue changes to the screen buffer.
	s.scr.Render(s.cellbuf.RenderBuffer)

	if cur := view.Cursor; cur != nil {
		// MoveTo must come after [uv.TerminalRenderer.Render] because the
		// cursor position might get updated during rendering.
		s.scr.MoveTo(view.Cursor.X, view.Cursor.Y)
	} else if !view.AltScreen {
		// We don't want the cursor to be dangling at the end of the line in
		// inline mode because it can cause unwanted line wraps in some
		// terminals. So we move it to the beginning of the next line if
		// necessary.
		// This is only needed when the cursor is hidden because when it's
		// visible, we already set its position above.
		x, y := s.scr.Position()
		if x >= s.width-1 {
			s.scr.MoveTo(0, y)
		}
	}

	if err := s.scr.Flush(); err != nil {
		return fmt.Errorf("bubbletea: error flushing screen writer: %w", err)
	}

	// Check if we have any render updates to flush.
	hasUpdates := s.buf.Len() > 0

	// Cursor visibility.
	didShowCursor := s.lastView != nil && s.lastView.Cursor != nil
	showCursor := view.Cursor != nil
	hideCursor := !showCursor
	shouldUpdateCursorVis := (s.lastView == nil || didShowCursor != showCursor) || shouldUpdateAltScreen

	// Build final output buffer with synchronized output or hide/show cursor
	// updates. But first, enter/exit alt screen mode if needed.
	//
	// Here, we have two scenarios:
	// 1. Synchronized output updates are supported. In this case, we want to
	//    wrap all updates, unless it's just a cursor visibility change, in
	//    synchronized output mode. This is because synchronized output mode
	//    takes care of rendering the updates atomically. In the case of
	//    just a cursor visibility change, we don't need to enter
	//    synchronized output mode because it's just a single sequence to
	//    flush out to the terminal.
	//
	// 2. We don't have synchronized output updates support. In this case, and
	//    if the cursor is visible or should be visible, we wrap the updates
	//    with hide/show cursor sequences to try and mitigate cursor
	//    flickering. This is terminal dependent and may still result in
	//    flickering in some terminals. It's the best effort we can do instead
	//    of showing the cursor flying around the screen during updates.

	var buf bytes.Buffer
	if shouldUpdateAltScreen {
		// We always disable keyboard enhancements when switching screens
		// because the terminal is expected to have two different keyboard
		// registries for main and alt screens.
		_, _ = buf.WriteString(ansi.ResetModifyOtherKeys)
		_, _ = buf.WriteString(ansi.KittyKeyboard(0, 1))
		if view.AltScreen {
			// Entering alt screen mode.
			buf.WriteString(ansi.SetModeAltScreenSaveCursor)
		} else {
			// Exiting alt screen mode.
			buf.WriteString(ansi.ResetModeAltScreenSaveCursor)
		}
	}

	if s.syncdUpdates {
		if hasUpdates {
			// We have synchronized output updates enabled.
			buf.WriteString(ansi.SetModeSynchronizedOutput)
		}
		if shouldUpdateCursorVis && hideCursor {
			// Do we need to update the cursor visibility to hidden? If so, do
			// it here before writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
		}
	} else if (shouldUpdateCursorVis && hideCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
	}

	if hasUpdates {
		buf.Write(s.buf.Bytes())
	}

	if s.syncdUpdates {
		if shouldUpdateCursorVis && showCursor {
			// Do we need to update the cursor visibility to visible? If so, do
			// it here after writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
		}
		if hasUpdates {
			// Close synchronized output mode.
			buf.WriteString(ansi.ResetModeSynchronizedOutput)
		}
	} else if (shouldUpdateCursorVis && showCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
	}

	// Reset internal screen renderer buffer.
	s.buf.Reset()

	// If our updates flush buffer has content, write it to the output writer.
	if buf.Len() > 0 {
		if s.logger != nil {
			s.logger.Printf("output: %q", buf.String())
		}
		if _, err := io.Copy(s.w, &buf); err != nil {
			return fmt.Errorf("bubbletea: error flushing update to the writer: %w", err)
		}
	}

	s.lastView = &view

	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *cursedRenderer) flush(closing bool) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	view := s.view
	frameArea := uv.Rect(0, 0, s.width, s.height)
	if len(view.Content) == 0 {
		// If the component is nil, we should clear the screen buffer.
		frameArea.Max.Y = 0
	}

	content := uv.NewStyledString(view.Content)
	if !view.AltScreen {
		// We need to resizes the screen based on the frame height and
		// terminal width. This is because the frame height can change based on
		// the content of the frame. For example, if the frame contains a list
		// of items, the height of the frame will be the number of items in the
		// list. This is different from the alt screen buffer, which has a
		// fixed height and width.
		frameHeight := content.Height()
		if frameHeight != frameArea.Dy() {
			frameArea.Max.Y = frameHeight
		}
	}

	// Restore tab stops if we have tab optimizations enabled.
	if s.starting && s.hardTabs {
		_, _ = s.scr.WriteString(ansi.SetTabEvery8Columns)
	}

	if !s.starting && !closing && s.lastView != nil && viewEquals(s.lastView, &view) && frameArea == s.cellbuf.Bounds() {
		// No changes, nothing to do.
		return nil
	}

	// We're no longer starting.
	s.starting = false

	if frameArea != s.cellbuf.Bounds() {
		s.scr.Erase() // Force a full redraw to avoid artifacts.

		// We need to reset the touched lines buffer to match the new height.
		s.cellbuf.Touched = nil

		// Resize the screen buffer to match the frame area. This is necessary
		// to ensure that the screen buffer is the same size as the frame area
		// and to avoid rendering issues when the frame area is smaller than
		// the screen buffer.
		s.cellbuf.Resize(frameArea.Dx(), frameArea.Dy())
	}

	// Clear our screen buffer before copying the new frame into it to ensure
	// we erase any old content.
	s.cellbuf.Clear()
	content.Draw(s.cellbuf, s.cellbuf.Bounds())

	// If the frame height is greater than the screen height, we drop the
	// lines from the top of the buffer.
	if frameHeight := frameArea.Dy(); frameHeight > s.height {
		s.cellbuf.Lines = s.cellbuf.Lines[frameHeight-s.height:]
	}

	// Alt screen mode.
	shouldUpdateAltScreen := (s.lastView == nil && view.AltScreen) || (s.lastView != nil && s.lastView.AltScreen != view.AltScreen)
	if shouldUpdateAltScreen {
		// We want to enter/exit altscreen mode but defer writing the actual
		// sequences until we flush the rest of the updates. This is because we
		// control the cursor visibility and we need to ensure that happens
		// after entering/exiting alt screen mode. Some terminals have
		// different cursor visibility states for main and alt screen modes and
		// this ensures we handle that correctly.
		enableAltScreen(s, view.AltScreen, false)
	}

	// bracketed paste mode.
	if s.lastView == nil || view.DisableBracketedPasteMode != s.lastView.DisableBracketedPasteMode {
		if !view.DisableBracketedPasteMode {
			_, _ = s.scr.WriteString(ansi.SetModeBracketedPaste)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeBracketedPaste)
		}
	}

	// report focus events mode.
	if s.lastView == nil || s.lastView.ReportFocus != view.ReportFocus {
		if view.ReportFocus {
			_, _ = s.scr.WriteString(ansi.SetModeFocusEvent)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeFocusEvent)
		}
	}

	// mouse events mode.
	if s.lastView == nil || view.MouseMode != s.lastView.MouseMode {
		switch view.MouseMode {
		case MouseModeNone:
			if s.lastView != nil && s.lastView.MouseMode != MouseModeNone {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent +
					ansi.ResetModeMouseAnyEvent +
					ansi.ResetModeMouseExtSgr)
			}
		case MouseModeCellMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeAllMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseAnyEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseButtonEvent + ansi.SetModeMouseExtSgr)
		case MouseModeAllMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeCellMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseAnyEvent + ansi.SetModeMouseExtSgr)
		}
	}

	// Set window title.
	if s.lastView == nil || view.WindowTitle != s.lastView.WindowTitle {
		if s.lastView != nil || view.WindowTitle != "" {
			_, _ = s.scr.WriteString(ansi.SetWindowTitle(view.WindowTitle))
		}
	}

	// kitty keyboard protocol
	if s.lastView == nil || view.KeyboardEnhancements != s.lastView.KeyboardEnhancements ||
		view.AltScreen != s.lastView.AltScreen {
		// NOTE: We need to reset the keyboard protocol when switching
		// between main and alt screen. This is because the specs specify
		// two different states for the main and alt screen.

		// Enable modifyOtherKeys and Kitty keyboard protocol.
		_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys2)

		kittyFlags := keyboardEnhancementsFlags(view.KeyboardEnhancements)
		_, _ = s.scr.WriteString(ansi.KittyKeyboard(kittyFlags, 1))
		if !closing {
			// Request keyboard enhancements when they change
			_, _ = s.scr.WriteString(ansi.RequestKittyKeyboard)
		}
	}

	// Set terminal colors.
	var (
		cc, lcc  color.Color
		lfg, lbg color.Color
	)
	if view.Cursor != nil {
		cc = view.Cursor.Color
	}
	if s.lastView != nil {
		if s.lastView.Cursor != nil {
			lcc = s.lastView.Cursor.Color
		}
		lfg = s.lastView.ForegroundColor
		lbg = s.lastView.BackgroundColor
	}
	for _, c := range []struct {
		newColor color.Color
		oldColor color.Color
		reset    string
		setter   func(string) string
	}{
		{newColor: cc, oldColor: lcc, reset: ansi.ResetCursorColor, setter: ansi.SetCursorColor},
		{newColor: view.ForegroundColor, oldColor: lfg, reset: ansi.ResetForegroundColor, setter: ansi.SetForegroundColor},
		{newColor: view.BackgroundColor, oldColor: lbg, reset: ansi.ResetBackgroundColor, setter: ansi.SetBackgroundColor},
	} {
		if c.newColor != c.oldColor {
			if c.newColor == nil {
				// Reset the color if it was set to nil.
				_, _ = s.scr.WriteString(c.reset)
			} else {
				// Set the color.
				col, ok := colorful.MakeColor(c.newColor)
				if ok {
					_, _ = s.scr.WriteString(c.setter(col.Hex()))
				}
			}
		}
	}

	// Set cursor shape and blink if set.
	var ccStyle, lcStyle int
	var lcur *Cursor
	ccur := view.Cursor
	if lv := s.lastView; lv != nil {
		lcur = lv.Cursor
	}
	if ccur != nil {
		ccStyle = encodeCursorStyle(ccur.Shape, ccur.Blink)
	}
	if lcur != nil {
		lcStyle = encodeCursorStyle(lcur.Shape, lcur.Blink)
	}
	if ccStyle != lcStyle {
		_, _ = s.scr.WriteString(ansi.SetCursorStyle(ccStyle))
	}

	// Render progress bar if it's changed.
	if (s.lastView == nil && view.ProgressBar != nil && view.ProgressBar.State != ProgressBarNone) ||
		(s.lastView != nil && (s.lastView.ProgressBar == nil) != (view.ProgressBar == nil)) ||
		(s.lastView != nil && s.lastView.ProgressBar != nil && view.ProgressBar != nil && *s.lastView.ProgressBar != *view.ProgressBar) {
		// Render or clear the progress bar if it was added or removed.
		setProgressBar(s, view.ProgressBar)
	}

	// Render and queue changes to the screen buffer.
	s.scr.Render(s.cellbuf.RenderBuffer)

	if cur := view.Cursor; cur != nil {
		// MoveTo must come after [uv.TerminalRenderer.Render] because the
		// cursor position might get updated during rendering.
		s.scr.MoveTo(view.Cursor.X, view.Cursor.Y)
	} else if !view.AltScreen {
		// We don't want the cursor to be dangling at the end of the line in
		// inline mode because it can cause unwanted line wraps in some
		// terminals. So we move it to the beginning of the next line if
		// necessary.
		// This is only needed when the cursor is hidden because when it's
		// visible, we already set its position above.
		x, y := s.scr.Position()
		if x >= s.width-1 {
			s.scr.MoveTo(0, y)
		}
	}

	if err := s.scr.Flush(); err != nil {
		return fmt.Errorf("bubbletea: error flushing screen writer: %w", err)
	}

	// Check if we have any render updates to flush.
	hasUpdates := s.buf.Len() > 0

	// Cursor visibility.
	didShowCursor := s.lastView != nil && s.lastView.Cursor != nil
	showCursor := view.Cursor != nil
	hideCursor := !showCursor
	shouldUpdateCursorVis := (s.lastView == nil || didShowCursor != showCursor) || shouldUpdateAltScreen

	// Build final output buffer with synchronized output or hide/show cursor
	// updates. But first, enter/exit alt screen mode if needed.
	//
	// Here, we have two scenarios:
	// 1. Synchronized output updates are supported. In this case, we want to
	//    wrap all updates, unless it's just a cursor visibility change, in
	//    synchronized output mode. This is because synchronized output mode
	//    takes care of rendering the updates atomically. In the case of
	//    just a cursor visibility change, we don't need to enter
	//    synchronized output mode because it's just a single sequence to
	//    flush out to the terminal.
	//
	// 2. We don't have synchronized output updates support. In this case, and
	//    if the cursor is visible or should be visible, we wrap the updates
	//    with hide/show cursor sequences to try and mitigate cursor
	//    flickering. This is terminal dependent and may still result in
	//    flickering in some terminals. It's the best effort we can do instead
	//    of showing the cursor flying around the screen during updates.

	var buf bytes.Buffer
	if shouldUpdateAltScreen {
		// We always disable keyboard enhancements when switching screens
		// because the terminal is expected to have two different keyboard
		// registries for main and alt screens.
		_, _ = buf.WriteString(ansi.ResetModifyOtherKeys)
		_, _ = buf.WriteString(ansi.KittyKeyboard(0, 1))
		if view.AltScreen {
			// Entering alt screen mode.
			buf.WriteString(ansi.SetModeAltScreenSaveCursor)
		} else {
			// Exiting alt screen mode.
			buf.WriteString(ansi.ResetModeAltScreenSaveCursor)
		}
	}

	if s.syncdUpdates {
		if hasUpdates {
			// We have synchronized output updates enabled.
			buf.WriteString(ansi.SetModeSynchronizedOutput)
		}
		if shouldUpdateCursorVis && hideCursor {
			// Do we need to update the cursor visibility to hidden? If so, do
			// it here before writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
		}
	} else if (shouldUpdateCursorVis && hideCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
	}

	if hasUpdates {
		buf.Write(s.buf.Bytes())
	}

	if s.syncdUpdates {
		if shouldUpdateCursorVis && showCursor {
			// Do we need to update the cursor visibility to visible? If so, do
			// it here after writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
		}
		if hasUpdates {
			// Close synchronized output mode.
			buf.WriteString(ansi.ResetModeSynchronizedOutput)
		}
	} else if (shouldUpdateCursorVis && showCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
	}

	// Reset internal screen renderer buffer.
	s.buf.Reset()

	// If our updates flush buffer has content, write it to the output writer.
	if buf.Len() > 0 {
		if s.logger != nil {
			s.logger.Printf("output: %q", buf.String())
		}
		if _, err := io.Copy(s.w, &buf); err != nil {
			return fmt.Errorf("bubbletea: error flushing update to the writer: %w", err)
		}
	}

	s.lastView = &view

	return nil
}
```


---

### 🔹 Commit #11: `729f05c3`
- **完整 Hash**: `729f05c315343faa36902cedff46d135b6a4b3c7`
- **說明 (Ground Truth)**: fix: add missing signal.Stop in suspendProcess to prevent signal channel leak (Closes #1673) (#1674)
- **變更檔案數**: 1

#### 📄 檔案: `tty_unix.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:12, E:9, A:0) ➔ After(N:13, E:10, A:0)
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
  • + [新增節點] `signal.Stop (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `suspendProcess` ──[CALLS]──> `signal.Stop (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `suspendProcess()`
- **變更前簽章 (Before)**: `func suspendProcess()` (L40~L46)
- **變更後簽章 (After)**: `func suspendProcess()` (L40~L47)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func suspendProcess() {
	c := make(chan os.Signal, 1)
	signal.Notify(c, syscall.SIGCONT)
	_ = syscall.Kill(0, syscall.SIGTSTP)
	// blocks until a CONT happens...
	<-c
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func suspendProcess() {
	c := make(chan os.Signal, 1)
	signal.Notify(c, syscall.SIGCONT)
	defer signal.Stop(c)
	_ = syscall.Kill(0, syscall.SIGTSTP)
	// blocks until a CONT happens...
	<-c
}
```


---

### 🔹 Commit #12: `ee06e98c`
- **完整 Hash**: `ee06e98c4174012046bd35c0f869e875131859b2`
- **說明 (Ground Truth)**: fix(examples): resolve nil pointer dereference (#1663)
- **變更檔案數**: 1

#### 📄 檔案: `examples/textarea/main.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:32, E:29, A:1) ➔ After(N:32, E:29, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#CLI: main** `(CLI Entry)`
    └── ⚡ **run()**
        └── 🎯 [TRIGGERS] `main()`
            └── 🎯 [CALLS] `log.Fatal (External/Pkg)()`
            └── 🎯 [CALLS] `p.Run (External/Pkg)()`
            └── 🎯 [CALLS] `tea.NewProgram (External/Pkg)()`
            └── 🎯 [CALLS] `initialModel()`
                └── 🎯 [CALLS] `textarea.DefaultStyles (External/Pkg)()`
                └── 🎯 [CALLS] `textarea.New (External/Pkg)()`
                └── 🎯 [CALLS] `ti.Focus (External/Pkg)()`
                └── 🎯 [CALLS] `ti.SetStyles (External/Pkg)()`
                └── 🎯 [CALLS] `ti.SetVirtualCursor (External/Pkg)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `model.View()`
- **變更前簽章 (Before)**: `func model.View()` (L86~L110)
- **變更後簽章 (After)**: `func model.View()` (L86~L112)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (m model) View() tea.View {
	const (
		footer = "\n(ctrl+c to quit)\n"
	)

	var c *tea.Cursor
	if !m.textarea.VirtualCursor() {
		c = m.textarea.Cursor()

		// Set the y offset of the cursor based on the position of the textarea
		// in the application.
		offset := lipgloss.Height(m.headerView())
		c.Y += offset
	}

	f := strings.Join([]string{
		m.headerView(),
		m.textarea.View(),
		footer,
	}, "\n")

	v := tea.NewView(f)
	v.Cursor = c
	return v
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (m model) View() tea.View {
	const (
		footer = "\n(ctrl+c to quit)\n"
	)

	var c *tea.Cursor
	if !m.textarea.VirtualCursor() {
		c = m.textarea.Cursor()

		if c != nil {
			// Set the y offset of the cursor based on the position of the textarea
			// in the application.
			offset := lipgloss.Height(m.headerView())
			c.Y += offset
		}
	}

	f := strings.Join([]string{
		m.headerView(),
		m.textarea.View(),
		footer,
	}, "\n")

	v := tea.NewView(f)
	v.Cursor = c
	return v
}
```


---

### 🔹 Commit #13: `7df1e650`
- **完整 Hash**: `7df1e650b31224cc8cc6e80f9854551c9dccde10`
- **說明 (Ground Truth)**: fix(examples): migrate imports to charm.land for the glamour example (#1642)
- **變更檔案數**: 1

#### 📄 檔案: `examples/glamour/main.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:35, E:29, A:1) ➔ After(N:35, E:29, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#CLI: main** `(CLI Entry)`
    └── ⚡ **run()**
        └── 🎯 [TRIGGERS] `main()`
            └── 🎯 [CALLS] `fmt.Println (External/Pkg)()`
            └── 🎯 [CALLS] `lipgloss.HasDarkBackground (External/Pkg)()`
            └── 🎯 [CALLS] `os.Exit (External/Pkg)()`
            └── 🎯 [CALLS] `tea.NewProgram (External/Pkg)()`
            └── 🎯 [CALLS] `tea.NewProgram(model).Run (External/Pkg)()`
            └── 🎯 [CALLS] `newExample()`
                └── 🎯 [CALLS] `glamour.NewTermRenderer (External/Pkg)()`
                └── 🎯 [CALLS] `glamour.WithStyles (External/Pkg)()`
                └── 🎯 [CALLS] `glamour.WithWordWrap (External/Pkg)()`
                └── 🎯 [CALLS] `lipgloss.Color (External/Pkg)()`
                └── 🎯 [CALLS] `lipgloss.NewStyle (External/Pkg)()`
                └── 🎯 [CALLS] `lipgloss.NewStyle().
		BorderStyle (External/Pkg)()`
                └── 🎯 [CALLS] `lipgloss.NewStyle().
		BorderStyle(lipgloss.RoundedBorder()).
		BorderForeground (External/Pkg)()`
                └── 🎯 [CALLS] `lipgloss.NewStyle().
		BorderStyle(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("62")).
		PaddingRight (External/Pkg)()`
                └── 🎯 [CALLS] `lipgloss.RoundedBorder (External/Pkg)()`
                └── 🎯 [CALLS] `renderer.Render (External/Pkg)()`
                └── 🎯 [CALLS] `viewport.New (External/Pkg)()`
                └── 🎯 [CALLS] `vp.SetContent (External/Pkg)()`
                └── 🎯 [CALLS] `vp.SetHeight (External/Pkg)()`
                └── 🎯 [CALLS] `vp.SetWidth (External/Pkg)()`
                └── 🎯 [CALLS] `vp.Style.GetHorizontalFrameSize (External/Pkg)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #14: `f25595a8`
- **完整 Hash**: `f25595a848eb11a87631a9e43ffe078d713c2236`
- **說明 (Ground Truth)**: fix(renderer): use mapNl optimization when not on Windows and no PTY input (#1615)
- **變更檔案數**: 1

#### 📄 檔案: `tea.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:156, E:206, A:0) ➔ After(N:156, E:206, A:0)
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

### 🔹 函式: `Program.Run()`
- **變更前簽章 (Before)**: `func Program.Run()` (L971~L1154)
- **變更後簽章 (After)**: `func Program.Run()` (L972~L1155)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Program) Run() (returnModel Model, returnErr error) {
	if p.initialModel == nil {
		return nil, errors.New("bubbletea: InitialModel cannot be nil")
	}

	// Initialize context and teardown channel.
	p.handlers = channelHandlers{}
	cmds := make(chan Cmd)

	p.finished = make(chan struct{})
	defer func() {
		close(p.finished)
	}()

	defer p.cancel()

	if p.disableInput {
		p.input = nil
	} else if p.input == nil {
		p.input = os.Stdin
		if !term.IsTerminal(os.Stdin.Fd()) {
			ttyIn, _, err := OpenTTY()
			if err != nil {
				return p.initialModel, fmt.Errorf("bubbletea: error opening TTY: %w", err)
			}
			p.input = ttyIn
		}
	}

	// Handle signals.
	if !p.disableSignalHandler {
		p.handlers.add(p.handleSignals())
	}

	// Recover from panics.
	if !p.disableCatchPanics {
		defer func() {
			if r := recover(); r != nil {
				returnErr = fmt.Errorf("%w: %w", ErrProgramKilled, ErrProgramPanic)
				p.recoverFromPanic(r)
			}
		}()
	}

	// Check if output is a TTY before entering raw mode, hiding the cursor and
	// so on.
	if err := p.initTerminal(); err != nil {
		return p.initialModel, err
	}

	// Get the initial window size.
	width, height := p.width, p.height
	if p.ttyOutput != nil {
		// Set the initial size of the terminal.
		w, h, err := term.GetSize(p.ttyOutput.Fd())
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error getting terminal size: %w", err)
		}

		width, height = w, h
	}

	p.width, p.height = width, height
	resizeMsg := WindowSizeMsg{Width: p.width, Height: p.height}

	if p.renderer == nil {
		if p.disableRenderer {
			p.renderer = &nilRenderer{}
		} else {
			// If no renderer is set use the cursed one.
			r := newCursedRenderer(
				p.output,
				p.environ,
				p.width,
				p.height,
			)
			r.setLogger(p.logger)
			// XXX: This breaks many things especially when we want the output
			// to be compatible with terminals that are not necessary a TTY.
			// This was originally done to work around a Wish emulated-pty
			// issue where when a PTY session is detected, and we don't
			// allocate a real PTY, the terminal settings (Termios and WinCon)
			// don't change and the we end up working in cooked mode instead of
			// raw mode.
			mapNl := false // p.ttyInput == nil
			r.setOptimizations(p.useHardTabs, p.useBackspace, mapNl)
			p.renderer = r
		}
	}

	// Get the color profile and send it to the program.
	if p.profile == nil {
		cp := colorprofile.Detect(p.output, p.environ)
		p.profile = &cp
	}

	// Set the color profile on the renderer and send it to the program.
	p.renderer.setColorProfile(*p.profile)
	go p.Send(ColorProfileMsg{*p.profile})

	// Send the initial size to the program.
	go p.Send(resizeMsg)
	p.renderer.resize(resizeMsg.Width, resizeMsg.Height)

	// Send the environment variables used by the program.
	go p.Send(EnvMsg(p.environ))

	// Init the input reader and initial model.
	model := p.initialModel
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return model, err
		}
	}

	// Start the renderer.
	p.startRenderer()

	if !p.disableRenderer && shouldQuerySynchronizedOutput(p.environ) {
		// Query for synchronized updates support (mode 2026) and unicode core
		// (mode 2027). If the terminal supports it, the renderer will enable
		// it once we get the response.
		p.execute(ansi.RequestModeSynchronizedOutput +
			ansi.RequestModeUnicodeCore)
	}

	// Initialize the program.
	initCmd := model.Init()
	if initCmd != nil {
		ch := make(chan struct{})
		p.handlers.add(ch)

		go func() {
			defer close(ch)

			select {
			case cmds <- initCmd:
			case <-p.ctx.Done():
			}
		}()
	}

	// Render the initial view.
	p.render(model)

	// Handle resize events.
	p.handlers.add(p.handleResize())

	// Process commands.
	p.handlers.add(p.handleCommands(cmds))

	// Run event loop, handle updates and draw.
	var err error
	model, err = p.eventLoop(model, cmds)

	if err == nil && len(p.errs) > 0 {
		err = <-p.errs // Drain a leftover error in case eventLoop crashed.
	}

	killed := p.externalCtx.Err() != nil || p.ctx.Err() != nil || err != nil
	if killed {
		if err == nil && p.externalCtx.Err() != nil {
			// Return also as context error the cancellation of an external context.
			// This is the context the user knows about and should be able to act on.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, p.externalCtx.Err())
		} else if err == nil && p.ctx.Err() != nil {
			// Return only that the program was killed (not the internal mechanism).
			// The user does not know or need to care about the internal program context.
			err = ErrProgramKilled
		} else {
			// Return that the program was killed and also the error that caused it.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, err)
		}
	} else {
		// Graceful shutdown of the program (not killed):
		// Ensure we rendered the final state of the model.
		p.render(model)
	}

	// Restore terminal state.
	p.shutdown(killed)

	return model, err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Program) Run() (returnModel Model, returnErr error) {
	if p.initialModel == nil {
		return nil, errors.New("bubbletea: InitialModel cannot be nil")
	}

	// Initialize context and teardown channel.
	p.handlers = channelHandlers{}
	cmds := make(chan Cmd)

	p.finished = make(chan struct{})
	defer func() {
		close(p.finished)
	}()

	defer p.cancel()

	if p.disableInput {
		p.input = nil
	} else if p.input == nil {
		p.input = os.Stdin
		if !term.IsTerminal(os.Stdin.Fd()) {
			ttyIn, _, err := OpenTTY()
			if err != nil {
				return p.initialModel, fmt.Errorf("bubbletea: error opening TTY: %w", err)
			}
			p.input = ttyIn
		}
	}

	// Handle signals.
	if !p.disableSignalHandler {
		p.handlers.add(p.handleSignals())
	}

	// Recover from panics.
	if !p.disableCatchPanics {
		defer func() {
			if r := recover(); r != nil {
				returnErr = fmt.Errorf("%w: %w", ErrProgramKilled, ErrProgramPanic)
				p.recoverFromPanic(r)
			}
		}()
	}

	// Check if output is a TTY before entering raw mode, hiding the cursor and
	// so on.
	if err := p.initTerminal(); err != nil {
		return p.initialModel, err
	}

	// Get the initial window size.
	width, height := p.width, p.height
	if p.ttyOutput != nil {
		// Set the initial size of the terminal.
		w, h, err := term.GetSize(p.ttyOutput.Fd())
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error getting terminal size: %w", err)
		}

		width, height = w, h
	}

	p.width, p.height = width, height
	resizeMsg := WindowSizeMsg{Width: p.width, Height: p.height}

	if p.renderer == nil {
		if p.disableRenderer {
			p.renderer = &nilRenderer{}
		} else {
			// If no renderer is set use the cursed one.
			r := newCursedRenderer(
				p.output,
				p.environ,
				p.width,
				p.height,
			)
			r.setLogger(p.logger)
			// XXX: This breaks many things especially when we want the output
			// to be compatible with terminals that are not necessary a TTY.
			// This was originally done to work around a Wish emulated-pty
			// issue where when a PTY session is detected, and we don't
			// allocate a real PTY, the terminal settings (Termios and WinCon)
			// don't change and the we end up working in cooked mode instead of
			// raw mode. See issue #1572.
			mapNl := runtime.GOOS != "windows" && p.ttyInput == nil
			r.setOptimizations(p.useHardTabs, p.useBackspace, mapNl)
			p.renderer = r
		}
	}

	// Get the color profile and send it to the program.
	if p.profile == nil {
		cp := colorprofile.Detect(p.output, p.environ)
		p.profile = &cp
	}

	// Set the color profile on the renderer and send it to the program.
	p.renderer.setColorProfile(*p.profile)
	go p.Send(ColorProfileMsg{*p.profile})

	// Send the initial size to the program.
	go p.Send(resizeMsg)
	p.renderer.resize(resizeMsg.Width, resizeMsg.Height)

	// Send the environment variables used by the program.
	go p.Send(EnvMsg(p.environ))

	// Init the input reader and initial model.
	model := p.initialModel
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return model, err
		}
	}

	// Start the renderer.
	p.startRenderer()

	if !p.disableRenderer && shouldQuerySynchronizedOutput(p.environ) {
		// Query for synchronized updates support (mode 2026) and unicode core
		// (mode 2027). If the terminal supports it, the renderer will enable
		// it once we get the response.
		p.execute(ansi.RequestModeSynchronizedOutput +
			ansi.RequestModeUnicodeCore)
	}

	// Initialize the program.
	initCmd := model.Init()
	if initCmd != nil {
		ch := make(chan struct{})
		p.handlers.add(ch)

		go func() {
			defer close(ch)

			select {
			case cmds <- initCmd:
			case <-p.ctx.Done():
			}
		}()
	}

	// Render the initial view.
	p.render(model)

	// Handle resize events.
	p.handlers.add(p.handleResize())

	// Process commands.
	p.handlers.add(p.handleCommands(cmds))

	// Run event loop, handle updates and draw.
	var err error
	model, err = p.eventLoop(model, cmds)

	if err == nil && len(p.errs) > 0 {
		err = <-p.errs // Drain a leftover error in case eventLoop crashed.
	}

	killed := p.externalCtx.Err() != nil || p.ctx.Err() != nil || err != nil
	if killed {
		if err == nil && p.externalCtx.Err() != nil {
			// Return also as context error the cancellation of an external context.
			// This is the context the user knows about and should be able to act on.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, p.externalCtx.Err())
		} else if err == nil && p.ctx.Err() != nil {
			// Return only that the program was killed (not the internal mechanism).
			// The user does not know or need to care about the internal program context.
			err = ErrProgramKilled
		} else {
			// Return that the program was killed and also the error that caused it.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, err)
		}
	} else {
		// Graceful shutdown of the program (not killed):
		// Ensure we rendered the final state of the model.
		p.render(model)
	}

	// Restore terminal state.
	p.shutdown(killed)

	return model, err
}
```


---

### 🔹 Commit #15: `66b7abde`
- **完整 Hash**: `66b7abdecfad6cc67a5b408e66d54170a063ff89`
- **說明 (Ground Truth)**: fix: check if os.Stdin is a terminal before opening the TTY
- **變更檔案數**: 1

#### 📄 檔案: `tea.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:154, E:204, A:0) ➔ After(N:156, E:206, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `term.IsTerminal (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `os.Stdin.Fd (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Program.Run` ──[CALLS]──> `term.IsTerminal (External/Pkg)`
  • + [新增呼叫邊] `Program.Run` ──[CALLS]──> `os.Stdin.Fd (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Program.Run()`
- **變更前簽章 (Before)**: `func Program.Run()` (L971~L1152)
- **變更後簽章 (After)**: `func Program.Run()` (L971~L1154)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Program) Run() (returnModel Model, returnErr error) {
	if p.initialModel == nil {
		return nil, errors.New("bubbletea: InitialModel cannot be nil")
	}

	// Initialize context and teardown channel.
	p.handlers = channelHandlers{}
	cmds := make(chan Cmd)

	p.finished = make(chan struct{})
	defer func() {
		close(p.finished)
	}()

	defer p.cancel()

	if p.disableInput {
		p.input = nil
	} else if p.input == nil {
		// Always open the TTY for input.
		ttyIn, _, err := OpenTTY()
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error opening TTY: %w", err)
		}
		p.input = ttyIn
	}

	// Handle signals.
	if !p.disableSignalHandler {
		p.handlers.add(p.handleSignals())
	}

	// Recover from panics.
	if !p.disableCatchPanics {
		defer func() {
			if r := recover(); r != nil {
				returnErr = fmt.Errorf("%w: %w", ErrProgramKilled, ErrProgramPanic)
				p.recoverFromPanic(r)
			}
		}()
	}

	// Check if output is a TTY before entering raw mode, hiding the cursor and
	// so on.
	if err := p.initTerminal(); err != nil {
		return p.initialModel, err
	}

	// Get the initial window size.
	width, height := p.width, p.height
	if p.ttyOutput != nil {
		// Set the initial size of the terminal.
		w, h, err := term.GetSize(p.ttyOutput.Fd())
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error getting terminal size: %w", err)
		}

		width, height = w, h
	}

	p.width, p.height = width, height
	resizeMsg := WindowSizeMsg{Width: p.width, Height: p.height}

	if p.renderer == nil {
		if p.disableRenderer {
			p.renderer = &nilRenderer{}
		} else {
			// If no renderer is set use the cursed one.
			r := newCursedRenderer(
				p.output,
				p.environ,
				p.width,
				p.height,
			)
			r.setLogger(p.logger)
			// XXX: This breaks many things especially when we want the output
			// to be compatible with terminals that are not necessary a TTY.
			// This was originally done to work around a Wish emulated-pty
			// issue where when a PTY session is detected, and we don't
			// allocate a real PTY, the terminal settings (Termios and WinCon)
			// don't change and the we end up working in cooked mode instead of
			// raw mode.
			mapNl := false // p.ttyInput == nil
			r.setOptimizations(p.useHardTabs, p.useBackspace, mapNl)
			p.renderer = r
		}
	}

	// Get the color profile and send it to the program.
	if p.profile == nil {
		cp := colorprofile.Detect(p.output, p.environ)
		p.profile = &cp
	}

	// Set the color profile on the renderer and send it to the program.
	p.renderer.setColorProfile(*p.profile)
	go p.Send(ColorProfileMsg{*p.profile})

	// Send the initial size to the program.
	go p.Send(resizeMsg)
	p.renderer.resize(resizeMsg.Width, resizeMsg.Height)

	// Send the environment variables used by the program.
	go p.Send(EnvMsg(p.environ))

	// Init the input reader and initial model.
	model := p.initialModel
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return model, err
		}
	}

	// Start the renderer.
	p.startRenderer()

	if !p.disableRenderer && shouldQuerySynchronizedOutput(p.environ) {
		// Query for synchronized updates support (mode 2026) and unicode core
		// (mode 2027). If the terminal supports it, the renderer will enable
		// it once we get the response.
		p.execute(ansi.RequestModeSynchronizedOutput +
			ansi.RequestModeUnicodeCore)
	}

	// Initialize the program.
	initCmd := model.Init()
	if initCmd != nil {
		ch := make(chan struct{})
		p.handlers.add(ch)

		go func() {
			defer close(ch)

			select {
			case cmds <- initCmd:
			case <-p.ctx.Done():
			}
		}()
	}

	// Render the initial view.
	p.render(model)

	// Handle resize events.
	p.handlers.add(p.handleResize())

	// Process commands.
	p.handlers.add(p.handleCommands(cmds))

	// Run event loop, handle updates and draw.
	var err error
	model, err = p.eventLoop(model, cmds)

	if err == nil && len(p.errs) > 0 {
		err = <-p.errs // Drain a leftover error in case eventLoop crashed.
	}

	killed := p.externalCtx.Err() != nil || p.ctx.Err() != nil || err != nil
	if killed {
		if err == nil && p.externalCtx.Err() != nil {
			// Return also as context error the cancellation of an external context.
			// This is the context the user knows about and should be able to act on.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, p.externalCtx.Err())
		} else if err == nil && p.ctx.Err() != nil {
			// Return only that the program was killed (not the internal mechanism).
			// The user does not know or need to care about the internal program context.
			err = ErrProgramKilled
		} else {
			// Return that the program was killed and also the error that caused it.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, err)
		}
	} else {
		// Graceful shutdown of the program (not killed):
		// Ensure we rendered the final state of the model.
		p.render(model)
	}

	// Restore terminal state.
	p.shutdown(killed)

	return model, err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Program) Run() (returnModel Model, returnErr error) {
	if p.initialModel == nil {
		return nil, errors.New("bubbletea: InitialModel cannot be nil")
	}

	// Initialize context and teardown channel.
	p.handlers = channelHandlers{}
	cmds := make(chan Cmd)

	p.finished = make(chan struct{})
	defer func() {
		close(p.finished)
	}()

	defer p.cancel()

	if p.disableInput {
		p.input = nil
	} else if p.input == nil {
		p.input = os.Stdin
		if !term.IsTerminal(os.Stdin.Fd()) {
			ttyIn, _, err := OpenTTY()
			if err != nil {
				return p.initialModel, fmt.Errorf("bubbletea: error opening TTY: %w", err)
			}
			p.input = ttyIn
		}
	}

	// Handle signals.
	if !p.disableSignalHandler {
		p.handlers.add(p.handleSignals())
	}

	// Recover from panics.
	if !p.disableCatchPanics {
		defer func() {
			if r := recover(); r != nil {
				returnErr = fmt.Errorf("%w: %w", ErrProgramKilled, ErrProgramPanic)
				p.recoverFromPanic(r)
			}
		}()
	}

	// Check if output is a TTY before entering raw mode, hiding the cursor and
	// so on.
	if err := p.initTerminal(); err != nil {
		return p.initialModel, err
	}

	// Get the initial window size.
	width, height := p.width, p.height
	if p.ttyOutput != nil {
		// Set the initial size of the terminal.
		w, h, err := term.GetSize(p.ttyOutput.Fd())
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error getting terminal size: %w", err)
		}

		width, height = w, h
	}

	p.width, p.height = width, height
	resizeMsg := WindowSizeMsg{Width: p.width, Height: p.height}

	if p.renderer == nil {
		if p.disableRenderer {
			p.renderer = &nilRenderer{}
		} else {
			// If no renderer is set use the cursed one.
			r := newCursedRenderer(
				p.output,
				p.environ,
				p.width,
				p.height,
			)
			r.setLogger(p.logger)
			// XXX: This breaks many things especially when we want the output
			// to be compatible with terminals that are not necessary a TTY.
			// This was originally done to work around a Wish emulated-pty
			// issue where when a PTY session is detected, and we don't
			// allocate a real PTY, the terminal settings (Termios and WinCon)
			// don't change and the we end up working in cooked mode instead of
			// raw mode.
			mapNl := false // p.ttyInput == nil
			r.setOptimizations(p.useHardTabs, p.useBackspace, mapNl)
			p.renderer = r
		}
	}

	// Get the color profile and send it to the program.
	if p.profile == nil {
		cp := colorprofile.Detect(p.output, p.environ)
		p.profile = &cp
	}

	// Set the color profile on the renderer and send it to the program.
	p.renderer.setColorProfile(*p.profile)
	go p.Send(ColorProfileMsg{*p.profile})

	// Send the initial size to the program.
	go p.Send(resizeMsg)
	p.renderer.resize(resizeMsg.Width, resizeMsg.Height)

	// Send the environment variables used by the program.
	go p.Send(EnvMsg(p.environ))

	// Init the input reader and initial model.
	model := p.initialModel
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return model, err
		}
	}

	// Start the renderer.
	p.startRenderer()

	if !p.disableRenderer && shouldQuerySynchronizedOutput(p.environ) {
		// Query for synchronized updates support (mode 2026) and unicode core
		// (mode 2027). If the terminal supports it, the renderer will enable
		// it once we get the response.
		p.execute(ansi.RequestModeSynchronizedOutput +
			ansi.RequestModeUnicodeCore)
	}

	// Initialize the program.
	initCmd := model.Init()
	if initCmd != nil {
		ch := make(chan struct{})
		p.handlers.add(ch)

		go func() {
			defer close(ch)

			select {
			case cmds <- initCmd:
			case <-p.ctx.Done():
			}
		}()
	}

	// Render the initial view.
	p.render(model)

	// Handle resize events.
	p.handlers.add(p.handleResize())

	// Process commands.
	p.handlers.add(p.handleCommands(cmds))

	// Run event loop, handle updates and draw.
	var err error
	model, err = p.eventLoop(model, cmds)

	if err == nil && len(p.errs) > 0 {
		err = <-p.errs // Drain a leftover error in case eventLoop crashed.
	}

	killed := p.externalCtx.Err() != nil || p.ctx.Err() != nil || err != nil
	if killed {
		if err == nil && p.externalCtx.Err() != nil {
			// Return also as context error the cancellation of an external context.
			// This is the context the user knows about and should be able to act on.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, p.externalCtx.Err())
		} else if err == nil && p.ctx.Err() != nil {
			// Return only that the program was killed (not the internal mechanism).
			// The user does not know or need to care about the internal program context.
			err = ErrProgramKilled
		} else {
			// Return that the program was killed and also the error that caused it.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, err)
		}
	} else {
		// Graceful shutdown of the program (not killed):
		// Ensure we rendered the final state of the model.
		p.render(model)
	}

	// Restore terminal state.
	p.shutdown(killed)

	return model, err
}
```


---

### 🔹 Commit #16: `110a9191`
- **完整 Hash**: `110a91911314541601ff156fa96904350a4cd07f`
- **說明 (Ground Truth)**: fix(examples): add missing `WithWidth` to table example (#1598)
- **變更檔案數**: 1

#### 📄 檔案: `examples/table/main.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:38, E:34, A:1) ➔ After(N:39, E:35, A:1)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#CLI: main** `(CLI Entry)`
    └── ⚡ **run()**
        └── 🎯 [TRIGGERS] `main()`
+           └── 🟢 [CALLS] `table.WithWidth (External/Pkg)()` [新增因果]
            └── 🎯 [CALLS] `fmt.Println (External/Pkg)()`
            └── 🎯 [CALLS] `lipgloss.Color (External/Pkg)()`
            └── 🎯 [CALLS] `lipgloss.NormalBorder (External/Pkg)()`
            └── 🎯 [CALLS] `os.Exit (External/Pkg)()`
            └── 🎯 [CALLS] `s.Header.
		BorderStyle (External/Pkg)()`
            └── 🎯 [CALLS] `s.Header.
		BorderStyle(lipgloss.NormalBorder()).
		BorderForeground (External/Pkg)()`
            └── 🎯 [CALLS] `s.Header.
		BorderStyle(lipgloss.NormalBorder()).
		BorderForeground(lipgloss.Color("240")).
		BorderBottom (External/Pkg)()`
            └── 🎯 [CALLS] `s.Header.
		BorderStyle(lipgloss.NormalBorder()).
		BorderForeground(lipgloss.Color("240")).
		BorderBottom(true).
		Bold (External/Pkg)()`
            └── 🎯 [CALLS] `s.Selected.
		Foreground (External/Pkg)()`
            └── 🎯 [CALLS] `s.Selected.
		Foreground(lipgloss.Color("229")).
		Background (External/Pkg)()`
            └── 🎯 [CALLS] `s.Selected.
		Foreground(lipgloss.Color("229")).
		Background(lipgloss.Color("57")).
		Bold (External/Pkg)()`
            └── 🎯 [CALLS] `t.SetStyles (External/Pkg)()`
            └── 🎯 [CALLS] `table.DefaultStyles (External/Pkg)()`
            └── 🎯 [CALLS] `table.New (External/Pkg)()`
            └── 🎯 [CALLS] `table.WithColumns (External/Pkg)()`
            └── 🎯 [CALLS] `table.WithFocused (External/Pkg)()`
            └── 🎯 [CALLS] `table.WithHeight (External/Pkg)()`
            └── 🎯 [CALLS] `table.WithRows (External/Pkg)()`
            └── 🎯 [CALLS] `tea.NewProgram (External/Pkg)()`
            └── 🎯 [CALLS] `tea.NewProgram(m).Run (External/Pkg)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `table.WithWidth (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `main` ──[CALLS]──> `table.WithWidth (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `main()`
- **變更前簽章 (Before)**: `func main()` (L49~L184)
- **變更後簽章 (After)**: `func main()` (L49~L185)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func main() {
	columns := []table.Column{
		{Title: "Rank", Width: 4},
		{Title: "City", Width: 10},
		{Title: "Country", Width: 10},
		{Title: "Population", Width: 10},
	}

	rows := []table.Row{
		{"1", "Tokyo", "Japan", "37,274,000"},
		{"2", "Delhi", "India", "32,065,760"},
		{"3", "Shanghai", "China", "28,516,904"},
		{"4", "Dhaka", "Bangladesh", "22,478,116"},
		{"5", "São Paulo", "Brazil", "22,429,800"},
		{"6", "Mexico City", "Mexico", "22,085,140"},
		{"7", "Cairo", "Egypt", "21,750,020"},
		{"8", "Beijing", "China", "21,333,332"},
		{"9", "Mumbai", "India", "20,961,472"},
		{"10", "Osaka", "Japan", "19,059,856"},
		{"11", "Chongqing", "China", "16,874,740"},
		{"12", "Karachi", "Pakistan", "16,839,950"},
		{"13", "Istanbul", "Turkey", "15,636,243"},
		{"14", "Kinshasa", "DR Congo", "15,628,085"},
		{"15", "Lagos", "Nigeria", "15,387,639"},
		{"16", "Buenos Aires", "Argentina", "15,369,919"},
		{"17", "Kolkata", "India", "15,133,888"},
		{"18", "Manila", "Philippines", "14,406,059"},
		{"19", "Tianjin", "China", "14,011,828"},
		{"20", "Guangzhou", "China", "13,964,637"},
		{"21", "Rio De Janeiro", "Brazil", "13,634,274"},
		{"22", "Lahore", "Pakistan", "13,541,764"},
		{"23", "Bangalore", "India", "13,193,035"},
		{"24", "Shenzhen", "China", "12,831,330"},
		{"25", "Moscow", "Russia", "12,640,818"},
		{"26", "Chennai", "India", "11,503,293"},
		{"27", "Bogota", "Colombia", "11,344,312"},
		{"28", "Paris", "France", "11,142,303"},
		{"29", "Jakarta", "Indonesia", "11,074,811"},
		{"30", "Lima", "Peru", "11,044,607"},
		{"31", "Bangkok", "Thailand", "10,899,698"},
		{"32", "Hyderabad", "India", "10,534,418"},
		{"33", "Seoul", "South Korea", "9,975,709"},
		{"34", "Nagoya", "Japan", "9,571,596"},
		{"35", "London", "United Kingdom", "9,540,576"},
		{"36", "Chengdu", "China", "9,478,521"},
		{"37", "Nanjing", "China", "9,429,381"},
		{"38", "Tehran", "Iran", "9,381,546"},
		{"39", "Ho Chi Minh City", "Vietnam", "9,077,158"},
		{"40", "Luanda", "Angola", "8,952,496"},
		{"41", "Wuhan", "China", "8,591,611"},
		{"42", "Xi An Shaanxi", "China", "8,537,646"},
		{"43", "Ahmedabad", "India", "8,450,228"},
		{"44", "Kuala Lumpur", "Malaysia", "8,419,566"},
		{"45", "New York City", "United States", "8,177,020"},
		{"46", "Hangzhou", "China", "8,044,878"},
		{"47", "Surat", "India", "7,784,276"},
		{"48", "Suzhou", "China", "7,764,499"},
		{"49", "Hong Kong", "Hong Kong", "7,643,256"},
		{"50", "Riyadh", "Saudi Arabia", "7,538,200"},
		{"51", "Shenyang", "China", "7,527,975"},
		{"52", "Baghdad", "Iraq", "7,511,920"},
		{"53", "Dongguan", "China", "7,511,851"},
		{"54", "Foshan", "China", "7,497,263"},
		{"55", "Dar Es Salaam", "Tanzania", "7,404,689"},
		{"56", "Pune", "India", "6,987,077"},
		{"57", "Santiago", "Chile", "6,856,939"},
		{"58", "Madrid", "Spain", "6,713,557"},
		{"59", "Haerbin", "China", "6,665,951"},
		{"60", "Toronto", "Canada", "6,312,974"},
		{"61", "Belo Horizonte", "Brazil", "6,194,292"},
		{"62", "Khartoum", "Sudan", "6,160,327"},
		{"63", "Johannesburg", "South Africa", "6,065,354"},
		{"64", "Singapore", "Singapore", "6,039,577"},
		{"65", "Dalian", "China", "5,930,140"},
		{"66", "Qingdao", "China", "5,865,232"},
		{"67", "Zhengzhou", "China", "5,690,312"},
		{"68", "Ji Nan Shandong", "China", "5,663,015"},
		{"69", "Barcelona", "Spain", "5,658,472"},
		{"70", "Saint Petersburg", "Russia", "5,535,556"},
		{"71", "Abidjan", "Ivory Coast", "5,515,790"},
		{"72", "Yangon", "Myanmar", "5,514,454"},
		{"73", "Fukuoka", "Japan", "5,502,591"},
		{"74", "Alexandria", "Egypt", "5,483,605"},
		{"75", "Guadalajara", "Mexico", "5,339,583"},
		{"76", "Ankara", "Turkey", "5,309,690"},
		{"77", "Chittagong", "Bangladesh", "5,252,842"},
		{"78", "Addis Ababa", "Ethiopia", "5,227,794"},
		{"79", "Melbourne", "Australia", "5,150,766"},
		{"80", "Nairobi", "Kenya", "5,118,844"},
		{"81", "Hanoi", "Vietnam", "5,067,352"},
		{"82", "Sydney", "Australia", "5,056,571"},
		{"83", "Monterrey", "Mexico", "5,036,535"},
		{"84", "Changsha", "China", "4,809,887"},
		{"85", "Brasilia", "Brazil", "4,803,877"},
		{"86", "Cape Town", "South Africa", "4,800,954"},
		{"87", "Jiddah", "Saudi Arabia", "4,780,740"},
		{"88", "Urumqi", "China", "4,710,203"},
		{"89", "Kunming", "China", "4,657,381"},
		{"90", "Changchun", "China", "4,616,002"},
		{"91", "Hefei", "China", "4,496,456"},
		{"92", "Shantou", "China", "4,490,411"},
		{"93", "Xinbei", "Taiwan", "4,470,672"},
		{"94", "Kabul", "Afghanistan", "4,457,882"},
		{"95", "Ningbo", "China", "4,405,292"},
		{"96", "Tel Aviv", "Israel", "4,343,584"},
		{"97", "Yaounde", "Cameroon", "4,336,670"},
		{"98", "Rome", "Italy", "4,297,877"},
		{"99", "Shijiazhuang", "China", "4,285,135"},
		{"100", "Montreal", "Canada", "4,276,526"},
	}

	t := table.New(
		table.WithColumns(columns),
		table.WithRows(rows),
		table.WithFocused(true),
		table.WithHeight(7),
	)

	s := table.DefaultStyles()
	s.Header = s.Header.
		BorderStyle(lipgloss.NormalBorder()).
		BorderForeground(lipgloss.Color("240")).
		BorderBottom(true).
		Bold(false)
	s.Selected = s.Selected.
		Foreground(lipgloss.Color("229")).
		Background(lipgloss.Color("57")).
		Bold(false)
	t.SetStyles(s)

	m := model{t}
	if _, err := tea.NewProgram(m).Run(); err != nil {
		fmt.Println("Error running program:", err)
		os.Exit(1)
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func main() {
	columns := []table.Column{
		{Title: "Rank", Width: 4},
		{Title: "City", Width: 10},
		{Title: "Country", Width: 10},
		{Title: "Population", Width: 10},
	}

	rows := []table.Row{
		{"1", "Tokyo", "Japan", "37,274,000"},
		{"2", "Delhi", "India", "32,065,760"},
		{"3", "Shanghai", "China", "28,516,904"},
		{"4", "Dhaka", "Bangladesh", "22,478,116"},
		{"5", "São Paulo", "Brazil", "22,429,800"},
		{"6", "Mexico City", "Mexico", "22,085,140"},
		{"7", "Cairo", "Egypt", "21,750,020"},
		{"8", "Beijing", "China", "21,333,332"},
		{"9", "Mumbai", "India", "20,961,472"},
		{"10", "Osaka", "Japan", "19,059,856"},
		{"11", "Chongqing", "China", "16,874,740"},
		{"12", "Karachi", "Pakistan", "16,839,950"},
		{"13", "Istanbul", "Turkey", "15,636,243"},
		{"14", "Kinshasa", "DR Congo", "15,628,085"},
		{"15", "Lagos", "Nigeria", "15,387,639"},
		{"16", "Buenos Aires", "Argentina", "15,369,919"},
		{"17", "Kolkata", "India", "15,133,888"},
		{"18", "Manila", "Philippines", "14,406,059"},
		{"19", "Tianjin", "China", "14,011,828"},
		{"20", "Guangzhou", "China", "13,964,637"},
		{"21", "Rio De Janeiro", "Brazil", "13,634,274"},
		{"22", "Lahore", "Pakistan", "13,541,764"},
		{"23", "Bangalore", "India", "13,193,035"},
		{"24", "Shenzhen", "China", "12,831,330"},
		{"25", "Moscow", "Russia", "12,640,818"},
		{"26", "Chennai", "India", "11,503,293"},
		{"27", "Bogota", "Colombia", "11,344,312"},
		{"28", "Paris", "France", "11,142,303"},
		{"29", "Jakarta", "Indonesia", "11,074,811"},
		{"30", "Lima", "Peru", "11,044,607"},
		{"31", "Bangkok", "Thailand", "10,899,698"},
		{"32", "Hyderabad", "India", "10,534,418"},
		{"33", "Seoul", "South Korea", "9,975,709"},
		{"34", "Nagoya", "Japan", "9,571,596"},
		{"35", "London", "United Kingdom", "9,540,576"},
		{"36", "Chengdu", "China", "9,478,521"},
		{"37", "Nanjing", "China", "9,429,381"},
		{"38", "Tehran", "Iran", "9,381,546"},
		{"39", "Ho Chi Minh City", "Vietnam", "9,077,158"},
		{"40", "Luanda", "Angola", "8,952,496"},
		{"41", "Wuhan", "China", "8,591,611"},
		{"42", "Xi An Shaanxi", "China", "8,537,646"},
		{"43", "Ahmedabad", "India", "8,450,228"},
		{"44", "Kuala Lumpur", "Malaysia", "8,419,566"},
		{"45", "New York City", "United States", "8,177,020"},
		{"46", "Hangzhou", "China", "8,044,878"},
		{"47", "Surat", "India", "7,784,276"},
		{"48", "Suzhou", "China", "7,764,499"},
		{"49", "Hong Kong", "Hong Kong", "7,643,256"},
		{"50", "Riyadh", "Saudi Arabia", "7,538,200"},
		{"51", "Shenyang", "China", "7,527,975"},
		{"52", "Baghdad", "Iraq", "7,511,920"},
		{"53", "Dongguan", "China", "7,511,851"},
		{"54", "Foshan", "China", "7,497,263"},
		{"55", "Dar Es Salaam", "Tanzania", "7,404,689"},
		{"56", "Pune", "India", "6,987,077"},
		{"57", "Santiago", "Chile", "6,856,939"},
		{"58", "Madrid", "Spain", "6,713,557"},
		{"59", "Haerbin", "China", "6,665,951"},
		{"60", "Toronto", "Canada", "6,312,974"},
		{"61", "Belo Horizonte", "Brazil", "6,194,292"},
		{"62", "Khartoum", "Sudan", "6,160,327"},
		{"63", "Johannesburg", "South Africa", "6,065,354"},
		{"64", "Singapore", "Singapore", "6,039,577"},
		{"65", "Dalian", "China", "5,930,140"},
		{"66", "Qingdao", "China", "5,865,232"},
		{"67", "Zhengzhou", "China", "5,690,312"},
		{"68", "Ji Nan Shandong", "China", "5,663,015"},
		{"69", "Barcelona", "Spain", "5,658,472"},
		{"70", "Saint Petersburg", "Russia", "5,535,556"},
		{"71", "Abidjan", "Ivory Coast", "5,515,790"},
		{"72", "Yangon", "Myanmar", "5,514,454"},
		{"73", "Fukuoka", "Japan", "5,502,591"},
		{"74", "Alexandria", "Egypt", "5,483,605"},
		{"75", "Guadalajara", "Mexico", "5,339,583"},
		{"76", "Ankara", "Turkey", "5,309,690"},
		{"77", "Chittagong", "Bangladesh", "5,252,842"},
		{"78", "Addis Ababa", "Ethiopia", "5,227,794"},
		{"79", "Melbourne", "Australia", "5,150,766"},
		{"80", "Nairobi", "Kenya", "5,118,844"},
		{"81", "Hanoi", "Vietnam", "5,067,352"},
		{"82", "Sydney", "Australia", "5,056,571"},
		{"83", "Monterrey", "Mexico", "5,036,535"},
		{"84", "Changsha", "China", "4,809,887"},
		{"85", "Brasilia", "Brazil", "4,803,877"},
		{"86", "Cape Town", "South Africa", "4,800,954"},
		{"87", "Jiddah", "Saudi Arabia", "4,780,740"},
		{"88", "Urumqi", "China", "4,710,203"},
		{"89", "Kunming", "China", "4,657,381"},
		{"90", "Changchun", "China", "4,616,002"},
		{"91", "Hefei", "China", "4,496,456"},
		{"92", "Shantou", "China", "4,490,411"},
		{"93", "Xinbei", "Taiwan", "4,470,672"},
		{"94", "Kabul", "Afghanistan", "4,457,882"},
		{"95", "Ningbo", "China", "4,405,292"},
		{"96", "Tel Aviv", "Israel", "4,343,584"},
		{"97", "Yaounde", "Cameroon", "4,336,670"},
		{"98", "Rome", "Italy", "4,297,877"},
		{"99", "Shijiazhuang", "China", "4,285,135"},
		{"100", "Montreal", "Canada", "4,276,526"},
	}

	t := table.New(
		table.WithColumns(columns),
		table.WithRows(rows),
		table.WithFocused(true),
		table.WithHeight(7),
		table.WithWidth(42),
	)

	s := table.DefaultStyles()
	s.Header = s.Header.
		BorderStyle(lipgloss.NormalBorder()).
		BorderForeground(lipgloss.Color("240")).
		BorderBottom(true).
		Bold(false)
	s.Selected = s.Selected.
		Foreground(lipgloss.Color("229")).
		Background(lipgloss.Color("57")).
		Bold(false)
	t.SetStyles(s)

	m := model{t}
	if _, err := tea.NewProgram(m).Run(); err != nil {
		fmt.Println("Error running program:", err)
		os.Exit(1)
	}
}
```


---

### 🔹 Commit #17: `1ff0a470`
- **完整 Hash**: `1ff0a470e0d938dc6e8a1b3c659f98a73d042df8`
- **說明 (Ground Truth)**: fix(tea): don't query for synchronized output if the renderer is disabled
- **變更檔案數**: 1

#### 📄 檔案: `tea.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:154, E:204, A:0) ➔ After(N:154, E:204, A:0)
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

### 🔹 函式: `Program.Run()`
- **變更前簽章 (Before)**: `func Program.Run()` (L971~L1152)
- **變更後簽章 (After)**: `func Program.Run()` (L971~L1152)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Program) Run() (returnModel Model, returnErr error) {
	if p.initialModel == nil {
		return nil, errors.New("bubbletea: InitialModel cannot be nil")
	}

	// Initialize context and teardown channel.
	p.handlers = channelHandlers{}
	cmds := make(chan Cmd)

	p.finished = make(chan struct{})
	defer func() {
		close(p.finished)
	}()

	defer p.cancel()

	if p.disableInput {
		p.input = nil
	} else if p.input == nil {
		// Always open the TTY for input.
		ttyIn, _, err := OpenTTY()
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error opening TTY: %w", err)
		}
		p.input = ttyIn
	}

	// Handle signals.
	if !p.disableSignalHandler {
		p.handlers.add(p.handleSignals())
	}

	// Recover from panics.
	if !p.disableCatchPanics {
		defer func() {
			if r := recover(); r != nil {
				returnErr = fmt.Errorf("%w: %w", ErrProgramKilled, ErrProgramPanic)
				p.recoverFromPanic(r)
			}
		}()
	}

	// Check if output is a TTY before entering raw mode, hiding the cursor and
	// so on.
	if err := p.initTerminal(); err != nil {
		return p.initialModel, err
	}

	// Get the initial window size.
	width, height := p.width, p.height
	if p.ttyOutput != nil {
		// Set the initial size of the terminal.
		w, h, err := term.GetSize(p.ttyOutput.Fd())
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error getting terminal size: %w", err)
		}

		width, height = w, h
	}

	p.width, p.height = width, height
	resizeMsg := WindowSizeMsg{Width: p.width, Height: p.height}

	if p.renderer == nil {
		if p.disableRenderer {
			p.renderer = &nilRenderer{}
		} else {
			// If no renderer is set use the cursed one.
			r := newCursedRenderer(
				p.output,
				p.environ,
				p.width,
				p.height,
			)
			r.setLogger(p.logger)
			// XXX: This breaks many things especially when we want the output
			// to be compatible with terminals that are not necessary a TTY.
			// This was originally done to work around a Wish emulated-pty
			// issue where when a PTY session is detected, and we don't
			// allocate a real PTY, the terminal settings (Termios and WinCon)
			// don't change and the we end up working in cooked mode instead of
			// raw mode.
			mapNl := false // p.ttyInput == nil
			r.setOptimizations(p.useHardTabs, p.useBackspace, mapNl)
			p.renderer = r
		}
	}

	// Get the color profile and send it to the program.
	if p.profile == nil {
		cp := colorprofile.Detect(p.output, p.environ)
		p.profile = &cp
	}

	// Set the color profile on the renderer and send it to the program.
	p.renderer.setColorProfile(*p.profile)
	go p.Send(ColorProfileMsg{*p.profile})

	// Send the initial size to the program.
	go p.Send(resizeMsg)
	p.renderer.resize(resizeMsg.Width, resizeMsg.Height)

	// Send the environment variables used by the program.
	go p.Send(EnvMsg(p.environ))

	// Init the input reader and initial model.
	model := p.initialModel
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return model, err
		}
	}

	// Start the renderer.
	p.startRenderer()

	if shouldQuerySynchronizedOutput(p.environ) {
		// Query for synchronized updates support (mode 2026) and unicode core
		// (mode 2027). If the terminal supports it, the renderer will enable
		// it once we get the response.
		p.execute(ansi.RequestModeSynchronizedOutput +
			ansi.RequestModeUnicodeCore)
	}

	// Initialize the program.
	initCmd := model.Init()
	if initCmd != nil {
		ch := make(chan struct{})
		p.handlers.add(ch)

		go func() {
			defer close(ch)

			select {
			case cmds <- initCmd:
			case <-p.ctx.Done():
			}
		}()
	}

	// Render the initial view.
	p.render(model)

	// Handle resize events.
	p.handlers.add(p.handleResize())

	// Process commands.
	p.handlers.add(p.handleCommands(cmds))

	// Run event loop, handle updates and draw.
	var err error
	model, err = p.eventLoop(model, cmds)

	if err == nil && len(p.errs) > 0 {
		err = <-p.errs // Drain a leftover error in case eventLoop crashed.
	}

	killed := p.externalCtx.Err() != nil || p.ctx.Err() != nil || err != nil
	if killed {
		if err == nil && p.externalCtx.Err() != nil {
			// Return also as context error the cancellation of an external context.
			// This is the context the user knows about and should be able to act on.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, p.externalCtx.Err())
		} else if err == nil && p.ctx.Err() != nil {
			// Return only that the program was killed (not the internal mechanism).
			// The user does not know or need to care about the internal program context.
			err = ErrProgramKilled
		} else {
			// Return that the program was killed and also the error that caused it.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, err)
		}
	} else {
		// Graceful shutdown of the program (not killed):
		// Ensure we rendered the final state of the model.
		p.render(model)
	}

	// Restore terminal state.
	p.shutdown(killed)

	return model, err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Program) Run() (returnModel Model, returnErr error) {
	if p.initialModel == nil {
		return nil, errors.New("bubbletea: InitialModel cannot be nil")
	}

	// Initialize context and teardown channel.
	p.handlers = channelHandlers{}
	cmds := make(chan Cmd)

	p.finished = make(chan struct{})
	defer func() {
		close(p.finished)
	}()

	defer p.cancel()

	if p.disableInput {
		p.input = nil
	} else if p.input == nil {
		// Always open the TTY for input.
		ttyIn, _, err := OpenTTY()
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error opening TTY: %w", err)
		}
		p.input = ttyIn
	}

	// Handle signals.
	if !p.disableSignalHandler {
		p.handlers.add(p.handleSignals())
	}

	// Recover from panics.
	if !p.disableCatchPanics {
		defer func() {
			if r := recover(); r != nil {
				returnErr = fmt.Errorf("%w: %w", ErrProgramKilled, ErrProgramPanic)
				p.recoverFromPanic(r)
			}
		}()
	}

	// Check if output is a TTY before entering raw mode, hiding the cursor and
	// so on.
	if err := p.initTerminal(); err != nil {
		return p.initialModel, err
	}

	// Get the initial window size.
	width, height := p.width, p.height
	if p.ttyOutput != nil {
		// Set the initial size of the terminal.
		w, h, err := term.GetSize(p.ttyOutput.Fd())
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error getting terminal size: %w", err)
		}

		width, height = w, h
	}

	p.width, p.height = width, height
	resizeMsg := WindowSizeMsg{Width: p.width, Height: p.height}

	if p.renderer == nil {
		if p.disableRenderer {
			p.renderer = &nilRenderer{}
		} else {
			// If no renderer is set use the cursed one.
			r := newCursedRenderer(
				p.output,
				p.environ,
				p.width,
				p.height,
			)
			r.setLogger(p.logger)
			// XXX: This breaks many things especially when we want the output
			// to be compatible with terminals that are not necessary a TTY.
			// This was originally done to work around a Wish emulated-pty
			// issue where when a PTY session is detected, and we don't
			// allocate a real PTY, the terminal settings (Termios and WinCon)
			// don't change and the we end up working in cooked mode instead of
			// raw mode.
			mapNl := false // p.ttyInput == nil
			r.setOptimizations(p.useHardTabs, p.useBackspace, mapNl)
			p.renderer = r
		}
	}

	// Get the color profile and send it to the program.
	if p.profile == nil {
		cp := colorprofile.Detect(p.output, p.environ)
		p.profile = &cp
	}

	// Set the color profile on the renderer and send it to the program.
	p.renderer.setColorProfile(*p.profile)
	go p.Send(ColorProfileMsg{*p.profile})

	// Send the initial size to the program.
	go p.Send(resizeMsg)
	p.renderer.resize(resizeMsg.Width, resizeMsg.Height)

	// Send the environment variables used by the program.
	go p.Send(EnvMsg(p.environ))

	// Init the input reader and initial model.
	model := p.initialModel
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return model, err
		}
	}

	// Start the renderer.
	p.startRenderer()

	if !p.disableRenderer && shouldQuerySynchronizedOutput(p.environ) {
		// Query for synchronized updates support (mode 2026) and unicode core
		// (mode 2027). If the terminal supports it, the renderer will enable
		// it once we get the response.
		p.execute(ansi.RequestModeSynchronizedOutput +
			ansi.RequestModeUnicodeCore)
	}

	// Initialize the program.
	initCmd := model.Init()
	if initCmd != nil {
		ch := make(chan struct{})
		p.handlers.add(ch)

		go func() {
			defer close(ch)

			select {
			case cmds <- initCmd:
			case <-p.ctx.Done():
			}
		}()
	}

	// Render the initial view.
	p.render(model)

	// Handle resize events.
	p.handlers.add(p.handleResize())

	// Process commands.
	p.handlers.add(p.handleCommands(cmds))

	// Run event loop, handle updates and draw.
	var err error
	model, err = p.eventLoop(model, cmds)

	if err == nil && len(p.errs) > 0 {
		err = <-p.errs // Drain a leftover error in case eventLoop crashed.
	}

	killed := p.externalCtx.Err() != nil || p.ctx.Err() != nil || err != nil
	if killed {
		if err == nil && p.externalCtx.Err() != nil {
			// Return also as context error the cancellation of an external context.
			// This is the context the user knows about and should be able to act on.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, p.externalCtx.Err())
		} else if err == nil && p.ctx.Err() != nil {
			// Return only that the program was killed (not the internal mechanism).
			// The user does not know or need to care about the internal program context.
			err = ErrProgramKilled
		} else {
			// Return that the program was killed and also the error that caused it.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, err)
		}
	} else {
		// Graceful shutdown of the program (not killed):
		// Ensure we rendered the final state of the model.
		p.render(model)
	}

	// Restore terminal state.
	p.shutdown(killed)

	return model, err
}
```


---

### 🔹 Commit #18: `faa0b9c3`
- **完整 Hash**: `faa0b9c36ba2d2ed00d8b9e16b8ff61bd7f28e0b`
- **說明 (Ground Truth)**: fix: lint issues
- **變更檔案數**: 3

#### 📄 檔案: `commands.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:17, E:15, A:0) ➔ After(N:17, E:15, A:0)
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

#### 📄 檔案: `cursed_renderer.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:107, E:156, A:0) ➔ After(N:107, E:157, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `cursedRenderer.insertAbove` ──[CALLS]──> `fmt.Errorf (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `cursedRenderer.insertAbove()`
- **變更前簽章 (Before)**: `func cursedRenderer.insertAbove(str string)` (L700~L752)
- **變更後簽章 (After)**: `func cursedRenderer.insertAbove(str string)` (L700~L756)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *cursedRenderer) insertAbove(str string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if len(str) == 0 {
		return nil
	}

	var sb strings.Builder
	w, h := s.cellbuf.Width(), s.cellbuf.Height()
	_, y := s.scr.Position()

	// We need to scroll the screen up by the number of lines in the queue.
	sb.WriteByte('\r')
	down := h - y - 1
	if down > 0 {
		sb.WriteString(ansi.CursorDown(down))
	}

	lines := strings.Split(str, "\n")
	offset := len(lines)
	for _, line := range lines {
		lineWidth := ansi.StringWidth(line)
		if w > 0 && lineWidth > w {
			offset += (lineWidth / w)
		}
	}

	// Scroll the screen up by the offset to make room for the new lines.
	sb.WriteString(strings.Repeat("\n", offset))

	// XXX: Now go to the top of the screen, insert new lines, and write
	// the queued strings. It is important to use [Screen.moveCursor]
	// instead of [Screen.move] because we don't want to perform any checks
	// on the cursor position.
	up := offset + h - 1
	sb.WriteString(ansi.CursorUp(up))
	sb.WriteString(ansi.InsertLine(offset))
	for _, line := range lines {
		sb.WriteString(line)
		sb.WriteString(ansi.EraseLineRight)
		sb.WriteString("\r\n")
	}

	s.scr.SetPosition(0, 0)

	if s.logger != nil {
		s.logger.Printf("insert above: %q", sb.String())
	}

	_, err := io.WriteString(s.w, sb.String())
	return err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *cursedRenderer) insertAbove(str string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if len(str) == 0 {
		return nil
	}

	var sb strings.Builder
	w, h := s.cellbuf.Width(), s.cellbuf.Height()
	_, y := s.scr.Position()

	// We need to scroll the screen up by the number of lines in the queue.
	sb.WriteByte('\r')
	down := h - y - 1
	if down > 0 {
		sb.WriteString(ansi.CursorDown(down))
	}

	lines := strings.Split(str, "\n")
	offset := len(lines)
	for _, line := range lines {
		lineWidth := ansi.StringWidth(line)
		if w > 0 && lineWidth > w {
			offset += (lineWidth / w)
		}
	}

	// Scroll the screen up by the offset to make room for the new lines.
	sb.WriteString(strings.Repeat("\n", offset))

	// XXX: Now go to the top of the screen, insert new lines, and write
	// the queued strings. It is important to use [Screen.moveCursor]
	// instead of [Screen.move] because we don't want to perform any checks
	// on the cursor position.
	up := offset + h - 1
	sb.WriteString(ansi.CursorUp(up))
	sb.WriteString(ansi.InsertLine(offset))
	for _, line := range lines {
		sb.WriteString(line)
		sb.WriteString(ansi.EraseLineRight)
		sb.WriteString("\r\n")
	}

	s.scr.SetPosition(0, 0)

	if s.logger != nil {
		s.logger.Printf("insert above: %q", sb.String())
	}

	_, err := io.WriteString(s.w, sb.String())
	if err != nil {
		return fmt.Errorf("bubbletea: error writing insert above to the writer: %w", err)
	}

	return nil
}
```


#### 📄 檔案: `tea.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:154, E:204, A:0) ➔ After(N:154, E:204, A:0)
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

### 🔹 Commit #19: `b3661ce3`
- **完整 Hash**: `b3661ce3d63f003545323b721212562c28647e0f`
- **說明 (Ground Truth)**: fix: always open the TTY for input
- **變更檔案數**: 1

#### 📄 檔案: `tea.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:153, E:203, A:0) ➔ After(N:154, E:204, A:0)
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
  • + [新增節點] `OpenTTY (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Program.Run` ──[CALLS]──> `OpenTTY (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Program.Run()`
- **變更前簽章 (Before)**: `func Program.Run()` (L964~L1138)
- **變更後簽章 (After)**: `func Program.Run()` (L964~L1143)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Program) Run() (returnModel Model, returnErr error) {
	if p.initialModel == nil {
		return nil, errors.New("bubbletea: InitialModel cannot be nil")
	}

	// Initialize context and teardown channel.
	p.handlers = channelHandlers{}
	cmds := make(chan Cmd)

	p.finished = make(chan struct{})
	defer func() {
		close(p.finished)
	}()

	defer p.cancel()

	if p.disableInput {
		p.input = nil
	} else if p.input == nil {
		p.input = os.Stdin
	}

	// Handle signals.
	if !p.disableSignalHandler {
		p.handlers.add(p.handleSignals())
	}

	// Recover from panics.
	if !p.disableCatchPanics {
		defer func() {
			if r := recover(); r != nil {
				returnErr = fmt.Errorf("%w: %w", ErrProgramKilled, ErrProgramPanic)
				p.recoverFromPanic(r)
			}
		}()
	}

	// Check if output is a TTY before entering raw mode, hiding the cursor and
	// so on.
	if err := p.initTerminal(); err != nil {
		return p.initialModel, err
	}

	// Get the initial window size.
	width, height := p.width, p.height
	if p.ttyOutput != nil {
		// Set the initial size of the terminal.
		w, h, err := term.GetSize(p.ttyOutput.Fd())
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error getting terminal size: %w", err)
		}

		width, height = w, h
	}

	p.width, p.height = width, height
	resizeMsg := WindowSizeMsg{Width: p.width, Height: p.height}

	if p.renderer == nil {
		if p.disableRenderer {
			p.renderer = &nilRenderer{}
		} else {
			// If no renderer is set use the cursed one.
			r := newCursedRenderer(
				p.output,
				p.environ,
				p.width,
				p.height,
			)
			r.setLogger(p.logger)
			// XXX: This breaks many things especially when we want the output
			// to be compatible with terminals that are not necessary a TTY.
			// This was originally done to work around a Wish emulated-pty
			// issue where when a PTY session is detected, and we don't
			// allocate a real PTY, the terminal settings (Termios and WinCon)
			// don't change and the we end up working in cooked mode instead of
			// raw mode.
			mapNl := false // p.ttyInput == nil
			r.setOptimizations(p.useHardTabs, p.useBackspace, mapNl)
			p.renderer = r
		}
	}

	// Get the color profile and send it to the program.
	if p.profile == nil {
		cp := colorprofile.Detect(p.output, p.environ)
		p.profile = &cp
	}

	// Set the color profile on the renderer and send it to the program.
	p.renderer.setColorProfile(*p.profile)
	go p.Send(ColorProfileMsg{*p.profile})

	// Send the initial size to the program.
	go p.Send(resizeMsg)
	p.renderer.resize(resizeMsg.Width, resizeMsg.Height)

	// Send the environment variables used by the program.
	go p.Send(EnvMsg(p.environ))

	// Init the input reader and initial model.
	model := p.initialModel
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return model, err
		}
	}

	// Start the renderer.
	p.startRenderer()

	if shouldQuerySynchronizedOutput(p.environ) {
		// Query for synchronized updates support (mode 2026). If the terminal
		// supports it, the renderer will enable it once we get the response.
		p.execute(ansi.RequestModeSynchronizedOutput)
	}

	// Initialize the program.
	initCmd := model.Init()
	if initCmd != nil {
		ch := make(chan struct{})
		p.handlers.add(ch)

		go func() {
			defer close(ch)

			select {
			case cmds <- initCmd:
			case <-p.ctx.Done():
			}
		}()
	}

	// Render the initial view.
	p.render(model)

	// Handle resize events.
	p.handlers.add(p.handleResize())

	// Process commands.
	p.handlers.add(p.handleCommands(cmds))

	// Run event loop, handle updates and draw.
	var err error
	model, err = p.eventLoop(model, cmds)

	if err == nil && len(p.errs) > 0 {
		err = <-p.errs // Drain a leftover error in case eventLoop crashed.
	}

	killed := p.externalCtx.Err() != nil || p.ctx.Err() != nil || err != nil
	if killed {
		if err == nil && p.externalCtx.Err() != nil {
			// Return also as context error the cancellation of an external context.
			// This is the context the user knows about and should be able to act on.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, p.externalCtx.Err())
		} else if err == nil && p.ctx.Err() != nil {
			// Return only that the program was killed (not the internal mechanism).
			// The user does not know or need to care about the internal program context.
			err = ErrProgramKilled
		} else {
			// Return that the program was killed and also the error that caused it.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, err)
		}
	} else {
		// Graceful shutdown of the program (not killed):
		// Ensure we rendered the final state of the model.
		p.render(model)
	}

	// Restore terminal state.
	p.shutdown(killed)

	return model, err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Program) Run() (returnModel Model, returnErr error) {
	if p.initialModel == nil {
		return nil, errors.New("bubbletea: InitialModel cannot be nil")
	}

	// Initialize context and teardown channel.
	p.handlers = channelHandlers{}
	cmds := make(chan Cmd)

	p.finished = make(chan struct{})
	defer func() {
		close(p.finished)
	}()

	defer p.cancel()

	if p.disableInput {
		p.input = nil
	} else if p.input == nil {
		// Always open the TTY for input.
		ttyIn, _, err := OpenTTY()
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error opening TTY: %w", err)
		}
		p.input = ttyIn
	}

	// Handle signals.
	if !p.disableSignalHandler {
		p.handlers.add(p.handleSignals())
	}

	// Recover from panics.
	if !p.disableCatchPanics {
		defer func() {
			if r := recover(); r != nil {
				returnErr = fmt.Errorf("%w: %w", ErrProgramKilled, ErrProgramPanic)
				p.recoverFromPanic(r)
			}
		}()
	}

	// Check if output is a TTY before entering raw mode, hiding the cursor and
	// so on.
	if err := p.initTerminal(); err != nil {
		return p.initialModel, err
	}

	// Get the initial window size.
	width, height := p.width, p.height
	if p.ttyOutput != nil {
		// Set the initial size of the terminal.
		w, h, err := term.GetSize(p.ttyOutput.Fd())
		if err != nil {
			return p.initialModel, fmt.Errorf("bubbletea: error getting terminal size: %w", err)
		}

		width, height = w, h
	}

	p.width, p.height = width, height
	resizeMsg := WindowSizeMsg{Width: p.width, Height: p.height}

	if p.renderer == nil {
		if p.disableRenderer {
			p.renderer = &nilRenderer{}
		} else {
			// If no renderer is set use the cursed one.
			r := newCursedRenderer(
				p.output,
				p.environ,
				p.width,
				p.height,
			)
			r.setLogger(p.logger)
			// XXX: This breaks many things especially when we want the output
			// to be compatible with terminals that are not necessary a TTY.
			// This was originally done to work around a Wish emulated-pty
			// issue where when a PTY session is detected, and we don't
			// allocate a real PTY, the terminal settings (Termios and WinCon)
			// don't change and the we end up working in cooked mode instead of
			// raw mode.
			mapNl := false // p.ttyInput == nil
			r.setOptimizations(p.useHardTabs, p.useBackspace, mapNl)
			p.renderer = r
		}
	}

	// Get the color profile and send it to the program.
	if p.profile == nil {
		cp := colorprofile.Detect(p.output, p.environ)
		p.profile = &cp
	}

	// Set the color profile on the renderer and send it to the program.
	p.renderer.setColorProfile(*p.profile)
	go p.Send(ColorProfileMsg{*p.profile})

	// Send the initial size to the program.
	go p.Send(resizeMsg)
	p.renderer.resize(resizeMsg.Width, resizeMsg.Height)

	// Send the environment variables used by the program.
	go p.Send(EnvMsg(p.environ))

	// Init the input reader and initial model.
	model := p.initialModel
	if p.input != nil {
		if err := p.initInputReader(false); err != nil {
			return model, err
		}
	}

	// Start the renderer.
	p.startRenderer()

	if shouldQuerySynchronizedOutput(p.environ) {
		// Query for synchronized updates support (mode 2026). If the terminal
		// supports it, the renderer will enable it once we get the response.
		p.execute(ansi.RequestModeSynchronizedOutput)
	}

	// Initialize the program.
	initCmd := model.Init()
	if initCmd != nil {
		ch := make(chan struct{})
		p.handlers.add(ch)

		go func() {
			defer close(ch)

			select {
			case cmds <- initCmd:
			case <-p.ctx.Done():
			}
		}()
	}

	// Render the initial view.
	p.render(model)

	// Handle resize events.
	p.handlers.add(p.handleResize())

	// Process commands.
	p.handlers.add(p.handleCommands(cmds))

	// Run event loop, handle updates and draw.
	var err error
	model, err = p.eventLoop(model, cmds)

	if err == nil && len(p.errs) > 0 {
		err = <-p.errs // Drain a leftover error in case eventLoop crashed.
	}

	killed := p.externalCtx.Err() != nil || p.ctx.Err() != nil || err != nil
	if killed {
		if err == nil && p.externalCtx.Err() != nil {
			// Return also as context error the cancellation of an external context.
			// This is the context the user knows about and should be able to act on.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, p.externalCtx.Err())
		} else if err == nil && p.ctx.Err() != nil {
			// Return only that the program was killed (not the internal mechanism).
			// The user does not know or need to care about the internal program context.
			err = ErrProgramKilled
		} else {
			// Return that the program was killed and also the error that caused it.
			err = fmt.Errorf("%w: %w", ErrProgramKilled, err)
		}
	} else {
		// Graceful shutdown of the program (not killed):
		// Ensure we rendered the final state of the model.
		p.render(model)
	}

	// Restore terminal state.
	p.shutdown(killed)

	return model, err
}
```


---

### 🔹 Commit #20: `6595041d`
- **完整 Hash**: `6595041da277654876da2e5458eeed687ba4687c`
- **說明 (Ground Truth)**: fix(renderer): no need to enable both modifyOtherKeys protocols
- **變更檔案數**: 1

#### 📄 檔案: `cursed_renderer.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:106, E:153, A:0) ➔ After(N:106, E:153, A:0)
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

### 🔹 函式: `cursedRenderer.flush()`
- **變更前簽章 (Before)**: `func cursedRenderer.flush(closing bool)` (L252~L570)
- **變更後簽章 (After)**: `func cursedRenderer.flush(closing bool)` (L251~L568)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *cursedRenderer) flush(closing bool) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	view := s.view
	frameArea := uv.Rect(0, 0, s.width, s.height)
	if len(view.Content) == 0 {
		// If the component is nil, we should clear the screen buffer.
		frameArea.Max.Y = 0
	}

	content := uv.NewStyledString(view.Content)
	if !view.AltScreen {
		// We need to resizes the screen based on the frame height and
		// terminal width. This is because the frame height can change based on
		// the content of the frame. For example, if the frame contains a list
		// of items, the height of the frame will be the number of items in the
		// list. This is different from the alt screen buffer, which has a
		// fixed height and width.
		frameHeight := content.Height()
		if frameHeight != frameArea.Dy() {
			frameArea.Max.Y = frameHeight
		}
	}

	if !s.starting && !closing && s.lastView != nil && viewEquals(s.lastView, &view) && frameArea == s.cellbuf.Bounds() {
		// No changes, nothing to do.
		return nil
	}

	// We're no longer starting.
	s.starting = false

	if frameArea != s.cellbuf.Bounds() {
		s.scr.Erase() // Force a full redraw to avoid artifacts.

		// We need to reset the touched lines buffer to match the new height.
		s.cellbuf.Touched = nil

		// Resize the screen buffer to match the frame area. This is necessary
		// to ensure that the screen buffer is the same size as the frame area
		// and to avoid rendering issues when the frame area is smaller than
		// the screen buffer.
		s.cellbuf.Resize(frameArea.Dx(), frameArea.Dy())
	}

	// Clear our screen buffer before copying the new frame into it to ensure
	// we erase any old content.
	s.cellbuf.Clear()
	content.Draw(s.cellbuf, s.cellbuf.Bounds())

	// If the frame height is greater than the screen height, we drop the
	// lines from the top of the buffer.
	if frameHeight := frameArea.Dy(); frameHeight > s.height {
		s.cellbuf.Lines = s.cellbuf.Lines[frameHeight-s.height:]
	}

	// Alt screen mode.
	shouldUpdateAltScreen := (s.lastView == nil && view.AltScreen) || (s.lastView != nil && s.lastView.AltScreen != view.AltScreen)
	if shouldUpdateAltScreen {
		// We want to enter/exit altscreen mode but defer writing the actual
		// sequences until we flush the rest of the updates. This is because we
		// control the cursor visibility and we need to ensure that happens
		// after entering/exiting alt screen mode. Some terminals have
		// different cursor visibility states for main and alt screen modes and
		// this ensures we handle that correctly.
		enableAltScreen(s, view.AltScreen, false)
	}

	// bracketed paste mode.
	if s.lastView == nil || view.DisableBracketedPasteMode != s.lastView.DisableBracketedPasteMode {
		if !view.DisableBracketedPasteMode {
			_, _ = s.scr.WriteString(ansi.SetModeBracketedPaste)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeBracketedPaste)
		}
	}

	// report focus events mode.
	if s.lastView == nil || s.lastView.ReportFocus != view.ReportFocus {
		if view.ReportFocus {
			_, _ = s.scr.WriteString(ansi.SetModeFocusEvent)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeFocusEvent)
		}
	}

	// mouse events mode.
	if s.lastView == nil || view.MouseMode != s.lastView.MouseMode {
		switch view.MouseMode {
		case MouseModeNone:
			if s.lastView != nil && s.lastView.MouseMode != MouseModeNone {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent +
					ansi.ResetModeMouseAnyEvent +
					ansi.ResetModeMouseExtSgr)
			}
		case MouseModeCellMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeAllMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseAnyEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseButtonEvent + ansi.SetModeMouseExtSgr)
		case MouseModeAllMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeCellMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseAnyEvent + ansi.SetModeMouseExtSgr)
		}
	}

	// Set window title.
	if s.lastView == nil || view.WindowTitle != s.lastView.WindowTitle {
		if s.lastView != nil || view.WindowTitle != "" {
			_, _ = s.scr.WriteString(ansi.SetWindowTitle(view.WindowTitle))
		}
	}

	// kitty keyboard protocol
	if s.lastView == nil || view.KeyboardEnhancements != s.lastView.KeyboardEnhancements ||
		view.AltScreen != s.lastView.AltScreen {
		// NOTE: We need to reset the keyboard protocol when switching
		// between main and alt screen. This is because the specs specify
		// two different states for the main and alt screen.

		// Enable modifyOtherKeys and Kitty keyboard protocol.
		_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys1)
		_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys2)

		kittyFlags := ansi.KittyDisambiguateEscapeCodes // always enable basic key disambiguation
		if view.KeyboardEnhancements.ReportEventTypes {
			kittyFlags |= ansi.KittyReportEventTypes
		}
		_, _ = s.scr.WriteString(ansi.KittyKeyboard(kittyFlags, 1))
		if !closing {
			// Request keyboard enhancements when they change
			_, _ = s.scr.WriteString(ansi.RequestKittyKeyboard)
		}
	}

	// Set terminal colors.
	var (
		cc, lcc  color.Color
		lfg, lbg color.Color
	)
	if view.Cursor != nil {
		cc = view.Cursor.Color
	}
	if s.lastView != nil {
		if s.lastView.Cursor != nil {
			lcc = s.lastView.Cursor.Color
		}
		lfg = s.lastView.ForegroundColor
		lbg = s.lastView.BackgroundColor
	}
	for _, c := range []struct {
		newColor color.Color
		oldColor color.Color
		reset    string
		setter   func(string) string
	}{
		{newColor: cc, oldColor: lcc, reset: ansi.ResetCursorColor, setter: ansi.SetCursorColor},
		{newColor: view.ForegroundColor, oldColor: lfg, reset: ansi.ResetForegroundColor, setter: ansi.SetForegroundColor},
		{newColor: view.BackgroundColor, oldColor: lbg, reset: ansi.ResetBackgroundColor, setter: ansi.SetBackgroundColor},
	} {
		if c.newColor != c.oldColor {
			if c.newColor == nil {
				// Reset the color if it was set to nil.
				_, _ = s.scr.WriteString(c.reset)
			} else {
				// Set the color.
				col, ok := colorful.MakeColor(c.newColor)
				if ok {
					_, _ = s.scr.WriteString(c.setter(col.Hex()))
				}
			}
		}
	}

	// Set cursor shape and blink if set.
	var ccStyle, lcStyle int
	var lcur *Cursor
	ccur := view.Cursor
	if lv := s.lastView; lv != nil {
		lcur = lv.Cursor
	}
	if ccur != nil {
		ccStyle = encodeCursorStyle(ccur.Shape, ccur.Blink)
	}
	if lcur != nil {
		lcStyle = encodeCursorStyle(lcur.Shape, lcur.Blink)
	}
	if ccStyle != lcStyle {
		_, _ = s.scr.WriteString(ansi.SetCursorStyle(ccStyle))
	}

	// Render progress bar if it's changed.
	if (s.lastView == nil && view.ProgressBar != nil && view.ProgressBar.State != ProgressBarNone) ||
		(s.lastView != nil && (s.lastView.ProgressBar == nil) != (view.ProgressBar == nil)) ||
		(s.lastView != nil && s.lastView.ProgressBar != nil && view.ProgressBar != nil && *s.lastView.ProgressBar != *view.ProgressBar) {
		// Render or clear the progress bar if it was added or removed.
		setProgressBar(s, view.ProgressBar)
	}

	// Render and queue changes to the screen buffer.
	s.scr.Render(s.cellbuf.RenderBuffer)

	if cur := view.Cursor; cur != nil {
		// MoveTo must come after [uv.TerminalRenderer.Render] because the
		// cursor position might get updated during rendering.
		s.scr.MoveTo(view.Cursor.X, view.Cursor.Y)
	} else if !view.AltScreen {
		// We don't want the cursor to be dangling at the end of the line in
		// inline mode because it can cause unwanted line wraps in some
		// terminals. So we move it to the beginning of the next line if
		// necessary.
		// This is only needed when the cursor is hidden because when it's
		// visible, we already set its position above.
		x, y := s.scr.Position()
		if x >= s.width-1 {
			s.scr.MoveTo(0, y)
		}
	}

	if err := s.scr.Flush(); err != nil {
		return fmt.Errorf("bubbletea: error flushing screen writer: %w", err)
	}

	// Check if we have any render updates to flush.
	hasUpdates := s.buf.Len() > 0

	// Cursor visibility.
	didShowCursor := s.lastView != nil && s.lastView.Cursor != nil
	showCursor := view.Cursor != nil
	hideCursor := !showCursor
	shouldUpdateCursorVis := (s.lastView == nil || didShowCursor != showCursor) || shouldUpdateAltScreen

	// Build final output buffer with synchronized output or hide/show cursor
	// updates. But first, enter/exit alt screen mode if needed.
	//
	// Here, we have two scenarios:
	// 1. Synchronized output updates are supported. In this case, we want to
	//    wrap all updates, unless it's just a cursor visibility change, in
	//    synchronized output mode. This is because synchronized output mode
	//    takes care of rendering the updates atomically. In the case of
	//    just a cursor visibility change, we don't need to enter
	//    synchronized output mode because it's just a single sequence to
	//    flush out to the terminal.
	//
	// 2. We don't have synchronized output updates support. In this case, and
	//    if the cursor is visible or should be visible, we wrap the updates
	//    with hide/show cursor sequences to try and mitigate cursor
	//    flickering. This is terminal dependent and may still result in
	//    flickering in some terminals. It's the best effort we can do instead
	//    of showing the cursor flying around the screen during updates.

	var buf bytes.Buffer
	if shouldUpdateAltScreen {
		// We always disable keyboard enhancements when switching screens
		// because the terminal is expected to have two different keyboard
		// registries for main and alt screens.
		_, _ = buf.WriteString(ansi.ResetModifyOtherKeys)
		_, _ = buf.WriteString(ansi.KittyKeyboard(0, 1))
		if view.AltScreen {
			// Entering alt screen mode.
			buf.WriteString(ansi.SetModeAltScreenSaveCursor)
		} else {
			// Exiting alt screen mode.
			buf.WriteString(ansi.ResetModeAltScreenSaveCursor)
		}
	}

	if s.syncdUpdates {
		if hasUpdates {
			// We have synchronized output updates enabled.
			buf.WriteString(ansi.SetModeSynchronizedOutput)
		}
		if shouldUpdateCursorVis && hideCursor {
			// Do we need to update the cursor visibility to hidden? If so, do
			// it here before writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
		}
	} else if (shouldUpdateCursorVis && hideCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
	}

	if hasUpdates {
		buf.Write(s.buf.Bytes())
	}

	if s.syncdUpdates {
		if shouldUpdateCursorVis && showCursor {
			// Do we need to update the cursor visibility to visible? If so, do
			// it here after writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
		}
		if hasUpdates {
			// Close synchronized output mode.
			buf.WriteString(ansi.ResetModeSynchronizedOutput)
		}
	} else if (shouldUpdateCursorVis && showCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
	}

	// Reset internal screen renderer buffer.
	s.buf.Reset()

	// If our updates flush buffer has content, write it to the output writer.
	if buf.Len() > 0 {
		if s.logger != nil {
			s.logger.Printf("output: %q", buf.String())
		}
		if _, err := io.Copy(s.w, &buf); err != nil {
			return fmt.Errorf("bubbletea: error flushing update to the writer: %w", err)
		}
	}

	s.lastView = &view

	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *cursedRenderer) flush(closing bool) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	view := s.view
	frameArea := uv.Rect(0, 0, s.width, s.height)
	if len(view.Content) == 0 {
		// If the component is nil, we should clear the screen buffer.
		frameArea.Max.Y = 0
	}

	content := uv.NewStyledString(view.Content)
	if !view.AltScreen {
		// We need to resizes the screen based on the frame height and
		// terminal width. This is because the frame height can change based on
		// the content of the frame. For example, if the frame contains a list
		// of items, the height of the frame will be the number of items in the
		// list. This is different from the alt screen buffer, which has a
		// fixed height and width.
		frameHeight := content.Height()
		if frameHeight != frameArea.Dy() {
			frameArea.Max.Y = frameHeight
		}
	}

	if !s.starting && !closing && s.lastView != nil && viewEquals(s.lastView, &view) && frameArea == s.cellbuf.Bounds() {
		// No changes, nothing to do.
		return nil
	}

	// We're no longer starting.
	s.starting = false

	if frameArea != s.cellbuf.Bounds() {
		s.scr.Erase() // Force a full redraw to avoid artifacts.

		// We need to reset the touched lines buffer to match the new height.
		s.cellbuf.Touched = nil

		// Resize the screen buffer to match the frame area. This is necessary
		// to ensure that the screen buffer is the same size as the frame area
		// and to avoid rendering issues when the frame area is smaller than
		// the screen buffer.
		s.cellbuf.Resize(frameArea.Dx(), frameArea.Dy())
	}

	// Clear our screen buffer before copying the new frame into it to ensure
	// we erase any old content.
	s.cellbuf.Clear()
	content.Draw(s.cellbuf, s.cellbuf.Bounds())

	// If the frame height is greater than the screen height, we drop the
	// lines from the top of the buffer.
	if frameHeight := frameArea.Dy(); frameHeight > s.height {
		s.cellbuf.Lines = s.cellbuf.Lines[frameHeight-s.height:]
	}

	// Alt screen mode.
	shouldUpdateAltScreen := (s.lastView == nil && view.AltScreen) || (s.lastView != nil && s.lastView.AltScreen != view.AltScreen)
	if shouldUpdateAltScreen {
		// We want to enter/exit altscreen mode but defer writing the actual
		// sequences until we flush the rest of the updates. This is because we
		// control the cursor visibility and we need to ensure that happens
		// after entering/exiting alt screen mode. Some terminals have
		// different cursor visibility states for main and alt screen modes and
		// this ensures we handle that correctly.
		enableAltScreen(s, view.AltScreen, false)
	}

	// bracketed paste mode.
	if s.lastView == nil || view.DisableBracketedPasteMode != s.lastView.DisableBracketedPasteMode {
		if !view.DisableBracketedPasteMode {
			_, _ = s.scr.WriteString(ansi.SetModeBracketedPaste)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeBracketedPaste)
		}
	}

	// report focus events mode.
	if s.lastView == nil || s.lastView.ReportFocus != view.ReportFocus {
		if view.ReportFocus {
			_, _ = s.scr.WriteString(ansi.SetModeFocusEvent)
		} else if s.lastView != nil {
			_, _ = s.scr.WriteString(ansi.ResetModeFocusEvent)
		}
	}

	// mouse events mode.
	if s.lastView == nil || view.MouseMode != s.lastView.MouseMode {
		switch view.MouseMode {
		case MouseModeNone:
			if s.lastView != nil && s.lastView.MouseMode != MouseModeNone {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent +
					ansi.ResetModeMouseAnyEvent +
					ansi.ResetModeMouseExtSgr)
			}
		case MouseModeCellMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeAllMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseAnyEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseButtonEvent + ansi.SetModeMouseExtSgr)
		case MouseModeAllMotion:
			if s.lastView != nil && s.lastView.MouseMode == MouseModeCellMotion {
				_, _ = s.scr.WriteString(ansi.ResetModeMouseButtonEvent)
			}
			_, _ = s.scr.WriteString(ansi.SetModeMouseAnyEvent + ansi.SetModeMouseExtSgr)
		}
	}

	// Set window title.
	if s.lastView == nil || view.WindowTitle != s.lastView.WindowTitle {
		if s.lastView != nil || view.WindowTitle != "" {
			_, _ = s.scr.WriteString(ansi.SetWindowTitle(view.WindowTitle))
		}
	}

	// kitty keyboard protocol
	if s.lastView == nil || view.KeyboardEnhancements != s.lastView.KeyboardEnhancements ||
		view.AltScreen != s.lastView.AltScreen {
		// NOTE: We need to reset the keyboard protocol when switching
		// between main and alt screen. This is because the specs specify
		// two different states for the main and alt screen.

		// Enable modifyOtherKeys and Kitty keyboard protocol.
		_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys2)

		kittyFlags := ansi.KittyDisambiguateEscapeCodes // always enable basic key disambiguation
		if view.KeyboardEnhancements.ReportEventTypes {
			kittyFlags |= ansi.KittyReportEventTypes
		}
		_, _ = s.scr.WriteString(ansi.KittyKeyboard(kittyFlags, 1))
		if !closing {
			// Request keyboard enhancements when they change
			_, _ = s.scr.WriteString(ansi.RequestKittyKeyboard)
		}
	}

	// Set terminal colors.
	var (
		cc, lcc  color.Color
		lfg, lbg color.Color
	)
	if view.Cursor != nil {
		cc = view.Cursor.Color
	}
	if s.lastView != nil {
		if s.lastView.Cursor != nil {
			lcc = s.lastView.Cursor.Color
		}
		lfg = s.lastView.ForegroundColor
		lbg = s.lastView.BackgroundColor
	}
	for _, c := range []struct {
		newColor color.Color
		oldColor color.Color
		reset    string
		setter   func(string) string
	}{
		{newColor: cc, oldColor: lcc, reset: ansi.ResetCursorColor, setter: ansi.SetCursorColor},
		{newColor: view.ForegroundColor, oldColor: lfg, reset: ansi.ResetForegroundColor, setter: ansi.SetForegroundColor},
		{newColor: view.BackgroundColor, oldColor: lbg, reset: ansi.ResetBackgroundColor, setter: ansi.SetBackgroundColor},
	} {
		if c.newColor != c.oldColor {
			if c.newColor == nil {
				// Reset the color if it was set to nil.
				_, _ = s.scr.WriteString(c.reset)
			} else {
				// Set the color.
				col, ok := colorful.MakeColor(c.newColor)
				if ok {
					_, _ = s.scr.WriteString(c.setter(col.Hex()))
				}
			}
		}
	}

	// Set cursor shape and blink if set.
	var ccStyle, lcStyle int
	var lcur *Cursor
	ccur := view.Cursor
	if lv := s.lastView; lv != nil {
		lcur = lv.Cursor
	}
	if ccur != nil {
		ccStyle = encodeCursorStyle(ccur.Shape, ccur.Blink)
	}
	if lcur != nil {
		lcStyle = encodeCursorStyle(lcur.Shape, lcur.Blink)
	}
	if ccStyle != lcStyle {
		_, _ = s.scr.WriteString(ansi.SetCursorStyle(ccStyle))
	}

	// Render progress bar if it's changed.
	if (s.lastView == nil && view.ProgressBar != nil && view.ProgressBar.State != ProgressBarNone) ||
		(s.lastView != nil && (s.lastView.ProgressBar == nil) != (view.ProgressBar == nil)) ||
		(s.lastView != nil && s.lastView.ProgressBar != nil && view.ProgressBar != nil && *s.lastView.ProgressBar != *view.ProgressBar) {
		// Render or clear the progress bar if it was added or removed.
		setProgressBar(s, view.ProgressBar)
	}

	// Render and queue changes to the screen buffer.
	s.scr.Render(s.cellbuf.RenderBuffer)

	if cur := view.Cursor; cur != nil {
		// MoveTo must come after [uv.TerminalRenderer.Render] because the
		// cursor position might get updated during rendering.
		s.scr.MoveTo(view.Cursor.X, view.Cursor.Y)
	} else if !view.AltScreen {
		// We don't want the cursor to be dangling at the end of the line in
		// inline mode because it can cause unwanted line wraps in some
		// terminals. So we move it to the beginning of the next line if
		// necessary.
		// This is only needed when the cursor is hidden because when it's
		// visible, we already set its position above.
		x, y := s.scr.Position()
		if x >= s.width-1 {
			s.scr.MoveTo(0, y)
		}
	}

	if err := s.scr.Flush(); err != nil {
		return fmt.Errorf("bubbletea: error flushing screen writer: %w", err)
	}

	// Check if we have any render updates to flush.
	hasUpdates := s.buf.Len() > 0

	// Cursor visibility.
	didShowCursor := s.lastView != nil && s.lastView.Cursor != nil
	showCursor := view.Cursor != nil
	hideCursor := !showCursor
	shouldUpdateCursorVis := (s.lastView == nil || didShowCursor != showCursor) || shouldUpdateAltScreen

	// Build final output buffer with synchronized output or hide/show cursor
	// updates. But first, enter/exit alt screen mode if needed.
	//
	// Here, we have two scenarios:
	// 1. Synchronized output updates are supported. In this case, we want to
	//    wrap all updates, unless it's just a cursor visibility change, in
	//    synchronized output mode. This is because synchronized output mode
	//    takes care of rendering the updates atomically. In the case of
	//    just a cursor visibility change, we don't need to enter
	//    synchronized output mode because it's just a single sequence to
	//    flush out to the terminal.
	//
	// 2. We don't have synchronized output updates support. In this case, and
	//    if the cursor is visible or should be visible, we wrap the updates
	//    with hide/show cursor sequences to try and mitigate cursor
	//    flickering. This is terminal dependent and may still result in
	//    flickering in some terminals. It's the best effort we can do instead
	//    of showing the cursor flying around the screen during updates.

	var buf bytes.Buffer
	if shouldUpdateAltScreen {
		// We always disable keyboard enhancements when switching screens
		// because the terminal is expected to have two different keyboard
		// registries for main and alt screens.
		_, _ = buf.WriteString(ansi.ResetModifyOtherKeys)
		_, _ = buf.WriteString(ansi.KittyKeyboard(0, 1))
		if view.AltScreen {
			// Entering alt screen mode.
			buf.WriteString(ansi.SetModeAltScreenSaveCursor)
		} else {
			// Exiting alt screen mode.
			buf.WriteString(ansi.ResetModeAltScreenSaveCursor)
		}
	}

	if s.syncdUpdates {
		if hasUpdates {
			// We have synchronized output updates enabled.
			buf.WriteString(ansi.SetModeSynchronizedOutput)
		}
		if shouldUpdateCursorVis && hideCursor {
			// Do we need to update the cursor visibility to hidden? If so, do
			// it here before writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
		}
	} else if (shouldUpdateCursorVis && hideCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.ResetModeTextCursorEnable)
	}

	if hasUpdates {
		buf.Write(s.buf.Bytes())
	}

	if s.syncdUpdates {
		if shouldUpdateCursorVis && showCursor {
			// Do we need to update the cursor visibility to visible? If so, do
			// it here after writing any updates to the buffer.
			_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
		}
		if hasUpdates {
			// Close synchronized output mode.
			buf.WriteString(ansi.ResetModeSynchronizedOutput)
		}
	} else if (shouldUpdateCursorVis && showCursor) || (hasUpdates && showCursor && didShowCursor) {
		_, _ = buf.WriteString(ansi.SetModeTextCursorEnable)
	}

	// Reset internal screen renderer buffer.
	s.buf.Reset()

	// If our updates flush buffer has content, write it to the output writer.
	if buf.Len() > 0 {
		if s.logger != nil {
			s.logger.Printf("output: %q", buf.String())
		}
		if _, err := io.Copy(s.w, &buf); err != nil {
			return fmt.Errorf("bubbletea: error flushing update to the writer: %w", err)
		}
	}

	s.lastView = &view

	return nil
}
```

### 🔹 函式: `cursedRenderer.start()`
- **變更前簽章 (Before)**: `func cursedRenderer.start()` (L71~L140)
- **變更後簽章 (After)**: `func cursedRenderer.start()` (L71~L139)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *cursedRenderer) start() {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Mark that we're starting. This is used to restore some state when
	// starting the renderer again after it was stopped.
	s.starting = true

	if s.lastView == nil {
		return
	}

	if s.lastView.AltScreen {
		enableAltScreen(s, true, true)
	}
	enableTextCursor(s, s.lastView.Cursor != nil)
	if s.lastView.Cursor != nil {
		if s.lastView.Cursor.Color != nil {
			col, ok := colorful.MakeColor(s.lastView.Cursor.Color)
			if ok {
				_, _ = s.scr.WriteString(ansi.SetCursorColor(col.Hex()))
			}
		}
		curStyle := encodeCursorStyle(s.lastView.Cursor.Shape, s.lastView.Cursor.Blink)
		if curStyle != 0 && curStyle != 1 {
			_, _ = s.scr.WriteString(ansi.SetCursorStyle(curStyle))
		}
	}
	if s.lastView.ForegroundColor != nil {
		col, ok := colorful.MakeColor(s.lastView.ForegroundColor)
		if ok {
			_, _ = s.scr.WriteString(ansi.SetForegroundColor(col.Hex()))
		}
	}
	if s.lastView.BackgroundColor != nil {
		col, ok := colorful.MakeColor(s.lastView.BackgroundColor)
		if ok {
			_, _ = s.scr.WriteString(ansi.SetBackgroundColor(col.Hex()))
		}
	}
	if !s.lastView.DisableBracketedPasteMode {
		_, _ = s.scr.WriteString(ansi.SetModeBracketedPaste)
	}
	if s.lastView.ReportFocus {
		_, _ = s.scr.WriteString(ansi.SetModeFocusEvent)
	}
	switch s.lastView.MouseMode {
	case MouseModeNone:
	case MouseModeCellMotion:
		_, _ = s.scr.WriteString(ansi.SetModeMouseButtonEvent + ansi.SetModeMouseExtSgr)
	case MouseModeAllMotion:
		_, _ = s.scr.WriteString(ansi.SetModeMouseAnyEvent + ansi.SetModeMouseExtSgr)
	}
	if s.lastView.WindowTitle != "" {
		_, _ = s.scr.WriteString(ansi.SetWindowTitle(s.lastView.WindowTitle))
	}
	if s.lastView.ProgressBar != nil {
		setProgressBar(s, s.lastView.ProgressBar)
	}
	// Enable modifyOtherKeys and Kitty keyboard protocol.
	// Both can coexist; terminals ignore what they don't support.
	_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys1)
	_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys2)

	kittyFlags := ansi.KittyDisambiguateEscapeCodes
	if s.lastView.KeyboardEnhancements.ReportEventTypes {
		kittyFlags |= ansi.KittyReportEventTypes
	}
	_, _ = s.scr.WriteString(ansi.KittyKeyboard(kittyFlags, 1))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *cursedRenderer) start() {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Mark that we're starting. This is used to restore some state when
	// starting the renderer again after it was stopped.
	s.starting = true

	if s.lastView == nil {
		return
	}

	if s.lastView.AltScreen {
		enableAltScreen(s, true, true)
	}
	enableTextCursor(s, s.lastView.Cursor != nil)
	if s.lastView.Cursor != nil {
		if s.lastView.Cursor.Color != nil {
			col, ok := colorful.MakeColor(s.lastView.Cursor.Color)
			if ok {
				_, _ = s.scr.WriteString(ansi.SetCursorColor(col.Hex()))
			}
		}
		curStyle := encodeCursorStyle(s.lastView.Cursor.Shape, s.lastView.Cursor.Blink)
		if curStyle != 0 && curStyle != 1 {
			_, _ = s.scr.WriteString(ansi.SetCursorStyle(curStyle))
		}
	}
	if s.lastView.ForegroundColor != nil {
		col, ok := colorful.MakeColor(s.lastView.ForegroundColor)
		if ok {
			_, _ = s.scr.WriteString(ansi.SetForegroundColor(col.Hex()))
		}
	}
	if s.lastView.BackgroundColor != nil {
		col, ok := colorful.MakeColor(s.lastView.BackgroundColor)
		if ok {
			_, _ = s.scr.WriteString(ansi.SetBackgroundColor(col.Hex()))
		}
	}
	if !s.lastView.DisableBracketedPasteMode {
		_, _ = s.scr.WriteString(ansi.SetModeBracketedPaste)
	}
	if s.lastView.ReportFocus {
		_, _ = s.scr.WriteString(ansi.SetModeFocusEvent)
	}
	switch s.lastView.MouseMode {
	case MouseModeNone:
	case MouseModeCellMotion:
		_, _ = s.scr.WriteString(ansi.SetModeMouseButtonEvent + ansi.SetModeMouseExtSgr)
	case MouseModeAllMotion:
		_, _ = s.scr.WriteString(ansi.SetModeMouseAnyEvent + ansi.SetModeMouseExtSgr)
	}
	if s.lastView.WindowTitle != "" {
		_, _ = s.scr.WriteString(ansi.SetWindowTitle(s.lastView.WindowTitle))
	}
	if s.lastView.ProgressBar != nil {
		setProgressBar(s, s.lastView.ProgressBar)
	}
	// Enable modifyOtherKeys and Kitty keyboard protocol.
	// Both can coexist; terminals ignore what they don't support.
	_, _ = s.scr.WriteString(ansi.SetModifyOtherKeys2)

	kittyFlags := ansi.KittyDisambiguateEscapeCodes
	if s.lastView.KeyboardEnhancements.ReportEventTypes {
		kittyFlags |= ansi.KittyReportEventTypes
	}
	_, _ = s.scr.WriteString(ansi.KittyKeyboard(kittyFlags, 1))
}
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/bubbletea show 96d69d2f7eb182bb311be08fc56ed2c208239aff
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 96d69d2f7eb182bb311be08fc56ed2c208239aff~1 --file test_repos/bubbletea/tea.go
   ```
