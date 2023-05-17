import datetime
from db import DB


class Habit:

    def __init__(self, name: str, description='', period='', goal=1):
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

    def complete_habit(self, db, name):
        """
        Increments the current day streak for the habit.
        :param db: an initialized sqlite3 database connection
        :param name: the name of the habit to be completed
        :return:
        """
        period = db.cur.execute("""SELECT periodicity FROM habits WHERE name=?""", (self.name,)).fetchall()
        self.period = period[0][0]
        curr_str = db.cur.execute("""SELECT current_streak FROM habits WHERE name=?""", (self.name,)).fetchall()
        self.current_streak = curr_str[0][0]
        lon_str = db.cur.execute("""SELECT longest_streak FROM habits WHERE name=?""", (self.name,)).fetchall()
        self.longest_streak = lon_str[0][0]
        if self.period == "daily":
            now = datetime.datetime.today()
            while True:
                try:
                    completed = db.cur.execute("""SELECT MAX(completion_date) FROM completions WHERE name=?""",
                                               (self.name,)).fetchall()
                    last = datetime.datetime.strptime(completed[0][0], '%Y-%m-%d %H:%M:%S.%f')
                    day_delta = (now - last).days
                    break
                except TypeError:
                    db.add_completion(name)
            if day_delta > 1:
                db.add_completion(name)
                self.current_streak = 1  # insert same for longest day streak and check goal!!! Put more code in other methods...
                db.update_curr_streak(self.name, self.current_streak)
                print(f"You broke the habit {self.name} and lost your day streak. "
                      f"Your new streak is {self.current_streak}!")
            elif day_delta < 1 and self.current_streak > 0:
                print("You have already completed this habit! Come back tomorrow...")
            else:
                db.add_completion(name)
                self.current_streak += 1
                db.update_curr_streak(self.name, self.current_streak)
                print(f"Congratulations! You have checked off your habit {self.name} "
                      f"and gained a streak of {self.current_streak} day(s)!")
        elif period[0] == "weekly":
            pass
        elif period[0] == "monthly":
            pass

    def _day_streak(self, db):
        pass

        # start_date = db.cur.execute("SELECT creation_date FROM habits WHERE name=?", self.name)
        # current_date = datetime.datetime.today()
        # self.current_streak = current_date - start_date
        # print(self.current_streak)
        # int_day_streak = self.current_streak.seconds//3600
        # print(int_day_streak)
        # if int_day_streak > self.longest_streak:
        #     self.longest_streak = self.current_streak

    def _check_longest(self):
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

    def _check_goal(self):
        if self.goal == self.longest_streak:
            print(f"Congratulations, you reached you goals for the habit '{self.name}'")

    def _reset_curr_streak(self, db):
        pass

    def delete_habit(self, db, name):
        db.drop_habit(name)
