import requests
import json
from loop_core.llm.base import BaseLLMProvider

class OllamaProvider(BaseLLMProvider):
    def __init__(self, model: str, base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    
    def _post(self, prompt: str, system: str | None = None, fmt: str | None = None) -> dict:
        payload = {
            "model": self.model,
            "prompt": prompt, 
            "stream": False,
        }
        if system:
            payload["system"] = system
        if fmt:
            payload["fmt"] = fmt

        response = requests.post(f"{self.base_url}/api/generate", json=payload)
        response.raise_for_status()
        return response.json()
    
    def generate(self, prompt: str, system: str | None = None) -> str:
        response = self._post(prompt, system)
        return response["response"].strip()
    
    def generate_json(self, prompt : str, system : str | None = None) -> dict:
        raw = self._post(prompt, system, fmt="json")["response"]
        return json.loads(raw)