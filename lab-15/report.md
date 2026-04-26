# Отчет по лабораторной работе №15

## Часть 1. ETL-пайплайн

Цель части: построить ETL-процесс для анализа продаж интернет-магазина.

В `part1-etl/data/sales.csv` подготовлены исходные данные с нормальными строками, дублем, пропуском и аномалией отрицательного количества. В `etl_pipeline.py` реализованы все этапы:

- `extract()` загружает CSV и логирует количество строк/колонок;
- `transform()` удаляет дубли, заполняет пропуски, приводит типы, удаляет аномалии, считает `total_amount` и `month_year`;
- `aggregate()` считает `total_quantity`, `total_revenue`, `avg_price`, `order_count`;
- `load_to_sqlite()` сохраняет `sales_cleaned` и `sales_aggregated` в SQLite;
- `visualize()` сохраняет графики выручки по категориям, месячной динамики и доли категорий.

Фактический запуск:

```text
Loaded 13 rows, 9 columns
Removed duplicates: 1
Rows after cleaning: 11
Aggregated rows: 3
Data loaded into sales.db
```

Проверка SQLite сохранена в `part1-etl/verification/sqlite_check.txt`.

## Часть 2. Kafka

Цель части: реализовать потоковую передачу событий заказов через Kafka.

В `part2-kafka/docker-compose.yml` описаны Zookeeper, Kafka и Kafka UI. В `producer.py` реализованы подключение к Kafka, генерация заказов и отправка сообщений с ключом покупателя. В `consumer.py` реализована агрегация общего числа заказов, выручки, категорий, городов и последних заказов. В `windowed_consumer.py` добавлен дополнительный consumer с оконной агрегацией.

## Верификация

ETL-пайплайн запущен успешно локально: создан `sales.db`, `logs/etl.log` и PNG-графики в `report/graphs`. Python-код Kafka прошел `python -m compileall`.

После запуска Docker Desktop Kafka runtime-проверка выполнена: Zookeeper, Kafka и Kafka UI подняты через Docker Compose, producer отправил 15 заказов, основной consumer обработал 15 сообщений с общей выручкой `526000.0`, оконный consumer сохранил окно на 15 заказов. Результаты сохранены в `part2-kafka/verification/`, `data/orders_processed.json` и `data/windowed_stats.json`.

