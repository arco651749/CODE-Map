# 🔬 CODE-Map 基準審查獨立驗證報告: `trpc`
> **技術生態**: `TypeScript (端到端型別 RPC / Proxy 路由)`  
> **本地倉庫路徑**: `test_repos/trpc`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 25 Files  
> **報告生成時間**: 2026-10-20 21:44:09  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `13` / `25` | `52.0%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `7` / `25` | `28.0%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `5` / `25` | `20.0%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`20` / `25`** | **`80.0%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `25` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `43b7afab`
- **完整 Hash**: `43b7afab8af3c202694d38a19f4a64131990c351`
- **說明 (Ground Truth)**: fix: remove duplicate words in code comments (#7399)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/src/adapters/aws-lambda/getPlanner.ts`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:20, E:8, A:0) ➔ After(N:20, E:8, A:0)
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

### 🔹 Commit #02: `90aba02d`
- **完整 Hash**: `90aba02dea96be9a15baa42453c07cfd968cc276`
- **說明 (Ground Truth)**: fix(server): stream the request body when express 5 body-parser leaves req.body undefined (#7447)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/src/adapters/node-http/incomingMessageToRequest.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:10, E:4, A:0) ➔ After(N:10, E:4, A:0)
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

### 🔹 函式: `createBody()`
- **變更前簽章 (Before)**: `function createBody(
  req: NodeHTTPRequest,
  opts:` (L6~L72)
- **變更後簽章 (After)**: `function createBody(
  req: NodeHTTPRequest,
  opts:` (L6~L79)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createBody(
  req: NodeHTTPRequest,
  opts: {
    /**
     * Max body size in bytes. If the body is larger than this, the request will be aborted
     */
    maxBodySize: number | null;
  },
): RequestInit['body'] {
  // Some adapters will pre-parse the body and add it to the request object
  if ('body' in req) {
    if (req.body === undefined) {
      // If body property exists but is undefined, return undefined
      return undefined;
    }
    // If the body is already a string, return it directly
    if (typeof req.body === 'string') {
      return req.body;
    }
    // formData use
    if (req.body instanceof IncomingMessage) {
      return req.body as any;
    }
    // If body exists but isn't a string, stringify it as JSON
    return JSON.stringify(req.body);
  }
  let size = 0;
  let hasClosed = false;

  return new ReadableStream({
    start(controller) {
      const onData = (chunk: Buffer) => {
        size += chunk.length;
        if (!opts.maxBodySize || size <= opts.maxBodySize) {
          controller.enqueue(
            new Uint8Array(chunk.buffer, chunk.byteOffset, chunk.byteLength),
          );
          return;
        }
        controller.error(
          new TRPCError({
            code: 'PAYLOAD_TOO_LARGE',
          }),
        );
        hasClosed = true;
        req.off('data', onData);
        req.off('end', onEnd);
      };

      const onEnd = () => {
        if (hasClosed) {
          return;
        }
        hasClosed = true;
        req.off('data', onData);
        req.off('end', onEnd);
        controller.close();
      };

      req.on('data', onData);
      req.on('end', onEnd);
    },
    cancel() {
      req.destroy();
    },
  });
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createBody(
  req: NodeHTTPRequest,
  opts: {
    /**
     * Max body size in bytes. If the body is larger than this, the request will be aborted
     */
    maxBodySize: number | null;
  },
): RequestInit['body'] {
  // Some adapters will pre-parse the body and add it to the request object
  if ('body' in req) {
    if (req.body !== undefined) {
      // If the body is already a string, return it directly
      if (typeof req.body === 'string') {
        return req.body;
      }
      // formData use
      if (req.body instanceof IncomingMessage) {
        return req.body as any;
      }
      // If body exists but isn't a string, stringify it as JSON
      return JSON.stringify(req.body);
    }
    if (req.readableEnded) {
      // The stream was consumed without producing a parsed body — there is
      // nothing left to read
      return undefined;
    }
    // The property was defined without the stream being read — e.g. express
    // 5's body-parser assigns `req.body = undefined` on content types it
    // skips (such as multipart/form-data) — so stream it like an unparsed
    // request
  }
  let size = 0;
  let hasClosed = false;

  return new ReadableStream({
    start(controller) {
      const onData = (chunk: Buffer) => {
        size += chunk.length;
        if (!opts.maxBodySize || size <= opts.maxBodySize) {
          controller.enqueue(
            new Uint8Array(chunk.buffer, chunk.byteOffset, chunk.byteLength),
          );
          return;
        }
        controller.error(
          new TRPCError({
            code: 'PAYLOAD_TOO_LARGE',
          }),
        );
        hasClosed = true;
        req.off('data', onData);
        req.off('end', onEnd);
      };

      const onEnd = () => {
        if (hasClosed) {
          return;
        }
        hasClosed = true;
        req.off('data', onData);
        req.off('end', onEnd);
        controller.close();
      };

      req.on('data', onData);
      req.on('end', onEnd);
    },
    cancel() {
      req.destroy();
    },
  });
}
```


---

### 🔹 Commit #03: `b1efc096`
- **完整 Hash**: `b1efc09694dc112396a1b99b05a148ce00bea4e0`
- **說明 (Ground Truth)**: refactor(server): start the sse maxDurationMs timer alongside the stream it ends (#7699)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/src/unstable-core-do-not-import/http/resolveResponse.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:57, E:56, A:2) ➔ After(N:51, E:51, A:1)
- **差分統計**: +Nodes: 1, -Nodes: 7, +Edges: 3, -Edges: 8, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
+ 🌲 **#abort.signal** `(Control)` [新增控制項]
+   └── [WIRES_TO] `on('abort')()`
+       └── [TRIGGERS] `onAbort()`
+           └── [CALLS] `onStreamEnd()`
+               └── [CALLS] `clearTimeout (External/Unresolved)()`
+               └── [CALLS] `removeEventListener()()`
- 🌲 **#abortSignal** `(Control)` [刪除控制項]
-   └── [WIRES_TO] `on('abort')()`
-       └── [TRIGGERS] `onAbort()`
- 🌲 **#combinedAbort.signal** `(Control)` [刪除控制項]
-   └── [WIRES_TO] `on('abort')()`
-       └── [TRIGGERS] `cleanup()`
-           └── [CALLS] `clearTimeout (External/Unresolved)()`
-           └── [CALLS] `removeEventListener()()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `#abort.signal` (UI_CONTROL)
  • - [移除節點] `#abortSignal` (UI_CONTROL)
  • - [移除節點] `clearMaxDurationTimer` (FUNCTION_DEF)
  • - [移除節點] `#combinedAbort.signal` (UI_CONTROL)
  • - [移除節點] `cleanup` (FUNCTION_DEF)
  • - [移除節點] `removeEventListener()` (INVARIANT_GUARD)
  • - [移除節點] `on('abort')` (EVENT_BINDING)
  • - [移除節點] `removeEventListener()` (INVARIANT_GUARD)
  • + [新增呼叫邊] `onStreamEnd` ──[CALLS]──> `clearTimeout (External/Unresolved)`
  • + [新增呼叫邊] `onAbort` ──[CALLS]──> `onStreamEnd`
  • + [新增呼叫邊] `#abort.signal` ──[WIRES_TO]──> `on('abort')`
  • - [移除呼叫邊] `rpcCalls` ──[CALLS]──> `clearMaxDurationTimer`
  • - [移除呼叫邊] `cleanup` ──[CALLS]──> `clearTimeout (External/Unresolved)`
  • - [移除呼叫邊] `cleanup` ──[CALLS]──> `removeEventListener()`
  • - [移除呼叫邊] `clearMaxDurationTimer` ──[CALLS]──> `clearTimeout (External/Unresolved)`
  • _... 以及其餘 4 項拓樸變更_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'onError' 被深鎖在內部閉包 (scope:resolveResponse@after/packages/server/src/unstable-core-do-not-import/http/resolveResponse.ts:L255C8)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `onStreamEnd()`
- **變更前簽章 (Before)**: `onStreamEnd()` (L609~L612)
- **變更後簽章 (After)**: `onStreamEnd()` (L582~L585)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
              abortSignal.removeEventListener('abort', onAbort);
              result?.clearMaxDurationTimer?.();
            }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
              clearTimeout(maxDurationTimer);
              abort.signal.removeEventListener('abort', onAbort);
            }
```

### 🔹 函式: `rpcCalls()`
- **變更前簽章 (Before)**: `rpcCalls(call)` (L376~L461)
- **變更後簽章 (After)**: `rpcCalls(call)` (L378~L440)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      let clearMaxDurationTimer: (() => void) | undefined;
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);

            // the request signal may never abort (e.g. after a completed
            // response), so the timer is also cleared when the stream ends
            clearMaxDurationTimer = () => {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);
            };
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
            clearMaxDurationTimer,
          },
        ];
      } catch (cause) {
        clearMaxDurationTimer?.();
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            abort:
              proc._def.type === 'subscription' ? combinedAbort : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    }
```

### 🔹 函式: `resolveResponse()`
- **變更前簽章 (Before)**: `async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response>` (L255~L849)
- **變更後簽章 (After)**: `async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response>` (L255~L831)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response> {
  const { router, req } = opts;
  const headers = new Headers([['vary', 'trpc-accept, accept']]);
  const config = router._def._config;

  const url = new URL(req.url);

  if (req.method === 'HEAD') {
    // can be used for lambda warmup
    return new Response(null, {
      status: 204,
    });
  }

  const allowBatching = opts.allowBatching ?? opts.batching?.enabled ?? true;
  const allowMethodOverride =
    (opts.allowMethodOverride ?? false) && req.method === 'POST';

  type $Context = inferRouterContext<TRouter>;

  const infoTuple: ResultTuple<TRPCRequestInfo> = await run(async () => {
    try {
      return [
        undefined,
        await getRequestInfo({
          req,
          path: decodePath(opts.path),
          router,
          searchParams: url.searchParams,
          headers: opts.req.headers,
          url,
          maxBatchSize: opts.maxBatchSize,
        }),
      ];
    } catch (cause) {
      return [getTRPCErrorFromUnknown(cause), undefined];
    }
  });

  interface ContextManager {
    valueOrUndefined: () => $Context | undefined;
    value: () => $Context;
    create: (info: TRPCRequestInfo) => Promise<void>;
  }
  const ctxManager: ContextManager = run(() => {
    let result: ResultTuple<$Context> | undefined = undefined;
    return {
      valueOrUndefined: () => {
        if (!result) {
          return undefined;
        }
        return result[1];
      },
      value: () => {
        const [err, ctx] = result!;
        if (err) {
          throw err;
        }
        return ctx;
      },
      create: async (info) => {
        if (result) {
          throw new Error(
            'This should only be called once - report a bug in tRPC',
          );
        }
        try {
          const ctx = await opts.createContext({
            info,
          });
          result = [undefined, ctx];
        } catch (cause) {
          result = [getTRPCErrorFromUnknown(cause), undefined];
        }
      },
    };
  });

  const methodMapper = allowMethodOverride
    ? TYPE_ACCEPTED_METHOD_MAP_WITH_METHOD_OVERRIDE
    : TYPE_ACCEPTED_METHOD_MAP;

  /**
   * @deprecated
   */
  const isStreamCall = getAcceptHeader(req.headers) === 'application/jsonl';

  const experimentalSSE = config.sse?.enabled ?? true;
  try {
    const [infoError, info] = infoTuple;
    if (infoError) {
      throw infoError;
    }
    if (info.isBatchCall && !allowBatching) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batching is not enabled on the server`,
      });
    }
    /* istanbul ignore if -- @preserve */
    if (isStreamCall && !info.isBatchCall) {
      throw new TRPCError({
        message: `Streaming requests must be batched (you can do a batch of 1)`,
        code: 'BAD_REQUEST',
      });
    }
    await ctxManager.create(info);

    interface RPCResultOk {
      data: unknown;
      signal?: AbortSignal;
      clearMaxDurationTimer?: () => void;
    }
    type RPCResult = ResultTuple<RPCResultOk>;
    const bodyCancelled = new AbortController();
    const callSignal = abortSignalsAnyPonyfill([
      opts.req.signal,
      bodyCancelled.signal,
    ]);
    const rpcCalls = info.calls.map(async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      let clearMaxDurationTimer: (() => void) | undefined;
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);

            // the request signal may never abort (e.g. after a completed
            // response), so the timer is also cleared when the stream ends
            clearMaxDurationTimer = () => {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);
            };
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
            clearMaxDurationTimer,
          },
        ];
      } catch (cause) {
        clearMaxDurationTimer?.();
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    });

    // ----------- response handlers -----------
    if (!info.isBatchCall) {
      const [call] = info.calls;
      const [error, result] = await rpcCalls[0]!;

      switch (info.type) {
        case 'unknown':
        case 'mutation':
        case 'query': {
          // httpLink
          headers.set('content-type', 'application/json');

          if (isDataStream(result?.data)) {
            throw new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            });
          }
          const res: TRPCResponse<unknown, inferRouterError<TRouter>> = error
            ? {
                error: getErrorShape({
                  config,
                  ctx: ctxManager.valueOrUndefined(),
                  error,
                  input: call!.result(),
                  path: call!.path,
                  type: info.type,
                }),
              }
            : { result: { data: result.data } };

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: error ? [error] : [],
            headers,
            untransformedJSON: [res],
          });
          return new Response(
            JSON.stringify(transformTRPCResponse(config, res)),
            {
              status: headResponse.status,
              headers,
            },
          );
        }
        case 'subscription': {
          // httpSubscriptionLink

          const iterable: AsyncIterable<unknown> = run(() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, callSignal)
              : result.data;
            return dataAsIterable;
          });

          const stream = sseStreamProducer({
            ...config.sse,
            lastEventId: getLastEventId({
              headers: req.headers,
              searchParams: url.searchParams,
            }),
            data: iterable,
            serialize: (v) => config.transformer.output.serialize(v),
            formatError(errorOpts) {
              const error = getTRPCErrorFromUnknown(errorOpts.error);
              const input = call?.result();
              const path = call?.path;
              const type = call?.procedure?._def.type ?? 'unknown';

              opts.onError?.({
                error,
                path,
                input,
                ctx: ctxManager.valueOrUndefined(),
                req: opts.req,
                type,
              });

              const shape = getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input,
                path,
                type,
              });

              return shape;
            },
          });
          for (const [key, value] of Object.entries(sseHeaders)) {
            headers.set(key, value);
          }

          let headResponse: ReturnType<typeof initResponse>;
          try {
            headResponse = initResponse({
              ctx: ctxManager.valueOrUndefined(),
              info,
              responseMeta: opts.responseMeta,
              errors: [],
              headers,
              untransformedJSON: null,
            });
          } catch (cause) {
            result?.clearMaxDurationTimer?.();
            throw cause;
          }

          const abortSignal = result?.signal;
          let responseBody: ReadableStream<Uint8Array> = stream;

          // Fixes: https://github.com/trpc/trpc/issues/7094
          if (abortSignal) {
            const reader = stream.getReader();
            const onAbort = () => void reader.cancel();
            if (abortSignal.aborted) {
              onAbort();
            } else {
              abortSignal.addEventListener('abort', onAbort, { once: true });
            }
            const onStreamEnd = () => {
              abortSignal.removeEventListener('abort', onAbort);
              result?.clearMaxDurationTimer?.();
            };

            responseBody = new ReadableStream({
              async pull(controller) {
                const chunk = await reader.read().catch((cause: unknown) => {
                  onStreamEnd();
                  throw cause;
                });
                if (chunk.done) {
                  onStreamEnd();
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              },
              cancel() {
                onStreamEnd();
                bodyCancelled.abort();
                return reader.cancel();
              },
            });
          }

          return new Response(responseBody, {
            headers,
            status: headResponse.status,
          });
        }
      }
    }

    // batch response handlers
    if (info.accept === 'application/jsonl') {
      // httpBatchStreamLink
      headers.set(
        'content-type',
        config.jsonl?.contentType ?? 'application/json',
      );
      headers.set('transfer-encoding', 'chunked');
      const headResponse = initResponse({
        ctx: ctxManager.valueOrUndefined(),
        info,
        responseMeta: opts.responseMeta,
        errors: [],
        headers,
        untransformedJSON: null,
      });
      const stream = jsonlStreamProducer({
        ...config.jsonl,
        /**
         * Example structure for `maxDepth: 4`:
         * {
         *   // 1
         *   0: {
         *     // 2
         *     result: {
         *       // 3
         *       data: // 4
         *     }
         *   }
         * }
         */
        maxDepth: Infinity,
        data: rpcCalls.map(async (res, index) => {
          const [error, result] = await res;

          const call = info.calls[index];

          if (error) {
            return {
              error: getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input: call!.result(),
                path: call!.path,
                type: call!.procedure?._def.type ?? 'unknown',
              }),
            };
          }

          /**
           * Not very pretty, but we need to wrap nested data in promises
           * Our stream producer will only resolve top-level async values or async values that are directly nested in another async value
           */
          const iterable = isObservable(result.data)
            ? observableToAsyncIterable(result.data, callSignal)
            : Promise.resolve(result.data);
          return {
            result: Promise.resolve({
              data: iterable,
            }),
          };
        }),
        serialize: (data) => config.transformer.output.serialize(data),
        onError: (cause) => {
          opts.onError?.({
            error: getTRPCErrorFromUnknown(cause.error),
            path: undefined,
            input: undefined,
            ctx: ctxManager.valueOrUndefined(),
            req: opts.req,
            type: info?.type ?? 'unknown',
          });
        },

        formatError(errorOpts) {
          const call = info?.calls[errorOpts.path[0] as any];

          const error = getTRPCErrorFromUnknown(errorOpts.error);
          const input = call?.result();
          const path = call?.path;
          const type = call?.procedure?._def.type ?? 'unknown';

          // no need to call `onError` here as it will be propagated through the stream itself

          const shape = getErrorShape({
            config,
            ctx: ctxManager.valueOrUndefined(),
            error,
            input,
            path,
            type,
          });

          return shape;
        },
      });

      return new Response(abortOnCancel(stream, bodyCancelled), {
        headers,
        status: headResponse.status,
      });
    }

    // httpBatchLink
    /**
     * Non-streaming response:
     * - await all responses in parallel, blocking on the slowest one
     * - create headers with known response body
     * - return a complete HTTPResponse
     */
    headers.set('content-type', 'application/json');
    const results: RPCResult[] = (await Promise.all(rpcCalls)).map(
      (res): RPCResult => {
        const [error, result] = res;
        if (error) {
          return res;
        }

        if (isDataStream(result.data)) {
          return [
            new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            }),
            undefined,
          ];
        }
        return res;
      },
    );
    const resultAsRPCResponse = results.map(
      (
        [error, result],
        index,
      ): TRPCResponse<unknown, inferRouterError<TRouter>> => {
        const call = info.calls[index]!;
        if (error) {
          return {
            error: getErrorShape({
              config,
              ctx: ctxManager.valueOrUndefined(),
              error,
              input: call.result(),
              path: call.path,
              type: call.procedure?._def.type ?? 'unknown',
            }),
          };
        }
        return {
          result: { data: result.data },
        };
      },
    );

    const errors = results
      .map(([error]) => error)
      .filter(Boolean) as TRPCError[];

    const headResponse = initResponse({
      ctx: ctxManager.valueOrUndefined(),
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON: resultAsRPCResponse,
      errors,
      headers,
    });

    return new Response(
      JSON.stringify(transformTRPCResponse(config, resultAsRPCResponse)),
      {
        status: headResponse.status,
        headers,
      },
    );
  } catch (cause) {
    const [_infoError, info] = infoTuple;
    const ctx = ctxManager.valueOrUndefined();
    // we get here if
    // - batching is called when it's not enabled
    // - `createContext()` throws
    // - `router._def._config.transformer.output.serialize()` throws
    // - post body is too large
    // - input deserialization fails
    // - `errorFormatter` return value is malformed
    const { error, untransformedJSON, body } = caughtErrorToData(cause, {
      opts,
      ctx: ctxManager.valueOrUndefined(),
      type: info?.type ?? 'unknown',
    });

    const headResponse = initResponse({
      ctx,
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON,
      errors: [error],
      headers,
    });

    return new Response(body, {
      status: headResponse.status,
      headers,
    });
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response> {
  const { router, req } = opts;
  const headers = new Headers([['vary', 'trpc-accept, accept']]);
  const config = router._def._config;

  const url = new URL(req.url);

  if (req.method === 'HEAD') {
    // can be used for lambda warmup
    return new Response(null, {
      status: 204,
    });
  }

  const allowBatching = opts.allowBatching ?? opts.batching?.enabled ?? true;
  const allowMethodOverride =
    (opts.allowMethodOverride ?? false) && req.method === 'POST';

  type $Context = inferRouterContext<TRouter>;

  const infoTuple: ResultTuple<TRPCRequestInfo> = await run(async () => {
    try {
      return [
        undefined,
        await getRequestInfo({
          req,
          path: decodePath(opts.path),
          router,
          searchParams: url.searchParams,
          headers: opts.req.headers,
          url,
          maxBatchSize: opts.maxBatchSize,
        }),
      ];
    } catch (cause) {
      return [getTRPCErrorFromUnknown(cause), undefined];
    }
  });

  interface ContextManager {
    valueOrUndefined: () => $Context | undefined;
    value: () => $Context;
    create: (info: TRPCRequestInfo) => Promise<void>;
  }
  const ctxManager: ContextManager = run(() => {
    let result: ResultTuple<$Context> | undefined = undefined;
    return {
      valueOrUndefined: () => {
        if (!result) {
          return undefined;
        }
        return result[1];
      },
      value: () => {
        const [err, ctx] = result!;
        if (err) {
          throw err;
        }
        return ctx;
      },
      create: async (info) => {
        if (result) {
          throw new Error(
            'This should only be called once - report a bug in tRPC',
          );
        }
        try {
          const ctx = await opts.createContext({
            info,
          });
          result = [undefined, ctx];
        } catch (cause) {
          result = [getTRPCErrorFromUnknown(cause), undefined];
        }
      },
    };
  });

  const methodMapper = allowMethodOverride
    ? TYPE_ACCEPTED_METHOD_MAP_WITH_METHOD_OVERRIDE
    : TYPE_ACCEPTED_METHOD_MAP;

  /**
   * @deprecated
   */
  const isStreamCall = getAcceptHeader(req.headers) === 'application/jsonl';

  const experimentalSSE = config.sse?.enabled ?? true;
  try {
    const [infoError, info] = infoTuple;
    if (infoError) {
      throw infoError;
    }
    if (info.isBatchCall && !allowBatching) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batching is not enabled on the server`,
      });
    }
    /* istanbul ignore if -- @preserve */
    if (isStreamCall && !info.isBatchCall) {
      throw new TRPCError({
        message: `Streaming requests must be batched (you can do a batch of 1)`,
        code: 'BAD_REQUEST',
      });
    }
    await ctxManager.create(info);

    interface RPCResultOk {
      data: unknown;
      /**
       * Only set for subscriptions
       */
      abort?: ReturnType<typeof combinedAbortController>;
    }
    type RPCResult = ResultTuple<RPCResultOk>;
    const bodyCancelled = new AbortController();
    const callSignal = abortSignalsAnyPonyfill([
      opts.req.signal,
      bodyCancelled.signal,
    ]);
    const rpcCalls = info.calls.map(async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            abort:
              proc._def.type === 'subscription' ? combinedAbort : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    });

    // ----------- response handlers -----------
    if (!info.isBatchCall) {
      const [call] = info.calls;
      const [error, result] = await rpcCalls[0]!;

      switch (info.type) {
        case 'unknown':
        case 'mutation':
        case 'query': {
          // httpLink
          headers.set('content-type', 'application/json');

          if (isDataStream(result?.data)) {
            throw new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            });
          }
          const res: TRPCResponse<unknown, inferRouterError<TRouter>> = error
            ? {
                error: getErrorShape({
                  config,
                  ctx: ctxManager.valueOrUndefined(),
                  error,
                  input: call!.result(),
                  path: call!.path,
                  type: info.type,
                }),
              }
            : { result: { data: result.data } };

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: error ? [error] : [],
            headers,
            untransformedJSON: [res],
          });
          return new Response(
            JSON.stringify(transformTRPCResponse(config, res)),
            {
              status: headResponse.status,
              headers,
            },
          );
        }
        case 'subscription': {
          // httpSubscriptionLink

          const iterable: AsyncIterable<unknown> = run(() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, callSignal)
              : result.data;
            return dataAsIterable;
          });

          const stream = sseStreamProducer({
            ...config.sse,
            lastEventId: getLastEventId({
              headers: req.headers,
              searchParams: url.searchParams,
            }),
            data: iterable,
            serialize: (v) => config.transformer.output.serialize(v),
            formatError(errorOpts) {
              const error = getTRPCErrorFromUnknown(errorOpts.error);
              const input = call?.result();
              const path = call?.path;
              const type = call?.procedure?._def.type ?? 'unknown';

              opts.onError?.({
                error,
                path,
                input,
                ctx: ctxManager.valueOrUndefined(),
                req: opts.req,
                type,
              });

              const shape = getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input,
                path,
                type,
              });

              return shape;
            },
          });
          for (const [key, value] of Object.entries(sseHeaders)) {
            headers.set(key, value);
          }

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: [],
            headers,
            untransformedJSON: null,
          });

          const abort = result?.abort;
          let responseBody: ReadableStream<Uint8Array> = stream;

          // Fixes: https://github.com/trpc/trpc/issues/7094
          if (abort) {
            const reader = stream.getReader();
            const maxDurationTimer = config.sse?.maxDurationMs
              ? setTimeout(
                  () => abort.controller.abort(),
                  config.sse.maxDurationMs,
                )
              : undefined;
            const onStreamEnd = () => {
              clearTimeout(maxDurationTimer);
              abort.signal.removeEventListener('abort', onAbort);
            };
            const onAbort = () => {
              onStreamEnd();
              void reader.cancel();
            };
            if (abort.signal.aborted) {
              onAbort();
            } else {
              abort.signal.addEventListener('abort', onAbort, { once: true });
            }

            responseBody = new ReadableStream({
              async pull(controller) {
                const chunk = await reader.read().catch((cause: unknown) => {
                  onStreamEnd();
                  throw cause;
                });
                if (chunk.done) {
                  onStreamEnd();
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              },
              cancel() {
                onStreamEnd();
                bodyCancelled.abort();
                return reader.cancel();
              },
            });
          }

          return new Response(responseBody, {
            headers,
            status: headResponse.status,
          });
        }
      }
    }

    // batch response handlers
    if (info.accept === 'application/jsonl') {
      // httpBatchStreamLink
      headers.set(
        'content-type',
        config.jsonl?.contentType ?? 'application/json',
      );
      headers.set('transfer-encoding', 'chunked');
      const headResponse = initResponse({
        ctx: ctxManager.valueOrUndefined(),
        info,
        responseMeta: opts.responseMeta,
        errors: [],
        headers,
        untransformedJSON: null,
      });
      const stream = jsonlStreamProducer({
        ...config.jsonl,
        /**
         * Example structure for `maxDepth: 4`:
         * {
         *   // 1
         *   0: {
         *     // 2
         *     result: {
         *       // 3
         *       data: // 4
         *     }
         *   }
         * }
         */
        maxDepth: Infinity,
        data: rpcCalls.map(async (res, index) => {
          const [error, result] = await res;

          const call = info.calls[index];

          if (error) {
            return {
              error: getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input: call!.result(),
                path: call!.path,
                type: call!.procedure?._def.type ?? 'unknown',
              }),
            };
          }

          /**
           * Not very pretty, but we need to wrap nested data in promises
           * Our stream producer will only resolve top-level async values or async values that are directly nested in another async value
           */
          const iterable = isObservable(result.data)
            ? observableToAsyncIterable(result.data, callSignal)
            : Promise.resolve(result.data);
          return {
            result: Promise.resolve({
              data: iterable,
            }),
          };
        }),
        serialize: (data) => config.transformer.output.serialize(data),
        onError: (cause) => {
          opts.onError?.({
            error: getTRPCErrorFromUnknown(cause.error),
            path: undefined,
            input: undefined,
            ctx: ctxManager.valueOrUndefined(),
            req: opts.req,
            type: info?.type ?? 'unknown',
          });
        },

        formatError(errorOpts) {
          const call = info?.calls[errorOpts.path[0] as any];

          const error = getTRPCErrorFromUnknown(errorOpts.error);
          const input = call?.result();
          const path = call?.path;
          const type = call?.procedure?._def.type ?? 'unknown';

          // no need to call `onError` here as it will be propagated through the stream itself

          const shape = getErrorShape({
            config,
            ctx: ctxManager.valueOrUndefined(),
            error,
            input,
            path,
            type,
          });

          return shape;
        },
      });

      return new Response(abortOnCancel(stream, bodyCancelled), {
        headers,
        status: headResponse.status,
      });
    }

    // httpBatchLink
    /**
     * Non-streaming response:
     * - await all responses in parallel, blocking on the slowest one
     * - create headers with known response body
     * - return a complete HTTPResponse
     */
    headers.set('content-type', 'application/json');
    const results: RPCResult[] = (await Promise.all(rpcCalls)).map(
      (res): RPCResult => {
        const [error, result] = res;
        if (error) {
          return res;
        }

        if (isDataStream(result.data)) {
          return [
            new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            }),
            undefined,
          ];
        }
        return res;
      },
    );
    const resultAsRPCResponse = results.map(
      (
        [error, result],
        index,
      ): TRPCResponse<unknown, inferRouterError<TRouter>> => {
        const call = info.calls[index]!;
        if (error) {
          return {
            error: getErrorShape({
              config,
              ctx: ctxManager.valueOrUndefined(),
              error,
              input: call.result(),
              path: call.path,
              type: call.procedure?._def.type ?? 'unknown',
            }),
          };
        }
        return {
          result: { data: result.data },
        };
      },
    );

    const errors = results
      .map(([error]) => error)
      .filter(Boolean) as TRPCError[];

    const headResponse = initResponse({
      ctx: ctxManager.valueOrUndefined(),
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON: resultAsRPCResponse,
      errors,
      headers,
    });

    return new Response(
      JSON.stringify(transformTRPCResponse(config, resultAsRPCResponse)),
      {
        status: headResponse.status,
        headers,
      },
    );
  } catch (cause) {
    const [_infoError, info] = infoTuple;
    const ctx = ctxManager.valueOrUndefined();
    // we get here if
    // - batching is called when it's not enabled
    // - `createContext()` throws
    // - `router._def._config.transformer.output.serialize()` throws
    // - post body is too large
    // - input deserialization fails
    // - `errorFormatter` return value is malformed
    const { error, untransformedJSON, body } = caughtErrorToData(cause, {
      opts,
      ctx: ctxManager.valueOrUndefined(),
      type: info?.type ?? 'unknown',
    });

    const headResponse = initResponse({
      ctx,
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON,
      errors: [error],
      headers,
    });

    return new Response(body, {
      status: headResponse.status,
      headers,
    });
  }
}
```

### 🔹 函式: `onAbort()`
- **變更前簽章 (Before)**: `onAbort()` (L603~L603)
- **變更後簽章 (After)**: `onAbort()` (L586~L589)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => void reader.cancel()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
              onStreamEnd();
              void reader.cancel();
            }
```


---

### 🔹 Commit #04: `78ac2eb5`
- **完整 Hash**: `78ac2eb56696ef68c6ee447be2430b57f5eeefbb`
- **說明 (Ground Truth)**: fix(server): only abort node-http requests when the connection closes early (#7664)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/src/adapters/node-http/incomingMessageToRequest.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:9, E:3, A:0) ➔ After(N:10, E:4, A:0)
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
  • + [新增節點] `onClose` (FUNCTION_DEF)
  • + [新增呼叫邊] `onClose` ──[CALLS [guard: (res.writableEnded)]]──> `onAbort`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `onAbort()`
- **變更前簽章 (Before)**: `onAbort()` (L133~L139)
- **變更後簽章 (After)**: `onAbort()` (L133~L139)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
    res.off('close', onAbort);
    req.off('aborted', onAbort);

    // abort the request
    ac.abort();
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
    res.off('close', onClose);
    req.off('aborted', onAbort);

    // abort the request
    ac.abort();
  }
```

### 🔹 函式: `incomingMessageToRequest()`
- **變更前簽章 (Before)**: `function incomingMessageToRequest(
  req: NodeHTTPRequest,
  res: NodeHTTPResponse,
  opts:` (L121~L167)
- **變更後簽章 (After)**: `function incomingMessageToRequest(
  req: NodeHTTPRequest,
  res: NodeHTTPResponse,
  opts:` (L121~L177)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function incomingMessageToRequest(
  req: NodeHTTPRequest,
  res: NodeHTTPResponse,
  opts: {
    /**
     * Max body size in bytes. If the body is larger than this, the request will be aborted
     */
    maxBodySize: number | null;
  },
): Request {
  const ac = new AbortController();

  const onAbort = () => {
    res.off('close', onAbort);
    req.off('aborted', onAbort);

    // abort the request
    ac.abort();
  };

  res.once('close', onAbort);
  req.once('aborted', onAbort);

  // Get host from either regular header or HTTP/2 pseudo-header
  const url = createURL(req);

  const init: RequestInit = {
    headers: createHeaders(req.headers),
    method: req.method,
    signal: ac.signal,
  };

  if (req.method !== 'GET' && req.method !== 'HEAD') {
    init.body = createBody(req, opts);

    // init.duplex = 'half' must be set when body is a ReadableStream, and Node follows the spec.
    // However, this property is not defined in the TypeScript types for RequestInit, so we have
    // to cast it here in order to set it without a type error.
    // See https://fetch.spec.whatwg.org/#dom-requestinit-duplex
    // @ts-expect-error this is fine
    init.duplex = 'half';
  }

  const request = new Request(url, init);

  return request;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function incomingMessageToRequest(
  req: NodeHTTPRequest,
  res: NodeHTTPResponse,
  opts: {
    /**
     * Max body size in bytes. If the body is larger than this, the request will be aborted
     */
    maxBodySize: number | null;
  },
): Request {
  const ac = new AbortController();

  const onAbort = () => {
    res.off('close', onClose);
    req.off('aborted', onAbort);

    // abort the request
    ac.abort();
  };

  const onClose = () => {
    // `close` is also emitted after a response that was sent completely,
    // so only abort if the connection closed before the response was ended
    if (res.writableEnded) {
      req.off('aborted', onAbort);
      return;
    }
    onAbort();
  };

  res.once('close', onClose);
  req.once('aborted', onAbort);

  // Get host from either regular header or HTTP/2 pseudo-header
  const url = createURL(req);

  const init: RequestInit = {
    headers: createHeaders(req.headers),
    method: req.method,
    signal: ac.signal,
  };

  if (req.method !== 'GET' && req.method !== 'HEAD') {
    init.body = createBody(req, opts);

    // init.duplex = 'half' must be set when body is a ReadableStream, and Node follows the spec.
    // However, this property is not defined in the TypeScript types for RequestInit, so we have
    // to cast it here in order to set it without a type error.
    // See https://fetch.spec.whatwg.org/#dom-requestinit-duplex
    // @ts-expect-error this is fine
    init.duplex = 'half';
  }

  const request = new Request(url, init);

  return request;
}
```


---

### 🔹 Commit #05: `243cd99a`
- **完整 Hash**: `243cd99af7c43d3cef26d813122150441d6187db`
- **說明 (Ground Truth)**: fix(server): clear the sse maxDurationMs timer when the subscription ends (#7666)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/src/unstable-core-do-not-import/http/resolveResponse.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:55, E:52, A:2) ➔ After(N:57, E:56, A:2)
- **差分統計**: +Nodes: 4, -Nodes: 2, +Edges: 6, -Edges: 2, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#abortSignal** `(Control)`
    └── ⚡ **on('abort')**
        └── 🎯 [TRIGGERS] `onAbort()`
  🌲 **#combinedAbort.signal** `(Control)`
    └── ⚡ **on('abort')**
        └── 🎯 [TRIGGERS] `cleanup()`
            └── 🎯 [CALLS] `clearTimeout (External/Unresolved)()`
            └── 🎯 [CALLS] `removeEventListener()()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `onStreamEnd` (FUNCTION_DEF)
  • + [新增節點] `clearMaxDurationTimer` (FUNCTION_DEF)
  • + [新增節點] `removeEventListener()` (INVARIANT_GUARD)
  • + [新增節點] `removeEventListener()` (INVARIANT_GUARD)
  • - [移除節點] `removeEventListener()` (INVARIANT_GUARD)
  • - [移除節點] `removeEventListener()` (INVARIANT_GUARD)
  • + [新增呼叫邊] `rpcCalls` ──[CALLS]──> `clearMaxDurationTimer`
  • + [新增呼叫邊] `clearMaxDurationTimer` ──[CALLS]──> `clearTimeout (External/Unresolved)`
  • + [新增呼叫邊] `clearMaxDurationTimer` ──[CALLS]──> `removeEventListener()`
  • + [新增呼叫邊] `onStreamEnd` ──[CALLS]──> `removeEventListener()`
  • + [新增呼叫邊] `pull` ──[CALLS [guard: (chunk.done)]]──> `onStreamEnd`
  • + [新增呼叫邊] `cancel` ──[CALLS]──> `onStreamEnd`
  • - [移除呼叫邊] `pull` ──[CALLS]──> `removeEventListener()`
  • - [移除呼叫邊] `cancel` ──[CALLS]──> `removeEventListener()`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'onError' 被深鎖在內部閉包 (scope:resolveResponse@after/packages/server/src/unstable-core-do-not-import/http/resolveResponse.ts:L255C8)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `pull()`
- **變更前簽章 (Before)**: `pull(controller)` (L594~L602)
- **變更後簽章 (After)**: `pull(controller)` (L615~L626)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async pull(controller) {
                const chunk = await reader.read();
                if (chunk.done) {
                  abortSignal.removeEventListener('abort', onAbort);
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async pull(controller) {
                const chunk = await reader.read().catch((cause: unknown) => {
                  onStreamEnd();
                  throw cause;
                });
                if (chunk.done) {
                  onStreamEnd();
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              }
```

### 🔹 函式: `rpcCalls()`
- **變更前簽章 (Before)**: `rpcCalls(call)` (L375~L450)
- **變更後簽章 (After)**: `rpcCalls(call)` (L376~L461)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      let clearMaxDurationTimer: (() => void) | undefined;
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);

            // the request signal may never abort (e.g. after a completed
            // response), so the timer is also cleared when the stream ends
            clearMaxDurationTimer = () => {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);
            };
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
            clearMaxDurationTimer,
          },
        ];
      } catch (cause) {
        clearMaxDurationTimer?.();
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    }
```

### 🔹 函式: `cancel()`
- **變更前簽章 (Before)**: `cancel()` (L603~L607)
- **變更後簽章 (After)**: `cancel()` (L627~L631)

#### ◀️ 變更前實作碼 (Before Implementation):
```
cancel() {
                abortSignal.removeEventListener('abort', onAbort);
                bodyCancelled.abort();
                return reader.cancel();
              }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
