"""
Clipping algorithms for lines and triangles in three dimensions.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

INSIDE = 0

VIEW_SPACE_FRONT = 1
VIEW_SPACE_BACK = 2

SCREEN_SPACE_TOP = 1
SCREEN_SPACE_BOTTOM = 2
SCREEN_SPACE_LEFT = 4
SCREEN_SPACE_RIGHT = 8


def calculate_view_space_outcode_by_z(vertex, near_z, far_z, clip_far):
    z = vertex[2]

    outcode = INSIDE

    if z > -near_z:
        outcode |= VIEW_SPACE_FRONT

    if clip_far and (z < -far_z):
        outcode |= VIEW_SPACE_BACK

    return outcode


def calculate_screen_space_outcode(vertex, screen_width, screen_height):
    x = vertex[0]
    y = vertex[1]

    outcode = INSIDE

    if x < 0.0:
        outcode |= SCREEN_SPACE_LEFT

    if x > screen_width:
        outcode |= SCREEN_SPACE_RIGHT

    if y < 0.0:
        outcode |= SCREEN_SPACE_BOTTOM

    if y > screen_height:
        outcode |= SCREEN_SPACE_TOP

    return outcode


def clip_view_space_line_by_z(line, near_z, far_z, clip_far=True):
    v0 = line[0]
    v1 = line[1]

    outcode_v0 = calculate_view_space_outcode_by_z(v0, near_z, far_z, clip_far)
    outcode_v1 = calculate_view_space_outcode_by_z(v1, near_z, far_z, clip_far)

    # completely outside
    if (outcode_v0 & outcode_v1) != 0:
        return None

    # completely inside
    if (outcode_v0 | outcode_v1) == 0:
        return line

    v0 = v0.copy()
    v1 = v1.copy()

    # front plane
    if v0[2] < -near_z:
        if v1[2] > -near_z:
            k = (-near_z - v0[2]) / (v1[2] - v0[2])
            v1 = v0 + k * (v1 - v0)
    elif v1[2] < -near_z:
        k = (-near_z - v0[2]) / (v1[2] - v0[2])
        v0 = v0 + k * (v1 - v0)

    if clip_far:
        # back plane
        if v0[2] > -far_z:
            if v1[2] < -far_z:
                k = (-far_z - v0[2]) / (v1[2] - v0[2])
                v1 = v0 + k * (v1 - v0)
        elif v1[2] > -far_z:
            k = (-far_z - v0[2]) / (v1[2] - v0[2])
            v0 = v0 + k * (v1 - v0)

    return (v0, v1, line[2])


def clip_view_space_triangle_by_z(triangle, near_z, far_z, clip_far=True):
    v0 = triangle[0]
    v1 = triangle[1]
    v2 = triangle[2]

    outcode_v0 = calculate_view_space_outcode_by_z(v0, near_z, far_z, clip_far)
    outcode_v1 = calculate_view_space_outcode_by_z(v1, near_z, far_z, clip_far)
    outcode_v2 = calculate_view_space_outcode_by_z(v2, near_z, far_z, clip_far)

    # completely outside
    if (outcode_v0 & outcode_v1 & outcode_v2) != 0:
        return None

    # completely inside
    if (outcode_v0 | outcode_v1 | outcode_v2) == 0:
        return [triangle]

    input_vertices = [v0, v1, v2]
    output_vertices = []
    vp = input_vertices[-1]

    # front plane
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

    if clip_far:
        input_vertices = output_vertices
        output_vertices = []
        vp = input_vertices[-1]

        # back plane
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

    # triangulate the resulted convex polygon
    for i in range(1, len(output_vertices) - 1):
        triangles.append((output_vertices[0], output_vertices[i], output_vertices[i + 1], color))

    return triangles


def clip_screen_space_line(line, screen_width, screen_height):
    return line


def clip_screen_space_triangle(triangle, screen_width, screen_height):
    v0 = triangle[0]
    v1 = triangle[1]
    v2 = triangle[2]

    outcode_v0 = calculate_screen_space_outcode(v0, screen_width, screen_height)
    outcode_v1 = calculate_screen_space_outcode(v1, screen_width, screen_height)
    outcode_v2 = calculate_screen_space_outcode(v2, screen_width, screen_height)

    # completely outside
    if (outcode_v0 & outcode_v1 & outcode_v2) != 0:
        return None

    # completely inside
    if (outcode_v0 | outcode_v1 | outcode_v2) == 0:
        return [triangle]

    input_vertices = [v0, v1, v2]
    output_vertices = []
    vp = input_vertices[-1]

    # screen left edge
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

    # screen right edge
    for vc in input_vertices:
        if vc[0] < screen_width:
            if vp[0] > screen_width:
                k = (screen_width - vc[0]) / (vp[0] - vc[0])
                output_vertices.append(vc + k * (vp - vc))
            output_vertices.append(vc)
        elif vp[0] < screen_width:
            k = (screen_width - vc[0]) / (vp[0] - vc[0])
            output_vertices.append(vc + k * (vp - vc))

        vp = vc

    input_vertices = output_vertices
    output_vertices = []
    vp = input_vertices[-1]

    # screen bottom edge
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

    # triangle is completely below the bottom edge
    if len(output_vertices) == 0:
        return None

    input_vertices = output_vertices
    output_vertices = []
    vp = input_vertices[-1]

    # screen top edge
    for vc in input_vertices:
        if vc[1] < screen_height:
            if vp[1] > screen_height:
                k = (screen_height - vc[1]) / (vp[1] - vc[1])
                output_vertices.append(vc + k * (vp - vc))
            output_vertices.append(vc)
        elif vp[1] < screen_height:
            k = (screen_height - vc[1]) / (vp[1] - vc[1])
            output_vertices.append(vc + k * (vp - vc))

        vp = vc

    # triangle is completely above the top edge
    if len(output_vertices) == 0:
        return None

    triangles = []
    color = triangle[3]

    # triangulate the resulted convex polygon
    for i in range(1, len(output_vertices) - 1):
        v0 = output_vertices[0]
        v1 = output_vertices[i]
        v2 = output_vertices[i + 1]

        min_z = min(min(v0[2], v1[2]), v2[2])

        triangles.append((v0, v1, v2, color, min_z))

    return triangles
