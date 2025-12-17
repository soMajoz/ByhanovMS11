from base.employee import Employee

class TestPart1:
    """Тестовый набор для Части 1: Инкапсуляция и валидация."""

    @staticmethod
    def run():
        print("=== ЗАПУСК ТЕСТОВ ЧАСТИ 1 (ИНКАПСУЛЯЦИЯ) ===")
        TestPart1.test_valid_creation()
        TestPart1.test_validation_errors()
        print("=== ТЕСТЫ ЧАСТИ 1 ЗАВЕРШЕНЫ ===\n")

    @staticmethod
    def test_valid_creation():
        print("   [1.1] Тест создания и обновления...")
        try:
            emp = Employee(1, "Тест Юзер", "QA", 50000)
            # Проверка геттеров
            assert emp.name == "Тест Юзер"
            assert emp.base_salary == 50000
            
            # Проверка сеттеров
            emp.base_salary = 60000
            assert emp.base_salary == 60000
            print("      -> Успешно.")
        except AssertionError:
            print("      -> ОШИБКА: Данные не обновились корректно.")
        except ValueError as e:
            print(f"      -> ОШИБКА: {e}")

    @staticmethod
    def test_validation_errors():
        print("   [1.2] Тест валидации (Negative Tests)...")
        errors_caught = 0
        expected_errors = 3

        # Кейс 1: Невалидный ID
        try:
            Employee(-1, "Name", "Dept", 100)
        except ValueError:
            errors_caught += 1

        # Кейс 2: Пустое имя
        try:
            Employee(1, "", "Dept", 100)
        except ValueError:
            errors_caught += 1

        # Кейс 3: Отрицательная зарплата
        try:
            Employee(1, "Name", "Dept", -5000)
        except ValueError:
            errors_caught += 1

        if errors_caught == expected_errors:
            print(f"      -> Успешно перехвачено {errors_caught}/{expected_errors} ошибок.")
        else:
            print(f"      -> ОШИБКА: Ожидалось {expected_errors} ошибок, перехвачено {errors_caught}.")
