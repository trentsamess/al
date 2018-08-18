import random
from collections import deque, defaultdict
from enum import Enum, auto


class TaskStatus(Enum):
    Open = auto()
    InProgress = auto()
    InDeployment = auto()
    Resolved = auto()


class Task:
    def __init__(self, name, dept_type, estimate, status=TaskStatus.Open):
        self.name = name
        self.dept_type = dept_type
        self.estimate = estimate
        self.status = status


class ProjectStatus(Enum):
    New = auto()
    Start = auto()
    InProgress = auto()
    Completed = auto()


class Project:
    def __init__(self, name, company, customer, status=ProjectStatus.New):
        self.name = name
        self.company = company
        self.customer = customer
        self.status = status
        # self.dept_types = list(DepartmentType)
        self.dept_types = list(self.company.depts)
        self.tasks = [Task("Name", random.choice(self.dept_types), random.randint(1, 30))
                      for _ in range(random.randint(2, 10))]
        self.count_tasks = len(self.tasks)
        self.tasks_by_dept_type = defaultdict(list)
        self.spec_by_dept_type = defaultdict(list)
        self.count_spec_by_dept_type = defaultdict(int)
        self.count_spec = 0
        self.assigned_tasks = defaultdict(list)
        self.tasks_by_status = defaultdict(list)
        self.count_resolved_tasks = 0
        self.free_specialists = list()

        for task in self.tasks:
            self.tasks_by_dept_type[task.dept_type].append(task)

        self.estimate_by_dept_type = defaultdict(int)
        for dept_type in self.tasks_by_dept_type:
            # print(task)
            for task in self.tasks_by_dept_type[dept_type]:
                self.estimate_by_dept_type[dept_type] += task.estimate
                # print(task.estimate)

    def start(self):
        print("--Project specialists--")
        self._create_team()
        for count in self.count_spec_by_dept_type.values():
            self.count_spec += count
        print("Total count of specialists for this project: ", self.count_spec)

        if self.count_spec > 0:
            print("--Project started--")
            print("Count of tasks: ", self.count_tasks)
            self.status = ProjectStatus.Start
        else:
            print("Need more gold...")

    def _create_team(self):
        for dept_type in self.estimate_by_dept_type:
            count_specialist, specialists = self.company.depts[dept_type]\
                                            .get_specialists(
                                                self.estimate_by_dept_type[dept_type],
                                                self.customer.importance,
                                                self.customer.expected_duration)

            self.spec_by_dept_type[dept_type] = specialists
            self.count_spec_by_dept_type[dept_type] = count_specialist

    def assign_tasks(self):
        self.status = ProjectStatus.InProgress
        for dept_type in self.tasks_by_dept_type:
            spec_free = self.spec_by_dept_type[dept_type] # free_specs
            tasks_sort_by_est = sorted(self.tasks_by_dept_type[dept_type], key=lambda task: task.estimate, reverse=True)
            for task in tasks_sort_by_est:
                if spec_free:
                    if task.estimate <= 10:
                        self.assigned_tasks[task].append(spec_free.pop())
                    elif task.estimate > 10:
                        self.assigned_tasks[task].append(spec_free.pop())
                        if spec_free:
                            self.assigned_tasks[task].append(spec_free.pop())
                        else:
                            continue
                else:
                    self.assigned_tasks[task] = []

    def execute(self):
        # self._sort_tasks_by_status(self.assigned_tasks)
        # self.current_task = random.choice(self.assigned_tasks.keys())
        for task in self.assigned_tasks:
            while task.status != TaskStatus.Resolved:
                if self.assigned_tasks[task]:
                    if task.status == TaskStatus.Open:
                        task.status = TaskStatus.InProgress
                    elif task.status == TaskStatus.InProgress:
                        task.status = TaskStatus.InDeployment
                    elif task.status == TaskStatus.InDeployment:
                        task.status = TaskStatus.Resolved
                        self.free_specialists.extend(self.assigned_tasks[task])
                else:
                    if self.free_specialists:
                        self.assigned_tasks[task].append(self.free_specialists.pop())

    def check_status(self):
        for task in self.assigned_tasks:
            if task.status == TaskStatus.Resolved:
                self.count_resolved_tasks += 1
        if self.count_tasks == self.count_resolved_tasks:
            print("--Project ended!--")
            print("Count of resolved tasks:", self.count_resolved_tasks)
            self._end()
        else:
            print("--Project in progress--")
            print("Count of resolved tasks:", self.count_resolved_tasks)

    def _end(self):
        self.status = ProjectStatus.Completed
        for dept_type in self.spec_by_dept_type:
            self.company.depts[dept_type].return_specialists(self.spec_by_dept_type[dept_type])
            # print(self.spec_by_dept_type[dept_type])