cancel() {
                onStreamEnd();
                bodyCancelled.abort();
                return reader.cancel();
              }
```

### 🔹 函式: `resolveResponse()`
- **變更前簽章 (Before)**: `async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response>` (L255~L825)
- **變更後簽章 (After)**: `async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response>` (L255~L849)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response> {
  const { router, req } = opts;
  const headers = new Headers([['vary', 'trpc-accept, accept']]);
  const config = router._def._config;

  const url = new URL(req.url);

  if (req.method === 'HEAD') {
    // can be used for lambda warmup
    return new Response(null, {
      status: 204,
    });
  }

  const allowBatching = opts.allowBatching ?? opts.batching?.enabled ?? true;
  const allowMethodOverride =
    (opts.allowMethodOverride ?? false) && req.method === 'POST';

  type $Context = inferRouterContext<TRouter>;

  const infoTuple: ResultTuple<TRPCRequestInfo> = await run(async () => {
    try {
      return [
        undefined,
        await getRequestInfo({
          req,
          path: decodePath(opts.path),
          router,
          searchParams: url.searchParams,
          headers: opts.req.headers,
          url,
          maxBatchSize: opts.maxBatchSize,
        }),
      ];
    } catch (cause) {
      return [getTRPCErrorFromUnknown(cause), undefined];
    }
  });

  interface ContextManager {
    valueOrUndefined: () => $Context | undefined;
    value: () => $Context;
    create: (info: TRPCRequestInfo) => Promise<void>;
  }
  const ctxManager: ContextManager = run(() => {
    let result: ResultTuple<$Context> | undefined = undefined;
    return {
      valueOrUndefined: () => {
        if (!result) {
          return undefined;
        }
        return result[1];
      },
      value: () => {
        const [err, ctx] = result!;
        if (err) {
          throw err;
        }
        return ctx;
      },
      create: async (info) => {
        if (result) {
          throw new Error(
            'This should only be called once - report a bug in tRPC',
          );
        }
        try {
          const ctx = await opts.createContext({
            info,
          });
          result = [undefined, ctx];
        } catch (cause) {
          result = [getTRPCErrorFromUnknown(cause), undefined];
        }
      },
    };
  });

  const methodMapper = allowMethodOverride
    ? TYPE_ACCEPTED_METHOD_MAP_WITH_METHOD_OVERRIDE
    : TYPE_ACCEPTED_METHOD_MAP;

  /**
   * @deprecated
   */
  const isStreamCall = getAcceptHeader(req.headers) === 'application/jsonl';

  const experimentalSSE = config.sse?.enabled ?? true;
  try {
    const [infoError, info] = infoTuple;
    if (infoError) {
      throw infoError;
    }
    if (info.isBatchCall && !allowBatching) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batching is not enabled on the server`,
      });
    }
    /* istanbul ignore if -- @preserve */
    if (isStreamCall && !info.isBatchCall) {
      throw new TRPCError({
        message: `Streaming requests must be batched (you can do a batch of 1)`,
        code: 'BAD_REQUEST',
      });
    }
    await ctxManager.create(info);

    interface RPCResultOk {
      data: unknown;
      signal?: AbortSignal;
    }
    type RPCResult = ResultTuple<RPCResultOk>;
    const bodyCancelled = new AbortController();
    const callSignal = abortSignalsAnyPonyfill([
      opts.req.signal,
      bodyCancelled.signal,
    ]);
    const rpcCalls = info.calls.map(async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    });

    // ----------- response handlers -----------
    if (!info.isBatchCall) {
      const [call] = info.calls;
      const [error, result] = await rpcCalls[0]!;

      switch (info.type) {
        case 'unknown':
        case 'mutation':
        case 'query': {
          // httpLink
          headers.set('content-type', 'application/json');

          if (isDataStream(result?.data)) {
            throw new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            });
          }
          const res: TRPCResponse<unknown, inferRouterError<TRouter>> = error
            ? {
                error: getErrorShape({
                  config,
                  ctx: ctxManager.valueOrUndefined(),
                  error,
                  input: call!.result(),
                  path: call!.path,
                  type: info.type,
                }),
              }
            : { result: { data: result.data } };

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: error ? [error] : [],
            headers,
            untransformedJSON: [res],
          });
          return new Response(
            JSON.stringify(transformTRPCResponse(config, res)),
            {
              status: headResponse.status,
              headers,
            },
          );
        }
        case 'subscription': {
          // httpSubscriptionLink

          const iterable: AsyncIterable<unknown> = run(() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, callSignal)
              : result.data;
            return dataAsIterable;
          });

          const stream = sseStreamProducer({
            ...config.sse,
            lastEventId: getLastEventId({
              headers: req.headers,
              searchParams: url.searchParams,
            }),
            data: iterable,
            serialize: (v) => config.transformer.output.serialize(v),
            formatError(errorOpts) {
              const error = getTRPCErrorFromUnknown(errorOpts.error);
              const input = call?.result();
              const path = call?.path;
              const type = call?.procedure?._def.type ?? 'unknown';

              opts.onError?.({
                error,
                path,
                input,
                ctx: ctxManager.valueOrUndefined(),
                req: opts.req,
                type,
              });

              const shape = getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input,
                path,
                type,
              });

              return shape;
            },
          });
          for (const [key, value] of Object.entries(sseHeaders)) {
            headers.set(key, value);
          }

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: [],
            headers,
            untransformedJSON: null,
          });

          const abortSignal = result?.signal;
          let responseBody: ReadableStream<Uint8Array> = stream;

          // Fixes: https://github.com/trpc/trpc/issues/7094
          if (abortSignal) {
            const reader = stream.getReader();
            const onAbort = () => void reader.cancel();
            if (abortSignal.aborted) {
              onAbort();
            } else {
              abortSignal.addEventListener('abort', onAbort, { once: true });
            }

            responseBody = new ReadableStream({
              async pull(controller) {
                const chunk = await reader.read();
                if (chunk.done) {
                  abortSignal.removeEventListener('abort', onAbort);
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              },
              cancel() {
                abortSignal.removeEventListener('abort', onAbort);
                bodyCancelled.abort();
                return reader.cancel();
              },
            });
          }

          return new Response(responseBody, {
            headers,
            status: headResponse.status,
          });
        }
      }
    }

    // batch response handlers
    if (info.accept === 'application/jsonl') {
      // httpBatchStreamLink
      headers.set(
        'content-type',
        config.jsonl?.contentType ?? 'application/json',
      );
      headers.set('transfer-encoding', 'chunked');
      const headResponse = initResponse({
        ctx: ctxManager.valueOrUndefined(),
        info,
        responseMeta: opts.responseMeta,
        errors: [],
        headers,
        untransformedJSON: null,
      });
      const stream = jsonlStreamProducer({
        ...config.jsonl,
        /**
         * Example structure for `maxDepth: 4`:
         * {
         *   // 1
         *   0: {
         *     // 2
         *     result: {
         *       // 3
         *       data: // 4
         *     }
         *   }
         * }
         */
        maxDepth: Infinity,
        data: rpcCalls.map(async (res, index) => {
          const [error, result] = await res;

          const call = info.calls[index];

          if (error) {
            return {
              error: getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input: call!.result(),
                path: call!.path,
                type: call!.procedure?._def.type ?? 'unknown',
              }),
            };
          }

          /**
           * Not very pretty, but we need to wrap nested data in promises
           * Our stream producer will only resolve top-level async values or async values that are directly nested in another async value
           */
          const iterable = isObservable(result.data)
            ? observableToAsyncIterable(result.data, callSignal)
            : Promise.resolve(result.data);
          return {
            result: Promise.resolve({
              data: iterable,
            }),
          };
        }),
        serialize: (data) => config.transformer.output.serialize(data),
        onError: (cause) => {
          opts.onError?.({
            error: getTRPCErrorFromUnknown(cause.error),
            path: undefined,
            input: undefined,
            ctx: ctxManager.valueOrUndefined(),
            req: opts.req,
            type: info?.type ?? 'unknown',
          });
        },

        formatError(errorOpts) {
          const call = info?.calls[errorOpts.path[0] as any];

          const error = getTRPCErrorFromUnknown(errorOpts.error);
          const input = call?.result();
          const path = call?.path;
          const type = call?.procedure?._def.type ?? 'unknown';

          // no need to call `onError` here as it will be propagated through the stream itself

          const shape = getErrorShape({
            config,
            ctx: ctxManager.valueOrUndefined(),
            error,
            input,
            path,
            type,
          });

          return shape;
        },
      });

      return new Response(abortOnCancel(stream, bodyCancelled), {
        headers,
        status: headResponse.status,
      });
    }

    // httpBatchLink
    /**
     * Non-streaming response:
     * - await all responses in parallel, blocking on the slowest one
     * - create headers with known response body
     * - return a complete HTTPResponse
     */
    headers.set('content-type', 'application/json');
    const results: RPCResult[] = (await Promise.all(rpcCalls)).map(
      (res): RPCResult => {
        const [error, result] = res;
        if (error) {
          return res;
        }

        if (isDataStream(result.data)) {
          return [
            new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            }),
            undefined,
          ];
        }
        return res;
      },
    );
    const resultAsRPCResponse = results.map(
      (
        [error, result],
        index,
      ): TRPCResponse<unknown, inferRouterError<TRouter>> => {
        const call = info.calls[index]!;
        if (error) {
          return {
            error: getErrorShape({
              config,
              ctx: ctxManager.valueOrUndefined(),
              error,
              input: call.result(),
              path: call.path,
              type: call.procedure?._def.type ?? 'unknown',
            }),
          };
        }
        return {
          result: { data: result.data },
        };
      },
    );

    const errors = results
      .map(([error]) => error)
      .filter(Boolean) as TRPCError[];

    const headResponse = initResponse({
      ctx: ctxManager.valueOrUndefined(),
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON: resultAsRPCResponse,
      errors,
      headers,
    });

    return new Response(
      JSON.stringify(transformTRPCResponse(config, resultAsRPCResponse)),
      {
        status: headResponse.status,
        headers,
      },
    );
  } catch (cause) {
    const [_infoError, info] = infoTuple;
    const ctx = ctxManager.valueOrUndefined();
    // we get here if
    // - batching is called when it's not enabled
    // - `createContext()` throws
    // - `router._def._config.transformer.output.serialize()` throws
    // - post body is too large
    // - input deserialization fails
    // - `errorFormatter` return value is malformed
    const { error, untransformedJSON, body } = caughtErrorToData(cause, {
      opts,
      ctx: ctxManager.valueOrUndefined(),
      type: info?.type ?? 'unknown',
    });

    const headResponse = initResponse({
      ctx,
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON,
      errors: [error],
      headers,
    });

    return new Response(body, {
      status: headResponse.status,
      headers,
    });
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response> {
  const { router, req } = opts;
  const headers = new Headers([['vary', 'trpc-accept, accept']]);
  const config = router._def._config;

  const url = new URL(req.url);

  if (req.method === 'HEAD') {
    // can be used for lambda warmup
    return new Response(null, {
      status: 204,
    });
  }

  const allowBatching = opts.allowBatching ?? opts.batching?.enabled ?? true;
  const allowMethodOverride =
    (opts.allowMethodOverride ?? false) && req.method === 'POST';

  type $Context = inferRouterContext<TRouter>;

  const infoTuple: ResultTuple<TRPCRequestInfo> = await run(async () => {
    try {
      return [
        undefined,
        await getRequestInfo({
          req,
          path: decodePath(opts.path),
          router,
          searchParams: url.searchParams,
          headers: opts.req.headers,
          url,
          maxBatchSize: opts.maxBatchSize,
        }),
      ];
    } catch (cause) {
      return [getTRPCErrorFromUnknown(cause), undefined];
    }
  });

  interface ContextManager {
    valueOrUndefined: () => $Context | undefined;
    value: () => $Context;
    create: (info: TRPCRequestInfo) => Promise<void>;
  }
  const ctxManager: ContextManager = run(() => {
    let result: ResultTuple<$Context> | undefined = undefined;
    return {
      valueOrUndefined: () => {
        if (!result) {
          return undefined;
        }
        return result[1];
      },
      value: () => {
        const [err, ctx] = result!;
        if (err) {
          throw err;
        }
        return ctx;
      },
      create: async (info) => {
        if (result) {
          throw new Error(
            'This should only be called once - report a bug in tRPC',
          );
        }
        try {
          const ctx = await opts.createContext({
            info,
          });
          result = [undefined, ctx];
        } catch (cause) {
          result = [getTRPCErrorFromUnknown(cause), undefined];
        }
      },
    };
  });

  const methodMapper = allowMethodOverride
    ? TYPE_ACCEPTED_METHOD_MAP_WITH_METHOD_OVERRIDE
    : TYPE_ACCEPTED_METHOD_MAP;

  /**
   * @deprecated
   */
  const isStreamCall = getAcceptHeader(req.headers) === 'application/jsonl';

  const experimentalSSE = config.sse?.enabled ?? true;
  try {
    const [infoError, info] = infoTuple;
    if (infoError) {
      throw infoError;
    }
    if (info.isBatchCall && !allowBatching) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batching is not enabled on the server`,
      });
    }
    /* istanbul ignore if -- @preserve */
    if (isStreamCall && !info.isBatchCall) {
      throw new TRPCError({
        message: `Streaming requests must be batched (you can do a batch of 1)`,
        code: 'BAD_REQUEST',
      });
    }
    await ctxManager.create(info);

    interface RPCResultOk {
      data: unknown;
      signal?: AbortSignal;
      clearMaxDurationTimer?: () => void;
    }
    type RPCResult = ResultTuple<RPCResultOk>;
    const bodyCancelled = new AbortController();
    const callSignal = abortSignalsAnyPonyfill([
      opts.req.signal,
      bodyCancelled.signal,
    ]);
    const rpcCalls = info.calls.map(async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      let clearMaxDurationTimer: (() => void) | undefined;
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);

            // the request signal may never abort (e.g. after a completed
            // response), so the timer is also cleared when the stream ends
            clearMaxDurationTimer = () => {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);
            };
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
            clearMaxDurationTimer,
          },
        ];
      } catch (cause) {
        clearMaxDurationTimer?.();
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    });

    // ----------- response handlers -----------
    if (!info.isBatchCall) {
      const [call] = info.calls;
      const [error, result] = await rpcCalls[0]!;

      switch (info.type) {
        case 'unknown':
        case 'mutation':
        case 'query': {
          // httpLink
          headers.set('content-type', 'application/json');

          if (isDataStream(result?.data)) {
            throw new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            });
          }
          const res: TRPCResponse<unknown, inferRouterError<TRouter>> = error
            ? {
                error: getErrorShape({
                  config,
                  ctx: ctxManager.valueOrUndefined(),
                  error,
                  input: call!.result(),
                  path: call!.path,
                  type: info.type,
                }),
              }
            : { result: { data: result.data } };

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: error ? [error] : [],
            headers,
            untransformedJSON: [res],
          });
          return new Response(
            JSON.stringify(transformTRPCResponse(config, res)),
            {
              status: headResponse.status,
              headers,
            },
          );
        }
        case 'subscription': {
          // httpSubscriptionLink

          const iterable: AsyncIterable<unknown> = run(() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, callSignal)
              : result.data;
            return dataAsIterable;
          });

          const stream = sseStreamProducer({
            ...config.sse,
            lastEventId: getLastEventId({
              headers: req.headers,
              searchParams: url.searchParams,
            }),
            data: iterable,
            serialize: (v) => config.transformer.output.serialize(v),
            formatError(errorOpts) {
              const error = getTRPCErrorFromUnknown(errorOpts.error);
              const input = call?.result();
              const path = call?.path;
              const type = call?.procedure?._def.type ?? 'unknown';

              opts.onError?.({
                error,
                path,
                input,
                ctx: ctxManager.valueOrUndefined(),
                req: opts.req,
                type,
              });

              const shape = getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input,
                path,
                type,
              });

              return shape;
            },
          });
          for (const [key, value] of Object.entries(sseHeaders)) {
            headers.set(key, value);
          }

          let headResponse: ReturnType<typeof initResponse>;
          try {
            headResponse = initResponse({
              ctx: ctxManager.valueOrUndefined(),
              info,
              responseMeta: opts.responseMeta,
              errors: [],
              headers,
              untransformedJSON: null,
            });
          } catch (cause) {
            result?.clearMaxDurationTimer?.();
            throw cause;
          }

          const abortSignal = result?.signal;
          let responseBody: ReadableStream<Uint8Array> = stream;

          // Fixes: https://github.com/trpc/trpc/issues/7094
          if (abortSignal) {
            const reader = stream.getReader();
            const onAbort = () => void reader.cancel();
            if (abortSignal.aborted) {
              onAbort();
            } else {
              abortSignal.addEventListener('abort', onAbort, { once: true });
            }
            const onStreamEnd = () => {
              abortSignal.removeEventListener('abort', onAbort);
              result?.clearMaxDurationTimer?.();
            };

            responseBody = new ReadableStream({
              async pull(controller) {
                const chunk = await reader.read().catch((cause: unknown) => {
                  onStreamEnd();
                  throw cause;
                });
                if (chunk.done) {
                  onStreamEnd();
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              },
              cancel() {
                onStreamEnd();
                bodyCancelled.abort();
                return reader.cancel();
              },
            });
          }

          return new Response(responseBody, {
            headers,
            status: headResponse.status,
          });
        }
      }
    }

    // batch response handlers
    if (info.accept === 'application/jsonl') {
      // httpBatchStreamLink
      headers.set(
        'content-type',
        config.jsonl?.contentType ?? 'application/json',
      );
      headers.set('transfer-encoding', 'chunked');
      const headResponse = initResponse({
        ctx: ctxManager.valueOrUndefined(),
        info,
        responseMeta: opts.responseMeta,
        errors: [],
        headers,
        untransformedJSON: null,
      });
      const stream = jsonlStreamProducer({
        ...config.jsonl,
        /**
         * Example structure for `maxDepth: 4`:
         * {
         *   // 1
         *   0: {
         *     // 2
         *     result: {
         *       // 3
         *       data: // 4
         *     }
         *   }
         * }
         */
        maxDepth: Infinity,
        data: rpcCalls.map(async (res, index) => {
          const [error, result] = await res;

          const call = info.calls[index];

          if (error) {
            return {
              error: getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input: call!.result(),
                path: call!.path,
                type: call!.procedure?._def.type ?? 'unknown',
              }),
            };
          }

          /**
           * Not very pretty, but we need to wrap nested data in promises
           * Our stream producer will only resolve top-level async values or async values that are directly nested in another async value
           */
          const iterable = isObservable(result.data)
            ? observableToAsyncIterable(result.data, callSignal)
            : Promise.resolve(result.data);
          return {
            result: Promise.resolve({
              data: iterable,
            }),
          };
        }),
        serialize: (data) => config.transformer.output.serialize(data),
        onError: (cause) => {
          opts.onError?.({
            error: getTRPCErrorFromUnknown(cause.error),
            path: undefined,
            input: undefined,
            ctx: ctxManager.valueOrUndefined(),
            req: opts.req,
            type: info?.type ?? 'unknown',
          });
        },

        formatError(errorOpts) {
          const call = info?.calls[errorOpts.path[0] as any];

          const error = getTRPCErrorFromUnknown(errorOpts.error);
          const input = call?.result();
          const path = call?.path;
          const type = call?.procedure?._def.type ?? 'unknown';

          // no need to call `onError` here as it will be propagated through the stream itself

          const shape = getErrorShape({
            config,
            ctx: ctxManager.valueOrUndefined(),
            error,
            input,
            path,
            type,
          });

          return shape;
        },
      });

      return new Response(abortOnCancel(stream, bodyCancelled), {
        headers,
        status: headResponse.status,
      });
    }

    // httpBatchLink
    /**
     * Non-streaming response:
     * - await all responses in parallel, blocking on the slowest one
     * - create headers with known response body
     * - return a complete HTTPResponse
     */
    headers.set('content-type', 'application/json');
    const results: RPCResult[] = (await Promise.all(rpcCalls)).map(
      (res): RPCResult => {
        const [error, result] = res;
        if (error) {
          return res;
        }

        if (isDataStream(result.data)) {
          return [
            new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            }),
            undefined,
          ];
        }
        return res;
      },
    );
    const resultAsRPCResponse = results.map(
      (
        [error, result],
        index,
      ): TRPCResponse<unknown, inferRouterError<TRouter>> => {
        const call = info.calls[index]!;
        if (error) {
          return {
            error: getErrorShape({
              config,
              ctx: ctxManager.valueOrUndefined(),
              error,
              input: call.result(),
              path: call.path,
              type: call.procedure?._def.type ?? 'unknown',
            }),
          };
        }
        return {
          result: { data: result.data },
        };
      },
    );

    const errors = results
      .map(([error]) => error)
      .filter(Boolean) as TRPCError[];

    const headResponse = initResponse({
      ctx: ctxManager.valueOrUndefined(),
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON: resultAsRPCResponse,
      errors,
      headers,
    });

    return new Response(
      JSON.stringify(transformTRPCResponse(config, resultAsRPCResponse)),
      {
        status: headResponse.status,
        headers,
      },
    );
  } catch (cause) {
    const [_infoError, info] = infoTuple;
    const ctx = ctxManager.valueOrUndefined();
    // we get here if
    // - batching is called when it's not enabled
    // - `createContext()` throws
    // - `router._def._config.transformer.output.serialize()` throws
    // - post body is too large
    // - input deserialization fails
    // - `errorFormatter` return value is malformed
    const { error, untransformedJSON, body } = caughtErrorToData(cause, {
      opts,
      ctx: ctxManager.valueOrUndefined(),
      type: info?.type ?? 'unknown',
    });

    const headResponse = initResponse({
      ctx,
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON,
      errors: [error],
      headers,
    });

    return new Response(body, {
      status: headResponse.status,
      headers,
    });
  }
}
```


---

### 🔹 Commit #06: `7e95bbcb`
- **完整 Hash**: `7e95bbcbefb4260acbcbabb2569597bc88ac3c49`
- **說明 (Ground Truth)**: fix(server): register keepalive once per websocket connection (#7529)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/src/adapters/fastify/fastifyTRPCPlugin.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:7, E:6, A:0) ➔ After(N:6, E:5, A:0)
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
  • - [移除節點] `handleKeepAlive (External/Unresolved)` (FUNCTION_DEF)
  • - [移除呼叫邊] `fastifyTRPCPlugin` ──[CALLS]──> `handleKeepAlive (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `fastifyTRPCPlugin()`
- **變更前簽章 (Before)**: `function fastifyTRPCPlugin<TRouter extends AnyRouter>(
  fastify: FastifyInstance,
  opts: FastifyTRPCPluginOptions<TRouter>,
  done: (err?: Error) => void,
)` (L36~L89)
- **變更後簽章 (After)**: `function fastifyTRPCPlugin<TRouter extends AnyRouter>(
  fastify: FastifyInstance,
  opts: FastifyTRPCPluginOptions<TRouter>,
  done: (err?: Error) => void,
)` (L39~L91)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function fastifyTRPCPlugin<TRouter extends AnyRouter>(
  fastify: FastifyInstance,
  opts: FastifyTRPCPluginOptions<TRouter>,
  done: (err?: Error) => void,
) {
  fastify.removeContentTypeParser('application/json');
  fastify.addContentTypeParser(
    'application/json',
    { parseAs: 'string' },
    function (_, body, _done) {
      _done(null, body);
    },
  );
  fastify.removeContentTypeParser('multipart/form-data');
  fastify.addContentTypeParser(
    'multipart/form-data',
    {},
    function (_, body, _done) {
      _done(null, body);
    },
  );

  let prefix = opts.prefix ?? '';

  // https://github.com/fastify/fastify-plugin/blob/fe079bef6557a83794bf437e14b9b9edb8a74104/plugin.js#L11
  // @ts-expect-error property 'default' does not exists on type ...
  if (typeof fastifyTRPCPlugin.default !== 'function') {
    prefix = ''; // handled by fastify internally
  }

  fastify.all(`${prefix}/:path`, async (req, res) => {
    const path = (req.params as any).path;
    await fastifyRequestHandler({ ...opts.trpcOptions, req, res, path });
  });

  if (opts.useWSS) {
    const trpcOptions =
      opts.trpcOptions as unknown as WSSHandlerOptions<TRouter>;

    const onConnection = getWSConnectionHandler<TRouter>({
      ...trpcOptions,
    });

    fastify.get(prefix ?? '/', { websocket: true }, (socket, req) => {
      onConnection(socket, req.raw);
      if (trpcOptions?.keepAlive?.enabled) {
        const { pingMs, pongWaitMs } = trpcOptions.keepAlive;
        handleKeepAlive(socket, pingMs, pongWaitMs);
      }
    });
  }

  done();
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function fastifyTRPCPlugin<TRouter extends AnyRouter>(
  fastify: FastifyInstance,
  opts: FastifyTRPCPluginOptions<TRouter>,
  done: (err?: Error) => void,
) {
  fastify.removeContentTypeParser('application/json');
  fastify.addContentTypeParser(
    'application/json',
    { parseAs: 'string' },
    function (_, body, _done) {
      _done(null, body);
    },
  );
  fastify.removeContentTypeParser('multipart/form-data');
  fastify.addContentTypeParser(
    'multipart/form-data',
    {},
    function (_, body, _done) {
      _done(null, body);
    },
  );

  let prefix = opts.prefix ?? '';

  // https://github.com/fastify/fastify-plugin/blob/fe079bef6557a83794bf437e14b9b9edb8a74104/plugin.js#L11
  // @ts-expect-error property 'default' does not exists on type ...
  if (typeof fastifyTRPCPlugin.default !== 'function') {
    prefix = ''; // handled by fastify internally
  }

  fastify.all(`${prefix}/:path`, async (req, res) => {
    const path = (req.params as any).path;
    await fastifyRequestHandler({ ...opts.trpcOptions, req, res, path });
  });

  if (opts.useWSS) {
    const trpcOptions =
      opts.trpcOptions as unknown as WSSHandlerOptions<TRouter>;

    const onConnection = getWSConnectionHandler<TRouter>({
      ...trpcOptions,
    });

    fastify.get(prefix ?? '/', { websocket: true }, (socket, req) => {
      // keepalive is registered by getWSConnectionHandler, which every
      // adapter goes through — registering it here as well gave each socket
      // two ping intervals and two pong-wait timers
      onConnection(socket, req.raw);
    });
  }

  done();
}
```


---

### 🔹 Commit #07: `210b6808`
- **完整 Hash**: `210b68080641a0e140624b5a1a57b50b5980c559`
- **說明 (Ground Truth)**: fix(react-query): support select() in useSuspenseInfiniteQuery (#7388)
- **變更檔案數**: 1

#### 📄 檔案: `packages/react-query/src/createTRPCReact.tsx`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:5, E:4, A:0) ➔ After(N:5, E:4, A:0)
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

### 🔹 Commit #08: `64a8b427`
- **完整 Hash**: `64a8b427a12a3724ca3490116c007b499b7682cf`
- **說明 (Ground Truth)**: fix(server): make batch stream content-type configurable (#7345)
- **變更檔案數**: 2

#### 📄 檔案: `packages/server/src/unstable-core-do-not-import/http/resolveResponse.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:55, E:52, A:2) ➔ After(N:55, E:52, A:2)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#abortSignal** `(Control)`
    └── ⚡ **on('abort')**
        └── 🎯 [TRIGGERS] `onAbort()`
  🌲 **#combinedAbort.signal** `(Control)`
    └── ⚡ **on('abort')**
        └── 🎯 [TRIGGERS] `cleanup()`
            └── 🎯 [CALLS] `clearTimeout (External/Unresolved)()`
            └── 🎯 [CALLS] `removeEventListener()()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'onError' 被深鎖在內部閉包 (scope:resolveResponse@after/packages/server/src/unstable-core-do-not-import/http/resolveResponse.ts:L255C8)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `resolveResponse()`
- **變更前簽章 (Before)**: `async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response>` (L255~L822)
- **變更後簽章 (After)**: `async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response>` (L255~L825)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response> {
  const { router, req } = opts;
  const headers = new Headers([['vary', 'trpc-accept, accept']]);
  const config = router._def._config;

  const url = new URL(req.url);

  if (req.method === 'HEAD') {
    // can be used for lambda warmup
    return new Response(null, {
      status: 204,
    });
  }

  const allowBatching = opts.allowBatching ?? opts.batching?.enabled ?? true;
  const allowMethodOverride =
    (opts.allowMethodOverride ?? false) && req.method === 'POST';

  type $Context = inferRouterContext<TRouter>;

  const infoTuple: ResultTuple<TRPCRequestInfo> = await run(async () => {
    try {
      return [
        undefined,
        await getRequestInfo({
          req,
          path: decodePath(opts.path),
          router,
          searchParams: url.searchParams,
          headers: opts.req.headers,
          url,
          maxBatchSize: opts.maxBatchSize,
        }),
      ];
    } catch (cause) {
      return [getTRPCErrorFromUnknown(cause), undefined];
    }
  });

  interface ContextManager {
    valueOrUndefined: () => $Context | undefined;
    value: () => $Context;
    create: (info: TRPCRequestInfo) => Promise<void>;
  }
  const ctxManager: ContextManager = run(() => {
    let result: ResultTuple<$Context> | undefined = undefined;
    return {
      valueOrUndefined: () => {
        if (!result) {
          return undefined;
        }
        return result[1];
      },
      value: () => {
        const [err, ctx] = result!;
        if (err) {
          throw err;
        }
        return ctx;
      },
      create: async (info) => {
        if (result) {
          throw new Error(
            'This should only be called once - report a bug in tRPC',
          );
        }
        try {
          const ctx = await opts.createContext({
            info,
          });
          result = [undefined, ctx];
        } catch (cause) {
          result = [getTRPCErrorFromUnknown(cause), undefined];
        }
      },
    };
  });

  const methodMapper = allowMethodOverride
    ? TYPE_ACCEPTED_METHOD_MAP_WITH_METHOD_OVERRIDE
    : TYPE_ACCEPTED_METHOD_MAP;

  /**
   * @deprecated
   */
  const isStreamCall = getAcceptHeader(req.headers) === 'application/jsonl';

  const experimentalSSE = config.sse?.enabled ?? true;
  try {
    const [infoError, info] = infoTuple;
    if (infoError) {
      throw infoError;
    }
    if (info.isBatchCall && !allowBatching) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batching is not enabled on the server`,
      });
    }
    /* istanbul ignore if -- @preserve */
    if (isStreamCall && !info.isBatchCall) {
      throw new TRPCError({
        message: `Streaming requests must be batched (you can do a batch of 1)`,
        code: 'BAD_REQUEST',
      });
    }
    await ctxManager.create(info);

    interface RPCResultOk {
      data: unknown;
      signal?: AbortSignal;
    }
    type RPCResult = ResultTuple<RPCResultOk>;
    const bodyCancelled = new AbortController();
    const callSignal = abortSignalsAnyPonyfill([
      opts.req.signal,
      bodyCancelled.signal,
    ]);
    const rpcCalls = info.calls.map(async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    });

    // ----------- response handlers -----------
    if (!info.isBatchCall) {
      const [call] = info.calls;
      const [error, result] = await rpcCalls[0]!;

      switch (info.type) {
        case 'unknown':
        case 'mutation':
        case 'query': {
          // httpLink
          headers.set('content-type', 'application/json');

          if (isDataStream(result?.data)) {
            throw new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            });
          }
          const res: TRPCResponse<unknown, inferRouterError<TRouter>> = error
            ? {
                error: getErrorShape({
                  config,
                  ctx: ctxManager.valueOrUndefined(),
                  error,
                  input: call!.result(),
                  path: call!.path,
                  type: info.type,
                }),
              }
            : { result: { data: result.data } };

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: error ? [error] : [],
            headers,
            untransformedJSON: [res],
          });
          return new Response(
            JSON.stringify(transformTRPCResponse(config, res)),
            {
              status: headResponse.status,
              headers,
            },
          );
        }
        case 'subscription': {
          // httpSubscriptionLink

          const iterable: AsyncIterable<unknown> = run(() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, callSignal)
              : result.data;
            return dataAsIterable;
          });

          const stream = sseStreamProducer({
            ...config.sse,
            lastEventId: getLastEventId({
              headers: req.headers,
              searchParams: url.searchParams,
            }),
            data: iterable,
            serialize: (v) => config.transformer.output.serialize(v),
            formatError(errorOpts) {
              const error = getTRPCErrorFromUnknown(errorOpts.error);
              const input = call?.result();
              const path = call?.path;
              const type = call?.procedure?._def.type ?? 'unknown';

              opts.onError?.({
                error,
                path,
                input,
                ctx: ctxManager.valueOrUndefined(),
                req: opts.req,
                type,
              });

              const shape = getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input,
                path,
                type,
              });

              return shape;
            },
          });
          for (const [key, value] of Object.entries(sseHeaders)) {
            headers.set(key, value);
          }

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: [],
            headers,
            untransformedJSON: null,
          });

          const abortSignal = result?.signal;
          let responseBody: ReadableStream<Uint8Array> = stream;

          // Fixes: https://github.com/trpc/trpc/issues/7094
          if (abortSignal) {
            const reader = stream.getReader();
            const onAbort = () => void reader.cancel();
            if (abortSignal.aborted) {
              onAbort();
            } else {
              abortSignal.addEventListener('abort', onAbort, { once: true });
            }

            responseBody = new ReadableStream({
              async pull(controller) {
                const chunk = await reader.read();
                if (chunk.done) {
                  abortSignal.removeEventListener('abort', onAbort);
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              },
              cancel() {
                abortSignal.removeEventListener('abort', onAbort);
                bodyCancelled.abort();
                return reader.cancel();
              },
            });
          }

          return new Response(responseBody, {
            headers,
            status: headResponse.status,
          });
        }
      }
    }

    // batch response handlers
    if (info.accept === 'application/jsonl') {
      // httpBatchStreamLink
      headers.set('content-type', 'application/json');
      headers.set('transfer-encoding', 'chunked');
      const headResponse = initResponse({
        ctx: ctxManager.valueOrUndefined(),
        info,
        responseMeta: opts.responseMeta,
        errors: [],
        headers,
        untransformedJSON: null,
      });
      const stream = jsonlStreamProducer({
        ...config.jsonl,
        /**
         * Example structure for `maxDepth: 4`:
         * {
         *   // 1
         *   0: {
         *     // 2
         *     result: {
         *       // 3
         *       data: // 4
         *     }
         *   }
         * }
         */
        maxDepth: Infinity,
        data: rpcCalls.map(async (res, index) => {
          const [error, result] = await res;

          const call = info.calls[index];

          if (error) {
            return {
              error: getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input: call!.result(),
                path: call!.path,
                type: call!.procedure?._def.type ?? 'unknown',
              }),
            };
          }

          /**
           * Not very pretty, but we need to wrap nested data in promises
           * Our stream producer will only resolve top-level async values or async values that are directly nested in another async value
           */
          const iterable = isObservable(result.data)
            ? observableToAsyncIterable(result.data, callSignal)
            : Promise.resolve(result.data);
          return {
            result: Promise.resolve({
              data: iterable,
            }),
          };
        }),
        serialize: (data) => config.transformer.output.serialize(data),
        onError: (cause) => {
          opts.onError?.({
            error: getTRPCErrorFromUnknown(cause.error),
            path: undefined,
            input: undefined,
            ctx: ctxManager.valueOrUndefined(),
            req: opts.req,
            type: info?.type ?? 'unknown',
          });
        },

        formatError(errorOpts) {
          const call = info?.calls[errorOpts.path[0] as any];

          const error = getTRPCErrorFromUnknown(errorOpts.error);
          const input = call?.result();
          const path = call?.path;
          const type = call?.procedure?._def.type ?? 'unknown';

          // no need to call `onError` here as it will be propagated through the stream itself

          const shape = getErrorShape({
            config,
            ctx: ctxManager.valueOrUndefined(),
            error,
            input,
            path,
            type,
          });

          return shape;
        },
      });

      return new Response(abortOnCancel(stream, bodyCancelled), {
        headers,
        status: headResponse.status,
      });
    }

    // httpBatchLink
    /**
     * Non-streaming response:
     * - await all responses in parallel, blocking on the slowest one
     * - create headers with known response body
     * - return a complete HTTPResponse
     */
    headers.set('content-type', 'application/json');
    const results: RPCResult[] = (await Promise.all(rpcCalls)).map(
      (res): RPCResult => {
        const [error, result] = res;
        if (error) {
          return res;
        }

        if (isDataStream(result.data)) {
          return [
            new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            }),
            undefined,
          ];
        }
        return res;
      },
    );
    const resultAsRPCResponse = results.map(
      (
        [error, result],
        index,
      ): TRPCResponse<unknown, inferRouterError<TRouter>> => {
        const call = info.calls[index]!;
        if (error) {
          return {
            error: getErrorShape({
              config,
              ctx: ctxManager.valueOrUndefined(),
              error,
              input: call.result(),
              path: call.path,
              type: call.procedure?._def.type ?? 'unknown',
            }),
          };
        }
        return {
          result: { data: result.data },
        };
      },
    );

    const errors = results
      .map(([error]) => error)
      .filter(Boolean) as TRPCError[];

    const headResponse = initResponse({
      ctx: ctxManager.valueOrUndefined(),
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON: resultAsRPCResponse,
      errors,
      headers,
    });

    return new Response(
      JSON.stringify(transformTRPCResponse(config, resultAsRPCResponse)),
      {
        status: headResponse.status,
        headers,
      },
    );
  } catch (cause) {
    const [_infoError, info] = infoTuple;
    const ctx = ctxManager.valueOrUndefined();
    // we get here if
    // - batching is called when it's not enabled
    // - `createContext()` throws
    // - `router._def._config.transformer.output.serialize()` throws
    // - post body is too large
    // - input deserialization fails
    // - `errorFormatter` return value is malformed
    const { error, untransformedJSON, body } = caughtErrorToData(cause, {
      opts,
      ctx: ctxManager.valueOrUndefined(),
      type: info?.type ?? 'unknown',
    });

    const headResponse = initResponse({
      ctx,
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON,
      errors: [error],
      headers,
    });

    return new Response(body, {
      status: headResponse.status,
      headers,
    });
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response> {
  const { router, req } = opts;
  const headers = new Headers([['vary', 'trpc-accept, accept']]);
  const config = router._def._config;

  const url = new URL(req.url);

  if (req.method === 'HEAD') {
    // can be used for lambda warmup
    return new Response(null, {
      status: 204,
    });
  }

  const allowBatching = opts.allowBatching ?? opts.batching?.enabled ?? true;
  const allowMethodOverride =
    (opts.allowMethodOverride ?? false) && req.method === 'POST';

  type $Context = inferRouterContext<TRouter>;

  const infoTuple: ResultTuple<TRPCRequestInfo> = await run(async () => {
    try {
      return [
        undefined,
        await getRequestInfo({
          req,
          path: decodePath(opts.path),
          router,
          searchParams: url.searchParams,
          headers: opts.req.headers,
          url,
          maxBatchSize: opts.maxBatchSize,
        }),
      ];
    } catch (cause) {
      return [getTRPCErrorFromUnknown(cause), undefined];
    }
  });

  interface ContextManager {
    valueOrUndefined: () => $Context | undefined;
    value: () => $Context;
    create: (info: TRPCRequestInfo) => Promise<void>;
  }
  const ctxManager: ContextManager = run(() => {
    let result: ResultTuple<$Context> | undefined = undefined;
    return {
      valueOrUndefined: () => {
        if (!result) {
          return undefined;
        }
        return result[1];
      },
      value: () => {
        const [err, ctx] = result!;
        if (err) {
          throw err;
        }
        return ctx;
      },
      create: async (info) => {
        if (result) {
          throw new Error(
            'This should only be called once - report a bug in tRPC',
          );
        }
        try {
          const ctx = await opts.createContext({
            info,
          });
          result = [undefined, ctx];
        } catch (cause) {
          result = [getTRPCErrorFromUnknown(cause), undefined];
        }
      },
    };
  });

  const methodMapper = allowMethodOverride
    ? TYPE_ACCEPTED_METHOD_MAP_WITH_METHOD_OVERRIDE
    : TYPE_ACCEPTED_METHOD_MAP;

  /**
   * @deprecated
   */
  const isStreamCall = getAcceptHeader(req.headers) === 'application/jsonl';

  const experimentalSSE = config.sse?.enabled ?? true;
  try {
    const [infoError, info] = infoTuple;
    if (infoError) {
      throw infoError;
    }
    if (info.isBatchCall && !allowBatching) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batching is not enabled on the server`,
      });
    }
    /* istanbul ignore if -- @preserve */
    if (isStreamCall && !info.isBatchCall) {
      throw new TRPCError({
        message: `Streaming requests must be batched (you can do a batch of 1)`,
        code: 'BAD_REQUEST',
      });
    }
    await ctxManager.create(info);

    interface RPCResultOk {
      data: unknown;
      signal?: AbortSignal;
    }
    type RPCResult = ResultTuple<RPCResultOk>;
    const bodyCancelled = new AbortController();
    const callSignal = abortSignalsAnyPonyfill([
      opts.req.signal,
      bodyCancelled.signal,
    ]);
    const rpcCalls = info.calls.map(async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    });

    // ----------- response handlers -----------
    if (!info.isBatchCall) {
      const [call] = info.calls;
      const [error, result] = await rpcCalls[0]!;

      switch (info.type) {
        case 'unknown':
        case 'mutation':
        case 'query': {
          // httpLink
          headers.set('content-type', 'application/json');

          if (isDataStream(result?.data)) {
            throw new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            });
          }
          const res: TRPCResponse<unknown, inferRouterError<TRouter>> = error
            ? {
                error: getErrorShape({
                  config,
                  ctx: ctxManager.valueOrUndefined(),
                  error,
                  input: call!.result(),
                  path: call!.path,
                  type: info.type,
                }),
              }
            : { result: { data: result.data } };

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: error ? [error] : [],
            headers,
            untransformedJSON: [res],
          });
          return new Response(
            JSON.stringify(transformTRPCResponse(config, res)),
            {
              status: headResponse.status,
              headers,
            },
          );
        }
        case 'subscription': {
          // httpSubscriptionLink

          const iterable: AsyncIterable<unknown> = run(() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, callSignal)
              : result.data;
            return dataAsIterable;
          });

          const stream = sseStreamProducer({
            ...config.sse,
            lastEventId: getLastEventId({
              headers: req.headers,
              searchParams: url.searchParams,
            }),
            data: iterable,
            serialize: (v) => config.transformer.output.serialize(v),
            formatError(errorOpts) {
              const error = getTRPCErrorFromUnknown(errorOpts.error);
              const input = call?.result();
              const path = call?.path;
              const type = call?.procedure?._def.type ?? 'unknown';

              opts.onError?.({
                error,
                path,
                input,
                ctx: ctxManager.valueOrUndefined(),
                req: opts.req,
                type,
              });

              const shape = getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input,
                path,
                type,
              });

              return shape;
            },
          });
          for (const [key, value] of Object.entries(sseHeaders)) {
            headers.set(key, value);
          }

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: [],
            headers,
            untransformedJSON: null,
          });

          const abortSignal = result?.signal;
          let responseBody: ReadableStream<Uint8Array> = stream;

          // Fixes: https://github.com/trpc/trpc/issues/7094
          if (abortSignal) {
            const reader = stream.getReader();
            const onAbort = () => void reader.cancel();
            if (abortSignal.aborted) {
              onAbort();
            } else {
              abortSignal.addEventListener('abort', onAbort, { once: true });
            }

            responseBody = new ReadableStream({
              async pull(controller) {
                const chunk = await reader.read();
                if (chunk.done) {
                  abortSignal.removeEventListener('abort', onAbort);
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              },
              cancel() {
                abortSignal.removeEventListener('abort', onAbort);
                bodyCancelled.abort();
                return reader.cancel();
              },
            });
          }

          return new Response(responseBody, {
            headers,
            status: headResponse.status,
          });
        }
      }
    }

    // batch response handlers
    if (info.accept === 'application/jsonl') {
      // httpBatchStreamLink
      headers.set(
        'content-type',
        config.jsonl?.contentType ?? 'application/json',
      );
      headers.set('transfer-encoding', 'chunked');
      const headResponse = initResponse({
        ctx: ctxManager.valueOrUndefined(),
        info,
        responseMeta: opts.responseMeta,
        errors: [],
        headers,
        untransformedJSON: null,
      });
      const stream = jsonlStreamProducer({
        ...config.jsonl,
        /**
         * Example structure for `maxDepth: 4`:
         * {
         *   // 1
         *   0: {
         *     // 2
         *     result: {
         *       // 3
         *       data: // 4
         *     }
         *   }
         * }
         */
        maxDepth: Infinity,
        data: rpcCalls.map(async (res, index) => {
          const [error, result] = await res;

          const call = info.calls[index];

          if (error) {
            return {
              error: getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input: call!.result(),
                path: call!.path,
                type: call!.procedure?._def.type ?? 'unknown',
              }),
            };
          }

          /**
           * Not very pretty, but we need to wrap nested data in promises
           * Our stream producer will only resolve top-level async values or async values that are directly nested in another async value
           */
          const iterable = isObservable(result.data)
            ? observableToAsyncIterable(result.data, callSignal)
            : Promise.resolve(result.data);
          return {
            result: Promise.resolve({
              data: iterable,
            }),
          };
        }),
        serialize: (data) => config.transformer.output.serialize(data),
        onError: (cause) => {
          opts.onError?.({
            error: getTRPCErrorFromUnknown(cause.error),
            path: undefined,
            input: undefined,
            ctx: ctxManager.valueOrUndefined(),
            req: opts.req,
            type: info?.type ?? 'unknown',
          });
        },

        formatError(errorOpts) {
          const call = info?.calls[errorOpts.path[0] as any];

          const error = getTRPCErrorFromUnknown(errorOpts.error);
          const input = call?.result();
          const path = call?.path;
          const type = call?.procedure?._def.type ?? 'unknown';

          // no need to call `onError` here as it will be propagated through the stream itself

          const shape = getErrorShape({
            config,
            ctx: ctxManager.valueOrUndefined(),
            error,
            input,
            path,
            type,
          });

          return shape;
        },
      });

      return new Response(abortOnCancel(stream, bodyCancelled), {
        headers,
        status: headResponse.status,
      });
    }

    // httpBatchLink
    /**
     * Non-streaming response:
     * - await all responses in parallel, blocking on the slowest one
     * - create headers with known response body
     * - return a complete HTTPResponse
     */
    headers.set('content-type', 'application/json');
    const results: RPCResult[] = (await Promise.all(rpcCalls)).map(
      (res): RPCResult => {
        const [error, result] = res;
        if (error) {
          return res;
        }

        if (isDataStream(result.data)) {
          return [
            new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            }),
            undefined,
          ];
        }
        return res;
      },
    );
    const resultAsRPCResponse = results.map(
      (
        [error, result],
        index,
      ): TRPCResponse<unknown, inferRouterError<TRouter>> => {
        const call = info.calls[index]!;
        if (error) {
          return {
            error: getErrorShape({
              config,
              ctx: ctxManager.valueOrUndefined(),
              error,
              input: call.result(),
              path: call.path,
              type: call.procedure?._def.type ?? 'unknown',
            }),
          };
        }
        return {
          result: { data: result.data },
        };
      },
    );

    const errors = results
      .map(([error]) => error)
      .filter(Boolean) as TRPCError[];

    const headResponse = initResponse({
      ctx: ctxManager.valueOrUndefined(),
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON: resultAsRPCResponse,
      errors,
      headers,
    });

    return new Response(
      JSON.stringify(transformTRPCResponse(config, resultAsRPCResponse)),
      {
        status: headResponse.status,
        headers,
      },
    );
  } catch (cause) {
    const [_infoError, info] = infoTuple;
    const ctx = ctxManager.valueOrUndefined();
    // we get here if
    // - batching is called when it's not enabled
    // - `createContext()` throws
    // - `router._def._config.transformer.output.serialize()` throws
    // - post body is too large
    // - input deserialization fails
    // - `errorFormatter` return value is malformed
    const { error, untransformedJSON, body } = caughtErrorToData(cause, {
      opts,
      ctx: ctxManager.valueOrUndefined(),
      type: info?.type ?? 'unknown',
    });

    const headResponse = initResponse({
      ctx,
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON,
      errors: [error],
      headers,
    });

    return new Response(body, {
      status: headResponse.status,
      headers,
    });
  }
}
```


#### 📄 檔案: `packages/server/src/unstable-core-do-not-import/rootConfig.ts`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:2, E:0, A:0) ➔ After(N:2, E:0, A:0)
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

### 🔹 Commit #09: `d8caf504`
- **完整 Hash**: `d8caf50471b533d7342cff4dce7a9a3f01b8594e`
- **說明 (Ground Truth)**: fix(server): stop untracked SSE events inheriting the previous tracked id (#7691)
- **變更檔案數**: 3

#### 📄 檔案: `packages/server/src/unstable-core-do-not-import/http/contentType.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:28, E:16, A:0) ➔ After(N:29, E:17, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `getLastEventId` (FUNCTION_DEF)
  • + [新增呼叫邊] `getRawInput` ──[CALLS [guard: (procedure?._def.type === 'subscription')]]──> `getLastEventId`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `jsonContentTypeHandler()`
- **變更前簽章 (Before)**: `[Module State] jsonContentTypeHandler` (L87~L221)
- **變更後簽章 (After)**: `[Module State] jsonContentTypeHandler` (L98~L229)

#### ◀️ 變更前實作碼 (Before Implementation):
```
jsonContentTypeHandler: ContentTypeHandler = {
  isMatch(req) {
    return hasContentType(req, 'application/json');
  },
  async parse(opts) {
    const { req } = opts;
    const isBatchCall = opts.searchParams.get('batch') === '1';
    const maxBatchSize = opts.maxBatchSize;

    const paths = isBatchCall ? opts.path.split(',') : [opts.path];
    if (
      isBatchCall &&
      typeof maxBatchSize === 'number' &&
      paths.length > maxBatchSize
    ) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batch call exceeds maximum size`,
      });
    }

    type InputRecord = Record<number, unknown>;
    const getInputs = memo(async (): Promise<InputRecord> => {
      let inputs: unknown = undefined;
      if (req.method === 'GET') {
        const queryInput = opts.searchParams.get('input');
        if (queryInput) {
          inputs = JSON.parse(queryInput);
        }
      } else {
        inputs = await req.json();
      }
      if (inputs === undefined) {
        return emptyObject();
      }

      if (!isBatchCall) {
        const result: InputRecord = emptyObject();
        result[0] =
          opts.router._def._config.transformer.input.deserialize(inputs);
        return result;
      }

      if (!isObject(inputs)) {
        throw new TRPCError({
          code: 'BAD_REQUEST',
          message: '"input" needs to be an object when doing a batch call',
        });
      }
      const acc: InputRecord = emptyObject();
      for (const index of paths.keys()) {
        const input = inputs[index];
        if (input !== undefined) {
          acc[index] =
            opts.router._def._config.transformer.input.deserialize(input);
        }
      }

      return acc;
    });

    const calls = await Promise.all(
      paths.map(
        async (path, index): Promise<TRPCRequestInfo['calls'][number]> => {
          const procedure = await getProcedureAtPath(opts.router, path);
          return {
            batchIndex: index,
            path,
            procedure,
            getRawInput: async () => {
              const inputs = await getInputs.read();
              let input = inputs[index];

              if (procedure?._def.type === 'subscription') {
                const lastEventId =
                  opts.headers.get('last-event-id') ??
                  opts.searchParams.get('lastEventId') ??
                  opts.searchParams.get('Last-Event-Id');

                if (lastEventId) {
                  if (isObject(input)) {
                    input = {
                      ...input,
                      lastEventId: lastEventId,
                    };
                  } else {
                    input ??= {
                      lastEventId: lastEventId,
                    };
                  }
                }
              }
              return input;
            },
            result: () => {
              return getInputs.result()?.[index];
            },
          };
        },
      ),
    );

    const types = new Set(
      calls.map((call) => call.procedure?._def.type).filter(Boolean),
    );

    /* istanbul ignore if -- @preserve */
    if (types.size > 1) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Cannot mix procedure types in call: ${Array.from(types).join(
          ', ',
        )}`,
      });
    }
    const type: ProcedureType | 'unknown' =
      types.values().next().value ?? 'unknown';

    const connectionParamsStr = opts.searchParams.get('connectionParams');

    const info: TRPCRequestInfo = {
      isBatchCall,
      accept: getAcceptHeader(req.headers),
      calls,
      type,
      connectionParams:
        connectionParamsStr === null
          ? null
          : parseConnectionParamsFromString(connectionParamsStr),
      signal: req.signal,
      url: opts.url,
    };
    return info;
  },
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
jsonContentTypeHandler: ContentTypeHandler = {
  isMatch(req) {
    return hasContentType(req, 'application/json');
  },
  async parse(opts) {
    const { req } = opts;
    const isBatchCall = opts.searchParams.get('batch') === '1';
    const maxBatchSize = opts.maxBatchSize;

    const paths = isBatchCall ? opts.path.split(',') : [opts.path];
    if (
      isBatchCall &&
      typeof maxBatchSize === 'number' &&
      paths.length > maxBatchSize
    ) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batch call exceeds maximum size`,
      });
    }

    type InputRecord = Record<number, unknown>;
    const getInputs = memo(async (): Promise<InputRecord> => {
      let inputs: unknown = undefined;
      if (req.method === 'GET') {
        const queryInput = opts.searchParams.get('input');
        if (queryInput) {
          inputs = JSON.parse(queryInput);
        }
      } else {
        inputs = await req.json();
      }
      if (inputs === undefined) {
        return emptyObject();
      }

      if (!isBatchCall) {
        const result: InputRecord = emptyObject();
        result[0] =
          opts.router._def._config.transformer.input.deserialize(inputs);
        return result;
      }

      if (!isObject(inputs)) {
        throw new TRPCError({
          code: 'BAD_REQUEST',
          message: '"input" needs to be an object when doing a batch call',
        });
      }
      const acc: InputRecord = emptyObject();
      for (const index of paths.keys()) {
        const input = inputs[index];
        if (input !== undefined) {
          acc[index] =
            opts.router._def._config.transformer.input.deserialize(input);
        }
      }

      return acc;
    });

    const calls = await Promise.all(
      paths.map(
        async (path, index): Promise<TRPCRequestInfo['calls'][number]> => {
          const procedure = await getProcedureAtPath(opts.router, path);
          return {
            batchIndex: index,
            path,
            procedure,
            getRawInput: async () => {
              const inputs = await getInputs.read();
              let input = inputs[index];

              if (procedure?._def.type === 'subscription') {
                const lastEventId = getLastEventId(opts);

                if (lastEventId) {
                  if (isObject(input)) {
                    input = {
                      ...input,
                      lastEventId: lastEventId,
                    };
                  } else {
                    input ??= {
                      lastEventId: lastEventId,
                    };
                  }
                }
              }
              return input;
            },
            result: () => {
              return getInputs.result()?.[index];
            },
          };
        },
      ),
    );

    const types = new Set(
      calls.map((call) => call.procedure?._def.type).filter(Boolean),
    );

    /* istanbul ignore if -- @preserve */
    if (types.size > 1) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Cannot mix procedure types in call: ${Array.from(types).join(
          ', ',
        )}`,
      });
    }
    const type: ProcedureType | 'unknown' =
      types.values().next().value ?? 'unknown';

    const connectionParamsStr = opts.searchParams.get('connectionParams');

    const info: TRPCRequestInfo = {
      isBatchCall,
      accept: getAcceptHeader(req.headers),
      calls,
      type,
      connectionParams:
        connectionParamsStr === null
          ? null
          : parseConnectionParamsFromString(connectionParamsStr),
      signal: req.signal,
      url: opts.url,
    };
    return info;
  },
}
```

