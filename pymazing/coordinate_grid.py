"""Render coordinate axles and a horizontal grid to the screen."""
# Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
# License: MIT, see the LICENSE file.

import numpy as np

from pymazing import color, renderer


class CoordinateGrid:
    def __init__(self):
        self.coordinate_axle_vertices = []
        self.coordinate_axle_colors = [color.from_int(255, 0, 0), color.from_int(0, 255, 0), color.from_int(255, 255, 255)]
        self.coordinate_axle_length = 100.0

        self.grid_line_vertices = []
        self.grid_line_color = color.from_int(128, 128, 128)
        self.grid_line_length = 10.0
        self.grid_line_step = 0.5
        self.grid_line_count = 20

        self.generate_vertices()

    def generate_vertices(self):
        """
        One time generation of the vertices of the grid and coordinate axles.
        """
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
        """
        Render both the grid and the axles to the framebuffer.
        """
        grid_line_view_space_vertices = []
        coordinate_axle_view_space_vertices = []

        for vertex in self.grid_line_vertices:
            grid_line_view_space_vertices.append(camera.view_matrix.dot(vertex))

        for vertex in self.coordinate_axle_vertices:
            coordinate_axle_view_space_vertices.append(camera.view_matrix.dot(vertex))

        view_space_lines = []

        for i in range(0, self.grid_line_count * 8 + 4, 2):
            v0 = grid_line_view_space_vertices[i]
            v1 = grid_line_view_space_vertices[i + 1]
            view_space_lines.append((v0, v1, self.grid_line_color))

        for i, j in enumerate(range(0, 6, 2)):
            v0 = coordinate_axle_view_space_vertices[j]
            v1 = coordinate_axle_view_space_vertices[j + 1]
            view_space_lines.append((v0, v1, self.coordinate_axle_colors[i]))

        renderer.render_lines(view_space_lines, camera, framebuffer, clip_far=False, depth_sort=False)
