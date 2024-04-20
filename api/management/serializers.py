from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from src.management.models import *


class ProfileMeta:
    exclude = ["password", "is_staff", "is_superuser", "verify_time", "verify_code"]
    read_only_fields = ["username", "user_type", "created_at", "updated_at", "last_login", "date_joined"]


class UserSerializer(serializers.ModelSerializer):
    """ """

    class Meta(ProfileMeta):
        model = User


class ChangeAvatarSerializer(serializers.Serializer):
    """ """
    avatar = serializers.ImageField()


class ChangePasswordSerializer(serializers.Serializer):
    """ """
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)


class VerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.IntegerField()


class AdminSerializer(serializers.ModelSerializer):
    """ """

    class Meta(ProfileMeta):
        model = Admin


class MeAdminSerializer(serializers.ModelSerializer):
    class Meta(ProfileMeta):
        model = Admin


class DoctorSerializer(serializers.ModelSerializer):
    """ """

    class Meta(ProfileMeta):
        model = Doctor


class MeDoctorSerializer(serializers.ModelSerializer):
    class Meta(ProfileMeta):
        model = Doctor


class PatientSerializer(serializers.ModelSerializer):
    """ """

    class Meta(ProfileMeta):
        model = Patient


class MePatientSerializer(serializers.ModelSerializer):
    class Meta(ProfileMeta):
        model = Patient