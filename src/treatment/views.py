from dateutil import parser as date_parser
from django.utils.dateparse import parse_date
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from src.base import MultiSerializerMixin
from src.treatment.models import Report, Profit, Consumption, Salary
from .serializers import (
    AppointmentSerializer,
    AppointmentReadSerializer,
    ReportSerializer,
    ProfitReadSerializer,
    ProfitWriteSerializer,
    ProfitAddSerializer,
    ConsumptionWriteSerializer,
    SalarySerializer,
    SalaryWriteSerializer,
)
from .filters import AppointmentFilter, ReportFilter, SalaryFilter
from .repository import AppointmentRepository, ReportRepository, SalaryRepository


class AppointmentViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    """Appointment model viewset"""

    queryset = AppointmentRepository.get()
    serializer_class = AppointmentSerializer
    serializer_action_classes = {
        "list": AppointmentReadSerializer,
        "retrieve": AppointmentReadSerializer,
    }
    filterset_class = AppointmentFilter

    @action(detail=True, methods=["post"], serializer_class=ProfitAddSerializer)
    def add_profit(self, request, pk=None):
        """Add profit report action"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appointment = self.get_object()
        date = serializer.validated_data["date"]
        amount = serializer.validated_data["amount"]

        try:
            report, created = Report.objects.update_or_create(date=date)
            profit = Profit.objects.create(
                report=report, appointment=appointment, amount=amount
            )
            appointment.save()
            return Response(ProfitReadSerializer(profit).data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ReportViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Report model viewset"""

    queryset = ReportRepository.get()
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

    @action(detail=False, methods=["get"], url_path="range")
    def get_reports_in_range(self, request):
        """Retrieve aggregated totals and a list of reports within a specified date range."""
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        # Validate and parse dates
        if not start_date_str or not end_date_str:
            return Response(
                {
                    "error": "Both 'start_date' and 'end_date' query parameters are required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not start_date or not end_date:
            return Response(
                {"error": "Both 'start_date' and 'end_date' must be valid dates."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if start_date > end_date:
            return Response(
                {"error": "'start_date' must be before 'end_date'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get aggregated totals and list of reports
        data = ReportRepository.get_reports_in_range(start_date, end_date)

        # Serialize the list of reports
        report_serializer = ReportSerializer(data["reports"], many=True)

        return Response(
            {
                "aggregated_totals": data["aggregated_totals"],
                "reports": report_serializer.data,
            }
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
            report, _ = Report.objects.update_or_create(date=date)
            Profit.objects.create(report=report, appointment=appointment, amount=amount)

            report = ReportRepository.get_annotated_report(report.id)
            return Response(ReportSerializer(report).data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            report, _ = Report.objects.update_or_create(date=date)
            Consumption.objects.create(
                report=report, title=title, description=description, amount=amount
            )

            report = ReportRepository.get_annotated_report(report.id)
            return Response(ReportSerializer(report).data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"], serializer_class=SalaryWriteSerializer)
    def add_salary(self, request):
        """Add consumption report action"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        date = serializer.validated_data["date"]
        title = serializer.validated_data["title"]
        description = serializer.validated_data["description"]
        amount = serializer.validated_data["amount"]
        doctor = serializer.validated_data["doctor"]

        try:
            report, _ = Report.objects.update_or_create(date=date)
            Salary.objects.create(
                report=report,
                title=title,
                description=description,
                amount=amount,
                doctor=doctor,
            )

            report = ReportRepository.get_annotated_report(report.id)
            return Response(ReportSerializer(report).data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SalaryViewSet(
    MultiSerializerMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Salary model view set"""

    queryset = SalaryRepository.get()
    serializer_class = SalarySerializer
    serializer_action_classes = {
        "create": SalaryWriteSerializer,
    }
    filterset_class = SalaryFilter

    def create(self, request, *args, **kwargs):
        """Create a new salary instance"""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        date = serializer.validated_data["date"]
        title = serializer.validated_data["title"]
        description = serializer.validated_data["description"]
        amount = serializer.validated_data["amount"]
        doctor = serializer.validated_data["doctor"]

        headers = self.get_success_headers(serializer.data)

        try:
            report, _ = Report.objects.update_or_create(date=date)
            Salary.objects.create(
                report=report,
                title=title,
                description=description,
                amount=amount,
                doctor=doctor,
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
