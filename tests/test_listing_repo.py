from app.models.marketplace_listing import MarketplaceListing
from app.repositories.listing_repo import ListingRepo


def make_listing(listing_id=1, seller_id=1, item_id=1, price=50.0, active=True):
    return MarketplaceListing(
        listing_id=listing_id,
        seller_id=seller_id,
        item_id=item_id,
        price=price,
        created_at="2026-01-01T00:00:00",
        active=active,
    )


class TestListingRepo:
    def test_save_listing_and_get_by_id(self, temp_listing_repo):
        listing = make_listing(listing_id=1)
        temp_listing_repo.save_listing(listing)
        result = temp_listing_repo.get_listing_by_id(1)
        assert result is not None
        assert result["listing_id"] == 1

    def test_get_listing_by_id_returns_none_when_not_found(self, temp_listing_repo):
        assert temp_listing_repo.get_listing_by_id(999) is None

    def test_get_all_listings_returns_all_saved(self, temp_listing_repo):
        temp_listing_repo.save_listing(make_listing(listing_id=1))
        temp_listing_repo.save_listing(make_listing(listing_id=2))
        assert len(temp_listing_repo.get_all_listings()) == 2

    def test_get_active_listings_filters_inactive(self, temp_listing_repo):
        temp_listing_repo.save_listing(make_listing(listing_id=1, active=True))
        temp_listing_repo.save_listing(make_listing(listing_id=2, active=False))
        temp_listing_repo.save_listing(make_listing(listing_id=3, active=True))
        active = temp_listing_repo.get_active_listings()
        assert len(active) == 2

    def test_update_listing_applies_changes(self, temp_listing_repo):
        temp_listing_repo.save_listing(make_listing(listing_id=1, price=50.0))
        updated = temp_listing_repo.update_listing(1, {"price": 100.0})
        assert updated["price"] == 100.0

    def test_update_listing_returns_none_when_not_found(self, temp_listing_repo):
        assert temp_listing_repo.update_listing(999, {"price": 100.0}) is None

    def test_delete_listing_removes_listing(self, temp_listing_repo):
        temp_listing_repo.save_listing(make_listing(listing_id=1))
        assert temp_listing_repo.delete_listing(1) is True
        assert temp_listing_repo.get_listing_by_id(1) is None

    def test_delete_listing_returns_false_when_not_found(self, temp_listing_repo):
        assert temp_listing_repo.delete_listing(999) is False

    def test_data_persists_across_repo_instances(self, temp_listing_repo):
        temp_listing_repo.save_listing(make_listing(listing_id=1))
        new_repo = ListingRepo()
        new_repo.filepath = temp_listing_repo.filepath
        assert new_repo.get_listing_by_id(1) is not None

    def test_load_from_json_returns_empty_list_when_file_missing(self, tmp_path):
        repo = ListingRepo()
        repo.filepath = str(tmp_path / "nonexistent.json")
        assert repo.load_from_json() == []
