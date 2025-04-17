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

class Goal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    coach_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s goal: {self.description}"

class Workout(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    coach_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s workout: {self.description}"

class CoachSuggestion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='suggestions')
    coach = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_suggestions')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Suggestion from {self.coach.username} to {self.user.username}"
