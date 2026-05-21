from cli.item_cli import prompt_create_item, prompt_view_all_items, prompt_view_owner_inventory
from cli.listing_cli import prompt_create_listing, prompt_view_active_listings, prompt_cancel_listing

print("=== Brainrot Shop ===")
print("1. Create Item")
print("2. View All Items")
print("3. View Owner Inventory")
print("4. Create Listing")
print("5. View Active Listings")
print("6. Cancel Listing")

choice = input("\nChoose: ").strip()

if choice == "1":
    prompt_create_item()
elif choice == "2":
    prompt_view_all_items()
elif choice == "3":
    prompt_view_owner_inventory()
elif choice == "4":
    prompt_create_listing()
elif choice == "5":
    prompt_view_active_listings()
elif choice == "6":
    prompt_cancel_listing()
else:
    print("Invalid option.")
