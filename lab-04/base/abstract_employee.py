from abc import ABC, abstractmethod
from base.employee import Employee

class AbstractEmployee(Employee, ABC):
    """
    Абстрактный слой с поддержкой магических методов и интерфейса сериализации.
    """
    
    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Сериализация сотрудника в словарь."""
        pass

    # --- Магические методы (3.2) ---

    def __eq__(self, other):
        """Сравнение сотрудников по ID."""
        if isinstance(other, AbstractEmployee):
            return self.id == other.id
        return False

    def __lt__(self, other):
        """Сравнение по зарплате (для сортировки)."""
        if isinstance(other, AbstractEmployee):
            return self.calculate_salary() < other.calculate_salary()
        return NotImplemented

    def __add__(self, other):
        """
        Сложение:
        Employee + Employee = сумма зарплат (float)
        Employee + int/float = зарплата + число (float)
        """
        if isinstance(other, AbstractEmployee):
            return self.calculate_salary() + other.calculate_salary()
        elif isinstance(other, (int, float)):
            return self.calculate_salary() + other
        return NotImplemented

    def __radd__(self, other):
        """
        Поддержка sum([emp1, emp2]).
        sum() начинает с 0, поэтому будет вызов: 0 + emp1.
        """
        if isinstance(other, (int, float)):
            return other + self.calculate_salary()
        return NotImplemented
