from dataclasses import dataclass

@dataclass
class AppSettings:
    api_key: str = ""
    api_url: str = "https://openrouter.ai/api/v1/chat/completions"
    model_name: str = "openai/gpt-oss-120b:free"
    temperature: float = 0.1
    max_tokens: int = 4000