from services.user_service import UserService

user_service = UserService()


def prompt_login() -> int | None:
    print("\n--- Login ---")

    identifier = input("Enter username or user ID: ").strip()
    if not identifier:
        print("Error: Input cannot be empty.")
        return None

    if identifier.isdigit():
        user = user_service.get_user_by_id(int(identifier))
    else:
        user = user_service.get_user_by_username(identifier)

    if not user:
        print(f"User '{identifier}' not found.")
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
    except ValueError as error:
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

    username = input("Username: ").strip()
    if not username:
        print("Error: Username cannot be empty.")
        return

    user = user_service.get_user_by_username(username)

    if not user:
        print(f"User '{username}' not found.")
        return

    print(f"  ID:       {user['user_id']}")
    print(f"  Username: {user['username']}")
    print(f"  Balance:  ${user['balance']:.2f}")


def prompt_add_balance() -> None:
    print("\n--- Add Balance ---")

    username = input("Username: ").strip()
    if not username:
        print("Error: Username cannot be empty.")
        return

    try:
        amount = float(input("Amount to add: "))
    except ValueError:
        print("Error: Amount must be a number.")
        return

    try:
        user = user_service.add_balance(amount, username)
        print(f"\nBalance updated!")
        print(f"  Username:    {user['username']}")
        print(f"  New Balance: ${user['balance']:.2f}")
    except ValueError as error:
        print(f"Error: {error}")


def prompt_remove_balance() -> None:
    print("\n--- Remove Balance ---")

    user_id = input("Username: ").strip()
    if not user_id:
        print("Error: Username cannot be empty.")
        return

    try:
        amount = float(input("Amount to remove: "))
    except ValueError:
        print("Error: Amount must be a number.")
        return

    try:
        user = user_service.remove_balance(amount, user_id)
        print(f"\nBalance updated!")
        print(f"  Username:    {user['username']}")
        print(f"  New Balance: ${user['balance']:.2f}")
    except ValueError as error:
        print(f"Error: {error}")
