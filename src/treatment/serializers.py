from rest_framework import serializers

from src.management.models import Doctor, Patient, Service
from .models import Appointment, Report, Profit, Consumption, Salary


# <-----Base Serializers----> #

class DoctorSerializer(serializers.ModelSerializer):
    """Doctor model serializer"""

    class Meta:
        model = Doctor
        fields = ["id", "first_name", "last_name", "middle_name", "phone"]


class PatientSerializer(serializers.ModelSerializer):
    """Patient model serializer"""

    class Meta:
        model = Patient
        fields = ["id", "first_name", "last_name", "middle_name", "phone"]


class ServiceSerializer(serializers.ModelSerializer):
    """Service model serializer"""

    class Meta:
        model = Service
        fields = [
            "id",
            "name_en",
            "name_ru",
            "name_uz",
            "category",
            "price_start",
            "price_end",
        ]


class ProfitReadSerializer(serializers.ModelSerializer):
    """Profit model serializer"""

    class Meta:
        model = Profit
        fields = "__all__"


# <-----Appointment Serializers----> #

class AppointmentSerializer(serializers.ModelSerializer):
    """Appointment model serializer"""

    class Meta:
        model = Appointment
        fields = "__all__"


class AppointmentReadSerializer(serializers.ModelSerializer):
    """Appointment model serializer"""

    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    profits = ProfitReadSerializer(many=True, read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"


class AppointmentNestedSerializer(serializers.ModelSerializer):
    """Appointment model serializer"""

    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"


# <-----Profit Serializers----> #

class ProfitSerializer(serializers.ModelSerializer):
    """Profit model serializer"""

    appointment = AppointmentNestedSerializer(read_only=True)

    class Meta:
        model = Profit
        fields = "__all__"


class ProfitWriteSerializer(serializers.ModelSerializer):
    """Profit model serializer"""

    date = serializers.DateField()

    class Meta:
        model = Profit
        exclude = ["report"]


class ProfitAddSerializer(serializers.ModelSerializer):
    """Profit add model serializer"""

    date = serializers.DateField()

    class Meta:
        model = Profit
        exclude = ["report", "appointment"]


# <-----Consumption Serializers----> #

class ConsumptionSerializer(serializers.ModelSerializer):
    """Consumption model serializer"""

    doctor = DoctorSerializer(source="salary.doctor", read_only=True)

    class Meta:
        model = Consumption
        fields = (
            "id",
            "title",
            "description",
            "amount",
            "created_at",
            "updated_at",
            "report",
            "doctor",
        )


class ConsumptionWriteSerializer(serializers.ModelSerializer):
    """Consumption model serializer"""

    date = serializers.DateField()

    class Meta:
        model = Consumption
        exclude = ["report"]


# <-----Salary Serializers----> #

class SalarySerializer(serializers.ModelSerializer):
    """Appointment model serializer"""

    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Salary
        fields = "__all__"


class SalaryWriteSerializer(serializers.ModelSerializer):
    """Salary write model serializer"""

    date = serializers.DateField()

    class Meta:
        model = Salary
        exclude = ["report"]


# <-----Report Serializers----> #

class ReportSerializer(serializers.ModelSerializer):
    """Report model serializer"""

    profits = ProfitSerializer(many=True, read_only=True)
    consumptions = ConsumptionSerializer(many=True, read_only=True)
    total_profit = serializers.DecimalField(
        max_digits=11, decimal_places=2, read_only=True
    )
    total_consumption = serializers.DecimalField(
        max_digits=11, decimal_places=2, read_only=True
    )
    net_profit = serializers.DecimalField(
        max_digits=11, decimal_places=2, read_only=True
    )

    class Meta:
        model = Report
        fields = [
            "id",
            "date",
            "total_profit",
            "total_consumption",
            "net_profit",
            "profits",
            "consumptions",
            "created_at",
            "updated_at",
        ]






