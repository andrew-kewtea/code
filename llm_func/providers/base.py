from abc import ABC, abstractmethod
from typing import List, Dict


class BaseProvider(ABC):

    @abstractmethod
    def chat(self, messages: List[Dict], **kwargs) -> Dict:
        """
        Returns:
            {
                "text": "...",
                "raw": {...}
            }
        """
        pass