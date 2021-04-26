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
import test_display as disp
import test_output as out
# -----------------------------
cell_size = 10
# Expressed in number of cells:
grid_size = 40

# To account for the border cells
plot_size = (cell_size+2)*grid_size

global agents
global herbivores
global predators

agents = []
herbivores = []
predators = []

##################################################

# screen = disp.create_display(plot_size, cell_size)

# background_colour = (255,255,255)
# (width, height) = (plot_size, plot_size)

# screen = pygame.display.set_mode((width+2*cell_size, height+2*cell_size))
# pygame.display.set_caption('IBM Monitor Display')
# screen.fill(background_colour)
# clock = pygame.time.Clock()

##################################################
# def distance_agent_pos(agent_a, pos):

#     d = round(math.sqrt( (agent_a.x - pos[0])**2 + (agent_a.y - pos[1])**2 ), 1)
#     return d
##################################################


####################################################
####################################################
####################################################



class agent():

# -----------------------------------------------------------------                        
    def __init__(self, xpos, ypos):

        # global agents
        self.x = xpos
        self.y = ypos
        # Body radius
        self.r = 10.0
        # Dispersal distance
        self.d = 40.0
        # self.species = rd.randint(1,2)
        self.species = ('AGENT', 0)
        self.biomass = 50.0 #rd.random()
        self.max_biomass = 200.0
        self.colour = (0, 0, 255)
        self.thickness = 3
        # self.biomass = np.random.rand(1,100)
        # self.k = 100.0
        agents.append(self)

# -----------------------------------------------------------------                    
    def pos(self):
    	pos = (self.x, self.y)
    	return pos

# -----------------------------------------------------------------                    
    def biomass_value(self):
    	return self.biomass
    
# -----------------------------------------------------------------                    
    def species(self, nb):
    	return self.species[nb]
    
# -----------------------------------------------------------------                        
    # def display(self, screen):
    #     global cell_size
    #     pygame.draw.circle(screen, self.colour, (self.x+2*cell_size, self.y+2*cell_size), self.r, self.thickness)
    #     return 0

# -----------------------------------------------------------------                        
    def display(self, screen):
        global cell_size
        disp.display_agent(screen, self.colour, (self.x+2*cell_size, self.y+2*cell_size), self.r, self.thickness)

# -----------------------------------------------------------------

    def distance_pos(self, pos):
        d = round(math.sqrt( (self.x - pos[0])**2 + (self.y - pos[1])**2 ), 1)
        return d

# -----------------------------------------------------------------

    def metabolic_cost(self):
        # IF THE METABOLIC COST FOR THIS TIME STEP
        # EXCEEDS THE CURRENT BIOMASS
        if self.biomass - self.max_biomass * 0.05 <= 0.0:
            # THE AGENT DIES
            self.death(True)
        else:
            self.biomass = self.biomass - self.max_biomass * 0.05

# -----------------------------------------------------------------                    
    def death(self, forced):
        # global agents
        death_percentage = 5
        if rd.randrange(0, 100, 1) >= 100 - death_percentage\
           or forced == True:
            # THE AGENT DIES
            agents.remove(self)
            if self.__class__.__name__ == 'herbivore':
                herbivores.remove(self)
                # print('DEATH HERBIVORE')
            elif self.__class__.__name__ == 'predator':
                predators.remove(self)
                # print('DEATH PREDATOR')
            del self

