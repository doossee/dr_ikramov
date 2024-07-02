from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Doctor, Patient, Service


class DoctorFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_by_names",
        label="Search by first_name, last_name and middle_name",
    )

    class Meta:
        model = Doctor
        fields = []

    def filter_by_names(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(middle_name__icontains=value)
        )


class PatientFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_by_names",
        label="Search by first_name, last_name and middle_name",
    )

    class Meta:
        model = Patient
        fields = []

    def filter_by_names(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(middle_name__icontains=value)
        )


class ServiceFilter(filters.FilterSet):
    search = filters.CharFilter(
        method="filter_by_names", label="Search by name_en, name_ru, name_uz"
    )

    class Meta:
        model = Service
        fields = []

    def filter_by_names(self, queryset, name, value):
        return queryset.filter(
            Q(name_en__icontains=value)
            | Q(name_ru__icontains=value)
            | Q(name_uz__icontains=value)
        )
