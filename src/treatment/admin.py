from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Appointment, Report


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "doctor",
        "service",
        "price",
        "start_time",
        "end_time",
    )
    search_fields = ("patient__phone", "doctor__phone", "service__name")
    list_filter = ("doctor", "service", "start_time")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass
