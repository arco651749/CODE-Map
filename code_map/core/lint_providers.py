"""
Multi-backend Gatekeeper (Decision API) & Explainer (LLM) providers for CODE-Map.
Zero external HTTP dependencies (uses Python stdlib urllib & subprocess).
"""
from dataclasses import dataclass, field
import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import time
from typing import Any, Dict, List, Optional
import urllib.error
import urllib.request


class LintProviderError(RuntimeError):
    """Raised when an external Decision API or Explainer LLM call fails (caught by Fail-Open handler)."""


@dataclass
class DecisionVerdict:
    """Normalized decision result for a single lint rule."""
    rule_id: str
    title: str
    domain: str
    severity: str
    question_type: str
    score: float
    confidence: float
    selected_choice: Optional[str] = None
    status: str = "PASS"  # PASS | WARN | BLOCK
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExplainerFinding:
    """Normalized explanation produced by the Explainer LLM for a triggered rule."""
    rule_id: str
    evidence_lines: str
    reasoning: str
    suggested_fix: str
    raw_text: str = ""


def resolve_secret(env_or_literal: str, override: Optional[str] = None) -> str:
    """Resolve an API key from override, `$ENV_VAR` reference, or literal string."""
    if override:
        return override.strip()
    raw = (env_or_literal or "").strip()
    if not raw:
        return ""
    if raw.startswith("$"):
        var_name = raw.lstrip("$").strip("{}")
        return os.environ.get(var_name, "").strip()
    return raw


def _http_post_json(
    url: str,
    payload: Dict[str, Any],
    headers: Dict[str, str],
    timeout_seconds: int,
) -> Dict[str, Any]:
    """Send a JSON POST request and return parsed JSON response."""
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise LintProviderError(f"HTTP {exc.code} from {url}: {err_body[:300]}") from exc
    except urllib.error.URLError as exc:
        raise LintProviderError(f"Network error calling {url}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise LintProviderError(f"Request timed out after {timeout_seconds}s: {url}") from exc
    except json.JSONDecodeError as exc:
        raise LintProviderError(f"Invalid JSON response from {url}: {exc}") from exc


def _extract_json_block(text: str) -> Optional[Any]:
    """Extract first valid JSON object/array from raw LLM output (handles markdown fences)."""
    cleaned = text.strip()
    if not cleaned:
        return None
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned, re.IGNORECASE)
    if fence_match:
        cleaned = fence_match.group(1).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    obj_match = re.search(r"(\{[\s\S]*\})", cleaned)
    if obj_match:
        try:
            return json.loads(obj_match.group(1))
        except json.JSONDecodeError:
            return None
    return None


def _extract_by_path(data: Any, path: str) -> Any:
    """Extract a value using a simple dot/bracket path like `results.0.score` or `$.a.b`."""
    if not path:
        return None
    cur = data
    cleaned = path.lstrip("$").lstrip(".")
    for part in re.split(r"\.|\[|\]", cleaned):
        if not part:
            continue
        if isinstance(cur, list) and part.isdigit():
            idx = int(part)
            cur = cur[idx] if 0 <= idx < len(cur) else None
        elif isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur


def _classify_verdict(
    rule: Dict[str, Any],
    default_warn: float,
    default_block: float,
    score: float,
    confidence: float,
    selected_choice: Optional[str] = None,
) -> str:
    """Map numeric probability or selected choice onto PASS / WARN / BLOCK."""
    thresholds = rule.get("Thresholds", {})
    q_type = rule.get("Decision", {}).get("Type", "noul").lower()

    if q_type == "choice":
        min_conf = float(thresholds.get("MinChoiceConfidence", 0.70))
        if confidence < min_conf or not selected_choice:
            return "PASS"
        if selected_choice in thresholds.get("BlockChoices", []):
            return "BLOCK"
        if selected_choice in thresholds.get("WarnChoices", []):
            return "WARN"
        return "PASS"

    warn_t = float(thresholds.get("Warn", default_warn))
    block_t = float(thresholds.get("Block", default_block))
    if score >= block_t:
        return "BLOCK"
    if score >= warn_t:
        return "WARN"
    return "PASS"


