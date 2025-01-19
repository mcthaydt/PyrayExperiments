from dataclasses import dataclass
from pyray import Vector3


# Dataclass Definitions
@dataclass
class UpdateCameraAction:
    angle: float
    offset_height: float
    type: str = "UPDATE_CAMERA"


@dataclass
class UpdateMovementAction:
    move_direction: dict
    last_move_direction: int
    type: str = "UPDATE_MOVEMENT"


@dataclass
class UpdatePositionAction:
    player_position: Vector3
    type: str = "UPDATE_POSITION"


@dataclass
class UpdateInputAction:
    move_intent: dict
    mouse_delta: dict
    type: str = "UPDATE_INPUT"


@dataclass
class UpdateFacingAction:
    facing_angle: float
    last_move_direction: int
    type: str = "UPDATE_FACING"


# Compatibility Functions
def create_action_update_camera(angle: float, offset_height: float):
    return UpdateCameraAction(angle=angle, offset_height=offset_height)


def create_action_update_movement(move_direction: dict, last_move_direction: int):
    return UpdateMovementAction(
        move_direction=move_direction, last_move_direction=last_move_direction
    )


def create_action_update_position(player_position: Vector3):
    return UpdatePositionAction(player_position=player_position)


def create_action_update_input(move_intent: dict, mouse_delta: dict):
    return UpdateInputAction(move_intent=move_intent, mouse_delta=mouse_delta)


def create_action_update_facing(facing_angle: float, last_move_direction: int):
    return UpdateFacingAction(
        facing_angle=facing_angle, last_move_direction=last_move_direction
    )
