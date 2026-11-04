import io
import json
import unittest

from workshop_desktop.ollama_provider import (
    OllamaTextProvider, ProviderError, _RejectRedirect,
)


class FakeResponse:
    def __enter__(self):
        return io.BytesIO(b'{"response":"ready"}')

    def __exit__(self, *args):
        return False


class ProviderTests(unittest.TestCase):
    def test_local_boundary(self):
        for endpoint in (
            "http://example.com:11434",
            "http://192.168.0.1:11434",
            "http://localhost:11434/trick",
            "http://localhost:11434?redirect=1",
            "https://localhost:11434",
        ):
            with self.subTest(endpoint=endpoint):
                with self.assertRaises(ValueError):
                    OllamaTextProvider("small", endpoint)

    def test_generate_matches_provider_contract(self):
        captured = []
        def transport(request, timeout):
            captured.append(json.loads(request.data))
            return FakeResponse()
        result = OllamaTextProvider("small", transport=transport).generate("hello")
        self.assertEqual(result.content, "ready")
        self.assertEqual(result.model, "small")
        self.assertEqual(result.provider, "ollama")
        self.assertEqual(captured[0]["stream"], False)

    def test_failure_redacts_internal_details(self):
        def transport(request, timeout):
            raise OSError("secret internal endpoint")
        with self.assertRaises(ProviderError) as ctx:
            OllamaTextProvider("small", transport=transport).generate("hello")
        self.assertEqual(str(ctx.exception), "LOCAL_PROVIDER_FAILED")

    def test_redirect_rejected(self):
        with self.assertRaisesRegex(ProviderError, "LOCAL_PROVIDER_REDIRECT_FORBIDDEN"):
            _RejectRedirect().redirect_request(None, None, 302, "redirect", {}, "http://example.com/")

    def test_prompt_validation(self):
        provider = OllamaTextProvider("small", transport=lambda *args, **kwargs: FakeResponse())
        with self.assertRaises(ValueError):
            provider.generate("")


if __name__ == "__main__":
    unittest.main()
