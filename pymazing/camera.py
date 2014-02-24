"""
First person style camera.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import sfml as sf
import numpy as np

from pymazing import matrix, euler_angle as ea


class Camera:
    def __init__(self, mouse_sensitivity):
        self.position = np.array([0.0, 0.0, 0.0])
        self.forward_vector = np.array([0.0, 0.0, -1.0])
        self.up_vector = np.array([0.0, 1.0, 0.0])
        self.right_vector = np.array([1.0, 0.0, 0.0])
        self.view_matrix = np.identity(4)
        self.angle = ea.EulerAngle()
        self.normal_movement_scale = 2.0
        self.fast_movement_scale = 5.0
        self.mouse_sensitivity = mouse_sensitivity

    def update(self, time_step, mouse_delta):
        self.angle.pitch += mouse_delta.y * self.mouse_sensitivity * time_step
        self.angle.yaw += mouse_delta.x * self.mouse_sensitivity * time_step
        self.angle.clamp_and_normalize()

        self.forward_vector = self.angle.get_direction_vector()
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

        rotation_x_matrix = matrix.create_rotation_matrix_x(-self.angle.get_pitch_radians())
        rotation_y_matrix = matrix.create_rotation_matrix_y(-self.angle.get_yaw_radians())
        translation_matrix = matrix.create_translation_matrix(-self.position[0], -self.position[1], -self.position[2])

        self.view_matrix = rotation_x_matrix.dot(rotation_y_matrix).dot(translation_matrix)