# -----------------------------------------------------------------            
            
    # check_bounds(x, y) is a recursive function verifying that the two
    # new coordinates, x and y passed for an agent are within the bounds of
    # the grid environment.
    # THIS VERSION HERE HAS BEEN TRANSFORMED TO BE ITERATIVE INSTEAD
    # BECAUSE OF FREQUENT RECURSION ERRORS
    def check_bounds(self, xpos, ypos, fleeing):
        
        global plot_size
        global cell_size
        # grid = plot_size-cell_size
        # If the new position is within the bounds of
        # the grid we accept it and send it back.
        # grid.size = 100
        for i in range(100):
            # if (xpos > self.r+cell_size) and (xpos < plot_size-cell_size-self.r) and (ypos > self.r+cell_size) and (ypos < plot_size-cell_size-self.r):
            if (xpos > self.r+cell_size) and (xpos < plot_size-cell_size-self.r) and (ypos > self.r+cell_size) and (ypos < plot_size-cell_size-self.r):
                return xpos, ypos
            else:
                # If xpos is beyond bounds.
                # We redraw the xpos
                if (xpos < self.r+cell_size) or (xpos > plot_size-cell_size-self.r):
                    if fleeing == True:
                        xpos = self.x
                        ypos = round(self.y + rd.uniform(-self.d, self.d),1)
                    xpos = round(self.x + rd.uniform(-self.d, self.d),1)
                    # OLDER RECURSIVE VERSION PART:
                    # return self.check_bounds(round(self.x + rd.uniform(-self.d, self.d),1), ypos)
                # If ypos is beyond bounds.
                # We redraw the ypos
                if (ypos < self.r+cell_size) or (ypos > plot_size-cell_size-self.r):
                    if fleeing == True:
                        xpos = round(self.x + rd.uniform(-self.d, self.d),1)
                        ypos = self.y
                    ypos = round(self.y + rd.uniform(-self.d, self.d),1)
                    # OLDER RECURSIVE VERSION PART:
                    # return self.check_bounds(xpos, round(self.y + rd.uniform(-self.d, self.d),1))
        
# -----------------------------------------------------------------                    
    def random_movement(self):
        
        # global agents
        max_attempts = 10
        newpos = ()
        new = True
        collision = False
        for i in range(max_attempts):
            # To monitor possible RecursionError
            newpos = (self.check_bounds(round(self.x + rd.uniform(-self.d, self.d),1), round(self.y + rd.uniform(-self.d, self.d),1), False))
            if newpos is None:
                # print("PROBLEM")
                new = False
                return 0

            # HERE THE COLLISION MODULE FOR AGENTS HAS BEEN COMMENTED OUT !
            ###############################################################
                # If there is a recursion error and no new coordinates
                # Then no need to verify if there are collisions
            # if new == True:
            #     for i in range(len(agents)):
            #         if 2.0*self.r > self.distance_pos(newpos) and agents[i] != self:
            #             # Only one agent occupying (even partially) the destination (newx, newy)
            #             # is sufficient to prevent movement.
            #             # Therefore, the necessity to draw a new random position.
            #             print('COLLISION!')
            #             collision = True
            #             break
            ###############################################################     
                    
        if collision == False and new == True:
            self.x = newpos[0]
            self.y = newpos[1]

        # return collision

# -----------------------------------------------------------------

    def move_to(self, obj):
        
        # Obtain the general direction for the movement
        pos = obj.pos()    
        dispx = 0.0
        dispy = 0.0

        if abs(pos[0]-self.x) <= self.d:
            self.x = pos[0]
        else:
            dispx = self.d
            
        if abs(pos[1]-self.y) <= self.d:
            self.y = pos[1]
        else:
            dispy = self.d

        if pos[1] > self.y and pos[0] > self.x or pos[1] < self.y and pos[0] < self.x:
            alpha = math.atan2(self.y-pos[1], self.x-pos[0])
            self.x += -round(math.sin(alpha) * dispx,1)
            self.y += -round(math.cos(alpha) * dispy,1)

        elif pos[1] == self.y:
            alpha = math.atan2(self.y-pos[1], self.x-pos[0])
            self.x += -round(math.cos(alpha) * dispx,1)
                        
        elif pos[0] == self.x:
            alpha = math.atan2(pos[1]-self.y, pos[0]-self.x)
            self.y += round(math.sin(alpha) * dispy,1)
        else:
            alpha = math.atan2(self.y-pos[1], self.x-pos[0])
            self.x += round(math.sin(alpha) * dispx,1)
            self.y += round(math.cos(alpha) * dispy,1)        
        
# -----------------------------------------------------------------                    
    def show(self):
        print('Class:', self.__class__.__name__, 'Species:', self.species[0],self.species[1],'', 'x=', self.x,'', 'y=', self.y)#,'', 'biomass=', self.biomass)
                # print('Biomass=', self.biomass)

                
####################################################
####################################################
####################################################


