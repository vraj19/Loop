from pydantic import BaseModel, Field
import uuid

class Relation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    subject_entity: str
    relation_type: str
    object_entity: str

    event_id: str | None = None  # Optional link to an event that supports this relation