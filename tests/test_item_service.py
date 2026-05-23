import pytest


class TestItemServiceCreateItem:
    def test_create_item_returns_saved_item(self, temp_item_service):
        result = temp_item_service.create_item("Gyatt Gauntlet", "epic", 250.0, owner_id=1)
        assert result["item_id"] == 1
        assert result["item_name"] == "Gyatt Gauntlet"
        assert result["rarity"] == "epic"
        assert result["base_value"] == 250.0
        assert result["owner_id"] == 1
        assert result["is_listed"] is False

    def test_create_item_auto_increments_ids(self, temp_item_service):
        temp_item_service.create_item("A", "common", 10.0, owner_id=1)
        temp_item_service.create_item("B", "rare", 20.0, owner_id=1)
        third = temp_item_service.create_item("C", "legendary", 30.0, owner_id=1)
        assert third["item_id"] == 3

    def test_create_item_lowercases_rarity(self, temp_item_service):
        result = temp_item_service.create_item("Mixed Case", "LEGENDARY", 100.0, owner_id=1)
        assert result["rarity"] == "legendary"

    def test_create_item_trims_whitespace_from_name(self, temp_item_service):
        result = temp_item_service.create_item("  Spaced Name  ", "rare", 50.0, owner_id=1)
        assert result["item_name"] == "Spaced Name"


class TestItemServiceValidation:
    def test_empty_name_raises_error(self, temp_item_service):
        with pytest.raises(ValueError, match="cannot be empty"):
            temp_item_service.create_item("", "common", 10.0, owner_id=1)

    def test_whitespace_only_name_raises_error(self, temp_item_service):
        with pytest.raises(ValueError, match="cannot be empty"):
            temp_item_service.create_item("   ", "common", 10.0, owner_id=1)

    def test_invalid_rarity_raises_error(self, temp_item_service):
        with pytest.raises(ValueError, match="Invalid rarity"):
            temp_item_service.create_item("Bad Item", "mythical", 10.0, owner_id=1)

    def test_negative_value_raises_error(self, temp_item_service):
        with pytest.raises(ValueError, match="cannot be negative"):
            temp_item_service.create_item("Cheap Item", "common", -5.0, owner_id=1)


class TestItemServiceQueries:
    def test_get_all_items_returns_all(self, temp_item_service):
        temp_item_service.create_item("A", "common", 10.0, owner_id=1)
        temp_item_service.create_item("B", "rare", 20.0, owner_id=2)
        assert len(temp_item_service.get_all_items()) == 2

    def test_get_item_returns_single_item(self, temp_item_service):
        temp_item_service.create_item("Target", "epic", 100.0, owner_id=1)
        result = temp_item_service.get_item_by_id(1)
        assert result["item_name"] == "Target"

    def test_get_item_returns_none_when_not_found(self, temp_item_service):
        assert temp_item_service.get_item_by_id(999) is None

    def test_get_owner_inventory_filters_by_owner(self, temp_item_service):
        temp_item_service.create_item("A", "common", 10.0, owner_id=1)
        temp_item_service.create_item("B", "rare", 20.0, owner_id=2)
        temp_item_service.create_item("C", "epic", 30.0, owner_id=1)
        assert len(temp_item_service.get_owner_inventory(1)) == 2
        assert len(temp_item_service.get_owner_inventory(2)) == 1

    def test_delete_item_removes_item(self, temp_item_service):
        temp_item_service.create_item("Doomed", "common", 5.0, owner_id=1)
        assert temp_item_service.delete_item(1) is True
        assert temp_item_service.get_item_by_id(1) is None
