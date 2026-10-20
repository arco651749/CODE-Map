# 🔬 CODE-Map 基準審查獨立驗證報告: `axum`
> **技術生態**: `Rust (Tokio 旗艦非同步 Web 框架 / Tower)`  
> **本地倉庫路徑**: `test_repos/axum`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 27 Files  
> **報告生成時間**: 2026-10-20 21:42:32  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `17` / `27` | `63.0%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `3` / `27` | `11.1%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `7` / `27` | `25.9%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`20` / `27`** | **`74.1%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `27` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `a000c300`
- **完整 Hash**: `a000c300848c0be7ba0f63ebabd5dbe0f6643067`
- **說明 (Ground Truth)**: axum-core: fix body stream size hints (#3925)
- **變更檔案數**: 1

#### 📄 檔案: `axum-core/src/body.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:44, E:51, A:0) ➔ After(N:38, E:50, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 7, +Edges: 7, -Edges: 8, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `data_stream_size_hints` (FUNCTION_DEF)
  • - [移除節點] `usize::try_from(size_hint.lower()).unwrap_or_default (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `BodyDataStream::size_hint` (FUNCTION_DEF)
  • - [移除節點] `size_hint.lower (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `size_hint.upper().and_then (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `usize::try_from (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `usize::try_from(v).ok (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `size_hint.upper (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `BodyDataStream::size_hint` ──[CALLS]──> `BodyDataStream::size_hint`
  • + [新增呼叫邊] `data_stream_size_hints` ──[CALLS]──> `Body::into_data_stream`
  • + [新增呼叫邊] `data_stream_size_hints` ──[CALLS]──> `Body::empty`
  • + [新增呼叫邊] `data_stream_size_hints` ──[CALLS]──> `assert_eq! (Macro)`
  • + [新增呼叫邊] `data_stream_size_hints` ──[CALLS]──> `BodyDataStream::size_hint`
  • + [新增呼叫邊] `data_stream_size_hints` ──[CALLS]──> `Body::from`
  • + [新增呼叫邊] `data_stream_size_hints` ──[CALLS]──> `Body::from_stream`
  • _... 以及其餘 8 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `BodyDataStream::size_hint()`
- **變更前簽章 (Before)**: `fn BodyDataStream::size_hint(&self)` (L189~L194)
- **變更後簽章 (After)**: `fn BodyDataStream::size_hint(&self)` (L207~L209)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn size_hint(&self) -> (usize, Option<usize>) {
        let size_hint = self.inner.size_hint();
        let lower = usize::try_from(size_hint.lower()).unwrap_or_default();
        let upper = size_hint.upper().and_then(|v| usize::try_from(v).ok());
        (lower, upper)
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn size_hint(&self) -> http_body::SizeHint {
        self.inner.size_hint()
    }
```


---

### 🔹 Commit #02: `f8b02f22`
- **完整 Hash**: `f8b02f22cf10bee707bda19b58265b9e33677535`
- **說明 (Ground Truth)**: axum: Don't wrap merged service routes in another Route (#3909)
- **變更檔案數**: 1

#### 📄 檔案: `axum/src/routing/path_router.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:86, E:131, A:0) ➔ After(N:86, E:131, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 1, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `PathRouter::merge` ──[CALLS]──> `PathRouter::route_endpoint`
  • - [移除呼叫邊] `PathRouter::merge` ──[CALLS]──> `PathRouter::route_service`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `PathRouter::merge()`
- **變更前簽章 (Before)**: `fn PathRouter::merge(&mut self, other: Self)` (L115~L132)
- **變更後簽章 (After)**: `fn PathRouter::merge(&mut self, other: Self)` (L115~L133)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(super) fn merge(&mut self, other: Self) -> Result<(), Cow<'static, str>> {
        let Self { routes, node } = other;

        for (id, route) in routes.into_iter().enumerate() {
            let route_id = RouteId(id);
            let path = node
                .route_id_to_path
                .get(&route_id)
                .expect("no path for route id. This is a bug in axum. Please file an issue");

            match route {
                Endpoint::MethodRouter(method_router) => self.route(path, method_router)?,
                Endpoint::Route(route) => self.route_service(path, route)?,
            }
        }

        Ok(())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(super) fn merge(&mut self, other: Self) -> Result<(), Cow<'static, str>> {
        let Self { routes, node } = other;

        for (id, route) in routes.into_iter().enumerate() {
            let route_id = RouteId(id);
            let path = node
                .route_id_to_path
                .get(&route_id)
                .expect("no path for route id. This is a bug in axum. Please file an issue");

            match route {
                Endpoint::MethodRouter(method_router) => self.route(path, method_router)?,
                // `route_service` would wrap this `Route` in another `Route`
                endpoint @ Endpoint::Route(_) => self.route_endpoint(path, endpoint)?,
            }
        }

        Ok(())
    }
```


---

### 🔹 Commit #03: `b14732f0`
- **完整 Hash**: `b14732f08cb54bde5b2ba3cfe324af3f6747b568`
- **說明 (Ground Truth)**: fix(axum-extra): handle missing optional typed headers (#3886)
- **變更檔案數**: 1

#### 📄 檔案: `axum-extra/src/typed_header.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:46, E:48, A:0) ➔ After(N:49, E:56, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 8, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `optional_cookie_is_none_when_missing` (FUNCTION_DEF)
  • + [新增節點] `cookie.is_none (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `handle` (FUNCTION_DEF)
  • + [新增呼叫邊] `optional_cookie_is_none_when_missing` ──[CALLS]──> `Router::new().route (External/Unresolved)`
  • + [新增呼叫邊] `optional_cookie_is_none_when_missing` ──[CALLS]──> `Router::new (External/Unresolved)`
  • + [新增呼叫邊] `optional_cookie_is_none_when_missing` ──[CALLS]──> `get (External/Unresolved)`
  • + [新增呼叫邊] `optional_cookie_is_none_when_missing` ──[CALLS]──> `TestClient::new (External/Unresolved)`
  • + [新增呼叫邊] `optional_cookie_is_none_when_missing` ──[CALLS]──> `client.get (External/Unresolved)`
  • + [新增呼叫邊] `optional_cookie_is_none_when_missing` ──[CALLS]──> `assert_eq! (Macro)`
  • + [新增呼叫邊] `optional_cookie_is_none_when_missing` ──[CALLS]──> `client.get("/").header (External/Unresolved)`
  • + [新增呼叫邊] `handle` ──[CALLS]──> `cookie.is_none (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TypedHeader::from_request_parts()`
- **變更前簽章 (Before)**: `fn TypedHeader::from_request_parts(
        parts: &mut Parts,
        _state: &S,
    )` (L88~L102)
- **變更後簽章 (After)**: `fn TypedHeader::from_request_parts(
        parts: &mut Parts,
        _state: &S,
    )` (L88~L104)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async fn from_request_parts(
        parts: &mut Parts,
        _state: &S,
    ) -> Result<Option<Self>, Self::Rejection> {
        let mut values = parts.headers.get_all(T::name()).iter();
        let is_missing = values.size_hint() == (0, Some(0));
        match T::decode(&mut values) {
            Ok(res) => Ok(Some(Self(res))),
            Err(_) if is_missing => Ok(None),
            Err(err) => Err(TypedHeaderRejection {
                name: T::name(),
                reason: TypedHeaderRejectionReason::Error(err),
            }),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async fn from_request_parts(
        parts: &mut Parts,
        _state: &S,
    ) -> Result<Option<Self>, Self::Rejection> {
        let mut values = parts.headers.get_all(T::name()).iter();
        if values.size_hint() == (0, Some(0)) {
            return Ok(None);
        }

        match T::decode(&mut values) {
            Ok(value) => Ok(Some(Self(value))),
            Err(err) => Err(TypedHeaderRejection {
                name: T::name(),
                reason: TypedHeaderRejectionReason::Error(err),
            }),
        }
    }
```


---

### 🔹 Commit #04: `715e9a89`
- **完整 Hash**: `715e9a8950b910dd6bb71aac48ce3633c9359ed0`
- **說明 (Ground Truth)**: fix(axum-extra): preserve protobuf body buffering rejections (#3881)
- **變更檔案數**: 1

#### 📄 檔案: `axum-extra/src/protobuf.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:40, E:53, A:0) ➔ After(N:40, E:62, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 4, +Edges: 13, -Edges: 4, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Router::new()
            .route (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `DefaultBodyLimit::max (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `body_too_large_is_bytes_rejection` (FUNCTION_DEF)
  • + [新增節點] `Router::new()
            .route("/", post(|_: Protobuf<Input>| async {}))
            .layer (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `req
            .into_limited_body()
            .collect()
            .await
            .map_err(ProtobufDecodeError)?
            .aggregate (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `req
            .into_limited_body()
            .collect()
            .await
            .map_err (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `req
            .into_limited_body (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `req
            .into_limited_body()
            .collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Protobuf::from_request` ──[CALLS]──> `Protobuf::from_request`
  • + [新增呼叫邊] `body_too_large_is_bytes_rejection` ──[CALLS]──> `Router::new()
            .route("/", post(|_: Protobuf<Input>| async {}))
            .layer (External/Unresolved)`
  • + [新增呼叫邊] `body_too_large_is_bytes_rejection` ──[CALLS]──> `Router::new()
            .route (External/Unresolved)`
  • + [新增呼叫邊] `body_too_large_is_bytes_rejection` ──[CALLS]──> `Router::new (External/Unresolved)`
  • + [新增呼叫邊] `body_too_large_is_bytes_rejection` ──[CALLS]──> `post (External/Unresolved)`
  • + [新增呼叫邊] `body_too_large_is_bytes_rejection` ──[CALLS]──> `DefaultBodyLimit::max (External/Unresolved)`
  • + [新增呼叫邊] `body_too_large_is_bytes_rejection` ──[CALLS]──> `"bar".to_owned (External/Unresolved)`
  • _... 以及其餘 10 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Protobuf::from_request()`
- **變更前簽章 (Before)**: `fn Protobuf::from_request(req: Request, _: &S)` (L103~L115)
- **變更後簽章 (After)**: `fn Protobuf::from_request(req: Request, state: &S)` (L101~L108)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async fn from_request(req: Request, _: &S) -> Result<Self, Self::Rejection> {
        let mut buf = req
            .into_limited_body()
            .collect()
            .await
            .map_err(ProtobufDecodeError)?
            .aggregate();

        match T::decode(&mut buf) {
            Ok(value) => Ok(Self(value)),
            Err(err) => Err(ProtobufDecodeError::from_err(err).into()),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async fn from_request(req: Request, state: &S) -> Result<Self, Self::Rejection> {
        let bytes = Bytes::from_request(req, state).await?;

        match T::decode(bytes) {
            Ok(value) => Ok(Self(value)),
            Err(err) => Err(ProtobufDecodeError::from_err(err).into()),
        }
    }
```


---

### 🔹 Commit #05: `c9a911b7`
- **完整 Hash**: `c9a911b7999de50e9e5023942ca072e9725ae943`
- **說明 (Ground Truth)**: axum-core: fix nested error downcast (#3858)
- **變更檔案數**: 1

#### 📄 檔案: `axum-core/src/extract/rejection.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:8, E:8, A:0) ➔ After(N:7, E:7, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 2, +Edges: 1, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `unwrapped.into_inner (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `err.into().downcast::<Error> (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `err.into_inner (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `FailedToBufferBody::from_err` ──[CALLS]──> `unwrapped.into_inner (External/Unresolved)`
  • - [移除呼叫邊] `FailedToBufferBody::from_err` ──[CALLS]──> `err.into().downcast::<Error> (External/Unresolved)`
  • - [移除呼叫邊] `FailedToBufferBody::from_err` ──[CALLS]──> `err.into_inner (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FailedToBufferBody::from_err()`
- **變更前簽章 (Before)**: `fn FailedToBufferBody::from_err(err: E)` (L18~L37)
- **變更後簽章 (After)**: `fn FailedToBufferBody::from_err(err: E)` (L18~L39)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub(crate) fn from_err<E>(err: E) -> Self
    where
        E: Into<BoxError>,
    {
        // two layers of boxes here because `with_limited_body`
        // wraps the `http_body_util::Limited` in an `axum_core::Body`
        // which also wraps the error type
        let box_error = match err.into().downcast::<Error>() {
            Ok(err) => err.into_inner(),
            Err(err) => err,
        };
        let box_error = match box_error.downcast::<Error>() {
            Ok(err) => err.into_inner(),
            Err(err) => err,
        };
        match box_error.downcast::<http_body_util::LengthLimitError>() {
            Ok(err) => Self::LengthLimitError(LengthLimitError::from_err(err)),
            Err(err) => Self::UnknownBodyError(UnknownBodyError::from_err(err)),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub(crate) fn from_err<E>(err: E) -> Self
    where
        E: Into<BoxError>,
    {
        // peel any number of `axum_core::Error` wrappers to reach the underlying source error
        let mut box_error = err.into();
        loop {
            match box_error.downcast::<Error>() {
                Ok(unwrapped) => {
                    box_error = unwrapped.into_inner();
                }
                Err(err) => {
                    box_error = err;
                    break;
                }
            }
        }
        match box_error.downcast::<http_body_util::LengthLimitError>() {
            Ok(err) => Self::LengthLimitError(LengthLimitError::from_err(err)),
            Err(err) => Self::UnknownBodyError(UnknownBodyError::from_err(err)),
        }
    }
```


---

### 🔹 Commit #06: `3f06eadb`
- **完整 Hash**: `3f06eadb1da3a6d8aa6c6b9caf4bb9d09606c7af`
- **說明 (Ground Truth)**: fix(axum-extra): reject opaque Attachment filenames (#3848)
- **變更檔案數**: 1

#### 📄 檔案: `axum-extra/src/response/attachment.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:22, E:42, A:0) ➔ After(N:27, E:53, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 0, +Edges: 11, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `attachment_with_opaque_filename` (FUNCTION_DEF)
  • + [新增節點] `filename.to_str().is_ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `HeaderValue::from_bytes(b"report\xff.pdf").unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `HeaderValue::from_bytes (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `filename.to_str (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Attachment::filename` ──[CALLS]──> `filename.to_str().is_ok (External/Unresolved)`
  • + [新增呼叫邊] `Attachment::filename` ──[CALLS]──> `filename.to_str (External/Unresolved)`
  • + [新增呼叫邊] `attachment_with_opaque_filename` ──[CALLS]──> `HeaderValue::from_bytes(b"report\xff.pdf").unwrap (External/Unresolved)`
  • + [新增呼叫邊] `attachment_with_opaque_filename` ──[CALLS]──> `HeaderValue::from_bytes (External/Unresolved)`
  • + [新增呼叫邊] `attachment_with_opaque_filename` ──[CALLS]──> `Attachment::into_response`
  • + [新增呼叫邊] `attachment_with_opaque_filename` ──[CALLS]──> `Attachment::filename`
  • + [新增呼叫邊] `attachment_with_opaque_filename` ──[CALLS]──> `Attachment::new`
  • + [新增呼叫邊] `attachment_with_opaque_filename` ──[CALLS]──> `attachment.headers().get(CONTENT_DISPOSITION).unwrap (External/Unresolved)`
  • + [新增呼叫邊] `attachment_with_opaque_filename` ──[CALLS]──> `attachment.headers().get (External/Unresolved)`
  • + [新增呼叫邊] `attachment_with_opaque_filename` ──[CALLS]──> `attachment.headers (External/Unresolved)`
  • _... 以及其餘 1 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Attachment::filename()`
- **變更前簽章 (Before)**: `fn Attachment::filename(mut self, value: H)` (L58~L66)
- **變更後簽章 (After)**: `fn Attachment::filename(mut self, value: H)` (L58~L67)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn filename<H: TryInto<HeaderValue>>(mut self, value: H) -> Self {
        self.filename = if let Ok(filename) = value.try_into() {
            Some(filename)
        } else {
            error!("Attachment filename contains invalid characters");
            None
        };
        self
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn filename<H: TryInto<HeaderValue>>(mut self, value: H) -> Self {
        self.filename = match value.try_into() {
            Ok(filename) if filename.to_str().is_ok() => Some(filename),
            _ => {
                error!("Attachment filename contains invalid characters");
                None
            }
        };
        self
    }
```


---

### 🔹 Commit #07: `502aa875`
- **完整 Hash**: `502aa875b78bccd7d743dbd783447050c3450139`
- **說明 (Ground Truth)**: fix(axum-core): skip non-data frames in BytesMut (#3811)
- **變更檔案數**: 1

#### 📄 檔案: `axum-core/src/extract/request_parts.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:48, E:48, A:0) ➔ After(N:48, E:48, A:0)
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

### 🔹 函式: `body_to_bytes_mut()`
- **變更前簽章 (Before)**: `fn body_to_bytes_mut(body: &mut Body, bytes: &mut BytesMut)` (L84~L98)
- **變更後簽章 (After)**: `fn body_to_bytes_mut(body: &mut Body, bytes: &mut BytesMut)` (L84~L99)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async fn body_to_bytes_mut(body: &mut Body, bytes: &mut BytesMut) -> Result<(), BytesRejection> {
    while let Some(frame) = body
        .frame()
        .await
        .transpose()
        .map_err(FailedToBufferBody::from_err)?
    {
        let Ok(data) = frame.into_data() else {
            return Ok(());
        };
        bytes.put(data);
    }

    Ok(())
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async fn body_to_bytes_mut(body: &mut Body, bytes: &mut BytesMut) -> Result<(), BytesRejection> {
    while let Some(frame) = body
        .frame()
        .await
        .transpose()
        .map_err(FailedToBufferBody::from_err)?
    {
        let Ok(data) = frame.into_data() else {
            // Match `Bytes` by ignoring non-data frames until the body ends.
            continue;
        };
        bytes.put(data);
    }

    Ok(())
}
```


---

### 🔹 Commit #08: `b7e37889`
- **完整 Hash**: `b7e37889932edcf521ca54e5ed30245f01180994`
- **說明 (Ground Truth)**: fix(axum): deduplicate methods in the `Allow` header after merging `MethodRouter`s (#3836)
- **變更檔案數**: 1

#### 📄 檔案: `axum/src/routing/method_routing.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:185, E:275, A:0) ➔ After(N:187, E:283, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 1, +Edges: 9, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `allow_header_merging_get_into_head` (FUNCTION_DEF)
  • + [新增節點] `methods.split (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `panic! [未完成實作/執行期中斷]` (FUNCTION_DEF)
  • - [移除節點] `a.extend_from_slice (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `AllowHeader::merge` ──[CALLS]──> `std::str::from_utf8 (External/Unresolved)`
  • + [新增呼叫邊] `AllowHeader::merge` ──[CALLS]──> `methods.split (External/Unresolved)`
  • + [新增呼叫邊] `AllowHeader::merge` ──[CALLS]──> `append_allow_header`
  • + [新增呼叫邊] `AllowHeader::merge` ──[CALLS]──> `panic! [未完成實作/執行期中斷]`
  • + [新增呼叫邊] `allow_header_merging_get_into_head` ──[CALLS]──> `get (External/Unresolved)`
  • + [新增呼叫邊] `allow_header_merging_get_into_head` ──[CALLS]──> `head (External/Unresolved)`
  • + [新增呼叫邊] `allow_header_merging_get_into_head` ──[CALLS]──> `merge`
  • + [新增呼叫邊] `allow_header_merging_get_into_head` ──[CALLS]──> `call`
  • + [新增呼叫邊] `allow_header_merging_get_into_head` ──[CALLS]──> `assert_eq! (Macro)`
  • - [移除呼叫邊] `AllowHeader::merge` ──[CALLS]──> `a.extend_from_slice (External/Unresolved)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `AllowHeader::merge()`
- **變更前簽章 (Before)**: `fn AllowHeader::merge(self, other: Self)` (L572~L583)
- **變更後簽章 (After)**: `fn AllowHeader::merge(self, other: Self)` (L572~L592)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn merge(self, other: Self) -> Self {
        match (self, other) {
            (Self::Skip, _) | (_, Self::Skip) => Self::Skip,
            (Self::None, Self::None) => Self::None,
            (Self::None, Self::Bytes(pick)) | (Self::Bytes(pick), Self::None) => Self::Bytes(pick),
            (Self::Bytes(mut a), Self::Bytes(b)) => {
                a.extend_from_slice(b",");
                a.extend_from_slice(&b);
                Self::Bytes(a)
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn merge(self, other: Self) -> Self {
        match (self, other) {
            (Self::Skip, _) | (_, Self::Skip) => Self::Skip,
            (Self::None, Self::None) => Self::None,
            (Self::None, Self::Bytes(pick)) | (Self::Bytes(pick), Self::None) => Self::Bytes(pick),
            (mut this @ Self::Bytes(_), Self::Bytes(b)) => {
                match std::str::from_utf8(&b) {
                    Ok(methods) => {
                        for method in methods.split(',') {
                            append_allow_header(&mut this, method);
                        }
                    }
                    Err(_) => {
                        #[cfg(debug_assertions)]
                        panic!("`allow_header` contained invalid utf-8. This should never happen")
                    }
                }
                this
            }
        }
    }
```


---

### 🔹 Commit #09: `600e762b`
- **完整 Hash**: `600e762b30dba5d1b9e253fabd36d0d23333e5d5`
- **說明 (Ground Truth)**: axum-extra: prevent `?&` in TypedPath query params (#3805)
- **變更檔案數**: 1

#### 📄 檔案: `axum-extra/src/routing/typed.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:29, E:23, A:0) ➔ After(N:33, E:29, A:0)
- **差分統計**: +Nodes: 6, -Nodes: 2, +Edges: 8, -Edges: 2, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `form_urlencoded::Serializer::for_suffix (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out.find('?').map (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `with_params_question_mark_no_params` (FUNCTION_DEF)
  • + [新增節點] `out.len (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out.find('?').map(|i| i + 1).unwrap_or_else (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `out.find (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `out.contains (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `form_urlencoded::Serializer::new (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `WithQueryParams::fmt` ──[CALLS]──> `out.find('?').map(|i| i + 1).unwrap_or_else (External/Unresolved)`
  • + [新增呼叫邊] `WithQueryParams::fmt` ──[CALLS]──> `out.find('?').map (External/Unresolved)`
  • + [新增呼叫邊] `WithQueryParams::fmt` ──[CALLS]──> `out.find (External/Unresolved)`
  • + [新增呼叫邊] `WithQueryParams::fmt` ──[CALLS]──> `out.len (External/Unresolved)`
  • + [新增呼叫邊] `WithQueryParams::fmt` ──[CALLS]──> `form_urlencoded::Serializer::for_suffix (External/Unresolved)`
  • + [新增呼叫邊] `with_params_question_mark_no_params` ──[CALLS]──> `assert_eq! (Macro)`
  • + [新增呼叫邊] `with_params_question_mark_no_params` ──[CALLS]──> `with_query_params`
  • _... 以及其餘 3 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 2 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `WithQueryParams::fmt()`
- **變更前簽章 (Before)**: `fn WithQueryParams::fmt(&self, f: &mut fmt::Formatter<'_>)` (L292~L309)
- **變更後簽章 (After)**: `fn WithQueryParams::fmt(&self, f: &mut fmt::Formatter<'_>)` (L292~L311)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut out = self.path.to_string();
        if !out.contains('?') {
            out.push('?');
        }
        let mut urlencoder = form_urlencoded::Serializer::new(&mut out);
        self.params
            .serialize(serde_html_form::ser::Serializer::new(&mut urlencoder))
            .unwrap_or_else(|err| {
                panic!(
                    "failed to URL encode value of type `{}`: {err}",
                    type_name::<T>(),
                )
            });
        f.write_str(&out)?;

        Ok(())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut out = self.path.to_string();

        let params_start = out.find('?').map(|i| i + 1).unwrap_or_else(|| {
            out.push('?');
            out.len()
        });
        let mut urlencoder = form_urlencoded::Serializer::for_suffix(&mut out, params_start);
        self.params
            .serialize(serde_html_form::ser::Serializer::new(&mut urlencoder))
            .unwrap_or_else(|err| {
                panic!(
                    "failed to URL encode value of type `{}`: {err}",
                    type_name::<T>(),
                )
            });
        f.write_str(&out)?;

        Ok(())
    }
```

### 🔹 函式: `with_params_called_multiple_times()`
- **變更前簽章 (Before)**: `fn with_params_called_multiple_times()` (L422~L434)
- **變更後簽章 (After)**: `fn with_params_called_multiple_times()` (L419~L431)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn with_params_called_multiple_times() {
        let path = UsersShow { id: 1 }
            .with_query_params(Params {
                foo: "foo",
                bar: 123,
                baz: true,
            })
            .with_query_params([("qux", 1337)]);

        let uri = path.to_uri();

        assert_eq!(uri, "/users/1?&foo=foo&bar=123&baz=true&qux=1337");
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn with_params_called_multiple_times() {
        let path = UsersShow { id: 1 }
            .with_query_params(Params {
                foo: "foo",
                bar: 123,
                baz: true,
            })
            .with_query_params([("qux", 1337)]);

        let uri = path.to_uri();

        assert_eq!(uri, "/users/1?foo=foo&bar=123&baz=true&qux=1337");
    }
```

### 🔹 函式: `with_params()`
- **變更前簽章 (Before)**: `fn with_params()` (L404~L419)
- **變更後簽章 (After)**: `fn with_params()` (L406~L416)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn with_params() {
        let path = UsersShow { id: 1 }.with_query_params(Params {
            foo: "foo",
            bar: 123,
            baz: true,
        });

        let uri = path.to_uri();

        // according to [the spec] starting the params with `?&` is allowed specifically:
        //
        // > If bytes is the empty byte sequence, then continue.
        //
        // [the spec]: https://url.spec.whatwg.org/#urlencoded-parsing
        assert_eq!(uri, "/users/1?&foo=foo&bar=123&baz=true");
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn with_params() {
        let path = UsersShow { id: 1 }.with_query_params(Params {
            foo: "foo",
            bar: 123,
            baz: true,
        });

        let uri = path.to_uri();

        assert_eq!(uri, "/users/1?foo=foo&bar=123&baz=true");
    }
```


---

### 🔹 Commit #10: `6ed92103`
- **完整 Hash**: `6ed9210351633ed2c420dc051dc0a13b73744dfe`
- **說明 (Ground Truth)**: fix(axum-macros): use OptionalFromRequest for Option<T> fields (#3760)
- **變更檔案數**: 2

#### 📄 檔案: `axum-macros/src/from_request/mod.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:131, E:195, A:0) ➔ After(N:131, E:195, A:0)
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
  • + [新增節點] `fields_iter
        .enumerate()
        .map(|(index, field)| {
            let FromRequestFieldAttrs { via } = parse_attrs("from_request", &field.attrs)?;

            let member = member(field, index);
            let ty_span = field.ty.span();
            let into_inner = into_inner(via.as_ref(), ty_span);

            if peel_option(&field.ty).is_some() {
                let field_ty = into_outer(via.as_ref(), ty_span, peel_option(&field.ty).unwrap());
                let map_err = if let Some(rejection) = rejection {
                    quote! { <#rejection as ::std::convert::From<_>>::from }
                } else {
                    quote! { ::axum::response::IntoResponse::into_response }
                };

                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::OptionalFromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(|opt| opt.map(#into_inner))
                                    .map_err(#map_err)?;
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::OptionalFromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(|opt| opt.map(#into_inner))
                                .map_err(#map_err)?
                            },
                        }
                    }
                };
                Ok(tokens)
            } else if peel_result_ok(&field.ty).is_some() {
                let field_ty = into_outer(via.as_ref(), ty_span, peel_result_ok(&field.ty).unwrap());
                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(#into_inner);
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(#into_inner)
                            },
                        }
                    }
                };
                Ok(tokens)
            } else {
                let field_ty = into_outer(via.as_ref(), ty_span, &field.ty);
                let map_err = if let Some(rejection) = rejection {
                    quote! { <#rejection as ::std::convert::From<_>>::from }
                } else {
                    quote! { ::axum::response::IntoResponse::into_response }
                };

                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(#into_inner)
                                    .map_err(#map_err)?;
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(#into_inner)
                                .map_err(#map_err)?
                            },
                        }
                    }
                };
                Ok(tokens)
            }
        })
        .collect::<syn::Result<_>> (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `fields_iter
        .enumerate()
        .map(|(index, field)| {
            let FromRequestFieldAttrs { via } = parse_attrs("from_request", &field.attrs)?;

            let member = member(field, index);
            let ty_span = field.ty.span();
            let into_inner = into_inner(via.as_ref(), ty_span);

            if peel_option(&field.ty).is_some() {
                let field_ty = into_outer(via.as_ref(), ty_span, peel_option(&field.ty).unwrap());
                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .ok()
                                    .map(#into_inner);
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .ok()
                                .map(#into_inner)
                            },
                        }
                    }
                };
                Ok(tokens)
            } else if peel_result_ok(&field.ty).is_some() {
                let field_ty = into_outer(via.as_ref(), ty_span, peel_result_ok(&field.ty).unwrap());
                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(#into_inner);
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(#into_inner)
                            },
                        }
                    }
                };
                Ok(tokens)
            } else {
                let field_ty = into_outer(via.as_ref(), ty_span, &field.ty);
                let map_err = if let Some(rejection) = rejection {
                    quote! { <#rejection as ::std::convert::From<_>>::from }
                } else {
                    quote! { ::axum::response::IntoResponse::into_response }
                };

                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(#into_inner)
                                    .map_err(#map_err)?;
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(#into_inner)
                                .map_err(#map_err)?
                            },
                        }
                    }
                };
                Ok(tokens)
            }
        })
        .collect::<syn::Result<_>> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `extract_fields` ──[CALLS]──> `fields_iter
        .enumerate()
        .map(|(index, field)| {
            let FromRequestFieldAttrs { via } = parse_attrs("from_request", &field.attrs)?;

            let member = member(field, index);
            let ty_span = field.ty.span();
            let into_inner = into_inner(via.as_ref(), ty_span);

            if peel_option(&field.ty).is_some() {
                let field_ty = into_outer(via.as_ref(), ty_span, peel_option(&field.ty).unwrap());
                let map_err = if let Some(rejection) = rejection {
                    quote! { <#rejection as ::std::convert::From<_>>::from }
                } else {
                    quote! { ::axum::response::IntoResponse::into_response }
                };

                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::OptionalFromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(|opt| opt.map(#into_inner))
                                    .map_err(#map_err)?;
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::OptionalFromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(|opt| opt.map(#into_inner))
                                .map_err(#map_err)?
                            },
                        }
                    }
                };
                Ok(tokens)
            } else if peel_result_ok(&field.ty).is_some() {
                let field_ty = into_outer(via.as_ref(), ty_span, peel_result_ok(&field.ty).unwrap());
                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(#into_inner);
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(#into_inner)
                            },
                        }
                    }
                };
                Ok(tokens)
            } else {
                let field_ty = into_outer(via.as_ref(), ty_span, &field.ty);
                let map_err = if let Some(rejection) = rejection {
                    quote! { <#rejection as ::std::convert::From<_>>::from }
                } else {
                    quote! { ::axum::response::IntoResponse::into_response }
                };

                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(#into_inner)
                                    .map_err(#map_err)?;
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(#into_inner)
                                .map_err(#map_err)?
                            },
                        }
                    }
                };
                Ok(tokens)
            }
        })
        .collect::<syn::Result<_>> (External/Unresolved)`
  • - [移除呼叫邊] `extract_fields` ──[CALLS]──> `fields_iter
        .enumerate()
        .map(|(index, field)| {
            let FromRequestFieldAttrs { via } = parse_attrs("from_request", &field.attrs)?;

            let member = member(field, index);
            let ty_span = field.ty.span();
            let into_inner = into_inner(via.as_ref(), ty_span);

            if peel_option(&field.ty).is_some() {
                let field_ty = into_outer(via.as_ref(), ty_span, peel_option(&field.ty).unwrap());
                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .ok()
                                    .map(#into_inner);
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .ok()
                                .map(#into_inner)
                            },
                        }
                    }
                };
                Ok(tokens)
            } else if peel_result_ok(&field.ty).is_some() {
                let field_ty = into_outer(via.as_ref(), ty_span, peel_result_ok(&field.ty).unwrap());
                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(#into_inner);
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(#into_inner)
                            },
                        }
                    }
                };
                Ok(tokens)
            } else {
                let field_ty = into_outer(via.as_ref(), ty_span, &field.ty);
                let map_err = if let Some(rejection) = rejection {
                    quote! { <#rejection as ::std::convert::From<_>>::from }
                } else {
                    quote! { ::axum::response::IntoResponse::into_response }
                };

                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(#into_inner)
                                    .map_err(#map_err)?;
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(#into_inner)
                                .map_err(#map_err)?
                            },
                        }
                    }
                };
                Ok(tokens)
            }
        })
        .collect::<syn::Result<_>> (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `extract_fields()`
- **變更前簽章 (Before)**: `fn extract_fields(
    fields: &syn::Fields,
    rejection: Option<&syn::Path>,
    tr: Trait,
)` (L412~L639)
- **變更後簽章 (After)**: `fn extract_fields(
    fields: &syn::Fields,
    rejection: Option<&syn::Path>,
    tr: Trait,
)` (L412~L651)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn extract_fields(
    fields: &syn::Fields,
    rejection: Option<&syn::Path>,
    tr: Trait,
) -> syn::Result<Vec<TokenStream>> {
    fn member(field: &syn::Field, index: usize) -> TokenStream {
        if let Some(ident) = &field.ident {
            quote! { #ident }
        } else {
            let member = syn::Member::Unnamed(syn::Index {
                index: index as u32,
                span: field.span(),
            });
            quote! { #member }
        }
    }

    fn into_inner(via: Option<&(attr::kw::via, syn::Path)>, ty_span: Span) -> TokenStream {
        if let Some((_, path)) = via {
            let span = path.span();
            quote_spanned! {span=>
                |#path(inner)| inner
            }
        } else {
            quote_spanned! {ty_span=>
                ::std::convert::identity
            }
        }
    }

    fn into_outer(
        via: Option<&(attr::kw::via, syn::Path)>,
        ty_span: Span,
        field_ty: &Type,
    ) -> TokenStream {
        if let Some((_, path)) = via {
            let span = path.span();
            quote_spanned! {span=>
                #path<#field_ty>
            }
        } else {
            quote_spanned! {ty_span=>
                #field_ty
            }
        }
    }

    let mut fields_iter = fields.iter();

    let last = match tr {
        // Use FromRequestParts for all elements except the last
        Trait::FromRequest => fields_iter.next_back(),
        // Use FromRequestParts for all elements
        Trait::FromRequestParts => None,
    };

    let mut res: Vec<_> = fields_iter
        .enumerate()
        .map(|(index, field)| {
            let FromRequestFieldAttrs { via } = parse_attrs("from_request", &field.attrs)?;

            let member = member(field, index);
            let ty_span = field.ty.span();
            let into_inner = into_inner(via.as_ref(), ty_span);

            if peel_option(&field.ty).is_some() {
                let field_ty = into_outer(via.as_ref(), ty_span, peel_option(&field.ty).unwrap());
                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .ok()
                                    .map(#into_inner);
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .ok()
                                .map(#into_inner)
                            },
                        }
                    }
                };
                Ok(tokens)
            } else if peel_result_ok(&field.ty).is_some() {
                let field_ty = into_outer(via.as_ref(), ty_span, peel_result_ok(&field.ty).unwrap());
                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(#into_inner);
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(#into_inner)
                            },
                        }
                    }
                };
                Ok(tokens)
            } else {
                let field_ty = into_outer(via.as_ref(), ty_span, &field.ty);
                let map_err = if let Some(rejection) = rejection {
                    quote! { <#rejection as ::std::convert::From<_>>::from }
                } else {
                    quote! { ::axum::response::IntoResponse::into_response }
                };

                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(#into_inner)
                                    .map_err(#map_err)?;
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(#into_inner)
                                .map_err(#map_err)?
                            },
                        }
                    }
                };
                Ok(tokens)
            }
        })
        .collect::<syn::Result<_>>()?;

    // Handle the last element, if deriving FromRequest
    if let Some(field) = last {
        let FromRequestFieldAttrs { via } = parse_attrs("from_request", &field.attrs)?;

        let member = member(field, fields.len() - 1);
        let ty_span = field.ty.span();
        let into_inner = into_inner(via.as_ref(), ty_span);

        let item = if peel_option(&field.ty).is_some() {
            let field_ty = into_outer(via.as_ref(), ty_span, peel_option(&field.ty).unwrap());
            quote_spanned! {ty_span=>
                #member: {
                    <#field_ty as ::axum::extract::FromRequest<_, _>>::from_request(req, state)
                        .await
                        .ok()
                        .map(#into_inner)
                },
            }
        } else if peel_result_ok(&field.ty).is_some() {
            let field_ty = into_outer(via.as_ref(), ty_span, peel_result_ok(&field.ty).unwrap());
            quote_spanned! {ty_span=>
                #member: {
                    <#field_ty as ::axum::extract::FromRequest<_, _>>::from_request(req, state)
                        .await
                        .map(#into_inner)
                },
            }
        } else {
            let field_ty = into_outer(via.as_ref(), ty_span, &field.ty);
            let map_err = if let Some(rejection) = rejection {
                quote! { <#rejection as ::std::convert::From<_>>::from }
            } else {
                quote! { ::axum::response::IntoResponse::into_response }
            };

            quote_spanned! {ty_span=>
                #member: {
                    <#field_ty as ::axum::extract::FromRequest<_, _>>::from_request(req, state)
                        .await
                        .map(#into_inner)
                        .map_err(#map_err)?
                },
            }
        };

        res.push(item);
    }

    Ok(res)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn extract_fields(
    fields: &syn::Fields,
    rejection: Option<&syn::Path>,
    tr: Trait,
) -> syn::Result<Vec<TokenStream>> {
    fn member(field: &syn::Field, index: usize) -> TokenStream {
        if let Some(ident) = &field.ident {
            quote! { #ident }
        } else {
            let member = syn::Member::Unnamed(syn::Index {
                index: index as u32,
                span: field.span(),
            });
            quote! { #member }
        }
    }

    fn into_inner(via: Option<&(attr::kw::via, syn::Path)>, ty_span: Span) -> TokenStream {
        if let Some((_, path)) = via {
            let span = path.span();
            quote_spanned! {span=>
                |#path(inner)| inner
            }
        } else {
            quote_spanned! {ty_span=>
                ::std::convert::identity
            }
        }
    }

    fn into_outer(
        via: Option<&(attr::kw::via, syn::Path)>,
        ty_span: Span,
        field_ty: &Type,
    ) -> TokenStream {
        if let Some((_, path)) = via {
            let span = path.span();
            quote_spanned! {span=>
                #path<#field_ty>
            }
        } else {
            quote_spanned! {ty_span=>
                #field_ty
            }
        }
    }

    let mut fields_iter = fields.iter();

    let last = match tr {
        // Use FromRequestParts for all elements except the last
        Trait::FromRequest => fields_iter.next_back(),
        // Use FromRequestParts for all elements
        Trait::FromRequestParts => None,
    };

    let mut res: Vec<_> = fields_iter
        .enumerate()
        .map(|(index, field)| {
            let FromRequestFieldAttrs { via } = parse_attrs("from_request", &field.attrs)?;

            let member = member(field, index);
            let ty_span = field.ty.span();
            let into_inner = into_inner(via.as_ref(), ty_span);

            if peel_option(&field.ty).is_some() {
                let field_ty = into_outer(via.as_ref(), ty_span, peel_option(&field.ty).unwrap());
                let map_err = if let Some(rejection) = rejection {
                    quote! { <#rejection as ::std::convert::From<_>>::from }
                } else {
                    quote! { ::axum::response::IntoResponse::into_response }
                };

                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::OptionalFromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(|opt| opt.map(#into_inner))
                                    .map_err(#map_err)?;
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::OptionalFromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(|opt| opt.map(#into_inner))
                                .map_err(#map_err)?
                            },
                        }
                    }
                };
                Ok(tokens)
            } else if peel_result_ok(&field.ty).is_some() {
                let field_ty = into_outer(via.as_ref(), ty_span, peel_result_ok(&field.ty).unwrap());
                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(#into_inner);
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(#into_inner)
                            },
                        }
                    }
                };
                Ok(tokens)
            } else {
                let field_ty = into_outer(via.as_ref(), ty_span, &field.ty);
                let map_err = if let Some(rejection) = rejection {
                    quote! { <#rejection as ::std::convert::From<_>>::from }
                } else {
                    quote! { ::axum::response::IntoResponse::into_response }
                };

                let tokens = match tr {
                    Trait::FromRequest => {
                        quote_spanned! {ty_span=>
                            #member: {
                                let (mut parts, body) = req.into_parts();
                                let value =
                                    <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                        &mut parts,
                                        state,
                                    )
                                    .await
                                    .map(#into_inner)
                                    .map_err(#map_err)?;
                                req = ::axum::http::Request::from_parts(parts, body);
                                value
                            },
                        }
                    }
                    Trait::FromRequestParts => {
                        quote_spanned! {ty_span=>
                            #member: {
                                <#field_ty as ::axum::extract::FromRequestParts<_>>::from_request_parts(
                                    parts,
                                    state,
                                )
                                .await
                                .map(#into_inner)
                                .map_err(#map_err)?
                            },
                        }
                    }
                };
                Ok(tokens)
            }
        })
        .collect::<syn::Result<_>>()?;

    // Handle the last element, if deriving FromRequest
    if let Some(field) = last {
        let FromRequestFieldAttrs { via } = parse_attrs("from_request", &field.attrs)?;

        let member = member(field, fields.len() - 1);
        let ty_span = field.ty.span();
        let into_inner = into_inner(via.as_ref(), ty_span);

        let item = if peel_option(&field.ty).is_some() {
            let field_ty = into_outer(via.as_ref(), ty_span, peel_option(&field.ty).unwrap());
            let map_err = if let Some(rejection) = rejection {
                quote! { <#rejection as ::std::convert::From<_>>::from }
            } else {
                quote! { ::axum::response::IntoResponse::into_response }
            };

            quote_spanned! {ty_span=>
                #member: {
                    <#field_ty as ::axum::extract::OptionalFromRequest<_, _>>::from_request(req, state)
                        .await
                        .map(|opt| opt.map(#into_inner))
                        .map_err(#map_err)?
                },
            }
        } else if peel_result_ok(&field.ty).is_some() {
            let field_ty = into_outer(via.as_ref(), ty_span, peel_result_ok(&field.ty).unwrap());
            quote_spanned! {ty_span=>
                #member: {
                    <#field_ty as ::axum::extract::FromRequest<_, _>>::from_request(req, state)
                        .await
                        .map(#into_inner)
                },
            }
        } else {
            let field_ty = into_outer(via.as_ref(), ty_span, &field.ty);
            let map_err = if let Some(rejection) = rejection {
                quote! { <#rejection as ::std::convert::From<_>>::from }
            } else {
                quote! { ::axum::response::IntoResponse::into_response }
            };

            quote_spanned! {ty_span=>
                #member: {
                    <#field_ty as ::axum::extract::FromRequest<_, _>>::from_request(req, state)
                        .await
                        .map(#into_inner)
                        .map_err(#map_err)?
                },
            }
        };

        res.push(item);
    }

    Ok(res)
}
```


#### 📄 檔案: `axum-macros/src/lib.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:44, E:46, A:0) ➔ After(N:44, E:46, A:0)
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

---

### 🔹 Commit #11: `ec4f5bbf`
- **完整 Hash**: `ec4f5bbf9ee70a8eac941da2e6c2ba87abad16f7`
- **說明 (Ground Truth)**: fix: Return specific error message when multipart body limit is exceeded (#3611)
- **變更檔案數**: 2

#### 📄 檔案: `axum-extra/src/extract/multipart.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:87, E:114, A:0) ➔ After(N:93, E:124, A:0)
- **差分統計**: +Nodes: 6, -Nodes: 0, +Edges: 10, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `err.downcast_ref::<axum_core::Error>()
                .and_then(|err| err.source())
                .and_then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `err.downcast_ref::<axum_core::Error> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `err.downcast_ref::<axum_core::Error>()
                .and_then(|err| err.source())
                .and_then(|err| err.downcast_ref::<http_body_util::LengthLimitError>())
                .is_some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `err.downcast_ref::<axum_core::Error>()
                .and_then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `"Request payload is too large".to_owned (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `is_body_limit_error` (FUNCTION_DEF)
  • + [新增呼叫邊] `MultipartError::body_text` ──[CALLS]──> `is_body_limit_error`
  • + [新增呼叫邊] `MultipartError::body_text` ──[CALLS]──> `"Request payload is too large".to_owned (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<multer::Error> (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `is_body_limit_error`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<axum_core::Error>()
                .and_then(|err| err.source())
                .and_then(|err| err.downcast_ref::<http_body_util::LengthLimitError>())
                .is_some (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<axum_core::Error>()
                .and_then(|err| err.source())
                .and_then (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<axum_core::Error>()
                .and_then (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<axum_core::Error> (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `MultipartError::source`
  • _... 以及其餘 1 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `MultipartError::body_text()`
- **變更前簽章 (Before)**: `fn MultipartError::body_text(&self)` (L249~L257)
- **變更後簽章 (After)**: `fn MultipartError::body_text(&self)` (L249~L261)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn body_text(&self) -> String {
        let body = self.source.to_string();
        axum_core::__log_rejection!(
            rejection_type = Self,
            body_text = body,
            status = self.status(),
        );
        body
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn body_text(&self) -> String {
        let body = if is_body_limit_error(&self.source) {
            "Request payload is too large".to_owned()
        } else {
            self.source.to_string()
        };
        axum_core::__log_rejection!(
            rejection_type = Self,
            body_text = body,
            status = self.status(),
        );
        body
    }
```

### 🔹 函式: `body_too_large()`
- **變更前簽章 (Before)**: `fn body_too_large()` (L385~L406)
- **變更後簽章 (After)**: `fn body_too_large()` (L405~L427)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async fn body_too_large() {
        const BYTES: &[u8] = "<!doctype html><title>🦀</title>".as_bytes();

        async fn handle(mut multipart: Multipart) -> Result<(), MultipartError> {
            while let Some(field) = multipart.next_field().await? {
                field.bytes().await?;
            }
            Ok(())
        }

        let app = Router::new()
            .route("/", post(handle))
            .layer(DefaultBodyLimit::max(BYTES.len() - 1));

        let client = TestClient::new(app);

        let form =
            reqwest::multipart::Form::new().part("file", reqwest::multipart::Part::bytes(BYTES));

        let res = client.post("/").multipart(form).await;
        assert_eq!(res.status(), StatusCode::PAYLOAD_TOO_LARGE);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async fn body_too_large() {
        const BYTES: &[u8] = "<!doctype html><title>🦀</title>".as_bytes();

        async fn handle(mut multipart: Multipart) -> Result<(), MultipartError> {
            while let Some(field) = multipart.next_field().await? {
                field.bytes().await?;
            }
            Ok(())
        }

        let app = Router::new()
            .route("/", post(handle))
            .layer(DefaultBodyLimit::max(BYTES.len() - 1));

        let client = TestClient::new(app);

        let form =
            reqwest::multipart::Form::new().part("file", reqwest::multipart::Part::bytes(BYTES));

        let res = client.post("/").multipart(form).await;
        assert_eq!(res.status(), StatusCode::PAYLOAD_TOO_LARGE);
        assert_eq!(res.text().await, "Request payload is too large");
    }
```


#### 📄 檔案: `axum/src/extract/multipart.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:88, E:118, A:0) ➔ After(N:94, E:128, A:0)
- **差分統計**: +Nodes: 6, -Nodes: 0, +Edges: 10, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `err.downcast_ref::<crate::Error>()
                .and_then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `err.downcast_ref::<crate::Error> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `err.downcast_ref::<crate::Error>()
                .and_then(|err| err.source())
                .and_then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `err.downcast_ref::<crate::Error>()
                .and_then(|err| err.source())
                .and_then(|err| err.downcast_ref::<http_body_util::LengthLimitError>())
                .is_some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `"Request payload is too large".to_owned (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `is_body_limit_error` (FUNCTION_DEF)
  • + [新增呼叫邊] `MultipartError::body_text` ──[CALLS]──> `is_body_limit_error`
  • + [新增呼叫邊] `MultipartError::body_text` ──[CALLS]──> `"Request payload is too large".to_owned (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<multer::Error> (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `is_body_limit_error`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<crate::Error>()
                .and_then(|err| err.source())
                .and_then(|err| err.downcast_ref::<http_body_util::LengthLimitError>())
                .is_some (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<crate::Error>()
                .and_then(|err| err.source())
                .and_then (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<crate::Error>()
                .and_then (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<crate::Error> (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `MultipartError::source`
  • _... 以及其餘 1 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `MultipartError::body_text()`
- **變更前簽章 (Before)**: `fn MultipartError::body_text(&self)` (L246~L248)
- **變更後簽章 (After)**: `fn MultipartError::body_text(&self)` (L246~L252)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn body_text(&self) -> String {
        self.source.to_string()
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn body_text(&self) -> String {
        if is_body_limit_error(&self.source) {
            "Request payload is too large".to_owned()
        } else {
            self.source.to_string()
        }
    }
```

### 🔹 函式: `body_too_large()`
- **變更前簽章 (Before)**: `fn body_too_large()` (L389~L410)
- **變更後簽章 (After)**: `fn body_too_large()` (L409~L431)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async fn body_too_large() {
        const BYTES: &[u8] = "<!doctype html><title>🦀</title>".as_bytes();

        async fn handle(mut multipart: Multipart) -> Result<(), MultipartError> {
            while let Some(field) = multipart.next_field().await? {
                field.bytes().await?;
            }
            Ok(())
        }

        let app = Router::new()
            .route("/", post(handle))
            .layer(DefaultBodyLimit::max(BYTES.len() - 1));

        let client = TestClient::new(app);

        let form =
            reqwest::multipart::Form::new().part("file", reqwest::multipart::Part::bytes(BYTES));

        let res = client.post("/").multipart(form).await;
        assert_eq!(res.status(), StatusCode::PAYLOAD_TOO_LARGE);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async fn body_too_large() {
        const BYTES: &[u8] = "<!doctype html><title>🦀</title>".as_bytes();

        async fn handle(mut multipart: Multipart) -> Result<(), MultipartError> {
            while let Some(field) = multipart.next_field().await? {
                field.bytes().await?;
            }
            Ok(())
        }

        let app = Router::new()
            .route("/", post(handle))
            .layer(DefaultBodyLimit::max(BYTES.len() - 1));

        let client = TestClient::new(app);

        let form =
            reqwest::multipart::Form::new().part("file", reqwest::multipart::Part::bytes(BYTES));

        let res = client.post("/").multipart(form).await;
        assert_eq!(res.status(), StatusCode::PAYLOAD_TOO_LARGE);
        assert_eq!(res.text().await, "Request payload is too large");
    }
```


---

### 🔹 Commit #12: `4fa5d80a`
- **完整 Hash**: `4fa5d80ab7fc17d880d19293e8838bd7e4255877`
- **說明 (Ground Truth)**: fix(axum-extra): escape filename in Content-Disposition header (#3664)
- **變更檔案數**: 4

#### 📄 檔案: `axum-extra/src/response/attachment.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:15, E:16, A:0) ➔ After(N:22, E:42, A:0)
- **差分統計**: +Nodes: 13, -Nodes: 6, +Edges: 32, -Edges: 6, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `filename
                .to_str()
                .expect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `HeaderValue::try_from(value).expect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert_eq! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `attachment_without_filename` (FUNCTION_DEF)
  • + [新增節點] `attachment_with_normal_filename` (FUNCTION_DEF)
  • + [新增節點] `format! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `attachment_filename_escapes_quotes` (FUNCTION_DEF)
  • + [新增節點] `HeaderValue::try_from (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `attachment_filename_escapes_backslashes` (FUNCTION_DEF)
  • + [新增節點] `attachment.headers().get (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `attachment.headers().get(CONTENT_DISPOSITION).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `filename
                .to_str (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `attachment.headers (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `bytes.push (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `b"attachment; filename=\"".to_vec (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 42 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Attachment::into_response()`
- **變更前簽章 (Before)**: `fn Attachment::into_response(self)` (L82~L102)
- **變更後簽章 (After)**: `fn Attachment::into_response(self)` (L83~L103)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn into_response(self) -> axum_core::response::Response {
        let mut headers = HeaderMap::new();

        if let Some(content_type) = self.content_type {
            headers.append(header::CONTENT_TYPE, content_type);
        }

        let content_disposition = if let Some(filename) = self.filename {
            let mut bytes = b"attachment; filename=\"".to_vec();
            bytes.extend_from_slice(filename.as_bytes());
            bytes.push(b'\"');

            HeaderValue::from_bytes(&bytes).expect("This was a HeaderValue so this can not fail")
        } else {
            HeaderValue::from_static("attachment")
        };

        headers.append(header::CONTENT_DISPOSITION, content_disposition);

        (headers, self.inner).into_response()
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn into_response(self) -> axum_core::response::Response {
        let mut headers = HeaderMap::new();

        if let Some(content_type) = self.content_type {
            headers.append(header::CONTENT_TYPE, content_type);
        }

        let content_disposition = if let Some(filename) = self.filename {
            let filename_str = filename
                .to_str()
                .expect("This was a HeaderValue so this can not fail");
            let value = format!("attachment; filename=\"{}\"", EscapedFilename(filename_str));
            HeaderValue::try_from(value).expect("This was a HeaderValue so this can not fail")
        } else {
            HeaderValue::from_static("attachment")
        };

        headers.append(header::CONTENT_DISPOSITION, content_disposition);

        (headers, self.inner).into_response()
    }
```


#### 📄 檔案: `axum-extra/src/response/content_disposition.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:8, E:6, A:0)
- **差分統計**: +Nodes: 8, -Nodes: 0, +Edges: 6, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `escapes_backslashes` (FUNCTION_DEF)
  • + [新增節點] `self.0.chars (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `no_special_characters` (FUNCTION_DEF)
  • + [新增節點] `Ok (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `EscapedFilename::fmt` (FUNCTION_DEF)
  • + [新增節點] `assert_eq! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `escapes_double_quotes` (FUNCTION_DEF)
  • + [新增節點] `f.write_char (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `EscapedFilename::fmt` ──[CALLS]──> `self.0.chars (External/Unresolved)`
  • + [新增呼叫邊] `EscapedFilename::fmt` ──[CALLS]──> `f.write_char (External/Unresolved)`
  • + [新增呼叫邊] `EscapedFilename::fmt` ──[CALLS]──> `Ok (External/Unresolved)`
  • + [新增呼叫邊] `no_special_characters` ──[CALLS]──> `assert_eq! (Macro)`
  • + [新增呼叫邊] `escapes_double_quotes` ──[CALLS]──> `assert_eq! (Macro)`
  • + [新增呼叫邊] `escapes_backslashes` ──[CALLS]──> `assert_eq! (Macro)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `axum-extra/src/response/file_stream.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:88, E:190, A:0) ➔ After(N:91, E:216, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 26, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `filename_escapes_backslashes` (FUNCTION_DEF)
  • + [新增節點] `filename_escapes_quotes` (FUNCTION_DEF)
  • + [新增節點] `b"data".to_vec (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `filename_escapes_quotes` ──[CALLS]──> `Router::new().route (External/Unresolved)`
  • + [新增呼叫邊] `filename_escapes_quotes` ──[CALLS]──> `FileStream::new`
  • + [新增呼叫邊] `filename_escapes_quotes` ──[CALLS]──> `get (External/Unresolved)`
  • + [新增呼叫邊] `filename_escapes_quotes` ──[CALLS]──> `b"data".to_vec (External/Unresolved)`
  • + [新增呼叫邊] `filename_escapes_quotes` ──[CALLS]──> `FileStream::into_response`
  • + [新增呼叫邊] `filename_escapes_quotes` ──[CALLS]──> `FileStream::file_name`
  • + [新增呼叫邊] `filename_escapes_quotes` ──[CALLS]──> `app
            .oneshot (External/Unresolved)`
  • + [新增呼叫邊] `filename_escapes_quotes` ──[CALLS]──> `Request::builder().uri("/file").body (External/Unresolved)`
  • + [新增呼叫邊] `filename_escapes_quotes` ──[CALLS]──> `Request::builder().uri (External/Unresolved)`
  • + [新增呼叫邊] `filename_escapes_quotes` ──[CALLS]──> `Request::builder (External/Unresolved)`
  • + [新增呼叫邊] `filename_escapes_quotes` ──[CALLS]──> `Body::empty (External/Unresolved)`
  • + [新增呼叫邊] `filename_escapes_quotes` ──[CALLS]──> `assert_eq! (Macro)`
  • _... 以及其餘 14 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FileStream::into_response()`
- **變更前簽章 (Before)**: `fn FileStream::into_response(self)` (L273~L295)
- **變更後簽章 (After)**: `fn FileStream::into_response(self)` (L273~L298)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn into_response(self) -> Response {
        let mut resp = Response::builder().header(header::CONTENT_TYPE, "application/octet-stream");

        if let Some(file_name) = self.file_name {
            resp = resp.header(
                header::CONTENT_DISPOSITION,
                format!("attachment; filename=\"{file_name}\""),
            );
        }

        if let Some(content_size) = self.content_size {
            resp = resp.header(header::CONTENT_LENGTH, content_size);
        }

        resp.body(body::Body::from_stream(self.stream))
            .unwrap_or_else(|e| {
                (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    format!("build FileStream responsec error: {e}"),
                )
                    .into_response()
            })
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn into_response(self) -> Response {
        let mut resp = Response::builder().header(header::CONTENT_TYPE, "application/octet-stream");

        if let Some(file_name) = self.file_name {
            resp = resp.header(
                header::CONTENT_DISPOSITION,
                format!(
                    "attachment; filename=\"{}\"",
                    super::content_disposition::EscapedFilename(&file_name)
                ),
            );
        }

        if let Some(content_size) = self.content_size {
            resp = resp.header(header::CONTENT_LENGTH, content_size);
        }

        resp.body(body::Body::from_stream(self.stream))
            .unwrap_or_else(|e| {
                (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    format!("build FileStream responsec error: {e}"),
                )
                    .into_response()
            })
    }
```


#### 📄 檔案: `axum-extra/src/response/mod.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:0, E:0, A:0)
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

### 🔹 Commit #13: `880cc381`
- **完整 Hash**: `880cc381745cbc4b9175a5e19e84899038c50e38`
- **說明 (Ground Truth)**: fix: silence `clippy::implicit_clone` in `TypedPath` macro expansions (#3663)
- **變更檔案數**: 1

#### 📄 檔案: `axum-macros/src/typed_path.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:74, E:108, A:0) ➔ After(N:74, E:108, A:0)
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

### 🔹 函式: `expand_named_fields()`
- **變更前簽章 (Before)**: `fn expand_named_fields(
    ident: &syn::Ident,
    path: LitStr,
    segments: &[Segment],
    rejection: Option<syn::Path>,
)` (L96~L161)
- **變更後簽章 (After)**: `fn expand_named_fields(
    ident: &syn::Ident,
    path: LitStr,
    segments: &[Segment],
    rejection: Option<syn::Path>,
)` (L96~L162)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn expand_named_fields(
    ident: &syn::Ident,
    path: LitStr,
    segments: &[Segment],
    rejection: Option<syn::Path>,
) -> TokenStream {
    let format_str = format_str_from_path(segments);
    let captures = captures_from_path(segments);

    let typed_path_impl = quote_spanned! {path.span()=>
        #[automatically_derived]
        impl ::axum_extra::routing::TypedPath for #ident {
            const PATH: &'static str = #path;
        }
    };

    let display_impl = quote_spanned! {path.span()=>
        #[automatically_derived]
        impl ::std::fmt::Display for #ident {
            #[allow(clippy::unnecessary_to_owned)]
            fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                let Self { #(#captures,)* } = self;
                write!(
                    f,
                    #format_str,
                    #(
                        #captures = ::axum_extra::__private::utf8_percent_encode(
                            &#captures.to_string(),
                            ::axum_extra::__private::PATH_SEGMENT,
                        )
                    ),*
                )
            }
        }
    };

    let rejection_assoc_type = rejection_assoc_type(&rejection);
    let map_err_rejection = map_err_rejection(&rejection);

    let from_request_impl = quote! {
        #[automatically_derived]
        impl<S> ::axum::extract::FromRequestParts<S> for #ident
        where
            S: Send + Sync,
        {
            type Rejection = #rejection_assoc_type;

            async fn from_request_parts(
                parts: &mut ::axum::http::request::Parts,
                state: &S,
            ) -> ::std::result::Result<Self, Self::Rejection> {
                <::axum::extract::Path<#ident> as ::axum::extract::FromRequestParts<S>>
                    ::from_request_parts(parts, state)
                    .await
                    .map(|path| path.0)
                    #map_err_rejection
            }
        }
    };

    quote! {
        #typed_path_impl
        #display_impl
        #from_request_impl
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn expand_named_fields(
    ident: &syn::Ident,
    path: LitStr,
    segments: &[Segment],
    rejection: Option<syn::Path>,
) -> TokenStream {
    let format_str = format_str_from_path(segments);
    let captures = captures_from_path(segments);

    let typed_path_impl = quote_spanned! {path.span()=>
        #[automatically_derived]
        impl ::axum_extra::routing::TypedPath for #ident {
            const PATH: &'static str = #path;
        }
    };

    let display_impl = quote_spanned! {path.span()=>
        #[automatically_derived]
        impl ::std::fmt::Display for #ident {
            #[allow(clippy::unnecessary_to_owned)]
            #[allow(clippy::implicit_clone)]
            fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                let Self { #(#captures,)* } = self;
                write!(
                    f,
                    #format_str,
                    #(
                        #captures = ::axum_extra::__private::utf8_percent_encode(
                            &#captures.to_string(),
                            ::axum_extra::__private::PATH_SEGMENT,
                        )
                    ),*
                )
            }
        }
    };

    let rejection_assoc_type = rejection_assoc_type(&rejection);
    let map_err_rejection = map_err_rejection(&rejection);

    let from_request_impl = quote! {
        #[automatically_derived]
        impl<S> ::axum::extract::FromRequestParts<S> for #ident
        where
            S: Send + Sync,
        {
            type Rejection = #rejection_assoc_type;

            async fn from_request_parts(
                parts: &mut ::axum::http::request::Parts,
                state: &S,
            ) -> ::std::result::Result<Self, Self::Rejection> {
                <::axum::extract::Path<#ident> as ::axum::extract::FromRequestParts<S>>
                    ::from_request_parts(parts, state)
                    .await
                    .map(|path| path.0)
                    #map_err_rejection
            }
        }
    };

    quote! {
        #typed_path_impl
        #display_impl
        #from_request_impl
    }
}
```

### 🔹 函式: `expand_unnamed_fields()`
- **變更前簽章 (Before)**: `fn expand_unnamed_fields(
    fields: &syn::FieldsUnnamed,
    ident: &syn::Ident,
    path: LitStr,
    segments: &[Segment],
    rejection: Option<syn::Path>,
)` (L163~L265)
- **變更後簽章 (After)**: `fn expand_unnamed_fields(
    fields: &syn::FieldsUnnamed,
    ident: &syn::Ident,
    path: LitStr,
    segments: &[Segment],
    rejection: Option<syn::Path>,
)` (L164~L267)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn expand_unnamed_fields(
    fields: &syn::FieldsUnnamed,
    ident: &syn::Ident,
    path: LitStr,
    segments: &[Segment],
    rejection: Option<syn::Path>,
) -> syn::Result<TokenStream> {
    let num_captures = segments
        .iter()
        .filter(|segment| match segment {
            Segment::Capture(_, _) => true,
            Segment::Static(_) => false,
        })
        .count();
    let num_fields = fields.unnamed.len();
    if num_fields != num_captures {
        return Err(syn::Error::new_spanned(
            fields,
            format!(
                "Mismatch in number of captures and fields. Path has {} but struct has {}",
                simple_pluralize(num_captures, "capture"),
                simple_pluralize(num_fields, "field"),
            ),
        ));
    }

    let destructure_self = segments
        .iter()
        .filter_map(|segment| match segment {
            Segment::Capture(capture, _) => Some(capture),
            Segment::Static(_) => None,
        })
        .enumerate()
        .map(|(idx, capture)| {
            let idx = syn::Index {
                index: idx as _,
                span: Span::call_site(),
            };
            let capture = format_ident!("{}", capture, span = path.span());
            quote_spanned! {path.span()=>
                #idx: #capture,
            }
        });

    let format_str = format_str_from_path(segments);
    let captures = captures_from_path(segments);

    let typed_path_impl = quote_spanned! {path.span()=>
        #[automatically_derived]
        impl ::axum_extra::routing::TypedPath for #ident {
            const PATH: &'static str = #path;
        }
    };

    let display_impl = quote_spanned! {path.span()=>
        #[automatically_derived]
        impl ::std::fmt::Display for #ident {
            #[allow(clippy::unnecessary_to_owned)]
            fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                let Self { #(#destructure_self)* } = self;
                write!(
                    f,
                    #format_str,
                    #(
                        #captures = ::axum_extra::__private::utf8_percent_encode(
                            &#captures.to_string(),
                            ::axum_extra::__private::PATH_SEGMENT,
                        )
                    ),*
                )
            }
        }
    };

    let rejection_assoc_type = rejection_assoc_type(&rejection);
    let map_err_rejection = map_err_rejection(&rejection);

    let from_request_impl = quote! {
        #[automatically_derived]
        impl<S> ::axum::extract::FromRequestParts<S> for #ident
        where
            S: Send + Sync,
        {
            type Rejection = #rejection_assoc_type;

            async fn from_request_parts(
                parts: &mut ::axum::http::request::Parts,
                state: &S,
            ) -> ::std::result::Result<Self, Self::Rejection> {
                ::axum::extract::Path::from_request_parts(parts, state)
                    .await
                    .map(|path| path.0)
                    #map_err_rejection
            }
        }
    };

    Ok(quote! {
        #typed_path_impl
        #display_impl
        #from_request_impl
    })
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn expand_unnamed_fields(
    fields: &syn::FieldsUnnamed,
    ident: &syn::Ident,
    path: LitStr,
    segments: &[Segment],
    rejection: Option<syn::Path>,
) -> syn::Result<TokenStream> {
    let num_captures = segments
        .iter()
        .filter(|segment| match segment {
            Segment::Capture(_, _) => true,
            Segment::Static(_) => false,
        })
        .count();
    let num_fields = fields.unnamed.len();
    if num_fields != num_captures {
        return Err(syn::Error::new_spanned(
            fields,
            format!(
                "Mismatch in number of captures and fields. Path has {} but struct has {}",
                simple_pluralize(num_captures, "capture"),
                simple_pluralize(num_fields, "field"),
            ),
        ));
    }

    let destructure_self = segments
        .iter()
        .filter_map(|segment| match segment {
            Segment::Capture(capture, _) => Some(capture),
            Segment::Static(_) => None,
        })
        .enumerate()
        .map(|(idx, capture)| {
            let idx = syn::Index {
                index: idx as _,
                span: Span::call_site(),
            };
            let capture = format_ident!("{}", capture, span = path.span());
            quote_spanned! {path.span()=>
                #idx: #capture,
            }
        });

    let format_str = format_str_from_path(segments);
    let captures = captures_from_path(segments);

    let typed_path_impl = quote_spanned! {path.span()=>
        #[automatically_derived]
        impl ::axum_extra::routing::TypedPath for #ident {
            const PATH: &'static str = #path;
        }
    };

    let display_impl = quote_spanned! {path.span()=>
        #[automatically_derived]
        impl ::std::fmt::Display for #ident {
            #[allow(clippy::unnecessary_to_owned)]
            #[allow(clippy::implicit_clone)]
            fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                let Self { #(#destructure_self)* } = self;
                write!(
                    f,
                    #format_str,
                    #(
                        #captures = ::axum_extra::__private::utf8_percent_encode(
                            &#captures.to_string(),
                            ::axum_extra::__private::PATH_SEGMENT,
                        )
                    ),*
                )
            }
        }
    };

    let rejection_assoc_type = rejection_assoc_type(&rejection);
    let map_err_rejection = map_err_rejection(&rejection);

    let from_request_impl = quote! {
        #[automatically_derived]
        impl<S> ::axum::extract::FromRequestParts<S> for #ident
        where
            S: Send + Sync,
        {
            type Rejection = #rejection_assoc_type;

            async fn from_request_parts(
                parts: &mut ::axum::http::request::Parts,
                state: &S,
            ) -> ::std::result::Result<Self, Self::Rejection> {
                ::axum::extract::Path::from_request_parts(parts, state)
                    .await
                    .map(|path| path.0)
                    #map_err_rejection
            }
        }
    };

    Ok(quote! {
        #typed_path_impl
        #display_impl
        #from_request_impl
    })
}
```


---

### 🔹 Commit #14: `27f40159`
- **完整 Hash**: `27f40159865f7fd485655a3e663d4bcb491df2d1`
- **說明 (Ground Truth)**: fix: Set connect endpoint on correct field in MethodRouter (#3656)
- **變更檔案數**: 1

#### 📄 檔案: `axum/src/routing/method_routing.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:172, E:261, A:0) ➔ After(N:173, E:262, A:0)
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
  • + [新增節點] `connect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `merge` ──[CALLS]──> `connect (External/Unresolved)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `merge()`
- **變更前簽章 (Before)**: `fn merge()` (L1402~L1410)
- **變更後簽章 (After)**: `fn merge()` (L1402~L1413)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async fn merge() {
        let mut svc = get(ok).merge(post(ok));

        let (status, _, _) = call(Method::GET, &mut svc).await;
        assert_eq!(status, StatusCode::OK);

        let (status, _, _) = call(Method::POST, &mut svc).await;
        assert_eq!(status, StatusCode::OK);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async fn merge() {
        let mut svc = get(ok).merge(post(ok)).merge(connect(ok));

        let (status, _, _) = call(Method::GET, &mut svc).await;
        assert_eq!(status, StatusCode::OK);

        let (status, _, _) = call(Method::POST, &mut svc).await;
        assert_eq!(status, StatusCode::OK);

        let (status, _, _) = call(Method::CONNECT, &mut svc).await;
        assert_eq!(status, StatusCode::OK);
    }
```

### 🔹 函式: `MethodRouter::on_endpoint()`
- **變更前簽章 (Before)**: `fn MethodRouter::on_endpoint(mut self, filter: MethodFilter, endpoint: MethodEndpoint<S, E>)` (L823~L943)
- **變更後簽章 (After)**: `fn MethodRouter::on_endpoint(mut self, filter: MethodFilter, endpoint: MethodEndpoint<S, E>)` (L823~L943)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn on_endpoint(mut self, filter: MethodFilter, endpoint: MethodEndpoint<S, E>) -> Self {
        // written as a separate function to generate less IR
        #[track_caller]
        fn set_endpoint<S, E>(
            method_name: &str,
            out: &mut MethodEndpoint<S, E>,
            endpoint: &MethodEndpoint<S, E>,
            endpoint_filter: MethodFilter,
            filter: MethodFilter,
            allow_header: &mut AllowHeader,
            methods: &[&'static str],
        ) where
            MethodEndpoint<S, E>: Clone,
            S: Clone,
        {
            if endpoint_filter.contains(filter) {
                if out.is_some() {
                    panic!(
                        "Overlapping method route. Cannot add two method routes that both handle \
                         `{method_name}`",
                    )
                }
                *out = endpoint.clone();
                for method in methods {
                    append_allow_header(allow_header, method);
                }
            }
        }

        set_endpoint(
            "GET",
            &mut self.get,
            &endpoint,
            filter,
            MethodFilter::GET,
            &mut self.allow_header,
            &["GET", "HEAD"],
        );

        set_endpoint(
            "HEAD",
            &mut self.head,
            &endpoint,
            filter,
            MethodFilter::HEAD,
            &mut self.allow_header,
            &["HEAD"],
        );

        set_endpoint(
            "TRACE",
            &mut self.trace,
            &endpoint,
            filter,
            MethodFilter::TRACE,
            &mut self.allow_header,
            &["TRACE"],
        );

        set_endpoint(
            "PUT",
            &mut self.put,
            &endpoint,
            filter,
            MethodFilter::PUT,
            &mut self.allow_header,
            &["PUT"],
        );

        set_endpoint(
            "POST",
            &mut self.post,
            &endpoint,
            filter,
            MethodFilter::POST,
            &mut self.allow_header,
            &["POST"],
        );

        set_endpoint(
            "PATCH",
            &mut self.patch,
            &endpoint,
            filter,
            MethodFilter::PATCH,
            &mut self.allow_header,
            &["PATCH"],
        );

        set_endpoint(
            "OPTIONS",
            &mut self.options,
            &endpoint,
            filter,
            MethodFilter::OPTIONS,
            &mut self.allow_header,
            &["OPTIONS"],
        );

        set_endpoint(
            "DELETE",
            &mut self.delete,
            &endpoint,
            filter,
            MethodFilter::DELETE,
            &mut self.allow_header,
            &["DELETE"],
        );

        set_endpoint(
            "CONNECT",
            &mut self.options,
            &endpoint,
            filter,
            MethodFilter::CONNECT,
            &mut self.allow_header,
            &["CONNECT"],
        );

        self
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn on_endpoint(mut self, filter: MethodFilter, endpoint: MethodEndpoint<S, E>) -> Self {
        // written as a separate function to generate less IR
        #[track_caller]
        fn set_endpoint<S, E>(
            method_name: &str,
            out: &mut MethodEndpoint<S, E>,
            endpoint: &MethodEndpoint<S, E>,
            endpoint_filter: MethodFilter,
            filter: MethodFilter,
            allow_header: &mut AllowHeader,
            methods: &[&'static str],
        ) where
            MethodEndpoint<S, E>: Clone,
            S: Clone,
        {
            if endpoint_filter.contains(filter) {
                if out.is_some() {
                    panic!(
                        "Overlapping method route. Cannot add two method routes that both handle \
                         `{method_name}`",
                    )
                }
                *out = endpoint.clone();
                for method in methods {
                    append_allow_header(allow_header, method);
                }
            }
        }

        set_endpoint(
            "GET",
            &mut self.get,
            &endpoint,
            filter,
            MethodFilter::GET,
            &mut self.allow_header,
            &["GET", "HEAD"],
        );

        set_endpoint(
            "HEAD",
            &mut self.head,
            &endpoint,
            filter,
            MethodFilter::HEAD,
            &mut self.allow_header,
            &["HEAD"],
        );

        set_endpoint(
            "TRACE",
            &mut self.trace,
            &endpoint,
            filter,
            MethodFilter::TRACE,
            &mut self.allow_header,
            &["TRACE"],
        );

        set_endpoint(
            "PUT",
            &mut self.put,
            &endpoint,
            filter,
            MethodFilter::PUT,
            &mut self.allow_header,
            &["PUT"],
        );

        set_endpoint(
            "POST",
            &mut self.post,
            &endpoint,
            filter,
            MethodFilter::POST,
            &mut self.allow_header,
            &["POST"],
        );

        set_endpoint(
            "PATCH",
            &mut self.patch,
            &endpoint,
            filter,
            MethodFilter::PATCH,
            &mut self.allow_header,
            &["PATCH"],
        );

        set_endpoint(
            "OPTIONS",
            &mut self.options,
            &endpoint,
            filter,
            MethodFilter::OPTIONS,
            &mut self.allow_header,
            &["OPTIONS"],
        );

        set_endpoint(
            "DELETE",
            &mut self.delete,
            &endpoint,
            filter,
            MethodFilter::DELETE,
            &mut self.allow_header,
            &["DELETE"],
        );

        set_endpoint(
            "CONNECT",
            &mut self.connect,
            &endpoint,
            filter,
            MethodFilter::CONNECT,
            &mut self.allow_header,
            &["CONNECT"],
        );

        self
    }
```


---

### 🔹 Commit #15: `6fd77f82`
- **完整 Hash**: `6fd77f82ca5b0991f4190042d48b871d7d8025e7`
- **說明 (Ground Truth)**: fix: TypedPath conflicts with OptionalFromRequestParts (#3645)
- **變更檔案數**: 1

#### 📄 檔案: `axum-macros/src/typed_path.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:74, E:108, A:0) ➔ After(N:74, E:108, A:0)
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

### 🔹 函式: `expand_named_fields()`
- **變更前簽章 (Before)**: `fn expand_named_fields(
    ident: &syn::Ident,
    path: LitStr,
    segments: &[Segment],
    rejection: Option<syn::Path>,
)` (L96~L160)
- **變更後簽章 (After)**: `fn expand_named_fields(
    ident: &syn::Ident,
    path: LitStr,
    segments: &[Segment],
    rejection: Option<syn::Path>,
)` (L96~L161)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn expand_named_fields(
    ident: &syn::Ident,
    path: LitStr,
    segments: &[Segment],
    rejection: Option<syn::Path>,
) -> TokenStream {
    let format_str = format_str_from_path(segments);
    let captures = captures_from_path(segments);

    let typed_path_impl = quote_spanned! {path.span()=>
        #[automatically_derived]
        impl ::axum_extra::routing::TypedPath for #ident {
            const PATH: &'static str = #path;
        }
    };

    let display_impl = quote_spanned! {path.span()=>
        #[automatically_derived]
        impl ::std::fmt::Display for #ident {
            #[allow(clippy::unnecessary_to_owned)]
            fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                let Self { #(#captures,)* } = self;
                write!(
                    f,
                    #format_str,
                    #(
                        #captures = ::axum_extra::__private::utf8_percent_encode(
                            &#captures.to_string(),
                            ::axum_extra::__private::PATH_SEGMENT,
                        )
                    ),*
                )
            }
        }
    };

    let rejection_assoc_type = rejection_assoc_type(&rejection);
    let map_err_rejection = map_err_rejection(&rejection);

    let from_request_impl = quote! {
        #[automatically_derived]
        impl<S> ::axum::extract::FromRequestParts<S> for #ident
        where
            S: Send + Sync,
        {
            type Rejection = #rejection_assoc_type;

            async fn from_request_parts(
                parts: &mut ::axum::http::request::Parts,
                state: &S,
            ) -> ::std::result::Result<Self, Self::Rejection> {
                ::axum::extract::Path::from_request_parts(parts, state)
                    .await
                    .map(|path| path.0)
                    #map_err_rejection
            }
        }
    };

    quote! {
        #typed_path_impl
        #display_impl
        #from_request_impl
    }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn expand_named_fields(
    ident: &syn::Ident,
    path: LitStr,
    segments: &[Segment],
    rejection: Option<syn::Path>,
) -> TokenStream {
    let format_str = format_str_from_path(segments);
    let captures = captures_from_path(segments);

    let typed_path_impl = quote_spanned! {path.span()=>
        #[automatically_derived]
        impl ::axum_extra::routing::TypedPath for #ident {
            const PATH: &'static str = #path;
        }
    };

    let display_impl = quote_spanned! {path.span()=>
        #[automatically_derived]
        impl ::std::fmt::Display for #ident {
            #[allow(clippy::unnecessary_to_owned)]
            fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                let Self { #(#captures,)* } = self;
                write!(
                    f,
                    #format_str,
                    #(
                        #captures = ::axum_extra::__private::utf8_percent_encode(
                            &#captures.to_string(),
                            ::axum_extra::__private::PATH_SEGMENT,
                        )
                    ),*
                )
            }
        }
    };

    let rejection_assoc_type = rejection_assoc_type(&rejection);
    let map_err_rejection = map_err_rejection(&rejection);

    let from_request_impl = quote! {
        #[automatically_derived]
        impl<S> ::axum::extract::FromRequestParts<S> for #ident
        where
            S: Send + Sync,
        {
            type Rejection = #rejection_assoc_type;

            async fn from_request_parts(
                parts: &mut ::axum::http::request::Parts,
                state: &S,
            ) -> ::std::result::Result<Self, Self::Rejection> {
                <::axum::extract::Path<#ident> as ::axum::extract::FromRequestParts<S>>
                    ::from_request_parts(parts, state)
                    .await
                    .map(|path| path.0)
                    #map_err_rejection
            }
        }
    };

    quote! {
        #typed_path_impl
        #display_impl
        #from_request_impl
    }
}
```


---

### 🔹 Commit #16: `27739660`
- **完整 Hash**: `2773966059a3de9734d4a2cc8f63486590e28784`
- **說明 (Ground Truth)**: Fix InternalServerError docs to match current behavior (#3640)
- **變更檔案數**: 1

#### 📄 檔案: `axum-extra/src/response/error_response.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:6, E:6, A:0) ➔ After(N:6, E:6, A:0)
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

### 🔹 Commit #17: `9c67c6c3`
- **完整 Hash**: `9c67c6c33a0986cdf1d6ac17e2b1048235be938f`
- **說明 (Ground Truth)**: [FIX] link to query-params-with-empty-string (#3695)
- **變更檔案數**: 2

#### 📄 檔案: `axum-extra/src/extract/query.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:56, E:77, A:0) ➔ After(N:56, E:77, A:0)
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

#### 📄 檔案: `axum/src/extract/query.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:36, E:34, A:0) ➔ After(N:36, E:34, A:0)
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

### 🔹 Commit #18: `d456816f`
- **完整 Hash**: `d456816f49c8798917e4184a66a6be8d1a9fa1b1`
- **說明 (Ground Truth)**: fix formatting (#3685)
- **變更檔案數**: 1

#### 📄 檔案: `axum-extra/src/extract/multipart.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:87, E:114, A:0) ➔ After(N:87, E:114, A:0)
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

### 🔹 Commit #19: `da26db26`
- **完整 Hash**: `da26db264f811e73485f1db1c134d374e8f99464`
- **說明 (Ground Truth)**: fix formatting (#3685)
- **變更檔案數**: 1

#### 📄 檔案: `axum-extra/src/extract/multipart.rs`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:93, E:124, A:0) ➔ After(N:93, E:124, A:0)
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

### 🔹 Commit #20: `22f769c7`
- **完整 Hash**: `22f769c7f1812b96a8f1a0539e520b41445ba88f`
- **說明 (Ground Truth)**: fix: Return specific error message when multipart body limit is exceeded (#3611)
- **變更檔案數**: 2

#### 📄 檔案: `axum-extra/src/extract/multipart.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:87, E:114, A:0) ➔ After(N:93, E:124, A:0)
- **差分統計**: +Nodes: 6, -Nodes: 0, +Edges: 10, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `err.downcast_ref::<axum_core::Error>()
                .and_then(|err| err.source())
                .and_then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `err.downcast_ref::<axum_core::Error> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `err.downcast_ref::<axum_core::Error>()
                .and_then(|err| err.source())
                .and_then(|err| err.downcast_ref::<http_body_util::LengthLimitError>())
                .is_some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `err.downcast_ref::<axum_core::Error>()
                .and_then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `"Request payload is too large".to_owned (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `is_body_limit_error` (FUNCTION_DEF)
  • + [新增呼叫邊] `MultipartError::body_text` ──[CALLS]──> `is_body_limit_error`
  • + [新增呼叫邊] `MultipartError::body_text` ──[CALLS]──> `"Request payload is too large".to_owned (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<multer::Error> (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `is_body_limit_error`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<axum_core::Error>()
                .and_then(|err| err.source())
                .and_then(|err| err.downcast_ref::<http_body_util::LengthLimitError>())
                .is_some (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<axum_core::Error>()
                .and_then(|err| err.source())
                .and_then (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<axum_core::Error>()
                .and_then (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<axum_core::Error> (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `MultipartError::source`
  • _... 以及其餘 1 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `MultipartError::body_text()`
- **變更前簽章 (Before)**: `fn MultipartError::body_text(&self)` (L249~L257)
- **變更後簽章 (After)**: `fn MultipartError::body_text(&self)` (L249~L261)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn body_text(&self) -> String {
        let body = self.source.to_string();
        axum_core::__log_rejection!(
            rejection_type = Self,
            body_text = body,
            status = self.status(),
        );
        body
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn body_text(&self) -> String {
        let body = if is_body_limit_error(&self.source) {
            "Request payload is too large".to_owned()
        } else {
            self.source.to_string()
        };
        axum_core::__log_rejection!(
            rejection_type = Self,
            body_text = body,
            status = self.status(),
        );
        body
    }
```

### 🔹 函式: `body_too_large()`
- **變更前簽章 (Before)**: `fn body_too_large()` (L385~L406)
- **變更後簽章 (After)**: `fn body_too_large()` (L405~L427)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async fn body_too_large() {
        const BYTES: &[u8] = "<!doctype html><title>🦀</title>".as_bytes();

        async fn handle(mut multipart: Multipart) -> Result<(), MultipartError> {
            while let Some(field) = multipart.next_field().await? {
                field.bytes().await?;
            }
            Ok(())
        }

        let app = Router::new()
            .route("/", post(handle))
            .layer(DefaultBodyLimit::max(BYTES.len() - 1));

        let client = TestClient::new(app);

        let form =
            reqwest::multipart::Form::new().part("file", reqwest::multipart::Part::bytes(BYTES));

        let res = client.post("/").multipart(form).await;
        assert_eq!(res.status(), StatusCode::PAYLOAD_TOO_LARGE);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async fn body_too_large() {
        const BYTES: &[u8] = "<!doctype html><title>🦀</title>".as_bytes();

        async fn handle(mut multipart: Multipart) -> Result<(), MultipartError> {
            while let Some(field) = multipart.next_field().await? {
                field.bytes().await?;
            }
            Ok(())
        }

        let app = Router::new()
            .route("/", post(handle))
            .layer(DefaultBodyLimit::max(BYTES.len() - 1));

        let client = TestClient::new(app);

        let form =
            reqwest::multipart::Form::new().part("file", reqwest::multipart::Part::bytes(BYTES));

        let res = client.post("/").multipart(form).await;
        assert_eq!(res.status(), StatusCode::PAYLOAD_TOO_LARGE);
        assert_eq!(res.text().await, "Request payload is too large");
    }
```


#### 📄 檔案: `axum/src/extract/multipart.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:88, E:118, A:0) ➔ After(N:94, E:128, A:0)
- **差分統計**: +Nodes: 6, -Nodes: 0, +Edges: 10, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `err.downcast_ref::<crate::Error>()
                .and_then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `err.downcast_ref::<crate::Error> (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `err.downcast_ref::<crate::Error>()
                .and_then(|err| err.source())
                .and_then (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `err.downcast_ref::<crate::Error>()
                .and_then(|err| err.source())
                .and_then(|err| err.downcast_ref::<http_body_util::LengthLimitError>())
                .is_some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `"Request payload is too large".to_owned (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `is_body_limit_error` (FUNCTION_DEF)
  • + [新增呼叫邊] `MultipartError::body_text` ──[CALLS]──> `is_body_limit_error`
  • + [新增呼叫邊] `MultipartError::body_text` ──[CALLS]──> `"Request payload is too large".to_owned (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<multer::Error> (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `is_body_limit_error`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<crate::Error>()
                .and_then(|err| err.source())
                .and_then(|err| err.downcast_ref::<http_body_util::LengthLimitError>())
                .is_some (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<crate::Error>()
                .and_then(|err| err.source())
                .and_then (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<crate::Error>()
                .and_then (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `err.downcast_ref::<crate::Error> (External/Unresolved)`
  • + [新增呼叫邊] `is_body_limit_error` ──[CALLS]──> `MultipartError::source`
  • _... 以及其餘 1 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `MultipartError::body_text()`
- **變更前簽章 (Before)**: `fn MultipartError::body_text(&self)` (L246~L248)
- **變更後簽章 (After)**: `fn MultipartError::body_text(&self)` (L246~L252)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn body_text(&self) -> String {
        self.source.to_string()
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn body_text(&self) -> String {
        if is_body_limit_error(&self.source) {
            "Request payload is too large".to_owned()
        } else {
            self.source.to_string()
        }
    }
```

### 🔹 函式: `body_too_large()`
- **變更前簽章 (Before)**: `fn body_too_large()` (L389~L410)
- **變更後簽章 (After)**: `fn body_too_large()` (L409~L431)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async fn body_too_large() {
        const BYTES: &[u8] = "<!doctype html><title>🦀</title>".as_bytes();

        async fn handle(mut multipart: Multipart) -> Result<(), MultipartError> {
            while let Some(field) = multipart.next_field().await? {
                field.bytes().await?;
            }
            Ok(())
        }

        let app = Router::new()
            .route("/", post(handle))
            .layer(DefaultBodyLimit::max(BYTES.len() - 1));

        let client = TestClient::new(app);

        let form =
            reqwest::multipart::Form::new().part("file", reqwest::multipart::Part::bytes(BYTES));

        let res = client.post("/").multipart(form).await;
        assert_eq!(res.status(), StatusCode::PAYLOAD_TOO_LARGE);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async fn body_too_large() {
        const BYTES: &[u8] = "<!doctype html><title>🦀</title>".as_bytes();

        async fn handle(mut multipart: Multipart) -> Result<(), MultipartError> {
            while let Some(field) = multipart.next_field().await? {
                field.bytes().await?;
            }
            Ok(())
        }

        let app = Router::new()
            .route("/", post(handle))
            .layer(DefaultBodyLimit::max(BYTES.len() - 1));

        let client = TestClient::new(app);

        let form =
            reqwest::multipart::Form::new().part("file", reqwest::multipart::Part::bytes(BYTES));

        let res = client.post("/").multipart(form).await;
        assert_eq!(res.status(), StatusCode::PAYLOAD_TOO_LARGE);
        assert_eq!(res.text().await, "Request payload is too large");
    }
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/axum show a000c300848c0be7ba0f63ebabd5dbe0f6643067
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff a000c300848c0be7ba0f63ebabd5dbe0f6643067~1 --file test_repos/axum/axum-core/src/body.rs
   ```
