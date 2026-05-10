from app.repositories.base import CRUDBase
from app.models.alert import Alert
from app.models.crop import CropProfile
from app.schemas.operations import AlertCreate, AlertUpdate, CropProfileCreate, CropProfileUpdate

class RepositoryAlert(CRUDBase[Alert, AlertCreate, AlertUpdate]):
    pass

class RepositoryCropProfile(CRUDBase[CropProfile, CropProfileCreate, CropProfileUpdate]):
    pass

alert = RepositoryAlert(Alert)
crop_profile = RepositoryCropProfile(CropProfile)
