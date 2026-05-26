import aiohttp
import json
from app.providers.base_provider import BaseProvider
from app.models.settings_model import AppSettings

SYSTEM_PROMPT = """
شما مترجم حرفه‌ای زیرنویس فیلم و سریال هستید.

قوانین بسیار مهم:

- ساختار subtitle باید کاملاً حفظ شود
- شماره‌ها نباید تغییر کنند
- timestamp ها نباید تغییر کنند
- فقط متن دیالوگ ترجمه شود
- ترجمه باید روان، طبیعی و محاوره‌ای باشد
- ترجمه تحت‌اللفظی نباشد
- هیچ توضیح اضافه ننویس
- markdown ننویس
- فقط subtitle نهایی را برگردان
- هیچ متن اضافه‌ای تولید نکن
"""

class OpenRouterProvider(BaseProvider):

    def __init__(self, settings: AppSettings):
        self.settings = settings

    async def translate(
        self, 
        prompt: str, 
        model_name: str = None, 
        temperature: float = None, 
        max_tokens: int = None
    ) -> str:
        
        headers = {
            "Authorization": f"Bearer {self.settings.api_key}",
            "Content-Type": "application/json",
            "Connection": "close",
        }

        payload = {
            "model": model_name or self.settings.model_name,
            "provider": {"allow_fallbacks": True},
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature or self.settings.temperature,
            "top_p": 0.9,
            "max_tokens": max_tokens or self.settings.max_tokens,
            "stream": False,
        }

        timeout = aiohttp.ClientTimeout(total=300, connect=60, sock_read=300)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.settings.api_url, 
                headers=headers, 
                json=payload, 
                timeout=timeout
            ) as response:
                
                raw = await response.read()
                text = raw.decode("utf-8", errors="ignore")

                if response.status != 200:
                    raise Exception(f"HTTP {response.status} => {text}")

                try:
                    data = json.loads(text)
                except Exception as e:
                    raise Exception(f"JSON Parse Error => {e}\n{text[:1000]}")

                if "choices" not in data:
                    raise Exception(f"Invalid response => {data}")

                translated = data["choices"][0]["message"]["content"].strip()

                if not translated:
                    raise Exception("Empty response")

                return translated