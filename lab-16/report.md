# Отчет по лабораторной работе №16

## Часть 1. GigaChat

Цель части: применить ИИ-ассистента для генерации кода, рефакторинга, тестирования и документации.

В `part1-gigachat/gigachat_client.py` реализован клиент GigaChat API: получение access token, отправка chat completion запроса, очистка markdown code block и сохранение результата. Секреты берутся только из `.env`, шаблон находится в `.env.example`.

Выполненные артефакты:

- `generated_code.py`: функции `is_prime`, `fibonacci`, `normalize_phone`;
- `bad_code.py`: исходный плохой пример с глобальным состоянием;
- `refactored_code.py`: рефакторинг через `OrderItem` и `OrderBasket`;
- `test_refactored.py`: pytest-тесты для рефакторинга и сгенерированных функций;
- `README_generated.md`: документация проекта;
- `report/analysis.json`: анализ качества кода.

Локальная проверка:

```text
python -m pytest test_refactored.py -v
3 passed
```

Реальная API-проверка `python test_connection.py` требует заполненного `part1-gigachat/.env`.

## Часть 2. Airtable

Цель части: создать CRM-систему управления заказами на low-code платформе Airtable и экспортировать структуру/данные.

В `part2-airtable/airtable_schema.json` описаны таблицы `Customers`, `Products`, `Orders`, `Order Items`, связи, views и форма ввода заказа. В `export_airtable.py` реализован экспорт реальных таблиц Airtable через API в CSV. Секреты `AIRTABLE_TOKEN` и `AIRTABLE_BASE_ID` хранятся только в локальном `.env`.

В `exported_data/` сохранены демонстрационные CSV-выгрузки таблиц, а в `integration/webhook_config.json` описан сценарий уведомления при оплате заказа. Сравнение low-code и традиционной разработки находится в `report/comparison_table.md`.

## Верификация

Python-код `part1-gigachat`, `part2-airtable` прошел `python -m compileall`. Pytest-тесты GigaChat-части прошли. Реальная проверка GigaChat и Airtable API ожидает локальные `.env` с действительными секретами.

