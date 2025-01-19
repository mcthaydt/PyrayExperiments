# src/systems/input_system.py

import pyray as rl
from core.actions import (
    create_action_update_input,
)


class InputSystem:
    def __init__(self, store):
        self.store = store

    def update(self):
        # Gather keyboard movement intent
        move_intent = {
            "x": 0,
            "y": 0,
        }
        if rl.is_key_down(rl.KEY_W):
            move_intent["y"] += 1
        if rl.is_key_down(rl.KEY_S):
            move_intent["y"] -= 1
        if rl.is_key_down(rl.KEY_A):
            move_intent["x"] += 1
        if rl.is_key_down(rl.KEY_D):
            move_intent["x"] -= 1

        # Get mouse delta as a Vector2-like object, then convert it to a dict
        vec = rl.get_mouse_delta()
        mouse_delta = {"x": vec.x, "y": vec.y}

        # Dispatch an action that updates the input-related state.
        self.store.dispatch(create_action_update_input(move_intent, mouse_delta))
