"""
Simple rotating cube.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

from pymazing import world, mesh, color, light, euler_angle, camera, renderer


class GameStateSimpleCube:
    def __init__(self, config):
        self.world = world.World()
        self.world.meshes = [mesh.create_cube(color.from_int(255, 215, 0))]
        self.world.ambient_light.color = color.from_int(255, 255, 255)
        self.world.ambient_light.intensity = 0.2

        diffuse_light = light.Light()
        diffuse_light.color = color.from_int(255, 255, 255)
        diffuse_light.euler_angle = euler_angle.EulerAngle(-20.0, 30.0, 0)
        diffuse_light.intensity = 0.6

        specular_light = light.Light()
        specular_light.color = color.from_int(255, 255, 255)
        specular_light.euler_angle = euler_angle.EulerAngle(-20.0, 30.0, 0)
        specular_light.intensity = 0.6
        specular_light.shininess = 4.0

        self.world.diffuse_lights.append(diffuse_light)
        self.world.specular_lights.append(specular_light)

        self.camera = camera.Camera(config)
        self.camera.position[0] = 3
        self.camera.position[1] = 3
        self.camera.position[2] = 3
        self.camera.euler_angle = euler_angle.EulerAngle(-40.0, 45.0, 0)

        self.render_wireframe = False

    def update(self, time_step, mouse_delta):
        self.camera.update(time_step, mouse_delta)

    def render(self, framebuffer, interpolation):
        if self.render_wireframe:
            renderer.render_as_wireframe(self.world, self.camera, framebuffer)
        else:
            renderer.render_as_solid(self.world, self.camera, framebuffer)
