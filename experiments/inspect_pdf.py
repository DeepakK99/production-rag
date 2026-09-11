from pathlib import Path

from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_from_json, elements_to_json

PDF_PATH = Path("data/Indian Recipes.pdf")
JSON_CACHE_PATH = Path("data/Indian_Recipes.json")

# 1. Check if the readable JSON file already exists
if JSON_CACHE_PATH.exists():
    print("⚡ Loading elements instantly from local JSON cache...")
    elements = elements_from_json(filename=str(JSON_CACHE_PATH))
else:
    print("⏳ Cache empty. Parsing PDF using hi_res strategy (takes a moment)...")
    elements = partition_pdf(
        filename=str(PDF_PATH),
        strategy="hi_res",
    )

    # Ensure the directory exists and save the elements as a JSON file
    JSON_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    elements_to_json(elements, filename=str(JSON_CACHE_PATH))
    print(f"✅ Successfully parsed and saved cache to: {JSON_CACHE_PATH}")

from dataclasses import dataclass


@dataclass
class DocumentElement:
    text: str
    element_type: str
    page_number: int | None
    metadata: dict


for i, element in enumerate(elements):
    # if "carrot halva" in str(element).lower() and type(element).__name__ == "Title":
    if 1148 <= i <= 1168:
        print(f"\n--- Element {i} ---")
        print(f"Type: {type(element).__name__}")
        print(f"Text: {str(element)[:200]}")
        print(f"Metadata: {element.metadata.to_dict()}")
