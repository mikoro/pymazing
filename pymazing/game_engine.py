"""
Game initialization and main loop management.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

from sdl2 import *
import sdl2.ext as sdl2ext

class GameEngine:
    def __init__(self):
        self.should_run = True

    def initialize(self):
        sdl2ext.init()
        self.window = sdl2ext.Window("Pymazing", size=(800, 600))

    def shutdown(self):
        sdl2ext.quit()

    def run(self):
        self.window.show()

        while self.should_run:
            events = sdl2ext.get_events()

            for event in events:
                if event.type == SDL_QUIT:
                    self.should_run = False
                    break

            self._update(0)
            self._render()

    def _update(self, time_step):
        pass

    def _render(self):
        self.window.refresh()
