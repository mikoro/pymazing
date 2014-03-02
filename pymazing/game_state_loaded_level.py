"""
Level loaded from a file.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

from pymazing import world, level_loader, color, light, euler_angle, camera, coordinate_grid, renderer


class GameStateLoadedLevel:
    def __init__(self, config):
        self.world = world.World()
        blocks = level_loader.generate_blocks_from_tga(config["game"]["level_file"])
        self.world.meshes = level_loader.generate_partial_meshes(blocks)
        self.world.ambient_light.color = color.from_int(255, 255, 255)
        self.world.ambient_light.intensity = 0.2

        diffuse_light = light.Light()
        diffuse_light.color = color.from_int(255, 255, 255)
        diffuse_light.euler_angle = euler_angle.EulerAngle(-20.0, 30.0, 0)
        diffuse_light.intensity = 0.6

        specular_light = light.Light()
        specular_light.color = color.from_int(255, 255, 255)
        specular_light.euler_angle = euler_angle.EulerAngle(-20.0, 30.0, 0)
        specular_light.intensity = 0.8
        specular_light.shininess = 4.0

        self.world.diffuse_lights.append(diffuse_light)
        #self.world.specular_lights.append(specular_light)

        self.camera = camera.Camera(config)
        self.camera.position[0] = 3
        self.camera.position[1] = 3
        self.camera.position[2] = 6

        self.coordinate_grid = coordinate_grid.CoordinateGrid()

        self.render_coordinate_grid = True
        self.render_wireframe = False

    def update(self, time_step, mouse_delta):
        self.camera.update(time_step, mouse_delta)

    def render(self, framebuffer, interpolation):
        if self.render_coordinate_grid:
            self.coordinate_grid.render(self.camera, framebuffer)

        if self.render_wireframe:
            renderer.render_as_wireframe(self.world, self.camera, framebuffer)
        else:
            renderer.render_as_solid(self.world, self.camera, framebuffer)
