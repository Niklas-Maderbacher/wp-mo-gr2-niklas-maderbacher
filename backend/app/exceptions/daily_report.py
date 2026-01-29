class DailyReportDateNotFoundException(Exception):
    def __init__(self, date):
        self.date = date
        self.message = f"No daily report for date: {date} exsists"
        super().__init__(self.message)

class DailyReportIdNotFoundException(Exception):
    def __init__(self, id):
        self.id = id
        self.message = f"No daily report with id: {id} exists"
        super().__init__(self.message)