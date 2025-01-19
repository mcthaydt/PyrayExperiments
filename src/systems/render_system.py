# src/systems/render_system.py

import math
import pyray as rl
from core.constants import (
    COMPONENT_PLAYER,
    COMPONENT_TRANSFORM,
    COMPONENT_FLOOR,
)


class RenderSystem:
    def __init__(self, store, ecs, resource_manager):
        self.store = store
        self.ecs = ecs
        self.res = resource_manager  # short alias to ResourceManager

        # Load (or retrieve) the floor texture
        self.floor_texture = self.res.load_texture(
            key="floor_texture",
            path="assets/FloorTexture.png",
            wrap_mode=rl.TEXTURE_WRAP_REPEAT,
        )

        # Create a default material for the floor and assign the texture
        self.floor_material = rl.load_material_default()
        self.floor_material.maps[rl.MATERIAL_MAP_DIFFUSE].texture = self.floor_texture

        # Create a mesh+model for a single floor tile
        self.tile_size = 3
        self.floor_model = self.res.load_mesh_model(
            "floor_tile_model", rl.gen_mesh_plane, self.tile_size, self.tile_size, 1, 1
        )

        # Ensure it uses the newly created floor material
        self.floor_model.materials[0] = self.floor_material

        # Load the sprite sheet texture
        self.sprite_sheet = self.res.load_texture(
            key="sprite_sheet", path="assets/SpriteSheet.png"
        )
        self.frame_width = self.sprite_sheet.width // 8
        self.frame_height = self.sprite_sheet.height

        # Create a camera
        self.camera = rl.Camera3D(
            rl.Vector3(0, 5, -5),  # position
            rl.Vector3(0, 1, 0),  # target
            rl.Vector3(0, 1, 0),  # up
            45,
            rl.CAMERA_PERSPECTIVE,
        )

    def update(self):
        state = self.store.get_state()
        angle = state["camera_angle"]
        offset_height = state["offset_height"]
        direction_idx = state["last_move_direction"]

        # Get player position from ECS
        player_entities = self.ecs.get_all_entities_with_components(
            [COMPONENT_PLAYER, COMPONENT_TRANSFORM]
        )
        if player_entities:
            player_id = player_entities[0]
            transform = self.ecs.get_component(player_id, COMPONENT_TRANSFORM)
            player_pos = transform["position"]
        else:
            player_pos = rl.Vector3(0, 0, 0)

        # Position the camera behind the player
        self.camera.position.x = player_pos.x + 5.0 * math.cos(angle)
        self.camera.position.z = player_pos.z + 5.0 * math.sin(angle)
        self.camera.position.y = player_pos.y + offset_height
        self.camera.target = rl.Vector3(player_pos.x, player_pos.y + 1.0, player_pos.z)

        # Begin drawing
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        rl.begin_mode_3d(self.camera)

        # Draw floor tiles
        floor_entities = self.ecs.get_all_entities_with_components(
            [COMPONENT_FLOOR, COMPONENT_TRANSFORM]
        )
        for floor_entity in floor_entities:
            floor_transform = self.ecs.get_component(floor_entity, COMPONENT_TRANSFORM)
            tile_pos = floor_transform["position"]
            rl.draw_model(self.floor_model, tile_pos, 1.0, rl.WHITE)

        # Draw player billboard
        frame_rect = rl.Rectangle(
            self.frame_width * direction_idx,
            0,
            self.frame_width,
            self.frame_height,
        )
        rl.draw_billboard_rec(
            self.camera,
            self.sprite_sheet,
            frame_rect,
            rl.Vector3(player_pos.x, player_pos.y + 0.9, player_pos.z),
            rl.Vector2(2.0, 2.0),
            rl.WHITE,
        )

        rl.end_mode_3d()
        rl.end_drawing()
