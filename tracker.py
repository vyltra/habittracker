import os.path
from datetime import datetime, timedelta
import json
import argparse

# fix input string spaces
# add overwrite error check
# add unit tests
# add analysis

# global Error / Warning sign
err = "[Error]"
war = "[Warning]"


class HabitTypeError(Exception):
    pass


class ElementNotFound(Exception):
    pass


class ElementAlreadyExists(Exception):
    pass


class IncompleteHabit(Exception):
    pass


class Habit:
    def __init__(self, name, period):
        # input check name
        if not isinstance(name, str):
            raise TypeError("The Habit's name must be a string!")

        # input check period
        try:
            period = int(period)
        except ValueError:
            raise HabitTypeError("The Habit's period must be an integer between 0 and 365!")

        if not period < 365:
            raise HabitTypeError("The Habit's period must be an integer between 0 and 365!x")
        self.period = period

        self.name = name

        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tasks = {}

    def add_task(self, name):
        if name in self.tasks:
            raise ElementAlreadyExists('This Task already exists!')
        else:
            self.tasks[name] = ['1970-01-01 00:00:00']
            print('Added task ' + name + ' to Habit ' + self.name)

    def remove_task(self, name):
        if name in self.tasks:
            del self.tasks[name]
            print('Task ' + name + ' in Habit ' + self.name + ' has been removed')
        else:
            raise ElementNotFound('There is no task with that name!')

    def check_task(self, name):
        if name not in self.tasks:
            raise ElementNotFound('There is no task with that name!')
        else:
            self.tasks[name].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print('Checked Task')

    def getAllTasks(self):
        print(list(iter(self.tasks)))
        return

    def calculate_streak(self):

        completions = []
        for n in self.tasks.items():
            task_completions = [datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in n[1]]
            completions.append(task_completions)

        step = datetime.strptime(self.creation_date, "%Y-%m-%d %H:%M:%S")

        active_streak = False
        streak_start = None
        streak_end = None
        streak_duration = 0
        analysis_data = []

        while step <= datetime.now():
            # function to check if a timestamp is between the current step and step + period
            is_between = lambda dt: step <= dt <= step + timedelta(days=self.period)

            # function to check if for the current period, every task has been completed at least once
            analyse_cache = 0
            for n in range(0, len(completions)):
                result = any(is_between(dt) for dt in completions[n])
                if result: analyse_cache += 1

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

            # print("Between: "+str(step)+" and :" + str(step+timedelta(days=self.period))+" is between: " + str(result))
            step += timedelta(days=self.period)

        # print("Streak Analysis Data: " + str(analysis_data))

        # task_dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in self.tasks.items()[1]]
        # print(str(task_dates))

        return analysis_data


habits = {}


def add_habit(name, period):
    try:
        if name in habits:
            raise ElementAlreadyExists('A Habit with that name already exists!')
        else:
            habits[name] = Habit(name, period)
            print('Added Habit: ' + name)
    except Exception as e:
        print(err, str(e))


def remove_habit(name):
    try:
        if name in habits:
            del habits[name]
            print('Deleted ' + name)
        else:
            print('There is no habit with that name!')
    except Exception as e:
        print(err, str(e))


def addTask(habit, task):
    try:
        if not habit in habits:
            print("Error: There is no Habit with that Name!")
        else:
            habits[habit].add_task(task)
    except Exception as e:
        print(err, str(e))


def removeTask(habit, task):
    try:
        if not habit in habits:
            print("There is no Habit with that Name!")
        else:
            habits[habit].remove_task(task)
    except Exception as e:
        print(err, str(e))


def checkTask(habit, task):
    try:
        if not habit in habits:
            print("There is no Habit with that Name!")
        else:
            habits[habit].check_task(task)
    except Exception as e:
        print(err, str(e))


def get_all_habits():
    print(list(habits.keys()))


def get_habits_by_period():
    # loop through all stored habits and extract periods
    unique_periods = set(habit.period for habit in habits.values())

    # loop through set of unique periods to extract habit names
    for period in sorted(unique_periods):
        filtered_habits = [habit.name for habit in habits.values() if habit.period == period]
        print("Habits with Period " + str(period) + ": " + str(filtered_habits))


