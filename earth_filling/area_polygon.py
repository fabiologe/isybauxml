import pandas as pd
import numpy as np

class AreaCalculator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.grouped = self.data.groupby('Name')
        self.polylines = {name: group[['X', 'Y', 'Z']].values for name, group in self.grouped}

    @staticmethod
    def shoelace_formula(points):
        n = len(points)
        if n < 3:
            return 0
        area = 0
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            area += x1 * y2 - y1 * x2
        return abs(area) / 2.0

    @staticmethod
    def point_to_segment_distance(px, py, pz, x1, y1, z1, x2, y2, z2):
        line_vec = np.array([x2 - x1, y2 - y1])
        point_vec = np.array([px - x1, py - y1])
        line_len = np.linalg.norm(line_vec)
        line_unitvec = line_vec / line_len
        proj_length = np.dot(point_vec, line_unitvec)
        proj_length = max(0, min(line_len, proj_length))
        proj_point = np.array([x1, y1]) + proj_length * line_unitvec

        orthogonal_distance = np.linalg.norm(np.array([px, py]) - proj_point)
        t = proj_length / line_len
        interpolated_z = (1 - t) * z1 + t * z2

        return orthogonal_distance, interpolated_z

    def calculate_area(self):
        areas = {}
        for name, group in self.grouped:
            points = list(zip(group['X'], group['Y']))
            area = self.shoelace_formula(points)
            areas[name] = area
        return areas

    def calculate_height_differences(self):
        if len(self.polylines) < 2:
            raise ValueError("At least two polylines are required")

        polyline1 = self.polylines['Point 1']
        polyline2 = self.polylines['Point 2']
        height_differences = []

        for px, py, pz in polyline1:
            min_distance = float('inf')
            intersection_z = None
            for i in range(len(polyline2) - 1):
                x1, y1, z1 = polyline2[i]
                x2, y2, z2 = polyline2[i + 1]
                dist, interp_z = self.point_to_segment_distance(px, py, pz, x1, y1, z1, x2, y2, z2)
                if dist < min_distance:
                    min_distance = dist
                    intersection_z = interp_z

            if intersection_z is not None:
                height_difference = pz - intersection_z
                height_differences.append(height_difference)

        height_differences = np.array(height_differences)
        average_height_difference = height_differences.mean()

        height_diff_df = pd.DataFrame({
            'Point': range(1, len(height_differences) + 1),
            'Height Difference': height_differences
        })

        return height_diff_df, average_height_difference

    def display_results(self):
        areas = self.calculate_area()
        height_diff_df, average_height_difference = self.calculate_height_differences()

        print("Height differences for each point:")
        print(height_diff_df)
        print(f"Average height difference: {average_height_difference:.2f}")

        for polyline, area in areas.items():
            print(f"Area of {polyline}: {area} square units")

        return areas, height_diff_df, average_height_difference
