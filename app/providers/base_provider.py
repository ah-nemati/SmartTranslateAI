from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    async def translate(self, prompt: str) -> str:
        pass
