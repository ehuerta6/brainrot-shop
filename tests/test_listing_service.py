import pytest
from app.models.item import Item


class TestListingServiceCreateListing:
    def test_create_listing_returns_saved_listing(
        self, temp_listing_service, temp_item_repo
    ):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", base_value=50.0)
        )
        listing = temp_listing_service.create_listing(
            item_id=1, seller_id=1, price=75.0
        )
        assert listing["listing_id"] == 1
        assert listing["item_id"] == 1
        assert listing["seller_id"] == 1
        assert listing["price"] == 75.0
        assert listing["is_active"] is True

    def test_create_listing_marks_item_as_listed(
        self, temp_listing_service, temp_item_repo
    ):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", base_value=50.0)
        )
        temp_listing_service.create_listing(item_id=1, seller_id=1, price=75.0)
        item = temp_item_repo.get_item_by_id(1)
        assert item["is_listed"] is True

    def test_create_listing_auto_increments_ids(
        self, temp_listing_service, temp_item_repo
    ):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="rare", item_name="A", base_value=10.0)
        )
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=2, rarity="epic", item_name="B", base_value=20.0)
        )
        temp_listing_service.create_listing(item_id=1, seller_id=1, price=50.0)
        second = temp_listing_service.create_listing(item_id=2, seller_id=1, price=60.0)
        assert second["listing_id"] == 2


class TestListingServiceOwnershipValidation:
    def test_cannot_list_nonexistent_item(self, temp_listing_service):
        with pytest.raises(ValueError, match="does not exist"):
            temp_listing_service.create_listing(item_id=999, seller_id=1, price=50.0)

    def test_cannot_list_item_you_dont_own(self, temp_listing_service, temp_item_repo):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", base_value=50.0)
        )
        with pytest.raises(ValueError, match="does not own"):
            temp_listing_service.create_listing(item_id=1, seller_id=999, price=50.0)

    def test_cannot_list_already_listed_item(
        self, temp_listing_service, temp_item_repo
    ):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", base_value=50.0)
        )
        temp_listing_service.create_listing(item_id=1, seller_id=1, price=75.0)
        with pytest.raises(ValueError, match="already listed"):
            temp_listing_service.create_listing(item_id=1, seller_id=1, price=100.0)

    def test_price_must_be_greater_than_zero(
        self, temp_listing_service, temp_item_repo
    ):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", base_value=50.0)
        )
        with pytest.raises(ValueError, match="greater than zero"):
            temp_listing_service.create_listing(item_id=1, seller_id=1, price=0)


class TestListingServiceCancelListing:
    def test_cancel_listing_deactivates_listing(
        self, temp_listing_service, temp_item_repo, temp_listing_repo
    ):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", base_value=50.0)
        )
        temp_listing_service.create_listing(item_id=1, seller_id=1, price=75.0)
        temp_listing_service.cancel_listing(1)
        listing = temp_listing_repo.get_listing_by_id(1)
        assert listing["is_active"] is False

    def test_cancel_listing_unmarks_item_as_listed(
        self, temp_listing_service, temp_item_repo
    ):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", base_value=50.0)
        )
        temp_listing_service.create_listing(item_id=1, seller_id=1, price=75.0)
        temp_listing_service.cancel_listing(1)
        item = temp_item_repo.get_item_by_id(1)
        assert item["is_listed"] is False

    def test_cancel_nonexistent_listing_returns_false(self, temp_listing_service):
        assert temp_listing_service.cancel_listing(999) is False

    def test_item_can_be_relisted_after_cancel(
        self, temp_listing_service, temp_item_repo
    ):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", base_value=50.0)
        )
        temp_listing_service.create_listing(item_id=1, seller_id=1, price=75.0)
        temp_listing_service.cancel_listing(1)
        relisted = temp_listing_service.create_listing(
            item_id=1, seller_id=1, price=80.0
        )
        assert relisted["listing_id"] == 2


class TestListingServiceQueries:
    def test_get_active_listings_excludes_cancelled(
        self, temp_listing_service, temp_item_repo
    ):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="rare", item_name="A", base_value=10.0)
        )
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=2, rarity="epic", item_name="B", base_value=20.0)
        )
        temp_listing_service.create_listing(item_id=1, seller_id=1, price=50.0)
        temp_listing_service.create_listing(item_id=2, seller_id=1, price=60.0)
        temp_listing_service.cancel_listing(1)
        active = temp_listing_service.get_active_listings()
        assert len(active) == 1
        assert active[0]["item_id"] == 2
