from datetime import datetime


class Habit:

    def __init__(self, name, desc="", period="daily", date=datetime.today(), completed_total=0, cur_streak=0,
                 lon_streak=0, goal=100):
        """
        The Habit class specifies all habit attributes. It can create and complete habits.
        Helper methods are included to break down the different steps of the complete_habit() method.
        :param name:
        :param desc:
        :param period:
        :param date:
        :param completed_total:
        :param cur_streak:
        :param lon_streak:
        :param goal:
        """
        self.name = name
        self.desc = desc
        self.period = period
        self.date = date
        self.completed_total = completed_total
        self.current_streak = cur_streak
        self.longest_streak = lon_streak
        self.goal = goal

    def create_habit(self, db):
        """
        Takes in all values necessary to create a habit and passes them to the respective db method.
        :param db: name of the actual database
        :return:
        """
        db.add_habit(self.name, self.desc, self.period, self.date, self.completed_total, self.current_streak,
                     self.longest_streak, self.goal)
        return self

    def fetch_habit_data(self, db):
        values = db.cur.execute("""SELECT * FROM habits WHERE name=?""", (self.name,)).fetchall()[0]
        habit_attributes = []
        for value in values:
            habit_attributes.append(value)
        habit = Habit(*habit_attributes)
        return habit

    def complete_habit(self, db):
        """
        Increments the current day streak for the habit.
        :param db: an initialized sqlite3 database connection
        :return:
        """
        # habit = self.fetch_habit_data(db, name)
        completed = datetime.today()
        last_completed = db.cur.execute("""SELECT MAX(completion_date) FROM completions WHERE name=?""",
                                        (self.name,)).fetchall()
        try:
            last = datetime.strptime(last_completed[0][0], "%Y-%m-%d %H:%M:%S.%f")
            timedelta, timespan = self._calculate_timedelta(completed, last)
            self._streak(db, timedelta)
        except TypeError or ValueError:
            self._first_time_completion(db)
        return self

    def _first_time_completion(self, db):
        db.add_completion(self.name)
        self.current_streak, self.longest_streak, self.completed_total = 1, 1, 1
        db.update_streaks(self.name, self.current_streak, self.longest_streak, self.completed_total)
        return self
        # print(f"Congratulations, you completed the habit {habit.name} for the first time!"

    def _calculate_timedelta(self, completed, last):
        timedelta = None
        timespan = None
        if self.period == "daily":
            timedelta = (completed.day - last.day)
            timespan = "day(s)"
        elif self.period == "weekly":
            timedelta = (completed.isocalendar()[1] - last.isocalendar()[1])
            timespan = "week(s)"
        elif self.period == "monthly":
            timedelta = (completed.month - last.month)
            timespan = "month(s)"
        return timedelta, timespan

    def _streak(self, db, timedelta):
        """
        Checks whether the habit is completed, broken or unavailable (in case it was already completed in the current
        period) and calls the respective helper methods.
        :param db: name of the database
        :param timedelta: the day/week/month delta calculated in complete_habit()
        :return:
        """
        if timedelta > 1:
            self._break_habit(db)
        elif timedelta < 1:
            self._completion_cooldown()
        else:
            self._check_off_habit(db)

    def _break_habit(self, db):
        db.add_completion(self)
        self.completed_total += 1
        self.current_streak = 1
        db.update_streaks(self.name, self.current_streak, self.longest_streak, self.completed_total)
        return self
        # print(f"You broke the habit {habit.name}! Your streak was reset to 1. Try again, you can do it!!")

    def _completion_cooldown(self):
        # update timestamp of last completion entry
        return self
        # print(f"You have already completed this {habit.period} habit! Try again later...")

    def _check_off_habit(self, db):
        db.add_completion(self)
        self.completed_total += 1
        self.current_streak += 1
        self._check_longest_streak()
        self._check_goal()
        db.update_streaks(self.name, self.current_streak, self.longest_streak, self.completed_total)
        return self
        # print(f"Congratulations! You have checked off your habit '{self.name}' "
        #       f"and gained a streak of {self.current_streak} {timespan}!")

    def _check_longest_streak(self):
        """
        Checks whether the longest day streak needs updating and whether the final goal is reached.
        :return:
        """
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        return self

    def _check_goal(self):
        if self.longest_streak < self.goal:
            to_go = self.goal - self.longest_streak
            return to_go
            # print(f"Keep it going, you have {to_go} time(s) to go until you reach your final goal!")
        elif self.goal == self.longest_streak:
            return self.goal
            # print(f"Congratulations, you reached your final goal for the habit '{habit.name}'")

    # @staticmethod
    # def delete_habit(db, name):
    #     """
    #     Call to the database method to delete a habit.
    #     :param db: name of the database
    #     :param name: name of the habit to be deleted
    #     :return:
    #     """
    #     db.drop_habit(name)
