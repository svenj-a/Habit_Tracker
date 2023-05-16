import os
import db
from habit import Habit


class TestHabit:

    def setup_method(self):
        self.db = db.get_db("test.db")
        db.add_habit(db, "test_habit_1", "This is a testing habit.", "daily")
        db.add_habit(db, "test_habit_2", "This is another testing habit.", "weekly")
        db.add_habit(db, "test_habit_3", "This is a third testing habit.", "monthly")

    def test_habit(self):
        habit = Habit("test_habit_1", "daily", 30)

        habit.day_streak()
        habit.complete_habit()
        habit.day_streak()
        habit.check_goal()

    def teardown_method(self):
        os.remove("test.db")
