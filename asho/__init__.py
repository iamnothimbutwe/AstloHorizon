#Copyright © 2026 Mark Macharia [@iamnothimbutwe Github]
# All rights reserved.
# Unauthorized copying, modification, distribution, or commercial use of this software (or substantial portions of it) is strictly prohibited without express written permission from the author

"""
astlohoriozons


astlohorizons is a plugin to the main astlo core engine. This module utilizes NASA-JPL ephemeris.

it was mainly created for tracking Earths moon and the other moons of the solar system.
Astlo the core engine does not pull any data from any external source.

Astlo Space systems,r/kenyaspacenerds
"""

__version__ = 'v0.1.100'
__author__ = 'maxharia/@iamnothimbutwe Github and Gitlab/Macharia'


from .astho import Asho

__all__ = ['Asho','__version__','__author__']

