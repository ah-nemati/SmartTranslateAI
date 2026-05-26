from pathlib import Path
from typing import List

SUPPORTED_EXTENSIONS = {".txt", ".srt", ".vtt"}

class FileService:
    @staticmethod
    def read_text(file_path: str | Path) -> str:
        return Path(file_path).read_text(encoding="utf-8", errors="replace")

    @staticmethod
    def save_text(file_path: str | Path, content: str):
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    @staticmethod
    def get_subtitle_files_in_folder(folder_path: str | Path) -> List[Path]:
        folder = Path(folder_path)
        files = []
        for file in folder.rglob("*"):
            if file.suffix.lower() in SUPPORTED_EXTENSIONS and "translated_output" not in file.parts:
                files.append(file)
        return files