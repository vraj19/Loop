from loop_core.storage.database import get_connection
from loop_core.memory.relation import Relation


def insert_relation(relation: Relation):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO relations (id, subject_entity, relation_type, object_entity, event_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            relation.id,
            relation.subject_entity,
            relation.relation_type,
            relation.object_entity,
            relation.event_id,
        ),
    )

    conn.commit()
    conn.close()


def get_relations_by_subject(entity_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM relations
        WHERE subject_entity = ?
        """,
        (entity_id,),
    )

    results = cursor.fetchall()
    conn.close()
    return results

def get_relations_by_object(entity_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM relations
        WHERE object_entity = ?
        """,
        (entity_id,),
    )

    results = cursor.fetchall()
    conn.close()
    return results