### 🔹 函式: `parse()`
- **變更前簽章 (Before)**: `parse(opts)` (L91~L220)
- **變更後簽章 (After)**: `parse(opts)` (L102~L228)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async parse(opts) {
    const { req } = opts;
    const isBatchCall = opts.searchParams.get('batch') === '1';
    const maxBatchSize = opts.maxBatchSize;

    const paths = isBatchCall ? opts.path.split(',') : [opts.path];
    if (
      isBatchCall &&
      typeof maxBatchSize === 'number' &&
      paths.length > maxBatchSize
    ) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batch call exceeds maximum size`,
      });
    }

    type InputRecord = Record<number, unknown>;
    const getInputs = memo(async (): Promise<InputRecord> => {
      let inputs: unknown = undefined;
      if (req.method === 'GET') {
        const queryInput = opts.searchParams.get('input');
        if (queryInput) {
          inputs = JSON.parse(queryInput);
        }
      } else {
        inputs = await req.json();
      }
      if (inputs === undefined) {
        return emptyObject();
      }

      if (!isBatchCall) {
        const result: InputRecord = emptyObject();
        result[0] =
          opts.router._def._config.transformer.input.deserialize(inputs);
        return result;
      }

      if (!isObject(inputs)) {
        throw new TRPCError({
          code: 'BAD_REQUEST',
          message: '"input" needs to be an object when doing a batch call',
        });
      }
      const acc: InputRecord = emptyObject();
      for (const index of paths.keys()) {
        const input = inputs[index];
        if (input !== undefined) {
          acc[index] =
            opts.router._def._config.transformer.input.deserialize(input);
        }
      }

      return acc;
    });

    const calls = await Promise.all(
      paths.map(
        async (path, index): Promise<TRPCRequestInfo['calls'][number]> => {
          const procedure = await getProcedureAtPath(opts.router, path);
          return {
            batchIndex: index,
            path,
            procedure,
            getRawInput: async () => {
              const inputs = await getInputs.read();
              let input = inputs[index];

              if (procedure?._def.type === 'subscription') {
                const lastEventId =
                  opts.headers.get('last-event-id') ??
                  opts.searchParams.get('lastEventId') ??
                  opts.searchParams.get('Last-Event-Id');

                if (lastEventId) {
                  if (isObject(input)) {
                    input = {
                      ...input,
                      lastEventId: lastEventId,
                    };
                  } else {
                    input ??= {
                      lastEventId: lastEventId,
                    };
                  }
                }
              }
              return input;
            },
            result: () => {
              return getInputs.result()?.[index];
            },
          };
        },
      ),
    );

    const types = new Set(
      calls.map((call) => call.procedure?._def.type).filter(Boolean),
    );

    /* istanbul ignore if -- @preserve */
    if (types.size > 1) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Cannot mix procedure types in call: ${Array.from(types).join(
          ', ',
        )}`,
      });
    }
    const type: ProcedureType | 'unknown' =
      types.values().next().value ?? 'unknown';

    const connectionParamsStr = opts.searchParams.get('connectionParams');

    const info: TRPCRequestInfo = {
      isBatchCall,
      accept: getAcceptHeader(req.headers),
      calls,
      type,
      connectionParams:
        connectionParamsStr === null
          ? null
          : parseConnectionParamsFromString(connectionParamsStr),
      signal: req.signal,
      url: opts.url,
    };
    return info;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async parse(opts) {
    const { req } = opts;
    const isBatchCall = opts.searchParams.get('batch') === '1';
    const maxBatchSize = opts.maxBatchSize;

    const paths = isBatchCall ? opts.path.split(',') : [opts.path];
    if (
      isBatchCall &&
      typeof maxBatchSize === 'number' &&
      paths.length > maxBatchSize
    ) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batch call exceeds maximum size`,
      });
    }

    type InputRecord = Record<number, unknown>;
    const getInputs = memo(async (): Promise<InputRecord> => {
      let inputs: unknown = undefined;
      if (req.method === 'GET') {
        const queryInput = opts.searchParams.get('input');
        if (queryInput) {
          inputs = JSON.parse(queryInput);
        }
      } else {
        inputs = await req.json();
      }
      if (inputs === undefined) {
        return emptyObject();
      }

      if (!isBatchCall) {
        const result: InputRecord = emptyObject();
        result[0] =
          opts.router._def._config.transformer.input.deserialize(inputs);
        return result;
      }

      if (!isObject(inputs)) {
        throw new TRPCError({
          code: 'BAD_REQUEST',
          message: '"input" needs to be an object when doing a batch call',
        });
      }
      const acc: InputRecord = emptyObject();
      for (const index of paths.keys()) {
        const input = inputs[index];
        if (input !== undefined) {
          acc[index] =
            opts.router._def._config.transformer.input.deserialize(input);
        }
      }

      return acc;
    });

    const calls = await Promise.all(
      paths.map(
        async (path, index): Promise<TRPCRequestInfo['calls'][number]> => {
          const procedure = await getProcedureAtPath(opts.router, path);
          return {
            batchIndex: index,
            path,
            procedure,
            getRawInput: async () => {
              const inputs = await getInputs.read();
              let input = inputs[index];

              if (procedure?._def.type === 'subscription') {
                const lastEventId = getLastEventId(opts);

                if (lastEventId) {
                  if (isObject(input)) {
                    input = {
                      ...input,
                      lastEventId: lastEventId,
                    };
                  } else {
                    input ??= {
                      lastEventId: lastEventId,
                    };
                  }
                }
              }
              return input;
            },
            result: () => {
              return getInputs.result()?.[index];
            },
          };
        },
      ),
    );

    const types = new Set(
      calls.map((call) => call.procedure?._def.type).filter(Boolean),
    );

    /* istanbul ignore if -- @preserve */
    if (types.size > 1) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Cannot mix procedure types in call: ${Array.from(types).join(
          ', ',
        )}`,
      });
    }
    const type: ProcedureType | 'unknown' =
      types.values().next().value ?? 'unknown';

    const connectionParamsStr = opts.searchParams.get('connectionParams');

    const info: TRPCRequestInfo = {
      isBatchCall,
      accept: getAcceptHeader(req.headers),
      calls,
      type,
      connectionParams:
        connectionParamsStr === null
          ? null
          : parseConnectionParamsFromString(connectionParamsStr),
      signal: req.signal,
      url: opts.url,
    };
    return info;
  }
```

### 🔹 函式: `getRawInput()`
- **變更前簽章 (Before)**: `getRawInput()` (L156~L180)
- **變更後簽章 (After)**: `getRawInput()` (L167~L188)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async () => {
              const inputs = await getInputs.read();
              let input = inputs[index];

              if (procedure?._def.type === 'subscription') {
                const lastEventId =
                  opts.headers.get('last-event-id') ??
                  opts.searchParams.get('lastEventId') ??
                  opts.searchParams.get('Last-Event-Id');

                if (lastEventId) {
                  if (isObject(input)) {
                    input = {
                      ...input,
                      lastEventId: lastEventId,
                    };
                  } else {
                    input ??= {
                      lastEventId: lastEventId,
                    };
                  }
                }
              }
              return input;
            }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async () => {
              const inputs = await getInputs.read();
              let input = inputs[index];

              if (procedure?._def.type === 'subscription') {
                const lastEventId = getLastEventId(opts);

                if (lastEventId) {
                  if (isObject(input)) {
                    input = {
                      ...input,
                      lastEventId: lastEventId,
                    };
                  } else {
                    input ??= {
                      lastEventId: lastEventId,
                    };
                  }
                }
              }
              return input;
            }
```


