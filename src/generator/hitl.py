

class HITLStore:
    def __init__(self):
        self.validations: list[dict] = []
        self.overrides: list[dict] = []

    def add_validation(self, validation: dict):
        self.validations.append(validation)

    def add_override(self, override: dict):
        self.overrides.append(override)

    def get_for_entity(self, entity_id: str) -> list[dict]:
        return [v for v in self.validations if v.get("entity_id") == entity_id]
