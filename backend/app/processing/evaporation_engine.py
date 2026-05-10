import pandas as pd
import numpy as np

def calculate_evaporation_index(df: pd.DataFrame) -> pd.Series:
    """
    Calculates a simplified evaporation index based on temperature, humidity, and wind speed.
    Higher values indicate faster water loss from soil/plants.
    
    Simplified formula based on Penman-Monteith concepts:
    Evap ~ (Temp * Wind_Speed) / (Humidity + 1)
    """
    # Adding 1 to humidity to avoid division by zero
    temp_factor = np.maximum(df['temperature'], 0) # Only consider positive temperatures for evaporation
    wind_factor = df['wind_speed'] + 1.0 # Base wind factor
    humidity_factor = df['humidity'] + 1.0
    
    evap_index = (temp_factor * wind_factor) / humidity_factor
    
    # Scale it to a reasonable index (0 to 10 typically)
    scaled_evap = np.clip(evap_index * 2.5, 0, 10.0)
    return scaled_evap
