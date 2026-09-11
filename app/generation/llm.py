from typing import Protocol

import ollama


class LLMProvider(Protocol):
    def generate(self, prompt: str) -> str: ...


class OllamaLLMProvider:
    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
        )

        return response["response"]
