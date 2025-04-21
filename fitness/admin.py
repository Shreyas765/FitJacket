from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Goal, Workout, WorkoutPlan, WorkoutPlanExercise,
    Challenge, ChallengeParticipation, Achievement, UserAchievement,
    AICoachingSession, ProgressStats, Location, CoachSuggestion
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'fitness_level', 'is_staff')
    list_filter = ('user_type', 'fitness_level', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'user_type', 'fitness_level', 'bio', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'target_date', 'is_completed', 'created_at')
    list_filter = ('is_completed', 'created_at')
    search_fields = ('user__username', 'description')

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout_type', 'duration', 'calories_burned', 'created_at')
    list_filter = ('workout_type', 'created_at')
    search_fields = ('user__username', 'description')

class WorkoutPlanExerciseInline(admin.TabularInline):
    model = WorkoutPlanExercise
    extra = 1

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach', 'user', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'coach__username', 'user__username')
    inlines = [WorkoutPlanExerciseInline]

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['challenger', 'challenged', 'workout_type', 'duration', 'deadline', 'status']
    list_filter = ['status', 'workout_type', 'deadline']
    search_fields = ['challenger__username', 'challenged__username', 'description']
    readonly_fields = ['created_at', 'completed_at']
    fieldsets = (
        ('Challenge Details', {
            'fields': ('challenger', 'challenged', 'workout_type', 'duration', 'deadline', 'status')
        }),
        ('Additional Information', {
            'fields': ('description', 'calories_target', 'location', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ChallengeParticipation)
class ChallengeParticipationAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'user', 'points', 'joined_at')
    list_filter = ('joined_at',)
    search_fields = ('challenge__name', 'user__username')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'earned_at')
    list_filter = ('earned_at',)
    search_fields = ('user__username', 'achievement__name')

@admin.register(AICoachingSession)
class AICoachingSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'question')

@admin.register(ProgressStats)
class ProgressStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'weight', 'body_fat_percentage', 'muscle_mass')
    list_filter = ('date',)
    search_fields = ('user__username',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_type', 'address', 'rating')
    list_filter = ('location_type', 'rating')
    search_fields = ('name', 'address')

@admin.register(CoachSuggestion)
class CoachSuggestionAdmin(admin.ModelAdmin):
    list_display = ('coach', 'user', 'created_at', 'is_read')
    list_filter = ('created_at', 'is_read')
    search_fields = ('coach__username', 'user__username', 'content')
