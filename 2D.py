from surface_runoff.visual import Viewer
from surface_runoff.boundary import ModelHandler


handler = ModelHandler()
stl_file_path = 'surface_runoff/input/2024-06-07-22h50m23s-attachments/DGM_ASCII.stl'
handler.load_stl(stl_file_path)
polygons = handler.get_polygons()

Viewer.default_poly(polygons)

pc_file_path = 'surface_runoff/input/'
handler.load_xyz(pc_file_path)
pointcloud = handler.get_pointcloud()
