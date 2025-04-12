from datetime import datetime

class Wait:
    def __init__(self):
        self.start_time = datetime.now()
        self.level = 0

    def check(self):
        """ Get seconds from original time """
        current_time = datetime.now()
        elapsed_seconds = (current_time - self.start_time).total_seconds() - self.level
        return elapsed_seconds
    def leveled(self, start_level:int):
        self.level = (datetime.now() - start_level).total_seconds()