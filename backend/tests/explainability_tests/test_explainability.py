import pytest
from app.ai_engine.explainability_engine import ExplainabilityEngine
from unittest.mock import MagicMock
import numpy as np
import torch

def test_generate_explanation():
    """Test the translation of TFT attention weights into natural language."""
    # Mock model and its outputs
    mock_model = MagicMock()
    mock_raw_predictions = MagicMock()
    mock_raw_predictions.output = "mock_output"
    
    mock_model.predict.return_value = mock_raw_predictions
    
    # Mock interpretation output
    mock_interpretation = {
        "encoder_variables": torch.tensor([0.45, 0.20, 0.15, 0.05, 0.10, 0.05])
    }
    mock_model.interpret_output.return_value = mock_interpretation
    mock_model.encoder_variables = [
        "temperature", "humidity", "wind_speed", "rainfall", "evaporation_index", "drought_risk_score"
    ]
    
    engine = ExplainabilityEngine(model=mock_model)
    
    explanation = engine.generate_explanation(dataloader="mock_dataloader")
    
    assert "temperature" in explanation["natural_language_explanation"].lower()
    assert explanation["top_features"]["temperature"] == pytest.approx(0.45, rel=1e-3)
    
def test_feature_importance_ranking():
    """Test that feature importance is ranked correctly."""
    mock_model = MagicMock()
    mock_raw_predictions = MagicMock()
    mock_model.predict.return_value = mock_raw_predictions
    
    mock_interpretation = {
        "encoder_variables": torch.tensor([0.1, 0.8, 0.1])
    }
    mock_model.interpret_output.return_value = mock_interpretation
    mock_model.encoder_variables = [
        "temperature", "drought_risk_score", "humidity"
    ]
    
    engine = ExplainabilityEngine(model=mock_model)
    
    explanation = engine.generate_explanation(dataloader="mock_dataloader")
    
    # Drought risk score should be identified as the top driver
    assert "drought_risk_score" in explanation["natural_language_explanation"].lower()
