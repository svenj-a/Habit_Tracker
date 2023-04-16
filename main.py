import questionary
from db import DB
from habit import Habit
# from user import User


def cli():
    db = DB()
    DB.get_db(db)

    stop = False

    while not stop:
        login = questionary.select(
            "Welcome. Have you been here before?",
            choices=[
                "Login",
                "Register",
                "Exit"
            ]
        ).ask()

        if login == "Login":
            pass
        elif login == "Register":
            pass
        elif login == "Exit":
            stop = True

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
            habit = Habit.create_habit(db, name, desc, period)  # attribute kauderwelsch in habit und db class beheben!
            habit.store(db)
        elif main_menu == "Delete":
            habit_name = questionary.confirm("Which habit do you want to delete?").ask()
        elif main_menu == "Analyze":
            pass
        elif main_menu == "Logout":
            # return to login question
        elif main_menu == "Exit":
            stop = True


if __name__ == '__main__':
    cli()
