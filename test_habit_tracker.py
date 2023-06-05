import pytest
# from freezegun import freeze_time

from db import DB
from habit import Habit
import analysis

# https://stackoverflow.com/questions/23988853/how-to-mock-set-system-date-in-pytest


@pytest.fixture(autouse=True)
def db():
    db = DB(":memory:")
    return db


@pytest.fixture(autouse=True)
def create_habits(db):
    Habit(name='sleep', desc='Sleep at least 7h per day.', period='daily', goal=30, ).create_habit(db)
    Habit(name='brush teeth', desc='Brush teeth every morning.', period='daily', goal=28).create_habit(db)
    Habit(name='clean bathroom', desc='Clean the bathroom including toilet, shower, and sink.', period='weekly', goal=8
          ).create_habit(db)
    Habit(name='call mom', desc='Call my mother once a month...', period='monthly', goal=4).create_habit(db)
    Habit(name='meditate', desc='Meditate at least 10 minutes every day after lunch.', period='daily', goal=60
          ).create_habit(db)


# @pytest.fixture(autouse=True)
# def completion_loop(db):  # put lists in a dict
#     completions_sleep = []
#     completions_brush_teeth = []
#     completions_clean_bathroom = []
#     completions_call_mom = []
#     completions_meditate = []
#     for date in completions_sleep:
#         @freeze_time(date)
#         def add_completion_data(name):
#             Habit.complete_habit(db, name)


class TestHabit:

    def test_create_habit(self, db):
        habit = Habit(name="diary", desc="Write a diary entry every evening.", period="daily", goal=14).create_habit(db)
        assert habit.name == "diary"

    def test_fetch_habit_data(self, db):
        habit = Habit(name="sleep")
        assert habit.goal == 100
        habit = Habit(name="sleep").fetch_habit_data(db)
        assert habit.goal == 30

    def test_complete_habit(self, db, name='sleep'):
        habit = Habit("sleep").fetch_habit_data(db)
        assert habit.completed_total == 0
        habit.complete_habit(db)
        assert habit.completed_total == 1
        # habit.complete_habit(db)
        # habit.complete_habit(db)
        # habit.complete_habit(db)
        # assert habit.completed_total == 1

    def test_first_time_completion(self):
        pass

    def test_timedelta_calculation(self):
        pass

    def test_streak(self):
        pass

    def test_break_habit(self):
        pass

    def test_completion_cooldown(self):
        pass

    def test_check_off_habit(self):
        pass

    def test_check_longest_goal(self):
        pass

    def test_check_closest_goal(self):
        pass


class TestAnalysis:

    def test_list_all_habits(self, db):
        data = analysis.list_all_habits(db)
        assert data == [('brush teeth', 'daily', 0, 0, 0, 28), ('meditate', 'daily', 0, 0, 0, 60),
                        ('sleep', 'daily', 0, 0, 0, 30), ('clean bathroom', 'weekly', 0, 0, 0, 8),
                        ('call mom', 'monthly', 0, 0, 0, 4)]  # change 0 to actual values after completion
        assert len(data) == 5

    def test_list_filtered_habits(self, db):
        daily = analysis.list_filtered_habits(db, "daily")
        weekly = analysis.list_filtered_habits(db, "weekly")
        monthly = analysis.list_filtered_habits(db, "monthly")
        assert daily == [('brush teeth', 0, 0, 0, 28), ('meditate', 0, 0, 0, 60), ('sleep', 0, 0, 0, 30)]
        assert weekly == [('clean bathroom', 0, 0, 0, 8)]
        assert monthly == [('call mom', 0, 0, 0, 4)]
        assert len(daily) == 3
        assert len(weekly) == 1
        assert len(monthly) == 1

    def test_view_single_habit(self, db):
        data = analysis.view_single_habit(db, "brush teeth")
        assert data == [('brush teeth', 'Brush teeth every morning.', 'daily', 0, 0, 28, 0,
                         '2023-05-17 22:29:51.444614')]  # correct timestamp to whatever data pytest creates the habit!

    # def test_view_longest_streak(self):
    #     data = analysis.view_longest_streaks(db)
    #     assert  data == # assert returned tuple
    #
    # def test_view_closest_goal(self):
    #     data = analysis.view_closest_goal(db)
    #     assert data == # assert returned tuple


class TestDatabase:

    def test_habit_table(self, db):
        data = db.cur.execute("""SELECT * FROM habits""").fetchall()
        assert len(data) == 5

    def test_completion_table(self, db):
        data = db.cur.execute("""SELECT * FROM completions""").fetchall()
        assert len(data) == 0  # set assert value to the number of completions total (78?)

    def test_delete_habit(self, db, name='call mom'):
        all_habits = analysis.list_all_habits(db)  # assert tuple is already done in test_list_all_habits!
        assert len(all_habits) == 5
        db.drop_habit((name, ))
        remaining = analysis.list_all_habits(db)
        assert remaining == [('brush teeth', 'daily', 0, 0, 0, 28), ('meditate', 'daily', 0, 0, 0, 60),
                             ('sleep', 'daily', 0, 0, 0, 30), ('clean bathroom', 'weekly', 0, 0, 0, 8)]
        # change 0 to actual values after completion
        assert len(remaining) == 4
