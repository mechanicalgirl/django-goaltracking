from django import template
from django.core.exceptions import ObjectDoesNotExist

from django-goaltracking.goals.models import Goal, Goalset, Date, Dateset, Activity, Quote

register = template.Library()

def date_activity(id):
    activity_list = []
    try:
        activities = Activity.objects.filter(date=id)
    except ObjectDoesNotExist:
        activities = None
    for activity in activities:
        activity_list.append(activity.description)
    return activity_list
register.filter('date_activity', date_activity)

