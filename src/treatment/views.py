from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import APIException

from src.base import MultiSerializerMixin
from src.treatment.models import Profit, Consumption
from .serializers import (
    AppointmentSerializer,
    AppointmentReadSerializer,
    ReportSerializer,
    ProfitWriteSerializer,
    ConsumptionWriteSerializer,
    SalarySerializer,
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


class ReportViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Report model viewset"""

    queryset = ReportRepository.get()
    serializer_class = ReportSerializer
    filterset_class = ReportFilter
    lookup_field = "date"

    @action(detail=False, methods=["post"], serializer_class=ProfitWriteSerializer)
    def add_profit(self, request):
        """Add profit report action"""
        return self._add_entry(
            request, entry_model=Profit, serializer_class=ProfitWriteSerializer
        )

    @action(detail=False, methods=["post"], serializer_class=ConsumptionWriteSerializer)
    def add_consumption(self, request):
        """Add consumption report action"""
        return self._add_entry(
            request,
            entry_model=Consumption,
            serializer_class=ConsumptionWriteSerializer,
        )

    def _add_entry(self, request, entry_model, serializer_class):
        """Helper method to add profit or consumption entry"""
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        date = serializer.validated_data["date"]

        try:
            report = ReportRepository.add_entry(date, entry_model, **serializer.validated_data)
            return Response(ReportSerializer(report).data)
        except Exception as e:
            raise APIException(detail=str(e))


class SalaryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Salary model view set"""

    queryset = SalaryRepository.get()
    serializer_class = SalarySerializer
    
