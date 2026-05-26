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
