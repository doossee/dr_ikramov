from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import User, Admin, Doctor, Patient, Specialty, Service, InitialRecord, Rating

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('avatar', 'middle_name', 'birth_date')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )
    list_display = ('phone', 'is_staff', 'is_active')
    search_fields = ('phone',)
    ordering = ('phone',)

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone')
    search_fields = ('phone',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'rating', 'is_published')
    search_fields = ('phone', 'specialties__name_en')
    list_filter = ('is_published', 'specialties')
    filter_horizontal = ('specialties',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone')
    search_fields = ('phone',)

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_en', 'is_published')
    search_fields = ('name_en',)
    list_filter = ('is_published',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_en', 'category', 'price_start', 'price_end', 'is_published')
    search_fields = ('name_en', 'category')
    list_filter = ('is_published', 'category')

@admin.register(InitialRecord)
class InitialRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'doctor', 'rate', 'created_at')
    search_fields = ('first_name', 'last_name', 'doctor__phone')
    list_filter = ('rate', 'doctor')
