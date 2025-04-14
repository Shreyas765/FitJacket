from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('set-goal/', views.set_goal, name='set_goal'),
    path('log-workout/', views.log_workout, name='log_workout'),
] 