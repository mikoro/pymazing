"""
Application executable file.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

import os
os.environ["PYSDL2_DLL_PATH"] = "dll"

from pymazing import main
main.main()
