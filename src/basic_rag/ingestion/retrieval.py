# from typing import Callable
# from basic_rag.data import data 
# from pathlib import Path
# from ingestion.file_reader import reading_from_data_dir

text_for_chunking = """
Run this on a small test string to verify before plugging it into your RAG pipeline — e.g. chunking_data("a" * 2500, 1000, 150) should give you 3 chunks with sizes 1000, 1000, 500.
My honest suggestion: hand-rolling chunkers is a good learning exercise, but for a real RAG project use RecursiveCharacterTextSplitter from LangChain or semantic-text-splitter — they handle edge cases (splitting mid-word, mid-paragraph, overlap bookkeeping) that this simple version won't."""
  

def chunking_data(text = text_for_chunking, text_window = 50, overlap = 15) -> list[int]: 
    result = []
    start = 0

    while start < len(text): 
        end = min(start + text_window, len(text))
        
        result.append(text[start : end])
        start = text_window - overlap
  
    return result

if __name__ == "__main__": 
    output = chunking_data()
    for t in output: 
        print(t)