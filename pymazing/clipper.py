"""
Clipping algorithms for lines and triangles.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

INSIDE = 0b000000 # 0
BACK = 0b100000 # 32
FRONT = 0b010000 # 16
TOP = 0b001000 # 8
BOTTOM = 0b000100 # 4
RIGHT = 0b000010 # 2
LEFT = 0b000001 # 1


def calculate_outcode(v):
    outcode = INSIDE

    if v[0] < -v[3]:
        outcode |= LEFT
    elif v[0] > v[3]:
        outcode |= RIGHT

    if v[1] < -v[3]:
        outcode |= BOTTOM
    elif v[1] > v[3]:
        outcode |= TOP

    if v[2] < -v[3]:
        outcode |= FRONT
    elif v[2] > v[3]:
        outcode |= BACK

    return outcode


def clip_line_3d(v0, v1):
    vc0 = v0.copy()
    vc1 = v1.copy()

    outcode0 = calculate_outcode(vc0)
    outcode1 = calculate_outcode(vc1)

    while True:
        if (outcode0 & outcode1) != 0:
            return None

        if (outcode0 | outcode1) == 0:
            return [vc0, vc1]

        if outcode0 != 0:
            outcode_selected = outcode0
        else:
            outcode_selected = outcode1

        x = 0.0
        y = 0.0
        z = 0.0
        x0 = vc0[0]
        y0 = vc0[1]
        z0 = vc0[2]
        x1 = vc1[0]
        y1 = vc1[1]
        z1 = vc1[2]

        if outcode_selected == outcode0:
            x_min = -vc0[3]
            x_max = vc0[3]
            y_min = -vc0[3]
            y_max = vc0[3]
            z_min = -vc0[3]
            z_max = vc0[3]
        else:
            x_min = -vc1[3]
            x_max = vc1[3]
            y_min = -vc1[3]
            y_max = vc1[3]
            z_min = -vc1[3]
            z_max = vc1[3]

        if (outcode_selected & TOP) != 0:
            x = x0 + (x1 - x0) * (y_max - y0) / (y1 - y0)
            y = y_max
            z = z0 + (z1 - z0) * (y_max - y0) / (y1 - y0)

        if (outcode_selected & BOTTOM) != 0:
            x = x0 + (x1 - x0) * (y_min - y0) / (y1 - y0)
            y = y_min
            z = z0 + (z1 - z0) * (y_min - y0) / (y1 - y0)

        if (outcode_selected & RIGHT) != 0:
            x = x_max
            y = y0 + (y1 - y0) * (x_max - x0) / (x1 - x0)
            z = z0 + (z1 - z0) * (x_max - x0) / (x1 - x0)

        if (outcode_selected & LEFT) != 0:
            x = x_min
            y = y0 + (y1 - y0) * (x_min - x0) / (x1 - x0)
            z = z0 + (z1 - z0) * (x_min - x0) / (x1 - x0)

        if (outcode_selected & BACK) != 0:
            x = x0 + (x1 - x0) * (z_max - z0) / (z1 - z0)
            y = y0 + (y1 - y0) * (z_max - z0) / (z1 - z0)
            z = z_max

        if (outcode_selected & FRONT) != 0:
            x = x0 + (x1 - x0) * (z_min - z0) / (z1 - z0)
            y = y0 + (y1 - y0) * (z_min - z0) / (z1 - z0)
            z = z_min

        if outcode_selected == outcode0:
            vc0[0] = x
            vc0[1] = y
            vc0[2] = z

            outcode0 = calculate_outcode(vc0)
        else:
            vc1[0] = x
            vc1[1] = y
            vc1[2] = z

            outcode1 = calculate_outcode(vc1)


def clip_triangle_3d(v0, v1, v2):
    vertices = []
    return vertices
