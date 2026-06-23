from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Optional


class Message(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid4()))
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None # если актор не ждет ответа, но получатель хочет ответить


class UserUtterance(Message):
    text: str
    timestamp: float

# ShutdownCommand — системное сообщение: 
# «актор, выйди из цикла, закончи работу». 
# Оно обрабатывается прямо в _run() базового класса 
# и не доходит до receive().
class ShutdownCommand(Message):
    pass
