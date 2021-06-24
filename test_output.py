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
  
  
    master_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test-ibm/')
    sim_id = 'configuration_' + str(int(sim_num/replicates_number))
    sim_dir = os.path.join(master_path, sim_id)
    file_name = 'simulation_' + str(int(sim_num/replicates_number)) + '_output.csv'
    
    out__path = os.path.join(os.path.dirname(os.path.abspath(__file__)), sim_dir, file_name)
    out_full_path = os.path.abspath(out__path)
    print(out_full_path)
    # print(output)
    output.to_csv(out_full_path, index=False)
    print("created file")
    # return (os.path.join(out_full_path, out_dir))
    return out_full_path

# -----------------------------------------------------------------
    
def graph_output(out_dir, sim_num):
    os.chdir(out_dir)
    
    sim = str('sim_num=\''+str(sim_num)+'\'')
    args = ['gnuplot',  '-e', sim, '/test_graph.gp']
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    output, error = process.communicate()

# -----------------------------------------------------------------

def create_output(sim_num, replicates_number):
    out = write_output(sim_num, replicates_number)
    # graph_output(out, sim_num)

# -----------------------------------------------------------------

    
def create_sim_dir(replicates_number):

    # Obtain number of simuilations to run
    with open('number_of_simulation_to_run.txt', 'r') as f:
        sim_num = int(int(f.read())/replicates_number)

    master_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test-ibm/')
    # Create the appropriate folders for each simulation
    print(master_path)
    if os.path.exists(master_path):
        print("exists")
        import shutil
        shutil.rmtree(master_path)
        os.mkdir(master_path)
    else:
        os.mkdir(master_path)
    for i in range(0, sim_num):
        sim_id = 'configuration_' + str(i)
        sim_dir = os.path.join(master_path, sim_id)
        if not os.path.exists(sim_dir):
            os.mkdir(sim_dir)
        else:
            os.mkdir(master_path)
            os.mkdir(sim_id)