class Employee:
    """
    Класс сотрудника, описывающий сущность предметной области.
    Содержит приватные данные и методы доступа к ним.
    """
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float):
        self.id = emp_id            # Использует сеттер для валидации
        self.name = name            # Использует сеттер для валидации
        self.department = department
        self.base_salary = base_salary

    # --- ID (Геттер и Сеттер) ---
    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"ID должен быть положительным целым числом. Получено: {value}")
        self.__id = value

    # --- Name (Геттер и Сеттер) ---
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя сотрудника не может быть пустой строкой.")
        self.__name = value.strip()

    # --- Department (Геттер и Сеттер) ---
    @property
    def department(self) -> str:
        return self.__department

    @department.setter
    def department(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Название отдела должно быть строкой.")
        self.__department = value.strip()

    # --- Base Salary (Геттер и Сеттер) ---
    @property
    def base_salary(self) -> float:
        return self.__base_salary

    @base_salary.setter
    def base_salary(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Базовая зарплата должна быть положительным числом. Получено: {value}")
        self.__base_salary = float(value)

    def __str__(self):
        return (f"Сотрудник [id: {self.__id}, имя: {self.__name}, "
                f"отдел: {self.__department}, зарплата: {self.__base_salary}]")
