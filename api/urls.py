from core.routers import DefaultRouter
from api.management.urls import router as management_router


router = DefaultRouter()

router.extend(management_router)

