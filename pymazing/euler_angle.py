"""
Euler angle (yaw, pitch, roll) representation.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

from math import *

import numpy as np


class EulerAngle:
    def __init__(self, pitch=0.0, yaw=0.0, roll=0.0):
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

    def get_pitch_radians(self):
        return self.pitch * (pi / 180.0)

    def get_yaw_radians(self):
        return self.yaw * (pi / 180.0)

    def get_roll_radians(self):
        return self.roll * (pi / 180.0)

    def get_direction_vector(self):
        pitch_radians = self.get_pitch_radians()
        yaw_radians = self.get_yaw_radians()

        return np.array([-sin(yaw_radians) * cos(pitch_radians), sin(pitch_radians), -cos(yaw_radians) * cos(pitch_radians)])
