from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

from src.management.models import (
    Patient,
    Doctor,
    Service
)


class Appointment(models.Model):
    
    """Appointment model"""
    
    patient = models.ForeignKey(verbose_name=_("Patient"), to=Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(verbose_name=_("Doctor"), to=Doctor, on_delete=models.SET_NULL, related_name='appointments', null=True)
    service = models.ForeignKey(verbose_name=_("Service"), to=Service, on_delete=models.SET_NULL, related_name='appointments', null=True)
    price = models.DecimalField(verbose_name=_("Price"), max_digits=11, decimal_places=2)

    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(verbose_name=_("End Time"), null=True, blank=True)
    
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")

    def __str__(self) -> str:
        return f"{self.patient.first_name} - {self.service.name}"



class Payment(models.Model):

    """Payment model"""

    appointment = models.ForeignKey(verbose_name=_("Appointment"), to=Appointment, on_delete=models.CASCADE, related_name='payments')
    paid_amount = models.DecimalField(verbose_name=_("Paid amount"), max_digits=11, decimal_places=2)

    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self) -> str:
        return f"{self.appointment.patient.first_name} - {self.paid_amount}"