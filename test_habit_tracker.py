from db import DB
from habit import Habit
import analysis


class TestHabitTracker:

    def setup_method(self):  # change into fixture and use temporary db, so that no setup and teardown is needed
        self.db = DB(":memory:")

        Habit('sleep', 'Sleep at least 7h per day.', 'daily', 30).create_habit(self.db)
        Habit('brush teeth', 'Brush teeth every morning.', 'daily', 28).create_habit(self.db)
        Habit('clean bathroom', 'Clean the bathroom including toilet, shower, and sink.', 'weekly', 8
              ).create_habit(self.db)
        Habit('call mom', 'Call my mother once a month...', 'monthly', 4).create_habit(self.db)
        Habit('meditate', 'Meditate at least 10 minutes every day after lunch.', 'daily', 60).create_habit(self.db)

        # add completion events with complete habit method and non-default timestamp arguments

    def test_create_habit(self):    # necessary? If create_habit() doesn't work, the fixtures don't work either!
        pass

    def test_complete_habit(self, name='sleep'):  # necessary? see above
        habit = Habit(name)
        habit.complete_habit(self.db, name)
        assert habit.current_streak == 1 and habit.longest_streak == 1

    def test_list_all_habits(self):
        data = analysis.list_all_habits(self.db)
        assert len(data) == 5  # is it sufficient to check for length or must db entry be checked?

    def test_filtered_habits(self):
        pass

    def test_view_single_habit(self):
        pass    # assert returned tuple

    def test_view_longest_streak(self):
        pass    # assert returned tuple

    def test_view_closest_goal(self):
        pass

    def test_delete_habit(self, name='call mom'):
        self.db.drop_habit((name, ))
        habits = analysis.list_all_habits(self.db)
        assert len(habits) == 4  # is it sufficient to check for length or must db entry be checked?
