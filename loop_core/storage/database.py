import sqlite3
from pathlib import Path

DB_PATH = Path("loop.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            faiss_id INTEGER UNIQUE,
            timestamp TEXT NOT NULL,
            source TEXT,
            content TEXT,
            metadata TEXT,
            embedding BLOB
        )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            metadata TEXT
        )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relations (
            id TEXT PRIMARY KEY,
            subject_entity TEXT NOT NULL,
            relation_type TEXT NOT NULL,
            object_entity TEXT NOT NULL,
            event_id TEXT,

            FOREIGN KEY(subject_entity) REFERENCES entities(id),
            FOREIGN KEY(object_entity) REFERENCES entities(id),
            FOREIGN KEY(event_id) REFERENCES events(id)
        )
        """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_subject ON relations(subject_entity)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_object ON relations(object_entity)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_event ON relations(event_id)")


    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS events_fts USING fts5(
            id,
            content
        )
        """)
    conn.commit()
    conn.close()