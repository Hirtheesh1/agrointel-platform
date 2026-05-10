from app.repositories.base import CRUDBase
from app.models.farm import Farm
from app.schemas.farm import FarmCreate, FarmUpdate

class RepositoryFarm(CRUDBase[Farm, FarmCreate, FarmUpdate]):
    pass

farm = RepositoryFarm(Farm)
