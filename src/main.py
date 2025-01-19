import pyray as rl
from core.store import Store, logger_middleware
from core.ecs import EntityComponentSystem
from core.constants import (
    COMPONENT_TRANSFORM,
    COMPONENT_PLAYER,
    INITIAL_STATE,
)
from core.reducers import game_reducer
from systems.camera_system import CameraSystem
from systems.movement_system import MovementSystem
from systems.render_system import RenderSystem


def main():
    rl.init_window(960, 540, "2D Sprites in 3D World")
    rl.set_target_fps(60)
    rl.disable_cursor()

    # Create the Redux-style store
    store = Store(
        reducer=game_reducer,
        initial_state=INITIAL_STATE,
        middleware=[logger_middleware],
    )

    # Initialize the ECS
    ecs = EntityComponentSystem()
    player_entity = ecs.create_entity()
    ecs.add_component(
        player_entity,
        COMPONENT_TRANSFORM,
        {"position": rl.Vector3(0, 0, 0), "rotation": 0},
    )
    ecs.add_component(player_entity, COMPONENT_PLAYER, {"speed": 1.0})

    # Initialize Systems
    camera_system = CameraSystem(store, ecs)
    movement_system = MovementSystem(store, ecs)
    render_system = RenderSystem(store, ecs)

    # Create the camera
    camera = rl.Camera3D(
        rl.Vector3(0, 5, -5),
        rl.Vector3(0, 1, 0),
        rl.Vector3(0, 1, 0),
        45,
        rl.CAMERA_PERSPECTIVE,
    )

    # Load the sprite sheet and figure out frame size
    sprite_sheet = rl.load_texture("assets/SpriteSheet.png")
    frame_width = sprite_sheet.width // 8
    frame_height = sprite_sheet.height

    # Main Loop
    while not rl.window_should_close():
        camera_system.update()
        movement_system.update()
        render_system.update(camera, sprite_sheet, frame_width, frame_height)

    # Cleanup
    rl.enable_cursor()
    rl.unload_texture(sprite_sheet)
    render_system.unload_resources()
    rl.close_window()


if __name__ == "__main__":
    main()
