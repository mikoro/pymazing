"""Application initialization and running."""
# Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
# License: MIT, see the LICENSE file.

import configparser as cp
import distutils.util as du

import sfml as sf

from pymazing import framebuffer, game_state_simple_cube, game_state_loaded_level, game_engine


def run():
    """
    Read settings from a file, initialize the components and run the game.
    """
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
    framebuffer_ = framebuffer.FrameBuffer()
    framebuffer_.resize(framebuffer_width, framebuffer_height)

    game_state_simple_cube_ = game_state_simple_cube.GameStateSimpleCube(config)
    game_state_loaded_level_ = game_state_loaded_level.GameStateLoadedLevel(config)

    game_engine_ = game_engine.GameEngine(window, framebuffer_, config)
    game_engine_.game_states.append(game_state_simple_cube_)
    game_engine_.game_states.append(game_state_loaded_level_)
    #game_engine_.active_game_state = game_state_simple_cube_
    game_engine_.active_game_state = game_state_loaded_level_

    game_engine_.run()
