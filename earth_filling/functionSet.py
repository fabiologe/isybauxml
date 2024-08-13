import logging
import pandas as pd
from input import Handler
from earth_filling.vol_polygon import VolumeCalculator
from area_polygon import AreaCalculator


logging.basicConfig(level=logging.ERROR, filename='errors.log', 
                    format='%(asctime)s %(levelname)s %(message)s')



def getVolumeFrom2Polylines():
    try:
       file_path = Handler.select_file()
       polylines = Handler.read_file(file_path)
       
       if len(polylines) < 2:
           raise ValueError("At least two polylines are required")

       # Extract the first two polylines
       names = list(polylines.keys())
       polyline1, polyline2 = polylines[names[0]], polylines[names[1]]
       
       # Determine the maximum number of points
       num_points = max(len(polyline1), len(polyline2))
       
       # Interpolate points for both polylines
       polyline1_interp = VolumeCalculator.interpolate_polyline(polyline1, num_points)
       polyline2_interp = VolumeCalculator.interpolate_polyline(polyline2, num_points)
       
       # Create surface mesh
       vertices, faces = VolumeCalculator.create_surface_mesh(polyline1_interp, polyline2_interp)
       
       # Calculate the volume of the mesh
       enclosed_volume_cubic_meters = VolumeCalculator.calculate_volume(vertices, faces)
       
       # Print the enclosed volume in cubic meters
       print(f"The enclosed volume between the two polylines is: {enclosed_volume_cubic_meters} cubic meters")
       
       # Save the results to a CSV file
       df = pd.DataFrame({
           "Volume (cubic meters)": [enclosed_volume_cubic_meters]
       })
       df.to_csv('enclosed_volume.csv', index=False)
       
       print("The enclosed volume has been saved to enclosed_volume.csv")
       
       # Visualize the surface mesh
       VolumeCalculator.visualize_surface_mesh(vertices, faces)
    except Exception as e:
        logging.error(e)
        print(f"An error occurred: {e}")


def getAreaFromPolygon():
    try:
        file_path = Handler.select_file()
        area_calculator = AreaCalculator(file_path)
        area_calculator.display_results()
    except Exception as e:
        logging.error(e)
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    getVolumeFrom2Polylines()
    getAreaFromPolygon()
