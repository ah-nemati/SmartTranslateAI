from PySide6.QtWidgets import (
    QComboBox, QDialog, QDoubleSpinBox, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QMessageBox, QPushButton, QSpinBox, QVBoxLayout
)
from app.models.settings_model import AppSettings
from app.services.settings_service import SettingsService

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.resize(500, 300)
        self.settings_service = SettingsService()
        self.settings = self.settings_service.load()
        self.setup_ui()
        self.load_values()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)

        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "openai/gpt-oss-120b:free",
            "google/gemma-3-27b-it:free",
            "meta-llama/llama-3.3-70b-instruct:free",
        ])

        self.temperature_input = QDoubleSpinBox()
        self.temperature_input.setRange(0, 2)
        self.temperature_input.setSingleStep(0.1)

        self.max_tokens_input = QSpinBox()
        self.max_tokens_input.setRange(100, 32000)

        form_layout.addRow(QLabel("API Key"), self.api_key_input)
        form_layout.addRow(QLabel("Model"), self.model_combo)
        form_layout.addRow(QLabel("Temperature"), self.temperature_input)
        form_layout.addRow(QLabel("Max Tokens"), self.max_tokens_input)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.close)

    def load_values(self):
        self.api_key_input.setText(self.settings.api_key)
        self.model_combo.setCurrentText(self.settings.model_name)
        self.temperature_input.setValue(self.settings.temperature)
        self.max_tokens_input.setValue(self.settings.max_tokens)

    def save_settings(self):
        api_key = self.api_key_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Warning", "API Key is required.")
            return

        settings = AppSettings(
            api_key=api_key,
            model_name=self.model_combo.currentText(),
            temperature=self.temperature_input.value(),
            max_tokens=self.max_tokens_input.value(),
        )
        self.settings_service.save(settings)
        QMessageBox.information(self, "Success", "Settings saved successfully.")
        self.accept()
