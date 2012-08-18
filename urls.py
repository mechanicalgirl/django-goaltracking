from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logout/logout.html'}),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^about/$',  direct_to_template,  {'template': 'about.html'}),

    url(r'^getstarted/', include('django-goaltracking.goals.urls')),
    url(r'^goals/', include('django-goaltracking.goals.urls')),
    url(r'^$', include('django-goaltracking.goals.urls')),
)
