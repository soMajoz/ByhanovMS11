"""Kafka producer that generates internet-shop order events."""

from __future__ import annotations

import json
import logging
import random
import time
import uuid
from datetime import datetime

from kafka import KafkaProducer


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class OrderEventProducer:
    def __init__(self, bootstrap_servers: str = "localhost:9092", topic: str = "orders"):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer: KafkaProducer | None = None

    def connect(self) -> None:
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda value: json.dumps(value, ensure_ascii=False).encode("utf-8"),
            key_serializer=lambda key: key.encode("utf-8") if key else None,
        )
        logger.info("Connected to Kafka at %s", self.bootstrap_servers)

    def generate_order(self) -> dict:
        products = [
            {"product_id": 1, "name": "Ноутбук", "price": 75000, "category": "Электроника"},
            {"product_id": 2, "name": "Мышь", "price": 1500, "category": "Электроника"},
            {"product_id": 3, "name": "Книга SQL", "price": 2500, "category": "Книги"},
            {"product_id": 4, "name": "Клавиатура", "price": 5000, "category": "Электроника"},
            {"product_id": 5, "name": "Монитор", "price": 25000, "category": "Электроника"},
            {"product_id": 6, "name": "Книга Python", "price": 3500, "category": "Книги"},
        ]
        customers = [
            {"id": 1, "name": "Анна Смирнова", "city": "Москва"},
            {"id": 2, "name": "Петр Иванов", "city": "Санкт-Петербург"},
            {"id": 3, "name": "Мария Сидорова", "city": "Казань"},
            {"id": 4, "name": "Иван Петров", "city": "Москва"},
            {"id": 5, "name": "Елена Козлова", "city": "Новосибирск"},
        ]
        product = random.choice(products)
        customer = random.choice(customers)
        quantity = random.randint(1, 3)
        return {
            "order_id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().isoformat(),
            "customer": customer,
            "items": [
                {
                    "product_id": product["product_id"],
                    "product_name": product["name"],
                    "category": product["category"],
                    "quantity": quantity,
                    "unit_price": product["price"],
                    "total_price": quantity * product["price"],
                }
            ],
            "total_amount": quantity * product["price"],
            "payment_method": random.choice(["card", "cash", "online"]),
        }

    def send_order(self, order: dict):
        if self.producer is None:
            raise RuntimeError("connect() must run before send_order()")
        key = str(order["customer"]["id"])
        future = self.producer.send(self.topic, key=key, value=order)
        metadata = future.get(timeout=10)
        logger.info("Order %s sent to partition %s offset %s", order["order_id"], metadata.partition, metadata.offset)
        return future

    def run(self, interval_seconds: float = 1.0, max_orders: int = 15) -> None:
        self.connect()
        for _ in range(max_orders):
            self.send_order(self.generate_order())
            time.sleep(interval_seconds)
        assert self.producer is not None
        self.producer.flush()
        self.producer.close()
        logger.info("All orders sent")


if __name__ == "__main__":
    OrderEventProducer().run()

