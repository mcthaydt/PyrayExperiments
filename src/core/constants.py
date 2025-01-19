import pyray as rl

# -- Component Types --
COMPONENT_TRANSFORM = "transform"
COMPONENT_SPRITE = "sprite"
COMPONENT_CAMERA = "camera"
COMPONENT_INPUT = "input"
COMPONENT_PLAYER = "player"

# -- Sprite Direction --
SPRITE_DIRECTION_MAP = {
    0: "front",
    1: "front-right",
    2: "right",
    3: "back-right",
    4: "back",
    5: "back-left",
    6: "left",
    7: "front-left",
}
DIRECTION_TO_INDEX = {v: k for k, v in SPRITE_DIRECTION_MAP.items()}

# -- Initial Game State --
INITIAL_STATE = {
    "player_position": rl.Vector3(0, 0, 0),
    "camera_angle": 0.0,
    "offset_height": 2.15,
    "move_direction": rl.Vector3(0, 0, 0),
    "last_move_direction": 4,
}
