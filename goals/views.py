from datetime import datetime
from datetime import timedelta
import sys

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q
from django.db import DatabaseError, IntegrityError

from goals.models import Goal, Goalset, Date, Dateset, Activity
from goals.forms import GoalForm, GoalsetForm, DateForm, DatesetForm, ActivityForm

@login_required
def show_home(request):
    template_name = 'home.html'
    context = {}

    try:
        # user has a goal set in progress
        goalset = Goalset.objects.get(active_date__lte=datetime.now(), 
            complete_date__isnull=True, goal_one__user=request.user)
        context['goalset'] = goalset
    except ObjectDoesNotExist:
        goalset = None

    if goalset == None:
        if 'getstarted' in request.path:
            context["getstarted"] = True
        try:
            goalpool = Goal.objects.filter(complete=False).filter(user=request.user).order_by('id')

            if len(goalpool) >= 4:
                # user is ready to define a goal set
                context["ready"] = True
                context["setform"] = GoalsetForm(user=request.user)
                context["goalform"] = GoalForm()
            else:
                # user is not ready to start a goal set - must add more goals to the pool
                context["ready"] = False
                context["setform"] = False
                context["goalform"] = GoalForm()
                context["howmanymore"] = 4-len(goalpool)

            context["goalpool"] = goalpool

        except ObjectDoesNotExist:
            # user does not have any available goals - either completed all, or has not added any
            goalpool = None

    else:
        today = datetime.now().date()
        dates = Dateset.objects.filter(
            Q(date_one__activity_date__lte=today, complete=False) | 
            Q(date_one__activity_date=today),
            date_one__goal__user=request.user).order_by('-date_one__activity_date')
        if len(dates) == 0:
            dates = Dateset.objects.filter(complete=True, 
                date_one__goal__user=request.user).order_by('-date_one__activity_date')[0:1]

        context["dates"] = dates
        context["activityform"] = ActivityForm()
        context["dateform"] = DateForm()
        context["datesetform"] = DatesetForm()

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
def show_summary(request, id=None):
    context = {}

    if id:
        template_name = 'goal_summary.html'
        try:
            dateset = Dateset.objects.get(pk=id)
            ## TODO: clean this up:
            date_one = Date.objects.get(pk=dateset.date_one_id)
            context['act_one'] = Activity.objects.filter(date=date_one.id)
            date_two = Date.objects.get(pk=dateset.date_two_id)
            context['act_two'] = Activity.objects.filter(date=date_two.id)
            date_three = Date.objects.get(pk=dateset.date_three_id)
            context['act_three'] = Activity.objects.filter(date=date_three.id)
            date_four = Date.objects.get(pk=dateset.date_four_id)
            context['act_four'] = Activity.objects.filter(date=date_four.id)
        except ObjectDoesNotExist:
           ## TODO: redirect to an error page
           return HttpResponseRedirect('/')

    else:
        template_name = 'summary.html'
        try:
            goalset = Goalset.objects.get(active_date__lte=datetime.now(),
                complete_date__isnull=True, goal_one__user=request.user)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/')

        if goalset:  # user has a goal set in progress
            context['goalset'] = goalset

            datesets_total = Dateset.objects.filter(date_one__goal__user=request.user).order_by('date_one__activity_date')
            datesets_complete = Dateset.objects.filter(date_one__goal__user=request.user, complete=True)
            context["datesets"] = datesets_total
            context["percent_complete"] = 100 * float(len(datesets_complete)) / float(len(datesets_total))

    return render_to_response(template_name, context, context_instance=RequestContext(request))

@login_required
def goal_set(request):
    template_name = 'home.html'
    try:
        del request.session['goal_set_errors']
    except KeyError:
        pass
    if request.method == 'POST': 
        if 'goback' in request.POST:
            return HttpResponseRedirect('/')
        else:
            form = GoalsetForm(request.POST) 
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()

                goalset = Goalset.objects.get(pk=obj.pk)
                goals = [goalset.goal_one.id, goalset.goal_two.id, goalset.goal_three.id, goalset.goal_four.id]

                start = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
                for g in goals:
                    for w in range(12):
                        for d in range(5):
                            newform = DateForm()
                            newobj = newform.save(commit=False)
                            newobj.goal = Goal.objects.get(pk=g)
                            newobj.week = w+1
                            newobj.day = d+1
                            newdate = (start + timedelta((7*w)) + timedelta(d))
                            newobj.activity_date = newdate
                            newobj.save()

                dateset = Date.objects.values('activity_date').filter(goal__in=goals)
                dates = set()
                for newdate in dateset:
                    sdate = newdate["activity_date"]
                    dates.add(sdate)
                for xdate in dates:
                    dobjs = Date.objects.filter(activity_date=xdate, goal__in=goals)
                    dsform = DatesetForm({'date_one': dobjs[0].id, 'date_two': dobjs[1].id, 
                        'date_three': dobjs[2].id, 'date_four': dobjs[3].id})
                    dsform.save()

                return HttpResponseRedirect('/')

            else: # form is not valid
                errors = dict(form.errors.items())
                request.session['goal_set_errors'] = errors
                return HttpResponseRedirect('/')

    return HttpResponseRedirect('/')

@login_required
def goal_add(request):
    template_name = 'home.html'
    try:
        del request.session['goal_add_errors']
    except KeyError:
        pass
    if request.method == 'POST':
        if 'getstarted' in request.POST:
            return HttpResponseRedirect('/getstarted/')
        if 'add' in request.POST:
            form = GoalForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
            else:
                errors = dict(form.errors.items()) 
                request.session['goal_add_errors'] = errors
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')


@login_required
def goal_remove(request,id):
    template_name = 'home.html'
    if request.method == 'POST':
        if 'remove' in request.POST:
            u = Goal.objects.get(pk=id).delete()
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

@login_required
def add_activity(request, id):
    template_name = 'home.html'
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.date = Date.objects.get(pk=id)
            obj.save()
            return HttpResponseRedirect('/')

    return HttpResponseRedirect('/')

@login_required
def close_dateset(request, id):
    template_name = 'home.html'
    if request.method == 'POST':
        dateset = Dateset.objects.get(pk=id)
        dateset.complete = True
        dateset.save()
        return HttpResponseRedirect('/')

    return HttpResponseRedirect('/')

