# 🔬 CODE-Map 基準審查獨立驗證報告: `vllm`
> **技術生態**: `Python (LLM 推理串流 / PagedAttention)`  
> **本地倉庫路徑**: `test_repos/vllm`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 33 Files  
> **報告生成時間**: 2026-10-20 21:44:04  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `22` / `33` | `66.7%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `10` / `33` | `30.3%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `1` / `33` | `3.0%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`32` / `33`** | **`97.0%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `33` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `34ac4f96`
- **完整 Hash**: `34ac4f96a399836393894207dae296760b413715`
- **說明 (Ground Truth)**: [Bugfix][KV Connector][Mooncake] Wait for all peers before completing failed receives to avoid potential KV block write-after-free (#62282)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/distributed/kv_transfer/kv_connector/v1/mooncake/mooncake_connector.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:238, E:347, A:0) ➔ After(N:240, E:350, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 6, -Edges: 3, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `MooncakeConnectorWorker._complete_pull_task` (FUNCTION_DEF)
  • + [新增節點] `copy (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `MooncakeConnectorWorker.receive_kv_from_single_worker` ──[CALLS]──> `copy (External/Unresolved)`
  • + [新增呼叫邊] `MooncakeConnectorWorker.receive_kv_from_single_worker` ──[CALLS]──> `list (External/Unresolved)`
  • + [新增呼叫邊] `MooncakeConnectorWorker._handle_failed_recv` ──[CALLS]──> `MooncakeConnectorWorker._complete_pull_task`
  • + [新增呼叫邊] `MooncakeConnectorWorker._complete_pull_task` ──[CALLS]──> `any (External/Unresolved)`
  • + [新增呼叫邊] `MooncakeConnectorWorker._complete_pull_task` ──[CALLS]──> `add (External/Unresolved)`
  • + [新增呼叫邊] `MooncakeConnectorWorker.process_pulling_result` ──[CALLS]──> `MooncakeConnectorWorker._complete_pull_task`
  • - [移除呼叫邊] `MooncakeConnectorWorker._handle_failed_recv` ──[CALLS]──> `add (External/Unresolved)`
  • - [移除呼叫邊] `MooncakeConnectorWorker.process_pulling_result` ──[CALLS]──> `any (External/Unresolved)`
  • - [移除呼叫邊] `MooncakeConnectorWorker.process_pulling_result` ──[CALLS]──> `add (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `MooncakeConnectorWorker.process_pulling_result()`
- **變更前簽章 (Before)**: `def process_pulling_result( self, response: MooncakeXferResponse, pull_metas: dict[ReqId, PullReqMeta], )` (L2516~L2540)
- **變更後簽章 (After)**: `def process_pulling_result( self, response: MooncakeXferResponse, pull_metas: dict[ReqId, PullReqMeta], )` (L2535~L2552)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def process_pulling_result(
        self,
        response: MooncakeXferResponse,
        pull_metas: dict[ReqId, PullReqMeta],
    ):
        ok_reqs: list[ReqId] = response.ok_reqs or []

        for req_id in ok_reqs:
            pull_meta = pull_metas[req_id]
            if pull_meta.failed:
                continue
            # No race because we are in async loop.
            pull_meta.pull_tasks_count -= 1
            # Empty pulls only release the producer's blocks; the consumer
            # did not enter WAITING_FOR_REMOTE_KVS.
            if pull_meta.pull_tasks_count == 0 and any(pull_meta.local_block_ids):
                self.finished_recving_reqs.add(pull_meta.d_req_id)

        if ok_reqs:
            logger.debug("pulling kv_caches for %s finished", ok_reqs)

        if response.err_reqs:
            self._handle_failed_recv(
                pull_metas, response.err_reqs, response.err_msg or "unknown error"
            )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def process_pulling_result(
        self,
        response: MooncakeXferResponse,
        pull_metas: dict[ReqId, PullReqMeta],
    ):
        if response.err_reqs:
            self._handle_failed_recv(
                pull_metas, response.err_reqs, response.err_msg or "unknown error"
            )
        ok_reqs: list[ReqId] = response.ok_reqs or []

        for req_id in ok_reqs:
            pull_meta = pull_metas.pop(req_id, None)
            if pull_meta is not None:
                self._complete_pull_task(pull_meta)

        if ok_reqs:
            logger.debug("pulling kv_caches for %s finished", ok_reqs)
```

### 🔹 函式: `MooncakeConnectorWorker.receive_kv_from_single_worker()`
- **變更前簽章 (Before)**: `async def receive_kv_from_single_worker( self, worker_addr: str, pull_metas: dict[ReqId, PullReqMeta], )` (L2397~L2470)
- **變更後簽章 (After)**: `async def receive_kv_from_single_worker( self, worker_addr: str, pull_metas: dict[ReqId, PullReqMeta], ): # Each peer settles its own requests, sharing the per-request counters.` (L2397~L2478)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async def receive_kv_from_single_worker(
        self,
        worker_addr: str,
        pull_metas: dict[ReqId, PullReqMeta],
    ):
        req_ids = set(pull_metas)
        include_layout = (
            not self._kv_layout_id or worker_addr not in self._acked_layout_peers
        )
        # Each pass either returns or breaks out of the recv loop to resend
        # the layout after a LAYOUT_MISS.
        while True:
            metadata = self._build_pull_metadata(
                pull_metas, include_layout=include_layout
            )
            encoded_data = self._encoder.encode(metadata)
            logger.debug(
                "MooncakeXferMetadata to %s is %d bytes (%s).",
                worker_addr,
                len(encoded_data),
                "layout" if include_layout else "blocks",
            )
            logger.debug(
                "Sending kv transfer request for %s on path: %s", req_ids, worker_addr
            )
            try:
                with make_zmq_socket(
                    self.async_zmq_ctx, worker_addr, zmq.DEALER, bind=False, linger=0
                ) as sock:
                    sock.setsockopt(
                        zmq.RCVTIMEO,
                        (envs.VLLM_MOONCAKE_ABORT_REQUEST_TIMEOUT + 60) * 1000,
                    )
                    await sock.send(encoded_data)
                    while True:
                        ret_msg = await sock.recv()
                        response = self._xfer_resp_decoder.decode(ret_msg)
                        status = response.status
                        if status == MooncakeXferResponseStatus.LAYOUT_MISS:
                            self._acked_layout_peers.discard(worker_addr)
                            if not include_layout:
                                logger.info(
                                    "Mooncake prefill %s lost the KV layout; "
                                    "resending it.",
                                    worker_addr,
                                )
                                include_layout = True
                                break
                        if status in (
                            MooncakeXferResponseStatus.ERROR,
                            MooncakeXferResponseStatus.LAYOUT_MISS,
                        ):
                            self._handle_failed_recv(
                                pull_metas,
                                req_ids,
                                response.err_msg or "transfer error",
                            )
                            return
                        if (
                            self._kv_layout_id
                            and response.layout_id == self._kv_layout_id
                        ):
                            self._acked_layout_peers.add(worker_addr)
                        self.process_pulling_result(response, pull_metas)
                        if status == MooncakeXferResponseStatus.FINISH:
                            return
            except zmq.ContextTerminated:
                logger.debug(
                    "ZMQ context terminated, exiting Mooncake receiver thread."
                )
                return
            except Exception as e:
                self._handle_failed_recv(pull_metas, req_ids, f"transfer failed: {e}")
                return
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async def receive_kv_from_single_worker(
        self,
        worker_addr: str,
        pull_metas: dict[ReqId, PullReqMeta],
    ):
        # Each peer settles its own requests, sharing the per-request counters.
        pull_metas = pull_metas.copy()
        req_ids = set(pull_metas)
        include_layout = (
            not self._kv_layout_id or worker_addr not in self._acked_layout_peers
        )
        # Each pass either returns or breaks out of the recv loop to resend
        # the layout after a LAYOUT_MISS.
        while True:
            metadata = self._build_pull_metadata(
                pull_metas, include_layout=include_layout
            )
            encoded_data = self._encoder.encode(metadata)
            logger.debug(
                "MooncakeXferMetadata to %s is %d bytes (%s).",
                worker_addr,
                len(encoded_data),
                "layout" if include_layout else "blocks",
            )
            logger.debug(
                "Sending kv transfer request for %s on path: %s", req_ids, worker_addr
            )
            try:
                with make_zmq_socket(
                    self.async_zmq_ctx, worker_addr, zmq.DEALER, bind=False, linger=0
                ) as sock:
                    sock.setsockopt(
                        zmq.RCVTIMEO,
                        (envs.VLLM_MOONCAKE_ABORT_REQUEST_TIMEOUT + 60) * 1000,
                    )
                    await sock.send(encoded_data)
                    while True:
                        ret_msg = await sock.recv()
                        response = self._xfer_resp_decoder.decode(ret_msg)
                        status = response.status
                        if status == MooncakeXferResponseStatus.LAYOUT_MISS:
                            self._acked_layout_peers.discard(worker_addr)
                            if not include_layout:
                                logger.info(
                                    "Mooncake prefill %s lost the KV layout; "
                                    "resending it.",
                                    worker_addr,
                                )
                                include_layout = True
                                break
                        if status in (
                            MooncakeXferResponseStatus.ERROR,
                            MooncakeXferResponseStatus.LAYOUT_MISS,
                        ):
                            self._handle_failed_recv(
                                pull_metas,
                                req_ids,
                                response.err_msg or "transfer error",
                            )
                            return
                        if (
                            self._kv_layout_id
                            and response.layout_id == self._kv_layout_id
                        ):
                            self._acked_layout_peers.add(worker_addr)
                        self.process_pulling_result(response, pull_metas)
                        if status == MooncakeXferResponseStatus.FINISH:
                            # P may omit expired requests from its final response.
                            self._handle_failed_recv(
                                pull_metas,
                                list(pull_metas),
                                "peer finished without reporting a transfer result",
                            )
                            return
            except zmq.ContextTerminated:
                logger.debug(
                    "ZMQ context terminated, exiting Mooncake receiver thread."
                )
                return
            except Exception as e:
                self._handle_failed_recv(pull_metas, req_ids, f"transfer failed: {e}")
                return
```

### 🔹 函式: `MooncakeConnectorWorker._handle_failed_recv()`
- **變更前簽章 (Before)**: `def _handle_failed_recv( self, pull_metas: dict[ReqId, PullReqMeta], req_ids: Collection[ReqId], reason: str, ) -> None` (L2472~L2504)
- **變更後簽章 (After)**: `def _handle_failed_recv( self, pull_metas: dict[ReqId, PullReqMeta], req_ids: Collection[ReqId], reason: str, ) -> None` (L2480~L2516)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _handle_failed_recv(
        self,
        pull_metas: dict[ReqId, PullReqMeta],
        req_ids: Collection[ReqId],
        reason: str,
    ) -> None:
        """Report a failed remote KV load so the scheduler can fail or recompute it."""
        failed: list[ReqId] = []
        for req_id in req_ids:
            pull_meta = pull_metas.get(req_id)
            if pull_meta is None or pull_meta.failed:
                continue
            pull_meta.failed = True
            failed.append(req_id)
            self.xfer_stats.record_failed_recv()

            invalid = {b for group in pull_meta.local_block_ids for b in group}
            if not invalid:
                # A pull with no local blocks only asks P to release its blocks
                # for a request that never reached the scheduler (see
                # AsyncLLM.notify_kv_transfer_request_rejected, which submits an
                # abort_immediately request just to run request_finished). No D
                # request is waiting on a load, and reporting one here would trip
                # the scheduler's `assert req_id in self.requests`.
                continue
            if self._is_hma_required:
                self._failed_recv_reqs.put(pull_meta.d_req_id)
            else:
                self._invalid_block_ids.put(invalid)
            self.finished_recving_reqs.add(pull_meta.d_req_id)

        if failed:
            logger.error("pulling kv_caches for %s failed: %s", failed, reason)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _handle_failed_recv(
        self,
        pull_metas: dict[ReqId, PullReqMeta],
        req_ids: Collection[ReqId],
        reason: str,
    ) -> None:
        """Report a failed remote KV load so the scheduler can fail or recompute it."""
        failed: list[ReqId] = []
        for req_id in req_ids:
            pull_meta = pull_metas.pop(req_id, None)
            if pull_meta is None:
                continue
            if pull_meta.failed:
                self._complete_pull_task(pull_meta)
                continue
            pull_meta.failed = True
            failed.append(req_id)
            self.xfer_stats.record_failed_recv()

            invalid = {b for group in pull_meta.local_block_ids for b in group}
            if not invalid:
                # A pull with no local blocks only asks P to release its blocks
                # for a request that never reached the scheduler (see
                # AsyncLLM.notify_kv_transfer_request_rejected, which submits an
                # abort_immediately request just to run request_finished). No D
                # request is waiting on a load, and reporting one here would trip
                # the scheduler's `assert req_id in self.requests`.
                self._complete_pull_task(pull_meta)
                continue
            if self._is_hma_required:
                self._failed_recv_reqs.put(pull_meta.d_req_id)
            else:
                self._invalid_block_ids.put(invalid)
            self._complete_pull_task(pull_meta)

        if failed:
            logger.error("pulling kv_caches for %s failed: %s", failed, reason)
```


---

### 🔹 Commit #02: `143ee3b4`
- **完整 Hash**: `143ee3b4c9eb7fd25b5343cf3d2621a0f1bfa7c7`
- **說明 (Ground Truth)**: [Misc] Fix pre-commit failure on main from conflicts between pluggable KV cache and Step5 (#62593)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/models/step5/nvidia/sparse_attention.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:100, E:103, A:0) ➔ After(N:100, E:103, A:0)
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

### 🔹 函式: `Step5DSAMetadataBuilder._plan_prefill()`
- **變更前簽章 (Before)**: `def _plan_prefill(self, metadata, common) -> None` (L213~L253)
- **變更後簽章 (After)**: `def _plan_prefill(self, metadata, common) -> None` (L212~L252)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _plan_prefill(self, metadata, common) -> None:
        """Plan prefill steps here, before the forward, so the forward has no
        host sync: host lengths come from the scheduler and exact positions
        stay on device. Uniform (decode and MTP verify) batches need no plan.
        """
        layer = self._layer()
        impl = getattr(layer, "impl", None)
        n, reqs, query_len = (
            common.num_actual_tokens,
            common.num_reqs,
            common.max_query_len,
        )
        if (
            impl is None
            or impl.adapter is None
            or impl.summary_cache is None
            or not n
            or common.seq_lens_cpu_upper_bound is None
            or (n == reqs * query_len and query_len <= impl.num_speculative_tokens + 1)
        ):
            return
        # Upper bounds are exact without speculative decoding.
        positions = common.positions[:n] if impl.num_speculative_tokens else None
        if impl.num_speculative_tokens and common.positions is None:
            return
        spec = cast(AttentionSpec, self.kv_cache_spec)
        metadata.step5_runtime = impl.plan_prefill_step(
            metadata,
            n,
            common.seq_lens_cpu_upper_bound[:reqs].numpy(),
            _PrefillLayout(
                impl.num_heads // spec.num_kv_heads,
                spec.head_size,
                spec.num_kv_heads,
                self.vllm_config.model_config.dtype,
                is_quantized_kv_cache(impl.kv_cache_dtype),
                spec.block_size,
                kv_page_stride(layer.kv_cache),
            ),
            positions,
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _plan_prefill(self, metadata, common) -> None:
        """Plan prefill steps here, before the forward, so the forward has no
        host sync: host lengths come from the scheduler and exact positions
        stay on device. Uniform (decode and MTP verify) batches need no plan.
        """
        layer = self._layer()
        impl = getattr(layer, "impl", None)
        n, reqs, query_len = (
            common.num_actual_tokens,
            common.num_reqs,
            common.max_query_len,
        )
        if (
            impl is None
            or impl.adapter is None
            or impl.summary_cache is None
            or not n
            or common.seq_lens_cpu_upper_bound is None
            or (n == reqs * query_len and query_len <= impl.num_speculative_tokens + 1)
        ):
            return
        # Upper bounds are exact without speculative decoding.
        positions = common.positions[:n] if impl.num_speculative_tokens else None
        if impl.num_speculative_tokens and common.positions is None:
            return
        spec = cast(AttentionSpec, self.kv_cache_spec)
        metadata.step5_runtime = impl.plan_prefill_step(
            metadata,
            n,
            common.seq_lens_cpu_upper_bound[:reqs].numpy(),
            _PrefillLayout(
                impl.num_heads // spec.num_kv_heads,
                spec.head_size,
                spec.num_kv_heads,
                cast(torch.dtype, self.vllm_config.model_config.dtype),
                is_quantized_kv_cache(impl.kv_cache_dtype),
                spec.block_size,
                kv_page_stride(layer.kv_cache),
            ),
            positions,
        )
```


---

### 🔹 Commit #03: `17dd7d8f`
- **完整 Hash**: `17dd7d8fdd76f83384721bab790a32631813347f`
- **說明 (Ground Truth)**: [Bugfix][AuxOutput] Send routed-experts block hashes only for computed or scheduled blocks (#62489)
- **變更檔案數**: 2

#### 📄 檔案: `vllm/distributed/aux_output_connector/connector.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:14, E:9, A:0) ➔ After(N:14, E:10, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 3, -Edges: 2, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `AuxOutputSchedulerConnector._take_new_hashes` (FUNCTION_DEF)
  • - [移除節點] `AuxOutputSchedulerConnector._pack_new_hashes` (FUNCTION_DEF)
  • + [新增呼叫邊] `AuxOutputSchedulerConnector.build_connector_meta` ──[CALLS]──> `AuxOutputSchedulerConnector._take_new_hashes`
  • + [新增呼叫邊] `AuxOutputSchedulerConnector.request_finished` ──[CALLS]──> `AuxOutputSchedulerConnector._take_new_hashes`
  • + [新增呼叫邊] `AuxOutputSchedulerConnector._take_new_hashes` ──[CALLS]──> `min (External/Unresolved)`
  • - [移除呼叫邊] `AuxOutputSchedulerConnector.build_connector_meta` ──[CALLS]──> `AuxOutputSchedulerConnector._pack_new_hashes`
  • - [移除呼叫邊] `AuxOutputSchedulerConnector.request_finished` ──[CALLS]──> `AuxOutputSchedulerConnector._pack_new_hashes`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `AuxOutputSchedulerConnector.request_finished()`
- **變更前簽章 (Before)**: `def request_finished(self, request: Request) -> None` (L135~L144)
- **變更後簽章 (After)**: `def request_finished(self, request: Request) -> None` (L135~L144)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def request_finished(self, request: Request) -> None:
        """Queue a request's terminal event and final block hashes."""
        request_id = request.request_id
        num_sent = self._sent_hash_counts.pop(request_id, None)
        if num_sent is None:
            return
        # The next metadata delivers this terminal event to the worker.
        self._finished_requests[request_id] = self._pack_new_hashes(
            request.block_hashes, num_sent
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def request_finished(self, request: Request) -> None:
        """Queue a request's terminal event and final block hashes."""
        request_id = request.request_id
        if request_id not in self._sent_hash_counts:
            return
        # The next metadata delivers this terminal event to the worker.
        self._finished_requests[request_id] = self._take_new_hashes(
            request, request.num_computed_tokens
        )
        del self._sent_hash_counts[request_id]
```

### 🔹 函式: `AuxOutputSchedulerConnector.build_connector_meta()`
- **變更前簽章 (Before)**: `def build_connector_meta( self, scheduler_output: SchedulerOutput, requests: dict[str, Request], ) -> AuxOutputConnectorMetadata` (L54~L103)
- **變更後簽章 (After)**: `def build_connector_meta( self, scheduler_output: SchedulerOutput, requests: dict[str, Request], ) -> AuxOutputConnectorMetadata` (L55~L103)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def build_connector_meta(
        self,
        scheduler_output: SchedulerOutput,
        requests: dict[str, Request],
    ) -> AuxOutputConnectorMetadata:
        """Build one step's incremental worker metadata."""
        scheduled_requests: dict[str, int] = {}
        block_hashes_by_request: dict[str, PackedBlockHashes] = {}
        for request_id in scheduler_output.num_scheduled_tokens:
            num_sent = self._sent_hash_counts.setdefault(request_id, 0)
            request = requests[request_id]
            packed = self._pack_new_hashes(request.block_hashes, num_sent)
            if packed is not None:
                block_hashes_by_request[request_id] = packed
            self._sent_hash_counts[request_id] = len(request.block_hashes)
            assert request.sampling_params is not None
            # A P/D prefiller may cut the prompt short of the requested start.
            scheduled_requests[request_id] = max(
                min(
                    request.sampling_params.routed_experts_prompt_start,
                    request.num_prompt_tokens,
                ),
                0 if request.num_output_tokens == 0 else request.num_tokens - 1,
            )
        # A settled token can complete a hash block after the next async schedule
        # was built. Send a hash-only update if the request was not rescheduled.
        if len(self._sent_hash_counts) != len(scheduled_requests):
            for request_id, num_sent in self._sent_hash_counts.items():
                if request_id in scheduled_requests:
                    continue
                request = requests[request_id]
                packed = self._pack_new_hashes(request.block_hashes, num_sent)
                if packed is None:
                    continue
                block_hashes_by_request[request_id] = packed
                self._sent_hash_counts[request_id] = len(request.block_hashes)
        # Sending transfers ownership of these one-shot events.
        finished_requests = tuple(self._finished_requests)
        block_hashes_by_request.update(
            (request_id, block_hashes)
            for request_id, block_hashes in self._finished_requests.items()
            if block_hashes is not None
        )
        self._finished_requests = {}
        return AuxOutputConnectorMetadata(
            self._generation,
            scheduled_requests,
            block_hashes_by_request,
            finished_requests,
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def build_connector_meta(
        self,
        scheduler_output: SchedulerOutput,
        requests: dict[str, Request],
    ) -> AuxOutputConnectorMetadata:
        """Build one step's incremental worker metadata."""
        scheduled_requests: dict[str, int] = {}
        block_hashes_by_request: dict[str, PackedBlockHashes] = {}
        for request_id, num_tokens in scheduler_output.num_scheduled_tokens.items():
            self._sent_hash_counts.setdefault(request_id, 0)
            request = requests[request_id]
            packed = self._take_new_hashes(
                request, request.num_computed_tokens + num_tokens
            )
            if packed is not None:
                block_hashes_by_request[request_id] = packed
            assert request.sampling_params is not None
            # A P/D prefiller may cut the prompt short of the requested start.
            scheduled_requests[request_id] = max(
                min(
                    request.sampling_params.routed_experts_prompt_start,
                    request.num_prompt_tokens,
                ),
                0 if request.num_output_tokens == 0 else request.num_tokens - 1,
            )
        # A settled token can complete a hash block after the next async schedule
        # was built. Send a hash-only update if the request was not rescheduled.
        if len(self._sent_hash_counts) != len(scheduled_requests):
            for request_id in self._sent_hash_counts:
                if request_id in scheduled_requests:
                    continue
                request = requests[request_id]
                packed = self._take_new_hashes(request, request.num_computed_tokens)
                if packed is not None:
                    block_hashes_by_request[request_id] = packed
        # Sending transfers ownership of these one-shot events.
        finished_requests = tuple(self._finished_requests)
        block_hashes_by_request.update(
            (request_id, block_hashes)
            for request_id, block_hashes in self._finished_requests.items()
            if block_hashes is not None
        )
        self._finished_requests = {}
        return AuxOutputConnectorMetadata(
            self._generation,
            scheduled_requests,
            block_hashes_by_request,
            finished_requests,
        )
```

### 🔹 函式: `AuxOutputSchedulerConnector.__init__()`
- **變更前簽章 (Before)**: `def __init__(self) -> None: # Number of hashes already sent to the worker for each active request.` (L47~L52)
- **變更後簽章 (After)**: `def __init__(self, hash_block_size: int) -> None` (L47~L53)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(self) -> None:
        # Number of hashes already sent to the worker for each active request.
        self._sent_hash_counts: dict[str, int] = {}
        # Terminal events are delivered with the next connector metadata.
        self._finished_requests: dict[str, PackedBlockHashes | None] = {}
        self._generation = 0
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(self, hash_block_size: int) -> None:
        self._hash_block_size = hash_block_size
        # Number of hashes already sent to the worker for each active request.
        self._sent_hash_counts: dict[str, int] = {}
        # Terminal events are delivered with the next connector metadata.
        self._finished_requests: dict[str, PackedBlockHashes | None] = {}
        self._generation = 0
```


#### 📄 檔案: `vllm/v1/core/sched/scheduler.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:226, E:326, A:0) ➔ After(N:226, E:326, A:0)
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

### 🔹 函式: `Scheduler.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, vllm_config: VllmConfig, kv_cache_config: KVCacheConfig, structured_output_manager: StructuredOutputManager, block_size: int, hash_block_size: int | None = None, mm_registry: MultiModalRegistry = MULTIMODAL_REGISTRY, include_finished_set: bool = False, log_stats: bool = False, ) -> None` (L85~L471)
- **變更後簽章 (After)**: `def __init__( self, vllm_config: VllmConfig, kv_cache_config: KVCacheConfig, structured_output_manager: StructuredOutputManager, block_size: int, hash_block_size: int | None = None, mm_registry: MultiModalRegistry = MULTIMODAL_REGISTRY, include_finished_set: bool = False, log_stats: bool = False, ) -> None` (L85~L471)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        vllm_config: VllmConfig,
        kv_cache_config: KVCacheConfig,
        structured_output_manager: StructuredOutputManager,
        block_size: int,
        hash_block_size: int | None = None,
        mm_registry: MultiModalRegistry = MULTIMODAL_REGISTRY,
        include_finished_set: bool = False,
        log_stats: bool = False,
    ) -> None:
        self.vllm_config = vllm_config
        self.scheduler_config = vllm_config.scheduler_config
        self.cache_config = vllm_config.cache_config
        self.lora_config = vllm_config.lora_config
        self.model_uses_mrope = vllm_config.model_config.uses_mrope
        self.kv_cache_config = kv_cache_config
        self.kv_events_config = vllm_config.kv_events_config
        self.parallel_config = vllm_config.parallel_config
        self.log_stats = log_stats
        self.observability_config = vllm_config.observability_config
        self.spec_decode_metrics_level = (
            self.observability_config.per_request_spec_decode_metrics
        )
        self.kv_metrics_collector: KVCacheMetricsCollector | None = None
        if self.observability_config.kv_cache_metrics:
            self.kv_metrics_collector = KVCacheMetricsCollector(
                self.observability_config.kv_cache_metrics_sample,
            )
        self.structured_output_manager = structured_output_manager
        self.is_encoder_decoder = vllm_config.model_config.is_encoder_decoder
        self.is_mm_encoder_only = vllm_config.is_mm_encoder_only

        # include_finished_set controls whether a separate set of finished
        # request ids should be included in the EngineCoreOutputs returned
        # by update_from_outputs(). This is currently used in the multi-engine
        # case to track request lifetimes efficiently.
        self.finished_req_ids_dict: dict[int, set[str]] | None = (
            defaultdict(set) if include_finished_set else None
        )
        # Track requests scheduled in prior step (MRV1-only).
        self.prev_step_scheduled_req_ids: set[str] = set()

        # Scheduling constraints.
        self.max_num_running_reqs = self.scheduler_config.max_num_seqs
        # Admission into RUNNING. Separate from max_num_running_reqs, which
        # is the model-runner slot count.
        self.max_num_active_reqs = (
            self.scheduler_config.max_num_active_seqs
            if self.scheduler_config.max_num_active_seqs is not None
            else self.max_num_running_reqs
        )
        self.max_num_scheduled_tokens = (
            self.scheduler_config.max_num_scheduled_tokens
            if self.scheduler_config.max_num_scheduled_tokens is not None
            else self.scheduler_config.max_num_batched_tokens
        )
        self.adaptive_long_prefill_threshold = (
            self.scheduler_config.long_prefill_token_threshold_adaptive
        )
        self.max_model_len = vllm_config.model_config.max_model_len
        self.enable_kv_cache_events = (
            self.kv_events_config is not None
            and self.kv_events_config.enable_kv_cache_events
        )
        # Pooling and diffusion models do not append a sampled token after
        # prefill, so they should not reserve one context slot while scheduling.
        self.num_sampled_tokens_per_step = (
            0
            if (
                vllm_config.model_config.runner_type == "pooling"
                or vllm_config.model_config.is_diffusion
            )
            else 1
        )

        # Create KVConnector for the Scheduler. Note that each Worker
        # will have a corresponding KVConnector with Role=WORKER.
        # KV Connector pushes/pull of remote KVs for P/D and offloading.
        self.connector = None
        self.connector_prefix_cache_stats: PrefixCacheStats | None = None
        self.recompute_kv_load_failures = True
        self.defer_block_free = False
        # Whether a preempted request's in-flight output must be dropped; see
        # KVConnectorBase_V1.requires_kv_delivery.
        self.requires_kv_delivery = False
        kv_transfer_config = self.vllm_config.kv_transfer_config
        if kv_transfer_config is not None:
            assert not self.is_encoder_decoder, (
                "Encoder-decoder models are not currently supported with KV connectors"
            )
            self.connector = KVConnectorFactory.create_connector(
                config=self.vllm_config,
                role=KVConnectorRole.SCHEDULER,
                kv_cache_config=self.kv_cache_config,
            )
            if self.log_stats:
                self.connector_prefix_cache_stats = PrefixCacheStats()
            kv_load_failure_policy = kv_transfer_config.kv_load_failure_policy
            self.recompute_kv_load_failures = kv_load_failure_policy == "recompute"

            # With overlapping batches (async scheduling or PP), a step may
            # still be writing a freed request's KV blocks. A consumer KV
            # Connector can reallocate and fill those blocks via a load that
            # isn't ordered against that write, so defer freeing them.
            multiple_inflight_batches = self.vllm_config.max_concurrent_batches > 1
            if multiple_inflight_batches and kv_transfer_config.is_kv_consumer:
                self.defer_block_free = True

            self.requires_kv_delivery = self.connector.requires_kv_delivery

        self.kv_event_publisher = EventPublisherFactory.create(
            self.kv_events_config,
            self.parallel_config.data_parallel_index,
        )
        self.ec_connector = None
        if self.vllm_config.ec_transfer_config is not None:
            self.ec_connector = ECConnectorFactory.create_connector(
                config=self.vllm_config, role=ECConnectorRole.SCHEDULER
            )

        num_gpu_blocks = self.cache_config.num_gpu_blocks
        assert num_gpu_blocks is not None and num_gpu_blocks > 0

        self.block_size = block_size
        self.dcp_world_size = vllm_config.parallel_config.decode_context_parallel_size
        self.pcp_world_size = vllm_config.parallel_config.prefill_context_parallel_size

        # req_id -> Request
        self.requests: dict[str, Request] = {}
        # Scheduling policy
        try:
            self.policy = SchedulingPolicy(self.scheduler_config.policy)
        except ValueError as e:
            raise ValueError(
                f"Unknown scheduling policy: {self.scheduler_config.policy}"
            ) from e
        # Priority queues for requests.
        self.waiting = create_request_queue(self.policy)
        # Waiting requests that hold KV blocks are always drained before
        # self.waiting: a block-holder must never sit behind a request whose
        # failed allocation would stop the scheduling scan.
        self.kv_holding_waiting = create_request_queue(self.policy)
        # Waiting requests that are deferred, i.e. were skipped by the scheduling
        # scan or enqueued in a blocked status.
        self.deferred_waiting: set[Request] = set()
        self.running: list[Request] = []

        # The request IDs that are finished in between the previous and the
        # current steps. This is used to notify the workers about the finished
        # requests so that they can free the cached states for those requests.
        # This is flushed at the end of each scheduling step.
        self.finished_req_ids: set[str] = set()

        # IDs of requests preempted since the last call to schedule().
        self.reset_preempted_req_ids: set[str] = set()

        # Counter for requests waiting for streaming input. Used to calculate
        # number of unfinished requests
        self.num_waiting_for_streaming_input: int = 0

        # KV Connector: requests in process of async KV loading or recving
        self.finished_recving_kv_req_ids: set[str] = set()
        self.failed_recving_kv_req_ids: set[str] = set()

        # Grammar compilation failures to finish as per-request errors in
        # update_from_output.
        self.grammar_compile_error_reqs: set[str] = set()
        self.encoder_cache_mismatch_reqs: set[str] = set()

        # Encoder-related.
        # Calculate encoder cache size if applicable
        supports_mm_inputs = vllm_config.model_config.supports_multimodal_inputs
        mm_budget = (
            MultiModalBudget(vllm_config, mm_registry) if supports_mm_inputs else None
        )

        # NOTE: Text-only encoder-decoder models are implemented as
        # multi-modal models for convenience
        # Example: https://github.com/vllm-project/bart-plugin
        if self.is_encoder_decoder:
            assert mm_budget and len(mm_budget.mm_max_toks_per_item) <= 1, (
                "Encoder-decoder models are expected to implement the "
                "multimodal interface with at most one modality."
            )

        self.max_num_encoder_input_tokens = (
            mm_budget.encoder_compute_budget if mm_budget else 0
        )
        encoder_cache_size = mm_budget.encoder_cache_size if mm_budget else 0
        manager_cls_obj = vllm_config.ec_manager_config.get_encoder_cache_manager_obj()
        if manager_cls_obj is None:
            manager_cls_obj = (
                EncoderDecoderCacheManager
                if self.is_encoder_decoder
                else EncoderCacheManager
            )
        self.encoder_cache_manager = manager_cls_obj.create_manager(
            cache_size=encoder_cache_size, vllm_config=vllm_config
        )
        speculative_config = vllm_config.speculative_config
        self.use_eagle = False
        self.use_eagle_block_drop = False
        self.num_spec_tokens = vllm_config.num_speculative_tokens
        self.num_lookahead_tokens = vllm_config.num_lookahead_tokens
        # DSV41 SWA bounded replay: groups that declare a replay window are rebuilt
        # after a prefix hit by recomputing its trailing tokens. One window
        # for all such groups, so the rewind matches every group's allocation.
        self.prefix_replay_group_ids = tuple(
            group_id
            for group_id, group in enumerate(kv_cache_config.kv_cache_groups)
            if group.kv_cache_spec.prefix_replay_tokens > 0
        )
        replay_windows = {
            kv_cache_config.kv_cache_groups[group_id].kv_cache_spec.prefix_replay_tokens
            for group_id in self.prefix_replay_group_ids
        }
        assert len(replay_windows) <= 1, (
            f"Prefix replay windows should agree: {sorted(replay_windows)}"
        )
        self.prefix_replay_tokens = replay_windows.pop() if replay_windows else 0
        self.num_prefill_lookahead = vllm_config.num_prefill_lookahead_tokens
        self.dynamic_sd_lookup: list[int] | None = None
        if speculative_config is not None:
            if speculative_config.num_speculative_tokens_per_batch_size:
                self.dynamic_sd_lookup = build_dynamic_sd_schedule_lookup(
                    speculative_config.num_speculative_tokens_per_batch_size,
                    vllm_max_batch_size=self.scheduler_config.max_num_seqs,
                    vllm_num_speculative_tokens=self.num_spec_tokens,
                )
            self.use_eagle = speculative_config.use_eagle()
            self.use_eagle_block_drop = speculative_config.use_eagle_block_drop()
            if self.use_eagle and not self.use_eagle_block_drop:
                logger.warning(
                    "EAGLE trailing prefix-cache block dropping is disabled. "
                    "This is experimental and may affect speculative-token "
                    "acceptance rates."
                )

        # Create the KV cache manager.
        if hash_block_size is None:
            hash_block_size = block_size
        self.hash_block_size = hash_block_size
        self.kv_cache_manager = KVCacheManager(
            kv_cache_config=kv_cache_config,
            max_model_len=self.max_model_len,
            max_in_flight_tokens=vllm_config.max_in_flight_tokens,
            enable_caching=self.cache_config.enable_prefix_caching,
            use_eagle=self.use_eagle_block_drop,
            num_prefill_lookahead=self.num_prefill_lookahead,
            log_stats=self.log_stats,
            enable_kv_cache_events=self.enable_kv_cache_events,
            dcp_world_size=self.dcp_world_size,
            pcp_world_size=1,
            scheduler_block_size=self.block_size,
            hash_block_size=hash_block_size,
            metrics_collector=self.kv_metrics_collector,
            watermark=self.scheduler_config.watermark,
            enable_mamba_shared_prefix_checkpoint=(
                self.cache_config.enable_mamba_shared_prefix_checkpoint
            ),
        )
        # Mamba managers already account for their speculative state blocks.
        num_spec_decode_tokens = (
            1 + self.num_spec_tokens + self.num_lookahead_tokens
            if self.num_spec_tokens
            else 0
        )
        self._spec_decode_step_blocks = sum(
            cdiv(num_spec_decode_tokens, manager.block_size)
            for manager in self.kv_cache_manager.coordinator.single_type_managers
            if not isinstance(manager.kv_cache_spec, MambaSpec)
        )
        # Bind after construction so connectors can access the cache manager.
        if self.connector is not None:
            self.connector.bind_kv_cache_manager(self.kv_cache_manager)

        self.use_pp = self.parallel_config.pipeline_parallel_size > 1
        self.use_v2_model_runner = vllm_config.use_v2_model_runner
        # Scheduler iteration counter. Drives the V2+PP+async decode-throttle
        # cadence (`next_decode_eligible_step`).
        self.current_step = 0
        # DP prefill balancing: Flag to track whether the last cadence-aligned
        # prefill batch fully drained the waiting queue. Prefill throttling
        # is disabled in this case.
        self.prefill_capacity_bound = False
        # The DP engine core drives this cadence from a counter shared across
        # ranks; an engine without one never throttles, so apply the interval
        # locally, timed from the last prefill-carrying step. Three regimes:
        #   1. no DP -- local cadence applies;
        #   2. dense DP rank -- `reconfigure_for_independent_dp_rank` already
        #      set data_parallel_size=1, so each rank gets its own cadence.
        #      Intended, but a behaviour change: this used to be a no-op;
        #   3. MoE DP rank (size > 1) -- the engine core drives it, no-op here.
        self.local_prefill_interval = (
            self.scheduler_config.prefill_schedule_interval
            if self.parallel_config.data_parallel_size == 1
            else 1
        )
        if self.local_prefill_interval > 1:
            # Neither the hold nor its release is otherwise visible in logs or
            # stats, which makes a misapplied cadence hard to diagnose.
            logger.info_once(
                "Prefill cadence: applying prefill_schedule_interval=%d "
                "locally (this engine is not DP-coordinated); prefill is held "
                "until %d executed steps have passed since the last "
                "prefill-carrying step.",
                self.local_prefill_interval,
                self.local_prefill_interval,
            )
        # A full interval back, so the first step is never gated.
        self.last_prefill_step = -self.local_prefill_interval
        # Steps that actually scheduled tokens. `current_step` counts every
        # schedule() call including empty ones, so it would expire the hold
        # early; it keeps its own meaning (next_decode_eligible_step).
        self.num_executed_steps = 0
        self.scheduler_reserve_full_isl = (
            self.scheduler_config.scheduler_reserve_full_isl
        )

        self.has_mamba_layers = kv_cache_config.has_mamba_layers
        self.needs_kv_cache_zeroing = kv_cache_config.needs_kv_cache_zeroing
        self.need_mamba_block_aligned_split = (
            self.has_mamba_layers and self.cache_config.mamba_cache_mode == "align"
        )
        # TODO: Support models with multiple Mamba specs that require different
        # prefill checkpoint alignments instead of selecting the first one.
        self.mamba_prefill_checkpoint_alignment = next(
            (
                group.kv_cache_spec.prefill_checkpoint_alignment
                for group in kv_cache_config.kv_cache_groups
                if isinstance(group.kv_cache_spec, MambaSpec)
            ),
            None,
        )
        self.mamba_has_prefill_checkpoint_blocks = self.has_mamba_layers and all(
            not isinstance(group.kv_cache_spec, MambaSpec)
            or group.kv_cache_spec.num_prefill_checkpoint_blocks > 0
            for group in kv_cache_config.kv_cache_groups
        )
        # Fine-grained hits reuse the prompt's hash-aligned Mamba checkpoint.
        # Split there only if the backend cannot save it within the final chunk.
        self.mamba_partial_cache_hit = (
            self.need_mamba_block_aligned_split
            and self.hash_block_size < self.block_size
            and self.kv_cache_manager.coordinator.enable_partial_hash_hits
        )
        # Opt-in: also stop at the junction, where an eagle sibling resumes. The
        # manager decides whether it can check-point there (per-group eagle bit,
        # no MTP re-prefill tail); splitting for a stop it would refuse costs a
        # forward pass and displaces the block-boundary stop.
        self.mamba_shared_prefix_checkpoint = (
            self.mamba_partial_cache_hit
            and self.kv_cache_manager.mamba_shared_prefix_checkpoint
        )

        # Counts of non-empty steps scheduled / processed. update_from_output
        # is called once per scheduled step in FIFO order, so these stay in sync.
        self.sched_step_seq = 0
        self.processed_step_seq = 0
        # FIFO of (fence_seq, blocks): blocks become safe to free once
        # processed_step_seq >= fence_seq.
        self.deferred_frees: deque[tuple[int, list[KVCacheBlock]]] = deque()

        self.perf_metrics: ModelMetrics | None = None
        if self.log_stats and vllm_config.observability_config.enable_mfu_metrics:
            self.perf_metrics = ModelMetrics(vllm_config)

        self.aux_output_connector = (
            AuxOutputSchedulerConnector()
            if vllm_config.aux_output_config.enabled
            else None
        )
        self.return_sampling_mask = vllm_config.model_config.return_sampling_mask

        self._pause_state: PauseState = PauseState.UNPAUSED

        # In-flight requests still prefilling (prefill chunks + in-progress
        # async KV loads). Their remaining-block reservation gates async loads.
        self._inflight_prefills: set[Request] = set()

        # Requests with an async KV load, by stage (KV_FETCH_STAGES).
        # None when not tracked (stats disabled or no KV connector).
        self._kv_fetch_stages: dict[Request, str] | None = (
            {} if self.log_stats and self.connector is not None else None
        )
        self._kv_fetch_counts: dict[str, int] = dict.fromkeys(KV_FETCH_STAGES, 0)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        vllm_config: VllmConfig,
        kv_cache_config: KVCacheConfig,
        structured_output_manager: StructuredOutputManager,
        block_size: int,
        hash_block_size: int | None = None,
        mm_registry: MultiModalRegistry = MULTIMODAL_REGISTRY,
        include_finished_set: bool = False,
        log_stats: bool = False,
    ) -> None:
        self.vllm_config = vllm_config
        self.scheduler_config = vllm_config.scheduler_config
        self.cache_config = vllm_config.cache_config
        self.lora_config = vllm_config.lora_config
        self.model_uses_mrope = vllm_config.model_config.uses_mrope
        self.kv_cache_config = kv_cache_config
        self.kv_events_config = vllm_config.kv_events_config
        self.parallel_config = vllm_config.parallel_config
        self.log_stats = log_stats
        self.observability_config = vllm_config.observability_config
        self.spec_decode_metrics_level = (
            self.observability_config.per_request_spec_decode_metrics
        )
        self.kv_metrics_collector: KVCacheMetricsCollector | None = None
        if self.observability_config.kv_cache_metrics:
            self.kv_metrics_collector = KVCacheMetricsCollector(
                self.observability_config.kv_cache_metrics_sample,
            )
        self.structured_output_manager = structured_output_manager
        self.is_encoder_decoder = vllm_config.model_config.is_encoder_decoder
        self.is_mm_encoder_only = vllm_config.is_mm_encoder_only

        # include_finished_set controls whether a separate set of finished
        # request ids should be included in the EngineCoreOutputs returned
        # by update_from_outputs(). This is currently used in the multi-engine
        # case to track request lifetimes efficiently.
        self.finished_req_ids_dict: dict[int, set[str]] | None = (
            defaultdict(set) if include_finished_set else None
        )
        # Track requests scheduled in prior step (MRV1-only).
        self.prev_step_scheduled_req_ids: set[str] = set()

        # Scheduling constraints.
        self.max_num_running_reqs = self.scheduler_config.max_num_seqs
        # Admission into RUNNING. Separate from max_num_running_reqs, which
        # is the model-runner slot count.
        self.max_num_active_reqs = (
            self.scheduler_config.max_num_active_seqs
            if self.scheduler_config.max_num_active_seqs is not None
            else self.max_num_running_reqs
        )
        self.max_num_scheduled_tokens = (
            self.scheduler_config.max_num_scheduled_tokens
            if self.scheduler_config.max_num_scheduled_tokens is not None
            else self.scheduler_config.max_num_batched_tokens
        )
        self.adaptive_long_prefill_threshold = (
            self.scheduler_config.long_prefill_token_threshold_adaptive
        )
        self.max_model_len = vllm_config.model_config.max_model_len
        self.enable_kv_cache_events = (
            self.kv_events_config is not None
            and self.kv_events_config.enable_kv_cache_events
        )
        # Pooling and diffusion models do not append a sampled token after
        # prefill, so they should not reserve one context slot while scheduling.
        self.num_sampled_tokens_per_step = (
            0
            if (
                vllm_config.model_config.runner_type == "pooling"
                or vllm_config.model_config.is_diffusion
            )
            else 1
        )

        # Create KVConnector for the Scheduler. Note that each Worker
        # will have a corresponding KVConnector with Role=WORKER.
        # KV Connector pushes/pull of remote KVs for P/D and offloading.
        self.connector = None
        self.connector_prefix_cache_stats: PrefixCacheStats | None = None
        self.recompute_kv_load_failures = True
        self.defer_block_free = False
        # Whether a preempted request's in-flight output must be dropped; see
        # KVConnectorBase_V1.requires_kv_delivery.
        self.requires_kv_delivery = False
        kv_transfer_config = self.vllm_config.kv_transfer_config
        if kv_transfer_config is not None:
            assert not self.is_encoder_decoder, (
                "Encoder-decoder models are not currently supported with KV connectors"
            )
            self.connector = KVConnectorFactory.create_connector(
                config=self.vllm_config,
                role=KVConnectorRole.SCHEDULER,
                kv_cache_config=self.kv_cache_config,
            )
            if self.log_stats:
                self.connector_prefix_cache_stats = PrefixCacheStats()
            kv_load_failure_policy = kv_transfer_config.kv_load_failure_policy
            self.recompute_kv_load_failures = kv_load_failure_policy == "recompute"

            # With overlapping batches (async scheduling or PP), a step may
            # still be writing a freed request's KV blocks. A consumer KV
            # Connector can reallocate and fill those blocks via a load that
            # isn't ordered against that write, so defer freeing them.
            multiple_inflight_batches = self.vllm_config.max_concurrent_batches > 1
            if multiple_inflight_batches and kv_transfer_config.is_kv_consumer:
                self.defer_block_free = True

            self.requires_kv_delivery = self.connector.requires_kv_delivery

        self.kv_event_publisher = EventPublisherFactory.create(
            self.kv_events_config,
            self.parallel_config.data_parallel_index,
        )
        self.ec_connector = None
        if self.vllm_config.ec_transfer_config is not None:
            self.ec_connector = ECConnectorFactory.create_connector(
                config=self.vllm_config, role=ECConnectorRole.SCHEDULER
            )

        num_gpu_blocks = self.cache_config.num_gpu_blocks
        assert num_gpu_blocks is not None and num_gpu_blocks > 0

        self.block_size = block_size
        self.dcp_world_size = vllm_config.parallel_config.decode_context_parallel_size
        self.pcp_world_size = vllm_config.parallel_config.prefill_context_parallel_size

        # req_id -> Request
        self.requests: dict[str, Request] = {}
        # Scheduling policy
        try:
            self.policy = SchedulingPolicy(self.scheduler_config.policy)
        except ValueError as e:
            raise ValueError(
                f"Unknown scheduling policy: {self.scheduler_config.policy}"
            ) from e
        # Priority queues for requests.
        self.waiting = create_request_queue(self.policy)
        # Waiting requests that hold KV blocks are always drained before
        # self.waiting: a block-holder must never sit behind a request whose
        # failed allocation would stop the scheduling scan.
        self.kv_holding_waiting = create_request_queue(self.policy)
        # Waiting requests that are deferred, i.e. were skipped by the scheduling
        # scan or enqueued in a blocked status.
        self.deferred_waiting: set[Request] = set()
        self.running: list[Request] = []

        # The request IDs that are finished in between the previous and the
        # current steps. This is used to notify the workers about the finished
        # requests so that they can free the cached states for those requests.
        # This is flushed at the end of each scheduling step.
        self.finished_req_ids: set[str] = set()

        # IDs of requests preempted since the last call to schedule().
        self.reset_preempted_req_ids: set[str] = set()

        # Counter for requests waiting for streaming input. Used to calculate
        # number of unfinished requests
        self.num_waiting_for_streaming_input: int = 0

        # KV Connector: requests in process of async KV loading or recving
        self.finished_recving_kv_req_ids: set[str] = set()
        self.failed_recving_kv_req_ids: set[str] = set()

        # Grammar compilation failures to finish as per-request errors in
        # update_from_output.
        self.grammar_compile_error_reqs: set[str] = set()
        self.encoder_cache_mismatch_reqs: set[str] = set()

        # Encoder-related.
        # Calculate encoder cache size if applicable
        supports_mm_inputs = vllm_config.model_config.supports_multimodal_inputs
        mm_budget = (
            MultiModalBudget(vllm_config, mm_registry) if supports_mm_inputs else None
        )

        # NOTE: Text-only encoder-decoder models are implemented as
        # multi-modal models for convenience
        # Example: https://github.com/vllm-project/bart-plugin
        if self.is_encoder_decoder:
            assert mm_budget and len(mm_budget.mm_max_toks_per_item) <= 1, (
                "Encoder-decoder models are expected to implement the "
                "multimodal interface with at most one modality."
            )

        self.max_num_encoder_input_tokens = (
            mm_budget.encoder_compute_budget if mm_budget else 0
        )
        encoder_cache_size = mm_budget.encoder_cache_size if mm_budget else 0
        manager_cls_obj = vllm_config.ec_manager_config.get_encoder_cache_manager_obj()
        if manager_cls_obj is None:
            manager_cls_obj = (
                EncoderDecoderCacheManager
                if self.is_encoder_decoder
                else EncoderCacheManager
            )
        self.encoder_cache_manager = manager_cls_obj.create_manager(
            cache_size=encoder_cache_size, vllm_config=vllm_config
        )
        speculative_config = vllm_config.speculative_config
        self.use_eagle = False
        self.use_eagle_block_drop = False
        self.num_spec_tokens = vllm_config.num_speculative_tokens
        self.num_lookahead_tokens = vllm_config.num_lookahead_tokens
        # DSV41 SWA bounded replay: groups that declare a replay window are rebuilt
        # after a prefix hit by recomputing its trailing tokens. One window
        # for all such groups, so the rewind matches every group's allocation.
        self.prefix_replay_group_ids = tuple(
            group_id
            for group_id, group in enumerate(kv_cache_config.kv_cache_groups)
            if group.kv_cache_spec.prefix_replay_tokens > 0
        )
        replay_windows = {
            kv_cache_config.kv_cache_groups[group_id].kv_cache_spec.prefix_replay_tokens
            for group_id in self.prefix_replay_group_ids
        }
        assert len(replay_windows) <= 1, (
            f"Prefix replay windows should agree: {sorted(replay_windows)}"
        )
        self.prefix_replay_tokens = replay_windows.pop() if replay_windows else 0
        self.num_prefill_lookahead = vllm_config.num_prefill_lookahead_tokens
        self.dynamic_sd_lookup: list[int] | None = None
        if speculative_config is not None:
            if speculative_config.num_speculative_tokens_per_batch_size:
                self.dynamic_sd_lookup = build_dynamic_sd_schedule_lookup(
                    speculative_config.num_speculative_tokens_per_batch_size,
                    vllm_max_batch_size=self.scheduler_config.max_num_seqs,
                    vllm_num_speculative_tokens=self.num_spec_tokens,
                )
            self.use_eagle = speculative_config.use_eagle()
            self.use_eagle_block_drop = speculative_config.use_eagle_block_drop()
            if self.use_eagle and not self.use_eagle_block_drop:
                logger.warning(
                    "EAGLE trailing prefix-cache block dropping is disabled. "
                    "This is experimental and may affect speculative-token "
                    "acceptance rates."
                )

        # Create the KV cache manager.
        if hash_block_size is None:
            hash_block_size = block_size
        self.hash_block_size = hash_block_size
        self.kv_cache_manager = KVCacheManager(
            kv_cache_config=kv_cache_config,
            max_model_len=self.max_model_len,
            max_in_flight_tokens=vllm_config.max_in_flight_tokens,
            enable_caching=self.cache_config.enable_prefix_caching,
            use_eagle=self.use_eagle_block_drop,
            num_prefill_lookahead=self.num_prefill_lookahead,
            log_stats=self.log_stats,
            enable_kv_cache_events=self.enable_kv_cache_events,
            dcp_world_size=self.dcp_world_size,
            pcp_world_size=1,
            scheduler_block_size=self.block_size,
            hash_block_size=hash_block_size,
            metrics_collector=self.kv_metrics_collector,
            watermark=self.scheduler_config.watermark,
            enable_mamba_shared_prefix_checkpoint=(
                self.cache_config.enable_mamba_shared_prefix_checkpoint
            ),
        )
        # Mamba managers already account for their speculative state blocks.
        num_spec_decode_tokens = (
            1 + self.num_spec_tokens + self.num_lookahead_tokens
            if self.num_spec_tokens
            else 0
        )
        self._spec_decode_step_blocks = sum(
            cdiv(num_spec_decode_tokens, manager.block_size)
            for manager in self.kv_cache_manager.coordinator.single_type_managers
            if not isinstance(manager.kv_cache_spec, MambaSpec)
        )
        # Bind after construction so connectors can access the cache manager.
        if self.connector is not None:
            self.connector.bind_kv_cache_manager(self.kv_cache_manager)

        self.use_pp = self.parallel_config.pipeline_parallel_size > 1
        self.use_v2_model_runner = vllm_config.use_v2_model_runner
        # Scheduler iteration counter. Drives the V2+PP+async decode-throttle
        # cadence (`next_decode_eligible_step`).
        self.current_step = 0
        # DP prefill balancing: Flag to track whether the last cadence-aligned
        # prefill batch fully drained the waiting queue. Prefill throttling
        # is disabled in this case.
        self.prefill_capacity_bound = False
        # The DP engine core drives this cadence from a counter shared across
        # ranks; an engine without one never throttles, so apply the interval
        # locally, timed from the last prefill-carrying step. Three regimes:
        #   1. no DP -- local cadence applies;
        #   2. dense DP rank -- `reconfigure_for_independent_dp_rank` already
        #      set data_parallel_size=1, so each rank gets its own cadence.
        #      Intended, but a behaviour change: this used to be a no-op;
        #   3. MoE DP rank (size > 1) -- the engine core drives it, no-op here.
        self.local_prefill_interval = (
            self.scheduler_config.prefill_schedule_interval
            if self.parallel_config.data_parallel_size == 1
            else 1
        )
        if self.local_prefill_interval > 1:
            # Neither the hold nor its release is otherwise visible in logs or
            # stats, which makes a misapplied cadence hard to diagnose.
            logger.info_once(
                "Prefill cadence: applying prefill_schedule_interval=%d "
                "locally (this engine is not DP-coordinated); prefill is held "
                "until %d executed steps have passed since the last "
                "prefill-carrying step.",
                self.local_prefill_interval,
                self.local_prefill_interval,
            )
        # A full interval back, so the first step is never gated.
        self.last_prefill_step = -self.local_prefill_interval
        # Steps that actually scheduled tokens. `current_step` counts every
        # schedule() call including empty ones, so it would expire the hold
        # early; it keeps its own meaning (next_decode_eligible_step).
        self.num_executed_steps = 0
        self.scheduler_reserve_full_isl = (
            self.scheduler_config.scheduler_reserve_full_isl
        )

        self.has_mamba_layers = kv_cache_config.has_mamba_layers
        self.needs_kv_cache_zeroing = kv_cache_config.needs_kv_cache_zeroing
        self.need_mamba_block_aligned_split = (
            self.has_mamba_layers and self.cache_config.mamba_cache_mode == "align"
        )
        # TODO: Support models with multiple Mamba specs that require different
        # prefill checkpoint alignments instead of selecting the first one.
        self.mamba_prefill_checkpoint_alignment = next(
            (
                group.kv_cache_spec.prefill_checkpoint_alignment
                for group in kv_cache_config.kv_cache_groups
                if isinstance(group.kv_cache_spec, MambaSpec)
            ),
            None,
        )
        self.mamba_has_prefill_checkpoint_blocks = self.has_mamba_layers and all(
            not isinstance(group.kv_cache_spec, MambaSpec)
            or group.kv_cache_spec.num_prefill_checkpoint_blocks > 0
            for group in kv_cache_config.kv_cache_groups
        )
        # Fine-grained hits reuse the prompt's hash-aligned Mamba checkpoint.
        # Split there only if the backend cannot save it within the final chunk.
        self.mamba_partial_cache_hit = (
            self.need_mamba_block_aligned_split
            and self.hash_block_size < self.block_size
            and self.kv_cache_manager.coordinator.enable_partial_hash_hits
        )
        # Opt-in: also stop at the junction, where an eagle sibling resumes. The
        # manager decides whether it can check-point there (per-group eagle bit,
        # no MTP re-prefill tail); splitting for a stop it would refuse costs a
        # forward pass and displaces the block-boundary stop.
        self.mamba_shared_prefix_checkpoint = (
            self.mamba_partial_cache_hit
            and self.kv_cache_manager.mamba_shared_prefix_checkpoint
        )

        # Counts of non-empty steps scheduled / processed. update_from_output
        # is called once per scheduled step in FIFO order, so these stay in sync.
        self.sched_step_seq = 0
        self.processed_step_seq = 0
        # FIFO of (fence_seq, blocks): blocks become safe to free once
        # processed_step_seq >= fence_seq.
        self.deferred_frees: deque[tuple[int, list[KVCacheBlock]]] = deque()

        self.perf_metrics: ModelMetrics | None = None
        if self.log_stats and vllm_config.observability_config.enable_mfu_metrics:
            self.perf_metrics = ModelMetrics(vllm_config)

        self.aux_output_connector = (
            AuxOutputSchedulerConnector(self.hash_block_size)
            if vllm_config.aux_output_config.enabled
            else None
        )
        self.return_sampling_mask = vllm_config.model_config.return_sampling_mask

        self._pause_state: PauseState = PauseState.UNPAUSED

        # In-flight requests still prefilling (prefill chunks + in-progress
        # async KV loads). Their remaining-block reservation gates async loads.
        self._inflight_prefills: set[Request] = set()

        # Requests with an async KV load, by stage (KV_FETCH_STAGES).
        # None when not tracked (stats disabled or no KV connector).
        self._kv_fetch_stages: dict[Request, str] | None = (
            {} if self.log_stats and self.connector is not None else None
        )
        self._kv_fetch_counts: dict[str, int] = dict.fromkeys(KV_FETCH_STAGES, 0)
```


---

### 🔹 Commit #04: `e1f31416`
- **完整 Hash**: `e1f3141647b93f12ac2ffa95f0cf7699fcaca21f`
- **說明 (Ground Truth)**: [Bugfix][V1] Null sliding-window block-table entries below the window (#60767)
- **變更檔案數**: 3

#### 📄 檔案: `vllm/v1/kv_cache_interface.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:156, E:158, A:0) ➔ After(N:157, E:158, A:0)
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
  • + [新增節點] `SlidingWindowSpec.num_retained_tokens` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `vllm/v1/worker/gpu/block_table.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:37, E:39, A:0) ➔ After(N:39, E:42, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 3, -Edges: 0, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `maximum (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `any (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `BlockTables.__init__` ──[CALLS]──> `any (External/Unresolved)`
  • + [新增呼叫邊] `_gather_block_tables_kernel` ──[CALLS]──> `where (External/Unresolved)`
  • + [新增呼叫邊] `_gather_block_tables_kernel` ──[CALLS]──> `maximum (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `BlockTables.gather_block_tables()`
- **變更前簽章 (Before)**: `def gather_block_tables( self, idx_mapping: torch.Tensor, num_reqs_padded: int, out: tuple[torch.Tensor, ...] | None = None, out_ptrs: torch.Tensor | None = None, ) -> tuple[torch.Tensor, ...]` (L146~L176)
- **變更後簽章 (After)**: `def gather_block_tables( self, idx_mapping: torch.Tensor, num_reqs_padded: int, out: tuple[torch.Tensor, ...] | None = None, out_ptrs: torch.Tensor | None = None, num_computed_tokens: torch.Tensor | None = None, ) -> tuple[torch.Tensor, ...]` (L160~L211)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def gather_block_tables(
        self,
        idx_mapping: torch.Tensor,
        num_reqs_padded: int,
        out: tuple[torch.Tensor, ...] | None = None,
        out_ptrs: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, ...]:
        if self.num_kv_cache_groups == 0:
            return ()
        num_reqs = idx_mapping.shape[0]
        num_rows = num_reqs_padded
        if out is None:
            out = tuple(self.input_block_tables)
            out_ptrs = self.input_block_table_ptrs
            num_rows = max(num_rows, self._num_dirty_rows)
            self._num_dirty_rows = num_reqs
        else:
            assert out_ptrs is not None
            assert len(out) == self.num_kv_cache_groups
        # Also clear rows left by a larger batch in the shared buffer.
        _gather_block_tables_kernel[(self.num_kv_cache_groups, num_rows)](
            idx_mapping,
            self.block_table_ptrs,
            out_ptrs,
            self.block_table_strides,
            self.num_blocks.gpu,
            self.num_blocks.gpu.stride(0),
            num_reqs,
            BLOCK_SIZE=1024,  # type: ignore
        )
        return tuple(bt[:num_reqs_padded] for bt in out)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def gather_block_tables(
        self,
        idx_mapping: torch.Tensor,
        num_reqs_padded: int,
        out: tuple[torch.Tensor, ...] | None = None,
        out_ptrs: torch.Tensor | None = None,
        num_computed_tokens: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, ...]:
        """Gather the batch's block-table rows into the forward-pass tables.

        When num_computed_tokens ([max_num_reqs], indexed like the block tables)
        is given, sliding-window groups get every entry wholly below the window
        of the request's first scheduled token replaced by the null block. Those
        blocks may already have been freed by the sliding-window manager and
        reused, while attention kernels can still load them as part of a KV
        tile that straddles the window start: masked-out NaN in such a tile
        propagates into the output.
        """
        if self.num_kv_cache_groups == 0:
            return ()
        mask_sliding_window = (
            self.has_sliding_window_groups and num_computed_tokens is not None
        )
        if not mask_sliding_window:
            # Unused by the kernel; any int32 tensor satisfies the signature.
            num_computed_tokens = self.sliding_window_reach
        num_reqs = idx_mapping.shape[0]
        num_rows = num_reqs_padded
        if out is None:
            out = tuple(self.input_block_tables)
            out_ptrs = self.input_block_table_ptrs
            num_rows = max(num_rows, self._num_dirty_rows)
            self._num_dirty_rows = num_reqs
        else:
            assert out_ptrs is not None
            assert len(out) == self.num_kv_cache_groups
        # Also clear rows left by a larger batch in the shared buffer.
        _gather_block_tables_kernel[(self.num_kv_cache_groups, num_rows)](
            idx_mapping,
            self.block_table_ptrs,
            out_ptrs,
            self.block_table_strides,
            self.num_blocks.gpu,
            self.num_blocks.gpu.stride(0),
            num_reqs,
            num_computed_tokens,
            self.sliding_window_reach,
            self.block_sizes_tensor,
            MASK_SLIDING_WINDOW=mask_sliding_window,
            BLOCK_SIZE=1024,  # type: ignore
        )
        return tuple(bt[:num_reqs_padded] for bt in out)
```

### 🔹 函式: `BlockTables.init_block_table_layout_tensors()`
- **變更前簽章 (Before)**: `def init_block_table_layout_tensors(self) -> None` (L94~L109)
- **變更後簽章 (After)**: `def init_block_table_layout_tensors(self) -> None` (L105~L123)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def init_block_table_layout_tensors(self) -> None:
        self.block_table_ptrs = self._make_ptr_tensor(
            [b.gpu for b in self.block_tables]
        )
        self.block_table_strides = torch.tensor(
            [b.gpu.stride(0) for b in self.block_tables],
            dtype=torch.int64,
            device=self.device,
        )
        self.block_sizes_tensor = torch.tensor(
            self.block_sizes, dtype=torch.int32, device=self.device
        )
        self.slot_mapping_enabled = torch.tensor(
            self._slot_mapping_enabled, dtype=torch.bool, device=self.device
        )
        self.input_block_table_ptrs = self._make_ptr_tensor(self.input_block_tables)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def init_block_table_layout_tensors(self) -> None:
        self.block_table_ptrs = self._make_ptr_tensor(
            [b.gpu for b in self.block_tables]
        )
        self.block_table_strides = torch.tensor(
            [b.gpu.stride(0) for b in self.block_tables],
            dtype=torch.int64,
            device=self.device,
        )
        self.block_sizes_tensor = torch.tensor(
            self.block_sizes, dtype=torch.int32, device=self.device
        )
        self.slot_mapping_enabled = torch.tensor(
            self._slot_mapping_enabled, dtype=torch.bool, device=self.device
        )
        self.sliding_window_reach = torch.tensor(
            self._sliding_window_reach, dtype=torch.int32, device=self.device
        )
        self.input_block_table_ptrs = self._make_ptr_tensor(self.input_block_tables)
```

### 🔹 函式: `BlockTables.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, block_sizes: list[int], max_num_reqs: int, max_num_batched_tokens: int, max_num_blocks_per_group: list[int], device: torch.device, cp_size: int = 1, cp_rank: int = 0, cp_interleave: int = 1, slot_mapping_enabled: list[bool] | None = None, dcp_sharded: list[bool] | None = None, )` (L21~L86)
- **變更後簽章 (After)**: `def __init__( self, block_sizes: list[int], max_num_reqs: int, max_num_batched_tokens: int, max_num_blocks_per_group: list[int], device: torch.device, cp_size: int = 1, cp_rank: int = 0, cp_interleave: int = 1, slot_mapping_enabled: list[bool] | None = None, dcp_sharded: list[bool] | None = None, sliding_window_reach: list[int] | None = None, )` (L21~L97)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        block_sizes: list[int],
        max_num_reqs: int,
        max_num_batched_tokens: int,
        max_num_blocks_per_group: list[int],
        device: torch.device,
        cp_size: int = 1,
        cp_rank: int = 0,
        cp_interleave: int = 1,
        slot_mapping_enabled: list[bool] | None = None,
        dcp_sharded: list[bool] | None = None,
    ):
        self.block_sizes = block_sizes
        self.max_num_reqs = max_num_reqs
        self.max_num_batched_tokens = max_num_batched_tokens
        self.device = device

        self.cp_size = cp_size
        self.cp_rank = cp_rank
        self.cp_interleave = cp_interleave

        self.num_kv_cache_groups = len(self.block_sizes)
        assert len(max_num_blocks_per_group) == self.num_kv_cache_groups
        if slot_mapping_enabled is None:
            slot_mapping_enabled = [True] * self.num_kv_cache_groups
        assert len(slot_mapping_enabled) == self.num_kv_cache_groups
        self._slot_mapping_enabled = slot_mapping_enabled
        if dcp_sharded is None:
            dcp_sharded = [True] * self.num_kv_cache_groups
        assert len(dcp_sharded) == self.num_kv_cache_groups
        self.dcp_sharded = torch.tensor(dcp_sharded, dtype=torch.bool, device=device)

        # num_kv_cache_groups x [max_num_reqs, max_num_blocks]
        self.block_tables: list[StagedWriteTensor] = []
        for max_num_blocks in max_num_blocks_per_group:
            block_table = StagedWriteTensor(
                (self.max_num_reqs, max_num_blocks), dtype=torch.int32, device=device
            )
            self.block_tables.append(block_table)

        self.num_blocks = UvaBackedTensor(
            (self.num_kv_cache_groups, self.max_num_reqs), dtype=torch.int32
        )
        self.fused_writer: FusedStagedWriter | None = None
        if self.num_kv_cache_groups > 1:
            # Only the multi-group path uses the fused writer.
            self.fused_writer = FusedStagedWriter(
                self.device, self.num_kv_cache_groups * self.max_num_reqs
            )

        # Block tables used for model's forward pass.
        # num_kv_cache_groups x [max_num_reqs, max_num_blocks]
        self.input_block_tables: list[torch.Tensor] = [
            torch.zeros_like(b.gpu) for b in self.block_tables
        ]
        self._num_dirty_rows = 0

        self.slot_mappings = torch.zeros(
            self.num_kv_cache_groups,
            self.max_num_batched_tokens,
            dtype=torch.int64,
            device=self.device,
        )

        self.init_block_table_layout_tensors()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        block_sizes: list[int],
        max_num_reqs: int,
        max_num_batched_tokens: int,
        max_num_blocks_per_group: list[int],
        device: torch.device,
        cp_size: int = 1,
        cp_rank: int = 0,
        cp_interleave: int = 1,
        slot_mapping_enabled: list[bool] | None = None,
        dcp_sharded: list[bool] | None = None,
        sliding_window_reach: list[int] | None = None,
    ):
        self.block_sizes = block_sizes
        self.max_num_reqs = max_num_reqs
        self.max_num_batched_tokens = max_num_batched_tokens
        self.device = device

        self.cp_size = cp_size
        self.cp_rank = cp_rank
        self.cp_interleave = cp_interleave

        self.num_kv_cache_groups = len(self.block_sizes)
        assert len(max_num_blocks_per_group) == self.num_kv_cache_groups
        if slot_mapping_enabled is None:
            slot_mapping_enabled = [True] * self.num_kv_cache_groups
        assert len(slot_mapping_enabled) == self.num_kv_cache_groups
        self._slot_mapping_enabled = slot_mapping_enabled
        if dcp_sharded is None:
            dcp_sharded = [True] * self.num_kv_cache_groups
        assert len(dcp_sharded) == self.num_kv_cache_groups
        self.dcp_sharded = torch.tensor(dcp_sharded, dtype=torch.bool, device=device)
        # Per group, how many tokens below a request's first scheduled position
        # attention can still read (SlidingWindowSpec.num_retained_tokens);
        # 0 disables it for the group. Under context parallelism a
        # block-table column does not map to a contiguous token range, so the
        # masking in gather_block_tables is disabled.
        if sliding_window_reach is None or cp_size > 1:
            sliding_window_reach = [0] * self.num_kv_cache_groups
        assert len(sliding_window_reach) == self.num_kv_cache_groups
        self._sliding_window_reach = sliding_window_reach
        self.has_sliding_window_groups = any(r > 0 for r in sliding_window_reach)

        # num_kv_cache_groups x [max_num_reqs, max_num_blocks]
        self.block_tables: list[StagedWriteTensor] = []
        for max_num_blocks in max_num_blocks_per_group:
            block_table = StagedWriteTensor(
                (self.max_num_reqs, max_num_blocks), dtype=torch.int32, device=device
            )
            self.block_tables.append(block_table)

        self.num_blocks = UvaBackedTensor(
            (self.num_kv_cache_groups, self.max_num_reqs), dtype=torch.int32
        )
        self.fused_writer: FusedStagedWriter | None = None
        if self.num_kv_cache_groups > 1:
            # Only the multi-group path uses the fused writer.
            self.fused_writer = FusedStagedWriter(
                self.device, self.num_kv_cache_groups * self.max_num_reqs
            )

        # Block tables used for model's forward pass.
        # num_kv_cache_groups x [max_num_reqs, max_num_blocks]
        self.input_block_tables: list[torch.Tensor] = [
            torch.zeros_like(b.gpu) for b in self.block_tables
        ]
        self._num_dirty_rows = 0

        self.slot_mappings = torch.zeros(
            self.num_kv_cache_groups,
            self.max_num_batched_tokens,
            dtype=torch.int64,
            device=self.device,
        )

        self.init_block_table_layout_tensors()
```

### 🔹 函式: `_gather_block_tables_kernel()`
- **變更前簽章 (Before)**: `def _gather_block_tables_kernel( batch_idx_to_req_idx, # [batch_size] src_block_table_ptrs, # [num_kv_cache_groups] dst_block_table_ptrs, # [num_kv_cache_groups] block_table_strides, # [num_kv_cache_groups] num_blocks_ptr, # [num_kv_cache_groups, max_num_reqs] num_blocks_stride, num_reqs, # actual number of requests (for padding) BLOCK_SIZE: tl.constexpr, ): # kv cache group id` (L240~L276)
- **變更後簽章 (After)**: `def _gather_block_tables_kernel( batch_idx_to_req_idx, # [batch_size] src_block_table_ptrs, # [num_kv_cache_groups] dst_block_table_ptrs, # [num_kv_cache_groups] block_table_strides, # [num_kv_cache_groups] num_blocks_ptr, # [num_kv_cache_groups, max_num_reqs] num_blocks_stride, num_reqs, # actual number of requests (for padding) num_computed_tokens_ptr, # [max_num_reqs] sliding_window_reach_ptr, # [num_kv_cache_groups] block_sizes_ptr, # [num_kv_cache_groups] MASK_SLIDING_WINDOW: tl.constexpr, BLOCK_SIZE: tl.constexpr, ): # kv cache group id` (L275~L330)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _gather_block_tables_kernel(
    batch_idx_to_req_idx,  # [batch_size]
    src_block_table_ptrs,  # [num_kv_cache_groups]
    dst_block_table_ptrs,  # [num_kv_cache_groups]
    block_table_strides,  # [num_kv_cache_groups]
    num_blocks_ptr,  # [num_kv_cache_groups, max_num_reqs]
    num_blocks_stride,
    num_reqs,  # actual number of requests (for padding)
    BLOCK_SIZE: tl.constexpr,
):
    # kv cache group id
    group_id = tl.program_id(0)
    batch_idx = tl.program_id(1)

    stride = tl.load(block_table_strides + group_id)
    max_num_blocks = stride  # stride equals max_num_blocks for this group.
    dst_block_table_ptr = _load_ptr(dst_block_table_ptrs + group_id, tl.int32)
    dst_row_ptr = dst_block_table_ptr + batch_idx * stride

    if batch_idx >= num_reqs:
        # Zero out padded rows.
        for i in tl.range(0, max_num_blocks, BLOCK_SIZE):
            offset = i + tl.arange(0, BLOCK_SIZE)
            tl.store(dst_row_ptr + offset, 0, mask=offset < max_num_blocks)
        return

    req_idx = tl.load(batch_idx_to_req_idx + batch_idx)
    group_num_blocks_ptr = num_blocks_ptr + group_id * num_blocks_stride
    num_blocks = tl.load(group_num_blocks_ptr + req_idx)

    src_block_table_ptr = _load_ptr(src_block_table_ptrs + group_id, tl.int32)
    src_row_ptr = src_block_table_ptr + req_idx * stride

    for i in tl.range(0, num_blocks, BLOCK_SIZE):
        offset = i + tl.arange(0, BLOCK_SIZE)
        block_ids = tl.load(src_row_ptr + offset, mask=offset < num_blocks)
        tl.store(dst_row_ptr + offset, block_ids, mask=offset < num_blocks)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _gather_block_tables_kernel(
    batch_idx_to_req_idx,  # [batch_size]
    src_block_table_ptrs,  # [num_kv_cache_groups]
    dst_block_table_ptrs,  # [num_kv_cache_groups]
    block_table_strides,  # [num_kv_cache_groups]
    num_blocks_ptr,  # [num_kv_cache_groups, max_num_reqs]
    num_blocks_stride,
    num_reqs,  # actual number of requests (for padding)
    num_computed_tokens_ptr,  # [max_num_reqs]
    sliding_window_reach_ptr,  # [num_kv_cache_groups]
    block_sizes_ptr,  # [num_kv_cache_groups]
    MASK_SLIDING_WINDOW: tl.constexpr,
    BLOCK_SIZE: tl.constexpr,
):
    # kv cache group id
    group_id = tl.program_id(0)
    batch_idx = tl.program_id(1)

    stride = tl.load(block_table_strides + group_id)
    max_num_blocks = stride  # stride equals max_num_blocks for this group.
    dst_block_table_ptr = _load_ptr(dst_block_table_ptrs + group_id, tl.int32)
    dst_row_ptr = dst_block_table_ptr + batch_idx * stride

    if batch_idx >= num_reqs:
        # Zero out padded rows.
        for i in tl.range(0, max_num_blocks, BLOCK_SIZE):
            offset = i + tl.arange(0, BLOCK_SIZE)
            tl.store(dst_row_ptr + offset, 0, mask=offset < max_num_blocks)
        return

    req_idx = tl.load(batch_idx_to_req_idx + batch_idx)
    group_num_blocks_ptr = num_blocks_ptr + group_id * num_blocks_stride
    num_blocks = tl.load(group_num_blocks_ptr + req_idx)

    src_block_table_ptr = _load_ptr(src_block_table_ptrs + group_id, tl.int32)
    src_row_ptr = src_block_table_ptr + req_idx * stride

    # Leading entries no query of this step can attend: null them (see
    # BlockTables.gather_block_tables).
    num_null = 0
    if MASK_SLIDING_WINDOW:
        reach = tl.load(sliding_window_reach_ptr + group_id)
        first_pos = tl.load(num_computed_tokens_ptr + req_idx)
        block_size = tl.load(block_sizes_ptr + group_id)
        num_null = tl.where(
            reach > 0, tl.maximum(first_pos - reach, 0) // block_size, 0
        )

    for i in tl.range(0, num_blocks, BLOCK_SIZE):
        offset = i + tl.arange(0, BLOCK_SIZE)
        block_ids = tl.load(
            src_row_ptr + offset,
            mask=(offset >= num_null) & (offset < num_blocks),
            other=0,
        )
        tl.store(dst_row_ptr + offset, block_ids, mask=offset < num_blocks)
```


#### 📄 檔案: `vllm/v1/worker/gpu/model_runner.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:306, E:353, A:0) ➔ After(N:306, E:353, A:0)
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

### 🔹 函式: `GPUModelRunner.prepare_attn()`
- **變更前簽章 (Before)**: `def prepare_attn( self, input_batch: InputBatch ) -> tuple[tuple[torch.Tensor, ...], torch.Tensor]` (L1569~L1587)
- **變更後簽章 (After)**: `def prepare_attn( self, input_batch: InputBatch ) -> tuple[tuple[torch.Tensor, ...], torch.Tensor]` (L1577~L1597)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def prepare_attn(
        self, input_batch: InputBatch
    ) -> tuple[tuple[torch.Tensor, ...], torch.Tensor]:
        if self.pcp_manager is not None:
            return self.pcp_manager.prepare_attn(input_batch)

        # Block tables: num_kv_cache_groups x [num_reqs_padded, max_num_blocks].
        block_tables = self.block_tables.gather_block_tables(
            input_batch.idx_mapping, num_reqs_padded=input_batch.num_reqs_after_padding
        )
        # Slot mappings: [num_kv_cache_groups, num_tokens_padded].
        # Kernel pads beyond num_tokens with PAD_SLOT_ID.
        slot_mappings = self.block_tables.compute_slot_mappings(
            input_batch.idx_mapping,
            input_batch.query_start_loc,
            input_batch.positions,
            num_tokens_padded=input_batch.num_tokens_after_padding,
        )
        return block_tables, slot_mappings
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def prepare_attn(
        self, input_batch: InputBatch
    ) -> tuple[tuple[torch.Tensor, ...], torch.Tensor]:
        if self.pcp_manager is not None:
            return self.pcp_manager.prepare_attn(input_batch)

        # Block tables: num_kv_cache_groups x [num_reqs_padded, max_num_blocks].
        block_tables = self.block_tables.gather_block_tables(
            input_batch.idx_mapping,
            num_reqs_padded=input_batch.num_reqs_after_padding,
            num_computed_tokens=self.req_states.num_computed_tokens.gpu,
        )
        # Slot mappings: [num_kv_cache_groups, num_tokens_padded].
        # Kernel pads beyond num_tokens with PAD_SLOT_ID.
        slot_mappings = self.block_tables.compute_slot_mappings(
            input_batch.idx_mapping,
            input_batch.query_start_loc,
            input_batch.positions,
            num_tokens_padded=input_batch.num_tokens_after_padding,
        )
        return block_tables, slot_mappings
```

### 🔹 函式: `GPUModelRunner.initialize_kv_cache()`
- **變更前簽章 (Before)**: `def initialize_kv_cache( self, kv_cache_config: KVCacheConfig, is_profiling: bool = False, kv_cache_allocation_context: AbstractContextManager | None = None, ) -> None: # GPUWorker finalizes the PD interleave before KV cache initialization.` (L621~L815)
- **變更後簽章 (After)**: `def initialize_kv_cache( self, kv_cache_config: KVCacheConfig, is_profiling: bool = False, kv_cache_allocation_context: AbstractContextManager | None = None, ) -> None: # GPUWorker finalizes the PD interleave before KV cache initialization.` (L622~L823)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def initialize_kv_cache(
        self,
        kv_cache_config: KVCacheConfig,
        is_profiling: bool = False,
        kv_cache_allocation_context: AbstractContextManager | None = None,
    ) -> None:
        # GPUWorker finalizes the PD interleave before KV cache initialization.
        self.cp_interleave = self.parallel_config.cp_kv_cache_interleave_size
        kv_cache_config = deepcopy(kv_cache_config)
        self.kv_cache_config = kv_cache_config

        block_table_max_model_len = self.max_model_len
        if self.is_encoder_decoder:
            # Cross-attention block tables need to index encoder tokens, which
            # can exceed the decoder's max_model_len.
            block_table_max_model_len = max(
                block_table_max_model_len,
                self.scheduler_config.max_num_encoder_input_tokens,
                getattr(self.model_config.hf_config, "max_source_positions", 0),
            )

        block_sizes = []
        max_num_blocks_per_group = []
        slot_mapping_enabled = []
        dcp_sharded = []
        for kv_cache_group in kv_cache_config.kv_cache_groups:
            spec = kv_cache_group.kv_cache_spec
            block_sizes.append(spec.block_size)
            layer_spec = (
                spec.first_spec if isinstance(spec, UniformTypeKVCacheSpecs) else spec
            )
            slot_mapping_enabled.append(layer_spec.uses_slot_mapping)
            dcp_sharded.append(spec.dcp_sharded)
            # Let each cache type account for CP. Attention KV is DCP-sharded,
            # while Mamba/GDN recurrent state is replicated across DCP ranks.
            max_num_blocks = spec.max_num_blocks_per_req(
                self.vllm_config, block_table_max_model_len
            )
            # Preserve each cache type's alignment requirements after applying
            # its topology-aware block-table width.
            max_num_blocks = get_block_table_width(
                max_num_blocks,
                spec.block_size,
                token_alignment=spec.block_table_token_alignment,
            )
            max_num_blocks_per_group.append(max_num_blocks)

        target_attn_layer_names = None
        if isinstance(self.speculator, DraftModelSpeculator):
            # Adaptive verification validates target attention separately.
            target_attn_layer_names = {
                layer_name
                for group in self.kv_cache_config.kv_cache_groups
                for layer_name in group.layer_names
            } - self.speculator.draft_attn_layer_names
        draft_attn_layer_names = None
        if isinstance(self.speculator, DraftModelSpeculator):
            draft_attn_layer_names = self.speculator.draft_attn_layer_names
        # Metadata builders select attention kernels that need JIT warmup.
        with self.jit_warmup_registry.activate():
            (
                self.attn_groups,
                attn_cg_support,
                self.kernel_block_sizes,
            ) = init_attn_backend(
                self.kv_cache_config,
                self.vllm_config,
                self.device,
                draft_layer_names=draft_attn_layer_names,
            )
        additional_attn_cg_support = self.model_state.get_additional_cg_support()
        attn_cg_support = attn_cg_support.narrow(*additional_attn_cg_support)
        # The speculator clears the flag at load time when the checkpoint has
        # no confidence head, so it holds the effective value.
        self.adaptive_verification = maybe_create_adaptive_verification_manager(
            enable_adaptive_verification=getattr(
                self.speculator, "enable_adaptive_verification", False
            ),
            attn_groups=self.attn_groups,
            req_states=self.req_states,
            query_start_loc=self.input_buffers.query_start_loc,
            num_bonus_tokens=self.model_state.num_new_sampled_tokens_per_step,
            max_total_logits=get_max_chunk_logits(self.vocab_size),
            vllm_config=self.vllm_config,
            target_layer_names=target_attn_layer_names,
            additional_attn_cg_support=additional_attn_cg_support,
        )

        self.block_tables = BlockTables(
            block_sizes=block_sizes,
            max_num_reqs=self.max_num_reqs,
            max_num_batched_tokens=self.max_num_tokens,
            max_num_blocks_per_group=max_num_blocks_per_group,
            device=self.device,
            slot_mapping_enabled=slot_mapping_enabled,
            dcp_sharded=dcp_sharded,
            cp_size=self.dcp_size,
            cp_rank=self.dcp_rank,
            cp_interleave=self.cp_interleave,
        )
        if self.pcp_manager is not None:
            self.pcp_manager.set_block_tables(self.block_tables)
        self.ubatch_runner = maybe_build_ubatch_runner(
            self.vllm_config,
            self.device,
            self.model_state,
            self.attn_groups,
            self.kv_cache_config,
            self.max_num_reqs,
        )
        if self.speculator is not None:
            self.speculator.pcp_manager = self.pcp_manager
        initialize_mamba_ssu_backend(
            self.vllm_config.mamba_config,
            self.kv_cache_config,
            use_replayssm=self.cache_config.use_replayssm,
        )
        piecewise_capture_available = bool(
            envs.VLLM_USE_BREAKABLE_CUDAGRAPH or has_compiled_submodule(self.model)
        )
        if self.adaptive_verification is not None:
            self.compilation_config.cudagraph_mode = resolve_adaptive_cudagraph_mode(
                self.compilation_config.cudagraph_mode,
                piecewise_capture_available=piecewise_capture_available,
            )
        cudagraph_mode = self.compilation_config.resolve_cudagraph_mode_and_sizes(
            attn_cg_support.min_cg_support,
            attn_cg_support.min_cg_attn_backend,
            self.decode_query_len,
            use_v2_model_runner=True,
            kv_cache_config=self.kv_cache_config,
            max_num_reqs=self.max_num_reqs,
            is_profiling=is_profiling,
            piecewise_capture_available=piecewise_capture_available,
        )
        self.cudagraph_manager = ModelCudaGraphManager(
            self.vllm_config,
            self.device,
            cudagraph_mode,
            decode_query_len=self.decode_query_len,
            lora_capture_cases=self.lora_capture_cases,
            varlen_decode=self.adaptive_verification is not None,
            ubatch_runner=self.ubatch_runner,
        )
        if self.cache_config.kv_sharing_fast_prefill and self.pcp_manager is None:
            self.fast_prefill = FastPrefillHelper(
                self.cudagraph_manager, self.max_num_tokens
            )
        check_attention_cp_compatibility(self.vllm_config, target_attn_layer_names)
        if isinstance(self.speculator, DraftModelSpeculator):
            # HACK(woosuk)
            self.speculator.set_attn(
                self.model_state,
                self.kv_cache_config,
                self.block_tables,
                self.input_buffers,
                self.attn_groups,
            )
        if self.speculator is not None:
            # After set_attn, so the speculator can size its cudagraph mode
            # to its own attention support.
            self.speculator.init_cudagraph_manager(cudagraph_mode)

        # Capture warmup providers that depend on allocated KV-cache strides.
        with self.jit_warmup_registry.activate():
            kv_caches_dict = init_kv_cache(
                self.compilation_config.static_forward_context,
                self.kv_cache_config,
                self.device,
                self.kernel_block_sizes,
                self.vllm_config,
                kv_cache_allocation_context=kv_cache_allocation_context,
                block_tables=self.block_tables,
                # Draft groups build their own metadata, so they map the views too.
                attn_groups=(
                    g
                    for groups in self.attn_groups
                    + getattr(self.speculator, "attn_groups", [])
                    for g in groups
                ),
            )
        self.kv_caches = [
            cache for cache in kv_caches_dict.values() if cache.device == self.device
        ]
        self.model_state.initialize_kv_cache(self.kv_cache_config, self.block_tables)
        if is_profiling:
            self.kv_connector = NO_OP_KV_CONNECTOR
        else:
            self.kv_connector = get_kv_connector(self.vllm_config, kv_caches_dict)

            # AuxOutput connector requires resolved kv_cache_config.
            if self.vllm_config.aux_output_config.enabled:
                self.aux_output_connector = get_aux_output_connector(
                    self.model, self.vllm_config, kv_cache_config
                )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def initialize_kv_cache(
        self,
        kv_cache_config: KVCacheConfig,
        is_profiling: bool = False,
        kv_cache_allocation_context: AbstractContextManager | None = None,
    ) -> None:
        # GPUWorker finalizes the PD interleave before KV cache initialization.
        self.cp_interleave = self.parallel_config.cp_kv_cache_interleave_size
        kv_cache_config = deepcopy(kv_cache_config)
        self.kv_cache_config = kv_cache_config

        block_table_max_model_len = self.max_model_len
        if self.is_encoder_decoder:
            # Cross-attention block tables need to index encoder tokens, which
            # can exceed the decoder's max_model_len.
            block_table_max_model_len = max(
                block_table_max_model_len,
                self.scheduler_config.max_num_encoder_input_tokens,
                getattr(self.model_config.hf_config, "max_source_positions", 0),
            )

        block_sizes = []
        max_num_blocks_per_group = []
        slot_mapping_enabled = []
        dcp_sharded = []
        sliding_window_reach = []
        for kv_cache_group in kv_cache_config.kv_cache_groups:
            spec = kv_cache_group.kv_cache_spec
            block_sizes.append(spec.block_size)
            layer_spec = (
                spec.first_spec if isinstance(spec, UniformTypeKVCacheSpecs) else spec
            )
            slot_mapping_enabled.append(layer_spec.uses_slot_mapping)
            dcp_sharded.append(spec.dcp_sharded)
            sliding_window_reach.append(
                layer_spec.num_retained_tokens
                if isinstance(layer_spec, SlidingWindowSpec)
                else 0
            )
            # Let each cache type account for CP. Attention KV is DCP-sharded,
            # while Mamba/GDN recurrent state is replicated across DCP ranks.
            max_num_blocks = spec.max_num_blocks_per_req(
                self.vllm_config, block_table_max_model_len
            )
            # Preserve each cache type's alignment requirements after applying
            # its topology-aware block-table width.
            max_num_blocks = get_block_table_width(
                max_num_blocks,
                spec.block_size,
                token_alignment=spec.block_table_token_alignment,
            )
            max_num_blocks_per_group.append(max_num_blocks)

        target_attn_layer_names = None
        if isinstance(self.speculator, DraftModelSpeculator):
            # Adaptive verification validates target attention separately.
            target_attn_layer_names = {
                layer_name
                for group in self.kv_cache_config.kv_cache_groups
                for layer_name in group.layer_names
            } - self.speculator.draft_attn_layer_names
        draft_attn_layer_names = None
        if isinstance(self.speculator, DraftModelSpeculator):
            draft_attn_layer_names = self.speculator.draft_attn_layer_names
        # Metadata builders select attention kernels that need JIT warmup.
        with self.jit_warmup_registry.activate():
            (
                self.attn_groups,
                attn_cg_support,
                self.kernel_block_sizes,
            ) = init_attn_backend(
                self.kv_cache_config,
                self.vllm_config,
                self.device,
                draft_layer_names=draft_attn_layer_names,
            )
        additional_attn_cg_support = self.model_state.get_additional_cg_support()
        attn_cg_support = attn_cg_support.narrow(*additional_attn_cg_support)
        # The speculator clears the flag at load time when the checkpoint has
        # no confidence head, so it holds the effective value.
        self.adaptive_verification = maybe_create_adaptive_verification_manager(
            enable_adaptive_verification=getattr(
                self.speculator, "enable_adaptive_verification", False
            ),
            attn_groups=self.attn_groups,
            req_states=self.req_states,
            query_start_loc=self.input_buffers.query_start_loc,
            num_bonus_tokens=self.model_state.num_new_sampled_tokens_per_step,
            max_total_logits=get_max_chunk_logits(self.vocab_size),
            vllm_config=self.vllm_config,
            target_layer_names=target_attn_layer_names,
            additional_attn_cg_support=additional_attn_cg_support,
        )

        self.block_tables = BlockTables(
            block_sizes=block_sizes,
            max_num_reqs=self.max_num_reqs,
            max_num_batched_tokens=self.max_num_tokens,
            max_num_blocks_per_group=max_num_blocks_per_group,
            device=self.device,
            slot_mapping_enabled=slot_mapping_enabled,
            dcp_sharded=dcp_sharded,
            sliding_window_reach=sliding_window_reach,
            cp_size=self.dcp_size,
            cp_rank=self.dcp_rank,
            cp_interleave=self.cp_interleave,
        )
        if self.pcp_manager is not None:
            self.pcp_manager.set_block_tables(self.block_tables)
        self.ubatch_runner = maybe_build_ubatch_runner(
            self.vllm_config,
            self.device,
            self.model_state,
            self.attn_groups,
            self.kv_cache_config,
            self.max_num_reqs,
        )
        if self.speculator is not None:
            self.speculator.pcp_manager = self.pcp_manager
        initialize_mamba_ssu_backend(
            self.vllm_config.mamba_config,
            self.kv_cache_config,
            use_replayssm=self.cache_config.use_replayssm,
        )
        piecewise_capture_available = bool(
            envs.VLLM_USE_BREAKABLE_CUDAGRAPH or has_compiled_submodule(self.model)
        )
        if self.adaptive_verification is not None:
            self.compilation_config.cudagraph_mode = resolve_adaptive_cudagraph_mode(
                self.compilation_config.cudagraph_mode,
                piecewise_capture_available=piecewise_capture_available,
            )
        cudagraph_mode = self.compilation_config.resolve_cudagraph_mode_and_sizes(
            attn_cg_support.min_cg_support,
            attn_cg_support.min_cg_attn_backend,
            self.decode_query_len,
            use_v2_model_runner=True,
            kv_cache_config=self.kv_cache_config,
            max_num_reqs=self.max_num_reqs,
            is_profiling=is_profiling,
            piecewise_capture_available=piecewise_capture_available,
        )
        self.cudagraph_manager = ModelCudaGraphManager(
            self.vllm_config,
            self.device,
            cudagraph_mode,
            decode_query_len=self.decode_query_len,
            lora_capture_cases=self.lora_capture_cases,
            varlen_decode=self.adaptive_verification is not None,
            ubatch_runner=self.ubatch_runner,
        )
        if self.cache_config.kv_sharing_fast_prefill and self.pcp_manager is None:
            self.fast_prefill = FastPrefillHelper(
                self.cudagraph_manager, self.max_num_tokens
            )
        check_attention_cp_compatibility(self.vllm_config, target_attn_layer_names)
        if isinstance(self.speculator, DraftModelSpeculator):
            # HACK(woosuk)
            self.speculator.set_attn(
                self.model_state,
                self.kv_cache_config,
                self.block_tables,
                self.input_buffers,
                self.attn_groups,
            )
        if self.speculator is not None:
            # After set_attn, so the speculator can size its cudagraph mode
            # to its own attention support.
            self.speculator.init_cudagraph_manager(cudagraph_mode)

        # Capture warmup providers that depend on allocated KV-cache strides.
        with self.jit_warmup_registry.activate():
            kv_caches_dict = init_kv_cache(
                self.compilation_config.static_forward_context,
                self.kv_cache_config,
                self.device,
                self.kernel_block_sizes,
                self.vllm_config,
                kv_cache_allocation_context=kv_cache_allocation_context,
                block_tables=self.block_tables,
                # Draft groups build their own metadata, so they map the views too.
                attn_groups=(
                    g
                    for groups in self.attn_groups
                    + getattr(self.speculator, "attn_groups", [])
                    for g in groups
                ),
            )
        self.kv_caches = [
            cache for cache in kv_caches_dict.values() if cache.device == self.device
        ]
        self.model_state.initialize_kv_cache(self.kv_cache_config, self.block_tables)
        if is_profiling:
            self.kv_connector = NO_OP_KV_CONNECTOR
        else:
            self.kv_connector = get_kv_connector(self.vllm_config, kv_caches_dict)

            # AuxOutput connector requires resolved kv_cache_config.
            if self.vllm_config.aux_output_config.enabled:
                self.aux_output_connector = get_aux_output_connector(
                    self.model, self.vllm_config, kv_cache_config
                )
```


---

### 🔹 Commit #05: `3aad5392`
- **完整 Hash**: `3aad5392abe2cb7268538e287a953c618e5a76d2`
- **說明 (Ground Truth)**: [Model] Support hotwords for MOSS-Transcribe-Diarize (#62329)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/model_executor/models/moss_transcribe_diarize.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:123, E:138, A:0) ➔ After(N:123, E:138, A:0)
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

### 🔹 函式: `MossTranscribeDiarizeForConditionalGeneration.get_generation_prompt()`
- **變更前簽章 (Before)**: `def get_generation_prompt(cls, stt_params: SpeechToTextParams) -> PromptType` (L631~L645)
- **變更後簽章 (After)**: `def get_generation_prompt(cls, stt_params: SpeechToTextParams) -> PromptType` (L633~L649)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def get_generation_prompt(cls, stt_params: SpeechToTextParams) -> PromptType:
        stt_config = stt_params.stt_config
        question = stt_params.request_prompt or DEFAULT_MOSS_TRANSCRIBE_DIARIZE_PROMPT
        question = question.strip() or DEFAULT_MOSS_TRANSCRIBE_DIARIZE_PROMPT
        prompt = (
            "<|im_start|>system\n"
            "You are a helpful assistant.<|im_end|>\n"
            f"<|im_start|>user\n{AUDIO_PLACEHOLDER}\n"
            f"{question}<|im_end|>\n"
            "<|im_start|>assistant\n"
        )
        return TextPrompt(
            prompt=prompt,
            multi_modal_data={"audio": (stt_params.audio, stt_config.sample_rate)},
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def get_generation_prompt(cls, stt_params: SpeechToTextParams) -> PromptType:
        stt_config = stt_params.stt_config
        question = stt_params.request_prompt or DEFAULT_MOSS_TRANSCRIBE_DIARIZE_PROMPT
        question = question.strip() or DEFAULT_MOSS_TRANSCRIBE_DIARIZE_PROMPT
        if hotwords := (stt_params.hotwords or "").strip():
            question += f"{MOSS_HOTWORDS_HINT}{hotwords}"
        prompt = (
            "<|im_start|>system\n"
            "You are a helpful assistant.<|im_end|>\n"
            f"<|im_start|>user\n{AUDIO_PLACEHOLDER}\n"
            f"{question}<|im_end|>\n"
            "<|im_start|>assistant\n"
        )
        return TextPrompt(
            prompt=prompt,
            multi_modal_data={"audio": (stt_params.audio, stt_config.sample_rate)},
        )
```


---

### 🔹 Commit #06: `2aa5080f`
- **完整 Hash**: `2aa5080fa0454b0f7bf107c85ffb149c5ecbcb83`
- **說明 (Ground Truth)**: [Bugfix][Weight Cache] Include RoPE parameters in IPC cache key (#60994)
- **變更檔案數**: 3

#### 📄 檔案: `vllm/model_executor/model_loader/weight_cache/daemon.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:79, E:88, A:0) ➔ After(N:81, E:90, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `remove (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `hash_rope_parameters (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `WeightCacheDaemon.load_model` ──[CALLS]──> `hash_rope_parameters (External/Unresolved)`
  • + [新增呼叫邊] `WeightCacheDaemon._handle_get_state` ──[CALLS]──> `remove (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `WeightCacheDaemon.load_model()`
- **變更前簽章 (Before)**: `def load_model(self) -> None` (L282~L308)
- **變更後簽章 (After)**: `def load_model(self) -> None` (L283~L311)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def load_model(self) -> None:
        torch.accelerator.set_device_index(self.local_rank)
        # Outside the config context so the daemon keeps its own rendezvous
        # instead of the engine's; model parallel groups (TP/DP/EP) are then
        # carved out of this world group like in the engine.
        init_distributed_environment(
            world_size=self.world_size,
            rank=self.global_rank,
            distributed_init_method=self.distributed_init_method,
            local_rank=self.local_rank,
            backend=current_platform.dist_backend,
        )
        with set_current_vllm_config(self.vllm_config):
            ensure_model_parallel_initialized(self.tp_size, self.pp_size)
            self.model = self.get_model()
        # Loading and post-processing leave freed transients in the caching
        # allocator; return them so engines sharing the GPU can use them.
        gc.collect()
        torch.accelerator.empty_cache()
        logger.info(
            "Weight cache %s daemon rank %d loaded model (%s GiB allocated, "
            "%s GiB reserved)",
            self.role,
            self.global_rank,
            format_gib(torch.accelerator.memory_allocated()),
            format_gib(torch.accelerator.memory_reserved()),
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def load_model(self) -> None:
        torch.accelerator.set_device_index(self.local_rank)
        # Outside the config context so the daemon keeps its own rendezvous
        # instead of the engine's; model parallel groups (TP/DP/EP) are then
        # carved out of this world group like in the engine.
        init_distributed_environment(
            world_size=self.world_size,
            rank=self.global_rank,
            distributed_init_method=self.distributed_init_method,
            local_rank=self.local_rank,
            backend=current_platform.dist_backend,
        )
        with set_current_vllm_config(self.vllm_config):
            ensure_model_parallel_initialized(self.tp_size, self.pp_size)
            self.model = self.get_model()
        # In-place reloads use configs already normalized by model construction.
        self.loaded_rope_parameters_hash = hash_rope_parameters(self.model_config)
        # Loading and post-processing leave freed transients in the caching
        # allocator; return them so engines sharing the GPU can use them.
        gc.collect()
        torch.accelerator.empty_cache()
        logger.info(
            "Weight cache %s daemon rank %d loaded model (%s GiB allocated, "
            "%s GiB reserved)",
            self.role,
            self.global_rank,
            format_gib(torch.accelerator.memory_allocated()),
            format_gib(torch.accelerator.memory_reserved()),
        )
```

### 🔹 函式: `WeightCacheDaemon._handle_get_state()`
- **變更前簽章 (Before)**: `def _handle_get_state(self, conn: socket.socket, request: dict) -> None` (L437~L468)
- **變更後簽章 (After)**: `def _handle_get_state(self, conn: socket.socket, request: dict) -> None` (L440~L477)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _handle_get_state(self, conn: socket.socket, request: dict) -> None:
        client_config = request.get("cache_config")
        if not isinstance(client_config, WeightCacheKey):
            send_msg(conn, {"status": "error", "message": "Missing cache_config"})
            return
        mismatched = self.cache_config.mismatched_fields(client_config)
        if mismatched:
            logger.warning("WeightCacheKey mismatch on fields: %s", mismatched)
            send_msg(conn, {"status": "mismatch", "fields": mismatched})
            return
        if self.model is None:
            send_msg(conn, {"status": "error", "message": "Weights were released"})
            return
        gpu_uuid = get_current_device_uuid()
        entries, aliases = export_entries(self.model)
        send_msg(
            conn,
            {
                "status": "ok",
                "entries": entries,
                "aliases": aliases,
                "attrs": export_model_attrs(self.model),
                "gpu_uuid": gpu_uuid,
            },
        )
        logger.info_once(
            "Weight cache %s daemon rank %d sent %d tensors (+%d aliases) to engine",
            self.role,
            self.global_rank,
            len(entries),
            len(aliases),
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _handle_get_state(self, conn: socket.socket, request: dict) -> None:
        client_config = request.get("cache_config")
        if not isinstance(client_config, WeightCacheKey):
            send_msg(conn, {"status": "error", "message": "Missing cache_config"})
            return
        mismatched = self.cache_config.mismatched_fields(client_config)
        if (
            request.get("is_reload", False)
            and "rope_parameters_hash" in mismatched
            and client_config.rope_parameters_hash == self.loaded_rope_parameters_hash
        ):
            mismatched.remove("rope_parameters_hash")
        if mismatched:
            logger.warning("WeightCacheKey mismatch on fields: %s", mismatched)
            send_msg(conn, {"status": "mismatch", "fields": mismatched})
            return
        if self.model is None:
            send_msg(conn, {"status": "error", "message": "Weights were released"})
            return
        gpu_uuid = get_current_device_uuid()
        entries, aliases = export_entries(self.model)
        send_msg(
            conn,
            {
                "status": "ok",
                "entries": entries,
                "aliases": aliases,
                "attrs": export_model_attrs(self.model),
                "gpu_uuid": gpu_uuid,
            },
        )
        logger.info_once(
            "Weight cache %s daemon rank %d sent %d tensors (+%d aliases) to engine",
            self.role,
            self.global_rank,
            len(entries),
            len(aliases),
        )
```


#### 📄 檔案: `vllm/model_executor/model_loader/weight_cache/ipc_loader.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:88, E:112, A:1) ➔ After(N:87, E:110, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 1, -Edges: 3, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#sock** `(Control)`
    └── ⚡ **clicked.connect**
        └── 🎯 [TRIGGERS] `socket_path (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `IpcModelLoader._request_state_with_startup_wait` (FUNCTION_DEF)
  • + [新增呼叫邊] `IpcModelLoader._fetch_entries` ──[CALLS]──> `IpcModelLoader._with_startup_wait`
  • - [移除呼叫邊] `IpcModelLoader._fetch_entries` ──[CALLS]──> `IpcModelLoader._request_state_with_startup_wait`
  • - [移除呼叫邊] `IpcModelLoader._request_state_with_startup_wait` ──[CALLS]──> `IpcModelLoader._with_startup_wait`
  • - [移除呼叫邊] `IpcModelLoader._request_state_with_startup_wait` ──[CALLS]──> `IpcModelLoader._request_state`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `IpcModelLoader._fetch_entries()`
- **變更前簽章 (Before)**: `def _fetch_entries(self, model_config: ModelConfig) -> WeightCacheState` (L347~L365)
- **變更後簽章 (After)**: `def _fetch_entries( self, model_config: ModelConfig, *, is_reload: bool = False ) -> WeightCacheState` (L347~L369)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _fetch_entries(self, model_config: ModelConfig) -> WeightCacheState:
        dp_group = get_dp_group()
        pp_group = get_pp_group()
        parallel_config = get_current_vllm_config().parallel_config
        cache_config = WeightCacheKey.from_model_config(
            model_config,
            tp_size=get_tensor_model_parallel_world_size(),
            tp_rank=get_tensor_model_parallel_rank(),
            pp_size=pp_group.world_size,
            pp_rank=pp_group.rank_in_group,
            dp_size=dp_group.world_size,
            dp_rank=dp_group.rank_in_group,
            is_draft=self.is_draft,
            enable_expert_parallel=parallel_config.enable_expert_parallel,
            expert_placement_strategy=parallel_config.expert_placement_strategy,
        )
        if not self.fallback:
            return self._request_state_with_startup_wait(cache_config)
        return self._request_state(cache_config)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _fetch_entries(
        self, model_config: ModelConfig, *, is_reload: bool = False
    ) -> WeightCacheState:
        dp_group = get_dp_group()
        pp_group = get_pp_group()
        parallel_config = get_current_vllm_config().parallel_config
        cache_config = WeightCacheKey.from_model_config(
            model_config,
            tp_size=get_tensor_model_parallel_world_size(),
            tp_rank=get_tensor_model_parallel_rank(),
            pp_size=pp_group.world_size,
            pp_rank=pp_group.rank_in_group,
            dp_size=dp_group.world_size,
            dp_rank=dp_group.rank_in_group,
            is_draft=self.is_draft,
            enable_expert_parallel=parallel_config.enable_expert_parallel,
            expert_placement_strategy=parallel_config.expert_placement_strategy,
        )
        if not self.fallback:
            return self._with_startup_wait(
                lambda: self._request_state(cache_config, is_reload=is_reload)
            )
        return self._request_state(cache_config, is_reload=is_reload)
```

### 🔹 函式: `IpcModelLoader.load_weights()`
- **變更前簽章 (Before)**: `def load_weights(self, model: nn.Module, model_config: ModelConfig) -> None` (L170~L187)
- **變更後簽章 (After)**: `def load_weights(self, model: nn.Module, model_config: ModelConfig) -> None` (L170~L187)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def load_weights(self, model: nn.Module, model_config: ModelConfig) -> None:
        """Best-effort in-place reload for an already-initialized model.

        Copies daemon tensors into matching parameters/buffers. The model is
        expected to already be in the post-quantized layout (e.g. previously
        loaded through this loader).
        """
        device_index = torch.accelerator.current_device_index()
        entries = self._fetch_entries(model_config).entries
        params = dict(model.named_parameters())
        buffers = dict(model.named_buffers())
        for name, entry in entries.items():
            target = params.get(name, buffers.get(name))
            source = entry.rebuild(device_index)
            if target is None or target.shape != source.shape:
                logger.warning("Skipping mismatched cached tensor %s", name)
                continue
            target.data.copy_(source)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def load_weights(self, model: nn.Module, model_config: ModelConfig) -> None:
        """Best-effort in-place reload for an already-initialized model.

        Copies daemon tensors into matching parameters/buffers. The model is
        expected to already be in the post-quantized layout (e.g. previously
        loaded through this loader).
        """
        device_index = torch.accelerator.current_device_index()
        entries = self._fetch_entries(model_config, is_reload=True).entries
        params = dict(model.named_parameters())
        buffers = dict(model.named_buffers())
        for name, entry in entries.items():
            target = params.get(name, buffers.get(name))
            source = entry.rebuild(device_index)
            if target is None or target.shape != source.shape:
                logger.warning("Skipping mismatched cached tensor %s", name)
                continue
            target.data.copy_(source)
```

### 🔹 函式: `IpcModelLoader._request_state()`
- **變更前簽章 (Before)**: `def _request_state(self, cache_config: WeightCacheKey) -> WeightCacheState` (L396~L414)
- **變更後簽章 (After)**: `def _request_state( self, cache_config: WeightCacheKey, *, is_reload: bool = False ) -> WeightCacheState` (L395~L422)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _request_state(self, cache_config: WeightCacheKey) -> WeightCacheState:
        with self._connect(self.state_timeout_s) as conn:
            send_msg(conn, {"cmd": "get_state", "cache_config": cache_config})
            response = recv_msg(conn)
        status = response.get("status")
        if status == "mismatch":
            raise CacheConfigMismatchError(
                f"WeightCacheKey mismatch on fields: {response.get('fields')}"
            )
        if status != "ok":
            raise WeightCacheUnavailableError(
                f"Weight cache daemon error: {response.get('message')}"
            )
        self._check_gpu_uuid(response.get("gpu_uuid"))
        return WeightCacheState(
            entries=response["entries"],
            aliases=response.get("aliases", {}),
            attrs=response.get("attrs", {}),
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _request_state(
        self, cache_config: WeightCacheKey, *, is_reload: bool = False
    ) -> WeightCacheState:
        with self._connect(self.state_timeout_s) as conn:
            send_msg(
                conn,
                {
                    "cmd": "get_state",
                    "cache_config": cache_config,
                    "is_reload": is_reload,
                },
            )
            response = recv_msg(conn)
        status = response.get("status")
        if status == "mismatch":
            raise CacheConfigMismatchError(
                f"WeightCacheKey mismatch on fields: {response.get('fields')}"
            )
        if status != "ok":
            raise WeightCacheUnavailableError(
                f"Weight cache daemon error: {response.get('message')}"
            )
        self._check_gpu_uuid(response.get("gpu_uuid"))
        return WeightCacheState(
            entries=response["entries"],
            aliases=response.get("aliases", {}),
            attrs=response.get("attrs", {}),
        )
```


#### 📄 檔案: `vllm/model_executor/model_loader/weight_cache/protocol.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:71, E:76, A:0) ➔ After(N:74, E:85, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 9, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `hash_rope_parameters` (FUNCTION_DEF)
  • + [新增節點] `is_integer (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `normalize_numbers` (FUNCTION_DEF)
  • + [新增呼叫邊] `hash_rope_parameters` ──[CALLS]──> `getattr (External/Unresolved)`
  • + [新增呼叫邊] `hash_rope_parameters` ──[CALLS]──> `dumps (External/Unresolved)`
  • + [新增呼叫邊] `hash_rope_parameters` ──[CALLS]──> `normalize_numbers`
  • + [新增呼叫邊] `hash_rope_parameters` ──[CALLS]──> `hexdigest (External/Unresolved)`
  • + [新增呼叫邊] `hash_rope_parameters` ──[CALLS]──> `safe_hash (External/Unresolved)`
  • + [新增呼叫邊] `hash_rope_parameters` ──[CALLS]──> `encode (External/Unresolved)`
  • + [新增呼叫邊] `normalize_numbers` ──[CALLS]──> `normalize_numbers`
  • + [新增呼叫邊] `normalize_numbers` ──[CALLS]──> `is_integer (External/Unresolved)`
  • + [新增呼叫邊] `WeightCacheKey.from_model_config` ──[CALLS]──> `hash_rope_parameters`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `WeightCacheKey.from_model_config()`
- **變更前簽章 (Before)**: `def from_model_config( cls, model_config: ModelConfig, tp_size: int, tp_rank: int, *, pp_size: int = 1, pp_rank: int = 0, is_draft: bool = False, dp_size: int = 1, dp_rank: int = 0, enable_expert_parallel: bool = False, expert_placement_strategy: str = "linear", ) -> "WeightCacheKey"` (L308~L357)
- **變更後簽章 (After)**: `def from_model_config( cls, model_config: ModelConfig, tp_size: int, tp_rank: int, *, pp_size: int = 1, pp_rank: int = 0, is_draft: bool = False, dp_size: int = 1, dp_rank: int = 0, enable_expert_parallel: bool = False, expert_placement_strategy: str = "linear", ) -> "WeightCacheKey"` (L331~L381)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def from_model_config(
        cls,
        model_config: ModelConfig,
        tp_size: int,
        tp_rank: int,
        *,
        pp_size: int = 1,
        pp_rank: int = 0,
        is_draft: bool = False,
        dp_size: int = 1,
        dp_rank: int = 0,
        enable_expert_parallel: bool = False,
        expert_placement_strategy: str = "linear",
    ) -> "WeightCacheKey":
        """Build the fingerprint for a model configuration.

        Must be called before weight loading: process_weights_after_loading
        may mutate hf_config.quantization_config, which would change the hash
        between the daemon and the engine.

        The checkpoint is identified by a hash of its safetensors metadata when
        the weights are available locally, so a daemon and engine referencing
        identical weights in different directories still match; otherwise it
        falls back to the model path.
        """
        hf_config = model_config.hf_config
        arch = ",".join(getattr(hf_config, "architectures", None) or [])
        quant_config = getattr(hf_config, "quantization_config", None)
        checkpoint = hash_checkpoint(model_config.model) or model_config.model
        return cls(
            checkpoint=checkpoint,
            model_arch=arch,
            tp_size=tp_size,
            tp_rank=tp_rank,
            pp_size=pp_size,
            pp_rank=pp_rank,
            dtype=str(model_config.dtype),
            quantization=model_config.quantization,
            quant_config_hash=_hash_quant_config(
                quant_config=quant_config,
                runtime_quant_config=model_config.quantization_config,
            ),
            revision=model_config.revision,
            vllm_version=vllm.version.__version__,
            is_draft=is_draft,
            dp_size=dp_size,
            dp_rank=dp_rank,
            enable_expert_parallel=enable_expert_parallel,
            expert_placement_strategy=expert_placement_strategy,
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def from_model_config(
        cls,
        model_config: ModelConfig,
        tp_size: int,
        tp_rank: int,
        *,
        pp_size: int = 1,
        pp_rank: int = 0,
        is_draft: bool = False,
        dp_size: int = 1,
        dp_rank: int = 0,
        enable_expert_parallel: bool = False,
        expert_placement_strategy: str = "linear",
    ) -> "WeightCacheKey":
        """Build the fingerprint for a model configuration.

        Must be called before weight loading: process_weights_after_loading
        may mutate hf_config.quantization_config, which would change the hash
        between the daemon and the engine.

        The checkpoint is identified by a hash of its safetensors metadata when
        the weights are available locally, so a daemon and engine referencing
        identical weights in different directories still match; otherwise it
        falls back to the model path.
        """
        hf_config = model_config.hf_config
        arch = ",".join(getattr(hf_config, "architectures", None) or [])
        quant_config = getattr(hf_config, "quantization_config", None)
        checkpoint = hash_checkpoint(model_config.model) or model_config.model
        return cls(
            checkpoint=checkpoint,
            model_arch=arch,
            tp_size=tp_size,
            tp_rank=tp_rank,
            pp_size=pp_size,
            pp_rank=pp_rank,
            dtype=str(model_config.dtype),
            quantization=model_config.quantization,
            quant_config_hash=_hash_quant_config(
                quant_config=quant_config,
                runtime_quant_config=model_config.quantization_config,
            ),
            rope_parameters_hash=hash_rope_parameters(model_config),
            revision=model_config.revision,
            vllm_version=vllm.version.__version__,
            is_draft=is_draft,
            dp_size=dp_size,
            dp_rank=dp_rank,
            enable_expert_parallel=enable_expert_parallel,
            expert_placement_strategy=expert_placement_strategy,
        )
```


---

### 🔹 Commit #07: `1641765f`
- **完整 Hash**: `1641765ffb53cb10f2753ece0efb41399f7381d3`
- **說明 (Ground Truth)**: [Bugfix][Scheduler] Fix encoder cache deadlock with drafter look-ahead (#60553)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/v1/core/sched/scheduler.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:226, E:326, A:0) ➔ After(N:226, E:326, A:0)
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

### 🔹 函式: `Scheduler._free_encoder_inputs()`
- **變更前簽章 (Before)**: `def _free_encoder_inputs(self, request: Request) -> None` (L2603~L2634)
- **變更後簽章 (After)**: `def _free_encoder_inputs(self, request: Request) -> None` (L2604~L2631)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _free_encoder_inputs(self, request: Request) -> None:
        cached_encoder_input_ids = self.encoder_cache_manager.get_cached_input_ids(
            request
        )
        # OPTIMIZATION: Avoid list(set) if the set is empty.
        if not cached_encoder_input_ids:
            return

        # Defer the free by the drafter's look-ahead so an entry stays
        # referenced until the drafter's read-ahead has also passed it,
        # mirroring the shift the encoder scheduling path applies.
        spec_lookahead = self.num_prefill_lookahead

        # Here, we use list(set) to avoid modifying the set while iterating
        # over it.
        for input_id in list(cached_encoder_input_ids):
            mm_feature = request.mm_features[input_id]
            start_pos = mm_feature.mm_position.offset
            num_tokens = mm_feature.mm_position.length
            if self.is_encoder_decoder and request.num_computed_tokens > 0:
                # With Whisper, as soon as we've generated a single token,
                # we know we're done with the encoder input. Cross Attention
                # KVs have been calculated and cached already.
                self._free_encoder_input(request, input_id)
            elif (
                start_pos + num_tokens + spec_lookahead
                <= request.num_computed_tokens - request.num_output_placeholders
            ):
                # Processed, stored in the decoder KV cache, and far enough past
                # the placeholder range (plus the drafter's look-ahead) that no
                # rejection or drafter gather can reference it.
                self._free_encoder_input(request, input_id)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _free_encoder_inputs(self, request: Request) -> None:
        cached_encoder_input_ids = self.encoder_cache_manager.get_cached_input_ids(
            request
        )
        # OPTIMIZATION: Avoid list(set) if the set is empty.
        if not cached_encoder_input_ids:
            return

        # Here, we use list(set) to avoid modifying the set while iterating
        # over it.
        for input_id in list(cached_encoder_input_ids):
            mm_feature = request.mm_features[input_id]
            start_pos = mm_feature.mm_position.offset
            num_tokens = mm_feature.mm_position.length
            if self.is_encoder_decoder and request.num_computed_tokens > 0:
                # With Whisper, as soon as we've generated a single token,
                # we know we're done with the encoder input. Cross Attention
                # KVs have been calculated and cached already.
                self._free_encoder_input(request, input_id)
            elif (
                start_pos + num_tokens
                <= request.num_computed_tokens - request.num_output_placeholders
            ):
                # Processed, stored in the decoder KV cache, and past the
                # placeholder range with no pending rejection that could roll
                # back into it. The drafter only reads ahead of
                # num_computed_tokens, so it cannot reference this input either.
                self._free_encoder_input(request, input_id)
```

### 🔹 函式: `Scheduler._try_schedule_encoder_inputs()`
- **變更前簽章 (Before)**: `def _try_schedule_encoder_inputs( self, request: Request, num_computed_tokens: int, num_new_tokens: int, encoder_compute_budget: int, shift_computed_tokens: int = 0, ) -> tuple[list[int], int, int, list[int], list[int]]` (L1869~L2059)
- **變更後簽章 (After)**: `def _try_schedule_encoder_inputs( self, request: Request, num_computed_tokens: int, num_new_tokens: int, encoder_compute_budget: int, shift_computed_tokens: int = 0, ) -> tuple[list[int], int, int, list[int], list[int]]` (L1869~L2060)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _try_schedule_encoder_inputs(
        self,
        request: Request,
        num_computed_tokens: int,
        num_new_tokens: int,
        encoder_compute_budget: int,
        shift_computed_tokens: int = 0,
    ) -> tuple[list[int], int, int, list[int], list[int]]:
        """Determine which encoder inputs need to be scheduled in the current step,
        and update `num_new_tokens` and encoder token budget accordingly.

        An encoder input will be scheduled if:
        - Its output tokens overlap with the range of tokens being computed
        in this step, i.e.,
        [num_computed_tokens, num_computed_tokens + num_new_tokens).
        - It is not already computed and stored in the encoder cache.
        - It is not exist on remote encoder cache (via ECConnector)
        - There is sufficient encoder token budget to process it.
        - The encoder cache has space to store it.

        If an encoder input cannot be scheduled due to cache or budget
        limitations, the method adjusts `num_new_tokens` to schedule only the
        decoder tokens up to just before the unschedulable encoder input.

        Note that num_computed_tokens includes both locally cached
        blocks and externally cached blocks (via KVConnector).
        """
        if num_new_tokens == 0 or not request.has_encoder_inputs:
            return [], num_new_tokens, encoder_compute_budget, [], []
        encoder_inputs_to_schedule: list[int] = []
        mm_features = request.mm_features
        assert mm_features is not None
        assert len(mm_features) > 0
        external_load_encoder_input = []
        duplicate_encoder_inputs = []

        # NOTE: since scheduler operates on the request level (possibly with
        # multiple encoder inputs per request), we need to create temporary
        # trackers for accounting at the encoder input level.
        mm_hashes_to_schedule: dict[str, int] = {}
        num_embeds_to_schedule = 0

        encoder_window_end = (
            num_computed_tokens + num_new_tokens + shift_computed_tokens
        )
        lo, hi = get_mm_features_in_window(
            mm_features,
            start=num_computed_tokens,
            end=encoder_window_end,
        )
        # For encoder-decoder, all inputs sit at start_pos=0, so lo=0 always.
        if self.is_encoder_decoder:
            lo = 0

        for i in range(lo, hi):
            mm_feature = mm_features[i]
            start_pos = mm_feature.mm_position.offset
            num_encoder_tokens = mm_feature.mm_position.length
            num_encoder_embeds = mm_feature.mm_position.get_num_embeds()
            item_identifier = mm_feature.identifier

            if self.is_encoder_decoder and num_computed_tokens > 0:
                assert start_pos == 0, (
                    "Encoder input should be processed at the beginning of "
                    "the sequence when encoder-decoder models are used."
                )
                # Encoder input has already been computed
                # The calculation here is a bit different. We don't turn encoder
                # output into tokens that get processed by the decoder and
                # reflected in num_computed_tokens. Instead, start_pos reflects
                # the position where we need to ensure we calculate encoder
                # inputs. This should always be 0 to ensure we calculate encoder
                # inputs before running the decoder.  Once we've calculated some
                # decoder tokens (num_computed_tokens > 0), then we know we
                # already calculated encoder inputs and can skip here.
                continue

            # If no encoder input chunking is allowed, we do not want to
            # partially schedule a multimodal item. If the scheduled range would
            # only cover part of the mm input, roll back to before the mm item.
            if (
                self.scheduler_config.disable_chunked_mm_input
                and not self.is_encoder_decoder
                # `<=`, not `<`: a chunk that starts exactly at the item still
                # splits it when it cannot cover the whole item.
                and num_computed_tokens <= start_pos
                and (num_computed_tokens + num_new_tokens)
                < (start_pos + num_encoder_tokens)
            ):
                # Account for EAGLE shift when rolling back to avoid
                # encoder cache miss. This ensures the scheduled range
                # stops before start_pos even with the shift.
                num_new_tokens = max(
                    0, start_pos - (num_computed_tokens + shift_computed_tokens)
                )
                break

            if not self.is_encoder_decoder:
                # We are not using the encoder cache for encoder-decoder models,
                # yet.
                if item_identifier in mm_hashes_to_schedule:
                    scheduled_num_encoder_embeds = mm_hashes_to_schedule[
                        item_identifier
                    ]
                    if self._reject_on_encoder_cache_embed_mismatch(
                        request,
                        i,
                        item_identifier,
                        scheduled_num_encoder_embeds,
                        num_encoder_embeds,
                    ):
                        return [], 0, encoder_compute_budget, [], []
                    # The same encoder input has already been scheduled in the
                    # current step.
                    duplicate_encoder_inputs.append(i)
                    continue

                cached_num_encoder_embeds = (
                    self.encoder_cache_manager.get_cached_num_encoder_embeds(request, i)
                )
                if cached_num_encoder_embeds is not None and (
                    self._reject_on_encoder_cache_embed_mismatch(
                        request,
                        i,
                        item_identifier,
                        cached_num_encoder_embeds,
                        num_encoder_embeds,
                    )
                ):
                    return [], 0, encoder_compute_budget, [], []

                if self.encoder_cache_manager.check_and_update_cache(request, i):
                    # The encoder input is already computed and cached from a
                    # previous step.
                    continue

            if not self.encoder_cache_manager.can_allocate(
                request, i, encoder_compute_budget, num_embeds_to_schedule
            ):
                # The encoder cache is full or the encoder budget is exhausted.
                # NOTE(woosuk): We assume that the encoder input tokens should
                # be processed altogether, as the encoder usually uses
                # bidirectional attention.
                if num_computed_tokens + shift_computed_tokens < start_pos:
                    # We only schedule the decoder tokens just before the
                    # encoder input.
                    num_new_tokens = start_pos - (
                        num_computed_tokens + shift_computed_tokens
                    )
                else:
                    # Because of prefix caching, num_computed_tokens is greater
                    # than start_pos even though its encoder input is not
                    # available. In this case, we can't schedule any token for
                    # the request in this step.
                    num_new_tokens = 0
                break

            # Calculate the number of embeddings to schedule in the current range
            # of scheduled encoder placeholder tokens.
            start_idx_rel = max(0, num_computed_tokens - start_pos)
            end_idx_rel = min(num_encoder_tokens, encoder_window_end - start_pos)
            curr_embeds_start, curr_embeds_end = (
                mm_feature.mm_position.get_embeds_indices_in_range(
                    start_idx_rel, end_idx_rel
                )
            )
            # There's no embeddings in the current range of encoder placeholder tokens
            # so we can skip the encoder input.
            if curr_embeds_end - curr_embeds_start == 0:
                continue

            if self.ec_connector is not None and self.ec_connector.has_cache_item(
                item_identifier
            ):
                mm_hashes_to_schedule[item_identifier] = num_encoder_embeds
                external_load_encoder_input.append(i)
                num_embeds_to_schedule += num_encoder_embeds
                continue

            num_embeds_to_schedule += num_encoder_embeds
            encoder_compute_budget -= num_encoder_embeds
            mm_hashes_to_schedule[item_identifier] = num_encoder_embeds
            encoder_inputs_to_schedule.append(i)

        return (
            encoder_inputs_to_schedule,
            num_new_tokens,
            encoder_compute_budget,
            external_load_encoder_input,
            duplicate_encoder_inputs,
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _try_schedule_encoder_inputs(
        self,
        request: Request,
        num_computed_tokens: int,
        num_new_tokens: int,
        encoder_compute_budget: int,
        shift_computed_tokens: int = 0,
    ) -> tuple[list[int], int, int, list[int], list[int]]:
        """Determine which encoder inputs need to be scheduled in the current step,
        and update `num_new_tokens` and encoder token budget accordingly.

        An encoder input will be scheduled if:
        - Its output tokens overlap with the range of tokens being computed
        in this step, i.e.,
        [num_computed_tokens, num_computed_tokens + num_new_tokens).
        - It is not already computed and stored in the encoder cache.
        - It is not exist on remote encoder cache (via ECConnector)
        - There is sufficient encoder token budget to process it.
        - The encoder cache has space to store it.

        If an encoder input cannot be scheduled due to cache or budget
        limitations, the method adjusts `num_new_tokens` to schedule only the
        decoder tokens up to just before the unschedulable encoder input.

        Note that num_computed_tokens includes both locally cached
        blocks and externally cached blocks (via KVConnector).
        """
        if num_new_tokens == 0 or not request.has_encoder_inputs:
            return [], num_new_tokens, encoder_compute_budget, [], []
        encoder_inputs_to_schedule: list[int] = []
        mm_features = request.mm_features
        assert mm_features is not None
        assert len(mm_features) > 0
        external_load_encoder_input = []
        duplicate_encoder_inputs = []

        # NOTE: since scheduler operates on the request level (possibly with
        # multiple encoder inputs per request), we need to create temporary
        # trackers for accounting at the encoder input level.
        mm_hashes_to_schedule: dict[str, int] = {}
        num_embeds_to_schedule = 0

        encoder_window_end = (
            num_computed_tokens + num_new_tokens + shift_computed_tokens
        )
        lo, hi = get_mm_features_in_window(
            mm_features,
            start=num_computed_tokens,
            end=encoder_window_end,
        )
        # For encoder-decoder, all inputs sit at start_pos=0, so lo=0 always.
        if self.is_encoder_decoder:
            lo = 0

        for i in range(lo, hi):
            mm_feature = mm_features[i]
            start_pos = mm_feature.mm_position.offset
            num_encoder_tokens = mm_feature.mm_position.length
            num_encoder_embeds = mm_feature.mm_position.get_num_embeds()
            item_identifier = mm_feature.identifier

            if self.is_encoder_decoder and num_computed_tokens > 0:
                assert start_pos == 0, (
                    "Encoder input should be processed at the beginning of "
                    "the sequence when encoder-decoder models are used."
                )
                # Encoder input has already been computed
                # The calculation here is a bit different. We don't turn encoder
                # output into tokens that get processed by the decoder and
                # reflected in num_computed_tokens. Instead, start_pos reflects
                # the position where we need to ensure we calculate encoder
                # inputs. This should always be 0 to ensure we calculate encoder
                # inputs before running the decoder.  Once we've calculated some
                # decoder tokens (num_computed_tokens > 0), then we know we
                # already calculated encoder inputs and can skip here.
                continue

            # If no encoder input chunking is allowed, we do not want to
            # partially schedule a multimodal item. If the scheduled range would
            # only cover part of the mm input, roll back to before the mm item.
            if (
                self.scheduler_config.disable_chunked_mm_input
                and not self.is_encoder_decoder
                # `<=`, not `<`: a chunk that starts exactly at the item still
                # splits it when it cannot cover the whole item.
                and num_computed_tokens <= start_pos
                and (num_computed_tokens + num_new_tokens)
                < (start_pos + num_encoder_tokens)
            ):
                # Account for EAGLE shift when rolling back to avoid
                # encoder cache miss. This ensures the scheduled range
                # stops before start_pos even with the shift.
                num_new_tokens = max(
                    0, start_pos - (num_computed_tokens + shift_computed_tokens)
                )
                break

            if not self.is_encoder_decoder:
                # We are not using the encoder cache for encoder-decoder models,
                # yet.
                if item_identifier in mm_hashes_to_schedule:
                    scheduled_num_encoder_embeds = mm_hashes_to_schedule[
                        item_identifier
                    ]
                    if self._reject_on_encoder_cache_embed_mismatch(
                        request,
                        i,
                        item_identifier,
                        scheduled_num_encoder_embeds,
                        num_encoder_embeds,
                    ):
                        return [], 0, encoder_compute_budget, [], []
                    # The same encoder input has already been scheduled in the
                    # current step.
                    duplicate_encoder_inputs.append(i)
                    continue

                cached_num_encoder_embeds = (
                    self.encoder_cache_manager.get_cached_num_encoder_embeds(request, i)
                )
                if cached_num_encoder_embeds is not None and (
                    self._reject_on_encoder_cache_embed_mismatch(
                        request,
                        i,
                        item_identifier,
                        cached_num_encoder_embeds,
                        num_encoder_embeds,
                    )
                ):
                    return [], 0, encoder_compute_budget, [], []

                if self.encoder_cache_manager.check_and_update_cache(request, i):
                    # The encoder input is already computed and cached from a
                    # previous step.
                    continue

            if not self.encoder_cache_manager.can_allocate(
                request, i, encoder_compute_budget, num_embeds_to_schedule
            ):
                # The encoder cache is full or the encoder budget is exhausted.
                # NOTE(woosuk): We assume that the encoder input tokens should
                # be processed altogether, as the encoder usually uses
                # bidirectional attention.
                if num_computed_tokens < start_pos:
                    # We only schedule the decoder tokens just before the
                    # encoder input. No drafter shift here: its read-ahead into
                    # this unencoded input falls back to token embeddings.
                    num_new_tokens = min(
                        num_new_tokens, start_pos - num_computed_tokens
                    )
                else:
                    # Because of prefix caching, num_computed_tokens is greater
                    # than start_pos even though its encoder input is not
                    # available. In this case, we can't schedule any token for
                    # the request in this step.
                    num_new_tokens = 0
                break

            # Calculate the number of embeddings to schedule in the current range
            # of scheduled encoder placeholder tokens.
            start_idx_rel = max(0, num_computed_tokens - start_pos)
            end_idx_rel = min(num_encoder_tokens, encoder_window_end - start_pos)
            curr_embeds_start, curr_embeds_end = (
                mm_feature.mm_position.get_embeds_indices_in_range(
                    start_idx_rel, end_idx_rel
                )
            )
            # There's no embeddings in the current range of encoder placeholder tokens
            # so we can skip the encoder input.
            if curr_embeds_end - curr_embeds_start == 0:
                continue

            if self.ec_connector is not None and self.ec_connector.has_cache_item(
                item_identifier
            ):
                mm_hashes_to_schedule[item_identifier] = num_encoder_embeds
                external_load_encoder_input.append(i)
                num_embeds_to_schedule += num_encoder_embeds
                continue

            num_embeds_to_schedule += num_encoder_embeds
            encoder_compute_budget -= num_encoder_embeds
            mm_hashes_to_schedule[item_identifier] = num_encoder_embeds
            encoder_inputs_to_schedule.append(i)

        return (
            encoder_inputs_to_schedule,
            num_new_tokens,
            encoder_compute_budget,
            external_load_encoder_input,
            duplicate_encoder_inputs,
        )
```


---

### 🔹 Commit #08: `d46cb9a6`
- **完整 Hash**: `d46cb9a6d40414fef1f27f0937a97796c351a216`
- **說明 (Ground Truth)**: [Bugfix][Weight Cache] Key non-MoE DP daemons as DP=1 like the engine (#60179)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/model_executor/model_loader/weight_cache/daemon.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:78, E:87, A:0) ➔ After(N:79, E:88, A:0)
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
  • + [新增節點] `get_engine_dp_placement` (FUNCTION_DEF)
  • + [新增呼叫邊] `WeightCacheDaemon.__init__` ──[CALLS]──> `get_engine_dp_placement`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `WeightCacheDaemon.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, vllm_config: VllmConfig, global_rank: int, local_rank: int, distributed_init_method: str, socket_dir: str | None = None, is_draft: bool = False, dp_rank: int = 0, pp_rank: int = 0, )` (L178~L244)
- **變更後簽章 (After)**: `def __init__( self, vllm_config: VllmConfig, global_rank: int, local_rank: int, distributed_init_method: str, socket_dir: str | None = None, is_draft: bool = False, dp_rank: int = 0, pp_rank: int = 0, )` (L178~L245)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        vllm_config: VllmConfig,
        global_rank: int,
        local_rank: int,
        distributed_init_method: str,
        socket_dir: str | None = None,
        is_draft: bool = False,
        dp_rank: int = 0,
        pp_rank: int = 0,
    ):
        parallel_config = vllm_config.parallel_config
        if parallel_config.enable_eplb:
            raise ValueError("The weight cache daemon does not support EPLB.")
        self.tp_size = parallel_config.tensor_parallel_size
        self.pp_size = parallel_config.pipeline_parallel_size
        self.dp_size = parallel_config.data_parallel_size
        if self.dp_size > 1:
            # The engine sets these on each DP rank's workers; the MoE/EP
            # layers read them to place their expert shards.
            if parallel_config.nnodes > 1:
                world_size = self.dp_size * self.tp_size
                local_world = world_size // parallel_config.nnodes
                start_dp_rank = parallel_config.node_rank * local_world // self.tp_size
            else:
                start_dp_rank = parallel_config.data_parallel_rank
            parallel_config = replace(
                parallel_config,
                data_parallel_rank=dp_rank,
                data_parallel_rank_local=dp_rank - start_dp_rank,
            )
            vllm_config = replace(vllm_config, parallel_config=parallel_config)
        self.vllm_config = vllm_config
        # A draft daemon builds the draft with the target's VllmConfig, like
        # the engine does; only the ModelConfig differs.
        if is_draft:
            spec = vllm_config.speculative_config
            assert spec is not None and spec.draft_model_config is not None
            self.model_config = spec.draft_model_config
        else:
            self.model_config = vllm_config.model_config
        self.global_rank = global_rank
        rank_in_dp = global_rank - dp_rank * self.pp_size * self.tp_size
        self.tp_rank = rank_in_dp % self.tp_size
        self.pp_rank = rank_in_dp // self.tp_size
        self.dp_rank = dp_rank
        self.world_size = self.dp_size * self.pp_size * self.tp_size
        self.local_rank = local_rank
        self.distributed_init_method = distributed_init_method
        self.socket_dir = socket_dir
        self.is_draft = is_draft
        self.role = format_daemon_role(is_draft)
        self.model: torch.nn.Module | None = None
        # Fingerprint before loading: process_weights_after_loading may
        # mutate hf_config.quantization_config.
        self.cache_config = WeightCacheKey.from_model_config(
            self.model_config,
            tp_size=self.tp_size,
            tp_rank=self.tp_rank,
            pp_size=self.pp_size,
            pp_rank=self.pp_rank,
            dp_size=self.dp_size,
            dp_rank=dp_rank,
            is_draft=is_draft,
            enable_expert_parallel=parallel_config.enable_expert_parallel,
            expert_placement_strategy=parallel_config.expert_placement_strategy,
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        vllm_config: VllmConfig,
        global_rank: int,
        local_rank: int,
        distributed_init_method: str,
        socket_dir: str | None = None,
        is_draft: bool = False,
        dp_rank: int = 0,
        pp_rank: int = 0,
    ):
        parallel_config = vllm_config.parallel_config
        if parallel_config.enable_eplb:
            raise ValueError("The weight cache daemon does not support EPLB.")
        self.tp_size = parallel_config.tensor_parallel_size
        self.pp_size = parallel_config.pipeline_parallel_size
        self.dp_size = parallel_config.data_parallel_size
        if self.dp_size > 1:
            # The engine sets these on each DP rank's workers; the MoE/EP
            # layers read them to place their expert shards.
            if parallel_config.nnodes > 1:
                world_size = self.dp_size * self.tp_size
                local_world = world_size // parallel_config.nnodes
                start_dp_rank = parallel_config.node_rank * local_world // self.tp_size
            else:
                start_dp_rank = parallel_config.data_parallel_rank
            parallel_config = replace(
                parallel_config,
                data_parallel_rank=dp_rank,
                data_parallel_rank_local=dp_rank - start_dp_rank,
            )
            vllm_config = replace(vllm_config, parallel_config=parallel_config)
        self.vllm_config = vllm_config
        # A draft daemon builds the draft with the target's VllmConfig, like
        # the engine does; only the ModelConfig differs.
        if is_draft:
            spec = vllm_config.speculative_config
            assert spec is not None and spec.draft_model_config is not None
            self.model_config = spec.draft_model_config
        else:
            self.model_config = vllm_config.model_config
        self.global_rank = global_rank
        rank_in_dp = global_rank - dp_rank * self.pp_size * self.tp_size
        self.tp_rank = rank_in_dp % self.tp_size
        self.pp_rank = rank_in_dp // self.tp_size
        self.dp_rank = dp_rank
        self.world_size = self.dp_size * self.pp_size * self.tp_size
        self.local_rank = local_rank
        self.distributed_init_method = distributed_init_method
        self.socket_dir = socket_dir
        self.is_draft = is_draft
        self.role = format_daemon_role(is_draft)
        self.model: torch.nn.Module | None = None
        key_dp_size, key_dp_rank = get_engine_dp_placement(vllm_config, dp_rank)
        # Fingerprint before loading: process_weights_after_loading may
        # mutate hf_config.quantization_config.
        self.cache_config = WeightCacheKey.from_model_config(
            self.model_config,
            tp_size=self.tp_size,
            tp_rank=self.tp_rank,
            pp_size=self.pp_size,
            pp_rank=self.pp_rank,
            dp_size=key_dp_size,
            dp_rank=key_dp_rank,
            is_draft=is_draft,
            enable_expert_parallel=parallel_config.enable_expert_parallel,
            expert_placement_strategy=parallel_config.expert_placement_strategy,
        )
```


---

### 🔹 Commit #09: `852989f5`
- **完整 Hash**: `852989f580820849113d67d13fd8053e279d0444`
- **說明 (Ground Truth)**: [Bugfix][Sampler] Fix split top-p masking every token for huge logits (thinking_token_budget + spec decode emits token 0) (#58231)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/v1/sample/ops/topk_topp_triton.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:62, E:170, A:0) ➔ After(N:62, E:169, A:0)
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
  • - [移除呼叫邊] `_topp_sb_mask_kernel` ──[CALLS]──> `log (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `_topp_sb_mask_kernel()`
- **變更前簽章 (Before)**: `def _topp_sb_mask_kernel( LOGITS, LOGITS_STRIDE_0, STATS, PARTS, K, P, HAS_K: tl.constexpr, MASK_VALUE: tl.constexpr, S: tl.constexpr, F: tl.constexpr, NUM_ROUNDS: tl.constexpr, VOCAB_SIZE: tl.constexpr, BLOCK: tl.constexpr, )` (L1396~L1523)
- **變更後簽章 (After)**: `def _topp_sb_mask_kernel( LOGITS, LOGITS_STRIDE_0, STATS, PARTS, K, P, HAS_K: tl.constexpr, MASK_VALUE: tl.constexpr, S: tl.constexpr, F: tl.constexpr, NUM_ROUNDS: tl.constexpr, VOCAB_SIZE: tl.constexpr, BLOCK: tl.constexpr, )` (L1396~L1518)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _topp_sb_mask_kernel(
    LOGITS,
    LOGITS_STRIDE_0,
    STATS,
    PARTS,
    K,
    P,
    HAS_K: tl.constexpr,
    MASK_VALUE: tl.constexpr,
    S: tl.constexpr,
    F: tl.constexpr,
    NUM_ROUNDS: tl.constexpr,
    VOCAB_SIZE: tl.constexpr,
    BLOCK: tl.constexpr,
):
    pid = tl.program_id(0)
    row = pid // S
    slice_id = pid % S
    p = tl.load(P + row)
    if p >= 1.0:
        return
    if HAS_K and tl.load(K + row) < VOCAB_SIZE:
        return
    M, Z, mn, num_finite = _topp_sb_row_stats(STATS, row, S)
    if (Z <= 0.0) or (num_finite < 1.0):
        return
    max_prob = 1.0 / Z
    min_prob = tl.maximum(tl.exp(mn - M) / Z, 1e-30)
    if max_prob <= min_prob * (1.0 + 1e-6):
        return  # (nearly) uniform row: keep everything
    # Replay the full combine chain; the last round finalizes with fallback
    # semantics. Rows that converged early stop the chain at that round.
    # `fin` tracks the (round, ladder slot) whose per-slice partials define
    # the boundary value, for deterministic duplicate handling below.
    lo = min_prob
    hi = max_prob
    best = -1.0
    best_mass = 0.0
    best_minl = 1.0
    best_nmin = 0.0
    done = 0.0
    nomask = 0.0
    pivot = 0.0
    dup = 1.0
    numdup = 1.0
    numkeep = 1.0
    fin = -1.0
    best_fin = -1.0
    for j in range(NUM_ROUNDS):
        if done == 0.0:
            (
                done,
                nomask,
                pivot,
                dup,
                numdup,
                numkeep,
                lo,
                hi,
                best,
                best_mass,
                best_minl,
                best_nmin,
                sel_fidx,
                best_sel,
            ) = _topp_sb_combine(
                PARTS + (row * NUM_ROUNDS + j) * S * F * 3,
                Z,
                p,
                lo,
                hi,
                best,
                best_mass,
                best_minl,
                best_nmin,
                S=S,
                F=F,
                IS_LAST=j == NUM_ROUNDS - 1,
            )
            if sel_fidx >= 0.0:
                fin = j * F + sel_fidx
            if best_sel >= 0.0:
                best_fin = j * F + best_sel
    if nomask != 0.0:
        return
    if fin < 0.0:
        fin = best_fin
    logZ = tl.log(Z)
    pivot_logit = tl.log(pivot) + logZ + M
    # numdup/numkeep are exact small integers held in fp32.
    ties = numkeep < numdup
    num_preceding = 0.0
    if ties:
        # Deterministic, index-ordered duplicate budget: per-slice counts of
        # the boundary value come from the finalizing round's partials (a
        # slice holds copies of `dup` iff its minl matches `dup`, with the
        # count in nmin), so each slice knows exactly how many copies were
        # kept by lower-indexed slices.
        fin_round = tl.cast(fin / F, tl.int32)
        fin_slot = tl.cast(fin - tl.cast(fin_round, tl.float32) * F, tl.int32)
        pbase = PARTS + ((row * NUM_ROUNDS + fin_round) * S * F + fin_slot) * 3
        sidx = tl.arange(0, S)
        minl_s = tl.load(pbase + sidx * (F * 3) + 1)
        nmin_s = tl.load(pbase + sidx * (F * 3) + 2)
        dupc_s = tl.where(tl.abs(minl_s - dup) < 1e-9, nmin_s, 0.0)
        num_preceding = tl.sum(tl.where(sidx < slice_id, dupc_s, 0.0))
    slice_len = (VOCAB_SIZE + S - 1) // S
    start = slice_id * slice_len
    end = tl.minimum(start + slice_len, VOCAB_SIZE)
    ROW = LOGITS + row.to(tl.int64) * LOGITS_STRIDE_0
    offs = tl.arange(0, BLOCK)
    for i in range(start, end, BLOCK):
        mask_n = i + offs < end
        x = tl.load(ROW + i + offs, mask=mask_n, other=-float("inf"))
        keep = x > pivot_logit
        if ties:
            # Match the boundary value in probability space with exact
            # equality: `dup` is a probability computed by the step kernels
            # as exp(x - M) / Z, so recomputing it here with the same ops
            # reproduces it bitwise on any platform. (The log/exp round-trip
            # to logit space loses ~1e-6 to cancellation, breaking any
            # absolute tolerance.)
            dmask = tl.exp(x - M) / Z == dup
            cum = tl.cumsum(dmask.to(tl.int32)).to(tl.float32) + num_preceding
            keep_dup = dmask & (cum <= numkeep)
            keep = keep & (~dmask | keep_dup)
            num_preceding += tl.sum(dmask.to(tl.float32))
        tl.store(ROW + i + offs, tl.where(keep, x, MASK_VALUE), mask=mask_n)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _topp_sb_mask_kernel(
    LOGITS,
    LOGITS_STRIDE_0,
    STATS,
    PARTS,
    K,
    P,
    HAS_K: tl.constexpr,
    MASK_VALUE: tl.constexpr,
    S: tl.constexpr,
    F: tl.constexpr,
    NUM_ROUNDS: tl.constexpr,
    VOCAB_SIZE: tl.constexpr,
    BLOCK: tl.constexpr,
):
    pid = tl.program_id(0)
    row = pid // S
    slice_id = pid % S
    p = tl.load(P + row)
    if p >= 1.0:
        return
    if HAS_K and tl.load(K + row) < VOCAB_SIZE:
        return
    M, Z, mn, num_finite = _topp_sb_row_stats(STATS, row, S)
    if (Z <= 0.0) or (num_finite < 1.0):
        return
    max_prob = 1.0 / Z
    min_prob = tl.maximum(tl.exp(mn - M) / Z, 1e-30)
    if max_prob <= min_prob * (1.0 + 1e-6):
        return  # (nearly) uniform row: keep everything
    # Replay the full combine chain; the last round finalizes with fallback
    # semantics. Rows that converged early stop the chain at that round.
    # `fin` tracks the (round, ladder slot) whose per-slice partials define
    # the boundary value, for deterministic duplicate handling below.
    lo = min_prob
    hi = max_prob
    best = -1.0
    best_mass = 0.0
    best_minl = 1.0
    best_nmin = 0.0
    done = 0.0
    nomask = 0.0
    pivot = 0.0
    dup = 1.0
    numdup = 1.0
    numkeep = 1.0
    fin = -1.0
    best_fin = -1.0
    for j in range(NUM_ROUNDS):
        if done == 0.0:
            (
                done,
                nomask,
                pivot,
                dup,
                numdup,
                numkeep,
                lo,
                hi,
                best,
                best_mass,
                best_minl,
                best_nmin,
                sel_fidx,
                best_sel,
            ) = _topp_sb_combine(
                PARTS + (row * NUM_ROUNDS + j) * S * F * 3,
                Z,
                p,
                lo,
                hi,
                best,
                best_mass,
                best_minl,
                best_nmin,
                S=S,
                F=F,
                IS_LAST=j == NUM_ROUNDS - 1,
            )
            if sel_fidx >= 0.0:
                fin = j * F + sel_fidx
            if best_sel >= 0.0:
                best_fin = j * F + best_sel
    if nomask != 0.0:
        return
    if fin < 0.0:
        fin = best_fin
    # numdup/numkeep are exact small integers held in fp32.
    ties = numkeep < numdup
    num_preceding = 0.0
    if ties:
        # Deterministic, index-ordered duplicate budget: per-slice counts of
        # the boundary value come from the finalizing round's partials (a
        # slice holds copies of `dup` iff its minl matches `dup`, with the
        # count in nmin), so each slice knows exactly how many copies were
        # kept by lower-indexed slices.
        fin_round = tl.cast(fin / F, tl.int32)
        fin_slot = tl.cast(fin - tl.cast(fin_round, tl.float32) * F, tl.int32)
        pbase = PARTS + ((row * NUM_ROUNDS + fin_round) * S * F + fin_slot) * 3
        sidx = tl.arange(0, S)
        minl_s = tl.load(pbase + sidx * (F * 3) + 1)
        nmin_s = tl.load(pbase + sidx * (F * 3) + 2)
        dupc_s = tl.where(tl.abs(minl_s - dup) < 1e-9, nmin_s, 0.0)
        num_preceding = tl.sum(tl.where(sidx < slice_id, dupc_s, 0.0))
    slice_len = (VOCAB_SIZE + S - 1) // S
    start = slice_id * slice_len
    end = tl.minimum(start + slice_len, VOCAB_SIZE)
    ROW = LOGITS + row.to(tl.int64) * LOGITS_STRIDE_0
    offs = tl.arange(0, BLOCK)
    for i in range(start, end, BLOCK):
        mask_n = i + offs < end
        x = tl.load(ROW + i + offs, mask=mask_n, other=-float("inf"))
        # Mask in probability space (bitwise the step kernels' predicate);
        # the logit-space pivot rounds to M for huge |M|.
        prob = tl.exp(x - M) / Z
        keep = (prob > pivot) | (x == M)
        if ties:
            dmask = prob == dup
            cum = tl.cumsum(dmask.to(tl.int32)).to(tl.float32) + num_preceding
            keep_dup = dmask & (cum <= numkeep)
            keep = keep & (~dmask | keep_dup)
            num_preceding += tl.sum(dmask.to(tl.float32))
        tl.store(ROW + i + offs, tl.where(keep, x, MASK_VALUE), mask=mask_n)
```


---

### 🔹 Commit #10: `10e8e921`
- **完整 Hash**: `10e8e921b8e3115e9e7fc5ab3bac7c5c5844c02f`
- **說明 (Ground Truth)**: [Bugfix][Frontend] Fix auto truncation without an output token limit (#62010)
- **變更檔案數**: 3

#### 📄 檔案: `vllm/entrypoints/openai/chat_completion/protocol.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:55, E:57, A:0) ➔ After(N:55, E:57, A:0)
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

### 🔹 函式: `ChatCompletionRequest.build_tok_params()`
- **變更前簽章 (Before)**: `def build_tok_params(self, model_config: ModelConfig) -> TokenizeParams` (L671~L689)
- **變更後簽章 (After)**: `def build_tok_params(self, model_config: ModelConfig) -> TokenizeParams` (L671~L689)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def build_tok_params(self, model_config: ModelConfig) -> TokenizeParams:
        if self.max_completion_tokens is not None:
            max_output_tokens: int | None = self.max_completion_tokens
            max_output_tokens_param = "max_completion_tokens"
        else:
            max_output_tokens = self.max_tokens
            max_output_tokens_param = "max_tokens"

        return TokenizeParams(
            max_total_tokens=model_config.max_model_len,
            max_output_tokens=max_output_tokens or 0,
            truncate_prompt_tokens=self.truncate_prompt_tokens,
            truncation_side=self.truncation_side,
            add_special_tokens=self.add_special_tokens,
            needs_detokenization=bool(self.echo and not self.return_token_ids),
            max_total_tokens_param="max_model_len",
            max_output_tokens_param=max_output_tokens_param,
            return_token_offsets=bool(self.return_token_offsets),
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def build_tok_params(self, model_config: ModelConfig) -> TokenizeParams:
        if self.max_completion_tokens is not None:
            max_output_tokens: int | None = self.max_completion_tokens
            max_output_tokens_param = "max_completion_tokens"
        else:
            max_output_tokens = self.max_tokens
            max_output_tokens_param = "max_tokens"

        return TokenizeParams(
            max_total_tokens=model_config.max_model_len,
            max_output_tokens=max_output_tokens,
            truncate_prompt_tokens=self.truncate_prompt_tokens,
            truncation_side=self.truncation_side,
            add_special_tokens=self.add_special_tokens,
            needs_detokenization=bool(self.echo and not self.return_token_ids),
            max_total_tokens_param="max_model_len",
            max_output_tokens_param=max_output_tokens_param,
            return_token_offsets=bool(self.return_token_offsets),
        )
```


#### 📄 檔案: `vllm/entrypoints/openai/responses/protocol.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:54, E:51, A:0) ➔ After(N:54, E:51, A:0)
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

### 🔹 函式: `ResponsesRequest.build_tok_params()`
- **變更前簽章 (Before)**: `def build_tok_params(self, model_config: ModelConfig) -> TokenizeParams` (L464~L471)
- **變更後簽章 (After)**: `def build_tok_params(self, model_config: ModelConfig) -> TokenizeParams` (L464~L471)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def build_tok_params(self, model_config: ModelConfig) -> TokenizeParams:
        return TokenizeParams(
            max_total_tokens=model_config.max_model_len,
            max_output_tokens=self.max_output_tokens or 0,
            truncate_prompt_tokens=-1 if self.truncation != "disabled" else None,
            max_total_tokens_param="max_model_len",
            max_output_tokens_param="max_output_tokens",
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def build_tok_params(self, model_config: ModelConfig) -> TokenizeParams:
        return TokenizeParams(
            max_total_tokens=model_config.max_model_len,
            max_output_tokens=self.max_output_tokens,
            truncate_prompt_tokens=-1 if self.truncation != "disabled" else None,
            max_total_tokens_param="max_model_len",
            max_output_tokens_param="max_output_tokens",
        )
```


#### 📄 檔案: `vllm/renderers/params.py`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:35, E:24, A:0) ➔ After(N:35, E:24, A:0)
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

### 🔹 Commit #11: `6a0b146c`
- **完整 Hash**: `6a0b146c1674bac69a783fda8bdbdcd0dfc5f998`
- **說明 (Ground Truth)**: [ROCm][Compile] Fuse AITER static FP8 quant into MLA attention output (#62371)
- **變更檔案數**: 2

#### 📄 檔案: `vllm/compilation/passes/fusion/mla_attn_quant_fusion.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:47, E:57, A:0) ➔ After(N:54, E:66, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 11, -Edges: 2, ΔFuncs: 7, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `RocmMLAAttnFp8StaticQuantPattern._output` (FUNCTION_DEF)
  • + [新增節點] `MLAAttnFp8StaticQuantPattern._quantize` (FUNCTION_DEF)
  • + [新增節點] `RocmMLAAttnFp8StaticQuantPattern.__init__` (FUNCTION_DEF)
  • + [新增節點] `MLAAttnFp8StaticQuantPattern._output` (FUNCTION_DEF)
  • + [新增節點] `is_rocm (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `RocmMLAAttnFp8StaticQuantPattern._quantize` (FUNCTION_DEF)
  • + [新增節點] `is_enabled (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `MLAAttnFp8StaticQuantPattern._quantize` ──[CALLS]──> `_quant_matcher (External/Unresolved)`
  • + [新增呼叫邊] `MLAAttnFp8StaticQuantPattern._pattern_with_ln` ──[CALLS]──> `MLAAttnFp8StaticQuantPattern._quantize`
  • + [新增呼叫邊] `MLAAttnFp8StaticQuantPattern._pattern` ──[CALLS]──> `MLAAttnFp8StaticQuantPattern._quantize`
  • + [新增呼叫邊] `MLAAttnFp8StaticQuantPattern._replacement_with_ln` ──[CALLS]──> `MLAAttnFp8StaticQuantPattern._output`
  • + [新增呼叫邊] `MLAAttnFp8StaticQuantPattern._replacement` ──[CALLS]──> `MLAAttnFp8StaticQuantPattern._output`
  • + [新增呼叫邊] `RocmMLAAttnFp8StaticQuantPattern.__init__` ──[CALLS]──> `RocmMLAAttnFp8StaticQuantPattern.__init__`
  • + [新增呼叫邊] `RocmMLAAttnFp8StaticQuantPattern.__init__` ──[CALLS]──> `super (External/Unresolved)`
  • + [新增呼叫邊] `RocmMLAAttnFp8StaticQuantPattern.__init__` ──[CALLS]──> `MatcherQuantFP8 (External/Unresolved)`
  • _... 以及其餘 5 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `MLAAttnFp8StaticQuantPattern._pattern()`
- **變更前簽章 (Before)**: `def _pattern(q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep)` (L84~L97)
- **變更後簽章 (After)**: `def _pattern(q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep)` (L99~L112)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _pattern(q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep):
            at1 = auto_functionalized(
                MLA_ATTN_OP,
                q=q,
                kv_c_normed=kv_c_normed,
                k_pe=k_pe,
                output=output_attn,
                layer_name=_ln,
                output_scale=None,
                output_block_scale=None,
                kv_cache_dummy_dep=kv_cache_dummy_dep,
            )
            # MLA output is already 2D (T, N*V), no reshape needed
            return self._quant_matcher(at1[1], scale)[0]
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _pattern(q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep):
            at1 = auto_functionalized(
                MLA_ATTN_OP,
                q=q,
                kv_c_normed=kv_c_normed,
                k_pe=k_pe,
                output=output_attn,
                layer_name=_ln,
                output_scale=None,
                output_block_scale=None,
                kv_cache_dummy_dep=kv_cache_dummy_dep,
            )
            # MLA output is already 2D (T, N*V), no reshape needed
            return self._quantize(at1[1], scale)
```

### 🔹 函式: `MLAAttnFp8StaticQuantPattern.replacement()`
- **變更前簽章 (Before)**: `def replacement(self) -> Callable[..., torch.Tensor]` (L102~L157)
- **變更後簽章 (After)**: `def replacement( self, ) -> Callable[..., torch.Tensor | tuple[torch.Tensor, torch.Tensor]]` (L117~L174)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def replacement(self) -> Callable[..., torch.Tensor]:
        _ln = _encode_layer_name(self._layer_name)

        if _USE_LAYERNAME:

            def _replacement_with_ln(  # type: ignore[misc]
                q,
                kv_c_normed,
                k_pe,
                output_attn,
                scale,
                kv_cache_dummy_dep,
                layer_name,
            ):
                # MLA output in quant_dtype
                output_attn = torch.empty(
                    [q.shape[0], self._output_dim],
                    dtype=FP8_DTYPE,
                    device=q.device,
                )
                at1 = auto_functionalized(
                    MLA_ATTN_OP,
                    q=q,
                    kv_c_normed=kv_c_normed,
                    k_pe=k_pe,
                    output=output_attn,
                    layer_name=layer_name,
                    output_scale=scale,
                    output_block_scale=None,
                    kv_cache_dummy_dep=kv_cache_dummy_dep,
                )
                return at1[1]

            return _replacement_with_ln

        def _replacement(q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep):
            # MLA output in quant_dtype
            output_attn = torch.empty(
                [q.shape[0], self._output_dim],
                dtype=FP8_DTYPE,
                device=q.device,
            )
            at1 = auto_functionalized(
                MLA_ATTN_OP,
                q=q,
                kv_c_normed=kv_c_normed,
                k_pe=k_pe,
                output=output_attn,
                layer_name=_ln,
                output_scale=scale,
                output_block_scale=None,
                kv_cache_dummy_dep=kv_cache_dummy_dep,
            )
            return at1[1]

        return _replacement
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def replacement(
        self,
    ) -> Callable[..., torch.Tensor | tuple[torch.Tensor, torch.Tensor]]:
        _ln = _encode_layer_name(self._layer_name)

        if _USE_LAYERNAME:

            def _replacement_with_ln(  # type: ignore[misc]
                q,
                kv_c_normed,
                k_pe,
                output_attn,
                scale,
                kv_cache_dummy_dep,
                layer_name,
            ):
                # MLA output in quant_dtype
                output_attn = torch.empty(
                    [q.shape[0], self._output_dim],
                    dtype=FP8_DTYPE,
                    device=q.device,
                )
                at1 = auto_functionalized(
                    MLA_ATTN_OP,
                    q=q,
                    kv_c_normed=kv_c_normed,
                    k_pe=k_pe,
                    output=output_attn,
                    layer_name=layer_name,
                    output_scale=scale,
                    output_block_scale=None,
                    kv_cache_dummy_dep=kv_cache_dummy_dep,
                )
                return self._output(at1[1], scale)

            return _replacement_with_ln

        def _replacement(q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep):
            # MLA output in quant_dtype
            output_attn = torch.empty(
                [q.shape[0], self._output_dim],
                dtype=FP8_DTYPE,
                device=q.device,
            )
            at1 = auto_functionalized(
                MLA_ATTN_OP,
                q=q,
                kv_c_normed=kv_c_normed,
                k_pe=k_pe,
                output=output_attn,
                layer_name=_ln,
                output_scale=scale,
                output_block_scale=None,
                kv_cache_dummy_dep=kv_cache_dummy_dep,
            )
            return self._output(at1[1], scale)

        return _replacement
```

### 🔹 函式: `MLAAttnFp8StaticQuantPattern.pattern()`
- **變更前簽章 (Before)**: `def pattern(self) -> Callable[..., torch.Tensor]` (L54~L99)
- **變更後簽章 (After)**: `def pattern( self, ) -> Callable[..., torch.Tensor | tuple[torch.Tensor, torch.Tensor]]` (L67~L114)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def pattern(self) -> Callable[..., torch.Tensor]:
        _ln = _encode_layer_name(self._layer_name)

        if _USE_LAYERNAME:

            def _pattern_with_ln(  # type: ignore[misc]
                q,
                kv_c_normed,
                k_pe,
                output_attn,
                scale,
                kv_cache_dummy_dep,
                layer_name,
            ):
                at1 = auto_functionalized(
                    MLA_ATTN_OP,
                    q=q,
                    kv_c_normed=kv_c_normed,
                    k_pe=k_pe,
                    output=output_attn,
                    layer_name=layer_name,
                    output_scale=None,
                    output_block_scale=None,
                    kv_cache_dummy_dep=kv_cache_dummy_dep,
                )
                # MLA output is already 2D (T, N*V), no reshape needed
                return self._quant_matcher(at1[1], scale)[0]

            return _pattern_with_ln

        def _pattern(q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep):
            at1 = auto_functionalized(
                MLA_ATTN_OP,
                q=q,
                kv_c_normed=kv_c_normed,
                k_pe=k_pe,
                output=output_attn,
                layer_name=_ln,
                output_scale=None,
                output_block_scale=None,
                kv_cache_dummy_dep=kv_cache_dummy_dep,
            )
            # MLA output is already 2D (T, N*V), no reshape needed
            return self._quant_matcher(at1[1], scale)[0]

        return _pattern
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def pattern(
        self,
    ) -> Callable[..., torch.Tensor | tuple[torch.Tensor, torch.Tensor]]:
        _ln = _encode_layer_name(self._layer_name)

        if _USE_LAYERNAME:

            def _pattern_with_ln(  # type: ignore[misc]
                q,
                kv_c_normed,
                k_pe,
                output_attn,
                scale,
                kv_cache_dummy_dep,
                layer_name,
            ):
                at1 = auto_functionalized(
                    MLA_ATTN_OP,
                    q=q,
                    kv_c_normed=kv_c_normed,
                    k_pe=k_pe,
                    output=output_attn,
                    layer_name=layer_name,
                    output_scale=None,
                    output_block_scale=None,
                    kv_cache_dummy_dep=kv_cache_dummy_dep,
                )
                # MLA output is already 2D (T, N*V), no reshape needed
                return self._quantize(at1[1], scale)

            return _pattern_with_ln

        def _pattern(q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep):
            at1 = auto_functionalized(
                MLA_ATTN_OP,
                q=q,
                kv_c_normed=kv_c_normed,
                k_pe=k_pe,
                output=output_attn,
                layer_name=_ln,
                output_scale=None,
                output_block_scale=None,
                kv_cache_dummy_dep=kv_cache_dummy_dep,
            )
            # MLA output is already 2D (T, N*V), no reshape needed
            return self._quantize(at1[1], scale)

        return _pattern
```

### 🔹 函式: `MLAAttnFp8StaticQuantPattern._replacement()`
- **變更前簽章 (Before)**: `def _replacement(q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep): # MLA output in quant_dtype` (L137~L155)
- **變更後簽章 (After)**: `def _replacement(q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep): # MLA output in quant_dtype` (L154~L172)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _replacement(q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep):
            # MLA output in quant_dtype
            output_attn = torch.empty(
                [q.shape[0], self._output_dim],
                dtype=FP8_DTYPE,
                device=q.device,
            )
            at1 = auto_functionalized(
                MLA_ATTN_OP,
                q=q,
                kv_c_normed=kv_c_normed,
                k_pe=k_pe,
                output=output_attn,
                layer_name=_ln,
                output_scale=scale,
                output_block_scale=None,
                kv_cache_dummy_dep=kv_cache_dummy_dep,
            )
            return at1[1]
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _replacement(q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep):
            # MLA output in quant_dtype
            output_attn = torch.empty(
                [q.shape[0], self._output_dim],
                dtype=FP8_DTYPE,
                device=q.device,
            )
            at1 = auto_functionalized(
                MLA_ATTN_OP,
                q=q,
                kv_c_normed=kv_c_normed,
                k_pe=k_pe,
                output=output_attn,
                layer_name=_ln,
                output_scale=scale,
                output_block_scale=None,
                kv_cache_dummy_dep=kv_cache_dummy_dep,
            )
            return self._output(at1[1], scale)
```

### 🔹 函式: `MLAAttnQuantFusionPass.__init__()`
- **變更前簽章 (Before)**: `def __init__(self, config: VllmConfig) -> None` (L579~L629)
- **變更後簽章 (After)**: `def __init__(self, config: VllmConfig) -> None` (L618~L670)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(self, config: VllmConfig) -> None:
        super().__init__(config, "mla_attn_quant_fusion")

        dtype = config.model_config.dtype
        layers = list(get_layers_from_vllm_config(config, MLAAttention).values())

        if len(layers) == 0:
            logger.warning(
                "MLA attention + quant fusion is enabled, but no MLA "
                "attention layers were found in "
                "CompilationConfig.static_forward_context "
                "so no fusion patterns were registered."
            )

        # When _USE_LAYERNAME is enabled, layer_name is a wildcard so all
        # layers produce the same pattern — register once then break.
        for layer in layers:
            if layer.impl.fused_output_quant_supported(kFp8StaticTensorSym):
                self.register(MLAAttnFp8StaticQuantPattern(layer, dtype))
                if _USE_LAYERNAME:
                    break

        if current_platform.is_cuda() and hasattr(torch.ops._C, "scaled_fp4_quant"):
            for layer in layers:
                if layer.impl.fused_output_quant_supported(kNvfp4Dynamic):
                    self.register(MLAAttnNvfp4QuantPattern(layer, dtype))
                    if _USE_LAYERNAME:
                        break

        # Per-group FP8 (block quant) — register all flag combinations.
        if current_platform.is_cuda():
            for quant_key in [kFp8Dynamic128Sym, kFp8Dynamic64Sym]:
                for col_major in [True, False]:
                    for is_e8m0 in [True, False]:
                        for tma_aligned in [False, True]:
                            for layer in layers:
                                if layer.impl.fused_output_quant_supported(quant_key):
                                    self.register(
                                        MLAAttnFp8GroupQuantPattern(
                                            layer,
                                            dtype,
                                            quant_key,
                                            col_major,
                                            is_e8m0,
                                            tma_aligned,
                                        )
                                    )
                                    if _USE_LAYERNAME:
                                        break

        self.dump_patterns(config, self.pm_pass)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(self, config: VllmConfig) -> None:
        super().__init__(config, "mla_attn_quant_fusion")

        dtype = config.model_config.dtype
        layers = list(get_layers_from_vllm_config(config, MLAAttention).values())

        if len(layers) == 0:
            logger.warning(
                "MLA attention + quant fusion is enabled, but no MLA "
                "attention layers were found in "
                "CompilationConfig.static_forward_context "
                "so no fusion patterns were registered."
            )

        # When _USE_LAYERNAME is enabled, layer_name is a wildcard so all
        # layers produce the same pattern — register once then break.
        for layer in layers:
            if layer.impl.fused_output_quant_supported(kFp8StaticTensorSym):
                self.register(MLAAttnFp8StaticQuantPattern(layer, dtype))
                if current_platform.is_rocm() and rocm_aiter_ops.is_enabled():
                    self.register(RocmMLAAttnFp8StaticQuantPattern(layer, dtype))
                if _USE_LAYERNAME:
                    break

        if current_platform.is_cuda() and hasattr(torch.ops._C, "scaled_fp4_quant"):
            for layer in layers:
                if layer.impl.fused_output_quant_supported(kNvfp4Dynamic):
                    self.register(MLAAttnNvfp4QuantPattern(layer, dtype))
                    if _USE_LAYERNAME:
                        break

        # Per-group FP8 (block quant) — register all flag combinations.
        if current_platform.is_cuda():
            for quant_key in [kFp8Dynamic128Sym, kFp8Dynamic64Sym]:
                for col_major in [True, False]:
                    for is_e8m0 in [True, False]:
                        for tma_aligned in [False, True]:
                            for layer in layers:
                                if layer.impl.fused_output_quant_supported(quant_key):
                                    self.register(
                                        MLAAttnFp8GroupQuantPattern(
                                            layer,
                                            dtype,
                                            quant_key,
                                            col_major,
                                            is_e8m0,
                                            tma_aligned,
                                        )
                                    )
                                    if _USE_LAYERNAME:
                                        break

        self.dump_patterns(config, self.pm_pass)
```

### 🔹 函式: `MLAAttnFp8StaticQuantPattern._pattern_with_ln()`
- **變更前簽章 (Before)**: `def _pattern_with_ln( # type: ignore[misc] q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep, layer_name, )` (L59~L80)
- **變更後簽章 (After)**: `def _pattern_with_ln( # type: ignore[misc] q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep, layer_name, )` (L74~L95)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _pattern_with_ln(  # type: ignore[misc]
                q,
                kv_c_normed,
                k_pe,
                output_attn,
                scale,
                kv_cache_dummy_dep,
                layer_name,
            ):
                at1 = auto_functionalized(
                    MLA_ATTN_OP,
                    q=q,
                    kv_c_normed=kv_c_normed,
                    k_pe=k_pe,
                    output=output_attn,
                    layer_name=layer_name,
                    output_scale=None,
                    output_block_scale=None,
                    kv_cache_dummy_dep=kv_cache_dummy_dep,
                )
                # MLA output is already 2D (T, N*V), no reshape needed
                return self._quant_matcher(at1[1], scale)[0]
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _pattern_with_ln(  # type: ignore[misc]
                q,
                kv_c_normed,
                k_pe,
                output_attn,
                scale,
                kv_cache_dummy_dep,
                layer_name,
            ):
                at1 = auto_functionalized(
                    MLA_ATTN_OP,
                    q=q,
                    kv_c_normed=kv_c_normed,
                    k_pe=k_pe,
                    output=output_attn,
                    layer_name=layer_name,
                    output_scale=None,
                    output_block_scale=None,
                    kv_cache_dummy_dep=kv_cache_dummy_dep,
                )
                # MLA output is already 2D (T, N*V), no reshape needed
                return self._quantize(at1[1], scale)
```

### 🔹 函式: `MLAAttnFp8StaticQuantPattern._replacement_with_ln()`
- **變更前簽章 (Before)**: `def _replacement_with_ln( # type: ignore[misc] q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep, layer_name, ): # MLA output in quant_dtype` (L107~L133)
- **變更後簽章 (After)**: `def _replacement_with_ln( # type: ignore[misc] q, kv_c_normed, k_pe, output_attn, scale, kv_cache_dummy_dep, layer_name, ): # MLA output in quant_dtype` (L124~L150)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _replacement_with_ln(  # type: ignore[misc]
                q,
                kv_c_normed,
                k_pe,
                output_attn,
                scale,
                kv_cache_dummy_dep,
                layer_name,
            ):
                # MLA output in quant_dtype
                output_attn = torch.empty(
                    [q.shape[0], self._output_dim],
                    dtype=FP8_DTYPE,
                    device=q.device,
                )
                at1 = auto_functionalized(
                    MLA_ATTN_OP,
                    q=q,
                    kv_c_normed=kv_c_normed,
                    k_pe=k_pe,
                    output=output_attn,
                    layer_name=layer_name,
                    output_scale=scale,
                    output_block_scale=None,
                    kv_cache_dummy_dep=kv_cache_dummy_dep,
                )
                return at1[1]
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _replacement_with_ln(  # type: ignore[misc]
                q,
                kv_c_normed,
                k_pe,
                output_attn,
                scale,
                kv_cache_dummy_dep,
                layer_name,
            ):
                # MLA output in quant_dtype
                output_attn = torch.empty(
                    [q.shape[0], self._output_dim],
                    dtype=FP8_DTYPE,
                    device=q.device,
                )
                at1 = auto_functionalized(
                    MLA_ATTN_OP,
                    q=q,
                    kv_c_normed=kv_c_normed,
                    k_pe=k_pe,
                    output=output_attn,
                    layer_name=layer_name,
                    output_scale=scale,
                    output_block_scale=None,
                    kv_cache_dummy_dep=kv_cache_dummy_dep,
                )
                return self._output(at1[1], scale)
```


#### 📄 檔案: `vllm/model_executor/layers/attention/mla_attention.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:210, E:303, A:0) ➔ After(N:212, E:305, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `enabled (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `rocm_aiter_per_tensor_quant (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `MLAAttention.__init__` ──[CALLS]──> `enabled (External/Unresolved)`
  • + [新增呼叫邊] `MLAAttention.forward_impl` ──[CALLS]──> `rocm_aiter_per_tensor_quant (External/Unresolved)`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'padded_rows' 被深鎖在內部閉包 (scope:build_mla_chunked_context_metadata@after/vllm/model_executor/layers/attention/mla_attention.py:L2024)，外部無法調用！ (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `MLAAttention.forward_impl()`
- **變更前簽章 (Before)**: `def forward_impl( self, q: torch.Tensor, k_c_normed: torch.Tensor, # key in unified attn k_pe: torch.Tensor, # value in unified attn kv_cache: torch.Tensor, attn_metadata: "MLACommonMetadata", output: torch.Tensor, output_scale: torch.Tensor | None = None, output_block_scale: torch.Tensor | None = None, quant_group_size: int | None = None, quant_scale_ue8m0: bool | None = None, quant_col_major: bool | None = None, quant_tma_aligned: bool | None = None, q_dcp_replicated: torch.Tensor | None = None, ) -> torch.Tensor` (L891~L1199)
- **變更後簽章 (After)**: `def forward_impl( self, q: torch.Tensor, k_c_normed: torch.Tensor, # key in unified attn k_pe: torch.Tensor, # value in unified attn kv_cache: torch.Tensor, attn_metadata: "MLACommonMetadata", output: torch.Tensor, output_scale: torch.Tensor | None = None, output_block_scale: torch.Tensor | None = None, quant_group_size: int | None = None, quant_scale_ue8m0: bool | None = None, quant_col_major: bool | None = None, quant_tma_aligned: bool | None = None, q_dcp_replicated: torch.Tensor | None = None, ) -> torch.Tensor` (L895~L1208)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def forward_impl(
        self,
        q: torch.Tensor,
        k_c_normed: torch.Tensor,  # key in unified attn
        k_pe: torch.Tensor,  # value in unified attn
        kv_cache: torch.Tensor,
        attn_metadata: "MLACommonMetadata",
        output: torch.Tensor,
        output_scale: torch.Tensor | None = None,
        output_block_scale: torch.Tensor | None = None,
        quant_group_size: int | None = None,
        quant_scale_ue8m0: bool | None = None,
        quant_col_major: bool | None = None,
        quant_tma_aligned: bool | None = None,
        q_dcp_replicated: torch.Tensor | None = None,
    ) -> torch.Tensor:
        assert output is not None, "Output tensor must be provided."

        quant_key = _detect_output_quant_key(
            output, output_scale, output_block_scale, self.num_heads * self.v_head_dim
        )
        if quant_key is not None:
            # The fusion pass has allocated output with quantized dtype
            # (FP8 or uint8 for FP4). We can't write into it directly,
            # so we swap in a temp buffer for computation, then quantize
            # into the real output at the end.
            # NOTE(carlyou): this is temporary until kernels support fp8 output
            quant_output = output
            output = torch.empty(
                output.shape[0],
                self.num_heads * self.v_head_dim,
                dtype=q.dtype,
                device=output.device,
            )

        if attn_metadata is None:
            # During the profile run try to simulate to worse case output size
            # for `self.kv_b_proj(kv_c_normed)` in `_compute_prefill_context`
            # since this can be large
            _ = torch.empty(
                (
                    self.chunked_prefill_workspace_size,
                    self.num_heads,
                    self.qk_nope_head_dim + self.v_head_dim,
                ),
                device=k_c_normed.device,
                dtype=k_c_normed.dtype,
            )
            self.impl.reserve_workspace()

            # The zero fill is required when used with DP + EP
            # to ensure all ranks within a DP group compute the
            # same expert outputs.
            if quant_key is not None:
                return quant_output.fill_(0)
            return output.fill_(0)

        fp8_attention = is_quantized_kv_cache(self.kv_cache_dtype)

        num_actual_toks = attn_metadata.num_actual_tokens
        if self.use_pcp and self.impl.dcp_world_size > 1 and quant_key is not None:
            raise NotImplementedError(
                "MRV2 MLA PCP+DCP does not support fused output quantization yet."
            )

        # Inputs and outputs may be padded for CUDA graphs
        output_padded = output
        output = output[:num_actual_toks, ...]
        q = q[:num_actual_toks, ...]
        if q_dcp_replicated is not None:
            q_dcp_replicated = q_dcp_replicated[:num_actual_toks, ...]
        k_c_normed = k_c_normed[:num_actual_toks, ...]
        k_pe = k_pe[:num_actual_toks, ...]

        if fp8_attention and self.kv_cache_dtype not in (
            # Opaque per-token byte formats stay as raw uint8
            "fp8_ds_mla",
            "nvfp4_ds_mla",
        ):
            kv_cache = kv_cache.view(current_platform.fp8_dtype())

        assert (
            attn_metadata.num_decodes is not None
            and attn_metadata.num_prefills is not None
            and attn_metadata.num_decode_tokens is not None
        )
        num_mqa_tokens = attn_metadata.num_decode_tokens
        num_mha_tokens = q.size(0) - num_mqa_tokens
        use_mha = True

        if self.impl.is_sparse and num_mha_tokens > 0:
            use_mha = self._use_sparse_mha(attn_metadata)
            if not use_mha:
                num_mqa_tokens = q.size(0)
                num_mha_tokens = 0

        mha_use_quant_output = (
            quant_key is not None
            and self.prefill_backend is not None
            and self.prefill_backend.supports_quant_output(quant_key)
            and (
                not self.impl.is_sparse
                or attn_metadata.prefill_max_seq_len  # type: ignore[attr-defined]
                <= attn_metadata.topk_tokens  # type: ignore[attr-defined]
            )
            and attn_metadata is not None
            and attn_metadata.prefill is not None
            and attn_metadata.prefill.chunked_context is None
            and self.impl.dcp_world_size <= 1
        )

        if num_mha_tokens > 0:
            if mha_use_quant_output:
                mha_output = quant_output
                mha_output_scale = output_scale
            else:
                mha_output = output
                mha_output_scale = None

            self.impl.forward_mha(  # type: ignore[attr-defined]
                q[num_mqa_tokens:],
                k_c_normed[num_mqa_tokens:],
                k_pe[num_mqa_tokens:],
                kv_cache,
                attn_metadata,
                self._k_scale,
                output=mha_output[num_mqa_tokens:num_actual_toks],
                output_scale=mha_output_scale,
            )

        if num_mqa_tokens > 0:
            if q_dcp_replicated is not None:
                mqa_q = q_dcp_replicated[:num_mqa_tokens]
                qrep_decode = True
            else:
                mqa_q = q[:num_mqa_tokens]
                qrep_decode = False
            mqa_output_slice = output[:num_mqa_tokens]

            mqa_q_nope, mqa_q_pe = mqa_q.split(
                [self.qk_nope_head_dim, self.qk_rope_head_dim], dim=-1
            )

            # Convert from (B, N, P) to (N, B, P)
            mqa_q_nope = mqa_q_nope.transpose(0, 1)

            if self.q_pad_num_heads is not None:
                B, N, L = mqa_q_pe.shape
                mqa_pe_padded = mqa_q_pe.new_empty((B, self.q_pad_num_heads, L))
                mqa_pe_padded.resize_((B, N, L))
                mqa_pe_padded.copy_(mqa_q_pe)
                mqa_q_pe = mqa_pe_padded

            if self.is_aiter_triton_fp4_bmm_enabled:
                mqa_ql_nope = rocm_aiter_ops.batched_gemm_a16wfp4(
                    mqa_q_nope,
                    self.W_K,
                    self.W_K_scale,
                    transpose_bm=True,
                    prequant=True,
                    y_scale=self._q_scale if fp8_attention else None,
                )
            elif self.is_aiter_triton_fp8_bmm_enabled:
                # Multiply+Transpose (N, B, P)x(N, P, L)->(N, B, L)->(B, N, L)
                mqa_ql_nope = rocm_aiter_ops.triton_fp8_bmm(
                    mqa_q_nope,
                    self.W_K,
                    self.W_K_scale,
                    group_size=128,
                    transpose_bm=True,
                )
            elif self.is_amx_bmm_enabled:
                # bmm_cpu computes out[n] = mat1[n] @ mat2[n]^T against
                # AMXMLAImpl's own (N, L, P) packed W_UK -- same as prefill.
                N, B, P = mqa_q_nope.shape
                L = self.kv_lora_rank
                mqa_ql_nope = mqa_q_nope.new_empty((N, B, L))
                ops.bmm_cpu(
                    mqa_ql_nope,
                    mqa_q_nope,
                    self.impl._w_uk_packed,  # type: ignore[attr-defined]
                    True,
                    self.impl._w_scale,  # type: ignore[attr-defined]
                )
                mqa_ql_nope = mqa_ql_nope.transpose(0, 1)
            else:
                # Pads the head_dim if necessary (for the underlying kernel)
                N, B, P = mqa_q_nope.shape
                W_UK_T = self.W_UK_T_dcp_qrep if qrep_decode else self.W_UK_T
                assert W_UK_T is not None
                _, _, L = W_UK_T.shape

                if self.q_pad_num_heads is not None:
                    mqa_ql_nope = mqa_q_nope.new_empty((self.q_pad_num_heads, B, L))
                    mqa_ql_nope.resize_((N, B, L))
                    # Multiply (N, B, P) x (N, P, L) -> (N, B, L)
                    torch.bmm(mqa_q_nope, W_UK_T, out=mqa_ql_nope)
                    # Convert from (N, B, L) to (B, N, L)
                    mqa_ql_nope = mqa_ql_nope.transpose(0, 1)
                else:
                    # Write the (N, B, L) bmm result straight into a
                    # token-major (B, N, L) buffer so the MQA query is already
                    # contiguous; a NoPE model (qk_rope_head_dim == 0) then
                    # needs no concat at all.
                    mqa_ql_nope = mqa_q_nope.new_empty((B, N, L))
                    torch.bmm(mqa_q_nope, W_UK_T, out=mqa_ql_nope.transpose(0, 1))

            if fp8_attention and self.impl.supports_quant_query_input:
                assert mqa_ql_nope.shape[0] == mqa_q_pe.shape[0]
                assert mqa_ql_nope.shape[1] == mqa_q_pe.shape[1]
                mqa_q = self._decode_concat_quant_fp8_op(
                    mqa_ql_nope, mqa_q_pe, self._q_scale
                )
            else:
                mqa_q = (mqa_ql_nope, mqa_q_pe)
            # concatenate nope + pe -> (B, N, L + P) (fp8 op above may have fused)
            if self.impl.dcp_world_size > 1:
                assert self.dcp_manager is not None
                if self.use_pcp:
                    if self.impl.dcp_world_size > self.impl.pcp_world_size:
                        if isinstance(mqa_q, tuple):
                            mqa_q = torch.cat(mqa_q, dim=-1)
                        mqa_q = get_tp_group().all_gather(mqa_q, dim=1)
                else:
                    if isinstance(mqa_q, tuple):
                        # concatenate mqa_ql_nope and mqa_q_pe -> (B, N, L + P)
                        mqa_q = torch.cat(mqa_q, dim=-1)
                    if not qrep_decode:
                        assert self.dcp_manager.query_gather is not None
                        mqa_q = self.dcp_manager.query_gather(mqa_q)

            # call decode attn
            if not self.impl.is_sparse:
                assert attn_metadata.decode is not None
            attn_out, lse = self.impl.forward_mqa(mqa_q, kv_cache, attn_metadata, self)  # type: ignore[attr-defined]

            # correct dcp attn_out with lse.
            if self.impl.dcp_world_size > 1:
                assert lse is not None
                assert self.dcp_manager is not None
                decode_metadata = getattr(attn_metadata, "decode", None)
                if not use_mha:
                    seq_lens = cast(torch.Tensor, attn_metadata.seq_lens)  # type: ignore[attr-defined]
                    query_start_loc = attn_metadata.query_start_loc
                else:
                    seq_lens = (
                        decode_metadata.seq_lens
                        if decode_metadata is not None
                        else cast(torch.Tensor, attn_metadata.seq_lens)[  # type: ignore[attr-defined]
                            : attn_metadata.num_decodes
                        ]
                    )
                    query_start_loc = attn_metadata.query_start_loc[
                        : attn_metadata.num_decodes + 1
                    ]
                attn_out = self.dcp_manager.combine(
                    attn_out,
                    lse,
                    seq_lens=seq_lens,
                    query_start_loc=query_start_loc,
                )
                if self.use_pcp:
                    attn_out = finalize_mla_pcp_decode(attn_out, self.num_heads)

            # v_up projection
            self._v_up_proj(attn_out, out=mqa_output_slice)

        if quant_key is not None:
            quant_idx = num_mqa_tokens if mha_use_quant_output else num_actual_toks
            if quant_idx == 0:
                return quant_output
            actual = output[:quant_idx]
            if quant_key == kNvfp4Dynamic:
                # NVFP4: two FP4 values packed into one uint8
                assert output_block_scale is not None
                fp4_data, fp4_scales = ops.scaled_fp4_quant(actual, output_scale)
                quant_output[:quant_idx].copy_(fp4_data)
                output_block_scale[: fp4_scales.shape[0]].copy_(fp4_scales)
            elif quant_key in (kFp8Dynamic128Sym, kFp8Dynamic64Sym):
                # Per-group FP8
                assert output_block_scale is not None
                assert quant_group_size is not None, (
                    "Group FP8 output quant requested but "
                    "quant_group_size not passed through custom op"
                )
                finfo = torch.finfo(_FP8_DTYPE)
                torch.ops._C.per_token_group_fp8_quant(
                    actual,
                    quant_output[:quant_idx],
                    output_block_scale[:quant_idx],
                    quant_group_size,
                    1e-10,  # eps
                    finfo.min,
                    finfo.max,
                    quant_scale_ue8m0,
                    quant_col_major,
                    quant_tma_aligned,
                )
            elif quant_key == kFp8StaticTensorSym:
                # Static FP8 quantization
                fp8_data, _ = self._quant_fp8_op(actual, output_scale)
                quant_output[:quant_idx].copy_(fp8_data)
            else:
                raise ValueError(f"Unsupported quant_key: {quant_key}")
            return quant_output

        if self.use_pcp and output_padded.shape[0] > num_actual_toks:
            output_padded[num_actual_toks:].zero_()
        return output_padded
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def forward_impl(
        self,
        q: torch.Tensor,
        k_c_normed: torch.Tensor,  # key in unified attn
        k_pe: torch.Tensor,  # value in unified attn
        kv_cache: torch.Tensor,
        attn_metadata: "MLACommonMetadata",
        output: torch.Tensor,
        output_scale: torch.Tensor | None = None,
        output_block_scale: torch.Tensor | None = None,
        quant_group_size: int | None = None,
        quant_scale_ue8m0: bool | None = None,
        quant_col_major: bool | None = None,
        quant_tma_aligned: bool | None = None,
        q_dcp_replicated: torch.Tensor | None = None,
    ) -> torch.Tensor:
        assert output is not None, "Output tensor must be provided."

        quant_key = _detect_output_quant_key(
            output, output_scale, output_block_scale, self.num_heads * self.v_head_dim
        )
        if quant_key is not None:
            # The fusion pass has allocated output with quantized dtype
            # (FP8 or uint8 for FP4). We can't write into it directly,
            # so we swap in a temp buffer for computation, then quantize
            # into the real output at the end.
            # NOTE(carlyou): this is temporary until kernels support fp8 output
            quant_output = output
            output = torch.empty(
                output.shape[0],
                self.num_heads * self.v_head_dim,
                dtype=q.dtype,
                device=output.device,
            )

        if attn_metadata is None:
            # During the profile run try to simulate to worse case output size
            # for `self.kv_b_proj(kv_c_normed)` in `_compute_prefill_context`
            # since this can be large
            _ = torch.empty(
                (
                    self.chunked_prefill_workspace_size,
                    self.num_heads,
                    self.qk_nope_head_dim + self.v_head_dim,
                ),
                device=k_c_normed.device,
                dtype=k_c_normed.dtype,
            )
            self.impl.reserve_workspace()

            # The zero fill is required when used with DP + EP
            # to ensure all ranks within a DP group compute the
            # same expert outputs.
            if quant_key is not None:
                return quant_output.fill_(0)
            return output.fill_(0)

        fp8_attention = is_quantized_kv_cache(self.kv_cache_dtype)

        num_actual_toks = attn_metadata.num_actual_tokens
        if self.use_pcp and self.impl.dcp_world_size > 1 and quant_key is not None:
            raise NotImplementedError(
                "MRV2 MLA PCP+DCP does not support fused output quantization yet."
            )

        # Inputs and outputs may be padded for CUDA graphs
        output_padded = output
        output = output[:num_actual_toks, ...]
        q = q[:num_actual_toks, ...]
        if q_dcp_replicated is not None:
            q_dcp_replicated = q_dcp_replicated[:num_actual_toks, ...]
        k_c_normed = k_c_normed[:num_actual_toks, ...]
        k_pe = k_pe[:num_actual_toks, ...]

        if fp8_attention and self.kv_cache_dtype not in (
            # Opaque per-token byte formats stay as raw uint8
            "fp8_ds_mla",
            "nvfp4_ds_mla",
        ):
            kv_cache = kv_cache.view(current_platform.fp8_dtype())

        assert (
            attn_metadata.num_decodes is not None
            and attn_metadata.num_prefills is not None
            and attn_metadata.num_decode_tokens is not None
        )
        num_mqa_tokens = attn_metadata.num_decode_tokens
        num_mha_tokens = q.size(0) - num_mqa_tokens
        use_mha = True

        if self.impl.is_sparse and num_mha_tokens > 0:
            use_mha = self._use_sparse_mha(attn_metadata)
            if not use_mha:
                num_mqa_tokens = q.size(0)
                num_mha_tokens = 0

        mha_use_quant_output = (
            quant_key is not None
            and self.prefill_backend is not None
            and self.prefill_backend.supports_quant_output(quant_key)
            and (
                not self.impl.is_sparse
                or attn_metadata.prefill_max_seq_len  # type: ignore[attr-defined]
                <= attn_metadata.topk_tokens  # type: ignore[attr-defined]
            )
            and attn_metadata is not None
            and attn_metadata.prefill is not None
            and attn_metadata.prefill.chunked_context is None
            and self.impl.dcp_world_size <= 1
        )

        if num_mha_tokens > 0:
            if mha_use_quant_output:
                mha_output = quant_output
                mha_output_scale = output_scale
            else:
                mha_output = output
                mha_output_scale = None

            self.impl.forward_mha(  # type: ignore[attr-defined]
                q[num_mqa_tokens:],
                k_c_normed[num_mqa_tokens:],
                k_pe[num_mqa_tokens:],
                kv_cache,
                attn_metadata,
                self._k_scale,
                output=mha_output[num_mqa_tokens:num_actual_toks],
                output_scale=mha_output_scale,
            )

        if num_mqa_tokens > 0:
            if q_dcp_replicated is not None:
                mqa_q = q_dcp_replicated[:num_mqa_tokens]
                qrep_decode = True
            else:
                mqa_q = q[:num_mqa_tokens]
                qrep_decode = False
            mqa_output_slice = output[:num_mqa_tokens]

            mqa_q_nope, mqa_q_pe = mqa_q.split(
                [self.qk_nope_head_dim, self.qk_rope_head_dim], dim=-1
            )

            # Convert from (B, N, P) to (N, B, P)
            mqa_q_nope = mqa_q_nope.transpose(0, 1)

            if self.q_pad_num_heads is not None:
                B, N, L = mqa_q_pe.shape
                mqa_pe_padded = mqa_q_pe.new_empty((B, self.q_pad_num_heads, L))
                mqa_pe_padded.resize_((B, N, L))
                mqa_pe_padded.copy_(mqa_q_pe)
                mqa_q_pe = mqa_pe_padded

            if self.is_aiter_triton_fp4_bmm_enabled:
                mqa_ql_nope = rocm_aiter_ops.batched_gemm_a16wfp4(
                    mqa_q_nope,
                    self.W_K,
                    self.W_K_scale,
                    transpose_bm=True,
                    prequant=True,
                    y_scale=self._q_scale if fp8_attention else None,
                )
            elif self.is_aiter_triton_fp8_bmm_enabled:
                # Multiply+Transpose (N, B, P)x(N, P, L)->(N, B, L)->(B, N, L)
                mqa_ql_nope = rocm_aiter_ops.triton_fp8_bmm(
                    mqa_q_nope,
                    self.W_K,
                    self.W_K_scale,
                    group_size=128,
                    transpose_bm=True,
                )
            elif self.is_amx_bmm_enabled:
                # bmm_cpu computes out[n] = mat1[n] @ mat2[n]^T against
                # AMXMLAImpl's own (N, L, P) packed W_UK -- same as prefill.
                N, B, P = mqa_q_nope.shape
                L = self.kv_lora_rank
                mqa_ql_nope = mqa_q_nope.new_empty((N, B, L))
                ops.bmm_cpu(
                    mqa_ql_nope,
                    mqa_q_nope,
                    self.impl._w_uk_packed,  # type: ignore[attr-defined]
                    True,
                    self.impl._w_scale,  # type: ignore[attr-defined]
                )
                mqa_ql_nope = mqa_ql_nope.transpose(0, 1)
            else:
                # Pads the head_dim if necessary (for the underlying kernel)
                N, B, P = mqa_q_nope.shape
                W_UK_T = self.W_UK_T_dcp_qrep if qrep_decode else self.W_UK_T
                assert W_UK_T is not None
                _, _, L = W_UK_T.shape

                if self.q_pad_num_heads is not None:
                    mqa_ql_nope = mqa_q_nope.new_empty((self.q_pad_num_heads, B, L))
                    mqa_ql_nope.resize_((N, B, L))
                    # Multiply (N, B, P) x (N, P, L) -> (N, B, L)
                    torch.bmm(mqa_q_nope, W_UK_T, out=mqa_ql_nope)
                    # Convert from (N, B, L) to (B, N, L)
                    mqa_ql_nope = mqa_ql_nope.transpose(0, 1)
                else:
                    # Write the (N, B, L) bmm result straight into a
                    # token-major (B, N, L) buffer so the MQA query is already
                    # contiguous; a NoPE model (qk_rope_head_dim == 0) then
                    # needs no concat at all.
                    mqa_ql_nope = mqa_q_nope.new_empty((B, N, L))
                    torch.bmm(mqa_q_nope, W_UK_T, out=mqa_ql_nope.transpose(0, 1))

            if fp8_attention and self.impl.supports_quant_query_input:
                assert mqa_ql_nope.shape[0] == mqa_q_pe.shape[0]
                assert mqa_ql_nope.shape[1] == mqa_q_pe.shape[1]
                mqa_q = self._decode_concat_quant_fp8_op(
                    mqa_ql_nope, mqa_q_pe, self._q_scale
                )
            else:
                mqa_q = (mqa_ql_nope, mqa_q_pe)
            # concatenate nope + pe -> (B, N, L + P) (fp8 op above may have fused)
            if self.impl.dcp_world_size > 1:
                assert self.dcp_manager is not None
                if self.use_pcp:
                    if self.impl.dcp_world_size > self.impl.pcp_world_size:
                        if isinstance(mqa_q, tuple):
                            mqa_q = torch.cat(mqa_q, dim=-1)
                        mqa_q = get_tp_group().all_gather(mqa_q, dim=1)
                else:
                    if isinstance(mqa_q, tuple):
                        # concatenate mqa_ql_nope and mqa_q_pe -> (B, N, L + P)
                        mqa_q = torch.cat(mqa_q, dim=-1)
                    if not qrep_decode:
                        assert self.dcp_manager.query_gather is not None
                        mqa_q = self.dcp_manager.query_gather(mqa_q)

            # call decode attn
            if not self.impl.is_sparse:
                assert attn_metadata.decode is not None
            attn_out, lse = self.impl.forward_mqa(mqa_q, kv_cache, attn_metadata, self)  # type: ignore[attr-defined]

            # correct dcp attn_out with lse.
            if self.impl.dcp_world_size > 1:
                assert lse is not None
                assert self.dcp_manager is not None
                decode_metadata = getattr(attn_metadata, "decode", None)
                if not use_mha:
                    seq_lens = cast(torch.Tensor, attn_metadata.seq_lens)  # type: ignore[attr-defined]
                    query_start_loc = attn_metadata.query_start_loc
                else:
                    seq_lens = (
                        decode_metadata.seq_lens
                        if decode_metadata is not None
                        else cast(torch.Tensor, attn_metadata.seq_lens)[  # type: ignore[attr-defined]
                            : attn_metadata.num_decodes
                        ]
                    )
                    query_start_loc = attn_metadata.query_start_loc[
                        : attn_metadata.num_decodes + 1
                    ]
                attn_out = self.dcp_manager.combine(
                    attn_out,
                    lse,
                    seq_lens=seq_lens,
                    query_start_loc=query_start_loc,
                )
                if self.use_pcp:
                    attn_out = finalize_mla_pcp_decode(attn_out, self.num_heads)

            # v_up projection
            self._v_up_proj(attn_out, out=mqa_output_slice)

        if quant_key is not None:
            quant_idx = num_mqa_tokens if mha_use_quant_output else num_actual_toks
            if quant_idx == 0:
                return quant_output
            actual = output[:quant_idx]
            if quant_key == kNvfp4Dynamic:
                # NVFP4: two FP4 values packed into one uint8
                assert output_block_scale is not None
                fp4_data, fp4_scales = ops.scaled_fp4_quant(actual, output_scale)
                quant_output[:quant_idx].copy_(fp4_data)
                output_block_scale[: fp4_scales.shape[0]].copy_(fp4_scales)
            elif quant_key in (kFp8Dynamic128Sym, kFp8Dynamic64Sym):
                # Per-group FP8
                assert output_block_scale is not None
                assert quant_group_size is not None, (
                    "Group FP8 output quant requested but "
                    "quant_group_size not passed through custom op"
                )
                finfo = torch.finfo(_FP8_DTYPE)
                torch.ops._C.per_token_group_fp8_quant(
                    actual,
                    quant_output[:quant_idx],
                    output_block_scale[:quant_idx],
                    quant_group_size,
                    1e-10,  # eps
                    finfo.min,
                    finfo.max,
                    quant_scale_ue8m0,
                    quant_col_major,
                    quant_tma_aligned,
                )
            elif quant_key == kFp8StaticTensorSym:
                # Static FP8 quantization
                if self._aiter_output_quant:
                    torch.ops.vllm.rocm_aiter_per_tensor_quant(
                        quant_output[:quant_idx], actual, output_scale, False
                    )
                else:
                    fp8_data, _ = self._quant_fp8_op(actual, output_scale)
                    quant_output[:quant_idx].copy_(fp8_data)
            else:
                raise ValueError(f"Unsupported quant_key: {quant_key}")
            return quant_output

        if self.use_pcp and output_padded.shape[0] > num_actual_toks:
            output_padded[num_actual_toks:].zero_()
        return output_padded
```

### 🔹 函式: `MLAAttention.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, num_heads: int, scale: float, qk_nope_head_dim: int, qk_rope_head_dim: int, v_head_dim: int, q_lora_rank: int | None, kv_lora_rank: int, kv_b_proj: ColumnParallelLinear, dcp_q_replicate: bool = False, cache_config: CacheConfig | None = None, quant_config: QuantizationConfig | None = None, prefix: str = "", attn_backend: type[AttentionBackend] | None = None, use_sparse: bool = False, indexer: object | None = None, topk_indices_buffer: torch.Tensor | None = None, index_group_builder: "SparseMLAIndexGroupBuilder | None" = None, non_causal_multi_token_decode: bool = False, sliding_window: int | None = None, prefill_backend_cls: type[MLAPrefillBackend] | None = None, **extra_impl_args, )` (L445~L739)
- **變更後簽章 (After)**: `def __init__( self, num_heads: int, scale: float, qk_nope_head_dim: int, qk_rope_head_dim: int, v_head_dim: int, q_lora_rank: int | None, kv_lora_rank: int, kv_b_proj: ColumnParallelLinear, dcp_q_replicate: bool = False, cache_config: CacheConfig | None = None, quant_config: QuantizationConfig | None = None, prefix: str = "", attn_backend: type[AttentionBackend] | None = None, use_sparse: bool = False, indexer: object | None = None, topk_indices_buffer: torch.Tensor | None = None, index_group_builder: "SparseMLAIndexGroupBuilder | None" = None, non_causal_multi_token_decode: bool = False, sliding_window: int | None = None, prefill_backend_cls: type[MLAPrefillBackend] | None = None, **extra_impl_args, )` (L445~L743)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        num_heads: int,
        scale: float,
        qk_nope_head_dim: int,
        qk_rope_head_dim: int,
        v_head_dim: int,
        q_lora_rank: int | None,
        kv_lora_rank: int,
        kv_b_proj: ColumnParallelLinear,
        dcp_q_replicate: bool = False,
        cache_config: CacheConfig | None = None,
        quant_config: QuantizationConfig | None = None,
        prefix: str = "",
        attn_backend: type[AttentionBackend] | None = None,
        use_sparse: bool = False,
        indexer: object | None = None,
        topk_indices_buffer: torch.Tensor | None = None,
        index_group_builder: "SparseMLAIndexGroupBuilder | None" = None,
        non_causal_multi_token_decode: bool = False,
        sliding_window: int | None = None,
        prefill_backend_cls: type[MLAPrefillBackend] | None = None,
        **extra_impl_args,
    ):
        super().__init__()
        self.num_heads = num_heads
        self.scale = scale
        self.qk_nope_head_dim = qk_nope_head_dim
        self.qk_rope_head_dim = qk_rope_head_dim
        self.v_head_dim = v_head_dim
        self.q_lora_rank = q_lora_rank
        self.kv_lora_rank = kv_lora_rank
        self.kv_b_proj = kv_b_proj
        self.dcp_q_replicate = dcp_q_replicate
        self.W_UK_T_dcp_qrep: torch.Tensor | None = None
        self.head_size = kv_lora_rank + qk_rope_head_dim
        self.layer_name = prefix
        self.indexer = indexer
        self.non_causal_multi_token_decode = non_causal_multi_token_decode
        self.sliding_window = sliding_window
        self.num_kv_heads = 1
        self.qk_head_dim = self.qk_nope_head_dim + self.qk_rope_head_dim

        if cache_config is not None:
            kv_cache_dtype: CacheDType = cache_config.cache_dtype
        else:
            kv_cache_dtype = "auto"
        self.quant_config = quant_config

        if cache_config is not None and cache_config.kv_cache_dtype_skip_layers:
            from vllm.model_executor.models.utils import extract_layer_index

            layer_idx = extract_layer_index(prefix)
            if str(layer_idx) in cache_config.kv_cache_dtype_skip_layers:
                kv_cache_dtype = "auto"
            logger.debug(
                "Layer %s: kv_cache_dtype=%s",
                prefix,
                kv_cache_dtype,
            )

        dtype = torch.get_default_dtype()
        if attn_backend is not None:
            assert attn_backend.is_mla(), (
                f"MLAAttention: attn_backend must be an MLA backend, "
                f"got {attn_backend.get_name()} instead"
            )
            self.attn_backend = attn_backend
        else:
            self.attn_backend = get_attn_backend(
                self.head_size,
                dtype,
                kv_cache_dtype,
                use_mla=True,
                use_sparse=use_sparse,
                num_heads=self.num_heads,
            )

        normalized_kv_cache_dtype = _canonicalize_sparse_mla_kv_cache_dtype(
            self.attn_backend, kv_cache_dtype
        )
        if normalized_kv_cache_dtype != kv_cache_dtype:
            if cache_config is not None:
                cache_config.cache_dtype = normalized_kv_cache_dtype
            kv_cache_dtype = normalized_kv_cache_dtype
            logger.info_once(
                "Using %s KV cache format for %s backend.",
                kv_cache_dtype,
                self.attn_backend.get_name(),
            )

        if (
            self.attn_backend.get_name() == "FLASHINFER_MLA_SPARSE"
            and kv_cache_dtype != "fp8_ds_mla"
            and is_quantized_kv_cache(kv_cache_dtype)
        ):
            logger.info_once(
                "Using standard fp8 KV cache format. To use DeepSeek's fp8_ds_mla "
                "KV cache format, please set `--attention-backend FLASHMLA_SPARSE`"
            )

        # Initialize KV cache quantization attributes
        self.kv_cache_dtype = kv_cache_dtype
        _init_kv_cache_quant(self, quant_config, prefix)

        if (
            cache_config is not None
            and cache_config.enable_prefix_caching
            and envs.VLLM_BATCH_INVARIANT
            and (
                self.attn_backend.get_name() == "TRITON_MLA"
                or self.attn_backend.get_name() == "FLASHINFER"
            )
        ):
            logger.warning_once(
                "Disabling prefix caching for TRITON_MLA / FLASHINFER "
                "with batch invariance, as it is not yet supported.",
            )
            cache_config.enable_prefix_caching = False

        # Sparse MLA reads top-k indices from a shared buffer. Pass it
        # explicitly so backbone "skip" layers (indexer=None) still find it.
        if use_sparse:
            extra_impl_args["topk_indices_buffer"] = topk_indices_buffer
            if index_group_builder is not None:
                extra_impl_args["index_group_builder"] = index_group_builder

        impl_cls = cast(type[MLAAttentionImpl], self.attn_backend.get_impl_cls())
        impl = impl_cls(
            num_heads=self.num_heads,
            head_size=self.head_size,
            scale=self.scale,
            num_kv_heads=1,
            alibi_slopes=None,
            sliding_window=sliding_window,
            kv_cache_dtype=self.kv_cache_dtype,
            logits_soft_cap=None,
            attn_type=AttentionType.DECODER,
            kv_sharing_target_layer_name=None,
            # MLA Args
            q_lora_rank=self.q_lora_rank,
            kv_lora_rank=self.kv_lora_rank,
            qk_nope_head_dim=self.qk_nope_head_dim,
            qk_rope_head_dim=self.qk_rope_head_dim,
            qk_head_dim=self.qk_nope_head_dim + self.qk_rope_head_dim,
            v_head_dim=self.v_head_dim,
            kv_b_proj=kv_b_proj,
            indexer=indexer,
            **extra_impl_args,
        )
        self.impl = impl  # type: ignore[assignment]
        index_group = getattr(impl, "index_group", None)
        self.hisparse_cache = (
            index_group.cache(cast(Any, impl).index_group_index)
            if isinstance(index_group, HiSparseMLAIndexGroup)
            else None
        )
        self.q_pad_num_heads = getattr(self.impl, "q_pad_num_heads", None)
        self.is_amx_bmm_enabled = getattr(self.impl, "uses_amx_bmm", False)
        # AMX reads kv_b_proj's weight directly and never calls it live; the
        # reference CPU MLA backend calls it but isn't perf-critical. Skip
        # the packed-kernel dispatch either way.
        kv_b_proj._cpu_skip_gemm_dispatch = True
        self.use_direct_call = not current_platform.opaque_attention_op()

        vllm_config = get_current_vllm_config()
        parallel_config = vllm_config.parallel_config
        self.use_pcp = parallel_config.prefill_context_parallel_size > 1
        self.pcp_shard_decode_requests = parallel_config.pcp_shard_decode_requests
        compilation_config = vllm_config.compilation_config
        if prefix in compilation_config.static_forward_context:
            raise ValueError(f"Duplicate layer name: {prefix}")
        compilation_config.static_forward_context[prefix] = self

        self.prefill_backend: MLAPrefillBackend | None
        if self.impl.is_sparse and not (
            self.impl.supports_dense_mha_prefill and self.supports_dense_mha_prefill
        ):
            logger.warning_once(
                "Sparse MLA layer has no dense-MHA prefill path; using the top-k "
                "MQA path only."
            )
            self.prefill_backend = None
        else:
            try:
                prefill_backend_cls = prefill_backend_cls or get_mla_prefill_backend(
                    vllm_config
                )
            except ValueError:
                if (
                    not self.impl.is_sparse
                    or vllm_config.attention_config.mla_prefill_backend is not None
                ):
                    raise
                logger.warning_once(
                    "No MLA prefill backend supports this model; sparse MLA will "
                    "use the top-k MQA path only (no dense-MHA prefill)."
                )
                self.prefill_backend = None
            else:
                self.prefill_backend = prefill_backend_cls(
                    num_heads=self.num_heads,
                    scale=self.scale,
                    kv_lora_rank=self.kv_lora_rank,
                    qk_nope_head_dim=self.qk_nope_head_dim,
                    qk_rope_head_dim=self.qk_rope_head_dim,
                    v_head_dim=self.v_head_dim,
                    vllm_config=vllm_config,
                )

        self.kv_cache = torch.tensor([])

        self.use_sparse = use_sparse

        if vllm_config.kernel_config.enable_jit_warmup:
            backend_name = self.attn_backend.get_name()
            if backend_name in (
                "FLASHMLA_SPARSE",
                "FLASHINFER_MLA_SPARSE",
                "FLASHINFER_MLA_SPARSE_SM120",
                "FLASH_ATTN_MLA_SPARSE_FA4",
                "DEEPSEEK_V32_INDEXER",
            ):
                from vllm.v1.attention.backends.mla.compressor_utils import (
                    _COMPRESSED_SLOT_MAPPING_KERNEL,
                )
                from vllm.v1.attention.backends.mla.indexer import (
                    _BUILD_PREFILL_CHUNK_METADATA_KERNEL,
                    _PREPARE_UNIFORM_DECODE_KERNEL,
                )

                _COMPRESSED_SLOT_MAPPING_KERNEL.register_warmup()
                _PREPARE_UNIFORM_DECODE_KERNEL.register_warmup()
                _BUILD_PREFILL_CHUNK_METADATA_KERNEL.register_warmup()

                if backend_name != "DEEPSEEK_V32_INDEXER":
                    from vllm.v1.attention.backends.mla.sparse_swa import (
                        _COMPUTE_PREFILL_METADATA_KERNEL,
                    )

                    _COMPUTE_PREFILL_METADATA_KERNEL.register_warmup()

        if self.use_pcp and self.impl.dcp_world_size > 1 and not self.supports_pcp_dcp:
            raise NotImplementedError(
                f"{type(self).__name__} does not support PCP+DCP."
            )
        self.dcp_manager: MLADCPManager | None = None
        if self.impl.dcp_world_size > 1:
            query_dtype = (
                current_platform.fp8_dtype()
                if is_quantized_kv_cache(self.kv_cache_dtype)
                and self.kv_cache_dtype != "fp8_ds_mla"
                and self.impl.supports_quant_query_input
                else dtype
            )
            self.dcp_manager = MLADCPManager(
                vllm_config=vllm_config,
                device=next(kv_b_proj.parameters()).device,
                num_heads=self.num_heads,
                query_head_dim=self.kv_lora_rank + self.qk_rope_head_dim,
                output_head_dim=self.kv_lora_rank,
                query_dtype=query_dtype,
                output_dtype=dtype,
                padded_num_heads=self.q_pad_num_heads,
                is_lse_base_on_e=self.impl.lse_base_on_e,
                use_pcp=self.use_pcp,
            )

        # TODO(ROCm): both BMM kernels re-quantize kv_b_proj online, ignoring
        # the precision the checkpoint asked for, so they now default to off.
        # Turning them back on needs long-context accuracy validation, and the
        # per-layer decision belongs in --quantization-config.targets rather
        # than in this layer.
        self.is_aiter_triton_fp8_bmm_enabled = rocm_aiter_ops.is_fp8bmm_enabled()

        # If kv_b_proj_weight is unquantized, quantize it to mxfp4 if supported
        self.is_aiter_triton_fp4_bmm_enabled = (
            rocm_aiter_ops.is_fp4bmm_enabled()
            and hasattr(self.kv_b_proj, "weight")
            and self.kv_b_proj.weight.dtype == torch.bfloat16
        )

        # Attributes for forward_impl method
        self._vllm_config = get_current_vllm_config()
        self._chunked_prefill_workspace_size: int | None = None
        self._decode_concat_quant_fp8_op = _DecodeConcatQuantFP8(
            static=True,
            group_shape=GroupShape.PER_TENSOR,
            compile_native=True,
        )
        self._quant_fp8_op = QuantFP8(
            static=True,
            group_shape=GroupShape.PER_TENSOR,
            compile_native=True,
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        num_heads: int,
        scale: float,
        qk_nope_head_dim: int,
        qk_rope_head_dim: int,
        v_head_dim: int,
        q_lora_rank: int | None,
        kv_lora_rank: int,
        kv_b_proj: ColumnParallelLinear,
        dcp_q_replicate: bool = False,
        cache_config: CacheConfig | None = None,
        quant_config: QuantizationConfig | None = None,
        prefix: str = "",
        attn_backend: type[AttentionBackend] | None = None,
        use_sparse: bool = False,
        indexer: object | None = None,
        topk_indices_buffer: torch.Tensor | None = None,
        index_group_builder: "SparseMLAIndexGroupBuilder | None" = None,
        non_causal_multi_token_decode: bool = False,
        sliding_window: int | None = None,
        prefill_backend_cls: type[MLAPrefillBackend] | None = None,
        **extra_impl_args,
    ):
        super().__init__()
        self.num_heads = num_heads
        self.scale = scale
        self.qk_nope_head_dim = qk_nope_head_dim
        self.qk_rope_head_dim = qk_rope_head_dim
        self.v_head_dim = v_head_dim
        self.q_lora_rank = q_lora_rank
        self.kv_lora_rank = kv_lora_rank
        self.kv_b_proj = kv_b_proj
        self.dcp_q_replicate = dcp_q_replicate
        self.W_UK_T_dcp_qrep: torch.Tensor | None = None
        self.head_size = kv_lora_rank + qk_rope_head_dim
        self.layer_name = prefix
        self.indexer = indexer
        self.non_causal_multi_token_decode = non_causal_multi_token_decode
        self.sliding_window = sliding_window
        self.num_kv_heads = 1
        self.qk_head_dim = self.qk_nope_head_dim + self.qk_rope_head_dim

        if cache_config is not None:
            kv_cache_dtype: CacheDType = cache_config.cache_dtype
        else:
            kv_cache_dtype = "auto"
        self.quant_config = quant_config

        if cache_config is not None and cache_config.kv_cache_dtype_skip_layers:
            from vllm.model_executor.models.utils import extract_layer_index

            layer_idx = extract_layer_index(prefix)
            if str(layer_idx) in cache_config.kv_cache_dtype_skip_layers:
                kv_cache_dtype = "auto"
            logger.debug(
                "Layer %s: kv_cache_dtype=%s",
                prefix,
                kv_cache_dtype,
            )

        dtype = torch.get_default_dtype()
        if attn_backend is not None:
            assert attn_backend.is_mla(), (
                f"MLAAttention: attn_backend must be an MLA backend, "
                f"got {attn_backend.get_name()} instead"
            )
            self.attn_backend = attn_backend
        else:
            self.attn_backend = get_attn_backend(
                self.head_size,
                dtype,
                kv_cache_dtype,
                use_mla=True,
                use_sparse=use_sparse,
                num_heads=self.num_heads,
            )

        normalized_kv_cache_dtype = _canonicalize_sparse_mla_kv_cache_dtype(
            self.attn_backend, kv_cache_dtype
        )
        if normalized_kv_cache_dtype != kv_cache_dtype:
            if cache_config is not None:
                cache_config.cache_dtype = normalized_kv_cache_dtype
            kv_cache_dtype = normalized_kv_cache_dtype
            logger.info_once(
                "Using %s KV cache format for %s backend.",
                kv_cache_dtype,
                self.attn_backend.get_name(),
            )

        if (
            self.attn_backend.get_name() == "FLASHINFER_MLA_SPARSE"
            and kv_cache_dtype != "fp8_ds_mla"
            and is_quantized_kv_cache(kv_cache_dtype)
        ):
            logger.info_once(
                "Using standard fp8 KV cache format. To use DeepSeek's fp8_ds_mla "
                "KV cache format, please set `--attention-backend FLASHMLA_SPARSE`"
            )

        # Initialize KV cache quantization attributes
        self.kv_cache_dtype = kv_cache_dtype
        _init_kv_cache_quant(self, quant_config, prefix)

        if (
            cache_config is not None
            and cache_config.enable_prefix_caching
            and envs.VLLM_BATCH_INVARIANT
            and (
                self.attn_backend.get_name() == "TRITON_MLA"
                or self.attn_backend.get_name() == "FLASHINFER"
            )
        ):
            logger.warning_once(
                "Disabling prefix caching for TRITON_MLA / FLASHINFER "
                "with batch invariance, as it is not yet supported.",
            )
            cache_config.enable_prefix_caching = False

        # Sparse MLA reads top-k indices from a shared buffer. Pass it
        # explicitly so backbone "skip" layers (indexer=None) still find it.
        if use_sparse:
            extra_impl_args["topk_indices_buffer"] = topk_indices_buffer
            if index_group_builder is not None:
                extra_impl_args["index_group_builder"] = index_group_builder

        impl_cls = cast(type[MLAAttentionImpl], self.attn_backend.get_impl_cls())
        impl = impl_cls(
            num_heads=self.num_heads,
            head_size=self.head_size,
            scale=self.scale,
            num_kv_heads=1,
            alibi_slopes=None,
            sliding_window=sliding_window,
            kv_cache_dtype=self.kv_cache_dtype,
            logits_soft_cap=None,
            attn_type=AttentionType.DECODER,
            kv_sharing_target_layer_name=None,
            # MLA Args
            q_lora_rank=self.q_lora_rank,
            kv_lora_rank=self.kv_lora_rank,
            qk_nope_head_dim=self.qk_nope_head_dim,
            qk_rope_head_dim=self.qk_rope_head_dim,
            qk_head_dim=self.qk_nope_head_dim + self.qk_rope_head_dim,
            v_head_dim=self.v_head_dim,
            kv_b_proj=kv_b_proj,
            indexer=indexer,
            **extra_impl_args,
        )
        self.impl = impl  # type: ignore[assignment]
        index_group = getattr(impl, "index_group", None)
        self.hisparse_cache = (
            index_group.cache(cast(Any, impl).index_group_index)
            if isinstance(index_group, HiSparseMLAIndexGroup)
            else None
        )
        self.q_pad_num_heads = getattr(self.impl, "q_pad_num_heads", None)
        self.is_amx_bmm_enabled = getattr(self.impl, "uses_amx_bmm", False)
        # AMX reads kv_b_proj's weight directly and never calls it live; the
        # reference CPU MLA backend calls it but isn't perf-critical. Skip
        # the packed-kernel dispatch either way.
        kv_b_proj._cpu_skip_gemm_dispatch = True
        self.use_direct_call = not current_platform.opaque_attention_op()

        vllm_config = get_current_vllm_config()
        parallel_config = vllm_config.parallel_config
        self.use_pcp = parallel_config.prefill_context_parallel_size > 1
        self.pcp_shard_decode_requests = parallel_config.pcp_shard_decode_requests
        compilation_config = vllm_config.compilation_config
        if prefix in compilation_config.static_forward_context:
            raise ValueError(f"Duplicate layer name: {prefix}")
        compilation_config.static_forward_context[prefix] = self

        self.prefill_backend: MLAPrefillBackend | None
        if self.impl.is_sparse and not (
            self.impl.supports_dense_mha_prefill and self.supports_dense_mha_prefill
        ):
            logger.warning_once(
                "Sparse MLA layer has no dense-MHA prefill path; using the top-k "
                "MQA path only."
            )
            self.prefill_backend = None
        else:
            try:
                prefill_backend_cls = prefill_backend_cls or get_mla_prefill_backend(
                    vllm_config
                )
            except ValueError:
                if (
                    not self.impl.is_sparse
                    or vllm_config.attention_config.mla_prefill_backend is not None
                ):
                    raise
                logger.warning_once(
                    "No MLA prefill backend supports this model; sparse MLA will "
                    "use the top-k MQA path only (no dense-MHA prefill)."
                )
                self.prefill_backend = None
            else:
                self.prefill_backend = prefill_backend_cls(
                    num_heads=self.num_heads,
                    scale=self.scale,
                    kv_lora_rank=self.kv_lora_rank,
                    qk_nope_head_dim=self.qk_nope_head_dim,
                    qk_rope_head_dim=self.qk_rope_head_dim,
                    v_head_dim=self.v_head_dim,
                    vllm_config=vllm_config,
                )

        self.kv_cache = torch.tensor([])

        self.use_sparse = use_sparse

        if vllm_config.kernel_config.enable_jit_warmup:
            backend_name = self.attn_backend.get_name()
            if backend_name in (
                "FLASHMLA_SPARSE",
                "FLASHINFER_MLA_SPARSE",
                "FLASHINFER_MLA_SPARSE_SM120",
                "FLASH_ATTN_MLA_SPARSE_FA4",
                "DEEPSEEK_V32_INDEXER",
            ):
                from vllm.v1.attention.backends.mla.compressor_utils import (
                    _COMPRESSED_SLOT_MAPPING_KERNEL,
                )
                from vllm.v1.attention.backends.mla.indexer import (
                    _BUILD_PREFILL_CHUNK_METADATA_KERNEL,
                    _PREPARE_UNIFORM_DECODE_KERNEL,
                )

                _COMPRESSED_SLOT_MAPPING_KERNEL.register_warmup()
                _PREPARE_UNIFORM_DECODE_KERNEL.register_warmup()
                _BUILD_PREFILL_CHUNK_METADATA_KERNEL.register_warmup()

                if backend_name != "DEEPSEEK_V32_INDEXER":
                    from vllm.v1.attention.backends.mla.sparse_swa import (
                        _COMPUTE_PREFILL_METADATA_KERNEL,
                    )

                    _COMPUTE_PREFILL_METADATA_KERNEL.register_warmup()

        if self.use_pcp and self.impl.dcp_world_size > 1 and not self.supports_pcp_dcp:
            raise NotImplementedError(
                f"{type(self).__name__} does not support PCP+DCP."
            )
        self.dcp_manager: MLADCPManager | None = None
        if self.impl.dcp_world_size > 1:
            query_dtype = (
                current_platform.fp8_dtype()
                if is_quantized_kv_cache(self.kv_cache_dtype)
                and self.kv_cache_dtype != "fp8_ds_mla"
                and self.impl.supports_quant_query_input
                else dtype
            )
            self.dcp_manager = MLADCPManager(
                vllm_config=vllm_config,
                device=next(kv_b_proj.parameters()).device,
                num_heads=self.num_heads,
                query_head_dim=self.kv_lora_rank + self.qk_rope_head_dim,
                output_head_dim=self.kv_lora_rank,
                query_dtype=query_dtype,
                output_dtype=dtype,
                padded_num_heads=self.q_pad_num_heads,
                is_lse_base_on_e=self.impl.lse_base_on_e,
                use_pcp=self.use_pcp,
            )

        # TODO(ROCm): both BMM kernels re-quantize kv_b_proj online, ignoring
        # the precision the checkpoint asked for, so they now default to off.
        # Turning them back on needs long-context accuracy validation, and the
        # per-layer decision belongs in --quantization-config.targets rather
        # than in this layer.
        self.is_aiter_triton_fp8_bmm_enabled = rocm_aiter_ops.is_fp8bmm_enabled()

        # If kv_b_proj_weight is unquantized, quantize it to mxfp4 if supported
        self.is_aiter_triton_fp4_bmm_enabled = (
            rocm_aiter_ops.is_fp4bmm_enabled()
            and hasattr(self.kv_b_proj, "weight")
            and self.kv_b_proj.weight.dtype == torch.bfloat16
        )

        # Attributes for forward_impl method
        self._vllm_config = get_current_vllm_config()
        self._chunked_prefill_workspace_size: int | None = None
        self._decode_concat_quant_fp8_op = _DecodeConcatQuantFP8(
            static=True,
            group_shape=GroupShape.PER_TENSOR,
            compile_native=True,
        )
        self._quant_fp8_op = QuantFP8(
            static=True,
            group_shape=GroupShape.PER_TENSOR,
            compile_native=True,
        )
        # Matches the graph quant replaced by fusion; writes into the output.
        self._aiter_output_quant = (
            self._quant_fp8_op.use_aiter and self._quant_fp8_op.enabled()
        )
```


---

### 🔹 Commit #12: `689effee`
- **完整 Hash**: `689effee6d07bfeb0afe42d44046141657238c23`
- **說明 (Ground Truth)**: [Bugfix][Attention] Fix Triton MLA decode int32 overflow and logits workspace accounting (#61938)
- **變更檔案數**: 4

#### 📄 檔案: `vllm/model_executor/layers/attention/mla_attention.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:209, E:302, A:0) ➔ After(N:210, E:303, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `reserve_workspace (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `MLAAttention.forward_impl` ──[CALLS]──> `reserve_workspace (External/Unresolved)`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'padded_rows' 被深鎖在內部閉包 (scope:build_mla_chunked_context_metadata@after/vllm/model_executor/layers/attention/mla_attention.py:L2015)，外部無法調用！ (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `MLAAttention.forward_impl()`
- **變更前簽章 (Before)**: `def forward_impl( self, q: torch.Tensor, k_c_normed: torch.Tensor, # key in unified attn k_pe: torch.Tensor, # value in unified attn kv_cache: torch.Tensor, attn_metadata: "MLACommonMetadata", output: torch.Tensor, output_scale: torch.Tensor | None = None, output_block_scale: torch.Tensor | None = None, quant_group_size: int | None = None, quant_scale_ue8m0: bool | None = None, quant_col_major: bool | None = None, quant_tma_aligned: bool | None = None, q_dcp_replicated: torch.Tensor | None = None, ) -> torch.Tensor` (L891~L1198)
- **變更後簽章 (After)**: `def forward_impl( self, q: torch.Tensor, k_c_normed: torch.Tensor, # key in unified attn k_pe: torch.Tensor, # value in unified attn kv_cache: torch.Tensor, attn_metadata: "MLACommonMetadata", output: torch.Tensor, output_scale: torch.Tensor | None = None, output_block_scale: torch.Tensor | None = None, quant_group_size: int | None = None, quant_scale_ue8m0: bool | None = None, quant_col_major: bool | None = None, quant_tma_aligned: bool | None = None, q_dcp_replicated: torch.Tensor | None = None, ) -> torch.Tensor` (L891~L1199)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def forward_impl(
        self,
        q: torch.Tensor,
        k_c_normed: torch.Tensor,  # key in unified attn
        k_pe: torch.Tensor,  # value in unified attn
        kv_cache: torch.Tensor,
        attn_metadata: "MLACommonMetadata",
        output: torch.Tensor,
        output_scale: torch.Tensor | None = None,
        output_block_scale: torch.Tensor | None = None,
        quant_group_size: int | None = None,
        quant_scale_ue8m0: bool | None = None,
        quant_col_major: bool | None = None,
        quant_tma_aligned: bool | None = None,
        q_dcp_replicated: torch.Tensor | None = None,
    ) -> torch.Tensor:
        assert output is not None, "Output tensor must be provided."

        quant_key = _detect_output_quant_key(
            output, output_scale, output_block_scale, self.num_heads * self.v_head_dim
        )
        if quant_key is not None:
            # The fusion pass has allocated output with quantized dtype
            # (FP8 or uint8 for FP4). We can't write into it directly,
            # so we swap in a temp buffer for computation, then quantize
            # into the real output at the end.
            # NOTE(carlyou): this is temporary until kernels support fp8 output
            quant_output = output
            output = torch.empty(
                output.shape[0],
                self.num_heads * self.v_head_dim,
                dtype=q.dtype,
                device=output.device,
            )

        if attn_metadata is None:
            # During the profile run try to simulate to worse case output size
            # for `self.kv_b_proj(kv_c_normed)` in `_compute_prefill_context`
            # since this can be large
            _ = torch.empty(
                (
                    self.chunked_prefill_workspace_size,
                    self.num_heads,
                    self.qk_nope_head_dim + self.v_head_dim,
                ),
                device=k_c_normed.device,
                dtype=k_c_normed.dtype,
            )

            # The zero fill is required when used with DP + EP
            # to ensure all ranks within a DP group compute the
            # same expert outputs.
            if quant_key is not None:
                return quant_output.fill_(0)
            return output.fill_(0)

        fp8_attention = is_quantized_kv_cache(self.kv_cache_dtype)

        num_actual_toks = attn_metadata.num_actual_tokens
        if self.use_pcp and self.impl.dcp_world_size > 1 and quant_key is not None:
            raise NotImplementedError(
                "MRV2 MLA PCP+DCP does not support fused output quantization yet."
            )

        # Inputs and outputs may be padded for CUDA graphs
        output_padded = output
        output = output[:num_actual_toks, ...]
        q = q[:num_actual_toks, ...]
        if q_dcp_replicated is not None:
            q_dcp_replicated = q_dcp_replicated[:num_actual_toks, ...]
        k_c_normed = k_c_normed[:num_actual_toks, ...]
        k_pe = k_pe[:num_actual_toks, ...]

        if fp8_attention and self.kv_cache_dtype not in (
            # Opaque per-token byte formats stay as raw uint8
            "fp8_ds_mla",
            "nvfp4_ds_mla",
        ):
            kv_cache = kv_cache.view(current_platform.fp8_dtype())

        assert (
            attn_metadata.num_decodes is not None
            and attn_metadata.num_prefills is not None
            and attn_metadata.num_decode_tokens is not None
        )
        num_mqa_tokens = attn_metadata.num_decode_tokens
        num_mha_tokens = q.size(0) - num_mqa_tokens
        use_mha = True

        if self.impl.is_sparse and num_mha_tokens > 0:
            use_mha = self._use_sparse_mha(attn_metadata)
            if not use_mha:
                num_mqa_tokens = q.size(0)
                num_mha_tokens = 0

        mha_use_quant_output = (
            quant_key is not None
            and self.prefill_backend is not None
            and self.prefill_backend.supports_quant_output(quant_key)
            and (
                not self.impl.is_sparse
                or attn_metadata.prefill_max_seq_len  # type: ignore[attr-defined]
                <= attn_metadata.topk_tokens  # type: ignore[attr-defined]
            )
            and attn_metadata is not None
            and attn_metadata.prefill is not None
            and attn_metadata.prefill.chunked_context is None
            and self.impl.dcp_world_size <= 1
        )

        if num_mha_tokens > 0:
            if mha_use_quant_output:
                mha_output = quant_output
                mha_output_scale = output_scale
            else:
                mha_output = output
                mha_output_scale = None

            self.impl.forward_mha(  # type: ignore[attr-defined]
                q[num_mqa_tokens:],
                k_c_normed[num_mqa_tokens:],
                k_pe[num_mqa_tokens:],
                kv_cache,
                attn_metadata,
                self._k_scale,
                output=mha_output[num_mqa_tokens:num_actual_toks],
                output_scale=mha_output_scale,
            )

        if num_mqa_tokens > 0:
            if q_dcp_replicated is not None:
                mqa_q = q_dcp_replicated[:num_mqa_tokens]
                qrep_decode = True
            else:
                mqa_q = q[:num_mqa_tokens]
                qrep_decode = False
            mqa_output_slice = output[:num_mqa_tokens]

            mqa_q_nope, mqa_q_pe = mqa_q.split(
                [self.qk_nope_head_dim, self.qk_rope_head_dim], dim=-1
            )

            # Convert from (B, N, P) to (N, B, P)
            mqa_q_nope = mqa_q_nope.transpose(0, 1)

            if self.q_pad_num_heads is not None:
                B, N, L = mqa_q_pe.shape
                mqa_pe_padded = mqa_q_pe.new_empty((B, self.q_pad_num_heads, L))
                mqa_pe_padded.resize_((B, N, L))
                mqa_pe_padded.copy_(mqa_q_pe)
                mqa_q_pe = mqa_pe_padded

            if self.is_aiter_triton_fp4_bmm_enabled:
                mqa_ql_nope = rocm_aiter_ops.batched_gemm_a16wfp4(
                    mqa_q_nope,
                    self.W_K,
                    self.W_K_scale,
                    transpose_bm=True,
                    prequant=True,
                    y_scale=self._q_scale if fp8_attention else None,
                )
            elif self.is_aiter_triton_fp8_bmm_enabled:
                # Multiply+Transpose (N, B, P)x(N, P, L)->(N, B, L)->(B, N, L)
                mqa_ql_nope = rocm_aiter_ops.triton_fp8_bmm(
                    mqa_q_nope,
                    self.W_K,
                    self.W_K_scale,
                    group_size=128,
                    transpose_bm=True,
                )
            elif self.is_amx_bmm_enabled:
                # bmm_cpu computes out[n] = mat1[n] @ mat2[n]^T against
                # AMXMLAImpl's own (N, L, P) packed W_UK -- same as prefill.
                N, B, P = mqa_q_nope.shape
                L = self.kv_lora_rank
                mqa_ql_nope = mqa_q_nope.new_empty((N, B, L))
                ops.bmm_cpu(
                    mqa_ql_nope,
                    mqa_q_nope,
                    self.impl._w_uk_packed,  # type: ignore[attr-defined]
                    True,
                    self.impl._w_scale,  # type: ignore[attr-defined]
                )
                mqa_ql_nope = mqa_ql_nope.transpose(0, 1)
            else:
                # Pads the head_dim if necessary (for the underlying kernel)
                N, B, P = mqa_q_nope.shape
                W_UK_T = self.W_UK_T_dcp_qrep if qrep_decode else self.W_UK_T
                assert W_UK_T is not None
                _, _, L = W_UK_T.shape

                if self.q_pad_num_heads is not None:
                    mqa_ql_nope = mqa_q_nope.new_empty((self.q_pad_num_heads, B, L))
                    mqa_ql_nope.resize_((N, B, L))
                    # Multiply (N, B, P) x (N, P, L) -> (N, B, L)
                    torch.bmm(mqa_q_nope, W_UK_T, out=mqa_ql_nope)
                    # Convert from (N, B, L) to (B, N, L)
                    mqa_ql_nope = mqa_ql_nope.transpose(0, 1)
                else:
                    # Write the (N, B, L) bmm result straight into a
                    # token-major (B, N, L) buffer so the MQA query is already
                    # contiguous; a NoPE model (qk_rope_head_dim == 0) then
                    # needs no concat at all.
                    mqa_ql_nope = mqa_q_nope.new_empty((B, N, L))
                    torch.bmm(mqa_q_nope, W_UK_T, out=mqa_ql_nope.transpose(0, 1))

            if fp8_attention and self.impl.supports_quant_query_input:
                assert mqa_ql_nope.shape[0] == mqa_q_pe.shape[0]
                assert mqa_ql_nope.shape[1] == mqa_q_pe.shape[1]
                mqa_q = self._decode_concat_quant_fp8_op(
                    mqa_ql_nope, mqa_q_pe, self._q_scale
                )
            else:
                mqa_q = (mqa_ql_nope, mqa_q_pe)
            # concatenate nope + pe -> (B, N, L + P) (fp8 op above may have fused)
            if self.impl.dcp_world_size > 1:
                assert self.dcp_manager is not None
                if self.use_pcp:
                    if self.impl.dcp_world_size > self.impl.pcp_world_size:
                        if isinstance(mqa_q, tuple):
                            mqa_q = torch.cat(mqa_q, dim=-1)
                        mqa_q = get_tp_group().all_gather(mqa_q, dim=1)
                else:
                    if isinstance(mqa_q, tuple):
                        # concatenate mqa_ql_nope and mqa_q_pe -> (B, N, L + P)
                        mqa_q = torch.cat(mqa_q, dim=-1)
                    if not qrep_decode:
                        assert self.dcp_manager.query_gather is not None
                        mqa_q = self.dcp_manager.query_gather(mqa_q)

            # call decode attn
            if not self.impl.is_sparse:
                assert attn_metadata.decode is not None
            attn_out, lse = self.impl.forward_mqa(mqa_q, kv_cache, attn_metadata, self)  # type: ignore[attr-defined]

            # correct dcp attn_out with lse.
            if self.impl.dcp_world_size > 1:
                assert lse is not None
                assert self.dcp_manager is not None
                decode_metadata = getattr(attn_metadata, "decode", None)
                if not use_mha:
                    seq_lens = cast(torch.Tensor, attn_metadata.seq_lens)  # type: ignore[attr-defined]
                    query_start_loc = attn_metadata.query_start_loc
                else:
                    seq_lens = (
                        decode_metadata.seq_lens
                        if decode_metadata is not None
                        else cast(torch.Tensor, attn_metadata.seq_lens)[  # type: ignore[attr-defined]
                            : attn_metadata.num_decodes
                        ]
                    )
                    query_start_loc = attn_metadata.query_start_loc[
                        : attn_metadata.num_decodes + 1
                    ]
                attn_out = self.dcp_manager.combine(
                    attn_out,
                    lse,
                    seq_lens=seq_lens,
                    query_start_loc=query_start_loc,
                )
                if self.use_pcp:
                    attn_out = finalize_mla_pcp_decode(attn_out, self.num_heads)

            # v_up projection
            self._v_up_proj(attn_out, out=mqa_output_slice)

        if quant_key is not None:
            quant_idx = num_mqa_tokens if mha_use_quant_output else num_actual_toks
            if quant_idx == 0:
                return quant_output
            actual = output[:quant_idx]
            if quant_key == kNvfp4Dynamic:
                # NVFP4: two FP4 values packed into one uint8
                assert output_block_scale is not None
                fp4_data, fp4_scales = ops.scaled_fp4_quant(actual, output_scale)
                quant_output[:quant_idx].copy_(fp4_data)
                output_block_scale[: fp4_scales.shape[0]].copy_(fp4_scales)
            elif quant_key in (kFp8Dynamic128Sym, kFp8Dynamic64Sym):
                # Per-group FP8
                assert output_block_scale is not None
                assert quant_group_size is not None, (
                    "Group FP8 output quant requested but "
                    "quant_group_size not passed through custom op"
                )
                finfo = torch.finfo(_FP8_DTYPE)
                torch.ops._C.per_token_group_fp8_quant(
                    actual,
                    quant_output[:quant_idx],
                    output_block_scale[:quant_idx],
                    quant_group_size,
                    1e-10,  # eps
                    finfo.min,
                    finfo.max,
                    quant_scale_ue8m0,
                    quant_col_major,
                    quant_tma_aligned,
                )
            elif quant_key == kFp8StaticTensorSym:
                # Static FP8 quantization
                fp8_data, _ = self._quant_fp8_op(actual, output_scale)
                quant_output[:quant_idx].copy_(fp8_data)
            else:
                raise ValueError(f"Unsupported quant_key: {quant_key}")
            return quant_output

        if self.use_pcp and output_padded.shape[0] > num_actual_toks:
            output_padded[num_actual_toks:].zero_()
        return output_padded
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def forward_impl(
        self,
        q: torch.Tensor,
        k_c_normed: torch.Tensor,  # key in unified attn
        k_pe: torch.Tensor,  # value in unified attn
        kv_cache: torch.Tensor,
        attn_metadata: "MLACommonMetadata",
        output: torch.Tensor,
        output_scale: torch.Tensor | None = None,
        output_block_scale: torch.Tensor | None = None,
        quant_group_size: int | None = None,
        quant_scale_ue8m0: bool | None = None,
        quant_col_major: bool | None = None,
        quant_tma_aligned: bool | None = None,
        q_dcp_replicated: torch.Tensor | None = None,
    ) -> torch.Tensor:
        assert output is not None, "Output tensor must be provided."

        quant_key = _detect_output_quant_key(
            output, output_scale, output_block_scale, self.num_heads * self.v_head_dim
        )
        if quant_key is not None:
            # The fusion pass has allocated output with quantized dtype
            # (FP8 or uint8 for FP4). We can't write into it directly,
            # so we swap in a temp buffer for computation, then quantize
            # into the real output at the end.
            # NOTE(carlyou): this is temporary until kernels support fp8 output
            quant_output = output
            output = torch.empty(
                output.shape[0],
                self.num_heads * self.v_head_dim,
                dtype=q.dtype,
                device=output.device,
            )

        if attn_metadata is None:
            # During the profile run try to simulate to worse case output size
            # for `self.kv_b_proj(kv_c_normed)` in `_compute_prefill_context`
            # since this can be large
            _ = torch.empty(
                (
                    self.chunked_prefill_workspace_size,
                    self.num_heads,
                    self.qk_nope_head_dim + self.v_head_dim,
                ),
                device=k_c_normed.device,
                dtype=k_c_normed.dtype,
            )
            self.impl.reserve_workspace()

            # The zero fill is required when used with DP + EP
            # to ensure all ranks within a DP group compute the
            # same expert outputs.
            if quant_key is not None:
                return quant_output.fill_(0)
            return output.fill_(0)

        fp8_attention = is_quantized_kv_cache(self.kv_cache_dtype)

        num_actual_toks = attn_metadata.num_actual_tokens
        if self.use_pcp and self.impl.dcp_world_size > 1 and quant_key is not None:
            raise NotImplementedError(
                "MRV2 MLA PCP+DCP does not support fused output quantization yet."
            )

        # Inputs and outputs may be padded for CUDA graphs
        output_padded = output
        output = output[:num_actual_toks, ...]
        q = q[:num_actual_toks, ...]
        if q_dcp_replicated is not None:
            q_dcp_replicated = q_dcp_replicated[:num_actual_toks, ...]
        k_c_normed = k_c_normed[:num_actual_toks, ...]
        k_pe = k_pe[:num_actual_toks, ...]

        if fp8_attention and self.kv_cache_dtype not in (
            # Opaque per-token byte formats stay as raw uint8
            "fp8_ds_mla",
            "nvfp4_ds_mla",
        ):
            kv_cache = kv_cache.view(current_platform.fp8_dtype())

        assert (
            attn_metadata.num_decodes is not None
            and attn_metadata.num_prefills is not None
            and attn_metadata.num_decode_tokens is not None
        )
        num_mqa_tokens = attn_metadata.num_decode_tokens
        num_mha_tokens = q.size(0) - num_mqa_tokens
        use_mha = True

        if self.impl.is_sparse and num_mha_tokens > 0:
            use_mha = self._use_sparse_mha(attn_metadata)
            if not use_mha:
                num_mqa_tokens = q.size(0)
                num_mha_tokens = 0

        mha_use_quant_output = (
            quant_key is not None
            and self.prefill_backend is not None
            and self.prefill_backend.supports_quant_output(quant_key)
            and (
                not self.impl.is_sparse
                or attn_metadata.prefill_max_seq_len  # type: ignore[attr-defined]
                <= attn_metadata.topk_tokens  # type: ignore[attr-defined]
            )
            and attn_metadata is not None
            and attn_metadata.prefill is not None
            and attn_metadata.prefill.chunked_context is None
            and self.impl.dcp_world_size <= 1
        )

        if num_mha_tokens > 0:
            if mha_use_quant_output:
                mha_output = quant_output
                mha_output_scale = output_scale
            else:
                mha_output = output
                mha_output_scale = None

            self.impl.forward_mha(  # type: ignore[attr-defined]
                q[num_mqa_tokens:],
                k_c_normed[num_mqa_tokens:],
                k_pe[num_mqa_tokens:],
                kv_cache,
                attn_metadata,
                self._k_scale,
                output=mha_output[num_mqa_tokens:num_actual_toks],
                output_scale=mha_output_scale,
            )

        if num_mqa_tokens > 0:
            if q_dcp_replicated is not None:
                mqa_q = q_dcp_replicated[:num_mqa_tokens]
                qrep_decode = True
            else:
                mqa_q = q[:num_mqa_tokens]
                qrep_decode = False
            mqa_output_slice = output[:num_mqa_tokens]

            mqa_q_nope, mqa_q_pe = mqa_q.split(
                [self.qk_nope_head_dim, self.qk_rope_head_dim], dim=-1
            )

            # Convert from (B, N, P) to (N, B, P)
            mqa_q_nope = mqa_q_nope.transpose(0, 1)

            if self.q_pad_num_heads is not None:
                B, N, L = mqa_q_pe.shape
                mqa_pe_padded = mqa_q_pe.new_empty((B, self.q_pad_num_heads, L))
                mqa_pe_padded.resize_((B, N, L))
                mqa_pe_padded.copy_(mqa_q_pe)
                mqa_q_pe = mqa_pe_padded

            if self.is_aiter_triton_fp4_bmm_enabled:
                mqa_ql_nope = rocm_aiter_ops.batched_gemm_a16wfp4(
                    mqa_q_nope,
                    self.W_K,
                    self.W_K_scale,
                    transpose_bm=True,
                    prequant=True,
                    y_scale=self._q_scale if fp8_attention else None,
                )
            elif self.is_aiter_triton_fp8_bmm_enabled:
                # Multiply+Transpose (N, B, P)x(N, P, L)->(N, B, L)->(B, N, L)
                mqa_ql_nope = rocm_aiter_ops.triton_fp8_bmm(
                    mqa_q_nope,
                    self.W_K,
                    self.W_K_scale,
                    group_size=128,
                    transpose_bm=True,
                )
            elif self.is_amx_bmm_enabled:
                # bmm_cpu computes out[n] = mat1[n] @ mat2[n]^T against
                # AMXMLAImpl's own (N, L, P) packed W_UK -- same as prefill.
                N, B, P = mqa_q_nope.shape
                L = self.kv_lora_rank
                mqa_ql_nope = mqa_q_nope.new_empty((N, B, L))
                ops.bmm_cpu(
                    mqa_ql_nope,
                    mqa_q_nope,
                    self.impl._w_uk_packed,  # type: ignore[attr-defined]
                    True,
                    self.impl._w_scale,  # type: ignore[attr-defined]
                )
                mqa_ql_nope = mqa_ql_nope.transpose(0, 1)
            else:
                # Pads the head_dim if necessary (for the underlying kernel)
                N, B, P = mqa_q_nope.shape
                W_UK_T = self.W_UK_T_dcp_qrep if qrep_decode else self.W_UK_T
                assert W_UK_T is not None
                _, _, L = W_UK_T.shape

                if self.q_pad_num_heads is not None:
                    mqa_ql_nope = mqa_q_nope.new_empty((self.q_pad_num_heads, B, L))
                    mqa_ql_nope.resize_((N, B, L))
                    # Multiply (N, B, P) x (N, P, L) -> (N, B, L)
                    torch.bmm(mqa_q_nope, W_UK_T, out=mqa_ql_nope)
                    # Convert from (N, B, L) to (B, N, L)
                    mqa_ql_nope = mqa_ql_nope.transpose(0, 1)
                else:
                    # Write the (N, B, L) bmm result straight into a
                    # token-major (B, N, L) buffer so the MQA query is already
                    # contiguous; a NoPE model (qk_rope_head_dim == 0) then
                    # needs no concat at all.
                    mqa_ql_nope = mqa_q_nope.new_empty((B, N, L))
                    torch.bmm(mqa_q_nope, W_UK_T, out=mqa_ql_nope.transpose(0, 1))

            if fp8_attention and self.impl.supports_quant_query_input:
                assert mqa_ql_nope.shape[0] == mqa_q_pe.shape[0]
                assert mqa_ql_nope.shape[1] == mqa_q_pe.shape[1]
                mqa_q = self._decode_concat_quant_fp8_op(
                    mqa_ql_nope, mqa_q_pe, self._q_scale
                )
            else:
                mqa_q = (mqa_ql_nope, mqa_q_pe)
            # concatenate nope + pe -> (B, N, L + P) (fp8 op above may have fused)
            if self.impl.dcp_world_size > 1:
                assert self.dcp_manager is not None
                if self.use_pcp:
                    if self.impl.dcp_world_size > self.impl.pcp_world_size:
                        if isinstance(mqa_q, tuple):
                            mqa_q = torch.cat(mqa_q, dim=-1)
                        mqa_q = get_tp_group().all_gather(mqa_q, dim=1)
                else:
                    if isinstance(mqa_q, tuple):
                        # concatenate mqa_ql_nope and mqa_q_pe -> (B, N, L + P)
                        mqa_q = torch.cat(mqa_q, dim=-1)
                    if not qrep_decode:
                        assert self.dcp_manager.query_gather is not None
                        mqa_q = self.dcp_manager.query_gather(mqa_q)

            # call decode attn
            if not self.impl.is_sparse:
                assert attn_metadata.decode is not None
            attn_out, lse = self.impl.forward_mqa(mqa_q, kv_cache, attn_metadata, self)  # type: ignore[attr-defined]

            # correct dcp attn_out with lse.
            if self.impl.dcp_world_size > 1:
                assert lse is not None
                assert self.dcp_manager is not None
                decode_metadata = getattr(attn_metadata, "decode", None)
                if not use_mha:
                    seq_lens = cast(torch.Tensor, attn_metadata.seq_lens)  # type: ignore[attr-defined]
                    query_start_loc = attn_metadata.query_start_loc
                else:
                    seq_lens = (
                        decode_metadata.seq_lens
                        if decode_metadata is not None
                        else cast(torch.Tensor, attn_metadata.seq_lens)[  # type: ignore[attr-defined]
                            : attn_metadata.num_decodes
                        ]
                    )
                    query_start_loc = attn_metadata.query_start_loc[
                        : attn_metadata.num_decodes + 1
                    ]
                attn_out = self.dcp_manager.combine(
                    attn_out,
                    lse,
                    seq_lens=seq_lens,
                    query_start_loc=query_start_loc,
                )
                if self.use_pcp:
                    attn_out = finalize_mla_pcp_decode(attn_out, self.num_heads)

            # v_up projection
            self._v_up_proj(attn_out, out=mqa_output_slice)

        if quant_key is not None:
            quant_idx = num_mqa_tokens if mha_use_quant_output else num_actual_toks
            if quant_idx == 0:
                return quant_output
            actual = output[:quant_idx]
            if quant_key == kNvfp4Dynamic:
                # NVFP4: two FP4 values packed into one uint8
                assert output_block_scale is not None
                fp4_data, fp4_scales = ops.scaled_fp4_quant(actual, output_scale)
                quant_output[:quant_idx].copy_(fp4_data)
                output_block_scale[: fp4_scales.shape[0]].copy_(fp4_scales)
            elif quant_key in (kFp8Dynamic128Sym, kFp8Dynamic64Sym):
                # Per-group FP8
                assert output_block_scale is not None
                assert quant_group_size is not None, (
                    "Group FP8 output quant requested but "
                    "quant_group_size not passed through custom op"
                )
                finfo = torch.finfo(_FP8_DTYPE)
                torch.ops._C.per_token_group_fp8_quant(
                    actual,
                    quant_output[:quant_idx],
                    output_block_scale[:quant_idx],
                    quant_group_size,
                    1e-10,  # eps
                    finfo.min,
                    finfo.max,
                    quant_scale_ue8m0,
                    quant_col_major,
                    quant_tma_aligned,
                )
            elif quant_key == kFp8StaticTensorSym:
                # Static FP8 quantization
                fp8_data, _ = self._quant_fp8_op(actual, output_scale)
                quant_output[:quant_idx].copy_(fp8_data)
            else:
                raise ValueError(f"Unsupported quant_key: {quant_key}")
            return quant_output

        if self.use_pcp and output_padded.shape[0] > num_actual_toks:
            output_padded[num_actual_toks:].zero_()
        return output_padded
```


#### 📄 檔案: `vllm/v1/attention/backend.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:91, E:53, A:0) ➔ After(N:92, E:53, A:0)
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
  • + [新增節點] `MLAAttentionImpl.reserve_workspace` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `vllm/v1/attention/backends/mla/triton_mla.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:48, E:42, A:0) ➔ After(N:51, E:45, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 1, +Edges: 9, -Edges: 6, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `get_current_vllm_config (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `max_decode_query_len (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `TritonMLAImpl.reserve_workspace` (FUNCTION_DEF)
  • + [新增節點] `_reserve_attn_logits_workspace` (FUNCTION_DEF)
  • - [移除節點] `TritonMLAMetadataBuilder._reserve_attn_logits_workspace` (FUNCTION_DEF)
  • + [新增呼叫邊] `_reserve_attn_logits_workspace` ──[CALLS]──> `is_workspace_manager_initialized (External/Unresolved)`
  • + [新增呼叫邊] `_reserve_attn_logits_workspace` ──[CALLS]──> `_compute_num_kv_splits`
  • + [新增呼叫邊] `_reserve_attn_logits_workspace` ──[CALLS]──> `num_compute_units (External/Unresolved)`
  • + [新增呼叫邊] `_reserve_attn_logits_workspace` ──[CALLS]──> `get_simultaneous (External/Unresolved)`
  • + [新增呼叫邊] `_reserve_attn_logits_workspace` ──[CALLS]──> `current_workspace_manager (External/Unresolved)`
  • + [新增呼叫邊] `TritonMLAMetadataBuilder.__init__` ──[CALLS]──> `_reserve_attn_logits_workspace`
  • + [新增呼叫邊] `TritonMLAImpl.reserve_workspace` ──[CALLS]──> `get_current_vllm_config (External/Unresolved)`
  • + [新增呼叫邊] `TritonMLAImpl.reserve_workspace` ──[CALLS]──> `_reserve_attn_logits_workspace`
  • + [新增呼叫邊] `TritonMLAImpl.reserve_workspace` ──[CALLS]──> `max_decode_query_len (External/Unresolved)`
  • - [移除呼叫邊] `TritonMLAMetadataBuilder.__init__` ──[CALLS]──> `TritonMLAMetadataBuilder._reserve_attn_logits_workspace`
  • _... 以及其餘 5 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TritonMLAMetadataBuilder.__init__()`
- **變更前簽章 (Before)**: `def __init__(self, kv_cache_spec, layer_names, vllm_config, device)` (L58~L62)
- **變更後簽章 (After)**: `def __init__(self, kv_cache_spec, layer_names, vllm_config, device)` (L81~L93)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(self, kv_cache_spec, layer_names, vllm_config, device):
        super().__init__(kv_cache_spec, layer_names, vllm_config, device)
        # DCP local sequence lengths are not advanced between draft steps.
        self.supports_draft_decode_metadata_update = self.dcp_world_size == 1
        self._reserve_attn_logits_workspace()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(self, kv_cache_spec, layer_names, vllm_config, device):
        super().__init__(kv_cache_spec, layer_names, vllm_config, device)
        # DCP local sequence lengths are not advanced between draft steps.
        self.supports_draft_decode_metadata_update = self.dcp_world_size == 1
        # forward_mqa flattens each request's block to query_len decode rows,
        # and query_len is bounded by the reorder threshold. DCP all-gathers
        # the query heads before forward_mqa.
        _reserve_attn_logits_workspace(
            vllm_config,
            vllm_config.scheduler_config.max_num_seqs * self.reorder_batch_threshold,
            self.num_heads * self.dcp_world_size,
            self.mla_dims.kv_lora_rank,
        )
```


#### 📄 檔案: `vllm/v1/attention/ops/triton_decode_attention.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:40, E:69, A:0) ➔ After(N:40, E:69, A:0)
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

### 🔹 函式: `_fwd_kernel_stage2()`
- **變更前簽章 (Before)**: `def _fwd_kernel_stage2( Mid_O, o, lse, B_Seqlen, stride_mid_ob, stride_mid_oh, stride_mid_os, stride_obs, stride_oh, stride_lse_bs, NUM_KV_SPLITS: tl.constexpr, BLOCK_DV: tl.constexpr, Lv: tl.constexpr, OUTPUT_FP16: tl.constexpr = 0, )` (L575~L638)
- **變更後簽章 (After)**: `def _fwd_kernel_stage2( Mid_O, o, lse, B_Seqlen, stride_mid_ob, stride_mid_oh, stride_mid_os, stride_obs, stride_oh, stride_lse_bs, NUM_KV_SPLITS: tl.constexpr, BLOCK_DV: tl.constexpr, Lv: tl.constexpr, OUTPUT_FP16: tl.constexpr = 0, )` (L575~L638)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _fwd_kernel_stage2(
    Mid_O,
    o,
    lse,
    B_Seqlen,
    stride_mid_ob,
    stride_mid_oh,
    stride_mid_os,
    stride_obs,
    stride_oh,
    stride_lse_bs,
    NUM_KV_SPLITS: tl.constexpr,
    BLOCK_DV: tl.constexpr,
    Lv: tl.constexpr,
    OUTPUT_FP16: tl.constexpr = 0,
):
    cur_batch = tl.program_id(0)
    cur_head = tl.program_id(1)

    cur_batch_seq_len = tl.load(B_Seqlen + cur_batch)

    offs_d = tl.arange(0, BLOCK_DV)
    mask_d = offs_d < Lv

    e_sum = 0.0
    e_max = -float("inf")
    acc = tl.zeros([BLOCK_DV], dtype=tl.float32)

    offs_v = cur_batch * stride_mid_ob + cur_head * stride_mid_oh + offs_d
    offs_logic = cur_batch * stride_mid_ob + cur_head * stride_mid_oh + Lv

    for split_kv_id in range(0, NUM_KV_SPLITS):
        kv_len_per_split = tl.cdiv(cur_batch_seq_len, NUM_KV_SPLITS)
        split_kv_start = kv_len_per_split * split_kv_id
        split_kv_end = tl.minimum(split_kv_start + kv_len_per_split, cur_batch_seq_len)

        if split_kv_end > split_kv_start:
            tv = tl.load(
                Mid_O + offs_v + split_kv_id * stride_mid_os, mask=mask_d, other=0.0
            )
            tlogic = tl.load(Mid_O + offs_logic + split_kv_id * stride_mid_os)
            n_e_max = tl.maximum(tlogic, e_max)

            old_scale = tl.exp(e_max - n_e_max)
            acc *= old_scale
            exp_logic = tl.exp(tlogic - n_e_max)
            acc += exp_logic * tv

            e_sum = e_sum * old_scale + exp_logic
            e_max = n_e_max

    result = acc / e_sum
    if OUTPUT_FP16:
        result = result.to(tl.float16)
    tl.store(
        o + cur_batch * stride_obs + cur_head * stride_oh + offs_d,
        result,
        mask=mask_d,
    )
    lse_val = e_max + tl.log(e_sum)
    tl.store(
        lse + cur_batch * stride_lse_bs + cur_head,
        lse_val,
    )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _fwd_kernel_stage2(
    Mid_O,
    o,
    lse,
    B_Seqlen,
    stride_mid_ob,
    stride_mid_oh,
    stride_mid_os,
    stride_obs,
    stride_oh,
    stride_lse_bs,
    NUM_KV_SPLITS: tl.constexpr,
    BLOCK_DV: tl.constexpr,
    Lv: tl.constexpr,
    OUTPUT_FP16: tl.constexpr = 0,
):
    cur_batch = tl.program_id(0)
    cur_head = tl.program_id(1)

    cur_batch_seq_len = tl.load(B_Seqlen + cur_batch)

    offs_d = tl.arange(0, BLOCK_DV)
    mask_d = offs_d < Lv

    e_sum = 0.0
    e_max = -float("inf")
    acc = tl.zeros([BLOCK_DV], dtype=tl.float32)

    offs_v = cur_batch.to(tl.int64) * stride_mid_ob + cur_head * stride_mid_oh + offs_d
    offs_logic = cur_batch.to(tl.int64) * stride_mid_ob + cur_head * stride_mid_oh + Lv

    for split_kv_id in range(0, NUM_KV_SPLITS):
        kv_len_per_split = tl.cdiv(cur_batch_seq_len, NUM_KV_SPLITS)
        split_kv_start = kv_len_per_split * split_kv_id
        split_kv_end = tl.minimum(split_kv_start + kv_len_per_split, cur_batch_seq_len)

        if split_kv_end > split_kv_start:
            tv = tl.load(
                Mid_O + offs_v + split_kv_id * stride_mid_os, mask=mask_d, other=0.0
            )
            tlogic = tl.load(Mid_O + offs_logic + split_kv_id * stride_mid_os)
            n_e_max = tl.maximum(tlogic, e_max)

            old_scale = tl.exp(e_max - n_e_max)
            acc *= old_scale
            exp_logic = tl.exp(tlogic - n_e_max)
            acc += exp_logic * tv

            e_sum = e_sum * old_scale + exp_logic
            e_max = n_e_max

    result = acc / e_sum
    if OUTPUT_FP16:
        result = result.to(tl.float16)
    tl.store(
        o + cur_batch * stride_obs + cur_head * stride_oh + offs_d,
        result,
        mask=mask_d,
    )
    lse_val = e_max + tl.log(e_sum)
    tl.store(
        lse + cur_batch * stride_lse_bs + cur_head,
        lse_val,
    )
```

### 🔹 函式: `_fwd_grouped_kernel_stage1()`
- **變更前簽章 (Before)**: `def _fwd_grouped_kernel_stage1( Q, K_Buffer, V_Buffer, sm_scale, Req_to_tokens, B_Seqlen, Att_Out, stride_req_to_tokens_b, stride_qbs, stride_qh, stride_buf_kpbs, stride_buf_kbs, stride_buf_kh, stride_buf_vpbs, stride_buf_vbs, stride_buf_vh, stride_mid_ob, stride_mid_oh, stride_mid_os, k_scale, v_scale, kv_group_num: tl.constexpr, q_head_num: tl.constexpr, BLOCK_DMODEL: tl.constexpr, BLOCK_DPE: tl.constexpr, BLOCK_DV: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_H: tl.constexpr, NUM_KV_SPLITS: tl.constexpr, PAGE_SIZE: tl.constexpr, logit_cap: tl.constexpr, Lk: tl.constexpr, Lv: tl.constexpr, IS_MLA: tl.constexpr = False, )` (L278~L466)
- **變更後簽章 (After)**: `def _fwd_grouped_kernel_stage1( Q, K_Buffer, V_Buffer, sm_scale, Req_to_tokens, B_Seqlen, Att_Out, stride_req_to_tokens_b, stride_qbs, stride_qh, stride_buf_kpbs, stride_buf_kbs, stride_buf_kh, stride_buf_vpbs, stride_buf_vbs, stride_buf_vh, stride_mid_ob, stride_mid_oh, stride_mid_os, k_scale, v_scale, kv_group_num: tl.constexpr, q_head_num: tl.constexpr, BLOCK_DMODEL: tl.constexpr, BLOCK_DPE: tl.constexpr, BLOCK_DV: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_H: tl.constexpr, NUM_KV_SPLITS: tl.constexpr, PAGE_SIZE: tl.constexpr, logit_cap: tl.constexpr, Lk: tl.constexpr, Lv: tl.constexpr, IS_MLA: tl.constexpr = False, )` (L278~L466)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _fwd_grouped_kernel_stage1(
    Q,
    K_Buffer,
    V_Buffer,
    sm_scale,
    Req_to_tokens,
    B_Seqlen,
    Att_Out,
    stride_req_to_tokens_b,
    stride_qbs,
    stride_qh,
    stride_buf_kpbs,
    stride_buf_kbs,
    stride_buf_kh,
    stride_buf_vpbs,
    stride_buf_vbs,
    stride_buf_vh,
    stride_mid_ob,
    stride_mid_oh,
    stride_mid_os,
    k_scale,
    v_scale,
    kv_group_num: tl.constexpr,
    q_head_num: tl.constexpr,
    BLOCK_DMODEL: tl.constexpr,
    BLOCK_DPE: tl.constexpr,
    BLOCK_DV: tl.constexpr,
    BLOCK_N: tl.constexpr,
    BLOCK_H: tl.constexpr,
    NUM_KV_SPLITS: tl.constexpr,
    PAGE_SIZE: tl.constexpr,
    logit_cap: tl.constexpr,
    Lk: tl.constexpr,
    Lv: tl.constexpr,
    IS_MLA: tl.constexpr = False,
):
    cur_batch = tl.program_id(0)
    cur_head_id = tl.program_id(1)
    cur_kv_head = cur_head_id // tl.cdiv(kv_group_num, BLOCK_H)
    split_kv_id = tl.program_id(2)

    VALID_BLOCK_H: tl.constexpr = BLOCK_H if kv_group_num > BLOCK_H else kv_group_num
    cur_head = cur_head_id * VALID_BLOCK_H + tl.arange(0, BLOCK_H)
    mask_h = cur_head < (cur_head_id + 1) * VALID_BLOCK_H
    mask_h = mask_h & (cur_head < q_head_num)

    offs_d = tl.arange(0, BLOCK_DMODEL)
    offs_dv = tl.arange(0, BLOCK_DV)
    mask_d = offs_d < Lk
    mask_dv = offs_dv < Lv
    cur_batch_seq_len = tl.load(B_Seqlen + cur_batch)
    cur_batch_req_idx = cur_batch

    offs_q = cur_batch * stride_qbs + cur_head[:, None] * stride_qh + offs_d[None, :]
    q = tl.load(
        Q + offs_q,
        mask=(mask_h[:, None]) & (mask_d[None, :]),
        other=0.0,
        cache_modifier=".ca",
    )

    if BLOCK_DPE > 0:
        offs_dpe = BLOCK_DMODEL + tl.arange(0, BLOCK_DPE)
        mask_dpe = offs_dpe < Lk
        off_qpe = (
            cur_batch * stride_qbs + cur_head[:, None] * stride_qh + offs_dpe[None, :]
        )
        qpe = tl.load(
            Q + off_qpe,
            mask=(mask_h[:, None]) & (mask_dpe[None, :]),
            other=0.0,
            cache_modifier=".ca",
        )

    kv_len_per_split = tl.cdiv(cur_batch_seq_len, NUM_KV_SPLITS)
    split_kv_start = kv_len_per_split * split_kv_id
    split_kv_end = tl.minimum(split_kv_start + kv_len_per_split, cur_batch_seq_len)

    e_max = tl.zeros([BLOCK_H], dtype=tl.float32) - float("inf")
    e_sum = tl.zeros([BLOCK_H], dtype=tl.float32)
    acc = tl.zeros([BLOCK_H, BLOCK_DV], dtype=tl.float32)

    if split_kv_end > split_kv_start:
        base_offs_k = cur_kv_head * stride_buf_kh + offs_d[:, None]
        base_offs_v = cur_kv_head * stride_buf_vh + offs_dv[None, :]
        if BLOCK_DPE > 0:
            base_offs_kpe = cur_kv_head * stride_buf_kh + offs_dpe[:, None]

        ks = tl.load(k_scale)
        vs = tl.load(v_scale)
        for start_n in tl.range(split_kv_start, split_kv_end, BLOCK_N):
            offs_n = start_n + tl.arange(0, BLOCK_N)
            kv_page_number = tl.load(
                Req_to_tokens
                + stride_req_to_tokens_b * cur_batch_req_idx
                + offs_n // PAGE_SIZE,
                mask=offs_n < split_kv_end,
                other=0,
                cache_modifier=".ca",
            ).to(tl.int64)  # page_number * page stride overflows int32
            kv_off_k = (
                kv_page_number * stride_buf_kpbs + (offs_n % PAGE_SIZE) * stride_buf_kbs
            )

            # explicitly facilitate overlapping load/compute
            offs_buf_k = kv_off_k[None, :] + base_offs_k
            k = tl.load(
                K_Buffer + offs_buf_k,
                mask=(offs_n[None, :] < split_kv_end) & (mask_d[:, None]),
                other=0.0,
                cache_modifier=".cg",
            )

            if k.dtype.is_fp8():
                k = (k.to(tl.float32) * ks).to(q.dtype)
            qk = tl.dot(q, k.to(q.dtype))
            if BLOCK_DPE > 0:
                offs_buf_kpe = kv_off_k[None, :] + base_offs_kpe
                kpe = tl.load(
                    K_Buffer + offs_buf_kpe,
                    mask=(offs_n[None, :] < split_kv_end) & (mask_dpe[:, None]),
                    other=0.0,
                    cache_modifier=".cg",
                )
                if kpe.dtype.is_fp8():
                    kpe = (kpe.to(tl.float32) * ks).to(qpe.dtype)
                qk += tl.dot(qpe, kpe.to(qpe.dtype))
            qk *= sm_scale

            if logit_cap > 0:
                qk = logit_cap * tanh(qk / logit_cap)

            qk = tl.where(
                mask_h[:, None] & (offs_n[None, :] < split_kv_end), qk, float("-inf")
            )

            if not IS_MLA:
                kv_off_v = (
                    kv_page_number * stride_buf_vpbs
                    + (offs_n % PAGE_SIZE) * stride_buf_vbs
                )
                offs_buf_v = kv_off_v[:, None] + base_offs_v
                v = tl.load(
                    V_Buffer + offs_buf_v,
                    mask=(offs_n[:, None] < split_kv_end) & (mask_dv[None, :]),
                    other=0.0,
                )
                if v.dtype.is_fp8():
                    v = (v.to(tl.float32) * vs).to(q.dtype)
            else:
                # MLA uses a single c_kv.
                # loading the same c_kv to interpret it as v is not necessary.
                # transpose the existing c_kv (aka k) for the dot product.
                v = tl.trans(k)

            n_e_max = tl.maximum(tl.max(qk, 1), e_max)
            re_scale = tl.exp(e_max - n_e_max)
            p = tl.exp(qk - n_e_max[:, None])
            acc *= re_scale[:, None]
            acc += tl.dot(p.to(v.dtype), v)

            e_sum = e_sum * re_scale + tl.sum(p, 1)
            e_max = n_e_max

        offs_mid_o = (
            cur_batch * stride_mid_ob
            + cur_head[:, None] * stride_mid_oh
            + split_kv_id * stride_mid_os
            + offs_dv[None, :]
        )

        tl.store(
            Att_Out + offs_mid_o,
            acc / e_sum[:, None],
            mask=(mask_h[:, None]) & (mask_dv[None, :]),
        )

        offs_mid_o_1 = (
            cur_batch * stride_mid_ob
            + cur_head * stride_mid_oh
            + split_kv_id * stride_mid_os
            + Lv
        )

        tl.store(
            Att_Out + offs_mid_o_1,
            e_max + tl.log(e_sum),
            mask=mask_h,
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _fwd_grouped_kernel_stage1(
    Q,
    K_Buffer,
    V_Buffer,
    sm_scale,
    Req_to_tokens,
    B_Seqlen,
    Att_Out,
    stride_req_to_tokens_b,
    stride_qbs,
    stride_qh,
    stride_buf_kpbs,
    stride_buf_kbs,
    stride_buf_kh,
    stride_buf_vpbs,
    stride_buf_vbs,
    stride_buf_vh,
    stride_mid_ob,
    stride_mid_oh,
    stride_mid_os,
    k_scale,
    v_scale,
    kv_group_num: tl.constexpr,
    q_head_num: tl.constexpr,
    BLOCK_DMODEL: tl.constexpr,
    BLOCK_DPE: tl.constexpr,
    BLOCK_DV: tl.constexpr,
    BLOCK_N: tl.constexpr,
    BLOCK_H: tl.constexpr,
    NUM_KV_SPLITS: tl.constexpr,
    PAGE_SIZE: tl.constexpr,
    logit_cap: tl.constexpr,
    Lk: tl.constexpr,
    Lv: tl.constexpr,
    IS_MLA: tl.constexpr = False,
):
    cur_batch = tl.program_id(0)
    cur_head_id = tl.program_id(1)
    cur_kv_head = cur_head_id // tl.cdiv(kv_group_num, BLOCK_H)
    split_kv_id = tl.program_id(2)

    VALID_BLOCK_H: tl.constexpr = BLOCK_H if kv_group_num > BLOCK_H else kv_group_num
    cur_head = cur_head_id * VALID_BLOCK_H + tl.arange(0, BLOCK_H)
    mask_h = cur_head < (cur_head_id + 1) * VALID_BLOCK_H
    mask_h = mask_h & (cur_head < q_head_num)

    offs_d = tl.arange(0, BLOCK_DMODEL)
    offs_dv = tl.arange(0, BLOCK_DV)
    mask_d = offs_d < Lk
    mask_dv = offs_dv < Lv
    cur_batch_seq_len = tl.load(B_Seqlen + cur_batch)
    cur_batch_req_idx = cur_batch

    offs_q = cur_batch * stride_qbs + cur_head[:, None] * stride_qh + offs_d[None, :]
    q = tl.load(
        Q + offs_q,
        mask=(mask_h[:, None]) & (mask_d[None, :]),
        other=0.0,
        cache_modifier=".ca",
    )

    if BLOCK_DPE > 0:
        offs_dpe = BLOCK_DMODEL + tl.arange(0, BLOCK_DPE)
        mask_dpe = offs_dpe < Lk
        off_qpe = (
            cur_batch * stride_qbs + cur_head[:, None] * stride_qh + offs_dpe[None, :]
        )
        qpe = tl.load(
            Q + off_qpe,
            mask=(mask_h[:, None]) & (mask_dpe[None, :]),
            other=0.0,
            cache_modifier=".ca",
        )

    kv_len_per_split = tl.cdiv(cur_batch_seq_len, NUM_KV_SPLITS)
    split_kv_start = kv_len_per_split * split_kv_id
    split_kv_end = tl.minimum(split_kv_start + kv_len_per_split, cur_batch_seq_len)

    e_max = tl.zeros([BLOCK_H], dtype=tl.float32) - float("inf")
    e_sum = tl.zeros([BLOCK_H], dtype=tl.float32)
    acc = tl.zeros([BLOCK_H, BLOCK_DV], dtype=tl.float32)

    if split_kv_end > split_kv_start:
        base_offs_k = cur_kv_head * stride_buf_kh + offs_d[:, None]
        base_offs_v = cur_kv_head * stride_buf_vh + offs_dv[None, :]
        if BLOCK_DPE > 0:
            base_offs_kpe = cur_kv_head * stride_buf_kh + offs_dpe[:, None]

        ks = tl.load(k_scale)
        vs = tl.load(v_scale)
        for start_n in tl.range(split_kv_start, split_kv_end, BLOCK_N):
            offs_n = start_n + tl.arange(0, BLOCK_N)
            kv_page_number = tl.load(
                Req_to_tokens
                + stride_req_to_tokens_b * cur_batch_req_idx
                + offs_n // PAGE_SIZE,
                mask=offs_n < split_kv_end,
                other=0,
                cache_modifier=".ca",
            ).to(tl.int64)  # page_number * page stride overflows int32
            kv_off_k = (
                kv_page_number * stride_buf_kpbs + (offs_n % PAGE_SIZE) * stride_buf_kbs
            )

            # explicitly facilitate overlapping load/compute
            offs_buf_k = kv_off_k[None, :] + base_offs_k
            k = tl.load(
                K_Buffer + offs_buf_k,
                mask=(offs_n[None, :] < split_kv_end) & (mask_d[:, None]),
                other=0.0,
                cache_modifier=".cg",
            )

            if k.dtype.is_fp8():
                k = (k.to(tl.float32) * ks).to(q.dtype)
            qk = tl.dot(q, k.to(q.dtype))
            if BLOCK_DPE > 0:
                offs_buf_kpe = kv_off_k[None, :] + base_offs_kpe
                kpe = tl.load(
                    K_Buffer + offs_buf_kpe,
                    mask=(offs_n[None, :] < split_kv_end) & (mask_dpe[:, None]),
                    other=0.0,
                    cache_modifier=".cg",
                )
                if kpe.dtype.is_fp8():
                    kpe = (kpe.to(tl.float32) * ks).to(qpe.dtype)
                qk += tl.dot(qpe, kpe.to(qpe.dtype))
            qk *= sm_scale

            if logit_cap > 0:
                qk = logit_cap * tanh(qk / logit_cap)

            qk = tl.where(
                mask_h[:, None] & (offs_n[None, :] < split_kv_end), qk, float("-inf")
            )

            if not IS_MLA:
                kv_off_v = (
                    kv_page_number * stride_buf_vpbs
                    + (offs_n % PAGE_SIZE) * stride_buf_vbs
                )
                offs_buf_v = kv_off_v[:, None] + base_offs_v
                v = tl.load(
                    V_Buffer + offs_buf_v,
                    mask=(offs_n[:, None] < split_kv_end) & (mask_dv[None, :]),
                    other=0.0,
                )
                if v.dtype.is_fp8():
                    v = (v.to(tl.float32) * vs).to(q.dtype)
            else:
                # MLA uses a single c_kv.
                # loading the same c_kv to interpret it as v is not necessary.
                # transpose the existing c_kv (aka k) for the dot product.
                v = tl.trans(k)

            n_e_max = tl.maximum(tl.max(qk, 1), e_max)
            re_scale = tl.exp(e_max - n_e_max)
            p = tl.exp(qk - n_e_max[:, None])
            acc *= re_scale[:, None]
            acc += tl.dot(p.to(v.dtype), v)

            e_sum = e_sum * re_scale + tl.sum(p, 1)
            e_max = n_e_max

        offs_mid_o = (
            cur_batch.to(tl.int64) * stride_mid_ob
            + cur_head[:, None] * stride_mid_oh
            + split_kv_id * stride_mid_os
            + offs_dv[None, :]
        )

        tl.store(
            Att_Out + offs_mid_o,
            acc / e_sum[:, None],
            mask=(mask_h[:, None]) & (mask_dv[None, :]),
        )

        offs_mid_o_1 = (
            cur_batch.to(tl.int64) * stride_mid_ob
            + cur_head * stride_mid_oh
            + split_kv_id * stride_mid_os
            + Lv
        )

        tl.store(
            Att_Out + offs_mid_o_1,
            e_max + tl.log(e_sum),
            mask=mask_h,
        )
```

### 🔹 函式: `_fwd_kernel_stage1()`
- **變更前簽章 (Before)**: `def _fwd_kernel_stage1( Q, K_Buffer, V_Buffer, sm_scale, Req_to_tokens, B_Seqlen, Att_Out, stride_req_to_tokens_b, stride_qbs, stride_qh, stride_buf_kpbs, stride_buf_kbs, stride_buf_kh, stride_buf_vpbs, stride_buf_vbs, stride_buf_vh, stride_mid_ob, stride_mid_oh, stride_mid_os, k_scale, v_scale, kv_group_num: tl.constexpr, BLOCK_DMODEL: tl.constexpr, BLOCK_DV: tl.constexpr, BLOCK_N: tl.constexpr, NUM_KV_SPLITS: tl.constexpr, PAGE_SIZE: tl.constexpr, logit_cap: tl.constexpr, Lk: tl.constexpr, Lv: tl.constexpr, )` (L68~L206)
- **變更後簽章 (After)**: `def _fwd_kernel_stage1( Q, K_Buffer, V_Buffer, sm_scale, Req_to_tokens, B_Seqlen, Att_Out, stride_req_to_tokens_b, stride_qbs, stride_qh, stride_buf_kpbs, stride_buf_kbs, stride_buf_kh, stride_buf_vpbs, stride_buf_vbs, stride_buf_vh, stride_mid_ob, stride_mid_oh, stride_mid_os, k_scale, v_scale, kv_group_num: tl.constexpr, BLOCK_DMODEL: tl.constexpr, BLOCK_DV: tl.constexpr, BLOCK_N: tl.constexpr, NUM_KV_SPLITS: tl.constexpr, PAGE_SIZE: tl.constexpr, logit_cap: tl.constexpr, Lk: tl.constexpr, Lv: tl.constexpr, )` (L68~L206)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _fwd_kernel_stage1(
    Q,
    K_Buffer,
    V_Buffer,
    sm_scale,
    Req_to_tokens,
    B_Seqlen,
    Att_Out,
    stride_req_to_tokens_b,
    stride_qbs,
    stride_qh,
    stride_buf_kpbs,
    stride_buf_kbs,
    stride_buf_kh,
    stride_buf_vpbs,
    stride_buf_vbs,
    stride_buf_vh,
    stride_mid_ob,
    stride_mid_oh,
    stride_mid_os,
    k_scale,
    v_scale,
    kv_group_num: tl.constexpr,
    BLOCK_DMODEL: tl.constexpr,
    BLOCK_DV: tl.constexpr,
    BLOCK_N: tl.constexpr,
    NUM_KV_SPLITS: tl.constexpr,
    PAGE_SIZE: tl.constexpr,
    logit_cap: tl.constexpr,
    Lk: tl.constexpr,
    Lv: tl.constexpr,
):
    cur_batch = tl.program_id(0)
    cur_head = tl.program_id(1)
    split_kv_id = tl.program_id(2)

    cur_kv_head = cur_head // kv_group_num

    offs_d = tl.arange(0, BLOCK_DMODEL)
    offs_dv = tl.arange(0, BLOCK_DV)
    mask_d = offs_d < Lk
    mask_dv = offs_dv < Lv
    cur_batch_seq_len = tl.load(B_Seqlen + cur_batch)
    cur_batch_req_idx = cur_batch

    off_q = cur_batch * stride_qbs + cur_head * stride_qh + offs_d
    q = tl.load(Q + off_q, mask=mask_d, other=0.0)

    kv_len_per_split = tl.cdiv(cur_batch_seq_len, NUM_KV_SPLITS)
    split_kv_start = kv_len_per_split * split_kv_id
    split_kv_end = tl.minimum(split_kv_start + kv_len_per_split, cur_batch_seq_len)

    e_max = -float("inf")
    e_sum = 0.0
    acc = tl.zeros([BLOCK_DV], dtype=tl.float32)

    if split_kv_end > split_kv_start:
        ks = tl.load(k_scale)
        vs = tl.load(v_scale)
        for start_n in range(split_kv_start, split_kv_end, BLOCK_N):
            offs_n = start_n + tl.arange(0, BLOCK_N)
            kv_page_number = tl.load(
                Req_to_tokens
                + stride_req_to_tokens_b * cur_batch_req_idx
                + offs_n // PAGE_SIZE,
                mask=offs_n < split_kv_end,
                other=0,
            ).to(tl.int64)  # page_number * page stride overflows int32
            kv_in_page = offs_n % PAGE_SIZE
            offs_buf_k = (
                (kv_page_number * stride_buf_kpbs + kv_in_page * stride_buf_kbs)[
                    :, None
                ]
                + cur_kv_head * stride_buf_kh
                + offs_d[None, :]
            )
            k = tl.load(
                K_Buffer + offs_buf_k,
                mask=(offs_n[:, None] < split_kv_end) & (mask_d[None, :]),
                other=0.0,
            )
            if k.dtype.is_fp8():
                k = (k.to(tl.float32) * ks).to(q.dtype)
            qk = tl.sum(q[None, :] * k, 1)
            qk *= sm_scale

            if logit_cap > 0:
                qk = logit_cap * tanh(qk / logit_cap)

            qk = tl.where(offs_n < split_kv_end, qk, float("-inf"))

            offs_buf_v = (
                (kv_page_number * stride_buf_vpbs + kv_in_page * stride_buf_vbs)[
                    :, None
                ]
                + cur_kv_head * stride_buf_vh
                + offs_dv[None, :]
            )
            v = tl.load(
                V_Buffer + offs_buf_v,
                mask=(offs_n[:, None] < split_kv_end) & (mask_dv[None, :]),
                other=0.0,
            )
            if v.dtype.is_fp8():
                v = (v.to(tl.float32) * vs).to(q.dtype)

            n_e_max = tl.maximum(tl.max(qk, 0), e_max)
            re_scale = tl.exp(e_max - n_e_max)
            p = tl.exp(qk - n_e_max)
            acc *= re_scale
            acc += tl.sum(p[:, None] * v, 0)

            e_sum = e_sum * re_scale + tl.sum(p, 0)
            e_max = n_e_max

        offs_mid_o = (
            cur_batch * stride_mid_ob
            + cur_head * stride_mid_oh
            + split_kv_id * stride_mid_os
            + offs_dv
        )

        tl.store(
            Att_Out + offs_mid_o,
            acc / e_sum,
            mask=(mask_dv),
        )

        offs_mid_o_1 = (
            cur_batch * stride_mid_ob
            + cur_head * stride_mid_oh
            + split_kv_id * stride_mid_os
            + Lv
        )

        tl.store(
            Att_Out + offs_mid_o_1,
            e_max + tl.log(e_sum),
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _fwd_kernel_stage1(
    Q,
    K_Buffer,
    V_Buffer,
    sm_scale,
    Req_to_tokens,
    B_Seqlen,
    Att_Out,
    stride_req_to_tokens_b,
    stride_qbs,
    stride_qh,
    stride_buf_kpbs,
    stride_buf_kbs,
    stride_buf_kh,
    stride_buf_vpbs,
    stride_buf_vbs,
    stride_buf_vh,
    stride_mid_ob,
    stride_mid_oh,
    stride_mid_os,
    k_scale,
    v_scale,
    kv_group_num: tl.constexpr,
    BLOCK_DMODEL: tl.constexpr,
    BLOCK_DV: tl.constexpr,
    BLOCK_N: tl.constexpr,
    NUM_KV_SPLITS: tl.constexpr,
    PAGE_SIZE: tl.constexpr,
    logit_cap: tl.constexpr,
    Lk: tl.constexpr,
    Lv: tl.constexpr,
):
    cur_batch = tl.program_id(0)
    cur_head = tl.program_id(1)
    split_kv_id = tl.program_id(2)

    cur_kv_head = cur_head // kv_group_num

    offs_d = tl.arange(0, BLOCK_DMODEL)
    offs_dv = tl.arange(0, BLOCK_DV)
    mask_d = offs_d < Lk
    mask_dv = offs_dv < Lv
    cur_batch_seq_len = tl.load(B_Seqlen + cur_batch)
    cur_batch_req_idx = cur_batch

    off_q = cur_batch * stride_qbs + cur_head * stride_qh + offs_d
    q = tl.load(Q + off_q, mask=mask_d, other=0.0)

    kv_len_per_split = tl.cdiv(cur_batch_seq_len, NUM_KV_SPLITS)
    split_kv_start = kv_len_per_split * split_kv_id
    split_kv_end = tl.minimum(split_kv_start + kv_len_per_split, cur_batch_seq_len)

    e_max = -float("inf")
    e_sum = 0.0
    acc = tl.zeros([BLOCK_DV], dtype=tl.float32)

    if split_kv_end > split_kv_start:
        ks = tl.load(k_scale)
        vs = tl.load(v_scale)
        for start_n in range(split_kv_start, split_kv_end, BLOCK_N):
            offs_n = start_n + tl.arange(0, BLOCK_N)
            kv_page_number = tl.load(
                Req_to_tokens
                + stride_req_to_tokens_b * cur_batch_req_idx
                + offs_n // PAGE_SIZE,
                mask=offs_n < split_kv_end,
                other=0,
            ).to(tl.int64)  # page_number * page stride overflows int32
            kv_in_page = offs_n % PAGE_SIZE
            offs_buf_k = (
                (kv_page_number * stride_buf_kpbs + kv_in_page * stride_buf_kbs)[
                    :, None
                ]
                + cur_kv_head * stride_buf_kh
                + offs_d[None, :]
            )
            k = tl.load(
                K_Buffer + offs_buf_k,
                mask=(offs_n[:, None] < split_kv_end) & (mask_d[None, :]),
                other=0.0,
            )
            if k.dtype.is_fp8():
                k = (k.to(tl.float32) * ks).to(q.dtype)
            qk = tl.sum(q[None, :] * k, 1)
            qk *= sm_scale

            if logit_cap > 0:
                qk = logit_cap * tanh(qk / logit_cap)

            qk = tl.where(offs_n < split_kv_end, qk, float("-inf"))

            offs_buf_v = (
                (kv_page_number * stride_buf_vpbs + kv_in_page * stride_buf_vbs)[
                    :, None
                ]
                + cur_kv_head * stride_buf_vh
                + offs_dv[None, :]
            )
            v = tl.load(
                V_Buffer + offs_buf_v,
                mask=(offs_n[:, None] < split_kv_end) & (mask_dv[None, :]),
                other=0.0,
            )
            if v.dtype.is_fp8():
                v = (v.to(tl.float32) * vs).to(q.dtype)

            n_e_max = tl.maximum(tl.max(qk, 0), e_max)
            re_scale = tl.exp(e_max - n_e_max)
            p = tl.exp(qk - n_e_max)
            acc *= re_scale
            acc += tl.sum(p[:, None] * v, 0)

            e_sum = e_sum * re_scale + tl.sum(p, 0)
            e_max = n_e_max

        offs_mid_o = (
            cur_batch.to(tl.int64) * stride_mid_ob
            + cur_head * stride_mid_oh
            + split_kv_id * stride_mid_os
            + offs_dv
        )

        tl.store(
            Att_Out + offs_mid_o,
            acc / e_sum,
            mask=(mask_dv),
        )

        offs_mid_o_1 = (
            cur_batch.to(tl.int64) * stride_mid_ob
            + cur_head * stride_mid_oh
            + split_kv_id * stride_mid_os
            + Lv
        )

        tl.store(
            Att_Out + offs_mid_o_1,
            e_max + tl.log(e_sum),
        )
```


---

### 🔹 Commit #13: `8f17dbf7`
- **完整 Hash**: `8f17dbf707459686eb7e500748552be98612218c`
- **說明 (Ground Truth)**: [Bugfix][KV Connector] Pair non-divisible hybrid MLA block sizes in NixlConnector (#61002)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/distributed/kv_transfer/kv_connector/v1/nixl/base_worker.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:237, E:423, A:0) ➔ After(N:239, E:430, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 7, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `gcd (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `NixlBaseConnectorWorker._split_remote_blocks` (FUNCTION_DEF)
  • + [新增呼叫邊] `NixlBaseConnectorWorker._split_remote_blocks` ──[CALLS]──> `gcd (External/Unresolved)`
  • + [新增呼叫邊] `NixlBaseConnectorWorker._split_remote_blocks` ──[CALLS]──> `max (External/Unresolved)`
  • + [新增呼叫邊] `NixlBaseConnectorWorker._split_remote_blocks` ──[CALLS]──> `warning (External/Unresolved)`
  • + [新增呼叫邊] `NixlBaseConnectorWorker._split_remote_blocks` ──[CALLS]──> `any (External/Unresolved)`
  • + [新增呼叫邊] `NixlBaseConnectorWorker._split_remote_blocks` ──[CALLS]──> `info_once (External/Unresolved)`
  • + [新增呼叫邊] `NixlBaseConnectorWorker._split_remote_blocks` ──[CALLS]──> `list (External/Unresolved)`
  • + [新增呼叫邊] `NixlBaseConnectorWorker.add_remote_agent` ──[CALLS]──> `NixlBaseConnectorWorker._split_remote_blocks`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `NixlBaseConnectorWorker.add_remote_agent()`
- **變更前簽章 (Before)**: `def add_remote_agent( self, nixl_agent_meta: NixlAgentMetadata, remote_tp_rank: int = 0, remote_tp_size: int = 1, remote_dcp_size: int = 1, ) -> str` (L2249~L2538)
- **變更後簽章 (After)**: `def add_remote_agent( self, nixl_agent_meta: NixlAgentMetadata, remote_tp_rank: int = 0, remote_tp_size: int = 1, remote_dcp_size: int = 1, ) -> str` (L2301~L2593)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def add_remote_agent(
        self,
        nixl_agent_meta: NixlAgentMetadata,
        remote_tp_rank: int = 0,
        remote_tp_size: int = 1,
        remote_dcp_size: int = 1,
    ) -> str:
        """Add the remote NIXL agent and prepare the descriptors for reading cache
        blocks from remote.

        In particular, handle both homogeneous and heterogeneous TP. The former
        requires local rank_i to read from remote rank_i.
        The latter, in the case of D.world_size < P.world_size, requires that a
        local (D) TP worker reads from multiple remote (P) TP workers.
        Conversely, assuming D.world_size > P.world_size, two or more local TP
        workers will read from a single remote TP worker.

        Here's an example for the last case described above (non-MLA):

        rank_offset     p_remote_tp_rank
        (kv split no)
        --------------------------------
            0                 0      Worker0  ---- 1st half of KV ----> Worker0  [ KV Cache ]
                                                                        /
            1                 0      Worker1  ---- 2nd half of KV -----/

            0                 1      Worker2  ---- 1st half of KV ----> Worker1  [ KV Cache ]
                                                                        /
            1                 1      Worker3  ---- 2nd half of KV -----/


                                Decoder TP workers                     Prefix TP workers
                                  (world_size=4)                         (world_size=2)
                                                 tp_ratio = 4 // 2 = 2

        Considering the KV Caches, if P-Worker_i has cache size [2, num_blocksP, kv_heads, block_size, head_dim]
        then D-Worker_j has [2, num_blocksD, kv_heads//tp_ratio, block_size, head_dim]. Mind the "LBHNC" layout format.
        Assuming num_blocksD >= num_blocksP, D-Worker0 reads from P-Worker0 by preparing the kv_heads//tp_ratio
        first heads from all the slots of all the blocks. D-Worker1 will do the same, but reading the second split
        along the kv_heads dimension, and so forth until "tp_ratio" D TP workers have pulled from P-Worker0.

        Note that the above will also hold true for the homogeneous TP case, where tp_ratio evaluates to 1.

        Regarding MLA case, the cache is replicated across TP workers so the rank_offset will just always be 0
        so that the whole cache is shared by "tp_ratio" D TP workers.

        For Mamba hetero-TP, both tp_ratio > 0 (D_TP > P_TP) and
        tp_ratio < 0 (P_TP > D_TP) are supported by the 3-read transfer.
        """  # noqa: E501
        engine_id = nixl_agent_meta.engine_id
        # TODO re-evaluate refreshing for scaling/recovery
        if (0, remote_tp_rank) in self._remote_agents.get(engine_id, {}):
            logger.debug(
                "Remote agent with engine_id %s and rank"
                "%s already exchanged metadata, skip handshake.",
                engine_id,
                remote_tp_rank,
            )
            return self._remote_agents[engine_id][(0, remote_tp_rank)]

        assert self.transfer_topo is not None
        transfer_topo = self.transfer_topo
        # Number of physical regions registered locally (one per layer/tensor).
        num_local_regions = len(self.block_len_per_layer)
        if self._transfer_layer_region_indices:
            if self.block_size != nixl_agent_meta.block_size:
                raise NotImplementedError(
                    "Attention-HMA push requires identical P/D block sizes."
                )
            if remote_tp_size > transfer_topo.tp_size and not self.use_mla:
                raise NotImplementedError(
                    "Attention-HMA push does not support decode TP greater than "
                    "prefill TP yet"
                )
            self._align_remote_regions_by_layer(nixl_agent_meta)
        elif nixl_agent_meta.packed_member_layouts and not self._packed_member_layouts:
            # With HiSparse, P may be on BL* while D is LB*, as only indexer is on HBM.
            # TODO (NickLucche) we may consider not allowing this case at all (P BL*)
            # and just clear this function.
            self._split_remote_packed_rows(nixl_agent_meta)
        elif (
            self.pp_size > 1
            and len(nixl_agent_meta.kv_caches_base_addr) > num_local_regions
        ):
            # This worker holds a PP layer-slice; the PP=1 remote registered
            # the full model. Slice its regions to our layer window so the
            # logic below sees congruent local/remote lists.
            start = self._remote_region_offset
            end = start + num_local_regions
            assert len(nixl_agent_meta.kv_caches_base_addr) >= end
            nixl_agent_meta.kv_caches_base_addr = nixl_agent_meta.kv_caches_base_addr[
                start:end
            ]
            nixl_agent_meta.block_lens = nixl_agent_meta.block_lens[start:end]
            nixl_agent_meta.block_strides = nixl_agent_meta.block_strides[start:end]
            if nixl_agent_meta.region_num_blocks is not None:
                nixl_agent_meta.region_num_blocks = nixl_agent_meta.region_num_blocks[
                    start:end
                ]
            if nixl_agent_meta.region_group_ids is not None:
                nixl_agent_meta.region_group_ids = nixl_agent_meta.region_group_ids[
                    start:end
                ]
            if nixl_agent_meta.region_names is not None:
                nixl_agent_meta.region_names = nixl_agent_meta.region_names[start:end]
            if nixl_agent_meta.region_mem_types is not None:
                nixl_agent_meta.region_mem_types = nixl_agent_meta.region_mem_types[
                    start:end
                ]

        if (
            self._packed_member_layouts
            and not self._transfer_layer_region_indices
            and self._packed_member_layouts != nixl_agent_meta.packed_member_layouts
        ):
            # Whole rows transfer as one unit, so both sides must pack them alike.
            raise RuntimeError(
                "Packed KV block rows differ between P and D. Use the same "
                "VLLM_KV_CACHE_LAYOUT and block size on both sides."
            )

        ### Register remote engine in TransferTopology (idempotent).
        physical_blocks_per_logical = (
            nixl_agent_meta.physical_blocks_per_logical_kv_block
        )
        transfer_info = EngineTransferInfo(
            remote_tp_size=remote_tp_size,
            remote_block_size=nixl_agent_meta.block_size,
            remote_block_len=nixl_agent_meta.block_lens[0],
            remote_physical_blocks_per_logical=physical_blocks_per_logical,
            remote_dcp_size=remote_dcp_size,
        )
        transfer_topo.register_remote_engine(engine_id, transfer_info)
        logger.info("Transfer plan: %s", transfer_topo.describe(engine_id))

        self.tp_mappings[engine_id] = compute_tp_mapping(
            transfer_topology=transfer_topo,
            remote_tp_size=remote_tp_size,
            group_spec_types=self._group_spec_types,
            remote_dcp_size=remote_dcp_size,
        )

        remote_agent_name = self.nixl_wrapper.add_remote_agent(
            nixl_agent_meta.agent_metadata
        )

        # Create dst descs and xfer side handles. TP workers have same #blocks
        # so we only register once per engine_id.
        # Example:
        # block_size_ratio > 1:
        # remote:               | 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|
        # local origin:|          0|          1|          8|         12|
        # local mapped:| 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|
        block_size_ratio = transfer_topo.block_size_ratio(nixl_agent_meta.block_size)

        if engine_id not in self.dst_num_blocks:
            num_remote_regions = len(nixl_agent_meta.kv_caches_base_addr)
            self.dst_num_blocks[engine_id] = nixl_agent_meta.num_blocks
            self.dst_region_num_blocks[engine_id] = (
                nixl_agent_meta.region_num_blocks
                or [nixl_agent_meta.num_blocks] * num_remote_regions
            )
            remote_region_group_ids = nixl_agent_meta.region_group_ids or (
                self.region_group_ids
                if len(self.region_group_ids) == num_remote_regions
                else [0] * num_remote_regions
            )
            self.dst_region_group_ids[engine_id] = remote_region_group_ids
            self.dst_uses_region_group_mapping[engine_id] = (
                len(set(self.dst_region_group_ids[engine_id])) > 1
            )
            self.dst_region_mem_types[engine_id] = (
                nixl_agent_meta.region_mem_types
                or [self.nixl_memory_type] * num_remote_regions
            )

        # Keep track of remote agent kv caches base addresses.
        self.kv_caches_base_addr[engine_id][remote_tp_rank] = (
            nixl_agent_meta.kv_caches_base_addr
        )
        self._validate_remote_agent_handshake(
            nixl_agent_meta, remote_tp_size, remote_dcp_size
        )

        # This is 1 when P and D `--tensor-parallel-size` match. Otherwise,
        # this is the ratio between the two sizes.
        tp_ratio = transfer_topo.tp_ratio(remote_tp_size)

        logger.debug(
            "Registering remote agent (%s, rank %s) memory regions with tp_ratio %s",
            engine_id,
            remote_tp_rank,
            tp_ratio,
        )

        plan = self.tp_mappings[engine_id]

        ### (Optional) Register a local handler at the remote engine's block
        ### granularity (remote/prefill blocks smaller than local).
        remote_block_size = nixl_agent_meta.block_size
        src_blocks_data = self.src_blocks_data
        if block_size_ratio > 1:
            if remote_block_size not in self.src_xfer_handles_by_block_size:
                handle, blocks_data = self.register_local_xfer_handler(
                    remote_block_size
                )
                self.src_xfer_handles_by_block_size[remote_block_size] = handle
                self.src_blocks_data_by_block_size[remote_block_size] = blocks_data
            src_blocks_data = self.src_blocks_data_by_block_size[remote_block_size]

        ### (Optional) Register local agent memory regions. MLA is not split.
        split_key = (tp_ratio, remote_block_size)
        if self._needs_split_local_xfer_handles(tp_ratio, plan) and (
            split_key not in self.src_xfer_handles_by_tp_ratio
        ):
            # Remote tp_size > local tp_size: read from multiple remote ranks.
            # Logically "split" own regions into per-source chunks. Hybrid
            # MLA+SSM also needs this path: MLA is replicated and read once,
            # while the SSM state is sharded across every remote TP rank.
            # We only do this once per remote (tp_size, block_size).
            self.src_xfer_handles_by_tp_ratio[split_key] = []
            if self._mixed_mem_types:
                self._dram_src_handles_by_tp_ratio[split_key] = []

            for handle_data in self._build_local_splits_from_plan(
                plan,
                src_blocks_data,
                self.num_descs * block_size_ratio,
                block_size_ratio,
            ):
                if self._mixed_mem_types:
                    desc_is_dram = self._desc_is_dram_by_block_size[remote_block_size]
                    strided_is_dram = desc_is_dram[
                        self._strided_desc_starts(handle_data)
                    ]
                    if self._skip_dram_xfer:
                        dram_handle = None
                    else:
                        dram_handle = self.nixl_wrapper.prep_xfer_dlist(
                            "NIXL_INIT_AGENT",
                            handle_data[strided_is_dram],
                            mem_type="DRAM",
                        )
                    self._dram_src_handles_by_tp_ratio[split_key].append(dram_handle)
                    handle_data = handle_data[~strided_is_dram]
                handle = self.nixl_wrapper.prep_xfer_dlist(
                    "NIXL_INIT_AGENT", handle_data, mem_type=self.nixl_memory_type
                )
                self.src_xfer_handles_by_tp_ratio[split_key].append(handle)

        ### Register remote agent memory regions
        # With homogeneous TP, D pulls the whole kv cache from corresponding rank. With
        # heterogeneous TP, prepare the descriptors by splitting the P KV cache along
        # kv_head dim, of D worker's kv_head size (D>P).
        # Eg. PTP1 DTP2 => P0 KV:[block0-KV_0 | block0-KV_1..].

        # Register all remote blocks, but only the corresponding kv heads.
        blocks_data = self._build_fa_remote(
            plan,
            nixl_agent_meta,
            block_size_ratio,
        )
        logger.debug(
            "Created %s blocks for dst engine %s with remote rank %s and local rank %s",
            blocks_data[:, 4].sum(),
            engine_id,
            remote_tp_rank,
            self.tp_rank,
        )
        if self._has_mamba:
            logger.debug(
                "Registering remote Mamba blocks for engine %s rank %s",
                engine_id,
                remote_tp_rank,
            )
            mamba = self._build_mamba_remote(nixl_agent_meta, tp_ratio, transfer_info)
            blocks_data = np.concatenate([blocks_data, mamba])

        remote_mem_types = set(self.dst_region_mem_types[engine_id])
        if len(remote_mem_types) != 1:
            raise NotImplementedError(
                "NIXL pull does not yet support a mixed-memory producer"
            )
        self.dst_xfer_side_handles[engine_id][remote_tp_rank] = (
            self.nixl_wrapper.prep_xfer_dlist(
                remote_agent_name, blocks_data, mem_type=remote_mem_types.pop()
            )
        )

        return remote_agent_name
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def add_remote_agent(
        self,
        nixl_agent_meta: NixlAgentMetadata,
        remote_tp_rank: int = 0,
        remote_tp_size: int = 1,
        remote_dcp_size: int = 1,
    ) -> str:
        """Add the remote NIXL agent and prepare the descriptors for reading cache
        blocks from remote.

        In particular, handle both homogeneous and heterogeneous TP. The former
        requires local rank_i to read from remote rank_i.
        The latter, in the case of D.world_size < P.world_size, requires that a
        local (D) TP worker reads from multiple remote (P) TP workers.
        Conversely, assuming D.world_size > P.world_size, two or more local TP
        workers will read from a single remote TP worker.

        Here's an example for the last case described above (non-MLA):

        rank_offset     p_remote_tp_rank
        (kv split no)
        --------------------------------
            0                 0      Worker0  ---- 1st half of KV ----> Worker0  [ KV Cache ]
                                                                        /
            1                 0      Worker1  ---- 2nd half of KV -----/

            0                 1      Worker2  ---- 1st half of KV ----> Worker1  [ KV Cache ]
                                                                        /
            1                 1      Worker3  ---- 2nd half of KV -----/


                                Decoder TP workers                     Prefix TP workers
                                  (world_size=4)                         (world_size=2)
                                                 tp_ratio = 4 // 2 = 2

        Considering the KV Caches, if P-Worker_i has cache size [2, num_blocksP, kv_heads, block_size, head_dim]
        then D-Worker_j has [2, num_blocksD, kv_heads//tp_ratio, block_size, head_dim]. Mind the "LBHNC" layout format.
        Assuming num_blocksD >= num_blocksP, D-Worker0 reads from P-Worker0 by preparing the kv_heads//tp_ratio
        first heads from all the slots of all the blocks. D-Worker1 will do the same, but reading the second split
        along the kv_heads dimension, and so forth until "tp_ratio" D TP workers have pulled from P-Worker0.

        Note that the above will also hold true for the homogeneous TP case, where tp_ratio evaluates to 1.

        Regarding MLA case, the cache is replicated across TP workers so the rank_offset will just always be 0
        so that the whole cache is shared by "tp_ratio" D TP workers.

        For Mamba hetero-TP, both tp_ratio > 0 (D_TP > P_TP) and
        tp_ratio < 0 (P_TP > D_TP) are supported by the 3-read transfer.
        """  # noqa: E501
        engine_id = nixl_agent_meta.engine_id
        # TODO re-evaluate refreshing for scaling/recovery
        if (0, remote_tp_rank) in self._remote_agents.get(engine_id, {}):
            logger.debug(
                "Remote agent with engine_id %s and rank"
                "%s already exchanged metadata, skip handshake.",
                engine_id,
                remote_tp_rank,
            )
            return self._remote_agents[engine_id][(0, remote_tp_rank)]

        assert self.transfer_topo is not None
        transfer_topo = self.transfer_topo
        # Number of physical regions registered locally (one per layer/tensor).
        num_local_regions = len(self.block_len_per_layer)
        if self._transfer_layer_region_indices:
            if self.block_size != nixl_agent_meta.block_size:
                raise NotImplementedError(
                    "Attention-HMA push requires identical P/D block sizes."
                )
            if remote_tp_size > transfer_topo.tp_size and not self.use_mla:
                raise NotImplementedError(
                    "Attention-HMA push does not support decode TP greater than "
                    "prefill TP yet"
                )
            self._align_remote_regions_by_layer(nixl_agent_meta)
        elif nixl_agent_meta.packed_member_layouts and not self._packed_member_layouts:
            # With HiSparse, P may be on BL* while D is LB*, as only indexer is on HBM.
            # TODO (NickLucche) we may consider not allowing this case at all (P BL*)
            # and just clear this function.
            self._split_remote_packed_rows(nixl_agent_meta)
        elif (
            self.pp_size > 1
            and len(nixl_agent_meta.kv_caches_base_addr) > num_local_regions
        ):
            # This worker holds a PP layer-slice; the PP=1 remote registered
            # the full model. Slice its regions to our layer window so the
            # logic below sees congruent local/remote lists.
            start = self._remote_region_offset
            end = start + num_local_regions
            assert len(nixl_agent_meta.kv_caches_base_addr) >= end
            nixl_agent_meta.kv_caches_base_addr = nixl_agent_meta.kv_caches_base_addr[
                start:end
            ]
            nixl_agent_meta.block_lens = nixl_agent_meta.block_lens[start:end]
            nixl_agent_meta.block_strides = nixl_agent_meta.block_strides[start:end]
            if nixl_agent_meta.region_num_blocks is not None:
                nixl_agent_meta.region_num_blocks = nixl_agent_meta.region_num_blocks[
                    start:end
                ]
            if nixl_agent_meta.region_group_ids is not None:
                nixl_agent_meta.region_group_ids = nixl_agent_meta.region_group_ids[
                    start:end
                ]
            if nixl_agent_meta.region_names is not None:
                nixl_agent_meta.region_names = nixl_agent_meta.region_names[start:end]
            if nixl_agent_meta.region_mem_types is not None:
                nixl_agent_meta.region_mem_types = nixl_agent_meta.region_mem_types[
                    start:end
                ]
        # The push WRITE path is not validated with split remote blocks.
        if self._has_mamba and self.use_mla and self._TRANSFER_MODE == "pull":
            self._split_remote_blocks(nixl_agent_meta)

        if (
            self._packed_member_layouts
            and not self._transfer_layer_region_indices
            and self._packed_member_layouts != nixl_agent_meta.packed_member_layouts
        ):
            # Whole rows transfer as one unit, so both sides must pack them alike.
            raise RuntimeError(
                "Packed KV block rows differ between P and D. Use the same "
                "VLLM_KV_CACHE_LAYOUT and block size on both sides."
            )

        ### Register remote engine in TransferTopology (idempotent).
        physical_blocks_per_logical = (
            nixl_agent_meta.physical_blocks_per_logical_kv_block
        )
        transfer_info = EngineTransferInfo(
            remote_tp_size=remote_tp_size,
            remote_block_size=nixl_agent_meta.block_size,
            remote_block_len=nixl_agent_meta.block_lens[0],
            remote_physical_blocks_per_logical=physical_blocks_per_logical,
            remote_dcp_size=remote_dcp_size,
        )
        transfer_topo.register_remote_engine(engine_id, transfer_info)
        logger.info("Transfer plan: %s", transfer_topo.describe(engine_id))

        self.tp_mappings[engine_id] = compute_tp_mapping(
            transfer_topology=transfer_topo,
            remote_tp_size=remote_tp_size,
            group_spec_types=self._group_spec_types,
            remote_dcp_size=remote_dcp_size,
        )

        remote_agent_name = self.nixl_wrapper.add_remote_agent(
            nixl_agent_meta.agent_metadata
        )

        # Create dst descs and xfer side handles. TP workers have same #blocks
        # so we only register once per engine_id.
        # Example:
        # block_size_ratio > 1:
        # remote:               | 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|
        # local origin:|          0|          1|          8|         12|
        # local mapped:| 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|
        block_size_ratio = transfer_topo.block_size_ratio(nixl_agent_meta.block_size)

        if engine_id not in self.dst_num_blocks:
            num_remote_regions = len(nixl_agent_meta.kv_caches_base_addr)
            self.dst_num_blocks[engine_id] = nixl_agent_meta.num_blocks
            self.dst_region_num_blocks[engine_id] = (
                nixl_agent_meta.region_num_blocks
                or [nixl_agent_meta.num_blocks] * num_remote_regions
            )
            remote_region_group_ids = nixl_agent_meta.region_group_ids or (
                self.region_group_ids
                if len(self.region_group_ids) == num_remote_regions
                else [0] * num_remote_regions
            )
            self.dst_region_group_ids[engine_id] = remote_region_group_ids
            self.dst_uses_region_group_mapping[engine_id] = (
                len(set(self.dst_region_group_ids[engine_id])) > 1
            )
            self.dst_region_mem_types[engine_id] = (
                nixl_agent_meta.region_mem_types
                or [self.nixl_memory_type] * num_remote_regions
            )

        # Keep track of remote agent kv caches base addresses.
        self.kv_caches_base_addr[engine_id][remote_tp_rank] = (
            nixl_agent_meta.kv_caches_base_addr
        )
        self._validate_remote_agent_handshake(
            nixl_agent_meta, remote_tp_size, remote_dcp_size
        )

        # This is 1 when P and D `--tensor-parallel-size` match. Otherwise,
        # this is the ratio between the two sizes.
        tp_ratio = transfer_topo.tp_ratio(remote_tp_size)

        logger.debug(
            "Registering remote agent (%s, rank %s) memory regions with tp_ratio %s",
            engine_id,
            remote_tp_rank,
            tp_ratio,
        )

        plan = self.tp_mappings[engine_id]

        ### (Optional) Register a local handler at the remote engine's block
        ### granularity (remote/prefill blocks smaller than local).
        remote_block_size = nixl_agent_meta.block_size
        src_blocks_data = self.src_blocks_data
        if block_size_ratio > 1:
            if remote_block_size not in self.src_xfer_handles_by_block_size:
                handle, blocks_data = self.register_local_xfer_handler(
                    remote_block_size
                )
                self.src_xfer_handles_by_block_size[remote_block_size] = handle
                self.src_blocks_data_by_block_size[remote_block_size] = blocks_data
            src_blocks_data = self.src_blocks_data_by_block_size[remote_block_size]

        ### (Optional) Register local agent memory regions. MLA is not split.
        split_key = (tp_ratio, remote_block_size)
        if self._needs_split_local_xfer_handles(tp_ratio, plan) and (
            split_key not in self.src_xfer_handles_by_tp_ratio
        ):
            # Remote tp_size > local tp_size: read from multiple remote ranks.
            # Logically "split" own regions into per-source chunks. Hybrid
            # MLA+SSM also needs this path: MLA is replicated and read once,
            # while the SSM state is sharded across every remote TP rank.
            # We only do this once per remote (tp_size, block_size).
            self.src_xfer_handles_by_tp_ratio[split_key] = []
            if self._mixed_mem_types:
                self._dram_src_handles_by_tp_ratio[split_key] = []

            for handle_data in self._build_local_splits_from_plan(
                plan,
                src_blocks_data,
                self.num_descs * block_size_ratio,
                block_size_ratio,
            ):
                if self._mixed_mem_types:
                    desc_is_dram = self._desc_is_dram_by_block_size[remote_block_size]
                    strided_is_dram = desc_is_dram[
                        self._strided_desc_starts(handle_data)
                    ]
                    if self._skip_dram_xfer:
                        dram_handle = None
                    else:
                        dram_handle = self.nixl_wrapper.prep_xfer_dlist(
                            "NIXL_INIT_AGENT",
                            handle_data[strided_is_dram],
                            mem_type="DRAM",
                        )
                    self._dram_src_handles_by_tp_ratio[split_key].append(dram_handle)
                    handle_data = handle_data[~strided_is_dram]
                handle = self.nixl_wrapper.prep_xfer_dlist(
                    "NIXL_INIT_AGENT", handle_data, mem_type=self.nixl_memory_type
                )
                self.src_xfer_handles_by_tp_ratio[split_key].append(handle)

        ### Register remote agent memory regions
        # With homogeneous TP, D pulls the whole kv cache from corresponding rank. With
        # heterogeneous TP, prepare the descriptors by splitting the P KV cache along
        # kv_head dim, of D worker's kv_head size (D>P).
        # Eg. PTP1 DTP2 => P0 KV:[block0-KV_0 | block0-KV_1..].

        # Register all remote blocks, but only the corresponding kv heads.
        blocks_data = self._build_fa_remote(
            plan,
            nixl_agent_meta,
            block_size_ratio,
        )
        logger.debug(
            "Created %s blocks for dst engine %s with remote rank %s and local rank %s",
            blocks_data[:, 4].sum(),
            engine_id,
            remote_tp_rank,
            self.tp_rank,
        )
        if self._has_mamba:
            logger.debug(
                "Registering remote Mamba blocks for engine %s rank %s",
                engine_id,
                remote_tp_rank,
            )
            mamba = self._build_mamba_remote(nixl_agent_meta, tp_ratio, transfer_info)
            blocks_data = np.concatenate([blocks_data, mamba])

        remote_mem_types = set(self.dst_region_mem_types[engine_id])
        if len(remote_mem_types) != 1:
            raise NotImplementedError(
                "NIXL pull does not yet support a mixed-memory producer"
            )
        self.dst_xfer_side_handles[engine_id][remote_tp_rank] = (
            self.nixl_wrapper.prep_xfer_dlist(
                remote_agent_name, blocks_data, mem_type=remote_mem_types.pop()
            )
        )

        return remote_agent_name
```


---

### 🔹 Commit #14: `3f1b04e0`
- **完整 Hash**: `3f1b04e045beb841329519bacafa9b2ded86a762`
- **說明 (Ground Truth)**: [Bugfix] Fix Opencv video backend frames count missing for WebM video inputs (#61759)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/multimodal/video_decoders/opencv.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:33, E:40, A:0) ➔ After(N:35, E:48, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 8, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `release (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `OpenCVVideoBackendMixin.demux_count_frames` (FUNCTION_DEF)
  • + [新增呼叫邊] `OpenCVVideoBackendMixin.demux_count_frames` ──[CALLS]──> `BytesIO (External/Unresolved)`
  • + [新增呼叫邊] `OpenCVVideoBackendMixin.demux_count_frames` ──[CALLS]──> `VideoCapture (External/Unresolved)`
  • + [新增呼叫邊] `OpenCVVideoBackendMixin.demux_count_frames` ──[CALLS]──> `OpenCVVideoBackendMixin.get_cv2_video_api`
  • + [新增呼叫邊] `OpenCVVideoBackendMixin.demux_count_frames` ──[CALLS]──> `grab (External/Unresolved)`
  • + [新增呼叫邊] `OpenCVVideoBackendMixin.demux_count_frames` ──[CALLS]──> `release (External/Unresolved)`
  • + [新增呼叫邊] `OpenCVVideoBackendMixin.demux_count_frames` ──[CALLS]──> `ValueError (External/Unresolved)`
  • + [新增呼叫邊] `OpenCVVideoBackendMixin.get_video_metadata` ──[CALLS]──> `OpenCVVideoBackendMixin.open_video_capture`
  • + [新增呼叫邊] `OpenCVVideoBackendMixin.get_video_metadata` ──[CALLS]──> `OpenCVVideoBackendMixin.demux_count_frames`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `OpenCVVideoBackendMixin.get_video_metadata()`
- **變更前簽章 (Before)**: `def get_video_metadata(cap: "cv2.VideoCapture") -> VideoSourceMetadata` (L78~L107)
- **變更後簽章 (After)**: `def get_video_metadata(data: bytes) -> VideoSourceMetadata` (L97~L133)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def get_video_metadata(cap: "cv2.VideoCapture") -> VideoSourceMetadata:
        total_frames_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        # CAP_PROP_FRAME_COUNT counts every physical sample in the container,
        # overstating the presentable frames when an mp4 edit list hides the
        # decode lead-in (e.g. a lossless `ffmpeg -ss ... -c copy` trim).
        # Cross-check with an end-of-stream seek: the FFMPEG backend reports
        # the resulting position against the edit-list-aware timeline, which
        # exposes the true frame count without decoding anything. The seek
        # may land mid-stream on corrupt files, so only trust it when the
        # stream really ends there. A one-frame tolerance keeps mere header
        # miscounts from being "corrected".
        if total_frames_num > 0 and cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1.0):
            visible_frames = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            at_stream_end = not cap.grab()
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            if at_stream_end and 0 < visible_frames < total_frames_num - 1:
                logger.warning(
                    "Video header claims %d frames but only %d are "
                    "presentable; sampling over the true frame count.",
                    total_frames_num,
                    visible_frames,
                )
                total_frames_num = visible_frames
        duration = total_frames_num / original_fps if original_fps > 0 else 0
        return VideoSourceMetadata(
            total_frames_num=total_frames_num,
            original_fps=original_fps,
            duration=duration,
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def get_video_metadata(data: bytes) -> VideoSourceMetadata:
        cap = OpenCVVideoBackendMixin.open_video_capture(data)
        total_frames_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        if total_frames_num <= 0:
            # Streamed WebM/MKV and raw H.264 miss frame count in headers;
            # We need to use demux frames count for retrieval
            total_frames_num = OpenCVVideoBackendMixin.demux_count_frames(data)
            duration = total_frames_num / original_fps if original_fps > 0 else 0
            return VideoSourceMetadata(total_frames_num, original_fps, duration)
        # CAP_PROP_FRAME_COUNT counts every physical sample in the container,
        # overstating the presentable frames when an mp4 edit list hides the
        # decode lead-in (e.g. a lossless `ffmpeg -ss ... -c copy` trim).
        # Cross-check with an end-of-stream seek: the FFMPEG backend reports
        # the resulting position against the edit-list-aware timeline, which
        # exposes the true frame count without decoding anything. The seek
        # may land mid-stream on corrupt files, so only trust it when the
        # stream really ends there. A one-frame tolerance keeps mere header
        # miscounts from being "corrected".
        if cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1.0):
            visible_frames = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            at_stream_end = not cap.grab()
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            if at_stream_end and 0 < visible_frames < total_frames_num - 1:
                logger.warning(
                    "Video header claims %d frames but only %d are "
                    "presentable; sampling over the true frame count.",
                    total_frames_num,
                    visible_frames,
                )
                total_frames_num = visible_frames
        duration = total_frames_num / original_fps if original_fps > 0 else 0
        return VideoSourceMetadata(
            total_frames_num=total_frames_num,
            original_fps=original_fps,
            duration=duration,
        )
```

### 🔹 函式: `decode_opencv()`
- **變更前簽章 (Before)**: `def decode_opencv( loader_cls, data: bytes, target: VideoTargetMetadata, sampling_kwargs: dict, *, frame_recovery: bool = False, ) -> tuple[npt.NDArray, VideoSourceMetadata, list[int], list[int]]` (L28~L51)
- **變更後簽章 (After)**: `def decode_opencv( loader_cls, data: bytes, target: VideoTargetMetadata, sampling_kwargs: dict, *, frame_recovery: bool = False, ) -> tuple[npt.NDArray, VideoSourceMetadata, list[int], list[int]]` (L28~L53)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def decode_opencv(
    loader_cls,
    data: bytes,
    target: VideoTargetMetadata,
    sampling_kwargs: dict,
    *,
    frame_recovery: bool = False,
) -> tuple[npt.NDArray, VideoSourceMetadata, list[int], list[int]]:
    cap = OpenCVVideoBackendMixin.open_video_capture(data)
    check_frame_pixel_limit(
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    source = loader_cls._prepare_source(OpenCVVideoBackendMixin.get_video_metadata(cap))
    frame_idx = loader_cls.compute_frames_index_to_sample(
        source=source, target=target, **sampling_kwargs
    )
    frames, valid = loader_cls.read_frames(
        cap,
        frame_idx,
        total_frames_num=source.total_frames_num,
        frame_recovery=frame_recovery,
    )
    return frames, source, frame_idx, valid
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def decode_opencv(
    loader_cls,
    data: bytes,
    target: VideoTargetMetadata,
    sampling_kwargs: dict,
    *,
    frame_recovery: bool = False,
) -> tuple[npt.NDArray, VideoSourceMetadata, list[int], list[int]]:
    cap = OpenCVVideoBackendMixin.open_video_capture(data)
    check_frame_pixel_limit(
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    source = loader_cls._prepare_source(
        OpenCVVideoBackendMixin.get_video_metadata(data)
    )
    frame_idx = loader_cls.compute_frames_index_to_sample(
        source=source, target=target, **sampling_kwargs
    )
    frames, valid = loader_cls.read_frames(
        cap,
        frame_idx,
        total_frames_num=source.total_frames_num,
        frame_recovery=frame_recovery,
    )
    return frames, source, frame_idx, valid
```


---

### 🔹 Commit #15: `7c9042c0`
- **完整 Hash**: `7c9042c05addf034366b9a1da5b1d3e3687c052b`
- **說明 (Ground Truth)**: [Bugfix][MRV2] Fix speculative warmup deadlock with pipeline parallelism (#62129)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/v1/worker/gpu/warmup.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:44, E:64, A:0) ➔ After(N:44, E:64, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'block_count' 被深鎖在內部閉包 (scope:_warmup_block_counter@after/vllm/v1/worker/gpu/warmup.py:L67)，外部無法調用！ (共 3 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `warmup_kernels()`
- **變更前簽章 (Before)**: `def warmup_kernels( model_runner: GPUModelRunner, worker_execute_model: Callable[[SchedulerOutput], Any], worker_sample_tokens: Callable[[GrammarOutput | None], Any], ) -> None` (L218~L251)
- **變更後簽章 (After)**: `def warmup_kernels( model_runner: GPUModelRunner, worker_execute_model: Callable[[SchedulerOutput], Any], worker_sample_tokens: Callable[[GrammarOutput | None], Any], ) -> None` (L218~L252)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def warmup_kernels(
    model_runner: GPUModelRunner,
    worker_execute_model: Callable[[SchedulerOutput], Any],
    worker_sample_tokens: Callable[[GrammarOutput | None], Any],
) -> None:
    """Run scheduler-realistic prefill and decode steps to JIT compile kernels.

    We must call the provided worker's execute_model for pipeline parallel
    coordination.
    """
    # Adaptive costs are calibrated during capture, after this warmup. Exercise
    # fixed draft counts here, then restore the manager for capture and serving.
    adaptive_verification = model_runner.adaptive_verification
    model_runner.adaptive_verification = None
    rejection_sampler = model_runner.rejection_sampler
    adaptive_sampling = (
        rejection_sampler is not None and rejection_sampler.enable_adaptive_verification
    )
    if adaptive_sampling:
        assert rejection_sampler is not None
        rejection_sampler.enable_adaptive_verification = False
    try:
        _warmup_kernels(model_runner, worker_execute_model, worker_sample_tokens)
        if rejection_sampler is not None:
            # Greedy batches skip logits processing, so rejection kernels
            # also see model-dtype logits instead of FP32.
            _warmup_kernels(
                model_runner, worker_execute_model, worker_sample_tokens, greedy=True
            )
    finally:
        model_runner.adaptive_verification = adaptive_verification
        if adaptive_sampling:
            assert rejection_sampler is not None
            rejection_sampler.enable_adaptive_verification = True
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def warmup_kernels(
    model_runner: GPUModelRunner,
    worker_execute_model: Callable[[SchedulerOutput], Any],
    worker_sample_tokens: Callable[[GrammarOutput | None], Any],
) -> None:
    """Run scheduler-realistic prefill and decode steps to JIT compile kernels.

    We must call the provided worker's execute_model for pipeline parallel
    coordination.
    """
    # Adaptive costs are calibrated during capture, after this warmup. Exercise
    # fixed draft counts here, then restore the manager for capture and serving.
    adaptive_verification = model_runner.adaptive_verification
    model_runner.adaptive_verification = None
    rejection_sampler = model_runner.rejection_sampler
    adaptive_sampling = (
        rejection_sampler is not None and rejection_sampler.enable_adaptive_verification
    )
    if adaptive_sampling:
        assert rejection_sampler is not None
        rejection_sampler.enable_adaptive_verification = False
    try:
        _warmup_kernels(model_runner, worker_execute_model, worker_sample_tokens)
        # All PP ranks must run the same forwards to match sends and receives.
        if model_runner.speculative_config is not None:
            # Greedy batches skip logits processing, so rejection kernels
            # also see model-dtype logits instead of FP32.
            _warmup_kernels(
                model_runner, worker_execute_model, worker_sample_tokens, greedy=True
            )
    finally:
        model_runner.adaptive_verification = adaptive_verification
        if adaptive_sampling:
            assert rejection_sampler is not None
            rejection_sampler.enable_adaptive_verification = True
```


---

### 🔹 Commit #16: `5c1c9035`
- **完整 Hash**: `5c1c903501927ea7c6c699aabd4c271015e66e71`
- **說明 (Ground Truth)**: [Perf][Parser] Stream Qwen3 tool argument values incrementally (12 KB call: 2.1 s to 11 ms) (#62027)
- **變更檔案數**: 2

#### 📄 檔案: `vllm/parser/mimo.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:11, E:10, A:0) ➔ After(N:12, E:11, A:0)
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
  • + [新增節點] `partial (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `MiMoParser.__init__` ──[CALLS]──> `partial (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `MiMoParser.__init__()`
- **變更前簽章 (Before)**: `def __init__(self, tokenizer, tools=None, **kwargs)` (L27~L42)
- **變更後簽章 (After)**: `def __init__(self, tokenizer, tools=None, **kwargs)` (L29~L47)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(self, tokenizer, tools=None, **kwargs):
        thinking = (kwargs.get("chat_template_kwargs") or {}).get(
            "enable_thinking", True
        )
        kwargs.setdefault(
            "parser_engine_config",
            replace(
                qwen3_config(
                    thinking=thinking,
                    name="mimo",
                    turn_boundary_tokens=CHATML_TURN_BOUNDARIES,
                ),
                arg_converter=_mimo_arg_converter,
            ),
        )
        super().__init__(tokenizer, tools, **kwargs)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(self, tokenizer, tools=None, **kwargs):
        thinking = (kwargs.get("chat_template_kwargs") or {}).get(
            "enable_thinking", True
        )
        kwargs.setdefault(
            "parser_engine_config",
            replace(
                qwen3_config(
                    thinking=thinking,
                    name="mimo",
                    turn_boundary_tokens=CHATML_TURN_BOUNDARIES,
                ),
                arg_converter=_mimo_arg_converter,
                arg_value_extender=functools.partial(
                    _param_value_extender, trim_newlines=False
                ),
            ),
        )
        super().__init__(tokenizer, tools, **kwargs)
```


#### 📄 檔案: `vllm/parser/qwen3.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:16, E:15, A:0) ➔ After(N:25, E:29, A:0)
- **差分統計**: +Nodes: 9, -Nodes: 0, +Edges: 14, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `extend` (FUNCTION_DEF)
  • + [新增節點] `_param_value_end_window` (FUNCTION_DEF)
  • + [新增節點] `any (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `removeprefix (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `fullmatch (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `_param_value_extender` (FUNCTION_DEF)
  • + [新增節點] `bool (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `_qwen3_arg_value_extender` (FUNCTION_DEF)
  • + [新增節點] `rfind (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `_param_value_end_window` ──[CALLS]──> `rfind (External/Unresolved)`
  • + [新增呼叫邊] `_param_value_end_window` ──[CALLS]──> `fullmatch (External/Unresolved)`
  • + [新增呼叫邊] `_param_value_extender` ──[CALLS]──> `search (External/Unresolved)`
  • + [新增呼叫邊] `_param_value_extender` ──[CALLS]──> `sub (External/Unresolved)`
  • + [新增呼叫邊] `_param_value_extender` ──[CALLS]──> `group (External/Unresolved)`
  • + [新增呼叫邊] `_param_value_extender` ──[CALLS]──> `any (External/Unresolved)`
  • _... 以及其餘 8 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `qwen3_config()`
- **變更前簽章 (Before)**: `def qwen3_config( thinking: bool = True, *, name: str = "qwen3", think_start: str = THINK_START, think_end: str = THINK_END, tool_start: str = TOOL_CALL_START, tool_end: str = TOOL_CALL_END, turn_boundary_tokens: frozenset[str] = frozenset(), ) -> ParserEngineConfig` (L90~L229)
- **變更後簽章 (After)**: `def qwen3_config( thinking: bool = True, *, name: str = "qwen3", think_start: str = THINK_START, think_end: str = THINK_END, tool_start: str = TOOL_CALL_START, tool_end: str = TOOL_CALL_END, turn_boundary_tokens: frozenset[str] = frozenset(), ) -> ParserEngineConfig` (L149~L289)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def qwen3_config(
    thinking: bool = True,
    *,
    name: str = "qwen3",
    think_start: str = THINK_START,
    think_end: str = THINK_END,
    tool_start: str = TOOL_CALL_START,
    tool_end: str = TOOL_CALL_END,
    turn_boundary_tokens: frozenset[str] = frozenset(),
) -> ParserEngineConfig:
    return ParserEngineConfig(
        name=name,
        initial_state=ParserState.REASONING if thinking else ParserState.CONTENT,
        wait_for_reasoning=thinking,
        turn_boundary_tokens=turn_boundary_tokens,
        terminals={
            # Reasoning terminals
            "THINK_START": think_start,
            "THINK_END": think_end,
            # Tool call terminals
            "TOOL_START": tool_start,
            "TOOL_END": tool_end,
            "FUNC_PREFIX": FUNC_PREFIX,
            "FUNC_END": FUNC_END,
            "PARAM_START": PARAM_START,
            "PARAM_END": PARAM_END,
            "CLOSE_ANGLE": ">",
        },
        token_id_terminals={
            "THINK_START": think_start,
            "THINK_END": think_end,
            "TOOL_START": tool_start,
            "TOOL_END": tool_end,
        },
        transitions={
            # -- Reasoning transitions --
            (ParserState.REASONING, "THINK_START"): Transition(
                ParserState.REASONING,
                (),
            ),
            (ParserState.REASONING, "THINK_END"): Transition(
                ParserState.CONTENT,
                (EventType.REASONING_END,),
            ),
            # Absorb duplicate </think> — model may emit it after
            # already transitioning to CONTENT; drop it silently.
            (ParserState.CONTENT, "THINK_END"): Transition(
                ParserState.CONTENT,
                (),
            ),
            # Tool call directly from reasoning (implicit end)
            (ParserState.REASONING, "TOOL_START"): Transition(
                ParserState.TOOL_PREAMBLE,
                (EventType.REASONING_END, EventType.TOOL_CALL_START),
            ),
            # -- Tool call transitions --
            (ParserState.CONTENT, "TOOL_START"): Transition(
                ParserState.TOOL_PREAMBLE,
                (EventType.REASONING_END, EventType.TOOL_CALL_START),
            ),
            # Fallback: <function= without a preceding <tool_call>
            (ParserState.CONTENT, "FUNC_PREFIX"): Transition(
                ParserState.TOOL_NAME,
                (EventType.TOOL_CALL_START,),
            ),
            (ParserState.TOOL_PREAMBLE, "TOOL_END"): Transition(
                ParserState.CONTENT,
                (EventType.TOOL_CALL_END,),
            ),
            (ParserState.TOOL_PREAMBLE, "FUNC_PREFIX"): Transition(
                ParserState.TOOL_NAME,
                (),
            ),
            (ParserState.TOOL_NAME, "CLOSE_ANGLE"): Transition(
                ParserState.TOOL_ARGS,
                (),
            ),
            # Malformed: </function> while still in TOOL_NAME (no closing >)
            (ParserState.TOOL_NAME, "FUNC_END"): Transition(
                ParserState.TOOL_BETWEEN,
                (EventType.TOOL_CALL_END,),
            ),
            # regression issue 58227
            # <function=...</tool_call>
            # function name is not closed, go to content
            (ParserState.TOOL_NAME, "TOOL_END"): Transition(
                ParserState.CONTENT,
                (EventType.TOOL_CALL_END,),
            ),
            # regression issue 58227
            # <function=...<tool_call>
            # unclosed tool call followed by another tool call
            (ParserState.TOOL_NAME, "TOOL_START"): Transition(
                ParserState.TOOL_PREAMBLE,
                (EventType.TOOL_CALL_END, EventType.TOOL_CALL_START),
            ),
            # regression issue 58227
            # <function=...<function=
            # unclosed function name followed by another function name
            (ParserState.TOOL_NAME, "FUNC_PREFIX"): Transition(
                ParserState.TOOL_NAME,
                (EventType.TOOL_CALL_END, EventType.TOOL_CALL_START),
            ),
            (ParserState.TOOL_ARGS, "FUNC_END"): Transition(
                ParserState.TOOL_BETWEEN,
                (EventType.TOOL_CALL_END,),
            ),
            # regression issue 58227
            # <function=abc>...<function=
            (ParserState.TOOL_ARGS, "FUNC_PREFIX"): Transition(
                ParserState.TOOL_NAME,
                (EventType.TOOL_CALL_END, EventType.TOOL_CALL_START),
            ),
            (ParserState.TOOL_ARGS, "PARAM_START"): Transition(
                ParserState.TOOL_ARGS,
                (EventType.ARG_VALUE_CHUNK,),
            ),
            (ParserState.TOOL_ARGS, "PARAM_END"): Transition(
                ParserState.TOOL_ARGS,
                (EventType.ARG_VALUE_CHUNK,),
            ),
            (ParserState.TOOL_BETWEEN, "TOOL_END"): Transition(
                ParserState.CONTENT,
                (),
            ),
            # Consecutive tool call without closing </tool_call>
            (ParserState.TOOL_BETWEEN, "TOOL_START"): Transition(
                ParserState.TOOL_PREAMBLE,
                (EventType.TOOL_CALL_START,),
            ),
            (ParserState.TOOL_BETWEEN, "FUNC_PREFIX"): Transition(
                ParserState.TOOL_NAME,
                (EventType.TOOL_CALL_START,),
            ),
        },
        arg_converter=_qwen3_arg_converter,
        stream_arg_deltas=True,
        strip_trailing_reasoning_whitespace=False,
        tool_args_json=False,
    )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def qwen3_config(
    thinking: bool = True,
    *,
    name: str = "qwen3",
    think_start: str = THINK_START,
    think_end: str = THINK_END,
    tool_start: str = TOOL_CALL_START,
    tool_end: str = TOOL_CALL_END,
    turn_boundary_tokens: frozenset[str] = frozenset(),
) -> ParserEngineConfig:
    return ParserEngineConfig(
        name=name,
        initial_state=ParserState.REASONING if thinking else ParserState.CONTENT,
        wait_for_reasoning=thinking,
        turn_boundary_tokens=turn_boundary_tokens,
        terminals={
            # Reasoning terminals
            "THINK_START": think_start,
            "THINK_END": think_end,
            # Tool call terminals
            "TOOL_START": tool_start,
            "TOOL_END": tool_end,
            "FUNC_PREFIX": FUNC_PREFIX,
            "FUNC_END": FUNC_END,
            "PARAM_START": PARAM_START,
            "PARAM_END": PARAM_END,
            "CLOSE_ANGLE": ">",
        },
        token_id_terminals={
            "THINK_START": think_start,
            "THINK_END": think_end,
            "TOOL_START": tool_start,
            "TOOL_END": tool_end,
        },
        transitions={
            # -- Reasoning transitions --
            (ParserState.REASONING, "THINK_START"): Transition(
                ParserState.REASONING,
                (),
            ),
            (ParserState.REASONING, "THINK_END"): Transition(
                ParserState.CONTENT,
                (EventType.REASONING_END,),
            ),
            # Absorb duplicate </think> — model may emit it after
            # already transitioning to CONTENT; drop it silently.
            (ParserState.CONTENT, "THINK_END"): Transition(
                ParserState.CONTENT,
                (),
            ),
            # Tool call directly from reasoning (implicit end)
            (ParserState.REASONING, "TOOL_START"): Transition(
                ParserState.TOOL_PREAMBLE,
                (EventType.REASONING_END, EventType.TOOL_CALL_START),
            ),
            # -- Tool call transitions --
            (ParserState.CONTENT, "TOOL_START"): Transition(
                ParserState.TOOL_PREAMBLE,
                (EventType.REASONING_END, EventType.TOOL_CALL_START),
            ),
            # Fallback: <function= without a preceding <tool_call>
            (ParserState.CONTENT, "FUNC_PREFIX"): Transition(
                ParserState.TOOL_NAME,
                (EventType.TOOL_CALL_START,),
            ),
            (ParserState.TOOL_PREAMBLE, "TOOL_END"): Transition(
                ParserState.CONTENT,
                (EventType.TOOL_CALL_END,),
            ),
            (ParserState.TOOL_PREAMBLE, "FUNC_PREFIX"): Transition(
                ParserState.TOOL_NAME,
                (),
            ),
            (ParserState.TOOL_NAME, "CLOSE_ANGLE"): Transition(
                ParserState.TOOL_ARGS,
                (),
            ),
            # Malformed: </function> while still in TOOL_NAME (no closing >)
            (ParserState.TOOL_NAME, "FUNC_END"): Transition(
                ParserState.TOOL_BETWEEN,
                (EventType.TOOL_CALL_END,),
            ),
            # regression issue 58227
            # <function=...</tool_call>
            # function name is not closed, go to content
            (ParserState.TOOL_NAME, "TOOL_END"): Transition(
                ParserState.CONTENT,
                (EventType.TOOL_CALL_END,),
            ),
            # regression issue 58227
            # <function=...<tool_call>
            # unclosed tool call followed by another tool call
            (ParserState.TOOL_NAME, "TOOL_START"): Transition(
                ParserState.TOOL_PREAMBLE,
                (EventType.TOOL_CALL_END, EventType.TOOL_CALL_START),
            ),
            # regression issue 58227
            # <function=...<function=
            # unclosed function name followed by another function name
            (ParserState.TOOL_NAME, "FUNC_PREFIX"): Transition(
                ParserState.TOOL_NAME,
                (EventType.TOOL_CALL_END, EventType.TOOL_CALL_START),
            ),
            (ParserState.TOOL_ARGS, "FUNC_END"): Transition(
                ParserState.TOOL_BETWEEN,
                (EventType.TOOL_CALL_END,),
            ),
            # regression issue 58227
            # <function=abc>...<function=
            (ParserState.TOOL_ARGS, "FUNC_PREFIX"): Transition(
                ParserState.TOOL_NAME,
                (EventType.TOOL_CALL_END, EventType.TOOL_CALL_START),
            ),
            (ParserState.TOOL_ARGS, "PARAM_START"): Transition(
                ParserState.TOOL_ARGS,
                (EventType.ARG_VALUE_CHUNK,),
            ),
            (ParserState.TOOL_ARGS, "PARAM_END"): Transition(
                ParserState.TOOL_ARGS,
                (EventType.ARG_VALUE_CHUNK,),
            ),
            (ParserState.TOOL_BETWEEN, "TOOL_END"): Transition(
                ParserState.CONTENT,
                (),
            ),
            # Consecutive tool call without closing </tool_call>
            (ParserState.TOOL_BETWEEN, "TOOL_START"): Transition(
                ParserState.TOOL_PREAMBLE,
                (EventType.TOOL_CALL_START,),
            ),
            (ParserState.TOOL_BETWEEN, "FUNC_PREFIX"): Transition(
                ParserState.TOOL_NAME,
                (EventType.TOOL_CALL_START,),
            ),
        },
        arg_converter=_qwen3_arg_converter,
        arg_value_extender=_qwen3_arg_value_extender,
        stream_arg_deltas=True,
        strip_trailing_reasoning_whitespace=False,
        tool_args_json=False,
    )
```


---

### 🔹 Commit #17: `4e964b26`
- **完整 Hash**: `4e964b2623c951d063f4b7f23790d16f2d6b7f94`
- **說明 (Ground Truth)**: [XPU] Fix Event init failure w/ external (#61743)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/v1/worker/xpu_model_runner.py`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:9, E:12, A:0) ➔ After(N:9, E:12, A:0)
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

### 🔹 函式: `_xpu_event()`
- **變更前簽章 (Before)**: `def _xpu_event(*args, blocking=None, **kwargs)` (L66~L67)
- **變更後簽章 (After)**: `def _xpu_event(*args, blocking=None, external=None, **kwargs)` (L66~L67)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _xpu_event(*args, blocking=None, **kwargs):
        return torch.xpu.Event(*args, **kwargs)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _xpu_event(*args, blocking=None, external=None, **kwargs):
        return torch.xpu.Event(*args, **kwargs)
```

### 🔹 函式: `_torch_cuda_wrapper()`
- **變更前簽章 (Before)**: `def _torch_cuda_wrapper(): # Replace cuda APIs with xpu APIs. Each callable gets its own functools.partial # so it is not the same object as torch.xpu.* (Torch Dynamo _get_handlers() # asserts on duplicate registration when cuda aliases xpu directly).` (L54~L75)
- **變更後簽章 (After)**: `def _torch_cuda_wrapper(): # Replace cuda APIs with xpu APIs. Each callable gets its own functools.partial # so it is not the same object as torch.xpu.* (Torch Dynamo _get_handlers() # asserts on duplicate registration when cuda aliases xpu directly).` (L54~L75)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def _torch_cuda_wrapper():
    # Replace cuda APIs with xpu APIs. Each callable gets its own functools.partial
    # so it is not the same object as torch.xpu.* (Torch Dynamo _get_handlers()
    # asserts on duplicate registration when cuda aliases xpu directly).
    torch.cuda.Stream = torch.xpu.Stream
    torch.cuda.default_stream = partial(torch.xpu.current_stream)
    torch.cuda.current_stream = partial(torch.xpu.current_stream)
    torch.cuda.stream = partial(torch.xpu.stream)
    torch.cuda.set_stream = partial(torch.xpu.set_stream)

    # torch.xpu.Event does not accept the ``blocking`` kwarg that
    # torch.cuda.Event supports, so drop it here.
    def _xpu_event(*args, blocking=None, **kwargs):
        return torch.xpu.Event(*args, **kwargs)

    torch.cuda.Event = _xpu_event
    if supports_xpu_graph():
        torch.cuda.graph = partial(torch.xpu.graph)
        torch.cuda.CUDAGraph = torch.xpu.XPUGraph
        torch.cuda.graph_pool_handle = partial(torch.xpu.graph_pool_handle)
        torch.cuda.is_current_stream_capturing = torch.xpu.is_current_stream_capturing
    yield
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def _torch_cuda_wrapper():
    # Replace cuda APIs with xpu APIs. Each callable gets its own functools.partial
    # so it is not the same object as torch.xpu.* (Torch Dynamo _get_handlers()
    # asserts on duplicate registration when cuda aliases xpu directly).
    torch.cuda.Stream = torch.xpu.Stream
    torch.cuda.default_stream = partial(torch.xpu.current_stream)
    torch.cuda.current_stream = partial(torch.xpu.current_stream)
    torch.cuda.stream = partial(torch.xpu.stream)
    torch.cuda.set_stream = partial(torch.xpu.set_stream)

    # torch.xpu.Event does not accept the ``blocking`` or ``external`` kwargs
    # that torch.cuda.Event supports, so drop them here.
    def _xpu_event(*args, blocking=None, external=None, **kwargs):
        return torch.xpu.Event(*args, **kwargs)

    torch.cuda.Event = _xpu_event
    if supports_xpu_graph():
        torch.cuda.graph = partial(torch.xpu.graph)
        torch.cuda.CUDAGraph = torch.xpu.XPUGraph
        torch.cuda.graph_pool_handle = partial(torch.xpu.graph_pool_handle)
        torch.cuda.is_current_stream_capturing = torch.xpu.is_current_stream_capturing
    yield
```


---

### 🔹 Commit #18: `ec8b20fb`
- **完整 Hash**: `ec8b20fbf01e04d33bb059e555a9b5f39fb4cc46`
- **說明 (Ground Truth)**: [Bugfix] Fix Gemma 4 encoder CUDA graph capture OOM at startup (#61365)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/model_executor/models/gemma4_mm.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:160, E:260, A:0) ➔ After(N:161, E:264, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 4, -Edges: 0, ΔFuncs: 4, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `tuple (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Gemma4ForConditionalGeneration.get_encoder_cudagraph_config` ──[CALLS]──> `tuple (External/Unresolved)`
  • + [新增呼叫邊] `Gemma4ForConditionalGeneration.get_encoder_cudagraph_item_specs` ──[CALLS]──> `max (External/Unresolved)`
  • + [新增呼叫邊] `Gemma4ForConditionalGeneration.select_encoder_cudagraph_items` ──[CALLS]──> `getattr (External/Unresolved)`
  • + [新增呼叫邊] `Gemma4ForConditionalGeneration.select_encoder_cudagraph_items` ──[CALLS]──> `max (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Gemma4ForConditionalGeneration.prepare_encoder_cudagraph_capture_inputs()`
- **變更前簽章 (Before)**: `def prepare_encoder_cudagraph_capture_inputs( self, token_budget: int = 256, max_batch_size: int = 4, max_frames_per_batch: int = 1, device: torch.device | str = "cpu", dtype: torch.dtype | None = None, path: str = "default", axis_keys: tuple[Hashable, ...] | None = None, **kwargs: Any, ) -> "EncoderCudaGraphCaptureInputs"` (L1825~L1886)
- **變更後簽章 (After)**: `def prepare_encoder_cudagraph_capture_inputs( self, token_budget: int = 256, max_batch_size: int = 4, max_frames_per_batch: int = 1, device: torch.device | str = "cpu", dtype: torch.dtype | None = None, path: str = "default", axis_keys: tuple[Hashable, ...] | None = None, **kwargs: Any, ) -> "EncoderCudaGraphCaptureInputs"` (L1859~L1921)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def prepare_encoder_cudagraph_capture_inputs(
        self,
        token_budget: int = 256,
        max_batch_size: int = 4,
        max_frames_per_batch: int = 1,
        device: torch.device | str = "cpu",
        dtype: torch.dtype | None = None,
        path: str = "default",
        axis_keys: tuple[Hashable, ...] | None = None,
        **kwargs: Any,
    ) -> "EncoderCudaGraphCaptureInputs":
        from vllm.v1.worker.encoder_cudagraph_defs import (
            EncoderCudaGraphCaptureInputs,
        )

        dtype = dtype or torch.float32

        max_size = max(max_batch_size, max_frames_per_batch)

        vision_cfg = self.vision_tower.config
        pool_ratio = getattr(vision_cfg, "pooling_kernel_size", 2) ** 2

        # Retrieve the model's actual configured maximum tokens:
        configured_max_tokens = getattr(
            self.config.vision_config,
            "num_soft_tokens",
            _SUPPORTED_SOFT_TOKENS[2],
        )
        # Dynamically compute the slot capacity per item bounded by both the
        # current graph budget and the user's maximum config:
        per_item_output = min(token_budget, configured_max_tokens)
        # Satisfy k^2 * per_item_output = per_item_patches
        per_item_patches = per_item_output * pool_ratio

        patch_size = self.vision_tower.config.patch_size
        num_channels = getattr(self.vision_tower.config, "num_channels", 3)
        patch_pixels = (patch_size**2) * num_channels

        dummy_pixel_values = torch.zeros(
            (max_size, per_item_patches, patch_pixels),
            device=device,
            dtype=dtype,
        )
        dummy_pixel_position_ids = torch.full(
            (max_size, per_item_patches, 2),
            -1,
            device=device,
            dtype=torch.long,
        )
        dummy_gather_indices = torch.zeros(
            (token_budget,),
            device=device,
            dtype=torch.long,
        )

        return EncoderCudaGraphCaptureInputs(
            values={
                "pixel_values": dummy_pixel_values,
                "pixel_position_ids": dummy_pixel_position_ids,
                "gather_indices": dummy_gather_indices,
            }
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def prepare_encoder_cudagraph_capture_inputs(
        self,
        token_budget: int = 256,
        max_batch_size: int = 4,
        max_frames_per_batch: int = 1,
        device: torch.device | str = "cpu",
        dtype: torch.dtype | None = None,
        path: str = "default",
        axis_keys: tuple[Hashable, ...] | None = None,
        **kwargs: Any,
    ) -> "EncoderCudaGraphCaptureInputs":
        from vllm.v1.worker.encoder_cudagraph_defs import (
            EncoderCudaGraphCaptureInputs,
        )

        dtype = dtype or torch.float32

        assert axis_keys is not None
        (per_item_output,) = axis_keys
        assert isinstance(per_item_output, int)

        # Every row of a batch replayed on this graph is an image or video
        # frame of per_item_output tokens, so a batch that fits token_budget
        # never needs more rows than this. Capture needs at least one row.
        max_size = min(
            max(max_batch_size, max_frames_per_batch),
            max(1, token_budget // per_item_output),
        )

        vision_cfg = self.vision_tower.config
        pool_ratio = getattr(vision_cfg, "pooling_kernel_size", 2) ** 2

        # Satisfy k^2 * per_item_output = per_item_patches
        per_item_patches = per_item_output * pool_ratio

        patch_size = self.vision_tower.config.patch_size
        num_channels = getattr(self.vision_tower.config, "num_channels", 3)
        patch_pixels = (patch_size**2) * num_channels

        dummy_pixel_values = torch.zeros(
            (max_size, per_item_patches, patch_pixels),
            device=device,
            dtype=dtype,
        )
        dummy_pixel_position_ids = torch.full(
            (max_size, per_item_patches, 2),
            -1,
            device=device,
            dtype=torch.long,
        )
        dummy_gather_indices = torch.zeros(
            (token_budget,),
            device=device,
            dtype=torch.long,
        )

        return EncoderCudaGraphCaptureInputs(
            values={
                "pixel_values": dummy_pixel_values,
                "pixel_position_ids": dummy_pixel_position_ids,
                "gather_indices": dummy_gather_indices,
            }
        )
```

### 🔹 函式: `Gemma4ForConditionalGeneration.get_encoder_cudagraph_item_specs()`
- **變更前簽章 (Before)**: `def get_encoder_cudagraph_item_specs( self, mm_kwargs: dict[str, Any], ) -> list["EncoderItemSpec"]` (L1702~L1746)
- **變更後簽章 (After)**: `def get_encoder_cudagraph_item_specs( self, mm_kwargs: dict[str, Any], ) -> list["EncoderItemSpec"]` (L1710~L1759)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def get_encoder_cudagraph_item_specs(
        self,
        mm_kwargs: dict[str, Any],
    ) -> list["EncoderItemSpec"]:
        from vllm.v1.worker.encoder_cudagraph_defs import EncoderItemSpec

        vision_cfg = self.vision_tower.config
        pool_ratio = getattr(vision_cfg, "pooling_kernel_size", 2) ** 2

        modality = self.get_input_modality(mm_kwargs)
        if modality == "image":
            pixel_values = mm_kwargs["pixel_values"]
            if isinstance(pixel_values, list):
                return [
                    EncoderItemSpec(
                        input_size=pv.shape[0],
                        output_tokens=pv.shape[0] // pool_ratio,
                    )
                    for pv in pixel_values
                ]
            else:
                return [
                    EncoderItemSpec(
                        input_size=pixel_values.shape[1],
                        output_tokens=pixel_values.shape[1] // pool_ratio,
                    )
                    for _ in range(pixel_values.shape[0])
                ]
        elif modality == "video":
            pixel_values_videos = mm_kwargs["pixel_values_videos"]
            video_frame_counts = mm_kwargs["video_frame_counts"]
            fc_list = (
                video_frame_counts.tolist()
                if isinstance(video_frame_counts, torch.Tensor)
                else list(video_frame_counts)
            )
            np_patches = pixel_values_videos.shape[1]
            return [
                EncoderItemSpec(
                    input_size=fc * np_patches,
                    output_tokens=fc * (np_patches // pool_ratio),
                )
                for fc in fc_list
            ]
        raise ValueError(f"Unknown modality: {modality}")
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def get_encoder_cudagraph_item_specs(
        self,
        mm_kwargs: dict[str, Any],
    ) -> list["EncoderItemSpec"]:
        from vllm.v1.worker.encoder_cudagraph_defs import EncoderItemSpec

        vision_cfg = self.vision_tower.config
        pool_ratio = getattr(vision_cfg, "pooling_kernel_size", 2) ** 2

        modality = self.get_input_modality(mm_kwargs)
        if modality == "image":
            pixel_values = mm_kwargs["pixel_values"]
            if isinstance(pixel_values, list):
                # A batch pads its images to the widest one, so pack by that.
                row_tokens = (
                    max((pv.shape[0] for pv in pixel_values), default=0) // pool_ratio
                )
                return [
                    EncoderItemSpec(
                        input_size=pv.shape[0],
                        output_tokens=pv.shape[0] // pool_ratio,
                        path_output_tokens={"default": row_tokens},
                    )
                    for pv in pixel_values
                ]
            else:
                return [
                    EncoderItemSpec(
                        input_size=pixel_values.shape[1],
                        output_tokens=pixel_values.shape[1] // pool_ratio,
                    )
                    for _ in range(pixel_values.shape[0])
                ]
        elif modality == "video":
            pixel_values_videos = mm_kwargs["pixel_values_videos"]
            video_frame_counts = mm_kwargs["video_frame_counts"]
            fc_list = (
                video_frame_counts.tolist()
                if isinstance(video_frame_counts, torch.Tensor)
                else list(video_frame_counts)
            )
            np_patches = pixel_values_videos.shape[1]
            return [
                EncoderItemSpec(
                    input_size=fc * np_patches,
                    output_tokens=fc * (np_patches // pool_ratio),
                )
                for fc in fc_list
            ]
        raise ValueError(f"Unknown modality: {modality}")
```

### 🔹 函式: `Gemma4ForConditionalGeneration.select_encoder_cudagraph_items()`
- **變更前簽章 (Before)**: `def select_encoder_cudagraph_items( self, mm_kwargs: dict[str, Any], indices: list[int], ) -> dict[str, Any]` (L1748~L1823)
- **變更後簽章 (After)**: `def select_encoder_cudagraph_items( self, mm_kwargs: dict[str, Any], indices: list[int], ) -> dict[str, Any]` (L1761~L1857)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def select_encoder_cudagraph_items(
        self,
        mm_kwargs: dict[str, Any],
        indices: list[int],
    ) -> dict[str, Any]:
        modality = self.get_input_modality(mm_kwargs)
        if modality == "image":
            pixel_values = mm_kwargs["pixel_values"]
            pixel_position_ids = mm_kwargs["pixel_position_ids"]
            if len(indices) == 0:
                is_pv_list = isinstance(pixel_values, list)
                is_pp_list = isinstance(pixel_position_ids, list)
                return {
                    "pixel_values": ([] if is_pv_list else pixel_values[:0]),
                    "pixel_position_ids": (
                        [] if is_pp_list else pixel_position_ids[:0]
                    ),
                }
            if isinstance(pixel_values, list):
                return {
                    "pixel_values": [pixel_values[i] for i in indices],
                    "pixel_position_ids": [pixel_position_ids[i] for i in indices],
                }
            return {
                "pixel_values": pixel_values[indices],
                "pixel_position_ids": pixel_position_ids[indices],
            }
        elif modality == "video":
            pixel_values_videos = mm_kwargs["pixel_values_videos"]
            pixel_position_ids_videos = mm_kwargs["pixel_position_ids_videos"]
            video_frame_counts = mm_kwargs["video_frame_counts"]

            if len(indices) == 0:
                is_fc_tensor = isinstance(video_frame_counts, torch.Tensor)
                return {
                    "pixel_values_videos": pixel_values_videos[:0],
                    "pixel_position_ids_videos": pixel_position_ids_videos[:0],
                    "video_frame_counts": (
                        video_frame_counts[:0] if is_fc_tensor else []
                    ),
                }

            fc_list = (
                video_frame_counts.tolist()
                if isinstance(video_frame_counts, torch.Tensor)
                else list(video_frame_counts)
            )
            cum_frames = [0]
            for fc in fc_list:
                cum_frames.append(cum_frames[-1] + fc)

            selected_pv = torch.cat(
                [
                    pixel_values_videos[cum_frames[i] : cum_frames[i + 1]]
                    for i in indices
                ],
                dim=0,
            )
            selected_pp = torch.cat(
                [
                    pixel_position_ids_videos[cum_frames[i] : cum_frames[i + 1]]
                    for i in indices
                ],
                dim=0,
            )
            selected_fc = (
                video_frame_counts[indices]
                if isinstance(video_frame_counts, torch.Tensor)
                else [video_frame_counts[i] for i in indices]
            )
            return {
                "pixel_values_videos": selected_pv,
                "pixel_position_ids_videos": selected_pp,
                "video_frame_counts": selected_fc,
            }
        raise ValueError(f"Unknown modality: {modality}")
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def select_encoder_cudagraph_items(
        self,
        mm_kwargs: dict[str, Any],
        indices: list[int],
    ) -> dict[str, Any]:
        from vllm.v1.worker.encoder_cudagraph_defs import (
            ENCODER_CUDAGRAPH_AXIS_KEYS_KWARG,
        )

        vision_cfg = self.vision_tower.config
        pool_ratio = getattr(vision_cfg, "pooling_kernel_size", 2) ** 2

        modality = self.get_input_modality(mm_kwargs)
        if modality == "image":
            pixel_values = mm_kwargs["pixel_values"]
            pixel_position_ids = mm_kwargs["pixel_position_ids"]
            if isinstance(pixel_values, list):
                row_patches = max(
                    (pixel_values[i].shape[0] for i in indices), default=0
                )
            else:
                row_patches = pixel_values.shape[1]
            axis_keys = (row_patches // pool_ratio,)

            if len(indices) == 0:
                is_pv_list = isinstance(pixel_values, list)
                is_pp_list = isinstance(pixel_position_ids, list)
                return {
                    "pixel_values": ([] if is_pv_list else pixel_values[:0]),
                    "pixel_position_ids": (
                        [] if is_pp_list else pixel_position_ids[:0]
                    ),
                    ENCODER_CUDAGRAPH_AXIS_KEYS_KWARG: axis_keys,
                }
            if isinstance(pixel_values, list):
                return {
                    "pixel_values": [pixel_values[i] for i in indices],
                    "pixel_position_ids": [pixel_position_ids[i] for i in indices],
                    ENCODER_CUDAGRAPH_AXIS_KEYS_KWARG: axis_keys,
                }
            return {
                "pixel_values": pixel_values[indices],
                "pixel_position_ids": pixel_position_ids[indices],
                ENCODER_CUDAGRAPH_AXIS_KEYS_KWARG: axis_keys,
            }
        elif modality == "video":
            pixel_values_videos = mm_kwargs["pixel_values_videos"]
            pixel_position_ids_videos = mm_kwargs["pixel_position_ids_videos"]
            video_frame_counts = mm_kwargs["video_frame_counts"]
            axis_keys = (pixel_values_videos.shape[1] // pool_ratio,)

            if len(indices) == 0:
                is_fc_tensor = isinstance(video_frame_counts, torch.Tensor)
                return {
                    "pixel_values_videos": pixel_values_videos[:0],
                    "pixel_position_ids_videos": pixel_position_ids_videos[:0],
                    "video_frame_counts": (
                        video_frame_counts[:0] if is_fc_tensor else []
                    ),
                    ENCODER_CUDAGRAPH_AXIS_KEYS_KWARG: axis_keys,
                }

            fc_list = (
                video_frame_counts.tolist()
                if isinstance(video_frame_counts, torch.Tensor)
                else list(video_frame_counts)
            )
            cum_frames = [0]
            for fc in fc_list:
                cum_frames.append(cum_frames[-1] + fc)

            selected_pv = torch.cat(
                [
                    pixel_values_videos[cum_frames[i] : cum_frames[i + 1]]
                    for i in indices
                ],
                dim=0,
            )
            selected_pp = torch.cat(
                [
                    pixel_position_ids_videos[cum_frames[i] : cum_frames[i + 1]]
                    for i in indices
                ],
                dim=0,
            )
            selected_fc = (
                video_frame_counts[indices]
                if isinstance(video_frame_counts, torch.Tensor)
                else [video_frame_counts[i] for i in indices]
            )
            return {
                "pixel_values_videos": selected_pv,
                "pixel_position_ids_videos": selected_pp,
                "video_frame_counts": selected_fc,
                ENCODER_CUDAGRAPH_AXIS_KEYS_KWARG: axis_keys,
            }
        raise ValueError(f"Unknown modality: {modality}")
```

### 🔹 函式: `Gemma4ForConditionalGeneration.get_encoder_cudagraph_config()`
- **變更前簽章 (Before)**: `def get_encoder_cudagraph_config(self) -> "EncoderCudaGraphConfig"` (L1653~L1679)
- **變更後簽章 (After)**: `def get_encoder_cudagraph_config(self) -> "EncoderCudaGraphConfig"` (L1653~L1687)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def get_encoder_cudagraph_config(self) -> "EncoderCudaGraphConfig":
        from vllm.v1.worker.encoder_cudagraph_defs import EncoderCudaGraphConfig

        def pad_pixel_values(dst: torch.Tensor, src: torch.Tensor) -> None:
            dst.zero_()
            batch_size, num_patches = src.shape[0], src.shape[1]
            dst[:batch_size, :num_patches].copy_(src)

        def pad_pixel_position_ids(dst: torch.Tensor, src: torch.Tensor) -> None:
            dst.fill_(-1)
            batch_size, num_patches = src.shape[0], src.shape[1]
            dst[:batch_size, :num_patches].copy_(src)

        return EncoderCudaGraphConfig(
            modalities=["image", "video"],
            buffer_keys=[
                "pixel_values",
                "pixel_position_ids",
                "gather_indices",
            ],
            out_hidden_size=self.config.text_config.hidden_size,
            max_frames_per_video=_VIDEO_MAX_FRAMES,
            padding_logics={
                "pixel_values": pad_pixel_values,
                "pixel_position_ids": pad_pixel_position_ids,
            },
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def get_encoder_cudagraph_config(self) -> "EncoderCudaGraphConfig":
        from vllm.v1.worker.encoder_cudagraph_defs import EncoderCudaGraphConfig

        def pad_pixel_values(dst: torch.Tensor, src: torch.Tensor) -> None:
            dst.zero_()
            batch_size, num_patches = src.shape[0], src.shape[1]
            dst[:batch_size, :num_patches].copy_(src)

        def pad_pixel_position_ids(dst: torch.Tensor, src: torch.Tensor) -> None:
            dst.fill_(-1)
            batch_size, num_patches = src.shape[0], src.shape[1]
            dst[:batch_size, :num_patches].copy_(src)

        configured_max_tokens = self.config.vision_config.default_output_length
        # One graph per row width (soft tokens of one image or video frame),
        # so a budget's rows are not all padded to the widest image.
        row_widths = tuple(
            t for t in _SUPPORTED_SOFT_TOKENS if t <= configured_max_tokens
        )

        return EncoderCudaGraphConfig(
            modalities=["image", "video"],
            buffer_keys=[
                "pixel_values",
                "pixel_position_ids",
                "gather_indices",
            ],
            out_hidden_size=self.config.text_config.hidden_size,
            max_frames_per_video=_VIDEO_MAX_FRAMES,
            padding_logics={
                "pixel_values": pad_pixel_values,
                "pixel_position_ids": pad_pixel_position_ids,
            },
            capture_axes=(row_widths,),
        )
```


---

### 🔹 Commit #19: `026f6ab2`
- **完整 Hash**: `026f6ab2689397e64c1f53a5ac57d37c4dc46b67`
- **說明 (Ground Truth)**: [Model] DeepSeek-V4/V4.1 VL: stream language-model weights instead of sorting the checkpoint (#58857)
- **變更檔案數**: 2

#### 📄 檔案: `vllm/models/deepseek_v4/common/vl_model.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:51, E:51, A:0) ➔ After(N:51, E:51, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 2, +Edges: 2, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `stream_language_model_first` (FUNCTION_DEF)
  • + [新增節點] `clone (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `iter (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `sorted (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `stream_language_model_first` ──[CALLS]──> `clone (External/Unresolved)`
  • + [新增呼叫邊] `DeepseekV4ForConditionalGeneration.load_weights` ──[CALLS]──> `stream_language_model_first`
  • - [移除呼叫邊] `DeepseekV4ForConditionalGeneration.load_weights` ──[CALLS]──> `iter (External/Unresolved)`
  • - [移除呼叫邊] `DeepseekV4ForConditionalGeneration.load_weights` ──[CALLS]──> `sorted (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `DeepseekV4ForConditionalGeneration.load_weights()`
- **變更前簽章 (Before)**: `def load_weights(self, weights: Iterable[tuple[str, torch.Tensor]]) -> set[str]` (L329~L341)
- **變更後簽章 (After)**: `def load_weights(self, weights: Iterable[tuple[str, torch.Tensor]]) -> set[str]` (L347~L359)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def load_weights(self, weights: Iterable[tuple[str, torch.Tensor]]) -> set[str]:
        child_finalizes = getattr(
            self.language_model, "finalizes_weights_during_load", True
        )
        mapped = self.hf_to_vllm_mapper.apply(weights)
        if child_finalizes:
            # A child which finalizes inside load_weights must see all of its
            # weights in one contiguous delegation from AutoWeightsLoader.
            mapped = iter(sorted(mapped, key=lambda x: x[0]))
        loader = AutoWeightsLoader(self)
        loaded_params = loader.load_weights(mapped)
        self._weights_finalized = child_finalizes
        return loaded_params
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def load_weights(self, weights: Iterable[tuple[str, torch.Tensor]]) -> set[str]:
        child_finalizes = getattr(
            self.language_model, "finalizes_weights_during_load", True
        )
        mapped = self.hf_to_vllm_mapper.apply(weights)
        if child_finalizes:
            # A child which finalizes inside load_weights must see all of its
            # weights in one contiguous delegation from AutoWeightsLoader.
            mapped = stream_language_model_first(mapped)
        loader = AutoWeightsLoader(self)
        loaded_params = loader.load_weights(mapped)
        self._weights_finalized = child_finalizes
        return loaded_params
```


#### 📄 檔案: `vllm/models/deepseek_v41/nvidia/vl_model.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:47, E:42, A:0) ➔ After(N:47, E:42, A:0)
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
  • + [新增節點] `stream_language_model_first (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `sorted (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `DeepseekV41ForCausalLM.load_weights` ──[CALLS]──> `stream_language_model_first (External/Unresolved)`
  • - [移除呼叫邊] `DeepseekV41ForCausalLM.load_weights` ──[CALLS]──> `sorted (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `DeepseekV41ForCausalLM.load_weights()`
- **變更前簽章 (Before)**: `def load_weights(self, weights: Iterable[tuple[str, torch.Tensor]]) -> set[str]: # Map HF names into this wrapper's namespace up front and sort, so # the "language_model." group reaches the child loader as one # contiguous block (AutoWeightsLoader delegates per contiguous group, # and the child's load_weights finalizes fused expert weights, which # must not run on a partially loaded model).` (L319~L330)
- **變更後簽章 (After)**: `def load_weights(self, weights: Iterable[tuple[str, torch.Tensor]]) -> set[str]: # The child finalizes in load_weights, so its weights must reach it as # one contiguous group.` (L320~L328)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def load_weights(self, weights: Iterable[tuple[str, torch.Tensor]]) -> set[str]:
        # Map HF names into this wrapper's namespace up front and sort, so
        # the "language_model." group reaches the child loader as one
        # contiguous block (AutoWeightsLoader delegates per contiguous group,
        # and the child's load_weights finalizes fused expert weights, which
        # must not run on a partially loaded model).
        mapped = sorted(self.hf_to_vllm_mapper.apply(weights), key=lambda x: x[0])
        loader = AutoWeightsLoader(self)
        loaded_params = loader.load_weights(mapped)
        # The child's load_weights already ran its post-load finalization.
        self._weights_finalized = True
        return loaded_params
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def load_weights(self, weights: Iterable[tuple[str, torch.Tensor]]) -> set[str]:
        # The child finalizes in load_weights, so its weights must reach it as
        # one contiguous group.
        mapped = stream_language_model_first(self.hf_to_vllm_mapper.apply(weights))
        loader = AutoWeightsLoader(self)
        loaded_params = loader.load_weights(mapped)
        # The child's load_weights already ran its post-load finalization.
        self._weights_finalized = True
        return loaded_params
```


---

### 🔹 Commit #20: `61bb5908`
- **完整 Hash**: `61bb590877521e2f4516912297a40f593e222ee9`
- **說明 (Ground Truth)**: [Bugfix][Spec Decode] Clear stale shared block-table rows (#61174)
- **變更檔案數**: 1

#### 📄 檔案: `vllm/v1/worker/gpu/block_table.py`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:36, E:37, A:0) ➔ After(N:37, E:39, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `max (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `BlockTables.gather_block_tables` ──[CALLS]──> `max (External/Unresolved)`
  • + [新增呼叫邊] `BlockTables.get_dummy_block_tables` ──[CALLS]──> `max (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `BlockTables.gather_block_tables()`
- **變更前簽章 (Before)**: `def gather_block_tables( self, idx_mapping: torch.Tensor, num_reqs_padded: int, out: tuple[torch.Tensor, ...] | None = None, out_ptrs: torch.Tensor | None = None, ) -> tuple[torch.Tensor, ...]` (L145~L172)
- **變更後簽章 (After)**: `def gather_block_tables( self, idx_mapping: torch.Tensor, num_reqs_padded: int, out: tuple[torch.Tensor, ...] | None = None, out_ptrs: torch.Tensor | None = None, ) -> tuple[torch.Tensor, ...]` (L146~L176)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def gather_block_tables(
        self,
        idx_mapping: torch.Tensor,
        num_reqs_padded: int,
        out: tuple[torch.Tensor, ...] | None = None,
        out_ptrs: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, ...]:
        if self.num_kv_cache_groups == 0:
            return ()
        if out is None:
            out = tuple(self.input_block_tables)
            out_ptrs = self.input_block_table_ptrs
        else:
            assert out_ptrs is not None
            assert len(out) == self.num_kv_cache_groups
        num_reqs = idx_mapping.shape[0]
        # Launch kernel with num_reqs_padded to fuse zeroing of padded rows.
        _gather_block_tables_kernel[(self.num_kv_cache_groups, num_reqs_padded)](
            idx_mapping,
            self.block_table_ptrs,
            out_ptrs,
            self.block_table_strides,
            self.num_blocks.gpu,
            self.num_blocks.gpu.stride(0),
            num_reqs,
            BLOCK_SIZE=1024,  # type: ignore
        )
        return tuple(bt[:num_reqs_padded] for bt in out)
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def gather_block_tables(
        self,
        idx_mapping: torch.Tensor,
        num_reqs_padded: int,
        out: tuple[torch.Tensor, ...] | None = None,
        out_ptrs: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, ...]:
        if self.num_kv_cache_groups == 0:
            return ()
        num_reqs = idx_mapping.shape[0]
        num_rows = num_reqs_padded
        if out is None:
            out = tuple(self.input_block_tables)
            out_ptrs = self.input_block_table_ptrs
            num_rows = max(num_rows, self._num_dirty_rows)
            self._num_dirty_rows = num_reqs
        else:
            assert out_ptrs is not None
            assert len(out) == self.num_kv_cache_groups
        # Also clear rows left by a larger batch in the shared buffer.
        _gather_block_tables_kernel[(self.num_kv_cache_groups, num_rows)](
            idx_mapping,
            self.block_table_ptrs,
            out_ptrs,
            self.block_table_strides,
            self.num_blocks.gpu,
            self.num_blocks.gpu.stride(0),
            num_reqs,
            BLOCK_SIZE=1024,  # type: ignore
        )
        return tuple(bt[:num_reqs_padded] for bt in out)
```

### 🔹 函式: `BlockTables.get_dummy_block_tables()`
- **變更前簽章 (Before)**: `def get_dummy_block_tables(self, num_reqs: int) -> tuple[torch.Tensor, ...]: # NOTE(woosuk): The output may be used for CUDA graph capture. # Therefore, this method must return the persistent tensor # with the same memory address as that used during the model's forward pass, # rather than allocating a new tensor. # # Zero the rows so dummy runs write mamba state to the reserved null # block rather than through the previous real step's (stale) block # ids, which may point at blocks since freed and reallocated.` (L174~L185)
- **變更後簽章 (After)**: `def get_dummy_block_tables(self, num_reqs: int) -> tuple[torch.Tensor, ...]: # NOTE(woosuk): The output may be used for CUDA graph capture. # Therefore, this method must return the persistent tensor # with the same memory address as that used during the model's forward pass, # rather than allocating a new tensor. # # Zero the rows so dummy runs write mamba state to the reserved null # block rather than through the previous real step's (stale) block # ids, which may point at blocks since freed and reallocated.` (L178~L192)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def get_dummy_block_tables(self, num_reqs: int) -> tuple[torch.Tensor, ...]:
        # NOTE(woosuk): The output may be used for CUDA graph capture.
        # Therefore, this method must return the persistent tensor
        # with the same memory address as that used during the model's forward pass,
        # rather than allocating a new tensor.
        #
        # Zero the rows so dummy runs write mamba state to the reserved null
        # block rather than through the previous real step's (stale) block
        # ids, which may point at blocks since freed and reallocated.
        return tuple(
            block_table[:num_reqs].zero_() for block_table in self.input_block_tables
        )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def get_dummy_block_tables(self, num_reqs: int) -> tuple[torch.Tensor, ...]:
        # NOTE(woosuk): The output may be used for CUDA graph capture.
        # Therefore, this method must return the persistent tensor
        # with the same memory address as that used during the model's forward pass,
        # rather than allocating a new tensor.
        #
        # Zero the rows so dummy runs write mamba state to the reserved null
        # block rather than through the previous real step's (stale) block
        # ids, which may point at blocks since freed and reallocated.
        num_rows = max(num_reqs, self._num_dirty_rows)
        for block_table in self.input_block_tables:
            block_table[:num_rows].zero_()
        # Profiling may populate the returned rows with valid block IDs.
        self._num_dirty_rows = num_reqs
        return tuple(block_table[:num_reqs] for block_table in self.input_block_tables)
```

### 🔹 函式: `BlockTables.__init__()`
- **變更前簽章 (Before)**: `def __init__( self, block_sizes: list[int], max_num_reqs: int, max_num_batched_tokens: int, max_num_blocks_per_group: list[int], device: torch.device, cp_size: int = 1, cp_rank: int = 0, cp_interleave: int = 1, slot_mapping_enabled: list[bool] | None = None, dcp_sharded: list[bool] | None = None, )` (L21~L85)
- **變更後簽章 (After)**: `def __init__( self, block_sizes: list[int], max_num_reqs: int, max_num_batched_tokens: int, max_num_blocks_per_group: list[int], device: torch.device, cp_size: int = 1, cp_rank: int = 0, cp_interleave: int = 1, slot_mapping_enabled: list[bool] | None = None, dcp_sharded: list[bool] | None = None, )` (L21~L86)

#### ◀️ 變更前實作碼 (Before Implementation):
```
def __init__(
        self,
        block_sizes: list[int],
        max_num_reqs: int,
        max_num_batched_tokens: int,
        max_num_blocks_per_group: list[int],
        device: torch.device,
        cp_size: int = 1,
        cp_rank: int = 0,
        cp_interleave: int = 1,
        slot_mapping_enabled: list[bool] | None = None,
        dcp_sharded: list[bool] | None = None,
    ):
        self.block_sizes = block_sizes
        self.max_num_reqs = max_num_reqs
        self.max_num_batched_tokens = max_num_batched_tokens
        self.device = device

        self.cp_size = cp_size
        self.cp_rank = cp_rank
        self.cp_interleave = cp_interleave

        self.num_kv_cache_groups = len(self.block_sizes)
        assert len(max_num_blocks_per_group) == self.num_kv_cache_groups
        if slot_mapping_enabled is None:
            slot_mapping_enabled = [True] * self.num_kv_cache_groups
        assert len(slot_mapping_enabled) == self.num_kv_cache_groups
        self._slot_mapping_enabled = slot_mapping_enabled
        if dcp_sharded is None:
            dcp_sharded = [True] * self.num_kv_cache_groups
        assert len(dcp_sharded) == self.num_kv_cache_groups
        self.dcp_sharded = torch.tensor(dcp_sharded, dtype=torch.bool, device=device)

        # num_kv_cache_groups x [max_num_reqs, max_num_blocks]
        self.block_tables: list[StagedWriteTensor] = []
        for max_num_blocks in max_num_blocks_per_group:
            block_table = StagedWriteTensor(
                (self.max_num_reqs, max_num_blocks), dtype=torch.int32, device=device
            )
            self.block_tables.append(block_table)

        self.num_blocks = UvaBackedTensor(
            (self.num_kv_cache_groups, self.max_num_reqs), dtype=torch.int32
        )
        self.fused_writer: FusedStagedWriter | None = None
        if self.num_kv_cache_groups > 1:
            # Only the multi-group path uses the fused writer.
            self.fused_writer = FusedStagedWriter(
                self.device, self.num_kv_cache_groups * self.max_num_reqs
            )

        # Block tables used for model's forward pass.
        # num_kv_cache_groups x [max_num_reqs, max_num_blocks]
        self.input_block_tables: list[torch.Tensor] = [
            torch.zeros_like(b.gpu) for b in self.block_tables
        ]

        self.slot_mappings = torch.zeros(
            self.num_kv_cache_groups,
            self.max_num_batched_tokens,
            dtype=torch.int64,
            device=self.device,
        )

        self.init_block_table_layout_tensors()
```

#### ▶️ 變更後實作碼 (After Implementation):
```
def __init__(
        self,
        block_sizes: list[int],
        max_num_reqs: int,
        max_num_batched_tokens: int,
        max_num_blocks_per_group: list[int],
        device: torch.device,
        cp_size: int = 1,
        cp_rank: int = 0,
        cp_interleave: int = 1,
        slot_mapping_enabled: list[bool] | None = None,
        dcp_sharded: list[bool] | None = None,
    ):
        self.block_sizes = block_sizes
        self.max_num_reqs = max_num_reqs
        self.max_num_batched_tokens = max_num_batched_tokens
        self.device = device

        self.cp_size = cp_size
        self.cp_rank = cp_rank
        self.cp_interleave = cp_interleave

        self.num_kv_cache_groups = len(self.block_sizes)
        assert len(max_num_blocks_per_group) == self.num_kv_cache_groups
        if slot_mapping_enabled is None:
            slot_mapping_enabled = [True] * self.num_kv_cache_groups
        assert len(slot_mapping_enabled) == self.num_kv_cache_groups
        self._slot_mapping_enabled = slot_mapping_enabled
        if dcp_sharded is None:
            dcp_sharded = [True] * self.num_kv_cache_groups
        assert len(dcp_sharded) == self.num_kv_cache_groups
        self.dcp_sharded = torch.tensor(dcp_sharded, dtype=torch.bool, device=device)

        # num_kv_cache_groups x [max_num_reqs, max_num_blocks]
        self.block_tables: list[StagedWriteTensor] = []
        for max_num_blocks in max_num_blocks_per_group:
            block_table = StagedWriteTensor(
                (self.max_num_reqs, max_num_blocks), dtype=torch.int32, device=device
            )
            self.block_tables.append(block_table)

        self.num_blocks = UvaBackedTensor(
            (self.num_kv_cache_groups, self.max_num_reqs), dtype=torch.int32
        )
        self.fused_writer: FusedStagedWriter | None = None
        if self.num_kv_cache_groups > 1:
            # Only the multi-group path uses the fused writer.
            self.fused_writer = FusedStagedWriter(
                self.device, self.num_kv_cache_groups * self.max_num_reqs
            )

        # Block tables used for model's forward pass.
        # num_kv_cache_groups x [max_num_reqs, max_num_blocks]
        self.input_block_tables: list[torch.Tensor] = [
            torch.zeros_like(b.gpu) for b in self.block_tables
        ]
        self._num_dirty_rows = 0

        self.slot_mappings = torch.zeros(
            self.num_kv_cache_groups,
            self.max_num_batched_tokens,
            dtype=torch.int64,
            device=self.device,
        )

        self.init_block_table_layout_tensors()
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/vllm show 34ac4f96a399836393894207dae296760b413715
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 34ac4f96a399836393894207dae296760b413715~1 --file test_repos/vllm/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/mooncake_connector.py
   ```
