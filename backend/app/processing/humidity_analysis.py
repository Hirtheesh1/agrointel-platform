import pandas as pd
import numpy as np

def calculate_humidity_trend(df: pd.DataFrame, window: int = 3) -> pd.Series:
    """
    Calculates the humidity trend over a given window.
    Returns categorized strings: 'Rising', 'Falling', 'Stable'
    """
    if len(df) < window:
        # Not enough data for trend, assume stable
        return pd.Series(['Stable'] * len(df), index=df.index)
        
    # Calculate the difference over the window
    diff = df['humidity'].diff(periods=window-1)
    
    # Categorize the trend based on threshold (e.g., 5% change)
    conditions = [
        (diff > 5.0),
        (diff < -5.0)
    ]
    choices = ['Rising', 'Falling']
    
    # np.select applies the conditions, default is 'Stable'
    trend = pd.Series(np.select(conditions, choices, default='Stable'), index=df.index)
    
    # For the first few rows where diff is NaN, fill with 'Stable'
    trend = trend.fillna('Stable')
    
    return trend
