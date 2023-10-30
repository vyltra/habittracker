# Habit Tracker Project

## Installation Instructions
1. Make sure you have Python 3.9 or higher installed. This project has been tested using Python 3.9.5 and 3.10.7
2. Place all files provided in the repository in the same folder
3. To start the Habit Tracker, open a terminal and navigate to the folder, then run tracker.py by typing `python tracker.py` or `python3 tracker.py` depending on your Python installation

## Save Files and Startup

### Startup
Upon starting the Program, it will automatically look for a save file to load.
The save file is identified by its name. The Program looks for a file called hbtracker_save.json

The Program informs the user about everything that is happening in the terminal.
If a save file is present, its contents will be loaded into memory. If no file can be found, the Program starts up without
data and prints a warning.

### Reload and Saving
Once the data in memory is modified using the commands below, it can be written to the save file using the `save` command.

CAUTION: The Program will overwrite the save file! Any changes made to the file outside the Program will be lost!

While the Program loads the save file on startup automatically, it is also possible to force reload the save by issuing the `reload` command.

CAUTION: Any unsaved changes in memory will be lost!

## Commands and Usage
### Habit and Task Management
In the following commands, <> are used as placeholders. Replace these with your own variables.
- `<habit name>` and `<task name>` are to be replaced with a coherent string. Example: workout, read_a_book
- `<period>` is to be replaced with a number that represents the desired habit period in days. Example: 1 (to create a daily habit), 7 (to create a weekly habit), 5 (to create a habit that occurs every 5 days)

### Commands

- `addHabit <habit name> <period>`            Adds a Habit
- `removeHabit <habit name>`         Removes a Habit and all its data
- `addTask <habit name> <task name>`             Adds a Task to a Habit
- `removeTask <habit name> <task name>`          Removes a Task from a Habit
- `checkTask <habit name> <task name>`           Checks off a Task in a Habit
- `getAllTasks <habit name>`         Returns all Tasks for a Habit
- `analyze <habit name>`             Calculates all streaks for a Habit
- `getMaxStreak <habit name>`        Calculates the maximum streak for a Habit
- `getMaxStreakAll`     Calculates the maximum streak between all Habits
- `getAllHabits`        Returns all stored Habits
- `getHabitsByPeriod`   Returns Lists of Habits sorted by period

### Quality of Life functions
The following commands can be used for debugging, testing, or as a convenience
- `reload`              Reloads the save file
- `save`                Saves data in memory to a save file
- `clear`               Clears the screen

### Getting Help
The list above can also be shown in the Program by typing `help` or `-h` or `--help` in the console.

## Testing
If you would like to run the tests for the Program, make sure you have the Pytest module for Python installed.
If not, run `pip install pytest` in your local terminal.

You can run the tests by typing `pytest test_tracker.py` in your terminal
This project has been developed using Pytest 7.2.2 and Python 3.9.5

## A Note on Testing
If you would like to do some manual testing, you can modify the timestamps in the hbtracker.json file by hand using a text editor. The timestamps are stored as 
strings and converted into datetime objects during runtime. Just make sure to adhere to the Y-m-d H:M:S structure.