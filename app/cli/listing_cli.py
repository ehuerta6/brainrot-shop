from app.services.listing_service import ListingService

listing_service = ListingService()


def prompt_create_listing() -> None:
    print("\n--- Create Listing ---")

    try:
        item_id = int(input("Item ID to list: "))
    except ValueError:
        print("Error: Item ID must be an integer.")
        return

    try:
        seller_id = int(input("Seller ID (owner): "))
    except ValueError:
        print("Error: Seller ID must be an integer.")
        return

    try:
        price = float(input("Listing price: "))
    except ValueError:
        print("Error: Price must be a number.")
        return

    try:
        listing = listing_service.create_listing(item_id, seller_id, price)
        print(f"\nListing created!")
        print(f"  Listing ID: {listing['listing_id']}")
        print(f"  Item ID:    {listing['item_id']}")
        print(f"  Seller ID:  {listing['seller_id']}")
        print(f"  Price:      ${listing['price']:.2f}")
    except ValueError as error:
        print(f"Error: {error}")


def prompt_view_active_listings() -> None:
    print("\n--- Active Listings ---")
    listings = listing_service.get_active_listings()

    if not listings:
        print("No active listings.")
        return

    for listing in listings:
        print(
            f"  [{listing['listing_id']}] Item #{listing['item_id']} | ${listing['price']:.2f} | seller={listing['seller_id']}"
        )


def prompt_cancel_listing() -> None:
    print("\n--- Cancel Listing ---")

    try:
        listing_id = int(input("Listing ID to cancel: "))
    except ValueError:
        print("Error: Listing ID must be an integer.")
        return

    if listing_service.cancel_listing(listing_id):
        print(f"Listing {listing_id} cancelled.")
    else:
        print(f"Listing {listing_id} not found.")
