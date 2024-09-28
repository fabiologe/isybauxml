
import numpy as np
import matplotlib.pyplot as plt

class Terrain:
    def __init__(self, elevation_matrix):
        self.elevation = elevation_matrix
        self.rows, self.cols = elevation_matrix.shape
        self.flow_direction = np.zeros((self.rows, self.cols), dtype=int)

    def calculate_flow_directions(self):
        """Calculate flow directions using D8 algorithm."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.flow_direction[r, c] = self.get_flow_direction(r, c)

    def get_flow_direction(self, row, col):
        """Determine the flow direction for a given cell."""
        min_elevation = self.elevation[row, col]
        direction = -1  # No flow
        
        for dr, dc in [(-1, 0), (-1, 1), (0, 1), (1, 1), 
                       (1, 0), (1, -1), (0, -1), (-1, -1)]:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                if self.elevation[r, c] < min_elevation:
                    min_elevation = self.elevation[r, c]
                    direction = self.get_direction_index(dr, dc)
        
        return direction

    def get_direction_index(self, dr, dc):
        """Get the direction index based on row and column changes."""
        if dr == -1 and dc == 0: return 0
        if dr == -1 and dc == 1: return 1
        if dr == 0 and dc == 1: return 2
        if dr == 1 and dc == 1: return 3
        if dr == 1 and dc == 0: return 4
        if dr == 1 and dc == -1: return 5
        if dr == 0 and dc == -1: return 6
        if dr == -1 and dc == -1: return 7

    def plot_terrain(self):
        """Plot the terrain and flow directions."""
        plt.imshow(self.elevation, cmap='terrain')
        plt.colorbar(label='Elevation')
        plt.quiver(np.arange(self.cols), np.arange(self.rows), 
                   np.cos(np.pi/4 * self.flow_direction), 
                   np.sin(np.pi/4 * self.flow_direction), 
                   color='blue', headlength=4)
        plt.title('Terrain and Flow Directions')
        plt.xlabel('Column Index')
        plt.ylabel('Row Index')
        plt.show()