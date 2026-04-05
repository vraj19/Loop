import json
import uuid
from datetime import datetime, timezone
import numpy as np

from loop_core.storage.database import get_connection
from loop_core.embeddings.embedding_model import get_embedding
from loop_core.embeddings.loader import get_faiss_index

from loop_core.config import (
    TOP_K_CANDIDATES,
    FINAL_TOP_K,
    RRF_K,
    RECENCY_WEIGHT
)
from loop_core.memory.event import Event

def get_next_faiss_id(cursor):
    cursor.execute("SELECT MAX(faiss_id) FROM events")
    result = cursor.fetchone()
    max_id = result[0] if result[0] is not None else 0
    return max_id + 1

def get_recency_boost(timestamp):
    event_time = datetime.fromisoformat(timestamp)

    # ensure event_time is timezone-aware
    if event_time.tzinfo is None:
        event_time = event_time.replace(tzinfo=timezone.utc)
    
    now = datetime.now(timezone.utc)
    age_days = (now - event_time).days
    return 1 / (1 + age_days)

def _fetch_events_by_ids(event_ids):
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

# Keyword search

def get_keyword_ranking(query: str, top_k: int = TOP_K_CANDIDATES):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM events_fts
        WHERE content MATCH ?
        order by bm25(events_fts) 
        LIMIT ?
        """,
        (
            query,
            top_k
        ),
    )
    ids = [row['id'] for row in cursor.fetchall()]
    conn.close()
    return ids

# Semantic Search

def get_semantic_ranking(query: str, top_k: int = TOP_K_CANDIDATES):
    query_embedding = get_embedding(query)
    faiss_ids = get_faiss_index().search(query_embedding, top_k)

    faiss_ids = [int(fid) for fid in faiss_ids if fid != -1]
    if not faiss_ids:
        return []

    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ",".join("?" for _ in faiss_ids)

    cursor.execute(
        f"""
        SELECT id, faiss_id
        FROM events
        WHERE faiss_id IN ({placeholders})
        """,
        faiss_ids,
    )
    rows = cursor.fetchall()
    conn.close()

    faiss_id_to_event_id = {row['faiss_id']: row['id'] for row in rows}
    results = [faiss_id_to_event_id[fid] for fid in faiss_ids if fid in faiss_id_to_event_id]
    return results

# Hybrid search (RRF + Recency)

def hybrid_search(query: str, limit: int = FINAL_TOP_K):
    keyword_ids = get_keyword_ranking(query, TOP_K_CANDIDATES)
    semantic_ids = get_semantic_ranking(query, TOP_K_CANDIDATES)

    scores = {}

    # RRF - keyword
    for rank, event_id in enumerate(keyword_ids, start = 1):
        scores[event_id] = scores.get(event_id, 0) + 1 / (RRF_K + rank)
    
    # RRF - semantic
    for rank, event_id in enumerate(semantic_ids, start = 1):
        scores[event_id] = scores.get(event_id, 0) + 1 / (RRF_K + rank)

    # Get recency scores
    conn = get_connection()
    cursor = conn.cursor()

    event_ids = list(scores.keys())
    placeholders = ",".join("?" for _ in event_ids)

    cursor.execute(
        f"""
        SELECT id, timestamp
        FROM events
        WHERE id IN ({placeholders})
        """,
        event_ids,
    )
    rows = cursor.fetchall()
    
    id_to_timestamps = {row['id']: row['timestamp'] for row in rows}

    for event_id in scores:
        recency_score = get_recency_boost(id_to_timestamps[event_id])
        scores[event_id] += RECENCY_WEIGHT * recency_score

    conn.close()
    ranked = sorted(scores.items(), key = lambda x: x[1], reverse = True)
    top_ids = [event_id for event_id, score in ranked[:limit]]

    return _fetch_events_by_ids(top_ids)