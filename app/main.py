import os
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QLabel, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout,
    QWidget, QMessageBox, QProgressBar, QFileDialog
)

from app.core.translator import Translator
from app.models.settings_model import AppSettings
from app.models.translation_model import ContentType, TranslationRequest
from app.providers.openrouter_provider import OpenRouterProvider
from app.services.translation_service import TranslationService
from app.services.settings_service import SettingsService
from app.services.file_service import FileService
from app.workers.translation_worker import TranslationWorker
from app.ui.settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartTranslateAi - Pro Batch Edition")
        self.resize(1000, 750)
        self.thread_pool = QThreadPool()
        self.settings_service = SettingsService()

        self.setup_menu()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # دکمه‌های ابزار
        button_layout = QHBoxLayout()
        
        self.open_file_button = QPushButton("Open File")
        self.open_file_button.clicked.connect(self.open_file)
        
        self.open_folder_button = QPushButton("Batch Folder Translate")
        self.open_folder_button.clicked.connect(self.open_folder)

        button_layout.addWidget(self.open_file_button)
        button_layout.addWidget(self.open_folder_button)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Subtitles text or paths will appear here...")

        self.translate_button = QPushButton("Start Translation")
        self.translate_button.clicked.connect(self.start_translation)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Translated output...")

        self.save_output_button = QPushButton("Save Output")
        self.save_output_button.clicked.connect(self.save_output)

        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setMaximumHeight(150)
        self.logs_text.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-family: monospace;")

        layout.addLayout(button_layout)
        layout.addWidget(self.input_text)
        layout.addWidget(self.translate_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.output_text)
        layout.addWidget(self.save_output_button)
        layout.addWidget(QLabel("Live Execution Logs:"))
        layout.addWidget(self.logs_text)
        
        self.batch_mode = False
        self.batch_files = []
        self.output_dir = ""

    def setup_menu(self):
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("Settings")
        open_settings_action = QAction("Open Settings", self)
        open_settings_action.triggered.connect(self.open_settings_dialog)
        settings_menu.addAction(open_settings_action)

    def open_settings_dialog(self):
        dialog = SettingsDialog()
        dialog.exec()

    def log(self, message: str):
        self.logs_text.append(message)
        # اسکرول خودکار به پایین
        scrollbar = self.logs_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Supported Files (*.txt *.srt *.vtt)"
        )
        if not file_path:
            return
        content = FileService.read_text(file_path)
        self.input_text.setPlainText(content)
        self.batch_mode = False
        self.log(f"Opened file: {file_path}")

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder for Batch Translation")
        if not folder_path:
            return
        
        # ساخت پوشه خروجی برای جلوگیری از تغییر نام یا بازنویسی فایل‌های اصلی
        self.output_dir = os.path.join(folder_path, "translated_output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.batch_files = []
        for root, _, files in os.walk(folder_path):
            # نادیده گرفتن پوشه خروجی در جستجو
            if "translated_output" in root:
                continue
            for file in files:
                if file.lower().endswith((".srt", ".vtt")):
                    self.batch_files.append(os.path.join(root, file))
        
        if not self.batch_files:
            QMessageBox.warning(self, "Warning", "No .srt or .vtt files found in the selected folder.")
            return

        self.batch_mode = True
        self.input_text.setPlainText(
            f"BATCH MODE ENABLED\n"
            f"Found {len(self.batch_files)} files in:\n{folder_path}\n\n"
            f"Files will be saved with ORIGINAL names in:\n{self.output_dir}\n\n" + 
            "\n".join(self.batch_files)
        )
        self.log(f"Loaded folder: {folder_path} ({len(self.batch_files)} files)")

    def save_output(self):
        if self.batch_mode:
            QMessageBox.information(self, "Info", "In Batch Mode, files are saved automatically.")
            return

        translated_text = self.output_text.toPlainText()
        if not translated_text:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Translation", "translated.srt", "Subtitle Files (*.srt *.vtt *.txt)"
        )
        if not file_path:
            return
        FileService.save_text(file_path, translated_text)
        self.log(f"Saved translation to: {file_path}")

    def start_translation(self):
        text = self.input_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Warning", "No content to translate.")
            return

        settings = self.settings_service.load()
        if not settings.api_key:
            QMessageBox.warning(self, "Warning", "Please set OpenRouter API Key in Settings first.")
            return

        self.translate_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.output_text.clear()

        if self.batch_mode:
            self.log(f"Starting batch translation for {len(self.batch_files)} files...")
            self.process_next_batch_file(0)
        else:
            self.log("Starting single text translation...")
            self._dispatch_worker(text, self.translation_finished)

    def process_next_batch_file(self, index: int):
        if index >= len(self.batch_files):
            self.translate_button.setEnabled(True)
            self.progress_bar.setVisible(False)
            self.log("✅ Batch Processing Complete!")
            QMessageBox.information(self, "Success", f"All files translated successfully!\nSaved in: {self.output_dir}")
            return

        file_path = self.batch_files[index]
        filename = os.path.basename(file_path)
        self.log(f"Processing ({index+1}/{len(self.batch_files)}): {filename}")
        content = FileService.read_text(file_path)

        def on_finished(translated_text):
            # ذخیره فایل دقیقاً با همان نام و پسوند در پوشه خروجی
            output_path = os.path.join(self.output_dir, filename)
            FileService.save_text(output_path, translated_text)
            self.log(f"💾 Saved: {filename}")
            # رفتن به فایل بعدی
            self.process_next_batch_file(index + 1)

        self._dispatch_worker(content, on_finished)

    def _dispatch_worker(self, text: str, finished_callback):
        settings = self.settings_service.load()
        provider = OpenRouterProvider(settings)
        translator = Translator(provider)
        service = TranslationService(translator)
        
        request = TranslationRequest(
            text=text,
            source_language="English",
            target_language="Persian",
            content_type=ContentType.SUBTITLE,
        )

        worker = TranslationWorker(service, request)
        worker.signals.finished.connect(finished_callback)
        worker.signals.error.connect(self.translation_error)
        worker.signals.progress_text.connect(self.log)
        worker.signals.progress_value.connect(self.progress_bar.setValue)
        
        self.thread_pool.start(worker)

    def translation_finished(self, translated_text: str):
        self.output_text.setPlainText(translated_text)
        self.translate_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.log("✅ Translation finished successfully.")

    def translation_error(self, error_message: str):
        QMessageBox.critical(self, "Error", error_message)
        self.translate_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.log(f"❌ Error: {error_message}")