from app.ingestion.grouping import group_by_recipe
from app.ingestion.models import DocumentElement


def test_group_elements_by_recipe():
    elements = [
        DocumentElement(
            text="Recipe A",
            element_type="Title",
            page_number=1,
            metadata={
                "chapter": "Chapter 1",
                "recipe_name": "Recipe A",
                "recipe_number": "1.1",
                "section": None,
            },
        ),
        DocumentElement(
            text="Ingredient A",
            element_type="Table",
            page_number=1,
            metadata={
                "chapter": "Chapter 1",
                "recipe": "1.1 Recipe A",
                "recipe_name": "Recipe A",
                "recipe_number": "1.1",
                "section": None,
            },
        ),
        DocumentElement(
            text="Recipe B",
            element_type="Title",
            page_number=2,
            metadata={
                "chapter": "Chapter 1",
                "recipe_name": "Recipe B",
                "recipe_number": "1.2",
                "section": None,
            },
        ),
        DocumentElement(
            text="Method B",
            element_type="ListItem",
            page_number=2,
            metadata={
                "chapter": "Chapter 1",
                "recipe_name": "Recipe B",
                "recipe_number": "1.2",
                "section": "Method",
            },
        ),
    ]

    recipes = group_by_recipe(elements)

    assert len(recipes) == 2

    assert recipes[0].recipe_name == "Recipe A"
    assert recipes[0].recipe_number == "1.1"
    assert len(recipes[0].elements) == 2

    assert recipes[1].recipe_name == "Recipe B"
    assert recipes[1].recipe_number == "1.2"
    assert len(recipes[1].elements) == 2
