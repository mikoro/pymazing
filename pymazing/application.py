"""
Game initialization and main loop management.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import configparser as cp
import distutils.util as du

import sfml as sf

from pymazing import game_engine as ge, framebuffer as fb, level_loader as ll, world as wr, camera as cm, renderer as re, mesh


class Application:
    def run(self):
        config = cp.ConfigParser()
        config.read("data/settings.ini")

        window_width = int(config["window"]["width"])
        window_height = int(config["window"]["height"])

        flags = sf.Style.DEFAULT
        fullscreen = du.strtobool(config["window"]["fullscreen"])

        if fullscreen:
            flags |= sf.Style.FULLSCREEN

        window = sf.RenderWindow(sf.VideoMode(window_width, window_height), "Pymazing", flags)
        window.vertical_synchronization = du.strtobool(config["window"]["vsync"])
        window.mouse_cursor_visible = not du.strtobool(config["window"]["hide_mouse"])
        window.key_repeat_enabled = False

        framebuffer_scale = float(config["window"]["framebuffer_scale"])
        framebuffer_width = int(framebuffer_scale * window_width)
        framebuffer_height = int(framebuffer_scale * window_height)
        framebuffer = fb.FrameBuffer()
        framebuffer.resize(framebuffer_width, framebuffer_height)

        block_data = ll.read_block_data_from_tga(config["game"]["level_file"])
        meshes = ll.generate_meshes_from_block_data(block_data)

        #meshes = [mesh.create_multicolor_cube()]

        world = wr.World(meshes)

        camera = cm.Camera()
        camera.position[0] = 4
        camera.position[1] = 2
        camera.position[2] = 8

        renderer = re.Renderer(framebuffer)
        renderer.calculate_projection_matrix()

        update_frequency = float(config["game"]["update_frequency"])
        game_engine = ge.GameEngine(window, framebuffer, framebuffer_scale, update_frequency, world, camera, renderer)

        game_engine.run()
