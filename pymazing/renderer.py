"""
Rendering logic.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import numpy as np

from pymazing import matrix, rasterizer


class Renderer:
    def __init__(self, framebuffer):
        self.framebuffer = framebuffer
        self.projection_matrix = np.identity(4)
        self.vertical_fov = 90.0
        self.near_z = 0.1
        self.far_z = 100.0
        self.half_framebuffer_width = 0.0
        self.half_framebuffer_height = 0.0

    def calculate_projection_matrix(self):
        self.projection_matrix = matrix.create_projection_matrix(self.vertical_fov, self.framebuffer.width / self.framebuffer.height, self.near_z, self.far_z)
        self.half_framebuffer_width = ((self.framebuffer.width - 1.0) / 2.0)
        self.half_framebuffer_height = ((self.framebuffer.height - 1.0) / 2.0)

    def render_meshes_as_wireframe(self, meshes, view_matrix):
        for mesh in meshes:
            mesh.calculate_world_matrix()
            transformation_matrix = self.projection_matrix.dot(view_matrix).dot(mesh.world_matrix)
            vertices = []

            for vertex in mesh.vertices:
                vertices.append(transformation_matrix.dot(vertex))

            for index in mesh.indices:
                v0 = vertices[index[0]]
                v1 = vertices[index[1]]
                v2 = vertices[index[2]]

                if v0[0] < -v0[3] or v0[0] > v0[3] or v0[1] < -v0[3] or v0[1] > v0[3] or v0[2] < -v0[3] or v0[2] > v0[3]:
                    continue

                if v1[0] < -v1[3] or v1[0] > v1[3] or v1[1] < -v1[3] or v1[1] > v1[3] or v1[2] < -v1[3] or v1[2] > v1[3]:
                    continue

                if v2[0] < -v2[3] or v2[0] > v2[3] or v2[1] < -v2[3] or v2[1] > v2[3] or v2[2] < -v2[3] or v2[2] > v2[3]:
                    continue

                line0_x0 = int(v0[0] / v0[3] * self.half_framebuffer_width + self.half_framebuffer_width + 0.5)
                line0_y0 = int(v0[1] / v0[3] * self.half_framebuffer_height + self.half_framebuffer_height + 0.5)
                line0_x1 = int(v1[0] / v1[3] * self.half_framebuffer_width + self.half_framebuffer_width + 0.5)
                line0_y1 = int(v1[1] / v1[3] * self.half_framebuffer_height + self.half_framebuffer_height + 0.5)
                line0_color = mesh.colors[index[0]]

                line1_x0 = line0_x1
                line1_y0 = line0_y1
                line1_x1 = int(v2[0] / v2[3] * self.half_framebuffer_width + self.half_framebuffer_width + 0.5)
                line1_y1 = int(v2[1] / v2[3] * self.half_framebuffer_height + self.half_framebuffer_height + 0.5)
                line1_color = mesh.colors[index[1]]

                line2_x0 = line1_x1
                line2_y0 = line1_y1
                line2_x1 = line0_x0
                line2_y1 = line0_y0
                line2_color = mesh.colors[index[2]]

                rasterizer.draw_line(self.framebuffer, line0_x0, line0_y0, line0_x1, line0_y1, line0_color)
                rasterizer.draw_line(self.framebuffer, line1_x0, line1_y0, line1_x1, line1_y1, line1_color)
                rasterizer.draw_line(self.framebuffer, line2_x0, line2_y0, line2_x1, line2_y1, line2_color)

    def render_meshes_as_solid(self, meshes, view_matrix):
        pass
