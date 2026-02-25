# llm_core/config.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMConfig:
    provider: str
    model: str
    api_key: str
    base_url: Optional[str] = None  # for OpenAI-compatible providers
    temperature: float = 0.2
    max_tokens: int = 1024