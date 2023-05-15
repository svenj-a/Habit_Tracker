import datetime
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
        self.date = datetime.datetime.today()
        self.completed_total = 0
        self.current_streak = 0
        self.longest_streak = 0
        self.goal = goal

    def create_habit(self, db):
        DB.add_habit(db, self.name, self.desc, self.period, self.date, self.completed_total, self.current_streak,
                     self.longest_streak, self.goal)

    def complete_habit(self, db, habit):
        """
        Increments the current day streak for the habit.
        :param db: an initialized sqlite3 database connection
        :param habit: name of the habit that was completed
        :return:
        """
        day_streak = db.cur.execute("SELECT current_streak FROM habits WHERE name=?", habit)
        day_streak += 1
        # update value in db!
        self._day_streak(db, habit)
        self._check_goal()

    def _day_streak(self, db, name):
        start_date = db.cur.execute("SELECT creation_date FROM habits WHERE name=?", name)
        current_date = datetime.datetime.today()
        self.current_streak = current_date - start_date
        print(self.current_streak)
        int_day_streak = self.current_streak.seconds//3600
        print(int_day_streak)
        if int_day_streak > self.longest_streak:
            self.longest_streak = self.current_streak

    def _break_habit(self):
        pass

    def _check_goal(self):
        if self.goal == self.longest_streak:
            print(f"Congratulations, you reached you goals for the habit '{self.name}'")

    def _reset_curr_streak(self, db):
        pass

    def delete_habit(self, name):
        pass
        # drop statement for entry by habit name (that must be the PK)
