"""
Game initialization and main loop management.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import configparser as cp
import distutils.util as du
import sfml as sf

from pymazing import gameengine as ge, framebuffer as fb


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

        update_frequency = float(config["game"]["update_frequency"])
        game = ge.GameEngine(window, framebuffer, framebuffer_scale, update_frequency)
        game.run()
