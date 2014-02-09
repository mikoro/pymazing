"""
Basic primitives.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import numpy as np

class Point:
    def __init__(self, x, y, z, w = 1.0):
        self.data = np.array([x, y, z, w])

class Triangle:
    def __init__(self, p0, p1, p2, color):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.color = color

def create_cube(color):
    triangles = []

    triangles.append(Triangle(Point(-1.0, -1.0, -1.0), Point(1.0, -1.0, -1.0), Point(1.0, 1.0, -1.0), color))
    triangles.append(Triangle(Point(-1.0, -1.0, -1.0), Point(1.0, 1.0, -1.0), Point(-1.0, 1.0, -1.0), color))

    triangles.append(Triangle(Point(1.0, -1.0, 1.0), Point(1.0, 1.0, -1.0), Point(1.0, -1.0, -1.0), color))
    triangles.append(Triangle(Point(1.0, -1.0, 1.0), Point(1.0, 1.0, 1.0), Point(1.0, 1.0, -1.0), color))

    triangles.append(Triangle(Point(-1.0, -1.0, 1.0), Point(1.0, 1.0, 1.0), Point(1.0, -1.0, 1.0), color))
    triangles.append(Triangle(Point(-1.0, -1.0, 1.0), Point(-1.0, 1.0, 1.0), Point(1.0, 1.0, 1.0), color))

    triangles.append(Triangle(Point(-1.0, -1.0, 1.0), Point(-1.0, -1.0, -1.0), Point(-1.0, 1.0, -1.0), color))
    triangles.append(Triangle(Point(-1.0, -1.0, 1.0), Point(-1.0, 1.0, -1.0), Point(-1.0, 1.0, 1.0), color))

    triangles.append(Triangle(Point(-1.0, 1.0, -1.0), Point(1.0, 1.0, -1.0), Point(1.0, 1.0, 1.0), color))
    triangles.append(Triangle(Point(-1.0, 1.0, -1.0), Point(1.0, 1.0, 1.0), Point(-1.0, 1.0, 1.0), color))

    triangles.append(Triangle(Point(-1.0, -1.0, -1.0), Point(1.0, -1.0, 1.0), Point(1.0, -1.0, -1.0), color))
    triangles.append(Triangle(Point(-1.0, -1.0, -1.0), Point(-1.0, -1.0, 1.0), Point(1.0, -1.0, 1.0), color))

    return triangles
