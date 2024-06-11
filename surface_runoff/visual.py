
from surface_runoff.boundary import Polygon, Vertex, ModelHandler
import numpy as np
import pyvista as pv
from typing import List, Tuple
from dataclasses import dataclass
    
@dataclass
class Viewer:
    def default_poly(polygons:List['Polygon']):
        '''This method generates a PyVista mesh representation of a collection of polygons.
            converts the input polygons into a PyVista PolyData object, 
            which can then be visualized using
            PyVista's plotting functionalities. 
        '''
        vertices = []
        faces = []
        colors = []

        vertex_dict = {}
        vertex_count = 0

        for polygon in polygons:
            face = []
            for vertex in polygon.vertices:
               
                if vertex not in vertex_dict:
                    vertex_dict[vertex] = vertex_count
                    vertices.append([vertex.x_value, vertex.y_value, vertex.z_value])
                    vertex_count += 1
                face.append(vertex_dict[vertex])
            faces.append(face)
            colors.append(polygon.color[:3])  

  
        vertices = np.array(vertices)
        faces = np.hstack([np.array([[len(face)] + face for face in faces])])
        colors = np.array(colors)

    
        mesh = pv.PolyData(vertices, faces)
        mesh.cell_data['colors'] = colors

        plotter = pv.Plotter()
        plotter.add_mesh(mesh, scalars='colors', rgb=True, show_edges=True)
        plotter.show()
        return
    def default_pc(vertices: List['Vertex']):
        
        return
        