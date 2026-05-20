from models.item import Item
from repositories.item_repo import ItemRepo

VALID_RARITIES = ["common", "uncommon", "rare", "epic", "legendary"]


class ItemService:
    def __init__(self):
        self.item_repo = ItemRepo()

    def create_item(self, item_name: str, rarity: str, value: float, owner_id: int) -> dict:
        if not item_name.strip():
            raise ValueError("Item name cannot be empty.")

        if rarity.lower() not in VALID_RARITIES:
            raise ValueError(f"Invalid rarity '{rarity}'. Must be one of: {', '.join(VALID_RARITIES)}")

        if value < 0:
            raise ValueError("Item value cannot be negative.")

        next_id = self.generate_next_id()

        new_item = Item(
            owner_id=owner_id,
            item_id=next_id,
            rarity=rarity.lower(),
            item_name=item_name.strip(),
            value=value,
        )

        return self.item_repo.save_item(new_item)

    def get_all_items(self) -> list[dict]:
        return self.item_repo.get_all_items()

    def get_item(self, item_id: int) -> dict | None:
        return self.item_repo.get_item_by_id(item_id)

    def delete_item(self, item_id: int) -> bool:
        return self.item_repo.delete_item(item_id)

    def generate_next_id(self) -> int:
        items = self.item_repo.get_all_items()
        if not items:
            return 1
        return max(item["item_id"] for item in items) + 1
