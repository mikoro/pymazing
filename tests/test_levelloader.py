"""
LevelLoader unit tests.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

from pymazing import level_loader as ll


def ttest_load_block_data():
    loader = ll.LevelLoader()
    blocks = loader.load_block_data("data/level_simple.tga")
    assert len(blocks) == 4
    assert blocks[0][0] == (0, 0)
    assert blocks[1][0] == (2, 1)
    assert blocks[2][0] == (1, 2)
    assert blocks[3][0] == (3, 3)
    assert blocks[1][1].r == 60
    assert blocks[1][1].g == 120
    assert blocks[1][1].b == 180
    assert blocks[1][1].a == 128
