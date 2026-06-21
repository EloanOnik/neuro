from pydantic import BaseModel

class UserUtterance(BaseModel):
    text: str