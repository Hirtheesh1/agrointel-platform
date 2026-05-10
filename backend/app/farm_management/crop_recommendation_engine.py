from typing import Dict, Any, List
from app.farm_management.crop_lifecycle_engine import crop_lifecycle_engine, TAMIL_NADU_CROPS


class CropRecommendationEngine:
    """
    Scores and ranks crops for a given farm based on soil, weather, and lifecycle data.
    Produces human-readable reasoning for each recommendation.
    """

    def generate_recommendations(self, farm_conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Returns a ranked list of crop recommendations with scores and reasoning.
        farm_conditions: {ph_level, avg_temperature, avg_humidity, water_availability, farm_size, rainfall_mm, season}
        """
        results = []

        for crop_key, crop_data in TAMIL_NADU_CROPS.items():
            score = crop_lifecycle_engine.match_crop_to_farm(crop_key, farm_conditions)

            # Build natural language reasoning
            reasoning = self._build_reasoning(crop_key, crop_data, farm_conditions, score)

            # Yield estimate
            farm_size_ha = farm_conditions.get("farm_size", 1.0)
            yield_low = round(crop_data["yield_range_tons"][0] * farm_size_ha, 1)
            yield_high = round(crop_data["yield_range_tons"][1] * farm_size_ha, 1)

            results.append({
                "crop_key": crop_key,
                "crop_name": crop_data["display_name"],
                "season": crop_data["season"],
                "score": score,
                "confidence": "High" if score >= 0.75 else "Medium" if score >= 0.5 else "Low",
                "status": "Recommended" if score >= 0.7 else "Monitor" if score >= 0.45 else "Not Recommended",
                "total_days": crop_data["total_days"],
                "water_need_mm_day": crop_data["water_need_mm_day"],
                "yield_range_tons": {"low": yield_low, "high": yield_high},
                "reasoning": reasoning,
            })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:10]  # Top 10

    def _build_reasoning(
        self,
        crop_key: str,
        crop_data: Dict[str, Any],
        farm_conditions: Dict[str, Any],
        score: float,
    ) -> str:
        """Generates an AI-style explanation for the recommendation."""
        current_season = crop_lifecycle_engine.get_current_season()
        crop_name = crop_data["display_name"]
        parts = []

        # Season fit
        if crop_data["season"] == "perennial":
            parts.append(f"{crop_name} is a perennial crop suitable year-round.")
        elif crop_data["season"] == current_season:
            parts.append(f"{crop_name} is well-aligned with the current {current_season.capitalize()} season.")
        else:
            parts.append(f"{crop_name} is typically grown in {crop_data['season'].capitalize()} season — currently off-season.")

        # pH fit
        ph = farm_conditions.get("ph_level", 6.5)
        if crop_data["soil_ph_min"] <= ph <= crop_data["soil_ph_max"]:
            parts.append(f"Soil pH ({ph:.1f}) is optimal for this crop.")
        else:
            parts.append(f"Soil pH ({ph:.1f}) is outside ideal range ({crop_data['soil_ph_min']}–{crop_data['soil_ph_max']}).")

        # Temperature fit
        temp = farm_conditions.get("avg_temperature", 30.0)
        if crop_data["temp_min_c"] <= temp <= crop_data["temp_max_c"]:
            parts.append(f"Current temperature ({temp:.0f}°C) is within the preferred range.")
        else:
            parts.append(f"Temperature ({temp:.0f}°C) may stress this crop (preferred: {crop_data['temp_min_c']}–{crop_data['temp_max_c']}°C).")

        # Confidence summary
        if score >= 0.75:
            parts.append(f"{crop_name} cultivation shows HIGH success probability for this farm zone.")
        elif score >= 0.5:
            parts.append(f"{crop_name} shows MODERATE potential — monitor conditions during growing season.")
        else:
            parts.append(f"{crop_name} is NOT recommended under current farm conditions.")

        return " ".join(parts)


crop_recommendation_engine = CropRecommendationEngine()
