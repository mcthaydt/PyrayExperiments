# src/core/resources.py

import pyray as rl


class ResourceManager:
    def __init__(self):
        # Dictionaries to track loaded resources
        self.textures = {}
        self.models = {}
        self.meshes = {}
        # You can also add dictionaries for sounds, shaders, etc.

    def load_texture(self, key, path, wrap_mode=None):
        """
        Load a texture from `path` and store it under `key`.
        If `key` already exists, returns the already-loaded texture.
        Optional 'wrap_mode' can be set (e.g., rl.TEXTURE_WRAP_REPEAT).
        """
        if key in self.textures:
            return self.textures[key]

        texture = rl.load_texture(path)
        if wrap_mode is not None:
            rl.set_texture_wrap(texture, wrap_mode)
        self.textures[key] = texture
        return texture

    def load_mesh_model(self, key, mesh_func, *mesh_args):
        if key in self.models:
            return self.models[key]

        mesh = mesh_func(*mesh_args)  # e.g. gen_mesh_plane(...)
        self.meshes[key] = mesh

        model = rl.load_model_from_mesh(mesh)
        self.models[key] = model
        return model

    def get_texture(self, key):
        """Retrieve a previously loaded texture by key (or None if not found)."""
        return self.textures.get(key)

    def get_model(self, key):
        """Retrieve a previously loaded model by key (or None if not found)."""
        return self.models.get(key)

    def unload_all(self):
        """Unload all tracked resources from memory."""
        for tex in self.textures.values():
            rl.unload_texture(tex)
        for model in self.models.values():
            rl.unload_model(model)
        # If needed, unload meshes as well (though unloading the Model often covers it).
        self.textures.clear()
        self.models.clear()
        self.meshes.clear()
