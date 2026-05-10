import pytest
import pandas as pd
import numpy as np
from app.processing.cleaning_service import cleaning_service
from app.processing.feature_engineering import feature_engineering_service

@pytest.fixture
def raw_pandas_df():
    """Generates a small DataFrame with dirty data for testing."""
    data = {
        'farm_id': ['test_farm', 'test_farm', 'test_farm'],
        'recorded_at': [pd.Timestamp('2023-01-01 10:00'), pd.Timestamp('2023-01-01 11:00'), pd.Timestamp('2023-01-01 12:00')],
        'temperature': [30.0, np.nan, 80.0],
        'humidity': [50.0, 110.0, 60.0],
        'rainfall': [0.0, -5.0, 10.0],
        'wind_speed': [5.0, 5.0, 5.0],
        'pressure': [1010.0, 1012.0, 1011.0]
    }
    return pd.DataFrame(data)

def test_data_cleaning(raw_pandas_df):
    """Test that missing values and outliers are handled correctly."""
    cleaned = cleaning_service.clean_data(raw_pandas_df)
    
    # Check NaN handling (forward fill should make second row temp 30.0)
    assert cleaned.iloc[1]['temperature'] == 30.0
    
    # Check Outlier handling
    assert cleaned.iloc[2]['temperature'] == 60.0 # Capped at 60
    assert cleaned.iloc[1]['humidity'] == 100.0   # Capped at 100
    assert cleaned.iloc[1]['rainfall'] == 0.0     # Capped at 0

def test_feature_engineering():
    """Test the generation of complex features."""
    data = {
        'temperature': [20.0, 25.0, 30.0],
        'humidity': [60.0, 50.0, 40.0],
        'rainfall': [0.0, 0.0, 0.0],
        'wind_speed': [2.0, 5.0, 10.0],
        'pressure': [1010.0, 1012.0, 1011.0]
    }
    df = pd.DataFrame(data)
    
    engineered = feature_engineering_service.generate_features(df)
    print("\nENGINEERED DataFrame:")
    print(engineered)
    
    # Evaporation should increase as temp/wind go up and humidity goes down
    assert 'evaporation_index' in engineered.columns
    assert engineered.iloc[2]['evaporation_index'] > engineered.iloc[0]['evaporation_index']
    
    # Humidity trend should be falling
    assert 'humidity_trend' in engineered.columns
    assert engineered.iloc[-1]['humidity_trend'] == 'Falling'
    
    # Drought risk should be high
    assert 'drought_risk_score' in engineered.columns
    assert engineered.iloc[-1]['drought_risk_score'] > 0.5
