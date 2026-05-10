from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
from uuid import UUID

from app.repositories.farm import farm as farm_repo
from app.geospatial.location_validator import location_validator
from app.geospatial.farm_boundary_engine import farm_boundary_engine
from app.geospatial.spatial_aggregation import spatial_aggregation
from app.geospatial.microclimate_engine import microclimate_engine

class GeospatialService:
    """
    Orchestrates geospatial operations.
    """
    
    async def analyze_farm_microclimate(self, db: AsyncSession, farm_id: UUID) -> Dict[str, Any]:
        """
        Calculates microclimate anomalies for a registered farm.
        """
        farm = await farm_repo.get(db, id=farm_id)
        if not farm:
            raise ValueError(f"Farm {farm_id} not found.")
            
        lat = farm.latitude
        lon = farm.longitude
        radius = farm.analysis_radius or 5.0
        
        # If boundary polygon exists, override centroid
        if farm.boundary_polygon:
            lat, lon = farm_boundary_engine.get_centroid(farm.boundary_polygon)
            
        location_validator.validate(lat, lon)
        
        # Fetch regional baseline
        baseline = await spatial_aggregation.get_regional_baseline(db, lat, lon, radius)
        
        # Calculate local stats (For now we simulate local stats slightly offset from baseline)
        local_stats = {
            "avg_temperature": baseline["avg_temperature"] + 1.6, # simulate heat accumulation
            "avg_humidity": baseline["avg_humidity"] - 6.0, # simulate humidity drop
            "avg_rainfall": baseline["avg_rainfall"]
        }
        
        insights = microclimate_engine.analyze(local_stats, baseline, radius)
        
        return {
            "farm_id": str(farm.id),
            "farm_name": farm.farm_name,
            "center_lat": lat,
            "center_lon": lon,
            "radius_km": radius,
            "insights": insights,
            "local_stats": local_stats,
            "regional_baseline": baseline
        }
        
geo_service = GeospatialService()
