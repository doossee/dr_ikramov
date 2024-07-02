from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    AdminViewSet,
    DoctorViewSet,
    PatientViewSet,
    SpecialtyViewSet,
    ServiceViewSet,
    InitialRecordViewSet,
    RatingViewSet
)

router = DefaultRouter()

router.register(r"users", UserViewSet)
router.register(r"admins", AdminViewSet)
router.register(r"doctors", DoctorViewSet, basename="doctor")
router.register(r"patients", PatientViewSet)
router.register(r"specialties", SpecialtyViewSet)
router.register(r"services", ServiceViewSet)
router.register(r"initial-records", InitialRecordViewSet)
router.register(r"ratings", RatingViewSet)
