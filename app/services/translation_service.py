from app.core.translator import Translator
from app.models.translation_model import TranslationRequest, TranslationResult

class TranslationService:
    def __init__(self, translator: Translator):
        self.translator = translator

    async def translate(self, request: TranslationRequest) -> TranslationResult:
        try:
            translated_text = await self.translator.translate(request)
            return TranslationResult(
                success=True,
                translated_text=translated_text
            )
        except Exception as error:
            return TranslationResult(
                success=False,
                translated_text="",
                error=str(error)
            )
