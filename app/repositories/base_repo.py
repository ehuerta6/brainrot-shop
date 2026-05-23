import json
import os


class BaseRepo:
    def __init__(self, filename: str):
        self.filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", filename
        )

    def _load_records(self) -> list[dict]:
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_records(self, records: list[dict]) -> None:
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w") as file:
            json.dump(records, file, indent=2)
