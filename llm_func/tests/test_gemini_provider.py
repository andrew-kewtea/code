import pytest
from ..thread import ChatThread
from ..llm_client import LLMClient


@pytest.mark.integration
@pytest.mark.provider
def test_gemini_provider(gemini_config):

    if not gemini_config.api_key:
        pytest.skip("GEMINI_API_KEY not set")

    client = LLMClient(gemini_config)
    thread = ChatThread()

    thread.add_user("Say hello in one word.")

    response = client.chat(thread)

    assert "text" in response
    assert isinstance(response["text"], str)
    assert len(response["text"]) > 0