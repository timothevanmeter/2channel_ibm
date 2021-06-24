
import pygame

import threading, queue
# -----------------------------
import test_simulation_agenda as sim
import test_yaml as yaml
# -----------------------------

print("starting")
# READING THE NUMBER OF REPLICATES FROM yaml FILE
replicates_number = yaml.read_plain('ibm_functioning', 'number_of_replicates')

# CREATING THE SIMULATION AGENDA
sim.create_agenda(replicates_number)


# -----------------------------
# IMPORT THE REST OF THE SCRIPTS ONCE
# THE SIMULATION AGENDA HAS BEEN CREATED
# TO AVOID ERRORS DUE TO ABSENCE OF TEXT FILES.
import test_resource as res
import test_animal as ani
import test_output as out
import test_display as disp
# import test_yaml as yaml
# -----------------------------
cell_size = 10
# Expressed in number of cells:
grid_size = 40

# To account for the border cells
plot_size = (cell_size+2)*grid_size

background_colour = (255, 255, 255)
##################################################
##################################################


def simulation_main(j, sim_num):
    # while True:
    print("SIMULATION", j, "/", sim_num)
    out.reset_output()

    # ------------------------------------------------------
    # READ PARAMETERS VALUE FROM YAML CONFIGURATION FILE
    init_herbivores = yaml.read('herbivore', 'initial_number_individuals', j)
    init_predators = yaml.read('predator', 'initial_number_individuals', j)
    max_time = yaml.read('ibm_functioning', 'max_simulation_time', j)
    graphic_display = yaml.read('ibm_display', 'enable_display', j)
    enable_stop = yaml.read('ibm_functioning', 'enable_stop_criteria', j)
    # ------------------------------------------------------

    if graphic_display:
        screen = disp.create_display(plot_size, cell_size)
    else:
        screen = None
    ani.init_animals(init_herbivores, init_predators)
    grid = res.lattice(grid_size+2)
    day = 0
    # ------------------------------------------------------
    if graphic_display:
        running = True
        print("-----------------------------")
        while running:
            day += 1
            print("DAY", day)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    # Erase previous drawings
            screen.fill(background_colour)
            biomass = round(grid.update_all_cells(graphic_display, screen)/150, 0)
            count = ani.update_all_agents(graphic_display, screen, grid)
            out.save_output(day, biomass, count[0], count[1], count[2], count[3])
            # Ensure that the ecosystem did not collapse
            if ani.stop_criteria(count) and enable_stop or max_time <= day:
                break
            pygame.time.wait(1000)
            pygame.display.flip()
    else:
        while day <= max_time:
            day += 1
            print("DAY ", day)
            biomass = grid.update_all_cells(graphic_display, screen)
            count = ani.update_all_agents(graphic_display, screen, grid)
            out.save_output(day, biomass[0], biomass[1], count[0], count[1], count[2], count[3])
            # Ensure that the ecosystem did not collapse
            if ani.stop_criteria(count) and enable_stop:
                break
            # ------------------------------------------------------
    out.create_output(j, replicates_number)

##################################################


# CREATING A QUEUE FOR THE SIMULATIONS
sim_queue = queue.Queue()


# DEFINING A WORKING UNIT FOR THE QUEUE
def worker():
    while True:
        item = sim_queue.get()
        # print(f'Working on {item}')
        # print(f'Finished {item}')
        sim_queue.task_done()

# OBTAINING THE NUMBER OF SIMULATIONS TO RUN
with open('number_of_simulation_to_run.txt', 'r') as f:
    sim_num = int(f.read())-1
# CREATING THE NECESSARY FOLDERS TO HOST ALL
# THE SIMULATION RESULTS
out.create_sim_dir(replicates_number)

print("console")

for j in range(int(sim_num+1)):
    sim_queue.put(simulation_main(j, sim_num))


threading.Thread(target=worker, daemon=True).start()

sim_queue.join()

##################################################
