import questionary
import sqlite3
import pandas as pd
from tabulate import tabulate

from habit import Habit
import analysis
from db import DB


def cli():
    db = DB()

    # delete the following block after development is completed or put in try except to create dummy data:
    # habit1 = Habit('sleep', 'Sleep at least 7h per day.', 'daily', 30)
    # habit1.create_habit(db)
    # habit2 = Habit('brush teeth', 'Brush teeth every morning.', 'daily', 28)
    # habit2.create_habit(db)
    # habit3 = Habit('clean bathroom', 'Clean the bathroom every week including toilet, shower, and sink.', 'weekly', 8)
    # habit3.create_habit(db)
    # habit4 = Habit('call mom', 'Call my mother once a month...', 'monthly', 4)
    # habit4.create_habit(db)
    # habit5 = Habit('meditate', 'Meditate at least 10 minutes every day after lunch.', 'daily', 60)
    # habit5.create_habit(db)

    stop = False

    while not stop:

        main_menu = questionary.select(
            "Welcome. What do you want to do?",
            choices=["Create habit", "Complete habit", "Analyze habits", "Delete habit", "Exit"]
        ).ask()

        if main_menu == "Create habit":
            name = questionary.text("What's the name of your new habit?").ask()
            desc = questionary.text("Please provide a short description of your habit.").ask()
            period = questionary.select(
                "How often do you want to perform your habit?",
                choices=["daily", "weekly", "monthly"]
            ).ask()
            goal = questionary.text(
                "Set a final goal: How often do you want to perform the habit? Please insert a number..."
            ).ask()
            habit_created = False
            while not habit_created:
                try:
                    habit = Habit(name, desc, period, int(goal))
                    habit.create_habit(db)
                    habit_created = True
                except (ValueError, TypeError):
                    print("Please enter an integer number!")
                    goal = questionary.text("Set a final goal: ").ask()
                except sqlite3.IntegrityError:
                    print(f"A habit with the name {name} already exists. Please choose a different name:")
                    name = questionary.text("What's the name of your new habit?").ask()

        elif main_menu == "Complete habit":
            db.cur.execute("SELECT name FROM habits ORDER BY name")
            habits = db.cur.fetchall()
            habit_list = []
            for habit in habits:
                habit_list.append(*habit)  # the asterisk unpacks the tuple, so that habit_list truly is a list!
            try:
                habit_name = questionary.select(
                    "Which habit do you want to check off today?",
                    choices=habit_list
                ).ask()
                habit = Habit(habit_name)
                habit.complete_habit(db, habit_name)
            except ValueError:
                print("There are no habits available! Please select a different option."
                      "You could start by creating a habit!")

        elif main_menu == "Analyze habits":
            analysis_menu = questionary.select(
                "What do you want to know about your habits?",
                choices=["View all habits", "View habits with periodicity ...", "View one habit ...",
                         "View personal records", "View established habits"]
            ).ask()

            if analysis_menu == "View all habits":
                habits = analysis.list_all_habits(db)
                format_print(db, habits)

            elif analysis_menu == "View habits with periodicity ...":
                period = questionary.select(
                    "Which filter do you want to apply?", choices=["daily", "weekly", "monthly"]
                ).ask()
                habits = analysis.list_filtered_habits(db, period)
                format_print(db, habits)

            elif analysis_menu == "View one habit ...":
                habits = db.cur.execute("SELECT name FROM habits ORDER BY name").fetchall()
                habit_list = []
                for habit in habits:
                    habit_list.append(*habit)  # the asterisk unpacks the tuple, so that habit_list truly is a list!
                try:
                    habit_name = questionary.select(
                        "Which habit do you want to display in detail?",
                        choices=habit_list
                    ).ask()
                    habit = analysis.view_single_habit(db, habit_name)  # turn argument into type tuple --> (arg,)
                    format_print(db, habit)
                except ValueError:
                    print("There are no habits available! Please select a different option."
                          "You could for example create a habit!")

            elif analysis_menu == "View personal records":
                record = questionary.select(
                    "Please select what you want to display:",
                    choices=["View habit with the longest day streak!", "View habit with the closest goal!"]  # "both"
                ).ask()
                if record == "View habit with the longest day streak!":
                    lon_str = analysis.view_longest_streaks(db)
                    print("\nYou have obtained the longest streak for these habits:\n")
                    format_print(db, lon_str)
                elif record == "View habit with the closest goal!":
                    cl_goal = analysis.view_closest_goal(db)
                    print("\nThese habits are closest to your final goal:\n")
                    format_print(db, cl_goal)
                # elif record == "both":
                #     analysis.view_longest_streaks(db)
                #     analysis.view_closest_goal(db)

            elif analysis_menu == "View established habits":
                habits = analysis.view_established_habits(db)
                print("\nThese habits are already established:\n")
                format_print(db, habits)

        elif main_menu == "Delete habit":
            db.cur.execute("SELECT name FROM habits ORDER BY name")
            habits = db.cur.fetchall()
            habit_list = []
            for habit in habits:
                habit_list.append(*habit)   # the asterisk unpacks the tuple, so that habit_list truly is a list!
            try:
                habit_name = questionary.select(
                    "Which habit do you want to delete?",
                    choices=habit_list
                ).ask()
                db.drop_habit((habit_name, ))   # argument must be turned into type tuple --> (arg,)
            except ValueError:
                print("There are no habits available! Please select a different option."
                      "You could for example create a habit!")  # put more stuff in db.py drop_habit!

        elif main_menu == "Exit":
            db.cur.close()
            stop = True


def format_print(db, value):
    """
    Format print statements with tabulate to return to cli
    :param db: name of the database connection
    :param value: an object that is returned by a method or function and needs to be printed to the console
    :return:
    """
    df = pd.DataFrame(value)
    headers = list(map(lambda x: x[0], db.cur.description))
    print(tabulate(df, headers=headers, tablefmt="grid"))


if __name__ == '__main__':
    cli()
