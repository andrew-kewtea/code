from openai import OpenAI
from typing import List, Dict
from .base import BaseProvider

# DeepSeek, Moonshot, Qwen API
class OpenAICompatibleProvider(BaseProvider):

    def __init__(self, api_key: str, model: str, base_url: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def chat(self, messages: List[Dict], temperature=0.2, max_tokens=1024):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return {
            "text": response.choices[0].message.content,
            "raw": response.model_dump()
        }