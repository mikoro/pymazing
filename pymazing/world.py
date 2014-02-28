"""
The world contains meshes and other relevant data.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

from pymazing import light


class World:
    def __init__(self):
        self.meshes = []
        self.ambient_light = light.Light()
        self.diffuse_lights = []
        self.specular_lights = []
