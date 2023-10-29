import os.path
from datetime import datetime
import json
import argparse
import TrackerExceptions as Exceptions
from TrackerHabit import Habit

# global Error / Warning sign
err = "[Error]"
war = "[Warning] "

# init habits array - stores all habits loaded into memory
habits = {}


# adds a habit
def add_habit(name, period):
    try:
        if name in habits:
            raise Exceptions.ElementAlreadyExists('A Habit with that name already exists!')
        else:
            habits[name] = Habit(name, period)
            print('Added Habit: ' + name)
    except Exception as e:
        print(err, str(e))


# removes a habit
def remove_habit(name):
    try:
        if name in habits:
            del habits[name]
            print('Deleted Habit ' + name)
        else:
            raise Exceptions.ElementNotFound('There is no habit with that name!')
    except Exception as e:
        print(err, str(e))


# wrapper function to add a task to a habit
def add_task(habit, task):
    try:
        if not habit in habits:
            raise Exceptions.ElementNotFound('There is no habit with that name!')
        else:
            habits[habit].add_task(task)
    except Exception as e:
        print(err, str(e))


# wrapper function to remove a task from a habit
def remove_task(habit, task):
    try:
        if not habit in habits:
            raise Exceptions.ElementNotFound('There is no habit with that name!')
        else:
            habits[habit].remove_task(task)
    except Exception as e:
        print(err, str(e))


# wrapper function to check off a task in a habit
def check_task(habit, task):
    try:
        if not habit in habits:
            raise Exceptions.ElementNotFound('There is no habit with that name!')
        else:
            habits[habit].check_task(task)
    except Exception as e:
        print(err, str(e))


# prints list of all habits stored in habits dict
def get_all_habits():
    print(list(habits.keys()))


# prints all periods and their associated habits
def get_habits_by_period():
    # loop through all stored habits and extract periods
    unique_periods = set(habit.period for habit in habits.values())

    # loop through set of unique periods to extract habit names
    for period in sorted(unique_periods):
        filtered_habits = [habit.name for habit in habits.values() if habit.period == period]
        print("Habits with Period " + str(period) + ": " + str(filtered_habits))


# prints all tasks for a habit
def get_all_tasks(habit):
    try:
        if not habit in habits:
            raise Exceptions.ElementNotFound('There is no habit with that name!')
        else:
            habits[habit].get_all_tasks()
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


# prints analysis data for a habit
def get_analysis(habit):
    try:
        if not habit in habits:
            raise Exceptions.ElementNotFound('There is no habit with that name!')
        else:
            streaks = habits[habit].calculate_streak()
            print("Here is the analysis for your " + habit + " Habit")
            print("-------------------------------------")
            print("This Habit has " + str(len(streaks)) + " Streaks")
            print("-------------------------------------")
            for n in range(0, len(streaks)):
                print("--- Streak Number: " + str(n + 1) + " ---")
                print("Streak Start: " + str(streaks[n][0]))
                print("Streak Duration: " + time_unit_conversion(streaks[n][1] * habits[habit].period) + " (" + str(
                    streaks[n][1]) + " Periods)")
                # print Ongoing instead of date in the future
                if streaks[n][2] > datetime.now():
                    streaks[n][2] = "Ongoing"
                print("Streak End: " + str(streaks[n][2]))
    except Exception as e:
        print(err, str(e))


# prints analysis data to find the longest streak between all habits
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
    print(
        "It lasted for " + time_unit_conversion(top_streak["days"]) + " (" + str(
            round(top_streak["days"] / top_streak["period"], 2)) + " Period(s))")
    print("Beginning on " + datetime.strftime(top_streak["start"],
                                              "%Y-%m-%d %H:%M:%S") + " and Ending on " + datetime.strftime(
        top_streak["end"], "%Y-%m-%d %H:%M:%S"))


# prints max streak for a single habit
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

    print("The Longest Streak in your " + habit + " Habit lasted for " + time_unit_conversion(
        top_streak["days"]) + " (" + str(round(top_streak["days"] / top_streak["period"], 2)) + " Period(s))")
    print("Beginning on " + datetime.strftime(top_streak["start"],
                                              "%Y-%m-%d %H:%M:%S") + " and Ending on " + datetime.strftime(
        top_streak["end"], "%Y-%m-%d %H:%M:%S"))


