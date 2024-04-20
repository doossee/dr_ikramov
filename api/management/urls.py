from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'admins', AdminViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
