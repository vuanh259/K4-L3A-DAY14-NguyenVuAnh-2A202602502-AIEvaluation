"""Offline checks for provider routing and Gemini response handling."""
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
import httpx

spec = importlib.util.spec_from_file_location(
    "domain_assistant_provider_test", Path(__file__).resolve().parents[1] / "domain_assistant.py"
)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_gemini_routing_and_endpoint():
    with patch.dict(module.os.environ, {"GEMINI_API_KEY": "test-key", "GEMINI_MODEL": "test-model"}, clear=True), patch.object(module, "OpenAI") as client:
        generator = module.configured_generator()
        assert isinstance(generator, module.GeminiGenerator)
        assert generator.model == "test-model"
        assert client.call_args.kwargs["base_url"] == "https://generativelanguage.googleapis.com/v1beta/openai/"


def test_explicit_openai_overrides_gemini_key():
    with patch.dict(module.os.environ, {"AI_PROVIDER": "openai", "GEMINI_API_KEY": "test-key"}, clear=True), patch.object(module, "OpenAIGenerator") as factory:
        assert module.configured_generator() is factory.return_value


@pytest.mark.parametrize("content,reason", [("", "stop"), ("partial", "length")])
def test_gemini_rejects_empty_or_truncated_answer(content, reason):
    generator = module.GeminiGenerator.__new__(module.GeminiGenerator)
    generator.model = "test-model"
    generator.max_output_tokens = 2048
    generator.min_interval = 0
    generator._last_request = 0
    generator.client = Mock()
    generator.client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content), finish_reason=reason)]
    )
    with pytest.raises(RuntimeError):
        generator.generate("question and retrieved evidence")


def test_gemini_rate_limit_retry_is_bounded():
    generator = module.GeminiGenerator.__new__(module.GeminiGenerator)
    generator.model = "test-model"
    generator.max_output_tokens = 2048
    generator.min_interval = 0
    generator._last_request = 0
    generator.client = Mock()
    response = httpx.Response(429, request=httpx.Request('POST', 'https://example.test'))
    generator.client.chat.completions.create.side_effect = module.RateLimitError(
        'rate limit', response=response, body=None
    )
    with patch.object(module.time, 'sleep') as sleep, pytest.raises(module.RateLimitError):
        generator.generate('question')
    assert generator.client.chat.completions.create.call_count == 4
    assert sleep.call_count == 3
    sleep.assert_called_with(60)
