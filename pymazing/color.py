"""
Color helper functions.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import numpy as np

class Color:
    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def get_value(self):
        return np.uint32(self.a << 24 | self.b << 16 | self.g << 8 | self.r)
