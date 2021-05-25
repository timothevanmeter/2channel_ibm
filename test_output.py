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
import itertools
###############################################

output = pd.DataFrame()

# -----------------------------------------------------------------

def reset_output():
    
    global output
    output = pd.DataFrame()

# -----------------------------------------------------------------
    
def save_output(day, biom1, biom2, ther, her1, her2, tpre):

    global output
    temp = pd.DataFrame({'Time':[day],\
                         'Resource1':[biom1],\
                         'Resource2':[biom2],\
                         'Herbivores':[ther],\
                         'Herbivores1':[her1],\
                         'Herbivores2':[her2],\
                         'Predators':[tpre]\
                         })
    output = output.append(temp)

# -----------------------------------------------------------------
    
def write_output(sim_num, replicates_number):

    global output
    master_dir = '/home/timothe/virtualenvs/test-ibm/'
    out_name = 'configuration_' + str(int(sim_num/replicates_number)) \
        + '/simulation_' + str(sim_num) + '_output.csv'
    out_dir = 'configuration_' + str(int(sim_num/replicates_number))
    out_full_path = os.path.join(master_dir, out_name)
    output.to_csv(out_full_path, index=False)
    return (os.path.join(master_dir, out_dir))

# -----------------------------------------------------------------
    
def graph_output(out_dir, sim_num):
    os.chdir(out_dir)
    
    sim = str('sim_num=\''+str(sim_num)+'\'')
    args = ['gnuplot',  '-e', sim, '/home/timothe/virtualenvs/test-ibm/test_graph.gp']
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    output, error = process.communicate()

# -----------------------------------------------------------------

def create_output(sim_num, replicates_number):
    out = write_output(sim_num, replicates_number)
    graph_output(out, sim_num)

# -----------------------------------------------------------------

    
def create_sim_dir(replicates_number):

    # Obtain number of simuilations to run
    with open('number_of_simulation_to_run.txt', 'r') as f:
        sim_num = int(int(f.read())/replicates_number)
    
    master_dir = '/home/timothe/virtualenvs/test-ibm/'
    # Create the appropriate folders for each simulation
    for i in range(0, sim_num):
        sim_id = 'configuration_' + str(i)
        sim_dir = os.path.join(master_dir, sim_id)
        os.mkdir(sim_dir)
	# Make folders for the replicates
	# if(replicates_number <= 1):
	#     create all configuration files in sim_dir
	#     try:
        #         create_config_files(config_dir,sim_dir)
	# else:
	#     create all configuration files in each rep_dir
        #     Create sim_dir
        #     os.mkdir(sim_dir)
        #     status = replication(replicates_number,sim_dir)



#-----------------------------------------------------
