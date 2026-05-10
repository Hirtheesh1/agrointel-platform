import pandas as pd
import numpy as np

def calculate_drought_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates drought risk score, drought level, and generates an explanation.
    Risk score is between 0.0 (no risk) and 1.0 (extreme risk).
    """
    
    # 1. Heat Stress: Higher temps increase drought risk
    heat_stress = np.clip((df['temperature'] - 25.0) / 15.0, 0.0, 1.0)
    
    # 2. Moisture Deficit: Low humidity and low rainfall increase risk
    # Assuming avg required rainfall is 5mm per hour for this simplified model
    rain_deficit = np.clip(1.0 - (df['rainfall'] / 5.0), 0.0, 1.0)
    humidity_deficit = np.clip(1.0 - (df['humidity'] / 60.0), 0.0, 1.0)
    
    moisture_deficit = (rain_deficit * 0.7) + (humidity_deficit * 0.3)
    
    # 3. Incorporate Evaporation Index (assuming max 10.0 from evaporation engine)
    evap_impact = np.clip(df['evaporation_index'] / 10.0, 0.0, 1.0)
    
    # 4. Final Risk Score Weighted Calculation
    risk_score = (heat_stress * 0.3) + (moisture_deficit * 0.5) + (evap_impact * 0.2)
    df['drought_risk_score'] = np.clip(risk_score, 0.0, 1.0)
    
    # 5. Categorize Drought Level
    conditions = [
        (df['drought_risk_score'] >= 0.8),
        (df['drought_risk_score'] >= 0.6),
        (df['drought_risk_score'] >= 0.4)
    ]
    choices = ['Severe', 'Moderate', 'Mild']
    df['drought_level'] = np.select(conditions, choices, default='None')
    
    # 6. Generate human-readable explanation
    def generate_explanation(row):
        if row['drought_level'] == 'None':
            return "Optimal moisture conditions."
        reasons = []
        if row['rainfall'] == 0:
            reasons.append("lack of rainfall")
        if row['temperature'] > 30:
            reasons.append("high temperatures")
        if row['evaporation_index'] > 6:
            reasons.append("rapid evaporation")
            
        reason_str = ", ".join(reasons) if reasons else "environmental deficits"
        return f"{row['drought_level']} drought risk driven by {reason_str}."
        
    df['drought_explanation'] = df.apply(generate_explanation, axis=1)
    df['heat_stress_score'] = heat_stress
    df['moisture_deficit_index'] = moisture_deficit
    
    return df
