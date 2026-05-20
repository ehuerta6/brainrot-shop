import json
from models.item import Item
from models.marketplace_listing import MarketplaceListing


class ListingRepo:
    def __init__(self):
        self.filepath = "data/listings.json"

    def get_all_listings(self):
        return self.load_from_json()

    def save_listing(self, data: Item):
        listings = self.load_from_json()
        new_listing = {
            "listing_id": len(listings) + 1,
            "item_id": data.item_id,
            "seller_id": data.seller_id,
            "price": data.price,
            "created_at": data.created_at,
            "active": True,
        }
        listings.append(new_listing)
        self.write_to_json(listings)
        return new_listing

    def update_listing(self, id):
        return None

    def delete_listing(self, id):
        return None

    def load_from_json(self, data):
        return data

    def write_to_json(self, data):
        return data
