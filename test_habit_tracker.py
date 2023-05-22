import os

from db import DB
from habit import Habit
import analysis


class TestHabitTracker:


    def setup_method(self):
        self.db = DB("test.db")
        self.db.get_db()

        habit1 = Habit('sleep', 'Sleep at least 7h per day.', 'daily', 30)
        habit1.create_habit(self.db)
        habit2 = Habit('brush teeth', 'Brush teeth every morning.', 'daily', 28)
        habit2.create_habit(self.db)
        habit3 = Habit('clean bathroom', 'Clean the bathroom including toilet, shower, and sink.', 'weekly', 8)
        habit3.create_habit(self.db)
        habit4 = Habit('call mom', 'Call my mother once a month...', 'monthly', 4)
        habit4.create_habit(self.db)
        habit5 = Habit('meditate', 'Meditate at least 10 minutes every day after lunch.', 'daily', 60)
        habit5.create_habit(self.db)

    def test_habit(self):
        habit = Habit("test_habit_1", "test_description_1")
        habit.create_habit(self.db)
        habit.complete_habit(self.db, habit)

        data = analysis.list_all_habits(self.db)
        assert len(data) == 6

    def test_db(self):
        pass

    def test_analysis(self):
        pass

    def teardown_method(self):
        os.remove("test.db")
