"""
Level loaded from a file.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import sfml as sf

from pymazing import world, level_loader, color, light, camera, coordinate_grid, renderer, matrix


class GameStateLoadedLevel:
    def __init__(self, config):
        self.world = world.World()
        self.world.ambient_light.color = color.from_int(255, 255, 255)
        self.world.ambient_light.intensity = 0.3

        diffuse_light = light.Light()
        diffuse_light.position[0] = 100
        diffuse_light.position[1] = 150
        diffuse_light.position[2] = 50
        diffuse_light.color = color.from_int(255, 255, 255)
        diffuse_light.intensity = 0.4

        specular_light = light.Light()
        specular_light.position[0] = 100
        specular_light.position[1] = 150
        specular_light.position[2] = 59
        specular_light.color = color.from_int(255, 255, 255)
        specular_light.intensity = 0.4
        specular_light.shininess = 8.0

        self.world.diffuse_lights.append(diffuse_light)
        self.world.specular_lights.append(specular_light)

        self.camera = camera.Camera(config)
        self.camera.position[0] = 4
        self.camera.position[1] = 3
        self.camera.position[2] = 6

        blocks = level_loader.generate_blocks_from_tga(config["game"]["level_file"])
        self.meshes = level_loader.generate_partial_meshes(blocks)

        self.coordinate_grid = coordinate_grid.CoordinateGrid()

        self.render_wireframe = False
        self.do_backface_culling = True
        self.render_coordinate_grid = False
        self.rotate_lights = True

        self.key_released = dict()

    def is_key_pressed_once(self, key_code):
        if sf.Keyboard.is_key_pressed(key_code):
            if self.key_released.get(key_code):
                self.key_released[key_code] = False
                return True
        else:
            self.key_released[key_code] = True

        return False

    def update(self, time_step, mouse_delta):
        self.camera.update(time_step, mouse_delta)

        if self.rotate_lights:
            light_rotation_matrix = matrix.create_rotation_matrix_y(0.5 * time_step)
            self.world.diffuse_lights[0].position = light_rotation_matrix.dot(self.world.diffuse_lights[0].position)
            self.world.specular_lights[0].position = light_rotation_matrix.dot(self.world.specular_lights[0].position)

        if self.is_key_pressed_once(sf.Keyboard.F1):
            self.render_wireframe = not self.render_wireframe

        if self.is_key_pressed_once(sf.Keyboard.F2):
            self.do_backface_culling = not self.do_backface_culling

        if self.is_key_pressed_once(sf.Keyboard.F3):
            self.render_coordinate_grid = not self.render_coordinate_grid


        if self.is_key_pressed_once(sf.Keyboard.F5):
            self.world.ambient_light_enabled = not self.world.ambient_light_enabled

        if self.is_key_pressed_once(sf.Keyboard.F6):
            self.world.diffuse_lights_enabled = not self.world.diffuse_lights_enabled

        if self.is_key_pressed_once(sf.Keyboard.F7):
            self.world.specular_lights_enabled = not self.world.specular_lights_enabled

        if self.is_key_pressed_once(sf.Keyboard.F8):
            self.rotate_lights = not self.rotate_lights

    def render(self, framebuffer, interpolation):
        if self.render_coordinate_grid:
            self.coordinate_grid.render(self.camera, framebuffer)

        if self.render_wireframe:
            renderer.render_meshes_wireframe(self.meshes[:1], self.world, self.camera, framebuffer, do_backface_culling=self.do_backface_culling)
            renderer.render_meshes_wireframe(self.meshes[1:], self.world, self.camera, framebuffer, do_backface_culling=self.do_backface_culling)
        else:
            renderer.render_meshes_solid(self.meshes[:1], self.world, self.camera, framebuffer, do_backface_culling=self.do_backface_culling)
            renderer.render_meshes_solid(self.meshes[1:], self.world, self.camera, framebuffer, do_backface_culling=self.do_backface_culling)
