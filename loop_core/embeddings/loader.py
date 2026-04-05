from loop_core.embeddings.faiss_index import FaissIndex, INDEX_PATH
from loop_core.config import EMBEDDING_DIM
from loop_core.embeddings.rebuild import rebuild_faiss_index


def load_faiss():
    if INDEX_PATH.exists():
        return FaissIndex()
    else:
        print("Faiss index not found. Rebuilding...")
        return rebuild_faiss_index()
    

_faiss_index = None

def get_faiss_index():
    global _faiss_index

    if _faiss_index is None:
        _faiss_index = load_faiss()

    return _faiss_index