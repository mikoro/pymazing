"""
Color unit tests.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

from pymazing import color


def test_get_value():
    my_color = color.Color(0xaa, 0xbb, 0xcc, 0xff)
    value = my_color.get_value()
    assert value == 0xffccbbaa
