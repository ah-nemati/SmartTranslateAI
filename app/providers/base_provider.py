from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    async def translate(self, prompt: str, model_name=None, temperature=None, max_tokens=None):
        pass