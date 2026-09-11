from pathlib import Path

from unstructured.partition.pdf import partition_pdf

from app.ingestion.cache import ElementCache
from app.ingestion.models import DocumentElement

cache = ElementCache()


def parse_pdf(path: Path) -> list[DocumentElement]:
    cached_elements = cache.load(path)
    if cached_elements is not None:
        print("Elements found in cache, using it")
        elements = cached_elements
    else:
        print("Elements not found in cache, parsing it")
        elements = partition_pdf(
            filename=str(path),
            strategy="hi_res",
        )
        cache.store(elements, Path)

    result = []

    for element in elements:
        metadata = element.metadata.to_dict()

        result.append(
            DocumentElement(
                text=str(element),
                element_type=type(element).__name__,
                page_number=metadata.get("page_number"),
                metadata=metadata,
            )
        )

    return result


if __name__ == "__main__":
    file_path = Path("data/Indian Recipes.pdf")
    elements = parse_pdf(file_path)
    print(elements[:5])
