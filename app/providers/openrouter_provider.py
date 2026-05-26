import aiohttp
from app.providers.base_provider import BaseProvider
from app.models.settings_model import AppSettings

class OpenRouterProvider(BaseProvider):
    def __init__(self, settings: AppSettings):
        self.settings = settings

    async def translate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.settings.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.settings.model_name,
            "messages": [
                {"role": "system", "content": "You are a professional translator."},
                {"role": "user", "content": prompt},
            ],
            "temperature": self.settings.temperature,
            "max_tokens": self.settings.max_tokens,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.settings.api_url, headers=headers, json=payload
            ) as response:
                data = await response.json()
                return data["choices"][0]["message"]["content"]
