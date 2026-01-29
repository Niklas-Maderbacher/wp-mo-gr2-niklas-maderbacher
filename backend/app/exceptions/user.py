class UserNotFoundException(Exception):
    """Exception raised when a user is not found in the database."""

    def __init__(self, id: int):
        self.id = id
        self.message = f"User with id: {id} not found"
        super().__init__(self.message)


class UserExistsException(Exception):
    """Exception raised when attempting to create a user that already exists."""

    def __init__(self, message: str = "User already exists"):
        self.message = message
        super().__init__(self.message)

