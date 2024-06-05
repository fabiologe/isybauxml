from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict
import numpy as np
from collections import defaultdict



@dataclass
class vertex:
    x_value: Optional[float]
    y_value: Optional[float]
    z_value: Optional[float]
    def __hash__(self):
        return hash((self.x_value, self.y_value, self.z_value))

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            return False
        return (self.x_value, self.y_value, self.z_value) == (other.x_value, other.y_value, other.z_value)


'''For getting an more precise mesh we split the triangle in smaller ones
@dataclass
class calc_triangle:
    vertices: List[vertex]
    typ: Optional[str] = 'Grass'
    perme: Optional[float]= 0
    focus: vertex
    part: triangle
    kst: Optional[float]= 100.0 #concrete smooth
    rain_volume: Optional[float]= 0.0'''

@dataclass
class triangle:
    vertices: List[vertex]
    typ: Optional[str] = 'Grass'
    perme: Optional[float]= 0
    focus: Optional[vertex]= 0
    kst: Optional[float]= 100.0 #concrete smooth
    slop: Optional[float]= 0 # Gefälle I in Promilley 
    rain_volume: Optional[float]= 0.0
    def contains_point(self, point: Tuple[float, float]) -> bool:
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        b1 = sign(point, (self.vertices[0].x_value, self.vertices[0].y_value), (self.vertices[1].x_value, self.vertices[1].y_value)) < 0.0
        b2 = sign(point, (self.vertices[1].x_value, self.vertices[1].y_value), (self.vertices[2].x_value, self.vertices[2].y_value)) < 0.0
        b3 = sign(point, (self.vertices[2].x_value, self.vertices[2].y_value), (self.vertices[0].x_value, self.vertices[0].y_value)) < 0.0

        return ((b1 == b2) and (b2 == b3))

    def get_centroid(self) -> Tuple[float, float, float]:
        cx = (self.vertices[0].x_value + self.vertices[1].x_value + self.vertices[2].x_value) / 3
        cy = (self.vertices[0].y_value + self.vertices[1].y_value + self.vertices[2].y_value) / 3
        cz = (self.vertices[0].z_value + self.vertices[1].z_value + self.vertices[2].z_value) / 3
        return (cx, cy, cz)

    def get_lowest_vertex(self) -> vertex:
        return min(self.vertices, key=lambda v: v.z_value)

    def __hash__(self):
        return hash(tuple(sorted((v.x_value, v.y_value) for v in self.vertices)))

    def __eq__(self, other):
        if not isinstance(other, triangle):
            return False
        return sorted((v.x_value, v.y_value) for v in self.vertices) == sorted((v.x_value, v.y_value) for v in other.vertices)

class RunoffSimulation:
    def __init__(self, triangles: List[triangle], start_point: Tuple[float, float]):
        self.triangles = triangles
        self.current_position = np.array(start_point)
        self.triangle_neighbors = self.compute_neighbors()
        self.path = []

    def compute_neighbors(self) -> Dict[int, List[int]]:
        edges = defaultdict(list)
        neighbors = defaultdict(list)
        
        for i, tri in enumerate(self.triangles):
            for j in range(3):
                edge = (tri.vertices[j], tri.vertices[(j + 1) % 3])
                edge = tuple(sorted(edge, key=lambda v: (v.x_value, v.y_value)))
                edges[edge].append(i)
        
        for edge, tris in edges.items():
            if len(tris) == 2:
                neighbors[tris[0]].append(tris[1])
                neighbors[tris[1]].append(tris[0])
        
        return neighbors

    def find_triangle(self, position: Tuple[float, float]) -> int:
        for i, triangle in enumerate(self.triangles):
            if triangle.contains_point(position):
                return i
        return -1

    def calculate_path_to_lowest_point(self):
        current_triangle_index = self.find_triangle(tuple(self.current_position))
        if current_triangle_index == -1:
            print("Starting point is outside the mesh.")
            return []

        while True:
            current_triangle = self.triangles[current_triangle_index]
            self.path.append(current_triangle)
            lowest_vertex = current_triangle.get_lowest_vertex()
            if all(v.z_value >= lowest_vertex.z_value for v in current_triangle.vertices):
                print("Reached the lowest point.")
                break
            
            lowest_neighbor_index = -1
            lowest_elevation = lowest_vertex.z_value

            for neighbor_index in self.triangle_neighbors[current_triangle_index]:
                neighbor_triangle = self.triangles[neighbor_index]
                neighbor_lowest_vertex = neighbor_triangle.get_lowest_vertex()
                if neighbor_lowest_vertex.z_value < lowest_elevation:
                    lowest_elevation = neighbor_lowest_vertex.z_value
                    lowest_neighbor_index = neighbor_index

            if lowest_neighbor_index == -1:
                print("No lower neighbors, water stops here.")
                break
            
            current_triangle_index = lowest_neighbor_index

        return self.path

# Example usage
vertices = [
    vertex(0, 0, 10),
    vertex(1, 0, 15),
    vertex(0, 1, 20),
    vertex(1, 1, 5),
]

triangles = [
    triangle(vertices=[vertices[0], vertices[1], vertices[2]], perme=0.1, slop=5.0),
    triangle(vertices=[vertices[1], vertices[3], vertices[2]], perme=0.05, slop=10.0),
]

start_point = (0.5, 0.5)  # Example start point

simulation = RunoffSimulation(triangles, start_point)
path = simulation.calculate_path_to_lowest_point()

for i, tri in enumerate(path):
    centroid = tri.get_centroid()
    print(f"Step {i+1}: triangle with centroid at {centroid}")




