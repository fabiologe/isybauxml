from shapely.geometry import Polygon as ShapelyPolygon
from hydraulik.flaechen import flaechen_list
from xml_parser import *

def get_vertices(flaeche_list, haltung_list, leitung_list):
    for flaeche in flaeche_list:
        vertices_inside = []
        
        ''' Trans. from class object to tuple to work with the shapely lib 
        neeeds to be done '''
        # convert the Flache polygon to a Shapely polygon
        flaeche_polygon = flaeche.convert_to_shapely(flaeche.polygon)

        for haltung in haltung_list:
            haltung_polygon = flaeche.convert_to_shapely(haltung.polygon)
            if flaeche_polygon.contains(haltung_polygon):
                vertices_inside.append(haltung)

        for leitung in leitung_list:
            leitung_polygon = flaeche.convert_to_shapely(leitung.polygon)
            if flaeche_polygon.contains(leitung_polygon):
                vertices_inside.append(leitung)

        flaeche.vertices = vertices_inside