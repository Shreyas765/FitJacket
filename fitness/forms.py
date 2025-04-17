from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Goal, Workout, CoachSuggestion

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='user'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

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
        fields = ['description']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Run 5km'})
        }

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['description']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 30 min cardio'})
        }

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