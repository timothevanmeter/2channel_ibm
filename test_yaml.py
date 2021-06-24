##########################
# YAML READER
##########################

import yaml
import pandas as pd

# sim = pd.read_csv("/home/timothe/virtualenvs/test-ibm/sim_summary.csv")

# -------------------------------------------


def read(category, parameter_name, sim_num):

    sim = pd.read_csv("sim_summary.csv")
    
    with open('ibm_config.yml') as f:
        
        config = yaml.load(f, Loader=yaml.FullLoader)
        # If the parameter has variable values for the simulation
        # looks for the appropriate value in the sim_summary.csv
        # table
        if config[category][parameter_name] == "variable":
            return sim[parameter_name][sim_num]

        # Otherwise use the value listed in the yaml
        # configuration file
        return config[category][parameter_name]

    
# print(read('predator', 'initial_number_individuals', 0))

# -------------------------------------------


def read_plain(category, parameter_name):
    with open('ibm_config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config[category][parameter_name]
