from django_filters import rest_framework as filters

from .models import Appointment

class AppointmentFilter(filters.FilterSet):
    start_time = filters.DateTimeFilter(field_name="start_time", lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name="end_time", lookup_expr='lte')

    class Meta:
        model = Appointment
        fields = ['doctor', 'start_time', 'end_time' ]