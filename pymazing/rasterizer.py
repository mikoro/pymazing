"""
Primitive shape rasterization.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
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
    color_value = color.get_value()
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
    color_value = color.get_value()
    pixel_data = framebuffer.pixel_data
    middle_line_drawn = False

    if y0 != y1:
        left_delta = (x1 - x0) / float(y1 - y0)
        right_delta = (x2 - x0) / float(y2 - y0)

        if left_delta > right_delta:
            left_delta, right_delta = right_delta, left_delta

        left_x = x0
        right_x = x0
        middle_line_drawn = True

        for y in range(y0, y1 + 1):
            index = y * width
            left_index = index + int(left_x + 0.5)
            right_index = index + int(right_x + 0.5)

            for x in range(left_index, right_index + 1):
                pixel_data[x] = color_value

            left_x += left_delta
            right_x += right_delta

    if y1 != y2:
        left_delta = -(x1 - x2) / float(y1 - y2)
        right_delta = -(x0 - x2) / float(y0 - y2)

        if left_delta > right_delta:
            left_delta, right_delta = right_delta, left_delta

        left_x = x2
        right_x = x2

        if middle_line_drawn:
            y1 += 1

        for y in reversed(range(y1, y2 + 1)):
            index = y * width
            left_index = index + int(left_x + 0.5)
            right_index = index + int(right_x + 0.5)

            for x in range(left_index, right_index + 1):
                pixel_data[x] = color_value

            left_x += left_delta
            right_x += right_delta
