from pydantic import BaseModel, Field
import uuid


class Entity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: str
    metadata: dict = {}