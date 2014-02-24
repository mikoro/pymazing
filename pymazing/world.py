"""
The world contains all objects (meshes) and other relevant data.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import time
from math import *

from pymazing import color, euler_angle as ea


class World:
    def __init__(self, meshes):
        self.meshes = meshes
        self.ambient_light_color = color.create_from_ints(255, 255, 255)
        self.ambient_light_intensity = 0.3
        self.diffuse_light_color = color.create_from_ints(255, 255, 255)
        self.diffuse_light_intensity = 0.8
        self.diffuse_light_angle = ea.EulerAngle(-45.0, 45.0, 0)

    def update(self, time_step):
        phase = 0.0
        for mesh in self.meshes:
            mesh.scale[0] = (cos(time.clock() + phase) / 2.0 + 2.0) * 10.0 * time_step
            mesh.scale[1] = (cos(time.clock() + phase) / 2.0 + 2.0) * 10.0 * time_step
            mesh.scale[2] = (cos(time.clock() + phase) / 2.0 + 2.0) * 10.0 * time_step
            mesh.rotation[0] = (time.clock() + phase) * 10.0 * time_step
            mesh.rotation[1] = (time.clock() + phase) * 10.0 * time_step
            mesh.rotation[2] = (time.clock() + phase) * 10.0 * time_step
            phase += 1.0
