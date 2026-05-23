import json
import os
from models.user import User


class UserRepo:
    def __init__(self):
        self.filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "users.json"
        )

    def get_all_users(self) -> list[dict]:
        return self.load_from_json()

    def get_user_by_id(self, user_id: int) -> dict | None:
        users = self.load_from_json()
        for user in users:
            if user["user_id"] == user_id:
                return user
        return None

    def get_user_by_username(self, username: str) -> dict | None:
        users = self.load_from_json()
        for user in users:
            if user["username"] == username:
                return user
        return None

    def save_user(self, user: User) -> dict:
        users = self.load_from_json()
        if any(existing_user["user_id"] == user.user_id for existing_user in users):
            raise ValueError(f"User with id {user.user_id} already exists")
        user_dict = user.model_dump()
        users.append(user_dict)
        self.write_to_json(users)
        return user_dict

    def update_user(self, user_id: int, field_updates: dict) -> dict | None:
        users = self.load_from_json()
        for i, user in enumerate(users):
            if user["user_id"] == user_id:
                users[i] = {**user, **field_updates}
                self.write_to_json(users)
                return users[i]
        return None

    def delete_user(self, user_id: int) -> bool:
        users = self.load_from_json()
        updated_users = [user for user in users if user["user_id"] != user_id]
        if len(updated_users) < len(users):
            self.write_to_json(updated_users)
            return True
        return False

    def load_from_json(self) -> list[dict]:
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write_to_json(self, data: list[dict]) -> None:
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=2)
