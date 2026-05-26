from services.listing_service import ListingService
from services.user_service import UserService
from services.item_service import ItemService
from exceptions.listing_error import ListingNotFoundError, ListingInactiveError
from exceptions.market_error import CannotBuyOwnListingError
from exceptions.user_error import UserNotFoundError, InsufficientBalanceError


class MarketService:

    def __init__(self):
        self.listing_service = ListingService()
        self.user_service = UserService()
        self.item_service = ItemService()

    # ── public API ──────────────────────────────────────────────

    def buy_listing(self, listing_id: int, buyer_id: int) -> dict:
        listing = self.listing_service.get_listing_by_id(listing_id)
        if not listing:
            raise ListingNotFoundError(listing_id)

        self._validate_purchase(listing, buyer_id)

        seller_id = listing["seller_id"]
        price = listing["price"]
        item_id = listing["item_id"]

        try:
            self._transfer_funds(price, buyer_id, seller_id)
            self._transfer_item(item_id, buyer_id)
            self._close_listing(listing_id)
        except Exception as e:
            print(
                f"CRITICAL: purchase partially failed "
                f"[listing={listing_id}, buyer={buyer_id}]: {e}"
            )
            raise

        return {
            "listing_id": listing_id,
            "item_id": item_id,
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "price": price,
        }

    # ── private helpers ─────────────────────────────────────────

    def _validate_purchase(self, listing: dict, buyer_id: int) -> None:
        if not listing["is_active"]:
            raise ListingInactiveError(listing["listing_id"])

        seller_id = listing["seller_id"]
        if buyer_id == seller_id:
            raise CannotBuyOwnListingError()

        buyer = self.user_service.get_user_by_id(buyer_id)
        if not buyer:
            raise UserNotFoundError(buyer_id)

        seller = self.user_service.get_user_by_id(seller_id)
        if not seller:
            raise UserNotFoundError(seller_id)

        price = listing["price"]
        if buyer["balance"] < price:
            raise InsufficientBalanceError(buyer_id, buyer["balance"], price)

    def _transfer_funds(
        self, price: float, buyer_id: int, seller_id: int
    ) -> None:
        self.user_service.remove_balance(price, buyer_id)
        self.user_service.add_balance(price, seller_id)

    def _transfer_item(self, item_id: int, buyer_id: int) -> None:
        self.item_service.transfer_ownership(item_id, buyer_id)

    def _close_listing(self, listing_id: int) -> None:
        self.listing_service.deactivate_listing(listing_id)
