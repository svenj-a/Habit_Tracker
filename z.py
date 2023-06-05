from habit import Habit
from db import DB

db = DB()

habit = Habit('sleep')
habit.fetch_habit_data(db, 'sleep')
