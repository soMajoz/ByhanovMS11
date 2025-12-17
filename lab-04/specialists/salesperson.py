from base.abstract_employee import AbstractEmployee

class Salesperson(AbstractEmployee):
    """
    Продавец. Зарплата состоит из оклада + процента с продаж.
    """

    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, 
                 commission_rate: float, sales_volume: float = 0.0):
        super().__init__(emp_id, name, department, base_salary)
        self.commission_rate = commission_rate
        self.sales_volume = sales_volume

    @property
    def commission_rate(self) -> float:
        return self.__commission_rate

    @commission_rate.setter
    def commission_rate(self, value: float):
        if not isinstance(value, (int, float)):
            raise ValueError("Комиссия должна быть числом.")
        if not (0 <= value <= 1.0):
            raise ValueError(f"Комиссия должна быть в диапазоне от 0.0 до 1.0. Получено: {value}")
        self.__commission_rate = float(value)

    @property
    def sales_volume(self) -> float:
        return self.__sales_volume

    @sales_volume.setter
    def sales_volume(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Объем продаж не может быть отрицательным.")
        self.__sales_volume = float(value)

    def update_sales(self, amount: float) -> None:
        """Добавляет сумму к текущему объему продаж."""
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Сумма добавления продаж должна быть положительной.")
        self.__sales_volume += float(amount)

    def calculate_salary(self) -> float:
        return self.base_salary + (self.sales_volume * self.commission_rate)

    def get_info(self) -> str:
        return (f"{super().__str__()}\n"
                f"   -> Тип: Salesperson\n"
                f"   -> Продажи: {self.sales_volume}\n"
                f"   -> Комиссия: {self.commission_rate * 100}%\n"
                f"   -> Итоговая выплата: {self.calculate_salary()} руб.")
