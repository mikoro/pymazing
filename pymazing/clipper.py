"""
Clipping algorithms for lines and triangles.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import numpy as np

INSIDE = 0b000000  # 0
BACK = 0b100000  # 32
FRONT = 0b010000  # 16
TOP = 0b001000  # 8
BOTTOM = 0b000100  # 4
RIGHT = 0b000010  # 2
LEFT = 0b000001  # 1


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

    outcode_v0 = calculate_outcode(vc0)
    outcode_v1 = calculate_outcode(vc1)

    while True:
        if (outcode_v0 & outcode_v1) != 0:
            return None

        if (outcode_v0 | outcode_v1) == 0:
            return [vc0, vc1]

        if outcode_v0 != 0:
            outcode_selected = outcode_v0
        else:
            outcode_selected = outcode_v1

        x0 = vc0[0]
        y0 = vc0[1]
        z0 = vc0[2]
        w0 = vc0[3]
        x1 = vc1[0]
        y1 = vc1[1]
        z1 = vc1[2]
        w1 = vc1[3]

        x = 0.0
        y = 0.0
        z = 0.0
        w = 0.0

        if (outcode_selected & TOP) != 0:
            u = (y0 - w0) / ((y0 - w0) - (y1 - w1))
            u = np.clip(u, 0.01, 0.99)
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            z = z0 + (z1 - z0) * u
            w = w0 + (w1 - w0) * u

        if (outcode_selected & BOTTOM) != 0:
            u = (y0 + w0) / ((y0 + w0) - (y1 + w1))
            u = np.clip(u, 0.01, 0.99)
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            z = z0 + (z1 - z0) * u
            w = w0 + (w1 - w0) * u

        if (outcode_selected & RIGHT) != 0:
            u = (x0 - w0) / ((x0 - w0) - (x1 - w1))
            u = np.clip(u, 0.01, 0.99)
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            z = z0 + (z1 - z0) * u
            w = w0 + (w1 - w0) * u

        if (outcode_selected & LEFT) != 0:
            u = (x0 + w0) / ((x0 + w0) - (x1 + w1))
            u = np.clip(u, 0.01, 0.99)
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            z = z0 + (z1 - z0) * u
            w = w0 + (w1 - w0) * u

        if (outcode_selected & BACK) != 0:
            u = (z0 - w0) / ((z0 - w0) - (z1 - w1))
            u = np.clip(u, 0.01, 0.99)
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            z = z0 + (z1 - z0) * u
            w = w0 + (w1 - w0) * u

        if (outcode_selected & FRONT) != 0:
            u = (z0 + w0) / ((z0 + w0) - (z1 + w1))
            u = np.clip(u, 0.01, 0.99)
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            z = z0 + (z1 - z0) * u
            w = w0 + (w1 - w0) * u

        if outcode_selected == outcode_v0:
            vc0[0] = x
            vc0[1] = y
            vc0[2] = z
            vc0[3] = w

            outcode_v0 = calculate_outcode(vc0)
        else:
            vc1[0] = x
            vc1[1] = y
            vc1[2] = z
            vc1[3] = w

            outcode_v1 = calculate_outcode(vc1)


def clip_triangle_3d(v0, v1, v2):
    vertices = []
    return vertices
