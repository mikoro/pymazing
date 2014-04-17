"""LevelLoader unit tests."""
# Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
# License: MIT, see the LICENSE file.

from pymazing import level_loader, color


def test_generate_blocks_from_tga():
    blocks = level_loader.generate_blocks_from_tga("data/level_simple.tga")

    assert len(blocks) == 4
    assert len(blocks[0]) == 4
    assert isinstance(blocks[0][0], color.Color)
    assert blocks[0][1] is None
    assert blocks[0][2] is None
    assert blocks[0][3] is None
    assert blocks[1][0] is None
    assert blocks[1][1] is None
    assert isinstance(blocks[1][2], color.Color)
    assert blocks[1][3] is None
    assert blocks[2][0] is None
    assert isinstance(blocks[2][1], color.Color)
    assert blocks[2][2] is None
    assert blocks[2][3] is None
    assert blocks[3][0] is None
    assert blocks[3][1] is None
    assert blocks[3][2] is None
    assert isinstance(blocks[3][3], color.Color)

    assert blocks[0][0].r == 1.0
    assert blocks[1][2].b == 1.0
    assert blocks[2][1].g == 1.0
    assert blocks[3][3].r == 0.0

def test_generate_full_meshes():
    blocks = level_loader.generate_blocks_from_tga("data/level_simple.tga")
    meshes = level_loader.generate_full_meshes(blocks)

    assert len(meshes) == 5

def test_generate_partial_meshes():
    blocks = level_loader.generate_blocks_from_tga("data/level_simple.tga")
    meshes = level_loader.generate_partial_meshes(blocks)

    assert len(meshes) == 5
