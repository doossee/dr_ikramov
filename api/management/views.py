from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *
from src.management.models import *


class UserViewSet(viewsets.ModelViewSet):
    """ """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        match self.action:
            case "signup":
                self.permission_classes = []
            case "verify":
                self.permission_classes = []
            case "regenerate_verify_code":
                self.permission_classes = []
            case "reset_password":
                self.permission_classes = []
            case _:
                self.permission_classes = super().permission_classes

        return super(UserViewSet, self).get_permissions()

    def get_serializer_class(self):
        match self.action:
            case "me":
                match self.request.user.user_type:
                    case "ADMIN":
                        return MeAdminSerializer
                    case "DOCTOR":
                        return MeDoctorSerializer
                    case "PATIENT":
                        return MePatientSerializer
                    case _:
                        return super().get_serializer_class()

            case "change_avatar":
                return ChangeAvatarSerializer
            case "change_password":
                return ChangePasswordSerializer
            case "reset_password":
                return PhoneSerializer
            case "regenerate_verify_code":
                return PhoneSerializer
            case "verify":
                return VerifySerializer
            case _:
                return super().get_serializer_class()

    def get_object(self):
        match self.action:
            case "me":
                return self.request.user
            case "change_avatar":
                return self.request.user
            case "change_password":
                return self.request.user
            case _:
                return super().get_object()

    def get_queryset(self):
        match self.action:
            case "monitoring":
                return self.request.user.monitoring()
            case _:
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
            return Response(serializer.data, status=status.HTTP_200_OK)
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

    @action(url_path="reset-password", detail=False, methods=["POST"])
    def reset_password(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                instance = self.queryset.get(phone=serializer.validated_data.get("phone"))
                if instance.reset_password():
                    return Response(
                        {"success": _("The password has been reset and sent to your phone number!")},
                        status=status.HTTP_200_OK
                    )
                return Response({"message": _("Error sending the message!")}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"message": _("The user with this phone has not been found!")}, status.HTTP_404_NOT_FOUND)

    @action(url_path="signup", detail=False, methods=["POST"])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            User.objects.signup(**data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(url_path="regenerate-verify-code", detail=False, methods=["POST"])
    def regenerate_verify_code(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                instance = self.queryset.get(phone=serializer.validated_data.get("phone"))
                if instance.regenerate_verify_code():
                    return Response({"success": _("The verification code sent!")}, status=status.HTTP_200_OK)
                return Response({"message": _("Error sending the message!")}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"message": _("The user with this phone has not been found!")}, status.HTTP_404_NOT_FOUND)

    @action(url_path="verify", detail=False, methods=["POST"])
    def verify(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                instance = self.queryset.get(phone=data.get("phone"))
                if instance.verify(data.get("code")):
                    return Response({"success": _("The user is verified!")}, status=status.HTTP_200_OK)
                return Response(
                    {"message": _("Verify error timeout or invalid code!")},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({"message": _("The user with this phone has not been found!")}, status.HTTP_404_NOT_FOUND)


class AdminViewSet(viewsets.ModelViewSet):
    """ """

    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().first()
        if queryset:
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class DoctorViewSet(viewsets.ModelViewSet):
    """ """

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    
class PatientViewSet(viewsets.ModelViewSet):
    """ """

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    search_fields = [
        'last_name', 
        'first_name', 
        'middle_name',
        'pinfl', 
        'phone', 
        'mahalla', 
        'street',    
    ]
    filterset_fields = [
        'birth_date', 
        'social_group', 
        'gender', 
        'district'
    ]


        
    


