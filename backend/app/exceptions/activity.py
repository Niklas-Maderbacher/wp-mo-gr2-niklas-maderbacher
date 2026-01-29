class ActivityNotFoundException(Exception):
    """Exception raised when an activity is not found."""

    def __init__(self, activity_id: int):
        self.activity_id = activity_id
        self.message = f"Activity with ID {self.activity_id} not found"
        super().__init__(self.message)