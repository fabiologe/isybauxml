import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
#141091;8,7;10,8;12,0;13,7;16,1;18,6;20,2;22,3;25,3;96,7;120,0;133,3;152,2;178,9;206,7;224,4;247,8;281,1;13;14;15;16;17;18;19;19;20

def rain_wrapper(x, y):
    rain_data = {}
    durations = [15]
    yearly_rain_types = ['3-yr', '5-yr', '10-yr']
    index_rc = generate_index_rc(x, y)
    if index_rc:
        print(index_rc)
        for duration in durations:
            rain_data[duration] = {}
            for yearly_rain_type in yearly_rain_types:
                try:
                    rain_mm = get_rain_mm(duration, yearly_rain_type, index_rc)
                    rain_data[duration][yearly_rain_type] = rain_mm
                    steps = 3  # Assuming 3-minute steps
                    euler_data = generate_euler_type2_rain(rain_mm, duration, steps)
                    rain_data[duration][yearly_rain_type + '_euler'] = euler_data
                except ValueError as e:
                    rain_data[duration][yearly_rain_type] = str(e)
                with open(f"hydraulik/rain_tabels/rain/{index_rc}_{duration}_{yearly_rain_type}.txt", "w") as file:
                    file.write("[TIMESERIES]\n")
                    file.write(";;Name           Date       Time       Value\n")
                    file.write(";;-------------- ---------- ---------- ----------\n")

                    # Write rain data sorted by yearly rain type
                    for time_point, rain_value in euler_data:
                        file.write(f"{yearly_rain_type: <10}     {' ' * 14}  {time_point: >2d}:00       {rain_value: .2f}\n")
                print(rain_data)
    else:
        print("Coordinates not found within any bounding box.")

    return rain_data

 

def generate_index_rc(x, y):
    raster_csv = "hydraulik/rain_tabels/data/raster.csv"
    with open(raster_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            x1 = float(row['X1_NW_WGS84'].replace(',', '.'))
            y1 = float(row['Y1_NW_WGS84'].replace(',', '.'))
            x3 = float(row['X3_SE_WGS84'].replace(',', '.'))
            y3 = float(row['Y3_SE_WGS84'].replace(',', '.'))
            if x1 <= x <= x3 and y1 >= y >= y3:
                return row['index_rc']
    return None

  # Specify the path to your CSV file

def get_rain_mm(duration, yearly_rain_type, index_rc):
    # Convert the index_rc value to match the format in the DataFrame
    index_rc_str = str(index_rc).zfill(6)  
    index_rc_int = int(index_rc_str)
    
    csv_file = f"hydraulik/rain_tabels/data/2020_D{duration}.csv"
    
    if yearly_rain_type == '3-yr':
        columns_to_use = ['HN_003A']
    elif yearly_rain_type == '5-yr':
        columns_to_use = ['HN_005A']
    elif yearly_rain_type == '10-yr':
        columns_to_use = ['HN_010A']
    else:
        raise ValueError("Invalid yearly rain type")
    
    df = pd.read_csv(csv_file, sep=';', index_col='INDEX_RC')
    
    
    
    if index_rc_int not in df.index:
        raise ValueError(f"INDEX_RC {index_rc_int} not found in the DataFrame.")
    
    row = df.loc[index_rc_int]
    
    rain_mm = row[columns_to_use].sum()
    print(rain_mm)
    return rain_mm




csv_folder = "data"


def generate_euler_type2_rain(rain_mm, duration, steps):
    rain_mm = float(rain_mm.replace(',', '.'))
 
    peak_time = duration / 6  # Peak intensity time (adjust as needed)
    peak_intensity = rain_mm / (np.sqrt(2 * np.pi) * peak_time)  # Peak intensity
    
    # Generate time points
    time_points = np.arange(0, duration, steps)
    
    # Calculate Euler Type 2 distribution
    euler_values = peak_intensity * np.exp(-(time_points - peak_time) ** 2 / (2 * peak_time ** 2))
    
    # Normalize the distribution to match the total rainfall amount
    euler_values *= rain_mm / np.sum(euler_values)
    
    # Create a list of tuples with time points and corresponding Euler values
    euler_data = [(time_point, euler_value) for time_point, euler_value in zip(time_points, euler_values)]
    print(euler_data)
    return euler_data


'''x = 6.99641136598768
y = 49.2853524841828
rain_wrapper(x,y)

# Example usage
rain_mm = 15 # Total rainfall amount in mm
duration = 15  # Total duration in minutes
steps = 1 # Time interval in minutes between measurements

rainfall_pattern = generate_euler_type2_rain(rain_mm, duration, steps)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(np.arange(0, duration, steps), rainfall_pattern, marker='o', color='b')
plt.title(f"Rainfall Pattern (Euler Type 2 Distribution) {steps} min/step")
plt.xlabel(f"Time {duration} (minutes)")
plt.ylabel(f"Rainfall {rain_mm}(mm)")
plt.grid(True)
plt.show()
'''