from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunking_data(text: str, text_window = 50, overlap = 15) -> list[str]: 
    result = []
    start = 0

    while start < len(text): 
        end = min(start + text_window, len(text))
        
        result.append(text[start : end])
        start = start + text_window - overlap
  
    return result



def chunking_using_langchain(text: str): 
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 50, 
        chunk_overlap = 15
    )

    return splitter.split_text(text)
