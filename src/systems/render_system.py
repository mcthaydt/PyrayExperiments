import math
import pyray as rl
from core.constants import DIRECTION_TO_INDEX


class RenderSystem:
    def __init__(self, store, ecs):
        self.store = store
        self.ecs = ecs

        # Load resources
        self.floor_texture = rl.load_texture("assets/FloorTexture.png")
        rl.set_texture_wrap(self.floor_texture, rl.TEXTURE_WRAP_REPEAT)

        self.floor_material = rl.load_material_default()
        self.floor_material.maps[rl.MATERIAL_MAP_DIFFUSE].texture = self.floor_texture

        self.tile_size = 3
        self.floor_mesh = rl.gen_mesh_plane(self.tile_size, self.tile_size, 1, 1)
        self.floor_model = rl.load_model_from_mesh(self.floor_mesh)
        self.floor_model.materials[0] = self.floor_material
        self.grid_size = 10

    def update(self, camera, sprite_sheet, frame_width, frame_height):
        state = self.store.get_state()
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

        # Begin drawing
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        rl.begin_mode_3d(camera)

        # Draw tiled floor
        for x in range(-self.grid_size // 2, self.grid_size // 2):
            for z in range(-self.grid_size // 2, self.grid_size // 2):
                position = rl.Vector3(x * self.tile_size, 0, z * self.tile_size)
                rl.draw_model(self.floor_model, position, 1.0, rl.WHITE)

        # Draw player billboard
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
                state["player_position"].y + 0.9,
                state["player_position"].z,
            ),
            rl.Vector2(2.0, 2.0),
            rl.WHITE,
        )

        rl.end_mode_3d()
        rl.end_drawing()

    def unload_resources(self):
        rl.unload_texture(self.floor_texture)
        rl.unload_model(self.floor_model)
