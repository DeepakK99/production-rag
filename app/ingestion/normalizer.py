import re
from dataclasses import replace

from app.ingestion.models import DocumentElement


def is_running_recipe_header(
    text: str,
    current_recipe_number: str | None,
    element_type: str,
) -> bool:
    if element_type not in {"Text", "ListItem", "NarrativeText"}:
        return False

    if current_recipe_number is None:
        return False

    match = re.match(
        r"^(\d+\.\d+)\.?\s+",
        text,
    )

    if not match:
        return False

    return match.group(1) != current_recipe_number


def parse_chapter(text: str) -> tuple[int, str | None] | None:
    full_match = re.match(
        r"^chapter\s+(\d+)\.\s*(.+)$",
        text.strip(),
        re.IGNORECASE,
    )

    if full_match:
        return (
            int(full_match.group(1)),
            full_match.group(2).strip(),
        )

    chapter_match = re.match(
        r"^chapter\s+(\d+)\s*$",
        text.strip(),
        re.IGNORECASE,
    )

    if chapter_match:
        return int(chapter_match.group(1)), None

    return None


def parse_recipe_title(text: str) -> tuple[str, str] | None:
    match = re.match(
        r"^(\d+\.\d+)\.?\s+(.+)$",
        text.strip(),
    )

    if not match:
        return None

    return match.group(1), match.group(2).strip()


def deduplicate_elements(
    elements: list[DocumentElement],
) -> list[DocumentElement]:
    """
    Remove consecutive duplicate elements based on normalized text.

    The first occurrence is preserved.
    """

    if not elements:
        return []

    deduplicated = [elements[0]]

    for element in elements[1:]:
        previous = deduplicated[-1]

        if element.text.strip() == previous.text.strip():
            continue

        deduplicated.append(element)

    return deduplicated


def normalize_elements(
    elements: list[DocumentElement],
) -> list[DocumentElement]:
    """
    Normalize parser elements into application-level semantic metadata.

    The original DocumentElement instances and their metadata are not modified.

    Running page headers are intentionally not used to determine recipe context.
    """

    # ---------------------------------------------------------
    # Pass 1: Discover chapter number -> chapter title mapping
    # ---------------------------------------------------------

    chapter_titles: dict[int, str] = {}

    for element in elements:
        category = element.element_type
        text = element.text.strip()

        if category in {"Header", "Footer", "FigureCaption", "Image"}:
            continue

        chapter = parse_chapter(text)

        if category in {"Text", "NarrativeText", "Title"} and chapter and chapter[1]:
            chapter_number, chapter_title = chapter
            chapter_titles[chapter_number] = chapter_title

    # ---------------------------------------------------------
    # Pass 2: Build normalized application-level elements
    # ---------------------------------------------------------

    normalized_elements = []

    current_chapter_number = None
    current_chapter_title = None
    current_recipe_number = None
    current_recipe_name = None
    current_section = None

    recipe_regex = re.compile(
        r"^\d+\.\d+\.?\s+",
    )

    section_names = {
        "method",
        "directions",
        "instructions",
        "ingredients",
        "preparation",
    }

    keep_keys = {
        "filename",
        "filetype",
        "last_modified",
        "page_number",
        "parent_id",
    }

    for element in elements:
        category = element.element_type
        text = element.text.strip()

        # -----------------------------------------------------
        # 1. Noise Filter
        # -----------------------------------------------------

        if category in {"Header", "Footer", "FigureCaption", "Image"}:
            continue

        if is_running_recipe_header(
            text,
            current_recipe_number,
            category,
        ):
            continue
        # -----------------------------------------------------
        # 2. Chapter Identification
        # -----------------------------------------------------

        chapter = parse_chapter(text)

        if category in {"Text", "NarrativeText", "Title"} and chapter:
            if current_chapter_number == chapter[0]:
                continue
            current_chapter_number, _ = chapter

            current_chapter_title = chapter_titles.get(current_chapter_number)

            current_recipe_name = None
            current_recipe_number = None
            current_section = None

        # -----------------------------------------------------
        # 3. Recipe Title Identification
        # -----------------------------------------------------

        elif category == "Title" and recipe_regex.match(text):
            recipe = parse_recipe_title(text)

            if category == "Title" and recipe:
                current_recipe_number, current_recipe_name = recipe
                current_section = None
            current_section = None

        # -----------------------------------------------------
        # 4. Section Marker Identification
        # -----------------------------------------------------

        elif text.lower() in section_names:
            current_section = text

        # -----------------------------------------------------
        # 5. Keep only useful metadata
        # -----------------------------------------------------

        filtered_metadata = {
            key: element.metadata[key] for key in keep_keys if key in element.metadata
        }

        filtered_metadata["chapter_number"] = current_chapter_number
        filtered_metadata["chapter_title"] = current_chapter_title
        filtered_metadata["recipe_number"] = current_recipe_number
        filtered_metadata["recipe_name"] = current_recipe_name
        filtered_metadata["section"] = current_section

        # -----------------------------------------------------
        # 6. Create a new DocumentElement
        # -----------------------------------------------------

        cloned_element = replace(
            element,
            metadata=filtered_metadata,
        )

        normalized_elements.append(cloned_element)

    # ---------------------------------------------------------
    # 7. Remove consecutive parser duplicates
    # ---------------------------------------------------------

    return deduplicate_elements(normalized_elements)
