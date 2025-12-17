from base.abstract_employee import AbstractEmployee

class OrdinaryEmployee(AbstractEmployee):
    """
    Реализация штатного сотрудника без бонусов и надбавок.
    """
    def calculate_salary(self) -> float:
        return self.base_salary

    def get_info(self) -> str:
        return (f"{super().__str__()}\n"
                f"   -> Тип: Штатный сотрудник\n"
                f"   -> Итоговая выплата: {self.calculate_salary()} руб.")
