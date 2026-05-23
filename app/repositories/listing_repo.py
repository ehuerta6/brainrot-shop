from repositories.base_repo import BaseRepo
from models.marketplace_listing import MarketplaceListing


class ListingRepo(BaseRepo):
    def __init__(self):
        super().__init__("listings.json")

    def get_all_listings(self) -> list[dict]:
        return self._load_records()

    def get_active_listings(self) -> list[dict]:
        listings = self._load_records()
        return [listing for listing in listings if listing["is_active"]]

    def get_listing_by_id(self, listing_id: int) -> dict | None:
        listings = self._load_records()
        for listing in listings:
            if listing["listing_id"] == listing_id:
                return listing
        return None

    def save_listing(self, listing: MarketplaceListing) -> dict:
        listings = self._load_records()
        listing_dict = listing.model_dump()
        listings.append(listing_dict)
        self._write_records(listings)
        return listing_dict

    def update_listing(self, listing_id: int, field_updates: dict) -> dict | None:
        listings = self._load_records()
        for i, listing in enumerate(listings):
            if listing["listing_id"] == listing_id:
                listings[i] = {**listing, **field_updates}
                self._write_records(listings)
                return listings[i]
        return None

    def delete_listing(self, listing_id: int) -> bool:
        listings = self._load_records()
        remaining_listings = [
            listing
            for listing in listings
            if listing["listing_id"] != listing_id
        ]
        if len(remaining_listings) < len(listings):
            self._write_records(remaining_listings)
            return True
        return False