def get_all_tasks(habit):
    try:
        if not habit in habits:
            print("There is no Habit with that Name!")
        else:
            habits[habit].getAllTasks()
    except Exception as e:
        print(err, str(e))


# helper function that takes days as input and converts them into weeks / months
def time_unit_conversion(days):
    if days < 0:
        return "Input must be a non-negative number of days."

    weeks, remaining_days = divmod(days, 7)

    if weeks > 0 and remaining_days > 0:
        return f"{weeks} week{'s' if weeks > 1 else ''} and {remaining_days} day{'s' if remaining_days > 1 else ''}"
    elif weeks > 0:
        return f"{weeks} week{'s' if weeks > 1 else ''}"
    elif days > 0:
        return f"{days} day{'s' if days > 1 else ''}"
    else:
        return "0 days"


def get_analysis(habit):
    try:
        if not habit in habits:
            print("There is no Habit with that Name!")
        else:
            streaks = habits[habit].calculate_streak()
            print("Here is the analysis for your " + habit + " Habit")
            print("-------------------------------------")
            print("This habit has " + str(len(streaks)) + " Streaks")
            print("-------------------------------------")
            for n in range(0, len(streaks)):
                print("--- Streak Number: " + str(n + 1) + " ---")
                print("Streak Start: " + str(streaks[n][0]))
                print("Streak Duration: " + time_unit_conversion(streaks[n][1] * habits[habit].period) + " (" + str(
                    streaks[n][1]) + " Periods)")
                print("Streak End: " + str(streaks[n][2]))
    except Exception as e:
        print(err, str(e))


def get_max_streak_all():
    top_streak = {"days": 0}
    for habit in habits:
        # streaks[habits[habit].name] = habits[habit].calculate_streak()
        data = habits[habit].calculate_streak()
        for streaks in data:
            streak_days = streaks[1] * habits[habit].period
            if streak_days > top_streak["days"]:
                top_streak["days"] = streak_days
                top_streak["habit"] = habits[habit].name
                top_streak["period"] = habits[habit].period
                top_streak["start"] = streaks[0]
                top_streak["end"] = streaks[2]

    print("The Longest Streak was your " + top_streak["habit"] + " Habit")
    print("It lasted for " + time_unit_conversion(top_streak["days"]) + " (" + str(top_streak["period"]) + " Period(s))")
    print("Beginning on " + datetime.strftime(top_streak["start"], "%Y-%m-%d %H:%M:%S") + " and Ending on " + datetime.strftime(top_streak["end"], "%Y-%m-%d %H:%M:%S"))


def get_max_streak_single(habit):
    top_streak = {"days": 0}
    data = habits[habit].calculate_streak()
    for streaks in data:
        streak_days = streaks[1] * habits[habit].period
        if streak_days > top_streak["days"]:
            top_streak["days"] = streak_days
            top_streak["period"] = habits[habit].period
            top_streak["start"] = streaks[0]
            top_streak["end"] = streaks[2]

    print("The Longest Streak in your " + habit + " Habit lasted for " + time_unit_conversion(top_streak["days"]) + " (" + str(top_streak["period"]) + " Period(s))")
    print("Beginning on " + datetime.strftime(top_streak["start"], "%Y-%m-%d %H:%M:%S") + " and Ending on " + datetime.strftime(top_streak["end"], "%Y-%m-%d %H:%M:%S"))


def save_to_file():
    data = []
    try:
        for habit in habits:
            data.append(
                {'name': habits[habit].name, 'period': habits[habit].period,
                 'creation_date': habits[habit].creation_date,
                 'tasks': habits[habit].tasks})
            if not habits[habit].tasks:
                raise IncompleteHabit('Could not save! --> Tasks for one or more habits are empty.')

        with open('hbtracker_save.json', 'w') as f:
            json.dump(data, f)
        f.close()
        print('Saved!')
    except Exception as e:
        print(err, str(e))


