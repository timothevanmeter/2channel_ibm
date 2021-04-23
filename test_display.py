###############################################
# Author of this project: Timothe van Meter

# Last modification: March 29th 2021

# Contact: tvanme2@uic.edu

# License: GNU General Public License version 3
# https://opensource.org/licenses/GPL-3.0
###############################################

import pygame

# import test_animal as ani

##################################################

background = (255,255,255)


def create_display(plot_size, cell_size):

    background_colour = background
    (width, height) = (plot_size, plot_size)
    screen = pygame.display.set_mode((width+2*cell_size, height+2*cell_size))
    pygame.display.set_caption('IBM Monitor Display')
    screen.fill(background_colour)

    return screen

####################################################

# def activate_display(screen):

#     running = True

#     print("-----------------------------")

#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 # Erase previous drawings
#         ani.update_all_agents()
#         screen.fill(background)
#         pygame.time.wait(10)
#         # print("-----------------------------")
#         pygame.display.flip()

####################################################

def display_agent(screen, colour, pos, size, thickness):

    pygame.draw.circle(screen, colour, pos, size, thickness)
    return 0

####################################################

def display_cell(screen, colour, xpos, ypos, size, thickness):

    rect = pygame.Rect(xpos, ypos, size, thickness)
    pygame.draw.rect(screen, colour, rect)
    return 0

####################################################

def deactivate_display(screen):

    pygame.QUIT
