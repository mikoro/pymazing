"""
Game initialization and main loop management.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import time

import sfml as sf
import OpenGL.GL as gl

from pymazing import fps_counter as fc


class GameEngine:
    def __init__(self, window, framebuffer, framebuffer_scale, update_frequency, world, camera, renderer):
        self.should_run = True
        self.window = window
        self.framebuffer = framebuffer
        self.framebuffer_scale = framebuffer_scale
        self.update_frequency = update_frequency
        self.world = world
        self.camera = camera
        self.renderer = renderer
        self.mouse_previous_position = sf.Vector2()
        self.mouse_delta = sf.Vector2()
        self.show_fps = True
        self.draw_wireframe = False
        self.fps_counter = fc.FpsCounter()
        self.fps_font = sf.Font.from_file("data/fonts/dejavu-sans-mono-bold.ttf")
        self.fps_text = sf.Text("56", self.fps_font, 16)
        self.fps_text.position = (4, 2)
        self.fps_text.style = sf.Text.REGULAR
        self.fps_text.color = sf.Color(255, 255, 255, 255)

        self.calculate_mouse_delta()
        self.calculate_mouse_delta()

    def run(self):
        time_step = 1.0 / self.update_frequency
        previous_time = time.clock()
        time_accumulator = 0.0

        self.update(time_step)

        while self.should_run:
            current_time = time.clock()
            frame_time = current_time - previous_time
            previous_time = current_time

            if frame_time > 0.25:
                frame_time = 0.25

            time_accumulator += frame_time

            while time_accumulator >= time_step:
                self.update(time_step)
                time_accumulator -= time_step

            self.render(time_accumulator / time_step)

    def update(self, time_step):
        self.handle_events()
        self.calculate_mouse_delta()
        self.camera.update(time_step, self.mouse_delta)

    def render(self, interpolation):
        if self.draw_wireframe:
            self.renderer.render_meshes_as_wireframe(self.world, self.camera)
        else:
            self.renderer.render_meshes_as_solid(self.world, self.camera)

        self.window.clear(sf.Color.RED)
        self.framebuffer.render()

        if self.show_fps:
            self.fps_text.string = self.fps_counter.get_fps()
            self.window.push_GL_states()
            self.window.draw(self.fps_text)
            self.window.pop_GL_states()

        self.window.display()
        self.framebuffer.clear()
        self.fps_counter.tick()

    def calculate_mouse_delta(self):
        self.mouse_delta = self.mouse_previous_position - sf.Mouse.get_position()
        sf.Mouse.set_position(self.window.size / 2, self.window)
        self.mouse_previous_position = sf.Mouse.get_position()

    def handle_events(self):
        for event in self.window.events:
            if type(event) is sf.CloseEvent:
                self.should_run = False

            if type(event) is sf.ResizeEvent:
                gl.glViewport(0, 0, event.size.x, event.size.y)
                self.framebuffer.resize(int(self.window.size.x * self.framebuffer_scale + 0.5), int(self.window.size.y * self.framebuffer_scale + 0.5))
                self.renderer.calculate_projection_matrix()

            if type(event) is sf.KeyEvent and event.pressed:
                if event.code == sf.Keyboard.ESCAPE:
                    self.should_run = False

                if event.code == sf.Keyboard.F12:
                    self.framebuffer_scale *= 2.0

                    if self.framebuffer_scale > 1.0:
                        self.framebuffer_scale = 1.0

                    self.framebuffer.resize(int(self.window.size.x * self.framebuffer_scale + 0.5), int(self.window.size.y * self.framebuffer_scale + 0.5))
                    self.renderer.calculate_projection_matrix()

                if event.code == sf.Keyboard.F11:
                    self.framebuffer_scale *= 0.5

                    if self.framebuffer_scale < 0.01:
                        self.framebuffer_scale = 0.01

                    self.framebuffer.resize(int(self.window.size.x * self.framebuffer_scale + 0.5), int(self.window.size.y * self.framebuffer_scale + 0.5))
                    self.renderer.calculate_projection_matrix()

                if event.code == sf.Keyboard.F10:
                    self.framebuffer.set_smoothing(not self.framebuffer.smoothing_state)

                if event.code == sf.Keyboard.F9:
                    self.show_fps = not self.show_fps

                if event.code == sf.Keyboard.F8:
                    self.renderer.vertical_fov *= 1.1
                    self.renderer.calculate_projection_matrix()

                if event.code == sf.Keyboard.F7:
                    self.renderer.vertical_fov *= 0.9
                    self.renderer.calculate_projection_matrix()

                if event.code == sf.Keyboard.F6:
                    self.draw_wireframe = not self.draw_wireframe
