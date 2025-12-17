import os
from organization.department import Department
from factory import EmployeeFactory
from specialists.developer import Developer
import utils.comparators as comps

class TestPart3:
    @staticmethod
    def run():
        print("=== ЗАПУСК ТЕСТОВ ЧАСТИ 3 (ПОЛИМОРФИЗМ И МАГИЯ) ===")
        TestPart3.test_magic_methods()
        TestPart3.test_department_collection()
        TestPart3.test_sorting_and_iter()
        TestPart3.test_serialization()
        print("=== ТЕСТЫ ЧАСТИ 3 ЗАВЕРШЕНЫ ===\n")

    @staticmethod
    def test_magic_methods():
        print("   [3.1] Магические методы сотрудников...")
        e1 = EmployeeFactory.create_employee('employee', id=1, name="A", department="D", base_salary=100)
        e2 = EmployeeFactory.create_employee('employee', id=2, name="B", department="D", base_salary=200)
        
        # __eq__
        assert e1 != e2
        # __lt__
        assert e1 < e2
        # __add__
        assert (e1 + e2) == 300.0
        
        print("      -> Успешно.")

    @staticmethod
    def test_department_collection():
        print("   [3.2] Коллекция Department...")
        dept = Department("IT Heroes")
        dev = EmployeeFactory.create_employee('developer', id=10, name="Dev", department="IT", base_salary=100, seniority="middle")
        dept.add_employee(dev)
        
        assert len(dept) == 1
        assert dept.calculate_total_salary() == 150.0
        assert dev in dept
        
        print("      -> Успешно.")

    @staticmethod
    def test_sorting_and_iter():
        print("   [3.3] Сортировка и Итерация...")
        dev = Developer(1, "Dev", "IT", 100, "junior", ["Python", "SQL"])
        skills = list(dev) # Итерация
        assert "Python" in skills
        
        e1 = EmployeeFactory.create_employee('employee', id=1, name="Zara", department="A", base_salary=500)
        e2 = EmployeeFactory.create_employee('employee', id=2, name="Anna", department="B", base_salary=100)
        
        # Сортировка по имени через компаратор
        sorted_emps = sorted([e1, e2], key=comps.sort_by_name)
        assert sorted_emps[0].name == "Anna"
        
        print("      -> Успешно.")

    @staticmethod
    def test_serialization():
        print("   [3.4] Сериализация (JSON) в папку docs/json/...")
        
        # 1. Определяем корневую папку проекта
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 2. Формируем путь: project/docs/json/test_dept.json
        target_file = os.path.join(base_dir, "docs", "json", "test_dept.json")
        
        dept = Department("Test Dept")
        dept.add_employee(EmployeeFactory.create_employee('employee', id=1, name="TestUser", department="QA", base_salary=50000))
        dept.add_employee(EmployeeFactory.create_employee('developer', id=2, name="PyDev", department="IT", base_salary=100000, seniority="senior", tech_stack=["Python", "Django"]))
        
        # 3. Сохраняем (файл останется на диске)
        dept.save_to_file(target_file)
        
        if os.path.exists(target_file):
            print(f"      -> Файл успешно создан и сохранен: {target_file}")
        else:
            print("      -> ОШИБКА: Файл не найден после сохранения.")
            return

        # 4. Проверяем загрузку, чтобы убедиться в валидности сохраненного файла
        loaded_dept = Department.load_from_file(target_file)
        assert len(loaded_dept) == 2
        assert loaded_dept.name == "Test Dept"
        
        print("      -> Валидация загрузки прошла успешно.")
