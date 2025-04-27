from django.db import migrations
from django.core.files import File
import os

def add_initial_achievements(apps, schema_editor):
    Achievement = apps.get_model('fitness', 'Achievement')
    achievements_data = [
        {
            'name': 'First Workout',
            'description': 'Complete your first workout',
            'criteria': 'Complete 1 workout',
        },
        {
            'name': 'Workout Streak',
            'description': 'Work out for 7 days in a row',
            'criteria': 'Workout streak of 7 days',
        },
        {
            'name': 'Weekend Warrior',
            'description': 'Work out on both Saturday and Sunday',
            'criteria': 'Weekend warrior',
        },
        {
            'name': 'Calorie Master',
            'description': 'Burn 1000 calories in total',
            'criteria': 'Calorie master',
        },
        {
            'name': 'Workout Master',
            'description': 'Complete 50 workouts',
            'criteria': 'Complete 50 workouts',
        },
        {
            'name': 'Early Bird',
            'description': 'Complete a workout before 7 AM',
            'criteria': 'Complete a workout before 7 AM',
        },
        {
            'name': 'Social Butterfly',
            'description': 'Add 5 friends',
            'criteria': 'Add 5 friends',
        },
        {
            'name': 'Challenge Champion',
            'description': 'Complete 3 challenges',
            'criteria': 'Complete 3 challenges',
        },
        {
            'name': 'Goal Achiever',
            'description': 'Complete 5 goals',
            'criteria': 'Complete 5 goals',
        },
        {
            'name': 'Consistent Progress',
            'description': 'Log progress for 30 days',
            'criteria': 'Log progress for 30 days',
        },
        {
            'name': 'Cardio King/Queen',
            'description': 'Complete 20 cardio workouts',
            'criteria': 'Complete 20 cardio workouts',
        },
        {
            'name': 'Strength Warrior',
            'description': 'Complete 20 strength training workouts',
            'criteria': 'Complete 20 strength training workouts',
        },
        {
            'name': 'Flexibility Master',
            'description': 'Complete 20 flexibility workouts',
            'criteria': 'Complete 20 flexibility workouts',
        },
        {
            'name': 'HIIT Hero',
            'description': 'Complete 20 HIIT workouts',
            'criteria': 'Complete 20 HIIT workouts',
        },
        {
            'name': 'Location Explorer',
            'description': 'Work out at 5 different locations',
            'criteria': 'Work out at 5 different locations',
        },
        {
            'name': 'Progress Pro',
            'description': 'Log progress for 7 consecutive days',
            'criteria': 'Log progress for 7 consecutive days',
        },
        {
            'name': 'Goal Crusher',
            'description': 'Complete a goal before its target date',
            'criteria': 'Complete a goal before its target date',
        },
        {
            'name': 'Workout Variety',
            'description': 'Complete at least one workout of each type',
            'criteria': 'Complete at least one workout of each type',
        },
        {
            'name': 'Morning Person',
            'description': 'Complete 10 workouts before 9 AM',
            'criteria': 'Complete 10 workouts before 9 AM',
        },
        {
            'name': 'Night Owl',
            'description': 'Complete 10 workouts after 8 PM',
            'criteria': 'Complete 10 workouts after 8 PM',
        },
        {
            'name': 'Weekday Warrior',
            'description': 'Work out on all 5 weekdays',
            'criteria': 'Work out on all 5 weekdays',
        },
        {
            'name': 'Calorie Burner',
            'description': 'Burn 500 calories in a single workout',
            'criteria': 'Burn 500 calories in a single workout',
        },
        {
            'name': 'Endurance Expert',
            'description': 'Complete a workout lasting more than 60 minutes',
            'criteria': 'Complete a workout lasting more than 60 minutes',
        },
        {
            'name': 'Consistency King/Queen',
            'description': 'Work out at least 3 times a week for a month',
            'criteria': 'Work out at least 3 times a week for a month',
        },
        {
            'name': 'Fitness Guru',
            'description': 'Earn 10 different achievements',
            'criteria': 'Earn 10 different achievements',
        }
    ]

    for achievement_data in achievements_data:
        achievement = Achievement.objects.create(
            name=achievement_data['name'],
            description=achievement_data['description'],
            criteria=achievement_data['criteria'],
        )
        # You would need to add badge images here if you have them

def remove_initial_achievements(apps, schema_editor):
    Achievement = apps.get_model('fitness', 'Achievement')
    Achievement.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('fitness', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_achievements, remove_initial_achievements),
    ] 