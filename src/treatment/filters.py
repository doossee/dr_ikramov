from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Appointment, Report


class AppointmentFilter(filters.FilterSet):
    start_time = filters.DateTimeFilter(field_name="start_time", lookup_expr="gte")
    end_time = filters.DateTimeFilter(field_name="end_time", lookup_expr="lte")
    patient_search = filters.CharFilter(method="filter_by_patient_name")

    class Meta:
        model = Appointment
        fields = [
            "doctor",
            "start_time",
            "end_time",
            "patient_search",
        ]

    def filter_by_patient_name(self, queryset, name, value):
        return queryset.filter(
            Q(patient__first_name__icontains=value)
            | Q(patient__last_name__icontains=value)
            | Q(patient__middle_name__icontains=value)
        )


class ReportFilter(filters.FilterSet):
    class Meta:
        model = Report
        fields = [
            "date",
        ]
