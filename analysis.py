from db import DB


def list_all_habits(db):
    pass


def view_habit(db, habit):
    """
    Displays the database entry for any single habit.
    :param db: an initialized sqlite3 database connection
    :param habit: name of the habit that is to be displayed
    :return: database entry for the respective habit
    """

    data = DB.get_habit_data(db, habit)
    return data


def view_closest_goal(db):
    pass


def view_longest_streaks(db):
    pass
