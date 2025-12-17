from base.abstract_employee import AbstractEmployee

class Manager(AbstractEmployee):
    """
    Менеджер. Получает фиксированный бонус к зарплате.
    """
    
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, bonus: float):
        super().__init__(emp_id, name, department, base_salary)
        self.bonus = bonus

    @property
    def bonus(self) -> float:
        return self.__bonus

    @bonus.setter
    def bonus(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Бонус должен быть положительным числом. Получено: {value}")
        self.__bonus = float(value)

    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus

    def get_info(self) -> str:
        return (f"{super().__str__()}\n"
                f"   -> Тип: Manager\n"
                f"   -> Бонус: {self.bonus}\n"
                f"   -> Итоговая выплата: {self.calculate_salary()} руб.")

    def to_dict(self) -> dict:
        """Сериализация данных менеджера."""
        return {
            "type": "manager",
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "base_salary": self.base_salary,
            "bonus": self.bonus
        }
