# src/systems/camera_system.py

import pyray as rl
from core.actions import create_action_update_camera


class CameraSystem:
    def __init__(self, store, ecs):
        self.store = store
        self.ecs = ecs
        self.mouse_sensitivity = 0.005

    def update(self):
        state = self.store.get_state()
        mouse_delta = state.get("mouse_delta", {"x": 0, "y": 0})
        # Access mouse_delta as a dictionary
        mouse_dx = mouse_delta["x"]

        new_angle = state.get("camera_angle", 0.0) - mouse_dx * self.mouse_sensitivity

        default_height = 2.15
        offset_height = state.get("offset_height", default_height)
        new_height = offset_height + (default_height - offset_height) * 0.1

        self.store.dispatch(create_action_update_camera(new_angle, new_height))
