from surface_runoff.visual import Viewer
from surface_runoff.boundary import ModelHandler


handler = ModelHandler()
'''
stl_file_path = 'surface_runoff/input/2024-06-07-22h50m23s-attachments/DGM_ASCII.stl'
handler.load_stl(stl_file_path)
polygons = handler.get_polygons()

Viewer.default_poly(polygons)'''

# Load point cloud from XYZ file
pc_file_path = 'surface_runoff/input/output.xyz'
handler.load_xyz(pc_file_path)



# Get polygons and point cloud

pointcloud = handler.get_pointcloud()

# Visualize combined
Viewer.default_pc(pointcloud)
