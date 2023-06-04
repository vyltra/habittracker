import os.path
from datetime import datetime, timedelta
import json
import argparse

# add custom error handles
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

    def get_current_streak(self):
        # figure out start time for backtrack
        timestamp = datetime.strptime(self.creation_date, "%Y-%m-%d %H:%M:%S")
        today = datetime.now()
        delta = (today - timestamp).days
        num_intervals = delta // self.period
        closest_date = timestamp + timedelta(days=num_intervals * self.period) if timestamp + timedelta(
            days=num_intervals * self.period) <= today else timestamp + timedelta(
            days=(num_intervals - 1) * self.period)
        print(closest_date)

        return


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


def save_to_file():
    data = []
    try:
        for habit in habits:
            data.append(
                {'name': habits[habit].name, 'period': habits[habit].period, 'creation_date': habits[habit].creation_date,
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

    subparsers.add_parser('reload', help='reload save file')
    subparsers.add_parser('getAllHabits', help='Returns all stored Habits')
    subparsers.add_parser('save', help='Saves data to file')
    subparsers.add_parser('clear', help='Clear the screen')

    commandFunctionMapping = {
        'loadData': load_from_file,
        'reload': reload,
        'getAllHabits': get_all_habits,
        'addHabit': add_habit,
        'removeHabit': remove_habit,
        'save': save_to_file,
        'clear': clearScreen,
        'addTask': addTask,
        'removeTask': removeTask,
        'checkTask': checkTask,
    }

    while True:
        userInput = input("HabitTracker> ")
        if userInput == 'exit':
            break
        else:
            try:
                args = parser.parse_args(userInput.split())
                if args.command in commandFunctionMapping:
                    function = commandFunctionMapping[args.command]
                    function_args = vars(args)
                    function_args.pop("command")
                    function(**function_args)
                else:
                    parser.print_help()

            except SystemExit:
                pass


if __name__ == '__main__':
    print("### HabitTracker 1.0 ###")
    load_from_file()
    main()
