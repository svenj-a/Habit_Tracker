from datetime import datetime
import sqlite3


class DB:

    def __init__(self, name='main.db'):
        """
        A class to create a local sqlite3 database. An active db connection and a cursor object are created.
        :param name: name of the db file, default is "main.db", for testing use "test.db"
        """
        self.db = sqlite3.connect(name)
        self.cur = self.db.cursor()
        self._get_db()

    def _get_db(self):
        """
        Initializes the database.
        :return: database
        """
        self._create_tables()
        return self.db

    def _create_tables(self):
        """
        Checks whether database tables already exist for a new db instance and creates them if not.
        """
        self.cur.execute("""CREATE TABLE IF NOT EXISTS habits (
                            name TEXT PRIMARY KEY,
                            description TEXT,
                            period TEXT,
                            creation_date DATE,
                            current_streak INTEGER,
                            longest_streak INTEGER,
                            total INTEGER,
                            goal INTEGER,
                            established BOOLEAN
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
        self.db.commit()

    def add_habit(self, name, desc, period, creation_date, completed_total, current_streak, longest_streak, goal,
                  goal_reached):
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
        :param goal_reached: boolean value that indicates where a habit is established
        """
        habit_attributes = [name, desc, period, creation_date, current_streak, longest_streak, completed_total, goal,
                            goal_reached]
        self.cur.execute("""INSERT INTO habits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", habit_attributes)
        self.db.commit()

    def add_completion(self, habit, date=datetime.today()):
        """
        Adds a new entry to the completions table and saves a timestamp for each habit that is checked off.
        :param habit: name of the habit that is checked off
        :param date: timestamp of completion event. Default value is the current timestamp, other values can be inserted
        for testing purposes.
        """
        self.cur.execute("""INSERT INTO completions (name, completion_date) VALUES (?, ?)""", (habit, date))
        self.db.commit()

    def update_streaks(self, name, curr_str, lon_str, comp_tot):
        """
        Updates the value for current_streak, longest_streak and completed_total when a habit is completed.
        :param name: name of the habit that needs to be updated
        :param curr_str: new value to be inserted for current_streak
        :param lon_str: new value to be inserted for longest_streak
        :param comp_tot: incremented value to be inserted for completed_total
        """
        self.cur.execute("""UPDATE habits SET current_streak=? WHERE name=?""", (curr_str, name))
        self.cur.execute("""UPDATE habits SET longest_streak=? WHERE name=?""", (lon_str, name))
        self.cur.execute("""UPDATE habits SET total=? WHERE name=?""", (comp_tot, name))
        self.db.commit()

    def update_established(self, goal_reached, name):
        """
        Updates the value for established when the final goal is reached.
        :param goal_reached: value to be inserted for established
        :param name: name of the habit that needs to be updated
        """
        self.cur.execute("""UPDATE habits SET established=? WHERE name=?""", (goal_reached, name))
        self.db.commit()

    def drop_habit(self, name):
        """
        Deletes a habit from the database that is selected by the user.
        :param name: name of the habit to be deleted
        :return:
        """
        self.cur.execute("""DELETE FROM habits WHERE name=?""", name)
        self.db.commit()
