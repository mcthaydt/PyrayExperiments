import math
from core.actions import create_action_update_facing
from utils.movement_utils import map_angle_to_direction, DIRECTION_TO_INDEX


class FacingSystem:
    def __init__(self, store):
        self.store = store
        self.camera_rotation_threshold = 0.1
        self.absolute_facing_angle = 0.0

    def update(self):
        state = self.store.get_state()
        move_intent = state.move_intent or {"x": 0, "y": 0}
        mouse_delta = state.mouse_delta or {"x": 0, "y": 0}
        current_direction_idx = state.last_move_direction

        if move_intent["x"] != 0 or move_intent["y"] != 0:
            angle_radians = math.atan2(-move_intent["x"], -move_intent["y"])
            self.absolute_facing_angle = math.degrees(angle_radians) % 360
            dir_name = map_angle_to_direction(self.absolute_facing_angle)
            new_direction_idx = DIRECTION_TO_INDEX[dir_name]
        else:
            if abs(mouse_delta["x"]) > self.camera_rotation_threshold:
                self.absolute_facing_angle += mouse_delta["x"] * -0.5
                self.absolute_facing_angle %= 360
                dir_name = map_angle_to_direction(self.absolute_facing_angle)
                new_direction_idx = DIRECTION_TO_INDEX[dir_name]
            else:
                new_direction_idx = current_direction_idx

        self.store.dispatch(
            create_action_update_facing(self.absolute_facing_angle, new_direction_idx)
        )
