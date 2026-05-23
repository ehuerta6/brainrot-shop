from pydantic import BaseModel


class Item(BaseModel):
    owner_id: int
    item_id: int
    is_listed: bool = False
    rarity: str
    item_name: str
    base_value: float
