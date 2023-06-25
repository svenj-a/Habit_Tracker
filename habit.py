from datetime import datetime


class Habit:

    def __init__(self, name, desc="", period="daily", date=datetime.today(), completed_total=0, cur_streak=0,
                 lon_streak=0, goal=100, goal_reached=False):
        """
        The Habit class specifies all habit attributes. It can create new habits or fetch existing habits from the
        database and complete habits. Helper methods are included to break down the different steps of the
        complete_habit() method.
        :param name: Name of the habit. Required, no default, provided by user input. Type str.
        :param desc: Short description of the habit. Default is an empty string, provided by user input. Type str.
        :param period: Periodicity of the habit. Default is "daily", other possible values are "weekly" and "monthly",
                       can be selected by the user at habit creation through selection menu. Type str.
        :param date: Creation date of the habit. Default at habit creation is the current timestamp. Other values can be
                     inserted for testing purposes. Type timestamp.
        :param completed_total: Counts overall completions of a habit. Default at habit creation is 0. Other values can
                                be inserted for testing purposes. Type int.
        :param cur_streak: Counts the current day streak of a habit. Default at habit creation is 0. Other values can be
                           inserted for testing purposes. Type int.
        :param lon_streak: Saves the longest day streak ever reached for a habit. Default at habit creation is 0. Other
                           values can be inserted for testing purposes. Type int.
        :param goal: Final goal for a habit. If the current day streak reaches the goal, then the habit is seen as
                     established. Default values is 100, provided by user input. Type int.
        :param goal_reached: Indicates where a habit is established. Default at habit creation is False. Other values
                             can be inserted for testing purposes. Type boolean.
        """
        self.name = name
        self.desc = desc
        self.period = period
        self.date = date
        self.completed_total = completed_total
        self.current_streak = cur_streak
        self.longest_streak = lon_streak
        self.goal = goal
        self.goal_reached = goal_reached

    def create_habit(self, db):
        """
        Takes in all necessary values to create a habit and passes them to the corresponding database method.
        :param db: name of the database connection
        :return: a habit object
        """
        db.add_habit(self.name, self.desc, self.period, self.date, self.completed_total, self.current_streak,
                     self.longest_streak, self.goal, self.goal_reached)
        return self

    def fetch_habit_data(self, db):
        """
        Fetches all habit data for a specified habit from the database to create a habit object for a saved habit.
        :param db: name of the database connection
        :return: a habit object
        """
        values = db.cur.execute("""SELECT * FROM habits WHERE name=?""", (self.name,)).fetchall()[0]
        habit_attributes = []
        for value in values:
            habit_attributes.append(value)
        habit = Habit(*habit_attributes)
        return habit

    def complete_habit(self, db, completed=datetime.today()):
        """
        Fetches the last completion date from the completions table and compares the current completion date against it.
        Calls the corresponding functions to either break the habit, check off the habit or do nothing when the habit is
        on completion cooldown (i.e. has already been completed in the specified period).
        :param db: name of the database connection
        :param completed: Timestamp of the completion event. Default is the current timestamp, other values can be
                          inserted for testing purposes.
        :return: a habit object
        """
        last_completed = db.cur.execute("""SELECT MAX(completion_date) FROM completions WHERE name=?""",
                                        (self.name,)).fetchall()
        try:
            last = datetime.strptime(last_completed[0][0], "%Y-%m-%d %H:%M:%S.%f")
            timedelta, timespan = self._calculate_timedelta(completed, last)
            self._streak(db, timedelta, timespan, completed)
        except TypeError or ValueError:
            self._first_time_completion(db, completed)
        return self

    def _first_time_completion(self, db, date):
        """
        Is called if there is no completion entry in the completions table for a habit. Completes the habit for the
        first time and sets the values for completed_total, longest_streak and current_streak to 1.
        :param db: name of the database connection
        :param date: timestamp for the first completion entry in the completions table
        :return: a habit object
        """
        db.add_completion(self.name, date)
        self.current_streak, self.longest_streak, self.completed_total = 1, 1, 1
        db.update_streaks(self.name, self.current_streak, self.longest_streak, self.completed_total)
        print(f"Congratulations, you completed the habit '{self.name}' for the first time!")
        return self

    def _calculate_timedelta(self, completed, last_completed):
        """
        Is called if there is at least one completion entry in the completions table. Calculates the timespan between
        the last completion and the current completion event according to the periodicity of the habit.
        :param completed: timestamp of current completion event
        :param last_completed: timestamp of last completion event
        :return: time difference between both events as timedelta, a string corresponding to the periodicity as timespan
        """
        timedelta = None
        timespan = None
        if self.period == "daily":
            timedelta = (completed.day - last_completed.day)
            timespan = "day(s)"
        elif self.period == "weekly":
            timedelta = (completed.isocalendar()[1] - last_completed.isocalendar()[1])
            timespan = "week(s)"
        elif self.period == "monthly":
            timedelta = (completed.month - last_completed.month)
            timespan = "month(s)"
        return timedelta, timespan

    def _streak(self, db, timedelta, timespan, date):
        """
        Checks whether the habit is checked off, broken or unavailable for completion (in case it was already completed
        in the specified period it is "on cooldown") and calls the corresponding function.
        :param db: name of the database connection
        :param timedelta: a timedelta calculated in _calculate_timedelta()
        :param timespan: a string corresponding to the periodicity, used for print statements
        :param date: timestamp of current completion event
        :return: a habit object
        """
        if timedelta > 1:
            self._break_habit(db, date)
        elif timedelta < 1:
            self._completion_cooldown()
        else:
            self._check_off_habit(db, date, timespan)
        return self

    def _break_habit(self, db, date):
        """
        Breaks the habit if the habit was not completed once within the specified period (timedelta >1), i.e. a
        completion event is added and completed_total is increased by 1. The current day streak is reset to 1.
        :param db: name of the database connection
        :param date: timestamp of the current completion event
        :return: a habit object
        """
        db.add_completion(self.name, date)
        self.completed_total += 1
        self.current_streak = 1
        db.update_streaks(self.name, self.current_streak, self.longest_streak, self.completed_total)
        print(f"You broke the habit '{self.name}'! Your streak was reset to 1. Try again, you can do it!!")
        return self

    def _completion_cooldown(self):
        """
        The habit cannot be completed, if the time difference between the current and last completion is <1. A message
        is printed to the user.
        :return: a habit object
        """
        # development idea: update timestamp of last completion entry when habit is completed multiple times
        print(f"You have already completed this {self.period} habit! Try again later...")
        return self

    def _check_off_habit(self, db, date, timespan):
        """
        The habit is checked off successfully if the time difference between the current and last completion is exactly
        1. A completion event is added and the values of completed_total and current_streak are incremented by 1. It is
        checked whether the new streak is no longer that the longest streak and whether the final goal has been reached.
        :param db: name of the database connection
        :param date: timestamp of the current completion event
        :param timespan: a string corresponding to the periodicity, used for print statements
        :return: a habit object
        """
        db.add_completion(self.name, date)
        self.completed_total += 1
        self.current_streak += 1
        print(self.longest_streak)
        self._check_longest_streak()
        print(self.longest_streak)
        self._check_goal(db)
        db.update_streaks(self.name, self.current_streak, self.longest_streak, self.completed_total)
        print(f"Congratulations! You have checked off your habit '{self.name}' "
              f"and gained a streak of {self.current_streak} {timespan}!")
        return self

    def _check_longest_streak(self):
        """
        Updates the longest day streak in case the new current day streak is greater.
        :return: a habit object
        """
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        return self

    def _check_goal(self, db):
        """
        Updates the boolean value of established, if the longest day streak now equals the final goal (the habit can
        then be displayed as established habit using the analysis module). Calculates the difference otherwise and
        prints a message to the user.
        :param db: name of the database connection
        :return: a habit object
        """
        if self.longest_streak < self.goal:
            to_go = self.goal - self.longest_streak
            print(f"Keep it going, you have {to_go} time(s) to go until you reach your final goal!")
            return self
        elif self.goal == self.longest_streak:
            self.goal_reached = True
            db.update_established(self.goal_reached, self.name)
            print(f"Congratulations, you reached your final goal for the habit '{self.name}'")
            return self
