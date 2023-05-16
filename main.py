import questionary
import sqlite3

import analysis
from db import DB
from habit import Habit


def cli():
    db = DB()
    DB.get_db(db)

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
            habit_created = False
            while not habit_created:
                try:
                    goal = questionary.text(
                        "Set a final goal: How often do you want to perform the habit? Please insert a number..."
                    ).ask()
                    habit = Habit(name, desc, period, int(goal))
                    habit.create_habit(db)
                    habit_created = True
                except (ValueError, TypeError):
                    print("Please enter an integer number!")
                except sqlite3.IntegrityError:
                    print(f"A habit with the name {name} already exists. Please choose a different name:")
                    name = questionary.text("What's the name of your new habit?").ask()

        elif main_menu == "Complete habit":
            pass

        elif main_menu == "Analyze habits":
            analysis_menu = questionary.select(
                "\nWhat do you want to know about your habits?",
                choices=["View all habits", "View one habit ...", "View habits with periodicity ...",
                         "View personal record"]
            ).ask()

            if analysis_menu == "View all habits":
                analysis.list_all_habits(db)

            elif analysis_menu == "View habits with periodicity ...":
                pass
                # selected_periodicity =
                # analysis.list_filtered_habits(db, selected_periodicity)

            elif analysis_menu == "View one habit ...":
                pass
                # selected_habit =    # same problem like in delete habit!!! how to turn tuple in list??
                # analysis.view_single_habit(db, selected_habit)

        elif main_menu == "Delete habit":
            db.cur.execute("SELECT name FROM habits ORDER BY name")
            habits = db.cur.fetchall()
            habit_list = []
            for habit in habits:
                habit_list.append(*habit)   # the asterisk unpacks the tuple, so that habit_list truly is a list!
            print(habit_list)
            try:
                habit_name = questionary.select(
                    "\nWhich habit do you want to delete?",
                    choices=habit_list
                ).ask()
                db.drop_habit((habit_name, ))   # argument must be turned into type tuple --> (arg,)
            except ValueError:
                print("\nThere are no habits available! Please select a different option."
                      "You could for example create a habit!\n")  # put more stuff in db.py drop_habit!

        elif main_menu == "Exit":
            stop = True
        else:
            print("\nInvalid input. Please select one of the displayed options.\n")


if __name__ == '__main__':
    cli()
