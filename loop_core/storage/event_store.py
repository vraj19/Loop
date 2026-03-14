import json
from loop_core.storage.database import get_connection
from loop_core.memory.event import Event

def insert_event(event: Event):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO events (id, timestamp, source, content, metadata)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            event.id,
            event.timestamp.isoformat(),
            event.source,
            event.content,
            json.dumps(event.metadata),
        ),
    )

    conn.commit()
    conn.close()