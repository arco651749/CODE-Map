# 🔬 CODE-Map 基準審查獨立驗證報告: `httpx`
> **技術生態**: `Python (現代非同步 HTTP 客戶端)`  
> **本地倉庫路徑**: `test_repos/httpx`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 23 Files  
> **報告生成時間**: 2026-10-20 21:40:53  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `11` / `23` | `47.8%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `8` / `23` | `34.8%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `4` / `23` | `17.4%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`19` / `23`** | **`82.6%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `23` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `89599a95`
- **完整 Hash**: `89599a9541af14bcf906fc4ed58ccbdf403802ba`
- **說明 (Ground Truth)**: Fix `verify=False`, `cert=...` case. (#3442)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_config.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:23, E:13, A:0) ➔ After(N:23, E:13, A:0)
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

### 🔹 函式: `create_ssl_context()`
- **變更前簽章 (Before)**: `def create_ssl_context( verify: ssl.SSLContext | str | bool = True, cert: CertTypes | None = None, trust_env: bool = True, ) -> ssl.SSLContext` (L23~L70)
- **變更後簽章 (After)**: `def create_ssl_context( verify: ssl.SSLContext | str | bool = True, cert: CertTypes | None = None, trust_env: bool = True, ) -> ssl.SSLContext` (L23~L69)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def create_ssl_context(
    verify: ssl.SSLContext | str | bool = True,
    cert: CertTypes | None = None,
    trust_env: bool = True,
) -> ssl.SSLContext:
    import ssl
    import warnings

    import certifi

    if verify is True:
        if trust_env and os.environ.get("SSL_CERT_FILE"):  # pragma: nocover
            ctx = ssl.create_default_context(cafile=os.environ["SSL_CERT_FILE"])
        elif trust_env and os.environ.get("SSL_CERT_DIR"):  # pragma: nocover
            ctx = ssl.create_default_context(capath=os.environ["SSL_CERT_DIR"])
        else:
            # Default case...
            ctx = ssl.create_default_context(cafile=certifi.where())
    elif verify is False:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context
    elif isinstance(verify, str):  # pragma: nocover
        message = (
            "`verify=<str>` is deprecated. "
            "Use `verify=ssl.create_default_context(cafile=...)` "
            "or `verify=ssl.create_default_context(capath=...)` instead."
        )
        warnings.warn(message, DeprecationWarning)
        if os.path.isdir(verify):
            return ssl.create_default_context(capath=verify)
        return ssl.create_default_context(cafile=verify)
    else:
        ctx = verify

    if cert:  # pragma: nocover
        message = (
            "`cert=...` is deprecated. Use `verify=<ssl_context>` instead,"
            "with `.load_cert_chain()` to configure the certificate chain."
        )
        warnings.warn(message, DeprecationWarning)
        if isinstance(cert, str):
            ctx.load_cert_chain(cert)
        else:
            ctx.load_cert_chain(*cert)

    return ctx
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def create_ssl_context(
    verify: ssl.SSLContext | str | bool = True,
    cert: CertTypes | None = None,
    trust_env: bool = True,
) -> ssl.SSLContext:
    import ssl
    import warnings

    import certifi

    if verify is True:
        if trust_env and os.environ.get("SSL_CERT_FILE"):  # pragma: nocover
            ctx = ssl.create_default_context(cafile=os.environ["SSL_CERT_FILE"])
        elif trust_env and os.environ.get("SSL_CERT_DIR"):  # pragma: nocover
            ctx = ssl.create_default_context(capath=os.environ["SSL_CERT_DIR"])
        else:
            # Default case...
            ctx = ssl.create_default_context(cafile=certifi.where())
    elif verify is False:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    elif isinstance(verify, str):  # pragma: nocover
        message = (
            "`verify=<str>` is deprecated. "
            "Use `verify=ssl.create_default_context(cafile=...)` "
            "or `verify=ssl.create_default_context(capath=...)` instead."
        )
        warnings.warn(message, DeprecationWarning)
        if os.path.isdir(verify):
            return ssl.create_default_context(capath=verify)
        return ssl.create_default_context(cafile=verify)
    else:
        ctx = verify

    if cert:  # pragma: nocover
        message = (
            "`cert=...` is deprecated. Use `verify=<ssl_context>` instead,"
            "with `.load_cert_chain()` to configure the certificate chain."
        )
        warnings.warn(message, DeprecationWarning)
        if isinstance(cert, str):
            ctx.load_cert_chain(cert)
        else:
            ctx.load_cert_chain(*cert)

    return ctx
```


---

### 🔹 Commit #02: `a33c8785`
- **完整 Hash**: `a33c87852b8a0dddc65e5f739af1e0a6fca4b91f`
- **說明 (Ground Truth)**: Fix `extensions` type annotation. (#3380)
- **變更檔案數**: 2

#### 📄 檔案: `httpx/_models.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:149, E:189, A:0) ➔ After(N:149, E:191, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `Request.__init__` ──[CALLS]──> `dict (External/Unresolved)`
  • + [新增呼叫邊] `Response.__init__` ──[CALLS]──> `dict (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Request.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, method: str, url: URL | str, *, params: QueryParamTypes | None = None, headers: HeaderTypes | None = None, cookies: CookieTypes | None = None, content: RequestContent | None = None, data: RequestData | None = None, files: RequestFiles | None = None, json: typing.Any | None = None, stream: SyncByteStream | AsyncByteStream | None = None, extensions: RequestExtensions | None = None, ) -> None` (L383~L439)
- **變更後簽章 (After)**: `def __init__( self, method: str, url: URL | str, *, params: QueryParamTypes | None = None, headers: HeaderTypes | None = None, cookies: CookieTypes | None = None, content: RequestContent | None = None, data: RequestData | None = None, files: RequestFiles | None = None, json: typing.Any | None = None, stream: SyncByteStream | AsyncByteStream | None = None, extensions: RequestExtensions | None = None, ) -> None` (L383~L439)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        method: str,
        url: URL | str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        stream: SyncByteStream | AsyncByteStream | None = None,
        extensions: RequestExtensions | None = None,
    ) -> None:
        self.method = method.upper()
        self.url = URL(url) if params is None else URL(url, params=params)
        self.headers = Headers(headers)
        self.extensions = {} if extensions is None else extensions

        if cookies:
            Cookies(cookies).set_cookie_header(self)

        if stream is None:
            content_type: str | None = self.headers.get("content-type")
            headers, stream = encode_request(
                content=content,
                data=data,
                files=files,
                json=json,
                boundary=get_multipart_boundary_from_content_type(
                    content_type=content_type.encode(self.headers.encoding)
                    if content_type
                    else None
                ),
            )
            self._prepare(headers)
            self.stream = stream
            # Load the request body, except for streaming content.
            if isinstance(stream, ByteStream):
                self.read()
        else:
            # There's an important distinction between `Request(content=...)`,
            # and `Request(stream=...)`.
            #
            # Using `content=...` implies automatically populated `Host` and content
            # headers, of either `Content-Length: ...` or `Transfer-Encoding: chunked`.
            #
            # Using `stream=...` will not automatically include *any*
            # auto-populated headers.
            #
            # As an end-user you don't really need `stream=...`. It's only
            # useful when:
            #
            # * Preserving the request stream when copying requests, eg for redirects.
            # * Creating request instances on the *server-side* of the transport API.
            self.stream = stream
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        method: str,
        url: URL | str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        stream: SyncByteStream | AsyncByteStream | None = None,
        extensions: RequestExtensions | None = None,
    ) -> None:
        self.method = method.upper()
        self.url = URL(url) if params is None else URL(url, params=params)
        self.headers = Headers(headers)
        self.extensions = {} if extensions is None else dict(extensions)

        if cookies:
            Cookies(cookies).set_cookie_header(self)

        if stream is None:
            content_type: str | None = self.headers.get("content-type")
            headers, stream = encode_request(
                content=content,
                data=data,
                files=files,
                json=json,
                boundary=get_multipart_boundary_from_content_type(
                    content_type=content_type.encode(self.headers.encoding)
                    if content_type
                    else None
                ),
            )
            self._prepare(headers)
            self.stream = stream
            # Load the request body, except for streaming content.
            if isinstance(stream, ByteStream):
                self.read()
        else:
            # There's an important distinction between `Request(content=...)`,
            # and `Request(stream=...)`.
            #
            # Using `content=...` implies automatically populated `Host` and content
            # headers, of either `Content-Length: ...` or `Transfer-Encoding: chunked`.
            #
            # Using `stream=...` will not automatically include *any*
            # auto-populated headers.
            #
            # As an end-user you don't really need `stream=...`. It's only
            # useful when:
            #
            # * Preserving the request stream when copying requests, eg for redirects.
            # * Creating request instances on the *server-side* of the transport API.
            self.stream = stream
```

### 🔹 函式: `Response.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, status_code: int, *, headers: HeaderTypes | None = None, content: ResponseContent | None = None, text: str | None = None, html: str | None = None, json: typing.Any = None, stream: SyncByteStream | AsyncByteStream | None = None, request: Request | None = None, extensions: ResponseExtensions | None = None, history: list[Response] | None = None, default_encoding: str | typing.Callable[[bytes], str] = "utf-8", ) -> None` (L516~L569)
- **變更後簽章 (After)**: `def __init__( self, status_code: int, *, headers: HeaderTypes | None = None, content: ResponseContent | None = None, text: str | None = None, html: str | None = None, json: typing.Any = None, stream: SyncByteStream | AsyncByteStream | None = None, request: Request | None = None, extensions: ResponseExtensions | None = None, history: list[Response] | None = None, default_encoding: str | typing.Callable[[bytes], str] = "utf-8", ) -> None` (L516~L569)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        status_code: int,
        *,
        headers: HeaderTypes | None = None,
        content: ResponseContent | None = None,
        text: str | None = None,
        html: str | None = None,
        json: typing.Any = None,
        stream: SyncByteStream | AsyncByteStream | None = None,
        request: Request | None = None,
        extensions: ResponseExtensions | None = None,
        history: list[Response] | None = None,
        default_encoding: str | typing.Callable[[bytes], str] = "utf-8",
    ) -> None:
        self.status_code = status_code
        self.headers = Headers(headers)

        self._request: Request | None = request

        # When follow_redirects=False and a redirect is received,
        # the client will set `response.next_request`.
        self.next_request: Request | None = None

        self.extensions: ResponseExtensions = {} if extensions is None else extensions
        self.history = [] if history is None else list(history)

        self.is_closed = False
        self.is_stream_consumed = False

        self.default_encoding = default_encoding

        if stream is None:
            headers, stream = encode_response(content, text, html, json)
            self._prepare(headers)
            self.stream = stream
            if isinstance(stream, ByteStream):
                # Load the response body, except for streaming content.
                self.read()
        else:
            # There's an important distinction between `Response(content=...)`,
            # and `Response(stream=...)`.
            #
            # Using `content=...` implies automatically populated content headers,
            # of either `Content-Length: ...` or `Transfer-Encoding: chunked`.
            #
            # Using `stream=...` will not automatically include any content headers.
            #
            # As an end-user you don't really need `stream=...`. It's only
            # useful when creating response instances having received a stream
            # from the transport API.
            self.stream = stream

        self._num_bytes_downloaded = 0
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        status_code: int,
        *,
        headers: HeaderTypes | None = None,
        content: ResponseContent | None = None,
        text: str | None = None,
        html: str | None = None,
        json: typing.Any = None,
        stream: SyncByteStream | AsyncByteStream | None = None,
        request: Request | None = None,
        extensions: ResponseExtensions | None = None,
        history: list[Response] | None = None,
        default_encoding: str | typing.Callable[[bytes], str] = "utf-8",
    ) -> None:
        self.status_code = status_code
        self.headers = Headers(headers)

        self._request: Request | None = request

        # When follow_redirects=False and a redirect is received,
        # the client will set `response.next_request`.
        self.next_request: Request | None = None

        self.extensions = {} if extensions is None else dict(extensions)
        self.history = [] if history is None else list(history)

        self.is_closed = False
        self.is_stream_consumed = False

        self.default_encoding = default_encoding

        if stream is None:
            headers, stream = encode_response(content, text, html, json)
            self._prepare(headers)
            self.stream = stream
            if isinstance(stream, ByteStream):
                # Load the response body, except for streaming content.
                self.read()
        else:
            # There's an important distinction between `Response(content=...)`,
            # and `Response(stream=...)`.
            #
            # Using `content=...` implies automatically populated content headers,
            # of either `Content-Length: ...` or `Transfer-Encoding: chunked`.
            #
            # Using `stream=...` will not automatically include any content headers.
            #
            # As an end-user you don't really need `stream=...`. It's only
            # useful when creating response instances having received a stream
            # from the transport API.
            self.stream = stream

        self._num_bytes_downloaded = 0
```


