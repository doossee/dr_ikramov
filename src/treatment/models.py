from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from src.management.models import Patient, Doctor, Service

from .choices import StatusChoices


class Appointment(models.Model):
    """Appointment model"""

    patient = models.ForeignKey(
        verbose_name=_("Patient"),
        to=Patient,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    doctor = models.ForeignKey(
        verbose_name=_("Doctor"),
        to=Doctor,
        on_delete=models.SET_NULL,
        related_name="appointments",
        null=True,
    )
    service = models.ForeignKey(
        verbose_name=_("Service"),
        to=Service,
        on_delete=models.SET_NULL,
        related_name="appointments",
        null=True,
    )
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=11, decimal_places=2
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )

    start_time = models.DateTimeField(verbose_name=_("Start time"))
    end_time = models.DateTimeField(verbose_name=_("End time"), null=True, blank=True)

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")

    def __str__(self) -> str:
        return f"{self.patient.first_name} - {self.service.name_en}"

    def save(self, *args, **kwargs):
        # Only perform the check if the appointment already exists (i.e., not on creation)
        if self.pk:
            # Calculate the total profit amount related to this appointment
            total_profit = self.profits.aggregate(total=Sum('amount'))['total'] or 0

            # If the total profit equals the price, set the status to PAID
            if self.price == total_profit:
                self.status = StatusChoices.PAID

        # Call the superclass save method to save the instance
        super().save(*args, **kwargs)


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
        verbose_name=_("Report"),
        to=Report,
        on_delete=models.CASCADE,
        related_name="profits",
    )
    appointment = models.ForeignKey(
        verbose_name=_("Appointment"),
        to=Appointment,
        on_delete=models.CASCADE,
        related_name="profits",
    )
    amount = models.DecimalField(
        verbose_name=_("Paid amount"), max_digits=11, decimal_places=2
    )

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self) -> str:
        return f"{self.appointment.patient.first_name} - {self.amount}"

    def save(self, *args, **kwargs):
        if self.pk:
            self.appointment.doctor.balance += (
                self.amount * self.appointment.service.kpi_percent
            ) / 100
        super(Profit, self).save(*args, **kwargs)


class Consumption(models.Model):
    """Consumption model"""

    report = models.ForeignKey(
        verbose_name=_("Report"),
        to=Report,
        on_delete=models.CASCADE,
        related_name="consumptions",
    )

    title = models.CharField(verbose_name=_("Consumption title"), max_length=255)
    description = models.TextField(
        verbose_name=_("Consumption description"), null=True, blank=True
    )

    amount = models.DecimalField(
        verbose_name=_("Paid amount"), max_digits=11, decimal_places=2
    )

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self) -> str:
        return f"{self.appointment.patient.first_name} - {self.amount}"
