from app.exceptions.base_error import BrainrotShopError


class UserNotFoundError(BrainrotShopError):
    def __init__(self, user_id: int):
        super().__init__(f"User {user_id} does not exist.")


class DuplicateUsernameError(BrainrotShopError):

    def __init__(self, username: str):
        super().__init__(f"Username {username} is already taken.")


class InsufficientBalanceError(BrainrotShopError):
    def __init__(self, user_id: int, current_balance: float, required_amount: float):
        super().__init__(
            f"User {user_id} has insufficient funds. "
            f"Balance: ${current_balance}, "
            f"Required: ${required_amount}"
        )


class InvalidAmountError(BrainrotShopError):
    def __init__(self):
        super().__init__("Amount must be positive.")
