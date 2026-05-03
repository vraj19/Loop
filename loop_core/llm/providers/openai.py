import os
import json 
from loop_core.llm.providers.openai import OpenAI
from loop_core.llm.base import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):

    def __init__(self, model: str, api_key: str | None = None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(
            api_key=self.api_key or os.getenv("OPENAI_API_KEY")
        )

    def build_messages(self, prompt: str, system: str | None) -> list[dict]:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return messages
    
    def generate(self, prompt: str, system: str | None = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.build_messages(prompt, system), 
            max_tokens = 2048,
        )
        return response.choices[0].message.content.strip()
    
    def generate_json(self, prompt: str, system: str | None = None) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.build_messages(prompt, system), 
            max_tokens = 2048,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content.strip())