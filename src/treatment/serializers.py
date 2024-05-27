from rest_framework import serializers

from src.management.models import (
    Doctor, Patient, Service
)
from .models import Appointment, Payment


class AppointmentSerializer(serializers.ModelSerializer):
    
    """Appointment model serializer"""
    
    class Meta:
        model = Appointment
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):

    """Doctor model serializer"""
    
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'phone']


class AppointmentReadSerializer(serializers.ModelSerializer):
    
    """Appointment model serializer"""
    
    doctor = DoctorSerializer(read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
    

class PaymentSerializer(serializers.ModelSerializer):

    """Payment model serializer"""
    
    class Meta:
        model = Payment
        fields = '__all__'
