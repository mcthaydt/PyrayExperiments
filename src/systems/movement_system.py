# src/systems/movement_system.py

import math
from core.actions import create_action_update_position
from core.constants import COMPONENT_PLAYER, COMPONENT_TRANSFORM
from pyray import Vector3


class MovementSystem:
    def __init__(self, store, ecs):
        self.store = store
        self.ecs = ecs

    def update(self):
        state = self.store.get_state()
        # Get move_intent from state (assumed to be a dictionary with keys "x", "y")
        move_intent = state.get("move_intent", {"x": 0, "y": 0})
        # Read the global camera angle (if needed for movement orientation)
        camera_angle = state.get("camera_angle", 0)

        # Calculate the world-space movement vector using the camera orientation.
        # For example, if the intent y represents forward/backward relative to the camera:
        forward = Vector3(-math.sin(camera_angle), 0, math.cos(camera_angle))
        right = Vector3(math.cos(camera_angle), 0, math.sin(camera_angle))

        movement_vector = Vector3(0, 0, 0)
        movement_vector.x = move_intent["y"] * (-right.x) + move_intent["x"] * (
            forward.x
        )
        movement_vector.z = move_intent["y"] * (-right.z) + move_intent["x"] * (
            forward.z
        )

        # Normalize the movement vector if necessary
        mag = (movement_vector.x**2 + movement_vector.z**2) ** 0.5
        if mag > 0:
            movement_vector.x /= mag
            movement_vector.z /= mag

        # Get the player entity and its transform component
        player_entities = self.ecs.get_all_entities_with_components(
            [COMPONENT_PLAYER, COMPONENT_TRANSFORM]
        )
        if not player_entities:
            return

        player_id = player_entities[0]
        transform = self.ecs.get_component(player_id, COMPONENT_TRANSFORM)
        # Update the position based on a speed value (here using a constant speed)
        speed = 1.0
        dt = 0.1  # time delta could be computed in your main loop
        transform["position"].x += movement_vector.x * speed * dt
        transform["position"].z += movement_vector.z * speed * dt

        # Dispatch action to keep the store updated (if needed)
        self.store.dispatch(create_action_update_position(transform["position"]))
