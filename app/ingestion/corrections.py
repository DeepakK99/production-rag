RECIPE_CORRECTIONS = {
    "11.2 Egg cooked with Meat and Fried (Nargisi": (
        "11.2 Egg cooked with Meat and Fried (Nargisi kofta)"
    ),
}


def correct_recipe_name(recipe: str | None) -> str | None:
    if recipe is None:
        return None

    return RECIPE_CORRECTIONS.get(recipe, recipe)
