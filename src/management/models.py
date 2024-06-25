from random import randint
from datetime import date

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

from solo.models import SingletonModel
from imagekit import models as ik_models, processors as ik_processors

from .choices import *  # noqa: F403
from .managers import UserManager
from .services.tasks import send_password, send_verify_code


class User(AbstractUser):
    """Main user"""

    avatar = models.ImageField(
        verbose_name=_("Avatar"), upload_to="avatars/", default=settings.NO_AVATAR
    )
    phone = models.CharField(verbose_name=_("Phone Number"), max_length=15, unique=True)

    middle_name = models.CharField(
        verbose_name=_("Middle name"), max_length=50, blank=True
    )
    birth_date = models.DateField(
        verbose_name=_("Birth date"), default=date(2000, 1, 1), blank=True
    )

    verify_code = models.PositiveSmallIntegerField(
        verbose_name=_("Verify Code"), default=0
    )
    verify_time = models.DateTimeField(
        verbose_name=_("Verify Time"), default=timezone.now
    )

    created_at = models.DateTimeField(verbose_name=_("Created Time"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated Time"), auto_now=True)

    user_type = models.CharField(
        verbose_name=_("User type"), max_length=10, choices=UserTypeChoices.choices
    )

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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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
            raise ValidationError(
                _("New password and confirmation password are equal!")
            )

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
        self.verify_time = timezone.now() + timezone.timedelta(
            minutes=settings.VERIFY_CODE_MINUTES
        )
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

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Doctor(User):
    """Doctor user model"""

    specialties = models.ManyToManyField(
        verbose_name=_("Specialty"), to="Specialty", blank=True, related_name="doctors"
    )

    experience = models.IntegerField(
        verbose_name=_("Experience"), null=True, blank=True
    )
    experiences = models.TextField(verbose_name=_("Experiences"), blank=True)

    licences = models.TextField(verbose_name=_("Licences"), blank=True)
    educations = models.TextField(verbose_name=_("Educations"), blank=True)
    certificates = models.TextField(verbose_name=_("Certificates"), blank=True)

    content = models.TextField(verbose_name=_("Content"), blank=True)
    rating = models.DecimalField(
        verbose_name=_("Rating"), max_digits=3, decimal_places=2, default=0
    )

    balance = models.DecimalField(
        verbose_name=_("Balance"), max_digits=11, decimal_places=2
    )

    is_published = models.BooleanField(verbose_name=_("Publish"), default=True)

    class Meta:
        db_table = "doctor"
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Patient(User):
    """Patient user model"""

    class Meta:
        db_table = "patient"
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")


class Specialty(models.Model):
    """Specialty model"""

    name_en = models.CharField(verbose_name=_("Name"), max_length=150)
    name_ru = models.CharField(verbose_name=_("Name (Russian)"), max_length=150)
    name_uz = models.CharField(verbose_name=_("Name (Uzbek)"), max_length=150)

    # Image and thumbnail
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to="specialties",
    )
    thumbnail = ik_models.ImageSpecField(
        source="image",
        processors=[ik_processors.ResizeToFill(100, 100)],
        format="WEBP",
        options={"quality": 60},
    )

    is_published = models.BooleanField(verbose_name=_("Publish"), default=False)

    # Create and update dates
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Specialty")
        verbose_name_plural = _("Specialties")

    def __str__(self) -> str:
        return self.name_en


class Service(models.Model):
    """Service model"""

    name_en = models.CharField(verbose_name=_("Name"), max_length=150)
    name_ru = models.CharField(verbose_name=_("Name (Russian)"), max_length=150)
    name_uz = models.CharField(verbose_name=_("Name (Uzbek)"), max_length=150)

    category = models.CharField(
        verbose_name=_("Category"), max_length=30, choices=CategoryChoices.choices
    )

    price_start = models.DecimalField(
        verbose_name=_("Service price start"), max_digits=11, decimal_places=2
    )
    price_end = models.DecimalField(
        verbose_name=_("Service price end"), max_digits=11, decimal_places=2
    )

    kpi_percent = models.PositiveIntegerField(
        verbose_name=_("KPI percent"),
        validators=[MaxValueValidator(100)],
    )

    slug = models.SlugField(
        verbose_name=_("Slug"), max_length=255, null=True, blank=True
    )

    image = models.ImageField(
        verbose_name=_("Image"), upload_to="services", null=True, blank=True
    )
    thumbnail = ik_models.ImageSpecField(
        source="image",
        processors=[ik_processors.ResizeToFill(100, 100)],
        format="WEBP",
        options={"quality": 60},
    )

    description_en = models.TextField(
        verbose_name=_("Description"), null=True, blank=True
    )
    description_ru = models.TextField(
        verbose_name=_("Description (Russian)"), null=True, blank=True
    )
    description_uz = models.TextField(
        verbose_name=_("Description (Uzbek)"), null=True, blank=True
    )

    content = models.TextField(verbose_name=_("Content"), blank=True)
    is_published = models.BooleanField(verbose_name=_("Publish"), default=True)

    # <-----Create and update dates----->

    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self) -> str:
        return self.name_en

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)


class InitialRecord(models.Model):
    """Initial record model"""

    first_name = models.CharField(verbose_name=_("First Name"), max_length=150)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=150)
    phone = models.CharField(verbose_name=_("Phone Number"), max_length=15)
    comment = models.TextField(verbose_name=_("Comment"), blank=True)

    # <-----Create date-----> #

    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Initial Record")
        verbose_name_plural = _("Initial Records")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Rating(models.Model):
    """Rating model"""

    first_name = models.CharField(verbose_name=_("First Name"), max_length=150)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=150)

    doctor = models.ForeignKey(
        verbose_name=_("Rated doctor"),
        to=Doctor,
        related_name="ratings",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    rate = models.PositiveSmallIntegerField(_("Rate"), choices=RateChoices.choices)
    review = models.TextField(_("Review text"))

    # <-----Create and update dates-----> #

    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
