import pytest
from app.models.item import Item
from app.models.marketplace_listing import MarketplaceListing


def _seed_purchase(temp_item_repo, temp_listing_repo, temp_user_service):
    temp_user_service.create_user("seller_user", 100.0)
    temp_user_service.create_user("buyer_user", 500.0)
    temp_item_repo.save_item(
        Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", value=50.0)
    )
    temp_listing_repo.save_listing(
        MarketplaceListing(listing_id=1, seller_id=1, item_id=1, price=75.0)
    )


class TestBuyListingHappyPath:
    def test_buy_listing_returns_transaction_summary(
        self, temp_market_service, temp_item_repo, temp_listing_repo, temp_user_service
    ):
        _seed_purchase(temp_item_repo, temp_listing_repo, temp_user_service)
        result = temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        assert result["listing_id"] == 1
        assert result["item_id"] == 1
        assert result["buyer_id"] == 2
        assert result["seller_id"] == 1
        assert result["price"] == 75.0

    def test_buy_listing_deducts_buyer_balance(
        self, temp_market_service, temp_item_repo, temp_listing_repo, temp_user_service
    ):
        _seed_purchase(temp_item_repo, temp_listing_repo, temp_user_service)
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        buyer = temp_user_service.get_user_by_id(2)
        assert buyer["balance"] == 425.0

    def test_buy_listing_credits_seller_balance(
        self, temp_market_service, temp_item_repo, temp_listing_repo, temp_user_service
    ):
        _seed_purchase(temp_item_repo, temp_listing_repo, temp_user_service)
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        seller = temp_user_service.get_user_by_id(1)
        assert seller["balance"] == 175.0

    def test_buy_listing_transfers_item_ownership(
        self, temp_market_service, temp_item_repo, temp_listing_repo, temp_user_service
    ):
        _seed_purchase(temp_item_repo, temp_listing_repo, temp_user_service)
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        item = temp_item_repo.get_item_by_id(1)
        assert item["owner_id"] == 2

    def test_buy_listing_unmarks_item_as_listed(
        self, temp_market_service, temp_item_repo, temp_listing_repo, temp_user_service
    ):
        _seed_purchase(temp_item_repo, temp_listing_repo, temp_user_service)
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        item = temp_item_repo.get_item_by_id(1)
        assert item["is_listed"] is False

    def test_buy_listing_deactivates_listing(
        self, temp_market_service, temp_item_repo, temp_listing_repo, temp_user_service
    ):
        _seed_purchase(temp_item_repo, temp_listing_repo, temp_user_service)
        temp_market_service.buy_listing(listing_id=1, buyer_id=2)
        listing = temp_listing_repo.get_listing_by_id(1)
        assert listing["active"] is False


class TestBuyListingValidation:
    def test_cannot_buy_nonexistent_listing(self, temp_market_service):
        with pytest.raises(ValueError, match="does not exist"):
            temp_market_service.buy_listing(listing_id=999, buyer_id=1)

    def test_cannot_buy_inactive_listing(
        self, temp_market_service, temp_item_repo, temp_listing_repo, temp_user_service
    ):
        _seed_purchase(temp_item_repo, temp_listing_repo, temp_user_service)
        temp_listing_repo.update_listing(1, {"active": False})
        with pytest.raises(ValueError, match="no longer active"):
            temp_market_service.buy_listing(listing_id=1, buyer_id=2)

    def test_cannot_buy_own_listing(
        self, temp_market_service, temp_item_repo, temp_listing_repo, temp_user_service
    ):
        _seed_purchase(temp_item_repo, temp_listing_repo, temp_user_service)
        with pytest.raises(ValueError, match="cannot buy your own"):
            temp_market_service.buy_listing(listing_id=1, buyer_id=1)

    def test_cannot_buy_with_insufficient_balance(
        self, temp_market_service, temp_item_repo, temp_listing_repo, temp_user_service
    ):
        temp_user_service.create_user("seller_user", 100.0)
        temp_user_service.create_user("broke_user", 10.0)
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="epic", item_name="Shield", value=200.0)
        )
        temp_listing_repo.save_listing(
            MarketplaceListing(listing_id=1, seller_id=1, item_id=1, price=500.0)
        )
        with pytest.raises(ValueError, match="Insufficient balance"):
            temp_market_service.buy_listing(listing_id=1, buyer_id=2)

    def test_buyer_must_exist(
        self, temp_market_service, temp_item_repo, temp_listing_repo, temp_user_service
    ):
        temp_user_service.create_user("seller_user", 100.0)
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", value=50.0)
        )
        temp_listing_repo.save_listing(
            MarketplaceListing(listing_id=1, seller_id=1, item_id=1, price=75.0)
        )
        with pytest.raises(ValueError, match="Buyer .* does not exist"):
            temp_market_service.buy_listing(listing_id=1, buyer_id=999)
