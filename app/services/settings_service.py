from PySide6.QtCore import QSettings
from app.models.settings_model import AppSettings

class SettingsService:
    def __init__(self):
        self.settings = QSettings("SmartTranslateAi", "SmartTranslateAi")

    def save(self, app_settings: AppSettings):
        self.settings.setValue("api_key", app_settings.api_key)
        self.settings.setValue("api_url", app_settings.api_url)
        self.settings.setValue("model_name", app_settings.model_name)
        self.settings.setValue("temperature", app_settings.temperature)
        self.settings.setValue("max_tokens", app_settings.max_tokens)

    def load(self) -> AppSettings:
        return AppSettings(
            api_key=self.settings.value("api_key", ""),
            api_url=self.settings.value("api_url", "https://openrouter.ai/api/v1/chat/completions"),
            model_name=self.settings.value("model_name", "openai/gpt-oss-120b:free"),
            temperature=float(self.settings.value("temperature", 0.1)),
            max_tokens=int(self.settings.value("max_tokens", 4000)),
        )
