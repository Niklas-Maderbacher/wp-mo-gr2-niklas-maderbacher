class SleepNotFoundException(Exception):
    def __init__(self, sleep_id: int):
        self.sleep_id = sleep_id
        self.message = f"Sleep entry with ID {sleep_id} not found."
        super().__init__(self.message)

class SleepCreationException(Exception):
    def __init__(self):
        self.message = f"Failed to create sleep entry: Already exists."
        super().__init__(self.message)