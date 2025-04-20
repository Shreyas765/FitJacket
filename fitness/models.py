from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('coach', 'Coach'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    fitness_level = models.CharField(max_length=20, choices=(
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ), default='beginner')
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)

    @property
    def workout_streak(self):
        """Calculate the current workout streak in days."""
        if not self.workout_set.exists():
            return 0
        
        # Get all workout dates
        workout_dates = self.workout_set.values_list('date', flat=True).order_by('-date')
        if not workout_dates:
            return 0
            
        # Start with the most recent workout
        streak = 1
        current_date = workout_dates[0]
        
        # Check consecutive days
        for date in workout_dates[1:]:
            if (current_date - date).days == 1:
                streak += 1
                current_date = date
            else:
                break
                
        return streak

    @property
    def has_weekend_workout(self):
        """Check if user has worked out on both Saturday and Sunday."""
        weekend_workouts = self.workout_set.filter(
            date__week_day__in=[1, 7]  # 1 is Sunday, 7 is Saturday
        ).values_list('date__week_day', flat=True).distinct()
        
        return len(weekend_workouts) == 2

class Goal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    target_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    coach_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s goal: {self.description}"

class Workout(models.Model):
    WORKOUT_TYPES = (
        ('cardio', 'Cardio'),
        ('strength', 'Strength Training'),
        ('flexibility', 'Flexibility'),
        ('hiit', 'HIIT'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    calories_burned = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    coach_feedback = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s {self.workout_type} workout"

class WorkoutPlan(models.Model):
    coach = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_plans')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_plans')
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class WorkoutPlanExercise(models.Model):
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=100)
    sets = models.IntegerField()
    reps = models.IntegerField()
    rest_time = models.IntegerField(help_text="Rest time in seconds")
    notes = models.TextField(blank=True)

class Challenge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    participants = models.ManyToManyField(CustomUser, through='ChallengeParticipation')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_challenges')

class ChallengeParticipation(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    badge_image = models.ImageField(upload_to='achievement_badges/')
    criteria = models.TextField(help_text="Description of how to earn this achievement")

class UserAchievement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

class AICoachingSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ProgressStats(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    body_fat_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    muscle_mass = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

class Location(models.Model):
    LOCATION_TYPES = (
        ('gym', 'Gym'),
        ('park', 'Park'),
    )
    name = models.CharField(max_length=255)
    location_type = models.CharField(max_length=10, choices=LOCATION_TYPES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

class CoachSuggestion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='suggestions')
    coach = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_suggestions')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Suggestion from {self.coach.username} to {self.user.username}"
