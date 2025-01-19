# src/core/constants.py

import math

# ECS component keys
COMPONENT_TRANSFORM = "transform"
COMPONENT_PLAYER = "player"
COMPONENT_FLOOR = "floor"  # <--- Added for floor tiles

# Initial store state
INITIAL_STATE = {
    "camera_angle": 0.0,
    "offset_height": 2.15,
    "last_move_direction": 0,
    "move_intent": {"x": 0, "y": 0},
    "mouse_delta": {"x": 0, "y": 0},
}

# For movement direction indexing (0..7)
DIRECTION_TO_INDEX = {
    "front": 0,
    "front-right": 1,
    "right": 2,
    "back-right": 3,
    "back": 4,
    "back-left": 5,
    "left": 6,
    "front-left": 7,
}

# For mapping direction names to sprite frames, if you need it
SPRITE_DIRECTION_MAP = {
    "front": 0,
    "front-right": 1,
    "right": 2,
    "back-right": 3,
    "back": 4,
    "back-left": 5,
    "left": 6,
    "front-left": 7,
}
