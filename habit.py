from datetime import date   # import in main.py and delete here
# add docstrings and comments!!!!


class Habit:

    def __init__(self, name: str, period):
        self.name = name
        self.period = period
        self.date = date.today()
        self.day_streak = 0
        self.longest_streak = 0

    def create_habit(self):
        pass

    def check_habit(self):
        pass

    def break_habit(self):
        pass

    def habit_day_streak(self):
        start_date = self.date
        current_date = date.today()
        self.day_streak = current_date - start_date
        print(self.day_streak)
        int_day_streak = self.day_streak.seconds//3600
        print(int_day_streak)
        if int_day_streak > self.longest_streak:
            self.longest_streak = self.day_streak

    def delete_habit(self):
        pass
