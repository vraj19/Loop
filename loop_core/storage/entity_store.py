import json
from loop_core.storage.database import get_connection
from loop_core.memory.entity import Entity

def insert_entity(entity: Entity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO entities (id, name, type, metadata)
        VALUES (?, ?, ?, ?)
        """,
        (entity.id, entity.name, entity.type, json.dumps(entity.metadata)),
    )

    cursor.execute(
        """
        INSERT INTO entities_fts (id, name)
        VALUES (?, ?)
        """,
        (entity.id, entity.name),
    )

    conn.commit()
    conn.close()