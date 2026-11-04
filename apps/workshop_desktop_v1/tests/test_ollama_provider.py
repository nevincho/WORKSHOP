import io
import json
import unittest

from workshop_desktop.ollama_provider import OllamaTextProvider, ProviderError


class FakeResponse:
    def __enter__(self):
        return io.BytesIO(b'{"response":"ready"}')

    def __exit__(self, *args):
        return False


class ProviderTests(unittest.TestCase):
    def test_local_boundary(self):
        with self.assertRaises(ValueError):
            OllamaTextProvider("small", "http://example.com:11434")

    def test_generate(self):
        captured = []
        def transport(request, timeout):
            captured.append(json.loads(request.data))
            return FakeResponse()
        result = OllamaTextProvider("small", transport=transport).generate("hello")
        self.assertEqual(result, "ready")
        self.assertEqual(captured[0]["stream"], False)

    def test_failure(self):
        def transport(request, timeout):
            raise OSError("connection refused")
        with self.assertRaises(ProviderError):
            OllamaTextProvider("small", transport=transport).generate("hello")


if __name__ == "__main__":
    unittest.main()
