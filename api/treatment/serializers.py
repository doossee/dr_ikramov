from rest_framework import serializers

from src.treatment.models import *


class AppointmentSerializer(serializers.ModelSerializer):
    
    """Appointment model serializer"""
    
    class Meta:
        model = Appointment
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    """Payment model serializer"""
    
    class Meta:
        model = Payment
        fields = '__all__'
