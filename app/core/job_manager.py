from PySide6.QtCore import QObject, Signal, QThreadPool
from app.workers.translation_worker import TranslationWorker
from app.models.translation_model import TranslationRequest, ContentType
from app.services.file_service import FileService
from pathlib import Path

class JobManager(QObject):
    progress_text = Signal(str)
    progress_value = Signal(int)
    finished = Signal(str)
    error = Signal(str)
    batch_finished = Signal()

    def __init__(self, thread_pool: QThreadPool, translation_service):
        super().__init__()
        self.thread_pool = thread_pool
        self.translation_service = translation_service
        self.is_cancelled = False
        self.batch_files = []
        self.output_dir = None
        self.current_index = 0
        self.current_worker = None

    def submit_single(self, text: str, finished_callback):
        self.is_cancelled = False
        request = TranslationRequest(text=text)
        worker = TranslationWorker(self.translation_service, request)
        self._connect(worker, finished_callback)
        self.current_worker = worker
        self.thread_pool.start(worker)

    def start_batch(self, folder_path: str):
        self.is_cancelled = False
        self.batch_files = FileService.get_subtitle_files_in_folder(folder_path)
        self.output_dir = Path(folder_path) / "translated_output"
        self.current_index = 0

        if not self.batch_files:
            self.error.emit("فایل زیرنویس پیدا نشد!")
            return

        self.progress_text.emit(f"شروع ترجمه {len(self.batch_files)} فایل...")
        self._process_next()

    def _process_next(self):
        if self.is_cancelled or self.current_index >= len(self.batch_files):
            if not self.is_cancelled:
                self.batch_finished.emit()
            return

        file_path = self.batch_files[self.current_index]
        content = FileService.read_text(file_path)
        filename = file_path.name

        def on_finished(translated: str):
            FileService.save_text(self.output_dir / filename, translated)
            self.progress_text.emit(f"ذخیره شد: {filename}")
            self.current_index += 1
            self._process_next()

        request = TranslationRequest(text=content)
        worker = TranslationWorker(self.translation_service, request)
        self._connect(worker, on_finished)
        self.current_worker = worker
        self.thread_pool.start(worker)

    def _connect(self, worker, finished_callback):
        worker.signals.finished.connect(finished_callback)
        worker.signals.error.connect(self.error.emit)
        worker.signals.progress_text.connect(self.progress_text.emit)
        worker.signals.progress_value.connect(self.progress_value.emit)

    def cancel(self):
        self.is_cancelled = True
        self.progress_text.emit("🛑 ترجمه متوقف شد.")