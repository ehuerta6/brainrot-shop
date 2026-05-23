from services.market_service import MarketService

market_service = MarketService()


def prompt_buy_listing(current_user_id: int) -> None:
    print("\n--- Buy Listing ---")

    try:
        listing_id = int(input("Listing ID to buy: "))
    except ValueError:
        print("Error: Listing ID must be an integer.")
        return

    try:
        purchase_summary = market_service.buy_listing(listing_id, current_user_id)
        print(f"\nPurchase successful!")
        print(f"  Listing ID: {purchase_summary['listing_id']}")
        print(f"  Item ID:    {purchase_summary['item_id']}")
        print(f"  Seller ID:  {purchase_summary['seller_id']}")
        print(f"  Price:      ${purchase_summary['price']:.2f}")
    except ValueError as error:
        print(f"Error: {error}")
