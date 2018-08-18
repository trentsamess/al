from collections import deque
from enum import Enum, auto
from customer import Importance


class Department:
    def __init__(self, dept_type, employees, softwares, hardwares):
        self.dept_type = dept_type
        self.employees = employees
        self.softwares = softwares
        self.hardwares = hardwares
        self.free_employees = deque(employees)
        self.busy_employees = deque([])

    def get_specialists(self, estimate, cust_importance, cust_exp_dur):
        count_spec = 0
        if cust_importance == Importance.High.value:  # not value
            if 1 <= estimate < 6:
                count_spec += 1
            elif 6 <= estimate < 21:
                count_spec += 2
            else:
                count_spec += 3

            if 1 <= cust_exp_dur < 7:
                count_spec += 1
            else:
                count_spec += 2

        if cust_importance == Importance.Middle.value:
            if 1 <= estimate < 21:
                count_spec += 1
            else:
                count_spec += 2

            if 1 <= cust_exp_dur < 13:
                count_spec += 1
            else:
                count_spec += 2

        if cust_importance == Importance.Low.value:
            if estimate > 30:
                count_spec += 1
            if cust_exp_dur < 7:
                count_spec += 1

        count_spec_return, spec_for_project = self._select_specialists(count_spec)
        return count_spec_return, spec_for_project

    def _select_specialists(self, count_spec):
        count_spec_return = 0
        spec_for_project = deque()
        print(self.dept_type)
        print("Requested: ", count_spec)
        while count_spec > 0:
            if self.free_employees:
                spec_for_project.append(self.free_employees[0])
                self.busy_employees.append(self.free_employees.popleft())
                count_spec -= 1
                count_spec_return += 1
        print("Returned: ", count_spec_return)
        return count_spec_return, spec_for_project

    def return_specialists(self, spec):
        if spec:
            for sp in spec:
                self.free_employees.append(sp)
                self.busy_employees.remove(sp)


class DepartmentType(Enum):
    Development = auto()
    Testing = auto()
    Monitoring = auto()
    Operation = auto()
    Management = auto()
    Administration = auto()


class Software:
    pass


class Hardware:
    pass


class Employee:
    pass


class Specialist(Employee):
    pass


class Head(Employee):
    pass


class Position:
    pass