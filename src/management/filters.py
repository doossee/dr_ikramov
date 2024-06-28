from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Doctor, Patient


class DoctorFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_by_name")
    
    class Meta:
        model = Doctor
        fields = [
            "search",
        ]

    def search_by_name(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(middle_name__icontains=value)
        )


class PatientFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_by_name")
    
    class Meta:
        model = Patient
        fields = [
            "search",
        ]

    def search_by_name(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(middle_name__icontains=value)
        )