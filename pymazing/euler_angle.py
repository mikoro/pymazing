"""Euler angle (yaw, pitch, roll) representation."""
# Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
# License: MIT, see the LICENSE file.

from math import *

import numpy as np


class EulerAngle:
    def __init__(self, pitch=0.0, yaw=0.0, roll=0.0):
        """
        :param float pitch: The pitch in degrees.
        :param float yaw: The yaw in degrees.
        :param float roll: The roll in degrees.
        """
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

    def get_pitch_radians(self):
        """
        Convert the pitch from degrees to radians.
        """
        return self.pitch * (pi / 180.0)

    def get_yaw_radians(self):
        """
        Convert the yaw from degrees to radians.
        """
        return self.yaw * (pi / 180.0)

    def get_roll_radians(self):
        """
        Convert the roll from degrees to radians.
        """
        return self.roll * (pi / 180.0)

    def get_direction_vector(self):
        """
        Convert the euler angle to a direction vector.

        :return: A 3D numpy vector.
        """
        pitch_radians = self.get_pitch_radians()
        yaw_radians = self.get_yaw_radians()

        return np.array([-sin(yaw_radians) * cos(pitch_radians), sin(pitch_radians), -cos(yaw_radians) * cos(pitch_radians)])
