from datetime import date
import db
# add docstrings and comments!!!!


class Habit:

    def __init__(self, name: str, period, goal: int):
        """
        The Habit class specifies the habit attributes. It can be used to create, complete, break and delete habits.
        Calculates the current day streak, updates the longest day streak if necessary and compares current state to the
        habit goal.
        """
        self.name = name
        self.period = period
        self.date = date.today()
        self.current_day_streak = 0
        self.longest_streak = 0
        self.goal = goal

    def create_habit(self, db):
        db.add_habit(db)

    def complete_habit(self, completion_date=None):
        if not completion_date:
            completion_date = date.today()
        self.current_day_streak += 1
        self.day_streak()
        self.check_goal()

    def break_habit(self):
        pass

    def day_streak(self):
        start_date = self.date
        current_date = date.today()
        self.current_day_streak = current_date - start_date
        print(self.current_day_streak)
        int_day_streak = self.current_day_streak.seconds//3600
        print(int_day_streak)
        if int_day_streak > self.longest_streak:
            self.longest_streak = self.current_day_streak

    def check_goal(self):
        if self.goal == self.longest_streak:
            print(f"Congratulations, you reached you goals for the habit {self.name}")

    def delete_habit(self):
        pass
