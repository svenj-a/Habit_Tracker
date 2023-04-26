import questionary
import sqlite3
from db import DB
from habit import Habit


def cli():
    db = DB("trialDB.db")   # remove name and .db files for first run!!
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
            goal = questionary.text(
                "Set a final goal: How often do you want to perform the habit? Please insert a number..."
            ).ask()

            habit_created = False
            while not habit_created:
                try:
                    habit = Habit(name, desc, period, int(goal))
                    habit.create_habit(db)
                    habit_created = True
                except TypeError:
                    print("Please enter an integer number!")
                except sqlite3.IntegrityError:
                    print(f"A habit with the name {name} already exists. Please choose a different name:")
                    name = questionary.text("What's the name of your new habit?").ask()
        elif main_menu == "Complete habit":
            pass
        elif main_menu == "Analyze habits":
            analysis_menu = questionary.select(
                "What do you want to know about your habits?",
                choices=["View all habits", "View habits with periodicity ...", "View personal record"]
            ).ask()
            if analysis_menu == "View all habits":
                db.cur.execute("SELECT * FROM habits")
                all_habits = db.cur.fetchall()
                for habit in all_habits:
                    print(habit)
            elif analysis_menu == "View habits with periodicity ...":
                pass

        elif main_menu == "Delete habit":
            db.cur.execute("""SELECT name FROM habits ORDER BY name ASC""")
            habit_list = db.cur.fetchall()
            print(habit_list)
            habit_name = questionary.select(
                "Which habit do you want to delete?",
                choices=[habit_list]
            ).ask()                     # What's the problem here? AttributeError: 'list' object has no attribute 'get'
            db.drop_habit(db, habit_name)

        elif main_menu == "Exit":
            stop = True
        else:
            print("\nInvalid input. Please select one of the displayed options.\n")


if __name__ == '__main__':
    cli()
