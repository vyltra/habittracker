import tracker
from datetime import datetime, timedelta


# adds a habit and checks that it is correctly stored in the habit array
def test_add_habit():
    # Test case 1: Adding a new habit
    tracker.add_habit('workout', 7)
    assert 'workout' in tracker.habits
    assert tracker.habits['workout'].name == 'workout'
    assert tracker.habits['workout'].period == 7

    tracker.add_habit('drink_water', 1)
    assert 'drink_water' in tracker.habits
    assert tracker.habits['drink_water'].name == 'drink_water'
    assert tracker.habits['drink_water'].period == 1


# removes a habit and checks the habit array for it being removed
def test_remove_habit():
    tracker.add_habit('workout', 7)
    tracker.remove_habit('workout')
    assert 'workout' not in tracker.habits


# adds a task and checks for its existance
def test_add_task():
    tracker.add_habit('workout', 7)
    tracker.add_task('workout', 'task1')
    assert 'task1' in tracker.habits['workout'].tasks


# removes a task from a habit and checks for it being gone
def test_remove_task():
    tracker.add_habit('workout', 7)
    tracker.add_task('workout', 'task1')
    tracker.remove_task('workout', 'task1')
    assert 'task1' not in tracker.habits['workout'].tasks


# checks off a task and ensures a recent timestamp is stored
def test_check_task():
    tracker.add_habit('workout', 7)
    tracker.add_task('workout', 'task1')
    tracker.check_task('workout', 'task1')
    print(tracker.habits['workout'].tasks['task1'])
    # checks if the task now stores a recently created timestamp (created within the last 5 seconds)
    assert datetime.strptime(tracker.habits['workout'].tasks['task1'][0],
                             "%Y-%m-%d %H:%M:%S") > datetime.now() - timedelta(seconds=5)


# checks the return value of the calculate_streak method to ensure the streaks are calculated correctly
def test_calcualate_streak():
    tracker.add_habit('examplehabit', 7)
    tracker.add_task('examplehabit', 'task1')
    tracker.habits['examplehabit'].creation_date = "2023-08-01 01:40:31"
    tracker.habits['examplehabit'].tasks['task1'] = ["2023-08-01 15:40:31",
                                                     "2023-08-07 12:10:25",
                                                     "2023-08-13 03:36:35",
                                                     "2023-08-20 13:44:49",
                                                     "2023-08-27 13:08:53",
                                                     "2023-09-02 23:35:28",
                                                     "2023-09-08 12:24:43",
                                                     "2023-09-13 09:48:08",
                                                     "2023-09-20 08:41:03",
                                                     "2023-10-03 07:41:03",
                                                     "2023-10-09 06:21:03",
                                                     "2023-10-15 05:41:03"]
    tracker.add_task('examplehabit', 'task2')
    tracker.habits['examplehabit'].tasks['task2'] = ["2023-08-01 15:10:31",
                                                     "2023-08-07 12:20:25",
                                                     "2023-08-13 03:35:35",
                                                     "2023-08-20 18:44:49",
                                                     "2023-08-27 13:08:53",
                                                     "2023-09-02 21:35:28",
                                                     "2023-09-08 13:24:43",
                                                     "2023-09-13 07:48:08",
                                                     "2023-09-20 05:41:03",
                                                     "2023-10-03 07:41:03",
                                                     "2023-10-09 06:21:03",
                                                     "2023-10-15 05:41:03"]
    target = [[datetime(2023, 8, 1, 1, 40, 31), 8, datetime(2023, 9, 26, 1, 40, 31)],
              [datetime(2023, 10, 3, 1, 40, 31), 2, datetime(2023, 10, 17, 1, 40, 31)]]
    assert tracker.habits['examplehabit'].calculate_streak() == target
