"""Additional Kafka consumer that groups orders into short processing windows."""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

from kafka import KafkaConsumer


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class WindowedOrderConsumer:
    def __init__(
        self,
        bootstrap_servers: str = "localhost:9092",
        topic: str = "orders",
        window_seconds: int = 30,
        group_id: str = "order_window_group",
    ):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.window_seconds = window_seconds
        self.group_id = group_id
        self.consumer: KafkaConsumer | None = None
        self.windows: list[dict] = []

    def connect(self) -> None:
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            consumer_timeout_ms=10000,
            value_deserializer=lambda value: json.loads(value.decode("utf-8")),
        )

    def run(self, max_messages: int | None = 15) -> None:
        self.connect()
        assert self.consumer is not None
        window_start = datetime.now()
        current = {"orders": 0, "revenue": 0.0, "categories": defaultdict(int)}
        consumed = 0

        try:
            for message in self.consumer:
                order = message.value
                now = datetime.now()
                if now - window_start >= timedelta(seconds=self.window_seconds):
                    self.windows.append(self._snapshot(window_start, now, current))
                    window_start = now
                    current = {"orders": 0, "revenue": 0.0, "categories": defaultdict(int)}

                current["orders"] += 1
                current["revenue"] += float(order["total_amount"])
                for item in order["items"]:
                    current["categories"][item["category"]] += item["quantity"]

                consumed += 1
                if max_messages is not None and consumed >= max_messages:
                    break
        finally:
            self.windows.append(self._snapshot(window_start, datetime.now(), current))
            self.consumer.close()
            (DATA_DIR / "windowed_stats.json").write_text(
                json.dumps(self.windows, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            logger.info("Saved %s windows", len(self.windows))

    @staticmethod
    def _snapshot(start: datetime, end: datetime, data: dict) -> dict:
        return {
            "window_start": start.isoformat(),
            "window_end": end.isoformat(),
            "orders": data["orders"],
            "revenue": data["revenue"],
            "categories": dict(data["categories"]),
        }


if __name__ == "__main__":
    WindowedOrderConsumer().run()
