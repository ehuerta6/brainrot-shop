import json
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from models.item import Item
from repositories.item_repo import ItemRepo
from services.item_service import ItemService


@pytest.fixture
def temp_repo(tmp_path):
    repo = ItemRepo()
    repo.filepath = str(tmp_path / "items.json")
    with open(repo.filepath, "w") as f:
        json.dump([], f)
    return repo


@pytest.fixture
def temp_service(temp_repo):
    service = ItemService()
    service.item_repo = temp_repo
    return service


class TestItemModel:
    def test_create_item_with_defaults(self):
        item = Item(owner_id=1, item_id=1, rarity="rare", item_name="Sigma Sword", value=99.99)
        assert item.is_listed is False

    def test_create_item_all_fields(self):
        item = Item(owner_id=2, item_id=5, is_listed=True, rarity="legendary", item_name="Rizz Ring", value=500.0)
        assert item.is_listed is True
        assert item.rarity == "legendary"


class TestItemRepo:
    def test_save_and_retrieve(self, temp_repo):
        item = Item(owner_id=1, item_id=1, rarity="common", item_name="Skibidi Shield", value=10.0)
        temp_repo.save_item(item)
        result = temp_repo.get_item_by_id(1)
        assert result is not None
        assert result["item_name"] == "Skibidi Shield"

    def test_get_item_not_found(self, temp_repo):
        assert temp_repo.get_item_by_id(999) is None

    def test_get_all_items(self, temp_repo):
        for i in range(3):
            item = Item(owner_id=1, item_id=i + 1, rarity="common", item_name=f"Item {i}", value=1.0)
            temp_repo.save_item(item)
        assert len(temp_repo.get_all_items()) == 3

    def test_delete_item(self, temp_repo):
        temp_repo.save_item(Item(owner_id=1, item_id=1, rarity="common", item_name="Temp", value=1.0))
        assert temp_repo.delete_item(1) is True
        assert temp_repo.get_item_by_id(1) is None

    def test_delete_item_not_found(self, temp_repo):
        assert temp_repo.delete_item(999) is False

    def test_persistence_across_loads(self, temp_repo):
        temp_repo.save_item(Item(owner_id=1, item_id=1, rarity="rare", item_name="Persistent", value=25.0))
        new_repo = ItemRepo()
        new_repo.filepath = temp_repo.filepath
        assert new_repo.get_item_by_id(1)["item_name"] == "Persistent"


class TestItemService:
    def test_create_item(self, temp_service):
        result = temp_service.create_item("Gyatt Gauntlet", "epic", 250.0, owner_id=1)
        assert result["item_id"] == 1
        assert result["item_name"] == "Gyatt Gauntlet"
        assert result["rarity"] == "epic"
        assert result["is_listed"] is False

    def test_auto_increment_ids(self, temp_service):
        temp_service.create_item("Item A", "common", 10.0, owner_id=1)
        temp_service.create_item("Item B", "rare", 20.0, owner_id=1)
        third = temp_service.create_item("Item C", "legendary", 30.0, owner_id=1)
        assert third["item_id"] == 3

    def test_invalid_rarity_raises(self, temp_service):
        with pytest.raises(ValueError, match="Invalid rarity"):
            temp_service.create_item("Bad Item", "mythical", 10.0, owner_id=1)

    def test_empty_name_raises(self, temp_service):
        with pytest.raises(ValueError, match="cannot be empty"):
            temp_service.create_item("", "common", 10.0, owner_id=1)

    def test_negative_value_raises(self, temp_service):
        with pytest.raises(ValueError, match="cannot be negative"):
            temp_service.create_item("Cheap Item", "common", -5.0, owner_id=1)

    def test_rarity_is_case_insensitive(self, temp_service):
        result = temp_service.create_item("Mixed Case", "LEGENDARY", 100.0, owner_id=1)
        assert result["rarity"] == "legendary"
