from app.ingestion.models import Chunk, DocumentElement, RecipeDocument


def build_element_text(
    recipe_document: RecipeDocument,
) -> str:
    parts = []

    for element in recipe_document.elements:
        text = element.text.strip()

        if not text:
            continue

        parts.append(text)

    return "\n".join(parts)


def group_elements_by_section(
    recipe_document: RecipeDocument,
) -> dict[str, list[DocumentElement]]:
    sections: dict[str, list[DocumentElement]] = {}

    for element in recipe_document.elements:
        section = element.metadata.get("section")

        if section is None and element.element_type == "Table":
            section = "Ingredients"

        if section is None:
            continue

        sections.setdefault(section, []).append(element)

    return sections


def build_chunks(
    recipe_document: RecipeDocument,
) -> list[Chunk]:
    sections = group_elements_by_section(recipe_document)

    chunks = []

    for chunk_index, (section, elements) in enumerate(sections.items()):
        content_parts = [
            f"Chapter: {recipe_document.chapter_title}",
            f"Recipe: {recipe_document.recipe_name}",
            f"Section: {section}",
            "",
        ]

        pages = set()

        for element in elements:
            text = element.text.strip()

            if not text:
                continue

            if text.isdigit() and len(text) <= 3:
                continue

            if element.element_type == "Title" and text.lower() == section.lower():
                continue

            content_parts.append(text)

            if element.page_number is not None:
                pages.add(element.page_number)

        content = "\n".join(content_parts)

        chunks.append(
            Chunk(
                content=content,
                chunk_index=chunk_index,
                recipe_number=recipe_document.recipe_number,
                recipe_name=recipe_document.recipe_name,
                chapter_number=recipe_document.chapter_number,
                chapter_title=recipe_document.chapter_title,
                section=section,
                pages=sorted(pages),
            )
        )

    return chunks
