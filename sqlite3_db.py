import sqlite3
# create db and handle
database = sqlite3.connect("habit_tracker.db")
cursor = database.cursor()

# create tables and insert values
cursor.execute("create table habits (name text, info text, date_created date, period , goal integer, streak integer)")
predefined_habits = [] # insert list of tuples
cursor.executemany("insert into habits values (?, ?, ?)", predefined_habits)

# print db records
for row in cursor.execute("select * from habtis"):
    print(row)

# close db handle
database.close()
