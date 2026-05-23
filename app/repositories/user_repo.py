from models.user import User
from repositories.base_repo import BaseRepo


class UserRepo(BaseRepo):
    def __init__(self):
        super().__init__("users.json")

    def get_all_users(self) -> list[dict]:
        return self._load_records()

    def get_user_by_id(self, user_id: int) -> dict | None:
        users = self._load_records()
        for user in users:
            if user["user_id"] == user_id:
                return user
        return None

    def get_user_by_username(self, username: str) -> dict | None:
        users = self._load_records()
        for user in users:
            if user["username"] == username:
                return user
        return None

    def save_user(self, user: User) -> dict:
        users = self._load_records()
        if any(existing_user["user_id"] == user.user_id for existing_user in users):
            raise ValueError(f"User with id {user.user_id} already exists")
        user_dict = user.model_dump()
        users.append(user_dict)
        self._write_records(users)
        return user_dict

    def update_user(self, user_id: int, field_updates: dict) -> dict | None:
        users = self._load_records()
        for i, user in enumerate(users):
            if user["user_id"] == user_id:
                users[i] = {**user, **field_updates}
                self._write_records(users)
                return users[i]
        return None

    def delete_user(self, user_id: int) -> bool:
        users = self._load_records()
        updated_users = [user for user in users if user["user_id"] != user_id]
        if len(updated_users) < len(users):
            self._write_records(updated_users)
            return True
        return False
