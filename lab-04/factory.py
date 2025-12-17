from base.abstract_employee import AbstractEmployee
from specialists.ordinary_employee import OrdinaryEmployee
from specialists.manager import Manager
from specialists.developer import Developer
from specialists.salesperson import Salesperson

class EmployeeFactory:
    """
    Фабрика для создания объектов сотрудников.
    Инкапсулирует логику выбора конкретного класса на основе строки типа.
    """

    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        """
        Создает сотрудника заданного типа.
        
        :param emp_type: Тип ('manager', 'developer', 'salesperson', 'employee')
        :param kwargs: Аргументы конструктора (id, name, department, base_salary, ...)
        """
        emp_type = emp_type.lower().strip()
        
        # Базовая валидация обязательных полей
        required_fields = ['id', 'name', 'department', 'base_salary']
        for field in required_fields:
            if field not in kwargs:
                # В to_dict ключи могут быть строками, поэтому kwargs['id'] корректно
                # Но если вызываем руками, нужно следить за названиями
                raise ValueError(f"Отсутствует обязательное поле для создания сотрудника: {field}")

        base_args = {
            'emp_id': kwargs['id'], 
            'name': kwargs['name'], 
            'department': kwargs['department'], 
            'base_salary': kwargs['base_salary']
        }

        if emp_type == 'employee':
            return OrdinaryEmployee(**base_args)
        
        elif emp_type == 'manager':
            # Ожидаем 'bonus' в kwargs
            return Manager(**base_args, bonus=kwargs.get('bonus', 0.0))
        
        elif emp_type == 'developer':
            # Ожидаем 'seniority' и 'tech_stack'
            # При загрузке из JSON ключи будут совпадать с этими именами
            return Developer(**base_args, 
                             seniority_level=kwargs.get('seniority', 'junior'),
                             tech_stack=kwargs.get('tech_stack', []))
        
        elif emp_type == 'salesperson':
            # Ожидаем 'commission' и 'sales_volume'
            return Salesperson(**base_args, 
                               commission_rate=kwargs.get('commission', 0.0),
                               sales_volume=kwargs.get('sales_volume', 0.0))
        
        else:
            raise ValueError(f"Неизвестный тип сотрудника: {emp_type}")
