from typing import Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.farm import Farm
from app.models.soil import SoilData
from app.farm_management.crop_recommendation_engine import crop_recommendation_engine
from app.farm_management.irrigation_decision_engine import irrigation_decision_engine
from app.farm_management.agricultural_timeline_engine import agricultural_timeline_engine
from app.farm_management.seasonal_forecasting_engine import (
    seasonal_forecasting_engine, yield_projection_engine
)
from app.geospatial.spatial_aggregation import spatial_aggregation


class FarmDecisionEngine:
    """
    Master orchestrator that generates a complete farm intelligence report.
    Single entry point: generate_farm_intelligence(farm_id, db)
    """

    async def generate_farm_intelligence(
        self, farm_id: UUID, db: AsyncSession
    ) -> Dict[str, Any]:
        """Returns a comprehensive farm decision intelligence report."""

        # 1. Load farm
        farm = await db.get(Farm, farm_id)
        if not farm:
            raise ValueError(f"Farm {farm_id} not found.")

        # 2. Load latest soil data
        soil_result = await db.execute(
            select(SoilData)
            .where(SoilData.farm_id == farm_id)
            .order_by(SoilData.recorded_at.desc())
            .limit(1)
        )
        soil = soil_result.scalar_one_or_none()

        # 3. Build farm conditions object
        farm_conditions = self._build_farm_conditions(farm, soil)

        # 4. Fetch live environmental data
        try:
            env_data = await spatial_aggregation.get_regional_baseline(
                db, farm.latitude, farm.longitude, farm.analysis_radius or 5.0
            )
            farm_conditions["avg_temperature"] = env_data.get("avg_temperature", 30.0)
            farm_conditions["avg_humidity"] = env_data.get("avg_humidity", 65.0)
        except Exception:
            farm_conditions["avg_temperature"] = 30.0
            farm_conditions["avg_humidity"] = 65.0

        # 5. Generate all intelligence modules
        crop_recs = crop_recommendation_engine.generate_recommendations(farm_conditions)

        irrigation_advice = await irrigation_decision_engine.generate_irrigation_advice(
            farm.latitude, farm.longitude, farm_conditions
        )

        seasonal_forecast = seasonal_forecasting_engine.generate_seasonal_forecast(
            farm.latitude, farm.longitude, farm_conditions
        )

        yield_projections = yield_projection_engine.generate_yield_projections(
            crop_recs, farm_conditions, seasonal_forecast
        )

        # Use top crop for timeline
        top_crop = crop_recs[0] if crop_recs else {"crop_name": "Paddy", "total_days": 135}
        timeline = agricultural_timeline_engine.generate_timeline(
            crop_name=top_crop["crop_name"],
            crop_total_days=top_crop["total_days"],
            farm_conditions=farm_conditions,
        )

        # 6. Compute farm health score
        health_score = self._compute_health_score(
            farm_conditions, crop_recs, seasonal_forecast
        )

        return {
            "farm_id": str(farm.id),
            "farm_name": farm.farm_name,
            "location_name": farm.location_name,
            "farm_size_ha": farm.farm_size,
            "active_crop": farm.active_crop,
            "farm_conditions": farm_conditions,
            "health_score": health_score,
            "crop_recommendations": crop_recs,
            "irrigation_advice": irrigation_advice,
            "seasonal_forecast": seasonal_forecast,
            "yield_projections": yield_projections,
            "agricultural_timeline": timeline,
        }

    def _build_farm_conditions(self, farm: Farm, soil: SoilData | None) -> Dict[str, Any]:
        """Assembles the farm_conditions dict from model data."""
        return {
            "farm_size": farm.farm_size or 1.0,
            "irrigation_method": farm.irrigation_method or "drip",
            "water_availability": farm.water_availability or 50.0,
            "active_crop": farm.active_crop or "Paddy",
            "soil_type": farm.soil_type or "loamy",
            "crop_factor": 0.85,
            # Soil analytics (from latest reading or defaults)
            "ph_level": soil.ph_level if soil else 6.5,
            "nitrogen_level": soil.nitrogen_level if soil else 120.0,
            "phosphorus_level": soil.phosphorus_level if soil else 45.0,
            "potassium_level": soil.potassium_level if soil else 80.0,
            "soil_moisture": soil.soil_moisture if soil else 45.0,
        }

    def _compute_health_score(
        self,
        farm_conditions: Dict[str, Any],
        crop_recs: list,
        seasonal_forecast: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Computes an overall farm health score (0-100)."""
        top_crop_score = (crop_recs[0]["score"] * 100) if crop_recs else 50
        season_score = seasonal_forecast.get("30_day", {}).get("suitability_score", 50)
        soil_ph = farm_conditions.get("ph_level", 6.5)
        ph_score = 100 - abs(soil_ph - 6.5) * 20

        overall = int((top_crop_score * 0.4 + season_score * 0.4 + ph_score * 0.2))
        overall = max(0, min(100, overall))

        if overall >= 75:
            status = "Excellent"
            color = "green"
        elif overall >= 55:
            status = "Good"
            color = "amber"
        elif overall >= 35:
            status = "Fair"
            color = "orange"
        else:
            status = "Poor"
            color = "red"

        return {"score": overall, "status": status, "color": color}


farm_decision_engine = FarmDecisionEngine()
