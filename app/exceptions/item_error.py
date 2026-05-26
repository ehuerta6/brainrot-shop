from app.exceptions.base_error import BrainrotShopError


class ItemNotFoundError(BrainrotShopError):
    def __init__(self, item_id: int):
        super().__init__(f"Item {item_id} does not exist.")


class ItemAlreadyListedError(BrainrotShopError):
    def __init__(self, item_id: int):
        super().__init__(f"Item {item_id} already listed.")


class ItemInvalidOwnershipError(BrainrotShopError):
    def __init__(self, item_id: int, owner_id: int):
        super().__init__(f"Item {item_id} does not belong to User {owner_id}.")


class InvalidItemNameError(BrainrotShopError):
    def __init__(self):
        super().__init__("Item name cannot be empty.")


class InvalidRarityError(BrainrotShopError):
    def __init__(self, rarity: str, valid_rarities: list[str]):
        super().__init__(
            f"Invalid rarity '{rarity}'. Must be one of: {', '.join(valid_rarities)}"
        )


class InvalidItemValueError(BrainrotShopError):
    def __init__(self):
        super().__init__("Item value cannot be negative.")
