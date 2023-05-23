import pandas as pd
from tabulate import tabulate


def list_all_habits(db):
    """
    Prints a list of all habits that are currently stored in the database.
    :param db: name of the database
    :return:
    """
    all_habits = db.cur.execute("""
        SELECT name, periodicity, completed_total, current_streak, longest_streak, final_goal
        FROM habits
        ORDER BY CASE
            WHEN periodicity = 'daily' THEN 1
            WHEN periodicity = 'weekly' THEN 2
            WHEN periodicity = 'monthly' THEN 3
            END,
        name
        """).fetchall()
    habit_df = pd.DataFrame(all_habits)
    headers = list(map(lambda x: x[0], db.cur.description))
    print(tabulate(habit_df, headers=headers, tablefmt="outline"))


def list_filtered_habits(db, periodicity):
    """
    Prints a list of all habits with the selected periodicity that are currently stored in the database.
    :param db: name of the database
    :param periodicity: periodicity for which the listed habits are filtered; selected by user
    :return:
    """
    filtered_habits = db.cur.execute("""
        SELECT name, completed_total, current_streak, longest_streak, final_goal
        FROM habits
        WHERE periodicity=?
        ORDER BY name
        """, (periodicity, )).fetchall()
    habit_df = pd.DataFrame(filtered_habits)
    headers = list(map(lambda x: x[0], db.cur.description))
    print(tabulate(habit_df, headers=headers, tablefmt="outline"))


def view_single_habit(db, habit):
    """
    Displays the database entry for any single habit.
    :param db: an initialized sqlite3 database connection
    :param habit: name of the habit that is to be displayed
    :return: database entry for the respective habit
    """
    data = db.cur.execute("""
        SELECT name, description, periodicity, current_streak, longest_streak, final_goal, completed_total,
            creation_date
        FROM habits
        WHERE name=?
        """, (habit, )).fetchall()
    df = pd.DataFrame(data)
    headers = list(map(lambda x: x[0], db.cur.description))
    print(tabulate(df, headers=headers, tablefmt="outline"))


def view_longest_streaks(db):
    """
    Prints all habits with the longest day streaks stratified by periodicity.
    :param db: name of the database
    :return:
    """
    periods = ["daily", "weekly", "monthly"]
    habits = []
    for period in periods:
        streaks = db.cur.execute("""
                SELECT ALL name, periodicity, longest_streak
                FROM habits
                WHERE periodicity = ?
                AND longest_streak = (SELECT MAX(longest_streak) FROM habits WHERE periodicity = ?)
                ORDER BY name
                """, (period, period)).fetchall()
        for streak in streaks:
            habits.append(streak)
    df = pd.DataFrame(habits)
    headers = list(map(lambda x: x[0], db.cur.description))
    print("\nYou have obtained the longest streak for these habits:\n")
    print(tabulate(df, headers=headers, tablefmt="grid"))


def view_closest_goal(db):
    """
    Prints the habits where the longest day streak is closest to the final goal stratified by periodicity.
    :param db: name of the database
    :return:
    """
    periods = ["daily", "weekly", "monthly"]
    habits = []
    for period in periods:
        streaks = db.cur.execute("""
                    SELECT ALL name, periodicity, current_streak, (final_goal-current_streak) AS difference, final_goal
                    FROM habits
                    WHERE periodicity = ?
                    AND difference = (SELECT MIN(final_goal-current_streak) FROM habits WHERE periodicity = ?)
                    ORDER BY name
                    """, (period, period)).fetchall()
        for streak in streaks:
            habits.append(streak)
    df = pd.DataFrame(habits)
    headers = list(map(lambda x: x[0], db.cur.description))
    print("\nThese habits are closest to your final goal:\n")
    print(tabulate(df, headers=headers, tablefmt="grid"))
