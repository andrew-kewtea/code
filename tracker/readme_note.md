tracking work progress from text references

sources:
- build_tracks : identify tracks (title, characteristics(type of work), references)
- gather sources - email, work note, activity log, git commits, server logs



llm_processor(function)

prompt: type:template
dataset
prompt_flow (theme) (prev_id, condition) ; theme_steps  : flow: steps
thread : 
run_prompt


(20고개를 하면서 원하는 겨로가 데이터를 추출해 낼수 있다)
prompt_flow (theme)에 의해 대화를 하면서 답변을 얻어 내면 이 dataset이 다시 원하는 서비스에 사용이 되게 된다
prompt_flow = function이 되는 것이지
funtion: type: prompt_flow


고등 function 예시 (prompt flows): 이것은 나중에 마법사 interface로도 사용될수 있다
(1) subtask_identifier
(2) dependency_inferencer
(3) task_progress_estimator

추가로 연구할 부분들: DAG 기반 Flow 설계, LangGraph 스타일 state machine 설계, multi-agent cooperative flow, auto retry + reflection 구조


다음 task description을 분석하여 subtask를 추출하라.

description: $description

출력 JSON:
{
  "subtasks": [
    {
      "title": string,
      "order": int,
      "dependencies": [int]
    }
  ],
  "confidence": float
}

{
  "status": "completed | in_progress | failed | paused | problematic",
  "progress_percent": 0-100,
  "reason": "...",
  "confidence": 0.0-1.0
}