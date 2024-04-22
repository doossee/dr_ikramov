from core.routers import DefaultRouter
from api.management.urls import router as management_router
from api.treatment.urls import router as treatment_router


router = DefaultRouter()

router.extend(management_router)
router.extend(treatment_router)

