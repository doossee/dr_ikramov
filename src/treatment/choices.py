from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    PENDING = "PN", _("Pending")
    FULLY_PAID = "FP", _("Fully paid")
    PARTIALLY_PAID = "PP", _("Partially paid")
    UNPAID = "UP", _("Unpaid")
    CANCELLED = "CD", _("Cancelled")
