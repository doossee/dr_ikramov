from random import randint
from datetime import date

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone

from solo.models import SingletonModel
from imagekit import models as ik_models, processors as ik_processors 

from .choices import *
from .managers import UserManager
from .services.tasks import send_password, send_verify_code


class User(AbstractUser, PermissionsMixin):

    """Main user"""

    avatar = models.ImageField(verbose_name=_("Avatar"), upload_to="avatars/", default=settings.NO_AVATAR)
    phone = models.CharField(verbose_name=_("Phone Number"), max_length=15, unique=True)

    middle_name = models.CharField(verbose_name=_("Middle name"), max_length=50, blank=True)
    birth_date = models.DateField(verbose_name=_("Birth date"), default=date(2000, 1, 1), blank=True)

    verify_code = models.PositiveSmallIntegerField(verbose_name=_("Verify Code"), default=0)
    verify_time = models.DateTimeField(verbose_name=_("Verify Time"), default=timezone.now)

    created_at = models.DateTimeField(verbose_name=_("Created Time"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated Time"), auto_now=True)

    user_type = models.CharField(verbose_name=_("User type"), max_length=10, choices=UserTypeChoices.choices)

    email = None
    groups = None
    user_permissions = None

    objects = UserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def save(self, *args, **kwargs):
        self.user_type = self.get_user_type()
        self.username = self.phone
        super().save(*args, **kwargs)

    def get_user_type(self):
        if isinstance(self, Doctor):
            return "DOCTOR"
        elif isinstance(self, Patient):
            return "PATIENT"
        elif isinstance(self, Admin):
            return "ADMIN"
        else:
            return self.user_type

    def change_password(self, password, new_password, confirm_password):
        """ """
        if not self.check_password(password):
            raise ValidationError(_("Password is incorrect!"))

        if new_password != confirm_password:
            raise ValidationError(_("New password and confirmation password are equal!"))

        self.set_password(confirm_password)
        super().save()

    def reset_password(self):
        password = randint(100000, 999999)
        self.set_password(str(password))
        super().save()
        return send_password.delay(self.phone, password)

    def change_avatar(self, avatar):
        self.avatar = avatar
        super().save()

    def generate_verify_code(self):
        code = randint(1000, 9999)
        self.is_active = False
        self.verify_code = code
        self.verify_time = timezone.now() + timezone.timedelta(minutes=settings.VERIFY_CODE_MINUTES)
        return send_verify_code.delay(self.phone, code)

    def regenerate_verify_code(self):
        result = self.generate_verify_code()
        super().save()
        return result

    def verify(self, code):
        if self.verify_code == code and self.verify_time >= timezone.now():
            self.is_active = True
            super().save()
            return True
        return False


class Admin(User, SingletonModel):

    """Admin user model"""

    singleton_instance_id = 2

    class Meta:
        db_table = "admin"
        verbose_name = _("Admin")


class Doctor(User):

    """Doctor user model"""
    
    # Специализации и отзывы
    # speciality = models.ManyToManyField(verbose_name=_("Specialty"), to="Specialty")
    # reviews = models.ManyToManyField('Review', verbose_name=_("Reviews"))

    # Лицензии, опыт и образование
    licences = models.TextField(verbose_name=_("Licences"))
    experience = models.IntegerField(verbose_name=_("Experience"))
    experiences = models.TextField(verbose_name=_("Experiences"))
    educations = models.TextField(verbose_name=_("Educations"))
    certificates = models.TextField(verbose_name=_("Certificates"))

    # Содержимое и рейтинг
    content = models.TextField(verbose_name=_("Content"))
    rating = models.IntegerField(verbose_name=_("Rating"))

    # Контактная информация
    tg_acc = models.CharField(verbose_name=_("Telegram"), max_length=255)
    inst_acc = models.CharField(verbose_name=_("Instagram"), max_length=255)
    fb_acc = models.CharField(verbose_name=_("Facebook"), max_length=255)
    
    # Публикация и лаборатория
    is_published = models.BooleanField(verbose_name=_("Publish"), default=True)

    # Назначения
    # appointments = models.ManyToManyField('Appointment', verbose_name=_("Appointments"))

    
    class Meta:
        db_table = "doctor"
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")


class Patient(User):

    """Patient user model"""

    class Meta:
        db_table = "patient"
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")

        
class Specialty(models.Model):

    """Specialty model"""
    
    doctor = models.ForeignKey(verbose_name=_("Doctor"), to="Doctor", on_delete=models.CASCADE)

    name = models.CharField(verbose_name=_("Name"), max_length=255, null=True, blank=True)
    name_ru = models.CharField(verbose_name=_("Name (Russian)"), max_length=255)
    name_uz = models.CharField(verbose_name=_("Name (Uzbek)"), max_length=255)

    # Изображение и миниатюра
    image = models.ImageField(verbose_name=_('Image'), upload_to='brands',)
    thumbnail = ik_models.ImageSpecField(
        source='image',
        processors=[ik_processors.ResizeToFill(100, 100)],
        format='WEBP',
        options={'quality': 60}
    )
    
    # Публикация
    is_published = models.BooleanField(verbose_name=_("Publish"), default=False)

    # Дата создания и обновления
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)