"""Opt-in Ollama text provider; never grants file, shell or repository access."""
import json
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


class ProviderError(RuntimeError):
    pass


class OllamaTextProvider:
    def __init__(self, model, endpoint="http://127.0.0.1:11434", transport=None):
        parsed = urlsplit(endpoint)
        if (parsed.scheme != "http" or parsed.hostname not in ("localhost", "127.0.0.1")
                or not parsed.port or parsed.username or parsed.password
                or parsed.path not in ("", "/") or parsed.query or parsed.fragment):
            raise ValueError("LOCAL_ENDPOINT_REQUIRED")
        if not isinstance(model, str) or not model.strip():
            raise ValueError("MODEL_REQUIRED")
        self.model = model
        self.endpoint = endpoint.rstrip("/")
        self.transport = transport or urlopen

    def generate(self, prompt):
        if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 100000:
            raise ValueError("INVALID_PROMPT")
        payload = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode("utf-8")
        request = Request(self.endpoint + "/api/generate", data=payload,
                          headers={"Content-Type": "application/json"}, method="POST")
        try:
            with self.transport(request, timeout=30) as response:
                raw = response.read(1000001)
            if len(raw) > 1000000:
                raise ValueError("OVERSIZED_RESPONSE")
            text = json.loads(raw.decode("utf-8"))["response"]
            if not isinstance(text, str):
                raise ValueError("NOT_TEXT")
            return text
        except Exception:
            raise ProviderError("LOCAL_PROVIDER_FAILED") from None
