import os
import json
import loop_core.llm.providers.anthropic as anthropic
from loop_core.llm.base import BaseLLMProvider

class AnthropicLLMProvider(BaseLLMProvider):
    """LLM provider implementation for Anthropic's API."""
    def __init__(self, model: str, api_key: str | None = None):
        self.client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    def build_kwargs(self, prompt: str, system: str | None) -> dict:
        kwargs = {
            "model": self.model,
            "max_tokens": 2048,
            "messages": [{"role": "user", "content": prompt}]
        }

        if system:
            kwargs["system"] = system
        
        return kwargs
    
    def generate(self, prompt: str, system: str | None = None) -> str:
        response = self.client.messages.create(**self._build_kwargs(prompt, system))
        return response.choices[0].text.strip()
    
    def generate_json(self, prompt: str, system: str | None = None) -> dict:
        system_prompt = (system or "") + "\nRespond only with valid JSON. No explanation, no markdown, no backticks."
        response = self.client.messages.create(**self._build_kwargs(prompt, system_prompt))
        return json.loads(response.choices[0].text.strip())