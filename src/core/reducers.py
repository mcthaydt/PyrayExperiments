def game_reducer(state, action):
    if action["type"] == "UPDATE_CAMERA":
        payload = action["payload"]
        return {
            **state,
            "camera_angle": payload["angle"],
            "offset_height": payload["offset_height"],
        }
    elif action["type"] == "UPDATE_MOVEMENT":
        payload = action["payload"]
        return {
            **state,
            "move_direction": payload["move_direction"],
            "last_move_direction": payload["last_move_direction"],
        }
    elif action["type"] == "UPDATE_POSITION":
        payload = action["payload"]
        return {
            **state,
            "player_position": payload["player_position"],
        }
    elif action["type"] == "UPDATE_INPUT":
        payload = action["payload"]
        return {
            **state,
            "move_intent": payload["move_intent"],
            "mouse_delta": payload["mouse_delta"],
        }
    elif action["type"] == "UPDATE_FACING":
        payload = action["payload"]
        return {
            **state,
            "facing_angle": payload["facing_angle"],
            "last_move_direction": payload["last_move_direction"],
        }
    return state
