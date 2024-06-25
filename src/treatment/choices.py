from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    PENDING = "PN", _("Pending")
    PAID = "PD", _("Paid")
    UNPAID = "UP", _("Unpaid")
    CANCELLED = "CD", _("Cancelled")
