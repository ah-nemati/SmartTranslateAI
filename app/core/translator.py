import asyncio
from app.models.translation_model import TranslationRequest
from app.providers.base_provider import BaseProvider
from app.core.splitter import dynamic_split_text

MODELS = [
    {"name": "openai/gpt-oss-120b:free", "context": 131000, "max_output": 8000, "temperature": 0.1},
]

class Translator:
    def __init__(self, provider: BaseProvider):
        self.provider = provider
        self.max_retries = 5

    async def translate(self, request: TranslationRequest, progress_callback=None) -> str:
        primary_model = MODELS[0]
        chunks = dynamic_split_text(
            request.text, 
            primary_model["context"], 
            primary_model["max_output"]
        )
        
        translated_chunks = []
        total_chunks = len(chunks)

        for i, chunk in enumerate(chunks, 1):
            if progress_callback:
                progress_callback(f"Translating chunk {i}/{total_chunks}...", int((i-1)/total_chunks * 100))

            prompt = self._build_prompt(chunk)
            translated_text = await self._translate_with_retries(prompt, progress_callback)
            translated_chunks.append(translated_text)
            
            if progress_callback:
                progress_callback(f"Chunk {i} completed.", int(i/total_chunks * 100))
                
            await asyncio.sleep(0.8)

        return "\n\n".join(translated_chunks)

    async def _translate_with_retries(self, prompt: str, progress_callback) -> str:
        for model in MODELS:
            if progress_callback:
                progress_callback(f"Trying model: {model['name']}", None)

            for attempt in range(1, self.max_retries + 1):
                try:
                    return await self.provider.translate(
                        prompt, 
                        model_name=model["name"],
                        temperature=model["temperature"],
                        max_tokens=model["max_output"]
                    )
                except Exception as e:
                    wait_time = min(attempt * 3, 15)
                    if progress_callback:
                        progress_callback(f"Attempt {attempt} failed. Retrying...", None)
                    await asyncio.sleep(wait_time)
        raise Exception("All models and retries failed.")

    def _build_prompt(self, text: str) -> str:
        return f"""
زیرنویس زیر را به فارسی روان و طبیعی ترجمه کن.

قوانین مهم:
- ساختار، شماره‌ها و زمان‌بندی را دقیقاً حفظ کن
- فقط متن دیالوگ را ترجمه کن
- ترجمه محاوره‌ای و طبیعی باشد

Subtitle:
----------------
{text}
----------------
"""