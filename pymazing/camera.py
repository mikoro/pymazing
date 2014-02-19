"""
Camera helper functions.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import numpy as np

from pymazing import math as my_math
from math import *

class Camera:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])
        self.pitch = 0.0
        self.yaw = 0.0
        self.roll = 0.0

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self, value):
        self.position[0] = value

    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, value):
        self.position[1] = value

    @property
    def z(self):
        return self.position[2]

    @z.setter
    def z(self, value):
        self.position[2] = value

    def create_view_matrix(self):
        mrx = my_math.create_rotation_matrix_x(-self.pitch)
        mry = my_math.create_rotation_matrix_y(-self.yaw)
        mrz = my_math.create_rotation_matrix_z(-self.roll)
        mt = my_math.create_translation_matrix(-self.x, -self.y, -self.z)

        return mrx.dot(mry).dot(mrz).dot(mt)

    def get_look_at_vector(self):
        return np.array([-sin(self.yaw)*cos(self.pitch), sin(self.pitch), -cos(self.yaw)*cos(self.pitch)])

    def get_up_vector(self):
        return np.array([0.0, 1.0, 0.0])
