from abc import ABC, abstractmethod
from base.employee import Employee

class AbstractEmployee(Employee, ABC):
    """
    Абстрактный слой поверх обычного сотрудника.
    Заставляет наследников реализовать бизнес-логику (зарплаты, инфо).
    """
    
    @abstractmethod
    def calculate_salary(self) -> float:
        """Расчет итоговой зарплаты."""
        pass

    @abstractmethod
    def get_info(self) -> str:
        """Полная информация о сотруднике."""
        pass
