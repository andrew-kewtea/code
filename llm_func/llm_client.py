from .config import LLMConfig
from .providers.openai_provider import OpenAIProvider
from .providers.gemini_provider import GeminiProvider
from .providers.openai_compatible_provider import OpenAICompatibleProvider


class LLMClient:

    def __init__(self, config: LLMConfig):

        if config.provider == "openai":
            self.provider = OpenAIProvider(
                api_key=config.api_key,
                model=config.model,
                base_url=config.base_url
            )

        elif config.provider == "gemini":
            self.provider = GeminiProvider(
                api_key=config.api_key,
                model=config.model
            )

        elif config.provider == "compatible":
            self.provider = OpenAICompatibleProvider(
                api_key=config.api_key,
                model=config.model,
                base_url=config.base_url
            )
        else:
            raise ValueError("Unsupported provider")

        self.config = config

    def chat(self, thread):
        return self.provider.chat(
            messages=thread.get_messages(),
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )