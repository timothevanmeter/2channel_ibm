###############################################
# Author of this project: Timothe van Meter

# Last modification: January 5th 2021

# Contact: tvanme2@uic.edu

# License: GNU General Public License version 3
# https://opensource.org/licenses/GPL-3.0
###############################################
# import matplotlib
import random as rd
import numpy as np
# import matplotlib.pyplot as plt
import math
import test_display as disp

# New Model test

cell_size = 10
# Expressed in number of cells:
grid_size = 40

plot_size = (cell_size+1)*grid_size

##################################################
##################################################
def distance(cell_a, cell_b):

    d = round(math.sqrt( (cell_a.x - cell_b.x)**2 + (cell_a.y - cell_b.y)**2 ), 1)
    return d


##################################################
##################################################

class cell():

# -----------------------------------------------------------------                        
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.species = rd.randint(1,2)
        # self.species = 1
        self.biomass = 5.0
        #rd.random()
        # self.biomass = np.random.rand(1,100)
        self.k = 100.0
        self.thickness = 3
        self.colour = (255, 255, 255)
        # color for carrying capacity: (74, 158, 0)
        # intermediate 1: (102, 218, 0)
        # intermediate 2: (120, 255, 1)        
        # color for empty: (255, 255, 255)
        self.size = 10

# -----------------------------------------------------------------                        
    def display(self, screen):
        disp.display_cell(screen, self.colour, self.x+2*cell_size, self.y+2*cell_size, self.size, self.size)

# -----------------------------------------------------------------                        
    def size_value(self):
    	return self.size
# -----------------------------------------------------------------                        
    def k_value(self):
    	return self.k
# -----------------------------------------------------------------                        
    def biomass_value(self):
    	return self.biomass
# -----------------------------------------------------------------                        
    def update_biomass(self, m):
    	self.biomass = m  
# -----------------------------------------------------------------                        
    def change_colour(self, col):
    	self.colour = col
# -----------------------------------------------------------------                        
    def update_colour(self):
        if self.species == 3:
            return 0
        if self.species == 1:
            if self.biomass > 50.0:
                if self.biomass == self.k:
                    self.colour = (74, 158, 0)
                else:
                    self.colour = (102, 218, 0)
            elif self.biomass == 0:
                self.colour = (255, 255, 255)
            else:
                self.colour = (120, 255, 1)

        elif self.species == 2:
            if self.biomass > 50.0:
                if self.biomass == self.k:
                    self.colour = (183, 0, 171)
                else:
                    self.colour = (223, 0, 208)
            elif self.biomass == 0:
                self.colour = (255, 255, 255)
            else:
                self.colour = (255, 0, 239)
# -----------------------------------------------------------------                    
    def growth(self, update):
        # Resource's growth rate
        r = 0.0
        if self.species == 1:
            r = 0.05
        elif self.species == 2:
            r = 0.05

        g = round(self.biomass*(1 + r),1)#   * (1 - self.biomass/self.k))
        # Is the resource exceeding the cell's carrying capacity?
        if g <= self.k:
            if update == True:
                self.biomass = g
            return 0
        else:
            if update == True:
                self.biomass = self.k
            return round(g-self.k,1)

# -----------------------------------------------------------------                    
    def show(self):
        print('Species:', self.species,'', 'x=', self.x,'', 'y=', self.y,'', 'biomass=', self.biomass) 
    
# -----------------------------------------------------------------                    
    def pos(self):
    	pos = (self.x, self.y)
    	return pos

##################################################
##################################################

# class border_cell():
class border_cell(cell):
    
# -----------------------------------------------------------------                        
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.species = 3
        self.thickness = 3
        self.colour = (139, 136, 136)
        self.size = 10

##################################################
##################################################

class lattice():

# -----------------------------------------------------------------                        
    def __init__(self,s):

        global cell_size

        self.cells = []
        self.borders = []
        # self.sp1 = []
        # self.sp2 = []
        self.s = s
        # The +1 is here to correct for the presence of the 4 layers
        # of border cells around the grid.
        for i in range(self.s):
            for j in range(self.s):
                # Conditions to create a surrounding layer of
                # inactive cells, of class border_cell()
                corner = False
                border = False
                if i==0:
                    border = True
                    if j==0:
                        corner = True
                        cl = border_cell(i*(cell_size+1), j*(cell_size+1))
                    elif j==self.s-1:
                        corner = True
                        cl = border_cell(i*(cell_size+1), j*(cell_size+1))
                    else:
                        cl = border_cell(i*(cell_size+1), j*(cell_size+1))
                        
                elif i==self.s-1:
                    border = True
                    if j==0:
                        corner = True
                        cl = border_cell(i*(cell_size+1), j*(cell_size+1))
                    elif j==self.s-1:
                        corner = True
                        cl = border_cell(i*(cell_size+1), j*(cell_size+1))
                    else:
                        cl = border_cell(i*(cell_size+1), j*(cell_size+1))
                        
                elif j==0 and corner==False:
                    border = True
                    cl = border_cell(i*(cell_size+1), j*(cell_size+1))
                elif j==self.s-1 and corner==False:
                    border = True
                    cl = border_cell(i*(cell_size+1), j*(cell_size+1))

                else:
                    cl = cell(i*(cell_size+1), j*(cell_size+1))
                # cl = cell(i*(cell_size+1), j*(cell_size+1))
                # if cl.species == 1:
                #     self.sp1.append(cl)
                # else:
                #     self.sp2.append(cl)
                if border == False:
                    self.cells.append(cl)
                else:
                    self.borders.append(cl)
                corner = False
                border = False

