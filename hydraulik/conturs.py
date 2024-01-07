import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

points = [
    (10.501, 51.917, 293), 
    (10.502, 51.918, 286), 
    (10.503, 51.919, 285), 
    (10.504, 51.920, 280), 
    # Additional points
    (10.598, 52.014, 305), 
    (10.599, 52.015, 304),
    (10.600, 52.016, 303),
    (10.601, 52.017, 300)
]

# Separate x, y, and z to different lists
x = [point[0] for point in points]
y = [point[1] for point in points]
z = [point[2] for point in points]

# Normalize x, y coordinates
x = (x - np.min(x)) / (np.max(x) - np.min(x))
y = (y - np.min(y)) / (np.max(y) - np.min(y))

# Create grid coordinates for plotting
grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]

# Interpolate Z for every point in the grid
grid_z = griddata((x, y), z, (grid_x, grid_y), method='linear')

# Ensure there are no NaNs in grid_z
if not np.isnan(grid_z).all():
    # Generate contour levels for this elevation points with steps of 0.1
    contour_levels = np.arange(np.nanmin(grid_z), np.nanmax(grid_z), 0.1)
    print("grid_z:", grid_z)
    print('np.nanmin(grid_z), np.nanmax(grid_z)', np.nanmin(grid_z), np.nanmax(grid_z))
    print("contour_levels:", contour_levels)
    # Create contour plot
    plt.figure(figsize=(8, 6))
    plt.contour(grid_x, grid_y, grid_z, levels=contour_levels)
    plt.colorbar(label='Elevation')
    plt.title('Contour Plot')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.tight_layout()
    plt.show()
else:
    print("grid_z contains only NaN values!")