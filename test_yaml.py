##########################
# YAML READER
##########################

import yaml


def read_yaml(category, parameter_name):
    with open('ibm_config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

        return config[category][parameter_name]

cat = 'ibm_display'
name = 'delay_between_frames'
print("value =", read_yaml(cat,name))
