from base.abstract_employee import AbstractEmployee
from specialists.ordinary_employee import OrdinaryEmployee
from specialists.manager import Manager
from specialists.developer import Developer
from specialists.salesperson import Salesperson

class EmployeeFactory:
    """
    Фабрика для создания сотрудников различных типов.
    Инкапсулирует логику выбора конкретного класса на основе строкового типа.
    """

    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        """
        Создает и возвращает объект сотрудника.

        :param emp_type: Тип сотрудника ('employee', 'manager', 'developer', 'salesperson').
        :param kwargs: Именованные аргументы для конструктора.
                       Обязательные: id, name, department, base_salary.
                       Специфические: bonus, seniority, tech_stack, commission, sales_volume.
        :return: Экземпляр класса, наследующего AbstractEmployee.
        :raises ValueError: Если отсутствуют обязательные поля или передан неизвестный тип.
        """
        emp_type = emp_type.lower().strip()
        
        # 1. Проверка наличия обязательных полей для любого сотрудника
        required_fields = ['id', 'name', 'department', 'base_salary']
        missing_fields = [field for field in required_fields if field not in kwargs]
        
        if missing_fields:
            raise ValueError(f"Ошибка создания {emp_type}: отсутствуют обязательные поля {missing_fields}")

        # Формируем базовый словарь аргументов, чтобы не дублировать код
        base_args = {
            'emp_id': kwargs['id'], 
            'name': kwargs['name'], 
            'department': kwargs['department'], 
            'base_salary': kwargs['base_salary']
        }

        # 2. Логика выбора класса
        if emp_type == 'employee':
            # Для типа 'employee' возвращаем OrdinaryEmployee, 
            # который реализует абстрактные методы calculate_salary и get_info
            return OrdinaryEmployee(**base_args)
        
        elif emp_type == 'manager':
            # Требуется 'bonus' (по умолчанию 0.0)
            bonus = kwargs.get('bonus', 0.0)
            return Manager(**base_args, bonus=bonus)
        
        elif emp_type == 'developer':
            # Требуется 'seniority' (по умолчанию 'junior') и 'tech_stack' (по умолчанию [])
            seniority = kwargs.get('seniority', 'junior')
            tech_stack = kwargs.get('tech_stack', [])
            return Developer(**base_args, seniority_level=seniority, tech_stack=tech_stack)
        
        elif emp_type == 'salesperson':
            # Требуется 'commission' (по умолчанию 0.0) и 'sales_volume' (по умолчанию 0.0)
            commission = kwargs.get('commission', 0.0)
            sales_volume = kwargs.get('sales_volume', 0.0)
            return Salesperson(**base_args, commission_rate=commission, sales_volume=sales_volume)
        
        else:
            raise ValueError(f"Неизвестный тип сотрудника: '{emp_type}'. "
                             f"Доступные типы: employee, manager, developer, salesperson.")
