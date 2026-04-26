"""ETL pipeline for internet-shop sales analytics."""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
GRAPH_DIR = BASE_DIR / "report" / "graphs"
LOG_DIR.mkdir(exist_ok=True)
GRAPH_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "etl.log", encoding="utf-8", mode="w"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class SalesETLPipeline:
    """Extract, clean, aggregate, load and visualize sales data."""

    def __init__(self, csv_path: str | Path, db_path: str | Path = "sales.db"):
        self.csv_path = Path(csv_path)
        self.db_path = Path(db_path)
        self.raw_data: pd.DataFrame | None = None
        self.cleaned_data: pd.DataFrame | None = None
        self.aggregated_data: pd.DataFrame | None = None

    def extract(self) -> pd.DataFrame:
        logger.info("EXTRACT started")
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        self.raw_data = pd.read_csv(self.csv_path)
        if self.raw_data.empty:
            raise ValueError("CSV file is empty")

        logger.info("Loaded %s rows, %s columns", len(self.raw_data), len(self.raw_data.columns))
        logger.info("Columns: %s", ", ".join(self.raw_data.columns))
        return self.raw_data

    def transform(self) -> pd.DataFrame:
        logger.info("TRANSFORM started")
        if self.raw_data is None:
            raise RuntimeError("extract() must run before transform()")

        df = self.raw_data.copy()
        before = len(df)
        df = df.drop_duplicates()
        logger.info("Removed duplicates: %s", before - len(df))

        numeric_columns = ["quantity", "price_per_unit"]
        for column in numeric_columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
            df[column] = df[column].fillna(df[column].median())

        text_columns = ["product_name", "category", "customer_name", "customer_city", "payment_method"]
        for column in text_columns:
            df[column] = df[column].fillna("Unknown").replace("", "Unknown")

        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
        df = df.dropna(subset=["order_date"])

        df = df[(df["quantity"] > 0) & (df["price_per_unit"] > 0)]
        df["quantity"] = df["quantity"].astype(int)
        df["total_amount"] = df["quantity"] * df["price_per_unit"]
        df["month_year"] = df["order_date"].dt.to_period("M").astype(str)

        self.cleaned_data = df
        logger.info("Rows after cleaning: %s", len(df))
        return df

    def aggregate(self) -> pd.DataFrame:
        logger.info("AGGREGATE started")
        if self.cleaned_data is None:
            raise RuntimeError("transform() must run before aggregate()")

        self.aggregated_data = (
            self.cleaned_data.groupby(["category", "month_year"], as_index=False)
            .agg(
                total_quantity=("quantity", "sum"),
                total_revenue=("total_amount", "sum"),
                avg_price=("price_per_unit", "mean"),
                order_count=("order_id", "nunique"),
            )
            .sort_values(["month_year", "total_revenue"], ascending=[True, False])
        )
        logger.info("Aggregated rows: %s", len(self.aggregated_data))
        return self.aggregated_data

    def load_to_sqlite(self) -> None:
        logger.info("LOAD started")
        if self.cleaned_data is None or self.aggregated_data is None:
            raise RuntimeError("transform() and aggregate() must run before load_to_sqlite()")

        with sqlite3.connect(self.db_path) as connection:
            self.cleaned_data.to_sql("sales_cleaned", connection, if_exists="replace", index=False)
            self.aggregated_data.to_sql("sales_aggregated", connection, if_exists="replace", index=False)
        logger.info("Data loaded into %s", self.db_path)

    def visualize(self) -> None:
        logger.info("VISUALIZE started")
        if self.cleaned_data is None or self.aggregated_data is None:
            raise RuntimeError("transform() and aggregate() must run before visualize()")

        revenue_by_category = (
            self.cleaned_data.groupby("category", as_index=False)["total_amount"]
            .sum()
            .sort_values("total_amount", ascending=False)
        )
        plt.figure(figsize=(8, 5))
        plt.bar(revenue_by_category["category"], revenue_by_category["total_amount"])
        plt.title("Revenue by category")
        plt.xlabel("Category")
        plt.ylabel("Revenue")
        plt.tight_layout()
        plt.savefig(GRAPH_DIR / "revenue_by_category.png", dpi=140)
        plt.close()

        monthly = self.cleaned_data.groupby("month_year", as_index=False)["total_amount"].sum()
        plt.figure(figsize=(8, 5))
        plt.plot(monthly["month_year"], monthly["total_amount"], marker="o")
        plt.title("Monthly revenue")
        plt.xlabel("Month")
        plt.ylabel("Revenue")
        plt.tight_layout()
        plt.savefig(GRAPH_DIR / "monthly_revenue.png", dpi=140)
        plt.close()

        plt.figure(figsize=(7, 7))
        plt.pie(revenue_by_category["total_amount"], labels=revenue_by_category["category"], autopct="%1.1f%%")
        plt.title("Category share")
        plt.tight_layout()
        plt.savefig(GRAPH_DIR / "category_share.png", dpi=140)
        plt.close()

    def run(self) -> None:
        logger.info("=" * 50)
        logger.info("ETL PIPELINE STARTED")
        logger.info("=" * 50)
        self.extract()
        self.transform()
        self.aggregate()
        self.load_to_sqlite()
        self.visualize()
        logger.info("ETL PIPELINE FINISHED")


if __name__ == "__main__":
    pipeline = SalesETLPipeline(BASE_DIR / "data" / "sales.csv", BASE_DIR / "sales.db")
    pipeline.run()
