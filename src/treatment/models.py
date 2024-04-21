from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

from src.management.models import *

class Record(models.Model):
    
    """Record model"""
    
    doctor = models.ForeignKey(verbose_name=_("Doctor"), to="Doctor", on_delete=models.CASCADE, related_name='record')
    patient = models.ForeignKey(verbose_name=_("Patient"), to="Patient", on_delete=models.CASCADE)

    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(verbose_name=_("End Time"))
    
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Record")
        verbose_name_plural = _("Records")

    def save(self, *args, **kwargs):
        self.end_time = self.start_time + timedelta(hours=1)
        super(Record).save(*args, **kwargs)