from django.db import models
from django.utils.translation import gettext_lazy as _


class UserTypeChoices(models.TextChoices):
    """User type choices"""

    # Администратор
    ADMIN = "admin", _("Admin")
    # Доктор
    DOCTOR = "doctor", _("Doctor")
    # Пациент
    PATIENT = "patient", _("Patient")


class GenderChoices(models.TextChoices):
    """Gender choices"""

    # Мужчина
    MALE = "male", _("Male")
    # Женщина
    FEMALE = "female", _("Female")


class CategoryChoices(models.TextChoices):
    """Category choices"""

    # Терапия
    THERAPY = "therapy", _("Therapy")
    # Хирургия
    SURGERY = "surgery", _("Surgery")
    # Ортодонтия
    ORTHODONTICS = "orthodontics", _("Orthodontics")
    # Ортопедия
    ORTHOPEDICS = "orthopedics", _("Orthopedics")


class RateChoices(models.IntegerChoices):
    """Rate choices"""

    # ОК
    OK = 1, _("Ok")
    # Хорошо
    GOOD = 2, _("Good")
    # Отлично
    FINE = 3, _("Fine")
    # Удивительно
    AMAZING = 4, _("Amazing")
    # Невероятно
    INCREDIBLE = 5, _("Incredible")
