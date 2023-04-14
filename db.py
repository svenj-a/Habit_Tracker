import sqlite3


class DB:

    def __int__(self, db):
        self.db_name = db

    def get_db(self, name="main.db"):       # main db is later exchanged against test.db or else
        db = sqlite3.connect(name)
        return db

    def create_tables(self, db):
        cur = db.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    name TEXT PRIMARY KEY,
                    password TEXT)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS habits (
                    habitID INT NOT NULL UNIQUE AUTO_INCREMENT,
                    name TEXT,
                    description TEXT,
                    date TIMESTAMP,
                    period TEXT,
                    current_streak INTEGER,
                    longest_streak INTEGER,
                    username,
                    FOREIGN KEY (username) REFERENCES users(name),
                    PRIMARY KEY (habitID))""")

        db.commit()

    def add_habit(self, db, name, description, period):
        cur = db.cursor()
        cur.execute("INSERT INTO habits VALUES (?, ?, ?)", (name, description, period))
        db.commmit()

    def add_user(self, db, name, password):
        cur = db.cursor()
        cur.execute("INSERT INTO users VALUES (?, ?, ?)", (name, password))
        db.commit()

    def get_habit_data(self, db, name):
        cur = db.cursor()
        cur.execute("SELECT * FROM habits WHERE name=?", (name))
        return cur.fetchall()
