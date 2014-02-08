"""
Framebuffer helper functions.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import ctypes

from sdl2 import *


class FrameBuffer:
    def __init__(self, renderer, texture, surface, width, height):
        self.renderer = renderer
        self.texture = texture
        self.surface = surface
        self.width = width
        self.width = height

    def render(self):
        SDL_UnlockTexture(self.texture)
        SDL_RenderClear(self.renderer)
        SDL_RenderCopy(self.renderer, self.texture, None, None)
        SDL_RenderPresent(self.renderer)
        SDL_LockTexture(self.texture, None, ctypes.byref(self.surface.contents.pixels), ctypes.byref(self.surface.contents.pitch))
