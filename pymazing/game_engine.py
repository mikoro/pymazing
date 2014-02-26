"""
Game main loop management (event handling, logic/physics updating and rendering)

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import time

import sfml as sf
import OpenGL.GL as gl
import numpy as np

from pymazing import matrix


class GameEngine:
    def __init__(self, window, framebuffer, framebuffer_scale, update_frequency, world, camera, grid_renderer, mesh_renderer, fps_counter, fps_text):
        self.window = window
        self.framebuffer = framebuffer
        self.framebuffer_scale = framebuffer_scale
        self.update_frequency = update_frequency
        self.world = world
        self.camera = camera
        self.grid_renderer = grid_renderer
        self.mesh_renderer = mesh_renderer
        self.fps_counter = fps_counter
        self.fps_text = fps_text
        self.should_run = True
        self.show_fps = True
        self.render_meshes_as_wireframe = True

        self.mouse_previous_position = sf.Vector2()
        self.calculate_mouse_delta()
        self.mouse_delta = sf.Vector2()

        self.projection_matrix = np.identity(4)
        self.vertical_fov = 75.0
        self.near_z = 0.1
        self.far_z = 100.0

        self.calculate_projection_matrix()


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
        #self.world.update(time_step)

    def render(self, interpolation):
        self.grid_renderer.render_coordinate_and_grid_lines(self.camera.view_matrix, self.projection_matrix, self.framebuffer)

        if self.render_meshes_as_wireframe:
            self.mesh_renderer.render_meshes_as_wireframe(self.world, self.camera.view_matrix, self.projection_matrix, self.framebuffer)
        else:
            self.mesh_renderer.render_meshes_as_solid(self.world, self.camera, self.projection_matrix, self.framebuffer)

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

    def calculate_projection_matrix(self):
        self.projection_matrix = matrix.create_projection_matrix(self.vertical_fov, self.framebuffer.width / self.framebuffer.height, self.near_z, self.far_z)

    def handle_events(self):
        for event in self.window.events:
            if type(event) is sf.CloseEvent:
                self.should_run = False

            if type(event) is sf.ResizeEvent:
                gl.glViewport(0, 0, event.size.x, event.size.y)
                self.framebuffer.resize(int(self.window.size.x * self.framebuffer_scale + 0.5), int(self.window.size.y * self.framebuffer_scale + 0.5))
                self.calculate_projection_matrix()

            if type(event) is sf.KeyEvent and event.pressed:
                if event.code == sf.Keyboard.ESCAPE:
                    self.should_run = False

                if event.code == sf.Keyboard.F12:
                    self.framebuffer_scale *= 2.0

                    if self.framebuffer_scale > 1.0:
                        self.framebuffer_scale = 1.0

                    self.framebuffer.resize(int(self.window.size.x * self.framebuffer_scale + 0.5), int(self.window.size.y * self.framebuffer_scale + 0.5))
                    self.calculate_projection_matrix()

                if event.code == sf.Keyboard.F11:
                    self.framebuffer_scale *= 0.5

                    if self.framebuffer_scale < 0.01:
                        self.framebuffer_scale = 0.01

                    self.framebuffer.resize(int(self.window.size.x * self.framebuffer_scale + 0.5), int(self.window.size.y * self.framebuffer_scale + 0.5))
                    self.calculate_projection_matrix()

                if event.code == sf.Keyboard.F10:
                    self.framebuffer.set_smoothing(not self.framebuffer.use_smoothing)

                if event.code == sf.Keyboard.F9:
                    self.show_fps = not self.show_fps

                if event.code == sf.Keyboard.F8:
                    self.vertical_fov *= 1.1
                    self.calculate_projection_matrix()

                if event.code == sf.Keyboard.F7:
                    self.vertical_fov *= 0.9
                    self.calculate_projection_matrix()

                if event.code == sf.Keyboard.F6:
                    self.render_meshes_as_wireframe = not self.render_meshes_as_wireframe

                if event.code == sf.Keyboard.INSERT:
                    self.world.ambient_light_intensity *= 1.1

                    if self.world.ambient_light_intensity > 1.0:
                        self.world.ambient_light_intensity = 1.0

                if event.code == sf.Keyboard.DELETE:
                    self.world.ambient_light_intensity *= 0.9

                    if self.world.ambient_light_intensity < 0.01:
                        self.world.ambient_light_intensity = 0.01

                if event.code == sf.Keyboard.HOME:
                    self.world.diffuse_light_intensity *= 1.1

                    if self.world.diffuse_light_intensity > 1.0:
                        self.world.diffuse_light_intensity = 1.0

                if event.code == sf.Keyboard.END:
                    self.world.diffuse_light_intensity *= 0.9

                    if self.world.diffuse_light_intensity < 0.01:
                        self.world.diffuse_light_intensity = 0.01
