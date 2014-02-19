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
    return mesh
