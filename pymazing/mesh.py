"""
Mesh that defines a shape in 3D.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import numpy as np


class Mesh:
    def __init__(self):
        self.vertices = []
        self.indices = []
        self.scale = [1.0, 1.0, 1.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.position = [0.0, 0.0, 0.0]
        self.radius = 1.0
        self.aabb = None


def create_cube():
    mesh = Mesh()
    mesh.vertices = np.array([[-1.0, -1.0, 1.0, 1.0],
                              [1.0, -1.0, 1.0, 1.0],
                              [1.0, -1.0, -1.0, 1.0],
                              [-1.0, -1.0, -1.0, 1.0],
                              [-1.0, 1.0, 1.0, 1.0],
                              [1.0, 1.0, 1.0, 1.0],
                              [1.0, 1.0, -1.0, 1.0],
                              [-1.0, 1.0, -1.0, 1.0]])

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

    return mesh
