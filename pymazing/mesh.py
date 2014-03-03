"""
Data that defines a shape in 3D space.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

from math import *

import numpy as np

from pymazing import color, matrix


class Mesh:
    def __init__(self):
        self.vertices = []
        self.colors = []
        self.indices = []
        self.scale = [1.0, 1.0, 1.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.position = [0.0, 0.0, 0.0]
        self.world_matrix = np.identity(4)
        self.bounding_radius = 1.0

    def calculate_bounding_radius(self):
        max_distance_squared = 0.0

        for vertex in self.vertices:
            x = vertex[0] * self.scale[0]
            y = vertex[1] * self.scale[1]
            z = vertex[2] * self.scale[2]

            max_distance_squared = max(max_distance_squared, x * x + y * y + z * z)

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


TOP = 1
BOTTOM = 2
LEFT = 4
RIGHT = 8
FRONT = 16
BACK = 32


def create_partial_cube(color, sides):
    mesh = create_cube(color)
    mesh.indices = []

    if (sides & FRONT) != 0:
        mesh.indices.append([0, 1, 5])
        mesh.indices.append([0, 5, 4])

    if (sides & RIGHT) != 0:
        mesh.indices.append([1, 2, 6])
        mesh.indices.append([1, 6, 5])

    if (sides & BACK) != 0:
        mesh.indices.append([2, 3, 7])
        mesh.indices.append([2, 7, 6])

    if (sides & LEFT) != 0:
        mesh.indices.append([7, 3, 0])
        mesh.indices.append([7, 0, 4])

    if (sides & TOP) != 0:
        mesh.indices.append([4, 5, 6])
        mesh.indices.append([4, 6, 7])

    if (sides & BOTTOM) != 0:
        mesh.indices.append([3, 2, 1])
        mesh.indices.append([3, 1, 0])

    return mesh


def create_multicolor_cube():
    mesh = create_cube(None)

    mesh.colors = [color.from_int(255, 0, 0),
                   color.from_int(255, 0, 0),
                   color.from_int(0, 255, 0),
                   color.from_int(0, 255, 0),
                   color.from_int(0, 0, 255),
                   color.from_int(0, 0, 255),
                   color.from_int(255, 255, 0),
                   color.from_int(255, 255, 0),
                   color.from_int(0, 255, 255),
                   color.from_int(0, 255, 255),
                   color.from_int(255, 255, 255),
                   color.from_int(255, 255, 255)]

    return mesh

