from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from src.management.models import Patient, Doctor, Service
from .choices import StatusChoices
from .services import update_appointment_status, update_doctor_balance_on_profit, update_doctor_balance_on_salary


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
        if self.pk:
            self = update_appointment_status(self)
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
    """Profit model"""

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
        verbose_name = _("Profit")
        verbose_name_plural = _("Profits")

    def __str__(self) -> str:
        return f"{self.appointment.patient.first_name} - {self.amount}"

    @transaction.atomic
    def save(self, *args, **kwargs):
        self = update_doctor_balance_on_profit(self)
        super().save(*args, **kwargs)


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
        verbose_name = _("Consumption")
        verbose_name_plural = _("Consumptions")

    def __str__(self) -> str:
        return f"{self.title} - {self.amount}"


class Salary(models.Model):
    """Salary model"""

    doctor = models.ForeignKey(
        verbose_name=_("Doctor"),
        to=Doctor,
        on_delete=models.CASCADE,
        related_name="salaries",
    )
    amount = models.DecimalField(
        verbose_name=_("Amount"), max_digits=11, decimal_places=2
    )
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Salary")
        verbose_name_plural = _("Salaries")

    def __str__(self):
        return f"{self.id}-{self.doctor.first_name}-{self.doctor.last_name}"

    @transaction.atomic
    def save(self, *args, **kwargs):
        self = update_doctor_balance_on_salary(self)
        super().save(*args, **kwargs)
