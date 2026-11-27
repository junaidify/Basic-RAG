from pypdf import PdfReader
from docx import Document 
from typing import Callable
from pathlib import Path

SUPPORTED_EXTENSION = [".md", ".pdf", ".txt", ".docx"]
DIR_PATH = Path(__file__).resolve().parent.parent / "data"


def read_pdf(file: Path) -> list[dict]: 
    pages = []
    reader = PdfReader(str(file))

    for pages_num, page in enumerate(reader.pages): 
        text = page.extract_text() or ""
        if text.strip(): 
            pages.append({
                "text": text.strip(), 
                "metadata": {
                    "source": file.name,
                    "page_number": pages_num, 
                    "file_type": "PDF"
                }
            })
    return pages      


def read_md(file: Path) -> list[dict]: 
    text = file.read_text(encoding="utf-8")   
    if not text.strip(): 
        return []

    return [{
        "text": text.strip(), 
        "metadata": {
            "source": file.name,
            "section": None, 
            "file_type": "markdown"
        }
    }]  


def read_docx(file: Path) -> list[dict]: 
    document = Document(str(file))
    content = []

    for para_num, paragraph in enumerate(document.paragraphs):
        if paragraph.text.strip(): 
            content.append({
                "text": paragraph.text.strip(), 
                "metadata": {
                    "source": file.name, 
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
            if row_text:
                content.append({
                    "text": " | ".join(row_text), 
                    "metadata": {
                        "source": file.name, 
                        "table_number": table_num, 
                        "file_type": "docx"
                    }
                })

    return content


def read_txt(file: Path) -> list[dict]: 
    with open(file, "r", encoding="utf-8", errors="replace") as f: 
        text = f.read()
    if not text.strip():
        return []
    return [{
        "text": text.strip(), 
        "metadata": {
            "source": file.name, 
            "section": None,
            "file_type": "txt"
        }
    }]


file_reader: dict[str, Callable[[Path], list[dict]]] = {
    ".pdf": read_pdf, 
    ".md": read_md, 
    ".docx": read_docx, 
    ".txt": read_txt
}


def reading_from_data_dir(data: Path = DIR_PATH) -> list[dict]: 
    documents = []
    folder = Path(data)

    if not folder.exists():
        return documents

    for file in folder.rglob("*"): 
        if not file.is_file(): 
            continue

        reader = file_reader.get(file.suffix.lower())
        if reader is None: 
            continue

        docs = reader(file)
        if docs:
            documents.extend(docs)
        
    return documents
