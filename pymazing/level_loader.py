"""
Load and generate world mesh data from files.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

from pymazing import color, mesh


# http://en.wikipedia.org/wiki/Truevision_TGA
def generate_blocks_from_tga(file_name):
    blocks = None

    with open(file_name, "rb") as file:
        file.read(1)  # image ID length
        file.read(1)  # color map type

        # image type
        if file.read(1) != b"\x02":
            raise Exception("Invalid file format")

        # color map specification
        file.read(2)
        file.read(2)
        file.read(1)

        file.read(2)  # x-origin
        file.read(2)  # y-origin

        width = int.from_bytes(file.read(2), byteorder="little")
        height = int.from_bytes(file.read(2), byteorder="little")
        depth = file.read(1)[0]

        if width < 1 or height < 1 or depth != 32:
            raise Exception("Invalid file format")

        file.read(1)  # image descriptor

        blocks = [[None] * width for _ in range(height)]

        for y in range(0, height):
            for x in range(0, width):
                pixel_data = file.read(4)

                if len(pixel_data) != 4:
                    raise Exception("Invalid file format")

                r = pixel_data[2]
                g = pixel_data[1]
                b = pixel_data[0]
                a = pixel_data[3]

                if a > 0:
                    blocks[y][x] = color.from_int(r, g, b, a)

    return blocks


def generate_full_meshes(blocks):
    meshes = []
    height = len(blocks)
    width = len(blocks[0])

    for y in range(height):
        for x in range(width):
            color = blocks[y][x]

            if color is not None:
                mesh_ = mesh.create_cube(color)
                mesh_.scale = [0.5, 0.5, 0.5]
                mesh_.position[0] = 1.0 * x + 0.5
                mesh_.position[1] = 0.5
                mesh_.position[2] = -1.0 * y - 0.5
                meshes.append(mesh_)

    return meshes

def generate_partial_meshes(blocks):
    meshes = []
    height = len(blocks)
    width = len(blocks[0])

    for y in range(height):
        for x in range(width):
            color = blocks[y][x]

            if color is not None:
                sides = mesh.TOP

                if x == 0 or (blocks[y][x - 1] is None):
                    sides |= mesh.LEFT

                if x == (width - 1) or (blocks[y][x + 1] is None):
                    sides |= mesh.RIGHT

                if y == 0 or (blocks[y - 1][x] is None):
                    sides |= mesh.FRONT

                if y == (height - 1) or (blocks[y + 1][x] is None):
                    sides |= mesh.BACK

                mesh_ = mesh.create_partial_cube(color, sides)
                mesh_.scale = [0.5, 0.5, 0.5]
                mesh_.position[0] = 1.0 * x + 0.5
                mesh_.position[1] = 0.5
                mesh_.position[2] = -1.0 * y - 0.5
                meshes.append(mesh_)

    return meshes
