from pyswmm import Simulation
import swmmio
from hydraulik.utils import latest_inp ,check_crs
from typing import List
from xml_parser import * 
from uuid import uuid4

def guid6():
    guid = uuid4()
    guid_str = str(guid)
    return guid_str
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

def default_plot(schacht_list:List):
    guid_str = guid6()
    directory = 'hydraulik/inp'
    file_pattern = 'model'
    file_name = f'hydraulik/inp{guid_str}'
    # Get the latest file
    try:
        latest_file = latest_inp(directory, file_pattern)
        print(f"The latest file is: {latest_file}")
        
        crs_check = check_crs(schacht_list)
        print(f"Determined CRS code: {crs_check}")
        
        crs = f'epsg:{crs_check}' 
        #crs_test = 'epsg:3728'
        simulation_info = swmmio.Model(latest_file, crs=crs)
        
        swmmio.create_map(simulation_info, filename=file_name)
        print(f"Map created successfully: {file_name}")
        
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
    return
