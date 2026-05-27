import logging

from app.exceptions.user_error import DuplicateUsernameError, InsufficientBalanceError, UserNotFoundError, InvalidAmountError
from models.user import User
from repositories.user_repo import UserRepo

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self):
        self.user_repo = UserRepo()

    def create_user(self, username: str, starting_balance: float) -> dict:
        existing_user = self.user_repo.get_user_by_username(username)

        if existing_user is not None:
            raise DuplicateUsernameError(username)

        next_user_id = self.generate_next_user_id()

        new_user = User(user_id=next_user_id, username=username, balance=starting_balance)

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
            raise UserNotFoundError(user_id)
        if amount <= 0:
            raise InvalidAmountError()
        updated_balance = user["balance"] + amount
        return self.user_repo.update_user(user_id, {"balance": updated_balance})

    def remove_balance(self, amount: float, user_id: int) -> dict | None:
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        if amount <= 0:
            raise InvalidAmountError()
        updated_balance = user["balance"] - amount
        if updated_balance < 0:
            raise InsufficientBalanceError(user_id, user["balance"], amount)
        return self.user_repo.update_user(user_id, {"balance": updated_balance})

    def generate_next_user_id(self) -> int:
        users = self.user_repo.get_all_users()
        if not users:
            return 1
        return max(user["user_id"] for user in users) + 1

    def resolve_user_identifier(self, username_or_id: str) -> dict | None:
        if username_or_id.isdigit():
            user = self.get_user_by_id(int(username_or_id))
        else:
            user = self.get_user_by_username(username_or_id)

        return user

    def set_balance(self, user_id: int, balance: float) -> dict | None:
        return self.user_repo.update_user(user_id, {"balance": balance})
