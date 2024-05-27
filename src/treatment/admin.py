from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Appointment, Payment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'service', 'price', 'start_time', 'end_time')
    search_fields = ('patient__phone', 'doctor__phone', 'service__name')
    list_filter = ('doctor', 'service', 'start_time')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment', 'paid_amount', 'created_at')
    search_fields = ('appointment__patient__phone', 'appointment__doctor__phone')