# GigaChat Developer Automation

Проект демонстрирует применение GigaChat в задачах разработчика: генерация функций, рефакторинг плохого кода, создание тестов и документации.

## Запуск

1. Скопировать `.env.example` в `.env` и заполнить `GIGACHAT_CREDENTIALS`.
2. Установить зависимости: `pip install -r requirements.txt`.
3. Проверить API: `python test_connection.py`.
4. Запустить генерацию: `python gigachat_client.py`.
5. Проверить код: `pytest -v`.

## Проверенные функции

- `is_prime(number)` проверяет простоту числа.
- `fibonacci(length)` возвращает последовательность Фибоначчи.
- `normalize_phone(phone)` нормализует российский телефонный номер.

