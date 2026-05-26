from app.models.translation_model import TranslationResult
from app.core.translator import Translator

class TranslationService:
    def __init__(self, translator: Translator):
        self.translator = translator

    async def translate(self, request, progress_callback=None):
        try:
            translated_text = await self.translator.translate(request, progress_callback)
            return TranslationResult(success=True, translated_text=translated_text)
        except Exception as error:
            return TranslationResult(success=False, error=str(error))