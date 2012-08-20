from django import template
from django.core.exceptions import ObjectDoesNotExist

from goals.models import Goal, Goalset, Date, Dateset, Activity, Quote

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

def goal_activity(id):
    # id is a dateset.id 
    activity_list = []
    try:
        dateset = Dateset.objects.get(pk=id)

        date_one = Date.objects.get(pk=dateset.date_one_id)
        act_one = Activity.objects.filter(date=date_one.id)
        for act in act_one:
            activity = {}
            activity['goal'] = act.date.goal.name
            activity['activity'] = act.description
            activity_list.append(activity)

        date_two = Date.objects.get(pk=dateset.date_two_id)
        act_two = Activity.objects.filter(date=date_two.id)
        for act in act_two:
            activity = {}
            activity['goal'] = act.date.goal.name
            activity['activity'] = act.description
            activity_list.append(activity)

        date_three = Date.objects.get(pk=dateset.date_three_id)
        act_three = Activity.objects.filter(date=date_three.id)
        for act in act_three:
            activity = {}
            activity['goal'] = act.date.goal.name
            activity['activity'] = act.description
            activity_list.append(activity)

        date_four = Date.objects.get(pk=dateset.date_four_id)
        act_four = Activity.objects.filter(date=date_four.id)
        for act in act_four:
            activity = {}
            activity['goal'] = act.date.goal.name
            activity['activity'] = act.description
            activity_list.append(activity)

    except ObjectDoesNotExist:
        pass

    return activity_list
register.filter('goal_activity', goal_activity)


def goal_activity_dates(id):
    # id is a dateset.id 
    try:
        dateset = Dateset.objects.get(pk=id)
	date = "Week " + str(dateset.date_one.week)
        date += ", Day " + str(dateset.date_one.day) + " : "
        date += dateset.date_one.activity_date.strftime("%b %d, %Y")
    except ObjectDoesNotExist:
        pass

    return date
register.filter('goal_activity_dates', goal_activity_dates)