#### 📄 檔案: `packages/server/src/unstable-core-do-not-import/http/resolveResponse.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:54, E:51, A:2) ➔ After(N:55, E:52, A:2)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#abortSignal** `(Control)`
    └── ⚡ **on('abort')**
        └── 🎯 [TRIGGERS] `onAbort()`
  🌲 **#combinedAbort.signal** `(Control)`
    └── ⚡ **on('abort')**
        └── 🎯 [TRIGGERS] `cleanup()`
            └── 🎯 [CALLS] `clearTimeout (External/Unresolved)()`
            └── 🎯 [CALLS] `removeEventListener()()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `getLastEventId (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `resolveResponse` ──[CALLS [guard: (!info.isBatchCall)]]──> `getLastEventId (External/Unresolved)`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'onError' 被深鎖在內部閉包 (scope:resolveResponse@after/packages/server/src/unstable-core-do-not-import/http/resolveResponse.ts:L255C8)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `resolveResponse()`
- **變更前簽章 (Before)**: `async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response>` (L255~L818)
- **變更後簽章 (After)**: `async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response>` (L255~L822)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response> {
  const { router, req } = opts;
  const headers = new Headers([['vary', 'trpc-accept, accept']]);
  const config = router._def._config;

  const url = new URL(req.url);

  if (req.method === 'HEAD') {
    // can be used for lambda warmup
    return new Response(null, {
      status: 204,
    });
  }

  const allowBatching = opts.allowBatching ?? opts.batching?.enabled ?? true;
  const allowMethodOverride =
    (opts.allowMethodOverride ?? false) && req.method === 'POST';

  type $Context = inferRouterContext<TRouter>;

  const infoTuple: ResultTuple<TRPCRequestInfo> = await run(async () => {
    try {
      return [
        undefined,
        await getRequestInfo({
          req,
          path: decodePath(opts.path),
          router,
          searchParams: url.searchParams,
          headers: opts.req.headers,
          url,
          maxBatchSize: opts.maxBatchSize,
        }),
      ];
    } catch (cause) {
      return [getTRPCErrorFromUnknown(cause), undefined];
    }
  });

  interface ContextManager {
    valueOrUndefined: () => $Context | undefined;
    value: () => $Context;
    create: (info: TRPCRequestInfo) => Promise<void>;
  }
  const ctxManager: ContextManager = run(() => {
    let result: ResultTuple<$Context> | undefined = undefined;
    return {
      valueOrUndefined: () => {
        if (!result) {
          return undefined;
        }
        return result[1];
      },
      value: () => {
        const [err, ctx] = result!;
        if (err) {
          throw err;
        }
        return ctx;
      },
      create: async (info) => {
        if (result) {
          throw new Error(
            'This should only be called once - report a bug in tRPC',
          );
        }
        try {
          const ctx = await opts.createContext({
            info,
          });
          result = [undefined, ctx];
        } catch (cause) {
          result = [getTRPCErrorFromUnknown(cause), undefined];
        }
      },
    };
  });

  const methodMapper = allowMethodOverride
    ? TYPE_ACCEPTED_METHOD_MAP_WITH_METHOD_OVERRIDE
    : TYPE_ACCEPTED_METHOD_MAP;

  /**
   * @deprecated
   */
  const isStreamCall = getAcceptHeader(req.headers) === 'application/jsonl';

  const experimentalSSE = config.sse?.enabled ?? true;
  try {
    const [infoError, info] = infoTuple;
    if (infoError) {
      throw infoError;
    }
    if (info.isBatchCall && !allowBatching) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batching is not enabled on the server`,
      });
    }
    /* istanbul ignore if -- @preserve */
    if (isStreamCall && !info.isBatchCall) {
      throw new TRPCError({
        message: `Streaming requests must be batched (you can do a batch of 1)`,
        code: 'BAD_REQUEST',
      });
    }
    await ctxManager.create(info);

    interface RPCResultOk {
      data: unknown;
      signal?: AbortSignal;
    }
    type RPCResult = ResultTuple<RPCResultOk>;
    const bodyCancelled = new AbortController();
    const callSignal = abortSignalsAnyPonyfill([
      opts.req.signal,
      bodyCancelled.signal,
    ]);
    const rpcCalls = info.calls.map(async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    });

    // ----------- response handlers -----------
    if (!info.isBatchCall) {
      const [call] = info.calls;
      const [error, result] = await rpcCalls[0]!;

      switch (info.type) {
        case 'unknown':
        case 'mutation':
        case 'query': {
          // httpLink
          headers.set('content-type', 'application/json');

          if (isDataStream(result?.data)) {
            throw new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            });
          }
          const res: TRPCResponse<unknown, inferRouterError<TRouter>> = error
            ? {
                error: getErrorShape({
                  config,
                  ctx: ctxManager.valueOrUndefined(),
                  error,
                  input: call!.result(),
                  path: call!.path,
                  type: info.type,
                }),
              }
            : { result: { data: result.data } };

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: error ? [error] : [],
            headers,
            untransformedJSON: [res],
          });
          return new Response(
            JSON.stringify(transformTRPCResponse(config, res)),
            {
              status: headResponse.status,
              headers,
            },
          );
        }
        case 'subscription': {
          // httpSubscriptionLink

          const iterable: AsyncIterable<unknown> = run(() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, callSignal)
              : result.data;
            return dataAsIterable;
          });

          const stream = sseStreamProducer({
            ...config.sse,
            data: iterable,
            serialize: (v) => config.transformer.output.serialize(v),
            formatError(errorOpts) {
              const error = getTRPCErrorFromUnknown(errorOpts.error);
              const input = call?.result();
              const path = call?.path;
              const type = call?.procedure?._def.type ?? 'unknown';

              opts.onError?.({
                error,
                path,
                input,
                ctx: ctxManager.valueOrUndefined(),
                req: opts.req,
                type,
              });

              const shape = getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input,
                path,
                type,
              });

              return shape;
            },
          });
          for (const [key, value] of Object.entries(sseHeaders)) {
            headers.set(key, value);
          }

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: [],
            headers,
            untransformedJSON: null,
          });

          const abortSignal = result?.signal;
          let responseBody: ReadableStream<Uint8Array> = stream;

          // Fixes: https://github.com/trpc/trpc/issues/7094
          if (abortSignal) {
            const reader = stream.getReader();
            const onAbort = () => void reader.cancel();
            if (abortSignal.aborted) {
              onAbort();
            } else {
              abortSignal.addEventListener('abort', onAbort, { once: true });
            }

            responseBody = new ReadableStream({
              async pull(controller) {
                const chunk = await reader.read();
                if (chunk.done) {
                  abortSignal.removeEventListener('abort', onAbort);
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              },
              cancel() {
                abortSignal.removeEventListener('abort', onAbort);
                bodyCancelled.abort();
                return reader.cancel();
              },
            });
          }

          return new Response(responseBody, {
            headers,
            status: headResponse.status,
          });
        }
      }
    }

    // batch response handlers
    if (info.accept === 'application/jsonl') {
      // httpBatchStreamLink
      headers.set('content-type', 'application/json');
      headers.set('transfer-encoding', 'chunked');
      const headResponse = initResponse({
        ctx: ctxManager.valueOrUndefined(),
        info,
        responseMeta: opts.responseMeta,
        errors: [],
        headers,
        untransformedJSON: null,
      });
      const stream = jsonlStreamProducer({
        ...config.jsonl,
        /**
         * Example structure for `maxDepth: 4`:
         * {
         *   // 1
         *   0: {
         *     // 2
         *     result: {
         *       // 3
         *       data: // 4
         *     }
         *   }
         * }
         */
        maxDepth: Infinity,
        data: rpcCalls.map(async (res, index) => {
          const [error, result] = await res;

          const call = info.calls[index];

          if (error) {
            return {
              error: getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input: call!.result(),
                path: call!.path,
                type: call!.procedure?._def.type ?? 'unknown',
              }),
            };
          }

          /**
           * Not very pretty, but we need to wrap nested data in promises
           * Our stream producer will only resolve top-level async values or async values that are directly nested in another async value
           */
          const iterable = isObservable(result.data)
            ? observableToAsyncIterable(result.data, callSignal)
            : Promise.resolve(result.data);
          return {
            result: Promise.resolve({
              data: iterable,
            }),
          };
        }),
        serialize: (data) => config.transformer.output.serialize(data),
        onError: (cause) => {
          opts.onError?.({
            error: getTRPCErrorFromUnknown(cause.error),
            path: undefined,
            input: undefined,
            ctx: ctxManager.valueOrUndefined(),
            req: opts.req,
            type: info?.type ?? 'unknown',
          });
        },

        formatError(errorOpts) {
          const call = info?.calls[errorOpts.path[0] as any];

          const error = getTRPCErrorFromUnknown(errorOpts.error);
          const input = call?.result();
          const path = call?.path;
          const type = call?.procedure?._def.type ?? 'unknown';

          // no need to call `onError` here as it will be propagated through the stream itself

          const shape = getErrorShape({
            config,
            ctx: ctxManager.valueOrUndefined(),
            error,
            input,
            path,
            type,
          });

          return shape;
        },
      });

      return new Response(abortOnCancel(stream, bodyCancelled), {
        headers,
        status: headResponse.status,
      });
    }

    // httpBatchLink
    /**
     * Non-streaming response:
     * - await all responses in parallel, blocking on the slowest one
     * - create headers with known response body
     * - return a complete HTTPResponse
     */
    headers.set('content-type', 'application/json');
    const results: RPCResult[] = (await Promise.all(rpcCalls)).map(
      (res): RPCResult => {
        const [error, result] = res;
        if (error) {
          return res;
        }

        if (isDataStream(result.data)) {
          return [
            new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            }),
            undefined,
          ];
        }
        return res;
      },
    );
    const resultAsRPCResponse = results.map(
      (
        [error, result],
        index,
      ): TRPCResponse<unknown, inferRouterError<TRouter>> => {
        const call = info.calls[index]!;
        if (error) {
          return {
            error: getErrorShape({
              config,
              ctx: ctxManager.valueOrUndefined(),
              error,
              input: call.result(),
              path: call.path,
              type: call.procedure?._def.type ?? 'unknown',
            }),
          };
        }
        return {
          result: { data: result.data },
        };
      },
    );

    const errors = results
      .map(([error]) => error)
      .filter(Boolean) as TRPCError[];

    const headResponse = initResponse({
      ctx: ctxManager.valueOrUndefined(),
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON: resultAsRPCResponse,
      errors,
      headers,
    });

    return new Response(
      JSON.stringify(transformTRPCResponse(config, resultAsRPCResponse)),
      {
        status: headResponse.status,
        headers,
      },
    );
  } catch (cause) {
    const [_infoError, info] = infoTuple;
    const ctx = ctxManager.valueOrUndefined();
    // we get here if
    // - batching is called when it's not enabled
    // - `createContext()` throws
    // - `router._def._config.transformer.output.serialize()` throws
    // - post body is too large
    // - input deserialization fails
    // - `errorFormatter` return value is malformed
    const { error, untransformedJSON, body } = caughtErrorToData(cause, {
      opts,
      ctx: ctxManager.valueOrUndefined(),
      type: info?.type ?? 'unknown',
    });

    const headResponse = initResponse({
      ctx,
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON,
      errors: [error],
      headers,
    });

    return new Response(body, {
      status: headResponse.status,
      headers,
    });
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response> {
  const { router, req } = opts;
  const headers = new Headers([['vary', 'trpc-accept, accept']]);
  const config = router._def._config;

  const url = new URL(req.url);

  if (req.method === 'HEAD') {
    // can be used for lambda warmup
    return new Response(null, {
      status: 204,
    });
  }

  const allowBatching = opts.allowBatching ?? opts.batching?.enabled ?? true;
  const allowMethodOverride =
    (opts.allowMethodOverride ?? false) && req.method === 'POST';

  type $Context = inferRouterContext<TRouter>;

  const infoTuple: ResultTuple<TRPCRequestInfo> = await run(async () => {
    try {
      return [
        undefined,
        await getRequestInfo({
          req,
          path: decodePath(opts.path),
          router,
          searchParams: url.searchParams,
          headers: opts.req.headers,
          url,
          maxBatchSize: opts.maxBatchSize,
        }),
      ];
    } catch (cause) {
      return [getTRPCErrorFromUnknown(cause), undefined];
    }
  });

  interface ContextManager {
    valueOrUndefined: () => $Context | undefined;
    value: () => $Context;
    create: (info: TRPCRequestInfo) => Promise<void>;
  }
  const ctxManager: ContextManager = run(() => {
    let result: ResultTuple<$Context> | undefined = undefined;
    return {
      valueOrUndefined: () => {
        if (!result) {
          return undefined;
        }
        return result[1];
      },
      value: () => {
        const [err, ctx] = result!;
        if (err) {
          throw err;
        }
        return ctx;
      },
      create: async (info) => {
        if (result) {
          throw new Error(
            'This should only be called once - report a bug in tRPC',
          );
        }
        try {
          const ctx = await opts.createContext({
            info,
          });
          result = [undefined, ctx];
        } catch (cause) {
          result = [getTRPCErrorFromUnknown(cause), undefined];
        }
      },
    };
  });

  const methodMapper = allowMethodOverride
    ? TYPE_ACCEPTED_METHOD_MAP_WITH_METHOD_OVERRIDE
    : TYPE_ACCEPTED_METHOD_MAP;

  /**
   * @deprecated
   */
  const isStreamCall = getAcceptHeader(req.headers) === 'application/jsonl';

  const experimentalSSE = config.sse?.enabled ?? true;
  try {
    const [infoError, info] = infoTuple;
    if (infoError) {
      throw infoError;
    }
    if (info.isBatchCall && !allowBatching) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batching is not enabled on the server`,
      });
    }
    /* istanbul ignore if -- @preserve */
    if (isStreamCall && !info.isBatchCall) {
      throw new TRPCError({
        message: `Streaming requests must be batched (you can do a batch of 1)`,
        code: 'BAD_REQUEST',
      });
    }
    await ctxManager.create(info);

    interface RPCResultOk {
      data: unknown;
      signal?: AbortSignal;
    }
    type RPCResult = ResultTuple<RPCResultOk>;
    const bodyCancelled = new AbortController();
    const callSignal = abortSignalsAnyPonyfill([
      opts.req.signal,
      bodyCancelled.signal,
    ]);
    const rpcCalls = info.calls.map(async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    });

    // ----------- response handlers -----------
    if (!info.isBatchCall) {
      const [call] = info.calls;
      const [error, result] = await rpcCalls[0]!;

      switch (info.type) {
        case 'unknown':
        case 'mutation':
        case 'query': {
          // httpLink
          headers.set('content-type', 'application/json');

          if (isDataStream(result?.data)) {
            throw new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            });
          }
          const res: TRPCResponse<unknown, inferRouterError<TRouter>> = error
            ? {
                error: getErrorShape({
                  config,
                  ctx: ctxManager.valueOrUndefined(),
                  error,
                  input: call!.result(),
                  path: call!.path,
                  type: info.type,
                }),
              }
            : { result: { data: result.data } };

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: error ? [error] : [],
            headers,
            untransformedJSON: [res],
          });
          return new Response(
            JSON.stringify(transformTRPCResponse(config, res)),
            {
              status: headResponse.status,
              headers,
            },
          );
        }
        case 'subscription': {
          // httpSubscriptionLink

          const iterable: AsyncIterable<unknown> = run(() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, callSignal)
              : result.data;
            return dataAsIterable;
          });

          const stream = sseStreamProducer({
            ...config.sse,
            lastEventId: getLastEventId({
              headers: req.headers,
              searchParams: url.searchParams,
            }),
            data: iterable,
            serialize: (v) => config.transformer.output.serialize(v),
            formatError(errorOpts) {
              const error = getTRPCErrorFromUnknown(errorOpts.error);
              const input = call?.result();
              const path = call?.path;
              const type = call?.procedure?._def.type ?? 'unknown';

              opts.onError?.({
                error,
                path,
                input,
                ctx: ctxManager.valueOrUndefined(),
                req: opts.req,
                type,
              });

              const shape = getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input,
                path,
                type,
              });

              return shape;
            },
          });
          for (const [key, value] of Object.entries(sseHeaders)) {
            headers.set(key, value);
          }

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: [],
            headers,
            untransformedJSON: null,
          });

          const abortSignal = result?.signal;
          let responseBody: ReadableStream<Uint8Array> = stream;

          // Fixes: https://github.com/trpc/trpc/issues/7094
          if (abortSignal) {
            const reader = stream.getReader();
            const onAbort = () => void reader.cancel();
            if (abortSignal.aborted) {
              onAbort();
            } else {
              abortSignal.addEventListener('abort', onAbort, { once: true });
            }

            responseBody = new ReadableStream({
              async pull(controller) {
                const chunk = await reader.read();
                if (chunk.done) {
                  abortSignal.removeEventListener('abort', onAbort);
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              },
              cancel() {
                abortSignal.removeEventListener('abort', onAbort);
                bodyCancelled.abort();
                return reader.cancel();
              },
            });
          }

          return new Response(responseBody, {
            headers,
            status: headResponse.status,
          });
        }
      }
    }

    // batch response handlers
    if (info.accept === 'application/jsonl') {
      // httpBatchStreamLink
      headers.set('content-type', 'application/json');
      headers.set('transfer-encoding', 'chunked');
      const headResponse = initResponse({
        ctx: ctxManager.valueOrUndefined(),
        info,
        responseMeta: opts.responseMeta,
        errors: [],
        headers,
        untransformedJSON: null,
      });
      const stream = jsonlStreamProducer({
        ...config.jsonl,
        /**
         * Example structure for `maxDepth: 4`:
         * {
         *   // 1
         *   0: {
         *     // 2
         *     result: {
         *       // 3
         *       data: // 4
         *     }
         *   }
         * }
         */
        maxDepth: Infinity,
        data: rpcCalls.map(async (res, index) => {
          const [error, result] = await res;

          const call = info.calls[index];

          if (error) {
            return {
              error: getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input: call!.result(),
                path: call!.path,
                type: call!.procedure?._def.type ?? 'unknown',
              }),
            };
          }

          /**
           * Not very pretty, but we need to wrap nested data in promises
           * Our stream producer will only resolve top-level async values or async values that are directly nested in another async value
           */
          const iterable = isObservable(result.data)
            ? observableToAsyncIterable(result.data, callSignal)
            : Promise.resolve(result.data);
          return {
            result: Promise.resolve({
              data: iterable,
            }),
          };
        }),
        serialize: (data) => config.transformer.output.serialize(data),
        onError: (cause) => {
          opts.onError?.({
            error: getTRPCErrorFromUnknown(cause.error),
            path: undefined,
            input: undefined,
            ctx: ctxManager.valueOrUndefined(),
            req: opts.req,
            type: info?.type ?? 'unknown',
          });
        },

        formatError(errorOpts) {
          const call = info?.calls[errorOpts.path[0] as any];

          const error = getTRPCErrorFromUnknown(errorOpts.error);
          const input = call?.result();
          const path = call?.path;
          const type = call?.procedure?._def.type ?? 'unknown';

          // no need to call `onError` here as it will be propagated through the stream itself

          const shape = getErrorShape({
            config,
            ctx: ctxManager.valueOrUndefined(),
            error,
            input,
            path,
            type,
          });

          return shape;
        },
      });

      return new Response(abortOnCancel(stream, bodyCancelled), {
        headers,
        status: headResponse.status,
      });
    }

    // httpBatchLink
    /**
     * Non-streaming response:
     * - await all responses in parallel, blocking on the slowest one
     * - create headers with known response body
     * - return a complete HTTPResponse
     */
    headers.set('content-type', 'application/json');
    const results: RPCResult[] = (await Promise.all(rpcCalls)).map(
      (res): RPCResult => {
        const [error, result] = res;
        if (error) {
          return res;
        }

        if (isDataStream(result.data)) {
          return [
            new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            }),
            undefined,
          ];
        }
        return res;
      },
    );
    const resultAsRPCResponse = results.map(
      (
        [error, result],
        index,
      ): TRPCResponse<unknown, inferRouterError<TRouter>> => {
        const call = info.calls[index]!;
        if (error) {
          return {
            error: getErrorShape({
              config,
              ctx: ctxManager.valueOrUndefined(),
              error,
              input: call.result(),
              path: call.path,
              type: call.procedure?._def.type ?? 'unknown',
            }),
          };
        }
        return {
          result: { data: result.data },
        };
      },
    );

    const errors = results
      .map(([error]) => error)
      .filter(Boolean) as TRPCError[];

    const headResponse = initResponse({
      ctx: ctxManager.valueOrUndefined(),
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON: resultAsRPCResponse,
      errors,
      headers,
    });

    return new Response(
      JSON.stringify(transformTRPCResponse(config, resultAsRPCResponse)),
      {
        status: headResponse.status,
        headers,
      },
    );
  } catch (cause) {
    const [_infoError, info] = infoTuple;
    const ctx = ctxManager.valueOrUndefined();
    // we get here if
    // - batching is called when it's not enabled
    // - `createContext()` throws
    // - `router._def._config.transformer.output.serialize()` throws
    // - post body is too large
    // - input deserialization fails
    // - `errorFormatter` return value is malformed
    const { error, untransformedJSON, body } = caughtErrorToData(cause, {
      opts,
      ctx: ctxManager.valueOrUndefined(),
      type: info?.type ?? 'unknown',
    });

    const headResponse = initResponse({
      ctx,
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON,
      errors: [error],
      headers,
    });

    return new Response(body, {
      status: headResponse.status,
      headers,
    });
  }
}
```


#### 📄 檔案: `packages/server/src/unstable-core-do-not-import/stream/sse.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:41, E:30, A:2) ➔ After(N:42, E:30, A:2)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#eventSource** `(Control)`
    └── ⚡ **on('CONNECTED_EVENT')**
    └── ⚡ **on('PING_EVENT')**
    └── ⚡ **on('RETURN_EVENT')**
    └── ⚡ **on('SERIALIZED_ERROR_EVENT')**
        └── 🎯 [CALLS] `deserialize (External/Unresolved)()`
    └── ⚡ **on('error')**
    └── ⚡ **on('message')**
        └── *ref:`deserialize (External/Unresolved)` [已折疊指針]
  🌲 **#signal** `(Control)`
    └── ⚡ **on('abort')**
        └── 🎯 [TRIGGERS] `onAbort()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `RESTORE_ID_EVENT` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `generator()`
- **變更前簽章 (Before)**: `async function* generator(): AsyncIterable<SSEvent, void>` (L106~L150)
- **變更後簽章 (After)**: `async function* generator(): AsyncIterable<SSEvent, void>` (L112~L175)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async function* generator(): AsyncIterable<SSEvent, void> {
    yield {
      event: CONNECTED_EVENT,
      data: JSON.stringify(client),
    };

    type TIteratorValue = Awaited<TValue> | typeof PING_SYM;

    let iterable: AsyncIterable<TValue | typeof PING_SYM> = opts.data;

    if (opts.emitAndEndImmediately) {
      iterable = takeWithGrace(iterable, {
        count: 1,
        gracePeriodMs: 1,
      });
    }

    if (ping.enabled && ping.intervalMs !== Infinity && ping.intervalMs > 0) {
      iterable = withPing(iterable, ping.intervalMs);
    }

    // We need those declarations outside the loop for garbage collection reasons. If they were
    // declared inside, they would not be freed until the next value is present.
    let value: null | TIteratorValue;
    let chunk: null | SSEvent;

    for await (value of iterable) {
      if (value === PING_SYM) {
        yield { event: PING_EVENT, data: '' };
        continue;
      }

      chunk = isTrackedEnvelope(value)
        ? { id: value[0], data: value[1] }
        : { data: value };

      chunk.data = JSON.stringify(serialize(chunk.data));

      yield chunk;

      // free up references for garbage collection
      value = null;
      chunk = null;
    }
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async function* generator(): AsyncIterable<SSEvent, void> {
    yield {
      event: CONNECTED_EVENT,
      data: JSON.stringify(client),
    };

    type TIteratorValue = Awaited<TValue> | typeof PING_SYM;

    let iterable: AsyncIterable<TValue | typeof PING_SYM> = opts.data;

    if (opts.emitAndEndImmediately) {
      iterable = takeWithGrace(iterable, {
        count: 1,
        gracePeriodMs: 1,
      });
    }

    if (ping.enabled && ping.intervalMs !== Infinity && ping.intervalMs > 0) {
      iterable = withPing(iterable, ping.intervalMs);
    }

    // We need those declarations outside the loop for garbage collection reasons. If they were
    // declared inside, they would not be freed until the next value is present.
    let value: null | TIteratorValue;
    let chunk: null | SSEvent;

    // The id the client's EventSource holds and sends when it reconnects.
    // An id with these characters can't be sent back in an `id` field
    let lastEventId =
      opts.lastEventId && !/[\0\n\r]/.test(opts.lastEventId)
        ? opts.lastEventId
        : null;

    for await (value of iterable) {
      if (value === PING_SYM) {
        yield { event: PING_EVENT, data: '' };
        continue;
      }

      chunk = isTrackedEnvelope(value)
        ? { id: value[0], data: value[1] }
        : { data: value };

      chunk.data = JSON.stringify(serialize(chunk.data));

      if (chunk.id !== undefined) {
        lastEventId = chunk.id;
        yield chunk;
      } else if (lastEventId === null) {
        yield chunk;
      } else {
        // EventSource gives an event without an `id` the last id it received,
        // so clear the id for this event and then set it back with an event
        // that clients don't listen to, so reconnecting still resumes from it
        chunk.id = '';
        yield chunk;
        yield { event: RESTORE_ID_EVENT, data: '', id: lastEventId };
      }

      // free up references for garbage collection
      value = null;
      chunk = null;
    }
  }
```

