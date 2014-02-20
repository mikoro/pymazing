"""
Camera helper functions.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

from math import *

import sfml as sf
import numpy as np

from pymazing import math as my_math


class Camera:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])
        self.forward_vector = np.array([0.0, 0.0, -1.0])
        self.up_vector = np.array([0.0, 1.0, 0.0])
        self.right_vector = np.array([1.0, 0.0, 0.0])
        self.view_matrix = np.identity(4)
        self.pitch = 0.0
        self.yaw = 0.0
        self.normal_movement_scale = 1.5
        self.fast_movement_scale = 3.0
        self.normal_rotation_scale = 0.05

    def update(self, time_step, mouse_delta):
        self.pitch += mouse_delta.y * self.normal_rotation_scale * time_step
        self.yaw += mouse_delta.x * self.normal_rotation_scale * time_step

        self.forward_vector = np.array([-sin(self.yaw) * cos(self.pitch), sin(self.pitch), -cos(self.yaw) * cos(self.pitch)])
        self.right_vector = np.cross(self.forward_vector, self.up_vector)
        self.right_vector /= np.linalg.norm(self.right_vector)

        if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT) or sf.Keyboard.is_key_pressed(sf.Keyboard.R_SHIFT):
            movement_scale = self.fast_movement_scale
        else:
            movement_scale = self.normal_movement_scale

        if sf.Keyboard.is_key_pressed(sf.Keyboard.W) or sf.Keyboard.is_key_pressed(sf.Keyboard.UP):
            self.position += self.forward_vector * movement_scale * time_step

        if sf.Keyboard.is_key_pressed(sf.Keyboard.S) or sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN):
            self.position -= self.forward_vector * movement_scale * time_step

        if sf.Keyboard.is_key_pressed(sf.Keyboard.D) or sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
            self.position += self.right_vector * movement_scale * time_step

        if sf.Keyboard.is_key_pressed(sf.Keyboard.A) or sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
            self.position -= self.right_vector * movement_scale * time_step

        rotation_x_matrix = my_math.create_rotation_matrix_x(-self.pitch)
        rotation_y_matrix = my_math.create_rotation_matrix_y(-self.yaw)
        translation_matrix = my_math.create_translation_matrix(-self.position[0], -self.position[1], -self.position[2])

        self.view_matrix = rotation_x_matrix.dot(rotation_y_matrix).dot(translation_matrix)
