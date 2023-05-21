import datetime
import sqlite3


class DB:

    def __init__(self, name='main.db'):
        """
        A class to create a local sqlite3 database. An active db connection and a cursor object are created.
        :param name: name of the db file
        """
        self.db = sqlite3.connect(name)
        self.cur = self.db.cursor()

    def get_db(self):
        """
        Initializes the database.
        :return: returns the db
        """
        self._create_tables(self.db)
        return self.db

    def _create_tables(self, db):
        """
        Checks whether db tables already exists for a new db instance and creates them if not.
        :param db: name of the database
        :return:
        """
        # cur = db.cursor()  # try to avoid cursor and commit in every function
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
        self.cur.execute("""CREATE TABLE IF NOT EXISTS completions (
                            name TEXT,
                            completion_date TIMESTAMP,
                            PRIMARY KEY (name, completion_date),
                            FOREIGN KEY (name)
                                REFERENCES habits (name)
                                    ON DELETE CASCADE
                                    ON UPDATE NO ACTION 
                            )""")
        db.commit()

    def add_habit(self, name, desc, period, creation_date, completed_total, current_streak, longest_streak, goal):
        """
        Adds a new entity (a new row) to the habits table.
        :param name: name of the habit (str); provided by user input
        :param desc: description of the habit (str); provided by user input
        :param period: periodicity of the habit (str); "daily", "weekly" or "monthly"; selected by user
        :param creation_date: timestamp of the current date and time when a new habit is created
        :param completed_total: counts the total number of how often a habit has been checked off successfully (int)
        :param current_streak: counts the current day streak of a habit (how often a habit was completed in a row
                                without breaks (int)
        :param longest_streak: saves the longest day streak that was ever reached for a habit as "high score" (int)
        :param goal: number of times a habit is to be completed (int); provided by user input
        :return:
        """
        habit_attributes = [name, desc, period, creation_date, completed_total, current_streak, longest_streak, goal]
        self.cur.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", habit_attributes)
        self.db.commit()

    def add_completion(self, habit):
        """
        Adds a new entry to the completions table and saves a timestamp for each habit that is checked off.
        :param habit: name of the habit that is checked off
        :return:
        """
        date = datetime.datetime.today()
        self.cur.execute("""INSERT INTO completions (name, completion_date) VALUES (?, ?)""", (habit, date))
        self.db.commit()

    def update_streaks(self, name, curr_str, lon_str, comp_tot):
        """
        Updates the value for current_streak, longest_streak and completed_total every time a habit is checked off.
        :param name: name of the habit that needs to be updated
        :param curr_str: new value that is to be inserted into the column current_streak
        :param lon_str: new value that is to be inserted into the column longest_streak
        :param comp_tot: incremented value to be inserted for completed_total
        :return:
        """
        self.cur.execute("""UPDATE habits SET current_streak=? WHERE name=?""", (curr_str, name))
        self.cur.execute("""UPDATE habits SET longest_streak=? WHERE name=?""", (lon_str, name))
        self.cur.execute("""UPDATE habits SET completed_total=? WHERE name=?""", (comp_tot, name))
        self.db.commit()

    def drop_habit(self, name):
        """
        Deletes a habit from the database that is selected by the user.
        :param name: name of the habit to be deleted
        :return:
        """
        self.cur.execute("""DELETE FROM habits WHERE name=?""", name)
        self.db.commit()
