from app.models.translation_model import TranslationRequest
from app.providers.base_provider import BaseProvider
from app.core.splitter import split_text

class Translator:
    def __init__(self, provider: BaseProvider):
        self.provider = provider

    async def translate(self, request: TranslationRequest) -> str:
        chunks = split_text(request.text)
        translated_chunks = []

        for chunk in chunks:
            prompt = self._build_prompt(
                chunk, request.source_language, request.target_language
            )
            translated = await self.provider.translate(prompt)
            translated_chunks.append(translated)

        return "\n\n".join(translated_chunks)

    def _build_prompt(self, text: str, source_language: str, target_language: str) -> str:
        return f"""
Translate the following text.

Source Language: {source_language}
Target Language: {target_language}

Text:
{text}
"""
