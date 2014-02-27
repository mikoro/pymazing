"""
Simple rotating cube.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import sfml as sf

from pymazing import mesh, world, camera, renderer

class GameStateSimpleCube:
    def __init__(self, config):
        meshes = [mesh.create_multicolor_cube()]
        self.world = world.World(meshes)

        self.camera = camera.Camera(config)
        self.camera.position[0] = 0
        self.camera.position[1] = 0
        self.camera.position[2] = 4

        self.render_wireframe = True

    def update(self, time_step, mouse_delta):
        self.camera.update(time_step, mouse_delta)

    def render(self, framebuffer, interpolation):
        if self.render_wireframe:
            renderer.render_as_wireframe(self.world, self.camera, framebuffer)
        else:
            renderer.render_as_solid(self.world, self.camera, framebuffer)
