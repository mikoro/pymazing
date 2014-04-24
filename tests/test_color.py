"""Color unit tests."""
# Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
# License: MIT, see the LICENSE file.

from pymazing import color


def test_get_uint32_value():
    my_color = color.from_int(0xaa, 0xbb, 0xcc, 0xff)
    value = my_color.get_uint32_value()
    assert value == 0xffccbbaa
