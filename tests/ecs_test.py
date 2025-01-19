import unittest
from modules.ecs import EntityComponentSystem


class TestEntityComponentSystem(unittest.TestCase):
    def setUp(self):
        self.ecs = EntityComponentSystem()

    def test_create_entity(self):
        entity1 = self.ecs.create_entity()
        entity2 = self.ecs.create_entity()
        self.assertNotEqual(entity1, entity2)
        self.assertIn(entity1, self.ecs.entities)
        self.assertIn(entity2, self.ecs.entities)

    def test_add_component(self):
        entity = self.ecs.create_entity()
        self.ecs.add_component(entity, "Position", {"x": 0, "y": 0})
        self.assertIn("Position", self.ecs.components[entity])
        self.assertEqual(self.ecs.components[entity]["Position"], {"x": 0, "y": 0})

    def test_add_component_to_non_existent_entity(self):
        with self.assertRaises(ValueError):
            self.ecs.add_component(999, "Position", {"x": 0, "y": 0})

    def test_remove_component(self):
        entity = self.ecs.create_entity()
        self.ecs.add_component(entity, "Position", {"x": 0, "y": 0})
        self.ecs.remove_component(entity, "Position")
        self.assertNotIn("Position", self.ecs.components[entity])

    def test_remove_non_existent_component(self):
        entity = self.ecs.create_entity()
        self.ecs.remove_component(entity, "Velocity")  # Should do nothing
        self.assertNotIn("Velocity", self.ecs.components.get(entity, {}))

    def test_get_all_entities_with_components(self):
        entity1 = self.ecs.create_entity()
        entity2 = self.ecs.create_entity()
        self.ecs.add_component(entity1, "Position", {"x": 0, "y": 0})
        self.ecs.add_component(entity2, "Position", {"x": 1, "y": 1})
        self.ecs.add_component(entity2, "Velocity", {"dx": 1, "dy": 1})

        result = self.ecs.get_all_entities_with_components(["Position"])
        self.assertListEqual(result, [entity1, entity2])

        result = self.ecs.get_all_entities_with_components(["Position", "Velocity"])
        self.assertListEqual(result, [entity2])

    def test_delete_entity(self):
        entity = self.ecs.create_entity()
        self.ecs.add_component(entity, "Position", {"x": 0, "y": 0})
        self.ecs.delete_entity(entity)
        self.assertNotIn(entity, self.ecs.entities)
        self.assertNotIn(entity, self.ecs.components)

    def test_delete_non_existent_entity(self):
        self.ecs.delete_entity(999)  # Should do nothing
        self.assertNotIn(999, self.ecs.entities)

    def test_performance_get_all_entities_with_components(self):
        for i in range(10000):
            entity = self.ecs.create_entity()
            if i % 2 == 0:
                self.ecs.add_component(entity, "Position", {"x": i, "y": i})

        result = self.ecs.get_all_entities_with_components(["Position"])
        self.assertEqual(len(result), 5000)


if __name__ == "__main__":
    unittest.main()
