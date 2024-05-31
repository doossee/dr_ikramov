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
    
    patient = models.ForeignKey(
        verbose_name=_("Patient"), to=Patient, 
        on_delete=models.CASCADE, related_name='appointments'
    )
    doctor = models.ForeignKey(
        verbose_name=_("Doctor"), to=Doctor, 
        on_delete=models.SET_NULL, related_name='appointments', null=True
    )
    service = models.ForeignKey(
        verbose_name=_("Service"), to=Service, 
        on_delete=models.SET_NULL, related_name='appointments', null=True
    )
    price = models.DecimalField(verbose_name=_("Price"), max_digits=11, decimal_places=2)

    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(verbose_name=_("End Time"), null=True, blank=True)
    
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")

    def __str__(self) -> str:
        return f"{self.patient.first_name} - {self.service.name_en}"



class Report(models.Model):
    
    """Report model"""

    date = models.DateField(verbose_name=_("Date"), unique=True)

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")


class Profit(models.Model):

    """Payment model"""

    report = models.ForeignKey(
        verbose_name=_("Report"), to=Report, 
        on_delete=models.CASCADE, related_name='profits'
    )
    appointment = models.ForeignKey(
        verbose_name=_("Appointment"), to=Appointment, 
        on_delete=models.CASCADE, related_name='consumptions'
    )
    amount = models.DecimalField(verbose_name=_("Paid amount"), max_digits=11, decimal_places=2)

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self) -> str:
        return f"{self.appointment.patient.first_name} - {self.amount}"


class Consumption(models.Model):

    """Consumption model"""

    report = models.ForeignKey(
        verbose_name=_("Report"), to=Report, 
        on_delete=models.CASCADE, related_name='consumptions'
    )

    title = models.CharField(verbose_name=_("Consumption title"), max_length=255)
    description = models.TextField(verbose_name=_("Consumption description"), null=True, blank=True)

    amount = models.DecimalField(verbose_name=_("Paid amount"), max_digits=11, decimal_places=2)

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self) -> str:
        return f"{self.appointment.patient.first_name} - {self.amount}"