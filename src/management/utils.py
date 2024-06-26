from random import randint
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .services.tasks import send_password, send_verify_code


def change_password(user, password, new_password, confirm_password):
    if not user.check_password(password):
        raise ValidationError(_("Password is incorrect!"))

    if new_password != confirm_password:
        raise ValidationError(_("New password and confirmation password are equal!"))

    user.set_password(confirm_password)
    user.save()

def reset_password(user):
    password = randint(100000, 999999)
    user.set_password(str(password))
    user.save()
    send_password.delay(user.phone, password)

def change_avatar(user, avatar):
    user.avatar = avatar
    user.save()

def generate_verify_code(user):
    code = randint(1000, 9999)
    user.is_active = False
    user.verify_code = code
    user.verify_time = timezone.now() + timezone.timedelta(minutes=settings.VERIFY_CODE_MINUTES)
    send_verify_code.delay(user.phone, code)
    user.save()

def verify_user(user, code):
    if user.verify_code == code and user.verify_time >= timezone.now():
        user.is_active = True
        user.save()
        return True
    return False
