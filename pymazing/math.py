"""
Various math functions.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import numpy as np
np.set_printoptions(suppress=True)

from math import *

def create_scale_matrix(sx, sy, sz):
    return np.array([[sx, 0.0, 0.0, 0.0],
                     [0.0, sy, 0.0, 0.0],
                     [0.0, 0.0, sz, 0.0],
                     [0.0, 0.0, 0.0, 1.0]])

def create_rotation_matrix_x(rx):
    return np.array([[1.0, 0.0, 0.0, 0.0],
                     [0.0, cos(rx), -sin(rx), 0.0],
                     [0.0, sin(rx), cos(rx), 0.0],
                     [0.0, 0.0, 0.0, 1.0]])

def create_rotation_matrix_y(ry):
    return np.array([[cos(ry), 0.0, sin(ry), 0.0],
                     [0.0, 1.0, 0.0, 0.0],
                     [-sin(ry), 0.0, cos(ry), 0.0],
                     [0.0, 0.0, 0.0, 1.0]])

def create_rotation_matrix_z(rz):
    return np.array([[cos(rz), -sin(rz), 0.0, 0.0],
                     [sin(rz), cos(rz), 0.0, 0.0],
                     [0.0, 0.0, 1.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0]])

def create_translation_matrix(tx, ty, tz):
    return np.array([[1.0, 0.0, 0.0, tx],
                     [0.0, 1.0, 0.0, ty],
                     [0.0, 0.0, 1.0, tz],
                     [0.0, 0.0, 0.0, 1.0]])

def create_projection_matrix(vertical_fov, aspect_ratio, near_z, far_z):
    f = 1.0 / (tan((vertical_fov / 2.0) * (pi / 180.0)))

    return np.array([[f / aspect_ratio, 0.0, 0.0, 0.0],
                     [0.0, f, 0.0, 0.0],
                     [0.0, 0.0, (near_z + far_z) / (near_z - far_z), (2.0 * near_z * far_z) / (near_z - far_z)],
                     [0.0, 0.0, -1.0, 0.0]])
