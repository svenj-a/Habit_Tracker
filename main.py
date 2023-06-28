import sqlite3
import pandas as pd
import questionary
from tabulate import tabulate

from db import DB
from habit import Habit
import analysis


def cli():
    """
    Main loop of the habit tracker program.
    """

    db = DB()

    stop = False
    while not stop:

        main_menu = questionary.select(
            "Welcome. What do you want to do?",
            choices=["Create habit", "Complete habit", "Analyze habits", "Delete habit", "Exit"]
        ).ask()

        if main_menu == "Create habit":

            name = questionary.text("What's the name of your new habit?").ask().lower()
            habit_created = False
            while not habit_created:
                if name == "":
                    print("\nPlease provide a name for your habit!\n")
                    name = questionary.text("What's the name of your new habit?").ask().lower()
                else:
                    habit_created = True

            desc = questionary.text("Please provide a short description of your habit.").ask()

            period = questionary.select(
                    "How often do you want to perform your habit?",
                    choices=["daily", "weekly", "monthly"]
                ).ask()

            goal = questionary.text(
                "Set a final goal: How often do you want to perform the habit? Please insert an integer number..."
            ).ask()
            habit_created = False
            while not habit_created:
                try:
                    if len(goal) > 5:
                        print("\nYou probably won't get that old ;). Please choose a reasonable goal.\n")
                        goal = questionary.text(
                            "Set a final goal: Insert an integer number between 2 and 99,999"
                        ).ask()
                    elif int(goal) < 2:
                        raise ValueError()
                    else:
                        Habit(name=name, desc=desc, period=period, goal=int(goal)).create_habit(db)
                        habit_created = True
                except (ValueError, TypeError):
                    print("\nYour goal must be an integer number larger than 1!\n")
                    goal = questionary.text(
                        "Set a final goal: How often do you want to perform the habit? Please insert a number..."
                    ).ask()
                except sqlite3.IntegrityError:
                    print(f"\nA habit with the name {name} already exists. Please choose a unique name:\n")
                    name = questionary.text("What's the name of your new habit?").ask().lower()

        elif main_menu == "Complete habit":
            habits = db.cur.execute("SELECT name FROM habits ORDER BY name").fetchall()
            habit_list = []
            for habit in habits:
                habit_list.append(*habit)  # the asterisk unpacks the tuple, so that habit_list truly is a list!
            habit_list.append("BACK TO MAIN MENU")
            selection = questionary.select(
                "Which habit do you want to check off today?",
                choices=habit_list
            ).ask()
            if selection == "BACK TO MAIN MENU":
                continue
            else:
                habit = Habit(selection).fetch_habit_data(db)
                habit.complete_habit(db)

        elif main_menu == "Analyze habits":
            selection = questionary.select(
                "What do you want to know about your habits?",
                choices=["View all habits", "View habits with periodicity ...", "View one habit ...",
                         "View personal records...", "View established habits", "BACK TO MAIN MENU"]
            ).ask()

            if selection == "BACK TO MAIN MENU":
                continue

            elif selection == "View all habits":
                habits = analysis.list_all_habits(db)
                format_print_outline(db, habits)

            elif selection == "View habits with periodicity ...":
                selection = questionary.select(
                    "Which filter do you want to apply?", choices=["daily", "weekly", "monthly", "BACK TO MAIN MENU"]
                ).ask()
                if selection == "BACK TO MAIN MENU":
                    continue
                else:
                    habits = analysis.list_filtered_habits(db, selection)
                    format_print_outline(db, habits)

            elif selection == "View one habit ...":
                habits = db.cur.execute("SELECT name FROM habits ORDER BY name").fetchall()
                habit_list = []
                for habit in habits:
                    habit_list.append(*habit)  # the asterisk unpacks the tuple, so that habit_list truly is a list!
                habit_list.append("BACK TO MAIN MENU")
                selection = questionary.select(
                    "Which habit do you want to display in detail?",
                    choices=habit_list
                ).ask()
                if selection == "BACK TO MAIN MENU":
                    continue
                else:
                    habit = analysis.view_single_habit(db, selection)  # turn argument back into type tuple --> (arg,)
                    print(habit)
                    format_print_grid(db, habit)

            elif selection == "View personal records...":
                selection = questionary.select(
                    "Please select what you want to display:",
                    choices=["View habits with the longest day streak!", "View habits with the closest goal!",
                             "BACK TO MAIN MENU"]
                ).ask()
                if selection == "BACK TO MAIN MENU":
                    continue
                elif selection == "View habits with the longest day streak!":
                    lon_str = analysis.view_longest_streaks(db)
                    print("\nYou have obtained the longest streak for these habits:\n")
                    format_print_grid(db, lon_str)
                elif selection == "View habits with the closest goal!":
                    cl_goal = analysis.view_closest_goal(db)
                    print("\nThese habits are closest to your final goal:\n")
                    format_print_grid(db, cl_goal)

            elif selection == "View established habits":
                habits = analysis.view_established_habits(db)
                print("\nThese habits are already established:\n")
                format_print_grid(db, habits)

        elif main_menu == "Delete habit":
            habits = db.cur.execute("SELECT name FROM habits ORDER BY name").fetchall()
            habit_list = []
            for habit in habits:
                habit_list.append(*habit)
            habit_list.append("BACK TO MAIN MENU")
            selection = questionary.select(
                "Which habit do you want to delete?",
                choices=habit_list
            ).ask()
            if selection == "BACK TO MAIN MENU":
                continue
            else:
                db.drop_habit((selection,))  # argument must be turned into type tuple --> (arg,)

        elif main_menu == "Exit":
            db.cur.close()
            db.db.close()
            stop = True


def format_print_grid(db, data):
    """
    Uses pandas DFs and tabulate to print data in a tidy format to CLI. Table format is "gird".
    :param db: name of the database connection
    :param data: an object that is returned by a method or function and needs to be printed to the console
    :return:
    """
    df = pd.DataFrame(data)
    headers = list(map(lambda x: x[0], db.cur.description))
    print(tabulate(df, headers=headers, tablefmt="grid"))


def format_print_outline(db, data):
    """
    Uses pandas DFs and tabulate to print data in a tidy format to CLI. Table format is "outline".
    :param db: name of the database connection
    :param data: an object that is returned by a method or function and needs to be printed to the console
    :return:
    """
    df = pd.DataFrame(data)
    headers = list(map(lambda x: x[0], db.cur.description))
    print(tabulate(df, headers=headers, tablefmt="outline"))


if __name__ == '__main__':
    cli()
