from basic_rag.ingestion.chunking import chunking_data, chunking_using_langchain
from basic_rag.ingestion.embedding import embed_chunks, embed_chunks_using_langchain

text_for_chunking = """
Run this on a small test string to verify before plugging it into your RAG pipeline — e.g. chunking_data("a" * 2500, 1000, 150) should give you 3 chunks with sizes 1000, 1000, 500.
My honest suggestion: hand-rolling chunkers is a good learning exercise, but for a real RAG project use RecursiveCharacterTextSplitter from LangChain or semantic-text-splitter — they handle edge cases (splitting mid-word, mid-paragraph, overlap bookkeeping) that this simple version won't."""

def main(): 
    # chunks = chunking_data(text_for_chunking)
    chunks = chunking_using_langchain(text_for_chunking)
    embedding = embed_chunks_using_langchain(chunks)

    print(embedding)
