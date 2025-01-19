def create_action_update_position(position):
    return {"type": "UPDATE_PLAYER_POSITION", "position": position}


def create_action_update_camera(angle, height):
    return {"type": "UPDATE_CAMERA", "angle": angle, "height": height}


def create_action_update_movement(direction, last_direction):
    return {
        "type": "UPDATE_MOVEMENT",
        "direction": direction,
        "last_direction": last_direction,
    }
