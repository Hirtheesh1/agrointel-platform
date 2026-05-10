export interface Farm {
  id: string;
  farm_name: string;
  location_name: string;
  latitude: number;
  longitude: number;
  farm_size: number;
  soil_type: string;
}

export interface WeatherData {
  id: string;
  farm_id: string;
  temperature: number;
  humidity: number;
  rainfall: number;
  wind_speed: number;
  pressure: number;
  weather_condition: string;
  recorded_at: string;
}

export interface AIPrediction {
  id: string;
  farm_id: string;
  prediction_type: 'irrigation' | 'drought' | 'environmental_risk';
  prediction_value: number;
  confidence_score: number;
  model_version: string;
  explanation: string;
  created_at: string;
}

export interface PredictionResponse {
  irrigation?: AIPrediction;
  drought?: AIPrediction;
}
