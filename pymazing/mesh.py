"""
Mesh that defines a shape in 3D.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

from math import *

import numpy as np

from pymazing import matrix


class Mesh:
    def __init__(self):
        self.vertices = []
        self.colors = []
        self.indices = []
        self.scale = [1.0, 1.0, 1.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.translation = [0.0, 0.0, 0.0]
        self.world_matrix = np.identity(4)
        self.bounding_radius = 1.0

    def calculate_bounding_radius(self):
        max_distance_squared = 0.0

        for vertex in self.vertices:
            max_distance_squared = max(max_distance_squared, vertex[0] * vertex[0] + vertex[1] * vertex[1] + vertex[2] * vertex[2])

        self.bounding_radius = sqrt(max_distance_squared)

    def calculate_world_matrix(self):
        scale_matrix = matrix.create_scale_matrix(self.scale[0], self.scale[1], self.scale[2])
        rotation_x_matrix = matrix.create_rotation_matrix_x(self.rotation[0])
        rotation_y_matrix = matrix.create_rotation_matrix_y(self.rotation[1])
        rotation_z_matrix = matrix.create_rotation_matrix_z(self.rotation[2])
        translation_matrix = matrix.create_translation_matrix(self.translation[0], self.translation[1], self.translation[2])

        self.world_matrix = scale_matrix.dot(rotation_x_matrix).dot(rotation_y_matrix).dot(rotation_z_matrix).dot(translation_matrix)


def create_cube(color):
    mesh = Mesh()
    mesh.vertices = np.array([[-1.0, -1.0, 1.0, 1.0],
                              [1.0, -1.0, 1.0, 1.0],
                              [1.0, -1.0, -1.0, 1.0],
                              [-1.0, -1.0, -1.0, 1.0],
                              [-1.0, 1.0, 1.0, 1.0],
                              [1.0, 1.0, 1.0, 1.0],
                              [1.0, 1.0, -1.0, 1.0],
                              [-1.0, 1.0, -1.0, 1.0]])

    mesh.colors = [color] * 8

    mesh.indices = [[0, 1, 5],
                    [0, 5, 4],
                    [1, 2, 5],
                    [2, 6, 5],
                    [3, 3, 6],
                    [3, 7, 6],
                    [3, 4, 7],
                    [3, 0, 4],
                    [4, 5, 6],
                    [4, 6, 7],
                    [0, 3, 2],
                    [0, 2, 1]]

    mesh.calculate_bounding_radius()

    return mesh