### 🔹 函式: `sseStreamProducer()`
- **變更前簽章 (Before)**: `function sseStreamProducer<TValue = unknown>(
  opts: SSEStreamProducerOptions<TValue>,
)` (L85~L199)
- **變更後簽章 (After)**: `function sseStreamProducer<TValue = unknown>(
  opts: SSEStreamProducerOptions<TValue>,
)` (L91~L224)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function sseStreamProducer<TValue = unknown>(
  opts: SSEStreamProducerOptions<TValue>,
) {
  const { serialize = identity } = opts;

  const ping: Required<SSEPingOptions> = {
    enabled: opts.ping?.enabled ?? false,
    intervalMs: opts.ping?.intervalMs ?? 1000,
  };
  const client: SSEClientOptions = opts.client ?? {};

  if (
    ping.enabled &&
    client.reconnectAfterInactivityMs &&
    ping.intervalMs > client.reconnectAfterInactivityMs
  ) {
    throw new Error(
      `Ping interval must be less than client reconnect interval to prevent unnecessary reconnection - ping.intervalMs: ${ping.intervalMs} client.reconnectAfterInactivityMs: ${client.reconnectAfterInactivityMs}`,
    );
  }

  async function* generator(): AsyncIterable<SSEvent, void> {
    yield {
      event: CONNECTED_EVENT,
      data: JSON.stringify(client),
    };

    type TIteratorValue = Awaited<TValue> | typeof PING_SYM;

    let iterable: AsyncIterable<TValue | typeof PING_SYM> = opts.data;

    if (opts.emitAndEndImmediately) {
      iterable = takeWithGrace(iterable, {
        count: 1,
        gracePeriodMs: 1,
      });
    }

    if (ping.enabled && ping.intervalMs !== Infinity && ping.intervalMs > 0) {
      iterable = withPing(iterable, ping.intervalMs);
    }

    // We need those declarations outside the loop for garbage collection reasons. If they were
    // declared inside, they would not be freed until the next value is present.
    let value: null | TIteratorValue;
    let chunk: null | SSEvent;

    for await (value of iterable) {
      if (value === PING_SYM) {
        yield { event: PING_EVENT, data: '' };
        continue;
      }

      chunk = isTrackedEnvelope(value)
        ? { id: value[0], data: value[1] }
        : { data: value };

      chunk.data = JSON.stringify(serialize(chunk.data));

      yield chunk;

      // free up references for garbage collection
      value = null;
      chunk = null;
    }
  }

  async function* generatorWithErrorHandling(): AsyncIterable<SSEvent, void> {
    try {
      yield* generator();

      yield {
        event: RETURN_EVENT,
        data: '',
      };
    } catch (cause) {
      if (isAbortError(cause)) {
        // ignore abort errors, send any other errors
        return;
      }
      // `err` must be caused by `opts.data`, `JSON.stringify` or `serialize`.
      // So, a user error in any case.
      const error = getTRPCErrorFromUnknown(cause);
      const data = opts.formatError?.({ error }) ?? null;
      yield {
        event: SERIALIZED_ERROR_EVENT,
        data: JSON.stringify(serialize(data)),
      };
    }
  }

  const stream = readableStreamFrom(generatorWithErrorHandling());

  return stream
    .pipeThrough(
      new TransformStream({
        transform(chunk, controller: TransformStreamDefaultController<string>) {
          if ('event' in chunk) {
            controller.enqueue(`event: ${chunk.event}\n`);
          }
          if ('data' in chunk) {
            controller.enqueue(`data: ${chunk.data}\n`);
          }
          if ('id' in chunk) {
            controller.enqueue(`id: ${chunk.id}\n`);
          }
          if ('comment' in chunk) {
            controller.enqueue(`: ${chunk.comment}\n`);
          }
          controller.enqueue('\n\n');
        },
      }),
    )
    .pipeThrough(new TextEncoderStream());
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function sseStreamProducer<TValue = unknown>(
  opts: SSEStreamProducerOptions<TValue>,
) {
  const { serialize = identity } = opts;

  const ping: Required<SSEPingOptions> = {
    enabled: opts.ping?.enabled ?? false,
    intervalMs: opts.ping?.intervalMs ?? 1000,
  };
  const client: SSEClientOptions = opts.client ?? {};

  if (
    ping.enabled &&
    client.reconnectAfterInactivityMs &&
    ping.intervalMs > client.reconnectAfterInactivityMs
  ) {
    throw new Error(
      `Ping interval must be less than client reconnect interval to prevent unnecessary reconnection - ping.intervalMs: ${ping.intervalMs} client.reconnectAfterInactivityMs: ${client.reconnectAfterInactivityMs}`,
    );
  }

  async function* generator(): AsyncIterable<SSEvent, void> {
    yield {
      event: CONNECTED_EVENT,
      data: JSON.stringify(client),
    };

    type TIteratorValue = Awaited<TValue> | typeof PING_SYM;

    let iterable: AsyncIterable<TValue | typeof PING_SYM> = opts.data;

    if (opts.emitAndEndImmediately) {
      iterable = takeWithGrace(iterable, {
        count: 1,
        gracePeriodMs: 1,
      });
    }

    if (ping.enabled && ping.intervalMs !== Infinity && ping.intervalMs > 0) {
      iterable = withPing(iterable, ping.intervalMs);
    }

    // We need those declarations outside the loop for garbage collection reasons. If they were
    // declared inside, they would not be freed until the next value is present.
    let value: null | TIteratorValue;
    let chunk: null | SSEvent;

    // The id the client's EventSource holds and sends when it reconnects.
    // An id with these characters can't be sent back in an `id` field
    let lastEventId =
      opts.lastEventId && !/[\0\n\r]/.test(opts.lastEventId)
        ? opts.lastEventId
        : null;

    for await (value of iterable) {
      if (value === PING_SYM) {
        yield { event: PING_EVENT, data: '' };
        continue;
      }

      chunk = isTrackedEnvelope(value)
        ? { id: value[0], data: value[1] }
        : { data: value };

      chunk.data = JSON.stringify(serialize(chunk.data));

      if (chunk.id !== undefined) {
        lastEventId = chunk.id;
        yield chunk;
      } else if (lastEventId === null) {
        yield chunk;
      } else {
        // EventSource gives an event without an `id` the last id it received,
        // so clear the id for this event and then set it back with an event
        // that clients don't listen to, so reconnecting still resumes from it
        chunk.id = '';
        yield chunk;
        yield { event: RESTORE_ID_EVENT, data: '', id: lastEventId };
      }

      // free up references for garbage collection
      value = null;
      chunk = null;
    }
  }

  async function* generatorWithErrorHandling(): AsyncIterable<SSEvent, void> {
    try {
      yield* generator();

      yield {
        event: RETURN_EVENT,
        data: '',
      };
    } catch (cause) {
      if (isAbortError(cause)) {
        // ignore abort errors, send any other errors
        return;
      }
      // `err` must be caused by `opts.data`, `JSON.stringify` or `serialize`.
      // So, a user error in any case.
      const error = getTRPCErrorFromUnknown(cause);
      const data = opts.formatError?.({ error }) ?? null;
      yield {
        event: SERIALIZED_ERROR_EVENT,
        data: JSON.stringify(serialize(data)),
      };
    }
  }

  const stream = readableStreamFrom(generatorWithErrorHandling());

  return stream
    .pipeThrough(
      new TransformStream({
        transform(chunk, controller: TransformStreamDefaultController<string>) {
          if ('event' in chunk) {
            controller.enqueue(`event: ${chunk.event}\n`);
          }
          if ('data' in chunk) {
            controller.enqueue(`data: ${chunk.data}\n`);
          }
          if ('id' in chunk) {
            controller.enqueue(`id: ${chunk.id}\n`);
          }
          if ('comment' in chunk) {
            controller.enqueue(`: ${chunk.comment}\n`);
          }
          controller.enqueue('\n\n');
        },
      }),
    )
    .pipeThrough(new TextEncoderStream());
}
```


---

### 🔹 Commit #10: `6c402cd3`
- **完整 Hash**: `6c402cd342de7a7a62a5dfaf7ce424fcaafd8361`
- **說明 (Ground Truth)**: fix(server): return 400 for malformed url-encoding in the request path (#7555)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/src/unstable-core-do-not-import/http/resolveResponse.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:53, E:50, A:2) ➔ After(N:54, E:51, A:2)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 2, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#abortSignal** `(Control)`
    └── ⚡ **on('abort')**
        └── 🎯 [TRIGGERS] `onAbort()`
  🌲 **#combinedAbort.signal** `(Control)`
    └── ⚡ **on('abort')**
        └── 🎯 [TRIGGERS] `cleanup()`
            └── 🎯 [CALLS] `clearTimeout (External/Unresolved)()`
            └── 🎯 [CALLS] `removeEventListener()()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `decodePath` (FUNCTION_DEF)
  • + [新增呼叫邊] `decodePath` ──[CALLS]──> `decodeURIComponent (External/Unresolved)`
  • + [新增呼叫邊] `resolveResponse` ──[CALLS]──> `decodePath`
  • - [移除呼叫邊] `resolveResponse` ──[CALLS]──> `decodeURIComponent (External/Unresolved)`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'onError' 被深鎖在內部閉包 (scope:resolveResponse@after/packages/server/src/unstable-core-do-not-import/http/resolveResponse.ts:L255C8)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `resolveResponse()`
- **變更前簽章 (Before)**: `async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response>` (L238~L801)
- **變更後簽章 (After)**: `async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response>` (L255~L818)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response> {
  const { router, req } = opts;
  const headers = new Headers([['vary', 'trpc-accept, accept']]);
  const config = router._def._config;

  const url = new URL(req.url);

  if (req.method === 'HEAD') {
    // can be used for lambda warmup
    return new Response(null, {
      status: 204,
    });
  }

  const allowBatching = opts.allowBatching ?? opts.batching?.enabled ?? true;
  const allowMethodOverride =
    (opts.allowMethodOverride ?? false) && req.method === 'POST';

  type $Context = inferRouterContext<TRouter>;

  const infoTuple: ResultTuple<TRPCRequestInfo> = await run(async () => {
    try {
      return [
        undefined,
        await getRequestInfo({
          req,
          path: decodeURIComponent(opts.path),
          router,
          searchParams: url.searchParams,
          headers: opts.req.headers,
          url,
          maxBatchSize: opts.maxBatchSize,
        }),
      ];
    } catch (cause) {
      return [getTRPCErrorFromUnknown(cause), undefined];
    }
  });

  interface ContextManager {
    valueOrUndefined: () => $Context | undefined;
    value: () => $Context;
    create: (info: TRPCRequestInfo) => Promise<void>;
  }
  const ctxManager: ContextManager = run(() => {
    let result: ResultTuple<$Context> | undefined = undefined;
    return {
      valueOrUndefined: () => {
        if (!result) {
          return undefined;
        }
        return result[1];
      },
      value: () => {
        const [err, ctx] = result!;
        if (err) {
          throw err;
        }
        return ctx;
      },
      create: async (info) => {
        if (result) {
          throw new Error(
            'This should only be called once - report a bug in tRPC',
          );
        }
        try {
          const ctx = await opts.createContext({
            info,
          });
          result = [undefined, ctx];
        } catch (cause) {
          result = [getTRPCErrorFromUnknown(cause), undefined];
        }
      },
    };
  });

  const methodMapper = allowMethodOverride
    ? TYPE_ACCEPTED_METHOD_MAP_WITH_METHOD_OVERRIDE
    : TYPE_ACCEPTED_METHOD_MAP;

  /**
   * @deprecated
   */
  const isStreamCall = getAcceptHeader(req.headers) === 'application/jsonl';

  const experimentalSSE = config.sse?.enabled ?? true;
  try {
    const [infoError, info] = infoTuple;
    if (infoError) {
      throw infoError;
    }
    if (info.isBatchCall && !allowBatching) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batching is not enabled on the server`,
      });
    }
    /* istanbul ignore if -- @preserve */
    if (isStreamCall && !info.isBatchCall) {
      throw new TRPCError({
        message: `Streaming requests must be batched (you can do a batch of 1)`,
        code: 'BAD_REQUEST',
      });
    }
    await ctxManager.create(info);

    interface RPCResultOk {
      data: unknown;
      signal?: AbortSignal;
    }
    type RPCResult = ResultTuple<RPCResultOk>;
    const bodyCancelled = new AbortController();
    const callSignal = abortSignalsAnyPonyfill([
      opts.req.signal,
      bodyCancelled.signal,
    ]);
    const rpcCalls = info.calls.map(async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    });

    // ----------- response handlers -----------
    if (!info.isBatchCall) {
      const [call] = info.calls;
      const [error, result] = await rpcCalls[0]!;

      switch (info.type) {
        case 'unknown':
        case 'mutation':
        case 'query': {
          // httpLink
          headers.set('content-type', 'application/json');

          if (isDataStream(result?.data)) {
            throw new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            });
          }
          const res: TRPCResponse<unknown, inferRouterError<TRouter>> = error
            ? {
                error: getErrorShape({
                  config,
                  ctx: ctxManager.valueOrUndefined(),
                  error,
                  input: call!.result(),
                  path: call!.path,
                  type: info.type,
                }),
              }
            : { result: { data: result.data } };

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: error ? [error] : [],
            headers,
            untransformedJSON: [res],
          });
          return new Response(
            JSON.stringify(transformTRPCResponse(config, res)),
            {
              status: headResponse.status,
              headers,
            },
          );
        }
        case 'subscription': {
          // httpSubscriptionLink

          const iterable: AsyncIterable<unknown> = run(() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, callSignal)
              : result.data;
            return dataAsIterable;
          });

          const stream = sseStreamProducer({
            ...config.sse,
            data: iterable,
            serialize: (v) => config.transformer.output.serialize(v),
            formatError(errorOpts) {
              const error = getTRPCErrorFromUnknown(errorOpts.error);
              const input = call?.result();
              const path = call?.path;
              const type = call?.procedure?._def.type ?? 'unknown';

              opts.onError?.({
                error,
                path,
                input,
                ctx: ctxManager.valueOrUndefined(),
                req: opts.req,
                type,
              });

              const shape = getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input,
                path,
                type,
              });

              return shape;
            },
          });
          for (const [key, value] of Object.entries(sseHeaders)) {
            headers.set(key, value);
          }

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: [],
            headers,
            untransformedJSON: null,
          });

          const abortSignal = result?.signal;
          let responseBody: ReadableStream<Uint8Array> = stream;

          // Fixes: https://github.com/trpc/trpc/issues/7094
          if (abortSignal) {
            const reader = stream.getReader();
            const onAbort = () => void reader.cancel();
            if (abortSignal.aborted) {
              onAbort();
            } else {
              abortSignal.addEventListener('abort', onAbort, { once: true });
            }

            responseBody = new ReadableStream({
              async pull(controller) {
                const chunk = await reader.read();
                if (chunk.done) {
                  abortSignal.removeEventListener('abort', onAbort);
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              },
              cancel() {
                abortSignal.removeEventListener('abort', onAbort);
                bodyCancelled.abort();
                return reader.cancel();
              },
            });
          }

          return new Response(responseBody, {
            headers,
            status: headResponse.status,
          });
        }
      }
    }

    // batch response handlers
    if (info.accept === 'application/jsonl') {
      // httpBatchStreamLink
      headers.set('content-type', 'application/json');
      headers.set('transfer-encoding', 'chunked');
      const headResponse = initResponse({
        ctx: ctxManager.valueOrUndefined(),
        info,
        responseMeta: opts.responseMeta,
        errors: [],
        headers,
        untransformedJSON: null,
      });
      const stream = jsonlStreamProducer({
        ...config.jsonl,
        /**
         * Example structure for `maxDepth: 4`:
         * {
         *   // 1
         *   0: {
         *     // 2
         *     result: {
         *       // 3
         *       data: // 4
         *     }
         *   }
         * }
         */
        maxDepth: Infinity,
        data: rpcCalls.map(async (res, index) => {
          const [error, result] = await res;

          const call = info.calls[index];

          if (error) {
            return {
              error: getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input: call!.result(),
                path: call!.path,
                type: call!.procedure?._def.type ?? 'unknown',
              }),
            };
          }

          /**
           * Not very pretty, but we need to wrap nested data in promises
           * Our stream producer will only resolve top-level async values or async values that are directly nested in another async value
           */
          const iterable = isObservable(result.data)
            ? observableToAsyncIterable(result.data, callSignal)
            : Promise.resolve(result.data);
          return {
            result: Promise.resolve({
              data: iterable,
            }),
          };
        }),
        serialize: (data) => config.transformer.output.serialize(data),
        onError: (cause) => {
          opts.onError?.({
            error: getTRPCErrorFromUnknown(cause.error),
            path: undefined,
            input: undefined,
            ctx: ctxManager.valueOrUndefined(),
            req: opts.req,
            type: info?.type ?? 'unknown',
          });
        },

        formatError(errorOpts) {
          const call = info?.calls[errorOpts.path[0] as any];

          const error = getTRPCErrorFromUnknown(errorOpts.error);
          const input = call?.result();
          const path = call?.path;
          const type = call?.procedure?._def.type ?? 'unknown';

          // no need to call `onError` here as it will be propagated through the stream itself

          const shape = getErrorShape({
            config,
            ctx: ctxManager.valueOrUndefined(),
            error,
            input,
            path,
            type,
          });

          return shape;
        },
      });

      return new Response(abortOnCancel(stream, bodyCancelled), {
        headers,
        status: headResponse.status,
      });
    }

    // httpBatchLink
    /**
     * Non-streaming response:
     * - await all responses in parallel, blocking on the slowest one
     * - create headers with known response body
     * - return a complete HTTPResponse
     */
    headers.set('content-type', 'application/json');
    const results: RPCResult[] = (await Promise.all(rpcCalls)).map(
      (res): RPCResult => {
        const [error, result] = res;
        if (error) {
          return res;
        }

        if (isDataStream(result.data)) {
          return [
            new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            }),
            undefined,
          ];
        }
        return res;
      },
    );
    const resultAsRPCResponse = results.map(
      (
        [error, result],
        index,
      ): TRPCResponse<unknown, inferRouterError<TRouter>> => {
        const call = info.calls[index]!;
        if (error) {
          return {
            error: getErrorShape({
              config,
              ctx: ctxManager.valueOrUndefined(),
              error,
              input: call.result(),
              path: call.path,
              type: call.procedure?._def.type ?? 'unknown',
            }),
          };
        }
        return {
          result: { data: result.data },
        };
      },
    );

    const errors = results
      .map(([error]) => error)
      .filter(Boolean) as TRPCError[];

    const headResponse = initResponse({
      ctx: ctxManager.valueOrUndefined(),
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON: resultAsRPCResponse,
      errors,
      headers,
    });

    return new Response(
      JSON.stringify(transformTRPCResponse(config, resultAsRPCResponse)),
      {
        status: headResponse.status,
        headers,
      },
    );
  } catch (cause) {
    const [_infoError, info] = infoTuple;
    const ctx = ctxManager.valueOrUndefined();
    // we get here if
    // - batching is called when it's not enabled
    // - `createContext()` throws
    // - `router._def._config.transformer.output.serialize()` throws
    // - post body is too large
    // - input deserialization fails
    // - `errorFormatter` return value is malformed
    const { error, untransformedJSON, body } = caughtErrorToData(cause, {
      opts,
      ctx: ctxManager.valueOrUndefined(),
      type: info?.type ?? 'unknown',
    });

    const headResponse = initResponse({
      ctx,
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON,
      errors: [error],
      headers,
    });

    return new Response(body, {
      status: headResponse.status,
      headers,
    });
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response> {
  const { router, req } = opts;
  const headers = new Headers([['vary', 'trpc-accept, accept']]);
  const config = router._def._config;

  const url = new URL(req.url);

  if (req.method === 'HEAD') {
    // can be used for lambda warmup
    return new Response(null, {
      status: 204,
    });
  }

  const allowBatching = opts.allowBatching ?? opts.batching?.enabled ?? true;
  const allowMethodOverride =
    (opts.allowMethodOverride ?? false) && req.method === 'POST';

  type $Context = inferRouterContext<TRouter>;

  const infoTuple: ResultTuple<TRPCRequestInfo> = await run(async () => {
    try {
      return [
        undefined,
        await getRequestInfo({
          req,
          path: decodePath(opts.path),
          router,
          searchParams: url.searchParams,
          headers: opts.req.headers,
          url,
          maxBatchSize: opts.maxBatchSize,
        }),
      ];
    } catch (cause) {
      return [getTRPCErrorFromUnknown(cause), undefined];
    }
  });

  interface ContextManager {
    valueOrUndefined: () => $Context | undefined;
    value: () => $Context;
    create: (info: TRPCRequestInfo) => Promise<void>;
  }
  const ctxManager: ContextManager = run(() => {
    let result: ResultTuple<$Context> | undefined = undefined;
    return {
      valueOrUndefined: () => {
        if (!result) {
          return undefined;
        }
        return result[1];
      },
      value: () => {
        const [err, ctx] = result!;
        if (err) {
          throw err;
        }
        return ctx;
      },
      create: async (info) => {
        if (result) {
          throw new Error(
            'This should only be called once - report a bug in tRPC',
          );
        }
        try {
          const ctx = await opts.createContext({
            info,
          });
          result = [undefined, ctx];
        } catch (cause) {
          result = [getTRPCErrorFromUnknown(cause), undefined];
        }
      },
    };
  });

  const methodMapper = allowMethodOverride
    ? TYPE_ACCEPTED_METHOD_MAP_WITH_METHOD_OVERRIDE
    : TYPE_ACCEPTED_METHOD_MAP;

  /**
   * @deprecated
   */
  const isStreamCall = getAcceptHeader(req.headers) === 'application/jsonl';

  const experimentalSSE = config.sse?.enabled ?? true;
  try {
    const [infoError, info] = infoTuple;
    if (infoError) {
      throw infoError;
    }
    if (info.isBatchCall && !allowBatching) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batching is not enabled on the server`,
      });
    }
    /* istanbul ignore if -- @preserve */
    if (isStreamCall && !info.isBatchCall) {
      throw new TRPCError({
        message: `Streaming requests must be batched (you can do a batch of 1)`,
        code: 'BAD_REQUEST',
      });
    }
    await ctxManager.create(info);

    interface RPCResultOk {
      data: unknown;
      signal?: AbortSignal;
    }
    type RPCResult = ResultTuple<RPCResultOk>;
    const bodyCancelled = new AbortController();
    const callSignal = abortSignalsAnyPonyfill([
      opts.req.signal,
      bodyCancelled.signal,
    ]);
    const rpcCalls = info.calls.map(async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    });

    // ----------- response handlers -----------
    if (!info.isBatchCall) {
      const [call] = info.calls;
      const [error, result] = await rpcCalls[0]!;

      switch (info.type) {
        case 'unknown':
        case 'mutation':
        case 'query': {
          // httpLink
          headers.set('content-type', 'application/json');

          if (isDataStream(result?.data)) {
            throw new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            });
          }
          const res: TRPCResponse<unknown, inferRouterError<TRouter>> = error
            ? {
                error: getErrorShape({
                  config,
                  ctx: ctxManager.valueOrUndefined(),
                  error,
                  input: call!.result(),
                  path: call!.path,
                  type: info.type,
                }),
              }
            : { result: { data: result.data } };

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: error ? [error] : [],
            headers,
            untransformedJSON: [res],
          });
          return new Response(
            JSON.stringify(transformTRPCResponse(config, res)),
            {
              status: headResponse.status,
              headers,
            },
          );
        }
        case 'subscription': {
          // httpSubscriptionLink

          const iterable: AsyncIterable<unknown> = run(() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, callSignal)
              : result.data;
            return dataAsIterable;
          });

          const stream = sseStreamProducer({
            ...config.sse,
            data: iterable,
            serialize: (v) => config.transformer.output.serialize(v),
            formatError(errorOpts) {
              const error = getTRPCErrorFromUnknown(errorOpts.error);
              const input = call?.result();
              const path = call?.path;
              const type = call?.procedure?._def.type ?? 'unknown';

              opts.onError?.({
                error,
                path,
                input,
                ctx: ctxManager.valueOrUndefined(),
                req: opts.req,
                type,
              });

              const shape = getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input,
                path,
                type,
              });

              return shape;
            },
          });
          for (const [key, value] of Object.entries(sseHeaders)) {
            headers.set(key, value);
          }

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: [],
            headers,
            untransformedJSON: null,
          });

          const abortSignal = result?.signal;
          let responseBody: ReadableStream<Uint8Array> = stream;

          // Fixes: https://github.com/trpc/trpc/issues/7094
          if (abortSignal) {
            const reader = stream.getReader();
            const onAbort = () => void reader.cancel();
            if (abortSignal.aborted) {
              onAbort();
            } else {
              abortSignal.addEventListener('abort', onAbort, { once: true });
            }

            responseBody = new ReadableStream({
              async pull(controller) {
                const chunk = await reader.read();
                if (chunk.done) {
                  abortSignal.removeEventListener('abort', onAbort);
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              },
              cancel() {
                abortSignal.removeEventListener('abort', onAbort);
                bodyCancelled.abort();
                return reader.cancel();
              },
            });
          }

          return new Response(responseBody, {
            headers,
            status: headResponse.status,
          });
        }
      }
    }

    // batch response handlers
    if (info.accept === 'application/jsonl') {
      // httpBatchStreamLink
      headers.set('content-type', 'application/json');
      headers.set('transfer-encoding', 'chunked');
      const headResponse = initResponse({
        ctx: ctxManager.valueOrUndefined(),
        info,
        responseMeta: opts.responseMeta,
        errors: [],
        headers,
        untransformedJSON: null,
      });
      const stream = jsonlStreamProducer({
        ...config.jsonl,
        /**
         * Example structure for `maxDepth: 4`:
         * {
         *   // 1
         *   0: {
         *     // 2
         *     result: {
         *       // 3
         *       data: // 4
         *     }
         *   }
         * }
         */
        maxDepth: Infinity,
        data: rpcCalls.map(async (res, index) => {
          const [error, result] = await res;

          const call = info.calls[index];

          if (error) {
            return {
              error: getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input: call!.result(),
                path: call!.path,
                type: call!.procedure?._def.type ?? 'unknown',
              }),
            };
          }

          /**
           * Not very pretty, but we need to wrap nested data in promises
           * Our stream producer will only resolve top-level async values or async values that are directly nested in another async value
           */
          const iterable = isObservable(result.data)
            ? observableToAsyncIterable(result.data, callSignal)
            : Promise.resolve(result.data);
          return {
            result: Promise.resolve({
              data: iterable,
            }),
          };
        }),
        serialize: (data) => config.transformer.output.serialize(data),
        onError: (cause) => {
          opts.onError?.({
            error: getTRPCErrorFromUnknown(cause.error),
            path: undefined,
            input: undefined,
            ctx: ctxManager.valueOrUndefined(),
            req: opts.req,
            type: info?.type ?? 'unknown',
          });
        },

        formatError(errorOpts) {
          const call = info?.calls[errorOpts.path[0] as any];

          const error = getTRPCErrorFromUnknown(errorOpts.error);
          const input = call?.result();
          const path = call?.path;
          const type = call?.procedure?._def.type ?? 'unknown';

          // no need to call `onError` here as it will be propagated through the stream itself

          const shape = getErrorShape({
            config,
            ctx: ctxManager.valueOrUndefined(),
            error,
            input,
            path,
            type,
          });

          return shape;
        },
      });

      return new Response(abortOnCancel(stream, bodyCancelled), {
        headers,
        status: headResponse.status,
      });
    }

    // httpBatchLink
    /**
     * Non-streaming response:
     * - await all responses in parallel, blocking on the slowest one
     * - create headers with known response body
     * - return a complete HTTPResponse
     */
    headers.set('content-type', 'application/json');
    const results: RPCResult[] = (await Promise.all(rpcCalls)).map(
      (res): RPCResult => {
        const [error, result] = res;
        if (error) {
          return res;
        }

        if (isDataStream(result.data)) {
          return [
            new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            }),
            undefined,
          ];
        }
        return res;
      },
    );
    const resultAsRPCResponse = results.map(
      (
        [error, result],
        index,
      ): TRPCResponse<unknown, inferRouterError<TRouter>> => {
        const call = info.calls[index]!;
        if (error) {
          return {
            error: getErrorShape({
              config,
              ctx: ctxManager.valueOrUndefined(),
              error,
              input: call.result(),
              path: call.path,
              type: call.procedure?._def.type ?? 'unknown',
            }),
          };
        }
        return {
          result: { data: result.data },
        };
      },
    );

    const errors = results
      .map(([error]) => error)
      .filter(Boolean) as TRPCError[];

    const headResponse = initResponse({
      ctx: ctxManager.valueOrUndefined(),
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON: resultAsRPCResponse,
      errors,
      headers,
    });

    return new Response(
      JSON.stringify(transformTRPCResponse(config, resultAsRPCResponse)),
      {
        status: headResponse.status,
        headers,
      },
    );
  } catch (cause) {
    const [_infoError, info] = infoTuple;
    const ctx = ctxManager.valueOrUndefined();
    // we get here if
    // - batching is called when it's not enabled
    // - `createContext()` throws
    // - `router._def._config.transformer.output.serialize()` throws
    // - post body is too large
    // - input deserialization fails
    // - `errorFormatter` return value is malformed
    const { error, untransformedJSON, body } = caughtErrorToData(cause, {
      opts,
      ctx: ctxManager.valueOrUndefined(),
      type: info?.type ?? 'unknown',
    });

    const headResponse = initResponse({
      ctx,
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON,
      errors: [error],
      headers,
    });

    return new Response(body, {
      status: headResponse.status,
      headers,
    });
  }
}
```


---

### 🔹 Commit #11: `9464658b`
- **完整 Hash**: `9464658b429b22e259b41f2e98991d14ede4d0cc`
- **說明 (Ground Truth)**: fix(react-query): honor skipToken in utils queryOptions and infiniteQueryOptions (#7594)
- **變更檔案數**: 1

#### 📄 檔案: `packages/react-query/src/shared/proxy/utilsProxy.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:28, E:10, A:0) ➔ After(N:29, E:12, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `withSkipToken` (FUNCTION_DEF)
  • + [新增呼叫邊] `infiniteQueryOptions` ──[CALLS]──> `withSkipToken`
  • + [新增呼叫邊] `queryOptions` ──[CALLS]──> `withSkipToken`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'withSkipToken' 被深鎖在內部閉包 (scope:arrow@after/packages/react-query/src/shared/proxy/utilsProxy.ts:L469C58)，外部無法調用！ (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `createRecursiveUtilsProxy()`
- **變更前簽章 (Before)**: `function createRecursiveUtilsProxy<TRouter extends AnyRouter>(
  context: TRPCQueryUtils<TRouter>,
)` (L465~L517)
- **變更後簽章 (After)**: `function createRecursiveUtilsProxy<TRouter extends AnyRouter>(
  context: TRPCQueryUtils<TRouter>,
)` (L466~L524)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createRecursiveUtilsProxy<TRouter extends AnyRouter>(
  context: TRPCQueryUtils<TRouter>,
) {
  return createRecursiveProxy<CreateQueryUtils<TRouter>>((opts) => {
    const path = [...opts.path];
    const utilName = path.pop() as keyof AnyDecoratedProcedure;
    const args = [...opts.args] as Parameters<
      AnyDecoratedProcedure[typeof utilName]
    >;
    const input = args.shift(); // args can now be spread when input removed
    const queryType = getQueryType(utilName);
    const queryKey = getQueryKeyInternal(path, input, queryType);

    const contextMap: Record<keyof AnyDecoratedProcedure, () => unknown> = {
      infiniteQueryOptions: () =>
        context.infiniteQueryOptions(path, queryKey, args[0]),
      queryOptions: () => context.queryOptions(path, queryKey, ...args),
      /**
       * DecorateQueryProcedure
       */
      fetch: () => context.fetchQuery(queryKey, ...args),
      fetchInfinite: () => context.fetchInfiniteQuery(queryKey, args[0]),
      prefetch: () => context.prefetchQuery(queryKey, ...args),
      prefetchInfinite: () => context.prefetchInfiniteQuery(queryKey, args[0]),
      ensureData: () => context.ensureQueryData(queryKey, ...args),
      invalidate: () => context.invalidateQueries(queryKey, ...args),
      reset: () => context.resetQueries(queryKey, ...args),
      refetch: () => context.refetchQueries(queryKey, ...args),
      cancel: () => context.cancelQuery(queryKey, ...args),
      setData: () => {
        context.setQueryData(queryKey, args[0], args[1]);
      },
      setQueriesData: () =>
        context.setQueriesData(queryKey, args[0], args[1], args[2]),
      setInfiniteData: () => {
        context.setInfiniteQueryData(queryKey, args[0], args[1]);
      },
      getData: () => context.getQueryData(queryKey),
      getInfiniteData: () => context.getInfiniteQueryData(queryKey),
      /**
       * DecorateMutationProcedure
       */
      setMutationDefaults: () =>
        context.setMutationDefaults(getMutationKeyInternal(path), input),
      getMutationDefaults: () =>
        context.getMutationDefaults(getMutationKeyInternal(path)),
      isMutating: () =>
        context.isMutating({ mutationKey: getMutationKeyInternal(path) }),
    };

    return contextMap[utilName]();
  });
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createRecursiveUtilsProxy<TRouter extends AnyRouter>(
  context: TRPCQueryUtils<TRouter>,
) {
  return createRecursiveProxy<CreateQueryUtils<TRouter>>((opts) => {
    const path = [...opts.path];
    const utilName = path.pop() as keyof AnyDecoratedProcedure;
    const args = [...opts.args] as Parameters<
      AnyDecoratedProcedure[typeof utilName]
    >;
    const input = args.shift(); // args can now be spread when input removed
    const queryType = getQueryType(utilName);
    const queryKey = getQueryKeyInternal(path, input, queryType);

    // `getQueryKeyInternal` strips `skipToken` from the query key, so the
    // options helpers can't detect it and would return a real `queryFn`
    const withSkipToken = <TOptions extends object>(options: TOptions) =>
      input === skipToken ? { ...options, queryFn: skipToken } : options;

    const contextMap: Record<keyof AnyDecoratedProcedure, () => unknown> = {
      infiniteQueryOptions: () =>
        withSkipToken(context.infiniteQueryOptions(path, queryKey, args[0])),
      queryOptions: () =>
        withSkipToken(context.queryOptions(path, queryKey, ...args)),
      /**
       * DecorateQueryProcedure
       */
      fetch: () => context.fetchQuery(queryKey, ...args),
      fetchInfinite: () => context.fetchInfiniteQuery(queryKey, args[0]),
      prefetch: () => context.prefetchQuery(queryKey, ...args),
      prefetchInfinite: () => context.prefetchInfiniteQuery(queryKey, args[0]),
      ensureData: () => context.ensureQueryData(queryKey, ...args),
      invalidate: () => context.invalidateQueries(queryKey, ...args),
      reset: () => context.resetQueries(queryKey, ...args),
      refetch: () => context.refetchQueries(queryKey, ...args),
      cancel: () => context.cancelQuery(queryKey, ...args),
      setData: () => {
        context.setQueryData(queryKey, args[0], args[1]);
      },
      setQueriesData: () =>
        context.setQueriesData(queryKey, args[0], args[1], args[2]),
      setInfiniteData: () => {
        context.setInfiniteQueryData(queryKey, args[0], args[1]);
      },
      getData: () => context.getQueryData(queryKey),
      getInfiniteData: () => context.getInfiniteQueryData(queryKey),
      /**
       * DecorateMutationProcedure
       */
      setMutationDefaults: () =>
        context.setMutationDefaults(getMutationKeyInternal(path), input),
      getMutationDefaults: () =>
        context.getMutationDefaults(getMutationKeyInternal(path)),
      isMutating: () =>
        context.isMutating({ mutationKey: getMutationKeyInternal(path) }),
    };

    return contextMap[utilName]();
  });
}
```

### 🔹 函式: `infiniteQueryOptions()`
- **變更前簽章 (Before)**: `infiniteQueryOptions()` (L479~L480)
- **變更後簽章 (After)**: `infiniteQueryOptions()` (L485~L486)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() =>
        context.infiniteQueryOptions(path, queryKey, args[0])
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() =>
        withSkipToken(context.infiniteQueryOptions(path, queryKey, args[0]))
```

### 🔹 函式: `queryOptions()`
- **變更前簽章 (Before)**: `queryOptions()` (L481~L481)
- **變更後簽章 (After)**: `queryOptions()` (L487~L488)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => context.queryOptions(path, queryKey, ...args)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() =>
        withSkipToken(context.queryOptions(path, queryKey, ...args))
```


---

### 🔹 Commit #12: `f2aa8b07`
- **完整 Hash**: `f2aa8b0721a58cdd83211e4d9e8b4dfd8912b82a`
- **說明 (Ground Truth)**: fix(client): clean up subscriptions after synchronous retries (#7607)
- **變更檔案數**: 1

#### 📄 檔案: `packages/client/src/links/retryLink.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:10, E:7, A:0) ➔ After(N:10, E:7, A:0)
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

### 🔹 函式: `attempt()`
- **變更前簽章 (Before)**: `function attempt(attempts: number)` (L68~L109)
- **變更後簽章 (After)**: `function attempt(attempts: number)` (L70~L128)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function attempt(attempts: number) {
          const op = opWithLastEventId();

          next$ = callOpts.next(op).subscribe({
            error(error) {
              const shouldRetry = opts.retry({
                op,
                attempts,
                error,
              });
              if (!shouldRetry) {
                observer.error(error);
                return;
              }
              const delayMs = opts.retryDelayMs?.(attempts) ?? 0;

              if (delayMs <= 0) {
                attempt(attempts + 1);
                return;
              }
              callNextTimeout = setTimeout(
                () => attempt(attempts + 1),
                delayMs,
              );
            },
            next(envelope) {
              //
              if (
                (!envelope.result.type || envelope.result.type === 'data') &&
                envelope.result.id
              ) {
                //
                lastEventId = envelope.result.id;
              }

              observer.next(envelope);
            },
            complete() {
              observer.complete();
            },
          });
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function attempt(attempts: number) {
          if (disposed) {
            return;
          }
          currentAttempt = attempts;
          const op = opWithLastEventId();

          const subscription = callOpts.next(op).subscribe({
            error(error) {
              const shouldRetry = opts.retry({
                op,
                attempts,
                error,
              });
              if (disposed) {
                return;
              }
              if (!shouldRetry) {
                observer.error(error);
                return;
              }
              const delayMs = opts.retryDelayMs?.(attempts) ?? 0;
              if (disposed) {
                return;
              }

              if (delayMs <= 0) {
                attempt(attempts + 1);
                return;
              }
              callNextTimeout = setTimeout(
                () => attempt(attempts + 1),
                delayMs,
              );
            },
            next(envelope) {
              //
              if (
                (!envelope.result.type || envelope.result.type === 'data') &&
                envelope.result.id
              ) {
                //
                lastEventId = envelope.result.id;
              }

              observer.next(envelope);
            },
            complete() {
              observer.complete();
            },
          });

          // A synchronous error may have already subscribed the next attempt.
          if (disposed) {
            subscription.unsubscribe();
          } else if (currentAttempt === attempts) {
            next$ = subscription;
          }
        }
```

### 🔹 函式: `error()`
- **變更前簽章 (Before)**: `error(error)` (L72~L92)
- **變更後簽章 (After)**: `error(error)` (L78~L104)

#### ◀️ 變更前實作碼 (Before Implementation):
```
error(error) {
              const shouldRetry = opts.retry({
                op,
                attempts,
                error,
              });
              if (!shouldRetry) {
                observer.error(error);
                return;
              }
              const delayMs = opts.retryDelayMs?.(attempts) ?? 0;

              if (delayMs <= 0) {
                attempt(attempts + 1);
                return;
              }
              callNextTimeout = setTimeout(
                () => attempt(attempts + 1),
                delayMs,
              );
            }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
error(error) {
              const shouldRetry = opts.retry({
                op,
                attempts,
                error,
              });
              if (disposed) {
                return;
              }
              if (!shouldRetry) {
                observer.error(error);
                return;
              }
              const delayMs = opts.retryDelayMs?.(attempts) ?? 0;
              if (disposed) {
                return;
              }

              if (delayMs <= 0) {
                attempt(attempts + 1);
                return;
              }
              callNextTimeout = setTimeout(
                () => attempt(attempts + 1),
                delayMs,
              );
            }
```

### 🔹 函式: `retryLink()`
- **變更前簽章 (Before)**: `function retryLink<TInferrable extends InferrableClientTypes>(
  opts: RetryLinkOptions<TInferrable>,
): TRPCLink<TInferrable>` (L39~L117)
- **變更後簽章 (After)**: `function retryLink<TInferrable extends InferrableClientTypes>(
  opts: RetryLinkOptions<TInferrable>,
): TRPCLink<TInferrable>` (L39~L137)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function retryLink<TInferrable extends InferrableClientTypes>(
  opts: RetryLinkOptions<TInferrable>,
): TRPCLink<TInferrable> {
  // initialized config
  return () => {
    // initialized in app
    return (callOpts) => {
      // initialized for request
      return observable((observer) => {
        let next$: Unsubscribable;
        let callNextTimeout: ReturnType<typeof setTimeout> | undefined =
          undefined;

        let lastEventId: string | undefined = undefined;

        attempt(1);

        function opWithLastEventId() {
          const op = callOpts.op;
          if (!lastEventId) {
            return op;
          }

          return {
            ...op,
            input: inputWithTrackedEventId(op.input, lastEventId),
          };
        }

        function attempt(attempts: number) {
          const op = opWithLastEventId();

          next$ = callOpts.next(op).subscribe({
            error(error) {
              const shouldRetry = opts.retry({
                op,
                attempts,
                error,
              });
              if (!shouldRetry) {
                observer.error(error);
                return;
              }
              const delayMs = opts.retryDelayMs?.(attempts) ?? 0;

              if (delayMs <= 0) {
                attempt(attempts + 1);
                return;
              }
              callNextTimeout = setTimeout(
                () => attempt(attempts + 1),
                delayMs,
              );
            },
            next(envelope) {
              //
              if (
                (!envelope.result.type || envelope.result.type === 'data') &&
                envelope.result.id
              ) {
                //
                lastEventId = envelope.result.id;
              }

              observer.next(envelope);
            },
            complete() {
              observer.complete();
            },
          });
        }
        return () => {
          next$.unsubscribe();
          clearTimeout(callNextTimeout);
        };
      });
    };
  };
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function retryLink<TInferrable extends InferrableClientTypes>(
  opts: RetryLinkOptions<TInferrable>,
): TRPCLink<TInferrable> {
  // initialized config
  return () => {
    // initialized in app
    return (callOpts) => {
      // initialized for request
      return observable((observer) => {
        let next$: Unsubscribable;
        let currentAttempt = 0;
        let disposed = false;
        let callNextTimeout: ReturnType<typeof setTimeout> | undefined =
          undefined;

        let lastEventId: string | undefined = undefined;

        attempt(1);

        function opWithLastEventId() {
          const op = callOpts.op;
          if (!lastEventId) {
            return op;
          }

          return {
            ...op,
            input: inputWithTrackedEventId(op.input, lastEventId),
          };
        }

        function attempt(attempts: number) {
          if (disposed) {
            return;
          }
          currentAttempt = attempts;
          const op = opWithLastEventId();

          const subscription = callOpts.next(op).subscribe({
            error(error) {
              const shouldRetry = opts.retry({
                op,
                attempts,
                error,
              });
              if (disposed) {
                return;
              }
              if (!shouldRetry) {
                observer.error(error);
                return;
              }
              const delayMs = opts.retryDelayMs?.(attempts) ?? 0;
              if (disposed) {
                return;
              }

              if (delayMs <= 0) {
                attempt(attempts + 1);
                return;
              }
              callNextTimeout = setTimeout(
                () => attempt(attempts + 1),
                delayMs,
              );
            },
            next(envelope) {
              //
              if (
                (!envelope.result.type || envelope.result.type === 'data') &&
                envelope.result.id
              ) {
                //
                lastEventId = envelope.result.id;
              }

              observer.next(envelope);
            },
            complete() {
              observer.complete();
            },
          });

          // A synchronous error may have already subscribed the next attempt.
          if (disposed) {
            subscription.unsubscribe();
          } else if (currentAttempt === attempts) {
            next$ = subscription;
          }
        }
        return () => {
          disposed = true;
          next$.unsubscribe();
          clearTimeout(callNextTimeout);
        };
      });
    };
  };
}
```


---

### 🔹 Commit #13: `38d3bea6`
- **完整 Hash**: `38d3bea691ed5152ff63de463eb98ba3377fedac`
- **說明 (Ground Truth)**: fix(server): match content-type header case-insensitively (#7614)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/src/unstable-core-do-not-import/http/contentType.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:27, E:13, A:0) ➔ After(N:28, E:16, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 3, -Edges: 0, ΔFuncs: 6, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `hasContentType` (FUNCTION_DEF)
  • + [新增呼叫邊] `isMatch` ──[CALLS]──> `hasContentType`
  • + [新增呼叫邊] `isMatch` ──[CALLS]──> `hasContentType`
  • + [新增呼叫邊] `isMatch` ──[CALLS]──> `hasContentType`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `octetStreamContentTypeHandler()`
- **變更前簽章 (Before)**: `[Module State] octetStreamContentTypeHandler` (L252~L288)
- **變更後簽章 (After)**: `[Module State] octetStreamContentTypeHandler` (L261~L295)

#### ◀️ 變更前實作碼 (Before Implementation):
```
octetStreamContentTypeHandler: ContentTypeHandler = {
  isMatch(req) {
    return !!req.headers
      .get('content-type')
      ?.startsWith('application/octet-stream');
  },
  async parse(opts) {
    const { req } = opts;
    if (req.method !== 'POST') {
      throw new TRPCError({
        code: 'METHOD_NOT_SUPPORTED',
        message:
          'Only POST requests are supported for application/octet-stream requests',
      });
    }
    const getInputs = memo(async () => {
      return req.body;
    });
    return {
      calls: [
        {
          batchIndex: 0,
          path: opts.path,
          getRawInput: getInputs.read,
          result: getInputs.result,
          procedure: await getProcedureAtPath(opts.router, opts.path),
        },
      ],
      isBatchCall: false,
      accept: null,
      type: 'mutation',
      connectionParams: null,
      signal: req.signal,
      url: opts.url,
    };
  },
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
octetStreamContentTypeHandler: ContentTypeHandler = {
  isMatch(req) {
    return hasContentType(req, 'application/octet-stream');
  },
  async parse(opts) {
    const { req } = opts;
    if (req.method !== 'POST') {
      throw new TRPCError({
        code: 'METHOD_NOT_SUPPORTED',
        message:
          'Only POST requests are supported for application/octet-stream requests',
      });
    }
    const getInputs = memo(async () => {
      return req.body;
    });
    return {
      calls: [
        {
          batchIndex: 0,
          path: opts.path,
          getRawInput: getInputs.read,
          result: getInputs.result,
          procedure: await getProcedureAtPath(opts.router, opts.path),
        },
      ],
      isBatchCall: false,
      accept: null,
      type: 'mutation',
      connectionParams: null,
      signal: req.signal,
      url: opts.url,
    };
  },
}
```

### 🔹 函式: `jsonContentTypeHandler()`
- **變更前簽章 (Before)**: `[Module State] jsonContentTypeHandler` (L78~L212)
- **變更後簽章 (After)**: `[Module State] jsonContentTypeHandler` (L87~L221)

#### ◀️ 變更前實作碼 (Before Implementation):
```
jsonContentTypeHandler: ContentTypeHandler = {
  isMatch(req) {
    return !!req.headers.get('content-type')?.startsWith('application/json');
  },
  async parse(opts) {
    const { req } = opts;
    const isBatchCall = opts.searchParams.get('batch') === '1';
    const maxBatchSize = opts.maxBatchSize;

    const paths = isBatchCall ? opts.path.split(',') : [opts.path];
    if (
      isBatchCall &&
      typeof maxBatchSize === 'number' &&
      paths.length > maxBatchSize
    ) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batch call exceeds maximum size`,
      });
    }

    type InputRecord = Record<number, unknown>;
    const getInputs = memo(async (): Promise<InputRecord> => {
      let inputs: unknown = undefined;
      if (req.method === 'GET') {
        const queryInput = opts.searchParams.get('input');
        if (queryInput) {
          inputs = JSON.parse(queryInput);
        }
      } else {
        inputs = await req.json();
      }
      if (inputs === undefined) {
        return emptyObject();
      }

      if (!isBatchCall) {
        const result: InputRecord = emptyObject();
        result[0] =
          opts.router._def._config.transformer.input.deserialize(inputs);
        return result;
      }

      if (!isObject(inputs)) {
        throw new TRPCError({
          code: 'BAD_REQUEST',
          message: '"input" needs to be an object when doing a batch call',
        });
      }
      const acc: InputRecord = emptyObject();
      for (const index of paths.keys()) {
        const input = inputs[index];
        if (input !== undefined) {
          acc[index] =
            opts.router._def._config.transformer.input.deserialize(input);
        }
      }

      return acc;
    });

    const calls = await Promise.all(
      paths.map(
        async (path, index): Promise<TRPCRequestInfo['calls'][number]> => {
          const procedure = await getProcedureAtPath(opts.router, path);
          return {
            batchIndex: index,
            path,
            procedure,
            getRawInput: async () => {
              const inputs = await getInputs.read();
              let input = inputs[index];

              if (procedure?._def.type === 'subscription') {
                const lastEventId =
                  opts.headers.get('last-event-id') ??
                  opts.searchParams.get('lastEventId') ??
                  opts.searchParams.get('Last-Event-Id');

                if (lastEventId) {
                  if (isObject(input)) {
                    input = {
                      ...input,
                      lastEventId: lastEventId,
                    };
                  } else {
                    input ??= {
                      lastEventId: lastEventId,
                    };
                  }
                }
              }
              return input;
            },
            result: () => {
              return getInputs.result()?.[index];
            },
          };
        },
      ),
    );

    const types = new Set(
      calls.map((call) => call.procedure?._def.type).filter(Boolean),
    );

    /* istanbul ignore if -- @preserve */
    if (types.size > 1) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Cannot mix procedure types in call: ${Array.from(types).join(
          ', ',
        )}`,
      });
    }
    const type: ProcedureType | 'unknown' =
      types.values().next().value ?? 'unknown';

    const connectionParamsStr = opts.searchParams.get('connectionParams');

    const info: TRPCRequestInfo = {
      isBatchCall,
      accept: getAcceptHeader(req.headers),
      calls,
      type,
      connectionParams:
        connectionParamsStr === null
          ? null
          : parseConnectionParamsFromString(connectionParamsStr),
      signal: req.signal,
      url: opts.url,
    };
    return info;
  },
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
jsonContentTypeHandler: ContentTypeHandler = {
  isMatch(req) {
    return hasContentType(req, 'application/json');
  },
  async parse(opts) {
    const { req } = opts;
    const isBatchCall = opts.searchParams.get('batch') === '1';
    const maxBatchSize = opts.maxBatchSize;

    const paths = isBatchCall ? opts.path.split(',') : [opts.path];
    if (
      isBatchCall &&
      typeof maxBatchSize === 'number' &&
      paths.length > maxBatchSize
    ) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batch call exceeds maximum size`,
      });
    }

    type InputRecord = Record<number, unknown>;
    const getInputs = memo(async (): Promise<InputRecord> => {
      let inputs: unknown = undefined;
      if (req.method === 'GET') {
        const queryInput = opts.searchParams.get('input');
        if (queryInput) {
          inputs = JSON.parse(queryInput);
        }
      } else {
        inputs = await req.json();
      }
      if (inputs === undefined) {
        return emptyObject();
      }

      if (!isBatchCall) {
        const result: InputRecord = emptyObject();
        result[0] =
          opts.router._def._config.transformer.input.deserialize(inputs);
        return result;
      }

      if (!isObject(inputs)) {
        throw new TRPCError({
          code: 'BAD_REQUEST',
          message: '"input" needs to be an object when doing a batch call',
        });
      }
      const acc: InputRecord = emptyObject();
      for (const index of paths.keys()) {
        const input = inputs[index];
        if (input !== undefined) {
          acc[index] =
            opts.router._def._config.transformer.input.deserialize(input);
        }
      }

      return acc;
    });

    const calls = await Promise.all(
      paths.map(
        async (path, index): Promise<TRPCRequestInfo['calls'][number]> => {
          const procedure = await getProcedureAtPath(opts.router, path);
          return {
            batchIndex: index,
            path,
            procedure,
            getRawInput: async () => {
              const inputs = await getInputs.read();
              let input = inputs[index];

              if (procedure?._def.type === 'subscription') {
                const lastEventId =
                  opts.headers.get('last-event-id') ??
                  opts.searchParams.get('lastEventId') ??
                  opts.searchParams.get('Last-Event-Id');

                if (lastEventId) {
                  if (isObject(input)) {
                    input = {
                      ...input,
                      lastEventId: lastEventId,
                    };
                  } else {
                    input ??= {
                      lastEventId: lastEventId,
                    };
                  }
                }
              }
              return input;
            },
            result: () => {
              return getInputs.result()?.[index];
            },
          };
        },
      ),
    );

    const types = new Set(
      calls.map((call) => call.procedure?._def.type).filter(Boolean),
    );

    /* istanbul ignore if -- @preserve */
    if (types.size > 1) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Cannot mix procedure types in call: ${Array.from(types).join(
          ', ',
        )}`,
      });
    }
    const type: ProcedureType | 'unknown' =
      types.values().next().value ?? 'unknown';

    const connectionParamsStr = opts.searchParams.get('connectionParams');

    const info: TRPCRequestInfo = {
      isBatchCall,
      accept: getAcceptHeader(req.headers),
      calls,
      type,
      connectionParams:
        connectionParamsStr === null
          ? null
          : parseConnectionParamsFromString(connectionParamsStr),
      signal: req.signal,
      url: opts.url,
    };
    return info;
  },
}
```

### 🔹 函式: `isMatch()`
- **變更前簽章 (Before)**: `isMatch(req)` (L79~L81)
- **變更後簽章 (After)**: `isMatch(req)` (L88~L90)

#### ◀️ 變更前實作碼 (Before Implementation):
```
isMatch(req) {
    return !!req.headers.get('content-type')?.startsWith('application/json');
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
isMatch(req) {
    return hasContentType(req, 'application/json');
  }
```

### 🔹 函式: `isMatch()`
- **變更前簽章 (Before)**: `isMatch(req)` (L253~L257)
- **變更後簽章 (After)**: `isMatch(req)` (L262~L264)

#### ◀️ 變更前實作碼 (Before Implementation):
```
isMatch(req) {
    return !!req.headers
      .get('content-type')
      ?.startsWith('application/octet-stream');
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
isMatch(req) {
    return hasContentType(req, 'application/octet-stream');
  }
```

### 🔹 函式: `isMatch()`
- **變更前簽章 (Before)**: `isMatch(req)` (L215~L217)
- **變更後簽章 (After)**: `isMatch(req)` (L224~L226)

#### ◀️ 變更前實作碼 (Before Implementation):
```
isMatch(req) {
    return !!req.headers.get('content-type')?.startsWith('multipart/form-data');
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
isMatch(req) {
    return hasContentType(req, 'multipart/form-data');
  }
```

### 🔹 函式: `formDataContentTypeHandler()`
- **變更前簽章 (Before)**: `[Module State] formDataContentTypeHandler` (L214~L250)
- **變更後簽章 (After)**: `[Module State] formDataContentTypeHandler` (L223~L259)