#### 📄 檔案: `httpx/_types.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:5, E:2, A:0) ➔ After(N:5, E:2, A:0)
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

### 🔹 Commit #03: `47f4a96f`
- **完整 Hash**: `47f4a96ffaaaa07dca1614409549b5d7a6e7af49`
- **說明 (Ground Truth)**: Handle empty zstd responses (#3412)
- **變更檔案數**: 2

#### 📄 檔案: `httpx/__version__.py`
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

#### 📄 檔案: `httpx/_decoders.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:52, E:59, A:0) ➔ After(N:52, E:59, A:0)
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

### 🔹 函式: `ZStandardDecoder.decode()`
- **變更前簽章 (Before)**: `def decode(self, data: bytes) -> bytes` (L179~L190)
- **變更後簽章 (After)**: `def decode(self, data: bytes) -> bytes` (L180~L192)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def decode(self, data: bytes) -> bytes:
        assert zstandard is not None
        output = io.BytesIO()
        try:
            output.write(self.decompressor.decompress(data))
            while self.decompressor.eof and self.decompressor.unused_data:
                unused_data = self.decompressor.unused_data
                self.decompressor = zstandard.ZstdDecompressor().decompressobj()
                output.write(self.decompressor.decompress(unused_data))
        except zstandard.ZstdError as exc:
            raise DecodingError(str(exc)) from exc
        return output.getvalue()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def decode(self, data: bytes) -> bytes:
        assert zstandard is not None
        self.seen_data = True
        output = io.BytesIO()
        try:
            output.write(self.decompressor.decompress(data))
            while self.decompressor.eof and self.decompressor.unused_data:
                unused_data = self.decompressor.unused_data
                self.decompressor = zstandard.ZstdDecompressor().decompressobj()
                output.write(self.decompressor.decompress(unused_data))
        except zstandard.ZstdError as exc:
            raise DecodingError(str(exc)) from exc
        return output.getvalue()
```

### 🔹 函式: `ZStandardDecoder.flush()`
- **變更前簽章 (Before)**: `def flush(self) -> bytes` (L192~L196)
- **變更後簽章 (After)**: `def flush(self) -> bytes` (L194~L200)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def flush(self) -> bytes:
        ret = self.decompressor.flush()  # note: this is a no-op
        if not self.decompressor.eof:
            raise DecodingError("Zstandard data is incomplete")  # pragma: no cover
        return bytes(ret)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def flush(self) -> bytes:
        if not self.seen_data:
            return b""
        ret = self.decompressor.flush()  # note: this is a no-op
        if not self.decompressor.eof:
            raise DecodingError("Zstandard data is incomplete")  # pragma: no cover
        return bytes(ret)
```

### 🔹 函式: `ZStandardDecoder.__init__()`
- **變更前簽章 (Before)**: `def __init__(self) -> None` (L170~L177)
- **變更後簽章 (After)**: `def __init__(self) -> None` (L170~L178)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(self) -> None:
        if zstandard is None:  # pragma: no cover
            raise ImportError(
                "Using 'ZStandardDecoder', ..."
                "Make sure to install httpx using `pip install httpx[zstd]`."
            ) from None

        self.decompressor = zstandard.ZstdDecompressor().decompressobj()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(self) -> None:
        if zstandard is None:  # pragma: no cover
            raise ImportError(
                "Using 'ZStandardDecoder', ..."
                "Make sure to install httpx using `pip install httpx[zstd]`."
            ) from None

        self.decompressor = zstandard.ZstdDecompressor().decompressobj()
        self.seen_data = False
```


---

### 🔹 Commit #04: `66225539`
- **完整 Hash**: `66225539796d819b5114ead2fd5e4d61865ab708`
- **說明 (Ground Truth)**: Cleanup `Request` method parameter. (#3378)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_models.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:143, E:179, A:0) ➔ After(N:143, E:178, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除呼叫邊] `Request.__init__` ──[CALLS]──> `decode (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Request.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, method: str | bytes, url: URL | str, *, params: QueryParamTypes | None = None, headers: HeaderTypes | None = None, cookies: CookieTypes | None = None, content: RequestContent | None = None, data: RequestData | None = None, files: RequestFiles | None = None, json: typing.Any | None = None, stream: SyncByteStream | AsyncByteStream | None = None, extensions: RequestExtensions | None = None, ) -> None` (L311~L371)
- **變更後簽章 (After)**: `def __init__( self, method: str, url: URL | str, *, params: QueryParamTypes | None = None, headers: HeaderTypes | None = None, cookies: CookieTypes | None = None, content: RequestContent | None = None, data: RequestData | None = None, files: RequestFiles | None = None, json: typing.Any | None = None, stream: SyncByteStream | AsyncByteStream | None = None, extensions: RequestExtensions | None = None, ) -> None` (L311~L367)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        method: str | bytes,
        url: URL | str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        stream: SyncByteStream | AsyncByteStream | None = None,
        extensions: RequestExtensions | None = None,
    ) -> None:
        self.method = (
            method.decode("ascii").upper()
            if isinstance(method, bytes)
            else method.upper()
        )
        self.url = URL(url) if params is None else URL(url, params=params)
        self.headers = Headers(headers)
        self.extensions = {} if extensions is None else extensions

        if cookies:
            Cookies(cookies).set_cookie_header(self)

        if stream is None:
            content_type: str | None = self.headers.get("content-type")
            headers, stream = encode_request(
                content=content,
                data=data,
                files=files,
                json=json,
                boundary=get_multipart_boundary_from_content_type(
                    content_type=content_type.encode(self.headers.encoding)
                    if content_type
                    else None
                ),
            )
            self._prepare(headers)
            self.stream = stream
            # Load the request body, except for streaming content.
            if isinstance(stream, ByteStream):
                self.read()
        else:
            # There's an important distinction between `Request(content=...)`,
            # and `Request(stream=...)`.
            #
            # Using `content=...` implies automatically populated `Host` and content
            # headers, of either `Content-Length: ...` or `Transfer-Encoding: chunked`.
            #
            # Using `stream=...` will not automatically include *any*
            # auto-populated headers.
            #
            # As an end-user you don't really need `stream=...`. It's only
            # useful when:
            #
            # * Preserving the request stream when copying requests, eg for redirects.
            # * Creating request instances on the *server-side* of the transport API.
            self.stream = stream
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        method: str,
        url: URL | str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        stream: SyncByteStream | AsyncByteStream | None = None,
        extensions: RequestExtensions | None = None,
    ) -> None:
        self.method = method.upper()
        self.url = URL(url) if params is None else URL(url, params=params)
        self.headers = Headers(headers)
        self.extensions = {} if extensions is None else extensions

        if cookies:
            Cookies(cookies).set_cookie_header(self)

        if stream is None:
            content_type: str | None = self.headers.get("content-type")
            headers, stream = encode_request(
                content=content,
                data=data,
                files=files,
                json=json,
                boundary=get_multipart_boundary_from_content_type(
                    content_type=content_type.encode(self.headers.encoding)
                    if content_type
                    else None
                ),
            )
            self._prepare(headers)
            self.stream = stream
            # Load the request body, except for streaming content.
            if isinstance(stream, ByteStream):
                self.read()
        else:
            # There's an important distinction between `Request(content=...)`,
            # and `Request(stream=...)`.
            #
            # Using `content=...` implies automatically populated `Host` and content
            # headers, of either `Content-Length: ...` or `Transfer-Encoding: chunked`.
            #
            # Using `stream=...` will not automatically include *any*
            # auto-populated headers.
            #
            # As an end-user you don't really need `stream=...`. It's only
            # useful when:
            #
            # * Preserving the request stream when copying requests, eg for redirects.
            # * Creating request instances on the *server-side* of the transport API.
            self.stream = stream
```


---

### 🔹 Commit #05: `88a81c5d`
- **完整 Hash**: `88a81c5d31a4a8b4bd0a860dedd3bb12dc09ff86`
- **說明 (Ground Truth)**: [fix] Use proxy ssl context consistently (#3175)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_transports/default.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:34, E:42, A:0) ➔ After(N:34, E:42, A:0)
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

### 🔹 函式: `AsyncHTTPTransport.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, verify: VerifyTypes = True, cert: CertTypes | None = None, http1: bool = True, http2: bool = False, limits: Limits = DEFAULT_LIMITS, trust_env: bool = True, proxy: ProxyTypes | None = None, uds: str | None = None, local_address: str | None = None, retries: int = 0, socket_options: typing.Iterable[SOCKET_OPTION] | None = None, ) -> None` (L266~L342)
- **變更後簽章 (After)**: `def __init__( self, verify: VerifyTypes = True, cert: CertTypes | None = None, http1: bool = True, http2: bool = False, limits: Limits = DEFAULT_LIMITS, trust_env: bool = True, proxy: ProxyTypes | None = None, uds: str | None = None, local_address: str | None = None, retries: int = 0, socket_options: typing.Iterable[SOCKET_OPTION] | None = None, ) -> None` (L266~L343)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        verify: VerifyTypes = True,
        cert: CertTypes | None = None,
        http1: bool = True,
        http2: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        trust_env: bool = True,
        proxy: ProxyTypes | None = None,
        uds: str | None = None,
        local_address: str | None = None,
        retries: int = 0,
        socket_options: typing.Iterable[SOCKET_OPTION] | None = None,
    ) -> None:
        ssl_context = create_ssl_context(verify=verify, cert=cert, trust_env=trust_env)
        proxy = Proxy(url=proxy) if isinstance(proxy, (str, URL)) else proxy

        if proxy is None:
            self._pool = httpcore.AsyncConnectionPool(
                ssl_context=ssl_context,
                max_connections=limits.max_connections,
                max_keepalive_connections=limits.max_keepalive_connections,
                keepalive_expiry=limits.keepalive_expiry,
                http1=http1,
                http2=http2,
                uds=uds,
                local_address=local_address,
                retries=retries,
                socket_options=socket_options,
            )
        elif proxy.url.scheme in ("http", "https"):
            self._pool = httpcore.AsyncHTTPProxy(
                proxy_url=httpcore.URL(
                    scheme=proxy.url.raw_scheme,
                    host=proxy.url.raw_host,
                    port=proxy.url.port,
                    target=proxy.url.raw_path,
                ),
                proxy_auth=proxy.raw_auth,
                proxy_headers=proxy.headers.raw,
                ssl_context=ssl_context,
                max_connections=limits.max_connections,
                max_keepalive_connections=limits.max_keepalive_connections,
                keepalive_expiry=limits.keepalive_expiry,
                http1=http1,
                http2=http2,
                socket_options=socket_options,
            )
        elif proxy.url.scheme == "socks5":
            try:
                import socksio  # noqa
            except ImportError:  # pragma: no cover
                raise ImportError(
                    "Using SOCKS proxy, but the 'socksio' package is not installed. "
                    "Make sure to install httpx using `pip install httpx[socks]`."
                ) from None

            self._pool = httpcore.AsyncSOCKSProxy(
                proxy_url=httpcore.URL(
                    scheme=proxy.url.raw_scheme,
                    host=proxy.url.raw_host,
                    port=proxy.url.port,
                    target=proxy.url.raw_path,
                ),
                proxy_auth=proxy.raw_auth,
                ssl_context=ssl_context,
                max_connections=limits.max_connections,
                max_keepalive_connections=limits.max_keepalive_connections,
                keepalive_expiry=limits.keepalive_expiry,
                http1=http1,
                http2=http2,
            )
        else:  # pragma: no cover
            raise ValueError(
                "Proxy protocol must be either 'http', 'https', or 'socks5',"
                " but got {proxy.url.scheme!r}."
            )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        verify: VerifyTypes = True,
        cert: CertTypes | None = None,
        http1: bool = True,
        http2: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        trust_env: bool = True,
        proxy: ProxyTypes | None = None,
        uds: str | None = None,
        local_address: str | None = None,
        retries: int = 0,
        socket_options: typing.Iterable[SOCKET_OPTION] | None = None,
    ) -> None:
        ssl_context = create_ssl_context(verify=verify, cert=cert, trust_env=trust_env)
        proxy = Proxy(url=proxy) if isinstance(proxy, (str, URL)) else proxy

        if proxy is None:
            self._pool = httpcore.AsyncConnectionPool(
                ssl_context=ssl_context,
                max_connections=limits.max_connections,
                max_keepalive_connections=limits.max_keepalive_connections,
                keepalive_expiry=limits.keepalive_expiry,
                http1=http1,
                http2=http2,
                uds=uds,
                local_address=local_address,
                retries=retries,
                socket_options=socket_options,
            )
        elif proxy.url.scheme in ("http", "https"):
            self._pool = httpcore.AsyncHTTPProxy(
                proxy_url=httpcore.URL(
                    scheme=proxy.url.raw_scheme,
                    host=proxy.url.raw_host,
                    port=proxy.url.port,
                    target=proxy.url.raw_path,
                ),
                proxy_auth=proxy.raw_auth,
                proxy_headers=proxy.headers.raw,
                proxy_ssl_context=proxy.ssl_context,
                ssl_context=ssl_context,
                max_connections=limits.max_connections,
                max_keepalive_connections=limits.max_keepalive_connections,
                keepalive_expiry=limits.keepalive_expiry,
                http1=http1,
                http2=http2,
                socket_options=socket_options,
            )
        elif proxy.url.scheme == "socks5":
            try:
                import socksio  # noqa
            except ImportError:  # pragma: no cover
                raise ImportError(
                    "Using SOCKS proxy, but the 'socksio' package is not installed. "
                    "Make sure to install httpx using `pip install httpx[socks]`."
                ) from None

            self._pool = httpcore.AsyncSOCKSProxy(
                proxy_url=httpcore.URL(
                    scheme=proxy.url.raw_scheme,
                    host=proxy.url.raw_host,
                    port=proxy.url.port,
                    target=proxy.url.raw_path,
                ),
                proxy_auth=proxy.raw_auth,
                ssl_context=ssl_context,
                max_connections=limits.max_connections,
                max_keepalive_connections=limits.max_keepalive_connections,
                keepalive_expiry=limits.keepalive_expiry,
                http1=http1,
                http2=http2,
            )
        else:  # pragma: no cover
            raise ValueError(
                "Proxy protocol must be either 'http', 'https', or 'socks5',"
                " but got {proxy.url.scheme!r}."
            )
