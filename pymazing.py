"""
Application executable file.

Copyright: Copyright © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
License: MIT License, see the LICENSE file.
"""

from pymazing import application

app = application.Application()
exit(app.run())
