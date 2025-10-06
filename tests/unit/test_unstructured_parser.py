from pathlib import Path
from nexa.adapters.parsers.unstructured_parser import UnstructuredDocumentParser

def test_parse_pdf():
    parser = UnstructuredDocumentParser()
    test_file = Path(__file__).parent / "fixtures" / "sample.pdf"
    result = parser.parse(test_file)
    assert result.file_type == "pdf"
    assert len(result.content) > 0
    assert "element_count" in result.metadata