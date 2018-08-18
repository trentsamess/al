import random
from collections import deque
import department as d
import project as p


class Company:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.dept_count = random.randint(2, 6)
        self.empl_counts = [random.randint(3, 10) for _ in range(self.dept_count)]
        self.employees = [d.Specialist() for _ in range(sum(self.empl_counts))] + [d.Head() for _ in range(self.dept_count)]
        self.software_count = len(self.employees)
        self.hardware_count = len(self.employees)
        self.software = [d.Software() for _ in range(self.software_count)]
        self.hardware = [d.Hardware() for _ in range(self.hardware_count)]
        self.projects = []

        empl_queue = deque(self.employees)
        soft_queue = deque(self.software)
        hw_queue = deque(self.hardware)

        self.depts = {
            d.DepartmentType(i + 1): self._create_department(d.DepartmentType(i + 1),
                                                             count, count, count,
                                                             empl_queue, soft_queue, hw_queue)
            for i, count in enumerate(self.empl_counts)}

    def _create_department(self, dept_type, spec_cnt, soft_cnt, hardw_cnt, employees, softwares, hardwares):
        dep_employees = [employees.popleft() for _ in range(spec_cnt)]
        dep_softwares = [softwares.popleft() for _ in range(soft_cnt)]
        dep_hardwares = [hardwares.popleft() for _ in range(hardw_cnt)]
        return d.Department(dept_type, dep_employees, dep_softwares, dep_hardwares)

    def create_project_for_customer(self, name_project, customer):
        prj = p.Project(name_project, self, customer)
        self.projects.append(prj)
        return prj
