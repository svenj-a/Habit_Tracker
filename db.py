import sqlite3
from datetime import date
from user import User


def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
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


def add_habit(db, name, description, period):
    cur = db.cursor()
    creation_date = date.today()
    current_streak = 0
    longest_streak = 0
    username = User.get_current_username()
    habit_attributes = [name, description, period, creation_date, current_streak, longest_streak, username]
    cur.execute("INSERT INTO habits VALUES (?, ?, ?)", habit_attributes)
    db.commmit()


def add_user(db, name, password):
    cur = db.cursor()
    cur.execute("INSERT INTO users VALUES (?, ?, ?)", (name, password))
    db.commit()


def update_habit(name):
    pass


def get_habit_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE name=?", name)
    return cur.fetchall()
