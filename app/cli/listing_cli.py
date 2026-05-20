def prompt_listing():
    print("What item would you like to list?")
    name: str = input("Enter name:")
    price: str = input("Enter price:")
    count: str = input("Enter count:")

    return {
        "name": name,
        "price": price,
        "count": count,
    }
