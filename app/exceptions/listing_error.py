from app.exceptions.base_error import BrainrotShopError


class ListingNotFoundError(BrainrotShopError):
    def __init__(self, listing_id: int):
        super().__init__(f"Listing {listing_id} does not exist.")


class ListingInactiveError(BrainrotShopError):
    def __init__(self, listing_id: int):
        super().__init__(f"Listing {listing_id} is inactive.")


class InvalidPriceError(BrainrotShopError):
    def __init__(self):
        super().__init__("Price must be greater than zero.")
