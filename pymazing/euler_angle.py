"""
Euler angle helper.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

from math import *

import numpy as np


class EulerAngle:
    def __init__(self):
        self.pitch = 0.0
        self.yaw = 0.0
        self.roll = 0.0

    def clamp_and_normalize(self):
        if self.pitch > 89.0:
            self.pitch = 89.0

        if self.pitch < -89.0:
            self.pitch = -89.0

        while self.yaw > 180.0:
            self.yaw -= 360.0

        while self.yaw < -180.0:
            self.yaw += 360.0

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
