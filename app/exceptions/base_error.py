class BrainrotShopError(Exception):

    def __init__(
        self,
        message: str = "An unexpected error occurred.",
        error_code: str | None = None,
    ):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
