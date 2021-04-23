###############################################
# Author of this project: Timothe van Meter

# Last modification: March 29th 2021

# Contact: tvanme2@uic.edu

# License: GNU General Public License version 3
# https://opensource.org/licenses/GPL-3.0
###############################################
import pandas as pd
import subprocess
import os
###############################################

output = pd.DataFrame()

# -----------------------------------------------------------------
    
def save_output(day, biom, ther, her1, her2, tpre):

    global output
    temp = pd.DataFrame({'Time':[day],\
                         'Resource':[biom],\
                         'Herbivores':[ther],\
                         'Herbivores1':[her1],\
                         'Herbivores2':[her2],\
                         'Predators':[tpre]\
                         })
    output = output.append(temp)

# -----------------------------------------------------------------
    
def write_output():

    global output
    output.to_csv('test_output.csv', index=False)

# -----------------------------------------------------------------
    
def graph_output():
    gnuplot = "gnuplot test_graph.gp"
    process = subprocess.Popen(gnuplot.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    
# def store_output():

# # Create the appropriate folders for each simulation 

# for i in range(0, r_csv-1):
   
# 	sim_id = 'configuration_' + str(i)
# 	sim_dir = os.path.join(master_dir, sim_id)
	
# 	# Make folders for the replicates
# 	if(num_replication <= 1):
# 		# create all configuration files in sim_dir
# 		try:
# 			create_config_files(config_dir,sim_dir)
		
# 	else:
# 		# create all configuration files in each rep_dir
#                 # Create sim_dir
#                 os.mkdir(sim_dir)
#                 status = replication(num_replication,sim_dir)


#-----------------------------------------------------




