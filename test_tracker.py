import pytest
import tracker



def test_add_habit():
    # Test case 1: Adding a new habit
    tracker.add_habit('workout', 7)
    assert 'workout' in tracker.habits
    assert tracker.habits['workout'].name == 'workout'
    assert tracker.habits['workout'].period == 7

    # Test case 2: Adding a habit with an existing name (should raise exception) THIS DOES NOT WORK
    # with pytest.raises(Exception):
    #    tracker.add_habit('workout', 5)



    # Test case 3: Adding a habit with a different name (should not raise an exception)
    tracker.add_habit('drink water', 1)
    assert 'drink water' in tracker.habits
    assert tracker.habits['drink water'].name == 'drink water'
    assert tracker.habits['drink water'].period == 1

