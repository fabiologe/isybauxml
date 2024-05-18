from xml_parser import *
from typing import List, Tuple
import math

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
        
