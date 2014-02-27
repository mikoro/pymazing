"""
Level loaded from a file.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import sfml as sf

from pymazing import world, camera, level_loader, coordinate_grid, renderer


class GameStateLoadedLevel:
    def __init__(self, config):
        block_data = level_loader.read_block_data_from_tga(config["game"]["level_file"])
        meshes = level_loader.generate_meshes_from_block_data(block_data)
        self.world = world.World(meshes)

        self.camera = camera.Camera(config)
        self.camera.position[0] = 2.5
        self.camera.position[1] = 2
        self.camera.position[2] = 4

        self.coordinate_grid = coordinate_grid.CoordinateGrid()

        self.render_coordinate_grid = True
        self.render_wireframe = True

    def update(self, time_step, mouse_delta):
        self.camera.update(time_step, mouse_delta)

    def render(self, framebuffer, interpolation):
        if self.render_coordinate_grid:
            self.coordinate_grid.render(self.camera, framebuffer)

        if self.render_wireframe:
            renderer.render_as_wireframe(self.world, self.camera, framebuffer)
        else:
            renderer.render_as_solid(self.world, self.camera, framebuffer)