#### ◀️ 變更前實作碼 (Before Implementation):
```
formDataContentTypeHandler: ContentTypeHandler = {
  isMatch(req) {
    return !!req.headers.get('content-type')?.startsWith('multipart/form-data');
  },
  async parse(opts) {
    const { req } = opts;
    if (req.method !== 'POST') {
      throw new TRPCError({
        code: 'METHOD_NOT_SUPPORTED',
        message:
          'Only POST requests are supported for multipart/form-data requests',
      });
    }
    const getInputs = memo(async () => {
      const fd = await req.formData();
      return fd;
    });
    const procedure = await getProcedureAtPath(opts.router, opts.path);
    return {
      accept: null,
      calls: [
        {
          batchIndex: 0,
          path: opts.path,
          getRawInput: getInputs.read,
          result: getInputs.result,
          procedure,
        },
      ],
      isBatchCall: false,
      type: 'mutation',
      connectionParams: null,
      signal: req.signal,
      url: opts.url,
    };
  },
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
formDataContentTypeHandler: ContentTypeHandler = {
  isMatch(req) {
    return hasContentType(req, 'multipart/form-data');
  },
  async parse(opts) {
    const { req } = opts;
    if (req.method !== 'POST') {
      throw new TRPCError({
        code: 'METHOD_NOT_SUPPORTED',
        message:
          'Only POST requests are supported for multipart/form-data requests',
      });
    }
    const getInputs = memo(async () => {
      const fd = await req.formData();
      return fd;
    });
    const procedure = await getProcedureAtPath(opts.router, opts.path);
    return {
      accept: null,
      calls: [
        {
          batchIndex: 0,
          path: opts.path,
          getRawInput: getInputs.read,
          result: getInputs.result,
          procedure,
        },
      ],
      isBatchCall: false,
      type: 'mutation',
      connectionParams: null,
      signal: req.signal,
      url: opts.url,
    };
  },
}
```


---

