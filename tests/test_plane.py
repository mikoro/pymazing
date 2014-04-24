"""Plane unit tests."""
# Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
# License: MIT, see the LICENSE file.

import numpy as np

from pymazing import plane


def test_point_distance():
    my_plane = plane.Plane()
    my_plane.setup_from_points(np.array([0.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0]), np.array([0.0, 0.0, -1.0]))

    assert my_plane.point_distance(np.array([0.0, 1.0, 0.0])) > 0.0
    assert my_plane.point_distance(np.array([0.0, -1.0, 0.0])) < 0.0
