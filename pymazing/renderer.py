"""
Transform 3D data to shapes on the screen.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import numpy as np

from pymazing import color, rasterizer


def render_world(world, camera, framebuffer, backface_culling=True, draw_wireframe=False):
    world_triangles = []

    for mesh in world.meshes:
        if not camera.frustum.sphere_is_inside(mesh.position, mesh.bounding_radius):
            continue

        mesh.calculate_world_matrix()
        world_vertices = []

        for vertex in mesh.vertices:
            world_vertices.append(mesh.world_matrix.dot(vertex))

        for i, index in enumerate(mesh.indices):
            v0 = world_vertices[index[0]]
            v1 = world_vertices[index[1]]
            v2 = world_vertices[index[2]]

            x0 = v0[0]
            y0 = v0[1]
            z0 = v0[2]
            x1 = v1[0]
            y1 = v1[1]
            z1 = v1[2]
            x2 = v2[0]
            y2 = v2[1]
            z2 = v2[2]

            triangle_position = v0[:3]

            triangle_normal = np.cross([x1 - x0, y1 - y0, z1 - z0], [x2 - x0, y2 - y0, z2 - z0])
            triangle_normal /= np.linalg.norm(triangle_normal)

            triangle_to_camera = camera.position - triangle_position
            triangle_to_camera /= np.linalg.norm(triangle_to_camera)

            if backface_culling and np.dot(triangle_to_camera, triangle_normal) < 0.0:
                continue

            combined_light_color = world.ambient_light.color.get_vector() * world.ambient_light.intensity

            for diffuse_light in world.diffuse_lights:
                triangle_to_light = diffuse_light.position - triangle_position
                triangle_to_light /= np.linalg.norm(triangle_to_light)
                diffuse_amount = np.dot(triangle_to_light, triangle_normal)
                diffuse_amount = np.clip(diffuse_amount, 0.0, 1.0)
                combined_light_color += diffuse_light.color.get_vector() * diffuse_light.intensity * diffuse_amount

            for specular_light in world.specular_lights:
                triangle_to_light = specular_light.position - triangle_position
                triangle_to_light /= np.linalg.norm(triangle_to_light)
                specular_amount = 0.0

                if np.dot(triangle_to_light, triangle_normal) > 0.0:
                    reflection_vector = 2.0 * np.dot(triangle_to_light, triangle_normal) * triangle_normal - triangle_to_light
                    reflection_vector /= np.linalg.norm(reflection_vector)
                    specular_amount = np.dot(triangle_to_camera, reflection_vector)
                    specular_amount = np.clip(specular_amount, 0.0, 1.0)
                    specular_amount = pow(specular_amount, specular_light.shininess)

                combined_light_color += specular_light.color.get_vector() * specular_light.intensity * specular_amount

            original_triangle_color = mesh.colors[i].get_vector()
            final_triangle_color = original_triangle_color * combined_light_color
            final_triangle_color = np.clip(final_triangle_color, 0.0, 1.0)

            world_triangles.append((v0, v1, v2, color.from_vector(final_triangle_color)))

    clip_matrix = camera.projection_matrix.dot(camera.view_matrix)

    for world_triangle in world_triangles:
        v0 = clip_matrix.dot(world_triangle[0])
        v1 = clip_matrix.dot(world_triangle[1])
        v2 = clip_matrix.dot(world_triangle[2])
        color_ = world_triangle[3]

        if draw_wireframe:
            rasterizer.draw_line_clip_space(framebuffer, v0, v1, color_)
            rasterizer.draw_line_clip_space(framebuffer, v1, v2, color_)
            rasterizer.draw_line_clip_space(framebuffer, v2, v0, color_)
        else:
            x0 = int(v0[0] / v0[3] * framebuffer.half_width + framebuffer.half_width + 0.5)
            y0 = int(v0[1] / v0[3] * framebuffer.half_height + framebuffer.half_height + 0.5)
            x1 = int(v1[0] / v1[3] * framebuffer.half_width + framebuffer.half_width + 0.5)
            y1 = int(v1[1] / v1[3] * framebuffer.half_height + framebuffer.half_height + 0.5)
            x2 = int(v2[0] / v2[3] * framebuffer.half_width + framebuffer.half_width + 0.5)
            y2 = int(v2[1] / v2[3] * framebuffer.half_height + framebuffer.half_height + 0.5)

            rasterizer.draw_triangle(framebuffer, x0, y0, x1, y1, x2, y2, color_)

