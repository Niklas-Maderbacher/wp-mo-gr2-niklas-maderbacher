class ActivityCategoryAlreadyExistsException(Exception):
    def __init__(self):
        self.message = "An Activity Category with this name already exists"
        super().__init__(self.message)

class NoActivityCategoriesExsitsYetException(Exception):
    def __init__(self):
        self.message = "No Activity Categories exists yet. Please feel free to create one"
        super().__init__(self.message)

class ActivityCategoryNotFoundException(Exception):
    def __init__(self, id):
        self.id = id
        self.message = f"No Activity Category with id: {id} exists"
        super().__init__(self.message)