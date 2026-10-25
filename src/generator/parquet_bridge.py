"""Bridge to write records via Spark Parquet writer from outside the orchestrator.

This module enables components outside the orchestrator to benefit from the Spark-backed
Parquet writer when available, while providing a clean fallback path when Spark is absent.
"""
from typing import Any

from .spark_generation import to_parquet_from_records


def write_records_parquet_or_fallback(records: list[dict[str, Any]], path: str, partitions: list[str] | None = None) -> str:
    return to_parquet_from_records(records, path, partitions)
