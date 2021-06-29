###############################################
# Author of this project: Timothe van Meter

# Last modification: March 29th 2021

# Contact: tvanme2@uic.edu

# License: GNU General Public License version 3
# https://opensource.org/licenses/GPL-3.0
###############################################

import pandas as pd
import sys, os
from itertools import product
from numpy import arange

###############################################################################

# Initializing tables
par = []
try:
    par = pd.read_csv("parameters.csv",header=None)
except:
    print("parameters csv not found")
    sys.exit()

###############################################################################
def par_name(id):
    # Obtains the name for a single parameter identified by its id number
    p_name = par.loc[id,0]
    return p_name

def par_min(id):
    # Obtains the minimum for a single parameter identified by its id number
    p_min = round(par.iloc[id,1].item(), 2)
    return p_min

def par_max(id):
    p_max = round(par.iloc[id,2].item(), 2)
    return p_max

def par_step(id):
    p_step = round(par.iloc[id,3].item(), 2)
    return p_step

def par_range(id):
    # Calculates the range for a single parameter identified by its id number
    ev_range = (par_max(id) - par_min(id))/ par_step(id) + 1
    return ev_range

###############################################################################

def create_agenda(replicates_number):

    length = len(par)
    table = []
    names = []
    cum_range = 1 

    for i in range(0, length):
        table.append(list(arange(par_min(i), par_max(i)+par_step(i), par_step(i))))
        cum_range = cum_range * par_range(i)
        names.append(par_name(i))
        i = 0
    sim_summary = pd.DataFrame(index=range(int(cum_range*replicates_number)), columns = names)

    # the * operator unpacks the two sublists in table
    # REF: https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
    for xs in product(*table):
        for j in range(replicates_number):
            sim_summary.iloc[i] = list(xs)
            i += 1
    with open('number_of_simulation_to_run.txt', 'w') as f:
        f.write('%d' % i)
        f.close()
        # print(sim_summary)
        sim_summary.to_csv('sim_summary.csv')



###############################################################################
