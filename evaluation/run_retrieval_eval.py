import json
from pathlib import Path

from app.database import SessionLocal
from app.evaluation.retrieval import mean_reciprocal_rank, recall_at_k, precision_at_k
from app.ingestion.embedding import OllamaEmbeddingProvider
from app.retrieval.hybrid import search_hybrid_chunks
from app.reranking.cross_encoder import CrossEncoderReranker

DATASET_PATH = Path(__file__).parent / "golden_dataset.json"

embedding_provider = OllamaEmbeddingProvider(
    model="nomic-embed-text:latest",
)

reranker = CrossEncoderReranker(
    model="cross-encoder/ms-marco-MiniLM-L-6-v2",
)


def load_dataset() -> list[dict]:
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_question(
    session,
    question_data: dict,
    k: int = 50,
    l: int = 5,
) -> float:
    question = question_data["question"]
    relevant = question_data["relevant"]

    query_embedding = embedding_provider.embed(question)

    results = search_hybrid_chunks(
        session=session,
        query=question,
        query_embedding=query_embedding,
    )

    reranked = reranker.rerank(
        query=question,
        results=results,
    )[:l]

    recall = recall_at_k(
        results=reranked,
        relevant=relevant,
        k=k,
    )
    precision = precision_at_k(
        results=reranked,
        relevant=relevant,
        k=5,
    )

    print(f"\nQuestion: {question}")
    print(f"Recall@{k}: {recall:.2f}")
    print(f"Precision@{k}: {precision:.2f}")

    # print("Retrieved:")

    # for rank, result in enumerate(results, start=1):
    #     metadata = result.chunk.metadata_

    #     print(
    #         f"  {rank}. "
    #         f"{metadata.get('recipe_number')} "
    #         f"{metadata.get('recipe_name')} "
    #         f"[{metadata.get('section')}] "
    #         f"score={result.score:.4f}"
    #     )

    return recall, precision, reranked


def main():
    k = 50
    dataset = load_dataset()

    recall_scores = []
    precision_scores = []
    all_results = []
    all_relevant = []

    with SessionLocal() as session:
        for question_data in dataset:
            if question_data["answerable"] == False:
                continue
            recall, precision, results = evaluate_question(
                session=session,
                question_data=question_data,
                k=k,
            )

            recall_scores.append(recall)
            precision_scores.append(precision)
            all_results.append(results)
            all_relevant.append(question_data["relevant"])

    average_recall = sum(recall_scores) / len(recall_scores)
    average_precision = sum(precision_scores) / len(precision_scores)

    mrr = mean_reciprocal_rank(
        all_results=all_results,
        all_relevant=all_relevant,
    )

    print("\n====================")
    print(f"Average Recall@{k}: {average_recall:.2f}")
    print(f"Average Precision@{k}: {average_precision:.2f}")
    print(f"MRR: {mrr:.2f}")
    print("====================")


if __name__ == "__main__":
    main()
