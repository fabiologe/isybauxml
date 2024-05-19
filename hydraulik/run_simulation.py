from pyswmm import Simulation
from hydraulik.utils import latest_inp

def default_sim():  
    directory = 'hydraulik/inp'
    file_pattern = 'model'

    # Get the latest file
    try:
        latest_file = latest_inp(directory, file_pattern)
        print(f"The latest file is: {latest_file}")

        # Run the simulation with the latest file
        with Simulation(latest_file) as sim:
            for ind, step in enumerate(sim):
                if ind % 100 == 0:
                    print(round(sim.percent_complete * 100))

    except FileNotFoundError as e:
        print(e)
    return