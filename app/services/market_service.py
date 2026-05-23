from services.listing_service import ListingService
from services.user_service import UserService
from services.item_service import ItemService


class MarketService:

    def __init__(self):
        self.listing_service = ListingService()
        self.user_service = UserService()
        self.item_service = ItemService()

    def buy_listing(self, listing_id: int, buyer_id: int) -> dict:
        listing = self.listing_service.get_listing_by_id(listing_id)
        if not listing:
            raise ValueError(f"Listing {listing_id} does not exist.")

        if not listing["active"]:
            raise ValueError(f"Listing {listing_id} is no longer active.")

        seller_id = listing["seller_id"]
        if buyer_id == seller_id:
            raise ValueError("You cannot buy your own listing.")

        buyer = self.user_service.get_user_by_id(buyer_id)
        if not buyer:
            raise ValueError(f"Buyer {buyer_id} does not exist.")

        seller = self.user_service.get_user_by_id(seller_id)
        if not seller:
            raise ValueError(f"Seller {seller_id} does not exist.")

        price = listing["price"]
        if buyer["balance"] < price:
            raise ValueError(
                f"Insufficient balance. Need ${price}, have ${buyer['balance']}."
            )

        self.user_service.remove_balance(price, buyer_id)
        self.user_service.add_balance(price, seller_id)

        item_id = listing["item_id"]
        self.item_service.transfer_ownership(item_id, buyer_id)

        self.listing_service.deactivate_listing(listing_id)

        return {
            "listing_id": listing_id,
            "item_id": item_id,
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "price": price,
        }
