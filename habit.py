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

    def complete_habit(self, db, name):
        """
        Increments the current day streak for the habit.
        :param db: an initialized sqlite3 database connection
        :param name: the name of the habit to be completed
        :return:
        """
        habit = self._fetch_habit_data(db, name)
        completed = datetime.today()
        last_completed = db.cur.execute("""SELECT MAX(completion_date) FROM completions WHERE name=?""",
                                        (self.name,)).fetchall()
        try:
            last = datetime.strptime(last_completed[0][0], "%Y-%m-%d %H:%M:%S.%f")
            timedelta = self._calculate_timedelta(habit, completed, last)
            self._day_streak(db, habit, timedelta)
            self._check_records(habit)
        except TypeError or ValueError:
            self._first_time_completion(db, habit)

    def _fetch_habit_data(self, db, name):
        values = db.cur.execute("""SELECT * FROM habits WHERE name=?""", (name,)).fetchall()[0]
        habit_attributes = []
        for value in values:
            habit_attributes.append(value)
        habit = Habit(*habit_attributes)
        return habit

    def _first_time_completion(self, db, habit):
        db.add_completion(habit.name)
        habit.current_streak, habit.longest_streak, habit.completed_total = 1, 1, 1
        db.update_streaks(habit.name, habit.current_streak, habit.longest_streak, habit.completed_total)
        return habit.current_streak, habit.longest_streak, habit.completed_total

    def _calculate_timedelta(self, habit, completed, last):
        timedelta = None
        timespan = None
        if habit.period == "daily":
            timedelta = (completed.day - last.day)
            timespan = "day(s)"
        elif habit.period == "weekly":
            timedelta = (completed.isocalendar()[1] - last.isocalendar()[1])
            timespan = "week(s)"
        elif habit.period == "monthly":
            timedelta = (completed.month - last.month)
            timespan = "month(s)"
        return timedelta, timespan

    def _day_streak(self, db, habit, timedelta):
        """
        Checks whether the habit is completed, broken or unavailable (in case it was already completed in the current
        period) and calls the respective helper methods.
        :param db: name of the database
        :param timedelta: the day/week/month delta calculated in complete_habit()
        :param habit: name of the habit
        :return:
        """
        if timedelta > 1:
            db.add_completion(habit)
            habit.current_streak = 1
            db.update_streaks(habit.name, habit.current_streak, habit.longest_streak, habit.completed_total)
            return habit.current_streak
        elif timedelta < 1:
            print(f"You have already completed this {habit.period} habit! Try again later...")
        else:
            db.add_completion(habit)
            habit.current_streak += 1
            self._check_records(habit)
            db.update_streaks(habit.name, habit.current_streak, habit.longest_streak, habit.completed_total)
            return habit.current_streak
            # print(f"Congratulations! You have checked off your habit '{habit.name}' "
            #       f"and gained a streak of {habit.current_streak} {timespan}!")

    def _increment_completed_total(self, db, habit):
        """
        Increments the current day streak in case the user checked off a habit successfully and updates the streaks if
        necessary.
        :param db: name of the database
        :param habit:
        :return:
        """
        habit.completed_total += 1
        db.update_streaks(self.name, self.current_streak, self.longest_streak, self.completed_total)
        self._check_records()
        return habit.completed_total
        # print(f"Congratulations! You have checked off your habit '{self.name}' "
        #       f"and gained a streak of {self.current_streak} {timespan}!")

    def _check_records(self, habit):
        """
        Checks whether the longest day streak needs updating and whether the final goal is reached.
        :return:
        """
        if habit.current_streak > habit.longest_streak:
            habit.longest_streak = habit.current_streak
            return habit.current_streak, habit.longest_streak

        if habit.goal < habit.longest_streak:
            to_go = habit.goal - habit.longest_streak
            return to_go
            # print(f"Keep it going, you have {to_go} time(s) to go until you reach your final goal!")
        elif habit.goal == habit.longest_streak:
            print(f"Congratulations, you reached your final goal for the habit '{habit.name}'")

    def delete_habit(self, db, name):
        """
        Call to the database method to delete a habit.
        :param db: name of the database
        :param name: name of the habit to be deleted
        :return:
        """
        db.drop_habit(name)
