import datetime
from db import DB


class Habit:

    def __init__(self, name: str, description: str, period: str, goal: int):
        """
        The Habit class specifies the habit attributes. It can create, complete, and delete habits.
        Helper methods calculate the current day streak, update the longest day streak if necessary and compare the
        current state to the final goal.
        :param name: name of the habit (str); provided by user input
        :param description: description of the habit (str); provided by user input
        :param period: periodicity of the habit (str); selected by user input from ("daily", "weekly", "monthly")
        :param goal: final goal: How often is the habit to be completed until it is established? (int); provided by user
                input
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
        """
        Takes in all values necessary to create a habit and passes them to the respective db method.
        :param db: name of the actual database
        :return:
        """
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
