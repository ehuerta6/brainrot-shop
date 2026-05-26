from models.marketplace_listing import MarketplaceListing
from repositories.listing_repo import ListingRepo
from repositories.item_repo import ItemRepo
from exceptions.listing_error import ListingNotFoundError, ListingInactiveError, InvalidPriceError
from exceptions.item_error import ItemNotFoundError, ItemInvalidOwnershipError, ItemAlreadyListedError


class ListingService:
    def __init__(self):
        self.listing_repo = ListingRepo()
        self.item_repo = ItemRepo()

    def create_listing(self, item_id: int, seller_id: int, price: float) -> dict:
        if price <= 0:
            raise InvalidPriceError()

        item = self.item_repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError(item_id)

        if item["owner_id"] != seller_id:
            raise ItemInvalidOwnershipError(item_id, seller_id)

        if item["is_listed"]:
            raise ItemAlreadyListedError(item_id)

        next_listing_id = self.generate_next_listing_id()

        new_listing = MarketplaceListing(
            listing_id=next_listing_id,
            seller_id=seller_id,
            item_id=item_id,
            price=price,
        )

        self.item_repo.update_item(item_id, {"is_listed": True})
        return self.listing_repo.save_listing(new_listing)

    def get_active_listings(self) -> list[dict]:
        return self.listing_repo.get_active_listings()

    def get_listing_by_id(self, listing_id: int) -> dict | None:
        return self.listing_repo.get_listing_by_id(listing_id)

    def deactivate_listing(self, listing_id: int) -> bool:
        listing = self.listing_repo.get_listing_by_id(listing_id)
        if listing is None:
            return False
        self.listing_repo.update_listing(listing_id, {"is_active": False})
        return True

    def cancel_listing(self, listing_id: int) -> bool:
        listing = self.listing_repo.get_listing_by_id(listing_id)
        if listing is None:
            return False

        self.listing_repo.update_listing(listing_id, {"is_active": False})
        self.item_repo.update_item(listing["item_id"], {"is_listed": False})
        return True

    def generate_next_listing_id(self) -> int:
        listings = self.listing_repo.get_all_listings()
        if not listings:
            return 1
        return max(listing["listing_id"] for listing in listings) + 1
