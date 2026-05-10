from typing import Dict, Any, List
from datetime import datetime


class SeasonalForecastingEngine:
    """
    Generates multi-horizon seasonal forecasts (7d, 30d, 3m, 10m)
    with climate suitability scores and irrigation sustainability analysis.
    """

    MONSOON_FORECAST = {
        # month -> NE/SW monsoon impact (0-100 rainfall index)
        1: 15, 2: 10, 3: 8, 4: 12, 5: 18,
        6: 55, 7: 80, 8: 85, 9: 70, 10: 65,
        11: 75, 12: 45,
    }

    def generate_seasonal_forecast(
        self,
        lat: float,
        lon: float,
        farm_conditions: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Returns forecasts for 4 time horizons."""
        current_month = datetime.now().month
        temp = farm_conditions.get("avg_temperature", 30.0)
        rainfall_idx = self.MONSOON_FORECAST.get(current_month, 30)

        return {
            "7_day": self._generate_horizon("7-Day", current_month, temp, rainfall_idx, 0),
            "30_day": self._generate_horizon("30-Day", current_month, temp, rainfall_idx, 1),
            "3_month": self._generate_horizon("3-Month", current_month, temp, rainfall_idx, 3),
            "10_month": self._generate_horizon("10-Month", current_month, temp, rainfall_idx, 10),
        }

    def _generate_horizon(
        self, label: str, current_month: int, temp: float, rain_idx: int, month_offset: int
    ) -> Dict[str, Any]:
        future_month = ((current_month - 1 + month_offset) % 12) + 1
        future_rain = self.MONSOON_FORECAST.get(future_month, 30)
        avg_rain = (rain_idx + future_rain) / 2

        # Suitability score: 0-100
        temp_factor = max(0, 100 - abs(temp - 28) * 3)
        rain_factor = avg_rain
        suitability = int((temp_factor * 0.5 + rain_factor * 0.5))

        # Drought risk
        if avg_rain < 20:
            drought_risk = "High"
            drought_color = "red"
        elif avg_rain < 45:
            drought_risk = "Medium"
            drought_color = "amber"
        else:
            drought_risk = "Low"
            drought_color = "green"

        # Irrigation sustainability
        if avg_rain > 65:
            irrigation_status = "Rainfed Sufficient"
            irrigation_color = "blue"
        elif avg_rain > 35:
            irrigation_status = "Supplementary Needed"
            irrigation_color = "amber"
        else:
            irrigation_status = "Full Irrigation Required"
            irrigation_color = "red"

        return {
            "label": label,
            "suitability_score": suitability,
            "rainfall_index": int(avg_rain),
            "drought_risk": drought_risk,
            "drought_color": drought_color,
            "irrigation_status": irrigation_status,
            "irrigation_color": irrigation_color,
            "outlook": self._get_outlook_text(label, suitability, drought_risk),
        }

    def _get_outlook_text(self, label: str, score: int, drought: str) -> str:
        if score >= 70:
            return f"Favorable {label.lower()} outlook. Excellent conditions for agricultural activity."
        elif score >= 50:
            return f"Moderate {label.lower()} outlook. Monitor rainfall and irrigation carefully."
        else:
            return f"Challenging {label.lower()} period. {drought} drought risk — plan supplementary irrigation."


class YieldProjectionEngine:
    """
    Projects expected yield for recommended crops based on farm conditions,
    seasonal forecast, and soil quality.
    """

    def generate_yield_projections(
        self,
        crop_recommendations: List[Dict[str, Any]],
        farm_conditions: Dict[str, Any],
        seasonal_forecast: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Returns yield projections for top crops."""
        farm_size = farm_conditions.get("farm_size", 1.0)
        rainfall_idx = seasonal_forecast.get("10_month", {}).get("rainfall_index", 50)
        soil_quality = min(1.0, max(0.3, (farm_conditions.get("ph_level", 6.5) - 4) / 4))

        projections = []
        for crop in crop_recommendations[:6]:
            base_low, base_high = crop["yield_range_tons"]["low"], crop["yield_range_tons"]["high"]
            score = crop["score"]

            # Adjust by seasonal rainfall
            rain_factor = rainfall_idx / 100
            quality_factor = 0.7 + (soil_quality * 0.3)

            adj_low = round(base_low * rain_factor * quality_factor, 1)
            adj_expected = round((base_low + base_high) / 2 * rain_factor * quality_factor * score, 1)
            adj_high = round(base_high * score, 1)

            projections.append({
                "crop_name": crop["crop_name"],
                "crop_key": crop["crop_key"],
                "score": score,
                "yield_low_tons": max(0.1, adj_low),
                "yield_expected_tons": max(0.1, adj_expected),
                "yield_high_tons": max(0.1, adj_high),
                "farm_size_ha": farm_size,
                "risk_adjusted": True,
            })

        return projections


seasonal_forecasting_engine = SeasonalForecastingEngine()
yield_projection_engine = YieldProjectionEngine()
