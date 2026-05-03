from loop_core.llm.base import BaseLLMProvider
from loop_core.config import (
    LLM_PROVIDER,
    LLM_MODEL,
    OLLAMA_BASE_URL,
)


_llm_provider: BaseLLMProvider |None = None

def get_llm_provider() -> BaseLLMProvider:
    global _llm_provider
    if _llm_provider is None:
        _llm_provider = _load_llm_provider()
    return _llm_provider

def _load_llm_provider() -> BaseLLMProvider:

    valid_providers = ["anthropic", "openai", "ollama"]

    if LLM_PROVIDER == "anthropic":
        from loop_core.llm.providers.anthropic import AnthropicLLMProvider
        return AnthropicLLMProvider(model=LLM_MODEL)
    
    elif LLM_PROVIDER == "openai":
        from loop_core.llm.providers.openai import OpenAIProvider
        return OpenAIProvider(model=LLM_MODEL)
    
    elif LLM_PROVIDER == "ollama":
        from loop_core.llm.providers.ollama import OllamaProvider
        return OllamaProvider(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)
    else:
        raise ValueError(
            f"Unsupported LLM provider: '{LLM_PROVIDER}'. "
            f"Valid options: {', '.join(valid_providers)}"
        )