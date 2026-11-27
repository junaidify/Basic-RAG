from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunking_data(text: str, text_window: int = 500, overlap: int = 50) -> list[str]: 
    result = []
    start = 0

    while start < len(text): 
        end = min(start + text_window, len(text))
        result.append(text[start:end])
        start = start + text_window - overlap
  
    return result


def chunking_using_langchain(text: str, chunk_size: int = 200, chunk_overlap: int = 30) -> list[str]: 
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    return splitter.split_text(text)
