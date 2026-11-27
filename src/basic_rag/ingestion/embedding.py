import numpy as np 
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings

MODEL_NAME = 'all-MiniLM-L6-v2'

_model = None

def get_model(): 
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    
    return _model


def embed_chunks(chunks: list[str]) -> np.ndarray: 
    model = get_model()
    embeddings = model.encode(
        chunks, 
        normalize_embeddings=False, 
        show_progress_bar=True
    )

    return embeddings


embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def embed_chunks_using_langchain(chunks):
    return embed_model.embed_documents(chunks)