from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Goal, Workout

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'created_at')
    list_filter = ('user', 'created_at')

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'created_at')
    list_filter = ('user', 'created_at')
