import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["numbers", "OpenGL"], "excludes": ["sfml"], "include_msvcr": "true"}

base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(name="pymazing",
      version="0.1.0",
      options = {"build_exe": build_exe_options},
      executables = [Executable("pymazing.py", base=base)])

# after build, copy the data directory and sfml (site-packages) directory to the build directory
