from rest_framework import viewsets

from src.treatment.models import *

from .serializers import *


class AppointmentViewSet(viewsets.ModelViewSet):
    
    """Appointment model viewset"""
    
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class PaymentViewSet(viewsets.ModelViewSet):

    """Payment model viewset"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
