import numpy as np
import matplotlib.pyplot as plt

def generate_gumbel_rain(rain_mm, duration, steps):
    # Calculate the peak intensity based on total rain amount
    peak_intensity = rain_mm / (duration / steps)
    
    # Initialize an array to store rainfall intensities
    rainfall_pattern = []
    
    # Generate Gumbel distribution for each time step
    for t in range(duration // steps):
        time = t * steps
        intensity = peak_intensity * np.exp(-np.exp(-(time - duration / 2) / (duration / 6)))
        rainfall_pattern.append(intensity)
    
    return rainfall_pattern

# Example usage
rain_mm = 8
duration = 60
steps = 5

rainfall_pattern = generate_gumbel_rain(rain_mm, duration, steps)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(np.arange(0, duration, steps), rainfall_pattern, marker='o', color='b')
plt.title("Rainfall Pattern (Gumbel Distribution)")
plt.xlabel("Time (minutes)")
plt.ylabel("Rainfall Intensity (mm/h)")
plt.grid(True)
plt.show()
