from abc import ABC, abstractmethod


class TextRefiner(ABC):
    @abstractmethod
    def refine(self, text: str) -> str:
        """Исправляет грамматику и стиль текста."""
        pass
