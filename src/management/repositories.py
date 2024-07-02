# repositories.py
from .models import User, Doctor, Patient, Specialty, Service, InitialRecord, Rating

class UserRepository:
    @staticmethod
    def get():
        return User.objects.all()

    @staticmethod
    def get_by_phone(phone):
        return User.objects.get(phone=phone)

    @staticmethod
    def signup(**data):
        return User.objects.create(**data)

class DoctorRepository:
    @staticmethod
    def get():
        return Doctor.objects.all().prefetch_related("specialties")
    
    @staticmethod
    def get_published():
        return Doctor.objects.filter(is_published=True).prefetch_related("specialties")

class PatientRepository:
    @staticmethod
    def get():
        return Patient.objects.all()

class SpecialtyRepository:
    @staticmethod
    def get():
        return Specialty.objects.all()

class ServiceRepository:
    @staticmethod
    def get():
        return Service.objects.all()

class InitialRecordRepository:
    @staticmethod
    def get():
        return InitialRecord.objects.all()

class RatingRepository:
    @staticmethod
    def get():
        return Rating.objects.all()
