from django.db.models import Sum, DecimalField, ExpressionWrapper
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
        reports = (
            Report.objects.all()
            .prefetch_related(
                Prefetch(
                    "profits",
                    queryset=Profit.objects.all().select_related(
                        "appointment",
                        "appointment__patient__user_ptr",
                        "appointment__doctor__user_ptr",
                        "appointment__service",
                    ),
                ),
                Prefetch(
                    "consumptions",
                    queryset=Consumption.objects.all().select_related(
                        "salary", "salary__doctor__user_ptr"
                    ),
                ),
            )
            .annotate(
                total_profit=Coalesce(
                    Sum("profits__amount"), 0, output_field=DecimalField()
                ),
                total_consumption=Coalesce(
                    Sum("consumptions__amount"), 0, output_field=DecimalField()
                ),
                net_profit=ExpressionWrapper(
                    Coalesce(Sum("profits__amount"), 0, output_field=DecimalField())
                    - Coalesce(
                        Sum("consumptions__amount"), 0, output_field=DecimalField()
                    ),
                    output_field=DecimalField(max_digits=11, decimal_places=2),
                ),
            )
        )
        return reports

    @staticmethod
    def get_annotated_report(report_id):
        """Helper method to get annotated report by id"""
        report = (
            Report.objects.filter(id=report_id)
            .prefetch_related(
                Prefetch(
                    "profits",
                    queryset=Profit.objects.all().select_related(
                        "appointment",
                        "appointment__patient__user_ptr",
                        "appointment__doctor__user_ptr",
                        "appointment__service",
                    ),
                ),
                Prefetch(
                    "consumptions",
                    queryset=Consumption.objects.all().select_related(
                        "salary", "salary__doctor__user_ptr"
                    ),
                ),
            )
            .annotate(
                total_profit=Coalesce(
                    Sum("profits__amount"), 0, output_field=DecimalField()
                ),
                total_consumption=Coalesce(
                    Sum("consumptions__amount"), 0, output_field=DecimalField()
                ),
                net_profit=ExpressionWrapper(
                    Coalesce(Sum("profits__amount"), 0, output_field=DecimalField())
                    - Coalesce(
                        Sum("consumptions__amount"), 0, output_field=DecimalField()
                    ),
                    output_field=DecimalField(max_digits=11, decimal_places=2),
                ),
            )
            .first()
        )
        return report

    @staticmethod
    def get_reports_in_range(start_date, end_date):
        """Retrieve individual reports and aggregated totals within the specified date range."""
        # Get individual reports within the date range
        reports = (
            Report.objects.filter(date__range=(start_date, end_date))
            .prefetch_related(
                Prefetch(
                    "profits",
                    queryset=Profit.objects.all().select_related(
                        "appointment",
                        "appointment__patient__user_ptr",
                        "appointment__doctor__user_ptr",
                        "appointment__service",
                    ),
                ),
                Prefetch(
                    "consumptions",
                    queryset=Consumption.objects.all().select_related(
                        "salary", "salary__doctor__user_ptr"
                    ),
                ),
            )
            .annotate(
                total_profit=Coalesce(
                    Sum("profits__amount"), 0, output_field=DecimalField()
                ),
                total_consumption=Coalesce(
                    Sum("consumptions__amount"), 0, output_field=DecimalField()
                ),
                net_profit=ExpressionWrapper(
                    Coalesce(Sum("profits__amount"), 0, output_field=DecimalField())
                    - Coalesce(
                        Sum("consumptions__amount"), 0, output_field=DecimalField()
                    ),
                    output_field=DecimalField(max_digits=11, decimal_places=2),
                ),
            )
        )

        # Calculate aggregated totals across all reports in Python
        total_profit = sum(report.total_profit for report in reports)
        total_consumption = sum(report.total_consumption for report in reports)
        net_profit = total_profit - total_consumption

        return {
            "aggregated_totals": {
                "total_profit": total_profit,
                "total_consumption": total_consumption,
                "net_profit": net_profit,
            },
            "reports": reports,
        }


class SalaryRepository:
    @staticmethod
    def get():
        """Optimize queryset by selecting related objects."""
        return Salary.objects.all().select_related("doctor")
