import re

TOKEN_CHAR_RATIO = 3.5
SAFE_CONTEXT_PERCENT = 0.55

def dynamic_split_text(
    text: str, 
    model_context: int = 131000, 
    reserved_output_tokens: int = 8000
) -> list[str]:

    safe_input_tokens = int(model_context * SAFE_CONTEXT_PERCENT)
    safe_input_tokens -= reserved_output_tokens
    max_chars = int(safe_input_tokens * TOKEN_CHAR_RATIO)

    paragraphs = re.split(r"\n\s*\n", text.strip())
    batches = []
    current_batch = []
    current_chars = 0

    for paragraph in paragraphs:
        block_size = len(paragraph)
        if current_chars + block_size > max_chars and current_batch:
            batches.append("\n\n".join(current_batch))
            current_batch = []
            current_chars = 0
            
        current_batch.append(paragraph)
        current_chars += block_size

    if current_batch:
        batches.append("\n\n".join(current_batch))

    return batches