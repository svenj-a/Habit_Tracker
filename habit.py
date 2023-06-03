from datetime import datetime


class Habit:

    def __init__(self, name: str, description='no description', period='daily',
                 goal=100, creation_date=datetime.today()):
        """
        The Habit class specifies the habit attributes. It can create, complete, and delete habits.
        Helper methods calculate the current day streak, update the longest day streak if necessary and compare the
        current state to the final goal.
        :param name: name of the habit (str); provided by user input
        :param description: description of the habit (str); provided by user input
        :param period: periodicity of the habit (str); selected by user input from ("daily", "weekly", "monthly")
        :param goal: final goal; How often is the habit to be completed until it is established? (int); provided by user
                input
        """
        self.name = name
        self.desc = description
        self.period = period
        self.date = creation_date
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
        db.add_habit(self.name, self.desc, self.period, self.date, self.completed_total, self.current_streak,
                     self.longest_streak, self.goal)

    def get_habit(self):
        pass

    def complete_habit(self, db, name, completed=datetime.today()):
        """
        Increments the current day streak for the habit.
        :param db: an initialized sqlite3 database connection
        :param name: the name of the habit to be completed
        :param completed: time of completion, default value is the current time
               (a different time can be inserted for testing)
        :return:
        """
        # Fetch habit attributes from db.
        period = db.cur.execute("""SELECT periodicity FROM habits WHERE name=?""", (self.name,)).fetchall()
        self.period = period[0][0]
        goal = db.cur.execute("""SELECT final_goal FROM habits WHERE name=?""", (self.name,)).fetchall()
        self.goal = goal[0][0]
        curr_str = db.cur.execute("""SELECT current_streak FROM habits WHERE name=?""", (self.name,)).fetchall()
        self.current_streak = curr_str[0][0]
        lon_str = db.cur.execute("""SELECT longest_streak FROM habits WHERE name=?""", (self.name,)).fetchall()
        self.longest_streak = lon_str[0][0]
        comp_tot = db.cur.execute("""SELECT completed_total FROM habits WHERE name=?""", (self.name,)).fetchall()
        self.completed_total = comp_tot[0][0]

        # Get timestamp of last completion.
        last_completion = db.cur.execute("""SELECT MAX(completion_date) FROM completions WHERE name=?""",
                                         (self.name,)).fetchall()
        timedelta = None
        timespan = None
        # Perform first completion
        try:
            last = datetime.strptime(last_completion[0][0], "%Y-%m-%d %H:%M:%S.%f")
        except TypeError or ValueError:
            db.add_completion(name)
            self.current_streak = 1
            self.longest_streak = 1
            self.completed_total = 1
            db.update_streaks(name, self.current_streak, self.longest_streak, self.completed_total)
            return self.current_streak, self.longest_streak, self.completed_total
        # Check off daily, weekly or monthly habits with the according streak calculations.
        if self.period == "daily":
            timedelta = (completed.day - last.day)
            timespan = "day(s)"
        elif self.period == "weekly":
            timedelta = (completed.isocalendar()[1] - last.isocalendar()[1])
            timespan = "week(s)"
        elif self.period == "monthly":
            timedelta = (completed.month - last.month)
            timespan = "month(s)"
        # self._day_streak(db, timedelta, timespan, name)
        if timedelta > 1:
            # self._reset_curr_streak(db)
            db.add_completion(name)
            self.current_streak = 1
            db.update_streaks(self.name, self.current_streak, self.longest_streak, self.completed_total)
            return self.current_streak, self.longest_streak, self.completed_total
            print(f"You broke the habit '{self.name}' and lost your day streak. "
                  f"Your new streak is {self.current_streak}!")

        elif timedelta < 1 and self.current_streak > 0:
            return self.current_streak, self.longest_streak, self.completed_total
            print(f"You have already completed this {self.period} habit! Try again later...")
        else:
            db.add_completion(name)
            self.current_streak += 1
            # self._check_records()
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak

            if self.goal > self.longest_streak:
                to_go = self.goal - self.longest_streak
                return to_go
                print(f"Keep it going, you have {to_go} time(s) to go until you reach your final goal!")
            elif self.goal == self.longest_streak:
                print(f"Congratulations, you reached your final goal for the habit '{self.name}'")
            db.update_streaks(self.name, self.current_streak, self.longest_streak, self.completed_total)
            return self.current_streak, self.longest_streak, self.completed_total
            print(f"Congratulations! You have checked off your habit '{self.name}' "
                  f"and gained a streak of {self.current_streak} {timespan}!")

    # def _day_streak(self, db, timedelta, timespan, habit):
    #     """
    #     Checks whether the habit is completed, broken or unavailable (in case it was already completed in the current
    #     period) and calls the respective helper methods.
    #     :param db: name of the database
    #     :param timedelta: the day/week/month delta calculated in complete_habit()
    #     :param timespan: the string according to the periodicity that can be inserted in formatted strings
    #     :param habit: name of the habit
    #     :return:
    #     """
    #     if timedelta > 1:
    #         self._reset_curr_streak(db)
    #         db.add_completion(habit)
    #     elif timedelta < 1 and self.current_streak > 0:
    #         print(f"You have already completed this {self.period} habit! Try again later...")
    #     else:
    #         self.current_streak += 1
    #         self._check_records()
    #         db.update_streaks(self.name, self.current_streak, self.longest_streak, self.completed_total)
    #         print(f"Congratulations! You have checked off your habit '{self.name}' "
    #               f"and gained a streak of {self.current_streak} {timespan}!")
    #         db.add_completion(habit)

    # def _reset_curr_streak(self, db):
    #     """
    #     Resets the current day streak in case the user broke the habit.
    #     :param db: name of the database
    #     :return:
    #     """
    #     self.current_streak = 1
    #     db.update_streaks(self.name, self.current_streak, self.longest_streak, self.completed_total)
    #     print(f"You broke the habit '{self.name}' and lost your day streak. "
    #           f"Your new streak is {self.current_streak}!")

    # def _increment_curr_streak(self, db, timespan):
    #     """
    #     Increments the current day streak in case the user checked off a habit successfully and updates the streaks if
    #     necessary.
    #     :param db: name of the database
    #     :param timespan: the string according to the periodicity that can be inserted in formatted strings
    #     :return:
    #     """
    #     self.current_streak += 1
    #     self._check_records()
    #     db.update_streaks(self.name, self.current_streak, self.longest_streak, self.completed_total)
    #     print(f"Congratulations! You have checked off your habit '{self.name}' "
    #           f"and gained a streak of {self.current_streak} {timespan}!")

    # def _check_records(self):
    #     """
    #     Checks whether the longest day streak needs updating and whether the final goal is reached.
    #     :return:
    #     """
    #     if self.current_streak > self.longest_streak:
    #         self.longest_streak = self.current_streak
    #
    #     if self.goal < self.longest_streak:
    #         to_go = self.goal - self.longest_streak
    #         print(f"Keep it going, you have {to_go} time(s) to go until you reach your final goal!")
    #     elif self.goal == self.longest_streak:
    #         print(f"Congratulations, you reached your final goal for the habit '{self.name}'")
