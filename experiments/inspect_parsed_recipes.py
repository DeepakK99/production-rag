from app.ingestion.chunker import build_chunks
from app.ingestion.grouping import group_by_recipe
from app.ingestion.normalizer import normalize_elements
from app.ingestion.parser import parse_pdf

elements = parse_pdf("data/Indian Recipes.pdf")
normalized_and_deduped_elements = normalize_elements(elements)
recipes = group_by_recipe(normalized_and_deduped_elements)

recipe = next(
    recipe
    for recipe in recipes
    if recipe.recipe_name == "Cauliflower and Potatoes (Aloo Gobi)"
)

chunks = build_chunks(recipe)

for chunk in chunks:
    print("=" * 80)
    print("INDEX:", chunk.chunk_index)
    print("SECTION:", chunk.section)
    print("PAGES:", chunk.pages)
    print(chunk.content)