def load_from_file():
    # overwirte error handleing
    if os.path.exists('hbtracker_save.json'):
        print('Loading Save Data from file...')
    else:
        print(war + 'No Save File found! Creating new... ')

    with open('hbtracker_save.json', 'r') as f:
        data = json.load(f)
    f.close()
    for entry in data:
        habit = Habit(entry['name'], entry['period'])
        habit.creation_date = entry['creation_date']
        habit.tasks = entry['tasks']
        habits[habit.name] = habit


def reload():
    habits.clear()
    load_from_file()


def writer():
    add_habit('workout', 7)
    habits['workout'].add_task('sit ups')
    habits['workout'].add_task('stand ups')
    habits['workout'].add_task('pull ups')
    add_habit('drink water', 1)
    habits['drink water'].add_task('drink 2L')
    add_habit('learn new skill', 30)
    habits['learn new skill'].add_task('read book')
    habits['learn new skill'].add_task('practice')
    habits['learn new skill'].add_task('show people')
    habits['learn new skill'].add_task('write report')
    habits['workout'].check_task('sit ups')
    habits['workout'].check_task('stand ups')
    habits['workout'].check_task('pull ups')
    habits['workout'].check_task('pull ups')


def clearScreen():
    os.system('cls')


# joins string input list into single string
def join_arguments(args):
    return ' '.join(args)


def main():
    parser = argparse.ArgumentParser(prog='Habit Tracker', description='Habit Tracker 1.0')
    subparsers = parser.add_subparsers(title='Commands', dest='command')

    parser_addhabit = subparsers.add_parser('addHabit', help='Adds a Habit')
    parser_addhabit.add_argument("name")
    parser_addhabit.add_argument("period")

    parser_removehabit = subparsers.add_parser('removeHabit', help='Removes a Habit and all its data')
    parser_removehabit.add_argument("name")

    parser_addtask = subparsers.add_parser('addTask', help='Adds a Task to a Habit')
    parser_addtask.add_argument("habit")
    parser_addtask.add_argument("task")

    parser_removetask = subparsers.add_parser('removeTask', help='Removes a Task from a Habit')
    parser_removetask.add_argument('habit')
    parser_removetask.add_argument('task')

    parser_checktask = subparsers.add_parser('checkTask', help='Checks off a Task')
    parser_checktask.add_argument('habit')
    parser_checktask.add_argument('task')

    parser_checktask = subparsers.add_parser('getAllTasks', help='Returns all Tasks for a habit')
    parser_checktask.add_argument('habit')

    parser_checktask = subparsers.add_parser('analyze', help='Returns all Tasks for a habit')
    parser_checktask.add_argument('habit')

    parser_checktask = subparsers.add_parser('getMaxStreak', help='Returns all Tasks for a habit')
    parser_checktask.add_argument('habit')

    subparsers.add_parser('reload', help='reload save file')
    subparsers.add_parser('getLongest', help='reload save file')
    subparsers.add_parser('getAllHabits', help='Returns all stored Habits')
    subparsers.add_parser('getHabitsByPeriod', help='Returns Lists of Habits sorted by period')
    subparsers.add_parser('save', help='Saves data to file')
    subparsers.add_parser('clear', help='Clear the screen')

    commandFunctionMapping = {
        'reload': reload,
        'getAllHabits': get_all_habits,
        'getHabitsByPeriod': get_habits_by_period,
        'getAllTasks': get_all_tasks,
        'addHabit': add_habit,
        'removeHabit': remove_habit,
        'save': save_to_file,
        'clear': clearScreen,
        'addTask': addTask,
        'removeTask': removeTask,
        'checkTask': checkTask,
        'analyze': get_analysis,
        'getLongest': get_max_streak_all,
        'getMaxStreak': get_max_streak_single,
    }

    while True:
        userInput = input("HabitTracker> ")
        if userInput == 'exit':
            break
        elif userInput == "":
            pass
        else:
            try:
                args = parser.parse_args(userInput.split())
                if args.command in commandFunctionMapping:
                    function = commandFunctionMapping[args.command]
                    function_args = vars(args)
                    function_args.pop("command")
                    function(**function_args)
                else:
                    print("Invalid Command")

            except SystemExit:
                pass


if __name__ == '__main__':
    print("### HabitTracker 1.0 ###")
    load_from_file()
    main()
