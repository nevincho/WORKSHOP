"""Explicitly opted-in, loopback-only Ollama text provider.

No file, shell or repository capabilities are exposed to the model.
"""
import json
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler, ProxyHandler

from .ai_provider_contract import ModelReply


class ProviderError(RuntimeError):
    """Stable provider error that must never include model output or credentials."""


class _RejectRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise ProviderError("LOCAL_PROVIDER_REDIRECT_FORBIDDEN")


def _safe_local_transport(request, timeout):
    # Default urllib redirects and environment proxies must not bypass loopback restrictions.
    return build_opener(ProxyHandler({}), _RejectRedirect()).open(request, timeout=timeout)


class OllamaTextProvider:
    def __init__(self, model, endpoint="http://127.0.0.1:11434", transport=None):
        parsed = urlsplit(endpoint)
        if (parsed.scheme != "http" or parsed.hostname not in ("localhost", "127.0.0.1")
                or not parsed.port or parsed.username or parsed.password
                or parsed.path not in ("", "/") or parsed.query or parsed.fragment):
            raise ValueError("LOCAL_ENDPOINT_REQUIRED")
        if not isinstance(model, str) or not model.strip() or len(model) > 128:
            raise ValueError("MODEL_REQUIRED")
        self.model = model
        self.endpoint = endpoint.rstrip("/")
        self.transport = transport or _safe_local_transport

    def generate(self, prompt):
        if not isinstance(prompt, str) or not prompt.strip() or len(prompt.encode("utf-8")) > 100000:
            raise ValueError("INVALID_PROMPT")
        payload = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode("utf-8")
        request = Request(self.endpoint + "/api/generate", data=payload,
                          headers={"Content-Type": "application/json"}, method="POST")
        try:
            with self.transport(request, timeout=30) as response:
                raw = response.read(1000001)
            if len(raw) > 1000000:
                raise ProviderError("LOCAL_PROVIDER_RESPONSE_TOO_LARGE")
            data = json.loads(raw.decode("utf-8"))
            text = data["response"]
            if not isinstance(text, str):
                raise ValueError("NOT_TEXT")
            return ModelReply(provider="ollama", model=self.model, content=text)
        except ProviderError:
            raise
        except Exception:
            raise ProviderError("LOCAL_PROVIDER_FAILED") from None
