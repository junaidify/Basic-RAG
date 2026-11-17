from typing import Callable
from basic_rag.data import data 
from pathlib import Path
from pypdf import PdfReader
from docx import Document 

SUPPORTED_EXTENSION = [".md", ".pdf", ".txt", ".docx"]


def reading_from_data_dir(data) -> list[dict]: 
    document = []
    folder = Path(data)

    for file in folder.rglob("*"): 
        if not file.is_file(): 
            continue

        reader = file_reader.get(file.suffix.lower())

        if reader is None: 
            continue

        document.append(reader(file))
        

file_reader: dict[str, Callable[[Path], list[dict]]] = {
    ".pdf" : read_pdf, 
    ".md": read_md, 
    ".docx": read_docx, 
    ".txt": read_txt
} 


def read_pdf(file) -> list[dict]: 
    pages = []
    reader = PdfReader(file)

    for pages_num, page in enumerate(reader.pages): 
        text = page.extract_text()

        if text.strip(): 
            pages.append({
                "text": text, 
                "metadata": {
                    "source": file.name,
                    "page_number": pages_num, 
                }
            })

    return pages      


def read_md(file) -> list[dict]: 
    text = file.read_text(encoding="utf8")   

    if not text.strip(): 
        return []

    return [{
        "text": text, 
        "metadata": {
            "source": file.name,
            "section": None
        }
    }]  


def read_docx(file) -> list[dict]: 
    document = Document(file)
    content = []

    for para_num, paragraph in enumerate(document.paragraphs):
        if paragraph.text.strip(): 
            content.append({
                "text": paragraph.text, 
                "metadata": {
                    "source": file, 
                    "paragraph": para_num, 
                    "file_type": "docx"
                }
            }) 

        
    for table_num, table in enumerate(document.tables): 
        for row in table.rows: 
            row_text = [
                cell.text.strip()
                for cell in row
                if cell.text.strip()
            ]

            content.append({
                "text": row_text, 
                "metadata": {
                    "source": file, 
                    "table_number": table_num, 
                    "file_type": "docx"
                }
            })

    return content




    

def chunking_data(text, text_window: 1000, overlap: 150) -> list[int]: 
    result = []
    start = 0

    while len(text) > text_window: 
        chunk = text.split(start, text_window - start)
        
        result.append(chunk)
        start = chunk - overlap
  
    return result


    