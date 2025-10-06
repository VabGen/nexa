from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class ParsedDocument:
    """Domain-объект результата парсинга."""

    def __init__(self, content: str, metadata: dict[str, Any], file_type: str):
        self.content = content
        self.metadata = metadata
        self.file_type = file_type


class DocumentParser(ABC):
    @abstractmethod
    def parse(
        self, file_path: Path | bytes, filename: str | None = None
    ) -> ParsedDocument:
        pass
