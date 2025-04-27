from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import (
    CustomUser, Goal, Workout, WorkoutPlan, WorkoutPlanExercise,
    Challenge, ProgressStats, Location, AICoachingSession, CoachSuggestion, Achievement
)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='user'
    )
    fitness_level = forms.ChoiceField(
        choices=CustomUser._meta.get_field('fitness_level').choices,
        required=True
    )
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type', 'fitness_level', 'bio', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['description', 'target_date']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Run 5km'}),
            'target_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['workout_type', 'description', 'duration', 'calories_burned', 'location']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 30 min cardio'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in minutes'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estimated calories burned'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where did you workout?'})
        }

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class WorkoutPlanExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlanExercise
        fields = ['name', 'sets', 'reps', 'rest_time', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sets': forms.NumberInput(attrs={'class': 'form-control'}),
            'reps': forms.NumberInput(attrs={'class': 'form-control'}),
            'rest_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['challenged', 'workout_type', 'duration', 'description', 'deadline', 'calories_target', 'location', 'notes']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, user, *args, **kwargs):
        super(ChallengeForm, self).__init__(*args, **kwargs)
        # Only show friends in the challenged field
        self.fields['challenged'].queryset = user.friends.all()
        self.fields['challenged'].label = "Challenge Friend"
        self.fields['duration'].label = "Duration (minutes)"
        self.fields['calories_target'].label = "Target Calories (optional)"
        self.fields['location'].label = "Location (optional)"
        self.fields['notes'].label = "Additional Notes (optional)"

class ProgressStatsForm(forms.ModelForm):
    class Meta:
        model = ProgressStats
        fields = ['date', 'weight', 'body_fat_percentage', 'muscle_mass', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Weight in lbs'}),
            'body_fat_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Body Fat %'}),
            'muscle_mass': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Muscle Mass in lbs'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }
        labels = {
            'weight': 'Weight (lbs)',
            'muscle_mass': 'Muscle Mass (lbs)',
            'body_fat_percentage': 'Body Fat Percentage (%)'
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'location_type', 'latitude', 'longitude', 'address', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'})
        }

class AICoachingForm(forms.ModelForm):
    class Meta:
        model = AICoachingSession
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ask your fitness question here...'
            })
        }

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

class CoachFeedbackForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['coach_feedback']
        widgets = {
            'coach_feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class CoachSuggestionForm(forms.ModelForm):
    class Meta:
        model = CoachSuggestion
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your suggestion here...'})
        }

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['name', 'description', 'badge_image', 'criteria']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'criteria': forms.Textarea(attrs={'rows': 3}),
        } 