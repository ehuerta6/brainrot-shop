from app.exceptions.base_error import BrainrotShopError


class CannotBuyOwnListingError(BrainrotShopError):
    def __init__(self):
        super().__init__("You cannot buy your own listing.")
