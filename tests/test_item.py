import json
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from models.item import Item
from models.marketplace_listing import MarketplaceListing
from repositories.item_repo import ItemRepo
from repositories.listing_repo import ListingRepo
from services.item_service import ItemService
from services.listing_service import ListingService


@pytest.fixture
def temp_item_repo(tmp_path):
    repo = ItemRepo()
    repo.filepath = str(tmp_path / "items.json")
    with open(repo.filepath, "w") as f:
        json.dump([], f)
    return repo


@pytest.fixture
def temp_listing_repo(tmp_path):
    repo = ListingRepo()
    repo.filepath = str(tmp_path / "listings.json")
    with open(repo.filepath, "w") as f:
        json.dump([], f)
    return repo


@pytest.fixture
def temp_item_service(temp_item_repo):
    service = ItemService()
    service.item_repo = temp_item_repo
    return service


@pytest.fixture
def temp_listing_service(temp_item_repo, temp_listing_repo):
    service = ListingService()
    service.item_repo = temp_item_repo
    service.listing_repo = temp_listing_repo
    return service


class TestItemRepo:
    def test_save_and_retrieve(self, temp_item_repo):
        item = Item(owner_id=1, item_id=1, rarity="common", item_name="Skibidi Shield", value=10.0)
        temp_item_repo.save_item(item)
        result = temp_item_repo.get_item_by_id(1)
        assert result is not None
        assert result["item_name"] == "Skibidi Shield"

    def test_get_item_not_found(self, temp_item_repo):
        assert temp_item_repo.get_item_by_id(999) is None

    def test_get_items_by_owner(self, temp_item_repo):
        temp_item_repo.save_item(Item(owner_id=1, item_id=1, rarity="common", item_name="A", value=1.0))
        temp_item_repo.save_item(Item(owner_id=2, item_id=2, rarity="rare", item_name="B", value=2.0))
        temp_item_repo.save_item(Item(owner_id=1, item_id=3, rarity="epic", item_name="C", value=3.0))
        assert len(temp_item_repo.get_items_by_owner(1)) == 2

    def test_delete_item(self, temp_item_repo):
        temp_item_repo.save_item(Item(owner_id=1, item_id=1, rarity="common", item_name="Temp", value=1.0))
        assert temp_item_repo.delete_item(1) is True
        assert temp_item_repo.get_item_by_id(1) is None

    def test_update_item(self, temp_item_repo):
        temp_item_repo.save_item(Item(owner_id=1, item_id=1, rarity="common", item_name="Old", value=1.0))
        updated = temp_item_repo.update_item(1, {"item_name": "New", "value": 50.0})
        assert updated["item_name"] == "New"
        assert updated["value"] == 50.0

    def test_persistence_across_loads(self, temp_item_repo):
        temp_item_repo.save_item(Item(owner_id=1, item_id=1, rarity="rare", item_name="Persistent", value=25.0))
        new_repo = ItemRepo()
        new_repo.filepath = temp_item_repo.filepath
        assert new_repo.get_item_by_id(1)["item_name"] == "Persistent"


class TestItemService:
    def test_create_item(self, temp_item_service):
        result = temp_item_service.create_item("Gyatt Gauntlet", "epic", 250.0, owner_id=1)
        assert result["item_id"] == 1
        assert result["item_name"] == "Gyatt Gauntlet"
        assert result["rarity"] == "epic"

    def test_auto_increment_ids(self, temp_item_service):
        temp_item_service.create_item("A", "common", 10.0, owner_id=1)
        temp_item_service.create_item("B", "rare", 20.0, owner_id=1)
        third = temp_item_service.create_item("C", "legendary", 30.0, owner_id=1)
        assert third["item_id"] == 3

    def test_invalid_rarity_raises(self, temp_item_service):
        with pytest.raises(ValueError, match="Invalid rarity"):
            temp_item_service.create_item("Bad", "mythical", 10.0, owner_id=1)

    def test_empty_name_raises(self, temp_item_service):
        with pytest.raises(ValueError, match="cannot be empty"):
            temp_item_service.create_item("", "common", 10.0, owner_id=1)

    def test_negative_value_raises(self, temp_item_service):
        with pytest.raises(ValueError, match="cannot be negative"):
            temp_item_service.create_item("X", "common", -5.0, owner_id=1)

    def test_get_owner_inventory(self, temp_item_service):
        temp_item_service.create_item("A", "common", 10.0, owner_id=1)
        temp_item_service.create_item("B", "rare", 20.0, owner_id=2)
        temp_item_service.create_item("C", "epic", 30.0, owner_id=1)
        assert len(temp_item_service.get_owner_inventory(1)) == 2


class TestListingService:
    def test_create_listing(self, temp_listing_service, temp_item_repo):
        temp_item_repo.save_item(Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", value=50.0))
        listing = temp_listing_service.create_listing(item_id=1, seller_id=1, price=75.0)
        assert listing["listing_id"] == 1
        assert listing["item_id"] == 1
        assert listing["seller_id"] == 1
        assert listing["price"] == 75.0

    def test_listing_marks_item_as_listed(self, temp_listing_service, temp_item_repo):
        temp_item_repo.save_item(Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", value=50.0))
        temp_listing_service.create_listing(item_id=1, seller_id=1, price=75.0)
        item = temp_item_repo.get_item_by_id(1)
        assert item["is_listed"] is True

    def test_cannot_list_nonexistent_item(self, temp_listing_service):
        with pytest.raises(ValueError, match="does not exist"):
            temp_listing_service.create_listing(item_id=999, seller_id=1, price=50.0)

    def test_cannot_list_item_you_dont_own(self, temp_listing_service, temp_item_repo):
        temp_item_repo.save_item(Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", value=50.0))
        with pytest.raises(ValueError, match="does not own"):
            temp_listing_service.create_listing(item_id=1, seller_id=999, price=50.0)

    def test_cannot_list_already_listed_item(self, temp_listing_service, temp_item_repo):
        temp_item_repo.save_item(Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", value=50.0))
        temp_listing_service.create_listing(item_id=1, seller_id=1, price=75.0)
        with pytest.raises(ValueError, match="already listed"):
            temp_listing_service.create_listing(item_id=1, seller_id=1, price=100.0)

    def test_cancel_listing_unmarks_item(self, temp_listing_service, temp_item_repo):
        temp_item_repo.save_item(Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", value=50.0))
        temp_listing_service.create_listing(item_id=1, seller_id=1, price=75.0)
        temp_listing_service.cancel_listing(1)
        item = temp_item_repo.get_item_by_id(1)
        assert item["is_listed"] is False

    def test_cancel_nonexistent_listing(self, temp_listing_service):
        assert temp_listing_service.cancel_listing(999) is False

    def test_price_must_be_positive(self, temp_listing_service, temp_item_repo):
        temp_item_repo.save_item(Item(owner_id=1, item_id=1, rarity="rare", item_name="Sword", value=50.0))
        with pytest.raises(ValueError, match="greater than zero"):
            temp_listing_service.create_listing(item_id=1, seller_id=1, price=0)
