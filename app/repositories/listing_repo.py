import json
import os
from app.models.marketplace_listing import MarketplaceListing


class ListingRepo:
    def __init__(self):
        self.filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "listings.json"
        )

    def get_all_listings(self) -> list[dict]:
        return self.load_from_json()

    def get_active_listings(self) -> list[dict]:
        listings = self.load_from_json()
        return [listing for listing in listings if listing["active"]]

    def get_listing_by_id(self, listing_id: int) -> dict | None:
        listings = self.load_from_json()
        for listing in listings:
            if listing["listing_id"] == listing_id:
                return listing
        return None

    def save_listing(self, listing: MarketplaceListing) -> dict:
        listings = self.load_from_json()
        listing_dict = listing.model_dump()
        listings.append(listing_dict)
        self.write_to_json(listings)
        return listing_dict

    def update_listing(self, listing_id: int, updates: dict) -> dict | None:
        listings = self.load_from_json()
        for i, listing in enumerate(listings):
            if listing["listing_id"] == listing_id:
                listings[i] = {**listing, **updates}
                self.write_to_json(listings)
                return listings[i]
        return None

    def delete_listing(self, listing_id: int) -> bool:
        listings = self.load_from_json()
        updated_listings = [l for l in listings if l["listing_id"] != listing_id]
        if len(updated_listings) < len(listings):
            self.write_to_json(updated_listings)
            return True
        return False

    def load_from_json(self) -> list[dict]:
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write_to_json(self, data: list[dict]) -> None:
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=2)
