import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class VolumeCalculator:
    @staticmethod
    def interpolate_polyline(polyline, num_points):
        distances = np.linspace(0, 1, len(polyline))
        interp_func = interp1d(distances, polyline, axis=0, kind='linear')
        new_distances = np.linspace(0, 1, num_points)
        return interp_func(new_distances)

    @staticmethod
    def create_surface_mesh(polyline1, polyline2):
        vertices = np.vstack((polyline1, polyline2))
        faces = []
        num_points = len(polyline1)
        
        for i in range(num_points - 1):
            # Create two triangles for each quad between the points of the polylines
            faces.append([i, i + 1, i + num_points])
            faces.append([i + 1, i + num_points + 1, i + num_points])
        
        # Close the loop
        faces.append([num_points - 1, 0, 2 * num_points - 1])
        faces.append([0, num_points, 2 * num_points - 1])
        
        return vertices, np.array(faces)

    @staticmethod
    def calculate_volume(vertices, faces):
        volume = 0.0
        for face in faces:
            tetra = np.vstack([vertices[face], [0, 0, 0]])  # Ensure we have four points for the tetrahedron
            mat = np.ones((4, 4))
            mat[:, :3] = tetra
            volume += np.abs(np.linalg.det(mat)) / 6.0
        return volume

    @staticmethod
    def visualize_surface_mesh(vertices, faces):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot the vertices
        ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], label='Vertices', marker='o')
        
        # Plot the faces
        for face in faces:
            tri = Poly3DCollection([vertices[face]], facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25)
            ax.add_collection3d(tri)
        
        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title("Surface Mesh Between Polylines")
        plt.legend()
        plt.show()

