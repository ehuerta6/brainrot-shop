import json
import os
from app.models.item import Item


class ItemRepo:
    def __init__(self):
        self.filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "items.json"
        )

    def get_all_items(self) -> list[dict]:
        return self.load_from_json()

    def get_item_by_id(self, item_id: int) -> dict | None:
        items = self.load_from_json()
        for item in items:
            if item["item_id"] == item_id:
                return item
        return None

    def get_items_by_owner(self, owner_id: int) -> list[dict]:
        items = self.load_from_json()
        return [item for item in items if item["owner_id"] == owner_id]

    def save_item(self, item: Item) -> dict:
        items = self.load_from_json()
        item_dict = item.model_dump()
        items.append(item_dict)
        self.write_to_json(items)
        return item_dict

    def update_item(self, item_id: int, updates: dict) -> dict | None:
        items = self.load_from_json()
        for i, item in enumerate(items):
            if item["item_id"] == item_id:
                items[i] = {**item, **updates}
                self.write_to_json(items)
                return items[i]
        return None

    def delete_item(self, item_id: int) -> bool:
        items = self.load_from_json()
        updated_items = [item for item in items if item["item_id"] != item_id]
        if len(updated_items) < len(items):
            self.write_to_json(updated_items)
            return True
        return False

    def load_from_json(self) -> list[dict]:
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write_to_json(self, data: list[dict]) -> None:
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=2)
