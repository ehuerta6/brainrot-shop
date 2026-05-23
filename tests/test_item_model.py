from app.models.item import Item


class TestItemModel:
    def test_create_item_has_default_is_listed_false(self):
        item = Item(owner_id=1, item_id=1, rarity="rare", item_name="Sigma Sword", base_value=99.99)
        assert item.is_listed is False

    def test_create_item_with_all_fields(self):
        item = Item(owner_id=2, item_id=5, is_listed=True, rarity="legendary", item_name="Rizz Ring", base_value=500.0)
        assert item.owner_id == 2
        assert item.item_id == 5
        assert item.is_listed is True
        assert item.rarity == "legendary"
        assert item.item_name == "Rizz Ring"
        assert item.base_value == 500.0

    def test_item_model_dump_returns_dict(self):
        item = Item(owner_id=1, item_id=1, rarity="common", item_name="Basic Blade", base_value=10.0)
        data = item.model_dump()
        assert isinstance(data, dict)
        assert data["item_name"] == "Basic Blade"
