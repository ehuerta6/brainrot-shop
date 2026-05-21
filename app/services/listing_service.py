from models.marketplace_listing import MarketplaceListing
from repositories.listing_repo import ListingRepo
from repositories.item_repo import ItemRepo


class ListingService:
    def __init__(self):
        self.listing_repo = ListingRepo()
        self.item_repo = ItemRepo()

    def create_listing(self, item_id: int, seller_id: int, price: float) -> dict:
        if price <= 0:
            raise ValueError("Price must be greater than zero.")

        item = self.item_repo.get_item_by_id(item_id)
        if item is None:
            raise ValueError(f"Item {item_id} does not exist.")

        if item["owner_id"] != seller_id:
            raise ValueError(f"Seller {seller_id} does not own item {item_id}.")

        if item["is_listed"]:
            raise ValueError(f"Item {item_id} is already listed.")

        next_id = self.generate_next_id()

        new_listing = MarketplaceListing(
            listing_id=next_id,
            seller_id=seller_id,
            item_id=item_id,
            price=price,
        )

        self.item_repo.update_item(item_id, {"is_listed": True})
        return self.listing_repo.save_listing(new_listing)

    def get_active_listings(self) -> list[dict]:
        return self.listing_repo.get_active_listings()

    def cancel_listing(self, listing_id: int) -> bool:
        listing = self.listing_repo.get_listing_by_id(listing_id)
        if listing is None:
            return False

        self.listing_repo.update_listing(listing_id, {"active": False})
        self.item_repo.update_item(listing["item_id"], {"is_listed": False})
        return True

    def generate_next_id(self) -> int:
        listings = self.listing_repo.get_all_listings()
        if not listings:
            return 1
        return max(listing["listing_id"] for listing in listings) + 1
