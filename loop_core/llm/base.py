from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, prompt: str, system: str | None = None) -> str:
        """Generate a response based on the given prompt."""
        pass

    @abstractmethod
    def generate_json(self, prompt: str, system: str | None = None) -> dict:
        """Generate a JSON response based on the given prompt."""
        pass