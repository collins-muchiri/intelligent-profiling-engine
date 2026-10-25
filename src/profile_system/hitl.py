

class HITLFeedback:
    def __init__(self):
        self.validations: list[dict] = []  # e.g., {"entity_id": "123", "validated": True, "notes": "..."}
        self.overrides: list[dict] = []    # e.g., {"rule": "anomaly_threshold", "override_value": 0.5}

    def add_validation(self, validation: dict):
        self.validations.append(validation)

    def add_override(self, override: dict):
        self.overrides.append(override)

    def get_feedback_for_entity(self, entity_id: str) -> list[dict]:
        return [v for v in self.validations if v.get("entity_id") == entity_id]

    def apply_overrides(self, config: dict) -> dict:
        for override in self.overrides:
            config[override["rule"]] = override["override_value"]
        return config
