"""
Rendering logic.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import sys

import numpy as np

from pymazing import matrix, rasterizer


class Renderer:
    def __init__(self, framebuffer):
        self.framebuffer = framebuffer
        self.projection_matrix = np.identity(4)
        self.vertical_fov = 75.0
        self.near_z = 0.1
        self.far_z = 100.0
        self.half_framebuffer_width = 0.0
        self.half_framebuffer_height = 0.0

    def calculate_projection_matrix(self):
        self.projection_matrix = matrix.create_projection_matrix(self.vertical_fov, self.framebuffer.width / self.framebuffer.height, self.near_z, self.far_z)
        self.half_framebuffer_width = ((self.framebuffer.width - 1.0) / 2.0)
        self.half_framebuffer_height = ((self.framebuffer.height - 1.0) / 2.0)

    def render_meshes_as_solid(self, meshes, view_matrix):
        # transform all the vertices of the mesh into the clip space (world space -> view space -> clip space)
        # also determine the distance from the camera to the nearest vertex of the mesh
        for mesh in meshes:
            mesh.transformed_vertices = []
            mesh.maximum_z = sys.float_info.min
            mesh.calculate_world_matrix()
            transformation_matrix = self.projection_matrix.dot(view_matrix).dot(mesh.world_matrix)

            for vertex in mesh.vertices:
                vertex = transformation_matrix.dot(vertex)
                mesh.transformed_vertices.append(vertex)
                mesh.maximum_z = max(mesh.maximum_z, vertex[2])

        # sort meshes so that we render from the furthest mesh to nearest
        meshes.sort(key=lambda m: m.maximum_z, reverse=True)

        # go through all the indices (i.e. single triangle) of the mesh and rasterize it
        for mesh in meshes:
            for i, index in enumerate(mesh.indices):
                v0 = mesh.transformed_vertices[index[0]]
                v1 = mesh.transformed_vertices[index[1]]
                v2 = mesh.transformed_vertices[index[2]]

                # ignore whole triangle if the z of even one vertex is outside of the clip space
                if v0[2] < -v0[3] or v0[2] > v0[3]:
                    continue

                if v1[2] < -v1[3] or v1[2] > v1[3]:
                    continue

                if v2[2] < -v2[3] or v2[2] > v2[3]:
                    continue

                # convert clip space -> ndc, then convert ndc -> screen space
                x0 = int(v0[0] / v0[3] * self.half_framebuffer_width + self.half_framebuffer_width + 0.5)
                y0 = int(v0[1] / v0[3] * self.half_framebuffer_height + self.half_framebuffer_height + 0.5)
                x1 = int(v1[0] / v1[3] * self.half_framebuffer_width + self.half_framebuffer_width + 0.5)
                y1 = int(v1[1] / v1[3] * self.half_framebuffer_height + self.half_framebuffer_height + 0.5)
                x2 = int(v2[0] / v2[3] * self.half_framebuffer_width + self.half_framebuffer_width + 0.5)
                y2 = int(v2[1] / v2[3] * self.half_framebuffer_height + self.half_framebuffer_height + 0.5)

                # backface culling, forward facing is ccw (positive area)
                signed_area = np.cross([x1 - x0, y1 - y0], [x2 - x0, y2 - y0])

                if signed_area < 0.0:
                    continue

                # rasterizer will deal with the clipping to the screen space
                rasterizer.draw_triangle(self.framebuffer, x0, y0, x1, y1, x2, y2, mesh.colors[i])

    def render_meshes_as_wireframe(self, meshes, view_matrix):
        for mesh in meshes:
            mesh.calculate_world_matrix()
            transformation_matrix = self.projection_matrix.dot(view_matrix).dot(mesh.world_matrix)
            mesh.transformed_vertices = []
            mesh.maximum_z = sys.float_info.min

            for vertex in mesh.vertices:
                vertex = transformation_matrix.dot(vertex)
                mesh.transformed_vertices.append(vertex)
                mesh.maximum_z = max(mesh.maximum_z, vertex[2])

        meshes.sort(key=lambda m: m.maximum_z, reverse=True)

        for mesh in meshes:
            for i, indices in enumerate(mesh.indices):
                v0 = mesh.transformed_vertices[indices[0]]
                v1 = mesh.transformed_vertices[indices[1]]
                v2 = mesh.transformed_vertices[indices[2]]

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

                line1_x0 = line0_x1
                line1_y0 = line0_y1
                line1_x1 = int(v2[0] / v2[3] * self.half_framebuffer_width + self.half_framebuffer_width + 0.5)
                line1_y1 = int(v2[1] / v2[3] * self.half_framebuffer_height + self.half_framebuffer_height + 0.5)

                line2_x0 = line1_x1
                line2_y0 = line1_y1
                line2_x1 = line0_x0
                line2_y1 = line0_y0

                rasterizer.draw_line(self.framebuffer, line0_x0, line0_y0, line0_x1, line0_y1, mesh.colors[i])
                rasterizer.draw_line(self.framebuffer, line1_x0, line1_y0, line1_x1, line1_y1, mesh.colors[i])
                rasterizer.draw_line(self.framebuffer, line2_x0, line2_y0, line2_x1, line2_y1, mesh.colors[i])
