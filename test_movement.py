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
import test_resource as res

# New Model test

cell_size = 10
# Expressed in number of cells:
grid_size = 40

# To account for the border cells
plot_size = (cell_size+1)*grid_size

agents = []
herbivores = []

##################################################

background_colour = (255,255,255)
(width, height) = (plot_size+200, plot_size+200)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('IBM Monitor Display')
screen.fill(background_colour)
# clock = pygame.time.Clock()

##################################################
def distance_agents(agent_a, agent_b):

    d = round(math.sqrt( (agent_a.x - agent_b.x)**2 + (agent_a.y - agent_b.y)**2 ), 1)
    return d

##################################################
def distance_agent_pos(agent_a, pos):

    d = round(math.sqrt( (agent_a.x - pos[0])**2 + (agent_a.y - pos[1])**2 ), 1)
    return d

##################################################

class agent():

# -----------------------------------------------------------------                        
    def __init__(self, xpos, ypos):

        global agents
        self.x = xpos
        self.y = ypos
        # Body radius
        self.r = 10.0
        # Dispersal distance
        self.d = 40.0
        # self.species = rd.randint(1,2)
        self.species = ('AGENT', 0)
        self.biomass = 50 #rd.random()
        self.colour = (0, 0, 255)
        self.thickness = 3
        # self.biomass = np.random.rand(1,100)
        # self.k = 100.0
        agents.append(self)
    
# -----------------------------------------------------------------                        
    def display(self):
        global cell_size
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.r, self.thickness)

# -----------------------------------------------------------------
    def distance_pos(self, pos):

        d = round(math.sqrt( (self.x - pos[0])**2 + (self.y - pos[1])**2 ), 1)
        return d
# -----------------------------------------------------------------
    # check_bounds(x, y) is a recursive function verifying that the two
    # new coordinates, x and y passed for an agent are within the bounds of
    # the grid environment.
    def check_bounds(self, xpos, ypos):
        
        global plot_size
        global cell_size
        # grid = plot_size-cell_size
        # If the new position is within the bounds of
        # the grid we accept it and send it back.
        # grid.size = 100
        if (xpos > self.r+cell_size) and (xpos < plot_size-cell_size-self.r) and (ypos > self.r+cell_size) and (ypos < plot_size-cell_size-self.r):
            return xpos, ypos
        else:
            # If xpos is beyond bounds.
            # We redraw the xpos
            if (xpos < self.r+cell_size) or (xpos > plot_size-cell_size-self.r):
                return self.check_bounds(round(self.x + rd.uniform(-self.d, self.d),1), ypos)
            # If ypos is beyond bounds.
            # We redraw the ypos
            if (ypos < self.r+cell_size) or (ypos > plot_size-cell_size-self.r):
                return self.check_bounds(xpos, round(self.y + rd.uniform(-self.d, self.d),1))
        
# -----------------------------------------------------------------                    
    def random_movement(self):
        
        global agents
        max_attempts = 10
        newpos = ()
        new = True
        collision = False
        for i in range(max_attempts):
            # To monitor possible RecursionError
            newpos = (self.check_bounds(round(self.x + rd.uniform(-self.d, self.d),1), round(self.y + rd.uniform(-self.d, self.d),1)))
            if newpos is None:
                # print("PROBLEM")
                new = False

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
    def show(self):
        # print('Species:', self.species[0],self.species[1],'', 'x=', self.x,'', 'y=', self.y,'', 'biomass=', self.biomass)
                print('Biomass=', self.biomass)

        
####################################################

class herbivore(agent):
    
    def __init__(self, xpos, ypos):

        global agents
        global herbivores
        self.x = xpos
        self.y = ypos
        # Body radius
        self.r = 10
        # Dispersal distance
        self.d = 10.0
        # Vision radius
        self.v = 1000.0
        # self.species = rd.randint(1,2)
        self.species = ('HERBIVORE', 1)
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

    def search(self, grid):

        global grid_size
        consumables = []
        
        # If the targeted cell in the previous time step
        # is within consumption range then consume it
        if self.target != False and\
           distance_agent_pos(self, self.target.pos()) == 0.0:
            
            # self.consume(self.target)
            
            self.target = False
            return 1
        
        # Searching for the closest cell, within its vision radius
        # Verify if consumption is possible:
        # - the resource is part of the consumer diet AND
        # - the resource's biomass is non-null
        for i in range(grid_size**2):
            if (self.distance_pos(grid.cells[i].pos()) <= self.v \
                and self.species[1] == grid.cells[i].species \
                and grid.cells[i].biomass != 0):
                
                if (distance_agent_pos(self, grid.cells[i].pos()) == 0.0)\
                   and grid.cells[i].biomass == grid.cells[i].k_value():#\
                   # or grid.cells[i].biomass >= self.target.biomass:
                    # Any cell at distance 0.0 with maximum or
                    # more biomass than previous target will do!
                    # No need to use a looot more memory
                    
                    # self.consume(grid.cells[i])

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
            # min = consumables[0][1]
            max = consumables[0][1]
            target = consumables[0][0]
            for i in range(len(consumables)):
                if consumables[i][1] > max:
                    max = consumables[i][1]
                    # Ensures that there is only one target
                    # even if there are multiple maxima
                    # Send only the cell object and not the
                    # associated biomass
                    # (distance in the older version)
                    target = consumables[i][0]
                
            # If the previously targeted cell:
            # - still exists
            # - is different from the renewed target (see above)
            # - has a greater biomass than the renewed target
            # Then, continue to move towards that cell
            red = (255, 0, 0)
            target.change_colour(red)
            if self.target != False \
               and target != self.target \
                   and self.target.biomass >= target.biomass:
                return self.target
            # Otherwise, move towards renewed target 
            else:
                self.target = target
                return target

