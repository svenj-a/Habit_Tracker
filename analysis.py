def list_all_habits(db):
    """
    Fetches the data from the database and returns a list of all habits that are currently stored.
    :param db: name of the database connection
    :return: a list of habits
    """
    habits = db.cur.execute("""
        SELECT name, periodicity, completed_total, current_streak, longest_streak, final_goal, established
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
    Fetches the data from the database and returns a list of all habits with the selected periodicity that are currently
    stored.
    :param db: name of the database connection
    :param periodicity: periodicity for which the listed habits are filtered; selected by user
    :return: a list of habits
    """
    habits = db.cur.execute("""
        SELECT name, completed_total, current_streak, longest_streak, final_goal, established
        FROM habits
        WHERE periodicity=?
        ORDER BY name
        """, (periodicity, )).fetchall()
    return habits


def view_single_habit(db, habit_name):
    """
    Fetches the data for a selected habit from the database and returns the currently stored values.
    :param db: the name of a database connection
    :param habit_name: name of the habit that is to be displayed
    :return: data for the selected habit
    """
    habit_data = db.cur.execute("""
        SELECT name, description, periodicity, completed_total, current_streak, longest_streak, final_goal, established,
            creation_date
        FROM habits
        WHERE name=?
        """, (habit_name, )).fetchall()
    return habit_data


def view_longest_streaks(db):
    """
    Fetches the data for all habits with the longest day streak stratified by periodicity from the database and
    returns the currently stored values.
    :param db: name of the database connection
    :return: a list of all habits with max value for longest_streak
    """
    periods = ["daily", "weekly", "monthly"]
    habits = []
    for period in periods:
        streaks = db.cur.execute("""
                SELECT ALL name, periodicity, longest_streak, established
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
    Fetches the data for all habits where the current day streak is closest to the final goal stratified by periodicity
    from the database and returns the currently stored values.
    :param db: name of the database connection
    :return: a list of all habits with the smallest difference of final_goal and current_streak
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
    :return:a list of habits
    """
    periods = ["daily", "weekly", "monthly"]
    habits = []
    for period in periods:
        established = db.cur.execute("""
                        SELECT ALL name, periodicity, completed_total, current_streak, longest_streak, final_goal
                        FROM habits
                        WHERE periodicity = ?
                        AND established = ?
                        ORDER BY periodicity, name
                        """, (period, True)).fetchall()
        for habit in established:
            habits.append(habit)
    return habits
