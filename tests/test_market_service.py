import pytest
from unittest.mock import patch

from exceptions.listing_error import ListingNotFoundError, ListingInactiveError
from exceptions.market_error import CannotBuyOwnListingError
from exceptions.user_error import UserNotFoundError, InsufficientBalanceError


def _seed_purchase(temp_user_service, temp_item_service, temp_listing_service):
    temp_user_service.create_user("seller_user", 100.0)
    temp_user_service.create_user("buyer_user", 500.0)
    temp_item_service.create_item(
        item_name="Sword", rarity="rare", value=50.0, owner_id=1
    )
    temp_listing_service.create_listing(item_id=1, seller_id=1, price=75.0)


class TestBuyListingHappyPath:
    def test_buy_listing_returns_transaction_summary(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        result = temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        assert result["listing_id"] == 1
        assert result["item_id"] == 1
        assert result["buyer_id"] == 2
        assert result["seller_id"] == 1
        assert result["price"] == 75.0

    def test_buy_listing_deducts_buyer_balance(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        buyer = temp_user_service.get_user_by_id(2)
        assert buyer["balance"] == 425.0

    def test_buy_listing_credits_seller_balance(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        seller = temp_user_service.get_user_by_id(1)
        assert seller["balance"] == 175.0

    def test_buy_listing_transfers_item_ownership(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        item = temp_item_service.get_item_by_id(1)
        assert item["owner_id"] == 2

    def test_buy_listing_unmarks_item_as_listed(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        item = temp_item_service.get_item_by_id(1)
        assert item["is_listed"] is False

    def test_buy_listing_deactivates_listing(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        listing = temp_listing_service.get_listing_by_id(1)
        assert listing["is_active"] is False


class TestBuyListingValidation:
    def test_cannot_buy_nonexistent_listing(self, temp_market_service):
        with pytest.raises(ListingNotFoundError):
            temp_market_service.buy_listing(listing_id=999, buyer_id=1)

    def test_cannot_buy_inactive_listing(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        temp_listing_service.cancel_listing(1)
        with pytest.raises(ListingInactiveError):
            temp_market_service.buy_listing(listing_id=1, buyer_id=2)

    def test_cannot_buy_own_listing(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        with pytest.raises(CannotBuyOwnListingError):
            temp_market_service.buy_listing(listing_id=1, buyer_id=1)

    def test_cannot_buy_with_insufficient_balance(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        temp_user_service.create_user("seller_user", 100.0)
        temp_user_service.create_user("broke_user", 10.0)
        temp_item_service.create_item(
            item_name="Shield", rarity="epic", value=200.0, owner_id=1
        )
        temp_listing_service.create_listing(item_id=1, seller_id=1, price=500.0)
        with pytest.raises(InsufficientBalanceError):
            temp_market_service.buy_listing(listing_id=1, buyer_id=2)

    def test_buyer_must_exist(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        temp_user_service.create_user("seller_user", 100.0)
        temp_item_service.create_item(
            item_name="Sword", rarity="rare", value=50.0, owner_id=1
        )
        temp_listing_service.create_listing(item_id=1, seller_id=1, price=75.0)
        with pytest.raises(UserNotFoundError):
            temp_market_service.buy_listing(listing_id=1, buyer_id=999)


class TestCaptureStateSnapshot:
    def test_snapshot_captures_buyer_balance(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        snapshot = temp_market_service._capture_state_snapshot(
            buyer_id=2, seller_id=1, item_id=1, listing_id=1
        )
        assert snapshot["buyer_original_balance"] == 500.0

    def test_snapshot_captures_seller_balance(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        snapshot = temp_market_service._capture_state_snapshot(
            buyer_id=2, seller_id=1, item_id=1, listing_id=1
        )
        assert snapshot["seller_original_balance"] == 100.0

    def test_snapshot_captures_item_owner(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        snapshot = temp_market_service._capture_state_snapshot(
            buyer_id=2, seller_id=1, item_id=1, listing_id=1
        )
        assert snapshot["original_owner_id"] == 1

    def test_snapshot_captures_listing_state(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        snapshot = temp_market_service._capture_state_snapshot(
            buyer_id=2, seller_id=1, item_id=1, listing_id=1
        )
        assert snapshot["listing_original_state"] is True

    def test_snapshot_stores_all_ids(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        snapshot = temp_market_service._capture_state_snapshot(
            buyer_id=2, seller_id=1, item_id=1, listing_id=1
        )
        assert snapshot["buyer_id"] == 2
        assert snapshot["seller_id"] == 1
        assert snapshot["item_id"] == 1
        assert snapshot["listing_id"] == 1


class TestRestoreStateSnapshot:
    def test_restore_resets_buyer_balance(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        snapshot = temp_market_service._capture_state_snapshot(
            buyer_id=2, seller_id=1, item_id=1, listing_id=1
        )
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        temp_market_service._restore_state_snapshot(snapshot)
        buyer = temp_user_service.get_user_by_id(2)
        assert buyer["balance"] == 500.0

    def test_restore_resets_seller_balance(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        snapshot = temp_market_service._capture_state_snapshot(
            buyer_id=2, seller_id=1, item_id=1, listing_id=1
        )
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        temp_market_service._restore_state_snapshot(snapshot)
        seller = temp_user_service.get_user_by_id(1)
        assert seller["balance"] == 100.0

    def test_restore_resets_item_ownership(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        snapshot = temp_market_service._capture_state_snapshot(
            buyer_id=2, seller_id=1, item_id=1, listing_id=1
        )
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        temp_market_service._restore_state_snapshot(snapshot)
        item = temp_item_service.get_item_by_id(1)
        assert item["owner_id"] == 1

    def test_restore_resets_listing_state(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        snapshot = temp_market_service._capture_state_snapshot(
            buyer_id=2, seller_id=1, item_id=1, listing_id=1
        )
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        temp_market_service._restore_state_snapshot(snapshot)
        listing = temp_listing_service.get_listing_by_id(1)
        assert listing["is_active"] is True


class TestRollbackOnFailure:
    def test_buyer_balance_restored_on_transfer_item_failure(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        with patch.object(
            temp_market_service.item_service,
            "transfer_ownership",
            side_effect=RuntimeError("disk error"),
        ):
            with pytest.raises(RuntimeError):
                temp_market_service.buy_listing(listing_id=1, buyer_id=2)

        buyer = temp_user_service.get_user_by_id(2)
        assert buyer["balance"] == 500.0

    def test_seller_balance_restored_on_transfer_item_failure(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        with patch.object(
            temp_market_service.item_service,
            "transfer_ownership",
            side_effect=RuntimeError("disk error"),
        ):
            with pytest.raises(RuntimeError):
                temp_market_service.buy_listing(listing_id=1, buyer_id=2)

        seller = temp_user_service.get_user_by_id(1)
        assert seller["balance"] == 100.0

    def test_item_ownership_restored_on_close_listing_failure(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        with patch.object(
            temp_market_service.listing_service,
            "deactivate_listing",
            side_effect=RuntimeError("disk error"),
        ):
            with pytest.raises(RuntimeError):
                temp_market_service.buy_listing(listing_id=1, buyer_id=2)

        item = temp_item_service.get_item_by_id(1)
        assert item["owner_id"] == 1

    def test_listing_remains_active_on_failure(
        self,
        temp_market_service,
        temp_user_service,
        temp_item_service,
        temp_listing_service,
    ):
        _seed_purchase(temp_user_service, temp_item_service, temp_listing_service)
        with patch.object(
            temp_market_service.item_service,
            "transfer_ownership",
            side_effect=RuntimeError("disk error"),
        ):
            with pytest.raises(RuntimeError):
                temp_market_service.buy_listing(listing_id=1, buyer_id=2)

        listing = temp_listing_service.get_listing_by_id(1)
        assert listing["is_active"] is True
