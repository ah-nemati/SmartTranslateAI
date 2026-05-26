#!/bin/bash

PROJECT="smart-translate-ai"

mkdir -p $PROJECT/app/{core,providers,services,ui/widgets,workers,models}
mkdir -p $PROJECT/tests
mkdir -p $PROJECT/assets

cd $PROJECT

# requirements.txt
cat > requirements.txt << 'EOL'
aiohttp
pyside6
python-dotenv
pysrt
webvtt-py
EOL

# .gitignore
cat > .gitignore << 'EOL'
.venv/
__pycache__/
*.pyc
.env
.idea/
.vscode/
dist/
build/
*.spec
EOL

# pyproject.toml
cat > pyproject.toml << 'EOL'
[project]
name = "smart-translate-ai"
version = "0.1.0"
description = "AI Desktop Translation App"
requires-python = ">=3.11"
EOL

# README.md
cat > README.md << 'EOL'
# SmartTranslateAi

AI-powered desktop translation application with subtitle support.
EOL

# LICENSE (MIT)
cat > LICENSE << 'EOL'
MIT License
Copyright (c) 2026 SmartTranslateAi
EOL

# ==================== app/models ====================
cat > app/models/settings_model.py << 'EOL'
from dataclasses import dataclass

@dataclass
class AppSettings:
    api_key: str = ""
    api_url: str = "https://openrouter.ai/api/v1/chat/completions"
    model_name: str = "openai/gpt-oss-120b:free"
    temperature: float = 0.1
    max_tokens: int = 4000
EOL

cat > app/models/translation_model.py << 'EOL'
from dataclasses import dataclass
from enum import Enum

class ContentType(Enum):
    SUBTITLE = "subtitle"
    PLAIN_TEXT = "plain_text"

@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
    content_type: ContentType

@dataclass
class TranslationResult:
    success: bool
    translated_text: str
    error: str | None = None
EOL

# ==================== app/providers ====================
cat > app/providers/base_provider.py << 'EOL'
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    async def translate(self, prompt: str) -> str:
        pass
EOL

cat > app/providers/openrouter_provider.py << 'EOL'
import aiohttp
from app.providers.base_provider import BaseProvider
from app.models.settings_model import AppSettings

class OpenRouterProvider(BaseProvider):
    def __init__(self, settings: AppSettings):
        self.settings = settings

    async def translate(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.settings.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.settings.model_name,
            "messages": [
                {"role": "system", "content": "You are a professional translator."},
                {"role": "user", "content": prompt},
            ],
            "temperature": self.settings.temperature,
            "max_tokens": self.settings.max_tokens,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.settings.api_url, headers=headers, json=payload
            ) as response:
                data = await response.json()
                return data["choices"][0]["message"]["content"]
EOL

# ==================== app/core ====================
cat > app/core/splitter.py << 'EOL'
import re

def split_text(text: str, max_chars: int = 6000) -> list[str]:
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) > max_chars:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = ""
        current_chunk += paragraph + "\n\n"

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
EOL

cat > app/core/translator.py << 'EOL'
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
EOL

cat > app/core/validators.py << 'EOL'
# TODO: Add validation functions later
pass
EOL

cat > app/core/enums.py << 'EOL'
# TODO: Add shared enums later
pass
EOL

# ==================== app/services ====================
cat > app/services/translation_service.py << 'EOL'
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
EOL

cat > app/services/settings_service.py << 'EOL'
# TODO: Implement settings service later
pass
EOL

# ==================== app/ui ====================
cat > app/ui/main_window.py << 'EOL'
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTextEdit,
    QPushButton, QLabel
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartTranslateAi")
        self.resize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.title_label = QLabel("SmartTranslateAi")
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text here...")
        self.translate_button = QPushButton("Translate")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.input_text)
        layout.addWidget(self.translate_button)
        layout.addWidget(self.output_text)
EOL

# ==================== app/workers ====================
cat > app/workers/translation_worker.py << 'EOL'
# TODO: Implement QThread worker in next phase
pass
EOL

# ==================== app/main.py ====================
cat > app/main.py << 'EOL'
import sys
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
EOL

echo "✅ Project structure created successfully!"
echo "Now run:"
echo "   python -m venv .venv"
echo "   source .venv/bin/activate    # Linux/Mac"
echo "   .venv\\Scripts\\activate     # Windows"
echo "   pip install -r requirements.txt"
echo "   python -m app.main"