# ============================================================================
# Gatekeeper (Decision API) Providers
# ============================================================================


class BaseDecisionProvider:
    """Abstract interface for multi-rule batch decision evaluation."""

    provider_name: str = "BaseDecision"

    def evaluate(
        self, code_context: str, rules: List[Dict[str, Any]]
    ) -> tuple[Dict[str, DecisionVerdict], float]:
        raise NotImplementedError


class GeminiDecisionProvider(BaseDecisionProvider):
    """Google Gemini Decision 1 (`POST /v1beta/decisions`) provider."""

    provider_name = "GeminiDecision"

    def __init__(self, cfg: Dict[str, Any], api_key_override: Optional[str] = None):
        self.endpoint = cfg.get(
            "Endpoint", "https://generativelanguage.googleapis.com/v1beta/decisions"
        )
        self.model = cfg.get("Model", "gemini-decision-1")
        self.api_key = resolve_secret(cfg.get("ApiKeyEnv", "$GOOGLE_API_KEY"), api_key_override)
        self.timeout = int(cfg.get("TimeoutSeconds", 15))
        self.default_warn = float(cfg.get("DefaultWarnThreshold", 0.65))
        self.default_block = float(cfg.get("DefaultBlockThreshold", 0.85))

    def evaluate(
        self, code_context: str, rules: List[Dict[str, Any]]
    ) -> tuple[Dict[str, DecisionVerdict], float]:
        if not self.api_key:
            raise LintProviderError("Missing API key for GeminiDecision (check $GOOGLE_API_KEY or --api-key).")

        questions: Dict[str, Any] = {}
        rule_map: Dict[str, Dict[str, Any]] = {}
        for r in rules:
            rid = r["Id"]
            rule_map[rid] = r
            dec = r.get("Decision", {})
            q_type = dec.get("Type", "noul").lower()
            q_obj: Dict[str, Any] = {
                "type": q_type,
                "instructions": dec.get("Instructions", r.get("Title", "")),
            }
            if q_type == "choice" and dec.get("Criteria"):
                q_obj["criteria"] = dec["Criteria"]
            elif q_type == "score" and dec.get("Levels"):
                q_obj["levels"] = dec["Levels"]
            questions[rid] = q_obj

        payload = {
            "model": self.model,
            "input": code_context,
            "questions": questions,
        }
        t0 = time.perf_counter()
        data = _http_post_json(
            self.endpoint,
            payload,
            headers={"x-goog-api-key": self.api_key},
            timeout_seconds=self.timeout,
        )
        latency_ms = (time.perf_counter() - t0) * 1000.0

        answers = data.get("answers", {})
        verdicts: Dict[str, DecisionVerdict] = {}
        for rid, r in rule_map.items():
            ans = answers.get(rid, {})
            q_type = ans.get("type", r.get("Decision", {}).get("Type", "noul")).lower()
            confidence = float(ans.get("confidence", 0.0))
            selected_choice = ans.get("selected_option") or ans.get("choice")

            if q_type == "noul":
                score = float(ans.get("noul", 0.0))
            elif q_type == "score":
                score = float(ans.get("expected_score", ans.get("score", 0.0)))
            else:
                # For choice, compute score of top triggered bad choice if available
                probs = ans.get("probabilities", {})
                if selected_choice and isinstance(probs, dict) and selected_choice in probs:
                    score = float(probs[selected_choice])
                else:
                    score = confidence

            status = _classify_verdict(
                r, self.default_warn, self.default_block, score, confidence, selected_choice
            )
            verdicts[rid] = DecisionVerdict(
                rule_id=rid,
                title=r.get("Title", rid),
                domain=r.get("Domain", "GLOBAL"),
                severity=r.get("Severity", "WARN"),
                question_type=q_type,
                score=score,
                confidence=confidence,
                selected_choice=selected_choice,
                status=status,
                raw=ans,
            )
        return verdicts, latency_ms


