from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseAdmin
# Register your models here.
class UserAdmin(BaseAdmin):
    list_display = ('id','first_name','last_name','email', 'phone_number','gender','user_type', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name', 'phone_number','gender','user_type')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_type', 'password1', 'password2'),
        }),
    )
    search_fields = ('id','email')
    ordering = ('email',)
    filter_horizontal = ()
admin.site.register(User, UserAdmin)

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','gender','experience','speciality']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id','doctor','appointment_date','start_time','end_time','appointment_status','booked_by','cancelled_by','is_available','booked_on']
    