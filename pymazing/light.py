"""
Light data.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

from pymazing import color, euler_angle


class Light:
    def __init__(self):
        self.color = color.from_int(255, 255, 255)
        self.euler_angle = euler_angle.EulerAngle()
        self.intensity = 1.0
        self.shininess = 1.0
