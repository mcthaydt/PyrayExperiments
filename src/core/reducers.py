from core.constants import GameState
from core.actions import (
    UpdateCameraAction,
    UpdateMovementAction,
    UpdatePositionAction,
    UpdateInputAction,
    UpdateFacingAction,
)


def game_reducer(state: GameState, action):
    # Create a copy of the current state
    updated_state = state.__dict__.copy()

    if isinstance(action, UpdateCameraAction):
        updated_state["camera_angle"] = action.angle
        updated_state["offset_height"] = action.offset_height

    elif isinstance(action, UpdateMovementAction):
        updated_state["move_intent"] = action.move_direction
        updated_state["last_move_direction"] = action.last_move_direction

    elif isinstance(action, UpdatePositionAction):
        updated_state["player_position"] = action.player_position

    elif isinstance(action, UpdateInputAction):
        updated_state["move_intent"] = action.move_intent
        updated_state["mouse_delta"] = action.mouse_delta

    elif isinstance(action, UpdateFacingAction):
        updated_state["facing_angle"] = action.facing_angle
        updated_state["last_move_direction"] = action.last_move_direction

    # Return a new GameState instance with the updated state
    return GameState(**updated_state)
