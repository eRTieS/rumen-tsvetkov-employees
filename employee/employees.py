"""
Task: Create an application that identifies the pair of employees who have worked
together on common projects for the longest period of time.

Classes:
    - EmployeeData: Contains data for employee (row from the csv file)
    - EmployeePair: Contains pair between employees
    - EmployeesController: Employees controller
    - EmployeesExecutor: Employees executor
"""

import sys

from csv import DictReader
from datetime import datetime, timedelta
from typing import Union

from employee.validate import ValidationError, Validator


class EmployeeData:
    """
    Contains data for employee (row from the csv)
    """

    EMPLOYEE_MAP = {
        'EmpID': 'emp_id',
        'ProjectID': 'project_id',
        'DateFrom': 'date_from',
        'DateTo': 'date_to'
    }

    def __init__(self, emp_id: int, project_id: int, date_from: datetime, date_to: Union[datetime, None]):
        self.emp_id: int = emp_id
        self.project_id: int = project_id
        self.date_from: datetime = date_from
        self.date_to: Union[datetime, None] = date_to

        if self.date_to is None:
            self.date_to = datetime.now()

        self.days: int = (self.date_to - self.date_from).days

    @classmethod
    def from_csv_record(cls, csv_record):
        """
        Transform a record from csv to object.

        :param csv_record: A record from csv file
        :type csv_record: dict
        :return:
        """
        mapped: dict = cls.map_employee_data(csv_record)

        return cls(*EmployeeData.validate(**mapped))

    @staticmethod
    def validate(emp_id, project_id: str, date_from: str, date_to: str) -> None:
        """
        Validate CSV record

        :param emp_id: employee ID
        :param project_id: project ID
        :param date_from: start date
        :param date_to: end date
        :return: Nothing
        """
        validator = Validator()

        return validator.validate(emp_id, project_id, date_from, date_to)

    @staticmethod
    def map_employee_data(employee_data: dict) -> dict:
        return {v: employee_data[k] for k, v in EmployeeData.EMPLOYEE_MAP.items()}

    def __str__(self):
        return f'{self.emp_id} | {self.project_id} | {self.date_from} | {self.date_to}'

    def __repr__(self):
        return self.__str__()

    def __dict__(self) -> dict:
        return {
            'emp_id': self.emp_id,
            'project_id': self.project_id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'days': self.days
        }


class EmployeePair:
    """
    Represents pair between employees who work on the same project.
    """

    def __init__(self, employee_1: EmployeeData, employee_2: EmployeeData):
        self.employee_1: EmployeeData = employee_1
        self.employee_2: EmployeeData = employee_2
        self.days: int = self.pair_days()

    def pair_days(self) -> int:
        """
        calculating the days employees worked together

        :return: Number of days employees worked together
        """
        if self.employee_1.date_to < self.employee_2.date_from:
            days = timedelta()
        elif self.employee_1.date_to <= self.employee_2.date_to:
            days: timedelta = self.employee_1.date_to - self.employee_2.date_from
        else:
            days: timedelta = self.employee_2.date_to - self.employee_2.date_from

        return days.days

    def __lt__(self, other):
        return self.days < other.days

    def __le__(self, other):
        return self.days <= other.days

    def __gt__(self, other):
        return self.days > other.days

    def __ge__(self, other):
        return self.days >= other.days

    def __eq__(self, other):
        return self.days == other.days

    def __ne__(self, other):
        return self.days != other.days

    def __hash__(self):
        return hash(f"{self.employee_1} {self.employee_2} {self.days}")

    def __str__(self):
        return f"{self.employee_1.emp_id}, {self.employee_2.emp_id}, {self.days}"

    def __repr__(self):
        return self.__str__()

    def __dict__(self):
        return {
            'employee_1': self.employee_1,
            'employee_2': self.employee_2,
            'days': self.days
        }


class EmployeesController:
    """
    Controller
    """

    def __init__(self):

        self.employees = []

    def add_employee_data(self, employee_data: dict) -> None:
        """
        Add CSV record of employee
        :param employee_data: CSV record
        :return: Nothing
        """
        try:
            self.employees.append(EmployeeData.from_csv_record(employee_data))
        except ValidationError:
            pass

    def get_employees_by_project(self) -> dict:
        """
        Return employees by project ID
        :return: Dict
        """
        result = {}

        for employee_data in self.employees:
            result.setdefault(employee_data.project_id, []).append(employee_data)

        return result

    def get_projects_by_employee(self, employee_id: int) -> list:
        """
        Return projects by employee ID
        :param employee_id: Employee ID
        :return: List ot EmployeeData
        """
        result = []

        for employee in self.employees:
            if employee.emp_id == int(employee_id):
                result.append(employee)

        return result

    def get_employees_by_project_id(self, project_id: int) -> list:
        """
        Return employees by project ID
        :param project_id: Project ID
        :return: List ot EmployeeData
        """
        result = []

        for employee in self.employees:
            if employee.project_id == int(project_id):
                result.append(employee)

        return result

    @staticmethod
    def longest_employee_pair(employees) -> EmployeePair:
        """
        Find the longest period of pair working of employees
        :param employees: List of employees
        :return: EmployeePair instance
        """
        longest_employees_pair = None

        for i in range(0, len(employees) - 1):
            for j in range(i + 1, len(employees)):
                employee = employees[i]
                next_employee = employees[j]

                employee_pair = EmployeePair(employee, next_employee)

                if longest_employees_pair is None or longest_employees_pair < employee_pair:
                    longest_employees_pair = employee_pair

        return longest_employees_pair

    def find_longest_pair_per_project(self) -> dict:
        """
        Return a list with the longest employee pairs by project
        :return: dict with employee pairs by project
        """
        result = {}

        for project_id, employees in self.get_employees_by_project().items():
            employees = sorted(employees, key=lambda emp: (emp.date_from, emp.days))

            longest_employees_pair = self.longest_employee_pair(employees)

            result[project_id] = longest_employees_pair

        return result

    def find_longest_pair(self) -> EmployeePair:
        """
        Return the longest employee pair for all projects
        :return: EmployeePair instance
        """
        longest_employee_pair = None

        for project_id, employees in self.get_employees_by_project().items():
            employees = sorted(employees, key=lambda emp: (emp.date_from, emp.days))

            project_longest_employees_pair = self.longest_employee_pair(employees)

            if longest_employee_pair is None or longest_employee_pair < project_longest_employees_pair:
                longest_employee_pair = project_longest_employees_pair

        return longest_employee_pair


class EmployeesExecutor:

    def __init__(self):
        self.employees_controller = None

    def read_employees_data(self, file_name: str):
        self.employees_controller = EmployeesController()

        with open(file_name, 'r') as csvfile:
            for row in DictReader(csvfile):
                row: dict
                self.employees_controller.add_employee_data(row)

    def __call__(self, file_name: str):
        self.read_employees_data(file_name)


if __name__ == '__main__':
    employees_executor = EmployeesExecutor()

    if len(sys.argv) == 1:
        filename = input('Enter filename: ')
    else:
        filename = sys.argv[1]

    if not filename:
        filename = 'input.csv'

    employees_executor(filename)

    longest_pair = employees_executor.employees_controller.find_longest_pair()
    print(f"Longest pair: {longest_pair}")

    longest_pairs_per_project = employees_executor.employees_controller.find_longest_pair_per_project()

    for pair, data in longest_pairs_per_project.items():
        print(pair, data)
