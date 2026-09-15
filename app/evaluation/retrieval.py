from app.models import Chunk

def is_relevant(
    chunk: Chunk,
    relevant: dict,
) -> bool:
    metadata = chunk.metadata_

    if metadata.get("recipe_number") != relevant["recipe_number"]:
        return False

    expected_section = relevant.get("section")

    if expected_section is None:
        return True

    return metadata.get("section") == expected_section


def recall_at_k(
    results: list,
    relevant: list[dict],
    k: int,
) -> float:
    top_results = results[:k]

    found = set()

    for expected in relevant:
        for result in top_results:
            if is_relevant(result.chunk, expected):
                found.add(
                    (
                        expected["recipe_number"],
                        expected.get("section"),
                    )
                )
                break

    return len(found) / len(relevant)


def reciprocal_rank(
    results: list,
    relevant: list[dict],
) -> float:
    for rank, result in enumerate(results, start=1):
        if any(is_relevant(result.chunk, expected) for expected in relevant):
            return 1 / rank

    return 0.0


def mean_reciprocal_rank(
    all_results: list[list],
    all_relevant: list[list[dict]],
) -> float:
    if not all_results:
        return 0.0

    scores = [
        reciprocal_rank(results, relevant)
        for results, relevant in zip(
            all_results,
            all_relevant,
            strict=True,
        )
    ]

    return sum(scores) / len(scores)

def precision_at_k(
    results: list,
    relevant: list[dict],
    k: int,
) -> float:
    top_results = results[:k]

    if not top_results:
        return 0.0

    relevant_found = sum(
        any(
            is_relevant(result.chunk, expected)
            for expected in relevant
        )
        for result in top_results
    )

    return relevant_found / len(top_results)
