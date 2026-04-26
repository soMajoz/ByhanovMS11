"""Kafka consumer that aggregates order statistics."""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from kafka import KafkaConsumer


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class OrderStatsConsumer:
    def __init__(self, bootstrap_servers: str = "localhost:9092", topic: str = "orders", group_id: str = "order_stats_group"):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer: KafkaConsumer | None = None
        self.stats = {
            "total_orders": 0,
            "total_revenue": 0.0,
            "orders_by_category": defaultdict(int),
            "orders_by_city": defaultdict(int),
            "recent_orders": [],
            "start_time": datetime.now().isoformat(),
        }

    def connect(self) -> None:
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            consumer_timeout_ms=10000,
            value_deserializer=lambda value: json.loads(value.decode("utf-8")),
            key_deserializer=lambda key: key.decode("utf-8") if key else None,
        )
        logger.info("Connected to Kafka topic %s", self.topic)

    def update_stats(self, order: dict) -> None:
        self.stats["total_orders"] += 1
        self.stats["total_revenue"] += float(order["total_amount"])
        for item in order["items"]:
            self.stats["orders_by_category"][item["category"]] += 1
        self.stats["orders_by_city"][order["customer"]["city"]] += 1
        self.stats["recent_orders"].append(
            {
                "order_id": order["order_id"],
                "customer": order["customer"]["name"],
                "total": order["total_amount"],
                "time": order["timestamp"],
            }
        )
        self.stats["recent_orders"] = self.stats["recent_orders"][-10:]

    def printable_stats(self) -> dict:
        return {
            **self.stats,
            "orders_by_category": dict(self.stats["orders_by_category"]),
            "orders_by_city": dict(self.stats["orders_by_city"]),
        }

    def save_stats(self) -> None:
        (DATA_DIR / "orders_processed.json").write_text(
            json.dumps(self.printable_stats(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def run(self, max_messages: int | None = None) -> None:
        self.connect()
        assert self.consumer is not None
        consumed = 0
        try:
            for message in self.consumer:
                self.update_stats(message.value)
                consumed += 1
                logger.info("Processed order %s", message.value["order_id"])
                if max_messages is not None and consumed >= max_messages:
                    break
        finally:
            self.consumer.close()
            self.save_stats()
            logger.info("Final stats: %s", self.printable_stats())


if __name__ == "__main__":
    OrderStatsConsumer().run(max_messages=15)
