# src/utils/movement_utils.py
import math
from core.constants import SPRITE_DIRECTION_MAP, DIRECTION_TO_INDEX


def map_angle_to_direction(angle):
    """Given an angle in degrees, return the string key for SPRITE_DIRECTION_MAP."""
    normalized_angle = angle % 360
    if 337.5 <= normalized_angle or normalized_angle < 22.5:
        return "front"
    elif 22.5 <= normalized_angle < 67.5:
        return "front-right"
    elif 67.5 <= normalized_angle < 112.5:
        return "right"
    elif 112.5 <= normalized_angle < 157.5:
        return "back-right"
    elif 157.5 <= normalized_angle < 202.5:
        return "back"
    elif 202.5 <= normalized_angle < 247.5:
        return "back-left"
    elif 247.5 <= normalized_angle < 292.5:
        return "left"
    elif 292.5 <= normalized_angle < 337.5:
        return "front-left"


def get_facing_direction(movement_input, last_direction_index):
    """Converts a Vector3 movement input to a direction index."""
    # movement_input.x, movement_input.z (2D plane)
    movement_length = math.sqrt(movement_input.x**2 + movement_input.z**2)
    if movement_length > 0:
        angle = math.degrees(math.atan2(movement_input.z, movement_input.x)) + 180
        direction_str = map_angle_to_direction(angle)
        return DIRECTION_TO_INDEX[direction_str]
    return last_direction_index
