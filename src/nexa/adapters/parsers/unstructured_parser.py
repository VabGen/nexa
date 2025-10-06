import io
from pathlib import Path
from typing import Any
from unstructured.partition.auto import partition
from unstructured.documents.elements import Element
from nexa.interfaces.document_parser import DocumentParser, ParsedDocument

class UnstructuredDocumentParser(DocumentParser):
    def parse(self, file_input: Path | bytes, filename: str | None = None) -> ParsedDocument:
        # Подготавливаем вход
        if isinstance(file_input, bytes):
            file = io.BytesIO(file_input)
            if not filename:
                raise ValueError("filename required when parsing bytes")
        else:
            file = file_input
            filename = file_input.name

        # Парсим
        elements = partition(
            file=file,
            file_filename=filename,
            strategy="fast",  # или "hi_res" для лучшего качества (медленнее)
        )

        # Собираем текст и метаданные
        content = "\n\n".join([str(el) for el in elements])
        meta: dict[str, Any] = {
            "filename": filename,
            "element_count": len(elements),
            "types": list({el.category for el in elements}),
        }

        # Определяем тип документа
        suffix = Path(filename).suffix.lower()
        file_type = suffix[1:] if suffix.startswith(".") else "unknown"

        return ParsedDocument(content=content, metadata=meta, file_type=file_type)