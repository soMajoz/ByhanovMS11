from factory import EmployeeFactory
from specialists.developer import Developer
from specialists.salesperson import Salesperson

class TestPart2:
    """Тестовый набор для Части 2: Наследование, Фабрика, Полиморфизм."""

    @staticmethod
    def run():
        print("=== ЗАПУСК ТЕСТОВ ЧАСТИ 2 (НАСЛЕДОВАНИЕ И ФАБРИКА) ===")
        TestPart2.test_specialist_logic()
        TestPart2.test_factory_polymorphism()
        print("=== ТЕСТЫ ЧАСТИ 2 ЗАВЕРШЕНЫ ===\n")

    @staticmethod
    def test_specialist_logic():
        print("   [2.1] Тест логики классов-наследников...")
        try:
            # Тест Developer
            dev = Developer(1, "Dev", "IT", 1000, "junior")
            assert dev.calculate_salary() == 1000.0
            dev.seniority_level = "senior" # x2.0
            assert dev.calculate_salary() == 2000.0
            
            # Тест Salesperson
            sales = Salesperson(2, "Sale", "Sales", 1000, 0.1)
            sales.update_sales(5000) # +500
            assert sales.calculate_salary() == 1500.0
            
            print("      -> Логика расчета зарплат работает корректно.")
        except AssertionError:
            print("      -> ОШИБКА: Неверный расчет зарплаты.")
        except Exception as e:
            print(f"      -> ОШИБКА: {e}")

    @staticmethod
    def test_factory_polymorphism():
        print("   [2.2] Тест фабрики и полиморфного вывода...")
        employees = []
        try:
            employees.append(EmployeeFactory.create_employee('manager', 
                id=10, name="Big Boss", department="Mgmt", base_salary=100, bonus=50))
            employees.append(EmployeeFactory.create_employee('developer',
                id=11, name="Code Master", department="IT", base_salary=100, seniority="middle"))
            
            print("      -> Фабрика успешно создала объекты.")
            
            # Просто проверяем, что методы вызываются без ошибок
            print("      -> Проверка вывода get_info():")
            for emp in employees:
                info = emp.get_info()
                if "Тип:" not in info or "Итоговая выплата:" not in info:
                    print("         -> ОШИБКА: get_info вернул некорректный формат.")
                    return
            print("      -> Полиморфизм работает корректно.")
            
        except ValueError as e:
            print(f"      -> ОШИБКА ФАБРИКИ: {e}")
