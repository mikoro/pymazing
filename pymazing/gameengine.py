"""
Game initialization and main loop management.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import sfml as sf
import OpenGL.GL as gl
import numpy as np
import time

from pymazing import fpscounter as fc, rasterizer as rz, color
from math import *

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

        self.fps_text.string = self.fps_counter.get_fps()

    def _render(self):
        half_width = int(self.framebuffer.width / 2)
        half_height = int(self.framebuffer.height / 2)
        triangle_length = min(half_width, half_height) - 1
        line_length = min(half_width, half_height) - 1
        triangle_color = color.Color(0, 148, 255)
        line_color = color.Color(64, 64, 64)
        point_color = color.Color(255, 0, 0)

        a = time.clock() / 4
        x0 = int(cos(a) * triangle_length) + half_width
        y0 = int(sin(a) * triangle_length) + half_height
        x1 = int(cos(a + pi*2/3) * triangle_length) + half_width
        y1 = int(sin(a + pi*2/3) * triangle_length) + half_height
        x2 = int(cos(a + pi*4/3) * triangle_length) + half_width
        y2 = int(sin(a + pi*4/3) * triangle_length) + half_height
        rz.draw_triangle(self.framebuffer, x0, y0, x1, y1, x2, y2, triangle_color)

        for i in range(0, 100):
            a = (pi * 2) / 100 * i
            x0 = int(cos(a) * line_length) + half_width
            y0 = int(sin(a) * line_length) + half_height
            x1 = int(cos(a + pi) * line_length) + half_width
            y1 = int(sin(a + pi) * line_length) + half_height
            rz.draw_line(self.framebuffer, x0, y0, x1, y1, line_color)
            rz.draw_point(self.framebuffer, x0, y0, point_color)
            rz.draw_point(self.framebuffer, x1, y1, point_color)

        self.window.clear(sf.Color.RED)
        self.framebuffer.render()

        if self.show_fps:
            self.window.push_GL_states()
            self.window.draw(self.fps_text)
            self.window.pop_GL_states()

        self.window.display()
        self.framebuffer.clear()
        self.fps_counter.tick()
