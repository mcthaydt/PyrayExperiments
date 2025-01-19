# src/core/actions.py


def create_action_update_camera(new_angle, new_offset):
    return {
        "type": "UPDATE_CAMERA",
        "payload": {
            "angle": new_angle,
            "offset_height": new_offset,
        },
    }


def create_action_update_movement(move_direction, last_move_direction):
    return {
        "type": "UPDATE_MOVEMENT",
        "payload": {
            "move_direction": move_direction,
            "last_move_direction": last_move_direction,
        },
    }


def create_action_update_position(new_position):
    return {
        "type": "UPDATE_POSITION",
        "payload": {
            "player_position": new_position,
        },
    }


def create_action_update_input(move_intent, mouse_delta):
    return {
        "type": "UPDATE_INPUT",
        "payload": {
            "move_intent": move_intent,
            "mouse_delta": mouse_delta,
        },
    }


def create_action_update_facing(angle, direction_idx):
    return {
        "type": "UPDATE_FACING",
        "payload": {
            "facing_angle": angle,
            "last_move_direction": direction_idx,
        },
    }