```


---

### 🔹 Commit #06: `6d852d31`
- **完整 Hash**: `6d852d319acd5d97caf14037dff15ede04b37542`
- **說明 (Ground Truth)**: Fix client.send() timeout new Request instance (#3116)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_client.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:134, E:181, A:0) ➔ After(N:135, E:186, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 5, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `BaseClient._set_timeout` (FUNCTION_DEF)
  • + [新增呼叫邊] `BaseClient._set_timeout` ──[CALLS]──> `Timeout (External/Unresolved)`
  • + [新增呼叫邊] `BaseClient._set_timeout` ──[CALLS]──> `dict (External/Unresolved)`
  • + [新增呼叫邊] `BaseClient._set_timeout` ──[CALLS]──> `as_dict (External/Unresolved)`
  • + [新增呼叫邊] `Client.send` ──[CALLS]──> `BaseClient._set_timeout`
  • + [新增呼叫邊] `AsyncClient.send` ──[CALLS]──> `BaseClient._set_timeout`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Client.send()`
- **變更前簽章 (Before)**: `def send( self, request: Request, *, stream: bool = False, auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT, follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT, ) -> Response` (L883~L930)
- **變更後簽章 (After)**: `def send( self, request: Request, *, stream: bool = False, auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT, follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT, ) -> Response` (L892~L941)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def send(
        self,
        request: Request,
        *,
        stream: bool = False,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
    ) -> Response:
        """
        Send a request.

        The request is sent as-is, unmodified.

        Typically you'll want to build one with `Client.build_request()`
        so that any client-level configuration is merged into the request,
        but passing an explicit `httpx.Request()` is supported as well.

        See also: [Request instances][0]

        [0]: /advanced/#request-instances
        """
        if self._state == ClientState.CLOSED:
            raise RuntimeError("Cannot send a request, as the client has been closed.")

        self._state = ClientState.OPENED
        follow_redirects = (
            self.follow_redirects
            if isinstance(follow_redirects, UseClientDefault)
            else follow_redirects
        )

        auth = self._build_request_auth(request, auth)

        response = self._send_handling_auth(
            request,
            auth=auth,
            follow_redirects=follow_redirects,
            history=[],
        )
        try:
            if not stream:
                response.read()

            return response

        except BaseException as exc:
            response.close()
            raise exc
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def send(
        self,
        request: Request,
        *,
        stream: bool = False,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
    ) -> Response:
        """
        Send a request.

        The request is sent as-is, unmodified.

        Typically you'll want to build one with `Client.build_request()`
        so that any client-level configuration is merged into the request,
        but passing an explicit `httpx.Request()` is supported as well.

        See also: [Request instances][0]

        [0]: /advanced/#request-instances
        """
        if self._state == ClientState.CLOSED:
            raise RuntimeError("Cannot send a request, as the client has been closed.")

        self._state = ClientState.OPENED
        follow_redirects = (
            self.follow_redirects
            if isinstance(follow_redirects, UseClientDefault)
            else follow_redirects
        )

        self._set_timeout(request)

        auth = self._build_request_auth(request, auth)

        response = self._send_handling_auth(
            request,
            auth=auth,
            follow_redirects=follow_redirects,
            history=[],
        )
        try:
            if not stream:
                response.read()

            return response

        except BaseException as exc:
            response.close()
            raise exc
```

### 🔹 函式: `AsyncClient.send()`
- **變更前簽章 (Before)**: `async def send( self, request: Request, *, stream: bool = False, auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT, follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT, ) -> Response` (L1630~L1677)
- **變更後簽章 (After)**: `async def send( self, request: Request, *, stream: bool = False, auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT, follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT, ) -> Response` (L1641~L1690)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def send(
        self,
        request: Request,
        *,
        stream: bool = False,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
    ) -> Response:
        """
        Send a request.

        The request is sent as-is, unmodified.

        Typically you'll want to build one with `AsyncClient.build_request()`
        so that any client-level configuration is merged into the request,
        but passing an explicit `httpx.Request()` is supported as well.

        See also: [Request instances][0]

        [0]: /advanced/#request-instances
        """
        if self._state == ClientState.CLOSED:
            raise RuntimeError("Cannot send a request, as the client has been closed.")

        self._state = ClientState.OPENED
        follow_redirects = (
            self.follow_redirects
            if isinstance(follow_redirects, UseClientDefault)
            else follow_redirects
        )

        auth = self._build_request_auth(request, auth)

        response = await self._send_handling_auth(
            request,
            auth=auth,
            follow_redirects=follow_redirects,
            history=[],
        )
        try:
            if not stream:
                await response.aread()

            return response

        except BaseException as exc:
            await response.aclose()
            raise exc
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def send(
        self,
        request: Request,
        *,
        stream: bool = False,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
    ) -> Response:
        """
        Send a request.

        The request is sent as-is, unmodified.

        Typically you'll want to build one with `AsyncClient.build_request()`
        so that any client-level configuration is merged into the request,
        but passing an explicit `httpx.Request()` is supported as well.

        See also: [Request instances][0]

        [0]: /advanced/#request-instances
        """
        if self._state == ClientState.CLOSED:
            raise RuntimeError("Cannot send a request, as the client has been closed.")

        self._state = ClientState.OPENED
        follow_redirects = (
            self.follow_redirects
            if isinstance(follow_redirects, UseClientDefault)
            else follow_redirects
        )

        self._set_timeout(request)

        auth = self._build_request_auth(request, auth)

        response = await self._send_handling_auth(
            request,
            auth=auth,
            follow_redirects=follow_redirects,
            history=[],
        )
        try:
            if not stream:
                await response.aread()

            return response

        except BaseException as exc:
            await response.aclose()
            raise exc
```


---

