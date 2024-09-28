import numpy as np

class BaseLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        """Abstract method to load data from a file."""
        raise NotImplementedError("Subclasses should implement this method.")



class STLLoader(BaseLoader):
    
    def load(self):
        """Load the STL file and return the vertices as a NumPy array."""
        vertices = []

        with open(self.file_path, 'r') as file:
            lines = file.readlines()

            for line in lines:
                if line.startswith("vertex"):
                    parts = line.split()
                    vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                    vertices.append(vertex)

        return np.array(vertices)

class OBJLoader(BaseLoader):
    def load(self):
        """Load the OBJ file and return vertices as a NumPy array."""
        vertices = []

        with open(self.file_path, 'r') as file:
            lines = file.readlines()

            for line in lines:
                if line.startswith("v "):  # OBJ format starts vertex lines with 'v '
                    parts = line.split()
                    vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                    vertices.append(vertex)

        return np.array(vertices)
