from basic_rag.data import data 
from pathlib import Path

SUPPORTED_EXTENSION = [".md", ".pdf", ".txt", ".docx"]

def read_pdf(file): 
def read_docx(file): 
def read_txt(file): 
def read_md(file): 


def reading_from_data_dir(data): 
    folder = Path(data)

    for i, file in enumerate(folder.rglob("*")): 
        curr_file = file.suffix.lower()
        if curr_file in SUPPORTED_EXTENSION: 

            if curr_file == ".pdf": 
                read_pdf(file)
            
            if curr_file == ".txt": 
                read_txt(file)
            
            if curr_file == ".docx": 
                read_docx(file)
            
            if curr_file == ".md": 
                read_md(file)

                

    

def chunking_data(text, text_window: 1000, overlap: 150) -> list[int]: 
    result = []

    start = 0

    while len(text) > text_window: 
        chunk = text.split(start, text_window - start)
        
        result.append(chunk)
        start = chunk - overlap

        
    return result


    