### 🔹 Commit #14: `6388402d`
- **完整 Hash**: `6388402d82c4b6f33aef3096f1c349ce6de4b2ac`
- **說明 (Ground Truth)**: fix(react-query,tanstack-react-query): keep falsy inputs in query keys (#7623)
- **變更檔案數**: 2

#### 📄 檔案: `packages/react-query/src/internals/getQueryKey.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:6, E:4, A:0) ➔ After(N:6, E:4, A:0)
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

### 🔹 函式: `getQueryKeyInternal()`
- **變更前簽章 (Before)**: `function getQueryKeyInternal(
  path: readonly string[],
  input: unknown,
  type: QueryType,
): TRPCQueryKey` (L26~L72)
- **變更後簽章 (After)**: `function getQueryKeyInternal(
  path: readonly string[],
  input: unknown,
  type: QueryType,
): TRPCQueryKey` (L26~L72)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function getQueryKeyInternal(
  path: readonly string[],
  input: unknown,
  type: QueryType,
): TRPCQueryKey {
  // Construct a query key that is easy to destructure and flexible for
  // partial selecting etc.
  // https://github.com/trpc/trpc/issues/3128

  // some parts of the path may be dot-separated, split them up
  const splitPath = path.flatMap((part) => part.split('.'));

  if (!input && (!type || type === 'any')) {
    // this matches also all mutations (see `getMutationKeyInternal`)

    // for `utils.invalidate()` to match all queries (including vanilla react-query)
    // we don't want nested array if path is empty, i.e. `[]` instead of `[[]]`
    return splitPath.length ? [splitPath] : ([] as unknown as TRPCQueryKey);
  }

  if (
    type === 'infinite' &&
    isObject(input) &&
    ('direction' in input || 'cursor' in input)
  ) {
    const {
      cursor: _,
      direction: __,
      ...inputWithoutCursorAndDirection
    } = input;
    return [
      splitPath,
      {
        input: inputWithoutCursorAndDirection,
        type: 'infinite',
      },
    ];
  }
  return [
    splitPath,
    {
      ...(typeof input !== 'undefined' &&
        input !== skipToken && { input: input }),
      ...(type && type !== 'any' && { type: type }),
    },
  ];
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function getQueryKeyInternal(
  path: readonly string[],
  input: unknown,
  type: QueryType,
): TRPCQueryKey {
  // Construct a query key that is easy to destructure and flexible for
  // partial selecting etc.
  // https://github.com/trpc/trpc/issues/3128

  // some parts of the path may be dot-separated, split them up
  const splitPath = path.flatMap((part) => part.split('.'));

  if (typeof input === 'undefined' && (!type || type === 'any')) {
    // this matches also all mutations (see `getMutationKeyInternal`)

    // for `utils.invalidate()` to match all queries (including vanilla react-query)
    // we don't want nested array if path is empty, i.e. `[]` instead of `[[]]`
    return splitPath.length ? [splitPath] : ([] as unknown as TRPCQueryKey);
  }

  if (
    type === 'infinite' &&
    isObject(input) &&
    ('direction' in input || 'cursor' in input)
  ) {
    const {
      cursor: _,
      direction: __,
      ...inputWithoutCursorAndDirection
    } = input;
    return [
      splitPath,
      {
        input: inputWithoutCursorAndDirection,
        type: 'infinite',
      },
    ];
  }
  return [
    splitPath,
    {
      ...(typeof input !== 'undefined' &&
        input !== skipToken && { input: input }),
      ...(type && type !== 'any' && { type: type }),
    },
  ];
}
```


#### 📄 檔案: `packages/tanstack-react-query/src/internals/utils.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:14, E:6, A:0) ➔ After(N:14, E:6, A:0)
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

### 🔹 函式: `key()`
- **變更前簽章 (Before)**: `key()` (L127~L172)
- **變更後簽章 (After)**: `key()` (L127~L172)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(): TRPCQueryKeyWithoutPrefix => {
    const { input, type } = opts;

    // Construct a query key that is easy to destructure and flexible for
    // partial selecting etc.
    // https://github.com/trpc/trpc/issues/3128

    // some parts of the path may be dot-separated, split them up
    const splitPath = opts.path.flatMap((part) => part.split('.'));

    if (!input && type === 'any') {
      // this matches also all mutations (see `getMutationKeyInternal`)

      // for `utils.invalidate()` to match all queries (including vanilla react-query)
      // we don't want nested array if path is empty, i.e. `[]` instead of `[[]]`
      return splitPath.length ? [splitPath] : ([] as unknown as TRPCQueryKey);
    }

    if (
      type === 'infinite' &&
      isObject(input) &&
      ('direction' in input || 'cursor' in input)
    ) {
      const {
        cursor: _,
        direction: __,
        ...inputWithoutCursorAndDirection
      } = input;
      return [
        splitPath,
        {
          input: inputWithoutCursorAndDirection,
          type: 'infinite',
        },
      ];
    }

    return [
      splitPath,
      {
        ...(typeof input !== 'undefined' &&
          input !== skipToken && { input: input }),
        ...(type && type !== 'any' && { type: type }),
      },
    ];
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(): TRPCQueryKeyWithoutPrefix => {
    const { input, type } = opts;

    // Construct a query key that is easy to destructure and flexible for
    // partial selecting etc.
    // https://github.com/trpc/trpc/issues/3128

    // some parts of the path may be dot-separated, split them up
    const splitPath = opts.path.flatMap((part) => part.split('.'));

    if (typeof input === 'undefined' && type === 'any') {
      // this matches also all mutations (see `getMutationKeyInternal`)

      // for `utils.invalidate()` to match all queries (including vanilla react-query)
      // we don't want nested array if path is empty, i.e. `[]` instead of `[[]]`
      return splitPath.length ? [splitPath] : ([] as unknown as TRPCQueryKey);
    }

    if (
      type === 'infinite' &&
      isObject(input) &&
      ('direction' in input || 'cursor' in input)
    ) {
      const {
        cursor: _,
        direction: __,
        ...inputWithoutCursorAndDirection
      } = input;
      return [
        splitPath,
        {
          input: inputWithoutCursorAndDirection,
          type: 'infinite',
        },
      ];
    }

    return [
      splitPath,
      {
        ...(typeof input !== 'undefined' &&
          input !== skipToken && { input: input }),
        ...(type && type !== 'any' && { type: type }),
      },
    ];
  }
```

### 🔹 函式: `getQueryKeyInternal()`
- **變更前簽章 (Before)**: `function getQueryKeyInternal(opts:` (L121~L178)
- **變更後簽章 (After)**: `function getQueryKeyInternal(opts:` (L121~L178)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function getQueryKeyInternal(opts: {
  path: string[];
  input?: unknown;
  type: QueryType;
  prefix: string | undefined;
}): AnyTRPCQueryKey {
  const key = run((): TRPCQueryKeyWithoutPrefix => {
    const { input, type } = opts;

    // Construct a query key that is easy to destructure and flexible for
    // partial selecting etc.
    // https://github.com/trpc/trpc/issues/3128

    // some parts of the path may be dot-separated, split them up
    const splitPath = opts.path.flatMap((part) => part.split('.'));

    if (!input && type === 'any') {
      // this matches also all mutations (see `getMutationKeyInternal`)

      // for `utils.invalidate()` to match all queries (including vanilla react-query)
      // we don't want nested array if path is empty, i.e. `[]` instead of `[[]]`
      return splitPath.length ? [splitPath] : ([] as unknown as TRPCQueryKey);
    }

    if (
      type === 'infinite' &&
      isObject(input) &&
      ('direction' in input || 'cursor' in input)
    ) {
      const {
        cursor: _,
        direction: __,
        ...inputWithoutCursorAndDirection
      } = input;
      return [
        splitPath,
        {
          input: inputWithoutCursorAndDirection,
          type: 'infinite',
        },
      ];
    }

    return [
      splitPath,
      {
        ...(typeof input !== 'undefined' &&
          input !== skipToken && { input: input }),
        ...(type && type !== 'any' && { type: type }),
      },
    ];
  });

  if (opts.prefix) {
    key.unshift([opts.prefix]);
  }
  return key;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function getQueryKeyInternal(opts: {
  path: string[];
  input?: unknown;
  type: QueryType;
  prefix: string | undefined;
}): AnyTRPCQueryKey {
  const key = run((): TRPCQueryKeyWithoutPrefix => {
    const { input, type } = opts;

    // Construct a query key that is easy to destructure and flexible for
    // partial selecting etc.
    // https://github.com/trpc/trpc/issues/3128

    // some parts of the path may be dot-separated, split them up
    const splitPath = opts.path.flatMap((part) => part.split('.'));

    if (typeof input === 'undefined' && type === 'any') {
      // this matches also all mutations (see `getMutationKeyInternal`)

      // for `utils.invalidate()` to match all queries (including vanilla react-query)
      // we don't want nested array if path is empty, i.e. `[]` instead of `[[]]`
      return splitPath.length ? [splitPath] : ([] as unknown as TRPCQueryKey);
    }

    if (
      type === 'infinite' &&
      isObject(input) &&
      ('direction' in input || 'cursor' in input)
    ) {
      const {
        cursor: _,
        direction: __,
        ...inputWithoutCursorAndDirection
      } = input;
      return [
        splitPath,
        {
          input: inputWithoutCursorAndDirection,
          type: 'infinite',
        },
      ];
    }

    return [
      splitPath,
      {
        ...(typeof input !== 'undefined' &&
          input !== skipToken && { input: input }),
        ...(type && type !== 'any' && { type: type }),
      },
    ];
  });

  if (opts.prefix) {
    key.unshift([opts.prefix]);
  }
  return key;
}
```


---

### 🔹 Commit #15: `db2605f3`
- **完整 Hash**: `db2605f3980ff0d324e0ab0d7c5c16f1fd3e7b21`
- **說明 (Ground Truth)**: fix(server): keep inferred types portable without baseUrl (#7662)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/tsdown.config.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:5, E:1, A:0) ➔ After(N:6, E:1, A:0)
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
  • + [新增節點] `footer` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #16: `ecac9d93`
- **完整 Hash**: `ecac9d9319d3c2a6e6183b9929a4a5421d81e96e`
- **說明 (Ground Truth)**: fix(server): cancel backpressured responses on disconnect (#7661)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/src/adapters/node-http/writeResponse.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:10, E:7, A:0) ➔ After(N:10, E:7, A:0)
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

### 🔹 函式: `writeResponseBodyChunk()`
- **變更前簽章 (Before)**: `async function writeResponseBodyChunk(
  res: NodeHTTPResponse,
  chunk: Uint8Array,
)` (L5~L30)
- **變更後簽章 (After)**: `async function writeResponseBodyChunk(
  res: NodeHTTPResponse,
  chunk: Uint8Array,
)` (L5~L32)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async function writeResponseBodyChunk(
  res: NodeHTTPResponse,
  chunk: Uint8Array,
) {
  // useful for debugging 🙃
  // console.debug('writing', new TextDecoder().decode(chunk));

  if (res.write(chunk) === false) {
    await new Promise<void>((resolve, reject) => {
      const onError = (err: unknown) => {
        reject(err);
        cleanup();
      };
      const onDrain = () => {
        resolve();
        cleanup();
      };
      const cleanup = () => {
        res.off('error', onError);
        res.off('drain', onDrain);
      };
      res.once('error', onError);
      res.once('drain', onDrain);
    });
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async function writeResponseBodyChunk(
  res: NodeHTTPResponse,
  chunk: Uint8Array,
) {
  // useful for debugging 🙃
  // console.debug('writing', new TextDecoder().decode(chunk));

  if (res.write(chunk) === false) {
    await new Promise<void>((resolve, reject) => {
      const onError = (err: unknown) => {
        reject(err);
        cleanup();
      };
      const onDrain = () => {
        resolve();
        cleanup();
      };
      const cleanup = () => {
        res.off('error', onError);
        res.off('drain', onDrain);
        res.off('close', onDrain);
      };
      res.once('error', onError);
      res.once('drain', onDrain);
      res.once('close', onDrain);
    });
  }
}
```

### 🔹 函式: `cleanup()`
- **變更前簽章 (Before)**: `cleanup()` (L22~L25)
- **變更後簽章 (After)**: `cleanup()` (L22~L26)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
        res.off('error', onError);
        res.off('drain', onDrain);
      }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
        res.off('error', onError);
        res.off('drain', onDrain);
        res.off('close', onDrain);
      }
```


---

### 🔹 Commit #17: `22220b3e`
- **完整 Hash**: `22220b3e7bb2abd36e197d52c9bff82c447e67b6`
- **說明 (Ground Truth)**: feat(react-query): pass `trpc.context` to links in `useSubscription` (#7655)
- **變更檔案數**: 2

#### 📄 檔案: `packages/react-query/src/shared/hooks/createHooksInternal.tsx`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:58, E:70, A:0) ➔ After(N:58, E:70, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'updateState' 被深鎖在內部閉包 (scope:useSubscription@after/packages/react-query/src/shared/hooks/createHooksInternal.tsx:L374C3)，外部無法調用！ (共 5 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `reset()`
- **變更前簽章 (Before)**: `reset()` (L420~L501)
- **變更後簽章 (After)**: `reset()` (L420~L502)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(): void => {
      // unsubscribe from the previous subscription
      currentSubscriptionRef.current?.unsubscribe();

      if (!enabled) {
        updateState(() => ({ ...initialStateIdle, reset }));
        return;
      }
      updateState(() => ({ ...initialStateConnecting, reset }));
      const subscription = client.subscription(
        path.join('.'),
        input ?? undefined,
        {
          onStarted: () => {
            optsRef.current.onStarted?.();
            updateState((prev) => ({
              ...prev,
              status: 'pending',
              error: null,
            }));
          },
          onData: (data) => {
            optsRef.current.onData?.(data);
            updateState((prev) => ({
              ...prev,
              status: 'pending',
              data,
              error: null,
            }));
          },
          onError: (error) => {
            optsRef.current.onError?.(error);
            updateState((prev) => ({
              ...prev,
              status: 'error',
              error,
            }));
          },
          onConnectionStateChange: (result) => {
            updateState((prev) => {
              switch (result.state) {
                case 'idle':
                  return {
                    ...prev,
                    status: result.state,
                    error: null,
                    data: undefined,
                  };
                case 'connecting':
                  return {
                    ...prev,
                    error: result.error,
                    status: result.state,
                  };

                case 'pending':
                  // handled when data is / onStarted
                  return prev;
              }
            });
          },
          onComplete: () => {
            optsRef.current.onComplete?.();

            // In the case of WebSockets, the connection might not be idle so `onConnectionStateChange` will not be called until the connection is closed.
            // In this case, we need to set the state to idle manually.
            updateState((prev) => ({
              ...prev,
              status: 'idle',
              error: null,
              data: undefined,
            }));

            // (We might want to add a `connectionState` to the state to track the connection state separately)
          },
        },
      );

      currentSubscriptionRef.current = subscription;

      // eslint-disable-next-line react-hooks/exhaustive-deps
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(): void => {
      // unsubscribe from the previous subscription
      currentSubscriptionRef.current?.unsubscribe();

      if (!enabled) {
        updateState(() => ({ ...initialStateIdle, reset }));
        return;
      }
      updateState(() => ({ ...initialStateConnecting, reset }));
      const subscription = client.subscription(
        path.join('.'),
        input ?? undefined,
        {
          context: optsRef.current?.trpc?.context,
          onStarted: () => {
            optsRef.current.onStarted?.();
            updateState((prev) => ({
              ...prev,
              status: 'pending',
              error: null,
            }));
          },
          onData: (data) => {
            optsRef.current.onData?.(data);
            updateState((prev) => ({
              ...prev,
              status: 'pending',
              data,
              error: null,
            }));
          },
          onError: (error) => {
            optsRef.current.onError?.(error);
            updateState((prev) => ({
              ...prev,
              status: 'error',
              error,
            }));
          },
          onConnectionStateChange: (result) => {
            updateState((prev) => {
              switch (result.state) {
                case 'idle':
                  return {
                    ...prev,
                    status: result.state,
                    error: null,
                    data: undefined,
                  };
                case 'connecting':
                  return {
                    ...prev,
                    error: result.error,
                    status: result.state,
                  };

                case 'pending':
                  // handled when data is / onStarted
                  return prev;
              }
            });
          },
          onComplete: () => {
            optsRef.current.onComplete?.();

            // In the case of WebSockets, the connection might not be idle so `onConnectionStateChange` will not be called until the connection is closed.
            // In this case, we need to set the state to idle manually.
            updateState((prev) => ({
              ...prev,
              status: 'idle',
              error: null,
              data: undefined,
            }));

            // (We might want to add a `connectionState` to the state to track the connection state separately)
          },
        },
      );

      currentSubscriptionRef.current = subscription;

      // eslint-disable-next-line react-hooks/exhaustive-deps
    }
```

### 🔹 函式: `useSubscription()`
- **變更前簽章 (Before)**: `function useSubscription(
    path: readonly string[],
    input: unknown,
    opts: UseTRPCSubscriptionOptions<unknown, TError>,
  )` (L374~L521)
- **變更後簽章 (After)**: `function useSubscription(
    path: readonly string[],
    input: unknown,
    opts: UseTRPCSubscriptionOptions<unknown, TError>,
  )` (L374~L522)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function useSubscription(
    path: readonly string[],
    input: unknown,
    opts: UseTRPCSubscriptionOptions<unknown, TError>,
  ) {
    const enabled = opts?.enabled ?? input !== skipToken;
    const queryKey = hashKey(getQueryKeyInternal(path, input, 'any'));
    const { client } = useContext();

    const optsRef = React.useRef<typeof opts>(opts);
    React.useEffect(() => {
      optsRef.current = opts;
    });

    type $Result = TRPCSubscriptionResult<unknown, TError>;

    const [trackedProps] = React.useState(new Set<keyof $Result>([]));

    const addTrackedProp = React.useCallback(
      (key: keyof $Result) => {
        trackedProps.add(key);
      },
      [trackedProps],
    );

    const currentSubscriptionRef = React.useRef<Unsubscribable>(null);

    const updateState = React.useCallback(
      (callback: (prevState: $Result) => $Result) => {
        const prev = resultRef.current;
        const next = (resultRef.current = callback(prev));

        let shouldUpdate = false;
        for (const key of trackedProps) {
          if (prev[key] !== next[key]) {
            shouldUpdate = true;
            break;
          }
        }
        if (shouldUpdate) {
          setState(trackResult(next, addTrackedProp));
        }
      },
      [addTrackedProp, trackedProps],
    );

    const reset = React.useCallback((): void => {
      // unsubscribe from the previous subscription
      currentSubscriptionRef.current?.unsubscribe();

      if (!enabled) {
        updateState(() => ({ ...initialStateIdle, reset }));
        return;
      }
      updateState(() => ({ ...initialStateConnecting, reset }));
      const subscription = client.subscription(
        path.join('.'),
        input ?? undefined,
        {
          onStarted: () => {
            optsRef.current.onStarted?.();
            updateState((prev) => ({
              ...prev,
              status: 'pending',
              error: null,
            }));
          },
          onData: (data) => {
            optsRef.current.onData?.(data);
            updateState((prev) => ({
              ...prev,
              status: 'pending',
              data,
              error: null,
            }));
          },
          onError: (error) => {
            optsRef.current.onError?.(error);
            updateState((prev) => ({
              ...prev,
              status: 'error',
              error,
            }));
          },
          onConnectionStateChange: (result) => {
            updateState((prev) => {
              switch (result.state) {
                case 'idle':
                  return {
                    ...prev,
                    status: result.state,
                    error: null,
                    data: undefined,
                  };
                case 'connecting':
                  return {
                    ...prev,
                    error: result.error,
                    status: result.state,
                  };

                case 'pending':
                  // handled when data is / onStarted
                  return prev;
              }
            });
          },
          onComplete: () => {
            optsRef.current.onComplete?.();

            // In the case of WebSockets, the connection might not be idle so `onConnectionStateChange` will not be called until the connection is closed.
            // In this case, we need to set the state to idle manually.
            updateState((prev) => ({
              ...prev,
              status: 'idle',
              error: null,
              data: undefined,
            }));

            // (We might want to add a `connectionState` to the state to track the connection state separately)
          },
        },
      );

      currentSubscriptionRef.current = subscription;

      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [client, queryKey, enabled, updateState]);
    React.useEffect(() => {
      reset();

      return () => {
        currentSubscriptionRef.current?.unsubscribe();
      };
    }, [reset]);

    const resultRef = React.useRef<$Result>(
      enabled
        ? { ...initialStateConnecting, reset }
        : { ...initialStateIdle, reset },
    );

    const [state, setState] = React.useState<$Result>(
      trackResult(resultRef.current, addTrackedProp),
    );

    return state;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function useSubscription(
    path: readonly string[],
    input: unknown,
    opts: UseTRPCSubscriptionOptions<unknown, TError>,
  ) {
    const enabled = opts?.enabled ?? input !== skipToken;
    const queryKey = hashKey(getQueryKeyInternal(path, input, 'any'));
    const { client } = useContext();

    const optsRef = React.useRef<typeof opts>(opts);
    React.useEffect(() => {
      optsRef.current = opts;
    });

    type $Result = TRPCSubscriptionResult<unknown, TError>;

    const [trackedProps] = React.useState(new Set<keyof $Result>([]));

    const addTrackedProp = React.useCallback(
      (key: keyof $Result) => {
        trackedProps.add(key);
      },
      [trackedProps],
    );

    const currentSubscriptionRef = React.useRef<Unsubscribable>(null);

    const updateState = React.useCallback(
      (callback: (prevState: $Result) => $Result) => {
        const prev = resultRef.current;
        const next = (resultRef.current = callback(prev));

        let shouldUpdate = false;
        for (const key of trackedProps) {
          if (prev[key] !== next[key]) {
            shouldUpdate = true;
            break;
          }
        }
        if (shouldUpdate) {
          setState(trackResult(next, addTrackedProp));
        }
      },
      [addTrackedProp, trackedProps],
    );

    const reset = React.useCallback((): void => {
      // unsubscribe from the previous subscription
      currentSubscriptionRef.current?.unsubscribe();

      if (!enabled) {
        updateState(() => ({ ...initialStateIdle, reset }));
        return;
      }
      updateState(() => ({ ...initialStateConnecting, reset }));
      const subscription = client.subscription(
        path.join('.'),
        input ?? undefined,
        {
          context: optsRef.current?.trpc?.context,
          onStarted: () => {
            optsRef.current.onStarted?.();
            updateState((prev) => ({
              ...prev,
              status: 'pending',
              error: null,
            }));
          },
          onData: (data) => {
            optsRef.current.onData?.(data);
            updateState((prev) => ({
              ...prev,
              status: 'pending',
              data,
              error: null,
            }));
          },
          onError: (error) => {
            optsRef.current.onError?.(error);
            updateState((prev) => ({
              ...prev,
              status: 'error',
              error,
            }));
          },
          onConnectionStateChange: (result) => {
            updateState((prev) => {
              switch (result.state) {
                case 'idle':
                  return {
                    ...prev,
                    status: result.state,
                    error: null,
                    data: undefined,
                  };
                case 'connecting':
                  return {
                    ...prev,
                    error: result.error,
                    status: result.state,
                  };

                case 'pending':
                  // handled when data is / onStarted
                  return prev;
              }
            });
          },
          onComplete: () => {
            optsRef.current.onComplete?.();

            // In the case of WebSockets, the connection might not be idle so `onConnectionStateChange` will not be called until the connection is closed.
            // In this case, we need to set the state to idle manually.
            updateState((prev) => ({
              ...prev,
              status: 'idle',
              error: null,
              data: undefined,
            }));

            // (We might want to add a `connectionState` to the state to track the connection state separately)
          },
        },
      );

      currentSubscriptionRef.current = subscription;

      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [client, queryKey, enabled, updateState]);
    React.useEffect(() => {
      reset();

      return () => {
        currentSubscriptionRef.current?.unsubscribe();
      };
    }, [reset]);

    const resultRef = React.useRef<$Result>(
      enabled
        ? { ...initialStateConnecting, reset }
        : { ...initialStateIdle, reset },
    );

    const [state, setState] = React.useState<$Result>(
      trackResult(resultRef.current, addTrackedProp),
    );

    return state;
  }
```

### 🔹 函式: `createRootHooks()`
- **變更前簽章 (Before)**: `function createRootHooks<
  TRouter extends AnyRouter,
  TSSRContext = unknown,
>(config?: CreateTRPCReactOptions<TRouter>)` (L82~L769)
- **變更後簽章 (After)**: `function createRootHooks<
  TRouter extends AnyRouter,
  TSSRContext = unknown,
>(config?: CreateTRPCReactOptions<TRouter>)` (L82~L770)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createRootHooks<
  TRouter extends AnyRouter,
  TSSRContext = unknown,
>(config?: CreateTRPCReactOptions<TRouter>) {
  const mutationSuccessOverride: UseMutationOverride['onSuccess'] =
    config?.overrides?.useMutation?.onSuccess ??
    ((options) => options.originalFn());

  type TError = TRPCClientErrorLike<TRouter>;

  type ProviderContext = TRPCContextState<TRouter, TSSRContext>;

  const Context = (config?.context ??
    TRPCContext) as React.Context<ProviderContext>;

  const createClient = createTRPCClient<TRouter>;

  const TRPCProvider: TRPCProvider<TRouter, TSSRContext> = (props) => {
    const { abortOnUnmount = false, queryClient, ssrContext } = props;
    const [ssrState, setSSRState] = React.useState<SSRState>(
      props.ssrState ?? false,
    );

    const client: TRPCUntypedClient<TRouter> =
      props.client instanceof TRPCUntypedClient
        ? props.client
        : getUntypedClient(props.client);

    const fns = React.useMemo(
      () =>
        createUtilityFunctions({
          client,
          queryClient,
        }),
      [client, queryClient],
    );

    const contextValue = React.useMemo<ProviderContext>(
      () => ({
        abortOnUnmount,
        queryClient,
        client,
        ssrContext: ssrContext ?? null,
        ssrState,
        ...fns,
      }),
      [abortOnUnmount, client, fns, queryClient, ssrContext, ssrState],
    );

    React.useEffect(() => {
      // Only updating state to `mounted` if we are using SSR.
      // This makes it so we don't have an unnecessary re-render when opting out of SSR.
      setSSRState((state) => (state ? 'mounted' : false));
    }, []);
    return (
      <Context.Provider value={contextValue}>{props.children}</Context.Provider>
    );
  };

  function useContext() {
    const context = React.useContext(Context);

    if (!context) {
      throw new Error(
        'Unable to find tRPC Context. Did you forget to wrap your App inside `withTRPC` HoC?',
      );
    }
    return context;
  }

  /**
   * Hack to make sure errors return `status`='error` when doing SSR
   * @see https://github.com/trpc/trpc/pull/1645
   */
  function useSSRQueryOptionsIfNeeded<
    TOptions extends { retryOnMount?: boolean } | undefined,
  >(queryKey: TRPCQueryKey, opts: TOptions): TOptions {
    const { queryClient, ssrState } = useContext();
    return ssrState &&
      ssrState !== 'mounted' &&
      queryClient.getQueryCache().find({ queryKey })?.state.status === 'error'
      ? {
          retryOnMount: false,
          ...opts,
        }
      : opts;
  }

  function useQuery(
    path: readonly string[],
    input: unknown,
    opts?: UseTRPCQueryOptions<unknown, unknown, TError>,
  ): UseTRPCQueryResult<unknown, TError> {
    const context = useContext();
    const { abortOnUnmount, client, ssrState, queryClient, prefetchQuery } =
      context;
    const queryKey = getQueryKeyInternal(path, input, 'query');

    const defaultOpts = queryClient.getQueryDefaults(queryKey);

    const isInputSkipToken = input === skipToken;

    if (
      typeof window === 'undefined' &&
      ssrState === 'prepass' &&
      opts?.trpc?.ssr !== false &&
      (opts?.enabled ?? defaultOpts?.enabled) !== false &&
      !isInputSkipToken &&
      !queryClient.getQueryCache().find({ queryKey })
    ) {
      void prefetchQuery(queryKey, opts as any);
    }
    const ssrOpts = useSSRQueryOptionsIfNeeded(queryKey, {
      ...defaultOpts,
      ...opts,
    });

    const shouldAbortOnUnmount =
      opts?.trpc?.abortOnUnmount ?? config?.abortOnUnmount ?? abortOnUnmount;

    const hook = __useQuery(
      {
        ...ssrOpts,
        queryKey: queryKey as any,
        queryFn: isInputSkipToken
          ? input
          : async (queryFunctionContext) => {
              const actualOpts = {
                ...ssrOpts,
                trpc: {
                  ...ssrOpts?.trpc,
                  ...(shouldAbortOnUnmount
                    ? { signal: queryFunctionContext.signal }
                    : { signal: null }),
                },
              };

              const result = await client.query(
                ...getClientArgs(queryKey, actualOpts),
              );

              if (isAsyncIterable(result)) {
                return buildQueryFromAsyncIterable(
                  result,
                  queryClient,
                  queryKey,
                );
              }
              return result;
            },
      },
      queryClient,
    ) as UseTRPCQueryResult<unknown, TError>;

    hook.trpc = useHookResult({
      path,
    });

    return hook;
  }

  function usePrefetchQuery(
    path: string[],
    input: unknown,
    opts?: UseTRPCPrefetchQueryOptions<unknown, unknown, TError>,
  ): void {
    const context = useContext();
    const queryKey = getQueryKeyInternal(path, input, 'query');

    const isInputSkipToken = input === skipToken;

    const shouldAbortOnUnmount =
      opts?.trpc?.abortOnUnmount ??
      config?.abortOnUnmount ??
      context.abortOnUnmount;

    _usePrefetchQuery({
      ...opts,
      queryKey: queryKey as any,
      queryFn: isInputSkipToken
        ? input
        : (queryFunctionContext) => {
            const actualOpts = {
              trpc: {
                ...opts?.trpc,
                ...(shouldAbortOnUnmount
                  ? { signal: queryFunctionContext.signal }
                  : {}),
              },
            };

            return context.client.query(...getClientArgs(queryKey, actualOpts));
          },
    });
  }

  function useSuspenseQuery(
    path: readonly string[],
    input: unknown,
    opts?: UseTRPCSuspenseQueryOptions<unknown, unknown, TError>,
  ): UseTRPCSuspenseQueryResult<unknown, TError> {
    const context = useContext();
    const queryKey = getQueryKeyInternal(path, input, 'query');

    const shouldAbortOnUnmount =
      opts?.trpc?.abortOnUnmount ??
      config?.abortOnUnmount ??
      context.abortOnUnmount;

    const hook = __useSuspenseQuery(
      {
        ...opts,
        queryKey: queryKey as any,
        queryFn: (queryFunctionContext) => {
          const actualOpts = {
            ...opts,
            trpc: {
              ...opts?.trpc,
              ...(shouldAbortOnUnmount
                ? { signal: queryFunctionContext.signal }
                : { signal: null }),
            },
          };

          return context.client.query(...getClientArgs(queryKey, actualOpts));
        },
      },
      context.queryClient,
    ) as UseTRPCQueryResult<unknown, TError>;

    hook.trpc = useHookResult({
      path,
    });

    return [hook.data, hook as any];
  }

  function useMutation(
    path: readonly string[],
    opts?: UseTRPCMutationOptions<unknown, TError, unknown, unknown>,
  ): UseTRPCMutationResult<unknown, TError, unknown, unknown> {
    const { client, queryClient } = useContext();

    const mutationKey = getMutationKeyInternal(path);

    const defaultOpts = queryClient.defaultMutationOptions(
      queryClient.getMutationDefaults(mutationKey),
    );

    const hook = __useMutation(
      {
        ...opts,
        mutationKey: mutationKey,
        mutationFn: (input) => {
          return client.mutation(...getClientArgs([path, { input }], opts));
        },
        onSuccess(...args) {
          const originalFn = () =>
            opts?.onSuccess?.(...args) ?? defaultOpts?.onSuccess?.(...args);

          return mutationSuccessOverride({
            originalFn,
            queryClient,
            meta: opts?.meta ?? defaultOpts?.meta ?? {},
          });
        },
      },
      queryClient,
    ) as UseTRPCMutationResult<unknown, TError, unknown, unknown>;

    hook.trpc = useHookResult({
      path,
    });

    return hook;
  }
  const initialStateIdle: Omit<TRPCSubscriptionIdleResult<unknown>, 'reset'> = {
    data: undefined,
    error: null,
    status: 'idle',
  };

  const initialStateConnecting: Omit<
    TRPCSubscriptionConnectingResult<unknown, TError>,
    'reset'
  > = {
    data: undefined,
    error: null,
    status: 'connecting',
  };

  /* istanbul ignore next -- @preserve */
  function useSubscription(
    path: readonly string[],
    input: unknown,
    opts: UseTRPCSubscriptionOptions<unknown, TError>,
  ) {
    const enabled = opts?.enabled ?? input !== skipToken;
    const queryKey = hashKey(getQueryKeyInternal(path, input, 'any'));
    const { client } = useContext();

    const optsRef = React.useRef<typeof opts>(opts);
    React.useEffect(() => {
      optsRef.current = opts;
    });

    type $Result = TRPCSubscriptionResult<unknown, TError>;

    const [trackedProps] = React.useState(new Set<keyof $Result>([]));

    const addTrackedProp = React.useCallback(
      (key: keyof $Result) => {
        trackedProps.add(key);
      },
      [trackedProps],
    );

    const currentSubscriptionRef = React.useRef<Unsubscribable>(null);

    const updateState = React.useCallback(
      (callback: (prevState: $Result) => $Result) => {
        const prev = resultRef.current;
        const next = (resultRef.current = callback(prev));

        let shouldUpdate = false;
        for (const key of trackedProps) {
          if (prev[key] !== next[key]) {
            shouldUpdate = true;
            break;
          }
        }
        if (shouldUpdate) {
          setState(trackResult(next, addTrackedProp));
        }
      },
      [addTrackedProp, trackedProps],
    );

    const reset = React.useCallback((): void => {
      // unsubscribe from the previous subscription
      currentSubscriptionRef.current?.unsubscribe();

      if (!enabled) {
        updateState(() => ({ ...initialStateIdle, reset }));
        return;
      }
      updateState(() => ({ ...initialStateConnecting, reset }));
      const subscription = client.subscription(
        path.join('.'),
        input ?? undefined,
        {
          onStarted: () => {
            optsRef.current.onStarted?.();
            updateState((prev) => ({
              ...prev,
              status: 'pending',
              error: null,
            }));
          },
          onData: (data) => {
            optsRef.current.onData?.(data);
            updateState((prev) => ({
              ...prev,
              status: 'pending',
              data,
              error: null,
            }));
          },
          onError: (error) => {
            optsRef.current.onError?.(error);
            updateState((prev) => ({
              ...prev,
              status: 'error',
              error,
            }));
          },
          onConnectionStateChange: (result) => {
            updateState((prev) => {
              switch (result.state) {
                case 'idle':
                  return {
                    ...prev,
                    status: result.state,
                    error: null,
                    data: undefined,
                  };
                case 'connecting':
                  return {
                    ...prev,
                    error: result.error,
                    status: result.state,
                  };

                case 'pending':
                  // handled when data is / onStarted
                  return prev;
              }
            });
          },
          onComplete: () => {
            optsRef.current.onComplete?.();

            // In the case of WebSockets, the connection might not be idle so `onConnectionStateChange` will not be called until the connection is closed.
            // In this case, we need to set the state to idle manually.
            updateState((prev) => ({
              ...prev,
              status: 'idle',
              error: null,
              data: undefined,
            }));

            // (We might want to add a `connectionState` to the state to track the connection state separately)
          },
        },
      );

      currentSubscriptionRef.current = subscription;

      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [client, queryKey, enabled, updateState]);
    React.useEffect(() => {
      reset();

      return () => {
        currentSubscriptionRef.current?.unsubscribe();
      };
    }, [reset]);

    const resultRef = React.useRef<$Result>(
      enabled
        ? { ...initialStateConnecting, reset }
        : { ...initialStateIdle, reset },
    );

    const [state, setState] = React.useState<$Result>(
      trackResult(resultRef.current, addTrackedProp),
    );

    return state;
  }

  function useInfiniteQuery(
    path: readonly string[],
    input: unknown,
    opts: UseTRPCInfiniteQueryOptions<unknown, unknown, TError>,
  ): UseTRPCInfiniteQueryResult<unknown, TError, unknown> {
    const {
      client,
      ssrState,
      prefetchInfiniteQuery,
      queryClient,
      abortOnUnmount,
    } = useContext();
    const queryKey = getQueryKeyInternal(path, input, 'infinite');

    const defaultOpts = queryClient.getQueryDefaults(queryKey);

    const isInputSkipToken = input === skipToken;

    if (
      typeof window === 'undefined' &&
      ssrState === 'prepass' &&
      opts?.trpc?.ssr !== false &&
      (opts?.enabled ?? defaultOpts?.enabled) !== false &&
      !isInputSkipToken &&
      !queryClient.getQueryCache().find({ queryKey })
    ) {
      void prefetchInfiniteQuery(queryKey, { ...defaultOpts, ...opts } as any);
    }

    const ssrOpts = useSSRQueryOptionsIfNeeded(queryKey, {
      ...defaultOpts,
      ...opts,
    });

    // request option should take priority over global
    const shouldAbortOnUnmount = opts?.trpc?.abortOnUnmount ?? abortOnUnmount;

    const hook = __useInfiniteQuery(
      {
        ...ssrOpts,
        initialPageParam: opts.initialCursor ?? null,
        persister: opts.persister,
        queryKey: queryKey as any,
        queryFn: isInputSkipToken
          ? input
          : (queryFunctionContext) => {
              const actualOpts = {
                ...ssrOpts,
                trpc: {
                  ...ssrOpts?.trpc,
                  ...(shouldAbortOnUnmount
                    ? { signal: queryFunctionContext.signal }
                    : { signal: null }),
                },
              };

              return client.query(
                ...getClientArgs(queryKey, actualOpts, {
                  pageParam:
                    queryFunctionContext.pageParam ?? opts.initialCursor,
                  direction: queryFunctionContext.direction,
                }),
              );
            },
      },
      queryClient,
    ) as UseTRPCInfiniteQueryResult<unknown, TError, unknown>;

    hook.trpc = useHookResult({
      path,
    });
    return hook;
  }

  function usePrefetchInfiniteQuery(
    path: string[],
    input: unknown,
    opts: UseTRPCPrefetchInfiniteQueryOptions<unknown, unknown, TError>,
  ): void {
    const context = useContext();
    const queryKey = getQueryKeyInternal(path, input, 'infinite');

    const defaultOpts = context.queryClient.getQueryDefaults(queryKey);

    const isInputSkipToken = input === skipToken;

    const ssrOpts = useSSRQueryOptionsIfNeeded(queryKey, {
      ...defaultOpts,
      ...opts,
    });

    // request option should take priority over global
    const shouldAbortOnUnmount =
      opts?.trpc?.abortOnUnmount ?? context.abortOnUnmount;

    __usePrefetchInfiniteQuery({
      ...opts,
      initialPageParam: opts.initialCursor ?? null,
      queryKey,
      queryFn: isInputSkipToken
        ? input
        : (queryFunctionContext) => {
            const actualOpts = {
              ...ssrOpts,
              trpc: {
                ...ssrOpts?.trpc,
                ...(shouldAbortOnUnmount
                  ? { signal: queryFunctionContext.signal }
                  : {}),
              },
            };

            return context.client.query(
              ...getClientArgs(queryKey, actualOpts, {
                pageParam: queryFunctionContext.pageParam ?? opts.initialCursor,
                direction: queryFunctionContext.direction,
              }),
            );
          },
    });
  }

  function useSuspenseInfiniteQuery(
    path: readonly string[],
    input: unknown,
    opts: UseTRPCSuspenseInfiniteQueryOptions<unknown, unknown, TError>,
  ): UseTRPCSuspenseInfiniteQueryResult<unknown, TError, unknown> {
    const context = useContext();
    const queryKey = getQueryKeyInternal(path, input, 'infinite');

    const defaultOpts = context.queryClient.getQueryDefaults(queryKey);

    const ssrOpts = useSSRQueryOptionsIfNeeded(queryKey, {
      ...defaultOpts,
      ...opts,
    });

    // request option should take priority over global
    const shouldAbortOnUnmount =
      opts?.trpc?.abortOnUnmount ?? context.abortOnUnmount;

    const hook = __useSuspenseInfiniteQuery(
      {
        ...opts,
        initialPageParam: opts.initialCursor ?? null,
        queryKey,
        queryFn: (queryFunctionContext) => {
          const actualOpts = {
            ...ssrOpts,
            trpc: {
              ...ssrOpts?.trpc,
              ...(shouldAbortOnUnmount
                ? { signal: queryFunctionContext.signal }
                : {}),
            },
          };

          return context.client.query(
            ...getClientArgs(queryKey, actualOpts, {
              pageParam: queryFunctionContext.pageParam ?? opts.initialCursor,
              direction: queryFunctionContext.direction,
            }),
          );
        },
      },
      context.queryClient,
    ) as UseTRPCInfiniteQueryResult<unknown, TError, unknown>;

    hook.trpc = useHookResult({
      path,
    });

    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    return [hook.data!, hook as any];
  }

  const useQueries: TRPCUseQueries<TRouter> = (queriesCallback, options) => {
    const { ssrState, queryClient, prefetchQuery, client } = useContext();

    const proxy = createUseQueries(client);

    const queries = queriesCallback(proxy);

    if (typeof window === 'undefined' && ssrState === 'prepass') {
      for (const query of queries) {
        const queryOption = query as TRPCQueryOptions<any, any>;
        if (
          queryOption.trpc?.ssr !== false &&
          !queryClient.getQueryCache().find({ queryKey: queryOption.queryKey })
        ) {
          void prefetchQuery(queryOption.queryKey, queryOption as any);
        }
      }
    }

    return __useQueries(
      {
        queries: queries.map((query) => ({
          ...query,
          queryKey: (query as TRPCQueryOptions<any, any>).queryKey,
        })),
        combine: options?.combine as any,
      },
      queryClient,
    );
  };

  const useSuspenseQueries: TRPCUseSuspenseQueries<TRouter> = (
    queriesCallback,
  ) => {
    const { queryClient, client } = useContext();

    const proxy = createUseQueries(client);

    const queries = queriesCallback(proxy);

    const hook = __useSuspenseQueries(
      {
        queries: queries.map((query) => ({
          ...query,
          queryFn: query.queryFn,
          queryKey: (query as TRPCQueryOptions<any, any>).queryKey,
        })),
      },
      queryClient,
    );

    return [hook.map((h) => h.data), hook] as any;
  };

  return {
    Provider: TRPCProvider,
    createClient,
    useContext,
    useUtils: useContext,
    useQuery,
    usePrefetchQuery,
    useSuspenseQuery,
    useQueries,
    useSuspenseQueries,
    useMutation,
    useSubscription,
    useInfiniteQuery,
    usePrefetchInfiniteQuery,
    useSuspenseInfiniteQuery,
  };
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createRootHooks<
  TRouter extends AnyRouter,
  TSSRContext = unknown,
>(config?: CreateTRPCReactOptions<TRouter>) {
  const mutationSuccessOverride: UseMutationOverride['onSuccess'] =
    config?.overrides?.useMutation?.onSuccess ??
    ((options) => options.originalFn());

  type TError = TRPCClientErrorLike<TRouter>;

  type ProviderContext = TRPCContextState<TRouter, TSSRContext>;

  const Context = (config?.context ??
    TRPCContext) as React.Context<ProviderContext>;

  const createClient = createTRPCClient<TRouter>;

  const TRPCProvider: TRPCProvider<TRouter, TSSRContext> = (props) => {
    const { abortOnUnmount = false, queryClient, ssrContext } = props;
    const [ssrState, setSSRState] = React.useState<SSRState>(
      props.ssrState ?? false,
    );

    const client: TRPCUntypedClient<TRouter> =
      props.client instanceof TRPCUntypedClient
        ? props.client
        : getUntypedClient(props.client);

    const fns = React.useMemo(
      () =>
        createUtilityFunctions({
          client,
          queryClient,
        }),
      [client, queryClient],
    );

    const contextValue = React.useMemo<ProviderContext>(
      () => ({
        abortOnUnmount,
        queryClient,
        client,
        ssrContext: ssrContext ?? null,
        ssrState,
        ...fns,
      }),
      [abortOnUnmount, client, fns, queryClient, ssrContext, ssrState],
    );

    React.useEffect(() => {
      // Only updating state to `mounted` if we are using SSR.
      // This makes it so we don't have an unnecessary re-render when opting out of SSR.
      setSSRState((state) => (state ? 'mounted' : false));
    }, []);
    return (
      <Context.Provider value={contextValue}>{props.children}</Context.Provider>
    );
  };

  function useContext() {
    const context = React.useContext(Context);

    if (!context) {
      throw new Error(
        'Unable to find tRPC Context. Did you forget to wrap your App inside `withTRPC` HoC?',
      );
    }
    return context;
  }

  /**
   * Hack to make sure errors return `status`='error` when doing SSR
   * @see https://github.com/trpc/trpc/pull/1645
   */
  function useSSRQueryOptionsIfNeeded<
    TOptions extends { retryOnMount?: boolean } | undefined,
  >(queryKey: TRPCQueryKey, opts: TOptions): TOptions {
    const { queryClient, ssrState } = useContext();
    return ssrState &&
      ssrState !== 'mounted' &&
      queryClient.getQueryCache().find({ queryKey })?.state.status === 'error'
      ? {
          retryOnMount: false,
          ...opts,
        }
      : opts;
  }

  function useQuery(
    path: readonly string[],
    input: unknown,
    opts?: UseTRPCQueryOptions<unknown, unknown, TError>,
  ): UseTRPCQueryResult<unknown, TError> {
    const context = useContext();
    const { abortOnUnmount, client, ssrState, queryClient, prefetchQuery } =
      context;
    const queryKey = getQueryKeyInternal(path, input, 'query');

    const defaultOpts = queryClient.getQueryDefaults(queryKey);

    const isInputSkipToken = input === skipToken;

    if (
      typeof window === 'undefined' &&
      ssrState === 'prepass' &&
      opts?.trpc?.ssr !== false &&
      (opts?.enabled ?? defaultOpts?.enabled) !== false &&
      !isInputSkipToken &&
      !queryClient.getQueryCache().find({ queryKey })
    ) {
      void prefetchQuery(queryKey, opts as any);
    }
    const ssrOpts = useSSRQueryOptionsIfNeeded(queryKey, {
      ...defaultOpts,
      ...opts,
    });

    const shouldAbortOnUnmount =
      opts?.trpc?.abortOnUnmount ?? config?.abortOnUnmount ?? abortOnUnmount;

    const hook = __useQuery(
      {
        ...ssrOpts,
        queryKey: queryKey as any,
        queryFn: isInputSkipToken
          ? input
          : async (queryFunctionContext) => {
              const actualOpts = {
                ...ssrOpts,
                trpc: {
                  ...ssrOpts?.trpc,
                  ...(shouldAbortOnUnmount
                    ? { signal: queryFunctionContext.signal }
                    : { signal: null }),
                },
              };

              const result = await client.query(
                ...getClientArgs(queryKey, actualOpts),
              );

              if (isAsyncIterable(result)) {
                return buildQueryFromAsyncIterable(
                  result,
                  queryClient,
                  queryKey,
                );
              }
              return result;
            },
      },
      queryClient,
    ) as UseTRPCQueryResult<unknown, TError>;

    hook.trpc = useHookResult({
      path,
    });

    return hook;
  }

  function usePrefetchQuery(
    path: string[],
    input: unknown,
    opts?: UseTRPCPrefetchQueryOptions<unknown, unknown, TError>,
  ): void {
    const context = useContext();
    const queryKey = getQueryKeyInternal(path, input, 'query');

    const isInputSkipToken = input === skipToken;

    const shouldAbortOnUnmount =
      opts?.trpc?.abortOnUnmount ??
      config?.abortOnUnmount ??
      context.abortOnUnmount;

    _usePrefetchQuery({
      ...opts,
      queryKey: queryKey as any,
      queryFn: isInputSkipToken
        ? input
        : (queryFunctionContext) => {
            const actualOpts = {
              trpc: {
                ...opts?.trpc,
                ...(shouldAbortOnUnmount
                  ? { signal: queryFunctionContext.signal }
                  : {}),
              },
            };

            return context.client.query(...getClientArgs(queryKey, actualOpts));
          },
    });
  }

  function useSuspenseQuery(
    path: readonly string[],
    input: unknown,
    opts?: UseTRPCSuspenseQueryOptions<unknown, unknown, TError>,
  ): UseTRPCSuspenseQueryResult<unknown, TError> {
    const context = useContext();
    const queryKey = getQueryKeyInternal(path, input, 'query');

    const shouldAbortOnUnmount =
      opts?.trpc?.abortOnUnmount ??
      config?.abortOnUnmount ??
      context.abortOnUnmount;

    const hook = __useSuspenseQuery(
      {
        ...opts,
        queryKey: queryKey as any,
        queryFn: (queryFunctionContext) => {
          const actualOpts = {
            ...opts,
            trpc: {
              ...opts?.trpc,
              ...(shouldAbortOnUnmount
                ? { signal: queryFunctionContext.signal }
                : { signal: null }),
            },
          };

          return context.client.query(...getClientArgs(queryKey, actualOpts));
        },
      },
      context.queryClient,
    ) as UseTRPCQueryResult<unknown, TError>;

    hook.trpc = useHookResult({
      path,
    });

    return [hook.data, hook as any];
  }

  function useMutation(
    path: readonly string[],
    opts?: UseTRPCMutationOptions<unknown, TError, unknown, unknown>,
  ): UseTRPCMutationResult<unknown, TError, unknown, unknown> {
    const { client, queryClient } = useContext();

    const mutationKey = getMutationKeyInternal(path);

    const defaultOpts = queryClient.defaultMutationOptions(
      queryClient.getMutationDefaults(mutationKey),
    );

    const hook = __useMutation(
      {
        ...opts,
        mutationKey: mutationKey,
        mutationFn: (input) => {
          return client.mutation(...getClientArgs([path, { input }], opts));
        },
        onSuccess(...args) {
          const originalFn = () =>
            opts?.onSuccess?.(...args) ?? defaultOpts?.onSuccess?.(...args);

          return mutationSuccessOverride({
            originalFn,
            queryClient,
            meta: opts?.meta ?? defaultOpts?.meta ?? {},
          });
        },
      },
      queryClient,
    ) as UseTRPCMutationResult<unknown, TError, unknown, unknown>;

    hook.trpc = useHookResult({
      path,
    });

    return hook;
  }
  const initialStateIdle: Omit<TRPCSubscriptionIdleResult<unknown>, 'reset'> = {
    data: undefined,
    error: null,
    status: 'idle',
  };

  const initialStateConnecting: Omit<
    TRPCSubscriptionConnectingResult<unknown, TError>,
    'reset'
  > = {
    data: undefined,
    error: null,
    status: 'connecting',
  };

  /* istanbul ignore next -- @preserve */
  function useSubscription(
    path: readonly string[],
    input: unknown,
    opts: UseTRPCSubscriptionOptions<unknown, TError>,
  ) {
    const enabled = opts?.enabled ?? input !== skipToken;
    const queryKey = hashKey(getQueryKeyInternal(path, input, 'any'));
    const { client } = useContext();

    const optsRef = React.useRef<typeof opts>(opts);
    React.useEffect(() => {
      optsRef.current = opts;
    });

    type $Result = TRPCSubscriptionResult<unknown, TError>;

    const [trackedProps] = React.useState(new Set<keyof $Result>([]));

    const addTrackedProp = React.useCallback(
      (key: keyof $Result) => {
        trackedProps.add(key);
      },
      [trackedProps],
    );

    const currentSubscriptionRef = React.useRef<Unsubscribable>(null);

    const updateState = React.useCallback(
      (callback: (prevState: $Result) => $Result) => {
        const prev = resultRef.current;
        const next = (resultRef.current = callback(prev));

        let shouldUpdate = false;
        for (const key of trackedProps) {
          if (prev[key] !== next[key]) {
            shouldUpdate = true;
            break;
          }
        }
        if (shouldUpdate) {
          setState(trackResult(next, addTrackedProp));
        }
      },
      [addTrackedProp, trackedProps],
    );

    const reset = React.useCallback((): void => {
      // unsubscribe from the previous subscription
      currentSubscriptionRef.current?.unsubscribe();

      if (!enabled) {
        updateState(() => ({ ...initialStateIdle, reset }));
        return;
      }
      updateState(() => ({ ...initialStateConnecting, reset }));
      const subscription = client.subscription(
        path.join('.'),
        input ?? undefined,
        {
          context: optsRef.current?.trpc?.context,
          onStarted: () => {
            optsRef.current.onStarted?.();
            updateState((prev) => ({
              ...prev,
              status: 'pending',
              error: null,
            }));
          },
          onData: (data) => {
            optsRef.current.onData?.(data);
            updateState((prev) => ({
              ...prev,
              status: 'pending',
              data,
              error: null,
            }));
          },
          onError: (error) => {
            optsRef.current.onError?.(error);
            updateState((prev) => ({
              ...prev,
              status: 'error',
              error,
            }));
          },
          onConnectionStateChange: (result) => {
            updateState((prev) => {
              switch (result.state) {
                case 'idle':
                  return {
                    ...prev,
                    status: result.state,
                    error: null,
                    data: undefined,
                  };
                case 'connecting':
                  return {
                    ...prev,
                    error: result.error,
                    status: result.state,
                  };

                case 'pending':
                  // handled when data is / onStarted
                  return prev;
              }
            });
          },
          onComplete: () => {
            optsRef.current.onComplete?.();

            // In the case of WebSockets, the connection might not be idle so `onConnectionStateChange` will not be called until the connection is closed.
            // In this case, we need to set the state to idle manually.
            updateState((prev) => ({
              ...prev,
              status: 'idle',
              error: null,
              data: undefined,
            }));

            // (We might want to add a `connectionState` to the state to track the connection state separately)
          },
        },
      );

      currentSubscriptionRef.current = subscription;

      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [client, queryKey, enabled, updateState]);
    React.useEffect(() => {
      reset();

      return () => {
        currentSubscriptionRef.current?.unsubscribe();
      };
    }, [reset]);

    const resultRef = React.useRef<$Result>(
      enabled
        ? { ...initialStateConnecting, reset }
        : { ...initialStateIdle, reset },
    );

    const [state, setState] = React.useState<$Result>(
      trackResult(resultRef.current, addTrackedProp),
    );

    return state;
  }

  function useInfiniteQuery(
    path: readonly string[],
    input: unknown,
    opts: UseTRPCInfiniteQueryOptions<unknown, unknown, TError>,
  ): UseTRPCInfiniteQueryResult<unknown, TError, unknown> {
    const {
      client,
      ssrState,
      prefetchInfiniteQuery,
      queryClient,
      abortOnUnmount,
    } = useContext();
    const queryKey = getQueryKeyInternal(path, input, 'infinite');

    const defaultOpts = queryClient.getQueryDefaults(queryKey);

    const isInputSkipToken = input === skipToken;

    if (
      typeof window === 'undefined' &&
      ssrState === 'prepass' &&
      opts?.trpc?.ssr !== false &&
      (opts?.enabled ?? defaultOpts?.enabled) !== false &&
      !isInputSkipToken &&
      !queryClient.getQueryCache().find({ queryKey })
    ) {
      void prefetchInfiniteQuery(queryKey, { ...defaultOpts, ...opts } as any);
    }

    const ssrOpts = useSSRQueryOptionsIfNeeded(queryKey, {
      ...defaultOpts,
      ...opts,
    });

    // request option should take priority over global
    const shouldAbortOnUnmount = opts?.trpc?.abortOnUnmount ?? abortOnUnmount;

    const hook = __useInfiniteQuery(
      {
        ...ssrOpts,
        initialPageParam: opts.initialCursor ?? null,
        persister: opts.persister,
        queryKey: queryKey as any,
        queryFn: isInputSkipToken
          ? input
          : (queryFunctionContext) => {
              const actualOpts = {
                ...ssrOpts,
                trpc: {
                  ...ssrOpts?.trpc,
                  ...(shouldAbortOnUnmount
                    ? { signal: queryFunctionContext.signal }
                    : { signal: null }),
                },
              };

              return client.query(
                ...getClientArgs(queryKey, actualOpts, {
                  pageParam:
                    queryFunctionContext.pageParam ?? opts.initialCursor,
                  direction: queryFunctionContext.direction,
                }),
              );
            },
      },
      queryClient,
    ) as UseTRPCInfiniteQueryResult<unknown, TError, unknown>;

    hook.trpc = useHookResult({
      path,
    });
    return hook;
  }

  function usePrefetchInfiniteQuery(
    path: string[],
    input: unknown,
    opts: UseTRPCPrefetchInfiniteQueryOptions<unknown, unknown, TError>,
  ): void {
    const context = useContext();
    const queryKey = getQueryKeyInternal(path, input, 'infinite');

    const defaultOpts = context.queryClient.getQueryDefaults(queryKey);

    const isInputSkipToken = input === skipToken;

    const ssrOpts = useSSRQueryOptionsIfNeeded(queryKey, {
      ...defaultOpts,
      ...opts,
    });

    // request option should take priority over global
    const shouldAbortOnUnmount =
      opts?.trpc?.abortOnUnmount ?? context.abortOnUnmount;

    __usePrefetchInfiniteQuery({
      ...opts,
      initialPageParam: opts.initialCursor ?? null,
      queryKey,
      queryFn: isInputSkipToken
        ? input
        : (queryFunctionContext) => {
            const actualOpts = {
              ...ssrOpts,
              trpc: {
                ...ssrOpts?.trpc,
                ...(shouldAbortOnUnmount
                  ? { signal: queryFunctionContext.signal }
                  : {}),
              },
            };

            return context.client.query(
              ...getClientArgs(queryKey, actualOpts, {
                pageParam: queryFunctionContext.pageParam ?? opts.initialCursor,
                direction: queryFunctionContext.direction,
              }),
            );
          },
    });
  }

  function useSuspenseInfiniteQuery(
    path: readonly string[],
    input: unknown,
    opts: UseTRPCSuspenseInfiniteQueryOptions<unknown, unknown, TError>,
  ): UseTRPCSuspenseInfiniteQueryResult<unknown, TError, unknown> {
    const context = useContext();
    const queryKey = getQueryKeyInternal(path, input, 'infinite');

    const defaultOpts = context.queryClient.getQueryDefaults(queryKey);

    const ssrOpts = useSSRQueryOptionsIfNeeded(queryKey, {
      ...defaultOpts,
      ...opts,
    });

    // request option should take priority over global
    const shouldAbortOnUnmount =
      opts?.trpc?.abortOnUnmount ?? context.abortOnUnmount;

    const hook = __useSuspenseInfiniteQuery(
      {
        ...opts,
        initialPageParam: opts.initialCursor ?? null,
        queryKey,
        queryFn: (queryFunctionContext) => {
          const actualOpts = {
            ...ssrOpts,
            trpc: {
              ...ssrOpts?.trpc,
              ...(shouldAbortOnUnmount
                ? { signal: queryFunctionContext.signal }
                : {}),
            },
          };

          return context.client.query(
            ...getClientArgs(queryKey, actualOpts, {
              pageParam: queryFunctionContext.pageParam ?? opts.initialCursor,
              direction: queryFunctionContext.direction,
            }),
          );
        },
      },
      context.queryClient,
    ) as UseTRPCInfiniteQueryResult<unknown, TError, unknown>;

    hook.trpc = useHookResult({
      path,
    });

    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    return [hook.data!, hook as any];
  }

  const useQueries: TRPCUseQueries<TRouter> = (queriesCallback, options) => {
    const { ssrState, queryClient, prefetchQuery, client } = useContext();

    const proxy = createUseQueries(client);

    const queries = queriesCallback(proxy);

    if (typeof window === 'undefined' && ssrState === 'prepass') {
      for (const query of queries) {
        const queryOption = query as TRPCQueryOptions<any, any>;
        if (
          queryOption.trpc?.ssr !== false &&
          !queryClient.getQueryCache().find({ queryKey: queryOption.queryKey })
        ) {
          void prefetchQuery(queryOption.queryKey, queryOption as any);
        }
      }
    }

    return __useQueries(
      {
        queries: queries.map((query) => ({
          ...query,
          queryKey: (query as TRPCQueryOptions<any, any>).queryKey,
        })),
        combine: options?.combine as any,
      },
      queryClient,
    );
  };

  const useSuspenseQueries: TRPCUseSuspenseQueries<TRouter> = (
    queriesCallback,
  ) => {
    const { queryClient, client } = useContext();

    const proxy = createUseQueries(client);

    const queries = queriesCallback(proxy);

    const hook = __useSuspenseQueries(
      {
        queries: queries.map((query) => ({
          ...query,
          queryFn: query.queryFn,
          queryKey: (query as TRPCQueryOptions<any, any>).queryKey,
        })),
      },
      queryClient,
    );

    return [hook.map((h) => h.data), hook] as any;
  };

  return {
    Provider: TRPCProvider,
    createClient,
    useContext,
    useUtils: useContext,
    useQuery,
    usePrefetchQuery,
    useSuspenseQuery,
    useQueries,
    useSuspenseQueries,
    useMutation,
    useSubscription,
    useInfiniteQuery,
    usePrefetchInfiniteQuery,
    useSuspenseInfiniteQuery,
  };
}
```


#### 📄 檔案: `packages/react-query/src/shared/hooks/types.ts`
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

### 🔹 Commit #18: `ea879a7a`
- **完整 Hash**: `ea879a7acfa46564e80d6b181e1614ed18d1eed4`
- **說明 (Ground Truth)**: fix(server): preserve lazy routes when composing routers (#7667)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/src/unstable-core-do-not-import/router.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:33, E:28, A:0) ➔ After(N:34, E:31, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 4, -Edges: 1, ΔFuncs: 5, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `getRouterInput` (FUNCTION_DEF)
  • + [新增呼叫邊] `getRouterInput` ──[CALLS [guarded]]──> `emptyObject (External/Unresolved)`
  • + [新增呼叫邊] `createLazyLoader` ──[CALLS]──> `getRouterInput`
  • + [新增呼叫邊] `step` ──[CALLS [guard: (isRouter(item))]]──> `getRouterInput`
  • + [新增呼叫邊] `mergeRouters` ──[CALLS]──> `getRouterInput`
  • - [移除呼叫邊] `createLazyLoader` ──[CALLS]──> `createLazyLoader`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `createRouterFactory()`
- **變更前簽章 (Before)**: `function createRouterFactory<TRoot extends AnyRootTypes>(
  config: RootConfig<TRoot>,
)` (L249~L359)
- **變更後簽章 (After)**: `function createRouterFactory<TRoot extends AnyRootTypes>(
  config: RootConfig<TRoot>,
)` (L271~L368)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createRouterFactory<TRoot extends AnyRootTypes>(
  config: RootConfig<TRoot>,
) {
  function createRouterInner<TInput extends CreateRouterOptions>(
    input: TInput,
  ): BuiltRouter<TRoot, DecorateCreateRouterOptions<TInput>> {
    const reservedWordsUsed = new Set(
      Object.keys(input).filter((v) => reservedWords.includes(v)),
    );
    if (reservedWordsUsed.size > 0) {
      throw new Error(
        'Reserved words used in `router({})` call: ' +
          Array.from(reservedWordsUsed).join(', '),
      );
    }

    const procedures: Record<string, AnyProcedure> = emptyObject();
    const lazy: Record<string, LazyLoader<AnyRouter>> = emptyObject();

    function createLazyLoader(opts: {
      ref: Lazy<AnyRouter>;
      path: readonly string[];
      key: string;
      aggregate: RouterRecord;
    }): LazyLoader<AnyRouter> {
      return {
        ref: opts.ref,
        load: once(async () => {
          const router = await opts.ref();
          const lazyPath = [...opts.path, opts.key];
          const lazyKey = lazyPath.join('.');

          opts.aggregate[opts.key] = step(router._def.record, lazyPath);

          delete lazy[lazyKey];

          // add lazy loaders for nested routers
          for (const [nestedKey, nestedItem] of Object.entries(
            router._def.lazy,
          )) {
            const nestedRouterKey = [...lazyPath, nestedKey].join('.');

            // console.log('adding lazy', nestedRouterKey);
            lazy[nestedRouterKey] = createLazyLoader({
              ref: nestedItem.ref,
              path: lazyPath,
              key: nestedKey,
              aggregate: opts.aggregate[opts.key] as RouterRecord,
            });
          }
        }),
      };
    }

    function step(from: CreateRouterOptions, path: readonly string[] = []) {
      const aggregate: RouterRecord = emptyObject();
      for (const [key, item] of Object.entries(from ?? {})) {
        if (isLazy(item)) {
          lazy[[...path, key].join('.')] = createLazyLoader({
            path,
            ref: item,
            key,
            aggregate,
          });
          continue;
        }
        if (isRouter(item)) {
          aggregate[key] = step(item._def.record, [...path, key]);
          continue;
        }
        if (!isProcedure(item)) {
          // RouterRecord
          aggregate[key] = step(item, [...path, key]);
          continue;
        }

        const newPath = [...path, key].join('.');

        if (procedures[newPath]) {
          throw new Error(`Duplicate key: ${newPath}`);
        }

        procedures[newPath] = item;
        aggregate[key] = item;
      }

      return aggregate;
    }
    const record = step(input);

    const _def: AnyRouter['_def'] = {
      _config: config,
      router: true,
      procedures,
      lazy,
      ...emptyRouter,
      record,
    };

    const router: BuiltRouter<TRoot, {}> = {
      ...(record as {}),
      _def,
      createCaller: createCallerFactory<TRoot>()({
        _def,
      }),
    };
    return router as BuiltRouter<TRoot, DecorateCreateRouterOptions<TInput>>;
  }

  return createRouterInner;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createRouterFactory<TRoot extends AnyRootTypes>(
  config: RootConfig<TRoot>,
) {
  function createRouterInner<TInput extends CreateRouterOptions>(
    input: TInput,
  ): BuiltRouter<TRoot, DecorateCreateRouterOptions<TInput>> {
    const reservedWordsUsed = new Set(
      Object.keys(input).filter((v) => reservedWords.includes(v)),
    );
    if (reservedWordsUsed.size > 0) {
      throw new Error(
        'Reserved words used in `router({})` call: ' +
          Array.from(reservedWordsUsed).join(', '),
      );
    }

    const procedures: Record<string, AnyProcedure> = emptyObject();
    const lazy: Record<string, LazyLoader<AnyRouter>> = emptyObject();

    function createLazyLoader(opts: {
      ref: Lazy<AnyRouter>;
      path: readonly string[];
      key: string;
      aggregate: RouterRecord;
    }): LazyLoader<AnyRouter> {
      return {
        ref: opts.ref,
        path: opts.path,
        key: opts.key,
        load: once(async () => {
          const router = await opts.ref();
          const lazyPath = [...opts.path, opts.key];
          const lazyKey = lazyPath.join('.');

          opts.aggregate[opts.key] = step(getRouterInput(router), lazyPath);

          delete lazy[lazyKey];
        }),
      };
    }

    function step(from: CreateRouterOptions, path: readonly string[] = []) {
      const aggregate: RouterRecord = emptyObject();
      for (const [key, item] of Object.entries(from ?? {})) {
        if (isLazy(item)) {
          lazy[[...path, key].join('.')] = createLazyLoader({
            path,
            ref: item,
            key,
            aggregate,
          });
          continue;
        }
        if (isRouter(item)) {
          aggregate[key] = step(getRouterInput(item), [...path, key]);
          continue;
        }
        if (!isProcedure(item)) {
          // RouterRecord
          aggregate[key] = step(item, [...path, key]);
          continue;
        }

        const newPath = [...path, key].join('.');

        if (procedures[newPath]) {
          throw new Error(`Duplicate key: ${newPath}`);
        }

        procedures[newPath] = item;
        aggregate[key] = item;
      }

      return aggregate;
    }
    const record = step(input);

    const _def: AnyRouter['_def'] = {
      _config: config,
      router: true,
      procedures,
      lazy,
      ...emptyRouter,
      record,
    };

    const router: BuiltRouter<TRoot, {}> = {
      ...(record as {}),
      _def,
      createCaller: createCallerFactory<TRoot>()({
        _def,
      }),
    };
    return router as BuiltRouter<TRoot, DecorateCreateRouterOptions<TInput>>;
  }

  return createRouterInner;
}
```

### 🔹 函式: `mergeRouters()`
- **變更前簽章 (Before)**: `function mergeRouters<TRouters extends AnyRouter[]>(
  ...routerList: [...TRouters]
): MergeRouters<TRouters>` (L509~L564)
- **變更後簽章 (After)**: `function mergeRouters<TRouters extends AnyRouter[]>(
  ...routerList: [...TRouters]
): MergeRouters<TRouters>` (L518~L573)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function mergeRouters<TRouters extends AnyRouter[]>(
  ...routerList: [...TRouters]
): MergeRouters<TRouters> {
  const record = mergeWithoutOverrides(
    {},
    ...routerList.map((r) => r._def.record),
  );
  const errorFormatter = routerList.reduce(
    (currentErrorFormatter, nextRouter) => {
      if (
        nextRouter._def._config.errorFormatter &&
        nextRouter._def._config.errorFormatter !== defaultFormatter
      ) {
        if (
          currentErrorFormatter !== defaultFormatter &&
          currentErrorFormatter !== nextRouter._def._config.errorFormatter
        ) {
          throw new Error('You seem to have several error formatters');
        }
        return nextRouter._def._config.errorFormatter;
      }
      return currentErrorFormatter;
    },
    defaultFormatter,
  );

  const transformer = routerList.reduce((prev, current) => {
    if (
      current._def._config.transformer &&
      current._def._config.transformer !== defaultTransformer
    ) {
      if (
        prev !== defaultTransformer &&
        prev !== current._def._config.transformer
      ) {
        throw new Error('You seem to have several transformers');
      }
      return current._def._config.transformer;
    }
    return prev;
  }, defaultTransformer);

  const router = createRouterFactory({
    errorFormatter,
    transformer,
    isDev: routerList.every((r) => r._def._config.isDev),
    allowOutsideOfServer: routerList.every(
      (r) => r._def._config.allowOutsideOfServer,
    ),
    isServer: routerList.every((r) => r._def._config.isServer),
    $types: routerList[0]?._def._config.$types,
    sse: routerList[0]?._def._config.sse,
  })(record);

  return router as MergeRouters<TRouters>;
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function mergeRouters<TRouters extends AnyRouter[]>(
  ...routerList: [...TRouters]
): MergeRouters<TRouters> {
  const record = mergeWithoutOverrides(
    {},
    ...[...new Set(routerList)].map((r) => getRouterInput(r)),
  );
  const errorFormatter = routerList.reduce(
    (currentErrorFormatter, nextRouter) => {
      if (
        nextRouter._def._config.errorFormatter &&
        nextRouter._def._config.errorFormatter !== defaultFormatter
      ) {
        if (
          currentErrorFormatter !== defaultFormatter &&
          currentErrorFormatter !== nextRouter._def._config.errorFormatter
        ) {
          throw new Error('You seem to have several error formatters');
        }
        return nextRouter._def._config.errorFormatter;
      }
      return currentErrorFormatter;
    },
    defaultFormatter,
  );

  const transformer = routerList.reduce((prev, current) => {
    if (
      current._def._config.transformer &&
      current._def._config.transformer !== defaultTransformer
    ) {
      if (
        prev !== defaultTransformer &&
        prev !== current._def._config.transformer
      ) {
        throw new Error('You seem to have several transformers');
      }
      return current._def._config.transformer;
    }
    return prev;
  }, defaultTransformer);

  const router = createRouterFactory({
    errorFormatter,
    transformer,
    isDev: routerList.every((r) => r._def._config.isDev),
    allowOutsideOfServer: routerList.every(
      (r) => r._def._config.allowOutsideOfServer,
    ),
    isServer: routerList.every((r) => r._def._config.isServer),
    $types: routerList[0]?._def._config.$types,
    sse: routerList[0]?._def._config.sse,
  })(record);

  return router as MergeRouters<TRouters>;
}
```

### 🔹 函式: `createRouterInner()`
- **變更前簽章 (Before)**: `function createRouterInner<TInput extends CreateRouterOptions>(
    input: TInput,
  ): BuiltRouter<TRoot, DecorateCreateRouterOptions<TInput>>` (L252~L356)
- **變更後簽章 (After)**: `function createRouterInner<TInput extends CreateRouterOptions>(
    input: TInput,
  ): BuiltRouter<TRoot, DecorateCreateRouterOptions<TInput>>` (L274~L365)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createRouterInner<TInput extends CreateRouterOptions>(
    input: TInput,
  ): BuiltRouter<TRoot, DecorateCreateRouterOptions<TInput>> {
    const reservedWordsUsed = new Set(
      Object.keys(input).filter((v) => reservedWords.includes(v)),
    );
    if (reservedWordsUsed.size > 0) {
      throw new Error(
        'Reserved words used in `router({})` call: ' +
          Array.from(reservedWordsUsed).join(', '),
      );
    }

    const procedures: Record<string, AnyProcedure> = emptyObject();
    const lazy: Record<string, LazyLoader<AnyRouter>> = emptyObject();

    function createLazyLoader(opts: {
      ref: Lazy<AnyRouter>;
      path: readonly string[];
      key: string;
      aggregate: RouterRecord;
    }): LazyLoader<AnyRouter> {
      return {
        ref: opts.ref,
        load: once(async () => {
          const router = await opts.ref();
          const lazyPath = [...opts.path, opts.key];
          const lazyKey = lazyPath.join('.');

          opts.aggregate[opts.key] = step(router._def.record, lazyPath);

          delete lazy[lazyKey];

          // add lazy loaders for nested routers
          for (const [nestedKey, nestedItem] of Object.entries(
            router._def.lazy,
          )) {
            const nestedRouterKey = [...lazyPath, nestedKey].join('.');

            // console.log('adding lazy', nestedRouterKey);
            lazy[nestedRouterKey] = createLazyLoader({
              ref: nestedItem.ref,
              path: lazyPath,
              key: nestedKey,
              aggregate: opts.aggregate[opts.key] as RouterRecord,
            });
          }
        }),
      };
    }

    function step(from: CreateRouterOptions, path: readonly string[] = []) {
      const aggregate: RouterRecord = emptyObject();
      for (const [key, item] of Object.entries(from ?? {})) {
        if (isLazy(item)) {
          lazy[[...path, key].join('.')] = createLazyLoader({
            path,
            ref: item,
            key,
            aggregate,
          });
          continue;
        }
        if (isRouter(item)) {
          aggregate[key] = step(item._def.record, [...path, key]);
          continue;
        }
        if (!isProcedure(item)) {
          // RouterRecord
          aggregate[key] = step(item, [...path, key]);
          continue;
        }

        const newPath = [...path, key].join('.');

        if (procedures[newPath]) {
          throw new Error(`Duplicate key: ${newPath}`);
        }

        procedures[newPath] = item;
        aggregate[key] = item;
      }

      return aggregate;
    }
    const record = step(input);

    const _def: AnyRouter['_def'] = {
      _config: config,
      router: true,
      procedures,
      lazy,
      ...emptyRouter,
      record,
    };

    const router: BuiltRouter<TRoot, {}> = {
      ...(record as {}),
      _def,
      createCaller: createCallerFactory<TRoot>()({
        _def,
      }),
    };
    return router as BuiltRouter<TRoot, DecorateCreateRouterOptions<TInput>>;
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createRouterInner<TInput extends CreateRouterOptions>(
    input: TInput,
  ): BuiltRouter<TRoot, DecorateCreateRouterOptions<TInput>> {
    const reservedWordsUsed = new Set(
      Object.keys(input).filter((v) => reservedWords.includes(v)),
    );
    if (reservedWordsUsed.size > 0) {
      throw new Error(
        'Reserved words used in `router({})` call: ' +
          Array.from(reservedWordsUsed).join(', '),
      );
    }

    const procedures: Record<string, AnyProcedure> = emptyObject();
    const lazy: Record<string, LazyLoader<AnyRouter>> = emptyObject();

    function createLazyLoader(opts: {
      ref: Lazy<AnyRouter>;
      path: readonly string[];
      key: string;
      aggregate: RouterRecord;
    }): LazyLoader<AnyRouter> {
      return {
        ref: opts.ref,
        path: opts.path,
        key: opts.key,
        load: once(async () => {
          const router = await opts.ref();
          const lazyPath = [...opts.path, opts.key];
          const lazyKey = lazyPath.join('.');

          opts.aggregate[opts.key] = step(getRouterInput(router), lazyPath);

          delete lazy[lazyKey];
        }),
      };
    }

    function step(from: CreateRouterOptions, path: readonly string[] = []) {
      const aggregate: RouterRecord = emptyObject();
      for (const [key, item] of Object.entries(from ?? {})) {
        if (isLazy(item)) {
          lazy[[...path, key].join('.')] = createLazyLoader({
            path,
            ref: item,
            key,
            aggregate,
          });
          continue;
        }
        if (isRouter(item)) {
          aggregate[key] = step(getRouterInput(item), [...path, key]);
          continue;
        }
        if (!isProcedure(item)) {
          // RouterRecord
          aggregate[key] = step(item, [...path, key]);
          continue;
        }

        const newPath = [...path, key].join('.');

        if (procedures[newPath]) {
          throw new Error(`Duplicate key: ${newPath}`);
        }

        procedures[newPath] = item;
        aggregate[key] = item;
      }

      return aggregate;
    }
    const record = step(input);

    const _def: AnyRouter['_def'] = {
      _config: config,
      router: true,
      procedures,
      lazy,
      ...emptyRouter,
      record,
    };

    const router: BuiltRouter<TRoot, {}> = {
      ...(record as {}),
      _def,
      createCaller: createCallerFactory<TRoot>()({
        _def,
      }),
    };
    return router as BuiltRouter<TRoot, DecorateCreateRouterOptions<TInput>>;
  }
```

### 🔹 函式: `createLazyLoader()`
- **變更前簽章 (Before)**: `function createLazyLoader(opts:` (L268~L301)
- **變更後簽章 (After)**: `function createLazyLoader(opts:` (L290~L310)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createLazyLoader(opts: {
      ref: Lazy<AnyRouter>;
      path: readonly string[];
      key: string;
      aggregate: RouterRecord;
    }): LazyLoader<AnyRouter> {
      return {
        ref: opts.ref,
        load: once(async () => {
          const router = await opts.ref();
          const lazyPath = [...opts.path, opts.key];
          const lazyKey = lazyPath.join('.');

          opts.aggregate[opts.key] = step(router._def.record, lazyPath);

          delete lazy[lazyKey];

          // add lazy loaders for nested routers
          for (const [nestedKey, nestedItem] of Object.entries(
            router._def.lazy,
          )) {
            const nestedRouterKey = [...lazyPath, nestedKey].join('.');

            // console.log('adding lazy', nestedRouterKey);
            lazy[nestedRouterKey] = createLazyLoader({
              ref: nestedItem.ref,
              path: lazyPath,
              key: nestedKey,
              aggregate: opts.aggregate[opts.key] as RouterRecord,
            });
          }
        }),
      };
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createLazyLoader(opts: {
      ref: Lazy<AnyRouter>;
      path: readonly string[];
      key: string;
      aggregate: RouterRecord;
    }): LazyLoader<AnyRouter> {
      return {
        ref: opts.ref,
        path: opts.path,
        key: opts.key,
        load: once(async () => {
          const router = await opts.ref();
          const lazyPath = [...opts.path, opts.key];
          const lazyKey = lazyPath.join('.');

          opts.aggregate[opts.key] = step(getRouterInput(router), lazyPath);

          delete lazy[lazyKey];
        }),
      };
    }
```

### 🔹 函式: `step()`
- **變更前簽章 (Before)**: `function step(from: CreateRouterOptions, path: readonly string[] = [])` (L303~L336)
- **變更後簽章 (After)**: `function step(from: CreateRouterOptions, path: readonly string[] = [])` (L312~L345)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function step(from: CreateRouterOptions, path: readonly string[] = []) {
      const aggregate: RouterRecord = emptyObject();
      for (const [key, item] of Object.entries(from ?? {})) {
        if (isLazy(item)) {
          lazy[[...path, key].join('.')] = createLazyLoader({
            path,
            ref: item,
            key,
            aggregate,
          });
          continue;
        }
        if (isRouter(item)) {
          aggregate[key] = step(item._def.record, [...path, key]);
          continue;
        }
        if (!isProcedure(item)) {
          // RouterRecord
          aggregate[key] = step(item, [...path, key]);
          continue;
        }

        const newPath = [...path, key].join('.');

        if (procedures[newPath]) {
          throw new Error(`Duplicate key: ${newPath}`);
        }

        procedures[newPath] = item;
        aggregate[key] = item;
      }

      return aggregate;
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function step(from: CreateRouterOptions, path: readonly string[] = []) {
      const aggregate: RouterRecord = emptyObject();
      for (const [key, item] of Object.entries(from ?? {})) {
        if (isLazy(item)) {
          lazy[[...path, key].join('.')] = createLazyLoader({
            path,
            ref: item,
            key,
            aggregate,
          });
          continue;
        }
        if (isRouter(item)) {
          aggregate[key] = step(getRouterInput(item), [...path, key]);
          continue;
        }
        if (!isProcedure(item)) {
          // RouterRecord
          aggregate[key] = step(item, [...path, key]);
          continue;
        }

        const newPath = [...path, key].join('.');

        if (procedures[newPath]) {
          throw new Error(`Duplicate key: ${newPath}`);
        }

        procedures[newPath] = item;
        aggregate[key] = item;
      }

      return aggregate;
    }
```


---

### 🔹 Commit #19: `9353f4f1`
- **完整 Hash**: `9353f4f10378a6b6fcbdee9e0456d88d876a2801`
- **說明 (Ground Truth)**: fix(server): resolve record values lazily in Serialize (#7660)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/src/unstable-core-do-not-import/clientish/serialize.ts`
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

### 🔹 Commit #20: `9d24cc89`
- **完整 Hash**: `9d24cc8916f98ed1ed7aedaa6b9ccf7ee19d3f48`
- **說明 (Ground Truth)**: fix(server): cancelling a streamed response aborts its calls' signals (#7683)
- **變更檔案數**: 1

#### 📄 檔案: `packages/server/src/unstable-core-do-not-import/http/resolveResponse.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:50, E:48, A:2) ➔ After(N:53, E:50, A:2)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#abortSignal** `(Control)`
    └── ⚡ **on('abort')**
        └── 🎯 [TRIGGERS] `onAbort()`
  🌲 **#combinedAbort.signal** `(Control)`
    └── ⚡ **on('abort')**
        └── 🎯 [TRIGGERS] `cleanup()`
            └── 🎯 [CALLS] `clearTimeout (External/Unresolved)()`
            └── 🎯 [CALLS] `removeEventListener()()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `pull` (FUNCTION_DEF)
  • + [新增節點] `cancel` (FUNCTION_DEF)
  • + [新增節點] `abortOnCancel` (FUNCTION_DEF)
  • + [新增呼叫邊] `resolveResponse` ──[CALLS [guard: (infoError)]]──> `abortSignalsAnyPonyfill (External/Unresolved)`
  • + [新增呼叫邊] `resolveResponse` ──[CALLS [guard: (info.accept === 'application/jsonl')]]──> `abortOnCancel`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'onError' 被深鎖在內部閉包 (scope:resolveResponse@after/packages/server/src/unstable-core-do-not-import/http/resolveResponse.ts:L238C8)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `iterable()`
- **變更前簽章 (Before)**: `iterable()` (L456~L483)
- **變更後簽章 (After)**: `iterable()` (L486~L513)

#### ◀️ 變更前實作碼 (Before Implementation):
```
() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, opts.req.signal)
              : result.data;
            return dataAsIterable;
          }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, callSignal)
              : result.data;
            return dataAsIterable;
          }
```

### 🔹 函式: `rpcCalls()`
- **變更前簽章 (Before)**: `rpcCalls(call)` (L328~L403)
- **變更後簽章 (After)**: `rpcCalls(call)` (L358~L433)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(opts.req.signal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    }
```

### 🔹 函式: `cancel()`
- **變更前簽章 (Before)**: `cancel()` (L552~L555)
- **變更後簽章 (After)**: `cancel()` (L582~L586)

#### ◀️ 變更前實作碼 (Before Implementation):
```
cancel() {
                abortSignal.removeEventListener('abort', onAbort);
                return reader.cancel();
              }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
cancel() {
                abortSignal.removeEventListener('abort', onAbort);
                bodyCancelled.abort();
                return reader.cancel();
              }
```

### 🔹 函式: `resolveResponse()`
- **變更前簽章 (Before)**: `async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response>` (L213~L770)
- **變更後簽章 (After)**: `async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response>` (L238~L801)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response> {
  const { router, req } = opts;
  const headers = new Headers([['vary', 'trpc-accept, accept']]);
  const config = router._def._config;

  const url = new URL(req.url);

  if (req.method === 'HEAD') {
    // can be used for lambda warmup
    return new Response(null, {
      status: 204,
    });
  }

  const allowBatching = opts.allowBatching ?? opts.batching?.enabled ?? true;
  const allowMethodOverride =
    (opts.allowMethodOverride ?? false) && req.method === 'POST';

  type $Context = inferRouterContext<TRouter>;

  const infoTuple: ResultTuple<TRPCRequestInfo> = await run(async () => {
    try {
      return [
        undefined,
        await getRequestInfo({
          req,
          path: decodeURIComponent(opts.path),
          router,
          searchParams: url.searchParams,
          headers: opts.req.headers,
          url,
          maxBatchSize: opts.maxBatchSize,
        }),
      ];
    } catch (cause) {
      return [getTRPCErrorFromUnknown(cause), undefined];
    }
  });

  interface ContextManager {
    valueOrUndefined: () => $Context | undefined;
    value: () => $Context;
    create: (info: TRPCRequestInfo) => Promise<void>;
  }
  const ctxManager: ContextManager = run(() => {
    let result: ResultTuple<$Context> | undefined = undefined;
    return {
      valueOrUndefined: () => {
        if (!result) {
          return undefined;
        }
        return result[1];
      },
      value: () => {
        const [err, ctx] = result!;
        if (err) {
          throw err;
        }
        return ctx;
      },
      create: async (info) => {
        if (result) {
          throw new Error(
            'This should only be called once - report a bug in tRPC',
          );
        }
        try {
          const ctx = await opts.createContext({
            info,
          });
          result = [undefined, ctx];
        } catch (cause) {
          result = [getTRPCErrorFromUnknown(cause), undefined];
        }
      },
    };
  });

  const methodMapper = allowMethodOverride
    ? TYPE_ACCEPTED_METHOD_MAP_WITH_METHOD_OVERRIDE
    : TYPE_ACCEPTED_METHOD_MAP;

  /**
   * @deprecated
   */
  const isStreamCall = getAcceptHeader(req.headers) === 'application/jsonl';

  const experimentalSSE = config.sse?.enabled ?? true;
  try {
    const [infoError, info] = infoTuple;
    if (infoError) {
      throw infoError;
    }
    if (info.isBatchCall && !allowBatching) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batching is not enabled on the server`,
      });
    }
    /* istanbul ignore if -- @preserve */
    if (isStreamCall && !info.isBatchCall) {
      throw new TRPCError({
        message: `Streaming requests must be batched (you can do a batch of 1)`,
        code: 'BAD_REQUEST',
      });
    }
    await ctxManager.create(info);

    interface RPCResultOk {
      data: unknown;
      signal?: AbortSignal;
    }
    type RPCResult = ResultTuple<RPCResultOk>;
    const rpcCalls = info.calls.map(async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(opts.req.signal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    });

    // ----------- response handlers -----------
    if (!info.isBatchCall) {
      const [call] = info.calls;
      const [error, result] = await rpcCalls[0]!;

      switch (info.type) {
        case 'unknown':
        case 'mutation':
        case 'query': {
          // httpLink
          headers.set('content-type', 'application/json');

          if (isDataStream(result?.data)) {
            throw new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            });
          }
          const res: TRPCResponse<unknown, inferRouterError<TRouter>> = error
            ? {
                error: getErrorShape({
                  config,
                  ctx: ctxManager.valueOrUndefined(),
                  error,
                  input: call!.result(),
                  path: call!.path,
                  type: info.type,
                }),
              }
            : { result: { data: result.data } };

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: error ? [error] : [],
            headers,
            untransformedJSON: [res],
          });
          return new Response(
            JSON.stringify(transformTRPCResponse(config, res)),
            {
              status: headResponse.status,
              headers,
            },
          );
        }
        case 'subscription': {
          // httpSubscriptionLink

          const iterable: AsyncIterable<unknown> = run(() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, opts.req.signal)
              : result.data;
            return dataAsIterable;
          });

          const stream = sseStreamProducer({
            ...config.sse,
            data: iterable,
            serialize: (v) => config.transformer.output.serialize(v),
            formatError(errorOpts) {
              const error = getTRPCErrorFromUnknown(errorOpts.error);
              const input = call?.result();
              const path = call?.path;
              const type = call?.procedure?._def.type ?? 'unknown';

              opts.onError?.({
                error,
                path,
                input,
                ctx: ctxManager.valueOrUndefined(),
                req: opts.req,
                type,
              });

              const shape = getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input,
                path,
                type,
              });

              return shape;
            },
          });
          for (const [key, value] of Object.entries(sseHeaders)) {
            headers.set(key, value);
          }

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: [],
            headers,
            untransformedJSON: null,
          });

          const abortSignal = result?.signal;
          let responseBody: ReadableStream<Uint8Array> = stream;

          // Fixes: https://github.com/trpc/trpc/issues/7094
          if (abortSignal) {
            const reader = stream.getReader();
            const onAbort = () => void reader.cancel();
            if (abortSignal.aborted) {
              onAbort();
            } else {
              abortSignal.addEventListener('abort', onAbort, { once: true });
            }

            responseBody = new ReadableStream({
              async pull(controller) {
                const chunk = await reader.read();
                if (chunk.done) {
                  abortSignal.removeEventListener('abort', onAbort);
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              },
              cancel() {
                abortSignal.removeEventListener('abort', onAbort);
                return reader.cancel();
              },
            });
          }

          return new Response(responseBody, {
            headers,
            status: headResponse.status,
          });
        }
      }
    }

    // batch response handlers
    if (info.accept === 'application/jsonl') {
      // httpBatchStreamLink
      headers.set('content-type', 'application/json');
      headers.set('transfer-encoding', 'chunked');
      const headResponse = initResponse({
        ctx: ctxManager.valueOrUndefined(),
        info,
        responseMeta: opts.responseMeta,
        errors: [],
        headers,
        untransformedJSON: null,
      });
      const stream = jsonlStreamProducer({
        ...config.jsonl,
        /**
         * Example structure for `maxDepth: 4`:
         * {
         *   // 1
         *   0: {
         *     // 2
         *     result: {
         *       // 3
         *       data: // 4
         *     }
         *   }
         * }
         */
        maxDepth: Infinity,
        data: rpcCalls.map(async (res, index) => {
          const [error, result] = await res;

          const call = info.calls[index];

          if (error) {
            return {
              error: getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input: call!.result(),
                path: call!.path,
                type: call!.procedure?._def.type ?? 'unknown',
              }),
            };
          }

          /**
           * Not very pretty, but we need to wrap nested data in promises
           * Our stream producer will only resolve top-level async values or async values that are directly nested in another async value
           */
          const iterable = isObservable(result.data)
            ? observableToAsyncIterable(result.data, opts.req.signal)
            : Promise.resolve(result.data);
          return {
            result: Promise.resolve({
              data: iterable,
            }),
          };
        }),
        serialize: (data) => config.transformer.output.serialize(data),
        onError: (cause) => {
          opts.onError?.({
            error: getTRPCErrorFromUnknown(cause.error),
            path: undefined,
            input: undefined,
            ctx: ctxManager.valueOrUndefined(),
            req: opts.req,
            type: info?.type ?? 'unknown',
          });
        },

        formatError(errorOpts) {
          const call = info?.calls[errorOpts.path[0] as any];

          const error = getTRPCErrorFromUnknown(errorOpts.error);
          const input = call?.result();
          const path = call?.path;
          const type = call?.procedure?._def.type ?? 'unknown';

          // no need to call `onError` here as it will be propagated through the stream itself

          const shape = getErrorShape({
            config,
            ctx: ctxManager.valueOrUndefined(),
            error,
            input,
            path,
            type,
          });

          return shape;
        },
      });

      return new Response(stream, {
        headers,
        status: headResponse.status,
      });
    }

    // httpBatchLink
    /**
     * Non-streaming response:
     * - await all responses in parallel, blocking on the slowest one
     * - create headers with known response body
     * - return a complete HTTPResponse
     */
    headers.set('content-type', 'application/json');
    const results: RPCResult[] = (await Promise.all(rpcCalls)).map(
      (res): RPCResult => {
        const [error, result] = res;
        if (error) {
          return res;
        }

        if (isDataStream(result.data)) {
          return [
            new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            }),
            undefined,
          ];
        }
        return res;
      },
    );
    const resultAsRPCResponse = results.map(
      (
        [error, result],
        index,
      ): TRPCResponse<unknown, inferRouterError<TRouter>> => {
        const call = info.calls[index]!;
        if (error) {
          return {
            error: getErrorShape({
              config,
              ctx: ctxManager.valueOrUndefined(),
              error,
              input: call.result(),
              path: call.path,
              type: call.procedure?._def.type ?? 'unknown',
            }),
          };
        }
        return {
          result: { data: result.data },
        };
      },
    );

    const errors = results
      .map(([error]) => error)
      .filter(Boolean) as TRPCError[];

    const headResponse = initResponse({
      ctx: ctxManager.valueOrUndefined(),
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON: resultAsRPCResponse,
      errors,
      headers,
    });

    return new Response(
      JSON.stringify(transformTRPCResponse(config, resultAsRPCResponse)),
      {
        status: headResponse.status,
        headers,
      },
    );
  } catch (cause) {
    const [_infoError, info] = infoTuple;
    const ctx = ctxManager.valueOrUndefined();
    // we get here if
    // - batching is called when it's not enabled
    // - `createContext()` throws
    // - `router._def._config.transformer.output.serialize()` throws
    // - post body is too large
    // - input deserialization fails
    // - `errorFormatter` return value is malformed
    const { error, untransformedJSON, body } = caughtErrorToData(cause, {
      opts,
      ctx: ctxManager.valueOrUndefined(),
      type: info?.type ?? 'unknown',
    });

    const headResponse = initResponse({
      ctx,
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON,
      errors: [error],
      headers,
    });

    return new Response(body, {
      status: headResponse.status,
      headers,
    });
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async function resolveResponse<TRouter extends AnyRouter>(
  opts: ResolveHTTPRequestOptions<TRouter>,
): Promise<Response> {
  const { router, req } = opts;
  const headers = new Headers([['vary', 'trpc-accept, accept']]);
  const config = router._def._config;

  const url = new URL(req.url);

  if (req.method === 'HEAD') {
    // can be used for lambda warmup
    return new Response(null, {
      status: 204,
    });
  }

  const allowBatching = opts.allowBatching ?? opts.batching?.enabled ?? true;
  const allowMethodOverride =
    (opts.allowMethodOverride ?? false) && req.method === 'POST';

  type $Context = inferRouterContext<TRouter>;

  const infoTuple: ResultTuple<TRPCRequestInfo> = await run(async () => {
    try {
      return [
        undefined,
        await getRequestInfo({
          req,
          path: decodeURIComponent(opts.path),
          router,
          searchParams: url.searchParams,
          headers: opts.req.headers,
          url,
          maxBatchSize: opts.maxBatchSize,
        }),
      ];
    } catch (cause) {
      return [getTRPCErrorFromUnknown(cause), undefined];
    }
  });

  interface ContextManager {
    valueOrUndefined: () => $Context | undefined;
    value: () => $Context;
    create: (info: TRPCRequestInfo) => Promise<void>;
  }
  const ctxManager: ContextManager = run(() => {
    let result: ResultTuple<$Context> | undefined = undefined;
    return {
      valueOrUndefined: () => {
        if (!result) {
          return undefined;
        }
        return result[1];
      },
      value: () => {
        const [err, ctx] = result!;
        if (err) {
          throw err;
        }
        return ctx;
      },
      create: async (info) => {
        if (result) {
          throw new Error(
            'This should only be called once - report a bug in tRPC',
          );
        }
        try {
          const ctx = await opts.createContext({
            info,
          });
          result = [undefined, ctx];
        } catch (cause) {
          result = [getTRPCErrorFromUnknown(cause), undefined];
        }
      },
    };
  });

  const methodMapper = allowMethodOverride
    ? TYPE_ACCEPTED_METHOD_MAP_WITH_METHOD_OVERRIDE
    : TYPE_ACCEPTED_METHOD_MAP;

  /**
   * @deprecated
   */
  const isStreamCall = getAcceptHeader(req.headers) === 'application/jsonl';

  const experimentalSSE = config.sse?.enabled ?? true;
  try {
    const [infoError, info] = infoTuple;
    if (infoError) {
      throw infoError;
    }
    if (info.isBatchCall && !allowBatching) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Batching is not enabled on the server`,
      });
    }
    /* istanbul ignore if -- @preserve */
    if (isStreamCall && !info.isBatchCall) {
      throw new TRPCError({
        message: `Streaming requests must be batched (you can do a batch of 1)`,
        code: 'BAD_REQUEST',
      });
    }
    await ctxManager.create(info);

    interface RPCResultOk {
      data: unknown;
      signal?: AbortSignal;
    }
    type RPCResult = ResultTuple<RPCResultOk>;
    const bodyCancelled = new AbortController();
    const callSignal = abortSignalsAnyPonyfill([
      opts.req.signal,
      bodyCancelled.signal,
    ]);
    const rpcCalls = info.calls.map(async (call): Promise<RPCResult> => {
      const proc = call.procedure;
      const combinedAbort = combinedAbortController(callSignal);
      try {
        if (opts.error) {
          throw opts.error;
        }

        if (!proc) {
          throw new TRPCError({
            code: 'NOT_FOUND',
            message: `No procedure found on path "${call.path}"`,
          });
        }

        if (!methodMapper[proc._def.type].includes(req.method as HTTPMethods)) {
          throw new TRPCError({
            code: 'METHOD_NOT_SUPPORTED',
            message: `Unsupported ${req.method}-request to ${proc._def.type} procedure at path "${call.path}"`,
          });
        }

        if (proc._def.type === 'subscription') {
          /* istanbul ignore if -- @preserve */
          if (info.isBatchCall) {
            throw new TRPCError({
              code: 'BAD_REQUEST',
              message: `Cannot batch subscription calls`,
            });
          }

          if (config.sse?.maxDurationMs) {
            function cleanup() {
              clearTimeout(timer);
              combinedAbort.signal.removeEventListener('abort', cleanup);

              combinedAbort.controller.abort();
            }
            const timer = setTimeout(cleanup, config.sse.maxDurationMs);
            combinedAbort.signal.addEventListener('abort', cleanup);
          }
        }
        const data: unknown = await proc({
          path: call.path,
          getRawInput: call.getRawInput,
          ctx: ctxManager.value(),
          type: proc._def.type,
          signal: combinedAbort.signal,
          batchIndex: call.batchIndex,
        });
        return [
          undefined,
          {
            data,
            signal:
              proc._def.type === 'subscription'
                ? combinedAbort.signal
                : undefined,
          },
        ];
      } catch (cause) {
        const error = getTRPCErrorFromUnknown(cause);
        const input = call.result();

        opts.onError?.({
          error,
          path: call.path,
          input,
          ctx: ctxManager.valueOrUndefined(),
          type: call.procedure?._def.type ?? 'unknown',
          req: opts.req,
        });

        return [error, undefined];
      }
    });

    // ----------- response handlers -----------
    if (!info.isBatchCall) {
      const [call] = info.calls;
      const [error, result] = await rpcCalls[0]!;

      switch (info.type) {
        case 'unknown':
        case 'mutation':
        case 'query': {
          // httpLink
          headers.set('content-type', 'application/json');

          if (isDataStream(result?.data)) {
            throw new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            });
          }
          const res: TRPCResponse<unknown, inferRouterError<TRouter>> = error
            ? {
                error: getErrorShape({
                  config,
                  ctx: ctxManager.valueOrUndefined(),
                  error,
                  input: call!.result(),
                  path: call!.path,
                  type: info.type,
                }),
              }
            : { result: { data: result.data } };

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: error ? [error] : [],
            headers,
            untransformedJSON: [res],
          });
          return new Response(
            JSON.stringify(transformTRPCResponse(config, res)),
            {
              status: headResponse.status,
              headers,
            },
          );
        }
        case 'subscription': {
          // httpSubscriptionLink

          const iterable: AsyncIterable<unknown> = run(() => {
            if (error) {
              return errorToAsyncIterable(error);
            }
            if (!experimentalSSE) {
              return errorToAsyncIterable(
                new TRPCError({
                  code: 'METHOD_NOT_SUPPORTED',
                  message: 'Missing experimental flag "sseSubscriptions"',
                }),
              );
            }

            if (!isObservable(result.data) && !isAsyncIterable(result.data)) {
              return errorToAsyncIterable(
                new TRPCError({
                  message: `Subscription ${
                    call!.path
                  } did not return an observable or a AsyncGenerator`,
                  code: 'INTERNAL_SERVER_ERROR',
                }),
              );
            }
            const dataAsIterable = isObservable(result.data)
              ? observableToAsyncIterable(result.data, callSignal)
              : result.data;
            return dataAsIterable;
          });

          const stream = sseStreamProducer({
            ...config.sse,
            data: iterable,
            serialize: (v) => config.transformer.output.serialize(v),
            formatError(errorOpts) {
              const error = getTRPCErrorFromUnknown(errorOpts.error);
              const input = call?.result();
              const path = call?.path;
              const type = call?.procedure?._def.type ?? 'unknown';

              opts.onError?.({
                error,
                path,
                input,
                ctx: ctxManager.valueOrUndefined(),
                req: opts.req,
                type,
              });

              const shape = getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input,
                path,
                type,
              });

              return shape;
            },
          });
          for (const [key, value] of Object.entries(sseHeaders)) {
            headers.set(key, value);
          }

          const headResponse = initResponse({
            ctx: ctxManager.valueOrUndefined(),
            info,
            responseMeta: opts.responseMeta,
            errors: [],
            headers,
            untransformedJSON: null,
          });

          const abortSignal = result?.signal;
          let responseBody: ReadableStream<Uint8Array> = stream;

          // Fixes: https://github.com/trpc/trpc/issues/7094
          if (abortSignal) {
            const reader = stream.getReader();
            const onAbort = () => void reader.cancel();
            if (abortSignal.aborted) {
              onAbort();
            } else {
              abortSignal.addEventListener('abort', onAbort, { once: true });
            }

            responseBody = new ReadableStream({
              async pull(controller) {
                const chunk = await reader.read();
                if (chunk.done) {
                  abortSignal.removeEventListener('abort', onAbort);
                  controller.close();
                } else {
                  controller.enqueue(chunk.value);
                }
              },
              cancel() {
                abortSignal.removeEventListener('abort', onAbort);
                bodyCancelled.abort();
                return reader.cancel();
              },
            });
          }

          return new Response(responseBody, {
            headers,
            status: headResponse.status,
          });
        }
      }
    }

    // batch response handlers
    if (info.accept === 'application/jsonl') {
      // httpBatchStreamLink
      headers.set('content-type', 'application/json');
      headers.set('transfer-encoding', 'chunked');
      const headResponse = initResponse({
        ctx: ctxManager.valueOrUndefined(),
        info,
        responseMeta: opts.responseMeta,
        errors: [],
        headers,
        untransformedJSON: null,
      });
      const stream = jsonlStreamProducer({
        ...config.jsonl,
        /**
         * Example structure for `maxDepth: 4`:
         * {
         *   // 1
         *   0: {
         *     // 2
         *     result: {
         *       // 3
         *       data: // 4
         *     }
         *   }
         * }
         */
        maxDepth: Infinity,
        data: rpcCalls.map(async (res, index) => {
          const [error, result] = await res;

          const call = info.calls[index];

          if (error) {
            return {
              error: getErrorShape({
                config,
                ctx: ctxManager.valueOrUndefined(),
                error,
                input: call!.result(),
                path: call!.path,
                type: call!.procedure?._def.type ?? 'unknown',
              }),
            };
          }

          /**
           * Not very pretty, but we need to wrap nested data in promises
           * Our stream producer will only resolve top-level async values or async values that are directly nested in another async value
           */
          const iterable = isObservable(result.data)
            ? observableToAsyncIterable(result.data, callSignal)
            : Promise.resolve(result.data);
          return {
            result: Promise.resolve({
              data: iterable,
            }),
          };
        }),
        serialize: (data) => config.transformer.output.serialize(data),
        onError: (cause) => {
          opts.onError?.({
            error: getTRPCErrorFromUnknown(cause.error),
            path: undefined,
            input: undefined,
            ctx: ctxManager.valueOrUndefined(),
            req: opts.req,
            type: info?.type ?? 'unknown',
          });
        },

        formatError(errorOpts) {
          const call = info?.calls[errorOpts.path[0] as any];

          const error = getTRPCErrorFromUnknown(errorOpts.error);
          const input = call?.result();
          const path = call?.path;
          const type = call?.procedure?._def.type ?? 'unknown';

          // no need to call `onError` here as it will be propagated through the stream itself

          const shape = getErrorShape({
            config,
            ctx: ctxManager.valueOrUndefined(),
            error,
            input,
            path,
            type,
          });

          return shape;
        },
      });

      return new Response(abortOnCancel(stream, bodyCancelled), {
        headers,
        status: headResponse.status,
      });
    }

    // httpBatchLink
    /**
     * Non-streaming response:
     * - await all responses in parallel, blocking on the slowest one
     * - create headers with known response body
     * - return a complete HTTPResponse
     */
    headers.set('content-type', 'application/json');
    const results: RPCResult[] = (await Promise.all(rpcCalls)).map(
      (res): RPCResult => {
        const [error, result] = res;
        if (error) {
          return res;
        }

        if (isDataStream(result.data)) {
          return [
            new TRPCError({
              code: 'UNSUPPORTED_MEDIA_TYPE',
              message:
                'Cannot use stream-like response in non-streaming request - use httpBatchStreamLink',
            }),
            undefined,
          ];
        }
        return res;
      },
    );
    const resultAsRPCResponse = results.map(
      (
        [error, result],
        index,
      ): TRPCResponse<unknown, inferRouterError<TRouter>> => {
        const call = info.calls[index]!;
        if (error) {
          return {
            error: getErrorShape({
              config,
              ctx: ctxManager.valueOrUndefined(),
              error,
              input: call.result(),
              path: call.path,
              type: call.procedure?._def.type ?? 'unknown',
            }),
          };
        }
        return {
          result: { data: result.data },
        };
      },
    );

    const errors = results
      .map(([error]) => error)
      .filter(Boolean) as TRPCError[];

    const headResponse = initResponse({
      ctx: ctxManager.valueOrUndefined(),
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON: resultAsRPCResponse,
      errors,
      headers,
    });

    return new Response(
      JSON.stringify(transformTRPCResponse(config, resultAsRPCResponse)),
      {
        status: headResponse.status,
        headers,
      },
    );
  } catch (cause) {
    const [_infoError, info] = infoTuple;
    const ctx = ctxManager.valueOrUndefined();
    // we get here if
    // - batching is called when it's not enabled
    // - `createContext()` throws
    // - `router._def._config.transformer.output.serialize()` throws
    // - post body is too large
    // - input deserialization fails
    // - `errorFormatter` return value is malformed
    const { error, untransformedJSON, body } = caughtErrorToData(cause, {
      opts,
      ctx: ctxManager.valueOrUndefined(),
      type: info?.type ?? 'unknown',
    });

    const headResponse = initResponse({
      ctx,
      info,
      responseMeta: opts.responseMeta,
      untransformedJSON,
      errors: [error],
      headers,
    });

    return new Response(body, {
      status: headResponse.status,
      headers,
    });
  }
}
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/trpc show 43b7afab8af3c202694d38a19f4a64131990c351
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 43b7afab8af3c202694d38a19f4a64131990c351~1 --file test_repos/trpc/packages/server/src/adapters/aws-lambda/getPlanner.ts
   ```
