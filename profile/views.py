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
from django.db import DatabaseError, IntegrityError

from profile.models import UserProfile, EmailNotification
from profile.forms import UserProfileForm, EmailNotificationForm

@login_required
def show_profile(request):
    template_name = 'profile.html'
    context = {}

    try:
        notification = EmailNotification.objects.get(user=request.user)
    except ObjectDoesNotExist:
        notification = None

    form = EmailNotificationForm(instance=notification)
    if request.method == 'POST':
        if notification:
            form = EmailNotificationForm(request.POST, instance=notification)
            if form.is_valid():
                print form.cleaned_data
                form.save()
        else:
            form = EmailNotificationForm(request.POST)
            if form.is_valid():
                print form.cleaned_data
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()

    context["emailnotificationform"] = form
    return render_to_response(template_name, context, context_instance=RequestContext(request))

