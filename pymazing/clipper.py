"""
Clipping algorithms for lines and triangles.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import sys

INSIDE = 0b000000  # 0
BACK = 0b100000  # 32
FRONT = 0b010000  # 16
TOP = 0b001000  # 8
BOTTOM = 0b000100  # 4
RIGHT = 0b000010  # 2
LEFT = 0b000001  # 1

tolerance = sys.float_info.epsilon * 100.0


def calculate_outcode(vertex):
    outcode = INSIDE

    x = vertex[0]
    y = vertex[1]
    z = vertex[2]
    w = vertex[3]

    if (x + tolerance) < -w:
        outcode |= LEFT
    elif (x - tolerance) > w:
        outcode |= RIGHT

    if (y + tolerance) < -w:
        outcode |= BOTTOM
    elif (y - tolerance) > w:
        outcode |= TOP

    if (z + tolerance) < -w:
        outcode |= FRONT
    elif (z - tolerance) > w:
        outcode |= BACK

    return outcode


def clip_line_3d(v0_in, v1_in):
    v0 = v0_in.copy()
    v1 = v1_in.copy()

    outcode_v0 = calculate_outcode(v0)
    outcode_v1 = calculate_outcode(v1)

    loop_count = 0

    while True:
        loop_count += 1

        # in some cases the loop may get stuck modifying vertices back and forth between two outside states
        # the tolerance value in outcode calculation is supposed to eliminate this
        # every line should be completely clipped in five passes -> abort if too many
        if loop_count >= 6:
            print("Line clipping got stuck!")
            return None

        # both vertices are outside and on the same side -> trivial reject
        if (outcode_v0 & outcode_v1) != 0:
            return None

        # both vertices are inside -> trivial accept
        if (outcode_v0 | outcode_v1) == 0:
            return [v0, v1]

        # select one vertex which is outside
        if outcode_v0 != 0:
            outcode_selected = outcode_v0
        else:
            outcode_selected = outcode_v1

        x0 = v0[0]
        y0 = v0[1]
        z0 = v0[2]
        w0 = v0[3]
        x1 = v1[0]
        y1 = v1[1]
        z1 = v1[2]
        w1 = v1[3]

        u = 0.0
        x = 0.0
        y = 0.0
        z = 0.0
        w = 0.0

        # parametric line equation: p = p0 + (p1 - p0) * u
        # example (top): y_ndc = 1 -> y/w = 1 -> (y0 + (y1 - y0) * u) / (w0 + (w1 - w0) * u) = 1 -> solve for u
        # u will be in [0,1] if there is an intersection of the top plane and the line
        if (outcode_selected & TOP) != 0:
            u = (y0 - w0) / ((y0 - w0) - (y1 - w1))
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            z = z0 + (z1 - z0) * u
            w = w0 + (w1 - w0) * u
        elif (outcode_selected & BOTTOM) != 0:
            u = (y0 + w0) / ((y0 + w0) - (y1 + w1))
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            z = z0 + (z1 - z0) * u
            w = w0 + (w1 - w0) * u
        elif (outcode_selected & RIGHT) != 0:
            u = (x0 - w0) / ((x0 - w0) - (x1 - w1))
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            z = z0 + (z1 - z0) * u
            w = w0 + (w1 - w0) * u
        elif (outcode_selected & LEFT) != 0:
            u = (x0 + w0) / ((x0 + w0) - (x1 + w1))
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            z = z0 + (z1 - z0) * u
            w = w0 + (w1 - w0) * u
        elif (outcode_selected & BACK) != 0:
            u = (z0 - w0) / ((z0 - w0) - (z1 - w1))
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            z = z0 + (z1 - z0) * u
            w = w0 + (w1 - w0) * u
        elif (outcode_selected & FRONT) != 0:
            u = (z0 + w0) / ((z0 + w0) - (z1 + w1))
            x = x0 + (x1 - x0) * u
            y = y0 + (y1 - y0) * u
            z = z0 + (z1 - z0) * u
            w = w0 + (w1 - w0) * u
        else:
            raise Exception("Line clipper logic fail")

        # the intersection point is not between the points (i.e. the line segment is completely out) -> reject
        if u < 0.0 or u > 1.0:
            return None

        # update the selected vertex
        if outcode_selected == outcode_v0:
            v0[0] = x
            v0[1] = y
            v0[2] = z
            v0[3] = w

            outcode_v0 = calculate_outcode(v0)
        else:
            v1[0] = x
            v1[1] = y
            v1[2] = z
            v1[3] = w

            outcode_v1 = calculate_outcode(v1)


def clip_triangle_3d(v0_in, v1_in, v2_in):
    v0 = v0_in.copy()
    v1 = v1_in.copy()
    v2 = v2_in.copy()
    return None
