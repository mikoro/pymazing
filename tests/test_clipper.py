"""
Clipper unit tests.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import numpy as np

from pymazing import clipper


def test_clip_world_space_triangle_by_z():
    v0 = np.array([0.0, 1.0, -15.0, 1.0])
    v1 = np.array([-3.0, 1.0, 2.0, 1.0])
    v2 = np.array([3.0, 1.0, 3.0, 1.0])
    triangle = (v0, v1, v2, None)

    clipper.clip_view_space_triangle_by_z(triangle, 1.0, 10.0)
