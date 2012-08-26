# from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import password_reset

from django.contrib import admin
admin.autodiscover()

# using django-registration
from registration.views import activate
from registration.views import register

urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logout/logout.html'}),

    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', \
            {'template_name': 'accounts/password/password_reset.html'}),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done', \
            {'template_name': 'accounts/password/password_reset_done.html'}),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', \
            'django.contrib.auth.views.password_reset_confirm', \
            {'template_name': 'accounts/password/password_reset_confirm.html'}),
    url(r'^password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', \
            {'template_name': 'accounts/password/password_reset_complete.html'}),

    # using django-registration
    url(r'^activate/complete/$', direct_to_template, {'template': 'activation_complete.html'}, name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$', activate, {'backend': 'registration.backends.default.DefaultBackend'}, name='registration_activate'),
    url(r'^register/$', register, {'backend': 'registration.backends.default.DefaultBackend'}, name='registration_register'),
    url(r'^register/complete/$', direct_to_template, {'template': 'registration_complete.html'}, name='registration_complete'),
    url(r'^register/closed/$', direct_to_template, {'template': 'registration_closed.html'}, name='registration_disallowed'),
    (r'', include('registration.auth_urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^about/$', direct_to_template, {'template': 'about.html'}),
    url(r'^contact/', include('django-goaltracking.contact.urls')),
    url(r'^getstarted/', include('django-goaltracking.goals.urls')),
    url(r'^goals/', include('django-goaltracking.goals.urls')),
    url(r'^profile/', include('django-goaltracking.profile.urls')),
    url(r'^$', include('django-goaltracking.goals.urls')),
)
