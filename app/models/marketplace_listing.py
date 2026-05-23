from pydantic import BaseModel


class MarketplaceListing(BaseModel):
    listing_id: int
    seller_id: int
    item_id: int
    price: float
    is_active: bool = True
