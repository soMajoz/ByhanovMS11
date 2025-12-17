"""
Функции-компараторы (key functions) для сортировки сотрудников.
"""

def sort_by_name(employee):
    return employee.name

def sort_by_salary(employee):
    return employee.calculate_salary()

def sort_by_dept_then_name(employee):
    # Возвращаем кортеж, Python сортирует сначала по первому элементу, потом по второму
    return (employee.department, employee.name)
