from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int
    username: str = Field(min_length=5, max_length=20)
    balance: float = Field(ge=0)
