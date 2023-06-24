import pytest
import os
from datetime import datetime

from db import DB
from habit import Habit
import analysis


class TestHabitTracker:

    def setup_method(self):
        # self.db = DB("test.db")
        # self.db.cur.close()
        # self.db.db.close()
        # os.remove("test.db")
        self.db = DB("test.db")

        habit_brush_teeth = ['brush teeth', 'Brush teeth every morning.', 'daily',
                             '2023-04-10 08:06:02.066485', 26, 4, 11, 28]
        habit_sleep = ['sleep', 'Sleep at least 7h per day.', 'daily',
                       '2023-04-10 08:30:05.845662', 30, 28, 28, 28]
        habit_meditate = ['meditate', 'Meditate at least 10 minutes every day after lunch.', 'daily',
                          '2023-04-13 11:46:33.765130', 17, 6, 7, 28]
        habit_clean_bathroom = ['clean bathroom', 'Clean the bathroom including toilet, shower, and sink.', 'weekly',
                                '2023-04-15 17:21:44.654321', 4, 4, 4, 8]
        habit_call_mom = ['call mom', 'Call my mother once a month...', 'monthly',
                          '2023-04-17 22:05:24.756612', 2, 2, 2, 4]

        self.db.cur.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", habit_brush_teeth)
        self.db.cur.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", habit_sleep)
        self.db.cur.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", habit_meditate)
        self.db.cur.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", habit_clean_bathroom)
        self.db.cur.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", habit_call_mom)
        self.db.db.commit()

        # Habit(name='brush teeth', desc='Brush teeth every morning.', date="2023-04-10 08:06:02.066485", period='daily',
        #       goal=28).create_habit(db)
        # Habit(name='sleep', desc='Sleep at least 7h per day.', date="2023-04-10 08:30:05.845662", period='daily',
        #       goal=30, ).create_habit(db)
        # Habit(name='meditate', desc='Meditate at least 10 minutes every day after lunch.',
        #       date="2023-04-13 11:46:33.765130", period='daily', goal=60).create_habit(db)
        # Habit(name='clean bathroom', desc='Clean the bathroom including toilet, shower, and sink.',
        #       date="2023-04-15 17:21:44.654321", period='weekly', goal=8).create_habit(db)
        # Habit(name='call mom', desc='Call my mother once a month...', period='monthly', date="2023-04-17 22:05:24.756612",
        #       goal=4).create_habit(db)

        completion_data = {"brush teeth": ["2023-04-10 08:15:40.123456", "2023-04-11 08:28:32.123789",
                                           "2023-04-12 09:43:15.456789", "2023-04-13 08:49:01.798456",
                                           "2023-04-14 09:18:56.123654", "2023-04-15 07:39:33.321987",
                                           "2023-04-16 07:50:25.789456", "2023-04-18 09:10:41.987564",
                                           "2023-04-19 08:08:50.654321", "2023-04-20 09:58:39.321654",
                                           "2023-04-21 09:38:49.123456", "2023-04-24 09:26:38.456789",
                                           "2023-04-25 07:26:38.987654", "2023-04-26 08:28:06.987654",
                                           "2023-04-27 09:16:58.456123", "2023-04-28 09:26:36.258369",
                                           "2023-04-29 07:16:09.741852", "2023-04-30 08:23:11.852963",
                                           "2023-05-01 09:22:27.789456", "2023-05-02 09:48:43.369258",
                                           "2023-05-03 07:55:43.258147", "2023-05-04 08:01:13.147369",
                                           "2023-05-06 08:59:04.741852", "2023-05-07 07:12:38.852963",
                                           "2023-05-08 09:42:29.933711", "2023-05-09 07:37:56.741852"],
                           "sleep": ["2023-04-10 08:54:14.987654", "2023-04-11 07:20:28.774411",
                                     "2023-04-13 06:51:14.885522", "2023-04-14 07:39:52.885522",
                                     "2023-04-15 06:49:50.996633", "2023-04-16 06:25:39.774411",
                                     "2023-04-17 07:09:53.112233", "2023-04-18 06:06:01.445566",
                                     "2023-04-19 07:50:56.778899", "2023-04-20 06:14:17.991199",
                                     "2023-04-21 07:11:15.321654", "2023-04-22 07:16:35.654987",
                                     "2023-04-23 06:37:33.123456", "2023-04-24 07:33:12.456789",
                                     "2023-04-25 07:12:35.741852", "2023-04-26 07:32:05.852963",
                                     "2023-04-27 07:26:39.987654", "2023-04-28 07:48:12.753421",
                                     "2023-04-29 07:35:51.753869", "2023-04-30 06:44:52.357689",
                                     "2023-05-01 06:32:44.456456", "2023-05-02 07:14:20.357241",
                                     "2023-05-03 06:03:19.159263", "2023-05-04 06:27:06.159487",
                                     "2023-05-05 07:58:55.951627", "2023-05-06 07:39:42.951623",
                                     "2023-05-07 07:05:30.951628", "2023-05-08 06:37:43.753869",
                                     "2023-05-09 07:05:47.321654", "2023-05-10 06:22:06.987654"],
                           "meditate": ["2023-04-13 12:42:09.123123", "2023-04-14 12:28:38.987654",
                                        "2023-04-15 13:07:34.654321", "2023-04-17 13:05:04.999666",
                                        "2023-04-18 12:46:20.888555", "2023-04-19 11:27:03.777444",
                                        "2023-04-20 12:56:20.444111", "2023-04-21 12:21:54.555222",
                                        "2023-04-22 11:38:22.666333", "2023-04-23 12:10:03.999666",
                                        "2023-04-30 12:55:20.789456", "2023-05-05 11:21:30.456456",
                                        "2023-05-06 13:32:10.987654", "2023-05-07 12:31:40.654321",
                                        "2023-05-08 13:44:42.777888", "2023-05-09 11:32:07.888999",
                                        "2023-05-10 12:58:43.444555"],
                           "clean bathroom": ["2023-04-16 15:49:41.789789", "2023-04-22 17:10:29.654654",
                                              "2023-04-28 15:08:26.321321", "2023-05-07 15:35:54.123123"],
                           "call mom": ["2023-04-19 19:26:45.654654", "2023-05-09 19:29:09.789789"]}

        for habit, dates in completion_data.items():
            # habit = Habit(habit).fetch_habit_data(self.db)
            if isinstance(dates, list):
                for date in dates:
                    # habit.complete_habit(db=db, completed=datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f"))
                    self.db.cur.execute("""INSERT INTO completions VALUES (?,?)""", (habit, date))
        self.db.db.commit()

    def test_create_habit(self):
        habit = Habit(name="diary", desc="Write a diary entry every evening.", period="daily", goal=14
                      ).create_habit(self.db)
        # assert habit.name == "diary"
        # print(self.db.cur.execute("""SELECT * FROM habits WHERE name=?""", (habit.name,)).fetchall())
        assert self.db.cur.execute("""
            SELECT name, description, periodicity, completed_total, current_streak, longest_streak, final_goal
            FROM habits WHERE name=?
            """, (habit.name,)).fetchall() == [('diary', 'Write a diary entry every evening.', 'daily', 0, 0, 0, 14)]

    def test_fetch_habit_data(self):
        habit = Habit(name="sleep").fetch_habit_data(self.db)
        assert habit.goal == 28

    def test_complete_daily_habit_break_habit(self):
        habit = Habit("meditate").fetch_habit_data(self.db)
        print(habit.completed_total)
        habit.complete_habit(self.db)
        print(habit.completed_total)
        assert habit.completed_total == 18

    def test_complete_habit_completion_cooldown(self):
        habit = Habit("meditate").fetch_habit_data(self.db)
        habit.complete_habit(self.db)
        assert habit.completed_total == 18

    def test_complete_weekly_habit_break_habit(self):
        habit = Habit('clean bathroom').fetch_habit_data(self.db)
        print(habit.completed_total)
        habit.complete_habit(self.db)
        print(habit.completed_total)
        assert habit.completed_total == 5

    def test_complete_monthly_habit_break_habit(self):
        habit = Habit('call mom').fetch_habit_data(self.db)
        print(habit.completed_total)
        habit.complete_habit(self.db)
        print(habit.completed_total)
        assert habit.completed_total == 3

    def test_complete_habit_first_time_completion(self):
        new_habit = Habit(name="read", desc="Read a few pages every evening.", period="daily", goal=14
                          ).create_habit(self.db)
        print(new_habit.name)
        print(new_habit.completed_total)
        new_habit.complete_habit(self.db)
        print(new_habit.completed_total)
        assert (new_habit.completed_total, new_habit.current_streak, new_habit.longest_streak) == (1, 1, 1)

    def test_calculate_daily_timedelta(self):
        habit = Habit("sleep").fetch_habit_data(self.db)
        timedelta, timespan = habit._calculate_timedelta(completed=datetime.strptime("2023-05-11 06:22:06.987654",
                                                                                     "%Y-%m-%d %H:%M:%S.%f"),
                                                         last_completed=datetime.strptime("2023-05-10 06:22:06.987654",
                                                                                          "%Y-%m-%d %H:%M:%S.%f"))
        assert (timedelta, timespan) == (1, "day(s)")

    def teardown_method(self):
        self.db.cur.close()
        self.db.db.close()
        os.remove("test.db")


