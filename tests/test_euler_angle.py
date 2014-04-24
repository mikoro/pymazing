"""Euler angle unit tests."""
# Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
# License: MIT, see the LICENSE file.

from pymazing import euler_angle


def test_get_direction_vector():
    angle = euler_angle.EulerAngle()
    vector = angle.get_direction_vector()

    assert vector[0] == 0
    assert vector[1] == 0
    assert vector[2] == -1
