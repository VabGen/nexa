import io
from pathlib import Path
from typing import Any
from unstructured.partition.auto import partition
from nexa.interfaces.document_parser import DocumentParser, ParsedDocument


class UnstructuredDocumentParser(DocumentParser):
    def parse(
        self, file_input: Path | bytes, filename: str | None = None
    ) -> ParsedDocument:
        if isinstance(file_input, bytes):
            if filename is None:
                raise ValueError("filename is required when parsing bytes")
            file_obj = io.BytesIO(file_input)
            elements = partition(file=file_obj, file_filename=filename, strategy="fast")
        else:
            elements = partition(filename=str(file_input), strategy="fast")
            filename = file_input.name

        content = "\n\n".join([str(el) for el in elements])
        meta: dict[str, Any] = {
            "filename": filename,
            "element_count": len(elements),
            "types": list({el.category for el in elements}),
        }
        file_type = filename.split(".")[-1].lower() if "." in filename else "unknown"

        return ParsedDocument(content=content, metadata=meta, file_type=file_type)
