import numpy as np
import pyvista as pv
from surface_runoff.boundary import ModelHandler
from typing import List, Tuple

def generate_contours(terrain_mesh: pv.PolyData, interval: float, polygons: List) -> pv.PolyData:
    # Calculate the scalar values for elevation
    vertex_elevations = {}

    for poly in polygons:
        for vertex in poly.vertices:
            vertex_tuple = (vertex.x_value, vertex.y_value, vertex.z_value)
            vertex_elevations[vertex_tuple] = []

    # Ensure all vertices are considered (handle duplicates)
    all_vertices = set((vertex.x_value, vertex.y_value, vertex.z_value) for poly in polygons for vertex in poly.vertices)
    average_elevations = {vertex: np.mean([p[2] for p in vertex_elevations if p[:2] == vertex[:2]]) for vertex in all_vertices}

    # Generate scalar values for the terrain mesh vertices
    scalar_values = []
    for vertex in terrain_mesh.points:
        vertex_tuple = tuple(vertex)
        if vertex_tuple in average_elevations:
            scalar_values.append(average_elevations[vertex_tuple])
        else:
            # Handle the case when vertex elevation is not found
            print(f"Vertex elevation not found: {vertex_tuple}")
            scalar_values.append(0.0)  # Set a default elevation or handle differently based on your requirements

    # Add scalar data to the terrain mesh
    terrain_mesh["Elevation"] = scalar_values

    # Generate contours using scalar data
    contours = terrain_mesh.contour(scalars="Elevation", isosurfaces=np.arange(terrain_mesh.bounds[4], terrain_mesh.bounds[5], interval))
    
    if contours.n_points == 0:
        print("Warning: Contour generation produced zero points.")
        return None

    return contours





def visualize_contours_and_polygons(terrain_mesh: pv.PolyData, contours: pv.PolyData, polygons: List):
    # Visualize the terrain mesh, contour lines, and polygons
    plotter = pv.Plotter()
    plotter.add_mesh(terrain_mesh, opacity=0.5, show_edges=True)
    plotter.add_mesh(contours, color="black", line_width=1)
    
    # Add polygons as wireframe to visualize them
    for poly in polygons:
        vertices = np.array([[v.x_value, v.y_value, v.z_value] for v in poly.vertices])
        faces = np.hstack([np.array([[len(poly.vertices)] + [i for i in range(len(poly.vertices))]])])
        mesh = pv.PolyData(vertices, faces)
        plotter.add_mesh(mesh, color="gray", style="wireframe")
    
    plotter.show()


# Load polygons
handler = ModelHandler()
stl_file_path = 'surface_runoff/input/2024-06-07-22h50m23s-attachments/DGM_ASCII.stl'
handler.load_stl(stl_file_path)
polygons = handler.get_polygons()

# Create a mesh from polygons
vertices = np.array([[v.x_value, v.y_value, v.z_value] for poly in polygons for v in poly.vertices])
faces = np.hstack([np.array([[len(poly.vertices)] + [i for i in range(len(poly.vertices))]]) for poly in polygons])
terrain_mesh = pv.PolyData(vertices, faces)

# Generate contours
contours = generate_contours(terrain_mesh, interval=10, polygons=polygons)

# Visualize contours and polygons
if contours is not None:
    visualize_contours_and_polygons(terrain_mesh, contours, polygons)

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


