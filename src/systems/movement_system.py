import math
import pyray as rl
from core.actions import (
    create_action_update_movement,
    create_action_update_position,
)
from core.constants import COMPONENT_PLAYER
from utils.movement_utils import (
    map_angle_to_direction,
    get_facing_direction,
    DIRECTION_TO_INDEX,
)


class MovementSystem:
    def __init__(self, store, ecs):
        self.store = store
        self.ecs = ecs
        self.camera_rotation_threshold = 0.1
        self.absolute_facing_angle = 0.0

    def update(self):
        state = self.store.get_state()
        camera_angle = state["camera_angle"]

        forward_vector = rl.Vector3(-math.sin(camera_angle), 0, math.cos(camera_angle))
        right_vector = rl.Vector3(math.cos(camera_angle), 0, math.sin(camera_angle))

        move_direction = rl.Vector3(0, 0, 0)
        facing_direction = rl.Vector2(0, 0)
        is_moving = False

        # Movement input
        if rl.is_key_down(rl.KEY_W):
            move_direction.x -= right_vector.x
            move_direction.z -= right_vector.z
            facing_direction.y = 1
            is_moving = True
        if rl.is_key_down(rl.KEY_S):
            move_direction.x += right_vector.x
            move_direction.z += right_vector.z
            facing_direction.y = -1
            is_moving = True
        if rl.is_key_down(rl.KEY_A):
            move_direction.x += forward_vector.x
            move_direction.z += forward_vector.z
            facing_direction.x = -1
            is_moving = True
        if rl.is_key_down(rl.KEY_D):
            move_direction.x -= forward_vector.x
            move_direction.z -= forward_vector.z
            facing_direction.x = 1
            is_moving = True

        # Normalize
        length = math.sqrt(move_direction.x**2 + move_direction.z**2)
        if length > 0:
            move_direction.x /= length
            move_direction.z /= length

        new_direction = state["last_move_direction"]
        mouse_dx = rl.get_mouse_delta().x

        if is_moving:
            # Movement-based facing
            movement_vector = rl.Vector3(facing_direction.y, 0, -facing_direction.x)
            new_direction = get_facing_direction(movement_vector, new_direction)
            self.absolute_facing_angle = new_direction * 45
        else:
            # Camera-based facing if not moving
            if abs(mouse_dx) > self.camera_rotation_threshold:
                self.absolute_facing_angle = (
                    self.absolute_facing_angle + math.degrees(mouse_dx * -0.005)
                ) % 360
                dir_name = map_angle_to_direction(self.absolute_facing_angle)
                new_direction = DIRECTION_TO_INDEX[dir_name]
            else:
                # Keep current absolute angle
                self.absolute_facing_angle = state["last_move_direction"] * 45

        # Dispatch updated movement
        self.store.dispatch(
            create_action_update_movement(move_direction, new_direction)
        )

        # Update player position
        new_position = rl.Vector3(
            state["player_position"].x + move_direction.x * 0.1,
            state["player_position"].y,
            state["player_position"].z + move_direction.z * 0.1,
        )
        self.store.dispatch(create_action_update_position(new_position))
