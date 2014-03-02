"""
First person style camera.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import sfml as sf
import numpy as np

from pymazing import euler_angle, matrix, frustum


class Camera:
    def __init__(self, config):
        self.position = np.array([0.0, 0.0, 0.0])
        self.forward_vector = np.array([0.0, 0.0, -1.0])
        self.up_vector = np.array([0.0, 1.0, 0.0])
        self.right_vector = np.array([1.0, 0.0, 0.0])
        self.view_matrix = np.identity(4)
        self.projection_matrix = np.identity(4)
        self.euler_angle = euler_angle.EulerAngle()
        self.frustum = frustum.Frustum()
        self.vertical_fov = 70.0
        self.aspect_ratio = 1.0
        self.near_z = 0.1
        self.far_z = 100.0
        self.slow_movement_speed = 1.0
        self.normal_movement_speed = 2.0
        self.fast_movement_speed = 5.0
        self.mouse_sensitivity = float(config["game"]["mouse_sensitivity"])

    def update_projection_matrix(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio
        self.projection_matrix = matrix.create_projection_matrix(self.vertical_fov, self.aspect_ratio, self.near_z, self.far_z)

    def update(self, time_step, mouse_delta):
        self.euler_angle.pitch += mouse_delta.y * self.mouse_sensitivity * time_step
        self.euler_angle.yaw += mouse_delta.x * self.mouse_sensitivity * time_step

        if self.euler_angle.pitch > 89.0:
            self.euler_angle.pitch = 89.0

        if self.euler_angle.pitch < -89.0:
            self.euler_angle.pitch = -89.0

        self.forward_vector = self.euler_angle.get_direction_vector()
        self.right_vector = np.cross(self.forward_vector, [0.0, 1.0, 0.0])
        self.right_vector /= np.linalg.norm(self.right_vector)
        self.up_vector = np.cross(self.right_vector, self.forward_vector)
        self.up_vector /= np.linalg.norm(self.up_vector)

        if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT) or sf.Keyboard.is_key_pressed(sf.Keyboard.R_SHIFT):
            movement_speed = self.fast_movement_speed
        elif sf.Keyboard.is_key_pressed(sf.Keyboard.L_CONTROL) or sf.Keyboard.is_key_pressed(sf.Keyboard.R_CONTROL):
            movement_speed = self.slow_movement_speed
        else:
            movement_speed = self.normal_movement_speed

        if sf.Keyboard.is_key_pressed(sf.Keyboard.W) or sf.Keyboard.is_key_pressed(sf.Keyboard.UP):
            self.position += self.forward_vector * movement_speed * time_step

        if sf.Keyboard.is_key_pressed(sf.Keyboard.S) or sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN):
            self.position -= self.forward_vector * movement_speed * time_step

        if sf.Keyboard.is_key_pressed(sf.Keyboard.D) or sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
            self.position += self.right_vector * movement_speed * time_step

        if sf.Keyboard.is_key_pressed(sf.Keyboard.A) or sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
            self.position -= self.right_vector * movement_speed * time_step

        if sf.Keyboard.is_key_pressed(sf.Keyboard.E):
            self.position += self.up_vector * movement_speed * time_step

        if sf.Keyboard.is_key_pressed(sf.Keyboard.Q):
            self.position -= self.up_vector * movement_speed * time_step

        self.frustum.setup_from_camera(self)

        rotation_x_matrix = matrix.create_rotation_matrix_x(-self.euler_angle.get_pitch_radians())
        rotation_y_matrix = matrix.create_rotation_matrix_y(-self.euler_angle.get_yaw_radians())
        translation_matrix = matrix.create_translation_matrix(-self.position[0], -self.position[1], -self.position[2])

        self.view_matrix = rotation_x_matrix.dot(rotation_y_matrix).dot(translation_matrix)
