import faiss
import numpy as np
from pathlib import Path
from loop_core.config import EMBEDDING_DIM, FAISS_INDEX_PATH

INDEX_PATH = Path(FAISS_INDEX_PATH)

class FaissIndex:
    def __init__(self):

        if INDEX_PATH.exists():
            self.index = faiss.read_index(str(INDEX_PATH))
        else:
            base_index = faiss.IndexFlatIP(EMBEDDING_DIM)
            self.index = faiss.IndexIDMap(base_index)

    def add(self, embedding: list, faiss_id: int):
        vector = np.array([embedding], dtype=np.float32) 
        faiss.normalize_L2(vector)
        ids = np.array([faiss_id], dtype=np.int64)
        self.index.add_with_ids(vector, ids)

    def search(self, query_embedding: list, top_k: int):
        vector = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(vector)
        distances, indices = self.index.search(vector, top_k)
        return indices[0]
    
    def save(self):
        faiss.write_index(self.index, str(INDEX_PATH))