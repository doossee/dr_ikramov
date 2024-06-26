from rest_framework import routers

from .views import AppointmentViewSet, ReportViewSet, SalaryViewSet


router = routers.DefaultRouter()

router.register(r"appointments", AppointmentViewSet)
router.register(r"reports", ReportViewSet)
router.register(r"salaries", SalaryViewSet)
