from models.user import User
from repositories.user_repo import UserRepo


class UserService:
    def __init__(self):
        self.user_repo = UserRepo()

    def create_user(self, _username: str, _balance: float) -> dict:
        user = self.user_repo.get_user_by_username(_username)

        if user is not None:
            raise ValueError(
                f"User {_username} already exists. Try a different username."
            )

        next_id = self.generate_next_id()

        new_user = User(user_id=next_id, username=_username, balance=_balance)

        return self.user_repo.save_user(new_user)

    def get_user_by_id(self, user_id: int) -> dict | None:
        return self.user_repo.get_user_by_id(user_id)

    def get_user_by_username(self, username: str) -> dict | None:
        return self.user_repo.get_user_by_username(username)

    def get_all_users(self) -> list[dict]:
        return self.user_repo.get_all_users()

    def add_balance(self, amount: float, user_id: int) -> dict | None:
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} does not exist.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        new_balance = user["balance"] + amount
        return self.user_repo.update_user(user_id, {"balance": new_balance})

    def remove_balance(self, amount: float, user_id: int) -> dict | None:
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} does not exist.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        new_balance = user["balance"] - amount
        if new_balance < 0:
            raise ValueError("User can't have a negative balance amount.")
        return self.user_repo.update_user(user_id, {"balance": new_balance})

    def generate_next_id(self) -> int:
        users = self.user_repo.get_all_users()
        if not users:
            return 1
        return max(user["user_id"] for user in users) + 1

    def resolve_user_identifier(self, identifier: str) -> dict | None:
        if identifier.isdigit():
            user = self.get_user_by_id(int(identifier))
        else:
            user = self.get_user_by_username(identifier)

        return user
