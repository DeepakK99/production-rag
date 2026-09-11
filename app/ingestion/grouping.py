from app.ingestion.models import DocumentElement, RecipeDocument


def group_by_recipe(
    elements: list[DocumentElement],
) -> list[RecipeDocument]:
    recipes = []

    current_recipe_name = None
    current_recipe_number = None
    current_chapter_number = None
    current_chapter_title = None
    current_elements = []

    for element in elements:
        recipe_number = element.metadata.get("recipe_number")
        recipe_name = element.metadata.get("recipe_name")
        chapter_number = element.metadata.get("chapter_number")
        chapter_title = element.metadata.get("chapter_title")

        if recipe_name is None:
            continue

        if current_recipe_name is None:
            current_recipe_name = recipe_name
            current_recipe_number = recipe_number
            current_chapter_number = chapter_number
            current_chapter_title = chapter_title

        elif recipe_name != current_recipe_name:
            recipes.append(
                RecipeDocument(
                    recipe_number=current_recipe_number,
                    recipe_name=current_recipe_name,
                    chapter_number=current_chapter_number,
                    chapter_title=current_chapter_title,
                    elements=current_elements,
                )
            )

            current_recipe_name = recipe_name
            current_recipe_number = recipe_number
            current_chapter_number = chapter_number
            current_chapter_title = chapter_title
            current_elements = []

        current_elements.append(element)

    if current_recipe_name is not None:
        recipes.append(
            RecipeDocument(
                recipe_number=current_recipe_number,
                recipe_name=current_recipe_name,
                chapter_number=current_chapter_number,
                chapter_title=current_chapter_title,
                elements=current_elements,
            )
        )

    return recipes
