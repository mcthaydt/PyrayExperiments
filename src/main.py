import pyray as rl
from pyray import Vector3

from core.store import Store, logger_middleware
from core.reducers import game_reducer
from core.ecs import EntityComponentSystem
from core.constants import (
    COMPONENT_PLAYER,
    COMPONENT_TRANSFORM,
    COMPONENT_FLOOR,
    GameState,
    Transform,
)

from systems.camera_system import CameraSystem
from systems.movement_system import MovementSystem
from systems.render_system import RenderSystem
from systems.input_system import InputSystem
from systems.facing_system import FacingSystem
from core.resources import ResourceManager


def create_floor_tiles(ecs, grid_size=10, tile_size=3):
    """Creates an ECS entity for each floor tile in a grid."""
    half_grid = grid_size // 2
    for x in range(-half_grid, half_grid):
        for z in range(-half_grid, half_grid):
            tile_entity = ecs.create_entity()
            ecs.add_component(tile_entity, COMPONENT_FLOOR, {})
            ecs.add_component(
                tile_entity,
                COMPONENT_TRANSFORM,
                Transform(
                    position=Vector3(x * tile_size, 0, z * tile_size), rotation=0.0
                ),
            )


def main():
    rl.init_window(960, 540, "2D Sprites in 3D World - ECS + Store")
    rl.set_target_fps(60)
    rl.disable_cursor()

    # Create a Redux-style store
    store = Store(
        reducer=game_reducer,
        initial_state=GameState(),
        middleware=[logger_middleware],
    )

    # Create ECS and entities
    ecs = EntityComponentSystem()

    # Create a Player entity in ECS
    player_entity = ecs.create_entity()
    ecs.add_component(
        player_entity,
        COMPONENT_TRANSFORM,
        Transform(position=Vector3(0, 0, 0), rotation=0.0),
    )
    ecs.add_component(player_entity, COMPONENT_PLAYER, {"speed": 1.0})

    # Create floor tiles in ECS
    create_floor_tiles(ecs, grid_size=10, tile_size=3)

    # Instantiate ResourceManager
    resource_manager = ResourceManager()

    # Initialize systems
    input_system = InputSystem(store)
    camera_system = CameraSystem(store, ecs)
    facing_system = FacingSystem(store)
    movement_system = MovementSystem(store, ecs)
    render_system = RenderSystem(store, ecs, resource_manager)

    # Main loop: update each system in a separated manner
    while not rl.window_should_close():
        # 1. Gather and dispatch input
        input_system.update()
        # 2. Update camera based on mouse input (and other factors)
        camera_system.update()
        # 3. Update player facing direction decoupled from movement
        facing_system.update()
        # 4. Update player movement based on input
        movement_system.update()
        # 5. Render the scene with all updated information
        render_system.update()

    # Cleanup
    rl.enable_cursor()
    resource_manager.unload_all()
    rl.close_window()


if __name__ == "__main__":
    main()
