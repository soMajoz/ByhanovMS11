import json
import os
from typing import List, Optional, Dict
from base.abstract_employee import AbstractEmployee

class Department:
    """Класс, описывающий отдел (коллекцию сотрудников)."""

    def __init__(self, name: str):
        self.name = name
        self.__employees: List[AbstractEmployee] = []

    def add_employee(self, employee: AbstractEmployee) -> None:
        if isinstance(employee, AbstractEmployee):
            self.__employees.append(employee)
        else:
            raise TypeError("Можно добавлять только наследников AbstractEmployee")

    def remove_employee(self, employee_id: int) -> None:
        self.__employees = [e for e in self.__employees if e.id != employee_id]

    def get_employees(self) -> List[AbstractEmployee]:
        return self.__employees

    def calculate_total_salary(self) -> float:
        """Полиморфный расчет общей зарплаты."""
        return sum(self.__employees)

    def get_employee_count(self) -> Dict[str, int]:
        """Возвращает количество сотрудников по типам."""
        counts = {}
        for emp in self.__employees:
            type_name = emp.__class__.__name__
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        for emp in self.__employees:
            if emp.id == employee_id:
                return emp
        return None

    # --- Магические методы ---

    def __len__(self) -> int:
        return len(self.__employees)

    def __getitem__(self, index) -> AbstractEmployee:
        return self.__employees[index]

    def __contains__(self, employee: AbstractEmployee) -> bool:
        return employee in self.__employees

    def __iter__(self):
        return iter(self.__employees)

    def __str__(self):
        return f"Отдел '{self.name}' (Сотрудников: {len(self)})"

    # --- Сериализация ---

    def save_to_file(self, filename: str) -> None:
        """
        Сохраняет сотрудников отдела в JSON файл.
        Автоматически создает папку для файла, если она не существует.
        """
        # Получаем путь к директории из имени файла
        directory = os.path.dirname(filename)
        
        # Если путь содержит директорию и она не существует — создаем её
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"[INFO] Создана директория: {directory}")
            except OSError as e:
                print(f"[ERROR] Не удалось создать директорию {directory}: {e}")
                raise

        data = {
            "department_name": self.name,
            "employees": [emp.to_dict() for emp in self.__employees]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[INFO] Отдел сохранен в файл: {filename}")

    @classmethod
    def load_from_file(cls, filename: str) -> 'Department':
        from factory import EmployeeFactory
        
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл не найден: {filename}")

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        dept = cls(data["department_name"])
        for emp_data in data["employees"]:
            emp_type = emp_data.pop("type")
            try:
                employee = EmployeeFactory.create_employee(emp_type, **emp_data)
                dept.add_employee(employee)
            except ValueError as e:
                print(f"[WARNING] Ошибка загрузки сотрудника: {e}")
        
        return dept
