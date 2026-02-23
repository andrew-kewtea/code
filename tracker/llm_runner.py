# services/llm_runner.py
from sqlalchemy.orm import Session
from models.prompt import PromptTemplate
from models.thread import Thread, ThreadMessage
from services.prompt_renderer import render_prompt
from services.llm_executor import call_llm
import json


def run_prompt(
    db: Session,
    prompt_name: str,
    dataset: dict,
    thread_id: int | None = None
) -> dict:

    prompt: PromptTemplate = db.query(PromptTemplate)\
        .filter(PromptTemplate.name == prompt_name)\
        .first()

    if not prompt:
        raise ValueError("Prompt not found")

    user_prompt = render_prompt(prompt.user_template, dataset)

    result = call_llm(prompt.system_prompt, user_prompt)

    # confidence 없으면 보정
    if "confidence" not in result:
        result["confidence"] = 0.5

    # thread 기록
    if thread_id:
        db.add(ThreadMessage(
            thread_id=thread_id,
            role="user",
            content=user_prompt
        ))

        db.add(ThreadMessage(
            thread_id=thread_id,
            role="assistant",
            content=json.dumps(result, ensure_ascii=False)
        ))

        db.commit()

    return result