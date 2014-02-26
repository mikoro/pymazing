"""
Application initialization and running.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import configparser as cp
import distutils.util as du

import sfml as sf

from pymazing import game_engine as ge, framebuffer as fb, level_loader as ll, world as wr, camera as cm, grid_renderer as gr, mesh_renderer as mr, fps_counter as fc


def run():
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

    block_data = ll.read_block_data_from_tga(config["game"]["level_file"])
    meshes = ll.generate_meshes_from_block_data(block_data)
    #meshes = [mesh.create_multicolor_cube()]
    world = wr.World(meshes)

    mouse_sensitivity = float(config["game"]["mouse_sensitivity"])
    camera = cm.Camera(mouse_sensitivity)
    camera.position[0] = 2.5
    camera.position[1] = 2
    camera.position[2] = 4

    grid_renderer = gr.GridRenderer()
    mesh_renderer = mr.MeshRenderer()
    fps_counter = fc.FpsCounter()

    fps_font = sf.Font.from_file("data/fonts/dejavu-sans-mono-bold.ttf")
    fps_text = sf.Text("56", fps_font, 16)
    fps_text.position = (4, 2)
    fps_text.style = sf.Text.REGULAR
    fps_text.color = sf.Color(255, 255, 255, 255)

    game_engine = ge.GameEngine(window, framebuffer, framebuffer_scale, update_frequency, world, camera, grid_renderer, mesh_renderer, fps_counter, fps_text)

    game_engine.run()
