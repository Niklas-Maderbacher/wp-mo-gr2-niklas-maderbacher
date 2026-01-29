class MoodNotFoundException(Exception):
    """Exception raised when a mood entry is not found."""

    def __init__(self, mood_id: int):
        self.mood_id = mood_id
        self.message = f"Mood with ID {self.mood_id} not found."
        super().__init__(self.message)

class MoodCreationException(Exception):
    def __init__(self):
        self.message = "Can not create another mood for today, try updating it"
        super().__init__(self.message)