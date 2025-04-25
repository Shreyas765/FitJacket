from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.db.models import Sum, Count, Avg
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
import json
from .models import (
    CustomUser, Goal, Workout, WorkoutPlan, WorkoutPlanExercise,
    Challenge, ChallengeParticipation, Achievement, UserAchievement,
    AICoachingSession, ProgressStats, Location, CoachSuggestion
)
from .forms import (
    UserRegistrationForm, GoalForm, WorkoutForm, WorkoutPlanForm,
    WorkoutPlanExerciseForm, ChallengeForm, ProgressStatsForm,
    LocationForm, AICoachingForm, CustomPasswordResetForm,
    CoachFeedbackForm, CoachSuggestionForm
)
from .utils import get_nearby_locations
from django.contrib import messages

# Make workout assistant optional
try:
    from workout_assistant import WorkoutData, get_workout_tip
    WORKOUT_ASSISTANT_AVAILABLE = True
except ImportError:
    WORKOUT_ASSISTANT_AVAILABLE = False
    def get_workout_tip(workout_data):
        return "Keep up the great work! Remember to stay hydrated and maintain proper form during your workouts."

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'fitness/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
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
    challenges = ChallengeParticipation.objects.filter(user=request.user)
    achievements = UserAchievement.objects.filter(user=request.user)
    progress_stats = ProgressStats.objects.filter(user=request.user).order_by('-date')[:5]
    
    # Calculate statistics
    total_workouts = workouts.count()
    total_calories = workouts.aggregate(total=Sum('calories_burned'))['total'] or 0
    avg_duration = workouts.aggregate(avg=Avg('duration'))['avg'] or 0

    # Get workout tip
    if WORKOUT_ASSISTANT_AVAILABLE:
        # Get last 3 workouts for the tip
        last_workouts = workouts.order_by('-created_at')[:3]
        workout_data = WorkoutData(
            goals=", ".join([goal.description for goal in goals]),
            progress=progress_stats.first().description if progress_stats else "",
            last_workouts=[{
                "date": workout.created_at.strftime("%Y-%m-%d"),
                "type": workout.workout_type,
                "duration": workout.duration
            } for workout in last_workouts]
        )
        workout_tip = get_workout_tip(workout_data)
    else:
        workout_tip = "Keep up the great work! Remember to stay hydrated and maintain proper form during your workouts."
    
    # Get nearby locations (using default coordinates for demo)
    # In a real app, you would get these from the user's location
    default_lat = 40.7128  # New York City coordinates
    default_lng = -74.0060
    
    # Get nearby parks and gyms
    parks = get_nearby_locations(default_lat, default_lng, ['16032'])  # Parks category
    gyms = get_nearby_locations(default_lat, default_lng, ['18021'])  # Gyms category
    
    return render(request, 'fitness/dashboard.html', {
        'goals': goals,
        'workouts': workouts,
        'suggestions': suggestions,
        'challenges': challenges,
        'achievements': achievements,
        'progress_stats': progress_stats,
        'total_workouts': total_workouts,
        'total_calories': total_calories,
        'avg_duration': avg_duration,
        'workout_tip': workout_tip,
        'parks': parks,
        'gyms': gyms
    })

