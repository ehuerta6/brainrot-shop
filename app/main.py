from cli.item_cli import (
    prompt_create_item,
    prompt_view_all_items,
    prompt_view_owner_inventory,
)
from cli.listing_cli import (
    prompt_create_listing,
    prompt_view_active_listings,
    prompt_cancel_listing,
)
from cli.user_cli import (
    prompt_login,
    prompt_create_user,
    prompt_view_all_users,
    prompt_view_user,
    prompt_add_balance,
    prompt_remove_balance,
)
from services.user_service import UserService

user_service = UserService()

programRunning: bool = True
current_user_id: int | None = None

while programRunning:
    if current_user_id is None:
        print("\n=== Brainrot Shop - Login ===")
        print("1. Login")
        print("2. Create Account")
        print("3. Exit")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            current_user_id = prompt_login()
        elif choice == "2":
            prompt_create_user()
        elif choice == "3":
            programRunning = False
            print("Program Terminated")
        else:
            print("Invalid option.")
    else:
        user_data = user_service.get_user_by_id(current_user_id)

        if not user_data:
            print("Error: Current user no longer exists. Logging out.")
            current_user_id = None
            continue

        print(f"\n=== Brainrot Shop === (logged in as {user_data['username']})")
        print("-- Users --")
        print("1.  View All Users")
        print("2.  View User")
        print("3.  Add Balance")
        print("4.  Remove Balance")
        print("-- Items --")
        print("5.  Create Item")
        print("6.  View All Items")
        print("7.  View Owner Inventory")
        print("-- Listings --")
        print("8.  Create Listing")
        print("9.  View Active Listings")
        print("10. Cancel Listing")
        print("--")
        print("11. Logout")
        print("12. Exit Program")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            prompt_view_all_users()
        elif choice == "2":
            prompt_view_user()
        elif choice == "3":
            prompt_add_balance(current_user_id)
        elif choice == "4":
            prompt_remove_balance(current_user_id)
        elif choice == "5":
            prompt_create_item()
        elif choice == "6":
            prompt_view_all_items()
        elif choice == "7":
            prompt_view_owner_inventory()
        elif choice == "8":
            prompt_create_listing()
        elif choice == "9":
            prompt_view_active_listings()
        elif choice == "10":
            prompt_cancel_listing()
        elif choice == "11":
            print(f"Logged out from {user_data['username']}.")
            current_user_id = None
        elif choice == "12":
            programRunning = False
            print("Program Terminated")
        else:
            print("Invalid option.")
