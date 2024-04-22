from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

from src.management.models import *

class Appointment(models.Model):
    
    """Appointment model"""
    
    patient = models.ForeignKey(verbose_name=_("Patient"), to=Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(verbose_name=_("Doctor"), to=Doctor, on_delete=models.SET_NULL, related_name='appointments', null=True)
    service = models.ForeignKey(verbose_name=_("Service"), to=Service, on_delete=models.SET_NULL, related_name='appointments', null=True)

    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(verbose_name=_("End Time"), null=True, blank=True)
    
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")


class Payment(models.Model):

    """Payment model"""

    CURRENCY_CHOICES = (
        ('uzs', _('Uzbekistan sum')),
        ('usd', _('United States dollar')),
    )

    appointment = models.ForeignKey(verbose_name=_("Appointment"), to=Appointment, on_delete=models.CASCADE, related_name='payments')
    paid_amount = models.DecimalField(verbose_name=_("Paid amount"), max_digits=11, decimal_places=2)
    currency = models.CharField(verbose_name=_("Currency"), max_length=3, choices=CURRENCY_CHOICES)

    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)