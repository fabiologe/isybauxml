from surface_runoff.boundary import ModelHandler

from surface_runoff.opengl_viewer import create_buffers
import numpy as np
import pyvista as pv



handler = ModelHandler()

# Load STL file
stl_file_path = 'surface_runoff/input/2024-06-07-22h50m23s-attachments/Auslauf_ASCII.stl'
handler.load_stl(stl_file_path)


stl_polygons = handler.get_polygons()
print("STL Polygons:")
for polygon in stl_polygons:
    print(polygon)

