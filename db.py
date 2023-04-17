import sqlite3
from datetime import date
from user import User


class DB:
    # __init__ function not necessarily required, since no objects is to be created.

    # def __init__(self, name='main.db'):
        # self.db = sqlite3.connect(name)

    def get_db(self, name='main.db'):
        db = sqlite3.connect(name)
        self.create_tables(db)
        return db

    def create_tables(self, db):
        cur = db.cursor()  # try to avoid cursor and commit in every function

        cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    name TEXT PRIMARY KEY,
                    password TEXT)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS habits (
                    habitID INT NOT NULL UNIQUE AUTO_INCREMENT,
                    name TEXT,
                    description TEXT,
                    period TEXT,
                    date TIMESTAMP,
                    current_streak INTEGER,
                    longest_streak INTEGER,
                    username TEXT,
                    PRIMARY KEY (habitID),
                    FOREIGN KEY (username) REFERENCES users(name))""")

        db.commit()

    def add_habit(self, db, name, description, period):
        cur = db.cursor()
        creation_date = date.today()
        current_streak = 0
        longest_streak = 0
        username = User.get_current_username()
        habit_attributes = [name, description, period, creation_date, current_streak, longest_streak, username]
        cur.execute("INSERT INTO habits VALUES (?, ?, ?)", habit_attributes)
        db.commmit()

    def add_user(self, db, username, password):
        cur = db.cursor()
        cur.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password))
        db.commit()

    def update_habit(self, name):
        pass

    def get_habit_data(self, db, name):
        cur = db.cursor()
        cur.execute("SELECT * FROM habits WHERE name=?", name)
        return cur.fetchall()
