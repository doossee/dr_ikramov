from django.db import models
from django.utils.translation import gettext_lazy as _
 

class UserTypeChoices(models.TextChoices):
    
    # Администратор
    ADMIN = 'admin', _('Admin')
    # Доктор
    DOCTOR = 'doctor', _('Doctor')
    # Пациент
    PATIENT = 'patient', _('Patient')


class GenderChoices(models.TextChoices):

    # Мужчина
    MALE = 'male', _('Male')
    # Женщина
    FEMALE = 'female', _('Female')


class EthnicityChoices(models.TextChoices):

    # Азиаты
    ASIAN = 'asian', _('Asian')
    # Европейцы
    EUROPEAN = 'european', _('European')
    # Прочие
    OTHER = 'other', _('Other')


class SocialGroupChoices(models.TextChoices):

    # Дети, до 16 лет
    CHILD = 'child', _('Child')
    # Трудоспособные, мужчины 16-59 лет, женщины 16-54 лет
    ADULTS = 'adult', _('Adult')
    # Пенсионеры, мужчины >59 лет, женщины >54 лет
    PENSIONERS = 'pensioner', _('Pensioner')
    # Прочие, любого возраста
    DISABLED = 'disabled', _('Disabled')


class ProfessionChoices(models.TextChoices):

    # Дехкане, работники, занятые в сельском хозяйстве без в/о
    FARMER = 'farmer', _('Farmer') 
    # Рабочие, любые профессии или род деятельности без в/о
    WORKER = 'worker', _('Worker') 
    # Служащие, любые профессии или род деятельности с в/о
    EMPLOYEE = 'employee', _('Employee') 
    # Лица свободных профессий
    FREELANCER = 'freelancer', _('Freelancer') 
    # Священнослужители
    PRIEST = 'priest', _('Priest') 
    # Прочие
    OTHER = 'other', _('Other')
