"""
Load level data from a file.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

from pymazing import color


class LevelLoader:
    def load_block_data(self, file_name):
        blocks = []

        # http://en.wikipedia.org/wiki/Truevision_TGA
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
                        blocks.append(((x, y), color.Color(r, g, b, a)))

        return blocks
