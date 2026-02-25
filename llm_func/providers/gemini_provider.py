import google.generativeai as genai
from typing import List, Dict
from .base import BaseProvider


class GeminiProvider(BaseProvider):

    def __init__(self, api_key: str, model: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def chat(self, messages: List[Dict], **kwargs):

        # Gemini는 메시지 포맷이 다름
        history = []
        for m in messages:
            if m["role"] == "user":
                history.append({"role": "user", "parts": [m["content"]]})
            elif m["role"] == "assistant":
                history.append({"role": "model", "parts": [m["content"]]})

        response = self.model.generate_content(history)

        return {
            "text": response.text,
            "raw": response.to_dict()
        }