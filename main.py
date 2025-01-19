import pyray as rl
import math
from modules.redux import Store, root_reducer, logger_middleware
from modules.ecs import EntityComponentSystem

# Component Types
COMPONENT_TRANSFORM = "transform"
COMPONENT_SPRITE = "sprite"
COMPONENT_CAMERA = "camera"
COMPONENT_INPUT = "input"
COMPONENT_PLAYER = "player"

# Sprite direction map
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

# Initial Game State
INITIAL_STATE = {
    "player_position": rl.Vector3(0, 0, 0),
    "camera_angle": 0.0,
    "offset_height": 2.15,
    "move_direction": rl.Vector3(0, 0, 0),
    "last_move_direction": 4,
}


# Redux Actions
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


# Enhanced Redux Reducer
def game_reducer(state, action):
    state = state or INITIAL_STATE

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


# Helper Functions
def map_angle_to_direction(angle):
    if 337.5 <= angle or angle < 22.5:
        return "front"
    elif 22.5 <= angle < 67.5:
        return "front-right"
    elif 67.5 <= angle < 112.5:
        return "right"
    elif 112.5 <= angle < 157.5:
        return "back-right"
    elif 157.5 <= angle < 202.5:
        return "back"
    elif 202.5 <= angle < 247.5:
        return "back-left"
    elif 247.5 <= angle < 292.5:
        return "left"
    elif 292.5 <= angle < 337.5:
        return "front-left"


