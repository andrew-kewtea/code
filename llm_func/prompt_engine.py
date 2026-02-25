#간단한 Jinja-like binding.


from typing import Dict
from string import Template


class PromptTemplate:

    def __init__(self, template: str):
        self.template = template

    def bind(self, dataset: Dict) -> str:
        """
        Simple string substitution.
        e.g. ${task_name}
        """
        return Template(self.template).safe_substitute(dataset)

# 사용 예시 
template = """
Evaluate task difficulty:

Task: ${task_name}
Description: ${description}
"""

dataset = {
    "task_name": "Implement login API",
    "description": "OAuth2 + JWT + Refresh token"
}