import sqlite3
# from user import User


# noinspection SqlNoDataSourceInspection
class DB:
    # __init__ function not necessarily required, since no objects is to be created.

    def __init__(self, name='main.db'):
        self.db = sqlite3.connect(name)
        self.cur = self.db.cursor()

    def get_db(self):
        self._create_table(self.db)
        return self.db

    def _create_table(self, db):
        # cur = db.cursor()  # try to avoid cursor and commit in every function

        # cur.execute("""CREATE TABLE IF NOT EXISTS users (
        #             name TEXT PRIMARY KEY,
        #             password TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS habits (
                            name TEXT PRIMARY KEY,
                            description TEXT,
                            periodicity TEXT,
                            creation_date DATE,
                            completed_total INTEGER,
                            current_streak INTEGER,
                            longest_streak INTEGER,
                            final_goal INTEGER
                            )""")
        db.commit()

    def add_habit(self, name, desc, period, creation_date, completed_total, current_streak, longest_streak, goal):
        # cur = db.cursor()
        # creation_date = date.today()
        # current_streak = 0
        # longest_streak = 0
        # username = User.get_current_username()
        habit_attributes = [name, desc, period, creation_date, completed_total, current_streak, longest_streak, goal]
        self.cur.execute("INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?)", habit_attributes)
        self.db.commit()

    # def add_user(self, db, username, password):
    #     cur = db.cursor()
    #     cur.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password))
    #     db.commit()

    def update_habit(self, name):
        pass

    def get_habit_data(self, name):
        self.cur.execute("SELECT * FROM habits WHERE name=?", name)
        self.db.commit()
        return self.cur.fetchall()

    def drop_habit(self, name):
        self.cur.execute("DELETE FROM habits WHERE name=?", name)
        self.db.commit()

# close database connection at the end of the program ???
