from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from profile.models import UserProfile, EmailNotification

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

class EmailNotificationForm(forms.ModelForm):
    class Meta:
        model = EmailNotification

