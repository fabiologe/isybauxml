import math

class VolumeCalculator:
    def __init__(self, area, height, slope):
        self.area = area  # Base area
        self.height = height  # Given height
        self.slope = slope  # Escarpment (slope ratio, e.g., 1.5 for a 1.5:1 slope)

    def calculate_rect(self):
        # Effective height adjustment (simplified approach, assuming slope extends the base area)
        # The height doesn't change, but the slope might affect how the volume is distributed.
        volume = self.area * self.height
        return volume
    
    def calculate_trap(self):
        # Calculate the area reduction due to slope (if needed)
        top_area = self.area / (1 + 2 * self.slope * self.height)
        
        # Trapezoidal volume calculation
        volume = (self.height / 3) * (self.area + math.sqrt(self.area * top_area) + top_area)
        return volume