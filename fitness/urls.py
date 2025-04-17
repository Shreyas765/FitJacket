from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('coach-dashboard/', views.coach_dashboard, name='coach_dashboard'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('feedback/<str:model_type>/<int:item_id>/', views.provide_feedback, name='provide_feedback'),
    path('suggestion/<int:suggestion_id>/read/', views.mark_suggestion_read, name='mark_suggestion_read'),
    path('set-goal/', views.set_goal, name='set_goal'),
    path('log-workout/', views.log_workout, name='log_workout'),
] 