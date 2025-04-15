from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView
from .models import CustomUser, Goal, Workout, CoachSuggestion
from .forms import GoalForm, WorkoutForm, UserRegistrationForm, CoachFeedbackForm, CoachSuggestionForm

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'fitness/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'fitness/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'fitness/login.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.user_type == 'coach':
        return redirect('coach_dashboard')
    
    goals = Goal.objects.filter(user=request.user)
    workouts = Workout.objects.filter(user=request.user)
    suggestions = CoachSuggestion.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'fitness/dashboard.html', {
        'goals': goals,
        'workouts': workouts,
        'suggestions': suggestions
    })

@login_required
def coach_dashboard(request):
    if request.user.user_type != 'coach':
        return redirect('dashboard')
    
    users = CustomUser.objects.filter(user_type='user')
    return render(request, 'fitness/coach_dashboard.html', {
        'users': users
    })

@login_required
def user_profile(request, user_id):
    if request.user.user_type != 'coach':
        return redirect('dashboard')
    
    user = get_object_or_404(CustomUser, id=user_id, user_type='user')
    goals = Goal.objects.filter(user=user)
    workouts = Workout.objects.filter(user=user)
    
    if request.method == 'POST':
        form = CoachSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.coach = request.user
            suggestion.user = user
            suggestion.save()
            return redirect('user_profile', user_id=user_id)
    else:
        form = CoachSuggestionForm()
    
    return render(request, 'fitness/user_profile.html', {
        'profile_user': user,
        'goals': goals,
        'workouts': workouts,
        'form': form
    })

@login_required
def provide_feedback(request, model_type, item_id):
    if request.user.user_type != 'coach':
        return redirect('dashboard')
    
    if model_type == 'goal':
        item = get_object_or_404(Goal, id=item_id)
    else:
        item = get_object_or_404(Workout, id=item_id)
    
    if request.method == 'POST':
        form = CoachFeedbackForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id=item.user.id)
    else:
        form = CoachFeedbackForm(instance=item)
    
    return render(request, 'fitness/provide_feedback.html', {
        'form': form,
        'item': item,
        'model_type': model_type
    })

@login_required
def set_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('dashboard')
    else:
        form = GoalForm()
    return render(request, 'fitness/set_goal.html', {'form': form})

@login_required
def log_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('dashboard')
    else:
        form = WorkoutForm()
    return render(request, 'fitness/log_workout.html', {'form': form})

@login_required
def mark_suggestion_read(request, suggestion_id):
    suggestion = get_object_or_404(CoachSuggestion, id=suggestion_id, user=request.user)
    suggestion.is_read = True
    suggestion.save()
    return redirect('dashboard')
