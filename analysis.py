import pandas as pd
from tabulate import tabulate


def list_all_habits(db):
    """
    Prints a list of all habits that are currently stored in the database.
    :param db: name of the database
    :return:
    """
    all_habits = db.cur.execute("""
            SELECT name, periodicity, completed_total, current_streak, longest_streak, final_goal FROM habits
            """).fetchall()
    habit_df = pd.DataFrame(all_habits)
    headers = list(map(lambda x: x[0], db.cur.description))
    print(tabulate(habit_df, headers=headers))


def list_filtered_habits(db, periodicity):
    """
    Prints a list of all habits with the selected periodicity that are currently stored in the database.
    :param db: name of the database
    :param periodicity: periodicity for which the listed habits are filtered; selected by user
    :return:
    """
    filtered_habits = db.cur.execute("""
            SELECT name, completed_total, current_streak, longest_streak, final_goal FROM habits WHERE periodicity=?
            """, (periodicity, )).fetchall()
    habit_df = pd.DataFrame(filtered_habits)
    headers = list(map(lambda x: x[0], db.cur.description))
    print(tabulate(habit_df, headers=headers))


def view_single_habit(db, habit):
    """
    Displays the database entry for any single habit.
    :param db: an initialized sqlite3 database connection
    :param habit: name of the habit that is to be displayed
    :return: database entry for the respective habit
    """
    data = db.cur.execute("""SELECT * FROM habits WHERE name=?""", (habit, )).fetchall()
    df = pd.DataFrame(data)
    headers = list(map(lambda x: x[0], db.cur.description))
    print(tabulate(df, headers=headers))


def view_closest_goal(db):
    """
    Prints the habit where the longest streak is closest to the final goal.
    :param db: name of the database
    :return:
    """
    print("\nThis habit is closest to your final goal:\n")
    goals = db.cur.execute("""
            SELECT name, final_goal, longest_streak, MIN(final_goal - longest_streak) AS difference FROM habits
            """).fetchall()
    df = pd.DataFrame(goals)
    headers = list(map(lambda x: x[0], db.cur.description))
    print(tabulate(df, headers=headers))


def view_longest_streaks(db):
    """
    Prints the habit with the longest day streak.
    :param db: name of the database
    :return:
    """
    print("\nYou have obtained the longest streak for this habit:\n")
    streak = db.cur.execute("""SELECT name, MAX(longest_streak) AS longest_streak FROM habits""").fetchall()
    df = pd.DataFrame(streak)
    headers = list(map(lambda x: x[0], db.cur.description))
    print(tabulate(df, headers=headers))
