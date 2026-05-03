import json
import uuid

import numpy as np

from loop_core.storage.database import get_connection
from loop_core.embeddings.embedding_model import get_embedding
from loop_core.embeddings.loader import get_faiss_index


from loop_core.memory.event import Event

def get_next_faiss_id(cursor):
    cursor.execute("SELECT MAX(faiss_id) FROM events")
    result = cursor.fetchone()
    max_id = result[0] if result[0] is not None else 0
    return max_id + 1


def fetch_events_by_ids(event_ids):
    if not event_ids:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ",".join("?" for _ in event_ids)
    query = f"""
        SELECT *
        FROM events
        WHERE id IN ({placeholders})
    """
    cursor.execute(query, event_ids)
    rows = cursor.fetchall()
    conn.close()

    id_to_row = {row["id"]: row for row in rows}
    return [id_to_row[event_id] for event_id in event_ids if event_id in id_to_row]
    

def insert_event(event: Event):
    conn = get_connection()
    cursor = conn.cursor()

    # Add embedding and faiss_id if content is not empty
    embedding = get_embedding(event.content) if event.content else None
    embedding_bytes = np.array(embedding, dtype=np.float32).tobytes() if embedding else None
    faiss_id = get_next_faiss_id(cursor) if embedding else None

    cursor.execute(
        """
        INSERT INTO events (id,faiss_id, timestamp, source, content, metadata, embedding)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event.id,
            faiss_id,
            event.timestamp.isoformat(),
            event.source,
            event.content,
            json.dumps(event.metadata),
            embedding_bytes
        ),
    )

    # FTS
    cursor.execute(
        """
        INSERT INTO events_fts (id, content)
        VALUES (?, ?)
        """,
        (
            event.id,
            event.content
        ),
    )
    conn.commit()
    conn.close()

    get_faiss_index().add(embedding, faiss_id)
