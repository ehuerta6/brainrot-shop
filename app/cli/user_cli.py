from services.user_service import UserService
from exceptions.base_error import BrainrotShopError

user_service = UserService()


def prompt_login() -> int | None:
    print("\n--- Login ---")

    username_or_id = input("Enter username or user ID: ").strip()
    if not username_or_id:
        print("Error: Input cannot be empty.")
        return None

    user = user_service.resolve_user_identifier(username_or_id)

    if not user:
        print(f"User '{username_or_id}' not found.")
        return None

    print(f"\nLogged in as {user['username']} (ID: {user['user_id']})")
    return user["user_id"]


def prompt_create_user() -> None:
    print("\n--- Create User ---")

    username = input("Username: ").strip()
    if not username:
        print("Error: Username cannot be empty.")
        return

    try:
        balance = float(input("Starting balance: "))
    except ValueError:
        print("Error: Balance must be a number.")
        return

    try:
        user = user_service.create_user(username, balance)
        print(f"\nUser created!")
        print(f"  ID:       {user['user_id']}")
        print(f"  Username: {user['username']}")
        print(f"  Balance:  ${user['balance']:.2f}")
    except BrainrotShopError as error:
        print(f"Error: {error}")


def prompt_view_all_users() -> None:
    print("\n--- All Users ---")
    users = user_service.get_all_users()

    if not users:
        print("No users found.")
        return

    for user in users:
        print(f"  [{user['user_id']}] {user['username']} | ${user['balance']:.2f}")


def prompt_view_user() -> None:
    print("\n--- View User ---")

    username_or_id = input("Enter username or user ID: ").strip()
    if not username_or_id:
        print("Error: Input cannot be empty.")
        return

    user = user_service.resolve_user_identifier(username_or_id)

    if not user:
        print(f"User '{username_or_id}' not found.")
        return

    print(f"  ID:       {user['user_id']}")
    print(f"  Username: {user['username']}")
    print(f"  Balance:  ${user['balance']:.2f}")


def prompt_add_balance(current_user_id: int) -> None:
    print("\n--- Add Balance ---")

    try:
        amount = float(input("Amount to add: "))
    except ValueError:
        print("Error: Amount must be a number.")
        return

    try:
        user = user_service.add_balance(amount, current_user_id)
        print(f"\nBalance updated!")
        print(f"  Username:    {user['username']}")
        print(f"  New Balance: ${user['balance']:.2f}")
    except BrainrotShopError as error:
        print(f"Error: {error}")


def prompt_remove_balance(current_user_id: int) -> None:
    print("\n--- Remove Balance ---")

    try:
        amount = float(input("Amount to remove: "))
    except ValueError:
        print("Error: Amount must be a number.")
        return

    try:
        user = user_service.remove_balance(amount, current_user_id)
        print(f"\nBalance updated!")
        print(f"  Username:    {user['username']}")
        print(f"  New Balance: ${user['balance']:.2f}")
    except BrainrotShopError as error:
        print(f"Error: {error}")
