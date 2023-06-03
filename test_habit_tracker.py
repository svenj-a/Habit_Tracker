import pytest

from db import DB
from habit import Habit
import analysis


@pytest.fixture(autouse=True)
def db():
    db = DB(":memory:")
    return db


@pytest.fixture(autouse=True)
def create_habits(db):
    Habit('sleep', 'Sleep at least 7h per day.', 'daily', 30).create_habit(db)
    Habit('brush teeth', 'Brush teeth every morning.', 'daily', 28).create_habit(db)
    Habit('clean bathroom', 'Clean the bathroom including toilet, shower, and sink.', 'weekly', 8
          ).create_habit(db)
    Habit('call mom', 'Call my mother once a month...', 'monthly', 4).create_habit(db)
    Habit('meditate', 'Meditate at least 10 minutes every day after lunch.', 'daily', 60).create_habit(db)


@pytest.fixture(autouse=True)
def add_completion_data(db):
    pass
    # add completion events with complete habit method and non-default timestamp arguments


class TestHabitDB:

    def test_create_habit_fixture(self, db):    # necessary?
        data = analysis.list_all_habits(db)
        print(data)
        assert data == [('brush teeth', 'daily', 0, 0, 0, 28), ('meditate', 'daily', 0, 0, 0, 60),
                        ('sleep', 'daily', 0, 0, 0, 30), ('clean bathroom', 'weekly', 0, 0, 0, 8),
                        ('call mom', 'monthly', 0, 0, 0, 4)]    # change 0 to actual values after completion
        assert len(data) == 5

    def test_complete_habit_fixture(self, db, name='sleep'):  # necessary? see above
        data = db.cur.execute("""SELECT * FROM completions""").fetchall()
        assert len(data) == 0
        # set assert value to the number of completions

    def test_day_streak(self):
        pass

    def test_reset_streak(self):
        pass

    def test_check_records(self):
        pass

    def test_delete_habit(self, db, name='call mom'):
        db.drop_habit((name, ))
        data = analysis.list_all_habits(db)
        assert data == [('brush teeth', 'daily', 0, 0, 0, 28), ('meditate', 'daily', 0, 0, 0, 60),
                        ('sleep', 'daily', 0, 0, 0, 30), ('clean bathroom', 'weekly', 0, 0, 0, 8)]  # change 0 to actual values after completion
        assert len(data) == 4  # is it sufficient to check for length or must db entry be checked?


class TestAnalysis:

    def test_list_all_habits(self, db):
        data = analysis.list_all_habits(db)
        assert len(data) == 5  # is it sufficient to check for length or must db entry be checked? Same as test_create

    def test_filtered_habits(self):
        pass

    def test_view_single_habit(self):
        pass    # assert returned tuple

    def test_view_longest_streak(self):
        pass    # assert returned tuple

    def test_view_closest_goal(self):
        pass
