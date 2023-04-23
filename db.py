import sqlite3
from datetime import date
# from user import User


# noinspection SqlNoDataSourceInspection
class DB:
    # __init__ function not necessarily required, since no objects is to be created.

    def __init__(self, name='main.db'):
        self.db = sqlite3.connect(name)
        self.cur = self.db.cursor()
        # self.create_tables(self.db)

    def get_db(self):
        # db = sqlite3.connect(name)
        # cur = db.cursor()
        self.create_tables(self.db)
        return self.db

    def create_tables(self, db):
        # cur = db.cursor()  # try to avoid cursor and commit in every function

        # cur.execute("""CREATE TABLE IF NOT EXISTS users (
        #             name TEXT PRIMARY KEY,
        #             password TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS habits (
                            habit_name TEXT PRIMARY KEY,
                            description TEXT,
                            periodic TEXT,
                            creation_date DATE,
                            current_streak INTEGER,
                            longest_streak INTEGER,
                            final_goal INTEGER
                            )""")
        db.commit()

    def add_habit(self, name, desc, period, creation_date, current_streak, longest_streak, goal):
        # cur = db.cursor()
        # creation_date = date.today()
        # current_streak = 0
        # longest_streak = 0
        # username = User.get_current_username()
        habit_attributes = [name, desc, period, creation_date, current_streak, longest_streak, goal]
        self.cur.execute("INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?)", habit_attributes)
        self.db.commit()

    # def add_user(self, db, username, password):
    #     cur = db.cursor()
    #     cur.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password))
    #     db.commit()

    def update_habit(self, db, name):
        pass

    def get_habit_data(self, db, name):
        cur = db.cursor()
        cur.execute("SELECT * FROM habits WHERE name=?", name)
        return cur.fetchall()

# close database connection at the end of the program ???
