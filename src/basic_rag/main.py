from basic_rag.ingestion.chunking import chunking_using_langchain
from basic_rag.ingestion.retrieval import create_vector_store, retrieval_input
from basic_rag.ingestion.file_reader import reading_from_data_dir
from basic_rag.ingestion.model import generate_answer

sample_text_for_chunking = """
Java is an object-oriented programming language.

Spring Boot simplifies Java backend development.

Python is used for machine learning and artificial intelligence.

React is a JavaScript frontend library for building user interfaces.

FastAPI is a modern, fast web framework for building APIs with Python.
"""


def load_chunks() -> list[str]:
    raw_docs = reading_from_data_dir()

    if raw_docs:
        print(f"Loaded {len(raw_docs)} document(s) from data directory.")
        chunks = []
        for doc in raw_docs:
            text = doc.get("text", "")
            if text:
                chunks.extend(chunking_using_langchain(text))
        if chunks:
            return chunks

    print("No documents found in data directory. Using sample dataset.")
    # In the sample dataset, each line is an independent fact:
    return [line.strip() for line in sample_text_for_chunking.strip().split("\n") if line.strip()]


def main():
    print("\n--- Basic RAG Pipeline ---")
    chunks = load_chunks()
    print(f"Total chunks indexed: {len(chunks)}")

    print("Building vector store...")
    vector_store = create_vector_store(chunks)

    question, results = retrieval_input(vector_store, k=2, score_threshold=None)

    if not results:
        print(f"\n[!] No chunks retrieved for: '{question}'")
        return

    print(f"\nTop retrieved chunk(s):")
    context_parts = []
    for doc, score in results:
        confidence = "High" if score < 0.8 else ("Moderate" if score < 1.3 else "Low")
        print(f"\n  [Distance score: {score:.4f} | Confidence: {confidence}]")
        print(f"  {doc.page_content}")
        context_parts.append(doc.page_content)

    combined_context = "\n\n".join(context_parts)

    print("\n--- Generating Answer ---")
    generate_answer(question=question, context=combined_context)


if __name__ == "__main__":
    main()
