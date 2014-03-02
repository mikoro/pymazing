"""
Clipping algorithms for lines and triangles in three dimensions.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
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


VIEW_SPACE_FRONT = 1
VIEW_SPACE_BACK = 2


def calculate_view_space_outcode_by_z(vertex, near_z, far_z):
    z = vertex[2]

    outcode = 0

    if z > -near_z:
        outcode |= VIEW_SPACE_FRONT

    if z < -far_z:
        outcode |= VIEW_SPACE_BACK

    return outcode


def clip_view_space_triangle_by_z(triangle, near_z, far_z):
    v0 = triangle[0]
    v1 = triangle[1]
    v2 = triangle[2]

    outcode_v0 = calculate_view_space_outcode_by_z(v0, near_z, far_z)
    outcode_v1 = calculate_view_space_outcode_by_z(v1, near_z, far_z)
    outcode_v2 = calculate_view_space_outcode_by_z(v2, near_z, far_z)

    # outside
    if (outcode_v0 & outcode_v1 & outcode_v2) != 0:
        return None

    # inside
    if (outcode_v0 | outcode_v1 | outcode_v2) == 0:
        return [triangle]

    input_vertices = [v0, v1, v2]
    output_vertices = []

    vp = input_vertices[-1]

    for vc in input_vertices:
        if vc[2] < -near_z:
            if vp[2] > -near_z:
                k = (-near_z - vc[2]) / (vp[2] - vc[2])
                output_vertices.append(vc + k * (vp - vc))
            output_vertices.append(vc)
        elif vp[2] < -near_z:
            k = (-near_z - vc[2]) / (vp[2] - vc[2])
            output_vertices.append(vc + k * (vp - vc))

        vp = vc

    input_vertices = output_vertices
    output_vertices = []

    vp = input_vertices[-1]

    for vc in input_vertices:
        if vc[2] > -far_z:
            if vp[2] < -far_z:
                k = (-far_z - vc[2]) / (vp[2] - vc[2])
                output_vertices.append(vc + k * (vp - vc))
            output_vertices.append(vc)
        elif vp[2] > -far_z:
            k = (-far_z - vc[2]) / (vp[2] - vc[2])
            output_vertices.append(vc + k * (vp - vc))

        vp = vc

    triangles = []
    color = triangle[3]

    for i in range(1, len(output_vertices) - 1):
        triangles.append((output_vertices[0], output_vertices[i], output_vertices[i + 1], color))

    return triangles


SCREEN_SPACE_TOP = 1
SCREEN_SPACE_BOTTOM = 2
SCREEN_SPACE_LEFT = 4
SCREEN_SPACE_RIGHT = 8


def calculate_screen_space_outcode(vertex, width, height):
    x = vertex[0]
    y = vertex[1]

    outcode = 0

    if x < 0.0:
        outcode |= SCREEN_SPACE_LEFT

    if x > width:
        outcode |= SCREEN_SPACE_RIGHT

    if y < 0.0:
        outcode |= SCREEN_SPACE_BOTTOM

    if y > height:
        outcode |= SCREEN_SPACE_TOP

    return outcode


def clip_screen_space_triangle(triangle, width, height):
    v0 = triangle[0]
    v1 = triangle[1]
    v2 = triangle[2]

    outcode_v0 = calculate_screen_space_outcode(v0, width, height)
    outcode_v1 = calculate_screen_space_outcode(v1, width, height)
    outcode_v2 = calculate_screen_space_outcode(v2, width, height)

    # outside
    if (outcode_v0 & outcode_v1 & outcode_v2) != 0:
        return None

    # inside
    if (outcode_v0 | outcode_v1 | outcode_v2) == 0:
        return [triangle]

    input_vertices = [v0, v1, v2]
    output_vertices = []
    vp = input_vertices[-1]

    for vc in input_vertices:
        if vc[0] > 0.0:
            if vp[0] < 0.0:
                k = (0.0 - vc[0]) / (vp[0] - vc[0])
                output_vertices.append(vc + k * (vp - vc))
            output_vertices.append(vc)
        elif vp[0] > 0.0:
            k = (0.0 - vc[0]) / (vp[0] - vc[0])
            output_vertices.append(vc + k * (vp - vc))

        vp = vc

    input_vertices = output_vertices
    output_vertices = []
    vp = input_vertices[-1]

    for vc in input_vertices:
        if vc[0] < width:
            if vp[0] > width:
                k = (width - vc[0]) / (vp[0] - vc[0])
                output_vertices.append(vc + k * (vp - vc))
            output_vertices.append(vc)
        elif vp[0] < width:
            k = (width - vc[0]) / (vp[0] - vc[0])
            output_vertices.append(vc + k * (vp - vc))

        vp = vc

    input_vertices = output_vertices
    output_vertices = []
    vp = input_vertices[-1]

    for vc in input_vertices:
        if vc[1] > 0.0:
            if vp[1] < 0.0:
                k = (0.0 - vc[1]) / (vp[1] - vc[1])
                output_vertices.append(vc + k * (vp - vc))
            output_vertices.append(vc)
        elif vp[1] > 0.0:
            k = (0.0 - vc[1]) / (vp[1] - vc[1])
            output_vertices.append(vc + k * (vp - vc))

        vp = vc

    # this is a bit of a hack, should check out for a better fix (triangle is completely out)
    if len(output_vertices) == 0:
        return None

    input_vertices = output_vertices
    output_vertices = []
    vp = input_vertices[-1]

    for vc in input_vertices:
        if vc[1] < height:
            if vp[1] > height:
                k = (height - vc[1]) / (vp[1] - vc[1])
                output_vertices.append(vc + k * (vp - vc))
            output_vertices.append(vc)
        elif vp[1] < height:
            k = (height - vc[1]) / (vp[1] - vc[1])
            output_vertices.append(vc + k * (vp - vc))

        vp = vc

    triangles = []
    color = triangle[3]

    for i in range(1, len(output_vertices) - 1):
        v0 = output_vertices[0]
        v1 = output_vertices[i]
        v2 = output_vertices[i + 1]
        min_z = min(min(v0[2], v1[2]), v2[2])

        triangles.append((output_vertices[0], output_vertices[i], output_vertices[i + 1], color, min_z))

    return triangles
