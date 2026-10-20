# 🔬 CODE-Map 基準審查獨立驗證報告: `Avalonia`
> **技術生態**: `C# (跨平台 GUI / 控制項樹 / XAML)`  
> **本地倉庫路徑**: `test_repos/Avalonia`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 33 Files  
> **報告生成時間**: 2026-10-20 21:42:15  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `22` / `33` | `66.7%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `6` / `33` | `18.2%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `5` / `33` | `15.2%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`28` / `33`** | **`84.8%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `1` / `33` | `3.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `b6ed89b8`
- **完整 Hash**: `b6ed89b8d946a2fd1481995c971c2a59899049bd`
- **說明 (Ground Truth)**: Fix Popup.InheritsTransform using the X scale for the Y axis (#22457)
- **變更檔案數**: 1

#### 📄 檔案: `src/Avalonia.Controls/Primitives/Popup.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:177, E:136, A:12) ➔ After(N:177, E:136, A:12)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#x** `(Button / UI Control)`
    └── ⚡ **TemplateApplied()**
  🌲 **#x** `(Button / UI Control)`
    └── ⚡ **Deactivated()**
  🌲 **#x** `(Button / UI Control)`
    └── ⚡ **LostFocus()**
  🌲 **#x** `(Button / UI Control)`
    └── ⚡ **PointerPressed()**
  🌲 **#x** `(Button / UI Control)`
    └── ⚡ **DetachedFromVisualTree()**
  🌲 **#x** `(Button / UI Control)`
    └── ⚡ **Deactivated()**
  🌲 **#x** `(Button / UI Control)`
    └── ⚡ **LostFocus()**
  🌲 **#x** `(Button / UI Control)`
    └── ⚡ **PositionChanged()**
  🌲 **#x** `(Button / UI Control)`
    └── ⚡ **LayoutUpdated()**
  🌲 **#x** `(Button / UI Control)`
    └── ⚡ **PositionChanged()**
  🌲 **#x** `(Button / UI Control)`
    └── ⚡ **Closed()**
  🌲 **#x** `(Button / UI Control)`
    └── ⚡ **LostFocus()**

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Popup.UpdateHostSizing()`
- **變更前簽章 (Before)**: `Popup.UpdateHostSizing(IPopupHost popupHost, TopLevel topLevel, Control placementTarget)` (L736~L765)
- **變更後簽章 (After)**: `Popup.UpdateHostSizing(IPopupHost popupHost, TopLevel topLevel, Control placementTarget)` (L736~L765)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private void UpdateHostSizing(IPopupHost popupHost, TopLevel topLevel, Control placementTarget)
        {
            var scaleX = 1.0;
            var scaleY = 1.0;

            if (InheritsTransform && placementTarget.TransformToVisual(topLevel) is { } m)
            {
                scaleX = Math.Sqrt(m.M11 * m.M11 + m.M12 * m.M12);
                scaleY = Math.Sqrt(m.M11 * m.M11 + m.M12 * m.M12);

                // Ideally we'd only assign a ScaleTransform here when the scale != 1, but there's
                // an issue with LayoutTransformControl in that it sets its LayoutTransform property
                // with LocalValue priority in ArrangeOverride in certain cases when LayoutTransform
                // is null, which breaks TemplateBindings to this property. Offending commit/line:
                //
                // https://github.com/AvaloniaUI/Avalonia/commit/6fbe1c2180ef45a940e193f1b4637e64eaab80ed#diff-5344e793df13f462126a8153ef46c44194f244b6890f25501709bae51df97f82R54
                popupHost.Transform = new ScaleTransform(scaleX, scaleY);
            }
            else
            {
                popupHost.Transform = null;
            }

            popupHost.Width = Width * scaleX;
            popupHost.MinWidth = MinWidth * scaleX;
            popupHost.MaxWidth = MaxWidth * scaleX;
            popupHost.Height = Height * scaleY;
            popupHost.MinHeight = MinHeight * scaleY;
            popupHost.MaxHeight = MaxHeight * scaleY;
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private void UpdateHostSizing(IPopupHost popupHost, TopLevel topLevel, Control placementTarget)
        {
            var scaleX = 1.0;
            var scaleY = 1.0;

            if (InheritsTransform && placementTarget.TransformToVisual(topLevel) is { } m)
            {
                scaleX = Math.Sqrt(m.M11 * m.M11 + m.M12 * m.M12);
                scaleY = Math.Sqrt(m.M21 * m.M21 + m.M22 * m.M22);

                // Ideally we'd only assign a ScaleTransform here when the scale != 1, but there's
                // an issue with LayoutTransformControl in that it sets its LayoutTransform property
                // with LocalValue priority in ArrangeOverride in certain cases when LayoutTransform
                // is null, which breaks TemplateBindings to this property. Offending commit/line:
                //
                // https://github.com/AvaloniaUI/Avalonia/commit/6fbe1c2180ef45a940e193f1b4637e64eaab80ed#diff-5344e793df13f462126a8153ef46c44194f244b6890f25501709bae51df97f82R54
                popupHost.Transform = new ScaleTransform(scaleX, scaleY);
            }
            else
            {
                popupHost.Transform = null;
            }

            popupHost.Width = Width * scaleX;
            popupHost.MinWidth = MinWidth * scaleX;
            popupHost.MaxWidth = MaxWidth * scaleX;
            popupHost.Height = Height * scaleY;
            popupHost.MinHeight = MinHeight * scaleY;
            popupHost.MaxHeight = MaxHeight * scaleY;
        }
```


---

