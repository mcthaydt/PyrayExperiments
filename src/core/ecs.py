# src/core/ecs.py


class EntityComponentSystem:
    def __init__(self):
        self.entities = set()
        # components[entity_id] = { component_type: component_data, ... }
        self.components = {}

    def create_entity(self):
        entity_id = len(self.entities) + 1
        self.entities.add(entity_id)
        return entity_id

    def add_component(self, entity_id, component_type, component_data):
        if entity_id not in self.entities:
            raise ValueError(f"Entity {entity_id} does not exist")
        if entity_id not in self.components:
            self.components[entity_id] = {}
        self.components[entity_id][component_type] = component_data

    def remove_component(self, entity_id, component_type):
        if (
            entity_id in self.components
            and component_type in self.components[entity_id]
        ):
            del self.components[entity_id][component_type]

    def get_component(self, entity_id, component_type):
        """Returns the component data for entity_id and component_type, or None if missing."""
        return self.components.get(entity_id, {}).get(component_type)

    def get_all_entities_with_components(self, component_types):
        """Return a list of all entities that have *all* of the given component_types."""
        result = []
        for entity_id, entity_comps in self.components.items():
            if all(ct in entity_comps for ct in component_types):
                result.append(entity_id)
        return result

    def delete_entity(self, entity_id):
        self.entities.discard(entity_id)
        self.components.pop(entity_id, None)
