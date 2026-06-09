"""Unit tests for the provider-agnostic LLM config. No network required."""

import pytest

from llm import LLMConfig, LLMError


def test_defaults_to_ollama():
    cfg = LLMConfig.from_request({})
    assert cfg.provider == "ollama"
    assert cfg.model  # a provider-specific default is filled in
    assert cfg.api_key is None


def test_unknown_provider_falls_back_to_ollama():
    assert LLMConfig.from_request({"provider": "bogus"}).provider == "ollama"


def test_provider_is_normalized():
    assert LLMConfig.from_request({"provider": "  OpenRouter "}).provider == "openrouter"


def test_camelcase_keys_accepted_and_base_url_trimmed():
    cfg = LLMConfig.from_request(
        {"provider": "openai", "apiKey": "sk-x", "baseUrl": "http://host/"}
    )
    assert cfg.api_key == "sk-x"
    assert cfg.base_url == "http://host"  # trailing slash stripped


@pytest.mark.parametrize("provider", ["openrouter", "gemini", "openai", "anthropic"])
def test_each_cloud_provider_has_a_default_model(provider):
    assert LLMConfig.from_request({"provider": provider}).model


@pytest.mark.parametrize("provider", ["openrouter", "gemini", "openai", "anthropic"])
def test_require_ready_raises_without_key(provider):
    with pytest.raises(LLMError):
        LLMConfig(provider=provider, model="m", api_key=None).require_ready()


def test_require_ready_ok_for_ollama_without_key():
    LLMConfig(provider="ollama", model="m").require_ready()  # must not raise


def test_label_format():
    assert LLMConfig(provider="ollama", model="x").label == "ollama:x"
