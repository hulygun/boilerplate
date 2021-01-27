#ToDo: Documentation
from typing import Any


class Next:
    step = None

    def __init__(self, step: Any = None):
        self.step = step


class Success(Next):
    """implement Next class"""


class Failure(Next):
    reason = None

    def __init__(self, reason: Any, step: Any = None):
        super().__init__(step)
        self.reason = reason


class Result:
    step = False
    def __init__(self, value: Any = None):
        self.value = value
