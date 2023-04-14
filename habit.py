from datetime import date
# add docstrings and comments!!!!


class Habit:

    def __init__(self, name: str, period, goal: int):
        self.name = name
        self.period = period
        self.date = date.today()
        self.day_streak = 0
        self.longest_streak = 0
        self.goal = goal

    def create_habit(self):
        pass

    def check_habit(self, completion_date=None):
        if not completion_date:
            completion_date = date.today()
        self.day_streak += 1
        self.habit_day_streak()
        self.check_goal()

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

    def check_goal(self):
        if self.goal == self.longest_streak:
            print(f"Congratulations, you reached you goals for the habit {self.name}")

    def delete_habit(self):
        pass
