from django.db import transaction
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.db.models import Prefetch
from .models import Appointment, Report, Profit, Consumption, Salary


class AppointmentRepository:
    @staticmethod
    def get():
        """Optimize queryset by selecting related objects."""
        return Appointment.objects.all().select_related("doctor", "patient", "service")


class ReportRepository:
    @staticmethod
    def get():
        """Annotate total profit, total consumption, and net profit for reports."""
        return (
            Report.objects.all()
            .prefetch_related(
                Prefetch(
                    "profits",
                    queryset=Profit.objects.all().select_related("appointment"),
                ),
                Prefetch("consumptions", queryset=Consumption.objects.all()),
            )
            .annotate(
                total_profit=Coalesce(
                    Sum("profits__amount"), 0, output_field=DecimalField()
                ),
                total_consumption=Coalesce(
                    Sum("consumptions__amount"), 0, output_field=DecimalField()
                ),
                net_profit=ExpressionWrapper(
                    F("total_profit") - F("total_consumption"),
                    output_field=DecimalField(max_digits=11, decimal_places=2),
                ),
            )
        )

    @staticmethod
    def get_annotated_report(report_id):
        """Helper method to get annotated report by id"""
        return (
            Report.objects.filter(id=report_id)
            .annotate(
                total_profit=Coalesce(
                    Sum("profits__amount"), 0, output_field=DecimalField()
                ),
                total_consumption=Coalesce(
                    Sum("consumptions__amount"), 0, output_field=DecimalField()
                ),
                net_profit=ExpressionWrapper(
                    F("total_profit") - F("total_consumption"),
                    output_field=DecimalField(max_digits=11, decimal_places=2),
                ),
            )
            .prefetch_related(
                Prefetch(
                    "profits",
                    queryset=Profit.objects.all().select_related("appointment"),
                ),
                Prefetch("consumptions", queryset=Consumption.objects.all()),
            )
            .first()
        )

    @staticmethod
    @transaction.atomic
    def add_entry(date, entry_model, **kwargs):
        """Add entry (profit or consumption) to the report"""
        report, _ = Report.objects.update_or_create(date=date)
        entry_model.objects.create(report=report, **kwargs)
        return ReportRepository.get_annotated_report(report.id)


class SalaryRepository:
    @staticmethod
    def get():
        """Optimize queryset by selecting related objects."""
        return Salary.objects.all()