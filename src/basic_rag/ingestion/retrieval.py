from basic_rag.ingestion.embedding import embed_model
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def create_vector_store(chunks: list[str | Document]):
    if not chunks:
        raise ValueError("Cannot create a vector store from empty chunks.")

    if isinstance(chunks[0], Document):
        return FAISS.from_documents(
            documents=chunks,
            embedding=embed_model
        )
    return FAISS.from_texts(
        texts=chunks,
        embedding=embed_model
    )


def retrieval_input(vector_store, question: str | None = None, k: int = 3, score_threshold: float | None = None):
    if not question:
        question = input("Enter your question: ")
        
    results_with_scores = vector_store.similarity_search_with_score(
        query=question,
        k=k
    )

    if score_threshold is not None:
        matched = [
            (doc, score) for doc, score in results_with_scores if score <= score_threshold
        ]
    else:
        matched = results_with_scores

    return question, matched
