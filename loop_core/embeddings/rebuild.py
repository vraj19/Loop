from loop_core.config import EMBEDDING_DIM
from loop_core.storage.database import get_connection
from loop_core.embeddings.faiss_index import FaissIndex
import numpy as np


def rebuild_faiss_index():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT faiss_id, embedding FROM events WHERE embedding IS NOT NULL""")
    rows = cursor.fetchall()

    if rows:
        first_emb = np.frombuffer(rows[0]["embedding"], dtype=np.float32)
        actual_dim = len(first_emb)

        if actual_dim != EMBEDDING_DIM:
            raise ValueError(
                f"Dimension mismatch! Expected {EMBEDDING_DIM}, got {actual_dim}"
            )

    if not rows:
        print("No embeddings found in the database.")
        return

    faiss_index = FaissIndex()

    for row in rows:
        faiss_id = row["faiss_id"]
        embedding = np.frombuffer(row["embedding"], dtype=np.float32).tolist()
        faiss_index.add(embedding, faiss_id)

    faiss_index.save()
    conn.close()
    print(f"Rebuilt Faiss index with {len(rows)} embeddings.")
    return faiss_index