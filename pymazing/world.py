"""
The world contains all objects (meshes) and other relevant data.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

from pymazing import color, euler_angle


class World:
    def __init__(self, meshes):
        self.meshes = meshes
        self.ambient_light_color = color.from_int(255, 255, 255)
        self.ambient_light_intensity = 0.3
        self.diffuse_light_color = color.from_int(255, 255, 255)
        self.diffuse_light_intensity = 0.8
        self.diffuse_light_angle = euler_angle.EulerAngle(-45.0, 45.0, 0)

