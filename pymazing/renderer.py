"""
Transform 3D data to shapes on the screen.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import sys

import numpy as np

from pymazing import color, clipper, rasterizer


def render_as_solid(world, camera, framebuffer):
    # go through every vertex and calculate its world space and clip space coordinates
    # also find the smallest distance to the camera
    for mesh in world.meshes:
        mesh.calculate_world_matrix()
        clip_matrix = camera.projection_matrix.dot(camera.view_matrix).dot(mesh.world_matrix)
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
            x0 = int(v0[0] / v0[3] * framebuffer.half_width + framebuffer.half_width + 0.5)
            y0 = int(v0[1] / v0[3] * framebuffer.half_height + framebuffer.half_height + 0.5)
            x1 = int(v1[0] / v1[3] * framebuffer.half_width + framebuffer.half_width + 0.5)
            y1 = int(v1[1] / v1[3] * framebuffer.half_height + framebuffer.half_height + 0.5)
            x2 = int(v2[0] / v2[3] * framebuffer.half_width + framebuffer.half_width + 0.5)
            y2 = int(v2[1] / v2[3] * framebuffer.half_height + framebuffer.half_height + 0.5)

            # reject triangles facing backwards in screen space (clockwise vertex order -> facing backwards -> negative signed area)
            signed_area = np.cross([x1 - x0, y1 - y0], [x2 - x0, y2 - y0])

            if signed_area < 0.0:
                continue

            # get the world space vertices
            v0 = mesh.world_vertices[index[0]]
            v1 = mesh.world_vertices[index[1]]
            v2 = mesh.world_vertices[index[2]]

            # calculate the normal of the triangle in the world space
            triangle_normal = np.cross([v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]], [v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]])
            triangle_normal /= np.linalg.norm(triangle_normal)

            # start with ambient light factor
            combined_light_color = world.ambient_light.color.get_vector() * world.ambient_light.intensity

            # calculate and add diffuse light factor
            for diffuse_light in world.diffuse_lights:
                light_vector = diffuse_light.euler_angle.get_direction_vector()
                diffuse_amount = np.dot(triangle_normal, -light_vector)
                diffuse_amount = np.clip(diffuse_amount, 0.0, 1.0)
                combined_light_color += diffuse_light.color.get_vector() * diffuse_light.intensity * diffuse_amount

            # camera vector points from the triangle to the camera
            camera_vector = camera.position - v0[:3]
            camera_vector /= np.linalg.norm(camera_vector)

            # calculate and add specular light factor
            for specular_light in world.specular_lights:
                light_vector = specular_light.euler_angle.get_direction_vector()
                specular_amount = 0.0

                # only do it if the camera is on the same side of the triangle as the light
                if np.dot(triangle_normal, -light_vector) > 0.0:
                    reflection_vector = 2.0 * np.dot(triangle_normal, -light_vector) * triangle_normal + light_vector
                    reflection_vector /= np.linalg.norm(reflection_vector)
                    specular_amount = np.dot(reflection_vector, camera_vector)
                    specular_amount = np.clip(specular_amount, 0.0, 1.0)
                    specular_amount = pow(specular_amount, specular_light.shininess)

                combined_light_color += specular_light.color.get_vector() * specular_light.intensity * specular_amount

            original_triangle_color = mesh.colors[i].get_vector()
            final_triangle_color = original_triangle_color * combined_light_color
            final_triangle_color = np.clip(final_triangle_color, 0.0, 1.0)

            # rasterizer will deal with the clipping to the screen space
            rasterizer.draw_triangle(framebuffer, x0, y0, x1, y1, x2, y2, color.from_vector(final_triangle_color))


def render_as_wireframe(world, camera, framebuffer):
    for mesh in world.meshes:
        mesh.calculate_world_matrix()
        clip_matrix = camera.projection_matrix.dot(camera.view_matrix).dot(mesh.world_matrix)
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

            lines = []

            lines.append(clipper.clip_line_3d(v0, v1))
            lines.append(clipper.clip_line_3d(v1, v2))
            lines.append(clipper.clip_line_3d(v2, v0))

            for line in lines:
                if line is not None:
                    rasterizer.draw_line_clip_space(framebuffer, line[0], line[1], mesh.colors[i])
