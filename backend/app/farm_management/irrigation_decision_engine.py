from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.ingestion.weather_client import OpenWeatherClient
from app.ingestion.exceptions import APIClientError


class IrrigationDecisionEngine:
    """
    Generates farm-specific irrigation schedules based on live weather,
    soil moisture, crop water needs, and rain probability forecasts.
    """

    def __init__(self):
        self.weather_client = OpenWeatherClient()

    async def generate_irrigation_advice(
        self, lat: float, lon: float, farm_conditions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fetches live weather data and generates actionable irrigation decisions.
        """
        try:
            raw = await self.weather_client.fetch_current_weather(lat, lon)
            rain_1h = raw.get("rain", {}).get("1h", 0.0)
            cloud_cover = raw.get("clouds", {}).get("all", 0)
            temp = raw["main"]["temp"]
            humidity = raw["main"]["humidity"]
            wind_speed = raw.get("wind", {}).get("speed", 0.0)
        except APIClientError:
            # Fallback values for offline mode
            rain_1h = 0.0
            cloud_cover = 40
            temp = 33.0
            humidity = 65
            wind_speed = 3.0

        # Estimate rain probability from cloud cover + humidity
        rain_probability = min(100, int(cloud_cover * 0.7 + humidity * 0.3 - 20))
        rain_probability = max(0, rain_probability)

        # Calculate ETo (Penman-Monteith simplified)
        eto = max(0, (0.0023 * (temp + 17.8) * (40 - humidity / 100 * 40) * 0.408))
        crop_factor = farm_conditions.get("crop_factor", 0.85)
        etc = eto * crop_factor  # Crop evapotranspiration

        # Determine irrigation action
        soil_moisture = farm_conditions.get("soil_moisture", 45.0)
        active_crop = farm_conditions.get("active_crop", "Paddy")

        if rain_probability > 70:
            action = "reduce"
            reduction_pct = 40 if rain_probability > 80 else 25
            decision_text = (
                f"Rain probability is {rain_probability}%. "
                f"Reduce irrigation by {reduction_pct}% for the next 24 hours to prevent waterlogging and nutrient leaching."
            )
        elif soil_moisture < 30 or (temp > 36 and rain_probability < 20):
            action = "increase"
            decision_text = (
                f"Soil moisture is low ({soil_moisture:.0f}%) and rain probability is {rain_probability}%. "
                f"Increase irrigation by 30% to support {active_crop} during heat stress."
            )
        else:
            action = "normal"
            decision_text = (
                f"Conditions are stable. Maintain normal irrigation schedule. "
                f"Estimated evapotranspiration: {etc:.1f} mm/day."
            )

        # Generate 7-day schedule
        schedule = self._generate_weekly_schedule(rain_probability, temp, etc, active_crop)

        return {
            "action": action,
            "decision_text": decision_text,
            "rain_probability_pct": rain_probability,
            "temperature_c": round(temp, 1),
            "humidity_pct": humidity,
            "etc_mm_day": round(etc, 2),
            "soil_moisture_pct": soil_moisture,
            "weekly_schedule": schedule,
        }

    def _generate_weekly_schedule(
        self, rain_prob: int, temp: float, etc: float, crop: str
    ) -> List[Dict[str, Any]]:
        """Generates a 7-day irrigation recommendation schedule."""
        today = datetime.now()
        schedule = []

        for i in range(7):
            day = today + timedelta(days=i)
            # Simulate slight weather variation across the week
            day_rain = max(0, min(100, rain_prob + (i * 5 - 15) + ((-1) ** i * 8)))
            day_temp = temp + (i % 3 - 1) * 1.5

            if day_rain > 70:
                rec = "Skip"
                water_mm = 0
            elif day_rain > 40:
                rec = "Reduce (25%)"
                water_mm = round(etc * 0.75, 1)
            elif day_temp > 37:
                rec = "Increase (30%)"
                water_mm = round(etc * 1.30, 1)
            else:
                rec = "Normal"
                water_mm = round(etc, 1)

            schedule.append({
                "date": day.strftime("%b %d"),
                "day": day.strftime("%A"),
                "recommendation": rec,
                "water_mm": water_mm,
                "rain_prob_pct": int(day_rain),
            })

        return schedule


irrigation_decision_engine = IrrigationDecisionEngine()
