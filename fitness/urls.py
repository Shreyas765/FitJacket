from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetCompleteView
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='fitness/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name='fitness/password_reset_complete.html'), name='password_reset_complete'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    
    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('coach-dashboard/', views.coach_dashboard, name='coach_dashboard'),
    
    # Goal and Workout URLs
    path('set-goal/', views.set_goal, name='set_goal'),
    path('log-workout/', views.log_workout, name='log_workout'),
    path('log-progress/', views.log_progress, name='log_progress'),
    
    # Workout Plan URLs
    path('create-workout-plan/<int:user_id>/', views.create_workout_plan, name='create_workout_plan'),
    path('workout-plan/<int:plan_id>/', views.workout_plan_detail, name='workout_plan_detail'),
    
    # Challenge URLs
    path('challenges/', views.challenges, name='challenges'),
    path('challenges/create/', views.create_challenge, name='create_challenge'),
    path('challenges/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    
    # Social URLs
    path('friends/', views.friends, name='friends'),
    path('add_friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('remove_friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('delete_goal/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    path('delete_progress/<int:progress_id>/', views.delete_progress, name='delete_progress'),
    path('delete_workout/<int:workout_id>/', views.delete_workout, name='delete_workout'),
    
    # Achievement URLs
    path('achievements/', views.achievements, name='achievements'),
    
    # Location URLs
    path('nearby-locations/', views.nearby_locations, name='nearby_locations'),
    
    # AI Coaching URLs
    path('ai-coaching/', views.ai_coaching, name='ai_coaching'),
    path('ai-coaching/history/', views.ai_coaching_history, name='ai_coaching_history'),
    
    # Coach URLs
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('feedback/<str:model_type>/<int:item_id>/', views.provide_feedback, name='provide_feedback'),
    path('suggestion/<int:suggestion_id>/read/', views.mark_suggestion_read, name='mark_suggestion_read'),
    path('get-workout-tip/', views.get_workout_tip_ajax, name='get_workout_tip'),
    path('get-nearby-locations/', views.get_nearby_locations_ajax, name='get_nearby_locations'),
] 