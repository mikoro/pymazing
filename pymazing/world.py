"""Data describing the world."""
# Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
# License: MIT, see the LICENSE file.

from pymazing import light


class World:
    def __init__(self):
        self.ambient_light = light.Light()
        self.diffuse_lights = []
        self.specular_lights = []
        self.ambient_light_enabled = True
        self.diffuse_lights_enabled = True
        self.specular_lights_enabled = False
