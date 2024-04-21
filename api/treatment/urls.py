from rest_framework import routers

from .views import *


router = routers.DefaultRouter()

router.register(r'appointments', AppointmentViewSet)
router.register(r'payments', PaymentViewSet)