#
#     def test_streak(self):
#         pass
#
#     def test_break_habit(self):
#         pass
#
#     def test_completion_cooldown(self):
#         pass
#
#     def test_check_off_habit(self):
#         pass
#
#     def test_check_longest_goal(self):
#         pass
#
#     def test_check_closest_goal(self):
#         pass
#
#
#     def test_list_all_habits(self, db_mock_data):
#         data = analysis.list_all_habits(db_mock_data)
#         assert data == [('brush teeth', 'daily', 0, 0, 0, 28), ('meditate', 'daily', 0, 0, 0, 60),
#                         ('sleep', 'daily', 0, 0, 0, 30), ('clean bathroom', 'weekly', 0, 0, 0, 8),
#                         ('call mom', 'monthly', 0, 0, 0, 4)]  # change 0 to actual values after completion
#         assert len(data) == 5
#
#     def test_list_filtered_habits(self, db_mock_data):
#         daily = analysis.list_filtered_habits(db_mock_data, "daily")
#         weekly = analysis.list_filtered_habits(db_mock_data, "weekly")
#         monthly = analysis.list_filtered_habits(db_mock_data, "monthly")
#         assert daily == [('brush teeth', 0, 0, 0, 28), ('meditate', 0, 0, 0, 60), ('sleep', 0, 0, 0, 30)]
#         assert weekly == [('clean bathroom', 0, 0, 0, 8)]
#         assert monthly == [('call mom', 0, 0, 0, 4)]
#         assert len(daily) == 3
#         assert len(weekly) == 1
#         assert len(monthly) == 1
#
#     def test_view_single_habit(self, db_mock_data):
#         data = analysis.view_single_habit(db_mock_data, "brush teeth")
#         assert data == [('brush teeth', 'Brush teeth every morning.', 'daily', 0, 0, 28, 0,
#                          '2023-05-17 22:29:51.444614')]  # correct timestamp to input value from setup!
#
    # def test_view_longest_streak(self):
    #     data = analysis.view_longest_streaks(db)
    #     assert  data == # assert returned tuple
    #
    # def test_view_closest_goal(self):
    #     data = analysis.view_closest_goal(db)
    #     assert data == # assert returned tuple

#
# class TestDatabase:
#
#     def test_habit_table(self, db_mock_data):
#         data = db_mock_data.cur.execute("""SELECT * FROM habits""").fetchall()
#         assert len(data) == 5
#
#     def test_completion_table(self, db_mock_data):
#         data = db_mock_data.cur.execute("""SELECT * FROM completions""").fetchall()
#         assert len(data) == 0  # set assert value to the number of completions total (78?)
#
#     def test_delete_habit(self, db_mock_data):
#         all_habits = analysis.list_all_habits(db_mock_data)  # assert tuple is already done in test_list_all_habits!
#         assert len(all_habits) == 5
#         db_mock_data.drop_habit(('call mom',))
#         remaining = analysis.list_all_habits(db_mock_data)
#         assert remaining == [('brush teeth', 'daily', 0, 0, 0, 28), ('meditate', 'daily', 0, 0, 0, 60),
#                              ('sleep', 'daily', 0, 0, 0, 30), ('clean bathroom', 'weekly', 0, 0, 0, 8)]
#         # change 0 to actual values after completion
#         assert len(remaining) == 4

# unique contraint test assert raise error ....