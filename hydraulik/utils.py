from xml_parser import *
from typing import List, Tuple
import math
import re 
import os
from datetime import datetime
from collections import Counter
class hydr_point: 
    def __init__(self,x, y, objekt):
        self.x = x
        self.y = y
        self.objekt = objekt
def point_in_polygon(point_2D, polygon_2D):
    num_vertices = len(polygon_2D)
    x, y = point_2D.x, point_2D.y
    inside = False
 
    # Store the first point in the polygon and initialize the second point
    p1 = polygon_2D[0]
 
    # Loop through each edge in the polygon
    for i in range(1, num_vertices + 1):
        # Get the next point in the polygon
        p2 = polygon_2D[i % num_vertices]
 
        # Check if the point is above the minimum y coordinate of the edge
        if y > min(p1.y, p2.y):
            # Check if the point is below the maximum y coordinate of the edge
            if y <= max(p1.y, p2.y):
                # Check if the point is to the left of the maximum x coordinate of the edge
                if x <= max(p1.x, p2.x):
                    # Calculate the x-intersection of the line connecting the point to the edge
                    x_intersection = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
 
                    # Check if the point is on the same line as the edge or to the left of the x-intersection
                    if p1.x == p2.x or x <= x_intersection:
                        # Flip the inside flag
                        inside = not inside
 
        # Store the current point as the first point for the next iteration
        p1 = p2
 
    # Return the value of the inside flag
    return inside
'''
def get_polygon2D(flaechen_list):
    for polygon in flaechen_list:
        num_vertices = len(polygon.points)
    return num_vertices

for flaeche in flaechen_list:
    point = point_2D(fefefefefef)
    point_in_polygon(point, polygon)'''
hydr_point_list= []

def zulauf_to_2d(haltung_list):
    for haltung in haltung_list:
        print(f"Haltung:{haltung.objektbezeichnung}")
        num_kanten = len(haltung.kanten)
        print(f"Anzahl Kanten{num_kanten}")
        for i in range (0,num_kanten):
            x= float(haltung.kante[i].punkte[0].x)
            y= float(haltung.kante[i].punkte[0].y)
            objekt = haltung.objektbezeichnung
            
            point = hydr_point(x,y, objekt)
            hydr_point_list.append(point)

    return hydro_poly_list

def ablauf_to_2d(haltung_list):
    for haltung in haltung_list:
        print(f"Haltung:{haltung.objektbezeichnung}")
        num_kanten = len(haltung.kanten)
        print(f"Anzahl Kanten{num_kanten}")
        for i in range (0,num_kanten):
            x= float(haltung.kante[i].punkte[1].x)
            y= float(haltung.kante[i].punkte[1].y)
            objekt = haltung.objektbezeichnung

            point = hydr_point(x,y, objekt)
            hydr_point_list.append(point)
    return hydro_poly_list

hydro_poly_list =[]

def flaeche_2D(flaeche):
        print(f"Flaeche:{flaeche.flaechenbezeichnung}")
        num_kanten = len(flaeche.kanten)
        print(f"Anzahl Kanten{num_kanten}")
        for i in range (0,num_kanten):
            x= float(flaeche.kante[i].punkte[0].x)
            y= float(flaeche.kante[i].punkte[0].y)
            objekt = flaeche.flaechenbezeichnung
            point = hydr_point(x,y, objekt)
            hydro_poly_list.append(point)
            x= float(flaeche.kante[i].punkte[1].x)
            y= float(flaeche.kante[i].punkte[1].y)
            objekt = flaeche.flaechenbezeichnung

            point = hydr_point(x,y, objekt)
            hydro_poly_list.append(point)
        return hydro_poly_list
    
def check_point_poly():
    for flaeche in flaechen_list:
        polygon_2D = flaeche_2D(flaeche)
        hydr_point_list = zulauf_to_2d(haltung_list)
        hydr_point_list= ablauf_to_2d(haltung_list)
        for point in hydr_point_list:
            point_in_polygon(point, polygon_2D)

def remove_outfall_double(junction_list: List, outfall_list: List) -> List:
    outfall_names = {outfall.name for outfall in outfall_list if outfall.name is not None}
    return [junction for junction in junction_list if junction.name not in outfall_names]

def site_middle(schacht_list: List):
    schacht_coord = []
    total_x = 0
    total_y = 0
    count = 0

    for schacht in schacht_list:
        for knoten in schacht.knoten:
            X = knoten.punkte[0].x
            Y = knoten.punkte[0].y
            total_x += X
            total_y += Y
            count += 1

    if count == 0:
        return None  

    
    middle_x = total_x / count
    middle_y = total_y / count

    return (middle_x, middle_y)


def site_corner(schacht_list: List) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    points = []

    for schacht in schacht_list:
        for knoten in schacht.knoten:
            X = knoten.punkte[0].x
            Y = knoten.punkte[0].y
            points.append((X, Y))

    if len(points) < 2:
        return None  

    max_distance = 0
    point1 = point2 = (0.0, 0.0)

   
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = math.sqrt((points[j][0] - points[i][0]) ** 2 + (points[j][1] - points[i][1]) ** 2)
            if dist > max_distance:
                max_distance = dist
                point1 = points[i]
                point2 = points[j]

    return (point1, point2)    
        


def latest_inp(directory: str, file_pattern: str) -> str:
    # Define a regular expression to match the filenames
    regex = re.compile(rf'{file_pattern}(\d{{8}}\d{{6}})\.inp')

    files = os.listdir(directory)
    dated_files = []

    for filename in files:
        match = regex.match(filename)
        if match:
            date_str = match.group(1)
            date_obj = datetime.strptime(date_str, '%Y%m%d%H%M%S')
            dated_files.append((date_obj, filename))

    if not dated_files:
        raise FileNotFoundError(f"No files matching the pattern {file_pattern} found in {directory}")

    # Sort by datetime object and get the latest one
    dated_files.sort(key=lambda x: x[0], reverse=True)
    latest_file = dated_files[0][1]
    
    return os.path.join(directory, latest_file)

def search_potential_out(schacht_list: List):
    min_sh_heigth = float('inf')
    min_schacht_name = None
    for schacht in schacht_list:
        sh_heigth = schacht.knoten[0].punkte[0].z
        if sh_heigth != 0 and sh_heigth < min_sh_heigth:
            min_sh_heigth = sh_heigth
            min_schacht_name = schacht.objektbezeichnung

            if min_schacht_name is not None:
                print(f'suggestion:{min_schacht_name} at {min_sh_heigth}m (SH)')
                return (min_schacht_name, min_sh_heigth)
            else:
                return None

def num_potential_out(schacht_list:List, haltung_list: List):
    zu_ab_list = []
    ablauf_set = set()
    zulauf_set = set()
    
    for haltung in haltung_list:
        zu_ab_list.append(haltung.ablauf)
        ablauf_set.add(haltung.ablauf)
        zulauf_set.add(haltung.zulauf)
    
    # Count occurrences of each objektbezeichnung in ablauf
    schacht_counter = Counter(zu_ab_list)
    
    # Filter Schacht objects that appear only once in zu_ab_list and do not appear in zulauf_set
    sgl_schacht = [schacht for schacht in schacht_list if schacht_counter[schacht.objektbezeichnung] == 1 and schacht.objektbezeichnung not in zulauf_set]
    
    # Print the results
    num_pot = len(sgl_schacht)
    print(f'Found {num_pot} possible Outfalls')
    for pot in sgl_schacht:
        print(pot.objektbezeichnung)
    
    return sgl_schacht
        
        
    
    