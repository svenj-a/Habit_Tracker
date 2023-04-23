from datetime import date
from db import DB
# add docstrings and comments!!!!


class Habit:

    def __init__(self, name: str, description: str, period: str, goal: int):
        """
        The Habit class specifies the habit attributes. It can be used to create, complete, break and delete habits.
        Calculates the current day streak, updates the longest day streak if necessary and compares current state to the
        habit goal.
        """

        self.name = name
        self.desc = description
        self.period = period
        self.date = date.today()
        self.curr_streak = 0
        self.long_streak = 0
        self.goal = goal

    def create_habit(self, db):
        DB.add_habit(db, self.name, self.desc, self.period, self.date, self.curr_streak, self.long_streak, self.goal)

    def complete_habit(self, habit):
        """
        Increments the current day streak for the habit.
        :param habit: name of the habit that was completed
        :return:
        """
        day_streak = DB.cur.execute("SELECT current_day_streak FROM habits WHERE habit_name = habit")
        day_streak += 1
        # update value in db!
        self.day_streak()
        self.check_goal()


    def day_streak(self, name):
        start_date = DB.cur.execute("SELECT creation_date FROM habits WHERE habit_name = name")
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

    def break_habit(self):
        pass

    def reset_curr_streak(self, db):
        pass

    def delete_habit(self, name):
        pass
        # drop statement for entry by habit name (that must be the PK)
