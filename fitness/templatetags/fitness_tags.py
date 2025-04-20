from django import template
from ..models import Goal

register = template.Library()

@register.filter
def filter_goals(goals, is_completed):
    return [goal for goal in goals if goal.is_completed == is_completed] 