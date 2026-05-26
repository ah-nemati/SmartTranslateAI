import os
from pathlib import Path
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QLabel, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout,
    QWidget, QMessageBox, QProgressBar, QFileDialog
)

from app.core.translator import Translator
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
        self.setWindowTitle("SmartTranslateAi - Enterprise Edition v1.3")
        self.resize(1150, 850)

        self.thread_pool = QThreadPool()
        self.settings_service = SettingsService()
        self.settings = self.settings_service.load()

        # Core Services (بهینه)
        self.provider = OpenRouterProvider(self.settings)
        self.translator = Translator(self.provider)
        self.translation_service = TranslationService(self.translator)

        self.setup_menu()
        self.setup_ui()

        self.batch_mode = False
        self.batch_files = []
        self.output_dir = ""

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Buttons
        btn_layout = QHBoxLayout()
        self.open_file_button = QPushButton("Open File")
        self.open_folder_button = QPushButton("Batch Folder Translate")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)

        btn_layout.addWidget(self.open_file_button)
        btn_layout.addWidget(self.open_folder_button)
        btn_layout.addWidget(self.stop_button)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Subtitles text or paths will appear here...")

        self.translate_button = QPushButton("Start Translation")
        self.translate_button.clicked.connect(self.start_translation)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        self.save_output_button = QPushButton("Save Output")
        self.save_output_button.clicked.connect(self.save_output)

        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setMaximumHeight(160)
        self.logs_text.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-family: monospace;")

        layout.addLayout(btn_layout)
        layout.addWidget(self.input_text)
        layout.addWidget(self.translate_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.output_text)
        layout.addWidget(self.save_output_button)
        layout.addWidget(QLabel("Live Execution Logs:"))
        layout.addWidget(self.logs_text)

        # Connect buttons
        self.open_file_button.clicked.connect(self.open_file)
        self.open_folder_button.clicked.connect(self.open_folder)
        self.stop_button.clicked.connect(self.stop_translation)

    def setup_menu(self):
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("Settings")
        action = QAction("Open Settings", self)
        action.triggered.connect(self.open_settings_dialog)
        settings_menu.addAction(action)

    def open_settings_dialog(self):
        dialog = SettingsDialog()
        dialog.exec()
        self.settings = self.settings_service.load()

    def log(self, message: str):
        self.logs_text.append(message)
        scrollbar = self.logs_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    # بقیه متدها (open_file, open_folder, start_translation و ...) دقیقاً مثل کد اصلی تو هستند
    # برای کوتاه شدن پیام، اگر خواستی بگو "main_window کامل" تا تمام متدها را دوباره بفرستم.

    def stop_translation(self):
        self.thread_pool.clear()
        self.translate_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.log("🛑 Translation stopped.")