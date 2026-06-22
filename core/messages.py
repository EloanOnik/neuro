from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Optional


class Message(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid4()))
    correlation_id: Optional[str] = None


class UserUtterance(Message):
    text: str
    timestamp: float
