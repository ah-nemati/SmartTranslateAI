from pathlib import Path

SUPPORTED_FILES = [".txt", ".srt", ".vtt"]

class FileService:
    @staticmethod
    def read_text(file_path: str) -> str:
        path = Path(file_path)
        return path.read_text(encoding="utf-8")

    @staticmethod
    def save_text(file_path: str, content: str):
        path = Path(file_path)
        path.write_text(content, encoding="utf-8")
