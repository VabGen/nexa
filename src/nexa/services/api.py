from typing import Any, Dict

from fastapi import Body, FastAPI, File, UploadFile

from ..adapters.ai.hf_grammar_refiner import HFGrammarRefiner
from ..adapters.parsers.unstructured_parser import UnstructuredDocumentParser
from ..core.use_cases.refine_text import RefineText
from ..interfaces.document_parser import DocumentParser


def create_app() -> FastAPI:
    app = FastAPI(title="Nexa Document AI", version="0.1.0")

    # Инициализация парсера
    parser: DocumentParser = UnstructuredDocumentParser()

    # Инициализация рефайнера (модель загрузится один раз)
    refiner = HFGrammarRefiner()
    text_refiner = RefineText(refiner=refiner)

    @app.post("/parse")
    async def parse_document(file: UploadFile = File(...)) -> Dict[str, Any]:
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

    @app.post("/refine")
    async def refine_text(raw_text: str = Body(..., embed=True)) -> Dict[str, Any]:
        refined = text_refiner.execute(raw_text)
        return {"refined_text": refined}

    return app
