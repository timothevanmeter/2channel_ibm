###############################################
# Author of this project: Timothe van Meter

# Last modification: March 29th 2021

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
import pandas as pd
import subprocess
# -----------------------------
import test_resource as res
import test_animal as ani
import test_output as out
import test_display as disp
# -----------------------------
cell_size = 10
# Expressed in number of cells:
grid_size = 40

# To account for the border cells
plot_size = (cell_size+2)*grid_size

background_colour = (255,255,255)
##################################################
##################################################

init_herbivores = 50
init_predators = 20

max_time = 500

graphic_display = True

screen = disp.create_display(plot_size, cell_size)

ani.init_animals(init_herbivores, init_predators)

grid = res.lattice(grid_size+2)
day = 0

if graphic_display == True:
    running = True
    print("-----------------------------")
    while running:
        day += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Erase previous drawings
        screen.fill(background_colour)
        biomass = round(grid.update_all_cells(graphic_display, screen)/150, 0)
        count = ani.update_all_agents(graphic_display, screen, grid)
        out.save_output(day, biomass, count[0], count[1], count[2], count[3])
        # Ensure that the ecosystem did not collapse
        if ani.stop_criteria() == True or max_time <= day:
            break

        pygame.time.wait(1000)
        pygame.display.flip()

else:
    for i in range(max_time):
        day += 1
        biomass = round(grid.update_all_cells(graphic_display, screen)/150, 0)
        count = ani.update_all_agents(graphic_display, screen, grid)
        out.save_output(day, biomass, count[0], count[1], count[2], count[3])
        # Ensure that the ecosystem did not collapse
        if ani.stop_criteria() == True:
            break



out.write_output()
out.graph_output()
