"""
Application entry point.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

from pymazing import game_engine

def main():
    game = game_engine.GameEngine()
    game.initialize()
    game.run()
    game.shutdown()