class OpenAiDecisionProvider(BaseDecisionProvider):
    """Structured-JSON Decision adapter for OpenAI-compatible chat endpoints."""

    provider_name = "OpenAiCompatible"

    def __init__(self, cfg: Dict[str, Any], api_key_override: Optional[str] = None):
        self.endpoint = cfg.get("Endpoint", "https://api.openai.com/v1/chat/completions")
        self.model = cfg.get("Model", "gpt-4o-mini")
        self.api_key = resolve_secret(cfg.get("ApiKeyEnv", "$OPENAI_API_KEY"), api_key_override)
        self.timeout = int(cfg.get("TimeoutSeconds", 25))
        self.default_warn = float(cfg.get("DefaultWarnThreshold", 0.65))
        self.default_block = float(cfg.get("DefaultBlockThreshold", 0.85))

    def evaluate(
        self, code_context: str, rules: List[Dict[str, Any]]
    ) -> tuple[Dict[str, DecisionVerdict], float]:
        if not self.api_key and "localhost" not in self.endpoint and "127.0.0.1" not in self.endpoint:
            raise LintProviderError("Missing API key for OpenAiCompatible Gatekeeper.")

        rules_spec = []
        for r in rules:
            dec = r.get("Decision", {})
            item = {
                "rule_id": r["Id"],
                "type": dec.get("Type", "noul"),
                "instructions": dec.get("Instructions", ""),
            }
            if dec.get("Criteria"):
                item["criteria"] = dec["Criteria"]
            rules_spec.append(item)

        prompt = (
            "Evaluate the following code against each rule strictly. "
            "Return ONLY valid JSON: {\"answers\": {\"<rule_id>\": "
            "{\"score\": <float 0.0-1.0 violation probability>, \"confidence\": <float 0.0-1.0>, "
            "\"selected_option\": <string or null>}}}.\n\n"
            f"Rules:\n{json.dumps(rules_spec, ensure_ascii=False, indent=2)}\n\n"
            f"Code Context:\n{code_context}"
        )
        payload = {
            "model": self.model,
            "temperature": 0.0,
            "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        t0 = time.perf_counter()
        data = _http_post_json(self.endpoint, payload, headers=headers, timeout_seconds=self.timeout)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        content = (
            data.get("choices", [{}])[0].get("message", {}).get("content", "")
        )
        parsed = _extract_json_block(content)
        if not isinstance(parsed, dict) or "answers" not in parsed:
            raise LintProviderError("OpenAiCompatible Gatekeeper did not return valid JSON answers.")

        answers = parsed["answers"]
        verdicts: Dict[str, DecisionVerdict] = {}
        for r in rules:
            rid = r["Id"]
            ans = answers.get(rid, {})
            q_type = r.get("Decision", {}).get("Type", "noul").lower()
            score = float(ans.get("score", 0.0))
            confidence = float(ans.get("confidence", score))
            selected_choice = ans.get("selected_option")
            status = _classify_verdict(
                r, self.default_warn, self.default_block, score, confidence, selected_choice
            )
            verdicts[rid] = DecisionVerdict(
                rule_id=rid,
                title=r.get("Title", rid),
                domain=r.get("Domain", "GLOBAL"),
                severity=r.get("Severity", "WARN"),
                question_type=q_type,
                score=score,
                confidence=confidence,
                selected_choice=selected_choice,
                status=status,
                raw=ans,
            )
        return verdicts, latency_ms


class HttpTemplateDecisionProvider(BaseDecisionProvider):
    """Generic customizable REST adapter (for JEV or custom internal Decision APIs)."""

    provider_name = "HttpTemplate"

    def __init__(self, cfg: Dict[str, Any], api_key_override: Optional[str] = None):
        self.endpoint = cfg.get("Endpoint", "")
        self.model = cfg.get("Model", "")
        self.api_key = resolve_secret(cfg.get("ApiKeyEnv", ""), api_key_override)
        self.headers_cfg = cfg.get("Headers", {})
        self.payload_template = cfg.get("PayloadTemplate", {"model": "{model}", "input": "{input}", "questions": "{questions}"})
        self.response_map = cfg.get("ResponseMapping", {"answers_path": "answers", "score_field": "score", "choice_field": "choice"})
        self.timeout = int(cfg.get("TimeoutSeconds", 15))
        self.default_warn = float(cfg.get("DefaultWarnThreshold", 0.65))
        self.default_block = float(cfg.get("DefaultBlockThreshold", 0.85))

    def evaluate(
        self, code_context: str, rules: List[Dict[str, Any]]
    ) -> tuple[Dict[str, DecisionVerdict], float]:
        if not self.endpoint:
            raise LintProviderError("HttpTemplate Gatekeeper requires `Endpoint` in config.")

        headers: Dict[str, str] = {}
        for k, v in self.headers_cfg.items():
            headers[k] = str(v).replace("{api_key}", self.api_key)
            if "$" in headers[k]:
                headers[k] = re.sub(r"\$\{?([A-Za-z0-9_]+)\}?", lambda m: os.environ.get(m.group(1), ""), headers[k])

        questions_obj = {
            r["Id"]: {
                "type": r.get("Decision", {}).get("Type", "noul"),
                "instructions": r.get("Decision", {}).get("Instructions", ""),
                **({"criteria": r["Decision"]["Criteria"]} if r.get("Decision", {}).get("Criteria") else {}),
            }
            for r in rules
        }

        def _render(obj: Any) -> Any:
            if isinstance(obj, str):
                if obj == "{questions}":
                    return questions_obj
                return obj.replace("{input}", code_context).replace("{model}", self.model)
            if isinstance(obj, dict):
                return {k: _render(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_render(x) for x in obj]
            return obj

        payload = _render(self.payload_template)
        t0 = time.perf_counter()
        data = _http_post_json(self.endpoint, payload, headers=headers, timeout_seconds=self.timeout)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        answers = _extract_by_path(data, self.response_map.get("answers_path", "answers")) or {}
        score_field = self.response_map.get("score_field", "score")
        conf_field = self.response_map.get("confidence_field", "confidence")
        choice_field = self.response_map.get("choice_field", "selected_option")

        verdicts: Dict[str, DecisionVerdict] = {}
        for r in rules:
            rid = r["Id"]
            ans = answers.get(rid, {}) if isinstance(answers, dict) else {}
            q_type = r.get("Decision", {}).get("Type", "noul").lower()
            score = float(ans.get(score_field, ans.get("noul", 0.0)))
            confidence = float(ans.get(conf_field, score))
            selected_choice = ans.get(choice_field)
            status = _classify_verdict(
                r, self.default_warn, self.default_block, score, confidence, selected_choice
            )
            verdicts[rid] = DecisionVerdict(
                rule_id=rid,
                title=r.get("Title", rid),
                domain=r.get("Domain", "GLOBAL"),
                severity=r.get("Severity", "WARN"),
                question_type=q_type,
                score=score,
                confidence=confidence,
                selected_choice=selected_choice,
                status=status,
                raw=ans,
            )
        return verdicts, latency_ms


# ============================================================================
# Explainer (Generative LLM) Providers
# ============================================================================


class BaseExplainerProvider:
    """Abstract interface for generating human/agent-readable line diagnostics."""

    provider_name: str = "BaseExplainer"

    def explain(
        self, code_context: str, triggered_verdicts: List[DecisionVerdict], rules_by_id: Dict[str, Dict[str, Any]]
    ) -> tuple[Dict[str, ExplainerFinding], float]:
        raise NotImplementedError

    @staticmethod
    def build_prompt(
        code_context: str, triggered_verdicts: List[DecisionVerdict], rules_by_id: Dict[str, Dict[str, Any]]
    ) -> str:
        rules_desc = []
        for v in triggered_verdicts:
            r = rules_by_id.get(v.rule_id, {})
            rules_desc.append(
                f"- {v.rule_id} ({v.title}) [Decision={v.status}, score={v.score:.3f}"
                + (f", choice={v.selected_choice}" if v.selected_choice else "")
                + f"]: {r.get('Decision', {}).get('Instructions', '')}"
            )
        return (
            "你是一個嚴謹的程式碼安全與品質審查官。前置 Decision 模型已標記以下規則可能違規。\n"
            "請針對每條被標記的規則，只依據下方實際程式碼行號給出精準證據（禁止捏造不存在的行號）。\n"
            "請使用繁體中文，且嚴格只輸出 JSON：\n"
            "{\n"
            '  "findings": [\n'
            "    {\n"
            '      "rule_id": "規則ID",\n'
            '      "evidence_lines": "L10-L15",\n'
            '      "reasoning": "精準說明問題成因",\n'
            '      "suggested_fix": "具體可執行的修改建議"\n'
            "    }\n"
            "  ]\n"
            "}\n\n"
            "【觸發之規則清單】\n"
            + "\n".join(rules_desc)
            + "\n\n【目標程式碼與圖譜上下文】\n"
            + code_context
        )

    @staticmethod
    def parse_findings(raw_text: str) -> Dict[str, ExplainerFinding]:
        parsed = _extract_json_block(raw_text)
        findings: Dict[str, ExplainerFinding] = {}
        if isinstance(parsed, dict) and isinstance(parsed.get("findings"), list):
            for item in parsed["findings"]:
                if not isinstance(item, dict) or "rule_id" not in item:
                    continue
                rid = str(item["rule_id"])
                findings[rid] = ExplainerFinding(
                    rule_id=rid,
                    evidence_lines=str(item.get("evidence_lines", "?")),
                    reasoning=str(item.get("reasoning", "")),
                    suggested_fix=str(item.get("suggested_fix", "")),
                    raw_text=raw_text,
                )
        return findings


class GeminiHttpExplainer(BaseExplainerProvider):
    """Google Gemini `generateContent` HTTP Explainer."""

    provider_name = "GeminiHttp"

    def __init__(self, cfg: Dict[str, Any], api_key_override: Optional[str] = None):
        self.model = cfg.get("Model", "gemini-3.1-flash-lite")
        template = cfg.get(
            "EndpointOrCommand",
            "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        )
        self.endpoint = template.replace("{model}", self.model)
        self.api_key = resolve_secret(cfg.get("ApiKeyEnv", "$GOOGLE_API_KEY"), api_key_override)
        self.timeout = int(cfg.get("TimeoutSeconds", 45))
        self.temperature = float(cfg.get("Temperature", 0.0))

    def explain(
        self, code_context: str, triggered_verdicts: List[DecisionVerdict], rules_by_id: Dict[str, Dict[str, Any]]
    ) -> tuple[Dict[str, ExplainerFinding], float]:
        if not self.api_key:
            raise LintProviderError("Missing API key for GeminiHttp Explainer (check $GOOGLE_API_KEY or --api-key).")

        prompt = self.build_prompt(code_context, triggered_verdicts, rules_by_id)
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": self.temperature,
                "responseMimeType": "application/json",
            },
        }
        t0 = time.perf_counter()
        data = _http_post_json(
            self.endpoint,
            payload,
            headers={"x-goog-api-key": self.api_key},
            timeout_seconds=self.timeout,
        )
        latency_ms = (time.perf_counter() - t0) * 1000.0

        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        raw_text = "".join(p.get("text", "") for p in parts if isinstance(p, dict))
        findings = self.parse_findings(raw_text)
        if not findings and raw_text:
            raise LintProviderError(f"GeminiHttp returned unparseable explanation: {raw_text[:200]}")
        return findings, latency_ms


class OpenAiCompatibleExplainer(BaseExplainerProvider):
    """OpenAI / vLLM / LM Studio / DeepSeek Chat Completions Explainer."""

    provider_name = "OpenAiCompatible"

    def __init__(self, cfg: Dict[str, Any], api_key_override: Optional[str] = None):
        self.endpoint = cfg.get("EndpointOrCommand", "https://api.openai.com/v1/chat/completions")
        self.model = cfg.get("Model", "gpt-4o-mini")
        self.api_key = resolve_secret(cfg.get("ApiKeyEnv", "$OPENAI_API_KEY"), api_key_override)
        self.timeout = int(cfg.get("TimeoutSeconds", 45))
        self.temperature = float(cfg.get("Temperature", 0.0))

    def explain(
        self, code_context: str, triggered_verdicts: List[DecisionVerdict], rules_by_id: Dict[str, Dict[str, Any]]
    ) -> tuple[Dict[str, ExplainerFinding], float]:
        if not self.api_key and "localhost" not in self.endpoint and "127.0.0.1" not in self.endpoint:
            raise LintProviderError("Missing API key for OpenAiCompatible Explainer.")

        prompt = self.build_prompt(code_context, triggered_verdicts, rules_by_id)
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        t0 = time.perf_counter()
        data = _http_post_json(self.endpoint, payload, headers=headers, timeout_seconds=self.timeout)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        raw_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        findings = self.parse_findings(raw_text)
        if not findings and raw_text:
            raise LintProviderError(f"OpenAiCompatible returned unparseable explanation: {raw_text[:200]}")
        return findings, latency_ms


class OllamaExplainer(BaseExplainerProvider):
    """Local Ollama `/api/chat` Explainer."""

    provider_name = "Ollama"

    def __init__(self, cfg: Dict[str, Any], _api_key_override: Optional[str] = None):
        self.endpoint = cfg.get("EndpointOrCommand", "http://localhost:11434/api/chat")
        self.model = cfg.get("Model", "qwen2.5-coder:7b")
        self.timeout = int(cfg.get("TimeoutSeconds", 60))
        self.temperature = float(cfg.get("Temperature", 0.0))

    def explain(
        self, code_context: str, triggered_verdicts: List[DecisionVerdict], rules_by_id: Dict[str, Dict[str, Any]]
    ) -> tuple[Dict[str, ExplainerFinding], float]:
        prompt = self.build_prompt(code_context, triggered_verdicts, rules_by_id)
        payload = {
            "model": self.model,
            "stream": False,
            "format": "json",
            "options": {"temperature": self.temperature},
            "messages": [{"role": "user", "content": prompt}],
        }
        t0 = time.perf_counter()
        data = _http_post_json(self.endpoint, payload, headers={}, timeout_seconds=self.timeout)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        raw_text = data.get("message", {}).get("content", "")
        findings = self.parse_findings(raw_text)
        if not findings and raw_text:
            raise LintProviderError(f"Ollama returned unparseable explanation: {raw_text[:200]}")
        return findings, latency_ms


class CliExplainer(BaseExplainerProvider):
    """CLI-based Explainer supporting AgyCli, ClaudeCli, CodexCli, and CustomCli."""

    def __init__(self, provider_type: str, cfg: Dict[str, Any]):
        self.provider_name = provider_type
        self.command = cfg.get("EndpointOrCommand", "") or {
            "AgyCli": "agy",
            "ClaudeCli": "claude",
            "CodexCli": "codex",
        }.get(provider_type, "")
        self.model = cfg.get("Model", "")
        self.cli_args_template = cfg.get("CliArgsTemplate", "")
        self.timeout = int(cfg.get("TimeoutSeconds", 60))

    def explain(
        self, code_context: str, triggered_verdicts: List[DecisionVerdict], rules_by_id: Dict[str, Dict[str, Any]]
    ) -> tuple[Dict[str, ExplainerFinding], float]:
        resolved_exe = shutil.which(self.command) or self.command
        if not resolved_exe or (not os.path.exists(resolved_exe) and not shutil.which(self.command)):
            raise LintProviderError(f"CLI command '{self.command}' not found on PATH.")

        prompt = self.build_prompt(code_context, triggered_verdicts, rules_by_id)
        temp_path: Optional[str] = None
        stdin_text: Optional[str] = None
        argv: List[str] = [resolved_exe]

        try:
            if self.provider_name == "AgyCli":
                argv.extend(["--disable-slash-commands", "--output-format", "json"])
                if self.model:
                    argv.extend(["--model", self.model])
                if len(prompt) > 20000:
                    fd, temp_path = tempfile.mkstemp(prefix="codemap_lint_", suffix=".txt")
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        f.write(prompt)
                    argv.extend(["-p", f"請讀取並依照此檔案指示審查：{temp_path}"])
                else:
                    argv.extend(["-p", prompt])
            elif self.provider_name == "ClaudeCli":
                extra = shlex.split(self.cli_args_template) if self.cli_args_template else ["-p"]
                argv.extend(extra)
                if self.model and "--model" not in extra:
                    argv.extend(["--model", self.model])
                stdin_text = prompt
            elif self.provider_name == "CodexCli":
                extra = shlex.split(self.cli_args_template) if self.cli_args_template else ["exec", "-"]
                argv.extend(extra)
                if self.model and "--model" not in extra and "-m" not in extra:
                    argv.extend(["--model", self.model])
                stdin_text = prompt
            else:
                # CustomCli
                if "{prompt_file}" in self.cli_args_template:
                    fd, temp_path = tempfile.mkstemp(prefix="codemap_lint_", suffix=".txt")
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        f.write(prompt)
                    rendered = self.cli_args_template.replace("{prompt_file}", temp_path)
                    argv.extend(shlex.split(rendered))
                else:
                    if self.cli_args_template:
                        argv.extend(shlex.split(self.cli_args_template))
                    stdin_text = prompt

            t0 = time.perf_counter()
            proc = subprocess.run(
                argv,
                input=stdin_text,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
            )
            latency_ms = (time.perf_counter() - t0) * 1000.0
            if proc.returncode != 0:
                err_msg = (proc.stderr or proc.stdout or "").strip()[:300]
                raise LintProviderError(f"{self.provider_name} exited with {proc.returncode}: {err_msg}")

            raw_out = proc.stdout.strip()
            if self.provider_name == "AgyCli":
                envelope = _extract_json_block(raw_out)
                if isinstance(envelope, dict) and "response" in envelope:
                    raw_out = str(envelope["response"])

            findings = self.parse_findings(raw_out)
            if not findings and raw_out:
                raise LintProviderError(f"{self.provider_name} output did not match findings JSON: {raw_out[:200]}")
            return findings, latency_ms
        except subprocess.TimeoutExpired as exc:
            raise LintProviderError(f"{self.provider_name} timed out after {self.timeout}s.") from exc
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass


def create_decision_provider(
    cfg: Dict[str, Any], api_key_override: Optional[str] = None
) -> Optional[BaseDecisionProvider]:
    """Factory returning the configured Gatekeeper Decision provider, or None if disabled."""
    if not cfg.get("Enabled", True):
        return None
    provider = cfg.get("Provider", "GeminiDecision")
    if provider == "Disabled":
        return None
    if provider == "GeminiDecision":
        return GeminiDecisionProvider(cfg, api_key_override)
    if provider in ("OpenAiCompatible", "OpenAiDecision"):
        return OpenAiDecisionProvider(cfg, api_key_override)
    if provider == "HttpTemplate":
        return HttpTemplateDecisionProvider(cfg, api_key_override)
    raise LintProviderError(f"Unknown Gatekeeper Provider: {provider}")


def create_explainer_provider(
    cfg: Dict[str, Any], api_key_override: Optional[str] = None
) -> Optional[BaseExplainerProvider]:
    """Factory returning the configured Explainer LLM provider, or None if disabled."""
    if not cfg.get("Enabled", True):
        return None
    provider = cfg.get("Provider", "GeminiHttp")
    if provider == "Disabled":
        return None
    if provider == "GeminiHttp":
        return GeminiHttpExplainer(cfg, api_key_override)
    if provider == "OpenAiCompatible":
        return OpenAiCompatibleExplainer(cfg, api_key_override)
    if provider == "Ollama":
        return OllamaExplainer(cfg, api_key_override)
    if provider in ("AgyCli", "ClaudeCli", "CodexCli", "CustomCli"):
        return CliExplainer(provider, cfg)
    raise LintProviderError(f"Unknown Explainer Provider: {provider}")
