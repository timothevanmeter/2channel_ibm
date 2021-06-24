###############################################
# Author of this project: Timothe van Meter

# Last modification: March 29th 2021

# Contact: tvanme2@uic.edu

# License: GNU General Public License version 3
# https://opensource.org/licenses/GPL-3.0
###############################################
# import matplotlib
import random as rd
import numpy as np
# import matplotlib.pyplot as plt
import math
from numpy.lib.shape_base import expand_dims
# from matplotlib.colors import BoundaryNorm
# from matplotlib.ticker import MaxNLocator
import pygame
import pandas as pd
import subprocess
# -----------------------------
import test_resource as res
import test_display as disp
import test_output as out
# -----------------------------

import uuid

cell_size = 10
# Expressed in number of cells:
grid_size = 40

# To account for the border cells
plot_size = (cell_size+2)*grid_size

global agents
global herbivores
global predators
global dead_agents

agents = []
herbivores = []
predators = []
dead_agents = []

####################################################
####################################################
####################################################

class agent():

# -----------------------------------------------------------------                        
    def __init__(self):

        self.id = uuid.uuid4()
    
    def __str__(self):
        return str(self.id)


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
        if self.biomass - self.max_biomass * 0.01 <= 0.0:
            # THE AGENT DIES
            self.death(True)
        else:
            self.biomass = self.biomass - self.max_biomass * 0.01

# -----------------------------------------------------------------                    
    def death(self, forced):
        death_percentage = 5
        if rd.randrange(0, 100, 1) >= 100 - death_percentage or forced == True:
            # THE AGENT DIES
            if self not in dead_agents:
                dead_agents.append(self)
            else:
                print('tried to kill carniovre alrady dead')
                print("problem in metabolic_cost > race condition")
                print("-> killed twice, one forced one not")
            self.status = False

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
                        ypos = round(self.y + rd.uniform(-self.d, self.d), 1)
                    xpos = round(self.x + rd.uniform(-self.d, self.d), 1)
                    # OLDER RECURSIVE VERSION PART:
                    # return self.check_bounds(round(self.x + rd.uniform(-self.d, self.d),1), ypos)
                # If ypos is beyond bounds.
                # We redraw the ypos
                if (ypos < self.r+cell_size) or (ypos > plot_size-cell_size-self.r):
                    if fleeing == True:
                        xpos = round(self.x + rd.uniform(-self.d, self.d), 1)
                        ypos = self.y
                    ypos = round(self.y + rd.uniform(-self.d, self.d), 1)
                    # OLDER RECURSIVE VERSION PART:
                    # return self.check_bounds(xpos, round(self.y + rd.uniform(-self.d, self.d),1))
        
# -----------------------------------------------------------------                    
    def random_movement(self):
        
        max_attempts = 10
        newpos = ()
        new = True
        collision = False
        for i in range(max_attempts):
            # To monitor possible RecursionError
            newpos = (self.check_bounds(round(self.x + rd.uniform(-self.d, self.d), 1), round(self.y + rd.uniform(-self.d, self.d), 1), False))
            if newpos is None:
                # print("PROBLEM")
                new = False
                return 0

      
                    
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
            self.x += -round(math.sin(alpha) * dispx, 1)
            self.y += -round(math.cos(alpha) * dispy, 1)

        elif pos[1] == self.y:
            alpha = math.atan2(self.y-pos[1], self.x-pos[0])
            self.x += -round(math.cos(alpha) * dispx, 1)
                        
        elif pos[0] == self.x:
            alpha = math.atan2(pos[1]-self.y, pos[0]-self.x)
            self.y += round(math.sin(alpha) * dispy, 1)
        else:
            alpha = math.atan2(self.y-pos[1], self.x-pos[0])
            self.x += round(math.sin(alpha) * dispx, 1)
            self.y += round(math.cos(alpha) * dispy, 1)
        
# -----------------------------------------------------------------                    
    def show(self):
        print('Class:', self.__class__.__name__, 'Species:', self.species[0], self.species[1], '', 'x=', self.x, '', 'y=', self.y)  # ,'', 'biomass=', self.biomass)
                # print('Biomass=', self.biomass)

                