class herbivore(agent):
    
    def __init__(self, xpos, ypos):

        # global agents
        # global herbivores
        self.x = xpos
        self.y = ypos
        # Body radius
        self.r = 10
        # Dispersal distance
        self.d = 10.0
        # Vision radius
        self.v = 30.0
        # self.species = rd.randint(1,2)
        self.species = ('HERBIVORE', rd.randint(1,2))
        self.biomass = 90.0 #rd.random()
        self.max_biomass = 200.0
        self.colour = (0, 0, 255)
        self.thickness = 3
        # Individual memory allocation to store
        # the targeted cell in the previous time step
        self.target = False
        # self.biomass = np.random.rand(1,100)
        # self.k = 100.0
        agents.append(self)
        herbivores.append(self)        

# -----------------------------------------------------------------                                
    def consume(self, cell):

        # if self.distance_pos((cell.x, cell.y) < self.r + cell.size():
        # print("CONSUMPTION =", cell.biomass_value())
        self.biomass += cell.biomass_value() # *conversion_efficiency
        cell.update_biomass(0.0)
        cell.change_colour((255,255,255))

# -----------------------------------------------------------------

    def search(self, grid):

        global grid_size
        consumables = []
        
        # If the targeted cell in the previous time step
        # is within consumption range then consume it
        if self.target != False and\
           self.distance_pos(self.target.pos())-self.r <= 0.0:
            self.consume(self.target)
            self.target = False
            return 1
        
        # Searching for the closest cell, within its vision radius
        # Verify if consumption is possible:
        # - the resource is part of the consumer diet AND
        # - the resource's biomass is non-null
        for i in range(grid_size**2):
            if self.distance_pos(grid.cells[i].pos())-self.r \
               <= self.v \
                and self.species[1] == grid.cells[i].species \
                and grid.cells[i].biomass != 0:
                
                if self.distance_pos(grid.cells[i].pos())-self.r <= 0.0\
                   and grid.cells[i].biomass == grid.cells[i].k_value():
                    # Any cell at distance 0.0 with maximum
                    # biomass will do!
                    # No need to use a looot more memory
                    self.consume(grid.cells[i])
                    return 1
                    # return grid.cells[i]
                # LOOKING FOR THE BIOMASS BIOMASS QUANTITY
                # AVAILABLE WITHIN VISION RADIUS OF THAT
                # INDIVIDUAL
                consumables.append( (grid.cells[i], grid.cells[i].biomass) )
                # Older version with a distance ranking instead:
                # consumables.append( (grid.cells[i], self.distance_pos(grid.cells[i].pos())) )
        if not consumables:
            return 0
        else:
            maximum = consumables[0][1]
            target = consumables[0][0]
            for i in range(len(consumables)):
                if consumables[i][1] > maximum:
                    maximum = consumables[i][1]
                    # Ensures that there is only one target
                    # even if there are multiple minima
                    # Send only the cell object and not the
                    # associated biomass
                    # (distance in the older version)
                    target = consumables[i][0]
                
            # If the previously targeted cell:
            # - still exists
            # - is different from the renewed target (see above)
            # - has a greater biomass than the renewed target
            # Then, continue to move towards that cell
            if self.target != False \
               and target != self.target \
                   and self.target.biomass >= target.biomass:
                return self.target
            # Otherwise, move towards renewed target 
            else:
                self.target = target
                return target

# -----------------------------------------------------------------

    def fleeing(self):
        # global predators
        for i in range(len(predators)):
            # If there is predator(s) in visible surroundings
            # Then flee in opposite direction
            if self.distance_pos(predators[i].pos()) <= self.v:
                # MOVE AWAY FROM THE FIRST THREAT

                xpos = predators[i].pos()[0]
                ypos = predators[i].pos()[1]
                if self.x == xpos:
                    xpos += 0.01
                    # AVOID ZERO DIVISION ERROR!
                alpha = math.atan( abs(self.y-ypos)/abs(self.x-xpos) )
                
                if self.x <= xpos and self.y >= ypos:
                    # CAS 1
                    tempx = self.x - math.cos(alpha)*self.d
                    tempy = self.y + math.sin(alpha)*self.d
                    newpos = self.check_bounds(tempx, tempy, True)
                    
                elif self.x >= xpos and self.y >= ypos:
                    # CAS 2
                    tempx = self.x + math.cos(alpha)*self.d
                    tempy = self.y + math.sin(alpha)*self.d
                    newpos = self.check_bounds(tempx, tempy, True)

                elif self.x >= xpos and self.y <= ypos:
                    # CAS 3
                    tempx = self.x + math.cos(alpha)*self.d
                    tempy = self.y - math.sin(alpha)*self.d
                    newpos = self.check_bounds(tempx, tempy, True)

                elif self.x <= xpos and self.y <= ypos:
                    # CAS 4
                    tempx = self.x - math.cos(alpha)*self.d
                    tempy = self.y - math.sin(alpha)*self.d
                    newpos = self.check_bounds(tempx, tempy, True)

                if newpos is None:
                    return 0
                self.x = newpos[0]
                self.y = newpos[1]
                return True
            else:
                return False

