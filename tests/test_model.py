from app.ingestion.models import DocumentElement


def test_document_element():
    element = DocumentElement(
        text="12.8 Carrot Halva",
        element_type="title",
        page_number=77,
    )

    assert element.text == "12.8 Carrot Halva"
    assert element.element_type == "title"
    assert element.page_number == 77
