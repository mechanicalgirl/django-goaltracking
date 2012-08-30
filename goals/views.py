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

from goals.models import Goal, Goalset, Date, Dateset, Activity, Copy
from goals.forms import GoalForm, GoalsetForm, DateForm, DatesetForm, ActivityForm

@login_required
def show_home(request):
    """
    This function handles the several conditions that can occur when
    a logged-in user hits the home page, returning views for:
    1) Users who have not yet begun the process of adding goals
    2) Users who have added goals but not yet started a goal set
    3) Users with an active goal set
    4) Users who have completed a goal set
    """
    template_name = 'home.html'
    context = {}

    try:
        goalset = Goalset.objects.get(active_date__lte=datetime.now(), 
            complete_date__isnull=True, goal_one__user=request.user)
        context['goalset'] = goalset
    except ObjectDoesNotExist:
        goalset = None

    # user is not working on an active set of four goals
    if goalset == None:
        if 'getstarted' in request.path:
            context["getstarted"] = True
        try:
            # user has a list of goals but has not yet selected a set of four to work on
            goalpool = Goal.objects.filter(complete=False).filter(user=request.user).order_by('id')

            if len(goalpool) >= 4: # user is ready to define a goal set
                context["ready"] = True
                context["setform"] = GoalsetForm(user=request.user)
                context["goalform"] = GoalForm()
            else: # user is not ready to start a goal set - must add more goals to the pool
                context["ready"] = False
                context["setform"] = False
                context["goalform"] = GoalForm()
                context["howmanymore"] = 4-len(goalpool)

            context["goalpool"] = goalpool

        except ObjectDoesNotExist:
            # user does not have any available goals - either completed all, or has not added any
            goalpool = None

    # user has a goal set in progress
    else:
        datesets_complete = Dateset.objects.filter(date_one__goal__user=request.user, complete=True)
        datesets_remaining = 60 - len(datesets_complete)

        today = datetime.now().date()
        dates = Dateset.objects.filter(
            Q(date_one__activity_date__lte=today, complete=False) | 
            Q(date_one__activity_date=today),
            date_one__goal__user=request.user).order_by('-date_one__activity_date')

        # if no open datesets are returned
        if len(dates) == 0:
            # then just get the latest closed dateset
            dates = Dateset.objects.filter(complete=True,
                date_one__goal__user=request.user).order_by('-date_one__activity_date')[0:1]

            if datesets_remaining == 0:  
                # when there are no goals left, let the user know the set is complete
                return HttpResponseRedirect('/goals/complete/')

        context["datesets_complete"] = len(datesets_complete)
        context["datesets_remaining"] = datesets_remaining

        context["dates"] = dates
        context["activityform"] = ActivityForm()
        context["dateform"] = DateForm()
        context["datesetform"] = DatesetForm()

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
def show_summary(request, id=None):
    """
    This method returns either:
    1) a summary of activity for a specific date set
    2) a summary of all activity for a user's current goal set
    """
    context = {}

    if id:
        # if an id is passed in, show the single date set summary
        template_name = 'goal_summary.html'
        try:
            dateset = Dateset.objects.get(pk=id)
            date_one = Date.objects.get(pk=dateset.date_one_id)
            context['act_one'] = Activity.objects.filter(date=date_one.id)
            date_two = Date.objects.get(pk=dateset.date_two_id)
            context['act_two'] = Activity.objects.filter(date=date_two.id)
            date_three = Date.objects.get(pk=dateset.date_three_id)
            context['act_three'] = Activity.objects.filter(date=date_three.id)
            date_four = Date.objects.get(pk=dateset.date_four_id)
            context['act_four'] = Activity.objects.filter(date=date_four.id)
        except ObjectDoesNotExist:
           return HttpResponseRedirect('/')

    else:
        # otherwise show the complete summary for the request user
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
def show_complete(request):
    """
    Users who have completed a current goal set are redirected to '/goals/complete/'
    This function gives the user an opportunity to close out the active 
    goal set while still leaving some goals available for further work.
    """
    template_name = 'complete.html'
    context = {}

    try:
        goalset = Goalset.objects.get(active_date__lte=datetime.now(),
            complete_date__isnull=True, goal_one__user=request.user)
        context['goalset'] = goalset
        goals = [goalset.goal_one.id, goalset.goal_two.id, goalset.goal_three.id, goalset.goal_four.id]
        goalsetform = GoalsetForm(instance=goalset)
        context['goalsetform'] = goalsetform
    except ObjectDoesNotExist:
        goalset = None

    if goalset == None:
        return HttpResponseRedirect('/')
    else:
        datesets_complete = Dateset.objects.filter(date_one__goal__user=request.user, complete=True)
        datesets_remaining = 60 - len(datesets_complete)
        if datesets_remaining > 0:
            return HttpResponseRedirect('/')
        else:
            if request.method == 'POST':
                if 'finish' in request.POST:
                    # 1) add a completed date to the goalset object
                    obj = goalsetform.save(commit=False)
                    obj.complete_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
                    obj.save()

                    # 2) update included goal objects to complete=True
                    goals = [k for k in request.POST if k.isdigit()]
                    for g in goals:
                        goal = Goal.objects.get(pk=g)
                        goalform = GoalForm(instance=goal)
                        obj = goalform.save(commit=False)
                        obj.complete = True
                        obj.save()

                return HttpResponseRedirect('/')

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
def show_mobile(request):
    """
    This function handles the mobile view, returns context also 
    included in the home and summary views
    """
    template_name = 'mobile.html'
    context = {}

    try:
        goalset = Goalset.objects.get(active_date__lte=datetime.now(),
            complete_date__isnull=True, goal_one__user=request.user)
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
        # user has a goal set in progress
        datesets_complete = Dateset.objects.filter(date_one__goal__user=request.user, complete=True)
        datesets_remaining = 60 - len(datesets_complete)
        datesets_total = Dateset.objects.filter(date_one__goal__user=request.user).order_by('date_one__activity_date')
        context["datesets"] = datesets_total
        context["percent_complete"] = 100 * float(len(datesets_complete)) / float(len(datesets_total))
        context["datesets_complete"] = len(datesets_complete)
        context["datesets_remaining"] = datesets_remaining

        today = datetime.now().date()
        dates = Dateset.objects.filter(
            Q(date_one__activity_date__lte=today, complete=False) |
            Q(date_one__activity_date=today),
            date_one__goal__user=request.user).order_by('-date_one__activity_date')

        if len(dates) == 0:  # if no open datesets are returned
            # get the latest closed dateset
            dates = Dateset.objects.filter(complete=True,
                date_one__goal__user=request.user).order_by('-date_one__activity_date')[0:1]

            if datesets_remaining == 0:
                # when there are no goals left, let the user know the set is complete
                return HttpResponseRedirect('/goals/complete/')

        context["dates"] = dates
        context["activityform"] = ActivityForm()
        context["dateform"] = DateForm()
        context["datesetform"] = DatesetForm()

        context['goalset'] = goalset

    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required
