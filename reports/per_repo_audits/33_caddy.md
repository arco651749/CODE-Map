# 🔬 CODE-Map 基準審查獨立驗證報告: `caddy`
> **技術生態**: `Go (雲原生 Web 伺服器 / 自動 TLS / 重載)`  
> **本地倉庫路徑**: `test_repos/caddy`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 33 Files  
> **報告生成時間**: 2026-10-20 21:44:37  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `22` / `33` | `66.7%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `7` / `33` | `21.2%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `4` / `33` | `12.1%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`29` / `33`** | **`87.9%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `33` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `612128e3`
- **完整 Hash**: `612128e3b0f290af44649d7a7dcb1111fc3ebb33`
- **說明 (Ground Truth)**: logging: Parse request URIs in the `query` filter like the server does (#8255)
- **變更檔案數**: 1

#### 📄 檔案: `modules/logging/filters.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:91, E:128, A:0) ➔ After(N:92, E:129, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 1, +Edges: 2, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `strings.HasPrefix (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `parse (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `url.Parse (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `QueryFilter.processQueryString` ──[CALLS]──> `strings.HasPrefix (External/Pkg)`
  • + [新增呼叫邊] `QueryFilter.processQueryString` ──[CALLS]──> `parse (External/Pkg)`
  • - [移除呼叫邊] `QueryFilter.processQueryString` ──[CALLS]──> `url.Parse (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `QueryFilter.processQueryString()`
- **變更前簽章 (Before)**: `func QueryFilter.processQueryString(s string)` (L417~L443)
- **變更後簽章 (After)**: `func QueryFilter.processQueryString(s string)` (L417~L451)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (m QueryFilter) processQueryString(s string) string {
	u, err := url.Parse(s)
	if err != nil {
		return s
	}

	q := u.Query()
	for _, a := range m.Actions {
		switch a.Type {
		case replaceAction:
			for i := range q[a.Parameter] {
				q[a.Parameter][i] = a.Value
			}

		case hashAction:
			for i := range q[a.Parameter] {
				q[a.Parameter][i] = hash(q[a.Parameter][i])
			}

		case deleteAction:
			q.Del(a.Parameter)
		}
	}

	u.RawQuery = q.Encode()
	return u.String()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (m QueryFilter) processQueryString(s string) string {
	parse := url.Parse
	if strings.HasPrefix(s, "/") {
		// parse a request-target like the server does. Browsers and most
		// clients strip a #fragment before sending, but a client that
		// sends a raw '#' has it kept in the query by the server
		// (url.ParseRequestURI does not split it off), so filter it too
		parse = url.ParseRequestURI
	}
	u, err := parse(s)
	if err != nil {
		return s
	}

	q := u.Query()
	for _, a := range m.Actions {
		switch a.Type {
		case replaceAction:
			for i := range q[a.Parameter] {
				q[a.Parameter][i] = a.Value
			}

		case hashAction:
			for i := range q[a.Parameter] {
				q[a.Parameter][i] = hash(q[a.Parameter][i])
			}

		case deleteAction:
			q.Del(a.Parameter)
		}
	}

	u.RawQuery = q.Encode()
	return u.String()
}
```


---

### 🔹 Commit #02: `872c864c`
- **完整 Hash**: `872c864c200b22dc5161942816be6409eafcb295`
- **說明 (Ground Truth)**: caddytls: skip client cert verifiers when no certificate is presented (#8251)
- **變更檔案數**: 1

#### 📄 檔案: `modules/caddytls/connpolicy.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:102, E:149, A:0) ➔ After(N:102, E:149, A:0)
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

### 🔹 函式: `ClientAuthentication.verifyConnection()`
- **變更前簽章 (Before)**: `func ClientAuthentication.verifyConnection(cs tls.ConnectionState)` (L909~L927)
- **變更後簽章 (After)**: `func ClientAuthentication.verifyConnection(cs tls.ConnectionState)` (L909~L933)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (clientauth *ClientAuthentication) verifyConnection(cs tls.ConnectionState) error {
	rawCerts := make([][]byte, len(cs.PeerCertificates))
	for i, cert := range cs.PeerCertificates {
		rawCerts[i] = cert.Raw
	}

	// first use any pre-existing custom verification function
	if clientauth.existingVerifyPeerCert != nil {
		if err := clientauth.existingVerifyPeerCert(rawCerts, cs.VerifiedChains); err != nil {
			return err
		}
	}
	for _, verifier := range clientauth.verifiers {
		if err := verifier.VerifyClientCertificate(rawCerts, cs.VerifiedChains); err != nil {
			return err
		}
	}
	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (clientauth *ClientAuthentication) verifyConnection(cs tls.ConnectionState) error {
	rawCerts := make([][]byte, len(cs.PeerCertificates))
	for i, cert := range cs.PeerCertificates {
		rawCerts[i] = cert.Raw
	}

	// first use any pre-existing custom verification function
	if clientauth.existingVerifyPeerCert != nil {
		if err := clientauth.existingVerifyPeerCert(rawCerts, cs.VerifiedChains); err != nil {
			return err
		}
	}

	// crypto/tls has already enforced whether the mode requires a
	// certificate, so the verifiers only check one that was presented
	if len(rawCerts) == 0 {
		return nil
	}
	for _, verifier := range clientauth.verifiers {
		if err := verifier.VerifyClientCertificate(rawCerts, cs.VerifiedChains); err != nil {
			return err
		}
	}
	return nil
}
```


---

### 🔹 Commit #03: `1619352f`
- **完整 Hash**: `1619352f4e36d2c7dfab6d9e793f8495d7b36993`
- **說明 (Ground Truth)**: ci: fix exhaustive linting (#8238)
- **變更檔案數**: 3

#### 📄 檔案: `context.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:122, E:137, A:0) ➔ After(N:122, E:137, A:0)
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

#### 📄 檔案: `modules/caddyhttp/responsewriter.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:50, E:44, A:0) ➔ After(N:50, E:44, A:0)
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

#### 📄 檔案: `service_windows.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:10, E:8, A:0) ➔ After(N:10, E:8, A:0)
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

### 🔹 Commit #04: `be5fba4f`
- **完整 Hash**: `be5fba4ff25f403ce4435395a7de4a9dace65ae9`
- **說明 (Ground Truth)**: caddyauth: handle CRLF and unterminated hash-password input (#8227)
- **變更檔案數**: 1

#### 📄 檔案: `modules/caddyhttp/caddyauth/command.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:38, E:33, A:0) ➔ After(N:41, E:36, A:0)
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
  • + [新增節點] `errors.Is (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `bytes.CutSuffix (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `bytes.TrimSuffix (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `cmdHashPassword` ──[CALLS]──> `errors.Is (External/Pkg)`
  • + [新增呼叫邊] `cmdHashPassword` ──[CALLS]──> `bytes.CutSuffix (External/Pkg)`
  • + [新增呼叫邊] `cmdHashPassword` ──[CALLS]──> `bytes.TrimSuffix (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `cmdHashPassword()`
- **變更前簽章 (Before)**: `func cmdHashPassword(fs caddycmd.Flags)` (L89~L184)
- **變更後簽章 (After)**: `func cmdHashPassword(fs caddycmd.Flags)` (L91~L190)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func cmdHashPassword(fs caddycmd.Flags) (int, error) {
	var err error

	algorithm := fs.String("algorithm")
	plaintext := []byte(fs.String("plaintext"))
	bcryptCost := fs.Int("bcrypt-cost")

	if len(plaintext) == 0 {
		fd := int(os.Stdin.Fd())
		if term.IsTerminal(fd) {
			// ensure the terminal state is restored on SIGINT
			state, _ := term.GetState(fd)
			c := make(chan os.Signal, 1)
			signal.Notify(c, os.Interrupt)
			go func() {
				<-c
				_ = term.Restore(fd, state)
				os.Exit(caddy.ExitCodeFailedStartup)
			}()
			defer signal.Stop(c)

			fmt.Fprint(os.Stderr, "Enter password: ")
			plaintext, err = term.ReadPassword(fd)
			fmt.Fprintln(os.Stderr)
			if err != nil {
				return caddy.ExitCodeFailedStartup, err
			}

			fmt.Fprint(os.Stderr, "Confirm password: ")
			confirmation, err := term.ReadPassword(fd)
			fmt.Fprintln(os.Stderr)
			if err != nil {
				return caddy.ExitCodeFailedStartup, err
			}

			if !bytes.Equal(plaintext, confirmation) {
				return caddy.ExitCodeFailedStartup, fmt.Errorf("password does not match")
			}
		} else {
			rd := bufio.NewReader(os.Stdin)
			plaintext, err = rd.ReadBytes('\n')
			if err != nil {
				return caddy.ExitCodeFailedStartup, err
			}

			plaintext = plaintext[:len(plaintext)-1] // Trailing newline
		}

		if len(plaintext) == 0 {
			return caddy.ExitCodeFailedStartup, fmt.Errorf("plaintext is required")
		}
	}

	var hash []byte
	var hashString string
	switch algorithm {
	case bcryptName:
		hash, err = BcryptHash{cost: bcryptCost}.Hash(plaintext)
		hashString = string(hash)
	case argon2idName:
		time, err := fs.GetUint32("argon2id-time")
		if err != nil {
			return caddy.ExitCodeFailedStartup, fmt.Errorf("failed to get argon2id time parameter: %w", err)
		}
		memory, err := fs.GetUint32("argon2id-memory")
		if err != nil {
			return caddy.ExitCodeFailedStartup, fmt.Errorf("failed to get argon2id memory parameter: %w", err)
		}
		threads, err := fs.GetUint8("argon2id-threads")
		if err != nil {
			return caddy.ExitCodeFailedStartup, fmt.Errorf("failed to get argon2id threads parameter: %w", err)
		}
		keyLen, err := fs.GetUint32("argon2id-keylen")
		if err != nil {
			return caddy.ExitCodeFailedStartup, fmt.Errorf("failed to get argon2id keylen parameter: %w", err)
		}

		hash, _ = Argon2idHash{
			time:    time,
			memory:  memory,
			threads: threads,
			keyLen:  keyLen,
		}.Hash(plaintext)

		hashString = string(hash)
	default:
		return caddy.ExitCodeFailedStartup, fmt.Errorf("unrecognized hash algorithm: %s", algorithm)
	}
	if err != nil {
		return caddy.ExitCodeFailedStartup, err
	}

	fmt.Println(hashString)

	return 0, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func cmdHashPassword(fs caddycmd.Flags) (int, error) {
	var err error

	algorithm := fs.String("algorithm")
	plaintext := []byte(fs.String("plaintext"))
	bcryptCost := fs.Int("bcrypt-cost")

	if len(plaintext) == 0 {
		fd := int(os.Stdin.Fd())
		if term.IsTerminal(fd) {
			// ensure the terminal state is restored on SIGINT
			state, _ := term.GetState(fd)
			c := make(chan os.Signal, 1)
			signal.Notify(c, os.Interrupt)
			go func() {
				<-c
				_ = term.Restore(fd, state)
				os.Exit(caddy.ExitCodeFailedStartup)
			}()
			defer signal.Stop(c)

			fmt.Fprint(os.Stderr, "Enter password: ")
			plaintext, err = term.ReadPassword(fd)
			fmt.Fprintln(os.Stderr)
			if err != nil {
				return caddy.ExitCodeFailedStartup, err
			}

			fmt.Fprint(os.Stderr, "Confirm password: ")
			confirmation, err := term.ReadPassword(fd)
			fmt.Fprintln(os.Stderr)
			if err != nil {
				return caddy.ExitCodeFailedStartup, err
			}

			if !bytes.Equal(plaintext, confirmation) {
				return caddy.ExitCodeFailedStartup, fmt.Errorf("password does not match")
			}
		} else {
			rd := bufio.NewReader(os.Stdin)
			line, err := rd.ReadBytes('\n')
			if err != nil && !errors.Is(err, io.EOF) {
				return caddy.ExitCodeFailedStartup, err
			}

			// drop the line ending (\n or \r\n), if any; a lone trailing \r is kept
			if trimmed, ok := bytes.CutSuffix(line, []byte("\n")); ok {
				line = bytes.TrimSuffix(trimmed, []byte("\r"))
			}
			plaintext = line
		}

		if len(plaintext) == 0 {
			return caddy.ExitCodeFailedStartup, fmt.Errorf("plaintext is required")
		}
	}

	var hash []byte
	var hashString string
	switch algorithm {
	case bcryptName:
		hash, err = BcryptHash{cost: bcryptCost}.Hash(plaintext)
		hashString = string(hash)
	case argon2idName:
		time, err := fs.GetUint32("argon2id-time")
		if err != nil {
			return caddy.ExitCodeFailedStartup, fmt.Errorf("failed to get argon2id time parameter: %w", err)
		}
		memory, err := fs.GetUint32("argon2id-memory")
		if err != nil {
			return caddy.ExitCodeFailedStartup, fmt.Errorf("failed to get argon2id memory parameter: %w", err)
		}
		threads, err := fs.GetUint8("argon2id-threads")
		if err != nil {
			return caddy.ExitCodeFailedStartup, fmt.Errorf("failed to get argon2id threads parameter: %w", err)
		}
		keyLen, err := fs.GetUint32("argon2id-keylen")
		if err != nil {
			return caddy.ExitCodeFailedStartup, fmt.Errorf("failed to get argon2id keylen parameter: %w", err)
		}

		hash, _ = Argon2idHash{
			time:    time,
			memory:  memory,
			threads: threads,
			keyLen:  keyLen,
		}.Hash(plaintext)

		hashString = string(hash)
	default:
		return caddy.ExitCodeFailedStartup, fmt.Errorf("unrecognized hash algorithm: %s", algorithm)
	}
	if err != nil {
		return caddy.ExitCodeFailedStartup, err
	}

	fmt.Println(hashString)

	return 0, nil
}
```


---

### 🔹 Commit #05: `860b4ce6`
- **完整 Hash**: `860b4ce635ed1f5496bc48f5989b1acdc6ebaa10`
- **說明 (Ground Truth)**: logging: include module logs from its parent namespace (#8221)
- **變更檔案數**: 1

#### 📄 檔案: `logging.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:99, E:111, A:0) ➔ After(N:99, E:111, A:0)
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

### 🔹 函式: `CustomLog.loggerAllowed()`
- **變更前簽章 (Before)**: `func CustomLog.loggerAllowed(name string, isModule bool)` (L533~L592)
- **變更後簽章 (After)**: `func CustomLog.loggerAllowed(name string, isModule bool)` (L533~L597)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (cl *CustomLog) loggerAllowed(name string, isModule bool) bool {
	// accept all loggers by default
	if len(cl.Include) == 0 && len(cl.Exclude) == 0 {
		return true
	}

	// append a dot so that partial names don't match
	// (i.e. we don't want "foo.b" to match "foo.bar"); we
	// will also have to append a dot when we do HasPrefix
	// below to compensate for when namespaces are equal
	if name != "" && name != "*" && name != "." {
		name += "."
	}

	var longestAccept, longestReject int

	if len(cl.Include) > 0 {
		for _, namespace := range cl.Include {
			var hasPrefix bool
			if isModule {
				hasPrefix = strings.HasPrefix(namespace+".", name)
			} else {
				hasPrefix = strings.HasPrefix(name, namespace+".")
			}
			if hasPrefix && len(namespace) > longestAccept {
				longestAccept = len(namespace)
			}
		}
		// the include list was populated, meaning that
		// a match in this list is absolutely required
		// if we are to accept the entry
		if longestAccept == 0 {
			return false
		}
	}

	if len(cl.Exclude) > 0 {
		for _, namespace := range cl.Exclude {
			// * == all logs emitted by modules
			// . == all logs emitted by core
			if (namespace == "*" && name != ".") ||
				(namespace == "." && name == ".") {
				return false
			}
			if strings.HasPrefix(name, namespace+".") &&
				len(namespace) > longestReject {
				longestReject = len(namespace)
			}
		}
		// the reject list is populated, so we have to
		// reject this entry if its match is better
		// than the best from the accept list
		if longestReject > longestAccept {
			return false
		}
	}

	return (longestAccept > longestReject) ||
		(len(cl.Include) == 0 && longestReject == 0)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (cl *CustomLog) loggerAllowed(name string, isModule bool) bool {
	// accept all loggers by default
	if len(cl.Include) == 0 && len(cl.Exclude) == 0 {
		return true
	}

	// append a dot so that partial names don't match
	// (i.e. we don't want "foo.b" to match "foo.bar"); we
	// will also have to append a dot when we do HasPrefix
	// below to compensate for when namespaces are equal
	if name != "" && name != "*" && name != "." {
		name += "."
	}

	var longestAccept, longestReject int

	if len(cl.Include) > 0 {
		for _, namespace := range cl.Include {
			var hasPrefix bool
			if isModule {
				// the namespace is the module or one of its
				// sub-loggers (e.g. "http.log.access" for "http")
				hasPrefix = strings.HasPrefix(namespace+".", name) ||
					// the namespace is a parent of the module (e.g.
					// "http.handlers" for "http.handlers.file_server")
					strings.HasPrefix(name, namespace+".")
			} else {
				hasPrefix = strings.HasPrefix(name, namespace+".")
			}
			if hasPrefix && len(namespace) > longestAccept {
				longestAccept = len(namespace)
			}
		}
		// the include list was populated, meaning that
		// a match in this list is absolutely required
		// if we are to accept the entry
		if longestAccept == 0 {
			return false
		}
	}

	if len(cl.Exclude) > 0 {
		for _, namespace := range cl.Exclude {
			// * == all logs emitted by modules
			// . == all logs emitted by core
			if (namespace == "*" && name != ".") ||
				(namespace == "." && name == ".") {
				return false
			}
			if strings.HasPrefix(name, namespace+".") &&
				len(namespace) > longestReject {
				longestReject = len(namespace)
			}
		}
		// the reject list is populated, so we have to
		// reject this entry if its match is better
		// than the best from the accept list
		if longestReject > longestAccept {
			return false
		}
	}

	return (longestAccept > longestReject) ||
		(len(cl.Include) == 0 && longestReject == 0)
}
```


---

### 🔹 Commit #06: `25c6901e`
- **完整 Hash**: `25c6901e05214573b87c48e07e3913e319032ec6`
- **說明 (Ground Truth)**: httpcaddyfile: isolate TLS policies across listeners (#8192)
- **變更檔案數**: 1

#### 📄 檔案: `caddyconfig/httpcaddyfile/httptype.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:138, E:184, A:0) ➔ After(N:139, E:188, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 4, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `cloneConnectionPolicy` (FUNCTION_DEF)
  • + [新增呼叫邊] `ServerType.serversFromPairings` ──[CALLS]──> `cloneConnectionPolicy`
  • + [新增呼叫邊] `cloneConnectionPolicy` ──[CALLS]──> `json.Marshal (External/Pkg)`
  • + [新增呼叫邊] `cloneConnectionPolicy` ──[CALLS]──> `new (External/Pkg)`
  • + [新增呼叫邊] `cloneConnectionPolicy` ──[CALLS]──> `json.Unmarshal (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `ServerType.serversFromPairings()`
- **變更前簽章 (Before)**: `func ServerType.serversFromPairings(
	pairings []sbAddrAssociation,
	options map[string]any,
	warnings *[]caddyconfig.Warning,
	groupCounter counter,
)` (L566~L1130)
- **變更後簽章 (After)**: `func ServerType.serversFromPairings(
	pairings []sbAddrAssociation,
	options map[string]any,
	warnings *[]caddyconfig.Warning,
	groupCounter counter,
)` (L566~L1135)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (st *ServerType) serversFromPairings(
	pairings []sbAddrAssociation,
	options map[string]any,
	warnings *[]caddyconfig.Warning,
	groupCounter counter,
) (map[string]*caddyhttp.Server, error) {
	servers := make(map[string]*caddyhttp.Server)
	defaultSNI := tryString(options["default_sni"], warnings)
	fallbackSNI := tryString(options["fallback_sni"], warnings)

	httpPort := strconv.Itoa(caddyhttp.DefaultHTTPPort)
	if hp, ok := options["http_port"].(int); ok {
		httpPort = strconv.Itoa(hp)
	}
	httpsPort := strconv.Itoa(caddyhttp.DefaultHTTPSPort)
	if hsp, ok := options["https_port"].(int); ok {
		httpsPort = strconv.Itoa(hsp)
	}
	autoHTTPS := []string{}
	if ah, ok := options["auto_https"].([]string); ok {
		autoHTTPS = ah
	}

	for i, p := range pairings {
		// detect ambiguous site definitions: server blocks which
		// have the same host bound to the same interface (listener
		// address), otherwise their routes will improperly be added
		// to the same server (see issue #4635)
		for j, sblock1 := range p.serverBlocks {
			for _, key := range sblock1.block.GetKeysText() {
				for k, sblock2 := range p.serverBlocks {
					if k == j {
						continue
					}
					if slices.Contains(sblock2.block.GetKeysText(), key) {
						return nil, fmt.Errorf("ambiguous site definition: %s", key)
					}
				}
			}
		}

		var (
			addresses []string
			protocols [][]string
		)

		for _, addressWithProtocols := range p.addressesWithProtocols {
			addresses = append(addresses, addressWithProtocols.address)
			protocols = append(protocols, addressWithProtocols.protocols)
		}

		srv := &caddyhttp.Server{
			Listen:          addresses,
			ListenProtocols: protocols,
		}

		// remove srv.ListenProtocols[j] if it only contains the default protocols
		for j, lnProtocols := range srv.ListenProtocols {
			srv.ListenProtocols[j] = nil
			for _, lnProtocol := range lnProtocols {
				if lnProtocol != "" {
					srv.ListenProtocols[j] = lnProtocols
					break
				}
			}
		}

		// remove srv.ListenProtocols if it only contains the default protocols for all listen addresses
		listenProtocols := srv.ListenProtocols
		srv.ListenProtocols = nil
		for _, lnProtocols := range listenProtocols {
			if lnProtocols != nil {
				srv.ListenProtocols = listenProtocols
				break
			}
		}

		// handle the auto_https global option
		for _, val := range autoHTTPS {
			switch val {
			case "off":
				if srv.AutoHTTPS == nil {
					srv.AutoHTTPS = new(caddyhttp.AutoHTTPSConfig)
				}
				srv.AutoHTTPS.Disabled = true

			case "disable_redirects":
				if srv.AutoHTTPS == nil {
					srv.AutoHTTPS = new(caddyhttp.AutoHTTPSConfig)
				}
				srv.AutoHTTPS.DisableRedir = true

			case "disable_certs":
				if srv.AutoHTTPS == nil {
					srv.AutoHTTPS = new(caddyhttp.AutoHTTPSConfig)
				}
				srv.AutoHTTPS.DisableCerts = true

			case "ignore_loaded_certs":
				if srv.AutoHTTPS == nil {
					srv.AutoHTTPS = new(caddyhttp.AutoHTTPSConfig)
				}
				srv.AutoHTTPS.IgnoreLoadedCerts = true
			}
		}

		// Using paths in site addresses is deprecated
		// See ParseAddress() where parsing should later reject paths
		// See https://github.com/caddyserver/caddy/pull/4728 for a full explanation
		for _, sblock := range p.serverBlocks {
			for _, addr := range sblock.parsedKeys {
				if addr.Path != "" {
					caddy.Log().Named("caddyfile").Warn("Using a path in a site address is deprecated; please use the 'handle' directive instead", zap.String("address", addr.String()))
				}
			}
		}

		// sort server blocks by their keys; this is important because
		// only the first matching site should be evaluated, and we should
		// attempt to match most specific site first (host and path), in
		// case their matchers overlap; we do this somewhat naively by
		// descending sort by length of host then path
		sort.SliceStable(p.serverBlocks, func(i, j int) bool {
			// TODO: we could pre-process the specificities for efficiency,
			// but I don't expect many blocks will have THAT many keys...
			var iLongestPath, jLongestPath string
			var iLongestHost, jLongestHost string
			var iWildcardHost, jWildcardHost bool
			for _, addr := range p.serverBlocks[i].parsedKeys {
				if strings.Contains(addr.Host, "*") || addr.Host == "" {
					iWildcardHost = true
				}
				if specificity(addr.Host) > specificity(iLongestHost) {
					iLongestHost = addr.Host
				}
				if specificity(addr.Path) > specificity(iLongestPath) {
					iLongestPath = addr.Path
				}
			}
			for _, addr := range p.serverBlocks[j].parsedKeys {
				if strings.Contains(addr.Host, "*") || addr.Host == "" {
					jWildcardHost = true
				}
				if specificity(addr.Host) > specificity(jLongestHost) {
					jLongestHost = addr.Host
				}
				if specificity(addr.Path) > specificity(jLongestPath) {
					jLongestPath = addr.Path
				}
			}
			// catch-all blocks (blocks with no hostname) should always go
			// last, even after blocks with wildcard hosts
			if specificity(iLongestHost) == 0 {
				return false
			}
			if specificity(jLongestHost) == 0 {
				return true
			}
			if iWildcardHost != jWildcardHost {
				// site blocks that have a key with a wildcard in the hostname
				// must always be less specific than blocks without one; see
				// https://github.com/caddyserver/caddy/issues/3410
				return jWildcardHost && !iWildcardHost
			}
			if specificity(iLongestHost) == specificity(jLongestHost) {
				return len(iLongestPath) > len(jLongestPath)
			}
			return specificity(iLongestHost) > specificity(jLongestHost)
		})

		var hasCatchAllTLSConnPolicy, addressQualifiesForTLS bool
		var emptyConnPolicies caddytls.ConnectionPolicies
		autoHTTPSWillAddConnPolicy := srv.AutoHTTPS == nil || !srv.AutoHTTPS.Disabled

		// if needed, the ServerLogConfig is initialized beforehand so
		// that all server blocks can populate it with data, even when not
		// coming with a log directive
		for _, sblock := range p.serverBlocks {
			if len(sblock.pile["custom_log"]) != 0 {
				srv.Logs = new(caddyhttp.ServerLogConfig)
				break
			}
		}

		// add named routes to the server if 'invoke' was used inside of it
		configuredNamedRoutes := options["named_routes"].(map[string]*caddyhttp.Route)
		namedRouteInvokes := options["named_route_invokes"].(map[string][]string)
		for _, sblock := range p.serverBlocks {
			if len(sblock.pile[namedRouteKey]) == 0 {
				continue
			}
			for _, value := range sblock.pile[namedRouteKey] {
				if srv.NamedRoutes == nil {
					srv.NamedRoutes = map[string]*caddyhttp.Route{}
				}
				// named routes may invoke other named routes, so
				// resolve the set of invoked names transitively
				names := []string{value.Value.(string)}
				for len(names) > 0 {
					name := names[0]
					names = names[1:]
					if _, ok := srv.NamedRoutes[name]; ok {
						continue
					}
					if configuredNamedRoutes[name] == nil {
						return nil, fmt.Errorf("cannot invoke named route '%s', which was not defined", name)
					}
					srv.NamedRoutes[name] = configuredNamedRoutes[name]
					names = append(names, namedRouteInvokes[name]...)
				}
			}
		}

		// create a subroute for each site in the server block
		for _, sblock := range p.serverBlocks {
			matcherSetsEnc, err := st.compileEncodedMatcherSets(sblock)
			if err != nil {
				return nil, fmt.Errorf("server block %v: compiling matcher sets: %v", sblock.block.Keys, err)
			}

			hosts := sblock.hostsFromKeys(false)

			// emit warnings if user put unspecified IP addresses; they probably want the bind directive
			for _, h := range hosts {
				if h == "0.0.0.0" || h == "::" {
					caddy.Log().Named("caddyfile").Warn("Site block has an unspecified IP address which only matches requests having that Host header; you probably want the 'bind' directive to configure the socket", zap.String("address", h))
				}
			}

			// collect hosts that are forced to be automated
			forceAutomatedNames := make(map[string]struct{})
			if _, ok := sblock.pile["tls.force_automate"]; ok {
				for _, host := range hosts {
					forceAutomatedNames[host] = struct{}{}
				}
			}

			// tls: connection policies
			if cpVals, ok := sblock.pile["tls.connection_policy"]; ok {
				// tls connection policies
				for _, cpVal := range cpVals {
					cp := cpVal.Value.(*caddytls.ConnectionPolicy)

					// make sure the policy covers all hostnames from the block
					for _, h := range hosts {
						if h == defaultSNI {
							hosts = append(hosts, "")
							cp.DefaultSNI = defaultSNI
							break
						}
						if h == fallbackSNI {
							hosts = append(hosts, "")
							cp.FallbackSNI = fallbackSNI
							break
						}
					}

					if len(hosts) > 0 {
						slices.Sort(hosts) // for deterministic JSON output
						cp.MatchersRaw = caddy.ModuleMap{
							"sni": caddyconfig.JSON(hosts, warnings), // make sure to match all hosts, not just auto-HTTPS-qualified ones
						}
					} else {
						cp.DefaultSNI = defaultSNI
						cp.FallbackSNI = fallbackSNI
					}

					// only append this policy if it actually changes something,
					// or if the configuration explicitly automates certs for
					// these names (this is necessary to hoist a connection policy
					// above one that may manually load a wildcard cert that would
					// otherwise clobber the automated one; the code that appends
					// policies that manually load certs comes later, so they're
					// lower in the list)
					if !cp.SettingsEmpty() || mapContains(forceAutomatedNames, hosts) {
						srv.TLSConnPolicies = append(srv.TLSConnPolicies, cp)
						hasCatchAllTLSConnPolicy = len(hosts) == 0
					} else if len(hosts) > 0 {
						emptyConnPolicies = append(emptyConnPolicies, cp)
					}
				}
			} else if specificHosts := slices.DeleteFunc(
				slices.Clone(hosts),
				func(h string) bool { return h == "" || strings.Contains(h, "*") },
			); len(specificHosts) > 0 {
				// site blocks with no TLS connection policy of their own may
				// still need an empty policy hoisted above a wildcard policy
				// that requires client authentication, or that requirement
				// would apply to their more specific hostnames too - see the
				// hoisting loop below and issue #7860
				slices.Sort(specificHosts)
				emptyConnPolicies = append(emptyConnPolicies, &caddytls.ConnectionPolicy{
					MatchersRaw: caddy.ModuleMap{
						"sni": caddyconfig.JSON(specificHosts, warnings),
					},
				})
			}

			for _, addr := range sblock.parsedKeys {
				// if server only uses HTTP port, auto-HTTPS will not apply
				if listenersUseAnyPortOtherThan(srv.Listen, httpPort) {
					// exclude any hosts that were defined explicitly with "http://"
					// in the key from automated cert management (issue #2998)
					if addr.Scheme == "http" && addr.Host != "" {
						if srv.AutoHTTPS == nil {
							srv.AutoHTTPS = new(caddyhttp.AutoHTTPSConfig)
						}
						if !slices.Contains(srv.AutoHTTPS.Skip, addr.Host) {
							srv.AutoHTTPS.Skip = append(srv.AutoHTTPS.Skip, addr.Host)
						}
					}
				}

				// If TLS is specified as directive, it will also result in 1 or more connection policy being created
				// Thus, catch-all address with non-standard port, e.g. :8443, can have TLS enabled without
				// specifying prefix "https://"
				// Second part of the condition is to allow creating TLS conn policy even though `auto_https` has been disabled
				// ensuring compatibility with behavior described in below link
				// https://caddy.community/t/making-sense-of-auto-https-and-why-disabling-it-still-serves-https-instead-of-http/9761
				createdTLSConnPolicies, ok := sblock.pile["tls.connection_policy"]
				hasTLSEnabled := (ok && len(createdTLSConnPolicies) > 0) ||
					(addr.Host != "" && (srv.AutoHTTPS == nil || !slices.Contains(srv.AutoHTTPS.Skip, addr.Host)))

				// we'll need to remember if the address qualifies for auto-HTTPS, so we
				// can add a TLS conn policy if necessary
				if addr.Scheme == "https" ||
					(addr.Scheme != "http" && addr.Port != httpPort && hasTLSEnabled) {
					addressQualifiesForTLS = true
				}

				// predict whether auto-HTTPS will add the conn policy for us; if so, we
				// may not need to add one for this server
				autoHTTPSWillAddConnPolicy = autoHTTPSWillAddConnPolicy &&
					(addr.Port == httpsPort || (addr.Port != httpPort && addr.Host != ""))
			}

			// Look for any config values that provide listener wrappers on the server block
			for _, listenerConfig := range sblock.pile["listener_wrapper"] {
				listenerWrapper, ok := listenerConfig.Value.(caddy.ListenerWrapper)
				if !ok {
					return nil, fmt.Errorf("config for a listener wrapper did not provide a value that implements caddy.ListenerWrapper")
				}
				jsonListenerWrapper := caddyconfig.JSONModuleObject(
					listenerWrapper,
					"wrapper",
					listenerWrapper.(caddy.Module).CaddyModule().ID.Name(),
					warnings,
				)
				srv.ListenerWrappersRaw = append(srv.ListenerWrappersRaw, jsonListenerWrapper)
			}

			// Look for any config values that provide packet conn wrappers on the server block
			for _, listenerConfig := range sblock.pile["packet_conn_wrapper"] {
				packetConnWrapper, ok := listenerConfig.Value.(caddy.PacketConnWrapper)
				if !ok {
					return nil, fmt.Errorf("config for a packet conn wrapper did not provide a value that implements caddy.PacketConnWrapper")
				}
				jsonPacketConnWrapper := caddyconfig.JSONModuleObject(
					packetConnWrapper,
					"wrapper",
					packetConnWrapper.(caddy.Module).CaddyModule().ID.Name(),
					warnings,
				)
				srv.PacketConnWrappersRaw = append(srv.PacketConnWrappersRaw, jsonPacketConnWrapper)
			}

			// set up each handler directive, making sure to honor directive order
			dirRoutes := sblock.pile["route"]
			siteSubroute, err := buildSubroute(dirRoutes, groupCounter, directiveOrderFor(options))
			if err != nil {
				return nil, err
			}

			// add the site block's route(s) to the server
			srv.Routes = appendSubrouteToRouteList(srv.Routes, siteSubroute, matcherSetsEnc, p, warnings)

			// if error routes are defined, add those too
			if errorSubrouteVals, ok := sblock.pile["error_route"]; ok {
				if srv.Errors == nil {
					srv.Errors = new(caddyhttp.HTTPErrorConfig)
				}
				sort.SliceStable(errorSubrouteVals, func(i, j int) bool {
					sri, srj := errorSubrouteVals[i].Value.(*caddyhttp.Subroute), errorSubrouteVals[j].Value.(*caddyhttp.Subroute)
					if len(sri.Routes[0].MatcherSetsRaw) == 0 && len(srj.Routes[0].MatcherSetsRaw) != 0 {
						return false
					}
					return true
				})
				errorsSubroute := &caddyhttp.Subroute{}
				for _, val := range errorSubrouteVals {
					sr := val.Value.(*caddyhttp.Subroute)
					errorsSubroute.Routes = append(errorsSubroute.Routes, sr.Routes...)
				}
				srv.Errors.Routes = appendSubrouteToRouteList(srv.Errors.Routes, errorsSubroute, matcherSetsEnc, p, warnings)
			}

			// add log associations
			// see https://github.com/caddyserver/caddy/issues/3310
			sblockLogHosts := sblock.hostsFromKeys(true)
			for _, cval := range sblock.pile["custom_log"] {
				ncl := cval.Value.(namedCustomLog)

				// if `no_hostname` is set, then this logger will not
				// be associated with any of the site block's hostnames,
				// and only be usable via the `log_name` directive
				// or the `access_logger_names` variable
				if ncl.noHostname {
					continue
				}

				if sblock.hasHostCatchAllKey() && len(ncl.hostnames) == 0 {
					// all requests for hosts not able to be listed should use
					// this log because it's a catch-all-hosts server block
					srv.Logs.DefaultLoggerName = ncl.name
				} else if len(ncl.hostnames) > 0 {
					// if the logger overrides the hostnames, map that to the logger name
					for _, h := range ncl.hostnames {
						if srv.Logs.LoggerNames == nil {
							srv.Logs.LoggerNames = make(map[string]caddyhttp.StringArray)
						}
						srv.Logs.LoggerNames[h] = append(srv.Logs.LoggerNames[h], ncl.name)
					}
				} else {
					// otherwise, map each host to the logger name
					for _, h := range sblockLogHosts {
						// strip the port from the host, if any
						host, _, err := net.SplitHostPort(h)
						if err != nil {
							host = h
						}
						if srv.Logs.LoggerNames == nil {
							srv.Logs.LoggerNames = make(map[string]caddyhttp.StringArray)
						}
						srv.Logs.LoggerNames[host] = append(srv.Logs.LoggerNames[host], ncl.name)
					}
				}
			}
			if srv.Logs != nil && len(sblock.pile["custom_log"]) == 0 {
				// server has access logs enabled, but this server block does not
				// enable access logs; therefore, all hosts of this server block
				// should not be access-logged
				if len(hosts) == 0 {
					// if the server block has a catch-all-hosts key, then we should
					// not log reqs to any host unless it appears in the map
					srv.Logs.SkipUnmappedHosts = true
				}
				srv.Logs.SkipHosts = append(srv.Logs.SkipHosts, sblockLogHosts...)
			}
		}

		// sort for deterministic JSON output
		if srv.Logs != nil {
			slices.Sort(srv.Logs.SkipHosts)
		}

		// a server cannot (natively) serve both HTTP and HTTPS at the
		// same time, so make sure the configuration isn't in conflict
		err := detectConflictingSchemes(srv, p.serverBlocks, options)
		if err != nil {
			return nil, err
		}

		// hostnames whose site blocks configure no TLS settings of their own
		// still need shielding if a policy matching a wildcard hostname would
		// otherwise impose CLIENT AUTHENTICATION on them. Because connection
		// policies are first-match, the shield hoisted above the wildcard
		// policy must be a COPY of that policy with only client_authentication
		// removed: an empty policy would not just lift the client-auth
		// requirement but suppress every other setting the wildcard policy
		// carries (certificate selection, protocol bounds, ALPN, ...), which
		// the covered hostname does want to inherit - see issue #7860
		// the wildcard names each client-auth policy matches, decoded once and
		// index-aligned with srv.TLSConnPolicies; nil for a policy that needs
		// no client auth or matches no wildcard
		clientAuthWildcards := make([][]string, len(srv.TLSConnPolicies))
		for i, cp := range srv.TLSConnPolicies {
			if cp.ClientAuthentication == nil {
				continue
			}
			names, ok := sniNames(cp, "of existing connection policy ", warnings)
			if !ok {
				continue
			}
			clientAuthWildcards[i] = slices.DeleteFunc(names, func(name string) bool {
				return !strings.Contains(name, "*")
			})
		}

		// each covering policy needs its OWN shield matching only the
		// hostnames it covers: the hostnames of a single site block may be
		// covered by DIFFERENT wildcards, and a shield hoisted above one
		// policy must not match the hostnames belonging to another, or it
		// would lift their client-auth requirement too
		shieldedHosts := make([][]string, len(srv.TLSConnPolicies))
		for _, ecp := range emptyConnPolicies {
			hosts, ok := sniNames(ecp, "", warnings)
			if !ok {
				continue // no SNI matcher to reason about
			}
			for _, host := range hosts {
				// connection policies are first-match, so only the first
				// covering policy is ever reached for this hostname
				for i, wildcards := range clientAuthWildcards {
					if slices.ContainsFunc(wildcards, func(name string) bool {
						return certmagic.MatchWildcard(host, name)
					}) {
						shieldedHosts[i] = append(shieldedHosts[i], host)
						break
					}
				}
			}
		}

		// hoist the shields last to last, so that inserting one does not
		// shift the index of a covering policy still to be shielded
		for i, hosts := range slices.Backward(shieldedHosts) {
			if len(hosts) == 0 {
				continue
			}
			slices.Sort(hosts)
			shield := *srv.TLSConnPolicies[i]
			shield.ClientAuthentication = nil
			shield.MatchersRaw = caddy.ModuleMap{
				"sni": caddyconfig.JSON(slices.Compact(hosts), warnings),
			}
			srv.TLSConnPolicies = slices.Insert(srv.TLSConnPolicies, i, &shield)
		}

		// a catch-all TLS conn policy is necessary to ensure TLS can
		// be offered to all hostnames of the server; even though only
		// one policy is needed to enable TLS for the server, that
		// policy might apply to only certain TLS handshakes; but when
		// using the Caddyfile, user would expect all handshakes to at
		// least have a matching connection policy, so here we append a
		// catch-all/default policy if there isn't one already (it's
		// important that it goes at the end) - see issue #3004:
		// https://github.com/caddyserver/caddy/issues/3004
		// TODO: maybe a smarter way to handle this might be to just make the
		// auto-HTTPS logic at provision-time detect if there is any connection
		// policy missing for any HTTPS-enabled hosts, if so, add it... maybe?
		if addressQualifiesForTLS &&
			!hasCatchAllTLSConnPolicy &&
			(len(srv.TLSConnPolicies) > 0 || !autoHTTPSWillAddConnPolicy || defaultSNI != "" || fallbackSNI != "") {
			srv.TLSConnPolicies = append(srv.TLSConnPolicies, &caddytls.ConnectionPolicy{
				DefaultSNI:  defaultSNI,
				FallbackSNI: fallbackSNI,
			})
		}

		// tidy things up a bit
		srv.TLSConnPolicies, err = consolidateConnPolicies(srv.TLSConnPolicies)
		if err != nil {
			return nil, fmt.Errorf("consolidating TLS connection policies for server %d: %v", i, err)
		}
		srv.Routes = consolidateRoutes(srv.Routes)

		servers[fmt.Sprintf("srv%d", i)] = srv
	}

	if err := applyServerOptions(servers, options, warnings); err != nil {
		return nil, fmt.Errorf("applying global server options: %v", err)
	}

	return servers, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (st *ServerType) serversFromPairings(
	pairings []sbAddrAssociation,
	options map[string]any,
	warnings *[]caddyconfig.Warning,
	groupCounter counter,
) (map[string]*caddyhttp.Server, error) {
	servers := make(map[string]*caddyhttp.Server)
	defaultSNI := tryString(options["default_sni"], warnings)
	fallbackSNI := tryString(options["fallback_sni"], warnings)

	httpPort := strconv.Itoa(caddyhttp.DefaultHTTPPort)
	if hp, ok := options["http_port"].(int); ok {
		httpPort = strconv.Itoa(hp)
	}
	httpsPort := strconv.Itoa(caddyhttp.DefaultHTTPSPort)
	if hsp, ok := options["https_port"].(int); ok {
		httpsPort = strconv.Itoa(hsp)
	}
	autoHTTPS := []string{}
	if ah, ok := options["auto_https"].([]string); ok {
		autoHTTPS = ah
	}

	for i, p := range pairings {
		// detect ambiguous site definitions: server blocks which
		// have the same host bound to the same interface (listener
		// address), otherwise their routes will improperly be added
		// to the same server (see issue #4635)
		for j, sblock1 := range p.serverBlocks {
			for _, key := range sblock1.block.GetKeysText() {
				for k, sblock2 := range p.serverBlocks {
					if k == j {
						continue
					}
					if slices.Contains(sblock2.block.GetKeysText(), key) {
						return nil, fmt.Errorf("ambiguous site definition: %s", key)
					}
				}
			}
		}

		var (
			addresses []string
			protocols [][]string
		)

		for _, addressWithProtocols := range p.addressesWithProtocols {
			addresses = append(addresses, addressWithProtocols.address)
			protocols = append(protocols, addressWithProtocols.protocols)
		}

		srv := &caddyhttp.Server{
			Listen:          addresses,
			ListenProtocols: protocols,
		}

		// remove srv.ListenProtocols[j] if it only contains the default protocols
		for j, lnProtocols := range srv.ListenProtocols {
			srv.ListenProtocols[j] = nil
			for _, lnProtocol := range lnProtocols {
				if lnProtocol != "" {
					srv.ListenProtocols[j] = lnProtocols
					break
				}
			}
		}

		// remove srv.ListenProtocols if it only contains the default protocols for all listen addresses
		listenProtocols := srv.ListenProtocols
		srv.ListenProtocols = nil
		for _, lnProtocols := range listenProtocols {
			if lnProtocols != nil {
				srv.ListenProtocols = listenProtocols
				break
			}
		}

		// handle the auto_https global option
		for _, val := range autoHTTPS {
			switch val {
			case "off":
				if srv.AutoHTTPS == nil {
					srv.AutoHTTPS = new(caddyhttp.AutoHTTPSConfig)
				}
				srv.AutoHTTPS.Disabled = true

			case "disable_redirects":
				if srv.AutoHTTPS == nil {
					srv.AutoHTTPS = new(caddyhttp.AutoHTTPSConfig)
				}
				srv.AutoHTTPS.DisableRedir = true

			case "disable_certs":
				if srv.AutoHTTPS == nil {
					srv.AutoHTTPS = new(caddyhttp.AutoHTTPSConfig)
				}
				srv.AutoHTTPS.DisableCerts = true

			case "ignore_loaded_certs":
				if srv.AutoHTTPS == nil {
					srv.AutoHTTPS = new(caddyhttp.AutoHTTPSConfig)
				}
				srv.AutoHTTPS.IgnoreLoadedCerts = true
			}
		}

		// Using paths in site addresses is deprecated
		// See ParseAddress() where parsing should later reject paths
		// See https://github.com/caddyserver/caddy/pull/4728 for a full explanation
		for _, sblock := range p.serverBlocks {
			for _, addr := range sblock.parsedKeys {
				if addr.Path != "" {
					caddy.Log().Named("caddyfile").Warn("Using a path in a site address is deprecated; please use the 'handle' directive instead", zap.String("address", addr.String()))
				}
			}
		}

		// sort server blocks by their keys; this is important because
		// only the first matching site should be evaluated, and we should
		// attempt to match most specific site first (host and path), in
		// case their matchers overlap; we do this somewhat naively by
		// descending sort by length of host then path
		sort.SliceStable(p.serverBlocks, func(i, j int) bool {
			// TODO: we could pre-process the specificities for efficiency,
			// but I don't expect many blocks will have THAT many keys...
			var iLongestPath, jLongestPath string
			var iLongestHost, jLongestHost string
			var iWildcardHost, jWildcardHost bool
			for _, addr := range p.serverBlocks[i].parsedKeys {
				if strings.Contains(addr.Host, "*") || addr.Host == "" {
					iWildcardHost = true
				}
				if specificity(addr.Host) > specificity(iLongestHost) {
					iLongestHost = addr.Host
				}
				if specificity(addr.Path) > specificity(iLongestPath) {
					iLongestPath = addr.Path
				}
			}
			for _, addr := range p.serverBlocks[j].parsedKeys {
				if strings.Contains(addr.Host, "*") || addr.Host == "" {
					jWildcardHost = true
				}
				if specificity(addr.Host) > specificity(jLongestHost) {
					jLongestHost = addr.Host
				}
				if specificity(addr.Path) > specificity(jLongestPath) {
					jLongestPath = addr.Path
				}
			}
			// catch-all blocks (blocks with no hostname) should always go
			// last, even after blocks with wildcard hosts
			if specificity(iLongestHost) == 0 {
				return false
			}
			if specificity(jLongestHost) == 0 {
				return true
			}
			if iWildcardHost != jWildcardHost {
				// site blocks that have a key with a wildcard in the hostname
				// must always be less specific than blocks without one; see
				// https://github.com/caddyserver/caddy/issues/3410
				return jWildcardHost && !iWildcardHost
			}
			if specificity(iLongestHost) == specificity(jLongestHost) {
				return len(iLongestPath) > len(jLongestPath)
			}
			return specificity(iLongestHost) > specificity(jLongestHost)
		})

		var hasCatchAllTLSConnPolicy, addressQualifiesForTLS bool
		var emptyConnPolicies caddytls.ConnectionPolicies
		autoHTTPSWillAddConnPolicy := srv.AutoHTTPS == nil || !srv.AutoHTTPS.Disabled

		// if needed, the ServerLogConfig is initialized beforehand so
		// that all server blocks can populate it with data, even when not
		// coming with a log directive
		for _, sblock := range p.serverBlocks {
			if len(sblock.pile["custom_log"]) != 0 {
				srv.Logs = new(caddyhttp.ServerLogConfig)
				break
			}
		}

		// add named routes to the server if 'invoke' was used inside of it
		configuredNamedRoutes := options["named_routes"].(map[string]*caddyhttp.Route)
		namedRouteInvokes := options["named_route_invokes"].(map[string][]string)
		for _, sblock := range p.serverBlocks {
			if len(sblock.pile[namedRouteKey]) == 0 {
				continue
			}
			for _, value := range sblock.pile[namedRouteKey] {
				if srv.NamedRoutes == nil {
					srv.NamedRoutes = map[string]*caddyhttp.Route{}
				}
				// named routes may invoke other named routes, so
				// resolve the set of invoked names transitively
				names := []string{value.Value.(string)}
				for len(names) > 0 {
					name := names[0]
					names = names[1:]
					if _, ok := srv.NamedRoutes[name]; ok {
						continue
					}
					if configuredNamedRoutes[name] == nil {
						return nil, fmt.Errorf("cannot invoke named route '%s', which was not defined", name)
					}
					srv.NamedRoutes[name] = configuredNamedRoutes[name]
					names = append(names, namedRouteInvokes[name]...)
				}
			}
		}

		// create a subroute for each site in the server block
		for _, sblock := range p.serverBlocks {
			matcherSetsEnc, err := st.compileEncodedMatcherSets(sblock)
			if err != nil {
				return nil, fmt.Errorf("server block %v: compiling matcher sets: %v", sblock.block.Keys, err)
			}

			hosts := sblock.hostsFromKeys(false)

			// emit warnings if user put unspecified IP addresses; they probably want the bind directive
			for _, h := range hosts {
				if h == "0.0.0.0" || h == "::" {
					caddy.Log().Named("caddyfile").Warn("Site block has an unspecified IP address which only matches requests having that Host header; you probably want the 'bind' directive to configure the socket", zap.String("address", h))
				}
			}

			// collect hosts that are forced to be automated
			forceAutomatedNames := make(map[string]struct{})
			if _, ok := sblock.pile["tls.force_automate"]; ok {
				for _, host := range hosts {
					forceAutomatedNames[host] = struct{}{}
				}
			}

			// tls: connection policies
			if cpVals, ok := sblock.pile["tls.connection_policy"]; ok {
				// tls connection policies
				for _, cpVal := range cpVals {
					// Policies are parsed once per original server block. Each listener
					// rewrites and consolidates them independently.
					cp, err := cloneConnectionPolicy(cpVal.Value.(*caddytls.ConnectionPolicy))
					if err != nil {
						return nil, fmt.Errorf("cloning TLS connection policy: %v", err)
					}

					// make sure the policy covers all hostnames from the block
					for _, h := range hosts {
						if h == defaultSNI {
							hosts = append(hosts, "")
							cp.DefaultSNI = defaultSNI
							break
						}
						if h == fallbackSNI {
							hosts = append(hosts, "")
							cp.FallbackSNI = fallbackSNI
							break
						}
					}

					if len(hosts) > 0 {
						slices.Sort(hosts) // for deterministic JSON output
						cp.MatchersRaw = caddy.ModuleMap{
							"sni": caddyconfig.JSON(hosts, warnings), // make sure to match all hosts, not just auto-HTTPS-qualified ones
						}
					} else {
						cp.DefaultSNI = defaultSNI
						cp.FallbackSNI = fallbackSNI
					}

					// only append this policy if it actually changes something,
					// or if the configuration explicitly automates certs for
					// these names (this is necessary to hoist a connection policy
					// above one that may manually load a wildcard cert that would
					// otherwise clobber the automated one; the code that appends
					// policies that manually load certs comes later, so they're
					// lower in the list)
					if !cp.SettingsEmpty() || mapContains(forceAutomatedNames, hosts) {
						srv.TLSConnPolicies = append(srv.TLSConnPolicies, cp)
						hasCatchAllTLSConnPolicy = len(hosts) == 0
					} else if len(hosts) > 0 {
						emptyConnPolicies = append(emptyConnPolicies, cp)
					}
				}
			} else if specificHosts := slices.DeleteFunc(
				slices.Clone(hosts),
				func(h string) bool { return h == "" || strings.Contains(h, "*") },
			); len(specificHosts) > 0 {
				// site blocks with no TLS connection policy of their own may
				// still need an empty policy hoisted above a wildcard policy
				// that requires client authentication, or that requirement
				// would apply to their more specific hostnames too - see the
				// hoisting loop below and issue #7860
				slices.Sort(specificHosts)
				emptyConnPolicies = append(emptyConnPolicies, &caddytls.ConnectionPolicy{
					MatchersRaw: caddy.ModuleMap{
						"sni": caddyconfig.JSON(specificHosts, warnings),
					},
				})
			}

			for _, addr := range sblock.parsedKeys {
				// if server only uses HTTP port, auto-HTTPS will not apply
				if listenersUseAnyPortOtherThan(srv.Listen, httpPort) {
					// exclude any hosts that were defined explicitly with "http://"
					// in the key from automated cert management (issue #2998)
					if addr.Scheme == "http" && addr.Host != "" {
						if srv.AutoHTTPS == nil {
							srv.AutoHTTPS = new(caddyhttp.AutoHTTPSConfig)
						}
						if !slices.Contains(srv.AutoHTTPS.Skip, addr.Host) {
							srv.AutoHTTPS.Skip = append(srv.AutoHTTPS.Skip, addr.Host)
						}
					}
				}

				// If TLS is specified as directive, it will also result in 1 or more connection policy being created
				// Thus, catch-all address with non-standard port, e.g. :8443, can have TLS enabled without
				// specifying prefix "https://"
				// Second part of the condition is to allow creating TLS conn policy even though `auto_https` has been disabled
				// ensuring compatibility with behavior described in below link
				// https://caddy.community/t/making-sense-of-auto-https-and-why-disabling-it-still-serves-https-instead-of-http/9761
				createdTLSConnPolicies, ok := sblock.pile["tls.connection_policy"]
				hasTLSEnabled := (ok && len(createdTLSConnPolicies) > 0) ||
					(addr.Host != "" && (srv.AutoHTTPS == nil || !slices.Contains(srv.AutoHTTPS.Skip, addr.Host)))

				// we'll need to remember if the address qualifies for auto-HTTPS, so we
				// can add a TLS conn policy if necessary
				if addr.Scheme == "https" ||
					(addr.Scheme != "http" && addr.Port != httpPort && hasTLSEnabled) {
					addressQualifiesForTLS = true
				}

				// predict whether auto-HTTPS will add the conn policy for us; if so, we
				// may not need to add one for this server
				autoHTTPSWillAddConnPolicy = autoHTTPSWillAddConnPolicy &&
					(addr.Port == httpsPort || (addr.Port != httpPort && addr.Host != ""))
			}

			// Look for any config values that provide listener wrappers on the server block
			for _, listenerConfig := range sblock.pile["listener_wrapper"] {
				listenerWrapper, ok := listenerConfig.Value.(caddy.ListenerWrapper)
				if !ok {
					return nil, fmt.Errorf("config for a listener wrapper did not provide a value that implements caddy.ListenerWrapper")
				}
				jsonListenerWrapper := caddyconfig.JSONModuleObject(
					listenerWrapper,
					"wrapper",
					listenerWrapper.(caddy.Module).CaddyModule().ID.Name(),
					warnings,
				)
				srv.ListenerWrappersRaw = append(srv.ListenerWrappersRaw, jsonListenerWrapper)
			}

			// Look for any config values that provide packet conn wrappers on the server block
			for _, listenerConfig := range sblock.pile["packet_conn_wrapper"] {
				packetConnWrapper, ok := listenerConfig.Value.(caddy.PacketConnWrapper)
				if !ok {
					return nil, fmt.Errorf("config for a packet conn wrapper did not provide a value that implements caddy.PacketConnWrapper")
				}
				jsonPacketConnWrapper := caddyconfig.JSONModuleObject(
					packetConnWrapper,
					"wrapper",
					packetConnWrapper.(caddy.Module).CaddyModule().ID.Name(),
					warnings,
				)
				srv.PacketConnWrappersRaw = append(srv.PacketConnWrappersRaw, jsonPacketConnWrapper)
			}

			// set up each handler directive, making sure to honor directive order
			dirRoutes := sblock.pile["route"]
			siteSubroute, err := buildSubroute(dirRoutes, groupCounter, directiveOrderFor(options))
			if err != nil {
				return nil, err
			}

			// add the site block's route(s) to the server
			srv.Routes = appendSubrouteToRouteList(srv.Routes, siteSubroute, matcherSetsEnc, p, warnings)

			// if error routes are defined, add those too
			if errorSubrouteVals, ok := sblock.pile["error_route"]; ok {
				if srv.Errors == nil {
					srv.Errors = new(caddyhttp.HTTPErrorConfig)
				}
				sort.SliceStable(errorSubrouteVals, func(i, j int) bool {
					sri, srj := errorSubrouteVals[i].Value.(*caddyhttp.Subroute), errorSubrouteVals[j].Value.(*caddyhttp.Subroute)
					if len(sri.Routes[0].MatcherSetsRaw) == 0 && len(srj.Routes[0].MatcherSetsRaw) != 0 {
						return false
					}
					return true
				})
				errorsSubroute := &caddyhttp.Subroute{}
				for _, val := range errorSubrouteVals {
					sr := val.Value.(*caddyhttp.Subroute)
					errorsSubroute.Routes = append(errorsSubroute.Routes, sr.Routes...)
				}
				srv.Errors.Routes = appendSubrouteToRouteList(srv.Errors.Routes, errorsSubroute, matcherSetsEnc, p, warnings)
			}

			// add log associations
			// see https://github.com/caddyserver/caddy/issues/3310
			sblockLogHosts := sblock.hostsFromKeys(true)
			for _, cval := range sblock.pile["custom_log"] {
				ncl := cval.Value.(namedCustomLog)

				// if `no_hostname` is set, then this logger will not
				// be associated with any of the site block's hostnames,
				// and only be usable via the `log_name` directive
				// or the `access_logger_names` variable
				if ncl.noHostname {
					continue
				}

				if sblock.hasHostCatchAllKey() && len(ncl.hostnames) == 0 {
					// all requests for hosts not able to be listed should use
					// this log because it's a catch-all-hosts server block
					srv.Logs.DefaultLoggerName = ncl.name
				} else if len(ncl.hostnames) > 0 {
					// if the logger overrides the hostnames, map that to the logger name
					for _, h := range ncl.hostnames {
						if srv.Logs.LoggerNames == nil {
							srv.Logs.LoggerNames = make(map[string]caddyhttp.StringArray)
						}
						srv.Logs.LoggerNames[h] = append(srv.Logs.LoggerNames[h], ncl.name)
					}
				} else {
					// otherwise, map each host to the logger name
					for _, h := range sblockLogHosts {
						// strip the port from the host, if any
						host, _, err := net.SplitHostPort(h)
						if err != nil {
							host = h
						}
						if srv.Logs.LoggerNames == nil {
							srv.Logs.LoggerNames = make(map[string]caddyhttp.StringArray)
						}
						srv.Logs.LoggerNames[host] = append(srv.Logs.LoggerNames[host], ncl.name)
					}
				}
			}
			if srv.Logs != nil && len(sblock.pile["custom_log"]) == 0 {
				// server has access logs enabled, but this server block does not
				// enable access logs; therefore, all hosts of this server block
				// should not be access-logged
				if len(hosts) == 0 {
					// if the server block has a catch-all-hosts key, then we should
					// not log reqs to any host unless it appears in the map
					srv.Logs.SkipUnmappedHosts = true
				}
				srv.Logs.SkipHosts = append(srv.Logs.SkipHosts, sblockLogHosts...)
			}
		}

		// sort for deterministic JSON output
		if srv.Logs != nil {
			slices.Sort(srv.Logs.SkipHosts)
		}

		// a server cannot (natively) serve both HTTP and HTTPS at the
		// same time, so make sure the configuration isn't in conflict
		err := detectConflictingSchemes(srv, p.serverBlocks, options)
		if err != nil {
			return nil, err
		}

		// hostnames whose site blocks configure no TLS settings of their own
		// still need shielding if a policy matching a wildcard hostname would
		// otherwise impose CLIENT AUTHENTICATION on them. Because connection
		// policies are first-match, the shield hoisted above the wildcard
		// policy must be a COPY of that policy with only client_authentication
		// removed: an empty policy would not just lift the client-auth
		// requirement but suppress every other setting the wildcard policy
		// carries (certificate selection, protocol bounds, ALPN, ...), which
		// the covered hostname does want to inherit - see issue #7860
		// the wildcard names each client-auth policy matches, decoded once and
		// index-aligned with srv.TLSConnPolicies; nil for a policy that needs
		// no client auth or matches no wildcard
		clientAuthWildcards := make([][]string, len(srv.TLSConnPolicies))
		for i, cp := range srv.TLSConnPolicies {
			if cp.ClientAuthentication == nil {
				continue
			}
			names, ok := sniNames(cp, "of existing connection policy ", warnings)
			if !ok {
				continue
			}
			clientAuthWildcards[i] = slices.DeleteFunc(names, func(name string) bool {
				return !strings.Contains(name, "*")
			})
		}

		// each covering policy needs its OWN shield matching only the
		// hostnames it covers: the hostnames of a single site block may be
		// covered by DIFFERENT wildcards, and a shield hoisted above one
		// policy must not match the hostnames belonging to another, or it
		// would lift their client-auth requirement too
		shieldedHosts := make([][]string, len(srv.TLSConnPolicies))
		for _, ecp := range emptyConnPolicies {
			hosts, ok := sniNames(ecp, "", warnings)
			if !ok {
				continue // no SNI matcher to reason about
			}
			for _, host := range hosts {
				// connection policies are first-match, so only the first
				// covering policy is ever reached for this hostname
				for i, wildcards := range clientAuthWildcards {
					if slices.ContainsFunc(wildcards, func(name string) bool {
						return certmagic.MatchWildcard(host, name)
					}) {
						shieldedHosts[i] = append(shieldedHosts[i], host)
						break
					}
				}
			}
		}

		// hoist the shields last to last, so that inserting one does not
		// shift the index of a covering policy still to be shielded
		for i, hosts := range slices.Backward(shieldedHosts) {
			if len(hosts) == 0 {
				continue
			}
			slices.Sort(hosts)
			shield := *srv.TLSConnPolicies[i]
			shield.ClientAuthentication = nil
			shield.MatchersRaw = caddy.ModuleMap{
				"sni": caddyconfig.JSON(slices.Compact(hosts), warnings),
			}
			srv.TLSConnPolicies = slices.Insert(srv.TLSConnPolicies, i, &shield)
		}

		// a catch-all TLS conn policy is necessary to ensure TLS can
		// be offered to all hostnames of the server; even though only
		// one policy is needed to enable TLS for the server, that
		// policy might apply to only certain TLS handshakes; but when
		// using the Caddyfile, user would expect all handshakes to at
		// least have a matching connection policy, so here we append a
		// catch-all/default policy if there isn't one already (it's
		// important that it goes at the end) - see issue #3004:
		// https://github.com/caddyserver/caddy/issues/3004
		// TODO: maybe a smarter way to handle this might be to just make the
		// auto-HTTPS logic at provision-time detect if there is any connection
		// policy missing for any HTTPS-enabled hosts, if so, add it... maybe?
		if addressQualifiesForTLS &&
			!hasCatchAllTLSConnPolicy &&
			(len(srv.TLSConnPolicies) > 0 || !autoHTTPSWillAddConnPolicy || defaultSNI != "" || fallbackSNI != "") {
			srv.TLSConnPolicies = append(srv.TLSConnPolicies, &caddytls.ConnectionPolicy{
				DefaultSNI:  defaultSNI,
				FallbackSNI: fallbackSNI,
			})
		}

		// tidy things up a bit
		srv.TLSConnPolicies, err = consolidateConnPolicies(srv.TLSConnPolicies)
		if err != nil {
			return nil, fmt.Errorf("consolidating TLS connection policies for server %d: %v", i, err)
		}
		srv.Routes = consolidateRoutes(srv.Routes)

		servers[fmt.Sprintf("srv%d", i)] = srv
	}

	if err := applyServerOptions(servers, options, warnings); err != nil {
		return nil, fmt.Errorf("applying global server options: %v", err)
	}

	return servers, nil
}
```


---

### 🔹 Commit #07: `5538b947`
- **完整 Hash**: `5538b947d2873e8a06dd45182b8c43081fc56d32`
- **說明 (Ground Truth)**: caddyhttp: skip matchers for satisfied route groups (#8189)
- **變更檔案數**: 1

#### 📄 檔案: `modules/caddyhttp/routes.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:48, E:63, A:0) ➔ After(N:49, E:63, A:0)
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
  • + [新增節點] `groups` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `wrapRoute()`
- **變更前簽章 (Before)**: `func wrapRoute(route Route)` (L256~L326)
- **變更後簽章 (After)**: `func wrapRoute(route Route)` (L256~L329)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func wrapRoute(route Route) Middleware {
	return func(next Handler) Handler {
		return HandlerFunc(func(rw http.ResponseWriter, req *http.Request) error {
			// TODO: Update this comment, it seems we've moved the copy into the handler?
			// copy the next handler (it's an interface, so it's just
			// a very lightweight copy of a pointer); this is important
			// because this is a closure to the func below, which
			// re-assigns the value as it compiles the middleware stack;
			// if we don't make this copy, we'd affect the underlying
			// pointer for all future request (yikes); we could
			// alternatively solve this by moving the func below out of
			// this closure and into a standalone package-level func,
			// but I just thought this made more sense
			nextCopy := next

			// route must match at least one of the matcher sets
			matches, err := route.MatcherSets.AnyMatchWithError(req)
			if err != nil {
				// allow matchers the opportunity to short circuit
				// the request and trigger the error handling chain
				return err
			}
			if !matches {
				// call the next handler, and skip this one,
				// since the matcher didn't match
				return nextCopy.ServeHTTP(rw, req)
			}

			// if route is part of a group, ensure only the
			// first matching route in the group is applied
			if route.Group != "" {
				groups := req.Context().Value(routeGroupCtxKey).(map[string]struct{})

				if _, ok := groups[route.Group]; ok {
					// this group has already been
					// satisfied by a matching route
					return nextCopy.ServeHTTP(rw, req)
				}

				// this matching route satisfies the group
				groups[route.Group] = struct{}{}
			}

			// make terminal routes terminate
			if route.Terminal {
				if _, ok := req.Context().Value(ErrorCtxKey).(error); ok {
					nextCopy = errorEmptyHandler
				} else {
					nextCopy = emptyHandler
				}
			}

			// compile this route's handler stack
			for _, middleware := range slices.Backward(route.middleware) {
				nextCopy = middleware(nextCopy)
			}

			// Apply metrics instrumentation once for the entire route,
			// rather than wrapping each individual handler. This avoids
			// redundant metrics collection that caused significant CPU
			// overhead (see issue #4644).
			if route.metrics != nil {
				nextCopy = newMetricsInstrumentedRoute(
					route.metricsCtx, route.handlerName, nextCopy, route.metrics,
				)
			}

			return nextCopy.ServeHTTP(rw, req)
		})
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func wrapRoute(route Route) Middleware {
	return func(next Handler) Handler {
		return HandlerFunc(func(rw http.ResponseWriter, req *http.Request) error {
			// TODO: Update this comment, it seems we've moved the copy into the handler?
			// copy the next handler (it's an interface, so it's just
			// a very lightweight copy of a pointer); this is important
			// because this is a closure to the func below, which
			// re-assigns the value as it compiles the middleware stack;
			// if we don't make this copy, we'd affect the underlying
			// pointer for all future request (yikes); we could
			// alternatively solve this by moving the func below out of
			// this closure and into a standalone package-level func,
			// but I just thought this made more sense
			nextCopy := next

			// if route is part of a group, ensure only the
			// first matching route in the group is applied
			var groups map[string]struct{}
			if route.Group != "" {
				groups = req.Context().Value(routeGroupCtxKey).(map[string]struct{})

				if _, ok := groups[route.Group]; ok {
					// this group has already been satisfied by a
					// matching route; skip without running matchers
					return nextCopy.ServeHTTP(rw, req)
				}
			}

			// route must match at least one of the matcher sets
			matches, err := route.MatcherSets.AnyMatchWithError(req)
			if err != nil {
				// allow matchers the opportunity to short circuit
				// the request and trigger the error handling chain
				return err
			}
			if !matches {
				// call the next handler, and skip this one,
				// since the matcher didn't match
				return nextCopy.ServeHTTP(rw, req)
			}

			// this matching route satisfies the group
			if groups != nil {
				groups[route.Group] = struct{}{}
			}

			// make terminal routes terminate
			if route.Terminal {
				if _, ok := req.Context().Value(ErrorCtxKey).(error); ok {
					nextCopy = errorEmptyHandler
				} else {
					nextCopy = emptyHandler
				}
			}

			// compile this route's handler stack
			for _, middleware := range slices.Backward(route.middleware) {
				nextCopy = middleware(nextCopy)
			}

			// Apply metrics instrumentation once for the entire route,
			// rather than wrapping each individual handler. This avoids
			// redundant metrics collection that caused significant CPU
			// overhead (see issue #4644).
			if route.metrics != nil {
				nextCopy = newMetricsInstrumentedRoute(
					route.metricsCtx, route.handlerName, nextCopy, route.metrics,
				)
			}

			return nextCopy.ServeHTTP(rw, req)
		})
	}
}
```


---

### 🔹 Commit #08: `c8591a1e`
- **完整 Hash**: `c8591a1e46e4d0e39b6ca20633c44cd42f874f71`
- **說明 (Ground Truth)**: httpcaddyfile: keep a site block's TLS policy for ECH public names (#8156)
- **變更檔案數**: 1

#### 📄 檔案: `caddyconfig/httpcaddyfile/tlsapp.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:93, E:131, A:0) ➔ After(N:95, E:136, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 5, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `strings.TrimSpace (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `automationPolicyCoversName` (FUNCTION_DEF)
  • + [新增呼叫邊] `ServerType.buildTLSApp` ──[CALLS]──> `automationPolicyCoversName`
  • + [新增呼叫邊] `automationPolicyCoversName` ──[CALLS]──> `strings.ToLower (External/Pkg)`
  • + [新增呼叫邊] `automationPolicyCoversName` ──[CALLS]──> `strings.TrimSpace (External/Pkg)`
  • + [新增呼叫邊] `automationPolicyCoversName` ──[CALLS]──> `slices.ContainsFunc (External/Pkg)`
  • + [新增呼叫邊] `automationPolicyCoversName` ──[CALLS]──> `certmagic.MatchWildcard (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `ServerType.buildTLSApp()`
- **變更前簽章 (Before)**: `func ServerType.buildTLSApp(
	pairings []sbAddrAssociation,
	options map[string]any,
	warnings []caddyconfig.Warning,
)` (L36~L559)
- **變更後簽章 (After)**: `func ServerType.buildTLSApp(
	pairings []sbAddrAssociation,
	options map[string]any,
	warnings []caddyconfig.Warning,
)` (L36~L566)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (st ServerType) buildTLSApp(
	pairings []sbAddrAssociation,
	options map[string]any,
	warnings []caddyconfig.Warning,
) (*caddytls.TLS, []caddyconfig.Warning, error) {
	tlsApp := &caddytls.TLS{CertificatesRaw: make(caddy.ModuleMap)}
	var certLoaders []caddytls.CertificateLoader

	httpPort := strconv.Itoa(caddyhttp.DefaultHTTPPort)
	if hp, ok := options["http_port"].(int); ok {
		httpPort = strconv.Itoa(hp)
	}
	autoHTTPS := []string{}
	if ah, ok := options["auto_https"].([]string); ok {
		autoHTTPS = ah
	}

	// find all hosts that share a server block with a hostless
	// key, so that they don't get forgotten/omitted by auto-HTTPS
	// (since they won't appear in route matchers)
	httpsHostsSharedWithHostlessKey := make(map[string]struct{})
	if !slices.Contains(autoHTTPS, "off") {
		for _, pair := range pairings {
			for _, sb := range pair.serverBlocks {
				for _, addr := range sb.parsedKeys {
					if addr.Host != "" {
						continue
					}

					// this server block has a hostless key, now
					// go through and add all the hosts to the set
					for _, otherAddr := range sb.parsedKeys {
						if otherAddr.Original == addr.Original {
							continue
						}
						if otherAddr.Host != "" && otherAddr.Scheme != "http" && otherAddr.Port != httpPort {
							httpsHostsSharedWithHostlessKey[otherAddr.Host] = struct{}{}
						}
					}
					break
				}
			}
		}
	}

	// a catch-all automation policy is used as a "default" for all subjects that
	// don't have custom configuration explicitly associated with them; this
	// is only to add if the global settings or defaults are non-empty
	catchAllAP, err := newBaseAutomationPolicy(options, warnings, false)
	if err != nil {
		return nil, warnings, err
	}
	if catchAllAP != nil {
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.Policies = append(tlsApp.Automation.Policies, catchAllAP)
	}

	forcedAutomatedNames := make(map[string]struct{}) // explicitly configured to be automated, even if covered by a wildcard

	for _, p := range pairings {
		// avoid setting up TLS automation policies for a server that is HTTP-only
		var addresses []string
		for _, addressWithProtocols := range p.addressesWithProtocols {
			addresses = append(addresses, addressWithProtocols.address)
		}
		if !listenersUseAnyPortOtherThan(addresses, httpPort) {
			continue
		}

		for _, sblock := range p.serverBlocks {
			// check the scheme of all the site addresses,
			// skip building AP if they all had http://
			if sblock.isAllHTTP() {
				continue
			}

			// get values that populate an automation policy for this block
			ap, err := newBaseAutomationPolicy(options, warnings, true)
			if err != nil {
				return nil, warnings, err
			}

			sblockHosts := sblock.hostsFromKeys(false)
			if len(sblockHosts) == 0 && catchAllAP != nil {
				ap = catchAllAP
			}

			// on-demand tls
			if _, ok := sblock.pile["tls.on_demand"]; ok {
				ap.OnDemand = true
			}

			// collect hosts that are forced to have certs automated for their specific name
			if _, ok := sblock.pile["tls.force_automate"]; ok {
				for _, host := range sblockHosts {
					forcedAutomatedNames[host] = struct{}{}
				}
			}

			// reuse private keys tls
			if _, ok := sblock.pile["tls.reuse_private_keys"]; ok {
				ap.ReusePrivateKeys = true
			}

			if keyTypeVals, ok := sblock.pile["tls.key_type"]; ok {
				ap.KeyType = keyTypeVals[0].Value.(string)
			}

			if renewalWindowRatioVals, ok := sblock.pile["tls.renewal_window_ratio"]; ok {
				ap.RenewalWindowRatio = renewalWindowRatioVals[0].Value.(float64)
			} else if globalRenewalWindowRatio, ok := options["renewal_window_ratio"]; ok {
				ap.RenewalWindowRatio = globalRenewalWindowRatio.(float64)
			}

			// certificate issuers
			if issuerVals, ok := sblock.pile["tls.cert_issuer"]; ok {
				var issuers []certmagic.Issuer
				for _, issuerVal := range issuerVals {
					issuers = append(issuers, issuerVal.Value.(certmagic.Issuer))
				}
				if ap == catchAllAP && !reflect.DeepEqual(ap.Issuers, issuers) {
					// this more correctly implements an error check that was removed
					// below; try it with this config:
					//
					// :443 {
					// 	bind 127.0.0.1
					// }
					//
					// :443 {
					// 	bind ::1
					// 	tls {
					// 		issuer acme
					// 	}
					// }
					return nil, warnings, fmt.Errorf("automation policy from site block is also default/catch-all policy because of key without hostname, and the two are in conflict: %#v != %#v", ap.Issuers, issuers)
				}
				ap.Issuers = issuers
			}

			// certificate managers
			if certManagerVals, ok := sblock.pile["tls.cert_manager"]; ok {
				for _, certManager := range certManagerVals {
					certGetterName := certManager.Value.(caddy.Module).CaddyModule().ID.Name()
					ap.ManagersRaw = append(ap.ManagersRaw, caddyconfig.JSONModuleObject(certManager.Value, "via", certGetterName, &warnings))
				}
			}
			// custom bind host
			for _, cfgVal := range sblock.pile["bind"] {
				for _, iss := range ap.Issuers {
					// if an issuer was already configured and it is NOT an ACME issuer,
					// skip, since we intend to adjust only ACME issuers; ensure we
					// include any issuer that embeds/wraps an underlying ACME issuer
					var acmeIssuer *caddytls.ACMEIssuer
					if acmeWrapper, ok := iss.(acmeCapable); ok {
						acmeIssuer = acmeWrapper.GetACMEIssuer()
					}
					if acmeIssuer == nil {
						continue
					}

					// proceed to configure the ACME issuer's bind host, without
					// overwriting any existing settings
					if acmeIssuer.Challenges == nil {
						acmeIssuer.Challenges = new(caddytls.ChallengesConfig)
					}
					if acmeIssuer.Challenges.BindHost == "" {
						// only binding to one host is supported
						var bindHost string
						if asserted, ok := cfgVal.Value.(addressesWithProtocols); ok && len(asserted.addresses) > 0 {
							bindHost = asserted.addresses[0]
						}
						acmeIssuer.Challenges.BindHost = bindHost
					}
				}
			}

			// we used to ensure this block is allowed to create an automation policy;
			// doing so was forbidden if it has a key with no host (i.e. ":443")
			// and if there is a different server block that also has a key with no
			// host -- since a key with no host matches any host, we need its
			// associated automation policy to have an empty Subjects list, i.e. no
			// host filter, which is indistinguishable between the two server blocks
			// because automation is not done in the context of a particular server...
			// this is an example of a poor mapping from Caddyfile to JSON but that's
			// the least-leaky abstraction I could figure out -- however, this check
			// was preventing certain listeners, like those provided by plugins, from
			// being used as desired (see the Tailscale listener plugin), so I removed
			// the check: and I think since I originally wrote the check I added a new
			// check above which *properly* detects this ambiguity without breaking the
			// listener plugin; see the check above with a commented example config
			if len(sblockHosts) == 0 && catchAllAP == nil {
				// this server block has a key with no hosts, but there is not yet
				// a catch-all automation policy (probably because no global options
				// were set), so this one becomes it
				catchAllAP = ap
			}

			hostsNotHTTP := sblock.hostsFromKeysNotHTTP(httpPort)
			sort.Strings(hostsNotHTTP) // solely for deterministic test results

			// associate our new automation policy with this server block's hosts
			ap.SubjectsRaw = hostsNotHTTP

			// if a combination of public and internal names were given
			// for this same server block and no issuer was specified, we
			// need to separate them out in the automation policies so
			// that the internal names can use the internal issuer and
			// the other names can use the default/public/ACME issuer
			var ap2 *caddytls.AutomationPolicy
			if len(ap.Issuers) == 0 {
				var internal, external []string
				for _, s := range ap.SubjectsRaw {
					// do not create Issuers for Tailscale domains; they will be given a Manager instead
					if isTailscaleDomain(s) {
						continue
					}
					if !certmagic.SubjectQualifiesForCert(s) {
						return nil, warnings, fmt.Errorf("subject does not qualify for certificate: '%s'", s)
					}
					// we don't use certmagic.SubjectQualifiesForPublicCert() because of one nuance:
					// names like *.*.tld that may not qualify for a public certificate are actually
					// fine when used with OnDemand, since OnDemand (currently) does not obtain
					// wildcards (if it ever does, there will be a separate config option to enable
					// it that we would need to check here) since the hostname is known at handshake;
					// and it is unexpected to switch to internal issuer when the user wants to get
					// regular certificates on-demand for a class of certs like *.*.tld.
					if subjectQualifiesForPublicCert(ap, s) {
						external = append(external, s)
					} else {
						internal = append(internal, s)
					}
				}
				if len(external) > 0 && len(internal) > 0 {
					ap.SubjectsRaw = external
					apCopy := *ap
					ap2 = &apCopy
					ap2.SubjectsRaw = internal
					ap2.IssuersRaw = []json.RawMessage{caddyconfig.JSONModuleObject(caddytls.InternalIssuer{}, "module", "internal", &warnings)}
				}
			}

			if tlsApp.Automation == nil {
				tlsApp.Automation = new(caddytls.AutomationConfig)
			}
			tlsApp.Automation.Policies = append(tlsApp.Automation.Policies, ap)
			if ap2 != nil {
				tlsApp.Automation.Policies = append(tlsApp.Automation.Policies, ap2)
			}

			// certificate loaders
			if clVals, ok := sblock.pile["tls.cert_loader"]; ok {
				for _, clVal := range clVals {
					certLoaders = append(certLoaders, clVal.Value.(caddytls.CertificateLoader))
				}
			}
		}
	}

	// group certificate loaders by module name, then add to config
	if len(certLoaders) > 0 {
		loadersByName := make(map[string]caddytls.CertificateLoader)
		for _, cl := range certLoaders {
			name := caddy.GetModuleName(cl)
			// ugh... technically, we may have multiple FileLoader and FolderLoader
			// modules (because the tls directive returns one per occurrence), but
			// the config structure expects only one instance of each kind of loader
			// module, so we have to combine them... instead of enumerating each
			// possible cert loader module in a type switch, we can use reflection,
			// which works on any cert loaders that are slice types
			if reflect.TypeOf(cl).Kind() == reflect.Slice {
				combined := reflect.ValueOf(loadersByName[name])
				if !combined.IsValid() {
					combined = reflect.New(reflect.TypeOf(cl)).Elem()
				}
				clVal := reflect.ValueOf(cl)
				for i := range clVal.Len() {
					combined = reflect.Append(combined, clVal.Index(i))
				}
				loadersByName[name] = combined.Interface().(caddytls.CertificateLoader)
			}
		}
		for certLoaderName, loaders := range loadersByName {
			tlsApp.CertificatesRaw[certLoaderName] = caddyconfig.JSON(loaders, &warnings)
		}
	}

	// set any of the on-demand options, for if/when on-demand TLS is enabled
	if onDemand, ok := options["on_demand_tls"].(*caddytls.OnDemandConfig); ok {
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.OnDemand = onDemand
	}

	// set up "global" (to the TLS app) DNS provider config
	if globalDNS, ok := options["dns"]; ok && globalDNS != nil {
		tlsApp.DNSRaw = caddyconfig.JSONModuleObject(globalDNS, "name", globalDNS.(caddy.Module).CaddyModule().ID.Name(), nil)
	}

	// set up "global" (to the TLS app) DNS resolvers config
	if globalResolvers, ok := options["tls_resolvers"]; ok && globalResolvers != nil {
		tlsApp.Resolvers = globalResolvers.([]string)
	}

	// set up ECH from Caddyfile options
	if ech, ok := options["ech"].(*caddytls.ECH); ok {
		tlsApp.EncryptedClientHello = ech

		// outer server names will need certificates, so make sure they're included
		// in an automation policy for them that applies any global options
		ap, err := newBaseAutomationPolicy(options, warnings, true)
		if err != nil {
			return nil, warnings, err
		}
		for _, cfg := range ech.Configs {
			if cfg.PublicName != "" {
				ap.SubjectsRaw = append(ap.SubjectsRaw, cfg.PublicName)
			}
		}
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.Policies = append(tlsApp.Automation.Policies, ap)
	}

	// if the storage clean interval is a boolean, then it's "off" to disable cleaning
	if sc, ok := options["storage_check"].(string); ok && sc == "off" {
		tlsApp.DisableStorageCheck = true
	}

	// if the storage clean interval is a boolean, then it's "off" to disable cleaning
	if sci, ok := options["storage_clean_interval"].(bool); ok && !sci {
		tlsApp.DisableStorageClean = true
	}

	// set the storage clean interval if configured
	if storageCleanInterval, ok := options["storage_clean_interval"].(caddy.Duration); ok {
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.StorageCleanInterval = storageCleanInterval
	}

	// set the expired certificates renew interval if configured
	if renewCheckInterval, ok := options["renew_interval"].(caddy.Duration); ok {
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.RenewCheckInterval = renewCheckInterval
	}

	// set the OCSP check interval if configured
	if ocspCheckInterval, ok := options["ocsp_interval"].(caddy.Duration); ok {
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.OCSPCheckInterval = ocspCheckInterval
	}

	// set whether OCSP stapling should be disabled for manually-managed certificates
	if ocspConfig, ok := options["ocsp_stapling"].(certmagic.OCSPConfig); ok {
		tlsApp.DisableOCSPStapling = ocspConfig.DisableStapling
	}

	// if any hostnames appear on the same server block as a key with
	// no host, they will not be used with route matchers because the
	// hostless key matches all hosts, therefore, it wouldn't be
	// considered for auto-HTTPS, so we need to make sure those hosts
	// are manually considered for managed certificates; we also need
	// to make sure that any of these names which are internal-only
	// get internal certificates by default rather than ACME
	var al caddytls.AutomateLoader
	internalAP := &caddytls.AutomationPolicy{
		IssuersRaw: []json.RawMessage{json.RawMessage(`{"module":"internal"}`)},
	}
	if !slices.Contains(autoHTTPS, "off") && !slices.Contains(autoHTTPS, "disable_certs") {
		for h := range httpsHostsSharedWithHostlessKey {
			al = append(al, h)
			if !certmagic.SubjectQualifiesForPublicCert(h) {
				internalAP.SubjectsRaw = append(internalAP.SubjectsRaw, h)
			}
		}
	}
	for name := range forcedAutomatedNames {
		if slices.Contains(al, name) {
			continue
		}
		al = append(al, name)
	}
	// names from the tls_automate_names global option are managed without a
	// site block of their own, so that asking for a certificate does not also
	// mean serving the name; like force_automate, an explicitly listed name is
	// managed even where auto-HTTPS would not have chosen it. Names that cannot
	// get a public certificate are given the internal issuer, the same
	// treatment they would get from a site block.
	if automateNames, ok := options["tls_automate_names"].([]string); ok {
		var publicNames []string
		for _, name := range automateNames {
			if slices.Contains(al, name) {
				continue
			}
			al = append(al, name)
			// a name that a site block already wrote a policy for keeps that
			// policy: it is more specific than anything the global options can
			// say, and a second policy naming the same subject is ambiguous --
			// adapting would fail outright. The name still belongs in the
			// automate loader, since a site block served only over HTTP does
			// not get its certificate managed by auto-HTTPS.
			if automationPolicyExistsForSubject(tlsApp.Automation, name) {
				continue
			}
			if certmagic.SubjectQualifiesForPublicCert(name) {
				publicNames = append(publicNames, name)
			} else {
				internalAP.SubjectsRaw = append(internalAP.SubjectsRaw, name)
			}
		}
		// the names still need an automation policy of their own, or they would
		// miss the issuer configured by global options -- the catch-all policy
		// that would otherwise carry it is dropped once every other policy
		// names its subjects. Consolidation folds this back into an identical
		// policy, so a name listed here ends up in the same place it would have
		// had it been given a site block.
		if len(publicNames) > 0 {
			// only worth a policy if it would carry something: either global
			// automation options, or ACME defaults filled in further below.
			// Without either, the names are managed with the defaults anyway,
			// and an empty policy would just be noise in the output.
			ap, err := newBaseAutomationPolicy(options, warnings, hasGlobalACMEDefaults(options))
			if err != nil {
				return nil, warnings, err
			}
			if ap != nil {
				ap.SubjectsRaw = publicNames
				if tlsApp.Automation == nil {
					tlsApp.Automation = new(caddytls.AutomationConfig)
				}
				tlsApp.Automation.Policies = append(tlsApp.Automation.Policies, ap)
			}
		}
	}
	slices.Sort(al) // to stabilize the adapt output
	if len(al) > 0 {
		tlsApp.CertificatesRaw["automate"] = caddyconfig.JSON(al, &warnings)
	}
	if len(internalAP.SubjectsRaw) > 0 {
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.Policies = append(tlsApp.Automation.Policies, internalAP)
	}

	// if there are any global options set for issuers (ACME ones in particular), make sure they
	// take effect in every automation policy that does not have any issuers
	if tlsApp.Automation != nil {
		globalEmail := options["email"]
		globalACMECA := options["acme_ca"]
		if hasGlobalACMEDefaults(options) {
			for i := range tlsApp.Automation.Policies {
				ap := tlsApp.Automation.Policies[i]
				if len(ap.Issuers) == 0 && automationPolicyHasAllPublicNames(ap) {
					// for public names, create default issuers which will later be filled in with configured global defaults
					// (internal names will implicitly use the internal issuer at auto-https time)
					emailStr, _ := globalEmail.(string)
					ap.Issuers = caddytls.DefaultIssuers(emailStr)

					// if a specific endpoint is configured, can't use multiple default issuers
					if globalACMECA != nil {
						ap.Issuers = []certmagic.Issuer{new(caddytls.ACMEIssuer)}
					}
				}
			}
		}
	}

	// finalize and verify policies; do cleanup
	if tlsApp.Automation != nil {
		for i, ap := range tlsApp.Automation.Policies {
			// ensure all issuers have global defaults filled in
			for j, issuer := range ap.Issuers {
				err := fillInGlobalACMEDefaults(issuer, options)
				if err != nil {
					return nil, warnings, fmt.Errorf("filling in global issuer defaults for AP %d, issuer %d: %v", i, j, err)
				}
			}

			// encode all issuer values we created, so they will be rendered in the output
			if len(ap.Issuers) > 0 && ap.IssuersRaw == nil {
				for _, iss := range ap.Issuers {
					issuerName := iss.(caddy.Module).CaddyModule().ID.Name()
					ap.IssuersRaw = append(ap.IssuersRaw, caddyconfig.JSONModuleObject(iss, "module", issuerName, &warnings))
				}
			}
		}

		// consolidate automation policies that are the exact same
		tlsApp.Automation.Policies = consolidateAutomationPolicies(tlsApp.Automation.Policies)

		// ensure automation policies don't overlap subjects (this should be
		// an error at provision-time as well, but catch it in the adapt phase
		// for convenience)
		automationHostSet := make(map[string]struct{})
		for _, ap := range tlsApp.Automation.Policies {
			for _, s := range ap.SubjectsRaw {
				if _, ok := automationHostSet[s]; ok {
					return nil, warnings, fmt.Errorf("hostname appears in more than one automation policy, making certificate management ambiguous: %s", s)
				}
				automationHostSet[s] = struct{}{}
			}
		}

		// if nothing remains, remove any excess values to clean up the resulting config
		if len(tlsApp.Automation.Policies) == 0 {
			tlsApp.Automation.Policies = nil
		}
		if reflect.DeepEqual(tlsApp.Automation, new(caddytls.AutomationConfig)) {
			tlsApp.Automation = nil
		}
	}

	return tlsApp, warnings, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (st ServerType) buildTLSApp(
	pairings []sbAddrAssociation,
	options map[string]any,
	warnings []caddyconfig.Warning,
) (*caddytls.TLS, []caddyconfig.Warning, error) {
	tlsApp := &caddytls.TLS{CertificatesRaw: make(caddy.ModuleMap)}
	var certLoaders []caddytls.CertificateLoader

	httpPort := strconv.Itoa(caddyhttp.DefaultHTTPPort)
	if hp, ok := options["http_port"].(int); ok {
		httpPort = strconv.Itoa(hp)
	}
	autoHTTPS := []string{}
	if ah, ok := options["auto_https"].([]string); ok {
		autoHTTPS = ah
	}

	// find all hosts that share a server block with a hostless
	// key, so that they don't get forgotten/omitted by auto-HTTPS
	// (since they won't appear in route matchers)
	httpsHostsSharedWithHostlessKey := make(map[string]struct{})
	if !slices.Contains(autoHTTPS, "off") {
		for _, pair := range pairings {
			for _, sb := range pair.serverBlocks {
				for _, addr := range sb.parsedKeys {
					if addr.Host != "" {
						continue
					}

					// this server block has a hostless key, now
					// go through and add all the hosts to the set
					for _, otherAddr := range sb.parsedKeys {
						if otherAddr.Original == addr.Original {
							continue
						}
						if otherAddr.Host != "" && otherAddr.Scheme != "http" && otherAddr.Port != httpPort {
							httpsHostsSharedWithHostlessKey[otherAddr.Host] = struct{}{}
						}
					}
					break
				}
			}
		}
	}

	// a catch-all automation policy is used as a "default" for all subjects that
	// don't have custom configuration explicitly associated with them; this
	// is only to add if the global settings or defaults are non-empty
	catchAllAP, err := newBaseAutomationPolicy(options, warnings, false)
	if err != nil {
		return nil, warnings, err
	}
	if catchAllAP != nil {
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.Policies = append(tlsApp.Automation.Policies, catchAllAP)
	}

	forcedAutomatedNames := make(map[string]struct{}) // explicitly configured to be automated, even if covered by a wildcard

	for _, p := range pairings {
		// avoid setting up TLS automation policies for a server that is HTTP-only
		var addresses []string
		for _, addressWithProtocols := range p.addressesWithProtocols {
			addresses = append(addresses, addressWithProtocols.address)
		}
		if !listenersUseAnyPortOtherThan(addresses, httpPort) {
			continue
		}

		for _, sblock := range p.serverBlocks {
			// check the scheme of all the site addresses,
			// skip building AP if they all had http://
			if sblock.isAllHTTP() {
				continue
			}

			// get values that populate an automation policy for this block
			ap, err := newBaseAutomationPolicy(options, warnings, true)
			if err != nil {
				return nil, warnings, err
			}

			sblockHosts := sblock.hostsFromKeys(false)
			if len(sblockHosts) == 0 && catchAllAP != nil {
				ap = catchAllAP
			}

			// on-demand tls
			if _, ok := sblock.pile["tls.on_demand"]; ok {
				ap.OnDemand = true
			}

			// collect hosts that are forced to have certs automated for their specific name
			if _, ok := sblock.pile["tls.force_automate"]; ok {
				for _, host := range sblockHosts {
					forcedAutomatedNames[host] = struct{}{}
				}
			}

			// reuse private keys tls
			if _, ok := sblock.pile["tls.reuse_private_keys"]; ok {
				ap.ReusePrivateKeys = true
			}

			if keyTypeVals, ok := sblock.pile["tls.key_type"]; ok {
				ap.KeyType = keyTypeVals[0].Value.(string)
			}

			if renewalWindowRatioVals, ok := sblock.pile["tls.renewal_window_ratio"]; ok {
				ap.RenewalWindowRatio = renewalWindowRatioVals[0].Value.(float64)
			} else if globalRenewalWindowRatio, ok := options["renewal_window_ratio"]; ok {
				ap.RenewalWindowRatio = globalRenewalWindowRatio.(float64)
			}

			// certificate issuers
			if issuerVals, ok := sblock.pile["tls.cert_issuer"]; ok {
				var issuers []certmagic.Issuer
				for _, issuerVal := range issuerVals {
					issuers = append(issuers, issuerVal.Value.(certmagic.Issuer))
				}
				if ap == catchAllAP && !reflect.DeepEqual(ap.Issuers, issuers) {
					// this more correctly implements an error check that was removed
					// below; try it with this config:
					//
					// :443 {
					// 	bind 127.0.0.1
					// }
					//
					// :443 {
					// 	bind ::1
					// 	tls {
					// 		issuer acme
					// 	}
					// }
					return nil, warnings, fmt.Errorf("automation policy from site block is also default/catch-all policy because of key without hostname, and the two are in conflict: %#v != %#v", ap.Issuers, issuers)
				}
				ap.Issuers = issuers
			}

			// certificate managers
			if certManagerVals, ok := sblock.pile["tls.cert_manager"]; ok {
				for _, certManager := range certManagerVals {
					certGetterName := certManager.Value.(caddy.Module).CaddyModule().ID.Name()
					ap.ManagersRaw = append(ap.ManagersRaw, caddyconfig.JSONModuleObject(certManager.Value, "via", certGetterName, &warnings))
				}
			}
			// custom bind host
			for _, cfgVal := range sblock.pile["bind"] {
				for _, iss := range ap.Issuers {
					// if an issuer was already configured and it is NOT an ACME issuer,
					// skip, since we intend to adjust only ACME issuers; ensure we
					// include any issuer that embeds/wraps an underlying ACME issuer
					var acmeIssuer *caddytls.ACMEIssuer
					if acmeWrapper, ok := iss.(acmeCapable); ok {
						acmeIssuer = acmeWrapper.GetACMEIssuer()
					}
					if acmeIssuer == nil {
						continue
					}

					// proceed to configure the ACME issuer's bind host, without
					// overwriting any existing settings
					if acmeIssuer.Challenges == nil {
						acmeIssuer.Challenges = new(caddytls.ChallengesConfig)
					}
					if acmeIssuer.Challenges.BindHost == "" {
						// only binding to one host is supported
						var bindHost string
						if asserted, ok := cfgVal.Value.(addressesWithProtocols); ok && len(asserted.addresses) > 0 {
							bindHost = asserted.addresses[0]
						}
						acmeIssuer.Challenges.BindHost = bindHost
					}
				}
			}

			// we used to ensure this block is allowed to create an automation policy;
			// doing so was forbidden if it has a key with no host (i.e. ":443")
			// and if there is a different server block that also has a key with no
			// host -- since a key with no host matches any host, we need its
			// associated automation policy to have an empty Subjects list, i.e. no
			// host filter, which is indistinguishable between the two server blocks
			// because automation is not done in the context of a particular server...
			// this is an example of a poor mapping from Caddyfile to JSON but that's
			// the least-leaky abstraction I could figure out -- however, this check
			// was preventing certain listeners, like those provided by plugins, from
			// being used as desired (see the Tailscale listener plugin), so I removed
			// the check: and I think since I originally wrote the check I added a new
			// check above which *properly* detects this ambiguity without breaking the
			// listener plugin; see the check above with a commented example config
			if len(sblockHosts) == 0 && catchAllAP == nil {
				// this server block has a key with no hosts, but there is not yet
				// a catch-all automation policy (probably because no global options
				// were set), so this one becomes it
				catchAllAP = ap
			}

			hostsNotHTTP := sblock.hostsFromKeysNotHTTP(httpPort)
			sort.Strings(hostsNotHTTP) // solely for deterministic test results

			// associate our new automation policy with this server block's hosts
			ap.SubjectsRaw = hostsNotHTTP

			// if a combination of public and internal names were given
			// for this same server block and no issuer was specified, we
			// need to separate them out in the automation policies so
			// that the internal names can use the internal issuer and
			// the other names can use the default/public/ACME issuer
			var ap2 *caddytls.AutomationPolicy
			if len(ap.Issuers) == 0 {
				var internal, external []string
				for _, s := range ap.SubjectsRaw {
					// do not create Issuers for Tailscale domains; they will be given a Manager instead
					if isTailscaleDomain(s) {
						continue
					}
					if !certmagic.SubjectQualifiesForCert(s) {
						return nil, warnings, fmt.Errorf("subject does not qualify for certificate: '%s'", s)
					}
					// we don't use certmagic.SubjectQualifiesForPublicCert() because of one nuance:
					// names like *.*.tld that may not qualify for a public certificate are actually
					// fine when used with OnDemand, since OnDemand (currently) does not obtain
					// wildcards (if it ever does, there will be a separate config option to enable
					// it that we would need to check here) since the hostname is known at handshake;
					// and it is unexpected to switch to internal issuer when the user wants to get
					// regular certificates on-demand for a class of certs like *.*.tld.
					if subjectQualifiesForPublicCert(ap, s) {
						external = append(external, s)
					} else {
						internal = append(internal, s)
					}
				}
				if len(external) > 0 && len(internal) > 0 {
					ap.SubjectsRaw = external
					apCopy := *ap
					ap2 = &apCopy
					ap2.SubjectsRaw = internal
					ap2.IssuersRaw = []json.RawMessage{caddyconfig.JSONModuleObject(caddytls.InternalIssuer{}, "module", "internal", &warnings)}
				}
			}

			if tlsApp.Automation == nil {
				tlsApp.Automation = new(caddytls.AutomationConfig)
			}
			tlsApp.Automation.Policies = append(tlsApp.Automation.Policies, ap)
			if ap2 != nil {
				tlsApp.Automation.Policies = append(tlsApp.Automation.Policies, ap2)
			}

			// certificate loaders
			if clVals, ok := sblock.pile["tls.cert_loader"]; ok {
				for _, clVal := range clVals {
					certLoaders = append(certLoaders, clVal.Value.(caddytls.CertificateLoader))
				}
			}
		}
	}

	// group certificate loaders by module name, then add to config
	if len(certLoaders) > 0 {
		loadersByName := make(map[string]caddytls.CertificateLoader)
		for _, cl := range certLoaders {
			name := caddy.GetModuleName(cl)
			// ugh... technically, we may have multiple FileLoader and FolderLoader
			// modules (because the tls directive returns one per occurrence), but
			// the config structure expects only one instance of each kind of loader
			// module, so we have to combine them... instead of enumerating each
			// possible cert loader module in a type switch, we can use reflection,
			// which works on any cert loaders that are slice types
			if reflect.TypeOf(cl).Kind() == reflect.Slice {
				combined := reflect.ValueOf(loadersByName[name])
				if !combined.IsValid() {
					combined = reflect.New(reflect.TypeOf(cl)).Elem()
				}
				clVal := reflect.ValueOf(cl)
				for i := range clVal.Len() {
					combined = reflect.Append(combined, clVal.Index(i))
				}
				loadersByName[name] = combined.Interface().(caddytls.CertificateLoader)
			}
		}
		for certLoaderName, loaders := range loadersByName {
			tlsApp.CertificatesRaw[certLoaderName] = caddyconfig.JSON(loaders, &warnings)
		}
	}

	// set any of the on-demand options, for if/when on-demand TLS is enabled
	if onDemand, ok := options["on_demand_tls"].(*caddytls.OnDemandConfig); ok {
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.OnDemand = onDemand
	}

	// set up "global" (to the TLS app) DNS provider config
	if globalDNS, ok := options["dns"]; ok && globalDNS != nil {
		tlsApp.DNSRaw = caddyconfig.JSONModuleObject(globalDNS, "name", globalDNS.(caddy.Module).CaddyModule().ID.Name(), nil)
	}

	// set up "global" (to the TLS app) DNS resolvers config
	if globalResolvers, ok := options["tls_resolvers"]; ok && globalResolvers != nil {
		tlsApp.Resolvers = globalResolvers.([]string)
	}

	// set up ECH from Caddyfile options
	if ech, ok := options["ech"].(*caddytls.ECH); ok {
		tlsApp.EncryptedClientHello = ech

		// outer server names will need certificates, so make sure they're included
		// in an automation policy for them that applies any global options. A name
		// that a site block's policy already covers keeps that policy, because a
		// second policy for it would be rejected as ambiguous or picked ahead of
		// the site's.
		ap, err := newBaseAutomationPolicy(options, warnings, true)
		if err != nil {
			return nil, warnings, err
		}
		for _, cfg := range ech.Configs {
			if cfg.PublicName == "" || automationPolicyCoversName(tlsApp.Automation, cfg.PublicName) {
				continue
			}
			ap.SubjectsRaw = append(ap.SubjectsRaw, cfg.PublicName)
		}
		// without subjects, the policy would apply to every name as a catch-all
		if len(ap.SubjectsRaw) > 0 {
			if tlsApp.Automation == nil {
				tlsApp.Automation = new(caddytls.AutomationConfig)
			}
			tlsApp.Automation.Policies = append(tlsApp.Automation.Policies, ap)
		}
	}

	// if the storage clean interval is a boolean, then it's "off" to disable cleaning
	if sc, ok := options["storage_check"].(string); ok && sc == "off" {
		tlsApp.DisableStorageCheck = true
	}

	// if the storage clean interval is a boolean, then it's "off" to disable cleaning
	if sci, ok := options["storage_clean_interval"].(bool); ok && !sci {
		tlsApp.DisableStorageClean = true
	}

	// set the storage clean interval if configured
	if storageCleanInterval, ok := options["storage_clean_interval"].(caddy.Duration); ok {
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.StorageCleanInterval = storageCleanInterval
	}

	// set the expired certificates renew interval if configured
	if renewCheckInterval, ok := options["renew_interval"].(caddy.Duration); ok {
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.RenewCheckInterval = renewCheckInterval
	}

	// set the OCSP check interval if configured
	if ocspCheckInterval, ok := options["ocsp_interval"].(caddy.Duration); ok {
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.OCSPCheckInterval = ocspCheckInterval
	}

	// set whether OCSP stapling should be disabled for manually-managed certificates
	if ocspConfig, ok := options["ocsp_stapling"].(certmagic.OCSPConfig); ok {
		tlsApp.DisableOCSPStapling = ocspConfig.DisableStapling
	}

	// if any hostnames appear on the same server block as a key with
	// no host, they will not be used with route matchers because the
	// hostless key matches all hosts, therefore, it wouldn't be
	// considered for auto-HTTPS, so we need to make sure those hosts
	// are manually considered for managed certificates; we also need
	// to make sure that any of these names which are internal-only
	// get internal certificates by default rather than ACME
	var al caddytls.AutomateLoader
	internalAP := &caddytls.AutomationPolicy{
		IssuersRaw: []json.RawMessage{json.RawMessage(`{"module":"internal"}`)},
	}
	if !slices.Contains(autoHTTPS, "off") && !slices.Contains(autoHTTPS, "disable_certs") {
		for h := range httpsHostsSharedWithHostlessKey {
			al = append(al, h)
			if !certmagic.SubjectQualifiesForPublicCert(h) {
				internalAP.SubjectsRaw = append(internalAP.SubjectsRaw, h)
			}
		}
	}
	for name := range forcedAutomatedNames {
		if slices.Contains(al, name) {
			continue
		}
		al = append(al, name)
	}
	// names from the tls_automate_names global option are managed without a
	// site block of their own, so that asking for a certificate does not also
	// mean serving the name; like force_automate, an explicitly listed name is
	// managed even where auto-HTTPS would not have chosen it. Names that cannot
	// get a public certificate are given the internal issuer, the same
	// treatment they would get from a site block.
	if automateNames, ok := options["tls_automate_names"].([]string); ok {
		var publicNames []string
		for _, name := range automateNames {
			if slices.Contains(al, name) {
				continue
			}
			al = append(al, name)
			// a name that a site block already wrote a policy for keeps that
			// policy: it is more specific than anything the global options can
			// say, and a second policy naming the same subject is ambiguous --
			// adapting would fail outright. The name still belongs in the
			// automate loader, since a site block served only over HTTP does
			// not get its certificate managed by auto-HTTPS.
			if automationPolicyExistsForSubject(tlsApp.Automation, name) {
				continue
			}
			if certmagic.SubjectQualifiesForPublicCert(name) {
				publicNames = append(publicNames, name)
			} else {
				internalAP.SubjectsRaw = append(internalAP.SubjectsRaw, name)
			}
		}
		// the names still need an automation policy of their own, or they would
		// miss the issuer configured by global options -- the catch-all policy
		// that would otherwise carry it is dropped once every other policy
		// names its subjects. Consolidation folds this back into an identical
		// policy, so a name listed here ends up in the same place it would have
		// had it been given a site block.
		if len(publicNames) > 0 {
			// only worth a policy if it would carry something: either global
			// automation options, or ACME defaults filled in further below.
			// Without either, the names are managed with the defaults anyway,
			// and an empty policy would just be noise in the output.
			ap, err := newBaseAutomationPolicy(options, warnings, hasGlobalACMEDefaults(options))
			if err != nil {
				return nil, warnings, err
			}
			if ap != nil {
				ap.SubjectsRaw = publicNames
				if tlsApp.Automation == nil {
					tlsApp.Automation = new(caddytls.AutomationConfig)
				}
				tlsApp.Automation.Policies = append(tlsApp.Automation.Policies, ap)
			}
		}
	}
	slices.Sort(al) // to stabilize the adapt output
	if len(al) > 0 {
		tlsApp.CertificatesRaw["automate"] = caddyconfig.JSON(al, &warnings)
	}
	if len(internalAP.SubjectsRaw) > 0 {
		if tlsApp.Automation == nil {
			tlsApp.Automation = new(caddytls.AutomationConfig)
		}
		tlsApp.Automation.Policies = append(tlsApp.Automation.Policies, internalAP)
	}

	// if there are any global options set for issuers (ACME ones in particular), make sure they
	// take effect in every automation policy that does not have any issuers
	if tlsApp.Automation != nil {
		globalEmail := options["email"]
		globalACMECA := options["acme_ca"]
		if hasGlobalACMEDefaults(options) {
			for i := range tlsApp.Automation.Policies {
				ap := tlsApp.Automation.Policies[i]
				if len(ap.Issuers) == 0 && automationPolicyHasAllPublicNames(ap) {
					// for public names, create default issuers which will later be filled in with configured global defaults
					// (internal names will implicitly use the internal issuer at auto-https time)
					emailStr, _ := globalEmail.(string)
					ap.Issuers = caddytls.DefaultIssuers(emailStr)

					// if a specific endpoint is configured, can't use multiple default issuers
					if globalACMECA != nil {
						ap.Issuers = []certmagic.Issuer{new(caddytls.ACMEIssuer)}
					}
				}
			}
		}
	}

	// finalize and verify policies; do cleanup
	if tlsApp.Automation != nil {
		for i, ap := range tlsApp.Automation.Policies {
			// ensure all issuers have global defaults filled in
			for j, issuer := range ap.Issuers {
				err := fillInGlobalACMEDefaults(issuer, options)
				if err != nil {
					return nil, warnings, fmt.Errorf("filling in global issuer defaults for AP %d, issuer %d: %v", i, j, err)
				}
			}

			// encode all issuer values we created, so they will be rendered in the output
			if len(ap.Issuers) > 0 && ap.IssuersRaw == nil {
				for _, iss := range ap.Issuers {
					issuerName := iss.(caddy.Module).CaddyModule().ID.Name()
					ap.IssuersRaw = append(ap.IssuersRaw, caddyconfig.JSONModuleObject(iss, "module", issuerName, &warnings))
				}
			}
		}

		// consolidate automation policies that are the exact same
		tlsApp.Automation.Policies = consolidateAutomationPolicies(tlsApp.Automation.Policies)

		// ensure automation policies don't overlap subjects (this should be
		// an error at provision-time as well, but catch it in the adapt phase
		// for convenience)
		automationHostSet := make(map[string]struct{})
		for _, ap := range tlsApp.Automation.Policies {
			for _, s := range ap.SubjectsRaw {
				if _, ok := automationHostSet[s]; ok {
					return nil, warnings, fmt.Errorf("hostname appears in more than one automation policy, making certificate management ambiguous: %s", s)
				}
				automationHostSet[s] = struct{}{}
			}
		}

		// if nothing remains, remove any excess values to clean up the resulting config
		if len(tlsApp.Automation.Policies) == 0 {
			tlsApp.Automation.Policies = nil
		}
		if reflect.DeepEqual(tlsApp.Automation, new(caddytls.AutomationConfig)) {
			tlsApp.Automation = nil
		}
	}

	return tlsApp, warnings, nil
}
```


---

### 🔹 Commit #09: `221ebc45`
- **完整 Hash**: `221ebc4503398fa8c87d95a52d43d0d93a6aeef4`
- **說明 (Ground Truth)**: fix: preserve FastCGI dial errors for retry (#8172)
- **變更檔案數**: 2

#### 📄 檔案: `modules/caddyhttp/reverseproxy/fastcgi/fastcgi.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:70, E:59, A:0) ➔ After(N:71, E:60, A:0)
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
  • + [新增節點] `reverseproxy.NewDialError (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Transport.RoundTrip` ──[CALLS]──> `reverseproxy.NewDialError (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Transport.RoundTrip()`
- **變更前簽章 (Before)**: `func Transport.RoundTrip(r *http.Request)` (L169~L262)
- **變更後簽章 (After)**: `func Transport.RoundTrip(r *http.Request)` (L169~L262)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (t Transport) RoundTrip(r *http.Request) (*http.Response, error) {
	server := r.Context().Value(caddyhttp.ServerCtxKey).(*caddyhttp.Server)

	// Disallow null bytes in the request path, because
	// PHP upstreams may do bad things, like execute a
	// non-PHP file as PHP code. See #4574
	if strings.Contains(r.URL.Path, "\x00") {
		return nil, caddyhttp.Error(http.StatusBadRequest, fmt.Errorf("invalid request path"))
	}

	env, err := t.buildEnv(r)
	if err != nil {
		return nil, fmt.Errorf("building environment: %v", err)
	}

	ctx := r.Context()

	// extract dial information from request (should have been embedded by the reverse proxy)
	network, address := "tcp", r.URL.Host
	if dialInfo, ok := reverseproxy.GetDialInfo(ctx); ok {
		network = dialInfo.Network
		address = dialInfo.Address
	}

	logCreds := server.Logs != nil && server.Logs.ShouldLogCredentials
	loggableReq := caddyhttp.LoggableHTTPRequest{
		Request:              r,
		ShouldLogCredentials: logCreds,
	}
	loggableEnv := loggableEnv{vars: env, logCredentials: logCreds}

	logger := t.logger.With(
		zap.Object("request", loggableReq),
		zap.Object("env", loggableEnv),
	)
	if c := t.logger.Check(zapcore.DebugLevel, "roundtrip"); c != nil {
		c.Write(
			zap.String("dial", address),
			zap.Object("env", loggableEnv),
			zap.Object("request", loggableReq),
		)
	}

	// connect to the backend
	dialer := net.Dialer{Timeout: time.Duration(t.DialTimeout)}
	conn, err := dialer.DialContext(ctx, network, address)
	if err != nil {
		return nil, fmt.Errorf("dialing backend: %v", err)
	}
	defer func() {
		// conn will be closed with the response body unless there's an error
		if err != nil {
			conn.Close()
		}
	}()

	// create the client that will facilitate the protocol
	client := client{
		rwc:    conn,
		reqID:  1,
		logger: logger,
		stderr: t.CaptureStderr,
	}

	// read/write timeouts
	if err = client.SetReadTimeout(time.Duration(t.ReadTimeout)); err != nil {
		return nil, fmt.Errorf("setting read timeout: %v", err)
	}
	if err = client.SetWriteTimeout(time.Duration(t.WriteTimeout)); err != nil {
		return nil, fmt.Errorf("setting write timeout: %v", err)
	}

	contentLength := r.ContentLength
	if contentLength == 0 {
		contentLength, _ = strconv.ParseInt(r.Header.Get("Content-Length"), 10, 64)
	}

	var resp *http.Response
	switch r.Method {
	case http.MethodHead:
		resp, err = client.Head(env)
	case http.MethodGet:
		resp, err = client.Get(env, r.Body, contentLength)
	case http.MethodOptions:
		resp, err = client.Options(env)
	default:
		resp, err = client.Post(env, r.Method, r.Header.Get("Content-Type"), r.Body, contentLength)
	}
	if err != nil {
		return nil, err
	}

	return resp, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (t Transport) RoundTrip(r *http.Request) (*http.Response, error) {
	server := r.Context().Value(caddyhttp.ServerCtxKey).(*caddyhttp.Server)

	// Disallow null bytes in the request path, because
	// PHP upstreams may do bad things, like execute a
	// non-PHP file as PHP code. See #4574
	if strings.Contains(r.URL.Path, "\x00") {
		return nil, caddyhttp.Error(http.StatusBadRequest, fmt.Errorf("invalid request path"))
	}

	env, err := t.buildEnv(r)
	if err != nil {
		return nil, fmt.Errorf("building environment: %v", err)
	}

	ctx := r.Context()

	// extract dial information from request (should have been embedded by the reverse proxy)
	network, address := "tcp", r.URL.Host
	if dialInfo, ok := reverseproxy.GetDialInfo(ctx); ok {
		network = dialInfo.Network
		address = dialInfo.Address
	}

	logCreds := server.Logs != nil && server.Logs.ShouldLogCredentials
	loggableReq := caddyhttp.LoggableHTTPRequest{
		Request:              r,
		ShouldLogCredentials: logCreds,
	}
	loggableEnv := loggableEnv{vars: env, logCredentials: logCreds}

	logger := t.logger.With(
		zap.Object("request", loggableReq),
		zap.Object("env", loggableEnv),
	)
	if c := t.logger.Check(zapcore.DebugLevel, "roundtrip"); c != nil {
		c.Write(
			zap.String("dial", address),
			zap.Object("env", loggableEnv),
			zap.Object("request", loggableReq),
		)
	}

	// connect to the backend
	dialer := net.Dialer{Timeout: time.Duration(t.DialTimeout)}
	conn, err := dialer.DialContext(ctx, network, address)
	if err != nil {
		return nil, reverseproxy.NewDialError(fmt.Errorf("dialing backend: %w", err))
	}
	defer func() {
		// conn will be closed with the response body unless there's an error
		if err != nil {
			conn.Close()
		}
	}()

	// create the client that will facilitate the protocol
	client := client{
		rwc:    conn,
		reqID:  1,
		logger: logger,
		stderr: t.CaptureStderr,
	}

	// read/write timeouts
	if err = client.SetReadTimeout(time.Duration(t.ReadTimeout)); err != nil {
		return nil, fmt.Errorf("setting read timeout: %v", err)
	}
	if err = client.SetWriteTimeout(time.Duration(t.WriteTimeout)); err != nil {
		return nil, fmt.Errorf("setting write timeout: %v", err)
	}

	contentLength := r.ContentLength
	if contentLength == 0 {
		contentLength, _ = strconv.ParseInt(r.Header.Get("Content-Length"), 10, 64)
	}

	var resp *http.Response
	switch r.Method {
	case http.MethodHead:
		resp, err = client.Head(env)
	case http.MethodGet:
		resp, err = client.Get(env, r.Body, contentLength)
	case http.MethodOptions:
		resp, err = client.Options(env)
	default:
		resp, err = client.Post(env, r.Method, r.Header.Get("Content-Type"), r.Body, contentLength)
	}
	if err != nil {
		return nil, err
	}

	return resp, nil
}
```


#### 📄 檔案: `modules/caddyhttp/reverseproxy/reverseproxy.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:244, E:321, A:0) ➔ After(N:245, E:321, A:0)
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
  • + [新增節點] `NewDialError` (FUNCTION_DEF)

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #10: `30d3bd2a`
- **完整 Hash**: `30d3bd2a8959d4d00ca72446f23a59a09f02a83b`
- **說明 (Ground Truth)**: caddyhttp: only bound HTTP/2 body reads in flight with the idle timeout (#8125)
- **變更檔案數**: 3

#### 📄 檔案: `modules/caddyhttp/idletimeout.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:48, E:69, A:0) ➔ After(N:52, E:70, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 17, -Edges: 16, ΔFuncs: 7, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `IdleTimeoutReader.releaseDeadlineLocked` (FUNCTION_DEF)
  • + [新增節點] `IdleTimeoutReader.setReadDeadlineLocked` (FUNCTION_DEF)
  • + [新增節點] `r.Deadline.HardDeadline.IsZero (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `IdleTimeoutWriter.setWriteDeadline` (FUNCTION_DEF)
  • + [新增呼叫邊] `IdleTimeoutReader.Read` ──[CALLS]──> `IdleTimeoutReader.releaseDeadlineLocked`
  • + [新增呼叫邊] `IdleTimeoutReader.setDeadlineLocked` ──[CALLS]──> `IdleTimeoutReader.setReadDeadlineLocked`
  • + [新增呼叫邊] `IdleTimeoutReader.setReadDeadlineLocked` ──[CALLS]──> `r.Ctrl.SetReadDeadline (External/Pkg)`
  • + [新增呼叫邊] `IdleTimeoutReader.setReadDeadlineLocked` ──[CALLS]──> `r.Logger.Check (External/Pkg)`
  • + [新增呼叫邊] `IdleTimeoutReader.setReadDeadlineLocked` ──[CALLS]──> `IdleTimeoutWriter.Write`
  • + [新增呼叫邊] `IdleTimeoutReader.setReadDeadlineLocked` ──[CALLS]──> `zap.Error (External/Pkg)`
  • + [新增呼叫邊] `IdleTimeoutReader.releaseDeadlineLocked` ──[CALLS]──> `r.Deadline.HardDeadline.IsZero (External/Pkg)`
  • + [新增呼叫邊] `IdleTimeoutReader.releaseDeadlineLocked` ──[CALLS]──> `time.Now().Before (External/Pkg)`
  • + [新增呼叫邊] `IdleTimeoutReader.releaseDeadlineLocked` ──[CALLS]──> `time.Now (External/Pkg)`
  • + [新增呼叫邊] `IdleTimeoutReader.releaseDeadlineLocked` ──[CALLS]──> `IdleTimeoutReader.setReadDeadlineLocked`
  • + [新增呼叫邊] `IdleTimeoutReader.clearDeadlineLocked` ──[CALLS]──> `IdleTimeoutReader.setReadDeadlineLocked`
  • _... 以及其餘 22 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `IdleTimeoutReader.clearDeadlineLocked()`
- **變更前簽章 (Before)**: `func IdleTimeoutReader.clearDeadlineLocked()` (L218~L230)
- **變更後簽章 (After)**: `func IdleTimeoutReader.clearDeadlineLocked()` (L277~L285)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (r *IdleTimeoutReader) clearDeadlineLocked() {
	if !r.deadlineSet {
		return
	}
	if err := r.Ctrl.SetReadDeadline(time.Time{}); err != nil {
		r.unsupported = true
		if c := r.Logger.Check(zapcore.DebugLevel, "could not clear read deadline"); c != nil {
			c.Write(zap.Error(err))
		}
		return
	}
	r.deadlineSet = false
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (r *IdleTimeoutReader) clearDeadlineLocked() {
	if r.armed == deadlineNone {
		return
	}
	if !r.setReadDeadlineLocked(time.Time{}, "could not clear read deadline") {
		return
	}
	r.armed = deadlineNone
}
```

### 🔹 函式: `IdleTimeoutWriter.clearDeadline()`
- **變更前簽章 (Before)**: `func IdleTimeoutWriter.clearDeadline()` (L295~L314)
- **變更後簽章 (After)**: `func IdleTimeoutWriter.clearDeadline()` (L361~L376)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (w *IdleTimeoutWriter) clearDeadline() {
	if !w.ClearBetweenWrites || !w.deadlineSet || w.unsupported {
		return
	}

	// once the hard deadline has passed, the deadline set by
	// resetDeadline (capped to it) has already expired; keep it
	if !w.Deadline.HardDeadline.IsZero() && !time.Now().Before(w.Deadline.HardDeadline) {
		return
	}

	if err := w.Ctrl.SetWriteDeadline(w.Deadline.HardDeadline); err != nil {
		w.unsupported = true
		if c := w.Logger.Check(zapcore.DebugLevel, "could not clear write deadline"); c != nil {
			c.Write(zap.Error(err))
		}
		return
	}
	w.deadlineSet = false
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (w *IdleTimeoutWriter) clearDeadline() {
	if !w.ClearBetweenWrites || !w.deadlineSet || w.unsupported {
		return
	}

	// once the hard deadline has passed, the deadline set by
	// resetDeadline (capped to it) has already expired; keep it
	if !w.Deadline.HardDeadline.IsZero() && !time.Now().Before(w.Deadline.HardDeadline) {
		return
	}

	if !w.setWriteDeadline(w.Deadline.HardDeadline, "could not clear write deadline") {
		return
	}
	w.deadlineSet = false
}
```

### 🔹 函式: `IdleTimeoutReader.setDeadlineLocked()`
- **變更前簽章 (Before)**: `func IdleTimeoutReader.setDeadlineLocked(logMessage string)` (L207~L216)
- **變更後簽章 (After)**: `func IdleTimeoutReader.setDeadlineLocked(logMessage string)` (L235~L239)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (r *IdleTimeoutReader) setDeadlineLocked(logMessage string) {
	if err := r.Ctrl.SetReadDeadline(r.Deadline.next()); err != nil {
		r.unsupported = true
		if c := r.Logger.Check(zapcore.DebugLevel, logMessage); c != nil {
			c.Write(zap.Error(err))
		}
		return
	}
	r.deadlineSet = true
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (r *IdleTimeoutReader) setDeadlineLocked(logMessage string) {
	if r.setReadDeadlineLocked(r.Deadline.next(), logMessage) {
		r.armed = deadlineIdle
	}
}
```

### 🔹 函式: `IdleTimeoutReader.HandlerDone()`
- **變更前簽章 (Before)**: `func IdleTimeoutReader.HandlerDone()` (L163~L176)
- **變更後簽章 (After)**: `func IdleTimeoutReader.HandlerDone()` (L191~L204)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (r *IdleTimeoutReader) HandlerDone() {
	r.mu.Lock()
	defer r.mu.Unlock()

	if r.finished {
		return
	}
	if r.terminalErr != nil {
		r.clearDeadlineLocked()
	} else if r.DrainDeadline && !r.deadlineSet && !r.unsupported {
		r.setDeadlineLocked("could not set final read deadline")
	}
	r.finished = true
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (r *IdleTimeoutReader) HandlerDone() {
	r.mu.Lock()
	defer r.mu.Unlock()

	if r.finished {
		return
	}
	if r.terminalErr != nil || r.armed == deadlineHard {
		r.clearDeadlineLocked()
	} else if r.DrainDeadline && r.armed != deadlineIdle && !r.unsupported {
		r.setDeadlineLocked("could not set final read deadline")
	}
	r.finished = true
}
```

### 🔹 函式: `IdleTimeoutReader.rearmLocked()`
- **變更前簽章 (Before)**: `func IdleTimeoutReader.rearmLocked()` (L201~L205)
- **變更後簽章 (After)**: `func IdleTimeoutReader.rearmLocked()` (L229~L233)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (r *IdleTimeoutReader) rearmLocked() {
	if r.deadlineSet && !r.finished && !r.unsupported {
		r.setDeadlineLocked("could not set read deadline")
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (r *IdleTimeoutReader) rearmLocked() {
	if r.armed == deadlineIdle && !r.finished && !r.unsupported {
		r.setDeadlineLocked("could not set read deadline")
	}
}
```

### 🔹 函式: `IdleTimeoutReader.Read()`
- **變更前簽章 (Before)**: `func IdleTimeoutReader.Read(p []byte)` (L132~L157)
- **變更後簽章 (After)**: `func IdleTimeoutReader.Read(p []byte)` (L157~L184)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (r *IdleTimeoutReader) Read(p []byte) (int, error) {
	r.mu.Lock()
	if r.terminalErr != nil {
		err := r.terminalErr
		r.mu.Unlock()
		return 0, err
	}
	if !r.finished && !r.unsupported {
		r.setDeadlineLocked("could not set read deadline")
	}
	r.mu.Unlock()

	n, err := r.ReadCloser.Read(p)

	r.mu.Lock()
	r.Deadline.transferred += int64(n)
	if err != nil {
		r.terminalErr = err
		if !r.finished {
			r.clearDeadlineLocked()
		}
	}
	r.mu.Unlock()

	return n, err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (r *IdleTimeoutReader) Read(p []byte) (int, error) {
	r.mu.Lock()
	if r.terminalErr != nil {
		err := r.terminalErr
		r.mu.Unlock()
		return 0, err
	}
	if !r.finished && !r.unsupported {
		r.setDeadlineLocked("could not set read deadline")
	}
	r.mu.Unlock()

	n, err := r.ReadCloser.Read(p)

	r.mu.Lock()
	r.Deadline.transferred += int64(n)
	if err != nil {
		r.terminalErr = err
		if !r.finished {
			r.clearDeadlineLocked()
		}
	} else if r.ClearBetweenReads && !r.finished {
		r.releaseDeadlineLocked()
	}
	r.mu.Unlock()

	return n, err
}
```

### 🔹 函式: `IdleTimeoutWriter.resetDeadline()`
- **變更前簽章 (Before)**: `func IdleTimeoutWriter.resetDeadline()` (L277~L290)
- **變更後簽章 (After)**: `func IdleTimeoutWriter.resetDeadline()` (L334~L342)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (w *IdleTimeoutWriter) resetDeadline() {
	if w.unsupported {
		return
	}

	if err := w.Ctrl.SetWriteDeadline(w.Deadline.next()); err != nil {
		w.unsupported = true
		if c := w.Logger.Check(zapcore.DebugLevel, "could not set write deadline"); c != nil {
			c.Write(zap.Error(err))
		}
		return
	}
	w.deadlineSet = true
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (w *IdleTimeoutWriter) resetDeadline() {
	if w.unsupported {
		return
	}

	if w.setWriteDeadline(w.Deadline.next(), "could not set write deadline") {
		w.deadlineSet = true
	}
}
```


#### 📄 檔案: `modules/caddyhttp/server.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:156, E:195, A:0) ➔ After(N:156, E:195, A:0)
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

### 🔹 函式: `Server.ServeHTTP()`
- **變更前簽章 (Before)**: `func Server.ServeHTTP(w http.ResponseWriter, r *http.Request)` (L551~L789)
- **變更後簽章 (After)**: `func Server.ServeHTTP(w http.ResponseWriter, r *http.Request)` (L551~L790)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	start := time.Now()

	// If there are listener wrappers that process tls connections but don't return a *tls.Conn, this field will be nil.
	if r.TLS == nil {
		if tlsConnStateFunc, ok := r.Context().Value(tlsConnectionStateFuncCtxKey).(func() *tls.ConnectionState); ok {
			r.TLS = tlsConnStateFunc()
		}
	}

	// enable full-duplex for HTTP/1, ensuring the entire
	// request body gets consumed before writing the response
	if s.EnableFullDuplex && r.ProtoMajor == 1 {
		if err := http.NewResponseController(w).EnableFullDuplex(); err != nil { //nolint:bodyclose
			if c := s.logger.Check(zapcore.WarnLevel, "failed to enable full duplex"); c != nil {
				c.Write(zap.Error(err))
			}
		}
	}

	// guard against slowloris-style attacks by aborting the connection
	// if a read from the request body or a write to the response
	// stalls for longer than the configured timeout; the deadline is
	// reset on every successful read/write, so this doesn't affect
	// legitimately slow clients as long as they keep making progress.
	// hardDeadline, anchored to this handler's start, caps how far
	// that reset can push the deadline out, so an explicitly configured
	// ReadTimeout/WriteTimeout ceiling still applies on top instead of
	// being silently overwritten by the first read/write.
	rc := http.NewResponseController(w)
	var readHardDeadline, writeHardDeadline time.Time
	if s.ReadTimeout > 0 {
		readHardDeadline = start.Add(time.Duration(s.ReadTimeout))
	}
	if s.WriteTimeout > 0 {
		writeHardDeadline = start.Add(time.Duration(s.WriteTimeout))
	}
	var idleReader *IdleTimeoutReader
	var idleWriter *IdleTimeoutWriter
	if s.ReadIdleTimeout > 0 && r.Body != nil {
		idleReader = &IdleTimeoutReader{
			ReadCloser: r.Body,
			Ctrl:       rc,
			Deadline: IdleDeadline{
				Start:        start,
				Timeout:      time.Duration(s.ReadIdleTimeout),
				MinRate:      s.ReadMinRate,
				HardDeadline: readHardDeadline,
			},
			Logger:        s.logger,
			DrainDeadline: r.ProtoMajor == 1 && r.ContentLength != 0,
		}
		defer idleReader.HandlerDone()
		r.Body = idleReader
	}
	if s.WriteIdleTimeout > 0 {
		idleWriter = &IdleTimeoutWriter{
			ResponseWriterWrapper: &ResponseWriterWrapper{ResponseWriter: w},
			Ctrl:                  rc,
			Deadline: IdleDeadline{
				Start:        start,
				Timeout:      time.Duration(s.WriteIdleTimeout),
				MinRate:      s.WriteMinRate,
				HardDeadline: writeHardDeadline,
			},
			MaxChunk:           s.MaxWriteChunk,
			Logger:             s.logger,
			ClearBetweenWrites: r.ProtoMajor == 2,
		}
		defer idleWriter.HandlerDone()
		w = idleWriter
	}

	// set the Server header
	h := w.Header()
	h["Server"] = serverHeader

	// advertise HTTP/3, if enabled
	if s.h3server != nil && r.ProtoMajor < 3 {
		if err := s.h3server.SetQUICHeaders(h); err != nil {
			lvl := zapcore.ErrorLevel
			if errors.Is(err, http3.ErrNoAltSvcPort) {
				lvl = zapcore.DebugLevel
			}
			if c := s.logger.Check(lvl, "setting HTTP/3 Alt-Svc header"); c != nil {
				c.Write(zap.Error(err))
			}
		}
	}

	// prepare internals of the request for the handler pipeline
	repl := caddy.NewReplacer()
	r = prepareRequest(r, repl, w, s, idleTimeouts{reader: idleReader, writer: idleWriter})

	// clone the request for logging purposes before it enters any handler chain;
	// this is necessary to capture the original request in case it gets modified
	// during handling (cloning the request and using .WithLazy is considerably
	// faster than using .With, which will JSON-encode the request immediately)
	shouldLogCredentials := s.Logs != nil && s.Logs.ShouldLogCredentials
	loggableReq := zap.Object("request", LoggableHTTPRequest{
		Request:              r.Clone(r.Context()),
		ShouldLogCredentials: shouldLogCredentials,
	})
	errLog := s.errorLogger.WithLazy(loggableReq)

	var duration time.Duration
	var wrec ResponseRecorder
	var writeErr error

	if s.shouldLogRequest(r) {
		wrec = NewResponseRecorder(w, nil, nil)
		w = wrec

		// wrap the request body in a LengthReader
		// so we can track the number of bytes read from it
		var bodyReader *lengthReader
		if r.Body != nil {
			bodyReader = &lengthReader{Source: r.Body}
			r.Body = bodyReader
			// should always be true, private interface can only be referenced in the same package
			if setReadSizer, ok := wrec.(interface{ setReadSize(*int) }); ok {
				setReadSizer.setReadSize(&bodyReader.Length)
			}
		}

		// capture the original version of the request
		accLog := s.accessLogger.WithLazy(loggableReq)

		defer s.logRequest(accLog, r, wrec, &duration, &writeErr, repl, bodyReader, shouldLogCredentials)

		// if the request went past the write timeout, flush so the access log can
		// see the write error. deferred because flushing before the error routes
		// run would commit a 200 and lose the error status. it sits after the
		// access log defer so it still runs first.
		defer func() {
			if s.WriteTimeout <= 0 ||
				r.ProtoMajor != 1 ||
				duration < time.Duration(s.WriteTimeout) {
				return
			}
			// over wrec, not the rc above: this reaches the recorder's
			// FlushError, which skips buffered responses (#6144); rc sits
			// below the recorder and would flush them anyway.
			flushErr := http.NewResponseController(wrec).Flush()
			if flushErr != nil &&
				!errors.Is(flushErr, http.ErrHijacked) &&
				!errors.Is(flushErr, http.ErrNotSupported) {
				writeErr = flushErr
			}
		}()
	}

	// guarantee ACME HTTP challenges; handle them separately from any user-defined handlers
	if s.tlsApp.HandleHTTPChallenge(w, r) {
		duration = time.Since(start)
		return
	}

	err := s.serveHTTP(w, r)
	duration = time.Since(start)

	if err == nil {
		return
	}

	// restore original request before invoking error handler chain (issue #3717)
	// NOTE: this does not restore original headers if modified (for efficiency)
	origReq, ok := r.Context().Value(OriginalRequestCtxKey).(http.Request)
	if ok {
		r.Method = origReq.Method
		r.RemoteAddr = origReq.RemoteAddr
		r.RequestURI = origReq.RequestURI
		cloneURL(origReq.URL, r.URL)
	}

	// prepare the error log
	errLog = errLog.With(zap.Duration("duration", duration))
	errLoggers := []*zap.Logger{errLog}
	if s.Logs != nil {
		errLoggers = s.Logs.wrapLogger(errLog, r)
	}

	// get the values that will be used to log the error
	errStatus, errMsg, errFields := errLogValues(err)

	// add HTTP error information to request context
	r = s.Errors.WithError(r, err)

	var fields []zapcore.Field
	if s.Errors != nil && len(s.Errors.Routes) > 0 {
		// execute user-defined error handling route
		if err2 := s.errorHandlerChain.ServeHTTP(w, r); err2 == nil {
			// user's error route handled the error response successfully, so now just log the error
			for _, logger := range errLoggers {
				if c := logger.Check(zapcore.DebugLevel, errMsg); c != nil {
					if fields == nil {
						fields = errFields()
					}
					c.Write(fields...)
				}
			}
		} else {
			// well... this is awkward
			for _, logger := range errLoggers {
				if c := logger.Check(zapcore.ErrorLevel, "error handling handler error"); c != nil {
					if fields == nil {
						fields = errFields()
						fields = append([]zapcore.Field{
							zap.String("error", err2.Error()),
							zap.Namespace("first_error"),
							zap.String("msg", errMsg),
						}, fields...)
					}
					c.Write(fields...)
				}
			}
			if handlerErr, ok := err.(HandlerError); ok {
				w.WriteHeader(handlerErr.StatusCode)
			} else {
				w.WriteHeader(http.StatusInternalServerError)
			}
		}
	} else {
		logLevel := zapcore.DebugLevel
		if errStatus >= 500 {
			logLevel = zapcore.ErrorLevel
		}

		for _, logger := range errLoggers {
			if c := logger.Check(logLevel, errMsg); c != nil {
				if fields == nil {
					fields = errFields()
				}
				c.Write(fields...)
			}
		}
		w.WriteHeader(errStatus)
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	start := time.Now()

	// If there are listener wrappers that process tls connections but don't return a *tls.Conn, this field will be nil.
	if r.TLS == nil {
		if tlsConnStateFunc, ok := r.Context().Value(tlsConnectionStateFuncCtxKey).(func() *tls.ConnectionState); ok {
			r.TLS = tlsConnStateFunc()
		}
	}

	// enable full-duplex for HTTP/1, ensuring the entire
	// request body gets consumed before writing the response
	if s.EnableFullDuplex && r.ProtoMajor == 1 {
		if err := http.NewResponseController(w).EnableFullDuplex(); err != nil { //nolint:bodyclose
			if c := s.logger.Check(zapcore.WarnLevel, "failed to enable full duplex"); c != nil {
				c.Write(zap.Error(err))
			}
		}
	}

	// guard against slowloris-style attacks by aborting the connection
	// if a read from the request body or a write to the response
	// stalls for longer than the configured timeout; the deadline is
	// reset on every successful read/write, so this doesn't affect
	// legitimately slow clients as long as they keep making progress.
	// hardDeadline, anchored to this handler's start, caps how far
	// that reset can push the deadline out, so an explicitly configured
	// ReadTimeout/WriteTimeout ceiling still applies on top instead of
	// being silently overwritten by the first read/write.
	rc := http.NewResponseController(w)
	var readHardDeadline, writeHardDeadline time.Time
	if s.ReadTimeout > 0 {
		readHardDeadline = start.Add(time.Duration(s.ReadTimeout))
	}
	if s.WriteTimeout > 0 {
		writeHardDeadline = start.Add(time.Duration(s.WriteTimeout))
	}
	var idleReader *IdleTimeoutReader
	var idleWriter *IdleTimeoutWriter
	if s.ReadIdleTimeout > 0 && r.Body != nil {
		idleReader = &IdleTimeoutReader{
			ReadCloser: r.Body,
			Ctrl:       rc,
			Deadline: IdleDeadline{
				Start:        start,
				Timeout:      time.Duration(s.ReadIdleTimeout),
				MinRate:      s.ReadMinRate,
				HardDeadline: readHardDeadline,
			},
			Logger:            s.logger,
			DrainDeadline:     r.ProtoMajor == 1 && r.ContentLength != 0,
			ClearBetweenReads: r.ProtoMajor == 2,
		}
		defer idleReader.HandlerDone()
		r.Body = idleReader
	}
	if s.WriteIdleTimeout > 0 {
		idleWriter = &IdleTimeoutWriter{
			ResponseWriterWrapper: &ResponseWriterWrapper{ResponseWriter: w},
			Ctrl:                  rc,
			Deadline: IdleDeadline{
				Start:        start,
				Timeout:      time.Duration(s.WriteIdleTimeout),
				MinRate:      s.WriteMinRate,
				HardDeadline: writeHardDeadline,
			},
			MaxChunk:           s.MaxWriteChunk,
			Logger:             s.logger,
			ClearBetweenWrites: r.ProtoMajor == 2,
		}
		defer idleWriter.HandlerDone()
		w = idleWriter
	}

	// set the Server header
	h := w.Header()
	h["Server"] = serverHeader

	// advertise HTTP/3, if enabled
	if s.h3server != nil && r.ProtoMajor < 3 {
		if err := s.h3server.SetQUICHeaders(h); err != nil {
			lvl := zapcore.ErrorLevel
			if errors.Is(err, http3.ErrNoAltSvcPort) {
				lvl = zapcore.DebugLevel
			}
			if c := s.logger.Check(lvl, "setting HTTP/3 Alt-Svc header"); c != nil {
				c.Write(zap.Error(err))
			}
		}
	}

	// prepare internals of the request for the handler pipeline
	repl := caddy.NewReplacer()
	r = prepareRequest(r, repl, w, s, idleTimeouts{reader: idleReader, writer: idleWriter})

	// clone the request for logging purposes before it enters any handler chain;
	// this is necessary to capture the original request in case it gets modified
	// during handling (cloning the request and using .WithLazy is considerably
	// faster than using .With, which will JSON-encode the request immediately)
	shouldLogCredentials := s.Logs != nil && s.Logs.ShouldLogCredentials
	loggableReq := zap.Object("request", LoggableHTTPRequest{
		Request:              r.Clone(r.Context()),
		ShouldLogCredentials: shouldLogCredentials,
	})
	errLog := s.errorLogger.WithLazy(loggableReq)

	var duration time.Duration
	var wrec ResponseRecorder
	var writeErr error

	if s.shouldLogRequest(r) {
		wrec = NewResponseRecorder(w, nil, nil)
		w = wrec

		// wrap the request body in a LengthReader
		// so we can track the number of bytes read from it
		var bodyReader *lengthReader
		if r.Body != nil {
			bodyReader = &lengthReader{Source: r.Body}
			r.Body = bodyReader
			// should always be true, private interface can only be referenced in the same package
			if setReadSizer, ok := wrec.(interface{ setReadSize(*int) }); ok {
				setReadSizer.setReadSize(&bodyReader.Length)
			}
		}

		// capture the original version of the request
		accLog := s.accessLogger.WithLazy(loggableReq)

		defer s.logRequest(accLog, r, wrec, &duration, &writeErr, repl, bodyReader, shouldLogCredentials)

		// if the request went past the write timeout, flush so the access log can
		// see the write error. deferred because flushing before the error routes
		// run would commit a 200 and lose the error status. it sits after the
		// access log defer so it still runs first.
		defer func() {
			if s.WriteTimeout <= 0 ||
				r.ProtoMajor != 1 ||
				duration < time.Duration(s.WriteTimeout) {
				return
			}
			// over wrec, not the rc above: this reaches the recorder's
			// FlushError, which skips buffered responses (#6144); rc sits
			// below the recorder and would flush them anyway.
			flushErr := http.NewResponseController(wrec).Flush()
			if flushErr != nil &&
				!errors.Is(flushErr, http.ErrHijacked) &&
				!errors.Is(flushErr, http.ErrNotSupported) {
				writeErr = flushErr
			}
		}()
	}

	// guarantee ACME HTTP challenges; handle them separately from any user-defined handlers
	if s.tlsApp.HandleHTTPChallenge(w, r) {
		duration = time.Since(start)
		return
	}

	err := s.serveHTTP(w, r)
	duration = time.Since(start)

	if err == nil {
		return
	}

	// restore original request before invoking error handler chain (issue #3717)
	// NOTE: this does not restore original headers if modified (for efficiency)
	origReq, ok := r.Context().Value(OriginalRequestCtxKey).(http.Request)
	if ok {
		r.Method = origReq.Method
		r.RemoteAddr = origReq.RemoteAddr
		r.RequestURI = origReq.RequestURI
		cloneURL(origReq.URL, r.URL)
	}

	// prepare the error log
	errLog = errLog.With(zap.Duration("duration", duration))
	errLoggers := []*zap.Logger{errLog}
	if s.Logs != nil {
		errLoggers = s.Logs.wrapLogger(errLog, r)
	}

	// get the values that will be used to log the error
	errStatus, errMsg, errFields := errLogValues(err)

	// add HTTP error information to request context
	r = s.Errors.WithError(r, err)

	var fields []zapcore.Field
	if s.Errors != nil && len(s.Errors.Routes) > 0 {
		// execute user-defined error handling route
		if err2 := s.errorHandlerChain.ServeHTTP(w, r); err2 == nil {
			// user's error route handled the error response successfully, so now just log the error
			for _, logger := range errLoggers {
				if c := logger.Check(zapcore.DebugLevel, errMsg); c != nil {
					if fields == nil {
						fields = errFields()
					}
					c.Write(fields...)
				}
			}
		} else {
			// well... this is awkward
			for _, logger := range errLoggers {
				if c := logger.Check(zapcore.ErrorLevel, "error handling handler error"); c != nil {
					if fields == nil {
						fields = errFields()
						fields = append([]zapcore.Field{
							zap.String("error", err2.Error()),
							zap.Namespace("first_error"),
							zap.String("msg", errMsg),
						}, fields...)
					}
					c.Write(fields...)
				}
			}
			if handlerErr, ok := err.(HandlerError); ok {
				w.WriteHeader(handlerErr.StatusCode)
			} else {
				w.WriteHeader(http.StatusInternalServerError)
			}
		}
	} else {
		logLevel := zapcore.DebugLevel
		if errStatus >= 500 {
			logLevel = zapcore.ErrorLevel
		}

		for _, logger := range errLoggers {
			if c := logger.Check(logLevel, errMsg); c != nil {
				if fields == nil {
					fields = errFields()
				}
				c.Write(fields...)
			}
		}
		w.WriteHeader(errStatus)
	}
}
```


#### 📄 檔案: `modules/caddyhttp/timeouts/timeouts.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:21, E:16, A:0) ➔ After(N:21, E:16, A:0)
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

### 🔹 函式: `Timeouts.ServeHTTP()`
- **變更前簽章 (Before)**: `func Timeouts.ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler)` (L89~L157)
- **變更後簽章 (After)**: `func Timeouts.ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler)` (L89~L158)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (t Timeouts) ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler) error {
	if t.ReadTimeout <= 0 && t.WriteTimeout <= 0 {
		return next.ServeHTTP(w, r)
	}

	// if the request already has idle timeouts, from the server or an
	// enclosing route, override them instead of wrapping again: the
	// wrapper closest to the connection sets the deadline last, so it
	// would take precedence over ours
	idleReader, idleWriter := caddyhttp.IdleTimeoutsFromContext(r.Context())
	var wrapped bool
	var rc *http.ResponseController
	start := time.Now()

	if t.ReadTimeout > 0 && r.Body != nil {
		if idleReader != nil {
			defer idleReader.Override(t.ReadTimeout, t.ReadMinRate)()
		} else {
			//nolint:bodyclose
			rc = http.NewResponseController(w)
			idleReader = &caddyhttp.IdleTimeoutReader{
				ReadCloser: r.Body,
				Ctrl:       rc,
				Deadline: caddyhttp.IdleDeadline{
					Start:   start,
					Timeout: t.ReadTimeout,
					MinRate: t.ReadMinRate,
				},
				Logger:        t.logger,
				DrainDeadline: r.ProtoMajor == 1 && r.ContentLength != 0,
			}
			defer idleReader.HandlerDone()
			r.Body = idleReader
			wrapped = true
		}
	}
	if t.WriteTimeout > 0 {
		if idleWriter != nil {
			defer idleWriter.Override(t.WriteTimeout, t.WriteMinRate, t.MaxWriteChunk)()
		} else {
			if rc == nil {
				//nolint:bodyclose
				rc = http.NewResponseController(w)
			}
			idleWriter = &caddyhttp.IdleTimeoutWriter{
				ResponseWriterWrapper: &caddyhttp.ResponseWriterWrapper{ResponseWriter: w},
				Ctrl:                  rc,
				Deadline: caddyhttp.IdleDeadline{
					Start:   start,
					Timeout: t.WriteTimeout,
					MinRate: t.WriteMinRate,
				},
				MaxChunk:           t.MaxWriteChunk,
				Logger:             t.logger,
				ClearBetweenWrites: r.ProtoMajor == 2,
			}
			defer idleWriter.HandlerDone()
			w = idleWriter
			wrapped = true
		}
	}

	// let nested timeouts handlers override the wrappers added here
	if wrapped {
		r = r.WithContext(caddyhttp.ContextWithIdleTimeouts(r.Context(), idleReader, idleWriter))
	}

	return next.ServeHTTP(w, r)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (t Timeouts) ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler) error {
	if t.ReadTimeout <= 0 && t.WriteTimeout <= 0 {
		return next.ServeHTTP(w, r)
	}

	// if the request already has idle timeouts, from the server or an
	// enclosing route, override them instead of wrapping again: the
	// wrapper closest to the connection sets the deadline last, so it
	// would take precedence over ours
	idleReader, idleWriter := caddyhttp.IdleTimeoutsFromContext(r.Context())
	var wrapped bool
	var rc *http.ResponseController
	start := time.Now()

	if t.ReadTimeout > 0 && r.Body != nil {
		if idleReader != nil {
			defer idleReader.Override(t.ReadTimeout, t.ReadMinRate)()
		} else {
			//nolint:bodyclose
			rc = http.NewResponseController(w)
			idleReader = &caddyhttp.IdleTimeoutReader{
				ReadCloser: r.Body,
				Ctrl:       rc,
				Deadline: caddyhttp.IdleDeadline{
					Start:   start,
					Timeout: t.ReadTimeout,
					MinRate: t.ReadMinRate,
				},
				Logger:            t.logger,
				DrainDeadline:     r.ProtoMajor == 1 && r.ContentLength != 0,
				ClearBetweenReads: r.ProtoMajor == 2,
			}
			defer idleReader.HandlerDone()
			r.Body = idleReader
			wrapped = true
		}
	}
	if t.WriteTimeout > 0 {
		if idleWriter != nil {
			defer idleWriter.Override(t.WriteTimeout, t.WriteMinRate, t.MaxWriteChunk)()
		} else {
			if rc == nil {
				//nolint:bodyclose
				rc = http.NewResponseController(w)
			}
			idleWriter = &caddyhttp.IdleTimeoutWriter{
				ResponseWriterWrapper: &caddyhttp.ResponseWriterWrapper{ResponseWriter: w},
				Ctrl:                  rc,
				Deadline: caddyhttp.IdleDeadline{
					Start:   start,
					Timeout: t.WriteTimeout,
					MinRate: t.WriteMinRate,
				},
				MaxChunk:           t.MaxWriteChunk,
				Logger:             t.logger,
				ClearBetweenWrites: r.ProtoMajor == 2,
			}
			defer idleWriter.HandlerDone()
			w = idleWriter
			wrapped = true
		}
	}

	// let nested timeouts handlers override the wrappers added here
	if wrapped {
		r = r.WithContext(caddyhttp.ContextWithIdleTimeouts(r.Context(), idleReader, idleWriter))
	}

	return next.ServeHTTP(w, r)
}
```


---

### 🔹 Commit #11: `8507b63c`
- **完整 Hash**: `8507b63cf03a7a0d90b2084f3aafbcc1d8e60a7b`
- **說明 (Ground Truth)**: caddytls: add not matcher for TLS handshakes (#8138)
- **變更檔案數**: 1

#### 📄 檔案: `modules/caddytls/matchers.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:80, E:116, A:0) ➔ After(N:91, E:129, A:0)
- **差分統計**: +Nodes: 11, -Nodes: 0, +Edges: 13, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `MatchNot.UnmarshalCaddyfile` (FUNCTION_DEF)
  • + [新增節點] `ctx.LoadModule (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `MatchNot.Match` (FUNCTION_DEF)
  • + [新增節點] `ParseCaddyfileNestedMatcherSet (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `MatchNot.Provision` (FUNCTION_DEF)
  • + [新增節點] `json.Marshal (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `MatchNot.MarshalJSON` (FUNCTION_DEF)
  • + [新增節點] `MatchNot.CaddyModule` (FUNCTION_DEF)
  • + [新增節點] `json.Unmarshal (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `ms` (MODULE_STATE)
  • + [新增節點] `MatchNot.UnmarshalJSON` (FUNCTION_DEF)
  • + [新增呼叫邊] `MatchNot.CaddyModule` ──[CALLS]──> `new (External/Pkg)`
  • + [新增呼叫邊] `MatchNot.UnmarshalJSON` ──[CALLS]──> `json.Unmarshal (External/Pkg)`
  • + [新增呼叫邊] `MatchNot.MarshalJSON` ──[CALLS]──> `json.Marshal (External/Pkg)`
  • + [新增呼叫邊] `MatchNot.Provision` ──[CALLS]──> `ctx.LoadModule (External/Pkg)`
  • _... 以及其餘 9 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `init()`
- **變更前簽章 (Before)**: `func init()` (L38~L43)
- **變更後簽章 (After)**: `func init()` (L39~L45)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func init() {
	caddy.RegisterModule(MatchServerName{})
	caddy.RegisterModule(MatchServerNameRE{})
	caddy.RegisterModule(MatchRemoteIP{})
	caddy.RegisterModule(MatchLocalIP{})
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func init() {
	caddy.RegisterModule(MatchServerName{})
	caddy.RegisterModule(MatchServerNameRE{})
	caddy.RegisterModule(MatchRemoteIP{})
	caddy.RegisterModule(MatchLocalIP{})
	caddy.RegisterModule(MatchNot{})
}
```


---

### 🔹 Commit #12: `f7eeb1d6`
- **完整 Hash**: `f7eeb1d65c80b2f634b3ce406fa71ba1f0e078a2`
- **說明 (Ground Truth)**: reverseproxy: log HTTP/3 client cancellations at debug level (#8135)
- **變更檔案數**: 2

#### 📄 檔案: `modules/caddyhttp/reverseproxy/reverseproxy.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:243, E:319, A:0) ➔ After(N:244, E:321, A:0)
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
  • + [新增節點] `isClientCanceledH3` (FUNCTION_DEF)
  • + [新增呼叫邊] `Handler.finalizeResponse` ──[CALLS]──> `isClientCanceledH3`
  • + [新增呼叫邊] `isClientCanceledH3` ──[CALLS]──> `errors.Is (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Handler.finalizeResponse()`
- **變更前簽章 (Before)**: `func Handler.finalizeResponse(
	rw http.ResponseWriter,
	req *http.Request,
	res *http.Response,
	repl *caddy.Replacer,
	start time.Time,
	logger *zap.Logger,
	upstreamAddr string,
)` (L1370~L1495)
- **變更後簽章 (After)**: `func Handler.finalizeResponse(
	rw http.ResponseWriter,
	req *http.Request,
	res *http.Response,
	repl *caddy.Replacer,
	start time.Time,
	logger *zap.Logger,
	upstreamAddr string,
)` (L1371~L1502)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (h *Handler) finalizeResponse(
	rw http.ResponseWriter,
	req *http.Request,
	res *http.Response,
	repl *caddy.Replacer,
	start time.Time,
	logger *zap.Logger,
	upstreamAddr string,
) error {
	responseWasIncremental := caddyhttp.IsIncremental(res.Header)

	// Strip hop-by-hop headers from the upstream response.
	// For 101 Switching Protocols, save the Upgrade value
	// first (handleUpgradeResponse needs it for validation)
	// and restore it with a canonical Connection header.
	upgradeVal := res.Header.Get("Upgrade")

	removeConnectionHeaders(res.Header)
	for _, h := range hopHeaders {
		res.Header.Del(h)
	}

	if res.StatusCode == http.StatusSwitchingProtocols && upgradeVal != "" {
		res.Header.Set("Upgrade", upgradeVal)
		res.Header.Set("Connection", "Upgrade")
	}

	// deal with 101 Switching Protocols responses: (WebSocket, h2c, etc)
	if res.StatusCode == http.StatusSwitchingProtocols {
		h.handleUpgradeResponse(logger, rw, req, res, upstreamAddr)
		return nil
	}

	// delete our Server header and use Via instead (see #6275)
	rw.Header().Del("Server")
	var protoPrefix string
	if !strings.HasPrefix(strings.ToUpper(res.Proto), "HTTP/") {
		protoPrefix = res.Proto[:strings.Index(res.Proto, "/")+1]
	}
	rw.Header().Add("Via", protoPrefix+strconv.Itoa(res.ProtoMajor)+"."+strconv.Itoa(res.ProtoMinor)+" Caddy")

	// apply any response header operations
	if h.Headers != nil && h.Headers.Response != nil {
		if h.Headers.Response.Require == nil ||
			h.Headers.Response.Require.Match(res.StatusCode, res.Header) {
			h.Headers.Response.ApplyTo(res.Header, repl)
		}
	}
	if responseHasContent(req, res) && h.ResponseBuffers != 0 &&
		(responseWasIncremental || caddyhttp.IsIncremental(res.Header)) {
		res.Body.Close()
		return roundtripSucceededError{h.refuseIncremental(rw, res.Header)}
	}

	copyHeader(rw.Header(), res.Header)

	// The "Trailer" header isn't included in the Transport's response,
	// at least for *http.Transport. Build it up from Trailer.
	announcedTrailers := len(res.Trailer)
	if announcedTrailers > 0 {
		trailerKeys := make([]string, 0, len(res.Trailer))
		for k := range res.Trailer {
			trailerKeys = append(trailerKeys, k)
		}
		rw.Header().Add("Trailer", strings.Join(trailerKeys, ", "))
	}

	rw.WriteHeader(res.StatusCode)
	if h.VerboseLogs {
		logger.Debug("wrote header")
	}

	err := h.copyResponse(rw, res.Body, h.flushInterval(req, res, responseWasIncremental), logger)
	errClose := res.Body.Close() // close now, instead of defer, to populate res.Trailer
	if h.VerboseLogs || errClose != nil {
		if c := logger.Check(zapcore.DebugLevel, "closed response body from upstream"); c != nil {
			c.Write(zap.Error(errClose))
		}
	}
	if err != nil {
		// we're streaming the response and we've already written headers, so
		// there's nothing an error handler can do to recover at this point;
		// we'll just log the error and abort the stream here and panic just as
		// the standard lib's proxy to propagate the stream error.
		// see issue https://github.com/caddyserver/caddy/issues/5951
		if c := logger.Check(zapcore.WarnLevel, "aborting with incomplete response"); c != nil {
			c.Write(zap.Error(err))
		}
		// flush the buffer to ensure the client sees the partial response
		// see: https://github.com/caddyserver/caddy/issues/7845
		//nolint:bodyclose
		http.NewResponseController(rw).Flush()
		// no extra logging from stdlib
		panic(http.ErrAbortHandler)
	}

	if len(res.Trailer) > 0 {
		// Force chunking if we saw a response trailer.
		// This prevents net/http from calculating the length for short
		// bodies and adding a Content-Length.
		//nolint:bodyclose
		http.NewResponseController(rw).Flush()
	}

	// total duration spent proxying, including writing response body
	repl.Set("http.reverse_proxy.upstream.duration", time.Since(start))
	repl.Set("http.reverse_proxy.upstream.duration_ms", time.Since(start).Seconds()*1e3)

	if len(res.Trailer) == announcedTrailers {
		copyHeader(rw.Header(), res.Trailer)
		return nil
	}

	for k, vv := range res.Trailer {
		k = http.TrailerPrefix + k
		for _, v := range vv {
			rw.Header().Add(k, v)
		}
	}

	if h.VerboseLogs {
		logger.Debug("response finalized")
	}

	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (h *Handler) finalizeResponse(
	rw http.ResponseWriter,
	req *http.Request,
	res *http.Response,
	repl *caddy.Replacer,
	start time.Time,
	logger *zap.Logger,
	upstreamAddr string,
) error {
	responseWasIncremental := caddyhttp.IsIncremental(res.Header)

	// Strip hop-by-hop headers from the upstream response.
	// For 101 Switching Protocols, save the Upgrade value
	// first (handleUpgradeResponse needs it for validation)
	// and restore it with a canonical Connection header.
	upgradeVal := res.Header.Get("Upgrade")

	removeConnectionHeaders(res.Header)
	for _, h := range hopHeaders {
		res.Header.Del(h)
	}

	if res.StatusCode == http.StatusSwitchingProtocols && upgradeVal != "" {
		res.Header.Set("Upgrade", upgradeVal)
		res.Header.Set("Connection", "Upgrade")
	}

	// deal with 101 Switching Protocols responses: (WebSocket, h2c, etc)
	if res.StatusCode == http.StatusSwitchingProtocols {
		h.handleUpgradeResponse(logger, rw, req, res, upstreamAddr)
		return nil
	}

	// delete our Server header and use Via instead (see #6275)
	rw.Header().Del("Server")
	var protoPrefix string
	if !strings.HasPrefix(strings.ToUpper(res.Proto), "HTTP/") {
		protoPrefix = res.Proto[:strings.Index(res.Proto, "/")+1]
	}
	rw.Header().Add("Via", protoPrefix+strconv.Itoa(res.ProtoMajor)+"."+strconv.Itoa(res.ProtoMinor)+" Caddy")

	// apply any response header operations
	if h.Headers != nil && h.Headers.Response != nil {
		if h.Headers.Response.Require == nil ||
			h.Headers.Response.Require.Match(res.StatusCode, res.Header) {
			h.Headers.Response.ApplyTo(res.Header, repl)
		}
	}
	if responseHasContent(req, res) && h.ResponseBuffers != 0 &&
		(responseWasIncremental || caddyhttp.IsIncremental(res.Header)) {
		res.Body.Close()
		return roundtripSucceededError{h.refuseIncremental(rw, res.Header)}
	}

	copyHeader(rw.Header(), res.Header)

	// The "Trailer" header isn't included in the Transport's response,
	// at least for *http.Transport. Build it up from Trailer.
	announcedTrailers := len(res.Trailer)
	if announcedTrailers > 0 {
		trailerKeys := make([]string, 0, len(res.Trailer))
		for k := range res.Trailer {
			trailerKeys = append(trailerKeys, k)
		}
		rw.Header().Add("Trailer", strings.Join(trailerKeys, ", "))
	}

	rw.WriteHeader(res.StatusCode)
	if h.VerboseLogs {
		logger.Debug("wrote header")
	}

	err := h.copyResponse(rw, res.Body, h.flushInterval(req, res, responseWasIncremental), logger)
	errClose := res.Body.Close() // close now, instead of defer, to populate res.Trailer
	if h.VerboseLogs || errClose != nil {
		if c := logger.Check(zapcore.DebugLevel, "closed response body from upstream"); c != nil {
			c.Write(zap.Error(errClose))
		}
	}
	if err != nil {
		// we're streaming the response and we've already written headers, so
		// there's nothing an error handler can do to recover at this point;
		// we'll just log the error and abort the stream here and panic just as
		// the standard lib's proxy to propagate the stream error.
		// see issue https://github.com/caddyserver/caddy/issues/5951
		lvl := zapcore.WarnLevel
		if isClientCanceledH3(err) {
			// the client canceled the request; expected and not actionable
			// see issue https://github.com/caddyserver/caddy/issues/5766
			lvl = zapcore.DebugLevel
		}
		if c := logger.Check(lvl, "aborting with incomplete response"); c != nil {
			c.Write(zap.Error(err))
		}
		// flush the buffer to ensure the client sees the partial response
		// see: https://github.com/caddyserver/caddy/issues/7845
		//nolint:bodyclose
		http.NewResponseController(rw).Flush()
		// no extra logging from stdlib
		panic(http.ErrAbortHandler)
	}

	if len(res.Trailer) > 0 {
		// Force chunking if we saw a response trailer.
		// This prevents net/http from calculating the length for short
		// bodies and adding a Content-Length.
		//nolint:bodyclose
		http.NewResponseController(rw).Flush()
	}

	// total duration spent proxying, including writing response body
	repl.Set("http.reverse_proxy.upstream.duration", time.Since(start))
	repl.Set("http.reverse_proxy.upstream.duration_ms", time.Since(start).Seconds()*1e3)

	if len(res.Trailer) == announcedTrailers {
		copyHeader(rw.Header(), res.Trailer)
		return nil
	}

	for k, vv := range res.Trailer {
		k = http.TrailerPrefix + k
		for _, v := range vv {
			rw.Header().Add(k, v)
		}
	}

	if h.VerboseLogs {
		logger.Debug("response finalized")
	}

	return nil
}
```


#### 📄 檔案: `modules/caddyhttp/reverseproxy/streaming.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:139, E:170, A:0) ➔ After(N:140, E:170, A:0)
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
  • + [新增節點] `errWritingDownstream` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Handler.copyBuffer()`
- **變更前簽章 (Before)**: `func Handler.copyBuffer(dst io.Writer, src io.Reader, buf []byte, logger *zap.Logger)` (L469~L520)
- **變更後簽章 (After)**: `func Handler.copyBuffer(dst io.Writer, src io.Reader, buf []byte, logger *zap.Logger)` (L473~L524)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (h Handler) copyBuffer(dst io.Writer, src io.Reader, buf []byte, logger *zap.Logger) (int64, error) {
	if len(buf) == 0 {
		buf = make([]byte, defaultBufferSize)
	}
	var written int64
	for {
		logger.Debug("waiting to read from upstream")
		nr, rerr := src.Read(buf)
		logger := logger.With(zap.Int("read", nr))
		if c := logger.Check(zapcore.DebugLevel, "read from upstream"); c != nil {
			c.Write(zap.Error(rerr))
		}
		if rerr != nil && rerr != io.EOF && rerr != context.Canceled {
			// TODO: this could be useful to know (indeed, it revealed an error in our
			// fastcgi PoC earlier; but it's this single error report here that necessitates
			// a function separate from io.CopyBuffer, since io.CopyBuffer does not distinguish
			// between read or write errors; in a reverse proxy situation, write errors are not
			// something we need to report to the client, but read errors are a problem on our
			// end for sure. so we need to decide what we want.)
			// p.logf("copyBuffer: ReverseProxy read error during body copy: %v", rerr)
			if c := logger.Check(zapcore.ErrorLevel, "reading from backend"); c != nil {
				c.Write(zap.Error(rerr))
			}
		}
		if nr > 0 {
			logger.Debug("writing to downstream")
			nw, werr := dst.Write(buf[:nr])
			if nw > 0 {
				written += int64(nw)
			}
			if c := logger.Check(zapcore.DebugLevel, "wrote to downstream"); c != nil {
				c.Write(
					zap.Int("written", nw),
					zap.Int64("written_total", written),
					zap.Error(werr),
				)
			}
			if werr != nil {
				return written, fmt.Errorf("writing: %w", werr)
			}
			if nr != nw {
				return written, io.ErrShortWrite
			}
		}
		if rerr != nil {
			if rerr == io.EOF {
				return written, nil
			}
			return written, fmt.Errorf("reading: %w", rerr)
		}
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (h Handler) copyBuffer(dst io.Writer, src io.Reader, buf []byte, logger *zap.Logger) (int64, error) {
	if len(buf) == 0 {
		buf = make([]byte, defaultBufferSize)
	}
	var written int64
	for {
		logger.Debug("waiting to read from upstream")
		nr, rerr := src.Read(buf)
		logger := logger.With(zap.Int("read", nr))
		if c := logger.Check(zapcore.DebugLevel, "read from upstream"); c != nil {
			c.Write(zap.Error(rerr))
		}
		if rerr != nil && rerr != io.EOF && rerr != context.Canceled {
			// TODO: this could be useful to know (indeed, it revealed an error in our
			// fastcgi PoC earlier; but it's this single error report here that necessitates
			// a function separate from io.CopyBuffer, since io.CopyBuffer does not distinguish
			// between read or write errors; in a reverse proxy situation, write errors are not
			// something we need to report to the client, but read errors are a problem on our
			// end for sure. so we need to decide what we want.)
			// p.logf("copyBuffer: ReverseProxy read error during body copy: %v", rerr)
			if c := logger.Check(zapcore.ErrorLevel, "reading from backend"); c != nil {
				c.Write(zap.Error(rerr))
			}
		}
		if nr > 0 {
			logger.Debug("writing to downstream")
			nw, werr := dst.Write(buf[:nr])
			if nw > 0 {
				written += int64(nw)
			}
			if c := logger.Check(zapcore.DebugLevel, "wrote to downstream"); c != nil {
				c.Write(
					zap.Int("written", nw),
					zap.Int64("written_total", written),
					zap.Error(werr),
				)
			}
			if werr != nil {
				return written, fmt.Errorf("%w: %w", errWritingDownstream, werr)
			}
			if nr != nw {
				return written, io.ErrShortWrite
			}
		}
		if rerr != nil {
			if rerr == io.EOF {
				return written, nil
			}
			return written, fmt.Errorf("reading: %w", rerr)
		}
	}
}
```


---

### 🔹 Commit #13: `04fe1610`
- **完整 Hash**: `04fe16102872eba7c017b495a9006fddae4dbdc4`
- **說明 (Ground Truth)**: encode: fix ETag list matching (#8128)
- **變更檔案數**: 1

#### 📄 檔案: `modules/caddyhttp/encode/encode.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:79, E:103, A:0) ➔ After(N:81, E:104, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 1, +Edges: 4, -Edges: 3, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `strings.Join (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `strings.ReplaceAll (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `r.Header.Values (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `strings.CutSuffix (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Encode.ServeHTTP` ──[CALLS]──> `r.Header.Values (External/Pkg)`
  • + [新增呼叫邊] `Encode.ServeHTTP` ──[CALLS]──> `len (External/Pkg)`
  • + [新增呼叫邊] `Encode.ServeHTTP` ──[CALLS]──> `strings.Join (External/Pkg)`
  • + [新增呼叫邊] `Encode.ServeHTTP` ──[CALLS]──> `strings.ReplaceAll (External/Pkg)`
  • - [移除呼叫邊] `Encode.ServeHTTP` ──[CALLS]──> `r.Header.Get (External/Pkg)`
  • - [移除呼叫邊] `Encode.ServeHTTP` ──[CALLS]──> `strings.HasPrefix (External/Pkg)`
  • - [移除呼叫邊] `Encode.ServeHTTP` ──[CALLS]──> `strings.CutSuffix (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Encode.ServeHTTP()`
- **變更前簽章 (Before)**: `func Encode.ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler)` (L164~L201)
- **變更後簽章 (After)**: `func Encode.ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler)` (L164~L201)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (enc *Encode) ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler) error {
	if isEncodeAllowed(r.Header) {
		for _, encName := range AcceptedEncodings(r, enc.Prefer) {
			if _, ok := enc.writerPools[encName]; !ok {
				continue // encoding not offered
			}
			w = enc.openResponseWriter(encName, w, r.Method == http.MethodConnect)
			defer w.(*responseWriter).Close()

			// to comply with RFC 9110 section 8.8.3(.3), we modify the Etag when encoding
			// by appending a hyphen and the encoder name; the problem is, the client will
			// send back that Etag in an If-None-Match header, but upstream handlers that set
			// the Etag in the first place don't know that we appended to their Etag! so here
			// we have to strip our addition so the upstream handlers can still honor client
			// caches without knowing about our changes...
			if etag := r.Header.Get("If-None-Match"); etag != "" && !strings.HasPrefix(etag, "W/") {
				ourSuffix := "-" + encName + `"`
				if before, ok := strings.CutSuffix(etag, ourSuffix); ok {
					etag = before + `"`
					r.Header.Set("If-None-Match", etag)
				}
			}

			break
		}
	}

	err := next.ServeHTTP(w, r)
	// If there was an error, disable encoding completely
	// This prevents corruption when handle_errors processes the response
	if err != nil {
		if ew, ok := w.(*responseWriter); ok {
			ew.disabled = true
		}
	}

	return err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (enc *Encode) ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler) error {
	if isEncodeAllowed(r.Header) {
		for _, encName := range AcceptedEncodings(r, enc.Prefer) {
			if _, ok := enc.writerPools[encName]; !ok {
				continue // encoding not offered
			}
			w = enc.openResponseWriter(encName, w, r.Method == http.MethodConnect)
			defer w.(*responseWriter).Close()

			// to comply with RFC 9110 section 8.8.3(.3), we modify the Etag when encoding
			// by appending a hyphen and the encoder name; the problem is, the client will
			// send back that Etag in an If-None-Match header, but upstream handlers that set
			// the Etag in the first place don't know that we appended to their Etag! so here
			// we have to strip our addition so the upstream handlers can still honor client
			// caches without knowing about our changes...
			if etags := r.Header.Values("If-None-Match"); len(etags) > 0 {
				etag := strings.Join(etags, ", ")
				stripped := strings.ReplaceAll(etag, "-"+encName+`"`, `"`)
				if stripped != etag || len(etags) > 1 {
					r.Header.Set("If-None-Match", stripped)
				}
			}

			break
		}
	}

	err := next.ServeHTTP(w, r)
	// If there was an error, disable encoding completely
	// This prevents corruption when handle_errors processes the response
	if err != nil {
		if ew, ok := w.(*responseWriter); ok {
			ew.disabled = true
		}
	}

	return err
}
```


---

### 🔹 Commit #14: `8f549e6d`
- **完整 Hash**: `8f549e6df151f6a947bc183200c5d26baefa8666`
- **說明 (Ground Truth)**: timeouts: take precedence over server-wide and enclosing idle timeouts (#8121)
- **變更檔案數**: 3

#### 📄 檔案: `modules/caddyhttp/idletimeout.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:35, E:54, A:0) ➔ After(N:48, E:69, A:0)
- **差分統計**: +Nodes: 13, -Nodes: 0, +Edges: 15, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `idleTimeoutsCtxKey` (MODULE_STATE)
  • + [新增節點] `IdleTimeoutWriter.Override` (FUNCTION_DEF)
  • + [新增節點] `IdleTimeoutReader.Override` (FUNCTION_DEF)
  • + [新增節點] `IdleTimeoutsFromContext` (FUNCTION_DEF)
  • + [新增節點] `prev.Start.Add (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `IdleTimeoutReader.rearmLocked` (FUNCTION_DEF)
  • + [新增節點] `ContextWithIdleTimeouts` (FUNCTION_DEF)
  • + [新增節點] `time.Since (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `IdleDeadline.override` (FUNCTION_DEF)
  • + [新增節點] `context.WithValue (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `ctx.Value (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `IdleDeadline.restore` (FUNCTION_DEF)
  • + [新增節點] `IdleTimeoutWriter.rearm` (FUNCTION_DEF)
  • + [新增呼叫邊] `IdleDeadline.override` ──[CALLS]──> `time.Now (External/Pkg)`
  • + [新增呼叫邊] `IdleDeadline.restore` ──[CALLS]──> `prev.Start.Add (External/Pkg)`
  • _... 以及其餘 13 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `modules/caddyhttp/server.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:153, E:194, A:0) ➔ After(N:156, E:195, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 10, -Edges: 9, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `idleWriter` (MODULE_STATE)
  • + [新增節點] `idleReader` (MODULE_STATE)
  • + [新增節點] `prepareRequest` (FUNCTION_DEF)
  • + [新增呼叫邊] `Server.ServeHTTP` ──[CALLS]──> `prepareRequest`
  • + [新增呼叫邊] `PrepareRequest` ──[CALLS]──> `prepareRequest`
  • + [新增呼叫邊] `prepareRequest` ──[CALLS]──> `context.WithValue (External/Pkg)`
  • + [新增呼叫邊] `prepareRequest` ──[CALLS]──> `r.Context (External/Pkg)`
  • + [新增呼叫邊] `prepareRequest` ──[CALLS]──> `determineTrustedProxy`
  • + [新增呼叫邊] `prepareRequest` ──[CALLS]──> `make (External/Pkg)`
  • + [新增呼叫邊] `prepareRequest` ──[CALLS]──> `originalRequest`
  • + [新增呼叫邊] `prepareRequest` ──[CALLS]──> `new (External/Pkg)`
  • + [新增呼叫邊] `prepareRequest` ──[CALLS]──> `r.WithContext (External/Pkg)`
  • + [新增呼叫邊] `prepareRequest` ──[CALLS]──> `addHTTPVarsToReplacer (External/Pkg)`
  • - [移除呼叫邊] `Server.ServeHTTP` ──[CALLS]──> `PrepareRequest`
  • - [移除呼叫邊] `PrepareRequest` ──[CALLS]──> `context.WithValue (External/Pkg)`
  • _... 以及其餘 7 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `PrepareRequest()`
- **變更前簽章 (Before)**: `func PrepareRequest(r *http.Request, repl *caddy.Replacer, w http.ResponseWriter, s *Server)` (L1372~L1396)
- **變更後簽章 (After)**: `func PrepareRequest(r *http.Request, repl *caddy.Replacer, w http.ResponseWriter, s *Server)` (L1374~L1376)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func PrepareRequest(r *http.Request, repl *caddy.Replacer, w http.ResponseWriter, s *Server) *http.Request {
	// set up the context for the request
	ctx := context.WithValue(r.Context(), caddy.ReplacerCtxKey, repl)
	ctx = context.WithValue(ctx, ServerCtxKey, s)

	trusted, clientIP := determineTrustedProxy(r, s)
	ctx = context.WithValue(ctx, VarsCtxKey, map[string]any{
		TrustedProxyVarKey: trusted,
		ClientIPVarKey:     clientIP,
	})

	ctx = context.WithValue(ctx, routeGroupCtxKey, make(map[string]struct{}))

	var url2 url.URL // avoid letting this escape to the heap
	ctx = context.WithValue(ctx, OriginalRequestCtxKey, originalRequest(r, &url2))

	ctx = context.WithValue(ctx, ExtraLogFieldsCtxKey, new(ExtraLogFields))
	r = r.WithContext(ctx)

	// once the pointer to the request won't change
	// anymore, finish setting up the replacer
	addHTTPVarsToReplacer(repl, r, w)

	return r
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func PrepareRequest(r *http.Request, repl *caddy.Replacer, w http.ResponseWriter, s *Server) *http.Request {
	return prepareRequest(r, repl, w, s, idleTimeouts{})
}
```

### 🔹 函式: `Server.ServeHTTP()`
- **變更前簽章 (Before)**: `func Server.ServeHTTP(w http.ResponseWriter, r *http.Request)` (L551~L787)
- **變更後簽章 (After)**: `func Server.ServeHTTP(w http.ResponseWriter, r *http.Request)` (L551~L789)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	start := time.Now()

	// If there are listener wrappers that process tls connections but don't return a *tls.Conn, this field will be nil.
	if r.TLS == nil {
		if tlsConnStateFunc, ok := r.Context().Value(tlsConnectionStateFuncCtxKey).(func() *tls.ConnectionState); ok {
			r.TLS = tlsConnStateFunc()
		}
	}

	// enable full-duplex for HTTP/1, ensuring the entire
	// request body gets consumed before writing the response
	if s.EnableFullDuplex && r.ProtoMajor == 1 {
		if err := http.NewResponseController(w).EnableFullDuplex(); err != nil { //nolint:bodyclose
			if c := s.logger.Check(zapcore.WarnLevel, "failed to enable full duplex"); c != nil {
				c.Write(zap.Error(err))
			}
		}
	}

	// guard against slowloris-style attacks by aborting the connection
	// if a read from the request body or a write to the response
	// stalls for longer than the configured timeout; the deadline is
	// reset on every successful read/write, so this doesn't affect
	// legitimately slow clients as long as they keep making progress.
	// hardDeadline, anchored to this handler's start, caps how far
	// that reset can push the deadline out, so an explicitly configured
	// ReadTimeout/WriteTimeout ceiling still applies on top instead of
	// being silently overwritten by the first read/write.
	rc := http.NewResponseController(w)
	var readHardDeadline, writeHardDeadline time.Time
	if s.ReadTimeout > 0 {
		readHardDeadline = start.Add(time.Duration(s.ReadTimeout))
	}
	if s.WriteTimeout > 0 {
		writeHardDeadline = start.Add(time.Duration(s.WriteTimeout))
	}
	if s.ReadIdleTimeout > 0 && r.Body != nil {
		idleReader := &IdleTimeoutReader{
			ReadCloser: r.Body,
			Ctrl:       rc,
			Deadline: IdleDeadline{
				Start:        start,
				Timeout:      time.Duration(s.ReadIdleTimeout),
				MinRate:      s.ReadMinRate,
				HardDeadline: readHardDeadline,
			},
			Logger:        s.logger,
			DrainDeadline: r.ProtoMajor == 1 && r.ContentLength != 0,
		}
		defer idleReader.HandlerDone()
		r.Body = idleReader
	}
	if s.WriteIdleTimeout > 0 {
		idleWriter := &IdleTimeoutWriter{
			ResponseWriterWrapper: &ResponseWriterWrapper{ResponseWriter: w},
			Ctrl:                  rc,
			Deadline: IdleDeadline{
				Start:        start,
				Timeout:      time.Duration(s.WriteIdleTimeout),
				MinRate:      s.WriteMinRate,
				HardDeadline: writeHardDeadline,
			},
			MaxChunk:           s.MaxWriteChunk,
			Logger:             s.logger,
			ClearBetweenWrites: r.ProtoMajor == 2,
		}
		defer idleWriter.HandlerDone()
		w = idleWriter
	}

	// set the Server header
	h := w.Header()
	h["Server"] = serverHeader

	// advertise HTTP/3, if enabled
	if s.h3server != nil && r.ProtoMajor < 3 {
		if err := s.h3server.SetQUICHeaders(h); err != nil {
			lvl := zapcore.ErrorLevel
			if errors.Is(err, http3.ErrNoAltSvcPort) {
				lvl = zapcore.DebugLevel
			}
			if c := s.logger.Check(lvl, "setting HTTP/3 Alt-Svc header"); c != nil {
				c.Write(zap.Error(err))
			}
		}
	}

	// prepare internals of the request for the handler pipeline
	repl := caddy.NewReplacer()
	r = PrepareRequest(r, repl, w, s)

	// clone the request for logging purposes before it enters any handler chain;
	// this is necessary to capture the original request in case it gets modified
	// during handling (cloning the request and using .WithLazy is considerably
	// faster than using .With, which will JSON-encode the request immediately)
	shouldLogCredentials := s.Logs != nil && s.Logs.ShouldLogCredentials
	loggableReq := zap.Object("request", LoggableHTTPRequest{
		Request:              r.Clone(r.Context()),
		ShouldLogCredentials: shouldLogCredentials,
	})
	errLog := s.errorLogger.WithLazy(loggableReq)

	var duration time.Duration
	var wrec ResponseRecorder
	var writeErr error

	if s.shouldLogRequest(r) {
		wrec = NewResponseRecorder(w, nil, nil)
		w = wrec

		// wrap the request body in a LengthReader
		// so we can track the number of bytes read from it
		var bodyReader *lengthReader
		if r.Body != nil {
			bodyReader = &lengthReader{Source: r.Body}
			r.Body = bodyReader
			// should always be true, private interface can only be referenced in the same package
			if setReadSizer, ok := wrec.(interface{ setReadSize(*int) }); ok {
				setReadSizer.setReadSize(&bodyReader.Length)
			}
		}

		// capture the original version of the request
		accLog := s.accessLogger.WithLazy(loggableReq)

		defer s.logRequest(accLog, r, wrec, &duration, &writeErr, repl, bodyReader, shouldLogCredentials)

		// if the request went past the write timeout, flush so the access log can
		// see the write error. deferred because flushing before the error routes
		// run would commit a 200 and lose the error status. it sits after the
		// access log defer so it still runs first.
		defer func() {
			if s.WriteTimeout <= 0 ||
				r.ProtoMajor != 1 ||
				duration < time.Duration(s.WriteTimeout) {
				return
			}
			// over wrec, not the rc above: this reaches the recorder's
			// FlushError, which skips buffered responses (#6144); rc sits
			// below the recorder and would flush them anyway.
			flushErr := http.NewResponseController(wrec).Flush()
			if flushErr != nil &&
				!errors.Is(flushErr, http.ErrHijacked) &&
				!errors.Is(flushErr, http.ErrNotSupported) {
				writeErr = flushErr
			}
		}()
	}

	// guarantee ACME HTTP challenges; handle them separately from any user-defined handlers
	if s.tlsApp.HandleHTTPChallenge(w, r) {
		duration = time.Since(start)
		return
	}

	err := s.serveHTTP(w, r)
	duration = time.Since(start)

	if err == nil {
		return
	}

	// restore original request before invoking error handler chain (issue #3717)
	// NOTE: this does not restore original headers if modified (for efficiency)
	origReq, ok := r.Context().Value(OriginalRequestCtxKey).(http.Request)
	if ok {
		r.Method = origReq.Method
		r.RemoteAddr = origReq.RemoteAddr
		r.RequestURI = origReq.RequestURI
		cloneURL(origReq.URL, r.URL)
	}

	// prepare the error log
	errLog = errLog.With(zap.Duration("duration", duration))
	errLoggers := []*zap.Logger{errLog}
	if s.Logs != nil {
		errLoggers = s.Logs.wrapLogger(errLog, r)
	}

	// get the values that will be used to log the error
	errStatus, errMsg, errFields := errLogValues(err)

	// add HTTP error information to request context
	r = s.Errors.WithError(r, err)

	var fields []zapcore.Field
	if s.Errors != nil && len(s.Errors.Routes) > 0 {
		// execute user-defined error handling route
		if err2 := s.errorHandlerChain.ServeHTTP(w, r); err2 == nil {
			// user's error route handled the error response successfully, so now just log the error
			for _, logger := range errLoggers {
				if c := logger.Check(zapcore.DebugLevel, errMsg); c != nil {
					if fields == nil {
						fields = errFields()
					}
					c.Write(fields...)
				}
			}
		} else {
			// well... this is awkward
			for _, logger := range errLoggers {
				if c := logger.Check(zapcore.ErrorLevel, "error handling handler error"); c != nil {
					if fields == nil {
						fields = errFields()
						fields = append([]zapcore.Field{
							zap.String("error", err2.Error()),
							zap.Namespace("first_error"),
							zap.String("msg", errMsg),
						}, fields...)
					}
					c.Write(fields...)
				}
			}
			if handlerErr, ok := err.(HandlerError); ok {
				w.WriteHeader(handlerErr.StatusCode)
			} else {
				w.WriteHeader(http.StatusInternalServerError)
			}
		}
	} else {
		logLevel := zapcore.DebugLevel
		if errStatus >= 500 {
			logLevel = zapcore.ErrorLevel
		}

		for _, logger := range errLoggers {
			if c := logger.Check(logLevel, errMsg); c != nil {
				if fields == nil {
					fields = errFields()
				}
				c.Write(fields...)
			}
		}
		w.WriteHeader(errStatus)
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	start := time.Now()

	// If there are listener wrappers that process tls connections but don't return a *tls.Conn, this field will be nil.
	if r.TLS == nil {
		if tlsConnStateFunc, ok := r.Context().Value(tlsConnectionStateFuncCtxKey).(func() *tls.ConnectionState); ok {
			r.TLS = tlsConnStateFunc()
		}
	}

	// enable full-duplex for HTTP/1, ensuring the entire
	// request body gets consumed before writing the response
	if s.EnableFullDuplex && r.ProtoMajor == 1 {
		if err := http.NewResponseController(w).EnableFullDuplex(); err != nil { //nolint:bodyclose
			if c := s.logger.Check(zapcore.WarnLevel, "failed to enable full duplex"); c != nil {
				c.Write(zap.Error(err))
			}
		}
	}

	// guard against slowloris-style attacks by aborting the connection
	// if a read from the request body or a write to the response
	// stalls for longer than the configured timeout; the deadline is
	// reset on every successful read/write, so this doesn't affect
	// legitimately slow clients as long as they keep making progress.
	// hardDeadline, anchored to this handler's start, caps how far
	// that reset can push the deadline out, so an explicitly configured
	// ReadTimeout/WriteTimeout ceiling still applies on top instead of
	// being silently overwritten by the first read/write.
	rc := http.NewResponseController(w)
	var readHardDeadline, writeHardDeadline time.Time
	if s.ReadTimeout > 0 {
		readHardDeadline = start.Add(time.Duration(s.ReadTimeout))
	}
	if s.WriteTimeout > 0 {
		writeHardDeadline = start.Add(time.Duration(s.WriteTimeout))
	}
	var idleReader *IdleTimeoutReader
	var idleWriter *IdleTimeoutWriter
	if s.ReadIdleTimeout > 0 && r.Body != nil {
		idleReader = &IdleTimeoutReader{
			ReadCloser: r.Body,
			Ctrl:       rc,
			Deadline: IdleDeadline{
				Start:        start,
				Timeout:      time.Duration(s.ReadIdleTimeout),
				MinRate:      s.ReadMinRate,
				HardDeadline: readHardDeadline,
			},
			Logger:        s.logger,
			DrainDeadline: r.ProtoMajor == 1 && r.ContentLength != 0,
		}
		defer idleReader.HandlerDone()
		r.Body = idleReader
	}
	if s.WriteIdleTimeout > 0 {
		idleWriter = &IdleTimeoutWriter{
			ResponseWriterWrapper: &ResponseWriterWrapper{ResponseWriter: w},
			Ctrl:                  rc,
			Deadline: IdleDeadline{
				Start:        start,
				Timeout:      time.Duration(s.WriteIdleTimeout),
				MinRate:      s.WriteMinRate,
				HardDeadline: writeHardDeadline,
			},
			MaxChunk:           s.MaxWriteChunk,
			Logger:             s.logger,
			ClearBetweenWrites: r.ProtoMajor == 2,
		}
		defer idleWriter.HandlerDone()
		w = idleWriter
	}

	// set the Server header
	h := w.Header()
	h["Server"] = serverHeader

	// advertise HTTP/3, if enabled
	if s.h3server != nil && r.ProtoMajor < 3 {
		if err := s.h3server.SetQUICHeaders(h); err != nil {
			lvl := zapcore.ErrorLevel
			if errors.Is(err, http3.ErrNoAltSvcPort) {
				lvl = zapcore.DebugLevel
			}
			if c := s.logger.Check(lvl, "setting HTTP/3 Alt-Svc header"); c != nil {
				c.Write(zap.Error(err))
			}
		}
	}

	// prepare internals of the request for the handler pipeline
	repl := caddy.NewReplacer()
	r = prepareRequest(r, repl, w, s, idleTimeouts{reader: idleReader, writer: idleWriter})

	// clone the request for logging purposes before it enters any handler chain;
	// this is necessary to capture the original request in case it gets modified
	// during handling (cloning the request and using .WithLazy is considerably
	// faster than using .With, which will JSON-encode the request immediately)
	shouldLogCredentials := s.Logs != nil && s.Logs.ShouldLogCredentials
	loggableReq := zap.Object("request", LoggableHTTPRequest{
		Request:              r.Clone(r.Context()),
		ShouldLogCredentials: shouldLogCredentials,
	})
	errLog := s.errorLogger.WithLazy(loggableReq)

	var duration time.Duration
	var wrec ResponseRecorder
	var writeErr error

	if s.shouldLogRequest(r) {
		wrec = NewResponseRecorder(w, nil, nil)
		w = wrec

		// wrap the request body in a LengthReader
		// so we can track the number of bytes read from it
		var bodyReader *lengthReader
		if r.Body != nil {
			bodyReader = &lengthReader{Source: r.Body}
			r.Body = bodyReader
			// should always be true, private interface can only be referenced in the same package
			if setReadSizer, ok := wrec.(interface{ setReadSize(*int) }); ok {
				setReadSizer.setReadSize(&bodyReader.Length)
			}
		}

		// capture the original version of the request
		accLog := s.accessLogger.WithLazy(loggableReq)

		defer s.logRequest(accLog, r, wrec, &duration, &writeErr, repl, bodyReader, shouldLogCredentials)

		// if the request went past the write timeout, flush so the access log can
		// see the write error. deferred because flushing before the error routes
		// run would commit a 200 and lose the error status. it sits after the
		// access log defer so it still runs first.
		defer func() {
			if s.WriteTimeout <= 0 ||
				r.ProtoMajor != 1 ||
				duration < time.Duration(s.WriteTimeout) {
				return
			}
			// over wrec, not the rc above: this reaches the recorder's
			// FlushError, which skips buffered responses (#6144); rc sits
			// below the recorder and would flush them anyway.
			flushErr := http.NewResponseController(wrec).Flush()
			if flushErr != nil &&
				!errors.Is(flushErr, http.ErrHijacked) &&
				!errors.Is(flushErr, http.ErrNotSupported) {
				writeErr = flushErr
			}
		}()
	}

	// guarantee ACME HTTP challenges; handle them separately from any user-defined handlers
	if s.tlsApp.HandleHTTPChallenge(w, r) {
		duration = time.Since(start)
		return
	}

	err := s.serveHTTP(w, r)
	duration = time.Since(start)

	if err == nil {
		return
	}

	// restore original request before invoking error handler chain (issue #3717)
	// NOTE: this does not restore original headers if modified (for efficiency)
	origReq, ok := r.Context().Value(OriginalRequestCtxKey).(http.Request)
	if ok {
		r.Method = origReq.Method
		r.RemoteAddr = origReq.RemoteAddr
		r.RequestURI = origReq.RequestURI
		cloneURL(origReq.URL, r.URL)
	}

	// prepare the error log
	errLog = errLog.With(zap.Duration("duration", duration))
	errLoggers := []*zap.Logger{errLog}
	if s.Logs != nil {
		errLoggers = s.Logs.wrapLogger(errLog, r)
	}

	// get the values that will be used to log the error
	errStatus, errMsg, errFields := errLogValues(err)

	// add HTTP error information to request context
	r = s.Errors.WithError(r, err)

	var fields []zapcore.Field
	if s.Errors != nil && len(s.Errors.Routes) > 0 {
		// execute user-defined error handling route
		if err2 := s.errorHandlerChain.ServeHTTP(w, r); err2 == nil {
			// user's error route handled the error response successfully, so now just log the error
			for _, logger := range errLoggers {
				if c := logger.Check(zapcore.DebugLevel, errMsg); c != nil {
					if fields == nil {
						fields = errFields()
					}
					c.Write(fields...)
				}
			}
		} else {
			// well... this is awkward
			for _, logger := range errLoggers {
				if c := logger.Check(zapcore.ErrorLevel, "error handling handler error"); c != nil {
					if fields == nil {
						fields = errFields()
						fields = append([]zapcore.Field{
							zap.String("error", err2.Error()),
							zap.Namespace("first_error"),
							zap.String("msg", errMsg),
						}, fields...)
					}
					c.Write(fields...)
				}
			}
			if handlerErr, ok := err.(HandlerError); ok {
				w.WriteHeader(handlerErr.StatusCode)
			} else {
				w.WriteHeader(http.StatusInternalServerError)
			}
		}
	} else {
		logLevel := zapcore.DebugLevel
		if errStatus >= 500 {
			logLevel = zapcore.ErrorLevel
		}

		for _, logger := range errLoggers {
			if c := logger.Check(logLevel, errMsg); c != nil {
				if fields == nil {
					fields = errFields()
				}
				c.Write(fields...)
			}
		}
		w.WriteHeader(errStatus)
	}
}
```


#### 📄 檔案: `modules/caddyhttp/timeouts/timeouts.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:11, E:8, A:0) ➔ After(N:21, E:16, A:0)
- **差分統計**: +Nodes: 10, -Nodes: 0, +Edges: 8, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `r.WithContext (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `idleWriter.Override(t.WriteTimeout, t.WriteMinRate, t.MaxWriteChunk) (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `rc` (MODULE_STATE)
  • + [新增節點] `caddyhttp.IdleTimeoutsFromContext (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `idleReader.Override(t.ReadTimeout, t.ReadMinRate) (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `caddyhttp.ContextWithIdleTimeouts (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `idleReader.Override (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `wrapped` (MODULE_STATE)
  • + [新增節點] `r.Context (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `idleWriter.Override (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Timeouts.ServeHTTP` ──[CALLS]──> `caddyhttp.IdleTimeoutsFromContext (External/Pkg)`
  • + [新增呼叫邊] `Timeouts.ServeHTTP` ──[CALLS]──> `r.Context (External/Pkg)`
  • + [新增呼叫邊] `Timeouts.ServeHTTP` ──[CALLS]──> `idleReader.Override(t.ReadTimeout, t.ReadMinRate) (External/Pkg)`
  • + [新增呼叫邊] `Timeouts.ServeHTTP` ──[CALLS]──> `idleReader.Override (External/Pkg)`
  • + [新增呼叫邊] `Timeouts.ServeHTTP` ──[CALLS]──> `idleWriter.Override(t.WriteTimeout, t.WriteMinRate, t.MaxWriteChunk) (External/Pkg)`
  • _... 以及其餘 3 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Timeouts.ServeHTTP()`
- **變更前簽章 (Before)**: `func Timeouts.ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler)` (L85~L127)
- **變更後簽章 (After)**: `func Timeouts.ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler)` (L89~L157)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (t Timeouts) ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler) error {
	if t.ReadTimeout <= 0 && t.WriteTimeout <= 0 {
		return next.ServeHTTP(w, r)
	}

	//nolint:bodyclose
	rc := http.NewResponseController(w)
	start := time.Now()

	if t.ReadTimeout > 0 && r.Body != nil {
		idleReader := &caddyhttp.IdleTimeoutReader{
			ReadCloser: r.Body,
			Ctrl:       rc,
			Deadline: caddyhttp.IdleDeadline{
				Start:   start,
				Timeout: t.ReadTimeout,
				MinRate: t.ReadMinRate,
			},
			Logger:        t.logger,
			DrainDeadline: r.ProtoMajor == 1 && r.ContentLength != 0,
		}
		defer idleReader.HandlerDone()
		r.Body = idleReader
	}
	if t.WriteTimeout > 0 {
		idleWriter := &caddyhttp.IdleTimeoutWriter{
			ResponseWriterWrapper: &caddyhttp.ResponseWriterWrapper{ResponseWriter: w},
			Ctrl:                  rc,
			Deadline: caddyhttp.IdleDeadline{
				Start:   start,
				Timeout: t.WriteTimeout,
				MinRate: t.WriteMinRate,
			},
			MaxChunk:           t.MaxWriteChunk,
			Logger:             t.logger,
			ClearBetweenWrites: r.ProtoMajor == 2,
		}
		defer idleWriter.HandlerDone()
		w = idleWriter
	}

	return next.ServeHTTP(w, r)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (t Timeouts) ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler) error {
	if t.ReadTimeout <= 0 && t.WriteTimeout <= 0 {
		return next.ServeHTTP(w, r)
	}

	// if the request already has idle timeouts, from the server or an
	// enclosing route, override them instead of wrapping again: the
	// wrapper closest to the connection sets the deadline last, so it
	// would take precedence over ours
	idleReader, idleWriter := caddyhttp.IdleTimeoutsFromContext(r.Context())
	var wrapped bool
	var rc *http.ResponseController
	start := time.Now()

	if t.ReadTimeout > 0 && r.Body != nil {
		if idleReader != nil {
			defer idleReader.Override(t.ReadTimeout, t.ReadMinRate)()
		} else {
			//nolint:bodyclose
			rc = http.NewResponseController(w)
			idleReader = &caddyhttp.IdleTimeoutReader{
				ReadCloser: r.Body,
				Ctrl:       rc,
				Deadline: caddyhttp.IdleDeadline{
					Start:   start,
					Timeout: t.ReadTimeout,
					MinRate: t.ReadMinRate,
				},
				Logger:        t.logger,
				DrainDeadline: r.ProtoMajor == 1 && r.ContentLength != 0,
			}
			defer idleReader.HandlerDone()
			r.Body = idleReader
			wrapped = true
		}
	}
	if t.WriteTimeout > 0 {
		if idleWriter != nil {
			defer idleWriter.Override(t.WriteTimeout, t.WriteMinRate, t.MaxWriteChunk)()
		} else {
			if rc == nil {
				//nolint:bodyclose
				rc = http.NewResponseController(w)
			}
			idleWriter = &caddyhttp.IdleTimeoutWriter{
				ResponseWriterWrapper: &caddyhttp.ResponseWriterWrapper{ResponseWriter: w},
				Ctrl:                  rc,
				Deadline: caddyhttp.IdleDeadline{
					Start:   start,
					Timeout: t.WriteTimeout,
					MinRate: t.WriteMinRate,
				},
				MaxChunk:           t.MaxWriteChunk,
				Logger:             t.logger,
				ClearBetweenWrites: r.ProtoMajor == 2,
			}
			defer idleWriter.HandlerDone()
			w = idleWriter
			wrapped = true
		}
	}

	// let nested timeouts handlers override the wrappers added here
	if wrapped {
		r = r.WithContext(caddyhttp.ContextWithIdleTimeouts(r.Context(), idleReader, idleWriter))
	}

	return next.ServeHTTP(w, r)
}
```


---

### 🔹 Commit #15: `72dd0fb0`
- **完整 Hash**: `72dd0fb067f6d7826c7f79907670ba4a713bfe37`
- **說明 (Ground Truth)**: timeouts: fix idle writer terminate h2 response writers between writes (#8119)
- **變更檔案數**: 3

#### 📄 檔案: `modules/caddyhttp/idletimeout.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:28, E:40, A:0) ➔ After(N:35, E:54, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 14, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `IdleTimeoutWriter.clearDeadline` (FUNCTION_DEF)
  • + [新增節點] `w.Deadline.HardDeadline.IsZero (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `time.Now().Before (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `IdleTimeoutWriter.HandlerDone` (FUNCTION_DEF)
  • + [新增節點] `http.NewResponseController (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `IdleTimeoutWriter.FlushError` (FUNCTION_DEF)
  • + [新增節點] `http.NewResponseController(w.ResponseWriter).Flush (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `IdleTimeoutWriter.clearDeadline` ──[CALLS]──> `w.Deadline.HardDeadline.IsZero (External/Pkg)`
  • + [新增呼叫邊] `IdleTimeoutWriter.clearDeadline` ──[CALLS]──> `time.Now().Before (External/Pkg)`
  • + [新增呼叫邊] `IdleTimeoutWriter.clearDeadline` ──[CALLS]──> `time.Now (External/Pkg)`
  • + [新增呼叫邊] `IdleTimeoutWriter.clearDeadline` ──[CALLS]──> `w.Ctrl.SetWriteDeadline (External/Pkg)`
  • + [新增呼叫邊] `IdleTimeoutWriter.clearDeadline` ──[CALLS]──> `w.Logger.Check (External/Pkg)`
  • + [新增呼叫邊] `IdleTimeoutWriter.clearDeadline` ──[CALLS]──> `IdleTimeoutWriter.Write`
  • + [新增呼叫邊] `IdleTimeoutWriter.clearDeadline` ──[CALLS]──> `zap.Error (External/Pkg)`
  • + [新增呼叫邊] `IdleTimeoutWriter.HandlerDone` ──[CALLS]──> `IdleTimeoutWriter.resetDeadline`
  • _... 以及其餘 6 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `IdleTimeoutWriter.Write()`
- **變更前簽章 (Before)**: `func IdleTimeoutWriter.Write(p []byte)` (L217~L235)
- **變更後簽章 (After)**: `func IdleTimeoutWriter.Write(p []byte)` (L273~L295)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (w *IdleTimeoutWriter) Write(p []byte) (int, error) {
	maxChunk := w.maxChunk()
	var total int
	for len(p) > 0 {
		chunk := p
		if len(chunk) > maxChunk {
			chunk = chunk[:maxChunk]
		}
		w.resetDeadline()
		n, err := w.ResponseWriterWrapper.Write(chunk)
		total += n
		w.Deadline.transferred += int64(n)
		p = p[n:]
		if err != nil {
			return total, err
		}
	}
	return total, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (w *IdleTimeoutWriter) Write(p []byte) (int, error) {
	maxChunk := w.maxChunk()
	var total int
	for len(p) > 0 {
		chunk := p
		if len(chunk) > maxChunk {
			chunk = chunk[:maxChunk]
		}
		w.resetDeadline()
		n, err := w.ResponseWriterWrapper.Write(chunk)
		total += n
		w.Deadline.transferred += int64(n)
		p = p[n:]
		if n > 0 {
			w.unflushed = true
		}
		if err != nil {
			return total, err
		}
	}
	w.clearDeadline()
	return total, nil
}
```

### 🔹 函式: `IdleTimeoutWriter.ReadFrom()`
- **變更前簽章 (Before)**: `func IdleTimeoutWriter.ReadFrom(r io.Reader)` (L237~L252)
- **變更後簽章 (After)**: `func IdleTimeoutWriter.ReadFrom(r io.Reader)` (L297~L319)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (w *IdleTimeoutWriter) ReadFrom(r io.Reader) (int64, error) {
	maxChunk := w.maxChunk()
	var total int64
	for {
		w.resetDeadline()
		n, err := w.ResponseWriterWrapper.ReadFrom(io.LimitReader(r, int64(maxChunk)))
		total += n
		w.Deadline.transferred += n
		if err != nil {
			return total, err
		}
		if n < int64(maxChunk) {
			return total, nil
		}
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (w *IdleTimeoutWriter) ReadFrom(r io.Reader) (int64, error) {
	maxChunk := w.maxChunk()
	var total int64
	for {
		w.resetDeadline()
		n, err := w.ResponseWriterWrapper.ReadFrom(io.LimitReader(r, int64(maxChunk)))
		total += n
		w.Deadline.transferred += n
		if n > 0 {
			w.unflushed = true
		}
		if err != nil {
			// the error may come from r rather than the client, in
			// which case the response can still be written to
			w.clearDeadline()
			return total, err
		}
		if n < int64(maxChunk) {
			w.clearDeadline()
			return total, nil
		}
	}
}
```

### 🔹 函式: `IdleTimeoutWriter.resetDeadline()`
- **變更前簽章 (Before)**: `func IdleTimeoutWriter.resetDeadline()` (L197~L208)
- **變更後簽章 (After)**: `func IdleTimeoutWriter.resetDeadline()` (L216~L229)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (w *IdleTimeoutWriter) resetDeadline() {
	if w.unsupported {
		return
	}

	if err := w.Ctrl.SetWriteDeadline(w.Deadline.next()); err != nil {
		w.unsupported = true
		if c := w.Logger.Check(zapcore.DebugLevel, "could not set write deadline"); c != nil {
			c.Write(zap.Error(err))
		}
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (w *IdleTimeoutWriter) resetDeadline() {
	if w.unsupported {
		return
	}

	if err := w.Ctrl.SetWriteDeadline(w.Deadline.next()); err != nil {
		w.unsupported = true
		if c := w.Logger.Check(zapcore.DebugLevel, "could not set write deadline"); c != nil {
			c.Write(zap.Error(err))
		}
		return
	}
	w.deadlineSet = true
}
```


#### 📄 檔案: `modules/caddyhttp/server.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:152, E:193, A:0) ➔ After(N:153, E:194, A:0)
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
  • + [新增節點] `idleWriter.HandlerDone (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Server.ServeHTTP` ──[CALLS]──> `idleWriter.HandlerDone (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Server.ServeHTTP()`
- **變更前簽章 (Before)**: `func Server.ServeHTTP(w http.ResponseWriter, r *http.Request)` (L551~L784)
- **變更後簽章 (After)**: `func Server.ServeHTTP(w http.ResponseWriter, r *http.Request)` (L551~L787)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	start := time.Now()

	// If there are listener wrappers that process tls connections but don't return a *tls.Conn, this field will be nil.
	if r.TLS == nil {
		if tlsConnStateFunc, ok := r.Context().Value(tlsConnectionStateFuncCtxKey).(func() *tls.ConnectionState); ok {
			r.TLS = tlsConnStateFunc()
		}
	}

	// enable full-duplex for HTTP/1, ensuring the entire
	// request body gets consumed before writing the response
	if s.EnableFullDuplex && r.ProtoMajor == 1 {
		if err := http.NewResponseController(w).EnableFullDuplex(); err != nil { //nolint:bodyclose
			if c := s.logger.Check(zapcore.WarnLevel, "failed to enable full duplex"); c != nil {
				c.Write(zap.Error(err))
			}
		}
	}

	// guard against slowloris-style attacks by aborting the connection
	// if a read from the request body or a write to the response
	// stalls for longer than the configured timeout; the deadline is
	// reset on every successful read/write, so this doesn't affect
	// legitimately slow clients as long as they keep making progress.
	// hardDeadline, anchored to this handler's start, caps how far
	// that reset can push the deadline out, so an explicitly configured
	// ReadTimeout/WriteTimeout ceiling still applies on top instead of
	// being silently overwritten by the first read/write.
	rc := http.NewResponseController(w)
	var readHardDeadline, writeHardDeadline time.Time
	if s.ReadTimeout > 0 {
		readHardDeadline = start.Add(time.Duration(s.ReadTimeout))
	}
	if s.WriteTimeout > 0 {
		writeHardDeadline = start.Add(time.Duration(s.WriteTimeout))
	}
	if s.ReadIdleTimeout > 0 && r.Body != nil {
		idleReader := &IdleTimeoutReader{
			ReadCloser: r.Body,
			Ctrl:       rc,
			Deadline: IdleDeadline{
				Start:        start,
				Timeout:      time.Duration(s.ReadIdleTimeout),
				MinRate:      s.ReadMinRate,
				HardDeadline: readHardDeadline,
			},
			Logger:        s.logger,
			DrainDeadline: r.ProtoMajor == 1 && r.ContentLength != 0,
		}
		defer idleReader.HandlerDone()
		r.Body = idleReader
	}
	if s.WriteIdleTimeout > 0 {
		w = &IdleTimeoutWriter{
			ResponseWriterWrapper: &ResponseWriterWrapper{ResponseWriter: w},
			Ctrl:                  rc,
			Deadline: IdleDeadline{
				Start:        start,
				Timeout:      time.Duration(s.WriteIdleTimeout),
				MinRate:      s.WriteMinRate,
				HardDeadline: writeHardDeadline,
			},
			MaxChunk: s.MaxWriteChunk,
			Logger:   s.logger,
		}
	}

	// set the Server header
	h := w.Header()
	h["Server"] = serverHeader

	// advertise HTTP/3, if enabled
	if s.h3server != nil && r.ProtoMajor < 3 {
		if err := s.h3server.SetQUICHeaders(h); err != nil {
			lvl := zapcore.ErrorLevel
			if errors.Is(err, http3.ErrNoAltSvcPort) {
				lvl = zapcore.DebugLevel
			}
			if c := s.logger.Check(lvl, "setting HTTP/3 Alt-Svc header"); c != nil {
				c.Write(zap.Error(err))
			}
		}
	}

	// prepare internals of the request for the handler pipeline
	repl := caddy.NewReplacer()
	r = PrepareRequest(r, repl, w, s)

	// clone the request for logging purposes before it enters any handler chain;
	// this is necessary to capture the original request in case it gets modified
	// during handling (cloning the request and using .WithLazy is considerably
	// faster than using .With, which will JSON-encode the request immediately)
	shouldLogCredentials := s.Logs != nil && s.Logs.ShouldLogCredentials
	loggableReq := zap.Object("request", LoggableHTTPRequest{
		Request:              r.Clone(r.Context()),
		ShouldLogCredentials: shouldLogCredentials,
	})
	errLog := s.errorLogger.WithLazy(loggableReq)

	var duration time.Duration
	var wrec ResponseRecorder
	var writeErr error

	if s.shouldLogRequest(r) {
		wrec = NewResponseRecorder(w, nil, nil)
		w = wrec

		// wrap the request body in a LengthReader
		// so we can track the number of bytes read from it
		var bodyReader *lengthReader
		if r.Body != nil {
			bodyReader = &lengthReader{Source: r.Body}
			r.Body = bodyReader
			// should always be true, private interface can only be referenced in the same package
			if setReadSizer, ok := wrec.(interface{ setReadSize(*int) }); ok {
				setReadSizer.setReadSize(&bodyReader.Length)
			}
		}

		// capture the original version of the request
		accLog := s.accessLogger.WithLazy(loggableReq)

		defer s.logRequest(accLog, r, wrec, &duration, &writeErr, repl, bodyReader, shouldLogCredentials)

		// if the request went past the write timeout, flush so the access log can
		// see the write error. deferred because flushing before the error routes
		// run would commit a 200 and lose the error status. it sits after the
		// access log defer so it still runs first.
		defer func() {
			if s.WriteTimeout <= 0 ||
				r.ProtoMajor != 1 ||
				duration < time.Duration(s.WriteTimeout) {
				return
			}
			// over wrec, not the rc above: this reaches the recorder's
			// FlushError, which skips buffered responses (#6144); rc sits
			// below the recorder and would flush them anyway.
			flushErr := http.NewResponseController(wrec).Flush()
			if flushErr != nil &&
				!errors.Is(flushErr, http.ErrHijacked) &&
				!errors.Is(flushErr, http.ErrNotSupported) {
				writeErr = flushErr
			}
		}()
	}

	// guarantee ACME HTTP challenges; handle them separately from any user-defined handlers
	if s.tlsApp.HandleHTTPChallenge(w, r) {
		duration = time.Since(start)
		return
	}

	err := s.serveHTTP(w, r)
	duration = time.Since(start)

	if err == nil {
		return
	}

	// restore original request before invoking error handler chain (issue #3717)
	// NOTE: this does not restore original headers if modified (for efficiency)
	origReq, ok := r.Context().Value(OriginalRequestCtxKey).(http.Request)
	if ok {
		r.Method = origReq.Method
		r.RemoteAddr = origReq.RemoteAddr
		r.RequestURI = origReq.RequestURI
		cloneURL(origReq.URL, r.URL)
	}

	// prepare the error log
	errLog = errLog.With(zap.Duration("duration", duration))
	errLoggers := []*zap.Logger{errLog}
	if s.Logs != nil {
		errLoggers = s.Logs.wrapLogger(errLog, r)
	}

	// get the values that will be used to log the error
	errStatus, errMsg, errFields := errLogValues(err)

	// add HTTP error information to request context
	r = s.Errors.WithError(r, err)

	var fields []zapcore.Field
	if s.Errors != nil && len(s.Errors.Routes) > 0 {
		// execute user-defined error handling route
		if err2 := s.errorHandlerChain.ServeHTTP(w, r); err2 == nil {
			// user's error route handled the error response successfully, so now just log the error
			for _, logger := range errLoggers {
				if c := logger.Check(zapcore.DebugLevel, errMsg); c != nil {
					if fields == nil {
						fields = errFields()
					}
					c.Write(fields...)
				}
			}
		} else {
			// well... this is awkward
			for _, logger := range errLoggers {
				if c := logger.Check(zapcore.ErrorLevel, "error handling handler error"); c != nil {
					if fields == nil {
						fields = errFields()
						fields = append([]zapcore.Field{
							zap.String("error", err2.Error()),
							zap.Namespace("first_error"),
							zap.String("msg", errMsg),
						}, fields...)
					}
					c.Write(fields...)
				}
			}
			if handlerErr, ok := err.(HandlerError); ok {
				w.WriteHeader(handlerErr.StatusCode)
			} else {
				w.WriteHeader(http.StatusInternalServerError)
			}
		}
	} else {
		logLevel := zapcore.DebugLevel
		if errStatus >= 500 {
			logLevel = zapcore.ErrorLevel
		}

		for _, logger := range errLoggers {
			if c := logger.Check(logLevel, errMsg); c != nil {
				if fields == nil {
					fields = errFields()
				}
				c.Write(fields...)
			}
		}
		w.WriteHeader(errStatus)
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	start := time.Now()

	// If there are listener wrappers that process tls connections but don't return a *tls.Conn, this field will be nil.
	if r.TLS == nil {
		if tlsConnStateFunc, ok := r.Context().Value(tlsConnectionStateFuncCtxKey).(func() *tls.ConnectionState); ok {
			r.TLS = tlsConnStateFunc()
		}
	}

	// enable full-duplex for HTTP/1, ensuring the entire
	// request body gets consumed before writing the response
	if s.EnableFullDuplex && r.ProtoMajor == 1 {
		if err := http.NewResponseController(w).EnableFullDuplex(); err != nil { //nolint:bodyclose
			if c := s.logger.Check(zapcore.WarnLevel, "failed to enable full duplex"); c != nil {
				c.Write(zap.Error(err))
			}
		}
	}

	// guard against slowloris-style attacks by aborting the connection
	// if a read from the request body or a write to the response
	// stalls for longer than the configured timeout; the deadline is
	// reset on every successful read/write, so this doesn't affect
	// legitimately slow clients as long as they keep making progress.
	// hardDeadline, anchored to this handler's start, caps how far
	// that reset can push the deadline out, so an explicitly configured
	// ReadTimeout/WriteTimeout ceiling still applies on top instead of
	// being silently overwritten by the first read/write.
	rc := http.NewResponseController(w)
	var readHardDeadline, writeHardDeadline time.Time
	if s.ReadTimeout > 0 {
		readHardDeadline = start.Add(time.Duration(s.ReadTimeout))
	}
	if s.WriteTimeout > 0 {
		writeHardDeadline = start.Add(time.Duration(s.WriteTimeout))
	}
	if s.ReadIdleTimeout > 0 && r.Body != nil {
		idleReader := &IdleTimeoutReader{
			ReadCloser: r.Body,
			Ctrl:       rc,
			Deadline: IdleDeadline{
				Start:        start,
				Timeout:      time.Duration(s.ReadIdleTimeout),
				MinRate:      s.ReadMinRate,
				HardDeadline: readHardDeadline,
			},
			Logger:        s.logger,
			DrainDeadline: r.ProtoMajor == 1 && r.ContentLength != 0,
		}
		defer idleReader.HandlerDone()
		r.Body = idleReader
	}
	if s.WriteIdleTimeout > 0 {
		idleWriter := &IdleTimeoutWriter{
			ResponseWriterWrapper: &ResponseWriterWrapper{ResponseWriter: w},
			Ctrl:                  rc,
			Deadline: IdleDeadline{
				Start:        start,
				Timeout:      time.Duration(s.WriteIdleTimeout),
				MinRate:      s.WriteMinRate,
				HardDeadline: writeHardDeadline,
			},
			MaxChunk:           s.MaxWriteChunk,
			Logger:             s.logger,
			ClearBetweenWrites: r.ProtoMajor == 2,
		}
		defer idleWriter.HandlerDone()
		w = idleWriter
	}

	// set the Server header
	h := w.Header()
	h["Server"] = serverHeader

	// advertise HTTP/3, if enabled
	if s.h3server != nil && r.ProtoMajor < 3 {
		if err := s.h3server.SetQUICHeaders(h); err != nil {
			lvl := zapcore.ErrorLevel
			if errors.Is(err, http3.ErrNoAltSvcPort) {
				lvl = zapcore.DebugLevel
			}
			if c := s.logger.Check(lvl, "setting HTTP/3 Alt-Svc header"); c != nil {
				c.Write(zap.Error(err))
			}
		}
	}

	// prepare internals of the request for the handler pipeline
	repl := caddy.NewReplacer()
	r = PrepareRequest(r, repl, w, s)

	// clone the request for logging purposes before it enters any handler chain;
	// this is necessary to capture the original request in case it gets modified
	// during handling (cloning the request and using .WithLazy is considerably
	// faster than using .With, which will JSON-encode the request immediately)
	shouldLogCredentials := s.Logs != nil && s.Logs.ShouldLogCredentials
	loggableReq := zap.Object("request", LoggableHTTPRequest{
		Request:              r.Clone(r.Context()),
		ShouldLogCredentials: shouldLogCredentials,
	})
	errLog := s.errorLogger.WithLazy(loggableReq)

	var duration time.Duration
	var wrec ResponseRecorder
	var writeErr error

	if s.shouldLogRequest(r) {
		wrec = NewResponseRecorder(w, nil, nil)
		w = wrec

		// wrap the request body in a LengthReader
		// so we can track the number of bytes read from it
		var bodyReader *lengthReader
		if r.Body != nil {
			bodyReader = &lengthReader{Source: r.Body}
			r.Body = bodyReader
			// should always be true, private interface can only be referenced in the same package
			if setReadSizer, ok := wrec.(interface{ setReadSize(*int) }); ok {
				setReadSizer.setReadSize(&bodyReader.Length)
			}
		}

		// capture the original version of the request
		accLog := s.accessLogger.WithLazy(loggableReq)

		defer s.logRequest(accLog, r, wrec, &duration, &writeErr, repl, bodyReader, shouldLogCredentials)

		// if the request went past the write timeout, flush so the access log can
		// see the write error. deferred because flushing before the error routes
		// run would commit a 200 and lose the error status. it sits after the
		// access log defer so it still runs first.
		defer func() {
			if s.WriteTimeout <= 0 ||
				r.ProtoMajor != 1 ||
				duration < time.Duration(s.WriteTimeout) {
				return
			}
			// over wrec, not the rc above: this reaches the recorder's
			// FlushError, which skips buffered responses (#6144); rc sits
			// below the recorder and would flush them anyway.
			flushErr := http.NewResponseController(wrec).Flush()
			if flushErr != nil &&
				!errors.Is(flushErr, http.ErrHijacked) &&
				!errors.Is(flushErr, http.ErrNotSupported) {
				writeErr = flushErr
			}
		}()
	}

	// guarantee ACME HTTP challenges; handle them separately from any user-defined handlers
	if s.tlsApp.HandleHTTPChallenge(w, r) {
		duration = time.Since(start)
		return
	}

	err := s.serveHTTP(w, r)
	duration = time.Since(start)

	if err == nil {
		return
	}

	// restore original request before invoking error handler chain (issue #3717)
	// NOTE: this does not restore original headers if modified (for efficiency)
	origReq, ok := r.Context().Value(OriginalRequestCtxKey).(http.Request)
	if ok {
		r.Method = origReq.Method
		r.RemoteAddr = origReq.RemoteAddr
		r.RequestURI = origReq.RequestURI
		cloneURL(origReq.URL, r.URL)
	}

	// prepare the error log
	errLog = errLog.With(zap.Duration("duration", duration))
	errLoggers := []*zap.Logger{errLog}
	if s.Logs != nil {
		errLoggers = s.Logs.wrapLogger(errLog, r)
	}

	// get the values that will be used to log the error
	errStatus, errMsg, errFields := errLogValues(err)

	// add HTTP error information to request context
	r = s.Errors.WithError(r, err)

	var fields []zapcore.Field
	if s.Errors != nil && len(s.Errors.Routes) > 0 {
		// execute user-defined error handling route
		if err2 := s.errorHandlerChain.ServeHTTP(w, r); err2 == nil {
			// user's error route handled the error response successfully, so now just log the error
			for _, logger := range errLoggers {
				if c := logger.Check(zapcore.DebugLevel, errMsg); c != nil {
					if fields == nil {
						fields = errFields()
					}
					c.Write(fields...)
				}
			}
		} else {
			// well... this is awkward
			for _, logger := range errLoggers {
				if c := logger.Check(zapcore.ErrorLevel, "error handling handler error"); c != nil {
					if fields == nil {
						fields = errFields()
						fields = append([]zapcore.Field{
							zap.String("error", err2.Error()),
							zap.Namespace("first_error"),
							zap.String("msg", errMsg),
						}, fields...)
					}
					c.Write(fields...)
				}
			}
			if handlerErr, ok := err.(HandlerError); ok {
				w.WriteHeader(handlerErr.StatusCode)
			} else {
				w.WriteHeader(http.StatusInternalServerError)
			}
		}
	} else {
		logLevel := zapcore.DebugLevel
		if errStatus >= 500 {
			logLevel = zapcore.ErrorLevel
		}

		for _, logger := range errLoggers {
			if c := logger.Check(logLevel, errMsg); c != nil {
				if fields == nil {
					fields = errFields()
				}
				c.Write(fields...)
			}
		}
		w.WriteHeader(errStatus)
	}
}
```


#### 📄 檔案: `modules/caddyhttp/timeouts/timeouts.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:10, E:7, A:0) ➔ After(N:11, E:8, A:0)
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
  • + [新增節點] `idleWriter.HandlerDone (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Timeouts.ServeHTTP` ──[CALLS]──> `idleWriter.HandlerDone (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Timeouts.ServeHTTP()`
- **變更前簽章 (Before)**: `func Timeouts.ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler)` (L85~L124)
- **變更後簽章 (After)**: `func Timeouts.ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler)` (L85~L127)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (t Timeouts) ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler) error {
	if t.ReadTimeout <= 0 && t.WriteTimeout <= 0 {
		return next.ServeHTTP(w, r)
	}

	//nolint:bodyclose
	rc := http.NewResponseController(w)
	start := time.Now()

	if t.ReadTimeout > 0 && r.Body != nil {
		idleReader := &caddyhttp.IdleTimeoutReader{
			ReadCloser: r.Body,
			Ctrl:       rc,
			Deadline: caddyhttp.IdleDeadline{
				Start:   start,
				Timeout: t.ReadTimeout,
				MinRate: t.ReadMinRate,
			},
			Logger:        t.logger,
			DrainDeadline: r.ProtoMajor == 1 && r.ContentLength != 0,
		}
		defer idleReader.HandlerDone()
		r.Body = idleReader
	}
	if t.WriteTimeout > 0 {
		w = &caddyhttp.IdleTimeoutWriter{
			ResponseWriterWrapper: &caddyhttp.ResponseWriterWrapper{ResponseWriter: w},
			Ctrl:                  rc,
			Deadline: caddyhttp.IdleDeadline{
				Start:   start,
				Timeout: t.WriteTimeout,
				MinRate: t.WriteMinRate,
			},
			MaxChunk: t.MaxWriteChunk,
			Logger:   t.logger,
		}
	}

	return next.ServeHTTP(w, r)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (t Timeouts) ServeHTTP(w http.ResponseWriter, r *http.Request, next caddyhttp.Handler) error {
	if t.ReadTimeout <= 0 && t.WriteTimeout <= 0 {
		return next.ServeHTTP(w, r)
	}

	//nolint:bodyclose
	rc := http.NewResponseController(w)
	start := time.Now()

	if t.ReadTimeout > 0 && r.Body != nil {
		idleReader := &caddyhttp.IdleTimeoutReader{
			ReadCloser: r.Body,
			Ctrl:       rc,
			Deadline: caddyhttp.IdleDeadline{
				Start:   start,
				Timeout: t.ReadTimeout,
				MinRate: t.ReadMinRate,
			},
			Logger:        t.logger,
			DrainDeadline: r.ProtoMajor == 1 && r.ContentLength != 0,
		}
		defer idleReader.HandlerDone()
		r.Body = idleReader
	}
	if t.WriteTimeout > 0 {
		idleWriter := &caddyhttp.IdleTimeoutWriter{
			ResponseWriterWrapper: &caddyhttp.ResponseWriterWrapper{ResponseWriter: w},
			Ctrl:                  rc,
			Deadline: caddyhttp.IdleDeadline{
				Start:   start,
				Timeout: t.WriteTimeout,
				MinRate: t.WriteMinRate,
			},
			MaxChunk:           t.MaxWriteChunk,
			Logger:             t.logger,
			ClearBetweenWrites: r.ProtoMajor == 2,
		}
		defer idleWriter.HandlerDone()
		w = idleWriter
	}

	return next.ServeHTTP(w, r)
}
```


---

### 🔹 Commit #16: `d483d781`
- **完整 Hash**: `d483d7816f7a28fc104a21a2e33f0723261fc758`
- **說明 (Ground Truth)**: listeners: close unix socket immediately and unlink file on reload (#8061)
- **變更檔案數**: 1

#### 📄 檔案: `listen_unix.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:57, E:56, A:0) ➔ After(N:59, E:61, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 5, +Edges: 11, -Edges: 6, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `addr.String (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `uc.LocalAddr (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `strings.HasPrefix (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `uln.closed.CompareAndSwap (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `uc.closed.CompareAndSwap (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `isAbstractUnixSocket` (FUNCTION_DEF)
  • + [新增節點] `uln.Addr (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `uc.File (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `func() {
			unixSocketsMu.Lock()
			delete(unixSockets, uc.mapKey)
			unixSocketsMu.Unlock()
			if err == nil {
				_ = syscall.Unlink(name)
			}
		} (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `file.Name (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `uln.File (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `func() {
			unixSocketsMu.Lock()
			delete(unixSockets, uln.mapKey)
			unixSocketsMu.Unlock()
			if err == nil {
				_ = syscall.Unlink(name)
			}
		} (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `reuseUnixSocket` ──[CALLS]──> `deletePacketConn.Close`
  • + [新增呼叫邊] `reuseUnixSocket` ──[CALLS]──> `isAbstractUnixSocket`
  • + [新增呼叫邊] `unixListener.Close` ──[CALLS]──> `uln.closed.CompareAndSwap (External/Pkg)`
  • _... 以及其餘 14 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `listenReusable()`
- **變更前簽章 (Before)**: `func listenReusable(ctx context.Context, lnKey string, network, address string, config net.ListenConfig)` (L94~L200)
- **變更後簽章 (After)**: `func listenReusable(ctx context.Context, lnKey string, network, address string, config net.ListenConfig)` (L108~L214)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func listenReusable(ctx context.Context, lnKey string, network, address string, config net.ListenConfig) (any, error) {
	// even though SO_REUSEPORT lets us bind the socket multiple times,
	// we still put it in the listenerPool so we can count how many
	// configs are using this socket; necessary to ensure we can know
	// whether to enforce shutdown delays, for example (see #5393).
	var (
		ln         io.Closer
		err        error
		socketFile *os.File
	)

	fd := slices.Contains([]string{"fd", "fdgram"}, network)
	if fd {
		socketFd, err := strconv.ParseUint(address, 0, strconv.IntSize)
		if err != nil {
			return nil, fmt.Errorf("invalid file descriptor: %v", err)
		}

		func() {
			socketFilesMu.Lock()
			defer socketFilesMu.Unlock()

			socketFdWide := uintptr(socketFd)
			var ok bool

			socketFile, ok = socketFiles[socketFdWide]

			if !ok {
				socketFile = os.NewFile(socketFdWide, lnKey)
				if socketFile != nil {
					socketFiles[socketFdWide] = socketFile
				}
			}
		}()

		if socketFile == nil {
			return nil, fmt.Errorf("invalid socket file descriptor: %d", socketFd)
		}
	} else {
		// wrap any Control function set by the user so we can also add our reusePort control without clobbering theirs
		oldControl := config.Control
		config.Control = func(network, address string, c syscall.RawConn) error {
			if oldControl != nil {
				if err := oldControl(network, address, c); err != nil {
					return err
				}
			}
			return reusePort(network, address, c)
		}
	}

	datagram := slices.Contains([]string{"udp", "udp4", "udp6", "unixgram", "fdgram"}, network)
	if datagram {
		if fd {
			ln, err = net.FilePacketConn(socketFile)
		} else {
			ln, err = config.ListenPacket(ctx, network, address)
		}
	} else {
		if fd {
			ln, err = net.FileListener(socketFile)
		} else {
			ln, err = config.Listen(ctx, network, address)
		}
	}

	if err == nil {
		listenerPool.LoadOrStore(lnKey, nil)
	}

	if datagram {
		if !fd {
			// TODO: Not 100% sure this is necessary, but we do this for net.UnixListener, so...
			if unix, ok := ln.(*net.UnixConn); ok {
				cnt := new(atomic.Int32)
				cnt.Store(1)
				ln = &unixConn{unix, lnKey, cnt}
				unixSockets[lnKey] = ln.(*unixConn)
			}
		}
		// lightly wrap the connection so that when it is closed,
		// we can decrement the usage pool counter
		if specificLn, ok := ln.(net.PacketConn); ok {
			ln = deletePacketConn{specificLn, lnKey}
		}
	} else {
		if !fd {
			// if new listener is a unix socket, make sure we can reuse it later
			// (we do our own "unlink on close" -- not required, but more tidy)
			if unix, ok := ln.(*net.UnixListener); ok {
				unix.SetUnlinkOnClose(false)
				cnt := new(atomic.Int32)
				cnt.Store(1)
				ln = &unixListener{unix, lnKey, cnt}
				unixSockets[lnKey] = ln.(*unixListener)
			}
		}
		// lightly wrap the listener so that when it is closed,
		// we can decrement the usage pool counter
		if specificLn, ok := ln.(net.Listener); ok {
			ln = deleteListener{specificLn, lnKey}
		}
	}

	// other types, I guess we just return them directly
	return ln, err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func listenReusable(ctx context.Context, lnKey string, network, address string, config net.ListenConfig) (any, error) {
	// even though SO_REUSEPORT lets us bind the socket multiple times,
	// we still put it in the listenerPool so we can count how many
	// configs are using this socket; necessary to ensure we can know
	// whether to enforce shutdown delays, for example (see #5393).
	var (
		ln         io.Closer
		err        error
		socketFile *os.File
	)

	fd := slices.Contains([]string{"fd", "fdgram"}, network)
	if fd {
		socketFd, err := strconv.ParseUint(address, 0, strconv.IntSize)
		if err != nil {
			return nil, fmt.Errorf("invalid file descriptor: %v", err)
		}

		func() {
			socketFilesMu.Lock()
			defer socketFilesMu.Unlock()

			socketFdWide := uintptr(socketFd)
			var ok bool

			socketFile, ok = socketFiles[socketFdWide]

			if !ok {
				socketFile = os.NewFile(socketFdWide, lnKey)
				if socketFile != nil {
					socketFiles[socketFdWide] = socketFile
				}
			}
		}()

		if socketFile == nil {
			return nil, fmt.Errorf("invalid socket file descriptor: %d", socketFd)
		}
	} else {
		// wrap any Control function set by the user so we can also add our reusePort control without clobbering theirs
		oldControl := config.Control
		config.Control = func(network, address string, c syscall.RawConn) error {
			if oldControl != nil {
				if err := oldControl(network, address, c); err != nil {
					return err
				}
			}
			return reusePort(network, address, c)
		}
	}

	datagram := slices.Contains([]string{"udp", "udp4", "udp6", "unixgram", "fdgram"}, network)
	if datagram {
		if fd {
			ln, err = net.FilePacketConn(socketFile)
		} else {
			ln, err = config.ListenPacket(ctx, network, address)
		}
	} else {
		if fd {
			ln, err = net.FileListener(socketFile)
		} else {
			ln, err = config.Listen(ctx, network, address)
		}
	}

	if err == nil {
		listenerPool.LoadOrStore(lnKey, nil)
	}

	if datagram {
		if !fd {
			// TODO: Not 100% sure this is necessary, but we do this for net.UnixListener, so...
			if unix, ok := ln.(*net.UnixConn); ok {
				cnt := new(atomic.Int32)
				cnt.Store(1)
				ln = &unixConn{UnixConn: unix, mapKey: lnKey, count: cnt}
				unixSockets[lnKey] = ln.(*unixConn)
			}
		}
		// lightly wrap the connection so that when it is closed,
		// we can decrement the usage pool counter
		if specificLn, ok := ln.(net.PacketConn); ok {
			ln = deletePacketConn{specificLn, lnKey}
		}
	} else {
		if !fd {
			// if new listener is a unix socket, make sure we can reuse it later
			// (we do our own "unlink on close" -- not required, but more tidy)
			if unix, ok := ln.(*net.UnixListener); ok {
				unix.SetUnlinkOnClose(false)
				cnt := new(atomic.Int32)
				cnt.Store(1)
				ln = &unixListener{UnixListener: unix, mapKey: lnKey, count: cnt}
				unixSockets[lnKey] = ln.(*unixListener)
			}
		}
		// lightly wrap the listener so that when it is closed,
		// we can decrement the usage pool counter
		if specificLn, ok := ln.(net.Listener); ok {
			ln = deleteListener{specificLn, lnKey}
		}
	}

	// other types, I guess we just return them directly
	return ln, err
}
```

### 🔹 函式: `reuseUnixSocket()`
- **變更前簽章 (Before)**: `func reuseUnixSocket(network, addr string)` (L43~L91)
- **變更後簽章 (After)**: `func reuseUnixSocket(network, addr string)` (L45~L105)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func reuseUnixSocket(network, addr string) (any, error) {
	socketKey := listenerKey(network, addr)

	socket, exists := unixSockets[socketKey]
	if exists {
		// make copy of file descriptor
		socketFile, err := socket.File() // does dup() deep down
		if err != nil {
			return nil, err
		}

		// use copied fd to make new Listener or PacketConn, then replace
		// it in the map so that future copies always come from the most
		// recent fd (as the previous ones will be closed, and we'd get
		// "use of closed network connection" errors) -- note that we
		// preserve the *pointer* to the counter (not just the value) so
		// that all socket wrappers will refer to the same value
		switch unixSocket := socket.(type) {
		case *unixListener:
			ln, err := net.FileListener(socketFile)
			if err != nil {
				return nil, err
			}
			unixSocket.count.Add(1)
			unixSockets[socketKey] = &unixListener{ln.(*net.UnixListener), socketKey, unixSocket.count}

		case *unixConn:
			pc, err := net.FilePacketConn(socketFile)
			if err != nil {
				return nil, err
			}
			unixSocket.count.Add(1)
			unixSockets[socketKey] = &unixConn{pc.(*net.UnixConn), socketKey, unixSocket.count}
		}

		return unixSockets[socketKey], nil
	}

	// from what I can tell after some quick research, it's quite common for programs to
	// leave their socket file behind after they close, so the typical pattern is to
	// unlink it before you bind to it -- this is often crucial if the last program using
	// it was killed forcefully without a chance to clean up the socket, but there is a
	// race, as the comment in net.UnixListener.close() explains... oh well, I guess?
	if err := syscall.Unlink(addr); err != nil && !errors.Is(err, fs.ErrNotExist) {
		return nil, err
	}

	return nil, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func reuseUnixSocket(network, addr string) (any, error) {
	socketKey := listenerKey(network, addr)

	socket, exists := unixSockets[socketKey]
	if exists {
		// make copy of file descriptor
		socketFile, err := socket.File() // does dup() deep down
		if err != nil {
			return nil, err
		}
		defer socketFile.Close()

		// use copied fd to make new Listener or PacketConn, then replace
		// it in the map so that future copies always come from the most
		// recent fd (as the previous ones will be closed, and we'd get
		// "use of closed network connection" errors) -- note that we
		// preserve the *pointer* to the counter (not just the value) so
		// that all socket wrappers will refer to the same value
		switch unixSocket := socket.(type) {
		case *unixListener:
			ln, err := net.FileListener(socketFile)
			if err != nil {
				return nil, err
			}
			unixSocket.count.Add(1)
			unixSockets[socketKey] = &unixListener{
				UnixListener: ln.(*net.UnixListener),
				mapKey:       socketKey,
				count:        unixSocket.count,
			}

		case *unixConn:
			pc, err := net.FilePacketConn(socketFile)
			if err != nil {
				return nil, err
			}
			unixSocket.count.Add(1)
			unixSockets[socketKey] = &unixConn{
				UnixConn: pc.(*net.UnixConn),
				mapKey:   socketKey,
				count:    unixSocket.count,
			}
		}

		return unixSockets[socketKey], nil
	}
	if isAbstractUnixSocket(addr) {
		return nil, nil
	}

	// from what I can tell after some quick research, it's quite common for programs to
	// leave their socket file behind after they close, so the typical pattern is to
	// unlink it before you bind to it -- this is often crucial if the last program using
	// it was killed forcefully without a chance to clean up the socket, but there is a
	// race, as the comment in net.UnixListener.close() explains... oh well, I guess?
	if err := syscall.Unlink(addr); err != nil && !errors.Is(err, fs.ErrNotExist) {
		return nil, err
	}

	return nil, nil
}
```

### 🔹 函式: `unixConn.Close()`
- **變更前簽章 (Before)**: `func unixConn.Close()` (L250~L268)
- **變更後簽章 (After)**: `func unixConn.Close()` (L268~L288)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (uc *unixConn) Close() error {
	newCount := uc.count.Add(-1)
	if newCount == 0 {
		file, err := uc.File()
		var name string
		if err == nil {
			name = file.Name()
		}
		defer func() {
			unixSocketsMu.Lock()
			delete(unixSockets, uc.mapKey)
			unixSocketsMu.Unlock()
			if err == nil {
				_ = syscall.Unlink(name)
			}
		}()
	}
	return uc.UnixConn.Close()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (uc *unixConn) Close() error {
	if !uc.closed.CompareAndSwap(false, true) {
		return net.ErrClosed
	}
	unixSocketsMu.Lock()
	defer unixSocketsMu.Unlock()

	var name string
	if addr := uc.LocalAddr(); addr != nil {
		name = addr.String()
	}
	newCount := uc.count.Add(-1)
	err := uc.UnixConn.Close()
	if newCount == 0 {
		delete(unixSockets, uc.mapKey)
		if name != "" && !isAbstractUnixSocket(name) {
			_ = syscall.Unlink(name)
		}
	}
	return err
}
```

### 🔹 函式: `unixListener.Close()`
- **變更前簽章 (Before)**: `func unixListener.Close()` (L224~L242)
- **變更後簽章 (After)**: `func unixListener.Close()` (L239~L259)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (uln *unixListener) Close() error {
	newCount := uln.count.Add(-1)
	if newCount == 0 {
		file, err := uln.File()
		var name string
		if err == nil {
			name = file.Name()
		}
		defer func() {
			unixSocketsMu.Lock()
			delete(unixSockets, uln.mapKey)
			unixSocketsMu.Unlock()
			if err == nil {
				_ = syscall.Unlink(name)
			}
		}()
	}
	return uln.UnixListener.Close()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (uln *unixListener) Close() error {
	if !uln.closed.CompareAndSwap(false, true) {
		return net.ErrClosed
	}
	unixSocketsMu.Lock()
	defer unixSocketsMu.Unlock()

	var name string
	if addr := uln.Addr(); addr != nil {
		name = addr.String()
	}
	newCount := uln.count.Add(-1)
	err := uln.UnixListener.Close()
	if newCount == 0 {
		delete(unixSockets, uln.mapKey)
		if name != "" && !isAbstractUnixSocket(name) {
			_ = syscall.Unlink(name)
		}
	}
	return err
}
```


---

### 🔹 Commit #17: `fbc88ae2`
- **完整 Hash**: `fbc88ae2322082b55aef52e0209a0bc56166eca6`
- **說明 (Ground Truth)**: internal: fix `MaxSizeSubjectsListForLog` off-by-one when `maxToDisplay` is `0` (#7970)
- **變更檔案數**: 1

#### 📄 檔案: `internal/logs.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:6, E:5, A:0) ➔ After(N:6, E:5, A:0)
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

### 🔹 函式: `MaxSizeSubjectsListForLog()`
- **變更前簽章 (Before)**: `func MaxSizeSubjectsListForLog(subjects map[string]struct{}, maxToDisplay int)` (L9~L22)
- **變更後簽章 (After)**: `func MaxSizeSubjectsListForLog(subjects map[string]struct{}, maxToDisplay int)` (L9~L22)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func MaxSizeSubjectsListForLog(subjects map[string]struct{}, maxToDisplay int) []string {
	numberOfNamesToDisplay := min(len(subjects), maxToDisplay)
	domainsToDisplay := make([]string, 0, numberOfNamesToDisplay)
	for domain := range subjects {
		domainsToDisplay = append(domainsToDisplay, domain)
		if len(domainsToDisplay) >= numberOfNamesToDisplay {
			break
		}
	}
	if len(subjects) > maxToDisplay {
		domainsToDisplay = append(domainsToDisplay, fmt.Sprintf("(and %d more...)", len(subjects)-maxToDisplay))
	}
	return domainsToDisplay
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func MaxSizeSubjectsListForLog(subjects map[string]struct{}, maxToDisplay int) []string {
	numberOfNamesToDisplay := min(len(subjects), maxToDisplay)
	domainsToDisplay := make([]string, 0, numberOfNamesToDisplay)
	for domain := range subjects {
		if len(domainsToDisplay) >= numberOfNamesToDisplay {
			break
		}
		domainsToDisplay = append(domainsToDisplay, domain)
	}
	if len(subjects) > maxToDisplay {
		domainsToDisplay = append(domainsToDisplay, fmt.Sprintf("(and %d more...)", len(subjects)-maxToDisplay))
	}
	return domainsToDisplay
}
```


---

### 🔹 Commit #18: `54937914`
- **完整 Hash**: `54937914234be0911a9d22a8d1f5560c1ca59fd2`
- **說明 (Ground Truth)**: caddyhttp: fix randString sameCase dictionary to match its docs (#7972)
- **變更檔案數**: 1

#### 📄 檔案: `modules/caddyhttp/errors.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:20, E:15, A:0) ➔ After(N:20, E:15, A:0)
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

### 🔹 函式: `randString()`
- **變更前簽章 (Before)**: `func randString(n int, sameCase bool)` (L90~L104)
- **變更後簽章 (After)**: `func randString(n int, sameCase bool)` (L92~L106)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func randString(n int, sameCase bool) string {
	if n <= 0 {
		return ""
	}
	dict := []byte("abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRTUVWXY23456789")
	if sameCase {
		dict = []byte("abcdefghijkmnpqrstuvwxyz0123456789")
	}
	b := make([]byte, n)
	for i := range b {
		//nolint:gosec
		b[i] = dict[weakrand.IntN(len(dict))]
	}
	return string(b)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func randString(n int, sameCase bool) string {
	if n <= 0 {
		return ""
	}
	dict := []byte("abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRTUVWXY23456789")
	if sameCase {
		dict = []byte("abcdefghijkmnpqrstuvwxyz23456789")
	}
	b := make([]byte, n)
	for i := range b {
		//nolint:gosec
		b[i] = dict[weakrand.IntN(len(dict))]
	}
	return string(b)
}
```


---

### 🔹 Commit #19: `89db4b75`
- **完整 Hash**: `89db4b75c3ba8d6362ba1d51909063cd55481aa2`
- **說明 (Ground Truth)**: reverseproxy: Fix partial response not flushed to clients (#7849)
- **變更檔案數**: 1

#### 📄 檔案: `modules/caddyhttp/reverseproxy/reverseproxy.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:212, E:265, A:0) ➔ After(N:212, E:265, A:0)
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

### 🔹 函式: `Handler.finalizeResponse()`
- **變更前簽章 (Before)**: `func Handler.finalizeResponse(
	rw http.ResponseWriter,
	req *http.Request,
	res *http.Response,
	repl *caddy.Replacer,
	start time.Time,
	logger *zap.Logger,
)` (L1222~L1337)
- **變更後簽章 (After)**: `func Handler.finalizeResponse(
	rw http.ResponseWriter,
	req *http.Request,
	res *http.Response,
	repl *caddy.Replacer,
	start time.Time,
	logger *zap.Logger,
)` (L1222~L1341)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (h *Handler) finalizeResponse(
	rw http.ResponseWriter,
	req *http.Request,
	res *http.Response,
	repl *caddy.Replacer,
	start time.Time,
	logger *zap.Logger,
) error {
	// Strip hop-by-hop headers from the upstream response.
	// For 101 Switching Protocols, save the Upgrade value
	// first (handleUpgradeResponse needs it for validation)
	// and restore it with a canonical Connection header.
	upgradeVal := res.Header.Get("Upgrade")

	removeConnectionHeaders(res.Header)
	for _, h := range hopHeaders {
		res.Header.Del(h)
	}

	if res.StatusCode == http.StatusSwitchingProtocols && upgradeVal != "" {
		res.Header.Set("Upgrade", upgradeVal)
		res.Header.Set("Connection", "Upgrade")
	}

	// deal with 101 Switching Protocols responses: (WebSocket, h2c, etc)
	if res.StatusCode == http.StatusSwitchingProtocols {
		var wg sync.WaitGroup
		h.handleUpgradeResponse(logger, &wg, rw, req, res)
		wg.Wait()
		return nil
	}

	// delete our Server header and use Via instead (see #6275)
	rw.Header().Del("Server")
	var protoPrefix string
	if !strings.HasPrefix(strings.ToUpper(res.Proto), "HTTP/") {
		protoPrefix = res.Proto[:strings.Index(res.Proto, "/")+1]
	}
	rw.Header().Add("Via", protoPrefix+strconv.Itoa(res.ProtoMajor)+"."+strconv.Itoa(res.ProtoMinor)+" Caddy")

	// apply any response header operations
	if h.Headers != nil && h.Headers.Response != nil {
		if h.Headers.Response.Require == nil ||
			h.Headers.Response.Require.Match(res.StatusCode, res.Header) {
			h.Headers.Response.ApplyTo(res.Header, repl)
		}
	}

	copyHeader(rw.Header(), res.Header)

	// The "Trailer" header isn't included in the Transport's response,
	// at least for *http.Transport. Build it up from Trailer.
	announcedTrailers := len(res.Trailer)
	if announcedTrailers > 0 {
		trailerKeys := make([]string, 0, len(res.Trailer))
		for k := range res.Trailer {
			trailerKeys = append(trailerKeys, k)
		}
		rw.Header().Add("Trailer", strings.Join(trailerKeys, ", "))
	}

	rw.WriteHeader(res.StatusCode)
	if h.VerboseLogs {
		logger.Debug("wrote header")
	}

	err := h.copyResponse(rw, res.Body, h.flushInterval(req, res), logger)
	errClose := res.Body.Close() // close now, instead of defer, to populate res.Trailer
	if h.VerboseLogs || errClose != nil {
		if c := logger.Check(zapcore.DebugLevel, "closed response body from upstream"); c != nil {
			c.Write(zap.Error(errClose))
		}
	}
	if err != nil {
		// we're streaming the response and we've already written headers, so
		// there's nothing an error handler can do to recover at this point;
		// we'll just log the error and abort the stream here and panic just as
		// the standard lib's proxy to propagate the stream error.
		// see issue https://github.com/caddyserver/caddy/issues/5951
		if c := logger.Check(zapcore.WarnLevel, "aborting with incomplete response"); c != nil {
			c.Write(zap.Error(err))
		}
		// no extra logging from stdlib
		panic(http.ErrAbortHandler)
	}

	if len(res.Trailer) > 0 {
		// Force chunking if we saw a response trailer.
		// This prevents net/http from calculating the length for short
		// bodies and adding a Content-Length.
		//nolint:bodyclose
		http.NewResponseController(rw).Flush()
	}

	// total duration spent proxying, including writing response body
	repl.Set("http.reverse_proxy.upstream.duration", time.Since(start))
	repl.Set("http.reverse_proxy.upstream.duration_ms", time.Since(start).Seconds()*1e3)

	if len(res.Trailer) == announcedTrailers {
		copyHeader(rw.Header(), res.Trailer)
		return nil
	}

	for k, vv := range res.Trailer {
		k = http.TrailerPrefix + k
		for _, v := range vv {
			rw.Header().Add(k, v)
		}
	}

	if h.VerboseLogs {
		logger.Debug("response finalized")
	}

	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (h *Handler) finalizeResponse(
	rw http.ResponseWriter,
	req *http.Request,
	res *http.Response,
	repl *caddy.Replacer,
	start time.Time,
	logger *zap.Logger,
) error {
	// Strip hop-by-hop headers from the upstream response.
	// For 101 Switching Protocols, save the Upgrade value
	// first (handleUpgradeResponse needs it for validation)
	// and restore it with a canonical Connection header.
	upgradeVal := res.Header.Get("Upgrade")

	removeConnectionHeaders(res.Header)
	for _, h := range hopHeaders {
		res.Header.Del(h)
	}

	if res.StatusCode == http.StatusSwitchingProtocols && upgradeVal != "" {
		res.Header.Set("Upgrade", upgradeVal)
		res.Header.Set("Connection", "Upgrade")
	}

	// deal with 101 Switching Protocols responses: (WebSocket, h2c, etc)
	if res.StatusCode == http.StatusSwitchingProtocols {
		var wg sync.WaitGroup
		h.handleUpgradeResponse(logger, &wg, rw, req, res)
		wg.Wait()
		return nil
	}

	// delete our Server header and use Via instead (see #6275)
	rw.Header().Del("Server")
	var protoPrefix string
	if !strings.HasPrefix(strings.ToUpper(res.Proto), "HTTP/") {
		protoPrefix = res.Proto[:strings.Index(res.Proto, "/")+1]
	}
	rw.Header().Add("Via", protoPrefix+strconv.Itoa(res.ProtoMajor)+"."+strconv.Itoa(res.ProtoMinor)+" Caddy")

	// apply any response header operations
	if h.Headers != nil && h.Headers.Response != nil {
		if h.Headers.Response.Require == nil ||
			h.Headers.Response.Require.Match(res.StatusCode, res.Header) {
			h.Headers.Response.ApplyTo(res.Header, repl)
		}
	}

	copyHeader(rw.Header(), res.Header)

	// The "Trailer" header isn't included in the Transport's response,
	// at least for *http.Transport. Build it up from Trailer.
	announcedTrailers := len(res.Trailer)
	if announcedTrailers > 0 {
		trailerKeys := make([]string, 0, len(res.Trailer))
		for k := range res.Trailer {
			trailerKeys = append(trailerKeys, k)
		}
		rw.Header().Add("Trailer", strings.Join(trailerKeys, ", "))
	}

	rw.WriteHeader(res.StatusCode)
	if h.VerboseLogs {
		logger.Debug("wrote header")
	}

	err := h.copyResponse(rw, res.Body, h.flushInterval(req, res), logger)
	errClose := res.Body.Close() // close now, instead of defer, to populate res.Trailer
	if h.VerboseLogs || errClose != nil {
		if c := logger.Check(zapcore.DebugLevel, "closed response body from upstream"); c != nil {
			c.Write(zap.Error(errClose))
		}
	}
	if err != nil {
		// we're streaming the response and we've already written headers, so
		// there's nothing an error handler can do to recover at this point;
		// we'll just log the error and abort the stream here and panic just as
		// the standard lib's proxy to propagate the stream error.
		// see issue https://github.com/caddyserver/caddy/issues/5951
		if c := logger.Check(zapcore.WarnLevel, "aborting with incomplete response"); c != nil {
			c.Write(zap.Error(err))
		}
		// flush the buffer to ensure the client sees the partial response
		// see: https://github.com/caddyserver/caddy/issues/7845
		//nolint:bodyclose
		http.NewResponseController(rw).Flush()
		// no extra logging from stdlib
		panic(http.ErrAbortHandler)
	}

	if len(res.Trailer) > 0 {
		// Force chunking if we saw a response trailer.
		// This prevents net/http from calculating the length for short
		// bodies and adding a Content-Length.
		//nolint:bodyclose
		http.NewResponseController(rw).Flush()
	}

	// total duration spent proxying, including writing response body
	repl.Set("http.reverse_proxy.upstream.duration", time.Since(start))
	repl.Set("http.reverse_proxy.upstream.duration_ms", time.Since(start).Seconds()*1e3)

	if len(res.Trailer) == announcedTrailers {
		copyHeader(rw.Header(), res.Trailer)
		return nil
	}

	for k, vv := range res.Trailer {
		k = http.TrailerPrefix + k
		for _, v := range vv {
			rw.Header().Add(k, v)
		}
	}

	if h.VerboseLogs {
		logger.Debug("response finalized")
	}

	return nil
}
```


---

### 🔹 Commit #20: `7e82a6b5`
- **完整 Hash**: `7e82a6b5281480f464d00d680ffb5573cf2d34a3`
- **說明 (Ground Truth)**: admin: fix warnings and status code in /load API (#7267)
- **變更檔案數**: 4

#### 📄 檔案: `admin.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:192, E:236, A:0) ➔ After(N:192, E:236, A:0)
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

#### 📄 檔案: `caddyconfig/configadapters.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:19, E:14, A:0) ➔ After(N:17, E:13, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 2, +Edges: 0, -Edges: 1, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `directive` (MODULE_STATE)
  • - [移除節點] `Warning.String` (FUNCTION_DEF)
  • - [移除呼叫邊] `Warning.String` ──[CALLS]──> `fmt.Sprintf (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `caddyconfig/load.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:36, E:39, A:0) ➔ After(N:33, E:37, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 4, +Edges: 2, -Edges: 4, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `warnings` (MODULE_STATE)
  • - [移除節點] `w.Write (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `err.Error (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `json.Marshal (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `caddy.Log().Named("admin.api.load").Error (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `adminLoad.handleLoad` ──[CALLS]──> `json.NewEncoder(w).Encode (External/Pkg)`
  • + [新增呼叫邊] `adminLoad.handleLoad` ──[CALLS]──> `json.NewEncoder (External/Pkg)`
  • - [移除呼叫邊] `adminLoad.handleLoad` ──[CALLS]──> `json.Marshal (External/Pkg)`
  • - [移除呼叫邊] `adminLoad.handleLoad` ──[CALLS]──> `caddy.Log().Named("admin.api.load").Error (External/Pkg)`
  • - [移除呼叫邊] `adminLoad.handleLoad` ──[CALLS]──> `err.Error (External/Pkg)`
  • - [移除呼叫邊] `adminLoad.handleLoad` ──[CALLS]──> `w.Write (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `adminLoad.handleLoad()`
- **變更前簽章 (Before)**: `func adminLoad.handleLoad(w http.ResponseWriter, r *http.Request)` (L73~L134)
- **變更後簽章 (After)**: `func adminLoad.handleLoad(w http.ResponseWriter, r *http.Request)` (L73~L141)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (adminLoad) handleLoad(w http.ResponseWriter, r *http.Request) error {
	if r.Method != http.MethodPost {
		return caddy.APIError{
			HTTPStatus: http.StatusMethodNotAllowed,
			Err:        fmt.Errorf("method not allowed"),
		}
	}

	buf := bufPool.Get().(*bytes.Buffer)
	buf.Reset()
	defer bufPool.Put(buf)

	_, err := io.Copy(buf, r.Body)
	if err != nil {
		return caddy.APIError{
			HTTPStatus: http.StatusBadRequest,
			Err:        fmt.Errorf("reading request body: %v", err),
		}
	}
	body := buf.Bytes()

	// if the config is formatted other than Caddy's native
	// JSON, we need to adapt it before loading it
	if ctHeader := r.Header.Get("Content-Type"); ctHeader != "" {
		result, warnings, err := adaptByContentType(ctHeader, body)
		if err != nil {
			return caddy.APIError{
				HTTPStatus: http.StatusBadRequest,
				Err:        err,
			}
		}
		if len(warnings) > 0 {
			respBody, err := json.Marshal(warnings)
			if err != nil {
				caddy.Log().Named("admin.api.load").Error(err.Error())
			}
			_, _ = w.Write(respBody) //nolint:gosec // false positive: no XSS here
		}
		body = result
	}

	forceReload := r.Header.Get("Cache-Control") == "must-revalidate"

	err = caddy.Load(body, forceReload)
	if err != nil {
		return caddy.APIError{
			HTTPStatus: http.StatusBadRequest,
			Err:        fmt.Errorf("loading config: %v", err),
		}
	}

	// If this request changed the config, clear the last
	// config info we have stored, if it is different from
	// the original source.
	caddy.ClearLastConfigIfDifferent(
		r.Header.Get("Caddy-Config-Source-File"),
		r.Header.Get("Caddy-Config-Source-Adapter"))

	caddy.Log().Named("admin.api").Info("load complete")

	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (adminLoad) handleLoad(w http.ResponseWriter, r *http.Request) error {
	if r.Method != http.MethodPost {
		return caddy.APIError{
			HTTPStatus: http.StatusMethodNotAllowed,
			Err:        fmt.Errorf("method not allowed"),
		}
	}

	buf := bufPool.Get().(*bytes.Buffer)
	buf.Reset()
	defer bufPool.Put(buf)

	_, err := io.Copy(buf, r.Body)
	if err != nil {
		return caddy.APIError{
			HTTPStatus: http.StatusBadRequest,
			Err:        fmt.Errorf("reading request body: %v", err),
		}
	}
	body := buf.Bytes()

	var warnings []Warning
	// if the config is formatted other than Caddy's native
	// JSON, we need to adapt it before loading it
	if ctHeader := r.Header.Get("Content-Type"); ctHeader != "" {
		result, wns, err := adaptByContentType(ctHeader, body)
		if err != nil {
			return caddy.APIError{
				HTTPStatus: http.StatusBadRequest,
				Err:        err,
				Warnings:   wns,
			}
		}
		warnings = wns
		body = result
	}

	forceReload := r.Header.Get("Cache-Control") == "must-revalidate"

	err = caddy.Load(body, forceReload)
	if err != nil {
		return caddy.APIError{
			HTTPStatus: http.StatusBadRequest,
			Err:        fmt.Errorf("loading config: %v", err),
			Warnings:   warnings,
		}
	}

	// If this request changed the config, clear the last
	// config info we have stored, if it is different from
	// the original source.
	caddy.ClearLastConfigIfDifferent(
		r.Header.Get("Caddy-Config-Source-File"),
		r.Header.Get("Caddy-Config-Source-Adapter"))

	caddy.Log().Named("admin.api").Info("load complete")

	// Send any warnings back even if there were no errors
	if len(warnings) > 0 {
		out := struct {
			Warnings []Warning `json:"warnings"`
		}{
			Warnings: warnings,
		}
		return json.NewEncoder(w).Encode(out)
	}

	return nil
}
```


#### 📄 檔案: `caddyconfig/warning/warning.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:3, E:1, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `fmt.Sprintf (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `Warning.String` (FUNCTION_DEF)
  • + [新增節點] `directive` (MODULE_STATE)
  • + [新增呼叫邊] `Warning.String` ──[CALLS]──> `fmt.Sprintf (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/caddy show 612128e3b0f290af44649d7a7dcb1111fc3ebb33
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 612128e3b0f290af44649d7a7dcb1111fc3ebb33~1 --file test_repos/caddy/modules/logging/filters.go
   ```
