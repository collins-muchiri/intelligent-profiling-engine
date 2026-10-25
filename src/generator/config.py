from typing import Any

import yaml


class ConfigLoader:
    def __init__(self, path: str):
        self.path = path
        self.config: dict[str, Any] = {}
        self.load()

    def load(self) -> dict[str, Any]:
        with open(self.path) as f:
            self.config = yaml.safe_load(f)
        return self.config

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)
