"""
Framebuffer helper functions.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import sfml as sf
import OpenGL.GL as gl

class FrameBuffer:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height

    def clear(self):
        pass

    def render(self):
        pass
