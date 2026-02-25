# llm_core/tests/conftest.py

import os
import pytest
from ..config import LLMConfig


@pytest.fixture
def openai_config():
    return LLMConfig(
        provider="openai",
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.1,
    )


@pytest.fixture
def gemini_config():
    return LLMConfig(
        provider="gemini",
        model="gemini-1.5-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
    )


@pytest.fixture
def compatible_config():
    return LLMConfig(
        provider="compatible",
        model="deepseek-chat",
        api_key=os.getenv("COMPATIBLE_API_KEY"),
        base_url=os.getenv("COMPATIBLE_BASE_URL"),
    )