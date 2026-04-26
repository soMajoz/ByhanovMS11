# Kafka verification

Planned command:

```powershell
docker compose up -d
python consumer.py
python producer.py
python windowed_consumer.py
```

Actual local environment status on 2026-04-26:

- Python files passed `python -m compileall`.
- Docker Desktop daemon was not running, so Kafka/Zookeeper/Kafka UI containers could not be started.
- Kafka runtime verification should be repeated after Docker Desktop is running.