# -----------------------------------------------------------------

    def reproduce(self):
        # IF THE ANIMAL HAS ENOUGH BIOMASS
        # IT CAN REPRODUCE ASEXUALLY
        if self.biomass >= 150.0:
            if rd.randint(0, 1)==1:
                xpos = self.x + 10.0
            else:
                xpos = self.x - 10.0
            if rd.randint(0, 1)==1:
                ypos = self.y + 10.0
            else:
                ypos = self.y - 10.0
            herbivore(xpos, ypos)
            
# -----------------------------------------------------------------

    def update(self, grid):

        # self.metabolic_cost()
        # self.death(False)
        # If there is predator(s) in visible surroundings
        # Then flee in opposite direction
        if self.fleeing() == True:
            return 0
        if self.biomass >= 150.0:
            self.reproduce()
            return 0
        # Then look for resource to consume nearby
        # (within their vision radius)
        elif self.search(grid) == 0:
            # If there is no resource move at random
            # to a new position
            self.random_movement()
            return 0
        elif self.search(grid) != 1 and self.search(grid) != 0 :
            # If there is available resources nearby
            # move towards the resource
            self.move_to(self.search(grid))
            return 0



####################################################
####################################################
####################################################



class predator(agent):
    
    def __init__(self, xpos, ypos):

        # global agents
        # global predators
        self.x = xpos
        self.y = ypos
        # Body radius
        self.r = 10
        # Dispersal distance
        self.d = 10.0
        # Vision radius
        self.v = 40.0
        # The predator's preference for herbivore of species 1
        self.alpha = 0.75
        # self.species = rd.randint(1,2)
        self.species = ('PREDATOR', 1)
        self.biomass = 90.0 #rd.random()
        self.max_biomass = 200.0
        self.colour = (255, 0, 0)
        self.thickness = 3
        # Individual memory allocation to store
        # the targeted cell in the previous time step
        self.target = False
        # self.biomass = np.random.rand(1,100)
        # self.k = 100.0
        agents.append(self)
        predators.append(self)

# -----------------------------------------------------------------

    def consume(self, herb):

        # if self.distance_pos((cell.x, cell.y) < self.r + cell.size():
        # print("CONSUMPTION =", cell.biomass_value())
        self.biomass += herb.biomass_value() # *conversion_efficiency
        herb.death(True)
        # print('PREDATION EVENT')
        
# -----------------------------------------------------------------

    def search(self, grid):

        global grid_size
        # global herbivores
        consumables = []
        
        # If the targeted herbivore in the previous time step
        # is within consumption range then consume it
        if self.target != False and\
           self.distance_pos(self.target.pos())-(self.r+self.target.r)\
                <= 0.0:
            self.consume(self.target)
            self.target = False
            return 1
        
        # Searching for the closest herbivore, within its vision radius
        # Verify if consumption is possible:
        # - the herbivore is part of the consumer diet
        for i in range(len(herbivores)):
            if self.distance_pos(herbivores[i].pos())\
                   -(self.r+herbivores[i].r) <= self.v:
                
                if self.distance_pos(herbivores[i].pos())\
                   -(self.r+herbivores[i].r) <= 0.0:
                    # Any herbivores[i]ivore at distance 0.0 will do!
                    # No need to use a looot more memory
                    self.consume(herbivores[i])
                    return 1
                # LOOKING FOR THE BIOMASS BIOMASS QUANTITY
                # AVAILABLE WITHIN VISION RADIUS OF THAT
                # INDIVIDUAL
                consumables.append( (herbivores[i], self.distance_pos(herbivores[i].pos())) )
        if not consumables:
            return 0
        else:
            mininmum = consumables[0][1]
            target = consumables[0][0]
            for i in range(len(consumables)):
                if consumables[i][1] < mininmum:
                    mininmum = consumables[i][1]
                    # Ensures that there is only one target
                    # even if there are multiple minima
                    # Send only the cell herbivoreand not the
                    # associated distance
                    target = consumables[i][0]

        return target

