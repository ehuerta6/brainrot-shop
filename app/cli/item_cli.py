from services.item_service import ItemService

item_service = ItemService()


def prompt_create_item() -> None:
    print("\n--- Create Item ---")

    name = input("Item name: ").strip()
    if not name:
        print("Error: Item name cannot be empty.")
        return

    print("Rarities: common, uncommon, rare, epic, legendary")
    rarity = input("Rarity: ").strip()

    try:
        value = float(input("Value: "))
    except ValueError:
        print("Error: Value must be a number.")
        return

    try:
        owner_id = int(input("Owner ID: "))
    except ValueError:
        print("Error: Owner ID must be an integer.")
        return

    try:
        item = item_service.create_item(name, rarity, value, owner_id)
        print(f"\nItem created!")
        print(f"  ID:     {item['item_id']}")
        print(f"  Name:   {item['item_name']}")
        print(f"  Rarity: {item['rarity']}")
        print(f"  Value:  {item['value']}")
        print(f"  Owner:  {item['owner_id']}")
    except ValueError as error:
        print(f"Error: {error}")


def prompt_view_all_items() -> None:
    print("\n--- All Items ---")
    items = item_service.get_all_items()

    if not items:
        print("No items found.")
        return

    for item in items:
        listed = "[LISTED]" if item["is_listed"] else ""
        print(
            f"  [{item['item_id']}] {item['item_name']} | {item['rarity']} | ${item['value']:.2f} | owner={item['owner_id']} {listed}"
        )


def prompt_view_owner_inventory() -> None:
    print("\n--- Owner Inventory ---")

    try:
        owner_id = int(input("Owner ID: "))
    except ValueError:
        print("Error: Owner ID must be an integer.")
        return

    items = item_service.get_owner_inventory(owner_id)

    if not items:
        print(f"No items found for owner {owner_id}.")
        return

    print(f"Owner {owner_id} has {len(items)} item(s):")
    for item in items:
        listed = "[LISTED]" if item["is_listed"] else ""
        print(
            f"  [{item['item_id']}] {item['item_name']} | {item['rarity']} | ${item['value']:.2f} {listed}"
        )
