from app.repositories.base import CRUDBase
from app.models.weather import WeatherData
from app.models.soil import SoilData
from app.models.environment import EnvironmentalMetrics
from app.schemas.weather import WeatherDataCreate, WeatherDataBase
from app.schemas.soil import SoilDataCreate, SoilDataBase
from app.schemas.ai import EnvMetricsCreate, EnvMetricsBase

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

class RepositoryWeatherData(CRUDBase[WeatherData, WeatherDataCreate, WeatherDataBase]):
    async def get_by_farm(self, db: AsyncSession, farm_id: UUID, limit: int = 168) -> List[WeatherData]:
        query = select(self.model).where(self.model.farm_id == farm_id).order_by(self.model.recorded_at.desc()).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
class RepositorySoilData(CRUDBase[SoilData, SoilDataCreate, SoilDataBase]):
    pass

class RepositoryEnvMetrics(CRUDBase[EnvironmentalMetrics, EnvMetricsCreate, EnvMetricsBase]):
    pass

weather = RepositoryWeatherData(WeatherData)
soil = RepositorySoilData(SoilData)
environment = RepositoryEnvMetrics(EnvironmentalMetrics)
