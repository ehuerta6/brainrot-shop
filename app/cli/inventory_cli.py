from services.item_service import ItemService

item_service = ItemService()


def prompt_create_item():
    print("\n--- Create a New Item ---")

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
