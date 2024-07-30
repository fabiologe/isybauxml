import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Discharge:
    def __init__(self, volume=None, time=None, initial_flow_rate=200, decay_constant=0.1, time_params=(0.1, 120, 100)):
        if volume is None and time is None:
            raise ValueError("Either volume or time must be provided")
        self.volume = volume
        self.time = time
        self.initial_flow_rate = initial_flow_rate
        self.decay_constant = decay_constant
        self.time_start, self.time_end, self.num_points = time_params
        self.times = np.linspace(self.time_start, self.time_end, self.num_points)
        self.flow_rates = None

    def sudden(self):
        def discharge_function(time):
            if time < 1:
                return self.initial_flow_rate
            else:
                return self.initial_flow_rate * np.exp(-self.decay_constant * (time - 1))

        self.flow_rates = np.array([discharge_function(t) for t in self.times])
        self._adjust_flow_rates()

    def euler(self):
        def discharge_function(time):
            if time < 5:
                return self.initial_flow_rate * (time / 5)
            else:
                return self.initial_flow_rate * np.exp(-self.decay_constant * (time - 5))

        self.flow_rates = np.array([discharge_function(t) for t in self.times])
        self._adjust_flow_rates()

    def laminar(self):
        if self.volume is None or self.time is None:
            raise ValueError("Volume and time must be provided for laminar flow")
        
        fixed_flow_rate = self.volume / self.time
        self.flow_rates = np.full_like(self.times, fixed_flow_rate)
        self.times = np.linspace(0, self.time, self.num_points)

    def _adjust_flow_rates(self):
        if self.volume is not None:
            total_volume = np.trapz(self.flow_rates, self.times)
            adjustment_factor = self.volume / total_volume
            self.flow_rates *= adjustment_factor
        elif self.time is not None:
            self.times = np.linspace(self.time_start, self.time, self.num_points)
            total_volume = np.trapz(self.flow_rates, self.times)
            if self.volume is not None:
                adjustment_factor = self.volume / total_volume
                self.flow_rates *= adjustment_factor

    def plot_diagram(self, title='Flow Rate vs Time', color='red'):
        if self.flow_rates is None:
            raise ValueError("Flow rates are not calculated. Call a discharge method first.")
        
        plt.figure(figsize=(12, 6))
        plt.plot(self.times, self.flow_rates, label=title, color=color)
        plt.xlabel('Time (s)')
        plt.ylabel('Flow Rate (m³/s)')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()

    def to_csv(self, filename):
        if self.flow_rates is None:
            raise ValueError("Flow rates are not calculated. Call a discharge method first.")
        
        data = {
            'Time (s)': self.times,
            'Flow Rate (m³/s)': self.flow_rates
        }
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def check_volume_from_csv(self, filename, expected_volume):
        df = pd.read_csv(filename)
        total_volume = np.trapz(df.iloc[:, 1], df.iloc[:, 0])
        print(f"Total volume of water: {total_volume:.2f} m³")

        if np.isclose(total_volume, expected_volume, atol=1e-2):
            print(f"The total volume of water is approximately {expected_volume} m³.")
        else:
            print(f"The total volume of water is not {expected_volume} m³.")
            print(f"Difference: {total_volume - expected_volume:.2f} m³")

# Example usage
discharge = Discharge(volume=3825, time=60, initial_flow_rate=200, decay_constant=0.1, time_params=(0.2, 60, 200))

# Sudden discharge
discharge.sudden()
discharge.plot_diagram(title='Flow Rate vs Time (Sudden Discharge)')
discharge.to_csv('sudden_discharge.csv')

# Euler discharge
discharge.euler()
discharge.plot_diagram(title='Flow Rate vs Time (Euler Discharge)', color='blue')
discharge.to_csv('euler_discharge.csv')

# Laminar flow
''''
discharge.laminar()
discharge.plot_diagram(title='Laminar Flow with Fixed Flow Rate', color='green')
discharge.to_csv('laminar_flow_profile.csv')
'''
# Check volume from CSV
discharge.check_volume_from_csv('sudden_discharge.csv', 3825)
discharge.check_volume_from_csv('euler_discharge.csv', 3825)

#discharge.check_volume_from_csv('laminar_flow_profile.csv', 1000)
