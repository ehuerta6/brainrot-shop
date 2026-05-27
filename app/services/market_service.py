import logging

from services.listing_service import ListingService
from services.user_service import UserService
from services.item_service import ItemService
from exceptions.listing_error import ListingNotFoundError, ListingInactiveError
from exceptions.market_error import CannotBuyOwnListingError
from exceptions.user_error import UserNotFoundError, InsufficientBalanceError

logger = logging.getLogger(__name__)


class MarketService:

    def __init__(self):
        self.listing_service = ListingService()
        self.user_service = UserService()
        self.item_service = ItemService()

    def buy_listing(self, listing_id: int, buyer_id: int) -> dict:
        listing = self.listing_service.get_listing_by_id(listing_id)
        if not listing:
            raise ListingNotFoundError(listing_id)

        self._validate_purchase(listing, buyer_id)

        seller_id = listing["seller_id"]
        price = listing["price"]
        item_id = listing["item_id"]

        snapshot = self._capture_state_snapshot(
            buyer_id, seller_id, item_id, listing_id
        )

        try:
            self._transfer_funds(price, buyer_id, seller_id)
            self._transfer_item(item_id, buyer_id)
            self._close_listing(listing_id)
        except Exception as e:
            self._restore_state_snapshot(snapshot)
            logger.critical(
                "Purchase failed, state restored "
                "[listing=%d, buyer=%d]: %s",
                listing_id, buyer_id, e,
            )
            raise

        return {
            "listing_id": listing_id,
            "item_id": item_id,
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "price": price,
        }

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

    def _transfer_funds(self, price: float, buyer_id: int, seller_id: int) -> None:
        self.user_service.remove_balance(price, buyer_id)
        self.user_service.add_balance(price, seller_id)

    def _transfer_item(self, item_id: int, buyer_id: int) -> None:
        self.item_service.transfer_ownership(item_id, buyer_id)

    def _close_listing(self, listing_id: int) -> None:
        self.listing_service.deactivate_listing(listing_id)

    def _capture_state_snapshot(
        self,
        buyer_id: int,
        seller_id: int,
        item_id: int,
        listing_id: int,
    ) -> dict:
        buyer = self.user_service.get_user_by_id(buyer_id)
        seller = self.user_service.get_user_by_id(seller_id)
        item = self.item_service.get_item_by_id(item_id)
        listing = self.listing_service.get_listing_by_id(listing_id)

        return {
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "item_id": item_id,
            "listing_id": listing_id,
            "buyer_original_balance": buyer["balance"],
            "seller_original_balance": seller["balance"],
            "original_owner_id": item["owner_id"],
            "listing_original_state": listing["is_active"],
        }

    def _restore_state_snapshot(self, snapshot: dict) -> None:
        self.user_service.set_balance(
            snapshot["buyer_id"],
            snapshot["buyer_original_balance"],
        )
        self.user_service.set_balance(
            snapshot["seller_id"],
            snapshot["seller_original_balance"],
        )
        self.item_service.set_owner(
            snapshot["item_id"],
            snapshot["original_owner_id"],
        )
        self.listing_service.set_listing_status(
            snapshot["listing_id"],
            snapshot["listing_original_state"],
        )
