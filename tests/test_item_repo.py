from models.item import Item
from repositories.item_repo import ItemRepo


class TestItemRepo:
    def test_save_item_and_get_by_id(self, temp_item_repo):
        item = Item(
            owner_id=1,
            item_id=1,
            rarity="common",
            item_name="Skibidi Shield",
            base_value=10.0,
        )
        temp_item_repo.save_item(item)
        result = temp_item_repo.get_item_by_id(1)
        assert result is not None
        assert result["item_name"] == "Skibidi Shield"

    def test_get_item_by_id_returns_none_when_not_found(self, temp_item_repo):
        assert temp_item_repo.get_item_by_id(999) is None

    def test_get_all_items_returns_all_saved_items(self, temp_item_repo):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="common", item_name="A", base_value=1.0)
        )
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=2, rarity="rare", item_name="B", base_value=2.0)
        )
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=3, rarity="epic", item_name="C", base_value=3.0)
        )
        assert len(temp_item_repo.get_all_items()) == 3

    def test_get_items_by_owner_filters_correctly(self, temp_item_repo):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="common", item_name="A", base_value=1.0)
        )
        temp_item_repo.save_item(
            Item(owner_id=2, item_id=2, rarity="rare", item_name="B", base_value=2.0)
        )
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=3, rarity="epic", item_name="C", base_value=3.0)
        )
        assert len(temp_item_repo.get_items_by_owner(1)) == 2
        assert len(temp_item_repo.get_items_by_owner(2)) == 1

    def test_delete_item_removes_item(self, temp_item_repo):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="common", item_name="Temp", base_value=1.0)
        )
        assert temp_item_repo.delete_item(1) is True
        assert temp_item_repo.get_item_by_id(1) is None

    def test_delete_item_returns_false_when_not_found(self, temp_item_repo):
        assert temp_item_repo.delete_item(999) is False

    def test_update_item_applies_changes(self, temp_item_repo):
        temp_item_repo.save_item(
            Item(owner_id=1, item_id=1, rarity="common", item_name="Old", base_value=1.0)
        )
        updated = temp_item_repo.update_item(1, {"item_name": "New", "base_value": 50.0})
        assert updated["item_name"] == "New"
        assert updated["base_value"] == 50.0

    def test_update_item_returns_none_when_not_found(self, temp_item_repo):
        assert temp_item_repo.update_item(999, {"item_name": "X"}) is None

    def test_data_persists_across_repo_instances(self, temp_item_repo):
        temp_item_repo.save_item(
            Item(
                owner_id=1, item_id=1, rarity="rare", item_name="Persistent", base_value=25.0
            )
        )
        new_repo = ItemRepo()
        new_repo.filepath = temp_item_repo.filepath
        assert new_repo.get_item_by_id(1)["item_name"] == "Persistent"

    def test_load_from_json_returns_empty_list_when_file_missing(self, tmp_path):
        repo = ItemRepo()
        repo.filepath = str(tmp_path / "nonexistent.json")
        assert repo.load_from_json() == []
