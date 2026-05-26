from dataclasses import dataclass
from enum import Enum

class ContentType(Enum):
    SUBTITLE = "subtitle"
    PLAIN_TEXT = "plain_text"

@dataclass
class TranslationRequest:
    text: str
    source_language: str = "English"
    target_language: str = "Persian"
    content_type: ContentType = ContentType.SUBTITLE

@dataclass
class TranslationResult:
    success: bool
    translated_text: str = ""
    error: str | None = None