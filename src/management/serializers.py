from rest_framework import serializers

from src.management.models import (
    User,
    Admin,
    Doctor,
    Patient,
    Specialty,
    Service,
    InitialRecord,
    Rating,
)


class ProfileMeta:
    exclude = [
        "password",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    read_only_fields = [
        "username",
        "user_type",
        "created_at",
        "updated_at",
        "last_login",
        "date_joined",
    ]


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta(ProfileMeta):
        model = User


class ChangeAvatarSerializer(serializers.Serializer):
    """Change avatar serializer"""

    avatar = serializers.ImageField()


class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer"""

    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)


class PhoneSerializer(serializers.Serializer):
    """Phone serializer"""

    phone = serializers.CharField(required=True)


class VerifySerializer(serializers.Serializer):
    """Verify serializer"""

    phone = serializers.CharField()
    code = serializers.IntegerField()


class AdminSerializer(serializers.ModelSerializer):
    """Admin model serializer"""

    class Meta(ProfileMeta):
        model = Admin


class MeAdminSerializer(serializers.ModelSerializer):
    """ME admin model serializer"""

    class Meta(ProfileMeta):
        model = Admin


class DoctorSerializer(serializers.ModelSerializer):
    """Doctor model serializer"""

    class Meta(ProfileMeta):
        model = Doctor


class MeDoctorSerializer(serializers.ModelSerializer):
    """ME doctor model serializer"""

    class Meta(ProfileMeta):
        model = Doctor


class PatientSerializer(serializers.ModelSerializer):
    """Patient model serializer"""

    class Meta(ProfileMeta):
        model = Patient


class MePatientSerializer(serializers.ModelSerializer):
    """ME patient model serializer"""

    class Meta(ProfileMeta):
        model = Patient


class SpecialtySerializer(serializers.ModelSerializer):
    """Specialty model serializer"""

    class Meta:
        model = Specialty
        fields = "__all__"


class DoctorGetSerializer(serializers.ModelSerializer):
    """Doctor model serializer"""

    specialties = SpecialtySerializer(many=True, read_only=True)

    class Meta(ProfileMeta):
        model = Doctor


class ServiceSerializer(serializers.ModelSerializer):
    """Service model serializer"""

    class Meta:
        model = Service
        fields = "__all__"


class InitialRecordSerializer(serializers.ModelSerializer):
    """Initial record model serializer"""

    class Meta:
        model = InitialRecord
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    """Rating model serializer"""

    class Meta:
        model = Rating
        fields = "__all__"
