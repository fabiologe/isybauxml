from shapely.geometry import Polygon as ShapelyPolygon, LineString
from hydraulik.flaechen import flaechen_list
from xml_parser import *

def convert_to_shapely(polygons):
    # Initialize empty list
    coordinates = []

    # Loop through each Kante
    for kante in polygons:  
        x_start = kante.start.punkt.x
        y_start = kante.start.punkt.y
        z_start = kante.start.punkt.z  # not needed for 2D geometry ops, but added for completeness
        # Add the start coordinates to our list
        coordinates.append((x_start, y_start, z_start))

    # Add the last point (the end of the last Kante) manually
    x_end = polygons[-1].kante.ende.punkt.x
    y_end = polygons[-1].kante.ende.punkt.y
    z_end = polygons[-1].kante.ende.punkt.z

    # Add the end coordinates to list
    coordinates.append((x_end, y_end, z_end))

    # Create a LineString
    shapely_line = LineString(coordinates)

    return shapely_line



def get_vertices(flaeche_list, haltung_list, leitung_list,convert_to_shapely):
    for flaeche in flaeche_list:
        vertices_inside = []
        
        ''' Trans. from class object to tuple to work with the shapely lib 
        neeeds to be done '''
        # convert the Flache polygon to a Shapely polygon
        flaeche_polygon = convert_to_shapely(flaeche.polygon)

        for haltung in haltung_list:
            haltung_polygon = convert_to_shapely(haltung.polygon)
            if flaeche_polygon.contains(haltung_polygon):
                vertices_inside.append(haltung)

        for leitung in leitung_list:
            leitung_polygon = convert_to_shapely(leitung.polygon)
            if flaeche_polygon.contains(leitung_polygon):
                vertices_inside.append(leitung)

        flaeche.vertices = vertices_inside