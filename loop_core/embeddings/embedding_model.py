from sentence_transformers import SentenceTransformer  
from loop_core.config import EMBEDDING_MODEL

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embedding_model

def get_embedding(text: str):
    model = get_embedding_model()
    return model.encode(text).tolist()