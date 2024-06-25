from datetime import datetime
from dateutil import parser as date_parser
from django.db.models import Prefetch, Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from src.base import MultiSerializerMixin
from src.treatment.models import Appointment, Report, Profit, Consumption
from .serializers import (
    AppointmentSerializer,
    AppointmentReadSerializer,
    ReportSerializer,
    ProfitWriteSerializer,
    ConsumptionWriteSerializer,
)
from .filters import AppointmentFilter, ReportFilter


class AppointmentViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    """Appointment model viewset"""

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    serializer_action_classes = {
        "list": AppointmentReadSerializer,
        "retrieve": AppointmentReadSerializer,
    }
    filterset_class = AppointmentFilter

    def get_queryset(self):
        """Optimize queryset by selecting related objects."""
        return super().get_queryset().select_related("doctor", "patient", "service")


class ReportViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Report model viewset"""

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filterset_class = ReportFilter
    lookup_field = "date"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        by_date = request.query_params.get("by_date")

        if by_date:
            try:
                # Validate date using dateutil.parser
                parsed_date = date_parser.parse(by_date)
                # Optionally, reformat the date if needed
                by_date = parsed_date.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                raise ValidationError(
                    {"by_date": "Invalid date format. Please use a valid date."}
                )

            # Filter queryset by the validated date
            queryset = queryset.filter(date=by_date)  # 2024-05-31

        else:
            raise ValidationError(detail="Your should set by_date query param")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        """Annotate total profit, total consumption, and net profit for reports."""
        return (
            super()
            .get_queryset()
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

    @action(detail=False, methods=["post"], serializer_class=ProfitWriteSerializer)
    def add_profit(self, request):
        """Add profit report action"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        date = serializer.validated_data["date"]
        appointment = serializer.validated_data["appointment"]
        amount = serializer.validated_data["amount"]

        try:
            report, created = Report.objects.update_or_create(date=date)
            Profit.objects.create(report=report, appointment=appointment, amount=amount)

            report = self.get_annotated_report(report.id)
            return Response(ReportSerializer(report).data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @action(detail=False, methods=["post"], serializer_class=ConsumptionWriteSerializer)
    def add_consumption(self, request):
        """Add consumption report action"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        date = serializer.validated_data["date"]
        title = serializer.validated_data["title"]
        description = serializer.validated_data["description"]
        amount = serializer.validated_data["amount"]

        try:
            report, created = Report.objects.update_or_create(date=date)
            Consumption.objects.create(
                report=report, title=title, description=description, amount=amount
            )

            report = self.get_annotated_report(report.id)
            return Response(ReportSerializer(report).data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def get_annotated_report(self, report_id):
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