def get_facing_direction(movement_input, last_direction):
    movement_length = math.sqrt(movement_input.x**2 + movement_input.z**2)
    if movement_length > 0:
        dx = movement_input.x
        dz = movement_input.z
        angle = math.atan2(dz, dx) * (180 / math.pi) + 180
    else:
        return last_direction

    return int((angle + 22.5) // 45) % 8


# Systems
class CameraSystem:
    def __init__(self, store, ecs):
        self.store = store
        self.ecs = ecs

    def update(self):
        state = self.store.get_state()
        mouse_dx, _ = rl.get_mouse_delta().x, rl.get_mouse_delta().y
        new_angle = state["camera_angle"] - mouse_dx * 0.005

        default_height = 2.15
        new_height = (
            state["offset_height"] + (default_height - state["offset_height"]) * 0.1
        )

        self.store.dispatch(create_action_update_camera(new_angle, new_height))


def map_angle_to_direction(angle):
    """Maps an angle in degrees to a direction string"""
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


def get_facing_direction(movement_input, last_direction):
    """Converts movement input to a direction index using the SPRITE_DIRECTION_MAP"""
    movement_length = math.sqrt(movement_input.x**2 + movement_input.z**2)

    if movement_length > 0:
        # Calculate angle from movement
        angle = math.degrees(math.atan2(movement_input.z, movement_input.x)) + 180
        # Get the direction string
        direction_string = map_angle_to_direction(angle)
        # Convert to index using the mapping
        return DIRECTION_TO_INDEX[direction_string]

    return last_direction


class MovementSystem:
    def __init__(self, store, ecs):
        self.store = store
        self.ecs = ecs
        self.camera_rotation_threshold = 0.1
        self.absolute_facing_angle = 0.0  # Track the absolute facing angle

    def update(self):
        state = self.store.get_state()
        camera_angle = state["camera_angle"]

        forward_vector = rl.Vector3(-math.sin(camera_angle), 0, math.cos(camera_angle))
        right_vector = rl.Vector3(math.cos(camera_angle), 0, math.sin(camera_angle))

        move_direction = rl.Vector3(0, 0, 0)
        facing_direction = rl.Vector2(0, 0)

        # Handle movement input
        is_moving = False
        if rl.is_key_down(rl.KEY_W):
            move_direction.x -= right_vector.x
            move_direction.z -= right_vector.z
            facing_direction.y = 1
            is_moving = True
        if rl.is_key_down(rl.KEY_S):
            move_direction.x += right_vector.x
            move_direction.z += right_vector.z
            facing_direction.y = -1
            is_moving = True
        if rl.is_key_down(rl.KEY_A):
            move_direction.x += forward_vector.x
            move_direction.z += forward_vector.z
            facing_direction.x = -1
            is_moving = True
        if rl.is_key_down(rl.KEY_D):
            move_direction.x -= forward_vector.x
            move_direction.z -= forward_vector.z
            facing_direction.x = 1
            is_moving = True

        # Normalize movement vector
        length = math.sqrt(move_direction.x**2 + move_direction.z**2)
        if length > 0:
            move_direction.x /= length
            move_direction.z /= length

        # Update facing direction
        new_direction = state["last_move_direction"]
        mouse_dx = rl.get_mouse_delta().x

        if is_moving:
            # When moving, update direction based on movement
            movement_vector = rl.Vector3(facing_direction.y, 0, -facing_direction.x)
            new_direction = get_facing_direction(
                movement_vector, state["last_move_direction"]
            )
            # Update absolute angle based on new direction
            self.absolute_facing_angle = new_direction * 45
        else:
            # When not moving, update based on camera rotation
            if abs(mouse_dx) > self.camera_rotation_threshold:
                # Update the absolute facing angle based on camera movement
                self.absolute_facing_angle = (
                    self.absolute_facing_angle + math.degrees(mouse_dx * -0.005)
                ) % 360
                # Convert absolute angle to direction
                direction_name = map_angle_to_direction(self.absolute_facing_angle)
                new_direction = DIRECTION_TO_INDEX[direction_name]
            else:
                # Maintain current absolute angle but ensure it matches the current direction
                self.absolute_facing_angle = state["last_move_direction"] * 45

        # Update state
        self.store.dispatch(
            create_action_update_movement(move_direction, new_direction)
        )

        # Update position
        new_position = rl.Vector3(
            state["player_position"].x + move_direction.x * 0.1,
            state["player_position"].y,
            state["player_position"].z + move_direction.z * 0.1,
        )
        self.store.dispatch(create_action_update_position(new_position))


class RenderSystem:
    def __init__(self, store, ecs):
        self.store = store
        self.ecs = ecs
        self.floor_texture = rl.load_texture("FloorTexture.png")

        # Set texture wrap to repeat
        rl.set_texture_wrap(self.floor_texture, rl.TEXTURE_WRAP_REPEAT)

        # Create a material and set the texture
        self.floor_material = rl.load_material_default()
        self.floor_material.maps[rl.MATERIAL_MAP_DIFFUSE].texture = self.floor_texture

        # Generate a single tile mesh
        self.tile_size = 3  # Size of each tile
        self.floor_mesh = rl.gen_mesh_plane(self.tile_size, self.tile_size, 1, 1)
        self.floor_model = rl.load_model_from_mesh(self.floor_mesh)

        # Assign the material to the model
        self.floor_model.materials[0] = self.floor_material

        # Define the grid size (number of tiles)
        self.grid_size = 10  # 10x10 grid

    def update(self, camera, sprite_sheet, frame_width, frame_height):
        state = self.store.get_state()

        # Update camera position and target
        camera.position.x = state["player_position"].x + 5.0 * math.cos(
            state["camera_angle"]
        )
        camera.position.z = state["player_position"].z + 5.0 * math.sin(
            state["camera_angle"]
        )
        camera.position.y = state["player_position"].y + state["offset_height"]

        camera.target = rl.Vector3(
            state["player_position"].x,
            state["player_position"].y + 1.0,
            state["player_position"].z,
        )

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.begin_mode_3d(camera)

        # Render the tiled floor
        for x in range(-self.grid_size // 2, self.grid_size // 2):
            for z in range(-self.grid_size // 2, self.grid_size // 2):
                position = rl.Vector3(
                    x * self.tile_size, 0, z * self.tile_size
                )  # Position for each tile
                rl.draw_model(self.floor_model, position, 1.0, rl.WHITE)

        # Draw player sprite
        direction_index = state["last_move_direction"]
        frame_rect = rl.Rectangle(
            frame_width * direction_index,
            0,
            frame_width,
            frame_height,
        )
        rl.draw_billboard_rec(
            camera,
            sprite_sheet,
            frame_rect,
            rl.Vector3(
                state["player_position"].x,
                state["player_position"].y + 1,
                state["player_position"].z,
            ),
            rl.Vector2(2.0, 2.0),
            rl.WHITE,
        )

        rl.end_mode_3d()
        rl.end_drawing()

    def unload_resources(self):
        rl.unload_texture(self.floor_texture)  # Clean up floor texture
        rl.unload_model(self.floor_model)  # Clean up model


def main():
    rl.init_window(800, 600, "2D Sprites in 3D World")
    rl.set_target_fps(60)
    rl.disable_cursor()

    store = Store(
        game_reducer, initial_state=INITIAL_STATE, middleware=[logger_middleware]
    )

    ecs = EntityComponentSystem()
    player_entity = ecs.create_entity()
    ecs.add_component(
        player_entity,
        COMPONENT_TRANSFORM,
        {"position": rl.Vector3(0, 0, 0), "rotation": 0},
    )
    ecs.add_component(player_entity, COMPONENT_PLAYER, {"speed": 1.0})

    camera_system = CameraSystem(store, ecs)
    movement_system = MovementSystem(store, ecs)
    render_system = RenderSystem(store, ecs)

    camera = rl.Camera3D(
        rl.Vector3(0, 5, -5),
        rl.Vector3(0, 1, 0),
        rl.Vector3(0, 1, 0),
        45,
        rl.CAMERA_PERSPECTIVE,
    )

    sprite_sheet = rl.load_texture("SpriteSheet.png")
    frame_width = sprite_sheet.width // 8
    frame_height = sprite_sheet.height

    while not rl.window_should_close():
        camera_system.update()
        movement_system.update()
        render_system.update(camera, sprite_sheet, frame_width, frame_height)

    rl.enable_cursor()
    rl.unload_texture(sprite_sheet)
    render_system.unload_resources()
    rl.close_window()


if __name__ == "__main__":
    main()
