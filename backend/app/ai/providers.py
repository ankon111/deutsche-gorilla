from abc import ABC, abstractmethod
from typing import List


class BaseAIProvider(ABC):
    @abstractmethod
    def generate_examples(self, word: str, count: int) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def chat(self, prompt: str, history: list, context: dict | None = None) -> str:
        raise NotImplementedError


class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_examples(self, word: str, count: int) -> List[str]:
        return [f"Example {i + 1} for {word}." for i in range(count)]

    def chat(self, prompt: str, history: list, context: dict | None = None) -> str:
        return "OpenAI response placeholder."


class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_examples(self, word: str, count: int) -> List[str]:
        return [f"Example {i + 1} for {word}." for i in range(count)]

    def chat(self, prompt: str, history: list, context: dict | None = None) -> str:
        return "Gemini response placeholder."


def provider_factory(provider: str, api_key: str) -> BaseAIProvider:
    if provider == "gemini":
        return GeminiProvider(api_key)
    return OpenAIProvider(api_key)