####################################################
####################################################
####################################################


class herbivore(agent):
    
    def __init__(self, xpos, ypos):

        super().__init__()
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
        self.biomass = 80.0  # rd.random()
        self.max_biomass = 200.0
        self.colour = (0, 0, 255)
        self.thickness = 3
        # The predator's preference for the herbivore's species
        self.alpha = 0.75
        # if self.species[0] == 1:
        #     self.alpha = 0.75
        # if self.species[0] == 2:
        #     self.alpha = 1.0-0.75
        # Individual memory allocation to store
        # the targeted cell in the previous time step
        self.target = False
        # This status specifies if the agent is alive or not
        # To avoid removing items of the list of agents
        # while looping over it, we commit agents to die by
        # adding them to a list and changing their status so
        # other agents cannot interact with them
        self.status = True
        # self.biomass = np.random.rand(1,100)
        # self.k = 100.0
        try:
            agents.append(self)
            herbivores.append(self)
        except:
            print('agent missing = ', self)
            self.show()
            print('agent status : ', self.status)
        


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
                    self.target = False
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

        for i in range(len(predators)):
            # If there is predator(s) in visible surroundings
            # Then flee in opposite direction
            if self.distance_pos(predators[i].pos()) <= self.v\
               and predators[i].status == True:
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
        if self.biomass >= 160.0:
            if rd.randint(0, 1) == 1:
                xpos = self.x + 10.0
            else:
                xpos = self.x - 10.0
            if rd.randint(0, 1) == 1:
                ypos = self.y + 10.0
            else:
                ypos = self.y - 10.0
            self.biomass = self.biomass - 80.0
            herbivore(xpos, ypos)
            
# -----------------------------------------------------------------

    def update(self, grid):

        self.metabolic_cost()
        self.death(False)
        # If the agent died not of the following takes place
        if self.status:
            # if self.status  == True: is equivalent to ifsefl.status:
            # Calling the search() function multiple times can cause to obtain different
            # value returned (in the case of predators), calling it only once and
            # storing the returned value avoid this type of error.
            search_result = self.search(grid)
            # If there is predator(s) in visible surroundings
            # Then flee in opposite direction
            if self.fleeing():
                return 0
            elif self.biomass >= 150.0:
                self.reproduce()
                return 0
            # Then look for resource to consume nearby
            # (within their vision radius)
            elif search_result == 0:
            # elif self.search(grid) == 0:
                # If there is no resource move at random
                # to a new position
                self.random_movement()
                return 0
            elif search_result != 1 and search_result != 0:
            # elif self.search(grid) != 1 and self.search(grid) != 0 :
                # If there is available resources nearby
                # move towards the resource
                self.move_to(search_result)
                # self.move_to(self.search(grid))
                return 0
        else:
            return 0



####################################################
####################################################
####################################################



