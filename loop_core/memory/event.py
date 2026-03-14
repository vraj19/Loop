from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: str
    content: str
    metadata: dict = {}