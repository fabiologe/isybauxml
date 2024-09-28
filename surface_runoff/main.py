import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
def load_centroids_and_vectors(file_path):
    centroids = []
    vectors = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            if line.startswith("Centroid"):
                # Extract centroid values
                centroid_str = line.split(":")[1].strip().strip('[]')
                centroid = np.array([float(x) for x in centroid_str.split()])
                centroids.append(centroid[:2])  # We only need X and Y for 2D

            elif line.startswith("Normal"):
                # Extract normal/flow vector values
                vector_str = line.split(":")[1].strip().strip('[]')
                vector = np.array([float(x) for x in vector_str.split()])
                
                # If the vector contains NaN, replace it with a zero vector
                if np.isnan(vector).any():
                    vector = np.array([0.0, 0.0, 0.0])
                
                vectors.append(vector[:2])  # We only need X and Y for 2D
    
    centroids = np.array(centroids)
    vectors = np.array(vectors)
    
    return centroids, vectors
# Load the TIFF image
def load_tiff_image(tiff_file):
    image = Image.open(tiff_file)
    return image

# Convert world coordinates (centroids) to image pixel coordinates
def world_to_pixel(centroid, world_bounds, image_size):
    # world_bounds = (min_x, max_x, min_y, max_y)
    min_x, max_x, min_y, max_y = world_bounds
    image_width, image_height = image_size

    # Normalize the world coordinates to [0, 1]
    x_norm = (centroid[0] - min_x) / (max_x - min_x)
    y_norm = (centroid[1] - min_y) / (max_y - min_y)

    # Convert normalized coordinates to pixel coordinates
    pixel_x = int(x_norm * image_width)
    pixel_y = int((1 - y_norm) * image_height)  # y is flipped because image origin is top-left

    return pixel_x, pixel_y

# Draw arrows on the image
def draw_arrows_on_image(image, centroids, vectors, world_bounds, arrow_scale=10):
    draw = ImageDraw.Draw(image)
    image_size = image.size

    # Loop through each centroid and vector
    for i in range(len(centroids)):
        # Convert world coordinates to pixel coordinates
        pixel_start = world_to_pixel(centroids[i], world_bounds, image_size)

        # Calculate the end point of the arrow
        vector = vectors[i] * arrow_scale
        pixel_end = (pixel_start[0] + vector[0], pixel_start[1] - vector[1])

        # Draw the arrow (line for now)
        draw.line([pixel_start, pixel_end], fill='red', width=2)
        draw.line([pixel_end, (pixel_end[0] - 2, pixel_end[1] - 2)], fill='red', width=2)  # Optional: a simple head
    return image
# Load the STL file
def load_stl(file_path):
    mesh = trimesh.load(file_path)
    return mesh

# Calculate the centroid of a triangle
def calculate_centroid(vertices):
    # The centroid is the average of the three vertices of the triangle
    centroid = np.mean(vertices, axis=0)
    return centroid

# Calculate the normal vector (runoff direction)
def calculate_normal(vertices):
    # Get the vectors of two edges of the triangle
    edge1 = vertices[1] - vertices[0]
    edge2 = vertices[2] - vertices[0]
    # Calculate the cross product of the two edges
    normal = np.cross(edge1, edge2)
    # Normalize the vector to get the unit normal vector
    normal = normal / np.linalg.norm(normal)
    return normal

# Main function to process the STL and calculate vectors
def process_stl(file_path):
    mesh = load_stl(file_path)

    # Arrays to store centroids and normals
    centroids = []
    normals = []

    # Loop through each triangular face
    for face in mesh.faces:
        # Get the three vertices of the triangle
        vertices = mesh.vertices[face]
        
        # Calculate the centroid
        centroid = calculate_centroid(vertices)
        centroids.append(centroid)

        # Calculate the normal (flow vector)
        normal = calculate_normal(vertices)
        normals.append(normal)

    return np.array(centroids), np.array(normals)

# Visualization function
def visualize_vectors(centroids, normals, scale=0.1):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot centroids as points
    ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], color='blue', label='Centroids')

    # Plot vectors (normals) as arrows
    for i in range(len(centroids)):
        # Centroid position
        centroid = centroids[i]
        # Normal vector scaled by a factor
        normal = normals[i] * scale

        # Plot the vector (as an arrow from the centroid)
        ax.quiver(centroid[0], centroid[1], centroid[2], normal[0], normal[1], normal[2], color='red')

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Flow Vectors on Triangular Mesh')
    plt.legend()
    plt.show()

# Save the centroids and normals (vectors) to a file
def save_vectors_to_file(centroids, normals, output_file='centroids_normals.txt'):
    with open(output_file, 'w') as f:
        for i in range(len(centroids)):
            centroid = centroids[i]
            normal = normals[i]
            f.write(f'Centroid: {centroid}, Normal (Flow Vector): {normal}\n')
    print(f'Centroids and normals saved to {output_file}')

# Main execution
if __name__ == "__main__":
    # Specify the STL file path
    file_path = "surface_runoff/input/2024-06-07-22h50m23s-attachments/DGM_ASCII.stl"

    # Process the STL to get centroids and normals
    centroids, normals = process_stl(file_path)

    # Visualize the vectors
    visualize_vectors(centroids, normals)

    # Optionally, save the vectors to a file
    save_vectors_to_file(centroids, normals)
