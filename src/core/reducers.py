import copy
from .constants import INITIAL_STATE


def game_reducer(state, action):
    # If no state, use our INITIAL_STATE
    if state is None:
        state = copy.deepcopy(INITIAL_STATE)

    if action["type"] == "UPDATE_PLAYER_POSITION":
        return {**state, "player_position": action["position"]}
    elif action["type"] == "UPDATE_CAMERA":
        return {
            **state,
            "camera_angle": action["angle"],
            "offset_height": action["height"],
        }
    elif action["type"] == "UPDATE_MOVEMENT":
        return {
            **state,
            "move_direction": action["direction"],
            "last_move_direction": action["last_direction"],
        }

    return state
