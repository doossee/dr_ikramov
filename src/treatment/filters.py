from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Appointment, Report


class AppointmentFilter(filters.FilterSet):
    start_time = filters.TimeFilter(field_name="start_time", lookup_expr="gte")
    end_time = filters.TimeFilter(field_name="end_time", lookup_expr="lte")
    date = filters.DateFilter(
        field_name="date", lookup_expr="exact", label="Filter by date"
    )
    patient_search = filters.CharFilter(
        method="filter_patient_by_names",
        label="Search by patient's first_name, last_name, and middle_name",
    )

    class Meta:
        model = Appointment
        fields = [
            "doctor",
            "start_time",
            "end_time",
        ]

    def filter_patient_by_names(self, queryset, name, value):
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