def goal_set(request):
    """
    This function handles the creation of an active goal set for a user:
    1) checks that the user has enough goals available to create a set
    2) on goal set save, also creates the necessary date and date sets
    """
    template_name = 'home.html'

    try: del request.session['goal_set_errors']
    except KeyError: pass

    redir = '/'

    if request.method == 'POST': 
        if 'goback' in request.POST:
            redir = '/'
        if 'goback-mobile' in request.POST:
            redir = '/goals/mobile/'
        if 'commit-mobile' in request.POST:
            redir = '/goals/mobile/'

        form = GoalsetForm(request.POST) 
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            goalset = Goalset.objects.get(pk=obj.pk)
            goals = [goalset.goal_one.id, goalset.goal_two.id, goalset.goal_three.id, goalset.goal_four.id]

            # generate and save 240 goal dates
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

            # group and save into 60 date sets
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

            return HttpResponseRedirect(redir)

        else: 
            # form is not valid
            errors = dict(form.errors.items())
            request.session['goal_set_errors'] = errors
            return HttpResponseRedirect(redir)

    return HttpResponseRedirect(redir)

@login_required
def goal_add(request):
    """
    Handles the form post for adding a new goal
    """
    template_name = 'home.html'

    try:
        del request.session['goal_add_errors']
    except KeyError:
        pass

    redir = '/'

    if request.method == 'POST':

        if 'getstarted-mobile' in request.POST:
            redir = '/goals/mobile/getstarted/'
        if 'getstarted' in request.POST:
            redir = '/getstarted/'
        if 'add-mobile' in request.POST:
            redir = '/goals/mobile/'

        if 'add' or 'add-mobile' in request.POST:
            form = GoalForm(request.POST, user=request.user)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
            else:
                errors = dict(form.errors.items()) 
                request.session['goal_add_errors'] = errors

            return HttpResponseRedirect(redir)

    return HttpResponseRedirect(redir)


@login_required
def goal_remove(request,id):
    """
    Handles the form post for removing a goal
    """
    template_name = 'home.html'

    redir = '/'
    if 'remove-mobile' in request.POST:
        redir = '/goals/mobile/'
    
    if request.method == 'POST':
        if 'remove' in request.POST:
            u = Goal.objects.get(pk=id).delete()
            return HttpResponseRedirect(redir)
    return HttpResponseRedirect(redir)

@login_required
def add_activity(request, id):
    """
    Handles the form post for adding an activity
    related to a goal and dateset
    """
    template_name = 'home.html'

    redir = '/'
    if 'activity-mobile' in request.POST:
        redir = '/goals/mobile/'

    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.date = Date.objects.get(pk=id)
            obj.save()
            return HttpResponseRedirect(redir)

    return HttpResponseRedirect(redir)

@login_required
def close_dateset(request, id):
    """
    Handles the form post for closing out a dateset
    """
    template_name = 'home.html'

    redir = '/'
    if 'date-complete-mobile' in request.POST:
        redir = '/goals/mobile/'

    if request.method == 'POST':
        dateset = Dateset.objects.get(pk=id)
        dateset.complete = True
        dateset.save()
        return HttpResponseRedirect(redir)

    return HttpResponseRedirect(redir)