# -----------------------------------------------------------------

    def reproduce(self):

        # global herbivores
        # IF THE ANIMAL HAS ENOUGH BIOMASS
        # IT CAN REPRODUCE ASEXUALLY
        if self.biomass >= 150.0:
            if rd.randint(0, 1)==1:
                xpos = self.x + 10.0
            else:
                xpos = self.x - 10.0
            if rd.randint(0, 1)==1:
                ypos = self.y + 10.0
            else:
                ypos = self.y - 10.0
            predator(xpos, ypos)
            
# -----------------------------------------------------------------            

    def update(self, grid):

        # self.metabolic_cost()
        # self.death(False)

        if self.biomass >= 150.0:
            self.reproduce()
            # print("REPRODUCTION")
            return 0

        # Then look for resource to consume nearby
        # (within their vision radius)
        elif self.search(grid) == 0:
            # If there is no resource move at random
            # to a new position
            self.random_movement()
            # print("RANDOM MOVEMENT")
            return 0
        elif self.search(grid) != 1 and self.search(grid) != 0 :
            # If there is available resources nearby
            # move towards the resource
            self.move_to(self.search(grid))
            # print("DIRECTED MOVEMENT")
            return 0

# -----------------------------------------------------------------            

def update_all_agents(graphic, screen, grid):
    global agents
    total_herbivores = 0
    total_herbivores1 = 0
    total_herbivores2 = 0
    total_predators = 0
    for ag in agents:
        if graphic ==True:
                ag.display(screen)
        if ag.species[0] == 'HERBIVORE':
            ag.update(grid)
            if ag.species[1] == 1:
                total_herbivores1 += 1
            else:
                total_herbivores2 += 1            
            total_herbivores += 1
        if ag.species[0] == 'PREDATOR':
            ag.update(grid)           
            total_predators += 1

    count = [ total_herbivores, total_herbivores1, total_herbivores2, total_predators ]
    return count

# -----------------------------------------------------------------

####################################################
####################################################
####################################################


def stop_criteria():
    # global herbivores
    # global predators

    if len(herbivores) == 0 or\
       len(predators) == 0:

        print('ECOSYSTEM COLLAPSED!')
        # save_output()
        return True


####################################################
####################################################
####################################################

def init_pos():
    return round(rd.uniform(cell_size+10.0, plot_size-cell_size-10.0), 0)

def init_animals(number_h, number_p):

    for i in range(number_h):
        herbivore(init_pos(), init_pos())

    for i in range(number_p):
        predator(init_pos(), init_pos()) 



####################################################
####################################################
####################################################

# running = True

# print("-----------------------------")
# day = 0

# while running:
#     day += 1
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Erase previous drawings
#     screen.fill(background_colour)
#     # Set count variables to 0
#     total_biomass = 0
#     total_herbivores = 0
#     total_herbivores1 = 0
#     total_herbivores2 = 0
#     total_predators = 0
#     total_predators1 = 0
#     total_predators2 = 0
#     # Update and display all cells 
#     for cell in grid.cells:
#         total_biomass += cell.biomass_value()
#         cell.display(screen)
#     for border in grid.borders:
#         border.display(screen)
#     grid.update()
#     # for agent in agents:
#     # print("# Active herbivores:", len(herbivores))
#     # Update and display all predators
#     for pred in predators:
#         pred.update(grid)
#         pred.display(screen)
#         if pred.species[1] == 1:
#             total_predators1 += 1
#         else:
#             total_predators2 += 1            
#         total_predators += 1
#     # Update and display all herbivores
#     for herb in herbivores:
#         herb.update(grid)
#         herb.display(screen)
#         if herb.species[1] == 1:
#             total_herbivores1 += 1
#         else:
#             total_herbivores2 += 1            
#         total_herbivores += 1
#     # Save each time step to output
#     out.save_output(day, round(total_biomass/150, 0), total_herbivores, total_herbivores1, total_herbivores2, total_predators, total_predators1, total_predators2)
#     # Ensure that the ecosystem did not collapse
#     # if stop_criteria() == False:
#     #     break
#     pygame.time.wait(10)
#     # print("-----------------------------")
#     pygame.display.flip()





# out.write_output()
# out.graph_output()
