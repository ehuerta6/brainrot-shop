from app.models.marketplace_listing import MarketplaceListing


class TestMarketplaceListingModel:
    def test_create_listing_has_default_active_true(self):
        listing = MarketplaceListing(
            listing_id=1, seller_id=1, item_id=1, price=50.0, created_at="2026-01-01T00:00:00"
        )
        assert listing.active is True

    def test_create_listing_with_all_fields(self):
        listing = MarketplaceListing(
            listing_id=3, seller_id=2, item_id=7, price=120.0, created_at="2026-05-20T12:00:00", active=False
        )
        assert listing.listing_id == 3
        assert listing.seller_id == 2
        assert listing.item_id == 7
        assert listing.price == 120.0
        assert listing.created_at == "2026-05-20T12:00:00"
        assert listing.active is False

    def test_listing_model_dump_returns_dict(self):
        listing = MarketplaceListing(
            listing_id=1, seller_id=1, item_id=1, price=25.0, created_at="2026-01-01T00:00:00"
        )
        data = listing.model_dump()
        assert isinstance(data, dict)
        assert data["price"] == 25.0