@login_required
def coach_dashboard(request):
    if request.user.user_type != 'coach':
        return redirect('dashboard')
    
    users = CustomUser.objects.filter(user_type='user')
    workout_plans = WorkoutPlan.objects.filter(coach=request.user)
    challenges = Challenge.objects.filter(challenger=request.user)
    
    return render(request, 'fitness/coach_dashboard.html', {
        'users': users,
        'workout_plans': workout_plans,
        'challenges': challenges
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

@login_required
def create_workout_plan(request, user_id):
    if request.user.user_type != 'coach':
        return redirect('dashboard')
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        plan_form = WorkoutPlanForm(request.POST)
        if plan_form.is_valid():
            plan = plan_form.save(commit=False)
            plan.coach = request.user
            plan.user = user
            plan.save()
            return redirect('workout_plan_detail', plan_id=plan.id)
    else:
        plan_form = WorkoutPlanForm()
    
    return render(request, 'fitness/create_workout_plan.html', {
        'plan_form': plan_form,
        'user': user
    })

@login_required
def workout_plan_detail(request, plan_id):
    plan = get_object_or_404(WorkoutPlan, id=plan_id)
    exercises = WorkoutPlanExercise.objects.filter(plan=plan)
    
    if request.method == 'POST' and request.user.user_type == 'coach':
        exercise_form = WorkoutPlanExerciseForm(request.POST)
        if exercise_form.is_valid():
            exercise = exercise_form.save(commit=False)
            exercise.plan = plan
            exercise.save()
            return redirect('workout_plan_detail', plan_id=plan.id)
    else:
        exercise_form = WorkoutPlanExerciseForm()
    
    return render(request, 'fitness/workout_plan_detail.html', {
        'plan': plan,
        'exercises': exercises,
        'exercise_form': exercise_form
    })

@login_required
def create_challenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.user, request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.challenger = request.user
            challenge.save()
            messages.success(request, 'Challenge created successfully!')
            return redirect('challenges')
    else:
        form = ChallengeForm(request.user)
    
    return render(request, 'fitness/create_challenge.html', {
        'form': form,
        'title': 'Create Challenge'
    })

@login_required
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    if request.user != challenge.challenger and request.user != challenge.challenged:
        raise Http404("Challenge not found")
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            challenge.status = 'accepted'
            challenge.save()
            messages.success(request, 'Challenge accepted!')
        elif action == 'decline':
            challenge.status = 'declined'
            challenge.save()
            messages.success(request, 'Challenge declined.')
        elif action == 'complete':
            challenge.status = 'completed'
            challenge.completed_at = timezone.now()
            challenge.save()
            messages.success(request, 'Challenge marked as completed!')
        
        return redirect('challenges')
    
    return render(request, 'fitness/challenge_detail.html', {
        'challenge': challenge,
        'title': 'Challenge Details'
    })

@login_required
def challenges(request):
    sent_challenges = Challenge.objects.filter(challenger=request.user)
    received_challenges = Challenge.objects.filter(challenged=request.user)
    
    return render(request, 'fitness/challenges.html', {
        'sent_challenges': sent_challenges,
        'received_challenges': received_challenges,
        'title': 'My Challenges'
    })

@login_required
def log_progress(request):
    if request.method == 'POST':
        form = ProgressStatsForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.save()
            return redirect('dashboard')
    else:
        form = ProgressStatsForm()
    return render(request, 'fitness/log_progress.html', {'form': form})

@login_required
def nearby_locations(request):
    locations = Location.objects.all()
    return render(request, 'fitness/nearby_locations.html', {'locations': locations})

@login_required
def ai_coaching(request):
    if request.method == 'POST':
        form = AICoachingForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            # Here you would integrate with your AI coaching API
            # For now, we'll just save the question
            session.response = "This is a placeholder response. AI integration coming soon!"
            session.save()
            return redirect('ai_coaching_history')
    else:
        form = AICoachingForm()
    
    return render(request, 'fitness/ai_coaching.html', {'form': form})

@login_required
def ai_coaching_history(request):
    sessions = AICoachingSession.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'fitness/ai_coaching_history.html', {'sessions': sessions})

@login_required
def achievements(request):
    completed_goals_count = request.user.goal_set.filter(is_completed=True).count()
    return render(request, 'fitness/achievements.html', {
        'completed_goals_count': completed_goals_count
    })

@login_required
def friends(request):
    # Get current user's friends
    friends = request.user.friends.all()
    
    # Get all users except current user and existing friends
    other_users = CustomUser.objects.exclude(id=request.user.id).exclude(id__in=friends.values_list('id', flat=True))
    
    return render(request, 'fitness/friends.html', {
        'friends': friends,
        'other_users': other_users
    })

@login_required
def add_friend(request, user_id):
    friend = get_object_or_404(CustomUser, id=user_id)
    
    # Add friend relationship
    request.user.friends.add(friend)
    friend.friends.add(request.user)  # Make it mutual
    
    return redirect('friends')

@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(CustomUser, id=user_id)
    request.user.friends.remove(friend)
    friend.friends.remove(request.user)  # Remove mutual friendship
    return redirect('friends')

@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted successfully.')
    return redirect('dashboard')

@login_required
def delete_progress(request, progress_id):
    progress = get_object_or_404(ProgressStats, id=progress_id, user=request.user)
    if request.method == 'POST':
        progress.delete()
        messages.success(request, 'Progress entry deleted successfully.')
    return redirect('dashboard')

@login_required
def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    if request.method == 'POST':
        workout.delete()
        messages.success(request, 'Workout deleted successfully.')
    return redirect('dashboard')

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'fitness/password_reset.html'
    email_template_name = 'fitness/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'fitness/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

@login_required
def profile(request):
    user = request.user
    goals = Goal.objects.filter(user=user)
    workouts = Workout.objects.filter(user=user)
    achievements = UserAchievement.objects.filter(user=user)
    progress_stats = ProgressStats.objects.filter(user=user).order_by('-date')[:5]
    
    return render(request, 'fitness/profile.html', {
        'user': user,
        'goals': goals,
        'workouts': workouts,
        'achievements': achievements,
        'progress_stats': progress_stats
    })

@login_required
def get_workout_tip_ajax(request):
    if not WORKOUT_ASSISTANT_AVAILABLE:
        return JsonResponse({
            'tip': "Keep up the great work! Remember to stay hydrated and maintain proper form during your workouts.",
            'source': 'default'
        })
    
    # Get user's recent data
    goals = Goal.objects.filter(user=request.user, is_completed=False)
    progress = ProgressStats.objects.filter(user=request.user).order_by('-date')[:5]
    last_workouts = Workout.objects.filter(user=request.user).order_by('-date')[:3]
    
    # Format the data
    goals_text = ", ".join([goal.description for goal in goals])
    progress_text = ", ".join([f"{stat.metric}: {stat.value}" for stat in progress])
    workouts_data = [{
        'date': workout.date.strftime('%Y-%m-%d'),
        'type': workout.workout_type,
        'duration': f"{workout.duration} min"
    } for workout in last_workouts]
    
    # Create workout data object
    workout_data = WorkoutData(
        goals=goals_text,
        progress=progress_text,
        last_workouts=workouts_data
    )
    
    # Get the tip
    tip = get_workout_tip(workout_data)
    
    return JsonResponse({
        'tip': tip,
        'source': 'ai'
    })

@login_required
@require_http_methods(["POST"])
def get_nearby_locations_ajax(request):
    try:
        data = json.loads(request.body)
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        
        # Get nearby parks and gyms (limited to 3 each)
        parks = get_nearby_locations(latitude, longitude, ['16032'])[:3]  # Parks category
        gyms = get_nearby_locations(latitude, longitude, ['18021'])[:3]  # Gyms category
        
        return JsonResponse({
            'parks': parks,
            'gyms': gyms
        })
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        return JsonResponse({'error': 'Invalid location data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
