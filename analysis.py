def list_all_habits(db):
    db.cur.execute("SELECT * FROM habits")
    all_habits = db.cur.fetchall()
    for habit in all_habits:
        print(habit)


def list_filtered_habits(db, periodicity):
    db.cur.execute("SELECT * FROM habits WHERE periodicity=?", periodicity)
    all_habits = db.cur.fetchall()
    for habit in all_habits:
        print(habit)


def view_single_habit(db, habit):
    """
    Displays the database entry for any single habit.
    :param db: an initialized sqlite3 database connection
    :param habit: name of the habit that is to be displayed
    :return: database entry for the respective habit
    """

    data = db.get_habit_data(habit)
    return data


def view_closest_goal(db):
    pass


def view_longest_streaks(db):
    pass
