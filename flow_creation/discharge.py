import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import pandas as pd

# Function to calculate the draining times and flow rates
def torricelli_flow(V0, H, d, C_d=0.582):
    # Konstanten
    g = 9.81  # Erdbeschleunigung in m/s^2

    # Querschnittsfläche der Öffnung
    A = np.pi * (d / 2)**2

    # Querschnittsfläche des Zylinders
    A_zyl = V0 / H

    # Funktion zur Berechnung der Durchflussgeschwindigkeit und Zeit
    def integrand(h):
        # Torricelli mit Berücksichtigung von C_d
        return (A_zyl / (C_d * A * np.sqrt(2 * g * h)))

    # Berechnung der Zeit für spezifische Entleerungsgrade (30%, 50%, 98%)
    def time_for_volume_fraction(fraction):
        target_height = H * (1 - fraction)
        time_partial, _ = quad(integrand, target_height, H)
        return time_partial

    # Berechnung der Entleerungszeiten
    time_full, _ = quad(integrand, 0, H)
    time_30_percent = time_for_volume_fraction(0.30)
    time_50_percent = time_for_volume_fraction(0.50)
    time_98_percent = time_for_volume_fraction(0.98)

    # Berechnung von Durchfluss, Volumen und Zeit abhängige Höhe
    heights = np.linspace(0, H, 100)
    times = []
    volumes = []
    flow_rates = []

    for h in heights:
        # Zeitberechnung
        time, _ = quad(integrand, h, H)
        times.append(time)
        
        # Volumenberechnung
        volume = A_zyl * h
        volumes.append(volume)
        
        # Durchflussrate (mit Scharfkantigkeit)
        flow_rate = C_d * A * np.sqrt(2 * g * h)
        flow_rates.append(flow_rate)

    # Zeiten invertieren, damit sie bei 0 starten
    times_inverted = [t - times[-1] for t in times]

    # Return calculated values
    return times_inverted, flow_rates, volumes, heights

# Function to save the CSV data
def save_to_csv(times, flow_rates, volumes, heights, csv_filename="entleerungsdaten.csv"):
    data = {
        "Entleerungszeit (Sek)": times,
        "Durchflussrate (m³/s)": flow_rates,
        "Volumen (m³)": volumes,
        "Höhe (m)": heights
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_filename, index=False)
    print(f"CSV-Datei '{csv_filename}' wurde erfolgreich erstellt.")

# Separate plotting function with red markers and text for Q and t
def plot_with_red_markers_and_text(times, heights, flow_rates):
    # Plot the draining curve
    plt.figure(figsize=(10, 6))
    plt.plot(times, heights, label="Entleerungskurve", color="blue")

    # Define the heights at which we want to mark and annotate (every 0.5m)
    annotation_heights = np.arange(0.5, max(heights), 0.5)

    # Loop over the annotation heights and mark only one value for each
    for h_annot in annotation_heights:
        # Find the index of the point closest to the desired annotation height
        idx = np.abs(heights - h_annot).argmin()

        # Get the corresponding time (in hours) and flow rate (rounded to 3 decimal places)
        time_in_hours = round(times[idx] / 3600, 3)
        flow_rate = round(flow_rates[idx], 3)

        # Plot a red dot at the closest point
        plt.plot(times[idx], heights[idx], 'ro')  # Red circle marker

        # Annotate the graph with time and flow rate at each 0.5m interval
        plt.annotate(f"t={time_in_hours:.3f} h\nQ={flow_rate:.3f} m³/s", 
                     (times[idx], heights[idx]), 
                     textcoords="offset points", 
                     xytext=(-30,5), ha='center', fontsize=8)

    # Adjust graph aesthetics
    plt.gca().invert_yaxis()  # Invert y-axis to match height drop
    plt.title("Entleerungskurve des zylinderförmigen Behälters")
    plt.xlabel("Zeit (Sekunden)")
    plt.ylabel("Flüssigkeitshöhe (m)")
    plt.grid(True)
    plt.legend()
    plt.show()

# Example usage
# Set volume, height, and opening diameter
V0 = 750  # Volume of the tank
H = 4.5    # Height of the tank
d = 0.1   # Diameter of the opening
C_d = 0.582  # Discharge coefficient for sharp-edged openings

# Run the flow calculations
times, flow_rates, volumes, heights = torricelli_flow(V0, H, d, C_d=C_d)

# Optionally save results to CSV
csv_filename = "entleerungsdaten_1000m3_scharfkantig_582.csv"
save_to_csv(times, flow_rates, volumes, heights, csv_filename=csv_filename)

# Plot with red markers and text annotations for Q and t values
plot_with_red_markers_and_text(times, heights, flow_rates)
