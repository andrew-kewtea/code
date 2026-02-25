# llm_core/main.py

from config import LLMConfig
from prompt_engine import PromptTemplate
from thread import ChatThread
from llm_client import LLMClient


def run():

    config = LLMConfig(
        provider="openai",  # openai | gemini | compatible
        model="gpt-4o-mini",
        api_key="YOUR_API_KEY",
        temperature=0.2,
    )

    client = LLMClient(config)
    thread = ChatThread()

    template_str = """
    Evaluate difficulty of task:

    Task: ${task_name}
    Description: ${description}

    Return JSON:
    {
        "difficulty_score": 1-10,
        "reason": "..."
    }
    """

    template = PromptTemplate(template_str)

    dataset = {
        "task_name": "Implement JWT login",
        "description": "Access + refresh token, blacklist, multi-device"
    }

    prompt = template.bind(dataset)

    thread.add_system("You are an expert project evaluator.")
    thread.add_user(prompt)

    response = client.chat(thread)

    print("RESPONSE:\n", response["text"])

    thread.add_assistant(response["text"])


if __name__ == "__main__":
    run()