### 🔹 Commit #07: `99cba6ac`
- **完整 Hash**: `99cba6ac642b12f0331d069ae324402c54c4c600`
- **說明 (Ground Truth)**: Fix RFC 2069 mode digest authentication (#3045)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_auth.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:46, E:50, A:0) ➔ After(N:46, E:50, A:0)
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

### 🔹 函式: `DigestAuth._build_auth_header()`
- **變更前簽章 (Before)**: `def _build_auth_header( self, request: Request, challenge: "_DigestAuthChallenge" ) -> str` (L258~L303)
- **變更後簽章 (After)**: `def _build_auth_header( self, request: Request, challenge: "_DigestAuthChallenge" ) -> str` (L258~L304)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _build_auth_header(
        self, request: Request, challenge: "_DigestAuthChallenge"
    ) -> str:
        hash_func = self._ALGORITHM_TO_HASH_FUNCTION[challenge.algorithm.upper()]

        def digest(data: bytes) -> bytes:
            return hash_func(data).hexdigest().encode()

        A1 = b":".join((self._username, challenge.realm, self._password))

        path = request.url.raw_path
        A2 = b":".join((request.method.encode(), path))
        # TODO: implement auth-int
        HA2 = digest(A2)

        nc_value = b"%08x" % self._nonce_count
        cnonce = self._get_client_nonce(self._nonce_count, challenge.nonce)
        self._nonce_count += 1

        HA1 = digest(A1)
        if challenge.algorithm.lower().endswith("-sess"):
            HA1 = digest(b":".join((HA1, challenge.nonce, cnonce)))

        qop = self._resolve_qop(challenge.qop, request=request)
        if qop is None:
            digest_data = [HA1, challenge.nonce, HA2]
        else:
            digest_data = [challenge.nonce, nc_value, cnonce, qop, HA2]
        key_digest = b":".join(digest_data)

        format_args = {
            "username": self._username,
            "realm": challenge.realm,
            "nonce": challenge.nonce,
            "uri": path,
            "response": digest(b":".join((HA1, key_digest))),
            "algorithm": challenge.algorithm.encode(),
        }
        if challenge.opaque:
            format_args["opaque"] = challenge.opaque
        if qop:
            format_args["qop"] = b"auth"
            format_args["nc"] = nc_value
            format_args["cnonce"] = cnonce

        return "Digest " + self._get_header_value(format_args)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _build_auth_header(
        self, request: Request, challenge: "_DigestAuthChallenge"
    ) -> str:
        hash_func = self._ALGORITHM_TO_HASH_FUNCTION[challenge.algorithm.upper()]

        def digest(data: bytes) -> bytes:
            return hash_func(data).hexdigest().encode()

        A1 = b":".join((self._username, challenge.realm, self._password))

        path = request.url.raw_path
        A2 = b":".join((request.method.encode(), path))
        # TODO: implement auth-int
        HA2 = digest(A2)

        nc_value = b"%08x" % self._nonce_count
        cnonce = self._get_client_nonce(self._nonce_count, challenge.nonce)
        self._nonce_count += 1

        HA1 = digest(A1)
        if challenge.algorithm.lower().endswith("-sess"):
            HA1 = digest(b":".join((HA1, challenge.nonce, cnonce)))

        qop = self._resolve_qop(challenge.qop, request=request)
        if qop is None:
            # Following RFC 2069
            digest_data = [HA1, challenge.nonce, HA2]
        else:
            # Following RFC 2617/7616
            digest_data = [HA1, challenge.nonce, nc_value, cnonce, qop, HA2]

        format_args = {
            "username": self._username,
            "realm": challenge.realm,
            "nonce": challenge.nonce,
            "uri": path,
            "response": digest(b":".join(digest_data)),
            "algorithm": challenge.algorithm.encode(),
        }
        if challenge.opaque:
            format_args["opaque"] = challenge.opaque
        if qop:
            format_args["qop"] = b"auth"
            format_args["nc"] = nc_value
            format_args["cnonce"] = cnonce

        return "Digest " + self._get_header_value(format_args)
```


---

### 🔹 Commit #08: `a11fc384`
- **完整 Hash**: `a11fc3849b94157274c98d99501acad05cbfb221`
- **說明 (Ground Truth)**: Cleanup URL percent-encoding behavior. (#2990)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_urlparse.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:31, E:34, A:0) ➔ After(N:34, E:37, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 2, +Edges: 8, -Edges: 5, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `percent_encoded` (FUNCTION_DEF)
  • + [新增節點] `group (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `end (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `start (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `finditer (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `findall (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `count (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `percent_encoded` ──[CALLS]──> `is_safe`
  • + [新增呼叫邊] `percent_encoded` ──[CALLS]──> `percent_encode`
  • + [新增呼叫邊] `quote` ──[CALLS]──> `finditer (External/Unresolved)`
  • + [新增呼叫邊] `quote` ──[CALLS]──> `start (External/Unresolved)`
  • + [新增呼叫邊] `quote` ──[CALLS]──> `end (External/Unresolved)`
  • + [新增呼叫邊] `quote` ──[CALLS]──> `group (External/Unresolved)`
  • + [新增呼叫邊] `quote` ──[CALLS]──> `percent_encoded`
  • + [新增呼叫邊] `urlencode` ──[CALLS]──> `percent_encoded`
  • _... 以及其餘 5 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `urlencode()`
- **變更前簽章 (Before)**: `def urlencode(items: typing.List[typing.Tuple[str, str]]) -> str` (L452~L467)
- **變更後簽章 (After)**: `def urlencode(items: typing.List[typing.Tuple[str, str]]) -> str` (L482~L502)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def urlencode(items: typing.List[typing.Tuple[str, str]]) -> str:
    """
    We can use a much simpler version of the stdlib urlencode here because
    we don't need to handle a bunch of different typing cases, such as bytes vs str.

    https://github.com/python/cpython/blob/b2f7b2ef0b5421e01efb8c7bee2ef95d3bab77eb/Lib/urllib/parse.py#L926

    Note that we use '%20' encoding for spaces. and '%2F  for '/'.
    This is slightly different than `requests`, but is the behaviour that browsers use.

    See
    - https://github.com/encode/httpx/issues/2536
    - https://github.com/encode/httpx/issues/2721
    - https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode
    """
    return "&".join([quote(k, safe="") + "=" + quote(v, safe="") for k, v in items])
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def urlencode(items: typing.List[typing.Tuple[str, str]]) -> str:
    """
    We can use a much simpler version of the stdlib urlencode here because
    we don't need to handle a bunch of different typing cases, such as bytes vs str.

    https://github.com/python/cpython/blob/b2f7b2ef0b5421e01efb8c7bee2ef95d3bab77eb/Lib/urllib/parse.py#L926

    Note that we use '%20' encoding for spaces. and '%2F  for '/'.
    This is slightly different than `requests`, but is the behaviour that browsers use.

    See
    - https://github.com/encode/httpx/issues/2536
    - https://github.com/encode/httpx/issues/2721
    - https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode
    """
    return "&".join(
        [
            percent_encoded(k, safe="") + "=" + percent_encoded(v, safe="")
            for k, v in items
        ]
    )
```

### 🔹 函式: `urlparse()`
- **變更前簽章 (Before)**: `def urlparse(url: str = "", **kwargs: typing.Optional[str]) -> ParseResult: # Initial basic checks on allowable URLs. # --------------------------------------- # Hard limit the maximum allowable URL length.` (L149~L283)
- **變更後簽章 (After)**: `def urlparse(url: str = "", **kwargs: typing.Optional[str]) -> ParseResult: # Initial basic checks on allowable URLs. # --------------------------------------- # Hard limit the maximum allowable URL length.` (L149~L281)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def urlparse(url: str = "", **kwargs: typing.Optional[str]) -> ParseResult:
    # Initial basic checks on allowable URLs.
    # ---------------------------------------

    # Hard limit the maximum allowable URL length.
    if len(url) > MAX_URL_LENGTH:
        raise InvalidURL("URL too long")

    # If a URL includes any ASCII control characters including \t, \r, \n,
    # then treat it as invalid.
    if any(char.isascii() and not char.isprintable() for char in url):
        raise InvalidURL("Invalid non-printable ASCII character in URL")

    # Some keyword arguments require special handling.
    # ------------------------------------------------

    # Coerce "port" to a string, if it is provided as an integer.
    if "port" in kwargs:
        port = kwargs["port"]
        kwargs["port"] = str(port) if isinstance(port, int) else port

    # Replace "netloc" with "host and "port".
    if "netloc" in kwargs:
        netloc = kwargs.pop("netloc") or ""
        kwargs["host"], _, kwargs["port"] = netloc.partition(":")

    # Replace "username" and/or "password" with "userinfo".
    if "username" in kwargs or "password" in kwargs:
        username = quote(kwargs.pop("username", "") or "")
        password = quote(kwargs.pop("password", "") or "")
        kwargs["userinfo"] = f"{username}:{password}" if password else username

    # Replace "raw_path" with "path" and "query".
    if "raw_path" in kwargs:
        raw_path = kwargs.pop("raw_path") or ""
        kwargs["path"], seperator, kwargs["query"] = raw_path.partition("?")
        if not seperator:
            kwargs["query"] = None

    # Ensure that IPv6 "host" addresses are always escaped with "[...]".
    if "host" in kwargs:
        host = kwargs.get("host") or ""
        if ":" in host and not (host.startswith("[") and host.endswith("]")):
            kwargs["host"] = f"[{host}]"

    # If any keyword arguments are provided, ensure they are valid.
    # -------------------------------------------------------------

    for key, value in kwargs.items():
        if value is not None:
            if len(value) > MAX_URL_LENGTH:
                raise InvalidURL(f"URL component '{key}' too long")

            # If a component includes any ASCII control characters including \t, \r, \n,
            # then treat it as invalid.
            if any(char.isascii() and not char.isprintable() for char in value):
                raise InvalidURL(
                    f"Invalid non-printable ASCII character in URL component '{key}'"
                )

            # Ensure that keyword arguments match as a valid regex.
            if not COMPONENT_REGEX[key].fullmatch(value):
                raise InvalidURL(f"Invalid URL component '{key}'")

    # The URL_REGEX will always match, but may have empty components.
    url_match = URL_REGEX.match(url)
    assert url_match is not None
    url_dict = url_match.groupdict()

    # * 'scheme', 'authority', and 'path' may be empty strings.
    # * 'query' may be 'None', indicating no trailing "?" portion.
    #   Any string including the empty string, indicates a trailing "?".
    # * 'fragment' may be 'None', indicating no trailing "#" portion.
    #   Any string including the empty string, indicates a trailing "#".
    scheme = kwargs.get("scheme", url_dict["scheme"]) or ""
    authority = kwargs.get("authority", url_dict["authority"]) or ""
    path = kwargs.get("path", url_dict["path"]) or ""
    query = kwargs.get("query", url_dict["query"])
    fragment = kwargs.get("fragment", url_dict["fragment"])

    # The AUTHORITY_REGEX will always match, but may have empty components.
    authority_match = AUTHORITY_REGEX.match(authority)
    assert authority_match is not None
    authority_dict = authority_match.groupdict()

    # * 'userinfo' and 'host' may be empty strings.
    # * 'port' may be 'None'.
    userinfo = kwargs.get("userinfo", authority_dict["userinfo"]) or ""
    host = kwargs.get("host", authority_dict["host"]) or ""
    port = kwargs.get("port", authority_dict["port"])

    # Normalize and validate each component.
    # We end up with a parsed representation of the URL,
    # with components that are plain ASCII bytestrings.
    parsed_scheme: str = scheme.lower()
    parsed_userinfo: str = quote(userinfo, safe=SUB_DELIMS + ":")
    parsed_host: str = encode_host(host)
    parsed_port: typing.Optional[int] = normalize_port(port, scheme)

    has_scheme = parsed_scheme != ""
    has_authority = (
        parsed_userinfo != "" or parsed_host != "" or parsed_port is not None
    )
    validate_path(path, has_scheme=has_scheme, has_authority=has_authority)
    if has_authority:
        path = normalize_path(path)

    # The GEN_DELIMS set is... : / ? # [ ] @
    # These do not need to be percent-quoted unless they serve as delimiters for the
    # specific component.

    # For 'path' we need to drop ? and # from the GEN_DELIMS set.
    parsed_path: str = quote(path, safe=SUB_DELIMS + ":/[]@")
    # For 'query' we need to drop '#' from the GEN_DELIMS set.
    # We also exclude '/' because it is more robust to replace it with a percent
    # encoding despite it not being a requirement of the spec.
    parsed_query: typing.Optional[str] = (
        None if query is None else quote(query, safe=SUB_DELIMS + ":?[]@")
    )
    # For 'fragment' we can include all of the GEN_DELIMS set.
    parsed_fragment: typing.Optional[str] = (
        None if fragment is None else quote(fragment, safe=SUB_DELIMS + ":/?#[]@")
    )

    # The parsed ASCII bytestrings are our canonical form.
    # All properties of the URL are derived from these.
    return ParseResult(
        parsed_scheme,
        parsed_userinfo,
        parsed_host,
        parsed_port,
        parsed_path,
        parsed_query,
        parsed_fragment,
    )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def urlparse(url: str = "", **kwargs: typing.Optional[str]) -> ParseResult:
    # Initial basic checks on allowable URLs.
    # ---------------------------------------

    # Hard limit the maximum allowable URL length.
    if len(url) > MAX_URL_LENGTH:
        raise InvalidURL("URL too long")

    # If a URL includes any ASCII control characters including \t, \r, \n,
    # then treat it as invalid.
    if any(char.isascii() and not char.isprintable() for char in url):
        raise InvalidURL("Invalid non-printable ASCII character in URL")

    # Some keyword arguments require special handling.
    # ------------------------------------------------

    # Coerce "port" to a string, if it is provided as an integer.
    if "port" in kwargs:
        port = kwargs["port"]
        kwargs["port"] = str(port) if isinstance(port, int) else port

    # Replace "netloc" with "host and "port".
    if "netloc" in kwargs:
        netloc = kwargs.pop("netloc") or ""
        kwargs["host"], _, kwargs["port"] = netloc.partition(":")

    # Replace "username" and/or "password" with "userinfo".
    if "username" in kwargs or "password" in kwargs:
        username = quote(kwargs.pop("username", "") or "")
        password = quote(kwargs.pop("password", "") or "")
        kwargs["userinfo"] = f"{username}:{password}" if password else username

    # Replace "raw_path" with "path" and "query".
    if "raw_path" in kwargs:
        raw_path = kwargs.pop("raw_path") or ""
        kwargs["path"], seperator, kwargs["query"] = raw_path.partition("?")
        if not seperator:
            kwargs["query"] = None

    # Ensure that IPv6 "host" addresses are always escaped with "[...]".
    if "host" in kwargs:
        host = kwargs.get("host") or ""
        if ":" in host and not (host.startswith("[") and host.endswith("]")):
            kwargs["host"] = f"[{host}]"

    # If any keyword arguments are provided, ensure they are valid.
    # -------------------------------------------------------------

    for key, value in kwargs.items():
        if value is not None:
            if len(value) > MAX_URL_LENGTH:
                raise InvalidURL(f"URL component '{key}' too long")

            # If a component includes any ASCII control characters including \t, \r, \n,
            # then treat it as invalid.
            if any(char.isascii() and not char.isprintable() for char in value):
                raise InvalidURL(
                    f"Invalid non-printable ASCII character in URL component '{key}'"
                )

            # Ensure that keyword arguments match as a valid regex.
            if not COMPONENT_REGEX[key].fullmatch(value):
                raise InvalidURL(f"Invalid URL component '{key}'")

    # The URL_REGEX will always match, but may have empty components.
    url_match = URL_REGEX.match(url)
    assert url_match is not None
    url_dict = url_match.groupdict()

    # * 'scheme', 'authority', and 'path' may be empty strings.
    # * 'query' may be 'None', indicating no trailing "?" portion.
    #   Any string including the empty string, indicates a trailing "?".
    # * 'fragment' may be 'None', indicating no trailing "#" portion.
    #   Any string including the empty string, indicates a trailing "#".
    scheme = kwargs.get("scheme", url_dict["scheme"]) or ""
    authority = kwargs.get("authority", url_dict["authority"]) or ""
    path = kwargs.get("path", url_dict["path"]) or ""
    query = kwargs.get("query", url_dict["query"])
    fragment = kwargs.get("fragment", url_dict["fragment"])

    # The AUTHORITY_REGEX will always match, but may have empty components.
    authority_match = AUTHORITY_REGEX.match(authority)
    assert authority_match is not None
    authority_dict = authority_match.groupdict()

    # * 'userinfo' and 'host' may be empty strings.
    # * 'port' may be 'None'.
    userinfo = kwargs.get("userinfo", authority_dict["userinfo"]) or ""
    host = kwargs.get("host", authority_dict["host"]) or ""
    port = kwargs.get("port", authority_dict["port"])

    # Normalize and validate each component.
    # We end up with a parsed representation of the URL,
    # with components that are plain ASCII bytestrings.
    parsed_scheme: str = scheme.lower()
    parsed_userinfo: str = quote(userinfo, safe=SUB_DELIMS + ":")
    parsed_host: str = encode_host(host)
    parsed_port: typing.Optional[int] = normalize_port(port, scheme)

    has_scheme = parsed_scheme != ""
    has_authority = (
        parsed_userinfo != "" or parsed_host != "" or parsed_port is not None
    )
    validate_path(path, has_scheme=has_scheme, has_authority=has_authority)
    if has_authority:
        path = normalize_path(path)

    # The GEN_DELIMS set is... : / ? # [ ] @
    # These do not need to be percent-quoted unless they serve as delimiters for the
    # specific component.

    # For 'path' we need to drop ? and # from the GEN_DELIMS set.
    parsed_path: str = quote(path, safe=SUB_DELIMS + ":/[]@")
    # For 'query' we need to drop '#' from the GEN_DELIMS set.
    parsed_query: typing.Optional[str] = (
        None if query is None else quote(query, safe=SUB_DELIMS + ":/?[]@")
    )
    # For 'fragment' we can include all of the GEN_DELIMS set.
    parsed_fragment: typing.Optional[str] = (
        None if fragment is None else quote(fragment, safe=SUB_DELIMS + ":/?#[]@")
    )

    # The parsed ASCII bytestrings are our canonical form.
    # All properties of the URL are derived from these.
    return ParseResult(
        parsed_scheme,
        parsed_userinfo,
        parsed_host,
        parsed_port,
        parsed_path,
        parsed_query,
        parsed_fragment,
    )
```

### 🔹 函式: `is_safe()`
- **變更前簽章 (Before)**: `def is_safe(string: str, safe: str = "/") -> bool` (L424~L436)
- **變更後簽章 (After)**: `def is_safe(string: str, safe: str = "/") -> bool` (L422~L433)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def is_safe(string: str, safe: str = "/") -> bool:
    """
    Determine if a given string is already quote-safe.
    """
    NON_ESCAPED_CHARS = UNRESERVED_CHARACTERS + safe + "%"

    # All characters must already be non-escaping or '%'
    for char in string:
        if char not in NON_ESCAPED_CHARS:
            return False

    # Any '%' characters must be valid '%xx' escape sequences.
    return string.count("%") == len(PERCENT_ENCODED_REGEX.findall(string))
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def is_safe(string: str, safe: str = "/") -> bool:
    """
    Determine if a given string is already quote-safe.
    """
    NON_ESCAPED_CHARS = UNRESERVED_CHARACTERS + safe + "%"

    # All characters must already be non-escaping or '%'
    for char in string:
        if char not in NON_ESCAPED_CHARS:
            return False

    return True
```

### 🔹 函式: `quote()`
- **變更前簽章 (Before)**: `def quote(string: str, safe: str = "/") -> str` (L439~L449)
- **變更後簽章 (After)**: `def quote(string: str, safe: str = "/") -> str` (L449~L479)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def quote(string: str, safe: str = "/") -> str:
    """
    Use percent-encoding to quote a string if required.
    """
    if is_safe(string, safe=safe):
        return string

    NON_ESCAPED_CHARS = UNRESERVED_CHARACTERS + safe
    return "".join(
        [char if char in NON_ESCAPED_CHARS else percent_encode(char) for char in string]
    )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def quote(string: str, safe: str = "/") -> str:
    """
    Use percent-encoding to quote a string, omitting existing '%xx' escape sequences.

    See: https://www.rfc-editor.org/rfc/rfc3986#section-2.1

    * `string`: The string to be percent-escaped.
    * `safe`: A string containing characters that may be treated as safe, and do not
        need to be escaped. Unreserved characters are always treated as safe.
        See: https://www.rfc-editor.org/rfc/rfc3986#section-2.3
    """
    parts = []
    current_position = 0
    for match in re.finditer(PERCENT_ENCODED_REGEX, string):
        start_position, end_position = match.start(), match.end()
        matched_text = match.group(0)
        # Add any text up to the '%xx' escape sequence.
        if start_position != current_position:
            leading_text = string[current_position:start_position]
            parts.append(percent_encoded(leading_text, safe=safe))

        # Add the '%xx' escape sequence.
        parts.append(matched_text)
        current_position = end_position

    # Add any text after the final '%xx' escape sequence.
    if current_position != len(string):
        trailing_text = string[current_position:]
        parts.append(percent_encoded(trailing_text, safe=safe))

    return "".join(parts)
```


---

### 🔹 Commit #09: `3b9060ee`
- **完整 Hash**: `3b9060ee1121b48669e0b30045c9344065f4f2ae`
- **說明 (Ground Truth)**: Fix environment proxies (#2741)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_utils.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:67, E:47, A:0) ➔ After(N:67, E:47, A:0)
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

### 🔹 函式: `get_environment_proxies()`
- **變更前簽章 (Before)**: `def get_environment_proxies() -> typing.Dict[str, typing.Optional[str]]` (L195~L239)
- **變更後簽章 (After)**: `def get_environment_proxies() -> typing.Dict[str, typing.Optional[str]]` (L195~L241)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def get_environment_proxies() -> typing.Dict[str, typing.Optional[str]]:
    """Gets proxy information from the environment"""

    # urllib.request.getproxies() falls back on System
    # Registry and Config for proxies on Windows and macOS.
    # We don't want to propagate non-HTTP proxies into
    # our configuration such as 'TRAVIS_APT_PROXY'.
    proxy_info = getproxies()
    mounts: typing.Dict[str, typing.Optional[str]] = {}

    for scheme in ("http", "https", "all"):
        if proxy_info.get(scheme):
            hostname = proxy_info[scheme]
            mounts[f"{scheme}://"] = (
                hostname if "://" in hostname else f"http://{hostname}"
            )

    no_proxy_hosts = [host.strip() for host in proxy_info.get("no", "").split(",")]
    for hostname in no_proxy_hosts:
        # See https://curl.haxx.se/libcurl/c/CURLOPT_NOPROXY.html for details
        # on how names in `NO_PROXY` are handled.
        if hostname == "*":
            # If NO_PROXY=* is used or if "*" occurs as any one of the comma
            # separated hostnames, then we should just bypass any information
            # from HTTP_PROXY, HTTPS_PROXY, ALL_PROXY, and always ignore
            # proxies.
            return {}
        elif hostname:
            # NO_PROXY=.google.com is marked as "all://*.google.com,
            #   which disables "www.google.com" but not "google.com"
            # NO_PROXY=google.com is marked as "all://*google.com,
            #   which disables "www.google.com" and "google.com".
            #   (But not "wwwgoogle.com")
            # NO_PROXY can include domains, IPv6, IPv4 addresses and "localhost"
            #   NO_PROXY=example.com,::1,localhost,192.168.0.0/16
            if is_ipv4_hostname(hostname):
                mounts[f"all://{hostname}"] = None
            elif is_ipv6_hostname(hostname):
                mounts[f"all://[{hostname}]"] = None
            elif hostname.lower() == "localhost":
                mounts[f"all://{hostname}"] = None
            else:
                mounts[f"all://*{hostname}"] = None

    return mounts
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def get_environment_proxies() -> typing.Dict[str, typing.Optional[str]]:
    """Gets proxy information from the environment"""

    # urllib.request.getproxies() falls back on System
    # Registry and Config for proxies on Windows and macOS.
    # We don't want to propagate non-HTTP proxies into
    # our configuration such as 'TRAVIS_APT_PROXY'.
    proxy_info = getproxies()
    mounts: typing.Dict[str, typing.Optional[str]] = {}

    for scheme in ("http", "https", "all"):
        if proxy_info.get(scheme):
            hostname = proxy_info[scheme]
            mounts[f"{scheme}://"] = (
                hostname if "://" in hostname else f"http://{hostname}"
            )

    no_proxy_hosts = [host.strip() for host in proxy_info.get("no", "").split(",")]
    for hostname in no_proxy_hosts:
        # See https://curl.haxx.se/libcurl/c/CURLOPT_NOPROXY.html for details
        # on how names in `NO_PROXY` are handled.
        if hostname == "*":
            # If NO_PROXY=* is used or if "*" occurs as any one of the comma
            # separated hostnames, then we should just bypass any information
            # from HTTP_PROXY, HTTPS_PROXY, ALL_PROXY, and always ignore
            # proxies.
            return {}
        elif hostname:
            # NO_PROXY=.google.com is marked as "all://*.google.com,
            #   which disables "www.google.com" but not "google.com"
            # NO_PROXY=google.com is marked as "all://*google.com,
            #   which disables "www.google.com" and "google.com".
            #   (But not "wwwgoogle.com")
            # NO_PROXY can include domains, IPv6, IPv4 addresses and "localhost"
            #   NO_PROXY=example.com,::1,localhost,192.168.0.0/16
            if "://" in hostname:
                mounts[hostname] = None
            elif is_ipv4_hostname(hostname):
                mounts[f"all://{hostname}"] = None
            elif is_ipv6_hostname(hostname):
                mounts[f"all://[{hostname}]"] = None
            elif hostname.lower() == "localhost":
                mounts[f"all://{hostname}"] = None
            else:
                mounts[f"all://*{hostname}"] = None

    return mounts
```


---

### 🔹 Commit #10: `1d73150c`
- **完整 Hash**: `1d73150c1f663757d63585aecfcb329d0ec00825`
- **說明 (Ground Truth)**: Cleanup response.json() method (#2911)
- **變更檔案數**: 2

#### 📄 檔案: `httpx/_models.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:145, E:182, A:0) ➔ After(N:144, E:180, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 0, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `guess_json_utf (External/Unresolved)` (FUNCTION_DEF)
  • - [移除呼叫邊] `Response.json` ──[CALLS]──> `guess_json_utf (External/Unresolved)`
  • - [移除呼叫邊] `Response.json` ──[CALLS]──> `decode (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Response.json()`
- **變更前簽章 (Before)**: `def json(self, **kwargs: typing.Any) -> typing.Any` (L761~L766)
- **變更後簽章 (After)**: `def json(self, **kwargs: typing.Any) -> typing.Any` (L760~L761)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def json(self, **kwargs: typing.Any) -> typing.Any:
        if self.charset_encoding is None and self.content and len(self.content) > 3:
            encoding = guess_json_utf(self.content)
            if encoding is not None:
                return jsonlib.loads(self.content.decode(encoding), **kwargs)
        return jsonlib.loads(self.text, **kwargs)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def json(self, **kwargs: typing.Any) -> typing.Any:
        return jsonlib.loads(self.content, **kwargs)
```


#### 📄 檔案: `httpx/_utils.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:69, E:48, A:0) ➔ After(N:67, E:47, A:0)
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
  • - [移除節點] `count (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `guess_json_utf` (FUNCTION_DEF)
  • - [移除呼叫邊] `guess_json_utf` ──[CALLS]──> `count (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #11: `e63b6594`
- **完整 Hash**: `e63b6594f2863b7c8274eb0991ebc6cad63661f7`
- **說明 (Ground Truth)**: Fix encode host (#2886)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_urlparse.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:31, E:34, A:0) ➔ After(N:31, E:34, A:0)
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

### 🔹 Commit #12: `301b8fb0`
- **完整 Hash**: `301b8fb03a81447c5b5ab1ca991202e10826fbda`
- **說明 (Ground Truth)**: Fix URLPattern examples (#2740)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_utils.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:69, E:48, A:0) ➔ After(N:69, E:48, A:0)
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

### 🔹 Commit #13: `a682f6f1`
- **完整 Hash**: `a682f6f1c7f1c5e10c66ae5bef139aea37ef0c4e`
- **說明 (Ground Truth)**: Fix exception suppression in asgi transport (#2669)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_transports/asgi.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:16, E:12, A:0) ➔ After(N:16, E:13, A:0)
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
  • + [新增呼叫邊] `ASGITransport.handle_async_request` ──[CALLS]──> `set (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `ASGITransport.handle_async_request()`
- **變更前簽章 (Before)**: `async def handle_async_request( self, request: Request, ) -> Response` (L91~L173)
- **變更後簽章 (After)**: `async def handle_async_request( self, request: Request, ) -> Response` (L91~L179)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def handle_async_request(
        self,
        request: Request,
    ) -> Response:
        assert isinstance(request.stream, AsyncByteStream)

        # ASGI scope.
        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": request.method,
            "headers": [(k.lower(), v) for (k, v) in request.headers.raw],
            "scheme": request.url.scheme,
            "path": request.url.path,
            "raw_path": request.url.raw_path,
            "query_string": request.url.query,
            "server": (request.url.host, request.url.port),
            "client": self.client,
            "root_path": self.root_path,
        }

        # Request.
        request_body_chunks = request.stream.__aiter__()
        request_complete = False

        # Response.
        status_code = None
        response_headers = None
        body_parts = []
        response_started = False
        response_complete = create_event()

        # ASGI callables.

        async def receive() -> typing.Dict[str, typing.Any]:
            nonlocal request_complete

            if request_complete:
                await response_complete.wait()
                return {"type": "http.disconnect"}

            try:
                body = await request_body_chunks.__anext__()
            except StopAsyncIteration:
                request_complete = True
                return {"type": "http.request", "body": b"", "more_body": False}
            return {"type": "http.request", "body": body, "more_body": True}

        async def send(message: typing.Dict[str, typing.Any]) -> None:
            nonlocal status_code, response_headers, response_started

            if message["type"] == "http.response.start":
                assert not response_started

                status_code = message["status"]
                response_headers = message.get("headers", [])
                response_started = True

            elif message["type"] == "http.response.body":
                assert not response_complete.is_set()
                body = message.get("body", b"")
                more_body = message.get("more_body", False)

                if body and request.method != "HEAD":
                    body_parts.append(body)

                if not more_body:
                    response_complete.set()

        try:
            await self.app(scope, receive, send)
        except Exception:  # noqa: PIE-786
            if self.raise_app_exceptions or not response_complete.is_set():
                raise

        assert response_complete.is_set()
        assert status_code is not None
        assert response_headers is not None

        stream = ASGIResponseStream(body_parts)

        return Response(status_code, headers=response_headers, stream=stream)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def handle_async_request(
        self,
        request: Request,
    ) -> Response:
        assert isinstance(request.stream, AsyncByteStream)

        # ASGI scope.
        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": request.method,
            "headers": [(k.lower(), v) for (k, v) in request.headers.raw],
            "scheme": request.url.scheme,
            "path": request.url.path,
            "raw_path": request.url.raw_path,
            "query_string": request.url.query,
            "server": (request.url.host, request.url.port),
            "client": self.client,
            "root_path": self.root_path,
        }

        # Request.
        request_body_chunks = request.stream.__aiter__()
        request_complete = False

        # Response.
        status_code = None
        response_headers = None
        body_parts = []
        response_started = False
        response_complete = create_event()

        # ASGI callables.

        async def receive() -> typing.Dict[str, typing.Any]:
            nonlocal request_complete

            if request_complete:
                await response_complete.wait()
                return {"type": "http.disconnect"}

            try:
                body = await request_body_chunks.__anext__()
            except StopAsyncIteration:
                request_complete = True
                return {"type": "http.request", "body": b"", "more_body": False}
            return {"type": "http.request", "body": body, "more_body": True}

        async def send(message: typing.Dict[str, typing.Any]) -> None:
            nonlocal status_code, response_headers, response_started

            if message["type"] == "http.response.start":
                assert not response_started

                status_code = message["status"]
                response_headers = message.get("headers", [])
                response_started = True

            elif message["type"] == "http.response.body":
                assert not response_complete.is_set()
                body = message.get("body", b"")
                more_body = message.get("more_body", False)

                if body and request.method != "HEAD":
                    body_parts.append(body)

                if not more_body:
                    response_complete.set()

        try:
            await self.app(scope, receive, send)
        except Exception:  # noqa: PIE-786
            if self.raise_app_exceptions:
                raise

            response_complete.set()
            if status_code is None:
                status_code = 500
            if response_headers is None:
                response_headers = {}

        assert response_complete.is_set()
        assert status_code is not None
        assert response_headers is not None

        stream = ASGIResponseStream(body_parts)

        return Response(status_code, headers=response_headers, stream=stream)
```


---

### 🔹 Commit #14: `ee432c0d`
- **完整 Hash**: `ee432c0d3098375df258b6d5844e7569080b2369`
- **說明 (Ground Truth)**: Fix for gen-delims escaping behaviour in path/query/fragment (#2701)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_urlparse.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:31, E:34, A:0) ➔ After(N:31, E:34, A:0)
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

### 🔹 函式: `urlparse()`
- **變更前簽章 (Before)**: `def urlparse(url: str = "", **kwargs: typing.Optional[str]) -> ParseResult: # Initial basic checks on allowable URLs. # --------------------------------------- # Hard limit the maximum allowable URL length.` (L149~L274)
- **變更後簽章 (After)**: `def urlparse(url: str = "", **kwargs: typing.Optional[str]) -> ParseResult: # Initial basic checks on allowable URLs. # --------------------------------------- # Hard limit the maximum allowable URL length.` (L149~L281)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def urlparse(url: str = "", **kwargs: typing.Optional[str]) -> ParseResult:
    # Initial basic checks on allowable URLs.
    # ---------------------------------------

    # Hard limit the maximum allowable URL length.
    if len(url) > MAX_URL_LENGTH:
        raise InvalidURL("URL too long")

    # If a URL includes any ASCII control characters including \t, \r, \n,
    # then treat it as invalid.
    if any(char.isascii() and not char.isprintable() for char in url):
        raise InvalidURL("Invalid non-printable ASCII character in URL")

    # Some keyword arguments require special handling.
    # ------------------------------------------------

    # Coerce "port" to a string, if it is provided as an integer.
    if "port" in kwargs:
        port = kwargs["port"]
        kwargs["port"] = str(port) if isinstance(port, int) else port

    # Replace "netloc" with "host and "port".
    if "netloc" in kwargs:
        netloc = kwargs.pop("netloc") or ""
        kwargs["host"], _, kwargs["port"] = netloc.partition(":")

    # Replace "username" and/or "password" with "userinfo".
    if "username" in kwargs or "password" in kwargs:
        username = quote(kwargs.pop("username", "") or "")
        password = quote(kwargs.pop("password", "") or "")
        kwargs["userinfo"] = f"{username}:{password}" if password else username

    # Replace "raw_path" with "path" and "query".
    if "raw_path" in kwargs:
        raw_path = kwargs.pop("raw_path") or ""
        kwargs["path"], seperator, kwargs["query"] = raw_path.partition("?")
        if not seperator:
            kwargs["query"] = None

    # Ensure that IPv6 "host" addresses are always escaped with "[...]".
    if "host" in kwargs:
        host = kwargs.get("host") or ""
        if ":" in host and not (host.startswith("[") and host.endswith("]")):
            kwargs["host"] = f"[{host}]"

    # If any keyword arguments are provided, ensure they are valid.
    # -------------------------------------------------------------

    for key, value in kwargs.items():
        if value is not None:
            if len(value) > MAX_URL_LENGTH:
                raise InvalidURL(f"URL component '{key}' too long")

            # If a component includes any ASCII control characters including \t, \r, \n,
            # then treat it as invalid.
            if any(char.isascii() and not char.isprintable() for char in value):
                raise InvalidURL(
                    f"Invalid non-printable ASCII character in URL component '{key}'"
                )

            # Ensure that keyword arguments match as a valid regex.
            if not COMPONENT_REGEX[key].fullmatch(value):
                raise InvalidURL(f"Invalid URL component '{key}'")

    # The URL_REGEX will always match, but may have empty components.
    url_match = URL_REGEX.match(url)
    assert url_match is not None
    url_dict = url_match.groupdict()

    # * 'scheme', 'authority', and 'path' may be empty strings.
    # * 'query' may be 'None', indicating no trailing "?" portion.
    #   Any string including the empty string, indicates a trailing "?".
    # * 'fragment' may be 'None', indicating no trailing "#" portion.
    #   Any string including the empty string, indicates a trailing "#".
    scheme = kwargs.get("scheme", url_dict["scheme"]) or ""
    authority = kwargs.get("authority", url_dict["authority"]) or ""
    path = kwargs.get("path", url_dict["path"]) or ""
    query = kwargs.get("query", url_dict["query"])
    fragment = kwargs.get("fragment", url_dict["fragment"])

    # The AUTHORITY_REGEX will always match, but may have empty components.
    authority_match = AUTHORITY_REGEX.match(authority)
    assert authority_match is not None
    authority_dict = authority_match.groupdict()

    # * 'userinfo' and 'host' may be empty strings.
    # * 'port' may be 'None'.
    userinfo = kwargs.get("userinfo", authority_dict["userinfo"]) or ""
    host = kwargs.get("host", authority_dict["host"]) or ""
    port = kwargs.get("port", authority_dict["port"])

    # Normalize and validate each component.
    # We end up with a parsed representation of the URL,
    # with components that are plain ASCII bytestrings.
    parsed_scheme: str = scheme.lower()
    parsed_userinfo: str = quote(userinfo, safe=SUB_DELIMS + ":")
    parsed_host: str = encode_host(host)
    parsed_port: typing.Optional[int] = normalize_port(port, scheme)

    has_scheme = parsed_scheme != ""
    has_authority = (
        parsed_userinfo != "" or parsed_host != "" or parsed_port is not None
    )
    validate_path(path, has_scheme=has_scheme, has_authority=has_authority)
    if has_authority:
        path = normalize_path(path)

    parsed_path: str = quote(path, safe=SUB_DELIMS + ":@/")
    parsed_query: typing.Optional[str] = (
        None if query is None else quote(query, safe=SUB_DELIMS + "/?")
    )
    parsed_fragment: typing.Optional[str] = (
        None if fragment is None else quote(fragment, safe=SUB_DELIMS + "/?")
    )

    # The parsed ASCII bytestrings are our canonical form.
    # All properties of the URL are derived from these.
    return ParseResult(
        parsed_scheme,
        parsed_userinfo,
        parsed_host,
        parsed_port,
        parsed_path,
        parsed_query,
        parsed_fragment,
    )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def urlparse(url: str = "", **kwargs: typing.Optional[str]) -> ParseResult:
    # Initial basic checks on allowable URLs.
    # ---------------------------------------

    # Hard limit the maximum allowable URL length.
    if len(url) > MAX_URL_LENGTH:
        raise InvalidURL("URL too long")

    # If a URL includes any ASCII control characters including \t, \r, \n,
    # then treat it as invalid.
    if any(char.isascii() and not char.isprintable() for char in url):
        raise InvalidURL("Invalid non-printable ASCII character in URL")

    # Some keyword arguments require special handling.
    # ------------------------------------------------

    # Coerce "port" to a string, if it is provided as an integer.
    if "port" in kwargs:
        port = kwargs["port"]
        kwargs["port"] = str(port) if isinstance(port, int) else port

    # Replace "netloc" with "host and "port".
    if "netloc" in kwargs:
        netloc = kwargs.pop("netloc") or ""
        kwargs["host"], _, kwargs["port"] = netloc.partition(":")

    # Replace "username" and/or "password" with "userinfo".
    if "username" in kwargs or "password" in kwargs:
        username = quote(kwargs.pop("username", "") or "")
        password = quote(kwargs.pop("password", "") or "")
        kwargs["userinfo"] = f"{username}:{password}" if password else username

    # Replace "raw_path" with "path" and "query".
    if "raw_path" in kwargs:
        raw_path = kwargs.pop("raw_path") or ""
        kwargs["path"], seperator, kwargs["query"] = raw_path.partition("?")
        if not seperator:
            kwargs["query"] = None

    # Ensure that IPv6 "host" addresses are always escaped with "[...]".
    if "host" in kwargs:
        host = kwargs.get("host") or ""
        if ":" in host and not (host.startswith("[") and host.endswith("]")):
            kwargs["host"] = f"[{host}]"

    # If any keyword arguments are provided, ensure they are valid.
    # -------------------------------------------------------------

    for key, value in kwargs.items():
        if value is not None:
            if len(value) > MAX_URL_LENGTH:
                raise InvalidURL(f"URL component '{key}' too long")

            # If a component includes any ASCII control characters including \t, \r, \n,
            # then treat it as invalid.
            if any(char.isascii() and not char.isprintable() for char in value):
                raise InvalidURL(
                    f"Invalid non-printable ASCII character in URL component '{key}'"
                )

            # Ensure that keyword arguments match as a valid regex.
            if not COMPONENT_REGEX[key].fullmatch(value):
                raise InvalidURL(f"Invalid URL component '{key}'")

    # The URL_REGEX will always match, but may have empty components.
    url_match = URL_REGEX.match(url)
    assert url_match is not None
    url_dict = url_match.groupdict()

    # * 'scheme', 'authority', and 'path' may be empty strings.
    # * 'query' may be 'None', indicating no trailing "?" portion.
    #   Any string including the empty string, indicates a trailing "?".
    # * 'fragment' may be 'None', indicating no trailing "#" portion.
    #   Any string including the empty string, indicates a trailing "#".
    scheme = kwargs.get("scheme", url_dict["scheme"]) or ""
    authority = kwargs.get("authority", url_dict["authority"]) or ""
    path = kwargs.get("path", url_dict["path"]) or ""
    query = kwargs.get("query", url_dict["query"])
    fragment = kwargs.get("fragment", url_dict["fragment"])

    # The AUTHORITY_REGEX will always match, but may have empty components.
    authority_match = AUTHORITY_REGEX.match(authority)
    assert authority_match is not None
    authority_dict = authority_match.groupdict()

    # * 'userinfo' and 'host' may be empty strings.
    # * 'port' may be 'None'.
    userinfo = kwargs.get("userinfo", authority_dict["userinfo"]) or ""
    host = kwargs.get("host", authority_dict["host"]) or ""
    port = kwargs.get("port", authority_dict["port"])

    # Normalize and validate each component.
    # We end up with a parsed representation of the URL,
    # with components that are plain ASCII bytestrings.
    parsed_scheme: str = scheme.lower()
    parsed_userinfo: str = quote(userinfo, safe=SUB_DELIMS + ":")
    parsed_host: str = encode_host(host)
    parsed_port: typing.Optional[int] = normalize_port(port, scheme)

    has_scheme = parsed_scheme != ""
    has_authority = (
        parsed_userinfo != "" or parsed_host != "" or parsed_port is not None
    )
    validate_path(path, has_scheme=has_scheme, has_authority=has_authority)
    if has_authority:
        path = normalize_path(path)

    # The GEN_DELIMS set is... : / ? # [ ] @
    # These do not need to be percent-quoted unless they serve as delimiters for the
    # specific component.

    # For 'path' we need to drop ? and # from the GEN_DELIMS set.
    parsed_path: str = quote(path, safe=SUB_DELIMS + ":/[]@")
    # For 'query' we need to drop '#' from the GEN_DELIMS set.
    parsed_query: typing.Optional[str] = (
        None if query is None else quote(query, safe=SUB_DELIMS + ":/?[]@")
    )
    # For 'fragment' we can include all of the GEN_DELIMS set.
    parsed_fragment: typing.Optional[str] = (
        None if fragment is None else quote(fragment, safe=SUB_DELIMS + ":/?#[]@")
    )

    # The parsed ASCII bytestrings are our canonical form.
    # All properties of the URL are derived from these.
    return ParseResult(
        parsed_scheme,
        parsed_userinfo,
        parsed_host,
        parsed_port,
        parsed_path,
        parsed_query,
        parsed_fragment,
    )
```


---

### 🔹 Commit #15: `32e25497`
- **完整 Hash**: `32e25497a36e6222cc64a758c98275b450dac28d`
- **說明 (Ground Truth)**: Fix ruff error and script (#2680)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_utils.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:69, E:48, A:0) ➔ After(N:69, E:48, A:0)
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

### 🔹 函式: `is_ipv6_hostname()`
- **變更前簽章 (Before)**: `def is_ipv6_hostname(hostname: str) -> bool` (L472~L477)
- **變更後簽章 (After)**: `def is_ipv6_hostname(hostname: str) -> bool` (L472~L477)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def is_ipv6_hostname(hostname: str) -> bool:
    try:
        ipaddress.IPv6Address(hostname.split("/")[0])
    except:
        return False
    return True
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def is_ipv6_hostname(hostname: str) -> bool:
    try:
        ipaddress.IPv6Address(hostname.split("/")[0])
    except Exception:
        return False
    return True
```

### 🔹 函式: `is_ipv4_hostname()`
- **變更前簽章 (Before)**: `def is_ipv4_hostname(hostname: str) -> bool` (L464~L469)
- **變更後簽章 (After)**: `def is_ipv4_hostname(hostname: str) -> bool` (L464~L469)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def is_ipv4_hostname(hostname: str) -> bool:
    try:
        ipaddress.IPv4Address(hostname.split("/")[0])
    except:
        return False
    return True
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def is_ipv4_hostname(hostname: str) -> bool:
    try:
        ipaddress.IPv4Address(hostname.split("/")[0])
    except Exception:
        return False
    return True
```


---

### 🔹 Commit #16: `9ae170a9`
- **完整 Hash**: `9ae170a936df39f42a6ddf8eb2c27026e20bea7e`
- **說明 (Ground Truth)**: Fix optional percent encoding behaviour. (#2671)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_urlparse.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:30, E:33, A:0) ➔ After(N:31, E:34, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 3, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `is_safe` (FUNCTION_DEF)
  • + [新增呼叫邊] `is_safe` ──[CALLS]──> `count (External/Unresolved)`
  • + [新增呼叫邊] `is_safe` ──[CALLS]──> `findall (External/Unresolved)`
  • + [新增呼叫邊] `quote` ──[CALLS]──> `is_safe`
  • - [移除呼叫邊] `quote` ──[CALLS]──> `count (External/Unresolved)`
  • - [移除呼叫邊] `quote` ──[CALLS]──> `findall (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `quote()`
- **變更前簽章 (Before)**: `def quote(string: str, safe: str = "/") -> str` (L414~L423)
- **變更後簽章 (After)**: `def quote(string: str, safe: str = "/") -> str` (L429~L439)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def quote(string: str, safe: str = "/") -> str:
    NON_ESCAPED_CHARS = UNRESERVED_CHARACTERS + safe
    if string.count("%") == len(PERCENT_ENCODED_REGEX.findall(string)):
        # If all occurances of '%' are valid '%xx' escapes, then treat
        # percent as a non-escaping character.
        NON_ESCAPED_CHARS += "%"

    return "".join(
        [char if char in NON_ESCAPED_CHARS else percent_encode(char) for char in string]
    )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def quote(string: str, safe: str = "/") -> str:
    """
    Use percent-encoding to quote a string if required.
    """
    if is_safe(string, safe=safe):
        return string

    NON_ESCAPED_CHARS = UNRESERVED_CHARACTERS + safe
    return "".join(
        [char if char in NON_ESCAPED_CHARS else percent_encode(char) for char in string]
    )
```


---

### 🔹 Commit #17: `15d09a3b`
- **完整 Hash**: `15d09a3bbc20372cd87e48f17f7c9381c8220a0f`
- **說明 (Ground Truth)**: fix: NO_PROXY should support IPv4, IPv6 and localhost (#2659)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_utils.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:65, E:43, A:0) ➔ After(N:69, E:48, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 5, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `is_ipv6_hostname` (FUNCTION_DEF)
  • + [新增節點] `IPv4Address (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `is_ipv4_hostname` (FUNCTION_DEF)
  • + [新增節點] `IPv6Address (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `get_environment_proxies` ──[CALLS]──> `is_ipv4_hostname`
  • + [新增呼叫邊] `get_environment_proxies` ──[CALLS]──> `is_ipv6_hostname`
  • + [新增呼叫邊] `get_environment_proxies` ──[CALLS]──> `lower (External/Unresolved)`
  • + [新增呼叫邊] `is_ipv4_hostname` ──[CALLS]──> `IPv4Address (External/Unresolved)`
  • + [新增呼叫邊] `is_ipv6_hostname` ──[CALLS]──> `IPv6Address (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `get_environment_proxies()`
- **變更前簽章 (Before)**: `def get_environment_proxies() -> typing.Dict[str, typing.Optional[str]]` (L229~L264)
- **變更後簽章 (After)**: `def get_environment_proxies() -> typing.Dict[str, typing.Optional[str]]` (L230~L274)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def get_environment_proxies() -> typing.Dict[str, typing.Optional[str]]:
    """Gets proxy information from the environment"""

    # urllib.request.getproxies() falls back on System
    # Registry and Config for proxies on Windows and macOS.
    # We don't want to propagate non-HTTP proxies into
    # our configuration such as 'TRAVIS_APT_PROXY'.
    proxy_info = getproxies()
    mounts: typing.Dict[str, typing.Optional[str]] = {}

    for scheme in ("http", "https", "all"):
        if proxy_info.get(scheme):
            hostname = proxy_info[scheme]
            mounts[f"{scheme}://"] = (
                hostname if "://" in hostname else f"http://{hostname}"
            )

    no_proxy_hosts = [host.strip() for host in proxy_info.get("no", "").split(",")]
    for hostname in no_proxy_hosts:
        # See https://curl.haxx.se/libcurl/c/CURLOPT_NOPROXY.html for details
        # on how names in `NO_PROXY` are handled.
        if hostname == "*":
            # If NO_PROXY=* is used or if "*" occurs as any one of the comma
            # separated hostnames, then we should just bypass any information
            # from HTTP_PROXY, HTTPS_PROXY, ALL_PROXY, and always ignore
            # proxies.
            return {}
        elif hostname:
            # NO_PROXY=.google.com is marked as "all://*.google.com,
            #   which disables "www.google.com" but not "google.com"
            # NO_PROXY=google.com is marked as "all://*google.com,
            #   which disables "www.google.com" and "google.com".
            #   (But not "wwwgoogle.com")
            mounts[f"all://*{hostname}"] = None

    return mounts
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def get_environment_proxies() -> typing.Dict[str, typing.Optional[str]]:
    """Gets proxy information from the environment"""

    # urllib.request.getproxies() falls back on System
    # Registry and Config for proxies on Windows and macOS.
    # We don't want to propagate non-HTTP proxies into
    # our configuration such as 'TRAVIS_APT_PROXY'.
    proxy_info = getproxies()
    mounts: typing.Dict[str, typing.Optional[str]] = {}

    for scheme in ("http", "https", "all"):
        if proxy_info.get(scheme):
            hostname = proxy_info[scheme]
            mounts[f"{scheme}://"] = (
                hostname if "://" in hostname else f"http://{hostname}"
            )

    no_proxy_hosts = [host.strip() for host in proxy_info.get("no", "").split(",")]
    for hostname in no_proxy_hosts:
        # See https://curl.haxx.se/libcurl/c/CURLOPT_NOPROXY.html for details
        # on how names in `NO_PROXY` are handled.
        if hostname == "*":
            # If NO_PROXY=* is used or if "*" occurs as any one of the comma
            # separated hostnames, then we should just bypass any information
            # from HTTP_PROXY, HTTPS_PROXY, ALL_PROXY, and always ignore
            # proxies.
            return {}
        elif hostname:
            # NO_PROXY=.google.com is marked as "all://*.google.com,
            #   which disables "www.google.com" but not "google.com"
            # NO_PROXY=google.com is marked as "all://*google.com,
            #   which disables "www.google.com" and "google.com".
            #   (But not "wwwgoogle.com")
            # NO_PROXY can include domains, IPv6, IPv4 addresses and "localhost"
            #   NO_PROXY=example.com,::1,localhost,192.168.0.0/16
            if is_ipv4_hostname(hostname):
                mounts[f"all://{hostname}"] = None
            elif is_ipv6_hostname(hostname):
                mounts[f"all://[{hostname}]"] = None
            elif hostname.lower() == "localhost":
                mounts[f"all://{hostname}"] = None
            else:
                mounts[f"all://*{hostname}"] = None

    return mounts
```


---

### 🔹 Commit #18: `f0fd9192`
- **完整 Hash**: `f0fd91925bc8663b4ec3635c302aa07fe5f8e72e`
- **說明 (Ground Truth)**: fix type annotation for MockTransport (#2581)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_transports/mock.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:6, E:4, A:0) ➔ After(N:6, E:4, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 1, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `TypeError (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `iscoroutine (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `MockTransport.handle_request` ──[CALLS]──> `TypeError (External/Unresolved)`
  • - [移除呼叫邊] `MockTransport.handle_async_request` ──[CALLS]──> `iscoroutine (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `MockTransport.handle_async_request()`
- **變更前簽章 (Before)**: `async def handle_async_request( self, request: Request, ) -> Response` (L19~L34)
- **變更後簽章 (After)**: `async def handle_async_request( self, request: Request, ) -> Response` (L24~L38)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def handle_async_request(
        self,
        request: Request,
    ) -> Response:
        await request.aread()
        response = self.handler(request)

        # Allow handler to *optionally* be an `async` function.
        # If it is, then the `response` variable need to be awaited to actually
        # return the result.

        # https://simonwillison.net/2020/Sep/2/await-me-maybe/
        if asyncio.iscoroutine(response):
            response = await response

        return response
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def handle_async_request(
        self,
        request: Request,
    ) -> Response:
        await request.aread()
        response = self.handler(request)

        # Allow handler to *optionally* be an `async` function.
        # If it is, then the `response` variable need to be awaited to actually
        # return the result.

        if not isinstance(response, Response):
            response = await response

        return response
```

### 🔹 函式: `MockTransport.handle_request()`
- **變更前簽章 (Before)**: `def handle_request( self, request: Request, ) -> Response` (L12~L17)
- **變更後簽章 (After)**: `def handle_request( self, request: Request, ) -> Response` (L14~L22)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def handle_request(
        self,
        request: Request,
    ) -> Response:
        request.read()
        return self.handler(request)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def handle_request(
        self,
        request: Request,
    ) -> Response:
        request.read()
        response = self.handler(request)
        if not isinstance(response, Response):  # pragma: no cover
            raise TypeError("Cannot use an async handler in a sync Client")
        return response
```


---

### 🔹 Commit #19: `1ff67ea4`
- **完整 Hash**: `1ff67ea47cd436fd2a835d00bcc830310ff9a0cd`
- **說明 (Ground Truth)**: Typing: use wsgiref.types to validate types and fix issues uncovered (#2467)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_transports/wsgi.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:17, E:11, A:0) ➔ After(N:18, E:11, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `TypeVar (External/Unresolved)` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_skip_leading_empty_chunks()`
- **變更前簽章 (Before)**: `def _skip_leading_empty_chunks(body: typing.Iterable[bytes]) -> typing.Iterable[bytes]` (L11~L16)
- **變更後簽章 (After)**: `def _skip_leading_empty_chunks(body: typing.Iterable[_T]) -> typing.Iterable[_T]` (L28~L33)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _skip_leading_empty_chunks(body: typing.Iterable[bytes]) -> typing.Iterable[bytes]:
    body = iter(body)
    for chunk in body:
        if chunk:
            return itertools.chain([chunk], body)
    return []
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _skip_leading_empty_chunks(body: typing.Iterable[_T]) -> typing.Iterable[_T]:
    body = iter(body)
    for chunk in body:
        if chunk:
            return itertools.chain([chunk], body)
    return []
```

### 🔹 函式: `WSGITransport.handle_request()`
- **變更前簽章 (Before)**: `def handle_request(self, request: Request) -> Response` (L80~L136)
- **變更後簽章 (After)**: `def handle_request(self, request: Request) -> Response` (L97~L154)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def handle_request(self, request: Request) -> Response:
        request.read()
        wsgi_input = io.BytesIO(request.content)

        port = request.url.port or {"http": 80, "https": 443}[request.url.scheme]
        environ = {
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": request.url.scheme,
            "wsgi.input": wsgi_input,
            "wsgi.errors": self.wsgi_errors or sys.stderr,
            "wsgi.multithread": True,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
            "REQUEST_METHOD": request.method,
            "SCRIPT_NAME": self.script_name,
            "PATH_INFO": request.url.path,
            "QUERY_STRING": request.url.query.decode("ascii"),
            "SERVER_NAME": request.url.host,
            "SERVER_PORT": str(port),
            "REMOTE_ADDR": self.remote_addr,
        }
        for header_key, header_value in request.headers.raw:
            key = header_key.decode("ascii").upper().replace("-", "_")
            if key not in ("CONTENT_TYPE", "CONTENT_LENGTH"):
                key = "HTTP_" + key
            environ[key] = header_value.decode("ascii")

        seen_status = None
        seen_response_headers = None
        seen_exc_info = None

        def start_response(
            status: str,
            response_headers: typing.List[typing.Tuple[str, str]],
            exc_info: typing.Any = None,
        ) -> None:
            nonlocal seen_status, seen_response_headers, seen_exc_info
            seen_status = status
            seen_response_headers = response_headers
            seen_exc_info = exc_info

        result = self.app(environ, start_response)

        stream = WSGIByteStream(result)

        assert seen_status is not None
        assert seen_response_headers is not None
        if seen_exc_info and self.raise_app_exceptions:
            raise seen_exc_info[1]

        status_code = int(seen_status.split()[0])
        headers = [
            (key.encode("ascii"), value.encode("ascii"))
            for key, value in seen_response_headers
        ]

        return Response(status_code, headers=headers, stream=stream)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def handle_request(self, request: Request) -> Response:
        request.read()
        wsgi_input = io.BytesIO(request.content)

        port = request.url.port or {"http": 80, "https": 443}[request.url.scheme]
        environ = {
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": request.url.scheme,
            "wsgi.input": wsgi_input,
            "wsgi.errors": self.wsgi_errors or sys.stderr,
            "wsgi.multithread": True,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
            "REQUEST_METHOD": request.method,
            "SCRIPT_NAME": self.script_name,
            "PATH_INFO": request.url.path,
            "QUERY_STRING": request.url.query.decode("ascii"),
            "SERVER_NAME": request.url.host,
            "SERVER_PORT": str(port),
            "REMOTE_ADDR": self.remote_addr,
        }
        for header_key, header_value in request.headers.raw:
            key = header_key.decode("ascii").upper().replace("-", "_")
            if key not in ("CONTENT_TYPE", "CONTENT_LENGTH"):
                key = "HTTP_" + key
            environ[key] = header_value.decode("ascii")

        seen_status = None
        seen_response_headers = None
        seen_exc_info = None

        def start_response(
            status: str,
            response_headers: typing.List[typing.Tuple[str, str]],
            exc_info: typing.Optional[_OptExcInfo] = None,
        ) -> typing.Callable[[bytes], typing.Any]:
            nonlocal seen_status, seen_response_headers, seen_exc_info
            seen_status = status
            seen_response_headers = response_headers
            seen_exc_info = exc_info
            return lambda _: None

        result = self.app(environ, start_response)

        stream = WSGIByteStream(result)

        assert seen_status is not None
        assert seen_response_headers is not None
        if seen_exc_info and seen_exc_info[0] and self.raise_app_exceptions:
            raise seen_exc_info[1]

        status_code = int(seen_status.split()[0])
        headers = [
            (key.encode("ascii"), value.encode("ascii"))
            for key, value in seen_response_headers
        ]

        return Response(status_code, headers=headers, stream=stream)
```

### 🔹 函式: `WSGITransport.start_response()`
- **變更前簽章 (Before)**: `def start_response( status: str, response_headers: typing.List[typing.Tuple[str, str]], exc_info: typing.Any = None, ) -> None` (L111~L119)
- **變更後簽章 (After)**: `def start_response( status: str, response_headers: typing.List[typing.Tuple[str, str]], exc_info: typing.Optional[_OptExcInfo] = None, ) -> typing.Callable[[bytes], typing.Any]` (L128~L137)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def start_response(
            status: str,
            response_headers: typing.List[typing.Tuple[str, str]],
            exc_info: typing.Any = None,
        ) -> None:
            nonlocal seen_status, seen_response_headers, seen_exc_info
            seen_status = status
            seen_response_headers = response_headers
            seen_exc_info = exc_info
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def start_response(
            status: str,
            response_headers: typing.List[typing.Tuple[str, str]],
            exc_info: typing.Optional[_OptExcInfo] = None,
        ) -> typing.Callable[[bytes], typing.Any]:
            nonlocal seen_status, seen_response_headers, seen_exc_info
            seen_status = status
            seen_response_headers = response_headers
            seen_exc_info = exc_info
            return lambda _: None
```


---

### 🔹 Commit #20: `d5900cd4`
- **完整 Hash**: `d5900cd40ec85e47800e21e77bc684b9f65325ed`
- **說明 (Ground Truth)**: Fix empty query params (#2354)
- **變更檔案數**: 1

#### 📄 檔案: `httpx/_urls.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:75, E:71, A:0) ➔ After(N:75, E:71, A:0)
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

### 🔹 函式: `QueryParams.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, *args: typing.Optional[QueryParamTypes], **kwargs: typing.Any ) -> None` (L532~L571)
- **變更後簽章 (After)**: `def __init__( self, *args: typing.Optional[QueryParamTypes], **kwargs: typing.Any ) -> None` (L532~L571)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self, *args: typing.Optional[QueryParamTypes], **kwargs: typing.Any
    ) -> None:
        assert len(args) < 2, "Too many arguments."
        assert not (args and kwargs), "Cannot mix named and unnamed arguments."

        value = args[0] if args else kwargs

        items: typing.Sequence[typing.Tuple[str, PrimitiveData]]
        if value is None or isinstance(value, (str, bytes)):
            value = value.decode("ascii") if isinstance(value, bytes) else value
            self._dict = parse_qs(value)
        elif isinstance(value, QueryParams):
            self._dict = {k: list(v) for k, v in value._dict.items()}
        else:
            dict_value: typing.Dict[typing.Any, typing.List[typing.Any]] = {}
            if isinstance(value, (list, tuple)):
                # Convert list inputs like:
                #     [("a", "123"), ("a", "456"), ("b", "789")]
                # To a dict representation, like:
                #     {"a": ["123", "456"], "b": ["789"]}
                for item in value:
                    dict_value.setdefault(item[0], []).append(item[1])
            else:
                # Convert dict inputs like:
                #    {"a": "123", "b": ["456", "789"]}
                # To dict inputs where values are always lists, like:
                #    {"a": ["123"], "b": ["456", "789"]}
                dict_value = {
                    k: list(v) if isinstance(v, (list, tuple)) else [v]
                    for k, v in value.items()
                }

            # Ensure that keys and values are neatly coerced to strings.
            # We coerce values `True` and `False` to JSON-like "true" and "false"
            # representations, and coerce `None` values to the empty string.
            self._dict = {
                str(k): [primitive_value_to_str(item) for item in v]
                for k, v in dict_value.items()
            }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self, *args: typing.Optional[QueryParamTypes], **kwargs: typing.Any
    ) -> None:
        assert len(args) < 2, "Too many arguments."
        assert not (args and kwargs), "Cannot mix named and unnamed arguments."

        value = args[0] if args else kwargs

        items: typing.Sequence[typing.Tuple[str, PrimitiveData]]
        if value is None or isinstance(value, (str, bytes)):
            value = value.decode("ascii") if isinstance(value, bytes) else value
            self._dict = parse_qs(value, keep_blank_values=True)
        elif isinstance(value, QueryParams):
            self._dict = {k: list(v) for k, v in value._dict.items()}
        else:
            dict_value: typing.Dict[typing.Any, typing.List[typing.Any]] = {}
            if isinstance(value, (list, tuple)):
                # Convert list inputs like:
                #     [("a", "123"), ("a", "456"), ("b", "789")]
                # To a dict representation, like:
                #     {"a": ["123", "456"], "b": ["789"]}
                for item in value:
                    dict_value.setdefault(item[0], []).append(item[1])
            else:
                # Convert dict inputs like:
                #    {"a": "123", "b": ["456", "789"]}
                # To dict inputs where values are always lists, like:
                #    {"a": ["123"], "b": ["456", "789"]}
                dict_value = {
                    k: list(v) if isinstance(v, (list, tuple)) else [v]
                    for k, v in value.items()
                }

            # Ensure that keys and values are neatly coerced to strings.
            # We coerce values `True` and `False` to JSON-like "true" and "false"
            # representations, and coerce `None` values to the empty string.
            self._dict = {
                str(k): [primitive_value_to_str(item) for item in v]
                for k, v in dict_value.items()
            }
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/httpx show 89599a9541af14bcf906fc4ed58ccbdf403802ba
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 89599a9541af14bcf906fc4ed58ccbdf403802ba~1 --file test_repos/httpx/httpx/_config.py
   ```
