from models.item import Item
from repositories.item_repo import ItemRepo
from exceptions.item_error import ItemNotFoundError, InvalidItemNameError, InvalidRarityError, InvalidItemValueError

VALID_RARITIES = ["common", "uncommon", "rare", "epic", "legendary"]


class ItemService:
    def __init__(self):
        self.item_repo = ItemRepo()

    def create_item(
        self, item_name: str, rarity: str, value: float, owner_id: int
    ) -> dict:
        if not item_name.strip():
            raise InvalidItemNameError()

        if rarity.lower() not in VALID_RARITIES:
            raise InvalidRarityError(rarity, VALID_RARITIES)

        if value < 0:
            raise InvalidItemValueError()

        next_item_id = self.generate_next_item_id()

        new_item = Item(
            owner_id=owner_id,
            item_id=next_item_id,
            rarity=rarity.lower(),
            item_name=item_name.strip(),
            base_value=value,
        )

        return self.item_repo.save_item(new_item)

    def get_all_items(self) -> list[dict]:
        return self.item_repo.get_all_items()

    def get_item_by_id(self, item_id: int) -> dict | None:
        return self.item_repo.get_item_by_id(item_id)

    def get_owner_inventory(self, owner_id: int) -> list[dict]:
        return self.item_repo.get_items_by_owner(owner_id)

    def transfer_ownership(self, item_id: int, new_owner_id: int) -> dict | None:
        item = self.item_repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError(item_id)
        return self.item_repo.update_item(
            item_id, {"owner_id": new_owner_id, "is_listed": False}
        )

    def delete_item(self, item_id: int) -> bool:
        return self.item_repo.delete_item(item_id)

    def generate_next_item_id(self) -> int:
        items = self.item_repo.get_all_items()
        if not items:
            return 1
        return max(item["item_id"] for item in items) + 1
