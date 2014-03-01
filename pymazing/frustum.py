"""
3D frustum.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

from math import *

from pymazing import plane

TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3
NEAR = 4
FAR = 5


class Frustum:
    def __init__(self):
        self.planes = [plane.Plane() for _ in range(6)]

    def setup_from_camera(self, camera):
        tangent = tan(camera.vertical_fov * pi / 180.0 / 2.0)
        near_distance = camera.near_z
        near_half_height = tangent * near_distance
        near_half_width = near_half_height * camera.aspect_ratio
        far_distance = camera.far_z
        far_half_height = tangent * far_distance
        far_half_width = far_half_height * camera.aspect_ratio

        origin = camera.position
        near_forward = camera.forward_vector * near_distance
        near_up = camera.up_vector * near_half_height
        near_right = camera.right_vector * near_half_width
        far_forward = camera.forward_vector * far_distance
        far_up = camera.up_vector * far_half_height
        far_right = camera.right_vector * far_half_width

        ntl = origin + near_forward + near_up - near_right
        ntr = origin + near_forward + near_up + near_right
        nbr = origin + near_forward - near_up + near_right
        nbl = origin + near_forward - near_up - near_right

        ftl = origin + far_forward + far_up - far_right
        ftr = origin + far_forward + far_up + far_right
        fbr = origin + far_forward - far_up + far_right
        fbl = origin + far_forward - far_up - far_right

        self.planes[TOP].setup_from_points(ntl, ftl, ftr)
        self.planes[BOTTOM].setup_from_points(nbl, fbr, fbl)
        self.planes[LEFT].setup_from_points(ntl, fbl, ftl)
        self.planes[RIGHT].setup_from_points(ntr, ftr, fbr)
        self.planes[NEAR].setup_from_points(ntl, ntr, nbr)
        self.planes[FAR].setup_from_points(ftr, ftl, fbl)

    def point_is_inside(self, p):
        for plane in self.planes:
            if plane.point_distance(p) < 0.0:
                return False

        return True

    def sphere_is_inside(self, center, radius):
        for plane in self.planes:
            if (plane.point_distance(center) + radius) < 0.0:
                return False

        return True
