from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone_number', 'is_staff')
    list_filter = UserAdmin.list_filter + ('role',)
    search_fields = UserAdmin.search_fields + ('phone_number',)
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('role', 'date_of_birth', 'phone_number')}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'avatar') 
    search_fields = ('user__username', 'user__email', 'address')