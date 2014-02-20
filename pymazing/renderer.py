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
        self.far_z = 40.0
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
                vertex = transformation_matrix.dot(vertex)
                vertex[0] /= vertex[3]
                vertex[1] /= vertex[3]
                vertex[2] /= vertex[3]
                vertices.append(vertex)

            for index in mesh.indices:
                line0_x0 = int(vertices[index[0]][0] * self.half_framebuffer_width + self.half_framebuffer_width + 0.5)
                line0_y0 = int(vertices[index[0]][1] * self.half_framebuffer_height + self.half_framebuffer_height + 0.5)
                line0_z0 = vertices[index[0]][2]
                line0_x1 = int(vertices[index[1]][0] * self.half_framebuffer_width + self.half_framebuffer_width + 0.5)
                line0_y1 = int(vertices[index[1]][1] * self.half_framebuffer_height + self.half_framebuffer_height + 0.5)
                line0_z1 = vertices[index[1]][2]
                line0_color = mesh.colors[index[0]]
                line1_x0 = line0_x1
                line1_y0 = line0_y1
                line1_z0 = line0_z1
                line1_x1 = int(vertices[index[2]][0] * self.half_framebuffer_width + self.half_framebuffer_width + 0.5)
                line1_y1 = int(vertices[index[2]][1] * self.half_framebuffer_height + self.half_framebuffer_height + 0.5)
                line1_z1 = vertices[index[2]][2]
                line1_color = mesh.colors[index[1]]
                line2_x0 = line1_x1
                line2_y0 = line1_y1
                line2_z0 = line1_z1
                line2_x1 = line0_x0
                line2_y1 = line0_y0
                line2_z1 = line0_z0
                line2_color = mesh.colors[index[2]]

                if line0_z0 > -1.0 and line0_z0 < 1.0 and line0_z1 > -1.0 and line0_z1 < 1.0:
                    rasterizer.draw_line(self.framebuffer, line0_x0, line0_y0, line0_x1, line0_y1, line0_color)

                if line1_z0 > -1.0 and line1_z0 < 1.0 and line1_z1 > -1.0 and line1_z1 < 1.0:
                    rasterizer.draw_line(self.framebuffer, line1_x0, line1_y0, line1_x1, line1_y1, line1_color)

                if line2_z0 > -1.0 and line2_z0 < 1.0 and line2_z1 > -1.0 and line2_z1 < 1.0:
                    rasterizer.draw_line(self.framebuffer, line2_x0, line2_y0, line2_x1, line2_y1, line2_color)

    def render_meshes_as_solid(self, meshes, view_matrix):
        pass
