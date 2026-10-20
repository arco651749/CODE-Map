# 🔬 CODE-Map 基準審查獨立驗證報告: `go-redis`
> **技術生態**: `Go (高性能連線池 / Pipeline / 超時控制)`  
> **本地倉庫路徑**: `test_repos/go-redis`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 29 Files  
> **報告生成時間**: 2026-10-20 21:42:55  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `15` / `29` | `51.7%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `10` / `29` | `34.5%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `4` / `29` | `13.8%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`25` / `29`** | **`86.2%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `29` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `3f37a3a4`
- **完整 Hash**: `3f37a3a4e4a1a20259c7db87d77075cdc83c069a`
- **說明 (Ground Truth)**: fix(cmd): accept RESP3 doubles and big numbers (#4138)
- **變更檔案數**: 1

#### 📄 檔案: `command.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:829, E:1115, A:0) ➔ After(N:839, E:1146, A:0)
- **差分統計**: +Nodes: 10, -Nodes: 0, +Edges: 31, -Edges: 0, ΔFuncs: 7, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `math.IsNaN (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `formatDouble` (FUNCTION_DEF)
  • + [新增節點] `internal.FormatFloat (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `math.Abs (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `strconv.Itoa (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `strconv.FormatInt (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `strings.Trim (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `strings.Replace (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `max (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `math.Trunc (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `toString` ──[CALLS]──> `formatDouble`
  • + [新增呼叫邊] `toString` ──[CALLS]──> `AREntrySliceCmd.String`
  • + [新增呼叫邊] `formatDouble` ──[CALLS]──> `math.IsNaN (External/Pkg)`
  • + [新增呼叫邊] `formatDouble` ──[CALLS]──> `math.IsInf (External/Pkg)`
  • + [新增呼叫邊] `formatDouble` ──[CALLS]──> `internal.FormatFloat (External/Pkg)`
  • _... 以及其餘 26 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Cmd.Int()`
- **變更前簽章 (Before)**: `func Cmd.Int()` (L745~L759)
- **變更後簽章 (After)**: `func Cmd.Int()` (L780~L798)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (cmd *Cmd) Int() (int, error) {
	cmd.await()
	if cmd.err != nil {
		return 0, cmd.err
	}
	switch val := cmd.val.(type) {
	case int64:
		return int(val), nil
	case string:
		return strconv.Atoi(val)
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Int", val)
		return 0, err
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (cmd *Cmd) Int() (int, error) {
	cmd.await()
	if cmd.err != nil {
		return 0, cmd.err
	}
	switch val := cmd.val.(type) {
	case int64:
		return int(val), nil
	case string:
		return strconv.Atoi(val)
	case float64:
		return strconv.Atoi(formatDouble(val))
	case *big.Int:
		return strconv.Atoi(val.String())
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Int", val)
		return 0, err
	}
}
```

### 🔹 函式: `toFloat64()`
- **變更前簽章 (Before)**: `func toFloat64(val interface{})` (L844~L856)
- **變更後簽章 (After)**: `func toFloat64(val interface{})` (L893~L907)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func toFloat64(val interface{}) (float64, error) {
	switch val := val.(type) {
	case float64:
		return val, nil
	case int64:
		return float64(val), nil
	case string:
		return strconv.ParseFloat(val, 64)
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Float64", val)
		return 0, err
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func toFloat64(val interface{}) (float64, error) {
	switch val := val.(type) {
	case float64:
		return val, nil
	case int64:
		return float64(val), nil
	case string:
		return strconv.ParseFloat(val, 64)
	case *big.Int:
		return toFloat64(val.String())
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Float64", val)
		return 0, err
	}
}
```

### 🔹 函式: `toFloat32()`
- **變更前簽章 (Before)**: `func toFloat32(val interface{})` (L809~L834)
- **變更後簽章 (After)**: `func toFloat32(val interface{})` (L856~L883)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func toFloat32(val interface{}) (float32, error) {
	switch val := val.(type) {
	case float64:
		// Return the range error that ParseFloat returns for a RESP2 bulk
		// string when a RESP3 double does not fit in a float32.
		if f := float32(val); math.IsInf(float64(f), 0) && !math.IsInf(val, 0) {
			return 0, &strconv.NumError{
				Func: "ParseFloat",
				Num:  strconv.FormatFloat(val, 'g', -1, 64),
				Err:  strconv.ErrRange,
			}
		}
		return float32(val), nil
	case int64:
		return float32(val), nil
	case string:
		f, err := strconv.ParseFloat(val, 32)
		if err != nil {
			return 0, err
		}
		return float32(f), nil
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Float32", val)
		return 0, err
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func toFloat32(val interface{}) (float32, error) {
	switch val := val.(type) {
	case float64:
		// Return the range error that ParseFloat returns for a RESP2 bulk
		// string when a RESP3 double does not fit in a float32.
		if f := float32(val); math.IsInf(float64(f), 0) && !math.IsInf(val, 0) {
			return 0, &strconv.NumError{
				Func: "ParseFloat",
				Num:  strconv.FormatFloat(val, 'g', -1, 64),
				Err:  strconv.ErrRange,
			}
		}
		return float32(val), nil
	case int64:
		return float32(val), nil
	case string:
		f, err := strconv.ParseFloat(val, 32)
		if err != nil {
			return 0, err
		}
		return float32(f), nil
	case *big.Int:
		return toFloat32(val.String())
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Float32", val)
		return 0, err
	}
}
```

### 🔹 函式: `toInt64()`
- **變更前簽章 (Before)**: `func toInt64(val interface{})` (L769~L779)
- **變更後簽章 (After)**: `func toInt64(val interface{})` (L808~L822)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func toInt64(val interface{}) (int64, error) {
	switch val := val.(type) {
	case int64:
		return val, nil
	case string:
		return strconv.ParseInt(val, 10, 64)
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Int64", val)
		return 0, err
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func toInt64(val interface{}) (int64, error) {
	switch val := val.(type) {
	case int64:
		return val, nil
	case string:
		return strconv.ParseInt(val, 10, 64)
	case float64:
		return toInt64(formatDouble(val))
	case *big.Int:
		return toInt64(val.String())
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Int64", val)
		return 0, err
	}
}
```

### 🔹 函式: `toUint64()`
- **變更前簽章 (Before)**: `func toUint64(val interface{})` (L789~L799)
- **變更後簽章 (After)**: `func toUint64(val interface{})` (L832~L846)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func toUint64(val interface{}) (uint64, error) {
	switch val := val.(type) {
	case int64:
		return uint64(val), nil
	case string:
		return strconv.ParseUint(val, 10, 64)
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Uint64", val)
		return 0, err
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func toUint64(val interface{}) (uint64, error) {
	switch val := val.(type) {
	case int64:
		return uint64(val), nil
	case string:
		return strconv.ParseUint(val, 10, 64)
	case float64:
		return toUint64(formatDouble(val))
	case *big.Int:
		return toUint64(val.String())
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Uint64", val)
		return 0, err
	}
}
```

### 🔹 函式: `toString()`
- **變更前簽章 (Before)**: `func toString(val interface{})` (L735~L743)
- **變更後簽章 (After)**: `func toString(val interface{})` (L736~L748)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func toString(val interface{}) (string, error) {
	switch val := val.(type) {
	case string:
		return val, nil
	default:
		err := fmt.Errorf("redis: unexpected type=%T for String", val)
		return "", err
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func toString(val interface{}) (string, error) {
	switch val := val.(type) {
	case string:
		return val, nil
	case float64:
		return formatDouble(val), nil
	case *big.Int:
		return val.String(), nil
	default:
		err := fmt.Errorf("redis: unexpected type=%T for String", val)
		return "", err
	}
}
```

### 🔹 函式: `toBool()`
- **變更前簽章 (Before)**: `func toBool(val interface{})` (L866~L878)
- **變更後簽章 (After)**: `func toBool(val interface{})` (L917~L933)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func toBool(val interface{}) (bool, error) {
	switch val := val.(type) {
	case bool:
		return val, nil
	case int64:
		return val != 0, nil
	case string:
		return strconv.ParseBool(val)
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Bool", val)
		return false, err
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func toBool(val interface{}) (bool, error) {
	switch val := val.(type) {
	case bool:
		return val, nil
	case int64:
		return val != 0, nil
	case string:
		return strconv.ParseBool(val)
	case float64:
		return strconv.ParseBool(formatDouble(val))
	case *big.Int:
		return strconv.ParseBool(val.String())
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Bool", val)
		return false, err
	}
}
```


---

### 🔹 Commit #02: `864a5f87`
- **完整 Hash**: `864a5f87f17415010938379b671751c706cd1964`
- **說明 (Ground Truth)**: fix(proto): reject uint overflow on 32-bit (#4081)
- **變更檔案數**: 1

#### 📄 檔案: `internal/proto/scan.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:47, E:45, A:0) ➔ After(N:47, E:45, A:0)
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

### 🔹 函式: `Scan()`
- **變更前簽章 (Before)**: `func Scan(b []byte, v any)` (L16~L133)
- **變更後簽章 (After)**: `func Scan(b []byte, v any)` (L16~L133)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func Scan(b []byte, v any) error {
	switch v := v.(type) {
	case nil:
		return fmt.Errorf("redis: Scan(nil)")
	case *string:
		*v = util.BytesToString(b)
		return nil
	case *[]byte:
		dest := make([]byte, len(b))
		copy(dest, b)
		*v = dest
		return nil
	case *int:
		var err error
		*v, err = util.Atoi(b)
		return err
	case *int8:
		n, err := util.ParseInt(b, 10, 8)
		if err != nil {
			return err
		}
		*v = int8(n)
		return nil
	case *int16:
		n, err := util.ParseInt(b, 10, 16)
		if err != nil {
			return err
		}
		*v = int16(n)
		return nil
	case *int32:
		n, err := util.ParseInt(b, 10, 32)
		if err != nil {
			return err
		}
		*v = int32(n)
		return nil
	case *int64:
		n, err := util.ParseInt(b, 10, 64)
		if err != nil {
			return err
		}
		*v = n
		return nil
	case *uint:
		n, err := util.ParseUint(b, 10, 64)
		if err != nil {
			return err
		}
		*v = uint(n)
		return nil
	case *uint8:
		n, err := util.ParseUint(b, 10, 8)
		if err != nil {
			return err
		}
		*v = uint8(n)
		return nil
	case *uint16:
		n, err := util.ParseUint(b, 10, 16)
		if err != nil {
			return err
		}
		*v = uint16(n)
		return nil
	case *uint32:
		n, err := util.ParseUint(b, 10, 32)
		if err != nil {
			return err
		}
		*v = uint32(n)
		return nil
	case *uint64:
		n, err := util.ParseUint(b, 10, 64)
		if err != nil {
			return err
		}
		*v = n
		return nil
	case *float32:
		n, err := util.ParseFloat(b, 32)
		if err != nil {
			return err
		}
		*v = float32(n)
		return err
	case *float64:
		var err error
		*v, err = util.ParseFloat(b, 64)
		return err
	case *bool:
		*v = len(b) == 1 && b[0] == '1'
		return nil
	case *time.Time:
		var err error
		*v, err = time.Parse(time.RFC3339Nano, util.BytesToString(b))
		return err
	case *time.Duration:
		n, err := util.ParseInt(b, 10, 64)
		if err != nil {
			return err
		}
		*v = time.Duration(n)
		return nil
	case encoding.BinaryUnmarshaler:
		dest := make([]byte, len(b))
		copy(dest, b)
		return v.UnmarshalBinary(dest)
	case *net.IP:
		dest := make(net.IP, len(b))
		copy(dest, b)
		*v = dest
		return nil
	default:
		return fmt.Errorf(
			"redis: can't unmarshal %T (consider implementing BinaryUnmarshaler)", v)
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func Scan(b []byte, v any) error {
	switch v := v.(type) {
	case nil:
		return fmt.Errorf("redis: Scan(nil)")
	case *string:
		*v = util.BytesToString(b)
		return nil
	case *[]byte:
		dest := make([]byte, len(b))
		copy(dest, b)
		*v = dest
		return nil
	case *int:
		var err error
		*v, err = util.Atoi(b)
		return err
	case *int8:
		n, err := util.ParseInt(b, 10, 8)
		if err != nil {
			return err
		}
		*v = int8(n)
		return nil
	case *int16:
		n, err := util.ParseInt(b, 10, 16)
		if err != nil {
			return err
		}
		*v = int16(n)
		return nil
	case *int32:
		n, err := util.ParseInt(b, 10, 32)
		if err != nil {
			return err
		}
		*v = int32(n)
		return nil
	case *int64:
		n, err := util.ParseInt(b, 10, 64)
		if err != nil {
			return err
		}
		*v = n
		return nil
	case *uint:
		n, err := util.ParseUint(b, 10, 0)
		if err != nil {
			return err
		}
		*v = uint(n)
		return nil
	case *uint8:
		n, err := util.ParseUint(b, 10, 8)
		if err != nil {
			return err
		}
		*v = uint8(n)
		return nil
	case *uint16:
		n, err := util.ParseUint(b, 10, 16)
		if err != nil {
			return err
		}
		*v = uint16(n)
		return nil
	case *uint32:
		n, err := util.ParseUint(b, 10, 32)
		if err != nil {
			return err
		}
		*v = uint32(n)
		return nil
	case *uint64:
		n, err := util.ParseUint(b, 10, 64)
		if err != nil {
			return err
		}
		*v = n
		return nil
	case *float32:
		n, err := util.ParseFloat(b, 32)
		if err != nil {
			return err
		}
		*v = float32(n)
		return err
	case *float64:
		var err error
		*v, err = util.ParseFloat(b, 64)
		return err
	case *bool:
		*v = len(b) == 1 && b[0] == '1'
		return nil
	case *time.Time:
		var err error
		*v, err = time.Parse(time.RFC3339Nano, util.BytesToString(b))
		return err
	case *time.Duration:
		n, err := util.ParseInt(b, 10, 64)
		if err != nil {
			return err
		}
		*v = time.Duration(n)
		return nil
	case encoding.BinaryUnmarshaler:
		dest := make([]byte, len(b))
		copy(dest, b)
		return v.UnmarshalBinary(dest)
	case *net.IP:
		dest := make(net.IP, len(b))
		copy(dest, b)
		*v = dest
		return nil
	default:
		return fmt.Errorf(
			"redis: can't unmarshal %T (consider implementing BinaryUnmarshaler)", v)
	}
}
```


---

### 🔹 Commit #03: `cfbdbccf`
- **完整 Hash**: `cfbdbccf3568495a2d175f8835bddb49273d9762`
- **說明 (Ground Truth)**: fix(sentinel): bound failover dials by DialTimeout (#4067)
- **變更檔案數**: 1

#### 📄 檔案: `sentinel.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:157, E:229, A:0) ➔ After(N:157, E:229, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
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

### 🔹 函式: `NewFailoverClient()`
- **變更前簽章 (Before)**: `func NewFailoverClient(failoverOpt *FailoverOptions)` (L567~L701)
- **變更後簽章 (After)**: `func NewFailoverClient(failoverOpt *FailoverOptions)` (L567~L701)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func NewFailoverClient(failoverOpt *FailoverOptions) *Client {
	if failoverOpt == nil {
		panic("redis: NewFailoverClient nil options")
	}

	if failoverOpt.RouteByLatency {
		panic("to route commands by latency, use NewFailoverClusterClient")
	}
	if failoverOpt.RouteRandomly {
		panic("to route commands randomly, use NewFailoverClusterClient")
	}

	sentinelAddrs := make([]string, len(failoverOpt.SentinelAddrs))
	copy(sentinelAddrs, failoverOpt.SentinelAddrs)

	rand.Shuffle(len(sentinelAddrs), func(i, j int) {
		sentinelAddrs[i], sentinelAddrs[j] = sentinelAddrs[j], sentinelAddrs[i]
	})

	failover := &sentinelFailover{
		opt:           failoverOpt,
		sentinelAddrs: sentinelAddrs,
	}

	opt := failoverOpt.clientOptions()
	opt.Dialer = masterReplicaDialer(failover)
	opt.init()

	rdb := &Client{
		baseClient: &baseClient{
			apClosed: &atomic.Bool{},
			opt:      opt,
			onClose:  &onCloseHooks{},
			himport:  newHImportRegistry(),
		},
	}
	rdb.init()

	// Registered first (at construction), so onClose.run's LIFO order invokes it LAST —
	// after any lazily-registered autopipeliner drain hook. The drain needs MasterAddr
	// (hence a live failover client) to dial a replacement conn for accepted-but-unsent
	// work; tearing the failover client down here first would make MasterAddr return
	// pool.ErrClosed and fail those replayable commands. See onCloseHooks.run.
	//
	// Registered BEFORE the pools exist, not after: with MinIdleConns > 0 the main
	// pool starts dialing as soon as it is created, and masterReplicaDialer then
	// builds the failover's Sentinel client and pubsub. If a later construction
	// step panics, the panic-cleanup defer below closes rdb, whose onClose hooks
	// must already include this one — otherwise those discovery resources outlive
	// the client nobody will ever hold (Copilot on #4002).
	rdb.onClose.register(onCloseHookIDSentinelFailover, failover.Close)

	// Close a partially-built client if any construction step below panics before
	// this constructor returns. Mirrors NewClient: the pools (and their MinIdleConns
	// dialing goroutines) are created below, and a later step can panic — a pipeline
	// pool whose PipelinePoolSize overflows int32, otel registration, or a push
	// processor rejecting handler registration. The panic propagates to the caller
	// (which may recover it), but rdb is never returned, so without this its pools
	// would leak with no reference left to Close them. Close is nil-safe for a
	// partially-built client and this defer does not recover, so the panic still
	// surfaces.
	built := false
	defer func() {
		if !built {
			_ = rdb.Close()
		}
	}()

	// Initialize push notification processor using shared helper
	// Use void processor by default for RESP2 connections
	rdb.pushProcessor = initializePushProcessor(opt)

	// Generate unique pool names for metrics
	uniqueID := generateUniqueID()
	mainPoolName := opt.Addr + "_" + uniqueID
	pubsubPoolName := opt.Addr + "_" + uniqueID + "_pubsub"

	// Assign the pool fields only AFTER the error check, mirroring NewClient.
	// newConnPool returns a nil *pool.ConnPool on error, and assigning that
	// straight to the pool.Pooler interface field would leave a typed-nil
	// interface that closeResources treats as present (its != nil check passes),
	// so the panic-cleanup defer above would nil-deref inside ConnPool.Close and
	// replace the intended "failed to create connection pool" panic. A local var
	// keeps the field nil on failure. (pubSubPool is a concrete *pool.PubSubPool
	// whose nil is caught correctly by the != nil check, but assign it the same
	// way to keep this constructor identical to NewClient.)
	connPool, err := newConnPool(opt, rdb.dialHook, mainPoolName)
	if err != nil {
		panic(fmt.Errorf("redis: failed to create connection pool: %w", err))
	}
	rdb.connPool = connPool
	pubSubPool, err := newPubSubPool(opt, rdb.dialHook, pubsubPoolName)
	if err != nil {
		panic(fmt.Errorf("redis: failed to create pubsub pool: %w", err))
	}
	rdb.pubSubPool = pubSubPool

	// Create the dedicated pipeline pool unconditionally, mirroring NewClient
	// via the shared buildPipelinePool helper. PipelinePoolSize < 0 opts out.
	if opt.PipelinePoolSize >= 0 {
		ref, err := rdb.buildPipelinePool(mainPoolName + "_pipeline")
		if err != nil {
			panic(fmt.Errorf("redis: failed to create pipeline connection pool: %w", err))
		}
		rdb.pipelinePool = ref
	}

	// Register pools for OTel async gauge metrics, matching NewClient (the
	// failover client previously registered none, so pool gauges were silent
	// for the identical standalone setup). The pipeline pool is nil when not
	// configured.
	otel.RegisterPools(rdb.connPool, rdb.pubSubPool, rdb.getPipelinePool(), opt.Addr)

	failover.mu.Lock()
	failover.onFailover = func(ctx context.Context, addr string) {
		if connPool, ok := rdb.connPool.(*pool.ConnPool); ok {
			_ = connPool.Filter(func(cn *pool.Conn) bool {
				return cn.RemoteAddr().String() != addr
			})
		}
		// Drop stale pipeline-pool connections dialed to the demoted master too;
		// otherwise pipelined traffic keeps using the old address after failover.
		// The pipeline pool is created at construction (before this callback can
		// fire), so the ref is simply read here.
		if ref := rdb.loadPipelinePool(); ref != nil {
			_ = ref.pool.Filter(func(cn *pool.Conn) bool {
				return cn.RemoteAddr().String() != addr
			})
		}
	}
	failover.mu.Unlock()

	built = true
	return rdb
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func NewFailoverClient(failoverOpt *FailoverOptions) *Client {
	if failoverOpt == nil {
		panic("redis: NewFailoverClient nil options")
	}

	if failoverOpt.RouteByLatency {
		panic("to route commands by latency, use NewFailoverClusterClient")
	}
	if failoverOpt.RouteRandomly {
		panic("to route commands randomly, use NewFailoverClusterClient")
	}

	sentinelAddrs := make([]string, len(failoverOpt.SentinelAddrs))
	copy(sentinelAddrs, failoverOpt.SentinelAddrs)

	rand.Shuffle(len(sentinelAddrs), func(i, j int) {
		sentinelAddrs[i], sentinelAddrs[j] = sentinelAddrs[j], sentinelAddrs[i]
	})

	failover := &sentinelFailover{
		opt:           failoverOpt,
		sentinelAddrs: sentinelAddrs,
	}

	opt := failoverOpt.clientOptions()
	opt.Dialer = masterReplicaDialer(failover, opt)
	opt.init()

	rdb := &Client{
		baseClient: &baseClient{
			apClosed: &atomic.Bool{},
			opt:      opt,
			onClose:  &onCloseHooks{},
			himport:  newHImportRegistry(),
		},
	}
	rdb.init()

	// Registered first (at construction), so onClose.run's LIFO order invokes it LAST —
	// after any lazily-registered autopipeliner drain hook. The drain needs MasterAddr
	// (hence a live failover client) to dial a replacement conn for accepted-but-unsent
	// work; tearing the failover client down here first would make MasterAddr return
	// pool.ErrClosed and fail those replayable commands. See onCloseHooks.run.
	//
	// Registered BEFORE the pools exist, not after: with MinIdleConns > 0 the main
	// pool starts dialing as soon as it is created, and masterReplicaDialer then
	// builds the failover's Sentinel client and pubsub. If a later construction
	// step panics, the panic-cleanup defer below closes rdb, whose onClose hooks
	// must already include this one — otherwise those discovery resources outlive
	// the client nobody will ever hold (Copilot on #4002).
	rdb.onClose.register(onCloseHookIDSentinelFailover, failover.Close)

	// Close a partially-built client if any construction step below panics before
	// this constructor returns. Mirrors NewClient: the pools (and their MinIdleConns
	// dialing goroutines) are created below, and a later step can panic — a pipeline
	// pool whose PipelinePoolSize overflows int32, otel registration, or a push
	// processor rejecting handler registration. The panic propagates to the caller
	// (which may recover it), but rdb is never returned, so without this its pools
	// would leak with no reference left to Close them. Close is nil-safe for a
	// partially-built client and this defer does not recover, so the panic still
	// surfaces.
	built := false
	defer func() {
		if !built {
			_ = rdb.Close()
		}
	}()

	// Initialize push notification processor using shared helper
	// Use void processor by default for RESP2 connections
	rdb.pushProcessor = initializePushProcessor(opt)

	// Generate unique pool names for metrics
	uniqueID := generateUniqueID()
	mainPoolName := opt.Addr + "_" + uniqueID
	pubsubPoolName := opt.Addr + "_" + uniqueID + "_pubsub"

	// Assign the pool fields only AFTER the error check, mirroring NewClient.
	// newConnPool returns a nil *pool.ConnPool on error, and assigning that
	// straight to the pool.Pooler interface field would leave a typed-nil
	// interface that closeResources treats as present (its != nil check passes),
	// so the panic-cleanup defer above would nil-deref inside ConnPool.Close and
	// replace the intended "failed to create connection pool" panic. A local var
	// keeps the field nil on failure. (pubSubPool is a concrete *pool.PubSubPool
	// whose nil is caught correctly by the != nil check, but assign it the same
	// way to keep this constructor identical to NewClient.)
	connPool, err := newConnPool(opt, rdb.dialHook, mainPoolName)
	if err != nil {
		panic(fmt.Errorf("redis: failed to create connection pool: %w", err))
	}
	rdb.connPool = connPool
	pubSubPool, err := newPubSubPool(opt, rdb.dialHook, pubsubPoolName)
	if err != nil {
		panic(fmt.Errorf("redis: failed to create pubsub pool: %w", err))
	}
	rdb.pubSubPool = pubSubPool

	// Create the dedicated pipeline pool unconditionally, mirroring NewClient
	// via the shared buildPipelinePool helper. PipelinePoolSize < 0 opts out.
	if opt.PipelinePoolSize >= 0 {
		ref, err := rdb.buildPipelinePool(mainPoolName + "_pipeline")
		if err != nil {
			panic(fmt.Errorf("redis: failed to create pipeline connection pool: %w", err))
		}
		rdb.pipelinePool = ref
	}

	// Register pools for OTel async gauge metrics, matching NewClient (the
	// failover client previously registered none, so pool gauges were silent
	// for the identical standalone setup). The pipeline pool is nil when not
	// configured.
	otel.RegisterPools(rdb.connPool, rdb.pubSubPool, rdb.getPipelinePool(), opt.Addr)

	failover.mu.Lock()
	failover.onFailover = func(ctx context.Context, addr string) {
		if connPool, ok := rdb.connPool.(*pool.ConnPool); ok {
			_ = connPool.Filter(func(cn *pool.Conn) bool {
				return cn.RemoteAddr().String() != addr
			})
		}
		// Drop stale pipeline-pool connections dialed to the demoted master too;
		// otherwise pipelined traffic keeps using the old address after failover.
		// The pipeline pool is created at construction (before this callback can
		// fire), so the ref is simply read here.
		if ref := rdb.loadPipelinePool(); ref != nil {
			_ = ref.pool.Filter(func(cn *pool.Conn) bool {
				return cn.RemoteAddr().String() != addr
			})
		}
	}
	failover.mu.Unlock()

	built = true
	return rdb
}
```

### 🔹 函式: `masterReplicaDialer()`
- **變更前簽章 (Before)**: `func masterReplicaDialer(
	failover *sentinelFailover,
)` (L703~L734)
- **變更後簽章 (After)**: `func masterReplicaDialer(
	failover *sentinelFailover,
	opt *Options,
)` (L703~L735)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func masterReplicaDialer(
	failover *sentinelFailover,
) func(ctx context.Context, network, addr string) (net.Conn, error) {
	return func(ctx context.Context, network, _ string) (net.Conn, error) {
		var addr string
		var err error

		if failover.opt.ReplicaOnly {
			addr, err = failover.RandomReplicaAddr(ctx)
		} else {
			addr, err = failover.MasterAddr(ctx)
			if err == nil {
				failover.trySwitchMaster(ctx, addr)
			}
		}
		if err != nil {
			return nil, err
		}
		if failover.opt.Dialer != nil {
			return failover.opt.Dialer(ctx, network, addr)
		}

		netDialer := &net.Dialer{
			Timeout:         failover.opt.DialTimeout,
			KeepAliveConfig: defaultKeepAliveConfig,
		}
		if failover.opt.TLSConfig == nil {
			return netDialer.DialContext(ctx, network, addr)
		}
		return tls.DialWithDialer(netDialer, network, addr, failover.opt.TLSConfig)
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func masterReplicaDialer(
	failover *sentinelFailover,
	opt *Options,
) func(ctx context.Context, network, addr string) (net.Conn, error) {
	return func(ctx context.Context, network, _ string) (net.Conn, error) {
		var addr string
		var err error

		if failover.opt.ReplicaOnly {
			addr, err = failover.RandomReplicaAddr(ctx)
		} else {
			addr, err = failover.MasterAddr(ctx)
			if err == nil {
				failover.trySwitchMaster(ctx, addr)
			}
		}
		if err != nil {
			return nil, err
		}
		if failover.opt.Dialer != nil {
			return failover.opt.Dialer(ctx, network, addr)
		}

		netDialer := &net.Dialer{
			Timeout:         opt.DialTimeout,
			KeepAliveConfig: defaultKeepAliveConfig,
		}
		if failover.opt.TLSConfig == nil {
			return netDialer.DialContext(ctx, network, addr)
		}
		return tls.DialWithDialer(netDialer, network, addr, failover.opt.TLSConfig)
	}
}
```


---

### 🔹 Commit #04: `5a9916dd`
- **完整 Hash**: `5a9916dd5aaba028ce80cbb1cd70b1f8813349fd`
- **說明 (Ground Truth)**: fix(command): read past error elements in slices (#4137)
- **變更檔案數**: 1

#### 📄 檔案: `command.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:825, E:1111, A:0) ➔ After(N:829, E:1115, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 4, -Edges: 0, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `elemErr` (MODULE_STATE)
  • + [新增節點] `elemErr` (MODULE_STATE)
  • + [新增節點] `elemErr` (MODULE_STATE)
  • + [新增節點] `elemErr` (MODULE_STATE)
  • + [新增呼叫邊] `UintSliceCmd.readReply` ──[CALLS]──> `isRedisError (External/Pkg)`
  • + [新增呼叫邊] `FloatSliceCmd.readReply` ──[CALLS]──> `isRedisError (External/Pkg)`
  • + [新增呼叫邊] `StringSliceCmd.readReply` ──[CALLS]──> `isRedisError (External/Pkg)`
  • + [新增呼叫邊] `BoolSliceCmd.readReply` ──[CALLS]──> `isRedisError (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FloatSliceCmd.readReply()`
- **變更前簽章 (Before)**: `func FloatSliceCmd.readReply(rd *proto.Reader)` (L2100~L2118)
- **變更後簽章 (After)**: `func FloatSliceCmd.readReply(rd *proto.Reader)` (L2106~L2130)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (cmd *FloatSliceCmd) readReply(rd *proto.Reader) error {
	n, err := rd.ReadArrayLen()
	if err != nil {
		return err
	}

	cmd.val = make([]float64, n)
	for i := 0; i < len(cmd.val); i++ {
		switch num, err := rd.ReadFloat(); {
		case err == Nil:
			cmd.val[i] = 0
		case err != nil:
			return err
		default:
			cmd.val[i] = num
		}
	}
	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (cmd *FloatSliceCmd) readReply(rd *proto.Reader) error {
	n, err := rd.ReadArrayLen()
	if err != nil {
		return err
	}

	cmd.val = make([]float64, n)
	var elemErr error
	for i := 0; i < len(cmd.val); i++ {
		switch num, err := rd.ReadFloat(); {
		case err == Nil:
			cmd.val[i] = 0
		case err != nil:
			if !isRedisError(err) {
				return err
			}
			if elemErr == nil {
				elemErr = err
			}
		default:
			cmd.val[i] = num
		}
	}
	return elemErr
}
```

### 🔹 函式: `StringSliceCmd.readReply()`
- **變更前簽章 (Before)**: `func StringSliceCmd.readReply(rd *proto.Reader)` (L2176~L2193)
- **變更後簽章 (After)**: `func StringSliceCmd.readReply(rd *proto.Reader)` (L2188~L2211)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (cmd *StringSliceCmd) readReply(rd *proto.Reader) error {
	n, err := rd.ReadArrayLen()
	if err != nil {
		return err
	}
	cmd.val = make([]string, n)
	for i := 0; i < len(cmd.val); i++ {
		switch s, err := rd.ReadString(); {
		case err == Nil:
			cmd.val[i] = ""
		case err != nil:
			return err
		default:
			cmd.val[i] = s
		}
	}
	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (cmd *StringSliceCmd) readReply(rd *proto.Reader) error {
	n, err := rd.ReadArrayLen()
	if err != nil {
		return err
	}
	cmd.val = make([]string, n)
	var elemErr error
	for i := 0; i < len(cmd.val); i++ {
		switch s, err := rd.ReadString(); {
		case err == Nil:
			cmd.val[i] = ""
		case err != nil:
			if !isRedisError(err) {
				return err
			}
			if elemErr == nil {
				elemErr = err
			}
		default:
			cmd.val[i] = s
		}
	}
	return elemErr
}
```

### 🔹 函式: `BoolSliceCmd.readReply()`
- **變更前簽章 (Before)**: `func BoolSliceCmd.readReply(rd *proto.Reader)` (L2443~L2460)
- **變更後簽章 (After)**: `func BoolSliceCmd.readReply(rd *proto.Reader)` (L2461~L2484)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (cmd *BoolSliceCmd) readReply(rd *proto.Reader) error {
	n, err := rd.ReadArrayLen()
	if err != nil {
		return err
	}
	cmd.val = make([]bool, n)
	for i := 0; i < len(cmd.val); i++ {
		switch b, err := rd.ReadBool(); {
		case err == Nil:
			cmd.val[i] = false
		case err != nil:
			return err
		default:
			cmd.val[i] = b
		}
	}
	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (cmd *BoolSliceCmd) readReply(rd *proto.Reader) error {
	n, err := rd.ReadArrayLen()
	if err != nil {
		return err
	}
	cmd.val = make([]bool, n)
	var elemErr error
	for i := 0; i < len(cmd.val); i++ {
		switch b, err := rd.ReadBool(); {
		case err == Nil:
			cmd.val[i] = false
		case err != nil:
			if !isRedisError(err) {
				return err
			}
			if elemErr == nil {
				elemErr = err
			}
		default:
			cmd.val[i] = b
		}
	}
	return elemErr
}
```

### 🔹 函式: `UintSliceCmd.readReply()`
- **變更前簽章 (Before)**: `func UintSliceCmd.readReply(rd *proto.Reader)` (L1670~L1687)
- **變更後簽章 (After)**: `func UintSliceCmd.readReply(rd *proto.Reader)` (L1670~L1693)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (cmd *UintSliceCmd) readReply(rd *proto.Reader) error {
	n, err := rd.ReadArrayLen()
	if err != nil {
		return err
	}
	cmd.val = make([]uint64, n)
	for i := range cmd.val {
		switch num, err := rd.ReadUint(); {
		case err == Nil:
			cmd.val[i] = 0
		case err != nil:
			return err
		default:
			cmd.val[i] = num
		}
	}
	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (cmd *UintSliceCmd) readReply(rd *proto.Reader) error {
	n, err := rd.ReadArrayLen()
	if err != nil {
		return err
	}
	cmd.val = make([]uint64, n)
	var elemErr error
	for i := range cmd.val {
		switch num, err := rd.ReadUint(); {
		case err == Nil:
			cmd.val[i] = 0
		case err != nil:
			if !isRedisError(err) {
				return err
			}
			if elemErr == nil {
				elemErr = err
			}
		default:
			cmd.val[i] = num
		}
	}
	return elemErr
}
```


---

### 🔹 Commit #05: `46da7e22`
- **完整 Hash**: `46da7e22c8617acf51e5c0f32e9ff608f25ad0a7`
- **說明 (Ground Truth)**: fix(search): parse EXPLAINSCORE and empty RETURN (#4140)
- **變更檔案數**: 1

#### 📄 檔案: `search_commands.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:174, E:313, A:0) ➔ After(N:174, E:315, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `FTSearchCmd.readReply` ──[CALLS]──> `len (External/Pkg)`
  • + [新增呼叫邊] `parseFTSearchDocumentMapRESP3` ──[CALLS]──> `len (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `parseFTSearchDocumentMapRESP3()`
- **變更前簽章 (Before)**: `func parseFTSearchDocumentMapRESP3(itemMap map[interface{}]interface{})` (L2918~L2961)
- **變更後簽章 (After)**: `func parseFTSearchDocumentMapRESP3(itemMap map[interface{}]interface{})` (L2928~L2974)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func parseFTSearchDocumentMapRESP3(itemMap map[interface{}]interface{}) (Document, error) {
	doc := Document{
		Fields: make(map[string]string),
	}

	for k, v := range itemMap {
		key, ok := k.(string)
		if !ok {
			continue
		}

		switch key {
		case "id":
			if id, ok := v.(string); ok {
				doc.ID = id
			}
		case "score":
			if score, ok := v.(float64); ok {
				doc.Score = &score
			}
		case "payload":
			if payload, ok := v.(string); ok {
				doc.Payload = &payload
			}
		case "sortkey":
			if sortKey, ok := v.(string); ok {
				doc.SortKey = &sortKey
			}
		case "extra_attributes":
			if extraAttrs, ok := v.(map[interface{}]interface{}); ok {
				for ek, ev := range extraAttrs {
					if ekStr, ok := ek.(string); ok {
						if evStr, ok := ev.(string); ok {
							doc.Fields[ekStr] = evStr
						}
					}
				}
			}
			// Ignore "values" and other fields as per the spec
		}
	}

	return doc, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func parseFTSearchDocumentMapRESP3(itemMap map[interface{}]interface{}) (Document, error) {
	doc := Document{
		Fields: make(map[string]string),
	}

	for k, v := range itemMap {
		key, ok := k.(string)
		if !ok {
			continue
		}

		switch key {
		case "id":
			if id, ok := v.(string); ok {
				doc.ID = id
			}
		case "score":
			if arr, ok := v.([]interface{}); ok && len(arr) > 0 {
				v = arr[0]
			}
			if score, ok := v.(float64); ok {
				doc.Score = &score
			}
		case "payload":
			if payload, ok := v.(string); ok {
				doc.Payload = &payload
			}
		case "sortkey":
			if sortKey, ok := v.(string); ok {
				doc.SortKey = &sortKey
			}
		case "extra_attributes":
			if extraAttrs, ok := v.(map[interface{}]interface{}); ok {
				for ek, ev := range extraAttrs {
					if ekStr, ok := ek.(string); ok {
						if evStr, ok := ev.(string); ok {
							doc.Fields[ekStr] = evStr
						}
					}
				}
			}
			// Ignore "values" and other fields as per the spec
		}
	}

	return doc, nil
}
```

### 🔹 函式: `FTSearchCmd.readReply()`
- **變更前簽章 (Before)**: `func FTSearchCmd.readReply(rd *proto.Reader)` (L2821~L2853)
- **變更後簽章 (After)**: `func FTSearchCmd.readReply(rd *proto.Reader)` (L2825~L2863)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (cmd *FTSearchCmd) readReply(rd *proto.Reader) (err error) {
	readType, err := rd.PeekReplyType()
	if err != nil {
		return err
	}

	// RESP3 returns a map, RESP2 returns an array
	if readType == proto.RespMap {
		// Read raw response first for backwards compatibility
		cmd.rawVal, err = rd.ReadReply()
		if err != nil {
			return err
		}
		// Parse the raw response into structured result
		if mapVal, ok := cmd.rawVal.(map[interface{}]interface{}); ok {
			cmd.val, err = parseFTSearchMapRESP3(mapVal)
		} else {
			return fmt.Errorf("unexpected RESP3 response type: %T", cmd.rawVal)
		}
		return err
	}

	// RESP2 format or error response - use ReadReply to handle errors properly
	data, err := rd.ReadReply()
	if err != nil {
		return err
	}
	if dataSlice, ok := data.([]interface{}); ok {
		cmd.val, err = parseFTSearch(dataSlice, cmd.options.NoContent, cmd.options.WithScores, cmd.options.WithPayloads, cmd.options.WithSortKeys)
		return err
	}
	return fmt.Errorf("unexpected response type: %T", data)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (cmd *FTSearchCmd) readReply(rd *proto.Reader) (err error) {
	readType, err := rd.PeekReplyType()
	if err != nil {
		return err
	}

	// RESP3 returns a map, RESP2 returns an array
	if readType == proto.RespMap {
		// Read raw response first for backwards compatibility
		cmd.rawVal, err = rd.ReadReply()
		if err != nil {
			return err
		}
		// Parse the raw response into structured result
		if mapVal, ok := cmd.rawVal.(map[interface{}]interface{}); ok {
			cmd.val, err = parseFTSearchMapRESP3(mapVal)
		} else {
			return fmt.Errorf("unexpected RESP3 response type: %T", cmd.rawVal)
		}
		return err
	}

	// RESP2 format or error response - use ReadReply to handle errors properly
	data, err := rd.ReadReply()
	if err != nil {
		return err
	}
	if dataSlice, ok := data.([]interface{}); ok {
		opts := cmd.options
		if opts == nil {
			opts = &FTSearchOptions{}
		}
		// An empty non-nil Return sends RETURN 0: no field list, like NOCONTENT.
		noContent := opts.NoContent || (opts.Return != nil && len(opts.Return) == 0)
		cmd.val, err = parseFTSearch(dataSlice, noContent, opts.WithScores, opts.WithPayloads, opts.WithSortKeys)
		return err
	}
	return fmt.Errorf("unexpected response type: %T", data)
}
```

### 🔹 函式: `parseFTSearch()`
- **變更前簽章 (Before)**: `func parseFTSearch(data []interface{}, noContent, withScores, withPayloads, withSortKeys bool)` (L2688~L2773)
- **變更後簽章 (After)**: `func parseFTSearch(data []interface{}, noContent, withScores, withPayloads, withSortKeys bool)` (L2688~L2777)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func parseFTSearch(data []interface{}, noContent, withScores, withPayloads, withSortKeys bool) (FTSearchResult, error) {
	if len(data) < 1 {
		return FTSearchResult{}, fmt.Errorf("unexpected search result format")
	}

	total, ok := data[0].(int64)
	if !ok {
		return FTSearchResult{}, fmt.Errorf("invalid total results format")
	}

	var results []Document
	for i := 1; i < len(data); {
		docID, ok := data[i].(string)
		if !ok {
			return FTSearchResult{}, fmt.Errorf("invalid document ID format")
		}

		doc := Document{
			ID:     docID,
			Fields: make(map[string]string),
		}
		i++

		if noContent {
			results = append(results, doc)
			continue
		}

		if withScores && i < len(data) {
			if scoreStr, ok := data[i].(string); ok {
				score, err := strconv.ParseFloat(scoreStr, 64)
				if err != nil {
					return FTSearchResult{}, fmt.Errorf("invalid score format")
				}
				doc.Score = &score
				i++
			}
		}

		if withPayloads && i < len(data) {
			if payload, ok := data[i].(string); ok {
				doc.Payload = &payload
				i++
			}
		}

		if withSortKeys && i < len(data) {
			if sortKey, ok := data[i].(string); ok {
				doc.SortKey = &sortKey
				i++
			}
		}

		if i < len(data) {
			fields, ok := data[i].([]interface{})
			if !ok {
				if data[i] == proto.Nil || data[i] == nil {
					doc.Error = proto.Nil
					doc.Fields = map[string]string{}
					fields = []interface{}{}
				} else {
					return FTSearchResult{}, fmt.Errorf("invalid document fields format")
				}
			}

			for j := 0; j < len(fields); j += 2 {
				key, ok := fields[j].(string)
				if !ok {
					return FTSearchResult{}, fmt.Errorf("invalid field key format")
				}
				value, ok := fields[j+1].(string)
				if !ok {
					return FTSearchResult{}, fmt.Errorf("invalid field value format")
				}
				doc.Fields[key] = value
			}
			i++
		}

		results = append(results, doc)
	}
	return FTSearchResult{
		Total: int(total),
		Docs:  results,
	}, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func parseFTSearch(data []interface{}, noContent, withScores, withPayloads, withSortKeys bool) (FTSearchResult, error) {
	if len(data) < 1 {
		return FTSearchResult{}, fmt.Errorf("unexpected search result format")
	}

	total, ok := data[0].(int64)
	if !ok {
		return FTSearchResult{}, fmt.Errorf("invalid total results format")
	}

	var results []Document
	for i := 1; i < len(data); {
		docID, ok := data[i].(string)
		if !ok {
			return FTSearchResult{}, fmt.Errorf("invalid document ID format")
		}

		doc := Document{
			ID:     docID,
			Fields: make(map[string]string),
		}
		i++

		if withScores && i < len(data) {
			scoreVal := data[i]
			if arr, ok := scoreVal.([]interface{}); ok && len(arr) > 0 {
				scoreVal = arr[0]
			}
			if scoreStr, ok := scoreVal.(string); ok {
				score, err := strconv.ParseFloat(scoreStr, 64)
				if err != nil {
					return FTSearchResult{}, fmt.Errorf("invalid score format")
				}
				doc.Score = &score
			}
			i++
		}

		if withPayloads && i < len(data) {
			if payload, ok := data[i].(string); ok {
				doc.Payload = &payload
			}
			i++
		}

		if withSortKeys && i < len(data) {
			if sortKey, ok := data[i].(string); ok {
				doc.SortKey = &sortKey
			}
			i++
		}

		if noContent {
			results = append(results, doc)
			continue
		}

		if i < len(data) {
			fields, ok := data[i].([]interface{})
			if !ok {
				if data[i] == proto.Nil || data[i] == nil {
					doc.Error = proto.Nil
					doc.Fields = map[string]string{}
					fields = []interface{}{}
				} else {
					return FTSearchResult{}, fmt.Errorf("invalid document fields format")
				}
			}

			for j := 0; j < len(fields); j += 2 {
				key, ok := fields[j].(string)
				if !ok {
					return FTSearchResult{}, fmt.Errorf("invalid field key format")
				}
				value, ok := fields[j+1].(string)
				if !ok {
					return FTSearchResult{}, fmt.Errorf("invalid field value format")
				}
				doc.Fields[key] = value
			}
			i++
		}

		results = append(results, doc)
	}
	return FTSearchResult{
		Total: int(total),
		Docs:  results,
	}, nil
}
```


---

### 🔹 Commit #06: `68d37e8d`
- **完整 Hash**: `68d37e8d8b6a12986ce18e4ab61030fb7d4dd2d2`
- **說明 (Ground Truth)**: fix(conn): validate URL retry and buffer values (#4144)
- **變更檔案數**: 3

#### 📄 檔案: `options.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:63, E:70, A:0) ➔ After(N:66, E:80, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 10, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `queryOptions.dialerRetryTimeout` (FUNCTION_DEF)
  • + [新增節點] `queryOptions.nonNegativeInt` (FUNCTION_DEF)
  • + [新增節點] `name` (MODULE_STATE)
  • + [新增呼叫邊] `queryOptions.nonNegativeInt` ──[CALLS]──> `queryOptions.int`
  • + [新增呼叫邊] `queryOptions.nonNegativeInt` ──[CALLS]──> `fmt.Errorf (External/Pkg)`
  • + [新增呼叫邊] `queryOptions.dialerRetryTimeout` ──[CALLS]──> `queryOptions.string`
  • + [新增呼叫邊] `queryOptions.dialerRetryTimeout` ──[CALLS]──> `strconv.Atoi (External/Pkg)`
  • + [新增呼叫邊] `queryOptions.dialerRetryTimeout` ──[CALLS]──> `time.ParseDuration (External/Pkg)`
  • + [新增呼叫邊] `queryOptions.dialerRetryTimeout` ──[CALLS]──> `strings.HasPrefix (External/Pkg)`
  • + [新增呼叫邊] `queryOptions.dialerRetryTimeout` ──[CALLS]──> `errors.New (External/Pkg)`
  • + [新增呼叫邊] `queryOptions.dialerRetryTimeout` ──[CALLS]──> `fmt.Errorf (External/Pkg)`
  • + [新增呼叫邊] `setupConnParams` ──[CALLS]──> `queryOptions.dialerRetryTimeout`
  • + [新增呼叫邊] `setupConnParams` ──[CALLS]──> `queryOptions.nonNegativeInt`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `setupConnParams()`
- **變更前簽章 (Before)**: `func setupConnParams(u *url.URL, o *Options)` (L1105~L1172)
- **變更後簽章 (After)**: `func setupConnParams(u *url.URL, o *Options)` (L1152~L1219)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func setupConnParams(u *url.URL, o *Options) (*Options, error) {
	q := queryOptions{q: u.Query()}

	// compat: a future major release may use q.int("db")
	if tmp := q.string("db"); tmp != "" {
		db, err := strconv.Atoi(tmp)
		if err != nil {
			return nil, fmt.Errorf("redis: invalid database number: %w", err)
		}
		o.DB = db
	}

	o.Protocol = q.int("protocol")
	o.ClientName = q.string("client_name")
	o.MaxRetries = q.int("max_retries")
	o.MinRetryBackoff = q.duration("min_retry_backoff")
	o.MaxRetryBackoff = q.duration("max_retry_backoff")
	o.DialTimeout = q.duration("dial_timeout")
	o.DialerRetries = q.int("dialer_retries")
	o.DialerRetryTimeout = q.duration("dialer_retry_timeout")
	o.ReadTimeout = q.duration("read_timeout")
	o.WriteTimeout = q.duration("write_timeout")
	o.ContextTimeoutEnabled = q.bool("context_timeout_enabled")
	o.ReadBufferSize = q.int("read_buffer_size")
	o.WriteBufferSize = q.int("write_buffer_size")
	o.DisableIdentity = q.bool("disable_identity")
	o.IdentitySuffix = q.string("identity_suffix")
	o.PoolFIFO = q.bool("pool_fifo")
	o.PoolSize = q.int("pool_size")
	o.PoolTimeout = q.duration("pool_timeout")
	o.MinIdleConns = q.int("min_idle_conns")
	o.MaxIdleConns = q.int("max_idle_conns")
	o.MaxActiveConns = q.int("max_active_conns")
	o.MaxConcurrentDials = q.int("max_concurrent_dials")
	// Pipeline pool (created by default): allow URL-configured clients to opt out
	// (pipeline_pool_size=-1) or tune it, otherwise these would be rejected as
	// unexpected options. q.int accepts a negative value.
	o.PipelinePoolSize = q.int("pipeline_pool_size")
	o.PipelineMinIdleConns = q.int("pipeline_min_idle_conns")
	o.PipelineReadBufferSize = q.int("pipeline_read_buffer_size")
	o.PipelineWriteBufferSize = q.int("pipeline_write_buffer_size")
	if q.has("conn_max_idle_time") {
		o.ConnMaxIdleTime = q.duration("conn_max_idle_time")
	} else {
		o.ConnMaxIdleTime = q.duration("idle_timeout")
	}
	if q.has("conn_max_lifetime") {
		o.ConnMaxLifetime = q.duration("conn_max_lifetime")
	} else {
		o.ConnMaxLifetime = q.duration("max_conn_age")
	}
	if q.has("conn_max_lifetime_jitter") {
		o.ConnMaxLifetimeJitter = min(q.duration("conn_max_lifetime_jitter"), o.ConnMaxLifetime)
	}
	if o.TLSConfig != nil && q.has("skip_verify") {
		o.TLSConfig.InsecureSkipVerify = q.bool("skip_verify")
	}
	if q.err != nil {
		return nil, q.err
	}

	// any parameters left?
	if r := q.remaining(); len(r) > 0 {
		return nil, fmt.Errorf("redis: unexpected option: %s", strings.Join(r, ", "))
	}

	return o, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func setupConnParams(u *url.URL, o *Options) (*Options, error) {
	q := queryOptions{q: u.Query()}

	// compat: a future major release may use q.int("db")
	if tmp := q.string("db"); tmp != "" {
		db, err := strconv.Atoi(tmp)
		if err != nil {
			return nil, fmt.Errorf("redis: invalid database number: %w", err)
		}
		o.DB = db
	}

	o.Protocol = q.int("protocol")
	o.ClientName = q.string("client_name")
	o.MaxRetries = q.int("max_retries")
	o.MinRetryBackoff = q.duration("min_retry_backoff")
	o.MaxRetryBackoff = q.duration("max_retry_backoff")
	o.DialTimeout = q.duration("dial_timeout")
	o.DialerRetries = q.int("dialer_retries")
	o.DialerRetryTimeout, o.DialerRetryBackoff = q.dialerRetryTimeout()
	o.ReadTimeout = q.duration("read_timeout")
	o.WriteTimeout = q.duration("write_timeout")
	o.ContextTimeoutEnabled = q.bool("context_timeout_enabled")
	o.ReadBufferSize = q.nonNegativeInt("read_buffer_size")
	o.WriteBufferSize = q.nonNegativeInt("write_buffer_size")
	o.DisableIdentity = q.bool("disable_identity")
	o.IdentitySuffix = q.string("identity_suffix")
	o.PoolFIFO = q.bool("pool_fifo")
	o.PoolSize = q.int("pool_size")
	o.PoolTimeout = q.duration("pool_timeout")
	o.MinIdleConns = q.int("min_idle_conns")
	o.MaxIdleConns = q.int("max_idle_conns")
	o.MaxActiveConns = q.int("max_active_conns")
	o.MaxConcurrentDials = q.int("max_concurrent_dials")
	// Pipeline pool (created by default): allow URL-configured clients to opt out
	// (pipeline_pool_size=-1) or tune it, otherwise these would be rejected as
	// unexpected options. q.int accepts a negative value.
	o.PipelinePoolSize = q.int("pipeline_pool_size")
	o.PipelineMinIdleConns = q.int("pipeline_min_idle_conns")
	o.PipelineReadBufferSize = q.int("pipeline_read_buffer_size")
	o.PipelineWriteBufferSize = q.int("pipeline_write_buffer_size")
	if q.has("conn_max_idle_time") {
		o.ConnMaxIdleTime = q.duration("conn_max_idle_time")
	} else {
		o.ConnMaxIdleTime = q.duration("idle_timeout")
	}
	if q.has("conn_max_lifetime") {
		o.ConnMaxLifetime = q.duration("conn_max_lifetime")
	} else {
		o.ConnMaxLifetime = q.duration("max_conn_age")
	}
	if q.has("conn_max_lifetime_jitter") {
		o.ConnMaxLifetimeJitter = min(q.duration("conn_max_lifetime_jitter"), o.ConnMaxLifetime)
	}
	if o.TLSConfig != nil && q.has("skip_verify") {
		o.TLSConfig.InsecureSkipVerify = q.bool("skip_verify")
	}
	if q.err != nil {
		return nil, q.err
	}

	// any parameters left?
	if r := q.remaining(); len(r) > 0 {
		return nil, fmt.Errorf("redis: unexpected option: %s", strings.Join(r, ", "))
	}

	return o, nil
}
```


#### 📄 檔案: `osscluster.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:343, E:552, A:0) ➔ After(N:345, E:554, A:0)
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
  • + [新增節點] `q.dialerRetryTimeout (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `q.nonNegativeInt (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `setupClusterQueryParams` ──[CALLS]──> `q.dialerRetryTimeout (External/Pkg)`
  • + [新增呼叫邊] `setupClusterQueryParams` ──[CALLS]──> `q.nonNegativeInt (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 2 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `setupClusterQueryParams()`
- **變更前簽章 (Before)**: `func setupClusterQueryParams(u *url.URL, o *ClusterOptions)` (L393~L460)
- **變更後簽章 (After)**: `func setupClusterQueryParams(u *url.URL, o *ClusterOptions)` (L398~L465)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func setupClusterQueryParams(u *url.URL, o *ClusterOptions) (*ClusterOptions, error) {
	q := queryOptions{q: u.Query()}

	o.Protocol = q.int("protocol")
	o.ClientName = q.string("client_name")
	o.MaxRedirects = q.int("max_redirects")
	o.ReadOnly = q.bool("read_only")
	o.RouteByLatency = q.bool("route_by_latency")
	o.RouteByLatencyTolerance = q.duration("route_by_latency_tolerance")
	o.RouteRandomly = q.bool("route_randomly")
	o.MaxRetries = q.int("max_retries")
	o.MinRetryBackoff = q.duration("min_retry_backoff")
	o.MaxRetryBackoff = q.duration("max_retry_backoff")
	o.DialTimeout = q.duration("dial_timeout")
	o.DialerRetries = q.int("dialer_retries")
	o.DialerRetryTimeout = q.duration("dialer_retry_timeout")
	o.ReadTimeout = q.duration("read_timeout")
	o.WriteTimeout = q.duration("write_timeout")
	o.ContextTimeoutEnabled = q.bool("context_timeout_enabled")
	o.ReadBufferSize = q.int("read_buffer_size")
	o.WriteBufferSize = q.int("write_buffer_size")
	o.DisableIdentity = q.bool("disable_identity")
	o.IdentitySuffix = q.string("identity_suffix")
	o.PoolFIFO = q.bool("pool_fifo")
	o.PoolSize = q.int("pool_size")
	o.MaxConcurrentDials = q.int("max_concurrent_dials")
	o.MinIdleConns = q.int("min_idle_conns")
	o.MaxIdleConns = q.int("max_idle_conns")
	o.MaxActiveConns = q.int("max_active_conns")
	// Pipeline pool (per node, created by default): allow URL opt-out
	// (pipeline_pool_size=-1) / tuning, else rejected as unexpected options.
	o.PipelinePoolSize = q.int("pipeline_pool_size")
	o.PipelineMinIdleConns = q.int("pipeline_min_idle_conns")
	o.PipelineReadBufferSize = q.int("pipeline_read_buffer_size")
	o.PipelineWriteBufferSize = q.int("pipeline_write_buffer_size")
	o.PoolTimeout = q.duration("pool_timeout")
	o.ConnMaxLifetime = q.duration("conn_max_lifetime")
	if q.has("conn_max_lifetime_jitter") {
		o.ConnMaxLifetimeJitter = min(q.duration("conn_max_lifetime_jitter"), o.ConnMaxLifetime)
	}
	o.ConnMaxIdleTime = q.duration("conn_max_idle_time")
	o.FailingTimeoutSeconds = q.int("failing_timeout_seconds")
	if o.TLSConfig != nil && q.has("skip_verify") {
		o.TLSConfig.InsecureSkipVerify = q.bool("skip_verify")
	}

	if q.err != nil {
		return nil, q.err
	}

	// addr can be specified as many times as needed
	addrs := q.strings("addr")
	for _, addr := range addrs {
		h, p, err := net.SplitHostPort(addr)
		if err != nil || h == "" || p == "" {
			return nil, fmt.Errorf("redis: unable to parse addr param: %s", addr)
		}

		o.Addrs = append(o.Addrs, net.JoinHostPort(h, p))
	}

	// any parameters left?
	if r := q.remaining(); len(r) > 0 {
		return nil, fmt.Errorf("redis: unexpected option: %s", strings.Join(r, ", "))
	}

	return o, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func setupClusterQueryParams(u *url.URL, o *ClusterOptions) (*ClusterOptions, error) {
	q := queryOptions{q: u.Query()}

	o.Protocol = q.int("protocol")
	o.ClientName = q.string("client_name")
	o.MaxRedirects = q.int("max_redirects")
	o.ReadOnly = q.bool("read_only")
	o.RouteByLatency = q.bool("route_by_latency")
	o.RouteByLatencyTolerance = q.duration("route_by_latency_tolerance")
	o.RouteRandomly = q.bool("route_randomly")
	o.MaxRetries = q.int("max_retries")
	o.MinRetryBackoff = q.duration("min_retry_backoff")
	o.MaxRetryBackoff = q.duration("max_retry_backoff")
	o.DialTimeout = q.duration("dial_timeout")
	o.DialerRetries = q.int("dialer_retries")
	o.DialerRetryTimeout, o.DialerRetryBackoff = q.dialerRetryTimeout()
	o.ReadTimeout = q.duration("read_timeout")
	o.WriteTimeout = q.duration("write_timeout")
	o.ContextTimeoutEnabled = q.bool("context_timeout_enabled")
	o.ReadBufferSize = q.nonNegativeInt("read_buffer_size")
	o.WriteBufferSize = q.nonNegativeInt("write_buffer_size")
	o.DisableIdentity = q.bool("disable_identity")
	o.IdentitySuffix = q.string("identity_suffix")
	o.PoolFIFO = q.bool("pool_fifo")
	o.PoolSize = q.int("pool_size")
	o.MaxConcurrentDials = q.int("max_concurrent_dials")
	o.MinIdleConns = q.int("min_idle_conns")
	o.MaxIdleConns = q.int("max_idle_conns")
	o.MaxActiveConns = q.int("max_active_conns")
	// Pipeline pool (per node, created by default): allow URL opt-out
	// (pipeline_pool_size=-1) / tuning, else rejected as unexpected options.
	o.PipelinePoolSize = q.int("pipeline_pool_size")
	o.PipelineMinIdleConns = q.int("pipeline_min_idle_conns")
	o.PipelineReadBufferSize = q.int("pipeline_read_buffer_size")
	o.PipelineWriteBufferSize = q.int("pipeline_write_buffer_size")
	o.PoolTimeout = q.duration("pool_timeout")
	o.ConnMaxLifetime = q.duration("conn_max_lifetime")
	if q.has("conn_max_lifetime_jitter") {
		o.ConnMaxLifetimeJitter = min(q.duration("conn_max_lifetime_jitter"), o.ConnMaxLifetime)
	}
	o.ConnMaxIdleTime = q.duration("conn_max_idle_time")
	o.FailingTimeoutSeconds = q.int("failing_timeout_seconds")
	if o.TLSConfig != nil && q.has("skip_verify") {
		o.TLSConfig.InsecureSkipVerify = q.bool("skip_verify")
	}

	if q.err != nil {
		return nil, q.err
	}

	// addr can be specified as many times as needed
	addrs := q.strings("addr")
	for _, addr := range addrs {
		h, p, err := net.SplitHostPort(addr)
		if err != nil || h == "" || p == "" {
			return nil, fmt.Errorf("redis: unable to parse addr param: %s", addr)
		}

		o.Addrs = append(o.Addrs, net.JoinHostPort(h, p))
	}

	// any parameters left?
	if r := q.remaining(); len(r) > 0 {
		return nil, fmt.Errorf("redis: unexpected option: %s", strings.Join(r, ", "))
	}

	return o, nil
}
```


#### 📄 檔案: `sentinel.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:155, E:227, A:0) ➔ After(N:157, E:229, A:0)
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
  • + [新增節點] `q.nonNegativeInt (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `q.dialerRetryTimeout (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `setupFailoverConnParams` ──[CALLS]──> `q.dialerRetryTimeout (External/Pkg)`
  • + [新增呼叫邊] `setupFailoverConnParams` ──[CALLS]──> `q.nonNegativeInt (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `setupFailoverConnParams()`
- **變更前簽章 (Before)**: `func setupFailoverConnParams(u *url.URL, o *FailoverOptions)` (L465~L556)
- **變更後簽章 (After)**: `func setupFailoverConnParams(u *url.URL, o *FailoverOptions)` (L470~L561)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func setupFailoverConnParams(u *url.URL, o *FailoverOptions) (*FailoverOptions, error) {
	q := queryOptions{q: u.Query()}

	o.MasterName = q.string("master_name")
	o.ClientName = q.string("client_name")
	o.RouteByLatency = q.bool("route_by_latency")
	o.RouteByLatencyTolerance = q.duration("route_by_latency_tolerance")
	o.RouteRandomly = q.bool("route_randomly")
	o.ReplicaOnly = q.bool("replica_only")
	o.UseDisconnectedReplicas = q.bool("use_disconnected_replicas")
	o.Protocol = q.int("protocol")
	o.Username = q.string("username")
	o.Password = q.string("password")
	o.MaxRetries = q.int("max_retries")
	o.MinRetryBackoff = q.duration("min_retry_backoff")
	o.MaxRetryBackoff = q.duration("max_retry_backoff")
	o.DialTimeout = q.duration("dial_timeout")
	o.DialerRetries = q.int("dialer_retries")
	o.DialerRetryTimeout = q.duration("dialer_retry_timeout")
	o.ReadTimeout = q.duration("read_timeout")
	o.WriteTimeout = q.duration("write_timeout")
	o.ContextTimeoutEnabled = q.bool("context_timeout_enabled")
	o.ReadBufferSize = q.int("read_buffer_size")
	o.WriteBufferSize = q.int("write_buffer_size")
	o.PoolFIFO = q.bool("pool_fifo")
	o.PoolSize = q.int("pool_size")
	o.MaxConcurrentDials = q.int("max_concurrent_dials")
	o.MinIdleConns = q.int("min_idle_conns")
	o.MaxIdleConns = q.int("max_idle_conns")
	o.MaxActiveConns = q.int("max_active_conns")
	// Pipeline pool (created by default): allow URL opt-out
	// (pipeline_pool_size=-1) / tuning, else rejected as unexpected options.
	o.PipelinePoolSize = q.int("pipeline_pool_size")
	o.PipelineMinIdleConns = q.int("pipeline_min_idle_conns")
	o.PipelineReadBufferSize = q.int("pipeline_read_buffer_size")
	o.PipelineWriteBufferSize = q.int("pipeline_write_buffer_size")
	o.ConnMaxLifetime = q.duration("conn_max_lifetime")
	if q.has("conn_max_lifetime_jitter") {
		o.ConnMaxLifetimeJitter = min(q.duration("conn_max_lifetime_jitter"), o.ConnMaxLifetime)
	}
	o.ConnMaxIdleTime = q.duration("conn_max_idle_time")
	o.PoolTimeout = q.duration("pool_timeout")
	// disableIdentity and identitySuffix are the original camelCase spellings;
	// the snake_case names match the other URL parsers and the ParseURL docs.
	if q.has("disable_identity") {
		o.DisableIdentity = q.bool("disable_identity")
	} else {
		o.DisableIdentity = q.bool("disableIdentity")
	}
	if q.has("identity_suffix") {
		o.IdentitySuffix = q.string("identity_suffix")
	} else {
		o.IdentitySuffix = q.string("identitySuffix")
	}
	o.UnstableResp3 = q.bool("unstable_resp3")

	if q.err != nil {
		return nil, q.err
	}

	if tmp := q.string("db"); tmp != "" {
		db, err := strconv.Atoi(tmp)
		if err != nil {
			return nil, fmt.Errorf("redis: invalid database number: %w", err)
		}
		o.DB = db
	}

	addrs := q.strings("addr")
	for _, addr := range addrs {
		h, p, err := net.SplitHostPort(addr)
		if err != nil || h == "" || p == "" {
			return nil, fmt.Errorf("redis: unable to parse addr param: %s", addr)
		}

		o.SentinelAddrs = append(o.SentinelAddrs, net.JoinHostPort(h, p))
	}

	if o.TLSConfig != nil && q.has("skip_verify") {
		o.TLSConfig.InsecureSkipVerify = q.bool("skip_verify")
	}
	if q.err != nil {
		return nil, q.err
	}

	// any parameters left?
	if r := q.remaining(); len(r) > 0 {
		return nil, fmt.Errorf("redis: unexpected option: %s", strings.Join(r, ", "))
	}

	return o, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func setupFailoverConnParams(u *url.URL, o *FailoverOptions) (*FailoverOptions, error) {
	q := queryOptions{q: u.Query()}

	o.MasterName = q.string("master_name")
	o.ClientName = q.string("client_name")
	o.RouteByLatency = q.bool("route_by_latency")
	o.RouteByLatencyTolerance = q.duration("route_by_latency_tolerance")
	o.RouteRandomly = q.bool("route_randomly")
	o.ReplicaOnly = q.bool("replica_only")
	o.UseDisconnectedReplicas = q.bool("use_disconnected_replicas")
	o.Protocol = q.int("protocol")
	o.Username = q.string("username")
	o.Password = q.string("password")
	o.MaxRetries = q.int("max_retries")
	o.MinRetryBackoff = q.duration("min_retry_backoff")
	o.MaxRetryBackoff = q.duration("max_retry_backoff")
	o.DialTimeout = q.duration("dial_timeout")
	o.DialerRetries = q.int("dialer_retries")
	o.DialerRetryTimeout, o.DialerRetryBackoff = q.dialerRetryTimeout()
	o.ReadTimeout = q.duration("read_timeout")
	o.WriteTimeout = q.duration("write_timeout")
	o.ContextTimeoutEnabled = q.bool("context_timeout_enabled")
	o.ReadBufferSize = q.nonNegativeInt("read_buffer_size")
	o.WriteBufferSize = q.nonNegativeInt("write_buffer_size")
	o.PoolFIFO = q.bool("pool_fifo")
	o.PoolSize = q.int("pool_size")
	o.MaxConcurrentDials = q.int("max_concurrent_dials")
	o.MinIdleConns = q.int("min_idle_conns")
	o.MaxIdleConns = q.int("max_idle_conns")
	o.MaxActiveConns = q.int("max_active_conns")
	// Pipeline pool (created by default): allow URL opt-out
	// (pipeline_pool_size=-1) / tuning, else rejected as unexpected options.
	o.PipelinePoolSize = q.int("pipeline_pool_size")
	o.PipelineMinIdleConns = q.int("pipeline_min_idle_conns")
	o.PipelineReadBufferSize = q.int("pipeline_read_buffer_size")
	o.PipelineWriteBufferSize = q.int("pipeline_write_buffer_size")
	o.ConnMaxLifetime = q.duration("conn_max_lifetime")
	if q.has("conn_max_lifetime_jitter") {
		o.ConnMaxLifetimeJitter = min(q.duration("conn_max_lifetime_jitter"), o.ConnMaxLifetime)
	}
	o.ConnMaxIdleTime = q.duration("conn_max_idle_time")
	o.PoolTimeout = q.duration("pool_timeout")
	// disableIdentity and identitySuffix are the original camelCase spellings;
	// the snake_case names match the other URL parsers and the ParseURL docs.
	if q.has("disable_identity") {
		o.DisableIdentity = q.bool("disable_identity")
	} else {
		o.DisableIdentity = q.bool("disableIdentity")
	}
	if q.has("identity_suffix") {
		o.IdentitySuffix = q.string("identity_suffix")
	} else {
		o.IdentitySuffix = q.string("identitySuffix")
	}
	o.UnstableResp3 = q.bool("unstable_resp3")

	if q.err != nil {
		return nil, q.err
	}

	if tmp := q.string("db"); tmp != "" {
		db, err := strconv.Atoi(tmp)
		if err != nil {
			return nil, fmt.Errorf("redis: invalid database number: %w", err)
		}
		o.DB = db
	}

	addrs := q.strings("addr")
	for _, addr := range addrs {
		h, p, err := net.SplitHostPort(addr)
		if err != nil || h == "" || p == "" {
			return nil, fmt.Errorf("redis: unable to parse addr param: %s", addr)
		}

		o.SentinelAddrs = append(o.SentinelAddrs, net.JoinHostPort(h, p))
	}

	if o.TLSConfig != nil && q.has("skip_verify") {
		o.TLSConfig.InsecureSkipVerify = q.bool("skip_verify")
	}
	if q.err != nil {
		return nil, q.err
	}

	// any parameters left?
	if r := q.remaining(); len(r) > 0 {
		return nil, fmt.Errorf("redis: unexpected option: %s", strings.Join(r, ", "))
	}

	return o, nil
}
```


---

### 🔹 Commit #07: `fecce1ac`
- **完整 Hash**: `fecce1ac79e5efa6d812c24fb3c81d3d8591f3a8`
- **說明 (Ground Truth)**: fix(cmd): allow = in CLIENT INFO values (#4096)
- **變更檔案數**: 1

#### 📄 檔案: `command.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:825, E:1110, A:0) ➔ After(N:825, E:1111, A:0)
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
  • + [新增呼叫邊] `parseClientInfo` ──[CALLS]──> `strings.Cut (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `parseClientInfo()`
- **變更前簽章 (Before)**: `func parseClientInfo(txt string)` (L8058~L8208)
- **變更後簽章 (After)**: `func parseClientInfo(txt string)` (L8058~L8207)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func parseClientInfo(txt string) (info *ClientInfo, err error) {
	info = &ClientInfo{}
	for _, s := range strings.Split(txt, " ") {
		kv := strings.Split(s, "=")
		if len(kv) != 2 {
			return nil, fmt.Errorf("redis: unexpected client info data (%s)", s)
		}
		key, val := kv[0], kv[1]

		switch key {
		case "id":
			info.ID, err = strconv.ParseInt(val, 10, 64)
		case "addr":
			info.Addr = val
		case "laddr":
			info.LAddr = val
		case "fd":
			info.FD, err = strconv.ParseInt(val, 10, 64)
		case "name":
			info.Name = val
		case "age":
			var age int
			if age, err = strconv.Atoi(val); err == nil {
				info.Age = time.Duration(age) * time.Second
			}
		case "idle":
			var idle int
			if idle, err = strconv.Atoi(val); err == nil {
				info.Idle = time.Duration(idle) * time.Second
			}
		case "flags":
			if val == "N" {
				break
			}

			for i := 0; i < len(val); i++ {
				switch val[i] {
				case 'S':
					info.Flags |= ClientSlave
				case 'O':
					info.Flags |= ClientSlave | ClientMonitor
				case 'M':
					info.Flags |= ClientMaster
				case 'P':
					info.Flags |= ClientPubSub
				case 'x':
					info.Flags |= ClientMulti
				case 'b':
					info.Flags |= ClientBlocked
				case 't':
					info.Flags |= ClientTracking
				case 'R':
					info.Flags |= ClientTrackingBrokenRedir
				case 'B':
					info.Flags |= ClientTrackingBCAST
				case 'd':
					info.Flags |= ClientDirtyCAS
				case 'c':
					info.Flags |= ClientCloseAfterCommand
				case 'u':
					info.Flags |= ClientUnBlocked
				case 'A':
					info.Flags |= ClientCloseASAP
				case 'U':
					info.Flags |= ClientUnixSocket
				case 'r':
					info.Flags |= ClientReadOnly
				case 'e':
					info.Flags |= ClientNoEvict
				case 'T':
					info.Flags |= ClientNoTouch
				default:
					// Forward compatibility: servers can return client-flag
					// characters this client does not recognize (new flags are
					// added over time). Skip them instead of failing, as the
					// CLIENT LIST/INFO docs advise for version-safe parsing, and
					// matching the "skip unknown fields" behaviour of the field
					// switch below.
				}
			}
		case "db":
			info.DB, err = strconv.Atoi(val)
		case "sub":
			info.Sub, err = strconv.Atoi(val)
		case "psub":
			info.PSub, err = strconv.Atoi(val)
		case "ssub":
			info.SSub, err = strconv.Atoi(val)
		case "multi":
			info.Multi, err = strconv.Atoi(val)
		case "watch":
			info.Watch, err = strconv.Atoi(val)
		case "qbuf":
			info.QueryBuf, err = strconv.Atoi(val)
		case "qbuf-free":
			info.QueryBufFree, err = strconv.Atoi(val)
		case "argv-mem":
			info.ArgvMem, err = strconv.Atoi(val)
		case "multi-mem":
			info.MultiMem, err = strconv.Atoi(val)
		case "rbs":
			info.BufferSize, err = strconv.Atoi(val)
		case "rbp":
			info.BufferPeak, err = strconv.Atoi(val)
		case "obl":
			info.OutputBufferLength, err = strconv.Atoi(val)
		case "oll":
			info.OutputListLength, err = strconv.Atoi(val)
		case "omem":
			info.OutputMemory, err = strconv.Atoi(val)
		case "tot-mem":
			info.TotalMemory, err = strconv.Atoi(val)
		case "tot-net-in":
			info.TotalNetIn, err = strconv.Atoi(val)
		case "tot-net-out":
			info.TotalNetOut, err = strconv.Atoi(val)
		case "tot-cmds":
			info.TotalCmds, err = strconv.Atoi(val)
		case "events":
			info.Events = val
		case "cmd":
			info.LastCmd = val
		case "user":
			info.User = val
		case "redir":
			info.Redir, err = strconv.ParseInt(val, 10, 64)
		case "resp":
			info.Resp, err = strconv.Atoi(val)
		case "lib-name":
			info.LibName = val
		case "lib-ver":
			info.LibVer = val
		case "io-thread":
			info.IoThread, err = strconv.Atoi(val)
		case "read-events":
			info.ReadEvents, err = strconv.ParseUint(val, 10, 64)
		case "avg-pipeline-len-sum":
			info.AvgPipelineLenSum, err = strconv.ParseUint(val, 10, 64)
		case "avg-pipeline-len-cnt":
			info.AvgPipelineLenCnt, err = strconv.ParseUint(val, 10, 64)
		default:
			// skip unknown fields
		}

		if err != nil {
			return nil, err
		}
	}

	return info, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func parseClientInfo(txt string) (info *ClientInfo, err error) {
	info = &ClientInfo{}
	for _, s := range strings.Split(txt, " ") {
		key, val, ok := strings.Cut(s, "=")
		if !ok {
			return nil, fmt.Errorf("redis: unexpected client info data (%s)", s)
		}

		switch key {
		case "id":
			info.ID, err = strconv.ParseInt(val, 10, 64)
		case "addr":
			info.Addr = val
		case "laddr":
			info.LAddr = val
		case "fd":
			info.FD, err = strconv.ParseInt(val, 10, 64)
		case "name":
			info.Name = val
		case "age":
			var age int
			if age, err = strconv.Atoi(val); err == nil {
				info.Age = time.Duration(age) * time.Second
			}
		case "idle":
			var idle int
			if idle, err = strconv.Atoi(val); err == nil {
				info.Idle = time.Duration(idle) * time.Second
			}
		case "flags":
			if val == "N" {
				break
			}

			for i := 0; i < len(val); i++ {
				switch val[i] {
				case 'S':
					info.Flags |= ClientSlave
				case 'O':
					info.Flags |= ClientSlave | ClientMonitor
				case 'M':
					info.Flags |= ClientMaster
				case 'P':
					info.Flags |= ClientPubSub
				case 'x':
					info.Flags |= ClientMulti
				case 'b':
					info.Flags |= ClientBlocked
				case 't':
					info.Flags |= ClientTracking
				case 'R':
					info.Flags |= ClientTrackingBrokenRedir
				case 'B':
					info.Flags |= ClientTrackingBCAST
				case 'd':
					info.Flags |= ClientDirtyCAS
				case 'c':
					info.Flags |= ClientCloseAfterCommand
				case 'u':
					info.Flags |= ClientUnBlocked
				case 'A':
					info.Flags |= ClientCloseASAP
				case 'U':
					info.Flags |= ClientUnixSocket
				case 'r':
					info.Flags |= ClientReadOnly
				case 'e':
					info.Flags |= ClientNoEvict
				case 'T':
					info.Flags |= ClientNoTouch
				default:
					// Forward compatibility: servers can return client-flag
					// characters this client does not recognize (new flags are
					// added over time). Skip them instead of failing, as the
					// CLIENT LIST/INFO docs advise for version-safe parsing, and
					// matching the "skip unknown fields" behaviour of the field
					// switch below.
				}
			}
		case "db":
			info.DB, err = strconv.Atoi(val)
		case "sub":
			info.Sub, err = strconv.Atoi(val)
		case "psub":
			info.PSub, err = strconv.Atoi(val)
		case "ssub":
			info.SSub, err = strconv.Atoi(val)
		case "multi":
			info.Multi, err = strconv.Atoi(val)
		case "watch":
			info.Watch, err = strconv.Atoi(val)
		case "qbuf":
			info.QueryBuf, err = strconv.Atoi(val)
		case "qbuf-free":
			info.QueryBufFree, err = strconv.Atoi(val)
		case "argv-mem":
			info.ArgvMem, err = strconv.Atoi(val)
		case "multi-mem":
			info.MultiMem, err = strconv.Atoi(val)
		case "rbs":
			info.BufferSize, err = strconv.Atoi(val)
		case "rbp":
			info.BufferPeak, err = strconv.Atoi(val)
		case "obl":
			info.OutputBufferLength, err = strconv.Atoi(val)
		case "oll":
			info.OutputListLength, err = strconv.Atoi(val)
		case "omem":
			info.OutputMemory, err = strconv.Atoi(val)
		case "tot-mem":
			info.TotalMemory, err = strconv.Atoi(val)
		case "tot-net-in":
			info.TotalNetIn, err = strconv.Atoi(val)
		case "tot-net-out":
			info.TotalNetOut, err = strconv.Atoi(val)
		case "tot-cmds":
			info.TotalCmds, err = strconv.Atoi(val)
		case "events":
			info.Events = val
		case "cmd":
			info.LastCmd = val
		case "user":
			info.User = val
		case "redir":
			info.Redir, err = strconv.ParseInt(val, 10, 64)
		case "resp":
			info.Resp, err = strconv.Atoi(val)
		case "lib-name":
			info.LibName = val
		case "lib-ver":
			info.LibVer = val
		case "io-thread":
			info.IoThread, err = strconv.Atoi(val)
		case "read-events":
			info.ReadEvents, err = strconv.ParseUint(val, 10, 64)
		case "avg-pipeline-len-sum":
			info.AvgPipelineLenSum, err = strconv.ParseUint(val, 10, 64)
		case "avg-pipeline-len-cnt":
			info.AvgPipelineLenCnt, err = strconv.ParseUint(val, 10, 64)
		default:
			// skip unknown fields
		}

		if err != nil {
			return nil, err
		}
	}

	return info, nil
}
```


---

### 🔹 Commit #08: `0c02a494`
- **完整 Hash**: `0c02a49410076dcc905308a5e29cc9e3230da413`
- **說明 (Ground Truth)**: fix(conn): preserve hooks in WithTimeout clones (#4095)
- **變更檔案數**: 1

#### 📄 檔案: `redis.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:382, E:511, A:0) ➔ After(N:382, E:512, A:0)
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
  • + [新增呼叫邊] `baseClient.clone` ──[CALLS]──> `baseClient.clone`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `baseClient.clone()`
- **變更前簽章 (Before)**: `func baseClient.clone()` (L519~L561)
- **變更後簽章 (After)**: `func baseClient.clone()` (L519~L566)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *baseClient) clone() *baseClient {
	c.maintNotificationsManagerLock.RLock()
	maintNotificationsManager := c.maintNotificationsManager
	c.maintNotificationsManagerLock.RUnlock()

	clone := &baseClient{
		apClosed: c.apClosed,
		opt:      c.opt,
		connPool: c.connPool,
		// Pointer copy on purpose: the clone shares the parent's already-created
		// pipeline pool over the one shared pool set, rather than building its own.
		pipelinePool:                c.pipelinePool,
		pubSubPool:                  c.pubSubPool,
		onClose:                     c.onClose,
		pushProcessor:               c.pushProcessor,
		maintNotificationsManager:   maintNotificationsManager,
		streamingCredentialsManager: c.streamingCredentialsManager,
		himport:                     c.himport,
		csc:                         c.csc,
		// cscPoolHook and cscActive travel with the cache (read in processCached);
		// the owner-only fields — cscDrainHandle, cscOwnsCache — do not, so a clone's
		// Close never tears down the owner's resources.
		cscPoolHook:  c.cscPoolHook,
		cscActive:    c.cscActive,
		cscKeyPrefix: c.cscKeyPrefix,
		// cscRefreshQueue is SHARED (pointer copy), like cscPoolHook: processCached
		// calls signalDemand on it so a miss for a key still in the refresher's
		// window flushes that window early. Without the share a clone's field is
		// nil and signalDemand no-ops, so the clone's miss waits the full window
		// (#3965 F4). Lifecycle stays owner-only: signalDemand is a nil-safe,
		// non-blocking buffered send that does no I/O, and teardown keys off the
		// owner-only cscRefreshHandle/cscDrainHandle (both nil in a clone), so a
		// clone only SIGNALS the queue and never stops it — even a clone outliving
		// the owner's Close just sends into a buffered channel whose worker has
		// exited, which is harmless.
		cscRefreshQueue: c.cscRefreshQueue,
	}
	// The miss coalescer travels with the cache (an atomic.Pointer cannot appear
	// in the literal above); a clone shares the OWNER's coalescer, whose
	// lifecycle stays owner-only — a clone's Close does not stop it.
	clone.cscMissCoalescer.Store(c.cscMissCoalescer.Load())
	return clone
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *baseClient) clone() *baseClient {
	c.maintNotificationsManagerLock.RLock()
	maintNotificationsManager := c.maintNotificationsManager
	c.maintNotificationsManagerLock.RUnlock()

	clone := &baseClient{
		apClosed: c.apClosed,
		opt:      c.opt,
		connPool: c.connPool,
		// Pointer copy on purpose: the clone shares the parent's already-created
		// pipeline pool over the one shared pool set, rather than building its own.
		pipelinePool:                c.pipelinePool,
		pubSubPool:                  c.pubSubPool,
		onClose:                     c.onClose,
		pushProcessor:               c.pushProcessor,
		maintNotificationsManager:   maintNotificationsManager,
		streamingCredentialsManager: c.streamingCredentialsManager,
		himport:                     c.himport,
		csc:                         c.csc,
		// cscPoolHook and cscActive travel with the cache (read in processCached);
		// the owner-only fields — cscDrainHandle, cscOwnsCache — do not, so a clone's
		// Close never tears down the owner's resources.
		cscPoolHook:  c.cscPoolHook,
		cscActive:    c.cscActive,
		cscKeyPrefix: c.cscKeyPrefix,
		// cscRefreshQueue is SHARED (pointer copy), like cscPoolHook: processCached
		// calls signalDemand on it so a miss for a key still in the refresher's
		// window flushes that window early. Without the share a clone's field is
		// nil and signalDemand no-ops, so the clone's miss waits the full window
		// (#3965 F4). Lifecycle stays owner-only: signalDemand is a nil-safe,
		// non-blocking buffered send that does no I/O, and teardown keys off the
		// owner-only cscRefreshHandle/cscDrainHandle (both nil in a clone), so a
		// clone only SIGNALS the queue and never stops it — even a clone outliving
		// the owner's Close just sends into a buffered channel whose worker has
		// exited, which is harmless.
		cscRefreshQueue: c.cscRefreshQueue,
	}
	// A baseClient built without NewClient (e.g. internal CSC tests) has no
	// hook state; keep the zero mixin instead of nil-dereferencing in clone.
	if c.hooksMixin.state != nil {
		clone.hooksMixin = c.hooksMixin.clone()
	}
	// The miss coalescer travels with the cache (an atomic.Pointer cannot appear
	// in the literal above); a clone shares the OWNER's coalescer, whose
	// lifecycle stays owner-only — a clone's Close does not stop it.
	clone.cscMissCoalescer.Store(c.cscMissCoalescer.Load())
	return clone
}
```


---

### 🔹 Commit #09: `372b420c`
- **完整 Hash**: `372b420c5689d24e95583e04d695a3ad53d3e2f5`
- **說明 (Ground Truth)**: fix(cmd): accept RESP3 doubles in Cmd.Float64 (#4088)
- **變更檔案數**: 1

#### 📄 檔案: `command.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:823, E:1107, A:0) ➔ After(N:825, E:1110, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 3, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `strconv.FormatFloat (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `math.IsInf (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `toFloat32` ──[CALLS]──> `math.IsInf (External/Pkg)`
  • + [新增呼叫邊] `toFloat32` ──[CALLS]──> `float64 (External/Pkg)`
  • + [新增呼叫邊] `toFloat32` ──[CALLS]──> `strconv.FormatFloat (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `toFloat64()`
- **變更前簽章 (Before)**: `func toFloat64(val interface{})` (L832~L842)
- **變更後簽章 (After)**: `func toFloat64(val interface{})` (L844~L856)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func toFloat64(val interface{}) (float64, error) {
	switch val := val.(type) {
	case int64:
		return float64(val), nil
	case string:
		return strconv.ParseFloat(val, 64)
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Float64", val)
		return 0, err
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func toFloat64(val interface{}) (float64, error) {
	switch val := val.(type) {
	case float64:
		return val, nil
	case int64:
		return float64(val), nil
	case string:
		return strconv.ParseFloat(val, 64)
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Float64", val)
		return 0, err
	}
}
```

### 🔹 函式: `toFloat32()`
- **變更前簽章 (Before)**: `func toFloat32(val interface{})` (L808~L822)
- **變更後簽章 (After)**: `func toFloat32(val interface{})` (L809~L834)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func toFloat32(val interface{}) (float32, error) {
	switch val := val.(type) {
	case int64:
		return float32(val), nil
	case string:
		f, err := strconv.ParseFloat(val, 32)
		if err != nil {
			return 0, err
		}
		return float32(f), nil
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Float32", val)
		return 0, err
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func toFloat32(val interface{}) (float32, error) {
	switch val := val.(type) {
	case float64:
		// Return the range error that ParseFloat returns for a RESP2 bulk
		// string when a RESP3 double does not fit in a float32.
		if f := float32(val); math.IsInf(float64(f), 0) && !math.IsInf(val, 0) {
			return 0, &strconv.NumError{
				Func: "ParseFloat",
				Num:  strconv.FormatFloat(val, 'g', -1, 64),
				Err:  strconv.ErrRange,
			}
		}
		return float32(val), nil
	case int64:
		return float32(val), nil
	case string:
		f, err := strconv.ParseFloat(val, 32)
		if err != nil {
			return 0, err
		}
		return float32(f), nil
	default:
		err := fmt.Errorf("redis: unexpected type=%T for Float32", val)
		return 0, err
	}
}
```


---

### 🔹 Commit #10: `9bfbc24c`
- **完整 Hash**: `9bfbc24c9e90b919e515c458e2534405cf0bd183`
- **說明 (Ground Truth)**: fix(pubsub): avoid panics on Channel conflict and Ring empty subscribe (#3968)
- **變更檔案數**: 2

#### 📄 檔案: `pubsub.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:99, E:167, A:0) ➔ After(N:97, E:175, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 2, +Edges: 12, -Edges: 4, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `panic() [執行期恐慌/中斷]` (FUNCTION_DEF)
  • - [移除節點] `panic() [執行期恐慌/中斷]` (FUNCTION_DEF)
  • + [新增呼叫邊] `PubSub.Channel` ──[CALLS]──> `c.mu.Lock (External/Pkg)`
  • + [新增呼叫邊] `PubSub.Channel` ──[CALLS]──> `c.mu.Unlock (External/Pkg)`
  • + [新增呼叫邊] `PubSub.Channel` ──[CALLS]──> `internal.Logger.Printf (External/Pkg)`
  • + [新增呼叫邊] `PubSub.Channel` ──[CALLS]──> `context.Background (External/Pkg)`
  • + [新增呼叫邊] `PubSub.Channel` ──[CALLS]──> `make (External/Pkg)`
  • + [新增呼叫邊] `PubSub.Channel` ──[CALLS]──> `close (External/Pkg)`
  • + [新增呼叫邊] `PubSub.ChannelWithSubscriptions` ──[CALLS]──> `c.mu.Lock (External/Pkg)`
  • + [新增呼叫邊] `PubSub.ChannelWithSubscriptions` ──[CALLS]──> `c.mu.Unlock (External/Pkg)`
  • + [新增呼叫邊] `PubSub.ChannelWithSubscriptions` ──[CALLS]──> `internal.Logger.Printf (External/Pkg)`
  • + [新增呼叫邊] `PubSub.ChannelWithSubscriptions` ──[CALLS]──> `context.Background (External/Pkg)`
  • + [新增呼叫邊] `PubSub.ChannelWithSubscriptions` ──[CALLS]──> `make (External/Pkg)`
  • + [新增呼叫邊] `PubSub.ChannelWithSubscriptions` ──[CALLS]──> `close (External/Pkg)`
  • - [移除呼叫邊] `PubSub.Channel` ──[CALLS]──> `fmt.Errorf (External/Pkg)`
  • _... 以及其餘 3 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `PubSub.ChannelWithSubscriptions()`
- **變更前簽章 (Before)**: `func PubSub.ChannelWithSubscriptions(opts ...ChannelOption)` (L597~L607)
- **變更後簽章 (After)**: `func PubSub.ChannelWithSubscriptions(opts ...ChannelOption)` (L634~L663)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *PubSub) ChannelWithSubscriptions(opts ...ChannelOption) <-chan interface{} {
	c.chOnce.Do(func() {
		c.allCh = newChannel(c, opts...)
		c.allCh.initAllChan()
	})
	if c.allCh == nil {
		err := fmt.Errorf("redis: ChannelWithSubscriptions can't be called after Channel")
		panic(err)
	}
	return c.allCh.allCh
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *PubSub) ChannelWithSubscriptions(opts ...ChannelOption) <-chan interface{} {
	c.mu.Lock()
	if c.stickyErr != nil && !c.closed {
		err := c.stickyErr
		c.mu.Unlock()
		internal.Logger.Printf(context.Background(),
			"redis: ChannelWithSubscriptions returning closed channel due to sticky error: %s", err)
		ch := make(chan interface{})
		close(ch)
		return ch
	}
	c.mu.Unlock()

	c.chOnce.Do(func() {
		c.allCh = newChannel(c, opts...)
		c.allCh.initAllChan()
	})
	if c.allCh == nil {
		// Already using Channel — return a closed channel instead of panicking
		// so callers can recover (issue #3761).
		// Use Background: getContext reads c.cmd which the other channel's
		// Receive loop may write concurrently (data race under -race).
		internal.Logger.Printf(context.Background(),
			"redis: ChannelWithSubscriptions can't be called after Channel")
		ch := make(chan interface{})
		close(ch)
		return ch
	}
	return c.allCh.allCh
}
```

### 🔹 函式: `PubSub.Channel()`
- **變更前簽章 (Before)**: `func PubSub.Channel(opts ...ChannelOption)` (L572~L582)
- **變更後簽章 (After)**: `func PubSub.Channel(opts ...ChannelOption)` (L585~L614)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *PubSub) Channel(opts ...ChannelOption) <-chan *Message {
	c.chOnce.Do(func() {
		c.msgCh = newChannel(c, opts...)
		c.msgCh.initMsgChan()
	})
	if c.msgCh == nil {
		err := fmt.Errorf("redis: Channel can't be called after ChannelWithSubscriptions")
		panic(err)
	}
	return c.msgCh.msgCh
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *PubSub) Channel(opts ...ChannelOption) <-chan *Message {
	c.mu.Lock()
	if c.stickyErr != nil && !c.closed {
		err := c.stickyErr
		c.mu.Unlock()
		internal.Logger.Printf(context.Background(),
			"redis: Channel returning closed channel due to sticky error: %s", err)
		ch := make(chan *Message)
		close(ch)
		return ch
	}
	c.mu.Unlock()

	c.chOnce.Do(func() {
		c.msgCh = newChannel(c, opts...)
		c.msgCh.initMsgChan()
	})
	if c.msgCh == nil {
		// Already using ChannelWithSubscriptions — return a closed channel
		// instead of panicking so callers can recover (issue #3761).
		// Use Background: getContext reads c.cmd which the other channel's
		// Receive loop may write concurrently (data race under -race).
		internal.Logger.Printf(context.Background(),
			"redis: Channel can't be called after ChannelWithSubscriptions")
		ch := make(chan *Message)
		close(ch)
		return ch
	}
	return c.msgCh.msgCh
}
```

### 🔹 函式: `PubSub.conn()`
- **變更前簽章 (Before)**: `func PubSub.conn(ctx context.Context, newChannels []string)` (L74~L114)
- **變更後簽章 (After)**: `func PubSub.conn(ctx context.Context, newChannels []string)` (L79~L122)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *PubSub) conn(ctx context.Context, newChannels []string) (*pool.Conn, error) {
	if c.closed {
		return nil, pool.ErrClosed
	}
	if c.cn != nil {
		return c.cn, nil
	}

	if c.opt.Addr == "" {
		// TODO(maintenanceNotifications):
		// this is probably cluster client
		// c.newConn will ignore the addr argument
		// will be changed when we have maintenanceNotifications upgrades for cluster clients
		c.opt.Addr = internal.RedisNull
	}

	// Include c.schannels so reconnect-time routing of an SSubscribe-only
	// PubSub picks the slot owner (channels[0] in ClusterClient.pubSub()'s
	// newConn closure) instead of a random node.
	// See https://github.com/redis/go-redis/issues/3806.
	// c.patterns is intentionally NOT included: patterns are not slot-
	// addressable, and adding them would force PSubscribe-only PubSubs to
	// pin to a single node based on pattern-string hash, regressing the
	// existing random-node behaviour.
	channels := slices.Collect(maps.Keys(c.channels))
	channels = append(channels, slices.Collect(maps.Keys(c.schannels))...)
	channels = append(channels, newChannels...)

	cn, err := c.newConn(ctx, c.opt.Addr, channels)
	if err != nil {
		return nil, err
	}

	if err := c.resubscribe(ctx, cn); err != nil {
		_ = c.closeConn(cn)
		return nil, err
	}

	c.cn = cn
	return cn, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *PubSub) conn(ctx context.Context, newChannels []string) (*pool.Conn, error) {
	if c.closed {
		return nil, pool.ErrClosed
	}
	if c.stickyErr != nil {
		return nil, c.stickyErr
	}
	if c.cn != nil {
		return c.cn, nil
	}

	if c.opt.Addr == "" {
		// TODO(maintenanceNotifications):
		// this is probably cluster client
		// c.newConn will ignore the addr argument
		// will be changed when we have maintenanceNotifications upgrades for cluster clients
		c.opt.Addr = internal.RedisNull
	}

	// Include c.schannels so reconnect-time routing of an SSubscribe-only
	// PubSub picks the slot owner (channels[0] in ClusterClient.pubSub()'s
	// newConn closure) instead of a random node.
	// See https://github.com/redis/go-redis/issues/3806.
	// c.patterns is intentionally NOT included: patterns are not slot-
	// addressable, and adding them would force PSubscribe-only PubSubs to
	// pin to a single node based on pattern-string hash, regressing the
	// existing random-node behaviour.
	channels := slices.Collect(maps.Keys(c.channels))
	channels = append(channels, slices.Collect(maps.Keys(c.schannels))...)
	channels = append(channels, newChannels...)

	cn, err := c.newConn(ctx, c.opt.Addr, channels)
	if err != nil {
		return nil, err
	}

	if err := c.resubscribe(ctx, cn); err != nil {
		_ = c.closeConn(cn)
		return nil, err
	}

	c.cn = cn
	return cn, nil
}
```


#### 📄 檔案: `ring.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:136, E:171, A:0) ➔ After(N:131, E:176, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 6, +Edges: 11, -Edges: 6, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Ring.failedPubSub` (FUNCTION_DEF)
  • - [移除節點] `panic() [執行期恐慌/中斷]` (FUNCTION_DEF)
  • - [移除節點] `panic() [執行期恐慌/中斷]` (FUNCTION_DEF)
  • - [移除節點] `panic() [執行期恐慌/中斷]` (FUNCTION_DEF)
  • - [移除節點] `panic() [執行期恐慌/中斷]` (FUNCTION_DEF)
  • - [移除節點] `panic() [執行期恐慌/中斷]` (FUNCTION_DEF)
  • - [移除節點] `panic() [執行期恐慌/中斷]` (FUNCTION_DEF)
  • + [新增呼叫邊] `Ring.failedPubSub` ──[CALLS]──> `fmt.Errorf (External/Pkg)`
  • + [新增呼叫邊] `Ring.failedPubSub` ──[CALLS]──> `internal.Logger.Printf (External/Pkg)`
  • + [新增呼叫邊] `Ring.failedPubSub` ──[CALLS]──> `context.Background (External/Pkg)`
  • + [新增呼叫邊] `Ring.failedPubSub` ──[CALLS]──> `RingOptions.clientOptions`
  • + [新增呼叫邊] `Ring.failedPubSub` ──[CALLS]──> `RingOptions.init`
  • + [新增呼叫邊] `Ring.Subscribe` ──[CALLS]──> `Ring.failedPubSub`
  • + [新增呼叫邊] `Ring.Subscribe` ──[CALLS]──> `fmt.Errorf (External/Pkg)`
  • + [新增呼叫邊] `Ring.PSubscribe` ──[CALLS]──> `Ring.failedPubSub`
  • _... 以及其餘 9 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Ring.PSubscribe()`
- **變更前簽章 (Before)**: `func Ring.PSubscribe(ctx context.Context, channels ...string)` (L749~L760)
- **變更後簽章 (After)**: `func Ring.PSubscribe(ctx context.Context, channels ...string)` (L767~L777)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Ring) PSubscribe(ctx context.Context, channels ...string) *PubSub {
	if len(channels) == 0 {
		panic("at least one channel is required")
	}

	shard, err := c.sharding.GetByKey(channels[0])
	if err != nil {
		// TODO: return PubSub with sticky error
		panic(err)
	}
	return shard.Client.PSubscribe(ctx, channels...)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Ring) PSubscribe(ctx context.Context, channels ...string) *PubSub {
	if len(channels) == 0 {
		return c.failedPubSub(fmt.Errorf("redis: at least one channel is required"))
	}

	shard, err := c.sharding.GetByKey(channels[0])
	if err != nil {
		return c.failedPubSub(err)
	}
	return shard.Client.PSubscribe(ctx, channels...)
}
```

### 🔹 函式: `Ring.SSubscribe()`
- **變更前簽章 (Before)**: `func Ring.SSubscribe(ctx context.Context, channels ...string)` (L763~L773)
- **變更後簽章 (After)**: `func Ring.SSubscribe(ctx context.Context, channels ...string)` (L782~L791)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Ring) SSubscribe(ctx context.Context, channels ...string) *PubSub {
	if len(channels) == 0 {
		panic("at least one channel is required")
	}
	shard, err := c.sharding.GetByKey(channels[0])
	if err != nil {
		// TODO: return PubSub with sticky error
		panic(err)
	}
	return shard.Client.SSubscribe(ctx, channels...)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Ring) SSubscribe(ctx context.Context, channels ...string) *PubSub {
	if len(channels) == 0 {
		return c.failedPubSub(fmt.Errorf("redis: at least one channel is required"))
	}
	shard, err := c.sharding.GetByKey(channels[0])
	if err != nil {
		return c.failedPubSub(err)
	}
	return shard.Client.SSubscribe(ctx, channels...)
}
```

### 🔹 函式: `Ring.Subscribe()`
- **變更前簽章 (Before)**: `func Ring.Subscribe(ctx context.Context, channels ...string)` (L735~L746)
- **變更後簽章 (After)**: `func Ring.Subscribe(ctx context.Context, channels ...string)` (L752~L762)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Ring) Subscribe(ctx context.Context, channels ...string) *PubSub {
	if len(channels) == 0 {
		panic("at least one channel is required")
	}

	shard, err := c.sharding.GetByKey(channels[0])
	if err != nil {
		// TODO: return PubSub with sticky error
		panic(err)
	}
	return shard.Client.Subscribe(ctx, channels...)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Ring) Subscribe(ctx context.Context, channels ...string) *PubSub {
	if len(channels) == 0 {
		return c.failedPubSub(fmt.Errorf("redis: at least one channel is required"))
	}

	shard, err := c.sharding.GetByKey(channels[0])
	if err != nil {
		return c.failedPubSub(err)
	}
	return shard.Client.Subscribe(ctx, channels...)
}
```


---

### 🔹 Commit #11: `97b7efde`
- **完整 Hash**: `97b7efdeee929848092058628cfc0e2abfc159bb`
- **說明 (Ground Truth)**: fix(command): read past error elements in IntSliceCmd (#4071)
- **變更檔案數**: 3

#### 📄 檔案: `command.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:821, E:1106, A:0) ➔ After(N:823, E:1107, A:0)
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
  • + [新增節點] `isRedisError (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `elemErr` (MODULE_STATE)
  • + [新增呼叫邊] `IntSliceCmd.readReply` ──[CALLS]──> `isRedisError (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `IntSliceCmd.readReply()`
- **變更前簽章 (Before)**: `func IntSliceCmd.readReply(rd *proto.Reader)` (L1578~L1595)
- **變更後簽章 (After)**: `func IntSliceCmd.readReply(rd *proto.Reader)` (L1578~L1605)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (cmd *IntSliceCmd) readReply(rd *proto.Reader) error {
	n, err := rd.ReadArrayLen()
	if err != nil {
		return err
	}
	cmd.val = make([]int64, n)
	for i := 0; i < len(cmd.val); i++ {
		switch num, err := rd.ReadInt(); {
		case err == Nil:
			cmd.val[i] = 0
		case err != nil:
			return err
		default:
			cmd.val[i] = num
		}
	}
	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (cmd *IntSliceCmd) readReply(rd *proto.Reader) error {
	n, err := rd.ReadArrayLen()
	if err != nil {
		return err
	}
	cmd.val = make([]int64, n)
	var elemErr error
	for i := 0; i < len(cmd.val); i++ {
		switch num, err := rd.ReadInt(); {
		case err == Nil:
			cmd.val[i] = 0
		case err != nil:
			if !isRedisError(err) {
				return err
			}
			// TS.MADD and CMS.INCRBY report a rejected item as an error
			// element and still answer for the items after it. The element
			// is a complete frame, so read on and return the first one once
			// the whole array is consumed.
			if elemErr == nil {
				elemErr = err
			}
		default:
			cmd.val[i] = num
		}
	}
	return elemErr
}
```


#### 📄 檔案: `probabilistic.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:148, E:240, A:0) ➔ After(N:148, E:240, A:0)
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

#### 📄 檔案: `timeseries_commands.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:96, E:186, A:0) ➔ After(N:96, E:186, A:0)
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

### 🔹 Commit #12: `5fcaf27e`
- **完整 Hash**: `5fcaf27e1a591e27838918257408f68c08f6a248`
- **說明 (Ground Truth)**: fix(search): initialize options in NewDropIndexBuilder to prevent panic (#4105)
- **變更檔案數**: 1

#### 📄 檔案: `search_builders.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:130, E:68, A:0) ➔ After(N:130, E:68, A:0)
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

### 🔹 函式: `Client.NewDropIndexBuilder()`
- **變更前簽章 (Before)**: `func Client.NewDropIndexBuilder(ctx context.Context, index string)` (L564~L566)
- **變更後簽章 (After)**: `func Client.NewDropIndexBuilder(ctx context.Context, index string)` (L564~L566)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Client) NewDropIndexBuilder(ctx context.Context, index string) *DropIndexBuilder {
	return &DropIndexBuilder{c: c, ctx: ctx, index: index}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Client) NewDropIndexBuilder(ctx context.Context, index string) *DropIndexBuilder {
	return &DropIndexBuilder{c: c, ctx: ctx, index: index, options: &FTDropIndexOptions{}}
}
```


---

### 🔹 Commit #13: `9bb5c7c2`
- **完整 Hash**: `9bb5c7c2c6ad6c0b10b2a897d4b4b9c272f4d8c9`
- **說明 (Ground Truth)**: fix(cluster): support skip_verify query parameter in ParseClusterURL (#4106)
- **變更檔案數**: 1

#### 📄 檔案: `osscluster.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:343, E:552, A:0) ➔ After(N:343, E:552, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
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

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `setupClusterQueryParams()`
- **變更前簽章 (Before)**: `func setupClusterQueryParams(u *url.URL, o *ClusterOptions)` (L392~L451)
- **變更後簽章 (After)**: `func setupClusterQueryParams(u *url.URL, o *ClusterOptions)` (L393~L455)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func setupClusterQueryParams(u *url.URL, o *ClusterOptions) (*ClusterOptions, error) {
	q := queryOptions{q: u.Query()}

	o.Protocol = q.int("protocol")
	o.ClientName = q.string("client_name")
	o.MaxRedirects = q.int("max_redirects")
	o.ReadOnly = q.bool("read_only")
	o.RouteByLatency = q.bool("route_by_latency")
	o.RouteByLatencyTolerance = q.duration("route_by_latency_tolerance")
	o.RouteRandomly = q.bool("route_randomly")
	o.MaxRetries = q.int("max_retries")
	o.MinRetryBackoff = q.duration("min_retry_backoff")
	o.MaxRetryBackoff = q.duration("max_retry_backoff")
	o.DialTimeout = q.duration("dial_timeout")
	o.DialerRetries = q.int("dialer_retries")
	o.DialerRetryTimeout = q.duration("dialer_retry_timeout")
	o.ReadTimeout = q.duration("read_timeout")
	o.WriteTimeout = q.duration("write_timeout")
	o.PoolFIFO = q.bool("pool_fifo")
	o.PoolSize = q.int("pool_size")
	o.MaxConcurrentDials = q.int("max_concurrent_dials")
	o.MinIdleConns = q.int("min_idle_conns")
	o.MaxIdleConns = q.int("max_idle_conns")
	o.MaxActiveConns = q.int("max_active_conns")
	// Pipeline pool (per node, created by default): allow URL opt-out
	// (pipeline_pool_size=-1) / tuning, else rejected as unexpected options.
	o.PipelinePoolSize = q.int("pipeline_pool_size")
	o.PipelineMinIdleConns = q.int("pipeline_min_idle_conns")
	o.PipelineReadBufferSize = q.int("pipeline_read_buffer_size")
	o.PipelineWriteBufferSize = q.int("pipeline_write_buffer_size")
	o.PoolTimeout = q.duration("pool_timeout")
	o.ConnMaxLifetime = q.duration("conn_max_lifetime")
	if q.has("conn_max_lifetime_jitter") {
		o.ConnMaxLifetimeJitter = min(q.duration("conn_max_lifetime_jitter"), o.ConnMaxLifetime)
	}
	o.ConnMaxIdleTime = q.duration("conn_max_idle_time")
	o.FailingTimeoutSeconds = q.int("failing_timeout_seconds")

	if q.err != nil {
		return nil, q.err
	}

	// addr can be specified as many times as needed
	addrs := q.strings("addr")
	for _, addr := range addrs {
		h, p, err := net.SplitHostPort(addr)
		if err != nil || h == "" || p == "" {
			return nil, fmt.Errorf("redis: unable to parse addr param: %s", addr)
		}

		o.Addrs = append(o.Addrs, net.JoinHostPort(h, p))
	}

	// any parameters left?
	if r := q.remaining(); len(r) > 0 {
		return nil, fmt.Errorf("redis: unexpected option: %s", strings.Join(r, ", "))
	}

	return o, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func setupClusterQueryParams(u *url.URL, o *ClusterOptions) (*ClusterOptions, error) {
	q := queryOptions{q: u.Query()}

	o.Protocol = q.int("protocol")
	o.ClientName = q.string("client_name")
	o.MaxRedirects = q.int("max_redirects")
	o.ReadOnly = q.bool("read_only")
	o.RouteByLatency = q.bool("route_by_latency")
	o.RouteByLatencyTolerance = q.duration("route_by_latency_tolerance")
	o.RouteRandomly = q.bool("route_randomly")
	o.MaxRetries = q.int("max_retries")
	o.MinRetryBackoff = q.duration("min_retry_backoff")
	o.MaxRetryBackoff = q.duration("max_retry_backoff")
	o.DialTimeout = q.duration("dial_timeout")
	o.DialerRetries = q.int("dialer_retries")
	o.DialerRetryTimeout = q.duration("dialer_retry_timeout")
	o.ReadTimeout = q.duration("read_timeout")
	o.WriteTimeout = q.duration("write_timeout")
	o.PoolFIFO = q.bool("pool_fifo")
	o.PoolSize = q.int("pool_size")
	o.MaxConcurrentDials = q.int("max_concurrent_dials")
	o.MinIdleConns = q.int("min_idle_conns")
	o.MaxIdleConns = q.int("max_idle_conns")
	o.MaxActiveConns = q.int("max_active_conns")
	// Pipeline pool (per node, created by default): allow URL opt-out
	// (pipeline_pool_size=-1) / tuning, else rejected as unexpected options.
	o.PipelinePoolSize = q.int("pipeline_pool_size")
	o.PipelineMinIdleConns = q.int("pipeline_min_idle_conns")
	o.PipelineReadBufferSize = q.int("pipeline_read_buffer_size")
	o.PipelineWriteBufferSize = q.int("pipeline_write_buffer_size")
	o.PoolTimeout = q.duration("pool_timeout")
	o.ConnMaxLifetime = q.duration("conn_max_lifetime")
	if q.has("conn_max_lifetime_jitter") {
		o.ConnMaxLifetimeJitter = min(q.duration("conn_max_lifetime_jitter"), o.ConnMaxLifetime)
	}
	o.ConnMaxIdleTime = q.duration("conn_max_idle_time")
	o.FailingTimeoutSeconds = q.int("failing_timeout_seconds")
	if o.TLSConfig != nil && q.has("skip_verify") {
		o.TLSConfig.InsecureSkipVerify = q.bool("skip_verify")
	}

	if q.err != nil {
		return nil, q.err
	}

	// addr can be specified as many times as needed
	addrs := q.strings("addr")
	for _, addr := range addrs {
		h, p, err := net.SplitHostPort(addr)
		if err != nil || h == "" || p == "" {
			return nil, fmt.Errorf("redis: unable to parse addr param: %s", addr)
		}

		o.Addrs = append(o.Addrs, net.JoinHostPort(h, p))
	}

	// any parameters left?
	if r := q.remaining(); len(r) > 0 {
		return nil, fmt.Errorf("redis: unexpected option: %s", strings.Join(r, ", "))
	}

	return o, nil
}
```


---

### 🔹 Commit #14: `a4a376ad`
- **完整 Hash**: `a4a376ad5554696f4da794c4f721a57d6b7ff0dd`
- **說明 (Ground Truth)**: fix(command): put IGNORE before LABELS (#4160)
- **變更檔案數**: 1

#### 📄 檔案: `timeseries_commands.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:96, E:186, A:0) ➔ After(N:96, E:186, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 5, ΔTrans: 0
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

### 🔹 函式: `cmdable.TSAlter()`
- **變更前簽章 (Before)**: `func cmdable.TSAlter(ctx context.Context, key string, options *TSAlterOptions)` (L409~L434)
- **變更後簽章 (After)**: `func cmdable.TSAlter(ctx context.Context, key string, options *TSAlterOptions)` (L409~L434)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c cmdable) TSAlter(ctx context.Context, key string, options *TSAlterOptions) *StatusCmd {
	args := []interface{}{"TS.ALTER", key}
	if options != nil {
		if options.Retention != 0 {
			args = append(args, "RETENTION", options.Retention)
		}
		if options.ChunkSize != 0 {
			args = append(args, "CHUNK_SIZE", options.ChunkSize)
		}
		if options.DuplicatePolicy != "" {
			args = append(args, "DUPLICATE_POLICY", options.DuplicatePolicy)
		}
		if options.Labels != nil {
			args = append(args, "LABELS")
			for label, value := range options.Labels {
				args = append(args, label, value)
			}
		}
		if options.IgnoreMaxTimeDiff != 0 || options.IgnoreMaxValDiff != 0 {
			args = append(args, "IGNORE", options.IgnoreMaxTimeDiff, options.IgnoreMaxValDiff)
		}
	}
	cmd := NewStatusCmd(ctx, args...)
	_ = c(ctx, cmd)
	return cmd
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c cmdable) TSAlter(ctx context.Context, key string, options *TSAlterOptions) *StatusCmd {
	args := []interface{}{"TS.ALTER", key}
	if options != nil {
		if options.Retention != 0 {
			args = append(args, "RETENTION", options.Retention)
		}
		if options.ChunkSize != 0 {
			args = append(args, "CHUNK_SIZE", options.ChunkSize)
		}
		if options.DuplicatePolicy != "" {
			args = append(args, "DUPLICATE_POLICY", options.DuplicatePolicy)
		}
		if options.IgnoreMaxTimeDiff != 0 || options.IgnoreMaxValDiff != 0 {
			args = append(args, "IGNORE", options.IgnoreMaxTimeDiff, options.IgnoreMaxValDiff)
		}
		if options.Labels != nil {
			args = append(args, "LABELS")
			for label, value := range options.Labels {
				args = append(args, label, value)
			}
		}
	}
	cmd := NewStatusCmd(ctx, args...)
	_ = c(ctx, cmd)
	return cmd
}
```

### 🔹 函式: `cmdable.TSDecrByWithArgs()`
- **變更前簽章 (Before)**: `func cmdable.TSDecrByWithArgs(ctx context.Context, key string, timestamp float64, options *TSIncrDecrOptions)` (L520~L551)
- **變更後簽章 (After)**: `func cmdable.TSDecrByWithArgs(ctx context.Context, key string, timestamp float64, options *TSIncrDecrOptions)` (L520~L551)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c cmdable) TSDecrByWithArgs(ctx context.Context, key string, timestamp float64, options *TSIncrDecrOptions) *IntCmd {
	args := []interface{}{"TS.DECRBY", key, timestamp}
	if options != nil {
		if options.Timestamp != 0 {
			args = append(args, "TIMESTAMP", options.Timestamp)
		}
		if options.Retention != 0 {
			args = append(args, "RETENTION", options.Retention)
		}
		if options.ChunkSize != 0 {
			args = append(args, "CHUNK_SIZE", options.ChunkSize)
		}
		if options.Uncompressed {
			args = append(args, "UNCOMPRESSED")
		}
		if options.DuplicatePolicy != "" {
			args = append(args, "DUPLICATE_POLICY", options.DuplicatePolicy)
		}
		if options.Labels != nil {
			args = append(args, "LABELS")
			for label, value := range options.Labels {
				args = append(args, label, value)
			}
		}
		if options.IgnoreMaxTimeDiff != 0 || options.IgnoreMaxValDiff != 0 {
			args = append(args, "IGNORE", options.IgnoreMaxTimeDiff, options.IgnoreMaxValDiff)
		}
	}
	cmd := NewIntCmd(ctx, args...)
	_ = c(ctx, cmd)
	return cmd
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c cmdable) TSDecrByWithArgs(ctx context.Context, key string, timestamp float64, options *TSIncrDecrOptions) *IntCmd {
	args := []interface{}{"TS.DECRBY", key, timestamp}
	if options != nil {
		if options.Timestamp != 0 {
			args = append(args, "TIMESTAMP", options.Timestamp)
		}
		if options.Retention != 0 {
			args = append(args, "RETENTION", options.Retention)
		}
		if options.ChunkSize != 0 {
			args = append(args, "CHUNK_SIZE", options.ChunkSize)
		}
		if options.Uncompressed {
			args = append(args, "UNCOMPRESSED")
		}
		if options.DuplicatePolicy != "" {
			args = append(args, "DUPLICATE_POLICY", options.DuplicatePolicy)
		}
		if options.IgnoreMaxTimeDiff != 0 || options.IgnoreMaxValDiff != 0 {
			args = append(args, "IGNORE", options.IgnoreMaxTimeDiff, options.IgnoreMaxValDiff)
		}
		if options.Labels != nil {
			args = append(args, "LABELS")
			for label, value := range options.Labels {
				args = append(args, label, value)
			}
		}
	}
	cmd := NewIntCmd(ctx, args...)
	_ = c(ctx, cmd)
	return cmd
}
```

### 🔹 函式: `cmdable.TSIncrByWithArgs()`
- **變更前簽章 (Before)**: `func cmdable.TSIncrByWithArgs(ctx context.Context, key string, timestamp float64, options *TSIncrDecrOptions)` (L474~L505)
- **變更後簽章 (After)**: `func cmdable.TSIncrByWithArgs(ctx context.Context, key string, timestamp float64, options *TSIncrDecrOptions)` (L474~L505)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c cmdable) TSIncrByWithArgs(ctx context.Context, key string, timestamp float64, options *TSIncrDecrOptions) *IntCmd {
	args := []interface{}{"TS.INCRBY", key, timestamp}
	if options != nil {
		if options.Timestamp != 0 {
			args = append(args, "TIMESTAMP", options.Timestamp)
		}
		if options.Retention != 0 {
			args = append(args, "RETENTION", options.Retention)
		}
		if options.ChunkSize != 0 {
			args = append(args, "CHUNK_SIZE", options.ChunkSize)
		}
		if options.Uncompressed {
			args = append(args, "UNCOMPRESSED")
		}
		if options.DuplicatePolicy != "" {
			args = append(args, "DUPLICATE_POLICY", options.DuplicatePolicy)
		}
		if options.Labels != nil {
			args = append(args, "LABELS")
			for label, value := range options.Labels {
				args = append(args, label, value)
			}
		}
		if options.IgnoreMaxTimeDiff != 0 || options.IgnoreMaxValDiff != 0 {
			args = append(args, "IGNORE", options.IgnoreMaxTimeDiff, options.IgnoreMaxValDiff)
		}
	}
	cmd := NewIntCmd(ctx, args...)
	_ = c(ctx, cmd)
	return cmd
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c cmdable) TSIncrByWithArgs(ctx context.Context, key string, timestamp float64, options *TSIncrDecrOptions) *IntCmd {
	args := []interface{}{"TS.INCRBY", key, timestamp}
	if options != nil {
		if options.Timestamp != 0 {
			args = append(args, "TIMESTAMP", options.Timestamp)
		}
		if options.Retention != 0 {
			args = append(args, "RETENTION", options.Retention)
		}
		if options.ChunkSize != 0 {
			args = append(args, "CHUNK_SIZE", options.ChunkSize)
		}
		if options.Uncompressed {
			args = append(args, "UNCOMPRESSED")
		}
		if options.DuplicatePolicy != "" {
			args = append(args, "DUPLICATE_POLICY", options.DuplicatePolicy)
		}
		if options.IgnoreMaxTimeDiff != 0 || options.IgnoreMaxValDiff != 0 {
			args = append(args, "IGNORE", options.IgnoreMaxTimeDiff, options.IgnoreMaxValDiff)
		}
		if options.Labels != nil {
			args = append(args, "LABELS")
			for label, value := range options.Labels {
				args = append(args, label, value)
			}
		}
	}
	cmd := NewIntCmd(ctx, args...)
	_ = c(ctx, cmd)
	return cmd
}
```

### 🔹 函式: `cmdable.TSCreateWithArgs()`
- **變更前簽章 (Before)**: `func cmdable.TSCreateWithArgs(ctx context.Context, key string, options *TSOptions)` (L374~L403)
- **變更後簽章 (After)**: `func cmdable.TSCreateWithArgs(ctx context.Context, key string, options *TSOptions)` (L374~L403)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c cmdable) TSCreateWithArgs(ctx context.Context, key string, options *TSOptions) *StatusCmd {
	args := []interface{}{"TS.CREATE", key}
	if options != nil {
		if options.Retention != 0 {
			args = append(args, "RETENTION", options.Retention)
		}
		if options.ChunkSize != 0 {
			args = append(args, "CHUNK_SIZE", options.ChunkSize)
		}
		if options.Encoding != "" {
			args = append(args, "ENCODING", options.Encoding)
		}

		if options.DuplicatePolicy != "" {
			args = append(args, "DUPLICATE_POLICY", options.DuplicatePolicy)
		}
		if options.Labels != nil {
			args = append(args, "LABELS")
			for label, value := range options.Labels {
				args = append(args, label, value)
			}
		}
		if options.IgnoreMaxTimeDiff != 0 || options.IgnoreMaxValDiff != 0 {
			args = append(args, "IGNORE", options.IgnoreMaxTimeDiff, options.IgnoreMaxValDiff)
		}
	}
	cmd := NewStatusCmd(ctx, args...)
	_ = c(ctx, cmd)
	return cmd
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c cmdable) TSCreateWithArgs(ctx context.Context, key string, options *TSOptions) *StatusCmd {
	args := []interface{}{"TS.CREATE", key}
	if options != nil {
		if options.Retention != 0 {
			args = append(args, "RETENTION", options.Retention)
		}
		if options.ChunkSize != 0 {
			args = append(args, "CHUNK_SIZE", options.ChunkSize)
		}
		if options.Encoding != "" {
			args = append(args, "ENCODING", options.Encoding)
		}

		if options.DuplicatePolicy != "" {
			args = append(args, "DUPLICATE_POLICY", options.DuplicatePolicy)
		}
		if options.IgnoreMaxTimeDiff != 0 || options.IgnoreMaxValDiff != 0 {
			args = append(args, "IGNORE", options.IgnoreMaxTimeDiff, options.IgnoreMaxValDiff)
		}
		if options.Labels != nil {
			args = append(args, "LABELS")
			for label, value := range options.Labels {
				args = append(args, label, value)
			}
		}
	}
	cmd := NewStatusCmd(ctx, args...)
	_ = c(ctx, cmd)
	return cmd
}
```

### 🔹 函式: `cmdable.TSAddWithArgs()`
- **變更前簽章 (Before)**: `func cmdable.TSAddWithArgs(ctx context.Context, key string, timestamp interface{}, value float64, options *TSOptions)` (L330~L359)
- **變更後簽章 (After)**: `func cmdable.TSAddWithArgs(ctx context.Context, key string, timestamp interface{}, value float64, options *TSOptions)` (L330~L359)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c cmdable) TSAddWithArgs(ctx context.Context, key string, timestamp interface{}, value float64, options *TSOptions) *IntCmd {
	args := []interface{}{"TS.ADD", key, timestamp, value}
	if options != nil {
		if options.Retention != 0 {
			args = append(args, "RETENTION", options.Retention)
		}
		if options.ChunkSize != 0 {
			args = append(args, "CHUNK_SIZE", options.ChunkSize)
		}
		if options.Encoding != "" {
			args = append(args, "ENCODING", options.Encoding)
		}

		if options.DuplicatePolicy != "" {
			args = append(args, "DUPLICATE_POLICY", options.DuplicatePolicy)
		}
		if options.Labels != nil {
			args = append(args, "LABELS")
			for label, value := range options.Labels {
				args = append(args, label, value)
			}
		}
		if options.IgnoreMaxTimeDiff != 0 || options.IgnoreMaxValDiff != 0 {
			args = append(args, "IGNORE", options.IgnoreMaxTimeDiff, options.IgnoreMaxValDiff)
		}
	}
	cmd := NewIntCmd(ctx, args...)
	_ = c(ctx, cmd)
	return cmd
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c cmdable) TSAddWithArgs(ctx context.Context, key string, timestamp interface{}, value float64, options *TSOptions) *IntCmd {
	args := []interface{}{"TS.ADD", key, timestamp, value}
	if options != nil {
		if options.Retention != 0 {
			args = append(args, "RETENTION", options.Retention)
		}
		if options.ChunkSize != 0 {
			args = append(args, "CHUNK_SIZE", options.ChunkSize)
		}
		if options.Encoding != "" {
			args = append(args, "ENCODING", options.Encoding)
		}

		if options.DuplicatePolicy != "" {
			args = append(args, "DUPLICATE_POLICY", options.DuplicatePolicy)
		}
		if options.IgnoreMaxTimeDiff != 0 || options.IgnoreMaxValDiff != 0 {
			args = append(args, "IGNORE", options.IgnoreMaxTimeDiff, options.IgnoreMaxValDiff)
		}
		if options.Labels != nil {
			args = append(args, "LABELS")
			for label, value := range options.Labels {
				args = append(args, label, value)
			}
		}
	}
	cmd := NewIntCmd(ctx, args...)
	_ = c(ctx, cmd)
	return cmd
}
```


---

### 🔹 Commit #15: `b1cc2f6c`
- **完整 Hash**: `b1cc2f6cebdd701f7840afafef4fcda3ce489629`
- **說明 (Ground Truth)**: fix(auth): send AUTH for a username with an empty password (#4161)
- **變更檔案數**: 3

#### 📄 檔案: `commands.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:141, E:215, A:0) ➔ After(N:141, E:215, A:0)
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

### 🔹 函式: `statefulCmdable.Hello()`
- **變更前簽章 (Before)**: `func statefulCmdable.Hello(ctx context.Context,
	ver int, username, password, clientName string,
)` (L361~L379)
- **變更後簽章 (After)**: `func statefulCmdable.Hello(ctx context.Context,
	ver int, username, password, clientName string,
)` (L361~L378)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c statefulCmdable) Hello(ctx context.Context,
	ver int, username, password, clientName string,
) *MapStringInterfaceCmd {
	args := make([]interface{}, 0, 7)
	args = append(args, "hello", ver)
	if password != "" {
		if username != "" {
			args = append(args, "auth", username, password)
		} else {
			args = append(args, "auth", "default", password)
		}
	}
	if clientName != "" {
		args = append(args, "setname", clientName)
	}
	cmd := NewMapStringInterfaceCmd(ctx, args...)
	_ = c(ctx, cmd)
	return cmd
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c statefulCmdable) Hello(ctx context.Context,
	ver int, username, password, clientName string,
) *MapStringInterfaceCmd {
	args := make([]interface{}, 0, 7)
	args = append(args, "hello", ver)
	if username != "" || password != "" {
		if username == "" {
			username = "default"
		}
		args = append(args, "auth", username, password)
	}
	if clientName != "" {
		args = append(args, "setname", clientName)
	}
	cmd := NewMapStringInterfaceCmd(ctx, args...)
	_ = c(ctx, cmd)
	return cmd
}
```


#### 📄 檔案: `options.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:63, E:70, A:0) ➔ After(N:63, E:70, A:0)
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

#### 📄 檔案: `redis.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:382, E:511, A:0) ➔ After(N:382, E:511, A:0)
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

### 🔹 函式: `baseClient.initConn()`
- **變更前簽章 (Before)**: `func baseClient.initConn(ctx context.Context, cn *pool.Conn)` (L880~L1277)
- **變更後簽章 (After)**: `func baseClient.initConn(ctx context.Context, cn *pool.Conn)` (L880~L1277)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *baseClient) initConn(ctx context.Context, cn *pool.Conn) error {
	// This function is called in two scenarios:
	// 1. First-time init: Connection is in CREATED state (from pool.Get())
	//    - We need to transition CREATED → INITIALIZING and do the initialization
	//    - If another goroutine is already initializing, we WAIT for it to finish
	// 2. Re-initialization: Connection is in INITIALIZING state (from SetNetConnAndInitConn())
	//    - We're already in INITIALIZING, so just proceed with initialization

	currentState := cn.GetStateMachine().GetState()

	// Fast path: Check if already initialized (IDLE or IN_USE)
	if currentState == pool.StateIdle || currentState == pool.StateInUse {
		return nil
	}

	// If in CREATED state, try to transition to INITIALIZING
	if currentState == pool.StateCreated {
		finalState, err := cn.GetStateMachine().TryTransition([]pool.ConnState{pool.StateCreated}, pool.StateInitializing)
		if err != nil {
			// Another goroutine is initializing or connection is in unexpected state
			// Check what state we're in now
			if finalState == pool.StateIdle || finalState == pool.StateInUse {
				// Already initialized by another goroutine
				return nil
			}

			if finalState == pool.StateInitializing {
				// Another goroutine is initializing - WAIT for it to complete
				// Use a context with timeout = min(remaining command timeout, DialTimeout)
				// This prevents waiting too long while respecting the caller's deadline
				var waitCtx context.Context
				var cancel context.CancelFunc
				dialTimeout := c.opt.DialTimeout

				if cmdDeadline, hasCmdDeadline := ctx.Deadline(); hasCmdDeadline {
					// Calculate remaining time until command deadline
					remainingTime := time.Until(cmdDeadline)
					// Use the minimum of remaining time and DialTimeout
					if remainingTime < dialTimeout {
						// Command deadline is sooner, use it
						waitCtx = ctx
					} else {
						// DialTimeout is shorter, cap the wait at DialTimeout
						waitCtx, cancel = context.WithTimeout(ctx, dialTimeout)
					}
				} else {
					// No command deadline, use DialTimeout to prevent waiting indefinitely
					waitCtx, cancel = context.WithTimeout(ctx, dialTimeout)
				}
				if cancel != nil {
					defer cancel()
				}

				finalState, err := cn.GetStateMachine().AwaitAndTransition(
					waitCtx,
					[]pool.ConnState{pool.StateIdle, pool.StateInUse},
					pool.StateIdle, // Target is IDLE (but we're already there, so this is a no-op)
				)
				if err != nil {
					return err
				}
				// Verify we're now initialized
				if finalState == pool.StateIdle || finalState == pool.StateInUse {
					return nil
				}
				// Unexpected state after waiting
				return fmt.Errorf("connection in unexpected state after initialization: %s", finalState)
			}

			// Unexpected state (CLOSED, UNUSABLE, etc.)
			return err
		}
	}

	// At this point, we're in INITIALIZING state and we own the initialization
	// If we fail, we must transition to CLOSED
	var initErr error
	connPool := pool.NewSingleConnPool(c.connPool, cn)
	// The handshake Conn (handed to OnConnect) must share the client's
	// HIMPORT registry: a private registry restarts versions at 1, so an
	// OnConnect prepare would mark the pooled connection with a version
	// number that collides with the client registry's and silently skips
	// the replay of a different fieldset definition.
	conn := newConn(c.opt, connPool, &c.hooksMixin, c.himport)
	// The internal wrapper does not serve cached reads, but it needs the
	// successful-attachment signal both to issue CLIENT TRACKING during init
	// and to guard the user-visible OnConnect callback below.
	conn.baseClient.cscActive = c.cscActive
	// This internal conn's init pipeline issues CLIENT TRACKING ON itself;
	// exempt it from the guard that blocks user-issued CLIENT TRACKING. Setting
	// the field after newConn is safe: initHooks bound the pipeline hook as a
	// method value on the addressable baseClient, so the guard reads the
	// updated field.
	conn.baseClient.allowClientTracking = true

	username, password := "", ""
	if c.opt.StreamingCredentialsProvider != nil {
		credListener, initErr := c.streamingCredentialsManager.Listener(
			cn,
			c.reAuthConnection(),
			c.onAuthenticationErr(),
		)
		if initErr != nil {
			cn.GetStateMachine().Transition(pool.StateClosed)
			return fmt.Errorf("failed to create credentials listener: %w", initErr)
		}

		credentials, unsubscribeFromCredentialsProvider, initErr := c.opt.StreamingCredentialsProvider.
			Subscribe(credListener)
		if initErr != nil {
			cn.GetStateMachine().Transition(pool.StateClosed)
			return fmt.Errorf("failed to subscribe to streaming credentials: %w", initErr)
		}

		// Per-connection unsubscribe is attached to the connection itself so it
		// runs when this specific connection is closed. Do not register it on
		// c.onClose: initConn runs for every (re)initialized connection, and
		// attaching per-connection state to the shared baseClient registry would
		// either leak entries (one per connection id, never trimmed) or — with
		// the pre-fix wrappedOnClose approach — build an unbounded closure chain
		// retaining every prior connection's unsubscribe (see issue #3772).
		//
		// Note: pool.Conn.SetOnClose OVERWRITES any prior callback (see the
		// doc on that method). That is safe here because the streaming
		// credentials Manager deduplicates listeners by connection id, so a
		// second initConn on the same cn re-Subscribes the SAME listener and
		// the returned unsubscribe is equivalent to the one already installed.
		// Any future code path that could hand out a distinct unsubscribe on
		// re-initialization must first invoke the existing one to avoid
		// orphaning the old subscription on the credentials provider.
		cn.SetOnClose(unsubscribeFromCredentialsProvider)

		username, password = credentials.BasicAuth()
	} else {
		username, password, initErr = c.opt.resolveCredentials(ctx)
		if initErr != nil {
			cn.GetStateMachine().Transition(pool.StateClosed)
			return fmt.Errorf("failed to resolve credentials: %w", initErr)
		}
	}

	// for redis-server versions that do not support the HELLO command,
	// RESP2 will continue to be used.
	// helloOK tracks whether HELLO succeeded. If it did not, the connection
	// falls back to RESP2 regardless of c.opt.Protocol, and features that
	// require RESP3 (e.g. maintenance notifications) must be skipped.
	helloOK := false
	// For redis-server versions that do not support HELLO, RESP2 continues to
	// be used. Remember that negotiated fallback: configured Protocol remains 3,
	// but CSC must not serve without RESP3 invalidations.
	helloFallbackToRESP2 := false
	if initErr = conn.Hello(ctx, c.opt.Protocol, username, password, c.opt.ClientName).Err(); initErr == nil {
		// Authentication successful with HELLO command
		helloOK = true
	} else if !isRedisError(initErr) {
		// When the server responds with the RESP protocol and the result is not a normal
		// execution result of the HELLO command, we consider it to be an indication that
		// the server does not support the HELLO command.
		// The server may be a redis-server that does not support the HELLO command,
		// or it could be DragonflyDB or a third-party redis-proxy. They all respond
		// with different error string results for unsupported commands, making it
		// difficult to rely on error strings to determine all results.
		cn.GetStateMachine().Transition(pool.StateClosed)
		return initErr
	} else {
		helloFallbackToRESP2 = c.opt.Protocol == 3
		if password != "" {
			// Try legacy AUTH command if HELLO failed.
			if username != "" {
				initErr = conn.AuthACL(ctx, username, password).Err()
			} else {
				initErr = conn.Auth(ctx, password).Err()
			}
			if initErr != nil {
				cn.GetStateMachine().Transition(pool.StateClosed)
				return fmt.Errorf("failed to authenticate: %w", initErr)
			}
		}
	}
	if helloFallbackToRESP2 {
		c.disableCSCServing(ctx, "HELLO 3 was rejected and the connection negotiated RESP2")
	}

	// trackingEnabled reports whether THIS pool connection must issue
	// CLIENT TRACKING ON during init. True when CSC (SharedTracking) is enabled:
	// the shared cache is fed by per-connection tracking + the background
	// drainer. Once CSC serving stops (owner Close, GC cleanup, or drainer
	// damping), new and re-inited conns skip tracking — nothing consumes the
	// pushes into the cache anymore.
	// Pipeline-pool connections are excluded from CLIENT TRACKING: pipelined
	// commands never consult or populate the client-side cache (only the
	// single-command cached path on main-pool connections does), so tracking
	// reads made on pipeline connections would only grow the server's tracking
	// table and produce invalidation pushes for keys the cache does not hold.
	trackingEnabled := !helloFallbackToRESP2 && !cn.IsPubSub() && c.cscTrackingRequested() &&
		!c.isPipelinePoolConn(cn)
	if trackingEnabled && c.cscConnInitGen(cn.GetID()) == 0 {
		// First initialization establishes generation 1. Reinitialization
		// already bumped and evicted through onCscReinit before replacing the
		// socket, so it must not bump a second time here.
		c.cscEvictOwnedEntries(cn.GetID())
	}
	var trackingCmd *StatusCmd
	initCmds, initErr := conn.Pipelined(ctx, func(pipe Pipeliner) error {
		if c.opt.DB > 0 {
			pipe.Select(ctx, c.opt.DB)
		}

		if c.opt.readOnly {
			pipe.ReadOnly(ctx)
		}

		if c.opt.ClientName != "" {
			pipe.ClientSetName(ctx, c.opt.ClientName)
		}

		if trackingEnabled {
			// Must run before any cacheable command is issued on this conn.
			trackingCmd = pipe.ClientTrackingOn(ctx, nil)
		}

		return nil
	})
	// The exemption is init-only. OnConnect is user code and must go through
	// the same CSC connection-state guard as every other public command path.
	conn.baseClient.allowClientTracking = false
	trackingRejected := trackingCmd != nil && isRedisError(trackingCmd.Err())
	for _, cmd := range initCmds {
		if cmd != trackingCmd && cmd.Err() != nil {
			trackingRejected = false
			break
		}
	}
	if trackingRejected {
		// A server-side rejection means tracking is unavailable, but the
		// connection and the preceding init commands are still usable. Disable
		// CSC globally and continue without caching. Transport and protocol
		// failures still take the normal connection-failure path below.
		c.disableCSCServing(ctx, fmt.Sprintf("CLIENT TRACKING ON was rejected: %v", trackingCmd.Err()))
		c.cscForgetConn(cn.GetID())
		trackingEnabled = false
		initErr = nil
	}
	if initErr != nil {
		if trackingEnabled {
			// cscEvictOwnedEntries above bumped this conn's init generation; a
			// failed init never serves, and the pubsub path has no OnRemove
			// hook (and the close hook below is not yet installed), so drop
			// the entry here to keep the map bounded to live conns.
			c.cscForgetConn(cn.GetID())
		}
		cn.GetStateMachine().Transition(pool.StateClosed)
		return fmt.Errorf("failed to initialize connection options: %w", initErr)
	}

	if trackingEnabled {
		// Evict this conn's entries on any close (incl. the ConnMaxLifetime/idle
		// path that bypasses the OnRemove hook), since the server drops its
		// tracking table on close.
		c.cscInstallConnCloseHook(cn)
		// A handoff replaces the socket before initConn runs. Bump and evict at
		// the pre-swap boundary so fulfillCached cannot publish an old-socket
		// reply during that gap.
		c.cscInstallConnReinitHook(cn)
	}

	// Enable maintnotifications if maintnotifications are configured
	c.optLock.RLock()
	maintNotifEnabled := c.opt.MaintNotificationsConfig != nil && c.opt.MaintNotificationsConfig.Mode != maintnotifications.ModeDisabled
	protocol := c.opt.Protocol
	var endpointType maintnotifications.EndpointType
	var maintNotifMode maintnotifications.Mode
	if maintNotifEnabled {
		endpointType = c.opt.MaintNotificationsConfig.EndpointType
		maintNotifMode = c.opt.MaintNotificationsConfig.Mode
	}
	c.optLock.RUnlock()

	// Maintenance notifications require RESP3 push frames. If HELLO failed
	// and the connection fell back to RESP2, there is no point in sending
	// CLIENT MAINT_NOTIFICATIONS: the server either rejects it (making the
	// error misleading) or accepts it silently, leaving the client unable
	// to receive any notifications. Decide based on the actual negotiated
	// protocol rather than the requested one.
	if maintNotifEnabled && protocol == 3 && !helloOK {
		if maintNotifMode == maintnotifications.ModeEnabled {
			// Explicitly requested - fail fast with a clear reason.
			cn.GetStateMachine().Transition(pool.StateClosed)
			if errorCallback := pool.GetMetricErrorCallback(); errorCallback != nil {
				errorCallback(ctx, "HANDSHAKE_FAILED", cn, "HANDSHAKE_FAILED", true, 0)
			}
			return fmt.Errorf("failed to enable maintnotifications: server does not support RESP3 (HELLO command failed)")
		}
		// auto/other modes: silently disable maintnotifications for this client.
		c.optLock.Lock()
		c.opt.MaintNotificationsConfig.Mode = maintnotifications.ModeDisabled
		c.optLock.Unlock()
		if err := c.disableMaintNotificationsUpgrades(); err != nil {
			internal.Logger.Printf(ctx, "failed to disable maintnotifications in auto mode: %v", err)
		}
		maintNotifEnabled = false
	}

	var maintNotifHandshakeErr error
	if maintNotifEnabled && protocol == 3 {
		// Hold the manager read lock across the handshake and tracking so a
		// concurrent downgrade cannot remove pool-level listeners before a
		// successfully enabled connection is tracked for retirement.
		c.maintNotificationsManagerLock.RLock()
		manager := c.maintNotificationsManager
		maintNotifHandshakeErr = conn.ClientMaintNotifications(
			ctx,
			true,
			endpointType.String(),
		).Err()
		// A successful handshake enables maintnotifications for this connection,
		// but must not promote ModeAuto to ModeEnabled. ModeEnabled is the
		// explicit fail-closed policy; ModeAuto must remain able to downgrade if a
		// later reconnect/failover reaches an endpoint that rejects the command.
		if maintNotifHandshakeErr == nil && manager != nil {
			manager.TrackMaintNotificationsConn(cn)
		}
		c.maintNotificationsManagerLock.RUnlock()
		if maintNotifHandshakeErr != nil {
			if !isRedisError(maintNotifHandshakeErr) {
				// if not redis error, fail the connection
				cn.GetStateMachine().Transition(pool.StateClosed)
				return maintNotifHandshakeErr
			}
			c.optLock.Lock()
			// handshake failed - check and modify config atomically
			switch c.opt.MaintNotificationsConfig.Mode {
			case maintnotifications.ModeEnabled:
				// enabled mode, fail the connection
				c.optLock.Unlock()
				cn.GetStateMachine().Transition(pool.StateClosed)

				// Record handshake failure metric
				if errorCallback := pool.GetMetricErrorCallback(); errorCallback != nil {
					errorCallback(ctx, "HANDSHAKE_FAILED", cn, "HANDSHAKE_FAILED", true, 0)
				}

				return fmt.Errorf("failed to enable maintnotifications: %w", maintNotifHandshakeErr)
			default: // will handle auto and any other
				// Disabling logging here as it's too noisy.
				// TODO: Enable when we have a better logging solution for log levels
				// internal.Logger.Printf(ctx, "auto mode fallback: maintnotifications disabled due to handshake error: %v", maintNotifHandshakeErr)
				c.opt.MaintNotificationsConfig.Mode = maintnotifications.ModeDisabled
				c.optLock.Unlock()
				// auto mode, disable maintnotifications and continue
				if initErr := c.disableMaintNotificationsUpgrades(); initErr != nil {
					// Log error but continue - auto mode should be resilient
					internal.Logger.Printf(ctx, "failed to disable maintnotifications in auto mode: %v", initErr)
				}
			}
		}
	}

	if !c.opt.DisableIdentity && !c.opt.DisableIndentity {
		libName := ""
		libVer := Version()
		if c.opt.IdentitySuffix != "" {
			libName = c.opt.IdentitySuffix
		}
		p := conn.Pipeline()
		p.ClientSetInfo(ctx, WithLibraryName(libName))
		p.ClientSetInfo(ctx, WithLibraryVersion(libVer))
		// Handle network errors (e.g. timeouts) in CLIENT SETINFO to avoid
		// out of order responses later on.
		if _, initErr = p.Exec(ctx); initErr != nil && !isRedisError(initErr) {
			cn.GetStateMachine().Transition(pool.StateClosed)
			return initErr
		}
	}

	// Set the connection initialization function for potential reconnections
	// This must be set before transitioning to IDLE so that handoff/reauth can use it
	cn.SetInitConnFunc(c.createInitConnFunc())

	// Initialization succeeded - transition to IDLE state
	// This marks the connection as initialized and ready for use
	// NOTE: The connection is still owned by the calling goroutine at this point
	// and won't be available to other goroutines until it's Put() back into the pool
	cn.GetStateMachine().Transition(pool.StateIdle)

	// Call OnConnect hook if configured
	// The connection is in IDLE state but still owned by this goroutine
	// If OnConnect needs to send commands, it can use the connection safely
	if c.opt.OnConnect != nil {
		if initErr = c.opt.OnConnect(ctx, conn); initErr != nil {
			// OnConnect failed - transition to closed
			cn.GetStateMachine().Transition(pool.StateClosed)
			return initErr
		}
	}

	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *baseClient) initConn(ctx context.Context, cn *pool.Conn) error {
	// This function is called in two scenarios:
	// 1. First-time init: Connection is in CREATED state (from pool.Get())
	//    - We need to transition CREATED → INITIALIZING and do the initialization
	//    - If another goroutine is already initializing, we WAIT for it to finish
	// 2. Re-initialization: Connection is in INITIALIZING state (from SetNetConnAndInitConn())
	//    - We're already in INITIALIZING, so just proceed with initialization

	currentState := cn.GetStateMachine().GetState()

	// Fast path: Check if already initialized (IDLE or IN_USE)
	if currentState == pool.StateIdle || currentState == pool.StateInUse {
		return nil
	}

	// If in CREATED state, try to transition to INITIALIZING
	if currentState == pool.StateCreated {
		finalState, err := cn.GetStateMachine().TryTransition([]pool.ConnState{pool.StateCreated}, pool.StateInitializing)
		if err != nil {
			// Another goroutine is initializing or connection is in unexpected state
			// Check what state we're in now
			if finalState == pool.StateIdle || finalState == pool.StateInUse {
				// Already initialized by another goroutine
				return nil
			}

			if finalState == pool.StateInitializing {
				// Another goroutine is initializing - WAIT for it to complete
				// Use a context with timeout = min(remaining command timeout, DialTimeout)
				// This prevents waiting too long while respecting the caller's deadline
				var waitCtx context.Context
				var cancel context.CancelFunc
				dialTimeout := c.opt.DialTimeout

				if cmdDeadline, hasCmdDeadline := ctx.Deadline(); hasCmdDeadline {
					// Calculate remaining time until command deadline
					remainingTime := time.Until(cmdDeadline)
					// Use the minimum of remaining time and DialTimeout
					if remainingTime < dialTimeout {
						// Command deadline is sooner, use it
						waitCtx = ctx
					} else {
						// DialTimeout is shorter, cap the wait at DialTimeout
						waitCtx, cancel = context.WithTimeout(ctx, dialTimeout)
					}
				} else {
					// No command deadline, use DialTimeout to prevent waiting indefinitely
					waitCtx, cancel = context.WithTimeout(ctx, dialTimeout)
				}
				if cancel != nil {
					defer cancel()
				}

				finalState, err := cn.GetStateMachine().AwaitAndTransition(
					waitCtx,
					[]pool.ConnState{pool.StateIdle, pool.StateInUse},
					pool.StateIdle, // Target is IDLE (but we're already there, so this is a no-op)
				)
				if err != nil {
					return err
				}
				// Verify we're now initialized
				if finalState == pool.StateIdle || finalState == pool.StateInUse {
					return nil
				}
				// Unexpected state after waiting
				return fmt.Errorf("connection in unexpected state after initialization: %s", finalState)
			}

			// Unexpected state (CLOSED, UNUSABLE, etc.)
			return err
		}
	}

	// At this point, we're in INITIALIZING state and we own the initialization
	// If we fail, we must transition to CLOSED
	var initErr error
	connPool := pool.NewSingleConnPool(c.connPool, cn)
	// The handshake Conn (handed to OnConnect) must share the client's
	// HIMPORT registry: a private registry restarts versions at 1, so an
	// OnConnect prepare would mark the pooled connection with a version
	// number that collides with the client registry's and silently skips
	// the replay of a different fieldset definition.
	conn := newConn(c.opt, connPool, &c.hooksMixin, c.himport)
	// The internal wrapper does not serve cached reads, but it needs the
	// successful-attachment signal both to issue CLIENT TRACKING during init
	// and to guard the user-visible OnConnect callback below.
	conn.baseClient.cscActive = c.cscActive
	// This internal conn's init pipeline issues CLIENT TRACKING ON itself;
	// exempt it from the guard that blocks user-issued CLIENT TRACKING. Setting
	// the field after newConn is safe: initHooks bound the pipeline hook as a
	// method value on the addressable baseClient, so the guard reads the
	// updated field.
	conn.baseClient.allowClientTracking = true

	username, password := "", ""
	if c.opt.StreamingCredentialsProvider != nil {
		credListener, initErr := c.streamingCredentialsManager.Listener(
			cn,
			c.reAuthConnection(),
			c.onAuthenticationErr(),
		)
		if initErr != nil {
			cn.GetStateMachine().Transition(pool.StateClosed)
			return fmt.Errorf("failed to create credentials listener: %w", initErr)
		}

		credentials, unsubscribeFromCredentialsProvider, initErr := c.opt.StreamingCredentialsProvider.
			Subscribe(credListener)
		if initErr != nil {
			cn.GetStateMachine().Transition(pool.StateClosed)
			return fmt.Errorf("failed to subscribe to streaming credentials: %w", initErr)
		}

		// Per-connection unsubscribe is attached to the connection itself so it
		// runs when this specific connection is closed. Do not register it on
		// c.onClose: initConn runs for every (re)initialized connection, and
		// attaching per-connection state to the shared baseClient registry would
		// either leak entries (one per connection id, never trimmed) or — with
		// the pre-fix wrappedOnClose approach — build an unbounded closure chain
		// retaining every prior connection's unsubscribe (see issue #3772).
		//
		// Note: pool.Conn.SetOnClose OVERWRITES any prior callback (see the
		// doc on that method). That is safe here because the streaming
		// credentials Manager deduplicates listeners by connection id, so a
		// second initConn on the same cn re-Subscribes the SAME listener and
		// the returned unsubscribe is equivalent to the one already installed.
		// Any future code path that could hand out a distinct unsubscribe on
		// re-initialization must first invoke the existing one to avoid
		// orphaning the old subscription on the credentials provider.
		cn.SetOnClose(unsubscribeFromCredentialsProvider)

		username, password = credentials.BasicAuth()
	} else {
		username, password, initErr = c.opt.resolveCredentials(ctx)
		if initErr != nil {
			cn.GetStateMachine().Transition(pool.StateClosed)
			return fmt.Errorf("failed to resolve credentials: %w", initErr)
		}
	}

	// for redis-server versions that do not support the HELLO command,
	// RESP2 will continue to be used.
	// helloOK tracks whether HELLO succeeded. If it did not, the connection
	// falls back to RESP2 regardless of c.opt.Protocol, and features that
	// require RESP3 (e.g. maintenance notifications) must be skipped.
	helloOK := false
	// For redis-server versions that do not support HELLO, RESP2 continues to
	// be used. Remember that negotiated fallback: configured Protocol remains 3,
	// but CSC must not serve without RESP3 invalidations.
	helloFallbackToRESP2 := false
	if initErr = conn.Hello(ctx, c.opt.Protocol, username, password, c.opt.ClientName).Err(); initErr == nil {
		// Authentication successful with HELLO command
		helloOK = true
	} else if !isRedisError(initErr) {
		// When the server responds with the RESP protocol and the result is not a normal
		// execution result of the HELLO command, we consider it to be an indication that
		// the server does not support the HELLO command.
		// The server may be a redis-server that does not support the HELLO command,
		// or it could be DragonflyDB or a third-party redis-proxy. They all respond
		// with different error string results for unsupported commands, making it
		// difficult to rely on error strings to determine all results.
		cn.GetStateMachine().Transition(pool.StateClosed)
		return initErr
	} else {
		helloFallbackToRESP2 = c.opt.Protocol == 3
		if username != "" || password != "" {
			// Try legacy AUTH command if HELLO failed.
			if username != "" {
				initErr = conn.AuthACL(ctx, username, password).Err()
			} else {
				initErr = conn.Auth(ctx, password).Err()
			}
			if initErr != nil {
				cn.GetStateMachine().Transition(pool.StateClosed)
				return fmt.Errorf("failed to authenticate: %w", initErr)
			}
		}
	}
	if helloFallbackToRESP2 {
		c.disableCSCServing(ctx, "HELLO 3 was rejected and the connection negotiated RESP2")
	}

	// trackingEnabled reports whether THIS pool connection must issue
	// CLIENT TRACKING ON during init. True when CSC (SharedTracking) is enabled:
	// the shared cache is fed by per-connection tracking + the background
	// drainer. Once CSC serving stops (owner Close, GC cleanup, or drainer
	// damping), new and re-inited conns skip tracking — nothing consumes the
	// pushes into the cache anymore.
	// Pipeline-pool connections are excluded from CLIENT TRACKING: pipelined
	// commands never consult or populate the client-side cache (only the
	// single-command cached path on main-pool connections does), so tracking
	// reads made on pipeline connections would only grow the server's tracking
	// table and produce invalidation pushes for keys the cache does not hold.
	trackingEnabled := !helloFallbackToRESP2 && !cn.IsPubSub() && c.cscTrackingRequested() &&
		!c.isPipelinePoolConn(cn)
	if trackingEnabled && c.cscConnInitGen(cn.GetID()) == 0 {
		// First initialization establishes generation 1. Reinitialization
		// already bumped and evicted through onCscReinit before replacing the
		// socket, so it must not bump a second time here.
		c.cscEvictOwnedEntries(cn.GetID())
	}
	var trackingCmd *StatusCmd
	initCmds, initErr := conn.Pipelined(ctx, func(pipe Pipeliner) error {
		if c.opt.DB > 0 {
			pipe.Select(ctx, c.opt.DB)
		}

		if c.opt.readOnly {
			pipe.ReadOnly(ctx)
		}

		if c.opt.ClientName != "" {
			pipe.ClientSetName(ctx, c.opt.ClientName)
		}

		if trackingEnabled {
			// Must run before any cacheable command is issued on this conn.
			trackingCmd = pipe.ClientTrackingOn(ctx, nil)
		}

		return nil
	})
	// The exemption is init-only. OnConnect is user code and must go through
	// the same CSC connection-state guard as every other public command path.
	conn.baseClient.allowClientTracking = false
	trackingRejected := trackingCmd != nil && isRedisError(trackingCmd.Err())
	for _, cmd := range initCmds {
		if cmd != trackingCmd && cmd.Err() != nil {
			trackingRejected = false
			break
		}
	}
	if trackingRejected {
		// A server-side rejection means tracking is unavailable, but the
		// connection and the preceding init commands are still usable. Disable
		// CSC globally and continue without caching. Transport and protocol
		// failures still take the normal connection-failure path below.
		c.disableCSCServing(ctx, fmt.Sprintf("CLIENT TRACKING ON was rejected: %v", trackingCmd.Err()))
		c.cscForgetConn(cn.GetID())
		trackingEnabled = false
		initErr = nil
	}
	if initErr != nil {
		if trackingEnabled {
			// cscEvictOwnedEntries above bumped this conn's init generation; a
			// failed init never serves, and the pubsub path has no OnRemove
			// hook (and the close hook below is not yet installed), so drop
			// the entry here to keep the map bounded to live conns.
			c.cscForgetConn(cn.GetID())
		}
		cn.GetStateMachine().Transition(pool.StateClosed)
		return fmt.Errorf("failed to initialize connection options: %w", initErr)
	}

	if trackingEnabled {
		// Evict this conn's entries on any close (incl. the ConnMaxLifetime/idle
		// path that bypasses the OnRemove hook), since the server drops its
		// tracking table on close.
		c.cscInstallConnCloseHook(cn)
		// A handoff replaces the socket before initConn runs. Bump and evict at
		// the pre-swap boundary so fulfillCached cannot publish an old-socket
		// reply during that gap.
		c.cscInstallConnReinitHook(cn)
	}

	// Enable maintnotifications if maintnotifications are configured
	c.optLock.RLock()
	maintNotifEnabled := c.opt.MaintNotificationsConfig != nil && c.opt.MaintNotificationsConfig.Mode != maintnotifications.ModeDisabled
	protocol := c.opt.Protocol
	var endpointType maintnotifications.EndpointType
	var maintNotifMode maintnotifications.Mode
	if maintNotifEnabled {
		endpointType = c.opt.MaintNotificationsConfig.EndpointType
		maintNotifMode = c.opt.MaintNotificationsConfig.Mode
	}
	c.optLock.RUnlock()

	// Maintenance notifications require RESP3 push frames. If HELLO failed
	// and the connection fell back to RESP2, there is no point in sending
	// CLIENT MAINT_NOTIFICATIONS: the server either rejects it (making the
	// error misleading) or accepts it silently, leaving the client unable
	// to receive any notifications. Decide based on the actual negotiated
	// protocol rather than the requested one.
	if maintNotifEnabled && protocol == 3 && !helloOK {
		if maintNotifMode == maintnotifications.ModeEnabled {
			// Explicitly requested - fail fast with a clear reason.
			cn.GetStateMachine().Transition(pool.StateClosed)
			if errorCallback := pool.GetMetricErrorCallback(); errorCallback != nil {
				errorCallback(ctx, "HANDSHAKE_FAILED", cn, "HANDSHAKE_FAILED", true, 0)
			}
			return fmt.Errorf("failed to enable maintnotifications: server does not support RESP3 (HELLO command failed)")
		}
		// auto/other modes: silently disable maintnotifications for this client.
		c.optLock.Lock()
		c.opt.MaintNotificationsConfig.Mode = maintnotifications.ModeDisabled
		c.optLock.Unlock()
		if err := c.disableMaintNotificationsUpgrades(); err != nil {
			internal.Logger.Printf(ctx, "failed to disable maintnotifications in auto mode: %v", err)
		}
		maintNotifEnabled = false
	}

	var maintNotifHandshakeErr error
	if maintNotifEnabled && protocol == 3 {
		// Hold the manager read lock across the handshake and tracking so a
		// concurrent downgrade cannot remove pool-level listeners before a
		// successfully enabled connection is tracked for retirement.
		c.maintNotificationsManagerLock.RLock()
		manager := c.maintNotificationsManager
		maintNotifHandshakeErr = conn.ClientMaintNotifications(
			ctx,
			true,
			endpointType.String(),
		).Err()
		// A successful handshake enables maintnotifications for this connection,
		// but must not promote ModeAuto to ModeEnabled. ModeEnabled is the
		// explicit fail-closed policy; ModeAuto must remain able to downgrade if a
		// later reconnect/failover reaches an endpoint that rejects the command.
		if maintNotifHandshakeErr == nil && manager != nil {
			manager.TrackMaintNotificationsConn(cn)
		}
		c.maintNotificationsManagerLock.RUnlock()
		if maintNotifHandshakeErr != nil {
			if !isRedisError(maintNotifHandshakeErr) {
				// if not redis error, fail the connection
				cn.GetStateMachine().Transition(pool.StateClosed)
				return maintNotifHandshakeErr
			}
			c.optLock.Lock()
			// handshake failed - check and modify config atomically
			switch c.opt.MaintNotificationsConfig.Mode {
			case maintnotifications.ModeEnabled:
				// enabled mode, fail the connection
				c.optLock.Unlock()
				cn.GetStateMachine().Transition(pool.StateClosed)

				// Record handshake failure metric
				if errorCallback := pool.GetMetricErrorCallback(); errorCallback != nil {
					errorCallback(ctx, "HANDSHAKE_FAILED", cn, "HANDSHAKE_FAILED", true, 0)
				}

				return fmt.Errorf("failed to enable maintnotifications: %w", maintNotifHandshakeErr)
			default: // will handle auto and any other
				// Disabling logging here as it's too noisy.
				// TODO: Enable when we have a better logging solution for log levels
				// internal.Logger.Printf(ctx, "auto mode fallback: maintnotifications disabled due to handshake error: %v", maintNotifHandshakeErr)
				c.opt.MaintNotificationsConfig.Mode = maintnotifications.ModeDisabled
				c.optLock.Unlock()
				// auto mode, disable maintnotifications and continue
				if initErr := c.disableMaintNotificationsUpgrades(); initErr != nil {
					// Log error but continue - auto mode should be resilient
					internal.Logger.Printf(ctx, "failed to disable maintnotifications in auto mode: %v", initErr)
				}
			}
		}
	}

	if !c.opt.DisableIdentity && !c.opt.DisableIndentity {
		libName := ""
		libVer := Version()
		if c.opt.IdentitySuffix != "" {
			libName = c.opt.IdentitySuffix
		}
		p := conn.Pipeline()
		p.ClientSetInfo(ctx, WithLibraryName(libName))
		p.ClientSetInfo(ctx, WithLibraryVersion(libVer))
		// Handle network errors (e.g. timeouts) in CLIENT SETINFO to avoid
		// out of order responses later on.
		if _, initErr = p.Exec(ctx); initErr != nil && !isRedisError(initErr) {
			cn.GetStateMachine().Transition(pool.StateClosed)
			return initErr
		}
	}

	// Set the connection initialization function for potential reconnections
	// This must be set before transitioning to IDLE so that handoff/reauth can use it
	cn.SetInitConnFunc(c.createInitConnFunc())

	// Initialization succeeded - transition to IDLE state
	// This marks the connection as initialized and ready for use
	// NOTE: The connection is still owned by the calling goroutine at this point
	// and won't be available to other goroutines until it's Put() back into the pool
	cn.GetStateMachine().Transition(pool.StateIdle)

	// Call OnConnect hook if configured
	// The connection is in IDLE state but still owned by this goroutine
	// If OnConnect needs to send commands, it can use the connection safely
	if c.opt.OnConnect != nil {
		if initErr = c.opt.OnConnect(ctx, conn); initErr != nil {
			// OnConnect failed - transition to closed
			cn.GetStateMachine().Transition(pool.StateClosed)
			return initErr
		}
	}

	return nil
}
```


---

### 🔹 Commit #16: `dc464bf4`
- **完整 Hash**: `dc464bf45c77bcf424cdd285e1204fd1f37a7ae1`
- **說明 (Ground Truth)**: fix(lint): mark discarded done receive for errcheck (#4115)
- **變更檔案數**: 1

#### 📄 檔案: `csc_miss_coalesce.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:91, E:98, A:0) ➔ After(N:91, E:98, A:0)
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

### 🔹 Commit #17: `ec50c698`
- **完整 Hash**: `ec50c6985c4029d8223f004f0e6feda808d5b3c6`
- **說明 (Ground Truth)**: feat(conn): add DisposableConn to discard on Close (#4039)
- **變更檔案數**: 2

#### 📄 檔案: `internal/pool/pool_sticky.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:40, E:45, A:0) ➔ After(N:41, E:45, A:0)
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
  • + [新增節點] `StickyConnPool.DiscardOnClose` (FUNCTION_DEF)

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `StickyConnPool.freeConn()`
- **變更前簽章 (Before)**: `func StickyConnPool.freeConn(ctx context.Context, cn *Conn)` (L130~L136)
- **變更後簽章 (After)**: `func StickyConnPool.freeConn(ctx context.Context, cn *Conn)` (L144~L152)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *StickyConnPool) freeConn(ctx context.Context, cn *Conn) {
	if err := p.badConnError(); err != nil {
		p.pool.Remove(ctx, cn, err)
	} else {
		p.pool.Put(ctx, cn)
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *StickyConnPool) freeConn(ctx context.Context, cn *Conn) {
	if err := p.badConnError(); err != nil {
		p.pool.Remove(ctx, cn, err)
	} else if p.discardOnClose {
		p.pool.Remove(ctx, cn, ErrClosed)
	} else {
		p.pool.Put(ctx, cn)
	}
}
```


#### 📄 檔案: `redis.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:378, E:507, A:0) ➔ After(N:381, E:510, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 7, -Edges: 4, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `sticky.DiscardOnClose (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `Client.EphemeralConn` (FUNCTION_DEF)
  • + [新增節點] `Client.conn` (FUNCTION_DEF)
  • + [新增呼叫邊] `Client.Conn` ──[CALLS]──> `Client.conn`
  • + [新增呼叫邊] `Client.EphemeralConn` ──[CALLS]──> `Client.conn`
  • + [新增呼叫邊] `Client.conn` ──[CALLS]──> `c.baseClient.newStickyConnPool (External/Pkg)`
  • + [新增呼叫邊] `Client.conn` ──[CALLS]──> `sticky.DiscardOnClose (External/Pkg)`
  • + [新增呼叫邊] `Client.conn` ──[CALLS]──> `newConn`
  • + [新增呼叫邊] `Client.conn` ──[CALLS]──> `conn.baseClient.attachCSC (External/Pkg)`
  • + [新增呼叫邊] `Client.conn` ──[CALLS]──> `context.Background (External/Pkg)`
  • - [移除呼叫邊] `Client.Conn` ──[CALLS]──> `newConn`
  • - [移除呼叫邊] `Client.Conn` ──[CALLS]──> `c.baseClient.newStickyConnPool (External/Pkg)`
  • - [移除呼叫邊] `Client.Conn` ──[CALLS]──> `conn.baseClient.attachCSC (External/Pkg)`
  • - [移除呼叫邊] `Client.Conn` ──[CALLS]──> `context.Background (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Client.Conn()`
- **變更前簽章 (Before)**: `func Client.Conn()` (L2679~L2698)
- **變更後簽章 (After)**: `func Client.Conn()` (L2684~L2686)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Client) Conn() *Conn {
	// Share the HIMPORT fieldset registry: the sticky pool borrows
	// connections from this client's pool, so fieldsets prepared on them
	// stay valid after the connections are returned.
	conn := newConn(c.opt, c.baseClient.newStickyConnPool(), &c.hooksMixin, c.himport)
	// A sticky client does not serve cache hits, but a new pool connection first
	// initialized through it may later be reused by the parent. Share the
	// successful-attachment signal so that connection is tracked exactly when
	// the parent's CSC is active.
	conn.baseClient.cscActive = c.baseClient.cscActive
	// No-op today: the strategy needs an idle-conn drainer and a StickyConnPool
	// has none, so CSC isn't active on a Conn() (its reads hit the server). Kept
	// so a future sticky-pool-capable strategy attaches here.
	conn.baseClient.attachCSC(context.Background(), c.csc)
	// Carry the parent's shared eviction hook so that if this derived client
	// initializes a pool conn, the close hook it installs still evicts from the
	// parent cache (its own csc is nil).
	conn.baseClient.cscPoolHook = c.baseClient.cscPoolHook
	return conn
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Client) Conn() *Conn {
	return c.conn(false)
}
```


---

### 🔹 Commit #18: `e3d2548a`
- **完整 Hash**: `e3d2548a381bed649926f90cfd177a10a7c6f9f3`
- **說明 (Ground Truth)**: fix(pool): fix ConnStateMachine waiter races (#4072)
- **變更檔案數**: 1

#### 📄 檔案: `internal/pool/conn_state.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:32, E:43, A:0) ➔ After(N:31, E:42, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 0, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `sm.waiters.PushFront (External/Pkg)` (FUNCTION_DEF)
  • - [移除呼叫邊] `ConnStateMachine.notifyWaiters` ──[CALLS]──> `sm.waiters.PushFront (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `ConnStateMachine.AwaitAndTransition()`
- **變更前簽章 (Before)**: `func ConnStateMachine.AwaitAndTransition(
	ctx context.Context,
	validFromStates []ConnState,
	targetState ConnState,
)` (L216~L286)
- **變更後簽章 (After)**: `func ConnStateMachine.AwaitAndTransition(
	ctx context.Context,
	validFromStates []ConnState,
	targetState ConnState,
)` (L216~L295)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (sm *ConnStateMachine) AwaitAndTransition(
	ctx context.Context,
	validFromStates []ConnState,
	targetState ConnState,
) (ConnState, error) {
	// Fast path: try immediate transition with CAS to prevent race conditions
	// BUT: only if there are no waiters in the queue (to maintain FIFO ordering)
	if sm.waiterCount.Load() == 0 {
		for _, fromState := range validFromStates {
			// Check if we're already in target state
			if fromState == targetState && sm.GetState() == targetState {
				return targetState, nil
			}

			// Try to atomically swap from fromState to targetState
			if sm.state.CompareAndSwap(uint32(fromState), uint32(targetState)) {
				// Success! We transitioned atomically
				sm.notifyWaiters()
				return targetState, nil
			}
		}
	}

	// Fast path failed - check if we should wait or fail
	currentState := sm.GetState()

	// Check if closed
	if currentState == StateClosed {
		return currentState, ErrStateMachineClosed
	}

	// Slow path: need to wait for state change
	// Create waiter with valid states map for fast lookup
	validStatesMap := make(map[ConnState]struct{}, len(validFromStates))
	for _, s := range validFromStates {
		validStatesMap[s] = struct{}{}
	}

	w := &waiter{
		validStates: validStatesMap,
		targetState: targetState,
		done:        make(chan error, 1), // Buffered to avoid goroutine leak
	}

	// Add to FIFO queue
	sm.mu.Lock()
	elem := sm.waiters.PushBack(w)
	sm.waiterCount.Add(1)
	sm.mu.Unlock()

	// Re-check now that the waiter is visible. A transition that happened
	// between the fast path above and the enqueue found no waiter to notify,
	// so without this the waiter would sleep until its context expires.
	sm.notifyWaiters()

	// Wait for state change or timeout
	select {
	case <-ctx.Done():
		// Timeout or cancellation - remove from queue
		sm.mu.Lock()
		sm.waiters.Remove(elem)
		sm.waiterCount.Add(-1)
		sm.mu.Unlock()
		return sm.GetState(), ctx.Err()
	case err := <-w.done:
		// Transition completed (or failed)
		// Note: waiterCount is decremented either in notifyWaiters (when the waiter is notified and removed)
		// or here (on timeout/cancellation).
		return sm.GetState(), err
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (sm *ConnStateMachine) AwaitAndTransition(
	ctx context.Context,
	validFromStates []ConnState,
	targetState ConnState,
) (ConnState, error) {
	// Fast path: try immediate transition with CAS to prevent race conditions
	// BUT: only if there are no waiters in the queue (to maintain FIFO ordering)
	if sm.waiterCount.Load() == 0 {
		for _, fromState := range validFromStates {
			// Check if we're already in target state
			if fromState == targetState && sm.GetState() == targetState {
				return targetState, nil
			}

			// Try to atomically swap from fromState to targetState
			if sm.state.CompareAndSwap(uint32(fromState), uint32(targetState)) {
				// Success! We transitioned atomically
				sm.notifyWaiters()
				return targetState, nil
			}
		}
	}

	// Fast path failed - check if we should wait or fail
	currentState := sm.GetState()

	// Check if closed
	if currentState == StateClosed {
		return currentState, ErrStateMachineClosed
	}

	// Slow path: need to wait for state change
	// Create waiter with valid states map for fast lookup
	validStatesMap := make(map[ConnState]struct{}, len(validFromStates))
	for _, s := range validFromStates {
		validStatesMap[s] = struct{}{}
	}

	w := &waiter{
		validStates: validStatesMap,
		targetState: targetState,
		done:        make(chan error, 1), // Buffered to avoid goroutine leak
	}

	// Add to FIFO queue
	sm.mu.Lock()
	elem := sm.waiters.PushBack(w)
	sm.waiterCount.Add(1)
	sm.mu.Unlock()

	// Re-check now that the waiter is visible. A transition that happened
	// between the fast path above and the enqueue found no waiter to notify,
	// so without this the waiter would sleep until its context expires.
	sm.notifyWaiters()

	// Wait for state change or timeout
	select {
	case <-ctx.Done():
		// Timeout or cancellation - remove from queue
		sm.mu.Lock()
		// notifyWaiters removes the waiter and sends on w.done under sm.mu, so
		// a value here means it was served before we got the lock: report the
		// transition and don't decrement waiterCount again.
		select {
		case err := <-w.done:
			sm.mu.Unlock()
			return sm.GetState(), err
		default:
		}
		sm.waiters.Remove(elem)
		sm.waiterCount.Add(-1)
		sm.mu.Unlock()
		return sm.GetState(), ctx.Err()
	case err := <-w.done:
		// Transition completed (or failed)
		// Note: waiterCount is decremented either in notifyWaiters (when the waiter is notified and removed)
		// or here (on timeout/cancellation).
		return sm.GetState(), err
	}
}
```

### 🔹 函式: `ConnStateMachine.notifyWaiters()`
- **變更前簽章 (Before)**: `func ConnStateMachine.notifyWaiters()` (L290~L341)
- **變更後簽章 (After)**: `func ConnStateMachine.notifyWaiters()` (L299~L347)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (sm *ConnStateMachine) notifyWaiters() {
	// Fast path: check atomic counter without acquiring lock
	// This eliminates mutex overhead in the common case (no waiters)
	if sm.waiterCount.Load() == 0 {
		return
	}

	sm.mu.Lock()
	defer sm.mu.Unlock()

	// Double-check after acquiring lock (waiters might have been processed)
	if sm.waiters.Len() == 0 {
		return
	}

	// Track state locally so we only consider transitions made within this
	// call, not concurrent transitions from woken goroutines. Re-reading the
	// atomic would let a fast goroutine's Transition(StateIdle) leak into our
	// view, causing us to wake multiple waiters at once and breaking FIFO
	// execution ordering.
	currentState := sm.GetState()

	for {
		processed := false

		for elem := sm.waiters.Front(); elem != nil; elem = elem.Next() {
			w := elem.Value.(*waiter)

			if _, valid := w.validStates[currentState]; valid {
				sm.waiters.Remove(elem)
				sm.waiterCount.Add(-1)

				if sm.state.CompareAndSwap(uint32(currentState), uint32(w.targetState)) {
					w.done <- nil
					currentState = w.targetState
					processed = true
					break
				} else {
					sm.waiters.PushFront(w)
					sm.waiterCount.Add(1)
					currentState = sm.GetState()
					processed = true
					break
				}
			}
		}

		if !processed {
			break
		}
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (sm *ConnStateMachine) notifyWaiters() {
	// Fast path: check atomic counter without acquiring lock
	// This eliminates mutex overhead in the common case (no waiters)
	if sm.waiterCount.Load() == 0 {
		return
	}

	sm.mu.Lock()
	defer sm.mu.Unlock()

	// Double-check after acquiring lock (waiters might have been processed)
	if sm.waiters.Len() == 0 {
		return
	}

	// Track state locally so we only consider transitions made within this
	// call, not concurrent transitions from woken goroutines. Re-reading the
	// atomic would let a fast goroutine's Transition(StateIdle) leak into our
	// view, causing us to wake multiple waiters at once and breaking FIFO
	// execution ordering.
	currentState := sm.GetState()

	for {
		processed := false

		for elem := sm.waiters.Front(); elem != nil; elem = elem.Next() {
			w := elem.Value.(*waiter)

			if _, valid := w.validStates[currentState]; valid {
				if sm.state.CompareAndSwap(uint32(currentState), uint32(w.targetState)) {
					sm.waiters.Remove(elem)
					sm.waiterCount.Add(-1)
					w.done <- nil
					currentState = w.targetState
				} else {
					// State changed concurrently. Keep the waiter where it is:
					// AwaitAndTransition holds elem and removes it on timeout.
					currentState = sm.GetState()
				}
				processed = true
				break
			}
		}

		if !processed {
			break
		}
	}
}
```


---

### 🔹 Commit #19: `83d45edd`
- **完整 Hash**: `83d45edda6edcb1f954c9ad1e94d506b2530afd3`
- **說明 (Ground Truth)**: fix:(proto): support uintptr in WriteArg (#4054)
- **變更檔案數**: 1

#### 📄 檔案: `internal/proto/writer.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:27, E:35, A:0) ➔ After(N:27, E:35, A:0)
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

### 🔹 函式: `Writer.WriteArg()`
- **變更前簽章 (Before)**: `func Writer.WriteArg(v interface{})` (L72~L210)
- **變更後簽章 (After)**: `func Writer.WriteArg(v interface{})` (L72~L217)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (w *Writer) WriteArg(v interface{}) error {
	switch v := v.(type) {
	case nil:
		return w.string("")
	case string:
		return w.string(v)
	case *string:
		if v == nil {
			return w.string("")
		}
		return w.string(*v)
	case []byte:
		return w.bytes(v)
	case int:
		return w.int(int64(v))
	case *int:
		if v == nil {
			return w.int(0)
		}
		return w.int(int64(*v))
	case int8:
		return w.int(int64(v))
	case *int8:
		if v == nil {
			return w.int(0)
		}
		return w.int(int64(*v))
	case int16:
		return w.int(int64(v))
	case *int16:
		if v == nil {
			return w.int(0)
		}
		return w.int(int64(*v))
	case int32:
		return w.int(int64(v))
	case *int32:
		if v == nil {
			return w.int(0)
		}
		return w.int(int64(*v))
	case int64:
		return w.int(v)
	case *int64:
		if v == nil {
			return w.int(0)
		}
		return w.int(*v)
	case uint:
		return w.uint(uint64(v))
	case *uint:
		if v == nil {
			return w.uint(0)
		}
		return w.uint(uint64(*v))
	case uint8:
		return w.uint(uint64(v))
	case *uint8:
		if v == nil {
			return w.uint(0)
		}
		return w.uint(uint64(*v))
	case uint16:
		return w.uint(uint64(v))
	case *uint16:
		if v == nil {
			return w.uint(0)
		}
		return w.uint(uint64(*v))
	case uint32:
		return w.uint(uint64(v))
	case *uint32:
		if v == nil {
			return w.uint(0)
		}
		return w.uint(uint64(*v))
	case uint64:
		return w.uint(v)
	case *uint64:
		if v == nil {
			return w.uint(0)
		}
		return w.uint(*v)
	case float32:
		return w.float(float64(v))
	case *float32:
		if v == nil {
			return w.float(0)
		}
		return w.float(float64(*v))
	case float64:
		return w.float(v)
	case *float64:
		if v == nil {
			return w.float(0)
		}
		return w.float(*v)
	case bool:
		if v {
			return w.int(1)
		}
		return w.int(0)
	case *bool:
		if v == nil {
			return w.int(0)
		}
		if *v {
			return w.int(1)
		}
		return w.int(0)
	case time.Time:
		w.numBuf = v.AppendFormat(w.numBuf[:0], time.RFC3339Nano)
		return w.bytes(w.numBuf)
	case *time.Time:
		if v == nil {
			v = &time.Time{}
		}
		w.numBuf = v.AppendFormat(w.numBuf[:0], time.RFC3339Nano)
		return w.bytes(w.numBuf)
	case time.Duration:
		return w.int(v.Nanoseconds())
	case *time.Duration:
		if v == nil {
			return w.int(0)
		}
		return w.int(v.Nanoseconds())
	case encoding.BinaryMarshaler:
		b, err := v.MarshalBinary()
		if err != nil {
			return err
		}
		return w.bytes(b)
	case net.IP:
		return w.bytes(v)
	default:
		return fmt.Errorf(
			"redis: can't marshal %T (implement encoding.BinaryMarshaler)", v)
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (w *Writer) WriteArg(v interface{}) error {
	switch v := v.(type) {
	case nil:
		return w.string("")
	case string:
		return w.string(v)
	case *string:
		if v == nil {
			return w.string("")
		}
		return w.string(*v)
	case []byte:
		return w.bytes(v)
	case int:
		return w.int(int64(v))
	case *int:
		if v == nil {
			return w.int(0)
		}
		return w.int(int64(*v))
	case int8:
		return w.int(int64(v))
	case *int8:
		if v == nil {
			return w.int(0)
		}
		return w.int(int64(*v))
	case int16:
		return w.int(int64(v))
	case *int16:
		if v == nil {
			return w.int(0)
		}
		return w.int(int64(*v))
	case int32:
		return w.int(int64(v))
	case *int32:
		if v == nil {
			return w.int(0)
		}
		return w.int(int64(*v))
	case int64:
		return w.int(v)
	case *int64:
		if v == nil {
			return w.int(0)
		}
		return w.int(*v)
	case uint:
		return w.uint(uint64(v))
	case *uint:
		if v == nil {
			return w.uint(0)
		}
		return w.uint(uint64(*v))
	case uint8:
		return w.uint(uint64(v))
	case *uint8:
		if v == nil {
			return w.uint(0)
		}
		return w.uint(uint64(*v))
	case uint16:
		return w.uint(uint64(v))
	case *uint16:
		if v == nil {
			return w.uint(0)
		}
		return w.uint(uint64(*v))
	case uint32:
		return w.uint(uint64(v))
	case *uint32:
		if v == nil {
			return w.uint(0)
		}
		return w.uint(uint64(*v))
	case uint64:
		return w.uint(v)
	case *uint64:
		if v == nil {
			return w.uint(0)
		}
		return w.uint(*v)
	case uintptr:
		return w.uint(uint64(v))
	case *uintptr:
		if v == nil {
			return w.uint(0)
		}
		return w.uint(uint64(*v))
	case float32:
		return w.float(float64(v))
	case *float32:
		if v == nil {
			return w.float(0)
		}
		return w.float(float64(*v))
	case float64:
		return w.float(v)
	case *float64:
		if v == nil {
			return w.float(0)
		}
		return w.float(*v)
	case bool:
		if v {
			return w.int(1)
		}
		return w.int(0)
	case *bool:
		if v == nil {
			return w.int(0)
		}
		if *v {
			return w.int(1)
		}
		return w.int(0)
	case time.Time:
		w.numBuf = v.AppendFormat(w.numBuf[:0], time.RFC3339Nano)
		return w.bytes(w.numBuf)
	case *time.Time:
		if v == nil {
			v = &time.Time{}
		}
		w.numBuf = v.AppendFormat(w.numBuf[:0], time.RFC3339Nano)
		return w.bytes(w.numBuf)
	case time.Duration:
		return w.int(v.Nanoseconds())
	case *time.Duration:
		if v == nil {
			return w.int(0)
		}
		return w.int(v.Nanoseconds())
	case encoding.BinaryMarshaler:
		b, err := v.MarshalBinary()
		if err != nil {
			return err
		}
		return w.bytes(b)
	case net.IP:
		return w.bytes(v)
	default:
		return fmt.Errorf(
			"redis: can't marshal %T (implement encoding.BinaryMarshaler)", v)
	}
}
```


---

### 🔹 Commit #20: `89ecbc5a`
- **完整 Hash**: `89ecbc5a8e24fd0addfa5457e1a983234c9aef52`
- **說明 (Ground Truth)**: fix(options): reject invalid skip_verify values in ParseURL (#4064)
- **變更檔案數**: 2

#### 📄 檔案: `options.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:63, E:70, A:0) ➔ After(N:63, E:70, A:0)
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

### 🔹 函式: `setupConnParams()`
- **變更前簽章 (Before)**: `func setupConnParams(u *url.URL, o *Options)` (L1076~L1135)
- **變更後簽章 (After)**: `func setupConnParams(u *url.URL, o *Options)` (L1076~L1135)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func setupConnParams(u *url.URL, o *Options) (*Options, error) {
	q := queryOptions{q: u.Query()}

	// compat: a future major release may use q.int("db")
	if tmp := q.string("db"); tmp != "" {
		db, err := strconv.Atoi(tmp)
		if err != nil {
			return nil, fmt.Errorf("redis: invalid database number: %w", err)
		}
		o.DB = db
	}

	o.Protocol = q.int("protocol")
	o.ClientName = q.string("client_name")
	o.MaxRetries = q.int("max_retries")
	o.MinRetryBackoff = q.duration("min_retry_backoff")
	o.MaxRetryBackoff = q.duration("max_retry_backoff")
	o.DialTimeout = q.duration("dial_timeout")
	o.ReadTimeout = q.duration("read_timeout")
	o.WriteTimeout = q.duration("write_timeout")
	o.PoolFIFO = q.bool("pool_fifo")
	o.PoolSize = q.int("pool_size")
	o.PoolTimeout = q.duration("pool_timeout")
	o.MinIdleConns = q.int("min_idle_conns")
	o.MaxIdleConns = q.int("max_idle_conns")
	o.MaxActiveConns = q.int("max_active_conns")
	o.MaxConcurrentDials = q.int("max_concurrent_dials")
	// Pipeline pool (created by default): allow URL-configured clients to opt out
	// (pipeline_pool_size=-1) or tune it, otherwise these would be rejected as
	// unexpected options. q.int accepts a negative value.
	o.PipelinePoolSize = q.int("pipeline_pool_size")
	o.PipelineReadBufferSize = q.int("pipeline_read_buffer_size")
	o.PipelineWriteBufferSize = q.int("pipeline_write_buffer_size")
	if q.has("conn_max_idle_time") {
		o.ConnMaxIdleTime = q.duration("conn_max_idle_time")
	} else {
		o.ConnMaxIdleTime = q.duration("idle_timeout")
	}
	if q.has("conn_max_lifetime") {
		o.ConnMaxLifetime = q.duration("conn_max_lifetime")
	} else {
		o.ConnMaxLifetime = q.duration("max_conn_age")
	}
	if q.has("conn_max_lifetime_jitter") {
		o.ConnMaxLifetimeJitter = min(q.duration("conn_max_lifetime_jitter"), o.ConnMaxLifetime)
	}
	if q.err != nil {
		return nil, q.err
	}
	if o.TLSConfig != nil && q.has("skip_verify") {
		o.TLSConfig.InsecureSkipVerify = q.bool("skip_verify")
	}

	// any parameters left?
	if r := q.remaining(); len(r) > 0 {
		return nil, fmt.Errorf("redis: unexpected option: %s", strings.Join(r, ", "))
	}

	return o, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func setupConnParams(u *url.URL, o *Options) (*Options, error) {
	q := queryOptions{q: u.Query()}

	// compat: a future major release may use q.int("db")
	if tmp := q.string("db"); tmp != "" {
		db, err := strconv.Atoi(tmp)
		if err != nil {
			return nil, fmt.Errorf("redis: invalid database number: %w", err)
		}
		o.DB = db
	}

	o.Protocol = q.int("protocol")
	o.ClientName = q.string("client_name")
	o.MaxRetries = q.int("max_retries")
	o.MinRetryBackoff = q.duration("min_retry_backoff")
	o.MaxRetryBackoff = q.duration("max_retry_backoff")
	o.DialTimeout = q.duration("dial_timeout")
	o.ReadTimeout = q.duration("read_timeout")
	o.WriteTimeout = q.duration("write_timeout")
	o.PoolFIFO = q.bool("pool_fifo")
	o.PoolSize = q.int("pool_size")
	o.PoolTimeout = q.duration("pool_timeout")
	o.MinIdleConns = q.int("min_idle_conns")
	o.MaxIdleConns = q.int("max_idle_conns")
	o.MaxActiveConns = q.int("max_active_conns")
	o.MaxConcurrentDials = q.int("max_concurrent_dials")
	// Pipeline pool (created by default): allow URL-configured clients to opt out
	// (pipeline_pool_size=-1) or tune it, otherwise these would be rejected as
	// unexpected options. q.int accepts a negative value.
	o.PipelinePoolSize = q.int("pipeline_pool_size")
	o.PipelineReadBufferSize = q.int("pipeline_read_buffer_size")
	o.PipelineWriteBufferSize = q.int("pipeline_write_buffer_size")
	if q.has("conn_max_idle_time") {
		o.ConnMaxIdleTime = q.duration("conn_max_idle_time")
	} else {
		o.ConnMaxIdleTime = q.duration("idle_timeout")
	}
	if q.has("conn_max_lifetime") {
		o.ConnMaxLifetime = q.duration("conn_max_lifetime")
	} else {
		o.ConnMaxLifetime = q.duration("max_conn_age")
	}
	if q.has("conn_max_lifetime_jitter") {
		o.ConnMaxLifetimeJitter = min(q.duration("conn_max_lifetime_jitter"), o.ConnMaxLifetime)
	}
	if o.TLSConfig != nil && q.has("skip_verify") {
		o.TLSConfig.InsecureSkipVerify = q.bool("skip_verify")
	}
	if q.err != nil {
		return nil, q.err
	}

	// any parameters left?
	if r := q.remaining(); len(r) > 0 {
		return nil, fmt.Errorf("redis: unexpected option: %s", strings.Join(r, ", "))
	}

	return o, nil
}
```


#### 📄 檔案: `sentinel.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:155, E:227, A:0) ➔ After(N:155, E:227, A:0)
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

### 🔹 函式: `setupFailoverConnParams()`
- **變更前簽章 (Before)**: `func setupFailoverConnParams(u *url.URL, o *FailoverOptions)` (L462~L537)
- **變更後簽章 (After)**: `func setupFailoverConnParams(u *url.URL, o *FailoverOptions)` (L462~L540)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func setupFailoverConnParams(u *url.URL, o *FailoverOptions) (*FailoverOptions, error) {
	q := queryOptions{q: u.Query()}

	o.MasterName = q.string("master_name")
	o.ClientName = q.string("client_name")
	o.RouteByLatency = q.bool("route_by_latency")
	o.RouteByLatencyTolerance = q.duration("route_by_latency_tolerance")
	o.RouteRandomly = q.bool("route_randomly")
	o.ReplicaOnly = q.bool("replica_only")
	o.UseDisconnectedReplicas = q.bool("use_disconnected_replicas")
	o.Protocol = q.int("protocol")
	o.Username = q.string("username")
	o.Password = q.string("password")
	o.MaxRetries = q.int("max_retries")
	o.MinRetryBackoff = q.duration("min_retry_backoff")
	o.MaxRetryBackoff = q.duration("max_retry_backoff")
	o.DialTimeout = q.duration("dial_timeout")
	o.DialerRetries = q.int("dialer_retries")
	o.DialerRetryTimeout = q.duration("dialer_retry_timeout")
	o.ReadTimeout = q.duration("read_timeout")
	o.WriteTimeout = q.duration("write_timeout")
	o.ContextTimeoutEnabled = q.bool("context_timeout_enabled")
	o.PoolFIFO = q.bool("pool_fifo")
	o.PoolSize = q.int("pool_size")
	o.MaxConcurrentDials = q.int("max_concurrent_dials")
	o.MinIdleConns = q.int("min_idle_conns")
	o.MaxIdleConns = q.int("max_idle_conns")
	o.MaxActiveConns = q.int("max_active_conns")
	// Pipeline pool (created by default): allow URL opt-out
	// (pipeline_pool_size=-1) / tuning, else rejected as unexpected options.
	o.PipelinePoolSize = q.int("pipeline_pool_size")
	o.PipelineReadBufferSize = q.int("pipeline_read_buffer_size")
	o.PipelineWriteBufferSize = q.int("pipeline_write_buffer_size")
	o.ConnMaxLifetime = q.duration("conn_max_lifetime")
	if q.has("conn_max_lifetime_jitter") {
		o.ConnMaxLifetimeJitter = min(q.duration("conn_max_lifetime_jitter"), o.ConnMaxLifetime)
	}
	o.ConnMaxIdleTime = q.duration("conn_max_idle_time")
	o.PoolTimeout = q.duration("pool_timeout")
	o.DisableIdentity = q.bool("disableIdentity")
	o.IdentitySuffix = q.string("identitySuffix")
	o.UnstableResp3 = q.bool("unstable_resp3")

	if q.err != nil {
		return nil, q.err
	}

	if tmp := q.string("db"); tmp != "" {
		db, err := strconv.Atoi(tmp)
		if err != nil {
			return nil, fmt.Errorf("redis: invalid database number: %w", err)
		}
		o.DB = db
	}

	addrs := q.strings("addr")
	for _, addr := range addrs {
		h, p, err := net.SplitHostPort(addr)
		if err != nil || h == "" || p == "" {
			return nil, fmt.Errorf("redis: unable to parse addr param: %s", addr)
		}

		o.SentinelAddrs = append(o.SentinelAddrs, net.JoinHostPort(h, p))
	}

	if o.TLSConfig != nil && q.has("skip_verify") {
		o.TLSConfig.InsecureSkipVerify = q.bool("skip_verify")
	}

	// any parameters left?
	if r := q.remaining(); len(r) > 0 {
		return nil, fmt.Errorf("redis: unexpected option: %s", strings.Join(r, ", "))
	}

	return o, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func setupFailoverConnParams(u *url.URL, o *FailoverOptions) (*FailoverOptions, error) {
	q := queryOptions{q: u.Query()}

	o.MasterName = q.string("master_name")
	o.ClientName = q.string("client_name")
	o.RouteByLatency = q.bool("route_by_latency")
	o.RouteByLatencyTolerance = q.duration("route_by_latency_tolerance")
	o.RouteRandomly = q.bool("route_randomly")
	o.ReplicaOnly = q.bool("replica_only")
	o.UseDisconnectedReplicas = q.bool("use_disconnected_replicas")
	o.Protocol = q.int("protocol")
	o.Username = q.string("username")
	o.Password = q.string("password")
	o.MaxRetries = q.int("max_retries")
	o.MinRetryBackoff = q.duration("min_retry_backoff")
	o.MaxRetryBackoff = q.duration("max_retry_backoff")
	o.DialTimeout = q.duration("dial_timeout")
	o.DialerRetries = q.int("dialer_retries")
	o.DialerRetryTimeout = q.duration("dialer_retry_timeout")
	o.ReadTimeout = q.duration("read_timeout")
	o.WriteTimeout = q.duration("write_timeout")
	o.ContextTimeoutEnabled = q.bool("context_timeout_enabled")
	o.PoolFIFO = q.bool("pool_fifo")
	o.PoolSize = q.int("pool_size")
	o.MaxConcurrentDials = q.int("max_concurrent_dials")
	o.MinIdleConns = q.int("min_idle_conns")
	o.MaxIdleConns = q.int("max_idle_conns")
	o.MaxActiveConns = q.int("max_active_conns")
	// Pipeline pool (created by default): allow URL opt-out
	// (pipeline_pool_size=-1) / tuning, else rejected as unexpected options.
	o.PipelinePoolSize = q.int("pipeline_pool_size")
	o.PipelineReadBufferSize = q.int("pipeline_read_buffer_size")
	o.PipelineWriteBufferSize = q.int("pipeline_write_buffer_size")
	o.ConnMaxLifetime = q.duration("conn_max_lifetime")
	if q.has("conn_max_lifetime_jitter") {
		o.ConnMaxLifetimeJitter = min(q.duration("conn_max_lifetime_jitter"), o.ConnMaxLifetime)
	}
	o.ConnMaxIdleTime = q.duration("conn_max_idle_time")
	o.PoolTimeout = q.duration("pool_timeout")
	o.DisableIdentity = q.bool("disableIdentity")
	o.IdentitySuffix = q.string("identitySuffix")
	o.UnstableResp3 = q.bool("unstable_resp3")

	if q.err != nil {
		return nil, q.err
	}

	if tmp := q.string("db"); tmp != "" {
		db, err := strconv.Atoi(tmp)
		if err != nil {
			return nil, fmt.Errorf("redis: invalid database number: %w", err)
		}
		o.DB = db
	}

	addrs := q.strings("addr")
	for _, addr := range addrs {
		h, p, err := net.SplitHostPort(addr)
		if err != nil || h == "" || p == "" {
			return nil, fmt.Errorf("redis: unable to parse addr param: %s", addr)
		}

		o.SentinelAddrs = append(o.SentinelAddrs, net.JoinHostPort(h, p))
	}

	if o.TLSConfig != nil && q.has("skip_verify") {
		o.TLSConfig.InsecureSkipVerify = q.bool("skip_verify")
	}
	if q.err != nil {
		return nil, q.err
	}

	// any parameters left?
	if r := q.remaining(); len(r) > 0 {
		return nil, fmt.Errorf("redis: unexpected option: %s", strings.Join(r, ", "))
	}

	return o, nil
}
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/go-redis show 3f37a3a4e4a1a20259c7db87d77075cdc83c069a
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 3f37a3a4e4a1a20259c7db87d77075cdc83c069a~1 --file test_repos/go-redis/command.go
   ```
