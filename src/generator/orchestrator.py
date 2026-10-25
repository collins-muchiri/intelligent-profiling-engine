"""Orchestrator to generate synthetic data according to a config.

Hardened:
- Unknown ``region_code`` now raises a clear ``KeyError`` instead of
  silently returning ``None`` (which previously caused a confusing
  ``TypeError: 'NoneType' object is not subscriptable``).
- Domains are read from ``config['domains']`` (no longer confused with
  regions because the YAML structure was fixed).
"""
from __future__ import annotations

import json
from typing import Any, Protocol

import numpy as np

from .config import ConfigLoader
from .domains import (
    FinanceDomainGenerator,
    NGODomainGenerator,
    TelecomDomainGenerator,
    TrafficDomainGenerator,
)


class DomainGenerator(Protocol):
    """Structural type for per-domain record generators (no shared base class)."""

    def generate_record(self, region: str, country: str, seed: int = 0) -> dict[str, Any]: ...


class SyntheticDataOrchestrator:
    def __init__(self, config_path: str):
        self.config = ConfigLoader(config_path).config
        self.regions: dict[str, dict[str, Any]] = self.config.get("regions", {}) or {}
        self.domains_cfg: dict[str, Any] = self.config.get("domains", {}) or {}
        self.domain_generators: dict[str, DomainGenerator] = {
            "finance": FinanceDomainGenerator(),
            "ngo": NGODomainGenerator(),
            "telecom": TelecomDomainGenerator(),
            "traffic": TrafficDomainGenerator(),
        }
        self.global_seed = self.config.get("seed", 42)
        # Instance RNG (was: random.seed() mutating GLOBAL state; bandit B311).
        # Deterministic per orchestrator: same seed -> same record stream.
        self._rng = np.random.default_rng(self.global_seed)

    def get_region_data(self, region_code: str) -> dict[str, Any]:
        if region_code not in self.regions:
            raise KeyError(
                f"Unknown region code '{region_code}'. "
                f"Known regions: {list(self.regions.keys())}"
            )
        return self.regions[region_code]

    def generate_record(self, domain: str, region_code: str) -> dict[str, Any]:
        if domain not in self.domain_generators:
            raise KeyError(
                f"Unknown domain '{domain}'. "
                f"Known domains: {list(self.domain_generators.keys())}"
            )
        region_info = self.get_region_data(region_code)
        countries = region_info.get("countries") or ["ZZ"]
        country = countries[0]
        seed = int(self._rng.integers(0, 1_000_001))
        generator = self.domain_generators[domain]
        return generator.generate_record(region_code, country, seed)

    def generate_batch(
        self, domain: str, region_code: str, size: int
    ) -> list[dict[str, Any]]:
        return [self.generate_record(domain, region_code) for _ in range(size)]

    def to_parquet(self, records: list[dict[str, Any]], path: str):
        # Lightweight: save as JSONL when PySpark/Parquet isn't available.
        with open(path, "w") as f:
            for r in records:
                f.write(json.dumps(r, default=str) + "\n")
        print(f"Saved {len(records)} records to {path} (JSONL fallback)")
