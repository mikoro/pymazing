"""Simple Light representation."""
# Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
# License: MIT, see the LICENSE file.

import numpy as np

from pymazing import color


class Light:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0, 1.0])
        self.color = color.from_int(255, 255, 255)
        self.intensity = 1.0
        self.shininess = 1.0