# -----------------------------------------------------------------

    def update(self):
        to_spread = []
        # The self.s - 2 is to take into account the border cells
        for i in range((self.s-2)**2):
            # For biomass spreading
            if self.cells[i].growth(False) != 0:
                # print('SPREADING')
                # Commiting cells to spread after growth has been processed for every cell
                to_spread.append(self.cells[i])
                # self.spread(self.cells[i].species, self.cells[i].x, self.cells[i].y, self.cells[i].growth())
            else:
                # print('NOT SPREADING')
                # Allow growth for cells that are not spreading this time step
                self.cells[i].growth(True)
        # Calling the spread procedures for the cells with extra biomass
        for i in range(len(to_spread)):
            self.spread(to_spread[i])
        # Updating the colors for all cells depending
        # on current biomass value
        # The self.s - 2 is to take into account the border cells
        for i in range((self.s-2)**2):
            self.cells[i].update_colour()
            


    # GENERAL VERSION OF THE spread() PROCEDURE
# -----------------------------------------------------------------                    
    def spread(self, cell):

        global cell_size
        # Look for 'neighboring' cells with the conditions:
        # - Cell carrying capacity is not already reached
        # - Is indeed a neighbor, not too far away
        # - Not the cell spreading
        # - Of the same species as the cell spreading or
        # uncolonised yet
        neighbors = []
        for i in range(len(self.cells)):
            if self.cells[i].biomass != self.cells[i].k  \
               and  distance(cell, self.cells[i]) <= round(math.sqrt(2)*(cell_size+1),1) \
               and cell != self.cells[i] and \
                   (cell.species == self.cells[i].species or self.cells[i].species == 0):
                
                neighbors.append(i)
                
        try:
            sup = round(cell.growth(True)/len(neighbors),1)
        except ZeroDivisionError:
            sup = 0.0
            # print('No available neighbors for cell at','(',cell.x,',',cell.y,')')
        rest = 0.0
        for i in range(len(neighbors)):
            if self.cells[neighbors[i]].k < self.cells[neighbors[i]].biomass + sup + rest:
                self.cells[neighbors[i]].biomass = round(self.cells[neighbors[i]].k,1)
                rest += self.cells[neighbors[i]].biomass + sup + rest - self.cells[neighbors[i]].k
            else:
                self.cells[neighbors[i]].biomass = round(self.cells[neighbors[i]].biomass + sup + rest,1)
            if self.cells[neighbors[i]].species == 0:
                # If the neighbor cell is uncolonised it is colonnised
                # through the spreading
                self.cells[neighbors[i]].species = cell.species
                
# -----------------------------------------------------------------                    
    def size(self):

        return self.s

# -----------------------------------------------------------------                    
    def generate_x(self):

        x = []
        for i in range(len(self.cells)):
            x.append(self.cells[i].x)
            # y.append(self.cells[i].y)
        return x

# -----------------------------------------------------------------                    
    def generate_y(self):

        y = []
        for i in range(len(self.cells)):
            y.append(self.cells[i].y)
            # y.append(self.cells[i].y)
        return y

# -----------------------------------------------------------------                    
    def generate_biomass(self):

        b = np.empty(shape=(self.s, self.s))
        j = 0
        u = 0
        for i in range(len(self.cells)):
            if (i+1)%self.s != 0:
                b[j][u] = self.cells[i].biomass
                u += 1
            else:
                b[j][u] = self.cells[i].biomass
                u = 0
                j += 1
        return b
                    
# -----------------------------------------------------------------                    
    def print(self):
        for i in range(self.s**2):
                self.cells[i].show()


##################################################

# NOTE:
# If enough time try to see, on paper at first, if a truely spatially homogeneous
# spread of the resource is possible to obtain in the model.

############################################################################

    def update_all_cells(self, graphic, screen):

        biomass_1 = 0.0
        biomass_2 = 0.0
        # Update and display all cells 
        for cell in self.cells:
            if cell.species == 1:
                biomass_1 += cell.biomass_value()
            elif cell.species == 2:
                biomass_2 += cell.biomass_value()
            if graphic ==True:
                cell.display(screen)
        for border in self.borders:
            if graphic ==True:
                border.display(screen)
        self.update()
        
        return (round(biomass_1/150, 0), round(biomass_2/150, 0))

