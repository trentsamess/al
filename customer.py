from enum import Enum, auto


class Customer:
    def __init__(self, name, importance, budget, expected_duration):
        self.name = name
        self.importance = importance
        self.budget = budget
        self.expected_duration = expected_duration


class Importance(Enum):
    High = auto()
    Middle = auto()
    Low = auto()
