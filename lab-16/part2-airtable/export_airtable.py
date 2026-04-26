"""Export Airtable CRM tables to CSV files using real API credentials."""

from __future__ import annotations

import csv
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "exported_data"
TABLES = ["Customers", "Products", "Orders", "Order Items"]


def load_config() -> tuple[str, str]:
    load_dotenv(BASE_DIR / ".env")
    token = os.getenv("AIRTABLE_TOKEN", "").strip()
    base_id = os.getenv("AIRTABLE_BASE_ID", "").strip()
    if not token or not base_id:
        raise RuntimeError("AIRTABLE_TOKEN and AIRTABLE_BASE_ID must be set in .env")
    return token, base_id


def fetch_table(token: str, base_id: str, table_name: str) -> list[dict]:
    records: list[dict] = []
    offset: str | None = None
    headers = {"Authorization": f"Bearer {token}"}
    while True:
        params = {"pageSize": 100}
        if offset:
            params["offset"] = offset
        response = requests.get(
            f"https://api.airtable.com/v0/{base_id}/{table_name}",
            headers=headers,
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        records.extend(payload.get("records", []))
        offset = payload.get("offset")
        if not offset:
            return records


def write_csv(table_name: str, records: list[dict]) -> Path:
    EXPORT_DIR.mkdir(exist_ok=True)
    fields = sorted({key for record in records for key in record.get("fields", {}).keys()})
    path = EXPORT_DIR / f"{table_name.replace(' ', '_')}.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", *fields])
        writer.writeheader()
        for record in records:
            row = {"id": record["id"], **record.get("fields", {})}
            writer.writerow(row)
    return path


def main() -> None:
    token, base_id = load_config()
    for table_name in TABLES:
        records = fetch_table(token, base_id, table_name)
        path = write_csv(table_name, records)
        print(f"Exported {len(records)} records from {table_name} to {path}")


if __name__ == "__main__":
    main()

