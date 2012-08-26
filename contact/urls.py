from django.conf.urls.defaults import *
from django.contrib.comments.models import Comment
from django.views.generic.simple import direct_to_template

from contact import views

urlpatterns = patterns('',
    url(r'^$',          views.contact,       name='contact_contact'),
)
