from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    user contact data, photo, personal information, etc.
    A basic profile which stores user information after the account has been activated.
    Use this model as the value of the ``AUTH_PROFILE_MODULE`` setting
    """
    user = models.ForeignKey(User, editable=False, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.IntegerField(max_length=5, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def fullname(self):
        return "%s, %s" %(self.last_name,self.first_name)
        fullname.short_description = 'Full Name'

    class Meta:
        ordering = ['last_name']


class EmailNotification(models.Model):
    """
    """
    user = models.ForeignKey(User, editable=False, unique=True)
    dailyreminder = models.BooleanField(default=False)
    weeklysummary = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s" % (self.user)
