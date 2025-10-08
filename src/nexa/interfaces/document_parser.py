from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional


class ParsedDocument:
    def __init__(self, content: str, metadata: dict[str, Any], file_type: str):
        self.content = content
        self.metadata = metadata
        self.file_type = file_type


class DocumentParser(ABC):
    @abstractmethod
    def parse(
        self, file_path: Path | bytes, filename: Optional[str] = None
    ) -> ParsedDocument:
        pass
