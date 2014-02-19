"""
Game initialization and main loop management.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import sfml as sf
import OpenGL.GL as gl
import numpy as np
import time

from pymazing import fpscounter as fc, rasterizer as rz, color, mesh, math as my_math, camera
from math import *

np.set_printoptions(suppress=True)

class GameEngine:
    def __init__(self, window, framebuffer, framebuffer_scale):
        self.should_run = True
        self.window = window
        self.framebuffer = framebuffer
        self.framebuffer_scale = framebuffer_scale
        self.show_fps = True
        self.fps_counter = fc.FpsCounter()
        self.fps_font = sf.Font.from_file("data/fonts/dejavu-sans-mono-bold.ttf")
        self.fps_text = sf.Text("56", self.fps_font, 16)
        self.fps_text.position = (4, 2)
        self.fps_text.style = sf.Text.REGULAR
        self.fps_text.color = sf.Color(255, 255, 255, 255)
        self.cube = mesh.create_cube()
        self.camera = camera.Camera()
        self.mouse_previous_position = sf.Vector2()

    def run(self):
        previous_time = time.clock()

        while self.should_run:
            current_time = time.clock()
            frame_time = current_time - previous_time
            previous_time = current_time

            if frame_time > 0.25:
                frame_time = 0.25

            self._update(frame_time)
            self._render()

    def _update(self, time_step):
        for event in self.window.events:
            if type(event) is sf.CloseEvent:
                self.should_run = False

            if type(event) is sf.ResizeEvent:
                gl.glViewport(0, 0, event.size.x, event.size.y)
                self.framebuffer.resize(int(self.window.size.x * self.framebuffer_scale + 0.5), int(self.window.size.y * self.framebuffer_scale + 0.5))

            if type(event) is sf.KeyEvent and event.pressed:
                if event.code == sf.Keyboard.F12:
                    self.framebuffer_scale *= 2.0

                    if self.framebuffer_scale > 1.0:
                        self.framebuffer_scale = 1.0

                    self.framebuffer.resize(int(self.window.size.x * self.framebuffer_scale + 0.5), int(self.window.size.y * self.framebuffer_scale + 0.5))

                if event.code == sf.Keyboard.F11:
                    self.framebuffer_scale *= 0.5

                    if self.framebuffer_scale < 0.01:
                        self.framebuffer_scale = 0.01

                    self.framebuffer.resize(int(self.window.size.x * self.framebuffer_scale + 0.5), int(self.window.size.y * self.framebuffer_scale + 0.5))

                if event.code == sf.Keyboard.F10:
                    self.framebuffer.set_smoothing(not self.framebuffer.smoothing_state)

                if event.code == sf.Keyboard.F9:
                    self.show_fps = not self.show_fps

        if sf.Keyboard.is_key_pressed(sf.Keyboard.ESCAPE):
            self.should_run = False

        mouse_delta = self.mouse_previous_position - sf.Mouse.get_position()
        sf.Mouse.set_position(self.window.size / 2, self.window)
        self.mouse_previous_position = sf.Mouse.get_position()

        self.camera.pitch += mouse_delta.y * time_step
        self.camera.yaw += mouse_delta.x * time_step

        forward_vector = self.camera.get_look_at_vector()
        up_vector = self.camera.get_up_vector()
        right_vector = np.cross(up_vector, forward_vector)

        if sf.Keyboard.is_key_pressed(sf.Keyboard.W) or sf.Keyboard.is_key_pressed(sf.Keyboard.UP):
            self.camera.position += forward_vector * 2.0 * time_step

        if sf.Keyboard.is_key_pressed(sf.Keyboard.S) or sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN):
            self.camera.position -= forward_vector * 2.0 * time_step

        if sf.Keyboard.is_key_pressed(sf.Keyboard.A) or sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
            self.camera.position += right_vector * 2.0 * time_step

        if sf.Keyboard.is_key_pressed(sf.Keyboard.D) or sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
            self.camera.position -= right_vector * 2.0 * time_step

        self.fps_text.string = self.fps_counter.get_fps()

    def _render(self):

        window_mouse_x = sf.Mouse.get_position(self.window).x
        window_mouse_y = self.window.size.y - sf.Mouse.get_position(self.window).y
        framebuffer_mouse_x = int((window_mouse_x / self.window.size.x) * self.framebuffer.width + 0.5)
        framebuffer_mouse_y = int((window_mouse_y / self.window.size.y) * self.framebuffer.height + 0.5)

        #if sf.Mouse.is_button_pressed(sf.Mouse.LEFT):
            #rz.draw_clipped_point(self.framebuffer, framebuffer_mouse_x, framebuffer_mouse_y, color.Color(255, 255, 0))
            #rz.draw_line(self.framebuffer, framebuffer_mouse_x - 20, framebuffer_mouse_y + 20, framebuffer_mouse_x + 20, framebuffer_mouse_y - 20, color.Color(255, 255, 0))
            #rz.draw_line(self.framebuffer, framebuffer_mouse_x - 20, framebuffer_mouse_y - 20, framebuffer_mouse_x + 20, framebuffer_mouse_y + 20, color.Color(255, 255, 0))

        MRY = my_math.create_rotation_matrix_y(time.clock())
        MT = my_math.create_translation_matrix(0, 0, -3)
        MV = self.camera.create_view_matrix()
        MP = my_math.create_projection_matrix(90.0, self.window.width / self.window.height, 1.0, 100.0)
        #M = MP.dot(MV).dot(MT).dot(MRY)
        M = MP.dot(MV).dot(MT)

        for vertex in self.cube.vertices:
            vertex = M.dot(vertex)
            vertex[0] /= vertex[3]
            vertex[1] /= vertex[3]
            vertex[2] /= vertex[3]

            if vertex[0] > -1.0 and vertex[0] < 1.0 and vertex[1] > -1.0 and vertex[1] < 1.0 and vertex[2] > -1.0 and vertex[2] < 1.0:
                px = int(vertex[0] * ((self.framebuffer.width - 1.0) / 2.0) + ((self.framebuffer.width - 1.0) / 2.0) + 0.5)
                py = int(vertex[1] * ((self.framebuffer.height - 1.0) / 2.0) + ((self.framebuffer.height - 1.0) / 2.0) + 0.5)
                rz.draw_clipped_point(self.framebuffer, px, py, color.Color(255, 255, 0))

        self.window.clear(sf.Color.RED)
        self.framebuffer.render()

        if self.show_fps:
            self.window.push_GL_states()
            self.window.draw(self.fps_text)
            self.window.pop_GL_states()

        self.window.display()
        self.framebuffer.clear()
        self.fps_counter.tick()
