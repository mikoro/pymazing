# Pymazing

Pymazing is a basic 3D software rasterizer that does all the drawing/rasterization and 3D math in pure Python. Levels ("mazes") can be loaded from image files in which each pixel represents a colored cube in the 3D world.

* Author: [Mikko Ronkainen](http://mikkoronkainen.com)
* Website: [github.com/mikoro/pymazing](https://github.com/mikoro/pymazing)

![Screenshot](http://mikoro.github.io/images/pymazing/readme-screenshot.jpg "Screenshot")

[A short feature video](http://youtu.be/01qt1wwhz1k) can be viewed at Youtube.

Some features:

- Rasterization of lines and solid triangles
- Clipping of lines and triangles in view and screen spaces
- Solid and wireframe mesh drawing modes
- Triangle backface culling and object view frustum culling
- Free camera movement in the world
- Basic lighting calculations (ambient, diffuse and specular)
- Decoupled game logic calculation and rendering
- Level loading from TGA image files
- Rendering result is displayed using OpenGL textured quads
  - Playable FPS can be achieved
  - Fullscreen mode possible
  - OpenGL scales the texture to the window size -> internal rendering resolution can be smaller than the window size/resolution

## Download

Download the pre-compiled packages (python does not need to be installed):

**Windows**: [pymazing-0.1.0-windows.zip](https://github.com/mikoro/pymazing/releases/download/v0.1.0/pymazing-0.1.0-windows.zip)

**Linux**: [pymazing-0.1.0-linux.zip](https://github.com/mikoro/pymazing/releases/download/v0.1.0/pymazing-0.1.0-linux.zip)

**Mac**: [pymazing-0.1.0-mac.zip](https://github.com/mikoro/pymazing/releases/download/v0.1.0/pymazing-0.1.0-mac.zip)

Program can be started by running the *pymazing* executable (on linux and mac the program needs to be launched from the terminal).

## Run

To run the program using the python interpreter, you will need the following:

Python 3.3.4 ([http://python.org/download/releases/3.3.4](http://python.org/download/releases/3.3.4))

pySFML 1.3 ([http://www.python-sfml.org/download.html](http://www.python-sfml.org/download.html))

PyOpenGL 3.0.2 ([http://pyopengl.sourceforge.net](http://pyopengl.sourceforge.net))

Numpy 1.8.0 ([http://www.scipy.org/scipylib/download.html](http://www.scipy.org/scipylib/download.html))

The program can be started by running the *pymazing.py* file.

## Instructions

The resolution, fullscreen mode and other settings can be changed by editing the *data/settings.ini* file.

The level files are TGA-formatted images. They can created/edited with any editor as long as they are saved in 32-bit bit depth without compression. The active level can be changed from the *settings.ini* file.

Controls:

- **Mouse**: look around
- **W/A/S/D + Q/E or arrow keys**: move around
- **Shift**: move faster
- **Ctrl**: move slower
- **F1**: toggle wireframe rendering on/off
- **F2**: toggle backface culling on/off
- **F3**: toggle rendering of coordinate axles and the grid on/off
- **F4**: toggle rendering of objects on/off
- **F5**: toggle ambient light on/off
- **F6**: toggle diffuse light on/off
- **F7**: toggle specular light on/off
- **F8**: toggle rotation of lights on/off
- **F9**: toggle fps counter on/off
- **F10**: toggle display smoothing (linear filtering) on/off
- **F11**: decrease internal rendering resolution
- **F12**: increase internal rendering resolution
