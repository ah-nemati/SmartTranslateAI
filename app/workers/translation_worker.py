import asyncio
from PySide6.QtCore import QObject, Signal, QRunnable
from app.models.translation_model import TranslationRequest
from app.services.translation_service import TranslationService

class WorkerSignals(QObject):
    finished = Signal(str)
    error = Signal(str)
    progress_text = Signal(str)
    progress_value = Signal(int)

class TranslationWorker(QRunnable):
    def __init__(self, service: TranslationService, request: TranslationRequest):
        super().__init__()
        self.service = service
        self.request = request
        self.signals = WorkerSignals()

    def progress_callback(self, text: str, value: int = None):
        if text:
            self.signals.progress_text.emit(text)
        if value is not None:
            self.signals.progress_value.emit(value)

    def run(self):
        try:
            result = asyncio.run(self.service.translate(self.request, self.progress_callback))
            if result.success:
                self.signals.progress_value.emit(100)
                self.signals.finished.emit(result.translated_text)
            else:
                self.signals.error.emit(result.error or "Unknown error")
        except Exception as error:
            self.signals.error.emit(str(error))