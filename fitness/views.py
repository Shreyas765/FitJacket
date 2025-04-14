from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Goal, Workout
from .forms import GoalForm, WorkoutForm, UserRegistrationForm

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
    goals = Goal.objects.filter(user=request.user)
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'fitness/dashboard.html', {
        'goals': goals,
        'workouts': workouts
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
