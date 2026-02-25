from typing import List, Dict


class ChatThread:

    def __init__(self):
        self.messages: List[Dict] = []

    def add_user(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def add_assistant(self, content: str):
        self.messages.append({"role": "assistant", "content": content})

    def add_system(self, content: str):
        self.messages.append({"role": "system", "content": content})

    def reset(self):
        self.messages = []

    def get_messages(self) -> List[Dict]:
        return self.messages