# converts data in habits dict to json and saves to file
def save_to_file():
    data = []
    try:
        for habit in habits:
            data.append(
                {'name': habits[habit].name, 'period': habits[habit].period,
                 'creation_date': habits[habit].creation_date,
                 'tasks': habits[habit].tasks})
            if not habits[habit].tasks:
                raise Exceptions.IncompleteHabit('Could not save! --> Tasks for one or more habits are empty.')

        with open('hbtracker_save.json', 'w') as f:
            json.dump(data, f)
        f.close()
        print('Saved!')
    except Exception as e:
        print(err, str(e))


# looks for save file - uses json information to create all habit objects and store them in habits array
# creates new save file of none is found
def load_from_file():
    # overwirte error handling
    if os.path.exists('hbtracker_save.json'):
        print('Loading Save Data from file...')
        with open('hbtracker_save.json', 'r') as f:
            data = json.load(f)
        f.close()
        for entry in data:
            habit = Habit(entry['name'], entry['period'])
            habit.creation_date = entry['creation_date']
            habit.tasks = entry['tasks']
            habits[habit.name] = habit
    else:
        print(war + 'No Save File found!')


# clears habit array and reloads data from save file
# initially used for debugging, left in because it might be useful for testing
def reload():
    habits.clear()
    load_from_file()


# wrapper function to clear the screen - quality of life feature
def clear_screen():
    os.system('cls')


# joins string input list into single string
def join_arguments(args):
    return ' '.join(args)


# main method that handles user input and command mapping
def main():
    # parsers used to handle commands with parameters
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

    parser_checktask = subparsers.add_parser('checkTask', help='Checks off a Task in a Habit')
    parser_checktask.add_argument('habit')
    parser_checktask.add_argument('task')

    parser_checktask = subparsers.add_parser('getAllTasks', help='Returns all Tasks for a Habit')
    parser_checktask.add_argument('habit')

    parser_checktask = subparsers.add_parser('analyze', help='Calculates all streaks for a Habit')
    parser_checktask.add_argument('habit')

    parser_checktask = subparsers.add_parser('getMaxStreak', help='Calculates the maximum streak for a Habit')
    parser_checktask.add_argument('habit')

    # subparsers used to handle commands that do not require parameters
    subparsers.add_parser('reload', help='reload save file')
    subparsers.add_parser('getMaxStreakAll', help='Calculates the maximum streak between all Habits')
    subparsers.add_parser('getAllHabits', help='Returns all stored Habits')
    subparsers.add_parser('getHabitsByPeriod', help='Returns Lists of Habits sorted by period')
    subparsers.add_parser('save', help='Saves data to file')
    subparsers.add_parser('clear', help='Clear the screen')

    # dict stores mappings for commands to corresponding functions
    commandFunctionMapping = {
        'reload': reload,
        'getAllHabits': get_all_habits,
        'getHabitsByPeriod': get_habits_by_period,
        'getAllTasks': get_all_tasks,
        'addHabit': add_habit,
        'removeHabit': remove_habit,
        'save': save_to_file,
        'clear': clear_screen,
        'addTask': add_task,
        'removeTask': remove_task,
        'checkTask': check_task,
        'analyze': get_analysis,
        'getMaxStreakAll': get_max_streak_all,
        'getMaxStreak': get_max_streak_single,
    }

    # main loop that handles user input
    while True:
        userInput = input("HabitTracker> ")
        if userInput == 'exit':
            break
        elif userInput == "":
            pass
        elif userInput == "help" or userInput == "-h":
            parser.print_help()
        else:
            if userInput.split()[0] in commandFunctionMapping:
                try:
                    args = parser.parse_args(userInput.split())
                    function = commandFunctionMapping[args.command]
                    function_args = vars(args)
                    function_args.pop("command")
                    function(**function_args)
                except SystemExit:
                    pass
            else:
                print("Invalid Command")


# program startup function - loads save file and hands off to main loop
if __name__ == '__main__':
    print("### HabitTracker 1.0 ###")
    load_from_file()
    main()
