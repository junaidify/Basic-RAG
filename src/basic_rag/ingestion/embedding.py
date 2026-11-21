import numpy as np 
from sentence-transformers import SentenceTransformer

MODEL_NAME = 'all-MiniLM-L6-v2'

_model = None

def get_model(): 
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    
    return _model


def embed_chunks(chunks: list[dict]) -> np.ndarray: 
    model = get_model()
    embeddings = model.encode(
        chunks, 
        normalize_embeddings=True, 
        show_progress_bar=True
    )

    return embeddings

