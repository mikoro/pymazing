"""
Render coordinate axles and a horizontal grid to the screen.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import numpy as np

from pymazing import color, clipper, rasterizer


class CoordinateGrid:
    def __init__(self):
        self.coordinate_axle_vertices = []
        self.coordinate_axle_colors = [color.from_int(255, 0, 0), color.from_int(0, 255, 0), color.from_int(255, 255, 255)]
        self.coordinate_axle_length = 10.0

        self.grid_line_vertices = []
        self.grid_line_color = color.from_int(128, 128, 128)
        self.grid_line_length = 10.0
        self.grid_line_step = 0.5
        self.grid_line_count = 20

        self.generate_vertices()

    def generate_vertices(self):
        vertices = [[self.coordinate_axle_length, 0.0, 0.0, 1.0],
                    [-self.coordinate_axle_length, 0.0, 0.0, 1.0],
                    [0.0, self.coordinate_axle_length, 0.0, 1.0],
                    [0.0, -self.coordinate_axle_length, 0.0, 1.0],
                    [0.0, 0.0, self.coordinate_axle_length, 1.0],
                    [0.0, 0.0, -self.coordinate_axle_length, 1.0]]

        self.coordinate_axle_vertices = np.array(vertices)

        vertices = []

        for i in range(-self.grid_line_count, self.grid_line_count + 1):
            vertices.append([i * self.grid_line_step, 0.0, self.grid_line_length, 1.0])
            vertices.append([i * self.grid_line_step, 0.0, -self.grid_line_length, 1.0])
            vertices.append([self.grid_line_length, 0.0, i * self.grid_line_step, 1.0])
            vertices.append([-self.grid_line_length, 0.0, i * self.grid_line_step, 1.0])

        self.grid_line_vertices = np.array(vertices)

    def render(self, camera, framebuffer):
        clip_matrix = camera.projection_matrix.dot(camera.view_matrix)
        coordinate_axle_clip_vertices = []
        grid_line_clip_vertices = []

        for vertex in self.coordinate_axle_vertices:
            clip_vertex = clip_matrix.dot(vertex)
            coordinate_axle_clip_vertices.append(clip_vertex)

        for vertex in self.grid_line_vertices:
            clip_vertex = clip_matrix.dot(vertex)
            grid_line_clip_vertices.append(clip_vertex)

        lines = []

        for i in range(0, self.grid_line_count * 8 + 4, 2):
            lines.append(clipper.clip_line_3d(grid_line_clip_vertices[i], grid_line_clip_vertices[i + 1]))

        for line in lines:
            if line is not None:
                rasterizer.draw_line_clip_space(framebuffer, line[0], line[1], self.grid_line_color)

        lines = []

        lines.append(clipper.clip_line_3d(coordinate_axle_clip_vertices[0], coordinate_axle_clip_vertices[1]))
        lines.append(clipper.clip_line_3d(coordinate_axle_clip_vertices[2], coordinate_axle_clip_vertices[3]))
        lines.append(clipper.clip_line_3d(coordinate_axle_clip_vertices[4], coordinate_axle_clip_vertices[5]))

        for i, line in enumerate(lines):
            if line is not None:
                rasterizer.draw_line_clip_space(framebuffer, line[0], line[1], self.coordinate_axle_colors[i])
