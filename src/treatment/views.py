from rest_framework import viewsets

from src.base import MultiSerializerMixin

from src.treatment.models import *

from .serializers import (
    AppointmentSerializer,
    AppointmentReadSerializer,
    PaymentSerializer
)
from .filters import AppointmentFilter


class AppointmentViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    
    """Appointment model viewset"""
    
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    serializer_action_classes = {
        "list": AppointmentReadSerializer,
        "retrieve": AppointmentReadSerializer
    }
    # filterset_fields = ['doctor', 'start_time', 'end_time']
    filterset_class = AppointmentFilter

    def get_queryset(self):
        qs = super().get_queryset().select_related(
            "doctor", "patient", "service"
        )
        return qs


class PaymentViewSet(viewsets.ModelViewSet):

    """Payment model viewset"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
