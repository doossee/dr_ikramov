from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from src.base import MultiSerializerMixin
from .models import User, Admin
from .repositories import (
    UserRepository,
    DoctorRepository,
    PatientRepository,
    SpecialtyRepository,
    ServiceRepository,
    InitialRecordRepository,
    RatingRepository,
)
from .serializers import (
    UserSerializer,
    ChangeAvatarSerializer,
    ChangePasswordSerializer,
    PhoneSerializer,
    VerifySerializer,
    AdminSerializer,
    MeAdminSerializer,
    DoctorSerializer,
    MeDoctorSerializer,
    DoctorGetSerializer,
    PatientSerializer,
    MePatientSerializer,
    SpecialtySerializer,
    ServiceSerializer,
    InitialRecordSerializer,
    RatingSerializer,
)
from .filters import DoctorFilter, PatientFilter, ServiceFilter


class UserViewSet(viewsets.ModelViewSet):
    """User model viewset"""

    queryset = UserRepository.get()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        action = self.action

        if action in ["signup", "verify", "regenerate_verify_code", "reset_password"]:
            self.permission_classes = []
        else:
            self.permission_classes = super().permission_classes

        return super(UserViewSet, self).get_permissions()

    def get_serializer_class(self):
        action = self.action
        user_type = (
            self.request.user.user_type
            if hasattr(self.request.user, "user_type")
            else None
        )

        if action == "me":
            if user_type == "ADMIN":
                return MeAdminSerializer
            elif user_type == "DOCTOR":
                return MeDoctorSerializer
            elif user_type == "PATIENT":
                return MePatientSerializer

        serializer_map = {
            "change_avatar": ChangeAvatarSerializer,
            "change_password": ChangePasswordSerializer,
            "reset_password": PhoneSerializer,
            "regenerate_verify_code": PhoneSerializer,
            "verify": VerifySerializer,
        }

        return serializer_map.get(action, super().get_serializer_class())

    def get_object(self):
        if self.action in ["me", "change_avatar", "change_password"]:
            return self.request.user

        return super().get_object()

    def get_queryset(self):
        if self.action == "monitoring":
            return self.request.user.monitoring()

        return super().get_queryset()

    @action(url_path="me", detail=False, methods=["GET", "PUT", "PATCH"])
    def me(self, request, *args, **kwargs):
        match request.method:
            case "GET":
                return super().retrieve(request, *args, **kwargs)
            case "PUT":
                return super().update(request, *args, **kwargs)
            case "PATCH":
                return super().partial_update(request, *args, **kwargs)

    @action(url_path="change-avatar", detail=False, methods=["POST"])
    def change_avatar(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            instance.change_avatar(**data)

            # Build the full URL for the avatar
            avatar_url = request.build_absolute_uri(instance.avatar.url)
            
            return Response({"avatar": avatar_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(url_path="change-password", detail=False, methods=["POST"])
    def change_password(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            instance.change_password(**data)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminViewSet(viewsets.ModelViewSet):
    """Admin model viewset"""

    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().first()
        if queryset:
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class DoctorViewSet(MultiSerializerMixin, viewsets.ModelViewSet):
    """Doctor model viewset"""

    serializer_class = DoctorSerializer
    serializer_action_classes = {
        "list": DoctorGetSerializer,
        "retrieve": DoctorGetSerializer,
    }
    filterset_class = DoctorFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Return queryset based on user's authentication status."""
        if self.request.user.is_authenticated:
            return DoctorRepository.get()
        else:
            return DoctorRepository.get_published()

    def get_permissions(self):
        """Set permissions based on user's authentication status."""
        if self.request.user.is_authenticated:
            # Authenticated users can perform any action
            return [permissions.IsAuthenticated()]
        else:
            # Unauthenticated users can only read data (list and retrieve)
            if self.action in ["list", "retrieve"]:
                return [permissions.AllowAny()]
            else:
                return [permissions.IsAuthenticated()]


class PatientViewSet(viewsets.ModelViewSet):
    """Patient model viewset"""

    queryset = PatientRepository.get()
    serializer_class = PatientSerializer
    filterset_class = PatientFilter
    permission_classes = [permissions.IsAuthenticated]


class SpecialtyViewSet(viewsets.ModelViewSet):
    """Specialty model viewset"""

    queryset = SpecialtyRepository.get()
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ServiceViewSet(viewsets.ModelViewSet):
    """Service model viewset"""

    queryset = ServiceRepository.get()
    serializer_class = ServiceSerializer
    lookup_field = "slug"
    filterset_class = ServiceFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class InitialRecordViewSet(viewsets.ModelViewSet):
    """Initial record model viewset"""

    queryset = InitialRecordRepository.get()
    serializer_class = InitialRecordSerializer


class RatingViewSet(viewsets.ModelViewSet):
    """Rating model viewset"""

    queryset = RatingRepository.get()
    serializer_class = RatingSerializer
