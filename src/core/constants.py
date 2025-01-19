from dataclasses import dataclass
from pyray import Vector3

# ECS component keys
COMPONENT_TRANSFORM = "transform"
COMPONENT_PLAYER = "player"
COMPONENT_FLOOR = "floor"


# Dataclass for Transform Component
@dataclass
class Transform:
    position: Vector3
    rotation: float


# Dataclass for GameState
@dataclass
class GameState:
    camera_angle: float = 0.0
    offset_height: float = 2.15
    last_move_direction: int = 0
    move_intent: dict = None
    mouse_delta: dict = None
    facing_angle: float = 0.0  # <-- Add this field
    player_position: Vector3 = Vector3(0, 0, 0)  # Add this attribute


# Initial state
INITIAL_STATE = GameState()

# Movement direction indexing
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

# Sprite direction map
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
