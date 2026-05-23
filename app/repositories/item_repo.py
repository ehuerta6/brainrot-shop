from repositories.base_repo import BaseRepo
from models.item import Item


class ItemRepo(BaseRepo):
    def __init__(self):
        super().__init__("items.json")

    def get_all_items(self) -> list[dict]:
        return self._load_records()

    def get_item_by_id(self, item_id: int) -> dict | None:
        items = self._load_records()
        for item in items:
            if item["item_id"] == item_id:
                return item
        return None

    def get_items_by_owner(self, owner_id: int) -> list[dict]:
        items = self._load_records()
        return [item for item in items if item["owner_id"] == owner_id]

    def save_item(self, item: Item) -> dict:
        items = self._load_records()
        item_dict = item.model_dump()
        items.append(item_dict)
        self._write_records(items)
        return item_dict

    def update_item(self, item_id: int, field_updates: dict) -> dict | None:
        items = self._load_records()
        for i, item in enumerate(items):
            if item["item_id"] == item_id:
                items[i] = {**item, **field_updates}
                self._write_records(items)
                return items[i]
        return None

    def delete_item(self, item_id: int) -> bool:
        items = self._load_records()
        updated_items = [item for item in items if item["item_id"] != item_id]
        if len(updated_items) < len(items):
            self._write_records(updated_items)
            return True
        return False
