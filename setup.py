import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["numbers", "OpenGL"], "excludes": ["sfml"]}
                
setup(name="pymazing",
      version="0.1.0",
      options = {"build_exe": build_exe_options},
      executables = [Executable("pymazing.py", base="Win32GUI")])

# after build, copy data (from project) and smfl (from site-packages) folders to the build folder