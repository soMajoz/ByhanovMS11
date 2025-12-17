from base.abstract_employee import AbstractEmployee

class Developer(AbstractEmployee):
    """
    Разработчик. Зарплата рассчитывается с учетом коэффициента уровня (Seniority).
    """
    
    LEVEL_MULTIPLIERS = {
        "junior": 1.0,
        "middle": 1.5,
        "senior": 2.0
    }

    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, 
                 seniority_level: str, tech_stack: list[str] = None):
        super().__init__(emp_id, name, department, base_salary)
        self.seniority_level = seniority_level
        # Если список не передан, создаем пустой
        self.__tech_stack = tech_stack if tech_stack is not None else []

    @property
    def seniority_level(self) -> str:
        return self.__seniority_level

    @seniority_level.setter
    def seniority_level(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Уровень должен быть строкой.")
        
        normalized_value = value.lower().strip()
        if normalized_value not in self.LEVEL_MULTIPLIERS:
            valid_levels = list(self.LEVEL_MULTIPLIERS.keys())
            raise ValueError(f"Недопустимый уровень: '{value}'. Доступны: {valid_levels}")
        
        self.__seniority_level = normalized_value

    def add_skill(self, new_skill: str) -> None:
        """Добавляет новый навык в стек технологий."""
        if new_skill and isinstance(new_skill, str):
            if new_skill not in self.__tech_stack:
                self.__tech_stack.append(new_skill)

    def calculate_salary(self) -> float:
        multiplier = self.LEVEL_MULTIPLIERS[self.seniority_level]
        return self.base_salary * multiplier

    def get_info(self) -> str:
        stack_str = ", ".join(self.__tech_stack)
        return (f"{super().__str__()}\n"
                f"   -> Тип: Developer ({self.seniority_level.title()})\n"
                f"   -> Стек: [{stack_str}]\n"
                f"   -> Итоговая выплата: {self.calculate_salary()} руб.")
