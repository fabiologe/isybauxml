from shapely.geometry import box, Point
from pyproj import CRS, exceptions
from xml_parser import *
from hydraulik.utils import site_middle
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd




def within_crs_bounds(epsg_code, x, y):
    '''
    Returns TRUE if point (x,y) is within the bounds of the
    given projection (epsg_code)
    otherwise returns FALSE

    '''
    try:
        crs = CRS.from_user_input(epsg_code)
        if(crs.area_of_use.west <= x <= crs.area_of_use.east) and (crs.area_of_use.south <= y <= crs.area_of_use.north):
                result = True
        else: 
                print(f"Invalid projection for EPSG code {epsg_code}")
                result = False
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        result = False
    return result


def find_CRS():
    x, y = site_middle(schacht_list)
    print(f'Find matching CRS for: {x, y}')
    all_crs = 'orientation/coordinate_reference_system.csv'
    try:
        with open(all_crs, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            matching_found = False
            for row_num, row in enumerate(reader, start=1):
                epsg_code = int(row['COORD_REF_SYS_CODE'])
                matching_found = within_crs_bounds(epsg_code, x, y)
                if matching_found:
                    print("Matching CRS found:")
                    print("EPSG Code:", epsg_code)
                    print("CRS Name:", row['CRS_NAME'])
                    break  # Exit the loop once a matching CRS is found
            
            if not matching_found:
                print("No matching CRS found.")
                print('GK3= 31467 , GK2 = 31466 , UTM32N = 25832')
                given_crs =int(input(f'Enter CRS as EPSG:'))
                
                return given_crs
                
    except FileNotFoundError:
        print(f"Error: File '{all_crs}' not found.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


def find_CRSfromXML(x,y):
    print(f'Find matching CRS for: {x, y}')
    all_crs = 'orientation/coordinate_reference_system.csv'
    try:
        with open(all_crs, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            matching_found = False
            for row_num, row in enumerate(reader, start=1):
                epsg_code = int(row['COORD_REF_SYS_CODE'])
                matching_found = within_crs_bounds(epsg_code, x, y)
                if matching_found:
                    print("Matching CRS found:")
                    print("EPSG Code:", epsg_code)
                    print("CRS Name:", row['CRS_NAME'])
                    break  # Exit the loop once a matching CRS is found
            
            if not matching_found:
                print("No matching CRS found.")
                print('GK3= 31467 , GK2 = 31466 , UTM32N = 25832')
                given_crs =int(input(f'Enter CRS as EPSG:'))
                
                return given_crs
                
    except FileNotFoundError:
        print(f"Error: File '{all_crs}' not found.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

