"""RGB color handling."""
# Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
# License: MIT, see the LICENSE file.

import numpy as np


class Color:
    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0):
        """
        :param float r: The red channel.
        :param float g: The green channel.
        :param float b: The blue channel.
        :param float a: The alpha channel.
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.assert_values()

    def get_vector(self):
        """
        Convert color data into a numpy vector.
        """
        return np.array([self.r, self.g, self.b, self.a])

    def get_uint32_value(self):
        """
        Convert color data into a 32 bit integer (in the format 0xAABBGGRR).
        """
        self.assert_values()
        return np.uint32(int(self.a * 255.0 + 0.5) << 24 | int(self.b * 255.0 + 0.5) << 16 | int(self.g * 255.0 + 0.5) << 8 | int(self.r * 255.0 + 0.5))

    def assert_values(self):
        assert self.r >= 0.0 and self.r <= 1.0 and self.g >= 0.0 and self.g <= 1.0 and self.b >= 0.0 and self.b <= 1.0 and self.a >= 0.0 and self.a <= 1.0


def from_int(r, g, b, a=255):
    """
    Create a new color instance from integer values ranging from 0 to 255.
    """
    return Color(float(r) / 255.0, float(g) / 255.0, float(b) / 255.0, float(a) / 255.0)


def from_vector(rgba):
    """
    Create a new color instance from a four dimensional vector.
    """
    return Color(rgba[0], rgba[1], rgba[2], rgba[3])
