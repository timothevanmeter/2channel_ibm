###############################################
# Author of this project: Timothe van Meter

# Last modification: January 5th 2021

# Contact: tvanme2@uic.edu

# License: GNU General Public License version 3
# https://opensource.org/licenses/GPL-3.0
###############################################
import matplotlib
import random as rd
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import pygame
# -----------------------------


def fleeing(xpos, ypos):

    x = 10.0
    y = 10.0
    x2 = 0.0
    y2 = 0.0
    d = 5.0

    if x == xpos:
        xpos += 0.01
        # AVOID ZERO DIVISION ERROR!
        
    alpha = math.atan( abs(y-ypos)/abs(x-xpos) )
    print('alpha =', alpha)
    print('cos(alpha) =', math.cos(alpha))
    print('sin(alpha) =', math.sin(alpha))
    print('-------------------------------')
    if x <= xpos and y >= ypos:
        # CAS 1
        print("CAS 1")
        x2 = x - math.cos(alpha)*d
        y2 = y + math.sin(alpha)*d

    elif x >= xpos and y >= ypos:
        # CAS 2
        print("CAS 2")
        x2 = x + math.cos(alpha)*d
        y2 = y + math.sin(alpha)*d

    elif x >= xpos and y <= ypos:
        # CAS 3
        print("CAS 3")
        x2 = x + math.cos(alpha)*d
        y2 = y - math.sin(alpha)*d

    elif x <= xpos and y <= ypos:
        # CAS 4
        print("CAS 4")
        x2 = x - math.cos(alpha)*d
        y2 = y - math.sin(alpha)*d

    print('X2 = ', round(x2,1))
    print('Y2 = ', round(y2,1))


fleeing(10.0, 15.0)
