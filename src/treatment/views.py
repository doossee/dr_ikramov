from django.db.models import Prefetch, Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from src.base import MultiSerializerMixin

from src.treatment.models import (
    Appointment,
    Report,
    Profit,
    Consumption
)

from .serializers import (
    AppointmentSerializer,
    AppointmentReadSerializer,
    ReportSerializer,
    ProfitWriteSerializer,
    ConsumptionWriteSerializer
)
from .filters import AppointmentFilter, ReportFilter


class AppointmentViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    
    """Appointment model viewset"""
    
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    serializer_action_classes = {
        "list": AppointmentReadSerializer,
        "retrieve": AppointmentReadSerializer
    }
    filterset_class = AppointmentFilter

    def get_queryset(self):
        qs = super().get_queryset().select_related(
            "doctor", "patient", "service"
        )
        return qs


class ReportViewSet(viewsets.ReadOnlyModelViewSet):

    """Report model viewset"""

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filterset_class = ReportFilter

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related(
            Prefetch(
                'profits', 
                queryset=Profit.objects.all().select_related('appointment')
            ),
            Prefetch(
                'consumptions', 
                queryset=Consumption.objects.all()
            )
        )

        # Annotate total profit and total consumption
        qs = qs.annotate(
            total_profit=Coalesce(Sum('profits__amount'), 0, output_field=DecimalField()),
            total_consumption=Coalesce(Sum('consumptions__amount'), 0, output_field=DecimalField())
        )
        
        # Calculate net profit
        qs = qs.annotate(
            net_profit=ExpressionWrapper(
                F('total_profit') - F('total_consumption'),
                output_field=DecimalField(max_digits=11, decimal_places=2)
            )
        )
        
        return qs

    @action(detail=False, methods=['post'], serializer_class=ProfitWriteSerializer)
    def add_profit(self, request):
        
        """Add profit report action"""
        
        # Передаем данные в сериализатор и валидируем
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Получаем валидированные данные из сериализатор
        date = serializer.validated_data['date']
        appointment = serializer.validated_data['appointment']
        amount = serializer.validated_data['amount']
        
        report, created = Report.objects.update_or_create(date=date)

        profit = Profit.objects.create(
            report=report, appointment=appointment, amount=amount
        )
                
        # Возвращаем созданный объект или его данные в ответе
        return Response(ReportSerializer(report).data)

    @action(detail=False, methods=['post'], serializer_class=ConsumptionWriteSerializer)
    def add_consumption(self, request):
        
        """Add consumption report action"""
        
        # Передаем данные в сериализатор и валидируем
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Получаем валидированные данные из сериализатор
        date = serializer.validated_data['date']
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        amount = serializer.validated_data['amount']
        
        report, created = Report.objects.update_or_create(date=date)

        profit = Consumption.objects.create(
            report=report, title=title, description=description, amount=amount
        )
                
        # Возвращаем созданный объект или его данные в ответе
        return Response(ReportSerializer(report).data)