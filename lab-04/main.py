from src.employee import Employee

class Main:
    """
    Главный класс приложения. 
    Отвечает за запуск сценариев использования и тестирование.
    """
    
    @staticmethod
    def run_tests():
        print("=== НАЧАЛО ТЕСТИРОВАНИЯ СИСТЕМЫ УЧЕТА ===\n")

        Main.test_valid_creation()
        Main.test_updates()
        Main.test_validation_errors()

        print("\n=== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ===")

    @staticmethod
    def test_valid_creation():
        print("--- Тест 1: Создание корректных сотрудников ---")
        try:
            emp1 = Employee(1, "Алексей Смирнов", "Разработка", 120000)
            emp2 = Employee(2, "Мария Иванова", "Маркетинг", 85000)
            print(f"Успешно создан: {emp1}")
            print(f"Успешно создан: {emp2}")
        except ValueError as e:
            print(f"Ошибка: {e}")
        print()

    @staticmethod
    def test_updates():
        print("--- Тест 2: Обновление данных через сеттеры ---")
        try:
            emp = Employee(3, "Тестовый Сотрудник", "IT", 50000)
            print(f"До изменения: {emp}")
            
            # Изменяем зарплату и отдел
            emp.base_salary = 60000
            emp.department = "DevOps"
            
            print(f"После изменения: {emp}")
            
            # Проверка, что данные действительно изменились в объекте
            if emp.base_salary == 60000 and emp.department == "DevOps":
                print("Результат: Данные успешно обновлены.")
            else:
                print("Результат: Ошибка обновления данных.")
        except ValueError as e:
            print(f"Ошибка: {e}")
        print()

    @staticmethod
    def test_validation_errors():
        print("--- Тест 3: Проверка валидации (Negative Tests) ---")
        
        # Список некорректных данных для теста
        test_cases = [
            # (id, name, dept, salary, Описание теста)
            (-10, "Иван", "IT", 100, "Отрицательный ID"),
            (10, "", "IT", 100, "Пустое имя"),
            (10, "Иван", "IT", -5000, "Отрицательная зарплата"),
            ("ID_STR", "Иван", "IT", 100, "ID не число")
        ]

        for t_id, t_name, t_dept, t_salary, desc in test_cases:
            print(f"Попытка: {desc} -> ", end="")
            try:
                Employee(t_id, t_name, t_dept, t_salary)
                print("ОШИБКА! Исключение не было вызвано.")
            except ValueError as e:
                print(f"УСПЕХ! Поймано исключение: '{e}'")

# Точка входа в программу
if __name__ == "__main__":
    Main.run_tests()
