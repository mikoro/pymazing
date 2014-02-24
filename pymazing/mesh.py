"""
Data that defines a shape in 3D space.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

from math import *
import sys

import numpy as np

from pymazing import matrix, color


class Mesh:
    def __init__(self):
        self.vertices = []
        self.world_vertices = []
        self.clip_vertices = []
        self.colors = []
        self.indices = []
        self.normals = []
        self.scale = [1.0, 1.0, 1.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.position = [0.0, 0.0, 0.0]
        self.world_matrix = np.identity(4)
        self.bounding_radius = 1.0
        self.maximum_z = sys.float_info.min

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
        translation_matrix = matrix.create_translation_matrix(self.position[0], self.position[1], self.position[2])

        self.world_matrix = translation_matrix.dot(rotation_z_matrix).dot(rotation_y_matrix).dot(rotation_x_matrix).dot(scale_matrix)


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

    mesh.colors = [color] * 12

    mesh.indices = [[0, 1, 5],
                    [0, 5, 4],
                    [1, 2, 6],
                    [1, 6, 5],
                    [2, 3, 7],
                    [2, 7, 6],
                    [7, 3, 0],
                    [7, 0, 4],
                    [4, 5, 6],
                    [4, 6, 7],
                    [3, 2, 1],
                    [3, 1, 0]]

    mesh.calculate_bounding_radius()

    return mesh


def create_multicolor_cube():
    mesh = create_cube(None)

    mesh.colors = [color.create_from_ints(255, 0, 0),
                   color.create_from_ints(255, 0, 0),
                   color.create_from_ints(0, 255, 0),
                   color.create_from_ints(0, 255, 0),
                   color.create_from_ints(0, 0, 255),
                   color.create_from_ints(0, 0, 255),
                   color.create_from_ints(255, 255, 0),
                   color.create_from_ints(255, 255, 0),
                   color.create_from_ints(0, 255, 255),
                   color.create_from_ints(0, 255, 255),
                   color.create_from_ints(255, 255, 255),
                   color.create_from_ints(255, 255, 255)]

    return mesh
