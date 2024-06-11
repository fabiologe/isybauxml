from surface_runoff.boundary import ModelHandler, RunoffSimulation
import numpy as np
import pyvista as pv
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Contour:
    terrain_mesh: pv.PolyData
    interval: float

    def generate_contours(self) -> pv.PolyData:
        return self.terrain_mesh.contour(scalars="Elevation", isosurfaces=np.arange(self.terrain_mesh.bounds[4], self.terrain_mesh.bounds[5], self.interval))

    def extract_contour_vertices(self) -> List[List[Tuple[float, float, float]]]:
        contours = self.generate_contours()
        contour_vertices = []

        for i in range(contours.n_cells):
            cell = contours.extract_cells(i)
            contour_vertices.append([(cell.points[j][0], cell.points[j][1], cell.points[j][2]) for j in range(cell.n_points)])

        return contour_vertices

    def visualize_contours(self):
        contours = self.generate_contours()

        plotter = pv.Plotter()
        plotter.add_mesh(self.terrain_mesh, opacity=0.5, show_edges=True)
        plotter.add_mesh(contours, color="black", line_width=1)
        plotter.show()

# Load polygons
handler = ModelHandler()
stl_file_path = 'surface_runoff/input/2024-06-07-22h50m23s-attachments/DGM_ASCII.stl'
handler.load_stl(stl_file_path)
polygons = handler.get_polygons()

# Create a mesh from polygons
vertices = np.array([[v.x_value, v.y_value, v.z_value] for poly in polygons for v in poly.vertices])
faces = np.hstack([np.array([[len(poly.vertices)] + [i for i in range(len(poly.vertices))]]) for poly in polygons])
terrain_mesh = pv.PolyData(vertices)


contours = terrain_mesh.contour()

pl = pv.Plotter()
pl.add_mesh(terrain_mesh, opacity=0.85)
pl.add_mesh(contours, color="white", line_width=5)
pl.show()
'''
handler = ModelHandler()

# Load STL file
stl_file_path = 'surface_runoff/input/2024-06-07-22h50m23s-attachments/DGM_ASCII.stl'
handler.load_stl(stl_file_path)


stl_polygons = handler.get_polygons()

vertices = []
faces = []
colors = []

vertex_dict = {}
vertex_count = 0

for polygon in stl_polygons:
    face = []
    for vertex in polygon.vertices:
        # Use a dictionary to avoid duplicate vertices
        if vertex not in vertex_dict:
            vertex_dict[vertex] = vertex_count
            vertices.append([vertex.x_value, vertex.y_value, vertex.z_value])
            vertex_count += 1
        face.append(vertex_dict[vertex])
    faces.append(face)
    colors.append(polygon.color[:3])  # Use RGB, ignore Alpha

# Convert to numpy arrays
vertices = np.array(vertices)
faces = np.hstack([np.array([[len(face)] + face for face in faces])])
colors = np.array(colors)

# Create a PyVista PolyData object with vertices and faces
mesh = pv.PolyData(vertices, faces)
mesh.cell_data['colors'] = colors

# Plot the mesh
plotter = pv.Plotter()
plotter.add_mesh(mesh, scalars='colors', rgb=True, show_edges=True)
plotter.show()'''
def test_alternating_polygon_colors():
    # Initialize the handler and load the STL file
    handler = ModelHandler()
    stl_file_path = 'surface_runoff/input/2024-06-07-22h50m23s-attachments/DGM_ASCII.stl'
    handler.load_stl(stl_file_path)

    # Extract polygons from the STL file
    stl_polygons = handler.get_polygons()

    # Set colors for alternating polygons
    light_green = [0.5, 1, 0.5, 1]
    light_red = [1, 0.5, 0.5, 1]

    # Alternate colors for polygons
    for i, polygon in enumerate(stl_polygons):
        polygon.color = light_red if i % 2 == 0 else light_green

    # Collect all vertices and faces from the polygons
    vertices = []
    faces = []
    colors = []

    vertex_dict = {}
    vertex_count = 0

    for polygon in stl_polygons:
        face = []
        for vertex in polygon.vertices:
            # Use a dictionary to avoid duplicate vertices
            if vertex not in vertex_dict:
                vertex_dict[vertex] = vertex_count
                vertices.append([vertex.x_value, vertex.y_value, vertex.z_value])
                vertex_count += 1
            face.append(vertex_dict[vertex])
        faces.append(face)
        colors.append(polygon.color[:3])  # Use RGB, ignore Alpha

    # Convert to numpy arrays
    vertices = np.array(vertices)
    faces = np.hstack([np.array([[len(face)] + face for face in faces])])
    colors = np.array(colors)

    # Create a PyVista PolyData object with vertices and faces
    mesh = pv.PolyData(vertices, faces)
    mesh.cell_data['colors'] = colors

    # Plot the mesh
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, scalars='colors', rgb=True, show_edges=True)
    plotter.show()


