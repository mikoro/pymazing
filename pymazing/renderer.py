"""
Rendering logic.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import sys

import numpy as np

from pymazing import matrix, rasterizer, color


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

    def render_meshes_as_solid(self, world, camera):
        # go through every vertex and calculate its world space and clip space coordinates
        # also find the smallest distance to the camera
        for mesh in world.meshes:
            mesh.calculate_world_matrix()
            clip_matrix = self.projection_matrix.dot(camera.view_matrix).dot(mesh.world_matrix)
            mesh.world_vertices = []
            mesh.clip_vertices = []
            mesh.maximum_z = sys.float_info.min

            for vertex in mesh.vertices:
                world_vertex = mesh.world_matrix.dot(vertex)
                clip_vertex = clip_matrix.dot(vertex)
                mesh.world_vertices.append(world_vertex)
                mesh.clip_vertices.append(clip_vertex)
                mesh.maximum_z = max(mesh.maximum_z, clip_vertex[2])

        # sort meshes so that we render from the furthest to nearest
        sorted_meshes = sorted(world.meshes, key=lambda m: m.maximum_z, reverse=True)

        world_ambient_color = world.ambient_light_color.get_vector() * world.ambient_light_intensity
        world_diffuse_color = world.diffuse_light_color.get_vector() * world.diffuse_light_intensity
        world_diffuse_direction = -world.diffuse_light_angle.get_direction_vector()

        # go through all the indices (i.e. single triangles) of the mesh and rasterize them
        for mesh in sorted_meshes:
            for i, index in enumerate(mesh.indices):
                # get the clip space vertices
                v0 = mesh.clip_vertices[index[0]]
                v1 = mesh.clip_vertices[index[1]]
                v2 = mesh.clip_vertices[index[2]]

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

                # reject triangles facing backwards in screen space (clockwise vertex order -> facing backwards -> negative signed area)
                signed_area = np.cross([x1 - x0, y1 - y0], [x2 - x0, y2 - y0])

                if signed_area < 0.0:
                    continue

                # get the world space vertices
                v0 = mesh.world_vertices[index[0]]
                v1 = mesh.world_vertices[index[1]]
                v2 = mesh.world_vertices[index[2]]

                # calculate the normal of the triangle in world space
                normal = np.cross([v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]], [v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]])
                normal /= np.linalg.norm(normal)

                diffuse_factor = np.dot(normal, world_diffuse_direction)
                diffuse_factor = np.clip(diffuse_factor, 0.0, 1.0)

                original_color = mesh.colors[i].get_vector()
                diffuse_color = world_diffuse_color * diffuse_factor
                final_color = (world_ambient_color + diffuse_color) * original_color
                final_color = np.clip(final_color, 0.0, 1.0)

                # rasterizer will deal with the clipping to the screen space
                rasterizer.draw_triangle(self.framebuffer, x0, y0, x1, y1, x2, y2, color.create_from_vector(final_color))


    def render_meshes_as_wireframe(self, world, camera):
        for mesh in world.meshes:
            mesh.calculate_world_matrix()
            clip_matrix = self.projection_matrix.dot(camera.view_matrix).dot(mesh.world_matrix)
            mesh.clip_vertices = []
            mesh.maximum_z = sys.float_info.min

            for vertex in mesh.vertices:
                clip_vertex = clip_matrix.dot(vertex)
                mesh.clip_vertices.append(clip_vertex)
                mesh.maximum_z = max(mesh.maximum_z, clip_vertex[2])

        sorted_meshes = sorted(world.meshes, key=lambda m: m.maximum_z, reverse=True)

        for mesh in sorted_meshes:
            for i, index in enumerate(mesh.indices):
                v0 = mesh.clip_vertices[index[0]]
                v1 = mesh.clip_vertices[index[1]]
                v2 = mesh.clip_vertices[index[2]]

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
