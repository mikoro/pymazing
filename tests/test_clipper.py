"""Clipper unit tests."""
# Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
# License: MIT, see the LICENSE file.

import numpy as np

from pymazing import clipper, color


def test_clip_view_space_triangle_by_z():
    v0 = np.array([0.0, 1.0, -15.0, 1.0])
    v1 = np.array([-3.0, 1.0, 2.0, 1.0])
    v2 = np.array([3.0, 1.0, 3.0, 1.0])
    triangle = (v0, v1, v2, None)
    triangles = clipper.clip_view_space_triangle_by_z(triangle, 1.0, 10.0)

    assert len(triangles) == 2
    assert triangles[0][0][2] == -1
    assert triangles[0][1][2] == -10
    assert triangles[1][0][2] == -1
    assert triangles[1][1][2] == -10


def test_clip_screen_space_triangle():
    triangle = (np.array([40.0, -30.0, 1.0]), np.array([-40.0, 20.0, 1.0]), np.array([-80.0, -40.0, 1.0]), color.from_int(255, 255, 255), 1.0)
    triangles = clipper.clip_screen_space_triangle(triangle, 100, 100)

    assert triangles is None