class predator(agent):
    
    def __init__(self, xpos, ypos):

        super().__init__()
        # global predators
        self.x = xpos
        self.y = ypos
        # Body radius
        self.r = 10
        # Dispersal distance
        self.d = 10.0
        # Vision radius
        self.v = 40.0
        # self.species = rd.randint(1,2)
        self.species = ('PREDATOR', 1)
        self.biomass = 80.0  # rd.random()
        self.max_biomass = 200.0
        self.colour = (255, 0, 0)
        self.thickness = 3
        # Individual memory allocation to store
        # the targeted cell in the previous time step
        self.target = False
        # This status specifies if the agent is alive or not
        # To avoid removing items of the list of agents
        # while looping over it, we commit agents to die by
        # adding them to a list and changing their status so
        # other agents cannot interact with them
        self.status = True
        # self.biomass = np.random.rand(1,100)
        # self.k = 100.0
        try:
            agents.append(self)
            predators.append(self)
        except:
            print('agent missing = ', self)
            self.show()
            print('agent status : ', self.status)
        
        def __str__(self):
            return str(self.predator_id)


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
        
        # if self.target != False and\
        #    self.distance_pos(self.target.pos())-(self.r+self.target.r)\
        #         <= 0.0:
        #     self.consume(self.target)
        #     self.target = False
        #     return 1
        # elif self.target != False and\
        #    self.distance_pos(self.target.pos())-(self.r+self.target.r)\
        #         <= self.v:
        #     return target            
        
        # Searching for the closest herbivore, within its vision radius
        # Verify if consumption is possible:
        # - the herbivore is part of the consumer diet
        for i in range(len(herbivores)):
            if self.distance_pos(herbivores[i].pos())\
                   -(self.r+herbivores[i].r) <= self.v\
                   and herbivores[i].status == True:
                consumables.append( (herbivores[i], max(self.distance_pos(herbivores[i].pos())-(self.r+herbivores[i].r), 0.0)) )
        if not consumables:
            return 0
        else:
            for i in range(len(consumables)):
                # TESTING FOR THE FORMULA:
                # U(0,1) < ALPHA * 2**-(d/max/6)
                if rd.uniform(0,1) <= consumables[i][0].alpha*\
                   2**(consumables[i][1]/self.v/6):
                    if consumables[i][1] <= 0.0:
                        # Any herbivore at distance 0.0 will do!
                        # No need to use a looot more memory
                        self.consume(consumables[i][0])
                        # self.target = False
                        # print('CONSUMPTION')
                        return 1
                    else:
                        # target = consumables[i][0]
                        return consumables[i][0]
                # IF NOTHING WAS SUCCESSFUL
                # print('FAIL')
                return 0
                    

# -----------------------------------------------------------------

    def reproduce(self):

        # global herbivores
        # IF THE ANIMAL HAS ENOUGH BIOMASS
        # IT CAN REPRODUCE ASEXUALLY
        if self.biomass >= 160.0:
            if rd.randint(0, 1)==1:
                xpos = self.x + 10.0
            else:
                xpos = self.x - 10.0
            if rd.randint(0, 1)==1:
                ypos = self.y + 10.0
            else:
                ypos = self.y - 10.0
            self.biomass = self.biomass - 80.0
            predator(xpos, ypos)
            
# -----------------------------------------------------------------            

    def update(self, grid):

        self.metabolic_cost()
        self.death(False)
        
        # If the agent died none of the following takes place
        if self.status == True:
            # Calling the search() function multiple times can cause to obtain different
            # value returned (in the case of predators), calling it only once and
            # storing the returned value avoid this type of error.
            search_result = self.search(grid)

            if self.biomass >= 150.0:
                self.reproduce()
                return 0

            # Look for resource to consume nearby
            # (within their vision radius)
            elif search_result == 0:
                # If there is no resource move at random
                # to a new position
                self.random_movement()
                return 0
            elif search_result == 1:
                return 0
            elif search_result != 1 and search_result != 0 :
                # If there is available resources nearby
                # move towards the resource
                # self.move_to(self.search(grid))
                self.move_to(search_result)
                return 0
        else:
            return 0

# -----------------------------------------------------------------            

def update_all_agents(graphic, screen, grid):
    # global agents
    total_herbivores = 0
    total_herbivores1 = 0
    total_herbivores2 = 0
    total_predators = 0

    # print(f" len avant: {len(agents)}")
    for ag in agents:
        if graphic == True:
                ag.display(screen)
        if ag.status == True:
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

    # print(f"len apres {len(agents)}")
    remove_dead_agents()
    count = [ total_herbivores, total_herbivores1, total_herbivores2, total_predators ]
    return count

# -----------------------------------------------------------------

def remove_dead_agents():
    for d in dead_agents:
        agents.remove(d)
        if d.__class__.__name__ == 'herbivore':
            herbivores.remove(d)
        else:
            predators.remove(d)


        del d
    # Clearing all the items from the list
    dead_agents.clear()
    # print('Purging dead animals from the simulation')
    return 0
        
####################################################
####################################################
####################################################


def stop_criteria(count):
    # global herbivores
    # global predators

    if count[1] == 0 or count[2] == 0 or count[3] == 0:

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