# -----------------------------------------------------------------

    # def move_to(self, cell):
        
    #     # Obtain the general direction for the movement
    #     pos = cell.pos()

    #     # TEST 
    #     # self.x = pos[0]
    #     # self.y = pos[1]
    #     # return 0
    #     # FIN TEST
    
    #     dispx = 0.0
    #     dispy = 0.0

    #     if abs(pos[0]-self.x) <= self.d:
    #         self.x = pos[0]
    #     else:
    #         dispx = self.d
            
    #     if abs(pos[1]-self.y) <= self.d:
    #         self.y = pos[1]
    #     else:
    #         dispy = self.d

    #     if pos[1] > self.y and pos[0] > self.x or pos[1] < self.y and pos[0] < self.x:
    #         alpha = math.atan2(self.y-pos[1], self.x-pos[0])
    #         self.x += -round(math.sin(alpha) * dispx,1)
    #         self.y += -round(math.cos(alpha) * dispy,1)

    #     elif pos[1] == self.y:
    #         alpha = math.atan2(self.y-pos[1], self.x-pos[0])
    #         self.x += -round(math.cos(alpha) * dispx,1)
                        
    #     elif pos[0] == self.x:
    #         alpha = math.atan2(pos[1]-self.y, pos[0]-self.x)
    #         self.y += round(math.sin(alpha) * dispy,1)
    #     else:
    #         alpha = math.atan2(self.y-pos[1], self.x-pos[0])
    #         self.x += round(math.sin(alpha) * dispx,1)
    #         self.y += round(math.cos(alpha) * dispy,1)

# -----------------------------------------------------------------
            
    def move_to(self, cell):
        
        # Obtain the general direction for the movement
        pos = cell.pos()    
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

    def update(self, grid):

        # self.metabolic_cost()
        # self.death()

        # First search for the presence of a predator

        # TO DO

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
        #     # If there is available resources nearby
        #     # move towards the resource
            self.move_to(self.search(grid))
            # print("agent=",self, " target=",self.search(grid), )
            # print("biomass=",self.search(grid).biomass_value())
            # print("DIRECTED MOVEMENT")
            return 0

# -----------------------------------------------------------------       




####################################################

herbivore(20, 20)
herbivore(20, 20)
herbivore(20, 20)
herbivore(20, 20)

herbivore(20, 400)
herbivore(20, 400)
herbivore(20, 400)
herbivore(20, 400)

herbivore(400, 20)
herbivore(400, 20)
herbivore(400, 20)
herbivore(400, 20)

herbivore(400, 400)
herbivore(400, 400)
herbivore(400, 400)
herbivore(400, 400)

grid = res.lattice(grid_size+2)


# grid.cells[29].species = 1
# grid.cells[29].update_biomass(100.0)

# grid.cells[780].species = 1
# grid.cells[780].update_biomass(100.0)
# grid.cells[780].update_colour()

grid.cells[1499].species = 1
grid.cells[1499].update_biomass(100.0)
grid.cells[1499].update_colour()

# grid.cells[1400].change_colour(red)
# grid.cells[1400].update_biomass(100.0)

# print('BIOMASS =', grid.cells[1400].biomass_value())

# print('target =',a.search(grid))
# print('target pos =',a.search(grid).pos())

for cell in grid.cells:
        cell.update_colour()

####################################################
# pygame.display.flip()

running = True

print("-----------------------------")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Erase previous drawings
    screen.fill(background_colour)
    for cell in grid.cells:
        cell.display(screen)
    for border in grid.borders:
        border.display(screen)
        # if cell.biomass > 0.0:
        #     print("cell biomass =", cell.biomass_value())
    grid.update()
    # for agent in agents:
    # print("# Active herbivores:", len(herbivores))
    for herb in herbivores:
        # herb.show()
        herb.update(grid)
        # agent.move_to(agent.search(grid))
        # if agent.random_movement() == True:
        #     pygame.time.wait(500)
        # try:
        #     agent.consume()
        # except:
        #     print('0')
        herb.display()
    pygame.time.wait(250)
    # print("-----------------------------")
    pygame.display.flip()

