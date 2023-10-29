from datetime import datetime, timedelta
import TrackerExceptions as Exceptions

# main habit class to define habit structure
class Habit:
    def __init__(self, name, period):
        # input check name
        if not isinstance(name, str):
            raise TypeError("The Habit's name must be a string!")

        # input check period
        try:
            period = int(period)
        except ValueError:
            raise Exceptions.HabitTypeError("The Habit's period must be an integer between 0 and 365!")

        if not period < 365:
            raise Exceptions.HabitTypeError("The Habit's period must be an integer between 0 and 365!x")

        self.period = period
        self.name = name
        self.creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.tasks = {}

    # adds a task to the habit
    def add_task(self, name):
        if name in self.tasks:
            raise Exceptions.ElementAlreadyExists('This Task already exists!')
        else:
            self.tasks[name] = []
            print('Added task ' + name + ' to Habit ' + self.name)

    # removes a task from the habit
    def remove_task(self, name):
        if name in self.tasks:
            del self.tasks[name]
            print('Task ' + name + ' in Habit ' + self.name + ' has been removed')
        else:
            raise Exceptions.ElementNotFound('There is no task with that name!')

    # "checks off" a task - adds the current timestamp to the array of the respective task
    def check_task(self, name):
        if name not in self.tasks:
            raise Exceptions.ElementNotFound('There is no task with that name!')
        else:
            self.tasks[name].append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print('Checked Task')

    # returns a list of all tasks currently set for the habit
    def get_all_tasks(self):
        print(list(iter(self.tasks)))
        return

    # analysis module core - computes all streaks achieved for the habit
    def calculate_streak(self):
        completions = []
        # convert task timestamps to datetime objects and store in array
        for n in self.tasks.items():
            task_completions = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in n[1]]
            completions.append(task_completions)

        # init variables used for analysis below
        step = datetime.strptime(self.creation_date, '%Y-%m-%d %H:%M:%S')
        active_streak = False
        streak_start = None
        streak_end = None
        streak_duration = 0
        analysis_data = []

        # while loop to step through the time periods being analyzed
        while step <= datetime.now():
            # function to check if a timestamp is between the current step and step + period
            is_between = lambda dt: step <= dt <= step + timedelta(days=self.period)

            # generator expression to check if for the current period, every task has been completed at least once
            analyse_cache = sum(any(is_between(dt) for dt in x) for x in completions)
            # check if current period is a streak
            if analyse_cache == len(completions) and not active_streak:
                streak_start = step
                streak_duration += 1
                active_streak = True
            elif analyse_cache == len(completions) and active_streak:
                streak_duration += 1
            elif analyse_cache != len(completions) and active_streak:
                streak_end = step
                active_streak = False
                analysis_data.append([streak_start, streak_duration, streak_end])
                streak_duration = 0
            step += timedelta(days=self.period)
        # check if streak is still active after loop - if write to array (ongoing streak)
        if active_streak:
            streak_end = step
            analysis_data.append([streak_start, streak_duration, streak_end])

        return analysis_data

