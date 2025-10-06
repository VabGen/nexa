from fastapi import FastAPI, UploadFile, File
from nexa.interfaces.document_parser import DocumentParser
from nexa.adapters.parsers.unstructured_parser import UnstructuredDocumentParser


def create_app() -> FastAPI:
    app = FastAPI(title="Nexa Document AI", version="0.1.0")
    parser: DocumentParser = UnstructuredDocumentParser()

    @app.post("/parse")
    async def parse_document(file: UploadFile = File(...)):
        content = await file.read()
        result = parser.parse(content, file.filename)
        return {
            "file_type": result.file_type,
            "summary": (
                result.content[:500] + "..."
                if len(result.content) > 500
                else result.content
            ),
            "metadata": result.metadata,
        }

    return app
