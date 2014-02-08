"""
Game initialization and main loop management.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import ctypes

from sdl2 import *


class GameEngine:
    def __init__(self, framebuffer):
        self.should_run = True
        self.framebuffer = framebuffer

    def run(self):
        event = SDL_Event()

        while self.should_run:
            while SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == SDL_QUIT:
                    self.should_run = False

                if event.type == SDL_KEYDOWN:
                    if event.key.keysym.sym == SDLK_ESCAPE:
                        self.should_run = False

            self._update(0)
            self._render()

    def _update(self, time_step):
        pass

    def _render(self):
        self.framebuffer.render()
