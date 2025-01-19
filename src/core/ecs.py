from core.constants import Transform
from typing import Type


class EntityComponentSystem:
    def __init__(self):
        self.entities = set()
        self.components = {}

    def create_entity(self) -> int:
        entity_id = len(self.entities) + 1
        self.entities.add(entity_id)
        return entity_id

    def add_component(
        self, entity_id: int, component_type: str, component_data: object
    ):
        if entity_id not in self.entities:
            raise ValueError(f"Entity {entity_id} does not exist")
        if entity_id not in self.components:
            self.components[entity_id] = {}
        self.components[entity_id][component_type] = component_data

    def get_component(self, entity_id: int, component_type: str):
        return self.components.get(entity_id, {}).get(component_type)

    def get_all_entities_with_components(self, component_types: list):
        """Return a list of all entities that have *all* of the given component_types."""
        result = []
        for entity_id, entity_comps in self.components.items():
            if all(ct in entity_comps for ct in component_types):
                result.append(entity_id)
        return result
