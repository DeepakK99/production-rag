from app.retrieval.models import RetrievalResult


def build_context(results: list[RetrievalResult]) -> str:
    context_parts = []

    for index, result in enumerate(results, start=1):
        chunk = result.chunk

        context_parts.append(
            "\n".join(
                [
                    f"[Source {index}]",
                    f"Recipe: {chunk.metadata_['recipe_name']}",
                    f"Section: {chunk.metadata_['section']}",
                    f"Pages: {', '.join(map(str, chunk.metadata_['pages']))}",
                    f"Score: {result.score:.4f}",
                    "",
                    chunk.content,
                ]
            )
        )

    return "\n\n".join(context_parts)
