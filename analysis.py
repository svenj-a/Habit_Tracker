
def list_all_habits(db):
    """
    Prints a list of all habits that are currently stored in the database.
    :param db: name of the database
    :return:
    """
    habits = db.cur.execute("""
        SELECT name, periodicity, completed_total, current_streak, longest_streak, final_goal
        FROM habits
        ORDER BY CASE
            WHEN periodicity = 'daily' THEN 1
            WHEN periodicity = 'weekly' THEN 2
            WHEN periodicity = 'monthly' THEN 3
            END,
        name
        """).fetchall()
    return habits


def list_filtered_habits(db, periodicity):
    """
    Prints a list of all habits with the selected periodicity that are currently stored in the database.
    :param db: name of the database
    :param periodicity: periodicity for which the listed habits are filtered; selected by user
    :return:
    """
    habits = db.cur.execute("""
        SELECT name, completed_total, current_streak, longest_streak, final_goal
        FROM habits
        WHERE periodicity=?
        ORDER BY name
        """, (periodicity, )).fetchall()
    return habits


def view_single_habit(db, habit):
    """
    Displays the database entry for any single habit.
    :param db: an initialized sqlite3 database connection
    :param habit: name of the habit that is to be displayed
    :return: database entry for the respective habit
    """
    habit = db.cur.execute("""
        SELECT name, description, periodicity, current_streak, longest_streak, final_goal, completed_total,
            creation_date
        FROM habits
        WHERE name=?
        """, (habit, )).fetchall()
    return habit


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
    return habits


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
                    WHERE longest_streak < final_goal
                    AND periodicity = ?
                    AND difference = (SELECT MIN(final_goal-current_streak) FROM habits WHERE periodicity = ?)
                    ORDER BY name
                    """, (period, period)).fetchall()
        for streak in streaks:
            habits.append(streak)
    return habits


def view_established_habits(db):
    """
    Return all habits that are already established, i.e. where the final goal has been reached in one streak.
    :param db: name of the database
    :return:
    """
    periods = ["daily", "weekly", "monthly"]
    habits = []
    for period in periods:
        established = db.cur.execute("""
                        SELECT ALL name, periodicity, current_streak, longest_streak, final_goal
                        FROM habits
                        WHERE periodicity = ?
                        AND longest_streak >= final_goal
                        ORDER BY periodicity, name
                        """, (period, )).fetchall()
        for habit in established:
            habits.append(habit)
    return habits
