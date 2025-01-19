import math
from core.actions import create_action_update_position
from core.constants import COMPONENT_PLAYER, COMPONENT_TRANSFORM, Transform
from pyray import Vector3


class MovementSystem:
    def __init__(self, store, ecs):
        self.store = store
        self.ecs = ecs

    def update(self):
        state = self.store.get_state()
        move_intent = state.move_intent or {"x": 0, "y": 0}
        camera_angle = state.camera_angle

        # Calculate world-space movement vector
        forward = Vector3(-math.sin(camera_angle), 0, math.cos(camera_angle))
        right = Vector3(math.cos(camera_angle), 0, math.sin(camera_angle))

        movement_vector = Vector3(
            move_intent["y"] * (-right.x) + move_intent["x"] * forward.x,
            0,
            move_intent["y"] * (-right.z) + move_intent["x"] * forward.z,
        )

        # Normalize movement vector
        mag = (movement_vector.x**2 + movement_vector.z**2) ** 0.5
        if mag > 0:
            movement_vector.x /= mag
            movement_vector.z /= mag

        # Update player position
        player_entities = self.ecs.get_all_entities_with_components(
            [COMPONENT_PLAYER, COMPONENT_TRANSFORM]
        )
        if not player_entities:
            return

        player_id = player_entities[0]
        transform: Transform = self.ecs.get_component(player_id, COMPONENT_TRANSFORM)

        # Update the transform's position
        transform.position.x += movement_vector.x * 0.1
        transform.position.z += movement_vector.z * 0.1

        # Dispatch action
        self.store.dispatch(create_action_update_position(transform.position))
