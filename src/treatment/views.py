from dateutil import parser as date_parser
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from src.base import MultiSerializerMixin
from src.treatment.models import Profit, Consumption, Report
from .serializers import (
    AppointmentSerializer,
    AppointmentReadSerializer,
    ReportSerializer,
    ProfitReadSerializer,
    ProfitWriteSerializer,
    ProfitAddSerializer,
    ConsumptionWriteSerializer,
    SalarySerializer,
    SalaryReadSerializer,
)
from .filters import AppointmentFilter, ReportFilter
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
            profit = Profit.objects.create(report=report, appointment=appointment, amount=amount)
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

            report = ReportRepository.get_annotated_report(report.id)
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

            report = ReportRepository.get_annotated_report(report.id)
            return Response(ReportSerializer(report).data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


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
        "list": SalaryReadSerializer,
        "retrieve": SalaryReadSerializer,
    }