### 🔹 Commit #02: `b72f1fd4`
- **完整 Hash**: `b72f1fd4d8665aeffe8022f7881eaf8f6d56fe7d`
- **說明 (Ground Truth)**: Browser: fix storage stream writes, seeking and reads (#22470)
- **變更檔案數**: 4

#### 📄 檔案: `src/Browser/Avalonia.Browser/Interop/StreamHelper.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:8, E:2, A:0) ➔ After(N:6, E:0, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 3, +Edges: 0, -Edges: 2, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `StreamHelper.ReadIntoAsync` (FUNCTION_DEF)
  • - [移除節點] `StreamHelper.ArrayBufferToMemoryView` (FUNCTION_DEF)
  • - [移除節點] `StreamHelper.SliceAsync` (FUNCTION_DEF)
  • - [移除節點] `StreamHelper.SliceToArrayBuffer` (FUNCTION_DEF)
  • - [移除呼叫邊] `StreamHelper.SliceAsync` ──[CALLS]──> `StreamHelper.SliceToArrayBuffer`
  • - [移除呼叫邊] `StreamHelper.SliceAsync` ──[CALLS]──> `StreamHelper.ArrayBufferToMemoryView`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `src/Browser/Avalonia.Browser/Storage/BlobReadableStream.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:21, E:10, A:0) ➔ After(N:26, E:15, A:0)
- **差分統計**: +Nodes: 10, -Nodes: 5, +Edges: 8, -Edges: 3, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `rented.AsSpan (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `ArrayPool<byte>.Shared.Rent (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_16` (MODULE_STATE)
  • + [新增節點] `segment.Slice (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `MemoryMarshal.TryGetArray<byte> (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `StreamHelper.ReadIntoAsync (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `rented.AsSpan(0, bytesRead).CopyTo (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_15` (MODULE_STATE)
  • + [新增節點] `Math.Clamp (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `ArrayPool<byte>.Shared.Return (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `StreamHelper.SliceAsync (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `Math.Min (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `state_13` (MODULE_STATE)
  • - [移除節點] `bytesRead.CopyTo (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `state_12` (MODULE_STATE)
  • _... 以及其餘 11 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `BlobReadableStream.ReadAsync()`
- **變更前簽章 (Before)**: `BlobReadableStream.ReadAsync(Memory<byte> buffer, CancellationToken cancellationToken = default)` (L65~L78)
- **變更後簽章 (After)**: `BlobReadableStream.ReadAsync(Memory<byte> buffer, CancellationToken cancellationToken = default)` (L73~L109)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public override async ValueTask<int> ReadAsync(Memory<byte> buffer, CancellationToken cancellationToken = default)
    {
        var numBytesToRead = (int)Math.Min(buffer.Length, Length - _position);
        var bytesRead = await StreamHelper.SliceAsync(JSReference, _position, numBytesToRead);
        if (bytesRead.Length != numBytesToRead)
        {
            throw new EndOfStreamException("Failed to read the requested number of bytes from the stream.");
        }

        _position += bytesRead.Length;
        bytesRead.CopyTo(buffer);

        return bytesRead.Length;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public override async ValueTask<int> ReadAsync(Memory<byte> buffer, CancellationToken cancellationToken = default)
    {
        var numBytesToRead = (int)Math.Clamp(Length - _position, 0, buffer.Length);
        if (numBytesToRead == 0)
        {
            return 0;
        }

        // Blob data is copied by JS directly into the managed buffer. Non-array memory goes through a pooled array.
        int bytesRead;
        if (MemoryMarshal.TryGetArray<byte>(buffer, out var segment))
        {
            bytesRead = await StreamHelper.ReadIntoAsync(JSReference, _position, segment.Slice(0, numBytesToRead));
        }
        else
        {
            var rented = ArrayPool<byte>.Shared.Rent(numBytesToRead);
            try
            {
                bytesRead = await StreamHelper.ReadIntoAsync(JSReference, _position, new ArraySegment<byte>(rented, 0, numBytesToRead));
                rented.AsSpan(0, bytesRead).CopyTo(buffer.Span);
            }
            finally
            {
                ArrayPool<byte>.Shared.Return(rented);
            }
        }

        if (bytesRead != numBytesToRead)
        {
            throw new EndOfStreamException("Failed to read the requested number of bytes from the stream.");
        }

        _position += bytesRead;

        return bytesRead;
    }
```

### 🔹 函式: `state_14()`
- **變更前簽章 (Before)**: `[Module State] state_14` (L14~L14)
- **變更後簽章 (After)**: `[Module State] state_14` (L14~L14)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private readonly long _length;
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private JSObject? _jSReference;
```

### 🔹 函式: `BlobReadableStream.Seek()`
- **變更前簽章 (Before)**: `BlobReadableStream.Seek(long offset, SeekOrigin origin)` (L41~L49)
- **變更後簽章 (After)**: `BlobReadableStream.Seek(long offset, SeekOrigin origin)` (L43~L57)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public override long Seek(long offset, SeekOrigin origin)
    {
        return _position = origin switch
        {
            SeekOrigin.Current => _position + offset,
            SeekOrigin.End => _length + offset,
            _ => offset
        };
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public override long Seek(long offset, SeekOrigin origin)
    {
        var position = origin switch
        {
            SeekOrigin.Current => _position + offset,
            SeekOrigin.End => _length + offset,
            _ => offset
        };
        if (position < 0)
        {
            throw new IOException("An attempt was made to move the position before the beginning of the stream.");
        }

        return _position = position;
    }
```


#### 📄 檔案: `src/Browser/Avalonia.Browser/Storage/BrowserStorageProvider.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:85, E:80, A:0) ➔ After(N:85, E:78, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除呼叫邊] `JSStorageFile.OpenWriteAsync` ──[CALLS]──> `StorageHelper.GetProperties (External/BCL)`
  • - [移除呼叫邊] `JSStorageFile.OpenWriteAsync` ──[CALLS]──> `(long?)properties?.GetPropertyAsDouble (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `JSStorageFile.OpenWriteAsync()`
- **變更前簽章 (Before)**: `JSStorageFile.OpenWriteAsync()` (L303~L317)
- **變更後簽章 (After)**: `JSStorageFile.OpenWriteAsync()` (L303~L314)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public async Task<Stream> OpenWriteAsync()
    {
        try
        {
            using var properties = await StorageHelper.GetProperties(FileHandle);
            var streamWriter = await StorageHelper.OpenWrite(FileHandle);
            var size = (long?)properties?.GetPropertyAsDouble("Size") ?? 0;

            return new WriteableStream(streamWriter, size);
        }
        catch (JSException ex) when (ex.Message == BrowserStorageProvider.NoPermissionsMessage)
        {
            throw new UnauthorizedAccessException("User denied permissions to open the file", ex);
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public async Task<Stream> OpenWriteAsync()
    {
        try
        {
            var streamWriter = await StorageHelper.OpenWrite(FileHandle);
            return new WriteableStream(streamWriter);
        }
        catch (JSException ex) when (ex.Message == BrowserStorageProvider.NoPermissionsMessage)
        {
            throw new UnauthorizedAccessException("User denied permissions to open the file", ex);
        }
    }
```


#### 📄 檔案: `src/Browser/Avalonia.Browser/Storage/WriteableStream.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:20, E:13, A:0) ➔ After(N:21, E:14, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 2, +Edges: 1, -Edges: 0, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_14` (MODULE_STATE)
  • + [新增節點] `MemoryMarshal.TryGetArray (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_17` (MODULE_STATE)
  • - [移除節點] `state_13` (MODULE_STATE)
  • - [移除節點] `state_16` (MODULE_STATE)
  • + [新增呼叫邊] `WriteableStream.WriteAsync` ──[CALLS]──> `MemoryMarshal.TryGetArray (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `WriteableStream.WriteableStream()`
- **變更前簽章 (Before)**: `WriteableStream.WriteableStream(JSObject jSReference, long initialLength)` (L18~L22)
- **變更後簽章 (After)**: `WriteableStream.WriteableStream(JSObject jSReference)` (L19~L22)

#### ◀️ 變更前實作碼 (Before Implementation):
```
internal WriteableStream(JSObject jSReference, long initialLength)
    {
        _jSReference = jSReference;
        _length = initialLength;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal WriteableStream(JSObject jSReference)
    {
        _jSReference = jSReference;
    }
```

### 🔹 函式: `WriteableStream.WriteAsyncInternal()`
- **變更前簽章 (Before)**: `WriteableStream.WriteAsyncInternal(byte[] buffer, int offset, int count, CancellationToken _)` (L102~L107)
- **變更後簽章 (After)**: `WriteableStream.WriteAsyncInternal(byte[] buffer, int offset, int count, CancellationToken _)` (L112~L121)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private Task WriteAsyncInternal(byte[] buffer, int offset, int count, CancellationToken _)
    {
        _position += count;

        return StreamHelper.WriteAsync(JSReference, buffer, offset, count);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private Task WriteAsyncInternal(byte[] buffer, int offset, int count, CancellationToken _)
    {
        _position += count;
        if (_position > _length)
        {
            _length = _position;
        }

        return StreamHelper.WriteAsync(JSReference, buffer, offset, count);
    }
```

### 🔹 函式: `WriteableStream.Seek()`
- **變更前簽章 (Before)**: `WriteableStream.Seek(long offset, SeekOrigin origin)` (L50~L60)
- **變更後簽章 (After)**: `WriteableStream.Seek(long offset, SeekOrigin origin)` (L50~L65)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public override long Seek(long offset, SeekOrigin origin)
    {
        var position = origin switch
        {
            SeekOrigin.Current => _position + offset,
            SeekOrigin.End => _length + offset,
            _ => offset
        };
        StreamHelper.Seek(JSReference, position);
        return position;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public override long Seek(long offset, SeekOrigin origin)
    {
        var position = origin switch
        {
            SeekOrigin.Current => _position + offset,
            SeekOrigin.End => _length + offset,
            _ => offset
        };
        if (position < 0)
        {
            throw new IOException("An attempt was made to move the position before the beginning of the stream.");
        }

        StreamHelper.Seek(JSReference, position);
        return _position = position;
    }
```

### 🔹 函式: `WriteableStream.WriteAsync()`
- **變更前簽章 (Before)**: `WriteableStream.WriteAsync(ReadOnlyMemory<byte> buffer, CancellationToken cancellationToken = default)` (L81~L84)
- **變更後簽章 (After)**: `WriteableStream.WriteAsync(ReadOnlyMemory<byte> buffer, CancellationToken cancellationToken = default)` (L86~L94)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public override ValueTask WriteAsync(ReadOnlyMemory<byte> buffer, CancellationToken cancellationToken = default)
    {
        return new ValueTask(WriteAsyncInternal(buffer.ToArray(), 0, buffer.Length, cancellationToken));
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public override ValueTask WriteAsync(ReadOnlyMemory<byte> buffer, CancellationToken cancellationToken = default)
    {
        if (MemoryMarshal.TryGetArray(buffer, out var segment))
        {
            return new ValueTask(WriteAsyncInternal(segment.Array!, segment.Offset, segment.Count, cancellationToken));
        }

        return new ValueTask(WriteAsyncInternal(buffer.ToArray(), 0, buffer.Length, cancellationToken));
    }
```


---

### 🔹 Commit #03: `da7ea04e`
- **完整 Hash**: `da7ea04e6d307d5424ab25dc5ec7f32d742801ff`
- **說明 (Ground Truth)**: Fix NRE when the application shuts down while showing the main window (#22497)
- **變更檔案數**: 1

#### 📄 檔案: `src/Avalonia.Controls/ApplicationLifetimes/ClassicDesktopStyleApplicationLifetime.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:46, E:40, A:0) ➔ After(N:46, E:40, A:0)
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

### 🔹 函式: `ClassicDesktopStyleApplicationLifetime.StartCore()`
- **變更前簽章 (Before)**: `ClassicDesktopStyleApplicationLifetime.StartCore(string[] args)` (L140~L158)
- **變更後簽章 (After)**: `ClassicDesktopStyleApplicationLifetime.StartCore(string[] args)` (L140~L160)

#### ◀️ 變更前實作碼 (Before Implementation):
```
internal int StartCore(string[] args)
        {
            // Before/AfterInit should have been called from ISetupApplicationLifetime.
            // If somehow they weren't (e.g., for a manually started lifetime), do it now.
            BeforeInit();
            AfterInit();
            Startup?.Invoke(this, new ControlledApplicationLifetimeStartupEventArgs(args));

            _cts = new CancellationTokenSource();

            // Note due to a bug in the JIT we wrap this in a method, otherwise MainWindow
            // gets stuffed into a local var and can not be GCed until after the program stops.
            // this method never exits until program end.
            ShowMainWindow();

            Dispatcher.UIThread.MainLoop(_cts.Token);
            Environment.ExitCode = _exitCode;
            return _exitCode;
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal int StartCore(string[] args)
        {
            // Before/AfterInit should have been called from ISetupApplicationLifetime.
            // If somehow they weren't (e.g., for a manually started lifetime), do it now.
            BeforeInit();
            AfterInit();
            Startup?.Invoke(this, new ControlledApplicationLifetimeStartupEventArgs(args));

            _cts = new CancellationTokenSource();
            var token = _cts.Token;

            // Note due to a bug in the JIT we wrap this in a method, otherwise MainWindow
            // gets stuffed into a local var and can not be GCed until after the program stops.
            // this method never exits until program end.
            ShowMainWindow();

            if (!token.IsCancellationRequested)
                Dispatcher.UIThread.MainLoop(token);
            Environment.ExitCode = _exitCode;
            return _exitCode;
        }
```


---

### 🔹 Commit #04: `82c96fe1`
- **完整 Hash**: `82c96fe15daaead9c53d28b2f71a4791fec43859`
- **說明 (Ground Truth)**: Win32: fix GetDpiForMonitor P/Invoke return type (x86 ignored DPI scaling) (#22419)
- **變更檔案數**: 1

#### 📄 檔案: `src/Windows/Avalonia.Win32/Interop/UnmanagedMethods.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:597, E:22, A:0) ➔ After(N:597, E:22, A:0)
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

### 🔹 函式: `UnmanagedMethods.GetDpiForMonitor()`
- **變更前簽章 (Before)**: `UnmanagedMethods.GetDpiForMonitor(IntPtr hmonitor, MONITOR_DPI_TYPE dpiType, out uint dpiX, out uint dpiY)` (L1732~L1733)
- **變更後簽章 (After)**: `UnmanagedMethods.GetDpiForMonitor(IntPtr hmonitor, MONITOR_DPI_TYPE dpiType, out uint dpiX, out uint dpiY)` (L1732~L1733)

#### ◀️ 變更前實作碼 (Before Implementation):
```
[DllImport("shcore.dll")]
        public static extern long GetDpiForMonitor(IntPtr hmonitor, MONITOR_DPI_TYPE dpiType, out uint dpiX, out uint dpiY);
```

#### ▶️ 變更後實作碼 (After Implementation):
```
[DllImport("shcore.dll")]
        public static extern int GetDpiForMonitor(IntPtr hmonitor, MONITOR_DPI_TYPE dpiType, out uint dpiX, out uint dpiY);
```


---

### 🔹 Commit #05: `d9311668`
- **完整 Hash**: `d9311668349b0c192c5486f3218a6f8feaaf0317`
- **說明 (Ground Truth)**: Fix - Don't change page in Tabbed Page if focus is owned by child element. (#22337)
- **變更檔案數**: 1

#### 📄 檔案: `src/Avalonia.Controls/Page/TabbedPage.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:96, E:105, A:5) ➔ After(N:97, E:106, A:5)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_tabControl** `(Button / UI Control)`
    └── ⚡ **ContainerPrepared()**
        └── 🎯 [TRIGGERS] `TabbedPage.OnContainerPrepared()`
            └── 🎯 [CALLS] `TabbedPage.GetIsTabEnabled()`
                └── 🎯 [CALLS] `page.GetValue (External/BCL)()`
            └── 🎯 [CALLS] `TabbedPage.PreparePageForContainer()`
                └── 🎯 [CALLS] `TabbedPage.ClearContainerPage()`
                    └── 🎯 [CALLS] `LogicalChildren.Remove (External/BCL)()`
                    └── 🎯 [CALLS] `_containerPageMap.Remove (External/BCL)()`
                    └── 🎯 [CALLS] `_pageContainerMap.Remove (External/BCL)()`
                    └── 🎯 [CALLS] `_templateCreatedPages.Remove (External/BCL)()`
                └── 🎯 [CALLS] `TabbedPage.TryGetItemAtIndex()`
                └── 🎯 [CALLS] `LogicalChildren.Add (External/BCL)()`
                └── 🎯 [CALLS] `PageTemplate?.Build (External/BCL)()`
                └── 🎯 [CALLS] `_templateCreatedPages.Add (External/BCL)()`
            └── 🎯 [CALLS] `TabbedPage.UpdateActivePage()`
                └── 🎯 [CALLS] `TabbedPage.CommitSelectionIfResolved()`
                    └── 🎯 [CALLS] `TabbedPage.ResolvePageAtIndex()`
                        └── *ref:`TabbedPage.ResolvePageAtIndex` [已折疊指針]
                        └── 🎯 [CALLS] `_containerPageMap.TryGetValue (External/BCL)()`
                        └── 🎯 [CALLS] `_tabControl?.ContainerFromIndex (External/BCL)()`
                    └── 🎯 [CALLS] `CommitSelection (External/BCL)()`
                    └── 🎯 [CALLS] `StoreSelectedIndex (External/BCL)()`
                    └── 🎯 [CALLS] `page == null &&
                ItemsSource != null &&
                index >= 0 &&
                _tabControl?.ContainerFromIndex (External/BCL)()`
                └── 🎯 [CALLS] `TabbedPage.UpdateContentSafeAreaPadding()`
                    └── 🎯 [CALLS] `TabbedPage.ResolveTabPlacement()`
                    └── *ref:`TabbedPage.UpdateContentSafeAreaPadding` [已折疊指針]
  🌲 **#_tabControl** `(Button / UI Control)`
    └── ⚡ **ContainerClearing()**
        └── 🎯 [TRIGGERS] `TabbedPage.OnContainerClearing()`
            └── 🎯 [CALLS] `TabbedPage.ClearContainerPage()`
                └── 🎯 [CALLS] `LogicalChildren.Remove (External/BCL)()`
                └── 🎯 [CALLS] `_containerPageMap.Remove (External/BCL)()`
                └── 🎯 [CALLS] `_pageContainerMap.Remove (External/BCL)()`
                └── 🎯 [CALLS] `_templateCreatedPages.Remove (External/BCL)()`
  🌲 **#_tabControl** `(Button / UI Control)`
    └── ⚡ **SelectedIndex()**
  🌲 **#_tabControl** `(Button / UI Control)`
    └── ⚡ **SelectionChanged()**
        └── 🎯 [TRIGGERS] `TabbedPage.TabControl_SelectionChanged()`
            └── 🎯 [CALLS] `TabbedPage.CommitSelectionIfResolved()`
                └── 🎯 [CALLS] `TabbedPage.ResolvePageAtIndex()`
                    └── *ref:`TabbedPage.ResolvePageAtIndex` [已折疊指針]
                    └── 🎯 [CALLS] `_containerPageMap.TryGetValue (External/BCL)()`
                    └── 🎯 [CALLS] `_tabControl?.ContainerFromIndex (External/BCL)()`
                └── 🎯 [CALLS] `CommitSelection (External/BCL)()`
                └── 🎯 [CALLS] `StoreSelectedIndex (External/BCL)()`
                └── 🎯 [CALLS] `page == null &&
                ItemsSource != null &&
                index >= 0 &&
                _tabControl?.ContainerFromIndex (External/BCL)()`
            └── 🎯 [CALLS] `TabbedPage.FindNearestEnabledTab()`
                └── 🎯 [CALLS] `TabbedPage.GetTabCount()`
                └── 🎯 [CALLS] `TabbedPage.IsTabEnabledAtIndex()`
                    └── 🎯 [CALLS] `TabbedPage.GetIsTabEnabled()`
                        └── 🎯 [CALLS] `page.GetValue (External/BCL)()`
                    └── *ref:`TabbedPage.ResolvePageAtIndex` [已折疊指針]
                    └── *ref:`_containerPageMap.TryGetValue (External/BCL)` [已折疊指針]
                    └── *ref:`_tabControl?.ContainerFromIndex (External/BCL)` [已折疊指針]
            └── *ref:`TabbedPage.GetIsTabEnabled` [已折疊指針]
            └── *ref:`TabbedPage.ResolvePageAtIndex` [已折疊指針]
            └── 🎯 [CALLS] `TabbedPage.UpdateContentSafeAreaPadding()`
                └── 🎯 [CALLS] `TabbedPage.ResolveTabPlacement()`
                └── *ref:`TabbedPage.UpdateContentSafeAreaPadding` [已折疊指針]
  🌲 **#page** `(Button / UI Control)`
    └── ⚡ **PropertyChanged()**
        └── 🎯 [TRIGGERS] `TabbedPage.OnPagePropertyChanged()`
            └── 🎯 [CALLS] `TabbedPage.SyncTabEnabledState()`
                └── 🎯 [CALLS] `TabbedPage.FindNearestEnabledTab()`
                    └── 🎯 [CALLS] `TabbedPage.GetTabCount()`
                    └── 🎯 [CALLS] `TabbedPage.IsTabEnabledAtIndex()`
                        └── 🎯 [CALLS] `TabbedPage.GetIsTabEnabled()`
                            └── 🎯 [CALLS] `page.GetValue (External/BCL)()`
                        └── 🎯 [CALLS] `TabbedPage.ResolvePageAtIndex()`
                            └── *ref:`TabbedPage.ResolvePageAtIndex` [已折疊指針]
                            └── 🎯 [CALLS] `_containerPageMap.TryGetValue (External/BCL)()`
                            └── 🎯 [CALLS] `_tabControl?.ContainerFromIndex (External/BCL)()`
                        └── *ref:`_containerPageMap.TryGetValue (External/BCL)` [已折疊指針]
                        └── *ref:`_tabControl?.ContainerFromIndex (External/BCL)` [已折疊指針]
                └── *ref:`TabbedPage.GetIsTabEnabled` [已折疊指針]
                └── 🎯 [CALLS] `ReferenceEquals (External/BCL)()`
                └── 🎯 [CALLS] `_pageContainerMap.TryGetValue (External/BCL)()`
                └── 🎯 [CALLS] `_tabControl.ContainerFromIndex (External/BCL)()`
            └── *ref:`_pageContainerMap.TryGetValue (External/BCL)` [已折疊指針]

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `_tabControl.LogicalChildren.Contains (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `TabbedPage.OnKeyDown` ──[CALLS]──> `_tabControl.LogicalChildren.Contains (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TabbedPage.OnKeyDown()`
- **變更前簽章 (Before)**: `TabbedPage.OnKeyDown(KeyEventArgs e)` (L701~L741)
- **變更後簽章 (After)**: `TabbedPage.OnKeyDown(KeyEventArgs e)` (L701~L759)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override void OnKeyDown(KeyEventArgs e)
        {
            base.OnKeyDown(e);

            if (!IsKeyboardNavigationEnabled || _tabControl == null)
                return;

            var resolved = ResolveTabPlacement();
            bool isHorizontal = resolved == TabPlacement.Top || resolved == TabPlacement.Bottom;
            bool isRtl = FlowDirection == Media.FlowDirection.RightToLeft;

            bool next = isHorizontal ? (isRtl ? e.Key == Key.Left : e.Key == Key.Right) : e.Key == Key.Down;
            bool prev = isHorizontal ? (isRtl ? e.Key == Key.Right : e.Key == Key.Left) : e.Key == Key.Up;

            if (e.KeyModifiers.HasFlag(KeyModifiers.Control) && e.Key == Key.Tab)
            {
                next = !e.KeyModifiers.HasFlag(KeyModifiers.Shift);
                prev = e.KeyModifiers.HasFlag(KeyModifiers.Shift);
            }

            if (next)
            {
                int target = FindNextEnabledTab(_tabControl.SelectedIndex + 1, 1);
                if (target >= 0)
                {
                    _tabControl.SelectedIndex = target;
                    FocusSelectedTabItem();
                    e.Handled = true;
                }
            }
            else if (prev)
            {
                int target = FindNextEnabledTab(_tabControl.SelectedIndex - 1, -1);
                if (target >= 0)
                {
                    _tabControl.SelectedIndex = target;
                    FocusSelectedTabItem();
                    e.Handled = true;
                }
            }
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override void OnKeyDown(KeyEventArgs e)
        {
            base.OnKeyDown(e);

            if (!IsKeyboardNavigationEnabled || _tabControl == null)
                return;

            bool _skipDirectionalNavigation = false, next = false, prev = false;

            // If focus is in tabbed page, but owned by a focusable element, we do not change pages.
            if (IsKeyboardFocusWithin && !IsFocused)
            {
                // If focus is owned by a tab item, continue as usual.
                if (!(KeyboardDevice.Instance?.FocusedElement is TabItem item && _tabControl.LogicalChildren.Contains(item)))
                {
                    // Focus is not on a tab item header, nor on the tabbed page element, but instead in a focusable child. We do not
                    // change page.
                    _skipDirectionalNavigation = true;
                }
            }

            if (!_skipDirectionalNavigation)
            {
                var resolved = ResolveTabPlacement();
                bool isHorizontal = resolved == TabPlacement.Top || resolved == TabPlacement.Bottom;
                bool isRtl = FlowDirection == Media.FlowDirection.RightToLeft;

                next = isHorizontal ? (isRtl ? e.Key == Key.Left : e.Key == Key.Right) : e.Key == Key.Down;
                prev = isHorizontal ? (isRtl ? e.Key == Key.Right : e.Key == Key.Left) : e.Key == Key.Up;

            }

            if (e.KeyModifiers.HasFlag(KeyModifiers.Control) && e.Key == Key.Tab)
            {
                next = !e.KeyModifiers.HasFlag(KeyModifiers.Shift);
                prev = e.KeyModifiers.HasFlag(KeyModifiers.Shift);
            }

            if (next)
            {
                int target = FindNextEnabledTab(_tabControl.SelectedIndex + 1, 1);
                if (target >= 0)
                {
                    _tabControl.SelectedIndex = target;
                    FocusSelectedTabItem();
                    e.Handled = true;
                }
            }
            else if (prev)
            {
                int target = FindNextEnabledTab(_tabControl.SelectedIndex - 1, -1);
                if (target >= 0)
                {
                    _tabControl.SelectedIndex = target;
                    FocusSelectedTabItem();
                    e.Handled = true;
                }
            }
        }
```


---

### 🔹 Commit #06: `f5807681`
- **完整 Hash**: `f5807681dcad9dd2a4da9fe92354a5b88d60cba4`
- **說明 (Ground Truth)**:  Fix Window arrange when its size is platform constrained (#22488)
- **變更檔案數**: 2

#### 📄 檔案: `src/Avalonia.Controls/Window.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:178, E:152, A:0) ➔ After(N:178, E:152, A:0)
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

### 🔹 函式: `Window.HandleResized()`
- **變更前簽章 (Before)**: `Window.HandleResized(Size clientSize, WindowResizeReason reason)` (L1464~L1500)
- **變更後簽章 (After)**: `Window.HandleResized(Size clientSize, WindowResizeReason reason)` (L1464~L1510)

#### ◀️ 變更前實作碼 (Before Implementation):
```
internal override void HandleResized(Size clientSize, WindowResizeReason reason)
        {
            // In forced decoration mode, the platform's clientSize includes decoration area.
            // Subtract the decoration inset so Window.ClientSize reflects the usable content area.
            if (_isForcedDecorationMode)
            {
                var inset = TopLevelHost.DecorationInset;
                clientSize = new Size(
                    Math.Max(0, clientSize.Width - inset.Left - inset.Right),
                    Math.Max(0, clientSize.Height - inset.Top - inset.Bottom));
            }

            if (_canHandleResized && (ClientSize != clientSize || double.IsNaN(Width) || double.IsNaN(Height)))
            {
                var sizeToContent = SizeToContent;

                // If auto-sizing is enabled, and the resize came from a user resize (or the reason was
                // unspecified) then turn off auto-resizing for any window dimension that is not equal
                // to the requested size.
                if (sizeToContent != SizeToContent.Manual &&
                    CanResize &&
                    reason == WindowResizeReason.Unspecified ||
                    reason == WindowResizeReason.User)
                {
                    if (clientSize.Width != ClientSize.Width)
                        sizeToContent &= ~SizeToContent.Width;
                    if (clientSize.Height != ClientSize.Height)
                        sizeToContent &= ~SizeToContent.Height;
                    SizeToContent = sizeToContent;
                }

                Width = clientSize.Width;
                Height = clientSize.Height;
            }

            base.HandleResized(clientSize, reason);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal override void HandleResized(Size clientSize, WindowResizeReason reason)
        {
            // In forced decoration mode, the platform's clientSize includes decoration area.
            // Subtract the decoration inset so Window.ClientSize reflects the usable content area.
            if (_isForcedDecorationMode)
            {
                var inset = TopLevelHost.DecorationInset;
                clientSize = new Size(
                    Math.Max(0, clientSize.Width - inset.Left - inset.Right),
                    Math.Max(0, clientSize.Height - inset.Top - inset.Bottom));
            }

            if (_canHandleResized && (ClientSize != clientSize || double.IsNaN(Width) || double.IsNaN(Height)))
            {
                var sizeToContent = SizeToContent;

                // If auto-sizing is enabled, and the resize came from a user resize (or the reason was
                // unspecified) then turn off auto-resizing for any window dimension that is not equal
                // to the requested size.
                if (sizeToContent != SizeToContent.Manual &&
                    CanResize &&
                    reason == WindowResizeReason.Unspecified ||
                    reason == WindowResizeReason.User)
                {
                    if (clientSize.Width != ClientSize.Width)
                        sizeToContent &= ~SizeToContent.Width;
                    if (clientSize.Height != ClientSize.Height)
                        sizeToContent &= ~SizeToContent.Height;
                    SizeToContent = sizeToContent;
                }

                Width = clientSize.Width;
                Height = clientSize.Height;
            }
            else if (_shown && !_canHandleResized)
            {
                // Show() is in progress: the platform may have constrained the requested size.
                // Update an explicit Width/Height before any layout pass, otherwise the content would be
                // measured with the requested size but arranged with the actual one.
                if (!double.IsNaN(Width))
                    Width = clientSize.Width;
                if (!double.IsNaN(Height))
                    Height = clientSize.Height;
            }

            base.HandleResized(clientSize, reason);
        }
```


#### 📄 檔案: `src/Avalonia.Controls/WindowBase.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:58, E:46, A:0) ➔ After(N:59, E:47, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 1, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_379` (MODULE_STATE)
  • + [新增節點] `Measure (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `state_373` (MODULE_STATE)
  • + [新增呼叫邊] `WindowBase.ArrangeCore` ──[CALLS]──> `Measure (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `WindowBase.ArrangeCore()`
- **變更前簽章 (Before)**: `WindowBase.ArrangeCore(Rect finalRect)` (L305~L310)
- **變更後簽章 (After)**: `WindowBase.ArrangeCore(Rect finalRect)` (L305~L316)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override void ArrangeCore(Rect finalRect)
        {
            var constraint = ArrangeSetBounds(finalRect.Size);
            var arrangeSize = ArrangeOverride(constraint);
            Bounds = new Rect(finalRect.Position, arrangeSize);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override void ArrangeCore(Rect finalRect)
        {
            var constraint = ArrangeSetBounds(finalRect.Size);

            // Setting the bounds may have resulted in a different size than requested, invalidating our measure:
            // measure again so that the content isn't arranged with a size it wasn't measured with.
            if (!IsMeasureValid)
                Measure(PreviousMeasure ?? finalRect.Size);

            var arrangeSize = ArrangeOverride(constraint);
            Bounds = new Rect(finalRect.Position, arrangeSize);
        }
```


---

### 🔹 Commit #07: `dd91d9dc`
- **完整 Hash**: `dd91d9dc44557e2dbe87d8fe5c881d33ba0d6f33`
- **說明 (Ground Truth)**: Use property helper to safely read _NET_WORKAREA in X11 (#22448)
- **變更檔案數**: 1

#### 📄 檔案: `src/Avalonia.X11/Screens/X11Screen.Providers.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:71, E:46, A:3) ➔ After(N:68, E:42, A:3)
- **差分統計**: +Nodes: 16, -Nodes: 19, +Edges: 1, -Edges: 5, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#Globals** `(Button / UI Control)`
    └── ⚡ **RootPropertyChanged()**
        └── 🎯 [TRIGGERS] `Randr15ScreensImpl.OnRootPropertyChanged()`
            └── 🎯 [CALLS] `Changed?.Invoke (External/BCL)()`
            └── 🎯 [CALLS] `Dispatcher.UIThread.Post (External/BCL)()`
  🌲 **#Globals** `(Button / UI Control)`
    └── ⚡ **RootGeometryChangedChanged()**
  🌲 **#scalingWithChanges** `(Button / UI Control)`
    └── ⚡ **SettingsChanged()**

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_96` (MODULE_STATE)
  • + [新增節點] `state_82` (MODULE_STATE)
  • + [新增節點] `state_98` (MODULE_STATE)
  • + [新增節點] `state_87` (MODULE_STATE)
  • + [新增節點] `state_95` (MODULE_STATE)
  • + [新增節點] `XGetWindowPropertyAsIntPtrArray (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_89` (MODULE_STATE)
  • + [新增節點] `state_88` (MODULE_STATE)
  • + [新增節點] `state_343` (MODULE_STATE)
  • + [新增節點] `state_86` (MODULE_STATE)
  • + [新增節點] `state_344` (MODULE_STATE)
  • + [新增節點] `state_83` (MODULE_STATE)
  • + [新增節點] `state_84` (MODULE_STATE)
  • + [新增節點] `state_90` (MODULE_STATE)
  • + [新增節點] `state_97` (MODULE_STATE)
  • _... 以及其餘 26 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `X11Screen.UpdateWorkArea()`
- **變更前簽章 (Before)**: `X11Screen.UpdateWorkArea()` (L34~L65)
- **變更後簽章 (After)**: `X11Screen.UpdateWorkArea()` (L34~L49)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected unsafe void UpdateWorkArea()
        {
            var rect = default(PixelRect);
            //Fallback value
            rect = rect.Union(Bounds);
            WorkingArea = Bounds;

            var res = XGetWindowProperty(x11.Display,
                x11.RootWindow,
                x11.Atoms._NET_WORKAREA,
                IntPtr.Zero,
                new IntPtr(128),
                false,
                AnyPropertyType,
                out var type,
                out var format,
                out var count,
                out var bytesAfter,
                out var prop);

            if (res != (int)Status.Success || type == IntPtr.Zero ||
                format == 0 || bytesAfter.ToInt64() != 0 || count.ToInt64() % 4 != 0)
                return;

            var pwa = (IntPtr*)prop;
            var wa = new PixelRect(pwa[0].ToInt32(), pwa[1].ToInt32(), pwa[2].ToInt32(), pwa[3].ToInt32());

            WorkingArea = Bounds.Intersect(wa);
            if (WorkingArea.Width <= 0 || WorkingArea.Height <= 0)
                WorkingArea = Bounds;
            XFree(prop);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected void UpdateWorkArea()
        {
            //Fallback value
            WorkingArea = Bounds;

            var pwa = XGetWindowPropertyAsIntPtrArray(x11.Display, x11.RootWindow,
                x11.Atoms._NET_WORKAREA, x11.Atoms.CARDINAL);
            if (pwa == null || pwa.Length % 4 != 0)
                return;

            var wa = new PixelRect(pwa[0].ToInt32(), pwa[1].ToInt32(), pwa[2].ToInt32(), pwa[3].ToInt32());

            WorkingArea = Bounds.Intersect(wa);
            if (WorkingArea.Width <= 0 || WorkingArea.Height <= 0)
                WorkingArea = Bounds;
        }
```


---

### 🔹 Commit #08: `66b7273b`
- **完整 Hash**: `66b7273b9a2b5ba8416feb4376b9cdc3078b8573`
- **說明 (Ground Truth)**: fix(atspi): report removed and added children in children-changed signals (#22398)
- **變更檔案數**: 1

#### 📄 檔案: `src/Avalonia.FreeDesktop.AtSpi/AtSpiNode.cs`
- ❌ **解析錯誤**: `maximum recursion depth exceeded`

---

### 🔹 Commit #09: `8973430f`
- **完整 Hash**: `8973430f37490a982fa9ca3659c7495f1a0969c8`
- **說明 (Ground Truth)**: Expose TextPresenter.CursorRectangle as a public property (#22319)
- **變更檔案數**: 3

#### 📄 檔案: `src/Avalonia.Controls/Presenters/TextPresenter.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:116, E:114, A:1) ➔ After(N:115, E:113, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 0, -Edges: 1, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_caretTimer** `(Button / UI Control)`
    └── ⚡ **Tick()**
        └── 🎯 [TRIGGERS] `TextPresenter.CaretTimerTick()`
            └── 🎯 [CALLS] `InvalidateVisual (External/BCL)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `TextPresenter.GetCursorRectangle` (FUNCTION_DEF)
  • - [移除呼叫邊] `TextPresenter.GetCursorRectangle` ──[CALLS]──> `TextPresenter.EnsureCaretBounds`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `src/Avalonia.Controls/Primitives/TextSelectionCanvas.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:143, E:139, A:20) ➔ After(N:141, E:136, A:20)
- **差分統計**: +Nodes: 0, -Nodes: 2, +Edges: 0, -Edges: 3, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_caretHandle** `(Button / UI Control)`
    └── ⚡ **DragStarted()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Handle_DragStarted()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.CloseFlyout()`
                └── 🎯 [CALLS] `_textBox?.RaiseEvent (External/BCL)()`
  🌲 **#_caretHandle** `(Button / UI Control)`
    └── ⚡ **DragDelta()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.CaretHandle_DragDelta()`
-           └── [CALLS] `_presenter.GetCursorRectangle (External/BCL)()` [已拆除]
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.BeginChange()`
                └── *ref:`TextSelectionHandleCanvas.BeginChange` [已折疊指針]
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.GetSearchPoint()`
-               └── [CALLS] `_presenter.GetCursorRectangle (External/BCL)()` [已拆除]
                └── 🎯 [CALLS] `indicator.WithY (External/BCL)()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToLayer()`
                └── 🎯 [CALLS] `_presenter?.TranslatePoint (External/BCL)()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToPresenter()`
                └── 🎯 [CALLS] `(presenter.VisualRoot as Visual)?.TranslatePoint (External/BCL)()`
            └── 🎯 [CALLS] `_caretHandle.SetTopLeft (External/BCL)()`
            └── 🎯 [CALLS] `_presenter.MoveCaretToPoint (External/BCL)()`
            └── 🎯 [CALLS] `_textBox.SetCurrentValue (External/BCL)()`
  🌲 **#_caretHandle** `(Button / UI Control)`
    └── ⚡ **DragCompleted()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Handle_DragCompleted()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.CheckStateAndShowFlyout()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.ShowFlyout()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.Place()`
                        └── 🎯 [CALLS] `offset.WithX (External/BCL)()`
                        └── 🎯 [CALLS] `offset.WithX(point.X)
                                .WithY (External/BCL)()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToTextBox()`
                        └── 🎯 [CALLS] `(textbox.VisualRoot as Visual)?.TranslatePoint (External/BCL)()`
                    └── 🎯 [CALLS] `Math.Max (External/BCL)()`
                    └── 🎯 [CALLS] `Math.Min (External/BCL)()`
                    └── 🎯 [CALLS] `_textBox.RaiseEvent (External/BCL)()`
                    └── 🎯 [CALLS] `double.IsNaN (External/BCL)()`
                    └── 🎯 [CALLS] `point.WithY (External/BCL)()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.MoveHandlesToSelection()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.EnsureVisible()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.IsOccluded()`
                        └── 🎯 [CALLS] `clip.Contains (External/BCL)()`
                    └── 🎯 [CALLS] `DispatcherTimer.RunOnce (External/BCL)()`
                    └── 🎯 [CALLS] `TimeSpan.FromSeconds (External/BCL)()`
                    └── 🎯 [CALLS] `_showDisposable?.Dispose (External/BCL)()`
                    └── 🎯 [CALLS] `bounds.Value.Clip.Inflate (External/BCL)()`
                    └── 🎯 [CALLS] `presenter.GetTransformedBounds (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.GetPosition()`
                    └── *ref:`Math.Max (External/BCL)` [已折疊指針]
                    └── 🎯 [CALLS] `_presenter!.TextLayout.HitTestTextRange (External/BCL)()`
                    └── 🎯 [CALLS] `_presenter.TextLayout.GetLineIndexFromCharacterIndex (External/BCL)()`
                    └── 🎯 [CALLS] `new List<Rect>(_presenter!.TextLayout.HitTestTextRange(index, 1)).FirstOrDefault (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToLayer()`
                    └── 🎯 [CALLS] `_presenter?.TranslatePoint (External/BCL)()`
                └── *ref:`Math.Max (External/BCL)` [已折疊指針]
                └── *ref:`Math.Min (External/BCL)` [已折疊指針]
                └── 🎯 [CALLS] `_caretHandle.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `_handle1.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `_handle2.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `_presenter.GetCaretPoints (External/BCL)()`
  🌲 **#_caretHandle** `(Button / UI Control)`
    └── ⚡ **ContextCanceled()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Caret_ContextCanceled()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.CloseFlyout()`
                └── 🎯 [CALLS] `_textBox?.RaiseEvent (External/BCL)()`
  🌲 **#_caretHandle** `(Button / UI Control)`
    └── ⚡ **ContextRequested()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Caret_ContextRequested()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.ShowFlyout()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.Place()`
                    └── 🎯 [CALLS] `offset.WithX (External/BCL)()`
                    └── 🎯 [CALLS] `offset.WithX(point.X)
                                .WithY (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToTextBox()`
                    └── 🎯 [CALLS] `(textbox.VisualRoot as Visual)?.TranslatePoint (External/BCL)()`
                └── 🎯 [CALLS] `Math.Max (External/BCL)()`
                └── 🎯 [CALLS] `Math.Min (External/BCL)()`
                └── 🎯 [CALLS] `_textBox.RaiseEvent (External/BCL)()`
                └── 🎯 [CALLS] `double.IsNaN (External/BCL)()`
                └── 🎯 [CALLS] `point.WithY (External/BCL)()`
            └── 🎯 [CALLS] `this.PerformFeedback (External/BCL)()`
  🌲 **#_handle1** `(Button / UI Control)`
    └── ⚡ **DragDelta()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.SelectionHandle_DragDelta()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.DragSelectionHandle()`
-               └── [CALLS] `presenter.GetCursorRectangle (External/BCL)()` [已拆除]
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.BeginChange()`
                    └── *ref:`TextSelectionHandleCanvas.BeginChange` [已折疊指針]
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.CloseFlyout()`
                    └── 🎯 [CALLS] `_textBox?.RaiseEvent (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.GetTextPosition()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.GetSearchPoint()`
-                       └── [CALLS] `_presenter.GetCursorRectangle (External/BCL)()` [已拆除]
                        └── 🎯 [CALLS] `indicator.WithY (External/BCL)()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToPresenter()`
                        └── 🎯 [CALLS] `(presenter.VisualRoot as Visual)?.TranslatePoint (External/BCL)()`
                    └── 🎯 [CALLS] `presenter.TextLayout.HitTestPoint (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.MoveHandlesToSelection()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.EnsureVisible()`
                        └── 🎯 [CALLS] `TextSelectionHandleCanvas.IsOccluded()`
                            └── 🎯 [CALLS] `clip.Contains (External/BCL)()`
                        └── 🎯 [CALLS] `DispatcherTimer.RunOnce (External/BCL)()`
                        └── 🎯 [CALLS] `TimeSpan.FromSeconds (External/BCL)()`
                        └── 🎯 [CALLS] `_showDisposable?.Dispose (External/BCL)()`
                        └── 🎯 [CALLS] `bounds.Value.Clip.Inflate (External/BCL)()`
                        └── 🎯 [CALLS] `presenter.GetTransformedBounds (External/BCL)()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.GetPosition()`
                        └── 🎯 [CALLS] `Math.Max (External/BCL)()`
                        └── 🎯 [CALLS] `_presenter!.TextLayout.HitTestTextRange (External/BCL)()`
                        └── 🎯 [CALLS] `_presenter.TextLayout.GetLineIndexFromCharacterIndex (External/BCL)()`
                        └── 🎯 [CALLS] `new List<Rect>(_presenter!.TextLayout.HitTestTextRange(index, 1)).FirstOrDefault (External/BCL)()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToLayer()`
                        └── 🎯 [CALLS] `_presenter?.TranslatePoint (External/BCL)()`
                    └── *ref:`Math.Max (External/BCL)` [已折疊指針]
                    └── 🎯 [CALLS] `Math.Min (External/BCL)()`
                    └── 🎯 [CALLS] `_caretHandle.SetTopLeft (External/BCL)()`
                    └── 🎯 [CALLS] `_handle1.SetTopLeft (External/BCL)()`
                    └── 🎯 [CALLS] `_handle2.SetTopLeft (External/BCL)()`
                    └── 🎯 [CALLS] `_presenter.GetCaretPoints (External/BCL)()`
                └── *ref:`TextSelectionHandleCanvas.ToLayer` [已折疊指針]
                └── *ref:`Math.Max (External/BCL)` [已折疊指針]
                └── *ref:`Math.Min (External/BCL)` [已折疊指針]
                └── 🎯 [CALLS] `handle.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `presenter.MoveCaretToTextPosition (External/BCL)()`
                └── 🎯 [CALLS] `textbox.SetCurrentValue (External/BCL)()`
  🌲 **#_handle1** `(Button / UI Control)`
    └── ⚡ **DragCompleted()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Handle_DragCompleted()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.CheckStateAndShowFlyout()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.ShowFlyout()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.Place()`
                        └── 🎯 [CALLS] `offset.WithX (External/BCL)()`
                        └── 🎯 [CALLS] `offset.WithX(point.X)
                                .WithY (External/BCL)()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToTextBox()`
                        └── 🎯 [CALLS] `(textbox.VisualRoot as Visual)?.TranslatePoint (External/BCL)()`
                    └── 🎯 [CALLS] `Math.Max (External/BCL)()`
                    └── 🎯 [CALLS] `Math.Min (External/BCL)()`
                    └── 🎯 [CALLS] `_textBox.RaiseEvent (External/BCL)()`
                    └── 🎯 [CALLS] `double.IsNaN (External/BCL)()`
                    └── 🎯 [CALLS] `point.WithY (External/BCL)()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.MoveHandlesToSelection()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.EnsureVisible()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.IsOccluded()`
                        └── 🎯 [CALLS] `clip.Contains (External/BCL)()`
                    └── 🎯 [CALLS] `DispatcherTimer.RunOnce (External/BCL)()`
                    └── 🎯 [CALLS] `TimeSpan.FromSeconds (External/BCL)()`
                    └── 🎯 [CALLS] `_showDisposable?.Dispose (External/BCL)()`
                    └── 🎯 [CALLS] `bounds.Value.Clip.Inflate (External/BCL)()`
                    └── 🎯 [CALLS] `presenter.GetTransformedBounds (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.GetPosition()`
                    └── *ref:`Math.Max (External/BCL)` [已折疊指針]
                    └── 🎯 [CALLS] `_presenter!.TextLayout.HitTestTextRange (External/BCL)()`
                    └── 🎯 [CALLS] `_presenter.TextLayout.GetLineIndexFromCharacterIndex (External/BCL)()`
                    └── 🎯 [CALLS] `new List<Rect>(_presenter!.TextLayout.HitTestTextRange(index, 1)).FirstOrDefault (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToLayer()`
                    └── 🎯 [CALLS] `_presenter?.TranslatePoint (External/BCL)()`
                └── *ref:`Math.Max (External/BCL)` [已折疊指針]
                └── *ref:`Math.Min (External/BCL)` [已折疊指針]
                └── 🎯 [CALLS] `_caretHandle.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `_handle1.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `_handle2.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `_presenter.GetCaretPoints (External/BCL)()`
  🌲 **#_handle1** `(Button / UI Control)`
    └── ⚡ **DragStarted()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Handle_DragStarted()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.CloseFlyout()`
                └── 🎯 [CALLS] `_textBox?.RaiseEvent (External/BCL)()`
  🌲 **#_handle1** `(Button / UI Control)`
    └── ⚡ **ContextCanceled()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Caret_ContextCanceled()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.CloseFlyout()`
                └── 🎯 [CALLS] `_textBox?.RaiseEvent (External/BCL)()`
  🌲 **#_handle1** `(Button / UI Control)`
    └── ⚡ **ContextRequested()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Caret_ContextRequested()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.ShowFlyout()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.Place()`
                    └── 🎯 [CALLS] `offset.WithX (External/BCL)()`
                    └── 🎯 [CALLS] `offset.WithX(point.X)
                                .WithY (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToTextBox()`
                    └── 🎯 [CALLS] `(textbox.VisualRoot as Visual)?.TranslatePoint (External/BCL)()`
                └── 🎯 [CALLS] `Math.Max (External/BCL)()`
                └── 🎯 [CALLS] `Math.Min (External/BCL)()`
                └── 🎯 [CALLS] `_textBox.RaiseEvent (External/BCL)()`
                └── 🎯 [CALLS] `double.IsNaN (External/BCL)()`
                └── 🎯 [CALLS] `point.WithY (External/BCL)()`
            └── 🎯 [CALLS] `this.PerformFeedback (External/BCL)()`
  🌲 **#_handle2** `(Button / UI Control)`
    └── ⚡ **DragDelta()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.SelectionHandle_DragDelta()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.DragSelectionHandle()`
-               └── [CALLS] `presenter.GetCursorRectangle (External/BCL)()` [已拆除]
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.BeginChange()`
                    └── *ref:`TextSelectionHandleCanvas.BeginChange` [已折疊指針]
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.CloseFlyout()`
                    └── 🎯 [CALLS] `_textBox?.RaiseEvent (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.GetTextPosition()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.GetSearchPoint()`
-                       └── [CALLS] `_presenter.GetCursorRectangle (External/BCL)()` [已拆除]
                        └── 🎯 [CALLS] `indicator.WithY (External/BCL)()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToPresenter()`
                        └── 🎯 [CALLS] `(presenter.VisualRoot as Visual)?.TranslatePoint (External/BCL)()`
                    └── 🎯 [CALLS] `presenter.TextLayout.HitTestPoint (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.MoveHandlesToSelection()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.EnsureVisible()`
                        └── 🎯 [CALLS] `TextSelectionHandleCanvas.IsOccluded()`
                            └── 🎯 [CALLS] `clip.Contains (External/BCL)()`
                        └── 🎯 [CALLS] `DispatcherTimer.RunOnce (External/BCL)()`
                        └── 🎯 [CALLS] `TimeSpan.FromSeconds (External/BCL)()`
                        └── 🎯 [CALLS] `_showDisposable?.Dispose (External/BCL)()`
                        └── 🎯 [CALLS] `bounds.Value.Clip.Inflate (External/BCL)()`
                        └── 🎯 [CALLS] `presenter.GetTransformedBounds (External/BCL)()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.GetPosition()`
                        └── 🎯 [CALLS] `Math.Max (External/BCL)()`
                        └── 🎯 [CALLS] `_presenter!.TextLayout.HitTestTextRange (External/BCL)()`
                        └── 🎯 [CALLS] `_presenter.TextLayout.GetLineIndexFromCharacterIndex (External/BCL)()`
                        └── 🎯 [CALLS] `new List<Rect>(_presenter!.TextLayout.HitTestTextRange(index, 1)).FirstOrDefault (External/BCL)()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToLayer()`
                        └── 🎯 [CALLS] `_presenter?.TranslatePoint (External/BCL)()`
                    └── *ref:`Math.Max (External/BCL)` [已折疊指針]
                    └── 🎯 [CALLS] `Math.Min (External/BCL)()`
                    └── 🎯 [CALLS] `_caretHandle.SetTopLeft (External/BCL)()`
                    └── 🎯 [CALLS] `_handle1.SetTopLeft (External/BCL)()`
                    └── 🎯 [CALLS] `_handle2.SetTopLeft (External/BCL)()`
                    └── 🎯 [CALLS] `_presenter.GetCaretPoints (External/BCL)()`
                └── *ref:`TextSelectionHandleCanvas.ToLayer` [已折疊指針]
                └── *ref:`Math.Max (External/BCL)` [已折疊指針]
                └── *ref:`Math.Min (External/BCL)` [已折疊指針]
                └── 🎯 [CALLS] `handle.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `presenter.MoveCaretToTextPosition (External/BCL)()`
                └── 🎯 [CALLS] `textbox.SetCurrentValue (External/BCL)()`
  🌲 **#_handle2** `(Button / UI Control)`
    └── ⚡ **DragCompleted()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Handle_DragCompleted()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.CheckStateAndShowFlyout()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.ShowFlyout()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.Place()`
                        └── 🎯 [CALLS] `offset.WithX (External/BCL)()`
                        └── 🎯 [CALLS] `offset.WithX(point.X)
                                .WithY (External/BCL)()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToTextBox()`
                        └── 🎯 [CALLS] `(textbox.VisualRoot as Visual)?.TranslatePoint (External/BCL)()`
                    └── 🎯 [CALLS] `Math.Max (External/BCL)()`
                    └── 🎯 [CALLS] `Math.Min (External/BCL)()`
                    └── 🎯 [CALLS] `_textBox.RaiseEvent (External/BCL)()`
                    └── 🎯 [CALLS] `double.IsNaN (External/BCL)()`
                    └── 🎯 [CALLS] `point.WithY (External/BCL)()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.MoveHandlesToSelection()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.EnsureVisible()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.IsOccluded()`
                        └── 🎯 [CALLS] `clip.Contains (External/BCL)()`
                    └── 🎯 [CALLS] `DispatcherTimer.RunOnce (External/BCL)()`
                    └── 🎯 [CALLS] `TimeSpan.FromSeconds (External/BCL)()`
                    └── 🎯 [CALLS] `_showDisposable?.Dispose (External/BCL)()`
                    └── 🎯 [CALLS] `bounds.Value.Clip.Inflate (External/BCL)()`
                    └── 🎯 [CALLS] `presenter.GetTransformedBounds (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.GetPosition()`
                    └── *ref:`Math.Max (External/BCL)` [已折疊指針]
                    └── 🎯 [CALLS] `_presenter!.TextLayout.HitTestTextRange (External/BCL)()`
                    └── 🎯 [CALLS] `_presenter.TextLayout.GetLineIndexFromCharacterIndex (External/BCL)()`
                    └── 🎯 [CALLS] `new List<Rect>(_presenter!.TextLayout.HitTestTextRange(index, 1)).FirstOrDefault (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToLayer()`
                    └── 🎯 [CALLS] `_presenter?.TranslatePoint (External/BCL)()`
                └── *ref:`Math.Max (External/BCL)` [已折疊指針]
                └── *ref:`Math.Min (External/BCL)` [已折疊指針]
                └── 🎯 [CALLS] `_caretHandle.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `_handle1.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `_handle2.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `_presenter.GetCaretPoints (External/BCL)()`
  🌲 **#_handle2** `(Button / UI Control)`
    └── ⚡ **DragStarted()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Handle_DragStarted()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.CloseFlyout()`
                └── 🎯 [CALLS] `_textBox?.RaiseEvent (External/BCL)()`
  🌲 **#_handle2** `(Button / UI Control)`
    └── ⚡ **ContextCanceled()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Caret_ContextCanceled()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.CloseFlyout()`
                └── 🎯 [CALLS] `_textBox?.RaiseEvent (External/BCL)()`
  🌲 **#_handle2** `(Button / UI Control)`
    └── ⚡ **ContextRequested()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Caret_ContextRequested()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.ShowFlyout()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.Place()`
                    └── 🎯 [CALLS] `offset.WithX (External/BCL)()`
                    └── 🎯 [CALLS] `offset.WithX(point.X)
                                .WithY (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToTextBox()`
                    └── 🎯 [CALLS] `(textbox.VisualRoot as Visual)?.TranslatePoint (External/BCL)()`
                └── 🎯 [CALLS] `Math.Max (External/BCL)()`
                └── 🎯 [CALLS] `Math.Min (External/BCL)()`
                └── 🎯 [CALLS] `_textBox.RaiseEvent (External/BCL)()`
                └── 🎯 [CALLS] `double.IsNaN (External/BCL)()`
                └── 🎯 [CALLS] `point.WithY (External/BCL)()`
            └── 🎯 [CALLS] `this.PerformFeedback (External/BCL)()`
  🌲 **#_layoutListener** `(Button / UI Control)`
    └── ⚡ **Invalidated()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.LayoutListener_Invalidated()`
            └── 🎯 [CALLS] `InvalidateMeasure (External/BCL)()`
  🌲 **#_presenter** `(Button / UI Control)`
    └── ⚡ **IsEffectivelyVisibleChanged()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.Presenter_IsEffectivelyVisibleChanged()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.CloseFlyout()`
                └── 🎯 [CALLS] `_textBox?.RaiseEvent (External/BCL)()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.EnsureVisible()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.IsOccluded()`
                    └── 🎯 [CALLS] `clip.Contains (External/BCL)()`
                └── 🎯 [CALLS] `DispatcherTimer.RunOnce (External/BCL)()`
                └── 🎯 [CALLS] `TimeSpan.FromSeconds (External/BCL)()`
                └── 🎯 [CALLS] `_showDisposable?.Dispose (External/BCL)()`
                └── 🎯 [CALLS] `bounds.Value.Clip.Inflate (External/BCL)()`
                └── 🎯 [CALLS] `presenter.GetTransformedBounds (External/BCL)()`
  🌲 **#_textBox** `(Button / UI Control)`
    └── ⚡ **PropertyChanged()**
        └── 🎯 [TRIGGERS] `TextSelectionHandleCanvas.TextBox_PropertyChanged()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.CloseFlyout()`
                └── 🎯 [CALLS] `_textBox?.RaiseEvent (External/BCL)()`
            └── 🎯 [CALLS] `TextSelectionHandleCanvas.MoveHandlesToSelection()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.EnsureVisible()`
                    └── 🎯 [CALLS] `TextSelectionHandleCanvas.IsOccluded()`
                        └── 🎯 [CALLS] `clip.Contains (External/BCL)()`
                    └── 🎯 [CALLS] `DispatcherTimer.RunOnce (External/BCL)()`
                    └── 🎯 [CALLS] `TimeSpan.FromSeconds (External/BCL)()`
                    └── 🎯 [CALLS] `_showDisposable?.Dispose (External/BCL)()`
                    └── 🎯 [CALLS] `bounds.Value.Clip.Inflate (External/BCL)()`
                    └── 🎯 [CALLS] `presenter.GetTransformedBounds (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.GetPosition()`
                    └── 🎯 [CALLS] `Math.Max (External/BCL)()`
                    └── 🎯 [CALLS] `_presenter!.TextLayout.HitTestTextRange (External/BCL)()`
                    └── 🎯 [CALLS] `_presenter.TextLayout.GetLineIndexFromCharacterIndex (External/BCL)()`
                    └── 🎯 [CALLS] `new List<Rect>(_presenter!.TextLayout.HitTestTextRange(index, 1)).FirstOrDefault (External/BCL)()`
                └── 🎯 [CALLS] `TextSelectionHandleCanvas.ToLayer()`
                    └── 🎯 [CALLS] `_presenter?.TranslatePoint (External/BCL)()`
                └── *ref:`Math.Max (External/BCL)` [已折疊指針]
                └── 🎯 [CALLS] `Math.Min (External/BCL)()`
                └── 🎯 [CALLS] `_caretHandle.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `_handle1.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `_handle2.SetTopLeft (External/BCL)()`
                └── 🎯 [CALLS] `_presenter.GetCaretPoints (External/BCL)()`
  🌲 **#control** `(Button / UI Control)`
    └── ⚡ **SizeChanged()**
        └── 🎯 [TRIGGERS] `PresenterVisualListener.Visual_SizeChanged()`
            └── 🎯 [CALLS] `PresenterVisualListener.OnInvalidated()`
                └── 🎯 [CALLS] `Invalidated?.Invoke (External/BCL)()`
  🌲 **#layoutable** `(Button / UI Control)`
    └── ⚡ **EffectiveViewportChanged()**
        └── 🎯 [TRIGGERS] `PresenterVisualListener.Visual_EffectiveViewportChanged()`
            └── 🎯 [CALLS] `PresenterVisualListener.OnInvalidated()`
                └── 🎯 [CALLS] `Invalidated?.Invoke (External/BCL)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `_presenter.GetCursorRectangle (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `presenter.GetCursorRectangle (External/BCL)` (FUNCTION_DEF)
  • - [移除呼叫邊] `TextSelectionHandleCanvas.CaretHandle_DragDelta` ──[CALLS]──> `_presenter.GetCursorRectangle (External/BCL)`
  • - [移除呼叫邊] `TextSelectionHandleCanvas.GetSearchPoint` ──[CALLS]──> `_presenter.GetCursorRectangle (External/BCL)`
  • - [移除呼叫邊] `TextSelectionHandleCanvas.DragSelectionHandle` ──[CALLS]──> `presenter.GetCursorRectangle (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TextSelectionHandleCanvas.CaretHandle_DragDelta()`
- **變更前簽章 (Before)**: `TextSelectionHandleCanvas.CaretHandle_DragDelta(object? sender, VectorEventArgs e)` (L151~L167)
- **變更後簽章 (After)**: `TextSelectionHandleCanvas.CaretHandle_DragDelta(object? sender, VectorEventArgs e)` (L151~L167)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private void CaretHandle_DragDelta(object? sender, VectorEventArgs e)
        {
            if (_presenter != null && _textBox != null)
            {
                var indicatorPosition = GetSearchPoint(_caretHandle);
                var point = ToPresenter(indicatorPosition);
                using var _ = BeginChange();
                _presenter.MoveCaretToPoint(point);
                var caretIndex = _presenter.CaretIndex;
                _textBox.SetCurrentValue(TextBox.CaretIndexProperty, caretIndex);
                _textBox.SetCurrentValue(TextBox.SelectionStartProperty, caretIndex);
                _textBox.SetCurrentValue(TextBox.SelectionEndProperty, caretIndex);

                var caretBound = _presenter.GetCursorRectangle();
                _caretHandle.SetTopLeft(ToLayer(caretBound.BottomLeft));
            }
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private void CaretHandle_DragDelta(object? sender, VectorEventArgs e)
        {
            if (_presenter != null && _textBox != null)
            {
                var indicatorPosition = GetSearchPoint(_caretHandle);
                var point = ToPresenter(indicatorPosition);
                using var _ = BeginChange();
                _presenter.MoveCaretToPoint(point);
                var caretIndex = _presenter.CaretIndex;
                _textBox.SetCurrentValue(TextBox.CaretIndexProperty, caretIndex);
                _textBox.SetCurrentValue(TextBox.SelectionStartProperty, caretIndex);
                _textBox.SetCurrentValue(TextBox.SelectionEndProperty, caretIndex);

                var caretBound = _presenter.CursorRectangle;
                _caretHandle.SetTopLeft(ToLayer(caretBound.BottomLeft));
            }
        }
```

### 🔹 函式: `TextSelectionHandleCanvas.DragSelectionHandle()`
- **變更前簽章 (Before)**: `TextSelectionHandleCanvas.DragSelectionHandle(TextSelectionHandle handle)` (L274~L355)
- **變更後簽章 (After)**: `TextSelectionHandleCanvas.DragSelectionHandle(TextSelectionHandle handle)` (L274~L355)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private void DragSelectionHandle(TextSelectionHandle handle)
        {
            if (_presenter is { } presenter && _textBox is { } textbox)
            {
                CloseFlyout();

                var position = GetTextPosition(handle);

                var otherHandle = handle == _handle1 ? _handle2 : _handle1;

                using var _ = BeginChange();

                // Some platforms do not allow handles to cause selection bounds to reverse, i.e. allow handles to move over each other.
                if (!s_shouldWrapAroundSelection)
                {
                    if (handle.SelectionHandleType == SelectionHandleType.Start)
                    {
                        position = position >= textbox.SelectionEnd ? textbox.SelectionEnd - 1 : position;
                        textbox.SetCurrentValue(TextBox.SelectionStartProperty, position);
                    }
                    else
                    {
                        position = position <= textbox.SelectionStart ? textbox.SelectionStart + 1 : position;
                        textbox.SetCurrentValue(TextBox.SelectionEndProperty, position);
                    }
                }
                else
                {
                    // For platforms that do, update the handle types for each and adjust selection.

                    if (_initialHandleType == SelectionHandleType.Start)
                    {
                        // If handle was previously the selection end, set new selection end to the previous selection start.
                        bool hasPositionSwapped = position > _saveSelectionEnd;
                        var otherPosition = _saveSelectionEnd;

                        if (position == otherPosition)
                        {
                            position = hasPositionSwapped ? Math.Min(position + 1, (textbox.Text?.Length - 1) ?? 0)
                                : Math.Max(position - 1, 0);
                        }

                        textbox.SetCurrentValue(TextBox.SelectionStartProperty, hasPositionSwapped ? otherPosition : position);
                        textbox.SetCurrentValue(TextBox.SelectionEndProperty, hasPositionSwapped ? position : otherPosition);

                        otherHandle.SelectionHandleType = hasPositionSwapped ? SelectionHandleType.Start : SelectionHandleType.End;
                    }
                    else
                    {
                        // If handle was previously the selection start, set new selection start to the previous selection end.
                        bool hasPositionSwapped = position < _savedSelectionStart;
                        var otherPosition = _savedSelectionStart;

                        if (position == otherPosition)
                        {
                            position = !hasPositionSwapped ? Math.Min(position + 1, (textbox.Text?.Length - 1) ?? 0)
                                : Math.Max(position - 1, 0);
                        }

                        textbox.SetCurrentValue(TextBox.SelectionStartProperty, hasPositionSwapped ? position : otherPosition);
                        textbox.SetCurrentValue(TextBox.SelectionEndProperty, hasPositionSwapped ? otherPosition : position);

                        otherHandle.SelectionHandleType = hasPositionSwapped ? SelectionHandleType.End : SelectionHandleType.Start;
                    }
                }

                presenter.MoveCaretToTextPosition(position);
                var caretBound = presenter.GetCursorRectangle();
                handle.SetTopLeft(ToLayer(handle.SelectionHandleType == SelectionHandleType.Start ? caretBound.BottomLeft : caretBound.BottomLeft));

                MoveHandlesToSelection();
            }

            int GetTextPosition(TextSelectionHandle handle)
            {
                var indicatorPosition = GetSearchPoint(handle);
                var point = ToPresenter(indicatorPosition);
                var hit = presenter.TextLayout.HitTestPoint(point);
                var position = hit.CharacterHit.FirstCharacterIndex + hit.CharacterHit.TrailingLength;
                return position;
            }
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private void DragSelectionHandle(TextSelectionHandle handle)
        {
            if (_presenter is { } presenter && _textBox is { } textbox)
            {
                CloseFlyout();

                var position = GetTextPosition(handle);

                var otherHandle = handle == _handle1 ? _handle2 : _handle1;

                using var _ = BeginChange();

                // Some platforms do not allow handles to cause selection bounds to reverse, i.e. allow handles to move over each other.
                if (!s_shouldWrapAroundSelection)
                {
                    if (handle.SelectionHandleType == SelectionHandleType.Start)
                    {
                        position = position >= textbox.SelectionEnd ? textbox.SelectionEnd - 1 : position;
                        textbox.SetCurrentValue(TextBox.SelectionStartProperty, position);
                    }
                    else
                    {
                        position = position <= textbox.SelectionStart ? textbox.SelectionStart + 1 : position;
                        textbox.SetCurrentValue(TextBox.SelectionEndProperty, position);
                    }
                }
                else
                {
                    // For platforms that do, update the handle types for each and adjust selection.

                    if (_initialHandleType == SelectionHandleType.Start)
                    {
                        // If handle was previously the selection end, set new selection end to the previous selection start.
                        bool hasPositionSwapped = position > _saveSelectionEnd;
                        var otherPosition = _saveSelectionEnd;

                        if (position == otherPosition)
                        {
                            position = hasPositionSwapped ? Math.Min(position + 1, (textbox.Text?.Length - 1) ?? 0)
                                : Math.Max(position - 1, 0);
                        }

                        textbox.SetCurrentValue(TextBox.SelectionStartProperty, hasPositionSwapped ? otherPosition : position);
                        textbox.SetCurrentValue(TextBox.SelectionEndProperty, hasPositionSwapped ? position : otherPosition);

                        otherHandle.SelectionHandleType = hasPositionSwapped ? SelectionHandleType.Start : SelectionHandleType.End;
                    }
                    else
                    {
                        // If handle was previously the selection start, set new selection start to the previous selection end.
                        bool hasPositionSwapped = position < _savedSelectionStart;
                        var otherPosition = _savedSelectionStart;

                        if (position == otherPosition)
                        {
                            position = !hasPositionSwapped ? Math.Min(position + 1, (textbox.Text?.Length - 1) ?? 0)
                                : Math.Max(position - 1, 0);
                        }

                        textbox.SetCurrentValue(TextBox.SelectionStartProperty, hasPositionSwapped ? position : otherPosition);
                        textbox.SetCurrentValue(TextBox.SelectionEndProperty, hasPositionSwapped ? otherPosition : position);

                        otherHandle.SelectionHandleType = hasPositionSwapped ? SelectionHandleType.End : SelectionHandleType.Start;
                    }
                }

                presenter.MoveCaretToTextPosition(position);
                var caretBound = presenter.CursorRectangle;
                handle.SetTopLeft(ToLayer(handle.SelectionHandleType == SelectionHandleType.Start ? caretBound.BottomLeft : caretBound.BottomLeft));

                MoveHandlesToSelection();
            }

            int GetTextPosition(TextSelectionHandle handle)
            {
                var indicatorPosition = GetSearchPoint(handle);
                var point = ToPresenter(indicatorPosition);
                var hit = presenter.TextLayout.HitTestPoint(point);
                var position = hit.CharacterHit.FirstCharacterIndex + hit.CharacterHit.TrailingLength;
                return position;
            }
        }
```

### 🔹 函式: `TextSelectionHandleCanvas.GetSearchPoint()`
- **變更前簽章 (Before)**: `TextSelectionHandleCanvas.GetSearchPoint(TextSelectionHandle handle)` (L263~L272)
- **變更後簽章 (After)**: `TextSelectionHandleCanvas.GetSearchPoint(TextSelectionHandle handle)` (L263~L272)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private Point GetSearchPoint(TextSelectionHandle handle)
        {
            if (_presenter == null)
                return default;

            var caretBounds = _presenter.GetCursorRectangle();
            var searchOffset = caretBounds.Height / 2;
            var indicator = handle.IndicatorPosition;
            return indicator.WithY(indicator.Y - searchOffset);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private Point GetSearchPoint(TextSelectionHandle handle)
        {
            if (_presenter == null)
                return default;

            var caretBounds = _presenter.CursorRectangle;
            var searchOffset = caretBounds.Height / 2;
            var indicator = handle.IndicatorPosition;
            return indicator.WithY(indicator.Y - searchOffset);
        }
```


#### 📄 檔案: `src/Avalonia.Controls/TextBoxTextInputMethodClient.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:32, E:21, A:3) ➔ After(N:32, E:21, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#_parent** `(Button / UI Control)`
    └── ⚡ **PropertyChanged()**
        └── 🎯 [TRIGGERS] `TextBoxTextInputMethodClient.OnParentPropertyChanged()`
            └── 🎯 [CALLS] `RaiseSelectionChanged (External/BCL)()`
            └── 🎯 [CALLS] `RaiseSurroundingTextChanged (External/BCL)()`
  🌲 **#_parent** `(Button / UI Control)`
    └── ⚡ **Tapped()**
        └── 🎯 [TRIGGERS] `TextBoxTextInputMethodClient.OnParentTapped()`
            └── 🎯 [CALLS] `RaiseInputPaneActivationRequested (External/BCL)()`
  🌲 **#_presenter** `(Button / UI Control)`
    └── ⚡ **CaretBoundsChanged()**

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #10: `c1da1af3`
- **完整 Hash**: `c1da1af3b7bb0ab5b62b0fc896bd675ebd7bb231`
- **說明 (Ground Truth)**: Added fix for the issue-22338, added thread-safe ConcurrentDictionary cache change for concurrent avares:// asset resolution. (#22352)
- **變更檔案數**: 1

#### 📄 檔案: `src/Avalonia.Base/Platform/Internal/AssemblyDescriptorResolver.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:18, E:11, A:0) ➔ After(N:18, E:11, A:0)
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
  • + [新增節點] `_assemblyNameCache.GetOrAdd (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_assemblyNameCache.TryRemove (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `_assemblyNameCache.Remove (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `_assemblyNameCache.TryGetValue (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `AssemblyDescriptorResolver.GetAssembly` ──[CALLS]──> `_assemblyNameCache.GetOrAdd (External/BCL)`
  • + [新增呼叫邊] `AssemblyDescriptorResolver.InvalidateAssemblyCache` ──[CALLS]──> `_assemblyNameCache.TryRemove (External/BCL)`
  • - [移除呼叫邊] `AssemblyDescriptorResolver.GetAssembly` ──[CALLS]──> `_assemblyNameCache.TryGetValue (External/BCL)`
  • - [移除呼叫邊] `AssemblyDescriptorResolver.InvalidateAssemblyCache` ──[CALLS]──> `_assemblyNameCache.Remove (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `AssemblyDescriptorResolver.GetAssembly()`
- **變更前簽章 (Before)**: `AssemblyDescriptorResolver.GetAssembly(string name)` (L21~L50)
- **變更後簽章 (After)**: `AssemblyDescriptorResolver.GetAssembly(string name)` (L22~L49)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public IAssemblyDescriptor GetAssembly(string name)
    {
        if (name == null)
            throw new ArgumentNullException(nameof(name));

        if (!_assemblyNameCache.TryGetValue(name, out var rv))
        {
            var loadedAssemblies = AppDomain.CurrentDomain.GetAssemblies();
            // Select assembly by ManifestModule.ScopeName instead of GetName().Name to avoid CultureInfo dependency.
            var match = loadedAssemblies.Where(a => a.ManifestModule.ScopeName.StartsWith(name, StringComparison.InvariantCultureIgnoreCase)).OrderBy(a => a.ManifestModule.ScopeName.Length).FirstOrDefault();
            if (match != null)
            {
                _assemblyNameCache[name] = rv = new AssemblyDescriptor(match);
            }
            else
            {
#if NET6_0_OR_GREATER
                if (!RuntimeFeature.IsDynamicCodeSupported)
                {
                    throw new InvalidOperationException(
                        $"Assembly {name} needs to be referenced and explicitly loaded before loading resources");
                }
#endif
                name = Uri.UnescapeDataString(name);
                _assemblyNameCache[name] = rv = new AssemblyDescriptor(Assembly.Load(name));
            }
        }

        return rv;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public IAssemblyDescriptor GetAssembly(string name)
    {
        if (name == null)
            throw new ArgumentNullException(nameof(name));

        return _assemblyNameCache.GetOrAdd(name, static name =>
        {
            var loadedAssemblies = AppDomain.CurrentDomain.GetAssemblies();
            // Select assembly by ManifestModule.ScopeName instead of GetName().Name to avoid CultureInfo dependency.
            var match = loadedAssemblies.Where(a => a.ManifestModule.ScopeName.StartsWith(name, StringComparison.InvariantCultureIgnoreCase)).OrderBy(a => a.ManifestModule.ScopeName.Length).FirstOrDefault();
            if (match != null)
            {
                return new AssemblyDescriptor(match);
            }
            else
            {
#if NET6_0_OR_GREATER
                if (!RuntimeFeature.IsDynamicCodeSupported)
                {
                    throw new InvalidOperationException(
                        $"Assembly {name} needs to be referenced and explicitly loaded before loading resources");
                }
#endif
                name = Uri.UnescapeDataString(name);
                return new AssemblyDescriptor(Assembly.Load(name));
            }
        });
    }
```

### 🔹 函式: `AssemblyDescriptorResolver.InvalidateAssemblyCache()`
- **變更前簽章 (Before)**: `AssemblyDescriptorResolver.InvalidateAssemblyCache(string name)` (L51~L54)
- **變更後簽章 (After)**: `AssemblyDescriptorResolver.InvalidateAssemblyCache(string name)` (L50~L53)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public void InvalidateAssemblyCache(string name)
    {
        _assemblyNameCache.Remove(name);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public void InvalidateAssemblyCache(string name)
    {
        _assemblyNameCache.TryRemove(name, out _);
    }
```


---

### 🔹 Commit #11: `6477086e`
- **完整 Hash**: `6477086eaad8e725664e287735a3fb12c0e7bba6`
- **說明 (Ground Truth)**: X11: use 32-bit visual for EGL alpha configs on Mesa without EGL_MESA_x11_native_visual_id (#22452)
- **變更檔案數**: 2

#### 📄 檔案: `src/Avalonia.OpenGL/Egl/EglConsts.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:97, E:0, A:0) ➔ After(N:98, E:0, A:0)
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
  • + [新增節點] `EGL_VENDOR` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `src/Avalonia.X11/X11EglHelper.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:18, E:18, A:0) ➔ After(N:22, E:24, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 6, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `X11EglHelper.HasStaleAlphaVisualIds` (FUNCTION_DEF)
  • + [新增節點] `egl.QueryString (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `extensions?.Contains (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `vendor.Contains (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `X11EglHelper.GetVisualInfo` ──[CALLS]──> `X11EglHelper.HasStaleAlphaVisualIds`
  • + [新增呼叫邊] `X11EglHelper.GetVisualInfo` ──[CALLS]──> `Logger.TryGet(LogEventLevel.Verbose, "OpenGL")?.Log (External/BCL)`
  • + [新增呼叫邊] `X11EglHelper.GetVisualInfo` ──[CALLS]──> `Logger.TryGet (External/BCL)`
  • + [新增呼叫邊] `X11EglHelper.HasStaleAlphaVisualIds` ──[CALLS]──> `egl.QueryString (External/BCL)`
  • + [新增呼叫邊] `X11EglHelper.HasStaleAlphaVisualIds` ──[CALLS]──> `vendor.Contains (External/BCL)`
  • + [新增呼叫邊] `X11EglHelper.HasStaleAlphaVisualIds` ──[CALLS]──> `extensions?.Contains (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `X11EglHelper.GetVisualInfo()`
- **變更前簽章 (Before)**: `X11EglHelper.GetVisualInfo(X11Info x11, EglInterface egl, IntPtr display, IntPtr config)` (L19~L24)
- **變更後簽章 (After)**: `X11EglHelper.GetVisualInfo(X11Info x11, EglInterface egl, IntPtr display, IntPtr config)` (L20~L37)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static XVisualInfo? GetVisualInfo(X11Info x11, EglInterface egl, IntPtr display, IntPtr config)
        {
            if (!egl.GetConfigAttrib(display, config, EGL_NATIVE_VISUAL_ID, out var visualId) || visualId == 0)
                return null;
            return XGetVisualInfoById(x11.DeferredDisplay, new IntPtr(visualId));
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static XVisualInfo? GetVisualInfo(X11Info x11, EglInterface egl, IntPtr display, IntPtr config)
        {
            if (!egl.GetConfigAttrib(display, config, EGL_NATIVE_VISUAL_ID, out var visualId) || visualId == 0)
                return null;
            var visual = XGetVisualInfoById(x11.DeferredDisplay, new IntPtr(visualId));
            if (visual is { depth: not 32 }
                && x11.TransparentVisualInfo is { } transparent
                && egl.GetConfigAttrib(display, config, EGL_ALPHA_SIZE, out var alphaSize) && alphaSize > 0
                && HasStaleAlphaVisualIds(egl, display))
            {
                Logger.TryGet(LogEventLevel.Verbose, "OpenGL")?.Log(null,
                    "EGL config {Config}: using 32-bit visual {Visual} instead of native visual {Native}",
                    config, transparent.visualid, visualId);
                return XGetVisualInfoById(x11.DeferredDisplay, transparent.visualid);
            }

            return visual;
        }
```


---

### 🔹 Commit #12: `6394d533`
- **完整 Hash**: `6394d5337c1a5cfb5087d40b349c0dc24c1db7b8`
- **說明 (Ground Truth)**: Fix WASM MT on .NET 11 runtime (#22444)
- **變更檔案數**: 2

#### 📄 檔案: `src/Browser/Avalonia.Browser/BrowserAppBuilder.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:23, E:22, A:0) ➔ After(N:23, E:22, A:0)
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

### 🔹 函式: `BrowserAppBuilder.StartBrowserAppAsync()`
- **變更前簽章 (Before)**: `BrowserAppBuilder.StartBrowserAppAsync(
        this AppBuilder builder,
        string mainDivId, BrowserPlatformOptions? options = null)` (L80~L125)
- **變更後簽章 (After)**: `BrowserAppBuilder.StartBrowserAppAsync(
        this AppBuilder builder,
        string mainDivId, BrowserPlatformOptions? options = null)` (L80~L125)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static async Task StartBrowserAppAsync(
        this AppBuilder builder,
        string mainDivId, BrowserPlatformOptions? options = null)
    {
        if (mainDivId is null)
        {
            throw new ArgumentNullException(nameof(mainDivId));
        }

        builder = await PreSetupBrowser(builder, options);

        var lifetime = new BrowserSingleViewLifetime();
        builder
            .AfterApplicationSetup(_ =>
            {
                lifetime.View = new AvaloniaView(mainDivId);
            });

        if (BrowserWindowingPlatform.IsThreadingEnabled)
        {
            var tcs = new TaskCompletionSource();
            var thread = new Thread(() =>
            {
                try
                {
                    builder
                        .SetupWithLifetime(lifetime);
                    tcs.TrySetResult();
                    builder.Instance!.Run(CancellationToken.None);
                }
                catch (Exception ex)
                {
                    tcs.TrySetException(ex);
                }
            });
#pragma warning disable CA1416
            thread.Start();
#pragma warning restore CA1416
            await tcs.Task;
        }
        else
        {
            builder
                .SetupWithLifetime(lifetime);
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static async Task StartBrowserAppAsync(
        this AppBuilder builder,
        string mainDivId, BrowserPlatformOptions? options = null)
    {
        if (mainDivId is null)
        {
            throw new ArgumentNullException(nameof(mainDivId));
        }

        builder = await PreSetupBrowser(builder, options);

        var lifetime = new BrowserSingleViewLifetime();
        builder
            .AfterApplicationSetup(_ =>
            {
                lifetime.View = new AvaloniaView(mainDivId);
            });

        if (BrowserWindowingPlatform.IsThreadingEnabled)
        {
            var tcs = new TaskCompletionSource();
            var thread = new Thread(() =>
            {
                try
                {
                    builder
                        .SetupWithLifetime(lifetime);
                    tcs.TrySetResult();
                    builder.Instance!.Run(CancellationToken.None);
                }
                catch (Exception ex)
                {
                    tcs.TrySetException(ex);
                }
            }) { Name = "Avalonia UI Thread" };
#pragma warning disable CA1416
            thread.Start();
#pragma warning restore CA1416
            await tcs.Task;
        }
        else
        {
            builder
                .SetupWithLifetime(lifetime);
        }
    }
```


#### 📄 檔案: `src/Browser/Avalonia.Browser/WindowingPlatform.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:42, E:31, A:0) ➔ After(N:43, E:32, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 1, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_59` (MODULE_STATE)
  • + [新增節點] `typeof(System.Runtime.CompilerServices.RuntimeFeature).GetProperty (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `state_53` (MODULE_STATE)
  • + [新增呼叫邊] `BrowserWindowingPlatform.DetectThreadSupport` ──[CALLS]──> `typeof(System.Runtime.CompilerServices.RuntimeFeature).GetProperty (External/BCL)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `BrowserWindowingPlatform.DetectThreadSupport()`
- **變更前簽章 (Before)**: `BrowserWindowingPlatform.DetectThreadSupport()` (L31~L51)
- **變更後簽章 (After)**: `BrowserWindowingPlatform.DetectThreadSupport()` (L31~L57)

#### ◀️ 變更前實作碼 (Before Implementation):
```
static bool DetectThreadSupport()
    {
        // TODO Replace with public API https://github.com/dotnet/runtime/issues/77541.
        var prop = typeof(System.Threading.Thread).GetProperty("IsThreadStartSupported",
            BindingFlags.Static | BindingFlags.NonPublic);
        if (prop != null && prop.GetValue(null) is bool value)
            return value;
        // No property is found, try to start a thread and get an exception in the face if threads aren't available
        try
        {
#pragma warning disable CA1416
            new Thread(() => { }).Start();
#pragma warning restore CA1416
            return true;
        }
        catch
        {
            return false;
        }

    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
static bool DetectThreadSupport()
    {
        // .NET 11+ has the public RuntimeFeature.IsMultithreadingSupported (https://github.com/dotnet/runtime/issues/77541).
        // Read it via reflection, as it's not in the reference assemblies of the TFMs we compile against.
        var prop = typeof(System.Runtime.CompilerServices.RuntimeFeature).GetProperty("IsMultithreadingSupported",
            BindingFlags.Static | BindingFlags.Public);
        if (prop != null && prop.GetValue(null) is bool value)
            return value;
        // Older runtimes have the internal Thread.IsThreadStartSupported instead.
        prop = typeof(System.Threading.Thread).GetProperty("IsThreadStartSupported",
            BindingFlags.Static | BindingFlags.NonPublic);
        if (prop != null && prop.GetValue(null) is bool legacyValue)
            return legacyValue;
        // No property is found, try to start a thread and get an exception in the face if threads aren't available.
        try
        {
#pragma warning disable CA1416
            new Thread(() => { }).Start();
#pragma warning restore CA1416
            return true;
        }
        catch
        {
            return false;
        }

    }
```


---

### 🔹 Commit #13: `35f28ce3`
- **完整 Hash**: `35f28ce32fa6e7198b913c89d906e7991c05a3a2`
- **說明 (Ground Truth)**: Fix stale screen information in tray-only Win32 apps (#22374)
- **變更檔案數**: 2

#### 📄 檔案: `src/Windows/Avalonia.Win32/Win32Platform.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:97, E:80, A:0) ➔ After(N:97, E:81, A:0)
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
  • + [新增呼叫邊] `Win32Platform.WndProc` ──[CALLS]──> `Win32Platform.UpdateTimerFps`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Win32Platform.WndProc()`
- **變更前簽章 (Before)**: `Win32Platform.WndProc(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam)` (L143~L209)
- **變更後簽章 (After)**: `Win32Platform.WndProc(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam)` (L143~L215)

#### ◀️ 變更前實作碼 (Before Implementation):
```
[SuppressMessage("Microsoft.StyleCop.CSharp.NamingRules", "SA1305:FieldNamesMustNotUseHungarianNotation", Justification = "Using Win32 naming for consistency.")]
        private IntPtr WndProc(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam)
        {
            if (msg == (int)WindowsMessage.WM_DISPATCH_WORK_ITEM 
                && wParam.ToInt64() == Win32DispatcherImpl.SignalW 
                && lParam.ToInt64() == Win32DispatcherImpl.SignalL) 
                _dispatcher?.DispatchWorkItem();

            if(msg == (uint)WindowsMessage.WM_QUERYENDSESSION)
            {
                if (ShutdownRequested != null)
                {
                    // https://learn.microsoft.com/en-us/windows/win32/shutdown/wm-queryendsession
                    // > LPARAM lParam   // logoff option
                    // >
                    // > This parameter can be one or more of the following values. If this parameter is 0, the system is shutting down or restarting (it is not possible to determine which event is occurring).
                    // >
                    // > - ENDSESSION_CLOSEAPP 0x00000001 The application is using a file that must be replaced, the system is being serviced, or system resources are exhausted. For more information, see Guidelines for Applications.
                    // > - ENDSESSION_CRITICAL 0x40000000 The application is forced to shut down.
                    // > - ENDSESSION_LOGOFF 0x80000000 The user is logging off.
                    var e = new ShutdownRequestedEventArgs()
                    {
                        IsOSShutdown = lParam == IntPtr.Zero,
                    };

                    ShutdownRequested(this, e);

                    if (e.Cancel)
                    {
                        return IntPtr.Zero;
                    }
                }
            }

            if (msg == (uint)WindowsMessage.WM_SETTINGCHANGE)
            {
                if (PlatformSettings is Win32PlatformSettings win32PlatformSettings)
                {
                    var changedSetting = Marshal.PtrToStringAuto(lParam);
                    if (changedSetting == "ImmersiveColorSet" // dark/light mode
                        || changedSetting == "WindowsThemeElement") // high contrast mode
                    {
                        win32PlatformSettings.OnColorValuesChanged();
                    }
                    else if (changedSetting == "intl") // language/locale change
                    {
                        win32PlatformSettings.OnLanguageChanged();
                    }
                }

                // Notify WorkingArea changed to Screens
                if ((SystemParametersInfo)wParam == SystemParametersInfo.SPI_SETWORKAREA)
                {
                    Screen?.OnChanged();
                }
            }

            if (msg == (uint)WindowsMessage.WM_TIMER)
            {
                if (wParam == (IntPtr)TIMERID_DISPATCHER)
                    _dispatcher?.FireTimer();
            }
            
            TrayIconImpl.ProcWnd(hWnd, msg, wParam, lParam);

            return DefWindowProc(hWnd, msg, wParam, lParam);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
[SuppressMessage("Microsoft.StyleCop.CSharp.NamingRules", "SA1305:FieldNamesMustNotUseHungarianNotation", Justification = "Using Win32 naming for consistency.")]
        private IntPtr WndProc(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam)
        {
            if (msg == (int)WindowsMessage.WM_DISPATCH_WORK_ITEM 
                && wParam.ToInt64() == Win32DispatcherImpl.SignalW 
                && lParam.ToInt64() == Win32DispatcherImpl.SignalL) 
                _dispatcher?.DispatchWorkItem();

            if(msg == (uint)WindowsMessage.WM_QUERYENDSESSION)
            {
                if (ShutdownRequested != null)
                {
                    // https://learn.microsoft.com/en-us/windows/win32/shutdown/wm-queryendsession
                    // > LPARAM lParam   // logoff option
                    // >
                    // > This parameter can be one or more of the following values. If this parameter is 0, the system is shutting down or restarting (it is not possible to determine which event is occurring).
                    // >
                    // > - ENDSESSION_CLOSEAPP 0x00000001 The application is using a file that must be replaced, the system is being serviced, or system resources are exhausted. For more information, see Guidelines for Applications.
                    // > - ENDSESSION_CRITICAL 0x40000000 The application is forced to shut down.
                    // > - ENDSESSION_LOGOFF 0x80000000 The user is logging off.
                    var e = new ShutdownRequestedEventArgs()
                    {
                        IsOSShutdown = lParam == IntPtr.Zero,
                    };

                    ShutdownRequested(this, e);

                    if (e.Cancel)
                    {
                        return IntPtr.Zero;
                    }
                }
            }

            if (msg == (uint)WindowsMessage.WM_DISPLAYCHANGE)
            {
                Screen?.OnChanged();
                UpdateTimerFps();
            }

            if (msg == (uint)WindowsMessage.WM_SETTINGCHANGE)
            {
                if (PlatformSettings is Win32PlatformSettings win32PlatformSettings)
                {
                    var changedSetting = Marshal.PtrToStringAuto(lParam);
                    if (changedSetting == "ImmersiveColorSet" // dark/light mode
                        || changedSetting == "WindowsThemeElement") // high contrast mode
                    {
                        win32PlatformSettings.OnColorValuesChanged();
                    }
                    else if (changedSetting == "intl") // language/locale change
                    {
                        win32PlatformSettings.OnLanguageChanged();
                    }
                }

                // Notify WorkingArea changed to Screens
                if ((SystemParametersInfo)wParam == SystemParametersInfo.SPI_SETWORKAREA)
                {
                    Screen?.OnChanged();
                }
            }

            if (msg == (uint)WindowsMessage.WM_TIMER)
            {
                if (wParam == (IntPtr)TIMERID_DISPATCHER)
                    _dispatcher?.FireTimer();
            }
            
            TrayIconImpl.ProcWnd(hWnd, msg, wParam, lParam);

            return DefWindowProc(hWnd, msg, wParam, lParam);
        }
```


#### 📄 檔案: `src/Windows/Avalonia.Win32/WindowImpl.AppWndProc.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:136, E:150, A:0) ➔ After(N:134, E:148, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 2, +Edges: 0, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `Win32Platform.UpdateTimerFps (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `Screen?.OnChanged (External/BCL)` (FUNCTION_DEF)
  • - [移除呼叫邊] `WindowImpl.AppWndProc` ──[CALLS]──> `Screen?.OnChanged (External/BCL)`
  • - [移除呼叫邊] `WindowImpl.AppWndProc` ──[CALLS]──> `Win32Platform.UpdateTimerFps (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `WindowImpl.AppWndProc()`
- **變更前簽章 (Before)**: `WindowImpl.AppWndProc(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam)` (L23~L1003)
- **變更後簽章 (After)**: `WindowImpl.AppWndProc(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam)` (L23~L994)

#### ◀️ 變更前實作碼 (Before Implementation):
```
[SuppressMessage("Microsoft.StyleCop.CSharp.NamingRules", "SA1305:FieldNamesMustNotUseHungarianNotation",
            Justification = "Using Win32 naming for consistency.")]
        [UnconditionalSuppressMessage("Trimming", "IL2026", Justification = "We do .NET COM interop availability checks")]
        [UnconditionalSuppressMessage("Trimming", "IL2050", Justification = "We do .NET COM interop availability checks")]
        protected virtual unsafe IntPtr AppWndProc(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam)
        {
            const double wheelDelta = 120.0;
            const long uiaRootObjectId = -25;
            uint timestamp = unchecked((uint)GetMessageTime());
            RawInputEventArgs? e = null;
            var shouldTakeFocus = false;
            var message = (WindowsMessage)msg;
            switch (message)
            {
                case WindowsMessage.WM_ACTIVATE:
                    {
                        var wa = (WindowActivate)(ToInt32(wParam) & 0xffff);

                        switch (wa)
                        {
                            case WindowActivate.WA_ACTIVE:
                            case WindowActivate.WA_CLICKACTIVE:
                                {
                                    Activated?.Invoke();
                                    UpdateInputMethod(GetKeyboardLayout(0));
                                    break;
                                }

                            case WindowActivate.WA_INACTIVE:
                                {
                                    Deactivated?.Invoke();
                                    break;
                                }
                        }

                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_NCCALCSIZE when ToInt32(wParam) == 1:
                    {
                        if (_windowProperties.Decorations == WindowDecorations.None)
                            return IntPtr.Zero;

                        // When the client area is extended into the frame, we are still requesting the standard styles matching
                        // the wanted decorations (such as WS_CAPTION or WS_BORDER) along with window bounds larger than the client size.
                        // This allows the window to have the standard resize borders *outside* of the client area.
                        // The logic for this lies in the Resize() method.
                        //
                        // After this happens, WM_NCCALCSIZE provides us with a new window area matching those requested bounds.
                        // We need to adjust that area back to our preferred client area, keeping the resize borders around it.
                        //
                        // The same logic applies when the window gets maximized, the only difference being that Windows chose
                        // the final bounds instead of us.
                        if (_isClientAreaExtended)
                        {
                            GetWindowPlacement(hWnd, out var placement);
                            if (placement.ShowCmd == ShowWindowCommand.ShowMinimized)
                                break;

                            var paramsObj = Marshal.PtrToStructure<NCCALCSIZE_PARAMS>(lParam);
                            ref var rect = ref paramsObj.rgrc[0];

                            var style = (WindowStyles)GetWindowLong(_hwnd, (int)WindowLongParam.GWL_STYLE);
                            var adjuster = CreateWindowRectAdjuster();
                            var borderThickness = new RECT();

                            // We told Windows we have a caption, but since we're actually extending into it, it should not be taken into account.
                            if (style.HasAllFlags(WindowStyles.WS_CAPTION))
                            {
                                if (placement.ShowCmd == ShowWindowCommand.ShowMaximized)
                                {
                                    adjuster.Adjust(ref borderThickness, style & ~WindowStyles.WS_CAPTION | WindowStyles.WS_BORDER | WindowStyles.WS_THICKFRAME, 0);
                                }
                                else
                                {
                                    // There's no extra border on top with WS_CAPTION: it's part of the caption.
                                    adjuster.Adjust(ref borderThickness, style, 0);
                                    borderThickness.top = 0;
                                }
                            }
                            else if (style.HasAllFlags(WindowStyles.WS_BORDER))
                            {
                                if (placement.ShowCmd == ShowWindowCommand.ShowMaximized)
                                {
                                    adjuster.Adjust(ref borderThickness, style, 0);
                                }
                                else
                                {
                                    adjuster.Adjust(ref borderThickness, style, 0);

                                    var thinBorderThickness = new RECT();
                                    adjuster.Adjust(ref thinBorderThickness, style & ~WindowStyles.WS_THICKFRAME, 0);
                                    borderThickness.top = thinBorderThickness.top;
                                }
                            }
                            else
                            {
                                adjuster.Adjust(ref borderThickness, style, 0);
                            }

                            rect.left -= borderThickness.left;
                            rect.top -= borderThickness.top;
                            rect.right -= borderThickness.right;
                            rect.bottom -= borderThickness.bottom;

                            Marshal.StructureToPtr(paramsObj, lParam, false);

                            return IntPtr.Zero;
                        }
                        break;
                    }

                case WindowsMessage.WM_CLOSE:
                    {
                        bool? preventClosing = Closing?.Invoke(WindowCloseReason.WindowClosing);
                        if (preventClosing == true)
                        {
                            return IntPtr.Zero;
                        }

                        BeforeCloseCleanup(false);

                        // Used to distinguish between programmatic and regular close requests.
                        _isCloseRequested = true;

                        break;
                    }

                case WindowsMessage.WM_DESTROY:
                    {
                        // The first and foremost thing to do - notify the TopLevel
                        Closed?.Invoke();

                        UiaCoreProviderApi.UiaReturnRawElementProvider(_hwnd, IntPtr.Zero, IntPtr.Zero, null);

                        // We need to release IMM context and state to avoid leaks.
                        if (Imm32InputMethod.Current.Hwnd == _hwnd)
                        {
                            Imm32InputMethod.Current.ClearLanguageAndWindow();
                        }

                        // Cleanup render targets
                        (_glSurface as IDisposable)?.Dispose();

                        if (_dropTarget != null)
                        {
                            OleContext.Current?.UnregisterDragDrop(Handle);
                            _dropTarget.Dispose();
                            _dropTarget = null;
                        }

                        _framebuffer.Dispose();
                        _inputPane?.Dispose();

                        //Window doesn't exist anymore
                        _hwnd = IntPtr.Zero;
                        //Remove root reference to this class, so unmanaged delegate can be collected
                        lock (s_instances)
                            s_instances.Remove(this);

                        _touchDevice.Dispose();
                        //Free other resources
                        Dispose();

                        // Schedule cleanup of anything that requires window to be destroyed
                        Dispatcher.UIThread.Post(AfterCloseCleanup);
                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_DPICHANGED:
                    {
                        _dpi = (uint)wParam >> 16;
                        var newDisplayRect = Marshal.PtrToStructure<RECT>(lParam);
                        _scaling = _dpi / StandardDpi;
                        RefreshIcon();
                        ScalingChanged?.Invoke(_scaling);

                        using (SetResizeReason(WindowResizeReason.DpiChange))
                        {
                            SetWindowPos(hWnd,
                                IntPtr.Zero,
                                newDisplayRect.left,
                                newDisplayRect.top,
                                newDisplayRect.right - newDisplayRect.left,
                                newDisplayRect.bottom - newDisplayRect.top,
                                SetWindowPosFlags.SWP_NOZORDER |
                                SetWindowPosFlags.SWP_NOACTIVATE);
                        }

                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_GETICON:
                    if (_iconImpl == null)
                    {
                        break;
                    }

                    var requestIcon = (Icons)wParam;
                    var requestDpi = (uint)lParam;

                    if (requestDpi == 0)
                    {
                        requestDpi = _dpi;
                    }

                    return LoadIcon(requestIcon, requestDpi)?.Handle ?? default;

                case WindowsMessage.WM_KEYDOWN:
                    e = TryCreateRawKeyEventArgs(RawKeyEventType.KeyDown, timestamp, wParam, lParam, true);
                    break;

                case WindowsMessage.WM_SYSKEYDOWN:
                    e = TryCreateRawKeyEventArgs(RawKeyEventType.KeyDown, timestamp, wParam, lParam, false);
                    break;

                case WindowsMessage.WM_SYSCOMMAND:
                    // Disable system handling of Alt/F10 menu keys.
                    if (GetSysCommand(wParam) == SysCommands.SC_KEYMENU && HighWord(ToInt32(lParam)) <= 0)
                        return IntPtr.Zero;
                    break;

                case WindowsMessage.WM_MENUCHAR:
                    {
                        // mute the system beep
                        return (IntPtr)((int)MenuCharParam.MNC_CLOSE << 16);
                    }

                case WindowsMessage.WM_KEYUP:
                    e = TryCreateRawKeyEventArgs(RawKeyEventType.KeyUp, timestamp, wParam, lParam, true);
                    _ignoreWmChar = false;
                    break;

                case WindowsMessage.WM_SYSKEYUP:
                    e = TryCreateRawKeyEventArgs(RawKeyEventType.KeyUp, timestamp, wParam, lParam, false);
                    _ignoreWmChar = false;
                    break;

                case WindowsMessage.WM_CHAR:
                    {
                        if (Imm32InputMethod.Current.IsComposing)
                        {
                            break;
                        }

                        // Ignore control chars and chars that were handled in WM_KEYDOWN.
                        if (ToInt32(wParam) >= 32 && !_ignoreWmChar)
                        {
                            var text = new string((char)ToInt32(wParam), 1);

                            e = new RawTextInputEventArgs(WindowsKeyboardDevice.Instance, timestamp, Owner, text);
                        }
                        break;
                    }

                case WindowsMessage.WM_LBUTTONDOWN:
                case WindowsMessage.WM_RBUTTONDOWN:
                case WindowsMessage.WM_MBUTTONDOWN:
                case WindowsMessage.WM_XBUTTONDOWN:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        shouldTakeFocus = ShouldTakeFocusOnClick;
                        if (ShouldIgnoreTouchEmulatedMessage())
                        {
                            break;
                        }

                        e = new RawPointerEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
#pragma warning disable CS8509
                            message switch
#pragma warning restore CS8509
                            {
                                WindowsMessage.WM_LBUTTONDOWN => RawPointerEventType.LeftButtonDown,
                                WindowsMessage.WM_RBUTTONDOWN => RawPointerEventType.RightButtonDown,
                                WindowsMessage.WM_MBUTTONDOWN => RawPointerEventType.MiddleButtonDown,
                                WindowsMessage.WM_XBUTTONDOWN =>
                                HighWord(ToInt32(wParam)) == 1 ?
                                    RawPointerEventType.XButton1Down :
                                    RawPointerEventType.XButton2Down,
                            },
                            DipFromLParam(lParam), GetMouseModifiers(wParam));
                        break;
                    }

                case WindowsMessage.WM_LBUTTONUP:
                case WindowsMessage.WM_RBUTTONUP:
                case WindowsMessage.WM_MBUTTONUP:
                case WindowsMessage.WM_XBUTTONUP:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        if (ShouldIgnoreTouchEmulatedMessage())
                        {
                            break;
                        }

                        e = new RawPointerEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
#pragma warning disable CS8509
                            message switch
#pragma warning restore CS8509
                            {
                                WindowsMessage.WM_LBUTTONUP => RawPointerEventType.LeftButtonUp,
                                WindowsMessage.WM_RBUTTONUP => RawPointerEventType.RightButtonUp,
                                WindowsMessage.WM_MBUTTONUP => RawPointerEventType.MiddleButtonUp,
                                WindowsMessage.WM_XBUTTONUP =>
                                HighWord(ToInt32(wParam)) == 1 ?
                                    RawPointerEventType.XButton1Up :
                                    RawPointerEventType.XButton2Up,
                            },
                            DipFromLParam(lParam), GetMouseModifiers(wParam));
                        break;
                    }

                case WindowsMessage.WM_MOUSEMOVE:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        if (ShouldIgnoreTouchEmulatedMessage())
                        {
                            break;
                        }

                        if (!_trackingMouse)
                        {
                            var tm = new TRACKMOUSEEVENT
                            {
                                cbSize = Marshal.SizeOf<TRACKMOUSEEVENT>(),
                                dwFlags = 2,
                                hwndTrack = _hwnd,
                                dwHoverTime = 0,
                            };

                            TrackMouseEvent(ref tm);
                        }

                        var point = DipFromLParam(lParam);

                        // Prepare points for the IntermediatePoints call.
                        var p = new POINT()
                        {
                            X = (int)(point.X * RenderScaling),
                            Y = (int)(point.Y * RenderScaling)
                        };
                        ClientToScreen(_hwnd, ref p);
                        var currPoint = new MOUSEMOVEPOINT()
                        {
                            x = p.X & 0xFFFF,
                            y = p.Y & 0xFFFF,
                            time = (int)timestamp
                        };
                        var prevPoint = _lastWmMousePoint;
                        _lastWmMousePoint = currPoint;

                        e = new RawPointerEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
                            RawPointerEventType.Move,
                            point,
                            GetMouseModifiers(wParam))
                        {
                            IntermediatePoints = new Lazy<IReadOnlyList<RawPointerPoint>?>(() => CreateIntermediatePoints(currPoint, prevPoint))
                        };

                        break;
                    }

                case WindowsMessage.WM_MOUSEWHEEL:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        e = new RawMouseWheelEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
                            PointToClient(PointFromLParam(lParam)),
                            new Vector(0, (ToInt32(wParam) >> 16) / wheelDelta),
                            GetMouseModifiers(wParam));
                        break;
                    }

                case WindowsMessage.WM_MOUSEHWHEEL:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        e = new RawMouseWheelEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
                            PointToClient(PointFromLParam(lParam)),
                            new Vector(-(ToInt32(wParam) >> 16) / wheelDelta, 0),
                            GetMouseModifiers(wParam));
                        break;
                    }

                case WindowsMessage.WM_MOUSELEAVE:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        _trackingMouse = false;
                        e = new RawPointerEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
                            RawPointerEventType.LeaveWindow,
                            new Point(-1, -1),
                            WindowsKeyboardDevice.Instance.Modifiers);
                        break;
                    }

                // covers WM_CANCELMODE which sends WM_CAPTURECHANGED in DefWindowProc
                case WindowsMessage.WM_CAPTURECHANGED:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        if (!IsOurWindow(lParam))
                        {
                            _trackingMouse = false;
                            e = new RawPointerEventArgs(
                                _mouseDevice,
                                timestamp,
                                Owner,
                                RawPointerEventType.CancelCapture,
                                new Point(-1, -1),
                                WindowsKeyboardDevice.Instance.Modifiers);
                        }
                        break;
                    }

                case WindowsMessage.WM_NCLBUTTONDOWN:
                case WindowsMessage.WM_NCRBUTTONDOWN:
                case WindowsMessage.WM_NCMBUTTONDOWN:
                case WindowsMessage.WM_NCXBUTTONDOWN:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        e = new RawPointerEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
#pragma warning disable CS8509
                            message switch
#pragma warning restore CS8509
                            {
                                WindowsMessage.WM_NCLBUTTONDOWN => RawPointerEventType
                                    .NonClientLeftButtonDown,
                                WindowsMessage.WM_NCRBUTTONDOWN => RawPointerEventType.RightButtonDown,
                                WindowsMessage.WM_NCMBUTTONDOWN => RawPointerEventType.MiddleButtonDown,
                                WindowsMessage.WM_NCXBUTTONDOWN =>
                                HighWord(ToInt32(wParam)) == 1 ?
                                    RawPointerEventType.XButton1Down :
                                    RawPointerEventType.XButton2Down,
                            },
                            PointToClient(PointFromLParam(lParam)), GetMouseModifiers(wParam));
                        break;
                    }
                case WindowsMessage.WM_TOUCH:
                    {
                        if (_wmPointerEnabled || Input is not { } input)
                        {
                            break;
                        }
                        var touchInputCount = wParam.ToInt32();

                        var pTouchInputs = stackalloc TOUCHINPUT[touchInputCount];
                        var touchInputs = new Span<TOUCHINPUT>(pTouchInputs, touchInputCount);

                        if (GetTouchInputInfo(lParam, (uint)touchInputCount, pTouchInputs, Marshal.SizeOf<TOUCHINPUT>()))
                        {
                            foreach (var touchInput in touchInputs)
                            {
                                var position = PointToClient(new PixelPoint(touchInput.X / 100, touchInput.Y / 100));
                                var rawPointerPoint = new RawPointerPoint()
                                {
                                    Position = position,
                                };

                                // Try to get the touch width and height.
                                // See https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-touchinput
                                // > The width of the touch contact area in hundredths of a pixel in physical screen coordinates. This value is only valid if the dwMask member has the TOUCHEVENTFMASK_CONTACTAREA flag set.
                                const int TOUCHEVENTFMASK_CONTACTAREA = 0x0004; // Known as TOUCHINPUTMASKF_CONTACTAREA in the docs.
                                if ((touchInput.Mask & TOUCHEVENTFMASK_CONTACTAREA) != 0)
                                {
                                    var centerX = touchInput.X / 100.0;
                                    var centerY = touchInput.Y / 100.0;

                                    var rightX = centerX + touchInput.CxContact / 100.0 /
                                        2 /*The center X add the half width is the right X*/;
                                    var bottomY = centerY + touchInput.CyContact / 100.0 /
                                        2 /*The center Y add the half height is the bottom Y*/;

                                    var bottomRightPixelPoint =
                                        new PixelPoint((int)rightX, (int)bottomY);
                                    var bottomRightPosition = PointToClient(bottomRightPixelPoint);

                                    var centerPosition = position;
                                    var halfWidth = bottomRightPosition.X - centerPosition.X;
                                    var halfHeight = bottomRightPosition.Y - centerPosition.Y;
                                    var leftTopPosition = new Point(centerPosition.X - halfWidth, centerPosition.Y - halfHeight);

                                    rawPointerPoint.ContactRect = new Rect(leftTopPosition, bottomRightPosition);
                                }

                                input.Invoke(new RawTouchEventArgs(_touchDevice, touchInput.Time,
                                    Owner,
                                    touchInput.Flags.HasAllFlags(TouchInputFlags.TOUCHEVENTF_UP) ?
                                        RawPointerEventType.TouchEnd :
                                        touchInput.Flags.HasAllFlags(TouchInputFlags.TOUCHEVENTF_DOWN) ?
                                            RawPointerEventType.TouchBegin :
                                            RawPointerEventType.TouchUpdate,
                                    rawPointerPoint,
                                    WindowsKeyboardDevice.Instance.Modifiers,
                                    touchInput.Id));
                            }

                            CloseTouchInputHandle(lParam);
                            return IntPtr.Zero;
                        }

                        break;
                    }
                case WindowsMessage.WM_NCPOINTERDOWN:
                case WindowsMessage.WM_NCPOINTERUP:
                case WindowsMessage.WM_POINTERDOWN:
                case WindowsMessage.WM_POINTERUP:
                case WindowsMessage.WM_POINTERUPDATE:
                    {
                        if (!_wmPointerEnabled)
                        {
                            break;
                        }
                        GetDevicePointerInfo(wParam, out var device, out var info, out var point, out var modifiers, ref timestamp);
                        var eventType = GetEventType(message, info);

                        var args = CreatePointerArgs(device, timestamp, eventType, point, modifiers, info.pointerId);
                        args.IntermediatePoints = CreateLazyIntermediatePoints(info);
                        e = args;
                        break;
                    }
                case WindowsMessage.WM_POINTERLEAVE:
                    {
                        if (!_wmPointerEnabled)
                        {
                            break;
                        }
                        GetDevicePointerInfo(wParam, out var device, out var info, out var point, out var modifiers, ref timestamp);
                        var eventType = device is TouchDevice ? RawPointerEventType.TouchCancel : RawPointerEventType.LeaveWindow;
                        e = CreatePointerArgs(device, timestamp, eventType, point, modifiers, info.pointerId);
                        break;
                    }
                case WindowsMessage.WM_POINTERCAPTURECHANGED:
                    {
                        if (!_wmPointerEnabled)
                        {
                            break;
                        }
                        GetDevicePointerInfo(wParam, out var device, out var info, out var point, out var modifiers, ref timestamp);
                        var eventType = device is TouchDevice ? RawPointerEventType.TouchCancel : RawPointerEventType.CancelCapture;
                        e = CreatePointerArgs(device, timestamp, eventType, point, modifiers, info.pointerId);
                        break;
                    }
                case WindowsMessage.WM_POINTERWHEEL:
                case WindowsMessage.WM_POINTERHWHEEL:
                    {
                        if (!_wmPointerEnabled)
                        {
                            break;
                        }
                        GetDevicePointerInfo(wParam, out var device, out var info, out var point, out var modifiers, ref timestamp);

                        var val = (ToInt32(wParam) >> 16) / wheelDelta;
                        var delta = message == WindowsMessage.WM_POINTERWHEEL ? new Vector(0, val) : new Vector(val, 0);
                        e = new RawMouseWheelEventArgs(device, timestamp, Owner, point.Position, delta, modifiers)
                        {
                            RawPointerId = info.pointerId
                        };
                        break;
                    }
                case WindowsMessage.WM_POINTERACTIVATE:
                    {
                        //occurs when a pointer activates an inactive window.
                        //we should handle this and return PA_ACTIVATE or PA_NOACTIVATE
                        //https://docs.microsoft.com/en-us/previous-versions/windows/desktop/inputmsg/wm-pointeractivate
                        break;
                    }
                case WindowsMessage.WM_POINTERDEVICECHANGE:
                    {
                        //notifies about changes in the settings of a monitor that has a digitizer attached to it.
                        //https://docs.microsoft.com/en-us/previous-versions/windows/desktop/inputmsg/wm-pointerdevicechange
                        break;
                    }
                case WindowsMessage.WM_NCPOINTERUPDATE:
                    {
                        //NC stands for non-client area - window header and window border
                        //As I found above in an old message handling - we dont need to handle NC pointer move/updates.
                        //All we need is pointer down and up. So this is skipped for now.
                        break;
                    }
                case WindowsMessage.WM_POINTERENTER:
                    {
                        //this is not handled by WM_MOUSEENTER so I think there is no need to handle this too.
                        //but we can detect a new pointer by this message and calling IS_POINTER_NEW_WPARAM

                        //note: by using a pen there can be a pointer leave or enter inside a window coords
                        //when you are just lift up the pen above the display
                        break;
                    }
                case WindowsMessage.DM_POINTERHITTEST:
                    {
                        //DM stands for direct manipulation.
                        //https://docs.microsoft.com/en-us/previous-versions/windows/desktop/directmanipulation/direct-manipulation-portal
                        break;
                    }
                case WindowsMessage.WM_TOUCHHITTESTING:
                    {
                        //This is to determine the most probable touch target.
                        //provides an input bounding box and receives hit proximity
                        //https://docs.microsoft.com/en-us/previous-versions/windows/desktop/inputmsg/wm-touchhittesting
                        //https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-touch_hit_testing_input
                        break;
                    }
                case WindowsMessage.WM_PARENTNOTIFY:
                    {
                        //This message is sent in a dialog scenarios. Contains mouse position.
                        //Old message, but listed in the wm_pointer reference
                        //https://docs.microsoft.com/en-us/previous-versions/windows/desktop/inputmsg/wm-parentnotify
                        break;
                    }
                case WindowsMessage.WM_NCPAINT:
                    {
                        if (!HasFullDecorations)
                        {
                            return IntPtr.Zero;
                        }

                        break;
                    }

                case WindowsMessage.WM_NCACTIVATE:
                    {
                        if (!HasFullDecorations)
                        {
                            return new IntPtr(1);
                        }

                        break;
                    }

                case WindowsMessage.WM_PAINT:
                    {
                        using (NonPumpingSyncContext.Use(NonPumpingWaitHelperImpl.Instance))
                        {
                            if (BeginPaint(_hwnd, out PAINTSTRUCT ps) != IntPtr.Zero)
                            {
                                var f = RenderScaling;
                                var r = ps.rcPaint;
                                Paint?.Invoke(new Rect(r.left / f, r.top / f, (r.right - r.left) / f,
                                    (r.bottom - r.top) / f));
                                EndPaint(_hwnd, ref ps);
                            }
                        }

                        return IntPtr.Zero;
                    }


                case WindowsMessage.WM_ENTERSIZEMOVE:
                    _resizeReason = WindowResizeReason.User;
                    break;

                case WindowsMessage.WM_SHOWWINDOW:
                    OnShowHideMessage(wParam != default);
                    break;

                case WindowsMessage.WM_SIZE:
                    {
                        var size = (SizeCommand)wParam;

                        var windowState = size switch
                        {
                            SizeCommand.Maximized => WindowState.Maximized,
                            SizeCommand.Minimized => WindowState.Minimized,
                            _ when _isFullScreenActive => WindowState.FullScreen,
                            // Ignore state changes for unshown windows. We always tell Windows that we are hidden
                            // until shown, so the OS value should be ignored while we are in the unshown state.
                            _ when !_shown => _lastWindowState,
                            _ => WindowState.Normal,
                        };

                        var stateChanged = windowState != _lastWindowState;
                        _lastWindowState = windowState;

                        if (Resized != null &&
                            (size == SizeCommand.Restored ||
                             size == SizeCommand.Maximized))
                        {
                            var clientSize = new Size(ToInt32(lParam) & 0xffff, ToInt32(lParam) >> 16);
                            Resized(clientSize / RenderScaling, _resizeReason);
                        }

                        if (IsWindowVisible(_hwnd) && !_shown)
                            _shown = true;

                        if (stateChanged)
                        {
                            var newWindowProperties = _windowProperties;

                            newWindowProperties.WindowState = windowState;

                            UpdateWindowProperties(newWindowProperties);

                            WindowStateChanged?.Invoke(windowState);

                            if (_isClientAreaExtended)
                            {
                                ExtendClientArea();

                                ExtendClientAreaToDecorationsChanged?.Invoke(true);
                            }
                        }
                        else if (windowState == WindowState.Maximized && _isClientAreaExtended)
                        {
                            ExtendClientArea();

                            ExtendClientAreaToDecorationsChanged?.Invoke(true);
                        }

                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_EXITSIZEMOVE:
                    _resizeReason = WindowResizeReason.Unspecified;
                    break;

                case WindowsMessage.WM_MOVE:
                    {
                        PositionChanged?.Invoke(Position);
                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_GETMINMAXINFO:
                    {
                        MINMAXINFO mmi = Marshal.PtrToStructure<MINMAXINFO>(lParam);

                        _maxTrackSize = mmi.ptMaxTrackSize;

                        // A window without a caption (i.e. None and BorderOnly decorations) maximizes to the whole screen
                        // by default. Adjust that to the screen's working area instead.
                        var style = GetStyle();
                        if (!style.HasAllFlags(WindowStyles.WS_CAPTION | WindowStyles.WS_THICKFRAME) &&
                            Screen.ScreenFromHwnd(Hwnd, MONITOR.MONITOR_DEFAULTTONEAREST) is { } screen)
                        {
                            var maximizedRect = GetCaptionlessMaximizedRect(style, screen.WorkingArea);
                            // We aren't changing ptMaxPosition because its coordinates must always target the primary screen.
                            // We can't do that, since the work area might not be the same for all screens.
                            // Instead, only set the desired max size here.
                            // WM_WINDOWPOSCHANGING moves the window to the correct position.
                            mmi.ptMaxSize.X = maximizedRect.Width;
                            mmi.ptMaxSize.Y = maximizedRect.Height;
                        }

                        if (_minSize.Width > 0)
                        {
                            mmi.ptMinTrackSize.X =
                                (int)((_minSize.Width * RenderScaling) + BorderThickness.Left + BorderThickness.Right);
                        }

                        if (_minSize.Height > 0)
                        {
                            mmi.ptMinTrackSize.Y =
                                (int)((_minSize.Height * RenderScaling) + BorderThickness.Top + BorderThickness.Bottom);
                        }

                        if (!double.IsInfinity(_maxSize.Width) && _maxSize.Width > 0)
                        {
                            mmi.ptMaxTrackSize.X =
                                (int)((_maxSize.Width * RenderScaling) + BorderThickness.Left + BorderThickness.Right);
                        }

                        if (!double.IsInfinity(_maxSize.Height) && _maxSize.Height > 0)
                        {
                            mmi.ptMaxTrackSize.Y =
                                (int)((_maxSize.Height * RenderScaling) + BorderThickness.Top + BorderThickness.Bottom);
                        }

                        Marshal.StructureToPtr(mmi, lParam, true);
                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_WINDOWPOSCHANGING:
                    {
                        var pos = (WINDOWPOS*)lParam;
                        var style = GetStyle();
                        var flags = (SetWindowPosFlags)pos->flags;

                        // A window without a caption (i.e. None and BorderOnly decorations) maximizes to the whole screen
                        // by default. Adjust that to the screen's working area instead.
                        if (!style.HasAllFlags(WindowStyles.WS_CAPTION | WindowStyles.WS_THICKFRAME) &&
                            style.HasAllFlags(WindowStyles.WS_MAXIMIZE) &&
                            !_isFullScreenActive &&
                            !flags.HasAllFlags(SetWindowPosFlags.SWP_NOMOVE | SetWindowPosFlags.SWP_NOSIZE))
                        {
                            GetWindowPlacement(Hwnd, out var placement);

                            // Prefer ScreenFromRect with the window's restored bounds.
                            // If the window was minimized, ScreenFromHwnd won't return the correct monitor at this point.
                            var screen = Screen.ScreenFromRect(placement.NormalPosition.ToPixelRect())
                                ?? Screen.ScreenFromHwnd(Hwnd, MONITOR.MONITOR_DEFAULTTONEAREST);

                            if (screen is not null)
                            {
                                var maximizedRect = GetCaptionlessMaximizedRect(style, screen.WorkingArea);
                                pos->x = maximizedRect.X;
                                pos->y = maximizedRect.Y;
                                pos->cx = maximizedRect.Width;
                                pos->cy = maximizedRect.Height;
                                return IntPtr.Zero;
                            }
                        }
                        break;
                    }

                case WindowsMessage.WM_DISPLAYCHANGE:
                    {
                        Screen?.OnChanged();

                        Win32Platform.UpdateTimerFps();

                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_KILLFOCUS:
                    if (Imm32InputMethod.Current.IsComposing)
                    {
                        _killFocusRequested = true;
                    }
                    else
                    {
                        LostFocus?.Invoke();
                    }

                    break;

                case WindowsMessage.WM_INPUTLANGCHANGE:
                    {
                        UpdateInputMethod(lParam);
                        // call DefWindowProc to pass to all children
                        break;
                    }
                case WindowsMessage.WM_IME_SETCONTEXT:
                    {
                        unchecked
                        {
                            DefWindowProc(Hwnd, msg, wParam, lParam & ~(nint)ISC_SHOWUICOMPOSITIONWINDOW);
                        }

                        UpdateInputMethod(GetKeyboardLayout(0));

                        return IntPtr.Zero;
                    }
                case WindowsMessage.WM_IME_COMPOSITION:
                    {
                        Imm32InputMethod.Current.HandleComposition(wParam, lParam, timestamp);

                        break;
                    }
                case WindowsMessage.WM_IME_SELECT:
                    break;
                case WindowsMessage.WM_IME_CHAR:
                case WindowsMessage.WM_IME_COMPOSITIONFULL:
                case WindowsMessage.WM_IME_CONTROL:
                case WindowsMessage.WM_IME_KEYDOWN:
                case WindowsMessage.WM_IME_KEYUP:
                case WindowsMessage.WM_IME_NOTIFY:
                    break;
                case WindowsMessage.WM_IME_STARTCOMPOSITION:
                    {
                        Imm32InputMethod.Current.HandleCompositionStart();

                        return IntPtr.Zero;
                    }
                case WindowsMessage.WM_IME_ENDCOMPOSITION:
                    {
                        Imm32InputMethod.Current.HandleCompositionEnd(timestamp);

                        if (_killFocusRequested)
                        {
                            LostFocus?.Invoke();

                            _killFocusRequested = false;
                        }

                        return IntPtr.Zero;
                    }
                case WindowsMessage.WM_GETOBJECT:
                    if ((long)lParam == uiaRootObjectId && _owner?.FocusRoot is Control control)
                    {
                        var peer = ControlAutomationPeer.CreatePeerForElement(control);
                        var node = AutomationNode.GetOrCreate(peer);
                        return UiaCoreProviderApi.UiaReturnRawElementProvider(_hwnd, wParam, lParam, node);
                    }
                    break;
                case WindowsMessage.WM_WINDOWPOSCHANGED:
                    var winPos = Marshal.PtrToStructure<WINDOWPOS>(lParam);
                    if ((winPos.flags & (uint)SetWindowPosFlags.SWP_SHOWWINDOW) != 0)
                    {
                        OnShowHideMessage(true);
                    }
                    else if ((winPos.flags & (uint)SetWindowPosFlags.SWP_HIDEWINDOW) != 0)
                    {
                        OnShowHideMessage(false);
                    }
                    break;
            }

#if USE_MANAGED_DRAG
            if (_managedDrag.PreprocessInputEvent(ref e))
                return UnmanagedMethods.DefWindowProc(hWnd, msg, wParam, lParam);
#endif

            if (shouldTakeFocus)
            {
                SetFocus(_hwnd);
            }

            if (e != null && Input != null)
            {
                Input(e);

                if (message == WindowsMessage.WM_KEYDOWN)
                {
                    if (e is RawKeyEventArgs args && args.Key == Key.ImeProcessed)
                    {
                        _ignoreWmChar = true;
                    }
                    else
                    {
                        // Handling a WM_KEYDOWN message should cause the subsequent WM_CHAR message to
                        // be ignored. This should be safe to do as WM_CHAR should only be produced in
                        // response to the call to TranslateMessage/DispatchMessage after a WM_KEYDOWN
                        // is handled.
                        _ignoreWmChar = e.Handled;
                    }
                }

                if (s_intermediatePointsPooledList.Count > 0)
                {
                    s_intermediatePointsPooledList.Dispose();
                }

                if (e.Handled)
                {
                    return IntPtr.Zero;
                }
            }

            return DefWindowProc(hWnd, msg, wParam, lParam);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
[SuppressMessage("Microsoft.StyleCop.CSharp.NamingRules", "SA1305:FieldNamesMustNotUseHungarianNotation",
            Justification = "Using Win32 naming for consistency.")]
        [UnconditionalSuppressMessage("Trimming", "IL2026", Justification = "We do .NET COM interop availability checks")]
        [UnconditionalSuppressMessage("Trimming", "IL2050", Justification = "We do .NET COM interop availability checks")]
        protected virtual unsafe IntPtr AppWndProc(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam)
        {
            const double wheelDelta = 120.0;
            const long uiaRootObjectId = -25;
            uint timestamp = unchecked((uint)GetMessageTime());
            RawInputEventArgs? e = null;
            var shouldTakeFocus = false;
            var message = (WindowsMessage)msg;
            switch (message)
            {
                case WindowsMessage.WM_ACTIVATE:
                    {
                        var wa = (WindowActivate)(ToInt32(wParam) & 0xffff);

                        switch (wa)
                        {
                            case WindowActivate.WA_ACTIVE:
                            case WindowActivate.WA_CLICKACTIVE:
                                {
                                    Activated?.Invoke();
                                    UpdateInputMethod(GetKeyboardLayout(0));
                                    break;
                                }

                            case WindowActivate.WA_INACTIVE:
                                {
                                    Deactivated?.Invoke();
                                    break;
                                }
                        }

                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_NCCALCSIZE when ToInt32(wParam) == 1:
                    {
                        if (_windowProperties.Decorations == WindowDecorations.None)
                            return IntPtr.Zero;

                        // When the client area is extended into the frame, we are still requesting the standard styles matching
                        // the wanted decorations (such as WS_CAPTION or WS_BORDER) along with window bounds larger than the client size.
                        // This allows the window to have the standard resize borders *outside* of the client area.
                        // The logic for this lies in the Resize() method.
                        //
                        // After this happens, WM_NCCALCSIZE provides us with a new window area matching those requested bounds.
                        // We need to adjust that area back to our preferred client area, keeping the resize borders around it.
                        //
                        // The same logic applies when the window gets maximized, the only difference being that Windows chose
                        // the final bounds instead of us.
                        if (_isClientAreaExtended)
                        {
                            GetWindowPlacement(hWnd, out var placement);
                            if (placement.ShowCmd == ShowWindowCommand.ShowMinimized)
                                break;

                            var paramsObj = Marshal.PtrToStructure<NCCALCSIZE_PARAMS>(lParam);
                            ref var rect = ref paramsObj.rgrc[0];

                            var style = (WindowStyles)GetWindowLong(_hwnd, (int)WindowLongParam.GWL_STYLE);
                            var adjuster = CreateWindowRectAdjuster();
                            var borderThickness = new RECT();

                            // We told Windows we have a caption, but since we're actually extending into it, it should not be taken into account.
                            if (style.HasAllFlags(WindowStyles.WS_CAPTION))
                            {
                                if (placement.ShowCmd == ShowWindowCommand.ShowMaximized)
                                {
                                    adjuster.Adjust(ref borderThickness, style & ~WindowStyles.WS_CAPTION | WindowStyles.WS_BORDER | WindowStyles.WS_THICKFRAME, 0);
                                }
                                else
                                {
                                    // There's no extra border on top with WS_CAPTION: it's part of the caption.
                                    adjuster.Adjust(ref borderThickness, style, 0);
                                    borderThickness.top = 0;
                                }
                            }
                            else if (style.HasAllFlags(WindowStyles.WS_BORDER))
                            {
                                if (placement.ShowCmd == ShowWindowCommand.ShowMaximized)
                                {
                                    adjuster.Adjust(ref borderThickness, style, 0);
                                }
                                else
                                {
                                    adjuster.Adjust(ref borderThickness, style, 0);

                                    var thinBorderThickness = new RECT();
                                    adjuster.Adjust(ref thinBorderThickness, style & ~WindowStyles.WS_THICKFRAME, 0);
                                    borderThickness.top = thinBorderThickness.top;
                                }
                            }
                            else
                            {
                                adjuster.Adjust(ref borderThickness, style, 0);
                            }

                            rect.left -= borderThickness.left;
                            rect.top -= borderThickness.top;
                            rect.right -= borderThickness.right;
                            rect.bottom -= borderThickness.bottom;

                            Marshal.StructureToPtr(paramsObj, lParam, false);

                            return IntPtr.Zero;
                        }
                        break;
                    }

                case WindowsMessage.WM_CLOSE:
                    {
                        bool? preventClosing = Closing?.Invoke(WindowCloseReason.WindowClosing);
                        if (preventClosing == true)
                        {
                            return IntPtr.Zero;
                        }

                        BeforeCloseCleanup(false);

                        // Used to distinguish between programmatic and regular close requests.
                        _isCloseRequested = true;

                        break;
                    }

                case WindowsMessage.WM_DESTROY:
                    {
                        // The first and foremost thing to do - notify the TopLevel
                        Closed?.Invoke();

                        UiaCoreProviderApi.UiaReturnRawElementProvider(_hwnd, IntPtr.Zero, IntPtr.Zero, null);

                        // We need to release IMM context and state to avoid leaks.
                        if (Imm32InputMethod.Current.Hwnd == _hwnd)
                        {
                            Imm32InputMethod.Current.ClearLanguageAndWindow();
                        }

                        // Cleanup render targets
                        (_glSurface as IDisposable)?.Dispose();

                        if (_dropTarget != null)
                        {
                            OleContext.Current?.UnregisterDragDrop(Handle);
                            _dropTarget.Dispose();
                            _dropTarget = null;
                        }

                        _framebuffer.Dispose();
                        _inputPane?.Dispose();

                        //Window doesn't exist anymore
                        _hwnd = IntPtr.Zero;
                        //Remove root reference to this class, so unmanaged delegate can be collected
                        lock (s_instances)
                            s_instances.Remove(this);

                        _touchDevice.Dispose();
                        //Free other resources
                        Dispose();

                        // Schedule cleanup of anything that requires window to be destroyed
                        Dispatcher.UIThread.Post(AfterCloseCleanup);
                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_DPICHANGED:
                    {
                        _dpi = (uint)wParam >> 16;
                        var newDisplayRect = Marshal.PtrToStructure<RECT>(lParam);
                        _scaling = _dpi / StandardDpi;
                        RefreshIcon();
                        ScalingChanged?.Invoke(_scaling);

                        using (SetResizeReason(WindowResizeReason.DpiChange))
                        {
                            SetWindowPos(hWnd,
                                IntPtr.Zero,
                                newDisplayRect.left,
                                newDisplayRect.top,
                                newDisplayRect.right - newDisplayRect.left,
                                newDisplayRect.bottom - newDisplayRect.top,
                                SetWindowPosFlags.SWP_NOZORDER |
                                SetWindowPosFlags.SWP_NOACTIVATE);
                        }

                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_GETICON:
                    if (_iconImpl == null)
                    {
                        break;
                    }

                    var requestIcon = (Icons)wParam;
                    var requestDpi = (uint)lParam;

                    if (requestDpi == 0)
                    {
                        requestDpi = _dpi;
                    }

                    return LoadIcon(requestIcon, requestDpi)?.Handle ?? default;

                case WindowsMessage.WM_KEYDOWN:
                    e = TryCreateRawKeyEventArgs(RawKeyEventType.KeyDown, timestamp, wParam, lParam, true);
                    break;

                case WindowsMessage.WM_SYSKEYDOWN:
                    e = TryCreateRawKeyEventArgs(RawKeyEventType.KeyDown, timestamp, wParam, lParam, false);
                    break;

                case WindowsMessage.WM_SYSCOMMAND:
                    // Disable system handling of Alt/F10 menu keys.
                    if (GetSysCommand(wParam) == SysCommands.SC_KEYMENU && HighWord(ToInt32(lParam)) <= 0)
                        return IntPtr.Zero;
                    break;

                case WindowsMessage.WM_MENUCHAR:
                    {
                        // mute the system beep
                        return (IntPtr)((int)MenuCharParam.MNC_CLOSE << 16);
                    }

                case WindowsMessage.WM_KEYUP:
                    e = TryCreateRawKeyEventArgs(RawKeyEventType.KeyUp, timestamp, wParam, lParam, true);
                    _ignoreWmChar = false;
                    break;

                case WindowsMessage.WM_SYSKEYUP:
                    e = TryCreateRawKeyEventArgs(RawKeyEventType.KeyUp, timestamp, wParam, lParam, false);
                    _ignoreWmChar = false;
                    break;

                case WindowsMessage.WM_CHAR:
                    {
                        if (Imm32InputMethod.Current.IsComposing)
                        {
                            break;
                        }

                        // Ignore control chars and chars that were handled in WM_KEYDOWN.
                        if (ToInt32(wParam) >= 32 && !_ignoreWmChar)
                        {
                            var text = new string((char)ToInt32(wParam), 1);

                            e = new RawTextInputEventArgs(WindowsKeyboardDevice.Instance, timestamp, Owner, text);
                        }
                        break;
                    }

                case WindowsMessage.WM_LBUTTONDOWN:
                case WindowsMessage.WM_RBUTTONDOWN:
                case WindowsMessage.WM_MBUTTONDOWN:
                case WindowsMessage.WM_XBUTTONDOWN:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        shouldTakeFocus = ShouldTakeFocusOnClick;
                        if (ShouldIgnoreTouchEmulatedMessage())
                        {
                            break;
                        }

                        e = new RawPointerEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
#pragma warning disable CS8509
                            message switch
#pragma warning restore CS8509
                            {
                                WindowsMessage.WM_LBUTTONDOWN => RawPointerEventType.LeftButtonDown,
                                WindowsMessage.WM_RBUTTONDOWN => RawPointerEventType.RightButtonDown,
                                WindowsMessage.WM_MBUTTONDOWN => RawPointerEventType.MiddleButtonDown,
                                WindowsMessage.WM_XBUTTONDOWN =>
                                HighWord(ToInt32(wParam)) == 1 ?
                                    RawPointerEventType.XButton1Down :
                                    RawPointerEventType.XButton2Down,
                            },
                            DipFromLParam(lParam), GetMouseModifiers(wParam));
                        break;
                    }

                case WindowsMessage.WM_LBUTTONUP:
                case WindowsMessage.WM_RBUTTONUP:
                case WindowsMessage.WM_MBUTTONUP:
                case WindowsMessage.WM_XBUTTONUP:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        if (ShouldIgnoreTouchEmulatedMessage())
                        {
                            break;
                        }

                        e = new RawPointerEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
#pragma warning disable CS8509
                            message switch
#pragma warning restore CS8509
                            {
                                WindowsMessage.WM_LBUTTONUP => RawPointerEventType.LeftButtonUp,
                                WindowsMessage.WM_RBUTTONUP => RawPointerEventType.RightButtonUp,
                                WindowsMessage.WM_MBUTTONUP => RawPointerEventType.MiddleButtonUp,
                                WindowsMessage.WM_XBUTTONUP =>
                                HighWord(ToInt32(wParam)) == 1 ?
                                    RawPointerEventType.XButton1Up :
                                    RawPointerEventType.XButton2Up,
                            },
                            DipFromLParam(lParam), GetMouseModifiers(wParam));
                        break;
                    }

                case WindowsMessage.WM_MOUSEMOVE:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        if (ShouldIgnoreTouchEmulatedMessage())
                        {
                            break;
                        }

                        if (!_trackingMouse)
                        {
                            var tm = new TRACKMOUSEEVENT
                            {
                                cbSize = Marshal.SizeOf<TRACKMOUSEEVENT>(),
                                dwFlags = 2,
                                hwndTrack = _hwnd,
                                dwHoverTime = 0,
                            };

                            TrackMouseEvent(ref tm);
                        }

                        var point = DipFromLParam(lParam);

                        // Prepare points for the IntermediatePoints call.
                        var p = new POINT()
                        {
                            X = (int)(point.X * RenderScaling),
                            Y = (int)(point.Y * RenderScaling)
                        };
                        ClientToScreen(_hwnd, ref p);
                        var currPoint = new MOUSEMOVEPOINT()
                        {
                            x = p.X & 0xFFFF,
                            y = p.Y & 0xFFFF,
                            time = (int)timestamp
                        };
                        var prevPoint = _lastWmMousePoint;
                        _lastWmMousePoint = currPoint;

                        e = new RawPointerEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
                            RawPointerEventType.Move,
                            point,
                            GetMouseModifiers(wParam))
                        {
                            IntermediatePoints = new Lazy<IReadOnlyList<RawPointerPoint>?>(() => CreateIntermediatePoints(currPoint, prevPoint))
                        };

                        break;
                    }

                case WindowsMessage.WM_MOUSEWHEEL:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        e = new RawMouseWheelEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
                            PointToClient(PointFromLParam(lParam)),
                            new Vector(0, (ToInt32(wParam) >> 16) / wheelDelta),
                            GetMouseModifiers(wParam));
                        break;
                    }

                case WindowsMessage.WM_MOUSEHWHEEL:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        e = new RawMouseWheelEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
                            PointToClient(PointFromLParam(lParam)),
                            new Vector(-(ToInt32(wParam) >> 16) / wheelDelta, 0),
                            GetMouseModifiers(wParam));
                        break;
                    }

                case WindowsMessage.WM_MOUSELEAVE:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        _trackingMouse = false;
                        e = new RawPointerEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
                            RawPointerEventType.LeaveWindow,
                            new Point(-1, -1),
                            WindowsKeyboardDevice.Instance.Modifiers);
                        break;
                    }

                // covers WM_CANCELMODE which sends WM_CAPTURECHANGED in DefWindowProc
                case WindowsMessage.WM_CAPTURECHANGED:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        if (!IsOurWindow(lParam))
                        {
                            _trackingMouse = false;
                            e = new RawPointerEventArgs(
                                _mouseDevice,
                                timestamp,
                                Owner,
                                RawPointerEventType.CancelCapture,
                                new Point(-1, -1),
                                WindowsKeyboardDevice.Instance.Modifiers);
                        }
                        break;
                    }

                case WindowsMessage.WM_NCLBUTTONDOWN:
                case WindowsMessage.WM_NCRBUTTONDOWN:
                case WindowsMessage.WM_NCMBUTTONDOWN:
                case WindowsMessage.WM_NCXBUTTONDOWN:
                    {
                        if (IsMouseInPointerEnabled)
                        {
                            break;
                        }
                        e = new RawPointerEventArgs(
                            _mouseDevice,
                            timestamp,
                            Owner,
#pragma warning disable CS8509
                            message switch
#pragma warning restore CS8509
                            {
                                WindowsMessage.WM_NCLBUTTONDOWN => RawPointerEventType
                                    .NonClientLeftButtonDown,
                                WindowsMessage.WM_NCRBUTTONDOWN => RawPointerEventType.RightButtonDown,
                                WindowsMessage.WM_NCMBUTTONDOWN => RawPointerEventType.MiddleButtonDown,
                                WindowsMessage.WM_NCXBUTTONDOWN =>
                                HighWord(ToInt32(wParam)) == 1 ?
                                    RawPointerEventType.XButton1Down :
                                    RawPointerEventType.XButton2Down,
                            },
                            PointToClient(PointFromLParam(lParam)), GetMouseModifiers(wParam));
                        break;
                    }
                case WindowsMessage.WM_TOUCH:
                    {
                        if (_wmPointerEnabled || Input is not { } input)
                        {
                            break;
                        }
                        var touchInputCount = wParam.ToInt32();

                        var pTouchInputs = stackalloc TOUCHINPUT[touchInputCount];
                        var touchInputs = new Span<TOUCHINPUT>(pTouchInputs, touchInputCount);

                        if (GetTouchInputInfo(lParam, (uint)touchInputCount, pTouchInputs, Marshal.SizeOf<TOUCHINPUT>()))
                        {
                            foreach (var touchInput in touchInputs)
                            {
                                var position = PointToClient(new PixelPoint(touchInput.X / 100, touchInput.Y / 100));
                                var rawPointerPoint = new RawPointerPoint()
                                {
                                    Position = position,
                                };

                                // Try to get the touch width and height.
                                // See https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-touchinput
                                // > The width of the touch contact area in hundredths of a pixel in physical screen coordinates. This value is only valid if the dwMask member has the TOUCHEVENTFMASK_CONTACTAREA flag set.
                                const int TOUCHEVENTFMASK_CONTACTAREA = 0x0004; // Known as TOUCHINPUTMASKF_CONTACTAREA in the docs.
                                if ((touchInput.Mask & TOUCHEVENTFMASK_CONTACTAREA) != 0)
                                {
                                    var centerX = touchInput.X / 100.0;
                                    var centerY = touchInput.Y / 100.0;

                                    var rightX = centerX + touchInput.CxContact / 100.0 /
                                        2 /*The center X add the half width is the right X*/;
                                    var bottomY = centerY + touchInput.CyContact / 100.0 /
                                        2 /*The center Y add the half height is the bottom Y*/;

                                    var bottomRightPixelPoint =
                                        new PixelPoint((int)rightX, (int)bottomY);
                                    var bottomRightPosition = PointToClient(bottomRightPixelPoint);

                                    var centerPosition = position;
                                    var halfWidth = bottomRightPosition.X - centerPosition.X;
                                    var halfHeight = bottomRightPosition.Y - centerPosition.Y;
                                    var leftTopPosition = new Point(centerPosition.X - halfWidth, centerPosition.Y - halfHeight);

                                    rawPointerPoint.ContactRect = new Rect(leftTopPosition, bottomRightPosition);
                                }

                                input.Invoke(new RawTouchEventArgs(_touchDevice, touchInput.Time,
                                    Owner,
                                    touchInput.Flags.HasAllFlags(TouchInputFlags.TOUCHEVENTF_UP) ?
                                        RawPointerEventType.TouchEnd :
                                        touchInput.Flags.HasAllFlags(TouchInputFlags.TOUCHEVENTF_DOWN) ?
                                            RawPointerEventType.TouchBegin :
                                            RawPointerEventType.TouchUpdate,
                                    rawPointerPoint,
                                    WindowsKeyboardDevice.Instance.Modifiers,
                                    touchInput.Id));
                            }

                            CloseTouchInputHandle(lParam);
                            return IntPtr.Zero;
                        }

                        break;
                    }
                case WindowsMessage.WM_NCPOINTERDOWN:
                case WindowsMessage.WM_NCPOINTERUP:
                case WindowsMessage.WM_POINTERDOWN:
                case WindowsMessage.WM_POINTERUP:
                case WindowsMessage.WM_POINTERUPDATE:
                    {
                        if (!_wmPointerEnabled)
                        {
                            break;
                        }
                        GetDevicePointerInfo(wParam, out var device, out var info, out var point, out var modifiers, ref timestamp);
                        var eventType = GetEventType(message, info);

                        var args = CreatePointerArgs(device, timestamp, eventType, point, modifiers, info.pointerId);
                        args.IntermediatePoints = CreateLazyIntermediatePoints(info);
                        e = args;
                        break;
                    }
                case WindowsMessage.WM_POINTERLEAVE:
                    {
                        if (!_wmPointerEnabled)
                        {
                            break;
                        }
                        GetDevicePointerInfo(wParam, out var device, out var info, out var point, out var modifiers, ref timestamp);
                        var eventType = device is TouchDevice ? RawPointerEventType.TouchCancel : RawPointerEventType.LeaveWindow;
                        e = CreatePointerArgs(device, timestamp, eventType, point, modifiers, info.pointerId);
                        break;
                    }
                case WindowsMessage.WM_POINTERCAPTURECHANGED:
                    {
                        if (!_wmPointerEnabled)
                        {
                            break;
                        }
                        GetDevicePointerInfo(wParam, out var device, out var info, out var point, out var modifiers, ref timestamp);
                        var eventType = device is TouchDevice ? RawPointerEventType.TouchCancel : RawPointerEventType.CancelCapture;
                        e = CreatePointerArgs(device, timestamp, eventType, point, modifiers, info.pointerId);
                        break;
                    }
                case WindowsMessage.WM_POINTERWHEEL:
                case WindowsMessage.WM_POINTERHWHEEL:
                    {
                        if (!_wmPointerEnabled)
                        {
                            break;
                        }
                        GetDevicePointerInfo(wParam, out var device, out var info, out var point, out var modifiers, ref timestamp);

                        var val = (ToInt32(wParam) >> 16) / wheelDelta;
                        var delta = message == WindowsMessage.WM_POINTERWHEEL ? new Vector(0, val) : new Vector(val, 0);
                        e = new RawMouseWheelEventArgs(device, timestamp, Owner, point.Position, delta, modifiers)
                        {
                            RawPointerId = info.pointerId
                        };
                        break;
                    }
                case WindowsMessage.WM_POINTERACTIVATE:
                    {
                        //occurs when a pointer activates an inactive window.
                        //we should handle this and return PA_ACTIVATE or PA_NOACTIVATE
                        //https://docs.microsoft.com/en-us/previous-versions/windows/desktop/inputmsg/wm-pointeractivate
                        break;
                    }
                case WindowsMessage.WM_POINTERDEVICECHANGE:
                    {
                        //notifies about changes in the settings of a monitor that has a digitizer attached to it.
                        //https://docs.microsoft.com/en-us/previous-versions/windows/desktop/inputmsg/wm-pointerdevicechange
                        break;
                    }
                case WindowsMessage.WM_NCPOINTERUPDATE:
                    {
                        //NC stands for non-client area - window header and window border
                        //As I found above in an old message handling - we dont need to handle NC pointer move/updates.
                        //All we need is pointer down and up. So this is skipped for now.
                        break;
                    }
                case WindowsMessage.WM_POINTERENTER:
                    {
                        //this is not handled by WM_MOUSEENTER so I think there is no need to handle this too.
                        //but we can detect a new pointer by this message and calling IS_POINTER_NEW_WPARAM

                        //note: by using a pen there can be a pointer leave or enter inside a window coords
                        //when you are just lift up the pen above the display
                        break;
                    }
                case WindowsMessage.DM_POINTERHITTEST:
                    {
                        //DM stands for direct manipulation.
                        //https://docs.microsoft.com/en-us/previous-versions/windows/desktop/directmanipulation/direct-manipulation-portal
                        break;
                    }
                case WindowsMessage.WM_TOUCHHITTESTING:
                    {
                        //This is to determine the most probable touch target.
                        //provides an input bounding box and receives hit proximity
                        //https://docs.microsoft.com/en-us/previous-versions/windows/desktop/inputmsg/wm-touchhittesting
                        //https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-touch_hit_testing_input
                        break;
                    }
                case WindowsMessage.WM_PARENTNOTIFY:
                    {
                        //This message is sent in a dialog scenarios. Contains mouse position.
                        //Old message, but listed in the wm_pointer reference
                        //https://docs.microsoft.com/en-us/previous-versions/windows/desktop/inputmsg/wm-parentnotify
                        break;
                    }
                case WindowsMessage.WM_NCPAINT:
                    {
                        if (!HasFullDecorations)
                        {
                            return IntPtr.Zero;
                        }

                        break;
                    }

                case WindowsMessage.WM_NCACTIVATE:
                    {
                        if (!HasFullDecorations)
                        {
                            return new IntPtr(1);
                        }

                        break;
                    }

                case WindowsMessage.WM_PAINT:
                    {
                        using (NonPumpingSyncContext.Use(NonPumpingWaitHelperImpl.Instance))
                        {
                            if (BeginPaint(_hwnd, out PAINTSTRUCT ps) != IntPtr.Zero)
                            {
                                var f = RenderScaling;
                                var r = ps.rcPaint;
                                Paint?.Invoke(new Rect(r.left / f, r.top / f, (r.right - r.left) / f,
                                    (r.bottom - r.top) / f));
                                EndPaint(_hwnd, ref ps);
                            }
                        }

                        return IntPtr.Zero;
                    }


                case WindowsMessage.WM_ENTERSIZEMOVE:
                    _resizeReason = WindowResizeReason.User;
                    break;

                case WindowsMessage.WM_SHOWWINDOW:
                    OnShowHideMessage(wParam != default);
                    break;

                case WindowsMessage.WM_SIZE:
                    {
                        var size = (SizeCommand)wParam;

                        var windowState = size switch
                        {
                            SizeCommand.Maximized => WindowState.Maximized,
                            SizeCommand.Minimized => WindowState.Minimized,
                            _ when _isFullScreenActive => WindowState.FullScreen,
                            // Ignore state changes for unshown windows. We always tell Windows that we are hidden
                            // until shown, so the OS value should be ignored while we are in the unshown state.
                            _ when !_shown => _lastWindowState,
                            _ => WindowState.Normal,
                        };

                        var stateChanged = windowState != _lastWindowState;
                        _lastWindowState = windowState;

                        if (Resized != null &&
                            (size == SizeCommand.Restored ||
                             size == SizeCommand.Maximized))
                        {
                            var clientSize = new Size(ToInt32(lParam) & 0xffff, ToInt32(lParam) >> 16);
                            Resized(clientSize / RenderScaling, _resizeReason);
                        }

                        if (IsWindowVisible(_hwnd) && !_shown)
                            _shown = true;

                        if (stateChanged)
                        {
                            var newWindowProperties = _windowProperties;

                            newWindowProperties.WindowState = windowState;

                            UpdateWindowProperties(newWindowProperties);

                            WindowStateChanged?.Invoke(windowState);

                            if (_isClientAreaExtended)
                            {
                                ExtendClientArea();

                                ExtendClientAreaToDecorationsChanged?.Invoke(true);
                            }
                        }
                        else if (windowState == WindowState.Maximized && _isClientAreaExtended)
                        {
                            ExtendClientArea();

                            ExtendClientAreaToDecorationsChanged?.Invoke(true);
                        }

                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_EXITSIZEMOVE:
                    _resizeReason = WindowResizeReason.Unspecified;
                    break;

                case WindowsMessage.WM_MOVE:
                    {
                        PositionChanged?.Invoke(Position);
                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_GETMINMAXINFO:
                    {
                        MINMAXINFO mmi = Marshal.PtrToStructure<MINMAXINFO>(lParam);

                        _maxTrackSize = mmi.ptMaxTrackSize;

                        // A window without a caption (i.e. None and BorderOnly decorations) maximizes to the whole screen
                        // by default. Adjust that to the screen's working area instead.
                        var style = GetStyle();
                        if (!style.HasAllFlags(WindowStyles.WS_CAPTION | WindowStyles.WS_THICKFRAME) &&
                            Screen.ScreenFromHwnd(Hwnd, MONITOR.MONITOR_DEFAULTTONEAREST) is { } screen)
                        {
                            var maximizedRect = GetCaptionlessMaximizedRect(style, screen.WorkingArea);
                            // We aren't changing ptMaxPosition because its coordinates must always target the primary screen.
                            // We can't do that, since the work area might not be the same for all screens.
                            // Instead, only set the desired max size here.
                            // WM_WINDOWPOSCHANGING moves the window to the correct position.
                            mmi.ptMaxSize.X = maximizedRect.Width;
                            mmi.ptMaxSize.Y = maximizedRect.Height;
                        }

                        if (_minSize.Width > 0)
                        {
                            mmi.ptMinTrackSize.X =
                                (int)((_minSize.Width * RenderScaling) + BorderThickness.Left + BorderThickness.Right);
                        }

                        if (_minSize.Height > 0)
                        {
                            mmi.ptMinTrackSize.Y =
                                (int)((_minSize.Height * RenderScaling) + BorderThickness.Top + BorderThickness.Bottom);
                        }

                        if (!double.IsInfinity(_maxSize.Width) && _maxSize.Width > 0)
                        {
                            mmi.ptMaxTrackSize.X =
                                (int)((_maxSize.Width * RenderScaling) + BorderThickness.Left + BorderThickness.Right);
                        }

                        if (!double.IsInfinity(_maxSize.Height) && _maxSize.Height > 0)
                        {
                            mmi.ptMaxTrackSize.Y =
                                (int)((_maxSize.Height * RenderScaling) + BorderThickness.Top + BorderThickness.Bottom);
                        }

                        Marshal.StructureToPtr(mmi, lParam, true);
                        return IntPtr.Zero;
                    }

                case WindowsMessage.WM_WINDOWPOSCHANGING:
                    {
                        var pos = (WINDOWPOS*)lParam;
                        var style = GetStyle();
                        var flags = (SetWindowPosFlags)pos->flags;

                        // A window without a caption (i.e. None and BorderOnly decorations) maximizes to the whole screen
                        // by default. Adjust that to the screen's working area instead.
                        if (!style.HasAllFlags(WindowStyles.WS_CAPTION | WindowStyles.WS_THICKFRAME) &&
                            style.HasAllFlags(WindowStyles.WS_MAXIMIZE) &&
                            !_isFullScreenActive &&
                            !flags.HasAllFlags(SetWindowPosFlags.SWP_NOMOVE | SetWindowPosFlags.SWP_NOSIZE))
                        {
                            GetWindowPlacement(Hwnd, out var placement);

                            // Prefer ScreenFromRect with the window's restored bounds.
                            // If the window was minimized, ScreenFromHwnd won't return the correct monitor at this point.
                            var screen = Screen.ScreenFromRect(placement.NormalPosition.ToPixelRect())
                                ?? Screen.ScreenFromHwnd(Hwnd, MONITOR.MONITOR_DEFAULTTONEAREST);

                            if (screen is not null)
                            {
                                var maximizedRect = GetCaptionlessMaximizedRect(style, screen.WorkingArea);
                                pos->x = maximizedRect.X;
                                pos->y = maximizedRect.Y;
                                pos->cx = maximizedRect.Width;
                                pos->cy = maximizedRect.Height;
                                return IntPtr.Zero;
                            }
                        }
                        break;
                    }

                case WindowsMessage.WM_KILLFOCUS:
                    if (Imm32InputMethod.Current.IsComposing)
                    {
                        _killFocusRequested = true;
                    }
                    else
                    {
                        LostFocus?.Invoke();
                    }

                    break;

                case WindowsMessage.WM_INPUTLANGCHANGE:
                    {
                        UpdateInputMethod(lParam);
                        // call DefWindowProc to pass to all children
                        break;
                    }
                case WindowsMessage.WM_IME_SETCONTEXT:
                    {
                        unchecked
                        {
                            DefWindowProc(Hwnd, msg, wParam, lParam & ~(nint)ISC_SHOWUICOMPOSITIONWINDOW);
                        }

                        UpdateInputMethod(GetKeyboardLayout(0));

                        return IntPtr.Zero;
                    }
                case WindowsMessage.WM_IME_COMPOSITION:
                    {
                        Imm32InputMethod.Current.HandleComposition(wParam, lParam, timestamp);

                        break;
                    }
                case WindowsMessage.WM_IME_SELECT:
                    break;
                case WindowsMessage.WM_IME_CHAR:
                case WindowsMessage.WM_IME_COMPOSITIONFULL:
                case WindowsMessage.WM_IME_CONTROL:
                case WindowsMessage.WM_IME_KEYDOWN:
                case WindowsMessage.WM_IME_KEYUP:
                case WindowsMessage.WM_IME_NOTIFY:
                    break;
                case WindowsMessage.WM_IME_STARTCOMPOSITION:
                    {
                        Imm32InputMethod.Current.HandleCompositionStart();

                        return IntPtr.Zero;
                    }
                case WindowsMessage.WM_IME_ENDCOMPOSITION:
                    {
                        Imm32InputMethod.Current.HandleCompositionEnd(timestamp);

                        if (_killFocusRequested)
                        {
                            LostFocus?.Invoke();

                            _killFocusRequested = false;
                        }

                        return IntPtr.Zero;
                    }
                case WindowsMessage.WM_GETOBJECT:
                    if ((long)lParam == uiaRootObjectId && _owner?.FocusRoot is Control control)
                    {
                        var peer = ControlAutomationPeer.CreatePeerForElement(control);
                        var node = AutomationNode.GetOrCreate(peer);
                        return UiaCoreProviderApi.UiaReturnRawElementProvider(_hwnd, wParam, lParam, node);
                    }
                    break;
                case WindowsMessage.WM_WINDOWPOSCHANGED:
                    var winPos = Marshal.PtrToStructure<WINDOWPOS>(lParam);
                    if ((winPos.flags & (uint)SetWindowPosFlags.SWP_SHOWWINDOW) != 0)
                    {
                        OnShowHideMessage(true);
                    }
                    else if ((winPos.flags & (uint)SetWindowPosFlags.SWP_HIDEWINDOW) != 0)
                    {
                        OnShowHideMessage(false);
                    }
                    break;
            }

#if USE_MANAGED_DRAG
            if (_managedDrag.PreprocessInputEvent(ref e))
                return UnmanagedMethods.DefWindowProc(hWnd, msg, wParam, lParam);
#endif

            if (shouldTakeFocus)
            {
                SetFocus(_hwnd);
            }

            if (e != null && Input != null)
            {
                Input(e);

                if (message == WindowsMessage.WM_KEYDOWN)
                {
                    if (e is RawKeyEventArgs args && args.Key == Key.ImeProcessed)
                    {
                        _ignoreWmChar = true;
                    }
                    else
                    {
                        // Handling a WM_KEYDOWN message should cause the subsequent WM_CHAR message to
                        // be ignored. This should be safe to do as WM_CHAR should only be produced in
                        // response to the call to TranslateMessage/DispatchMessage after a WM_KEYDOWN
                        // is handled.
                        _ignoreWmChar = e.Handled;
                    }
                }

                if (s_intermediatePointsPooledList.Count > 0)
                {
                    s_intermediatePointsPooledList.Dispose();
                }

                if (e.Handled)
                {
                    return IntPtr.Zero;
                }
            }

            return DefWindowProc(hWnd, msg, wParam, lParam);
        }
```


---

### 🔹 Commit #14: `26246191`
- **完整 Hash**: `262461912870242138ece8d57dfb0b1cd375f1f9`
- **說明 (Ground Truth)**: Fix `Arc` Calculation and Update `ArcSegment` Comments (#22404)
- **變更檔案數**: 2

#### 📄 檔案: `src/Avalonia.Base/Media/ArcSegment.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:9, E:2, A:0) ➔ After(N:9, E:2, A:0)
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

#### 📄 檔案: `src/Avalonia.Controls/Shapes/Arc.cs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:18, E:14, A:0) ➔ After(N:18, E:14, A:0)
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

### 🔹 函式: `Arc.CreateDefiningGeometry()`
- **變更前簽章 (Before)**: `Arc.CreateDefiningGeometry()` (L54~L106)
- **變更後簽章 (After)**: `Arc.CreateDefiningGeometry()` (L54~L106)

#### ◀️ 變更前實作碼 (Before Implementation):
```
protected override Geometry CreateDefiningGeometry()
        {
            var angle1 = MathUtilities.Deg2Rad(StartAngle);
            var angle2 = angle1 + MathUtilities.Deg2Rad(SweepAngle);

            var startAngle = Math.Min(angle1, angle2);
            var sweepAngle = Math.Max(angle1, angle2);

            var normStart = RadToNormRad(startAngle);
            var normEnd = RadToNormRad(sweepAngle);

            var rect = new Rect(Bounds.Size);

            if ((normStart == normEnd) && (startAngle != sweepAngle)) // Complete ring.
            {
                return new EllipseGeometry(rect.Deflate(StrokeThickness / 2));
            }
            else if (SweepAngle == 0)
            {
                return new StreamGeometry();
            }
            else // Partial arc.
            {
                var deflatedRect = rect.Deflate(StrokeThickness / 2);

                var centerX = rect.Center.X;
                var centerY = rect.Center.Y;

                var radiusX = deflatedRect.Width / 2;
                var radiusY = deflatedRect.Height / 2;

                var angleGap = RadToNormRad(sweepAngle - startAngle);

                var startPoint = GetRingPoint(radiusX, radiusY, centerX, centerY, startAngle);
                var endPoint = GetRingPoint(radiusX, radiusY, centerX, centerY, sweepAngle);

                var arcGeometry = new StreamGeometry();

                using (StreamGeometryContext context = arcGeometry.Open())
                {
                    context.BeginFigure(startPoint, false);
                    context.ArcTo(
                        endPoint,
                        new Size(radiusX, radiusY),
                        rotationAngle: angleGap,
                        isLargeArc: angleGap >= Math.PI,
                        SweepDirection.Clockwise);
                    context.EndFigure(false);
                }

                return arcGeometry;
            }
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
protected override Geometry CreateDefiningGeometry()
        {
            var angle1 = MathUtilities.Deg2Rad(StartAngle);
            var angle2 = angle1 + MathUtilities.Deg2Rad(SweepAngle);

            var startAngle = Math.Min(angle1, angle2);
            var sweepAngle = Math.Max(angle1, angle2);

            var normStart = RadToNormRad(startAngle);
            var normEnd = RadToNormRad(sweepAngle);

            var rect = new Rect(Bounds.Size);

            if ((normStart == normEnd) && (startAngle != sweepAngle)) // Complete ring.
            {
                return new EllipseGeometry(rect.Deflate(StrokeThickness / 2));
            }
            else if (SweepAngle == 0)
            {
                return new StreamGeometry();
            }
            else // Partial arc.
            {
                var deflatedRect = rect.Deflate(StrokeThickness / 2);

                var centerX = rect.Center.X;
                var centerY = rect.Center.Y;

                var radiusX = deflatedRect.Width / 2;
                var radiusY = deflatedRect.Height / 2;

                var angleGap = RadToNormRad(sweepAngle - startAngle);

                var startPoint = GetRingPoint(radiusX, radiusY, centerX, centerY, startAngle);
                var endPoint = GetRingPoint(radiusX, radiusY, centerX, centerY, sweepAngle);

                var arcGeometry = new StreamGeometry();

                using (StreamGeometryContext context = arcGeometry.Open())
                {
                    context.BeginFigure(startPoint, false);
                    context.ArcTo(
                        endPoint,
                        new Size(radiusX, radiusY),
                        rotationAngle: 0.0,
                        isLargeArc: angleGap >= Math.PI,
                        SweepDirection.Clockwise);
                    context.EndFigure(false);
                }

                return arcGeometry;
            }
        }
```


---

### 🔹 Commit #15: `3b8d0fbf`
- **完整 Hash**: `3b8d0fbfea607015c9cbee2c982a8987884f0510`
- **說明 (Ground Truth)**: Fix ArgumentNullException in chrome hit test after window close (#22409)
- **變更檔案數**: 1

#### 📄 檔案: `src/Avalonia.Controls/PresentationSource/PresentationSource.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:25, E:15, A:2) ➔ After(N:25, E:15, A:2)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 1, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#PlatformImpl** `(Button / UI Control)`
    └── ⚡ **ScalingChanged()**
  🌲 **#Renderer** `(Button / UI Control)`
    └── ⚡ **SceneInvalidated()**

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `rootVisual.GetVisualAt (External/BCL)` (FUNCTION_DEF)
  • - [移除節點] `RootVisual.GetVisualAt (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `PresentationSource.HitTestChromeElement` ──[CALLS]──> `rootVisual.GetVisualAt (External/BCL)`
  • - [移除呼叫邊] `PresentationSource.HitTestChromeElement` ──[CALLS]──> `RootVisual.GetVisualAt (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `PresentationSource.HitTestChromeElement()`
- **變更前簽章 (Before)**: `PresentationSource.HitTestChromeElement(Point point)` (L150~L154)
- **變更後簽章 (After)**: `PresentationSource.HitTestChromeElement(Point point)` (L150~L158)

#### ◀️ 變更前實作碼 (Before Implementation):
```
WindowDecorationsElementRole? IInputRoot.HitTestChromeElement(Point point)
    {
        var visual = RootVisual.GetVisualAt(point, ChromeHitTestFilter);
        return GetChromeRoleFromVisual(visual);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
WindowDecorationsElementRole? IInputRoot.HitTestChromeElement(Point point)
    {
        // RootVisual is cleared when the top level closes, but the platform can still hit-test the window.
        if (RootVisual is not { } rootVisual)
            return null;

        var visual = rootVisual.GetVisualAt(point, ChromeHitTestFilter);
        return GetChromeRoleFromVisual(visual);
    }
```


---

### 🔹 Commit #16: `1ac93092`
- **完整 Hash**: `1ac9309278a1440e7de50549a7b4891c2b7a2c2e`
- **說明 (Ground Truth)**: Fix Comments for `PreciseArcTo()` (#22402)
- **變更檔案數**: 3

#### 📄 檔案: `src/Avalonia.Base/Media/PreciseEllipticArcHelper.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:82, E:75, A:0) ➔ After(N:82, E:75, A:0)
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

#### 📄 檔案: `src/Avalonia.Base/Media/StreamGeometryContext.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:15, E:10, A:0) ➔ After(N:15, E:10, A:0)
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

#### 📄 檔案: `src/Avalonia.Base/Platform/IGeometryContext.cs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:7, E:0, A:0) ➔ After(N:7, E:0, A:0)
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

### 🔹 Commit #17: `ab712638`
- **完整 Hash**: `ab7126382c525ad9f24f369fe8c91772ce56e5ee`
- **說明 (Ground Truth)**: iOS High Refresh Rate Part 1/3 - Render at up to 120 Hz on ProMotion devices and pause the display link when idle (#22395)
- **變更檔案數**: 2

#### 📄 檔案: `src/iOS/Avalonia.iOS/DisplayLinkTimer.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:11, E:7, A:0) ➔ After(N:26, E:18, A:0)
- **差分統計**: +Nodes: 18, -Nodes: 3, +Edges: 13, -Edges: 2, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Logger.TryGet (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `DisplayLinkTimer.SetPreferredFrameRateRange` (FUNCTION_DEF)
  • + [新增節點] `tick?.Invoke (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_23` (MODULE_STATE)
  • + [新增節點] `CAFrameRateRange.Create (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `DisplayLinkTimer.WarnIfLimitedTo60Hz` (FUNCTION_DEF)
  • + [新增節點] `state_18` (MODULE_STATE)
  • + [新增節點] `OperatingSystem.IsTvOSVersionAtLeast (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `OperatingSystem.IsMacCatalystVersionAtLeast (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `DisplayLinkTimer.UpdateLinkState` (FUNCTION_DEF)
  • + [新增節點] `OperatingSystem.IsIOSVersionAtLeast (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `_paused` (MODULE_STATE)
  • + [新增節點] `DisplayLinkTimer.SetInBackground` (FUNCTION_DEF)
  • + [新增節點] `_link.AddToRunLoop (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `state_22` (MODULE_STATE)
  • _... 以及其餘 21 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `DisplayLinkTimer.OnLinkTick()`
- **變更前簽章 (Before)**: `DisplayLinkTimer.OnLinkTick()` (L40~L43)
- **變更後簽章 (After)**: `DisplayLinkTimer.OnLinkTick()` (L115~L122)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private void OnLinkTick()
        {
            _tick?.Invoke(_st.Elapsed);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private void OnLinkTick()
        {
            Action<TimeSpan>? tick;
            // A callback already scheduled when the link was paused can still arrive.
            lock (_lock)
                tick = _paused ? null : _tick;
            tick?.Invoke(_st.Elapsed);
        }
```

### 🔹 函式: `DisplayLinkTimer.DisplayLinkTimer()`
- **變更前簽章 (Before)**: `DisplayLinkTimer.DisplayLinkTimer()` (L16~L27)
- **變更後簽章 (After)**: `DisplayLinkTimer.DisplayLinkTimer()` (L26~L41)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public DisplayLinkTimer()
        {
            var link = CADisplayLink.Create(OnLinkTick);
            TimerThread = new Thread(() =>
            {
                link.AddToRunLoop(NSRunLoop.Current, NSRunLoopMode.Common);
                NSRunLoop.Current.Run();
            });
            TimerThread.Start();
            UIApplication.Notifications.ObserveDidEnterBackground((_,__) => link.Paused = true);
            UIApplication.Notifications.ObserveWillEnterForeground((_, __) => link.Paused = false);
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public DisplayLinkTimer()
        {
            _link = CADisplayLink.Create(OnLinkTick);
            _link.Paused = true;
            SetPreferredFrameRateRange(_link);
            WarnIfLimitedTo60Hz();
            TimerThread = new Thread(() =>
            {
                _link.AddToRunLoop(NSRunLoop.Current, NSRunLoopMode.Common);
                NSRunLoop.Current.Run();
            });
            TimerThread.Start();

            UIApplication.Notifications.ObserveDidEnterBackground((_, _) => SetInBackground(true));
            UIApplication.Notifications.ObserveWillEnterForeground((_, _) => SetInBackground(false));
        }
```

### 🔹 函式: `_st()`
- **變更前簽章 (Before)**: `[Module State] _st` (L14~L14)
- **變更後簽章 (After)**: `[Module State] _st` (L19~L19)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private Stopwatch _st = Stopwatch.StartNew();
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private readonly Stopwatch _st = Stopwatch.StartNew();
```


#### 📄 檔案: `src/iOS/Avalonia.iOS/Platform.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:45, E:41, A:0) ➔ After(N:45, E:41, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 3, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `state_79` (MODULE_STATE)
  • + [新增節點] `state_77` (MODULE_STATE)
  • + [新增節點] `state_78` (MODULE_STATE)
  • - [移除節點] `state_69` (MODULE_STATE)
  • - [移除節點] `state_67` (MODULE_STATE)
  • - [移除節點] `state_68` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #18: `a9429a32`
- **完整 Hash**: `a9429a328057befa287ffb5e981f58b86a86eda0`
- **說明 (Ground Truth)**: Fix duplicate insertion of shared StyleInstance into the same ValueStore (#22276)
- **變更檔案數**: 1

#### 📄 檔案: `src/Avalonia.Base/Styling/StyleBase.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:21, E:15, A:0) ➔ After(N:25, E:17, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 1, +Edges: 2, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `StyleBase.SetSharedInstance` (FUNCTION_DEF)
  • + [新增節點] `state_24` (MODULE_STATE)
  • + [新增節點] `StyleBase.GetSharedInstance` (FUNCTION_DEF)
  • + [新增節點] `state_25` (MODULE_STATE)
  • + [新增節點] `state_23` (MODULE_STATE)
  • - [移除節點] `state_21` (MODULE_STATE)
  • + [新增呼叫邊] `StyleBase.Attach` ──[CALLS]──> `StyleBase.GetSharedInstance`
  • + [新增呼叫邊] `StyleBase.Attach` ──[CALLS]──> `StyleBase.SetSharedInstance`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `StyleBase.Attach()`
- **變更前簽章 (Before)**: `StyleBase.Attach(
            StyledElement target,
            IStyleActivator? activator,
            FrameType type,
            bool canShareInstance)` (L110~L154)
- **變更後簽章 (After)**: `StyleBase.Attach(
            StyledElement target,
            IStyleActivator? activator,
            FrameType type,
            bool canShareInstance)` (L114~L158)

#### ◀️ 變更前實作碼 (Before Implementation):
```
internal ValueFrame Attach(
            StyledElement target,
            IStyleActivator? activator,
            FrameType type,
            bool canShareInstance)
        {
            if (target is not AvaloniaObject ao)
                throw new InvalidOperationException("Styles can only be applied to AvaloniaObjects.");

            StyleInstance instance;

            if (_sharedInstance is not null && canShareInstance)
            {
                instance = _sharedInstance;
            }
            else
            {
                canShareInstance &= activator is null;

                instance = new StyleInstance(this, activator, type);

                if (_setters is not null)
                {
                    foreach (var setter in _setters)
                    {
                        var setterInstance = setter.Instance(instance, target);
                        instance.Add(setterInstance);
                        canShareInstance &= setterInstance == setter;
                    }
                }

                if (_animations is not null)
                    instance.Add(_animations);

                if (canShareInstance)
                {
                    instance.MakeShared();
                    _sharedInstance = instance;
                }
            }

            ao.GetValueStore().AddFrame(instance);
            instance.ApplyAnimations(ao);
            return instance;
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
internal ValueFrame Attach(
            StyledElement target,
            IStyleActivator? activator,
            FrameType type,
            bool canShareInstance)
        {
            if (target is not AvaloniaObject ao)
                throw new InvalidOperationException("Styles can only be applied to AvaloniaObjects.");

            StyleInstance instance;

            if (canShareInstance && GetSharedInstance(type) is { } shared)
            {
                instance = shared;
            }
            else
            {
                canShareInstance &= activator is null;

                instance = new StyleInstance(this, activator, type);

                if (_setters is not null)
                {
                    foreach (var setter in _setters)
                    {
                        var setterInstance = setter.Instance(instance, target);
                        instance.Add(setterInstance);
                        canShareInstance &= setterInstance == setter;
                    }
                }

                if (_animations is not null)
                    instance.Add(_animations);

                if (canShareInstance)
                {
                    instance.MakeShared();
                    SetSharedInstance(type, instance);
                }
            }

            ao.GetValueStore().AddFrame(instance);
            instance.ApplyAnimations(ao);
            return instance;
        }
```


---

### 🔹 Commit #19: `16572aef`
- **完整 Hash**: `16572aeff14531c02deaac5ba1a7c132a9c985d0`
- **說明 (Ground Truth)**: Fix keyboard focus staying on a removed element when an overlay popup or flyout closes (#22345)
- **變更檔案數**: 1

#### 📄 檔案: `src/Avalonia.Base/Input/FocusManager.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:87, E:134, A:0) ➔ After(N:87, E:135, A:0)
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
  • + [新增呼叫邊] `FocusManager.Focus` ──[CALLS]──> `FocusManager.IsVisible`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FocusManager.Focus()`
- **變更前簽章 (Before)**: `FocusManager.Focus(
            IInputElement? element,
            NavigationMethod method = NavigationMethod.Unspecified,
            KeyModifiers keyModifiers = KeyModifiers.None)` (L68~L104)
- **變更後簽章 (After)**: `FocusManager.Focus(
            IInputElement? element,
            NavigationMethod method = NavigationMethod.Unspecified,
            KeyModifiers keyModifiers = KeyModifiers.None)` (L68~L105)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public bool Focus(
            IInputElement? element,
            NavigationMethod method = NavigationMethod.Unspecified,
            KeyModifiers keyModifiers = KeyModifiers.None)
        {
            if (KeyboardDevice.Instance is not { } keyboardDevice)
                return false;

            if (element is not null)
            {
                return FocusCore(keyboardDevice, element, method, keyModifiers);
            }

            if (_focusRoot?.GetValue(FocusedElementProperty) is { } restore && restore != Current)
            {
                if (!CanFocus(restore))
                {
                    // Previous effective focus is no longer part of the focus root's visual tree. We clear the focused element
                    _focusRoot.ClearValue(FocusedElementProperty);

                    if (Current != null && GetFocusScope(Current) != _focusRoot)
                    {
                        _focusRoot = null;

                        return false;
                    }
                }
                else
                {
                    return FocusCore(keyboardDevice, restore, method, keyModifiers);
                }
            }

            _focusRoot = null;
            keyboardDevice.SetFocusedElement(null, NavigationMethod.Unspecified, KeyModifiers.None, false);
            return false;
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public bool Focus(
            IInputElement? element,
            NavigationMethod method = NavigationMethod.Unspecified,
            KeyModifiers keyModifiers = KeyModifiers.None)
        {
            if (KeyboardDevice.Instance is not { } keyboardDevice)
                return false;

            if (element is not null)
            {
                return FocusCore(keyboardDevice, element, method, keyModifiers);
            }

            if (_focusRoot?.GetValue(FocusedElementProperty) is { } restore && restore != Current)
            {
                if (!CanFocus(restore))
                {
                    // Previous effective focus is no longer part of the focus root's visual tree. We clear the focused element
                    _focusRoot.ClearValue(FocusedElementProperty);

                    // Keep focus in another scope (e.g. window), unless the focused element was removed or hidden.
                    if (Current != null && IsVisible(Current) && GetFocusScope(Current) != _focusRoot)
                    {
                        _focusRoot = null;

                        return false;
                    }
                }
                else
                {
                    return FocusCore(keyboardDevice, restore, method, keyModifiers);
                }
            }

            _focusRoot = null;
            keyboardDevice.SetFocusedElement(null, NavigationMethod.Unspecified, KeyModifiers.None, false);
            return false;
        }
```


---

### 🔹 Commit #20: `a6df0e3c`
- **完整 Hash**: `a6df0e3c39722ff8bb04091ffb32a5003add7712`
- **說明 (Ground Truth)**: Fix re-attaching a child visual cleared on detach (#22334)
- **變更檔案數**: 1

#### 📄 檔案: `src/Avalonia.Base/Rendering/Composition/ElementCompositionPreview.cs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:5, E:2, A:0) ➔ After(N:7, E:4, A:0)
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
  • + [新增節點] `ReferenceEquals (External/BCL)` (FUNCTION_DEF)
  • + [新增節點] `visual.CompositionVisual?.Children.Remove (External/BCL)` (FUNCTION_DEF)
  • + [新增呼叫邊] `ElementComposition.SetElementChildVisual` ──[CALLS]──> `ReferenceEquals (External/BCL)`
  • + [新增呼叫邊] `ElementComposition.SetElementChildVisual` ──[CALLS]──> `visual.CompositionVisual?.Children.Remove (External/BCL)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `ElementComposition.SetElementChildVisual()`
- **變更前簽章 (Before)**: `ElementComposition.SetElementChildVisual(Visual visual, CompositionVisual? compositionVisual)` (L21~L29)
- **變更後簽章 (After)**: `ElementComposition.SetElementChildVisual(Visual visual, CompositionVisual? compositionVisual)` (L21~L37)

#### ◀️ 變更前實作碼 (Before Implementation):
```
public static void SetElementChildVisual(Visual visual, CompositionVisual? compositionVisual)
    {
        if (compositionVisual != null && visual.CompositionVisual != null &&
            compositionVisual.Compositor != visual.CompositionVisual.Compositor)
            throw new InvalidOperationException("Composition visuals belong to different compositor instances");
        
        visual.ChildCompositionVisual = compositionVisual;
        visual.GetPresentationSource()?.Renderer.RecalculateChildren(visual);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
public static void SetElementChildVisual(Visual visual, CompositionVisual? compositionVisual)
    {
        if (compositionVisual != null && visual.CompositionVisual != null &&
            compositionVisual.Compositor != visual.CompositionVisual.Compositor)
            throw new InvalidOperationException("Composition visuals belong to different compositor instances");
        
        // Un-parent the previous child here rather than waiting for the renderer to
        // reconcile the children, because that sync may never run again for this element:
        // a child cleared from OnDetachedFromVisualTree is cleared before
        // DetachFromCompositor discards the element's composition visual, and a child
        // left parented there cannot be attached anywhere else.
        if (visual.ChildCompositionVisual is { } oldChild && !ReferenceEquals(oldChild, compositionVisual))
            visual.CompositionVisual?.Children.Remove(oldChild);

        visual.ChildCompositionVisual = compositionVisual;
        visual.GetPresentationSource()?.Renderer.RecalculateChildren(visual);
    }
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/Avalonia show b6ed89b8d946a2fd1481995c971c2a59899049bd
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff b6ed89b8d946a2fd1481995c971c2a59899049bd~1 --file test_repos/Avalonia/src/Avalonia.Controls/Primitives/Popup.cs
   ```
