from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from profile import views

urlpatterns = patterns('',
    url(r'^$',          views.show_profile,        name='profile_home'),
)

