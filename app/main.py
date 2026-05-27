from utils.logging_config import logging

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
from cli.market_cli import prompt_buy_listing
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

is_program_running: bool = True
current_user_id: int | None = None

while is_program_running:
    if current_user_id is None:
        print("\n=== Brainrot Shop - Login ===")
        print("1. Login")
        print("2. Create Account")
        print("3. Exit")

        menu_choice = input("\nChoose: ").strip()

        if menu_choice == "1":
            current_user_id = prompt_login()
        elif menu_choice == "2":
            prompt_create_user()
        elif menu_choice == "3":
            is_program_running = False
            print("Program Terminated")
        else:
            print("Invalid option.")
    else:
        current_user_record = user_service.get_user_by_id(current_user_id)

        if not current_user_record:
            print("Error: Current user no longer exists. Logging out.")
            current_user_id = None
            continue

        print(
            f"\n=== Brainrot Shop === (logged in as {current_user_record['username']})"
        )
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
        print("-- Market --")
        print("11. Buy Listing")
        print("--")
        print("12. Logout")
        print("13. Exit Program")

        menu_choice = input("\nChoose: ").strip()

        if menu_choice == "1":
            prompt_view_all_users()
        elif menu_choice == "2":
            prompt_view_user()
        elif menu_choice == "3":
            prompt_add_balance(current_user_id)
        elif menu_choice == "4":
            prompt_remove_balance(current_user_id)
        elif menu_choice == "5":
            prompt_create_item()
        elif menu_choice == "6":
            prompt_view_all_items()
        elif menu_choice == "7":
            prompt_view_owner_inventory()
        elif menu_choice == "8":
            prompt_create_listing()
        elif menu_choice == "9":
            prompt_view_active_listings()
        elif menu_choice == "10":
            prompt_cancel_listing()
        elif menu_choice == "11":
            prompt_buy_listing(current_user_id)
        elif menu_choice == "12":
            print(f"Logged out from {current_user_record['username']}.")
            current_user_id = None
        elif menu_choice == "13":
            is_program_running = False
            print("Program Terminated")
        else:
            print("Invalid option.")
