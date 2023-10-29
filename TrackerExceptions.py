# custom exceptions for clarity
class HabitTypeError(Exception):
    pass


class ElementNotFound(Exception):
    pass


class ElementAlreadyExists(Exception):
    pass


class IncompleteHabit(Exception):
    pass
