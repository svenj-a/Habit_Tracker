import questionary
from db import DB
from habit import Habit
# from user import User


def cli():
    db = DB()
    DB.get_db(db)

    stop = False

    while not stop:
        # login = questionary.select(
        #     "Welcome. Have you been here before?",
        #     choices=[
        #         "Login",
        #         "Register",
        #         "Exit"
        #     ]
        # ).ask()
        #
        # if login == "Login":
        #     pass
        # elif login == "Register":
        #     pass
        # elif login == "Exit":
        #     stop = True

        main_menu = questionary.select(
            "What do you want to do?",
            choices=["Create", "Delete", "Analyze", "Logout", "Exit"]
        ).ask()

        if main_menu == "Create":
            name = questionary.text("What's the name of your new habit?").ask()
            desc = questionary.text("Please provide a short description of your habit.").ask()
            period = questionary.select(
                "How often do you want to perform your habit?",
                choices=["daily", "weekly", "monthly"]
            ).ask()
            goal = questionary.text(
                "Set a final goal. Choose the number of days/ weeks/ months you want to perform the habit."
            ).ask()
            habit = Habit(name, desc, period, int(goal))
            habit.create_habit(db)
            # add exception handling for already existing names or add artificial key for habits table in DB!

        elif main_menu == "Delete":
            habit_name = questionary.text("Which habit do you want to delete?").ask()
            # change to questionary.select type and display the selection of currently stored habits.
        elif main_menu == "Analyze":
            pass
        # print(self.cur.execute("SELECT * FROM habits"))
        elif main_menu == "Logout":
            # return to log in question
            pass
        elif main_menu == "Exit":
            stop = True
        else:
            print("\nInvalid input. Please select one of the displayed options.\n")


if __name__ == '__main__':
    cli()
