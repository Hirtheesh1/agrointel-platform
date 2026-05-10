from typing import Dict, Any

class MicroclimateEngine:
    """
    Analyzes localized environmental behavior compared to regional baselines.
    Outputs human-readable geospatial intelligence.
    """

    def analyze(self, local_stats: Dict[str, Any], regional_baseline: Dict[str, Any], radius_km: float) -> Dict[str, Any]:
        """
        Compares local to regional.
        """
        insights = []
        anomalies = []

        # Temperature Delta
        temp_diff = local_stats.get("avg_temperature", 30) - regional_baseline.get("avg_temperature", 30)
        if temp_diff > 1.5:
            insights.append(f"Localized heat accumulation detected within the {radius_km}km zone (+{temp_diff:.1f}°C vs region).")
            anomalies.append("heat_concentration")
        elif temp_diff < -1.5:
            insights.append(f"Microclimate is significantly cooler than surrounding region ({temp_diff:.1f}°C).")

        # Humidity Delta
        hum_diff = local_stats.get("avg_humidity", 60) - regional_baseline.get("avg_humidity", 60)
        if hum_diff < -5.0:
            insights.append(f"Declining humidity within the {radius_km}km zone suggests increasing evapotranspiration stress.")
            anomalies.append("humidity_instability")

        if not insights:
            insights.append(f"Environmental conditions within the {radius_km}km zone are stable and match regional patterns.")

        text_explanation = " ".join(insights)

        return {
            "text_explanation": text_explanation,
            "anomalies": anomalies,
            "temp_delta": round(temp_diff, 2),
            "humidity_delta": round(hum_diff, 2)
        }

microclimate_engine = MicroclimateEngine()
