import os
from datetime import datetime

from db import DB
from habit import Habit
import analysis


class TestHabitTracker:

    def setup_method(self):
        self.db = DB("test.db")

        habit_brush_teeth = ['brush teeth', 'Brush teeth every morning.', 'daily',
                             '2023-04-10 08:06:02.066485', 26, 4, 11, 28, False]
        habit_sleep = ['sleep', 'Sleep at least 7h per day.', 'daily',
                       '2023-04-10 08:30:05.845662', 29, 27, 27, 28, False]
        habit_meditate = ['meditate', 'Meditate at least 10 minutes every day after lunch.', 'daily',
                          '2023-04-13 11:46:33.765130', 17, 6, 7, 28, False]
        habit_clean_bathroom = ['clean bathroom', 'Clean the bathroom including toilet, shower, and sink.', 'weekly',
                                '2023-04-15 17:21:44.654321', 4, 4, 4, 8, False]
        habit_call_mom = ['call mom', 'Call my mother once a month...', 'monthly',
                          '2023-04-17 22:05:24.756612', 2, 2, 2, 4, False]

        self.db.cur.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", habit_brush_teeth)
        self.db.cur.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", habit_sleep)
        self.db.cur.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", habit_meditate)
        self.db.cur.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", habit_clean_bathroom)
        self.db.cur.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", habit_call_mom)
        self.db.db.commit()

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
                                     "2023-04-14 07:39:52.885522", "2023-04-15 06:49:50.996633",
                                     "2023-04-16 06:25:39.774411", "2023-04-17 07:09:53.112233",
                                     "2023-04-18 06:06:01.445566", "2023-04-19 07:50:56.778899",
                                     "2023-04-20 06:14:17.991199", "2023-04-21 07:11:15.321654",
                                     "2023-04-22 07:16:35.654987", "2023-04-23 06:37:33.123456",
                                     "2023-04-24 07:33:12.456789", "2023-04-25 07:12:35.741852",
                                     "2023-04-26 07:32:05.852963", "2023-04-27 07:26:39.987654",
                                     "2023-04-28 07:48:12.753421", "2023-04-29 07:35:51.753869",
                                     "2023-04-30 06:44:52.357689", "2023-05-01 06:32:44.456456",
                                     "2023-05-02 07:14:20.357241", "2023-05-03 06:03:19.159263",
                                     "2023-05-04 06:27:06.159487", "2023-05-05 07:58:55.951627",
                                     "2023-05-06 07:39:42.951623", "2023-05-07 07:05:30.951628",
                                     "2023-05-08 06:37:43.753869", "2023-05-09 07:05:47.321654",
                                     "2023-05-10 06:22:06.987654"],
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
            if isinstance(dates, list):
                for date in dates:
                    self.db.cur.execute("""INSERT INTO completions VALUES (?,?)""", (habit, date))
        self.db.db.commit()

    def test_create_habit(self):
        habit = Habit(name="diary", desc="Write a diary entry every evening.", period="daily", goal=14,
                      ).create_habit(self.db)
        diary = self.db.cur.execute("""
            SELECT name, description, periodicity, completed_total, current_streak, longest_streak, final_goal,
                established
            FROM habits WHERE name=?
            """, (habit.name,)).fetchall()
        assert diary == [('diary', 'Write a diary entry every evening.', 'daily', 0, 0, 0, 14, False)]

    def test_fetch_habit_data(self):
        habit = Habit(name="sleep").fetch_habit_data(self.db)
        assert (habit.name, habit.desc, habit.period, habit.date, habit.completed_total, habit.current_streak,
                habit.longest_streak, habit.goal, habit.goal_reached) == ('sleep', 'Sleep at least 7h per day.',
                                                                          'daily', '2023-04-10 08:30:05.845662',
                                                                          29, 27, 27, 28, False)

    def test_complete_daily_habit_break_habit(self):
        habit = Habit("brush teeth").fetch_habit_data(self.db)
        habit.complete_habit(db=self.db, completed=datetime(2023, 5, 11, 10, 43, 58, 654978))
        assert (habit.completed_total, habit.current_streak, habit.longest_streak) == (27, 1, 11)

    def test_complete_daily_habit_completion_cooldown(self):
        habit = Habit("meditate").fetch_habit_data(self.db)
        habit.complete_habit(db=self.db, completed=datetime(2023, 5, 10, 15, 43, 58, 654978))
        assert (habit.completed_total, habit.current_streak, habit.longest_streak) == (17, 6, 7)

    def test_complete_daily_habit_check_off_habit(self):
        habit = Habit("meditate").fetch_habit_data(self.db)
        habit.complete_habit(db=self.db, completed=datetime(2023, 5, 11, 10, 43, 58, 654978))
        assert (habit.completed_total, habit.current_streak, habit.longest_streak) == (18, 7, 7)

    def test_complete_weekly_habit_break_habit(self):
        habit = Habit('clean bathroom').fetch_habit_data(self.db)
        habit.complete_habit(db=self.db, completed=datetime(2023, 5, 15, 10, 43, 58, 654978))
        assert (habit.completed_total, habit.current_streak, habit.longest_streak) == (5, 1, 4)

    def test_complete_weekly_habit_completion_cooldown(self):
        habit = Habit('clean bathroom').fetch_habit_data(self.db)
        habit.complete_habit(db=self.db, completed=datetime(2023, 5, 7, 20, 43, 58, 654978))
        assert (habit.completed_total, habit.current_streak, habit.longest_streak) == (4, 4, 4)

    def test_complete_weekly_habit_check_off_habit(self):
        habit = Habit('clean bathroom').fetch_habit_data(self.db)
        habit.complete_habit(db=self.db, completed=datetime(2023, 5, 8, 20, 43, 58, 654978))
        assert (habit.completed_total, habit.current_streak, habit.longest_streak) == (5, 5, 5)

    def test_complete_monthly_habit_break_habit(self):
        habit = Habit('call mom').fetch_habit_data(self.db)
        habit.complete_habit(db=self.db, completed=datetime(2023, 7, 2, 21, 43, 58, 654978))
        assert (habit.completed_total, habit.current_streak, habit.longest_streak) == (3, 1, 2)

    def test_complete_monthly_habit_completion_cooldown(self):
        habit = Habit('call mom').fetch_habit_data(self.db)
        habit.complete_habit(db=self.db, completed=datetime(2023, 5, 31, 20, 43, 58, 654978))
        assert (habit.completed_total, habit.current_streak, habit.longest_streak) == (2, 2, 2)

    def test_complete_monthly_habit_check_off_habit(self):
        habit = Habit('call mom').fetch_habit_data(self.db)
        habit.complete_habit(db=self.db, completed=datetime(2023, 6, 25, 14, 43, 58, 654978))
        assert (habit.completed_total, habit.current_streak, habit.longest_streak) == (3, 3, 3)

    def test_complete_daily_habit_check_off_habit_with_final_goal_reached(self):
        habit = Habit("sleep").fetch_habit_data(self.db)
        habit.complete_habit(db=self.db, completed=datetime(2023, 5, 11, 8, 43, 58, 654978))
        assert (habit.completed_total, habit.current_streak, habit.longest_streak, habit.goal_reached) == (30, 28, 28,
                                                                                                           True)
        assert self.db.cur.execute("""
            SELECT name, completed_total, current_streak, longest_streak, final_goal, established
            FROM habits WHERE name=?
            """, (habit.name,)).fetchall() == [("sleep", 30, 28, 28, 28, 1)]

    def test_complete_habit_first_time_completion(self):
        new_habit = Habit(name="read", desc="Read a few pages every evening.", period="daily", goal=14
                          ).create_habit(self.db)
        new_habit.complete_habit(self.db)
        assert (new_habit.completed_total, new_habit.current_streak, new_habit.longest_streak) == (1, 1, 1)

    def test_calculate_daily_timedelta(self):
        habit = Habit("sleep").fetch_habit_data(self.db)
        timedelta, timespan = habit._calculate_timedelta(completed=datetime.strptime("2023-05-11 06:22:06.987654",
                                                                                     "%Y-%m-%d %H:%M:%S.%f"),
                                                         last_completed=datetime.strptime("2023-05-10 06:22:06.987654",
                                                                                          "%Y-%m-%d %H:%M:%S.%f"))
        assert (timedelta, timespan) == (1, "day(s)")

    def test_list_all_habits(self):
        data = analysis.list_all_habits(self.db)
        assert (len(data), data) == (5, [('brush teeth', 'daily', 26, 4, 11, 28, False),
                                         ('meditate', 'daily', 17, 6, 7, 28, False),
                                         ('sleep', 'daily', 29, 27, 27, 28, False),
                                         ('clean bathroom', 'weekly', 4, 4, 4, 8, False),
                                         ('call mom', 'monthly', 2, 2, 2, 4, False)])

    def test_list_filtered_habits_daily(self):
        daily = analysis.list_filtered_habits(self.db, "daily")
        assert (len(daily), daily) == (3, [('brush teeth', 26, 4, 11, 28, False), ('meditate', 17, 6, 7, 28, False),
                                           ('sleep', 29, 27, 27, 28, False)])

    def test_list_filtered_habits_weekly(self):
        weekly = analysis.list_filtered_habits(self.db, "weekly")
        assert (len(weekly), weekly) == (1, [('clean bathroom', 4, 4, 4, 8, False)])

    def test_list_filtered_habits_monthly(self):
        monthly = analysis.list_filtered_habits(self.db, "monthly")
        assert (len(monthly), monthly) == (1, [('call mom', 2, 2, 2, 4, False)])

    def test_view_single_habit(self):
        data = analysis.view_single_habit(self.db, "brush teeth")
        assert data == [('brush teeth', 'Brush teeth every morning.', 'daily', 26, 4, 11, 28, False,
                         '2023-04-10 08:06:02.066485')]

    def test_view_longest_streak(self):
        data = analysis.view_longest_streaks(self.db)
        assert data == [('sleep', 'daily', 27, False), ('clean bathroom', 'weekly', 4, False),
                        ('call mom', 'monthly', 2, False)]

    def test_view_closest_goal(self):
        data = analysis.view_closest_goal(self.db)
        assert data == [('sleep', 'daily', 27, 1, 28), ('clean bathroom', 'weekly', 4, 4, 8),
                        ('call mom', 'monthly', 2, 2, 4)]

    def test_view_established_habits(self):
        habit = Habit('sleep').fetch_habit_data(self.db)
        habit.complete_habit(db=self.db, completed=datetime(2023, 5, 11, 8, 43, 58, 654978))
        established = analysis.view_established_habits(self.db)
        assert (len(established), established) == (1, [("sleep", "daily", 30, 28, 28, 28)])

    def test_habit_table(self):
        data = self.db.cur.execute("""SELECT * FROM habits""").fetchall()
        assert len(data) == 5

    def test_completion_table(self):
        data = self.db.cur.execute("""SELECT * FROM completions""").fetchall()
        assert len(data) == 78

    def test_delete_habit(self):
        self.db.drop_habit(('meditate',))
        remaining = analysis.list_all_habits(self.db)
        assert (len(remaining), remaining) == (4, [('brush teeth', 'daily', 26, 4, 11, 28, False),
                                                   ('sleep', 'daily', 29, 27, 27, 28, False),
                                                   ('clean bathroom', 'weekly', 4, 4, 4, 8, False),
                                                   ('call mom', 'monthly', 2, 2, 2, 4, False)])

    def teardown_method(self):
        self.db.cur.close()
        self.db.db.close()
        os.remove("test.db")

# unique constraint test assert raise error ....
# make sure to run tests simultaneously -> put correct command in instructions!
