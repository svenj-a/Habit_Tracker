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
    Habit(name='brush teeth', desc='Brush teeth every morning.', date="2023-04-10 08:06:02.066485", period='daily',
          goal=28).create_habit(db)
    Habit(name='sleep', desc='Sleep at least 7h per day.', date="2023-04-10 08:30:05.845662", period='daily',
          goal=30, ).create_habit(db)
    Habit(name='meditate', desc='Meditate at least 10 minutes every day after lunch.',
          date="2023-04-13 11:46:33.765130", period='daily', goal=60).create_habit(db)
    Habit(name='clean bathroom', desc='Clean the bathroom including toilet, shower, and sink.',
          date="2023-04-15 17:21:44.654321", period='weekly', goal=8).create_habit(db)
    Habit(name='call mom', desc='Call my mother once a month...', period='monthly', date="2023-04-17 22:05:24.756612",
          goal=4).create_habit(db)


@pytest.fixture(autouse=True)
def completion_loop(db):
    predefined_habits = {"sleep": ["2023-04-10 07:54:14", "2023-04-11 07:20:28", "2023-04-13 06:51:14",
                                   "2023-04-14 07:39:52", "2023-04-15 06:49:50", "2023-04-16 06:25:39",
                                   "2023-04-17 07:09:53", "2023-04-18 06:06:01", "2023-04-19 07:50:56",
                                   "2023-04-20 06:14:17", "2023-04-21 07:11:15", "2023-04-22 07:16:35",
                                   "2023-04-23 06:37:33", "2023-04-24 07:33:12", "2023-04-25 07:12:35",
                                   "2023-04-26 07:32:05", "2023-04-27 07:26:39", "2023-04-28 07:48:12",
                                   "2023-04-29 07:35:51", "2023-04-30 06:44:52", "2023-05-01 06:32:44",
                                   "2023-05-02 07:14:20", "2023-05-03 06:03:19", "2023-05-04 06:27:06",
                                   "2023-05-05 07:58:55", "2023-05-06 07:39:42", "2023-05-07 07:05:30",
                                   "2023-05-08 06:37:43", "2023-05-09 07:05:47", "2023-05-10 06:22:06"],
                         "brush teeth": ["2023-04-10 08:15:42", "2023-04-11	08:28:32", "2023-04-12 09:43:15",
                                         "2023-04-13 08:49:01", "2023-04-14	09:18:56", "2023-04-15 07:39:33",
                                         "2023-04-16 07:50:25", "2023-04-18	09:10:41", "2023-04-19 08:08:50",
                                         "2023-04-20 09:58:39", "2023-04-21	09:38:49", "2023-04-24 09:26:38",
                                         "2023-04-25 07:26:38", "2023-04-26	08:28:06", "2023-04-27 09:16:58",
                                         "2023-04-28 09:26:36", "2023-04-29	07:16:09", "2023-04-30 08:23:11",
                                         "2023-05-01 09:22:27", "2023-05-02 09:48:43", "2023-05-03 07:55:43",
                                         "2023-05-04 08:01:13", "2023-05-06	08:59:04", "2023-05-07 07:12:38",
                                         "2023-05-08 09:42:29", "2023-05-09	07:37:56"],
                         "meditate": ["2023-04-13 11:42:09", "2023-04-14 12:28:38", "2023-04-15 13:07:34",
                                      "2023-04-17 13:05:04", "2023-04-18 12:46:20", "2023-04-19 11:27:03",
                                      "2023-04-20 12:56:20", "2023-04-21 12:21:54", "2023-04-22 11:38:22",
                                      "2023-04-23 12:10:03", "2023-04-30 12:55:20", "2023-05-05 11:21:30",
                                      "2023-05-06 13:32:10", "2023-05-07 12:31:40", "2023-05-08 13:44:42",
                                      "2023-05-09 11:32:07", "2023-05-10 12:58:43"],
                         "clean bathroom": ["2023-04-16 15:49:41", "2023-04-22 17:10:29", "2023-04-28 15:08:26",
                                            "2023-05-07 15:35:54"],
                         "call mom": ["2023-04-19 19:26:45", "2023-05-09 19:29:09"]}
    for habit, dates in predefined_habits.items():
        habit = Habit(habit).fetch_habit_data(db)
        for date in dates:
            habit.complete_habit(db, date)
            print(habit.name, date, habit.completed_total)


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
