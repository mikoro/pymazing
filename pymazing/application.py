"""
Game initialization and main loop management.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import os
import configparser
import distutils.util
import ctypes

os.environ["PYSDL2_DLL_PATH"] = "dll"

from sdl2 import *
from pymazing import game_engine as ge, framebuffer as fb


class Application:
    def run(self):
        config = configparser.ConfigParser()
        config.read("data/settings.ini")

        SDL_Init(SDL_INIT_EVERYTHING)

        flags = SDL_WINDOW_SHOWN
        flags |= SDL_WINDOW_RESIZABLE

        if distutils.util.strtobool(config["window"]["fullscreen"]):
            flags |= SDL_WINDOW_FULLSCREEN

        width = int(config["window"]["width"])
        height = int(config["window"]["height"])

        window = SDL_CreateWindow(b"Pymazing", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width, height, flags)

        flags = SDL_RENDERER_ACCELERATED

        if distutils.util.strtobool(config["window"]["vsync"]):
            flags |= SDL_RENDERER_PRESENTVSYNC

        renderer = SDL_CreateRenderer(window, -1, flags)
        texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_ARGB8888, SDL_TEXTUREACCESS_STREAMING, width, height)
        surface = SDL_CreateRGBSurface(0, width, height, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
        SDL_LockTexture(texture, 0, ctypes.byref(surface.contents.pixels), ctypes.byref(surface.contents.pitch))

        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)

        framebuffer = fb.FrameBuffer(renderer, texture, surface, width, height)

        game = ge.GameEngine(framebuffer)
        game.run()

        SDL_DestroyTexture(texture)
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(window)
        SDL_Quit()

        return 0
