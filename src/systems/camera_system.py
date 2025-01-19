import pyray as rl
from core.actions import create_action_update_camera


class CameraSystem:
    def __init__(self, store, ecs):
        self.store = store
        self.ecs = ecs
        self.mouse_sensitivity = 0.005

    def update(self):
        state = self.store.get_state()
        mouse_dx = rl.get_mouse_delta().x

        # Update camera angle
        new_angle = state["camera_angle"] - mouse_dx * self.mouse_sensitivity

        # Smoothly move offset_height back to 2.15
        default_height = 2.15
        new_height = (
            state["offset_height"] + (default_height - state["offset_height"]) * 0.1
        )

        self.store.dispatch(create_action_update_camera(new_angle, new_height))
