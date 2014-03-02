"""
Rasterize different shapes to the framebuffer.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""


def draw_point(framebuffer, x, y, color):
    framebuffer.pixel_data[y * framebuffer.width + x] = color.get_value()


def draw_line(framebuffer, x0, y0, x1, y1, color):
    steep = (abs(y1 - y0) > abs(x1 - x0))

    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    delta_x = x1 - x0
    delta_y = abs(y1 - y0)
    error = delta_x / 2
    step_y = 1 if (y0 < y1) else -1
    y = y0
    width = framebuffer.width
    color_value = color.get_uint32_value()
    pixel_data = framebuffer.pixel_data

    for x in range(x0, x1 + 1):
        if steep:
            pixel_data[x * width + y] = color_value
        else:
            pixel_data[y * width + x] = color_value

        error -= delta_y

        if error < 0:
            y += step_y
            error += delta_x


def draw_triangle(framebuffer, x0, y0, x1, y1, x2, y2, color):
    if y0 > y1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    if y0 > y2:
        x0, x2 = x2, x0
        y0, y2 = y2, y0

    if y1 > y2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    width = framebuffer.width
    color_value = color.get_uint32_value()
    pixel_data = framebuffer.pixel_data
    middle_line_drawn = False

    # bottom half
    if y0 != y1:
        left_delta = float(x1 - x0) / float(y1 - y0)
        right_delta = float(x2 - x0) / float(y2 - y0)

        if left_delta > right_delta:
            left_delta, right_delta = right_delta, left_delta

        left_x = float(x0)
        right_x = float(x0)
        middle_line_drawn = True

        for y in range(y0, y1 + 1):
            left_index = y * width + int(left_x + 0.5)
            right_index = y * width + int(right_x + 0.5)
            left_x += left_delta
            right_x += right_delta

            for index in range(left_index, right_index + 1):
                pixel_data[index] = color_value

    # top half
    if y1 != y2:
        left_delta = -float(x1 - x2) / float(y1 - y2)
        right_delta = -float(x0 - x2) / float(y0 - y2)

        if left_delta > right_delta:
            left_delta, right_delta = right_delta, left_delta

        left_x = float(x2)
        right_x = float(x2)

        if middle_line_drawn:
            y1 += 1

        for y in reversed(range(y1, y2 + 1)):
            left_index = y * width + int(left_x + 0.5)
            right_index = y * width + int(right_x + 0.5)
            left_x += left_delta
            right_x += right_delta

            for index in range(left_index, right_index + 1):
                pixel_data[index] = color_value


def draw_triangle_z_buffer(framebuffer, x0, y0, z0, x1, y1, z1, x2, y2, z2, color):
    if y0 > y1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
        z0, z1 = z1, z0

    if y0 > y2:
        x0, x2 = x2, x0
        y0, y2 = y2, y0
        z0, z2 = z2, z0

    if y1 > y2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        z1, z2 = z2, z1

    width = framebuffer.width
    color_value = color.get_uint32_value()
    pixel_data = framebuffer.pixel_data
    depth_data = framebuffer.depth_data
    middle_line_drawn = False

    y0_1_delta = float(y1 - y0)
    y0_2_delta = float(y2 - y0)
    y1_2_delta = float(y2 - y1)

    # bottom half
    if y0 != y1:
        left_delta = float(x1 - x0) / float(y1 - y0)
        right_delta = float(x2 - x0) / float(y2 - y0)

        if left_delta > right_delta:
            left_delta, right_delta = right_delta, left_delta

        left_x = float(x0)
        right_x = float(x0)
        middle_line_drawn = True

        for y in range(y0, y1 + 1):
            left_index = y * width + int(left_x + 0.5)
            right_index = y * width + int(right_x + 0.5)
            left_x += left_delta
            right_x += right_delta

            t0_1 = float(y1 - y) / y0_1_delta
            t0_2 = float(y2 - y) / y0_2_delta

            z0_1 = t0_1 * z0 + (1.0 - t0_1) * z1
            z0_2 = t0_2 * z0 + (1.0 - t0_2) * z2

            if x1 > x0:
                z0_1, z0_2 = z0_2, z0_1

            x1_0_delta = float(right_index + 1 - left_index)

            for index in range(left_index, right_index + 1):
                u1_0 = float(right_index - index) / x1_0_delta
                z = u1_0 * z0_1 + (1.0 - u1_0) * z0_2

                if z < depth_data[index]:
                    pixel_data[index] = color_value
                    depth_data[index] = z

    # top half
    if y1 != y2:
        left_delta = -float(x1 - x2) / float(y1 - y2)
        right_delta = -float(x0 - x2) / float(y0 - y2)

        if left_delta > right_delta:
            left_delta, right_delta = right_delta, left_delta

        left_x = float(x2)
        right_x = float(x2)

        if middle_line_drawn:
            y1 += 1

        for y in reversed(range(y1, y2 + 1)):
            left_index = y * width + int(left_x + 0.5)
            right_index = y * width + int(right_x + 0.5)
            left_x += left_delta
            right_x += right_delta

            t1_2 = float(y2 - y) / y1_2_delta
            t0_2 = float(y2 - y) / y0_2_delta

            z1_2 = t1_2 * z1 + (1.0 - t1_2) * z2
            z0_2 = t0_2 * z0 + (1.0 - t0_2) * z2

            if x1 > x0:
                z1_2, z0_2 = z0_2, z1_2

            x1_2_delta = float(right_index + 1 - left_index)

            for index in range(left_index, right_index + 1):
                u1_2 = float(right_index - index) / x1_2_delta
                z = u1_2 * z1_2 + (1.0 - u1_2) * z0_2

                if z < depth_data[index]:
                    pixel_data[index] = color_value
                    depth_data[index] = z
